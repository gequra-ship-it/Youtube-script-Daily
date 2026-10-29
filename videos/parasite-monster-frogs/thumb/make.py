# Thumbnails A-C for parasite-monster-frogs (guideline 16-6/16-8, brief tools/briefs/thumb_art.md). Run: python3 videos/parasite-monster-frogs/thumb/make.py
# Sensitive topic: cartoon only (no blood, no wounds); the deformed frog is a cute leopard frog with extra legs.
# A  MADE BY A WORM     homage: Frankenstein (1931) lab: storm window, lightning, coil arcs; a goggled flatworm throws the switch (S09 parasite, S36 tiny worm reshapes a far larger animal)
# B  1 WORM 3 HOSTS     intuitive: glowing cycle ramshorn snail -> tadpole limb buds -> heron (S11 "three different hosts", S12-S27)
# C  WHY CRIPPLE IT?    homage: The Birds (Hitchcock): frogs on a bench, the frame behind them fills with herons (S22 question, S24 deformed hosts easier to catch)
import os, sys, math, random
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../tools'))
from thumb_lib import page, svg, lin, rad, spark

INK = '#1d2b1c'; GREEN = '#6aa55a'
FILTERS = ''.join(f'<filter id="b{d}" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="{d}"/></filter>' for d in (2, 3, 6, 12, 24, 50))


# ---------------- mascot frog (tools/assets/frog.svg body; outfit layers vary) ----------------
def frog(x, y, s, mouth='o', arms=('q-14 6 -16 22', 'q14 6 16 22'), look=(2, 0), back='', torso='', head='', front='', flip=False, sweat=False):
    sx = -s if flip else s
    g = f'<g transform="translate({x} {y}) scale({sx} {s})" stroke="{INK}" stroke-linejoin="round" stroke-linecap="round">'
    g += back
    g += '<ellipse cx="-22" cy="4" rx="16" ry="9" fill="#4d8a4a" stroke-width="3.2"/><ellipse cx="22" cy="4" rx="16" ry="9" fill="#4d8a4a" stroke-width="3.2"/>'
    g += f'<path d="M-34 0 q-6 -64 34 -70 q40 -2 42 62 q0 10 -6 12 q-36 6 -70 -4z" fill="{GREEN}" stroke-width="4"/>'
    g += '<ellipse cx="2" cy="-12" rx="22" ry="20" fill="#9cc98a" stroke="none" opacity=".7"/>'
    g += '<path d="M-26 -50 q6 -16 22 -18" fill="none" stroke="#b9e0a6" stroke-width="3" opacity=".7"/>'
    g += torso
    dx, dy = look
    for ex in (-10, 22):
        g += f'<circle cx="{ex}" cy="-66" r="13" fill="#e3e5d6" stroke-width="3.2"/><circle cx="{ex + dx}" cy="{-66 + dy}" r="5" fill="{INK}" stroke="none"/>'
        g += f'<circle cx="{ex + 2 + dx * .6}" cy="{-68 + dy}" r="1.7" fill="#fff" stroke="none"/>'
    g += '<ellipse cx="-18" cy="-46" rx="5" ry="3" fill="#e98a8a" stroke="none" opacity=".55"/><ellipse cx="30" cy="-46" rx="5" ry="3" fill="#e98a8a" stroke="none" opacity=".55"/>'
    if mouth == 'o':
        g += '<ellipse cx="6" cy="-42" rx="6.5" ry="8" fill="#7a2f33" stroke-width="3"/><ellipse cx="6" cy="-38" rx="3.5" ry="2.6" fill="#e07b7b" stroke="none"/>'
    elif mouth == 'yuck':
        g += '<path d="M-7 -42 q4 -5 7 0 q4 5 7 0 q4 -5 7 0 q4 5 6 1" fill="none" stroke-width="3.2"/>'
    else:
        g += '<path d="M-8 -45 q14 14 28 0 q-14 4 -28 0z" fill="#7a2f33" stroke-width="3"/>'
    if sweat:
        g += '<path d="M40 -84 q6 9 0 13 q-6 -4 0 -13z" fill="#bfe8ff" stroke-width="2.2"/>'
    g += head
    la, ra = arms
    for st, path in (('M-32 -22', la), ('M38 -22', ra)):
        g += f'<path d="{st} {path}" fill="none" stroke-width="7.5"/><path d="{st} {path}" fill="none" stroke="{GREEN}" stroke-width="3.4"/>'
        sx0, sy0 = map(float, st[1:].split()); q = [float(v) for v in path[1:].split()]
        g += f'<circle cx="{sx0 + q[2]}" cy="{sy0 + q[3]}" r="5.5" fill="{GREEN}" stroke-width="3"/>'
    g += front
    return g + '</g>'


# ---------------- the "monster" leopard frog (cartoon, extra hind legs from the hip) ----------------
def leg(x0, y0, pts, col='#86a957', w=9.0):
    """a frog leg: hip (x0,y0) -> knee -> ankle -> foot tip, drawn as thick ink + colour stroke, webbed foot at the end"""
    (kx, ky), (ax, ay), (fx, fy) = pts
    d = f'M{x0} {y0} L{kx} {ky} L{ax} {ay}'
    g = f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="{w + 4.5}"/><path d="{d}" fill="none" stroke="{col}" stroke-width="{w}"/>'
    g += f'<path d="M{x0} {y0} L{(x0 + kx) / 2:.1f} {(y0 + ky) / 2:.1f}" stroke="#4a6b2c" stroke-width="{w * .35:.1f}" opacity=".7"/>'   # thigh stripe
    ang = math.atan2(fy - ay, fx - ax); L = math.hypot(fx - ax, fy - ay)
    toes = []
    for k in range(4):
        a = ang + (k - 1.5) * .32
        toes.append((ax + L * math.cos(a), ay + L * math.sin(a)))
    web = f'M{ax} {ay} ' + ' '.join(f'L{tx:.1f} {ty:.1f}' for tx, ty in toes) + 'Z'
    g += f'<path d="{web}" fill="#a6c46f" stroke="{INK}" stroke-width="3" opacity=".95"/>'
    for tx, ty in toes:
        g += f'<path d="M{ax} {ay} L{tx:.1f} {ty:.1f}" stroke="{INK}" stroke-width="3"/><circle cx="{tx:.1f}" cy="{ty:.1f}" r="3.2" fill="#c7dd96" stroke="{INK}" stroke-width="2"/>'
    return g


