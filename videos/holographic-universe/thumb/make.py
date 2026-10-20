import sys, os, math, random
TOOLS = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', 'tools')
sys.path.insert(0, TOOLS)
from thumb_lib import *
from hands import hand
os.chdir(os.path.dirname(os.path.abspath(__file__)))
# v2 (2026-10-20): owner rejected v1 (Plato's cave / AREA NOT VOLUME / A FLAT CARD = 3D). Wish: "what if this world is a hologram?" + one Matrix homage.
FX = ('<filter id="bl"><feGaussianBlur stdDeviation="8"/></filter><filter id="bl2"><feGaussianBlur stdDeviation="26"/></filter>'
      '<filter id="bl3"><feGaussianBlur stdDeviation="3"/></filter><filter id="bl5"><feGaussianBlur stdDeviation="60"/></filter>')


def glyph(x, y, s, col, op, sw=2.4):
    """abstract code-rain glyph: 2-3 short strokes in a cell (never a real letter)"""
    pts = [(0, 0), (.5, 0), (1, 0), (0, .5), (.5, .5), (1, .5), (0, 1), (.5, 1), (1, 1)]
    d = ''
    for _ in range(random.choice([2, 3, 3])):
        a = random.choice(pts)   # only straight horizontal/vertical strokes: invented runes, never readable letters
        b = (a[0], 1 - a[1]) if random.random() < .5 else (1 - a[0], a[1])
        if a == b: b = (a[0], 0 if a[1] else 1)
        d += f'M{x + a[0] * s:.1f} {y + a[1] * s * 1.3:.1f}L{x + b[0] * s:.1f} {y + b[1] * s * 1.3:.1f}'
    if random.random() < .3:
        d += f'M{x + s * .5:.1f} {y + s * .2:.1f}h.1'
    return f'<path d="{d}" stroke="{col}" stroke-width="{sw}" stroke-linecap="round" fill="none" opacity="{op:.2f}"/>'


def person(x, y, h, col='#05070c', rim=None):
    """small standing figure seen from behind (no face), feet at (x, y), height h"""
    k = h / 100
    o = f'<g transform="translate({x} {y}) scale({k:.3f})" fill="{col}">'
    o += '<ellipse cx="0" cy="-88" rx="9" ry="10"/><path d="M-13 -76 Q0 -80 13 -76 L16 -40 Q0 -36 -16 -40Z"/>'
    o += '<path d="M-15 -74 L-21 -38 L-16 -37 L-10 -66Z M15 -74 L21 -38 L16 -37 L10 -66Z"/>'
    o += '<path d="M-13 -42 L-11 0 L-3 0 L-1 -36 L1 -36 L3 0 L11 0 L13 -42Z"/>'
    if rim:
        o += f'<path d="M9 -96 Q13 -88 9 -80 M13 -76 L16 -40 M13 -42 L11 0" stroke="{rim}" stroke-width="2.4" fill="none" opacity=".9"/>'
    return o + '</g>'


# ======================= A: IS THIS A HOLOGRAM?  (homage: The Matrix — two open hands offering a choice, inside falling green code) =======================
random.seed(11)
d = lin('mbg', [(0, '#010603'), (.6, '#03120a'), (1, '#010402')])
d += rad('mglow', 1290, 560, 820, [(0, '#2aff8a', .32), (.4, '#0c8a44', .14), (1, '#000', 0)])
d += rad('redg', 0, 0, 120, [(0, '#ff4a3a', .95), (.4, '#ff2a1a', .35), (1, '#ff0000', 0)])
d += rad('cubeg', 0, 0, 260, [(0, '#bff8ff', .85), (.35, '#4ad8ff', .35), (1, '#0080ff', 0)])
d += lin('pillR', [(0, '#ff8a7a'), (.45, '#e0221a'), (1, '#6a0606')])
d += lin('slv', [(0, '#0f1a13'), (1, '#030605')], 1, 0)
d += '<linearGradient id="cone" x1="0" y1="1" x2="0" y2="0"><stop offset="0" stop-color="#9ff4ff" stop-opacity=".55"/><stop offset="1" stop-color="#9ff4ff" stop-opacity="0"/></linearGradient>'
d += '<linearGradient id="fadeTL" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#010402" stop-opacity=".82"/><stop offset=".5" stop-color="#010402" stop-opacity=".45"/><stop offset=".62" stop-color="#010402" stop-opacity="0"/></linearGradient>'
d += FX
b = '<rect width="1920" height="1080" fill="url(#mbg)"/>'
# far layer of code rain (small, dim), then near layer (bigger, brighter heads)
for layer, (ncol, gs, op0) in enumerate([(70, 22, .30), (34, 34, .75)]):
    for c in range(ncol):
        x = random.uniform(0, 1900); head = random.uniform(150, 1100); n = random.randint(10, 26)
        for i in range(n):
            y = head - i * gs * 1.45
            if y < -40: break
            f = 1 - i / n
            col = '#eaffef' if i == 0 else ('#7dffae' if i < 3 else '#1fd16a')
            o = op0 * (1 if i == 0 else f * .85)
            if x < 1000 and y < 520: o *= .45     # calmer behind the title
            b += glyph(x, y, gs * .72, col, o, 1.6 + layer * 1.4)
        if layer == 1:
            b += f'<circle cx="{x + gs * .36:.0f}" cy="{head + gs * .4:.0f}" r="{gs * .9:.0f}" fill="#9dffc0" opacity=".25" filter="url(#bl3)"/>'
