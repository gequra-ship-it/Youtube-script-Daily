# Shorts thumbnails for quantum-god-short1..5 (guideline 16-9, brief tools/briefs/thumb_art.md "Shorts thumbnails").
# Run: python3 videos/quantum-god-short1/thumb/make.py   -> writes videos/quantum-god-shortN/thumb/A.html (+ common.css, font) for N=1..5
# 1  BOTH / SLITS / AT ONCE?        intuitive: electron gun -> two slits -> striped screen; frog's thought bubble = two plain bars (S04 "as if", S02-S03)
# 2  WAS / EINSTEIN / WRONG?        intuitive: Bell test, source in the middle, two polarizer detector stations (S01 "nobody knew", S06)
# 3  NOTHING IS / NEVER / NOTHING   intuitive: an "empty" bell jar seething with popping particle pairs, frog with magnifier (S01, S05-S06)
# 4  MORE THAN / ONE / REALITY?     intuitive: sealed lab box (Wigner's friend) with a branching trunk of worlds (S01, S03-S05)
# 5  IT FROM / BIT?                 intuitive: a moon dissolving into glowing 0/1 cubes (S08-S09, Wheeler's phrase, kept as a question)
import os, sys, math, random, shutil
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '../../..'))
sys.path.insert(0, os.path.join(REPO, 'tools'))
from thumb_lib import page, svg, lin, rad, spark

INK = '#1d2b1c'; GREEN = '#6aa55a'
FILTERS = ''.join(f'<filter id="b{s}" x="-60%" y="-60%" width="220%" height="220%"><feGaussianBlur stdDeviation="{s}"/></filter>'
                  for s in (2, 3, 6, 12, 24, 50, 90))
BODY = 'M-34 0 q-6 -64 34 -70 q40 -2 42 62 q0 10 -6 12 q-36 6 -70 -4z'


def lina(id, stops, x1=0, y1=0, x2=0, y2=1):
    return f'<linearGradient id="{id}" x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}">' + ''.join(
        f'<stop offset="{o}" stop-color="{c}" stop-opacity="{a}"/>' for o, c, a in stops) + '</linearGradient>'


def stars(n, x0, y0, x1, y1, col='#e8f4ff', omax=.8):
    return ''.join(f'<circle cx="{random.uniform(x0, x1):.0f}" cy="{random.uniform(y0, y1):.0f}" r="{random.choice([1.1, 1.6, 2.2, 2.8]):.1f}" '
                   f'fill="{col}" opacity="{random.uniform(.15, omax):.2f}"/>' for _ in range(n))


def lerp(a, b, t):
    return (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t)


def pts(*p):
    return ' '.join(f'{x:.1f},{y:.1f}' for x, y in p)


# ---------------- mascot frog (same body as tools/assets/frog.svg and the quantum-god long thumbnails) ----------------
def frog(x, y, s, mouth='o', arms='down', look=(2, 0), outfit='', flip=False, rim=None):
    sx = -s if flip else s
    g = f'<g transform="translate({x} {y}) scale({sx:.2f} {s:.2f})" stroke="{INK}" stroke-linejoin="round" stroke-linecap="round">'
    g += '<ellipse cx="-22" cy="4" rx="16" ry="9" fill="#4d8a4a" stroke-width="3.2"/><ellipse cx="22" cy="4" rx="16" ry="9" fill="#4d8a4a" stroke-width="3.2"/>'
    g += f'<path d="{BODY}" fill="{GREEN}" stroke-width="4"/>'
    g += '<ellipse cx="2" cy="-12" rx="22" ry="20" fill="#9cc98a" stroke="none" opacity=".7"/>'
    g += '<path d="M-26 -50 q6 -16 22 -18" fill="none" stroke="#b9e0a6" stroke-width="3" opacity=".7"/>'
    if rim:   # coloured rim light on the side facing the scene's light
        g += f'<path d="M36 -56 q8 22 6 50" fill="none" stroke="{rim}" stroke-width="3.6" opacity=".9"/>'
    if outfit == 'coat':    # open white lab coat + collar
        g += '<path d="M-31 -38 L-6 -30 L-12 3 L-35 0 Q-40 -20 -31 -38 Z" fill="#eef2f6" stroke-width="3"/>'
        g += '<path d="M36 -38 L14 -30 L20 3 L41 -2 Q44 -20 36 -38 Z" fill="#eef2f6" stroke-width="3"/>'
        g += '<path d="M-6 -30 L4 -20 L14 -30" fill="none" stroke-width="2.4"/><rect x="24" y="-22" width="10" height="7" rx="1.5" fill="#cfd8e2" stroke-width="1.8"/>'
        g += '<path d="M27 -24 l0 -6" stroke="#3a7bd5" stroke-width="2.2"/>'
    if outfit == 'headset':
        pass
    dx, dy = look
    g += f'<circle cx="-10" cy="-66" r="13" fill="#e3e5d6" stroke-width="3.2"/><circle cx="{-10 + dx}" cy="{-66 + dy}" r="5" fill="{INK}" stroke="none"/>'
    g += f'<circle cx="22" cy="-66" r="13" fill="#e3e5d6" stroke-width="3.2"/><circle cx="{22 + dx}" cy="{-66 + dy}" r="5" fill="{INK}" stroke="none"/>'
    g += f'<circle cx="{-8 + dx}" cy="{-68 + dy}" r="1.7" fill="#fff" stroke="none"/><circle cx="{24 + dx}" cy="{-68 + dy}" r="1.7" fill="#fff" stroke="none"/>'
    g += '<ellipse cx="-18" cy="-46" rx="5" ry="3" fill="#e98a8a" stroke="none" opacity=".55"/><ellipse cx="30" cy="-46" rx="5" ry="3" fill="#e98a8a" stroke="none" opacity=".55"/>'
    if mouth == 'o':
        g += '<ellipse cx="6" cy="-42" rx="6.5" ry="8" fill="#7a2f33" stroke-width="3"/><ellipse cx="6" cy="-38" rx="3.5" ry="2.6" fill="#e07b7b" stroke="none"/>'
    else:
        g += '<path d="M-8 -45 q14 14 28 0 q-14 4 -28 0z" fill="#7a2f33" stroke-width="3"/>'
    A = {'down': ('M-34 -22 q-14 6 -16 22', 'M38 -22 q14 6 16 22'),
         'reach': ('M-34 -22 q-14 6 -16 22', 'M38 -24 q22 -6 30 -34'),
         'up': ('M-34 -24 q-20 -6 -24 -36', 'M38 -24 q20 -6 24 -36'),
         'hold': ('M-34 -22 q-14 6 -16 22', 'M38 -24 q18 2 30 -10'),
         'lens': ('M-34 -22 q-14 6 -16 22', 'M38 -26 q20 -4 26 -26')}[arms]
    for d in A:
        g += f'<path d="{d}" fill="none" stroke-width="7.5"/><path d="{d}" fill="none" stroke="{GREEN}" stroke-width="3.4"/>'
    if outfit == 'goggles':  # lab goggles pushed up over the eyes + strap
        g += '<path d="M-30 -70 Q6 -84 42 -70" fill="none" stroke="#2a3346" stroke-width="5"/>'
        for ex in (-10, 22):
            g += f'<rect x="{ex - 16}" y="-82" width="32" height="30" rx="12" fill="#bff3ff" fill-opacity=".22" stroke="#2a3346" stroke-width="3.6"/>'
            g += f'<path d="M{ex - 10} -76 q4 -3 9 -3" fill="none" stroke="#fff" stroke-width="2.4" opacity=".9"/>'
        g += '<path d="M6 -70 l0 6" stroke="#2a3346" stroke-width="4"/>'
    if outfit == 'headset':
        g += '<path d="M-26 -60 C-30 -104 42 -104 38 -60" fill="none" stroke="#2a3140" stroke-width="6"/>'
        g += '<ellipse cx="-27" cy="-56" rx="7" ry="11" fill="#3e4a62" stroke-width="3"/><ellipse cx="39" cy="-56" rx="7" ry="11" fill="#3e4a62" stroke-width="3"/>'
        g += '<path d="M40 -48 q6 18 -16 24" fill="none" stroke="#2a3140" stroke-width="3"/><circle cx="23" cy="-24" r="3.6" fill="#ff5a6e" stroke-width="2"/>'
    if outfit == 'visor':    # translucent cyan data visor
        g += '<rect x="-30" y="-80" width="70" height="26" rx="12" fill="#5ff2ff" fill-opacity=".32" stroke="#16304a" stroke-width="3.4"/>'
        g += '<path d="M-22 -74 L28 -74" stroke="#d8fdff" stroke-width="2.2" opacity=".8"/><circle cx="40" cy="-67" r="3.4" fill="#ffd36a" stroke-width="2"/>'
    return g + '</g>'


