# Shared helpers for the five shorts thumbnails of deep-time-bedtime (guideline 16-9). Called from videos/deep-time-bedtime-shortN/thumb/make.py.
# Frog + curve helpers copied from make.py (long-form thumbnails) so both stay independent.
import os, sys, math, random
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../../tools'))
from thumb_lib import page, svg, lin, rad, spark, stars, blobs
INK = '#1d2b1c'; GREEN = '#6aa55a'

F = ''.join(f'<filter id="b{s}" x="-60%" y="-60%" width="220%" height="220%"><feGaussianBlur stdDeviation="{s}"/></filter>' for s in (3, 6, 12, 24, 50))


def P(v):
    return ' '.join(f'{a:.1f},{b:.1f}' for a, b in v)


def cr(pts, n=12):
    """Catmull-Rom smoothing of a point list -> dense list"""
    out = []
    p = [pts[0]] + pts + [pts[-1]]
    for i in range(1, len(p) - 2):
        p0, p1, p2, p3 = p[i - 1], p[i], p[i + 1], p[i + 2]
        for k in range(n):
            t = k / n; t2 = t * t; t3 = t2 * t
            out.append(tuple(.5 * (2 * p1[j] + (-p0[j] + p2[j]) * t + (2 * p0[j] - 5 * p1[j] + 4 * p2[j] - p3[j]) * t2 + (-p0[j] + 3 * p1[j] - 3 * p2[j] + p3[j]) * t3) for j in (0, 1)))
    out.append(pts[-1]); return out


def at(dense, u):
    """point + unit tangent at fraction u along a dense polyline"""
    L = [0]
    for a, b in zip(dense, dense[1:]): L.append(L[-1] + math.dist(a, b))
    s = u * L[-1]
    for i in range(1, len(L)):
        if L[i] >= s:
            a, b = dense[i - 1], dense[i]; f = (s - L[i - 1]) / ((L[i] - L[i - 1]) or 1)
            d = math.dist(a, b) or 1
            return (a[0] + (b[0] - a[0]) * f, a[1] + (b[1] - a[1]) * f), ((b[0] - a[0]) / d, (b[1] - a[1]) / d)
    return dense[-1], (1, 0)


# ---------------- mascot frog (tools/assets/frog.svg body; hat / props per thumbnail) ----------------
ARMS = {'down': ('q-14 6 -16 22', 'q14 6 16 22'), 'up': ('q-14 6 -16 22', 'q22 -4 30 -26'),
        'hold': ('q-10 10 -2 26', 'q10 10 2 26'), 'edge': ('q-10 14 -4 34', 'q10 14 4 34')}


def frog(x, y, s, mouth='o', arms='down', look=(2, 0), hat='', front='', back='', flip=False, legs=True):
    la, ra = ARMS[arms]; sx = -s if flip else s
    g = f'<g transform="translate({x} {y}) scale({sx} {s})" stroke="{INK}" stroke-linejoin="round" stroke-linecap="round">' + back
    if legs:
        g += '<ellipse cx="-22" cy="4" rx="16" ry="9" fill="#4d8a4a" stroke-width="3.2"/><ellipse cx="22" cy="4" rx="16" ry="9" fill="#4d8a4a" stroke-width="3.2"/>'
    g += f'<path d="M-34 0 q-6 -64 34 -70 q40 -2 42 62 q0 10 -6 12 q-36 6 -70 -4z" fill="{GREEN}" stroke-width="4"/>'
    g += '<ellipse cx="2" cy="-12" rx="22" ry="20" fill="#9cc98a" stroke="none" opacity=".7"/>'
    g += '<path d="M-26 -50 q6 -16 22 -18" fill="none" stroke="#b9e0a6" stroke-width="3" opacity=".7"/>'
    g += hat
    dx, dy = look
    for ex in (-10, 22):
        g += f'<circle cx="{ex}" cy="-66" r="13" fill="#e3e5d6" stroke-width="3.2"/><circle cx="{ex + dx}" cy="{-66 + dy}" r="5" fill="{INK}" stroke="none"/>'
        g += f'<circle cx="{ex + 2 + dx}" cy="{-68 + dy}" r="1.7" fill="#fff" stroke="none"/>'
    g += '<ellipse cx="-18" cy="-46" rx="5" ry="3" fill="#e98a8a" stroke="none" opacity=".55"/><ellipse cx="30" cy="-46" rx="5" ry="3" fill="#e98a8a" stroke="none" opacity=".55"/>'
    if mouth == 'o':
        g += '<ellipse cx="6" cy="-42" rx="6.5" ry="8" fill="#7a2f33" stroke-width="3"/><ellipse cx="6" cy="-38" rx="3.5" ry="2.6" fill="#e07b7b" stroke="none"/>'
    else:
        g += '<path d="M-8 -45 q14 14 28 0 q-14 4 -28 0z" fill="#7a2f33" stroke-width="3"/>'
    for st, path in (('M-34 -22', la), ('M38 -22', ra)):
        g += f'<path d="{st} {path}" fill="none" stroke-width="7.5"/><path d="{st} {path}" fill="none" stroke="{GREEN}" stroke-width="3.4"/>'
        sx0, sy0 = map(float, st[1:].split()); q = [float(v) for v in path[1:].split()]
        g += f'<circle cx="{sx0 + q[2]}" cy="{sy0 + q[3]}" r="5.5" fill="{GREEN}" stroke-width="3"/>'
    return g + front + '</g>'


GUARD_CAP = ('<path d="M-20 -82 C-24 -110 36 -114 34 -82 Z" fill="#23315e" stroke-width="3.2"/>'
             '<path d="M-21 -84 L35 -84 L35 -77 L-21 -77 Z" fill="#141c38" stroke-width="2.6"/>'
             '<path d="M30 -80 q22 0 30 6 q-14 6 -32 2 z" fill="#141c38" stroke-width="2.8"/>'
             '<path d="M7 -101 l3 6 l6 1 l-4.5 4 l1.2 6 l-5.7 -3 l-5.7 3 l1.2 -6 l-4.5 -4 l6 -1 z" fill="#f2d27a" stroke-width="1.6"/>'
             '<path d="M-14 -100 q8 -8 18 -8" fill="none" stroke="#5b6ea8" stroke-width="2.4"/>')


def nightcap(col='#6f6fc8', stripe='#c8c8f4'):
    g = (f'<path d="M-24 -80 C-30 -118 30 -132 70 -116 C84 -108 90 -92 92 -78 C70 -98 46 -104 36 -82 Z" fill="{col}" stroke-width="3.2"/>'
         f'<path d="M-10 -105 C10 -116 30 -118 46 -112 M20 -122 C34 -122 52 -118 64 -112 M60 -111 C72 -104 80 -96 86 -86" fill="none" stroke="{stripe}" stroke-width="5" opacity=".9"/>'
         f'<path d="M-26 -84 C-6 -90 18 -90 38 -82 L38 -76 C18 -82 -6 -82 -26 -77 Z" fill="#f3efe0" stroke-width="2.8"/>'
         f'<circle cx="94" cy="-76" r="9" fill="#f3efe0" stroke-width="2.8"/>')
    return g



