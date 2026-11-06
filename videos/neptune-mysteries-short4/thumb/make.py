# Shorts thumbnail A for neptune-mysteries-short4 (guideline 16-9; brief tools/briefs/thumb_art.md). Run: python3 videos/neptune-mysteries-short4/thumb/make.py
# A  DIAMOND / HAIL / INSIDE?   intuitive: deep inside Neptune's hot slushy mantle, diamonds sink like hail toward the glowing core; the frog in a diving
#                               helmet rides the biggest diamond down; small cut-away Neptune top-right marks where we are
#                               (S06, S11-S12: slush of water, ammonia, methane; "diamonds may be forming ... drift downward through the slush like heavy hail")
import os, math, random, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../../tools'))
from thumb_lib import blobs
HERE = os.path.dirname(os.path.abspath(__file__))
LONG = os.path.join(HERE, '../../neptune-mysteries/thumb/make.py')   # shared helpers (frog, neptune, diamond) from the long-form thumbs
_src = open(LONG).read(); _g = {'__file__': LONG}; exec(_src[:_src.index('def thumb_A')], _g); globals().update({k: v for k, v in _g.items() if not k.startswith('__') and k != 'HERE'})


def trail(x, y, s, L):
    # sinking trail above a diamond (wake + bubbles)
    o = f'<path d="M{x - s * .9:.0f} {y - s * .3:.0f} Q{x - s * .5:.0f} {y - L * .6:.0f} {x - s * .15:.0f} {y - L:.0f} L{x + s * .15:.0f} {y - L:.0f} Q{x + s * .5:.0f} {y - L * .6:.0f} {x + s * .9:.0f} {y - s * .3:.0f}Z" fill="#bff0ff" opacity=".16"/>'
    o += f'<path d="M{x - s * .45:.0f} {y - s * .5:.0f} L{x - s * .1:.0f} {y - L * .9:.0f} M{x + s * .45:.0f} {y - s * .5:.0f} L{x + s * .1:.0f} {y - L * .9:.0f}" stroke="#e6fbff" stroke-width="{max(2, s * .06):.1f}" stroke-linecap="round" opacity=".45"/>'
    for k in range(4):
        o += f'<circle cx="{x + random.uniform(-s * .5, s * .5):.0f}" cy="{y - s - random.uniform(0, L * .8):.0f}" r="{random.uniform(2, max(3, s * .1)):.1f}" fill="none" stroke="#e6fbff" stroke-width="2" opacity=".6"/>'
    return o


