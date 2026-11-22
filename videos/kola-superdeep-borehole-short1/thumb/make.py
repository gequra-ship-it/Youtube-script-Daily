# Shorts thumbnail A for kola-superdeep-borehole-short1 (style B, guideline 16-9). Run: python3 videos/kola-superdeep-borehole-short1/thumb/make.py
# Hook  IT SHOULD BE / BONE-DRY  -- script S01 "Scientists expected rock at that depth to be bone-dry."
# Scene: a split granite block deep underground; glowing water beads out of quartz crystals in its crack and runs down the fractures
#        (S02 "liquid water came flooding out through fractured stone", S04 "water squeezed directly out of mineral crystals").
#        Hard-hat frog (headlamp) bottom-left, a drip-fed pool bottom-right.
import os, sys, math, random
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from kshort_common import *

r = random.Random(21)
defs = FILTERS + vig()
defs += lin('cave', [(0, '#05080f'), (.5, '#0b1522'), (1, '#04070c')])
defs += halo('hal', 540, 500, 560, inner='#e8fbff', outer='#4fd2ff')
defs += lin('face', [(0, '#8d7f80'), (.6, '#5d5355'), (1, '#2c2628')])
defs += lin('topf', [(0, '#c9bab4'), (1, '#94878a')])
defs += lina('qz', [(0, '#ffffff', .95), (.45, '#bff0ff', .75), (1, '#4fb8e8', .55)], x2=1, y2=0)
defs += rad('pool', 820, 1700, 260, [(0, '#bff4ff', .8), (.5, '#4fd2ff', .35), (1, '#4fd2ff', 0)])
b = f'<rect width="{W}" height="{H}" fill="url(#cave)"/>'
# cave walls: dark rock masses at the sides
b += f'<path d="M0 0 H260 Q200 400 120 700 T60 1300 L0 1400z" fill="#0f1620"/><path d="M1080 0 H840 Q900 380 980 640 T1040 1320 L1080 1380z" fill="#0f1620"/>'
b += crystals(r, 160, 0, 0, W, H, ['#2a3a4c', '#1a2634', '#3a4a5c'], 6, 18, .2, .5, skip=lambda x, y: 180 < x < 900 and 180 < y < 1300)
b += f'<ellipse cx="540" cy="520" rx="620" ry="560" fill="url(#hal)"/>'
# ---- granite block (3D: top face + front face), split by a glowing crack ----
top = [(150, 330), (420, 240), (930, 290), (960, 360), (700, 420), (170, 400)]
front = [(170, 400), (700, 420), (960, 360), (950, 760), (700, 830), (160, 790)]
b += f'<ellipse cx="560" cy="830" rx="460" ry="40" fill="#000" opacity=".5" filter="url(#b12)"/>'
b += f'<polygon points="{P(front)}" fill="url(#face)" stroke="#120e10" stroke-width="6" stroke-linejoin="round"/>'
b += f'<polygon points="{P(top)}" fill="url(#topf)" stroke="#120e10" stroke-width="6" stroke-linejoin="round"/>'
b += f'<path d="M700 420 L700 830" stroke="#120e10" stroke-width="5"/>'
b += f'<path d="M700 424 L950 364 L948 760 L700 826z" fill="#000" opacity=".22"/>'
# granite speckle (feldspar pink, quartz white, biotite black)
inside = lambda pts: (lambda x, y: not _pip(x, y, pts))
def _pip(x, y, pts):
    c = False; j = len(pts) - 1
    for i in range(len(pts)):
        (xi, yi), (xj, yj) = pts[i], pts[j]
        if (yi > y) != (yj > y) and x < (xj - xi) * (y - yi) / (yj - yi) + xi: c = not c
        j = i
    return c
