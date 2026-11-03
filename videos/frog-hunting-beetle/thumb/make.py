# Thumbnails A-C for frog-hunting-beetle, v2 (owner 2026-11-03: "express it INTUITIVELY, with the feeling of a bug eating a frog"; v1 kept in ./v1).
# Guideline 16-6/16-8, brief tools/briefs/thumb_art.md. Run: python3 videos/frog-hunting-beetle/thumb/make.py
# A  IT BIT / BACK        larva clamped on a wild toad's lower lip, the toad thrashes (tiny pupils, sweat, tongue out)   (hypothesis "dodge a tongue and bite back", S26-S28)
# B  WHO EATS / WHOM?     adult beetle riding a bucking frog's back, jaws in its back                                    (adult "jump onto the back of an amphibian", S10 role reversal)
# C  FROG + BUG / = BONES frog skeleton on the mud, a fat larva asleep on it, the mascot's flashlight finds it            (S42 "all that remains ... is a pile of bones")
# Mascot (separate cute character, bystander): A shocked with notebook, B hands up, C flashlight. No blood or wounds.
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




def sweat(x, y, s=1.0, rot=0):
    return (f'<g transform="translate({x} {y}) rotate({rot}) scale({s})"><path d="M0,-30 C10,-12 18,0 18,10 C18,22 9,30 0,30 C-9,30 -18,22 -18,10 C-18,0 -10,-12 0,-30Z" '
            f'fill="#bfe9ff" stroke="#0b1a24" stroke-width="4"/><ellipse cx="-6" cy="8" rx="4" ry="7" fill="#fff" opacity=".9"/></g>')


def shake(x, y, s=1.0, flip=False, col='#fff3d0', op=.8):
    k = -1 if flip else 1
    return ''.join(f'<path d="M{x + k * i * 26 * s:.0f},{y - 60 * s + i * 8:.0f} Q{x + k * (i * 26 + 22) * s:.0f},{y:.0f} {x + k * i * 26 * s:.0f},{y + 60 * s - i * 8:.0f}" '
                   f'fill="none" stroke="{col}" stroke-width="{9 - i * 2}" stroke-linecap="round" opacity="{op - i * .2:.2f}"/>' for i in range(3))


def fingers(x, y, ang, L, col, ink, n=4, spread=70, w=16):
    o = ''
    for k in range(n):
        a = math.radians(ang - spread / 2 + spread * k / (n - 1))
        tx, ty = x + math.cos(a) * L, y + math.sin(a) * L
        o += f'<path d="M{x:.0f},{y:.0f} L{tx:.0f},{ty:.0f}" stroke="{ink}" stroke-width="{w + 7}" stroke-linecap="round"/>'
        o += f'<path d="M{x:.0f},{y:.0f} L{tx:.0f},{ty:.0f}" stroke="{col}" stroke-width="{w}" stroke-linecap="round"/>'
        o += f'<circle cx="{tx:.0f}" cy="{ty:.0f}" r="{w * .75:.0f}" fill="{col}" stroke="{ink}" stroke-width="4"/>'
    return o


def limb(pts, w0, w1, fill, ink, sw=7):
    return f'<path d="{taper(pts, w0, w1)}" fill="{fill}" stroke="{ink}" stroke-width="{sw}" stroke-linejoin="round"/>'


def notebook_front():
    return ('<g transform="rotate(-6)" stroke="#1d2b1c" stroke-width="2.6"><path d="M-24 -40 L2 -36 L2 -6 L-24 -10Z" fill="#f6efd8"/>'
            '<path d="M2 -36 L30 -40 L30 -10 L2 -6Z" fill="#fffaf0"/><path d="M-19 -30 l16 2 M-19 -23 l16 2 M-19 -16 l12 2 M7 -31 l18 -2 M7 -24 l18 -2" stroke="#7b8bb0" stroke-width="1.6"/>'
            '<path d="M34 -52 l-12 22" stroke="#1d2b1c" stroke-width="5"/><path d="M34 -52 l-12 22" stroke="#f2c14e" stroke-width="2.6"/></g>')