def monster(x, y, s, extra=3, pick=None, mouth='smile', look=(0, 0), glow=None):
    g = f'<g transform="translate({x} {y}) scale({s})" stroke-linejoin="round" stroke-linecap="round">'
    if glow:
        g += f'<ellipse cx="0" cy="-40" rx="110" ry="80" fill="{glow}" opacity=".55" filter="url(#b24)"/>'
    # extra legs (behind the body), sprouting from the hips
    xl = [((-52, 10), (-88, -18), (-112, -40)), ((52, 12), (96, -10), (118, -36)), ((-46, 22), (-84, 32), (-120, 20)),
          ((46, 22), (86, 30), (122, 16)), ((-20, 28), (-34, 58), (-50, 76))]
    hips = [(-26, -6), (30, -6), (-24, -2), (28, -2), (-8, 2)]
    idx = pick or list(range(extra))
    xl = [xl[i] for i in idx]; hips = [hips[i] for i in idx]
    for (hx, hy), p in zip(hips, xl):
        g += leg(hx, hy, p, w=8)
    # normal hind legs folded at the sides
    for sgn in (-1, 1):
        g += f'<path d="M{sgn * 20} -14 q{sgn * 40} -10 {sgn * 42} 14 q-2 10 {-sgn * 30} 10z" fill="#7f9f50" stroke="{INK}" stroke-width="3.2"/>'
        g += f'<path d="M{sgn * 30} 8 l{sgn * 26} 4 l{sgn * 4} -6 m{-sgn * 4} 6 l{sgn * 6} 4" fill="none" stroke="{INK}" stroke-width="3"/>'
    # body: pear shape, olive-green with leopard spots
    body = 'M-36 4 q-12 -60 36 -74 q48 6 38 74 q-38 10 -74 0z'
    g += f'<path d="{body}" fill="#93b862" stroke="{INK}" stroke-width="4"/>'
    g += '<ellipse cx="2" cy="-10" rx="22" ry="17" fill="#e7e3b8" opacity=".85"/>'
    for sx_, sy_, r in ((-22, -44, 6), (14, -54, 5), (26, -30, 6), (-28, -18, 5), (-6, -62, 4), (30, -12, 4)):
        g += f'<ellipse cx="{sx_}" cy="{sy_}" rx="{r}" ry="{r * .8:.1f}" fill="#3f5a26" stroke="#c9dd9a" stroke-width="1.4"/>'
    g += '<path d="M-28 -50 q6 -16 22 -20" fill="none" stroke="#d6efb0" stroke-width="3" opacity=".8"/>'
    # gold eyes with dark horizontal pupils
    dx, dy = look
    for ex in (-14, 18):
        g += f'<circle cx="{ex}" cy="-68" r="12" fill="#e6c25a" stroke="{INK}" stroke-width="3.2"/><ellipse cx="{ex + dx}" cy="{-68 + dy}" rx="6" ry="3.6" fill="{INK}"/>'
        g += f'<circle cx="{ex + 3 + dx * .5}" cy="{-71 + dy}" r="2" fill="#fff"/>'
    if mouth == 'smile':
        g += f'<path d="M-14 -42 q16 10 32 0" fill="none" stroke="{INK}" stroke-width="3.2"/>'
    else:
        g += f'<path d="M-10 -40 q12 -8 24 0" fill="none" stroke="{INK}" stroke-width="3.2"/>'
    # front arms
    for sgn in (-1, 1):
        g += f'<path d="M{sgn * 18} -30 q{sgn * 6} 18 {sgn * 4} 32" fill="none" stroke="{INK}" stroke-width="8"/><path d="M{sgn * 18} -30 q{sgn * 6} 18 {sgn * 4} 32" fill="none" stroke="#93b862" stroke-width="4"/>'
        g += f'<path d="M{sgn * 22} 2 l{sgn * -6} 4 m{sgn * 6} -4 l0 6 m0 -6 l{sgn * 6} 4" stroke="{INK}" stroke-width="2.6" fill="none"/>'
    return g + '</g>'


# ---------------- heron (standing, facing right; feet at 0,0, ~230 units high) ----------------
def heron(x, y, s, flip=False, sil=None, rim='#e8eef0'):
    sx = -s if flip else s
    body, neck, wing, beak, leg_c = ('#8d9aa6', '#e6eaec', '#5f6c78', '#e8b34a', '#a88a50') if sil is None else (sil, sil, sil, sil, sil)
    g = f'<g transform="translate({x} {y}) scale({sx} {s})" stroke-linecap="round" stroke-linejoin="round">'
    g += f'<path d="M-4 -78 L-10 0 M8 -78 L12 0" stroke="{leg_c}" stroke-width="5" fill="none"/>'
    g += f'<path d="M-10 0 l-14 2 M-10 0 l10 3 M12 0 l14 1 M12 0 l-6 4" stroke="{leg_c}" stroke-width="3.4"/>'
    g += f'<path d="M38 -118 q-18 -30 4 -56 q16 -20 -4 -42" fill="none" stroke="{neck}" stroke-width="15"/>'
    g += f'<path d="M-62 -84 q18 -46 76 -42 q30 4 30 28 q-6 26 -48 30 q-36 2 -58 -16z" fill="{body}"/>'
    g += f'<path d="M-66 -84 q34 -24 86 -16 q-10 18 -40 24 q-26 2 -46 -8z" fill="{wing}"/>'
    g += f'<path d="M-70 -82 l-22 12 l26 -4z" fill="{wing}"/>'
    g += f'<ellipse cx="38" cy="-220" rx="14" ry="11" fill="{neck}"/>'
    g += f'<path d="M48 -224 L110 -216 L48 -211z" fill="{beak}"/>'
    g += f'<path d="M30 -228 L-6 -236" stroke="{"#20262b" if sil is None else sil}" stroke-width="4"/>'
    if sil is None:
        g += f'<circle cx="42" cy="-222" r="2.6" fill="#f2d27a" stroke="#20262b" stroke-width="1.5"/>'
        g += '<path d="M40 -170 q6 20 0 44" stroke="#20262b" stroke-width="2.4" stroke-dasharray="4 5" fill="none" opacity=".7"/>'
    else:   # thin rim light on silhouettes (light from the left / top)
        g += f'<path d="M-62 -86 q18 -44 76 -40" stroke="{rim}" stroke-width="2.4" fill="none" opacity=".55"/>'
        g += f'<path d="M30 -128 q-16 -28 6 -50 q12 -16 0 -34" stroke="{rim}" stroke-width="2" fill="none" opacity=".45"/>'
    return g + '</g>'


