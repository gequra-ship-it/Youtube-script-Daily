# Miya's Lab — picture spec (read fully)

One spec for every picture agent. It replaces the six layered files `art_spec.md` (v1), `art_spec_v2.md`, `art_spec_v3.md`,
`art_spec_v3_vertical.md`, `art_spec_v4_backdrop.md` and `art_spec_cosmic.md` (merged 2026-10-13; where they disagreed the
newer rule and the guideline `docs/miyas-lab-guideline.md` won — the list is in `docs/repo-changes.md`).
Give this file plus the video's `videos/<slug>/art_brief.md` (character sheet) to every agent.

- Sections 1-9: every new picture (one picture per narration unit, landscape).
- Section 10: Shorts (vertical) — overrides sizes and positions.
- Section 11: cosmic mode (space videos, `STYLE = 'cosmic'` in `config.py`) — overrides where it differs.
- Appendix A: revising the backdrop of EXISTING pictures. Appendix B: the retired first look (only to reproduce the first video).

## 1. What you draw
ONE NEW PICTURE per narration unit (a sentence or clause, 2-7 s on screen). Your units (uid, text, background mode, transition,
previous/next text, palette `pal`) are in `videos/<slug>/plan.json`. The picture must show THAT unit's idea, with a different
composition from the neighbouring units, not a copy of the scene picture. Story first: show the narration's idea clearly, a metaphor
object is welcome, a busy crowd is not.
- **Objects change with the text (user decision 2026-10-14).** Only characters stay fixed (people, astronauts, named craft: colours,
  clothes and build from the character sheet). Every other object (planets, black holes, clocks, devices, symbols) takes the shape and
  view that shows what THIS unit says: spinning → a view where the spin shows; swallowing → matter spiralling in; a real photo or
  observation → that look; size or distance → a view that shows scale. Do not draw one fixed look for an object across the whole
  video. The video's `art_brief.md` lists the allowed looks for its main objects and when to use each.

## 2. Files
- `videos/<slug>/art3/<uid>.svg` and `videos/<slug>/art3/<uid>.json` (sidecar, section 8). Paths are relative to the repo root.
- `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1920 1080" width="1920" height="1080">`
- Allowed: shapes, paths, groups, `<linearGradient>`, `<radialGradient>`, opacity, stroke-dasharray, `<clipPath>`.
  FORBIDDEN: `<filter>` (any, it slows the render), `<image>`, `<text>` / letters / numbers anywhere (on-screen text goes in the sidecar
  `labels`), CSS/SMIL animation, `<style>`, `<foreignObject>`. Glow = stacked circles with a radialGradient fading to opacity 0.
- Ids unique inside the file, every `url(#id)` must resolve, valid XML (`xmllint --noout file.svg`).
- Under ~120 KB per picture: one clear idea, 8-25 shape groups.
- Previews go to your OWN scratch folder, never into `art3/` (agents working in parallel must not share a folder).

## 3. Look
- Background mode = plan.json `bg` for every unit of the scene:
  - "paper": base `pal.paper_base`, thin lines `pal.paper_ink`
  - "night": vertical wash `pal.night_top` -> `pal.night_bottom`, lines `pal.night_line`, glow `pal.night_glow`
  - "dusk": gradient `pal.dusk_stops[0]` -> [1] -> [2], lines `pal.dusk_ink`
- **Colours come ONLY from `pal`** (the palette chosen for the script topic, `tools/palettes.py`): backgrounds, lines and glows from
  `pal`, main subjects from `pal.accents` (4 colours). Natural colours of things (skin, animal bodies, plants, water) follow the art brief,
  tinted to harmonise with `pal`. Do NOT fall back to purple/magenta/orange unless `pal.palette` is "sunset" or the thing itself has that
  colour (the old purple/peach defaults made every video look the same, user complaint 2026-10-10).
- Linework: thin hand-drawn ink lines, stroke-width 2.5-4 (up to 6 for the main subject), slightly wobbly (cubic curves, not perfect
  geometry), 1-2 hatching groups for shading. NO uniform thick black outline around every object.
- Shading: soft gradients on big forms (sky, glow, rounded bodies), hatching for texture. Saturated but harmonious, no neon on white.
- People: simplified, dignified, readable silhouettes, small dot eyes, calm faces, varied skin tones; no caricature, no stereotypes.
- Never: gore, blood, nudity, violence shown, weapons pointed at anyone, real/famous persons, logos. Death/cannibalism topics only
  through mourning scenes, symbols, hands, bowls, smoke, empty places.
