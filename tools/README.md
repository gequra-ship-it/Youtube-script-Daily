# Miya's Lab pipeline tools (cine look)

Script (English narration) -> Kokoro narration -> units, captions, SFX, music -> 3D page (Three.js) -> GitHub Actions chunked render -> Google Drive.
Rules: `docs/miyas-lab-guideline.md`. Scene spec for agents: `tools/cine_spec.md`.
All paths come from `tools/paths.py`. Set `SLUG=<video-slug>` and `MIYA_WORK=<scratch dir>` (default `/tmp/miya-work`). Run from the repo root.

## Per video: `videos/<slug>/`
- `script.py` — `SCENES = [(id, chapter title, "ill", theme, narration paragraph), ...]` (one paragraph = one scene)
- `config.py` — `PAL_DEFAULT` (palette, `palettes.py`), optional `STYLE = 'cosmic'`, `CHALK` (data cards, guideline chapter 6), `TITLE`, `DESC`, `CHAPTERS`, `SOURCES`, `HASHTAGS`
- `cine.json` — chapters (`stage` / `cuts`), scene params with word cues, beats per unit (`cine_spec.md` section 2)
- `scenes/*.js` — new 3D scenes for this video (library: `tools/cine/scenes/`)
- Example: `videos/whale-fall-cine/` (one stage chapter with the `whale` scene), `videos/stolen-time/cine.json` (stage + cuts)

## Steps
1. `SLUG=x HYPERFRAMES_PYTHON=<venv python> bash tools/tts.sh` — Kokoro `am_michael`, one wav per scene in `<work>/x/tts/`.
   Venv: `python3 -m venv <dir> && <dir>/bin/pip install kokoro-onnx soundfile`.
2. `SLUG=x python3 tools/audio_prep.py` — stereo 48 kHz, loudnorm −16.8 LUFS, per-scene clips, scene lengths.
3. `SLUG=x PLAN=1 python3 tools/build_audio.py` — unit split -> `videos/x/plan.json` (uid, text, duration).
4. Write `videos/x/cine.json` (+ `videos/x/scenes/*.js`).
5. `SLUG=x python3 tools/build_audio.py` — captions, SFX cues (from the transitions in cine.json, chalk taps for data cards), music, one pre-mixed `render/x/mix.m4a`, `<work>/x/build/build_data.json`. `SEL=1,2` partial, `VERT=1` Shorts, `NOBGM=1`, `BGM_BELOW=13`.
6. `SLUG=x python3 tools/build_cine.py` — writes `render/x/` (index.html with `window.CINE`, `cine.js`, `cine.css`, `kit.js`, scene files, Three.js r169, GSAP, fonts Lora/Inter (OFL), logo). Checks cues, gaps, unknown scene types. `CINE_JSON=<file>` for a test layout, `SEL=` with a partial build_data, `VERT=1`.
7. `python3 tools/cineshot.py render/x <outdir> 5 30 61.2 ...` — screenshots, seconds per frame, page errors. `python3 tools/cineshot.py render/x --estimate` — chunk count.
8. `SLUG=x python3 tools/gen_text.py` — `<slug>_script.txt` and `<slug>_metadata.txt` into `render/x/deliver/`. Thumbnails: `videos/x/thumb/A.html`, `B.html` -> `SLUG=x python3 tools/thumb_shot.py` -> `render/x/deliver/`.
9. `render/x/.dest` (Drive folder), then a line `x <chunks>` in `render/.chunked`, push to `render-pipeline` -> `.github/workflows/render-chunked.yml`: one job per chunk (`tools/chunk_prep.py` makes a chunk page that seeks the main timeline from its start, audio removed), concat without re-encoding, `mix.m4a` muxed once, report, Drive upload (`.dest`, `.outname`, `deliver/`, `.skip_deliver`).

## Files
| file | what |
|---|---|
| `tts.sh`, `audio_prep.py` | narration |
| `build_audio.py` | units, captions, SFX, music, mix, build_data |
| `sfx_lib.py`, `bgm_lib.py` | synthesised SFX (25 + 6 cosmic, 3 variants each, peak −24 dBFS) and music (ducked 13 dB under the narration) |
| `caption_hl.py` | word times for the spoken-word highlight |
| `palettes.py` | topic palettes (blinds transition tones) |
| `build_cine.py` | the 3D page |
| `cine/cine.js`, `cine/cine.css` | runtime: renderer, compositor + transitions, HUD/text layers, data cards, captions |
| `cine/kit.js` | realism kit: noise, normal maps, `body()` one-mesh organisms (+ `extra` merged parts), `fin()`, god rays, marine snow, water surface from below |
| `cine/scenes/` | library: dataglobe, blackhole (4 looks), ocean, clockfield, whale, watch, river, cubefield (heavy), void |
| `cine/assets/` | three.js r169 (classic-script wrap), room-env.js, gsap, fonts + licences |
| `cineshot.py` | screenshots / cost estimate |
| `chunk_prep.py` | chunk pages for the parallel render |
| `gen_text.py`, `thumb_shot.py` | script/metadata text, thumbnail capture |
| `assets/` | `logo.png`, `Fredoka-700.woff2` (thumbnail text) |
| `paths.py` | shared paths and loaders |

The retired SVG pipeline (build3.py/build.py, art_spec.md, label/motion tools, render.yml) is in git history (commit `ff7818b`).