def fly_heron(x, y, s, sil=None):
    """heron in flight, facing left: tucked S-neck, trailing legs, broad wings raised"""
    body, neck, wfar, wnear, beak, legc, ink = ('#9aa7b3', '#e6eaec', '#6f7c89', 'url(#wingB)', '#e8b34a', '#a88a50', '#20262b') if sil is None else (sil,) * 7
    sw = 3.6 if sil is None else 0
    g = f'<g transform="translate({x} {y}) scale({s})" stroke="{ink}" stroke-width="{sw}" stroke-linejoin="round" stroke-linecap="round">'
    g += f'<path d="M0 -6 q30 -90 120 -150 q-10 40 -26 64 q22 -8 40 -6 q-30 34 -64 52 q16 2 24 10 q-40 26 -96 30z" fill="{wfar}"/>'
    g += f'<path d="M70 8 L200 22 M70 8 L196 32" stroke="{legc}" stroke-width="5"/>'
    g += f'<path d="M-64 4 q40 -36 130 -18 q36 8 38 22 q-40 20 -116 14 q-40 -4 -52 -18z" fill="{body}"/>'
    g += f'<path d="M-40 -2 q-20 -100 -150 -150 q20 46 44 70 q-36 -2 -58 6 q44 30 86 44 q-26 6 -34 16 q60 26 130 20z" fill="{wnear}"/>'
    if sil is None:
        g += '<path d="M-60 -50 q-40 -40 -96 -70 M-46 -24 q-40 -16 -96 -22" stroke="#5f6c78" stroke-width="3" fill="none"/>'
        g += '<path d="M-44 -6 q-24 -90 -136 -140" stroke="#fff" stroke-width="3" fill="none" opacity=".6"/>'
    g += f'<path d="M-58 4 q-36 10 -48 -8 q-8 -18 10 -26" fill="none" stroke="{neck}" stroke-width="16"/>'
    g += f'<ellipse cx="-96" cy="-32" rx="15" ry="11" fill="{neck}"/><path d="M-108 -34 L-178 -24 L-108 -26z" fill="{beak}"/>'
    g += f'<path d="M-88 -40 L-60 -50" stroke="{"#20262b" if sil is None else sil}" stroke-width="4"/>'
    if sil is None:
        g += '<circle cx="-100" cy="-34" r="2.6" fill="#f2d27a" stroke-width="1.4"/>'
    return g + '</g>'


def cerc(x, y, a, s=1.0, col='#e9fbff'):
    """cercaria: tiny swimming larva with a forked tail (a = heading in degrees)"""
    return (f'<g transform="translate({x:.0f} {y:.0f}) rotate({a:.0f}) scale({s})" stroke="{col}" stroke-linecap="round" fill="none">'
            f'<ellipse cx="0" cy="0" rx="7" ry="4.2" fill="{col}" stroke="none"/><path d="M-6 0 q-8 3 -16 0" stroke-width="2.4"/>'
            f'<path d="M-22 0 l-7 -5 M-22 0 l-7 5" stroke-width="2"/></g>')


def snail(x, y, s):
    """ramshorn snail: flat coiled shell seen from the side + red foot, two thin tentacles"""
    g = f'<g transform="translate({x} {y}) scale({s})" stroke-linejoin="round" stroke-linecap="round">'
    g += f'<path d="M-170 96 q-6 -36 40 -40 l170 0 q52 6 60 40 q-130 14 -270 0z" fill="#b5523e" stroke="{INK}" stroke-width="4"/>'
    g += '<path d="M-150 84 q100 8 250 -2" stroke="#e8907a" stroke-width="4" fill="none" opacity=".7"/>'
    g += f'<path d="M-150 66 q-30 -40 -60 -56 M-140 64 q-14 -46 -30 -70" stroke="{INK}" stroke-width="9" fill="none"/>'
    g += '<path d="M-150 66 q-30 -40 -60 -56 M-140 64 q-14 -46 -30 -70" stroke="#c96a52" stroke-width="5" fill="none"/>'
    g += f'<circle cx="-146" cy="62" r="5" fill="{INK}"/><circle cx="-134" cy="60" r="5" fill="{INK}"/>'
    g += f'<circle cx="0" cy="-30" r="118" fill="url(#shellG)" stroke="{INK}" stroke-width="5"/>'
    # spiral suture (log spiral), whorls get smaller to the centre
    pts = []
    for i in range(0, 420):
        t = i / 40; r = 116 * math.exp(-.16 * t)
        pts.append(f'{r * math.cos(t + 2.2):.1f},{-30 + r * math.sin(t + 2.2):.1f}')
    g += f'<polyline points="{" ".join(pts)}" fill="none" stroke="{INK}" stroke-width="4"/>'
    for i in range(0, 260, 6):   # growth lines
        t = i / 40; r1 = 116 * math.exp(-.16 * t); r2 = 116 * math.exp(-.16 * (t + 6.283))
        a = t + 2.2
        g += f'<path d="M{r1 * math.cos(a):.1f} {-30 + r1 * math.sin(a):.1f} L{r2 * math.cos(a):.1f} {-30 + r2 * math.sin(a):.1f}" stroke="#5a2a1a" stroke-width="1.6" opacity=".45"/>'
    g += '<path d="M-84 -96 q40 -46 104 -40" stroke="#ffd9a8" stroke-width="9" fill="none" opacity=".75"/>'
    g += '<path d="M-60 -60 q20 -20 50 -20" stroke="#ffe8c8" stroke-width="5" fill="none" opacity=".6"/>'
    return g + '</g>'