b += '<rect width="1920" height="1080" fill="url(#mglow)"/>'
# the "real" city skyline at the back, dissolving upward into code
sky = ''
x = 560
while x < 1960:
    w = random.randint(60, 150); h = random.randint(120, 360)
    top = 760 - h
    sky += f'<rect x="{x}" y="{top}" width="{w}" height="{h + 40}" fill="#04140b"/>'
    sky += f'<path d="M{x} {top} h{w}" stroke="#36ff8a" stroke-width="2" opacity=".55"/>'
    for wy in range(top + 20, 760, 26):    # windows
        for wx in range(x + 10, x + w - 10, 20):
            if random.random() < .35:
                sky += f'<rect x="{wx}" y="{wy}" width="8" height="12" fill="#5dff9c" opacity="{random.uniform(.25, .7):.2f}"/>'
    for _ in range(int(w / 9)):            # roof breaking up into green squares
        bx = x + random.uniform(0, w); by = top - random.expovariate(1 / 70)
        s = random.choice([5, 7, 10])
        sky += f'<rect x="{bx:.0f}" y="{by:.0f}" width="{s}" height="{s}" fill="#4dff94" opacity="{random.uniform(.25, .8):.2f}"/>'
    x += w + random.randint(4, 20)
b += sky
b += '<path d="M0 760 L1920 760 L1920 1080 L0 1080Z" fill="#010603" opacity=".9"/>'
b += '<path d="M0 760 L1920 760" stroke="#2aff7a" stroke-width="3" opacity=".5"/>'
for k in range(1, 9):   # glowing floor grid
    y = 760 + 320 * (k / 8) ** 1.8
    b += f'<path d="M0 {y:.0f} L1920 {y:.0f}" stroke="#1fd16a" stroke-width="2" opacity="{.12 + k * .02:.2f}"/>'
for k in range(-12, 13):
    b += f'<path d="M1290 760 L{1290 + k * 240} 1080" stroke="#1fd16a" stroke-width="2" opacity=".16"/>'
