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
3. (new look, current) `SLUG=x PLAN=1 python3 tools/build3.py` -> plan.json; draw `art3/<uid>.svg+json` per unit (tools/art_spec.md, incl. the on-screen text `labels` checked/previewed with `python3 tools/labelshot.py <slug> <dir> <uid...>`; the spec says: NO rings/radiating lines — every picture needs a scene-specific backdrop, see tools/art_spec.md section 5, appendix A is the brief for revising existing pictures; at most 2 of 12 units may share a backdrop kind); `SLUG=x python3 tools/build3.py` (`VERT=1` for Shorts). Old flow: `SLUG=x python3 tools/build.py` — writes `render/x/` (index.html, audio as m4a, assets). `SEL=1,2,16` builds a partial test.
4. `SLUG=x python3 tools/thumb_shot.py` — thumbnails into `render/x/deliver/`.
5. `SLUG=x python3 tools/gen_text.py` — script txt and metadata txt into `render/x/deliver/`.
6. Shorts: same steps with slug `x-short` (`VERT=1` for build3; no thumbnails; `gen_text.py` writes title/description/hashtags because `CHAPTERS=[]`). Shorts art is vertical (`art_spec.md` section 10).
7. (The workflow reads slugs through fd 3 because npx/ffmpeg inside the loop otherwise swallow the remaining slug lines — this made the first run skip the long video.) Write both slugs to `render/.slug`, one per line (`x` then `x-short`), commit, push to `render-pipeline`. The workflow renders each slug in turn and uploads to Drive: long -> `x/`, Shorts -> `x/short/`.
   - `render/<slug>/.dest` (one line) overrides the Drive folder (e.g. `x/short`) when the slug name does not follow `<long>-short`.
   - A slug folder containing an empty file `.deliver_only` skips the render and only uploads `deliver/` (use to re-upload thumbnails/text).

Check: with the saved TTS wavs, steps 2-3 reproduce `render/never-eat-human-meat/index.html` byte for byte.

## 2026-10-10 additions
- `sfx_lib.py` v2: 25 quiet unpitched sounds x 3 variants (peak -24 dBFS). Old name `shimmer` is an alias of `hush`. Sidecar `sfx.name` list is in `art_spec.md` section 8.
- `bgm_lib.py`: synthesised background music (own composition, no samples/vocals), highpass 250 Hz, ducked under the real narration (`n##.wav`), 13 dB below narration RMS (`BGM_BELOW`). `build3.py` writes `bgm.m4a` and adds it as audio track 20. `NOBGM=1` disables it.
- Two Shorts per video: slugs `<slug>-short1`, `<slug>-short2` (also `-short`); the workflow uploads them to `<slug>/short/`. Put all three slugs in `render/.slug`.

## 2026-10-10 (epomis-frog-hunter-v2)
- Kokoro speed re-measured at ~163 words/min (not 126): plan ~3,100 words for a ~20 min video. Always check `audio_prep.py`'s total.
- `build3.py`: very short units (<1.6 s) merge into a neighbour; a short last unit re-splits with the previous one. A partial `SEL=` build now takes picture uids from `plan.json` (before, numbering restarted at 1 and pictures were mismatched).
- Picture agents: write a per-video `videos/<slug>/art_brief.md` (character sheet, own scratch folder per agent) and give it to every agent.
- Workflow: Chrome warm-up, one render retry, continue with the next slug on failure.
- Guideline copy: `docs/miyas-lab-guideline.md`.

## Palettes (2026-10-10)
- `palettes.py`: 10 topic palettes (ocean, forest, desert, ice, lab, history, space, storm, body, sunset). New video: set `PAL_DEFAULT` and optionally `PAL = {art_theme: palette}` in `config.py`, chosen from what the script is about (max 3 palettes per video). `build3.py PLAN=1` writes the chosen colours into every plan.json unit (`pal`) and the transition wash uses the scene's palette. Without `PAL_DEFAULT` the old purple/peach look (palette `sunset`) is used and PLAN=1 prints a warning.
- Picture agents must use only `pal` colours (see art_spec.md section 3). Existing videos (`epomis-frog-hunter-v2`, `never-eat-human-meat-v4`) were drawn with the old colours and are NOT changed.

## 우주 모드 (2026-10-12)
- `config.py`: `STYLE = 'cosmic'`, `PAL_DEFAULT = 'nebula'|'aurora'|'deepfield'|'solar'`. 그림 명세는 `art_spec.md` 11절.
- 효과음 6종 추가(`sfx_lib.COSMIC`, riser·sweep는 파도 소리 같다는 지적으로 삭제), 배경음악은 `STYLE='cosmic'`이면 `bgm_lib.synth_cosmic`(코드 변경 12초, 3중 디튠 패드, 느린 고음 아르페지오, 지연 에코, 저역통과 6.5kHz).
- 확인: 합성과 주파수 분석만(150Hz 미만 에너지 비율 0.001 안팎). 실제 렌더·소리 판단은 안 함.

## Centre-object motions (2026-10-13)
- `motions.py`: 19 motion types for the round centre object (`mv-core-<type>`: spin, sway, orbit, glide, heartbeat, flicker, swell, tremble, approach, reveal, squeeze, wobble, roll, and from a motion-graphics reference: pop, ping, stamp, flip, draw, drop). The old `mv-glint-core` is auto-assigned a type by rotation (neighbouring pictures never match). `build3.py` prints the types used and warns if fewer than 10 are used, the same type repeats in a row, or one type is over 20%. Light groups (`glint`, `lamp`, `lantern`, `beacon`) now pulse in place instead of stretching vertically. Tested in headless Chromium only (seek-safe, per-type change); not yet seen in a rendered MP4.
- `restyle_motion.py`: re-styles the centre motion of an already built `render/<slug>/index.html` in place (no TTS, no pictures needed): `python3 tools/restyle_motion.py render/<slug> ...`. Idempotent. Tested on `whale-fall-short1` only (page loads, 13 centre motions replaced, pictures unchanged before the motion starts).
- 2026-10-13 from a motion-graphics reference: number badges count up from 0 (`labels_lib.count_span/count_js`, seek-safe `innerText` tween with a formatting modifier, years 1000-2100 skipped); focus spotlight `#sp<n>` dims the picture around the focus point while the camera pushes in (sidecar `"spot": false` turns it off); `ping`/`stamp` use a ring drawn by `miyaWrapCores`, `draw` uses stroke lengths measured there.
- 2026-10-13: `caption_hl.py` — the spoken subtitle word turns yellow (#ffd54a); word times split the line's speaking window by word length. `motions.CHALK_FIT_JS` — chalkboard card values stay on one line and shrink to fit (they used to wrap and spill out of the 140 px card). `restyle_motion.py` now also applies chalk fit, badge count-up, focus spotlight and the subtitle highlight; run it on the original build output only.
- 2026-10-13: the six picture specs were merged into `tools/art_spec.md` (sections 1-9 landscape, 10 Shorts, 11 cosmic, appendix A backdrop revision, appendix B retired v1 look). Record of repo changes: `docs/repo-changes.md`.
