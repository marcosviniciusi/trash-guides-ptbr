# unmanic.plugin.helpers.ffmpeg

This python module is a helper library for any Unmanic plugin that needs to build FFmpeg commands to be executed.


# Using the module

## Adding it to your project

```bash
└── my_plugin_id/
    ├── changelog.md
    ├── description.md
    ├── .gitignore
    ├── icon.png
    ├── info.json
    ├── lib/
    |   └── ffmpeg/
    |       ├── __init__.py
    |       ├── LICENSE
    |       ├── mimetype_overrides.py
    |       ├── parser.py
    |       ├── probe.py
    |       ├── README.md
    |       └── stream_mapper.py
    ├── LICENSE
    ├── plugin.py
    └── requirements.txt
```

### Git Submodule
It can be included in your plugin project as a submodule.
```
git submodule add https://github.com/Josh5/unmanic.plugin.helpers.ffmpeg.git ./lib/ffmpeg
```
If you use it sure to include all files in the lib directory when publishing your project to the Unmanic plugin repository.

### Project source download
Download the git repository as zip file and extract it to `lib` directory.
```
mkdir -p ./lib
curl -L "https://github.com/Josh5/unmanic.plugin.helpers.ffmpeg/archive/refs/heads/master.zip" --output /tmp/unmanic.plugin.helpers.ffmpeg.zip
unzip /tmp/unmanic.plugin.helpers.ffmpeg.zip -d ./lib/
mv -v ./lib/unmanic.plugin.helpers.ffmpeg-master ./lib/ffmpeg
```

---

## Importing it in your project

This module comes with x3 classes to assist in generating FFmpeg commands for your Unmanic plugin.

You can import all 3 classes into your plugin like this:

```python
from my_plugin_id.lib.ffmpeg import Parser, Probe, StreamMapper
```
> **Note**
> Be sure to rename 'my_plugin_id' in the example above.

---

## Using the `Probe` class

The Probe class is a wrapper around the `ffprobe` cli. This can be used to generate a file probe object containing file format and stream info.

Add this to your plugin runner function:
```python
    # Get file probe
    probe = Probe.init_probe(data, logger, allowed_mimetypes=['video', 'audio'])
    if not probe:
        # File not able to be probed by ffprobe. The file is probably not a audio/video file.
        return
```

You can then use this newly created Probe object in your plugin. To read the FFprobe data, add this:
```python
    ffprobe_data = probe.get_probe()
```