# ---------------- frog outfits for the shorts ----------------
def helmet():
    return ('<circle cx="6" cy="-40" r="72" fill="#bfe6ff" fill-opacity=".14" stroke="#e6f6ff" stroke-width="3.2"/>'
            '<path d="M-44 -78 A60 60 0 0 1 10 -104" fill="none" stroke="#fff" stroke-width="5" opacity=".7"/>'
            '<path d="M60 -20 A60 60 0 0 1 40 6" fill="none" stroke="#ffd09a" stroke-width="4" opacity=".6"/>')


def scarf(col='#c8333a', st='#f3efe0'):
    return (f'<path d="M-34 -32 q38 14 76 0 l2 15 q-40 13 -80 0 z" fill="{col}" stroke-width="3"/>'
            f'<path d="M20 -20 l6 36 l15 -3 l-5 -35 z" fill="{col}" stroke-width="3"/>'
            f'<path d="M-24 -26 l0 10 M-6 -22 l0 10 M12 -22 l0 10 M30 -26 l0 10" stroke="{st}" stroke-width="3" opacity=".8"/>')


def earmuffs(col='#c8333a'):
    return (f'<path d="M-36 -58 C-34 -110 52 -110 52 -58" fill="none" stroke="{col}" stroke-width="6"/>'
            '<circle cx="-38" cy="-56" r="11" fill="#f6f3ea" stroke-width="3"/><circle cx="54" cy="-56" r="11" fill="#f6f3ea" stroke-width="3"/>')


def lava_cracks(cx, cy, r, n, seed):
    random.seed(seed); out = ''
    for _ in range(n):
        a = random.uniform(0, 6.283); d = random.uniform(0, r * .95)
        x, y = cx + d * math.cos(a), cy + d * math.sin(a); pts = [(x, y)]
        h = random.uniform(0, 6.283)
        for _ in range(random.randint(4, 9)):
            h += random.uniform(-.8, .8); s = random.uniform(18, 46)
            x += s * math.cos(h); y += s * math.sin(h); pts.append((x, y))
        w = random.choice([3, 4, 5, 7])
        d_ = 'M' + ' L'.join(f'{a_:.0f} {b_:.0f}' for a_, b_ in pts)
        out += f'<path d="{d_}" fill="none" stroke="#ff7a20" stroke-width="{w * 3.5}" opacity=".5" filter="url(#b6)"/>'
        out += f'<path d="{d_}" fill="none" stroke="#ffd36a" stroke-width="{w}" stroke-linejoin="round" stroke-linecap="round"/>'
    return out


# ====================================================================== short 1: the giant impact that made the Moon
def short1():
    random.seed(11)
    EX, EY, ER = 1040, 800, 400
    TX, TY, TR = 1425, 415, 165
    ux, uy = (TX - EX), (TY - EY); L = math.hypot(ux, uy); ux, uy = ux / L, uy / L
    CX, CY = EX + ux * ER, EY + uy * ER
    defs = F + rad('sp1', 1200, 560, 1300, [(0, '#3a1420', 1), (.5, '#1a0a18', 1), (1, '#07040c', 1)])
    defs += rad('earth1', CX - 60, CY + 40, 620, [(0, '#ffc25a', 1), (.25, '#f0702a', 1), (.6, '#8a2414', 1), (1, '#2a0a08', 1)])
    defs += rad('shade1', EX - 260, EY + 300, 600, [(0, '#000', .55), (.6, '#000', .2), (1, '#000', 0)])
    defs += rad('theia', TX + 60, TY - 70, 260, [(0, '#8a7c70', 1), (.6, '#4c4038', 1), (1, '#1e1814', 1)])
    defs += rad('flash1', CX, CY, 420, [(0, '#fff6d8', .95), (.18, '#ffd27a', .7), (.5, '#ff7a30', .25), (1, '#ff5a20', 0)])
    defs += rad('vig1', 960, 540, 1150, [(0, '#000', 0), (.7, '#000', 0), (1, '#000', .55)])
    defs += f'<clipPath id="ec1"><circle cx="{EX}" cy="{EY}" r="{ER}"/></clipPath><clipPath id="tc1"><circle cx="{TX}" cy="{TY}" r="{TR}"/></clipPath>'
    b = '<rect width="1920" height="1080" fill="url(#sp1)"/>' + stars(150, 1060, col='#ffe9d8', op=.6, sparks=0)
    b += '<ellipse cx="1300" cy="520" rx="700" ry="420" fill="#ff6a30" opacity=".10" filter="url(#b50)"/>'
    # faint debris ring behind the Earth
    b += f'<ellipse cx="{EX}" cy="{EY}" rx="620" ry="150" transform="rotate(-14 {EX} {EY})" fill="none" stroke="#ff9a50" stroke-width="26" opacity=".12" filter="url(#b12)"/>'
    for k in range(70):
        a = random.uniform(3.3, 6.1); rx, ry = 620 + random.uniform(-30, 30), 150 + random.uniform(-15, 15)
        x0, y0 = rx * math.cos(a), ry * math.sin(a); t = math.radians(-14)
        b += f'<circle cx="{EX + x0 * math.cos(t) - y0 * math.sin(t):.0f}" cy="{EY + x0 * math.sin(t) + y0 * math.cos(t):.0f}" r="{random.uniform(2, 6):.1f}" fill="#ffb070" opacity="{random.uniform(.3, .8):.2f}"/>'
    # Earth: glow, molten body, crust plates, lava cracks, shading, rim
    b += f'<circle cx="{EX}" cy="{EY}" r="{ER + 40}" fill="#ff6a20" opacity=".35" filter="url(#b24)"/>'
    b += f'<circle cx="{EX}" cy="{EY}" r="{ER}" fill="url(#earth1)"/>'
    b += '<g clip-path="url(#ec1)">'
    random.seed(5)
    for _ in range(26):
        a = random.uniform(0, 6.283); d = random.uniform(40, ER)
        x, y = EX + d * math.cos(a), EY + d * math.sin(a); s = random.uniform(40, 110)
        pts = ' '.join(f'{x + s * random.uniform(.6, 1.1) * math.cos(k * .9 + a):.0f},{y + s * random.uniform(.4, .8) * math.sin(k * .9 + a):.0f}' for k in range(7))
        b += f'<polygon points="{pts}" fill="#2a0d0a" opacity="{random.uniform(.35, .7):.2f}" stroke="#ffb050" stroke-width="3" stroke-opacity=".6"/>'
    b += lava_cracks(EX, EY, ER, 34, 9)
    b += f'<rect x="0" y="0" width="1920" height="1080" fill="url(#shade1)"/>'
    # little meteorite strikes on the surface
    for (mx, my) in ((820, 560), (700, 820), (960, 470)):
        b += f'<circle cx="{mx}" cy="{my}" r="24" fill="#ffe2a0" opacity=".8" filter="url(#b6)"/><circle cx="{mx}" cy="{my}" r="8" fill="#fff"/>'
    b += '</g>'
    b += f'<circle cx="{EX}" cy="{EY}" r="{ER - 4}" fill="none" stroke="#ffb060" stroke-width="10" opacity=".55" filter="url(#b6)"/>'
    for (sx, sy, ex, ey) in ((560, 430, 800, 545), (600, 640, 690, 760), (760, 330, 945, 455)):
        b += f'<path d="M{sx} {sy} L{ex} {ey}" stroke="#ffcf8a" stroke-width="6" stroke-linecap="round" opacity=".55" filter="url(#b3)"/>'
    # Theia (Mars-sized body) hitting
    b += f'<circle cx="{TX}" cy="{TY}" r="{TR + 16}" fill="#ff8a40" opacity=".35" filter="url(#b12)"/>'
    b += f'<circle cx="{TX}" cy="{TY}" r="{TR}" fill="url(#theia)" stroke="#120c0a" stroke-width="5"/>'
    b += '<g clip-path="url(#tc1)">'
    for (cx_, cy_, r_) in ((TX + 40, TY - 60, 30), (TX - 50, TY - 20, 18), (TX + 70, TY + 40, 22), (TX - 10, TY - 110, 14), (TX + 110, TY - 20, 12)):
        b += f'<circle cx="{cx_}" cy="{cy_}" r="{r_}" fill="#3a302a"/><path d="M{cx_ - r_ * .8:.0f} {cy_ + r_ * .3:.0f} A{r_} {r_} 0 0 0 {cx_ + r_ * .8:.0f} {cy_ + r_ * .3:.0f}" fill="none" stroke="#a89888" stroke-width="3" opacity=".7"/>'
    b += f'<circle cx="{CX}" cy="{CY}" r="190" fill="#ff7a30" opacity=".75" filter="url(#b24)"/>'
    b += '</g>'
    # impact flash and debris spray
    b += f'<circle cx="{CX}" cy="{CY}" r="420" fill="url(#flash1)"/>'
    b += f'<circle cx="{CX}" cy="{CY}" r="70" fill="#fffbe8" filter="url(#b12)"/><circle cx="{CX}" cy="{CY}" r="34" fill="#fff"/>'
    b += spark(CX, CY, 150, '#fff8e0', .9)
    random.seed(21)
    MX, MY = 1720, 700
    for k in range(150):
        t = random.random() ** .8
        qx = (1 - t) ** 2 * CX + 2 * (1 - t) * t * 1760 + t * t * MX
        qy = (1 - t) ** 2 * CY + 2 * (1 - t) * t * 430 + t * t * MY
        qx += random.gauss(0, 26 * (1 - t) + 6); qy += random.gauss(0, 26 * (1 - t) + 6)
        r_ = random.uniform(2, 9) * (1.2 - t * .5)
        col = random.choice(['#ffd27a', '#ff9a40', '#ffe9b8', '#c86a3a'])
        b += f'<circle cx="{qx:.0f}" cy="{qy:.0f}" r="{r_:.1f}" fill="{col}" opacity="{random.uniform(.5, 1):.2f}"/>'
    for k in range(40):  # spray upward-left
        a = random.uniform(-2.5, -1.2); d = random.uniform(80, 330)
        x, y = CX + d * math.cos(a), CY + d * math.sin(a)
        b += f'<path d="M{CX + (d - 40) * math.cos(a):.0f} {CY + (d - 40) * math.sin(a):.0f} L{x:.0f} {y:.0f}" stroke="#ffcf7a" stroke-width="{random.uniform(2, 5):.1f}" stroke-linecap="round" opacity="{random.uniform(.4, .9):.2f}"/>'
    # the young Moon gathering
    b += f'<circle cx="{MX}" cy="{MY}" r="95" fill="#ffb070" opacity=".35" filter="url(#b24)"/>'
    b += f'<circle cx="{MX}" cy="{MY}" r="58" fill="#d9a074" stroke="#2a1410" stroke-width="4"/>'
    b += f'<path d="M{MX - 40} {MY + 30} A58 58 0 0 0 {MX + 50} {MY + 26} A70 70 0 0 1 {MX - 40} {MY + 30} Z" fill="#5a2e20" opacity=".6"/>'
    b += f'<circle cx="{MX - 16}" cy="{MY - 14}" r="10" fill="#b87a54"/><circle cx="{MX + 20}" cy="{MY + 8}" r="7" fill="#b87a54"/>'
    b += f'<path d="M{MX - 44} {MY - 26} A52 52 0 0 1 {MX - 4} {MY - 54}" fill="none" stroke="#ffe6c0" stroke-width="5" opacity=".8"/>'
    # frog astronaut on a drifting rock, lower left
    b += '<path d="M150 950 C170 900 260 880 340 890 C430 896 500 920 510 950 C500 990 420 1010 330 1006 C240 1004 160 990 150 950 Z" fill="#3a2a26" stroke="#120a08" stroke-width="5"/>'
    b += '<path d="M190 930 C250 900 380 895 470 925" fill="none" stroke="#ff9a5a" stroke-width="5" opacity=".6"/>'
    b += '<circle cx="250" cy="960" r="12" fill="#22180f"/><circle cx="410" cy="975" r="9" fill="#22180f"/>'
    b += frog(330, 912, 2.75, mouth='o', arms='up', look=(5, -3), front=helmet())
    b += spark(1780, 180, 20) + spark(640, 960, 14) + spark(1600, 900, 0.1)
    b += '<rect width="1920" height="1080" fill="url(#vig1)"/>'
    lines = [('BORN FROM', 150, 'w'), ('A CRASH?', 196, 'y')]
    return page('#1a0a18', svg(defs, b), lines, outline='#14060c')


