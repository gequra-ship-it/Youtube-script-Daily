# Shorts thumbnail A for neptune-mysteries-short2 (guideline 16-9; brief tools/briefs/thumb_art.md). Run: python3 videos/neptune-mysteries-short2/thumb/make.py
# A  WEAKEST SUN / STRONGEST / WINDS   intuitive: inside Neptune's sky, white jet-stream streaks blast westward (to the left) past a frog in goggles
#                                      clinging to a windsock pole on a methane-ice cloud; the Sun is only a tiny dim dot (S08-S10: "the weakest sunlight
#                                      in the solar system drives some of its strongest winds"; S04 westward jets)
import os, math, random
HERE = os.path.dirname(os.path.abspath(__file__))
LONG = os.path.join(HERE, '../../neptune-mysteries/thumb/make.py')   # shared helpers (frog, neptune, diamond) from the long-form thumbs
_src = open(LONG).read(); _g = {'__file__': LONG}; exec(_src[:_src.index('def thumb_A')], _g); globals().update({k: v for k, v in _g.items() if not k.startswith('__') and k != 'HERE'})

GOGGLES = ('<path d="M-30 -70 q36 -10 68 0" fill="none" stroke="#5a3b25" stroke-width="6"/>'
           '<circle cx="-10" cy="-66" r="16" fill="#9fd8ff" fill-opacity=".25" stroke="#7a5233" stroke-width="5"/>'
           '<circle cx="22" cy="-66" r="16" fill="#9fd8ff" fill-opacity=".25" stroke="#7a5233" stroke-width="5"/>'
           '<path d="M-18 -74 q4 -4 10 -4 M14 -74 q4 -4 10 -4" fill="none" stroke="#fff" stroke-width="3" opacity=".8"/>')
