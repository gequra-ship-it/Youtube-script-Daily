# Thumbnails A-C for kola-superdeep-borehole (guideline 16-6 / 16-8, brief tools/briefs/thumb_art.md).
# Run: python3 videos/kola-superdeep-borehole/thumb/make.py
# A  EXPECTED 100°C / GOT / 180°C  (number contrast)  homage (book illustration): Alice falling down the rabbit hole -> the frog in a hard
#    hat falls down an endless rock shaft that glows hotter toward the bottom, a pocket watch, jar, book and a drill bit float beside it.
#    Script: "temperature at twelve kilometers would reach roughly one hundred degrees Celsius. Instead, the rock soared to ... one hundred
#    eighty degrees Celsius".
# B  WELDED / SHUT  (declarative)  intuitive: a small rusted steel cap on the snowy Arctic tundra (ruins, aurora) with a cut-away below it:
#    rock layers, the glowing shaft, water in cracks, gas bubbles, orange heat at the bottom. Parka frog shining a flashlight on the cap.
#    Script: "heavy steel plate bolted to the ground ... roughly twenty-three centimeters in diameter, is welded shut"; "Arctic tundra";
#    "crumbling concrete foundations and rusted iron scrap"; hydrogen foaming, water in cracks.
# C  PLANKTON / IN THE ROCK?  (question)  intuitive: a long drill core on a lab bench; a big magnifying glass shows glowing microfossils
#    (plankton) inside the crystalline rock; lab-coat frog on the core looking through the lens.
#    Script: "rock cores ... fossilized remains of twenty-four distinct species of microscopic single-celled marine plankton ... encased in
#    crystalline metamorphic rock".
import os, sys, math, random
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', '..', 'tools'))
from thumb_lib import page, svg, lin, rad, spark

INK = '#1d2b1c'; GREEN = '#6aa55a'; DARKG = '#4d8a4a'; BELLY = '#9cc98a'
FILTERS = ''.join(f'<filter id="b{n}" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="{n}"/></filter>' for n in (2, 4, 8, 14, 26, 50, 90))


def P(pts):
    return ' '.join(f'{a:.1f},{b:.1f}' for a, b in pts)


def limb(d, w=7.5, wi=3.4, col=GREEN):
    return f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="{w}"/><path d="{d}" fill="none" stroke="{col}" stroke-width="{wi}"/>'


def end_of(d):
    n = [float(v) for v in d.replace('M', ' ').replace('q', ' ').split()]
    return n[0] + n[-2], n[1] + n[-1]


def frog(x, y, s, rot=0, flip=False, look=(0, 0), mouth='O', armL=None, armR=None, brows=True, back='', front='', mid='', top='', sleeve=GREEN):
    sx = -s if flip else s
    g = [f'<g transform="translate({x} {y}) rotate({rot}) scale({sx} {s})" stroke="{INK}" stroke-linejoin="round" stroke-linecap="round">', back]
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
        g.append(limb(a, col=sleeve)); ex_, ey_ = end_of(a)
        g.append(f'<circle cx="{ex_:.1f}" cy="{ey_:.1f}" r="5.6" fill="{GREEN}" stroke-width="3"/>')
    g.append(front); g.append('</g>')
    return ''.join(g)


def jag(p0, p1, n, amp, seed):
    """jagged polyline from p0 to p1 (n segments, perpendicular noise amp)"""
    r = random.Random(seed); pts = [p0]
    dx, dy = p1[0] - p0[0], p1[1] - p0[1]; L = math.hypot(dx, dy); nx, ny = -dy / L, dx / L
    for i in range(1, n):
        t = i / n; a = r.uniform(-amp, amp) * math.sin(math.pi * t) ** .5
        pts.append((p0[0] + dx * t + nx * a, p0[1] + dy * t + ny * a))
    return pts + [p1]


def sparkles(lst, col='#fff6d6'):
    return ''.join(spark(x, y, s, col) for x, y, s in lst)


def hx(c):
    c = c.lstrip('#'); return tuple(int(c[i:i + 2], 16) for i in (0, 2, 4))


def mix(cols, t):
    """colour along a list of hex stops, t in 0..1"""
    t = max(0, min(1, t)) * (len(cols) - 1); i = min(int(t), len(cols) - 2); f = t - i
    a, b = hx(cols[i]), hx(cols[i + 1])
    return '#%02x%02x%02x' % tuple(round(a[k] + (b[k] - a[k]) * f) for k in range(3))


def lina(id, stops, x2=0, y2=1):
    return f'<linearGradient id="{id}" x1="0" y1="0" x2="{x2}" y2="{y2}">' + ''.join(f'<stop offset="{o}" stop-color="{c}" stop-opacity="{a}"/>' for o, c, a in stops) + '</linearGradient>'


# shared frog outfit: a yellow hard hat with a headlamp (dome above the brows, brim at y -94)
def hardhat(lamp=True):
    h = ('<path d="M-36 -94 q2 -42 42 -44 q40 2 42 44z" fill="#f2b632" stroke-width="3.6"/>'
         '<path d="M-14 -133 q20 -8 40 0 l-4 39 h-32z" fill="#ffd25a" stroke="none" opacity=".75"/>'
         '<path d="M2 -138 v42" fill="none" stroke-width="3"/>'
         '<rect x="-46" y="-98" width="104" height="11" rx="5.5" fill="#e0a020" stroke-width="3.4"/>'
         '<path d="M-26 -124 q8 -10 18 -12" fill="none" stroke="#fff3c0" stroke-width="3.4" opacity=".9"/>')
    if lamp:
        h += '<rect x="-6" y="-124" width="22" height="16" rx="5" fill="#5a5f6e" stroke-width="3"/><circle cx="5" cy="-116" r="5.5" fill="#fff8d8" stroke-width="2"/>'
    return h