b += '<rect width="1920" height="1080" fill="url(#fadeTL)"/>'
# ---- two forearms in dark coat sleeves, hands open, palms to the viewer ----
HL = (1060, 880, -14)   # wrist x, y, angle (viewer's left hand = person's right)
HR = (1560, 880, 14)
SZ = 200
for (wx, wy, ang), sgn in ((HL, -1), (HR, 1)):
    a = math.radians(ang)
    # sleeve: from the wrist down and outward to the frame bottom
    bx = wx - math.sin(a) * 330; by = wy + math.cos(a) * 330
    px, py = math.cos(a), math.sin(a)
    w0, w1 = 92, 150
    pts = [(wx - px * w0, wy - py * w0), (wx + px * w0, wy + py * w0), (bx + px * w1, by + py * w1), (bx - px * w1, by - py * w1)]
    b += f'<ellipse cx="{wx}" cy="{wy - 180}" rx="260" ry="300" fill="#2aff8a" opacity=".18" filter="url(#bl5)"/>'
    b += '<path d="M' + ' L'.join(f'{p[0]:.0f} {p[1]:.0f}' for p in pts) + 'Z" fill="url(#slv)" stroke="#000" stroke-width="6"/>'
    # rim light on the outer edge of each sleeve + cuff
    o0 = pts[0] if sgn < 0 else pts[1]; o1 = pts[3] if sgn < 0 else pts[2]
    b += f'<path d="M{o0[0]:.0f} {o0[1]:.0f} L{o1[0]:.0f} {o1[1]:.0f}" stroke="#5dff9c" stroke-width="5" opacity=".7"/>'
    b += f'<path d="M{pts[0][0]:.0f} {pts[0][1]:.0f} L{pts[1][0]:.0f} {pts[1][1]:.0f}" stroke="#1a2a20" stroke-width="22"/>'
    for k in range(3):   # leather folds
        t = .3 + k * .22
        cx_, cy_ = wx + (bx - wx) * t, wy + (by - wy) * t
        b += f'<path d="M{cx_ - px * 60:.0f} {cy_ - py * 60:.0f} q{px * 60 + 10:.0f} {py * 60 + 14:.0f} {px * 120:.0f} {py * 120:.0f}" stroke="#2a3a30" stroke-width="4" fill="none" opacity=".7"/>'
b += hand(HL[0], HL[1], HL[2], SZ, side='R', view='palm', pose='open', skin='#d2a483', line='#071209')
b += hand(HR[0], HR[1], HR[2], SZ, side='L', view='palm', pose='open', skin='#d2a483', line='#071209')
# green light washing over the hands from the code (soft overlay on the outer edges)
for (wx, wy, ang), sgn in ((HL, -1), (HR, 1)):
    a = math.radians(ang); cx_ = wx + math.sin(a) * SZ * .55; cy_ = wy - math.cos(a) * SZ * .55
    b += f'<ellipse cx="{cx_ + sgn * 120:.0f}" cy="{cy_:.0f}" rx="70" ry="200" fill="#2aff8a" opacity=".18" filter="url(#bl)"/>'
# red pill on the left palm
a = math.radians(HL[2]); pcx = HL[0] + math.sin(a) * SZ * .5; pcy = HL[1] - math.cos(a) * SZ * .5
b += f'<g transform="translate({pcx:.0f} {pcy:.0f})"><circle r="120" fill="url(#redg)"/>'
b += '<g transform="rotate(-32)"><g transform="scale(1.25)"><rect x="-58" y="-25" width="116" height="50" rx="25" fill="#3a0404" transform="translate(4 6)" opacity=".5"/>'
b += '<rect x="-58" y="-25" width="116" height="50" rx="25" fill="url(#pillR)" stroke="#2a0202" stroke-width="4"/>'
b += '<path d="M-44 -13 Q-10 -20 34 -14" stroke="#ffd6cf" stroke-width="7" stroke-linecap="round" fill="none" opacity=".85"/>'
b += '<path d="M0 -24 V24" stroke="#7a0a08" stroke-width="3" opacity=".6"/></g></g></g>'
# hologram cube projected from the right palm
a = math.radians(HR[2]); hx = HR[0] + math.sin(a) * SZ * .5; hy = HR[1] - math.cos(a) * SZ * .5
cx_, cy_ = hx + 20, hy - 480
b += f'<path d="M{hx - 40:.0f} {hy:.0f} L{cx_ - 170:.0f} {cy_ + 90:.0f} L{cx_ + 170:.0f} {cy_ + 90:.0f} L{hx + 40:.0f} {hy:.0f}Z" fill="url(#cone)" opacity=".75"/>'
b += f'<circle cx="{cx_}" cy="{cy_}" r="260" fill="url(#cubeg)"/>'
b += f'<ellipse cx="{hx:.0f}" cy="{hy:.0f}" rx="46" ry="16" fill="#dffbff" opacity=".9" filter="url(#bl3)"/>'
# isometric wireframe cube with a tiny lit world inside
S = 150
V = {}
for i, (X, Y, Z) in enumerate([(x_, y_, z_) for x_ in (-1, 1) for y_ in (-1, 1) for z_ in (-1, 1)]):
    ry_ = math.radians(28); rx_ = math.radians(-22)
    X1 = X * math.cos(ry_) + Z * math.sin(ry_); Z1 = -X * math.sin(ry_) + Z * math.cos(ry_)
    Y1 = Y * math.cos(rx_) - Z1 * math.sin(rx_)
    V[(X, Y, Z)] = (cx_ + X1 * S * .8, cy_ + Y1 * S * .8)