# =====================================================================================
# A  intuitive: larva clamped on a toad's lip, the toad thrashing
# =====================================================================================
def make_A():
    random.seed(21)
    TINK = '#1a1208'
    D = FILTERS + LARVA_DEFS
    D += lin('skyA', [(0, '#03141a'), (.6, '#0a2a2c'), (1, '#0f3a33')])
    D += lin('bankA', [(0, '#1b2416'), (.4, '#10170d'), (1, '#050804')])
    D += rad('moonA', 1420, 330, 700, [(0, '#fff3cf', .95), (.18, '#ffe2a0', .55), (.5, '#7fbfa0', .16), (1, '#0a2a2c', 0)])
    D += rad('toadA', -60, -200, 640, [(0, '#c9a865', 1), (.45, '#8d6c38', 1), (.8, '#5a4222', 1), (1, '#33250f', 1)])
    D += rad('bellyA', 0, 120, 300, [(0, '#f7ecc8', 1), (.7, '#dcc48e', 1), (1, '#a88d58', 1)])
    D += rad('irisA', -14, -14, 70, [(0, '#fff2a8', 1), (.5, '#e9b23a', 1), (1, '#8a5a12', 1)])
    D += lin('tngA', [(0, '#ffb9c4'), (1, '#d8607a')])
    b = '<rect width="1920" height="1080" fill="url(#skyA)"/>'
    b += '<rect width="1920" height="1080" fill="url(#moonA)"/>'
    b += '<circle cx="1420" cy="300" r="150" fill="#fff6dc" opacity=".95" filter="url(#b8)"/>'
    for _ in range(40):
        b += f'<circle cx="{random.randint(900, 1900)}" cy="{random.randint(20, 520)}" r="{random.choice([1.5, 2.2, 3])}" fill="#fffbe8" opacity="{random.uniform(.2, .7):.2f}"/>'
    # far reeds
    for _ in range(110):
        b += grass(random.randint(-20, 1940), 840, random.randint(80, 300), random.randint(-50, 50), random.choice(['#06201d', '#082622', '#0a2c26']), w=random.randint(6, 13))
    b += '<path d="M0,820 C400,800 900,830 1920,810 L1920,1080 L0,1080Z" fill="url(#bankA)"/>'
    b += '<ellipse cx="1300" cy="905" rx="520" ry="40" fill="#000" opacity=".55" filter="url(#b14)"/>'
    # ---------- toad (front view, tilted by the thrash) ----------
    T = '<g transform="translate(1330 560) rotate(-7)">'
    # hind legs
    for sg in (-1, 1):
        T += f'<ellipse cx="{sg * 300}" cy="250" rx="140" ry="72" fill="#5f4724" stroke="{TINK}" stroke-width="8"/>'
        T += fingers(sg * 380, 300, 90 - sg * 30, 70, '#6b5229', TINK, n=4, spread=60, w=14)
    body = 'M-360,150 C-390,-70 -250,-262 0,-268 C250,-262 390,-70 360,150 C330,282 -330,282 -360,150Z'
    T += f'<path d="{body}" fill="url(#toadA)" stroke="{TINK}" stroke-width="9"/>'
    T += '<clipPath id="tbA"><path d="' + body + '"/></clipPath><g clip-path="url(#tbA)">'
    T += '<ellipse cx="0" cy="170" rx="250" ry="120" fill="url(#bellyA)"/>'
    for _ in range(85):  # warts
        x, y = random.randint(-360, 360), random.randint(-260, 120)
        if abs(x) < 240 and y > 30:
            continue
        r = random.randint(7, 17)
        T += f'<circle cx="{x}" cy="{y}" r="{r}" fill="#4a3519" opacity=".75"/><circle cx="{x - r * .3:.0f}" cy="{y - r * .35:.0f}" r="{r * .35:.0f}" fill="#e6c98a" opacity=".55"/>'
    T += '<path d="M150,-250 C300,-200 370,-60 360,120" fill="none" stroke="#fff0c0" stroke-width="22" opacity=".55" filter="url(#b8)"/>'
    T += '</g>'
    T += f'<path d="M150,-252 C300,-205 372,-60 362,120" fill="none" stroke="#fff4d2" stroke-width="6" opacity=".9" filter="url(#b2)"/>'
    # parotoid glands
    for sg in (-1, 1):
        T += f'<ellipse cx="{sg * 285}" cy="-120" rx="48" ry="95" transform="rotate({sg * -28} {sg * 285} -120)" fill="#7a5a2c" stroke="{TINK}" stroke-width="6" opacity=".95"/>'
        T += f'<ellipse cx="{sg * 275}" cy="-150" rx="16" ry="40" transform="rotate({sg * -28} {sg * 275} -150)" fill="#d6b678" opacity=".45"/>'
    # mouth: wavy worried line, slightly open, tongue lolling out of the left corner
    T += f'<path d="M-310,60 Q-160,10 0,36 Q160,10 310,60 Q160,58 0,78 Q-160,58 -310,60Z" fill="#3a0d14" stroke="{TINK}" stroke-width="8" stroke-linejoin="round"/>'
    T += f'<path d="M-250,52 C-275,90 -300,160 -268,200 C-240,232 -200,205 -205,160 C-208,120 -210,85 -195,50Z" fill="url(#tngA)" stroke="{TINK}" stroke-width="7"/>'
    T += '<path d="M-240,70 C-255,110 -262,150 -248,182" fill="none" stroke="#a83a58" stroke-width="5" stroke-linecap="round"/>'
    T += '<ellipse cx="-262" cy="168" rx="10" ry="16" fill="#fff" opacity=".6"/>'
    # nostrils
    T += f'<ellipse cx="-50" cy="-90" rx="12" ry="8" fill="{TINK}"/><ellipse cx="50" cy="-90" rx="12" ry="8" fill="{TINK}"/>'
    # eyes: bulging, tiny panicked pupils, worried brows
    for sg in (-1, 1):
        ex, ey = sg * 165, -222
        T += f'<circle cx="{ex}" cy="{ey + 6}" r="98" fill="#6b5028" stroke="{TINK}" stroke-width="9"/>'
        T += f'<circle cx="{ex}" cy="{ey}" r="80" fill="#fffdf2" stroke="{TINK}" stroke-width="6"/>'
        T += f'<g transform="translate({ex + sg * 4} {ey + 10})"><circle r="52" fill="url(#irisA)" stroke="#5a3a0a" stroke-width="4"/>'
        T += '<ellipse rx="17" ry="11" fill="#0a0703"/><ellipse cx="-20" cy="-22" rx="13" ry="9" fill="#fff" opacity=".95"/><circle cx="18" cy="20" r="5" fill="#fff" opacity=".7"/></g>'
        T += f'<path d="M{ex - sg * 95},{ey - 50} Q{ex - sg * 30},{ey - 135} {ex + sg * 70},{ey - 95}" fill="none" stroke="{TINK}" stroke-width="16" stroke-linecap="round"/>'
        T += f'<path d="M{ex - sg * 92},{ey - 56} Q{ex - sg * 30},{ey - 128} {ex + sg * 66},{ey - 100}" fill="none" stroke="#9a7840" stroke-width="6" stroke-linecap="round"/>'
    # arms: left flails up and out, right claws at the larva
    T += limb([(-315, 120), (-420, 110), (-470, 40)], 70, 46, '#7a5c2e', TINK)
    T += fingers(-474, 30, -150, 62, '#8d6c38', TINK, n=4, spread=80)
    T += limb([(300, 150), (250, 230), (150, 250)], 70, 46, '#7a5c2e', TINK)
    T += fingers(140, 252, 180, 56, '#8d6c38', TINK, n=4, spread=70)
    # the larva hanging from the lower lip, jaws clamped
    T += '<path d="M30,170 C-10,270 150,330 210,430" stroke="#3a2410" stroke-width="120" stroke-linecap="round" fill="none" opacity=".35" filter="url(#b14)"/>'
    T += larva(((240, 400), (170, 330), (-20, 290), (30, 185)), W=48, opn=-0.06, head_rot=-6,
               ants=((-70, 3.6, -40), (70, 3.6, 40)), legs='flail', vside=1, light=(1, -0.6), rim='#fff1c4')
    T += f'<path d="M-30,62 Q10,90 60,64" fill="none" stroke="{TINK}" stroke-width="6" stroke-linecap="round"/>'
    for a in (-150, -110, -70, -30):  # pinch lines
        r0, r1 = 60, 95
        T += f'<path d="M{15 + math.cos(math.radians(a)) * r0:.0f},{70 + math.sin(math.radians(a)) * r0 * .5:.0f} L{15 + math.cos(math.radians(a)) * r1:.0f},{70 + math.sin(math.radians(a)) * r1 * .5:.0f}" stroke="#fff4c8" stroke-width="7" stroke-linecap="round"/>'
    T += '</g>'
    b += T
    # thrash lines + sweat drops
    b += shake(960, 300, 1.0, flip=True) + shake(1800, 300, 1.3)
    b += sweat(940, 170, 1.4, -30) + sweat(880, 470, 1.1, -45) + sweat(1760, 160, 1.5, 30) + sweat(1830, 420, 1.1, 40)
    b += spark(1530, 700, 20) + spark(1110, 760, 14) + spark(1650, 560, 16)
    # mascot with notebook, shocked
    b += '<ellipse cx="320" cy="1012" rx="150" ry="22" fill="#000" opacity=".5" filter="url(#b4)"/>'
    b += frog(320, 1010, 3.0, mouth='o', look=(5, -2), arms=('M-34 -22 q-4 14 12 -10', 'M38 -22 q8 14 -10 -12'), front=notebook_front(), rim='#ffe9b0')
    b += '<path d="M470,700 l-8,70" stroke="#fff3d0" stroke-width="14" stroke-linecap="round"/><circle cx="458" cy="800" r="9" fill="#fff3d0"/>'
    for _ in range(16):
        b += grass(random.randint(80, 620), 1090, random.randint(60, 130), random.randint(-30, 30), '#040a06', w=9)
    return page('#03141a', svg(D, b), [('IT BIT', 200, 'w'), ('BACK', 300, 'y')], outline='#04100e')


