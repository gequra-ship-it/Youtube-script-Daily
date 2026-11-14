# Miya's Note pipeline tools

> Last updated: 2026-11-14 · The body holds only what is true now. How things changed is in "History" at the bottom. Rules live in the guideline (`docs/miyas-lab-guideline.md`); this file says which tool does what.

Script (English narration) → narration wavs → pictures → render folder → GitHub Actions render → Google Drive.

## 1. Layout

| Folder | What | Files |
|---|---|---|
| `tools/` | importable libraries + `chunk_prep.py` (called by the render workflow, do not move) | `paths motions frog frog_rig fxlib labels_lib sfx_lib sfx_pick bgm_lib rhythm palettes axis_lib concepts picev pivots caption_hl thumb_lib figlib hands body tts_text facing` |
| `tools/build/` | pipeline steps, in order | `tts.sh audio_prep align build3 frog_place gen_text thumb_shot chunk_plan clip_prep svg_opt remake remap_art restyle_motion ws_setup.sh` |
| `tools/check/` | gates and checks (report only) | `final_check attachcheck pivotlive originlive pivcheck entrycheck figcheck eyecheck variety_check used_check motion_check freezecheck mvcheck partaxis` |
| `tools/fix/` | repair helpers that rewrite pictures | `axisfix armfix scalefix galaxyfix corefix splitlimbs splitclumps joinpart setbase gearmesh fallwrap` |
| `tools/preview/` | strips and contact sheets | `motionaudit motion_preview frogshot labelshot svgshot grpinfo` |
| `tools/writing/` | script and title helpers | `hookscore (+hooks.json) title_lint` |
| `tools/assets/` | shared page assets: gsap + 14 plugins, anime.js, lucide icons, fonts, logo, grain, frog | |
| `tools/briefs/`, `tools/ref/` | agent briefs, reference drawings | |

- Run from the repo root: `SLUG=x python3 tools/build/build3.py`, `python3 tools/check/final_check.py`.
- Every script in a subfolder adds `tools/` and its sibling folders to `sys.path` in its first code line, so `import motions` works from anywhere. One tool calls another through `paths.tool('name.py')`.
- Outside scripts (thumbnail `make.py`, picture generators) use `sys.path.insert(0, 'tools')` and the libraries in `tools/`.
- A new tool goes into the folder that matches what it does; a new library stays in `tools/`. Add it to this file.
- Shared page assets live only in `tools/assets/`. `build3.py` copies them into `render/<slug>/` for local preview (git-ignored there); `chunk_prep.py` / `clip_prep.py` link them into the chunk folder; `paths.ensure_assets(dir)` links them for the check tools on a fresh clone.
- Environment: `SLUG=<video-slug>`, optional `MIYA_WORK=<scratch dir>` (default `/tmp/miya-work`). All paths come from `tools/paths.py`. `paths.chrome()` finds Chromium (env `HYPERFRAMES_BROWSER_PATH` / `PW_CHROME` / `CHROME`, else the newest `/opt/pw-browsers/chromium-*`).
- Tools that open the built page need playwright; run them with the system `python3`. Only TTS needs the Kokoro venv.

## 2. Per-video folder `videos/<slug>/`

| File | What |
|---|---|
| `script.py` | `SCENES = [(id, chapter title, "ill"|"chalk", art id, narration), ...]` |
| `config.py` | `CHALK`, `WHOOSH`, `TITLE`, `DESC`, `CHAPTERS`, `SOURCES`, `HASHTAGS`, palette and build options (section 6) |
| `plan.json` | units written by `PLAN=1` (uid, text, backdrop kind, transition, `pal`) |
| `art3/<uid>.svg` + `<uid>.json` | one picture and sidecar per unit (spec `tools/art_spec.md`; movable parts as `id="mv-<kind>-<name>"` groups) |
| `art_brief.md` | character sheet and per-video picture notes for the agents (this name only) |
| `thumb/` | `A.html`, `B.html`, `C.html`, `make.py`, `common.css`, `Fredoka-700.woff2` (shorts: `A.html` only) |
| long-form folder only | `script-check.md` (fact-check table, length changes), corrected narration `long.txt`, `short1.txt`…`short5.txt` |

