# Thumbnails A-C for first-virus-origin (guideline 16-6 / 16-8, brief tools/briefs/thumb_art.md). Run: python3 videos/first-virus-origin/thumb/make.py
# A  A VIRUS / BIGGER / THAN BACTERIA?   (question)  homage: Gulliver's Travels (Gulliver tied down on the beach by the Lilliputians,
#    public-domain book illustrations): a giant hairy Mimivirus lies on a Chilean shore at sunset, tied down by tiny phages; two bacteria
#    lie next to it for scale; explorer frog with a magnifying glass. Script: "colossal viruses ... Mimivirus and Pandoravirus, were larger
#    than some species of bacteria" (sediments off the coast of Chile).
# B  YOU ARE / PART / VIRUS   (declarative)  intuitive: a huge neon DNA helix with one glowing magenta stretch; a retrovirus sews its code
#    into it with needle and thread; lab frog. Script: retroviruses "stitch their own genetic code into the chromosomes"; "roughly eight
#    percent of our DNA consists of these viral remnants".
# C  OUTNUMBERED / 10 TO 1   (number)  intuitive: one giant seawater droplet lifted from a wave, magnified: 5 bacteria among 50 viruses;
#    snorkel frog. Script: "In every milliliter of natural seawater ... viruses outnumber bacteria about ten to one."
import os, sys, math, random
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', '..', 'tools'))
from thumb_lib import page, svg, lin, rad, spark

INK = '#1d2b1c'; GREEN = '#6aa55a'; DARKG = '#4d8a4a'; BELLY = '#9cc98a'
FILTERS = ''.join(f'<filter id="b{n}" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="{n}"/></filter>' for n in (2, 4, 8, 14, 26, 50, 90))


def P(pts):
    return ' '.join(f'{a:.1f},{b:.1f}' for a, b in pts)


def hx(c):
    c = c.lstrip('#'); return [int(c[i:i + 2], 16) for i in (0, 2, 4)]


def mix(a, b, t):
    t = max(0, min(1, t)); A, B = hx(a), hx(b)
    return '#' + ''.join(f'{round(A[i] + (B[i] - A[i]) * t):02x}' for i in range(3))


# ---------------- mascot frog (tools/assets/frog.svg body), posable; pupils clamped inside the whites (eyecheck) ----------------
def limb(d, w=7.5, wi=3.4):
    return f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="{w}"/><path d="{d}" fill="none" stroke="{GREEN}" stroke-width="{wi}"/>'


def end_of(d):
    n = [float(v) for v in d.replace('M', ' ').replace('q', ' ').split()]
    return n[0] + n[-2], n[1] + n[-1]


def frog(x, y, s, rot=0, flip=False, look=(0, 0), mouth='O', armL=None, armR=None, brows=True, back='', front='', mid='', top='', shadow=False):
    sx = -s if flip else s
    g = [f'<g transform="translate({x} {y}) rotate({rot}) scale({sx} {s})" stroke="{INK}" stroke-linejoin="round" stroke-linecap="round">', back]
    if shadow:
        g.append('<ellipse cx="0" cy="8" rx="54" ry="9" fill="#000" opacity=".3" stroke="none"/>')
    for fx, fy in ((-22, 4), (22, 4)):
        g.append(f'<ellipse cx="{fx}" cy="{fy}" rx="16" ry="9" fill="{DARKG}" stroke-width="3.2"/>')
    g.append(f'<path d="M-34 0 q-6 -64 34 -70 q40 -2 42 62 q0 10 -6 12 q-36 6 -70 -4z" fill="{GREEN}" stroke-width="4"/>')
    g.append(f'<ellipse cx="2" cy="-12" rx="22" ry="20" fill="{BELLY}" stroke="none" opacity=".7"/>')
    g.append('<path d="M-24 -50 q6 -14 18 -16" fill="none" stroke="#b6dea0" stroke-width="3" opacity=".8"/>')
    g.append(mid)
    lx, ly = look
    _d = math.hypot(1 + lx, ly)
    if _d > 6.9: _k = 6.9 / _d; lx, ly = (1 + lx) * _k - 1, ly * _k
    for ex in (-10, 22):
        g.append(f'<circle cx="{ex}" cy="-66" r="13.5" fill="#f4f5ea" stroke-width="3.2"/>')
        g.append(f'<circle cx="{ex + 1 + lx:.2f}" cy="{-66 + ly:.2f}" r="4.4" fill="{INK}" stroke="none"/>')
        g.append(f'<circle cx="{ex + 2.4 + lx:.2f}" cy="{-67.6 + ly:.2f}" r="1.5" fill="#fff" stroke="none"/>')
    if brows:
        g.append('<path d="M-22 -88 q12 -9 24 -1 M10 -89 q12 -8 24 1" fill="none" stroke-width="3.4"/>')
    if mouth == 'O':
        g.append('<ellipse cx="6" cy="-38" rx="10" ry="12" fill="#7a2f33" stroke-width="3"/><ellipse cx="6" cy="-31" rx="6" ry="4" fill="#e07b7b" stroke="none"/>')
    else:
        g.append('<ellipse cx="6" cy="-41" rx="6" ry="7.5" fill="#7a2f33" stroke-width="3"/>')
    g.append('<ellipse cx="-18" cy="-48" rx="5" ry="3" fill="#e98a8a" stroke="none" opacity=".55"/><ellipse cx="30" cy="-48" rx="5" ry="3" fill="#e98a8a" stroke="none" opacity=".55"/>')
    g.append(top)
    for a in (armL or 'M-34 -22 q-14 6 -16 22', armR or 'M38 -22 q14 6 16 22'):
        g.append(limb(a)); ex_, ey_ = end_of(a)
        g.append(f'<circle cx="{ex_:.1f}" cy="{ey_:.1f}" r="5.6" fill="{GREEN}" stroke-width="3"/>')
    g.append(front); g.append('</g>')
    return ''.join(g)


# ---------------- icosahedral capsid (true 3D icosahedron, flat-shaded) ----------------
PHI = (1 + 5 ** .5) / 2
IV = [(0, a, b * PHI) for a in (-1, 1) for b in (-1, 1)] + [(a, b * PHI, 0) for a in (-1, 1) for b in (-1, 1)] + [(b * PHI, 0, a) for a in (-1, 1) for b in (-1, 1)]
IF = [(i, j, k) for i in range(12) for j in range(i + 1, 12) for k in range(j + 1, 12)
      if all(abs(math.dist(IV[p], IV[q]) - 2) < 1e-6 for p, q in ((i, j), (j, k), (i, k)))]