# ====================================================================== A  (Alice down the rabbit hole homage)
def watch(x, y, s, rot):
    g = f'<g transform="translate({x} {y}) rotate({rot}) scale({s})" stroke="#2a1606" stroke-linejoin="round">'
    g += '<path d="M0 -62 q-30 -40 10 -64 q34 -14 52 20" fill="none" stroke="#c99a3a" stroke-width="5" stroke-dasharray="7 4"/>'
    g += '<rect x="-9" y="-66" width="18" height="14" rx="4" fill="#d9a843" stroke-width="3"/>'
    g += '<circle r="56" fill="#d9a843" stroke-width="4"/><circle r="46" fill="#fff7e2" stroke-width="3"/>'
    for k in range(12):
        a = k * math.pi / 6
        g += f'<line x1="{38 * math.sin(a):.1f}" y1="{-38 * math.cos(a):.1f}" x2="{43 * math.sin(a):.1f}" y2="{-43 * math.cos(a):.1f}" stroke-width="{3.5 if k % 3 == 0 else 2}"/>'
    g += '<line x1="0" y1="0" x2="0" y2="-30" stroke-width="4" stroke-linecap="round"/><line x1="0" y1="0" x2="22" y2="8" stroke-width="4" stroke-linecap="round"/><circle r="4" fill="#2a1606"/>'
    g += '<path d="M-40 30 a56 56 0 0 0 80 0" fill="none" stroke="#ff9a3c" stroke-width="7" opacity=".9"/>'
    g += '<path d="M-30 -30 a40 40 0 0 1 22 -12" fill="none" stroke="#fff" stroke-width="5" opacity=".8"/>'
    return g + '</g>'


def jar(x, y, s, rot):
    g = f'<g transform="translate({x} {y}) rotate({rot}) scale({s})" stroke="#2a1606" stroke-linejoin="round">'
    g += '<path d="M-38 -50 q-6 50 0 96 q38 10 76 0 q6 -46 0 -96z" fill="#e8742a" fill-opacity=".85" stroke-width="4"/>'
    g += '<rect x="-34" y="-12" width="68" height="30" rx="4" fill="#f6e7c6" stroke-width="3"/>'
    g += '<path d="M-22 -2 h44 M-16 8 h32" stroke="#b5835a" stroke-width="3"/>'
    g += '<rect x="-42" y="-66" width="84" height="18" rx="5" fill="#f2f0e8" stroke-width="3.4"/><path d="M-42 -60 q42 -18 84 0" fill="none" stroke="#c0392b" stroke-width="3"/>'
    g += '<path d="M-28 -40 q-4 30 0 70" fill="none" stroke="#fff" stroke-width="6" opacity=".55"/>'
    g += '<path d="M-36 44 q36 10 72 0" fill="none" stroke="#ffcf6a" stroke-width="7" opacity=".9"/>'
    return g + '</g>'


def book(x, y, s, rot):
    g = f'<g transform="translate({x} {y}) rotate({rot}) scale({s})" stroke="#2a1606" stroke-linejoin="round">'
    g += '<path d="M0 10 q-40 -22 -86 -10 l-6 -54 q48 -14 92 10 q44 -24 92 -10 l-6 54 q-46 -12 -86 10z" fill="#7a2d3a" stroke-width="4"/>'
    g += '<path d="M0 0 q-38 -22 -80 -12 l-4 -48 q44 -12 84 10z" fill="#fbf2dc" stroke-width="3"/>'
    g += '<path d="M0 0 q38 -22 80 -12 l4 -48 q-44 -12 -84 10z" fill="#f3e6c8" stroke-width="3"/>'
    for k in range(4):
        g += f'<path d="M-68 {-44 + k * 10} q30 -8 58 4 M12 {-40 + k * 10} q30 -12 58 -4" fill="none" stroke="#b09a78" stroke-width="2.2"/>'
    g += '<path d="M0 -50 q22 -36 58 -40 l2 30 q-36 2 -60 10z" fill="#fffaf0" stroke-width="2.6" opacity=".95"/>'
    g += '<path d="M-86 6 q44 -10 86 8 q44 -18 86 -6" fill="none" stroke="#ff9a3c" stroke-width="6" opacity=".9"/>'
    return g + '</g>'


def drillbit(x, y, s, rot):
    """tricone rock bit: threaded pin on top, body, three toothed cones below"""
    g = f'<g transform="translate({x} {y}) rotate({rot}) scale({s})" stroke="#1a1410" stroke-linejoin="round">'
    g += '<path d="M-20 -110 h40 l6 46 h-52z" fill="#8a8f9c" stroke-width="3.4"/>'
    for k in range(5):
        g += f'<path d="M-22 {-104 + k * 9} h44" stroke="#4a4f5a" stroke-width="2.4"/>'
    g += '<path d="M-48 -66 h96 l10 46 q-58 22 -116 0z" fill="#6c7280" stroke-width="3.6"/>'
    g += '<path d="M-40 -60 l-6 36" stroke="#c9cfdb" stroke-width="5" opacity=".7"/>'
    for cx, cy, r in ((-34, 2, 30), (34, 2, 30), (0, 18, 32)):
        g += f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="#9aa0ac" stroke-width="3.4"/>'
        for k in range(7):
            a = k * 2 * math.pi / 7 + .3
            tx, ty = cx + r * .92 * math.cos(a), cy + r * .92 * math.sin(a)
            g += f'<circle cx="{tx:.1f}" cy="{ty:.1f}" r="5.5" fill="#d8dce4" stroke-width="2"/>'
    g += '<path d="M-60 26 q60 40 120 0" fill="none" stroke="#ff9a3c" stroke-width="8" opacity=".95"/>'
    return g + '</g>'


