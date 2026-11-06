# Shorts thumbnail A for neptune-mysteries-short2 (guideline 16-9: vertical 1080x1920, centred text; brief tools/briefs/thumb_art.md).
# Run: python3 videos/neptune-mysteries-short2/thumb/make.py
# A  WEAKEST SUN / STRONGEST / WINDS   intuitive: inside Neptune's sky the Sun is only a tiny dim dot at the top; white jet-stream streaks blast
#                                      westward (to the left) through the whole frame; text in the middle; below, a frog in goggles and a streaming
#                                      scarf clings to a windsock pole on a methane-ice cloud (S08-S10: "the weakest sunlight in the solar system drives
#                                      some of its strongest winds"; S04 westward jets)
import os, sys, math, random
HERE = os.path.dirname(os.path.abspath(__file__))
LONG = os.path.join(HERE, '../../neptune-mysteries/thumb/make.py')   # shared helpers (frog, neptune, diamond, starfield) from the long-form thumbs
_src = open(LONG).read(); _g = {'__file__': LONG}; exec(_src[:_src.index('def thumb_A')], _g); globals().update({k: v for k, v in _g.items() if not k.startswith('__') and k != 'HERE'})
from thumb_lib import vpage, vsvg, blobs

GOGGLES = ('<path d="M-30 -70 q36 -10 68 0" fill="none" stroke="#5a3b25" stroke-width="6"/>'
           '<circle cx="-10" cy="-66" r="16" fill="#9fd8ff" fill-opacity=".25" stroke="#7a5233" stroke-width="5"/>'
           '<circle cx="22" cy="-66" r="16" fill="#9fd8ff" fill-opacity=".25" stroke="#7a5233" stroke-width="5"/>'
           '<path d="M-18 -74 q4 -4 10 -4 M14 -74 q4 -4 10 -4" fill="none" stroke="#fff" stroke-width="3" opacity=".8"/>')
SCARF = '<path d="M-30 -30 q36 12 68 0 l0 12 q-34 12 -68 0z" fill="#d9a43a" stroke-width="3.2"/>'
TAILS = ('<path d="M-28 -24 q-40 -10 -80 4 q-20 8 -46 0 l6 14 q22 6 42 -2 q40 -14 80 -4z" fill="#e8b84a" stroke-width="3.2"/>'
         '<path d="M-26 -20 q-36 8 -70 30 q-16 8 -36 6 l8 12 q20 0 34 -8 q34 -20 66 -28z" fill="#c98f2a" stroke-width="3.2"/>'
         '<path d="M-124 6 l-10 -6 M-122 12 l-12 2 M-100 46 l-10 2 M-98 40 l-10 -6" stroke-width="3"/>')


def streak(x, y, L, w, col, op, bend=0):
    # tapered speed streak: thick head at the left (it races left), thin tail on the right
    return (f'<path d="M{x:.0f} {y:.0f} q{L * .5:.0f} {bend - w:.0f} {L:.0f} {bend:.0f} q{-L * .5:.0f} {w * .2 - bend * .2:.0f} {-L:.0f} {w:.0f} q{-w * .6:.0f} {-w * .5:.0f} 0 {-w:.0f}z" '
            f'fill="{col}" opacity="{op:.2f}"/>')


