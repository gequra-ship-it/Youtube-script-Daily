# Thumbnails A-C for frog-hunting-beetle, v3 (owner on v2: "like #2's SIDE-view running frog, but with #1's larva hanging from the
# frog's mouth, so the bug hunts the frog by going for its MOUTH; the frog should look FLUSTERED; the current frog is gross").
# v1, v2 kept in ./v1, ./v2. Guideline 16-2/16-6/16-8, brief tools/briefs/thumb_art.md. Run: python3 videos/frog-hunting-beetle/thumb/make.py
# One idea, three variations. The eaten frog = a cute, smooth jade frog in SIDE profile (no warts, closed mouth line, big glossy eye with a
# tiny pupil, raised brow, sweat) - clearly not the mascot (mascot: small, front-facing, yellow-green, bystander with props).
# A  IT BIT / BACK     tight close-up of the frog's head, larva clamped on its lower lip, golden backlight  (S28 "dodge a tongue and bite back")
# B  WHO EATS / WHOM?  whole frog mid-hop over a moonlit pond, larva swinging from its lip                    (S10 role reversal)
# C  BUG 1 / FROG 0    frog sitting side-on, larva has just grabbed its lip, '!?', shocked mascot in fireflies (S26-S29 the tongue fails, the larva bites on)
# No blood or wounds.
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



# pale larva (owner: "pale, segmented") - overrides the v2 amber gradients
LARVA_DEFS = ('<radialGradient id="lvb" cx=".45" cy=".35" r=".7"><stop offset="0" stop-color="#fffaea"/><stop offset=".55" stop-color="#f3dba6"/>'
              '<stop offset="1" stop-color="#b88a4c"/></radialGradient>'
              '<radialGradient id="lvh" cx=".4" cy=".35" r=".75"><stop offset="0" stop-color="#e6a85e"/><stop offset=".6" stop-color="#9a5522"/>'
              '<stop offset="1" stop-color="#4a230c"/></radialGradient>')


def larva_grip(G, ddeg, W, L, bend=0.0, **kw):
    """larva whose closed jaw tips end just inside point G; ddeg = direction (deg, SVG) the head points; bend sways the tail sideways"""
    d = (math.cos(math.radians(ddeg)), math.sin(math.radians(ddeg))); s = (-d[1], d[0])
    seg = L / len(PROF)
    neck = add(G, d, -(seg * 0.55 + 0.55 * W + 0.82 * W + 2.25 * W))
    c2 = add(neck, d, -L * 0.38)
    c1 = add(add(neck, d, -L * 0.75), s, bend * L * 0.5)
    tail = add(add(neck, d, -L * 0.95), s, bend * L)
    return larva((tail, c1, c2, neck), W, opn=-0.07, **kw)


# ---------------- the eaten frog: cute, smooth, side profile, facing left ----------------
JADE = dict(hi='#9fe6c8', mid='#45b596', lo='#1f6f63', limb='#3aa088', far='#2a7d6c', belly='#fff5d8', belly2='#e9d9a8', ink='#0f2422')
BODY = ('M-240,-60 C-242,-130 -190,-175 -130,-180 C-60,-185 0,-170 60,-150 C150,-120 232,-60 236,10 C238,70 190,104 120,106 '
        'L-60,102 C-140,100 -200,62 -225,12 C-236,-14 -242,-36 -240,-60Z')
G_LOC = (-233, -38)
MOUTH = 'M-238,-50 Q-210,-38 -188,-46 Q-168,-56 -146,-44 Q-136,-38 -128,-44'     # lower lip, just behind the snout tip, where the larva bites


def toes(x, y, ang, L, col, pad, ink, n=3, spread=56, w=11):
    o = ''; tips = []
    for k in range(n):
        a = math.radians(ang - spread / 2 + spread * k / (n - 1))
        Lk = L * (0.85 if k in (0, n - 1) else 1.0)
        tips.append((x + math.cos(a) * Lk, y + math.sin(a) * Lk))
    for tx, ty in tips:
        o += f'<path d="M{x:.1f},{y:.1f} L{tx:.1f},{ty:.1f}" stroke="{ink}" stroke-width="{w + 7}" stroke-linecap="round"/>'
        o += f'<circle cx="{tx:.1f}" cy="{ty:.1f}" r="{w * .78 + 3.5:.1f}" fill="{ink}"/>'
    for tx, ty in tips:
        o += f'<path d="M{x:.1f},{y:.1f} L{tx:.1f},{ty:.1f}" stroke="{col}" stroke-width="{w}" stroke-linecap="round"/>'
        o += f'<circle cx="{tx:.1f}" cy="{ty:.1f}" r="{w * .78:.1f}" fill="{pad}"/>'
    return o


