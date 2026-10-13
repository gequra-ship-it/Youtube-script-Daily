# ribeiroia-monster-frogs — art brief (shared by all picture agents)

Read fully: `tools/art_spec.md` (section 5 backdrop rules: the backdrop variety rules apply to NEW pictures too: no concentric rings, no radiating lines/rays/sunbursts; every picture gets a backdrop that fits its own text; neighbouring units must not share a backdrop kind; at most 2 of every 12 units share a kind). Vertical Shorts agents also follow section 10 of `tools/art_spec.md`.

Paths in those specs that mention `/home/claude/ht/videos/never-eat-human-meat-v3/` mean, for this video:
- plan: `/home/claude/youtube-script-daily/videos/<SLUG>/plan.json` (use the entries for YOUR uids; `bg`, `text`, `prev`, `nxt`, `transition_in`, `dur`)
- output: `/home/claude/youtube-script-daily/videos/<SLUG>/art3/<uid>.svg` and `<uid>.json`
- preview tool: `python3 /home/claude/youtube-script-daily/tools/svgshot.py <preview dir> f1.svg ...` (vertical: `SHOT_W=1080 SHOT_H=1920`)
- `<SLUG>` is given in your task (long video `ribeiroia-monster-frogs`, Shorts `ribeiroia-monster-frogs-short1` / `-short2`).
Write ONLY your own uids. Do not edit any other repo file. **Scratch work (generator scripts, previews) goes ONLY in your own folder** `/tmp/claude-0/-home-claude-youtube-script-daily/53bea993-48d4-5496-836b-a9dbb74ebe3e/scratchpad/<first uid>_<last uid>/` — other agents work in parallel; never write to a shared scratch file name.

## Topic
Ribeiroia ondatrae, a parasitic flatworm that gives frogs extra or missing legs. 1995 Minnesota pond (students with nets find deformed northern leopard frogs), state scientists wading in the pond, a 1996 scientists' meeting about suspects (pesticides, ultraviolet light, retinoic acid), California ponds with Pacific treefrogs, lab tanks with tadpoles, microscope views of cysts at the base of hind legs. Life cycle: ram's horn snail -> free-swimming cercariae -> tadpole limb buds (cysts) -> heron/duck/hawk -> eggs in droppings -> back to the pond. Fertilizer runoff, algae, more snails; diverse ponds protect frogs; global amphibian decline.

## Character / object sheet (keep identical across all agents)
- **Northern leopard frog** (Minnesota scenes): green-brown body `#6f8f4e`, rounded dark spots `#2f3f25` each with a thin pale rim, pale cream belly `#e6e2c0`, golden eye with a horizontal dark pupil.
- **Pacific treefrog** (California scenes): small, bright green `#7fb35a` (or tan), a dark stripe through the eye, round toe pads.
- **Malformed frog**: the same frog with ONE clear difference drawn calmly like a museum sketch: extra hind legs (2-4 small extra legs from the hip, mirror-image), or a missing leg (smooth stump outline), or skin webbing binding a leg. No blood, no wounds, no pain faces, never grotesque; the frog looks calm.
- **Tadpole**: olive-brown oval body `#6b6a3e` with a long finned tail; at later stages two tiny hind limb buds at the base of the tail (small rounded nubs).
- **Ram's horn snail**: flat, coiled (planispiral) shell, reddish-brown `#8a4a2e` with darker growth lines, soft grey-red body.
- **Cercariae**: tiny translucent larvae `#e8e4cf` with a body and a simple tail (like a tiny tadpole), drawn as small light shapes; **miracidium**: tiny oval with fine hair-like edge.
- **Cysts (metacercariae)**: small round pale beads `#f0e6c8` with a thin rim, clustered around the base of the hind limbs.
- **Great blue heron**: blue-grey `#7b8ea0` body, long neck, long yellow bill, dark crown stripe. Ducks and hawks generic.
- **People**: generic only. Students = small figures seen from behind with nets and rubber boots (no faces). Scientists (Judy Helgen, Pieter Johnson, Stan Sessions) are real people: NEVER a face or portrait; show hands, sleeves, waders, notebooks, microscopes, tanks.
- **Chemistry**: retinoic acid = a simple hexagon-chain molecule sketch WITHOUT letters; ultraviolet = a pale sun with a thin shield arc (no rays); pesticides = a sprayer or barrel, no labels.

## Notes
- Colours: every plan.json unit has `pal` (palette `forest` for most of the video; `lab` for microscope, tanks, journal, beads, chemistry; `history` for old records). Use ONLY `pal` colours for backgrounds, lines, glows and `pal.accents` for main subjects (art_spec.md section 3). The colour codes above are natural colours; tint them to harmonise with `pal`.
- No text inside pictures (no letters, numbers, labels, no newspaper headlines with words; use blank lines for text).
- `focus` on 40-50 % of units; sfx on 35-45 % using ONLY the 25 library names in art_spec.md section 8 (unpitched; vary — never the same name in two consecutive units). Good fits: splash, drip, bubble, rustle, wind, step, page, pencil, click, tick, flutter, sand.
- Motion groups: frogs and people `mv-breathe-<name>`, frog/heron heads `mv-nod-<name>`, legs/arms `mv-arm-<name>`, cercariae/bubbles `mv-cells-<name>` (float up), reeds `mv-lean-<name>`, glowing centre `mv-glint-core`. Ids unique inside each file.
- Final answer: one line per uid: `uid | centre | backdrop kind | focus_word or - | sfx or -`, plus problems left.