- The untouched original script stays on `main` in `scripts/<daily|owl|igwahyung>/used/`.
- Nothing else loose in the folder (no `__pycache__`, scratch images or agent logs).
- Shorts are separate slugs `<slug>-short1` … `<slug>-short5`, each with its own folder and `.dest`.

## 3. Steps

| # | Command | Result |
|---|---|---|
| 1 | `SLUG=x HYPERFRAMES_PYTHON=<venv python> tools/build/tts.sh` | Kokoro `am_michael`, one wav per scene. `tts_text.py` spells out 4-digit years |
| 2 | `SLUG=x python3 tools/build/audio_prep.py` | stereo, loudnorm −16.8 LUFS, per-scene clips, timing. Check its total length (≤ 15 min) |
| 3 | `SLUG=x python3 tools/build/align.py` | word times (faster-whisper small.en, CPU, about 4 min per 45 paragraphs) into `build/words.json`. Required before build3 (it stops when a paragraph matches < 90 % of its words) |
| 4 | thumbnails: Opus agent (`tools/briefs/thumb_art.md`) writes `thumb/{A,B,C}.html` via `make.py` + `thumb_lib.py`; then `SLUG=x python3 tools/build/thumb_shot.py` | `render/x/deliver/x_thumbnail_A..C.png`. Wait for miya's OK before step 5 (guideline 12-1) |
| 5 | `SLUG=x PLAN=1 python3 tools/build/build3.py` | `plan.json` |
| 6 | picture agents draw `art3/<uid>.svg+json` (`tools/art_spec.md` + `art_brief.md`); each agent runs `axisfix` → `splitlimbs` → `partaxis` → `attachcheck` | pictures |
| 7 | `python3 tools/build/frog_place.py <slug>` | sidecar `frog` of every `frog_hint` unit (guideline 7-2). Picture agents never write the frog |
| 8 | `SLUG=x python3 tools/build/build3.py` (`VERT=1` for Shorts) | `render/x/` (`index.html`, `mix.m4a`). Check the log lines in section 6 |
| 9 | `SLUG=x python3 tools/build/gen_text.py` | metadata txt into `render/x/deliver/` |
| 10 | `SLUG=x python3 tools/check/final_check.py` | gate; writes `render/x/.checked` when everything passes (guideline 15-8) |
| 11 | `python3 tools/build/chunk_plan.py render/x` → put `"<slug> <chunks>"` in `render/.chunked` and push | `render-chunked.yml` renders, joins and uploads to Drive |
| 12 | download the chunk artifact, `python3 tools/check/freezecheck.py chunk.mp4` | frozen-picture check before reporting done |

- Shorts: same steps with the short's slug. One vertical thumbnail each (`videos/x-shortN/thumb/A.html`, 1080×1920, `thumb_lib.vpage/vsvg`, `assets/thumb_v/common.css`), no approval needed (guideline 16-9). `gen_text.py` writes title/description/hashtags because `CHAPTERS=[]`. Shorts art is vertical (`art_spec.md` section 10).
- Upload thumbnails/text without rendering: `"<slug> 0"` in `render/.chunked`.
- `render/<slug>/.dest` (one line) = Drive folder; `.outname` = Drive file name; `.skip_deliver` = do not re-upload `deliver/`.
- Every line of `render/.chunked` runs again on each push: remove finished lines. To avoid touching the file, use workflow_dispatch with `spec`.
- The Kokoro venv held `kokoro-onnx 0.6.1, soundfile, onnxruntime, phonemizer, espeakng-loader, numpy`; `align.py` needs `faster-whisper`. Setting the venv up from scratch was not re-tested.

