# Transcode Video Files
Plugin for [Unmanic](https://github.com/Unmanic)

---

## Supported Hardware Encoders

This plugin supports the following hardware-accelerated video encoders:

- **LibX** (CPU - Software encoders)
  - libx264 (H.264)
  - libx265 (HEVC/H.265)
  - libsvtav1 (AV1)

- **Intel Quick Sync Video (QSV)**
  - H.264, HEVC, AV1
  - Requires Intel CPU with Quick Sync support

- **NVIDIA NVENC**
  - H.264, HEVC
  - Requires NVIDIA GPU (Kepler or newer)

- **AMD/Intel VAAPI**
  - H.264, HEVC
  - Requires compatible AMD or Intel GPU on Linux

- **Apple VideoToolbox** ✨ NEW
  - H.264, HEVC
  - Requires macOS with Apple Silicon (M1/M2/M3/M4) or Intel Mac (2017+)
  - Automatic HDR10 metadata preservation for HEVC
  - VBV rate control support for streaming-optimized encodes

---

## Apple VideoToolbox Features

### Quality Control
- Quality scale: 0-100 (higher = better quality)
- Recommended defaults:
  - H.264: 50 (≈ libx264 crf=23)
  - HEVC: 65 (≈ libx265 crf=28)

### VBV Rate Control (Optional)
- **Maximum bitrate**: Limits bitrate spikes for streaming
- **Buffer size**: Rate control buffer (typically 2x maxrate)
- Example Netflix-style 720p: maxrate=3800k, bufsize=7600k

### Performance
- 10-20x faster than software encoding on Apple Silicon
- Power efficient encoding with minimal battery impact
- Note: File sizes may be 20-30% larger than QSV/NVENC at equivalent quality

### HDR Support
- Automatic HDR10 metadata preservation for HEVC
- Supports both 8-bit and 10-bit encoding
- Profile selection: auto, baseline, main, high (H.264), main10 (HEVC)

---

### Information:

- [Description](description.md)
- [Changelog](changelog.md)

---

### Credits

- Original plugin: Josh.5
- VideoToolbox support: Marcos Gabriel
