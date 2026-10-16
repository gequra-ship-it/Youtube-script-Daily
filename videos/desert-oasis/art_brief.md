# desert-oasis — art brief (shared by all picture agents)

Read fully: `tools/art_spec.md` (section 5 backdrop rules: the backdrop variety rules apply to NEW pictures too: no concentric rings, no radiating lines/rays/sunbursts; every picture gets a backdrop that fits its own text; neighbouring units must not share a backdrop kind; at most 2 of every 12 units share a kind). Vertical Shorts agents also follow section 10 of `tools/art_spec.md`.

Paths in those specs that mention `/home/claude/ht/videos/never-eat-human-meat-v3/` mean, for this video:
- plan: `/home/claude/youtube-script-daily/videos/<SLUG>/plan.json` (use the entries for YOUR uids; `bg`, `pal`, `text`, `prev`, `nxt`, `transition_in`, `dur`)
- output: `/home/claude/youtube-script-daily/videos/<SLUG>/art3/<uid>.svg` and `<uid>.json`
- preview tool: `python3 /home/claude/youtube-script-daily/tools/svgshot.py <preview dir> f1.svg ...` (vertical: `SHOT_W=1080 SHOT_H=1920`)
- `<SLUG>` is given in your task (long video `desert-oasis`, Shorts `desert-oasis-short1` / `-short2`).
Write ONLY your own uids. Do not edit any other repo file. **Scratch work (generator scripts, previews) goes ONLY in your own folder** `/tmp/claude-0/-home-claude-youtube-script-daily/53bea993-48d4-5496-836b-a9dbb74ebe3e/scratchpad/<first uid>_<last uid>/` (Shorts agents: prefix the folder with the slug) — other agents work in parallel; never write to a shared scratch file name.

## Topic
How desert oases are made: dunes and heat shimmer, mirages, oasis springs with date palms; why deserts are dry (sinking air near 30 degrees latitude); cut-away cross-sections of rock layers (sandstone aquifers, clay/shale aquitards, faults, water table); rain on distant mountains seeping underground; artesian pressure (garden-hose idea); Siwa Oasis in Egypt (springs, palms, olive trees, salty lakes, mudbrick old town); the Green Sahara 11,000-6,000 years ago (savanna, lakes, elephants, giraffes, hippos, rock art); fossil water and isotope dating; wind deflation and the Qattara Depression (salt flats); faults and the desert fan palms of the Coachella Valley along the San Andreas Fault; flash floods in wadis, water under gravel; the Nile as a long oasis fed by Ethiopian Highland rain; birds and wind bringing seeds; the date palm and three-layer oasis farming (palms, fruit trees, vegetables); Al-Ahsa, the largest oasis (vast palm groves); qanats (mother well, gently sloping tunnel, line of vertical shafts), foggara, falaj, karez, puquios; Silk Road caravans and oasis cities (Dunhuang, Samarkand, Palmyra — generic architecture, no text); barchan dunes and palm-frond fences; salt crusts (salinization); center-pivot fields from space; dried springs; Libya's Great Man-Made River (huge buried concrete pipes); desalination plants (reverse osmosis); Atacama fog nets; swales and mulch; Cuatro Ciénegas spring pools (pupfish, snails, aquatic box turtle, stromatolites); wildlife (gazelles, fennec foxes, migrating birds); shuttle radar revealing buried river valleys; land subsidence; water-sharing by time in oases; climate pressure; a calm ending at a pool at dusk.

## Character / object sheet (keep identical across all agents)
- **Traveler (recurring)**: adult in a loose sand-coloured tunic, teal head scarf, sandals, carrying a waterskin; calm and dignified.
- **Oasis farmers / villagers**: generic people in light cotton clothes and head cloths, varied skin tones; dignified, no stereotypes.
- **Scientists**: generic, seen from behind or in profile, lab coats or field vests.
- **Real people** (Ibn Chabbat, researchers): never a face or portrait — show hands, manuscripts with blank lines, tools.
- **Date palm**: tall slightly curved trunk with diamond leaf-scar pattern, crown of long feathery fronds, hanging date clusters.
- **Desert fan palm (Washingtonia)**: thick straight trunk with a skirt of dry hanging leaves, fan-shaped leaves.
- **Cross-sections**: clean geological cut-away, layers in palette tints, water shown as soft blue dots/flow arrows (no letters).
- **Camels**: dromedaries (one hump) for Sahara/Arabia, Bactrian (two humps) only for Central Asia Silk Road scenes.

## Notes
- Colours: every plan.json unit has `pal` (`desert` default; `ocean` for underground water, aquifers, pressure, fog and pools; `forest` for the Green Sahara). Use ONLY `pal` colours for backgrounds, lines, glows and `pal.accents` for main subjects.
- No text inside pictures (no letters, numbers, labels, signs).
- `focus` on 40-50 % of units; sfx on 35-45 % using ONLY the 25 library names in art_spec.md section 8 (unpitched; never the same name in two consecutive units). Good fits: wind, sand, drip, splash, bubble, rain, stone, step, rustle, flutter, page, creak, breath.
- **On-screen text**: also write `"labels"` in each sidecar following the "On-screen text — sidecar labels" part of section 8 of `tools/art_spec.md` (names that are visible AND said in the unit text, a `num` badge when the unit says a number, a short `say` bubble on about 1 unit in 8 — never for a real person). Then run `python3 /home/claude/youtube-script-daily/tools/labelshot.py <SLUG> <your scratch>/lab <uids...>`; fix every reported problem and look at every `<uid>_lab.png`.
- Motion groups: people `mv-breathe-<name>`, heads `mv-nod-<name>`, arms `mv-arm-<name>` (draw each arm as an open path that starts or ends at the SHOULDER; the builder rotates it around the end nearest the body — see art_spec.md section 7), hands `mv-hand-<name>`, palm crowns `mv-lean-<name>`, water ripples/bubbles/dust `mv-cells-<name>`, heat shimmer `mv-smoke-<name>`, flames `mv-flame-<name>`, glowing centre `mv-glint-core`. Ids unique inside each file.
- Final answer: one line per uid: `uid | centre | backdrop kind | focus_word or - | sfx or - | labels count`, plus problems left.