## 4. Tool reference

### build/

| Tool | Use |
|---|---|
| `build3.py` | builds the page. Runs first: `axisfix`, `galaxyfix`, `armfix`, `scalefix`, `corefix`, `svg_opt`; runs last: `attachcheck`. Options in section 6 |
| `frog_place.py <slug>...` | picks the frog's act, outfit, mood, bubble and place from script words + picture evidence (`contact_pick`, `loco_pick`, `costume_pick`, `concept_apply`, `pulse_response`). A hand-edited sidecar needs `"lock": true` |
| `svg_opt.py` | svgo pass (`npx --yes svgo@4`) into `<work>/build/art_opt/`; keeps ids, data-*, groups, hidden elements, basic shapes, transforms. `SVGO=0` disables. `python3 tools/build/svg_opt.py videos/<slug>/art3` prints the saving |
| `chunk_plan.py render/<slug> [target_min]` | number of chunks; refuses without a current `.checked` |
| `clip_prep.py <slug> <t0> <len>` | prepares any time range as a short sample clip; mux audio with `ffmpeg -ss <t0> -t <len>` |
| `remake.py` | `SLUG=x python3 tools/build/remake.py`: keeps the old plan, re-splits, re-links pictures with `remap_art.py`, prints `NO ART` / `NEEDS VARIANT` units, checks `.dest` / `.skip_deliver` (guideline 21). Briefs `briefs/remake_art.md`, `briefs/people_restyle.md` |
| `remap_art.py <old plan>` | links old pictures to re-split units |
| `restyle_motion.py render/<slug>` | re-styles motion of an already built page in place (no TTS, no pictures). Original build output only (guideline 15-7) |
| `ws_setup.sh <ws-dir> <slug>` | copies tools, docs, the video folder and the work folder into a sandbox so an agent can do partial `SEL=` builds and run `motionaudit.py` / `pivotlive.py` |

`tools/chunk_prep.py <slug> <n> <i>` (library folder): prepares chunk `i` of `n` for the render workflow; also used for a local range render.

### check/

| Tool | Use |
|---|---|
| `final_check.py` | main's gate before every render push: attachcheck, pivotlive, originlive, partaxis, splitlimbs `--check`, armfix `--check`, entrycheck, variety_check, figcheck (WARN), used_check (WARN), missing pictures, forbidden eases |
| `attachcheck.py <slug> [uid..] [--fix]` | static per-picture check: hinges on the body, rotor centres, gears mesh, tails inside moving bodies, standing things = foot pivot, label pointers inside moving objects, axis-catalogue mismatches (guideline 4-7, 4-8) |
| `pivotlive.py` | built page: fails when a hinge pivot is carried ≥ 10 px |
| `originlive.py` | built page: spin/turn/roll groups without `data-pivot` must turn about their own centre (< 10 px) |
| `pivcheck.py <slug>` | lists chain/joint/rotor pivots that land > 40 px from their part |
| `partaxis.py <slug> [--fix] [uid..]` | hinged parts pivot at the body-side end (advisory heuristic); `mv-wiggle` amp > .3 or period < .6 fails (`--fix` sets .06 / 1). `data-keep="1"` skips a part (guideline 4-12) |
| `entrycheck.py <slug>` | entrance motions must be hidden with `tl.set` before they start (guideline 4-15) |
| `variety_check.py <slug>.. [--report]` | frog acts / outfits / moods, object `mv-` kinds, moving-prop pictures (WARN), centre-motion event share ≤ 15 %, frog riding a pulsing object = 0, fast throb ≤ 10 % (guideline 7-2 K-6) |
| `figcheck.py <slug> [uid..] [--strict]` | hand groups drawn outside `figlib` |
| `eyecheck.py` | frog pupils inside the eye whites on thumbnails |
| `used_check.py <slug> [pasted.txt]` / `--all` | exactly one untouched original in `scripts/<daily|owl|igwahyung>/used/` |
| `motion_check.py render/<slug> [--step 6]` | finds stretches where the picture hardly moves (guideline 20-4) |
| `freezecheck.py <mp4> [sec]` | rendered picture frozen (≤ 2 distinct frames for ≥ 5 s) although the workflow succeeded |
| `mvcheck.py <new.svg> [<original.svg>] [outdir]` | adding `mv-` groups did not change the picture; renders every group posed |