def thumb_A():
    r = random.Random(3)
    defs = FILTERS
    vp = (1250, 790)
    defs += rad('coreA', vp[0], vp[1], 420, [(0, '#ffffff', 1), (.08, '#fff2c0', 1), (.25, '#ffb347', .75), (.6, '#ff6a1e', .25), (1, '#ff6a1e', 0)])
    defs += rad('vigA', 960, 540, 1150, [(0, '#000', 0), (.65, '#000', 0), (1, '#000', .6)])
    b = '<rect width="1920" height="1080" fill="#0b0710"/>'
    # ---- the endless shaft: rings shrinking toward the glowing bottom ----
    c0 = (760, 330); R0 = 1650; N = 30
    heatcols = ['#100b16', '#1d1420', '#33202a', '#5a2a24', '#9a3d1e', '#e2671f', '#ffae4a', '#ffe7a8']
    rings = []
    for i in range(N):
        s = .865 ** i
        cx, cy = vp[0] + (c0[0] - vp[0]) * s, vp[1] + (c0[1] - vp[1]) * s
        rings.append((cx, cy, R0 * s, R0 * s * .72, s))
    for i, (cx, cy, rx, ry, s) in enumerate(rings):
        heat = (1 - s) ** 2.6
        col = mix(heatcols, heat)
        if i % 2: col = mix([col, '#000000'], .14)
        b += f'<ellipse cx="{cx:.1f}" cy="{cy:.1f}" rx="{rx:.1f}" ry="{ry:.1f}" fill="{col}"/>'
        # rock chunks along the band (lit on the side facing the glow)
        nch = max(4, int(26 * s ** .5))
        for _ in range(nch):
            a = r.uniform(0, 2 * math.pi); rr = r.uniform(.9, .97)
            px, py = cx + rx * rr * math.cos(a), cy + ry * rr * math.sin(a)
            w = r.uniform(18, 60) * s ** .8 + 2
            b += f'<ellipse cx="{px:.1f}" cy="{py:.1f}" rx="{w:.1f}" ry="{w * .45:.1f}" transform="rotate({math.degrees(a) + 90:.0f} {px:.1f} {py:.1f})" fill="{mix([col, "#000000"], .35)}"/>'
            if r.random() < .5:
                b += f'<ellipse cx="{px - math.cos(a) * w * .25:.1f}" cy="{py - math.sin(a) * w * .25:.1f}" rx="{w * .7:.1f}" ry="{w * .18:.1f}" transform="rotate({math.degrees(a) + 90:.0f} {px:.1f} {py:.1f})" fill="{mix([col, "#ffd08a"], .25 + .4 * heat)}" opacity=".7"/>'
        # rim light on the inner edge of each ring (the glow comes from deeper down)
        b += f'<ellipse cx="{cx:.1f}" cy="{cy:.1f}" rx="{rx:.1f}" ry="{ry:.1f}" fill="none" stroke="{mix(heatcols, min(1, heat + .25))}" stroke-width="{1 + 5 * s ** .5:.1f}" opacity=".55"/>'
    # cracks running down the walls toward the bottom
    for k in range(16):
        a = k * 2 * math.pi / 16 + r.uniform(-.1, .1)
        pts = []
        for j in range(3, 18):
            cx, cy, rx, ry, s = rings[j]
            aa = a + r.uniform(-.05, .05)
            pts.append((cx + rx * math.cos(aa), cy + ry * math.sin(aa)))
        b += f'<polyline points="{P(pts)}" fill="none" stroke="#000" stroke-width="3" opacity=".35"/>'
        b += f'<polyline points="{P([(x + 2, y + 2) for x, y in pts])}" fill="none" stroke="#ff9a4a" stroke-width="1.5" opacity=".25"/>'
    # hot glow at the bottom
    b += f'<circle cx="{vp[0]}" cy="{vp[1]}" r="430" fill="url(#coreA)"/>'
    b += f'<circle cx="{vp[0]}" cy="{vp[1]}" r="60" fill="#fffbe8" filter="url(#b14)"/>'
    # embers / heat sparks rising
    for _ in range(90):
        a = r.uniform(0, 2 * math.pi); d = r.uniform(80, 900)
        x, y = vp[0] + d * math.cos(a) * 1.1, vp[1] + d * math.sin(a) * .8
        if x < 1000 and y < 520: continue
        rr = r.choice([1.6, 2.4, 3.4]) * (1 + d / 900)
        b += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{rr * 3:.1f}" fill="#ff8a2a" opacity=".22" filter="url(#b4)"/><circle cx="{x:.0f}" cy="{y:.0f}" r="{rr:.1f}" fill="#ffd38a" opacity="{r.uniform(.5, .95):.2f}"/>'
    # ---- floating things (as in Alice's fall), lit orange from below ----
    b += watch(1730, 250, 1.3, 24)
    b += jar(660, 770, 1.25, -28)
    b += book(1740, 700, 1.25, 18)
    b += drillbit(300, 870, 1.2, -30)
    # small falling pebbles
    for x, y, s in ((1100, 330, 9), (980, 610, 7), (1560, 860, 8), (900, 980, 6), (1880, 430, 7)):
        b += f'<path d="M{x} {y} l{s} {-s * .6:.1f} l{s * .8:.1f} {s:.1f} l{-s * .6:.1f} {s * .9:.1f} l{-s * 1.2:.1f} {-s * .3:.1f}z" fill="#3a2a2a" stroke="#ff9a3c" stroke-width="1.5"/>'
    # ---- frog falling, arms up, hard hat lifting off ----
    for k, (x, y, L) in enumerate(((1330, 230, 120), (1390, 200, 160), (1500, 210, 140), (1570, 240, 110))):
        b += f'<path d="M{x} {y} v{-L}" stroke="#fff3d6" stroke-width="5" stroke-linecap="round" opacity=".45"/>'
    hat = f'<g transform="translate(-2 -16) rotate(-12)">{hardhat()}</g>'
    vest = ('<path d="M-30 -4 q-6 -26 0 -40 l18 0 l4 44z M36 -4 q6 -26 0 -40 l-18 0 l-4 44z" fill="#ff7a1a" stroke-width="3"/>'
            '<path d="M-31 -18 h20 M35 -18 h-20" stroke="#e8f0f0" stroke-width="5"/>')
    under = '<path d="M-34 2 q36 12 76 -6" fill="none" stroke="#ff9a3c" stroke-width="5" opacity=".9"/>'
    b += frog(1450, 600, 2.75, rot=-10, look=(-2, 5), mouth='O', mid=vest, top=hat, front=under,
              armL='M-34 -26 q-24 -18 -22 -58', armR='M38 -26 q24 -18 22 -58')
    b += sparkles([(1640, 380, 18), (1180, 230, 14), (520, 620, 14), (1000, 860, 16)], '#fff1c8')
    b += '<rect width="1920" height="1080" fill="url(#vigA)"/>'
    lines = [('EXPECTED 100°C', 98, 'w'), ('GOT', 118, 'w'), ('180°C', 236, 'y')]
    return page('#0b0710', svg(defs, b), lines, outline='#14060a')