# ====================================================================== short 2: Snowball Earth in a snow globe
def flake(x, y, s, op=.9):
    g = f'<g transform="translate({x} {y})" stroke="#ffffff" stroke-width="{max(1.5, s / 6):.1f}" stroke-linecap="round" opacity="{op}">'
    for k in range(3):
        a = math.radians(k * 60)
        g += f'<path d="M{-s * math.cos(a):.1f} {-s * math.sin(a):.1f} L{s * math.cos(a):.1f} {s * math.sin(a):.1f}"/>'
    return g + '</g>'


def short2():
    random.seed(23)
    GX, GY, GR = 1270, 520, 370
    EX, EY, ER = GX, GY - 20, 215
    defs = F + lin('bg2', [(0, '#0f3346'), (.65, '#0a2232'), (1, '#05121c')])
    defs += rad('in2', GX - 80, GY - 120, 520, [(0, '#2d6f96', 1), (.6, '#163f5e', 1), (1, '#0b2440', 1)])
    defs += rad('snowE', EX - 70, EY - 80, 300, [(0, '#ffffff', 1), (.5, '#e6f2fb', 1), (.85, '#a9cbe4', 1), (1, '#6f97bb', 1)])
    defs += lin('wood2', [(0, '#7a4a2a'), (1, '#3a2014')])
    defs += lin('table2', [(0, '#3b2a22'), (1, '#170f0b')])
    defs += rad('vig2', 960, 540, 1150, [(0, '#000', 0), (.7, '#000', 0), (1, '#000', .55)])
    defs += f'<clipPath id="gc2"><circle cx="{GX}" cy="{GY}" r="{GR - 6}"/></clipPath><clipPath id="ec2"><circle cx="{EX}" cy="{EY}" r="{ER}"/></clipPath>'
    b = '<rect width="1920" height="1080" fill="url(#bg2)"/>'
    b += ''.join(flake(random.randint(40, 1880), random.randint(20, 960), random.choice([6, 9, 12]), random.uniform(.15, .45)) for _ in range(55))
    b += f'<circle cx="{GX}" cy="{GY}" r="{GR + 90}" fill="#7fd4ff" opacity=".22" filter="url(#b50)"/>'
    # table
    b += '<rect x="0" y="985" width="1920" height="95" fill="url(#table2)"/><rect x="0" y="980" width="1920" height="10" fill="#5a4032"/>'
    b += f'<ellipse cx="{GX}" cy="992" rx="360" ry="20" fill="#000" opacity=".5" filter="url(#b6)"/>'
    # globe interior
    b += f'<circle cx="{GX}" cy="{GY}" r="{GR - 6}" fill="url(#in2)"/>'
    b += f'<g clip-path="url(#gc2)">'
    b += ''.join(f'<circle cx="{random.randint(GX - GR, GX + GR)}" cy="{random.randint(GY - GR, GY + GR)}" r="1.6" fill="#dff2ff" opacity="{random.uniform(.3, .8):.2f}"/>' for _ in range(60))
    # snowball Earth
    b += f'<circle cx="{EX}" cy="{EY}" r="{ER + 30}" fill="#dff4ff" opacity=".35" filter="url(#b24)"/>'
    b += f'<circle cx="{EX}" cy="{EY}" r="{ER}" fill="url(#snowE)"/>'
    b += f'<g clip-path="url(#ec2)">'
    for d in ('M1150 380 C1200 360 1240 400 1230 440 C1222 480 1180 500 1150 470 C1120 440 1110 400 1150 380 Z',
              'M1300 470 C1360 450 1420 480 1420 540 C1420 600 1380 650 1330 630 C1290 610 1280 520 1300 470 Z',
              'M1110 560 C1150 540 1200 560 1196 600 C1190 640 1140 650 1110 620 Z'):
        b += f'<path d="{d}" fill="#bcd6ea" opacity=".55"/>'
    random.seed(4)
    for _ in range(16):
        x, y = EX + random.uniform(-180, 180), EY + random.uniform(-180, 180); pts = [(x, y)]; h = random.uniform(0, 6.3)
        for _ in range(4):
            h += random.uniform(-.7, .7); x += 30 * math.cos(h); y += 30 * math.sin(h); pts.append((x, y))
        b += '<path d="M' + ' L'.join(f'{a:.0f} {c:.0f}' for a, c in pts) + '" fill="none" stroke="#7fa6c8" stroke-width="2.5" opacity=".7"/>'
    b += f'<ellipse cx="{EX + 40}" cy="{EY + 120}" rx="260" ry="200" fill="#4a7aa6" opacity=".35" filter="url(#b24)"/>'
    b += '</g>'
    # glowing volcanic hot spot (life's refuge)
    vx, vy = EX - 70, EY + 120
    b += f'<circle cx="{vx}" cy="{vy}" r="46" fill="#ff8a30" opacity=".55" filter="url(#b12)"/>'
    b += f'<path d="M{vx - 22} {vy + 10} L{vx - 6} {vy - 14} L{vx + 6} {vy - 14} L{vx + 22} {vy + 10} Z" fill="#4a2a20" stroke="#1a0c08" stroke-width="3"/>'
    b += f'<circle cx="{vx}" cy="{vy - 14}" r="9" fill="#ffd27a"/><path d="M{vx} {vy - 22} C{vx - 14} {vy - 44} {vx + 14} {vy - 56} {vx} {vy - 80}" fill="none" stroke="#e6eef4" stroke-width="7" stroke-linecap="round" opacity=".6"/>'
    # ice sheen on the snowball
    b += f'<path d="M{EX - 160} {EY - 90} A190 190 0 0 1 {EX - 40} {EY - 190}" fill="none" stroke="#fff" stroke-width="12" stroke-linecap="round" opacity=".8"/>'
    # snow inside the globe: falling flakes + heap at the bottom
    random.seed(8)
    b += ''.join(f'<circle cx="{random.randint(GX - GR + 30, GX + GR - 30)}" cy="{random.randint(GY - GR + 30, GY + GR - 60)}" r="{random.choice([3, 4, 5, 6])}" fill="#ffffff" opacity="{random.uniform(.6, 1):.2f}"/>' for _ in range(70))
    b += ''.join(flake(random.randint(GX - 300, GX + 300), random.randint(GY - 300, GY + 220), random.choice([10, 14, 18]), .9) for _ in range(14))
    b += f'<path d="M{GX - 380} {GY + 300} C{GX - 260} {GY + 250} {GX - 120} {GY + 290} {GX} {GY + 270} C{GX + 140} {GY + 250} {GX + 260} {GY + 280} {GX + 380} {GY + 300} L{GX + 380} {GY + 400} L{GX - 380} {GY + 400} Z" fill="#eef7ff"/>'
    b += f'<path d="M{GX - 300} {GY + 282} C{GX - 200} {GY + 262} {GX - 100} {GY + 286} {GX} {GY + 274}" fill="none" stroke="#fff" stroke-width="6" opacity=".9"/>'
    b += '</g>'
    # glass
    b += f'<circle cx="{GX}" cy="{GY}" r="{GR}" fill="none" stroke="#d8f2ff" stroke-width="8" opacity=".55"/>'
    b += f'<circle cx="{GX}" cy="{GY}" r="{GR - 14}" fill="none" stroke="#ffffff" stroke-width="2" opacity=".25"/>'
    b += f'<path d="M{GX - 300} {GY - 120} A320 320 0 0 1 {GX - 90} {GY - 330}" fill="none" stroke="#fff" stroke-width="22" stroke-linecap="round" opacity=".45"/>'
    b += f'<path d="M{GX - 320} {GY - 30} A330 330 0 0 1 {GX - 312} {GY - 74}" fill="none" stroke="#fff" stroke-width="14" stroke-linecap="round" opacity=".4"/>'
    b += f'<ellipse cx="{GX + 210}" cy="{GY + 170}" rx="60" ry="22" transform="rotate(-50 {GX + 210} {GY + 170})" fill="#fff" opacity=".18"/>'
    # wooden base with gold trim
    b += f'<path d="M{GX - 300} 860 L{GX + 300} 860 L{GX + 330} 985 L{GX - 330} 985 Z" fill="url(#wood2)" stroke="#1a0c06" stroke-width="5"/>'
    b += f'<path d="M{GX - 286} 860 L{GX + 286} 860 L{GX + 290} 880 L{GX - 290} 880 Z" fill="#e2b85a" stroke="#4a3010" stroke-width="3"/>'
    b += f'<path d="M{GX - 322} 955 L{GX + 322} 955 L{GX + 328} 972 L{GX - 328} 972 Z" fill="#c9993e" stroke="#4a3010" stroke-width="3"/>'
    b += f'<path d="M{GX - 290} 892 L{GX - 270} 950" stroke="#a86a40" stroke-width="5" opacity=".6"/><path d="M{GX + 120} 892 L{GX + 140} 950" stroke="#2a160c" stroke-width="4" opacity=".4"/>'
    # shivering frog with earmuffs + scarf
    b += '<ellipse cx="560" cy="990" rx="120" ry="14" fill="#000" opacity=".45" filter="url(#b6)"/>'
    b += frog(560, 984, 2.95, mouth='o', arms='hold', look=(5, -5), hat='', front=scarf('#d4413f') + earmuffs('#d4413f'))
    for (sx, sy) in ((380, 820), (740, 800), (390, 900), (735, 890)):
        d = 1 if sx > 560 else -1
        b += f'<path d="M{sx} {sy} l{8 * d} 10 l{-8 * d} 10 l{8 * d} 10" fill="none" stroke="#dff4ff" stroke-width="5" stroke-linecap="round" opacity=".8"/>'
    b += spark(1720, 230, 22) + spark(1010, 900, 14) + spark(860, 520, 16, op=.7)
    b += '<rect width="1920" height="1080" fill="url(#vig2)"/>'
    lines = [('SNOWBALL', 172, 'y'), ('EARTH?', 196, 'w')]
    return page('#0a2232', svg(defs, b), lines, outline='#04111a')


