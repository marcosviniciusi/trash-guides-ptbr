
---

##### Links:

- [Support](https://unmanic.app/discord)
- [Issues/Feature Requests](https://github.com/Unmanic/plugin.video_transcoder/issues)
- [Pull Requests](https://github.com/Unmanic/plugin.video_transcoder/pulls)

---

##### Documentation:

For information on the available encoder settings:
- LibX (CPU encoders)
  - [FFmpeg - H.264](https://trac.ffmpeg.org/wiki/Encode/H.264)
  - [FFmpeg - H.265](https://trac.ffmpeg.org/wiki/Encode/H.265)
- QuickSync
  - [FFmpeg - QuickSync](https://trac.ffmpeg.org/wiki/Hardware/QuickSync)
  - [INTEL CPU compatibility chart](https://en.wikipedia.org/wiki/Intel_Quick_Sync_Video#Hardware_decoding_and_encoding).
- VAAPI
  - [FFmpeg - VAAPI](https://trac.ffmpeg.org/wiki/Hardware/VAAPI)
  - [FFmpeg - HWAccelIntro](https://trac.ffmpeg.org/wiki/HWAccelIntro#VAAPI)
- NVENC
  - [FFmpeg - HWAccelIntro](https://trac.ffmpeg.org/wiki/HWAccelIntro#NVENC)
  - [NVIDIA GPU compatibility chart](https://developer.nvidia.com/video-encode-and-decode-gpu-support-matrix-new)
  - [NVIDIA FFmpeg Transcoding Guide](https://developer.nvidia.com/blog/nvidia-ffmpeg-transcoding-guide/)
- **VideoToolbox (Apple Silicon & Intel Macs)**
  - [FFmpeg - VideoToolbox](https://trac.ffmpeg.org/wiki/HWAccelIntro#VideoToolbox)
  - [Apple VideoToolbox Documentation](https://developer.apple.com/documentation/videotoolbox)
  - [HandBrake - VideoToolbox Guide](https://handbrake.fr/docs/en/latest/technical/video-videotoolbox.html)

:::important
**Apple VideoToolbox Support**

VideoToolbox hardware encoding is now supported for macOS users:
- **Apple Silicon** (M1, M2, M3, M4) - Full support
- **Intel Macs** (2017 or newer) - Full support
- Supports H.264 and HEVC/H.265 encoding
- Automatic HDR10 metadata preservation for HEVC
- Quality-based encoding (0-100 scale, higher = better)
- Optional VBV rate control (maxrate/bufsize) for streaming-optimized encodes
- **Note**: VideoToolbox prioritizes speed and efficiency over maximum compression. Files may be 20-30% larger than QSV/NVENC at equivalent quality.
:::

:::important
**Legacy Intel Hardware (Broadwell or older)**

While the [INTEL CPU compatibility chart](https://en.wikipedia.org/wiki/Intel_Quick_Sync_Video#Hardware_decoding_and_encoding) states that all Sandy Bridge, Ivy Bridge, Haswell and Broadwell CPUs support Quick Sync Video encoding, the required iHD VA driver on Linux does not support anything older than Broadwell ([REF](https://github.com/intel/libva/issues/436#issuecomment-668116723)). These chips need to use the i965 VA driver. Therefore, if you are using a Broadwell or older Intel CPU and you want to use HW accelerated encoding of h264, then you need to use VAAPI.
:::

---

##### Additional Information:

:::note
**Advanced**

If you set the Config mode to *"Advanced"*, the input text privdes the ability to add FFmpeg commandline args in three different places:
1. **MAIN OPTIONS** - After the default generic options.
   ([Main Options Docs](https://ffmpeg.org/ffmpeg.html#Main-options))
1. **ADVANCED OPTIONS** - After the input file has been specified.
   ([Advanced Options Docs](https://ffmpeg.org/ffmpeg.html#Advanced-options))
1. **VIDEO OPTIONS** - After the video is mapped. Here you can specify the video encoder, its params and any additional video options.
   ([Video Options Docs](https://ffmpeg.org/ffmpeg.html#Video-Options))
   ([Advanced Video Options Docs](https://ffmpeg.org/ffmpeg.html#Advanced-Video-options))

```
ffmpeg \
    -hide_banner \
    -loglevel info \
    <CUSTOM MAIN OPTIONS HERE> \
    -i /path/to/input/video.mkv \
    <CUSTOM ADVANCED OPTIONS HERE> \
    -map 0:0 -map 0:1 \
    -c:v:0 <CUSTOM VIDEO OPTIONS HERE> \
    -c:a:0 copy \
    -y /path/to/output/video.mkv 
```
:::

:::note
**Force transcoding**

Enabling the *"Force transcoding ..."* option under *"Standard"* mode will force a transcode of the video stream even if it matches the selected video codec.

A file will only be forced to be transcoded once. It will then be flagged in a local `.unmanic` file to prevent it being added to the pending tasks list in a loop.

However, a file previously flagged to be ignored by this will still be transcoded to apply any matching smart filters such as scaling, stripping data streams, etc.
:::

:::note
**VideoToolbox Quality Settings**

VideoToolbox uses a quality scale from 0-100 (higher = better quality), which is different from software encoders:
- **H.264**: Recommended starting point is 50 (≈ libx264 crf=23)
- **HEVC**: Recommended starting point is 65 (≈ libx265 crf=28)

For streaming-optimized encodes, enable VBV rate control:
- **Maximum bitrate**: Limits bitrate spikes (e.g., 3800k for Netflix-style 720p)
- **Buffer size**: Usually 2x maxrate (e.g., 7600k)

**Performance**: VideoToolbox on Apple Silicon can encode 10-20x faster than software encoding with good quality, though file sizes may be 20-30% larger than QSV/NVENC at equivalent quality.
:::
