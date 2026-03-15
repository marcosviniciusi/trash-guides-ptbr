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


class LibsvtAv1Encoder(Encoder):
    def __init__(self, settings=None, probe=None):
        super().__init__(settings=settings, probe=probe)

    def provides(self):
        return {
            "libsvtav1": {
                "codec": "av1",
                "label": "CPU - libsvtav1",
            }
        }

    def options(self):
        return {
            "preset":                     "4",
            "encoder_ratecontrol_method": "CRF",
            "constant_quality_scale":     "23",
            "video_pix_fmt":              "auto",
            "tune_stvav1":                1,
            "overlays":                   0,
            "variance_boost":             0,
            "enable_qm":                  False,
            "qm_min":                     "8",
            "encoder_additional_params":  "no_additional_params",
            "additional_params":          "",
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

        # Check software format to use
        target_fmt = self._target_pix_fmt_for_encoder(encoder_name)

        # Handle HDR (only for HEVC)
        target_color_config = self._target_color_config_for_encoder(encoder_name)

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

    def stream_args(self, stream_id, filter_state=None):
        stream_encoding = []

        # Use defaults for basic mode
        if self.settings.get_setting('mode') in ['basic']:
            defaults = self.options()
            stream_encoding += [
                '-preset', str(defaults.get('preset')),
            ]
            # TODO: Calculate best crf based on source bitrate
            default_crf = defaults.get('constant_quality_scale')
            if self.settings.get_setting('video_encoder') in ['libsvtav1']:
                default_crf = 23
            stream_encoding += ['-crf', str(default_crf)]
            return stream_encoding

        stav1_params = ["enable-stat-report=1"]
        stav1_params += ['tune=' + str(self.settings.get_setting('tune_stvav1'))]

        if self.settings.get_setting('overlays'):
            # Enable overlays
            stav1_params += ['enable-overlays=1']

        if self.settings.get_setting('variance_boost'):
            # Enable variance boost
            stav1_params += ['enable-variance-boost=1']

        if self.settings.get_setting('enable_qm'):
            # Enable quantization matrix
            stav1_params += ['enable-qm=1']
            stav1_params += ['qm-min=' + str(self.settings.get_setting('qm_min'))]

        if self.settings.get_setting('encoder_additional_params') in ['additional_params'] and len(
            self.settings.get_setting('encoder_svtav1_additional_params')):
            # Add additional parameters for SVT-AV1
            stav1_params += self.settings.get_setting('encoder_svtav1_additional_params')

        stream_encoding += ['-svtav1-params', ":".join(stav1_params)]

        # Add the preset
        if self.settings.get_setting('preset'):
            stream_encoding += ['-preset', str(self.settings.get_setting('preset'))]

        if self.settings.get_setting('encoder_ratecontrol_method') in ['CRF']:
            # Set values for constant quantizer scale
            stream_encoding += [
                '-crf', str(self.settings.get_setting('constant_quality_scale')),
            ]

        if self.settings.get_setting('video_pix_fmt') not in ['auto']:
            # Set the pixel format
            stream_encoding += ['-pix_fmt', str(self.settings.get_setting('video_pix_fmt'))]

        return stream_encoding

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
                    "value": "12",
                    "label": "Very fast (12) - Fastest setting, biggest quality drop",
                },
                {
                    "value": "10",
                    "label": "Faster (10) - Close to medium/fast quality, faster performance",
                },
                {
                    "value": "8",
                    "label": "Fast (8)",
                },
                {
                    "value": "6",
                    "label": "Medium (6)",
                },
                {
                    "value": "4",
                    "label": "Slow (4) - Balanced performance and quality",
                },
                {
                    "value": "2",
                    "label": "Slower (2) - Close to 'very slow' quality, faster performance",
                },
                {
                    "value": "1",
                    "label": "Very Slow (1) - Best quality",
                },
            ],
        }
        if self.settings.get_setting('mode') not in ['standard']:
            values["display"] = "hidden"
        return values

    def get_encoder_ratecontrol_method_form_settings(self):
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
        if self.settings.get_setting('video_encoder') in ['libsvtav1']:
            values["description"] = "Default value for libsvtav1 = 23"
        return values

    def get_video_pix_fmt_form_settings(self):
        values = {
            "label":          "Pixel Format",
            "description":    "Select the pixel format",
            "sub_setting":    True,
            "input_type":     "select",
            "select_options": [
                {
                    "value": "auto",
                    "label": "Let ffmpeg decide (default)"
                },
                {
                    "value": "yuv420p",
                    "label": "yuv420p (8-bit, 4:2:0)"
                },
                {
                    "value": "yuv420p10le",
                    "label": "yuv420p10le (10-bit, 4:2:0)"
                },
            ],
        }
        if self.settings.get_setting('mode') not in ['standard']:
            values["display"] = "hidden"
        return values

    def get_tune_stvav1_form_settings(self):
        values = {
            "label":          "SVT-AV1: Tune",
            "description":    "VQ (Visual Quality), PSNR (Objective Quality), SSIM (Objective Quality).",
            "sub_setting":    True,
            "input_type":     "select",
            "select_options": [
                {
                    "value": 0,
                    "label": "VQ (Recommended for animes, cartoons, and other animated content)",
                },
                {
                    "value": 1,
                    "label": "PSNR (default)",
                },
                {
                    "value": 2,
                    "label": "SSIM (Recommended for movies, TV shows, and other live-action content)",
                },
            ]
        }
        if self.settings.get_setting('mode') not in ['standard']:
            values["display"] = "hidden"
        return values

    def get_overlays_form_settings(self):
        values = {
            "label":          "SVT-AV1: Enable Overlays",
            "sub_setting":    True,
            "input_type":     "select",
            "select_options": [
                {
                    "value": 0,
                    "label": "No (Default)",
                },
                {
                    "value": 1,
                    "label": "Yes"
                },
            ]
        }
        if self.settings.get_setting('mode') not in ['standard']:
            values["display"] = "hidden"
        return values

    def get_variance_boost_form_settings(self):
        values = {
            "label":          "SVT-AV1: Enable Variance Boost (enable-variance-boost)",
            "sub_setting":    True,
            "input_type":     "select",
            "select_options": [
                {
                    "value": 0,
                    "label": "No (Default)"
                },
                {
                    "value": 1,
                    "label": "Yes"
                },
            ]
        }
        if self.settings.get_setting('mode') not in ['standard']:
            values["display"] = "hidden"
        return values

    def get_enable_qm_form_settings(self):
        values = {
            "label":          "SVT-AV1: Enable Quantization Matrix (enable-qm)",
            "description":    "",
            "sub_setting":    True,
            "input_type":     "select",
            "select_options": [
                {
                    "value": False,
                    "label": "No (Default)"
                },
                {
                    "value": True,
                    "label": "Yes"
                },
            ]
        }
        self.__set_default_option(values['select_options'], 'enable_qm', default_option=False)
        if self.settings.get_setting('mode') not in ['standard']:
            values["display"] = "hidden"
        return values

    def get_qm_min_form_settings(self):
        values = {
            "label":          "SVT-AV1: Quantization Matrix Min (qm-min)",
            "description":    "Specifies qm-min level (Default: 8).",
            "sub_setting":    True,
            "input_type":     "slider",
            "slider_options": {
                "min": 0,
                "max": 14,
            },
        }
        if self.settings.get_setting('mode') not in ['standard']:
            values["display"] = "hidden"
        if (not self.settings.get_setting('enable_qm')):
            values["display"] = "hidden"

        return values

    def get_encoder_additional_params_form_settings(self):
        values = {
            "label":          "SVT-AV1: Additional Parameters",
            "sub_setting":    True,
            "input_type":     "select",
            "select_options": [
                {
                    "value": "additional_params",
                    "label": "SVT-AV1: Additional Parameters",
                },
                {
                    "value": "no_additional_params",
                    "label": "No Additional Parameters",
                },
            ]
        }
        self.__set_default_option(values['select_options'], 'encoder_additional_params', default_option='no_additional_params')
        if self.settings.get_setting('mode') not in ['standard']:
            values["display"] = "hidden"
        return values

    def get_additional_params_form_settings(self):
        values = {
            "label":       "SVT-AV1: Additional Parameters field",
            "description": "Additional SVT-AV1 parameters as a colon-separated string (e.g., enable-cdef=1:enable-restoration=1).",
            "sub_setting": True,
            "input_type":  "textarea",
        }
        if self.settings.get_setting('mode') not in ['standard']:
            values["display"] = "hidden"
        if self.settings.get_setting('encoder_additional_params') not in ['additional_params']:
            values["display"] = "hidden"

        return values
