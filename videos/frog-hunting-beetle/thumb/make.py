# Thumbnails A-C for frog-hunting-beetle (guideline 16-6/16-8, brief tools/briefs/thumb_art.md). Run: python3 videos/frog-hunting-beetle/thumb/make.py
# A  IT / DODGES / THE TONGUE     homage: The Matrix (1999) bullet-time dodge -> the larva arches back, the frog's tongue streaks past with
#                                 ripple wakes (S25 "almost always dodges the strike", S80 "slips the tongue and bites on")
# B  WORM / OR / TRAP?            intuitive: the mascot's flashlight finds a "worm" waving on the mud, its shadow on the rock shows hooked jaws
#                                 (S16 "can look like a worm", S06 "it is a trap", S69 "a worm or a trap")
# C  BUG WINS / NEARLY / 100%     homage: The Silence of the Lambs poster (pale face, moth over the mouth) -> pale frog face, larva over its mouth
#                                 (S39 "success rate of close to one hundred percent" -> hedged NEARLY; S29 "the tongue ... is now useless")
# Mascot: A peeks over a pebble with slipping sunglasses; B holds the flashlight; C covers its own mouth. No blood or wounds anywhere.
import os, sys, math, random
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../tools'))
from thumb_lib import page, svg, lin, rad, spark

INK = '#1d2b1c'; GREEN = '#6aa55a'
random.seed(11)

FILTERS = ''.join(f'<filter id="b{k}" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="{k}"/></filter>'
                  for k in (2, 4, 8, 14, 24, 40, 60))


# ---------------- geometry helpers ----------------
def cb(p0, p1, p2, p3, t):
    u = 1 - t
    return tuple(u ** 3 * p0[i] + 3 * u * u * t * p1[i] + 3 * u * t * t * p2[i] + t ** 3 * p3[i] for i in (0, 1))


def qb(p0, p1, p2, t):
    u = 1 - t
    return tuple(u * u * p0[i] + 2 * u * t * p1[i] + t * t * p2[i] for i in (0, 1))


def norm(v):
    L = math.hypot(*v) or 1e-6
    return (v[0] / L, v[1] / L)


def rotv(v, deg):
    a = math.radians(deg); c, s = math.cos(a), math.sin(a)
    return (v[0] * c - v[1] * s, v[0] * s + v[1] * c)


def add(a, b, k=1.0):
    return (a[0] + b[0] * k, a[1] + b[1] * k)


def taper(pts, w0, w1, cap=True):
    """closed path of a tapered ribbon along pts (width w0 -> w1)"""
    n = len(pts); L, R = [], []
    for i, p in enumerate(pts):
        a = pts[max(0, i - 1)]; b = pts[min(n - 1, i + 1)]
        t = norm((b[0] - a[0], b[1] - a[1])); nn = (-t[1], t[0])
        w = (w0 + (w1 - w0) * i / (n - 1)) / 2
        L.append(add(p, nn, w)); R.append(add(p, nn, -w))
    d = 'M' + ' L'.join(f'{x:.1f},{y:.1f}' for x, y in L)
    if cap:
        d += f' A{w1 / 2:.1f},{w1 / 2:.1f} 0 0 1 {R[-1][0]:.1f},{R[-1][1]:.1f}'
    d += ' L' + ' L'.join(f'{x:.1f},{y:.1f}' for x, y in reversed(R)) + 'Z'
    return d


def poly(pts):
    return 'M' + ' L'.join(f'{x:.1f},{y:.1f}' for x, y in pts)


# ---------------- Epomis larva ----------------
PROF = [0.40, 0.52, 0.63, 0.73, 0.82, 0.90, 0.96, 1.0, 0.96, 0.9, 0.84]


