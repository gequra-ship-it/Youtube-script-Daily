# whale-fall — art brief (shared by all picture agents)

Read fully, in this order: `/home/claude/youtube-script-daily/tools/art_spec_v2.md`, `tools/art_spec_v3.md`, `tools/art_spec_v4_backdrop.md` (the backdrop variety rules apply to NEW pictures too: no concentric rings, no radiating lines/rays/sunbursts; every picture gets a backdrop that fits its own text; neighbouring units must not share a backdrop kind; at most 2 of every 12 units share a kind). Vertical Shorts agents also read `tools/art_spec_v3_vertical.md`.

Paths in those specs that mention `/home/claude/ht/videos/never-eat-human-meat-v3/` mean, for this video:
- plan: `/home/claude/youtube-script-daily/videos/<SLUG>/plan.json` (use the entries for YOUR uids; `bg`, `text`, `prev`, `nxt`, `transition_in`, `dur`)
- output: `/home/claude/youtube-script-daily/videos/<SLUG>/art3/<uid>.svg` and `<uid>.json`
- preview tool: `python3 /home/claude/youtube-script-daily/tools/svgshot.py <preview dir> f1.svg ...` (vertical: `SHOT_W=1080 SHOT_H=1920`)
- `<SLUG>` is given in your task (long video `whale-fall`, Shorts `whale-fall-short1` / `-short2`).
Write ONLY your own uids. Do not edit any other repo file. **Scratch work (generator scripts, previews) goes ONLY in your own folder** `/tmp/claude-0/-home-claude-youtube-script-daily/53bea993-48d4-5496-836b-a9dbb74ebe3e/scratchpad/<first uid>_<last uid>/` — other agents work in parallel; never write to a shared scratch file name.

## Topic
Whale falls: a dead whale sinks to the deep seafloor and feeds an ecosystem for decades. Surface ocean at dusk, sinking through ocean layers (sunlit -> twilight -> dark), marine snow, the abyssal mud plain. Stages: mobile scavengers (sleeper sharks, hagfish, crabs, squat lobsters, amphipods, giant isopods), enrichment opportunists (bristle worms, snails, tiny crustaceans in the mud), sulfophilic stage (bacterial mats, hydrogen sulfide, chemosynthetic clams), reef stage (sponges, corals on bare bone). Osedax bone-eating worms. Fossil whale bones with borings, a plesiosaur and sea-turtle fossil, sunken wood with boring clams, research submersibles/ROVs, sonar survey, whaling ships (historical, no killing shown), carbon.

## Character / object sheet (keep identical across all agents)
- **Whale carcass / living whale**: blue-grey `#5a7391` back, paler belly `#b9c6d3`, long throat grooves (thin lines), small dorsal fin. Living whale = blue whale or gray whale silhouette, calm. The carcass lies on its side on the mud; never show wounds, blood, guts or rot — scavenging = animals clustered on the body, soft shading, missing parts shown as a clean outline gap.
- **Whale skeleton**: cream bone `#e8dcc0` with soft amber shading `#c9a86a` (fat-rich), long spine of vertebrae, ribs arching, jaw bones; museum-sketch look.
- **Osedax worm**: small stalk with a feathery red-pink plume `#d64b6a` on top (like a tiny flower), green-tinted root lobes `#6f9a5a` spreading into the bone (show roots inside a cut-away bone). Females only visible; males = tiny dots inside a clear tube.
- **Sleeper shark**: heavy, slow, grey-brown `#5d5a52`, small fins, small eye. **Hagfish**: pink-grey `#b88f86` eel-shape, no fins, no jaws, small barbels. **Giant isopod**: armoured pill-bug shape, lilac-grey `#a99bb5`, segmented plates, many legs. **Squat lobster/crab**: orange-red `#d9694a`. **Bristle worms**: thin pink worms with side bristles. **Clams**: pale oval shells half in mud. **Bacterial mats**: white-yellow `#f2e9b8` fuzzy patches with a faint glow.
- **Plesiosaur / sea turtle fossil**: bone sketches in rock, a ghostly outline of the living animal only as a faint dashed line.
- **Submersible / ROV**: small white-yellow vehicle with lights (lights = soft glow, no beams/rays).
- **People**: generic only (a viewer looking at the sea, scientists as hands/sleeves/notebooks, sailors as small silhouettes on an old ship). No real person, no faces.

## Notes
- Colours: every plan.json unit has `pal` (palette `ocean` for most of the video; `history` for whaling and fossil scenes; `lab` for discovery, survey and ROV scenes). Use ONLY `pal` colours for backgrounds, lines, glows and `pal.accents` for main subjects (art_spec_v3.md). The colour codes in the character sheet below are the natural colours of the animals; tint them to harmonise with `pal`.
- No text inside pictures (no letters, numbers, labels).
- The deep sea is dark: most deep scenes use the night palette; keep animals readable with soft glow and thin light lines.
- `focus` on 40-50 % of units; sfx on 35-45 % using ONLY the 25 library names in art_spec_v3.md (unpitched; vary — never the same name in two consecutive units). Good fits: bubble, drip, splash, sand, thud, flutter, stone, creak, page, pencil, wind, rustle.
- Motion groups: whales `mv-breathe-<name>`, fins/tails `mv-arm-<name>`, plumes `mv-lean-<name>`, bubbles/marine snow `mv-cells-<name>` (float up) — glowing centre `mv-glint-core`. Ids unique inside each file.
- Final answer: one line per uid: `uid | centre | backdrop kind | focus_word or - | sfx or -`, plus problems left.
