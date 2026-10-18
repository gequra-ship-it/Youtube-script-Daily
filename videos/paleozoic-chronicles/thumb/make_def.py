# Thumbnails D, E, F for paleozoic-chronicles (A/B/C are made separately and stay untouched).
# D = film homage (E.T.: silhouette crossing a giant full moon) -> Meganeura, wingspan ~70 cm, about a hawk's (script S28)
# E = famous-image homage (Michelangelo, The Creation of Adam: two almost-touching fingers) -> Tiktaalik fin bones vs your arm (S22-S23, S40)
# F = intuitive: Arthropleura, ~2.6 m long, largest land invertebrate, measured by a tape (S29)
import sys, math, random, os
sys.path.insert(0, '/home/user/rp/tools')
from thumb_lib import *
from hands import hand
HERE = os.path.dirname(os.path.abspath(__file__))
random.seed(7)

BLUR = ''.join(f'<filter id="b{n}" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="{n}"/></filter>' for n in (3, 6, 14, 30))


def bez(p0, p1, p2, p3, t):
    u = 1 - t
    return (u ** 3 * p0[0] + 3 * u * u * t * p1[0] + 3 * u * t * t * p2[0] + t ** 3 * p3[0],
            u ** 3 * p0[1] + 3 * u * u * t * p1[1] + 3 * u * t * t * p2[1] + t ** 3 * p3[1])


def write(name, html):
    open(f'{HERE}/{name}.html', 'w').write(html)