def larva(P, W, opn=0.35, head_rot=0, ants=((-28, 3.4, -30), (28, 3.4, 30)), legs='walk', vside=1,
          light=(-0.6, -0.8), sil=None, wave=False, rim='#fff1c4', glow=None):
    """P = (tail, c1, c2, neck) cubic spine; W = max half-width. vside +1: ventral side = left normal of tail->head direction."""
    pts = [cb(*P, i / 80) for i in range(81)]
    acc = [0]
    for i in range(1, 81):
        acc.append(acc[-1] + math.dist(pts[i], pts[i - 1]))
    Ltot = acc[-1]; N = len(PROF); seg = Ltot / N

    def at(s):
        for i in range(1, 81):
            if acc[i] >= s:
                f = (s - acc[i - 1]) / max(1e-6, acc[i] - acc[i - 1])
                p = (pts[i - 1][0] + (pts[i][0] - pts[i - 1][0]) * f, pts[i - 1][1] + (pts[i][1] - pts[i - 1][1]) * f)
                return p, norm((pts[i][0] - pts[i - 1][0], pts[i][1] - pts[i - 1][1]))
        return pts[-1], norm((pts[-1][0] - pts[-2][0], pts[-1][1] - pts[-2][1]))

    S = []
    for i in range(N):
        c, t = at(seg * (i + 0.5))
        nv = (-t[1] * vside, t[0] * vside)                    # ventral normal
        S.append((c, t, nv, W * PROF[i]))
    body = sil or 'url(#lvb)'; ol = sil or '#24120a'; lw = 0 if sil else W * 0.07
    leg_col = sil or '#b07a3c'; dark = sil or '#24120a'
    out = []
    # legs on the three thorax segments
    A_walk = [(48, 30), (10, 0), (-30, -40)]
    A_flail = [(80, 120), (25, 70), (-25, 10)]
    angs = A_flail if legs == 'flail' else A_walk

    def leg(k, far):
        c, t, nv, w = S[N - 3 + k]
        a1, a2 = angs[2 - k]
        if far:
            a1 += 14; a2 += 14
        d1 = norm(add(rotv(nv, 0), t, 0)); d1 = norm((nv[0] * math.cos(math.radians(a1)) + t[0] * math.sin(math.radians(a1)),
                                                        nv[1] * math.cos(math.radians(a1)) + t[1] * math.sin(math.radians(a1))))
        d2 = norm((nv[0] * math.cos(math.radians(a2)) + t[0] * math.sin(math.radians(a2)),
                   nv[1] * math.cos(math.radians(a2)) + t[1] * math.sin(math.radians(a2))))
        base = add(c, nv, w * (0.35 if far else 0.55))
        knee = add(base, d1, W * 1.15); foot = add(knee, d2, W * 1.3)
        claw = add(foot, d2, W * 0.25)
        dd = poly([base, knee, foot, claw])
        o = ''
        if not sil:
            o += f'<path d="{dd}" fill="none" stroke="{dark}" stroke-width="{W * 0.27:.1f}" stroke-linecap="round" stroke-linejoin="round"/>'
            o += f'<path d="{dd}" fill="none" stroke="{"#7a4e22" if far else leg_col}" stroke-width="{W * 0.15:.1f}" stroke-linecap="round" stroke-linejoin="round"/>'
        else:
            o += f'<path d="{dd}" fill="none" stroke="{sil}" stroke-width="{W * 0.22:.1f}" stroke-linecap="round" stroke-linejoin="round"/>'
        return o

    out += [leg(k, True) for k in range(3)]
    # urogomphi (tail spines)
    c0, t0, nv0, w0 = S[0]
    for sg in (-1, 1):
        a = add(c0, t0, -w0 * 0.6); b = add(add(a, t0, -W * 1.2), nv0, -sg * W * 0.45 - W * 0.25)
        out.append(f'<path d="{taper([a, ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2), b], W * 0.22, 2, cap=False)}" fill="{dark}"/>')
    # segments
    for i, (c, t, nv, w) in enumerate(S):
        ang = math.degrees(math.atan2(t[1], t[0]))
        rx = seg * 0.74
        out.append(f'<ellipse cx="{c[0]:.1f}" cy="{c[1]:.1f}" rx="{rx:.1f}" ry="{w:.1f}" transform="rotate({ang:.1f} {c[0]:.1f} {c[1]:.1f})" '
                   f'fill="{body}" stroke="{ol}" stroke-width="{lw:.1f}"/>')
        if not sil:
            dc = add(c, nv, -w * 0.28)
            out.append(f'<ellipse cx="{dc[0]:.1f}" cy="{dc[1]:.1f}" rx="{rx * 0.78:.1f}" ry="{w * 0.5:.1f}" transform="rotate({ang:.1f} {dc[0]:.1f} {dc[1]:.1f})" '
                       f'fill="#8a4f1e" opacity=".42"/>')
            sp = add(add(c, nv, w * 0.25), t, -rx * 0.3)
            out.append(f'<circle cx="{sp[0]:.1f}" cy="{sp[1]:.1f}" r="{W * 0.06:.1f}" fill="#5a3010" opacity=".7"/>')
    # rim light along the lit flank
    if not sil:
        lv = norm(light); rp = []
        for c, t, nv, w in S:
            n1 = (-t[1], t[0]); n1 = n1 if n1[0] * lv[0] + n1[1] * lv[1] > 0 else (-n1[0], -n1[1])
            rp.append(add(c, n1, w * 0.72))
        out.append(f'<path d="{poly(rp)}" fill="none" stroke="{rim}" stroke-width="{W * 0.13:.1f}" stroke-linecap="round" opacity=".85" filter="url(#b2)"/>')
    out += [leg(k, False) for k in range(3)]
    # head
    cN, tN, nvN, wN = S[-1]
    d = norm(rotv(tN, head_rot)); s = (-d[1] * vside, d[0] * vside)
    H = add(cN, tN, seg * 0.55 + W * 0.55)
    hx, hy = W * 1.0, W * 0.82
    hang = math.degrees(math.atan2(d[1], d[0]))
    # mandibles (behind the head front)
    Lm = W * 2.45
    for sg in (-1, 1):
        B = add(add(H, d, hx * 0.82), s, sg * hy * 0.42)
        o = opn
        c1 = add(add(B, d, Lm * 0.45), s, sg * Lm * (0.22 + o))
        c2 = add(add(B, d, Lm * 1.0), s, sg * Lm * (0.12 + o * 0.7))
        T = add(add(B, d, Lm * 1.05), s, -sg * Lm * (0.08 - o * 0.25))
        mp = [cb(B, c1, c2, T, k / 20) for k in range(21)]
        out.append(f'<path d="{taper(mp, W * 0.46, W * 0.06)}" fill="{sil or "#3b1a0b"}" stroke="{ol}" stroke-width="{lw * 0.8:.1f}" stroke-linejoin="round"/>')
        if not sil:
            out.append(f'<path d="{poly(mp[3:15])}" fill="none" stroke="#c9874a" stroke-width="{W * 0.07:.1f}" stroke-linecap="round" opacity=".8" transform="translate({-s[0] * sg * 2:.1f} {-s[1] * sg * 2:.1f})"/>')
            tooth = mp[9]; tb = add(tooth, s, -sg * W * 0.18)
            out.append(f'<path d="M{mp[8][0]:.1f},{mp[8][1]:.1f} L{add(tb, d, W * 0.1)[0]:.1f},{add(tb, d, W * 0.1)[1]:.1f} L{mp[11][0]:.1f},{mp[11][1]:.1f}Z" fill="#3b1a0b"/>')
    out.append(f'<ellipse cx="{H[0]:.1f}" cy="{H[1]:.1f}" rx="{hx:.1f}" ry="{hy:.1f}" transform="rotate({hang:.1f} {H[0]:.1f} {H[1]:.1f})" '
               f'fill="{sil or "url(#lvh)"}" stroke="{ol}" stroke-width="{lw:.1f}"/>')
    if not sil:
        for sg in (-1, 1):   # stemmata (tiny eye clusters)
            e = add(add(H, d, hx * 0.25), s, sg * hy * 0.48)
            for k in range(3):
                ee = add(e, d, (k - 1) * W * 0.13)
                out.append(f'<circle cx="{ee[0]:.1f}" cy="{ee[1]:.1f}" r="{W * 0.07:.1f}" fill="#120804"/>')
        hl = add(add(H, d, -hx * 0.2), s, -hy * 0.35)
        out.append(f'<ellipse cx="{hl[0]:.1f}" cy="{hl[1]:.1f}" rx="{hx * 0.45:.1f}" ry="{hy * 0.2:.1f}" transform="rotate({hang:.1f} {hl[0]:.1f} {hl[1]:.1f})" fill="#ffe2a6" opacity=".55"/>')
    # antennae
    for k, (off, lf, curl) in enumerate(ants):
        sg = -1 if off < 0 else 1
        A0 = add(add(H, d, hx * 0.55), s, sg * hy * 0.55)
        L = W * lf
        dir1 = rotv(d, off * vside); dir2 = rotv(d, (off + curl) * vside)
        A1 = add(A0, dir1, L * 0.55); A2 = add(A1, dir2, L * 0.5)
        ap = [qb(A0, A1, A2, j / 24) for j in range(25)]
        out.append(f'<path d="{taper(ap, W * 0.2, W * 0.08)}" fill="{sil or "#6b3b16"}" stroke="{ol}" stroke-width="{lw * 0.7:.1f}"/>')
        if not sil:
            for j in range(3, 25, 3):
                p = ap[j]
                out.append(f'<circle cx="{p[0]:.1f}" cy="{p[1]:.1f}" r="{W * (0.12 - j * 0.002):.1f}" fill="#c98a45" stroke="#24120a" stroke-width="{W * 0.03:.1f}"/>')
        if wave and not sil:  # motion arcs at the tips
            tp = ap[-1]; tn = norm((ap[-1][0] - ap[-4][0], ap[-1][1] - ap[-4][1])); pn = (-tn[1], tn[0])
            for r in (1.0, 1.7):
                a = add(add(tp, pn, W * 0.6 * r), tn, -W * 0.6 * r); b = add(add(tp, pn, -W * 0.6 * r), tn, -W * 0.6 * r)
                cc = add(tp, tn, W * 0.5 * r)
                out.append(f'<path d="M{a[0]:.1f},{a[1]:.1f} Q{cc[0]:.1f},{cc[1]:.1f} {b[0]:.1f},{b[1]:.1f}" fill="none" stroke="#fff3c4" stroke-width="{W * 0.09:.1f}" stroke-linecap="round" opacity="{.8 / r:.2f}"/>')
    return ''.join(out)