def tadpole(x, y, s, buds=True):
    g = f'<g transform="translate({x} {y}) scale({s})" stroke-linejoin="round" stroke-linecap="round">'
    g += f'<path d="M70 -10 q80 -40 160 -6 q60 22 120 6 q-50 30 -120 18 q-80 -12 -160 20z" fill="#a9b98a" fill-opacity=".55" stroke="{INK}" stroke-width="3.4"/>'
    g += f'<path d="M70 -6 q90 -14 270 4" stroke="#5d6a3e" stroke-width="10" fill="none"/>'
    g += f'<ellipse cx="0" cy="0" rx="96" ry="66" fill="url(#tadG)" stroke="{INK}" stroke-width="4.5"/>'
    for sx_, sy_ in ((-40, -30), (10, -40), (40, -20), (-10, -12), (-50, 6), (20, 10)):
        g += f'<circle cx="{sx_}" cy="{sy_}" r="5" fill="#3d3a22" opacity=".6"/>'
    g += '<path d="M-70 -30 q30 -32 80 -30" stroke="#e6e2b0" stroke-width="6" fill="none" opacity=".6"/>'
    g += f'<circle cx="-52" cy="-14" r="14" fill="#f0eccc" stroke="{INK}" stroke-width="3.4"/><circle cx="-56" cy="-14" r="7" fill="{INK}"/><circle cx="-58" cy="-17" r="2.4" fill="#fff"/>'
    g += f'<path d="M-90 16 q8 6 16 2" stroke="{INK}" stroke-width="3" fill="none"/>'
    if buds:
        g += '<circle cx="66" cy="40" r="44" fill="#ffe08a" opacity=".55" filter="url(#b12)"/>'
        for bx in (54, 82):
            g += f'<ellipse cx="{bx}" cy="48" rx="11" ry="15" fill="#ffd36a" stroke="{INK}" stroke-width="3"/>'
    return g + '</g>'


def bolt(pts, w=10, col='#f4fbff', glow='#9fdcff'):
    d = 'M' + ' L'.join(f'{a} {b}' for a, b in pts)
    return (f'<path d="{d}" fill="none" stroke="{glow}" stroke-width="{w * 4}" opacity=".5" filter="url(#b12)"/>'
            f'<path d="{d}" fill="none" stroke="{col}" stroke-width="{w}" stroke-linejoin="round"/>')


def arc_zig(x0, y0, x1, y1, n=9, amp=26):
    pts = [(x0, y0)]
    for i in range(1, n):
        t = i / n; nx, ny = -(y1 - y0), (x1 - x0); L = math.hypot(nx, ny)
        o = random.uniform(-amp, amp)
        pts.append((round(x0 + (x1 - x0) * t + nx / L * o), round(y0 + (y1 - y0) * t + ny / L * o)))
    pts.append((x1, y1))
    return pts


