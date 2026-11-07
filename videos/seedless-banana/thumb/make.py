# Thumbnails A-C for seedless-banana (guideline 16-6 / 16-8, brief tools/briefs/thumb_art.md). Run: python3 videos/seedless-banana/thumb/make.py
# A  TR4 / IS SPREADING      homage: the Alien (1979) egg poster: one huge Cavendish standing on a dark perspective grid, a glowing green
#                            crack and creeping fungus; frog in a hazmat suit with a torch. Script S55-S60: "TR4 ... has since spread across Asia,
#                            Australia ..."; "in August 2019 ... TR4 was officially detected in Colombia".
# B  OUR BANANAS / WHY NO / SEEDS?     intuitive: a wild banana cut open lengthwise, packed with hard black seeds, in the jungle; explorer frog holds one up.
#                            Script S12-S13: "packed to the brim with dozens of hard, pebble-like seeds ... roughly the size of pea gravel".
# C  ARE BANANAS / RADIOACTIVE?  intuitive: a glowing bunch of bananas giving off tiny decay sparks, lab frog with a ticking Geiger counter.
#                            Script S63-S66: "bananas are naturally radioactive" (potassium-40, harmless).
import os, sys, math, random
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', '..', 'tools'))
from thumb_lib import page, svg, lin, rad, spark

INK = '#1d2b1c'; GREEN = '#6aa55a'; DARKG = '#4d8a4a'; BELLY = '#9cc98a'
FILTERS = ''.join(f'<filter id="b{n}" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="{n}"/></filter>' for n in (2, 4, 8, 14, 26, 50, 90))


def P(pts):
    return ' '.join(f'{a:.1f},{b:.1f}' for a, b in pts)


# ---------------- mascot frog (tools/assets/frog.svg body), posable (same helper as deep-sea-giants) ----------------
def limb(d, w=7.5, wi=3.4):
    return f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="{w}"/><path d="{d}" fill="none" stroke="{GREEN}" stroke-width="{wi}"/>'


def end_of(d):
    n = [float(v) for v in d.replace('M', ' ').replace('q', ' ').split()]
    return n[0] + n[-2], n[1] + n[-1]


def frog(x, y, s, rot=0, flip=False, look=(0, 0), mouth='O', armL=None, armR=None, helmet=False,
         brows=True, back="", front="", shadow=False, mid="", top=""):
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
    _d = math.hypot(1 + lx, ly)  # keep pupil inside the eye white (eyecheck, guideline 16-9)
    if _d > 6.9: _k = 6.9 / _d; lx, ly = (1 + lx) * _k - 1, ly * _k
    for ex in (-10, 22):
        g.append(f'<circle cx="{ex}" cy="-66" r="13.5" fill="#f4f5ea" stroke-width="3.2"/>')
        g.append(f'<circle cx="{ex + 1 + lx}" cy="{-66 + ly}" r="4.4" fill="{INK}" stroke="none"/>')
        g.append(f'<circle cx="{ex + 2.4 + lx}" cy="{-67.6 + ly}" r="1.5" fill="#fff" stroke="none"/>')
    if brows:
        g.append('<path d="M-22 -88 q12 -9 24 -1 M10 -89 q12 -8 24 1" fill="none" stroke-width="3.4"/>')
    if mouth == 'O':
        g.append('<ellipse cx="6" cy="-38" rx="10" ry="12" fill="#7a2f33" stroke-width="3"/><ellipse cx="6" cy="-31" rx="6" ry="4" fill="#e07b7b" stroke="none"/>')
    else:
        g.append('<ellipse cx="6" cy="-41" rx="6" ry="7.5" fill="#7a2f33" stroke-width="3"/>')
    g.append('<ellipse cx="-18" cy="-48" rx="5" ry="3" fill="#e98a8a" stroke="none" opacity=".55"/><ellipse cx="30" cy="-48" rx="5" ry="3" fill="#e98a8a" stroke="none" opacity=".55"/>')
    g.append(top)
    if helmet:
        g.append('<circle cx="6" cy="-58" r="45" fill="#d8ffd0" fill-opacity=".12" stroke="#effff0" stroke-width="3.4" stroke-opacity=".95"/>')
        g.append('<path d="M-26 -82 q12 -18 32 -21" fill="none" stroke="#fff" stroke-width="5" opacity=".8"/>')
        g.append('<ellipse cx="6" cy="-16" rx="40" ry="9" fill="#3a3a30" stroke-width="3.2"/>')
    for a in (armL or 'M-34 -22 q-14 6 -16 22', armR or 'M38 -22 q14 6 16 22'):
        g.append(limb(a)); ex_, ey_ = end_of(a)
        g.append(f'<circle cx="{ex_:.1f}" cy="{ey_:.1f}" r="5.6" fill="{GREEN}" stroke-width="3"/>')
    g.append(front); g.append('</g>')
    return ''.join(g)