# ====================================================================== short 3: Tiktaalik lifts its head out of the water
def short3():
    random.seed(31)
    WL = 735
    defs = F + lin('sky3', [(0, '#123236'), (.55, '#3e5a4a'), (.85, '#d99a5a'), (1, '#f2c27a')])
    defs += lin('wat3', [(0, '#3d7a72'), (.3, '#1f4f50'), (1, '#0a2226')])
    defs += lin('mud3', [(0, '#7a5a38'), (.5, '#4e3a26'), (1, '#24180f')])
    defs += '<linearGradient id="fish3" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#7d8a4a"/><stop offset=".55" stop-color="#5a6a3a"/><stop offset=".8" stop-color="#c9b77a"/><stop offset="1" stop-color="#e0d29a"/></linearGradient>'
    defs += rad('sun3', 1520, 600, 520, [(0, '#fff0c0', .9), (.25, '#ffc870', .45), (1, '#ff9040', 0)])
    defs += rad('vig3', 960, 540, 1150, [(0, '#000', 0), (.7, '#000', 0), (1, '#000', .55)])
    defs += f'<clipPath id="wc3"><rect x="0" y="{WL}" width="1920" height="400"/></clipPath>'
    b = '<rect width="1920" height="1080" fill="url(#sky3)"/><rect width="1920" height="1080" fill="url(#sun3)"/>'
    b += '<circle cx="1520" cy="610" r="70" fill="#fff4d0" opacity=".95" filter="url(#b3)"/>'
    for (y0, op, col) in ((380, .25, '#f6d6a0'), (450, .3, '#f6d6a0')):
        b += blobs(4, 1000, y0 - 20, 1900, y0 + 20, col, op * .25, op * .5, 90, 220)
    # far barren hills + low green scouts on the shore
    b += f'<path d="M0 {WL - 60} C200 {WL - 120} 420 {WL - 90} 640 {WL - 70} C900 {WL - 140} 1180 {WL - 110} 1400 {WL - 60} C1600 {WL - 90} 1800 {WL - 120} 1920 {WL - 80} L1920 {WL} L0 {WL} Z" fill="#5a5a52" opacity=".75"/>'
    b += f'<path d="M0 {WL - 20} C300 {WL - 50} 700 {WL - 30} 1000 {WL - 26} C1300 {WL - 40} 1600 {WL - 30} 1920 {WL - 20} L1920 {WL} L0 {WL} Z" fill="#3c4a3a"/>'
    for x in range(30, 1900, 37):
        h = random.randint(10, 30)
        b += f'<path d="M{x} {WL - 22} l{random.randint(-4, 4)} -{h}" stroke="#2e5a34" stroke-width="3" stroke-linecap="round"/>'
    # water
    b += f'<rect x="0" y="{WL}" width="1920" height="{1080 - WL}" fill="url(#wat3)"/>'
    b += f'<path d="M1300 {WL + 4} L1740 {WL + 4} L1640 {WL + 120} L1400 {WL + 120} Z" fill="#ffd08a" opacity=".28" filter="url(#b12)"/>'
    for k in range(26):
        y = WL + 10 + k * 13; x = random.randint(900, 1800)
        b += f'<path d="M{x} {y} l{random.randint(40, 140)} 0" stroke="#ffe0a8" stroke-width="3" opacity="{max(.05, .5 - k * .02):.2f}" stroke-linecap="round"/>'
    # underwater weeds
    for x in range(1250, 1900, 70):
        b += f'<path d="M{x} 1080 C{x - 30} 1000 {x + 30} 960 {x - 10} {900 + random.randint(0, 60)}" fill="none" stroke="#1e4a2e" stroke-width="10" stroke-linecap="round" opacity=".8"/>'
    # mud bank (left)
    bank = f'M0 {WL - 10} C300 {WL - 20} 620 {WL - 5} 880 {WL + 20} C1020 {WL + 34} 1110 {WL + 70} 1150 {WL + 130} C1190 {WL + 200} 1170 1000 1120 1080 L0 1080 Z'
    b += f'<path d="{bank}" fill="url(#mud3)" stroke="#1a120a" stroke-width="5"/>'
    b += f'<path d="M20 {WL + 6} C320 {WL - 4} 640 {WL + 10} 880 {WL + 34} C1000 {WL + 46} 1080 {WL + 80} 1120 {WL + 130}" fill="none" stroke="#c9a070" stroke-width="5" opacity=".7"/>'
    b += blobs(30, 40, WL + 60, 1050, 1060, '#2a1c10', .25, .55, 10, 34)
    for (mx, my, s) in ((240, WL + 40, 1), (760, WL + 60, 1.3), (1000, WL + 110, .9)):
        b += f'<path d="M{mx} {my} c10 -40 30 -60 40 -70 M{mx + 20} {my} c0 -30 -14 -46 -20 -56 M{mx + 8} {my} c4 -20 20 -30 32 -30" fill="none" stroke="#4f8a3a" stroke-width="{6 * s:.0f}" stroke-linecap="round"/>'
    # ---- Tiktaalik (facing left), placed with its fins on the bank, tail in the water
    T = '<g transform="translate(890 640) rotate(10) scale(1.0 1.2)" stroke="#1d1a0e" stroke-linejoin="round" stroke-linecap="round">'
    T += '<path d="M330 40 C360 70 380 110 360 140 C330 150 300 120 290 70 Z" fill="#4c5a30" stroke-width="4"/>'  # far fin
    body = ('M0 0 C10 -26 50 -44 110 -50 C150 -56 200 -62 260 -62 C380 -64 520 -52 660 -30 C760 -14 840 4 900 20 '
            'L960 -20 C968 10 966 50 958 80 L900 46 C820 52 700 66 580 74 C440 82 300 84 200 70 C110 58 40 40 6 20 C-2 14 -4 6 0 0 Z')
    T += f'<path d="M640 -34 C700 -60 780 -44 860 4" fill="#8a7a48" stroke-width="3.5"/>'  # dorsal fin
    T += f'<path d="{body}" fill="url(#fish3)" stroke-width="5"/>'
    T += '<path d="M40 -32 C200 -60 520 -60 860 2" fill="none" stroke="#c9d08a" stroke-width="6" opacity=".55"/>'
    for (sx_, sy_, r_) in ((200, -30, 16), (300, -36, 20), (420, -30, 18), (540, -26, 22), (660, -14, 16), (760, 0, 14), (250, 10, 12), (480, 14, 14)):
        T += f'<ellipse cx="{sx_}" cy="{sy_}" rx="{r_}" ry="{r_ * .6:.0f}" fill="#3a4420" stroke="none" opacity=".55"/>'
    for i in range(10):
        x0 = 190 + i * 60
        T += f'<path d="M{x0} {-50 + i * 2} q18 40 0 {100 - i * 6}" fill="none" stroke="#3e4a22" stroke-width="2.5" opacity=".45"/>'
    for k in range(6):
        T += f'<path d="M{904 + k * 9} {18 - k * 6} L{960 - k * 1} {-14 + k * 16}" stroke="#4a4a26" stroke-width="2" opacity=".6"/>'
    T += '<path d="M8 12 C40 30 90 36 140 30" fill="none" stroke-width="4"/>'  # mouth
    T += '<path d="M140 30 q8 -4 8 -12" fill="none" stroke-width="3"/>'
    T += '<circle cx="22" cy="-8" r="3" fill="#1d1a0e" stroke="none"/>'
    for ex in (70, 108):
        T += f'<ellipse cx="{ex}" cy="-44" rx="17" ry="14" fill="#6a7a3e" stroke-width="3.5"/><circle cx="{ex - 2}" cy="-46" r="11" fill="#f4eed0" stroke-width="2.5"/>'
        T += f'<circle cx="{ex - 6}" cy="-46" r="5.5" fill="#1d1a0e" stroke="none"/><circle cx="{ex - 4}" cy="-49" r="2" fill="#fff" stroke="none"/>'
    T += '<path d="M180 60 C190 30 210 20 226 36" fill="none" stroke-width="3" opacity=".6"/>'
    T += '<path d="M150 44 C150 80 146 100 130 120" fill="none" stroke="#1d1a0e" stroke-width="30"/><path d="M150 44 C150 80 146 100 130 120" fill="none" stroke="#6a7a3e" stroke-width="22"/>'
    T += '<path d="M134 112 C110 130 70 140 40 136 C44 124 70 116 100 110 Z" fill="#8a9a52" stroke-width="4"/>'
    for k in range(5):
        T += f'<path d="M{124 - k * 4} {118 + k} L{56 + k * 4} {132 - k * 3}" stroke="#4c5a2c" stroke-width="2"/>'
    T += '</g>'
    b += T
    # water covering the rear of the body + ripples
    b += f'<g clip-path="url(#wc3)"><path d="M1150 {WL} L1920 {WL} L1920 1080 L1170 1080 C1190 1000 1200 {WL + 200} 1150 {WL + 130} Z" fill="#1f4f50" opacity=".62"/></g>'
    for (rx_, ry_, w_) in ((1280, WL + 6, 160), (1520, WL + 10, 220), (1760, WL + 4, 130)):
        b += f'<ellipse cx="{rx_}" cy="{ry_}" rx="{w_}" ry="12" fill="none" stroke="#e8f4e0" stroke-width="4" opacity=".55"/>'
    for (bx, by, r_) in ((1340, 900, 9), (1360, 860, 6), (1580, 920, 8), (1600, 880, 5)):
        b += f'<circle cx="{bx}" cy="{by}" r="{r_}" fill="none" stroke="#cfeee6" stroke-width="3" opacity=".7"/>'
    b += '<path d="M905 740 C930 760 960 770 990 762" fill="none" stroke="#e8f4e0" stroke-width="4" opacity=".6"/>'
    # frog waving at its distant relative
    b += '<ellipse cx="560" cy="860" rx="110" ry="14" fill="#000" opacity=".4" filter="url(#b6)"/>'
    b += frog(560, 856, 2.9, mouth='o', arms='up', look=(6, 0), flip=False)
    b += spark(1720, 300, 18) + spark(1100, 480, 14) + spark(760, 620, 12, op=.7)
    b += '<rect width="1920" height="1080" fill="url(#vig3)"/>'
    lines = [('LEAVING', 200, 'y'), ('THE WATER', 150, 'w')]
    return page('#123236', svg(defs, b), lines, outline='#0a1a1a')


