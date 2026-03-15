#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    plugins.tools.py

    Written by:               Josh.5 <jsunnex@gmail.com>
    Date:                     04 Jun 2022, (1:52 PM)

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
import re
import shlex
import subprocess
from collections import Counter
from typing import List, Optional, Iterable

from video_transcoder.lib.encoders.libx import LibxEncoder
from video_transcoder.lib.encoders.libsvtav1 import LibsvtAv1Encoder
from video_transcoder.lib.encoders.qsv import QsvEncoder
from video_transcoder.lib.encoders.vaapi import VaapiEncoder
from video_transcoder.lib.encoders.nvenc import NvencEncoder
from video_transcoder.lib.encoders.videotoolbox import VideoToolboxEncoder
from video_transcoder.lib.ffmpeg import StreamMapper

image_video_codecs = [
    'alias_pix',
    'apng',
    'brender_pix',
    'dds',
    'dpx',
    'exr',
    'fits',
    'gif',
    'mjpeg',
    'mjpegb',
    'pam',
    'pbm',
    'pcx',
    'pfm',
    'pgm',
    'pgmyuv',
    'pgx',
    'photocd',
    'pictor',
    'pixlet',
    'png',
    'ppm',
    'ptx',
    'sgi',
    'sunrast',
    'tiff',
    'vc1image',
    'wmv3image',
    'xbm',
    'xface',
    'xpm',
    'xwd',
]

resolution_map = {
    '480p_sdtv':   {
        'width':  854,
        'height': 480,
        'label':  "480p (SDTV)",
    },
    '576p_sdtv':   {
        'width':  1024,
        'height': 576,
        'label':  "576p (SDTV)",
    },
    '720p_hdtv':   {
        'width':  1280,
        'height': 720,
        'label':  "720p (HDTV)",
    },
    '1080p_hdtv':  {
        'width':  1920,
        'height': 1080,
        'label':  "1080p (HDTV)",
    },
    'dci_2k_hdtv': {
        'width':  2048,
        'height': 1080,
        'label':  "DCI 2K (HDTV)",
    },
    '1440p':       {
        'width':  2560,
        'height': 1440,
        'label':  "1440p (WQHD)",
    },
    '4k_uhd':      {
        'width':  3840,
        'height': 2160,
        'label':  "4K (UHD)",
    },
    'dci_4k':      {
        'width':  4096,
        'height': 2160,
        'label':  "DCI 4K",
    },
    '8k_uhd':      {
        'width':  8192,
        'height': 4608,
        'label':  "8k (UHD)",
    },
}


def append_worker_log(worker_log, line: str):
    """
    Append a log line to Unmanic's `worker_log` list (if provided).
    """
    if worker_log is None or not isinstance(worker_log, list):
        return
    try:
        worker_log.append(str(line))
    except Exception:
        # Never break processing due to logging issues
        return


def available_encoders(settings=None, probe=None):
    return_encoders = {}
    encoder_libs = [
        LibxEncoder,
        LibsvtAv1Encoder,
        QsvEncoder,
        VaapiEncoder,
        NvencEncoder,
        VideoToolboxEncoder,
    ]
    for encoder_class in encoder_libs:
        encoder_lib = encoder_class(settings=settings, probe=probe)
        for encoder in encoder_lib.provides():
            return_encoders[encoder] = encoder_lib
    return return_encoders


def get_video_stream_data(streams):
    width = 0
    height = 0
    video_stream_index = 0

    for stream in streams:
        if stream.get('codec_type') == 'video':
            width = stream.get('width', stream.get('coded_width', 0))
            height = stream.get('height', stream.get('coded_height', 0))
            video_stream_index = stream.get('index')
            break

    return width, height, video_stream_index


def format_command_multiline(mapper, max_width=120, indent="  "):
    """
    Prints command for debugging...
    Pretty-print a shell command with flag/value grouping and hard wraps.

    - max_width: wrap line when it would exceed this width
    - indent: indent used at the start of wrapped lines
    """

    ffmpeg_args = mapper.get_ffmpeg_args()
    cmd = ['ffmpeg']
    cmd += ffmpeg_args

    # Quote everything for safe copy/paste
    q = [shlex.quote(x) for x in cmd]

    # Head is the binary; tail are the arguments we want to group/wrap
    head, tail = q[0], q[1:]

    # Group (flag + value) when it's "-something" followed by a non-flag token
    chunks = []
    i = 0
    while i < len(tail):
        cur = tail[i]
        nxt = tail[i + 1] if i + 1 < len(tail) else None
        if cur.startswith("-") and nxt is not None and not nxt.startswith("-"):
            chunks.append(f"{cur} {nxt}")
            i += 2
        else:
            chunks.append(cur)
            i += 1

    # Now wrap into lines <= max_width
    lines = [head]  # start with the binary on the first line
    cur = head
    for chunk in chunks:
        # try to append to current line
        attempt = f"{cur} {chunk}"
        if len(attempt) <= max_width:
            cur = attempt
            lines[-1] = cur
        else:
            # wrap to a new line
            cur = f"{indent}{chunk}"
            lines.append(cur)

    # Join with line continuations
    return " \\\n".join(lines)


def join_filtergraph(filter_id, filter_args, stream_id):
    """
    Joins a filtergraph from a collection of args
    """
    filtergraph = ''
    count = 1
    for filter_string in filter_args:
        # If we are appending to existing filters, separate by a semicolon to start a new chain
        if filtergraph:
            filtergraph += ';'
        # Add the input for this filter
        filtergraph += '[{}]'.format(filter_id)
        # Add filtergraph
        filtergraph += '{}'.format(filter_string)
        # Update filter ID and add it to the end
        filter_id = '0:vf:{}-{}'.format(stream_id, count)
        filtergraph += '[{}]'.format(filter_id)
        # Increment filter ID counter
        count += 1
    return filter_id, filtergraph
