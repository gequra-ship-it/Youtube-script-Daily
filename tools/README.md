# Miya's Note pipeline tools

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
2b. `SLUG=x python3 tools/align.py` — word times of the narration (faster-whisper small.en, CPU, ~4 min per 45 paragraphs) into `build/words.json`; build3 uses them for captions, cuts, sfx. Required before build3 (it stops when a paragraph matches < 90 % of its words). Needs `pip install faster-whisper`.
3. (new look, current) `SLUG=x PLAN=1 python3 tools/build3.py` -> plan.json; draw `art3/<uid>.svg+json` per unit (tools/art_spec.md, incl. the on-screen text `labels` checked/previewed with `python3 tools/labelshot.py <slug> <dir> <uid...>`; the spec says: NO rings/radiating lines — every picture needs a scene-specific backdrop, see tools/art_spec.md section 5, appendix A is the brief for revising existing pictures; at most 2 of 12 units may share a backdrop kind); `SLUG=x python3 tools/build3.py` (`VERT=1` for Shorts). Old flow: `SLUG=x python3 tools/build.py` — writes `render/x/` (index.html, audio as m4a, assets). `SEL=1,2,16` builds a partial test.
4. Thumbnails (guideline 16-6/16-7): an **Opus agent** (brief `tools/briefs/thumb_art.md`) writes `videos/<slug>/thumb/{A,B,C}.html` with a generator `make.py` using `tools/thumb_lib.py` (`page`, `svg`, `lin`, `rad`, `stars`, `spark`, `blobs`) and `tools/hands.py`; then `SLUG=x python3 tools/thumb_shot.py` -> `render/x/deliver/x_thumbnail_A..F.png` (A-C always, D-F only if the html exists). To upload only the thumbnails: `render/<slug>/.deliver_only` + `render/.slug` (see 16-7).
5. `SLUG=x python3 tools/gen_text.py` — script txt and metadata txt into `render/x/deliver/`.
6. Shorts: same steps with slug `x-short` (`VERT=1` for build3; no thumbnails; `gen_text.py` writes title/description/hashtags because `CHAPTERS=[]`). Shorts art is vertical (`art_spec.md` section 10).
7. (The workflow reads slugs through fd 3 because npx/ffmpeg inside the loop otherwise swallow the remaining slug lines — this made the first run skip the long video.) Write both slugs to `render/.slug`, one per line (`x` then `x-short`), commit, push to `render-pipeline`. The workflow renders each slug in turn and uploads to Drive: long -> `x/`, Shorts -> `x/short/`.
   - `render/<slug>/.dest` (one line) overrides the Drive folder (e.g. `x/short`) when the slug name does not follow `<long>-short`.
   - A slug folder containing an empty file `.deliver_only` skips the render and only uploads `deliver/` (use to re-upload thumbnails/text).

Check: with the saved TTS wavs, steps 2-3 reproduced the first video's `render/never-eat-human-meat/index.html` byte for byte (that render folder was deleted 2026-10-14; it is in git history).

## 2026-10-10 additions
- `sfx_lib.py` v2: 25 quiet unpitched sounds x 3 variants (peak -24 dBFS). Old name `shimmer` is an alias of `hush`. Sidecar `sfx.name` list is in `art_spec.md` section 8.
- `bgm_lib.py`: synthesised background music (own composition, no samples/vocals), highpass 250 Hz, ducked under the real narration (`n##.wav`), 13 dB below narration RMS (`BGM_BELOW`). `build3.py` writes `bgm.m4a` and adds it as audio track 20. `NOBGM=1` disables it.
- Two Shorts per video: slugs `<slug>-short1`, `<slug>-short2` (also `-short`); the workflow uploads them to `<slug>/short/`. Put all three slugs in `render/.slug`.

## 2026-10-10 (epomis-frog-hunter-v2)
- Kokoro speed re-measured at ~163 words/min (not 126): plan ~2,200 words (2,000-2,300) for a video of at most 15 min (since 2026-10-24; was 3,450 for 20+ min). Always check `audio_prep.py`'s total.
- `build3.py`: very short units (<1.6 s) merge into a neighbour; a short last unit re-splits with the previous one. A partial `SEL=` build now takes picture uids from `plan.json` (before, numbering restarted at 1 and pictures were mismatched).
- `body.py` (2026-10-17): human proportions in head heights + `arm()` (2-link `mv-limb` arm with a hands.py hand; art_spec 6B); `python3 tools/body.py out.svg` draws the reference sheet. build3 animates `mv-limb-*` gently and in step.
- `hands.py` (2026-10-17): anatomically sane hands for every picture (art_spec 6A); `python3 tools/hands.py out.svg` draws a test sheet.
- `build3.py` transitions (2026-10-14): 11 types (blinds removed 2026-10-16, user decision) — zoom, fade, slide, match, wash, plus wipe (diagonal with a light edge), iris (circle from a side subject; sidecar `iris`), eye (opens from a horizontal line), push (vertical), whip (fast pass with speed streaks), tilt (card tips in). `TR_WORDS` picks one from words in the unit text (50 %, unless that type is over its share); other picks are weighted against types already used a lot; never the same type twice in a row; hard cuts around chalkboards.
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

## 3D (cine) — 보관
3D 도구와 명세는 `cine-test/`로 옮겼다(`cine-test/README.md`). `chunk_prep.py`(구간 나누기)는 SVG 병렬 렌더에도 쓰므로 여기에 남아 있다.

