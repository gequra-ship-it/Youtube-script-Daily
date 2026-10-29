# Agent brief: pictures for a REMAKE (reuse first). Fill in <slug> and the task lines when you launch the agent. 2026-10-17.
Owner: reuse existing pictures, draw as little as possible, save tokens. Do NOT run git. Report in at most 8 lines.
Repo /home/user/rp (branch render-pipeline). `export MIYA_WORK=/home/user/miya-work`. Read only the sections of tools/art_spec.md you need
(general SVG rules, 10 = vertical Shorts, 6A/6B = hands/people, 7 = motion groups).
People: cute proportions (tools/body.py default kind='cute', children 'cute_child'), one smooth arm per arm (body.arm), elbow link only where
the forearm really swings, ROUND hands unless fingers matter (pointing, gripping a visible object, waving close-up, hand is the subject, stencils/icons).
Sources (copy, then adapt; never edit the originals): the video's old art3 copy (horizontal 1920x1080, texts in its old plan.json) and the old
Shorts' art3 copies (vertical 1080x1920). Keep copies in your scratch folder before changing anything in the repo.
- Long video, NEEDS VARIANT units (same picture as the unit before): make a variant: re-crop/zoom about a different point + one added element
  that matches the unit's own text. Neighbours must differ.
- Shorts (vertical): reuse old vertical Shorts art first, then long-video art moved into the tall frame. Do NOT just scale the horizontal
  picture (leaves empty bands): scale ~1.1-1.2 with the centre object at (540,860), move side groups (people, palms, sun) inward and up/down,
  continue the ground/sky to the frame edges. Keep every mv-* id intact and ids unique (suffix per uid).
- Draw new only when no picture fits the unit text.
Sidecar json: keep valid; labels/focus/sfx words must be in THAT unit's text (drop the others).
Checks: XML valid; tools/mvcheck.py (it only sees the top 1080 px of a vertical frame); tools/labelshot.py if labels moved; ONE build
(`SLUG=<slug> [VERT=1] python3 tools/build3.py <scratch>/b`, fallback art must be 0); ONE contact sheet you look at. Delete your build dir afterwards (disk allowance is small).
Report: counts reused / adapted / new, sheet path, known flaws.

**Attachment check (2026-10-29, mandatory):** every part you move or redraw must be attached to its body (`tools/art_spec.md` 7A). Before reporting run `python3 tools/attachcheck.py <slug> <your uids>` (0 problems) and look at `tools/motionaudit.py` strips for pictures with creatures, machines or hinged things; the lead re-checks the built page with `tools/final_check.py`.
