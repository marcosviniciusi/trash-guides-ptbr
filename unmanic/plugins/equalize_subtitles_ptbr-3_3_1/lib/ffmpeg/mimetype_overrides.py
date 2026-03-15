#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    plugins.probe.py

    Written by:               Josh.5 <jsunnex@gmail.com>
    Date:                     17 Mar 2022, (9:29 AM)

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


class MimetypeOverrides(object):
    audio = {
        '.flac': 'audio/flac',
    }
    video = {
        '.m4v':   'video/x-m4v',
        '.3gp':   'video/3gpp',
        '.axv':   'video/annodex',
        '.dl':    'video/dl',
        '.dif':   'video/dv',
        '.dv':    'video/dv',
        '.fli':   'video/fli',
        '.gl':    'video/gl',
        '.mpeg':  'video/mpeg',
        '.mpg':   'video/mpeg',
        '.mpe':   'video/mpeg',
        '.ts':    'video/MP2T',
        '.mp4':   'video/mp4',
        '.qt':    'video/quicktime',
        '.mov':   'video/quicktime',
        '.ogv':   'video/ogg',
        '.webm':  'video/webm',
        '.mxu':   'video/vnd.mpegurl',
        '.flv':   'video/x-flv',
        '.lsf':   'video/x-la-asf',
        '.lsx':   'video/x-la-asf',
        '.mng':   'video/x-mng',
        '.asf':   'video/x-ms-asf',
        '.asx':   'video/x-ms-asf',
        '.wm':    'video/x-ms-wm',
        '.wmv':   'video/x-ms-wmv',
        '.wmx':   'video/x-ms-wmx',
        '.wvx':   'video/x-ms-wvx',
        '.avi':   'video/x-msvideo',
        '.movie': 'video/x-sgi-movie',
        '.mpv':   'video/x-matroska',
        '.mkv':   'video/x-matroska',
    }

    def get_all(self):
        return {**self.audio, **self.video}