- Units of one scene share bg, palette and character looks (same person = same clothes/skin/hair; the first unit you draw is the model).

## 4. The centre rule (most important)
The zoom transition dives into the exact centre of a picture (to 2.6x) and the next picture arrives zoomed on its centre.
- ONE round (or roughly round) focal object centred at (960, 500), diameter 170-260 px, with a bright or high-contrast core (eye, lens,
  lamp, bowl, moon, cell, dial, porthole, flame, coin, doorway...). Nothing important on top of it.
- It relates to the NEXT unit's idea where natural; at minimum it is round and bright.
- **No radiating lines and no concentric rings** around the centre (removed 2026-10-10: they repeated in every picture). Every picture
  gets its own backdrop instead (section 5).
- `transition_in` "match": the centre object sits at (960,500) with about the same size and colour family as the PREVIOUS unit's centre
  object of the same scene (you draw in order, look at your previous svg), because the cut grows the new picture out of that shape.
- Other points of interest: left (about x 400) and right (about x 1500).
- Wrap the centre object in its motion group `mv-core-<type>` (section 7).

## 5. Backdrop
Each picture gets a backdrop that fits its text: a place or atmosphere in thin sketch lines and soft flat/gradient shapes filling the
canvas under the content (highland ridge and huts, hut interior, open ground with trees, microscope field, lab bench, lined notebook,
wood table, plain wash with hatching, night sky with horizon, museum wall, kitchen counter, hospital corridor, pasture, calendar/time
marks...). Abstract ideas may get a symbolic backdrop (sand drift, stacked layers, rain of dots) but never rings or rays.
- Different from the neighbouring units; at most 2 of every 12 units share the same kind of backdrop.
- Built on the unit's `pal` base colours; backdrop shapes in related low-contrast tones (lines 1.6-3 px, opacity 0.35-0.7) so the
  centre object and people stay the most contrasted things; the bottom 200 px stays calm (captions).

## 6. Composition and framing
- The camera is STATIC unless the sidecar names a focus: the picture must read well as a still, and the things the text mentions
  must be easy to see.
- Consecutive units change viewpoint/subject (wide scene -> close object -> symbol/diagram -> person): new shots, same world.
- Keep the bottom 200 px free of important content (captions), the top-right 160x160 corner empty (logo), important content inside
  x 120..1800, y 80..880. `transition_in` "slide": keep important content away from the far left/right 150 px.

## 7. Motion groups
Wrap moving parts as `<g id="mv-<type>-<unique>">...</g>`; each must still look right when static, each id unique. If a figure group
has a transform attribute, wrap it in an outer group first. 1-4 groups per picture (cosmic: 4-8), spread left/centre/right, none over
the bottom 200 px or the top-right corner; every visible person gets `mv-breathe`. Each unit is only 2-7 s, keep motions subtle.

| group | what the video does |
|---|---|
| `mv-breathe-*` torso/whole figure | scaleY 1 -> 1.03, pivot bottom centre, 2.2 s |
| `mv-nod-*` head as its own group | +-3 deg around the neck (bottom centre), 1.8 s |
| `mv-lean-*` whole figure | +-2 deg around the feet, 3 s |
| `mv-arm-*` arm | +-7 deg, 1.4 s around the SHOULDER. The builder finds the shoulder (`tools/pivots.py`): it takes the first `<path>`/`<line>`/`<polyline>` in the group and uses whichever end is nearer the body (nearest mv-breathe/lean/walk group). Draw each arm as an open path/line that starts or ends at the shoulder, keep sleeve, forearm and hand in the one group, put it inside or next to the body group |
| `mv-hand-*` hand | +-5 deg around the hand's own centre, 1.0 s, no lift (it stays on the wrist) |
| `mv-walk-*` walking figure | drifts 120 px sideways over 3.5 s; leave 60 px free on both sides |
| `mv-flame` `mv-spark` | short flame pulse |
| `mv-lamp` `mv-lantern` `mv-beacon` `mv-glint` | in-place light pulse (size 1 -> 1.06, opacity .85 -> 1) |
| `mv-smoke` `mv-steam` `mv-stink` `mv-cells` `mv-rain` `mv-key` | drift up |
| `mv-bell` `mv-knot` | swing |
| `mv-antenna` | sway |