# ====================================================================== B  (welded cap + cut-away)
def thumb_B():
    r = random.Random(7)
    G = 500           # snow surface line
    SX = 1220         # shaft x
    defs = FILTERS
    defs += lin('skyB', [(0, '#040a1e'), (.55, '#0d2448'), (1, '#24476e')])
    defs += lina('aur', [(0, '#5cf2b0', 0), (.5, '#5cf2b0', .55), (1, '#2fb6a0', 0)])
    defs += rad('aurG', 1300, 120, 700, [(0, '#7dffc8', .35), (1, '#7dffc8', 0)])
    defs += lin('snowB', [(0, '#f3f8ff'), (1, '#b9cbe2')])
    defs += lin('shaftB', [(0, '#bfe6ff'), (.45, '#ffd98a'), (.8, '#ff8a2a'), (1, '#fff3c0')])
    defs += rad('heatB', SX, 1110, 520, [(0, '#fff3c8', .95), (.18, '#ffb347', .8), (.5, '#ff5a1e', .35), (1, '#ff5a1e', 0)])
    defs += rad('capG', SX, G - 10, 300, [(0, '#ffe6a8', .55), (1, '#ffe6a8', 0)])
    defs += rad('vigB', 960, 540, 1150, [(0, '#000', 0), (.7, '#000', 0), (1, '#000', .55)])
    defs += lin('rust', [(0, '#c9693a'), (.5, '#8a3c22'), (1, '#4e2216')], x2=1, y2=0)
    b = '<rect width="1920" height="1080" fill="url(#skyB)"/>'
    b += ''.join(f'<circle cx="{r.randint(0, 1920)}" cy="{r.randint(0, 430)}" r="{r.choice([1.2, 1.8, 2.4])}" fill="#e8f4ff" opacity="{r.uniform(.25, .8):.2f}"/>' for _ in range(140))
    # aurora curtains
    b += '<rect width="1920" height="600" fill="url(#aurG)"/>'
    for k, (x0, amp, op) in enumerate(((700, 70, .5), (980, 90, .65), (1260, 60, .55), (1500, 80, .45))):
        d = f'M{x0} 60 C {x0 + 200} {60 + amp}, {x0 + 300} {-20}, {x0 + 520} 70 L {x0 + 520} 340 C {x0 + 300} 250, {x0 + 200} {330 + amp}, {x0} 300 Z'
        b += f'<path d="{d}" fill="url(#aur)" opacity="{op}" filter="url(#b14)"/>'
        for j in range(16):
            xx = x0 + 30 + j * 30
            b += f'<path d="M{xx} {90 + 30 * math.sin(j * .7 + k)} v{170 + 40 * math.sin(j * 1.3)}" stroke="#a8ffd8" stroke-width="3" opacity="{op * .35:.2f}" filter="url(#b2)"/>'
    # distant tundra hills + ruined rig silhouettes
    b += f'<path d="M0 {G - 50} Q 300 {G - 90} 600 {G - 60} T 1200 {G - 70} T 1920 {G - 55} V {G} H 0z" fill="#3d5a7e"/>'
    b += f'<path d="M0 {G - 30} Q 400 {G - 55} 800 {G - 34} T 1920 {G - 38} V {G} H 0z" fill="#8aa6c8"/>'
    # abandoned concrete block + broken derrick far right-back
    b += f'<path d="M1560 {G - 40} v-120 l40 -10 v20 l50 -6 v-30 l70 10 v136z" fill="#2a3a52"/>'
    for k in range(4):
        b += f'<rect x="{1580 + k * 34}" y="{G - 140}" width="14" height="22" fill="#141e30"/>'
    b += f'<path d="M1460 {G - 40} l30 -190 l30 190 M1470 {G - 100} h40 M1480 {G - 160} h20 M1470 {G - 100} l34 -56 M1510 {G - 100} l-34 -56" fill="none" stroke="#22324a" stroke-width="7"/>'
    b += f'<path d="M1490 {G - 230} l24 24" stroke="#22324a" stroke-width="7"/>'
    # ---- ground cross-section (cut-away) below the snow ----
    layers = [('#e9f1fb', 26), ('#5f6f86', 40), ('#46506a', 70), ('#3a3f58', 80), ('#463a4c', 80), ('#5a3a3e', 80), ('#7a3c2e', 90), ('#9a4426', 200)]
    y = G
    for k, (col, h) in enumerate(layers):
        top = jag((-20, y), (1940, y), 24, 6 if k else 2, 30 + k)
        bot = jag((1940, y + h + 40), (-20, y + h + 40), 24, 10, 60 + k)
        b += f'<polygon points="{P(top + bot)}" fill="{col}"/>'
        if k >= 2:  # bright upper edge = layer boundary
            b += f'<polyline points="{P(top)}" fill="none" stroke="{mix([col, "#ffffff"], .25)}" stroke-width="3" opacity=".6"/>'
        y += h
    # crystalline texture in the rock layers
    for _ in range(420):
        x = r.uniform(0, 1920); yy = r.uniform(G + 70, 1080)
        if abs(x - SX) < 40: continue
        s = r.uniform(4, 13); c = mix(['#9aa4c0', '#e0a070', '#ffd090'], (yy - G) / 600)
        b += f'<path d="M{x:.0f} {yy:.0f} l{s:.1f} {-s * .5:.1f} l{s * .5:.1f} {s:.1f} l{-s:.1f} {s * .3:.1f}z" fill="{c}" opacity="{r.uniform(.12, .35):.2f}"/>'
    # water veins in cracks (blue) crossing the rock near the shaft
    for k, (yy, x0, x1) in enumerate(((700, 820, 1620), (820, 760, 1700))):
        pts = jag((x0, yy), (x1, yy + 30), 16, 22, 90 + k)
        b += f'<polyline points="{P(pts)}" fill="none" stroke="#0a0c18" stroke-width="7"/>'
        b += f'<polyline points="{P(pts)}" fill="none" stroke="#5fd0ff" stroke-width="3" opacity=".9"/>'
        b += f'<polyline points="{P(pts)}" fill="none" stroke="#5fd0ff" stroke-width="12" opacity=".25" filter="url(#b4)"/>'
    # the lower crust glow
    b += '<rect x="0" y="560" width="1920" height="520" fill="url(#heatB)"/>'
    # cut edge highlight along the surface
    b += f'<path d="M0 {G + 2} H1920" stroke="#ffffff" stroke-width="3" opacity=".7"/>'
    # ---- the glowing shaft ----
    b += f'<rect x="{SX - 34}" y="{G}" width="68" height="600" fill="#ffcf7a" opacity=".35" filter="url(#b26)"/>'
    b += f'<rect x="{SX - 15}" y="{G}" width="30" height="600" fill="#0b0d16"/>'
    b += f'<rect x="{SX - 9}" y="{G + 6}" width="18" height="600" fill="url(#shaftB)"/>'
    b += f'<rect x="{SX - 3}" y="{G + 6}" width="6" height="600" fill="#fffbe8" opacity=".75"/>'
    # gas bubbles foaming up the shaft
    for k in range(18):
        yy = G + 60 + k * 28 + r.uniform(-8, 8); xx = SX + r.uniform(-8, 8); s = r.uniform(3, 7)
        b += f'<circle cx="{xx:.0f}" cy="{yy:.0f}" r="{s:.1f}" fill="none" stroke="#ffffff" stroke-width="2" opacity=".8"/>'
    for k in range(10):
        yy = G + 120 + k * 50; side = 1 if k % 2 else -1
        b += f'<circle cx="{SX + side * r.uniform(30, 70):.0f}" cy="{yy:.0f}" r="{r.uniform(5, 10):.1f}" fill="none" stroke="#dff6ff" stroke-width="2.4" opacity=".6"/>'
    # tiny plankton fossils in a mid layer
    for x, yy in ((980, 760), (1480, 740), (1050, 640), (1400, 660)):
        b += f'<g transform="translate({x} {yy})" opacity=".85"><circle r="10" fill="none" stroke="#f2d27a" stroke-width="2.5"/>' + ''.join(f'<path d="M{10 * math.cos(a):.1f} {10 * math.sin(a):.1f} L{17 * math.cos(a):.1f} {17 * math.sin(a):.1f}" stroke="#f2d27a" stroke-width="2"/>' for a in [j * math.pi / 4 for j in range(8)]) + '</g>'
    # ---- snow surface (front) with drifts ----
    drift = jag((-20, G + 4), (1940, G + 4), 30, 4, 5)
    b += f'<path d="M-20 {G - 18} Q 300 {G - 34} 620 {G - 16} T 1240 {G - 20} T 1940 {G - 16} V {G + 10} H -20z" fill="url(#snowB)"/>'
    # concrete slabs + rebar near the cap
    b += f'<path d="M820 {G - 14} l40 -50 l170 -14 l26 58z" fill="#7c8597" stroke="#2a3040" stroke-width="3"/><path d="M860 {G - 64} l170 -14" stroke="#e8f0ff" stroke-width="10" opacity=".9"/>'
    b += f'<path d="M1500 {G - 16} l20 -36 l120 4 l14 32z" fill="#6c7587" stroke="#2a3040" stroke-width="3"/><path d="M1520 {G - 52} l120 4" stroke="#e8f0ff" stroke-width="8"/>'
    for d in (f'M900 {G - 70} q-10 -60 30 -80 q30 -10 20 -50', f'M960 {G - 74} q20 -50 -10 -90', f'M1580 {G - 50} q30 -40 0 -70 q-20 -20 10 -40'):
        b += f'<path d="{d}" fill="none" stroke="#2a1a14" stroke-width="9" stroke-linecap="round"/><path d="{d}" fill="none" stroke="#a8502a" stroke-width="4" stroke-linecap="round"/>'
    # ---- the welded steel cap (rusted disc with bolts) ----
    b += f'<ellipse cx="{SX}" cy="{G - 10}" rx="300" ry="120" fill="url(#capG)"/>'
    cx, cy, RX, RY, TH = SX, G - 28, 170, 50, 24
    b += f'<ellipse cx="{cx}" cy="{cy + TH + 6}" rx="{RX + 30}" ry="{RY + 12}" fill="#000" opacity=".35" filter="url(#b8)"/>'
    b += f'<path d="M{cx - RX} {cy} v{TH} a{RX} {RY} 0 0 0 {2 * RX} 0 v{-TH}z" fill="#5a2a18" stroke="#1a0c08" stroke-width="4"/>'
    b += f'<ellipse cx="{cx}" cy="{cy}" rx="{RX}" ry="{RY}" fill="url(#rust)" stroke="#1a0c08" stroke-width="4"/>'
    b += f'<ellipse cx="{cx}" cy="{cy}" rx="{RX - 22}" ry="{RY - 7}" fill="none" stroke="#3a180e" stroke-width="3"/>'
    b += f'<ellipse cx="{cx}" cy="{cy}" rx="{RX - 26}" ry="{RY - 9}" fill="none" stroke="#e8a070" stroke-width="2" opacity=".6" stroke-dasharray="6 5"/>'
    for k in range(12):
        a = k * math.pi / 6
        bx, by = cx + (RX - 11) * math.cos(a), cy + (RY - 4) * math.sin(a)
        b += f'<ellipse cx="{bx:.1f}" cy="{by:.1f}" rx="7" ry="4.5" fill="#9a5a3a" stroke="#1a0c08" stroke-width="2.4"/><ellipse cx="{bx - 1.5:.1f}" cy="{by - 1.5:.1f}" rx="2.5" ry="1.5" fill="#ffd0a0"/>'
    # rust streaks + snow patch + rim light
    for k in range(6):
        x = cx - 120 + k * 46
        b += f'<path d="M{x} {cy + 8} q4 10 0 {16 + k % 3 * 6}" stroke="#3a180e" stroke-width="3" opacity=".6"/>'
    b += f'<path d="M{cx - 120} {cy - 10} q50 -30 110 -28 q-10 18 -50 26 q-30 6 -60 2z" fill="#f3f8ff"/>'
    b += f'<path d="M{cx - RX + 10} {cy - 14} a{RX} {RY} 0 0 1 {RX * 1.3:.0f} {-RY + 6}" fill="none" stroke="#ffe0b0" stroke-width="4" opacity=".85"/>'
    # ---- frog in a parka, kneeling, shining a flashlight onto the cap ----
    FX, FY, FS = 1660, G - 6, 3.2
    hood = ('<path d="M-44 -78 q-6 30 2 46 q12 2 14 -8 l-2 -40z M56 -78 q6 30 -2 46 q-12 2 -14 -8 l2 -40z" fill="#8a5a3a" stroke-width="3.2"/>'
            '<path d="M-42 -66 q0 16 4 26 M54 -66 q0 16 -4 26" fill="none" stroke="#c49a74" stroke-width="3"/>')
    ushanka = ('<path d="M-32 -96 q4 -38 38 -40 q34 2 38 40z" fill="#8a5a3a" stroke-width="3.6"/>'
               '<rect x="-44" y="-104" width="100" height="22" rx="11" fill="#c49a74" stroke-width="3.4"/>'
               '<path d="M-36 -98 q8 -4 14 0 M-12 -98 q8 -4 14 0 M12 -98 q8 -4 14 0 M36 -98 q8 -4 14 0" fill="none" stroke="#e9d2b4" stroke-width="2.6"/>'
               '<circle cx="6" cy="-120" r="6" fill="#f2d27a" stroke-width="2.4"/>')
    parka = ('<path d="M-38 2 q-6 -22 2 -30 q40 -8 78 0 q10 10 2 30 q-42 10 -82 0z" fill="#d2452e" stroke-width="3.6"/>'
             '<path d="M-34 -26 q40 -10 78 0" fill="none" stroke="#f4ece0" stroke-width="7"/>'
             '<path d="M4 -24 v24" stroke-width="2.6"/><circle cx="-2" cy="-14" r="2.4" fill="{INK}" stroke="none"/>'
             '<path d="M-32 -6 q36 8 72 0" fill="none" stroke="#f4ece0" stroke-width="5"/>').replace('{INK}', INK)
    # flashlight in the frog's left hand (viewer's left), pointing down-left at the cap; the beam starts at the lens
    TR = -15; HX, HY = -54, -26
    torch = (f'<g transform="translate({HX} {HY}) rotate({TR})"><rect x="-30" y="-8" width="34" height="16" rx="4" fill="#3a3f4c" stroke-width="3"/>'
             '<rect x="-40" y="-11" width="12" height="22" rx="3" fill="#596070" stroke-width="3"/><ellipse cx="-40" cy="0" rx="3" ry="9" fill="#fffbe0" stroke="none"/></g>')
    t = math.radians(TR); lx_, ly_ = HX + -40 * math.cos(t), HY + -40 * math.sin(t)
    LXs, LYs = FX + FS * lx_, FY + FS * ly_
    b += f'<path d="M{LXs:.0f} {LYs - 8:.0f} L{cx - 110} {cy - 40} L{cx + 60} {cy + 34} L{LXs:.0f} {LYs + 8:.0f}z" fill="#fff6c8" opacity=".32" filter="url(#b8)"/>'
    b += f'<ellipse cx="{cx - 20}" cy="{cy}" rx="110" ry="34" fill="#fff6c8" opacity=".22" filter="url(#b8)"/>'
    b += f'<ellipse cx="{FX}" cy="{FY + 8}" rx="90" ry="12" fill="#000" opacity=".25"/>'
    b += frog(FX, FY, FS, look=(-5, 4), mouth='O', back=hood, mid=parka, top=ushanka, sleeve='#d2452e',
              armL=f'M-34 -24 q-14 -4 {HX + 34} {HY + 24}', armR='M38 -24 q12 8 10 24', front=torch)
    b += sparkles([(cx - 30, cy - 95, 18), (cx - 190, cy - 40, 14), (1880, 110, 16), (560, 470, 12)], '#fff6d6')
    b += '<rect width="1920" height="1080" fill="url(#vigB)"/>'
    lines = [('WELDED', 200, 'y'), ('SHUT', 200, 'w')]
    return page('#0d2448', svg(defs, b), lines, outline='#050b18')