# ====================================================================== short 4: this coal was a tree
def short4():
    random.seed(41)
    CX0 = 1260
    defs = F + lin('bg4', [(0, '#0e1410'), (.6, '#120e0a'), (1, '#1c0e08')])
    defs += rad('ember4', CX0, 1000, 700, [(0, '#ff8a30', .55), (.4, '#c0461a', .2), (1, '#000', 0)])
    defs += rad('ghost4', CX0, 420, 600, [(0, '#8af0b0', .35), (.6, '#4ac080', .1), (1, '#2a8050', 0)])
    defs += lin('coal4', [(0, '#3a3f4c'), (.5, '#16171c'), (1, '#07070a')])
    defs += rad('vig4', 960, 540, 1150, [(0, '#000', 0), (.7, '#000', 0), (1, '#000', .6)])
    b = '<rect width="1920" height="1080" fill="url(#bg4)"/><rect width="1920" height="1080" fill="url(#ghost4)"/>'
    # faint swamp ferns in the far ghost-forest
    # ghost Lepidodendron rising from the coal like smoke
    G = '#9cf0c0'
    b += f'<path d="M{CX0 - 30} 700 C{CX0 - 90} 600 {CX0 + 40} 540 {CX0 - 10} 460 C{CX0 - 40} 400 {CX0 + 20} 360 {CX0} 300" fill="none" stroke="#c8ffe0" stroke-width="40" opacity=".12" filter="url(#b12)"/>'
    trunk = f'M{CX0 - 46} 690 C{CX0 - 40} 560 {CX0 - 34} 400 {CX0 - 28} 250 L{CX0 + 28} 250 C{CX0 + 34} 400 {CX0 + 40} 560 {CX0 + 46} 690 Z'
    b += f'<path d="{trunk}" fill="#3a9a6a" opacity=".42" stroke="{G}" stroke-width="5" stroke-opacity=".75"/>'
    for yy in range(270, 690, 30):
        for xx in range(-30, 40, 20):
            b += f'<path d="M{CX0 + xx} {yy} l9 13 l-9 13 l-9 -13 z" fill="none" stroke="{G}" stroke-width="2.4" opacity=".55"/>'
    def branch(x, y, ang, L, w, depth):
        nonlocal b
        x2, y2 = x + L * math.sin(math.radians(ang)), y - L * math.cos(math.radians(ang))
        b += f'<path d="M{x:.0f} {y:.0f} L{x2:.0f} {y2:.0f}" stroke="#3a9a6a" stroke-width="{w}" stroke-linecap="round" opacity=".5"/><path d="M{x:.0f} {y:.0f} L{x2:.0f} {y2:.0f}" stroke="{G}" stroke-width="3" opacity=".7"/>'
        if depth == 0:
            for k in range(9):
                a = math.radians(ang - 80 + k * 20)
                b += f'<path d="M{x2:.0f} {y2:.0f} l{34 * math.sin(a):.0f} {-34 * math.cos(a):.0f}" stroke="{G}" stroke-width="4" stroke-linecap="round" opacity=".7"/>'
            return
        branch(x2, y2, ang - 26, L * .78, w * .72, depth - 1); branch(x2, y2, ang + 26, L * .78, w * .72, depth - 1)
    branch(CX0, 252, -30, 120, 44, 3); branch(CX0, 252, 30, 120, 44, 3)
    # giant dragonfly relative
    DX, DY = 1640, 300
    b += f'<g transform="translate({DX} {DY}) rotate(-12)" stroke="#dffff0" stroke-linecap="round">'
    for (sx, sy, rot) in ((1, 1, -8), (1, 1, 14), (-1, 1, 8), (-1, 1, -14)):
        b += f'<g transform="scale({sx} {sy}) rotate({rot})"><path d="M10 -4 C80 -40 200 -40 250 -10 C200 10 80 14 10 4 Z" fill="#bff8dc" fill-opacity=".28" stroke-width="3"/>'
        b += '<path d="M14 0 L240 -12 M60 -20 L80 6 M120 -26 L130 8 M180 -24 L184 4" fill="none" stroke-width="1.5" opacity=".6"/></g>'
    b += '<path d="M0 -14 L0 150" stroke="#2a6a4a" stroke-width="16"/><path d="M0 -14 L0 150" stroke="#9cf0c0" stroke-width="9"/>'
    b += '<circle cx="-9" cy="-22" r="11" fill="#9cf0c0" stroke-width="2.5"/><circle cx="9" cy="-22" r="11" fill="#9cf0c0" stroke-width="2.5"/></g>'
    b += f'<circle cx="{DX}" cy="{DY}" r="200" fill="#9cf0c0" opacity=".08" filter="url(#b24)"/>'
    # floor + ember glow
    b += '<rect x="0" y="950" width="1920" height="130" fill="#0b0806"/><rect width="1920" height="1080" fill="url(#ember4)"/>'
    # the lump of coal
    poly = [(CX0 - 330, 940), (CX0 - 360, 830), (CX0 - 250, 720), (CX0 - 80, 676), (CX0 + 120, 690), (CX0 + 290, 740), (CX0 + 350, 860), (CX0 + 310, 950)]
    b += f'<ellipse cx="{CX0}" cy="955" rx="400" ry="26" fill="#000" opacity=".6" filter="url(#b6)"/>'
    b += '<polygon points="' + ' '.join(f'{x},{y}' for x, y in poly) + '" fill="url(#coal4)" stroke="#000" stroke-width="6"/>'
    facets = [[(CX0 - 250, 720), (CX0 - 80, 676), (CX0 - 40, 780), (CX0 - 220, 820)],
              [(CX0 - 80, 676), (CX0 + 120, 690), (CX0 + 90, 790), (CX0 - 40, 780)],
              [(CX0 + 120, 690), (CX0 + 290, 740), (CX0 + 230, 830), (CX0 + 90, 790)],
              [(CX0 - 360, 830), (CX0 - 250, 720), (CX0 - 220, 820), (CX0 - 300, 930)]]
    for f_, col in zip(facets, ('#4a5060', '#5a6274', '#2e323e', '#252830')):
        b += '<polygon points="' + ' '.join(f'{x},{y}' for x, y in f_) + f'" fill="{col}" stroke="#000" stroke-width="3" opacity=".9"/>'
    b += f'<path d="M{CX0 - 240} 724 L{CX0 - 82} 682 L{CX0 + 116} 694" fill="none" stroke="#c8d4f0" stroke-width="4" opacity=".7"/>'
    # fossil bark + fern imprint glowing on the front face
    fx, fy = CX0 + 20, 870
    b += f'<g opacity=".95">'
    for i in range(4):
        for j in range(3):
            x = fx - 200 + j * 34 + (i % 2) * 17; y = fy - 40 + i * 26
            b += f'<path d="M{x} {y} l12 13 l-12 13 l-12 -13 z" fill="none" stroke="#f2d27a" stroke-width="3" opacity=".85"/>'
    b += f'<path d="M{fx + 20} {fy + 60} C{fx + 60} {fy + 10} {fx + 120} {fy - 30} {fx + 200} {fy - 50}" fill="none" stroke="#f2d27a" stroke-width="5"/>'
    for k in range(9):
        t = k / 9; px = fx + 20 + t * 180; py = fy + 60 - t * 110 + t * t * 10
        b += f'<path d="M{px:.0f} {py:.0f} l{-16 + t * 6:.0f} {-26 + t * 8:.0f} M{px:.0f} {py:.0f} l{24 - t * 6:.0f} {6 - t * 2:.0f}" stroke="#f2d27a" stroke-width="4" stroke-linecap="round"/>'
    b += '</g>'
    b += f'<ellipse cx="{fx}" cy="{fy}" rx="240" ry="80" fill="#f2d27a" opacity=".10" filter="url(#b24)"/>'
    # glowing ember cracks at the base
    for d in (f'M{CX0 - 300} 935 L{CX0 - 220} 900 L{CX0 - 160} 928', f'M{CX0 + 120} 945 L{CX0 + 180} 905 L{CX0 + 260} 925 L{CX0 + 300} 900', f'M{CX0 - 60} 948 L{CX0 - 20} 918 L{CX0 + 30} 940'):
        b += f'<path d="{d}" fill="none" stroke="#ff7a20" stroke-width="16" opacity=".55" filter="url(#b6)"/><path d="{d}" fill="none" stroke="#ffd36a" stroke-width="4"/>'
    for _ in range(18):
        b += f'<circle cx="{random.randint(CX0 - 300, CX0 + 300)}" cy="{random.randint(560, 900)}" r="{random.choice([2, 3, 4])}" fill="#ffb050" opacity="{random.uniform(.4, .9):.2f}"/>'
    # frog in a winter scarf, warmed by the coal, looking up at the ghost tree
    b += '<ellipse cx="650" cy="962" rx="120" ry="14" fill="#000" opacity=".5" filter="url(#b6)"/>'
    b += frog(650, 956, 3.0, mouth='o', arms='up', look=(5, -6), front=scarf('#d48a2a', '#fff2c8'))
    b += spark(1520, 560, 16, '#dffff0') + spark(1090, 200, 14, '#dffff0', .7) + spark(860, 650, 12)
    b += '<rect width="1920" height="1080" fill="url(#vig4)"/>'
    lines = [('THIS COAL', 150, 'w'), ('WAS A', 130, 'w'), ('TREE', 236, 'y')]
    return page('#0e1410', svg(defs, b), lines, outline='#050806')


