# Shorts thumbnail A for neptune-mysteries-short4 (guideline 16-9: vertical 1080x1920, centred text; brief tools/briefs/thumb_art.md).
# Run: python3 videos/neptune-mysteries-short4/thumb/make.py
# A  DIAMOND / HAIL / INSIDE?   intuitive: deep inside Neptune's hot slushy mantle, diamonds sink like hail through the whole frame toward the glowing
#                               core at the bottom; text in the middle; below, the frog in a diving helmet rides the biggest diamond down; a small
#                               cut-away Neptune top-right marks where we are (S06, S11-S12: slush of water, ammonia, methane;
#                               "diamonds may be forming ... drift downward through the slush like heavy hail")
import os, sys, math, random
HERE = os.path.dirname(os.path.abspath(__file__))
LONG = os.path.join(HERE, '../../neptune-mysteries/thumb/make.py')   # shared helpers (frog, neptune, diamond, starfield) from the long-form thumbs
_src = open(LONG).read(); _g = {'__file__': LONG}; exec(_src[:_src.index('def thumb_A')], _g); globals().update({k: v for k, v in _g.items() if not k.startswith('__') and k != 'HERE'})
from thumb_lib import vpage, vsvg, blobs


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
    d += lin('sea', [(0, '#05162e'), (.3, '#0a3550'), (.62, '#145a66'), (.84, '#6a5a3a'), (1, '#c8662a')])
    d += rad('core', 540, 2250, 1150, [(0, '#fff2c0', 1), (.45, '#ffb04a', .9), (.62, '#ff7a2a', .55), (.8, '#c8462a', .15), (1, '#c8462a', 0)])
    d += rad('vig', 540, 960, 1150, [(0, '#000', 0), (.7, '#000', 0), (1, '#000', .5)])
    b = '<rect width="1080" height="1920" fill="url(#sea)"/><rect width="1080" height="1920" fill="url(#core)"/>'
    b += blobs(50, 0, 100, 1080, 1800, '#5fb6c0', .05, .14, 60, 220)   # churning slush
    for _ in range(24):
        x, y = random.uniform(-60, 1000), random.uniform(140, 1800)
        b += f'<path d="M{x:.0f} {y:.0f} q60 -40 120 0 t120 0" fill="none" stroke="#8fd6dc" stroke-width="{random.uniform(3, 7):.0f}" opacity="{random.uniform(.1, .25):.2f}" stroke-linecap="round"/>'
    for k in range(7):   # heat shimmer rising from the core
        x = 60 + k * 160
        b += f'<path d="M{x} 1920 q-20 -40 0 -80 t0 -80" fill="none" stroke="#ffd08a" stroke-width="5" stroke-linecap="round" opacity=".35"/>'
    # many diamonds sinking (hail), with wakes; the ones behind the text band are small
    hail = [(150, 330, 34), (420, 230, 22), (560, 520, 44), (260, 610, 26), (720, 640, 24), (950, 560, 30), (90, 760, 18), (980, 900, 16),
            (120, 1080, 20), (990, 1180, 18), (130, 1460, 36), (930, 1520, 40), (290, 1760, 22), (820, 1800, 26), (700, 300, 16), (60, 1300, 14)]
    for x, y, s in hail:
        b += trail(x, y, s, s * 5)
        b += diamond(x, y, s, rot=random.uniform(-14, 14))
    # hero diamond with the frog riding it down
    HX, HY, HS = 560, 1610, 175
    b += f'<circle cx="{HX}" cy="{HY + 40}" r="{HS * 1.9:.0f}" fill="#bff0ff" opacity=".18" filter="url(#b50)"/>'
    b += diamond(HX, HY, HS, rot=-6)
    b += f'<path d="M{HX - 55} {HY + 28} L{HX - 18} {HY + 110}" stroke="#ffffff" stroke-width="5" opacity=".5" stroke-linecap="round"/>'
    b += f'<path d="M{HX - HS} {HY + 6} L{HX} {HY + HS * 1.05:.0f} L{HX + HS} {HY - 10}" fill="none" stroke="#ffb04a" stroke-width="6" opacity=".55" transform="rotate(-6 {HX} {HY})"/>'
    collar = ('<ellipse cx="6" cy="-4" rx="42" ry="9" fill="#c99b45" stroke-width="3"/>'
              '<circle cx="-26" cy="-4" r="3" fill="#7a5233" stroke="none"/><circle cx="6" cy="2" r="3" fill="#7a5233" stroke="none"/><circle cx="38" cy="-4" r="3" fill="#7a5233" stroke="none"/>'
              '<path d="M48 -30 q34 -2 44 -34" fill="none" stroke="#5a3b25" stroke-width="7"/>')
    FX, FY, S = HX + 6, HY - 70, 2.3
    b += frog(FX, FY, S, la='q-22 4 -40 30', ra='q22 4 40 30', mouth='o', look=(-3, 3), helmet=True, front=collar, tilt=-6)
    for k in range(6):   # bubbles from the helmet hose, drifting up the right side
        b += f'<circle cx="{FX + 220 + k * 22 + random.uniform(-8, 8):.0f}" cy="{FY - 150 - k * 52:.0f}" r="{7 + k * 2}" fill="#dff8ff" fill-opacity=".15" stroke="#e6fbff" stroke-width="3" opacity=".8"/>'
    # small cut-away Neptune, top-right: "you are here" in the mantle
    NX, NY, NR = 860, 300, 120
    nd, nb = neptune(NX, NY, NR, 'mini', spot=False)
    d += nd
    b += f'<circle cx="{NX}" cy="{NY}" r="{NR + 20}" fill="#05162e" opacity=".6" filter="url(#b12)"/>' + nb
    a0, a1 = math.radians(20), math.radians(110)
    def wedge(r):
        return f'M{NX} {NY} L{NX + r * math.cos(a0):.1f} {NY + r * math.sin(a0):.1f} A{r} {r} 0 0 1 {NX + r * math.cos(a1):.1f} {NY + r * math.sin(a1):.1f}Z'
    b += f'<path d="{wedge(NR)}" fill="#1f4bc2" stroke="#e6fbff" stroke-width="3"/>'
    b += f'<path d="{wedge(NR * .82)}" fill="#1d7f8c"/><path d="{wedge(NR * .38)}" fill="#ffb04a"/>'
    for k in range(5):
        a = math.radians(35 + k * 15); r = NR * (.5 + .06 * (k % 3))
        b += diamond(NX + r * math.cos(a), NY + r * math.sin(a), 8, glow=False)
    b += f'<circle cx="{NX + NR * .62 * math.cos(math.radians(65)):.0f}" cy="{NY + NR * .62 * math.sin(math.radians(65)):.0f}" r="17" fill="none" stroke="#F2D27A" stroke-width="5"/>'
    b += '<rect width="1080" height="1920" fill="url(#vig)"/>'
    return vpage('#05162e', vsvg(d, b), [('DIAMOND', 172, 'w'), ('HAIL', 270, 'y'), ('INSIDE?', 150, 'w')], outline='#041022', top=700)


open(os.path.join(HERE, 'A.html'), 'w').write(make())
print('wrote A')
