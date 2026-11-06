# Shorts thumbnail A for neptune-mysteries-short3 (guideline 16-9: vertical 1080x1920, centred text; brief tools/briefs/thumb_art.md).
# Run: python3 videos/neptune-mysteries-short3/thumb/make.py
# A  A HIDDEN / FIRE?   intuitive: Neptune (top) with a cut-away wedge glowing like a furnace, heat waves rolling down; text in the middle; its frozen
#                       twin Uranus below is an icebox with a frost cap and icicles, and a shivering frog in a woolly hat on Uranus holds its hands up
#                       to Neptune's warmth (S02-S07: Neptune emits more than 2.5x the heat it absorbs; Uranus "a quiet, frozen icebox";
#                       "What hidden fire is burning inside Neptune")
import os, sys, math, random
HERE = os.path.dirname(os.path.abspath(__file__))
LONG = os.path.join(HERE, '../../neptune-mysteries/thumb/make.py')   # shared helpers (frog, neptune, diamond, starfield) from the long-form thumbs
_src = open(LONG).read(); _g = {'__file__': LONG}; exec(_src[:_src.index('def thumb_A')], _g); globals().update({k: v for k, v in _g.items() if not k.startswith('__') and k != 'HERE'})
from thumb_lib import vpage, vsvg, blobs

BEANIE = ('<path d="M-30 -80 q4 -40 38 -40 q36 0 38 40z" fill="#c9443c" stroke-width="3.2"/>'
          '<path d="M-34 -84 q40 -12 84 0 l0 12 q-42 -10 -84 0z" fill="#f2efe4" stroke-width="3.2"/>'
          '<path d="M-14 -112 q20 -8 40 0 M-22 -98 q30 -10 58 0" fill="none" stroke="#e8746a" stroke-width="3"/>'
          '<circle cx="8" cy="-124" r="11" fill="#f2efe4" stroke-width="3.2"/>')
SCARF = ('<path d="M-30 -30 q36 12 68 0 l0 14 q-34 12 -68 0z" fill="#3f7fd0" stroke-width="3.2"/>'
         '<path d="M-22 -22 l-8 40 l16 2 l4 -40z" fill="#3f7fd0" stroke-width="3.2"/><path d="M-30 18 l2 6 M-22 19 l0 7 M-15 20 l1 6" stroke-width="2.4"/>')