b += crystals(r, 900, 150, 230, 970, 840, ['#e9d6cc', '#f4f0ec', '#1e1a1c', '#c9968a', '#2e2a2e'], 4, 14, .35, .85, skip=lambda x, y: not (_pip(x, y, front) or _pip(x, y, top)))
# edge highlights from the glow
b += f'<path d="M170 400 L700 420 L960 360" fill="none" stroke="#dff8ff" stroke-width="5" opacity=".75"/>'
b += f'<path d="M150 330 L420 240 L930 290" fill="none" stroke="#f0fbff" stroke-width="4" opacity=".7"/>'
# fractures with water (cyan glow)
cracks = [jag((560, 252), (520, 410), 6, 14, 1), jag((520, 410), (470, 600), 8, 18, 2), jag((470, 600), (430, 800), 8, 16, 3),
          jag((520, 410), (300, 540), 7, 16, 4), jag((470, 600), (700, 660), 7, 14, 5), jag((700, 660), (900, 560), 6, 14, 6),
          jag((300, 540), (175, 520), 4, 10, 7), jag((470, 600), (250, 720), 6, 14, 8), jag((780, 300), (700, 420), 4, 10, 9)]
for c in cracks:
    b += f'<polyline points="{P(c)}" fill="none" stroke="#4fd2ff" stroke-width="30" opacity=".5" filter="url(#b8)"/>'
    b += f'<polyline points="{P(c)}" fill="none" stroke="#06080e" stroke-width="11" stroke-linejoin="round"/>'
    b += f'<polyline points="{P(c)}" fill="none" stroke="#7fe6ff" stroke-width="5" stroke-linejoin="round"/>'
    b += f'<polyline points="{P(c)}" fill="none" stroke="#ffffff" stroke-width="1.8" opacity=".9"/>'
    for (x, y) in c[1:-1:2]:   # beads of water along the crack
        b += f'<circle cx="{x + 6:.0f}" cy="{y:.0f}" r="6" fill="#dff8ff" stroke="#1a6a8a" stroke-width="2"/><circle cx="{x + 4:.0f}" cy="{y - 2:.0f}" r="2" fill="#fff"/>'
# ---- quartz crystal cluster bursting out of the main crack, sweating water ----
def prism(x, y, w, h, rot):
    g = f'<g transform="translate({x} {y}) rotate({rot})">'
    g += f'<path d="M{-w} 0 V{-h} L0 {-h - w * 1.4:.0f} L{w} {-h} V0z" fill="url(#qz)" stroke="#0c3a52" stroke-width="4" stroke-linejoin="round"/>'
    g += f'<path d="M0 0 V{-h} L0 {-h - w * 1.4:.0f}" fill="none" stroke="#0c3a52" stroke-width="2.4" opacity=".7"/>'
    g += f'<path d="M{-w} {-h} L0 {-h + w * .5:.0f} L{w} {-h}" fill="none" stroke="#0c3a52" stroke-width="2.4" opacity=".6"/>'
    g += f'<path d="M{-w * .6:.0f} -10 V{-h + 6}" stroke="#ffffff" stroke-width="5" opacity=".85" stroke-linecap="round"/>'
    for k in range(3):
        dy = -h * (.25 + .25 * k)
        g += f'<path d="M{w * .4:.0f} {dy - 10:.0f} q7 10 0 16 q-7 -6 0 -16z" fill="#e8fbff" stroke="#1a6a8a" stroke-width="2"/>'
    return g + '</g>'
CX, CY = 520, 470
b += f'<ellipse cx="{CX}" cy="{CY - 60}" rx="220" ry="200" fill="#bff4ff" opacity=".35" filter="url(#b26)"/>'
for x, y, w, h, rot in ((CX - 70, CY + 20, 26, 120, -28), (CX + 80, CY + 20, 24, 110, 30), (CX - 20, CY + 10, 34, 190, -8),
                        (CX + 30, CY + 30, 30, 150, 12), (CX - 120, CY + 40, 18, 70, -48), (CX + 130, CY + 44, 18, 66, 50)):
    b += prism(x, y, w, h, rot)
