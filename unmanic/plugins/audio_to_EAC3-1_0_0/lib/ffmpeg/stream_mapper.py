#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    unmanic.stream_mapper.py

    Written by:               Josh.5 <jsunnex@gmail.com>
    Date:                     30 Jul 2021, (9:41 AM)

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
import os
import shutil
from logging import Logger

from .probe import Probe


class StreamMapper(object):
    """
    StreamMapper

    Manage FFmpeg stream mapping and generating FFmpeg command-line args.
    """

    probe: Probe = None

    stream_type_idents = {
        'video':      'v',
        'audio':      'a',
        'subtitle':   's',
        'data':       'd',
        'attachment': 't'
    }

    processing_stream_type = ''
    found_streams_to_encode = False
    stream_mapping = []
    stream_encoding = []
    video_stream_count = 0
    audio_stream_count = 0
    subtitle_stream_count = 0
    data_stream_count = 0
    attachment_stream_count = 0

    input_file = ''
    output_file = ''
    generic_options = []
    main_options = []
    advanced_options = []
    format_options = []

    def __init__(self, logger: Logger, processing_stream_type: list):
        # Ensure ffmpeg is installed
        if shutil.which('ffmpeg') is None:
            raise Exception("Unable to find executable 'ffmpeg'. Please ensure that FFmpeg is installed correctly.")

        self.logger = logger
        if processing_stream_type is not None:
            if any(pst for pst in processing_stream_type if
                   pst not in ['video', 'audio', 'subtitle', 'data', 'attachment']):
                raise Exception(
                    "processing_stream_type must be one of ['video','audio','subtitle','data','attachment']")
            self.processing_stream_type = processing_stream_type

        # Set default Generic options
        self.generic_options = [
            '-hide_banner',
            '-loglevel', 'info',
        ]

        # Set default Main options
        self.main_options = []

        # Set default Advanced options
        self.advanced_options = [
            '-strict', '-2',
            '-max_muxing_queue_size', '4096',
        ]

    def __copy_stream_mapping(self, codec_type, stream_id):
        """
        Create stream mapping to simply copy the stream without encoding.
        Apply this to the 'stream_mapping' and 'stream_encoding' attributes.

        :param codec_type:
        :param stream_id:
        :return:
        """
        # Map this stream for copy to the destination file
        self.stream_mapping += ['-map', '0:{}:{}'.format(codec_type, stream_id)]
        # Add a encoding flag copying this stream
        self.stream_encoding += ['-c:{}:{}'.format(codec_type, stream_id), 'copy']

    def __apply_custom_stream_mapping(self, mapping_dict):
        """
        Apply a custom stream mapping.
        This method tests that the provided mapping dictionary is valid.
        If it is valid, apply it to the 'stream_mapping' and 'stream_encoding' attributes.

        :param mapping_dict:
        :return:
        """
        # Ensure the mapping dictionary provided is correct
        if not isinstance(mapping_dict, dict):
            raise Exception("processing_stream_type must return a dictionary")
        if 'stream_mapping' not in mapping_dict:
            raise Exception("processing_stream_type return dictionary must contain 'stream_mapping' key")
        if not isinstance(mapping_dict.get('stream_mapping'), list):
            raise Exception("processing_stream_type 'stream_mapping' value must be of type 'list'")
        if 'stream_encoding' not in mapping_dict:
            raise Exception("processing_stream_type return dictionary must contain 'stream_encoding' key")
        if not isinstance(mapping_dict.get('stream_encoding'), list):
            raise Exception("processing_stream_type 'stream_mapping' value must be of type 'list'")
        # Append this custom stream mapping
        self.stream_mapping += mapping_dict.get('stream_mapping')
        # Append these custom encoding flags
        self.stream_encoding += mapping_dict.get('stream_encoding')

    def set_probe(self, probe: Probe):
        """Set the ffprobe Probe object"""
        self.probe = probe

    def test_stream_needs_processing(self, stream_info: dict):
        """
        Overwrite this function to test a stream.
        Return 'True' if it needs to be process.
        Return 'False' if it should just be copied over to the new file.

        :param stream_info:
        :return: bool
        """
        raise NotImplementedError

    def custom_stream_mapping(self, stream_info: dict, stream_id: int):
        """
        Configure custom mapping for a single stream
        This function must return a dictionary containing 2 key values:
            {
                'stream_mapping': [],
                'stream_encoding': [],
            }

        :param stream_info:
        :param stream_id:
        :return: dict
        """
        raise NotImplementedError

    def __set_stream_mapping(self):
        """
        Sets a list of stream maps and encoding variables

        :return:
        """

        # Require a list of probe streams to continue
        file_probe_streams = self.probe.get('streams')
        if not file_probe_streams:
            return False

        # What type of streams are we looking for ('video', 'audio', 'subtitle', 'data' or 'attachment')
        processing_stream_type = self.processing_stream_type

        # Map the streams into two arrays that will be placed together in the correct order.
        self.stream_mapping = []
        self.stream_encoding = []

        # Count streams by type
        self.video_stream_count = 0
        self.audio_stream_count = 0
        self.subtitle_stream_count = 0
        self.data_stream_count = 0
        self.attachment_stream_count = 0

        # Set flag for finding a stream that needs to be processed as False by default.
        found_streams_to_process = False

        # Loop over all streams found in the file probe
        for stream_info in file_probe_streams:
            codec_type = stream_info.get('codec_type', '').lower()
            # Fore each of these streams:

            # If this is a video/image stream?
            if codec_type == "video":
                # Map the video stream
                if "video" in processing_stream_type:
                    if not self.test_stream_needs_processing(stream_info):
                        self.__copy_stream_mapping('v', self.video_stream_count)
                        self.video_stream_count += 1
                        continue
                    else:
                        mapping = self.custom_stream_mapping(stream_info, self.video_stream_count)
                        if mapping:
                            found_streams_to_process = True
                            self.__apply_custom_stream_mapping(mapping)
                        else:
                            self.__copy_stream_mapping('v', self.video_stream_count)
                        self.video_stream_count += 1
                        continue
                else:
                    self.__copy_stream_mapping('v', self.video_stream_count)
                    self.video_stream_count += 1
                    continue

            # If this is a audio stream?
            elif codec_type == "audio":
                # Map the audio stream
                if "audio" in processing_stream_type:
                    if not self.test_stream_needs_processing(stream_info):
                        self.__copy_stream_mapping('a', self.audio_stream_count)
                        self.audio_stream_count += 1
                        continue
                    else:
                        mapping = self.custom_stream_mapping(stream_info, self.audio_stream_count)
                        if mapping:
                            found_streams_to_process = True
                            self.__apply_custom_stream_mapping(mapping)
                        else:
                            self.__copy_stream_mapping('a', self.audio_stream_count)
                        self.audio_stream_count += 1
                        continue
                else:
                    if self.settings.get_setting('mode') == 'advanced':
                        amaps = self.settings.get_setting('custom_options').split()
                        self.logger.debug("Advanced Mode Video Settings with custom audio encoding: '%s'", amaps)
                        if '-c:a' not in amaps:
                            self.logger.debug("-c:a not detected in custom mappings: '%s'", amaps)
                            self.__copy_stream_mapping('a', self.audio_stream_count)
                        else:
                            self.logger.debug("-c:a detected in custom mappings: '%s'", amaps)
                            self.stream_mapping += ['-map', '0:{}:{}'.format('a', self.audio_stream_count)]
                        self.audio_stream_count += 1
                    else:
                        self.__copy_stream_mapping('a', self.audio_stream_count)
                        self.audio_stream_count += 1
                    continue

            # If this is a subtitle stream?
            elif codec_type == "subtitle":
                # Map the subtitle stream
                if "subtitle" in processing_stream_type:
                    if not self.test_stream_needs_processing(stream_info):
                        self.__copy_stream_mapping('s', self.subtitle_stream_count)
                        self.subtitle_stream_count += 1
                        continue
                    else:
                        mapping = self.custom_stream_mapping(stream_info, self.subtitle_stream_count)
                        if mapping:
                            found_streams_to_process = True
                            self.__apply_custom_stream_mapping(mapping)
                        else:
                            self.__copy_stream_mapping('s', self.subtitle_stream_count)
                        self.subtitle_stream_count += 1
                        continue
                else:
                    if self.settings.get_setting('mode') == 'advanced':
                        submaps = self.settings.get_setting('custom_options').split()
                        self.logger.debug("Advanced Mode Video Settings with custom subtitle encoding: '%s'", submaps)
                        if '-c:s' not in submaps:
                            self.logger.debug("-c:s not detected in custom mappings: '%s'", submaps)
                            self.__copy_stream_mapping('s', self.subtitle_stream_count)
                        else:
                            self.logger.debug("-c:s detected in custom mappings: '%s'", submaps)
                            self.stream_mapping += ['-map', '0:{}:{}'.format('s', self.subtitle_stream_count)]
                        self.subtitle_stream_count += 1
                    else:
                        self.__copy_stream_mapping('s', self.subtitle_stream_count)
                        self.subtitle_stream_count += 1
                    continue

            # If this is a data stream?
            elif codec_type == "data":
                # Map the data stream
                if "data" in processing_stream_type:
                    if not self.test_stream_needs_processing(stream_info):
                        self.__copy_stream_mapping('d', self.data_stream_count)
                        self.data_stream_count += 1
                        continue
                    else:
                        mapping = self.custom_stream_mapping(stream_info, self.data_stream_count)
                        if mapping:
                            found_streams_to_process = True
                            self.__apply_custom_stream_mapping(mapping)
                        else:
                            self.__copy_stream_mapping('d', self.data_stream_count)
                        self.data_stream_count += 1
                        continue
                else:
                    self.__copy_stream_mapping('d', self.data_stream_count)
                    self.data_stream_count += 1
                    continue

            # If this is a attachment stream?
            elif codec_type == "attachment":
                # Map the attachment stream
                if "attachment" in processing_stream_type:
                    if not self.test_stream_needs_processing(stream_info):
                        self.__copy_stream_mapping('t', self.attachment_stream_count)
                        self.attachment_stream_count += 1
                        continue
                    else:
                        mapping = self.custom_stream_mapping(stream_info, self.attachment_stream_count)
                        if mapping:
                            found_streams_to_process = True
                            self.__apply_custom_stream_mapping(mapping)
                        else:
                            self.__copy_stream_mapping('t', self.attachment_stream_count)
                        self.attachment_stream_count += 1
                        continue
                else:
                    self.__copy_stream_mapping('t', self.attachment_stream_count)
                    self.attachment_stream_count += 1
                    continue

        return found_streams_to_process

    def __build_args(self, options: list, *args, **kwargs):
        """
        Build a list of FFmpeg options based on the given default options, args and kwargs

        :param options:
        :param args:
        :param kwargs:
        :return:
        """
        for arg in args:
            if arg in options:
                options = [value for value in options if value != arg]
                options += [arg]
            else:
                options += [arg]
        for kwarg in kwargs:
            key = kwarg
            value = kwargs.get(kwarg)
            if key in options:
                key_pos = options.index(key)
                val_pos = int(key_pos) + 1
                options[key_pos] = key
                options[val_pos] = value
            else:
                options += [key, value]
        return

    def streams_need_processing(self):
        """
        Returns True/False if the streams need to be processed.
        If at least one stream needs custom stream mapping (processing), then this will return True.
        If the stream mapping will copy all streams to output file untouched, then this will return False.

        :return:
        """
        return self.__set_stream_mapping()

    def container_needs_remuxing(self, container_extension):
        """
        Returns True/False if the file container needs to be processed.

        :return:
        """
        if not self.input_file:
            raise Exception("Input file not yet set")

        split_file_in = os.path.splitext(self.input_file)
        if split_file_in[1].lstrip('.') != container_extension.lstrip('.'):
            return True
        return False

    def set_input_file(self, path):
        """Set the input file for the FFmpeg args"""
        self.input_file = os.path.abspath(path)

    def set_output_file(self, path):
        """Set the output file for the FFmpeg args"""
        self.output_file = os.path.abspath(path)

    def set_output_null(self):
        """Set the output container to NULL for the FFmpeg args"""
        self.output_file = '-'

    def set_ffmpeg_generic_options(self, *args, **kwargs):
        """
        Set FFmpeg Generic options.
        These are the initial options that follow the 'ffmpeg' command.

        Ref:
            http://ffmpeg.org/ffmpeg-all.html#Generic-options


        :param args:
        :param kwargs:
        :return:
        """
        self.__build_args(self.generic_options, *args, **kwargs)

    def set_ffmpeg_main_options(self, *args, **kwargs):
        """
        Set FFmpeg Main options.
        These options follow the generic options.
        They include things like the input file(s), metadata mapping, etc.

        Ref:
            http://ffmpeg.org/ffmpeg-all.html#Main-options

        :return:
        """
        self.__build_args(self.main_options, *args, **kwargs)

    def set_ffmpeg_advanced_options(self, *args, **kwargs):
        """
        Set FFmpeg Advanced options.
        These options follow the generic options.
        They include things like the custom stream mapping, custom metadata mapping,
            filters, etc.

        Note:
            The custom stream mapping is carried out with another method.
            This method should not be used for creating custom stream mapping if the
                'stream_mapping' and 'stream_encoding' attributes are set.

        Ref:
            http://ffmpeg.org/ffmpeg-all.html#Advanced-options

        :return:
        """
        self.__build_args(self.advanced_options, *args, **kwargs)

    def get_stream_mapping(self):
        """
        Fetch the custom stream mapping generated by this class.
        If the mapping args are not yet generated, generate them at this point.

        :return:
        """
        if not self.stream_mapping:
            self.__set_stream_mapping()
        return self.stream_mapping

    def get_stream_encoding(self):
        """
        Fetch the custom stream encoding args generated by this class.
        If the encoding args are not yet generated, generate them at this point.

        :return:
        """
        if not self.stream_encoding:
            self.__set_stream_mapping()
        return self.stream_encoding

    def get_ffmpeg_args(self):
        """
        Build the FFmpeg command args and return them as a list.

        :return:
        """
        args = []

        # Add generic options first
        args += self.generic_options

        # Add other main options
        args += self.main_options

        # Add the input file
        # This class requires at least one input file specified with the input_file attribute
        if not self.input_file:
            raise Exception("Input file has not been set")
        args += ['-i', self.input_file]

        # Add advanced options. This includes the stream mapping and the encoding args
        args += self.advanced_options
        args += self.stream_mapping
        args += self.stream_encoding

        # Add the output file
        # This class requires at least one output file specified with the output_file attribute
        if not self.output_file:
            raise Exception("Output file has not been set")
        elif self.output_file == '-':
            if os.name == "nt":
                # Windows uses NUL instead
                self.output_file = 'NUL'
            args += ['-f', 'null']
            args += [self.output_file]
        else:
            args += ['-y', self.output_file]

        return args
