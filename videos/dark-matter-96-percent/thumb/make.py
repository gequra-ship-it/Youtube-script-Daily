# Thumbnails A-C for dark-matter-96-percent (guideline 16-6 / 16-8, brief tools/briefs/thumb_art.md). Run: python3 videos/dark-matter-96-percent/thumb/make.py
# Title number (96 vs 95) undecided -> thumbnail text uses only 5% / 68% / words (no 95, no 96).
# A  WE SEE ONLY 5%      homage: Titanic (1997) "I'm flying" at the bow + the iceberg: the frog stands at the ship's bow with arms spread toward
#                        an iceberg whose small glowing tip (stars, a galaxy) is all that shows; a huge dark ghost bulk hides under the water.
#                        Script S03 ("only about 5 percent of the cosmos"), S05 ("something we cannot see"), S51-S53 (bright foam on a dark ocean).
# B  WHAT HOLDS IT TOGETHER?  intuitive: a big spiral galaxy whose fast outer stars should fly off, wrapped in a faint invisible halo; the astronaut
#                        frog shines a torch at the empty-looking halo. Script S16-S20 ("Something is holding them together ... invisible halo").
# C  68% UNKNOWN         intuitive: the cosmic pie on a plate: only a thin golden 5% slice is real (on the frog's fork); the 27% slice is a purple
#                        ghost and the 68% part is only a dashed outline. Script S34-S40, S56 ("dark energy ... roughly 68 percent ... remains unknown").
import os, sys, math, random
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', '..', 'tools'))
from thumb_lib import page, svg, lin, rad, spark

INK = '#1d2b1c'; GREEN = '#6aa55a'; DARKG = '#4d8a4a'; BELLY = '#9cc98a'
FILTERS = ''.join(f'<filter id="b{n}" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="{n}"/></filter>' for n in (2, 3, 6, 12, 24, 50))


def poly(pts):
    return 'M' + ' L'.join(f'{x:.1f},{y:.1f}' for x, y in pts) + 'Z'


def path(pts):
    return 'M' + ' L'.join(f'{x:.1f},{y:.1f}' for x, y in pts)


# ---------------- mascot frog (tools/assets/frog.svg body), posable ----------------
def limb(d, w=7.5, wi=3.4):
    return f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="{w}"/><path d="{d}" fill="none" stroke="{GREEN}" stroke-width="{wi}"/>'


def end_of(d):
    n = [float(v) for v in d.replace('M', ' ').replace('q', ' ').split()]
    return n[0] + n[-2], n[1] + n[-1]


def frog(x, y, s, rot=0, flip=False, look=(0, 0), mouth='O', armL=None, armR=None, legs=None, helmet=False,
         back='', front='', mid='', hat=''):
    sx = -s if flip else s
    g = [f'<g transform="translate({x} {y}) rotate({rot}) scale({sx} {s})" stroke="{INK}" stroke-linejoin="round" stroke-linecap="round">', back]
    if helmet:   # backpack
        g.append('<rect x="-50" y="-58" width="20" height="42" rx="7" fill="#d9dde6" stroke-width="3"/><rect x="-46" y="-52" width="5" height="30" rx="2" fill="#fff" stroke="none" opacity=".7"/>')
    for hx, hy, fx, fy, fa in (legs or ((-20, -6, -22, 4, 0), (20, -6, 22, 4, 0))):
        if abs(fx - hx) + abs(fy - hy) > 14:
            g.append(limb(f'M{hx} {hy} L{fx} {fy}', 15, 9))
        g.append(f'<ellipse cx="{fx}" cy="{fy}" rx="16" ry="9" transform="rotate({fa} {fx} {fy})" fill="{DARKG}" stroke-width="3.2"/>')
    g.append(f'<path d="M-34 0 q-6 -64 34 -70 q40 -2 42 62 q0 10 -6 12 q-36 6 -70 -4z" fill="{GREEN}" stroke-width="4"/>')
    g.append(f'<ellipse cx="2" cy="-12" rx="22" ry="20" fill="{BELLY}" stroke="none" opacity=".7"/>')
    g.append('<path d="M-24 -50 q6 -14 18 -16" fill="none" stroke="#b6dea0" stroke-width="3" opacity=".8"/>')
    lx, ly = look
    for ex in (-10, 22):
        g.append(f'<circle cx="{ex}" cy="-66" r="13.5" fill="#f4f5ea" stroke-width="3.2"/>')
        g.append(f'<circle cx="{ex + 1 + lx}" cy="{-66 + ly}" r="4.4" fill="{INK}" stroke="none"/>')
        g.append(f'<circle cx="{ex + 2.4 + lx}" cy="{-67.6 + ly}" r="1.5" fill="#fff" stroke="none"/>')
    g.append('<path d="M-22 -88 q12 -9 24 -1 M10 -89 q12 -8 24 1" fill="none" stroke-width="3.4"/>')
    if mouth == 'O':
        g.append('<ellipse cx="6" cy="-38" rx="10" ry="12" fill="#7a2f33" stroke-width="3"/><ellipse cx="6" cy="-31" rx="6" ry="4" fill="#e07b7b" stroke="none"/>')
    else:
        g.append('<ellipse cx="6" cy="-41" rx="6" ry="7.5" fill="#7a2f33" stroke-width="3"/>')
    g.append('<ellipse cx="-18" cy="-48" rx="5" ry="3" fill="#e98a8a" stroke="none" opacity=".55"/><ellipse cx="30" cy="-48" rx="5" ry="3" fill="#e98a8a" stroke="none" opacity=".55"/>')
    g.append(hat)
    if helmet:   # space helmet bubble
        g.append('<circle cx="6" cy="-56" r="47" fill="#cfeaff" fill-opacity=".13" stroke="#eef6ff" stroke-width="4.5"/>')
        g.append('<path d="M-28 -80 q12 -18 32 -21" fill="none" stroke="#fff" stroke-width="5" opacity=".8"/><path d="M44 -40 q6 -10 6 -22" fill="none" stroke="#fff" stroke-width="3" opacity=".5"/>')
        g.append('<ellipse cx="6" cy="-12" rx="42" ry="9" fill="#e6eaf2" stroke-width="3.2"/><path d="M-30 -14 q36 8 72 0" fill="none" stroke="#fff" stroke-width="2.2" opacity=".8"/>')
    g.append(mid)
    for a in (armL or 'M-34 -22 q-14 6 -16 22', armR or 'M38 -22 q14 6 16 22'):
        g.append(limb(a)); ex_, ey_ = end_of(a)
        g.append(f'<circle cx="{ex_:.1f}" cy="{ey_:.1f}" r="5.6" fill="{GREEN}" stroke-width="3"/>')
    g.append(front); g.append('</g>')
    return ''.join(g)


