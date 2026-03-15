#!/usr/bin/env python3

import json
import math
import os
import shutil
import subprocess
import logging
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple


logger = logging.getLogger()


class FFProbeError(Exception):
    """
    FFProbeError
    Custom exception for errors encountered while executing the ffprobe command.
    """

    def __init__(self, path, info):
        Exception.__init__(self, "Unable to fetch data from file {}. {}".format(path, info))
        self.path = path
        self.info = info


def ffprobe_cmd(params):
    """
    Execute a ffprobe command subprocess and read the output

    :param params:
    :return:
    """
    command = ["ffprobe"] + params

    pipe = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    out, err = pipe.communicate()

    # Check for results
    try:
        raw_output = out.decode("utf-8")
    except Exception as e:
        raise FFProbeError(command, str(e))

    if 'error' in raw_output:
        try:
            info = json.loads(raw_output)
        except Exception as e:
            raise FFProbeError(command, raw_output)
    if pipe.returncode != 0:
        raise FFProbeError(command, raw_output)
    if not raw_output:
        raise FFProbeError(command, 'No info found')

    return raw_output


def ffprobe_file(vid_file_path):
    """
    Returns a dictionary result from ffprobe command line prove of a file

    :param vid_file_path: The absolute (full) path of the video file, string.
    :return:
    """
    if type(vid_file_path) != str:
        raise Exception('Give ffprobe a full file path of the video')

    params = [
        "-loglevel", "quiet",
        "-print_format", "json",
        "-show_format",
        "-show_streams",
        "-show_error",
        "-show_chapters",
        vid_file_path
    ]

    # Check result
    results = ffprobe_cmd(params)
    try:
        info = json.loads(results)
    except Exception as e:
        raise FFProbeError(vid_file_path, str(e))

    return info


def _which_or_die(cmd: str) -> None:
    if shutil.which(cmd) is None:
        raise SystemExit(f"Error: {cmd} is required but was not found in PATH.")


class DeriveBitrateHelper:

    _LOG_PREFIX = "[SmartOutputTargetHelper]"

    def __init__(self, max_probe_seconds: float = 2.0):
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

    def process_file(self, file_path: str):
        probe_dict = ffprobe_file(file_path)
        duration = self._duration_seconds(probe_dict)
        return self._derive_video_bitrate_from_packet_samples(file_path, duration)


def main() -> int:
    if len(sys.argv) != 2:
        print(f"Usage: {Path(sys.argv[0]).name} <input_path>", file=sys.stderr)
        return 2

    input_path = Path(sys.argv[1])
    if not input_path.exists():
        print(f"Error: input file not found: {input_path}", file=sys.stderr)
        return 1
    if not input_path.is_file():
        print(f"Error: input path is not a file: {input_path}", file=sys.stderr)
        return 1
    if not os.access(input_path, os.R_OK):
        print(f"Error: input file is not readable: {input_path}", file=sys.stderr)
        return 1

    _which_or_die("ffprobe")

    db = DeriveBitrateHelper()
    sampled_bitrate = db.process_file(str(input_path.resolve()))
    print(sampled_bitrate)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
