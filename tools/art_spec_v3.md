# Miya's Lab — per-unit picture spec v3 (read this AND art_spec_v2.md fully; v3 overrides v2 where they differ)

You draw ONE NEW PICTURE per narration unit (a sentence or clause, 2-7 s on screen). The list of your units (uid, text, background mode, transition, previous/next text) is in plan.json (path given in your task). The picture must show THAT unit's idea — a different composition from the neighbouring units, not a copy of the scene picture.

## Files (per unit)
- `/home/claude/ht/videos/never-eat-human-meat-v3/art3/<uid>.svg`  (1920x1080, rules of art_spec_v2: no filter/text/image/style/SMIL; unique ids; valid XML; keep each file under ~120 KB — a unit picture is simpler than a scene picture: one clear idea, 8-25 shapes groups, not a busy crowd)
- `/home/claude/ht/videos/never-eat-human-meat-v3/art3/<uid>.json`  sidecar (below)
- Previews: render with `python3 /home/claude/ht/tools/svgshot.py <your_preview_dir> file1.svg file2.svg ...` and LOOK at every picture with Read (check centre object, nothing cut off, style). Keep previews OUT of the art3 folder.

## Background mode
Use plan.json `bg` for every unit of the scene: "paper" (warm #e5e3dd, thin ink lines #1b1830), "night" (#0b0a21..#16142f, lavender/gold lines, soft glow), "dusk" (peach #f3c290 -> pink #d68673 -> violet #7c4577). Units of one scene share bg, palette and character looks (same person = same clothes/skin/hair across the scene's units; use the first unit you draw as the model).

## Composition rules
- Centre rule (v2): one round/bright focal object at (960,500), diameter 170-260 px. Radiating thin lines / rings around it.
- NEW: if `transition_in` is "match", the centre object of this picture must sit at (960,500) with ~the same size and colour family as the centre object of the PREVIOUS unit of the same scene (you draw them in order — look at your previous svg), because the cut grows the new picture out of that shape. Only vary what is inside/around it.
- If `transition_in` is "slide": keep important content away from the far left/right 150 px.
- NEW: the camera is STATIC unless the sidecar names a focus. Therefore the picture must read well as a still, and the objects mentioned in the text must be easy to see.
- Keep the bottom 200 px free of important content (captions), top-right 160x160 empty, important content inside x 120..1800, y 80..880.
- Consecutive units: change the viewpoint/subject (wide scene -> close object -> symbol/diagram -> person) so the sequence feels like new shots; same world, same palette. Metaphors for abstract ideas are welcome (as in v2).
- People: simplified, dignified, calm; no gore, no blood, no nudity, no violence shown, no stereotypes, no real people. Cannibalism / death topics are shown only through mourning scenes, symbols, hands, bowls, smoke, empty places — never graphic.
- Motion groups (v2 list: mv-breathe/nod/lean/arm/hand/walk, mv-flame/lamp/lantern/beacon/glint/spark, mv-smoke/steam/stink/cells/rain/key, mv-bell/knot, mv-antenna): 1-4 per picture; every visible person gets mv-breathe; the centre object gets `mv-glint-core` when it glows. Each unit is only 2-7 s long, so keep motions subtle.

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
- `sfx.name` must be one of: swish, shimmer, tick, crackle, bubble, wind, bell, click, creak, drip, thud, chime, rustle, pop. Use only when the unit text or picture has a matching event: fire/cooking -> crackle; boiling/liquid -> bubble; outdoors/mountain/open sky -> wind; bell/alarm/warning -> bell; lock/latch/closing/sealing -> click; wooden hut/door/scale/weight shifting -> creak; a single drop/tear/sample -> drip; something set down/heavy/final -> thud; a bright discovery/idea/sparkle -> shimmer or chime; paper/cloth/notes -> rustle; small appearing symbol -> pop. Roughly 35-45 % of units get one. `word` = the spoken words the sound belongs to. Never add drones/hums.
- Write the JSON with correct quoting (validate with python json).

## Work method
Draw units in the listed order. For each: read text (+prev/next), decide the picture, write svg + json, run svgshot for a batch of 3-4, Read the previews, fix at most once. Finish all your units. Final answer: one line per uid: `uid | centre | focus_word or - | sfx or -` and any problem.
