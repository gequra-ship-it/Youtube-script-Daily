# Thumbnails A-C for fourth-dimension, round 2 (guideline 16-6 / 16-8, brief tools/briefs/thumb_art.md). Run: python3 videos/fourth-dimension/thumb/make.py
# Round 1 (Plato's cave / apple through paper / worldline) is kept as PNGs in /mnt/project-files/fourth-dimension/thumbs_draft/v1/.
# Owner 2026-11-01: "express the 4th dimension better; may cite the Avengers Tesseract or the film Cube".
# A  8 CUBES IN ONE?      homage: The Avengers' glowing Tesseract on its lab pedestal, but drawn as a true tesseract projection
#                         (inner cube + outer cube + 8 struts); script: "eight identical three-dimensional cubic cells"; frog in goggles + lab coat
# B  IT TURNS INSIDE OUT  homage: Cube (1997), the lit cubic cell with hatch doors; through the open hatch the next (teal) cell holds a
#                         tesseract turning inside out (ghost stages); script: "the inner cube seems to turn itself inside out"; frog in orange jumpsuit
# C  A 4D VISITOR         intuitive: the hypersphere passing through your living room: a dot pops up, grows to a ball, shrinks, vanishes
#                         (script S19-S22: "You witnessed a four-dimensional visitor"); frog in nightcap peeking over the armchair
import os, sys, math, random
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', '..', 'tools'))
from thumb_lib import page, svg, lin, rad, spark

INK = '#1d2b1c'; GREEN = '#6aa55a'; DARKG = '#4d8a4a'; BELLY = '#9cc98a'

FILTERS = ''.join(f'<filter id="b{n}" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="{n}"/></filter>' for n in (3, 6, 12, 24, 50))


def P(pts):
    return ' '.join(f'{a:.1f},{b:.1f}' for a, b in pts)


# ---------------- mascot frog (tools/assets/frog.svg body), posable ----------------
def limb(d, w=7.5, wi=3.4):
    return f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="{w}"/><path d="{d}" fill="none" stroke="{GREEN}" stroke-width="{wi}"/>'


def end_of(d):
    n = [float(v) for v in d.replace('M', ' ').replace('q', ' ').split()]
    return n[0] + n[-2], n[1] + n[-1]


def frog(x, y, s, rot=0, flip=False, look=(0, 0), mouth='O', armL=None, armR=None, legs=None, helmet=False, hat=False,
         brows=True, back="", front="", shadow=False, mid=""):
    sx = -s if flip else s
    g = [f'<g transform="translate({x} {y}) rotate({rot}) scale({sx} {s})" stroke="{INK}" stroke-linejoin="round" stroke-linecap="round">', back]
    if shadow:
        g.append('<ellipse cx="0" cy="8" rx="50" ry="8" fill="#000" opacity=".2" stroke="none"/>')
    if helmet:   # small life-support pack behind the body
        g.append('<rect x="-50" y="-58" width="20" height="42" rx="7" fill="#c9ced8" stroke-width="3"/><rect x="-46" y="-52" width="5" height="30" rx="2" fill="#fff" stroke="none" opacity=".6"/>')
    # legs: (hip x, hip y, foot x, foot y, foot angle)
    for hx, hy, fx, fy, fa in (legs or ((-20, -6, -22, 4, 0), (20, -6, 22, 4, 0))):
        if abs(fx - hx) + abs(fy - hy) > 14:
            g.append(limb(f'M{hx} {hy} L{fx} {fy}', 15, 9))
        g.append(f'<ellipse cx="{fx}" cy="{fy}" rx="16" ry="9" transform="rotate({fa} {fx} {fy})" fill="{DARKG}" stroke-width="3.2"/>')
    g.append(f'<path d="M-34 0 q-6 -64 34 -70 q40 -2 42 62 q0 10 -6 12 q-36 6 -70 -4z" fill="{GREEN}" stroke-width="4"/>')
    g.append(f'<ellipse cx="2" cy="-12" rx="22" ry="20" fill="{BELLY}" stroke="none" opacity=".7"/>')
    g.append('<path d="M-24 -50 q6 -14 18 -16" fill="none" stroke="#b6dea0" stroke-width="3" opacity=".8"/>')
    lx, ly = look
    for ex in (-10, 22):   # big round eyes, small pupils = surprised
        g.append(f'<circle cx="{ex}" cy="-66" r="13.5" fill="#f4f5ea" stroke-width="3.2"/>')
        g.append(f'<circle cx="{ex + 1 + lx}" cy="{-66 + ly}" r="4.4" fill="{INK}" stroke="none"/>')
        g.append(f'<circle cx="{ex + 2.4 + lx}" cy="{-67.6 + ly}" r="1.5" fill="#fff" stroke="none"/>')
    if brows:
        g.append('<path d="M-22 -88 q12 -9 24 -1 M10 -89 q12 -8 24 1" fill="none" stroke-width="3.4"/>')
    if mouth == 'O':   # wide-open surprised mouth with tongue
        g.append('<ellipse cx="6" cy="-38" rx="10" ry="12" fill="#7a2f33" stroke-width="3"/><ellipse cx="6" cy="-31" rx="6" ry="4" fill="#e07b7b" stroke="none"/>')
    else:
        g.append('<ellipse cx="6" cy="-41" rx="6" ry="7.5" fill="#7a2f33" stroke-width="3"/>')
    g.append('<ellipse cx="-18" cy="-48" rx="5" ry="3" fill="#e98a8a" stroke="none" opacity=".55"/><ellipse cx="30" cy="-48" rx="5" ry="3" fill="#e98a8a" stroke="none" opacity=".55"/>')
    if helmet:   # glass bubble around the head + silver collar
        g.append('<circle cx="6" cy="-58" r="45" fill="#bfe6ff" fill-opacity=".13" stroke="#e8f6ff" stroke-width="3.4" stroke-opacity=".95"/>')
        g.append('<path d="M-26 -82 q12 -18 32 -21" fill="none" stroke="#fff" stroke-width="5" opacity=".8"/><path d="M42 -40 q6 -10 6 -22" fill="none" stroke="#fff" stroke-width="3" opacity=".5"/>')
        g.append('<ellipse cx="6" cy="-16" rx="40" ry="9" fill="#d3d9e3" stroke-width="3.2"/><path d="M-30 -18 q36 8 72 0" fill="none" stroke="#fff" stroke-width="2.2" opacity=".8"/>')
    if hat:      # straw boater, knocked off the head
        g.append('<g transform="translate(40 -104) rotate(24)"><ellipse cx="0" cy="8" rx="40" ry="9" fill="#e7c77c" stroke-width="3.2"/>'
                 '<path d="M-24 8 L-22 -14 Q0 -20 22 -14 L24 8 Z" fill="#efd590" stroke-width="3.2"/><path d="M-23 -2 L23 -2 L23.5 5 L-23.5 5Z" fill="#2e2a4a" stroke-width="2"/>'
                 '<path d="M-30 6 q30 6 60 0" fill="none" stroke="#fff6d0" stroke-width="2" opacity=".7"/></g>')
    g.append(mid)
    for a in (armL or 'M-34 -22 q-14 6 -16 22', armR or 'M38 -22 q14 6 16 22'):
        g.append(limb(a)); ex_, ey_ = end_of(a)
        g.append(f'<circle cx="{ex_:.1f}" cy="{ey_:.1f}" r="5.6" fill="{GREEN}" stroke-width="3"/>')
    g.append(front); g.append('</g>')
    return ''.join(g)