### FFprobe Example
<details>
  <summary>Show</summary>

  ```json
{
    "streams": [
        {
            "index": 0,
            "codec_name": "hevc",
            "codec_long_name": "H.265 / HEVC (High Efficiency Video Coding)",
            "profile": "Main",
            "codec_type": "video",
            "codec_tag_string": "[0][0][0][0]",
            "codec_tag": "0x0000",
            "width": 1920,
            "height": 1080,
            "coded_width": 1920,
            "coded_height": 1080,
            "closed_captions": 0,
            "film_grain": 0,
            "has_b_frames": 2,
            "sample_aspect_ratio": "1:1",
            "display_aspect_ratio": "16:9",
            "pix_fmt": "yuv420p",
            "level": 120,
            "color_range": "tv",
            "color_space": "bt709",
            "color_transfer": "bt709",
            "color_primaries": "bt709",
            "chroma_location": "left",
            "refs": 1,
            "r_frame_rate": "24000/1001",
            "avg_frame_rate": "24000/1001",
            "time_base": "1/1000",
            "start_pts": 21,
            "start_time": "0.021000",
            "extradata_size": 2471,
            "disposition": {
                "default": 1,
                "dub": 0,
                "original": 0,
                "comment": 0,
                "lyrics": 0,
                "karaoke": 0,
                "forced": 0,
                "hearing_impaired": 0,
                "visual_impaired": 0,
                "clean_effects": 0,
                "attached_pic": 0,
                "timed_thumbnails": 0,
                "captions": 0,
                "descriptions": 0,
                "metadata": 0,
                "dependent": 0,
                "still_image": 0
            },
            "tags": {
                "DURATION": "00:00:10.239000000"
            }
        },
        {
            "index": 1,
            "codec_name": "aac",
            "codec_long_name": "AAC (Advanced Audio Coding)",
            "profile": "LC",
            "codec_type": "audio",
            "codec_tag_string": "[0][0][0][0]",
            "codec_tag": "0x0000",
            "sample_fmt": "fltp",
            "sample_rate": "48000",
            "channels": 6,
            "channel_layout": "5.1",
            "bits_per_sample": 0,
            "r_frame_rate": "0/0",
            "avg_frame_rate": "0/0",
            "time_base": "1/1000",
            "start_pts": 0,
            "start_time": "0.000000",
            "extradata_size": 5,
            "disposition": {
                "default": 1,
                "dub": 0,
                "original": 0,
                "comment": 0,
                "lyrics": 0,
                "karaoke": 0,
                "forced": 0,
                "hearing_impaired": 0,
                "visual_impaired": 0,
                "clean_effects": 0,
                "attached_pic": 0,
                "timed_thumbnails": 0,
                "captions": 0,
                "descriptions": 0,
                "metadata": 0,
                "dependent": 0,
                "still_image": 0
            },
            "tags": {
                "language": "eng",
                "title": "Surround",
                "DURATION": "00:00:10.005000000"
            }
        },
        {
            "index": 2,
            "codec_name": "ass",
            "codec_long_name": "ASS (Advanced SSA) subtitle",
            "codec_type": "subtitle",
            "codec_tag_string": "[0][0][0][0]",
            "codec_tag": "0x0000",
            "r_frame_rate": "0/0",
            "avg_frame_rate": "0/0",
            "time_base": "1/1000",
            "start_pts": 0,
            "start_time": "0.000000",
            "duration_ts": 10614,
            "duration": "10.614000",
            "extradata_size": 487,
            "disposition": {
                "default": 0,
                "dub": 0,
                "original": 0,
                "comment": 0,
                "lyrics": 0,
                "karaoke": 0,
                "forced": 0,
                "hearing_impaired": 0,
                "visual_impaired": 0,
                "clean_effects": 0,
                "attached_pic": 0,
                "timed_thumbnails": 0,
                "captions": 0,
                "descriptions": 0,
                "metadata": 0,
                "dependent": 0,
                "still_image": 0
            },
            "tags": {
                "language": "bul",
                "DURATION": "00:00:10.614000000"
            }
        }
    ],
    "chapters": [
        {
            "id": 1,
            "time_base": "1/1000000000",
            "start": 0,
            "start_time": "0.000000",
            "end": 10000000000,
            "end_time": "10.000000",
            "tags": {
                "title": "Chapter 1"
            }
        }
    ],
    "format": {
        "filename": "TEST_FILE.mkv",
        "nb_streams": 3,
        "nb_programs": 0,
        "format_name": "matroska,webm",
        "format_long_name": "Matroska / WebM",
        "start_time": "0.000000",
        "duration": "10.614000",
        "size": "1280059",
        "bit_rate": "964807",
        "probe_score": 100,
        "tags": {
            "ENCODER": "Lavf59.27.100"
        }
    }
}
  ```
</details>

---

## Using the `StreamMapper` class

The StreamMapper class is used to simplify building a ffmpeg command. It uses a previously initialised probe object as an input and uses it to define stream mapping from the input file to the output.

This class should be extended with a child class to configure it and implement the custom functions required to manage streams that will need to be processed.

