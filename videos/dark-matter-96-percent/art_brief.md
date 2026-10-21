# dark-matter-96-percent — art brief (shared by all picture agents) — COSMIC MODE

Read fully: `tools/art_spec.md` (**cosmic mode = section 11 wins where sections conflict**; section 5 backdrop rules: every picture gets a backdrop that fits its own text, no concentric rings or radiating-line backdrops, neighbouring units never share a backdrop kind, at most 2 of 12 units share a kind; vertical Shorts also follow section 10; people follow 6A/6B with `tools/body.py` and `tools/hands.py`).

Paths: repo root is `/home/user/youtube-script-daily` (the specs say `/home/claude/ht/...` or `/home/user/rp/...`: use the repo root instead). `export MIYA_WORK=/tmp/miya-work`.
- plan: `videos/<SLUG>/plan.json` (use the entries for YOUR uids: `bg`, `pal`, `text`, `prev`, `nxt`, `transition_in`, `dur`)
- output: `videos/<SLUG>/art3/<uid>.svg` and `<uid>.json`
- preview: `python3 tools/svgshot.py <preview dir> f1.svg ...` (vertical Shorts: `SHOT_W=1080 SHOT_H=1920`)
- SLUG is given in your task: long `dark-matter-96-percent`, Shorts `dark-matter-96-percent-short1/2`.
Write ONLY your own uids. Scratch work (generator scripts, previews) goes ONLY in your own folder given in your task. No git.

## Topic
Why only about 5 % of the universe is ordinary matter and ~27 % dark matter, ~68 % dark energy: galaxy rotation (Zwicky 1933, Vera Rubin and Kent Ford ~1970), gravitational lensing, the Bullet Cluster, the leading dark matter suspects, underground detectors (LUX-ZEPLIN in a South Dakota mine), the cosmic web, the Planck map of the Big Bang afterglow, accelerating expansion (Type Ia supernovae, Hubble 1929), dark energy and the cosmological constant, DESI hint, the cosmic budget, a 100-page book with 5 readable pages, Hubble 1924 (Andromeda is another galaxy), Euclid and the Rubin Observatory, the far future, atoms as stardust, looking up tonight.
Modern anchors: a hand on a desk / a person at a window with a glowing phone (hook), a person looking up at the night sky from a hill or balcony (silhouette from behind), a desk with star charts, a small observatory dome, a radio dish. NEVER a portrait or likeness of Zwicky, Rubin, Ford, Hubble, Einstein or any real person; show silhouettes from behind, hands, desks, instruments, a generic observatory.

## Character / object sheet (keep identical across all agents)
- **Modern person** (hook/ending): a calm adult in a dark-teal jacket and grey scarf, short dark hair, simple dot eyes; ids `mv-breathe-gazer`, `mv-nod-gazer`, `mv-arm-gazer`. Always from the side or behind.
- **Visual language of the three ingredients (use consistently):**
  - **Ordinary matter** (stars, gas, planets, atoms): warm gold-white glints, soft cream, coral hot gas; crisp, bright, with thin sketch lines.
  - **Dark matter**: a faint translucent blue-indigo haze with thin pale filament threads, NO sharp outline and no shining parts. It is only ever shown as haze / halo / web / a glassy shape / "empty-looking" space that bends things. Never a monster, ghost or face.
  - **Dark energy**: a cool teal-white gentle outward push: a stretching grid or fabric of space, galaxies drifting apart, a smooth teal gradient spreading outward (no radiating-line fans, no concentric rings).
- **Galaxies**: spiral = soft gold-white core, blue-white arms made of star dots, a thin dark dust lane; seen face-on or tilted. The Milky Way, Andromeda and cluster members use the same spiral look in different sizes.
- **Bullet Cluster**: two clusters of small galaxy dots; the hot gas drawn as coral clouds that lag in the middle, the dark matter haze (blue) drawn passing ahead on both sides (qualitative, no scale).
- **Lensing**: a bright background galaxy stretched into thin gold arcs around a blue-haze cluster; keep arcs as curved strokes, not rings.
- **Detectors**: a tank of pale liquid glowing softly in a dark shaft underground, rock layers above (generic; no logos); **telescopes**: a dish, a dome, a generic space telescope with a hexagon-free simple mirror.
- **Supernova**: a bright white-gold burst blob with a soft glow (not ray fans); **white dwarf**: small bright pale-blue sphere with a gas stream from a red companion star.
- **Book (invisible ink)**: an open book on a desk with a small patch of printed lines on one page and the rest of the pages blank-looking with faint gleam; no letters.
- No film references. No text, letters, numbers or equations inside the SVG (on-screen text comes from `labels`). The chalkboard scenes (`chalk`, `chalk2`, `chalk3`) need no picture from you (they have none in the plan).

## Notes
- **Backgrounds**: mostly `night` (cosmic look, art_spec section 11: nebula gradient layers, three star tiers, rim-lit spheres, fine sketch lines); `dusk`/`paper` units get the normal look with the same palette. Each plan unit has `bg` and `pal`: follow them.
- Be truthful: hypotheses stay hypotheses (what dark matter is, DESI hint, far future, Big Rip). Draw dark matter only as haze/halo/web. Qualitative scale only (no invented numbers). Do not draw aliens or anything not in the text.
- `focus` on 40-50 % of units; sfx on 35-45 % using ONLY: `sparkle`, `bloom`, `starfall`, `pulse`, `warp`, `glimmer`, `tick`, `click`, `pop`, `drip`, `pencil`, `page`, `woodblock`, `stone`, `step`, `cloth` (never `hush`, `breath`, `wind`, `rain`, `swish`; never the same name in two consecutive units).
- **On-screen text**: also write `"labels"` in each sidecar (art_spec section 8, "On-screen text"): names that are visible AND said in the unit text (Milky Way, Andromeda, Coma Cluster, Bullet Cluster, Mercury, Neptune, Planck, LUX-ZEPLIN, DESI, Euclid, Rubin Observatory, ...), a `num` badge when the unit says a number or year (e.g. "five percent" -> `5%`, "twenty-seven percent" -> `27%`, "1933" -> `1933`, "forty-seven kilometers per second" -> `47 KM/S`), a short `say` bubble on about 1 unit in 8 (only from the generic person; never a real person; no facts). Then run `python3 tools/labelshot.py <SLUG> <your scratch>/lab <uids...>`; fix every reported problem and look at every `<uid>_lab.png`.
- Motion groups (4-8 per picture): stars `mv-glint-s1/s2/s3`, one nebula layer `mv-drift-nebula` (bigger than the canvas by 40 px each side), orbiting bodies `mv-orbit-<name>` (group contains an invisible full-orbit circle `fill="none" stroke="none"` plus the body), `mv-pulse-core`, glowing centre `mv-core-<type>` (or `mv-glint-core`), people `mv-breathe-/mv-nod-/mv-arm-<name>`, hands `mv-hand-<name>`, drifting particles `mv-cells-<name>`. Objects with parts that must move on their own (rotating things, e.g. a galaxy disk, a clock) follow guideline 4-1: `mv-rotor-*`/`mv-joint-*`, no whole-object spin of something with neighbours. Ids unique inside each file.
- Final answer: one line per uid: `uid | centre | backdrop kind | focus_word or - | sfx or - | labels count`, plus problems left (8 lines max if more than 8 uids: summarise).