edges = [(p, q) for p in V for q in V if p < q and sum(abs(p[i] - q[i]) for i in range(3)) == 2]
cube = ''
for p, q in edges:
    cube += f'<path d="M{V[p][0]:.0f} {V[p][1]:.0f} L{V[q][0]:.0f} {V[q][1]:.0f}" stroke="#7fe8ff" stroke-width="16" opacity=".35" filter="url(#bl3)"/>'
    cube += f'<path d="M{V[p][0]:.0f} {V[p][1]:.0f} L{V[q][0]:.0f} {V[q][1]:.0f}" stroke="#e6fdff" stroke-width="5" stroke-linecap="round"/>'
for k in range(1, 4):   # faint scanlines on the faces
    t = k / 4
    a0 = V[(-1, -1, 1)]; a1 = V[(-1, 1, 1)]; b0 = V[(1, -1, 1)]; b1 = V[(1, 1, 1)]
    cube += f'<path d="M{a0[0] + (a1[0] - a0[0]) * t:.0f} {a0[1] + (a1[1] - a0[1]) * t:.0f} L{b0[0] + (b1[0] - b0[0]) * t:.0f} {b0[1] + (b1[1] - b0[1]) * t:.0f}" stroke="#9ff4ff" stroke-width="2" opacity=".5"/>'
# glowing planet inside
cube += f'<circle cx="{cx_}" cy="{cy_}" r="52" fill="#3ab8ff" opacity=".85"/><circle cx="{cx_ - 14}" cy="{cy_ - 16}" r="26" fill="#d8f8ff" opacity=".55" filter="url(#bl3)"/>'
cube += f'<path d="M{cx_ - 50} {cy_ + 6} Q{cx_} {cy_ - 16} {cx_ + 50} {cy_ - 2}" stroke="#bff6ff" stroke-width="3" fill="none" opacity=".8"/>'
cube += f'<ellipse cx="{cx_}" cy="{cy_}" rx="86" ry="20" fill="none" stroke="#f2d27a" stroke-width="4" opacity=".8" transform="rotate(-12 {cx_} {cy_})"/>'
b += cube
for _ in range(40):   # hologram pixels drifting off the cube
    ang = random.uniform(0, 6.28); r = random.uniform(150, 280)
    s = random.choice([4, 6, 8])
    b += f'<rect x="{cx_ + math.cos(ang) * r:.0f}" y="{cy_ + math.sin(ang) * r * .8:.0f}" width="{s}" height="{s}" fill="#bff6ff" opacity="{random.uniform(.3, .9):.2f}"/>'
b += spark(cx_ + 180, cy_ - 150, 22, '#e6fdff') + spark(pcx - 100, pcy - 110, 18, '#ffd6cf') + spark(1820, 300, 16, '#d6ffe4')
open('A.html', 'w', encoding='utf-8').write(page('#010402', svg(d, b), [('IS THIS A', 130, 'w'), ('HOLOGRAM?', 178, 'y')], '#010402', top=70))


# ======================= B: THE WORLD MIGHT BE PROJECTED  (intuitive: a dusk street whose far half turns into glowing wireframe, inside a thin glowing shell) =======================
random.seed(23)
VPX, VPY, F = 760, 600, 300


def P3(X, Y, Z):
    return VPX + F * X / Z, VPY + F * Y / Z


d = lin('skyB', [(0, '#141a44'), (.45, '#5a3a78'), (.8, '#e0784a'), (1, '#ffb070')])
d += rad('vpg', VPX, VPY, 700, [(0, '#e9fdff', 1), (.12, '#9ff0ff', .7), (.4, '#3ab8e0', .2), (1, '#000', 0)])
d += lin('road', [(0, '#3a2a3a'), (1, '#0c0812')])
d += lin('facN', [(0, '#7a4a3a'), (1, '#2a1620')])
d += lin('facF', [(0, '#a8604a'), (1, '#3a2030')])
d += FX
b = '<rect width="1920" height="1080" fill="url(#skyB)"/>'
for _ in range(60):
    b += f'<circle cx="{random.uniform(0, 1920):.0f}" cy="{random.uniform(0, 300):.0f}" r="{random.choice([1.2, 1.8, 2.4])}" fill="#fff" opacity="{random.uniform(.2, .7):.2f}"/>'
