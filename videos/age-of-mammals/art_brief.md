# age-of-mammals — art brief (shared by all picture agents)

Read fully: `tools/art_spec.md` (section 5 backdrop rules: the backdrop variety rules apply to NEW pictures too: no concentric rings, no radiating lines/rays/sunbursts; every picture gets a backdrop that fits its own text; neighbouring units must not share a backdrop kind; at most 2 of every 12 units share a kind). Vertical Shorts agents also follow section 10 of `tools/art_spec.md`.

Paths in those specs that mention `/home/claude/ht/videos/never-eat-human-meat-v3/` mean, for this video:
- plan: `/home/user/youtube-script-daily/videos/<SLUG>/plan.json` (use the entries for YOUR uids; `bg`, `text`, `prev`, `nxt`, `transition_in`, `dur`)
- output: `/home/user/youtube-script-daily/videos/<SLUG>/art3/<uid>.svg` and `<uid>.json`
- preview tool: `python3 /home/user/youtube-script-daily/tools/svgshot.py <preview dir> f1.svg ...` (vertical: `SHOT_W=1080 SHOT_H=1920`)

Write ONLY your own uids. Do not edit any other repo file. Scratch work (generator scripts, previews) goes ONLY in your own folder `/tmp/miya-scratch/<first uid>_<last uid>/`; other agents work in parallel, never write to a shared scratch file name.

## Topic
The Age of Mammals (Cenozoic, 66 million years ago to today). Late Cretaceous forest with small nocturnal mammals under sauropods; asteroid impact, darkness, ash; birds as the last dinosaurs; Paleocene diversification (milk, placenta, dens); Eocene greenhouse jungle, early primates (forward eyes, grasping hands), early bats, whales evolving from land mammals; Antarctica freezing, drying Oligocene woodland, indricotheres; Miocene grass, silica, tall teeth, hooves, predators; continents colliding, Panama land bridge and animal exchange; East African Rift, savanna, standing upright, free hands, stone tools, bone marrow, brains; Ice Age (glaciers, mammoths, sabre-toothed cats, ground sloths), fire, cave painting, farming, villages, clay tablets; closing on your own hand and a campfire.

## Character / object sheet (keep identical across all agents)
- **Early mammals**: shrew-like, 8-12 cm, soft grey-brown fur `#8a7a66`, paler belly `#cdbfa6`, pointed snout, big dark eyes, small round ears, thin tail. Always calm and cute, never hurt.
- **Dinosaurs**: sauropods grey-green `#7d8f78` with long necks and heavy legs; meat-eaters only as dim silhouettes with a glint of teeth. No blood, no gore, no carcasses. Birds: ordinary small songbirds on a wire for the modern tie-in.
- **Asteroid**: dark rock with a glowing orange-white edge, small trailing glow (no rays, no radiating lines); crater = a soft round basin seen from above, shown as a landscape, no concentric rings.
- **Primates / bats / whale ancestors**: small tree primate with orange-brown fur `#b9784a`, huge forward eyes, flat-nailed hands; early bat with skin wings, dark brown `#5e4a3f`; Pakicetus-like wader = lean wolf-shaped animal, grey-brown `#7a7367`, standing in shallow water; later whale = sleek blue-grey `#5a7391`.
- **Indricothere**: huge hornless rhino-like animal, long neck and legs, dusty tan `#b49b79`, tiny people-scale comparison optional (a distant small tree-top).
- **Grazers**: early horse = small dog-size, cream-brown `#c7a67c`, several toes; later horse/antelope = long-legged, tan `#c49a63`, hooves. Predators: lean cat-like and dog-like silhouettes, tawny `#c98f4f`.
- **Hominins**: australopithecine (Lucy) = small, upright, dark-brown skin, dark short hair, bare simple form, no clothes detail; early Homo = taller, simple hide wraps `#9a7b57`; Homo sapiens = diverse skin tones, hide clothing, calm and dignified (guideline 3-1 body rules apply); Neanderthal = stocky, heavy brow, same dignity. Hands via tools/hands.py. No faces beyond dot eyes.
- **Ice Age animals**: woolly mammoth = dark brown shaggy `#6b4a36`, tusks cream `#e8dcc0`; sabre-toothed cat tawny; giant ground sloth = shaggy reddish-brown `#8a5a3c`.
- **Fire / hearth**: orange-gold flame `#f2a53a`, glow as soft radial gradient (no rays); cave walls ochre `#c8793a` and charcoal for paintings (bison, horses as simple strokes).
- **Humans today**: a viewer's hand held up, palm lit by warm light; a campfire gathering of small silhouettes.

## Notes
- Colours: every plan.json unit has `pal` (forest for most; storm for the impact; ice for glaciers; desert for savanna and early humans; history for dates, villages, writing; body for mammal biology). Use ONLY `pal` colours for backgrounds, lines, glows and `pal.accents` for main subjects (art_spec.md section 3). The colour codes above are natural colours; tint them to harmonise with `pal`.
- No text inside pictures (no letters, numbers, labels).
- Different pictures need clearly different backdrops (art_spec.md section 5); several units are in the same place/time (e.g. the Cretaceous forest, the savanna) so vary the view, camera angle and what stands in the middle.
- `focus` on 40-50 % of units; sfx on 35-45 % using ONLY the 25 library names in art_spec.md section 8 (unpitched; vary, never the same name in two consecutive units). Good fits: rustle, step, wind, thud, stone, crackle, flutter, creak, sand, pencil, page, pop.
- Motion groups: animals `mv-breathe-<name>`, heads `mv-nod-<name>`, legs/tails `mv-joint-<name>`, fire `mv-flame-<name>`, smoke/ash `mv-smoke-<name>`; centre object `mv-core-<type>` or `mv-glint-core` (art_spec.md 7). Animals with moving parts (wings, propellers) follow the rotor/joint rule. Ids unique inside each file.
- Final answer: one line per uid: `uid | centre | backdrop kind | focus_word or - | sfx or -`, plus problems left.