# ======================= A: Frankenstein lab =======================
def thumb_A():
    random.seed(11)
    defs = FILTERS
    defs += lin('wallA', [(0, '#222c3d'), (1, '#121822')])
    defs += lin('stormA', [(0, '#1b2546'), (.6, '#3b4f86'), (1, '#6f86b8')])
    defs += lin('copper', [(0, '#5a2c12'), (.4, '#e09a5a'), (.6, '#ffd2a0'), (1, '#6a3414')], x2=1, y2=0)
    defs += lin('metalA', [(0, '#3a414a'), (.45, '#c9d1d9'), (1, '#4a5058')], x2=1, y2=0)
    defs += rad('haloA', 1290, 520, 560, [(0, '#bff0ff', .55), (.35, '#6fc8ff', .2), (1, '#6fc8ff', 0)])
    defs += rad('vigA', 960, 540, 1150, [(0, '#000', 0), (.6, '#000', 0), (1, '#000', .7)])
    b = '<rect width="1920" height="1080" fill="url(#wallA)"/>'
    # stone blocks
    for row in range(0, 16):
        y = row * 70; off = (row % 2) * 70
        for x in range(-140 + off, 1920, 140):
            sh = random.choice(['#273246', '#222b3c', '#2b364b', '#1f2737'])
            b += f'<rect x="{x + 4}" y="{y + 4}" width="132" height="62" rx="8" fill="{sh}" stroke="#141a26" stroke-width="3"/>'
    # tall arched storm window (top centre-right)
    WX0, WX1, WY0, WY1 = 1060, 1520, 30, 470
    cx = (WX0 + WX1) / 2
    win = f'M{WX0} {WY1} L{WX0} {WY0 + 160} A{(WX1 - WX0) / 2} 170 0 0 1 {WX1} {WY0 + 160} L{WX1} {WY1} Z'
    b += f'<path d="{win}" fill="#0c1018" stroke="#0c1018" stroke-width="44"/>'
    b += f'<path d="{win}" fill="url(#stormA)"/>'
    defs += f'<clipPath id="winA"><path d="{win}"/></clipPath>'
    sky = '<g clip-path="url(#winA)">'
    for _ in range(14):
        sky += f'<ellipse cx="{random.randint(WX0 - 40, WX1 + 40)}" cy="{random.randint(WY0 + 40, WY1 - 120)}" rx="{random.randint(80, 170)}" ry="{random.randint(30, 60)}" fill="#1a2242" opacity=".7" filter="url(#b12)"/>'
    sky += '<ellipse cx="1300" cy="200" rx="200" ry="120" fill="#cfe8ff" opacity=".45" filter="url(#b50)"/>'
    sky += bolt([(1340, 30), (1310, 120), (1350, 150), (1290, 260), (1330, 280), (1270, 400)], w=9)
    sky += bolt([(1310, 120), (1250, 170), (1230, 230)], w=5)
    sky += f'<path d="M{WX0} 420 q120 -50 220 -10 q120 -60 240 -20 L{WX1} {WY1} L{WX0} {WY1}z" fill="#0b0f1a"/>'   # far hill tower silhouette
    sky += '<path d="M1420 420 l0 -70 l14 -14 l14 14 l0 60z" fill="#0b0f1a"/>'
    sky += '</g>'
    b += sky
    b += f'<path d="M{cx} {WY0 + 6} L{cx} {WY1} M{WX0} 300 L{WX1} 300" stroke="#0c1018" stroke-width="16"/>'
    b += f'<path d="M{WX0 - 30} {WY1 + 12} L{WX1 + 30} {WY1 + 12}" stroke="#3a4560" stroke-width="22"/>'
    b += '<rect width="1920" height="1080" fill="url(#haloA)"/>'
    # light shaft from window down to the slab
    b += f'<path d="M{WX0 + 40} {WY1} L{WX1 - 40} {WY1} L1640 800 L940 800 Z" fill="#cfefff" opacity=".10" filter="url(#b12)"/>'
    # hanging chains
    for chx in (1000, 1590):
        for k in range(0, 13):
            b += f'<ellipse cx="{chx}" cy="{10 + k * 34}" rx="{7 if k % 2 else 4}" ry="17" fill="none" stroke="#7d8692" stroke-width="5"/>'
    # floor
    b += '<path d="M0 880 L1920 860 L1920 1080 L0 1080 Z" fill="#0d1118"/>'
    b += '<path d="M0 880 L1920 860" stroke="#3a4560" stroke-width="3"/>'
    for i in range(-6, 14):
        b += f'<path d="M{960 + i * 70} 870 L{960 + i * 190} 1080" stroke="#161c27" stroke-width="3"/>'
    # Tesla coil on the right
    TX, TB, TT = 1700, 860, 470
    b += f'<rect x="{TX - 70}" y="{TB - 40}" width="140" height="44" rx="6" fill="#2b2f36" stroke="#0a0d12" stroke-width="4"/>'
    b += f'<rect x="{TX - 34}" y="{TT + 50}" width="68" height="{TB - TT - 90}" fill="url(#copper)" stroke="#2a1608" stroke-width="4"/>'
    for yy in range(TT + 60, TB - 40, 12):
        b += f'<path d="M{TX - 34} {yy} L{TX + 34} {yy}" stroke="#7a3e18" stroke-width="2.5"/>'
    b += f'<ellipse cx="{TX}" cy="{TT + 20}" rx="92" ry="38" fill="url(#metalA)" stroke="#0a0d12" stroke-width="4"/>'
    b += f'<ellipse cx="{TX - 26}" cy="{TT + 6}" rx="40" ry="10" fill="#fff" opacity=".55"/>'
    # electric arcs from the coil to the frog's head clamp
    for k in range(3):
        b += bolt(arc_zig(TX - 70, TT + 10 + k * 10, 1400, 470 + k * 30, n=8, amp=30), w=4 if k else 6, glow='#7fd6ff')
    # operating slab
    SX0, SX1, SY = 960, 1600, 790
    b += f'<ellipse cx="{(SX0 + SX1) / 2}" cy="{SY + 90}" rx="380" ry="30" fill="#000" opacity=".5" filter="url(#b12)"/>'
    for lx in (SX0 + 60, SX1 - 60):
        b += f'<rect x="{lx - 18}" y="{SY + 30}" width="36" height="58" fill="#2e333b" stroke="#0a0d12" stroke-width="4"/>'
    b += f'<path d="M{SX0} {SY} L{SX1} {SY} L{SX1 - 20} {SY + 36} L{SX0 + 20} {SY + 36} Z" fill="#5a6270" stroke="#0a0d12" stroke-width="5"/>'
    b += f'<path d="M{SX0 + 10} {SY + 6} L{SX1 - 10} {SY + 6}" stroke="#aab4c2" stroke-width="5"/>'
    # the monster frog sitting on the slab, electric glow
    FX, FY = 1290, SY + 2
    b += monster(FX, FY, 3.5, extra=4, mouth='smile', look=(-2, 1), glow='#9fe6ff')
    # head clamp + cables up to the ceiling
    b += f'<path d="M{FX - 80} {FY - 296} q-60 -120 -170 -300 M{FX + 90} {FY - 296} q50 -150 160 -300" stroke="#0c0f14" stroke-width="12" fill="none"/>'
    b += f'<path d="M{FX - 88} {FY - 300} a96 30 0 0 1 192 0" stroke="#9aa3ad" stroke-width="12" fill="none"/>'
    for cx_ in (FX - 88, FX + 104):
        b += f'<rect x="{cx_ - 14}" y="{FY - 314}" width="28" height="30" rx="5" fill="#b8c0c8" stroke="#0a0d12" stroke-width="4"/>'
    # sparks around the frog
    for sx_, sy_, ss in ((FX - 210, FY - 330, 22), (FX + 230, FY - 260, 18), (FX - 250, FY - 120, 14), (FX + 260, FY - 380, 14), (1220, 560, 10)):
        b += spark(sx_, sy_, ss, col='#e6f8ff')
    # control panel + knife switch on the left of the slab, with the flatworm scientist
    PX, PY = 760, 600
    b += f'<rect x="{PX}" y="{PY}" width="170" height="260" rx="10" fill="#2f3540" stroke="#0a0d12" stroke-width="5"/>'
    for k, c in enumerate(('#ff6a5a', '#ffd36a', '#7fe08a')):
        b += f'<circle cx="{PX + 40 + k * 45}" cy="{PY + 36}" r="11" fill="{c}" stroke="#0a0d12" stroke-width="3"/><circle cx="{PX + 40 + k * 45}" cy="{PY + 36}" r="20" fill="{c}" opacity=".35" filter="url(#b6)"/>'
    b += f'<circle cx="{PX + 85}" cy="{PY + 110}" r="36" fill="#d8dccf" stroke="#0a0d12" stroke-width="4"/><path d="M{PX + 85} {PY + 110} l22 -20" stroke="#c0392b" stroke-width="5"/>'
    b += f'<rect x="{PX + 50}" y="{PY + 170}" width="70" height="26" rx="4" fill="#1a1d22"/>'
    b += f'<path d="M{PX + 85} {PY + 186} L{PX + 160} {PY + 120}" stroke="#c9d1d9" stroke-width="12"/><rect x="{PX + 150}" y="{PY + 98}" width="44" height="22" rx="8" transform="rotate(-42 {PX + 172} {PY + 109})" fill="#2a2a2a" stroke="#0a0d12" stroke-width="3"/>'
    # flatworm: flat leaf-shaped pale pink body, coiled tail on the switch handle, goggles
    W = f'<g transform="translate({PX + 250} {PY + 230}) scale(1.35)" stroke="{INK}" stroke-linejoin="round" stroke-linecap="round">'
    W += '<path d="M-10 40 q-30 -20 -20 -70 q10 -50 40 -90 q16 -20 36 -10 q20 14 6 50 q-16 40 -12 80 q2 30 -18 44 q-20 10 -32 -4z" fill="#f2b7a8" stroke-width="4"/>'
    W += '<path d="M16 -88 q-20 30 -24 70 q-4 30 6 52" stroke="#d98d7c" stroke-width="4" fill="none" opacity=".8"/>'
    W += '<path d="M-28 20 q-40 -10 -62 -90" stroke-width="13" fill="none"/><path d="M-28 20 q-40 -10 -62 -90" stroke="#f2b7a8" stroke-width="8" fill="none"/>'
    W += '<path d="M14 -92 q30 -6 40 10" stroke="#1a1d22" stroke-width="5" fill="none"/>'
    W += '<circle cx="18" cy="-82" r="12" fill="#bfe8ff" stroke-width="4"/><circle cx="44" cy="-74" r="12" fill="#bfe8ff" stroke-width="4"/><path d="M30 -78 l2 2" stroke-width="4"/>'
    W += '<circle cx="18" cy="-82" r="4" fill="#1d2b1c" stroke="none"/><circle cx="44" cy="-74" r="4" fill="#1d2b1c" stroke="none"/>'
    W += '<path d="M24 -56 q10 8 18 -2" fill="none" stroke-width="3.4"/>'
    W += '</g>'
    b += W
    # foreground lab bench with flasks, the mascot frog in a lab coat peeking over it
    coat = ('<path d="M-33 -34 q36 12 74 0 l3 34 q-40 10 -80 0z" fill="#eef2f5" stroke-width="3.4"/>'
            '<path d="M-2 -30 l6 18 l6 -18" fill="none" stroke-width="2.6"/><rect x="18" y="-18" width="12" height="9" rx="2" fill="#dfe6ea" stroke-width="2.2"/>')
    goggles = ('<path d="M-24 -84 q30 -14 60 0" stroke="#3a3a3a" stroke-width="5" fill="none"/>'
               '<circle cx="-8" cy="-88" r="9" fill="#ffd36a" stroke-width="3"/><circle cx="22" cy="-88" r="9" fill="#ffd36a" stroke-width="3"/>')
    b += frog(470, 905, 3.2, mouth='o', arms=('q-18 -8 -22 -30', 'q18 -8 22 -30'), look=(5, -2), torso=coat, head=goggles)
    b += '<rect x="120" y="900" width="760" height="40" rx="6" fill="#4a3424" stroke="#120c08" stroke-width="5"/>'
    b += '<rect x="140" y="940" width="720" height="160" fill="#2a1d14" stroke="#120c08" stroke-width="5"/>'
    for fx, fc, fh in ((210, '#7fe08a', 120), (790, '#ff8fd1', 100)):
        b += f'<ellipse cx="{fx}" cy="{900 - fh / 2}" rx="60" ry="60" fill="{fc}" opacity=".35" filter="url(#b24)"/>'
        b += f'<path d="M{fx - 12} {900 - fh} l0 {fh * .4:.0f} l-36 {fh * .6 - 4:.0f} q0 4 4 4 l88 0 q4 0 4 -4 l-36 {-(fh * .6 - 4):.0f} l0 {-fh * .4:.0f} z" fill="#bfe8ff" fill-opacity=".25" stroke="#d9f2ff" stroke-width="4"/>'
        b += f'<path d="M{fx - 40} {900 - 14} l80 0 l-14 -{fh * .3:.0f} l-52 0z" fill="{fc}" opacity=".85"/>'
        for _ in range(4):
            b += f'<circle cx="{fx + random.randint(-14, 14)}" cy="{900 - fh - random.randint(10, 60)}" r="{random.randint(4, 9)}" fill="none" stroke="{fc}" stroke-width="3" opacity=".8"/>'
    b += '<rect width="1920" height="1080" fill="url(#vigA)"/>'
    lines = [('MADE BY', 150, 'w'), ('A WORM', 230, 'y')]
    return page('#121822', svg(defs, b), lines, outline='#070a10')


