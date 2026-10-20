# quantum-god — art brief (shared by all picture agents)

Read fully: `tools/art_spec.md` (section 5 backdrop rules: every picture gets a backdrop that fits its own text, no concentric rings or radiating-line backdrops, neighbouring units never share a backdrop kind, at most 2 of 12 units share a kind; people follow 6A/6B with `tools/body.py` and `tools/hands.py`; Shorts also follow section 10).

Paths: repo root is `/home/user/youtube-script-daily`.
- plan: `videos/<SLUG>/plan.json` (use the entries for YOUR uids: `bg`, `pal`, `text`, `prev`, `nxt`, `transition_in`, `dur`)
- output: `videos/<SLUG>/art3/<uid>.svg` and `<uid>.json`
- preview: `python3 tools/svgshot.py <preview dir> f1.svg ...` (Shorts: `SHOT_W=1080 SHOT_H=1920`)
- SLUG given in your task: long `quantum-god`, Shorts `quantum-god-short1/2/3`.
Write ONLY your own uids. Scratch work only in your own folder. No git. Palettes are a skeleton (3-5): add or change colours to fit the subject.

## Topic
Quantum mechanics and what it does and does not say about God. Tone: awe and curiosity, calm, honest, NOT mocking any religion. Show experiments, instruments and abstract physics diagrams. NO portraits of real people (Einstein, Bohr, Heisenberg, Bell, Hawking, Planck, Laplace, Schrodinger, Everett, Wigner, Aquinas, Newton, Berkeley): show desks, chalkboards without readable text, instruments, silhouettes from behind, a conference hall from far away. NO religious symbols that mock (no skulls/devils); a single warm light, an empty throne room as an abstract set, or a clockwork may stand for the old picture of order. No text or numbers inside pictures (labels are added by the builder).

## Visual motifs (keep consistent)
- **Clockwork**: brass gears, a pendulum, an orrery. Old, ordered, warm gold. Cracks appear in later scenes.
- **Electron/wave**: small bright dot with a soft glow; waves as thin overlapping ripples with a pale-blue/gold palette. Double-slit rig: a plate with two narrow slits, a screen with a pattern of bands (draw bands as soft vertical stripes of varied brightness).
- **Dice / roulette** for chance (calm, not gambling-glitzy). **Fog** for uncertainty.
- **Entangled pair**: two glowing orbs far apart joined by a thin faint line; two sealed envelopes for the classical picture.
- **Cat scene**: a sealed box, a silhouette of a cat shown as a soft shape only; no harm, no poison shown (use a closed box with a small glowing atom icon).
- **Modern person** (hook/ending): a calm adult in a dark-teal jacket and grey scarf, short dark hair, simple dot eyes; ids `mv-breathe-gazer`, `mv-nod-gazer`.
- Scale scenes (vacuum, big bang, CMB, Hawking, heat death): cosmic palette with soft radial gradients, no filters.

## Model split (CLAUDE.md)
People, animals, creatures or complex compositions -> Opus; simple objects, diagrams, landscapes -> Sonnet.
