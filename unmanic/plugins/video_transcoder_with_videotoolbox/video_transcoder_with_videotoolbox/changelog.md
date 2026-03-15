**<span style="color:#56adda">0.2.2</span>**
- Updated README.md with comprehensive VideoToolbox documentation
- Updated description.md with VideoToolbox encoder information and usage guidelines
- Added performance notes and quality recommendations

**<span style="color:#56adda">0.2.1</span>**
- Added VBV rate control: -maxrate and -bufsize parameters
- Allows fine-grained bitrate control for streaming-quality encodes
- Useful for Netflix-like 720p quality with controlled peaks
- Both parameters optional (0 = disabled)

**<span style="color:#56adda">0.2.0</span>**
- MAJOR FIX: VideoToolbox encoder now properly applies quality settings (-q:v)
- Fixed plugin_stream_mapper.py missing VideoToolbox support (critical bug)
- Fixed encoder_args vs stream_args placement for VideoToolbox
- Added full Apple VideoToolbox hardware encoder support (h264_videotoolbox and hevc_videotoolbox)
- Support for Apple Silicon (M1/M2/M3/M4) and Intel Macs (2017+)
- Automatic HDR10 metadata preservation for HEVC with VideoToolbox
- Quality-based encoding with proper 0-100 scale (higher = better)
- Proper configuration isolation with videotoolbox_ prefix
- Contributed by: Marcos Gabriel

**<span style="color:#56adda">0.1.15</span>**
- Add a warning against using "Prefer Quality" when scaling a video down
- Add smart output target support for QSV
- Reduce sample time for black-box detection to 10 seconds of video
- Fix smart output target bitrate derivation to prefer video-only stream stats (Matroska `BPS`) and packet sampling over container bitrate
- Add ffprobe sampling as a fallback option when bitrate is not specified on a video stream
- Add more detailed ouput to worker logs as the plugin processes and generates the ffmpeg command to be run

**<span style="color:#56adda">0.1.14</span>**
- Enable smart filters and resolution scaling in basic mode (works only with NVENC at this stage)
- Added new smart output target controls to basic mode, including goal presets (Prefer Quality/Balanced/Prefer Compression)

**<span style="color:#56adda">0.1.13</span>**
- Fix bug where intermittently HW accelerated config was reverted to CPU encoding on its own

**<span style="color:#56adda">0.1.12</span>**
- Improved handling for HDR content with new helper tools for detecting and parsing metadata.
- Removed the look-ahead feature from QSV's HEVC and AV1 encoders (not supported).
- Fixed an issue with default tune options on libx264 and libx265
- Removed the tune option from QSV encoders (not supported).
- Changed the VAAPI hardware decoding setting to now be a dropdown menu instead of a checkbox (like all the other encoders).
- Speed up crop-detect on smaller files.

**<span style="color:#56adda">0.1.11</span>**
- Fix CQP quality selector for VAAPI encoding

**<span style="color:#56adda">0.1.10</span>**
- Adds better management of 10Bit video formats for NVIDIA, Intel, and AMD hardware. 
- Adds an improved fallback system to prevent failed decodes for QSV.
- The video scaling smart filter has been improved to correctly work with custom resolutions and different aspect ratios.
- A new debugging tool has been added to make troubleshooting and development easier.

**<span style="color:#56adda">0.1.9</span>**
- Add some safety rails to the black-bar detection so we ignore bars of a few px

**<span style="color:#56adda">0.1.8</span>**
- Improvements to black-bar detection

**<span style="color:#56adda">0.1.7</span>**
- Add support for the STV-AV1 encoder

**<span style="color:#56adda">0.1.6</span>**
- Fix bug causing files to be perpetually added to the task queue if mode is set to advanced, but the smart filters were previously applied

**<span style="color:#56adda">0.1.5</span>**
- Fix video scaling smart filter for videos that do not use a 16:9 aspect ratio

**<span style="color:#56adda">0.1.4</span>**
- add missing 'generic_kwargs' from return statement in nvenc.py basic config section

**<span style="color:#56adda">0.1.3</span>**
- fix nvenc 10 bit profile name

**<span style="color:#56adda">0.1.2</span>**
- Fix for plugin updates from versions older than 0.1.0

**<span style="color:#56adda">0.1.1</span>**
- Add support for the av1_qsv encoder

**<span style="color:#56adda">0.1.0</span>**
- Stable release
- Prefix QSV config options in plugin settings file to isolate them from libx encoder settings (users will need to reconfigure some QSV settings)
- Prefix VAAPI config options in plugin settings file to isolate them from libx encoder settings (users will need to reconfigure some VAAPI settings)

**<span style="color:#56adda">0.0.10</span>**
- Add support for QSV HW accelerated decoding
- Add support for the scale_qsv filter when using qsv encoding
- Add support for the scale_cuda filter when using nvenc

**<span style="color:#56adda">0.0.9</span>**
- Add support for the h264_vaapi encoder
- Add support for the h264_nvenc encoder
- Add support for the hevc_nvenc encoder

**<span style="color:#56adda">0.0.8</span>**
- update ffmpeg helper library to latest version

**<span style="color:#56adda">0.0.7</span>**
- Handle circumstance where file probe has no 'codec_name'
- Improve library scan speed when used with other plugins that use ffprobe

**<span style="color:#56adda">0.0.6</span>**
- Fix an error in ffmpeg command generator

**<span style="color:#56adda">0.0.5</span>**
- Improvements to ffmpeg command generator
- Fix issue where input file was added before additional main options

**<span style="color:#56adda">0.0.4</span>**
- Add ability to specify a codec in plain text in advanced mode

**<span style="color:#56adda">0.0.3</span>**
- Fix bug where videos would forever be re-added to the task list if force transcoding was enabled

**<span style="color:#56adda">0.0.2</span>**
- Fix detection if video stream is already in the correct codec
- Add ability to strip data and attachment streams from video files

**<span style="color:#56adda">0.0.1</span>**
- Add an "Advanced" configuration option to the plugin's settings
- Add ability to force transcoding of a video when it is already in the desired video codec

**<span style="color:#56adda">0.0.1-beta2</span>**
- Add support for specifying the VAAPI device
- Improvements to code that generates the encoder specific arguments

**<span style="color:#56adda">0.0.1-beta1</span>**
- Initial version