# ====================================================================== C  (plankton in the drill core)
def radiolarian(x, y, s, col):
    g = f'<g transform="translate({x} {y}) scale({s})">'
    g += f'<circle r="30" fill="{col}" fill-opacity=".18" stroke="{col}" stroke-width="3"/>'
    for i in range(3):
        g += f'<circle r="{22 - i * 7}" fill="none" stroke="{col}" stroke-width="1.6" opacity=".8"/>'
    for k in range(14):
        a = k * 2 * math.pi / 14
        g += f'<path d="M{30 * math.cos(a):.1f} {30 * math.sin(a):.1f} L{50 * math.cos(a):.1f} {50 * math.sin(a):.1f}" stroke="{col}" stroke-width="2.6" stroke-linecap="round"/>'
    for k in range(8):
        a = k * 2 * math.pi / 8 + .2
        g += f'<circle cx="{14 * math.cos(a):.1f}" cy="{14 * math.sin(a):.1f}" r="3.5" fill="{col}" opacity=".7"/>'
    return g + '</g>'


def foram(x, y, s, col, rot=0):
    """chambered spiral (foraminifera-like)"""
    g = f'<g transform="translate({x} {y}) rotate({rot}) scale({s})">'
    for k in range(9):
        a = k * .75; rr = 6 + k * 3.4; d = 4 + k * 2.2
        cx, cy = d * math.cos(a), d * math.sin(a)
        g += f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{rr:.1f}" fill="{col}" fill-opacity=".2" stroke="{col}" stroke-width="2.4"/>'
    return g + '</g>'


