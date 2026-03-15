#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    plugins.plugin.py

    Written by:               Josh.5 <jsunnex@gmail.com>
    Date:                     4 June 2022, (6:08 PM)

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

"""
TODO:
    - Add support for 2-pass libx264 and libx265
    - Add support for VAAPI 264
    - Add support for NVENC 264/265
    - Add advanced input forms for building custom ffmpeg queries
    - Add support for source bitrate matching on basic mode
"""

import os
import logging
import subprocess
import json
from video_transcoder.lib import plugin_stream_mapper, tools
from video_transcoder.lib.ffmpeg import Parser, Probe
from video_transcoder.lib.global_settings import GlobalSettings
from video_transcoder.lib.encoders.libx import LibxEncoder
from video_transcoder.lib.encoders.qsv import QsvEncoder
from video_transcoder.lib.encoders.vaapi import VaapiEncoder
from video_transcoder.lib.encoders.nvenc import NvencEncoder
from video_transcoder.lib.encoders.libsvtav1 import LibsvtAv1Encoder
from video_transcoder.lib.encoders.videotoolbox import VideoToolboxEncoder
from unmanic.libs.unplugins.settings import PluginSettings


# Configure plugin logger
logger = logging.getLogger("Unmanic.Plugin.video_transcoder")


class Settings(PluginSettings):

    def __init__(self, *args, **kwargs):
        # Add optional flag to disable default fallback logic. This should be set for the plugin runner calls
        self.apply_default_fallbacks = kwargs.pop('apply_default_fallbacks', True)
        super(Settings, self).__init__(*args, **kwargs)
        self.settings = self.__build_settings_object()
        self.global_settings = GlobalSettings(self)
        self.form_settings = self.__build_form_settings_object()

    def __build_form_settings_object(self):
        """
        Build a form input config for all the plugin settings
        This input changes dynamically based on the encoder selected

        :return:
        """
        return_values = {}
        for setting in self.settings:
            # Fetch currently configured encoder
            # This should be done every loop as some settings my change this value
            selected_encoder = tools.available_encoders(settings=self).get(self.get_setting('video_encoder'))
            # Disable form by default
            setting_form_settings = {
                "display": "hidden"
            }
            # First check if selected_encoder object has form settings method
            if hasattr(selected_encoder, 'get_{}_form_settings'.format(setting)):
                getter = getattr(selected_encoder, 'get_{}_form_settings'.format(setting))
                if callable(getter):
                    setting_form_settings = getter()
            # Next check if global_settings object has form settings method
            elif hasattr(self.global_settings, 'get_{}_form_settings'.format(setting)):
                getter = getattr(self.global_settings, 'get_{}_form_settings'.format(setting))
                if callable(getter):
                    setting_form_settings = getter()
            # Apply form settings
            return_values[setting] = setting_form_settings
        return return_values

    def __available_encoders(self):
        return_encoders = {}
        encoder_libs = [
            LibxEncoder,
            QsvEncoder,
            VaapiEncoder,
            NvencEncoder,
            LibsvtAv1Encoder,
        ]
        for encoder_class in encoder_libs:
            encoder_lib = encoder_class(self)
            for encoder in encoder_lib.provides():
                return_encoders[encoder] = encoder_lib
        return return_encoders

    def __encoder_settings_object(self):
        """
        Returns a list of encoder settings for FFmpeg

        :return:
        """
        # Initial options forces the order they appear in the settings list
        # We need this because some encoders have settings that
        # Fetch all encoder settings from encoder libs
        libx_options = LibxEncoder(self.settings).options()
        qsv_options = QsvEncoder(self.settings).options()
        vaapi_options = VaapiEncoder(self.settings).options()
        nvenc_options = NvencEncoder(self.settings).options()
        libsvtav1_options = LibsvtAv1Encoder(self.settings).options()
        videotoolbox_options = VideoToolboxEncoder(self.settings).options()
        return {
            **libx_options,
            **qsv_options,
            **vaapi_options,
            **nvenc_options,
            **libsvtav1_options,
            **videotoolbox_options,
        }

    def __build_settings_object(self):
        # Global and main config options
        global_settings = GlobalSettings.options()
        main_options = global_settings.get('main_options')
        encoder_selection = global_settings.get('encoder_selection')
        encoder_settings = self.__encoder_settings_object()
        advanced_input_options = global_settings.get('advanced_input_options')
        output_settings = global_settings.get('output_settings')
        filter_settings = global_settings.get('filter_settings')
        smart_output_target = global_settings.get('smart_output_target')
        return {
            **main_options,
            **encoder_selection,
            **encoder_settings,
            **advanced_input_options,
            **output_settings,
            **filter_settings,
            **smart_output_target,
        }


