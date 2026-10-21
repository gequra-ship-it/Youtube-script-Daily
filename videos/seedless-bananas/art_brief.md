# seedless-bananas — art brief (shared by all picture agents)

Read fully: `tools/art_spec.md` (section 5 backdrop rules: every picture gets a backdrop that fits its own text, no concentric rings or radiating-line/ray/sunburst backdrops, neighbouring units never share a backdrop kind, at most 2 of every 12 units share a kind; vertical Shorts also follow section 10; people follow 6A/6B with `tools/body.py` and `tools/hands.py`).

Paths: repo root is `/home/user/youtube-script-daily`.
- plan: `videos/<SLUG>/plan.json` (use the entries for YOUR uids: `bg`, `pal`, `text`, `prev`, `nxt`, `transition_in`, `dur`)
- output: `videos/<SLUG>/art3/<uid>.svg` and `<uid>.json`
- preview: `python3 tools/svgshot.py <preview dir> f1.svg ...` (vertical Shorts: `SHOT_W=1080 SHOT_H=1920`)
- SLUG is given in your task: long `seedless-bananas`, Shorts `seedless-bananas-short1/2/3`.
Write ONLY your own uids. Scratch work (generator scripts, previews) goes ONLY in your own folder given in your task. No git. Delete big preview dirs when done.

## Topic
Why bananas are seedless and how they are grown, as natural history and plant science: a kitchen counter and a bunch of bananas; apple/orange/watermelon halves with seeds next to a banana cross-section with tiny dark specks; a huge plantation; a wild banana split open and packed with hard black seeds; two wild species as botanical-plate style drawings; chromosome diagrams (two sets vs three sets, drawn as coloured rods, no letters or numbers); a plant cell dividing unevenly; a swelling fruit without pollination (parthenocarpy); early New Guinea farmers in a forest clearing; a banana plant cut open to show the pseudostem layers like an onion; the underground corm with suckers; a farmer cutting a sucker; a tissue-culture lab (jars, jelly, tiny plantlets); rows of identical banana plants (clones); Gros Michel bunches on a 1930s-looking ship deck; candy, ice cream and milk beside banana (flavor story); a soil fungus entering roots under the ground (cutaway), wilted yellow leaves; abandoned fields; Chatsworth-style glasshouse; the Cavendish bruising in a padded box; map-like cutaway of spreading fungus (no text); Colombia farm entrance with a disinfection mat; a lab bench with a GM seedling; many banana varieties on a market table (red, apple, plantain); potassium atom diagram and a decay burst; a radiation detector gate with a banana crate; a berry cross-section (skin, flesh, seed layer) next to strawberry and raspberry; a young bunch bending upward; hands/fingers of a bunch; ethylene gas wisps between a banana and an avocado in a paper bag; a cargo ship; a ripening room; brown sugar spots; matooke steaming in Uganda (a cooking pot, green bananas, family kitchen); sprayer plane over a plantation; a frozen gene bank (liquid-nitrogen dewars with plantlet vials).

## Character / object sheet (keep identical across all agents)
- **Farmer (recurring)**: adult, medium-brown skin, short black hair, simple dot eyes, straw hat, olive shirt, khaki trousers, rubber boots; calm and dignified; cute proportions via `tools/body.py` (kind='cute').
- **Scientist (recurring)**: adult, light-tan skin, dark ponytail, dot eyes, white lab coat, blue gloves; cute proportions.
- **Shopper / reader at the counter (recurring)**: adult, dark skin, short curly hair, dot eyes, warm yellow sweater, jeans.
- **William Cavendish / O. Henry / real people**: never drawn as portraits; show a glasshouse, a book, a hat on a chair.
- Colours: bananas ripe yellow `#e8c547` with soft green tips, green unripe `#8fb55a`, leaves deep green; the rest from `pal`. Keep 'Cavendish' and 'Gros Michel' the same curved shape; Gros Michel slightly thicker skin.
- Plants, fruit, fungus, atoms, containers are NOT fixed: draw the view that fits THIS unit (cutaway, close-up, diagram, wide landscape).

## Care points
- No text or numbers anywhere in the SVG (sidecar `labels` only). Chromosome diagrams = coloured rods; radiation = soft particle dots, no trefoil symbol with text.
- Fungus and disease: cutaway of roots, wilted leaves, never gore.
- History scenes (banana republics, strike): symbols only — a train on a plantation rail, a crate stack, an empty chair; no weapons aimed at anyone, no real persons.
- Nothing about brand logos (no company marks on crates).
