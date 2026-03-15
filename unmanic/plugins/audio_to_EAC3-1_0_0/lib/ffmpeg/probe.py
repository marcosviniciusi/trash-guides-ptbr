#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    plugins.probe.py

    Written by:               Josh.5 <jsunnex@gmail.com>
    Date:                     12 Aug 2021, (9:20 AM)

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
import json
import mimetypes
import os
import shutil
import subprocess
from logging import Logger

from .mimetype_overrides import MimetypeOverrides


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


class Probe(object):
    """
    Probe
    """

    probe_info = {}

    def __init__(self, logger: Logger, allowed_mimetypes=None):
        # Ensure ffprobe is installed
        if shutil.which('ffprobe') is None:
            raise Exception("Unable to find executable 'ffprobe'. Please ensure that FFmpeg is installed correctly.")

        self.logger = logger
        if allowed_mimetypes is None:
            allowed_mimetypes = ['audio', 'video', 'image']
        self.allowed_mimetypes = allowed_mimetypes

        # Init (reset) our mimetype list
        mimetypes.init()

        # Add mimetype overrides to mimetype dictionary (replaces any existing entries)
        mimetype_overrides = MimetypeOverrides()
        all_mimetype_overrides = mimetype_overrides.get_all()
        for extension in all_mimetype_overrides:
            mimetypes.add_type(all_mimetype_overrides.get(extension), extension)

    def __test_valid_mimetype(self, file_path):
        """
        Test the given file path for its mimetype.
        If the mimetype cannot be detected, it will fail this test.
        If the detected mimetype is not in the configured 'allowed_mimetypes'
            class variable, it will fail this test.

        :param file_path:
        :return:
        """
        # Only run this check against video/audio/image MIME types
        file_type = mimetypes.guess_type(file_path)[0]

        # If the file has no MIME type then it cannot be tested
        if file_type is None:
            self.logger.debug("Unable to fetch file MIME type - '{}'".format(file_path))
            return False

        # Make sure the MIME type is either audio, video or image
        file_type_category = file_type.split('/')[0]
        if file_type_category not in self.allowed_mimetypes:
            self.logger.debug("File MIME type not in [{}] - '{}'".format(', '.join(self.allowed_mimetypes), file_path))
            return False

        return True

    @staticmethod
    def init_probe(data, logger, allowed_mimetypes=None):
        """
        Fetch the Probe object given a plugin's data object

        :param data:
        :param logger:
        :param allowed_mimetypes:
        :return:
        """
        probe = Probe(logger, allowed_mimetypes=allowed_mimetypes)
        # Start by fetching probe data from 'shared_info'.
        ffprobe_data = data.get('shared_info', {}).get('ffprobe')
        if ffprobe_data:
            if not probe.set_probe(ffprobe_data):
                # Failed to set ffprobe from 'shared_info'.
                # Probably due to it being for an incompatible mimetype declared above.
                return
            return probe
        # No 'shared_info' ffprobe exists. Attempt to probe file.
        if not probe.file(data.get('path')):
            # File probe failed, skip the rest of this test.
            # Again, probably due to it being for an incompatible mimetype.
            return
        # Successfully probed file.
        # Set file probe to 'shared_info' for subsequent file test runners.
        if 'shared_info' not in data:
            data['shared_info'] = {}
        data['shared_info']['ffprobe'] = probe.get_probe()
        return probe

    def file(self, file_path):
        """
        Sets the 'probe' dict by probing the given file path.
        Files that are not able to be probed will not set the 'probe' dict.

        :param file_path:
        :return:
        """
        self.probe_info = {}

        # Ensure file exists
        if not os.path.exists(file_path):
            self.logger.debug("File does not exist - '{}'".format(file_path))
            return

        if not self.__test_valid_mimetype(file_path):
            return

        try:
            # Get the file probe info
            self.probe_info = ffprobe_file(file_path)
            return True
        except FFProbeError:
            # This will only happen if it was not a file that could be probed.
            self.logger.debug("File unable to be probed by FFProbe - '{}'".format(file_path))
            return

    def set_probe(self, probe_info):
        """Sets the probe dictionary"""
        file_path = probe_info.get('format', {}).get('filename')
        if not file_path:
            self.logger.error("Provided file probe information does not contain the expected 'filename' key.")
            return
        if not self.__test_valid_mimetype(file_path):
            return

        self.probe_info = probe_info
        return self.probe_info

    def get_probe(self):
        """Return the probe dictionary"""
        return self.probe_info

    def get(self, key, default=None):
        """Return the value of the given key from the probe dictionary"""
        return self.probe_info.get(key, default)

    def get_first_video_stream(self):
        for st in (self.probe_info.get("streams") or []):
            if st.get("codec_type") == "video":
                return st
        return {}

    def get_video_stream_pix_fmt(self, default="nv12"):
        """
        Return the pixel format of the first video stream in the probe info.
        Falls back to `default` (nv12) if not available.

        Example outputs:
          - 'nv12'
          - 'yuv420p'
          - 'p010le'
          - 'yuv420p10le'
        """
        vs = self.get_first_video_stream()
        if vs:
            return vs.get("pix_fmt", default)
        return default

    def get_color_tags(self):
        """
        Returns a dict of standard FFmpeg color tags for HDR or SDR content.
        For example: {'color_primaries':'bt2020', 'color_trc':'smpte2084',
                       'colorspace':'bt2020nc', 'color_range':'tv'}.
        Only includes keys that exist on the input.
        """
        vs = self.get_first_video_stream()

        # Map ffprobe keys to FFmpeg command-line option names
        # ffprobe uses 'color_transfer', but the command-line option is 'color_trc'
        # ffprobe uses 'color_space', but the command-line option is 'colorspace'
        mapper = {
            "color_primaries": "color_primaries",
            "color_transfer":  "color_trc",
            "color_space":     "colorspace",
            "color_range":     "color_range",
        }

        out = {}
        for probe_key, cmd_key in mapper.items():
            value = vs.get(probe_key)
            # Handle the case where ffprobe might use an old key
            if not value:
                if probe_key == "color_transfer":
                    value = vs.get("color_trc")
                elif probe_key == "color_space":
                    value = vs.get("colorspace")

            if value:
                # ffprobe values like 'bt2020nc' are correct for the command-line
                out[cmd_key] = str(value)

        return out

    def get_hdr_static_metadata(self):
        """
        Returns {'master_display': 'G(x,y)B(x,y)R(x,y)WP(x,y)L(max,min)',
                 'max_cll': (MaxCLL, MaxFALL)}  when present; else {}.
        """
        vs = self.get_first_video_stream()
        sdl = vs.get("side_data_list") or []
        md = {}

        def _parse_fraction_string(s):
            """Safely parses a string that might be an int, float, or fraction."""
            if s is None:
                return 0.0
            if isinstance(s, (int, float)):
                return float(s)
            try:
                if isinstance(s, str) and '/' in s:
                    num, den = map(int, s.split('/'))
                    if den == 0:
                        return 0.0
                    return num / den
                return float(s)
            except (ValueError, TypeError, ZeroDivisionError):
                return 0.0

        # Mastering Display
        for sd in sdl:
            if sd.get("side_data_type", "").lower() == "mastering display metadata":
                # ffprobe gives floats in range [0,1] for x/y; luminance in cd/m^2.
                # hevc_metadata bsf expects ints scaled by 50000 for x/y, and cd/m^2 * 10000 for luminance.
                def xy(v): return int(round(_parse_fraction_string(v) * 50000))

                prim = sd.get("red", {}), sd.get("green", {}), sd.get("blue", {}), sd.get("white_point", {})
                r, g, b, wp = prim
                max_l = int(round(_parse_fraction_string(sd.get("max_luminance", 0)) * 10000))
                min_l = int(round(_parse_fraction_string(sd.get("min_luminance", 0)) * 10000))
                md["master_display"] = (
                    f"G({xy(g.get('x', 0))},{xy(g.get('y', 0))})"
                    f"B({xy(b.get('x', 0))},{xy(b.get('y', 0))})"
                    f"R({xy(r.get('x', 0))},{xy(r.get('y', 0))})"
                    f"WP({xy(wp.get('x', 0))},{xy(wp.get('y', 0))})"
                    f"L({max_l},{min_l})"
                )
            if sd.get("side_data_type", "").lower() == "content light level metadata":
                md["max_cll"] = (
                    int(sd.get("max_content", 0)),
                    int(sd.get("max_average", 0))
                )
        return md

    def is_hdr_source(self) -> bool:
        """
        Checks if a probe object represents a HDR10 source.
        """
        tags = self.get_color_tags()

        # Check for the core HDR10 metadata flags
        is_bt2020 = tags.get("color_primaries") == "bt2020"
        is_pq = tags.get("color_trc") == "smpte2084"
        is_bt2020_csp = tags.get("colorspace") in ("bt2020nc", "bt2020ncl", "bt2020c")

        # Also require a 10-bit or higher pixel format
        pix_fmt = self.get_video_stream_pix_fmt()
        is_10bit_or_more = any(key in pix_fmt for key in ("p010", "yuv420p10", "p016", "yuv420p12"))

        return is_bt2020 and is_pq and is_bt2020_csp and is_10bit_or_more