def write(n, html):
    d = os.path.join(REPO, f'videos/quantum-god-short{n}/thumb'); os.makedirs(d, exist_ok=True)
    for f in ('common.css', 'Fredoka-700.woff2'):
        if not os.path.exists(os.path.join(d, f)):
            shutil.copy(os.path.join(REPO, 'videos/quantum-god/thumb', f), d)
    open(os.path.join(d, 'A.html'), 'w').write(html)


# ============ 1: BOTH SLITS AT ONCE? ============
def t1():
    random.seed(21)
    defs = FILTERS + lin('sk1', [(0, '#040a1c'), (.6, '#08183a'), (1, '#030714')])
    defs += rad('g1', 1660, 500, 760, [(0, '#2fd2ff', .42), (.5, '#1b5fa8', .18), (1, '#040a1c', 0)])
    defs += rad('g2', 1080, 640, 300, [(0, '#9ff6ff', .5), (1, '#9ff6ff', 0)])
    defs += lina('slab', [(0, '#22355a', 1), (1, '#0c1630', 1)], x2=1, y2=0)
    defs += lina('gun', [(0, '#c9d3e6', 1), (.45, '#6c7a98', 1), (1, '#2a3450', 1)])
    defs += lina('cone', [(0, '#bdfbff', .75), (1, '#4fe3ff', .15)], x2=1, y2=0)
    defs += '<clipPath id="wv"><rect x="1112" y="120" width="452" height="820"/></clipPath>'
    b = '<rect width="1920" height="1080" fill="url(#sk1)"/><rect width="1920" height="1080" fill="url(#g1)"/>'
    b += stars(90, 900, 0, 1920, 700, '#cfefff', .5)
    # floor with perspective grid
    b += '<rect y="900" width="1920" height="180" fill="#030611"/>'
    vx, vy = 1150, 640
    for k in range(-14, 22):
        x = 1150 + k * 150
        b += f'<line x1="{lerp((vx, vy), (x, 1080), .29)[0]:.0f}" y1="900" x2="{x}" y2="1080" stroke="#2fd2ff" stroke-width="2" opacity=".14"/>'
    for yy in (916, 942, 980, 1036):
        b += f'<line x1="0" y1="{yy}" x2="1920" y2="{yy}" stroke="#2fd2ff" stroke-width="2" opacity=".12"/>'
    # waves spreading from the two slits (overlap -> interference)
    s1, s2 = (1112, 572), (1112, 712)
    wv = ''
    for (sx_, sy_), col in ((s1, '#9ff6ff'), (s2, '#ffe39a')):
        for r in range(26, 640, 34):
            op = max(0, .62 * (1 - r / 660))
            wv += f'<path d="M{sx_} {sy_ - r} A{r} {r} 0 0 1 {sx_} {sy_ + r}" fill="none" stroke="{col}" stroke-width="3.2" opacity="{op:.2f}"/>'
    b += f'<g clip-path="url(#wv)">{wv}</g>'
    # screen (face turned toward the viewer) with interference fringes
    L0, L1, R0, R1 = (1560, 196), (1560, 806), (1768, 120), (1768, 872)
    b += f'<polygon points="{pts((1536, 206), L0, L1, (1536, 796))}" fill="#0b1426" stroke="#050913" stroke-width="5"/>'
    b += f'<polygon points="{pts(L0, R0, R1, L1)}" fill="#08111f" stroke="#050913" stroke-width="10"/>'
    fr = ''; N = 90
    for i in range(N):
        v0, v1 = i / N, (i + 1) / N; v = (v0 + v1) / 2
        I = math.cos(math.pi * 4.5 * (v - .5)) ** 2 * math.exp(-((v - .5) / .33) ** 2)
        if I < .03:
            continue
        p = (lerp(L0, L1, v0), lerp(R0, R1, v0), lerp(R0, R1, v1), lerp(L0, L1, v1))
        fr += f'<polygon points="{pts(*p)}" fill="#c8fbff" opacity="{I:.2f}"/>'
    b += f'<g filter="url(#b12)" opacity=".9">{fr}</g>' + fr
    hits = ''
    while hits.count('<circle') < 170:
        v = random.random(); I = math.cos(math.pi * 4.5 * (v - .5)) ** 2 * math.exp(-((v - .5) / .33) ** 2)
        if random.random() < I:
            u = random.uniform(.06, .94); a = lerp(L0, R0, u); c = lerp(L1, R1, u); p = lerp(a, c, v)
            hits += f'<circle cx="{p[0]:.0f}" cy="{p[1]:.0f}" r="{random.choice([2.2, 3, 3.8])}" fill="#ffffff" opacity="{random.uniform(.5, 1):.2f}"/>'
    b += hits
    b += f'<polygon points="{pts(L0, R0, R1, L1)}" fill="none" stroke="#7fe8ff" stroke-width="3" opacity=".55"/>'
    b += '<path d="M1768 130 L1768 862" stroke="#bff7ff" stroke-width="4" opacity=".6"/>'
    b += '<path d="M1600 860 L1590 906 M1730 878 L1744 906" stroke="#0b1426" stroke-width="14" stroke-linecap="round"/>'
    # barrier slab with two slits
    b += '<rect x="1040" y="640" width="1" height="1" fill="url(#g2)"/>'
    b += '<circle cx="1090" cy="642" r="260" fill="url(#g2)"/>'
    for y0, y1 in ((236, 560), (584, 700), (724, 900)):
        b += f'<rect x="1040" y="{y0}" width="72" height="{y1 - y0}" fill="url(#slab)" stroke="#050913" stroke-width="5"/>'
    b += '<polygon points="1040,236 1112,236 1140,214 1068,214" fill="#3a5482" stroke="#050913" stroke-width="5"/>'
    b += '<polygon points="1112,236 1140,214 1140,880 1112,900" fill="#14213f" stroke="#050913" stroke-width="5"/>'
    b += '<path d="M1110 240 L1110 556 M1110 588 L1110 696 M1110 728 L1110 896" stroke="#7fe8ff" stroke-width="3" opacity=".7"/>'
    for yy in (572, 712):
        b += f'<rect x="1030" y="{yy - 12}" width="96" height="24" rx="10" fill="#dffcff" filter="url(#b6)"/><rect x="1040" y="{yy - 8}" width="72" height="16" fill="#f4feff"/>'
    # beam of electrons from the gun into the barrier
    b += '<polygon points="900,770 1042,548 1042,736 900,800" fill="url(#cone)" filter="url(#b6)" opacity=".85"/>'
    for t in (.12, .3, .47, .63, .8, .93):
        p = lerp((905, 785), (1040, 642), t)
        b += f'<circle cx="{p[0]:.0f}" cy="{p[1]:.0f}" r="13" fill="#9ff6ff" filter="url(#b6)"/><circle cx="{p[0]:.0f}" cy="{p[1]:.0f}" r="6" fill="#fff"/>'
    # electron gun on a tripod (tilted up toward the slits)
    g = '<g transform="rotate(-24 830 800)">'
    g += '<rect x="700" y="768" width="170" height="64" rx="20" fill="url(#gun)" stroke="#0b1022" stroke-width="5"/>'
    for xx in (730, 756, 782):
        g += f'<rect x="{xx}" y="762" width="12" height="76" rx="5" fill="#d98a3a" stroke="#0b1022" stroke-width="3.5"/>'
    g += '<polygon points="868,778 906,788 906,812 868,822" fill="#4a5674" stroke="#0b1022" stroke-width="4"/>'
    g += '<circle cx="908" cy="800" r="16" fill="#bff7ff" filter="url(#b6)"/><circle cx="906" cy="800" r="7" fill="#fff"/>'
    g += '<circle cx="826" cy="786" r="7" fill="#5fffb0" stroke="#0b1022" stroke-width="2.5"/>'
    g += '<path d="M708 780 q60 -6 156 -4" fill="none" stroke="#fff" stroke-width="3.5" opacity=".5"/></g>'
    b += '<path d="M790 812 L740 920 M800 812 L842 922 M796 812 L796 930" stroke="#1a2238" stroke-width="10" stroke-linecap="round"/>'
    b += '<path d="M790 812 L740 920 M800 812 L842 922" stroke="#56658a" stroke-width="3" stroke-linecap="round" opacity=".7"/>'
    b += g
    b += '<ellipse cx="796" cy="930" rx="80" ry="12" fill="#000" opacity=".5"/>'
    # frog in goggles + lab coat; thought bubble = what common sense expected: two plain bars
    b += '<ellipse cx="470" cy="1030" rx="120" ry="16" fill="#000" opacity=".5"/>'
    b += frog(470, 1022, 3.2, mouth='o', arms='up', look=(6, -3), outfit='goggles', rim='#9ff6ff')
    b += '<circle cx="612" cy="762" r="10" fill="#eaf4ff" stroke="#0b1022" stroke-width="4"/><circle cx="640" cy="726" r="15" fill="#eaf4ff" stroke="#0b1022" stroke-width="4"/>'
    b += '<ellipse cx="712" cy="640" rx="88" ry="66" fill="#eaf4ff" stroke="#0b1022" stroke-width="5"/>'
    b += '<rect x="676" y="598" width="22" height="84" rx="4" fill="#3a6fd8"/><rect x="726" y="598" width="22" height="84" rx="4" fill="#3a6fd8"/>'
    b += spark(1230, 330, 20, '#dffcff') + spark(1440, 980 - 120, 14) + spark(980, 420, 16, '#dffcff') + spark(1840, 70, 16)
    lines = [('BOTH', 228, 'y'), ('SLITS', 168, 'w'), ('AT ONCE?', 148, 'w')]
    return page('#040a1c', svg(defs, b), lines, outline='#030714')


