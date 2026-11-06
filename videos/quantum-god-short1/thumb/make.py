# VERTICAL shorts thumbnails (1080x1920) for quantum-god-short1..5 (guideline 16-9, brief tools/briefs/thumb_art.md "Shorts thumbnails").
# Replaces the earlier landscape version (2026-11-06). Text centred around mid-height (thumb_lib.vpage), scene above + below it, frog in the lower part.
# Run: python3 videos/quantum-god-short1/thumb/make.py   -> writes videos/quantum-god-shortN/thumb/A.html (+ tools/assets/thumb_v/*) for N=1..5
# then: for n in 1 2 3 4 5; do SLUG=quantum-god-short$n python3 tools/thumb_shot.py; done
# 1  BOTH / SLITS / AT ONCE?        electron gun -> two slits -> striped screen (top); frog in goggles + thought bubble of two plain bars (bottom)
# 2  WAS / EINSTEIN / WRONG?        Bell test: source in the middle, two polarizer detector stations (top); frog in headset + coincidence counter (bottom)
# 3  NOTHING IS / NEVER / NOTHING   tall "empty" bell jar seething with popping particle pairs; frog with magnifier at the glass (bottom)
# 4  MORE THAN / ONE / REALITY?     sealed lab box (bottom) whose glowing trunk branches into many worlds (top); frog in lab coat
# 5  IT FROM / BIT?                 a moon (top) dissolving into glowing 0/1 cubes that tumble down to the frog on a big cube (bottom)
import os, sys, math, random, shutil
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '../../..'))
sys.path.insert(0, os.path.join(REPO, 'tools'))
from thumb_lib import vpage, vsvg, lin, rad, spark

W, H = 1080, 1920
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


def textband(y0, y1, col='#000', op=.45):
    """soft dark band behind the centred title so it reads over busy art"""
    return f'<rect x="-100" y="{y0}" width="1280" height="{y1 - y0}" fill="{col}" opacity="{op}" filter="url(#b50)"/>'


# ---------------- mascot frog (same body as tools/assets/frog.svg and the quantum-god long thumbnails) ----------------
def frog(x, y, s, mouth='o', arms='down', look=(2, 0), outfit='', flip=False, rim=None):
    sx = -s if flip else s
    g = f'<g transform="translate({x} {y}) scale({sx:.2f} {s:.2f})" stroke="{INK}" stroke-linejoin="round" stroke-linecap="round">'
    g += '<ellipse cx="-22" cy="4" rx="16" ry="9" fill="#4d8a4a" stroke-width="3.2"/><ellipse cx="22" cy="4" rx="16" ry="9" fill="#4d8a4a" stroke-width="3.2"/>'
    g += f'<path d="{BODY}" fill="{GREEN}" stroke-width="4"/>'
    g += '<ellipse cx="2" cy="-12" rx="22" ry="20" fill="#9cc98a" stroke="none" opacity=".7"/>'
    g += '<path d="M-26 -50 q6 -16 22 -18" fill="none" stroke="#b9e0a6" stroke-width="3" opacity=".7"/>'
    if rim:
        g += f'<path d="M36 -56 q8 22 6 50" fill="none" stroke="{rim}" stroke-width="3.6" opacity=".9"/>'
    if outfit == 'coat':
        g += '<path d="M-31 -38 L-6 -30 L-12 3 L-35 0 Q-40 -20 -31 -38 Z" fill="#eef2f6" stroke-width="3"/>'
        g += '<path d="M36 -38 L14 -30 L20 3 L41 -2 Q44 -20 36 -38 Z" fill="#eef2f6" stroke-width="3"/>'
        g += '<path d="M-6 -30 L4 -20 L14 -30" fill="none" stroke-width="2.4"/><rect x="24" y="-22" width="10" height="7" rx="1.5" fill="#cfd8e2" stroke-width="1.8"/>'
        g += '<path d="M27 -24 l0 -6" stroke="#3a7bd5" stroke-width="2.2"/>'
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
    if outfit == 'goggles':
        g += '<path d="M-30 -70 Q6 -84 42 -70" fill="none" stroke="#2a3346" stroke-width="5"/>'
        for ex in (-10, 22):
            g += f'<rect x="{ex - 16}" y="-82" width="32" height="30" rx="12" fill="#bff3ff" fill-opacity=".22" stroke="#2a3346" stroke-width="3.6"/>'
            g += f'<path d="M{ex - 10} -76 q4 -3 9 -3" fill="none" stroke="#fff" stroke-width="2.4" opacity=".9"/>'
        g += '<path d="M6 -70 l0 6" stroke="#2a3346" stroke-width="4"/>'
    if outfit == 'headset':
        g += '<path d="M-26 -60 C-30 -104 42 -104 38 -60" fill="none" stroke="#2a3140" stroke-width="6"/>'
        g += '<ellipse cx="-27" cy="-56" rx="7" ry="11" fill="#3e4a62" stroke-width="3"/><ellipse cx="39" cy="-56" rx="7" ry="11" fill="#3e4a62" stroke-width="3"/>'
        g += '<path d="M40 -48 q6 18 -16 24" fill="none" stroke="#2a3140" stroke-width="3"/><circle cx="23" cy="-24" r="3.6" fill="#ff5a6e" stroke-width="2"/>'
    if outfit == 'visor':
        g += '<rect x="-30" y="-80" width="70" height="26" rx="12" fill="#5ff2ff" fill-opacity=".32" stroke="#16304a" stroke-width="3.4"/>'
        g += '<path d="M-22 -74 L28 -74" stroke="#d8fdff" stroke-width="2.2" opacity=".8"/><circle cx="40" cy="-67" r="3.4" fill="#ffd36a" stroke-width="2"/>'
    return g + '</g>'


