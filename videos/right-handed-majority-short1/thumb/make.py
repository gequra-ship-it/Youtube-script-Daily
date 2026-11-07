# STYLE B (guideline 16-9 B, 2026-11-07): dark scene + glowing concrete subject (magnifier on a scratched tooth) + one-line hook.
# Shorts thumbnail (VERTICAL 1080x1920, text centred) for right-handed-majority-short1 (guideline 16-9, brief tools/briefs/thumb_art.md 'Shorts thumbnails').
# OLDER THAN OUR SPECIES   intuitive: a cute Homo heidelbergensis grips a strip of hide in his teeth and slices it with a stone
#                          flake in his RIGHT hand; the frog archaeologist (pith helmet) holds a magnifier showing one front
#                          tooth with diagonal scratches top-left -> bottom-right (script: heidelbergensis teeth, over half a
#                          million years ago, "right-hand bias existed long before modern Homo sapiens", "far older than our own species").
# Differs from long C (cave hand stencils) and the other shorts. Helpers are shared with the long thumbnails' make.py.
import os, sys, math, random, importlib.util
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', '..', 'tools'))
_s = importlib.util.spec_from_file_location('rhm_thumb', os.path.join(HERE, '..', '..', 'right-handed-majority', 'thumb', 'make.py'))
L = importlib.util.module_from_spec(_s); _s.loader.exec_module(L)
from thumb_lib import vpage, vsvg, lin, rad, spark, fireflies, halo, darkband
from body import shoulders
LINE, BODY = L.LINE, L.BODY


def make():
    rnd = random.Random(5)
    d = L.FILTERS
    d += lin('sky1', [(0, '#0b0618'), (.5, '#1c0f34'), (.8, '#4a1a3a'), (1, '#7a2a30')])
    d += halo('sun1', 540, 470, 640, inner='#fff2c0', outer='#ffb040')
    d += '<filter id="b6" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="6"/></filter><filter id="b50" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="50"/></filter>'
    d += rad('glass1', 600, 700, 230, [(0, '#fff6d8', 1), (.75, '#f4dcae', 1), (1, '#d9b47a', 1)])
    d += rad('vig1', 540, 960, 1250, [(0, '#000', 0), (.6, '#000', 0), (1, '#000', .6)])
    d += '<clipPath id="lens1"><circle cx="600" cy="700" r="205"/></clipPath>'
    b = '<rect width="1080" height="1920" fill="url(#sky1)"/>'
    b += '<rect width="1080" height="1920" fill="url(#sun1)"/>'
    b += '<path d="M0 1700 Q200 1640 420 1670 T860 1650 T1080 1660 L1080 1920 L0 1920Z" fill="#1a0a1e"/>'
    b += fireflies(60, 120, 1850, seed=3)
    # ---------- magnifier with the scratched tooth (frog archaeologist) ----------
    b += '<g transform="translate(540 470) scale(1.42) translate(-600 -700)">'
    b += '<circle cx="600" cy="700" r="250" fill="#ffe7a8" opacity=".55" filter="url(#b32)"/>'
    b += f'<circle cx="600" cy="700" r="205" fill="url(#glass1)"/>'
    tooth = (f'<path d="M470 600 Q470 500 545 505 Q575 508 600 525 Q625 508 655 505 Q730 500 730 600 Q732 680 705 740 Q690 860 655 875 Q625 885 620 800 Q612 750 600 750 Q588 750 580 800 Q575 885 545 875 Q510 860 495 740 Q468 680 470 600Z" fill="#fbf4e2" stroke="{LINE}" stroke-width="10" stroke-linejoin="round"/>'
             f'<path d="M505 590 Q510 540 545 535" stroke="#fff" stroke-width="16" fill="none" opacity=".9" stroke-linecap="round"/>'
             f'<path d="M705 620 Q700 700 680 740" stroke="#d8c8a2" stroke-width="16" fill="none" opacity=".7" stroke-linecap="round"/>')
    for k in range(8):   # scratch marks sloping top-left -> bottom-right
        x0 = 490 + k * 22 + rnd.uniform(-5, 5); y0 = 545 + rnd.uniform(0, 50)
        L_ = rnd.uniform(80, 150)
        tooth += f'<path d="M{x0:.0f} {y0:.0f} l{L_ * .55:.0f} {L_ * .83:.0f}" stroke="#7a4a2a" stroke-width="{rnd.choice([4, 5, 6])}" stroke-linecap="round" opacity=".85"/>'
    b += f'<g clip-path="url(#lens1)">{tooth}</g>'
    b += '<circle cx="600" cy="700" r="205" fill="none" stroke="#c99a3a" stroke-width="26"/><circle cx="600" cy="700" r="205" fill="none" stroke="' + LINE + '" stroke-width="6"/>'
    b += '<circle cx="600" cy="700" r="218" fill="none" stroke="' + LINE + '" stroke-width="6"/>'
    b += '<path d="M470 560 A170 170 0 0 1 560 520" stroke="#fff" stroke-width="12" fill="none" opacity=".8" stroke-linecap="round"/>'
    b += f'<path d="M450 850 L360 930" stroke="{LINE}" stroke-width="44" stroke-linecap="round"/><path d="M450 850 L360 930" stroke="#6a3a1a" stroke-width="30" stroke-linecap="round"/>'
    b += '</g>'
    # frog archaeologist (pith helmet, khaki shirt) holding the magnifier
    helmet = ('<path d="M-30 -84 Q-26 -122 8 -124 Q42 -122 46 -84Z" fill="#e2cf9a" stroke-width="4"/>'
              '<path d="M-48 -83 Q8 -96 64 -83 Q8 -74 -48 -83Z" fill="#cdb27a" stroke-width="4"/><path d="M-26 -96 Q8 -103 42 -96" stroke="#8a6a3a" stroke-width="5" fill="none"/>')
    shirt = f'<g clip-path="url(#fbody)"><rect x="-50" y="-36" width="110" height="60" fill="#c9a86a" stroke-width="3"/><path d="M-4 -36 L8 -22 L20 -36" fill="#a8884a" stroke-width="2.6"/><rect x="18" y="-20" width="14" height="12" fill="#a8884a" stroke-width="2"/></g><path d="{BODY}" fill="none" stroke-width="4"/>'
    b += '<ellipse cx="230" cy="1600" rx="230" ry="200" fill="#ffd27a" opacity=".18" filter="url(#b32)"/>'
    b += L.frog(230, 1700, 2.6, look=(5, -6), mouth='O', armL='M-34 -24 q-14 -14 -20 -34', armR='M38 -22 q14 -14 20 -34', mid=shirt, top=helmet, shadow=False)
    b += spark(850, 200, 26) + spark(170, 250, 18) + spark(960, 560, 20, '#ffe8b0') + spark(110, 640, 14, '#ffe8b0')
    b += darkband(860, 1240, .45)
    b += '<rect width="1080" height="1920" fill="url(#vig1)"/>'
    lines = [('OLDER THAN', 150, 'w'), ('OUR SPECIES', 150, 'y')]
    return vpage('#0b0618', vsvg(d, b), lines, outline='#14081a', top=905)


if __name__ == '__main__':
    open(os.path.join(HERE, 'A.html'), 'w').write(make()); print('ok')