# ============ 2: WAS EINSTEIN WRONG? (Bell test) ============
def station(x, y, s, face_left, lamp, bcol):
    """polarizer disk + detector box; centred on the beam axis at (x, y); faces the source on the other side"""
    f = -1 if face_left else 1
    g = f'<g transform="translate({x} {y}) scale({f * s:.2f} {s:.2f})" stroke="#061014" stroke-linejoin="round">'
    # stand
    g += '<path d="M40 60 L40 170 M0 170 L80 170" stroke="#1c2c34" stroke-width="16" stroke-linecap="round"/>'
    # detector body (box) behind the disk
    g += '<rect x="20" y="-70" width="170" height="130" rx="14" fill="#2c4250" stroke-width="6"/>'
    g += '<rect x="20" y="-70" width="170" height="24" rx="10" fill="#4f6d7c" stroke="none"/>'
    g += '<rect x="80" y="-30" width="86" height="46" rx="6" fill="#06161c" stroke-width="4"/>'
    for k, hh in enumerate((18, 32, 12, 26, 38)):
        g += f'<rect x="{88 + k * 15}" y="{12 - hh}" width="10" height="{hh}" fill="{bcol}" stroke="none" opacity=".9"/>'
    g += f'<circle cx="120" cy="-92" r="18" fill="{lamp}" stroke-width="5"/><rect x="108" y="-80" width="24" height="12" fill="#1c2c34" stroke-width="4"/>'
    g += f'<circle cx="120" cy="-92" r="40" fill="{lamp}" stroke="none" opacity=".35" filter="url(#b12)"/>'
    # input tube + polarizer disk (rotatable dial with ticks)
    g += '<rect x="-30" y="-26" width="56" height="52" fill="#3c5664" stroke-width="5"/>'
    g += '<ellipse cx="-34" cy="0" rx="26" ry="74" fill="#1a2a32" stroke-width="6"/>'
    g += '<ellipse cx="-40" cy="0" rx="20" ry="62" fill="#8fd8e8" fill-opacity=".35" stroke="#d8f6ff" stroke-width="3"/>'
    for k in range(-5, 6):
        g += f'<line x1="{-46 + abs(k) * 1.2:.1f}" y1="{k * 10}" x2="{-34 + abs(k) * 1.2:.1f}" y2="{k * 10 - 4}" stroke="#e8fbff" stroke-width="2" opacity=".7"/>'
    for k in range(12):
        a = k * math.pi / 6
        g += f'<line x1="{-34 + 26 * math.cos(a) * .95:.1f}" y1="{74 * math.sin(a) * .95:.1f}" x2="{-34 + 26 * math.cos(a) * .8:.1f}" y2="{74 * math.sin(a) * .8:.1f}" stroke="#ffd36a" stroke-width="3"/>'
    g += '<path d="M-34 -74 l-8 -16 l16 0 z" fill="#ffd36a" stroke-width="3"/>'
    return g + '</g>'


