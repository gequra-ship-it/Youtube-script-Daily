# Miya's Note picture spec (read fully)

Read with `videos/<slug>/art_brief.md`. Older full text (branch `archive/miyas-lab-2026-10-24` only): `docs/archive/art_spec-full-2026-10-18.md`. 1-9 landscape; 10 Shorts and 11
cosmic override them; Appendix A re-backdrops old pictures, B is the retired look.

## 1. What you draw
ONE NEW PICTURE per narration unit (2-7 s); units (uid, text, bg, transition, prev/next, `pal`) in `videos/<slug>/plan.json`.
Show THAT unit's idea clearly (metaphor object yes, busy crowd no), composition unlike the neighbours, no copy of the scene picture.
- **Objects change with the text.** Only characters stay fixed (people, astronauts, named craft: per sheet). Other objects take the view that shows what THIS unit says (spin, swallowing → matter spiralling in, real photo look, scale); no fixed look; `art_brief.md` lists allowed looks.

## 2. Files
- `videos/<slug>/art3/<uid>.svg` + `<uid>.json` (sidecar, section 8).
- `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1920 1080" width="1920" height="1080">`
- Allowed: shapes, paths, groups, linear/radial gradients, opacity, stroke-dasharray, `<clipPath>`. FORBIDDEN: `<filter>`, `<image>`, `<text>`/letters/numbers anywhere (use sidecar `labels`), CSS/SMIL animation, `<style>`, `<foreignObject>`. Glow = stacked circles, radialGradient to opacity 0.
- Unique ids, `url(#id)` resolve, valid XML (`xmllint --noout`). Under ~120 KB: one clear idea, 8-25 shape groups.
- Previews in your OWN scratch folder, never `art3/`.

## 3. Look
- Background = plan.json `bg`: "paper": base `pal.paper_base`, lines `pal.paper_ink`; "night": vertical wash `pal.night_top` -> `pal.night_bottom`, lines `pal.night_line`, glow `pal.night_glow`; "dusk": `pal.dusk_stops[0]` -> [1] -> [2], lines `pal.dusk_ink`.
- **Colours start from `pal`** (`tools/palettes.py`; a skeleton: change/add colours as the script needs): backgrounds/lines/glows from `pal`, main subjects from `pal.accents` (4). Natural colours per art brief, tinted to `pal`. No purple/magenta/orange unless `pal.palette` is "sunset" or the thing is that colour.
- Linework: thin wobbly ink (cubic curves), stroke-width 2.5-4 (main subject up to 6), 1-2 hatching groups. NO uniform thick black outline. Soft gradients on big forms; saturated but harmonious, no neon on white.
- People: simple dignified silhouettes, dot eyes, calm faces, varied skin; no caricature/stereotypes.
- Never: gore, blood, nudity, shown violence, weapons pointed at anyone, real/famous persons, logos. Death/cannibalism only via mourning, symbols, hands, bowls, smoke, empty places.
- One scene = same bg, palette, character looks (clothes/skin/hair; your first unit is the model).

## 4. The centre rule (most important)
The zoom cut dives into the exact centre (2.6x); the next picture arrives zoomed on its own.
- Focal object (flexible, 2026-10-22): decide per unit from the narration. Use a round centre object at (960, 500), diameter 170-260 px, bright core (eye, lens, lamp, bowl, moon, dial, flame, coin...) ONLY when the scene calls for one; otherwise place the main object anywhere, round or not. No fixed ratio. Nothing important on top of a centre object. Relates to the NEXT unit where natural.
- **No radiating lines, no concentric rings** around it; backdrop instead (section 5).
- `transition_in` "match": about the same size and colour family as the PREVIOUS unit's centre object (check your previous svg).
- Other points of interest: left (x ~400), right (x ~1500). Centre object in `mv-core-<type>` (section 7).

## 5. Backdrop
Each picture gets a backdrop fitting its text: a place/atmosphere in thin sketch lines and soft flat/gradient shapes filling the canvas
(hut interior, microscope field, lab bench, notebook, night sky with horizon, museum wall, hospital corridor, time marks...).
Abstract ideas: symbolic (sand drift, stacked layers, rain of dots), never rings or rays.
- Different from neighbouring units; at most 2 of every 12 units share a backdrop kind.
- On `pal` base colours, low-contrast tones (lines 1.6-3 px, opacity 0.35-0.7): centre object and people stay most contrasted; bottom 200 px calm.

## 6. Composition and framing
- Slow drift camera (push 1->1.06x, pan or pull; guideline 20-1) unless a focus is set (then push into it). Must read at ~6% zoom and 2.5% pan (important content ~60 px inside the safe area) and as a still; mentioned things easy to see.
- Consecutive units change viewpoint/subject (wide -> close -> diagram -> person): new shots, same world.
- Important content in x 120..1800, y 80..880, not in the bottom 200 px; top-right 160x160 empty (logo). "slide": none in the far left/right 150 px.

## 6A. Hands — MANDATORY (2026-10-17)
Hands needing fingers (6B) only via `tools/hands.py`, never free-hand; other hands simple and round.
```python
import sys; sys.path.insert(0, 'tools')  # run from the repo root; from hands import hand
svg += hand(x, y, angle, size, side='L'|'R', view='palm'|'back', pose='open'|'flat'|'wave'|'point'|'fist'|'hold', skin=..., line=...)
```
(x, y) wrist, `angle` finger direction (0 = up, clockwise), `size` palm length px. Built in: middle finger ~ palm; thumb low on the palm
side, out 22-40 deg, tip ~ index knuckle, never hooked/bent back/longer than the index; side follows L/R and palm/back. `body.arm()` puts the hand in the forearm link. Stencils (cave art): `hand(...)` in stencil colour or as mask. Gloves/mittens
may be free-hand. Missing pose: rotate/scale a module pose, never invent a thumb. Check every hand at 100 % zoom.

