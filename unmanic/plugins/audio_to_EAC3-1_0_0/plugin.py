#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    unmanic-plugins.plugin.py

    Written by:               Josh.5 <jsunnex@gmail.com>
    Modified by:              Marcos Gabriel
    Date:                     12 Mar 2026

    Copyright:
        Copyright (C) 2021 Josh Sunnex
        Copyright (C) 2026 Marcos Gabriel

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

from unmanic.libs.unplugins.settings import PluginSettings

from dts_to_dd.lib.ffmpeg import StreamMapper, Probe, Parser

# Configure plugin logger
logger = logging.getLogger("Unmanic.Plugin.dts_to_dd")


class Settings(PluginSettings):
    settings = {
        'eac3_bitrate':    '1536k',
        'remove_original': True,
    }

    form_settings = {
        "eac3_bitrate": {
            "label":      "EAC3 5.1 bitrate",
            "input_type": "select",
            "select_options": [
                {'value': "768k",  'label': "768 kbps (5.1 balanced)"},
                {'value': "1024k", 'label': "1024 kbps (5.1 good)"},
                {'value': "1536k", 'label': "1536 kbps (5.1 maximum, recommended)"},
            ],
        },
        "remove_original": {
            "label":      "Remove original stream after conversion (DTS, FLAC, Opus, Vorbis)",
            "input_type": "checkbox",
        },
    }


class PluginStreamMapper(StreamMapper):
    def __init__(self):
        super(PluginStreamMapper, self).__init__(logger, ['audio'])
        self.settings = None

    def set_settings(self, settings):
        self.settings = settings

    def test_stream_needs_processing(self, stream_info: dict):
        """
        Returns True for DTS, FLAC, Opus and Vorbis streams.
        AC3, EAC3, TrueHD and AAC are left untouched (copy).
        """
        codec = stream_info.get('codec_name', '').lower()
        return codec in ('dts', 'flac', 'opus', 'vorbis')

    def custom_stream_mapping(self, stream_info: dict, stream_id: int):
        """
        Convert stream to EAC3 5.1.
        - Sources > 6 channels are downmixed to 5.1 via -ac 6.
        - Sources <= 6 channels preserve channel count.
        - Original stream removed or kept based on remove_original setting.
        """
        codec_name    = stream_info.get('codec_name', '').lower()
        channels      = stream_info.get('channels', 6)
        original_lang = stream_info.get('tags', {}).get('language', '')

        # Cap at 5.1 (6 channels)
        output_channels = min(channels, 6)

        eac3_bitrate = self.settings.get_setting('eac3_bitrate')

        if output_channels <= 1:
            title = f'EAC3 Mono ({eac3_bitrate})'
        elif output_channels == 2:
            title = f'EAC3 Stereo ({eac3_bitrate})'
        else:
            title = f'EAC3 5.1 ({eac3_bitrate})'

        logger.info(
            f"Converting {codec_name.upper()} stream "
            f"(audio #{stream_id}, {channels}ch -> {output_channels}ch, {eac3_bitrate})"
        )

        stream_mapping  = ['-map', f'0:a:{stream_id}']
        stream_encoding = [
            f'-c:a:{stream_id}',          'eac3',
            f'-b:a:{stream_id}',          eac3_bitrate,
            f'-ac:a:{stream_id}',         str(output_channels),
            f'-metadata:s:a:{stream_id}', f'title={title}',
        ]

        if original_lang:
            stream_encoding += [f'-metadata:s:a:{stream_id}', f'language={original_lang}']

        if not self.settings.get_setting('remove_original'):
            # Keep original: map again as copy after the converted stream
            stream_mapping  += ['-map', f'0:a:{stream_id}']
            stream_encoding += [f'-c:a:{stream_id + 1}', 'copy']
            logger.info(f"Keeping original {codec_name.upper()} track")
        else:
            logger.info(f"Removing original {codec_name.upper()} track")

        return {
            'stream_mapping':  stream_mapping,
            'stream_encoding': stream_encoding,
        }


def on_library_management_file_test(data):
    """
    Runner function - enables additional actions during the library management file tests.

    The 'data' object argument includes:
        path                        - String containing the full path to the file being tested.
        issues                      - List of currently found issues for not processing the file.
        add_file_to_pending_tasks   - Boolean, is the file currently marked to be added to the queue for processing.

    :param data:
    :return:
    """
    abspath = data.get('path')

    probe = Probe(logger, allowed_mimetypes=['audio', 'video'])
    if not probe.file(abspath):
        return data

    if data.get('library_id'):
        settings = Settings(library_id=data.get('library_id'))
    else:
        settings = Settings()

    mapper = PluginStreamMapper()
    mapper.set_settings(settings)
    mapper.set_probe(probe)

    if mapper.streams_need_processing():
        data['add_file_to_pending_tasks'] = True
        logger.debug("File '{}' should be added to task list.".format(abspath))
    else:
        logger.debug("File '{}' does not require processing.".format(abspath))

    return data


def on_worker_process(data):
    """
    Runner function - enables additional configured processing jobs during the worker stages of a task.

    The 'data' object argument includes:
        exec_command            - A command that Unmanic should execute. Can be empty.
        command_progress_parser - A function that Unmanic can use to parse the STDOUT of the command to collect progress stats. Can be empty.
        file_in                 - The source file to be processed by the command.
        file_out                - The destination that the command should output (may be the same as the file_in if necessary).
        original_file_path      - The absolute path to the original file.
        repeat                  - Boolean, should this runner be executed again once completed with the same variables.

    DEPRECIATED 'data' object args passed for legacy Unmanic versions:
        exec_ffmpeg             - Boolean, should Unmanic run FFMPEG with the data returned from this plugin.
        ffmpeg_args             - A list of Unmanic's default FFMPEG args.

    :param data:
    :return:
    """
    data['exec_command'] = []
    data['repeat'] = False
    data['exec_ffmpeg'] = False

    abspath = data.get('file_in')

    probe = Probe(logger, allowed_mimetypes=['audio', 'video'])
    if not probe.file(abspath):
        return data

    if data.get('library_id'):
        settings = Settings(library_id=data.get('library_id'))
    else:
        settings = Settings()

    mapper = PluginStreamMapper()
    mapper.set_settings(settings)
    mapper.set_probe(probe)

    if mapper.streams_need_processing():
        mapper.set_input_file(abspath)

        # Keep same container extension
        split_file_in  = os.path.splitext(abspath)
        split_file_out = os.path.splitext(data.get('file_out'))
        mapper.set_output_file("{}{}".format(split_file_out[0], split_file_in[1]))

        ffmpeg_args = mapper.get_ffmpeg_args()

        data['exec_command'] = ['ffmpeg'] + ffmpeg_args
        data['ffmpeg_args']  = ffmpeg_args

        parser = Parser(logger)
        parser.set_probe(probe)
        data['command_progress_parser'] = parser.parse_progress

    return data
