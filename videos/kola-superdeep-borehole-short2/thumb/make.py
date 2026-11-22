# Shorts thumbnail A for kola-superdeep-borehole-short2 (style B, guideline 16-9). Run: python3 videos/kola-superdeep-borehole-short2/thumb/make.py
# Hook  THE HOLE / KEPT CLOSING  -- script S01 "the hole it left behind started closing on its own"; S03 "the surrounding rock tended to creep
#        inward and squeeze the borehole narrower".
# Scene: cross-section of the deep borehole; hot (glowing) granite bulges in like soft clay around the drill pipe, flow bands follow the bulge,
#        the drill bit glows at the bottom (S03 "behaved more like hot plastic or dense modeling clay"). Frog in a hard hat with a wrench
#        in a side pocket bottom-right.
import os, sys, math, random
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', 'kola-superdeep-borehole-short1', 'thumb'))
from kshort_common import *

r = random.Random(32)
defs = FILTERS + vig(a=.8)
defs += lin('rockA', [(0, '#1a1426'), (.35, '#2e1c2a'), (.6, '#4a2224'), (1, '#1a0e12')])
defs += rad('heat', 540, 640, 520, [(0, '#fff0c0', .95), (.2, '#ffb347', .75), (.55, '#ff6a1e', .3), (1, '#ff6a1e', 0)])
defs += halo('hal', 540, 560, 600, inner='#ffe9b0', outer='#ff9a3c')
defs += lin('pipe', [(0, '#3a3f4c'), (.35, '#c9d0dc'), (.55, '#f4f8ff'), (1, '#4a505e')], x2=1, y2=0)
defs += lin('hole', [(0, '#120a10'), (.7, '#3a1a12'), (1, '#ff9a3c')])
b = f'<rect width="{W}" height="{H}" fill="url(#rockA)"/>'
b += crystals(r, 700, 0, 0, W, H, ['#5a4a6a', '#7a5a5a', '#3a2a3a', '#9a6a5a'], 5, 16, .15, .45)
b += f'<ellipse cx="540" cy="560" rx="640" ry="640" fill="url(#hal)" opacity=".75"/>'
# clay-like flow bands that follow the bulging walls (offset copies of each wall edge, hot near the hole, cool outward)
LEFT = 'M410 -20 C400 200 420 330 480 420 C518 470 514 600 506 640 C490 700 470 740 470 790'
RIGHT = 'M670 -20 C680 200 660 330 600 420 C562 470 566 600 574 640 C590 700 610 740 610 790'
for k in range(1, 9):
    col = mix(['#ffd27a', '#ff7a2a', '#8a2a2a', '#3a2034'], k / 8)
    for side, path in ((-1, LEFT), (1, RIGHT)):
        sx = 1 + k * .06
        b += (f'<path d="{path}" transform="translate({540 + side * k * 46} 0) scale({sx:.2f} 1) translate(-540 0)" fill="none" stroke="{col}" '
              f'stroke-width="{max(3, 12 - k):.0f}" opacity="{.85 - k * .07:.2f}" stroke-linecap="round"/>')
b += f'<ellipse cx="540" cy="640" rx="560" ry="620" fill="url(#heat)" opacity=".55"/>'
# the borehole cavity: wide near the top, squeezed almost shut around the pipe, closing in under the bit
HOLE = ('M410 -20 C400 200 420 330 480 420 C518 470 514 600 506 640 C490 700 470 740 470 790 Q540 860 610 790 '
        'C610 740 590 700 580 640 C566 600 562 470 600 420 C660 330 680 200 670 -20 Z')
b += f'<path d="{HOLE}" fill="none" stroke="#ffb347" stroke-width="40" opacity=".55" filter="url(#b14)"/>'
b += f'<path d="{HOLE}" fill="url(#hole)" stroke="#1a0a08" stroke-width="7"/>'
b += f'<path d="{LEFT}" fill="none" stroke="#ffe2a0" stroke-width="6" opacity=".95"/><path d="{RIGHT}" fill="none" stroke="#ffe2a0" stroke-width="6" opacity=".95"/>'
# squeeze arrows: glowing chevrons pushing in from both sides at the pinch
for side in (-1, 1):
    for k, xo in enumerate((120, 200)):
        x = 540 + side * xo; d = -side * 34
        b += f'<path d="M{x - d:.0f} {470 + k * 0} L{x} 530 L{x - d:.0f} 590" fill="none" stroke="#1a0a08" stroke-width="20" stroke-linecap="round" stroke-linejoin="round"/>'
        b += f'<path d="M{x - d:.0f} 470 L{x} 530 L{x - d:.0f} 590" fill="none" stroke="#fff0c0" stroke-width="10" stroke-linecap="round" stroke-linejoin="round" opacity="{.95 - k * .3:.2f}"/>'