**Centre object `mv-core-<type>` (always).** Pick the type by what the object is (table in guideline 4-1 and `tools/motions.py`):
spin, sway, orbit, glide, heartbeat, flicker, swell, tremble, approach, reveal, squeeze, wobble, roll, pop, ping, stamp, flip, draw, drop.
Never the same type in two neighbouring units, never a plain up-and-down bob; over a whole video use at least 10 types, none above 20 %
of the pictures. `draw` traces the object's stroked outlines, so give such an object real outlines. If you leave the old name
`mv-glint-core`, the build assigns a type by rotation (it may not suit the object).

## 8. Sidecar JSON (exact keys)
```
{
 "centre": "short English description of the centre object",
 "focus": [x, y, scale] or null,
 "focus_word": "exact words from the unit text" or null,
 "sfx": [ {"name": "<library name>", "word": "<exact words from the unit text>", "vol": 0.5-0.8} ],
 "labels": [ ... ],
 "spot": true,
 "iris": [x, y]
}
```
- `iris` (optional, 2026-10-14): when the subject of the picture stands at the side (a person, a craft at about x 400 or x 1500),
  give its centre. If the build picks the `iris` transition for this unit, the picture opens as a growing circle from that point.
  Without it the build uses an off-centre `focus` point, else the left or right third.
- `focus`: only if the text names a specific thing to look at closely. x,y = its centre, scale 1.5-2.2 (the camera pushes in there and
  holds; the rest of the picture dims, guideline 4-1 — set `"spot": false` to keep it bright). About 40-50 % of units get a focus.
  `focus_word` occurs verbatim in the unit text (the camera starts shortly before it is spoken). The focused thing needs enough detail
  for 2x zoom.
- `sfx` (0 or 1 entry): `name` is one of swish, hush, tick, crackle, bubble, wind, bell, click, creak, drip, thud, chime, rustle, pop,
  pencil, page, cloth, woodblock, sand, rain, splash, step, breath, stone, flutter (all soft and unpitched; `bell`/`chime` are a dull
  knock / paper flick, `shimmer` is an alias of `hush`); cosmic videos use section 11's list. Only for a matching event: fire/cooking ->
  crackle; boiling/liquid -> bubble; rain -> rain; splash/pour -> splash; outdoors/open sky -> wind; alarm/hollow -> bell or woodblock;
  lock/latch/sealing -> click; wooden hut/door/scale -> creak; a single drop/tear/sample -> drip; something heavy/final -> thud or stone;
  writing/drawing -> pencil; book/paper/records -> page or rustle; clothing/body movement -> cloth; walking/arrival -> step;
  sand/powder -> sand; birds/wings -> flutter; quiet/tension -> breath; small appearing symbol -> pop; idea/discovery -> hush.
  Vary: not the same name in two consecutive units; roughly 35-45 % of units get one; never drones, hums or musical tones.
- `labels` (0-3, guideline 3-6). The SVG still has NO text; the builder lays these over the picture as HTML:
  ```
  {"type": "name", "text": "Anomalocaris", "x": 1320, "y": 300, "to": [1180, 470], "word": "Anomalocaris"}
  {"type": "num",  "text": "539 MILLION YEARS AGO", "word": "539 million"}
  {"type": "say",  "text": "Still here!", "x": 1080, "y": 520, "to": [1272, 650]}
  ```
  - `name` (max 28 chars): a creature, plant, place, era or object VISIBLE in the picture and SAID in this unit (same spelling). x,y =
    centre of the pill (~34 px text, ~20 px per letter), `to` = a point on the subject. Empty space next to the subject, never over a
    face, the centre object or the thing the text is about. Not the same name again in the next unit unless the subject changes.
  - `num` (max 26 chars, UPPER CASE): a number, date, size or share SAID in this unit ("four meters" -> "4 M" is fine, "nine meters" ->
    "10 M" is not). Fixed at the top-left (landscape x 80, y 64; keep that corner free when you use one). Its first number counts up from
    0 when it appears (years 1000-2100 do not count). Short: "~3.5 M LONG", "539 MILLION YEARS AGO".
  - `say` (max 4 words / 24 chars, no digits): a short reaction of an animal, a generic person or an object, `to` = its mouth. Never a
    fact, number or claim, never for a real named person, kind not mocking; about 1 unit in 8.
  - `word` (optional): exact words of the unit; the label pops in when they are spoken (else ~0.4 s after the cut).
  - Safe area landscape x 120-1800, y 80-860, nothing in the logo corner (x > 1660, y < 190). With a focus, labels move with the zoom
    (their size stays), so keep them near the focus point. About half of the units get a label. Chalkboard units get none.
- Validate the JSON (python `json`).