# the thin glowing boundary shell around the whole world: a huge sphere edge across the sky, tiled with faint data cells
SCX, SCY, SR = 980, 1700, 1640
b += f'<circle cx="{SCX}" cy="{SCY}" r="{SR}" fill="none" stroke="#7fe8ff" stroke-width="60" opacity=".18" filter="url(#bl2)"/>'
for k in range(70):   # cells along the shell
    th = math.radians(-160 + k * 140 / 70)
    for j in range(3):
        rr = SR - 10 - j * 30
        x, y = SCX + math.cos(th) * rr, SCY + math.sin(th) * rr
        if -40 < x < 1960 and y > -40 and random.random() < .7:
            b += f'<rect x="{x - 9:.0f}" y="{y - 9:.0f}" width="18" height="18" fill="{random.choice(["#7fe8ff", "#bff6ff", "#f2d27a"])}" opacity="{random.uniform(.15, .6) * (1 - j * .25):.2f}" transform="rotate({math.degrees(th) + 90:.0f} {x:.0f} {y:.0f})"/>'
b += f'<circle cx="{SCX}" cy="{SCY}" r="{SR}" fill="none" stroke="#e6fdff" stroke-width="5" opacity=".9"/>'
b += f'<circle cx="{SCX}" cy="{SCY}" r="{SR - 70}" fill="none" stroke="#7fe8ff" stroke-width="2" opacity=".35" stroke-dasharray="6 14"/>'
b += '<rect width="1920" height="1080" fill="url(#vpg)"/>'
# road + sidewalks
b += f'<path d="M{VPX} {VPY} L2200 1080 L-700 1080Z" fill="url(#road)"/>'
for k in range(1, 14):   # road grid: solid near, glowing far
    Z = 1.2 * 1.32 ** k
    xl, y = P3(-5, 1.6, Z); xr, _ = P3(6, 1.6, Z)
    b += f'<path d="M{xl:.0f} {y:.0f} L{xr:.0f} {y:.0f}" stroke="#7fe8ff" stroke-width="{max(1, 3 - k * .15):.1f}" opacity="{min(.8, .1 + k * .06):.2f}"/>'
for X in (-5, -2.5, 0, 2.5, 6):
    x0, y0 = P3(X, 1.6, 1.1)
    b += f'<path d="M{x0:.0f} {y0:.0f} L{VPX} {VPY}" stroke="#7fe8ff" stroke-width="2" opacity=".3"/>'
for k in range(10):   # centre dashes
    z0 = 1.3 * 1.4 ** k; z1 = z0 * 1.18
    a0 = P3(0, 1.6, z0); a1 = P3(0, 1.6, z1)
    b += f'<path d="M{a0[0]:.0f} {a0[1]:.0f} L{a1[0]:.0f} {a1[1]:.0f}" stroke="#ffd98a" stroke-width="{max(2, 14 / z0 * 1.4):.1f}" opacity=".8"/>'
# left side: low dark wall with street lamps (kept calm under the title)
for Z in (2.2, 3.4, 5.2, 8, 12, 18):
    x0, y0 = P3(-5, 1.6, Z); x1, y1 = P3(-5, -3.2, Z)
    b += f'<path d="M{x0:.0f} {y0:.0f} L{x1:.0f} {y1:.0f}" stroke="#0c0812" stroke-width="{max(2, 14 / Z):.0f}"/>'
    b += f'<circle cx="{x1:.0f}" cy="{y1:.0f}" r="{max(4, 40 / Z):.0f}" fill="#ffd98a"/><circle cx="{x1:.0f}" cy="{y1:.0f}" r="{max(10, 120 / Z):.0f}" fill="#ffb060" opacity=".35" filter="url(#bl)"/>'
wl = [P3(-5, 1.6, 1.0), P3(-5, 0.4, 1.0), P3(-5, 0.4, 60), P3(-5, 1.6, 60)]
b += '<path d="M' + ' L'.join(f'{p[0]:.0f} {p[1]:.0f}' for p in wl) + 'Z" fill="#1a1020"/>'
# right side: buildings from far (wireframe) to near (solid)
blds = []
Z = 1.0
while Z < 70:
    dz = Z * random.uniform(.32, .5); blds.append((Z, Z + dz, random.uniform(4.5, 8))); Z += dz * random.uniform(1.0, 1.12)