def write(n, html):
    d = os.path.join(REPO, f'videos/quantum-god-short{n}/thumb'); os.makedirs(d, exist_ok=True)
    src = os.path.join(REPO, 'tools/assets/thumb_v')
    for f in os.listdir(src):
        shutil.copy(os.path.join(src, f), d)          # vertical common.css (1080x1920) + font, overwrite the landscape css
    open(os.path.join(d, 'A.html'), 'w').write(html)


# ============ 1: BOTH SLITS AT ONCE? ============
def t1():
    random.seed(21)
    defs = FILTERS + lin('sk1', [(0, '#040a1c'), (.45, '#08183a'), (1, '#030714')])
    defs += rad('g1', 900, 330, 760, [(0, '#2fd2ff', .42), (.5, '#1b5fa8', .18), (1, '#040a1c', 0)])
    defs += rad('g2', 1080, 640, 300, [(0, '#9ff6ff', .5), (1, '#9ff6ff', 0)])
    defs += rad('g7', 300, 1560, 520, [(0, '#2fd2ff', .2), (1, '#040a1c', 0)])
    defs += lina('slab', [(0, '#22355a', 1), (1, '#0c1630', 1)], x2=1, y2=0)
    defs += lina('gun', [(0, '#c9d3e6', 1), (.45, '#6c7a98', 1), (1, '#2a3450', 1)])
    defs += lina('cone', [(0, '#bdfbff', .75), (1, '#4fe3ff', .15)], x2=1, y2=0)
    defs += '<clipPath id="wv"><rect x="1112" y="120" width="452" height="820"/></clipPath>'
    b = f'<rect width="{W}" height="{H}" fill="url(#sk1)"/><rect width="{W}" height="{H}" fill="url(#g1)"/><rect width="{W}" height="{H}" fill="url(#g7)"/>'
    b += stars(160, 0, 0, W, 760, '#cfefff', .55)
    # floor with perspective grid (portrait coords)
    FY = 800
    b += f'<rect y="{FY}" width="{W}" height="{H - FY}" fill="#030611"/><path d="M0 {FY} L{W} {FY}" stroke="#2fd2ff" stroke-width="3" opacity=".3"/>'
    for k in range(-10, 18):
        x = k * 90
        b += f'<line x1="{540 + (x - 540) * .25:.0f}" y1="{FY}" x2="{x * 1.6 - 324:.0f}" y2="{H}" stroke="#2fd2ff" stroke-width="2" opacity=".12"/>'
    yy = FY
    for g_ in range(1, 12):
        yy += 14 * g_
        b += f'<line x1="0" y1="{yy}" x2="{W}" y2="{yy}" stroke="#2fd2ff" stroke-width="2" opacity=".1"/>'
    # apparatus drawn in the landscape coordinates, scaled into the upper part
    k = .86; tx = 70 - 690 * k; ty = 110 - 120 * k
    a = ''
    s1, s2 = (1112, 572), (1112, 712)
    wv = ''
    for (sx_, sy_), col in ((s1, '#9ff6ff'), (s2, '#ffe39a')):
        for r in range(26, 640, 34):
            op = max(0, .62 * (1 - r / 660))
            wv += f'<path d="M{sx_} {sy_ - r} A{r} {r} 0 0 1 {sx_} {sy_ + r}" fill="none" stroke="{col}" stroke-width="3.6" opacity="{op:.2f}"/>'
    a += f'<g clip-path="url(#wv)">{wv}</g>'
    L0, L1, R0, R1 = (1560, 196), (1560, 806), (1768, 120), (1768, 872)
    a += f'<polygon points="{pts((1536, 206), L0, L1, (1536, 796))}" fill="#0b1426" stroke="#050913" stroke-width="5"/>'
    a += f'<polygon points="{pts(L0, R0, R1, L1)}" fill="#08111f" stroke="#050913" stroke-width="10"/>'
    fr = ''; N = 90
    for i in range(N):
        v0, v1 = i / N, (i + 1) / N; v = (v0 + v1) / 2
        I = math.cos(math.pi * 4.5 * (v - .5)) ** 2 * math.exp(-((v - .5) / .33) ** 2)
        if I < .03:
            continue
        p = (lerp(L0, L1, v0), lerp(R0, R1, v0), lerp(R0, R1, v1), lerp(L0, L1, v1))
        fr += f'<polygon points="{pts(*p)}" fill="#c8fbff" opacity="{I:.2f}"/>'
    a += f'<g filter="url(#b12)" opacity=".9">{fr}</g>' + fr
    hits = ''
    while hits.count('<circle') < 170:
        v = random.random(); I = math.cos(math.pi * 4.5 * (v - .5)) ** 2 * math.exp(-((v - .5) / .33) ** 2)
        if random.random() < I:
            u = random.uniform(.06, .94); p_ = lerp(lerp(L0, R0, u), lerp(L1, R1, u), v)
            hits += f'<circle cx="{p_[0]:.0f}" cy="{p_[1]:.0f}" r="{random.choice([2.2, 3, 3.8])}" fill="#ffffff" opacity="{random.uniform(.5, 1):.2f}"/>'
    a += hits
    a += f'<polygon points="{pts(L0, R0, R1, L1)}" fill="none" stroke="#7fe8ff" stroke-width="3" opacity=".55"/>'
    a += '<path d="M1768 130 L1768 862" stroke="#bff7ff" stroke-width="4" opacity=".6"/>'
    a += '<path d="M1600 860 L1590 906 M1730 878 L1744 906" stroke="#0b1426" stroke-width="14" stroke-linecap="round"/>'
    a += '<circle cx="1090" cy="642" r="260" fill="url(#g2)"/>'
    for y0, y1 in ((236, 560), (584, 700), (724, 900)):
        a += f'<rect x="1040" y="{y0}" width="72" height="{y1 - y0}" fill="url(#slab)" stroke="#050913" stroke-width="5"/>'
    a += '<polygon points="1040,236 1112,236 1140,214 1068,214" fill="#3a5482" stroke="#050913" stroke-width="5"/>'
    a += '<polygon points="1112,236 1140,214 1140,880 1112,900" fill="#14213f" stroke="#050913" stroke-width="5"/>'
    a += '<path d="M1110 240 L1110 556 M1110 588 L1110 696 M1110 728 L1110 896" stroke="#7fe8ff" stroke-width="3" opacity=".7"/>'
    for yy in (572, 712):
        a += f'<rect x="1030" y="{yy - 12}" width="96" height="24" rx="10" fill="#dffcff" filter="url(#b6)"/><rect x="1040" y="{yy - 8}" width="72" height="16" fill="#f4feff"/>'
    a += '<polygon points="900,770 1042,548 1042,736 900,800" fill="url(#cone)" filter="url(#b6)" opacity=".85"/>'
    for t in (.12, .3, .47, .63, .8, .93):
        p_ = lerp((905, 785), (1040, 642), t)
        a += f'<circle cx="{p_[0]:.0f}" cy="{p_[1]:.0f}" r="13" fill="#9ff6ff" filter="url(#b6)"/><circle cx="{p_[0]:.0f}" cy="{p_[1]:.0f}" r="6" fill="#fff"/>'
    g = '<g transform="rotate(-24 830 800)">'
    g += '<rect x="700" y="768" width="170" height="64" rx="20" fill="url(#gun)" stroke="#0b1022" stroke-width="5"/>'
    for xx in (730, 756, 782):
        g += f'<rect x="{xx}" y="762" width="12" height="76" rx="5" fill="#d98a3a" stroke="#0b1022" stroke-width="3.5"/>'
    g += '<polygon points="868,778 906,788 906,812 868,822" fill="#4a5674" stroke="#0b1022" stroke-width="4"/>'
    g += '<circle cx="908" cy="800" r="16" fill="#bff7ff" filter="url(#b6)"/><circle cx="906" cy="800" r="7" fill="#fff"/>'
    g += '<circle cx="826" cy="786" r="7" fill="#5fffb0" stroke="#0b1022" stroke-width="2.5"/>'
    g += '<path d="M708 780 q60 -6 156 -4" fill="none" stroke="#fff" stroke-width="3.5" opacity=".5"/></g>'
    a += '<path d="M790 812 L740 920 M800 812 L842 922 M796 812 L796 930" stroke="#1a2238" stroke-width="10" stroke-linecap="round"/>'
    a += '<path d="M790 812 L740 920 M800 812 L842 922" stroke="#56658a" stroke-width="3" stroke-linecap="round" opacity=".7"/>'
    a += g + '<ellipse cx="796" cy="930" rx="80" ry="12" fill="#000" opacity=".5"/>'
    b += f'<g transform="translate({tx:.1f} {ty:.1f}) scale({k})">{a}</g>'
    b += textband(830, 1350, op=.5)
    # frog (bottom-left) + thought bubble of what common sense expected: two plain bars
    b += '<ellipse cx="300" cy="1772" rx="140" ry="18" fill="#000" opacity=".55"/>'
    b += frog(300, 1762, 3.7, mouth='o', arms='up', look=(6, -4), outfit='goggles', rim='#9ff6ff')
    b += '<circle cx="490" cy="1500" r="13" fill="#eaf4ff" stroke="#0b1022" stroke-width="4"/><circle cx="532" cy="1462" r="19" fill="#eaf4ff" stroke="#0b1022" stroke-width="4"/>'
    b += '<ellipse cx="760" cy="1560" rx="190" ry="140" fill="#eaf4ff" stroke="#0b1022" stroke-width="6"/>'
    b += '<rect x="690" y="1480" width="36" height="160" rx="6" fill="#3a6fd8"/><rect x="794" y="1480" width="36" height="160" rx="6" fill="#3a6fd8"/>'
    b += '<path d="M640 1680 L880 1680" stroke="#9aa8c4" stroke-width="5" stroke-linecap="round"/>'
    # stray electrons flying toward the apparatus
    for (x, y) in ((560, 1760), (680, 1740), (820, 1772), (950, 1745)):
        b += f'<circle cx="{x}" cy="{y}" r="16" fill="#9ff6ff" opacity=".7" filter="url(#b6)"/><circle cx="{x}" cy="{y}" r="7" fill="#fff"/>'
    b += spark(500, 230, 20, '#dffcff') + spark(980, 1430, 16) + spark(120, 1380, 14, '#dffcff') + spark(1010, 110, 14)
    lines = [('BOTH', 236, 'y'), ('SLITS', 186, 'w'), ('AT ONCE?', 160, 'w')]
    return vpage('#040a1c', vsvg(defs, b), lines, outline='#030714', top=820)