def soft_limb(pts, w0, w1, fill, ink, sw=7, hl=None):
    """rounded capsule limb along a quadratic curve (cute, no sharp ends)"""
    d = f'M{pts[0][0]},{pts[0][1]} Q{pts[1][0]},{pts[1][1]} {pts[2][0]},{pts[2][1]}'
    w = (w0 + w1) / 2
    o = f'<path d="{d}" fill="none" stroke="{ink}" stroke-width="{w + 2 * sw}" stroke-linecap="round"/>'
    o += f'<path d="{d}" fill="none" stroke="{fill}" stroke-width="{w}" stroke-linecap="round"/>'
    if hl:
        o += f'<path d="{d}" fill="none" stroke="{hl}" stroke-width="{w * .22:.1f}" stroke-linecap="round" opacity=".5" transform="translate({-w * .12:.1f} {-w * .2:.1f})"/>'
    return o


def cute_frog(uid, x, y, s, rot=0, pose='sit', P=JADE, rim='#fff1c8', look=(-12, 16), far_arm='up', glint=1.0):
    """returns (main_svg, cover_svg, defs, G_global). Facing left. cover = lip drawn again over the larva's jaw tips."""
    ink = P['ink']
    D = (f'<radialGradient id="fb{uid}" cx=".32" cy=".18" r=".85"><stop offset="0" stop-color="{P["hi"]}"/><stop offset=".45" stop-color="{P["mid"]}"/>'
         f'<stop offset="1" stop-color="{P["lo"]}"/></radialGradient>'
         f'<linearGradient id="fl{uid}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{P["mid"]}"/><stop offset="1" stop-color="{P["lo"]}"/></linearGradient>'
         f'<radialGradient id="be{uid}" cx=".4" cy=".2" r=".9"><stop offset="0" stop-color="{P["belly"]}"/><stop offset="1" stop-color="{P["belly2"]}"/></radialGradient>'
         f'<radialGradient id="sc{uid}" cx=".38" cy=".32" r=".75"><stop offset="0" stop-color="#ffffff"/><stop offset=".7" stop-color="#f4f7f2"/><stop offset="1" stop-color="#c9d6d6"/></radialGradient>'
         f'<radialGradient id="ir{uid}" cx=".35" cy=".3" r=".8"><stop offset="0" stop-color="#fff0a0"/><stop offset=".6" stop-color="#e3a82e"/><stop offset="1" stop-color="#8a5a10"/></radialGradient>'
         f'<clipPath id="cb{uid}"><path d="{BODY}"/><circle cx="-118" cy="-180" r="64"/></clipPath>'
         f'<clipPath id="cg{uid}"><circle cx="{G_LOC[0] + 12}" cy="{G_LOC[1] + 2}" r="17"/></clipPath>')
    tr = f'translate({x} {y}) rotate({rot}) scale({s})'
    o = f'<g transform="{tr}" stroke-linejoin="round" stroke-linecap="round">'
    # ---- far side limbs (darker) ----
    if far_arm == 'up':          # flustered: the far hand thrown up behind the head
        o += toes(-58, -290, -115, 42, P['far'], P['limb'], ink, w=10)
        o += soft_limb([(-40, -110), (-10, -215), (-55, -285)], 40, 30, P['far'], ink)
    if pose == 'sit':
        o += toes(-112, 110, 200, 34, P['far'], P['far'], ink, w=9)
        o += soft_limb([(-70, 60), (-95, 95), (-110, 108)], 34, 26, P['far'], ink)
    elif pose == 'hop':
        o += soft_limb([(150, -10), (260, -50), (370, -40)], 70, 38, P['far'], ink)
        o += toes(505, -52, -10, 42, P['far'], P['far'], ink, w=10)
        o += soft_limb([(370, -40), (450, -40), (500, -50)], 40, 30, P['far'], ink)
        o += toes(-214, 112, 160, 34, P['far'], P['far'], ink, w=9)
        o += soft_limb([(-90, 50), (-150, 90), (-210, 110)], 34, 26, P['far'], ink)
    # ---- body + eye dome, merged silhouette ----
    o += f'<path d="{BODY}" fill="none" stroke="{ink}" stroke-width="16"/><circle cx="-118" cy="-180" r="64" fill="none" stroke="{ink}" stroke-width="16"/>'
    o += f'<path d="{BODY}" fill="url(#fb{uid})"/><circle cx="-118" cy="-180" r="64" fill="url(#fb{uid})"/>'
    o += f'<g clip-path="url(#cb{uid})">'
    o += f'<path d="M-250,0 C-170,70 -40,62 80,60 C160,58 220,40 260,20 L260,140 L-250,140Z" fill="url(#be{uid})"/>'
    o += f'<ellipse cx="150" cy="80" rx="190" ry="90" fill="{P["lo"]}" opacity=".35" filter="url(#b14)"/>'
    o += f'<path d="M-236,-70 C-230,-140 -180,-178 -130,-182" fill="none" stroke="{rim}" stroke-width="16" opacity=".55" filter="url(#b4)"/>'
    o += f'<path d="M-60,-178 C30,-170 150,-125 225,-40" fill="none" stroke="{rim}" stroke-width="26" opacity=".6" filter="url(#b8)"/>'
    o += f'<ellipse cx="-20" cy="-120" rx="70" ry="24" fill="#ffffff" opacity=".22" filter="url(#b8)" transform="rotate(10 -20 -120)"/>'
    o += '</g>'
    o += f'<path d="M-50,-183 C40,-175 150,-128 228,-42" fill="none" stroke="{rim}" stroke-width="5" opacity=".95" filter="url(#b2)"/>'
    o += f'<path d="M-170,-232 C-150,-246 -110,-250 -80,-232" fill="none" stroke="{rim}" stroke-width="5" opacity=".9" filter="url(#b2)"/>'
    # ---- near hind leg ----
    if pose == 'sit':
        o += f'<path d="M60,105 C20,112 -40,114 -60,108 C-40,96 40,92 80,96Z" fill="{P["limb"]}" stroke="{ink}" stroke-width="7"/>'
        o += toes(-58, 108, 185, 40, P['limb'], P['hi'], ink, w=10)
        o += f'<ellipse cx="125" cy="40" rx="108" ry="70" transform="rotate(-22 125 40)" fill="url(#fl{uid})" stroke="{ink}" stroke-width="8"/>'
        o += f'<path d="M50,0 C90,-30 160,-30 200,-5" fill="none" stroke="{P["hi"]}" stroke-width="12" opacity=".7" stroke-linecap="round"/>'
    elif pose == 'hop':
        o += soft_limb([(130, 40), (250, 10), (360, 20)], 100, 50, f'url(#fl{uid})', ink, 8)
        o += soft_limb([(360, 20), (450, 30), (510, 10)], 48, 34, P['limb'], ink)
        o += f'<path d="M150,0 C220,-25 290,-20 350,0" fill="none" stroke="{P["hi"]}" stroke-width="12" opacity=".6" stroke-linecap="round"/>'
        o += toes(516, 8, -5, 48, P['limb'], P['hi'], ink, w=11)
    # ---- face ----
    o += f'<ellipse cx="-168" cy="-98" rx="28" ry="14" fill="#ff8f9e" opacity=".55"/>'
    o += f'<ellipse cx="-222" cy="-96" rx="6" ry="4.5" fill="{ink}"/>'
    o += f'<path d="{MOUTH}" fill="none" stroke="{ink}" stroke-width="7"/>'
    # eye: big glossy, wide, tiny pupil looking down at the larva
    ex, ey = -116, -186
    o += f'<circle cx="{ex}" cy="{ey}" r="52" fill="url(#sc{uid})" stroke="{ink}" stroke-width="6"/>'
    px, py = ex + look[0], ey + look[1]
    o += f'<circle cx="{px}" cy="{py}" r="17" fill="url(#ir{uid})" stroke="#5a3a0a" stroke-width="2.5"/><circle cx="{px - 1}" cy="{py + 1}" r="8" fill="#0a0703"/>'
    o += f'<circle cx="{px - 6}" cy="{py - 6}" r="4" fill="#fff"/>'
    o += f'<ellipse cx="{ex - 20}" cy="{ey - 24}" rx="16" ry="10" transform="rotate(-30 {ex - 20} {ey - 24})" fill="#fff" opacity="{.95 * glint:.2f}"/>'
    o += f'<path d="M{ex + 30},{ey + 26} Q{ex + 40},{ey + 8} {ex + 38},{ey - 10}" fill="none" stroke="#fff" stroke-width="5" opacity=".75"/>'
    # raised, worried brow + surprise ticks
    o += f'<path d="M-178,-262 Q-140,-300 -88,-276" fill="none" stroke="{ink}" stroke-width="12"/>'
    for a in (-150, -118, -86):
        r0, r1 = 110, 150
        o += (f'<path d="M{ex + math.cos(math.radians(a)) * r0:.0f},{ey - 10 + math.sin(math.radians(a)) * r0:.0f} '
              f'L{ex + math.cos(math.radians(a)) * r1:.0f},{ey - 10 + math.sin(math.radians(a)) * r1:.0f}" stroke="{ink}" stroke-width="9"/>')
    # near front arm
    if pose == 'sit' and far_arm == 'cheek':   # flustered: near hand pressed to the cheek
        o += toes(-152, -84, -95, 34, P['limb'], P['hi'], ink, w=10)
        o += soft_limb([(-95, 40), (-175, 10), (-152, -76)], 30, 24, P['limb'], ink, hl=P['hi'])
    elif pose == 'sit':
        o += toes(-142, 108, 195, 36, P['limb'], P['hi'], ink, w=10)
        o += soft_limb([(-105, 40), (-128, 82), (-140, 106)], 34, 26, P['limb'], ink, hl=P['hi'])
    elif pose == 'hop':
        o += toes(-250, 92, 175, 38, P['limb'], P['hi'], ink, w=10)
        o += soft_limb([(-110, 40), (-170, 80), (-245, 92)], 42, 30, P['limb'], ink, hl=P['hi'])
    o += '</g>'
    # cover: the lip over the jaw tips
    cov = (f'<g transform="{tr}"><g clip-path="url(#cg{uid})"><path d="{BODY}" fill="none" stroke="{ink}" stroke-width="16"/>'
           f'<path d="{BODY}" fill="url(#fb{uid})"/></g><path d="{MOUTH}" fill="none" stroke="{ink}" stroke-width="7" stroke-linecap="round"/></g>')
    a = math.radians(rot)
    gx, gy = G_LOC[0] * s, G_LOC[1] * s
    G = (x + gx * math.cos(a) - gy * math.sin(a), y + gx * math.sin(a) + gy * math.cos(a))
    return o, cov, D, G