# ======================= B: 1 WORM, 3 HOSTS (intuitive cycle) =======================
def thumb_B():
    random.seed(5)
    defs = FILTERS
    defs += lin('skyB', [(0, '#f3a35e'), (.55, '#f8cf8e'), (1, '#fde8b8')])
    defs += lin('waterB', [(0, '#5a9a7a'), (.4, '#2f6b58'), (1, '#12302a')])
    defs += rad('sunB', 1500, 470, 520, [(0, '#fff3c4', .9), (.3, '#ffd98a', .35), (1, '#ffd98a', 0)])
    defs += ('<radialGradient id="shellG" cx="-40" cy="-80" r="190" gradientUnits="userSpaceOnUse"><stop offset="0" stop-color="#f0a46a"/>'
             '<stop offset=".55" stop-color="#a2512c"/><stop offset="1" stop-color="#4a1d0e"/></radialGradient>')
    defs += ('<radialGradient id="tadG" cx="-30" cy="-30" r="120" gradientUnits="userSpaceOnUse"><stop offset="0" stop-color="#9a9a5a"/>'
             '<stop offset="1" stop-color="#4a4a26"/></radialGradient>')
    defs += lin('wingB', [(0, '#c9d2da'), (1, '#6c7a88')])
    defs += rad('vigB', 960, 540, 1150, [(0, '#000', 0), (.65, '#000', 0), (1, '#000', .55)])
    WL = 560
    b = f'<rect width="1920" height="{WL}" fill="url(#skyB)"/>'
    b += f'<rect width="1920" height="{WL}" fill="url(#sunB)"/>'
    b += '<circle cx="1500" cy="470" r="70" fill="#fff6d8" opacity=".9"/>'
    # far shore: tree line + reeds
    b += f'<path d="M0 {WL - 40} q120 -50 240 -20 q140 -60 300 -10 q160 -40 320 0 q200 -50 380 -6 q180 -40 340 0 q140 -30 340 6 L1920 {WL} L0 {WL}z" fill="#5d7a4a" opacity=".75"/>'
    b += f'<path d="M0 {WL - 14} q300 -26 640 -4 q400 -22 760 0 q300 -14 520 4 L1920 {WL} L0 {WL}z" fill="#3e5a36"/>'
    for _ in range(70):
        rx = random.randint(0, 1920); rh = random.randint(30, 90)
        b += f'<path d="M{rx} {WL} q{random.randint(-8, 8)} {-rh / 2} {random.randint(-14, 14)} {-rh}" stroke="#2f4a2a" stroke-width="3" fill="none"/>'
    # water body
    b += f'<rect y="{WL}" width="1920" height="{1080 - WL}" fill="url(#waterB)"/>'
    b += f'<path d="M0 {WL} L1920 {WL}" stroke="#fff3c4" stroke-width="4" opacity=".8"/>'
    for k in range(7):   # light rays
        x0 = 1200 + k * 90
        b += f'<path d="M{x0} {WL} L{x0 + 60} {WL} L{x0 - 260} 1080 L{x0 - 360} 1080z" fill="#d8ffe8" opacity=".06"/>'
    for _ in range(30):
        b += f'<path d="M{random.randint(0, 1920)} {WL + random.randint(8, 30)} l{random.randint(30, 90)} 0" stroke="#e8fff0" stroke-width="2" opacity=".35"/>'
    # mud bottom + plants
    b += '<path d="M0 960 q300 -40 600 -10 q500 30 900 -6 q240 -16 420 0 L1920 1080 L0 1080z" fill="#1d2a1e"/>'
    for _ in range(40):
        b += f'<ellipse cx="{random.randint(0, 1920)}" cy="{random.randint(990, 1070)}" rx="{random.randint(6, 18)}" ry="{random.randint(4, 9)}" fill="#33402e"/>'
    for px in (70, 140, 1880):
        for k in range(3):
            b += f'<path d="M{px + k * 18} 1000 q{-20 + k * 10} -160 {10 + k * 6} -{260 + k * 30}" stroke="#2e5a3a" stroke-width="10" fill="none" opacity=".9"/>'
    # ---- the cycle: a glowing gold loop (snail -> tadpole -> heron -> back to snail)
    loop = 'M930 850 C1120 900 1260 840 1340 760 M1500 640 C1580 520 1560 430 1520 380 M1150 330 C860 360 640 520 700 720'
    b += f'<path d="{loop}" stroke="#F2D27A" stroke-width="40" opacity=".35" fill="none" filter="url(#b12)" stroke-linecap="round"/>'
    b += f'<path d="{loop}" stroke="#F2D27A" stroke-width="12" fill="none" stroke-dasharray="26 18" stroke-linecap="round"/>'
    for (ax, ay, ang) in ((1340, 760, -40), (1520, 380, -115), (700, 720, 80)):
        b += f'<path transform="translate({ax} {ay}) rotate({ang})" d="M18 0 L-22 -24 L-12 0 L-22 24z" fill="#F2D27A" stroke="#5a3a10" stroke-width="4" stroke-linejoin="round"/>'
    # eggs dropping from the bird toward the pond
    for k, (ex, ey) in enumerate(((1010, 360), (880, 410), (790, 490), (740, 600))):
        b += f'<ellipse cx="{ex}" cy="{ey}" rx="9" ry="12" fill="#fff4c8" stroke="#5a3a10" stroke-width="3"/>'
    # host 1: ramshorn snail
    b += '<ellipse cx="760" cy="880" rx="260" ry="200" fill="#ffd98a" opacity=".25" filter="url(#b50)"/>'
    b += snail(780, 860, 1.25)
    # cercariae streaming from the snail to the tadpole
    for k in range(16):
        t = k / 15
        cx_ = 900 + t * 520 + random.randint(-30, 30); cy_ = 760 - t * 70 + random.randint(-50, 50)
        b += f'<circle cx="{cx_}" cy="{cy_}" r="14" fill="#cff6ff" opacity=".3" filter="url(#b6)"/>'
        b += cerc(cx_, cy_, -10 + random.randint(-20, 20), s=1.2)
    # host 2: tadpole, glowing limb buds
    b += tadpole(1500, 700, 1.25)
    # host 3: flying heron (wings up), top right
    b += '<ellipse cx="1440" cy="240" rx="330" ry="180" fill="#fff3c4" opacity=".35" filter="url(#b50)"/>'
    b += fly_heron(1420, 290, 1.55)
    # mascot frog with a snorkel mask, under water bottom-left, watching the loop
    mask = ('<rect x="-28" y="-82" width="66" height="32" rx="14" fill="#bfe8ff" fill-opacity=".35" stroke-width="3.4"/>'
            '<path d="M-28 -66 l-8 2 M38 -66 l6 2" stroke-width="4"/><path d="M42 -60 q10 -2 10 -16 l0 -40" stroke="#f08a3c" stroke-width="9" fill="none"/>'
            '<path d="M42 -60 q10 -2 10 -16 l0 -40" stroke="' + INK + '" stroke-width="2" fill="none" opacity=".4"/>')
    b += frog(360, 1010, 3.1, mouth='o', arms=('q-18 -8 -24 -28', 'q16 6 20 22'), look=(4, -4), head=mask)
    for k in range(6):
        b += f'<circle cx="{530 + k * 8 + random.randint(-6, 6)}" cy="{640 - k * 46}" r="{6 + k}" fill="none" stroke="#e8fff8" stroke-width="3" opacity=".7"/>'
    b += spark(1640, 120, 20) + spark(1060, 470, 14) + spark(1660, 600, 16) + spark(620, 760, 12)
    b += '<rect width="1920" height="1080" fill="url(#vigB)"/>'
    lines = [('1 WORM', 170, 'w'), ('3 HOSTS', 210, 'y')]
    return page('#12302a', svg(defs, b), lines, outline='#1a1206')