## 6B. People: proportions and arms — MANDATORY (2026-10-17)
Cute style (not realistic jointed elbows, not free-hand over-long arms).
- `P` in `tools/body.py`: **adult `kind='cute'` 5.5 head heights, child `'cute_child'` 4.5** (big head, short limbs). Hanging arm: fingertips at top/middle of thigh, never knee. Realistic 'adult' (7.5) only if truly needed.
- Every human arm via `body.arm(...)` (hand included): ONE smooth tapered curve, no elbow shown, one `mv-limb` link from the shoulder. `elbow_moves=True` (upper arm + forearm links) ONLY where the forearm swings (waving, hammering, writing). Elbows fold 0-140 deg one way, never backwards. Holding/pressing arms: `amp=(0, 0)`.
- Shoulders inside the torso corners (`shoulders()`); facing us, the figure's right arm is on our left.
- Hands **round by default** (`fingers=False`); `fingers=True` ONLY for pointing, gripping a visible object, waving close-up, hand as the subject, stencils/icons.
- No `mv-chain` on human arms (tails/tentacles only). Reference sheet: `python3 tools/body.py /tmp/b.svg`.

## 7. Motion groups
`<g id="mv-<type>-<unique>">`, fine static, unique ids; wrap a figure group that has a transform. 1-4 groups (cosmic 4-8), spread
left/centre/right, not in the bottom 200 px or top-right corner; every visible person gets `mv-breathe`. Subtle.

| group | motion |
|---|---|
| `mv-breathe-*` torso/figure | scaleY 1 -> 1.03, pivot bottom centre, 2.2 s |
| `mv-nod-*` head (own group) | +-3 deg around neck (bottom centre), 1.8 s |
| `mv-lean-*` figure | +-2 deg around feet, 3 s |
| `mv-arm-*` | +-7 deg, 1.4 s around the SHOULDER = end of the first `<path>`/`<line>`/`<polyline>` nearer the body (mv-breathe/lean/walk; `tools/pivots.py`): open path from the shoulder; sleeve, forearm, hand in one group by the body |
| `mv-hand-*` | +-5 deg around own centre, 1.0 s, no lift |
| `mv-walk-*` | drifts 120 px sideways over 3.5 s; 60 px free both sides |
| `mv-flame` `mv-spark` | short flame pulse |
| `mv-lamp` `mv-lantern` `mv-beacon` `mv-glint` | light pulse (size 1 -> 1.06, opacity .85 -> 1) |
| `mv-smoke` `mv-steam` `mv-stink` `mv-cells` `mv-rain` `mv-key` | drift up |
| `mv-bell` `mv-knot` / `mv-antenna` | swing / sway |
| `mv-<kind>-<name>` 35 more kinds (2026-10-26 round 4): `bob hover pendulum wiggle tilt crumble emph spin rollby float flap swim hop drip unfold unroll flagwave ripple sparkle circle squash neon shiver beat settle magnet bouncing creep sink ascend tick flicker breathe nodding sway` | each kind's AXIS is fixed in `tools/motions.py` (comment per kind): pendulum/drip/unfold = TOP edge, tilt/sway/squash/hop/bouncing = FEET (bottom), flap/tick/spin = CENTRE, unroll = LEFT edge, flagwave = the pole side, `circle` needs `data-pivot` = orbit centre (else it floats). Name the group after the THING (`mv-sway-tree`, `mv-spin-coin`): the builder reads the name and fixes a wrong axis or kind automatically (a tree never spins, a whale never drops/rolls, a lantern asked to spin swings instead); `data-keep="1"` keeps your choice |
| `mv-blink-*` eyes of a creature/person (whites + pupils in ONE group, nothing else) | eyelids close for 0.07 s at an irregular rhythm (3.1 / 4.2 / 0.35 / 2.5 s); draw each face's eyes as their own group so they can blink (2026-10-26) |

**Creature joints (guideline 20-6)**, never one stiff piece:
- `mv-joint-<name>`: one hinge (jaw, leg, wing, flipper, platform, pointing hand). `data-pivot="x y"` (picture coords), optional `data-amp` (deg, default 12), `data-per` (half-cycle s, default 1.1), `data-phase` (radians).
- `mv-chain-<name>-1`, `-2`, `-3`...: links NESTED (2 in 1, 3 in 2), each `data-pivot` where it meets its parent (tail, fin, tentacle, snake, neck, seaweed); each rotates about its pivot, carrying its children; amp x1.35 per link to the tip, lag 0.55 rad per link; default amp 7 deg, half-cycle 1.5 s.
- Links overlap the parent a few px at the joint; no transform on link groups; pivots in drawing coords.