def check_file_has_processed_metadata(path):
    """
    Check if file has UNMANIC_STATUS=processed metadata using ffprobe
    
    :param path: Path to the file
    :return: True if metadata exists with matching value, False otherwise
    """
    try:
        # Use ffprobe to get file metadata in JSON format
        command = [
            'ffprobe',
            '-v', 'quiet',
            '-print_format', 'json',
            '-show_format',
            path
        ]
        
        result = subprocess.run(command, capture_output=True, text=True, timeout=30)
        
        if result.returncode != 0:
            logger.warning(f"ffprobe failed for file: {path}")
            return False
        
        # Parse JSON output
        probe_data = json.loads(result.stdout)
        
        # Check if format tags exist
        if 'format' in probe_data and 'tags' in probe_data['format']:
            tags = probe_data['format']['tags']
            
            # Check for UNMANIC_STATUS metadata (case-insensitive)
            for key, value in tags.items():
                if key.upper() == 'UNMANIC_STATUS':
                    if value == 'processed':
                        logger.debug(f"Found UNMANIC_STATUS=processed in file: {path}")
                        return True
        
        return False
        
    except subprocess.TimeoutExpired:
        logger.error(f"ffprobe timed out for file: {path}")
        return False
    except json.JSONDecodeError:
        logger.error(f"Failed to parse ffprobe output for file: {path}")
        return False
    except Exception as e:
        logger.error(f"Error checking metadata for file {path}: {str(e)}")
        return False


def on_library_management_file_test(data):
    """
    Runner function - enables additional actions during the library management file tests.

    The 'data' object argument includes:
        library_id                      - The library that the current task is associated with
        path                            - String containing the full path to the file being tested.
        issues                          - List of currently found issues for not processing the file.
        add_file_to_pending_tasks       - Boolean, is the file currently marked to be added to the queue for processing.
        priority_score                  - Integer, an additional score that can be added to set the position of the new task in the task queue.
        shared_info                     - Dictionary, information provided by previous plugin runners. This can be appended to for subsequent runners.

    :param data:
    :return:

    """

    # Get settings (do not persist defaults during worker/library execution)
    settings = Settings(library_id=data.get('library_id'), apply_default_fallbacks=False)

    # Get the path to the file
    abspath = data.get('path')

    # Get file probe
    probe = Probe.init_probe(data, logger, allowed_mimetypes=['video'])
    if not probe:
        # File not able to be probed by ffprobe
        return

    # Get stream mapper
    mapper = plugin_stream_mapper.PluginStreamMapper()
    mapper.set_default_values(settings, abspath, probe)

    # Check if this file needs to be processed
    if mapper.streams_need_processing():
        # If force_transcode is enabled, check if file already has processed metadata
        if settings.get_setting('force_transcode') and check_file_has_processed_metadata(abspath):
            logger.debug(
                "File '%s' has UNMANIC_STATUS=processed metadata and force_transcode is enabled. Ignoring this file.",
                abspath)
            return
        # Mark this file to be added to the pending tasks
        data['add_file_to_pending_tasks'] = True
        logger.debug("File '%s' should be added to task list. Plugin found streams require processing.", abspath)
    else:
        logger.debug("File '%s' does not contain streams require processing.", abspath)