def photon_path(a, b, amp, waves, phase=0):
    (x0, y0), (x1, y1) = a, b
    L = math.hypot(x1 - x0, y1 - y0); ux, uy = (x1 - x0) / L, (y1 - y0) / L; nx, ny = -uy, ux
    d = ''
    for i in range(121):
        t = i / 120; w = amp * math.sin(2 * math.pi * waves * t + phase)
        d += ('M' if i == 0 else 'L') + f'{x0 + ux * L * t + nx * w:.1f} {y0 + uy * L * t + ny * w:.1f} '
    return d


def t2():
    random.seed(32)
    defs = FILTERS + lin('sk2', [(0, '#03161c'), (.55, '#072a30'), (1, '#020a0d')])
    defs += rad('g3', 1190, 610, 520, [(0, '#ff7ae0', .55), (.35, '#8a4dff', .2), (1, '#03161c', 0)])
    defs += rad('core', 1190, 610, 90, [(0, '#ffffff', 1), (.4, '#ffd6f4', .9), (1, '#ff7ae0', 0)])
    defs += lina('tbl', [(0, '#1b3a42', 1), (1, '#071418', 1)])
    b = '<rect width="1920" height="1080" fill="url(#sk2)"/>'
    b += stars(120, 820, 0, 1920, 560, '#d6fff6', .45)
    # optical table in perspective
    b += '<polygon points="300,760 1920,470 1920,1080 0,1080 0,860" fill="url(#tbl)"/>'
    b += '<polygon points="300,760 1920,470 1920,486 300,778" fill="#3f7480" opacity=".7"/>'
    for i in range(1, 30):
        for j in range(1, 14):
            u, v = i / 30, j / 14
            top = lerp((300, 778), (1920, 486), u); bot = lerp((-300, 1080), (2400, 1080), u)
            p = lerp(top, bot, v ** 1.25)
            r = 1.6 + 3.2 * v
            b += f'<circle cx="{p[0]:.0f}" cy="{p[1]:.0f}" r="{r:.1f}" fill="#020a0d" opacity=".75"/>'
    b += '<rect width="1920" height="1080" fill="url(#g3)"/>'
    A, S, B = (690, 808), (1190, 610), (1640, 432)
    # entangled photon beams (two wave trains leaving the source in opposite directions)
    for (p, q, col) in ((S, A, '#ffd36a'), (S, B, '#ffd36a')):
        b += f'<path d="M{p[0]} {p[1]} L{q[0]} {q[1]}" stroke="{col}" stroke-width="22" opacity=".22" filter="url(#b12)"/>'
        b += f'<path d="{photon_path(p, q, 16, 7)}" fill="none" stroke="{col}" stroke-width="7" opacity=".95" filter="url(#b3)"/>'
        b += f'<path d="{photon_path(p, q, 16, 7)}" fill="none" stroke="#fffbe8" stroke-width="2.6"/>'
    for (p, q) in ((S, A), (S, B)):
        for t in (.36, .7):
            c = lerp(p, q, t)
            b += f'<circle cx="{c[0]:.0f}" cy="{c[1]:.0f}" r="30" fill="#ffd36a" opacity=".5" filter="url(#b12)"/><circle cx="{c[0]:.0f}" cy="{c[1]:.0f}" r="10" fill="#fffbe8"/>'
    # violet pump laser coming in from behind
    b += '<path d="M1190 610 L1520 140" stroke="#a46bff" stroke-width="16" opacity=".35" filter="url(#b6)"/><path d="M1190 610 L1520 140" stroke="#e0ccff" stroke-width="4" opacity=".8"/>'
    b += '<rect x="1490" y="96" width="90" height="56" rx="10" transform="rotate(-55 1535 124)" fill="#28323c" stroke="#061014" stroke-width="5"/>'
    # source crystal on a post
    b += '<path d="M1190 650 L1190 760" stroke="#1c2c34" stroke-width="18" stroke-linecap="round"/><ellipse cx="1190" cy="764" rx="40" ry="10" fill="#0a1a20"/>'
    b += '<circle cx="1190" cy="610" r="210" fill="url(#g3)"/>'
    b += '<polygon points="1160,580 1206,566 1226,606 1196,650 1156,636" fill="#ffc2f0" stroke="#3a0f36" stroke-width="5"/>'
    b += '<polygon points="1160,580 1206,566 1196,604" fill="#fff" opacity=".7"/><polygon points="1196,604 1226,606 1196,650" fill="#d65cc4" opacity=".55"/>'
    b += '<circle cx="1190" cy="610" r="90" fill="url(#core)" opacity=".75"/>'
    # two detector stations
    b += station(1652, 432, .9, False, '#5fffb0', '#5fffb0')
    b += station(676, 808, 1.22, True, '#ff6a7e', '#ffd36a')
    # frog operator in a headset behind the near station, looking at the far one
    b += '<ellipse cx="360" cy="1022" rx="110" ry="15" fill="#000" opacity=".5"/>'
    b += frog(360, 1014, 3.05, mouth='o', arms='reach', look=(7, -5), outfit='headset', rim='#ffd36a')
    b += spark(1400, 300, 18) + spark(960, 470, 14, '#ffd6f4') + spark(1820, 250, 16) + spark(1310, 760, 14)
    lines = [('WAS', 150, 'w'), ('EINSTEIN', 186, 'w'), ('WRONG?', 214, 'y')]
    return page('#03161c', svg(defs, b), lines, outline='#020a0d')