# water spilling from the crystal root down the face, dripping off the bottom edge
spill = f'M{CX - 10} {CY + 30} q-30 60 -20 120 q8 50 -30 110 q-20 40 -26 84'
b += f'<path d="{spill}" fill="none" stroke="#4fd2ff" stroke-width="30" opacity=".35" filter="url(#b8)"/>'
b += f'<path d="{spill}" fill="none" stroke="#bff4ff" stroke-width="12" stroke-linecap="round"/><path d="{spill}" fill="none" stroke="#ffffff" stroke-width="4" stroke-linecap="round"/>'
for dx, dy, s in ((428, 820, 1.1),):
    b += f'<path transform="translate({dx} {dy}) scale({s})" d="M0 -14 q11 16 0 24 q-11 -8 0 -24z" fill="#dff8ff" stroke="#1a6a8a" stroke-width="2.4"/>'
b += sparkles([(CX - 10, CY - 260, 26), (CX + 190, CY - 150, 18), (CX - 210, CY - 120, 20), (CX + 300, CY + 90, 16), (CX - 330, CY + 200, 14)], '#f0fcff')
b += fireflies(46, 120, 1850, col='#9fe8ff', core='#e8fbff', seed=5)
# ---- lower cave: pool fed by drips from a crack in the ceiling-right; frog bottom-left ----
b += f'<path d="M0 1560 Q300 1500 560 1540 T1080 1520 V1920 H0z" fill="#0a1018"/>'
b += f'<ellipse cx="820" cy="1700" rx="300" ry="120" fill="url(#pool)"/>'
b += f'<ellipse cx="820" cy="1690" rx="210" ry="46" fill="#0e3a52" stroke="#9fe8ff" stroke-width="4"/>'
for k, rr in enumerate((40, 90, 150)):
    b += f'<ellipse cx="830" cy="1690" rx="{rr}" ry="{rr * .2:.0f}" fill="none" stroke="#dff8ff" stroke-width="3" opacity="{.8 - k * .22:.2f}"/>'
b += f'<path d="M1080 1290 L1080 1420 Q1000 1400 940 1420 L880 1400 L850 1420 L820 1380 Q900 1330 1080 1290z" fill="#152030" stroke="#060a10" stroke-width="5"/>'
b += f'<path d="M830 1384 Q900 1338 1080 1300" fill="none" stroke="#7fe6ff" stroke-width="3" opacity=".5"/>'
b += f'<path d="M870 1400 q-10 80 -40 0" fill="#bff4ff" opacity=".0"/>'
for y in (1450, 1560):
    b += f'<path transform="translate(845 {y})" d="M0 -14 q11 16 0 24 q-11 -8 0 -24z" fill="#dff8ff" stroke="#1a6a8a" stroke-width="2.4"/>'
b += crystals(r, 60, 0, 1560, W, 1900, ['#2a3a4c', '#1a2634'], 6, 16, .3, .6)
b += darkband(860, 1240, .45)
# frog: hard hat with a lit headlamp, overalls, holding up a little glass of the deep water
FX, FY, FS = 270, 1770, 3.3
b += f'<ellipse cx="{FX}" cy="{FY + 10}" rx="110" ry="16" fill="#000" opacity=".4"/>'
b += f'<ellipse cx="{FX}" cy="{FY - 200}" rx="230" ry="220" fill="#9fe8ff" opacity=".12" filter="url(#b24)"/>'
glass = ('<g transform="translate(66 -10)"><path d="M-12 -30 l3 34 h18 l3 -34z" fill="#bff4ff" fill-opacity=".55" stroke-width="2.6"/>'
         '<path d="M-10 -18 l2 22 h16 l2 -22z" fill="#4fd2ff" opacity=".8" stroke="none"/><path d="M-7 -26 v20" stroke="#fff" stroke-width="2"/></g>')
b += frog(FX, FY, FS, look=(4, -6), mouth='O', mid=OVERALLS, top=hardhat(), sleeve=GREEN,
          armR='M38 -22 q16 2 20 2', armL='M-34 -22 q-14 6 -16 22', front=glass)
b += f'<rect width="{W}" height="{H}" fill="url(#vig)"/>'
write(HERE, '#05080f', defs, b, [('IT SHOULD BE', 124, 'w'), ('BONE-DRY', 200, 'y')], outline='#04101a', top=880)