LARVA_DEFS = ('<radialGradient id="lvb" cx=".45" cy=".35" r=".7"><stop offset="0" stop-color="#fbe7b0"/><stop offset=".55" stop-color="#e2ad5f"/>'
              '<stop offset="1" stop-color="#9a5f26"/></radialGradient>'
              '<radialGradient id="lvh" cx=".4" cy=".35" r=".75"><stop offset="0" stop-color="#e2a35a"/><stop offset=".6" stop-color="#a25a22"/>'
              '<stop offset="1" stop-color="#4e260e"/></radialGradient>')


# ---------------- mascot frog (tools/assets/frog.svg body) ----------------
def frog(x, y, s, mouth='o', arms=('M-34 -22 q-14 6 -16 22', 'M38 -22 q14 6 16 22'), look=(2, 0), front='', back='', flip=False, rim=None):
    sx = -s if flip else s
    g = f'<g transform="translate({x} {y}) scale({sx} {s})" stroke="{INK}" stroke-linejoin="round" stroke-linecap="round">' + back
    g += '<ellipse cx="-22" cy="4" rx="16" ry="9" fill="#4d8a4a" stroke-width="3.2"/><ellipse cx="22" cy="4" rx="16" ry="9" fill="#4d8a4a" stroke-width="3.2"/>'
    g += f'<path d="M-34 0 q-6 -64 34 -70 q40 -2 42 62 q0 10 -6 12 q-36 6 -70 -4z" fill="{GREEN}" stroke-width="4"/>'
    g += '<ellipse cx="2" cy="-12" rx="22" ry="20" fill="#9cc98a" stroke="none" opacity=".7"/>'
    g += '<path d="M-26 -50 q6 -16 22 -18" fill="none" stroke="#b9e0a6" stroke-width="3" opacity=".7"/>'
    if rim:
        g += f'<path d="M36 -40 q6 18 4 36" fill="none" stroke="{rim}" stroke-width="3" opacity=".8"/>'
    dx, dy = look
    g += f'<circle cx="-10" cy="-66" r="13" fill="#e3e5d6" stroke-width="3.2"/><circle cx="{-10 + dx}" cy="{-66 + dy}" r="5" fill="{INK}" stroke="none"/>'
    g += f'<circle cx="22" cy="-66" r="13" fill="#e3e5d6" stroke-width="3.2"/><circle cx="{22 + dx}" cy="{-66 + dy}" r="5" fill="{INK}" stroke="none"/>'
    g += f'<circle cx="{-8 + dx}" cy="{-68 + dy}" r="1.6" fill="#fff" stroke="none"/><circle cx="{24 + dx}" cy="{-68 + dy}" r="1.6" fill="#fff" stroke="none"/>'
    g += '<ellipse cx="-18" cy="-46" rx="5" ry="3" fill="#e98a8a" stroke="none" opacity=".55"/><ellipse cx="30" cy="-46" rx="5" ry="3" fill="#e98a8a" stroke="none" opacity=".55"/>'
    if mouth == 'o':
        g += '<ellipse cx="6" cy="-42" rx="6.5" ry="8" fill="#7a2f33" stroke-width="3"/><ellipse cx="6" cy="-38" rx="3.5" ry="2.6" fill="#e07b7b" stroke="none"/>'
    elif mouth == 'wide':
        g += '<path d="M-8 -45 q14 16 28 0 q-14 4 -28 0z" fill="#7a2f33" stroke-width="3"/>'
    for a in arms:
        g += f'<path d="{a}" fill="none" stroke-width="7.5"/><path d="{a}" fill="none" stroke="{GREEN}" stroke-width="3.4"/>'
    return g + front + '</g>'