# ============ 3: NOTHING IS NEVER NOTHING (vacuum fluctuations) ============
def pair(cx, cy, r, ang, op, c1='#ff9b3d', c2='#3ee8ff'):
    a = math.radians(ang); dx, dy = math.cos(a) * r, math.sin(a) * r
    o = f'<g opacity="{op:.2f}">'
    o += f'<ellipse cx="{cx}" cy="{cy}" rx="{r * 1.15:.1f}" ry="{r * .55:.1f}" transform="rotate({ang} {cx} {cy})" fill="none" stroke="#fff3d6" stroke-width="{max(1.6, r / 9):.1f}" stroke-dasharray="{r / 3:.1f} {r / 5:.1f}" opacity=".7"/>'
    for (px, py, c) in ((cx + dx, cy + dy, c1), (cx - dx, cy - dy, c2)):
        o += f'<circle cx="{px:.1f}" cy="{py:.1f}" r="{r * .9:.1f}" fill="{c}" opacity=".5" filter="url(#b6)"/>'
        o += f'<circle cx="{px:.1f}" cy="{py:.1f}" r="{r * .46:.1f}" fill="{c}" stroke="#1a0c06" stroke-width="{max(1.5, r / 12):.1f}"/>'
        o += f'<circle cx="{px - r * .14:.1f}" cy="{py - r * .16:.1f}" r="{r * .14:.1f}" fill="#fff" opacity=".85"/>'
    o += spark(cx, cy, r * .55, '#ffffff', .95)
    return o + '</g>'


