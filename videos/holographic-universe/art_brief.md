# holographic-universe — art brief (shared by all picture agents, long video and Shorts)

Read fully: `tools/art_spec.md` (section 5 backdrop rules: every picture gets a backdrop that fits its own text, no concentric rings or radiating-line backdrops, neighbouring units never share a backdrop kind, at most 2 of 12 units share a kind; people follow 6A/6B with `tools/body.py` and `tools/hands.py`; **cosmic mode section 11 applies** (STYLE='cosmic': night >= 70 %, nebula layers, 3-tier stars, planets with rim light, `mv-glint-s*`, `mv-drift-nebula`; paper/dusk only for the everyday scenes); Shorts also follow section 10).

Paths: repo root is `/home/user/youtube-script-daily`.
- plan: `videos/<SLUG>/plan.json` (use the entries for YOUR uids: `bg`, `pal`, `text`, `prev`, `nxt`, `transition_in`, `dur`)
- output: `videos/<SLUG>/art3/<uid>.svg` and `<uid>.json`
- preview: `python3 tools/svgshot.py <preview dir> f1.svg ...` (Shorts: `SHOT_W=1080 SHOT_H=1920`)
- SLUG given in your task: long `holographic-universe`, Shorts `holographic-universe-short1/2/3`.
Write ONLY your own uids. Scratch work only in your own folder. No git. Palettes are a skeleton (3-5): add or change colours to fit the subject.

## Topic
The holographic principle: from the hologram on a credit card, through black hole entropy and Hawking radiation, the information paradox, 't Hooft/Susskind, Maldacena's duality (a conjecture, anti-de Sitter space is not our universe), entanglement and space, the Page curve, the Holometer test. Tone: awe, curiosity, calm and HONEST (the video says clearly that nothing is proven for our universe). Show instruments, abstract physics diagrams, black holes, boundaries, light. NO portraits of real people (Einstein, Hawking, Bekenstein, 't Hooft, Susskind, Maldacena, Wheeler, Preskill, Thorne, Gabor, Page, Hogan, Schwarzschild): show desks, chalkboards without readable text, instruments, silhouettes from behind, a conference hall from far away, a baseball encyclopedia as a plain closed book. No text or numbers inside pictures (labels are added by the builder). No logos (the card hologram is a generic shiny square with a simple abstract motif).

## Visual motifs (keep consistent)
- **Hologram**: a flat translucent plate or sheet (thin edge-lit rectangle) with a glowing 3D shape floating above or behind it; fine interference ripples (thin overlapping arcs, pale cyan and gold) on the plate; a broken plate whose pieces each still show the shape (S04). No rings/rays as backdrop; ripples live only ON the plate.
- **Black hole**: use the four looks from `tools/art_spec.md` section 11 item 10 and pick the one that fits the text (shadow with bright ring only in S07 where the real Event Horizon image is described; horizon as a dark sphere with thin lensing arcs; accretion disc edge-on; wireframe/graph look for the diagrams). Event horizon in diagrams: a thin glowing sphere/line, matter (small dots) approaching, a mesh of small square patches on the sphere surface for the entropy/area scenes (S11, S12, S15).
- **Boundary / dictionary**: a bowl-shaped or box-shaped 3D region drawn as a transparent glass volume, with a faint mesh on its surface; the interior shows curved space as a bent grid, the surface shows a flat pattern of small glowing dots; a thin double arrow between them for "two languages". Keep it diagrammatic and calm.
- **Entanglement**: two glowing orbs joined by a thin faint line; many such links stitching a grid of space together (S23).
- **Emergence**: tiny dots (molecules) whose crowd forms a smooth flowing shape (S24, S25).
- **Page curve / islands**: a simple rising-then-falling curve drawn as a glowing line on a dark diagram plate (no axis numbers/text); a black hole with a small bright island region inside (S26).
- **Holometer**: two long laser arms meeting at a right angle in a field/lab corridor seen from far above, thin beams, mirrors as small discs (S27). **Quantum lab**: a cryostat chandelier or a small chip with a glowing core, calm (S28).
- **Plasma**: heavy nuclei colliding as two bright discs flattening into a glowing swirl (S22), warm gold/white.
- **Modern person** (S01 hands, S33 room, S34 outro): the S01 picture is the viewer's own hands (hands.py, round or open pose) on a desk with a phone; S33 a calm adult seen from behind sipping coffee by a window in morning light. Adult in a dark-teal jacket and grey scarf, short dark hair, simple dot eyes; ids `mv-breathe-gazer`, `mv-nod-gazer`.
- **Everyday props** (paper/dusk scenes): credit card (generic, a small shiny square), cup of tea on a lab desk (S08), a hard drive as a plain box with a small disc (S11 is a chalkboard, no picture), Dublin-style conference hall seen from far (S14), two desks far apart with notebooks (S15; no faces).
- Scale scenes (S06 horizon, S19, S20 cosmic horizon): cosmic palette with soft radial gradients, no filters.

## Model split (CLAUDE.md)
People, animals, creatures or complex compositions -> Opus (S01, S33, S34, S14, S15 and any scene with a person); simple objects, diagrams, space scenes -> Sonnet.