def grass(x, y, h, lean, col, w=10):
    tip = (x + lean, y - h)
    c = (x + lean * 0.3, y - h * 0.6)
    return f'<path d="M{x - w / 2:.1f},{y} Q{c[0]:.1f},{c[1]:.1f} {tip[0]:.1f},{tip[1]:.1f} Q{c[0] + w * 0.3:.1f},{c[1]:.1f} {x + w / 2:.1f},{y}Z" fill="{col}"/>'


# =====================================================================================
# A  homage: The Matrix bullet-time dodge
# =====================================================================================
def make_A():
    D = FILTERS + LARVA_DEFS
    D += lin('skyA', [(0, '#020c07'), (.55, '#06200f'), (1, '#0c3a1c')])
    D += lin('mudA', [(0, '#0e2414'), (.35, '#08160c'), (1, '#030805')])
    D += rad('glA', 1150, 640, 620, [(0, '#d6ffe0', .55), (.35, '#5cf08a', .22), (1, '#0a3018', 0)])
    D += rad('eyeA', 1716, 318, 60, [(0, '#ffe9a0', 1), (.55, '#e6a72e', 1), (1, '#7a4a0c', 1)])
    D += lin('skinA', [(0, '#a3ad5a'), (.35, '#6f7d36'), (1, '#27301a')], x2=1, y2=0.3)
    D += lin('tng', [(0, '#ffb3bd'), (.5, '#e8708a'), (1, '#a83a58')], x2=0, y2=1)
    D += '<clipPath id="headA"><path d="M1588,438 C1598,380 1648,330 1690,300 C1760,250 1860,262 1920,272 L1920,840 C1830,820 1700,730 1642,630 C1618,580 1604,548 1608,522 Z"/></clipPath>'
    b = '<rect width="1920" height="1080" fill="url(#skyA)"/>'
    # digital rain (letterless dashes), dense at the top, fading down
    for col in range(0, 1920, 34):
        if random.random() < 0.25:
            continue
        y = random.randint(-200, 300)
        L = random.randint(4, 14)
        for k in range(L):
            yy = y + k * 30
            if yy > 760:
                break
            op = (k + 1) / L * (0.32 if col > 900 else 0.16) * (1 - yy / 900)
            if op <= 0.01:
                continue
            ln = random.choice([10, 14, 18])
            b += f'<rect x="{col + random.randint(0, 6)}" y="{yy}" width="5" height="{ln}" rx="2" fill="{"#c8ffd8" if k == L - 1 else "#3cff86"}" opacity="{op:.2f}"/>'
    # distant reeds along the pond edge
    for i in range(140):
        x = random.randint(-20, 1940)
        b += grass(x, 790, random.randint(60, 230), random.randint(-40, 40), random.choice(['#04130a', '#061a0d', '#082110']), w=random.randint(6, 12))
    b += '<rect x="0" y="770" width="1920" height="310" fill="url(#mudA)"/>'
    b += '<ellipse cx="1150" cy="640" rx="760" ry="520" fill="url(#glA)"/>'
    # wet mud shine + pebbles
    b += '<ellipse cx="1180" cy="905" rx="420" ry="34" fill="#9dffc0" opacity=".14" filter="url(#b14)"/>'
    for (px, py, r) in [(820, 930, 26), (900, 965, 14), (1560, 915, 22), (1500, 960, 12), (1010, 890, 10)]:
        b += f'<ellipse cx="{px}" cy="{py}" rx="{r * 1.5}" ry="{r}" fill="#0d2214" stroke="#020603" stroke-width="3"/><ellipse cx="{px - r * .3}" cy="{py - r * .45}" rx="{r * .7}" ry="{r * .25}" fill="#7dd99a" opacity=".35"/>'
    # ---- prey frog head (profile, mouth gaping), right edge
    b += '<g>'
    b += '<path d="M1588,438 C1598,380 1648,330 1690,300 C1760,250 1860,262 1920,272 L1920,520 L1790,500 Q1700,470 1588,438 Z" fill="url(#skinA)" stroke="#0b1006" stroke-width="7" stroke-linejoin="round"/>'
    b += '<path d="M1608,522 Q1700,516 1790,506 L1920,524 L1920,840 C1830,820 1700,730 1642,630 C1618,580 1604,548 1608,522 Z" fill="url(#skinA)" stroke="#0b1006" stroke-width="7" stroke-linejoin="round"/>'
    b += '<path d="M1588,438 Q1700,470 1790,500 Q1700,512 1608,522 Q1592,480 1588,438 Z" fill="#4a1220" stroke="#0b1006" stroke-width="6"/>'
    b += '<path d="M1600,450 Q1700,480 1780,500" fill="none" stroke="#c75a72" stroke-width="6" opacity=".6"/>'
    sp = ''
    for i in range(40):
        sx_, sy_ = random.randint(1620, 1920), random.randint(280, 830)
        sp += f'<ellipse cx="{sx_}" cy="{sy_}" rx="{random.randint(8, 22)}" ry="{random.randint(6, 14)}" fill="#1f2a10" opacity="{random.uniform(.3, .6):.2f}"/>'
    for i in range(50):
        sp += f'<circle cx="{random.randint(1620, 1920)}" cy="{random.randint(280, 830)}" r="{random.randint(2, 5)}" fill="#c4cf7a" opacity=".35"/>'
    b += f'<g clip-path="url(#headA)">{sp}<path d="M1920,560 C1830,600 1760,600 1700,640" fill="none" stroke="#d9e3a0" stroke-width="26" opacity=".25" filter="url(#b8)"/></g>'
    b += '<circle cx="1838" cy="420" r="38" fill="#3e4a20" stroke="#0b1006" stroke-width="4" opacity=".9"/>'  # eardrum
    b += '<circle cx="1622" cy="408" r="6" fill="#0b1006"/>'  # nostril
    # rim light from the green glow on the front contour
    b += '<path d="M1592,432 C1600,380 1648,332 1690,302" fill="none" stroke="#d6ffd0" stroke-width="7" opacity=".8" filter="url(#b2)"/>'
    b += '<path d="M1610,530 C1608,560 1622,590 1645,630 C1690,710 1760,780 1850,815" fill="none" stroke="#d6ffd0" stroke-width="6" opacity=".55" filter="url(#b2)"/>'
    # bulging eye
    b += '<circle cx="1716" cy="318" r="64" fill="#2b3416" stroke="#0b1006" stroke-width="7"/>'
    b += '<circle cx="1716" cy="318" r="52" fill="url(#eyeA)"/>'
    b += '<ellipse cx="1712" cy="320" rx="32" ry="13" fill="#090a04"/>'
    b += '<ellipse cx="1698" cy="300" rx="12" ry="7" fill="#fff" opacity=".9"/><circle cx="1736" cy="338" r="4" fill="#fff" opacity=".6"/>'
    b += '<path d="M1650,300 Q1716,232 1784,296" fill="none" stroke="#0b1006" stroke-width="9" stroke-linecap="round"/>'
    b += '</g>'
    # ---- tongue (bullet-time): from the mouth (1612,488) to a sticky tip just past the arched larva
    T0, T1, T2 = (1612, 488), (1300, 520), (960, 590)
    tp = [qb(T0, T1, T2, k / 40) for k in range(41)]
    b += f'<path d="{taper(tp, 50, 70)}" fill="#ff9fb4" opacity=".25" filter="url(#b14)"/>'
    # wake rings (the Matrix bullet ripples)
    for k, tt in enumerate([0.18, 0.34, 0.5, 0.64, 0.77, 0.88]):
        p = qb(T0, T1, T2, tt); q = qb(T0, T1, T2, tt + 0.01)
        ang = math.degrees(math.atan2(q[1] - p[1], q[0] - p[0]))
        for j, r in enumerate((1.0, 1.45, 1.9)):
            op = (0.55 - j * 0.15) * (0.4 + tt * 0.6)
            b += (f'<ellipse cx="{p[0]:.1f}" cy="{p[1]:.1f}" rx="{10 * r:.1f}" ry="{48 * r:.1f}" transform="rotate({ang:.1f} {p[0]:.1f} {p[1]:.1f})" '
                  f'fill="none" stroke="#dfffe8" stroke-width="{4 - j}" opacity="{op:.2f}"/>')
    for dy in (-60, -34, 38, 64):   # speed lines
        b += f'<path d="M{1520},{500 + dy * .6:.0f} Q1300,{530 + dy:.0f} 1080,{590 + dy * 1.1:.0f}" fill="none" stroke="#c8ffd8" stroke-width="3" opacity=".3" stroke-dasharray="80 40"/>'
    b += f'<path d="{taper(tp, 44, 30, cap=False)}" fill="url(#tng)" stroke="#3a0c18" stroke-width="5"/>'
    b += f'<path d="{poly(tp[2:38])}" fill="none" stroke="#ffd6de" stroke-width="7" stroke-linecap="round" opacity=".7" transform="translate(0 -9)"/>'
    b += '<path d="M972,565 C920,545 890,580 902,615 C912,647 960,655 990,633 C1012,617 1006,580 972,565 Z" fill="url(#tng)" stroke="#3a0c18" stroke-width="5"/>'
    b += '<ellipse cx="935" cy="587" rx="16" ry="9" fill="#fff" opacity=".7"/>'
    for (dx, dy) in [(-30, 70), (10, 80), (-55, 40)]:   # sticky droplets flying off
        b += f'<circle cx="{900 + dx}" cy="{540 + dy}" r="6" fill="#ffc2cf" opacity=".8"/>'
    # ---- larva: tail planted on the right, front arched back away from the tongue, legs flailing (bullet-dodge pose)
    b += '<ellipse cx="1260" cy="900" rx="280" ry="26" fill="#000" opacity=".5" filter="url(#b8)"/>'
    b += larva(((1560, 905), (1330, 915), (1250, 700), (1090, 735)), W=46, opn=0.5, head_rot=-38,
               ants=((-60, 4.2, -30), (-35, 4.6, -30)), legs='flail', vside=-1, light=(-0.2, -1), wave=True, rim='#e4ffd8')
    b += spark(1090, 640, 22, '#e8ffe8') + spark(1460, 760, 16, '#e8ffe8') + spark(880, 700, 14, '#e8ffe8') + spark(1350, 650, 12, '#e8ffe8')
    # ---- mascot: peeking over a pebble, sunglasses slipping down its nose
    glasses = ('<g stroke="#000" stroke-width="2.5"><rect x="-24" y="-60" width="26" height="13" rx="6" fill="#0a0f0c"/>'
               '<rect x="10" y="-60" width="26" height="13" rx="6" fill="#0a0f0c"/><path d="M2 -55 h8" fill="none" stroke-width="3"/>'
               '<path d="M-20 -57 l8 0" stroke="#9fffc0" stroke-width="2" opacity=".8"/><path d="M14 -57 l8 0" stroke="#9fffc0" stroke-width="2" opacity=".8"/></g>')
    b += frog(330, 1000, 3.3, mouth='o', look=(4, -1), arms=('M-34 -22 q-10 -6 -10 -20', 'M38 -22 q14 -6 18 -20'), front=glasses, rim='#b8ffc8')
    b += '<path d="M150,1080 C160,990 240,960 330,962 C430,962 500,995 520,1080 Z" fill="#0c2213" stroke="#020603" stroke-width="6"/>'
    b += '<path d="M200,1000 C240,975 300,972 350,976" fill="none" stroke="#8fe8a8" stroke-width="6" opacity=".4" stroke-linecap="round"/>'
    for i in range(14):
        b += grass(random.randint(120, 560), 1085, random.randint(60, 120), random.randint(-30, 30), '#04100a', w=9)
    lines = [('IT', 118, 'w'), ('DODGES', 214, 'y'), ('THE TONGUE', 128, 'w')]
    return page('#020c07', svg(D, b), lines)


