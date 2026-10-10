# never-eat-human-meat-v4 — art brief (shared by all picture agents)

Read fully, in this order: `/home/claude/youtube-script-daily/tools/art_spec_v2.md`, `tools/art_spec_v3.md`, `tools/art_spec_v4_backdrop.md` (the backdrop variety rules apply to NEW pictures too: no concentric rings, no radiating lines/rays/sunbursts; every picture gets a backdrop that fits its own text; neighbouring units must not share a backdrop kind; at most 2 of every 12 units share a kind). Vertical Shorts agents also read `tools/art_spec_v3_vertical.md`.

Paths in those specs that mention `/home/claude/ht/videos/never-eat-human-meat-v3/` mean, for this video:
- plan: `/home/claude/youtube-script-daily/videos/<SLUG>/plan.json` (use the entries for YOUR uids; `bg`, `text`, `prev`, `nxt`, `transition_in`, `dur`)
- output: `/home/claude/youtube-script-daily/videos/<SLUG>/art3/<uid>.svg` and `<uid>.json`
- preview tool: `python3 /home/claude/youtube-script-daily/tools/svgshot.py <preview dir> f1.svg ...` (vertical: `SHOT_W=1080 SHOT_H=1920`)
- `<SLUG>` is given in your task (long video `never-eat-human-meat-v4`, Shorts `never-eat-human-meat-v4-short1` / `-short2`).
Write ONLY your own uids. Do not edit any other repo file. **Scratch work (generator scripts, previews) goes ONLY in your own folder** `/tmp/claude-0/-home-claude-youtube-script-daily/53bea993-48d4-5496-836b-a9dbb74ebe3e/scratchpad/<first uid>_<last uid>/` — other agents work in parallel; never write to a shared scratch file name.

## Topic
Kuru and prions: the Fore people of the Papua New Guinea highlands (1950s), a funeral custom that spread a fatal brain disease, misfolded proteins (prions) that survive cooking and fool the immune system, mad cow disease, scrapie and chronic wasting disease, ancient cut-marked bones (Gran Dolina, Gough's Cave skull cups), calorie counts, pollutants and the species barrier, disgust, the PRNP gene (codon 129, G127V), hospital safety rules.

## Character / object sheet (keep identical across all agents)
- **Fore people**: dignified, calm, varied ages; simple highland clothing (bark-cloth and woven skirts, string bags, feather or shell ornaments drawn simply), warm dark-brown skin tones `#6b4a32`/`#7c5639`, black hair; thatched round houses, gardens on steep green ridges, mist. Never caricature; no spears-and-skulls clichés. Mourning is shown with sorrowful gatherings, hands, bowls, smoke, a covered shape — never a body being eaten, never flesh or blood.
- **Patients**: shown with care: a person supported by family, an empty stool, a shaking hand drawn with tremor lines. No grotesque faces.
- **Researchers / doctors** (1950s-60s): generic figures, mostly from behind or as hands, khaki shirts, notebooks, microscopes, specimen jars with blank labels; never a recognisable real person (no portraits of Gajdusek, Prusiner, Zigas, Cole).
- **Prion**: normal protein PrP-C = soft teal coiled ribbon `#3fa7a0`; misfolded PrP-Sc = angular magenta/coral folded sheet `#d64b9a`/`#d9694a`; clumps = stacked angular shards. The brain = soft pink-grey `#c9a0b4` with a sponge texture of round holes (holes are scattered, NOT concentric rings).
- **Cattle / sheep / deer**: calm farm and forest animals; no sick-animal gore.
- **Ancient humans** (Gran Dolina, Gough's Cave): cave interior, stone tools, bones with small cut-mark ticks, a clean museum-style skull cup on a stand. Calm, archaeological.
- **Violence / death / cannibalism**: never depicted directly. Use symbols: a woven mat with an empty space, smoke, a covered bowl, footprints, a museum case. No blood, no wounds, no flesh.

## Notes
- No text inside pictures (no letters, numbers, labels).
- `focus` on 40-50 % of units; sfx on 35-45 % using ONLY the 25 library names in art_spec_v3.md (unpitched; vary — never the same name in two consecutive units).
- Motion groups: every visible person `mv-breathe-<name>` (plus nod/arm/hand where natural); fire `mv-flame-*`, smoke `mv-smoke-*`, prion clumps `mv-cells-*`; glowing centre `mv-glint-core`. Ids unique inside each file.
- Final answer: one line per uid: `uid | centre | backdrop kind | focus_word or - | sfx or -`, plus problems left.