# ---------------- banana geometry ----------------
def bez(p, t):
    (x0, y0), (x1, y1), (x2, y2), (x3, y3) = p; u = 1 - t
    return (u ** 3 * x0 + 3 * u * u * t * x1 + 3 * u * t * t * x2 + t ** 3 * x3,
            u ** 3 * y0 + 3 * u * u * t * y1 + 3 * u * t * t * y2 + t ** 3 * y3)


def frame(p, wmax, n=80, prof=None):
    """centreline points, unit normals, half-widths. t=0 stem end, t=1 tip."""
    prof = prof or (lambda t: .30 + .70 * math.sin(math.pi * min(1, max(0, t))) ** .55)
    C = [bez(p, i / n) for i in range(n + 1)]; N = []; W = []
    for i in range(n + 1):
        a = C[max(i - 1, 0)]; b = C[min(i + 1, n)]
        dx, dy = b[0] - a[0], b[1] - a[1]; l = math.hypot(dx, dy) or 1
        N.append((-dy / l, dx / l)); W.append(wmax * prof(i / n))
    return C, N, W


def off(F, u, i0=0, i1=None):
    C, N, W = F; i1 = len(C) if i1 is None else i1
    return [(C[i][0] + N[i][0] * W[i] * u, C[i][1] + N[i][1] * W[i] * u) for i in range(i0, i1)]


def strip(F, u0, u1, fill, extra=''):
    a = off(F, u0); b = off(F, u1)[::-1]
    return f'<path d="M{P(a)} L{P(b)}Z" fill="{fill}" {extra}/>'


def banana(p, wmax, pal, line='#3a2a08', lw=6, stem=True, spots=None, rnd=None, glow=None):
    """faceted ripe banana: pal = (shadow, mid, light, rim)."""
    F = frame(p, wmax); C, N, W = F
    o = ''
    if glow:
        o += f'<path d="M{P(off(F, 1.25))} L{P(off(F, -1.25)[::-1])}Z" fill="{glow}" opacity=".55" filter="url(#b26)"/>'
    out = f'M{P(off(F, 1))} L{P(off(F, -1)[::-1])}Z'
    o += f'<path d="{out}" fill="{pal[1]}" stroke="{line}" stroke-width="{lw * 2}" stroke-linejoin="round"/>'
    o += strip(F, -1, -.55, pal[0]) + strip(F, -.55, -.05, pal[1]) + strip(F, -.05, .5, pal[2]) + strip(F, .5, 1, pal[1])
    o += strip(F, .78, 1, pal[3], 'opacity=".55"')
    for u in (-.55, -.05, .5):   # ridges
        o += f'<polyline points="{P(off(F, u, 3, len(C) - 3))}" fill="none" stroke="{line}" stroke-width="{lw * .45:.1f}" opacity=".35"/>'
    o += f'<polyline points="{P(off(F, .22, 8, len(C) - 12))}" fill="none" stroke="#fffbe6" stroke-width="{wmax * .12:.0f}" stroke-linecap="round" opacity=".55"/>'
    if spots:
        for _ in range(spots):
            i = rnd.randint(6, len(C) - 6); u = rnd.uniform(-.85, .85)
            x, y = C[i][0] + N[i][0] * W[i] * u, C[i][1] + N[i][1] * W[i] * u
            o += f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{rnd.uniform(2, 6):.1f}" ry="{rnd.uniform(1.5, 4):.1f}" fill="#5a3c10" opacity="{rnd.uniform(.3, .7):.2f}"/>'
    o += f'<path d="{out}" fill="none" stroke="{line}" stroke-width="{lw}" stroke-linejoin="round"/>'
    # blunt dark tip
    tx, ty = C[-1]; nx, ny = N[-1]; tw = W[-1]
    dx, dy = ny, -nx  # tangent forward
    o += (f'<path d="M{tx + nx * tw:.1f} {ty + ny * tw:.1f} Q{tx + dx * tw * 1.3:.1f} {ty + dy * tw * 1.3:.1f} {tx - nx * tw:.1f} {ty - ny * tw:.1f}Z" '
          f'fill="#3a2a14" stroke="{line}" stroke-width="{lw * .8:.1f}" stroke-linejoin="round"/>')
    if stem:
        sx, sy = C[0]; nx, ny = N[0]; dx, dy = -ny, nx  # backward tangent
        L = wmax * 1.05; sw = W[0] * .62
        q = [(sx + nx * sw, sy + ny * sw), (sx + dx * L + nx * sw * .8, sy + dy * L + ny * sw * .8),
             (sx + dx * L - nx * sw * .8, sy + dy * L - ny * sw * .8), (sx - nx * sw, sy - ny * sw)]
        o += f'<path d="M{P(q)}Z" fill="#8a9a3c" stroke="{line}" stroke-width="{lw * .8:.1f}" stroke-linejoin="round"/>'
        o += f'<path d="M{P([q[0], q[1]])}" stroke="#c8d470" stroke-width="{lw * .7:.1f}" opacity=".7"/>'
        ex, ey = sx + dx * L, sy + dy * L
        o += f'<ellipse cx="{ex:.1f}" cy="{ey:.1f}" rx="{sw * .85:.1f}" ry="{sw * .45:.1f}" transform="rotate({math.degrees(math.atan2(ny, nx)):.1f} {ex:.1f} {ey:.1f})" fill="#4a3a1c" stroke="{line}" stroke-width="{lw * .6:.1f}"/>'
    return o, F


