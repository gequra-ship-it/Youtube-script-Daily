# Agent brief: scene-matched motion, camera tracking and speech bubbles for EXISTING pictures (2026-10-22)
Owner rule (miya, repeated several times): motions, camera tracking and speech bubbles are NOT a fixed list of examples. For every unit you decide from
what ITS narration says happens. The building blocks are in `tools/art_spec.md` section 7 ("Object motions anywhere" paragraph) and guideline
`docs/guideline/04-motion.md` 4-1 (17 object motions, tracking camera) and `docs/guideline/03-illustration-style.md` 3-6 (speech bubbles).
Do NOT run git. Work only on the units you are given. Keep your scratch files in your own folder (`<scratch>/<you>/`). Report in at most 8 lines.

## Steps for each unit (uid in `videos/<slug>/plan.json`, picture `videos/<slug>/art3/<uid>.svg`, sidecar `<uid>.json`)
1. Read the unit text (plan.json `text`, plus `prev`/`nxt` for context) and look at the picture (render it with `python3 tools/labelshot.py` or any SVG renderer you have).
2. Write ONE sentence: what the narration says happens here (an event, a movement, a change, a relation, a feeling). If nothing moves in the text
   (plain explanation, a still fact), do not force a motion: leave the picture alone except for a speech bubble if one fits.
3. Pick the motion that shows exactly that. Combine kinds (`path` + `dash`, `flip` + `fill` + `shake`, `topple` row, `popin` + `edge`) or, if none of the 17 fits,
   say so in your report with the motion you want (do not edit `tools/motions.py` yourself; the lead will add it). Typical mapping examples are only examples.
4. Edit the SVG surgically: wrap the EXISTING shapes of the moving thing in `<g id="mv-<kind>-<name>" data-...>` (ids `mv-*` become classes, duplicates are fine;
   other ids must stay unique). Never delete the picture's current `mv-` groups or the centre object; keep the style (thin sketch lines, palette colours, no text in the SVG,
   no filters). `data-pivot="x y"` is in picture coordinates (1920x1080). `data-delay` (s after the picture starts, default 0.3) orders events inside the picture; the picture
   is 3.5-6 s long, so finish motions within about 4 s. Repeat a motion kind in neighbouring pictures only when the narration repeats the situation (2026-10-27 principle), not as a default filler.
5. Camera tracking (same rule, from the narration): if the text describes a long continuous movement, journey or survey (a creature crossing the scene, an arm reaching along a
   rock, a drifting current, scanning along a series), add an empty group `<g id="mv-track-<name>" data-path="M x y C ..." data-delay=".3" data-dur="3" data-scale="1.3"/>`
   whose path is where the camera centre goes (a picture with `mv-path-*` or 3+ `mv-topple-*` tracks automatically; `"track": false` in the sidecar turns it off).
   A tracking picture does not use `focus`; remove the sidecar `focus` and `focus_word` then.
6. Speech bubbles (`say`, sidecar `labels`): about 1 unit in 3 gets one, up to 2 when two things talk. Creatures, objects, people without a name. At most 4 words / 24 characters,
   no digits, a feeling or reaction, no facts, no real named person, `to` = the speaker's mouth/front, `word` = a word from the unit text. Not the same line twice in
   neighbouring units. Safe area x 120-1800, y 80-860 and not in the top-right corner (logo); keep clear of faces and the centre object. At most 3 labels per unit, 1 `name`/`num` kept as they are.
7. Sidecar: keep valid JSON; add `"motion": "<one short line: what you chose and why>"`.

## Checks (cheap, do them)
- `SLUG=<slug> python3 tools/motion_preview.py <scratch>/pv <uid> ... --times 0.5,1.5,2.5,3.5,4.5` -> `<uid>_motion.png` strips; look at ONE strip per kind of motion you used (not every unit).
  It must print `no page errors`.
- `python3 tools/labelshot.py <slug> <scratch>/lab <uid> ...` for the units with new bubbles; it prints problems (fix them).
- XML valid (python `xml.dom.minidom`), JSON valid.
Report: units changed / left alone, motion kinds used (counts), bubbles added, tracking pictures, wanted-but-missing motions, known flaws.
