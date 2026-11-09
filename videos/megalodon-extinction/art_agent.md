# Picture agent instructions (megalodon-extinction family)
Repo /home/user/youtube-script-daily (branch render-pipeline). You draw ONLY the units named in your task. Do NOT run git. Do not touch render/, other uids, tools/, plan.json, thumb/.
1. Read `tools/art_spec.md` fully and `videos/megalodon-extinction/art_brief.md` (topic, character designs, vocabulary, rules; it applies to the long form and shorts 1-5).
2. Read `videos/<slug>/plan.json` for your units (text, prev, nxt, pal, bg, transition_in). Shorts (slug ends -shortN) are vertical 1080x1920: art_spec section 10, safe area y 288-1632, x 0-940. Long = 1920x1080.
3. Write `videos/<slug>/art3/<uid>.svg` + `<uid>.json` (sidecar spec section 8: labels, sfx, motions; choose from what each unit's narration says). Study two finished examples first (videos/deep-sea-giants/art3, videos/whale-fall/art3). Draw only what the narration states; keep Megalodon/great white/whale designs identical across pictures.
4. Per batch run: `SLUG=<slug> python3 tools/axisfix.py <slug>` (see tools/README.md for usage), then `python3 tools/attachcheck.py <slug> <your uids>` until 0, `xmllint --noout` on each svg, and one before/after contact sheet of your pictures with `python3 tools/svgshot.py` (see README) in your own scratch dir (not art3/).
5. Report in at most 8 lines: units done, any rule you could not meet, your token usage if visible.