# scarf around the neck, tails streaming to the left (downwind)
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
    d += lin('sky', [(0, '#040c33'), (.45, '#0f2f97'), (.72, '#2a63db'), (.78, '#6aa2ff'), (1, '#0a1e66')])
    d += rad('sun', 1640, 150, 60, [(0, '#fff6d6', .9), (.3, '#ffe9a8', .25), (1, '#ffe9a8', 0)])
    d += lin('pole', [(0, '#e7ebf2'), (.5, '#9aa3b5'), (1, '#5d6678')], 1, 0)
    b = '<rect width="1920" height="1080" fill="url(#sky)"/>' + starfield(90, y1=420, seed=5, op=.5)
    # the tiny, faint Sun
    b += '<circle cx="1640" cy="150" r="60" fill="url(#sun)"/><circle cx="1640" cy="150" r="7" fill="#fff8e0"/>'
    for a in range(0, 360, 45):
        r0, r1 = 14, 26
        b += f'<path d="M{1640 + r0 * math.cos(math.radians(a)):.1f} {150 + r0 * math.sin(math.radians(a)):.1f} L{1640 + r1 * math.cos(math.radians(a)):.1f} {150 + r1 * math.sin(math.radians(a)):.1f}" stroke="#ffe9a8" stroke-width="2" opacity=".5" stroke-linecap="round"/>'
    # distant cloud bands
    for k in range(6):
        y = 520 + k * 50
        b += f'<path d="M-50 {y} q960 {-30 + k * 6} 2020 {-10}" fill="none" stroke="#7fb0ff" stroke-width="{18 + k * 6}" opacity="{.08 + k * .02:.2f}" filter="url(#b12)"/>'
    # cloud deck (bright methane-ice wisps) at ~78 %
    b += '<path d="M0 840 q240 -40 480 -10 q260 30 520 -20 q280 -40 560 0 q220 30 360 0 L1920 1080 L0 1080Z" fill="#0d2a85"/>'
    b += '<path d="M0 860 q260 -30 520 0 q260 30 520 -10 q300 -30 560 10 q200 24 320 0 L1920 1080 L0 1080Z" fill="#081b5c"/>'
    for _ in range(26):
        x = random.uniform(-100, 1900); y = random.uniform(780, 900); L = random.uniform(160, 420)
        b += f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{L / 2:.0f}" ry="{random.uniform(6, 14):.0f}" fill="#e8f2ff" opacity="{random.uniform(.25, .6):.2f}" filter="url(#b6)"/>'
    # jet-stream streaks racing left across the sky
    for _ in range(46):
        y = random.uniform(160, 820); L = random.uniform(220, 620); x = random.uniform(-200, 1900)
        textzone = x < 1050 and y < 520
        op = random.uniform(.12, .3) if textzone else random.uniform(.45, .95)
        w = random.uniform(6, 20)
        b += streak(x, y, L, w, random.choice(['#ffffff', '#cfe6ff', '#9fd0ff']), op, bend=random.uniform(-14, 6))
    for _ in range(14):  # blurred big gusts
        y = random.uniform(300, 800); x = random.uniform(500, 1700)
        b += f'<path d="M{x:.0f} {y:.0f} q300 -20 640 -6" fill="none" stroke="#bfe0ff" stroke-width="{random.uniform(20, 40):.0f}" stroke-linecap="round" opacity=".12" filter="url(#b12)"/>'
    # methane-ice cloud the frog stands on
    CXc, CYc = 1130, 900
    cl = ''
    for dx, dy, r in ((-150, 10, 70), (-80, -30, 90), (10, -50, 100), (100, -26, 86), (170, 10, 62), (0, 20, 110)):
        cl += f'<circle cx="{CXc + dx}" cy="{CYc + dy}" r="{r}" fill="#f4f8ff" stroke="#1d2b4c" stroke-width="5"/>'
    for dx, dy, r in ((-150, 10, 70), (-80, -30, 90), (10, -50, 100), (100, -26, 86), (170, 10, 62), (0, 20, 110)):
        cl += f'<circle cx="{CXc + dx}" cy="{CYc + dy}" r="{r - 3}" fill="#f4f8ff"/>'
    cl += f'<ellipse cx="{CXc + 10}" cy="{CYc + 60}" rx="200" ry="40" fill="#b9cdf0" opacity=".7"/>'
    cl += f'<path d="M{CXc - 120} {CYc - 40} q30 -40 80 -50" fill="none" stroke="#ffffff" stroke-width="10" stroke-linecap="round"/>'
    b += f'<g>{cl}</g>'
    # wisps torn off the cloud to the left
    for k in range(5):
        b += f'<path d="M{CXc - 200} {CYc - 40 + k * 22} q-90 -8 -{200 + k * 50} {-6 + k * 4}" fill="none" stroke="#f4f8ff" stroke-width="{12 - k * 2}" stroke-linecap="round" opacity=".55"/>'
    # windsock pole
    FX, FY, S = 1110, 850, 2.8
    hx = FX + (78 * math.cos(math.radians(10)) + 50 * math.sin(math.radians(10))) * S
    hy = FY + (78 * math.sin(math.radians(10)) - 50 * math.cos(math.radians(10))) * S
    PX = int(hx)
    b += f'<rect x="{PX - 9}" y="430" width="18" height="{CYc - 110 - 430}" rx="9" fill="url(#pole)" stroke="{INK}" stroke-width="4"/>'
    b += f'<circle cx="{PX}" cy="428" r="14" fill="#d9a43a" stroke="{INK}" stroke-width="4"/>'
    # windsock fully horizontal, pointing downwind (left)
    ws = f'<g transform="translate({PX - 4} 470)">'
    segs = [(0, 54, '#e2453c'), (-60, 48, '#f4f1e6'), (-116, 42, '#e2453c'), (-168, 36, '#f4f1e6'), (-214, 30, '#e2453c')]
    for x, h, col in segs:
        ws += f'<path d="M{x} {-h} L{x - 56} {-h + 6} L{x - 56} {h - 6 + 8} L{x} {h}Z" fill="{col}" stroke="{INK}" stroke-width="4" stroke-linejoin="round"/>'
    ws += '<path d="M0 -54 L-270 -24" fill="none" stroke="#ffffff" stroke-width="4" opacity=".5"/>'
    ws += '</g>'
    b += ws
    # frog leaning into the wind, gripping the pole, scarf streaming left
    b += frog(FX, FY, S, la='q-26 -14 -46 -4', ra='q22 -12 40 -28', mouth='o', look=(4, -3), hat=GOGGLES, front=SCARF, back=TAILS, tilt=10)
    # the frog's grip on the pole (redraw hand over the pole)
    b += f'<circle cx="{hx:.0f}" cy="{hy:.0f}" r="{5.5 * S:.0f}" fill="{GREEN}" stroke="{INK}" stroke-width="{3 * S:.1f}"/>'
    # a few streaks in front of the frog for depth
    for y in (640, 720, 800):
        b += streak(random.uniform(260, 420), y, random.uniform(300, 380), 9, '#ffffff', .8, bend=-6)
    return page('#040c33', svg(d, b), [('WEAKEST SUN', 112, 'w'), ('STRONGEST', 146, 'w'), ('WINDS', 220, 'y')], outline='#030a2a')


open(os.path.join(HERE, 'A.html'), 'w').write(make())
print('wrote A')
