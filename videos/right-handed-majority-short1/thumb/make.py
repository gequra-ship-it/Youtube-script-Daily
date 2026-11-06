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
from thumb_lib import vpage, vsvg, lin, rad, spark
from body import shoulders
LINE, BODY = L.LINE, L.BODY


def make():
    rnd = random.Random(5)
    d = L.FILTERS
    d += lin('sky1', [(0, '#24163a'), (.45, '#7a2f45'), (.75, '#d8693a'), (1, '#f2b25a')])
    d += rad('sun1', 540, 1330, 620, [(0, '#fff2c0', .95), (.25, '#ffc46a', .6), (1, '#ff8a3a', 0)])
    d += rad('glass1', 600, 700, 230, [(0, '#fff6d8', 1), (.75, '#f4dcae', 1), (1, '#d9b47a', 1)])
    d += rad('vig1', 540, 960, 1250, [(0, '#000', 0), (.6, '#000', 0), (1, '#000', .6)])
    d += '<clipPath id="lens1"><circle cx="600" cy="700" r="205"/></clipPath>'
    b = '<rect width="1080" height="1920" fill="url(#sky1)"/>'
    b += '<rect width="1080" height="1920" fill="url(#sun1)"/>'
    b += '<circle cx="540" cy="1360" r="200" fill="#ffe8a8" opacity=".9" filter="url(#b8)"/>'
    b += '<path d="M0 1500 Q200 1430 420 1470 T860 1450 T1080 1460 L1080 1920 L0 1920Z" fill="#6a2c3a" opacity=".8"/>'
    for x, s_ in ((90, 1), (980, 1.2), (850, .7)):
        b += (f'<g transform="translate({x} 1470) scale({s_})"><path d="M-4 0 L-2 -60 L2 -60 L4 0Z" fill="#3a1626"/>'
              f'<ellipse cx="0" cy="-66" rx="70" ry="16" fill="#3a1626"/><ellipse cx="-30" cy="-58" rx="30" ry="10" fill="#3a1626"/></g>')
    b += '<path d="M0 1600 Q500 1560 1080 1590 L1080 1920 L0 1920Z" fill="#3a1a1e"/>'
    b += '<g transform="translate(-790 900)">'
    # ---------- the big ancestor ----------
    CX, TOP, H = 1290, 230, 250
    SK = '#b98058'; FUR = '#8a5a2e'
    (lx, ly), (rx, ry) = shoulders(CX, TOP, H, 'cute')
    mx, my = CX, TOP + .5 * H + .3 * H
    # hide strip from the teeth down to his left hand (viewer right)
    strip = (f'<path d="M{mx - 40} {my - 6} Q{mx + 120} {my - 10} {mx + 220} {my + 90} L{mx + 255} {my + 170} L{mx + 205} {my + 182} '
             f'Q{mx + 160} {my + 70} {mx - 30} {my + 22}Z" fill="#9a4a2e" stroke="{LINE}" stroke-width="7" stroke-linejoin="round"/>'
             f'<path d="M{mx - 20} {my + 4} Q{mx + 120} {my + 6} {mx + 205} {my + 100}" fill="none" stroke="#d27a5a" stroke-width="10" opacity=".8"/>'
             + ''.join(f'<path d="M{mx + 40 + k * 34} {my - 4 + k * 10} l6 -14" stroke="#5a2a14" stroke-width="5" stroke-linecap="round"/>' for k in range(5)))
    # brow ridge, broad nose, clenched teeth over the hide
    brow = f'<path d="M{CX - .5 * H} {TOP + .36 * H} Q{CX} {TOP + .2 * H} {CX + .5 * H} {TOP + .36 * H} L{CX + .48 * H} {TOP + .41 * H} Q{CX} {TOP + .29 * H} {CX - .48 * H} {TOP + .41 * H}Z" fill="#8a5636" stroke="{LINE}" stroke-width="7" stroke-linejoin="round"/>'
    nose = f'<ellipse cx="{CX}" cy="{TOP + .66 * H}" rx="{.16 * H}" ry="{.09 * H}" fill="#a86c48" stroke="{LINE}" stroke-width="6"/>'
    teeth = (f'<rect x="{mx - 46}" y="{my - 22}" width="92" height="44" rx="16" fill="#5a1a14" stroke="{LINE}" stroke-width="7"/>'
             f'<rect x="{mx - 40}" y="{my - 18}" width="80" height="16" rx="4" fill="#fbf4e0"/>'
             f'<rect x="{mx - 40}" y="{my + 4}" width="80" height="14" rx="4" fill="#fbf4e0"/>'
             + ''.join(f'<line x1="{mx - 40 + k * 16}" y1="{my - 18}" x2="{mx - 40 + k * 16}" y2="{my + 18}" stroke="#c9b89a" stroke-width="3"/>' for k in range(1, 5)))
    beard = f'<path d="M{CX - .48 * H} {TOP + .62 * H} Q{CX - .5 * H} {TOP + 1.25 * H} {CX} {TOP + 1.3 * H} Q{CX + .5 * H} {TOP + 1.25 * H} {CX + .48 * H} {TOP + .62 * H} Q{CX + .3 * H} {TOP + 1.0 * H} {CX} {TOP + 1.0 * H} Q{CX - .3 * H} {TOP + 1.0 * H} {CX - .48 * H} {TOP + .62 * H}Z" fill="#3a2414" stroke="{LINE}" stroke-width="7"/>'
    # fur pelt over one shoulder
    hem = ' '.join(f'L{CX + .95 * H - k * .19 * H:.0f} {TOP + (2.75 if k % 2 else 2.95) * H:.0f}' for k in range(11))
    pelt = (f'<path d="M{CX - .35 * H} {TOP + 1.12 * H} Q{CX - .95 * H} {TOP + 1.25 * H} {CX - 1.0 * H} {TOP + 2.0 * H} L{CX - .98 * H} {TOP + 2.9 * H} '
            f'L{CX + .98 * H} {TOP + 2.9 * H} L{CX + 1.0 * H} {TOP + 2.0 * H} Q{CX + .95 * H} {TOP + 1.25 * H} {CX + .35 * H} {TOP + 1.12 * H}Z" fill="#9a6838" stroke="{LINE}" stroke-width="7" stroke-linejoin="round"/>'
            f'<path d="M{CX + .7 * H} {TOP + 1.4 * H} Q{CX + .9 * H} {TOP + 1.9 * H} {CX + .85 * H} {TOP + 2.6 * H}" stroke="#ffd27a" stroke-width="10" fill="none" opacity=".6" stroke-linecap="round"/>'
            + ''.join(f'<ellipse cx="{CX + rnd.uniform(-.8, .8) * H:.0f}" cy="{TOP + rnd.uniform(1.45, 2.6) * H:.0f}" rx="14" ry="9" fill="#5a3418"/>' for _ in range(14)))
    # right hand (viewer left) with a stone flake slicing at the hide by the mouth; left hand (viewer right) holds the hide
    fx, fy = mx + 70, my + 110
    flake = (f'<path d="M{fx - 20} {fy + 10} L{fx + 60} {fy - 130} L{fx + 40} {fy - 20} Z" fill="#9aa0aa" stroke="{LINE}" stroke-width="7" stroke-linejoin="round"/>'
             f'<path d="M{fx - 10} {fy} L{fx + 50} {fy - 110}" stroke="#e8eef6" stroke-width="5" opacity=".9"/>')
    armR = L.limb_to((lx, ly), (fx - 10, fy + 20), H, 'cute', 1, 'h1r', SK, SK, 'short')
    armL = L.limb_to((rx, ry), (mx + 235, my + 185), H, 'cute', 1, 'h1l', SK, SK, 'short')
    slash = ''.join(f'<path d="M{mx + 150 + k * 30} {my - 40 + k * 8} l46 46" stroke="#fff6c8" stroke-width="7" stroke-linecap="round" opacity="{.9 - k * .25:.2f}"/>' for k in range(3))
    b += f'<ellipse cx="{CX}" cy="{TOP + 1.6 * H}" rx="360" ry="420" fill="#ffd28a" opacity=".35" filter="url(#b32)"/>'
    b += L.person(CX, TOP, H, 'cute', SK, ('spiky', '#3a2414'), FUR, FUR, '#2a1a10', look=(-1.2, .6), mouth='flat', brows='up', legs=False,
                  deco=pelt, rim=(1, '#ffd27a'),
                  props_front=beard + nose + brow + strip + teeth + armL + armR + flake + slash)
    b += (f'<path d="M700 1080 L760 960 Q1000 900 1120 905 Q1300 880 1480 910 Q1700 920 1800 990 L1900 1080Z" fill="#3a2018" stroke="{LINE}" stroke-width="8"/>'
          f'<path d="M1000 930 Q1200 900 1440 920" stroke="#ffb070" stroke-width="8" fill="none" opacity=".55" stroke-linecap="round"/>'
          f'<path d="M1060 990 l40 -20 M1300 1010 l50 -12 M1500 980 l30 -20" stroke="#24100c" stroke-width="6" stroke-linecap="round"/>')
    b += '</g>'
    b += '<path d="M-20 1920 L-10 1810 Q200 1770 520 1790 Q800 1770 1100 1800 L1100 1920Z" fill="#24100f"/>'
    # ---------- magnifier with the scratched tooth (frog archaeologist) ----------
    b += '<g transform="translate(420 400) scale(1.05) translate(-600 -700)">'
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
    b += '</g>'
    b += f'<path d="M612 548 L736 600" stroke="{LINE}" stroke-width="44" stroke-linecap="round"/><path d="M612 548 L736 600" stroke="#6a3a1a" stroke-width="30" stroke-linecap="round"/>'
    # frog archaeologist (pith helmet, khaki shirt) holding the magnifier
    helmet = ('<path d="M-30 -84 Q-26 -122 8 -124 Q42 -122 46 -84Z" fill="#e2cf9a" stroke-width="4"/>'
              '<path d="M-48 -83 Q8 -96 64 -83 Q8 -74 -48 -83Z" fill="#cdb27a" stroke-width="4"/><path d="M-26 -96 Q8 -103 42 -96" stroke="#8a6a3a" stroke-width="5" fill="none"/>')
    shirt = f'<g clip-path="url(#fbody)"><rect x="-50" y="-36" width="110" height="60" fill="#c9a86a" stroke-width="3"/><path d="M-4 -36 L8 -22 L20 -36" fill="#a8884a" stroke-width="2.6"/><rect x="18" y="-20" width="14" height="12" fill="#a8884a" stroke-width="2"/></g><path d="{BODY}" fill="none" stroke-width="4"/>'
    b += L.frog(880, 650, 2.2, look=(-5, -4), mouth='O', armL='M-34 -24 q-14 -4 -28 -2', armR='M38 -22 q14 6 16 22', mid=shirt, top=helmet, shadow=False)
    b += spark(700, 220, 24) + spark(150, 160, 16) + spark(960, 300, 18, '#ffe8b0') + spark(110, 560, 14, '#ffe8b0')
    b += '<rect width="1080" height="1920" fill="url(#vig1)"/>'
    lines = [('OLDER', 190, 'y'), ('THAN OUR', 115, 'w'), ('SPECIES', 115, 'w')]
    return vpage('#24163a', vsvg(d, b), lines, outline='#14081a', top=665)


if __name__ == '__main__':
    open(os.path.join(HERE, 'A.html'), 'w').write(make()); print('ok')
