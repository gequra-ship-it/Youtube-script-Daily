# epomis-frog-hunter-v2 — art brief (shared by all picture agents)

Read fully: `tools/art_spec.md` (section 5 backdrop rules: the backdrop variety rules apply to NEW pictures too: no concentric rings, no radiating lines/rays/sunbursts; every picture gets a backdrop that fits its own text; neighbouring units must not share a backdrop kind; at most 2 of every 12 units share a kind). Vertical Shorts agents also follow section 10 of `tools/art_spec.md`.

Paths in those specs that mention `/home/claude/ht/videos/never-eat-human-meat-v3/` mean, for this video:
- plan: `/home/claude/youtube-script-daily/videos/<SLUG>/plan.json` (use the entries for YOUR uids; `bg`, `text`, `prev`, `nxt`, `transition_in`, `dur`)
- output: `/home/claude/youtube-script-daily/videos/<SLUG>/art3/<uid>.svg` and `<uid>.json`
- preview tool: `python3 /home/claude/youtube-script-daily/tools/svgshot.py <preview dir> f1.svg ...` (vertical: `SHOT_W=1080 SHOT_H=1920`)
- `<SLUG>` is given in your task (long video `epomis-frog-hunter-v2`, Shorts `epomis-frog-hunter-v2-short1` / `-short2`).
Write ONLY your own uids. Do not edit any other repo file. **Scratch work (generator scripts, previews) goes ONLY in your own folder** `/tmp/claude-0/-home-claude-youtube-script-daily/53bea993-48d4-5496-836b-a9dbb74ebe3e/scratchpad/<first uid>_<last uid>/` — other agents work in parallel; never write to a shared scratch file name.

## Topic
Epomis ground beetles (Israel lab study, 2011). The larva lures frogs/toads by waving its antennae and moving its jaws, dodges the frog's tongue, latches on with double-hooked jaws, and feeds on the amphibian. The adult beetle shares shelters with amphibians by day; at night it jumps onto an amphibian's back and makes a cut across its lower back. Night ponds, wet leaf litter, lab containers, field notebooks. Some scenes compare other lures (anglerfish, alligator snapping turtle) and small hunters (praying mantis and a hummingbird, giant water bug).

## Character / object sheet (keep identical across all agents)
- **Epomis larva**: long slim segmented body (10-12 segments), pale cream-yellow `#f3e3b0`; each segment has a thin dark band `#1b1830` near its rear edge, a small black dot near the side and a small orange `#d9694a` mark (banded look — do NOT put a centred dot + orange blush + curve on each segment: that reads as rows of cute faces). Small rounded dark-orange `#c46a2e` head with NO face (no eyes-and-smile); TWO dark-brown `#3a2418` sickle jaws at the front, each with a hooked tip and a second inner hook (double hook); two short thin antennae; two short tail extensions at the rear; six tiny legs near the front. Thin ink outline.
- **Adult Epomis beetle**: ground-beetle shape (oval wing covers, narrower neck shield, head with jaws); metallic blue-green wing covers (gradient `#2f5f8f` -> `#2f8f74`, soft highlight), bright yellow-orange rim `#f2a33a` along the wing-cover edge, yellow `#e8c25a` legs and antennae.
- **Frog** (Levant water frog): green `#5f8f5a`, darker spots `#3f6a45`, pale belly `#cfe0b0`, golden eye `#f2c14e` with a horizontal dark pupil. **Green toad**: cream-grey `#c9c3a6` with olive-green blotches `#6f9a5a`, warty dots, two oval glands behind the eyes. **Savigny's tree frog**: small, bright green `#6fbf5a`, dark side stripe. **Banded newt**: slim, brown-olive with a pale side band. **Fire salamander**: black with yellow spots. In the lab trials the amphibians are YOUNG (small, just out of the water) but still much larger than the larva.
- **People**: only generic people (a person by a pond at night, a viewer). Researchers appear as hands, lab-coat sleeves, notebooks, small lab containers and a video camera; never a recognisable real person, never faces.
- **Violence / death**: no blood, no wounds, no gore. Feeding = larva clinging near the frog's mouth/throat/chest, frog calm and still, soft shading. Adult's cut = a thin dashed line on the lower back, no wound. Remains = a small clean, museum-style bone sketch. Calm and scientific.

## Notes
- No text inside pictures (no letters, numbers, labels).
- `focus` on 40-50 % of units; sfx on 35-45 % using ONLY the 25 library names in art_spec.md section 8 (unpitched; vary — never the same name in two consecutive units).
- Motion groups: frogs `mv-breathe-<name>`; larva antennae `mv-antenna-<name>` when the text is about the lure; glowing centre `mv-glint-core`. Ids unique inside each file.
- Final answer: one line per uid: `uid | centre | backdrop kind | focus_word or - | sfx or -`, plus problems left.