## 9. Check and work method
- Render previews: `python3 tools/svgshot.py <your_preview_dir> f1.svg f2.svg ...` and LOOK at every picture (centre object present
  and bright, no stray shapes, nothing cut off, the style above, not the old thick-outline look).
- Labels: `python3 tools/labelshot.py <slug> <your_preview_dir> <uid> ...` prints problems (the build stops on any) and writes
  `<uid>_lab.png` with the labels and a sample caption; fix overlaps.
- Draw the units in order: read text (+ previous/next), decide the picture, write svg + json, preview a batch of 3-4, fix at most once.
- Final answer: one line per uid `uid | centre | focus_word or - | sfx or -`, plus any problem.

## 10. Shorts (vertical) — overrides
- Canvas `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1080 1920" width="1080" height="1920">`. NEW pictures only, never a
  reused or cropped landscape picture. Under ~100 KB each.
- Centre object at (540, 860), diameter 150-230 px; "match" keeps it at the previous unit's place/size.
- Shorts overlays cover the top ~290 px, the bottom ~290 px and the right ~140 px; captions sit at y ~1440-1560. All important content
  inside x 100..940, y 300..1400 (backgrounds/glows may fill the canvas). "slide": keep x 0..100 and 980..1080 empty of important content.
- Compose vertically: stack subjects top-to-bottom instead of left/right.
- Sidecar focus [x, y, scale] (scale 1.5-2.0) and label x, y / to use the 1080x1920 space. The num badge sits at x 100, y 330. Label safe
  area x 100-940, y 300-1400.
- Previews: `SHOT_W=1080 SHOT_H=1920 python3 tools/svgshot.py <dir> files...`

## 11. Cosmic mode (space videos) — overrides
Use when `config.py` has `STYLE = 'cosmic'` and `PAL_DEFAULT` is one of `nebula` (nebulae, galaxies, star birth), `aurora` (planet
atmospheres, magnetospheres, solar wind), `deepfield` (distant galaxies, black holes, cosmic scale), `solar` (the Sun, supernovae,
flares); per-scene `PAL` may mix up to 3. Look = surfaces and light, keeping the thin sketch lines (user decision 2026-10-12).
1. Night (`night_*`) on 70 % or more of the units; paper/dusk only for everyday scenes at the start and end.
2. Nebula layer (required): 3-4 large `radialGradient` shapes (40-90 % of the canvas) overlapping, colours from `pal.accents` and
   `night_glow`, opacity 0.15-0.55, edges fading to `stop-opacity 0`. No `<filter>`: softness only through gradient stops.
3. Stars in three tiers: 120-250 small (r 0.8-1.6 px, opacity 0.4-0.9); 12-25 medium (2.5-4 px) split into groups `mv-glint-s1`,
   `mv-glint-s2`, `mv-glint-s3` (staggered twinkle); 2-4 large with a cross flare (4 thin lines + radial glow). Keep stars off the centre
   object and the key subject.
4. Celestial bodies: two radialGradient layers (body + atmosphere glow) and a rim light (thin bright arc) on one edge; the shadow side
   darker than `night_bottom`; a few hatching lines for texture; a thin sketch outline (2.5-3 px, `night_line`) only on the main body.
5. Light beams and orbits: orbits as `night_line` at opacity 0.35, dotted or thin, only when the content needs them and not in the same
   layout as the neighbouring unit (the no-rings rule stays); beams = 1-3 thin gradient trapezoids.
6. The centre rule holds: a bright body, eye or lens at (960,500), 170-260 px, in `mv-core-<type>` chosen by its nature (planet `spin`,
   star `flicker` or `ping`, moon/satellite `orbit`, nebula `swell`...), never the same type as the neighbouring unit.
7. Extra motion groups: `mv-glint-s*` star twinkle, `mv-drift-nebula` (one nebula layer +-25 px, 20 s period), `mv-orbit-*` (a small
   body travelling on an orbit; the group holds an invisible full orbit circle so its centre is the orbit centre), `mv-pulse-core`
   (brightness pulse of a star/sun). 4-8 `mv-` groups per picture.
