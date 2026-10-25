# Thumbnails A-C for whale-fall (guideline 16-6, brief tools/briefs/thumb_art.md). Run: python3 videos/whale-fall/thumb/make.py
# A  WHERE IS ITS MOUTH?      intuitive: zombie worm Osedax (S18-S19: no mouth, no stomach, red plumes, roots in the bone)
# B  UNKNOWN UNTIL 1987       homage: Titanic (bow pose + submersible lights on a wreck; S03: Alvin found the first whale fall in 1987)
# C  FEEDS THE DEEP / FOR DECADES   intuitive: full whale skeleton with scavengers (hagfish, crabs, isopods); S02 "can feed ... for decades" (hedged: CAN), S07-S10
# v2 (2026-10-25): every thumb has a clearly drawn whale skeleton (skull + lower jaw, vertebrae, curved ribs, tapering tail)
import os, sys, math, random
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../tools'))
from thumb_lib import page, svg, lin, rad, spark

INK = '#1d2b1c'; GREEN = '#6aa55a'


def P(v):
    return ' '.join(f'{a:.1f},{b:.1f}' for a, b in v)


def qb(p0, p1, p2, t):
    return ((1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * p1[0] + t * t * p2[0], (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * p1[1] + t * t * p2[1])


def cb(p0, p1, p2, p3, t):
    u = 1 - t
    return tuple(u ** 3 * p0[i] + 3 * u * u * t * p1[i] + 3 * u * t * t * p2[i] + t ** 3 * p3[i] for i in (0, 1))


FILTERS = ('<filter id="b4" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="4"/></filter>'
           '<filter id="b10" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="10"/></filter>'
           '<filter id="b24" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="24"/></filter>'
           '<filter id="b50" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="50"/></filter>')


# ---------------- mascot frog (tools/assets/frog.svg body, diving helmet added) ----------------
ARMS = {'down': ('q-14 6 -16 22', 'q14 6 16 22'), 'wide': ('q-30 0 -62 -12', 'q30 0 62 -12'),
        'fwd': ('q-14 6 -16 22', 'q20 -2 30 -22'), 'fork': ('q-16 0 -22 -22', 'q16 0 22 -22')}


def frog(x, y, s, mouth='o', arms='down', look=(2, 0), front='', back='', flip=False):
    la, ra = ARMS[arms]
    sx = -s if flip else s
    g = f'<g transform="translate({x} {y}) scale({sx} {s})" stroke="{INK}" stroke-linejoin="round" stroke-linecap="round">'
    # air tank + hose (behind)
    g += back
    g += '<rect x="-56" y="-62" width="22" height="52" rx="10" fill="#e3ab3e" stroke-width="3.2"/><rect x="-52" y="-56" width="5" height="40" rx="2" fill="#fff3c4" stroke="none" opacity=".7"/>'
    g += '<path d="M-46 -62 q-6 -34 22 -38" fill="none" stroke-width="8"/><path d="M-46 -62 q-6 -34 22 -38" fill="none" stroke="#6b6f78" stroke-width="4"/>'
    g += '<ellipse cx="-22" cy="4" rx="16" ry="9" fill="#4d8a4a" stroke-width="3.2"/><ellipse cx="22" cy="4" rx="16" ry="9" fill="#4d8a4a" stroke-width="3.2"/>'
    g += f'<path d="M-34 0 q-6 -64 34 -70 q40 -2 42 62 q0 10 -6 12 q-36 6 -70 -4z" fill="{GREEN}" stroke-width="4"/>'
    g += '<ellipse cx="2" cy="-12" rx="22" ry="20" fill="#9cc98a" stroke="none" opacity=".7"/>'
    g += '<path d="M-26 -50 q6 -16 22 -18" fill="none" stroke="#b9e0a6" stroke-width="3" opacity=".7"/>'
    dx, dy = look
    g += f'<circle cx="-10" cy="-66" r="13" fill="#e3e5d6" stroke-width="3.2"/><circle cx="{-10 + dx}" cy="{-66 + dy}" r="5" fill="{INK}" stroke="none"/>'
    g += f'<circle cx="22" cy="-66" r="13" fill="#e3e5d6" stroke-width="3.2"/><circle cx="{22 + dx}" cy="{-66 + dy}" r="5" fill="{INK}" stroke="none"/>'
    g += f'<circle cx="{-8 + dx}" cy="{-68 + dy}" r="1.6" fill="#fff" stroke="none"/><circle cx="{24 + dx}" cy="{-68 + dy}" r="1.6" fill="#fff" stroke="none"/>'
    g += '<ellipse cx="-18" cy="-46" rx="5" ry="3" fill="#e98a8a" stroke="none" opacity=".55"/><ellipse cx="30" cy="-46" rx="5" ry="3" fill="#e98a8a" stroke="none" opacity=".55"/>'
    if mouth == 'o':
        g += '<ellipse cx="6" cy="-42" rx="6.5" ry="8" fill="#7a2f33" stroke-width="3"/><ellipse cx="6" cy="-38" rx="3.5" ry="2.6" fill="#e07b7b" stroke="none"/>'
    else:
        g += '<path d="M-8 -45 q14 14 28 0 q-14 4 -28 0z" fill="#7a2f33" stroke-width="3"/>'
    # helmet glass + brass collar
    g += '<circle cx="6" cy="-56" r="42" fill="#bfe6ff" fill-opacity=".14" stroke="#d6a94f" stroke-width="4.5"/>'
    g += '<circle cx="6" cy="-56" r="37.5" fill="none" stroke="#fff" stroke-width="1.6" opacity=".35"/>'
    g += '<path d="M-24 -78 A34 34 0 0 1 8 -92" fill="none" stroke="#fff" stroke-width="5" opacity=".75"/><circle cx="34" cy="-30" r="3" fill="#fff" stroke="none" opacity=".6"/>'
    g += '<ellipse cx="5" cy="-16" rx="38" ry="9" fill="#c48d38" stroke-width="3.2"/><path d="M-30 -18 q35 8 70 0" fill="none" stroke="#f4d58a" stroke-width="2.2" opacity=".8"/>'
    g += ''.join(f'<circle cx="{c}" cy="-15" r="2.4" fill="#ffe7a6" stroke="none"/>' for c in (-24, -9, 6, 21, 34))
    for st, path in (('M-32 -12', la), ('M38 -12', ra)):
        g += f'<path d="{st} {path}" fill="none" stroke-width="7.5"/><path d="{st} {path}" fill="none" stroke="{GREEN}" stroke-width="3.4"/>'
        sx0, sy0 = map(float, st[1:].split()); q = [float(v) for v in path[1:].split()]
        g += f'<circle cx="{sx0 + q[2]}" cy="{sy0 + q[3]}" r="5.5" fill="{GREEN}" stroke-width="3"/>'
    g += front
    return g + '</g>'


def bubbles(x, y, n, spread=40, rise=260, s=1.0, col='#dff6ff'):
    out = ''
    for i in range(n):
        yy = y - rise * i / n - random.uniform(0, 20); xx = x + math.sin(i * 1.7) * spread * i / n
        r = (4 + 7 * random.random()) * s
        out += f'<circle cx="{xx:.0f}" cy="{yy:.0f}" r="{r:.1f}" fill="{col}" fill-opacity=".12" stroke="{col}" stroke-width="2" stroke-opacity=".7"/>'
        out += f'<circle cx="{xx - r * .35:.0f}" cy="{yy - r * .35:.0f}" r="{r * .25:.1f}" fill="#fff" opacity=".8"/>'
    return out


def snow(n, x0, y0, x1, y1, col='#dfeee8', omax=.55, rmax=2.6):
    return ''.join(f'<circle cx="{random.uniform(x0, x1):.0f}" cy="{random.uniform(y0, y1):.0f}" r="{random.uniform(.8, rmax):.1f}" fill="{col}" opacity="{random.uniform(.1, omax):.2f}"/>' for _ in range(n))


# ---------------- creatures ----------------
def osedax(x, y, h, s=1.0, lean=0.0, bright=1.0):
    cx, cy = x + lean, y - h
    o = ''
    # trunk (translucent tube)
    d = f'M{x:.1f},{y:.1f} Q{x + lean * .2:.1f},{y - h * .55:.1f} {cx:.1f},{cy:.1f}'
    o += f'<path d="{d}" stroke="#5a0d1a" stroke-width="{15 * s:.1f}" fill="none" stroke-linecap="round"/>'
    o += f'<path d="{d}" stroke="#f3c9c0" stroke-width="{10 * s:.1f}" fill="none" stroke-linecap="round" opacity=".95"/>'
    o += f'<path d="{d}" stroke="#fff" stroke-width="{2.4 * s:.1f}" fill="none" stroke-linecap="round" opacity=".55" transform="translate({-2.5 * s:.1f} 0)"/>'
    base = math.degrees(math.atan2(lean, h)) * .6
    for k, a in enumerate((-62, -26, 14, 52)):
        a = math.radians(a + base); L = 118 * s * (1 - .08 * (k % 2))
        p0 = (cx, cy); p3 = (cx + math.sin(a) * L, cy - math.cos(a) * L)
        a1 = a * .45; p1 = (cx + math.sin(a1) * L * .45, cy - math.cos(a1) * L * .45)
        a2 = a * 1.25; p2 = (cx + math.sin(a2) * L * .85, cy - math.cos(a2) * L * .85)
        dd = f'M{p0[0]:.1f},{p0[1]:.1f} C{p1[0]:.1f},{p1[1]:.1f} {p2[0]:.1f},{p2[1]:.1f} {p3[0]:.1f},{p3[1]:.1f}'
        o += f'<path d="{dd}" stroke="#4a0712" stroke-width="{19 * s:.1f}" fill="none" stroke-linecap="round"/>'
        # pinnules
        pin = ''
        for i in range(3, 19):
            t = i / 19; q = cb(p0, p1, p2, p3, t); q2 = cb(p0, p1, p2, p3, t + .01)
            tx, ty = q2[0] - q[0], q2[1] - q[1]; ln = math.hypot(tx, ty) or 1; nx, ny = -ty / ln, tx / ln
            l = (17 - 9 * t) * s
            pin += f'M{q[0] + nx * l:.1f},{q[1] + ny * l:.1f} L{q[0] - nx * l:.1f},{q[1] - ny * l:.1f} '
        o += f'<path d="{pin}" stroke="#4a0712" stroke-width="{5.5 * s:.1f}" stroke-linecap="round"/>'
        o += f'<path d="{pin}" stroke="#ff5a69" stroke-width="{2.8 * s:.1f}" stroke-linecap="round"/>'
        o += f'<path d="{dd}" stroke="#e0213a" stroke-width="{13 * s:.1f}" fill="none" stroke-linecap="round"/>'
        o += f'<path d="{dd}" stroke="#ff8a95" stroke-width="{3.6 * s:.1f}" fill="none" stroke-linecap="round" opacity="{.8 * bright:.2f}" transform="translate({-2 * s:.1f} {-1.5 * s:.1f})"/>'
    o += f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{9 * s:.1f}" fill="#c4152e" stroke="#4a0712" stroke-width="{3 * s:.1f}"/>'
    return o


def tuft(x, y, s=1.0):   # tiny osedax seen from far: red feathery dot
    o = f'<path d="M{x},{y} l0,{-10 * s:.1f}" stroke="#f3c9c0" stroke-width="{3 * s:.1f}"/>'
    for a in (-50, -15, 20, 55):
        r = math.radians(a)
        o += f'<path d="M{x},{y - 10 * s:.1f} q{math.sin(r) * 8 * s:.1f},{-12 * s:.1f} {math.sin(r) * 18 * s:.1f},{-math.cos(r) * 18 * s:.1f}" stroke="#ff3a4f" stroke-width="{3.2 * s:.1f}" fill="none" stroke-linecap="round"/>'
    return o


def isopod(x, y, s=1.0, flip=False, rot=0):
    f = -1 if flip else 1
    g = f'<g transform="translate({x} {y}) rotate({rot}) scale({f * s} {s})" stroke="#241a30" stroke-linejoin="round" stroke-linecap="round">'
    g += ''.join(f'<path d="M{lx},-4 l{-6 + i},16" stroke-width="4" fill="none"/>' for i, lx in enumerate(range(-38, 40, 11)))
    g += '<path d="M44 -14 q30 -20 46 -6" fill="none" stroke-width="3"/><path d="M44 -10 q24 -4 40 10" fill="none" stroke-width="3"/>'
    g += '<path d="M-60 2 Q-56 -44 0 -46 Q52 -44 56 2 Z" fill="#b8a6c8" stroke-width="4"/>'
    g += '<path d="M-52 -6 Q-48 -38 0 -40 Q30 -40 44 -26" fill="none" stroke="#ece2f4" stroke-width="5" opacity=".7"/>'
    g += ''.join(f'<path d="M{sx} -{40 - abs(sx) * .35:.0f} Q{sx + 4} -20 {sx} 0" fill="none" stroke-width="2.6" opacity=".75"/>' for sx in range(-40, 44, 12))
    g += '<path d="M-60 2 q-20 -6 -26 10 q14 4 26 -4z" fill="#a593b8" stroke-width="3"/>'
    g += '<ellipse cx="44" cy="-14" rx="9" ry="7" fill="#2a2a2a" stroke-width="2"/><circle cx="46" cy="-16" r="2.4" fill="#fff" stroke="none"/>'
    return g + '</g>'


def crab(x, y, s=1.0, col='#e2643a', rot=0):
    g = f'<g transform="translate({x} {y}) rotate({rot}) scale({s})" stroke="#3a150b" stroke-linejoin="round" stroke-linecap="round" fill="none">'
    for sd in (-1, 1):
        for i in range(3):
            g += f'<path d="M{sd * 18},{-2 + i * 5} l{sd * 16},{-10 + i * 2} l{sd * 10},{18}" stroke-width="4.5"/>'
            g += f'<path d="M{sd * 18},{-2 + i * 5} l{sd * 16},{-10 + i * 2} l{sd * 10},{18}" stroke="{col}" stroke-width="2"/>'
        g += f'<path d="M{sd * 16},-10 q{sd * 10},-18 {sd * 22},-18" stroke-width="6"/><path d="M{sd * 16},-10 q{sd * 10},-18 {sd * 22},-18" stroke="{col}" stroke-width="3"/>'
        g += f'<ellipse cx="{sd * 40}" cy="-30" rx="11" ry="8" fill="{col}" stroke-width="3" transform="rotate({sd * -25} {sd * 40} -30)"/>'
        g += f'<path d="M{sd * 6},-14 l{sd * 3},-12" stroke-width="3"/><circle cx="{sd * 9}" cy="-28" r="4" fill="#111" stroke-width="1.5"/>'
    g += f'<ellipse cx="0" cy="-4" rx="26" ry="15" fill="{col}" stroke-width="3.5"/><path d="M-18 -10 q18 -9 36 0" stroke="#ffb08a" stroke-width="3" opacity=".8"/>'
    return g + '</g>'


def hagfish(d, w=16):
    return (f'<path d="{d}" stroke="#3b1f22" stroke-width="{w + 6}" fill="none" stroke-linecap="round"/>'
            f'<path d="{d}" stroke="#d6968c" stroke-width="{w}" fill="none" stroke-linecap="round"/>'
            f'<path d="{d}" stroke="#f6c9bd" stroke-width="{w * .28:.1f}" fill="none" stroke-linecap="round" opacity=".7" transform="translate(-2 -3)"/>')


def shark(x, y, s=1.0, flip=False, rot=0):
    f = -1 if flip else 1
    g = f'<g transform="translate({x} {y}) rotate({rot}) scale({f * s} {s})" stroke="#11161c" stroke-linejoin="round" stroke-width="4">'
    g += '<path d="M300,26 L282,64 L258,30 Z" fill="#454e58"/>'
    g += ('<path d="M400,0 C380,-30 320,-45 220,-46 C140,-46 60,-32 0,-12 L-70,-56 L-56,-6 L-84,32 L0,8 '
          'C70,30 150,40 230,38 C320,35 380,22 400,0 Z" fill="#5a646f"/>')
    g += '<path d="M392,4 C360,26 300,32 230,32 C150,32 80,22 20,6" fill="none" stroke="#8b96a1" stroke-width="6" opacity=".55"/>'
    g += '<path d="M380,-14 C340,-36 280,-42 220,-42" fill="none" stroke="#aebbc6" stroke-width="4" opacity=".6"/>'
    g += '<path d="M190,-45 L215,-70 L240,-45" fill="#4d5761"/><path d="M80,-36 L100,-56 L122,-32" fill="#4d5761"/>'
    g += '<path d="M318,-8 q2,16 -2,26 M308,-8 q2,16 -2,26 M298,-8 q2,16 -2,26" fill="none" stroke-width="2.5" opacity=".7"/>'
    g += '<circle cx="362" cy="-10" r="6" fill="#d8f7e6" stroke-width="2"/><circle cx="363" cy="-10" r="2.6" fill="#0c1a12" stroke="none"/>'
    g += '<path d="M372,12 q-16,8 -34,6" fill="none" stroke-width="3"/>'
    return g + '</g>'


def fish(x, y, s=1.0, col='#bcd7d8', flip=False):
    f = -1 if flip else 1
    return (f'<g transform="translate({x} {y}) scale({f * s} {s})" stroke="#16262a" stroke-width="2.5" stroke-linejoin="round">'
            f'<path d="M0,0 C10,-14 34,-16 46,-2 C34,12 10,12 0,0 Z M0,0 L-14,-10 L-12,0 L-14,10 Z" fill="{col}"/>'
            '<circle cx="36" cy="-3" r="2.4" fill="#111" stroke="none"/></g>')


# ---------------- whale skeleton (v2: owner wants the WHALE BONE SHAPE to read clearly) ----------------
# local coords: rostrum tip at x=0 (head left), tail at x=1800, seafloor y=0, up = negative y.
# f(x, y) -> screen point, k(x) -> local scale at x; fx=-1 mirrors the small parts (head right).
BONE = lin('bone', [(0, '#fff6dd'), (.45, '#e6d3a8'), (1, '#8a7250')])
SKULLG = lin('skullG', [(0, '#fffaea'), (.35, '#eedcb2'), (.8, '#b89f73'), (1, '#6e5a3c')])
OUT = '#2f2416'
SK_TOP = [((470, -300), (420, -350), (300, -306), (225, -246)), ((225, -246), (150, -190), (70, -150), (0, -122))]
SK_BOT = [((0, -122), (110, -124), (260, -144), (400, -154)), ((400, -154), (485, -150), (530, -236), (470, -300))]
JAW = [((486, -150), (330, -104), (160, -76), (16, -64)), ((16, -64), (6, -56), (8, -48), (18, -46)),
       ((18, -46), (160, -30), (340, -42), (498, -110)), ((498, -110), (512, -126), (510, -150), (486, -150))]


def chain(segs, n=18):
    pts = []
    for s in segs:
        pts += [cb(*s, i / n) for i in range(n + (s is segs[-1]))]
    return pts


def spline_d(pts):
    return 'M' + ' L'.join(f'{x:.1f},{y:.1f}' for x, y in pts)


def vert(X, Y, sc, fx, rot=0, dark=False):
    f = '#6f5f45' if dark else 'url(#bone)'
    return (f'<g transform="translate({X:.1f} {Y:.1f}) rotate({rot:.1f}) scale({fx * sc:.3f} {sc:.3f})" stroke="{OUT}" stroke-width="4.5" stroke-linejoin="round">'
            f'<path d="M-11,-18 L2,-84 Q11,-92 19,-83 L11,-18 Z" fill="{f}"/>'
            f'<path d="M-14,8 L-30,22 L-22,30 L-6,18 Z M14,8 L30,22 L22,30 L6,18 Z" fill="{f}"/>'
            f'<rect x="-19" y="-26" width="38" height="50" rx="13" fill="{f}"/>'
            '<path d="M-12,-17 q12,-6 24,0" fill="none" stroke="#fffaea" stroke-width="5" opacity=".75"/>'
            '<path d="M-19,0 l38,0" fill="none" stroke-width="2.5" opacity=".35"/></g>')


def skeleton(f, k, fx=1, skull_rot=0, n=26, nribs=11, flipper=True, tail=1800):
    piv = (525, -240)
    a = math.radians(skull_rot)

    def R(p):
        dx, dy = p[0] - piv[0], p[1] - piv[1]
        return (piv[0] + dx * math.cos(a) - dy * math.sin(a), piv[1] + dx * math.sin(a) + dy * math.cos(a))
    F = lambda p: f(*p)
    sizes = [1 - .1 * i / 13 if i < 14 else .9 - .58 * ((i - 14) / (n - 15)) for i in range(n)]
    cum = [0]
    for s in sizes[:-1]:
        cum.append(cum[-1] + s)
    sp = ((545, -238), (950, -278), (tail - 380, -250), (tail, -62))
    verts = []
    for i in range(n):
        t = cum[i] / cum[-1]; p = cb(*sp, t); q = cb(*sp, min(1, t + .01)); q0 = cb(*sp, max(0, t - .01))
        S0, S1 = F(q0), F(q)
        rot = math.degrees(math.atan2(S1[1] - S0[1], (S1[0] - S0[0]) * fx)) * fx
        verts.append((p, sizes[i], rot))
    far = near = vs = ''
    ribs = []
    for j in range(1, nribs + 1):
        (vx, vy), s, _ = verts[j]
        fr = 1.0 - .48 * (j - 1) / (nribs - 1)
        h = (-vy - 14) * fr
        for off, dark in (((22, -12), True), ((0, 0), False)):
            bx, by = vx + off[0], vy + off[1]
            c = [(bx, by + 16), (bx - 70, by + h * .34), (bx - 34, by + h * .94), (bx + 44, by + h)]
            C = [F(p) for p in c]; kk = k(bx)
            d = f'M{C[0][0]:.1f},{C[0][1]:.1f} C{C[1][0]:.1f},{C[1][1]:.1f} {C[2][0]:.1f},{C[2][1]:.1f} {C[3][0]:.1f},{C[3][1]:.1f}'
            w = 20 * kk * (1.05 - .3 * (j - 1) / nribs)
            if dark:
                far += f'<path d="{d}" stroke="#20180f" stroke-width="{w + 6 * kk:.1f}" fill="none" stroke-linecap="round"/><path d="{d}" stroke="#7a6a4f" stroke-width="{w * .85:.1f}" fill="none" stroke-linecap="round"/>'
            else:
                near += f'<path d="{d}" stroke="{OUT}" stroke-width="{w + 8 * kk:.1f}" fill="none" stroke-linecap="round"/><path d="{d}" stroke="#ead9b0" stroke-width="{w:.1f}" fill="none" stroke-linecap="round"/>'
                near += f'<path d="{d}" stroke="#fffbee" stroke-width="{w * .3:.1f}" fill="none" stroke-linecap="round" opacity=".85" transform="translate({-2.5 * kk * fx:.1f} {-3 * kk:.1f})"/>'
                ribs.append(C)
    tops = []
    for (p, s, rot) in verts:
        kk = k(p[0]); X, Y = F(p)
        vs += vert(X, Y, s * kk, fx, rot)
        tops.append((X, Y, s * kk))
    # skull + lower jaw
    jaw = [F(R(p)) for p in chain(JAW)]
    sk = [F(R(p)) for p in chain(SK_TOP + SK_BOT)]
    kh = k(250)
    g = f'<polygon points="{P(jaw)}" fill="url(#bone)" stroke="{OUT}" stroke-width="{7 * kh:.1f}" stroke-linejoin="round"/>'
    jt = [F(R(p)) for p in chain([JAW[0]])]
    g += f'<path d="{spline_d(jt[2:-1])}" fill="none" stroke="#fffaea" stroke-width="{5 * kh:.1f}" opacity=".8" transform="translate(0 {4 * kh:.1f})"/>'
    g += f'<polygon points="{P(sk)}" fill="url(#skullG)" stroke="{OUT}" stroke-width="{7.5 * kh:.1f}" stroke-linejoin="round"/>'
    tp = [F(R(p)) for p in chain(SK_TOP)]
    g += f'<path d="{spline_d(tp[2:-2])}" fill="none" stroke="#fffdf4" stroke-width="{8 * kh:.1f}" opacity=".9" transform="translate(0 {7 * kh:.1f})"/>'
    # maxilla line along the rostrum, blowhole slot, eye socket, cheek arch
    ml = [F(R(cb((390, -232), (260, -200), (120, -150), (30, -126), i / 16))) for i in range(17)]
    g += f'<path d="{spline_d(ml)}" fill="none" stroke="#8a744f" stroke-width="{4 * kh:.1f}" opacity=".8"/>'
    for (cx, cy, rx, ry, col) in ((436, -196, 30, 22, '#2a1d10'), (338, -290, 22, 8, '#4a3820')):
        X, Y = F(R((cx, cy)))
        g += f'<ellipse cx="{X:.1f}" cy="{Y:.1f}" rx="{rx * kh:.1f}" ry="{ry * kh:.1f}" fill="{col}" stroke="{OUT}" stroke-width="{3 * kh:.1f}" transform="rotate({skull_rot * fx - 8 * fx:.1f} {X:.1f} {Y:.1f})"/>'
    ca = [F(R(cb((470, -170), (430, -150), (380, -160), (330, -158), i / 10))) for i in range(11)]
    g += f'<path d="{spline_d(ca)}" fill="none" stroke="#7d6644" stroke-width="{4 * kh:.1f}" opacity=".7"/>'
    # flipper lying in front of the chest: forearm + finger bones
    fl = ''
    if flipper:
        kf = k(600)
        segs = [((640, -150), (600, -84), 20), ((600, -84), (540, -50), 15), ((606, -80), (548, -40), 12)]
        for d0 in range(4):
            x0, y0 = 540 - d0 * 2, -48 + d0 * 9
            for b in range(4 - d0 // 2):
                x1, y1 = x0 - 38 + d0 * 4, y0 + 4 + d0 * 3
                segs.append(((x0, y0), (x1, y1), 9 - b))
                x0, y0 = x1 - 6, y1 + 1
        for (p0, p1, w) in segs:
            A0, A1 = F(p0), F(p1)
            fl += f'<path d="M{A0[0]:.1f},{A0[1]:.1f} L{A1[0]:.1f},{A1[1]:.1f}" stroke="{OUT}" stroke-width="{(w + 7) * kf:.1f}" stroke-linecap="round"/>'
            fl += f'<path d="M{A0[0]:.1f},{A0[1]:.1f} L{A1[0]:.1f},{A1[1]:.1f}" stroke="#dcc89c" stroke-width="{w * kf:.1f}" stroke-linecap="round"/>'
    svgs = far + vs + near + fl + g
    info = {'tip': F(R((0, -122))), 'jawtip': F(R((14, -52))), 'tops': tops, 'ribs': ribs,
            'skulltop': [F(R(p)) for p in chain(SK_TOP, 6)], 'neck': F(R((470, -300)))}
    return svgs, info


def hag(p0, p1, p2, p3, w, slime=True):
    N = 40; pts = [cb(p0, p1, p2, p3, i / N) for i in range(N + 1)]
    L, Rr, nrm = [], [], []
    for i, q in enumerate(pts):
        t = i / N; a = pts[max(i - 1, 0)]; b = pts[min(i + 1, N)]
        tx, ty = b[0] - a[0], b[1] - a[1]; ln = math.hypot(tx, ty) or 1; nx, ny = -ty / ln, tx / ln
        hw = w / 2 * (1 - .62 * t ** 1.4) * (min(1, .6 + t * 12))
        L.append((q[0] + nx * hw, q[1] + ny * hw)); Rr.append((q[0] - nx * hw, q[1] - ny * hw)); nrm.append((nx, ny, hw))
    o = ''
    if slime:
        for sd, op in ((1, .32), (-1, .22)):
            sl = [(q[0] + sd * nrm[i][0] * (nrm[i][2] + w * .45), q[1] + sd * nrm[i][1] * (nrm[i][2] + w * .45)) for i, q in enumerate(pts) if 4 < i < 34]
            o += f'<path d="{spline_d(sl)}" fill="none" stroke="#eef8ff" stroke-width="{w * .35:.1f}" opacity="{op}" stroke-linecap="round" filter="url(#b4)"/>'
        tq, tb = pts[-1], pts[-6]
        for dd in (-1, 1):   # slime strands trailing from the tail
            o += f'<path d="M{tq[0]:.0f},{tq[1]:.0f} q{(tq[0] - tb[0]) * 1.2:.0f},{(tq[1] - tb[1]) * 1.2 + dd * 14:.0f} {(tq[0] - tb[0]) * 2.6:.0f},{(tq[1] - tb[1]) * 2.6 + dd * 6:.0f}" fill="none" stroke="#eef8ff" stroke-width="{w * .16:.1f}" opacity=".5" stroke-linecap="round"/>'
        for i in (12, 26):
            q = pts[i]; nx, ny, hw = nrm[i]
            o += f'<circle cx="{q[0] + nx * (hw + w * .5):.0f}" cy="{q[1] + ny * (hw + w * .5):.0f}" r="{w * .22:.1f}" fill="#eef8ff" fill-opacity=".25" stroke="#eef8ff" stroke-width="2" stroke-opacity=".6"/>'
    # tail fin fold
    fin = [(q[0] + nrm[i][0] * (nrm[i][2] + w * .16), q[1] + nrm[i][1] * (nrm[i][2] + w * .16)) for i, q in enumerate(pts) if i >= 28]
    o += f'<polygon points="{P(L[28:] + fin[::-1])}" fill="#f2b9b3" fill-opacity=".7" stroke="#4a2226" stroke-width="3"/>'
    o += f'<polygon points="{P(L + Rr[::-1])}" fill="#eaa2a6" stroke="#4a2226" stroke-width="4" stroke-linejoin="round"/>'
    o += f'<path d="{spline_d(Rr[3:34])}" fill="none" stroke="#c97f80" stroke-width="{w * .22:.1f}" opacity=".8" transform="translate(0 0)"/>'
    hl = [(q[0] + nrm[i][0] * nrm[i][2] * .45, q[1] + nrm[i][1] * nrm[i][2] * .45) for i, q in enumerate(pts) if 2 < i < 30]
    o += f'<path d="{spline_d(hl)}" fill="none" stroke="#ffe0d8" stroke-width="{w * .18:.1f}" opacity=".85" stroke-linecap="round"/>'
    for i in range(5, 11):   # gill pores
        q = pts[i]; nx, ny, hw = nrm[i]
        o += f'<circle cx="{q[0] - nx * hw * .35:.1f}" cy="{q[1] - ny * hw * .35:.1f}" r="{w * .07:.1f}" fill="#8a4a4c"/>'
    # head: pale eye spot + barbels
    hx, hy = pts[0]; dx, dy = pts[0][0] - pts[2][0], pts[0][1] - pts[2][1]; ln = math.hypot(dx, dy) or 1; dx, dy = dx / ln, dy / ln
    q = pts[3]; nx, ny, hw = nrm[3]
    o += f'<circle cx="{q[0] + nx * hw * .3:.1f}" cy="{q[1] + ny * hw * .3:.1f}" r="{w * .13:.1f}" fill="#fbe3dc" stroke="#7a4144" stroke-width="1.5"/>'
    for ang in (-35, 0, 35):
        r = math.radians(ang); ex, ey = dx * math.cos(r) - dy * math.sin(r), dx * math.sin(r) + dy * math.cos(r)
        o += f'<path d="M{hx:.1f},{hy:.1f} q{ex * w * .5 - ey * 4:.1f},{ey * w * .5 + ex * 4:.1f} {ex * w * .8:.1f},{ey * w * .8:.1f}" fill="none" stroke="#4a2226" stroke-width="5" stroke-linecap="round"/>'
        o += f'<path d="M{hx:.1f},{hy:.1f} q{ex * w * .5 - ey * 4:.1f},{ey * w * .5 + ex * 4:.1f} {ex * w * .8:.1f},{ey * w * .8:.1f}" fill="none" stroke="#f0b4b0" stroke-width="2.2" stroke-linecap="round"/>'
    return o


def affine(X0, Y0, s, fx=1):
    return (lambda x, y: (X0 + fx * s * x, Y0 + s * y)), (lambda x: s)


def persp(X0, Y0, u0, D, dx, dy):
    g = lambda x: D * math.log(1 + x / D)
    k = lambda x: u0 / (1 + x / D)
    return (lambda x, y: (X0 + dx * u0 * g(x), Y0 + dy * u0 * g(x) + y * k(x))), k


def small_whale(x, y, s, rot):
    return (f'<g transform="translate({x} {y}) rotate({rot}) scale({s})" stroke="#0b121c" stroke-width="8" stroke-linejoin="round">'
            '<path d="M230,70 C300,130 380,180 480,214 C420,150 350,100 300,78 Z" fill="#33465a"/>'
            '<path d="M0,0 C10,-55 120,-108 290,-112 C470,-116 640,-78 790,-26 L850,-14 C880,-60 930,-110 995,-132 C965,-80 950,-40 925,-5 '
            'C950,30 965,70 995,124 C930,100 880,50 850,14 L790,24 C640,70 470,100 300,100 C150,98 45,62 0,0 Z" fill="url(#whale)"/>'
            '<path d="M8,-20 C40,-80 140,-108 290,-112 C470,-116 640,-78 790,-26" fill="none" stroke="#e6fbff" stroke-width="12" opacity=".8"/>'
            '<circle cx="150" cy="16" r="12" fill="#0b121c"/></g>')


# ====================================================================== A
def thumb_A():
    random.seed(11)
    defs = FILTERS + BONE + SKULLG
    defs += lin('bgA', [(0, '#0f3d40'), (.5, '#0a2627'), (1, '#040d0e')])
    defs += lin('floorA', [(0, '#16332e'), (1, '#050c0b')])
    defs += '<linearGradient id="beamF" x1="430" y1="900" x2="1300" y2="480" gradientUnits="userSpaceOnUse"><stop offset="0" stop-color="#fff2c2" stop-opacity=".6"/><stop offset="1" stop-color="#ffe9b0" stop-opacity=".03"/></linearGradient>'
    defs += rad('glowA', 1200, 520, 560, [(0, '#ff6f6a', .4), (.45, '#ff5a5a', .12), (1, '#ff5a5a', 0)])
    defs += rad('poolA', 1050, 860, 700, [(0, '#bff0dc', .30), (.5, '#9fe0c8', .08), (1, '#9fe0c8', 0)])
    defs += rad('vigA', 960, 540, 1150, [(0, '#000', 0), (.7, '#000', 0), (1, '#000', .55)])
    b = '<rect width="1920" height="1080" fill="url(#bgA)"/>'
    b += '<rect width="1920" height="1080" fill="url(#glowA)"/>'
    b += snow(160, 0, 0, 1920, 900, '#cfe7e0', .4)
    b += '<path d="M0,820 C300,800 600,840 900,820 C1200,800 1500,760 1920,730 L1920,1080 L0,1080 Z" fill="url(#floorA)"/>'
    b += ''.join(f'<ellipse cx="{random.randint(0, 1920)}" cy="{random.randint(840, 1070)}" rx="{random.randint(20, 70)}" ry="{random.randint(4, 10)}" fill="#24433c" opacity=".5"/>' for _ in range(30))
    b += '<rect width="1920" height="1080" fill="url(#poolA)"/>'
    # torch beam from the frog onto the skull/ribs
    b += '<path d="M430,900 L1150,430 L1340,860 Z" fill="url(#beamF)" filter="url(#b10)"/>'
    f, k = persp(560, 940, 1.12, 1700, .975, -.19)
    sk, info = skeleton(f, k, 1)
    b += '<ellipse cx="1180" cy="900" rx="720" ry="70" fill="#000" opacity=".45" filter="url(#b24)"/>'
    b += '<ellipse cx="1150" cy="860" rx="640" ry="90" fill="#e8fff4" opacity=".12" filter="url(#b24)"/>'
    b += sk
    # bacterial mats
    b += ''.join(f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="10" fill="#f4fbf2" opacity=".35" filter="url(#b4)"/>' for x, y, rx in ((760, 920, 90), (1250, 850, 80), (1600, 780, 60)))
    # zombie worms blooming on spine and ribs (a red forest)
    worms = []
    for i in (3, 11, 15, 19):
        X, Y, s = info['tops'][i]
        worms.append((Y, osedax(X - 4 * s, Y - 26 * s, 40 * s + 20, .30 + .34 * s, random.uniform(-12, 12), .8)))
    for j, C in enumerate(info['ribs']):
        if j % 2 == 1 or j == 0:
            for t in ((.45,) if j % 4 else (.35, .7)):
                q = cb(*C, t)
                worms.append((q[1], osedax(q[0] - 8, q[1], 22, .26 + .08 * (j < 6), random.uniform(-10, 6), .7)))
    for _, w in sorted(worms):
        b += w
    # hero worm on the spine, glowing
    X, Y, s = info['tops'][8]
    b += f'<ellipse cx="{X + 10:.0f}" cy="{Y - 300:.0f}" rx="230" ry="170" fill="#ff3048" opacity=".35" filter="url(#b50)"/>'
    b += osedax(X, Y - 30, 210, 1.75, 26, 1.2)
    b += spark(X - 240, Y - 340, 22) + spark(X + 300, Y - 400, 16) + spark(X + 280, Y - 120, 12) + spark(1760, 300, 18)
    b += bubbles(X + 60, Y - 540, 4, 30, 160, .8)
    b += crab(1440, 770, .75, rot=-8) + isopod(1700, 700, .7, flip=True, rot=-6)
    torch = ('<g transform="translate(60 -36) rotate(-38)"><rect x="-6" y="-9" width="40" height="18" rx="5" fill="#8a929e" stroke-width="3"/>'
             '<rect x="30" y="-13" width="12" height="26" rx="3" fill="#c9ced6" stroke-width="3"/><ellipse cx="43" cy="0" rx="3" ry="11" fill="#fff6c8" stroke="none"/></g>')
    b += frog(300, 1020, 2.6, mouth='o', arms='fwd', look=(4, -3), front=torch)
    b += bubbles(340, 720, 5, 30, 160, 1.0)
    b += '<rect width="1920" height="1080" fill="url(#vigA)"/>'
    lines = [('WHERE IS', 140, 'w'), ('ITS', 140, 'w'), ('MOUTH?', 236, 'y')]
    return page('#0a2627', svg(defs, b), lines, outline='#061314')


# ====================================================================== B
def thumb_B():
    random.seed(22)
    defs = FILTERS + BONE + SKULLG
    defs += lin('bgB', [(0, '#123c4a'), (.45, '#0b2833'), (1, '#03090d')])
    defs += lin('floorB', [(0, '#1a3a3e'), (1, '#040a0c')])
    defs += '<linearGradient id="beamB" x1="1530" y1="230" x2="1250" y2="820" gradientUnits="userSpaceOnUse"><stop offset="0" stop-color="#fff4cf" stop-opacity=".7"/><stop offset="1" stop-color="#fff0c0" stop-opacity=".06"/></linearGradient>'
    defs += lin('subW', [(0, '#ffffff'), (1, '#9aa7b0')])
    defs += rad('poolB', 1250, 760, 640, [(0, '#fff1c4', .32), (.5, '#ffe4a0', .1), (1, '#ffe4a0', 0)])
    defs += rad('vigB', 960, 560, 1150, [(0, '#000', 0), (.65, '#000', 0), (1, '#000', .6)])
    beams = '<path d="M1505,215 L1000,880 L1420,920 L1530,238 Z"/><path d="M1540,240 L1480,900 L1760,830 L1560,236 Z"/>'
    defs += f'<clipPath id="beamclip">{beams}</clipPath>'
    b = '<rect width="1920" height="1080" fill="url(#bgB)"/>'
    b += snow(200, 0, 0, 1920, 1000, '#bcd8d6', .3, 2.2)
    b += '<path d="M1700,800 C1760,750 1850,740 1920,760 L1920,820 L1700,820Z" fill="#0d2a30" opacity=".8"/>'
    b += '<path d="M0,900 C300,890 700,920 1000,905 C1300,890 1600,910 1920,890 L1920,1080 L0,1080Z" fill="url(#floorB)"/>'
    b += ''.join(f'<ellipse cx="{random.randint(0, 1920)}" cy="{random.randint(920, 1070)}" rx="{random.randint(20, 80)}" ry="{random.randint(4, 10)}" fill="#24474a" opacity=".45"/>' for _ in range(30))
    b += '<rect width="1920" height="1080" fill="url(#poolB)"/>'
    b += f'<g fill="url(#beamB)" filter="url(#b10)">{beams}</g>'
    f, k = affine(1560, 935, .8, -1)
    sk, info = skeleton(f, k, -1, skull_rot=40)
    b += '<ellipse cx="900" cy="925" rx="720" ry="50" fill="#000" opacity=".5" filter="url(#b24)"/>'
    b += '<path d="M1080,930 C1180,860 1330,850 1460,880 C1560,900 1600,925 1560,945 L1060,950 Z" fill="#2a4448"/>'   # silt mound under the raised skull
    b += sk
    for i in (3, 7, 12, 18):
        X, Y, s = info['tops'][i]; b += tuft(X, Y - 60 * s, 1.0)
    for x, y in info['skulltop'][3:10:2]:
        b += tuft(x, y + 4, 1.1)
    b += crab(1290, 905, .8, rot=-10) + crab(560, 915, .7, col='#d9562f', rot=5)
    b += isopod(300, 975, .8)
    b += hag((760, 1000), (700, 980), (640, 1030), (520, 1000), 26)
    # frog on the tip of the skull, arms wide (the bow pose)
    tx, ty = info['tip']
    b += frog(tx + 26, ty + 10, 2.2, mouth='smile', arms='wide', look=(-2, -1))
    b += bubbles(tx, ty - 290, 4, 20, 110, .9)
    sub = ('<g transform="translate(1660 170)" stroke="#16222a" stroke-width="5" stroke-linejoin="round">'
           '<rect x="-30" y="-92" width="80" height="50" rx="14" fill="#d8402f"/><rect x="-20" y="-86" width="40" height="8" rx="3" fill="#f58a72" stroke="none"/>'
           '<path d="M-150,0 C-150,-60 -90,-70 0,-70 C110,-70 170,-50 170,0 C170,50 110,70 0,70 C-90,70 -150,60 -150,0 Z" fill="url(#subW)"/>'
           '<path d="M-130,-20 C-120,-52 -60,-60 40,-60" fill="none" stroke="#fff" stroke-width="7" opacity=".8"/>'
           '<rect x="-120" y="44" width="250" height="26" rx="10" fill="#e8b33a"/>'
           '<circle cx="-118" cy="10" r="20" fill="#3a6f8a"/><circle cx="-124" cy="4" r="6" fill="#d9f2ff" stroke="none"/>'
           '<path d="M170,-6 l40,-22 l0,56 l-40,-22" fill="#8c98a2"/>'
           '<rect x="-160" y="34" width="34" height="18" rx="6" fill="#9aa5ae"/><circle cx="-155" cy="44" r="9" fill="#fff8d8"/>'
           '<rect x="-130" y="60" width="26" height="16" rx="5" fill="#9aa5ae"/></g>')
    b += '<circle cx="1508" cy="214" r="40" fill="#fff4cf" opacity=".7" filter="url(#b10)"/><circle cx="1540" cy="238" r="34" fill="#fff4cf" opacity=".6" filter="url(#b10)"/>'
    b += sub
    b += f'<g clip-path="url(#beamclip)">{snow(260, 1000, 200, 1800, 900, "#fffbe8", .9, 3.2)}</g>'
    b += fish(1250, 470, 1.1, '#cfe3e0', flip=True) + fish(1190, 520, .8, '#cfe3e0', flip=True) + fish(1760, 560, .9, '#cfe3e0')
    b += spark(1400, 420, 18) + spark(1760, 400, 14) + spark(1000, 640, 12)
    b += '<rect width="1920" height="1080" fill="url(#vigB)"/>'
    lines = [('UNKNOWN', 176, 'w'), ('UNTIL', 120, 'w'), ('1987', 260, 'y')]
    return page('#0b2833', svg(defs, b), lines, outline='#04131a')


# ====================================================================== C
def thumb_C():
    random.seed(33)
    defs = FILTERS + BONE + SKULLG
    defs += lin('bgC', [(0, '#2f93a6'), (.3, '#145a72'), (.62, '#0b2a45'), (1, '#050a16')])
    defs += lin('floorC', [(0, '#1b2c45'), (1, '#05070f')])
    defs += lin('whale', [(0, '#8fb0c0'), (.35, '#50697d'), (.7, '#2a3a4d'), (1, '#141d2a')])
    defs += rad('haloC', 1620, 200, 420, [(0, '#bff3ff', .4), (.5, '#9fe6ff', .1), (1, '#9fe6ff', 0)])
    defs += rad('poolC', 1150, 800, 760, [(0, '#a8f0ff', .26), (.5, '#7fd8f0', .08), (1, '#7fd8f0', 0)])
    defs += rad('vigC', 960, 520, 1150, [(0, '#000', 0), (.7, '#000', 0), (1, '#000', .5)])
    defs += '<linearGradient id="rayg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#eafcff" stop-opacity=".4"/><stop offset="1" stop-color="#eafcff" stop-opacity="0"/></linearGradient>'
    b = '<rect width="1920" height="1080" fill="url(#bgC)"/>'
    b += ''.join(f'<path d="M{x},0 L{x + w},0 L{x - 200 + w * 2},{800} L{x - 360},{800} Z" fill="url(#rayg)" opacity="{o}" filter="url(#b10)"/>'
                 for x, w, o in ((1350, 70, .5), (1600, 50, .45), (1760, 80, .5), (1150, 40, .3)))
    b += '<rect width="1920" height="1080" fill="url(#haloC)"/>'
    b += snow(220, 0, 0, 1920, 1000, '#e6f6ff', .4)
    # small whale far above, still sinking (the next meal)
    b += small_whale(1520, 330, .38, -28)
    b += bubbles(1700, 210, 4, 16, 90, .5)
    b += '<path d="M0,880 C300,862 700,895 1000,878 C1300,862 1600,872 1920,860 L1920,1080 L0,1080Z" fill="url(#floorC)"/>'
    b += ''.join(f'<ellipse cx="{random.randint(0, 1920)}" cy="{random.randint(900, 1070)}" rx="{random.randint(20, 80)}" ry="{random.randint(4, 10)}" fill="#2a3d5c" opacity=".45"/>' for _ in range(30))
    b += '<rect width="1920" height="1080" fill="url(#poolC)"/>'
    f, k = affine(410, 915, .88, 1)
    sk, info = skeleton(f, k, 1, tail=1680)
    b += '<ellipse cx="1150" cy="900" rx="760" ry="55" fill="#000" opacity=".45" filter="url(#b24)"/>'
    b += '<ellipse cx="1150" cy="860" rx="700" ry="110" fill="#dff8ff" opacity=".14" filter="url(#b24)"/>'
    # hagfish behind the bones
    b += hag((1180, 760), (1240, 700), (1320, 800), (1420, 740), 30)
    b += sk
    for i in (4, 9, 15, 21):
        X, Y, s = info['tops'][i]; b += tuft(X, Y - 60 * s, .9)
    # scavengers: hagfish weaving through ribs, crabs on the bones, isopods on the floor
    b += hag((900, 820), (960, 760), (1040, 860), (1130, 800), 32)
    b += hag((640, 930), (720, 900), (800, 960), (900, 935), 30)
    b += hag((1460, 860), (1400, 820), (1350, 880), (1270, 850), 26)
    X, Y, s = info['tops'][6]; b += crab(X + 4, Y - 64 * s, .8, rot=-6)
    X, Y, s = info['tops'][16]; b += crab(X, Y - 56 * s, .62, col='#d9562f', rot=8)
    b += isopod(1060, 925, .95, rot=-4) + isopod(1500, 905, .85, flip=True, rot=6)
    b += crab(760, 905, .8, rot=6)
    b += spark(1060, 520, 18) + spark(1800, 520, 16) + spark(1280, 300, 14)
    napkin = '<path d="M-14,-24 L26,-24 L32,-2 L6,10 L-20,-2 Z" fill="#fbfbf4" stroke-width="3"/><circle cx="6" cy="-12" r="2.5" fill="#d84848" stroke="none"/><circle cx="16" cy="-4" r="2.5" fill="#d84848" stroke="none"/><circle cx="-4" cy="-4" r="2.5" fill="#d84848" stroke="none"/>'
    cutlery = ('<g stroke-width="3"><path d="M-54,-40 l0,-34" stroke-width="6"/><path d="M-54,-40 l0,-34" stroke="#d9dee6" stroke-width="3"/>'
               '<path d="M-62,-74 l0,-12 M-54,-74 l0,-14 M-46,-74 l0,-12 M-62,-74 q8,6 16,0" fill="none" stroke="#d9dee6" stroke-width="3.2"/>'
               '<path d="M58,-40 l0,-30 q10,-14 2,-30 l-4,0 z" fill="#d9dee6"/></g>')
    b += frog(225, 1020, 2.45, mouth='o', arms='fork', look=(4, -3), front=napkin + cutlery)
    b += '<rect width="1920" height="1080" fill="url(#vigC)"/>'
    lines = [('FEEDS THE DEEP', 140, 'w'), ('FOR DECADES', 198, 'y')]
    return page('#0b2a45', svg(defs, b), lines, outline='#061222')


for n, fn in (('A', thumb_A), ('B', thumb_B), ('C', thumb_C)):
    open(os.path.join(HERE, f'{n}.html'), 'w').write(fn())
print('ok')
