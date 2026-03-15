#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    plugins.nvenc.py

    Written by:               Josh.5 <jsunnex@gmail.com>
    Date:                     16 Dec 2025, (09:36 AM)

    Copyright:
        Copyright (C) 2021 Josh Sunnex

        This program is free software: you can redistribute it and/or modify it under the terms of the GNU General
        Public License as published by the Free Software Foundation, version 3.

        This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the
        implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License
        for more details.

        You should have received a copy of the GNU General Public License along with this program.
        If not, see <https://www.gnu.org/licenses/>.

"""

import logging
import os
import re
import json
import subprocess
import math
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple


logger = logging.getLogger("Unmanic.Plugin.video_transcoder")


@dataclass
class SourceStats:
    """Snapshot of the source used to build recommendations."""

    width: int
    height: int
    codec_name: Optional[str]
    bit_depth: Optional[int]
    duration: Optional[float]
    stream_bitrate: Optional[int]
    container_bitrate: Optional[int]
    filesize_bits: Optional[int]
    derived_bitrate: Optional[int]
    is_hdr: bool
    pix_fmt: Optional[str]
    fps: Optional[float]
    confidence: bool
    confidence_level: str
    confidence_notes: list


class SmartOutputTargetHelper:
    """Human-readable helper for selecting sane encoder params in Basic mode."""

    _LOG_PREFIX = "[SmartOutputTargetHelper]"

    GOAL_PREFER_QUALITY = "prefer_quality"
    GOAL_BALANCED = "balanced"
    GOAL_PREFER_COMPRESSION = "prefer_compression"

    QUALITY_CONST = "const_quality"
    QUALITY_CAPPED = "capped_quality"
    QUALITY_TARGET = "target_bitrate"

    _GOALS = {GOAL_PREFER_QUALITY, GOAL_BALANCED, GOAL_PREFER_COMPRESSION}

    # This table provides a selection of factors for each goal that modifies how aggressively to cap bitrate.
    # Goal adjusts the cap headroom (Prefer Quality keeps more bitrate, Prefer Compression clamps harder) relative
    # to the source-per-pixel when scaling, to avoid inflating downscales or starving upscales when deriving
    # maxrate/bufsize rails from the source bitrate.
    _CAP_FACTORS = {
        GOAL_PREFER_QUALITY:     1.3,
        GOAL_BALANCED:           1.1,
        GOAL_PREFER_COMPRESSION: 0.9,
    }

    # This table provides per-resolution thresholds that decide when a low-bitrate source should fall back from constqp to VBR.
    # sd/hd/uhd buckets raise the bar for what counts as "already low bitrate" before forcing the safer mode.
    _LOW_BITRATE_THRESHOLDS = {
        "sd": 800_000,
        "hd": 2_500_000,
        "uhd": 6_000_000,
    }

    # This table provides CQ ladders keyed by codec -> goal -> dynamic range -> resolution bucket.
    # Codec nudges the ladder based on encoder behaviour (hevc/h264/av1); goal balances size vs fidelity;
    # HDR entries lower CQ to reduce banding risk; sd/hd/uhd buckets scale quantisers with detail expectations.
    _BASE_QUALITY_LADDERS = {
        "hevc": {
            GOAL_PREFER_COMPRESSION: {
                "sdr": {"sd": 27, "hd": 28, "uhd": 29},
                "hdr": {"sd": 26, "hd": 27, "uhd": 28},
            },
            GOAL_BALANCED: {
                "sdr": {"sd": 25, "hd": 26, "uhd": 27},
                "hdr": {"sd": 24, "hd": 25, "uhd": 26},
            },
            GOAL_PREFER_QUALITY: {
                "sdr": {"sd": 23, "hd": 24, "uhd": 25},
                "hdr": {"sd": 22, "hd": 23, "uhd": 24},
            },
        },
        "h264": {
            GOAL_PREFER_COMPRESSION: {
                "sdr": {"sd": 24, "hd": 25, "uhd": 26},
                "hdr": {"sd": 23, "hd": 24, "uhd": 25},
            },
            GOAL_BALANCED: {
                "sdr": {"sd": 22, "hd": 23, "uhd": 24},
                "hdr": {"sd": 21, "hd": 22, "uhd": 23},
            },
            GOAL_PREFER_QUALITY: {
                "sdr": {"sd": 20, "hd": 21, "uhd": 22},
                "hdr": {"sd": 19, "hd": 20, "uhd": 21},
            },
        },
        "av1": {
            GOAL_PREFER_COMPRESSION: {
                "sdr": {"sd": 27, "hd": 28, "uhd": 29},
                "hdr": {"sd": 26, "hd": 27, "uhd": 28},
            },
            GOAL_BALANCED: {
                "sdr": {"sd": 24, "hd": 25, "uhd": 26},
                "hdr": {"sd": 23, "hd": 24, "uhd": 25},
            },
            GOAL_PREFER_QUALITY: {
                "sdr": {"sd": 22, "hd": 23, "uhd": 24},
                "hdr": {"sd": 21, "hd": 22, "uhd": 23},
            },
        },
    }

    # This table provides CQ bias offsets keyed by (source_codec, target_codec).
    # Efficient source codecs (hevc/av1/vp9) get negative offsets to preserve quality; h264 -> hevc can take a small
    # positive offset for extra compression; matching codecs lean negative to reduce generational loss.
    _REENCODE_CQ_OFFSETS = {
        ("h264", "hevc"): 1,
        ("hevc", "hevc"): -1,
        ("hevc", "h264"): -2,
        ("av1", "hevc"): -1,
        ("av1", "h264"): -2,
        ("av1", "av1"): -1,
        ("hevc", "av1"): -1,
        ("h264", "h264"): 0,
        ("vp9", "hevc"): -1,
        ("vp9", "h264"): -2,
        ("vp9", "av1"): -1,
        ("vp9", "vp9"): -1,
    }

    # Minimum bits-per-pixel-per-frame guardrails, scaled by goal, HDR, and FPS bucket.
    # Higher FPS buckets demand more minimum bitrate; HDR entries give a small bump to reduce banding risk.
    _MIN_BPPPF = {
        GOAL_PREFER_QUALITY: {
            "sdr": {"low_motion": 0.050, "medium_motion": 0.060, "high_motion": 0.070},
            "hdr": {"low_motion": 0.055, "medium_motion": 0.065, "high_motion": 0.075},
        },
        GOAL_BALANCED: {
            "sdr": {"low_motion": 0.040, "medium_motion": 0.050, "high_motion": 0.060},
            "hdr": {"low_motion": 0.045, "medium_motion": 0.055, "high_motion": 0.065},
        },
        GOAL_PREFER_COMPRESSION: {
            "sdr": {"low_motion": 0.033, "medium_motion": 0.040, "high_motion": 0.048},
            "hdr": {"low_motion": 0.038, "medium_motion": 0.045, "high_motion": 0.053},
        },
    }

    # Codec/encoder efficiency scalers for bitrate floors (lower means more efficient output).
    _CODEC_EFFICIENCY = {
        ("libx265", "hevc"): 0.75,
        ("hevc_nvenc", "hevc"): 0.85,
        ("hevc_qsv", "hevc"): 0.82,
        ("libx264", "h264"): 1.0,
        ("h264_nvenc", "h264"): 1.05,
        ("h264_qsv", "h264"): 1.02,
        ("libsvtav1", "av1"): 0.65,
        ("av1_nvenc", "av1"): 0.70,
        ("av1_qsv", "av1"): 0.70,
        ("vp9_vaapi", "vp9"): 0.90,
        # Codec-only fallbacks
        "h264": 1.0,
        "hevc": 0.80,
        "av1": 0.65,
        "vp9": 0.85,
    }

    def __init__(self, probe, max_probe_seconds: float = 2.0):
        self.probe = probe
        self.max_probe_seconds = max_probe_seconds

    # --------------------------
    # Parsing helpers
    # --------------------------
    def _safe_int(self, value: Optional[str]) -> Optional[int]:
        try:
            return int(value)
        except (TypeError, ValueError):
            return None

    def _safe_float(self, value: Optional[str]) -> Optional[float]:
        try:
            return float(value)
        except (TypeError, ValueError):
            return None

    def _clamp(self, value: float, min_value: float, max_value: float) -> float:
        return max(min_value, min(value, max_value))

    def _parse_duration_hhmmss(self, duration_tag: Optional[str]) -> Optional[float]:
        """
        Parse common duration formats found in Matroska statistics tags.

        Examples:
            "00:10:34.534000000" -> 634.534
            "0:10:34.534" -> 634.534
        """
        if not duration_tag or not isinstance(duration_tag, str) or ":" not in duration_tag:
            return None
        try:
            h, m, s = duration_tag.split(":")
            return float(h) * 3600 + float(m) * 60 + float(s)
        except (ValueError, TypeError):
            return None

    def _get_tag_value(self, tags: Optional[Dict], key: str) -> Optional[str]:
        """
        Fetch a tag value from an ffprobe `tags` dict, supporting common variants like `-eng`
        and case differences across containers and muxers.
        """
        if not isinstance(tags, dict) or not key:
            return None

        candidates = (
            key,
            key.upper(),
            key.lower(),
            f"{key}-eng",
            f"{key.upper()}-eng",
            f"{key.lower()}-eng",
        )
        for candidate in candidates:
            if candidate in tags:
                return tags.get(candidate)

        key_lower = key.lower()
        for tag_key, tag_value in tags.items():
            if str(tag_key).lower() in (key_lower, f"{key_lower}-eng"):
                return tag_value
        return None

    def _max_samples_for_even_gap(
        self,
        duration_s: float,
        win_s: int,
        start_buffer_s: float,
        end_buffer_s: float,
        min_gap_s: float
    ) -> int:
        """
        Conservative cap on sample count for evenly-spaced windows with fixed start/end buffers.
        """
        if duration_s <= 0 or win_s <= 0:
            return 0

        usable_span_s = float(duration_s) - float(start_buffer_s) - float(end_buffer_s)
        if usable_span_s < float(win_s):
            return 1

        min_gap_s = max(0.0, float(min_gap_s))
        denom = float(win_s) + min_gap_s
        if denom <= 0:
            return 1

        # N*win + (N-1)*gap <= usable  =>  N <= (usable + gap) / (win + gap)
        ms = int(math.floor((usable_span_s + min_gap_s) / denom))
        return max(1, ms)

    def _build_even_gap_windows_with_buffers(
        self,
        duration_s: float,
        desired_samples: int,
        win_s: int,
        buffer_s: int,
        min_gap_s: int
    ) -> List[Tuple[float, float]]:
        """
        Build (start, duration) windows that are evenly-spaced, with a fixed buffer at the start and end.

        - First window starts at `buffer_s`
        - Last window ends at `duration_s - buffer_s`
        - All windows are `win_s` long
        - Gap between windows is evenly distributed

        If the file is too short to satisfy the requested buffers/samples, buffers and sample count are reduced
        as needed (but at least 1 window is returned when possible).
        """
        if duration_s <= 0 or win_s <= 0 or desired_samples <= 0:
            return []

        duration_s = float(duration_s)
        win_s = int(win_s)
        desired_samples = int(desired_samples)
        buffer_s = max(0.0, float(buffer_s))
        min_gap_s = max(0.0, float(min_gap_s))

        # If a full window doesn't fit, just sample the whole file.
        if duration_s <= float(win_s):
            return [(0.0, float(duration_s))]

        # Keep requested buffer when possible; otherwise shrink it evenly so at least 1 window fits.
        max_buffer = max(0.0, (duration_s - float(win_s)) / 2.0)
        eff_buffer = self._clamp(buffer_s, 0.0, max_buffer)

        first_start = float(eff_buffer)
        last_start = float(duration_s - eff_buffer - float(win_s))
        if last_start < first_start:
            centered = max(0.0, (duration_s - float(win_s)) / 2.0)
            return [(centered, float(win_s))]

        max_samples = self._max_samples_for_even_gap(
            duration_s,
            win_s,
            start_buffer_s=eff_buffer,
            end_buffer_s=eff_buffer,
            min_gap_s=min_gap_s,
        )
        actual_samples = min(desired_samples, max_samples)

        if actual_samples <= 1:
            start = (first_start + last_start) / 2.0
            return [(start, float(win_s))]

        step = (last_start - first_start) / float(actual_samples - 1)
        windows = []
        for i in range(actual_samples):
            start = first_start + float(i) * step
            start = self._clamp(start, 0.0, max(0.0, duration_s - float(win_s)))
            windows.append((start, float(win_s)))
        return windows

    def _ffprobe_packets_json(self, file_path: str, read_interval: str, timeout_seconds: float) -> Optional[Dict]:
        cmd = [
            "ffprobe",
            "-v",
            "error",
            "-select_streams",
            "v:0",
            "-read_intervals",
            read_interval,
            "-show_packets",
            "-show_entries",
            "packet=size,pts_time,dts_time",
            "-of",
            "json",
            file_path,
        ]
        try:
            proc = subprocess.run(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                timeout=timeout_seconds,
                check=False,
            )
        except (OSError, subprocess.TimeoutExpired) as exc:
            logger.debug("%s ffprobe packet sampling failed (%s) for interval '%s'",
                         self._LOG_PREFIX, exc, read_interval)
            return None

        if proc.returncode != 0 or not proc.stdout:
            # Keep stderr out of normal logs unless debugging; it can be noisy.
            logger.debug(
                "%s ffprobe packet sampling returned code=%s for interval '%s' (stderr=%s)",
                self._LOG_PREFIX,
                proc.returncode,
                read_interval,
                (proc.stderr or "").strip()[:500],
            )
            return None

        try:
            return json.loads(proc.stdout)
        except Exception as exc:
            logger.debug("%s Failed to parse ffprobe JSON for interval '%s' (%s)", self._LOG_PREFIX, read_interval, exc)
            return None

    def _packet_bitrate_sample(self, file_path: str, start_s: float, dur_s: float, timeout_seconds: float) -> Optional[int]:
        """
        Sample packet sizes for v:0 over a requested window and return the total bytes, filtering by PTS.

        Note: `-read_intervals` seeks to a nearby keyframe, so we request a slightly wider integer-aligned interval
        and then filter packets precisely in Python by timestamp.
        """
        if dur_s <= 0:
            return None

        probe_start_s = int(math.floor(start_s))
        desired_end_s = float(start_s) + float(dur_s)
        probe_dur_s = int(math.ceil(desired_end_s - float(probe_start_s)))
        if probe_dur_s < 1:
            probe_dur_s = 1

        data = self._ffprobe_packets_json(file_path, f"{probe_start_s}%+{probe_dur_s}", timeout_seconds=timeout_seconds)
        if not data:
            return None

        packets = data.get("packets") or []
        total_bytes = 0
        for pkt in packets:
            if not isinstance(pkt, dict):
                continue

            size = self._safe_int(pkt.get("size"))
            if not size or size <= 0:
                continue

            pts = self._safe_float(pkt.get("pts_time"))
            if pts is None:
                pts = self._safe_float(pkt.get("dts_time"))
            if pts is None:
                continue

            if float(start_s) <= pts < (float(start_s) + float(dur_s)):
                total_bytes += size

        if total_bytes <= 0:
            return None

        return total_bytes

    def _derive_video_bitrate_from_packet_samples(self, file_path: Optional[str], duration: Optional[float]) -> Optional[int]:
        """
        Estimate a video-only bitrate by sampling packet sizes over a few short windows.

        This is a last-resort fallback used before container/file-level bitrate estimates, which can be
        inflated by high-bitrate audio streams.
        """
        if not file_path or not os.path.exists(file_path):
            return None

        duration_s = float(duration) if duration and duration > 0 else None
        if not duration_s or duration_s <= 0:
            return None

        # Strategy:
        # - <=15 seconds: sample entire file (video-only packets)
        # - >15 seconds: evenly-spaced 2-minute windows, with 2-minute buffers at the start and end
        whole_file_threshold_s = 15.0
        if duration_s <= float(whole_file_threshold_s):
            windows = [(0.0, float(duration_s))]
        else:
            # Sampling config:
            # - desired_samples: target number of windows to sample (reduced automatically if the file is too short)
            # - sample_window_s: length of each sampling window, in seconds
            # - buffer_s: keep this many seconds clear at the start and end of the file (no samples start/end inside this buffer)
            # - min_gap_s: minimum allowed gap between adjacent sampling windows, in seconds (0 = evenly distribute any available gap)
            desired_samples = 5
            sample_window_s = 120
            buffer_s = 120
            min_gap_s = 0
            windows = self._build_even_gap_windows_with_buffers(
                duration_s=duration_s,
                desired_samples=desired_samples,
                win_s=sample_window_s,
                buffer_s=buffer_s,
                min_gap_s=min_gap_s,
            )
            if not windows:
                return None

        # Per-sample timeout: scale with window size and cap to avoid runaway hangs.
        win_max = max((w[1] for w in windows), default=0.0)
        base_timeout = max(20.0, float(self.max_probe_seconds) if self.max_probe_seconds else 0.0)
        timeout_seconds = max(base_timeout, float(win_max) * 2.0)
        timeout_seconds = min(timeout_seconds, 300.0)

        total_bytes = 0
        total_dur = 0.0
        for start_s, dur_s in windows:
            sample_bytes = self._packet_bitrate_sample(file_path, start_s, dur_s, timeout_seconds=timeout_seconds)
            if sample_bytes and sample_bytes > 0:
                total_bytes += int(sample_bytes)
                total_dur += float(dur_s)

        if total_bytes <= 0 or total_dur <= 0:
            return None

        avg = int((total_bytes * 8.0) / float(total_dur))
        logger.debug(
            "%s Packet-sampled video bitrate=%s from total_dur=%ss (window=%ss)",
            self._LOG_PREFIX,
            avg,
            int(total_dur),
            int(win_max) if win_max else 0,
        )
        return avg

    def _video_stream_from_probe(self, probe_dict: Dict) -> Optional[Dict]:
        """
        Return the primary video stream, skipping attached pictures when possible.
        """
        streams = probe_dict.get("streams") or []
        for st in streams:
            if st.get("codec_type") != "video":
                continue
            disposition = st.get("disposition") or {}
            if disposition.get("attached_pic"):
                continue
            return st
        return next((st for st in streams if st.get("codec_type") == "video"), None)

    def _derive_video_bitrate_from_stream_tags(self, video_stream: Dict) -> Optional[int]:
        """
        Estimate a video-only bitrate from stream tags when `bit_rate` is missing.

        Matroska files muxed with mkvmerge often include per-stream statistics tags:
            - BPS (bits per second)
            - NUMBER_OF_BYTES + DURATION
        """
        if not isinstance(video_stream, dict):
            return None
        tags = video_stream.get("tags") or {}

        bps = self._safe_int(self._get_tag_value(tags, "BPS"))
        if bps and bps > 0:
            return bps

        number_of_bytes = self._safe_int(self._get_tag_value(tags, "NUMBER_OF_BYTES"))
        duration_tag = self._get_tag_value(tags, "DURATION")
        duration_seconds = self._parse_duration_hhmmss(duration_tag)
        if number_of_bytes and number_of_bytes > 0 and duration_seconds and duration_seconds > 0:
            return int((number_of_bytes * 8) / duration_seconds)

        return None

    def _duration_seconds(self, probe_dict: Dict) -> Optional[float]:
        fmt = probe_dict.get("format") or {}
        dur = self._safe_float(fmt.get("duration"))
        if dur:
            return dur

        streams = probe_dict.get("streams") or []
        for st in streams:
            dur = self._safe_float(st.get("duration"))
            if dur:
                return dur

        tags = fmt.get("tags") or {}
        tag_dur = tags.get("DURATION")
        duration = self._parse_duration_hhmmss(tag_dur)
        if duration:
            return duration
        return None

    def _bit_depth_from_pix_fmt(self, pix_fmt: Optional[str], default: Optional[int] = None) -> Optional[int]:
        if not pix_fmt:
            return default
        # p010le / p016le (10/16-bit formats)
        match = re.search(r"p0(\d{2})", pix_fmt)
        if match:
            return int(match.group(1))
        # The most common pattern: yuv420p10le -> contains 10
        match = re.search(r"p(\d{2})", pix_fmt)
        if match:
            return int(match.group(1))
        return default

    def _derive_bitrate(self, probe_dict: Dict, file_path: Optional[str], duration: Optional[float]):
        """Pull bitrates from stream/container; fall back to size/duration."""
        video_stream = self._video_stream_from_probe(probe_dict)
        # Get stream bitrate from ffprobe
        stream_bitrate = self._safe_int(video_stream.get("bit_rate")) if video_stream else None

        # If no stream bitrate was found, get a sampled bitrate from ffprobe
        sampled_bitrate = None
        if not stream_bitrate:
            sampled_bitrate = self._derive_video_bitrate_from_packet_samples(file_path, duration)

        tag_bitrate = self._derive_video_bitrate_from_stream_tags(video_stream) if not stream_bitrate else None

        container_bitrate = self._safe_int((probe_dict.get("format") or {}).get("bit_rate"))

        filesize_bits = None
        if file_path and os.path.exists(file_path):
            try:
                filesize_bits = os.path.getsize(file_path) * 8
            except OSError:
                filesize_bits = None

        derived = None
        if stream_bitrate:
            derived = stream_bitrate
        elif sampled_bitrate:
            derived = sampled_bitrate
        elif tag_bitrate:
            derived = tag_bitrate
        elif container_bitrate:
            derived = container_bitrate
        elif filesize_bits and duration and duration > 0:
            derived = int(filesize_bits / duration)

        return stream_bitrate, container_bitrate, filesize_bits, derived

    def collect_source_stats(self, file_path: Optional[str] = None) -> SourceStats:
        """
        Summarise the source into a simple struct (resolution, bitrate, HDR, confidence).

        Confidence levels:
        - high: duration present AND a usable bitrate estimate exists (derived/container/stream)
        - medium: usable bitrate exists but duration missing, OR HDR signalling partially missing, OR HDR probe failed
        - low: no usable bitrate estimate, OR HDR status is ambiguous and could affect output profile selection
        """
        probe_dict = self.probe.get_probe()
        first_video = self.probe.get_first_video_stream() or {}

        width = self._safe_int(first_video.get("width")) or self._safe_int(first_video.get("coded_width")) or 0
        height = self._safe_int(first_video.get("height")) or self._safe_int(first_video.get("coded_height")) or 0
        codec_name = first_video.get("codec_name")

        # FPS (prefer avg_frame_rate if available, fall back to r_frame_rate)
        fps = None
        rate = first_video.get("avg_frame_rate") or first_video.get("r_frame_rate")
        if rate:
            try:
                num, den = str(rate).split("/")
                fps = float(num) / float(den) if float(den) != 0 else None
            except (ValueError, ZeroDivisionError):
                fps = None

        # Duration + bitrate derivation feed rail calculations; if either is weak, confidence drops later.
        duration = self._duration_seconds(probe_dict)
        stream_bitrate, container_bitrate, filesize_bits, derived_bitrate = self._derive_bitrate(
            probe_dict, file_path, duration
        )

        confidence_notes = []
        confidence_level = "high"
        has_duration = bool(duration and duration > 0)
        has_bitrate = any(b is not None for b in (derived_bitrate, container_bitrate, stream_bitrate))

        if not has_bitrate:
            confidence_notes.append("missing_bitrate")
            confidence_level = "low"
        elif not has_duration:
            confidence_notes.append("missing_duration")
            confidence_level = "medium"

        # Informational: stream/container bitrate missing is common (esp. VP9/WebM)
        if stream_bitrate is None:
            confidence_notes.append("missing_stream_bitrate")
        if container_bitrate is None:
            confidence_notes.append("missing_container_bitrate")

        # HDR detection: trust probe first, but downgrade confidence when signalling is incomplete or ambiguous.
        is_hdr = False
        hdr_probe_failed = False
        try:
            is_hdr = bool(self.probe.is_hdr_source())
        except Exception:
            hdr_probe_failed = True
            confidence_notes.append("hdr_detection_failed")
            if confidence_level == "high":
                confidence_level = "medium"

        # Fallback HDR detection from metadata
        transfer = first_video.get("color_transfer")
        if not is_hdr and transfer in ("smpte2084", "arib-std-b67"):
            is_hdr = True

        # If HDR is detected but key tags are missing, downgrade to medium (not low) since profile/tagging may be off.
        if is_hdr:
            if not first_video.get("color_primaries") or not transfer or not first_video.get("color_space"):
                confidence_notes.append("missing_hdr_tags")
                if confidence_level == "high":
                    confidence_level = "medium"

        side_data = first_video.get("side_data_list") or []
        has_mastering = any(sd.get("side_data_type") == "Mastering display metadata" for sd in side_data)
        has_cll = any(sd.get("side_data_type") == "Content light level metadata" for sd in side_data)

        # If HDR probe failed AND metadata suggests possible HDR but is incomplete, mark ambiguous -> low.
        # (Example: 10-bit + BT.2020 primaries but transfer missing.)
        if hdr_probe_failed and not is_hdr:
            primaries = first_video.get("color_primaries")
            pix_fmt = first_video.get("pix_fmt") or ""
            looks_10bit = "p10" in pix_fmt or "p010" in pix_fmt
            looks_bt2020 = primaries == "bt2020"
            looks_bt2020cs = first_video.get("color_space") == "bt2020nc"
            if (looks_10bit or has_mastering or has_cll or looks_bt2020 or looks_bt2020cs) and not transfer:
                confidence_notes.append("hdr_ambiguous")
                confidence_level = "low"

        # Bit depth (note: ensure _bit_depth_from_pix_fmt is correct; yuv420p10le should become 10)
        pix_fmt = first_video.get("pix_fmt")
        bit_depth = self._safe_int(first_video.get("bits_per_raw_sample")) or self._bit_depth_from_pix_fmt(pix_fmt)
        if bit_depth is None and pix_fmt:
            bit_depth = 8

        confidence = confidence_level != "low"

        stats = SourceStats(
            width=width,
            height=height,
            codec_name=codec_name,
            bit_depth=bit_depth,
            duration=duration,
            stream_bitrate=stream_bitrate,
            container_bitrate=container_bitrate,
            filesize_bits=filesize_bits,
            derived_bitrate=derived_bitrate,
            is_hdr=is_hdr,
            pix_fmt=pix_fmt,
            fps=fps,
            confidence=confidence,
            confidence_level=confidence_level,
            confidence_notes=confidence_notes,
        )

        logger.info(
            "%s Smart output target source stats: res=%sx%s codec=%s hdr=%s bit_depth=%s "
            "bitrate_derived=%s stream_bitrate=%s container_bitrate=%s "
            "confidence=%s level=%s reasons=%s",
            self._LOG_PREFIX,
            stats.width,
            stats.height,
            stats.codec_name,
            stats.is_hdr,
            stats.bit_depth,
            stats.derived_bitrate,
            stats.stream_bitrate,
            stats.container_bitrate,
            stats.confidence,
            stats.confidence_level,
            stats.confidence_notes,
        )

        return stats

    def _resolution_bucket(self, width: int, height: int) -> str:
        width = max(width, 0)
        height = max(height, 0)
        pixel_area = width * height
        # Use pixel area with width guards so near-720p content does not fall into SD.
        if width >= 2400 or pixel_area >= 3_000_000:
            return "uhd"
        if width >= 1100 or pixel_area >= 700_000:
            return "hd"
        return "sd"

    def _fps_bucket_and_offset(self, fps: float):
        """
        Bucket FPS into speed classes and return the quality ladder offset for that class.
        """
        bucket = "low_motion"
        offset = 0
        if 30 <= fps < 45:
            bucket = "medium_motion"
            offset = -1
        elif fps >= 45:
            bucket = "high_motion"
            offset = -2
        return bucket, offset

    def _min_bpppf_value(self, goal: str, is_hdr: bool, fps_bucket: str) -> Optional[float]:
        """
        Look up the minimum bits-per-pixel-per-frame value for the given goal/HDR/FPS bucket.
        """
        goal_table = self._MIN_BPPPF.get(goal) or self._MIN_BPPPF.get(self.GOAL_BALANCED, {})
        range_table = goal_table.get("hdr" if is_hdr else "sdr", {})
        return range_table.get(fps_bucket) or range_table.get("medium_motion") or next(
            iter(range_table.values()), None
        )

    def _codec_efficiency_factor(self, target_codec: str, target_encoder: str) -> float:
        """
        Scale bitrate floors by the relative efficiency of the target codec.
        """
        codec = (target_codec or "").lower()
        encoder = (target_encoder or "").lower()
        return self._CODEC_EFFICIENCY.get((encoder, codec), self._CODEC_EFFICIENCY.get(codec, 1.0))

    def _min_target_bitrate(
        self,
        goal: str,
        target_codec: str,
        target_encoder: str,
        is_hdr: bool,
        fps_bucket: str,
        target_width: int,
        target_height: int,
        target_fps: float,
        min_bpppf: Optional[float] = None,
    ) -> Optional[int]:
        """
        Compute a normalized bitrate floor using bits-per-pixel-per-frame, scaled by resolution, FPS, and codec.
        """
        area = max(target_width, 0) * max(target_height, 0)
        if area <= 0 or not target_fps or target_fps <= 0:
            return None
        min_bpppf = min_bpppf if min_bpppf is not None else self._min_bpppf_value(goal, is_hdr, fps_bucket)
        if not min_bpppf:
            return None
        codec_factor = self._codec_efficiency_factor(target_codec, target_encoder)
        return int(min_bpppf * area * target_fps * codec_factor)

    def _target_cap(
        self,
        goal: str,
        source_bitrate: Optional[int],
        rate_ratio: float,
        is_hdr: bool,
        min_target_bitrate: Optional[int],
    ):
        """
        Guardrail: cap bitrate relative to source, scaled by rate ratio (pixels * fps).
        """
        if not source_bitrate:
            return int(min_target_bitrate) if min_target_bitrate else None
        cap_factor = self._CAP_FACTORS.get(goal, 1.1)
        if is_hdr and goal != self.GOAL_PREFER_QUALITY:
            cap_factor += 0.05
        base_cap = source_bitrate * rate_ratio
        same_res_cap = source_bitrate * 1.05
        upper_cap = source_bitrate if rate_ratio < 1 else source_bitrate * 1.05
        target_cap = (base_cap if rate_ratio < 1 else same_res_cap) * cap_factor
        candidate = target_cap
        if min_target_bitrate:
            candidate = max(candidate, min_target_bitrate)
        return int(self._clamp(candidate, 0, upper_cap))

    # --------------------------
    # Recommendation assembly
    # --------------------------
    def _base_quality_index(self, target_codec: str, goal: str, is_hdr: bool, resolution_bucket: str) -> Optional[int]:
        """
        Quality ladders are per codec, with HDR slightly more conservative.
        """
        target_codec = (target_codec or "").lower()
        codec_table = self._BASE_QUALITY_LADDERS.get(target_codec) or self._BASE_QUALITY_LADDERS.get("hevc")
        goal_table = codec_table.get(goal)
        if not goal_table:
            return None
        bucket_table = goal_table["hdr" if is_hdr else "sdr"]
        return bucket_table.get(resolution_bucket)

    def _reencode_cq_offset(self, source_codec: Optional[str], target_codec: Optional[str]) -> int:
        """
        Bias CQ based on codec direction to avoid over-compressing already efficient sources.
        Negative offsets reduce CQ (more quality), positive offsets allow more compression.
        """
        src = (source_codec or "").lower()
        dst = (target_codec or "").lower()
        return self._REENCODE_CQ_OFFSETS.get((src, dst), 0)

    def recommend_params(
        self,
        goal: str,
        source_stats: SourceStats,
        target_filters: Dict,
        target_codec: str,
        target_encoder: str,
        target_supports_hdr10: bool,
    ):
        """
        Build encoder-agnostic recommendations:
            - quality_mode: const_quality / capped_quality / target_bitrate
            - quality_index: abstract quantiser step (ladder entry)
            - wants_cap: desire to apply a bitrate rail
        """
        requested_goal = goal or self.GOAL_BALANCED
        goal = requested_goal if requested_goal in self._GOALS else self.GOAL_BALANCED
        if requested_goal != goal:
            logger.debug("%s Smart target goal normalized from '%s' to '%s'", self._LOG_PREFIX, requested_goal, goal)

        target_width = int(target_filters.get("target_width") or source_stats.width or 0)
        target_height = int(target_filters.get("target_height") or source_stats.height or 0)
        source_width = max(source_stats.width, 1)
        source_height = max(source_stats.height, 1)

        pixel_ratio = (target_width * target_height) / float(source_width * source_height)
        target_bucket = self._resolution_bucket(target_width, target_height)
        source_bucket = self._resolution_bucket(source_width, source_height)
        source_bitrate = source_stats.derived_bitrate
        target_codec = (target_codec or "").lower()
        target_encoder = (target_encoder or "").lower()

        logger.debug(
            "%s Smart target dimensions/buckets: target=%sx%s (%s) source=%sx%s (%s) pixel_ratio=%.3f",
            self._LOG_PREFIX,
            target_width,
            target_height,
            target_bucket,
            source_width,
            source_height,
            source_bucket,
            pixel_ratio,
        )

        logger.info(
            "%s Smart output target recommend_params input: goal=%s target_codec=%s target_encoder=%s target=%sx%s source_bitrate=%s pixel_ratio=%.3f",
            self._LOG_PREFIX,
            goal,
            target_codec,
            target_encoder,
            target_width,
            target_height,
            source_bitrate,
            pixel_ratio,
        )

        # FPS + normalized complexity:
        #   The cap/floor logic below needs an FPS value to behave sanely for high frame-rate sources.
        #   When fps is not present in the probe, assume a typical film/TV cadence (24fps) rather than 0.
        #   We treat "complexity" as (pixels * fps) instead of pixels-only so that 720p60 is not capped
        #   as aggressively as 720p24. This aligns the ceiling behaviour (cap) with the floor behaviour
        #   (minimum bpppf).
        src_fps = source_stats.fps if source_stats.fps and source_stats.fps > 0 else 24.0
        target_fps = src_fps
        fps_bucket, fps_offset = self._fps_bucket_and_offset(src_fps)
        min_bpppf = self._min_bpppf_value(goal, source_stats.is_hdr, fps_bucket)

        # Encoder/codec efficiency adjustment:
        #   The bpppf table yields a codec-agnostic minimum. Apply an efficiency multiplier based on the
        #   chosen encoder+codec so that (for example) software x265 can hit similar perceptual quality at
        #   lower bitrate than hardware NVENC for the same HEVC output.
        codec_efficiency = self._codec_efficiency_factor(target_codec, target_encoder)

        # Minimum target bitrate derived from bpppf:
        #   Convert the normalized minimum bpppf into a bitrate floor for the *target* output:
        #     min_rate = min_bpppf * target_area * target_fps * codec_efficiency
        #   This floor scales naturally with resolution and FPS, and nudges based on output encoder/codec.
        min_target_bitrate = self._min_target_bitrate(
            goal,
            target_codec,
            target_encoder,
            source_stats.is_hdr,
            fps_bucket,
            target_width,
            target_height,
            target_fps,
            min_bpppf,
        )

        # Rate ratio (cap scaling input):
        #   Derive a source→target scaling ratio using (area * fps). This replaces the legacy pixels-only
        #   ratio so bitrate caps remain reasonable for high-FPS outputs.
        #     rate_ratio = (target_area * target_fps) / (source_area * src_fps)
        source_area = max(source_width * source_height, 1)
        target_area = max(target_width * target_height, 1)
        rate_ratio = (target_area * target_fps) / float(source_area * src_fps)
        logger.debug(
            "%s Rate ratio: src_area=%s src_fps=%.3f tgt_area=%s tgt_fps=%.3f -> rate_ratio=%.3f",
            self._LOG_PREFIX,
            source_area,
            src_fps,
            target_area,
            target_fps,
            rate_ratio,
        )
        logger.debug(
            "%s Min bitrate floor: bpppf=%s codec_efficiency=%.3f target_fps=%.3f area=%s -> min_rate=%s",
            self._LOG_PREFIX,
            min_bpppf,
            codec_efficiency,
            target_fps,
            target_width * target_height,
            min_target_bitrate,
        )

        # Bitrate cap guardrail:
        #   Scale relative to the source and the rate ratio (pixels * fps).
        #   Anchor to a normalized bits-per-pixel-per-frame floor so high-FPS downscales are not over-clamped.
        target_cap = self._target_cap(
            goal,
            source_bitrate,
            rate_ratio,
            source_stats.is_hdr,
            min_target_bitrate,
        )
        logger.debug(
            "%s Bitrate cap inputs: source_br=%s min_floor=%s rate_ratio=%.3f hdr=%s -> target_cap=%s",
            self._LOG_PREFIX,
            source_bitrate,
            min_target_bitrate,
            rate_ratio,
            source_stats.is_hdr,
            target_cap,
        )

        # Downscale guardrail for low-bitrate sources:
        #   When Prefer Quality is downscaling a weak source, switch to capped mode to avoid runaway constqp.
        low_bitrate_threshold = self._LOW_BITRATE_THRESHOLDS.get(source_bucket, 0)

        # Pick quality mode/index and record any downgrade reason.
        quality_mode = self.QUALITY_CONST if goal == self.GOAL_PREFER_QUALITY else self.QUALITY_CAPPED
        downgraded_reason = None
        logger.debug(
            "%s Initial quality mode=%s goal=%s source_bitrate=%s low_br_threshold=%s pixel_ratio=%.3f",
            self._LOG_PREFIX,
            quality_mode,
            goal,
            source_bitrate,
            low_bitrate_threshold,
            pixel_ratio,
        )
        if (
            quality_mode == self.QUALITY_CONST
            and pixel_ratio < 1
            and source_bitrate
            and source_bitrate <= low_bitrate_threshold
        ):
            quality_mode = self.QUALITY_CAPPED
            downgraded_reason = "low_bitrate_downscale"
            logger.debug(
                "%s Downgrading to capped quality due to low bitrate downscale (threshold=%s)",
                self._LOG_PREFIX,
                low_bitrate_threshold,
            )

        # HDR handling guardrails:
        #   Flag HDR outputs that are likely to band.
        #   That happens when there is no HDR10 path or when the HDR source is only 8-bit.
        hdr_output_limited = False
        hdr_output_limited_reason = None
        if source_stats.is_hdr:
            if target_supports_hdr10 is False:
                hdr_output_limited = True
                hdr_output_limited_reason = "hdr_output_not_supported"
            elif source_stats.bit_depth and source_stats.bit_depth <= 8:
                hdr_output_limited = True
                hdr_output_limited_reason = "hdr_8bit_source"
        if hdr_output_limited:
            logger.debug(
                "%s HDR output limited for encoder=%s reason=%s bit_depth=%s",
                self._LOG_PREFIX,
                target_encoder,
                hdr_output_limited_reason,
                source_stats.bit_depth,
            )

        # Base params per goal:
        #   Pull from codec/goal/resolution ladders and fall back to safe defaults when needed.
        quality_index = self._base_quality_index(target_codec, goal, source_stats.is_hdr, target_bucket)
        ladder_pick = quality_index
        if quality_index is None:
            if goal == self.GOAL_PREFER_QUALITY:
                quality_index = 22 if source_stats.is_hdr else 24
            else:
                quality_index = 24 if not source_stats.is_hdr else 26
                if goal == self.GOAL_PREFER_COMPRESSION:
                    quality_index = 30 if not source_stats.is_hdr else 28
        logger.debug(
            "%s Quality index selection: ladder=%s fallback=%s goal=%s hdr=%s target_bucket=%s",
            self._LOG_PREFIX,
            ladder_pick,
            quality_index,
            goal,
            source_stats.is_hdr,
            target_bucket,
        )

        # FPS bucket adjustments:
        #   Give higher frame rate sources a small quality boost.
        if quality_index is not None and fps_offset:
            quality_index = max(0, quality_index + fps_offset)
        logger.debug(
            "%s FPS adjustment: fps=%.3f bucket=%s offset=%s -> quality_index=%s",
            self._LOG_PREFIX,
            src_fps,
            fps_bucket,
            fps_offset,
            quality_index,
        )

        # Apply re-encode bias and HDR banding sensitivity adjustments.
        cq_offset = self._reencode_cq_offset(source_stats.codec_name, target_codec)
        if quality_index is not None and quality_mode != self.QUALITY_CONST:
            quality_index = max(0, quality_index + cq_offset)
            logger.debug(
                "%s Applied re-encode CQ offset: source_codec=%s target_codec=%s offset=%s -> quality_index=%s",
                self._LOG_PREFIX,
                source_stats.codec_name,
                target_codec,
                cq_offset,
                quality_index,
            )

        # HDR-limited output (no HDR10 path or 8-bit HDR):
        #   Lower CQ/QP a bit to reduce the chance of banding.
        if hdr_output_limited and quality_index is not None:
            quality_index = max(0, quality_index - 2)
            logger.debug("%s HDR limited output; easing quality index to %s", self._LOG_PREFIX, quality_index)

        # Build bitrate rails (maxrate/bufsize) only when caps make sense for the chosen mode/scale.
        wants_cap = bool(target_cap) and quality_mode in (self.QUALITY_CAPPED, self.QUALITY_TARGET)
        if downgraded_reason and target_cap:
            wants_cap = True
        logger.debug(
            "%s Cap decision: target_cap=%s wants_cap=%s quality_mode=%s downgraded_reason=%s",
            self._LOG_PREFIX,
            target_cap,
            wants_cap,
            quality_mode,
            downgraded_reason,
        )

        # Build bitrate params for VBR modes using the derived guardrail cap.
        maxrate = int(target_cap) if target_cap and wants_cap else None
        bufsize = int(target_cap * 2.0) if target_cap and wants_cap else None
        logger.debug("%s Cap rails: maxrate=%s bufsize=%s", self._LOG_PREFIX, maxrate, bufsize)

        # Confidence tracking and adjustments:
        #   Mark low confidence when HDR output is limited or probe stats are weak.
        #   Ease CQ when confidence is low.
        confidence_level = source_stats.confidence_level
        confidence = confidence_level != "low"
        confidence_notes = list(source_stats.confidence_notes)
        if hdr_output_limited:
            confidence = False
            confidence_level = "low"
            if hdr_output_limited_reason:
                confidence_notes.append(hdr_output_limited_reason)
            if hdr_output_limited_reason == "hdr_output_not_supported":
                logger.info(
                    "%s HDR source detected but target encoder lacks HDR10 output; applying conservative settings.",
                    self._LOG_PREFIX,
                )
        if not confidence:
            if quality_index is not None:
                quality_index = max(0, quality_index - 2)
                logger.debug("%s Low confidence; easing quality index to %s", self._LOG_PREFIX, quality_index)
        if confidence_level != "high":
            logger.info(
                "%s Smart output target low confidence: level=%s reasons=%s",
                self._LOG_PREFIX,
                confidence_level,
                confidence_notes,
            )

        master_display = None
        max_cll = None
        if source_stats.is_hdr:
            try:
                hdr_md = self.probe.get_hdr_static_metadata()
                master_display = hdr_md.get("master_display")
                max_cll = hdr_md.get("max_cll")
            except Exception:
                master_display = None
                max_cll = None

        recommendation = {
            "goal": goal,
            "quality_mode": quality_mode,
            "quality_index": quality_index,
            "wants_cap": wants_cap,
            "maxrate": maxrate,
            "bufsize": bufsize,
            "target_cap": target_cap,
            "pixel_ratio": pixel_ratio,
            "downgraded_reason": downgraded_reason,
            "confidence": confidence,
            "confidence_level": confidence_level,
            "confidence_notes": confidence_notes,
            "target_resolution": {"width": target_width, "height": target_height},
            "source_resolution": {"width": source_stats.width, "height": source_stats.height},
            "hdr": {
                "is_hdr": source_stats.is_hdr,
                "bit_depth": source_stats.bit_depth,
                "output_supported": not hdr_output_limited,
                "master_display": master_display,
                "max_cll": max_cll,
            },
            "target_supports_hdr10": target_supports_hdr10,
            "source_bucket": source_bucket,
            "target_bucket": target_bucket,
        }
        logger.info(
            "%s Smart output target recommendation: goal=%s quality_mode=%s quality_index=%s cap=%s maxrate=%s bufsize=%s confidence=%s notes=%s",
            self._LOG_PREFIX,
            recommendation.get("goal"),
            recommendation.get("quality_mode"),
            recommendation.get("quality_index"),
            recommendation.get("target_cap"),
            recommendation.get("maxrate"),
            recommendation.get("bufsize"),
            recommendation.get("confidence"),
            recommendation.get("confidence_notes"),
        )

        return recommendation
