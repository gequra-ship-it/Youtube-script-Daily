# Miya's Lab — SVG scene art spec v2 (read fully)

Goal: redraw scenes in the style of the reference motion piece. LOOK at the reference first:
/tmp/claude-0/-home-claude/5155a11f-00a7-5c8c-a875-26fa5c990302/scratchpad/ref/sheet1.png (32 frames, 1 per second) and t1.png/t2.png/t3.png in the same folder (transition sequences).
Reference traits (measured/seen): two background modes — warm paper (#e5e3dd, sketchy thin pencil lines) and deep night navy (#0b0a21 to #16142f with soft vignette); rich but soft colour. **COLOURS COME FROM THE VIDEO'S PALETTE (plan.json `pal`, defined in tools/palettes.py), not from this file**: the old defaults (purple #6b4bd6, magenta #d64b9a, orange #d9694a, peach-to-pink-to-violet dusk) are only for the 'sunset' palette and made every video look purple/orange (user complaint 2026-10-10); thin hand-drawn ink lines, NOT thick black outlines; soft gradients and glow are allowed; hatching strokes for shading; small glowing focal element; one clear round/central focal object per shot.

## File rules
- Output: /home/claude/vid3/art/<id>.svg (ids are given in your task); previews /home/claude/vid3/art/preview/<id>.png.
- `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1920 1080" width="1920" height="1080">`
- Allowed: shapes, paths, groups, `<linearGradient>`, `<radialGradient>`, opacity, stroke-dasharray, `<clipPath>`. FORBIDDEN: `<filter>` (any), `<image>`, `<text>`/letters/numbers anywhere, CSS/SMIL animation, `<style>`, `<foreignObject>`. Glow = stacked circles with radialGradient from the colour to opacity 0.
- Ids must be unique inside the file; every `url(#id)` must resolve.
- Size under ~600 KB; valid XML (`xmllint --noout file.svg`).

## Look
- Pick ONE background mode per scene: "paper" (everyday, human, historical, lab, hospital) or "night" (molecules, brain, space-like or abstract science, ominous ideas). Use at least 8 paper and at least 8 night scenes overall; the rest may be dusk/sky gradients (peach #f3c290 -> pink #d68673 -> violet #7c4577) like the sunflower/starling frames.
- Linework: `pal.paper_ink` on paper scenes, `pal.night_line` (+ `pal.night_glow` for glows) on night scenes, `pal.dusk_ink` on dusk scenes; stroke-width 2.5-4 (up to 6 for the main subject); lines slightly wobbly (use cubic curves, not perfect geometry); 1-2 hatching groups for shading. NO uniform thick black outline around every object.
- Shading: soft gradients on big forms (sky, glow, rounded bodies), hatching for texture. Colour fills may be saturated but harmonious; no neon-on-white.
- People: simplified, dignified, readable silhouettes with a few clothing details, small dot eyes, calm faces; varied skin tones; respectful, no caricature. No gore, no blood, no nudity, no violence shown, no famous persons, no logos.
- Story first: the picture must show the narration's idea clearly (see script.py scene text) via a metaphor object, not a busy crowd.

## THE CENTRE RULE (most important)
The video zooms INTO the exact centre of every picture (to 2.6x) to cut to the next scene, and arrives zoomed on the centre of the next one. So:
- Put ONE round (or roughly round) focal object centred at (960, 500), diameter 170-260 px (an eye, lens, lamp, bowl, moon, cell, dial, porthole, flame, coin, doorway...) with a bright or high-contrast core. Everything else is arranged around it, nothing important on top of it.
- Do NOT add radiating lines or concentric rings around the centre (removed 2026-10-10: they repeated in every picture). Give each picture a backdrop that fits its text instead — see tools/art_spec_v4_backdrop.md.
- The centre object should relate to the NEXT scene's idea where natural, but at minimum must be round and bright.
- Other points of interest: left (about x 400) and right (about x 1500) for the slow camera drift (zoom 1.04-1.22 over x +-80 px).

## Framing
- Keep the bottom 200 px free of important content (subtitles), the top-right 160x160 corner empty, important content inside x 120..1800, y 80..880.

## Motion groups (required where people appear, otherwise optional)
Wrap moving parts as `<g id="mv-<type>-<unique>">...</g>`, each still correct when static:
- `mv-breathe-*` torso/whole figure (scaleY 1->1.03, pivot bottom centre, 2.2 s). EVERY person's body gets one.
- `mv-nod-*` head as own group (pivot bottom centre = neck), +-3 deg, 1.8 s.
- `mv-lean-*` whole figure +-2 deg around feet, 3 s.
- `mv-arm-*` arm group, +-7 deg, 1.4 s, rotating around the SHOULDER. The builder finds the shoulder automatically (tools/pivots.py): it takes the first <path>/<line>/<polyline> inside the group and uses whichever of its two ends is nearer the body (the nearest mv-breathe/mv-lean/mv-walk group). So draw each arm as an open path/line that STARTS or ENDS at the shoulder (not only a closed outline or ellipse), keep the whole arm (sleeve, forearm, hand) inside the one group, and put the group inside or next to the body group.
- `mv-hand-*` small turn of +-5 deg around the hand's own centre (no lift).
- `mv-hand-*` hand/forearm, lifts 10 px, +-6 deg, 0.7 s.
- `mv-walk-*` whole walking figure, drifts 120 px over 3.5 s; leave 60 px free each side.
- `mv-flame` `mv-lamp` `mv-lantern` `mv-beacon` `mv-glint` `mv-spark` (pulse), `mv-smoke` `mv-steam` `mv-stink` `mv-cells` `mv-rain` `mv-key` (drift up), `mv-bell` `mv-knot` (swing), `mv-antenna` (sway).
- Always make the CENTRE object a motion group `<g id="mv-core-<type>">` (types in `tools/motions.py`: spin, sway, orbit, glide, heartbeat, flicker, swell, tremble, approach, reveal, squeeze, wobble, roll; choose by the object, not the same type as the neighbouring picture). `<g id="mv-glint-core">` still works and is auto-assigned a type. Aim for 3-6 groups per scene spread left/centre/right; none over the bottom 200 px or top-right corner. If a figure group has a transform attribute, wrap it in an outer group first.

## Self-check (required)
Render each svg to PNG with Chromium via Playwright (python or node; PLAYWRIGHT_BROWSERS_PATH=/opt/pw-browsers, do NOT run playwright install; node executablePath '/opt/pw-browsers/chromium-1194/chrome-linux/chrome'), 1920x1080, save to the preview path, LOOK at it (Read). Check: centre object present and bright, no stray shapes, nothing cut off, style matches the reference (not the old flat thick-outline look). 1-2 fix passes per scene at most.