# ======================= C: The Birds (Hitchcock) =======================
def thumb_C():
    random.seed(9)
    defs = FILTERS
    defs += lin('skyC', [(0, '#9fb0b2'), (.6, '#d5ddd8'), (1, '#e9ece4')])
    defs += rad('spotC', 640, 820, 520, [(0, '#fff6d8', .55), (.5, '#fff0c0', .15), (1, '#fff0c0', 0)])
    defs += rad('vigC', 960, 540, 1150, [(0, '#000', 0), (.6, '#000', 0), (1, '#000', .55)])
    HZ = 700
    b = f'<rect width="1920" height="1080" fill="url(#skyC)"/>'
    for _ in range(12):
        b += f'<ellipse cx="{random.randint(0, 1920)}" cy="{random.randint(40, 420)}" rx="{random.randint(160, 320)}" ry="{random.randint(40, 80)}" fill="#8e9ea2" opacity=".35" filter="url(#b24)"/>'
    # hills and pond
    b += f'<path d="M0 {HZ - 60} q240 -70 520 -30 q300 -80 600 -20 q300 -60 800 0 L1920 {HZ} L0 {HZ}z" fill="#7d8f80"/>'
    b += f'<path d="M0 {HZ - 20} q400 -40 900 -10 q500 -30 1020 0 L1920 {HZ} L0 {HZ}z" fill="#61746a"/>'
    b += f'<rect y="{HZ}" width="1920" height="{1080 - HZ}" fill="#7f9690"/>'
    b += f'<path d="M0 {HZ} L1920 {HZ}" stroke="#d9e2dc" stroke-width="3"/>'
    for _ in range(26):
        b += f'<path d="M{random.randint(0, 1920)} {random.randint(HZ + 10, 860)} l{random.randint(40, 120)} 0" stroke="#c6d3cc" stroke-width="2" opacity=".5"/>'
    # shore (foreground grass)
    b += '<path d="M0 840 q300 -30 700 -10 q500 20 1220 -20 L1920 1080 L0 1080z" fill="#4c5f3e"/>'
    for _ in range(140):
        gx = random.randint(0, 1920); gy = random.randint(860, 1075)
        b += f'<path d="M{gx} {gy} q{random.randint(-6, 6)} -14 {random.randint(-10, 10)} -{random.randint(18, 34)}" stroke="#6e8456" stroke-width="3" fill="none" opacity=".8"/>'
    # the wooden climbing frame (old dock posts and rails) behind the bench, right side
    FX0, FX1, FT, FB = 960, 1800, 210, 840
    cols = [FX0 + i * (FX1 - FX0) / 5 for i in range(6)]
    rows = [FT + j * (FB - FT - 60) / 4 for j in range(5)]
    for x in cols:
        b += f'<rect x="{x - 9:.0f}" y="{FT - 20}" width="18" height="{FB - FT + 20}" fill="#3c3a34" stroke="#22211d" stroke-width="3"/>'
    for y in rows:
        b += f'<rect x="{FX0 - 20}" y="{y - 7:.0f}" width="{FX1 - FX0 + 40}" height="14" fill="#4a463c" stroke="#22211d" stroke-width="3"/>'
    for i in range(5):   # diagonal braces
        b += f'<path d="M{cols[i]:.0f} {rows[3]:.0f} L{cols[i + 1]:.0f} {rows[4]:.0f}" stroke="#3c3a34" stroke-width="9"/>'
    # herons perched on every rail: dark slate silhouettes with a pale rim
    for j, y in enumerate(rows):
        n = 7 - (j % 2)
        for i in range(n):
            hx = FX0 + 20 + i * (FX1 - FX0 - 40) / (n - 1) + random.randint(-18, 18)
            sc = .5 + random.uniform(-.04, .04) - j * .01
            b += heron(hx, y - 6, sc, flip=random.random() < .8, sil=random.choice(['#2c3338', '#323a40', '#262c30']))
    # more herons gliding in
    for (fx_, fy_, fs) in ((800, 170, .75), (600, 300, .5), (1760, 110, .55), (1060, 80, .45)):
        b += fly_heron(fx_, fy_, fs, sil='#2c3338')
    # soft light patch on the bench (the focal spot)
    b += '<rect width="1920" height="1080" fill="url(#spotC)"/>'
    # park bench
    BX0, BX1, BY = 230, 1010, 880
    b += f'<ellipse cx="{(BX0 + BX1) / 2}" cy="{BY + 120}" rx="430" ry="30" fill="#000" opacity=".35" filter="url(#b12)"/>'
    for lx in (BX0 + 50, BX1 - 50):
        b += f'<rect x="{lx - 14}" y="{BY}" width="28" height="120" fill="#2a2a28" stroke="#121210" stroke-width="4"/>'
    for k in range(3):   # back slats
        b += f'<rect x="{BX0}" y="{BY - 230 + k * 50}" width="{BX1 - BX0}" height="34" rx="6" fill="#9a6f44" stroke="#3a2614" stroke-width="4"/>'
        b += f'<path d="M{BX0 + 10} {BY - 222 + k * 50} L{BX1 - 10} {BY - 222 + k * 50}" stroke="#c99a68" stroke-width="3" opacity=".7"/>'
    for lx in (BX0 + 50, BX1 - 50):
        b += f'<rect x="{lx - 10}" y="{BY - 240}" width="20" height="240" fill="#2a2a28" stroke="#121210" stroke-width="4"/>'
    # the frogs sit on the seat (drawn before the seat front so feet rest on it)
    scarf = ('<path d="M-32 -34 q36 12 72 0 l-2 12 q-34 10 -68 0z" fill="#d95b6a" stroke-width="3.2"/>'
             '<path d="M20 -26 l10 30 l12 -4 l-12 -28z" fill="#d95b6a" stroke-width="2.8"/>'
             '<path d="M-26 -30 q30 8 60 0" stroke="#f4a7b0" stroke-width="2.6" fill="none"/>')
    b += frog(420, BY - 4, 3.3, mouth='o', arms=('q-12 8 -12 24', 'q14 6 16 22'), look=(6, -4), torso=scarf, sweat=True)
    b += monster(790, BY - 4, 2.6, pick=[1, 3, 4], mouth='smile', look=(-3, 1))
    b += f'<rect x="{BX0 - 20}" y="{BY - 6}" width="{BX1 - BX0 + 40}" height="34" rx="6" fill="#a87a4c" stroke="#3a2614" stroke-width="4"/>'
    b += f'<path d="M{BX0} {BY + 2} L{BX1} {BY + 2}" stroke="#d9a874" stroke-width="3"/>'
    b += spark(620, 520, 14, col='#fffbe8') + spark(900, 600, 10, col='#fffbe8')
    b += '<rect width="1920" height="1080" fill="url(#vigC)"/>'
    lines = [('WHY', 150, 'w'), ('CRIPPLE', 200, 'y'), ('IT?', 150, 'w')]
    return page('#9fb0b2', svg(defs, b), lines, outline='#141a1c')


for n, fn in (('A', thumb_A), ('B', thumb_B), ('C', thumb_C)):
    open(os.path.join(HERE, f'{n}.html'), 'w').write(fn())
print('ok')