for Z1, Z2, H in reversed(blds):
    w = max(0., min(1., (Z1 - 2.3) / 3.2))     # 0 = solid, 1 = pure wireframe
    side = [P3(6, 1.6, Z1), P3(6, -H, Z1), P3(6, -H, Z2), P3(6, 1.6, Z2)]
    front = [P3(6, 1.6, Z1), P3(6, -H, Z1), P3(16, -H, Z1), P3(16, 1.6, Z1)]
    top = [P3(6, -H, Z1), P3(6, -H, Z2), P3(16, -H, Z2), P3(16, -H, Z1)]
    pth = lambda ps: 'M' + ' L'.join(f'{p[0]:.0f} {p[1]:.0f}' for p in ps) + 'Z'
    if w < 1:
        b += f'<g opacity="{1 - w:.2f}"><path d="{pth(front)}" fill="url(#facN)"/><path d="{pth(side)}" fill="url(#facF)"/>'
        b += f'<path d="{pth(side)}" fill="none" stroke="#ffcf9a" stroke-width="2" opacity=".5"/>'
        # windows on the street-facing side
        for zi in range(1, 6):
            za = Z1 + (Z2 - Z1) * (zi - .75) / 5.2; zb = za + (Z2 - Z1) * .11
            for yy in [1.6 - 1.2 - 1.6 * k for k in range(int(H / 1.6))]:
                q = [P3(6, yy, za), P3(6, yy - .8, za), P3(6, yy - .8, zb), P3(6, yy, zb)]
                lit = random.random() < .55
                b += f'<path d="{pth(q)}" fill="{"#ffd98a" if lit else "#2a1a2a"}" opacity="{.9 if lit else .8}"/>'
        b += '</g>'
    if w > 0:
        col = '#9ff0ff'
        g = f'<g opacity="{w:.2f}" fill="none" stroke="{col}">'
        g += f'<path d="{pth(side)}" stroke-width="3"/><path d="{pth(front)}" stroke-width="3"/><path d="{pth(top)}" stroke-width="2"/>'
        for k in range(1, 6):
            zz = Z1 + (Z2 - Z1) * k / 6; a0 = P3(6, 1.6, zz); a1 = P3(6, -H, zz)
            g += f'<path d="M{a0[0]:.0f} {a0[1]:.0f} L{a1[0]:.0f} {a1[1]:.0f}" stroke-width="1.5" opacity=".7"/>'
        for yy in [1.6 - 1.6 * k for k in range(1, int(H / 1.6) + 1)]:
            a0 = P3(6, yy, Z1); a1 = P3(6, yy, Z2)
            g += f'<path d="M{a0[0]:.0f} {a0[1]:.0f} L{a1[0]:.0f} {a1[1]:.0f}" stroke-width="1.5" opacity=".7"/>'
        b += g + '</g>'
        # pixels breaking off the roof and drifting up toward the shell
        for _ in range(int(16 * w + 6)):
            zz = random.uniform(Z1, Z2); px_, py_ = P3(random.uniform(6, 10), -H, zz)
            py_ -= random.expovariate(1 / 90); s = random.choice([5, 8, 11, 14])
            b += f'<rect x="{px_:.0f}" y="{py_:.0f}" width="{s}" height="{s}" fill="{random.choice(["#bff6ff", "#7fe8ff", "#f2d27a"])}" opacity="{random.uniform(.4, .95):.2f}"/>'
# transition band: the solid near buildings already flaking into pixels at their far edge
for _ in range(120):
    zz = random.uniform(2.0, 3.6); X = 6; Y = random.uniform(-7, 1.4)
    px_, py_ = P3(X, Y, zz); s = random.choice([6, 9, 12])
    b += f'<rect x="{px_ + random.uniform(-10, 10):.0f}" y="{py_:.0f}" width="{s}" height="{s}" fill="{random.choice(["#9ff0ff", "#bff6ff", "#ffd98a"])}" opacity="{random.uniform(.35, .9):.2f}"/>'
# light streams from the far end toward the shell
for k in range(9):
    ang = math.radians(-150 + k * 15)
    ex, ey = VPX + math.cos(ang) * 1400, VPY + math.sin(ang) * 1400
    b += f'<path d="M{VPX} {VPY} L{ex:.0f} {ey:.0f}" stroke="#bff6ff" stroke-width="3" opacity=".10"/>'