VN = math.hypot(1, PHI)


def rot3(v, rx, ry, rz):
    x, y, z = v
    c, s = math.cos(rx), math.sin(rx); y, z = y * c - z * s, y * s + z * c
    c, s = math.cos(ry), math.sin(ry); x, z = x * c + z * s, -x * s + z * c
    c, s = math.cos(rz), math.sin(rz); x, y = x * c - y * s, x * s + y * c
    return x, y, z


def hull(pts):
    pts = sorted(set((round(a, 2), round(b, 2)) for a, b in pts))
    def cr(o, a, b): return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
    lo, up = [], []
    for p in pts:
        while len(lo) >= 2 and cr(lo[-2], lo[-1], p) <= 0: lo.pop()
        lo.append(p)
    for p in reversed(pts):
        while len(up) >= 2 and cr(up[-2], up[-1], p) <= 0: up.pop()
        up.append(p)
    return lo[:-1] + up[:-1]


def icosa(cx, cy, R, rx=.35, ry=.5, rz=.1, dark='#123', lite='#9ff', ink='#0a1420', sw=4, light=(-.55, .6, .58), edge='#fff', eop=.35):
    V = [rot3(v, rx, ry, rz) for v in IV]
    S = [(cx + R * x / VN, cy - R * y / VN) for x, y, z in V]
    L = math.sqrt(sum(c * c for c in light)); light = [c / L for c in light]
    faces = []
    for f in IF:
        n = [sum(V[i][a] for i in f) / 3 for a in range(3)]; nl = math.sqrt(sum(c * c for c in n)); n = [c / nl for c in n]
        if n[2] <= 0: continue
        b = max(0, sum(n[a] * light[a] for a in range(3)))
        faces.append((n[2], f, b))
    o = ''
    for z, f, b in sorted(faces):
        o += f'<polygon points="{P([S[i] for i in f])}" fill="{mix(dark, lite, .15 + .85 * b)}" stroke="{ink}" stroke-width="{sw}" stroke-linejoin="round"/>'
        o += f'<polygon points="{P([S[i] for i in f])}" fill="none" stroke="{edge}" stroke-width="{sw * .35:.1f}" stroke-linejoin="round" opacity="{eop * b:.2f}"/>'
    H = hull(S)
    front = max(range(12), key=lambda i: V[i][2])
    return o, H, S[front]


def hull_d(H):
    return 'M' + ' L'.join(f'{a:.1f},{b:.1f}' for a, b in H) + 'Z'


def fibers(H, cx, cy, L, col, ink, step=5, w=3.2, seed=1):
    rnd = random.Random(seed); o = ''; oi = ''
    for k in range(len(H)):
        a, b = H[k], H[(k + 1) % len(H)]
        n = max(1, int(math.dist(a, b) / step))
        for i in range(n):
            t = i / n; x, y = a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t
            dx, dy = x - cx, y - cy; d = math.hypot(dx, dy) or 1; dx, dy = dx / d, dy / d
            l = L * rnd.uniform(.6, 1.15); j = rnd.uniform(-.35, .35)
            ex, ey = x + (dx + j * dy) * l, y + (dy - j * dx) * l
            x0, y0 = x - dx * L * .25, y - dy * L * .25
            oi += f'M{x0:.1f},{y0:.1f} L{ex:.1f},{ey:.1f} '
    o += f'<path d="{oi}" stroke="{ink}" stroke-width="{w + 2.4}" stroke-linecap="round" fill="none"/>'
    o += f'<path d="{oi}" stroke="{col}" stroke-width="{w}" stroke-linecap="round" fill="none"/>'
    return o


def phage(x, y, s=1.0, rot=0, head='#c7b5ff', body='#e9e4f6', ink='#1c1430', glow=False):
    g = f'<g transform="translate({x:.1f} {y:.1f}) rotate({rot}) scale({s})" stroke="{ink}" stroke-linejoin="round" stroke-linecap="round">'
    if glow:
        g += f'<ellipse cx="0" cy="-50" rx="40" ry="56" fill="{head}" opacity=".35" stroke="none" filter="url(#b8)"/>'
    for sd in (-1, 1):
        for i in range(3):
            d = f'M{sd * 3},-2 L{sd * (13 + 6 * i)},{-12 + 4 * i} L{sd * (20 + 8 * i)},16'
            g += f'<path d="{d}" fill="none" stroke-width="5.2"/><path d="{d}" fill="none" stroke="{body}" stroke-width="2.2"/>'
    g += f'<rect x="-9" y="-6" width="18" height="7" rx="2" fill="{body}" stroke-width="2.6"/>'
    g += f'<rect x="-5" y="-38" width="10" height="33" rx="2" fill="{body}" stroke-width="2.6"/>'
    g += ''.join(f'<path d="M-5 {yy} h10" stroke-width="1.6" opacity=".7"/>' for yy in range(-33, -7, 5))
    g += f'<rect x="-9" y="-43" width="18" height="6" rx="2" fill="{body}" stroke-width="2.6"/>'
    hp = [(0, -86), (15, -77), (15, -52), (0, -43), (-15, -52), (-15, -77)]
    g += f'<polygon points="{P(hp)}" fill="{head}" stroke-width="3"/>'
    g += f'<polygon points="-15,-77 0,-68 0,-43 -15,-52" fill="#fff" opacity=".28" stroke="none"/>'
    g += '<path d="M-15 -77 L0 -68 L15 -77 M0 -68 L0 -43" fill="none" stroke-width="1.8" opacity=".75"/>'
    g += '<path d="M-11 -74 L-2 -80" stroke="#fff" stroke-width="2.4" opacity=".8"/>'
    return g + '</g>'