def on_worker_process(data):
    """
    Runner function - enables additional configured processing jobs during the worker stages of a task.

    The 'data' object argument includes:
        worker_log              - Array, the log lines that are being tailed by the frontend. Can be left empty.
        library_id              - Number, the library that the current task is associated with.
        exec_command            - Array, a subprocess command that Unmanic should execute. Can be empty.
        command_progress_parser - Function, a function that Unmanic can use to parse the STDOUT of the command to collect progress stats. Can be empty.
        file_in                 - String, the source file to be processed by the command.
        file_out                - String, the destination that the command should output (may be the same as the file_in if necessary).
        original_file_path      - String, the absolute path to the original file.
        repeat                  - Boolean, should this runner be executed again once completed with the same variables.

    :param data:
    :return:

    """
    # Default to no FFMPEG command required. This prevents the FFMPEG command from running if it is not required
    data['exec_command'] = []
    data['repeat'] = False

    worker_log = data.get('worker_log')

    # Get settings (do not persist defaults during worker execution)
    settings = Settings(library_id=data.get('library_id'), apply_default_fallbacks=False)

    # Get the path to the file
    abspath = data.get('file_in')

    # Get file probe
    tools.append_worker_log(worker_log, "Probing file: {}".format(abspath))
    probe = Probe(logger, allowed_mimetypes=['video'])
    if not probe.file(abspath):
        # File probe failed, skip the rest of this test
        tools.append_worker_log(worker_log, "Probe failed - skipping file")
        return

    # Get stream mapper
    mapper = plugin_stream_mapper.PluginStreamMapper(worker_log=worker_log)
    mapper.set_default_values(settings, abspath, probe)

    # Check if this file needs to be processed
    tools.append_worker_log(worker_log, "Checking what streams need processing...")
    needs_processing = mapper.streams_need_processing()
    if needs_processing:
        # If force_transcode is enabled, check if file already has processed metadata
        if settings.get_setting('force_transcode') and check_file_has_processed_metadata(abspath):
            # Do not process this file, it has been processed before
            tools.append_worker_log(worker_log, "File already has processed metadata - skipping")
            return

        # Set the output file
        if settings.get_setting('keep_container'):
            # Do not remux the file. Keep the file out in the same container
            mapper.set_output_file(data.get('file_out'))
            tools.append_worker_log(worker_log, "Output container kept - writing to: {}".format(data.get('file_out')))
        else:
            # Force the remux to the configured container
            container_extension = settings.get_setting('dest_container')
            split_file_out = os.path.splitext(data.get('file_out'))
            new_file_out = "{}.{}".format(split_file_out[0], container_extension.lstrip('.'))
            mapper.set_output_file(new_file_out)
            data['file_out'] = new_file_out
            tools.append_worker_log(worker_log, "Output container set to '{}' - writing to: {}".format(container_extension, new_file_out))

        # # Pretty, wrapped printing of the command to null for debugging. Should always be commented out.
        # mapper.set_output_null()
        # print(tools.format_command_multiline(mapper, max_width=120))

        # Get generated ffmpeg args
        tools.append_worker_log(worker_log, "Generating FFmpeg command...")
        mapper.enable_execution_stage()
        mapper.streams_need_processing()
        ffmpeg_args = mapper.get_ffmpeg_args()

        # Apply ffmpeg args to command
        data['exec_command'] = ['ffmpeg']
        data['exec_command'] += ffmpeg_args

        # Set the parser
        parser = Parser(logger)
        parser.set_probe(probe)
        data['command_progress_parser'] = parser.parse_progress
    else:
        tools.append_worker_log(worker_log, "No streams require processing - no FFmpeg command generated")

    return


def on_postprocessor_task_results(data):
    """
    Runner function - provides a means for additional postprocessor functions based on the task success.

    The 'data' object argument includes:
        final_cache_path                - The path to the final cache file that was then used as the source for all destination files.
        library_id                      - The library that the current task is associated with.
        task_processing_success         - Boolean, did all task processes complete successfully.
        file_move_processes_success     - Boolean, did all postprocessor movement tasks complete successfully.
        destination_files               - List containing all file paths created by postprocessor file movements.
        source_data                     - Dictionary containing data pertaining to the original source file.

    :param data:
    :return:
    """
    # This function is no longer needed as metadata is handled by ffmpeg
    # The UNMANIC_STATUS=processed metadata should be added via ffmpeg -metadata flag
    pass