def t3():
    random.seed(43)
    defs = FILTERS + lin('sk3', [(0, '#0a0610'), (.6, '#170a1c'), (1, '#05030a')])
    defs += rad('g4', 1250, 520, 560, [(0, '#ff6a3d', .30), (.5, '#9b2a6a', .14), (1, '#0a0610', 0)])
    defs += lina('glass', [(0, '#bfe9ff', .16), (.5, '#bfe9ff', .03), (1, '#bfe9ff', .14)], x2=1, y2=0)
    defs += lina('brass', [(0, '#f3c46a', 1), (.5, '#a86b26', 1), (1, '#4a2a10', 1)])
    defs += '<clipPath id="jar"><path d="M985 860 L985 420 C985 220 1105 140 1260 140 C1415 140 1535 220 1535 420 L1535 860 Z"/></clipPath>'
    defs += rad('lensg', 980, 690, 92, [(0, '#ffffff', .25), (1, '#bfe9ff', .05)])
    b = '<rect width="1920" height="1080" fill="url(#sk3)"/>'
    b += stars(70, 900, 0, 1920, 600, '#ffe8d6', .35)
    # table
    b += '<polygon points="0,930 1920,900 1920,1080 0,1080" fill="#120a0c"/><polygon points="0,930 1920,900 1920,912 0,944" fill="#3a1f1a"/>'
    b += '<rect width="1920" height="1080" fill="url(#g4)"/>'
    # inside: seething vacuum (faint foam + popping pairs)
    inner = ''
    for _ in range(60):
        x, y = random.uniform(1000, 1520), random.uniform(160, 850)
        inner += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{random.uniform(20, 70):.0f}" fill="{random.choice(["#ff6a3d", "#3ee8ff", "#ff5fc8"])}" opacity="{random.uniform(.04, .1):.2f}" filter="url(#b24)"/>'
    for _ in range(260):
        x, y = random.uniform(1000, 1520), random.uniform(170, 850)
        inner += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{random.choice([1.4, 2, 2.6])}" fill="#fff3d6" opacity="{random.uniform(.15, .7):.2f}"/>'
    P = [(1260, 470, 46, -20, 1), (1120, 300, 26, 35, .85), (1420, 300, 30, -50, .9), (1400, 640, 38, 15, 1), (1110, 600, 30, 60, .9),
         (1270, 740, 24, -35, .8), (1180, 200, 16, 0, .6), (1340, 210, 14, 70, .55), (1480, 470, 18, 80, .7), (1050, 440, 16, -60, .6),
         (1300, 330, 14, 120, .5), (1200, 820, 14, 20, .5), (1470, 800, 16, -10, .6), (1060, 760, 12, 40, .5), (1350, 545, 12, 0, .45)]
    for (x, y, r, a, op) in P:
        inner += pair(x, y, r, a, op)
    b += f'<g clip-path="url(#jar)">{inner}</g>'
    # vacuum pipe to the left + pump knob
    b += '<path d="M985 880 L900 880 L900 960" fill="none" stroke="#1a0e08" stroke-width="30" stroke-linecap="round"/><path d="M985 880 L900 880 L900 960" fill="none" stroke="#b07a34" stroke-width="18" stroke-linecap="round"/>'
    # bell jar glass
    jar = 'M985 860 L985 420 C985 220 1105 140 1260 140 C1415 140 1535 220 1535 420 L1535 860'
    b += f'<path d="{jar} Z" fill="url(#glass)"/>'
    b += f'<path d="{jar}" fill="none" stroke="#0d1620" stroke-width="12"/><path d="{jar}" fill="none" stroke="#d8f4ff" stroke-width="4" opacity=".7"/>'
    b += '<path d="M1030 760 L1030 430 C1030 300 1100 210 1190 190" fill="none" stroke="#fff" stroke-width="14" opacity=".28" stroke-linecap="round"/>'
    b += '<path d="M1060 430 C1060 330 1110 260 1170 236" fill="none" stroke="#fff" stroke-width="6" opacity=".5" stroke-linecap="round"/>'
    b += '<path d="M1500 720 L1500 470" fill="none" stroke="#fff" stroke-width="6" opacity=".25" stroke-linecap="round"/>'
    b += '<ellipse cx="1260" cy="130" rx="44" ry="14" fill="#2a1a12" stroke="#0d0806" stroke-width="5"/><rect x="1236" y="96" width="48" height="36" rx="8" fill="url(#brass)" stroke="#0d0806" stroke-width="5"/>'
    # brass base plate
    b += '<ellipse cx="1260" cy="880" rx="320" ry="46" fill="#2a160a" stroke="#0d0806" stroke-width="6"/>'
    b += '<path d="M940 868 L940 900 A320 46 0 0 0 1580 900 L1580 868" fill="url(#brass)" stroke="#0d0806" stroke-width="6"/>'
    b += '<ellipse cx="1260" cy="866" rx="320" ry="44" fill="url(#brass)" stroke="#0d0806" stroke-width="6"/>'
    b += '<ellipse cx="1260" cy="862" rx="282" ry="32" fill="none" stroke="#ffe2a0" stroke-width="3" opacity=".7"/>'
    # frog with a magnifying glass at the jar wall
    b += '<ellipse cx="770" cy="1030" rx="120" ry="15" fill="#000" opacity=".55"/>'
    b += frog(770, 1022, 3.1, mouth='o', arms='lens', look=(7, -4), rim='#ff9b3d')
    b += '<path d="M874 942 L930 780" stroke="#1a0e08" stroke-width="22" stroke-linecap="round"/><path d="M874 942 L930 780" stroke="#8a4a1e" stroke-width="12" stroke-linecap="round"/>'
    b += '<circle cx="980" cy="690" r="96" fill="#0d0806"/>'
    b += f'<circle cx="980" cy="690" r="82" fill="#1a0c14"/>'
    b += '<g transform="translate(980 690) scale(1.7) translate(-1040 -655)" opacity="1">' + pair(1040, 655, 22, 30, 1) + '</g>'
    b += '<circle cx="980" cy="690" r="82" fill="url(#lensg)"/><path d="M928 646 A70 70 0 0 1 990 618" fill="none" stroke="#fff" stroke-width="7" opacity=".7" stroke-linecap="round"/>'
    b += '<circle cx="980" cy="690" r="88" fill="none" stroke="url(#brass)" stroke-width="14"/><circle cx="980" cy="690" r="96" fill="none" stroke="#0d0806" stroke-width="4"/>'
    b += spark(1600, 260, 18) + spark(930, 250 + 200, 12, '#ffe8d6') + spark(1700, 560, 14) + spark(1560, 120, 12)
    lines = [('NOTHING IS', 152, 'w'), ('NEVER', 236, 'y'), ('NOTHING', 172, 'w')]
    return page('#0a0610', svg(defs, b), lines, outline='#05030a')


# ============ 4: MORE THAN ONE REALITY? (many worlds from Wigner's sealed lab) ============
def branches(x, y, ang, L, w, depth, out, tips):
    a = math.radians(ang)
    x2, y2 = x + math.sin(a) * L, y - math.cos(a) * L
    cx, cy = x + math.sin(a + .25) * L * .5, y - math.cos(a + .25) * L * .5
    out.append((depth, f'M{x:.0f} {y:.0f} Q{cx:.0f} {cy:.0f} {x2:.0f} {y2:.0f}', w))
    if depth == 0:
        tips.append((x2, y2)); return
    spread = random.uniform(30, 40)
    for s in (-1, 1):
        na = ang + s * spread + random.uniform(-6, 6)
        na = max(-20, min(112, na))   # keep the crown up-right, away from the text
        branches(x2, y2, na, L * random.uniform(.8, .9), w * .68, depth - 1, out, tips)


def t4():
    random.seed(54)
    defs = FILTERS + lin('sk4', [(0, '#041218'), (.55, '#08262a'), (1, '#030a0e')])
    defs += rad('g5', 1330, 380, 720, [(0, '#ffd36a', .26), (.45, '#2fbf8f', .12), (1, '#041218', 0)])
    defs += lina('boxL', [(0, '#5d6b78', 1), (1, '#2b343e', 1)])
    defs += lina('boxR', [(0, '#3b4652', 1), (1, '#1a2028', 1)])
    b = '<rect width="1920" height="1080" fill="url(#sk4)"/><rect width="1920" height="1080" fill="url(#g5)"/>'
    b += stars(200, 860, 0, 1920, 800, '#e6fff6', .6)
    b += '<polygon points="0,900 1920,860 1920,1080 0,1080" fill="#03090c"/><path d="M0 900 L1920 860" stroke="#2fbf8f" stroke-width="3" opacity=".3"/>'
    # branching trunk of worlds
    random.seed(7)
    segs, tips = [], []
    branches(1250, 700, 22, 150, 44, 5, segs, tips)
    tree = ''
    for depth, d, w in sorted(segs):
        tree += f'<path d="{d}" fill="none" stroke="#ffd36a" stroke-width="{w * 2.2:.1f}" opacity=".22" stroke-linecap="round" filter="url(#b12)"/>'
    for depth, d, w in sorted(segs):
        tree += f'<path d="{d}" fill="none" stroke="#1a1206" stroke-width="{w + 6:.1f}" stroke-linecap="round"/>'
    for depth, d, w in sorted(segs):
        tree += f'<path d="{d}" fill="none" stroke="#ffcf5a" stroke-width="{w:.1f}" stroke-linecap="round"/>'
        tree += f'<path d="{d}" fill="none" stroke="#fff6d0" stroke-width="{max(1.5, w * .3):.1f}" stroke-linecap="round" opacity=".85"/>'
    b += tree
    cols = ['#5fd0ff', '#ff7a9a', '#8affc0', '#c59bff', '#ffb35a', '#5ff2e0', '#ff9be8', '#a8e05a']
    for i, (x, y) in enumerate(tips):
        if x > 1870 or y < 40 or (x < 1080 and y < 620) or (x > 1640 and y > 800):
            continue
        r = random.uniform(22, 34); c = cols[i % len(cols)]
        b += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r * 1.9:.0f}" fill="{c}" opacity=".35" filter="url(#b12)"/>'
        b += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r:.0f}" fill="{c}" stroke="#08141a" stroke-width="4"/>'
        b += f'<path d="M{x - r * .8:.0f} {y + r * .1:.0f} q{r * .5:.0f} {-r * .5:.0f} {r * .9:.0f} {-r * .1:.0f} q{r * .3:.0f} {r * .3:.0f} {r * .6:.0f} {-r * .1:.0f}" fill="none" stroke="#08141a" stroke-width="3" opacity=".45"/>'
        b += f'<circle cx="{x - r * .35:.0f}" cy="{y - r * .38:.0f}" r="{r * .22:.0f}" fill="#fff" opacity=".8"/>'
    # sealed lab box (isometric cube)
    cx, cy, s = 1250, 760, 210
    top = ((cx, cy - s * .5), (cx + s, cy - s * .5 + s * .5 * .0), )
    T = [(cx - 230, 700), (cx, 620), (cx + 230, 700), (cx, 780)]
    Lf = [(cx - 230, 700), (cx, 780), (cx, 990), (cx - 230, 910)]
    Rf = [(cx, 780), (cx + 230, 700), (cx + 230, 910), (cx, 990)]
    b += f'<ellipse cx="{cx}" cy="985" rx="300" ry="34" fill="#000" opacity=".55"/>'
    b += f'<polygon points="{pts(*Lf)}" fill="url(#boxL)" stroke="#0a0e12" stroke-width="7"/>'
    b += f'<polygon points="{pts(*Rf)}" fill="url(#boxR)" stroke="#0a0e12" stroke-width="7"/>'
    b += f'<polygon points="{pts(*T)}" fill="#7c8a96" stroke="#0a0e12" stroke-width="7"/>'
    b += f'<polygon points="{pts(*T)}" fill="#ffd36a" opacity=".25"/>'
    for k in (1, 2, 3):   # rivets / panel seams
        p = lerp(Rf[0], Rf[3], k / 4); q = lerp(Rf[1], Rf[2], k / 4)
        b += f'<line x1="{p[0]:.0f}" y1="{p[1]:.0f}" x2="{q[0]:.0f}" y2="{q[1]:.0f}" stroke="#0a0e12" stroke-width="3" opacity=".5"/>'
    # door on the left face (closed), with a glowing round window
    D = [lerp(lerp(Lf[0], Lf[1], .28), lerp(Lf[3], Lf[2], .28), .18), lerp(lerp(Lf[0], Lf[1], .78), lerp(Lf[3], Lf[2], .78), .18),
         lerp(lerp(Lf[0], Lf[1], .78), lerp(Lf[3], Lf[2], .78), 1.0), lerp(lerp(Lf[0], Lf[1], .28), lerp(Lf[3], Lf[2], .28), 1.0)]
    b += f'<polygon points="{pts(*D)}" fill="#46525e" stroke="#0a0e12" stroke-width="6"/>'
    wc = lerp(lerp(D[0], D[1], .5), lerp(D[3], D[2], .5), .3)
    b += f'<ellipse cx="{wc[0]:.0f}" cy="{wc[1]:.0f}" rx="40" ry="46" transform="rotate(-20 {wc[0]:.0f} {wc[1]:.0f})" fill="#ffe49a" stroke="#0a0e12" stroke-width="6"/>'
    b += f'<ellipse cx="{wc[0]:.0f}" cy="{wc[1]:.0f}" rx="70" ry="76" fill="#ffd36a" opacity=".35" filter="url(#b12)"/>'
    b += f'<path d="M{wc[0] - 12:.0f} {wc[1] + 14:.0f} q0 -26 14 -26 q14 0 14 26" fill="#c98a2a" opacity=".55"/><path d="M{wc[0] - 4:.0f} {wc[1] + 18:.0f} q0 -26 14 -26 q14 0 14 26" fill="#8a5a1a" opacity=".35"/>'
    kb = lerp(lerp(D[0], D[1], .82), lerp(D[3], D[2], .82), .6)
    b += f'<circle cx="{kb[0]:.0f}" cy="{kb[1]:.0f}" r="10" fill="#ffd36a" stroke="#0a0e12" stroke-width="4"/>'
    # warning stripes along the top edge (sealed)
    b += f'<path d="M{Lf[0][0] + 8} {Lf[0][1] + 18} L{Lf[1][0] - 4} {Lf[1][1] + 18}" stroke="#ffd36a" stroke-width="10" stroke-dasharray="20 16" opacity=".8"/>'
    # Wigner frog outside the door, lab coat, looking up at the branches
    b += '<ellipse cx="870" cy="1030" rx="120" ry="15" fill="#000" opacity=".55"/>'
    b += frog(870, 1024, 3.1, mouth='o', arms='hold', look=(6, -6), outfit='coat', rim='#ffd36a')
    b += spark(1090, 480, 20) + spark(1700, 760, 16) + spark(950, 300 + 300, 12) + spark(1830, 430, 14)
    lines = [('MORE THAN', 158, 'w'), ('ONE', 250, 'y'), ('REALITY?', 168, 'w')]
    return page('#041218', svg(defs, b), lines, outline='#020a0d')