def rod(x, y, L, W, rot, col, ink, hi='#fff', flag=True, seed=0):
    rnd = random.Random(seed)
    g = f'<g transform="translate({x:.1f} {y:.1f}) rotate({rot})" stroke="{ink}" stroke-linejoin="round" stroke-linecap="round">'
    if flag:
        for k in range(3):
            yy = (k - 1) * W * .25; amp = W * .18
            d = f'M{-L / 2:.1f},{yy:.1f} ' + ' '.join(f'q{-L * .08:.1f},{amp * (1 if i % 2 else -1):.1f} {-L * .16:.1f},0' for i in range(5))
            g += f'<path d="{d}" fill="none" stroke-width="3.4" opacity=".85"/><path d="{d}" fill="none" stroke="{mix(col, "#ffffff", .35)}" stroke-width="1.4"/>'
    g += f'<rect x="{-L / 2:.1f}" y="{-W / 2:.1f}" width="{L:.1f}" height="{W:.1f}" rx="{W / 2:.1f}" fill="{col}" stroke-width="{max(2.5, W * .07):.1f}"/>'
    g += f'<rect x="{-L / 2 + W * .2:.1f}" y="{W * .05:.1f}" width="{L - W * .4:.1f}" height="{W * .36:.1f}" rx="{W * .18:.1f}" fill="#000" opacity=".16" stroke="none"/>'
    g += f'<rect x="{-L / 2 + W * .3:.1f}" y="{-W * .36:.1f}" width="{L - W * .7:.1f}" height="{W * .16:.1f}" rx="{W * .08:.1f}" fill="{hi}" opacity=".55" stroke="none"/>'
    for _ in range(int(L / W * 2.5)):
        g += f'<circle cx="{rnd.uniform(-L / 2 + W * .4, L / 2 - W * .4):.1f}" cy="{rnd.uniform(-W * .18, W * .26):.1f}" r="{rnd.uniform(W * .03, W * .07):.1f}" fill="{mix(col, "#000000", .3)}" opacity=".5" stroke="none"/>'
    return g + '</g>'


