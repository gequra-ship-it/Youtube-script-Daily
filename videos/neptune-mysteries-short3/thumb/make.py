# Shorts thumbnail A for neptune-mysteries-short3 (guideline 16-9; brief tools/briefs/thumb_art.md). Run: python3 videos/neptune-mysteries-short3/thumb/make.py
# A  A HIDDEN / FIRE?   intuitive: Neptune with a cut-away wedge glowing like a furnace, heat waves rolling out; its frozen twin Uranus sits like an
#                       icebox with icicles, and a shivering frog in a woolly hat on Uranus holds its hands out to Neptune's warmth
#                       (S02-S07: Neptune emits more than 2.5x the heat it absorbs; Uranus "a quiet, frozen icebox"; "What hidden fire is burning inside Neptune")
import os, math, random
HERE = os.path.dirname(os.path.abspath(__file__))
LONG = os.path.join(HERE, '../../neptune-mysteries/thumb/make.py')   # shared helpers (frog, neptune, diamond) from the long-form thumbs
_src = open(LONG).read(); _g = {'__file__': LONG}; exec(_src[:_src.index('def thumb_A')], _g); globals().update({k: v for k, v in _g.items() if not k.startswith('__') and k != 'HERE'})

BEANIE = ('<path d="M-30 -80 q4 -40 38 -40 q36 0 38 40z" fill="#c9443c" stroke-width="3.2"/>'
          '<path d="M-34 -84 q40 -12 84 0 l0 12 q-42 -10 -84 0z" fill="#f2efe4" stroke-width="3.2"/>'
          '<path d="M-14 -112 q20 -8 40 0 M-22 -98 q30 -10 58 0" fill="none" stroke="#e8746a" stroke-width="3"/>'
          '<circle cx="8" cy="-124" r="11" fill="#f2efe4" stroke-width="3.2"/>')
SCARF = ('<path d="M-30 -30 q36 12 68 0 l0 14 q-34 12 -68 0z" fill="#3f7fd0" stroke-width="3.2"/>'
         '<path d="M-22 -22 l-8 40 l16 2 l4 -40z" fill="#3f7fd0" stroke-width="3.2"/><path d="M-30 18 l2 6 M-22 19 l0 7 M-15 20 l1 6" stroke-width="2.4"/>')


