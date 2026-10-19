# kardashev-scale — art brief (shared by all picture agents) — COSMIC MODE

Read fully: `tools/art_spec.md` (**cosmic mode = section 11 wins where sections conflict**; section 5 backdrop rules: every picture gets a backdrop that fits its own text, no concentric rings or radiating-line backdrops, neighbouring units never share a backdrop kind, at most 2 of 12 units share a kind; vertical Shorts also follow section 10; people follow 6A/6B with `tools/body.py` and `tools/hands.py`).

Paths: repo root is `/home/user/youtube-script-daily` (the specs say `/home/claude/ht/...` or `/home/user/rp/...`: use the repo root instead).
- plan: `videos/<SLUG>/plan.json` (use the entries for YOUR uids: `bg`, `pal`, `text`, `prev`, `nxt`, `transition_in`, `dur`)
- output: `videos/<SLUG>/art3/<uid>.svg` and `<uid>.json`
- preview: `python3 tools/svgshot.py <preview dir> f1.svg ...` (vertical Shorts: `SHOT_W=1080 SHOT_H=1920`)
- SLUG is given in your task: long `kardashev-scale`, Shorts `kardashev-scale-short1/2/3`.
Write ONLY your own uids. Scratch work (generator scripts, previews) goes ONLY in your own folder given in your task. No git.

## Topic
The Kardashev scale: how much energy a civilization can command. Modern-day anchors (a wall light switch, a hand holding a glowing smartphone, a city grid at night, a power-line web across a continent, a hydro dam, a radio telescope dish, a desk with star charts and a 1960s chalkboard: NEVER a portrait of Kardashev, Sagan, Dyson or Hanson: show hands, desks, instruments, silhouettes from behind). Planet-scale power (sunlight on the whole world, wind, tides, geothermal vents), a calm "managed planet" with weather and tectonic plates shown as diagrams, Earth with a faint city-light network and a thin gauge; a solar storm hitting the magnetosphere and a darkened city (Quebec 1989 as a dark city under aurora, no text); Mount Tambora-style eruption cloud cooling a pale summer; a category-five hurricane viewed from orbit; a star wrapped by a swarm of mirrored solar collectors (Dyson swarm: a SWARM of separate collectors, not a solid shell, but it may look like a glowing golden lattice); a whole spiral galaxy with a Type Three glow, a supermassive black hole with a spinning accretion disk and a little energy-extraction ring; a galaxy full of stars with one lit-up network of civilizations; the Great Silence: a radio dish under a star-filled sky with an empty waveform strip; the Great Filter as a narrow gate or tall hurdle on a path of steps; a night sky with the Milky Way and a person looking up.

## Character / object sheet (keep identical across all agents)
- **Modern person** (hook/ending): a calm adult in a dark-teal jacket and grey scarf, short dark hair, simple dot eyes; ids `mv-breathe-gazer`, `mv-nod-gazer`, `mv-arm-gazer`.
- **Earth**: blue-green sphere with a thin bright rim; at night a faint web of golden city lights.
- **The Sun / host star**: warm gold-white sphere with radial-gradient glow (no ray fans). **Dyson swarm**: many small gold-and-mirror panels around the star, denser toward the equator, a few panels in motion.
- **Galaxy**: spiral with a warm core and blue-white arms, drawn with radial gradients (no filters).
- **Ladder motif** (used across the video): three glowing steps/rungs, pale blue (planet), gold (star), violet-white (galaxy), with Earth sitting at the foot, a little below the first step. No numerals on it.
- No film references: nothing recognisable from any movie. No text, letters, numbers or equations inside the SVG (on-screen text comes from `labels`).

## Notes
- **Backgrounds**: mostly `night` (cosmic look, art_spec section 11: nebula gradient layers, three star tiers, rim-lit spheres, fine sketch lines); `dusk`/`paper` units get the normal look with the same palette. Each plan unit has `bg` and `pal`: follow them.
- Be truthful: Type One/Two/Three are *hypothetical* civilizations; draw them as possibilities. Do not draw an alien or any "found" evidence. Show "in theory" abilities (eased earthquakes, steered weather) as diagrams, not as an existing fact.
- `focus` on 40-50 % of units; sfx on 35-45 % using ONLY: `sparkle`, `bloom`, `starfall`, `pulse`, `warp`, `glimmer`, `tick`, `click`, `pop`, `drip`, `pencil`, `page`, `woodblock`, `stone`, `step`, `cloth` (never `hush`, `breath`, `wind`, `rain`, `swish`; never the same name in two consecutive units).
- **On-screen text**: also write `"labels"` in each sidecar (art_spec section 8, "On-screen text"): names that are visible AND said in the unit text (Type One, Type Two, Type Three, Dyson sphere, Great Filter, Milky Way, ...), a `num` badge when the unit says a number or year (e.g. "zero point seven" -> `0.7`, "nineteen sixty" -> `1960`, "nineteen eighty-nine" -> `1989`, "nineteen sixty-four" -> `1964`), a short `say` bubble on about 1 unit in 8 (only from the generic person; never a real person; no facts). Then run `python3 tools/labelshot.py <SLUG> <your scratch>/lab <uids...>`; fix every reported problem and look at every `<uid>_lab.png`.
- Motion groups (4-8 per picture): stars `mv-glint-s1/s2/s3`, one nebula layer `mv-drift-nebula` (bigger than the canvas by 40 px each side), orbiting bodies `mv-orbit-<name>` (group contains an invisible full-orbit circle `fill="none" stroke="none"` plus the body), `mv-pulse-core`, glowing centre `mv-core-<type>` (or `mv-glint-core`), people `mv-breathe-/mv-nod-/mv-arm-<name>`, hands `mv-hand-<name>`, drifting particles `mv-cells-<name>`. Ids unique inside each file.
- Final answer: one line per uid: `uid | centre | backdrop kind | focus_word or - | sfx or - | labels count`, plus problems left (8 lines max if more than 8 uids: summarise).