# =====================================================================================
# B  intuitive: flashlight finds a "worm"; the shadow tells the truth
# =====================================================================================
def make_B():
    D = FILTERS + LARVA_DEFS
    D += lin('rockB', [(0, '#1b2b33'), (.6, '#13202a'), (1, '#0b141a')])
    D += lin('mudB', [(0, '#2a2117'), (.4, '#17120c'), (1, '#080604')])
    D += rad('spotB', 1480, 430, 560, [(0, '#ffe3a0', .75), (.55, '#f2b860', .42), (.85, '#c27a30', .12), (1, '#000', 0)])
    D += lin('beamB', [(0, '#fff2c4'), (1, '#ffcf70')], x2=1, y2=-0.4)
    D += rad('lampB', 790, 872, 150, [(0, '#fffbe8', 1), (.3, '#ffe9a8', .7), (1, '#ffcf70', 0)])
    b = '<rect width="1920" height="1080" fill="url(#rockB)"/>'
    # rock wall texture: big slabs and cracks
    for i in range(26):
        x, y = random.randint(-100, 1900), random.randint(-60, 700)
        b += f'<ellipse cx="{x}" cy="{y}" rx="{random.randint(120, 300)}" ry="{random.randint(60, 140)}" fill="{random.choice(["#22343e", "#0f1a21", "#1a2a31"])}" opacity=".55" filter="url(#b14)"/>'
    for i in range(9):
        x = random.randint(950, 1900); y = random.randint(60, 600)
        b += f'<path d="M{x},{y} l{random.randint(-60, 60)},{random.randint(40, 90)} l{random.randint(-50, 50)},{random.randint(40, 100)}" fill="none" stroke="#070d11" stroke-width="5" opacity=".7"/>'
    # moss on top of the wall
    b += '<path d="M0,0 L1920,0 L1920,70 C1700,120 1500,60 1300,110 C1100,150 900,80 700,120 C500,160 300,90 0,130 Z" fill="#14281c" opacity=".9"/>'
    # spotlight on the rock and the beam cone
    b += '<ellipse cx="1480" cy="430" rx="560" ry="420" fill="url(#spotB)"/>'
    b += '<path d="M790,872 L1080,120 L1920,170 L1920,760 Z" fill="url(#beamB)" opacity=".13"/>'
    b += '<path d="M790,872 L1180,250 L1920,330 L1920,640 Z" fill="#fff2c4" opacity=".08"/>'
    # the GIANT SHADOW on the rock: hooked jaws open, antennae high
    b += '<g opacity=".93" filter="url(#b4)">' + larva(((1930, 700), (1720, 720), (1520, 650), (1370, 500)), W=80, opn=0.7, head_rot=-4,
                                                         ants=((-34, 5.0, -50), (22, 5.2, 50)), legs='walk', vside=-1, sil='#0a0806') + '</g>'
    # ground
    b += '<path d="M0,800 C400,780 900,790 1300,770 C1600,760 1800,780 1920,775 L1920,1080 L0,1080 Z" fill="url(#mudB)"/>'
    b += '<path d="M0,800 C400,780 900,790 1300,770 C1600,760 1800,780 1920,775" fill="none" stroke="#3b2f22" stroke-width="5"/>'
    b += '<ellipse cx="1140" cy="890" rx="520" ry="70" fill="#ffd88a" opacity=".22" filter="url(#b24)"/>'
    # puddle reflecting the beam
    b += '<ellipse cx="1500" cy="960" rx="190" ry="28" fill="#0c1820"/><ellipse cx="1470" cy="955" rx="120" ry="10" fill="#ffe2a0" opacity=".35" filter="url(#b4)"/>'
    for (px, py, r) in [(1000, 930, 18), (1620, 880, 14), (930, 860, 10), (1720, 925, 9)]:
        b += f'<ellipse cx="{px}" cy="{py}" rx="{r * 1.5}" ry="{r}" fill="#2a2016" stroke="#0a0705" stroke-width="3"/><ellipse cx="{px - r * .3}" cy="{py - r * .4}" rx="{r * .6}" ry="{r * .22}" fill="#ffd88a" opacity=".45"/>'
    # left reeds framing
    for i in range(30):
        b += grass(random.randint(-20, 300), 1085, random.randint(200, 520), random.randint(-60, 80), random.choice(['#0a130f', '#0d1912', '#08100c']), w=14)
    # the real larva on the mud, lit by the beam, antennae waving like a worm
    b += '<ellipse cx="1300" cy="880" rx="240" ry="20" fill="#000" opacity=".55" filter="url(#b8)"/>'
    b += larva(((1500, 872), (1400, 884), (1250, 880), (1170, 820)), W=32, opn=0.3, head_rot=-10,
               ants=((-34, 4.6, -50), (20, 4.8, 45)), legs='walk', vside=-1, light=(-1, -0.3), wave=True, rim='#fff4cc')
    b += spark(1060, 720, 20) + spark(1260, 700, 14) + spark(960, 820, 12)
    # mascot holding the flashlight, leaning in, curious
    torch = ('<g transform="rotate(-24 72 -38)"><rect x="56" y="-47" width="40" height="18" rx="5" fill="#d6b04a" stroke-width="3"/>'
             '<rect x="92" y="-51" width="10" height="26" rx="3" fill="#8f7a3a" stroke-width="3"/><rect x="62" y="-44" width="24" height="4" rx="2" fill="#fff3c4" stroke="none" opacity=".8"/></g>')
    b += f'<circle cx="790" cy="872" r="150" fill="url(#lampB)"/>'
    b += frog(500, 1010, 3.1, mouth='o', look=(5, -1), arms=('M-34 -22 q-14 6 -16 22', 'M38 -22 q20 -2 30 -14'), front=torch, rim='#ffe9a8')
    b += '<circle cx="790" cy="872" r="22" fill="#fffbe8" opacity=".95" filter="url(#b4)"/>'
    lines = [('WORM', 206, 'w'), ('OR', 112, 'w'), ('TRAP?', 246, 'y')]
    return page('#0b141a', svg(D, b), lines)


