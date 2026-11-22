# Shorts thumbnail A for kola-superdeep-borehole-short4 (style B, guideline 16-9). Run: python3 videos/kola-superdeep-borehole-short4/thumb/make.py
# Hook  MUD FULL OF / GAS  -- script S02 "The drilling mud that returned to the surface was described as boiling, because it was so full of gas."
# Scene: Arctic night, aurora; thick gray drilling mud foams out of a steel wellhead and pours down onto the snow, full of glowing gas bubbles
#        (S01 "Thick gray mud surged out of the deep borehole, bubbling like a boiling cauldron ... on the Arctic platform").
#        Parka frog bottom-left in the snow, hands up in surprise.
import os, sys, math, random
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', 'kola-superdeep-borehole-short1', 'thumb'))
from kshort_common import *

r = random.Random(54)
G = 760   # snow line around the wellhead
defs = FILTERS + vig(a=.8)
defs += lin('sky', [(0, '#030817'), (.55, '#0b2142'), (1, '#1d3e66')])
defs += lina('aur', [(0, '#5cf2b0', 0), (.5, '#5cf2b0', .6), (1, '#2fb6a0', 0)])
defs += halo('hal', 540, 380, 520, inner='#fff8e0', outer='#9fe8ff')
defs += lin('snow', [(0, '#c9d8ee'), (.12, '#7088aa'), (.4, '#2e4262'), (1, '#0e1a2e')])
defs += lin('steel', [(0, '#3a404c'), (.4, '#b9c2d0'), (.6, '#e8eef6'), (1, '#4a505e')], x2=1, y2=0)
defs += lin('mud', [(0, '#d6d2ca'), (.45, '#8e8880'), (1, '#4e4a46')])
b = f'<rect width="{W}" height="{H}" fill="url(#sky)"/>'
b += stars(r, 130, 0, 560)
b += aurora(((-120, 70, .55), (240, 90, .7), (600, 60, .55), (860, 80, .45)), y=90, h=320)
b += f'<ellipse cx="540" cy="400" rx="600" ry="560" fill="url(#hal)" opacity=".7"/>'
# distant tundra hills + ruined buildings
b += f'<path d="M0 620 Q200 560 420 600 T820 590 T1080 600 V700 H0z" fill="#2c4466"/>'
b += f'<path d="M60 600 v-90 l50 -10 v100z M130 600 v-60 h70 v60z" fill="#1a2a44"/>'
b += f'<path d="M880 600 l24 -170 l24 170 M888 540 h32 M896 480 h16 M888 540 l30 -50 M920 540 l-30 -50" fill="none" stroke="#1a2a44" stroke-width="6"/>'
b += f'<path d="M0 660 Q300 630 560 650 T1080 640 V{H} H0z" fill="url(#snow)"/>'
# ---- the wellhead (steel spool + flanges + valve wheel) ----
WX = 540
b += f'<ellipse cx="{WX}" cy="{G + 10}" rx="300" ry="50" fill="#000" opacity=".35" filter="url(#b8)"/>'
b += f'<rect x="{WX - 46}" y="430" width="92" height="{G - 430}" fill="url(#steel)" stroke="#12141a" stroke-width="5"/>'
for y, w in ((G - 40, 150), (600, 130), (470, 140)):
    b += f'<rect x="{WX - w / 2:.0f}" y="{y}" width="{w}" height="28" rx="5" fill="url(#steel)" stroke="#12141a" stroke-width="5"/>'
    for k in range(5):
        bx = WX - w / 2 + 14 + k * (w - 28) / 4
        b += f'<circle cx="{bx:.0f}" cy="{y + 14}" r="5" fill="#5a606c" stroke="#12141a" stroke-width="2"/>'
# side valve with a red hand wheel
b += f'<rect x="{WX + 46}" y="640" width="90" height="40" fill="url(#steel)" stroke="#12141a" stroke-width="5"/>'
b += f'<ellipse cx="{WX + 150}" cy="660" rx="16" ry="54" fill="none" stroke="#12141a" stroke-width="16"/><ellipse cx="{WX + 150}" cy="660" rx="16" ry="54" fill="none" stroke="#d2452e" stroke-width="9"/>'
b += f'<path d="M{WX + 150} 610 V710" stroke="#d2452e" stroke-width="6"/>'
b += f'<path d="M{WX - 20} 440 V{G - 10}" stroke="#ffffff" stroke-width="6" opacity=".55"/>'
# ---- the mud: a foaming dome on top, sheets pouring down both sides, puddle on the snow ----
DOME = f'M{WX - 70} 440 C{WX - 120} 400 {WX - 130} 320 {WX - 70} 300 C{WX - 60} 240 {WX + 20} 230 {WX + 40} 270 C{WX + 100} 250 {WX + 140} 320 {WX + 100} 360 C{WX + 130} 400 {WX + 90} 450 {WX + 70} 440 Z'
b += f'<path d="{DOME}" fill="#fff8e0" opacity=".45" filter="url(#b26)"/>'
pours = [f'M{WX - 70} 420 C{WX - 110} 470 {WX - 70} 560 {WX - 96} 640 C{WX - 110} 700 {WX - 80} 730 {WX - 60} {G} L{WX - 30} {G} C{WX - 40} 700 {WX - 56} 640 {WX - 40} 560 C{WX - 30} 500 {WX - 40} 460 {WX - 20} 430 Z',
         f'M{WX + 60} 420 C{WX + 100} 480 {WX + 64} 540 {WX + 84} 600 C{WX + 96} 640 {WX + 70} 700 {WX + 56} {G} L{WX + 26} {G} C{WX + 36} 700 {WX + 50} 640 {WX + 40} 590 C{WX + 30} 520 {WX + 46} 470 {WX + 20} 430 Z']
