# Miya's Lab — per-unit picture spec v3 (read this AND art_spec_v2.md fully; v3 overrides v2 where they differ)

You draw ONE NEW PICTURE per narration unit (a sentence or clause, 2-7 s on screen). The list of your units (uid, text, background mode, transition, previous/next text) is in plan.json (path given in your task). The picture must show THAT unit's idea — a different composition from the neighbouring units, not a copy of the scene picture.

## Files (per unit)
- `/home/claude/ht/videos/never-eat-human-meat-v3/art3/<uid>.svg`  (1920x1080, rules of art_spec_v2: no filter/text/image/style/SMIL; unique ids; valid XML; keep each file under ~120 KB — a unit picture is simpler than a scene picture: one clear idea, 8-25 shapes groups, not a busy crowd)
- `/home/claude/ht/videos/never-eat-human-meat-v3/art3/<uid>.json`  sidecar (below)
- Previews: render with `python3 /home/claude/ht/tools/svgshot.py <your_preview_dir> file1.svg file2.svg ...` and LOOK at every picture with Read (check centre object, nothing cut off, style). Keep previews OUT of the art3 folder.

## Background mode
Use plan.json `bg` for every unit of the scene: "paper" (base `pal.paper_base`, thin lines `pal.paper_ink`), "night" (vertical wash `pal.night_top` -> `pal.night_bottom`, lines `pal.night_line`, glow `pal.night_glow`), "dusk" (gradient `pal.dusk_stops[0]` -> [1] -> [2], lines `pal.dusk_ink`). **Every plan.json unit has a `pal` object (palette chosen for the script topic, tools/palettes.py). Use ONLY `pal` colours for backgrounds, lines and glows, and `pal.accents` (4 colours) for the main subjects; natural colours of things (skin, animal bodies, plants, water) follow the art brief character sheet, tinted to harmonise with `pal`. Do NOT fall back to purple/magenta/orange unless `pal.palette` is "sunset" or the thing drawn is itself that colour.** Units of one scene share bg, palette and character looks (same person = same clothes/skin/hair across the scene's units; use the first unit you draw as the model).

## Composition rules
- Centre rule (v2): one round/bright focal object at (960,500), diameter 170-260 px. NO radiating lines and NO concentric rings (removed 2026-10-10: they repeated in every picture). Instead each picture gets a backdrop that fits its text (see art_spec_v4_backdrop.md): room, landscape, lab, microscope field, notebook page, timeline, etc.; vary it from unit to unit.
- NEW: if `transition_in` is "match", the centre object of this picture must sit at (960,500) with ~the same size and colour family as the centre object of the PREVIOUS unit of the same scene (you draw them in order — look at your previous svg), because the cut grows the new picture out of that shape. Only vary what is inside/around it.
- If `transition_in` is "slide": keep important content away from the far left/right 150 px.
- NEW: the camera is STATIC unless the sidecar names a focus. Therefore the picture must read well as a still, and the objects mentioned in the text must be easy to see.
- Keep the bottom 200 px free of important content (captions), top-right 160x160 empty, important content inside x 120..1800, y 80..880.
- Consecutive units: change the viewpoint/subject (wide scene -> close object -> symbol/diagram -> person) so the sequence feels like new shots; same world, same palette. Metaphors for abstract ideas are welcome (as in v2).
- People: simplified, dignified, calm; no gore, no blood, no nudity, no violence shown, no stereotypes, no real people. Cannibalism / death topics are shown only through mourning scenes, symbols, hands, bowls, smoke, empty places — never graphic.
- Motion groups (v2 list: mv-breathe/nod/lean/arm/hand/walk, mv-flame/lamp/lantern/beacon/glint/spark, mv-smoke/steam/stink/cells/rain/key, mv-bell/knot, mv-antenna): 1-4 per picture; every visible person gets mv-breathe; the centre object gets `mv-core-<type>` (always; pick the type by what the object is, see the table in `tools/motions.py` and guideline 4-1: spin, sway, orbit, glide, heartbeat, flicker, swell, tremble, approach, reveal, squeeze, wobble, roll). Never the same type in two neighbouring units, never a plain up-and-down bob; over a whole video use at least 10 different types, none above 20% of the pictures. Only if you do not set a type (`mv-glint-core`) the build assigns one by rotation. Each unit is only 2-7 s long, so keep motions subtle.

## Sidecar JSON (exact keys)
```
{
 "centre": "short English description of the centre object",
 "focus": [x, y, scale] or null,
 "focus_word": "exact words from the unit text when the narration says them" or null,
 "sfx": [ {"name": "<library name>", "word": "<exact words from the unit text>", "vol": 0.5-0.8} ]   // 0 or 1 entry
}
```
- `focus`: only if the text names a specific thing that should be looked at closely (a detail, an object, a number-bearing symbol). x,y = that thing's centre in the 1920x1080 picture, scale 1.5-2.2 (the camera zooms there and holds). Aim for focus on about 40-50 % of your units; otherwise null (picture stays still). `focus_word` must occur verbatim in the unit text (the camera starts moving shortly before it is spoken). The focused thing must be drawn with enough detail to survive 2x zoom.
- `sfx.name` must be one of: swish, hush, tick, crackle, bubble, wind, bell, click, creak, drip, thud, chime, rustle, pop, pencil, page, cloth, woodblock, sand, rain, splash, step, breath, stone, flutter, plus the cosmic set riser, sparkle, sweep, bloom, starfall, pulse, warp, glimmer (space videos, see art_spec_cosmic.md) (all soft, unpitched; `bell`/`chime` are now dull knock / paper flick, `shimmer` is an alias of `hush`). Use only when the unit text or picture has a matching event: fire/cooking -> crackle; boiling/liquid -> bubble; rain -> rain; water splash/pour -> splash; outdoors/mountain/open sky -> wind; alarm/warning/hollow -> bell or woodblock; lock/latch/closing/sealing -> click; wooden hut/door/scale -> creak; a single drop/tear/sample -> drip; something set down/heavy/final -> thud or stone; writing/notes/drawing -> pencil; book/paper/records -> page or rustle; clothing/robe/body movement -> cloth; walking/arrival -> step; sand/powder/grain -> sand; birds/wings/fluttering -> flutter; quiet/tension/breathing -> breath; small appearing symbol -> pop; idea/discovery -> hush (never a ringing tone). Pick the sound that fits the event and VARY the choice: the same name should not appear in two consecutive units. Roughly 35-45 % of units get one. `word` = the spoken words the sound belongs to. Never add drones, hums, bells or musical tones.
- Write the JSON with correct quoting (validate with python json).

## Work method
Draw units in the listed order. For each: read text (+prev/next), decide the picture, write svg + json, run svgshot for a batch of 3-4, Read the previews, fix at most once. Finish all your units. Final answer: one line per uid: `uid | centre | focus_word or - | sfx or -` and any problem.

## On-screen text — sidecar "labels" (guideline 3-6, 2026-10-11)
The SVG still has NO text. Text goes in the sidecar; the builder lays it over the picture as HTML (exact spelling, channel fonts). 0-3 labels per unit:
```
"labels": [
 {"type": "name", "text": "Anomalocaris", "x": 1320, "y": 300, "to": [1180, 470], "word": "Anomalocaris"},
 {"type": "num",  "text": "539 MILLION YEARS AGO", "word": "539 million"},
 {"type": "say",  "text": "Still here!", "x": 1080, "y": 520, "to": [1272, 650]}
]
```
- `name` (max 28 chars): the name of an animal, plant, place, era or object that is VISIBLE in your picture and SAID in this unit's text (same spelling, case may differ). x,y = centre of the label pill (about 34 px text, ~20 px per letter wide), `to` = a point on the subject (a thin pointer line + dot). Put the pill in empty space next to the subject, never over a face, the centre object or the thing the text is about. Do not repeat the same name in the next unit unless the picture changes subject.
- `num` (max 26 chars, UPPER CASE): a number, date, size or share that is SAID in this unit (digits or number words; "four meters" -> "4 M" is fine, "nine meters" -> "10 M" is not). It is fixed at the top-left of the screen (x 80-700, y 60-140; vertical x 100-700, y 330-400): when you use it, keep that corner free of important content. Write it short: "~3.5 M LONG", "539 MILLION YEARS AGO", "90%+ OF FOSSILS".
- `say` (max 4 words / 24 chars, no digits): a short speech bubble for an animal, a generic person or an object, `to` = its mouth. Only a reaction or feeling that fits the narration ("Still here!", "Too hot...", "Hmm?", "Not today!"), NEVER a fact, a number or a claim, and NEVER for a real named person. Use on about 1 unit in 8; keep it light and kind, not mocking.
- `word` (optional): exact words from this unit's text; the label pops in when they are spoken (else ~0.4 s after the cut).
- Safe area: landscape x 120-1800, y 80-860 (captions are below; no labels in the top-right logo corner x>1660, y<190); vertical x 100-940, y 300-1400. With a `focus`, labels move with the zoom (their size stays the same): the check also tests where they land after the zoom, so keep them close to the focus point.
- Aim: about half of your units get at least one label — names when a creature/place first appears on screen, a num badge whenever the narration states a number. Chalkboard units get none.
- Check + preview: `python3 /home/claude/youtube-script-daily/tools/labelshot.py <slug> <your preview dir> <uid> ...` prints problems (the build stops on any) and writes `<uid>_lab.png` with the labels and a sample caption on top — Read it and fix overlaps.