## 2026-10-16 추가 (지침서 20장)
- `remake.py`: 기존 영상 다시 만들기(지침서 21장). `SLUG=x python3 tools/remake.py` → 예전 plan 보관, 다시 나누기, `remap_art.py`로 그림 재연결, `NO ART`/`NEEDS VARIANT` 단위 출력, `.dest`·`.skip_deliver` 점검. 에이전트 지시문은 `briefs/remake_art.md`(재사용), `briefs/people_restyle.md`(사람 ③ 스타일).
- `build3.py`: **`PACE = 1.5`(2026-10-22)**: `maxu`·`slow`·`minu`·`minu_slow`(기본값과 `config.py`의 `HOOK` 모두)에 곱해진다(최소 6.0초, 최대 9.3초). `config.py`에 `PACE = 1`이면 예전 길이. 아래 수치는 PACE 1.0 기준. `HOOK`이 없으면 기본값(2026-10-17: 롱폼 `until=300, maxu=5.5`, 숏츠 `until=999, maxu=6.0, slow=7.5`; `HOOK = None`이면 예전 나누기). 예전 시험값 `HOOK = dict(until=300, maxu=4.5)`(숏츠 `until=999, maxu=4.8`; 컷 시점을 옮겨 그림마다 최소 3.5초 `minu`, 느린 문단 4.5초 `minu_slow`, 그림은 버리지 않음; 설명·숫자 장면은 자동으로 느리게, `SLOW`/`NOT_SLOW`로 조정), `tools/remap_art.py`(다시 나눈 뒤 예전 그림 연결), `DRIFT = False`(드리프트 카메라 끄기). 우주 모드는 속도 단어가 있는 단위에 속도선(사이드카 `"speed": true/false`).
- `motion_check.py render/<slug> [--step 6]`: 화면이 거의 안 움직이는 구간을 찾는다(SVG·3D 페이지 모두).
- `art3` 관절: `mv-joint-<이름>`(관절 하나, `data-pivot`·`data-amp`·`data-per`·`data-phase`), `mv-chain-<이름>-1,-2…`(겹쳐 넣은 마디 사슬, 끝으로 갈수록 크게·늦게). `tools/art_spec.md` 7절.
- 병렬 렌더: `chunk_plan.py render/<slug>`로 구간 수 → `render/.chunked`에 `"<slug> <n>"` → `render-chunked.yml`(+`chunk_prep.py`). 지침서 20-7.
- 3D(cine) 도구는 `cine-test/`에 보관(`build_cine.py`, `build_audio.py`, `cineshot.py`, `cine/`).
- `mv-rotor-<이름>`(2026-10-19): 부분이 `data-pivot` 둘레를 계속 도는 모션(시계 바늘·바람개비·플라스마 고리, `data-per` 한 바퀴 초, `data-dir` ±1). 코어 타입 `turn` = 그 그룹만 회전(이웃 안 묶음, 풍차 날개). 움직이는 부분이 있는 물체에 전체 회전 코어 모션 금지(지침서 4-1).

## 2026-10-22 additions (motion test, user decision)
- `motions.py`: 5 new transitions `seam` (line drawn from bottom-left to top-right, then it opens into a diagonal band), `diamond`, `page`, `zigzag`, `wave` (`NEW_TR`, `tr_js`, `miyaTr` driven by a modifier-based proxy tween so it is seek-safe) and 12 position-free object motions (`OBJ_KINDS`, `obj_js`: path, flip, fill, grow, swing, topple, liquid, bubble, edge, keyturn, shackle, popin). `build3.py` adds them to the transition pool (16 types now), sounds (`TRSND`), the `#trfx` overlay, the page-fold exit, and parses `data-*` of the new `mv-<kind>-<name>` groups. Tested only in a headless-Chromium harness (seek at several times, all five transitions and every motion kind); not yet seen in a full MP4 render.
- The 20 s test video (8 scenes, v8) and its source are in the project files, `motion-demo/`.

## 2026-10-22 additions (title lint)
`python3 tools/title_lint.py --title "..." [--thumb "..."]` checks a title/thumbnail text pair against guideline 16-6 and 17-3 (advisory). Adapted from Jakeschincariol/youtube-agent-skill (MIT).
- 2026-10-22 (later): 5 more object motions (`shake`, `dash`, `scroll`, `slam`, `rise`), camera tracking (`track_spec`, `track_js`, `miyaTrack`: follows `mv-path`, 3+ `mv-topple`, or `mv-track-*`; replaces focus/drift; build log `tracking cams`), speech bubbles up to 2 per unit (`labels_lib.py`) and ~1 unit in 3 (guideline 3-6).

## 2026-10-24 additions (bear demo v3, user decision)
- `motions.py`: object kinds `slide`, `fade`, `ticks`, `rack` (+ `popin` `data-axis`), `miyaTicks`/`miyaRack`; `miyaTrack`/`track_js` take the world size (sidecar `"world": [w, h]`) so the camera can travel or scroll over one big picture.
- `rhythm.py` (new): `silence_windows`, `accent_times`, `gain_mask`; `build3.py` mutes music + sfx in two near-silences (config `SILENCE`, env `NOSILENCE=1`) and `bgm_lib.synth(accents=)` adds chord-tone accents on big scene changes (env `NOACCENT=1`). Guideline 9-5.
- `paths.chrome()`: finds the installed Chromium (env `HYPERFRAMES_BROWSER_PATH`/`PW_CHROME`/`CHROME`, else newest `/opt/pw-browsers/chromium-*`); six preview tools use it.
- Checked on a 4-scene test video (TTS, align, build, seek screenshots). Not checked: full MP4 render, sound by ear.