# drill pipe with tool joints, and the bit at the bottom
b += f'<rect x="514" y="-30" width="52" height="790" fill="url(#pipe)" stroke="#12141a" stroke-width="5"/>'
for y in (110, 330, 690):
    b += f'<rect x="506" y="{y}" width="68" height="40" rx="6" fill="url(#pipe)" stroke="#12141a" stroke-width="5"/>'
b += f'<path d="M548 -20 V750" stroke="#ffffff" stroke-width="5" opacity=".6"/>'
bit = ('<g transform="translate(540 760)" stroke="#12141a" stroke-width="5" stroke-linejoin="round">'
       '<path d="M-34 0 H34 L44 22 H-44z" fill="#8a909c"/>'
       '<circle cx="-24" cy="38" r="20" fill="#c99a3a"/><circle cx="24" cy="38" r="20" fill="#c99a3a"/><circle cx="0" cy="46" r="20" fill="#e0b050"/>'
       + ''.join(f'<path d="M{x} {y} l-5 9 h10z" fill="#fff0c0" stroke-width="2.4"/>' for x, y in ((-30, 50), (-16, 54), (0, 62), (16, 54), (30, 50), (-8, 30), (12, 30)))
       + '</g>')
b += f'<ellipse cx="540" cy="820" rx="120" ry="60" fill="#fff0c0" opacity=".6" filter="url(#b14)"/>' + bit
b += sparkles([(380, 260, 22), (700, 200, 18), (330, 700, 18), (760, 660, 22), (540, 150, 14)], '#fff4d0')
b += fireflies(44, 80, 1850, col='#ffcf7a', core='#fff3c8', seed=8)
b += darkband(860, 1240, .5)
# side pocket (bottom-right) where the frog stands
PX, PY = 790, 1650
b += f'<path d="M{PX - 240} {PY + 150} Q{PX - 250} {PY - 170} {PX} {PY - 190} Q{PX + 260} {PY - 170} {PX + 250} {PY + 150}z" fill="#120a10" stroke="#ffb347" stroke-width="5" opacity=".95"/>'
b += f'<path d="M{PX - 240} {PY + 150} H{PX + 250}" stroke="#ffcf7a" stroke-width="5"/>'
b += f'<ellipse cx="{PX}" cy="{PY - 60}" rx="200" ry="170" fill="#ff9a3c" opacity=".14" filter="url(#b24)"/>'
FX, FY, FS = PX, PY + 146, 3.0
COVER = OVERALLS.replace('#3c6fb4', '#e0742a').replace('#2e5a96', '#b85a1e')
wrench = ('<g transform="translate(-52 -22) rotate(-150)"><rect x="-6" y="-4" width="74" height="12" rx="5" fill="#9aa2b2" stroke-width="3"/>'
          '<path d="M66 -12 a18 18 0 1 1 0 28 l-4 -8 h12 v-12 h-12z" fill="#9aa2b2" stroke-width="3"/></g>')
sweat = ''.join(f'<path d="M{x} {y} q6 9 0 13 q-6 -4 0 -13z" fill="#bfe6ff" stroke-width="2"/>' for x, y in ((-40, -86), (50, -78)))
b += f'<ellipse cx="{FX}" cy="{FY + 4}" rx="100" ry="14" fill="#000" opacity=".4"/>'
b += frog(FX, FY, FS, look=(-5, -5), mouth='O', mid=COVER, top=hardhat(lamp=False) + sweat, sleeve=GREEN,
          armL='M-34 -22 q-16 0 -18 0', armR='M38 -22 q14 6 16 22', front=wrench, flip=False)
b += f'<rect width="{W}" height="{H}" fill="url(#vig)"/>'
write(HERE, '#1a1426', defs, b, [('THE HOLE', 150, 'w'), ('KEPT CLOSING', 138, 'y')], outline='#14060a', top=890)