def make():
    random.seed(22)
    d = FILTERS
    d += lin('sky', [(0, '#030a2c'), (.35, '#0b2580'), (.62, '#1a4cc0'), (.84, '#4f8cf0'), (.9, '#8ab8ff'), (1, '#0a1e66')])
    SX, SY = 790, 300
    d += rad('sun', SX, SY, 90, [(0, '#fff6d6', .9), (.3, '#ffe9a8', .25), (1, '#ffe9a8', 0)])
    d += lin('pole', [(0, '#e7ebf2'), (.5, '#9aa3b5'), (1, '#5d6678')], 1, 0)
    b = '<rect width="1080" height="1920" fill="url(#sky)"/>' + starfield(120, x1=1080, y1=650, seed=5, op=.55)
    # the tiny, faint Sun
    b += f'<circle cx="{SX}" cy="{SY}" r="90" fill="url(#sun)"/><circle cx="{SX}" cy="{SY}" r="9" fill="#fff8e0"/>'
    for a in range(0, 360, 45):
        r0, r1 = 17, 32
        b += f'<path d="M{SX + r0 * math.cos(math.radians(a)):.1f} {SY + r0 * math.sin(math.radians(a)):.1f} L{SX + r1 * math.cos(math.radians(a)):.1f} {SY + r1 * math.sin(math.radians(a)):.1f}" stroke="#ffe9a8" stroke-width="2.4" opacity=".55" stroke-linecap="round"/>'
    b += f'<circle cx="{SX}" cy="{SY}" r="46" fill="none" stroke="#ffe9a8" stroke-width="2" stroke-dasharray="6 8" opacity=".35"/>'
    # distant cloud bands
    for k in range(9):
        y = 520 + k * 120
        b += f'<path d="M-50 {y} q540 {-30 + k * 6} 1180 {-10}" fill="none" stroke="#7fb0ff" stroke-width="{18 + k * 5}" opacity="{.06 + k * .015:.2f}" filter="url(#b12)"/>'
    # jet-stream streaks racing left through the whole frame (dim behind the text band)
    for _ in range(70):
        y = random.uniform(380, 1640); L = random.uniform(200, 520); x = random.uniform(-200, 1060)
        textzone = 740 < y < 1290
        op = random.uniform(.1, .22) if textzone else random.uniform(.45, .95)
        w = random.uniform(6, 20)
        b += streak(x, y, L, w, random.choice(['#ffffff', '#cfe6ff', '#9fd0ff']), op, bend=random.uniform(-14, 6))
    for _ in range(14):  # blurred big gusts
        y = random.uniform(420, 1600); x = random.uniform(-100, 700)
        b += f'<path d="M{x:.0f} {y:.0f} q300 -20 640 -6" fill="none" stroke="#bfe0ff" stroke-width="{random.uniform(20, 40):.0f}" stroke-linecap="round" opacity=".12" filter="url(#b12)"/>'
    # cloud deck (bright methane-ice wisps)
    b += '<path d="M0 1700 q180 -40 360 -10 q200 30 380 -20 q200 -30 340 0 L1080 1920 L0 1920Z" fill="#0d2a85"/>'
    b += '<path d="M0 1730 q200 -30 400 0 q200 30 380 -10 q180 -20 300 6 L1080 1920 L0 1920Z" fill="#081b5c"/>'
    for _ in range(18):
        x = random.uniform(-100, 1100); y = random.uniform(1660, 1760); L = random.uniform(140, 340)
        b += f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{L / 2:.0f}" ry="{random.uniform(6, 14):.0f}" fill="#e8f2ff" opacity="{random.uniform(.25, .6):.2f}" filter="url(#b6)"/>'
    # methane-ice cloud the frog stands on
    CXc, CYc = 600, 1720
    blobs_ = ((-170, 10, 70), (-90, -30, 90), (10, -50, 100), (110, -26, 86), (190, 10, 62), (0, 20, 110))
    cl = ''.join(f'<circle cx="{CXc + dx}" cy="{CYc + dy}" r="{r}" fill="#f4f8ff" stroke="#1d2b4c" stroke-width="5"/>' for dx, dy, r in blobs_)
    cl += ''.join(f'<circle cx="{CXc + dx}" cy="{CYc + dy}" r="{r - 3}" fill="#f4f8ff"/>' for dx, dy, r in blobs_)
    cl += f'<ellipse cx="{CXc + 10}" cy="{CYc + 60}" rx="210" ry="40" fill="#b9cdf0" opacity=".7"/>'
    cl += f'<path d="M{CXc - 130} {CYc - 40} q30 -40 80 -50" fill="none" stroke="#ffffff" stroke-width="10" stroke-linecap="round"/>'
    b += cl
    for k in range(5):  # wisps torn off the cloud to the left
        b += f'<path d="M{CXc - 220} {CYc - 40 + k * 22} q-90 -8 -{200 + k * 50} {-6 + k * 4}" fill="none" stroke="#f4f8ff" stroke-width="{12 - k * 2}" stroke-linecap="round" opacity=".55"/>'
    # windsock pole
    FX, FY, S = 560, 1676, 2.6
    hx = FX + (78 * math.cos(math.radians(10)) + 50 * math.sin(math.radians(10))) * S
    hy = FY + (78 * math.sin(math.radians(10)) - 50 * math.cos(math.radians(10))) * S
    PX, PT = int(hx), 1330
    b += f'<rect x="{PX - 9}" y="{PT}" width="18" height="{CYc - 100 - PT}" rx="9" fill="url(#pole)" stroke="{INK}" stroke-width="4"/>'
    b += f'<circle cx="{PX}" cy="{PT - 2}" r="14" fill="#d9a43a" stroke="{INK}" stroke-width="4"/>'
    ws = f'<g transform="translate({PX - 4} {PT + 46})">'   # windsock fully horizontal, pointing downwind (left)
    for x, h, col in [(0, 50, '#e2453c'), (-56, 44, '#f4f1e6'), (-108, 38, '#e2453c'), (-156, 33, '#f4f1e6'), (-198, 28, '#e2453c')]:
        ws += f'<path d="M{x} {-h} L{x - 52} {-h + 6} L{x - 52} {h - 6 + 8} L{x} {h}Z" fill="{col}" stroke="{INK}" stroke-width="4" stroke-linejoin="round"/>'
    b += ws + '</g>'
    # frog leaning into the wind, gripping the pole, scarf streaming left
    b += frog(FX, FY, S, la='q-26 -14 -46 -4', ra='q22 -12 40 -28', mouth='o', look=(4, -3), hat=GOGGLES, front=SCARF, back=TAILS, tilt=10)
    b += f'<circle cx="{hx:.0f}" cy="{hy:.0f}" r="{5.5 * S:.0f}" fill="{GREEN}" stroke="{INK}" stroke-width="{3 * S:.1f}"/>'
    for y in (1420, 1500, 1580):   # streaks in front of the frog for depth
        b += streak(random.uniform(40, 120), y, random.uniform(220, 280), 9, '#ffffff', .8, bend=-6)
    return vpage('#030a2c', vsvg(d, b), [('WEAKEST SUN', 122, 'w'), ('STRONGEST', 156, 'w'), ('WINDS', 260, 'y')], outline='#030a2a', top=770)


open(os.path.join(HERE, 'A.html'), 'w').write(make())
print('wrote A')