def pinch(G, r0, r1, angs, col='#fff6d6', w=8):
    return ''.join(f'<path d="M{G[0] + math.cos(math.radians(a)) * r0:.0f},{G[1] + math.sin(math.radians(a)) * r0:.0f} '
                   f'L{G[0] + math.cos(math.radians(a)) * r1:.0f},{G[1] + math.sin(math.radians(a)) * r1:.0f}" stroke="{col}" stroke-width="{w}" stroke-linecap="round"/>'
                   for a in angs)


def mascot(x, y, s, **kw):
    return f'<ellipse cx="{x}" cy="{y + 2}" rx="{s * 50:.0f}" ry="{s * 7:.0f}" fill="#000" opacity=".45" filter="url(#b4)"/>' + frog(x, y, s, **kw)


def bang(x, y, s=1.0, col='#fff3d0'):   # '!' mark
    return f'<path d="M{x},{y} l{-3 * s:.0f},{70 * s:.0f}" stroke="{col}" stroke-width="{14 * s:.0f}" stroke-linecap="round"/><circle cx="{x - 4 * s:.0f}" cy="{y + 98 * s:.0f}" r="{9 * s:.0f}" fill="{col}"/>'


# =====================================================================================
# A  close-up of the frog's head, larva clamped on the lip, golden backlight
# =====================================================================================
def make_A():
    random.seed(101)
    D = FILTERS + LARVA_DEFS
    D += lin('skyA', [(0, '#2b0f2e'), (.45, '#7a2c3c'), (.8, '#d9753a'), (1, '#f3b257')])
    D += rad('sunA', 1500, 330, 900, [(0, '#fff6d8', 1), (.15, '#ffd98a', .85), (.45, '#f08a3a', .3), (1, '#7a2c3c', 0)])
    D += lin('waterA', [(0, '#3a1a2a'), (.3, '#24101c'), (1, '#0c0509')])
    b = '<rect width="1920" height="1080" fill="url(#skyA)"/><rect width="1920" height="1080" fill="url(#sunA)"/>'
    b += '<circle cx="1500" cy="330" r="190" fill="#fff6dc" opacity=".85" filter="url(#b24)"/>'
    for i in range(16):
        a = math.radians(i * 360 / 16 + 4)
        b += (f'<path d="M1500,330 L{1500 + math.cos(a - .04) * 1500:.0f},{330 + math.sin(a - .04) * 1500:.0f} '
              f'L{1500 + math.cos(a + .04) * 1500:.0f},{330 + math.sin(a + .04) * 1500:.0f}Z" fill="#ffe9b0" opacity=".07"/>')
    for _ in range(90):   # blurred far reeds (depth)
        b += grass(random.randint(-20, 1940), 760, random.randint(80, 300), random.randint(-50, 50), random.choice(['#5a2236', '#4a1c2e', '#6a2a3a']), w=random.randint(7, 14))
    b += '<path d="M0,740 C500,725 1200,750 1920,735 L1920,1080 L0,1080Z" fill="url(#waterA)"/>'
    for _ in range(18):
        x = random.randint(0, 1900); y = random.randint(780, 1060)
        b += f'<path d="M{x},{y} l{random.randint(40, 120)},0" stroke="#f7b866" stroke-width="3" opacity="{random.uniform(.15, .4):.2f}"/>'
    # bokeh
    for _ in range(14):
        b += f'<circle cx="{random.randint(800, 1900)}" cy="{random.randint(80, 700)}" r="{random.randint(10, 34)}" fill="#ffe2a0" opacity="{random.uniform(.08, .22):.2f}" filter="url(#b4)"/>'
    fo, cov, fd, G = cute_frog('A', 1610, 700, 2.1, rot=-4, pose='sit', far_arm='none', rim='#fff0c4', look=(-16, 18))
    D += fd
    b += '<ellipse cx="1500" cy="930" rx="520" ry="34" fill="#000" opacity=".5" filter="url(#b14)"/>'
    b += fo
    # the larva: hangs from the lower lip, body arching back, antennae waving
    b += larva_grip(G, -62, 58, 640, bend=0.3, head_rot=0, ants=((-55, 3.8, -35), (55, 3.8, 45)), legs='flail', vside=1,
                    light=(1, -.5), rim='#fff6dc', wave=True)
    b += cov
    b += pinch(G, 70, 110, (150, 185, 215, 250))
    b += shake(1010, 330, 1.0, flip=True)
    b += sweat(1180, 150, 1.5, -25) + sweat(1640, 120, 1.1, 25) + sweat(1090, 420, 1.0, -40)
    b += spark(980, 620, 20) + spark(1260, 900, 14) + spark(1700, 830, 12)
    # mascot: shocked, notebook
    b += mascot(300, 1010, 2.7, mouth='o', look=(7, -2), arms=('M-34 -22 q-4 14 12 -10', 'M38 -22 q8 14 -10 -12'), front=notebook_front(), rim='#ffd9a0')
    b += bang(445, 735, 0.9)
    for _ in range(14):
        b += grass(random.randint(60, 600), 1090, random.randint(60, 130), random.randint(-30, 30), '#12060c', w=9)
    return page('#2b0f2e', svg(D, b), [('IT BIT', 200, 'w'), ('BACK', 300, 'y')], outline='#1a0610')