# ====================================================================== A  Gulliver's Travels homage: the giant virus tied down on the beach
def thumb_A():
    random.seed(101)
    cx, cy, R = 1320, 545, 290
    defs = FILTERS
    defs += lin('skyA', [(0, '#1b2f57'), (.38, '#6a4a7c'), (.66, '#e9875c'), (.82, '#ffc47a'), (1, '#ffe2a6')])
    defs += lin('seaA', [(0, '#ffcf8a'), (.18, '#d07a63'), (1, '#3b3c68')])
    defs += lin('sandA', [(0, '#e9b27a'), (.35, '#c98a5c'), (1, '#5d3a33')])
    defs += rad('sunA', 1640, 640, 520, [(0, '#fff6d8', 1), (.12, '#ffe39c', .9), (.4, '#ffb36b', .35), (1, '#ff9a5a', 0)])
    defs += rad('haloA', cx, cy, 560, [(0, '#bdfff0', .55), (.45, '#7ff0d8', .18), (1, '#7ff0d8', 0)])
    defs += rad('vigA', 960, 520, 1150, [(0, '#000', 0), (.68, '#000', 0), (1, '#000', .55)])
    defs += ('<pattern id="fuzz" width="16" height="16" patternUnits="userSpaceOnUse">'
             '<path d="M2 3 l5 -2 M10 9 l4 3 M4 12 l-2 3 M12 2 l2 4" stroke="#fff3c0" stroke-width="2" stroke-linecap="round" opacity=".3"/></pattern>')
    b = '<rect width="1920" height="1080" fill="url(#skyA)"/>'
    b += ''.join(f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{ry}" fill="#ffd7a8" opacity="{o}" filter="url(#b14)"/>'
                 for x, y, rx, ry, o in ((300, 520, 360, 26, .35), (900, 470, 300, 20, .3), (1500, 400, 380, 24, .35), (1750, 520, 200, 16, .45)))
    b += ''.join(f'<path d="M{x},{y} q12,-10 24,0 q12,-10 24,0" fill="none" stroke="#2a1d33" stroke-width="4" stroke-linecap="round" opacity=".8"/>'
                 for x, y in ((1700, 180), (1780, 230), (1630, 250)))
    b += '<rect width="1920" height="1080" fill="url(#sunA)"/>'
    # sea + horizon
    b += '<rect x="0" y="640" width="1920" height="140" fill="url(#seaA)"/>'
    b += ''.join(f'<rect x="{random.randint(0, 1900)}" y="{random.randint(648, 770)}" width="{random.randint(20, 90)}" height="3" rx="1.5" fill="#fff1c8" opacity="{random.uniform(.3, .8):.2f}"/>' for _ in range(70))
    b += '<path d="M1450,650 L1830,650 L1760,780 L1520,780 Z" fill="#fff3c8" opacity=".35" filter="url(#b14)"/>'
    # sand
    b += '<path d="M0,770 C300,740 700,760 1000,748 C1300,736 1600,752 1920,742 L1920,1080 L0,1080 Z" fill="url(#sandA)"/>'
    b += '<path d="M0,772 C300,742 700,762 1000,750 C1300,738 1600,754 1920,744" fill="none" stroke="#fff6e0" stroke-width="7" opacity=".7"/>'
    b += ''.join(f'<ellipse cx="{random.randint(0, 1920)}" cy="{random.randint(800, 1070)}" rx="{random.randint(10, 40)}" ry="{random.randint(2, 6)}" fill="#7a4c3a" opacity=".35"/>' for _ in range(60))
    b += ''.join(f'<circle cx="{random.randint(0, 1920)}" cy="{random.randint(790, 1070)}" r="{random.choice([1.5, 2.2])}" fill="#fff1d0" opacity=".6"/>' for _ in range(120))
    # giant glow + shadow
    b += f'<ellipse cx="{cx}" cy="{cy}" rx="560" ry="520" fill="url(#haloA)"/>'
    b += f'<ellipse cx="{cx - 60}" cy="{cy + R * .93:.0f}" rx="{R * 1.35:.0f}" ry="70" fill="#2b1420" opacity=".6" filter="url(#b26)"/>'
    caps, H, fv = icosa(cx, cy, R, rx=.42, ry=.62, rz=.18, dark='#0d4a55', lite='#7ff2dc', ink='#06232a', sw=6, light=(-.2, .55, .8), edge='#e8fff8', eop=.6)
    b += fibers(H, cx, cy, 34, '#f6e2a0', '#3a2b12', step=4.5, w=3, seed=3)
    b += f'<path d="{hull_d(H)}" fill="#06232a"/>' + caps
    b += f'<clipPath id="hullA"><path d="{hull_d(H)}"/></clipPath>'
    b += f'<g clip-path="url(#hullA)"><rect x="{cx - R}" y="{cy - R}" width="{2 * R}" height="{2 * R}" fill="url(#fuzz)"/>'
    b += f'<path d="{hull_d(H)}" fill="none" stroke="#ffd59a" stroke-width="40" opacity=".55" filter="url(#b14)" transform="translate(-14 4)"/></g>'
    # stargate (Mimivirus' star-shaped portal) on the front vertex
    sx_, sy_ = fv
    st = ' '.join(f'{sx_ + math.cos(math.radians(-90 + 36 * i)) * (46 if i % 2 == 0 else 14):.1f},{sy_ + math.sin(math.radians(-90 + 36 * i)) * (46 if i % 2 == 0 else 14):.1f}' for i in range(10))
    b += f'<circle cx="{sx_:.0f}" cy="{sy_:.0f}" r="70" fill="#fff3b0" opacity=".55" filter="url(#b14)"/>'
    b += f'<polygon points="{st}" fill="#fff0a8" stroke="#5a3d10" stroke-width="4" stroke-linejoin="round"/>'
    # ropes thrown over the giant, pegged into the sand on both sides (Gulliver)
    sand = (f'<path d="M{cx - R - 80},{cy + R * .86:.0f} C{cx - R},{cy + R * .62:.0f} {cx + R},{cy + R * .62:.0f} {cx + R + 90},{cy + R * .86:.0f} '
            f'L{cx + R + 90},{cy + R + 40:.0f} L{cx - R - 80},{cy + R + 40:.0f} Z" fill="#c98a5c"/>'
            f'<path d="M{cx - R - 80},{cy + R * .86:.0f} C{cx - R},{cy + R * .62:.0f} {cx + R},{cy + R * .62:.0f} {cx + R + 90},{cy + R * .86:.0f}" fill="none" stroke="#f3c58e" stroke-width="6" opacity=".8"/>')
    b += sand
    arcs = [((cx - R + 10, 860), (cx - 40, 260), (cx + R - 20, 850)), ((cx - R + 60, 905), (cx + 60, 420), (cx + R + 10, 890)),
            ((cx - R - 20, 820), (cx - 160, 300), (cx + R - 90, 900)), ((cx - R + 130, 930), (cx + 200, 380), (cx + R + 40, 830))]
    pegs = ''
    for (p0, c1, p1) in arcs:
        d = f'M{p0[0]},{p0[1]} Q{c1[0]},{c1[1]} {p1[0]},{p1[1]}'
        b += f'<path d="{d}" stroke="#2a1a10" stroke-width="14" fill="none" stroke-linecap="round"/><path d="{d}" stroke="#c89a62" stroke-width="8.5" fill="none" stroke-linecap="round"/>'
        b += f'<path d="{d}" stroke="#f3d6a2" stroke-width="3" fill="none" stroke-dasharray="7 9" stroke-linecap="round"/>'
        for q in (p0, p1):
            pegs += f'<rect x="{q[0] - 8}" y="{q[1] - 22}" width="16" height="34" rx="4" fill="#7a5230" stroke="#2a1a10" stroke-width="3.4"/><path d="M{q[0] - 4},{q[1] - 18} l0,22" stroke="#c49a6a" stroke-width="3"/>'
    b += pegs
    # bacteria lying on the sand for scale (smaller than the giant)
    b += f'<ellipse cx="740" cy="915" rx="130" ry="18" fill="#3b1d1c" opacity=".45" filter="url(#b8)"/>'
    b += rod(740, 880, 250, 76, -4, '#f08a6a', '#3a1610', seed=4)
    b += f'<ellipse cx="1755" cy="825" rx="80" ry="12" fill="#3b1d1c" opacity=".4" filter="url(#b8)"/>'
    b += rod(1760, 800, 150, 50, 8, '#f0b04a', '#3a2410', seed=5, flag=False)
    # tiny phages = the Lilliputians: hauling ropes, one climbing a ladder, one planting a flag on top
    for (x, y, sc, r, hd) in ((cx - R - 95, 890, .75, -22, '#c7b5ff'), (cx - R - 40, 945, .7, -18, '#9fd6ff'), (cx - R + 40, 990, .72, -16, '#ffb3d1'),
                              (cx + R + 75, 880, .72, 20, '#9fd6ff'), (cx + R + 110, 925, .66, 22, '#c7b5ff'), (cx - 20, 1000, .7, -6, '#ffd88a')):
        b += phage(x, y, sc, r, head=hd)
    lad = ''
    for k in range(9):
        y0 = 900 - k * 30
        lad += f'M{1455 + k * 5.2:.0f},{y0 + 10} L{1489 + k * 5.2:.0f},{y0 + 10} '
    b += f'<path d="M1452,925 L1500,650 M1490,925 L1538,650" stroke="#2a1a10" stroke-width="9" stroke-linecap="round"/><path d="M1452,925 L1500,650 M1490,925 L1538,650" stroke="#a47744" stroke-width="5" stroke-linecap="round"/>'
    b += f'<path d="{lad}" stroke="#2a1a10" stroke-width="7"/><path d="{lad}" stroke="#a47744" stroke-width="3.5"/>'
    b += phage(1506, 780, .62, -8, head='#ffd88a')
    tx, ty = H[min(range(len(H)), key=lambda i: H[i][1])]
    b += f'<path d="M{tx + 10:.0f},{ty - 30:.0f} l0,-120" stroke="#2a1a10" stroke-width="6"/><path d="M{tx + 10:.0f},{ty - 150:.0f} l70,22 l-70,24 z" fill="#f2d27a" stroke="#2a1a10" stroke-width="4" stroke-linejoin="round"/>'
    b += phage(tx - 20, ty - 26, .6, 6, head='#ffb3d1', glow=True)
    b += spark(1600, 300, 22) + spark(940, 380, 16) + spark(1580, 520, 14) + spark(1110, 230, 12)
    # explorer frog with pith helmet + magnifying glass
    helmet = ('<path d="M-36 -86 Q6 -98 48 -86 Q50 -80 6 -78 Q-38 -80 -36 -86Z" fill="#e4cf98" stroke-width="3.4"/>'
              '<path d="M-22 -88 Q-20 -128 6 -128 Q32 -128 34 -88 Z" fill="#efdcaa" stroke-width="3.6"/>'
              '<path d="M-21 -96 Q6 -90 33 -96" fill="none" stroke="#8a5a2a" stroke-width="6"/><path d="M-12 -118 q10 -6 22 -2" fill="none" stroke="#fff" stroke-width="3" opacity=".7"/>')
    glass = ('<path d="M72 -50 L92 -78" stroke-width="10"/><path d="M72 -50 L92 -78" stroke="#8a5a2a" stroke-width="5"/>'
             '<circle cx="106" cy="-98" r="24" fill="#d8f6ff" fill-opacity=".35" stroke-width="5"/><circle cx="106" cy="-98" r="24" fill="none" stroke="#e8c86a" stroke-width="2.4"/>'
             '<path d="M94 -108 q8 -8 18 -6" fill="none" stroke="#fff" stroke-width="3"/>')
    b += f'<ellipse cx="300" cy="1028" rx="160" ry="22" fill="#3b1d1c" opacity=".45" filter="url(#b8)"/>'
    b += frog(290, 1022, 2.55, look=(5, -3), mouth='O', brows=False, armR='M38 -22 q20 -4 34 -28', top=helmet, front=glass)
    b += '<rect width="1920" height="1080" fill="url(#vigA)"/>'
    lines = [('A VIRUS', 118, 'w'), ('BIGGER', 214, 'y'), ('THAN BACTERIA?', 112, 'w')]
    return page('#1b2f57', svg(defs, b), lines, outline='#120d24')