# =====================================================================================
# C  homage: The Silence of the Lambs poster (pale face, insect over the mouth)
# =====================================================================================
def larva_top(x, y0, y1, W):
    """dorsal view, head at the top (y0), tail at y1: symmetric like the moth on the poster"""
    o = []
    N = len(PROF); seg = (y1 - y0) / N
    cen = [(x, y1 - seg * (i + 0.5)) for i in range(N)]          # i=0 tail (bottom)
    # legs, splayed sideways like wings (3 pairs on the thorax)
    for k, (a1, a2) in enumerate([(-58, -95), (-95, -120), (-130, -150)]):   # degrees from straight up
        cx_, cy_ = cen[N - 1 - k]
        for sg in (-1, 1):
            base = (cx_ + sg * W * PROF[N - 1 - k] * 0.8, cy_)
            d1 = (sg * math.sin(math.radians(-a1)), -math.cos(math.radians(-a1)))
            d2 = (sg * math.sin(math.radians(-a2)), -math.cos(math.radians(-a2)))
            knee = add(base, d1, W * 1.5); foot = add(knee, d2, W * 1.6); claw = add(foot, d2, W * 0.3)
            dd = poly([base, knee, foot, claw])
            o.append(f'<path d="{dd}" fill="none" stroke="#24120a" stroke-width="{W * 0.27:.1f}" stroke-linecap="round" stroke-linejoin="round"/>'
                     f'<path d="{dd}" fill="none" stroke="#b07a3c" stroke-width="{W * 0.15:.1f}" stroke-linecap="round" stroke-linejoin="round"/>')
    for sg in (-1, 1):   # urogomphi
        a = (x + sg * W * 0.2, y1 - seg * 0.2); bb = (x + sg * W * 0.7, y1 + W * 1.2)
        o.append(f'<path d="{taper([a, ((a[0] + bb[0]) / 2, (a[1] + bb[1]) / 2 + 4), bb], W * 0.22, 2, cap=False)}" fill="#24120a"/>')
    for i, (cx_, cy_) in enumerate(cen):
        w = W * PROF[i]
        o.append(f'<ellipse cx="{cx_:.1f}" cy="{cy_:.1f}" rx="{w:.1f}" ry="{seg * 0.74:.1f}" fill="url(#lvb)" stroke="#24120a" stroke-width="{W * 0.07:.1f}"/>')
        o.append(f'<ellipse cx="{cx_:.1f}" cy="{cy_ - seg * 0.06:.1f}" rx="{w * 0.62:.1f}" ry="{seg * 0.5:.1f}" fill="#8a4f1e" opacity=".42"/>')
        o.append(f'<path d="M{cx_ - w * 0.75:.1f},{cy_ + seg * 0.1:.1f} Q{cx_ - w * 0.8:.1f},{cy_ - seg * 0.5:.1f} {cx_ - w * 0.3:.1f},{cy_ - seg * 0.6:.1f}" fill="none" stroke="#fff6d8" stroke-width="{W * 0.1:.1f}" stroke-linecap="round" opacity=".8"/>')
    o.append(f'<path d="M{x:.1f},{y1 - seg * 0.4:.1f} L{x:.1f},{y0 + seg * 0.4:.1f}" stroke="#5a3010" stroke-width="{W * 0.05:.1f}" opacity=".6"/>')
    # head + mandibles + antennae
    H = (x, y0 - W * 0.7)
    Lm = W * 2.3
    for sg in (-1, 1):
        B = (x + sg * W * 0.45, H[1] - W * 0.65)
        mp = [cb(B, (B[0] + sg * Lm * 0.55, B[1] - Lm * 0.4), (B[0] + sg * Lm * 0.35, B[1] - Lm * 1.0), (B[0] - sg * Lm * 0.05, B[1] - Lm * 0.95), k / 20) for k in range(21)]
        o.append(f'<path d="{taper(mp, W * 0.46, W * 0.06)}" fill="#3b1a0b" stroke="#24120a" stroke-width="{W * 0.05:.1f}"/>')
        o.append(f'<path d="{poly(mp[3:14])}" fill="none" stroke="#c9874a" stroke-width="{W * 0.07:.1f}" stroke-linecap="round" opacity=".8" transform="translate({-sg * 3} 2)"/>')
        A0 = (x + sg * W * 0.7, H[1] - W * 0.4)
        A1 = (A0[0] + sg * W * 2.6, A0[1] - W * 1.6); A2 = (A1[0] + sg * W * 1.4, A1[1] - W * 2.4)
        ap = [qb(A0, A1, A2, j / 24) for j in range(25)]
        o.append(f'<path d="{taper(ap, W * 0.2, W * 0.08)}" fill="#6b3b16" stroke="#24120a" stroke-width="{W * 0.04:.1f}"/>')
        for j in range(3, 25, 3):
            p = ap[j]
            o.append(f'<circle cx="{p[0]:.1f}" cy="{p[1]:.1f}" r="{W * (0.12 - j * 0.002):.1f}" fill="#c98a45" stroke="#24120a" stroke-width="{W * 0.03:.1f}"/>')
    o.append(f'<ellipse cx="{H[0]:.1f}" cy="{H[1]:.1f}" rx="{W * 0.92:.1f}" ry="{W * 1.0:.1f}" fill="url(#lvh)" stroke="#24120a" stroke-width="{W * 0.07:.1f}"/>')
    for sg in (-1, 1):
        for k in range(3):
            o.append(f'<circle cx="{x + sg * W * (0.55 + k * 0.08):.1f}" cy="{H[1] - W * (0.35 - k * 0.15):.1f}" r="{W * 0.08:.1f}" fill="#120804"/>')
    o.append(f'<ellipse cx="{x - W * 0.25:.1f}" cy="{H[1] - W * 0.4:.1f}" rx="{W * 0.3:.1f}" ry="{W * 0.18:.1f}" fill="#ffe2a6" opacity=".6"/>')
    return ''.join(o)


