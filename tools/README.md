# Miya's Lab pipeline tools

Script (English narration) -> narration wavs -> render folder -> GitHub Actions render -> Google Drive.
All paths come from `tools/paths.py`. Set `SLUG=<video-slug>` (and optionally `MIYA_WORK=<scratch dir>`, default `/tmp/miya-work`).

Per video you need `videos/<slug>/`:
- `script.py` — `SCENES = [(id, chapter title, "ill"|"chalk", art id, narration), ...]`
- `art/<art id>.svg` — one 1920x1080 SVG per scene (spec: `tools/art_spec.md`; movable parts as `id="mv-name"` groups)
- `config.py` — `CHALK`, `WHOOSH`, `TITLE`, `DESC`, `CHAPTERS`, `SOURCES`, `HASHTAGS` (see the existing one)
- `thumb/A.html`, `thumb/B.html`, `thumb/common.css`, `thumb/Fredoka-700.woff2` — two original thumbnails

Steps (run from the repo root):
1. `SLUG=x HYPERFRAMES_PYTHON=<venv python> tools/tts.sh` — Kokoro am_michael, one wav per scene.
   The venv held `kokoro-onnx 0.6.1, soundfile, onnxruntime, phonemizer, espeakng-loader, numpy`.
   Setting it up from scratch was not re-tested.
2. `SLUG=x python3 tools/audio_prep.py` — stereo, loudnorm -16.8 LUFS, per-scene clips, timing.
3. (new look, current) `SLUG=x PLAN=1 python3 tools/build3.py` -> plan.json; draw `art3/<uid>.svg+json` per unit (tools/art_spec_v3.md); `SLUG=x python3 tools/build3.py` (`VERT=1` for Shorts). Old flow: `SLUG=x python3 tools/build.py` — writes `render/x/` (index.html, audio as m4a, assets). `SEL=1,2,16` builds a partial test.
4. `SLUG=x python3 tools/thumb_shot.py` — thumbnails into `render/x/deliver/`.
5. `SLUG=x python3 tools/gen_text.py` — script txt and metadata txt into `render/x/deliver/`.
6. `echo x > render/.slug`, commit, push to `render-pipeline` — the Actions workflow renders and uploads to Drive.

Check: with the saved TTS wavs, steps 2-3 reproduce `render/never-eat-human-meat/index.html` byte for byte.
