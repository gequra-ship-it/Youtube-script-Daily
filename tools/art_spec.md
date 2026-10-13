# Miya's Lab — SVG scene art spec (read fully)

Goal: flat 2D editorial illustration, like a Korean indie comic / webtoon background. One standalone SVG per scene.

## File rules
- Output: /home/claude/vid/art/<id>.svg  (ids are given in your task)
- `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1920 1080" width="1920" height="1080">`
- Only basic shapes/paths/groups, flat fills. NO `<filter>`, NO gradients (use 2 flat tones for shading), NO `<image>`, NO `<text>`/fonts (no letters or numbers anywhere in the picture), NO CSS animation, NO `<style>` needed (use attributes).
- Outline: ALL objects get black outline `stroke="#0A0A0A" stroke-width="6" stroke-linejoin="round" stroke-linecap="round"` (thin detail lines may use 4).
- Cell shading: base tone + ONE darker tone shadow shape per object. Muted desaturated palette:
  night/space #1F2A44 #2B3442, day sky #A9CFE6, earth/hut/paper #D9C29A #C9A56E, sea/teal #3E7F8C, olive green #8FA35A, brick red #B5483B, lamp yellow #F2D27A, plus muted darker/lighter variants of these and neutral grays, skin tones (varied, respectful), foliage greens (#5E7A45 #7F9B55 #3F5A38), wood browns (#8A6A45 #6B4F33), white #F1ECE0.
- Highly detailed background (foliage layers, roof thatch, windows, shelves, props), realistic human proportions, calm restrained faces (dot eyes, small mouth). No anime big eyes, no chibi, no 3D look, no neon, no glow, no lens flare.
- NO gore, NO blood, NO nudity, NO violence shown, no weapons pointed at anyone. People are dignified. No real/famous persons, no recognizable logos.
- Framing: the video crops this picture at several zoom levels (up to 1.5x) around different points, so spread 3+ distinct points of interest across left / center / right. Keep the bottom 200px free of important content (subtitles go there) and keep the top-right 160x160 corner empty-ish (logo). Keep important content inside x 120..1800, y 80..880.
- Motion groups (required for scenes with people, optional otherwise): wrap parts that should move as `<g id="mv-<type>-<unique>">…</g>`. Each group must still look correct when static, and each id must be unique inside the file (e.g. `mv-nod-doctor1`). Types and what the video does with them:
  - `mv-breathe-*` torso/whole figure: scaleY 1 -> 1.03, pivot at bottom center, 2.2 s. Put EVERY standing/sitting person's body in one.
  - `mv-nod-*` head (draw the head as its own group, pivot is the bottom center = neck): rotates +-3 deg, 1.8 s.
  - `mv-lean-*` whole figure rotates +-2 deg around its feet, 3 s (people waiting, listening).
  - `mv-arm-*` an arm drawn as its own group whose TOP is the shoulder: swings +-14 deg, 0.9 s (waving, stirring, writing).
  - `mv-hand-*` a hand/forearm: lifts 10 px and tilts +-6 deg, 0.7 s (handing something over).
  - `mv-walk-*` a whole figure walking: drifts 120 px sideways over 3.5 s with a small step bounce. Only use where a figure should cross the scene, and leave 60 px free on both sides of it.
  - Others: `mv-flame` `mv-lamp` `mv-lantern` `mv-beacon` `mv-glint` `mv-spark` (pulse), `mv-smoke` `mv-steam` `mv-stink` `mv-cells` `mv-rain` `mv-key` (drift up), `mv-bell` `mv-knot` (swing), `mv-antenna` (sway).
  - Aim for 3-6 motion groups per scene, at least one on each foreground person, spread over left / center / right so every zoomed crop still shows movement. A moving group must not overlap the bottom 200 px or the top-right corner.
- Size under ~800 KB. Must be valid XML (`xmllint --noout file.svg`).

## Self-check (required)
Render each svg to PNG with Chromium via Playwright (python `playwright` or node `playwright`; chromium is at /opt/pw-browsers/chromium; PLAYWRIGHT_BROWSERS_PATH=/opt/pw-browsers, do NOT run playwright install; for node use executablePath '/opt/pw-browsers/chromium-1194/chrome-linux/chrome'), 1920x1080, and LOOK at the PNG (Read tool). Fix anything broken: overlapping/misplaced shapes, empty areas, unreadable subject, cut-off objects. Do 1-2 fix iterations at most per scene; quality bar = clear subject, tidy outlines, recognizable story.
Put your PNG previews in /home/claude/vid/art/preview/<id>.png.