# ====================================================================== B  intuitive: a retrovirus sews itself into your DNA
def thumb_B():
    random.seed(202)
    defs = FILTERS
    defs += rad('bgB', 1300, 520, 1300, [(0, '#3a1f63', 1), (.45, '#1c1238', 1), (1, '#07050f', 1)])
    defs += rad('glowB', 1290, 520, 380, [(0, '#ff5fa2', .55), (.5, '#ff4f8a', .16), (1, '#ff4f8a', 0)])
    defs += rad('vigB', 960, 540, 1150, [(0, '#000', 0), (.66, '#000', 0), (1, '#000', .6)])
    defs += rad('envB', 1595, 420, 170, [(0, '#ffe0a8', 1), (.5, '#f0a04a', 1), (1, '#7a3a20', 1)])
    b = '<rect width="1920" height="1080" fill="url(#bgB)"/>'
    b += ''.join(f'<circle cx="{random.randint(900, 1900)}" cy="{random.randint(0, 1080)}" r="{random.randint(10, 46)}" fill="{random.choice(["#8a7dff", "#5fe3ff", "#ff7fb8"])}" opacity="{random.uniform(.05, .18):.2f}" filter="url(#b8)"/>' for _ in range(40))
    b += ''.join(f'<circle cx="{random.randint(0, 1920)}" cy="{random.randint(0, 1080)}" r="{random.choice([1.4, 2, 2.6])}" fill="#e8e4ff" opacity="{random.uniform(.15, .6):.2f}"/>' for _ in range(110))
    # helix along a gently curved axis from top-right to bottom-centre
    A0, A1 = (1560, -120), (980, 1200)
    N = 260; amp = 175; turns = 3.3
    ax = lambda t: (A0[0] + (A1[0] - A0[0]) * t + 90 * math.sin(math.pi * t), A0[1] + (A1[1] - A0[1]) * t)
    dx, dy = A1[0] - A0[0], A1[1] - A0[1]; ln = math.hypot(dx, dy); nx, ny = -dy / ln, dx / ln
    VIR = (.40, .51)   # the viral stretch (~8% of the visible strand; stylised)

    def pt(t, ph):
        a = 2 * math.pi * turns * t + ph; X, Y = ax(t)
        return X + nx * amp * math.sin(a), Y + ny * amp * math.sin(a), math.cos(a)
    def runs(ph, front):
        out, cur = [], []
        for i in range(N + 1):
            t = i / N; p = pt(t, ph)
            if (p[2] >= 0) == front: cur.append((t, p))
            elif cur:
                cur.append((t, p)); out.append(cur); cur = []
        if cur: out.append(cur)
        return out

    def strand(run, c, f):
        pts = [(p[0], p[1]) for t, p in run]
        o = f'<polyline points="{P(pts)}" fill="none" stroke="#0b0618" stroke-width="{38 + 12 * f}" stroke-linecap="round" stroke-linejoin="round"/>'
        o += f'<polyline points="{P(pts)}" fill="none" stroke="{mix("#24124a", c[0], .45 + .55 * f)}" stroke-width="{28 + 10 * f}" stroke-linecap="round" stroke-linejoin="round"/>'
        vp = [(p[0], p[1]) for t, p in run if VIR[0] <= t <= VIR[1]]
        if len(vp) > 1:
            o += f'<polyline points="{P(vp)}" fill="none" stroke="{mix("#4a0f2a", "#ff3f86", .45 + .55 * f)}" stroke-width="{28 + 10 * f}" stroke-linecap="round" stroke-linejoin="round"/>'
        if f > .5:
            o += f'<polyline points="{P(pts)}" fill="none" stroke="{c[1]}" stroke-width="7" stroke-linecap="round" opacity=".75" transform="translate(-6 -6)"/>'
            if len(vp) > 1:
                o += f'<polyline points="{P(vp)}" fill="none" stroke="#ffd0e4" stroke-width="7" stroke-linecap="round" opacity=".9" transform="translate(-6 -6)"/>'
        return o
    C1, C2 = ('#3fd2ff', '#c8f6ff'), ('#8f7bff', '#e4dcff')
    back = ''.join(strand(r, C1, 0) for r in runs(0, False)) + ''.join(strand(r, C2, 0) for r in runs(math.pi, False))
    rungs = ''
    nr = 50
    for k in range(nr):
        t = (k + .5) / nr
        x0, y0, z0 = pt(t, 0); x1, y1, z1 = pt(t, math.pi); mx, my = (x0 + x1) / 2, (y0 + y1) / 2
        vir = VIR[0] <= t <= VIR[1]
        ca, cb_ = (('#ffe27a', '#ff6fa8') if vir else [('#ffcf6a', '#6fe8b0'), ('#ff8f7a', '#7fb8ff')][k % 2])
        for (ax_, ay_, bx_, by_, cc) in ((x0, y0, mx, my, ca), (mx, my, x1, y1, cb_)):
            rungs += f'<path d="M{ax_:.1f},{ay_:.1f} L{bx_:.1f},{by_:.1f}" stroke="#0b0618" stroke-width="17" stroke-linecap="round"/>'
            rungs += f'<path d="M{ax_:.1f},{ay_:.1f} L{bx_:.1f},{by_:.1f}" stroke="{cc}" stroke-width="10" stroke-linecap="round"/>'
        if vir:
            rungs += f'<circle cx="{mx:.0f}" cy="{my:.0f}" r="22" fill="#ff6fa8" opacity=".55" filter="url(#b8)"/>'
    front = ''.join(strand(r, C1, 1) for r in runs(0, True)) + ''.join(strand(r, C2, 1) for r in runs(math.pi, True))
    body = back + rungs + front
    xv, yv, _ = pt(sum(VIR) / 2, 0)
    b += f'<ellipse cx="{xv:.0f}" cy="{yv + 40:.0f}" rx="300" ry="220" fill="#ff3f86" opacity=".45" filter="url(#b50)"/>'
    b += f'<ellipse cx="1290" cy="520" rx="420" ry="380" fill="url(#glowB)"/>'
    b += f'<g filter="url(#b26)" opacity=".5">{body}</g>' + body
    # glow sparks on the viral stretch
    for t in (.44, .47, .5):
        x, y, _ = pt(t, 0); b += spark(x + 20, y - 10, 16, '#ffe2f0')
    # retrovirus (enveloped sphere with spikes) on the right, sewing its code in
    vx, vy, vr = 1640, 470, 112
    b += f'<circle cx="{vx}" cy="{vy}" r="{vr * 1.9:.0f}" fill="#ffb35f" opacity=".22" filter="url(#b26)"/>'
    sp = ''
    for i in range(26):
        a = 2 * math.pi * i / 26 + .1; ca_, sa = math.cos(a), math.sin(a)
        x0, y0 = vx + ca_ * vr * .9, vy + sa * vr * .9; x1, y1 = vx + ca_ * (vr + 34), vy + sa * (vr + 34)
        sp += f'<path d="M{x0:.1f},{y0:.1f} L{x1:.1f},{y1:.1f}" stroke="#2a1208" stroke-width="11" stroke-linecap="round"/><path d="M{x0:.1f},{y0:.1f} L{x1:.1f},{y1:.1f}" stroke="#ffd59a" stroke-width="5" stroke-linecap="round"/>'
        sp += f'<circle cx="{x1:.1f}" cy="{y1:.1f}" r="10" fill="#ffe7a6" stroke="#2a1208" stroke-width="4"/>'
    b += sp
    b += f'<circle cx="{vx}" cy="{vy}" r="{vr}" fill="url(#envB)" stroke="#2a1208" stroke-width="7"/>'
    b += ''.join(f'<circle cx="{vx + r_ * math.cos(a_):.1f}" cy="{vy + r_ * math.sin(a_):.1f}" r="{rr}" fill="#c2702e" opacity=".45"/>' for r_, a_, rr in ((50, 2.2, 14), (70, .4, 10), (30, 4.3, 12), (80, 3.4, 9), (60, 5.4, 11)))
    # capsid core showing through
    core, Hc, _ = icosa(vx + 6, vy + 8, 58, rx=.3, ry=.4, dark='#7a1f4a', lite='#ff9cc8', ink='#3a0820', sw=3.4, eop=.7)
    b += f'<g opacity=".92">{core}</g>'
    b += f'<path d="M{vx - 70},{vy - 64} a{vr * .9:.0f},{vr * .9:.0f} 0 0 1 80,-40" fill="none" stroke="#fff6dc" stroke-width="9" stroke-linecap="round" opacity=".8"/>'
    # the thread: from the capsid core, through a needle, sewn into the helix (stitches over the viral stretch)
    xa, ya, _ = pt(.455, 0); xb, yb, _ = pt(.505, math.pi)
    nxp, nyp = 1430, 600
    thread = f'M{vx - 20},{vy + 30} C{vx - 120},{vy + 170} {nxp + 120},{nyp - 40} {nxp},{nyp}'
    b += f'<path d="{thread}" fill="none" stroke="#ff4f8a" stroke-width="14" opacity=".45" filter="url(#b8)"/>'
    b += f'<path d="{thread}" fill="none" stroke="#3a0820" stroke-width="10" stroke-linecap="round"/><path d="{thread}" fill="none" stroke="#ff7fb0" stroke-width="5" stroke-linecap="round"/>'
    st = ''
    for t in (.445, .47, .495):
        x0, y0, _ = pt(t, 0); x1, y1, _ = pt(t + .012, math.pi)
        st += f'M{x0 + 10:.0f},{y0 - 14:.0f} L{x1 - 10:.0f},{y1 + 14:.0f} '
    b += f'<path d="{st}" stroke="#3a0820" stroke-width="9" stroke-linecap="round"/><path d="{st}" stroke="#ffb3d1" stroke-width="4.5" stroke-linecap="round" stroke-dasharray="14 8"/>'
    # silver needle piercing the helix
    ang = math.radians(-32); Lnd = 300
    ex, ey = nxp + math.cos(ang) * -Lnd, nyp + math.sin(ang) * -Lnd
    b += f'<g transform="translate({nxp} {nyp}) rotate({math.degrees(ang):.1f})">'
    b += f'<path d="M0,-9 L-{Lnd},-3 L-{Lnd + 30},0 L-{Lnd},3 L0,9 Q14,0 0,-9 Z" fill="#dfe6f0" stroke="#1b1d2a" stroke-width="5" stroke-linejoin="round"/>'
    b += f'<path d="M-6,-4 L-{Lnd - 10},-1" stroke="#ffffff" stroke-width="3" opacity=".9"/><ellipse cx="-18" cy="0" rx="10" ry="3.4" fill="#2a1d33"/></g>'
    b += spark(ex - 10, ey - 6, 20)
    b += spark(1780, 300, 18) + spark(1250, 150, 14) + spark(1110, 760, 14) + spark(1520, 820, 16)
    # lab frog in a white coat, holding up a glowing test tube
    coat = ('<path d="M-37 2 Q-42 -34 -16 -52 L-4 -22 L-2 4 Z" fill="#f2f4fa" stroke-width="3.4"/>'
            '<path d="M41 2 Q46 -34 20 -52 L8 -22 L6 4 Z" fill="#f2f4fa" stroke-width="3.4"/>'
            '<path d="M-16 -52 L-6 -38 M20 -52 L10 -38" fill="none" stroke-width="2.6"/><rect x="18" y="-24" width="12" height="9" rx="2" fill="#cfd6e4" stroke-width="2"/>')
    tube = ('<g transform="translate(-58 -66) rotate(-14)"><circle cx="0" cy="-16" r="34" fill="#ff5fa2" opacity=".45" stroke="none" filter="url(#b8)"/>'
            '<rect x="-9" y="-46" width="18" height="54" rx="9" fill="#e9f4ff" fill-opacity=".45" stroke-width="3.2"/>'
            '<rect x="-6.5" y="-20" width="13" height="25" rx="6.5" fill="#ff6fae" stroke="none"/><rect x="-12" y="-50" width="24" height="7" rx="3" fill="#cfd6e4" stroke-width="2.6"/>'
            '<path d="M-4 -40 l0 26" stroke="#fff" stroke-width="2.4" opacity=".8"/></g>')
    b += f'<ellipse cx="310" cy="1030" rx="170" ry="24" fill="#000" opacity=".45" filter="url(#b8)"/>'
    b += frog(300, 1024, 2.6, look=(5, -3), mouth='O', mid=coat, armL='M-34 -24 q-20 -6 -24 -34', front=tube)
    b += '<rect width="1920" height="1080" fill="url(#vigB)"/>'
    lines = [('YOU ARE', 132, 'w'), ('PART', 196, 'w'), ('VIRUS', 236, 'y')]
    return page('#1c1238', svg(defs, b), lines, outline='#0b0618')