def starfield(rnd, n, box, col='#eef4ff', skip=None):
    x0, y0, x1, y1 = box; o = ''
    for _ in range(n):
        x = rnd.uniform(x0, x1); y = rnd.uniform(y0, y1)
        if skip and skip(x, y): continue
        o += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{rnd.choice([1.1, 1.6, 2.2, 2.8])}" fill="{col}" opacity="{rnd.uniform(.2, .85):.2f}"/>'
    return o


from itertools import product


def tess_pts(a4, ry, rx, d4=3.2, d3=6.0):
    pts = []
    for v in product((-1, 1), repeat=4):
        x, y, z, w = v
        x, w = x * math.cos(a4) - w * math.sin(a4), x * math.sin(a4) + w * math.cos(a4)
        f = d4 / (d4 - w)
        X, Y, Z = x * f, y * f, z * f
        X, Z = X * math.cos(ry) + Z * math.sin(ry), -X * math.sin(ry) + Z * math.cos(ry)
        Y, Z = Y * math.cos(rx) - Z * math.sin(rx), Y * math.sin(rx) + Z * math.cos(rx)
        g = d3 / (d3 - Z)
        pts.append((X * g, Y * g, Z))
    edges = [(i, j) for i in range(16) for j in range(i + 1, 16) if bin(i ^ j).count('1') == 1]
    return pts, edges


def tess_lines(cx, cy, S, pts, edges, col, w, op=1, extra=''):
    o = ''
    for i, j in edges:
        a, b = pts[i], pts[j]
        o += (f'<line x1="{cx + a[0] * S:.1f}" y1="{cy + a[1] * S:.1f}" x2="{cx + b[0] * S:.1f}" y2="{cy + b[1] * S:.1f}" '
              f'stroke="{col}" stroke-width="{w}" stroke-linecap="round" opacity="{op}" {extra}/>')
    return o


def flame(x, y, w, h, col, op=1):
    return (f'<path d="M{x - w} {y} C{x - w * 1.1} {y - h * .45} {x - w * .1} {y - h * .55} {x + w * .15} {y - h} '
            f'C{x + w * .5} {y - h * .55} {x + w * 1.1} {y - h * .45} {x + w} {y} Q{x} {y + w * .5} {x - w} {y}Z" fill="{col}" opacity="{op}"/>')



# ---------------- tesseract helpers ----------------
def tess_screen(a4, ry, rx, cx, cy, half, d4=3.2, d3=6.0):
    pts, edges = tess_pts(a4, ry, rx, d4, d3)
    m = max(max(abs(p[0]), abs(p[1])) for p in pts)
    k = half / m
    return [(cx + p[0] * k, cy + p[1] * k, p[2]) for p in pts], edges