# ============ 5: IT FROM BIT? (a moon dissolving into 0/1 cubes) ============
def cube(x, y, s, digit, col, op=1.0, rot=0, glow=True):
    h = s * .5
    o = f'<g transform="rotate({rot:.0f} {x:.0f} {y:.0f})" opacity="{op:.2f}" stroke="#04101c" stroke-width="{max(2, s / 14):.1f}" stroke-linejoin="round">'
    if glow:
        o += f'<rect x="{x - s * .9:.0f}" y="{y - s * .9:.0f}" width="{s * 1.8:.0f}" height="{s * 1.8:.0f}" fill="{col}" opacity=".35" filter="url(#b12)" stroke="none"/>'
    o += f'<polygon points="{pts((x - h, y - h * .55), (x, y - h * 1.1), (x + h, y - h * .55), (x, y))}" fill="#e8fdff"/>'
    o += f'<polygon points="{pts((x - h, y - h * .55), (x, y), (x, y + h * 1.05), (x - h, y + h * .5))}" fill="{col}"/>'
    o += f'<polygon points="{pts((x, y), (x + h, y - h * .55), (x + h, y + h * .5), (x, y + h * 1.05))}" fill="#1b6c8a"/>'
    o += (f'<text x="{x - h * .5:.1f}" y="{y + h * .42:.1f}" font-family="Fredoka" font-weight="700" font-size="{s * .6:.0f}" text-anchor="middle" '
          f'fill="#04101c" stroke="none" transform="skewY(29) translate(0 {-(x - h * .5) * math.tan(math.radians(29)):.1f})">{digit}</text>')
    return o + '</g>'


