# Miya's Lab — cine spec (3D look, read fully)

The cine look (user decision 2026-10-14) is how every Miya's Lab video is made: dark, realistic 3D scenes (Three.js)
under a calm HUD, after the user's reference video 1 (motion, transitions, HUD, the 2:11-2:40 "one 3D stage, information changes")
and reference video 2 (realistic 3D: metal, light, glowing particles). Guideline: `docs/miyas-lab-guideline.md` chapter 3 (rules), 6 (data cards), 10 (work order).

## 1. What a video is made of
- **Units** (`plan.json`, one per narration clause, same split as before) give the timing. Nothing is drawn per unit any more unless
  the chapter is in `cuts` mode.
- **Chapters** (`videos/<slug>/cine.json`) group units. Each chapter is one of:
  - `stage` — ONE 3D scene stays for the whole chapter and changes with the narration (rotation, light, deformation, particles,
    camera). Per unit only the text layers change: rolling keyword, subtitle, log line, plot value, badge. No cuts inside.
    Use it where one object carries the idea (a black hole, a planet, a field of clocks, spacetime). This is the reference 2:11-2:40.
  - `cuts` — a sequence of **shots**; each shot is one 3D scene over one or more units (aim 6-15 s per shot, never per clause),
    joined by transitions. Use it for a story moving through places or examples.
  - Mix both through a video by content. Data-card scenes (config `CHALK`, guideline chapter 6) become **data cards** automatically.
- **Beats** (`cine.json` `beats`, per unit id): the text and plot values for that unit.

## 2. cine.json (exact keys)
```
{ "title": "short series title for the HUD", "accent": "#ffc65a",
  "chapters": [
    { "id": "c1", "label": "Chapter 1", "title": "The physics of stolen time", "mode": "stage", "from": "U001", "to": "U009",
      "tr": "dip",                                   // transition INTO this chapter (first chapter: cut)
      "plot": {"label": "The pace of time", "min": 0, "max": 1},   // optional: a line drawn over the chapter from beat "plot" values
      "badge_label": "Clock rate",                   // optional: label over the badge values
      "scene": {"type": "dataglobe", "params": { ...cues... }} },
    { "id": "c2", "label": "Chapter 2", "title": "...", "mode": "cuts", "from": "U010", "tr": "dip",
      "shots": [ {"from": "U010", "type": "ocean", "params": {...}},
                 {"from": "U014", "type": "blackhole", "params": {"look": "lensed"}, "tr": "whip"},
                 {"from": "U016", "type": "clockfield", "tr": "flash"} ] } ],
  "beats": { "U001": {"kw": "Now", "sub": "Look down at your wristwatch.", "log": "Your watch: one tick per second",
                      "badge": "Same everywhere?", "plot": 1},
             "U006": {"kw": "Wrong", "acc": true},
             "U016": {"card": "On Earth, more than *twenty-three years* have vanished."} } }
```
- `to` is optional (a chapter runs until the next chapter or data card). Every unit must belong to a chapter (the build checks gaps).
- **Cues** — any string param of the form `"U007"` (start of that unit) or `"U009:standstill"` / `"U008:bent stretched"` (the moment
  that word or phrase is spoken inside that unit) is turned into a time. Scenes use cues to start their changes exactly on the words.