# =====================================================================================
# B  whole frog mid-hop over a moonlit pond, larva swinging from its lip
# =====================================================================================
def make_B():
    random.seed(202)
    D = FILTERS + LARVA_DEFS
    D += lin('skyB', [(0, '#050c22'), (.55, '#12305a'), (1, '#1f5a74')])
    D += rad('moonB', 1240, 380, 760, [(0, '#f4f8ff', .95), (.14, '#cfe4ff', .7), (.45, '#5d9fd0', .22), (1, '#12305a', 0)])
    D += lin('pondB', [(0, '#123a52'), (.4, '#0a2234'), (1, '#030a12')])
    b = '<rect width="1920" height="1080" fill="url(#skyB)"/><rect width="1920" height="1080" fill="url(#moonB)"/>'
    for _ in range(80):
        b += f'<circle cx="{random.randint(700, 1900)}" cy="{random.randint(10, 520)}" r="{random.choice([1.4, 2, 2.8])}" fill="#eef6ff" opacity="{random.uniform(.2, .8):.2f}"/>'
    b += '<circle cx="1240" cy="380" r="235" fill="#f6f9ff"/><circle cx="1240" cy="380" r="300" fill="#dbe9ff" opacity=".35" filter="url(#b24)"/>'
    b += '<circle cx="1170" cy="320" r="40" fill="#e3ebf8"/><circle cx="1330" cy="440" r="28" fill="#e3ebf8"/><circle cx="1300" cy="300" r="18" fill="#e3ebf8"/>'
    for _ in range(110):
        b += grass(random.randint(-20, 1940), 780, random.randint(60, 260), random.randint(-40, 40), random.choice(['#06182a', '#081e32', '#0a243a']), w=random.randint(6, 12))
    b += '<path d="M0,770 C500,755 1200,780 1920,765 L1920,1080 L0,1080Z" fill="url(#pondB)"/>'
    b += '<path d="M1080,800 L1400,800 L1460,1080 L1020,1080Z" fill="#cfe4ff" opacity=".12" filter="url(#b8)"/>'   # moon path on the water
    for k in range(9):
        y = 810 + k * 28; w = 180 + k * 40
        b += f'<path d="M{1240 - w / 2:.0f},{y} l{w:.0f},0" stroke="#e6f0ff" stroke-width="5" stroke-linecap="round" opacity="{.5 - k * .04:.2f}" stroke-dasharray="{40 + k * 6} {30 + k * 4}"/>'
    # lily pads + the ripple where the frog took off
    for (x, y, r) in ((560, 900, 70), (820, 1000, 55), (1500, 860, 60)):
        b += f'<ellipse cx="{x}" cy="{y}" rx="{r}" ry="{r * .32:.0f}" fill="#1f5c3c" stroke="#081a12" stroke-width="5"/><path d="M{x},{y} l{r * .8:.0f},{-r * .1:.0f}" stroke="#081a12" stroke-width="5"/>'
    for k in range(3):
        b += f'<ellipse cx="1500" cy="860" rx="{90 + k * 60}" ry="{20 + k * 13}" fill="none" stroke="#cfe4ff" stroke-width="4" opacity="{.5 - k * .14:.2f}"/>'
    fo, cov, fd, G = cute_frog('B', 1380, 610, 1.02, rot=10, pose='hop', far_arm='none', rim='#e8f4ff', look=(-14, 18),
                               P=dict(JADE, hi='#a8f0d4', mid='#3fae93', lo='#195a56'))
    D += fd
    # speed lines behind the hop
    for k, (y, L) in enumerate(((380, 200), (450, 260), (520, 180), (590, 240))):
        b += f'<path d="M{1640 + k * 20},{y} l{L},{-30}" stroke="#e6f0ff" stroke-width="8" stroke-linecap="round" opacity=".55"/>'
    b += '<ellipse cx="1150" cy="990" rx="380" ry="26" fill="#000" opacity=".45" filter="url(#b14)"/>'
    b += fo
    b += larva_grip(G, -112, 40, 330, bend=-0.55, head_rot=0, ants=((-50, 3.8, -40), (50, 3.8, 40)), legs='flail', vside=1,
                    light=(1, -.6), rim='#eef6ff', wave=True)
    b += cov
    b += pinch(G, 55, 88, (160, 195, 225))
    b += sweat(1150, 300, 1.0, -30) + sweat(1440, 230, 1.0, 15)
    b += spark(1520, 620, 18) + spark(960, 820, 14) + spark(640, 640, 12)
    # mascot on a lily pad at the left, hands up
    b += '<ellipse cx="300" cy="1000" rx="170" ry="44" fill="#1f5c3c" stroke="#081a12" stroke-width="6"/>'
    b += frog(300, 1000, 2.7, mouth='o', look=(7, -3), arms=('M-34 -22 q-18 -10 -22 -38', 'M38 -22 q18 -10 22 -38'), rim='#dbe9ff')
    b += bang(440, 735, 0.9, '#eef6ff')
    return page('#050c22', svg(D, b), [('WHO EATS', 175, 'w'), ('WHOM?', 270, 'y')], outline='#040a1a')