def make():
    random.seed(33)
    CX, CY, R = 1330, 520, 330
    d = FILTERS
    nd, nb = neptune(CX, CY, R, 'np', spot=False, light=(-.5, -.4))
    d += nd
    d += lin('bg', [(0, '#05061c'), (1, '#0b1030')])
    d += rad('core', CX, CY, R * .62, [(0, '#fff6c8', 1), (.25, '#ffd66a', 1), (.6, '#ff8a2a', 1), (1, '#c8361c', 1)])
    d += rad('mant', CX, CY, R * .86, [(0, '#ff7a2a', 1), (.7, '#b0402a', 1), (1, '#5a2a5a', 1)])
    d += rad('heat', CX, CY, R * 1.7, [(0, '#ff9a3a', .45), (.55, '#ff7a2a', .15), (1, '#ff7a2a', 0)])
    d += rad('ur', 300, 820, 280, [(0, '#f0fdfd', 1), (.55, '#b6e8ec', 1), (1, '#6aa8b2', 1)])
    d += rad('cold', 330, 930, 420, [(0, '#bfefff', .3), (1, '#bfefff', 0)])
    b = '<rect width="1920" height="1080" fill="url(#bg)"/>' + starfield(170, seed=8, op=.6)
    b += '<rect width="1920" height="1080" fill="url(#cold)"/>'
    b += f'<circle cx="{CX}" cy="{CY}" r="{R * 1.7:.0f}" fill="url(#heat)"/>'
    # heat waves rolling out of Neptune toward the frog (left/down-left)
    for k in range(5):
        rr = R + 40 + k * 46
        a0, a1 = 150, 222
        pts = []
        for i in range(0, 61):
            a = math.radians(a0 + (a1 - a0) * i / 60)
            rw = rr + 12 * math.sin(i * .55 + k)
            pts.append((CX + rw * math.cos(a), CY + rw * math.sin(a)))
        b += f'<path d="M' + ' L'.join(f'{x:.0f} {y:.0f}' for x, y in pts) + f'" fill="none" stroke="#ffc46a" stroke-width="{11 - k * 1.4:.1f}" stroke-linecap="round" opacity="{.85 - k * .14:.2f}"/>'
    b += nb
    # cut-away wedge facing the frog: glowing mantle + white-hot core
    a0, a1 = math.radians(122), math.radians(228)
    def wedge(r):
        return f'M{CX} {CY} L{CX + r * math.cos(a0):.1f} {CY + r * math.sin(a0):.1f} A{r} {r} 0 0 1 {CX + r * math.cos(a1):.1f} {CY + r * math.sin(a1):.1f}Z'
    b += f'<path d="{wedge(R)}" fill="#0b1d6a" stroke="#06123d" stroke-width="4"/>'
    b += f'<path d="{wedge(R * .9)}" fill="url(#mant)"/>'
    b += f'<path d="{wedge(R * .52)}" fill="url(#core)"/>'
    b += f'<clipPath id="wc"><path d="{wedge(R * .9)}"/></clipPath>'
    b += f'<circle cx="{CX}" cy="{CY}" r="{R * .45:.0f}" fill="#ffcf6a" opacity=".55" filter="url(#b24)" clip-path="url(#wc)"/>'
    # flames licking at the core edge
    for k in range(7):
        a = a0 + (a1 - a0) * (k + .5) / 7
        rr = R * .52
        x, y = CX + rr * math.cos(a), CY + rr * math.sin(a)
        b += f'<path d="M{x:.0f} {y:.0f} q{18 * math.cos(a) - 10:.0f} {18 * math.sin(a) - 8:.0f} {34 * math.cos(a):.0f} {34 * math.sin(a):.0f}" fill="none" stroke="#ffe08a" stroke-width="7" stroke-linecap="round" opacity=".8"/>'
    b += f'<path d="M{CX} {CY} L{CX + R * math.cos(a0):.1f} {CY + R * math.sin(a0):.1f} M{CX} {CY} L{CX + R * math.cos(a1):.1f} {CY + R * math.sin(a1):.1f}" stroke="#ffe6b0" stroke-width="4" opacity=".7"/>'
    b += f'<circle cx="{CX}" cy="{CY}" r="{R}" fill="none" stroke="#ffb35a" stroke-width="6" opacity=".35" filter="url(#b6)"/>'
    # Uranus: frozen icebox, bottom-left, with frost and icicles
    UX, UY, UR = 300, 950, 250
    b += f'<circle cx="{UX}" cy="{UY}" r="{UR + 30}" fill="#cff4ff" opacity=".18" filter="url(#b24)"/>'
    b += f'<circle cx="{UX}" cy="{UY}" r="{UR}" fill="url(#ur)" stroke="#2a4a5a" stroke-width="5"/>'
    b += f'<clipPath id="uc"><circle cx="{UX}" cy="{UY}" r="{UR}"/></clipPath><g clip-path="url(#uc)">'
    b += f'<circle cx="{UX + 90}" cy="{UY + 60}" r="{UR + 40}" fill="none" stroke="#1d3a4c" stroke-width="140" opacity=".22"/>'
    for k in range(5):
        b += f'<ellipse cx="{UX}" cy="{UY - 160 + k * 70}" rx="{UR + 20}" ry="10" fill="#ffffff" opacity=".18"/>'
    b += '</g>'
    # frost cap on top
    cap = 'M{0} {1}'.format(UX - 200, UY - 150)
    for i in range(0, 21):
        a = math.radians(-145 + 110 * i / 20)
        r = UR + 6 + (10 if i % 2 else -4)
        cap += f' L{UX + r * math.cos(a):.0f} {UY + r * math.sin(a):.0f}'
    b += f'<path d="{cap} L{UX + 200} {UY - 150} Q{UX} {UY - 190} {UX - 200} {UY - 150}Z" fill="#ffffff" stroke="#2a4a5a" stroke-width="4" stroke-linejoin="round" opacity=".95"/>'
    # icicles hanging off the right flank
    for k, a in enumerate(range(-40, 20, 8)):
        ar = math.radians(a)
        x, y = UX + UR * math.cos(ar), UY + UR * math.sin(ar)
        L = 34 + (k % 3) * 18
        b += f'<path d="M{x - 9:.0f} {y - 4:.0f} L{x + 9:.0f} {y + 2:.0f} L{x + 14 + L * .3:.0f} {y + L:.0f}Z" fill="#e8fbff" stroke="#2a4a5a" stroke-width="3" stroke-linejoin="round"/>'
    for _ in range(26):  # snow specks
        b += f'<circle cx="{random.uniform(40, 760):.0f}" cy="{random.uniform(560, 1060):.0f}" r="{random.choice([2, 3, 4])}" fill="#ffffff" opacity="{random.uniform(.4, .9):.2f}"/>'
    for x, y in ((150, 720), (470, 760), (90, 960)):
        b += spark(x, y, 16, '#e8fbff', .9)
    # shivering frog on top of Uranus, hands out toward Neptune's warmth
    FX, FY, S = 330, 730, 2.1
    b += frog(FX, FY, S, la='q20 -10 40 -6', ra='q30 -16 56 -26', mouth='o', look=(5, -1), hat=BEANIE, front=SCARF, tilt=4)
    for dx, dy in ((-110, -170), (-118, -120), (130, -200), (138, -150)):  # shiver marks
        b += f'<path d="M{FX + dx} {FY + dy} l{8 if dx > 0 else -8} 10 l{-8 if dx > 0 else 8} 10" fill="none" stroke="#cfefff" stroke-width="5" stroke-linecap="round"/>'
    for k in range(3):  # warm glow on the frog's hands
        b += f'<circle cx="{FX + 150}" cy="{FY - 100}" r="{60 + k * 20}" fill="#ffb35a" opacity=".08" filter="url(#b12)"/>'
    for x, y, s in ((1060, 180, 16), (1720, 160, 20), (1800, 420, 14)):
        b += spark(x, y, s)
    return page('#05061c', svg(d, b), [('A HIDDEN', 160, 'w'), ('FIRE?', 240, 'y')], outline='#05061c')


open(os.path.join(HERE, 'A.html'), 'w').write(make())
print('wrote A')