# ====================================================================== C  intuitive: one seawater drop, magnified: 10 viruses per bacterium
def thumb_C():
    random.seed(303)
    cx, cy, R = 1300, 485, 360
    defs = FILTERS
    defs += lin('skyC', [(0, '#0b2a4a'), (.5, '#1d6c86'), (.8, '#58c0c4'), (1, '#bfeee0')])
    defs += lin('seaC', [(0, '#1f8c9c'), (.4, '#0f5470'), (1, '#05182c')])
    defs += rad('inC', cx - 90, cy - 110, R * 1.25, [(0, '#c9fff3', 1), (.45, '#57d0d0', 1), (.85, '#16708e', 1), (1, '#0b3e5e', 1)])
    defs += rad('haloC', cx, cy, R * 1.7, [(0, '#e9fff8', .55), (.4, '#9ff5e6', .22), (1, '#9ff5e6', 0)])
    defs += rad('vigC', 960, 540, 1150, [(0, '#000', 0), (.66, '#000', 0), (1, '#000', .55)])
    defs += rad('rimC', cx, cy, R, [(0, '#000', 0), (.8, '#062a40', 0), (.97, '#062a40', .55), (1, '#e9fff8', .9)])
    defs += f'<clipPath id="dropC"><circle cx="{cx}" cy="{cy}" r="{R}"/></clipPath>'
    b = '<rect width="1920" height="1080" fill="url(#skyC)"/>'
    b += ''.join(f'<circle cx="{random.randint(0, 1920)}" cy="{random.randint(0, 520)}" r="{random.choice([1.3, 1.9, 2.5])}" fill="#eafcff" opacity="{random.uniform(.15, .6):.2f}"/>' for _ in range(90))
    b += '<ellipse cx="1300" cy="760" rx="900" ry="160" fill="#ffd9a0" opacity=".35" filter="url(#b50)"/>'
    b += '<path d="M0,760 L1920,760 L1920,1080 L0,1080 Z" fill="url(#seaC)"/>'
    b += ''.join(f'<path d="M{x},{y} q{w / 4:.0f},-8 {w / 2:.0f},0 q{w / 4:.0f},8 {w / 2:.0f},0" fill="none" stroke="#bff3ff" stroke-width="3" opacity="{random.uniform(.25, .6):.2f}"/>'
                 for x, y, w in [(random.randint(0, 1880), random.randint(770, 1060), random.randint(40, 120)) for _ in range(55)])
    b += f'<ellipse cx="{cx}" cy="{cy}" rx="{R * 1.7:.0f}" ry="{R * 1.7:.0f}" fill="url(#haloC)"/>'
    # ripples on the sea surface under the drop + spray: the drop was flung up from the sea
    for k, (rx, ry, op) in enumerate(((150, 16, .8), (250, 28, .55), (360, 40, .35))):
        b += f'<ellipse cx="{cx}" cy="{872 + k * 8}" rx="{rx}" ry="{ry}" fill="none" stroke="#dffcff" stroke-width="{6 - k * 1.5}" opacity="{op}"/>'
    b += f'<ellipse cx="{cx}" cy="872" rx="200" ry="26" fill="#dffcff" opacity=".25" filter="url(#b14)"/>'
    for i in range(16):
        a = math.radians(random.uniform(-170, -10)); d = random.uniform(60, 200)
        x, y = cx + math.cos(a) * d * 1.9, 860 + math.sin(a) * d * .45
        r = random.uniform(5, 12)
        b += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r:.1f}" fill="#dffcff" fill-opacity=".5" stroke="#04263a" stroke-width="2.5"/><circle cx="{x - r * .3:.0f}" cy="{y - r * .3:.0f}" r="{r * .3:.1f}" fill="#fff"/>'
    # the drop
    b += f'<circle cx="{cx}" cy="{cy}" r="{R}" fill="url(#inC)" stroke="#04263a" stroke-width="8"/>'
    inner = ''
    # faint plankton specks
    inner += ''.join(f'<circle cx="{random.uniform(cx - R, cx + R):.0f}" cy="{random.uniform(cy - R, cy + R):.0f}" r="{random.uniform(1.5, 4):.1f}" fill="#eafff8" opacity="{random.uniform(.2, .6):.2f}"/>' for _ in range(80))
    # 5 bacteria
    bac = [(cx - 150, cy - 110, 210, 74, 24, '#f2a24a'), (cx + 140, cy - 150, 180, 66, -32, '#f08a6a'), (cx - 40, cy + 70, 230, 80, 8, '#f6c14a'),
           (cx + 170, cy + 150, 170, 62, 58, '#f08a6a'), (cx - 210, cy + 190, 150, 58, -40, '#f2a24a')]
    for i, (x, y, L, W, r, col) in enumerate(bac):
        inner += rod(x, y, L, W, r, col, '#3a1a10', seed=10 + i)
    # 50 viruses (10 per bacterium): tiny glowing capsids and phages
    pts = []
    rnd = random.Random(7)
    while len(pts) < 50:
        x, y = rnd.uniform(cx - R + 40, cx + R - 40), rnd.uniform(cy - R + 40, cy + R - 40)
        if math.hypot(x - cx, y - cy) > R - 46: continue
        if any(math.hypot(x - bx, y - by) < max(L, W) * .5 + 6 for bx, by, L, W, _, _ in bac): continue
        if any(math.hypot(x - px, y - py) < 40 for px, py in pts): continue
        pts.append((x, y))
    cols = [('#7a1f6a', '#ff8ce0'), ('#5a2a9a', '#c9a8ff'), ('#8a1f3a', '#ff9cb0')]
    for i, (x, y) in enumerate(pts):
        dk, lt = cols[i % 3]
        if i % 6 == 0:
            inner += phage(x, y + 28, .42, rnd.uniform(-40, 40), head=lt)
        else:
            rr = rnd.uniform(13, 20)
            inner += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{rr * 1.9:.1f}" fill="{lt}" opacity=".35" filter="url(#b4)"/>'
            ic, _, _ = icosa(x, y, rr, rx=rnd.uniform(0, 3), ry=rnd.uniform(0, 3), rz=rnd.uniform(0, 3), dark=dk, lite=lt, ink='#2a0828', sw=1.8, eop=.8)
            inner += ic
            inner += ''.join(f'<path d="M{x + math.cos(a) * rr * .9:.1f},{y + math.sin(a) * rr * .9:.1f} l{math.cos(a) * rr * .45:.1f},{math.sin(a) * rr * .45:.1f}" stroke="#2a0828" stroke-width="2.4" stroke-linecap="round"/>' for a in [k * math.pi / 3 + .3 for k in range(6)])
    # viruses latched onto bacteria (attack in progress)
    for (x, y, L, W, r, col), side in zip(bac[:3], (1, -1, 1)):
        a = math.radians(r + 90 * side)
        inner += phage(x + math.cos(a) * (W * .5 + 30), y + math.sin(a) * (W * .5 + 30), .42, math.degrees(a) + 90 + (0 if side > 0 else 0), head='#ff8ce0')
    b += f'<g clip-path="url(#dropC)">{inner}'
    b += f'<circle cx="{cx}" cy="{cy}" r="{R}" fill="url(#rimC)"/>'
    b += f'<ellipse cx="{cx + 40}" cy="{cy + R * .78:.0f}" rx="{R * .6:.0f}" ry="{R * .16:.0f}" fill="#eafff8" opacity=".35" filter="url(#b14)"/></g>'
    # glass highlights
    b += f'<path d="M{cx - R * .78:.0f},{cy - R * .22:.0f} A{R * .82:.0f},{R * .82:.0f} 0 0 1 {cx - R * .2:.0f},{cy - R * .78:.0f}" fill="none" stroke="#ffffff" stroke-width="22" stroke-linecap="round" opacity=".75"/>'
    b += f'<ellipse cx="{cx - R * .42:.0f}" cy="{cy - R * .5:.0f}" rx="46" ry="24" transform="rotate(-38 {cx - R * .42:.0f} {cy - R * .5:.0f})" fill="#fff" opacity=".9"/>'
    b += f'<circle cx="{cx + R * .55:.0f}" cy="{cy + R * .55:.0f}" r="14" fill="#fff" opacity=".6"/>'
    b += f'<circle cx="{cx}" cy="{cy}" r="{R + 3}" fill="none" stroke="#e9fff8" stroke-width="3" opacity=".7"/>'
    b += spark(cx - R - 30, cy - 120, 22) + spark(cx + R + 40, cy - 200, 18) + spark(cx + 120, cy - R - 40, 16) + spark(980, 640, 14) + spark(1700, 660, 14)
    # small drops flying off
    for x, y, r in ((1720, 250, 34), (880, 820, 22), (1760, 520, 18), (930, 230, 16)):
        b += f'<circle cx="{x}" cy="{y}" r="{r}" fill="#9ff0e6" fill-opacity=".45" stroke="#04263a" stroke-width="3"/><circle cx="{x - r * .35:.0f}" cy="{y - r * .35:.0f}" r="{r * .28:.1f}" fill="#fff"/>'
    # snorkel frog in a swim ring, bobbing in the sea
    mask = ('<path d="M-30 -84 Q6 -92 42 -84 Q48 -66 40 -52 Q24 -46 6 -54 Q-12 -46 -28 -52 Q-36 -66 -30 -84Z" fill="#bff1ff" fill-opacity=".3" stroke="#14303a" stroke-width="4.2"/>'
            '<path d="M-30 -74 L-40 -72 M42 -74 L52 -72" stroke="#ff7a59" stroke-width="5"/>'
            '<path d="M-20 -80 q8 -5 16 -3" fill="none" stroke="#fff" stroke-width="3" opacity=".85"/>'
            '<path d="M48 -58 Q58 -60 58 -80 L58 -128" fill="none" stroke="#14303a" stroke-width="11"/><path d="M48 -58 Q58 -60 58 -80 L58 -128" fill="none" stroke="#ffd34a" stroke-width="6"/>'
            '<rect x="51" y="-140" width="14" height="16" rx="4" fill="#ff7a59" stroke="#14303a" stroke-width="3"/>')
    ring = ('<ellipse cx="4" cy="-8" rx="58" ry="20" fill="#ff7a8a" stroke-width="4"/>'
            '<path d="M-40 -18 q-10 10 -6 20 M-6 -27 q-4 12 2 19 M30 -26 q6 10 0 20" fill="none" stroke="#fff6f0" stroke-width="10"/>'
            '<path d="M-44 -14 q48 -16 96 0" fill="none" stroke="#ffd0d6" stroke-width="3" opacity=".8"/>')
    b += frog(285, 1000, 2.6, look=(5, -4), mouth='O', brows=True, armL='M-34 -24 q-24 -6 -30 -36', top=mask, front=ring)
    b += ('<path d="M-20,992 C80,974 160,1006 240,988 C320,968 420,1006 520,986 C620,936 700,972 800,990 C900,1010 960,1040 1000,1090 L-20,1090Z" fill="#0f5470" fill-opacity=".92" stroke="#04263a" stroke-width="5"/>'
          '<path d="M-10,994 C80,976 160,1008 240,990 C320,970 420,1008 520,988 C620,938 700,974 800,992" fill="none" stroke="#c9fff6" stroke-width="6" opacity=".8"/>')
    b += '<rect width="1920" height="1080" fill="url(#vigC)"/>'
    lines = [('OUTNUMBERED', 124, 'w'), ('10 TO 1', 250, 'y')]
    return page('#0b2a4a', svg(defs, b), lines, outline='#04131f')


for n, fn in (('A', thumb_A), ('B', thumb_B), ('C', thumb_C)):
    open(os.path.join(HERE, f'{n}.html'), 'w').write(fn())
print('ok')