# ================= A: the Alien egg -> the infected Cavendish =================
def make_A():
    rnd = random.Random(4)
    d = FILTERS
    d += lin('skyA', [(0, '#020604'), (.6, '#06120c'), (1, '#0a1c12')])
    d += lin('floorA', [(0, '#0a1a10'), (1, '#010302')])
    d += rad('haloA', 1250, 470, 620, [(0, '#7dff6a', .35), (.45, '#2fae4a', .12), (1, '#000', 0)])
    d += rad('crackA', 1260, 380, 260, [(0, '#f4ffd0', 1), (.3, '#b8ff5a', .9), (1, '#3aff3a', 0)])
    d += rad('vigA', 960, 540, 1150, [(0, '#000', 0), (.65, '#000', 0), (1, '#000', .75)])
    b = '<rect width="1920" height="1080" fill="url(#skyA)"/>'
    b += '<rect width="1920" height="1080" fill="url(#haloA)"/>'
    # perspective grid floor (poster homage)
    hz = 760
    b += f'<rect x="0" y="{hz}" width="1920" height="{1080 - hz}" fill="url(#floorA)"/>'
    vx = 1250
    for k in range(-26, 27):
        x2 = vx + k * 130
        b += f'<line x1="{vx + k * 9}" y1="{hz}" x2="{x2}" y2="1080" stroke="#5aff7a" stroke-width="2" opacity="{max(.04, .32 - abs(k) * .012):.2f}"/>'
    for j in range(1, 12):
        y = hz + (1080 - hz) * (j / 11) ** 1.9
        b += f'<line x1="0" y1="{y:.0f}" x2="1920" y2="{y:.0f}" stroke="#5aff7a" stroke-width="2" opacity="{.08 + j * .018:.2f}"/>'
    b += f'<line x1="0" y1="{hz}" x2="1920" y2="{hz}" stroke="#8aff8a" stroke-width="3" opacity=".35"/>'
    # glow pool on the floor + shadow
    b += '<ellipse cx="1255" cy="905" rx="420" ry="70" fill="#7dff6a" opacity=".25" filter="url(#b26)"/>'
    b += '<ellipse cx="1255" cy="912" rx="210" ry="30" fill="#000" opacity=".7" filter="url(#b8)"/>'
    # rising spore mist
    for k in range(9):
        x = 1180 + rnd.uniform(-90, 90); w = rnd.uniform(30, 70)
        b += (f'<path d="M{x:.0f} 330 C{x - w:.0f} 260 {x + w:.0f} 200 {x + rnd.uniform(-60, 60):.0f} {rnd.uniform(40, 140):.0f}" fill="none" '
              f'stroke="#9cff7a" stroke-width="{rnd.uniform(10, 26):.0f}" opacity="{rnd.uniform(.08, .2):.2f}" stroke-linecap="round" filter="url(#b8)"/>')
    # the banana standing upright on its stem (the egg)
    p = ((1250, 860), (1430, 700), (1420, 330), (1235, 140))
    pal = ('#b3871c', '#e8bf3a', '#ffe680', '#d8ff9a')
    art, F = banana(p, 165, pal, line='#1a1404', lw=7, spots=40, rnd=rnd, glow='#6aff5a')
    b += art
    C, N, W = F
    # creeping fungal rot from the base: brown-black patches with green glowing veins
    d += f'<clipPath id="bodyA"><path d="M{P(off(F, 1))} L{P(off(F, -1)[::-1])}Z"/></clipPath>'
    rot = ''
    for _ in range(26):
        i = rnd.randint(0, 34); u = rnd.uniform(-1, 1)
        x, y = C[i][0] + N[i][0] * W[i] * u, C[i][1] + N[i][1] * W[i] * u
        rot += f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{rnd.uniform(30, 80):.0f}" ry="{rnd.uniform(20, 50):.0f}" fill="#2a1e0c" opacity="{rnd.uniform(.35, .7):.2f}" filter="url(#b4)"/>'
    rot += '<rect x="1000" y="700" width="600" height="300" fill="#1e1608" opacity=".55" filter="url(#b14)"/>'
    for _ in range(14):
        i = rnd.randint(2, 30); x, y = C[i]; ang = rnd.uniform(-2.6, -.6); L = rnd.uniform(60, 170)
        pts = [(x, y)]
        for s in range(5):
            x += math.cos(ang) * L / 5 + rnd.uniform(-10, 10); y += math.sin(ang) * L / 5; pts.append((x, y))
        rot += f'<polyline points="{P(pts)}" fill="none" stroke="#7dff4a" stroke-width="4" opacity=".75"/>'
        rot += f'<polyline points="{P(pts)}" fill="none" stroke="#c8ff8a" stroke-width="10" opacity=".25" filter="url(#b4)"/>'
    b += f'<g clip-path="url(#bodyA)">{rot}</g>'
    # glowing crack across the upper body (light leaking out)
    i = 58; cx, cy = C[i]; nx, ny = N[i]; w = W[i]
    crack = []
    for k in range(9):
        u = -1.02 + k * 2.04 / 8
        jig = (18 if k % 2 else -14)
        crack.append((cx + nx * w * u + ny * jig, cy + ny * w * u - nx * jig))
    b += f'<circle cx="{cx:.0f}" cy="{cy:.0f}" r="240" fill="url(#crackA)" opacity=".55" filter="url(#b26)"/>'
    b += f'<polyline points="{P(crack)}" fill="none" stroke="#cfff7a" stroke-width="34" opacity=".55" filter="url(#b8)" stroke-linejoin="round"/>'
    b += f'<polyline points="{P(crack)}" fill="none" stroke="#1a1404" stroke-width="16" stroke-linejoin="round"/>'
    b += f'<polyline points="{P(crack)}" fill="none" stroke="#f4ffd0" stroke-width="8" stroke-linejoin="round"/>'
    # light rays out of the crack
    for k in range(7):
        a = -math.pi / 2 + (k - 3) * .22; L = rnd.uniform(260, 420)
        b += (f'<path d="M{cx:.0f} {cy:.0f} L{cx + math.cos(a - .05) * L:.0f} {cy + math.sin(a - .05) * L:.0f} L{cx + math.cos(a + .05) * L:.0f} {cy + math.sin(a + .05) * L:.0f}Z" '
              f'fill="#c8ff8a" opacity=".13" filter="url(#b8)"/>')
    # spores floating
    for _ in range(80):
        x = rnd.gauss(1250, 230); y = rnd.uniform(60, 760)
        b += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{rnd.choice([1.6, 2.4, 3.4, 4.5])}" fill="#d8ffb0" opacity="{rnd.uniform(.25, .85):.2f}"/>'
    b += spark(1170, 300, 26, '#f4ffd0') + spark(1420, 420, 18, '#e8ffd0') + spark(1060, 560, 14, '#e8ffd0')
    # wilting banana plants silhouetted far away on the horizon
    for x0, h in ((180, 120), (300, 90), (1720, 110), (1830, 80), (560, 70)):
        b += f'<path d="M{x0} {hz} L{x0 + 6} {hz - h}" stroke="#0e2a18" stroke-width="12"/>'
        for a in (-1, 1):
            b += f'<path d="M{x0 + 6} {hz - h} q{a * 40} -10 {a * 70} 30 q{-a * 30} -4 {-a * 70} -30z" fill="#0e2a18"/>'
    # frog in a hazmat suit with a torch, bottom-left, beam towards the banana
    b += '<path d="M500 860 L1120 600 L1130 820 Z" fill="#fffbd0" opacity=".10" filter="url(#b14)"/>'
    suit = ('<path d="M-36 -26 Q-40 4 -30 8 L42 8 Q50 2 44 -26 Q4 -16 -36 -26Z" fill="#f2c21a" stroke-width="3.6"/>'
            '<path d="M-34 -6 L44 -6" stroke="#1a1404" stroke-width="5"/><path d="M-32 -6 L44 -6" stroke="#2a2a2a" stroke-width="3" stroke-dasharray="7 7"/>'
            '<circle cx="4" cy="-16" r="7" fill="#1a1404" stroke="none"/><path d="M4 -22 l0 -3 M-1 -12 l-3 3 M9 -12 l3 3" stroke="#f2c21a" stroke-width="2.4"/>')
    torch = ('<g transform="translate(64 -48) rotate(-24)"><rect x="-6" y="-10" width="34" height="18" rx="4" fill="#444" stroke-width="3"/>'
             '<path d="M28 -14 L40 -18 L40 16 L28 12Z" fill="#888" stroke-width="3"/><ellipse cx="40" cy="-1" rx="4" ry="17" fill="#fffbe0" stroke-width="2"/></g>')
    b += '<circle cx="420" cy="860" r="170" fill="#f2ffd0" opacity=".12" filter="url(#b50)"/>'
    b += frog(400, 1000, 2.75, rot=-4, look=(10, -7), mouth='O', helmet=True, shadow=True, mid=suit, brows=False,
              armL='M-34 -22 q-18 4 -22 24', armR='M38 -22 q18 -8 26 -26', front=torch)
    b += '<rect width="1920" height="1080" fill="url(#vigA)"/>'
    lines = [('TR4', 260, 'y'), ('IS SPREADING', 128, 'w')]
    return page('#020604', svg(d, b), lines, outline='#03100a', top=40)