b += f'<circle cx="{VPX}" cy="{VPY}" r="70" fill="#ffffff" opacity=".9" filter="url(#bl)"/>'
# small figure on the road, rim-lit by the far glow
b += f'<ellipse cx="660" cy="922" rx="46" ry="9" fill="#000" opacity=".5"/>' + person(660, 920, 150, '#07040c', '#bff6ff')
b += spark(1500, 140, 24, '#e6fdff') + spark(1180, 250, 16) + spark(1760, 420, 18, '#e6fdff')
open('B.html', 'w', encoding='utf-8').write(page('#141a44', svg(d, b), [('THE WORLD', 130, 'w'), ('MIGHT BE', 130, 'w'), ('PROJECTED', 160, 'y')], '#0a0618', top=50))


# ======================= C: 3D SPACE = 2D?  (intuitive: a whole galaxy projected up from a thin glowing plate) =======================
random.seed(37)
GX, GY, GR = 1330, 430, 470
d = lin('bgC', [(0, '#07041a'), (.6, '#160a36'), (1, '#05020e')])
d += rad('coreC', GX, GY, 260, [(0, '#fffbe8', 1), (.15, '#ffe6a8', .9), (.45, '#e08acf', .3), (1, '#000', 0)])
d += rad('haloC', GX, GY, 700, [(0, '#b06ae0', .35), (.5, '#5a2a9a', .12), (1, '#000', 0)])
d += rad('plateC', 1330, 880, 460, [(0, '#fff2c8', 1), (.4, '#f2d27a', .85), (.8, '#c07a3a', .6), (1, '#5a2a1a', .4)])
d += '<linearGradient id="beamG" x1="0" y1="1" x2="0" y2="0"><stop offset="0" stop-color="#ffe6a8" stop-opacity=".55"/><stop offset=".6" stop-color="#d8a8ff" stop-opacity=".16"/><stop offset="1" stop-color="#d8a8ff" stop-opacity="0"/></linearGradient>'
d += FX
b = '<rect width="1920" height="1080" fill="url(#bgC)"/>' + stars(260, 1000, 0, '#efe8ff', .6, 0)
b += '<rect width="1920" height="1080" fill="url(#haloC)"/>'
# floor: dark reflective plane with a faint grid
b += '<path d="M0 820 L1920 820 L1920 1080 L0 1080Z" fill="#06030f" opacity=".85"/>'
for k in range(1, 9):
    y = 820 + 260 * (k / 8) ** 1.7
    b += f'<path d="M0 {y:.0f} L1920 {y:.0f}" stroke="#8a5ad0" stroke-width="1.5" opacity="{.08 + k * .02:.2f}"/>'
for k in range(-14, 15):
    b += f'<path d="M1330 820 L{1330 + k * 200} 1080" stroke="#8a5ad0" stroke-width="1.5" opacity=".1"/>'
# light cone from the plate up to the galaxy
PX, PY, PRX, PRY = 1330, 880, 430, 84
b += f'<path d="M{PX - PRX} {PY} L{GX - GR * .98:.0f} {GY + 10} L{GX + GR * .98:.0f} {GY + 10} L{PX + PRX} {PY}Z" fill="url(#beamG)"/>'
for k in range(46):   # thin rising light lines from the plate's bits
    x = PX + random.uniform(-PRX * .95, PRX * .95); y = PY + random.uniform(-PRY * .5, PRY * .5)
    tx = GX + (x - PX) * 1.08; ty = GY + random.uniform(-60, 80)
    b += f'<path d="M{x:.0f} {y:.0f} L{tx:.0f} {ty:.0f}" stroke="{random.choice(["#ffe6a8", "#e6c8ff"])}" stroke-width="{random.choice([1.5, 2, 3])}" opacity="{random.uniform(.12, .35):.2f}"/>'