def make():
    random.seed(33)
    CX, CY, R = 600, 470, 305
    d = FILTERS
    nd, nb = neptune(CX, CY, R, 'np', spot=False, light=(.4, -.5))
    d += nd
    d += lin('bg', [(0, '#05061c'), (.6, '#0b1030'), (1, '#0e2236')])
    d += rad('core', CX, CY, R * .62, [(0, '#fff6c8', 1), (.25, '#ffd66a', 1), (.6, '#ff8a2a', 1), (1, '#c8361c', 1)])
    d += rad('mant', CX, CY, R * .86, [(0, '#ff7a2a', 1), (.7, '#b0402a', 1), (1, '#5a2a5a', 1)])
    d += rad('heat', CX, CY, R * 1.8, [(0, '#ff9a3a', .45), (.55, '#ff7a2a', .15), (1, '#ff7a2a', 0)])
    UX, UY, UR = 420, 1830, 300
    d += rad('ur', UX - 60, UY - 120, UR * 1.1, [(0, '#f0fdfd', 1), (.55, '#b6e8ec', 1), (1, '#6aa8b2', 1)])
    d += rad('cold', UX, UY - 100, 560, [(0, '#bfefff', .3), (1, '#bfefff', 0)])
    b = '<rect width="1080" height="1920" fill="url(#bg)"/>' + starfield(240, x1=1080, y1=1920, seed=8, op=.6)
    b += '<rect width="1080" height="1920" fill="url(#cold)"/>'
    b += f'<circle cx="{CX}" cy="{CY}" r="{R * 1.8:.0f}" fill="url(#heat)"/>'
    # heat waves rolling out of Neptune, down toward the frog (behind the text they are faint)
    for k in range(5):
        rr = R + 40 + k * 44
        pts = []
        for i in range(0, 61):
            a = math.radians(55 + 90 * i / 60)
            rw = rr + 12 * math.sin(i * .55 + k)
            pts.append((CX + rw * math.cos(a), CY + rw * math.sin(a)))
        b += '<path d="M' + ' L'.join(f'{x:.0f} {y:.0f}' for x, y in pts) + f'" fill="none" stroke="#ffc46a" stroke-width="{11 - k * 1.4:.1f}" stroke-linecap="round" opacity="{.85 - k * .16:.2f}"/>'
    b += nb
    # cut-away wedge facing down (toward the frog): glowing mantle + white-hot core
    a0, a1 = math.radians(48), math.radians(150)
    def wedge(r):
        return f'M{CX} {CY} L{CX + r * math.cos(a0):.1f} {CY + r * math.sin(a0):.1f} A{r} {r} 0 0 1 {CX + r * math.cos(a1):.1f} {CY + r * math.sin(a1):.1f}Z'
    b += f'<path d="{wedge(R)}" fill="#0b1d6a" stroke="#06123d" stroke-width="4"/>'
    b += f'<path d="{wedge(R * .9)}" fill="url(#mant)"/>'
    b += f'<path d="{wedge(R * .52)}" fill="url(#core)"/>'
    b += f'<clipPath id="wc"><path d="{wedge(R * .9)}"/></clipPath>'
    b += f'<circle cx="{CX}" cy="{CY}" r="{R * .45:.0f}" fill="#ffcf6a" opacity=".55" filter="url(#b24)" clip-path="url(#wc)"/>'
    for k in range(7):   # flames licking at the core edge
        a = a0 + (a1 - a0) * (k + .5) / 7
        x, y = CX + R * .52 * math.cos(a), CY + R * .52 * math.sin(a)
        b += f'<path d="M{x:.0f} {y:.0f} q{18 * math.cos(a) - 10:.0f} {18 * math.sin(a) - 8:.0f} {34 * math.cos(a):.0f} {34 * math.sin(a):.0f}" fill="none" stroke="#ffe08a" stroke-width="7" stroke-linecap="round" opacity=".8"/>'
    b += f'<path d="M{CX} {CY} L{CX + R * math.cos(a0):.1f} {CY + R * math.sin(a0):.1f} M{CX} {CY} L{CX + R * math.cos(a1):.1f} {CY + R * math.sin(a1):.1f}" stroke="#ffe6b0" stroke-width="4" opacity=".7"/>'
    b += f'<circle cx="{CX}" cy="{CY}" r="{R}" fill="none" stroke="#ffb35a" stroke-width="6" opacity=".35" filter="url(#b6)"/>'
    for x, y, s in ((160, 260, 18), (980, 210, 22), (1000, 700, 14)):
        b += spark(x, y, s)
    # Uranus: frozen icebox at the bottom, with frost cap and icicles
    b += f'<circle cx="{UX}" cy="{UY}" r="{UR + 30}" fill="#cff4ff" opacity=".18" filter="url(#b24)"/>'
    b += f'<circle cx="{UX}" cy="{UY}" r="{UR}" fill="url(#ur)" stroke="#2a4a5a" stroke-width="5"/>'
    b += f'<clipPath id="uc"><circle cx="{UX}" cy="{UY}" r="{UR}"/></clipPath><g clip-path="url(#uc)">'
    b += f'<circle cx="{UX + 110}" cy="{UY + 70}" r="{UR + 40}" fill="none" stroke="#1d3a4c" stroke-width="150" opacity=".22"/>'
    for k in range(5):
        b += f'<ellipse cx="{UX}" cy="{UY - 200 + k * 80}" rx="{UR + 20}" ry="10" fill="#ffffff" opacity=".18"/>'
    b += '</g>'
    cap = f'M{UX - 240} {UY - 180}'
    for i in range(0, 21):
        a = math.radians(-145 + 110 * i / 20)
        r = UR + 6 + (10 if i % 2 else -4)
        cap += f' L{UX + r * math.cos(a):.0f} {UY + r * math.sin(a):.0f}'
    b += f'<path d="{cap} L{UX + 240} {UY - 180} Q{UX} {UY - 230} {UX - 240} {UY - 180}Z" fill="#ffffff" stroke="#2a4a5a" stroke-width="4" stroke-linejoin="round" opacity=".95"/>'
    for k, a in enumerate(range(-36, 4, 7)):   # icicles hanging off the right flank
        ar = math.radians(a)
        x, y = UX + UR * math.cos(ar), UY + UR * math.sin(ar)
        L = 36 + (k % 3) * 20
        b += f'<path d="M{x - 10:.0f} {y - 4:.0f} L{x + 10:.0f} {y + 2:.0f} L{x + 14 + L * .3:.0f} {y + L:.0f}Z" fill="#e8fbff" stroke="#2a4a5a" stroke-width="3" stroke-linejoin="round"/>'
    for _ in range(30):  # snow specks
        b += f'<circle cx="{random.uniform(30, 1050):.0f}" cy="{random.uniform(1330, 1880):.0f}" r="{random.choice([2, 3, 4])}" fill="#ffffff" opacity="{random.uniform(.4, .9):.2f}"/>'
    for x, y in ((120, 1450), (900, 1420), (980, 1700)):
        b += spark(x, y, 16, '#e8fbff', .9)
    # shivering frog on top of Uranus, hands raised toward Neptune's warmth
    FX, FY, S = 450, 1585, 2.3
    for k in range(3):  # warm glow on the frog's hands
        b += f'<circle cx="{FX + 20}" cy="{FY - 260}" r="{70 + k * 24}" fill="#ffb35a" opacity=".08" filter="url(#b12)"/>'
    b += frog(FX, FY, S, la='q-26 -14 -38 -40', ra='q26 -14 38 -40', mouth='o', look=(1, -5), hat=BEANIE, front=SCARF, tilt=0)
    for dx, dy in ((-120, -170), (-128, -120), (140, -190), (148, -140)):  # shiver marks
        b += f'<path d="M{FX + dx} {FY + dy} l{8 if dx > 0 else -8} 10 l{-8 if dx > 0 else 8} 10" fill="none" stroke="#cfefff" stroke-width="5" stroke-linecap="round"/>'
    return vpage('#05061c', vsvg(d, b), [('A HIDDEN', 172, 'w'), ('FIRE?', 270, 'y')], outline='#05061c', top=820)


open(os.path.join(HERE, 'A.html'), 'w').write(make())
print('wrote A')