# ================= B: wild banana cut open, packed with gravel-like seeds =================
def leaf(x, y, L, ang, col, vein, w=.22):
    a = math.radians(ang); dx, dy = math.cos(a), math.sin(a); nx, ny = -dy, dx
    ex, ey = x + dx * L, y + dy * L
    o = (f'<path d="M{x} {y} Q{x + dx * L * .5 + nx * L * w:.0f} {y + dy * L * .5 + ny * L * w:.0f} {ex:.0f} {ey:.0f} '
         f'Q{x + dx * L * .5 - nx * L * w:.0f} {y + dy * L * .5 - ny * L * w:.0f} {x} {y}Z" fill="{col}"/>')
    o += f'<path d="M{x} {y} L{ex:.0f} {ey:.0f}" stroke="{vein}" stroke-width="5" opacity=".6"/>'
    for k in range(1, 9):
        t = k / 9; px, py = x + dx * L * t, y + dy * L * t; ww = L * w * .9 * math.sin(math.pi * t)
        for s in (1, -1):
            o += f'<path d="M{px:.0f} {py:.0f} l{(nx * s + dx * .5) * ww:.0f} {(ny * s + dy * .5) * ww:.0f}" stroke="{vein}" stroke-width="2" opacity=".35"/>'
    return o


def make_B():
    rnd = random.Random(8)
    d = FILTERS
    d += lin('skyB', [(0, '#1f4a22'), (.5, '#2f6a2a'), (1, '#16301a')])
    d += rad('sunB', 1500, 160, 760, [(0, '#fff4c0', .95), (.25, '#f2d27a', .55), (1, '#f2d27a', 0)])
    d += lin('fleshB', [(0, '#fff6d8'), (.5, '#f3e2a8'), (1, '#d9c27a')])
    d += rad('vigB', 960, 540, 1150, [(0, '#000', 0), (.62, '#000', 0), (1, '#06140a', .75)])
    d += lin('groundB', [(0, '#3e3018'), (1, '#1a140a')])
    b = '<rect width="1920" height="1080" fill="url(#skyB)"/>'
    # back leaves (dark) for depth
    for x, y, L, a, c in ((1900, 40, 700, 150, '#173d1c'), (1100, -60, 640, 70, '#1b4620'), (60, 720, 600, -40, '#12301a'),
                          (1880, 600, 600, 200, '#143619'), (700, 620, 520, -70, '#173d1c')):
        b += leaf(x, y, L, a, c, '#0a2410')
    b += '<rect width="1920" height="1080" fill="url(#sunB)"/>'
    for k in range(6):  # sun rays through the canopy
        x = 1300 + k * 90
        b += f'<path d="M{x} -20 L{x + 60} -20 L{x - 360} 1100 L{x - 470} 1100Z" fill="#fff4c0" opacity=".06"/>'
    # mid leaves lit
    b += leaf(1920, 260, 520, 168, '#4e8a2e', '#2a5a18', .2)
    b += leaf(980, -40, 420, 100, '#3f7a28', '#24501a', .2)
    # ground
    b += '<path d="M0 900 Q700 850 1920 880 L1920 1080 L0 1080Z" fill="url(#groundB)"/>'
    # the wild banana, cut in half lengthwise (cut face up)
    p = ((690, 790), (980, 960), (1520, 820), (1700, 360))
    F = frame(p, 190, prof=lambda t: .34 + .66 * math.sin(math.pi * min(1, max(0, t))) ** .5)
    C, N, W = F
    b += f'<path d="M{P(off(F, 1.15))} L{P(off(F, -1.15)[::-1])}Z" fill="#fff0a0" opacity=".45" filter="url(#b26)"/>'
    b += f'<ellipse cx="1220" cy="930" rx="560" ry="60" fill="#000" opacity=".45" filter="url(#b14)"/>'
    # peel shell underneath (seen as thick lower rim) -- greenish wild banana skin
    b += f'<path d="M{P(off(F, 1.08))} L{P(off(F, -1.08)[::-1])}Z" fill="#6c8a2c" stroke="#1a1a08" stroke-width="12" stroke-linejoin="round" transform="translate(0 26)"/>'
    b += f'<path d="M{P(off(F, 1.08))} L{P(off(F, -1.08)[::-1])}Z" fill="#9cb048" stroke="#1a1a08" stroke-width="10" stroke-linejoin="round"/>'
    b += f'<path d="M{P(off(F, .92))} L{P(off(F, -.92)[::-1])}Z" fill="#e6e0a6"/>'
    b += f'<path d="M{P(off(F, .84))} L{P(off(F, -.84)[::-1])}Z" fill="url(#fleshB)" stroke="#a89850" stroke-width="3"/>'
    b += f'<polyline points="{P(off(F, .55, 6, len(C) - 8))}" fill="none" stroke="#ffffff" stroke-width="14" opacity=".45" stroke-linecap="round"/>'
    # seeds packed in three rows along the core
    seeds = []
    for i in range(4, len(C) - 3, 2):
        for u in (-.5, 0, .5):
            if rnd.random() < .12: continue
            x, y = C[i][0] + N[i][0] * W[i] * (u + rnd.uniform(-.08, .08)), C[i][1] + N[i][1] * W[i] * (u + rnd.uniform(-.08, .08))
            r = W[i] * rnd.uniform(.16, .21)
            seeds.append((x, y, r))
    for x, y, r in seeds:
        b += f'<ellipse cx="{x + 3:.0f}" cy="{y + 5:.0f}" rx="{r * 1.15:.1f}" ry="{r:.1f}" fill="#8a7838" opacity=".55"/>'
    for x, y, r in seeds:
        a = rnd.uniform(0, 180)
        b += (f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{r * 1.1:.1f}" ry="{r * .92:.1f}" transform="rotate({a:.0f} {x:.0f} {y:.0f})" fill="#1c1610" stroke="#000" stroke-width="2.5"/>'
              f'<ellipse cx="{x - r * .35:.1f}" cy="{y - r * .38:.1f}" rx="{r * .38:.1f}" ry="{r * .22:.1f}" transform="rotate(-30 {x - r * .35:.1f} {y - r * .38:.1f})" fill="#fff" opacity=".75"/>'
              f'<path d="M{x - r * .6:.1f} {y + r * .3:.1f} q{r * .6:.1f} {r * .4:.1f} {r * 1.2:.1f} 0" fill="none" stroke="#5a4a30" stroke-width="2" opacity=".8"/>')
    # stem end and dark tip of the wild banana
    sx, sy = C[0]; b += f'<path d="M{sx - 10} {sy - 30} L{sx - 110} {sy - 70} L{sx - 120} {sy - 20} L{sx - 6} {sy + 34}Z" fill="#6c7a2c" stroke="#1a1a08" stroke-width="8" stroke-linejoin="round"/>'
    b += f'<ellipse cx="{sx - 116}" cy="{sy - 45}" rx="14" ry="28" fill="#3a3418" stroke="#1a1a08" stroke-width="5"/>'
    tx, ty = C[-1]; b += f'<path d="M{tx - 50} {ty + 10} Q{tx + 10} {ty - 90} {tx + 60} {ty + 20}Z" fill="#3a3418" stroke="#1a1a08" stroke-width="8" stroke-linejoin="round"/>'
    # loose seeds spilled on the ground
    for x, y, r in ((820, 960, 22), (880, 990, 19), (1000, 1000, 24), (760, 1010, 18), (1120, 985, 16)):
        b += (f'<ellipse cx="{x}" cy="{y}" rx="{r * 1.1:.0f}" ry="{r * .85:.0f}" fill="#1c1610" stroke="#000" stroke-width="2.5"/>'
              f'<ellipse cx="{x - r * .35:.0f}" cy="{y - r * .35:.0f}" rx="{r * .35:.0f}" ry="{r * .2:.0f}" fill="#fff" opacity=".7"/>')
    # dust motes in the sun
    for _ in range(70):
        b += f'<circle cx="{rnd.uniform(900, 1900):.0f}" cy="{rnd.uniform(0, 800):.0f}" r="{rnd.choice([1.5, 2.2, 3])}" fill="#fff8d0" opacity="{rnd.uniform(.2, .7):.2f}"/>'
    b += spark(1560, 470, 26, '#fffbe6') + spark(1000, 740, 18) + spark(1700, 250, 16)
    # explorer frog (pith helmet) holding up one seed, bottom-left
    hat = ('<g transform="translate(6 -86) rotate(-8)"><ellipse cx="0" cy="6" rx="52" ry="11" fill="#d9c08a" stroke-width="3.4"/>'
           '<path d="M-34 6 Q-34 -34 0 -36 Q34 -34 34 6Z" fill="#e8d4a0" stroke-width="3.4"/><path d="M-33 -2 Q0 4 33 -2 L34 6 Q0 12 -34 6Z" fill="#7a5a2a" stroke-width="2.4"/>'
           '<path d="M-20 -22 Q-8 -32 8 -32" fill="none" stroke="#fff6dc" stroke-width="4" opacity=".8"/></g>')
    strap = '<path d="M-30 -30 L40 -4" stroke="#7a5a2a" stroke-width="6"/><rect x="26" y="-14" width="22" height="18" rx="4" fill="#9a7a3a" stroke-width="3"/>'
    seed = ('<ellipse cx="62" cy="-104" rx="11" ry="9" fill="#1c1610" stroke="#000" stroke-width="2.4"/>'
            '<ellipse cx="58" cy="-108" rx="4" ry="2.4" fill="#fff" stroke="none" opacity=".8"/>')
    b += '<circle cx="440" cy="790" r="170" fill="#fff6c8" opacity=".25" filter="url(#b50)"/>'
    b += frog(400, 1000, 2.75, rot=4, look=(10, -8), mouth='O', shadow=True, mid=strap, top=hat, brows=False,
              armL='M-34 -22 q-18 4 -22 22', armR='M38 -22 q24 -30 22 -72', front=seed)
    b += '<rect width="1920" height="1080" fill="url(#vigB)"/>'
    lines = [('OUR BANANAS', 112, 'w'), ('WHY NO', 150, 'w'), ('SEEDS?', 240, 'y')]
    return page('#1f4a22', svg(d, b), lines, outline='#0a1a0c', top=40)