8. Never: letters in the picture, uniform thick black outlines, 3D/photo look, copies of real photos, astronomy that contradicts the
   facts (follow the script's numbers where scale matters, otherwise draw symbolically).
9. Sound: `sfx.name` from `sparkle` (starlight specks), `bloom` (quick spread and fade: flare, star birth), `starfall` (falling light
   tail), `pulse` (short round beat: signal), `warp` (0.3 s sharp brush: change of place), `glimmer` (tiny glints), plus `tick`, `click`,
   `pop`, `drip`, `pencil`, `page`, `woodblock`, `stone`, `step`, `cloth`. Not `riser`/`sweep` (removed: they sounded like waves), and
   not `hush`, `breath`, `wind`, `rain`, `swish`. 35-45 % of units, never the same name in two consecutive units.
10. Black holes — four looks, chosen by what the unit says (user decision 2026-10-14; one fixed look read like Saturn at small size).
   Never a thin flat ring around a black disc on its own. Every look has a pure black shadow disc and a thin bright photon ring on its edge.
   - **Lensed disk** (default, side view): a THICK glowing accretion disk (layered strokes, hottest/brightest on the side turning toward
     us) crossing in front of the shadow, and the far side of the disk bent up over the top of the shadow (and thinly under the bottom) as
     a crescent that touches the shadow and merges into the disk at both ends, never a loop floating apart. Use for orbits, planets
     beside the hole, ISCO, horizons, scale, tides.
   - **Face-on ring** (like the 2019 M87* / 2022 Sagittarius A* images): a thick soft ring of light around the shadow, brighter on one side
     (Doppler beaming), soft halo, no disk ellipse. Use when the text talks about the real images, the Event Horizon Telescope, the
     shadow, or a real named hole (M87*, Sagittarius A*, TON 618).
   - **Whirlpool** (face-on swirl): gas arms spiralling into the shadow, from coral/gold at the outside to white-hot at the edge. Use when
     the text says swallowing, feeding, falling in, spinning, frame-dragging, stirring. Not too often: it can read as a spiral galaxy.
   - **Simple dark disc + thin ring** (the old look): only small and far away (a black hole in the distance, under 120 px), as an icon in
     a diagram, or when a quiet calm hole is meant ("stopped feeding").
   Vary the look between neighbouring units that both show a black hole unless the transition is `match` (then keep the previous look).
   Reference drawings (960x540, deepfield colours): `tools/ref/blackhole-lensed-disk.svg`, `blackhole-face-on-ring.svg`,
   `blackhole-whirlpool.svg`. Copy the idea, not the file: scale to the unit, add the scene's own backdrop and motion groups.

## Appendix A — revising the backdrop of existing pictures
Task used on 2026-10-10 to remove the repeated rings/rays from already drawn pictures. Do not redraw people/objects. Per unit:
1. Open `<uid>.svg`; delete the generic decoration: the big radial "rays" path (many `M..L..` lines from the centre), the concentric ring
   circles (r ~330-640 around the centre) and the large soft glow disc behind them. Keep people, props, the centre object (position,
   size, its `mv-core-*`/`mv-glint-core` group), all `mv-` groups and ids.
2. Draw a backdrop for THAT unit's text as in section 5 (read plan.json text, previous and next text), different from its neighbours.
3. Keep the unit's background-mode colours as the base wash; backdrop shapes low-contrast; bottom 200 px calm.
4. The centre object stays at (960,500) with about the same size/colour. A meaningless "sun/ring" centre may be re-dressed to fit the
   backdrop (lamp, window, plate, clock, lens...); then update `centre` in the json.
5. Rules of section 2 hold; keep `focus`, `focus_word`, `sfx` unless the focus target moved (then fix the coordinates); do not rename
   `mv-` groups. Edit in place (keep a backup), preview outside `art3/`, check no rays/rings are left.
6. Final answer: one line per uid `uid | backdrop kind`, plus any problem.

## Appendix B — the retired first look (v1, 2026-10-08)
Only to reproduce the very first video with `tools/build.py` (`videos/never-eat-human-meat/art/<id>.svg`, one picture per scene). Do
not use for new videos (user decision 2026-10-09). Differences from the current look: flat 2D webtoon-like illustration; every object
outlined in black (`stroke="#0A0A0A" stroke-width="6"`, details 4); cell shading with one darker flat tone, NO gradients; fixed muted
palette (night #1F2A44 #2B3442, sky #A9CFE6, earth #D9C29A #C9A56E, teal #3E7F8C, olive #8FA35A, brick #B5483B, lamp #F2D27A, foliage
#5E7A45 #7F9B55 #3F5A38, wood #8A6A45 #6B4F33, white #F1ECE0); no glow; highly detailed backgrounds; 3+ points of interest left/centre/
right for crops up to 1.5x; under ~800 KB. Motion values of that time differed (`mv-arm` +-14 deg 0.9 s, `mv-hand` lift 10 px +-6 deg
0.7 s) and were later changed (guideline 4-1).