```python
class PluginStreamMapper(StreamMapper):
    def __init__(self):
        super(PluginStreamMapper, self).__init__(logger, ['video'])
        self.settings = None

    def set_settings(self, settings):
        self.settings = settings

    def test_stream_needs_processing(self, stream_info: dict):
        """
        Run through a set of test against the given stream_info.

        Return 'True' if it needs to be process.
        Return 'False' if it should just be copied over to the new file.

        :param stream_info:
        :return: bool
        """
        if stream_info.get('codec_name').lower() in ['h264']:
            return False
        return True

    def custom_stream_mapping(self, stream_info: dict, stream_id: int):
        """
        Will be provided with stream_info and the stream_id of a stream that has been 
        determined to need processing by the `test_stream_needs_processing` function.

        Use this function to `-map` (select) an input stream to be included in the output file
        and apply a `-c` (codec) selection and encoder arguments to the command.

        This function must return a dictionary containing 2 key values:
            {
                'stream_mapping': [],
                'stream_encoding': [],
            }
        
        Where:
            - 'stream_mapping' is a list of arguments for input streams to map. Eg. ['-map', '0:v:1']
            - 'stream_encoding' is a list of encoder arguments. Eg. ['-c:v:1', 'libx264', '-preset', 'slow']


        :param stream_info:
        :param stream_id:
        :return: dict
        """
        if self.settings.get_setting('advanced'):
            stream_encoding = ['-c:v:{}'.format(stream_id), 'libx264']
            stream_encoding += self.settings.get_setting('custom_options').split()
        else:
            stream_encoding = [
                '-c:v:{}'.format(stream_id), 'libx264',
                '-preset', str(self.settings.get_setting('preset')),
                '-crf', str(self.settings.get_setting('crf')),
            ]

        return {
            'stream_mapping':  ['-map', '0:v:{}'.format(stream_id)],
            'stream_encoding': stream_encoding,
        }
```

Once you have created your stream mapper class, you can use it to determine if a file needs a FFmpeg command executed against it using its `streams_need_processing` function.

```python
def on_library_management_file_test(data):

    ...

    # Get plugin settings
    settings = Settings(library_id=data.get('library_id'))

    # Get file probe
    probe = Probe.init_probe(data, logger, allowed_mimetypes=['audio'])
    if not probe:
        # File not able to be probed by FFprobe. The file is probably not a audio/video file.
        return

    # Get stream mapper
    mapper = PluginStreamMapper()
    mapper.set_settings(settings)
    mapper.set_probe(probe)

    # Check if file needs a FFmpeg command run against it
    if mapper.streams_need_processing():
        # Mark this file to be added to the pending tasks
        data['add_file_to_pending_tasks'] = True


def on_worker_process(data):

    ...

    # Get plugin settings
    settings = Settings(library_id=data.get('library_id'))

    # Get file probe
    probe = Probe.init_probe(data, logger, allowed_mimetypes=['audio'])
    if not probe:
        # File not able to be probed by FFprobe. The file is probably not a audio/video file.
        return

    # Get stream mapper
    mapper = PluginStreamMapper()
    mapper.set_settings(settings)
    mapper.set_probe(probe)

    # Check if file needs a FFmpeg command run against it
    if mapper.streams_need_processing():

        """
        HERE: Configure FFmpeg command args as required for this plugin
        """

        # Set the input and output file
        mapper.set_input_file(data.get('file_in'))
        mapper.set_output_file(data.get('file_out'))

        # Get final generated FFmpeg args
        ffmpeg_args = mapper.get_ffmpeg_args()

        # Apply FFmpeg args to command for Unmanic to execute
        data['exec_command'] = ['ffmpeg']
        data['exec_command'] += ffmpeg_args

```

---

## Using the `Parser` class

Unmanic has the ability to execute a command provided by a plugin and display a output of that command's progress. As Unmanic is able to execute any command a plugin provides it, we need a way

This progress is only possible if the provided command is accompanied with a progress parser function. If such a function is not provided to Unmanic, then the command will still be executed, but the Unmanic worker will only report an indeterminate progress status with the logs.

This python module provides a function for parsing the output of a FFmpeg command to determine progress of that command's execution.

This should be returned with the built command in the `on_worker_process` plugin function:


```python
def on_worker_process(data):

    ...

    # Get file probe
    probe = Probe.init_probe(data, logger, allowed_mimetypes=['audio'])
    if not probe:
        # File not able to be probed by FFprobe. The file is probably not a audio/video file.
        return

    # Set the parser
    parser = Parser(logger)
    parser.set_probe(probe)
    data['command_progress_parser'] = parser.parse_progress
```

---

## Examples
For examples of how to use this module, see these plugin sources:
- [Limit Library Search by FFprobe Data](https://github.com/Unmanic/plugin.limit_library_search_by_ffprobe_data/blob/master/plugin.py)
- [Re-order audio streams by language](https://github.com/Unmanic/plugin.reorder_audio_streams_by_language/blob/master/plugin.py)
- [Transcode Video Files](https://github.com/Unmanic/plugin.video_transcoder/blob/master/plugin.py)
