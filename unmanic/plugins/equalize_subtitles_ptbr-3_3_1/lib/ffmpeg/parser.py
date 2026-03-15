#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    plugins.parser.py

    Written by:               Josh.5 <jsunnex@gmail.com>
    Date:                     12 Aug 2021, (9:00 AM)

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
import datetime
import math
import re
from logging import Logger

from .probe import Probe


class Parser(object):
    """
    Parser

    Class to manage parsing the FFmpeg commandline output and return progress data for Unmanic.
    """

    percent = '0'
    time = '0'
    frame = '0'
    speed = '0'
    bitrate = '0'

    src_fps = None
    duration = None
    total_frames = None

    def __init__(self, logger: Logger, duration=None, total_frames=None):
        self.logger = logger

    def set_probe(self, probe: Probe):
        """
        Set the information require to calculate progress from the file probe

        :param probe:
        :return:
        """
        # Get FPS from file probe info
        self.src_fps = None
        try:
            file_probe_streams = probe.get('streams', [])
            self.src_fps = eval(file_probe_streams[0]['avg_frame_rate'])
        except ZeroDivisionError:
            # Warning, Cannot use input FPS
            self.logger.warning('Cannot use input FPS for FFmpeg conversion progress')
        except KeyError:
            # Warning, Cannot use input FPS
            self.logger.warning('Cannot use input FPS for FFmpeg conversion progress - key not found in probe')
        if self.src_fps == 0:
            raise ValueError('Unexpected zero FPS')

        # Get Duration from file probe info
        self.duration = None
        try:
            file_probe_format = probe.get('format', {})
            self.duration = float(file_probe_format['duration'])
        except ZeroDivisionError:
            # Warning, Cannot use input Duration
            self.logger.warning('Cannot use input Duration for FFmpeg conversion progress')
        except KeyError:
            # Warning, Cannot use input Duration
            self.logger.warning('Cannot use input Duration for FFmpeg conversion progress - key not found in probe')

        if self.src_fps is None and self.duration is None:
            raise ValueError('Unable to match against FPS or Duration.')

        # If we have probed both the source FPS and total duration, then we can calculate the total frames
        if self.duration and self.src_fps and self.duration > 0 and self.src_fps > 0:
            self.total_frames = int(self.duration * self.src_fps)

    def parse_progress(self, line_text):
        """
        Given a single line of STDOUT text, parse it using regex and extract progress as a percent value.

        :param line_text:
        :return:
        """
        # Fetch data from line text
        if line_text and ('frame=' in line_text or 'time=' in line_text):
            # Update time
            _time = self.get_progress_from_regex_of_string(line_text, r"time=(\s+|)(\d+:\d+:\d+\.\d+)", self.time)
            if _time:
                self.time = str(self.time_string_to_seconds(_time))

            # Update frames
            _frame = self.get_progress_from_regex_of_string(line_text, r"frame=(\s+|)(\d+)", self.frame)
            if _frame and int(_frame) > int(self.frame):
                self.frame = _frame

            # Update speed
            _speed = self.get_progress_from_regex_of_string(line_text, r"speed=(\s+|)(\d+\.\d+)", self.speed)
            if _speed:
                self.speed = str(_speed)

            # Update bitrate
            _bitrate = self.get_progress_from_regex_of_string(line_text, r"bitrate=(\s+|)(\d+\.\d+\w+|\d+w)",
                                                              self.bitrate)
            if _bitrate:
                self.bitrate = "{}/s".format(_bitrate)

            # Update file size
            _size = self.get_progress_from_regex_of_string(line_text, r"size=(\s+|)(\d+\w+|\d+.\d+\w+)", self.frame)
            if _size:
                self.file_size = _size

            # Update percent
            _percent = None
            if _frame and self.total_frames and int(_frame) > 0 and int(self.total_frames) > 0:
                # If we have both the current frame and the total number of frames, then we can easily calculate the %
                # _percent = float(int(_frame) / int(self.total_frames))
                _percent = float(int(_frame) / int(self.total_frames)) * 100
                _percent = math.trunc(_percent)
            elif self.time and self.duration and int(self.time) > 0 and int(self.duration) > 0:
                # If that was not successful, we need to resort to assuming the percent by the duration and the time
                # passed so far
                _percent = float(int(self.time) / int(self.duration)) * 100
                _percent = math.trunc(_percent)
            if _percent and int(_percent) > int(self.percent):
                self.percent = str(_percent)

        # Return the values.
        # Currently Unmanic only cares about the percent. So for now we will ignore everything else.
        return {
            'percent': self.percent
        }

    @staticmethod
    def time_string_to_seconds(time_string):
        """
        Converts a time string from the FFmpeg output into an epoch timestamp

        :param time_string:
        :return:
        """
        pt = datetime.datetime.strptime(time_string, '%H:%M:%S.%f')
        return pt.second + pt.minute * 60 + pt.hour * 3600

    @staticmethod
    def get_progress_from_regex_of_string(line, regex_string, default=None):
        """
        Parse value from line text using the given regular expression.
        If no match is found, return the given default value.

        :param line:
        :param regex_string:
        :param default:
        :return:
        """
        if default is None:
            default = 0

        return_value = default
        regex = re.compile(regex_string)
        findall = re.findall(regex, line)
        if findall:
            split_list = findall[-1]
            if len(split_list) == 2:
                return_value = split_list[1].strip()
        return return_value
