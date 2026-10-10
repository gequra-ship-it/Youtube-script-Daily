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
3. (new look, current) `SLUG=x PLAN=1 python3 tools/build3.py` -> plan.json; draw `art3/<uid>.svg+json` per unit (tools/art_spec_v3.md; v3 and v2 both say: NO rings/radiating lines — every picture needs a scene-specific backdrop, see tools/art_spec_v4_backdrop.md, which is also the brief for revising existing pictures; at most 2 of 12 units may share a backdrop kind); `SLUG=x python3 tools/build3.py` (`VERT=1` for Shorts). Old flow: `SLUG=x python3 tools/build.py` — writes `render/x/` (index.html, audio as m4a, assets). `SEL=1,2,16` builds a partial test.
4. `SLUG=x python3 tools/thumb_shot.py` — thumbnails into `render/x/deliver/`.
5. `SLUG=x python3 tools/gen_text.py` — script txt and metadata txt into `render/x/deliver/`.
6. Shorts: same steps with slug `x-short` (`VERT=1` for build3; no thumbnails; `gen_text.py` writes title/description/hashtags because `CHAPTERS=[]`). Shorts art is vertical (`art_spec_v3_vertical.md`).
7. (The workflow reads slugs through fd 3 because npx/ffmpeg inside the loop otherwise swallow the remaining slug lines — this made the first run skip the long video.) Write both slugs to `render/.slug`, one per line (`x` then `x-short`), commit, push to `render-pipeline`. The workflow renders each slug in turn and uploads to Drive: long -> `x/`, Shorts -> `x/short/`.
   - `render/<slug>/.dest` (one line) overrides the Drive folder (e.g. `x/short`) when the slug name does not follow `<long>-short`.
   - A slug folder containing an empty file `.deliver_only` skips the render and only uploads `deliver/` (use to re-upload thumbnails/text).

Check: with the saved TTS wavs, steps 2-3 reproduce `render/never-eat-human-meat/index.html` byte for byte.