# =====================================================================================
# B  intuitive: adult beetle riding a frog's back, biting
# =====================================================================================
def beetle(x, y, ang, s):
    INKB = '#120a04'; LEG = '#d39a35'
    o = f'<g transform="translate({x} {y}) rotate({ang}) scale({s})">'
    legs = [(70, [(30, 95), (-20, 160)]), (35, [(10, 105), (-70, 150)]), (0, [(-60, 95), (-150, 140)])]
    for sg, dx, LEG in ((-1, -26, '#8a5f1c'), (-1, 0, '#d39a35')):   # both leg rows grip the frog's back (far row darker)
        for cx_, ((kx, ky), (fx, fy)) in legs:
            cx_ += dx
            pts = [(cx_, 0), (cx_ + kx * .5, sg * ky * .5), (cx_ + kx, sg * ky), (cx_ + kx + (fx - kx) * .5, sg * (ky + (fy - ky) * .5)), (cx_ + fx, sg * fy)]
            o += f'<path d="{poly(pts)}" fill="none" stroke="{INKB}" stroke-width="20" stroke-linecap="round" stroke-linejoin="round"/>'
            o += f'<path d="{poly(pts)}" fill="none" stroke="{LEG}" stroke-width="10" stroke-linecap="round" stroke-linejoin="round"/>'
            o += f'<path d="M{cx_ + fx},{sg * fy} l-14,{sg * 10} M{cx_ + fx},{sg * fy} l-4,{sg * 16}" stroke="{INKB}" stroke-width="6" stroke-linecap="round"/>'
    # antennae
    for sg in (-1, 1):
        ap = [qb((150, sg * 20), (200, sg * 150), (60, sg * 170 - 40), k / 20) for k in range(21)]
        o += f'<path d="{poly(ap)}" fill="none" stroke="{INKB}" stroke-width="13" stroke-linecap="round"/><path d="{poly(ap)}" fill="none" stroke="#e9b44a" stroke-width="6" stroke-linecap="round"/>'
        for k in range(2, 21, 3):
            o += f'<circle cx="{ap[k][0]:.0f}" cy="{ap[k][1]:.0f}" r="5" fill="#f3c560" stroke="{INKB}" stroke-width="2"/>'
    # mandibles (sickles biting down)
    for sg in (-1, 1):
        mp = [cb((150, sg * 22), (200, sg * 45), (235, sg * 25), (232, -sg * 6), k / 16) for k in range(17)]
        o += f'<path d="{taper(mp, 26, 4)}" fill="#3a1d08" stroke="{INKB}" stroke-width="4"/>'
        o += f'<path d="{poly(mp[2:12])}" fill="none" stroke="#d08a3a" stroke-width="3" opacity=".8"/>'
    # elytra
    el = 'M40,0 C42,-88 -70,-92 -160,-24 Q-176,0 -160,24 C-70,92 42,88 40,0Z'
    o += f'<path d="{el}" fill="#e8b03a" stroke="{INKB}" stroke-width="7"/>'
    o += '<path d="M30,0 C32,-74 -66,-78 -146,-20 Q-160,0 -146,20 C-66,78 32,74 30,0Z" fill="url(#elyB)"/>'
    for k in range(1, 4):
        o += f'<path d="M30,{-k * 17} C0,{-k * 19} -80,{-k * 16} -140,{-k * 5}" fill="none" stroke="#3d6b7a" stroke-width="2.5" opacity=".6"/>'
        o += f'<path d="M30,{k * 17} C0,{k * 19} -80,{k * 16} -140,{k * 5}" fill="none" stroke="#3d6b7a" stroke-width="2.5" opacity=".6"/>'
    o += f'<path d="M38,0 L-160,0" stroke="{INKB}" stroke-width="4"/>'
    o += '<path d="M10,-56 C-30,-64 -90,-50 -130,-24" fill="none" stroke="#c9f6ff" stroke-width="9" stroke-linecap="round" opacity=".75"/>'
    # pronotum + head
    o += f'<path d="M36,-50 Q100,-58 108,-30 L108,30 Q100,58 36,50 Q48,0 36,-50Z" fill="#e8b03a" stroke="{INKB}" stroke-width="7"/>'
    o += '<path d="M44,-42 Q96,-48 100,-26 L100,26 Q96,48 44,42 Q54,0 44,-42Z" fill="url(#elyB)"/>'
    o += '<path d="M56,-34 Q88,-38 94,-20" fill="none" stroke="#c9f6ff" stroke-width="6" opacity=".7" stroke-linecap="round"/>'
    o += f'<ellipse cx="135" cy="0" rx="34" ry="34" fill="#0f1a1e" stroke="{INKB}" stroke-width="7"/>'
    o += f'<circle cx="138" cy="-30" r="11" fill="#2a1a0a" stroke="{INKB}" stroke-width="3"/><circle cx="138" cy="30" r="11" fill="#2a1a0a" stroke="{INKB}" stroke-width="3"/>'
    o += '<circle cx="135" cy="-33" r="3.5" fill="#fff"/><circle cx="135" cy="27" r="3.5" fill="#fff"/>'
    o += '<path d="M120,-14 Q140,-22 156,-10" fill="none" stroke="#9ad8e6" stroke-width="5" opacity=".7" stroke-linecap="round"/>'
    return o + '</g>'