# =====================================================================================
# D  homage E.T.: a giant griffinfly crosses a huge full moon over a Carboniferous swamp forest
# =====================================================================================
MX, MY, MR = 1310, 460, 410
d = BLUR + lin('sky', [(0, '#06151c'), (.5, '#0d2b30'), (.78, '#1b4a44'), (1, '#0a1d1a')])
d += rad('halo', MX, MY, 820, [(0, '#f4f7dc', .55), (.33, '#b9d9b8', .2), (.7, '#3d7b6a', .06), (1, '#0d2b30', 0)])
d += rad('moon', MX - 90, MY - 100, 520, [(0, '#fffdf0', 1), (.55, '#f6f2d6', 1), (1, '#dfe2bf', 1)])
d += lin('wing', [(0, '#f8fff2'), (1, '#cfe9d6')], 1, 0)
d += lin('mist', [(0, '#9fc8b0'), (1, '#9fc8b0')])
b = '<rect width="1920" height="1080" fill="url(#sky)"/>' + stars(110, 600, 0, '#e8f4ff', .55, 0)
b += '<rect width="1920" height="1080" fill="url(#halo)"/>'
b += f'<circle cx="{MX}" cy="{MY}" r="{MR + 40}" fill="#f4f7dc" opacity=".18" filter="url(#b30)"/>'
b += f'<circle cx="{MX}" cy="{MY}" r="{MR}" fill="url(#moon)"/>'
# moon maria and craters
b += f'<g clip-path="url(#mc)" fill="#c9cda6">'
for cx, cy, rx, ry, op in [(1180, 330, 120, 80, .35), (1390, 300, 70, 55, .3), (1420, 520, 140, 90, .28), (1150, 560, 80, 60, .25),
                           (1300, 420, 50, 40, .2), (1510, 410, 45, 70, .22)]:
    b += f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" opacity="{op}" filter="url(#b6)"/>'
for _ in range(12):
    cx, cy, r = random.randint(MX - 250, MX + 250), random.randint(MY - 120, MY + 300), random.randint(6, 14)
    b += f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="#bfc39b" stroke-width="2.5" opacity=".35"/>'
b += '</g>'
d += f'<clipPath id="mc"><circle cx="{MX}" cy="{MY}" r="{MR}"/></clipPath>'


def scale_tree(x, base, h, col, w=16, crown=1.0):
    """Lepidodendron-like: tall straight trunk, forked crown with grass-like leaf tufts"""
    o = f'<path d="M{x - w} {base} L{x - w * .6:.0f} {base - h} L{x + w * .6:.0f} {base - h} L{x + w} {base}Z" fill="{col}"/>'
    top = base - h
    for side in (-1, 1):
        for k, (dx, dy) in enumerate([(70, -60), (120, -40)]):
            ex, ey = x + side * dx * crown, top + dy * crown
            o += f'<path d="M{x} {top + 6} Q{x + side * dx * .4 * crown:.0f} {top - 10} {ex:.0f} {ey:.0f}" stroke="{col}" stroke-width="{w * .7:.0f}" fill="none" stroke-linecap="round"/>'
            o += f'<ellipse cx="{ex:.0f}" cy="{ey - 4:.0f}" rx="{34 * crown:.0f}" ry="{20 * crown:.0f}" fill="{col}"/>'
            for j in range(7):
                a = -math.pi / 2 + (j - 3) * .35
                o += f'<path d="M{ex:.0f} {ey:.0f} l{math.cos(a) * 46 * crown:.0f} {math.sin(a) * 46 * crown:.0f}" stroke="{col}" stroke-width="5" stroke-linecap="round"/>'
    return o


def tree_fern(x, base, h, col, s=1.0):
    o = f'<path d="M{x - 9 * s} {base} Q{x - 4} {base - h * .5} {x} {base - h} L{x + 6 * s} {base - h} Q{x + 6} {base - h * .5} {x + 11 * s} {base}Z" fill="{col}"/>'
    top = base - h
    for a in [-160, -130, -100, -75, -50, -20, 0, -180]:
        r = math.radians(a); L = 170 * s
        ex, ey = x + math.cos(r) * L, top + math.sin(r) * L * .55 + 60 * s
        cxp, cyp = x + math.cos(r) * L * .5, top + math.sin(r) * L * .6 - 30 * s
        o += f'<path d="M{x} {top} Q{cxp:.0f} {cyp:.0f} {ex:.0f} {ey:.0f}" stroke="{col}" stroke-width="{6 * s:.0f}" fill="none" stroke-linecap="round"/>'
        for k in range(1, 9):
            t = k / 9; px, py = bez((x, top), (cxp, cyp), (cxp, cyp), (ex, ey), t)
            ll = 34 * s * (1 - t * .7)
            o += f'<path d="M{px:.0f} {py:.0f} l{-ll * .3:.0f} {ll:.0f} M{px:.0f} {py:.0f} l{ll * .45:.0f} {ll * .8:.0f}" stroke="{col}" stroke-width="{4 * s:.1f}" stroke-linecap="round"/>'
    return o


# far forest (lit by moon haze), mist, near forest
far = '#1d4640'
for x, h in [(760, 210), (880, 260), (1010, 200), (1150, 280), (1460, 240), (1590, 300), (1730, 220), (1850, 270), (640, 240), (520, 200)]:
    b += scale_tree(x, 800, h, far, 11, .8)
b += f'<path d="M0 790 Q480 770 960 788 T1920 780 L1920 1080 L0 1080Z" fill="{far}"/>'
b += '<rect x="0" y="740" width="1920" height="90" fill="url(#mist)" opacity=".25" filter="url(#b30)"/>'
near = '#0a1a17'
for x, h in [(980, 330), (1640, 380)]:
    b += scale_tree(x, 880, h, '#12302b', 15, 1.05)
b += f'<path d="M0 860 Q500 830 1000 856 T1920 850 L1920 1080 L0 1080Z" fill="#0f2622"/>'
b += tree_fern(300, 900, 300, near, 1.3) + tree_fern(1500, 930, 230, near, 1.0) + tree_fern(760, 950, 170, near, .85)
b += f'<path d="M0 930 Q700 900 1400 940 T1920 950 L1920 1080 L0 1080Z" fill="{near}"/>'
# water strip reflecting the moon
b += '<path d="M820 968 Q1250 950 1640 968 L1640 986 Q1250 970 820 986Z" fill="#7fae9a" opacity=".35"/>'
b += ''.join(f'<path d="M{1290 - w} {y} h{2 * w}" stroke="#eef5d8" stroke-width="3" opacity="{op}" stroke-linecap="round"/>'
             for w, y, op in [(160, 972, .55), (110, 982, .45), (220, 966, .3), (70, 990, .4)])

# ---- the griffinfly (Meganeura), top view, backlit by the moon
WF = 'M8,-16 C120,-66 290,-70 352,-44 C368,-34 360,-14 336,-8 C240,6 110,4 8,2 Z'
WH = 'M8,8 C110,10 252,26 330,50 C350,58 344,80 318,82 C222,86 92,56 8,24 Z'


def veins(fore):
    o = ''
    if fore:
        for y0, y1 in [(-12, -46), (-6, -30), (0, -18), (-2, -8)]:
            o += f'<path d="M14,{y0} C140,{y0 - 24} 260,{y1 - 12} 340,{y1 - 8}" fill="none"/>'
        for x in range(40, 340, 15):
            o += f'<path d="M{x},{-12 - x * .12:.0f} l{4},{30 - x * .05:.0f}" fill="none" stroke-width="1.2"/>'
        o += '<path d="M300,-58 l22,4 l-2,8 l-22,-4Z" fill="#0b1714"/>'
    else:
        for y0, y1 in [(10, 54), (14, 66), (18, 76), (22, 70)]:
            o += f'<path d="M14,{y0} C140,{y0 + 10} 250,{y1 - 16} 330,{y1}" fill="none"/>'
        for x in range(40, 330, 15):
            o += f'<path d="M{x},{12 + x * .1:.0f} l{4},{40 - x * .05:.0f}" fill="none" stroke-width="1.2"/>'
        o += '<path d="M292,58 l22,6 l-3,8 l-22,-6Z" fill="#0b1714"/>'
    return o


ins = ''
for sx in (1, -1):
    g = f'<g transform="scale({sx} 1)">'
    for wp, fore in ((WH, False), (WF, True)):
        g += f'<path d="{wp}" fill="url(#wing)" fill-opacity=".38" stroke="#0b1714" stroke-width="4" stroke-linejoin="round"/>'
        g += f'<g stroke="#0b1714" stroke-width="2" opacity=".75">{veins(fore)}</g>'
    ins += g + '</g>'
# legs (spiny), tucked forward under the thorax
for sx in (1, -1):
    for (ax, ay, kx, ky, tx, ty) in [(10, -30, 40, -54, 52, -90), (12, -18, 48, -20, 70, -46), (12, -4, 46, 14, 70, -6)]:
        ins += f'<path d="M{sx * ax},{ay} L{sx * kx},{ky} L{sx * tx},{ty}" fill="none" stroke="#0b1714" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>'
        ins += ''.join(f'<path d="M{sx * (kx + (tx - kx) * t):.0f},{ky + (ty - ky) * t:.0f} l{sx * 7},{-3}" stroke="#0b1714" stroke-width="2.5"/>' for t in (.3, .55, .8))
# abdomen segments
y = 34
for k in range(10):
    w = 17 - k * .6; h = 40
    ins += f'<rect x="{-w:.1f}" y="{y}" width="{2 * w:.1f}" height="{h}" rx="{w * .8:.1f}" fill="#0b1714"/>'
    ins += f'<path d="M{w - 4:.1f},{y + 6} L{w - 4:.1f},{y + h - 6}" stroke="#bfe0c4" stroke-width="2.4" opacity=".45" stroke-linecap="round"/>'
    y += h - 2
ins += f'<path d="M-6,{y} l-14,40 M6,{y} l14,40" stroke="#0b1714" stroke-width="6" stroke-linecap="round"/>'
# thorax and head with huge eyes
ins += '<ellipse cx="0" cy="-4" rx="30" ry="46" fill="#0b1714"/><path d="M24,-30 Q34,-4 22,28" stroke="#bfe0c4" stroke-width="3" fill="none" opacity=".5"/>'
ins += '<ellipse cx="0" cy="-56" rx="26" ry="18" fill="#0b1714"/>'
ins += '<circle cx="-24" cy="-66" r="22" fill="#0b1714"/><circle cx="24" cy="-66" r="22" fill="#0b1714"/>'
ins += '<path d="M36,-82 Q48,-66 40,-50" stroke="#bfe0c4" stroke-width="3" fill="none" opacity=".55"/>'
b += f'<g transform="translate({MX + 6} {MY - 70}) rotate(-9) scale(1.16)">{ins}</g>'
# drifting spores and sparkles
for _ in range(40):
    b += f'<circle cx="{random.randint(700, 1880)}" cy="{random.randint(120, 900)}" r="{random.choice([1.5, 2.2, 3])}" fill="#f2f5d8" opacity="{random.uniform(.2, .6):.2f}"/>'
b += spark(1720, 190, 20) + spark(870, 300, 14) + spark(1660, 700, 16, op=.6) + spark(1050, 120, 12)
write('D', page('#06151c', svg(d, b), [('WINGS', 196, 'w'), ('LIKE A', 132, 'w'), ('HAWK', 236, 'y')], outline='#03100f'))

# =====================================================================================
# E  homage The Creation of Adam: Tiktaalik's fin (glowing upper-arm / forearm / wrist bones) almost touches a human finger
# =====================================================================================
d = BLUR + lin('wat', [(0, '#0e3d44'), (.45, '#1a5d5a'), (.8, '#174a45'), (1, '#0a2427')])
d += rad('sun', 1500, -60, 1100, [(0, '#f6f0c8', .55), (.35, '#9fd8c0', .18), (1, '#1a5d5a', 0)])
d += lin('ray', [(0, '#f8f4d0'), (1, '#f8f4d0')])
d += lin('tbody', [(0, '#c9a062'), (.45, '#9a7a45'), (1, '#4d4a2e')])
d += lin('tbelly', [(0, '#e8d3a2'), (1, '#b89a66')])
d += lin('fin', [(0, '#8a6e3e'), (1, '#c9a46a')], 1, 0)
d += lin('arm', [(0, '#c98f6a'), (.5, '#e7b892'), (1, '#f2c9a3')], 0, 1)
d += rad('gap', 1072, 648, 120, [(0, '#fff4c8', .9), (.4, '#f2d27a', .35), (1, '#f2d27a', 0)])
d += '<filter id="glow" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="7" result="g"/><feMerge><feMergeNode in="g"/><feMergeNode in="SourceGraphic"/></feMerge></filter>'
b = '<rect width="1920" height="1080" fill="url(#wat)"/><rect width="1920" height="1080" fill="url(#sun)"/>'
# god rays from the surface (top right)
for x0, w, op in [(1100, 120, .10), (1330, 80, .12), (1520, 160, .09), (1720, 90, .11), (900, 70, .07), (1880, 120, .08)]:
    b += f'<path d="M{x0} 0 L{x0 + w} 0 L{x0 - 380 + w * 2} 1080 L{x0 - 520} 1080Z" fill="url(#ray)" opacity="{op}"/>'
# caustic ripples at the surface
for k in range(7):
    yy = 22 + k * 20
    b += f'<path d="M{900 + k * 20} {yy} q60 -10 120 0 t120 0 t120 0 t120 0 t120 0 t120 0 t120 0 t120 0" fill="none" stroke="#d9f3e0" stroke-width="2" opacity="{.25 - k * .03:.2f}"/>'
# far weeds and floor
b += '<path d="M0 930 Q600 900 1200 930 T1920 920 L1920 1080 L0 1080Z" fill="#0b2a2a"/>'
for x in list(range(20, 1500, 46)):
    h = random.randint(80, 240); c = random.choice(['#123c36', '#0f332f', '#174841'])
    b += f'<path d="M{x} 960 q{random.randint(-30, 30)} {-h / 2:.0f} {random.randint(-20, 20)} {-h}" stroke="{c}" stroke-width="{random.randint(6, 12)}" fill="none" stroke-linecap="round" opacity=".9"/>'
b += '<path d="M0 990 Q500 970 1000 990 T1920 995 L1920 1080 L0 1080Z" fill="#071d1d"/>'
# bubbles
for _ in range(30):
    x, yy, r = random.randint(700, 1880), random.randint(120, 900), random.choice([3, 4, 6, 8])
    b += f'<circle cx="{x}" cy="{yy}" r="{r}" fill="none" stroke="#d9f3e0" stroke-width="1.6" opacity="{random.uniform(.25, .55):.2f}"/>'
b += '<rect width="1920" height="1080" fill="url(#gap)"/>'

# ---- Tiktaalik (upper right), head to the left, reaching down-left with its pectoral fin
T = ''
# tail / body going off the right edge
T += '<path d="M1330 330 C1480 280 1700 270 1930 300 L1930 520 C1740 540 1560 520 1420 490 C1360 470 1320 420 1330 330Z" fill="url(#tbody)" stroke="#2c2616" stroke-width="5"/>'
T += '<path d="M1360 470 C1520 520 1740 525 1930 505 L1930 525 C1740 545 1520 535 1380 492Z" fill="url(#tbelly)" opacity=".8"/>'
# scales
d += '<clipPath id="tb"><path d="M1330 330 C1480 280 1700 270 1930 300 L1930 520 C1740 540 1560 520 1420 490 C1360 470 1320 420 1330 330Z"/></clipPath>'
sc = '<g clip-path="url(#tb)" fill="none" stroke="#3a3220" stroke-width="2.4" opacity=".45">'
for row in range(9):
    for col in range(22):
        x = 1350 + col * 28 + (row % 2) * 14; yy = 300 + row * 26
        sc += f'<path d="M{x - 13} {yy} q13 14 26 0"/>'
sc += '</g>'
T += sc
T += '<path d="M1360 320 C1500 285 1720 280 1930 306" stroke="#f2e2b0" stroke-width="5" fill="none" opacity=".55" stroke-linecap="round"/>'
# dorsal ridge spots
T += ''.join(f'<ellipse cx="{x}" cy="{y}" rx="16" ry="9" fill="#5e4c2a" opacity=".6"/>' for x, y in [(1480, 330), (1560, 318), (1650, 312), (1740, 312), (1830, 315)])
# flat crocodile-like head
HEAD = 'M1340 340 C1300 330 1200 340 1110 372 C1080 384 1078 410 1100 424 C1170 452 1290 470 1380 470 C1410 450 1420 380 1340 340Z'
T += f'<path d="{HEAD}" fill="url(#tbody)" stroke="#2c2616" stroke-width="5" stroke-linejoin="round"/>'
T += '<path d="M1098 418 C1170 436 1280 446 1370 444" stroke="#2c2616" stroke-width="4" fill="none" stroke-linecap="round"/>'  # mouth line
T += '<path d="M1110 404 C1180 420 1280 428 1360 426" stroke="#e8d3a2" stroke-width="3" fill="none" opacity=".5"/>'
T += '<path d="M1130 372 C1200 348 1290 338 1350 346" stroke="#f2e2b0" stroke-width="5" fill="none" opacity=".6" stroke-linecap="round"/>'
# eyes on top of the head
T += '<ellipse cx="1262" cy="352" rx="26" ry="18" fill="#2c2616"/><ellipse cx="1262" cy="350" rx="20" ry="13" fill="#e9f1d0"/>'
T += '<circle cx="1256" cy="350" r="8" fill="#1b160c"/><circle cx="1253" cy="347" r="3" fill="#fff"/>'
T += '<circle cx="1124" cy="388" r="4" fill="#2c2616"/>'  # nostril
# texture dots on head
T += ''.join(f'<circle cx="{random.randint(1150, 1360)}" cy="{random.randint(360, 420)}" r="{random.choice([2, 3])}" fill="#5e4c2a" opacity=".5"/>' for _ in range(30))
# gill line / neck fold (it had a neck that could move)
T += '<path d="M1392 360 C1408 400 1408 440 1390 470" stroke="#2c2616" stroke-width="4" fill="none"/>'
T += '<path d="M1408 358 C1424 400 1424 440 1406 472" stroke="#2c2616" stroke-width="3" fill="none" opacity=".5"/>'
# pectoral fin: fleshy lobe with glowing bones, rays fan at the tip (points down-left)
FA, FB = (1440, 470), (1100, 632)        # shoulder -> fin tip
ang = math.degrees(math.atan2(FB[1] - FA[1], FB[0] - FA[0]))
Lf = math.hypot(FB[0] - FA[0], FB[1] - FA[1])
fin = (f'<path d="M-20,-58 C{Lf * .25:.0f},-70 {Lf * .55:.0f},-42 {Lf * .76:.0f},-26 C{Lf * .8:.0f},-10 {Lf * .8:.0f},12 {Lf * .76:.0f},24 C{Lf * .55:.0f},48 {Lf * .2:.0f},66 -20,58 Z" '
       f'fill="url(#fin)" stroke="#2c2616" stroke-width="5" stroke-linejoin="round"/>')
# fin rays fan
for k in range(9):
    a = math.radians(-30 + k * 7.5)
    x0, y0 = Lf * .74, (k - 4) * 5
    fin += f'<path d="M{x0:.0f},{y0:.0f} L{x0 + math.cos(a) * 90:.0f},{y0 + math.sin(a) * 100:.0f}" stroke="#d9be86" stroke-width="7" stroke-linecap="round"/>'
fin += f'<path d="M{Lf * .74:.0f},-26 Q{Lf * .95:.0f},-62 {Lf + 4:.0f},-4 Q{Lf * .95:.0f},58 {Lf * .74:.0f},26Z" fill="#e8d3a2" fill-opacity=".35" stroke="#2c2616" stroke-width="3"/>'
fin += f'<path d="M10,-38 C{Lf * .35:.0f},-52 {Lf * .6:.0f},-36 {Lf * .76:.0f},-20" stroke="#f2e2b0" stroke-width="4" fill="none" opacity=".6"/>'
# bones: humerus (1), radius + ulna (2), wrist bones (small)
bone = '<g filter="url(#glow)" fill="#fff1bf" stroke="#f2d27a" stroke-width="2">'
bone += f'<rect x="20" y="-11" width="{Lf * .3:.0f}" height="22" rx="11"/>'
bone += f'<rect x="{Lf * .34:.0f}" y="-20" width="{Lf * .2:.0f}" height="13" rx="6.5" transform="rotate(-4 {Lf * .34:.0f} -14)"/>'
bone += f'<rect x="{Lf * .34:.0f}" y="6" width="{Lf * .2:.0f}" height="13" rx="6.5" transform="rotate(4 {Lf * .34:.0f} 12)"/>'
for i, (bx, by) in enumerate([(.57, -18), (.57, 2), (.63, -10), (.63, 10), (.69, -14), (.69, 4)]):
    bone += f'<circle cx="{Lf * bx:.0f}" cy="{by}" r="8"/>'
bone += '</g>'
fin += bone
T += f'<g transform="translate({FA[0]} {FA[1]}) rotate({ang:.1f})">{fin}</g>'
b += T

# ---- the human arm from the lower left, index finger reaching up-right (hands.py)
WX, WY = 842, 742; HA = 68
ax = math.radians(HA)
dxu, dyu = math.sin(ax), -math.cos(ax)            # finger direction
nx, ny = -dyu, dxu                                 # normal
e0 = (WX - dxu * 1150, WY - dyu * 1150)
w0, w1 = 150, 86
arm = (f'M{e0[0] + nx * w0 / 2:.0f},{e0[1] + ny * w0 / 2:.0f} L{WX + nx * w1 / 2:.0f},{WY + ny * w1 / 2:.0f} '
       f'L{WX - nx * w1 / 2:.0f},{WY - ny * w1 / 2:.0f} L{e0[0] - nx * w0 / 2:.0f},{e0[1] - ny * w0 / 2:.0f}Z')
b += f'<path d="{arm}" fill="url(#arm)" stroke="#2a1c14" stroke-width="5" stroke-linejoin="round"/>'
# rim light on the upper edge of the arm
b += f'<path d="M{e0[0] - nx * (w0 / 2 - 8):.0f},{e0[1] - ny * (w0 / 2 - 8):.0f} L{WX - nx * (w1 / 2 - 6):.0f},{WY - ny * (w1 / 2 - 6):.0f}" stroke="#fff0d8" stroke-width="5" opacity=".6" stroke-linecap="round"/>'
# matching forearm bones (radius + ulna) faintly glowing
for off in (-14, 14):
    p0 = (WX - dxu * 420 + nx * off, WY - dyu * 420 + ny * off); p1 = (WX - dxu * 40 + nx * off * .7, WY - dyu * 40 + ny * off * .7)
    b += f'<path d="M{p0[0]:.0f},{p0[1]:.0f} L{p1[0]:.0f},{p1[1]:.0f}" stroke="#fff1bf" stroke-width="10" stroke-linecap="round" opacity=".55" filter="url(#glow)"/>'
b += hand(WX, WY, angle=HA, size=118, side='R', view='back', pose='point', skin='#efc29c', line='#2a1c14')
# the spark in the gap
b += '<circle cx="1072" cy="648" r="26" fill="#fff6d6" opacity=".55" filter="url(#b14)"/>'
b += spark(1074, 646, 22, '#fffbe8', .95) + spark(1120, 590, 10) + spark(1022, 700, 9) + spark(1700, 640, 16, op=.6) + spark(980, 180, 12, op=.6)
write('E', page('#0e3d44', svg(d, b), [('YOUR ARM', 168, 'w'), ('WAS A', 124, 'w'), ('FIN?', 248, 'y')], outline='#04191b'))

# =====================================================================================
# F  intuitive: Arthropleura stretched across the forest floor, a tape measure along its body
# =====================================================================================
d = BLUR + lin('fsky', [(0, '#1c2a16'), (.45, '#33421f'), (.7, '#55562a'), (1, '#2a2412')])
d += rad('sunF', 1650, 80, 1100, [(0, '#ffe7a6', .6), (.35, '#e8b85a', .22), (1, '#55562a', 0)])
d += lin('shaft', [(0, '#fff2c0'), (1, '#fff2c0')])
d += lin('soil', [(0, '#4a3c1d'), (1, '#1c160b')])
d += lin('plate', [(0, '#d99a52'), (.5, '#a8662e'), (1, '#5a3418')])
d += lin('bark', [(0, '#2d3a1e'), (.5, '#4a5a2c'), (1, '#24301a')], 1, 0)
d += lin('tape', [(0, '#f6d66a'), (1, '#d9a93a')])
b = '<rect width="1920" height="1080" fill="url(#fsky)"/><rect width="1920" height="1080" fill="url(#sunF)"/>'
# background scale-tree trunks with diamond bark
for x, w, col, op in [(560, 50, '#2a3a1c', .7), (760, 36, '#2a3a1c', .6), (1080, 60, '#26341a', .8), (1330, 44, '#2a3a1c', .65), (1830, 70, '#1f2b15', .9), (1600, 40, '#2a3a1c', .6)]:
    b += f'<rect x="{x - w / 2}" y="0" width="{w}" height="760" fill="{col}" opacity="{op}"/>'
    b += f'<g opacity="{op * .5:.2f}" stroke="#121a0b" stroke-width="2" fill="none">'
    for yy in range(10, 760, 26):
        for xx in range(int(x - w / 2), int(x + w / 2) - 10, 18):
            ox = 9 if (yy // 26) % 2 else 0
            b += f'<path d="M{xx + ox} {yy} l9 -11 l9 11 l-9 11Z"/>'
    b += '</g>'
# light shafts
for x0, w, op in [(1500, 140, .14), (1700, 90, .12), (1250, 110, .10), (1880, 160, .1)]:
    b += f'<path d="M{x0} 0 L{x0 + w} 0 L{x0 - 500 + w} 1080 L{x0 - 640} 1080Z" fill="url(#shaft)" opacity="{op}"/>'
# ferns behind
for x, h, s in [(380, 800, 1.0), (1240, 790, .8), (1720, 800, 1.1)]:
    b += tree_fern(x, h, 200 * s, '#22301a', s)
# forest floor
b += '<path d="M0 690 Q700 660 1300 690 T1920 680 L1920 1080 L0 1080Z" fill="url(#soil)"/>'
b += blobs(40, 0, 720, 1920, 1060, '#120d06', .2, .45, 60, 200)
for _ in range(140):   # leaf litter
    x, yy = random.randint(0, 1900), random.randint(700, 1070)
    c = random.choice(['#6b5626', '#7e6a2e', '#5a4a20', '#8a6a2c', '#4c5a26'])
    a = random.randint(0, 180)
    b += f'<ellipse cx="{x}" cy="{yy}" rx="{random.randint(10, 22)}" ry="{random.randint(4, 8)}" fill="{c}" opacity="{random.uniform(.5, .9):.2f}" transform="rotate({a} {x} {yy})"/>'
for _ in range(14):    # seeds / nuts (what it probably ate)
    x, yy = random.randint(80, 1500), random.randint(760, 1040)
    b += f'<ellipse cx="{x}" cy="{yy}" rx="11" ry="14" fill="#9a6a34" stroke="#3a2510" stroke-width="2.5"/><path d="M{x - 4} {yy - 8} q4 -4 8 0" stroke="#f0d49a" stroke-width="2" fill="none" opacity=".6"/>'

# ---- Arthropleura body along a curve (tail lower-left -> head right)
P0, P1, P2, P3 = (240, 850), (640, 960), (930, 540), (1560, 480)
N = 30
pts = []
# sample at equal arc length
dense = [bez(P0, P1, P2, P3, i / 2000) for i in range(2001)]
acc = [0]
for i in range(1, len(dense)):
    acc.append(acc[-1] + math.hypot(dense[i][0] - dense[i - 1][0], dense[i][1] - dense[i - 1][1]))
total = acc[-1]
j = 0
for k in range(N + 1):
    target = total * k / N
    while acc[j] < target and j < len(acc) - 1:
        j += 1
    pts.append(dense[j])


def tang(i):
    a = pts[max(0, i - 1)]; c = pts[min(N, i + 1)]
    return math.atan2(c[1] - a[1], c[0] - a[0])


seg = total / N
shadow = ''
for i in range(N + 1):
    x, yy = pts[i]
    shadow += f'<ellipse cx="{x:.0f}" cy="{yy + 40:.0f}" rx="{seg * .9:.0f}" ry="70" fill="#0a0704" opacity=".35"/>'
b += f'<g filter="url(#b14)">{shadow}</g>'
legs = ''
plates = ''
for i in range(N):
    x, yy = pts[i]; a = tang(i); t = i / N
    wdt = 120 + 110 * math.sin(math.pi * min(1, t * 1.15)) ** .6    # body width: narrow tail, wide middle
    if t > .9: wdt *= 1 - (t - .9) * 1.5
    deg = math.degrees(a)
    # two pairs of legs per body ring (it was a millipede relative)
    for side in (-1, 1):
        for off in (-seg * .22, seg * .22):
            L1 = wdt * .5 + 34
            swing = 18 * math.sin(i * 1.3 + off)
            legs += (f'<g transform="translate({x:.0f} {yy:.0f}) rotate({deg:.1f})"><path d="M{off:.0f},{side * wdt * .38:.0f} '
                     f'L{off + swing:.0f},{side * L1:.0f} L{off + swing + 12:.0f},{side * (L1 + 26):.0f}" fill="none" stroke="#2a1708" stroke-width="9" stroke-linecap="round" stroke-linejoin="round"/>'
                     f'<path d="M{off:.0f},{side * wdt * .38:.0f} L{off + swing:.0f},{side * L1:.0f}" stroke="#b07a3e" stroke-width="3" opacity=".6"/></g>')
    # tergite plate with side lobes (paranota)
    hw = wdt / 2; hl = seg * .62
    plate = (f'M{-hl:.0f},{-hw * .55:.0f} Q{-hl * .9:.0f},{-hw:.0f} {-hl * .2:.0f},{-hw:.0f} L{hl * .7:.0f},{-hw * .96:.0f} Q{hl * 1.15:.0f},{-hw * .9:.0f} {hl:.0f},{-hw * .45:.0f} '
             f'L{hl:.0f},{hw * .45:.0f} Q{hl * 1.15:.0f},{hw * .9:.0f} {hl * .7:.0f},{hw * .96:.0f} L{-hl * .2:.0f},{hw:.0f} Q{-hl * .9:.0f},{hw:.0f} {-hl:.0f},{hw * .55:.0f}Z')
    pg = f'<g transform="translate({x:.0f} {yy:.0f}) rotate({deg:.1f})">'
    pg += f'<path d="{plate}" fill="url(#plate)" stroke="#2a1708" stroke-width="5" stroke-linejoin="round"/>'
    pg += f'<path d="M{-hl * .5:.0f},{-hw * .55:.0f} L{-hl * .5:.0f},{hw * .55:.0f}" stroke="#4a2a12" stroke-width="3" opacity=".6"/>'  # mid groove
    pg += f'<path d="M{-hl * .7:.0f},{-hw * .86:.0f} L{hl * .6:.0f},{-hw * .84:.0f}" stroke="#ffd9a0" stroke-width="5" opacity=".55" stroke-linecap="round"/>'  # rim light (sun side)
    for kx, ky in [(-.2, -.6), (.3, -.62), (-.2, .6), (.3, .62), (0, -.25), (0, .25)]:
        pg += f'<circle cx="{hl * kx:.0f}" cy="{hw * ky:.0f}" r="5" fill="#e6b06a" stroke="#4a2a12" stroke-width="1.6"/>'
    pg += '</g>'
    plates = pg + plates   # head-side plates sit under the next one toward the tail
b += legs + plates
# head
hx, hy = pts[N]; a = math.degrees(tang(N))
head = '<path d="M-30,-70 Q40,-86 70,-40 Q86,0 70,40 Q40,86 -30,70 Z" fill="url(#plate)" stroke="#2a1708" stroke-width="5"/>'
head += '<path d="M-20,-62 Q36,-74 60,-36" stroke="#ffd9a0" stroke-width="5" fill="none" opacity=".6" stroke-linecap="round"/>'
for side in (-1, 1):   # segmented antennae
    px, py = 64, side * 26
    for k in range(7):
        qx, qy = px + 26, py + side * (6 + k * 3)
        head += f'<path d="M{px:.0f},{py:.0f} L{qx:.0f},{qy:.0f}" stroke="#2a1708" stroke-width="{9 - k * .7:.1f}" stroke-linecap="round"/>'
        px, py = qx, qy
    head += f'<circle cx="34" cy="{side * 40}" r="7" fill="#1a0f05"/><circle cx="32" cy="{side * 42}" r="2.5" fill="#fff"/>'
b += f'<g transform="translate({hx:.0f} {hy:.0f}) rotate({a:.1f})">{head}</g>'
b += f'<ellipse cx="{hx + 40:.0f}" cy="{hy - 40:.0f}" rx="220" ry="160" fill="#ffe7a6" opacity=".10" filter="url(#b30)"/>'

# ---- tape measure along the near side of the body (tail case -> beyond the head)
tp = []
for i in range(N + 1):
    x, yy = pts[i]; a = tang(i); t = i / N
    wdt = 120 + 110 * math.sin(math.pi * min(1, t * 1.15)) ** .6
    off = wdt * .5 + 80
    tp.append((x - math.sin(a) * -off, yy + math.cos(a) * off))
tp[-1] = (tp[-1][0] + 60, tp[-1][1] + 6)
tpath = 'M' + ' L'.join(f'{x:.0f},{yy:.0f}' for x, yy in tp)
b += f'<path d="{tpath}" fill="none" stroke="#2a1708" stroke-width="40" stroke-linejoin="round" stroke-linecap="butt" opacity=".9"/>'
b += f'<path d="{tpath}" fill="none" stroke="url(#tape)" stroke-width="32" stroke-linejoin="round"/>'
b += f'<path d="{tpath}" fill="none" stroke="#3a2510" stroke-width="12" stroke-dasharray="3 17" stroke-linejoin="round" transform="translate(0 -6)"/>'
b += f'<path d="{tpath}" fill="none" stroke="#3a2510" stroke-width="22" stroke-dasharray="3 97" stroke-linejoin="round"/>'
# end hook near the head, tape case at the tail
ex, ey = tp[-1]
b += f'<rect x="{ex - 4:.0f}" y="{ey - 26:.0f}" width="16" height="52" rx="3" fill="#cfd4d8" stroke="#2a1708" stroke-width="4"/>'
cx0, cy0 = tp[0]
b += f'<g transform="translate({cx0 - 40:.0f} {cy0 - 10:.0f})"><rect x="-70" y="-62" width="130" height="124" rx="28" fill="#c9443a" stroke="#2a1708" stroke-width="6"/>' \
     '<circle cx="-6" cy="0" r="34" fill="#e8e2d0" stroke="#2a1708" stroke-width="5"/><circle cx="-6" cy="0" r="10" fill="#2a1708"/>' \
     '<path d="M-60 -48 Q-20 -60 40 -50" stroke="#ffb6a8" stroke-width="6" fill="none" opacity=".6" stroke-linecap="round"/></g>'
b += spark(1720, 330, 18) + spark(1460, 420, 12) + spark(1000, 560, 10, op=.6) + spark(1880, 520, 14, op=.6)
for _ in range(30):
    b += f'<circle cx="{random.randint(900, 1900)}" cy="{random.randint(80, 700)}" r="{random.choice([1.5, 2.5])}" fill="#fff2c0" opacity="{random.uniform(.25, .6):.2f}"/>'
write('F', page('#2a2412', svg(d, b), [('2.6 METERS', 176, 'y'), ('OF LEGS', 150, 'w')], outline='#140c04'))
print('wrote D E F')