def hull(points):
    p = sorted(set((round(a, 2), round(b, 2)) for a, b in points))
    if len(p) < 3: return p
    cr = lambda o, a, b: (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
    lo, up = [], []
    for q in p:
        while len(lo) >= 2 and cr(lo[-2], lo[-1], q) <= 0: lo.pop()
        lo.append(q)
    for q in reversed(p):
        while len(up) >= 2 and cr(up[-2], up[-1], q) <= 0: up.pop()
        up.append(q)
    return lo[:-1] + up[:-1]


def tess_draw(sp, edges, cin, cout, cstrut, w=7, glow=True, gcol=None, op=1, dots=True, core='#ffffff'):
    zs = [p[2] for p in sp]; z0, z1 = min(zs), max(zs)
    o = ''
    if glow:
        g = ''.join(f'<line x1="{sp[i][0]:.1f}" y1="{sp[i][1]:.1f}" x2="{sp[j][0]:.1f}" y2="{sp[j][1]:.1f}"/>' for i, j in edges)
        o += f'<g stroke="{gcol or cout}" stroke-width="{w * 4}" stroke-linecap="round" opacity="{.55 * op}" filter="url(#b12)">{g}</g>'
    for i, j in sorted(edges, key=lambda e: sp[e[0]][2] + sp[e[1]][2]):
        dz = ((sp[i][2] + sp[j][2]) / 2 - z0) / ((z1 - z0) or 1)   # 0 back .. 1 front
        col = cstrut if (i ^ j) == 1 else (cout if i & 1 else cin)
        ww = w * (.6 + .7 * dz)
        o += (f'<line x1="{sp[i][0]:.1f}" y1="{sp[i][1]:.1f}" x2="{sp[j][0]:.1f}" y2="{sp[j][1]:.1f}" stroke="{col}" stroke-width="{ww:.1f}" '
              f'stroke-linecap="round" opacity="{op * (.55 + .45 * dz):.2f}"/>')
        o += (f'<line x1="{sp[i][0]:.1f}" y1="{sp[i][1]:.1f}" x2="{sp[j][0]:.1f}" y2="{sp[j][1]:.1f}" stroke="{core}" stroke-width="{ww * .32:.1f}" '
              f'stroke-linecap="round" opacity="{op * (.5 + .5 * dz):.2f}"/>')
    if dots:
        for p in sp:
            dz = (p[2] - z0) / ((z1 - z0) or 1)
            o += f'<circle cx="{p[0]:.1f}" cy="{p[1]:.1f}" r="{w * (.8 + .6 * dz):.1f}" fill="{core}" opacity="{op:.2f}"/>'
    return o


def bil(Q, u, v):   # bilinear point in quad Q = [p00, p10, p11, p01]
    (ax, ay), (bx, by), (cx_, cy_), (dx, dy) = Q
    x = (1 - u) * (1 - v) * ax + u * (1 - v) * bx + u * v * cx_ + (1 - u) * v * dx
    y = (1 - u) * (1 - v) * ay + u * (1 - v) * by + u * v * cy_ + (1 - u) * v * dy
    return x, y


def subq(Q, u0, v0, u1, v1):
    return [bil(Q, u0, v0), bil(Q, u1, v0), bil(Q, u1, v1), bil(Q, u0, v1)]


def jag(rnd, x, y, ang, L, n=6, amp=18):
    pts = [(x, y)]
    for k in range(1, n + 1):
        t = k / n; px = x + math.cos(ang) * L * t; py = y + math.sin(ang) * L * t
        if k < n: px += rnd.uniform(-amp, amp); py += rnd.uniform(-amp, amp)
        pts.append((px, py))
    return P(pts)


# ================= A: the Avengers' Tesseract, drawn as a true tesseract =================
def make_A():
    rnd = random.Random(21)
    cx, cy = 1250, 400
    d = FILTERS
    d += lin('labA', [(0, '#0a1a36'), (.6, '#06102a'), (1, '#02060f')])
    d += rad('haloA', cx, cy, 950, [(0, '#bff4ff', .95), (.12, '#4fd2ff', .7), (.4, '#1a6ad8', .25), (1, '#0a1a36', 0)])
    d += rad('rayA', cx, cy, 1300, [(0, '#e8fbff', .9), (.25, '#6fdcff', .45), (1, '#3aa0ff', 0)])
    d += rad('coreA', cx, cy, 190, [(0, '#ffffff', 1), (.35, '#b8f2ff', .95), (.8, '#2fb8ff', .7), (1, '#1a7ad8', .5)])
    d += rad('shellA', cx, cy, 340, [(0, '#7fe0ff', .35), (1, '#1a6ad8', .12)])
    d += lin('metal', [(0, '#1a2436'), (.25, '#5a6a84'), (.5, '#c6d2e2'), (.7, '#4a5872'), (1, '#121a2a')], x2=1, y2=0)
    d += lin('floorA', [(0, '#0a1630'), (1, '#01040a')])
    d += rad('vigA', 960, 540, 1150, [(0, '#000', 0), (.65, '#000', 0), (1, '#000', .7)])
    b = '<rect width="1920" height="1080" fill="url(#labA)"/>'
    # lab back wall: tall panels with light slits
    for k in range(17):
        x = k * 120
        b += f'<rect x="{x + 6}" y="0" width="108" height="780" fill="#0e2246" opacity=".55"/>'
        b += f'<rect x="{x + 54}" y="60" width="6" height="640" fill="#4fb8ff" opacity="{.10 + .18 * (k % 3 == 0):.2f}"/>'
    b += '<rect y="770" width="1920" height="14" fill="#1a3a6a"/>'
    b += '<rect width="1920" height="1080" fill="url(#haloA)"/>'
    # floor with perspective grid
    b += '<rect y="784" width="1920" height="296" fill="url(#floorA)"/>'
    for k in range(-14, 15):
        b += f'<line x1="{cx + k * 30}" y1="784" x2="{cx + k * 260}" y2="1080" stroke="#3a8ad8" stroke-width="2" opacity=".18"/>'
    for k in range(1, 7):
        y = 784 + (k / 7) ** 1.6 * 296
        b += f'<line x1="0" y1="{y:.0f}" x2="1920" y2="{y:.0f}" stroke="#3a8ad8" stroke-width="2" opacity=".15"/>'
    b += f'<ellipse cx="{cx}" cy="960" rx="520" ry="90" fill="#4fd2ff" opacity=".28" filter="url(#b50)"/>'
    # light rays (skip most of the text area up-left)
    for k in range(22):
        a = math.radians(k * 360 / 22 + rnd.uniform(-5, 5)); wd = math.radians(rnd.uniform(1.6, 3.8))
        deg = math.degrees(a) % 360
        op = .18 if 185 < deg < 265 else rnd.uniform(.35, .7)
        L = 1500
        b += (f'<path d="M{cx} {cy} L{cx + L * math.cos(a - wd):.0f} {cy + L * math.sin(a - wd):.0f} L{cx + L * math.cos(a + wd):.0f} {cy + L * math.sin(a + wd):.0f}Z" '
              f'fill="url(#rayA)" opacity="{op:.2f}" filter="url(#b6)"/>')
    # pedestal
    b += f'<ellipse cx="{cx}" cy="1000" rx="330" ry="58" fill="#000" opacity=".5" filter="url(#b12)"/>'
    b += f'<path d="M{cx - 300} 930 L{cx - 300} 975 A300 52 0 0 0 {cx + 300} 975 L{cx + 300} 930Z" fill="url(#metal)" stroke="#060a14" stroke-width="4"/>'
    b += f'<ellipse cx="{cx}" cy="930" rx="300" ry="52" fill="#2a3650" stroke="#060a14" stroke-width="4"/>'
    b += f'<path d="M{cx - 170} 760 L{cx - 200} 930 A200 34 0 0 0 {cx + 200} 930 L{cx + 170} 760Z" fill="url(#metal)" stroke="#060a14" stroke-width="4"/>'
    for k in range(5):
        y = 790 + k * 28
        b += f'<path d="M{cx - 175 - k * 5} {y} A{175 + k * 5} 26 0 0 0 {cx + 175 + k * 5} {y}" fill="none" stroke="#7fe0ff" stroke-width="3" opacity="{.6 - k * .1:.2f}"/>'
    b += f'<ellipse cx="{cx}" cy="760" rx="240" ry="44" fill="#3a4a66" stroke="#060a14" stroke-width="4"/>'
    b += f'<ellipse cx="{cx}" cy="752" rx="200" ry="34" fill="#9fe8ff" opacity=".55" filter="url(#b6)"/>'
    b += f'<ellipse cx="{cx}" cy="752" rx="200" ry="34" fill="none" stroke="#e8fbff" stroke-width="5"/>'
    # tesseract (a true 4D cube projection: inner cube + outer cube + 8 struts)
    sp, ed = tess_screen(math.radians(14), math.radians(32), math.radians(-20), cx, cy, 320)
    inner = [p[:2] for i, p in enumerate(sp) if not i & 1]; outer = [p[:2] for i, p in enumerate(sp) if i & 1]
    # clamp prongs reaching up to the lowest outer corners
    low = sorted(outer, key=lambda p: -p[1])[:3]
    for (px, py) in low:
        bx = cx + (px - cx) * .55
        b += f'<path d="M{bx:.0f} 762 Q{(bx + px) / 2:.0f} {py + 120:.0f} {px:.0f} {py + 18:.0f}" fill="none" stroke="#060a14" stroke-width="22" stroke-linecap="round"/>'
        b += f'<path d="M{bx:.0f} 762 Q{(bx + px) / 2:.0f} {py + 120:.0f} {px:.0f} {py + 18:.0f}" fill="none" stroke="url(#metal)" stroke-width="14" stroke-linecap="round"/>'
        b += f'<circle cx="{px:.0f}" cy="{py + 18:.0f}" r="14" fill="#9fe8ff" stroke="#060a14" stroke-width="4"/>'
    b += f'<circle cx="{cx}" cy="{cy}" r="360" fill="#4fd2ff" opacity=".35" filter="url(#b50)"/>'
    b += f'<polygon points="{P(hull(outer))}" fill="url(#shellA)" stroke="none"/>'
    b += f'<polygon points="{P(hull(inner))}" fill="#4fd2ff" opacity=".6" filter="url(#b24)"/>'
    b += f'<polygon points="{P(hull(inner))}" fill="url(#coreA)" opacity=".85"/>'
    b += f'<circle cx="{cx}" cy="{cy}" r="70" fill="#ffffff" opacity=".9" filter="url(#b24)"/>'
    b += tess_draw(sp, ed, '#ffffff', '#6fe2ff', '#a9eeff', w=9, gcol='#3ac8ff')
    # electric arcs off the corners
    for p in rnd.sample(sp, 8):
        a = math.atan2(p[1] - cy, p[0] - cx) + rnd.uniform(-.5, .5)
        path = jag(rnd, p[0], p[1], a, rnd.uniform(70, 150), 5, 14)
        b += f'<polyline points="{path}" fill="none" stroke="#6fe2ff" stroke-width="10" opacity=".55" filter="url(#b6)"/>'
        b += f'<polyline points="{path}" fill="none" stroke="#f2fdff" stroke-width="3"/>'
    for _ in range(26):
        a = rnd.uniform(0, 6.28); r = rnd.uniform(340, 560)
        x, y = cx + r * math.cos(a), cy + r * math.sin(a) * .8
        if x < 900 and y < 500: continue
        b += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{rnd.uniform(2, 5):.1f}" fill="#d8f8ff" opacity="{rnd.uniform(.4, .9):.2f}"/>'
    b += spark(cx + 360, cy - 250, 26, '#ffffff') + spark(cx - 380, cy + 170, 18, '#e8fbff') + spark(1700, 640, 16, '#e8fbff', .7)
    # frog scientist: lab coat, goggles pushed up, arms up in awe
    coat = ('<path d="M-37 -2 Q-42 -32 -26 -46 L-6 -26 L-10 2 Z" fill="#f2f6fa" stroke-width="3.2"/>'
            '<path d="M44 -2 Q46 -32 30 -46 L14 -26 L18 2 Z" fill="#f2f6fa" stroke-width="3.2"/>'
            '<rect x="24" y="-20" width="12" height="10" rx="2" fill="#dfe6ee" stroke-width="2"/><path d="M28 -24 V-12" stroke="#3a7ad8" stroke-width="3"/>')
    gog = ('<path d="M-34 -84 Q6 -104 48 -84" fill="none" stroke="#2a3040" stroke-width="6"/>'
           '<circle cx="-6" cy="-92" r="11" fill="#8fe6ff" stroke-width="3.5"/><circle cx="20" cy="-92" r="11" fill="#8fe6ff" stroke-width="3.5"/>'
           '<circle cx="-9" cy="-95" r="3.5" fill="#fff" stroke="none"/><circle cx="17" cy="-95" r="3.5" fill="#fff" stroke="none"/>')
    b += f'<circle cx="600" cy="880" r="220" fill="#4fd2ff" opacity=".16" filter="url(#b50)"/>'
    b += frog(610, 1000, 3.0, look=(6, -5), mouth='O', brows=False, mid=coat, front=gog, shadow=True,
              armL='M-34 -22 q-22 -20 -14 -52', armR='M38 -22 q24 -18 18 -52')
    b += '<rect width="1920" height="1080" fill="url(#vigA)"/>'
    lines = [('<span class="g">8 CUBES</span>', 205, 'w'), ('IN ONE?', 205, 'w')]
    return page('#06102a', svg(d, b), lines, outline='#030818', top=48)


# ================= B: Cube (1997) cell, tesseract turning inside out through the hatch =================
def panels(Q, n, base, lite, edge, rnd, skip=None, sym=True):
    o = f'<polygon points="{P(Q)}" fill="{base}"/>'
    for i in range(n):
        for j in range(n):
            if skip and (i, j) in skip: continue
            u0, v0, u1, v1 = i / n, j / n, (i + 1) / n, (j + 1) / n
            o += f'<polygon points="{P(subq(Q, u0, v0, u1, v1))}" fill="none" stroke="{edge}" stroke-width="7"/>'
            o += f'<polygon points="{P(subq(Q, u0 + .02 / n * 8, v0 + .02 / n * 8, u1 - .02 / n * 8, v1 - .02 / n * 8))}" fill="{lite}" opacity=".55"/>'
            # inner 3x3 engraved squares (the cell walls' grid look)
            for a in range(1, 3):
                p0 = bil(Q, u0 + (u1 - u0) * a / 3, v0 + .1 / n); p1 = bil(Q, u0 + (u1 - u0) * a / 3, v1 - .1 / n)
                o += f'<line x1="{p0[0]:.0f}" y1="{p0[1]:.0f}" x2="{p1[0]:.0f}" y2="{p1[1]:.0f}" stroke="{edge}" stroke-width="2.5" opacity=".55"/>'
                p0 = bil(Q, u0 + .1 / n, v0 + (v1 - v0) * a / 3); p1 = bil(Q, u1 - .1 / n, v0 + (v1 - v0) * a / 3)
                o += f'<line x1="{p0[0]:.0f}" y1="{p0[1]:.0f}" x2="{p1[0]:.0f}" y2="{p1[1]:.0f}" stroke="{edge}" stroke-width="2.5" opacity=".55"/>'
            if sym and rnd.random() < .45:
                c = bil(Q, (u0 + u1) / 2, (v0 + v1) / 2)
                s = 8 + 10 * rnd.random()
                o += f'<circle cx="{c[0]:.0f}" cy="{c[1]:.0f}" r="{s:.0f}" fill="none" stroke="{edge}" stroke-width="3" opacity=".6"/>'
    return o


def make_B():
    rnd = random.Random(5)
    X0, X1, Y0, Y1 = 860, 1500, 150, 790          # back wall of this cell
    HX0, HX1, HY0, HY1 = 1010, 1350, 300, 640     # open hatch in the back wall
    d = FILTERS
    d += rad('lightB', 1180, 470, 1200, [(0, '#ffd08a', .55), (.5, '#ff8a2a', .15), (1, '#ff6a00', 0)])
    d += rad('tealB', 1180, 470, 260, [(0, '#e8fffa', 1), (.35, '#5af0d0', .9), (1, '#0a6a6a', .9)])
    d += rad('vigB', 960, 540, 1150, [(0, '#000', 0), (.6, '#000', 0), (1, '#000', .7)])
    d += f'<clipPath id="hatch"><rect x="{HX0}" y="{HY0}" width="{HX1 - HX0}" height="{HY1 - HY0}"/></clipPath>'
    C = [(0, 0), (1920, 0), (1920, 1080), (0, 1080)]
    back = [(X0, Y0), (X1, Y0), (X1, Y1), (X0, Y1)]
    ceil = [C[0], C[1], back[1], back[0]]; rwall = [back[1], C[1], C[2], back[2]]
    floor = [back[3], back[2], C[2], C[3]]; lwall = [C[0], back[0], back[3], C[3]]
    b = ''
    b += panels(lwall, 3, '#5a2408', '#c0581a', '#2a0e02', rnd)
    b += panels(rwall, 3, '#a8480e', '#ff9a3a', '#3a1404', rnd)
    b += panels(ceil, 3, '#7a6a20', '#d8e070', '#2a2604', rnd, skip={(1, 1)}, sym=False)
    b += panels(floor, 3, '#5a2a08', '#b05a1a', '#220c02', rnd, skip={(1, 1)}, sym=False)
    # ceiling hatch glowing green, floor hatch closed (lit edge)
    ch = subq(ceil, 1 / 3, 1 / 3, 2 / 3, 2 / 3)
    b += f'<polygon points="{P(ch)}" fill="#9cff7a" opacity=".85"/><polygon points="{P(ch)}" fill="#e8ffd0" opacity=".7" filter="url(#b12)"/>'
    b += f'<polygon points="{P(ch)}" fill="none" stroke="#2a3004" stroke-width="10"/>'
    fh = subq(floor, 1 / 3, 1 / 3, 2 / 3, 2 / 3)
    b += f'<polygon points="{P(fh)}" fill="#3a1806" stroke="#1a0802" stroke-width="10"/><polygon points="{P(subq(floor, .38, .4, .62, .6))}" fill="#7a3a10"/>'
    # wheel handle on the floor hatch
    fc = bil(floor, .5, .5)
    b += f'<ellipse cx="{fc[0]:.0f}" cy="{fc[1]:.0f}" rx="60" ry="22" fill="none" stroke="#c8b090" stroke-width="8"/>'
    # back wall frame with panels around the hatch
    b += panels(back, 3, '#c25a14', '#ffb050', '#3a1404', rnd, skip={(1, 1)})
    b += '<rect width="1920" height="1080" fill="url(#lightB)"/>'
    # next cell (teal), seen through the hatch
    n = ''
    nb = (1110, 400, 1250, 540)
    nC = [(HX0, HY0), (HX1, HY0), (HX1, HY1), (HX0, HY1)]; nB = [(nb[0], nb[1]), (nb[2], nb[1]), (nb[2], nb[3]), (nb[0], nb[3])]
    n += panels([nC[0], nC[1], nB[1], nB[0]], 2, '#0a6a5a', '#5af0c0', '#022a24', rnd, sym=False)
    n += panels([nB[1], nC[1], nC[2], nB[2]], 2, '#0a8a7a', '#6affe0', '#022a24', rnd, sym=False)
    n += panels([nB[3], nB[2], nC[2], nC[3]], 2, '#064a40', '#3ac0a0', '#022a24', rnd, sym=False)
    n += panels([nC[0], nB[0], nB[3], nC[3]], 2, '#08584a', '#4ad8b0', '#022a24', rnd, sym=False)
    n += panels(nB, 1, '#0c7a6a', '#7affe8', '#022a24', rnd, sym=False)
    n += f'<rect x="{HX0}" y="{HY0}" width="{HX1 - HX0}" height="{HY1 - HY0}" fill="url(#tealB)" opacity=".55"/>'
    b += f'<g clip-path="url(#hatch)">{n}</g>'
    # hatch frame (thick, bevelled) and the swung-open hatch door on its left hinge
    b += f'<rect x="{HX0 - 16}" y="{HY0 - 16}" width="{HX1 - HX0 + 32}" height="{HY1 - HY0 + 32}" fill="none" stroke="#2a0e02" stroke-width="24"/>'
    b += f'<rect x="{HX0 - 6}" y="{HY0 - 6}" width="{HX1 - HX0 + 12}" height="{HY1 - HY0 + 12}" fill="none" stroke="#ffcf7a" stroke-width="5" opacity=".8"/>'
    door = [(HX0 - 10, HY0 - 10), (HX0 - 170, HY0 - 70), (HX0 - 170, HY1 + 70), (HX0 - 10, HY1 + 10)]
    b += f'<polygon points="{P([(x - 12, y + 14) for x, y in door])}" fill="#000" opacity=".35" filter="url(#b12)"/>'
    b += panels(door, 2, '#d8762a', '#ffc070', '#3a1404', rnd, sym=False)
    b += f'<polygon points="{P(door)}" fill="none" stroke="#2a0e02" stroke-width="8"/>'
    dc = bil(door, .5, .5)
    b += f'<ellipse cx="{dc[0]:.0f}" cy="{dc[1]:.0f}" rx="18" ry="46" fill="none" stroke="#e8d0a0" stroke-width="8"/>'
    # the tesseract turning inside out: ghost stages + the current one, pouring out through the hatch
    hc = (1180, 470)
    b += f'<circle cx="{hc[0]}" cy="{hc[1]}" r="330" fill="#5af0d0" opacity=".35" filter="url(#b50)"/>'
    stages = [(-50, .45, 200), (-18, .6, 250), (22, 1, 310)]
    for a4, op, half in stages:
        sp, ed = tess_screen(math.radians(a4), math.radians(28), math.radians(-18), hc[0], hc[1], half)
        b += tess_draw(sp, ed, '#ffffff', '#7affe0' if op == 1 else '#f2d27a', '#b8fff0' if op == 1 else '#ffe6a8', w=8 if op == 1 else 4, gcol='#2affc8' if op == 1 else '#ffb84a', op=op, dots=op == 1, glow=True)
        if op == 1:
            inner = [p[:2] for i, p in enumerate(sp) if not i & 1]
            b += f'<polygon points="{P(hull(inner))}" fill="#c8fff0" opacity=".22"/>'
            last = sp
        else:
            prev = sp
    # motion arcs: inner corners sweeping outward
    for i in (0, 4, 10, 14):
        (x0, y0, _), (x1, y1, _) = prev[i], last[i]
        mx, my = (x0 + x1) / 2 + (y1 - y0) * .3, (y0 + y1) / 2 - (x1 - x0) * .3
        b += f'<path d="M{x0:.0f} {y0:.0f} Q{mx:.0f} {my:.0f} {x1:.0f} {y1:.0f}" fill="none" stroke="#f2d27a" stroke-width="5" stroke-dasharray="4 14" stroke-linecap="round" opacity=".9"/>'
    b += spark(hc[0] + 340, hc[1] - 280, 24, '#ffffff') + spark(hc[0] - 300, hc[1] + 240, 16, '#e8fffa') + spark(1640, 380, 16, '#fff6d6', .7)
    # frog prisoner in grey coveralls, standing in the cell, looking at the hatch
    suit = ('<path d="M-37 -4 Q-40 -26 -30 -34 Q6 -22 42 -34 Q48 -26 44 -4 Q6 4 -37 -4Z" fill="#5a6a7a" stroke-width="3.2"/>'
            '<path d="M-30 -34 Q6 -18 42 -34" fill="none" stroke="#8a9aaa" stroke-width="3"/>'
            '<rect x="-24" y="-24" width="20" height="10" rx="2" fill="#f2f2e8" stroke-width="2"/>')
    b += f'<ellipse cx="560" cy="1000" rx="170" ry="26" fill="#000" opacity=".45" filter="url(#b6)"/>'
    b += frog(560, 1000, 3.1, look=(7, -4), mouth='O', mid=suit,
              armL='M-34 -22 q-20 2 -26 24', armR='M38 -22 q26 -14 34 -44',
              legs=((-20, -6, -26, 4, -6), (20, -6, 26, 4, 8)))
    b += '<rect width="1920" height="1080" fill="url(#vigB)"/>'
    lines = [('IT TURNS', 140, 'w'), ('<span class="g">INSIDE</span>', 225, 'w'), ('<span class="g">OUT</span>', 225, 'w')]
    return page('#3a1404', svg(d, b), lines, outline='#1a0802', top=40)


# ================= C: a 4D visitor in your living room =================
def ball(cx, cy, r, op=1, tag=''):
    o = f'<circle cx="{cx}" cy="{cy}" r="{r * 1.9:.0f}" fill="#7ae8ff" opacity="{.35 * op:.2f}" filter="url(#b50)"/>'
    o += f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="url(#ballG{tag})" opacity="{op}"/>'
    o += f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="url(#ballRim{tag})" opacity="{op}"/>'
    o += f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="#e8fbff" stroke-width="{max(2, r * .025):.1f}" opacity="{.8 * op:.2f}"/>'
    o += f'<ellipse cx="{cx - r * .35:.0f}" cy="{cy - r * .42:.0f}" rx="{r * .28:.0f}" ry="{r * .16:.0f}" fill="#fff" opacity="{.75 * op:.2f}" transform="rotate(-30 {cx - r * .35:.0f} {cy - r * .42:.0f})" filter="url(#b3)"/>'
    return o


def make_C():
    rnd = random.Random(9)
    d = FILTERS
    d += lin('wallC', [(0, '#1c1838'), (1, '#2c2048')])
    d += lin('floorC', [(0, '#3a2414'), (1, '#120a06')])
    d += lin('skyC', [(0, '#0a1030'), (1, '#28305a')])
    d += rad('roomGlow', 1190, 540, 1000, [(0, '#8af0ff', .55), (.35, '#5a8aff', .2), (1, '#3a2a7a', 0)])
    d += rad('lampC', 1780, 600, 520, [(0, '#ffd08a', .6), (1, '#ff9a40', 0)])
    d += '<radialGradient id="ballG" cx=".38" cy=".34" r=".75"><stop offset="0" stop-color="#ffffff"/><stop offset=".25" stop-color="#c8f6ff"/><stop offset=".6" stop-color="#5ac8ff"/><stop offset="1" stop-color="#3a3ad0"/></radialGradient>'
    d += '<radialGradient id="ballRim" cx=".5" cy=".5" r=".5"><stop offset=".72" stop-color="#ff7ad8" stop-opacity="0"/><stop offset=".93" stop-color="#ff7ad8" stop-opacity=".55"/><stop offset="1" stop-color="#ffd0f0" stop-opacity=".9"/></radialGradient>'
    d += rad('vigC', 960, 540, 1150, [(0, '#000', 0), (.65, '#000', 0), (1, '#000', .7)])
    b = '<rect width="1920" height="1080" fill="url(#wallC)"/>'
    # wallpaper stripes
    for k in range(0, 1920, 64):
        b += f'<rect x="{k}" y="0" width="22" height="780" fill="#3a2e5a" opacity=".35"/>'
    b += '<rect y="740" width="1920" height="40" fill="#4a3a2a"/><rect y="740" width="1920" height="6" fill="#8a6a4a"/>'
    # window with night sky (top right)
    b += '<rect x="1420" y="70" width="380" height="380" fill="url(#skyC)" stroke="#6a4a2a" stroke-width="22"/>'
    b += starfield(rnd, 40, (1440, 90, 1780, 430))
    b += '<circle cx="1700" cy="160" r="34" fill="#fff4d0"/><circle cx="1714" cy="152" r="30" fill="#28305a" opacity=".9"/>'
    b += '<line x1="1610" y1="70" x2="1610" y2="450" stroke="#6a4a2a" stroke-width="14"/><line x1="1420" y1="260" x2="1800" y2="260" stroke="#6a4a2a" stroke-width="14"/>'
    b += '<path d="M1380 40 Q1420 260 1390 480 L1450 480 Q1470 260 1440 40Z" fill="#7a2a4a"/><path d="M1840 40 Q1800 260 1830 480 L1770 480 Q1760 260 1790 40Z" fill="#7a2a4a"/>'
    b += '<rect x="1360" y="30" width="500" height="18" rx="9" fill="#3a2410"/>'
    # picture frame on the wall
    b += '<rect x="780" y="140" width="190" height="150" fill="#d8c090" stroke="#4a3018" stroke-width="12"/><path d="M790 280 L850 200 L900 250 L930 220 L960 280Z" fill="#6a8a5a"/>'
    # floor planks in perspective
    b += '<rect y="780" width="1920" height="300" fill="url(#floorC)"/>'
    for k in range(-12, 13):
        b += f'<line x1="{1190 + k * 110}" y1="780" x2="{1190 + k * 330}" y2="1080" stroke="#1a0e06" stroke-width="3" opacity=".6"/>'
    b += '<ellipse cx="1190" cy="900" rx="520" ry="90" fill="#6a3a5a" opacity=".55"/><ellipse cx="1190" cy="900" rx="470" ry="74" fill="none" stroke="#e0a0c0" stroke-width="5" opacity=".4"/>'
    # side lamp (right) and small table
    b += '<rect width="1920" height="1080" fill="url(#lampC)"/>'
    b += '<rect x="1730" y="640" width="120" height="16" fill="#5a3a20"/><rect x="1780" y="656" width="20" height="150" fill="#3a2410"/>'
    b += '<path d="M1740 560 L1840 560 L1820 500 L1760 500Z" fill="#f2c27a" stroke="#6a4a20" stroke-width="4"/><rect x="1786" y="560" width="8" height="80" fill="#3a2410"/>'
    b += '<rect width="1920" height="1080" fill="url(#roomGlow)"/>'
    # the 4D visitor: dot pops up, grows to a ball, shrinks, vanishes (time-lapse ghosts)
    seq = [(700, 520, 7, .9), (830, 520, 46, .45), (1190, 500, 190, 1), (1530, 520, 60, .45), (1650, 520, 8, .9)]
    for x, y, r, op in seq:
        b += f'<ellipse cx="{x}" cy="840" rx="{max(14, r * 1.1):.0f}" ry="{max(4, r * .18):.0f}" fill="#000" opacity="{.45 * op:.2f}" filter="url(#b6)"/>'
    b += '<path d="M700 520 Q1190 230 1650 520" fill="none" stroke="#f2d27a" stroke-width="5" stroke-dasharray="3 16" stroke-linecap="round" opacity=".7"/>'
    for x, y, r, op in seq:
        if r < 20:
            b += f'<circle cx="{x}" cy="{y}" r="40" fill="#bff4ff" opacity=".6" filter="url(#b12)"/><circle cx="{x}" cy="{y}" r="{r}" fill="#ffffff"/>' + spark(x, y, 30, '#ffffff', .9)
        else:
            b += ball(x, y, r, op)
    # 3D slices hint: faint latitude rings on the big ball
    for k, yy in enumerate((-110, -40, 40, 110)):
        rr = math.sqrt(190 ** 2 - yy ** 2)
        b += f'<ellipse cx="1190" cy="{500 + yy}" rx="{rr:.0f}" ry="{rr * .22:.0f}" fill="none" stroke="#ffffff" stroke-width="3" opacity=".28"/>'
    b += spark(1420, 300, 22) + spark(960, 330, 16) + spark(1350, 720, 14, '#e8fbff')
    # armchair (bottom-left) with the frog peeking over its back in a nightcap
    cap = ('<path d="M-30 -86 Q4 -112 44 -88 Q30 -128 -4 -130 Q-40 -126 -60 -100 Q-66 -92 -58 -86 Z" fill="#4a6ad0" stroke-width="3.4"/>'
           '<path d="M-32 -86 Q6 -98 46 -86" fill="none" stroke="#f2f2e8" stroke-width="9"/><circle cx="-62" cy="-92" r="11" fill="#f2f2e8" stroke-width="3"/>'
           '<circle cx="-10" cy="-112" r="4" fill="#f2d27a" stroke="none"/><circle cx="20" cy="-108" r="4" fill="#f2d27a" stroke="none"/>')
    b += f'<circle cx="430" cy="760" r="200" fill="#7ae8ff" opacity=".14" filter="url(#b50)"/>'
    b += frog(440, 860, 3.0, look=(8, -4), mouth='O', brows=False, front=cap,
              armL='M-34 -22 q-8 -8 -10 -12', armR='M38 -22 q8 -8 10 -12')
    b += '<path d="M150 1080 L150 830 Q150 770 220 770 L660 770 Q730 770 730 830 L730 1080Z" fill="#8a2a3a" stroke="#2a0a10" stroke-width="7"/>'
    b += '<path d="M180 800 Q440 780 700 800" fill="none" stroke="#c8506a" stroke-width="8" opacity=".6"/>'
    for x in (300, 440, 580):
        b += f'<circle cx="{x}" cy="880" r="7" fill="#4a1018"/>'
    b += '<path d="M80 1080 L80 900 Q80 860 130 860 Q180 860 180 900 L180 1080Z" fill="#a03448" stroke="#2a0a10" stroke-width="7"/>'
    b += '<path d="M700 1080 L700 900 Q700 860 750 860 Q800 860 800 900 L800 1080Z" fill="#a03448" stroke="#2a0a10" stroke-width="7"/>'
    # frog hands gripping the chair top
    for hx in (338, 548):
        b += f'<circle cx="{hx}" cy="776" r="17" fill="{GREEN}" stroke="{INK}" stroke-width="9"/>'
    b += '<rect width="1920" height="1080" fill="url(#vigC)"/>'
    lines = [('A <span class="g">4D</span>', 250, 'w'), ('VISITOR', 205, 'w')]
    return page('#1c1838', svg(d, b), lines, outline='#0a0820', top=44)


for n, fn in (('A', make_A), ('B', make_B), ('C', make_C)):
    open(os.path.join(HERE, f'{n}.html'), 'w').write(fn())
print('ok')
