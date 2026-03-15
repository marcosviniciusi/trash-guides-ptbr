**3.3.1** - Handle all subtitle codecs
- CHANGED: classify_subtitle now applies to ALL subtitle codecs regardless of type
- REMOVED: TEXT_SUBTITLE_CODECS, BITMAP_SUBTITLE_CODECS, ALL_SUBTITLE_CODECS constants
- CHANGED: codec parameter removed from classify_subtitle (lang-only decision)

**3.3.1** - Remove untagged subtitle streams
- CHANGED: Streams without language tag are now removed (previously kept as potential PT-BR)
- Only streams explicitly tagged as PT-BR variants are kept

**3.3.0** - Simplified: keep PT-BR as-is, remove the rest
- CHANGED: No more extraction of EN/audio-lang subtitles to .srt
- CHANGED: No more ASS/SSA -> SRT conversion
- CHANGED: No more language tagging of untagged streams
- CHANGED: PT-BR subtitles kept via framework default copy path (no custom encoding)
- REMOVED: `subprocess` dependency (no extraction phase)
- REMOVED: `is_english`, `is_audio_language`, `get_audio_languages`, `build_subtitle_tag` helpers
- Logic: classify_subtitle() now returns only 'embed' or 'remove'

**3.2.3** - Add bitmap subtitle support (VobSub/DVD)
- NEW: Added BITMAP_SUBTITLE_CODECS covering dvd_subtitle/dvdsub/xsub in addition to PGS
- NEW: classify_subtitle handles bitmap formats first — keeps PT-BR, removes everything else

**3.2.1** - Rewritten to use StreamMapper (same pattern as official plugins)
- CHANGED: Worker now uses StreamMapper.get_ffmpeg_args() instead of manual arg building
- FIX: Unmanic should now properly handle the output file movement

**3.2.0** - New subtitle logic + extraction
- CHANGED: PT-BR subtitles are the ONLY ones kept embedded in the MKV
- NEW: EN and audio-language subtitles extracted as external .srt files

**3.1.0** - Major rewrite fixing all bugs
- FIX: Removed dependency on StreamMapper for worker process
- FIX: SSA subtitles now properly converted to SRT
- FIX: Output subtitle indices tracked separately from input

**3.0.4** - Initial release
