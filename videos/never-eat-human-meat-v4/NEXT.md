# never-eat-human-meat-v4 — status and next steps (2026-10-10)

Done: fact-checked script (2,956 words, 36 scenes, 4 chalkboards), config, Kokoro TTS for long + 2 Shorts (saved as `tts/p##.flac`),
plan.json for all three (long: 263 pictures, 20:56; short1: 14 pictures, 62.2 s; short2: 12 pictures, 59.3 s), art_brief.md.
Kokoro read this script at ~145 words/min (epomis: ~163) — speed varies, always measure.

Next (when usage allows):
1. Restore audio: for each slug, `mkdir -p $MIYA_WORK/<slug>/tts && for f in videos/<slug>/tts/*.flac; do ffmpeg -y -i $f $MIYA_WORK/<slug>/tts/$(basename ${f%.flac}).wav; done`,
   then `SLUG=<slug> python3 tools/audio_prep.py` (check total: 1242.63 / 61.18 / 58.3 s).
2. Pictures: agents with `videos/never-eat-human-meat-v4/art_brief.md` (10-20 units each, by scene); Shorts vertical.
3. Thumbnails A/B (new look, different hooks from the Shorts titles).
4. `build3.py` (VERT=1 for Shorts), test-render a SEL part, `gen_text.py`, write the three slugs to `render/.slug`, push.