# ============ 2: WAS EINSTEIN WRONG? (Bell test) ============
def station(x, y, s, face_left, lamp, bcol):
    f = -1 if face_left else 1
    g = f'<g transform="translate({x} {y}) scale({f * s:.2f} {s:.2f})" stroke="#061014" stroke-linejoin="round">'
    g += '<path d="M40 60 L40 170 M0 170 L80 170" stroke="#1c2c34" stroke-width="16" stroke-linecap="round"/>'
    g += '<rect x="20" y="-70" width="170" height="130" rx="14" fill="#2c4250" stroke-width="6"/>'
    g += '<rect x="20" y="-70" width="170" height="24" rx="10" fill="#4f6d7c" stroke="none"/>'
    g += '<rect x="80" y="-30" width="86" height="46" rx="6" fill="#06161c" stroke-width="4"/>'
    for k, hh in enumerate((18, 32, 12, 26, 38)):
        g += f'<rect x="{88 + k * 15}" y="{12 - hh}" width="10" height="{hh}" fill="{bcol}" stroke="none" opacity=".9"/>'
    g += f'<circle cx="120" cy="-92" r="18" fill="{lamp}" stroke-width="5"/><rect x="108" y="-80" width="24" height="12" fill="#1c2c34" stroke-width="4"/>'
    g += f'<circle cx="120" cy="-92" r="40" fill="{lamp}" stroke="none" opacity=".35" filter="url(#b12)"/>'
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
    defs = FILTERS + lin('sk2', [(0, '#03161c'), (.35, '#072a30'), (1, '#020a0d')])
    BY = 520; S = (540, BY)
    defs += rad('g3', 540, BY, 560, [(0, '#ff7ae0', .55), (.35, '#8a4dff', .2), (1, '#03161c', 0)])
    defs += rad('core', 540, BY, 90, [(0, '#ffffff', 1), (.4, '#ffd6f4', .9), (1, '#ff7ae0', 0)])
    defs += lina('tbl', [(0, '#1b3a42', 1), (1, '#050f12', 1)])
    b = f'<rect width="{W}" height="{H}" fill="url(#sk2)"/>'
    b += stars(150, 0, 0, W, 600, '#d6fff6', .5)
    # optical table: top surface from y=640 down, holes in perspective toward (540, 300)
    TY = 720
    b += f'<rect y="{TY}" width="{W}" height="{H - TY}" fill="url(#tbl)"/><rect y="{TY}" width="{W}" height="16" fill="#3f7480" opacity=".7"/>'
    vp = (540, 300)
    for j in range(1, 16):
        yy = TY + 18 + 1250 * (j / 15) ** 1.6
        for i in range(-12, 13):
            xb = 540 + i * 85
            t = (yy - vp[1]) / (TY - vp[1])
            x = vp[0] + (xb - vp[0]) * t
            if -10 < x < W + 10:
                b += f'<circle cx="{x:.0f}" cy="{yy:.0f}" r="{1.5 + 2.4 * t:.1f}" fill="#020a0d" opacity=".7"/>'
    b += f'<rect width="{W}" height="{H}" fill="url(#g3)"/>'
    A, B = (300, BY), (780, BY)
    for p, q in ((S, A), (S, B)):
        b += f'<path d="M{p[0]} {p[1]} L{q[0]} {q[1]}" stroke="#ffd36a" stroke-width="24" opacity=".22" filter="url(#b12)"/>'
        b += f'<path d="{photon_path(p, q, 18, 4)}" fill="none" stroke="#ffd36a" stroke-width="8" opacity=".95" filter="url(#b3)"/>'
        b += f'<path d="{photon_path(p, q, 18, 4)}" fill="none" stroke="#fffbe8" stroke-width="3"/>'
        for t in (.45, .8):
            c = lerp(p, q, t)
            b += f'<circle cx="{c[0]:.0f}" cy="{c[1]:.0f}" r="30" fill="#ffd36a" opacity=".5" filter="url(#b12)"/><circle cx="{c[0]:.0f}" cy="{c[1]:.0f}" r="10" fill="#fffbe8"/>'
    # violet pump laser from above
    b += f'<path d="M540 {BY} L720 150" stroke="#a46bff" stroke-width="16" opacity=".35" filter="url(#b6)"/><path d="M540 {BY} L720 150" stroke="#e0ccff" stroke-width="4" opacity=".8"/>'
    b += '<rect x="680" y="106" width="90" height="56" rx="10" transform="rotate(-63 725 134)" fill="#28323c" stroke="#061014" stroke-width="5"/>'
    # source crystal on a post
    b += f'<path d="M540 {BY + 40} L540 {TY + 10}" stroke="#1c2c34" stroke-width="18" stroke-linecap="round"/><ellipse cx="540" cy="{TY + 12}" rx="40" ry="10" fill="#0a1a20"/>'
    b += f'<g transform="translate({540 - 1190} {BY - 610})">'
    b += '<polygon points="1160,580 1206,566 1226,606 1196,650 1156,636" fill="#ffc2f0" stroke="#3a0f36" stroke-width="5"/>'
    b += '<polygon points="1160,580 1206,566 1196,604" fill="#fff" opacity=".7"/><polygon points="1196,604 1226,606 1196,650" fill="#d65cc4" opacity=".55"/></g>'
    b += f'<circle cx="540" cy="{BY}" r="90" fill="url(#core)" opacity=".75"/>'
    b += station(258, BY, 1.1, True, '#ff6a7e', '#ffd36a')
    b += station(822, BY, 1.1, False, '#5fffb0', '#5fffb0')
    b += textband(800, 1340, op=.5)
    # bottom: frog operator in a headset + a coincidence counter with two matching readouts
    b += '<ellipse cx="290" cy="1772" rx="140" ry="18" fill="#000" opacity=".55"/>'
    b += frog(290, 1762, 3.7, mouth='o', arms='reach', look=(7, -5), outfit='headset', rim='#ffd36a')
    cx0, cy0 = 590, 1440
    b += f'<rect x="{cx0}" y="{cy0}" width="400" height="300" rx="26" fill="#1d3640" stroke="#061014" stroke-width="7"/>'
    b += f'<rect x="{cx0}" y="{cy0}" width="400" height="40" rx="18" fill="#3f6472"/>'
    for i, (col, hs) in enumerate((('#ff6a7e', (60, 110, 40, 90, 130)), ('#5fffb0', (60, 110, 40, 90, 130)))):
        x0 = cx0 + 30 + i * 186
        b += f'<rect x="{x0}" y="{cy0 + 64}" width="156" height="170" rx="10" fill="#04121a" stroke="#061014" stroke-width="4"/>'
        for k_, hh in enumerate(hs):
            b += f'<rect x="{x0 + 12 + k_ * 28}" y="{cy0 + 224 - hh}" width="20" height="{hh}" fill="{col}" opacity=".95"/>'
        b += f'<circle cx="{x0 + 78}" cy="{cy0 + 266}" r="14" fill="{col}" stroke="#061014" stroke-width="4"/><circle cx="{x0 + 78}" cy="{cy0 + 266}" r="30" fill="{col}" opacity=".35" filter="url(#b6)"/>'
    b += f'<path d="M{cx0 + 186} {cy0 + 120} l0 60" stroke="#ffd36a" stroke-width="6" stroke-dasharray="10 8"/>'
    b += f'<path d="M{cx0 + 200} {cy0 + 300} L{cx0 + 200} 1772" stroke="#1c2c34" stroke-width="18" stroke-linecap="round"/>'
    b += spark(420, 220, 18) + spark(160, 660, 14, '#ffd6f4') + spark(980, 640, 16) + spark(1000, 1370, 14) + spark(90, 1400, 12)
    lines = [('WAS', 160, 'w'), ('EINSTEIN', 176, 'w'), ('WRONG?', 220, 'y')]
    return vpage('#03161c', vsvg(defs, b), lines, outline='#020a0d', top=810)


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
    X0, X1, TOP, BOT = 150, 930, 190, 1590
    jar = f'M{X0} {BOT} L{X0} 560 C{X0} 300 330 {TOP} 540 {TOP} C750 {TOP} {X1} 300 {X1} 560 L{X1} {BOT}'
    defs = FILTERS + lin('sk3', [(0, '#0a0610'), (.5, '#170a1c'), (1, '#05030a')])
    defs += rad('g4', 540, 700, 820, [(0, '#ff6a3d', .30), (.5, '#9b2a6a', .14), (1, '#0a0610', 0)])
    defs += lina('glass', [(0, '#bfe9ff', .16), (.5, '#bfe9ff', .03), (1, '#bfe9ff', .14)], x2=1, y2=0)
    defs += lina('brass', [(0, '#f3c46a', 1), (.5, '#a86b26', 1), (1, '#4a2a10', 1)])
    defs += f'<clipPath id="jar"><path d="{jar} Z"/></clipPath>'
    defs += rad('lensg', 600, 1430, 120, [(0, '#ffffff', .25), (1, '#bfe9ff', .05)])
    b = f'<rect width="{W}" height="{H}" fill="url(#sk3)"/>'
    b += stars(110, 0, 0, W, 1500, '#ffe8d6', .35)
    b += f'<polygon points="0,1640 {W},1620 {W},{H} 0,{H}" fill="#120a0c"/><polygon points="0,1640 {W},1620 {W},1632 0,1654" fill="#3a1f1a"/>'
    b += f'<rect width="{W}" height="{H}" fill="url(#g4)"/>'
    inner = ''
    for _ in range(90):
        x, y = random.uniform(X0, X1), random.uniform(TOP, BOT)
        inner += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{random.uniform(20, 80):.0f}" fill="{random.choice(["#ff6a3d", "#3ee8ff", "#ff5fc8"])}" opacity="{random.uniform(.04, .1):.2f}" filter="url(#b24)"/>'
    for _ in range(420):
        x, y = random.uniform(X0, X1), random.uniform(TOP, BOT)
        inner += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{random.choice([1.4, 2, 2.6])}" fill="#fff3d6" opacity="{random.uniform(.15, .7):.2f}"/>'
    # pairs above the title (big) and below it (right of the lens); a few faint ones behind the title
    P = [(540, 470, 60, -20, 1), (330, 340, 34, 35, .9), (760, 330, 40, -50, .95), (300, 610, 40, 60, .9), (790, 620, 44, 15, 1),
         (450, 250, 18, 0, .6), (640, 240, 16, 70, .55), (870, 470, 20, 80, .7), (200, 470, 18, -60, .6), (560, 700, 22, 120, .7),
         (820, 1380, 40, -35, .95), (760, 1530, 26, 20, .8), (880, 1270, 22, 60, .7), (240, 1300, 22, -10, .65), (420, 1290, 16, 40, .6),
         (300, 900, 18, 0, .35), (800, 1000, 20, 50, .35), (540, 1150, 16, -30, .3)]
    for (x, y, r, a, op) in P:
        inner += pair(x, y, r, a, op)
    b += f'<g clip-path="url(#jar)">{inner}</g>'
    b += f'<path d="{jar} Z" fill="url(#glass)"/>'
    b += f'<path d="{jar}" fill="none" stroke="#0d1620" stroke-width="12"/><path d="{jar}" fill="none" stroke="#d8f4ff" stroke-width="4" opacity=".7"/>'
    b += f'<path d="M200 1500 L200 580 C200 400 280 290 400 250" fill="none" stroke="#fff" stroke-width="16" opacity=".22" stroke-linecap="round"/>'
    b += f'<path d="M236 560 C236 430 300 340 380 300" fill="none" stroke="#fff" stroke-width="7" opacity=".5" stroke-linecap="round"/>'
    b += f'<path d="M890 1450 L890 620" fill="none" stroke="#fff" stroke-width="6" opacity=".25" stroke-linecap="round"/>'
    b += f'<ellipse cx="540" cy="{TOP - 8}" rx="48" ry="15" fill="#2a1a12" stroke="#0d0806" stroke-width="5"/><rect x="514" y="{TOP - 46}" width="52" height="38" rx="8" fill="url(#brass)" stroke="#0d0806" stroke-width="5"/>'
    # brass base plate + vacuum pipe on the right
    b += f'<path d="M{X1 + 20} 1610 L1040 1610 L1040 1700" fill="none" stroke="#1a0e08" stroke-width="30" stroke-linecap="round"/><path d="M{X1 + 20} 1610 L1040 1610 L1040 1700" fill="none" stroke="#b07a34" stroke-width="18" stroke-linecap="round"/>'
    b += '<ellipse cx="540" cy="1614" rx="440" ry="50" fill="#2a160a" stroke="#0d0806" stroke-width="6"/>'
    b += '<path d="M100 1600 L100 1636 A440 50 0 0 0 980 1636 L980 1600" fill="url(#brass)" stroke="#0d0806" stroke-width="6"/>'
    b += '<ellipse cx="540" cy="1598" rx="440" ry="48" fill="url(#brass)" stroke="#0d0806" stroke-width="6"/>'
    b += '<ellipse cx="540" cy="1594" rx="400" ry="34" fill="none" stroke="#ffe2a0" stroke-width="3" opacity=".7"/>'
    b += textband(760, 1300, op=.55)
    # frog in front of the jar with a magnifying glass on the glass
    b += '<ellipse cx="250" cy="1792" rx="130" ry="17" fill="#000" opacity=".6"/>'
    b += frog(250, 1782, 3.5, mouth='o', arms='lens', look=(7, -5), rim='#ff9b3d')
    LX, LY, LR = 600, 1430, 112
    hx, hy = 250 + 64 * 3.5, 1782 - 52 * 3.5
    b += f'<path d="M{hx:.0f} {hy:.0f} L{LX - 70} {LY + 86}" stroke="#1a0e08" stroke-width="26" stroke-linecap="round"/><path d="M{hx:.0f} {hy:.0f} L{LX - 70} {LY + 86}" stroke="#8a4a1e" stroke-width="14" stroke-linecap="round"/>'
    b += f'<circle cx="{LX}" cy="{LY}" r="{LR + 14}" fill="#0d0806"/><circle cx="{LX}" cy="{LY}" r="{LR}" fill="#1a0c14"/>'
    b += f'<g transform="translate({LX} {LY}) scale(2.2) translate(-1040 -655)">' + pair(1040, 655, 22, 30, 1) + '</g>'
    b += f'<circle cx="{LX}" cy="{LY}" r="{LR}" fill="url(#lensg)"/><path d="M{LX - 72} {LY - 56} A96 96 0 0 1 {LX + 12} {LY - 96}" fill="none" stroke="#fff" stroke-width="8" opacity=".7" stroke-linecap="round"/>'
    b += f'<circle cx="{LX}" cy="{LY}" r="{LR + 6}" fill="none" stroke="url(#brass)" stroke-width="18"/><circle cx="{LX}" cy="{LY}" r="{LR + 15}" fill="none" stroke="#0d0806" stroke-width="5"/>'
    b += spark(980, 260, 18) + spark(80, 300, 14, '#ffe8d6') + spark(1010, 900, 14) + spark(60, 1180, 12) + spark(1000, 1790, 14)
    lines = [('NOTHING IS', 132, 'w'), ('NEVER', 240, 'y'), ('NOTHING', 176, 'w')]
    return vpage('#0a0610', vsvg(defs, b), lines, outline='#05030a', top=770)


# ============ 4: MORE THAN ONE REALITY? (many worlds from Wigner's sealed lab) ============
def branches(x, y, ang, L, w, depth, out, tips):
    a = math.radians(ang)
    x2, y2 = x + math.sin(a) * L, y - math.cos(a) * L
    cx, cy = x + math.sin(a + .25) * L * .5, y - math.cos(a + .25) * L * .5
    out.append((depth, f'M{x:.0f} {y:.0f} Q{cx:.0f} {cy:.0f} {x2:.0f} {y2:.0f}', w))
    if depth == 0:
        tips.append((x2, y2)); return
    spread = random.uniform(26, 36) + (12 if depth >= 4 else 0)
    for s in (-1, 1):
        na = ang + s * spread + random.uniform(-6, 6)
        na = max(-80, min(80, na))
        branches(x2, y2, na, L * random.uniform(.78, .88), w * .7, depth - 1, out, tips)


def t4():
    random.seed(54)
    defs = FILTERS + lin('sk4', [(0, '#041218'), (.45, '#08262a'), (1, '#030a0e')])
    defs += rad('g5', 540, 470, 760, [(0, '#ffd36a', .26), (.45, '#2fbf8f', .12), (1, '#041218', 0)])
    defs += lina('boxL', [(0, '#5d6b78', 1), (1, '#2b343e', 1)])
    defs += lina('boxR', [(0, '#3b4652', 1), (1, '#1a2028', 1)])
    b = f'<rect width="{W}" height="{H}" fill="url(#sk4)"/><rect width="{W}" height="{H}" fill="url(#g5)"/>'
    b += stars(260, 0, 0, W, 1500, '#e6fff6', .6)
    FY = 1660
    b += f'<polygon points="0,{FY} {W},{FY - 30} {W},{H} 0,{H}" fill="#03090c"/><path d="M0 {FY} L{W} {FY - 30}" stroke="#2fbf8f" stroke-width="3" opacity=".3"/>'
    # box placement (landscape box coords scaled): box top-centre lands at (BX, BYT)
    k = .9; BX = 650; tx = BX - 1250 * k; ty = 1360 - 620 * k
    trunk0 = (BX, ty + 700 * k)
    # trunk + branching worlds (portrait coords)
    random.seed(7)
    segs, tips = [], []
    segs.append((6, f'M{trunk0[0]:.0f} {trunk0[1]:.0f} Q{BX - 40} {1060} {540} {760}', 46))
    branches(540, 760, -4, 160, 40, 5, segs, tips)
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
        if not (40 < x < 1040 and 70 < y < 760):
            continue
        r = random.uniform(24, 36); c = cols[i % len(cols)]
        b += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r * 1.9:.0f}" fill="{c}" opacity=".35" filter="url(#b12)"/>'
        b += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r:.0f}" fill="{c}" stroke="#08141a" stroke-width="4"/>'
        b += f'<path d="M{x - r * .8:.0f} {y + r * .1:.0f} q{r * .5:.0f} {-r * .5:.0f} {r * .9:.0f} {-r * .1:.0f} q{r * .3:.0f} {r * .3:.0f} {r * .6:.0f} {-r * .1:.0f}" fill="none" stroke="#08141a" stroke-width="3" opacity=".45"/>'
        b += f'<circle cx="{x - r * .35:.0f}" cy="{y - r * .38:.0f}" r="{r * .22:.0f}" fill="#fff" opacity=".8"/>'
    b += textband(800, 1330, op=.5)
    # sealed lab box (isometric), landscape coords scaled
    cx = 1250
    T = [(cx - 230, 700), (cx, 620), (cx + 230, 700), (cx, 780)]
    Lf = [(cx - 230, 700), (cx, 780), (cx, 990), (cx - 230, 910)]
    Rf = [(cx, 780), (cx + 230, 700), (cx + 230, 910), (cx, 990)]
    bx = f'<ellipse cx="{cx}" cy="985" rx="300" ry="34" fill="#000" opacity=".55"/>'
    bx += f'<polygon points="{pts(*Lf)}" fill="url(#boxL)" stroke="#0a0e12" stroke-width="7"/>'
    bx += f'<polygon points="{pts(*Rf)}" fill="url(#boxR)" stroke="#0a0e12" stroke-width="7"/>'
    bx += f'<polygon points="{pts(*T)}" fill="#7c8a96" stroke="#0a0e12" stroke-width="7"/><polygon points="{pts(*T)}" fill="#ffd36a" opacity=".25"/>'
    bx += f'<ellipse cx="{cx}" cy="700" rx="70" ry="30" fill="#ffd36a" opacity=".5" filter="url(#b12)"/>'
    for kk in (1, 2, 3):
        p = lerp(Rf[0], Rf[3], kk / 4); q = lerp(Rf[1], Rf[2], kk / 4)
        bx += f'<line x1="{p[0]:.0f}" y1="{p[1]:.0f}" x2="{q[0]:.0f}" y2="{q[1]:.0f}" stroke="#0a0e12" stroke-width="3" opacity=".5"/>'
    D = [lerp(lerp(Lf[0], Lf[1], .28), lerp(Lf[3], Lf[2], .28), .18), lerp(lerp(Lf[0], Lf[1], .78), lerp(Lf[3], Lf[2], .78), .18),
         lerp(lerp(Lf[0], Lf[1], .78), lerp(Lf[3], Lf[2], .78), 1.0), lerp(lerp(Lf[0], Lf[1], .28), lerp(Lf[3], Lf[2], .28), 1.0)]
    bx += f'<polygon points="{pts(*D)}" fill="#46525e" stroke="#0a0e12" stroke-width="6"/>'
    wc = lerp(lerp(D[0], D[1], .5), lerp(D[3], D[2], .5), .3)
    bx += f'<ellipse cx="{wc[0]:.0f}" cy="{wc[1]:.0f}" rx="40" ry="46" transform="rotate(-20 {wc[0]:.0f} {wc[1]:.0f})" fill="#ffe49a" stroke="#0a0e12" stroke-width="6"/>'
    bx += f'<ellipse cx="{wc[0]:.0f}" cy="{wc[1]:.0f}" rx="70" ry="76" fill="#ffd36a" opacity=".35" filter="url(#b12)"/>'
    bx += f'<path d="M{wc[0] - 12:.0f} {wc[1] + 14:.0f} q0 -26 14 -26 q14 0 14 26" fill="#c98a2a" opacity=".55"/>'
    kb = lerp(lerp(D[0], D[1], .82), lerp(D[3], D[2], .82), .6)
    bx += f'<circle cx="{kb[0]:.0f}" cy="{kb[1]:.0f}" r="10" fill="#ffd36a" stroke="#0a0e12" stroke-width="4"/>'
    bx += f'<path d="M{Lf[0][0] + 8} {Lf[0][1] + 18} L{Lf[1][0] - 4} {Lf[1][1] + 18}" stroke="#ffd36a" stroke-width="10" stroke-dasharray="20 16" opacity=".8"/>'
    bx += f'<path d="M{Rf[0][0] + 6} {Rf[0][1] + 18} L{Rf[1][0] - 8} {Rf[1][1] + 18}" stroke="#ffd36a" stroke-width="10" stroke-dasharray="20 16" opacity=".6"/>'
    b += f'<g transform="translate({tx:.1f} {ty:.1f}) scale({k})">{bx}</g>'
    # Wigner frog outside the door, lab coat, looking up at the branches
    b += '<ellipse cx="200" cy="1782" rx="130" ry="17" fill="#000" opacity=".6"/>'
    b += frog(200, 1772, 3.4, mouth='o', arms='hold', look=(6, -7), outfit='coat', rim='#ffd36a')
    b += spark(110, 140, 16) + spark(980, 1420, 16) + spark(60, 1380, 12) + spark(1010, 820, 14) + spark(990, 1800, 12)
    lines = [('MORE THAN', 150, 'w'), ('ONE', 250, 'y'), ('REALITY?', 172, 'w')]
    return vpage('#041218', vsvg(defs, b), lines, outline='#020a0d', top=800)


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
    C, R = (470, 450), 300
    defs = FILTERS + lin('sk5', [(0, '#030818'), (.45, '#071a36'), (1, '#02050f')])
    defs += rad('g6', 760, 500, 820, [(0, '#2fe6ff', .30), (.5, '#1f4aa8', .14), (1, '#030818', 0)])
    defs += rad('moon', C[0] - 80, C[1] - 120, 480, [(0, '#e9e4d6', 1), (.55, '#a8a294', 1), (1, '#4a4a58', 1)])
    defs += rad('sun', 1060, 60, 360, [(0, '#ffffff', .8), (.2, '#ffe9b0', .45), (1, '#ffd36a', 0)])
    b = f'<rect width="{W}" height="{H}" fill="url(#sk5)"/><rect width="{W}" height="{H}" fill="url(#g6)"/>'
    b += stars(360, 0, 0, W, H, '#dff6ff', .7)
    b += f'<rect width="{W}" height="{H}" fill="url(#sun)"/>'
    cell = 44; removed = []; keep_mask = ''
    for gx in range(int(C[0] - R), int(C[0] + R), cell):
        for gy in range(int(C[1] - R), int(C[1] + R), cell):
            mx, my = gx + cell / 2, gy + cell / 2
            if math.hypot(mx - C[0], my - C[1]) > R + 20:
                continue
            t = ((mx - C[0]) * .85 + (my - C[1]) * .5) / R     # dissolving toward the lower right
            if random.random() < (t - .05) * 1.6:
                removed.append((mx, my, t))
                keep_mask += f'<rect x="{gx}" y="{gy}" width="{cell}" height="{cell}" fill="#000"/>'
    defs += f'<mask id="mm"><rect width="{W}" height="{H}" fill="#fff"/>{keep_mask}</mask>'
    defs += f'<clipPath id="mc"><circle cx="{C[0]}" cy="{C[1]}" r="{R}"/></clipPath>'
    m = f'<circle cx="{C[0]}" cy="{C[1]}" r="{R}" fill="url(#moon)"/>'
    for _ in range(26):
        x = random.uniform(C[0] - R, C[0] + R); y = random.uniform(C[1] - R, C[1] + R); r = random.uniform(10, 46)
        m += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r:.0f}" fill="#6e6a64" opacity=".45"/><path d="M{x - r * .8:.0f} {y + r * .3:.0f} A{r:.0f} {r:.0f} 0 0 0 {x + r * .8:.0f} {y + r * .3:.0f}" fill="none" stroke="#f6f2e6" stroke-width="3" opacity=".45"/>'
    m += f'<circle cx="{C[0] - 130}" cy="{C[1] + 120}" r="{R}" fill="#0a1024" opacity=".35"/>'
    for gx in range(int(C[0] - R), int(C[0] + R), cell):
        m += f'<line x1="{gx}" y1="{C[1] - R}" x2="{gx}" y2="{C[1] + R}" stroke="#5ff2ff" stroke-width="2" opacity=".22"/>'
    for gy in range(int(C[1] - R), int(C[1] + R), cell):
        m += f'<line x1="{C[0] - R}" y1="{gy}" x2="{C[0] + R}" y2="{gy}" stroke="#5ff2ff" stroke-width="2" opacity=".22"/>'
    b += f'<circle cx="{C[0]}" cy="{C[1]}" r="{R + 60}" fill="#5ff2ff" opacity=".18" filter="url(#b24)"/>'
    b += f'<g mask="url(#mm)"><g clip-path="url(#mc)">{m}</g><circle cx="{C[0]}" cy="{C[1]}" r="{R}" fill="none" stroke="#04101c" stroke-width="6"/></g>'
    # cubes drift to the right and tumble down the right side (sparser behind the title band)
    cubes = []
    for (mx, my, t) in removed:
        kk = max(0, t) ** 1.3
        dx = 30 + kk * random.uniform(120, 340); dy = 10 + kk * random.uniform(40, 560)
        x, y = mx + dx * random.uniform(.4, 1), my + dy * random.uniform(.3, 1)
        if x > 1050 or y < 40:
            continue
        if 800 < y < 1330 and x < 930:
            continue
        cubes.append((y, x, 20 + 26 * random.random() * (1 - kk * .25), random.choice('01'), random.choice(['#2fd8f0', '#2fd8f0', '#ffd36a']), max(.5, 1 - kk * .3), random.uniform(-20, 20)))
    for (y, x, s, d, c, op, r) in sorted(cubes):
        b += cube(x, y, s, d, c, op, r)
    b += ''.join(spark(random.uniform(800, 1050), random.uniform(80, 700), random.choice([10, 14, 18]), '#dffcff') for _ in range(6))
    b += textband(790, 1330, op=.5)
    # falling stream of cubes below the title down to the frog
    for (x, y, s, d, c, r) in ((900, 1400, 46, '1', '#2fd8f0', 12), (980, 1520, 38, '0', '#ffd36a', -14), (860, 1600, 54, '0', '#2fd8f0', 8),
                               (970, 1700, 44, '1', '#2fd8f0', -6), (130, 1400, 34, '0', '#2fd8f0', 10), (80, 1560, 28, '1', '#ffd36a', -10)):
        b += cube(x, y, s, d, c, .95, r)
    # frog on a big "0" cube, visor on, holding a glowing "1" cube up
    b += '<ellipse cx="420" cy="1822" rx="190" ry="18" fill="#000" opacity=".55"/>'
    b += cube(420, 1690, 270, '0', '#2fd8f0', 1, 0, glow=False)
    b += frog(420, 1616, 3.2, mouth='o', arms='reach', look=(6, -6), outfit='visor', rim='#5ff2ff')
    b += cube(420 + 70 * 3.2, 1616 - 60 * 3.2 - 14, 76, '1', '#ffd36a', 1, -10)
    lines = [('IT FROM', 210, 'w'), ('BIT?', 330, 'y')]
    return vpage('#030818', vsvg(defs, b), lines, outline='#02050f', top=800)


if __name__ == '__main__':
    for n, fn in ((1, t1), (2, t2), (3, t3), (4, t4), (5, t5)):
        if len(sys.argv) < 2 or str(n) in sys.argv[1:]:
            write(n, fn())
    print('ok')
