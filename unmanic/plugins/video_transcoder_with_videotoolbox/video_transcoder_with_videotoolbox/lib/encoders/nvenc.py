#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    plugins.nvenc.py

    Written by:               Josh.5 <jsunnex@gmail.com>
    Date:                     27 Dec 2023, (11:21 AM)

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
Notes:
    - Listing available encoder options:
        ffmpeg -h encoder=h264_nvenc
        ffmpeg -h encoder=hevc_nvenc
"""
import re
import logging
import subprocess
from functools import lru_cache
from video_transcoder.lib.smart_output_target import SmartOutputTargetHelper
from video_transcoder.lib.encoders.base import Encoder


logger = logging.getLogger("Unmanic.Plugin.video_transcoder")


@lru_cache(maxsize=1)
def list_available_cuda_devices():
    """
    Return a list of available CUDA devices via nvidia-smi.
    """
    gpu_dicts = []
    try:
        # Run the nvidia-smi command
        result = subprocess.check_output(['nvidia-smi', '-L'], encoding='utf-8', timeout=2)
        if not result:
            raise ValueError("Failed to fetch available cuda devices")
        # Use regular expression to find device IDs, names, and UUIDs
        gpu_info = re.findall(r'GPU (\d+): (.+) \(UUID: (.+)\)', result)
        # Populate the list of dictionaries for each GPU
        for gpu_id, gpu_name, gpu_uuid in gpu_info:
            gpu_dicts.append({
                'hwaccel_device':      gpu_id,
                'hwaccel_device_name': f"{gpu_name} (UUID: {gpu_uuid})",
            })
    except (FileNotFoundError, subprocess.CalledProcessError, subprocess.TimeoutExpired):
        # nvidia-smi executable not found or command failed
        raise ValueError("Failed to fetch available cuda devices")
    except ValueError:
        raise

    return gpu_dicts


@lru_cache(maxsize=1)
def _max_compute_capability():
    """
    Try to read the highest compute capability reported by nvidia-smi.
    """
    queries = [
        ['nvidia-smi', '--query-gpu=compute_cap', '--format=csv,noheader'],
        ['nvidia-smi', '--query-gpu=compute_capability', '--format=csv,noheader'],
    ]
    for cmd in queries:
        try:
            result = subprocess.check_output(cmd, encoding='utf-8', timeout=2)
        except (FileNotFoundError, subprocess.CalledProcessError, subprocess.TimeoutExpired):
            continue
        if not result:
            continue
        caps = []
        for line in result.splitlines():
            cap_str = line.strip()
            if not cap_str:
                continue
            try:
                caps.append(float(cap_str))
            except ValueError:
                continue
        if caps:
            return max(caps)
    raise ValueError("Failed to fetch compute capability via nvidia-smi")


def is_pascal_or_newer():
    """
    Detect whether the available GPU(s) meet Pascal (6.x) compute capability or newer.
    Returns:
        True if Pascal+, False if definitively older, None if unknown.
    """
    try:
        max_capability = _max_compute_capability()
    except ValueError:
        return None
    if max_capability is None:
        return None
    return max_capability >= 6.0


def is_turing_or_newer():
    """
    Detect whether the available GPU(s) meet Turing (7.5) compute capability or newer.
    Returns:
        True if Turing+, False if definitively older, None if unknown.
    """
    try:
        max_capability = _max_compute_capability()
    except ValueError:
        return None
    if max_capability is None:
        return None
    return max_capability >= 7.5


@lru_cache(maxsize=None)
def _supports_temporal_aq(encoder_name, hw_device):
    """
    Detect whether NVENC temporal AQ is supported by the configured GPU/driver for a specific encoder.
    Returns:
        True if supported, False if definitively unsupported, None if unknown.
    """
    if not encoder_name:
        return None
    # Normalize cache key inputs (lru_cache uses args).
    device_idx = None if hw_device in (None, 'none') else str(hw_device)
    cmd = [
        'ffmpeg',
        '-v', 'info',
        '-nostdin',
        '-f', 'lavfi',
        '-i', 'testsrc=size=320x240:rate=1:duration=1',
        '-frames:v', '1',
        '-c:v', str(encoder_name),
    ]
    if device_idx is not None:
        cmd += ['-gpu', device_idx]
    cmd += ['-temporal-aq', '1', '-f', 'null', '-']

    try:
        subprocess.check_output(cmd, stderr=subprocess.STDOUT, timeout=4)
        return True
    except FileNotFoundError:
        logger.info("ffmpeg not found while probing NVENC temporal AQ support.")
        return None
    except subprocess.TimeoutExpired:
        logger.info("Timed out while probing NVENC temporal AQ support.")
        return None
    except subprocess.CalledProcessError as exc:
        output = exc.output or ""
        if isinstance(output, bytes):
            output = output.decode(errors='ignore')
        output_lower = output.lower()
        failure_markers = (
            "does not support temporal",
            "temporal aq not supported",
            "temporal aq: not supported",
            "temporal aq not supported for this encoder",
            "invalid param",
            "unsupported parameter",
            "unrecognized option 'temporal-aq'",
        )
        if any(marker in output_lower for marker in failure_markers):
            return False
        if "no nvenc capable devices" in output_lower or "no capable devices found" in output_lower:
            return None
        logger.info(
            "NVENC temporal AQ probe failed; treating as unsupported. Output: %s",
            output.strip(),
        )
        return False


def get_configured_device_info(settings):
    """
    Returns the currently configured device
    Checks to ensure that the configured device exists and otherwise will return the first device available
    :param settings:
    :return:
    """
    hardware_device = None
    # Set the hardware device
    try:
        hardware_devices = list_available_cuda_devices()
    except ValueError:
        hardware_devices = []
    if not hardware_devices:
        # Return no options. No hardware device was found
        raise Exception("No NVIDIA device found")
    # If we have configured a hardware device
    if settings.get_setting('nvenc_device') not in ['none']:
        # Attempt to match to that configured hardware device
        for hw_device in hardware_devices:
            if str(settings.get_setting('nvenc_device')) == str(hw_device.get('hwaccel_device')):
                hardware_device = hw_device
                break
    # If no matching hardware device is set, then select the first one
    if not hardware_device:
        hardware_device = hardware_devices[0]
    return hardware_device


class NvencEncoder(Encoder):
    def __init__(self, settings=None, probe=None):
        super().__init__(settings=settings, probe=probe)

    def _smart_basic_stream_args(self, stream_id, filter_state, target_encoder, hardware_device):
        """
        Build smart output target args for basic mode, returning the stream args list.
        """
        stream_args = []
        smart_recommendation = None
        provides = self.provides()
        try:
            helper = SmartOutputTargetHelper(self.probe)
            file_path = None
            try:
                file_path = (self.probe.get_probe() or {}).get("format", {}).get("filename")
            except Exception:
                file_path = None
            target_filters = {
                "target_width":  filter_state.get("target_width") if filter_state else None,
                "target_height": filter_state.get("target_height") if filter_state else None,
                "scale_applied": filter_state.get("scale_applied") if filter_state else False,
                "crop_applied":  filter_state.get("crop_applied") if filter_state else False,
            }
            source_stats = helper.collect_source_stats(file_path=file_path)
            goal = self.settings.get_setting('smart_output_target')
            target_codec = provides.get(target_encoder, {}).get('codec', 'h264')
            target_supports_hdr10 = target_encoder in ("hevc_nvenc",)
            smart_recommendation = helper.recommend_params(
                goal,
                source_stats,
                target_filters,
                target_codec,
                target_encoder,
                target_supports_hdr10,
            )
        except Exception as exc:
            logger.info("Smart output target unavailable, falling back to defaults: %s", exc)

        if smart_recommendation:
            preset_value = "p7"
            stream_args += ['-preset', str(preset_value)]

            quality_mode = smart_recommendation.get("quality_mode")
            quality_index = smart_recommendation.get("quality_index")
            wants_cap = smart_recommendation.get("wants_cap")
            rc_mode = "constqp" if quality_mode == SmartOutputTargetHelper.QUALITY_CONST else "vbr"
            if rc_mode == "constqp" and wants_cap:
                rc_mode = "vbr"
            stream_args += [f'-rc:v:{stream_id}', rc_mode]

            if rc_mode == "constqp":
                if quality_index is not None:
                    stream_args += [f'-qp:v:{stream_id}', str(int(quality_index))]
            else:
                if quality_index is not None:
                    stream_args += [f'-cq:v:{stream_id}', str(int(quality_index))]
                    # NVENC VBR target-quality mode still expects an average bitrate; set 0 so maxrate is the only rail.
                    # REF: https://docs.nvidia.com/video-technologies/video-codec-sdk/12.1/nvenc-video-encoder-api-prog-guide/index.html?utm_source=chatgpt.com#finer-control-by-overriding-preset-parameters
                    stream_args += [f'-b:v:{stream_id}', '0']
                maxrate = smart_recommendation.get("maxrate")
                bufsize = smart_recommendation.get("bufsize")
                if maxrate:
                    stream_args += [f'-maxrate:v:{stream_id}', str(int(maxrate))]
                if bufsize:
                    stream_args += [f'-bufsize:v:{stream_id}', str(int(bufsize))]

            # Apply fixed lookahead/AQ defaults in encoder layer.
            if rc_mode == "vbr":
                stream_args += [f'-rc-lookahead:v:{stream_id}', '12']

            if is_pascal_or_newer():
                stream_args += [f'-aq-strength:v:{stream_id}', '8']
                stream_args += [f'-spatial-aq:v:{stream_id}', '1']
                if _supports_temporal_aq(target_encoder, hardware_device.get('hwaccel_device', 0)):
                    stream_args += [f'-temporal-aq:v:{stream_id}', '1']
            else:
                logger.info("Skipping NVENC AQ because GPU compute capability is older than Pascal or indeterminate.")

            logger.info(
                "Smart output target applied (goal=%s, mode=%s, preset=%s, target=%sx%s, cap=%s, confidence=%s)",
                smart_recommendation.get("goal"),
                smart_recommendation.get("quality_mode"),
                preset_value,
                smart_recommendation.get("target_resolution", {}).get("width"),
                smart_recommendation.get("target_resolution", {}).get("height"),
                smart_recommendation.get("target_cap"),
                smart_recommendation.get("confidence"),
            )

        return stream_args

    def _map_pix_fmt(self, is_h264: bool, is_10bit: bool) -> str:
        if is_10bit and not is_h264:
            return "p010le"
        else:
            return "nv12"

    def provides(self):
        return {
            "h264_nvenc": {
                "codec": "h264",
                "label": "NVENC - h264_nvenc",
            },
            "hevc_nvenc": {
                "codec": "hevc",
                "label": "NVENC - hevc_nvenc",
            },
        }

    def options(self):
        return {
            "nvenc_device":                        "none",
            "nvenc_decoding_method":               "cpu",
            "nvenc_preset":                        "p4",
            "nvenc_tune":                          "auto",
            "nvenc_profile":                       "main",
            "nvenc_encoder_ratecontrol_method":    "auto",
            "nvenc_encoder_ratecontrol_lookahead": 0,
            "nvenc_constant_quantizer_scale":      23,
            "nvenc_enable_spatial_aq":             False,
            "nvenc_enable_temporal_aq":            False,
            "nvenc_aq_strength":                   8,
        }

    def generate_default_args(self):
        """
        Generate a list of args for using a NVENC decoder

        REF: https://trac.ffmpeg.org/wiki/HWAccelIntro#NVDECCUVID

        :return:
        """
        hardware_device = get_configured_device_info(self.settings)

        generic_kwargs = {}
        advanced_kwargs = {}
        # Check if we are using a HW accelerated decoder also
        if self.settings.get_setting('nvenc_decoding_method') in ['cuda', 'nvdec', 'cuvid']:
            generic_kwargs = {
                "-hwaccel_device":   hardware_device.get('hwaccel_device', 0),
                "-hwaccel":          self.settings.get_setting('nvenc_decoding_method'),
                "-init_hw_device":   "cuda=hw",
                "-filter_hw_device": "hw",
            }
            if self.settings.get_setting('nvenc_decoding_method') in ['cuda', 'nvdec']:
                generic_kwargs["-hwaccel_output_format"] = "cuda"

        return generic_kwargs, advanced_kwargs

    def generate_filtergraphs(self, current_filter_args, smart_filters, encoder_name):
        """
        Generate the required filter for enabling NVENC/CUDA HW acceleration.

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
                hw_smart_filters.append(f"scale_cuda={w}:-1")
            else:
                remaining_smart_filters.append(sf)

        # Check for HW accelerated decode mode
        # All decode methods ('cuda', 'nvdec', 'cuvid') are handled by the same
        # filtergraph logic and output CUDA frames. The main FFmpeg command handles the specific decoder.
        hw_decode = (self.settings.get_setting('nvenc_decoding_method') or '').lower() in ('cuda', 'nvdec', 'cuvid')

        # Check software format to use
        target_fmt = self._target_pix_fmt_for_encoder(encoder_name)

        # Handle HDR
        enc_supports_hdr = (encoder_name in ["hevc_nvenc"])
        target_color_config = self._target_color_config_for_encoder(encoder_name)

        # If we have SW filters:
        if remaining_smart_filters or current_filter_args:
            # If we have SW filters and HW decode (CUDA/NVDEC) is enabled, make decoder produce SW frames
            if hw_decode:
                generic_kwargs['-hwaccel_output_format'] = target_fmt

            # Add filter to upload software frames to CUDA for CUDA filters
            # Note, format conversion (if any - eg yuv422p10le -> p010le) happens after the software filters.
            # If a user applies a custom software filter that does not support the pix_fmt, then will need to prefix it with 'format=p010le'
            chain = [f"format={target_fmt}"]
            if enc_supports_hdr and target_color_config.get('apply_color_params'):
                # Apply setparams filter if software filters exist (apply at the start of the filters list) to preserve HDR tags
                chain.append(target_color_config['setparams_filter'])
            chain += ["hwupload_cuda"]
            end_filter_args.append(",".join(chain))
        # If we have no software filters:
        elif not hw_decode:
            # CPU decode -> setparams (if HDR) -> upload to CUDA
            chain = [f"format={target_fmt}"]
            if enc_supports_hdr and target_color_config.get('apply_color_params'):
                chain.append(target_color_config['setparams_filter'])
            chain.append("hwupload_cuda")
            start_filter_args.append(",".join(chain))

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
        try:
            hardware_devices = list_available_cuda_devices()
        except ValueError:
            hardware_devices = []
        if not hardware_devices:
            # Return no options. No hardware device was found
            return {}
        provides = self.provides()
        return provides.get(encoder, {})

    def stream_args(self, stream_info, stream_id, encoder_name, filter_state=None):
        generic_kwargs = {}
        advanced_kwargs = {}
        encoder_args = []
        stream_args = []

        # Specify the GPU to use for encoding
        hardware_device = get_configured_device_info(self.settings)
        stream_args += ['-gpu', str(hardware_device.get('hwaccel_device', '0'))]

        # Handle HDR
        enc_supports_hdr = (encoder_name in ["hevc_nvenc"])
        if enc_supports_hdr:
            target_color_config = self._target_color_config_for_encoder(encoder_name)
        else:
            target_color_config = {
                "apply_color_params": False
            }
        if enc_supports_hdr and target_color_config.get('apply_color_params'):
            # Force Main10 profile
            stream_args += [f'-profile:v:{stream_id}', 'main10']

        # Use defaults for basic mode
        if self.settings.get_setting('mode') in ['basic']:
            # Read defaults
            defaults = self.options()

            if enc_supports_hdr and target_color_config.get('apply_color_params'):
                # Add HDR color tags to the encoder output stream
                for k, v in target_color_config.get('stream_color_params', {}).items():
                    stream_args += [k, v]

            smart_stream_args = []
            smart_goal_enabled = (
                self.settings.get_setting('enable_smart_output_target') and
                filter_state and filter_state.get("execution_stage")
            )
            if smart_goal_enabled and self.probe:
                smart_stream_args = self._smart_basic_stream_args(
                    stream_id,
                    filter_state,
                    encoder_name,
                    hardware_device,
                )

            if smart_stream_args:
                stream_args += smart_stream_args
            elif smart_goal_enabled:
                stream_args += ['-preset', 'p7']
            else:
                stream_args += ['-preset', str(defaults.get('nvenc_preset'))]

            return {
                "generic_kwargs":  generic_kwargs,
                "advanced_kwargs": advanced_kwargs,
                "encoder_args":    encoder_args,
                "stream_args":     stream_args,
            }

        # Add the preset and tune
        if self.settings.get_setting('nvenc_preset'):
            stream_args += ['-preset', str(self.settings.get_setting('nvenc_preset'))]
        if self.settings.get_setting('nvenc_tune') and self.settings.get_setting('nvenc_tune') != 'auto':
            stream_args += ['-tune', str(self.settings.get_setting('nvenc_tune'))]
        if self.settings.get_setting('nvenc_profile') and self.settings.get_setting('nvenc_profile') != 'auto':
            stream_args += [f'-profile:v:{stream_id}', str(self.settings.get_setting('nvenc_profile'))]

        # Apply rate control config
        if self.settings.get_setting('nvenc_encoder_ratecontrol_method') in ['constqp', 'vbr', 'cbr']:
            # Set the rate control method
            stream_args += [f'-rc:v:{stream_id}', str(self.settings.get_setting('nvenc_encoder_ratecontrol_method'))]
            if self.settings.get_setting('nvenc_encoder_ratecontrol_method') == 'constqp':
                qp_value = self.settings.get_setting('nvenc_constant_quantizer_scale')
                try:
                    qp_value = int(qp_value)
                except (TypeError, ValueError):
                    qp_value = -1
                if qp_value >= 0:
                    stream_args += [f'-qp:v:{stream_id}', str(qp_value)]
        rc_la = int(self.settings.get_setting('nvenc_encoder_ratecontrol_lookahead') or 0)
        if rc_la > 0:
            stream_args += [f'-rc-lookahead:v:{stream_id}', str(rc_la)]

        # Apply adaptive quantization
        if self.settings.get_setting('nvenc_enable_spatial_aq'):
            stream_args += [f'-spatial-aq:v:{stream_id}', '1']
        if self.settings.get_setting('nvenc_enable_spatial_aq') or self.settings.get_setting('nvenc_enable_temporal_aq'):
            stream_args += [f'-aq-strength:v:{stream_id}', str(self.settings.get_setting('nvenc_aq_strength'))]
        if self.settings.get_setting('nvenc_enable_temporal_aq'):
            temporal_aq_supported = _supports_temporal_aq(encoder_name, hardware_device.get('hwaccel_device', 0))
            if not temporal_aq_supported:
                logger.warning(
                    "NVENC temporal AQ is configured, but this GPU does not appear to support it. This will likely fail.")
            stream_args += [f'-temporal-aq:v:{stream_id}', '1']

        # If CUVID is enabled, return generic_kwargs
        if (self.settings.get_setting('nvenc_decoding_method') or '').lower() in ['cuvid']:
            in_codec = stream_info.get('codec_name', 'unknown_codec_name')
            generic_kwargs = {f'-c:v:{stream_id}': f'{in_codec}_cuvid'}

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

    def get_nvenc_device_form_settings(self):
        values = {
            "label":          "NVIDIA Device",
            "sub_setting":    True,
            "input_type":     "select",
            "select_options": [
                {
                    "value": "none",
                    "label": "No NVIDIA devices available",
                }
            ]
        }
        default_option = None
        try:
            hardware_devices = list_available_cuda_devices()
        except ValueError:
            hardware_devices = []
        if hardware_devices:
            values['select_options'] = []
            for hw_device in hardware_devices:
                if not default_option:
                    default_option = hw_device.get('hwaccel_device', 'none')
                values['select_options'].append({
                    "value": hw_device.get('hwaccel_device', 'none'),
                    "label": "NVIDIA device '{}'".format(hw_device.get('hwaccel_device_name', 'not found')),
                })
        if not default_option:
            default_option = 'none'

        self.__set_default_option(values['select_options'], 'nvenc_device', default_option=default_option)
        if self.settings.get_setting('mode') not in ['standard']:
            values["display"] = "hidden"
        return values

    def get_nvenc_decoding_method_form_settings(self):
        values = {
            "label":          "Enable HW Decoding",
            "description":    "Warning: Ensure your device supports decoding the source video codec or it will fail.\n"
                              "This enables full hardware transcode with NVDEC and NVENC, using only GPU memory for the entire video transcode.\n"
                              "If filters are configured in the plugin, decoder will output NV12 software surfaces which are slightly slower.\n"
                              "Note: It is recommended that you disable this option for 10-bit encodes.",
            "sub_setting":    True,
            "input_type":     "select",
            "select_options": [
                {
                    "value": "cpu",
                    "label": "Disabled - Use CPU to decode of video source (provides best compatibility)",
                },
                {
                    "value": "cuda",
                    "label": "NVDEC/CUDA - Use the GPUs HW decoding the video source and upload surfaces to CUDA (recommended)",
                },
                {
                    "value": "cuvid",
                    "label": "CUVID - Older interface for HW video decoding. Kepler or older hardware may perform better with this option",
                }
            ]
        }
        if self.settings.get_setting('mode') not in ['standard']:
            values["display"] = "hidden"
        return values

    def get_nvenc_preset_form_settings(self):
        values = {
            "label":          "Encoder quality preset",
            "sub_setting":    True,
            "input_type":     "select",
            "select_options": [
                {
                    "value": "p1",
                    "label": "Fastest (P1)",
                },
                {
                    "value": "p2",
                    "label": "Faster (P2)",
                },
                {
                    "value": "p3",
                    "label": "Fast (P3)",
                },
                {
                    "value": "p4",
                    "label": "Medium (P4) - Balanced performance and quality",
                },
                {
                    "value": "p5",
                    "label": "Slow (P5)",
                },
                {
                    "value": "p6",
                    "label": "Slower (P6)",
                },
                {
                    "value": "p7",
                    "label": "Slowest (P7)",
                },
            ],
        }
        self.__set_default_option(values['select_options'], 'nvenc_preset', default_option='p4')
        if self.settings.get_setting('mode') not in ['standard']:
            values["display"] = "hidden"
        return values

    def get_nvenc_tune_form_settings(self):
        values = {
            "label":          "Tune for a particular type of source or situation",
            "sub_setting":    True,
            "input_type":     "select",
            "select_options": [
                {
                    "value": "auto",
                    "label": "Disabled – Do not apply any tune",
                },
                {
                    "value": "hq",
                    "label": "HQ – High quality (ffmpeg default)",
                },
                {
                    "value": "ll",
                    "label": "LL – Low latency",
                },
                {
                    "value": "ull",
                    "label": "ULL – Ultra low latency",
                },
                {
                    "value": "lossless",
                    "label": "Lossless",
                },
            ],
        }
        self.__set_default_option(values['select_options'], 'nvenc_tune', default_option='auto')
        if self.settings.get_setting('mode') not in ['standard']:
            values["display"] = "hidden"
        return values

    def get_nvenc_profile_form_settings(self):
        values = {
            "label":          "Profile",
            "description":    "The profile determines which features of the codec are available and enabled,\n"
                              "while also affecting other restrictions.\n"
                              "Any of these profiles are capable of 4:2:0, 4:2:2 and 4:4:4, however the support\n"
                              "depends on the installed hardware.",
            "sub_setting":    True,
            "input_type":     "select",
            "select_options": [
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
                    "value": "main10",
                    "label": "Main10",
                },
                {
                    "value": "high444p",
                    "label": "High444p",
                },
            ],
        }
        self.__set_default_option(values['select_options'], 'nvenc_profile', default_option='main')
        if self.settings.get_setting('mode') not in ['standard']:
            values["display"] = "hidden"
        return values

    def get_nvenc_encoder_ratecontrol_method_form_settings(self):
        values = {
            "label":          "Encoder ratecontrol method",
            "description":    "Note that the rate control is already defined in the Encoder Quality Preset option.\n"
                              "Selecting anything other than 'Disabled' will override the preset rate-control.",
            "sub_setting":    True,
            "input_type":     "select",
            "select_options": [
                {
                    "value": "auto",
                    "label": "Auto – Use the rate control setting pre-defined in the preset option (recommended)",
                },
                {
                    "value": "constqp",
                    "label": "CQP - Quality based mode using constant quantizer scale",
                },
                {
                    "value": "vbr",
                    "label": "VBR - Bitrate based mode using variable bitrate",
                },
                {
                    "value": "cbr",
                    "label": "CBR - Bitrate based mode using constant bitrate",
                },
            ]
        }
        self.__set_default_option(values['select_options'], 'nvenc_encoder_ratecontrol_method', default_option='auto')
        if self.settings.get_setting('mode') not in ['standard']:
            values["display"] = "hidden"
        return values

    def get_nvenc_encoder_ratecontrol_lookahead_form_settings(self):
        # Lower is better
        values = {
            "label":          "Configure the number of frames to look ahead for rate-control",
            "sub_setting":    True,
            "input_type":     "slider",
            "slider_options": {
                "min": 0,
                "max": 30,
            },
        }
        if self.settings.get_setting('mode') not in ['standard']:
            values["display"] = "hidden"
        return values

    def get_nvenc_constant_quantizer_scale_form_settings(self):
        # Lower is better
        values = {
            "label":          "Constant quantizer scale",
            "description":    "Sets the quantizer when rate control is set to CQP. Lower values increase quality. Use -1 for NVENC defaults.",
            "sub_setting":    True,
            "input_type":     "slider",
            "slider_options": {
                "min": -1,
                "max": 51,
            },
        }
        if self.settings.get_setting('mode') not in ['standard']:
            values["display"] = "hidden"
        if self.settings.get_setting('nvenc_encoder_ratecontrol_method') != 'constqp':
            values["display"] = "hidden"
        return values

    def get_nvenc_enable_spatial_aq_form_settings(self):
        values = {
            "label":       "Enable Spatial Adaptive Quantization",
            "description": "This adjusts the quantization parameter within each frame based on spatial complexity.\n"
                           "This helps in improving the quality of areas within a frame that are more detailed or complex.",
            "sub_setting": True,
        }
        # Hide when hardware is definitively older than Pascal.
        pascal_capable = is_pascal_or_newer()
        if pascal_capable is False:
            values["display"] = 'hidden'
        if self.settings.get_setting('mode') not in ['standard']:
            values["display"] = 'hidden'
        return values

    def get_nvenc_enable_temporal_aq_form_settings(self):
        values = {
            "label":       "Enable Temporal Adaptive Quantization",
            "description": "This adjusts the quantization parameter across frames, based on the motion and temporal complexity.\n"
                           "This is particularly effective in scenes with varying levels of motion, enhancing quality where it's most needed.\n"
                           "Support depends on the encoder/GPU combination. Ensure that your GPU supports this (Eg. at least Turing or newer hardware. Not a TU117 processor. Etc.).",
            "sub_setting": True,
        }
        # Hide when hardware is definitively older than Turing.
        # TODO: This changes depending on the encoder and hardware. Update this to use _supports_temporal_aq to detect if the GPU can use Temporal AQ.
        turing_capable = is_turing_or_newer()
        if turing_capable is False:
            values["display"] = 'hidden'
        if self.settings.get_setting('mode') not in ['standard']:
            values["display"] = 'hidden'
        return values

    def get_nvenc_aq_strength_form_settings(self):
        # Lower is better
        values = {
            "label":          "Strength of the adaptive quantization",
            "description":    "Controls the strength of the adaptive quantization (both spatial and temporal).\n"
                              "A higher value indicates stronger adaptation, which can lead to better preservation\n"
                              "of detail but might also increase the bitrate.",
            "sub_setting":    True,
            "input_type":     "slider",
            "slider_options": {
                "min": 0,
                "max": 15,
            },
        }
        if self.settings.get_setting('mode') not in ['standard']:
            values["display"] = "hidden"
        if (
            not self.settings.get_setting('nvenc_enable_spatial_aq') and
            not self.settings.get_setting('nvenc_enable_temporal_aq')
        ):
            values["display"] = "hidden"
        return values
