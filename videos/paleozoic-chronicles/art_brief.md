# paleozoic-chronicles — art brief (shared by all picture agents)

Read fully: `tools/art_spec.md` (section 5 backdrop rules: the backdrop variety rules apply to NEW pictures too: no concentric rings, no radiating lines/rays/sunbursts; every picture gets a backdrop that fits its own text; neighbouring units must not share a backdrop kind; at most 2 of every 12 units share a kind). Vertical Shorts agents also follow section 10 of `tools/art_spec.md`.

Paths in those specs that mention `/home/claude/ht/videos/never-eat-human-meat-v3/` mean, for this video:
- plan: `/home/claude/youtube-script-daily/videos/<SLUG>/plan.json` (use the entries for YOUR uids; `bg`, `pal`, `text`, `prev`, `nxt`, `transition_in`, `dur`)
- output: `/home/claude/youtube-script-daily/videos/<SLUG>/art3/<uid>.svg` and `<uid>.json`
- preview tool: `python3 /home/claude/youtube-script-daily/tools/svgshot.py <preview dir> f1.svg ...` (vertical: `SHOT_W=1080 SHOT_H=1920`)
- `<SLUG>` is given in your task (long video `paleozoic-chronicles`, Shorts `paleozoic-chronicles-short1` / `-short2`).
Write ONLY your own uids. Do not edit any other repo file. **Scratch work (generator scripts, previews) goes ONLY in your own folder** `/tmp/claude-0/-home-claude-youtube-script-daily/53bea993-48d4-5496-836b-a9dbb74ebe3e/scratchpad/<first uid>_<last uid>/` (Shorts agents: prefix the folder with the slug) — other agents work in parallel; never write to a shared scratch file name.

## Topic
The Paleozoic Era, about 539 to 252 million years ago: Cambrian Explosion and the Burgess Shale (Canadian Rockies), Ordovician seas and the first land plants, the Late Ordovician ice age and extinction, Silurian vascular plants and the first land animals, the invention of jaws, sea scorpions, the Devonian Age of Fishes, lobe-finned fish and the first four-limbed animals, the first forests and the Late Devonian dead zones, Carboniferous coal swamps, high oxygen, giant insects and millipedes, the amniotic egg and the first reptiles, Permian Pangaea and its deserts, synapsids (Dimetrodon, gorgonopsians, cynodonts), the Siberian Traps eruptions, the Great Dying and the survivor Lystrosaurus. Modern framing scenes: a person feeling their heartbeat (opening) and a calm closing scene.

## Character / object sheet (keep identical across all agents; scientific look, not monster-movie)
- **Anomalocaris**: segmented flattened body with flaps along both sides, fan tail, two large stalked compound eyes, two spiny curved frontal arms, small round mouth underneath. Reddish-tan.
- **Trilobite**: oval three-lobed shell (central ridge + two side lobes), head shield with crescent eyes, segmented thorax, many small legs; some rolled into a ball. Grey-brown.
- **Opabinia**: small soft segmented body with side flaps and a tail fan, FIVE stalked eyes on top of the head, long flexible nozzle with a small claw at the tip. Pale pinkish.
- **Hallucigenia**: tiny worm-like body with paired spines on the back and thin legs underneath, small head.
- **Pikaia**: small leaf-shaped flattened swimmer with faint zig-zag muscle blocks and a rod along the back.
- **Nautiloid (Cameroceras-like)**: long straight cone shell with faint chamber lines, tentacles at the open end. Cream with brown bands.
- **Jawless fish (Sacabambaspis/Astraspis)**: small, bony plated head, eyes at the very front, open mouth with no jaw, scaly tail.
- **Sea scorpion (Pterygotus)**: long segmented body, paddle-like swimming legs, flat tail paddle, two long toothed claws in front. Olive-brown.
- **Dunkleosteus**: big armored head shield with bony blade jaws (no teeth), short stocky body (shorter and chunkier, NOT long shark-like), dark grey-blue.
- **Lobe-finned fish / Tiktaalik**: Tiktaalik = flat crocodile-like head, eyes on top, scales, sturdy front fins it props up on, shallow water. Acanthostega = salamander-like with a tail fin and paddle limbs with many fingers. No humans.
- **Plants**: Cooksonia = tiny bare Y-branching stems with round caps; Archaeopteris = tall tree with fern-like leafy branches; coal swamp = Lepidodendron/Sigillaria (tall straight trunks with diamond scale pattern, crowns of grassy leaves), tree ferns, giant horsetails.
- **Meganeura**: giant dragonfly-like insect, two pairs of long veined wings.
- **Arthropleura**: very long flat segmented millipede-like animal with many legs, brown.
- **Amniotic egg / Hylonomus**: leathery egg; Hylonomus = small lizard-like reptile, about 20 cm, inside/near a hollow fossil tree stump.
- **Dimetrodon**: sprawling four-legged synapsid, tall sail of spines on the back, large head with different-sized teeth. Earthy reddish-brown.
- **Gorgonopsian (Inostrancevia)**: dog-like/big-cat-like posture, long skull, two saber canines; calm stalking pose, no blood, no killing.
- **Cynodont (Procynosuchus)**: small dog-like animal, low body, near a burrow.
- **Lystrosaurus**: stocky pig-sized, barrel body, beaked face with two tusks, short legs, near a burrow.
- **Siberian Traps**: long fissure eruptions and stacked lava flows over wide land, gas clouds (no rays).
- **People**: generic only. Charles Walcott and other scientists are real people: NEVER a face or portrait — show hands, sleeves, hammers, notebooks, rock layers, a museum drawer. Modern scenes: a person seen from behind or side silhouette without detailed face.
- **Maps**: Pangaea as one large C-shaped supercontinent in one ocean; Gondwana over the South Pole with ice; no labels.

## Notes
- Colours: every plan.json unit has `pal` (`ocean` for Paleozoic seas, `forest` for land plants, coal forests and giant arthropods, `desert` for Permian Pangaea, the Great Dying and the opening/closing scenes). Use ONLY `pal` colours for backgrounds, lines, glows and `pal.accents` for main subjects (art_spec.md section 3). Natural colours above are guides; tint them to harmonise with `pal`.
- No text inside pictures (no letters, numbers, labels; time scales as blank tick marks only).
- Death and extinction shown with symbols and mood (empty shells, fading reef, drifting gas), never gore.
- `focus` on 40-50 % of units; sfx on 35-45 % using ONLY the 25 library names in art_spec.md section 8 (unpitched; vary — never the same name in two consecutive units). Good fits: bubble, splash, drip, wind, sand, stone, thud, rustle, crackle, flutter, step, page, pencil.
- Motion groups: animals and people `mv-breathe-<name>`, heads `mv-nod-<name>`, tails/legs/claws `mv-arm-<name>`, bubbles/gas/spores `mv-cells-<name>`, plants `mv-lean-<name>`, lava glow `mv-flame-<name>`, glowing centre `mv-glint-core`. Ids unique inside each file.
- Final answer: one line per uid: `uid | centre | backdrop kind | focus_word or - | sfx or -`, plus problems left.