- Transitions: `cut`, `dip` (to black, the default between chapters), `xfade`, `flash` (light burn), `wipe` (diagonal with a light
  edge), `iris` (circle from `"tro": [x, y]` in 0-1 screen fractions — put it on the subject), `eye` (opens from a line), `push` (up),
  `whip` (fast pan with motion blur), `zoom` (through the subject at `tro`), `blinds` (bars in the palette's muted tones).
  Pick by meaning: chapter change `dip`/`blinds`; speed or sudden `whip`/`flash`; into/inside `zoom`/`iris`; reveal `eye`; up/down
  `push`; same place, time passes `xfade`. Never the same transition twice in a row; `flash` at most once per chapter.

### Beats (all optional)
| key | what it does | rules |
|---|---|---|
| `kw` | big thin keyword at the left; rolls (blur out up, blur in from below) to the next `kw` | 1-3 words or a number, ≤ 16 characters, **from the narration of that unit** (or its exact meaning: "45 µs" for "forty-five microseconds") |
| `acc` | keyword in the accent colour | the turn of the chapter only (1-2 per chapter) |
| `sub` | serif line under the keyword | ≤ 60 characters, paraphrase of the unit, no new facts |
| `log` | adds a line to the right-side list (stage chapters); older lines move up and dim | ≤ 34 characters; a running record of the argument |
| `badge` | value under `badge_label` at the lower right | short word or number, changes only when the narration changes it |
| `plot` | value of the chapter plot at this unit | a number in the plot's min..max; the line eases between units |
| `card` | centred serif sentence over the dimmed scene (the reference's text interlude) | ≤ 90 characters, `*word*` = accent; unit ≥ 2.5 s; at most ~1 per chapter |
- Numbers and names shown must be said in that unit or already said before (same rule as the old labels). No invented figures.
- Keep the left column quiet: about half of the units get a `kw`; units that only continue the sentence get nothing or only `sub`.

## 3. Scene library (`tools/cine/scenes/*.js`)
| type | what | key params |
|---|---|---|
| `dataglobe` | glowing point sphere (stage) | `satellites`, `river:[on,off]`, `desync`, `grid`, `bend`, `stretch`, `crush`, `slow:[from,to]` (all cues), `bg`, `orbit`, `dist`, `side` |
| `blackhole` | black hole, four looks | `look`: `lensed` / `ring` (real EHT images, M87*, Sgr A*) / `whirlpool` (swallowing, spin) / `icon` (far, small); `approach` (+ in, - out), `dist`, `tilt`, `spin` |
| `ocean` | dark alien sea, black hole in the sky, wave wall | `look`, `wall`, `speed`, `start`, `bh`, `bhScale`, `rise` |
| `clockfield` | a spiral of solid 3D clocks in navy-violet space (smoked body, glowing gold rim, light-point marks, glowing hands, halos, gold dust river); rims pulse together each second; camera pulls back from one clock | `n`, `pull`, `bg` |
| `whale` | realistic swimming great whale in the open ocean (stage) | cues `court`, `courtOff`, `calf`, `exhale`, `sink`, `deep`; `length` |
| `watch` | metal wristwatch close-up | `gold`, `time:[h,m]` |
| `river` | river of light across a dark plain | `color`, `speed` |
| `cubefield` | cube field bent into a well, chrome ball | `bend`, `crush`, `slow` (cues), `nx`,`nz` — **heavy**: keep ≤ 20 s per video |
| `void` | slow star field (behind data cards; also a calm pause) | `bg`, `tint` |
All scenes take `side` (subject offset, + = right; the left third holds the text) and are framed for 1920x1080 and 1080x1920.

## 3A. Realism of objects, animals and plants (user decision 2026-10-14: "the clock scene looks like a 2D image, not real —
upgrade how objects, things, animals and plants are made")
A thing must read as a solid, lit, physical object, never a flat icon or a coin-like disc.
- **Form**: real proportions and thickness. Man-made things: real parts with depth (case + bezel + dial + crystal + hands for a
  clock; bevels everywhere, no zero-thickness planes for solid objects) — separate parts are right for machines.
- **Depth that survives a turn** (user, 2026-10-14: "once things rotate, flat ones give themselves away"): anything that turns or is
  seen at an angle must show thickness and structure from the side — e.g. a clock: deep case with rounded sides and a domed back
  (`LatheGeometry`), raised bezel, recessed dial, domed crystal, raised markers, crown and bow. A disc or a card is never enough.
- **Living things are ONE mesh** (user rule 2026-10-14, after the whale's fluke came off the body): never a body plus separately
  positioned fin/tail/limb objects. `MIYA.kit.body()` sweeps the body along a spine; tail fins and flukes come from its width/height
  profiles plus a sweep in `deform()`, small ridges (dorsal fin) from a local bump in `deform()`, and flat parts that are not tubes
  (flippers, leaves, petals: `kit.fin()`) go in `extra` — placed in body space, merged into the same mesh and moved by the same
  deform, so nothing can come apart. Only eyes/teeth may be small separate objects. Reference: `scenes/whale.js`.
- **Joints** (an arm bending, a leg walking, a neck turning, a wing beating): one mesh with a skeleton — `THREE.SkinnedMesh` +
  `THREE.Skeleton`; every vertex carries `skinIndex`/`skinWeight` for 1-2 nearby bones (blend weights across the joint so the skin
  bends smoothly, no seam). In `draw(t)` set each bone's rotation from `t` only (seek-safe), e.g. elbow = `sm(cue(c), cue(c)+1, t) * 1.9`.
  Keep bones few (a human arm: shoulder, elbow, wrist). People only as silhouettes from behind (rule 2 below).
- **Surface**: procedural textures from `kit.noise()` — colour variation (mottling, grain, rust, bark, scales), a normal map from a height
  canvas (`kit.normalMap()`: pores, pleats, scratches, veins) and roughness that matches the material (wet skin clearcoat, polished metal
  low roughness + `env()`, matte rock high roughness). UV canvases: set `flipY = false` when the canvas rows mean v.
- **Life**: living things move by deforming (swim wave along the spine, breathing, swaying stems), and attached parts follow the body.
  Machines move by their mechanism (hands tick, gears turn, pistons slide).
- **Light and air**: a key light, a coloured rim light from behind, ambient/hemisphere for the environment; atmosphere with fog
  (underwater blue `FogExp2`, haze, smoke), god rays `kit.shafts()`, particles `kit.snow()` (marine snow, dust, pollen) for depth and
  scale; `kit.surfaceFromBelow()` for underwater shots. Dark, cinematic exposure — no flat full-bright lighting.
- **Scale**: show size with a known reference drawn as a ghost outline (the whale scene's basketball court) or companions (a calf).
- Reference scenes: `tools/cine/scenes/whale.js` (animal), `clockfield` in `basic.js` (objects).
- **Surfaces stay realistic** (user decision 2026-10-15): a "look C" (dark bodies + glowing outline + mesh lines + points) was
  tried on all outdoor samples and rejected ("the earlier images were better"). Keep realistic materials, light and atmosphere;
  fix awkward spots by better form, lighting and framing, not by switching to an outline/point style.
- **One visual language** (user, 2026-10-14: "the clocks feel cut off from the other scenes"): realism serves the series look, not
  the other way round. Every scene sits in the same world as dataglobe/blackhole: dark navy-violet (space) or deep blue (sea)
  backgrounds, light carried by glowing edges, light points, halos and dust in the palette's warm accent, stars or particles for
  depth. A realistic object in a space scene gets an emissive rim/marks and a halo, never a flat brown or grey prop under plain lights.

## 4. Writing a new scene (when the library has nothing that shows the idea)
Put it in `videos/<slug>/scenes/<name>.js` (one file may define several types). Template:
```js
(window.MIYA = window.MIYA || { scenes: {} }).scenes.mything = function (ctx, p) {
  const { T, sm, rng, cue } = ctx, K = window.MIYA.kit;   // K = realism kit (section 3A)               // T = THREE (r169); ctx.W/H/VERT, ctx.t0/t1 (shot span), ctx.ACC (accent)
  const S = new T.Scene(); S.background = new T.Color('#02030a');
  ctx.stars(S, 2500, 300, { seed: 7 });           // helpers: points(n,{size,opacity,color}), glow(parent,color,scale,op), ctex(size,fn),
  const cam = new T.PerspectiveCamera(40, ctx.W / ctx.H, .1, 800); ctx.side(cam, .1);   //   env() (reflections), rng(seed), sm(a,b,x)
  // build geometry ONCE here (deterministic: use rng(seed), never Math.random)
  return { scene: S, camera: cam, draw(t, u) {   // t = video time, u = time since the shot started
    // set every moving thing from t / u / cue(...) only — no state carried from the previous frame
  } };
};
```
Hard rules
1. **Seek-safe**: `draw(t)` must give the same picture for the same `t` no matter which frames were drawn before (chunks render in
   parallel and start in the middle). No `Math.random`, no `Date`, no accumulation (`x += ...`) across frames, no `requestAnimationFrame`.
2. No text, letters or numbers inside the 3D scene (the HUD carries all text). No logos, no recognisable film designs, no real
   people's faces (silhouettes from behind at most).
3. Colours: dark backgrounds (`#01020a`-`#141a3a`), the video palette's accents for light; realistic materials (`MeshStandardMaterial`,
   `env()` for metal), additive glow for light, fog for depth. Keep the subject inside the right two thirds (`side`), nothing important
   under the caption band (bottom 160 px) or the HUD corners.
4. Budget: on the render server a frame costs about 3x what `tools/cineshot.py` measures here. Aim for ≤ 2 s/frame here
   (≤ 1 s for scenes longer than 30 s). Avoid per-frame `computeVertexNormals` on more than ~60k vertices and more than ~3000 instances.
5. Physics true to the script: follow its numbers where scale matters; otherwise draw symbolically. Black holes: the four looks above.
6. One file per idea, comment the params at the top like the library files.

## 5. Check before handing in
```
SLUG=x python3 tools/build_audio.py                    # audio + timing    (Shorts: VERT=1)
SLUG=x python3 tools/build_cine.py                    # page; prints warnings/errors (missing cues, gaps, unknown scene types)
python3 tools/cineshot.py render/x /tmp/x_prev 5 30 61.2 ...   # look at every new shot at its start, middle and a cue moment
python3 tools/cineshot.py render/x --estimate          # render cost -> chunk count for render/.chunked
```
Look at every screenshot (Read tool). Fix overlaps with the text column, empty frames, blown-out white, and page errors.
Render: write `"<slug> <chunks>"` lines into `render/.chunked` and push (render-chunked.yml); Shorts use their own slug lines.