### fix/

| Tool | Use |
|---|---|
| `axisfix.py <slug> [uid..] [--force] [--report] [--svg f..]` | writes missing `data-pivot` from the axis catalogue; `--force` rewrites foot/hook/hub/edge pivots > 12 px off (32 for hanging points). Contact/centre pivots are only filled when missing |
| `corefix.py <slug>.. [--report]` | rewrites `mv-core-<event>` ids without a sentence word or thing name, or over 15 %, to the least-used calm kind that fits the catalogue; `data-strong="1"` for strong heartbeats (guideline 4-13) |
| `armfix.py <slug>.. [--report\|--check]` | raised arms curve down (guideline 4-11) |
| `scalefix.py <slug>.. [--report]` | balance: only the beam tilts, pans hang (guideline 4-11) |
| `galaxyfix.py <slug>.. [--report]` | tilted galaxy disc spins in its own plane (`mv-disc-galaxy`, guideline 4-9) |
| `splitlimbs.py <slug> [uid..] [--dry\|--check]` | splits a bundle of strands under one pivot into per-strand hinges (guideline 4-12) |
| `splitclumps.py`, `joinpart.py`, `setbase.py <slug>` | one group per clump; put a tail/leg inside its moving body; foot pivots for standing things (guideline 4-7) |
| `gearmesh.py <svg> <gearA id> <gearB id> <angle>` | redraws two gears so they mesh |
| `fallwrap.py <svg> <first-needle> <last-needle> '<path d>' [dur] [delay] [name]` | wraps a whole falling object (body + joints) in `mv-path-sink-*`; such paths are not followed by the camera |

### preview/

| Tool | Use |
|---|---|
| `motionaudit.py <dir> <uid..>` | strips from the built page at 3 times with a red dot on every pivot |
| `motion_preview.py <out_dir> <uid>...` (`SLUG=`) | strip of one picture at several seconds with the same `motions.py` code, no full build |
| `frogshot.py <out.png> <t1,t2,...>` (`SLUG=`, `VERT=1`) | contact strip of the built page at those seconds |
| `labelshot.py <slug> <dir> <uid...>` | on-screen text preview |
| `svgshot.py <out_dir> <svg>...` | static PNG of SVG files (`SHOT_W/SHOT_H` for vertical) |
| `grpinfo.py <slug> <uid..>` | mv groups: boxes, pivots, parents |

Seeking a built page from Playwright: `tl.pause(); tl.seek(t, false)` and launch Chromium with `--no-sandbox` (`timeline.pause(t)` or a launch without it hangs in the cloud container).

### writing/

| Tool | Use |
|---|---|
| `hookscore.py hooks.txt` (+ `hooks.json`) | scores 3-5 hook candidates for the first 15 s (reference only, guideline 12-1) |
| `title_lint.py --title "..." [--thumb "..."]` | checks a title/thumbnail text pair against guideline 16-6 and 17-3 (advisory) |

Both adapted from Jakeschincariol/youtube-agent-skill (MIT).

## 5. Libraries (`tools/*.py`)

