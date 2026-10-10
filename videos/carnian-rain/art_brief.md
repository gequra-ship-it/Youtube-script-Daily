# carnian-rain — art brief (shared by all picture agents)

Read fully, in this order: `/home/claude/youtube-script-daily/tools/art_spec_v2.md`, `tools/art_spec_v3.md`, `tools/art_spec_v4_backdrop.md` (the backdrop variety rules apply to NEW pictures too: no concentric rings, no radiating lines/rays/sunbursts; every picture gets a backdrop that fits its own text; neighbouring units must not share a backdrop kind; at most 2 of every 12 units share a kind). Vertical Shorts agents also read `tools/art_spec_v3_vertical.md`.

Paths in those specs that mention `/home/claude/ht/videos/never-eat-human-meat-v3/` mean, for this video:
- plan: `/home/claude/youtube-script-daily/videos/<SLUG>/plan.json` (use the entries for YOUR uids; `bg`, `text`, `prev`, `nxt`, `transition_in`, `dur`)
- output: `/home/claude/youtube-script-daily/videos/<SLUG>/art3/<uid>.svg` and `<uid>.json`
- preview tool: `python3 /home/claude/youtube-script-daily/tools/svgshot.py <preview dir> f1.svg ...` (vertical: `SHOT_W=1080 SHOT_H=1920`)
- `<SLUG>` is given in your task (long video `carnian-rain`, Shorts `carnian-rain-short1` / `-short2`).
Write ONLY your own uids. Do not edit any other repo file. **Scratch work (generator scripts, previews) goes ONLY in your own folder** `/tmp/claude-0/-home-claude-youtube-script-daily/53bea993-48d4-5496-836b-a9dbb74ebe3e/scratchpad/<first uid>_<last uid>/` — other agents work in parallel; never write to a shared scratch file name.

## Topic
The Carnian Pluvial Episode, about 234-232 million years ago (Late Triassic): supercontinent Pangaea in one ocean (Panthalassa), dry red landscapes, Wrangellia volcanic fissure eruptions in the ocean, warming and a stronger water cycle (mega-monsoon), several wet pulses over 1-2 million years, rivers/lakes/wetlands, kaolinite clay, the oldest amber with mites and a fly, marine losses (ammonoids, conodonts, crinoids, bryozoans), black shales, new stony coral reefs and plankton (coccolithophores, dinoflagellates), conifers/ferns, pollen studies, rhynchosaurs declining, dinosaur footprints in the Dolomites, Ischigualasto (Argentina) early dinosaurs, modern scenes (rain on a window, a museum skeleton).

## Character / object sheet (keep identical across all agents)
- **Rhynchosaur** (Hyperodapedon-like): stout, barrel-bodied, sprawling legs, broad triangular head with a hooked beak-like snout, grey-brown `#8a7a62` with a paler belly.
- **Dicynodont**: barrel body, short legs, beaked face with two small tusks, olive-tan `#9a8a5a`.
- **Pseudosuchians**: rauisuchian predator = long crocodile-like head, deep body, legs held under the body, dark brown-olive `#5e5038`; aetosaur = low armored plant-eater with rows of plates and side spikes, earthy brown.
- **Eoraptor**: small (about 1 m), slim, bipedal, long tail, small head, scaly (NO feathers), sandy `#c9a06a` with darker stripes.
- **Herrerasaurus**: larger bipedal predator, long jaws with curved teeth, scaly, rust-brown `#a3583a` with darker back. Calm or striding; no blood, no killing.
- **Early mammal relative (mammaliamorph)**: tiny shrew-like furry animal, big dark eyes, grey-brown.
- **Plants**: conifers (tall, layered branches), ferns, bennettitaleans (cycad-like trunks with fronds), seed ferns.
- **Sea life**: ammonoid (coiled ribbed shell with tentacles), conodont (small eel-like animal, big eyes), crinoid (sea lily on a stalk), stony corals (branching and brain-like colonies), coccolithophore (tiny sphere covered in round plates), dinoflagellate (tiny armored cell with a whip tail), ichthyosaur (dolphin-shaped reptile).
- **Amber**: golden translucent drop with a tiny mite inside.
- **Volcanoes**: long fissure eruptions on the sea floor / ocean islands, basalt lava flows, rising gas plumes (no rays).
- **People**: generic only. The geologists Michael Simms and Alastair Ruffell, Mike Benton, Massimo Bernardi and Jacopo Dal Corso are real people: NEVER a face or portrait; show hands, sleeves, hammers, notebooks, rock layers, microscopes. Modern scenes: a person seen from behind at a rainy window or in a museum.
- **Maps**: Pangaea as one C-shaped supercontinent around the equator inside one ocean; no labels.

## Notes
- Colours: every plan.json unit has `pal` (palette `desert` for dry lands, volcanoes and dinosaurs; `forest` for rain, rivers, plants and amber; `ocean` for the sea scenes). Use ONLY `pal` colours for backgrounds, lines, glows and `pal.accents` for main subjects (art_spec_v3.md). The colour codes above are natural colours; tint them to harmonise with `pal`.
- No text inside pictures (no letters, numbers, labels; time scales as blank tick marks only).
- `focus` on 40-50 % of units; sfx on 35-45 % using ONLY the 25 library names in art_spec_v3.md (unpitched; vary — never the same name in two consecutive units). Good fits: rain, drip, wind, thud, stone, sand, step, crackle, bubble, splash, page, pencil, rustle.
- Motion groups: animals and people `mv-breathe-<name>`, heads `mv-nod-<name>`, tails/legs `mv-arm-<name>`, rain/bubbles/gas `mv-cells-<name>` or `mv-rain-<name>`, plants `mv-lean-<name>`, lava glow `mv-flame-<name>`, glowing centre `mv-glint-core`. Ids unique inside each file.
- Final answer: one line per uid: `uid | centre | backdrop kind | focus_word or - | sfx or -`, plus problems left.