for d in pours:
    b += f'<path d="{d}" fill="url(#mud)" stroke="#2a2b30" stroke-width="5"/>'
PUD = f'M{WX - 250} {G + 10} C{WX - 260} {G - 30} {WX - 120} {G - 40} {WX} {G - 30} C{WX + 140} {G - 40} {WX + 270} {G - 30} {WX + 250} {G + 10} C{WX + 200} {G + 50} {WX - 200} {G + 50} {WX - 250} {G + 10} Z'
b += f'<path d="{PUD}" fill="url(#mud)" stroke="#2a2b30" stroke-width="5"/>'
b += f'<path d="{DOME}" fill="url(#mud)" stroke="#2a2b30" stroke-width="6"/>'
b += f'<path d="M{WX - 90} 310 C{WX - 60} 260 {WX + 10} 250 {WX + 40} 280" fill="none" stroke="#ffffff" stroke-width="7" opacity=".7" stroke-linecap="round"/>'
# gas bubbles: glowing rings in the mud and popping above it
def bub(x, y, s, glow=True):
    o = f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{s * 2.2:.0f}" fill="#bff4ff" opacity=".35" filter="url(#b4)"/>' if glow else ''
    return o + (f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{s:.0f}" fill="#e8f6ff" fill-opacity=".25" stroke="#ffffff" stroke-width="3"/>'
                f'<circle cx="{x - s * .35:.0f}" cy="{y - s * .35:.0f}" r="{max(2, s * .22):.0f}" fill="#fff"/>')
for x, y, s in ((WX - 60, 330, 16), (WX - 10, 300, 22), (WX + 50, 320, 14), (WX + 80, 380, 18), (WX - 90, 400, 12), (WX + 10, 380, 26),
                (WX - 40, 420, 10), (WX + 40, 420, 12), (WX - 80, 520, 10), (WX + 70, 560, 9), (WX - 70, 660, 9), (WX + 66, 690, 10),
                (WX - 180, G - 10, 12), (WX + 170, G - 6, 14), (WX - 90, G + 10, 10), (WX + 90, G + 14, 9), (WX + 220, G, 8)):
    b += bub(x, y, s)
for x, y, s in ((WX - 30, 220, 10), (WX + 60, 200, 8), (WX - 90, 250, 7), (WX + 20, 160, 6), (WX + 110, 280, 9), (WX - 130, 330, 6)):
    b += bub(x, y, s)
rf = random.Random(3)
for _ in range(70):
    a = rf.uniform(0, 2 * math.pi); x = WX + 15 + 110 * math.cos(a) * rf.uniform(.6, 1.05); y = 345 + 100 * math.sin(a) * rf.uniform(.6, 1.05)
    b += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{rf.uniform(3, 8):.1f}" fill="#f4f0ea" fill-opacity=".5" stroke="#ffffff" stroke-width="1.6"/>'
for _ in range(40):
    x = WX + rf.choice([-1, 1]) * rf.uniform(30, 95); y = rf.uniform(460, G)
    b += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{rf.uniform(2.5, 6):.1f}" fill="#f4f0ea" fill-opacity=".4" stroke="#ffffff" stroke-width="1.4"/>'
for x, d in ((WX - 200, -1), (WX + 200, 1), (WX - 120, -1), (WX + 130, 1)):
    b += f'<path d="M{x} {G - 6} q{d * 14} -30 {d * 30} -26 M{x} {G - 6} q{d * 2} -36 {d * 10} -44" fill="none" stroke="#d6d2ca" stroke-width="6" stroke-linecap="round"/>'
# steam
for k, (x, y) in enumerate(((WX - 40, 200), (WX + 50, 150), (WX - 10, 100))):
    b += f'<path d="M{x} {y} q-30 -40 0 -80 q30 -40 0 -80" fill="none" stroke="#e8f0ff" stroke-width="{26 - k * 6}" opacity=".18" filter="url(#b8)" stroke-linecap="round"/>'
b += sparkles([(WX - 230, 300, 22), (WX + 240, 250, 18), (WX + 280, 480, 16), (WX - 260, 560, 14), (WX + 10, 120, 14)], '#fffbe8')
b += fireflies(40, 120, 1850, col='#dff4ff', core='#ffffff', seed=21)
# snow drifts in the lower half + footprints
b += f'<path d="M0 1500 Q260 1440 540 1480 T1080 1460 V{H} H0z" fill="#3a5274" opacity=".45"/>'
b += f'<ellipse cx="{WX}" cy="{G + 10}" rx="420" ry="110" fill="#fff8e0" opacity=".25" filter="url(#b26)"/>'
for k in range(6):
    b += f'<ellipse cx="{620 + k * 60}" cy="{1560 + (k % 2) * 30}" rx="16" ry="8" fill="#3a5070" opacity=".4"/>'
b += darkband(860, 1240, .5)
# frog in parka + ushanka (bottom-left), hands up in surprise
FX, FY, FS = 290, 1740, 3.3
b += f'<ellipse cx="{FX}" cy="{FY - 200}" rx="230" ry="220" fill="#dff4ff" opacity=".1" filter="url(#b24)"/>'
b += f'<ellipse cx="{FX}" cy="{FY + 8}" rx="110" ry="14" fill="#1a2a44" opacity=".5"/>'
b += frog(FX, FY, FS, look=(5, -6), mouth='O', back=FLAPS, mid=PARKA, top=USHANKA, sleeve='#d2452e',
          armL='M-34 -24 q-22 -6 -24 -32', armR='M38 -24 q22 -6 24 -32')
b += f'<rect width="{W}" height="{H}" fill="url(#vig)"/>'
write(HERE, '#030817', defs, b, [('MUD FULL OF', 140, 'w'), ('GAS', 250, 'y')], outline='#04101c', top=870)
