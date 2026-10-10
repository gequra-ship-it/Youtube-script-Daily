# Vertical (Shorts) addendum to art_spec_v3.md — read art_spec_v3.md and art_spec_v2.md first; this file overrides sizes/positions

- Canvas: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1080 1920" width="1080" height="1920">` (portrait 9:16). NEW pictures only — do not reuse or crop any landscape picture.
- Centre object (the "centre rule") at (540, 860), diameter 150-230 px. "match" transition: keep that object at the same place/size as the previous unit's.
- Safe zones (YouTube Shorts overlays cover the top ~290 px, the bottom ~290 px and the right ~140 px; captions of this video sit at y ~1440-1560): keep ALL important content inside x 100..940, y 300..1400. Backgrounds/glows may fill the full canvas. "slide" transition: keep x 0..100 and 980..1080 empty of important content.
- Compose vertically: stack subjects top-to-bottom (e.g. object above, person/detail below the centre) instead of left/right.
- Sidecar focus [x, y, scale] uses this 1080x1920 coordinate space (scale 1.5-2.0). Everything else as in art_spec_v3.md.
- Previews: `SHOT_W=1080 SHOT_H=1920 python3 /home/claude/ht/tools/svgshot.py <dir> files...`
- Output dir: /home/claude/ht/videos/never-eat-human-meat-short/art3/ ; plan: /home/claude/ht/videos/never-eat-human-meat-short/plan.json
- Background modes in the plan (paper/night/dusk) and the `pal` colours as in v3 (never default to purple/orange). Same character/palette consistency inside a scene. Keep each svg under ~100 KB.
- Topic care: prions/kuru/cannibalism context — symbols and metaphors only, nothing graphic.
