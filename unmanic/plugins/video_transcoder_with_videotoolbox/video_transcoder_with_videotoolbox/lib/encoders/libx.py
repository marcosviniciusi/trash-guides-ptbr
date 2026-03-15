#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    plugins.libx.py

    Written by:               Josh.5 <jsunnex@gmail.com>
    Date:                     12 Jun 2022, (9:48 AM)

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
from video_transcoder.lib.encoders.base import Encoder


class LibxEncoder(Encoder):
    def __init__(self, settings=None, probe=None):
        super().__init__(settings=settings, probe=probe)

    def provides(self):
        return {
            "libx264": {
                "codec": "h264",
                "label": "CPU - libx264",
            },
            "libx265": {
                "codec": "hevc",
                "label": "CPU - libx265",
            },
        }

    def options(self):
        return {
            "preset":                     "slow",
            "tune":                       "auto",
            "profile":                    "auto",
            "encoder_ratecontrol_method": "CRF",
            "constant_quality_scale":     "23",
            "average_bitrate":            "5",
        }

    def generate_default_args(self):
        """
        Generate a list of args for using a libx decoder

        :return:
        """
        # No default args required
        generic_kwargs = {}
        advanced_kwargs = {}
        return generic_kwargs, advanced_kwargs

    def generate_filtergraphs(self, current_filter_args, smart_filters, encoder_name):
        """
        Generate the required filter for this encoder

        :return:
        """
        generic_kwargs = {}
        advanced_kwargs = {}
        start_filter_args = []
        end_filter_args = []

        is_x265 = (encoder_name == "libx265")

        # Check software format to use
        target_fmt = self._target_pix_fmt_for_encoder(encoder_name)

        # Handle HDR (only for HEVC)
        if is_x265:
            target_color_config = self._target_color_config_for_encoder(encoder_name)
        else:
            target_color_config = {
                "apply_color_params": False
            }

        # If we have existing filters:
        if smart_filters or current_filter_args:
            start_filter_args.append(f'format={target_fmt}')
            if target_color_config.get('apply_color_params'):
                # Apply setparams filter if software filters exist (apply at the start of the filters list) to preserve HDR tags
                end_filter_args.append(target_color_config['setparams_filter'])

        # Return built args
        return {
            "generic_kwargs":    generic_kwargs,
            "advanced_kwargs":   advanced_kwargs,
            "smart_filters":     smart_filters,
            "start_filter_args": start_filter_args,
            "end_filter_args":   end_filter_args,
        }

    def encoder_details(self, encoder):
        provides = self.provides()
        return provides.get(encoder, {})

    def stream_args(self, stream_info, stream_id, encoder_name, filter_state=None):
        generic_kwargs = {}
        advanced_kwargs = {}
        encoder_args = []
        stream_args = []

        # Handle HDR
        enc_supports_hdr = (encoder_name in ["libx265"])
        target_color_config = self._target_color_config_for_encoder(encoder_name)
        if enc_supports_hdr and target_color_config.get('apply_color_params'):
            if self.settings.get_setting('profile') == 'auto':
                # Force Main10 profile
                stream_args += [f'-profile:v:{stream_id}', 'main10']

            # Mirrors the explicit x265 params
            x265_params = ["hdr10=1", "hdr10_opt=1"]
            # Add color tags
            color_tags = target_color_config.get('color_tags', {})
            if color_tags.get('color_primaries'):
                x265_params.append(f"colorprim={color_tags['color_primaries']}")
            if color_tags.get('color_trc'):
                x265_params.append(f"transfer={color_tags['color_trc']}")
            if color_tags.get('colorspace'):
                x265_params.append(f"colormatrix={color_tags['colorspace']}")

            # Add static HDR SEI for x265 when present
            hdr_md = self.probe.get_hdr_static_metadata()
            md_str = hdr_md.get("master_display")
            cll = hdr_md.get("max_cll")
            if md_str:
                x265_params.append(f"master-display={md_str}")
            if cll:
                x265_params.append(f"max-cll={cll[0]},{cll[1]}")

            # Add encoder args
            encoder_args = encoder_args + ["-x265-params"] + [":".join(x265_params)]

            # Add HDR color tags to the encoder output stream
            for k, v in target_color_config.get('stream_color_params', {}).items():
                stream_args += [k, v]

        # Use defaults for basic mode
        if self.settings.get_setting('mode') in ['basic']:
            defaults = self.options()
            stream_args += [
                '-preset', str(defaults.get('preset')),
            ]
            # TODO: Calculate best crf based on source bitrate
            default_crf = defaults.get('constant_quality_scale')
            if self.settings.get_setting('video_encoder') in ['libx265']:
                default_crf = 28
            elif self.settings.get_setting('video_encoder') in ['libx264']:
                default_crf = 23
            stream_args += ['-crf', str(default_crf)]
            return {
                "generic_kwargs":  generic_kwargs,
                "advanced_kwargs": advanced_kwargs,
                "encoder_args":    encoder_args,
                "stream_args":     stream_args,
            }

        # Add the configured encoder args
        if self.settings.get_setting('preset'):
            encoder_args += ['-preset', str(self.settings.get_setting('preset'))]
        if self.settings.get_setting('tune') and self.settings.get_setting('tune') not in ('auto', 'disabled'):
            encoder_args += ['-tune', str(self.settings.get_setting('tune'))]
        if self.settings.get_setting('encoder_ratecontrol_method') in ['CRF']:
            # Set values for constant quantizer scale
            encoder_args += [
                '-crf', str(self.settings.get_setting('constant_quality_scale')),
            ]

        # Add configured stream args
        if self.settings.get_setting('profile') and self.settings.get_setting('profile') not in ('auto', 'disabled'):
            stream_args += ['-profile:v:{}'.format(stream_id), str(self.settings.get_setting('profile'))]

        return {
            "generic_kwargs":  generic_kwargs,
            "advanced_kwargs": advanced_kwargs,
            "encoder_args":    encoder_args,
            "stream_args":     stream_args,
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
            available_options.append(option.get('value'))
            if not default_option:
                default_option = option.get('value')
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

    def get_preset_form_settings(self):
        values = {
            "label":          "Encoder quality preset",
            "sub_setting":    True,
            "input_type":     "select",
            "select_options": [
                {
                    "value": "veryfast",
                    "label": "Very fast - Fastest setting, biggest quality drop",
                },
                {
                    "value": "faster",
                    "label": "Faster - Close to medium/fast quality, faster performance",
                },
                {
                    "value": "fast",
                    "label": "Fast",
                },
                {
                    "value": "medium",
                    "label": "Medium - Balanced performance and quality",
                },
                {
                    "value": "slow",
                    "label": "Slow",
                },
                {
                    "value": "slower",
                    "label": "Slower - Close to 'very slow' quality, faster performance",
                },
                {
                    "value": "veryslow",
                    "label": "Very Slow - Best quality",
                },
            ],
        }
        if self.settings.get_setting('mode') not in ['standard']:
            values["display"] = "hidden"
        return values

    def get_tune_form_settings(self):
        values = {
            "label":          "Tune for a particular type of source or situation",
            "sub_setting":    True,
            "input_type":     "select",
            "select_options": [],
        }
        common_select_options = [
            {
                "value": "auto",
                "label": "Disabled – Do not apply any tune",
            },
            {
                "value": "animation",
                "label": "Animation – good for cartoons; uses higher deblocking and more reference frames",
            },
            {
                "value": "grain",
                "label": "Grain – preserves the grain structure in old, grainy film material",
            },
            {
                "value": "fastdecode",
                "label": "Fast decode – allows faster decoding by disabling certain filters",
            },
            {
                "value": "zerolatency",
                "label": "Zero latency – good for fast encoding and low-latency streaming",
            },
        ]
        if self.settings.get_setting('video_encoder') in ['libx264']:
            values["select_options"] = common_select_options + [
                {
                    "value": "film",
                    "label": "Film – use for high quality movie content; lowers deblocking",
                },
                {
                    "value": "stillimage",
                    "label": "Still image – good for slideshow-like content",
                },
            ]
        elif self.settings.get_setting('video_encoder') in ['libx265']:
            values["select_options"] = common_select_options
        self.__set_default_option(values['select_options'], 'tune')
        if self.settings.get_setting('mode') not in ['standard']:
            values["display"] = "hidden"
        return values

    def get_profile_form_settings(self):
        values = {
            "label":          "Profile for a particular type of source or situation",
            "sub_setting":    True,
            "input_type":     "select",
            "select_options": [],
        }
        if self.settings.get_setting('video_encoder') in ['libx264']:
            values["select_options"] = [
                {
                    "value": "auto",
                    "label": "Auto – Let ffmpeg automatically select the required profile (recommended)",
                },
                {
                    "value": "baseline",
                    "label": "Baseline",
                },
                {
                    "value": "main",
                    "label": "Main",
                },
                {
                    "value": "high",
                    "label": "High",
                },
                {
                    "value": "high10",
                    "label": "High10",
                },
                {
                    "value": "high422",
                    "label": "High422",
                },
                {
                    "value": "high444",
                    "label": "High444",
                },
            ]
        elif self.settings.get_setting('video_encoder') in ['libx265']:
            values["select_options"] = [
                {
                    "value": "auto",
                    "label": "Auto – Let ffmpeg automatically select the required profile (recommended)",
                },
                {
                    "value": "main",
                    "label": "Main",
                },
                {
                    "value": "main-intra",
                    "label": "Main-intra",
                },
                {
                    "value": "mainstillpicture",
                    "label": "Mainstillpicture",
                },
                {
                    "value": "main444-8",
                    "label": "Main444-8",
                },
                {
                    "value": "main444-intra",
                    "label": "Main444-intra",
                },
                {
                    "value": "main444-stillpicture",
                    "label": "Main444-stillpicture",
                },
                {
                    "value": "main10",
                    "label": "Main10",
                },
                {
                    "value": "main10-intra",
                    "label": "Main10-intra",
                },
                {
                    "value": "main422-10",
                    "label": "Main422-10",
                },
                {
                    "value": "main422-10-intra",
                    "label": "Main422-10-intra",
                },
                {
                    "value": "main444-10",
                    "label": "Main444-10",
                },
                {
                    "value": "main444-10-intra",
                    "label": "Main444-10-intra",
                },
                {
                    "value": "main12",
                    "label": "Main12",
                },
                {
                    "value": "main12-intra",
                    "label": "Main12-intra",
                },
                {
                    "value": "main422-12",
                    "label": "Main422-12",
                },
                {
                    "value": "main422-12-intra",
                    "label": "Main422-12-intra",
                },
                {
                    "value": "main444-12",
                    "label": "Main444-12",
                },
                {
                    "value": "main444-12-intra",
                    "label": "Main444-12-intra",
                },
            ]
        # TODO: Enable profile options (currently causing issues)
        values["select_options"] = [
            {
                "value": "auto",
                "label": "Auto – Let ffmpeg automatically select the required profile (recommended)",
            },
        ]
        self.__set_default_option(values['select_options'], 'profile')
        if self.settings.get_setting('mode') not in ['standard']:
            values["display"] = "hidden"
        return values

    def get_encoder_ratecontrol_method_form_settings(self):
        # TODO: Add Two-Pass
        values = {
            "label":          "Encoder ratecontrol method",
            "sub_setting":    True,
            "input_type":     "select",
            "select_options": [
                {
                    "value": "CRF",
                    "label": "CRF - Constant Rate Factor",
                },
            ]
        }
        self.__set_default_option(values['select_options'], 'encoder_ratecontrol_method', default_option='CRF')
        if self.settings.get_setting('mode') not in ['standard']:
            values["display"] = "hidden"
        return values

    def get_constant_quality_scale_form_settings(self):
        # Lower is better
        values = {
            "label":          "Constant rate factor",
            "description":    "",
            "sub_setting":    True,
            "input_type":     "slider",
            "slider_options": {
                "min": 1,
                "max": 51,
            },
        }
        if self.settings.get_setting('mode') not in ['standard']:
            values["display"] = "hidden"
        if self.settings.get_setting('encoder_ratecontrol_method') not in ['CRF']:
            values["display"] = "hidden"
        if self.settings.get_setting('video_encoder') in ['libx264']:
            values["description"] = "Default value for libx264 = 23"
        elif self.settings.get_setting('video_encoder') in ['libx265']:
            values["description"] = "Default value for libx265 = 28 (equivalent to 23 in libx264)"
        return values

    def get_average_bitrate_form_settings(self):
        values = {
            "label":          "Bitrate",
            "sub_setting":    True,
            "input_type":     "slider",
            "slider_options": {
                "min":    1,
                "max":    20,
                "suffix": "M"
            },
        }
        if self.settings.get_setting('mode') not in ['standard']:
            values["display"] = "hidden"
        if self.settings.get_setting('encoder_ratecontrol_method') not in ['VBR', 'LA', 'CBR']:
            values["display"] = "hidden"
        return values