def mini_galaxy(cx, cy, r, rot, col='#fff2c8', arms=2, n=70, rnd=None, op=1.0):
    rnd = rnd or random.Random(1)
    o = f'<g transform="translate({cx} {cy}) rotate({rot}) scale(1 .45)">'
    o += f'<circle r="{r * .9:.0f}" fill="{col}" opacity="{.25 * op:.2f}" filter="url(#b6)"/>'
    for a in range(arms):
        for k in range(n):
            t = k / n
            ang = a * 2 * math.pi / arms + t * 3.6
            rr = r * (.12 + .95 * t)
            x, y = rr * math.cos(ang) + rnd.gauss(0, r * .05), rr * math.sin(ang) + rnd.gauss(0, r * .05)
            o += f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{rnd.uniform(.8, 2.4) * (1 - t * .5) * max(1, r / 60):.1f}" fill="{col}" opacity="{op * rnd.uniform(.5, 1):.2f}"/>'
    o += f'<circle r="{r * .2:.0f}" fill="#fff" opacity="{op:.2f}" filter="url(#b3)"/><circle r="{r * .1:.0f}" fill="#fff" opacity="{op:.2f}"/></g>'
    return o


def cosmic_web(nodes, rnd, glow='#b46bff', core='#f0e0ff', knot='#ffffff', w=1.0, k=3, maxd=260, dots=26, op=1.0):
    """Large-scale structure: glowing filaments between nearest nodes, bright knots at the nodes, dark voids between."""
    edges = set()
    for i, (x, y) in enumerate(nodes):
        near = sorted(((math.hypot(x - u, y - v), j) for j, (u, v) in enumerate(nodes) if j != i))[:k]
        for dd, j in near:
            if dd < maxd:
                edges.add((min(i, j), max(i, j)))
    lo = hi = dt = ''
    for i, j in edges:
        (x0, y0), (x1, y1) = nodes[i], nodes[j]
        L = math.hypot(x1 - x0, y1 - y0); bend = rnd.uniform(-.18, .18) * L
        mx, my = (x0 + x1) / 2 - (y1 - y0) / L * bend, (y0 + y1) / 2 + (x1 - x0) / L * bend
        dpath = f'M{x0:.0f} {y0:.0f} Q{mx:.0f} {my:.0f} {x1:.0f} {y1:.0f}'
        lo += f'<path d="{dpath}" stroke-width="{16 * w:.1f}"/>'
        hi += f'<path d="{dpath}" stroke-width="{2.6 * w:.1f}"/>'
        for _ in range(int(dots * L / 200)):
            t = rnd.random()
            px = (1 - t) ** 2 * x0 + 2 * t * (1 - t) * mx + t * t * x1 + rnd.gauss(0, 5 * w)
            py = (1 - t) ** 2 * y0 + 2 * t * (1 - t) * my + t * t * y1 + rnd.gauss(0, 5 * w)
            dt += f'<circle cx="{px:.0f}" cy="{py:.0f}" r="{rnd.uniform(.8, 2.2) * w:.1f}"/>'
    o = f'<g opacity="{op}">'
    o += f'<g fill="none" stroke="{glow}" opacity=".45" filter="url(#b6)" stroke-linecap="round">{lo}</g>'
    o += f'<g fill="none" stroke="{core}" opacity=".8" stroke-linecap="round">{hi}</g>'
    o += f'<g fill="{core}" opacity=".75">{dt}</g>'
    for x, y in nodes:
        r0 = rnd.uniform(5, 11) * w
        o += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r0 * 2.6:.0f}" fill="{glow}" opacity=".5" filter="url(#b6)"/><circle cx="{x:.0f}" cy="{y:.0f}" r="{r0 * .55:.1f}" fill="{knot}"/>'
    return o + '</g>'


def scatter(n, rnd, x0, y0, x1, y1, inside, gap=70):
    pts = []
    for _ in range(n * 60):
        if len(pts) >= n:
            break
        x, y = rnd.uniform(x0, x1), rnd.uniform(y0, y1)
        if inside(x, y) and all(math.hypot(x - u, y - v) > gap for u, v in pts):
            pts.append((x, y))
    return pts


def in_poly(x, y, P_):
    c = False
    for i in range(len(P_)):
        (x0, y0), (x1, y1) = P_[i], P_[i - 1]
        if (y0 > y) != (y1 > y) and x < (x1 - x0) * (y - y0) / (y1 - y0) + x0:
            c = not c
    return c


# =============================== A: Titanic bow + iceberg ===============================
def make_A():
    rnd = random.Random(5)
    HY = 560   # waterline / horizon
    d = FILTERS
    d += lin('skyA', [(0, '#03061a'), (.6, '#0b1640'), (1, '#1d3166')])
    d += lin('seaA', [(0, '#0d2c52'), (.25, '#071a33'), (1, '#01050e')])
    d += rad('moonA', 1300, 330, 650, [(0, '#bfe6ff', .55), (.35, '#5aa0ff', .18), (1, '#3060ff', 0)])
    d += lin('iceA', [(0, '#ffffff'), (.45, '#d6f2ff'), (1, '#7cc4f0')], x2=.6, y2=1)
    d += rad('bulkA', 1250, 760, 520, [(0, '#5b3fb0', .55), (.6, '#2a1d6e', .45), (1, '#1a1050', .05)])
    d += lin('hullA', [(0, '#1a1f2a'), (1, '#05070b')], x2=0, y2=1)
    d += lin('deckA', [(0, '#7b5a3c'), (1, '#4e3826')], x2=1, y2=0)
    d += rad('vigA', 1100, 520, 1250, [(0, '#000', 0), (.6, '#000', 0), (1, '#000', .7)])
    b = f'<rect width="1920" height="{HY}" fill="url(#skyA)"/>'
    for _ in range(170):
        b += f'<circle cx="{rnd.uniform(0, 1920):.0f}" cy="{rnd.uniform(0, HY - 30):.0f}" r="{rnd.choice([1.2, 1.7, 2.3])}" fill="#e8f2ff" opacity="{rnd.uniform(.2, .8):.2f}"/>'
    b += '<rect width="1920" height="1080" fill="url(#moonA)"/>'
    # distant Milky Way band behind the berg
    b += '<path d="M700 0 Q1200 250 1920 300 L1920 420 Q1200 380 640 0Z" fill="#9fb6ff" opacity=".07" filter="url(#b24)"/>'
    # sea
    b += f'<rect y="{HY}" width="1920" height="{1080 - HY}" fill="url(#seaA)"/>'
    # ---- underwater ghost bulk (the invisible part) ----
    bulk = [(1080, HY), (990, 610), (930, 690), (900, 790), (930, 880), (1010, 950), (1140, 1000), (1300, 1010), (1440, 975),
            (1560, 905), (1630, 820), (1640, 720), (1600, 640), (1530, 590), (1480, HY)]
    b += f'<path d="{poly(bulk)}" fill="url(#bulkA)"/>'
    b += f'<path d="{poly(bulk)}" fill="none" stroke="#a98cff" stroke-width="18" opacity=".25" filter="url(#b12)"/>'
    b += f'<path d="{poly(bulk)}" fill="none" stroke="#c7b4ff" stroke-width="3" stroke-dasharray="16 16" opacity=".45"/>'
    # dark-matter cosmic web filling the hidden bulk (clipped to it)
    d += f'<clipPath id="bulkClip"><path d="{poly(bulk)}"/></clipPath>'
    nodes = scatter(26, random.Random(12), 900, HY + 20, 1650, 1010, lambda x, y: in_poly(x, y, bulk), gap=75)
    b += f'<g clip-path="url(#bulkClip)"><rect x="880" y="{HY}" width="780" height="460" fill="#05021a" opacity=".45"/>' + \
         cosmic_web(nodes, random.Random(13), glow='#a06bff', core='#e6d8ff', w=1.25, maxd=230) + '</g>'
    # water caustic lines over the bulk
    for k in range(14):
        y = HY + 14 + k * k * 2.6
        b += f'<path d="M0 {y:.0f} Q480 {y + 6:.0f} 960 {y:.0f} T1920 {y:.0f}" stroke="#4f8fd0" stroke-width="2" fill="none" opacity="{.28 - k * .016:.2f}"/>'
    # ---- the visible tip ----
    tip = [(1060, HY), (1110, 470), (1150, 430), (1190, 330), (1230, 300), (1265, 250), (1300, 280), (1335, 230), (1370, 300),
           (1410, 360), (1450, 420), (1475, 500), (1500, HY)]
    b += f'<ellipse cx="1280" cy="420" rx="300" ry="220" fill="#bfe6ff" opacity=".35" filter="url(#b50)"/>'
    b += f'<path d="{poly(tip)}" fill="url(#iceA)" stroke="#0a1838" stroke-width="5" stroke-linejoin="round"/>'
    # shaded right faces
    b += f'<path d="{poly([(1300, 280), (1335, 230), (1370, 300), (1410, 360), (1450, 420), (1475, 500), (1500, HY), (1330, HY), (1310, 420)])}" fill="#4f8fd0" opacity=".45"/>'
    b += f'<path d="{poly([(1150, 430), (1190, 330), (1230, 300), (1200, 420), (1160, HY), (1060, HY), (1110, 470)])}" fill="#ffffff" opacity=".45"/>'
    b += f'<path d="M1110 470 L1150 430 L1190 330 L1230 300 L1265 250" fill="none" stroke="#fff" stroke-width="5" stroke-linecap="round" opacity=".9"/>'
    # stars / galaxy inside the visible tip (ordinary matter)
    b += mini_galaxy(1300, 420, 70, -20, '#fff1b8', rnd=random.Random(3))
    for _ in range(28):
        x, y = rnd.uniform(1130, 1460), rnd.uniform(330, 545)
        b += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{rnd.uniform(1.5, 3.5):.1f}" fill="#ffe9a8" opacity="{rnd.uniform(.5, 1):.2f}"/>'
    b += spark(1220, 360, 20) + spark(1420, 470, 16) + spark(1265, 225, 26) + spark(1180, 505, 12, '#fff')
    # water line glints at the tip
    b += f'<path d="M1030 {HY + 4} Q1280 {HY + 18} 1530 {HY + 4}" stroke="#d6f2ff" stroke-width="5" fill="none" opacity=".8"/>'
    b += f'<ellipse cx="1280" cy="{HY + 30}" rx="260" ry="18" fill="#bfe6ff" opacity=".35" filter="url(#b6)"/>'
    # ---- ship bow (foreground, lower left) ----
    TIP = (800, 720)
    hull = [(-40, 770), (300, 760), TIP, (760, 820), (640, 960), (520, 1080), (-40, 1080)]
    b += f'<path d="{poly(hull)}" fill="url(#hullA)" stroke="#000" stroke-width="4" stroke-linejoin="round"/>'
    # white upper strake + red waterline band
    b += f'<path d="{poly([(-40, 770), (300, 760), TIP, (788, 742), (300, 790), (-40, 802)])}" fill="#e9e4d6" stroke="#000" stroke-width="3"/>'
    for k in range(9):   # rivet rows
        x = 40 + k * 70
        b += f'<circle cx="{x}" cy="{850 - k * 2}" r="3" fill="#3a4050"/><circle cx="{x + 20}" cy="{930 - k * 2}" r="3" fill="#3a4050"/>'
    # deck seen from above-front + railing converging to the tip
    deck = [(-40, 770), (300, 760), TIP, (300, 735), (-40, 728)]
    b += f'<path d="{poly(deck)}" fill="url(#deckA)" stroke="#000" stroke-width="3"/>'
    for k in range(10):
        b += f'<path d="M{-40 + k * 34} {770 - k * .8:.0f} L{TIP[0] - (9 - k) * 4} {TIP[1] + 2}" stroke="#3a2a1c" stroke-width="1.5" opacity=".4"/>'
    rail_y = 60
    for side in [((-40, 728), (300, 735), TIP), ((-40, 770), (300, 760), TIP)]:
        top = [(x, y - rail_y * (1 - max(0, x - 300) / 900)) for x, y in side]
        b += f'<path d="{path(top)}" fill="none" stroke="#f2ead6" stroke-width="5" stroke-linejoin="round"/>'
        for t in range(0, 11):
            u = t / 10; x = -40 + u * (TIP[0] + 40)
            seg = 0 if x < 300 else 1
            p0 = side[seg]; p1 = side[seg + 1]; f = (x - p0[0]) / (p1[0] - p0[0]); y = p0[1] + (p1[1] - p0[1]) * f
            h = rail_y * (1 - max(0, x - 300) / 900)
            b += f'<path d="M{x:.0f} {y:.0f} L{x:.0f} {y - h:.0f}" stroke="#f2ead6" stroke-width="3"/>'
    # bow wave foam
    b += f'<path d="M{TIP[0]} {TIP[1]} L760 820 L640 960 L520 1080" fill="none" stroke="#9fd0ff" stroke-width="5" opacity=".55"/>'
    b += f'<path d="M{TIP[0]} {TIP[1]} L760 820 L640 960 L520 1080" fill="none" stroke="#9fd0ff" stroke-width="18" opacity=".18" filter="url(#b6)"/>'

    # ---- frog at the bow, arms spread (the "flying" pose) ----
    fx, fy = 730, 724
    scarf = ('<path d="M-30 -24 q36 10 70 0 l2 9 q-38 10 -74 0z" fill="#d94a4a" stroke-width="2.6"/>'
             '<path d="M-28 -18 q-26 -4 -46 -20 q4 14 -6 20 q24 10 50 8z" fill="#e2645a" stroke-width="2.6"/>')
    b += frog(fx, fy, 2.4, look=(7, -3), mouth='O',
              armL='M-34 -24 q-26 -6 -50 -24', armR='M38 -24 q30 -6 56 -24', mid=scarf)
    b += '<rect width="1920" height="1080" fill="url(#vigA)"/>'
    lines = [('WE SEE', 168, 'w'), ('ONLY', 168, 'w'), ('5%', 290, 'y')]
    return page('#03061a', svg(d, b), lines, outline='#030616', top=40)


# =============================== B: galaxy held by an invisible halo ===============================
def make_B():
    rnd = random.Random(21)
    GX, GY = 1420, 620
    d = FILTERS
    d += rad('bgB', GX, GY, 1250, [(0, '#3a1a5c', 1), (.45, '#1a0c33', 1), (1, '#07030f', 1)])
    d += rad('coreB', GX, GY, 300, [(0, '#fff6d8', 1), (.15, '#ffd890', .9), (.4, '#ff8fb8', .35), (1, '#7a3cff', 0)])
    d += rad('haloB', GX, GY, 500, [(0, '#6be8ff', 0), (.72, '#6be8ff', .04), (.93, '#7ff0ff', .16), (1, '#7ff0ff', 0)])
    d += rad('vigB', GX, GY, 1250, [(0, '#000', 0), (.6, '#000', 0), (1, '#000', .7)])
    d += lin('beamB', [(0, '#fff6c8'), (1, '#fff6c8')], x2=1, y2=0)
    d += '<linearGradient id="beamFadeB" x1="0" y1="1" x2="1" y2="0"><stop offset="0" stop-color="#fff" stop-opacity=".9"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>'
    d += '<mask id="beamMaskB"><rect width="1920" height="1080" fill="url(#beamFadeB)"/></mask>'
    b = '<rect width="1920" height="1080" fill="url(#bgB)"/>'
    for _ in range(220):
        b += f'<circle cx="{rnd.uniform(0, 1920):.0f}" cy="{rnd.uniform(0, 1080):.0f}" r="{rnd.choice([1.1, 1.6, 2.2])}" fill="#efe6ff" opacity="{rnd.uniform(.15, .7):.2f}"/>'
    for _ in range(12):
        b += f'<ellipse cx="{rnd.uniform(800, 1900):.0f}" cy="{rnd.uniform(40, 1000):.0f}" rx="{rnd.uniform(60, 160):.0f}" ry="{rnd.uniform(30, 80):.0f}" fill="{rnd.choice(["#ff6ad5", "#6b8cff", "#b46bff"])}" opacity="{rnd.uniform(.05, .12):.2f}" filter="url(#b24)"/>'
    # ---- invisible halo: big faint sphere with a shimmering lattice ----
    HR = 410
    b += f'<circle cx="{GX}" cy="{GY}" r="{HR}" fill="url(#haloB)"/>'
    # cosmic web wrapping the galaxy: filaments and knots in the halo, densest in a ring round the disc
    def ring(x, y):
        rr = math.hypot(x - GX, (y - GY) * 1.05)
        return 170 < rr < HR + 40 and not (x < 1080 and y < 500)
    nodes = scatter(34, random.Random(22), GX - HR - 40, GY - HR - 40, GX + HR + 40, min(1030, GY + HR + 40), ring, gap=78)
    b += cosmic_web(nodes, random.Random(23), glow='#5fe0ff', core='#d8fbff', w=1.6, maxd=230, dots=30)
    # ---- the spiral galaxy ----
    TILT = .42; ROT = -18
    g = f'<g transform="translate({GX} {GY}) rotate({ROT}) scale(1 {TILT})">'
    g += '<circle r="420" fill="#8a5cff" opacity=".18" filter="url(#b50)"/>'
    g += '<circle r="260" fill="#ff8fd0" opacity=".2" filter="url(#b24)"/>'
    cols = ['#fff2c8', '#ffd6f0', '#c8d8ff', '#9fe8ff']
    for a in range(2):
        for k in range(520):
            t = k / 520
            ang = a * math.pi + t * 4.6
            rr = 36 + 330 * t
            x = rr * math.cos(ang) + rnd.gauss(0, 10 + 22 * t); y = rr * math.sin(ang) + rnd.gauss(0, 10 + 22 * t)
            g += f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{rnd.uniform(1.2, 3.6) * (1.1 - t * .5):.1f}" fill="{rnd.choice(cols)}" opacity="{rnd.uniform(.45, 1):.2f}"/>'
        # arm glow lane
        pts = [((36 + 330 * t) * math.cos(a * math.pi + t * 4.6), (36 + 330 * t) * math.sin(a * math.pi + t * 4.6)) for t in [i / 40 for i in range(41)]]
        g += f'<path d="{path(pts)}" fill="none" stroke="#ffb8e8" stroke-width="46" opacity=".16" filter="url(#b12)"/>'
        g += f'<path d="{path(pts)}" fill="none" stroke="#e0d0ff" stroke-width="14" opacity=".22" filter="url(#b6)"/>'
    for _ in range(80):   # pink star-forming knots
        t = rnd.random(); a = rnd.randint(0, 1); ang = a * math.pi + t * 4.6; rr = 36 + 330 * t
        g += f'<circle cx="{rr * math.cos(ang):.1f}" cy="{rr * math.sin(ang):.1f}" r="{rnd.uniform(3, 6):.1f}" fill="#ff7ac8" opacity=".7"/>'
    g += '</g>'
    b += g
    b += f'<circle cx="{GX}" cy="{GY}" r="300" fill="url(#coreB)"/>'
    b += f'<ellipse cx="{GX}" cy="{GY}" rx="70" ry="38" transform="rotate({ROT} {GX} {GY})" fill="#fffaf0"/>'
    # ---- fast outer stars with speed trails (they "should fly off") ----
    for ang0, rr in [(200, 455), (330, 440), (30, 450), (120, 430), (260, 445)]:
        a = math.radians(ang0)
        def pt(aa, r=rr):
            x, y = r * math.cos(aa), r * math.sin(aa) * TILT
            c, s = math.cos(math.radians(ROT)), math.sin(math.radians(ROT))
            return GX + x * c - y * s, GY + x * s + y * c
        trail = [pt(a - i * .02) for i in range(0, 16)]
        b += f'<path d="{path(trail)}" fill="none" stroke="#fff2c8" stroke-width="7" stroke-linecap="round" opacity=".55"/>'
        x, y = pt(a)
        b += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="14" fill="#fff2c8" opacity=".5" filter="url(#b6)"/><circle cx="{x:.0f}" cy="{y:.0f}" r="6" fill="#fff"/>'
    b += spark(GX + 380, GY - 330, 26) + spark(GX - 420, GY + 250, 20, '#e8fbff') + spark(GX + 470, GY + 260, 18)
    # ---- frog astronaut with a torch, lower-left, beam into the halo ----
    fx, fy = 560, 960
    bx, by = fx + 2.4 * 70, fy - 2.4 * 66
    beam = f'M{bx:.0f} {by - 6:.0f} L{GX - 380} {GY - 120} L{GX - 250} {GY + 330} L{bx + 8:.0f} {by + 10:.0f}Z'
    b += f'<g mask="url(#beamMaskB)"><path d="{beam}" fill="#fff2b0" opacity=".45" filter="url(#b12)"/><path d="{beam}" fill="#fff6c8" opacity=".2"/></g>'
    torch = ('<g transform="translate(64 -60) rotate(-28)"><rect x="-6" y="-8" width="34" height="16" rx="5" fill="#c9cfdc" stroke-width="3"/>'
             '<path d="M28 -12 L40 -16 L40 16 L28 12Z" fill="#e2b85a" stroke-width="3"/><ellipse cx="40" cy="0" rx="4" ry="15" fill="#fffbe0" stroke="none"/></g>')
    b += f'<ellipse cx="{fx}" cy="{fy + 120}" rx="10" ry="4" fill="#000" opacity="0"/>'
    b += frog(fx, fy, 2.4, rot=-8, look=(9, -5), mouth='O', helmet=True, armR='M38 -22 q22 -10 30 -38', armL='M-34 -22 q-24 -16 -30 -44',
              legs=((-20, -6, -32, 10, -20), (20, -6, 30, 14, 20)), front=torch)
    b += '<rect width="1920" height="1080" fill="url(#vigB)"/>'
    lines = [('WHAT HOLDS', 150, 'w'), ('IT', 150, 'w'), ('TOGETHER?', 160, 'y')]
    return page('#07030f', svg(d, b), lines, outline='#0a0414', top=40)


# =============================== C: the cosmic pie ===============================
def make_C():
    rnd = random.Random(33)
    CX, CY, R, r, H = 1330, 600, 380, 190, 70
    d = FILTERS
    d += rad('bgC', 1300, 450, 1300, [(0, '#2a1640', 1), (.5, '#140a24', 1), (1, '#06030c', 1)])
    d += rad('lampC', 1290, 120, 720, [(0, '#ffd890', .4), (.5, '#ff9a5a', .1), (1, '#ff9a5a', 0)])
    d += rad('plateC', CX, CY + 90, 520, [(0, '#3a3058', 1), (.75, '#2a2244', 1), (1, '#1a1430', 1)])
    d += lin('crustC', [(0, '#ffe7a0'), (.5, '#e9a84e'), (1, '#9a5a22')])
    d += lin('fillC', [(0, '#2a1a5a'), (1, '#120a30')], x2=1, y2=1)
    d += rad('vigC', 1200, 520, 1250, [(0, '#000', 0), (.6, '#000', 0), (1, '#000', .72)])
    b = '<rect width="1920" height="1080" fill="url(#bgC)"/><rect width="1920" height="1080" fill="url(#lampC)"/>'
    for _ in range(160):
        b += f'<circle cx="{rnd.uniform(0, 1920):.0f}" cy="{rnd.uniform(0, 1080):.0f}" r="{rnd.choice([1.1, 1.6, 2.2])}" fill="#ffe8f4" opacity="{rnd.uniform(.12, .6):.2f}"/>'
    b += mini_galaxy(1760, 140, 60, 25, '#d8c8ff', rnd=random.Random(8), op=.6)
    # light cone from above
    b += f'<path d="M1180 0 L1400 0 L1800 760 L780 760Z" fill="#ffe0a8" opacity=".06" filter="url(#b24)"/>'

    def P(a, dy=0, rr=R, ry=r, ox=0, oy=0):
        return (CX + ox + rr * math.cos(a), CY + oy + ry * math.sin(a) + dy)

    def arc(a0, a1, dy=0, n=60, **k):
        return [P(a0 + (a1 - a0) * i / n, dy, **k) for i in range(n + 1)]
    # plate
    b += f'<ellipse cx="{CX}" cy="{CY + H + 50}" rx="560" ry="240" fill="#000" opacity=".5" filter="url(#b24)"/>'
    b += f'<ellipse cx="{CX}" cy="{CY + H + 22}" rx="520" ry="230" fill="#120c22" stroke="#2a2040" stroke-width="5"/>'
    b += f'<ellipse cx="{CX}" cy="{CY + H + 10}" rx="520" ry="230" fill="url(#plateC)" stroke="#b9a6ff" stroke-width="5"/>'
    b += f'<ellipse cx="{CX}" cy="{CY + H + 18}" rx="430" ry="190" fill="none" stroke="#4a3e70" stroke-width="4"/>'
    b += f'<path d="M{CX - 490} {CY + H - 40} A520 230 0 0 1 {CX - 200} {CY + H - 200}" fill="none" stroke="#e0d4ff" stroke-width="6" stroke-linecap="round" opacity=".5"/>'
    deg = math.radians
    G0, G1 = deg(81), deg(99)          # 5 % gap at the front
    D0, D1 = deg(99), deg(196)         # 27 % dark matter (ghost purple)
    E0, E1 = deg(196), deg(441)        # 68 % dark energy (dashed outline only)
    # 68 %: dashed outline + very faint fill
    top68 = [P(0)] + arc(E0, E1) if False else [(CX, CY)] + arc(E0, E1)
    side68 = arc(deg(360), E1) + list(reversed(arc(deg(360), E1, dy=H)))
    b += f'<path d="{poly(top68)}" fill="#7ff0ff" opacity=".10"/>'
    b += f'<path d="{poly(side68)}" fill="#7ff0ff" opacity=".07"/>'
    for _ in range(40):
        a = rnd.uniform(E0 + .05, E1 - .05); f = rnd.uniform(.2, .95)
        b += f'<circle cx="{CX + R * f * math.cos(a):.0f}" cy="{CY + r * f * math.sin(a):.0f}" r="{rnd.uniform(1.5, 3):.1f}" fill="#bff8ff" opacity="{rnd.uniform(.3, .7):.2f}"/>'
    for shape in (top68, side68):
        b += f'<path d="{poly(shape)}" fill="none" stroke="#7ff0ff" stroke-width="16" opacity=".35" filter="url(#b6)"/>'
        b += f'<path d="{poly(shape)}" fill="none" stroke="#bff8ff" stroke-width="4" stroke-dasharray="18 14" stroke-linejoin="round" opacity=".85"/>'
    b += f'<path d="M{P(E1)[0]:.0f} {P(E1)[1]:.0f} L{P(E1, H)[0]:.0f} {P(E1, H)[1]:.0f}" stroke="#bff8ff" stroke-width="4" stroke-dasharray="10 10" opacity=".85"/>'
    # 27 %: translucent purple ghost with a wobble glow
    top27 = [(CX, CY)] + arc(D0, D1)
    side27 = arc(D0, deg(180)) + list(reversed(arc(D0, deg(180), dy=H)))
    wall27 = [(CX, CY), P(D0), P(D0, H), (CX, CY + H)]
    b += f'<path d="{poly(wall27)}" fill="#5b3fb0" opacity=".35" stroke="#c7b4ff" stroke-width="3"/>'
    b += f'<path d="{poly(side27)}" fill="#4a2f9a" opacity=".45"/>'
    b += f'<path d="{poly(top27)}" fill="#8a6cff" opacity=".35"/>'
    b += f'<path d="{poly(top27)}" fill="none" stroke="#c7b4ff" stroke-width="14" opacity=".3" filter="url(#b6)"/>'
    b += f'<path d="{poly(top27)}" fill="none" stroke="#e0d4ff" stroke-width="4" opacity=".85"/>'
    b += f'<path d="{poly(side27)}" fill="none" stroke="#e0d4ff" stroke-width="3" opacity=".6"/>'
    # cosmic-web filaments inside the ghost slice (top face + side)
    d += f'<clipPath id="c27"><path d="{poly(top27)}"/><path d="{poly(side27)}"/></clipPath>'
    shape27 = top27
    nodes = scatter(14, random.Random(34), CX - R, CY - r, CX + 20, CY + r + H, lambda x, y: in_poly(x, y, top27) or in_poly(x, y, side27), gap=55)
    b += '<g clip-path="url(#c27)">' + cosmic_web(nodes, random.Random(35), glow='#c06bff', core='#f4e8ff', w=1.0, maxd=170, k=3) + '</g>'
    # gap wall of the 68 % part (dashed) at the front
    b += f'<path d="{poly([(CX, CY), P(G0), P(G0, H), (CX, CY + H)])}" fill="#7ff0ff" opacity=".05" stroke="#bff8ff" stroke-width="3" stroke-dasharray="12 10"/>'
    # crumbs on the plate where the real slice was
    for _ in range(10):
        b += f'<circle cx="{CX + rnd.uniform(-40, 60):.0f}" cy="{CY + H + rnd.uniform(110, 170):.0f}" r="{rnd.uniform(3, 6):.1f}" fill="#e9a84e" stroke="#7a4214" stroke-width="1.5"/>'

    # ---- the real 5 % slice, on the frog's fork (drawn in its own frame) ----
    def slice_svg(x, y, s, rot):
        a0, a1 = deg(-9), deg(9)
        RR, rr, HH = 300, 200, 60
        def q(a, dy=0):
            return (RR * math.cos(a), rr * math.sin(a) + dy)
        top = [(0, 0)] + [q(a0 + (a1 - a0) * i / 12) for i in range(13)]
        side = [q(a0 + (a1 - a0) * i / 12) for i in range(13)] + [q(a1 - (a1 - a0) * i / 12, HH) for i in range(13)]
        wall = [(0, 0), q(a1), q(a1, HH), (0, HH)]
        o = f'<g transform="translate({x} {y}) rotate({rot}) scale({s})">'
        o += f'<path d="{poly(top)}" fill="#ffe7a0" opacity=".6" filter="url(#b24)"/>'
        o += f'<path d="{poly(wall)}" fill="url(#fillC)" stroke="#3a1c08" stroke-width="4" stroke-linejoin="round"/>'
        # cross-section shows the cosmos: stars & a tiny galaxy in the filling
        for _ in range(16):
            u = rnd.uniform(.15, .95); v = rnd.uniform(.25, .85)
            px, py = q(a1)[0] * u, q(a1)[1] * u + HH * v
            o += f'<circle cx="{px:.1f}" cy="{py:.1f}" r="{rnd.uniform(1.4, 3.2):.1f}" fill="#fff1b8" opacity="{rnd.uniform(.6, 1):.2f}"/>'
        o += mini_galaxy(q(a1)[0] * .62, q(a1)[1] * .62 + HH * .5, 22, -10, '#ffd6f0', n=40, rnd=random.Random(4))
        o += f'<path d="{poly(wall)}" fill="none" stroke="#3a1c08" stroke-width="4" stroke-linejoin="round"/>'
        o += f'<path d="{poly(side)}" fill="url(#crustC)" stroke="#3a1c08" stroke-width="4" stroke-linejoin="round"/>'
        o += f'<path d="{poly(top)}" fill="url(#crustC)" stroke="#3a1c08" stroke-width="4" stroke-linejoin="round"/>'
        for i in range(1, 6):   # lattice top
            p0 = (q(a0)[0] * i / 6, q(a0)[1] * i / 6); p1 = (q(a1)[0] * i / 6, q(a1)[1] * i / 6)
            o += f'<path d="M{p0[0]:.1f} {p0[1]:.1f} L{p1[0]:.1f} {p1[1]:.1f}" stroke="#9a5a22" stroke-width="3" opacity=".7"/>'
        o += f'<path d="M30 -2 L{RR - 20} -6" stroke="#fff6d0" stroke-width="4" stroke-linecap="round" opacity=".8"/>'
        o += '</g>'
        return o
    # frog chef, lower left of the plate, holding a fork with the slice
    fx, fy, fs = 520, 1010, 2.6
    hat = ('<g transform="translate(6 -96)"><path d="M-30 6 L-28 -12 Q-46 -18 -40 -36 Q-30 -52 -12 -44 Q-4 -62 14 -58 Q32 -60 36 -44 Q54 -46 54 -28 Q54 -14 38 -12 L40 6Z" '
           'fill="#fbfbf6" stroke-width="3.2"/><rect x="-31" y="0" width="72" height="10" rx="3" fill="#ecebe0" stroke-width="3"/></g>')
    napkin = '<path d="M-22 -26 L32 -26 L20 -6 L5 4 L-12 -6Z" fill="#f4f0e4" stroke-width="2.6"/><path d="M-22 -26 L32 -26" stroke-width="3"/>'
    fork = ('<g transform="translate(62 -70) rotate(28)"><rect x="-4" y="-6" width="8" height="64" rx="3" fill="#c9cfdc" stroke-width="2.6"/>'
            '<path d="M-12 -6 L-12 -40 M-4 -6 L-4 -42 M4 -6 L4 -42 M12 -6 L12 -40 M-12 -6 Q0 4 12 -6" fill="none" stroke="#c9cfdc" stroke-width="5"/>'
            '<path d="M-12 -6 L-12 -40 M-4 -6 L-4 -42 M4 -6 L4 -42 M12 -6 L12 -40" fill="none" stroke="#1d2b1c" stroke-width="1.2" opacity=".5"/></g>')
    b += f'<ellipse cx="{fx + 10}" cy="{fy + 10}" rx="130" ry="18" fill="#000" opacity=".45" filter="url(#b3)"/>'
    b += frog(fx, fy, fs, look=(9, -6), mouth='O', armR='M38 -24 q22 -8 30 -40', armL='M-34 -22 q-18 0 -22 22',
              hat=hat, mid=napkin, front=fork)
    # slice skewered on the fork, glowing (the only visible part)
    sx, sy = fx + fs * 88, fy - fs * 128
    b += f'<circle cx="{sx + 120}" cy="{sy - 20}" r="150" fill="#ffd890" opacity=".35" filter="url(#b50)"/>'
    b += slice_svg(sx, sy, 1.25, -14)
    b += spark(sx + 260, sy - 130, 26) + spark(sx + 40, sy - 110, 16) + spark(CX + 470, CY - 220, 22, '#e8fbff') + spark(CX - 230, CY - 260, 18, '#e0d4ff')
    b += '<rect width="1920" height="1080" fill="url(#vigC)"/>'
    lines = [('68%', 300, 'y'), ('UNKNOWN', 170, 'w')]
    return page('#06030c', svg(d, b), lines, outline='#07030c', top=36)


if __name__ == '__main__':
    which = sys.argv[1:] or ['A', 'B', 'C']
    for n in which:
        open(os.path.join(HERE, f'{n}.html'), 'w').write(globals()[f'make_{n}']())
    print('ok')