def diatom(x, y, s, col, rot=0):
    g = f'<g transform="translate({x} {y}) rotate({rot}) scale({s})">'
    g += f'<ellipse rx="44" ry="16" fill="{col}" fill-opacity=".18" stroke="{col}" stroke-width="2.6"/><path d="M-40 0 H40" stroke="{col}" stroke-width="1.8"/>'
    for k in range(-5, 6):
        g += f'<path d="M{k * 7} -13 v26" stroke="{col}" stroke-width="1.4" opacity=".7"/>'
    return g + '</g>'


def thumb_C():
    r = random.Random(11)
    defs = FILTERS
    defs += lin('labC', [(0, '#0a1420'), (.6, '#112436'), (1, '#0b1520')])
    defs += rad('lampC', 1500, -60, 900, [(0, '#ffe6b0', .55), (.4, '#ffcf8a', .15), (1, '#ffcf8a', 0)])
    defs += lin('coreTop', [(0, '#c9ced8'), (.35, '#8e95a6'), (1, '#3d4252')])
    defs += lin('bench', [(0, '#6a4a32'), (1, '#2e1e14')])
    defs += rad('lensBg', 1180, 735, 220, [(0, '#1c3a52', 1), (.8, '#0c1a2a', 1), (1, '#06101c', 1)])
    defs += rad('lensGlow', 1180, 735, 330, [(0, '#7ff5d8', .35), (.7, '#7ff5d8', .12), (1, '#7ff5d8', 0)])
    defs += rad('vigC', 960, 540, 1150, [(0, '#000', 0), (.68, '#000', 0), (1, '#000', .6)])
    b = '<rect width="1920" height="1080" fill="url(#labC)"/>'
    # background: shelves of core trays (rows of grey cylinders in boxes)
    for row, yy in enumerate((150, 330)):
        b += f'<rect x="1340" y="{yy}" width="600" height="150" fill="#0d1a28" stroke="#22364a" stroke-width="4"/>'
        for k in range(5):
            b += f'<rect x="1356" y="{yy + 14 + k * 26}" width="570" height="18" rx="9" fill="#3a4658" opacity=".8"/><rect x="1356" y="{yy + 16 + k * 26}" width="570" height="5" rx="2.5" fill="#7a889c" opacity=".5"/>'
    b += '<rect width="1920" height="1080" fill="url(#lampC)"/>'
    # bench
    b += '<path d="M0 820 L1920 780 V1080 H0z" fill="url(#bench)"/><path d="M0 820 L1920 780" stroke="#c08a5a" stroke-width="4" opacity=".6"/>'
    for k in range(6):
        b += f'<path d="M0 {870 + k * 38} L1920 {832 + k * 40}" stroke="#20140c" stroke-width="2" opacity=".5"/>'
    # ---- the drill core: long cylinder, slightly tilted, broken into segments ----
    x0, x1, yc, R = 380, 1560, 770, 112
    tilt = -4
    g = f'<g transform="rotate({tilt} {(x0 + x1) / 2} {yc})">'
    g += f'<ellipse cx="{(x0 + x1) / 2}" cy="{yc + R + 10}" rx="{(x1 - x0) / 2 + 40}" ry="22" fill="#000" opacity=".45" filter="url(#b8)"/>'
    g += f'<rect x="{x0}" y="{yc - R}" width="{x1 - x0}" height="{2 * R}" fill="url(#coreTop)" stroke="#141820" stroke-width="5"/>'
    # metamorphic banding + crystals on the core
    for k in range(9):
        off = r.uniform(-R * .8, R * .8)
        d = f'M{x0} {yc + off:.0f} ' + ' '.join(f'Q {x0 + (j + .5) * 130} {yc + off + r.uniform(-24, 24):.0f} {x0 + (j + 1) * 131} {yc + off + r.uniform(-10, 10):.0f}' for j in range(9))
        g += f'<path d="{d}" fill="none" stroke="{r.choice(["#5a6070", "#d9dde6", "#7b6f6a"])}" stroke-width="{r.uniform(3, 9):.1f}" opacity=".45"/>'
    for _ in range(260):
        x = r.uniform(x0 + 6, x1 - 6); y = r.uniform(yc - R + 6, yc + R - 6); s = r.uniform(3, 9)
        g += f'<path d="M{x:.0f} {y:.0f} l{s:.1f} {-s * .4:.1f} l{s * .4:.1f} {s:.1f} l{-s:.1f} {s * .2:.1f}z" fill="{r.choice(["#f2f4f8", "#2a2e38", "#c9b29a", "#9aa2b4"])}" opacity="{r.uniform(.3, .8):.2f}"/>'
    # tiny glints of fossils on the surface
    for _ in range(14):
        x = r.uniform(x0 + 40, x1 - 40); y = r.uniform(yc - R + 20, yc + R - 20)
        g += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="7" fill="#7ff5d8" opacity=".3" filter="url(#b2)"/><circle cx="{x:.0f}" cy="{y:.0f}" r="2.6" fill="#d8fff4"/>'
    # segment breaks
    for xb in (640, 960, 1290):
        g += f'<path d="M{xb} {yc - R} q-14 {R * .6:.0f} 6 {R:.0f} q16 {R * .5:.0f} -4 {R:.0f}" fill="none" stroke="#141820" stroke-width="5"/>'
    # cylinder shading: light top band, dark bottom
    g += f'<rect x="{x0}" y="{yc - R + 10}" width="{x1 - x0}" height="22" fill="#ffffff" opacity=".28"/>'
    g += f'<rect x="{x0}" y="{yc + R * .45:.0f}" width="{x1 - x0}" height="{R * .55:.0f}" fill="#000" opacity=".3"/>'
    # cut end face (left), rim light
    g += f'<ellipse cx="{x0}" cy="{yc}" rx="42" ry="{R}" fill="#a7adbb" stroke="#141820" stroke-width="5"/>'
    for _ in range(40):
        a = r.uniform(0, 2 * math.pi); d = r.uniform(0, .85)
        g += f'<circle cx="{x0 + 42 * d * math.cos(a):.0f}" cy="{yc + R * d * math.sin(a):.0f}" r="{r.uniform(2, 5):.1f}" fill="{r.choice(["#e8ecf2", "#4a505c", "#c9b29a"])}"/>'
    g += f'<ellipse cx="{x1}" cy="{yc}" rx="42" ry="{R}" fill="#6a7080" stroke="#141820" stroke-width="5" clip-path="none" opacity="0"/>'
    g += f'<path d="M{x1} {yc - R} a42 {R} 0 0 1 0 {2 * R}" fill="#4a5060" stroke="#141820" stroke-width="5"/>'
    g += f'<path d="M{x0 + 40} {yc - R + 2} H{x1 - 6}" stroke="#ffe6b0" stroke-width="4" opacity=".75"/>'
    g += '</g>'
    b += g
    # ---- the magnifying glass with glowing microfossils ----
    LX, LY, LR = 1180, 735, 215
    b += f'<circle cx="{LX}" cy="{LY}" r="330" fill="url(#lensGlow)"/>'
    defs += f'<clipPath id="lensClip"><circle cx="{LX}" cy="{LY}" r="{LR}"/></clipPath>'
    lens = f'<g clip-path="url(#lensClip)"><rect x="{LX - LR}" y="{LY - LR}" width="{2 * LR}" height="{2 * LR}" fill="url(#lensBg)"/>'
    # magnified crystal grains
    for _ in range(40):
        x = r.uniform(LX - LR, LX + LR); y = r.uniform(LY - LR, LY + LR); s = r.uniform(14, 40)
        lens += f'<path d="M{x:.0f} {y:.0f} l{s:.0f} {-s * .4:.0f} l{s * .5:.0f} {s:.0f} l{-s:.0f} {s * .3:.0f}z" fill="{r.choice(["#2c4a66", "#1a3046", "#3b5a74"])}" opacity=".8"/>'
    for f in (radiolarian(LX - 70, LY - 70, 1.25, '#7ff5d8'), foram(LX + 90, LY - 40, 1.6, '#f2d27a', 20), diatom(LX - 20, LY + 110, 1.5, '#9ad8ff', -18),
              radiolarian(LX + 110, LY + 120, .8, '#f2d27a'), foram(LX - 150, LY + 60, 1.0, '#7ff5d8', 140), diatom(LX + 40, LY - 160, .9, '#7ff5d8', 30)):
        lens += f'<g filter="url(#b4)" opacity=".8">{f}</g>' + f
    lens += f'<circle cx="{LX - 60}" cy="{LY - 90}" r="140" fill="#ffffff" opacity=".06"/>'
    lens += '</g>'
    b += lens
    b += f'<path d="M{LX - 150} {LY - 120} a{LR - 20} {LR - 20} 0 0 1 120 -70" fill="none" stroke="#ffffff" stroke-width="10" opacity=".55" stroke-linecap="round"/>'
    b += f'<circle cx="{LX}" cy="{LY}" r="{LR + 12}" fill="none" stroke="#1a1208" stroke-width="34"/>'
    b += f'<circle cx="{LX}" cy="{LY}" r="{LR + 12}" fill="none" stroke="#c9963a" stroke-width="22"/>'
    b += f'<path d="M{LX - LR - 8} {LY - 40} a{LR + 12} {LR + 12} 0 0 1 {LR * .9:.0f} {-LR + 30}" fill="none" stroke="#ffe7a8" stroke-width="6" opacity=".9"/>'
    # handle toward the frog (lower left)
    a = math.radians(212); hx0, hy0 = LX + (LR + 22) * math.cos(a), LY - (LR + 22) * math.sin(a) * -1
    hx0, hy0 = LX - (LR + 18) * .97, LY - (LR + 18) * .25
    hx1, hy1 = hx0 - 135, hy0 - 6
    b += f'<path d="M{hx0:.0f} {hy0:.0f} L{hx1:.0f} {hy1:.0f}" stroke="#1a1208" stroke-width="40" stroke-linecap="round"/>'
    b += f'<path d="M{hx0:.0f} {hy0:.0f} L{hx1:.0f} {hy1:.0f}" stroke="#6a3a1e" stroke-width="28" stroke-linecap="round"/>'
    b += f'<path d="M{hx0 - 10:.0f} {hy0 - 4:.0f} L{hx1 + 6:.0f} {hy1 - 12:.0f}" stroke="#b56a3a" stroke-width="7" stroke-linecap="round" opacity=".8"/>'
    # ---- frog in a lab coat standing on the core, holding the handle ----
    FX, FY, FS = 760, 652, 3.0
    coat = ('<path d="M-38 2 q-6 -22 2 -30 q12 -4 30 -4 l8 18 l8 -18 q18 0 32 4 q10 10 2 30 q-42 10 -82 0z" fill="#f2f4f6" stroke-width="3.6"/>'
            '<path d="M2 -16 v16" stroke-width="2.4"/>'
            '<rect x="16" y="-18" width="14" height="10" rx="2" fill="#dfe4ea" stroke-width="2"/><path d="M20 -22 v6" stroke="#2a6ad0" stroke-width="2.4"/>')
    goggles = ('<path d="M-30 -86 q36 -16 72 0" fill="none" stroke="#3a3f4c" stroke-width="6"/>'
               '<circle cx="-10" cy="-90" r="9" fill="#bfe6ff" stroke-width="3"/><circle cx="22" cy="-90" r="9" fill="#bfe6ff" stroke-width="3"/>')
    b += frog(FX, FY, FS, look=(5, -3), mouth='O', mid=coat, top=goggles, sleeve='#f2f4f6',
              armR='M38 -24 q14 0 18 8', armL='M-34 -22 q-14 6 -16 22')
    b += sparkles([(LX + 250, LY - 160, 22), (LX - 260, LY - 150, 14), (LX + 280, LY + 140, 16), (1700, 640, 12)], '#e8fff8')
    for _ in range(30):
        x = r.uniform(900, 1500); y = r.uniform(220, 760)
        b += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r.choice([1.5, 2.2, 3])}" fill="#d8fff4" opacity="{r.uniform(.3, .8):.2f}"/>'
    b += '<rect width="1920" height="1080" fill="url(#vigC)"/>'
    lines = [('PLANKTON', 176, 'y'), ('IN THE ROCK?', 124, 'w')]
    return page('#0a1420', svg(defs, b), lines, outline='#04101c')


for n, fn in (('A', thumb_A), ('B', thumb_B), ('C', thumb_C)):
    open(os.path.join(HERE, f'{n}.html'), 'w').write(fn())
print('ok')