# ====================================================================== short 5: small mammal sheltering in a burrow
def short5():
    random.seed(51)
    GL = 575
    defs = F + lin('sky5', [(0, '#1e1a1c'), (.6, '#3a2e2a'), (1, '#5a3a2a')])
    defs += lin('soil5', [(0, '#5a3c26'), (.4, '#3e2a1a'), (1, '#1e140c')])
    defs += rad('den5', 1150, 830, 360, [(0, '#e0a060', 1), (.5, '#9a6434', 1), (1, '#4a2e18', 1)])
    defs += rad('warm5', 1150, 830, 460, [(0, '#ffc070', .45), (1, '#ff9040', 0)])
    defs += lin('fur5', [(0, '#a8744a'), (1, '#6a4428')])
    defs += rad('vig5', 960, 540, 1150, [(0, '#000', 0), (.7, '#000', 0), (1, '#000', .6)])
    b = '<rect width="1920" height="1080" fill="url(#sky5)"/>'
    b += '<circle cx="1480" cy="250" r="140" fill="#c0503a" opacity=".35" filter="url(#b24)"/><circle cx="1480" cy="250" r="62" fill="#d8704a" opacity=".55"/>'
    b += blobs(14, 900, 120, 1900, 420, '#2a2220', .25, .5, 120, 260)
    b += f'<path d="M0 {GL - 30} C400 {GL - 60} 800 {GL - 40} 1100 {GL - 50} C1400 {GL - 60} 1700 {GL - 40} 1920 {GL - 50} L1920 {GL} L0 {GL} Z" fill="#2a2220"/>'
    b += f'<ellipse cx="1700" cy="{GL - 40}" rx="260" ry="30" fill="#ff7a30" opacity=".35" filter="url(#b12)"/>'
    # burnt stumps / trunks
    for (x, h, w, lean) in ((240, 120, 30, -4), (980, 200, 38, 6), (1560, 160, 34, -6), (1820, 110, 26, 3)):
        b += f'<path d="M{x - w} {GL} L{x - w * .6 + lean:.0f} {GL - h} L{x - w * .1 + lean:.0f} {GL - h - 14} L{x + w * .4 + lean:.0f} {GL - h + 8} L{x + w} {GL} Z" fill="#141010" stroke="#000" stroke-width="3"/>'
        b += f'<path d="M{x - w * .5 + lean:.0f} {GL - h + 4} l-40 -30 M{x + w * .3 + lean:.0f} {GL - h * .6:.0f} l36 -24" stroke="#141010" stroke-width="8" stroke-linecap="round"/>'
        b += f'<circle cx="{x + 4}" cy="{GL - h * .4:.0f}" r="4" fill="#ff8a30" opacity=".8"/>'
    # falling ash
    b += ''.join(f'<circle cx="{random.randint(0, 1920)}" cy="{random.randint(0, GL)}" r="{random.choice([2, 3, 4])}" fill="#8a7e74" opacity="{random.uniform(.35, .75):.2f}"/>' for _ in range(110))
    # soil
    b += f'<rect x="0" y="{GL}" width="1920" height="{1080 - GL}" fill="url(#soil5)"/>'
    b += f'<path d="M0 {GL} L1920 {GL}" stroke="#141010" stroke-width="10"/>'
    b += blobs(60, 0, GL + 30, 1920, 1070, '#2a1a10', .3, .6, 8, 28)
    for (x, y) in ((300, GL), (980, GL), (1560, GL)):
        p = f'M{x} {y} C{x - 30} {y + 80} {x + 40} {y + 140} {x - 10} {y + 230} M{x} {y + 70} C{x + 40} {y + 100} {x + 80} {y + 110} {x + 120} {y + 170}'
        b += f'<path d="{p}" fill="none" stroke="#2a1a0e" stroke-width="7" stroke-linecap="round"/>'
    b += '<rect width="1920" height="1080" fill="url(#warm5)"/>'
    # tunnel from the surface down to the warm den (lit from below)
    b += '<linearGradient id="tun5" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2a1a10"/><stop offset="1" stop-color="#b07840"/></linearGradient>'
    tun = f'M1150 {GL} C1150 {GL + 60} 1230 {GL + 80} 1220 {GL + 140} L1340 {GL + 140} C1340 {GL + 60} 1250 {GL + 50} 1250 {GL} Z'
    b += f'<path d="{tun}" fill="url(#tun5)" stroke="#120a06" stroke-width="5"/>'
    b += f'<ellipse cx="1200" cy="{GL}" rx="56" ry="10" fill="#0c0806"/>'
    b += '<path d="M830 830 C830 700 1000 660 1160 664 C1340 668 1470 720 1470 830 C1470 940 1320 985 1150 985 C980 985 830 950 830 830 Z" fill="url(#den5)" stroke="#1a0e06" stroke-width="7"/>'
    b += '<path d="M860 800 C880 720 1000 690 1150 690" fill="none" stroke="#f0c080" stroke-width="5" opacity=".5"/>'
    # nest of dry grass + seeds
    random.seed(9)
    for _ in range(46):
        x = random.randint(880, 1420); y = random.randint(920, 968); a = random.uniform(-.5, .5)
        b += f'<path d="M{x} {y} l{60 * math.cos(a):.0f} {-14 * math.sin(a) - 6:.0f}" stroke="{random.choice(["#d8b060", "#b88a40", "#e8c878"])}" stroke-width="4" stroke-linecap="round"/>'
    for (sx, sy) in ((1360, 940), (1385, 950), (1340, 955), (900, 948)):
        b += f'<ellipse cx="{sx}" cy="{sy}" rx="11" ry="7" fill="#7a4a24" stroke="#2a1608" stroke-width="2.5"/><ellipse cx="{sx - 3}" cy="{sy - 2}" rx="4" ry="2" fill="#c08a50"/>'
    # small furry mammal, nibbling a seed
    M = '<g transform="translate(1235 930) scale(1.3)" stroke="#2a1608" stroke-linejoin="round" stroke-linecap="round">'
    M += '<path d="M-110 -10 C-170 -10 -200 -50 -180 -80 C-170 -96 -150 -90 -160 -70" fill="none" stroke-width="9"/><path d="M-110 -10 C-170 -10 -200 -50 -180 -80 C-170 -96 -150 -90 -160 -70" fill="none" stroke="#c89a78" stroke-width="4"/>'
    M += '<path d="M-130 0 C-140 -70 -70 -110 0 -104 C60 -100 100 -70 104 -30 C108 0 80 10 40 10 L-110 10 C-126 10 -132 6 -130 0 Z" fill="url(#fur5)" stroke-width="5"/>'
    for k in range(9):
        M += f'<path d="M{-110 + k * 22} {-80 + abs(k - 4) * 6} q6 8 12 0" fill="none" stroke="#4a2c16" stroke-width="2.5" opacity=".6"/>'
    M += '<path d="M-40 -20 C-20 4 40 8 70 -6" fill="#e0c09a" stroke="none" opacity=".8"/>'
    M += '<ellipse cx="36" cy="-108" rx="20" ry="24" fill="#a8744a" stroke-width="4"/><ellipse cx="36" cy="-106" rx="11" ry="14" fill="#e8a0a0" stroke="none"/>'
    M += '<path d="M40 -90 C70 -96 110 -80 136 -56 C150 -44 146 -32 130 -32 C100 -30 70 -36 50 -50 Z" fill="#b07c52" stroke-width="4"/>'
    M += '<circle cx="142" cy="-42" r="7" fill="#e07a8a" stroke-width="2.5"/>'
    M += '<circle cx="82" cy="-70" r="13" fill="#1a0e06" stroke="none"/><circle cx="86" cy="-75" r="4.5" fill="#fff" stroke="none"/><circle cx="78" cy="-66" r="2" fill="#fff" stroke="none"/>'
    M += '<path d="M128 -40 l40 -10 M128 -38 l42 4 M126 -36 l34 16" stroke="#3a2010" stroke-width="2" opacity=".8"/>'
    M += '<path d="M110 -20 q10 -10 22 -6" fill="none" stroke-width="7"/><path d="M110 -20 q10 -10 22 -6" fill="none" stroke="#d8a888" stroke-width="3"/>'
    M += '<ellipse cx="138" cy="-24" rx="12" ry="8" fill="#7a4a24" stroke-width="2.5"/>'
    M += '<path d="M-90 10 l-6 12 M-60 10 l-4 12 M40 10 l4 12" stroke-width="6"/>'
    M += '</g>'
    b += M
    # frog curled up beside it, curious
    b += frog(940, 962, 2.4, mouth='o', arms='hold', look=(6, 1))
    b += spark(1440, 700, 14, '#ffe6b0') + spark(1050, 400, 16) + spark(1720, 120, 12, op=.6)
    b += '<rect width="1920" height="1080" fill="url(#vig5)"/>'
    lines = [('THE SMALL', 156, 'w'), ('SURVIVED', 206, 'y')]
    return page('#1e1a1c', svg(defs, b), lines, outline='#0c0808')


SHORTS = {1: short1, 2: short2, 3: short3, 4: short4, 5: short5}


def build(n, here):
    open(os.path.join(here, 'A.html'), 'w').write(SHORTS[n]())