# =====================================================================================
# C  frog sitting side-on, larva just grabbed its lip, fireflies, shocked mascot
# =====================================================================================
def make_C():
    random.seed(303)
    D = FILTERS + LARVA_DEFS
    D += lin('skyC', [(0, '#160a2e'), (.5, '#3d1a5a'), (1, '#7a3a78')])
    D += rad('glowC', 1250, 560, 700, [(0, '#ffe7f2', .8), (.25, '#f3a8d0', .4), (.6, '#9a4a9a', .15), (1, '#3d1a5a', 0)])
    D += lin('gndC', [(0, '#2a1438'), (.4, '#170a22'), (1, '#07030c')])
    b = '<rect width="1920" height="1080" fill="url(#skyC)"/><rect width="1920" height="1080" fill="url(#glowC)"/>'
    for _ in range(60):
        b += f'<circle cx="{random.randint(700, 1900)}" cy="{random.randint(10, 420)}" r="{random.choice([1.4, 2, 2.6])}" fill="#fff0fa" opacity="{random.uniform(.2, .7):.2f}"/>'
    for _ in range(100):
        b += grass(random.randint(-20, 1940), 760, random.randint(60, 260), random.randint(-40, 40), random.choice(['#24103a', '#2c1444', '#1d0c30']), w=random.randint(6, 12))
    b += '<path d="M0,740 C500,720 1200,760 1920,740 L1920,1080 L0,1080Z" fill="url(#gndC)"/>'
    # fireflies
    for _ in range(26):
        x, y = random.randint(650, 1900), random.randint(120, 860)
        r = random.choice([5, 6, 8])
        b += f'<circle cx="{x}" cy="{y}" r="{r * 4}" fill="#e8ff8a" opacity=".22" filter="url(#b8)"/><circle cx="{x}" cy="{y}" r="{r}" fill="#f8ffd0"/>'
    fo, cov, fd, G = cute_frog('C', 1350, 820, 1.45, rot=-2, pose='sit', far_arm='cheek', rim='#ffe8f4', look=(-14, 19),
                               P=dict(JADE, hi='#a6f0d0', mid='#48b898', lo='#1d6a62'))
    D += fd
    b += fo
    b += larva_grip(G, -62, 46, 500, bend=0.3, head_rot=0, ants=((-60, 3.8, -40), (60, 3.8, 40)), legs='flail', vside=1,
                    light=(-.6, -.8), rim='#fff4fa', wave=True)
    b += cov
    b += pinch(G, 58, 92, (140, 170, 200, 235))
    # '!?' above the frog
    b += ('<g font-family="Fredoka" font-weight="700" fill="#fff6d6" stroke="#160a2e" stroke-width="10" paint-order="stroke">'
          '<text x="1520" y="430" font-size="150" transform="rotate(12 1520 430)">!?</text></g>')
    b += sweat(1050, 500, 1.2, -30) + sweat(1360, 400, 1.0, 20)
    b += spark(1600, 560, 18) + spark(900, 620, 14)
    # mascot: flashlight on the scene, shocked
    torch = ('<g><rect x="34" y="-42" width="34" height="16" rx="4" fill="#d9dde8" stroke="#1d2b1c" stroke-width="3"/>'
             '<path d="M66 -46 L80 -50 L80 -18 L66 -22Z" fill="#f2d27a" stroke="#1d2b1c" stroke-width="3"/></g>')
    b += '<path d="M520,880 L800,640 L900,1060 Z" fill="#fff3c0" opacity=".1" filter="url(#b14)"/>'
    b += mascot(300, 1010, 2.8, mouth='o', look=(7, -1), arms=('M-34 -22 q-14 6 -16 22', 'M38 -22 q10 -4 4 -14'), front=torch, rim='#ffd9ef')
    b += '<circle cx="530" cy="875" r="34" fill="#fff6c8" opacity=".7" filter="url(#b8)"/>'
    b += bang(250, 690, 0.9)
    for _ in range(14):
        b += grass(random.randint(60, 560), 1090, random.randint(50, 110), random.randint(-30, 30), '#07030c', w=9)
    return page('#160a2e', svg(D, b), [('BUG 1', 230, 'y'), ('FROG 0', 230, 'w')], outline='#12061e')


for name, fn in (('A', make_A), ('B', make_B), ('C', make_C)):
    open(os.path.join(HERE, f'{name}.html'), 'w').write(fn())
