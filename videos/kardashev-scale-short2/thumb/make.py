# Shorts thumbnail A for kardashev-scale-short2 (guideline 16-9: VERTICAL 1080x1920, text centred). Run: python3 make.py
# TYPE 0.7 / LONG WAY UP   intuitive: a golden ladder rising from Earth's night-side horizon (bottom) up into space, a bright star
#                          half way, a galaxy at the top; the frog in a climbing helmet with a headlamp stands on Earth and
#                          stretches for the glowing first rung, still out of reach. Text centred across the ladder's middle.
#                          (script: "where exactly do we stand on this monumental ladder?",
#                           "Carl Sagan estimated that humanity sits somewhere around Type zero point seven", "a long way to go")
import os, sys, math, random
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
sys.path.insert(0, os.path.join(REPO, 'tools'))
LONG = os.path.join(REPO, 'videos', 'kardashev-scale', 'thumb', 'make.py')
G = {'__file__': LONG}; exec(open(LONG).read().split('\nfor n, fn in')[0], G)
frog, starfield, nebula, galaxy, FILTERS, P, INK = G['frog'], G['starfield'], G['nebula'], G['galaxy'], G['FILTERS'], G['P'], G['INK']
from thumb_lib import vpage, vsvg, lin, rad, spark


def climb_helmet():
    return ('<path d="M-38 -82 q0 -50 44 -52 q44 2 46 52 q-44 -8 -90 0z" fill="#e2483a" stroke-width="4"/>'
            '<path d="M-20 -104 q10 -18 30 -20" fill="none" stroke="#ffb0a0" stroke-width="4" opacity=".85"/>'
            '<path d="M-12 -132 q14 -4 32 0" fill="none" stroke="#a82a20" stroke-width="4"/>'
            '<rect x="-6" y="-104" width="24" height="16" rx="5" fill="#3a3f4a" stroke-width="3"/><circle cx="6" cy="-96" r="5.5" fill="#fff6c8" stroke="none"/>'
            '<path d="M-40 -82 q-2 30 8 52 M52 -82 q2 30 -8 52" fill="none" stroke="#3a3f4a" stroke-width="3"/>')


def lerp(a, b, t):
    return a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t