| Library | What it holds |
|---|---|
| `paths.py` | all paths, `tool()`, `chrome()`, `ensure_assets()` |
| `motions.py` | centre motions (`mv-core-*`, `core_js`, `CORE_WORDS`, `CORE_NAMES`, `core_fit`), object motions (`OBJ_KINDS` 73, `obj_js`), transitions (`tr_js`, `miyaTr`), tracking camera (`track_spec`, `miyaTrack`, sidecar `world`), background effects (`FX_KINDS` 63, `fx_for`, `FX_WORDS`, `FX_PIC`, `FX_AMBIENT`), axis sanity (`pivot_of`, `core_sanitize`, `obj_sanitize`), `chalk_life_js`, `settle_js`, `miyaFollow`, `dir_sign` |
| `fxlib.py` | GSAP plugin list, `script_tags()`, `REGISTER_JS` (eases `miyaW`, `miyaJit`, `miyaWig*`, `miyaBnc*`), `plain_wiggles()`, `LIB_JS` (`miyaAnime`, `miyaSpring*`, `miyaMorph`, `miyaRegroup`, `miyaIconDraw`), word tables (`SCRAMBLE_W`, `TYPE_W`, `SPEED_W`, `ROUGH_W`, `ZOOM_W`, `PLAYFUL_W`/`SERIOUS_W`), `path_ease`, `spring_params`, lucide `icon_for` / `icon_svg`. `python3 tools/fxlib.py "Whale fall"` shows the pictogram choice |
| `labels_lib.py` | on-screen text: `check`, name-label / bubble / badge entrances (`NAME_FX`, `SAY_FX`, `NUM_FX`, `PIC_FX`), count-up, pictograms |
| `caption_hl.py` | spoken subtitle word turns yellow (`#ffd54a`) |
| `frog.py` | frog drawing, `MOODS` + `face_js`, outfits (`outfit_markup`, `OUTFITS2`), acts, `enter_js` / `cam_js` (camera coupling, `CAM_CALM`) |
| `frog_rig.py` | joints, `life_js`, `CONTACT` (25), `LOCO` (10), `COSTUME_ACTS` (38), `CONCEPT_ACTS` (34), `RESPONSE_ACTS`, `CAMERA_ACTS`, `obj_span`, `arm_bend_pass`, `shadow_follow_pass`, `HITS`. `python3 tools/frog_rig.py --check` lists look-alike acts in one pool |
| `concepts.py` | 9 domains, 25 idea classes, act pools, outfit packs, picture packs, least-used picker `Tally`. `--doc > tools/concepts_catalog.md`; `python3 tools/concepts.py <slug>` prints the video's pack |
| `axis_lib.py` | axis catalogue (about 380 thing words → base/top/contact/round/edge/center/none). `--doc` prints `axis_catalog.md` |
| `facing.py` | direction rules (guideline 4-4): `context()`, `facing_sign`, `_path_rules`, `_dir_rules2`, `spin_dir`. `python3 tools/facing.py <slug>` reports without changing files |
| `picev.py` | picture evidence tags from object groups' names and sizes |
| `pivots.py` | shoulder/wrist pivots for `mv-arm` / hand groups |
| `sfx_lib.py`, `sfx_pick.py` | 92 quiet unpitched sounds; cue per unit by word rules, palette ambience, density cap 45 %, sidecar fallback, `sfx_lock`. `python3 tools/sfx_pick.py` checks every rule names an existing sound |
| `bgm_lib.py` | synthesised background music: 9 `STYLES` × 4 mood `POOLS`, `style_for`, `scene_moods`, `synth_cosmic`; highpass 250 Hz, ducked 13 dB below narration RMS (`BGM_BELOW`) |
| `rhythm.py` | `silence_windows`, `accent_times`, `gain_mask` (guideline 9-5) |
| `palettes.py` | 10 topic palettes + 4 cosmic palettes |
| `thumb_lib.py` | thumbnail pages (`page`, `svg`, `vpage`, `vsvg`, `lin`, `rad`, `stars`, `spark`, `blobs`, fireflies / halo / darkband) |
| `figlib.py` | `hand(pose, x, y, size, side, rot)` 12 poses (mandatory for every hand with fingers); optional `person(...)`. `python3 tools/figlib.py <dir>` writes reference sheets |
| `body.py` | human proportions and `arm()`. `python3 tools/body.py out.svg` draws the reference sheet |
| `hands.py` | older hands: only for existing pictures and thumbnails |
| `tts_text.py` | TTS text pre-processing |