def make():
    random.seed(44)
    d = FILTERS + DIA
    d += lin('sea', [(0, '#05162e'), (.35, '#0a3550'), (.68, '#145a66'), (.86, '#6a5a3a'), (1, '#c8662a')])
    d += rad('core', 960, 1500, 900, [(0, '#fff2c0', 1), (.45, '#ffb04a', .9), (.62, '#ff7a2a', .55), (.8, '#c8462a', .15), (1, '#c8462a', 0)])
    d += rad('vig', 960, 540, 1150, [(0, '#000', 0), (.7, '#000', 0), (1, '#000', .55)])
    b = '<rect width="1920" height="1080" fill="url(#sea)"/>'
    b += '<rect width="1920" height="1080" fill="url(#core)"/>'
    # churning slush: soft swirls and blobs
    b += blobs(40, 0, 80, 1920, 900, '#5fb6c0', .05, .14, 60, 220)
    for _ in range(18):
        x, y = random.uniform(0, 1900), random.uniform(120, 860)
        b += f'<path d="M{x:.0f} {y:.0f} q60 -40 120 0 t120 0" fill="none" stroke="#8fd6dc" stroke-width="{random.uniform(3, 7):.0f}" opacity="{random.uniform(.1, .25):.2f}" stroke-linecap="round"/>'
    # heat shimmer rising from the core
    for k in range(9):
        x = 200 + k * 200
        b += f'<path d="M{x} 1080 q-20 -40 0 -80 t0 -80" fill="none" stroke="#ffd08a" stroke-width="5" stroke-linecap="round" opacity=".35"/>'
    # many small diamonds sinking (hail), with wakes
    hail = [(1040, 250, 26), (1560, 300, 34), (1780, 520, 22), (1450, 840, 30), (880, 760, 24), (640, 880, 18), (1000, 960, 16),
            (1700, 760, 40), (1600, 120, 18), (1860, 300, 14), (760, 640, 14), (300, 960, 22), (1120, 850, 20), (1320, 180, 16)]
    for x, y, s in hail:
        b += trail(x, y, s, s * 5)
        b += diamond(x, y, s, rot=random.uniform(-14, 14))
    # hero diamond with the frog riding it down
    HX, HY, HS = 1250, 610, 190
    b += f'<circle cx="{HX}" cy="{HY + 40}" r="{HS * 1.9:.0f}" fill="#bff0ff" opacity=".18" filter="url(#b50)"/>'
    b += trail(HX, HY, HS, 420)
    b += diamond(HX, HY, HS, rot=-6)
    b += f'<path d="M{HX - 60} {HY + 30} L{HX - 20} {HY + 120}" stroke="#ffffff" stroke-width="5" opacity=".5" stroke-linecap="round"/>'
    # warm under-light from the core on the diamond's lower facets
    b += f'<path d="M{HX - HS} {HY + 6} L{HX} {HY + HS * 1.05:.0f} L{HX + HS} {HY - 10}" fill="none" stroke="#ffb04a" stroke-width="6" opacity=".55" transform="rotate(-6 {HX} {HY})"/>'
    collar = ('<ellipse cx="6" cy="-4" rx="42" ry="9" fill="#c99b45" stroke-width="3"/>'
              '<circle cx="-26" cy="-4" r="3" fill="#7a5233" stroke="none"/><circle cx="6" cy="2" r="3" fill="#7a5233" stroke="none"/><circle cx="38" cy="-4" r="3" fill="#7a5233" stroke="none"/>'
              '<path d="M50 -60 q30 -20 30 -60" fill="none" stroke="#5a3b25" stroke-width="7"/>')
    b += frog(HX + 6, HY - 74, 2.3, la='q-22 4 -40 30', ra='q22 4 40 30', mouth='o', look=(-3, 3), helmet=True, front=collar, tilt=-6)
    # bubbles streaming up from the helmet hose
    for k in range(6):
        b += f'<circle cx="{HX + 170 + random.uniform(-14, 14):.0f}" cy="{HY - 330 - k * 46:.0f}" r="{6 + k * 2}" fill="#dff8ff" fill-opacity=".15" stroke="#e6fbff" stroke-width="3" opacity=".8"/>'
    # small cut-away Neptune, top-right: "you are here" in the mantle
    NX, NY, NR = 1730, 170, 110
    nd, nb = neptune(NX, NY, NR, 'mini', spot=False)
    d += nd
    b += nb
    a0, a1 = math.radians(20), math.radians(110)
    def wedge(r):
        return f'M{NX} {NY} L{NX + r * math.cos(a0):.1f} {NY + r * math.sin(a0):.1f} A{r} {r} 0 0 1 {NX + r * math.cos(a1):.1f} {NY + r * math.sin(a1):.1f}Z'
    b += f'<path d="{wedge(NR)}" fill="#1f4bc2" stroke="#e6fbff" stroke-width="3"/>'
    b += f'<path d="{wedge(NR * .82)}" fill="#1d7f8c"/>'
    b += f'<path d="{wedge(NR * .38)}" fill="#ffb04a"/>'
    for k in range(5):
        a = math.radians(35 + k * 15); r = NR * (.5 + .06 * (k % 3))
        b += diamond(NX + r * math.cos(a), NY + r * math.sin(a), 7, glow=False)
    b += f'<circle cx="{NX + NR * .62 * math.cos(math.radians(65)):.0f}" cy="{NY + NR * .62 * math.sin(math.radians(65)):.0f}" r="16" fill="none" stroke="#F2D27A" stroke-width="5"/>'
    b += '<rect width="1920" height="1080" fill="url(#vig)"/>'
    return page('#05162e', svg(d, b), [('DIAMOND', 156, 'w'), ('HAIL', 250, 'y'), ('INSIDE?', 140, 'w')], outline='#041022')


open(os.path.join(HERE, 'A.html'), 'w').write(make())
print('wrote A')
