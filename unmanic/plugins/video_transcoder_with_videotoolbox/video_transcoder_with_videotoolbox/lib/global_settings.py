#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    plugins.global_settings.py

    Written by:               Josh.5 <jsunnex@gmail.com>
    Date:                     10 Jun 2022, (6:52 PM)

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
import subprocess

from video_transcoder.lib import tools

supported_codecs = {
    "h264": {
        "label": "H264"
    },
    "hevc": {
        "label": "HEVC/H265"
    },
    "av1":  {
        "label": "AV1"
    },
}


class GlobalSettings:

    def __init__(self, settings):
        self.settings = settings

    @staticmethod
    def options():
        # Global and main config options
        return {
            "main_options":           {
                "mode":                  "basic",
                "max_muxing_queue_size": 2048,
            },
            "encoder_selection":      {
                "video_codec":     "hevc",
                "force_transcode": False,
                "video_encoder":   "libx265",
            },
            "advanced_input_options": {
                "main_options":     "",
                "advanced_options": "-strict -2\n"
                                    "-max_muxing_queue_size 2048\n",
                "custom_options":   "libx264\n"
                                    "-preset slow\n"
                                    "-tune film\n"
                                    "-global_quality 23\n"
                                    "-look_ahead 1\n",
            },
            "output_settings":        {
                "keep_container": True,
                "dest_container": "mkv",
            },
            "filter_settings":        {
                "apply_smart_filters":      False,
                "autocrop_black_bars":      False,
                "target_resolution":        "source",
                "strip_data_streams":       False,
                "strip_attachment_streams": False,
                "apply_custom_filters":     False,
                "custom_software_filters":  "",
            },
            "smart_output_target":   {
                "enable_smart_output_target": False,
                "smart_output_target":        "balanced",
            },
        }

    def __set_default_option(self, select_options, key, default_option=None):
        """
        Sets the default option if the currently set option is not available

        :param select_options:
        :param key:
        :return:
        """
        available_options = []
        for option in select_options:
            available_options.append(option.get("value"))
            if not default_option:
                default_option = option.get("value")
        current_value = self.settings.get_setting(key)
        if not getattr(self.settings, 'apply_default_fallbacks', True):
            return current_value
        if current_value not in available_options:
            # Update in-memory setting for display only. 
            # IMPORTANT: do not persist settings from plugin.
            #   Only the Unmanic API calls should persist to JSON file.
            self.settings.settings_configured[key] = default_option
            return default_option
        return current_value

    def get_mode_form_settings(self):
        return {
            "label":          "Config mode",
            "input_type":     "select",
            "select_options": [
                {
                    "value": "basic",
                    "label": "Basic (Not sure what I am doing. Configure most of it for me.)",
                },
                {
                    "value": "standard",
                    "label": "Standard (I know how to transcode some video. Let me tweak some settings.)",
                },
                {
                    "value": "advanced",
                    "label": "Advanced (Dont tell me what to do, I write FFmpeg commands in my sleep.)",
                },
            ],
        }

    def get_max_muxing_queue_size_form_settings(self):
        values = {
            "label":          "Max input stream packet buffer",
            "input_type":     "slider",
            "slider_options": {
                "min": 1024,
                "max": 10240,
            },
        }
        if self.settings.get_setting('mode') not in ['standard']:
            values["display"] = 'hidden'
        return values

    def get_video_codec_form_settings(self):
        values = {
            "label":       "Video Codec",
            "description": "Specify the name of the video codec that your video library should be. Eg. 'h264', 'hevc'.",
        }
        if self.settings.get_setting('mode') not in ['advanced']:
            values = {
                "label":          "Video Codec",
                "description":    "Select the video codec that your video library should be.",
                "input_type":     "select",
                "select_options": [],
            }
            for key in supported_codecs:
                values['select_options'].append(
                    {
                        "value": key,
                        "label": supported_codecs.get(key, {}).get('label'),
                    }
                )
            self.__set_default_option(values['select_options'], 'video_codec')
        if self.settings.get_setting('mode') not in ['basic', 'standard', 'advanced']:
            values["display"] = 'hidden'
        return values

    def get_force_transcode_form_settings(self):
        values = {
            "label":       "Force transcoding even if the file is already using the desired video codec",
            "description": "Will force a transcode of the video stream even if it matches the selected video codec.\n"
                           "A file will only be forced to be transcoded once.\n"
                           "After that it is flagged to prevent it being added to the pending tasks list in a loop.\n"
                           "Note: A file previously flagged to be ignored by this will still be transcoded to apply \n"
                           "a matching smart filter specified below.",
            "sub_setting": True,
        }
        if self.settings.get_setting('mode') not in ['basic', 'standard', 'advanced']:
            values["display"] = 'hidden'
        return values

    def get_video_encoder_form_settings(self):
        values = {
            "label":          "Video Encoder",
            "input_type":     "select",
            "select_options": [],
        }
        encoder_libs = tools.available_encoders(settings=self.settings)
        for encoder_name, encoder_lib in encoder_libs.items():
            encoder_details = encoder_lib.encoder_details(encoder_name)
            if encoder_details.get('codec') != self.settings.get_setting('video_codec'):
                continue
            values['select_options'].append(
                {
                    "value": encoder_name,
                    "label": encoder_details.get('label'),
                }
            )
        self.__set_default_option(values['select_options'], 'video_encoder')
        if self.settings.get_setting('mode') not in ['basic', 'standard']:
            values["display"] = 'hidden'
        return values

    def get_main_options_form_settings(self):
        values = {
            "label":      "Write your own custom main options",
            "input_type": "textarea",
        }
        if self.settings.get_setting('mode') not in ['advanced']:
            values["display"] = 'hidden'
        return values

    def get_advanced_options_form_settings(self):
        values = {
            "label":      "Write your own custom advanced options",
            "input_type": "textarea",
        }
        if self.settings.get_setting('mode') not in ['advanced']:
            values["display"] = 'hidden'
        return values

    def get_custom_options_form_settings(self):
        values = {
            "label":      "Write your own custom video options (starting with the encoder to use)",
            "input_type": "textarea",
        }
        if self.settings.get_setting('mode') not in ['advanced']:
            values["display"] = 'hidden'
        return values

    def get_keep_container_form_settings(self):
        return {
            "label": "Keep the same container",
        }

    def get_dest_container_form_settings(self):
        values = {
            "label":          "Set the output container",
            "sub_setting":    True,
            "input_type":     "select",
            "select_options": [
                {
                    "value": "mkv",
                    "label": ".mkv - Matroska",
                },
                {
                    "value": "mp4",
                    "label": ".mp4 - MP4 (MPEG-4 Part 14)",
                },
            ],
        }
        if self.settings.get_setting('keep_container'):
            values["display"] = 'hidden'
        return values

    def get_apply_smart_filters_form_settings(self):
        values = {
            "label":   "Enable plugin's smart video filters",
            "tooltip": "Provides some pre-configured FFmpeg filtergraphs",
        }
        if self.settings.get_setting('mode') not in ['basic', 'standard']:
            values["display"] = 'hidden'
        return values

    def get_autocrop_black_bars_form_settings(self):
        values = {
            "label":       "Autocrop black bars",
            "description": "Runs FFmpeg 'cropdetect' on the file to auto-detect the crop size.\n"
                           "This detected crop size is then applied during video transcode as a 'crop' filter.",
            "sub_setting": True,
            "req_lev":     2,
        }
        if not self.settings.get_setting('apply_smart_filters'):
            values["display"] = 'hidden'
        if self.settings.get_setting('mode') not in ['basic', 'standard']:
            values["display"] = 'hidden'
        return values

    def get_target_resolution_form_settings(self):
        def generate_label_resolution(key):
            return "{} - {}x{}".format(tools.resolution_map.get(key, {}).get("label"),
                                       tools.resolution_map.get(key, {}).get("width"),
                                       tools.resolution_map.get(key, {}).get("height"))

        values = {
            "label":          "Scale down resolution",
            "description":    "Uses FFprobe to determine resolution.\n"
                              "If the resolution does not match what is configured,\n"
                              "a scale filter will be applied during video transcode.\n"
                              "If resolution is already lower that this set value, no scale will be applied.",
            "sub_setting":    True,
            "input_type":     "select",
            "select_options": [
                {
                    "value": "source",
                    "label": "Same as source",
                },
                {
                    "value": "480p_sdtv",
                    "label": generate_label_resolution("480p_sdtv"),
                },
                {
                    "value": "576p_sdtv",
                    "label": generate_label_resolution("576p_sdtv"),
                },
                {
                    "value": "720p_hdtv",
                    "label": generate_label_resolution("720p_hdtv"),
                },
                {
                    "value": "1080p_hdtv",
                    "label": generate_label_resolution("1080p_hdtv"),
                },
                {
                    "value": "dci_2k_hdtv",
                    "label": generate_label_resolution("dci_2k_hdtv"),
                },
                {
                    "value": "1440p",
                    "label": generate_label_resolution("1440p"),
                },
                {
                    "value": "4k_uhd",
                    "label": generate_label_resolution("4k_uhd"),
                },
                {
                    "value": "dci_4k",
                    "label": generate_label_resolution("dci_4k"),
                },
                {
                    "value": "8k_uhd",
                    "label": generate_label_resolution("8k_uhd"),
                },
            ],
        }
        if not self.settings.get_setting('apply_smart_filters'):
            values["display"] = 'hidden'
        if self.settings.get_setting('mode') not in ['basic', 'standard']:
            values["display"] = 'hidden'
        return values

    def get_strip_data_streams_form_settings(self):
        values = {
            "label":       "Strip data streams",
            "description": "Remove any data streams.\n"
                           "These streams could contain an EPG or metadata.\n"
                           "Certain subtitle formats are stored as data streams in some containers.\n"
                           "Data streams are not supported by all containers.",
            "sub_setting": True,
            "req_lev":     2,
        }
        if not self.settings.get_setting('apply_smart_filters'):
            values["display"] = 'hidden'
        if self.settings.get_setting('mode') not in ['basic', 'standard']:
            values["display"] = 'hidden'
        return values

    def get_strip_attachment_streams_form_settings(self):
        values = {
            "label":       "Strip attachment streams",
            "description": "Remove any attachment streams.\n"
                           "These streams could contain fonts used in rendering subtitles.\n"
                           "Attachment streams are not supported by all containers.",
            "sub_setting": True,
            "req_lev":     2,
        }
        if not self.settings.get_setting('apply_smart_filters'):
            values["display"] = 'hidden'
        if self.settings.get_setting('mode') not in ['basic', 'standard']:
            values["display"] = 'hidden'
        return values

    def get_apply_custom_filters_form_settings(self):
        values = {
            "label":   "Enable custom video filters",
            "tooltip": "Provides text input for adding custom FFmpeg filtergraphs",
        }
        if self.settings.get_setting('mode') not in ['standard']:
            values["display"] = 'hidden'
        return values

    def get_enable_smart_output_target_form_settings(self):
        values = {
            "label":       "Enable smart output target",
            "description": "Automatically detects the best FFmpeg encoder params to use based on the source file.",
            "req_lev":     2,
        }
        if self.settings.get_setting('mode') not in ['basic']:
            values["display"] = 'hidden'
        return values

    def get_smart_output_target_form_settings(self):
        description = "Select the goal that best matches how you want Basic mode to balance quality and compression."
        if self.settings.get_setting('apply_smart_filters') and \
                self.settings.get_setting('target_resolution') not in ['source', None]:
            description += (
                "\n\nWarning: \"Prefer Quality\" is not recommended when scaling down the resolution of a video."
            )
        values = {
            "label":          "Smart output target",
            "description":    description,
            "sub_setting":    True,
            "req_lev":        2,
            "input_type":     "select",
            "select_options": [
                {
                    "value": "prefer_quality",
                    "label": "Prefer Quality",
                },
                {
                    "value": "balanced",
                    "label": "Balanced",
                },
                {
                    "value": "prefer_compression",
                    "label": "Prefer Compression",
                },
            ],
        }
        self.__set_default_option(values['select_options'], 'smart_output_target', default_option='balanced')
        if not self.settings.get_setting('enable_smart_output_target'):
            values["display"] = 'hidden'
        if self.settings.get_setting('mode') not in ['basic']:
            values["display"] = 'hidden'
        return values

    def get_custom_software_filters_form_settings(self):
        values = {
            "label":       "Custom video filters",
            "description": "Video filters and filter chains - https://trac.ffmpeg.org/wiki/FilteringGuide.\n"
                           "Note that any hardware accelerated filters may need to implement the appropriate hwupload filter.",
            "tooltip":     "Separate each filter chain by a linebreak",
            "sub_setting": True,
            "input_type":  "textarea",
        }
        if not self.settings.get_setting('apply_custom_filters'):
            values["display"] = 'hidden'
        if self.settings.get_setting('mode') not in ['standard']:
            values["display"] = 'hidden'
        return values
