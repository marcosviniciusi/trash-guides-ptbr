#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    plugins.tools.py

    Written by:               Josh.5 <jsunnex@gmail.com>
    Date:                     17 Feb 2023, (12:07 PM)

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


def get_video_stream_resolution(streams: list) -> object:
    """
    Given a list of streams from a video file, returns the first video
    stream's resolution and index.

    :param streams: The list of streams for the video file.
    :type streams: list
    :return: A tuple of the (width, height, stream_index,)
    :rtype: object
    """
    width = 0
    height = 0
    video_stream_index = 0

    for stream in streams:
        if stream.get('codec_type', '') == 'video':
            width = stream.get('width', stream.get('coded_width', 0))
            height = stream.get('height', stream.get('coded_height', 0))
            video_stream_index = stream.get('index')
            break

    return width, height, video_stream_index