# ================= C: a radioactive bunch of bananas + Geiger counter =================
def make_C():
    rnd = random.Random(31)
    d = FILTERS
    d += lin('bgC', [(0, '#1a0c34'), (.55, '#2a1452'), (1, '#0c0618')])
    d += rad('haloC', 1250, 540, 640, [(0, '#ffe68a', .6), (.35, '#f2b23a', .25), (.7, '#a040ff', .08), (1, '#000', 0)])
    d += rad('vigC', 960, 540, 1150, [(0, '#000', 0), (.62, '#000', 0), (1, '#05020c', .8)])
    d += lin('tableC', [(0, '#3a2a5a'), (1, '#120a22')])
    b = '<rect width="1920" height="1080" fill="url(#bgC)"/>'
    # lab background: shelves with flasks (soft, out of focus)
    sh = ''
    for y in (300, 560):
        sh += f'<rect x="0" y="{y}" width="1920" height="14" fill="#3a2a64"/>'
        for k in range(14):
            x = 60 + k * 140 + rnd.uniform(-20, 20); h = rnd.uniform(60, 110)
            col = rnd.choice(['#5ad0ff', '#ff7ad8', '#8aff9a', '#b48aff'])
            sh += f'<path d="M{x - 12:.0f} {y - h:.0f} L{x + 12:.0f} {y - h:.0f} L{x + 12:.0f} {y - h * .55:.0f} L{x + 34:.0f} {y} L{x - 34:.0f} {y} L{x - 12:.0f} {y - h * .55:.0f}Z" fill="{col}" opacity=".35"/>'
    b += f'<g filter="url(#b4)" opacity=".8">{sh}</g>'
    b += '<rect width="1920" height="1080" fill="url(#haloC)"/>'
    # table
    b += '<path d="M0 820 L1920 800 L1920 1080 L0 1080Z" fill="url(#tableC)"/><path d="M0 820 L1920 800" stroke="#7a5ab0" stroke-width="4" opacity=".6"/>'
    b += '<g transform="translate(160 110) scale(.93)">'
    # concentric radiation rings around the bunch
    for k, r in enumerate((300, 390, 480)):
        b += f'<ellipse cx="1250" cy="560" rx="{r}" ry="{r * .92:.0f}" fill="none" stroke="#ffe68a" stroke-width="{6 - k * 1.5}" opacity="{.35 - k * .08:.2f}" stroke-dasharray="{30 + k * 10} {18 + k * 8}"/>'
    # shadow on the table
    b += '<ellipse cx="1240" cy="850" rx="400" ry="40" fill="#000" opacity=".5" filter="url(#b14)"/>'
    b += '<ellipse cx="1240" cy="840" rx="460" ry="60" fill="#ffd060" opacity=".22" filter="url(#b26)"/>'
    # bunch: three bananas from one crown
    pal = ('#d89a1a', '#f6c932', '#fff08a', '#fff8c8')
    crown = (1020, 330)
    bunch = [((crown), (1020, 620), (1300, 860), (1600, 700)),
             ((1050, 310), (1180, 560), (1460, 700), (1700, 520)),
             ((1010, 360), (920, 650), (1120, 860), (1360, 830))]
    for k, p in enumerate(bunch):
        art, _ = banana(p, 105 if k != 1 else 98, pal, line='#3a1c04', lw=6, stem=False, spots=18, rnd=rnd, glow='#ffd84a')
        b += art
    # crown stalk
    b += '<path d="M980 360 Q960 240 1010 170 L1060 190 Q1040 260 1070 330 Z" fill="#9aa83c" stroke="#3a1c04" stroke-width="7" stroke-linejoin="round"/>'
    b += '<ellipse cx="1035" cy="178" rx="30" ry="14" transform="rotate(20 1035 178)" fill="#5a4a1c" stroke="#3a1c04" stroke-width="5"/>'
    b += '<path d="M1000 340 Q990 260 1020 200" fill="none" stroke="#d8e47a" stroke-width="6" opacity=".7"/>'
    # decay sparks / particle tracks flying out
    for _ in range(26):
        a = rnd.uniform(0, 2 * math.pi); r0 = rnd.uniform(260, 330); L = rnd.uniform(40, 120)
        x0, y0 = 1250 + math.cos(a) * r0, 560 + math.sin(a) * r0 * .9
        if y0 > 800: continue
        b += f'<line x1="{x0:.0f}" y1="{y0:.0f}" x2="{x0 + math.cos(a) * L:.0f}" y2="{y0 + math.sin(a) * L:.0f}" stroke="#fff4b0" stroke-width="3.5" stroke-linecap="round" opacity=".85"/>'
        b += f'<circle cx="{x0 + math.cos(a) * L:.0f}" cy="{y0 + math.sin(a) * L:.0f}" r="5" fill="#fff" opacity=".9"/>'
    for _ in range(60):
        b += f'<circle cx="{rnd.gauss(1250, 330):.0f}" cy="{rnd.gauss(520, 230):.0f}" r="{rnd.choice([1.6, 2.4, 3.2])}" fill="#ffeeb0" opacity="{rnd.uniform(.25, .8):.2f}"/>'
    b += spark(1520, 300, 28, '#fffbe0') + spark(880, 520, 18) + spark(1640, 620, 16, '#ffe9ff')
    b += '</g>'
    # frog in a lab coat with goggles holding a Geiger counter towards the bananas
    coat = ('<path d="M-36 -40 Q-44 -6 -36 4 L-4 4 L-2 -34 Z" fill="#f2f0f8" stroke-width="3.4"/>'
            '<path d="M44 -40 Q52 -6 46 4 L14 4 L12 -34 Z" fill="#f2f0f8" stroke-width="3.4"/>'
            '<path d="M-2 -34 L-12 -20 M12 -34 L22 -20" stroke-width="3"/><rect x="24" y="-18" width="12" height="10" rx="2" fill="#dcd8ea" stroke-width="2.4"/>')
    goggles = ('<path d="M-30 -94 Q6 -104 42 -94" fill="none" stroke="#2a2a3a" stroke-width="6"/>'
               '<ellipse cx="-6" cy="-96" rx="14" ry="10" fill="#9ae8ff" stroke-width="3.4"/><ellipse cx="24" cy="-96" rx="14" ry="10" fill="#9ae8ff" stroke-width="3.4"/>'
               '<path d="M-12 -100 l8 -2 M18 -100 l8 -2" stroke="#fff" stroke-width="2.4"/>')
    geiger = ('<g transform="translate(66 -66)"><rect x="-6" y="-26" width="64" height="46" rx="8" fill="#f2c21a" stroke-width="3.6"/>'
              '<path d="M2 4 A22 22 0 0 1 46 4" fill="#fffbe6" stroke-width="2.6"/><path d="M24 4 L34 -12" stroke="#c0202a" stroke-width="3"/>'
              '<circle cx="24" cy="4" r="3" fill="#1d2b1c" stroke="none"/>'
              '<g transform="translate(24 -16) scale(.5)" stroke="none" fill="#1d2b1c"><circle r="4"/>'
              + ''.join(f'<path d="M0 0 L{14 * math.cos(math.radians(a - 30)):.1f} {14 * math.sin(math.radians(a - 30)):.1f} A14 14 0 0 1 {14 * math.cos(math.radians(a + 30)):.1f} {14 * math.sin(math.radians(a + 30)):.1f}Z"/>' for a in (-90, 30, 150)) +
              '</g><path d="M58 -6 Q80 -6 84 -30" fill="none" stroke-width="3.4"/><rect x="76" y="-60" width="14" height="34" rx="5" fill="#cfd2dc" stroke-width="3" transform="rotate(30 83 -43)"/></g>')
    b += '<circle cx="520" cy="820" r="180" fill="#ffe68a" opacity=".16" filter="url(#b50)"/>'
    b += frog(470, 1000, 2.8, rot=-3, look=(11, -6), mouth='O', shadow=True, mid=coat, top=goggles, brows=True,
              armL='M-34 -22 q-18 4 -22 22', armR='M38 -22 q18 -14 28 -36', front=geiger)
    # "tick" arcs from the counter
    for k in range(3):
        b += f'<path d="M{790 + k * 26} {690 - k * 10} q14 -22 0 -46" fill="none" stroke="#ffe68a" stroke-width="5" stroke-linecap="round" opacity="{.85 - k * .22:.2f}"/>'
    b += '<rect width="1920" height="1080" fill="url(#vigC)"/>'
    lines = [('ARE BANANAS', 128, 'w'), ('RADIOACTIVE?', 150, 'y')]
    return page('#1a0c34', svg(d, b), lines, outline='#0a0418', top=44)


for n, fn in (('A', make_A), ('B', make_B), ('C', make_C)):
    open(os.path.join(HERE, f'{n}.html'), 'w').write(fn())
print('ok')