def make_B():
    random.seed(32)
    FI = '#170f06'
    D = FILTERS
    D += lin('skyB', [(0, '#2a0b1c'), (.45, '#7a2a2a'), (.75, '#d8752e'), (1, '#f1b252')])
    D += lin('gndB', [(0, '#3a2412'), (.4, '#1e1209'), (1, '#090503')])
    D += rad('sunB', 1250, 560, 760, [(0, '#fff2c0', 1), (.12, '#ffd77a', .9), (.4, '#f08a3a', .35), (1, '#7a2a2a', 0)])
    D += lin('frogB', [(0, '#c9b45e'), (.45, '#8d7b3a'), (1, '#3e3418')], x2=0.3, y2=1)
    D += rad('irisB', -10, -10, 50, [(0, '#fff3a8', 1), (.55, '#e0a42c', 1), (1, '#7a4a0a', 1)])
    D += lin('elyB', [(0, '#0b1418'), (.5, '#16323a'), (1, '#0b1418')])
    D += lin('tngB', [(0, '#ffb9c4'), (1, '#d8607a')])
    b = '<rect width="1920" height="1080" fill="url(#skyB)"/><rect width="1920" height="1080" fill="url(#sunB)"/>'
    b += '<circle cx="1250" cy="600" r="210" fill="#fff4cf" opacity=".9" filter="url(#b14)"/>'
    for i in range(14):  # sun rays
        a = math.radians(i * 360 / 14 + 5)
        b += f'<path d="M1250,600 L{1250 + math.cos(a - .05) * 1400:.0f},{600 + math.sin(a - .05) * 1400:.0f} L{1250 + math.cos(a + .05) * 1400:.0f},{600 + math.sin(a + .05) * 1400:.0f}Z" fill="#ffe6a0" opacity=".08"/>'
    for _ in range(120):
        b += grass(random.randint(-20, 1940), 800, random.randint(70, 260), random.randint(-40, 40), random.choice(['#3a1a14', '#2a120e', '#4a2416']), w=random.randint(6, 13))
    b += '<path d="M0,790 C500,770 1200,800 1920,780 L1920,1080 L0,1080Z" fill="url(#gndB)"/>'
    b += '<ellipse cx="1150" cy="945" rx="560" ry="40" fill="#000" opacity=".6" filter="url(#b14)"/>'
    # dust kicked up
    for _ in range(14):
        b += f'<circle cx="{random.randint(700, 1600)}" cy="{random.randint(880, 960)}" r="{random.randint(14, 40)}" fill="#c99a62" opacity="{random.uniform(.15, .35):.2f}" filter="url(#b4)"/>'
    # ---------- frog (side view, facing left, front lifted: bucking) ----------
    F = '<g transform="rotate(-9 1150 760)">'
    F += limb([(1180, 820), (1240, 900), (1320, 930)], 80, 40, '#6d5c2a', FI)   # far hind foot hint
    body = 'M690,690 C695,640 760,585 850,555 C960,515 1080,495 1200,500 C1340,503 1480,555 1540,635 C1580,695 1545,790 1470,812 C1350,848 1150,862 980,840 C880,826 790,790 740,752 C712,730 688,712 690,690Z'
    F += f'<path d="{body}" fill="url(#frogB)" stroke="{FI}" stroke-width="9"/>'
    F += '<clipPath id="fbB"><path d="' + body + '"/></clipPath><g clip-path="url(#fbB)">'
    F += '<path d="M700,720 C800,800 1000,850 1300,845 L1500,840 L1500,900 L700,900Z" fill="#efe2b0" opacity=".9"/>'
    for _ in range(26):
        x, y = random.randint(780, 1520), random.randint(510, 760)
        F += f'<ellipse cx="{x}" cy="{y}" rx="{random.randint(14, 34)}" ry="{random.randint(10, 22)}" transform="rotate({random.randint(-40, 40)} {x} {y})" fill="#3b3016" opacity=".7"/>'
    F += '<path d="M860,560 C1000,520 1200,515 1350,545 C1440,565 1510,610 1540,660" fill="none" stroke="#fff0b8" stroke-width="30" opacity=".5" filter="url(#b8)"/>'
    F += '</g>'
    F += '<path d="M870,553 C1000,512 1200,500 1350,528 C1450,550 1520,600 1544,650" fill="none" stroke="#fff6d4" stroke-width="7" opacity=".95" filter="url(#b2)"/>'
    F += f'<path d="M930,600 C1060,575 1250,575 1450,640" fill="none" stroke="#e8d48a" stroke-width="10" stroke-linecap="round" opacity=".55"/>'
    # hind leg folded (thigh, shin, long webbed foot)
    F += limb([(1480, 690), (1420, 790), (1330, 870)], 150, 80, 'url(#frogB)', FI)
    F += limb([(1320, 875), (1450, 900), (1560, 880)], 78, 54, '#8d7b3a', FI)
    for k in range(4):
        F += f'<ellipse cx="{1440 - k * 20}" cy="{760 + k * 30}" rx="22" ry="12" fill="#3b3016" opacity=".7"/>'
    F += f'<path d="M1560,880 L1380,935" stroke="{FI}" stroke-width="40" stroke-linecap="round"/><path d="M1560,880 L1380,935" stroke="#7d6c33" stroke-width="28" stroke-linecap="round"/>'
    F += fingers(1385, 935, 175, 70, '#8d7b3a', FI, n=4, spread=50, w=12)
    # front leg raised and pawing
    F += limb([(880, 780), (830, 860), (760, 880)], 66, 40, '#8d7b3a', FI)
    F += fingers(752, 882, 190, 48, '#a69250', FI, n=4, spread=70, w=12)
    # tympanum, mouth, tongue
    F += f'<circle cx="1000" cy="630" r="40" fill="#6d5226" stroke="{FI}" stroke-width="6"/><circle cx="990" cy="620" r="14" fill="#c9a865" opacity=".5"/>'
    F += f'<path d="M698,700 C780,722 880,725 960,700" fill="none" stroke="{FI}" stroke-width="8" stroke-linecap="round"/>'
    F += f'<path d="M712,708 C690,750 670,800 694,830 C716,856 750,834 744,800 C740,770 738,740 742,714Z" fill="url(#tngB)" stroke="{FI}" stroke-width="7"/>'
    F += '<ellipse cx="702" cy="805" rx="7" ry="13" fill="#fff" opacity=".6"/>'
    F += f'<ellipse cx="722" cy="640" rx="9" ry="6" fill="{FI}"/>'
    # eye: bulging, looking back at the rider, panicked
    F += f'<circle cx="868" cy="552" r="76" fill="#7d6c33" stroke="{FI}" stroke-width="9"/>'
    F += f'<circle cx="872" cy="545" r="62" fill="#fffdf2" stroke="{FI}" stroke-width="6"/>'
    F += '<g transform="translate(900 526)"><circle r="40" fill="url(#irisB)" stroke="#5a3a0a" stroke-width="4"/><ellipse cx="10" cy="-6" rx="13" ry="8" fill="#0a0703"/>'
    F += '<ellipse cx="-14" cy="-16" rx="10" ry="7" fill="#fff"/><circle cx="14" cy="15" r="4" fill="#fff" opacity=".7"/></g>'
    F += f'<path d="M790,500 Q850,445 950,470" fill="none" stroke="{FI}" stroke-width="16" stroke-linecap="round"/>'
    F += '</g>'
    b += F
    # rider beetle, jaws into the back
    b += '<ellipse cx="1200" cy="560" rx="200" ry="40" fill="#000" opacity=".35" filter="url(#b8)" transform="rotate(-12 1200 560)"/>'
    b += beetle(1330, 478, 170, 1.2)
    for a in (110, 150, 190, 230):
        ax, ay = 1050 + math.cos(math.radians(a)) * 62, 525 + math.sin(math.radians(a)) * 62
        bx, by = 1050 + math.cos(math.radians(a)) * 100, 525 + math.sin(math.radians(a)) * 100
        b += f'<path d="M{ax:.0f},{ay:.0f} L{bx:.0f},{by:.0f}" stroke="#fff8d8" stroke-width="8" stroke-linecap="round"/>'
    b += shake(610, 690, 1.2, flip=True, col='#fff3d0') + shake(1650, 560, 1.2, col='#fff3d0')
    b += sweat(700, 500, 1.3, -30) + sweat(640, 590, 1.0, -50) + sweat(800, 440, 1.1, -10)
    b += spark(1480, 360, 22) + spark(1580, 470, 14) + spark(1120, 330, 16)
    # mascot: hands up, shocked, ankle-deep in the grass
    b += '<ellipse cx="300" cy="1002" rx="150" ry="22" fill="#000" opacity=".5" filter="url(#b4)"/>'
    b += frog(300, 1000, 3.0, mouth='o', look=(6, -3), arms=('M-34 -22 q-18 -10 -22 -38', 'M38 -22 q18 -10 22 -38'), rim='#ffd890')
    b += '<path d="M430,720 l-6,64" stroke="#fff3d0" stroke-width="14" stroke-linecap="round"/><circle cx="420" cy="812" r="9" fill="#fff3d0"/>'
    for _ in range(16):
        b += grass(random.randint(80, 560), 1090, random.randint(50, 110), random.randint(-30, 30), '#120804', w=9)
    return page('#2a0b1c', svg(D, b), [('WHO EATS', 175, 'w'), ('WHOM?', 270, 'y')], outline='#1a0610')


