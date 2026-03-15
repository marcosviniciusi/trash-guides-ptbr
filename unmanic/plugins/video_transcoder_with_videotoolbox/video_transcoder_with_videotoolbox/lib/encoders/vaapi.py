#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    plugins.vaapi.py

    Written by:               Josh.5 <jsunnex@gmail.com>
    Date:                     08 Jun 2022, (8:15 AM)

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

from video_transcoder.lib.encoders.base import Encoder


def list_available_vaapi_devices():
    """
    Return a list of available VAAPI decoder devices
    :return:
    """
    decoders = []
    dir_path = os.path.join("/", "dev", "dri")

    if os.path.exists(dir_path):
        for device in sorted(os.listdir(dir_path)):
            if device.startswith('render'):
                device_data = {
                    'hwaccel':             'vaapi',
                    'hwaccel_device':      device,
                    'hwaccel_device_path': os.path.join("/", "dev", "dri", device),
                }
                decoders.append(device_data)

    # Return the list of decoders
    return decoders


class VaapiEncoder(Encoder):
    def __init__(self, settings=None, probe=None):
        super().__init__(settings=settings, probe=probe)

    def _map_pix_fmt(self, is_h264: bool, is_10bit: bool) -> str:
        if is_10bit and not is_h264:
            return "p010le"
        else:
            return "nv12"

    def _map_color_config_for_encoder(self, encoder_name: str, color_tags: dict):
        """
        This method must be implemented by a child class to provide the
        specific HDR configuration for a given encoder.

        Returns a dict containing:
            "requires_p010": bool,
            "encoder_args": dict,
            "bitstream_filter": str|None,
            "notes": str
        """
        result = {}
        if encoder_name in ["hevc_vaapi"]:
            encoder_args = {"-profile:v": "main10"}

    def provides(self):
        return {
            "h264_vaapi": {
                "codec": "h264",
                "label": "VAAPI - h264_vaapi",
            },
            "hevc_vaapi": {
                "codec": "hevc",
                "label": "VAAPI - hevc_vaapi",
            },
        }

    def options(self):
        return {
            "vaapi_device":                     "none",
            "vaapi_decoding_method":            "cpu",
            "vaapi_encoder_ratecontrol_method": "ICQ",
            "vaapi_constant_quantizer_scale":   "25",
            "vaapi_constant_quality_scale":     "23",
            "vaapi_average_bitrate":            "5",
        }

    def generate_default_args(self):
        """
        Generate a list of args for using a VAAPI decoder

        :return:
        """
        # Set the hardware device
        hardware_devices = list_available_vaapi_devices()
        if not hardware_devices:
            # Return no options. No hardware device was found
            raise Exception("No VAAPI device found")

        hardware_device = None
        # If we have configured a hardware device
        if self.settings.get_setting('vaapi_device') not in ['none']:
            # Attempt to match to that configured hardware device
            for hw_device in hardware_devices:
                if self.settings.get_setting('vaapi_device') == hw_device.get('hwaccel_device'):
                    hardware_device = hw_device
                    break
        # If no matching hardware device is set, then select the first one
        if not hardware_device:
            hardware_device = hardware_devices[0]

        # Check if we are using a VAAPI decoder also...
        if self.settings.get_setting('vaapi_decoding_method') in ['vaapi']:
            # Set a named global device that can be used with various params
            dev_id = 'vaapi0'
            # Configure args such that when the input may or may not be able to be decoded with hardware we can do:
            #   REF: https://trac.ffmpeg.org/wiki/Hardware/VAAPI#Encoding
            generic_kwargs = {
                "-init_hw_device":        "vaapi={}:{}".format(dev_id, hardware_device.get('hwaccel_device_path')),
                "-hwaccel":               "vaapi",
                "-hwaccel_output_format": "vaapi",
                "-hwaccel_device":        dev_id,
                "-filter_hw_device":      dev_id,
            }
            advanced_kwargs = {}
        else:
            # Encode only (no decoding)
            #   REF: https://trac.ffmpeg.org/wiki/Hardware/VAAPI#Encode-only (sorta)
            generic_kwargs = {
                "-vaapi_device": hardware_device.get('hwaccel_device_path'),
            }
            advanced_kwargs = {}

        return generic_kwargs, advanced_kwargs

    def generate_filtergraphs(self, current_filter_args, smart_filters, encoder_name):
        """
        Generate the required filter for enabling VAAPI HW acceleration

        :return:
        """
        generic_kwargs = {}
        advanced_kwargs = {}
        start_filter_args = []
        end_filter_args = []

        # Loop over any HW smart filters to be applied and add them as required.
        hw_smart_filters = []
        remaining_smart_filters = []
        for sf in smart_filters:
            if sf.get("scale"):
                w = sf["scale"]["values"]["width"]
                hw_smart_filters.append(f"scale_vaapi=w={w}:h=-1")
            else:
                remaining_smart_filters.append(sf)

        # Check if we are decoding with VAAPI
        hw_decode = self.settings.get_setting('vaapi_decoding_method') in ['vaapi']
        # Check software format to use
        target_fmt = self._target_pix_fmt_for_encoder(encoder_name)

        # Handle HDR
        enc_supports_hdr = (encoder_name in ["hevc_vaapi"])
        target_color_config = self._target_color_config_for_encoder(encoder_name)

        # If we have SW filters:
        if remaining_smart_filters or current_filter_args:
            # If we have SW filters and HW decode is enabled, make decoder produce SW frames
            if hw_decode:
                # Force decoder to deliver SW frames
                generic_kwargs['-hwaccel_output_format'] = target_fmt

            # Add filter to upload software frames to VAAPI for VAAPI filters
            # Note, format conversion (if any - eg yuv422p10le -> p010le) happens after the software filters.
            # If a user applies a custom software filter that does not support the pix_fmt, then will need to prefix it with 'format=p010le'
            # Set format and setparams at start of filter
            start_chain = [f"format={target_fmt}"]
            if enc_supports_hdr and target_color_config.get('apply_color_params'):
                start_chain.append(target_color_config['setparams_filter'])
            start_filter_args.append(",".join(start_chain))
            # Upload to hw frames at the end of the filter
            end_chain = start_chain + ["hwupload"]
            end_filter_args.append(",".join(end_chain))
        # If we have no software filters:
        else:
            # Check if we are software decoding
            if not hw_decode:
                # Set format and setparams at start of filter
                start_chain = [f"format={target_fmt}"]
                if enc_supports_hdr and target_color_config.get('apply_color_params'):
                    start_chain.append(target_color_config['setparams_filter'])
                start_filter_args.append(",".join(start_chain))
                # Upload to hw frames at the end of the filter
                end_chain = start_chain + ["hwupload"]
                end_filter_args.append(",".join(end_chain))
            else:
                # Add hwupload filter that can handle when the frame was decoded in software or hardware
                chain = [f"format={target_fmt}|vaapi", "hwupload"]
                end_filter_args.append(",".join(chain))

        # Add the smart filters to the end
        end_filter_args += hw_smart_filters

        # Return built args
        return {
            "generic_kwargs":    generic_kwargs,
            "advanced_kwargs":   advanced_kwargs,
            "smart_filters":     remaining_smart_filters,
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
        enc_supports_hdr = (encoder_name in ["hevc_vaapi"])
        target_color_config = self._target_color_config_for_encoder(encoder_name)
        if enc_supports_hdr and target_color_config.get('apply_color_params'):
            # Force Main10 profile
            stream_args += [f'-profile:v:{stream_id}', 'main10']

            # TODO: Fix this for vaapi (seems to work fine for libx265)
            # # Add static HDR SEI for x265 when present
            # hdr_md = self.probe.get_hdr_static_metadata()
            # md_str = hdr_md.get("master_display")
            # cll = hdr_md.get("max_cll")
            # if md_str or cll:
            #     bsf_parts = ["hevc_metadata=sei_user_data=remove"]
            #     if md_str:
            #         bsf_parts += ["sei_mastering_display=insert", f"mastering-display={md_str}"]
            #     if cll:
            #         bsf_parts += ["sei_content_light_level=insert", f"max_cll={cll[0]}:{cll[1]}"]
            #     stream_args += [f'-bsf:v:{stream_id}', ",".join(bsf_parts)]

        # Use defaults for basic mode
        if self.settings.get_setting('mode') == 'basic':
            if enc_supports_hdr and target_color_config.get('apply_color_params'):
                # Add HDR color tags to the encoder output stream
                for k, v in target_color_config.get('stream_color_params', {}).items():
                    stream_args += [k, v]
            # Use the default VAAPI settings - Choose the mode automatically based on driver support
            return {
                "generic_kwargs":  generic_kwargs,
                "advanced_kwargs": advanced_kwargs,
                "encoder_args":    encoder_args,
                "stream_args":     stream_args,
            }

        encoder_args += [
            '-rc_mode', str(self.settings.get_setting('vaapi_encoder_ratecontrol_method')),
        ]
        if self.settings.get_setting('vaapi_encoder_ratecontrol_method') in ['CQP', 'ICQ']:
            if self.settings.get_setting('vaapi_encoder_ratecontrol_method') in ['CQP']:
                encoder_args += [
                    '-global_quality', str(self.settings.get_setting('vaapi_constant_quantizer_scale')),
                ]
            elif self.settings.get_setting('vaapi_encoder_ratecontrol_method') in ['ICQ']:
                encoder_args += [
                    '-global_quality', str(self.settings.get_setting('vaapi_constant_quality_scale')),
                ]
        else:
            # Configure the encoder with a bitrate-based mode
            # Set the max and average bitrate (used by all bitrate-based modes)
            stream_args += [
                '-b:v:{}'.format(stream_id), '{}M'.format(self.settings.get_setting('vaapi_average_bitrate')),
            ]
            if self.settings.get_setting('vaapi_encoder_ratecontrol_method') == 'CBR':
                # Add 'maxrate' with the same value to make CBR mode
                stream_args += [
                    '-maxrate', '{}M'.format(self.settings.get_setting('vaapi_average_bitrate')),
                ]

        # Add stream color args
        if enc_supports_hdr and target_color_config.get('apply_color_params'):
            # Add HDR color tags to the encoder output stream
            for k, v in target_color_config.get('stream_color_params', {}).items():
                stream_args += [k, v]

        # Return built args
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

    def get_vaapi_device_form_settings(self):
        values = {
            "label":          "VAAPI Device",
            "sub_setting":    True,
            "input_type":     "select",
            "select_options": [
                {
                    "value": "none",
                    "label": "No VAAPI devices available",
                }
            ]
        }
        default_option = None
        hardware_devices = list_available_vaapi_devices()
        if hardware_devices:
            values['select_options'] = []
            for hw_device in hardware_devices:
                if not default_option:
                    default_option = hw_device.get('hwaccel_device', 'none')
                values['select_options'].append({
                    "value": hw_device.get('hwaccel_device', 'none'),
                    "label": "VAAPI device '{}'".format(hw_device.get('hwaccel_device_path', 'not found')),
                })
        if not default_option:
            default_option = 'none'

        self.__set_default_option(values['select_options'], 'vaapi_device', default_option=default_option)
        if self.settings.get_setting('mode') not in ['standard']:
            values["display"] = "hidden"
        return values

    def get_vaapi_decoding_method_form_settings(self):
        values = {
            "label":          "Enable HW Accelerated Decoding",
            "description":    "Warning: Ensure your device supports decoding the source video codec or it will fail.\n"
                              "This enables full hardware transcode with VAAPI, using only GPU memory for the entire video transcode.\n"
                              "If filters are configured in the plugin, decoder will output NV12 or P010LE software surfaces to\n"
                              "those filters which will be slightly slower.",
            "sub_setting":    True,
            "input_type":     "select",
            "select_options": [
                {
                    "value": "cpu",
                    "label": "Disabled - Use CPU to decode of video source (provides best compatibility)",
                },
                {
                    "value": "vaapi",
                    "label": "VAAPI - Enable VAAPI decoding",
                }
            ]
        }
        self.__set_default_option(values['select_options'], 'vaapi_decoding_method', 'cpu')
        if self.settings.get_setting('mode') not in ['standard']:
            values["display"] = "hidden"
        return values

    def get_vaapi_encoder_ratecontrol_method_form_settings(self):
        values = {
            "label":          "Encoder ratecontrol method",
            "sub_setting":    True,
            "input_type":     "select",
            "select_options": [
                {
                    "value": "CQP",
                    "label": "CQP - Quality based mode using constant quantizer scale",
                },
                {
                    "value": "ICQ",
                    "label": "ICQ - Quality based mode using intelligent constant quality",
                },
                {
                    "value": "CBR",
                    "label": "CBR - Bitrate based mode using constant bitrate",
                },
                {
                    "value": "VBR",
                    "label": "VBR - Bitrate based mode using variable bitrate",
                },
            ]
        }
        # TODO: Add support for these:
        # {
        #     "value": "QVBR",
        #     "label": "QVBR - Quality defined variable bitrate mode",
        # },
        # {
        #     "value": "AVBR",
        #     "label": "AVBR - Average variable bitrate mode",
        # },
        self.__set_default_option(values['select_options'], 'vaapi_encoder_ratecontrol_method', default_option='CQP')
        if self.settings.get_setting('mode') not in ['standard']:
            values["display"] = "hidden"
        return values

    def get_vaapi_constant_quantizer_scale_form_settings(self):
        # Lower is better
        values = {
            "label":          "Constant quantizer scale",
            "sub_setting":    True,
            "input_type":     "slider",
            "slider_options": {
                "min": 0,
                "max": 51,
            },
        }
        if self.settings.get_setting('mode') not in ['standard']:
            values["display"] = "hidden"
        if self.settings.get_setting('vaapi_encoder_ratecontrol_method') != 'CQP':
            values["display"] = "hidden"
        return values

    def get_vaapi_constant_quality_scale_form_settings(self):
        # Lower is better
        values = {
            "label":          "Constant quality scale",
            "sub_setting":    True,
            "input_type":     "slider",
            "slider_options": {
                "min": 1,
                "max": 51,
            },
        }
        if self.settings.get_setting('mode') not in ['standard']:
            values["display"] = "hidden"
        if self.settings.get_setting('vaapi_encoder_ratecontrol_method') not in ['LA_ICQ', 'ICQ']:
            values["display"] = "hidden"
        return values

    def get_vaapi_average_bitrate_form_settings(self):
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
        if self.settings.get_setting('vaapi_encoder_ratecontrol_method') not in ['VBR', 'LA', 'CBR']:
            values["display"] = "hidden"
        return values