def t5():
    random.seed(65)
    defs = FILTERS + lin('sk5', [(0, '#030818'), (.6, '#071a36'), (1, '#02050f')])
    defs += rad('g6', 1420, 460, 760, [(0, '#2fe6ff', .30), (.5, '#1f4aa8', .14), (1, '#030818', 0)])
    defs += rad('moon', 1180, 400, 520, [(0, '#e9e4d6', 1), (.55, '#a8a294', 1), (1, '#4a4a58', 1)])
    defs += rad('sun', 1840, 120, 340, [(0, '#ffffff', .9), (.2, '#ffe9b0', .5), (1, '#ffd36a', 0)])
    C, R = (1260, 540), 320
    b = '<rect width="1920" height="1080" fill="url(#sk5)"/><rect width="1920" height="1080" fill="url(#g6)"/>'
    b += stars(260, 0, 0, 1920, 1080, '#dff6ff', .7)
    b += '<rect width="1920" height="1080" fill="url(#sun)"/>'
    # moon: solid on the lower left, dissolving into cubes toward the upper right
    cell = 46; removed = []; keep_mask = ''
    for gx in range(int(C[0] - R), int(C[0] + R), cell):
        for gy in range(int(C[1] - R), int(C[1] + R), cell):
            mx, my = gx + cell / 2, gy + cell / 2
            if math.hypot(mx - C[0], my - C[1]) > R + 20:
                continue
            t = ((mx - C[0]) * .8 - (my - C[1]) * .6) / R    # distance along the up-right direction
            if random.random() < (t - .05) * 1.6:
                removed.append((mx, my, t))
                keep_mask += f'<rect x="{gx}" y="{gy}" width="{cell}" height="{cell}" fill="#000"/>'
    defs += f'<mask id="mm"><rect width="1920" height="1080" fill="#fff"/>{keep_mask}</mask>'
    defs += f'<clipPath id="mc"><circle cx="{C[0]}" cy="{C[1]}" r="{R}"/></clipPath>'
    m = f'<circle cx="{C[0]}" cy="{C[1]}" r="{R}" fill="url(#moon)"/>'
    for _ in range(26):
        x = random.uniform(C[0] - R, C[0] + R); y = random.uniform(C[1] - R, C[1] + R); r = random.uniform(10, 46)
        m += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r:.0f}" fill="#6e6a64" opacity=".45"/><path d="M{x - r * .8:.0f} {y + r * .3:.0f} A{r:.0f} {r:.0f} 0 0 0 {x + r * .8:.0f} {y + r * .3:.0f}" fill="none" stroke="#f6f2e6" stroke-width="3" opacity=".45"/>'
    m += f'<circle cx="{C[0] - 120}" cy="{C[1] + 140}" r="{R}" fill="#0a1024" opacity=".35"/>'   # terminator shade lower-left
    # grid seams glowing on the moon near the edge of dissolution
    for gx in range(int(C[0] - R), int(C[0] + R), cell):
        m += f'<line x1="{gx}" y1="{C[1] - R}" x2="{gx}" y2="{C[1] + R}" stroke="#5ff2ff" stroke-width="2" opacity=".22"/>'
    for gy in range(int(C[1] - R), int(C[1] + R), cell):
        m += f'<line x1="{C[0] - R}" y1="{gy}" x2="{C[0] + R}" y2="{gy}" stroke="#5ff2ff" stroke-width="2" opacity=".22"/>'
    b += f'<circle cx="{C[0]}" cy="{C[1]}" r="{R + 60}" fill="#5ff2ff" opacity=".18" filter="url(#b24)"/>'
    b += f'<g mask="url(#mm)"><g clip-path="url(#mc)">{m}</g><circle cx="{C[0]}" cy="{C[1]}" r="{R}" fill="none" stroke="#04101c" stroke-width="6"/></g>'
    # cubes drifting away
    cubes = []
    for (mx, my, t) in removed:
        k = max(0, t) ** 1.4
        dx = 40 + k * random.uniform(260, 560); dy = -(20 + k * random.uniform(160, 380))
        x, y = mx + dx * random.uniform(.3, 1), my + dy * random.uniform(.3, 1)
        if x > 1880 or y < 30 or (x > 1600 and y > 820):
            continue
        cubes.append((y, x, 22 + 26 * random.random() * (1 - k * .3), random.choice('01'), random.choice(['#2fd8f0', '#2fd8f0', '#ffd36a']), max(.45, 1 - k * .35), random.uniform(-20, 20)))
    for (y, x, s, d, c, op, r) in sorted(cubes):
        b += cube(x, y, s, d, c, op, r)
    b += ''.join(spark(random.uniform(1300, 1880), random.uniform(60, 700), random.choice([10, 14, 18]), '#dffcff') for _ in range(7))
    # frog on a big cube, visor on, holding a glowing "1" cube up
    b += '<ellipse cx="800" cy="1040" rx="150" ry="16" fill="#000" opacity=".5"/>'
    b += cube(800, 1000, 250, '0', '#2fd8f0', 1, 0, glow=False)
    b += frog(800, 948, 2.8, mouth='o', arms='reach', look=(6, -6), outfit='visor', rim='#5ff2ff')
    b += cube(992, 770, 64, '1', '#ffd36a', 1, -10)
    lines = [('IT FROM', 200, 'w'), ('BIT?', 330, 'y')]
    return page('#030818', svg(defs, b), lines, outline='#02050f')


for n, fn in ((1, t1), (2, t2), (3, t3), (4, t4), (5, t5)):
    write(n, fn())
print('ok')