# =====================================================================================
# C  intuitive: frog skeleton on the mud, a fat larva asleep on it (S42 "only a pile of bones")
# =====================================================================================
def bone(p, q, w, col='#efe6cf', ink='#2a2440'):
    d = norm((q[0] - p[0], q[1] - p[1])); n = (-d[1], d[0]); o = ''
    for layer, (c, ww, k) in enumerate(((ink, w + 9, 4.5), (col, w, 0))):
        o += f'<path d="M{p[0]:.0f},{p[1]:.0f} L{q[0]:.0f},{q[1]:.0f}" stroke="{c}" stroke-width="{ww}" stroke-linecap="round"/>'
        for e in (p, q):
            for sg in (-1, 1):
                cc = add(e, n, sg * w * .45)
                o += f'<circle cx="{cc[0]:.0f}" cy="{cc[1]:.0f}" r="{w * .55 + k:.1f}" fill="{c}"/>'
    o += f'<path d="M{add(p, n, -w * .15)[0]:.0f},{add(p, n, -w * .15)[1]:.0f} L{add(q, n, -w * .15)[0]:.0f},{add(q, n, -w * .15)[1]:.0f}" stroke="#fffdf4" stroke-width="{w * .25:.1f}" stroke-linecap="round" opacity=".8"/>'
    return o


