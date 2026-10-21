# octopus-alien-mind — art brief (shared by all picture agents)

Read fully: `tools/art_spec.md` (section 5 backdrop rules: every picture gets a backdrop that fits its own text, no concentric rings or radiating-line/ray/sunburst backdrops, neighbouring units never share a backdrop kind, at most 2 of every 12 units share a kind; people follow 6A/6B with `tools/body.py` and `tools/hands.py`; sidecar JSON keys incl. `labels`, `focus`, `focus_word`, `sfx`, `centre`).

Paths: repo root is `/home/user/youtube-script-daily`.
- plan: `videos/octopus-alien-mind/plan.json` (use the entries for YOUR uids: `bg`, `pal`, `text`, `prev`, `nxt`, `transition_in`, `dur`)
- output: `videos/octopus-alien-mind/art3/<uid>.svg` and `<uid>.json`
- preview: `python3 tools/svgshot.py <preview dir> f1.svg ...`
Write ONLY your own uids. Scratch work (generator scripts, previews) goes ONLY in your own folder given in your task. No git. Delete big preview dirs when done.

## Topic
The octopus as an "alien mind" on Earth, as natural history and biology: a deep reef at night where a rock turns into an octopus; a glass aquarium wall with an eye looking back; the ancient sea floor with a small worm-like animal (600 million years ago); two branches of a tree of life (vertebrate on one side, mollusk on the other); clams, oysters and snails with shells; an animal shrinking its shell (cutaway: shell moving inside the body, then gone); an octopus squeezing through a gap barely larger than its beak; glowing neuron clouds (brain vs arms); a cut arm still reaching; suckers tasting a rock; manager (central brain) and workers (arms) as a simple diagram; camouflage on kelp, a mossy rock and coral; skin cross-section with three layers (pigment sacs, shimmering mirror cells, white scatter cells); colour pixels flickering; skin bumps (papillae) forming spikes; an eye with a horizontal slit pupil (colour-blind puzzle); light splitting into slightly different focus depths (chromatic aberration diagram); skin patch glowing in light; veined octopus walking on stilt-like arms carrying two coconut shell halves, then hiding inside them; a jar with a crab and a screw lid; Inky's night escape (tank lid gap, wet floor, drainpipe to the sea, moonlit bay); an octopus squirting a jet at a lamp; two keepers in the same shirt (one feeds, one holds a bristly stick) and an octopus reaching toward one and away from the other; an octopus pushing a floating pill bottle into a water jet; DNA -> RNA -> protein with scissors-like enzymes changing letters (coloured beads, no letters); polar sea with ice and a nerve cell; genome strip with locked regions; blue blood vessels and a hemocyanin copper atom; three hearts in a cutaway; an octopus jetting away with its heart pausing; mimic octopus as lionfish, sea snake, flatfish; hourglass and sand; mother octopus guarding eggs (calm, dignified, never gory), hatchlings drifting; a tiny gland near the eye; a lonely hatchling in plankton; a parallel-world sketch of an undersea city (only as imagination, clearly a thought bubble); a tree of life with two glowing tips; an aquarium eye close-up; a telescope looking at stars then the ocean floor; a living kaleidoscope; a montage of reef scenes; sunset surface with subscribe-friendly warmth.

## Character / object sheet (keep identical across all agents)
- **Octopus (recurring hero, common octopus)**: round bulb-shaped mantle (head and body), eight arms of unequal gentle curl with two rows of small round suckers on the underside, large side-set eyes with golden iris and a horizontal slit pupil, a small siphon tube under the eye. Base colour warm reddish-brown `#b4553f` with lighter belly `#e9b9a0`; colours shift with the scene (it camouflages), but anatomy stays right: EXACTLY 8 arms, no tentacles with clubs, no fins on the mantle.
- **Diver / scientist (recurring)**: adult, light-tan skin, dark ponytail, dot eyes, teal wetsuit or white lab coat with blue gloves; cute proportions via `tools/body.py` (kind='cute').
- **Aquarium keeper (recurring)**: adult, dark skin, short curly hair, dot eyes, navy polo shirt, rubber boots. The two keepers in the face-recognition unit wear the SAME shirt; the second one has medium-brown skin and a ponytail.
- **Real people (Godfrey-Smith, Wodinsky) and named animals (Inky, Otto)**: no portraits. Show a book on a shelf, a lab bench, a lamp; Inky is just an octopus.
- Other animals (damselfish, lionfish, sea snake, flatfish, mimic octopus, hatchlings, cuttlefish, squid, crab) are NOT fixed: draw the view that fits THIS unit. The mimic octopus is a brown-and-white banded octopus.
- Colours from `pal`; deep sea blues and teals dominate; skin/ink details may use extra colours.

## Care points
- No text or numbers anywhere in the SVG (sidecar `labels` only). Letters of DNA/RNA are coloured beads; the ink-ring and symbols have no letters.
- Death and decline (mother octopus, severed arm): dignity, symbols and mood only. No blood, no gore, no visible wound; a cut arm is shown as a clean stump in shadow or just the arm reaching.
- Octopus pupils horizontal slit; cuttlefish pupil U-shaped (only in the chromatic aberration unit).
- Octopuses have no shell; do not add one except in the shell-shrinking unit. Squid and cuttlefish have a small inner support.
- Tool use: veined octopus holds two half coconut shells (hollow domes) with arms like stilts.