def make_C():
    cx = 1340
    D = FILTERS + LARVA_DEFS
    D += rad('bgC', 1300, 480, 1300, [(0, '#efe9dc', 1), (.6, '#d8cfbd', 1), (1, '#a99f8c', 1)])
    D += '<linearGradient id="skinC" x1="0" y1="0" x2="1" y2="0.2"><stop offset="0" stop-color="#f4f2e2"/><stop offset=".5" stop-color="#d9dcc0"/><stop offset="1" stop-color="#8e957a"/></linearGradient>'
    D += lin('bodyC', [(0, '#bfc3a6'), (.55, '#d4ccb9'), (1, '#d8cfbd')])
    for k, ex in enumerate((cx - 230, cx + 230)):
        D += rad(f'irC{k}', ex - 12, 240, 100, [(0, '#f6c25a', 1), (.45, '#d2702a', 1), (.85, '#7a2410', 1), (1, '#3a0e06', 1)])
    head = (f'M{cx - 400},560 C{cx - 415},420 {cx - 330},300 {cx - 190},290 Q{cx},265 {cx + 190},290 C{cx + 330},300 {cx + 415},420 {cx + 400},560 '
            f'C{cx + 390},720 {cx + 250},830 {cx},845 C{cx - 250},830 {cx - 390},720 {cx - 400},560 Z')
    D += f'<clipPath id="headC"><path d="{head}"/></clipPath>'
    b = '<rect width="1920" height="1080" fill="url(#bgC)"/>'
    b += f'<ellipse cx="{cx}" cy="460" rx="640" ry="470" fill="#fffaf0" opacity=".75" filter="url(#b60)"/>'
    # throat / shoulders fading into the paper
    b += f'<path d="M{cx - 300},700 C{cx - 360},880 {cx - 380},980 {cx - 400},1080 L{cx + 260},1080 C{cx + 280},980 {cx + 300},880 {cx + 260},700 Z" fill="url(#bodyC)" opacity=".85"/>'
    b += f'<ellipse cx="{cx}" cy="1080" rx="560" ry="170" fill="#d8cfbd" filter="url(#b40)"/>'
    b += f'<path d="{head}" fill="url(#skinC)" stroke="#2b2a20" stroke-width="6"/>'
    sp = ''
    for i in range(70):
        sp += f'<ellipse cx="{random.randint(cx - 400, cx + 400)}" cy="{random.randint(290, 845)}" rx="{random.randint(6, 20)}" ry="{random.randint(5, 13)}" fill="#8f9878" opacity="{random.uniform(.12, .3):.2f}"/>'
    sp += f'<ellipse cx="{cx + 330}" cy="620" rx="210" ry="320" fill="#5f6650" opacity=".4" filter="url(#b40)"/>'
    sp += f'<ellipse cx="{cx - 170}" cy="470" rx="170" ry="80" fill="#ffffff" opacity=".5" filter="url(#b24)"/>'
    sp += f'<path d="M{cx - 340},770 Q{cx},905 {cx + 340},770" fill="none" stroke="#7d8268" stroke-width="40" opacity=".35" filter="url(#b14)"/>'
    b += f'<g clip-path="url(#headC)">{sp}</g>'
    b += f'<ellipse cx="{cx - 50}" cy="455" rx="10" ry="6" fill="#3d3b2c"/><ellipse cx="{cx + 50}" cy="455" rx="10" ry="6" fill="#3d3b2c"/>'
    b += f'<path d="M{cx - 370},610 C{cx - 230},690 {cx - 100},712 {cx},714 C{cx + 100},712 {cx + 230},690 {cx + 370},610" fill="none" stroke="#2b2a20" stroke-width="9" stroke-linecap="round"/>'
    # staring eyes (no lids over the iris)
    for k, ex in enumerate((cx - 230, cx + 230)):
        b += f'<ellipse cx="{ex}" cy="262" rx="150" ry="132" fill="#c8cbb0" stroke="#2b2a20" stroke-width="6"/>'
        b += f'<ellipse cx="{ex + 30}" cy="300" rx="110" ry="80" fill="#6f7560" opacity=".25" filter="url(#b14)"/>'
        b += f'<circle cx="{ex}" cy="246" r="106" fill="url(#irC{k})" stroke="#1b1a14" stroke-width="5"/>'
        for j in range(16):
            a = j / 16 * 2 * math.pi
            b += f'<path d="M{ex + math.cos(a) * 44:.1f},{246 + math.sin(a) * 30:.1f} L{ex + math.cos(a) * 94:.1f},{246 + math.sin(a) * 90:.1f}" stroke="#ffd98a" stroke-width="3" opacity=".25"/>'
        b += f'<ellipse cx="{ex}" cy="248" rx="64" ry="25" fill="#0a0806"/>'
        b += f'<ellipse cx="{ex - 38}" cy="206" rx="24" ry="14" fill="#fff" opacity=".92"/><circle cx="{ex + 44}" cy="286" r="7" fill="#fff" opacity=".55"/>'
        b += f'<path d="M{ex - 140},215 Q{ex},90 {ex + 140},215" fill="none" stroke="#2b2a20" stroke-width="7" stroke-linecap="round" opacity=".6"/>'
    # the larva over the mouth, seen from above, legs spread like the poster's moth wings
    b += f'<ellipse cx="{cx + 14}" cy="720" rx="240" ry="150" fill="#3d3b2c" opacity=".3" filter="url(#b14)"/>'
    b += larva_top(cx, 610, 900, 60)
    b += spark(cx - 500, 560, 20, '#ffffff') + spark(cx + 470, 120, 16, '#ffffff')
    # mascot: bottom-left, both hands (round frog pads) over its own mouth in shock
    pads = '<circle cx="-2" cy="-42" r="8" fill="#6aa55a" stroke-width="3"/><circle cx="14" cy="-42" r="8" fill="#6aa55a" stroke-width="3"/>'
    b += f'<ellipse cx="350" cy="1035" rx="130" ry="18" fill="#6c6452" opacity=".35" filter="url(#b8)"/>'
    b += frog(350, 1030, 3.0, mouth='none', look=(6, -2), arms=('M-34 -22 q-6 -18 26 -20', 'M38 -22 q6 -18 -18 -20'), front=pads)
    lines = [('BUG WINS', 158, 'w'), ('NEARLY', 104, 'w'), ('100%', 270, 'y')]
    return page('#d8cfbd', svg(D, b), lines, outline='#1b1712')


for name, fn in (('A', make_A), ('B', make_B), ('C', make_C)):
    open(os.path.join(HERE, f'{name}.html'), 'w').write(fn())
    print('wrote', name)