def make_C():
    random.seed(43)
    D = FILTERS + LARVA_DEFS
    D += lin('skyC', [(0, '#060a1e'), (.6, '#141c44'), (1, '#252a5a')])
    D += lin('mudC', [(0, '#1a1c30'), (.5, '#0e0f1c'), (1, '#05060c')])
    D += rad('moonC', 1500, 200, 600, [(0, '#e8f0ff', .7), (.3, '#9fb2ff', .25), (1, '#141c44', 0)])
    D += rad('poolC', 1150, 740, 480, [(0, '#fff3c8', .75), (.4, '#f2d27a', .35), (1, '#f2d27a', 0)])
    D += lin('beamC', [(0, '#fff6c8'), (1, '#fff6c8')], x2=1, y2=0)
    b = '<rect width="1920" height="1080" fill="url(#skyC)"/><rect width="1920" height="1080" fill="url(#moonC)"/>'
    b += '<circle cx="1560" cy="170" r="70" fill="#f4f7ff"/><circle cx="1540" cy="160" r="14" fill="#d6dcf0"/><circle cx="1585" cy="195" r="9" fill="#d6dcf0"/>'
    b += '<circle cx="1560" cy="170" r="110" fill="#c8d4ff" opacity=".3" filter="url(#b24)"/>'
    for _ in range(70):
        b += f'<circle cx="{random.randint(900, 1900)}" cy="{random.randint(10, 480)}" r="{random.choice([1.4, 2, 2.8])}" fill="#eef2ff" opacity="{random.uniform(.2, .8):.2f}"/>'
    for _ in range(100):
        b += grass(random.randint(-20, 1940), 560, random.randint(60, 230), random.randint(-40, 40), random.choice(['#0a0e24', '#0d1230', '#101636']), w=random.randint(6, 12))
    b += '<path d="M0,540 C500,520 1200,550 1920,530 L1920,1080 L0,1080Z" fill="url(#mudC)"/>'
    for _ in range(30):
        x, y = random.randint(0, 1900), random.randint(600, 1060)
        b += f'<ellipse cx="{x}" cy="{y}" rx="{random.randint(20, 60)}" ry="{random.randint(4, 10)}" fill="#2a2e50" opacity=".5"/>'
    # flashlight beam from the mascot onto the bones
    b += '<path d="M470,872 L900,500 L1500,640 L1300,980 Z" fill="#fff3c0" opacity=".16" filter="url(#b14)"/>'
    b += '<ellipse cx="1150" cy="740" rx="520" ry="240" fill="url(#poolC)"/>'
    # ---------- frog skeleton (dorsal view, lying flat, perspective squash) ----------
    S = '<g transform="translate(1110 760) scale(.8 .5) rotate(-6)">'
    S += '<ellipse cx="0" cy="40" rx="430" ry="330" fill="#000" opacity=".25" filter="url(#b24)"/>'
    # hind legs (Z-fold, splayed)
    for sg in (-1, 1):
        hip = (sg * 40, 170)
        knee = (sg * 270, 130); ankle = (sg * 200, 300); foot = (sg * 340, 360)
        S += bone(hip, knee, 30) + bone(knee, ankle, 26) + bone(ankle, foot, 18)
        for k in range(5):
            a = math.radians((-20 + k * 14) if sg > 0 else (200 - k * 14))
            S += bone(foot, (foot[0] + math.cos(a) * 95, foot[1] + math.sin(a) * 95 + 30), 8)
        # front legs
        sh = (sg * 90, -150); el = (sg * 210, -100); wr = (sg * 250, -10)
        S += bone(sh, el, 20) + bone(el, wr, 16)
        for k in range(4):
            a = math.radians((40 + k * 25) if sg > 0 else (140 - k * 25))
            S += bone(wr, (wr[0] + math.cos(a) * 55, wr[1] + math.sin(a) * 55), 7)
        # ilia (long hip bones)
        S += bone((sg * 30, 180), (sg * 70, 20), 20)
    # spine + urostyle
    S += bone((0, 190), (0, 60), 16)
    for k in range(8):
        y = 50 - k * 28
        S += bone((-60 + k * 3, y), (60 - k * 3, y), 10)
        S += f'<ellipse cx="0" cy="{y}" rx="20" ry="14" fill="#efe6cf" stroke="#2a2440" stroke-width="5"/>'
    # skull: wide U with two huge orbits
    S += ('<path d="M-170,-210 C-200,-300 -120,-400 0,-405 C120,-400 200,-300 170,-210 C150,-180 -150,-180 -170,-210Z" '
          'fill="#efe6cf" stroke="#2a2440" stroke-width="9"/>')
    for sg in (-1, 1):
        S += f'<ellipse cx="{sg * 82}" cy="-290" rx="62" ry="70" fill="#2a2440" stroke="#2a2440" stroke-width="4"/>'
        S += f'<ellipse cx="{sg * 82}" cy="-280" rx="40" ry="44" fill="#141428"/>'
    S += '<path d="M-18,-395 L0,-200 L18,-395" fill="#d6caa8" stroke="#2a2440" stroke-width="4" opacity=".9"/>'
    S += '<path d="M-150,-260 C-150,-330 -100,-380 -30,-392" fill="none" stroke="#fffdf4" stroke-width="10" stroke-linecap="round" opacity=".8"/>'
    S += '</g>'
    b += S
    # fat larva asleep across the skeleton
    b += '<ellipse cx="1620" cy="830" rx="190" ry="30" fill="#000" opacity=".45" filter="url(#b8)"/>'
    b += larva(((1800, 800), (1740, 650), (1540, 650), (1470, 770)), W=60, opn=0.0, head_rot=20,
               ants=((-60, 2.4, -40), (-20, 2.4, -50)), legs='walk', vside=-1, light=(.6, -1), rim='#fff6d6')
    b += '<g font-family="Fredoka" font-weight="700" fill="#fff6d6" stroke="#1a1838" stroke-width="7" paint-order="stroke">'
    b += '<text x="1640" y="540" font-size="70">z</text><text x="1700" y="460" font-size="96">z</text><text x="1770" y="360" font-size="128">Z</text></g>'
    b += spark(1640, 560, 22) + spark(960, 610, 16) + spark(1500, 900, 14) + spark(1060, 900, 12)
    # mascot with flashlight, shocked
    torch = ('<g><rect x="34" y="-42" width="34" height="16" rx="4" fill="#d9dde8" stroke="#1d2b1c" stroke-width="3"/>'
             '<path d="M66 -46 L80 -50 L80 -18 L66 -22Z" fill="#f2d27a" stroke="#1d2b1c" stroke-width="3"/></g>')
    b += '<ellipse cx="300" cy="1002" rx="150" ry="22" fill="#000" opacity=".55" filter="url(#b4)"/>'
    b += frog(300, 1000, 3.1, mouth='o', look=(7, 0), arms=('M-34 -22 q-14 6 -16 22', 'M38 -22 q10 -4 4 -14'), front=torch, rim='#fff3c0')
    b += '<circle cx="545" cy="855" r="40" fill="#fff6c8" opacity=".7" filter="url(#b8)"/>'
    for _ in range(14):
        b += grass(random.randint(80, 520), 1090, random.randint(50, 110), random.randint(-30, 30), '#05060f', w=9)
    return page('#060a1e', svg(D, b), [('FROG + BUG', 165, 'w'), ('= BONES', 270, 'y')], outline='#070818')


for name, fn in (('A', make_A), ('B', make_B), ('C', make_C)):
    open(os.path.join(HERE, f'{name}.html'), 'w').write(fn())