# the galaxy: tilted spiral of stars and dust
G = f'<g transform="translate({GX} {GY}) rotate(-12) scale(1 .42)">'
G += f'<ellipse rx="{GR}" ry="{GR}" fill="#8a4ad0" opacity=".25" filter="url(#bl5)"/>'
for arm in range(2):
    for i in range(900):
        t = i / 900; th = arm * math.pi + t * 3.3 * math.pi
        r = 40 + t * (GR - 40) ** 1 * .98
        sc = 6 + 16 * t
        x = math.cos(th) * r + random.gauss(0, 1) * sc; y = math.sin(th) * r + random.gauss(0, 1) * sc
        col = random.choice(['#ffe9c8', '#e6c8ff', '#bfe0ff', '#ffffff', '#ff9ad8'])
        G += f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{random.choice([1.6, 2.2, 3, 4]) * (1.3 - t * .5):.1f}" fill="{col}" opacity="{random.uniform(.35, 1):.2f}"/>'
    for i in range(60):   # dust/glow clumps along the arms
        t = random.random(); th = arm * math.pi + t * 3.3 * math.pi; r = 40 + t * (GR - 40) + random.gauss(0, 8)
        G += f'<circle cx="{math.cos(th) * r:.0f}" cy="{math.sin(th) * r:.0f}" r="{random.uniform(12, 34):.0f}" fill="{random.choice(["#ff7ac8", "#a86aff", "#7ab8ff"])}" opacity=".22" filter="url(#bl)"/>'
G += '</g>'
b += G
b += f'<ellipse cx="{GX}" cy="{GY}" rx="200" ry="95" fill="#e08acf" opacity=".45" filter="url(#bl2)" transform="rotate(-12 {GX} {GY})"/>'
b += f'<ellipse cx="{GX}" cy="{GY}" rx="120" ry="58" fill="#ffe6a8" opacity=".9" filter="url(#bl)" transform="rotate(-12 {GX} {GY})"/>'
b += f'<ellipse cx="{GX}" cy="{GY}" rx="46" ry="26" fill="#fffbe8" filter="url(#bl3)"/>'
# hologram scan lines across the galaxy
for k in range(-6, 7):
    y = GY + k * 34
    b += f'<path d="M{GX - 420} {y} L{GX + 420} {y}" stroke="#e6c8ff" stroke-width="1.5" opacity=".10"/>'
# the plate: thin glowing disc covered in tiny data cells (the "boundary")
b += f'<ellipse cx="{PX}" cy="{PY + 22}" rx="{PRX + 20}" ry="{PRY + 18}" fill="#1a0a2a" stroke="#6a3a9a" stroke-width="3"/>'
b += f'<ellipse cx="{PX}" cy="{PY + 10}" rx="{PRX + 8}" ry="{PRY + 6}" fill="#3a1a3a"/>'
b += f'<ellipse cx="{PX}" cy="{PY}" rx="{PRX}" ry="{PRY}" fill="url(#plateC)"/>'
cells = ''
for i in range(-26, 27):
    for j in range(-6, 7):
        u, v = i / 26, j / 6
        if u * u + v * v < .92 and random.random() < .55:
            x = PX + u * PRX; y = PY + v * PRY
            cells += f'<rect x="{x - 7:.0f}" y="{y - 3:.0f}" width="12" height="5" fill="{random.choice(["#fffbe8", "#7a3a1a", "#ffffff", "#c07a3a"])}" opacity="{random.uniform(.3, .85):.2f}"/>'
b += cells
b += f'<ellipse cx="{PX}" cy="{PY}" rx="{PRX}" ry="{PRY}" fill="none" stroke="#fff6d6" stroke-width="4"/>'
b += f'<ellipse cx="{PX}" cy="{PY}" rx="{PRX + 60}" ry="{PRY + 26}" fill="#ffd98a" opacity=".22" filter="url(#bl2)"/>'
# reflection of the glow on the floor
b += f'<ellipse cx="{PX}" cy="{PY + 120}" rx="{PRX + 80}" ry="40" fill="#f2b06a" opacity=".18" filter="url(#bl2)"/>'
# small figure at the plate's edge looking up, for scale
b += f'<ellipse cx="870" cy="952" rx="48" ry="7" fill="#000" opacity=".6"/>' + person(870, 950, 170, '#0a0618', '#ffe6a8')
b += spark(1780, 160, 24, '#fff6d6') + spark(980, 640, 14, '#e6c8ff') + spark(1700, 640, 16, '#fff6d6')
open('C.html', 'w', encoding='utf-8').write(page('#07041a', svg(d, b), [('3D SPACE', 150, 'w'), ('= 2D?', 250, 'y')], '#05020e', top=60))
print('ok')