## 6. Build options and log lines

**`config.py` / environment**

| Option | Effect |
|---|---|
| `PAL_DEFAULT`, `PAL = {art_theme: palette}` | palette (always set `PAL_DEFAULT` for a new video; without it `sunset` is used and `PLAN=1` warns) |
| `STYLE = 'cosmic'` | cosmic mode (guideline 3-7) |
| `PACE` (default 1.5), `HOOK`, `SLOW`, `NOT_SLOW`, `DRIFT = False` | cut lengths and drift camera (guideline 20-1, 20-2) |
| `FROG = False`, `FROG_TONE = 'serious'` | chalkboard frog off; serious topic (guideline 7-2) |
| `SILENCE` | near-silence windows (guideline 9-5) |
| env `PLAN=1` | write `plan.json` only |
| env `VERT=1` | vertical (Shorts) |
| env `SEL=1,2,3` | partial build of those scenes (picture uids come from `plan.json`) |
| env `FALLBACK=1` | test build without pictures |
| env `NOBGM=1`, `NOSILENCE=1`, `NOACCENT=1`, `SVGO=0` | switch off music, silences, accents, svgo |

**Log lines to read after build3**: `fallback art 0`, `min` (shortest unit), `cuts moved for min time`, `slow scenes`, `axisfix:`, `galaxyfix:`, `corefix:`, `motion sanity`, `direction sanity`, `tracking cams`, `labels follow moving objects`, `hinge tweens added after the follow measuring`, `library fx`, `svgo`, `sfx auto`, `music style`, `bgm moods`, `theme pack:`.

**How to verify a change to motion code**: build a synthetic page (all kinds on simple shapes), seek it with Playwright, look at frames; then a local range render + `freezecheck.py` for new eases/plugins. Do not start with a full render.

---

## History
- 2026-10-10: palettes, sfx v2, background music, per-video `art_brief.md`.
- 2026-10-12: cosmic mode. 2026-10-13: centre-object motions, count-up badges, focus spotlight, subtitle highlight, six picture specs merged into `art_spec.md`.
- 2026-10-14~19: transitions, parallel render (`chunk_plan`, `chunk_prep`), `HOOK`/`DRIFT`, joints, `mv-rotor`, `remake.py`.
- 2026-10-22: `PACE`, 5 transitions, object motions, camera tracking, `title_lint`, `hookscore`.
- 2026-10-24: `slide/fade/ticks/rack`, world camera, `rhythm.py`, `paths.chrome()`. 3D tools moved to branch `archive/miyas-lab-2026-10-24`.
- 2026-10-25~27: `tts_text`, preview tools, `frog_place`, `fallwrap`, `pivots`, axis sanity, background/text effects, `picev`, `facing`, sfx 92 kinds, music styles.
- 2026-10-29~30: `fxlib` (GSAP 3.15 plugins, anime.js, lucide, svgo), `frog_rig`, attachment checks, axis catalogue, `final_check`, `freezecheck`, `galaxyfix`; CustomWiggle eases replaced by `miyaW`/`miyaJit`.
- 2026-10-31~11-05: `concepts`, `variety_check`, `armfix`, `scalefix`, `splitlimbs`, `partaxis`, `corefix`, `figlib`, `entrycheck`. 2026-11-11: `used_check`.
- 2026-11-14 (miya): tools grouped into `build/ check/ fix/ preview/ writing/`, shared assets only in `tools/assets`; `render.yml` / `render/.slug` / `.deliver_only` removed (one workflow, `"<slug> 0"` = deliver only); this file rewritten in the current-rules form.
