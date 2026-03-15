
This Plugin will automatically manage bitrate for you. 

- If the source stream bitrate is equal or less than 768kb/s, the bitrate will be set to 448k
- If the source stream bitrate is greater than 768kb/s, the bitrate will be set to 640k (max value for encoder)

:::note
The FFmpeg AC3 encoder is not able to encode more than 6 channels.
:::

---

### Config description:

#### <span style="color:blue">Downmix DTS-HD Master Audio (max 6 channels)?</span>
When this is selected, DTS-HD Master Audio streams will be left untouched.

DTS-HD Master Audio contains more than 6 channels which is not supported by FFmpeg.

To transcode this you will need a commercial encoder.
