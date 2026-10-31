# Agent brief: restyle people in existing pictures to the approved style ③ (owner decision 2026-10-17). Save tokens, report in at most 8 lines. Do NOT run git.

- Proportions: cute (body.py default `kind='cute'` adult 5.5 H, `'cute_child'` 4.5 H). OLD pictures: start from your orig/ copies and keep
  the original heads and bodies (they are already cute); fix only clearly broken bodies. NEW pictures: switch your figure helper to cute.
- Arms: `body.arm(...)` = one smooth path per arm, no visible elbow, one mv-limb link. `elbow_moves=True` only where the forearm really swings.
- Hands: ROUND by default (`fingers=False`). `fingers=True` only where needed: pointing, gripping a visible object, waving close-up,
  a hand that is the subject of the sentence, hand stencils/icons.
- Write the final files to the repo art3 (your own uids only). Keep sidecars valid (labels/focus that pointed at moved hands).
- Checks: XML valid, your pose check or mvcheck, labelshot if labels moved, ONE build into your scratch dir (fallback 0), ONE
  before/after contact sheet that you look at. No extra preview rounds unless something is broken.

**Attachment check (2026-10-29, mandatory):** every part you move or redraw must be attached to its body (`tools/art_spec.md` 7A). Before reporting run `python3 tools/attachcheck.py <slug> <your uids>` (0 problems) and look at `tools/motionaudit.py` strips for pictures with creatures, machines or hinged things; the lead re-checks the built page with `tools/final_check.py`. **Axis catalogue (same day):** name every moving group after the thing (head noun last, `tools/axis_catalog.md`), run `python3 tools/axisfix.py <slug> <your uids>` BEFORE attachcheck — it writes the axes; you do not pick them (art_spec 7A).

**Variety (2026-10-31, mandatory, art_spec 7B):** the video has a theme pack (`tools/concepts_catalog.md`, `python3 tools/concepts.py <slug>`). Over your units use >= 4 of its compositions and >= 5 of its motion kinds, and give at least 1 picture in 6 a moving, named small prop (`mv-core-drop` / `mv-rollby` / `mv-topple` / `mv-bouncing` / `mv-swing` / `mv-rise` / `mv-popin` / `mv-toss` / `mv-coast` …) off the subject. Before reporting run `python3 tools/variety_check.py <slug> --report` and put its object-kind count and prop count in your report.
