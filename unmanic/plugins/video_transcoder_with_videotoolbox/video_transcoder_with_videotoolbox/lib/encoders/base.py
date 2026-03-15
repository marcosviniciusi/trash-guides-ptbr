#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    plugins.base.py

    Written by:               Josh.5 <jsunnex@gmail.com>
    Date:                     29 August 2025, (10:45 AM)

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

logger = logging.getLogger("Unmanic.Plugin.video_transcoder")


class Encoder:
    def __init__(self, settings=None, probe=None):
        self.settings = settings
        self.probe = probe

    def set_probe(self, probe=None, probe_info=None):
        if isinstance(probe_info, dict):
            from video_transcoder.lib.ffmpeg import Probe
            probe = Probe(logger, allowed_mimetypes=['video'])
            probe.set_probe(probe_info)
        self.probe = probe

    def _target_pix_fmt_for_encoder(self, encoder_name: str) -> str:
        """
        Determines the target pixel format for a given encoder based on the source pixel format.
        This generic method handles software encoders and calls a specific hardware mapper.

        Args:
            encoder_name: The name of the FFmpeg encoder (e.g., "hevc_vaapi").

        Returns:
            The target pixel format string supported by the encoder.
        """
        if not self.probe:
            raise ValueError("Probe not yet specified on Encoder class")
        src_pix_fmt = self.probe.get_video_stream_pix_fmt()
        enc = (encoder_name or "").lower()
        src = (src_pix_fmt or "").lower()

        is_h264 = "h264" in enc

        # Determine bit depth of the source pixel format
        is_10bit_or_more = any(tag in src for tag in ("10", "12", "p010", "p016"))

        return self._map_pix_fmt(is_h264, is_10bit_or_more)

    def _map_pix_fmt(self, is_h264: bool, is_10bit: bool) -> str:
        """
        This method is implemented by child classes to provide the specific
        pixel format mapping logic. This default implementation handles
        software formats.
        """
        if is_10bit and not is_h264:
            return "yuv420p10le"
        else:
            return "yuv420p"

    def _target_color_config_for_encoder(self, encoder_name: str):
        """
        Returns a dict describing how to preserve HDR for the given encoder.
        This generic method handles common HDR checks and calls a specific
        mapping method for encoder-specific logic.
        """
        if not self.probe:
            raise ValueError("Probe not yet specified on Encoder class")

        # If the source is not HDR, return early with no changes
        if not self.probe.is_hdr_source():
            return {
                "apply_color_params":  False,
                "setparams_filter":    None,
                "color_tags":          {},
                "stream_color_params": {},
            }

        # Common pieces for HDR10
        src_color_tags = self.probe.get_color_tags()
        color_tags = {
            "color_primaries": src_color_tags.get("color_primaries", "bt2020"),
            "color_trc":       src_color_tags.get("color_trc", "smpte2084"),
            "colorspace":      src_color_tags.get("colorspace", "bt2020nc"),
            "color_range":     src_color_tags.get("color_range", "tv"),
        }

        # Build the setparams filter string
        setparams_filter = (
            f"setparams="
            f"range={color_tags['color_range']}:"
            f"color_primaries={color_tags['color_primaries']}:"
            f"color_trc={color_tags['color_trc']}:"
            f"colorspace={color_tags['colorspace']}"
        )

        # Build the color tags dictionary for output stream
        stream_color_params = {
            "-color_primaries": color_tags['color_primaries'],
            "-color_trc":       color_tags['color_trc'],
            "-colorspace":      color_tags['colorspace'],
            "-color_range":     color_tags['color_range'],
        }

        # Get encoder-specific configuration
        # TODO: Check if we need this
        # encoder_config = self._map_color_config_for_encoder(encoder_name, color_tags)

        # Merge the generic and specific configurations
        result = {
            "apply_color_params":  True,
            "setparams_filter":    setparams_filter,
            "color_tags":          color_tags,
            "stream_color_params": stream_color_params,
        }
        # TODO: Check if we need this
        # result.update(encoder_config)
        return result

    def _map_color_config_for_encoder(self, encoder_name: str, color_tags: dict):
        """
        This method must be implemented by a child class to provide the
        specific HDR configuration for a given encoder.

        Returns a dict containing:
            "requires_p010": bool,
            "encoder_args": dict,
            "bitstream_filter": str|None,
            "notes": str
        """
        raise NotImplementedError("This method must be implemented by a child class.")

    def provides(self):
        """
        Returns a dictionary of supported encoder types for a given plugin.
        Each dictionary entry should contain the codec name and a human-readable label.
        """
        raise NotImplementedError("This method must be implemented by a child class.")

    def options(self):
        """
        Returns a dictionary of configurable options for the encoder plugin.
        """
        raise NotImplementedError("This method must be implemented by a child class.")

    def generate_default_args(self):
        """
        Generate a dictionary of default FFmpeg args for the encoder.
        This method is primarily for hardware encoders to set up the device and context.
        """
        raise NotImplementedError("This method must be implemented by a child class.")

    def generate_filtergraphs(self, current_filter_args, smart_filters, encoder_name):
        """
        Generate the required filtergraph for the encoder based on the workflow.
        """
        raise NotImplementedError("This method must be implemented by a child class.")

    def stream_args(self, stream_info, stream_id, encoder_name, filter_state=None):
        """
        Generate a list of arguments for the encoder.
        """
        raise NotImplementedError("This method must be implemented by a child class.")