- `mv-rotor-<name>` (2026-10-19): a part that keeps turning about `data-pivot="x y"` (clock hand, fan, wheel, plasma ring); `data-per` = seconds per full turn (default 8), `data-dir` = 1 or -1.
- **Object motions anywhere (2026-10-22):** the round centre object is no longer required; the main object may sit anywhere and need not be round. Besides `mv-core-*` there are position-free motions (21 kinds in all, incl. the 2026-10-24 four below), each a group `mv-<kind>-<name>` with `data-*` attributes (`data-delay` s after the picture starts, default 0.3; `data-dur` s, default 1.0): `path` (`data-path="M.. C.."`, follows the path and turns with it unless `data-rot="0"`), `flip` (`data-pivot`, `data-deg` 180), `fill`/`grow` (`data-from`, `data-to`, `data-axis` y|x, about `data-pivot`: sand level, bars, gauges), `swing` (damped pendulum, `data-amp` 28, `data-per` 2.4), `topple` (`data-deg` 72, give each domino a `data-delay` 0.2 s later), `liquid` (`data-rise` px, `data-scroll` px: draw a wide wavy-topped shape and clip it with the vessel's `clipPath`), `bubble` (`data-rise`, `data-per`), `edge` (strokes in the group draw on), `keyturn` (side-view key bow turning about its shaft, `data-to` .32), `shackle` (`data-lift` 46, `data-deg` -16), `popin`. Draw the moving part as its own group; `data-pivot="x y"` is in picture coordinates. Also `shake` (`data-amp` 3, `data-dur` .25), `dash` (dashes march along a dashed line, `data-speed` 40), `scroll` (`data-dist` 160 px sideways drift), `slam` (stamp in from 2.4x), `rise` (`data-from` 60 px, fade in). **Derive the motion from the unit's narration, not from a list (2026-10-22, owner repeated this):** the motions above are building blocks, not a menu of fixed scenes. For each unit write one sentence for what the narration says happens (event, movement, change, relation), then pick the motion(s) that show exactly that, combining kinds (`path` + `dash` + tracking; `flip` + `fill` + `shake`) or adding a new kind to `tools/motions.py` `obj_js` + `OBJ_KINDS` + this section when nothing fits. Units with nothing to move (plain explanation, dialogue) get no forced motion. Repetition follows the narration (2026-10-27 principle): the same kind in neighbouring pictures is fine when the story repeats the situation, wrong when it is just the nearest tool; note the chosen motion in the sidecar/report. **Camera tracking (same rule: decided from the narration, not from examples):** when the narration describes a long continuous movement, journey or survey (a creature walking, a herd moving, scanning along a timeline, food chain or rock layers, a river flowing, something flying, a chain reaction), the camera follows it; you decide the route per unit. It starts automatically for a picture with a long travelling motion (`mv-path-*`, 3+ `mv-topple-*`); for every other scene add an empty `mv-track-*` group with `data-path` (the route of the camera centre), `data-delay`, `data-dur`, `data-scale`. The camera follows it (zoom 1.3 in the first 12 %, back out in the last 12 %; sidecar `"track": false` or `{"scale": 1.4}`); it replaces focus and drift. Rules: a padlock opens only after its key (drawn from the side, going into the keyway) has turned clockwise; an hourglass flips first, then the upper chamber drains and the lower one fills from the bottom. Implementation: `tools/motions.py` `obj_js`. **Hourglass / vessel fills (2026-10-25, miya saw sand pass through the glass):** never draw sand as a shape that a `fill` scales (a funnel-shaped sand scaled toward the neck pokes through the walls). Draw each sand body as a plain RECT as wide as the chamber, inside a static `<g clip-path="url(#id)">` whose `<clipPath>` repeats the glass outline, and put the `mv-fill-*` group (rect) inside that clip group; pivot = the neck for the draining chamber, the chamber's far wall for the filling one. The same applies to any liquid, bar or gauge that must stay inside an outline. **Pivots (same day):** a rotating or swaying centre object turns about its visual centre or its true hinge: ships, probes, planes and rockets use `wobble` (about the centre), never `sway` (about the bottom edge); poles, signs, lamps and masts use `sway`, with the pivot at the pole's foot; a spinning disc or galaxy must have its drawn centre at the group's bbox centre (no off-centre glow or shadow inside the group). Check rotating groups with `getBBox()` centre vs the drawn centre before building. **Pivot coordinates and falling objects (2026-10-25, miya saw whale tails detach and a falling whale stand still):** (1) `data-pivot` (and `data-path` start) should be in PICTURE coordinates; when a part sits inside a translated/rotated/scaled wrapper group, write the pivot as the point's picture position, not the wrapper's inner coordinates. `miyaPv` converts to the parent's space and, when the numbers only make sense as inner coordinates, accepts those instead (it picks the reading that lands nearer the part's bbox). A tail/fin/limb link must be a child of the body's moving group so a path carries it too. (2) An object that falls, sinks or descends must really cross the frame: wrap the whole object (body + tail/joint groups) in `mv-path-sink-<name>` (any id with sink|fall|drop|plunge|descen|carcass is NOT followed by the camera, so it visibly moves); `python3 tools/fallwrap.py <svg> <first-needle> <last-needle> '<path d>' [dur] [delay]` does the wrapping. A dashed "fall line" or arrow alone with a static object is a defect. (3) After build run `python3 tools/pivcheck.py <slug>`; it lists every chain/joint/rotor pivot that lands far from its part.
- **More object motions (2026-10-24):** `slide` (panel/bar slides in by `data-dx`/`data-dy`, default -960/0; `data-dir="out"` slides out; 0.7 s; split screen = two panels, eraser = slide out + fade), `fade` (`data-from` 0 -> `data-to` 1, `data-dur` .4; ghost trail .1 -> .6), `ticks` (children of the group appear one by one every `data-step` s, default .1; `data-fill` marks the filled ones; grid = quantity), `rack` (focus pull: blurred copies of the group sharpen (`data-dir="in"`) or blur ("out"), `data-r` 14 px, 1.2 s; no SVG filter). `popin` takes `data-axis="x|y"`.
- **Big pictures / camera travel (2026-10-24):** sidecar `"world": [w, h]` (e.g. [3840,1080] to travel sideways, [1920,2160] to scroll down) means the SVG is drawn w x h px; a `mv-track-*` group (data-path, data-delay, data-dur, data-scale) moves the camera over it at constant speed. Draw the world edge to edge; keep the 1920x1080 safe rules per screen. Do not use a log-zoom dive or a stepped/stuttering scroll (rejected).
- **Objects with moving parts (2026-10-19, rule):** never give them a whole-object centre motion (`spin`, `roll`, `flip`, `wobble`, `tremble`, `orbit`, `sway`): `miyaWrapCores` bundles the neighbouring shapes (tower, clock face, stand) into the same group, so the whole thing turns (a wind turbine's tower spun with its blades). Draw each moving part as its own group (`mv-rotor-*` for continuous turning, `mv-joint-*` for needles/hinges) and give the core a gentle type (`swell`, `heartbeat`, `approach`). If the core group itself is the turning part (rotor blades + hub, nothing else), use `mv-core-turn`: only that group turns (90 deg/s) and no neighbours are wrapped in; keep tower/body OUTSIDE the group.

**Centre object `mv-core-<type>` (only when the scene uses one; flexible)**, by its nature (guideline 4-1, `tools/motions.py`): spin, sway, orbit, glide, heartbeat,
flicker, swell, tremble, approach, reveal, squeeze, wobble, roll, pop, ping, stamp, flip, draw, drop. Not the neighbour's type, never a plain bob;
per video at least 10 types, none above 20 %. `draw` traces stroked outlines (give real outlines). Old `mv-glint-core`: type by rotation.

**Axis rule (2026-10-26, round 4, owner request):** every motion group is named after the thing it holds, in English, singular (`mv-core-sway-tree`, `mv-swing-sign`, `mv-sway-person`). The builder (`motions.pivot_of`) turns the name into the pivot: things standing on the ground (tree, pole, tower, person, house, flag, sign …) pivot at the BOTTOM (the trunk stays, the crown sways), hanging things (lantern, bell, rope, vine, icicle …) pivot at the TOP, centred things (ship, scale, planet, wheel, compass needle …) at the CENTRE. Non-round things never spin/roll/flip; heavy bodies never drop. If you draw a tree that really should pivot at the top (an upside-down reflection, say) add `data-keep="1"`. Do not write `data-pivot` to fake an axis the name already gives.
- **Direction rule (2026-10-27)**: a creature or vehicle that travels sideways (`mv-path-*`, `mv-swim-*`, `mv-rollby-*`, `mv-creep-*`, `mv-magnet-*`) must face the way it moves. Draw the head toward the travel; build3 checks it (`tools/facing.py`: dark pupil circles inside the biggest opaque shape = the head side) and mirrors the drawing about its body when they disagree (log `direction sanity`). Shapes without eyes are not checked: add `data-face="left|right"` to the group for vehicles, arrows, boats. Background particle rows (fish, meteors) are oriented by the code. **Wider direction rules (same day, guideline 4-4):** eyeless pointed things (rocket, arrow, probe, plane, comet, ship, boat, sub, sled, train, car… in the group name) are judged by their pointed end; a `mv-path` whose name says down (sink/fall/drop/descend/plunge/dive/settle) or up (rise/ascend/climb/launch/lift/soar/bubble/float/balloon/escape) gets its path reversed when it goes the other way; with an attractor in the picture (a group named hole/vortex/whirl/drain/magnet/gravity/funnel/mouth/maw/sun/star, or sidecar `"attractor": [x, y]`) `mv-magnet` pulls toward it and a path named pull/suck/spiral/drain/inward/toward/into/capture is reversed if it leads away; rain slant, wind lines, fog/cloud drift and horizontal particle drift follow the wind (sidecar `"wind": "left"|"right"`, default = against the travel, else to the right), fish/bird/bat rows swim or fly WITH the travelling object; the drift camera pans along the travel; a riding frog faces the travel and a pushing frog pushes from behind. So: draw flags, smoke, hair and spray leaning the same way and write `wind` when it is not the default; name downward/upward/pulled paths with those words; **Second round (same day, guideline 4-4 B)** also handles these by name: touching gears (gear/cog/sprocket in `mv-spin`/`mv-rotor`/`mv-core-spin`) turn opposite ways (`data-dir` rewritten, the core gear is the reference); a flag group (flag/banner/pennant/windsock/sail/streamer: pole = the tallest thin shape) and leaning shapes (smoke/steam/plume/hair/scarf/cape/spray/grass/reed/kelp/flame…) are mirrored to blow with the wind when the wind is known; a character/animal group (person/man/woman/kid/scientist/owl/cat/bear/deer/cow/bird…, not parts) with pupils is mirrored to look toward the focus (the travelling object, else the attractor, else the centre object) when it looks away; a shadow (id/class shadow/shade) or highlight (highlight/glint/shine/specular/rim-light) drawn INSIDE its object's group is mirrored to the far/lit side of the light (sidecar `"light": "left"|"right"` or the widest sun/lamp/lantern/candle/torch/moon/bulb/fire/window group); the orbiting frog goes the way the ring spins. So name these groups with those words, give shadows/highlights an id inside the object's group, and draw a second-person gaze exchange yourself (only one focus is computed). **Names feed everything (2026-10-27):** `tools/picev.py` reads what the picture shows from object group NAMES and sizes (fire, candle, smoke, steam, water, rain, cloud, ice, forest, flower, desert, sun, space, clock, bell, gear, book, typewriter, coin, chain, heart, bird, insect, crowd, door, flag/windmill, bubble/flask, bone, cave) and the build picks background effects, sounds and name-label entrances from them when the narration says nothing; the frog's outfit and act use them too (guideline 7-2 E). So every meaningful object group gets a plain English name that says what it is (`mv-core-flicker-fire`, `clock-face`, `chimney-smoke`, `sea-water`), never `g1`/`shape3`; background layers keep bg/sky/haze in their name so they are not mistaken for objects.

- **Library kinds (2026-10-29, guideline 4-6)** — six more `mv-<kind>-<name>` groups, use them when the narration calls for exactly that:
  - `mv-draw-<name>`: the strokes draw themselves like a pen, fills follow (maps, blueprints, routes, a sketch being made). Give real stroked outlines. `data-dur` (1.4), `data-delay`.
  - `mv-morph-<name>`: "A turns into B": put the CURRENT shape as the first `<path>` and the TARGET shape as the last `<path>` with `opacity="0"` (same group); `data-back="1"` morphs back; `data-dur` (1.0). One path each, no compound sub-shapes.
  - `mv-toss-<name>`: thrown object on a gravity arc — `data-v` px/s (520), `data-angle` deg (-60 up-right, -120 up-left), `data-g` (1400), `data-deg` turn (240).
  - `mv-skid-<name>`: slides sideways and stops with a snap — `data-v` px/s (900), `data-dist` px (420), `data-res` (800).
  - `mv-coast-<name>`: a wheel / top / coin that spins down — `data-v` deg/s (720), `data-friction` (.12); the axis rule applies (round things only).
  - `mv-regroup-<name>`: 2+ direct children re-arrange from where you drew them into `data-shape` `ring` | `line` | `grid` ("they gathered", "lined up", "formed a circle"); `data-dur` (1.2).
  - You do NOT add: speed ramps (SlowMo on `mv-path` when the sentence says fast/rush), camera shake (RoughEase on earthquake sentences), spring entrances (playful sentences), bursts / grid ripples (background), scrambled / typed labels, lucide pictograms beside labels — the builder picks those from the words. `data-ease="<gsap ease>"` on an `mv-path` overrides the builder's choice.

Background effects (rain, snow, bubbles, fog, rays … 57 kinds, 2026-10-29: + `burst`) and on-screen text effects are added by the builder from the narration words and the palette; do NOT draw rain/snow/particles into the picture (guideline 4-1 "4차 보강").

## 7A. Attachment rules — MANDATORY (2026-10-29, miya: windmill, net, frog legs, tails, bird neck, clock hand, gears, tree, grass, sign post all turned about the wrong point)
Every moving part must be attached to its body (guideline 4-7):
- `data-pivot` of mv-joint / chain / swing / rotor / pendulum = the point where the part TOUCHES the body (on the part AND on the body or parent link within 12 px), never empty space. A hinge pin (small circle) inside the group counts as the support.
- Net / flag / banner on a pole: the swing pivot is the junction of pole end and rim, or put pole + bag in ONE group. Tail / leg / neck / head of a creature that moves (mv-path, glide, swim, creep ...): the part goes INSIDE that moving group. A bird's head belongs to the neck chain.
- Clock hand / wheel: pivot = centre of the round face. Gears: pivot = gear centre, neighbours mesh (centre distance = sum of pitch radii), opposite directions, period proportional to tooth count, inside the circle/shell they sit in (`python3 tools/gearmesh.py`).
- Standing things (tree, reed, grass, sign post, pole, tower): the group holds the thing ITSELF (a sign = post + boards), no ground/shadow/water inside; one group per clump (`tools/splitclumps.py`); the pivot is the FOOT (`python3 tools/setbase.py <slug> <uid>` writes it).
- Label `to` points INSIDE the moving object it names.
- **Axis catalogue (2026-10-29, guideline 4-8) — you do NOT choose axes.** Name the group after the thing, head noun LAST (`mv-sway-tree-oak`, `mv-swing-net-bag`, `mv-joint-bird-neck`, `mv-rotor-gear-1`, `mv-flagwave-flag`); `tools/axis_catalog.md` lists ~380 thing words with their axis rule (foot / hanging point / contact / hub / hoist edge / centre / none) and the motion kinds that fit. Then run `python3 tools/axisfix.py <slug> <your uids>`: it computes the axis from your drawing and writes the missing `data-pivot`s. Do not type pivot numbers for standing / hanging / round things (the tool's point wins); for limbs, tails, necks draw the part OVERLAPPING the body by a few px and let the tool place it, or put a hinge-pin circle in the group. Never put a rotating kind on water / smoke / fire / light / ground.
- **Before you report:** run `python3 tools/axisfix.py <slug> <your uids>` then `python3 tools/attachcheck.py <slug> <your uids>` (fix everything it prints; `--fix` moves label pointers), and for every picture with people, animals, machines or a swinging thing run a partial build and look at `tools/motionaudit.py` strips (red dot on every pivot must sit on the body). The lead repeats the check on the built page (`tools/final_check.py`) — it will find what you skip.

## 8. Sidecar JSON (exact keys)
```
{"centre": "short English description of the centre object",
 "focus": [x, y, scale] or null, "frog" (written by tools/frog_place.py, not by the picture agent: section 12), "focus_word": "exact words from the unit text" or null,
 "sfx": [ {"name": "<library name>", "word": "<exact words from the unit text>", "vol": 0.5-0.8} ],
 "labels": [ ... ], "spot": true, "iris": [x, y], "world": [w, h]}
```
- `iris` (optional): centre of a side subject (x ~400 or ~1500); an `iris` transition grows a circle from there (else off-centre `focus`, else left/right third).
- `focus`: only when the text names a thing to look at; its centre, scale 1.5-2.2 (camera pushes in and holds; rest dims unless `"spot": false`); ~40-50 % of units. `focus_word` verbatim (camera starts just before it is spoken). Detail for 2x zoom.
- `sfx` (0-1 entry, 2026-10-27: a FALLBACK only; `tools/sfx_pick.py` picks the cue from the narration words first and uses your entry only when no word rule matches, or always with `"sfx_lock": true`; so set it only for something the picture shows that the words do not say), `name` from the 92 kinds in `tools/sfx_lib.py` (`python3 tools/sfx_lib.py <dir>` lists them); the original 25: swish, hush, tick, crackle, bubble, wind, bell, click, creak, drip, thud, chime, rustle, pop, pencil, page, cloth, woodblock, sand, rain, splash, step, breath, stone, flutter (soft, unpitched; `bell`/`chime`: dull knock/paper flick; `shimmer` = `hush`; cosmic: section 11). Only for a matching event: crackle fire/cooking; bubble boiling/liquid; rain; splash/pour; wind outdoors/open sky; bell or woodblock alarm/hollow; click lock/latch/sealing; creak wooden hut/door/scale; drip single drop/tear/sample; thud or stone heavy/final; pencil writing/drawing; page or rustle book/paper/records; cloth clothing/body moves; step walking/arrival; sand powder; flutter birds/wings; breath quiet/tension; pop small appearing symbol; hush idea/discovery. The picker keeps ~45 % of units at most and repeats a sound only when the situation repeats; no drones, hums or musical tones.
- `light` (`"left"`|`"right"`, optional, 2026-10-27): where the light comes from when no light-source group is drawn (shadow/highlight side, guideline 4-4 B).
- `wind` (`"left"`|`"right"`, optional, 2026-10-27) and `attractor` (`[x, y]`, optional): the picture's wind and pull centre for guideline 4-4; only when the defaults (wind against the travel, attractor = widest hole/vortex/sun… group) are wrong.
- `labels` (0-3, guideline 3-6; builder overlays HTML):
  ```
  {"type": "name", "text": "Anomalocaris", "x": 1320, "y": 300, "to": [1180, 470], "word": "Anomalocaris"}
  {"type": "num", "text": "539 MILLION YEARS AGO", "word": "539 million"}
  {"type": "say", "text": "Still here!", "x": 1080, "y": 520, "to": [1272, 650]}
  ```
  - `name` (max 28 chars): thing VISIBLE and SAID here (same spelling). x,y = pill centre (~34 px text, ~20 px/letter), `to` = point on the subject. In empty space, not over a face, the centre object or subject. Not again next unit unless the subject changes.
  - `num` (max 26 chars, UPPER CASE): number/date/size/share SAID ("four meters" -> "4 M" ok, "nine meters" -> "10 M" not). Fixed top-left (x 80, y 64; keep free). First number counts up from 0 (years 1000-2100 do not).
  - `say` (max 4 words/24 chars, no digits): reaction of an animal, generic person or thing, `to` = mouth; no fact/number/claim, no real named person, not mocking; ~1 unit in 3 (2026-10-22, owner wants them more often); objects (key, hourglass, rocket, flask) may speak too; up to 2 per unit when two things talk; do not repeat the same line in neighbouring units.
  - `word` (optional): exact words; pops in when spoken (else ~0.4 s after the cut).
  - Safe area x 120-1800, y 80-860, not x > 1660 and y < 190 (logo). With a focus labels follow the zoom (size fixed): keep near it. **A label on a MOVING object follows it (2026-10-27):** when `to` (else x,y) lies on a travelling group (mv-path/swim/rollby/slide/sink/rise/magnet/creep/hop/float/circle/scroll, or a glide/orbit/drop core) the builder moves the pill, its line and the bubble tail with that group, so place such labels relative to where the object is when the unit starts, and do not try to offset them by hand for the motion. ~Half the units get labels; chalkboard units none.
- Validate the JSON (python `json`).

## 9. Check and work method
- `python3 tools/svgshot.py <your_preview_dir> f1.svg ...` and LOOK at each (bright centre, no stray shapes, nothing cut off, this style, no thick outlines).
- `python3 tools/labelshot.py <slug> <your_preview_dir> <uid> ...` prints problems (build stops on any) and writes `<uid>_lab.png`; fix overlaps.
- In order: read text (+ prev/next), decide, write svg + json; preview in batches of 3-4, fix at most once.
- `python3 tools/attachcheck.py <slug> <uids>` must print 0 problems for your units (section 7A) before you report.
- Final answer: one line per uid `uid | centre | focus_word or - | sfx or -`, plus any problem.

## 10. Shorts (vertical) — overrides
- `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1080 1920" width="1080" height="1920">`. NEW pictures only (no reused/cropped landscape), under ~100 KB.
- Centre object at (540, 860), diameter 150-230 px; "match" keeps the previous place/size.
- Overlays: top ~290, bottom ~290, right ~140 px; captions y ~1440-1560. Important content in x 100..940, y 300..1400 (backgrounds may fill). "slide": none in x 0..100, 980..1080.
- Stack subjects vertically. Focus scale 1.5-2.0, focus/label coords in 1080x1920. Num badge x 100, y 330. Label safe area x 100-940, y 300-1400.
- Previews: `SHOT_W=1080 SHOT_H=1920 python3 tools/svgshot.py <dir> ...`

## 11. Cosmic mode (space videos) — overrides
`config.py` `STYLE = 'cosmic'`, `PAL_DEFAULT`: `nebula` (nebulae, galaxies, star birth), `aurora` (atmospheres, magnetospheres, solar
wind), `deepfield` (far galaxies, black holes, scale), `solar` (Sun, supernovae, flares); scene `PAL` mixes up to 3. Surfaces and light, thin lines kept.
1. Night on 70 %+ of units; paper/dusk only for everyday start/end scenes.
2. Nebula layer (required): 3-4 big overlapping `radialGradient` shapes (40-90 % of canvas), `pal.accents` + `night_glow`, opacity 0.15-0.55, edges to `stop-opacity 0`.
3. Stars: 120-250 small (r 0.8-1.6 px, opacity 0.4-0.9); 12-25 medium (2.5-4 px) in `mv-glint-s1`, `mv-glint-s2`, `mv-glint-s3` (staggered twinkle); 2-4 large with a cross flare (4 thin lines + radial glow). None on the centre object or key subject.
4. Bodies: two radialGradient layers (body + atmosphere glow), thin bright rim arc on one edge, shadow side darker than `night_bottom`, some hatching, sketch outline (2.5-3 px, `night_line`) only on the main body.
5. Orbits: `night_line`, opacity 0.35, dotted/thin, only when needed, not the neighbour's layout (no-rings rule stays). Beams: 1-3 thin gradient trapezoids.
6. Centre rule holds (960,500, 170-260 px), `mv-core-<type>` by nature (planet `spin`, star `flicker`/`ping`, moon/satellite `orbit`, nebula `swell`...), not the neighbour's type.
7. Extra groups: `mv-glint-s*` twinkle, `mv-drift-nebula` (one nebula layer +-25 px, 20 s period), `mv-orbit-*` (small body + an invisible full orbit circle that sets the orbit centre), `mv-pulse-core` (star/sun brightness). 4-8 `mv-` groups.
8. Never: letters, thick black outlines, 3D/photo look, copied photos, wrong astronomy (script's numbers where scale matters, else symbolic).
9. `sfx.name` (fallback only, see section 8): `sparkle` (starlight), `bloom` (flare, star birth), `starfall` (falling light), `pulse` (signal), `warp` (0.3 s, change of place), `glimmer` (tiny glints), `tick`, `click`, `pop`, `drip`, `pencil`, `page`, `woodblock`, `stone`, `step`, `cloth`, `thrust`, `static`, `radio`, `clock`. Not `riser`, `sweep`, `hush`, `breath`, `wind`, `rain`, `swish` (the picker swaps earthly textures for the space family anyway).
10. Black holes: four looks by what the unit says. Never a thin flat ring round a black disc alone. All: pure black shadow disc + thin bright photon ring.
   - **Lensed disk** (default, side view): THICK glowing accretion disk (layered strokes, brightest on the approaching side) in front of the shadow; far side bent over the top (thinly under) as a crescent touching the shadow and merging into the disk at both ends, never a floating loop. For orbits, planets nearby, ISCO, horizons, scale, tides.
   - **Face-on ring**: thick soft ring, one side brighter (Doppler), soft halo, no disk ellipse. For the real EHT images, the shadow, named holes (M87*, Sagittarius A*, TON 618).
   - **Whirlpool**: gas arms spiralling in, coral/gold outside to white-hot at the edge. For swallowing, feeding, falling in, spin, frame-dragging, stirring; not often (looks like a galaxy).
   - **Simple dark disc + thin ring**: only small/far (under 120 px), diagram icon, or a quiet hole ("stopped feeding").
   - Vary the look between neighbouring black-hole units unless `match`. References: `tools/ref/blackhole-lensed-disk.svg`, `blackhole-face-on-ring.svg`, `blackhole-whirlpool.svg` (copy the idea, scale it, add own backdrop and motion groups).

## Appendix A — revising the backdrop of existing pictures
Remove old rings/rays, do not redraw people/objects. Per unit:
1. Delete the radial "rays" path (many `M..L..` lines from the centre), the ring circles (r ~330-640) and the big glow disc behind. Keep people, props, centre object (position, size, `mv-core-*`/`mv-glint-core`), all `mv-` groups and ids.
2. New backdrop for THAT unit's text per section 5 (read prev/next too), unlike neighbours.
3. Bg-mode colours as base wash; backdrop low-contrast; bottom 200 px calm.
4. Centre object stays at (960,500), same size/colour; a meaningless "sun/ring" centre may become a lamp, window, clock, lens... (update `centre`).
5. Section 2 holds; keep `focus`/`focus_word`/`sfx` (fix coords if the focus target moved); never rename `mv-` groups. Edit in place (backup), preview outside `art3/`, no rays/rings left.
6. Final answer: one line per uid `uid | backdrop kind`, plus any problem.

## 12. Mascot frog (2026-10-24, rewritten 2026-10-25, guideline 7-2)
Picture agents do NOT draw the frog and do NOT write the `frog` sidecar key. In picture scenes the frog is a companion, not an explainer: after the pictures exist `tools/frog_place.py <slug>` puts it ON a moving object (injected into that `mv-` group, so it rides along) or roams the free part of the background (small; swims/floats/rolls/hops on a platform; `roam`, guideline 7-2) with a speech-bubble sound word (`says`), moods per sentence, a helmet (space) or goggles (water), no arm. Only the chalkboard has the explainer frog that points. So: leave a spot ~150x150 px free on top of the main moving object (a rideable group: core swell/heartbeat/wobble/sway/glide/approach/drop/ping/tremble, path, slide, swing) and in a bottom corner, and keep labels away from the top of that object. The frog must not cover the subject, labels or the logo corner.

Round-3 hooks (2026-10-26, the frog's relation acts are chosen by regexes over the narration + these group/id names, never by judgement): name a person group with person/people/astronaut/scientist/villager/figure/… in its id (frog waves beside it); name balloon/branch/rope/wire/ring/hook/tail/fin/antenna/pole groups by that word (frog hangs under it); a big solid object the frog can hide behind must NOT be named glow/halo/ring/bg/sky/grid/star/cloud/line/path (those are skipped as "soft"); one-shot motions (`path`, `slide`, `slam`, `popin`, `rise`, `topple`, `flip`) get an automatic breathe once they stop, so do not add a second idle group to the same object; cosmic pictures get one automatic shooting star in the upper sky, so leave the top 30 % of a space backdrop free of text.
Joint rig + contact acts (2026-10-29, guideline 7-2 I): the frog now has joints and meets MOVING props of the picture at the prop's own time (a small thing that `mv-core-drop`s onto its head — the drop starts 160 px above where it is drawn and stops there, so draw it at its landing spot, not in a tree canopy; a sign that `mv-topple`s onto it, a wheel that `mv-rollby`s under its jump, a ball that `mv-bouncing`s beside it, a `mv-swing` it hangs under, a `mv-rise` box it holds up), climbs rope/pole/tree/ladder groups, crosses a long thin rope/beam/plank group, dangles from balloon/branch/hook groups, trips over a low rock/root/log/puddle group on its lane, and does an act that fits its outfit (wizard casts, chef stirs, cowboy lassoes...). More props that trigger a gag (same day, 2nd round): a big heavy `mv-core-drop` (boulder/anvil/crate: the frog gets flattened), a `mv-bouncing` ball wider than 120 px (it bounces on top), a `mv-pendulum`/`mv-swing` taller than 250 px (it gets bowled over), `mv-slam`/`mv-squash` (thrown up by the thud), `mv-magnet` (dragged along), `mv-hop` creatures (hops along), `mv-drip` (dripped on), a `mv-spin` wheel/gear/fan 160-600 px (rides the rim), `mv-popin` (lifted on top), a long `mv-unroll` carpet (swept off its feet), `mv-ascend` balloons (hangs under), `mv-sink` rafts (waves for help). All of this is chosen by `tools/frog_place.py` from the `mv-` kind, the group name, the group size and the sentence words. So: give small props a real motion (`mv-core-drop`, `mv-topple`, `mv-rollby`, `mv-bouncing`, `mv-swing`, `mv-rise`) and plain names (apple, sign, wheel, ball, swing, crate, rope, pole, ladder, tree, rock, root, log, puddle); a prop drawn static or named `g7` never triggers a gag. Keep ~120x120 px of the ground free under a dropping prop and at the near end of a rolling prop's lane. Still: do not draw the frog.

Script-word -> gag-prop table (2026-10-29, miya "대본 규칙과 그림 규칙을 맞춰라"): when the unit's narration has one of these words AND the scene can hold a small prop without covering the subject, draw that prop with that motion (and the plain name) so `frog_place.py` can stage the gag. The frog side is already coded (guideline 7-2 I-4); this is the picture side.
| narration says | draw | gag |
|---|---|---|
| fall, drop, land, plummet, tumble down, hit (something small) | a small thing above head height with `mv-core-drop` (it lands where you draw it, start 160 px higher) | bonk / sidestep / catch / splash; big heavy things (`boulder`, `anvil`, `crate` in the name) -> flattened |
| topple, collapse, fall over, tip | a pole / sign / stack with `mv-topple` | squish |
| roll, rolling, wheel, boulder, barrel, runaway | `mv-rollby` across the ground | dodge / chase |
| bounce, spring, boing | a ball wider than 120 px with `mv-bouncing` | trampoline; smaller -> bumped |
| swing, pendulum, wrecking ball, hang | `mv-swing` / `mv-pendulum` from a top pivot (taller than 250 px for the knock-over) | swingride / knocked |
| stamp, slam, crash down, thud | `mv-slam` or `mv-squash` on the thing that lands | shockwave |
| magnet, attract, snap to, pull toward | `mv-magnet` with `data-dx` >= 120 | magnetized |
| hop, rabbit, frog, grasshopper, bounce along | `mv-hop` on the small creature | hopalong |
| drip, leak, melt, tap, stalactite | `mv-drip` with `data-fall` >= 80 | dripped |
| wheel, gear, mill, fan, carousel turning | `mv-spin` on a 160-600 px wheel named wheel/gear/fan/... | rimride |
| pop up, appear, sprout, emerge | `mv-popin` (<= 320 px) | launched |
| unroll, carpet, scroll, timeline opens | `mv-unroll` wider than 400 px | unrolled |
| rise, float up, balloon, lantern | `mv-ascend` (<= 320 px) | balloonride |
| sink, go under, submerge, raft | `mv-sink` (120-500 px) | sinkride |
| lift, carry, heavy load | `mv-rise` box (<= 320 px) | lift |
| wind, gust, storm (no vehicle) | nothing extra: the frog braces and is blown | blown |
| rope, tug, haul, anchor | a `rope`/`chain`/`cable` group wider than 150 px | tug |
No matching word -> no prop for the frog's sake; the frog then roams or does a calm act. Never draw the frog.

Frog automation hooks (2026-10-26): draw hut/house doors as separate elements with `id="door1"`, `door2`, … (enables the `huts` act); name book/notebook/page/paper/desk/card/chart/board groups with that word in the id (enables `doodle`); ride objects that get pushed (lens, crate) should have the grip point at the lower right of their group. For heavy topics set `FROG_TONE = 'serious'` in config.py.