def make():
    rnd = random.Random(8)
    EX, EY, ER = 540, 3080, 1460           # Earth (top of the horizon at y = 1620)
    d = FILTERS
    d += lin('sky', [(0, '#0a0c2c'), (.55, '#0d1a3e'), (1, '#12355a')], 0, 1)
    d += rad('earth', EX, EY, ER, [(0, '#03060e', 1), (.93, '#081428', 1), (.985, '#14407a', 1), (1, '#6fd0ff', 1)])
    d += rad('dawn', -60, 1640, 760, [(0, '#ffd08a', .75), (.3, '#ff8a4a', .35), (1, '#a03a6a', 0)])
    d += lin('railG', [(0, '#b87a28'), (.5, '#f2c25a'), (1, '#9a6020')], 1, 0)
    d += rad('vig', 540, 960, 1150, [(0, '#000', 0), (.7, '#000', 0), (1, '#000', .55)])
    d += rad('topglow', 760, 220, 560, [(0, '#fff2d8', .6), (.3, '#c9b8ff', .3), (1, '#6a4ac0', 0)])
    d += rad('beam', 540, 1300, 700, [(0, '#fff6c8', .5), (1, '#fff6c8', 0)])
    d += rad('starM', 860, 560, 190, [(0, '#ffffff', 1), (.2, '#ffe9a8', .9), (.5, '#ffb455', .3), (1, '#ff8a3a', 0)])
    d += rad('txtBg', 540, 960, 560, [(0, '#040620', .55), (.6, '#040620', .3), (1, '#040620', 0)])
    b = '<rect width="1080" height="1920" fill="url(#sky)"/>'
    b += nebula(rnd, 14, (0, 0, 1080, 1500), ['#4a3aa0', '#1a5aa0', '#8a3a8a', '#2a7a9a'], 160, 360)
    b += starfield(rnd, 520, (0, 0, 1080, 1650))
    b += '<rect width="1080" height="1920" fill="url(#topglow)"/>'
    b += galaxy(760, 220, 330, 110, -14, rnd)
    b += '<circle cx="860" cy="560" r="190" fill="url(#starM)"/><circle cx="860" cy="560" r="24" fill="#fffdf4"/>'
    b += '<ellipse cx="860" cy="560" rx="220" ry="4" fill="#fff6d8" opacity=".7"/><ellipse cx="860" cy="560" rx="4" ry="150" fill="#fff6d8" opacity=".5"/>'
    # ---- the ladder into space (perspective: wide at the base, thin at the top, leaning to the upper right) ----
    L0, R0, L1, R1 = (330, 1625), (750, 1625), (740, 120), (790, 120)
    def rail(a, c, w0=46, w1=4):
        q = [(a[0] - w0 / 2, a[1]), (c[0] - w1 / 2, c[1]), (c[0] + w1 / 2, c[1]), (a[0] + w0 / 2, a[1])]
        hl = [(a[0] - w0 * .32, a[1]), (c[0] - w1 * .3, c[1]), (c[0] - w1 * .05, c[1]), (a[0] - w0 * .05, a[1])]
        return (f'<polygon points="{P(q)}" fill="url(#railG)" stroke="#2a1a08" stroke-width="5" stroke-linejoin="round"/>'
                f'<polygon points="{P(hl)}" fill="#fff2c0" opacity=".75"/>')
    lad = f'<path d="M{L0[0]} {L0[1]} L{L1[0]} {L1[1]} L{R1[0]} {R1[1]} L{R0[0]} {R0[1]}z" fill="#ffd27a" opacity=".12" filter="url(#b24)"/>'
    lad += rail(L0, L1) + rail(R0, R1)
    for k in range(1, 16):
        u = 1 - .73 ** k
        a, c = lerp(L0, L1, u), lerp(R0, R1, u); w = 34 * (1 - u) ** 1.4 + 3
        lad += f'<path d="M{a[0]:.1f} {a[1]:.1f} L{c[0]:.1f} {c[1]:.1f}" stroke="#2a1a08" stroke-width="{w + 6:.1f}" stroke-linecap="round" opacity="{1 - u * .55:.2f}"/>'
        lad += f'<path d="M{a[0]:.1f} {a[1]:.1f} L{c[0]:.1f} {c[1]:.1f}" stroke="#f2c25a" stroke-width="{w:.1f}" stroke-linecap="round" opacity="{1 - u * .45:.2f}"/>'
        lad += f'<path d="M{a[0]:.1f} {a[1] - w * .25:.1f} L{c[0]:.1f} {c[1] - w * .25:.1f}" stroke="#fff6d0" stroke-width="{w * .3:.1f}" stroke-linecap="round" opacity="{.9 - u * .5:.2f}"/>'
        if k == 1:   # the first rung glows (Type One), just out of reach
            lad = (lad + f'<path d="M{a[0]:.1f} {a[1]:.1f} L{c[0]:.1f} {c[1]:.1f}" stroke="#ffe7a8" stroke-width="{w + 40:.0f}" opacity=".85" filter="url(#b12)" stroke-linecap="round"/>'
                   + f'<path d="M{a[0]:.1f} {a[1]:.1f} L{c[0]:.1f} {c[1]:.1f}" stroke="#fff3c0" stroke-width="{w:.1f}" stroke-linecap="round"/>')
    # ---- Earth's horizon (night side, city lights, dawn on the left) ----
    b += f'<circle cx="{EX}" cy="{EY}" r="{ER + 8}" fill="#7fd8ff" opacity=".55" filter="url(#b12)"/>'
    b += f'<circle cx="{EX}" cy="{EY}" r="{ER}" fill="url(#earth)"/>'
    b += '<rect width="1080" height="1920" fill="url(#dawn)"/>'
    for _ in range(320):
        x = rnd.uniform(-20, 1100); top = EY - math.sqrt(max(0, ER ** 2 - (x - EX) ** 2))
        y = rnd.uniform(top + 10, top + 260)
        b += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{rnd.uniform(1.2, 3):.1f}" fill="#ffd98a" opacity="{rnd.uniform(.35, .9):.2f}"/>'
    for _ in range(14):
        x = rnd.uniform(0, 1080); top = EY - math.sqrt(max(0, ER ** 2 - (x - EX) ** 2)); y = top + rnd.uniform(40, 230)
        b += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{rnd.uniform(14, 28):.0f}" fill="#ffc86a" opacity=".3" filter="url(#b6)"/>'
    b += '<rect width="1080" height="1920" fill="url(#txtBg)"/>'
    b += '<ellipse cx="540" cy="1630" rx="300" ry="24" fill="#000" opacity=".5" filter="url(#b6)"/>' + lad
    for (x, y) in (L0, R0):
        b += f'<rect x="{x - 24}" y="{y - 10}" width="48" height="20" rx="6" fill="#6a4a20" stroke="#2a1a08" stroke-width="4"/>'
    # headlamp beam up the ladder
    b += '<path d="M548 1380 L640 1000 L860 1060z" fill="url(#beam)" opacity=".8" filter="url(#b6)"/>'
    # frog at the base, stretching for the first rung
    b += frog(540, 1632, 2.6, look=(3, -7), mouth='O', armL='M-34 -22 q-14 -40 -6 -86', armR='M38 -22 q14 -40 6 -88',
              legs=((-20, -6, -26, 2, -8), (20, -6, 26, 2, 8)), brows=False, shadow=True, front=climb_helmet())
    b += spark(200, 180, 18) + spark(980, 900, 16) + spark(120, 640, 14) + spark(1000, 1420, 14) + spark(160, 1300, 12)
    b += '<rect width="1080" height="1920" fill="url(#vig)"/>'
    lines = [('TYPE <span class="g">0.7</span>', 212, 'w'), ('LONG WAY UP', 124, 'w')]
    return vpage('#0a0c2c', vsvg(d, b), lines, outline='#060820', top=800)


open(os.path.join(HERE, 'A.html'), 'w').write(make())
print('ok')
