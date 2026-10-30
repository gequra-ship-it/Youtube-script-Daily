# Thumbnails A-C v2 for kardashev-scale (guideline 16-6 / 16-8, brief tools/briefs/thumb_art.md; owner feedback on v1:
# "express a powerful civilization in space more intuitively, include a Dyson sphere"). v1 sources in thumb/v1/. Run: python3 make.py
# A  A STAR / IN A CAGE?        intuitive: a huge half-built Dyson shell + swarm, light leaking from inside, beaming power to a planet;
#                               the frog in a helmet rides a tug carrying a new panel (S39 "swallow the light of a star", S41-S42, S40 none found)
# B  ENERGY OF / A WHOLE STAR   homage: 2001: A Space Odyssey opening alignment (moon limb, planet limb, sun rising), the rising sun is
#                               wrapped in a Dyson swarm; frog on the moon (S15-S16 Type Two "total power radiated by its parent star")
# C  ONLY / TYPE 0.7?           intuitive 3 tiers: frog holds a tiny Earth (planet), a huge Dyson swarm (star) and a galaxy behind
#                               (S13 three tiers, S30 Sagan "somewhere around Type zero point seven")
import os, sys, math, random
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', '..', 'tools'))
from thumb_lib import page, svg, lin, rad, spark

INK = '#1d2b1c'; GREEN = '#6aa55a'; DARKG = '#4d8a4a'; BELLY = '#9cc98a'

FILTERS = ''.join(f'<filter id="b{n}" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="{n}"/></filter>' for n in (2, 3, 6, 12, 24, 50))


def P(pts):
    return ' '.join(f'{a:.1f},{b:.1f}' for a, b in pts)


# ---------------- mascot frog (tools/assets/frog.svg body), posable ----------------
def limb(d, w=7.5, wi=3.4, col=GREEN):
    return f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="{w}"/><path d="{d}" fill="none" stroke="{col}" stroke-width="{wi}"/>'


def end_of(d):
    n = [float(v) for v in d.replace('M', ' ').replace('q', ' ').split()]
    return n[0] + n[-2], n[1] + n[-1]


def frog(x, y, s, rot=0, flip=False, look=(0, 0), mouth='O', armL=None, armR=None, legs=None, robe=False, phones=False,
         brows=True, back='', front='', shadow=False):
    sx = -s if flip else s
    g = [f'<g transform="translate({x} {y}) rotate({rot}) scale({sx} {s})" stroke="{INK}" stroke-linejoin="round" stroke-linecap="round">', back]
    if shadow:
        g.append('<ellipse cx="0" cy="6" rx="52" ry="8" fill="#000" opacity=".3" stroke="none"/>')
    for hx, hy, fx, fy, fa in (legs or ((-20, -6, -22, 4, 0), (20, -6, 22, 4, 0))):
        if abs(fx - hx) + abs(fy - hy) > 14:
            g.append(limb(f'M{hx} {hy} L{fx} {fy}', 15, 9))
        g.append(f'<ellipse cx="{fx}" cy="{fy}" rx="16" ry="9" transform="rotate({fa} {fx} {fy})" fill="{DARKG}" stroke-width="3.2"/>')
    g.append(f'<path d="M-34 0 q-6 -64 34 -70 q40 -2 42 62 q0 10 -6 12 q-36 6 -70 -4z" fill="{GREEN}" stroke-width="4"/>')
    g.append(f'<ellipse cx="2" cy="-12" rx="22" ry="20" fill="{BELLY}" stroke="none" opacity=".7"/>')
    g.append('<path d="M-24 -50 q6 -14 18 -16" fill="none" stroke="#b6dea0" stroke-width="3" opacity=".8"/>')
    if robe:     # sand-coloured desert scarf blowing in the wind
        g.append('<path d="M-36 -30 q40 12 80 -2 l2 12 q-42 14 -84 2z" fill="#d9c3a0" stroke-width="3.4"/>')
        g.append('<path d="M-30 -24 q-30 -6 -62 -24 q-10 10 -4 20 q30 14 64 16z" fill="#c9a87a" stroke-width="3.2"/>')
        g.append('<path d="M-60 -38 q-14 -4 -26 -14" fill="none" stroke="#fff3dc" stroke-width="2.2" opacity=".7"/>')
    lx, ly = look
    for ex in (-10, 22):   # big round eyes, small pupils = surprised
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
    if phones:   # big over-ear headphones
        g.append('<path d="M-30 -62 q-2 -50 36 -52 q38 0 40 52" fill="none" stroke-width="11"/><path d="M-30 -62 q-2 -50 36 -52 q38 0 40 52" fill="none" stroke="#3a3f4a" stroke-width="6"/>')
        g.append('<path d="M-20 -100 q20 -16 46 -4" fill="none" stroke="#9aa3b8" stroke-width="2.4"/>')
        for cx_ in (-34, 48):
            g.append(f'<rect x="{cx_ - 9}" y="-78" width="18" height="30" rx="8" fill="#2a2e38" stroke-width="3.2"/><rect x="{cx_ - 5}" y="-74" width="5" height="18" rx="2" fill="#7c86a0" stroke="none"/>')
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


def corner(x, y):
    return x > 1540 and y > 850

def galaxy(cx, cy, rx, ry, rot, rnd):
    o = f'<g transform="translate({cx} {cy}) rotate({rot})">'
    o += f'<ellipse rx="{rx * 1.15}" ry="{ry * 1.25}" fill="#a98cff" opacity=".22" filter="url(#b24)"/>'
    o += f'<ellipse rx="{rx * .8}" ry="{ry * .8}" fill="#7f6be0" opacity=".25" filter="url(#b12)"/>'
    for arm in range(2):
        ph = arm * math.pi
        for i in range(260):
            t = i / 259; r = .08 + .95 * t; a = ph + 3.6 * t + rnd.uniform(-.25, .25)
            rr = r + rnd.uniform(-.05, .05)
            x = rx * rr * math.cos(a); y = ry * rr * math.sin(a)
            col = rnd.choice(['#ffffff', '#cfe0ff', '#a8c4ff', '#ffd9f0', '#e9d8ff'])
            o += f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{rnd.uniform(1, 3.4) * (1.3 - t * .6):.1f}" fill="{col}" opacity="{rnd.uniform(.35, .95) * (1 - t * .5):.2f}"/>'
        pts = [(rx * (.08 + .95 * t) * math.cos(ph + 3.6 * t), ry * (.08 + .95 * t) * math.sin(ph + 3.6 * t)) for t in [k / 40 for k in range(41)]]
        o += f'<polyline points="{P(pts)}" fill="none" stroke="#c9b8ff" stroke-width="{ry * .35:.0f}" opacity=".28" filter="url(#b6)" stroke-linecap="round"/>'
    o += f'<ellipse rx="{rx * .26}" ry="{ry * .34}" fill="#ffe9c0" opacity=".85" filter="url(#b12)"/>'
    o += f'<ellipse rx="{rx * .12}" ry="{ry * .16}" fill="#fffaf0"/>'
    return o + '</g>'



# ============================ shared v2 pieces: star, Dyson shell, Dyson swarm rings, helmet ============================
def mix(c1, c2, t):
    t = max(0, min(1, t))
    a = [int(c1[i:i + 2], 16) for i in (1, 3, 5)]; b = [int(c2[i:i + 2], 16) for i in (1, 3, 5)]
    return '#' + ''.join(f'{round(x + (y - x) * t):02x}' for x, y in zip(a, b))


def star_defs(id, cx, cy, r, halo):
    return (rad(id + 'h', cx, cy, halo, [(0, '#fff3c4', .95), (.18, '#ffc560', .7), (.42, '#ff8a3a', .28), (.7, '#c2406a', .1), (1, '#5a1a60', 0)]) +
            rad(id + 'c', cx - r * .25, cy - r * .25, r * 1.3, [(0, '#ffffff', 1), (.35, '#fff1b8', 1), (.7, '#ffbf55', 1), (1, '#ff7a2a', 1)]))


def star(id, cx, cy, r, halo, rnd):
    o = f'<circle cx="{cx}" cy="{cy}" r="{halo}" fill="url(#{id}h)"/>'
    o += f'<circle cx="{cx}" cy="{cy}" r="{r * 1.08:.0f}" fill="#ffd27a" opacity=".6" filter="url(#b24)"/>'
    o += f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="url(#{id}c)"/>'
    for _ in range(int(r * .9)):        # granulation
        a = rnd.uniform(0, 6.283); d = r * math.sqrt(rnd.uniform(0, .9))
        o += f'<circle cx="{cx + d * math.cos(a):.0f}" cy="{cy + d * math.sin(a):.0f}" r="{rnd.uniform(r * .02, r * .06):.1f}" fill="{rnd.choice(["#ffdf90", "#ff9f45", "#fff6d8"])}" opacity="{rnd.uniform(.15, .4):.2f}"/>'
    for k in range(5):                  # prominences on the limb
        a = rnd.uniform(0, 6.283); x0 = cx + r * math.cos(a); y0 = cy + r * math.sin(a)
        x1 = cx + r * 1.16 * math.cos(a + .08); y1 = cy + r * 1.16 * math.sin(a + .08)
        x2 = cx + r * math.cos(a + .16); y2 = cy + r * math.sin(a + .16)
        o += f'<path d="M{x0:.0f} {y0:.0f} Q{x1:.0f} {y1:.0f} {x2:.0f} {y2:.0f}" fill="none" stroke="#ffb24a" stroke-width="{r * .035:.1f}" opacity=".8"/>'
    return o


def sph(phi, lam, tilt, spin):
    x = math.cos(phi) * math.sin(lam + spin); y = math.sin(phi); z = math.cos(phi) * math.cos(lam + spin)
    t = math.radians(tilt)
    return x, y * math.cos(t) - z * math.sin(t), y * math.sin(t) + z * math.cos(t)


def shell(cx, cy, R, rnd, tilt=22, spin=.3, missing=lambda la, lo: False, holes=.12, dlat=15, dlon=15):
    """Dyson shell of panels. returns (back, front, open_dirs)"""
    back = ''; front = ''; opens = []
    for la in range(-90 + dlat, 90, dlat):
        n = max(6, int(round(360 / dlon * math.cos(math.radians(la)))))
        for j in range(n):
            lo = j * 360 / n; dl = 360 / n
            phi = math.radians(la); lam = math.radians(lo)
            gone = missing(la, lo) or rnd.random() < holes
            c = sph(phi, lam, tilt, spin)
            corners = [sph(math.radians(la + a * dlat * .44), math.radians(lo + b * dl * .44), tilt, spin) for a, b in ((-1, -1), (-1, 1), (1, 1), (1, -1))]
            pts = [(cx + R * p[0], cy - R * p[1]) for p in corners]
            if c[2] < 0:     # back half: inner face lit by the star
                if c[2] > -.05: continue
                back += f'<polygon points="{P(pts)}" fill="{mix("#ff7a30", "#ffc66a", -c[2])}" opacity="{.35 + .5 * -c[2]:.2f}" stroke="#ffe1a0" stroke-width="1.5"/>'
            else:
                if gone:
                    opens.append((c[0], c[1], c[2])); continue
                shade = mix('#15101f', '#4a3c66', .5 + .5 * c[1])
                rim = .25 + .75 * (1 - c[2]) ** 2
                mid = lambda p, q: ((p[0] + q[0]) / 2, (p[1] + q[1]) / 2)
                m1, m2, m3, m4 = mid(pts[0], pts[1]), mid(pts[1], pts[2]), mid(pts[2], pts[3]), mid(pts[3], pts[0])
                front += (f'<polygon points="{P(pts)}" fill="{shade}" stroke="#ffcf7a" stroke-width="{1.4 + 2.6 * rim:.1f}" stroke-opacity="{rim:.2f}"/>'
                          f'<path d="M{m1[0]:.1f} {m1[1]:.1f} L{m3[0]:.1f} {m3[1]:.1f} M{m2[0]:.1f} {m2[1]:.1f} L{m4[0]:.1f} {m4[1]:.1f}" stroke="#7d6aa8" stroke-width="1.2" opacity=".55"/>')
                if c[1] > .35 and c[0] < 0:   # cool reflection of the nebula on the upper-left panels
                    front += f'<polygon points="{P(pts)}" fill="#9fd4ff" opacity="{.18 * c[1]:.2f}"/>'
    return back, front, opens


def collector(x, y, s, ang, front_side, lit=1.0):
    w, h = s, s * .62
    if front_side:
        body = (f'<rect x="{-w / 2:.1f}" y="{-h / 2:.1f}" width="{w:.1f}" height="{h:.1f}" fill="#1b1428" stroke="#ffd27a" stroke-width="{max(1.2, s * .07):.1f}"/>'
                f'<path d="M0 {-h / 2:.1f} V{h / 2:.1f} M{-w / 2:.1f} 0 H{w / 2:.1f}" stroke="#6f5d9a" stroke-width="{max(.8, s * .04):.1f}"/>')
    else:
        body = f'<rect x="{-w / 2:.1f}" y="{-h / 2:.1f}" width="{w:.1f}" height="{h:.1f}" fill="#ffb455" opacity="{.45 + .4 * lit:.2f}" stroke="#ffe7b0" stroke-width="{max(1, s * .05):.1f}"/>'
    return f'<g transform="translate({x:.1f} {y:.1f}) rotate({ang:.1f})">{body}</g>'


def ring(cx, cy, Rr, flat, rot, n, size, rnd, jitter=.06):
    """an orbit of collectors; returns (back, front)"""
    back = ''; front = ''; cr, sr = math.cos(math.radians(rot)), math.sin(math.radians(rot))
    for i in range(n):
        th = 2 * math.pi * i / n + rnd.uniform(-.02, .02)
        rr = Rr * (1 + rnd.uniform(-jitter, jitter))
        x0 = rr * math.cos(th); y0 = rr * math.sin(th) * flat; z = math.sin(th)
        x = cx + x0 * cr - y0 * sr; y = cy + x0 * sr + y0 * cr
        tx, ty = -math.sin(th), math.cos(th) * flat
        ang = math.degrees(math.atan2(tx * sr + ty * cr, tx * cr - ty * sr))
        s = size * (1 + .22 * z) * rnd.uniform(.8, 1.15)
        if z >= 0: front += collector(x, y, s, ang, True)
        else: back += collector(x, y, s, ang, False, -z)
    return back, front


def helmet(cx=6, cy=-62, r=50):
    return (f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="#bfe6ff" fill-opacity=".14" stroke="#e8f6ff" stroke-width="4"/>'
            f'<path d="M{cx - r * .72:.0f} {cy - r * .3:.0f} a{r * .78:.0f} {r * .78:.0f} 0 0 1 {r * .5:.0f} {-r * .55:.0f}" fill="none" stroke="#fff" stroke-width="6" opacity=".75"/>'
            f'<ellipse cx="{cx}" cy="{cy + r * .92:.0f}" rx="{r * .82:.0f}" ry="{r * .2:.0f}" fill="#d9dee8" stroke-width="3.4"/>'
            f'<ellipse cx="{cx}" cy="{cy + r * .88:.0f}" rx="{r * .62:.0f}" ry="{r * .1:.0f}" fill="#9aa4b8" stroke="none"/>')


def ship(x, y, s, ang, trail=120, col='#8fe8ff'):
    return (f'<g transform="translate({x} {y}) rotate({ang}) scale({s})">'
            f'<path d="M-{trail} 0 L-8 -3 L-8 3z" fill="{col}" opacity=".55" filter="url(#b2)"/>'
            f'<path d="M-10 -7 L14 0 L-10 7 L-5 0z" fill="#dfe6f5" stroke="#0a0818" stroke-width="1.6"/><circle cx="-9" cy="0" r="3.4" fill="#fff"/></g>')


def nebula(rnd, n, box, cols, rmin, rmax, op=(.05, .16)):
    x0, y0, x1, y1 = box
    return ''.join(f'<ellipse cx="{rnd.uniform(x0, x1):.0f}" cy="{rnd.uniform(y0, y1):.0f}" rx="{rnd.uniform(rmin, rmax):.0f}" ry="{rnd.uniform(rmin, rmax) * .6:.0f}" '
                   f'fill="{rnd.choice(cols)}" opacity="{rnd.uniform(*op):.2f}" filter="url(#b50)"/>' for _ in range(n))


def shafts(cx, cy, r0, opens, length, n, rnd, w=.11):
    """light beams escaping through the open panels"""
    o = ''
    picks = sorted(opens, key=lambda p: p[2])[:n]
    for (x, y, z) in picks:
        a = math.atan2(-y, x); d = math.hypot(x, y)
        if d < .25: continue
        a0, a1 = a - w / 2, a + w / 2
        p = [(cx + r0 * d * math.cos(a0), cy + r0 * d * math.sin(a0)), (cx + length * math.cos(a0 - .03), cy + length * math.sin(a0 - .03)),
             (cx + length * math.cos(a1 + .03), cy + length * math.sin(a1 + .03)), (cx + r0 * d * math.cos(a1), cy + r0 * d * math.sin(a1))]
        o += f'<polygon points="{P(p)}" fill="url(#shaft)" opacity="{rnd.uniform(.35, .6):.2f}" filter="url(#b6)"/>'
    return o


def shaft_def(cx, cy, length):
    return rad('shaft', cx, cy, length, [(0, '#fff6d0', .9), (.45, '#ffc76a', .45), (1, '#ff8a3a', 0)])


# =========================== A: A STAR IN A CAGE? (intuitive, half-built Dyson shell) ===========================
def make_A():
    rnd = random.Random(11); cx, cy, R = 1385, 505, 365; r = R * .7
    d = FILTERS + star_defs('sa', cx, cy, r, 900) + shaft_def(cx, cy, 900)
    d += lin('skyA', [(0, '#0d0a2a'), (.55, '#1b0f3a'), (1, '#2a0f2e')], 1, 1)
    d += rad('vigA', 960, 540, 1150, [(0, '#000', 0), (.7, '#000', 0), (1, '#000', .55)])
    d += rad('plA', 150, 960, 260, [(0, '#4f8fd0', 1), (.7, '#1d3f7a', 1), (1, '#0a1530', 1)])
    d += lin('beamA', [(0, '#ffe3a0'), (1, '#8fe8ff')], 1, 0)
    b = '<rect width="1920" height="1080" fill="url(#skyA)"/>'
    b += nebula(rnd, 14, (0, 0, 1920, 1080), ['#5a2a9a', '#2a4aa0', '#a03a7a', '#1a6a9a'], 160, 380)
    b += starfield(rnd, 380, (0, 0, 1920, 1080), skip=lambda x, y: math.hypot(x - cx, y - cy) < R * 1.2)
    # power beam to a colonised planet (bottom-left)
    b += '<path d="M1040 690 L300 900" stroke="url(#beamA)" stroke-width="34" opacity=".35" filter="url(#b12)" stroke-linecap="round"/>'
    b += '<path d="M1040 690 L300 900" stroke="url(#beamA)" stroke-width="9" opacity=".9" stroke-linecap="round"/>'
    for k in range(6):
        t = k / 6 + .05; x = 1040 + (300 - 1040) * t; y = 690 + (900 - 690) * t
        b += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="7" fill="#fff" opacity=".85"/>'
    b += '<circle cx="150" cy="980" r="250" fill="#8fd0ff" opacity=".25" filter="url(#b24)"/><circle cx="150" cy="980" r="240" fill="url(#plA)" stroke="#0a0818" stroke-width="4"/>'
    for _ in range(9):
        b += f'<ellipse cx="{rnd.randint(-40, 300)}" cy="{rnd.randint(780, 1080)}" rx="{rnd.randint(30, 80)}" ry="{rnd.randint(14, 30)}" fill="#5aa060" opacity=".75"/>'
    for _ in range(70):   # city lights on the night side
        a = rnd.uniform(1.3, 3.3); dd = 240 * math.sqrt(rnd.uniform(.1, .95))
        b += f'<circle cx="{150 + dd * math.cos(a):.0f}" cy="{980 + dd * math.sin(a) * -1:.0f}" r="{rnd.uniform(1.5, 3.2):.1f}" fill="#ffe08a" opacity=".9"/>'
    b += '<path d="M-90 980 a240 240 0 0 1 400 -178" fill="none" stroke="#bfe8ff" stroke-width="7" opacity=".8"/>'
    # swarm rings outside the shell (back halves)
    r1 = ring(cx, cy, R * 1.24, .26, -14, 66, 30, rnd); r2 = ring(cx, cy, R * 1.18, .5, 32, 56, 24, rnd)
    sh_back, sh_front, opens = shell(cx, cy, R, rnd, tilt=20, spin=.25, holes=.09,
                                     missing=lambda la, lo: (la >= 30 and (lo > 300 or lo < 30)) or (la >= 0 and 320 < lo < 350) or (-15 <= la <= 0 and 330 < lo < 360))
    b += r1[0] + r2[0]
    b += shafts(cx, cy, R, opens, 980, 7, rnd)
    b += sh_back + star('sa', cx, cy, r, 900, rnd) + sh_front
    b += f'<circle cx="{cx}" cy="{cy}" r="{R + 3}" fill="none" stroke="#ffb45a" stroke-width="10" opacity=".45" filter="url(#b6)"/>'
    b += r2[1] + r1[1]
    # construction drones at the open top
    for (x, y, a) in ((1235, 160, 20), (1395, 118, -10), (1520, 190, 40)):
        b += (f'<g transform="translate({x} {y}) rotate({a})"><rect x="-14" y="-9" width="28" height="18" rx="4" fill="#c9d2e6" stroke="#0a0818" stroke-width="2.5"/>'
              f'<path d="M0 9 L0 30" stroke="#0a0818" stroke-width="3"/><circle cx="0" cy="34" r="5" fill="#8fe8ff"/><circle cx="0" cy="34" r="14" fill="#8fe8ff" opacity=".4" filter="url(#b3)"/></g>')
    b += ship(1760, 300, 1.4, 160, 160) + ship(1110, 960, 1.2, -20, 140) + ship(1690, 120, 1.0, 200, 120) + ship(880, 560, 1.1, 10, 130, '#ffd27a')
    # tug with the frog, hauling a new panel towards the shell
    fx, fy = 730, 690
    hexp = P([(fx + 150 + 70 * math.cos(math.radians(60 * k + 30)), fy - 40 + 70 * math.sin(math.radians(60 * k + 30))) for k in range(6)])
    b += f'<path d="M{fx - 40} {fy + 40} L{fx + 110} {fy - 30}" stroke="#c9d2e6" stroke-width="5"/>'
    b += f'<polygon points="{hexp}" fill="#231a36" stroke="#ffd27a" stroke-width="5"/><path d="M{fx + 80} {fy - 40} H{fx + 220} M{fx + 115} {fy - 100} L{fx + 185} {fy + 20} M{fx + 185} {fy - 100} L{fx + 115} {fy + 20}" stroke="#7d6aa8" stroke-width="2.4"/>'
    b += f'<polygon points="{hexp}" fill="#9fd4ff" opacity=".12"/>'
    b += f'<path d="M{fx - 175} {fy + 48} L{fx - 330} {fy + 70} L{fx - 175} {fy + 92}z" fill="#8fe8ff" opacity=".5" filter="url(#b6)"/>'
    b += (f'<path d="M{fx - 175} {fy + 40} q-10 30 0 60 l300 0 q34 -30 0 -60z" fill="#d6dcea" stroke="{INK}" stroke-width="5"/>'
          f'<path d="M{fx - 165} {fy + 84} h290" stroke="#8d96ad" stroke-width="5"/><rect x="{fx - 140}" y="{fy + 50}" width="40" height="22" rx="6" fill="#ffd27a" stroke="{INK}" stroke-width="3"/>'
          f'<circle cx="{fx + 105}" cy="{fy + 70}" r="9" fill="#ff7a6a" stroke="{INK}" stroke-width="3"/>')
    b += frog(fx - 10, fy + 44, 2.05, rot=-4, look=(3, -3), mouth='O', armL='M-34 -22 q-24 -6 -30 -30', armR='M38 -22 q24 -14 30 -34',
              legs=((-20, -6, -26, 2, -10), (20, -6, 26, 2, 10)), front=helmet())
    b += spark(1100, 80, 20) + spark(1820, 560, 18) + spark(620, 420, 14) + spark(980, 330, 12)
    b += '<rect width="1920" height="1080" fill="url(#vigA)"/>'
    lines = [('A STAR', 165, 'w'), ('IN A <span class="g">CAGE?</span>', 165, 'w')]
    return page('#0d0a2a', svg(d, b), lines, outline='#07051a', top=46)


# =========================== B: 2001 alignment, the rising sun is a Dyson swarm ===========================
def make_B():
    rnd = random.Random(23); cx, cy, r = 1420, 470, 215
    d = FILTERS + star_defs('sb', cx, cy, r, 760)
    d += rad('earthB', 1370, 1950, 1220, [(0, '#05070e', 1), (.93, '#0a1226', 1), (.985, '#16407a', 1), (1, '#5fb8ff', 1)])
    d += rad('moonB', 760, 980, 900, [(0, '#c9c6bf', 1), (.6, '#8e8a84', 1), (1, '#3c3a38', 1)])
    d += rad('vigB', 960, 540, 1150, [(0, '#000', 0), (.65, '#000', 0), (1, '#000', .6)])
    d += shaft_def(cx, cy, 1000)
    b = '<rect width="1920" height="1080" fill="#02030a"/>'
    b += starfield(rnd, 260, (0, 0, 1920, 760), col='#dfe8ff')
    # 2001-like long horizontal and vertical flare
    b += f'<ellipse cx="{cx}" cy="{cy}" rx="900" ry="10" fill="#fff0c8" opacity=".55" filter="url(#b6)"/>'
    b += f'<ellipse cx="{cx}" cy="{cy}" rx="10" ry="520" fill="#fff0c8" opacity=".35" filter="url(#b6)"/>'
    for k in range(16):
        a = k * math.pi / 8 + .1
        b += f'<path d="M{cx} {cy} L{cx + 900 * math.cos(a - .025):.0f} {cy + 900 * math.sin(a - .025):.0f} L{cx + 900 * math.cos(a + .025):.0f} {cy + 900 * math.sin(a + .025):.0f}z" fill="url(#shaft)" opacity=".3" filter="url(#b3)"/>'
    rings = [ring(cx, cy, r * 1.3, .22, -12, 60, 30, rnd), ring(cx, cy, r * 1.45, .55, 38, 70, 28, rnd), ring(cx, cy, r * 1.6, .35, -52, 76, 27, rnd),
             ring(cx, cy, r * 1.4, .85, 80, 64, 26, rnd), ring(cx, cy, r * 1.75, .18, 8, 92, 28, rnd), ring(cx, cy, r * 1.22, .7, -20, 56, 26, rnd)]
    b += ''.join(x[0] for x in rings)
    b += star('sb', cx, cy, r, 760, rnd)
    b += ''.join(x[1] for x in rings)
    # planet limb (dark, thin blue atmosphere, city lights)
    b += '<circle cx="1370" cy="1950" r="1228" fill="#7fd0ff" opacity=".5" filter="url(#b12)"/>'
    b += '<circle cx="1370" cy="1950" r="1220" fill="url(#earthB)"/>'
    for _ in range(260):
        x = rnd.uniform(560, 1920); top = 1950 - math.sqrt(max(0, 1220 ** 2 - (x - 1370) ** 2))
        y = rnd.uniform(top + 12, top + 220)
        b += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{rnd.uniform(1.2, 2.8):.1f}" fill="#ffd98a" opacity="{rnd.uniform(.4, .9):.2f}"/>'
    # moon limb in the foreground
    b += '<circle cx="760" cy="2660" r="1760" fill="url(#moonB)" stroke="#e8e4da" stroke-width="5"/>'
    for _ in range(40):
        x = rnd.uniform(-100, 1500); top = 2660 - math.sqrt(max(0, 1760 ** 2 - (x - 760) ** 2))
        y = rnd.uniform(top + 20, 1100); rr = rnd.uniform(10, 46)
        b += f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{rr:.0f}" ry="{rr * .32:.0f}" fill="#5a5753" opacity=".55"/><ellipse cx="{x:.0f}" cy="{y - rr * .06:.0f}" rx="{rr * .8:.0f}" ry="{rr * .22:.0f}" fill="#d8d4cb" opacity=".25"/>'
    b += '<rect x="1540" y="850" width="380" height="230" fill="#000" opacity="0"/>'
    fx, fy = 520, 1000
    b += frog(fx, fy, 2.35, look=(4, -4), mouth='O', armL='M-34 -22 q-22 -10 -26 -36', armR='M38 -22 q26 -4 34 -30', shadow=True, front=helmet())
    b += spark(980, 160, 18) + spark(1780, 220, 16) + spark(620, 560, 12)
    b += '<rect width="1920" height="1080" fill="url(#vigB)"/>'
    lines = [('ENERGY OF', 125, 'w'), ('A WHOLE', 125, 'w'), ('<span class="g">STAR</span>', 170, 'w')]
    return page('#02030a', svg(d, b), lines, outline='#02030a', top=44)


# =========================== C: planet < star < galaxy (intuitive scale) ===========================
def make_C():
    rnd = random.Random(37); cx, cy, r = 1170, 585, 175
    d = FILTERS + star_defs('sc', cx, cy, r, 700) + shaft_def(cx, cy, 800)
    d += lin('skyC', [(0, '#0a1430'), (.6, '#160f38'), (1, '#0b0a20')], 1, 1)
    d += '<radialGradient id="eC" cx=".35" cy=".35" r=".75"><stop offset="0" stop-color="#7fc4ff"/><stop offset=".6" stop-color="#2a6ab8"/><stop offset="1" stop-color="#0b2350"/></radialGradient>'
    d += rad('vigC', 960, 540, 1150, [(0, '#000', 0), (.7, '#000', 0), (1, '#000', .55)])
    b = '<rect width="1920" height="1080" fill="url(#skyC)"/>'
    b += nebula(rnd, 10, (600, 0, 1920, 900), ['#5a3aa0', '#2a5ab0', '#8a3a8a'], 180, 400)
    b += starfield(rnd, 360, (0, 0, 1920, 1080))
    b += '<g opacity="1">' + galaxy(1500, 300, 640, 230, -12, rnd) + galaxy(1500, 300, 600, 215, -12, rnd).replace('<g transform', '<g opacity=".6" transform') + '</g>'
    b += '<circle cx="1500" cy="300" r="120" fill="#fff2d8" opacity=".5" filter="url(#b24)"/>'
    rings = [ring(cx, cy, r * 1.4, .28, -16, 50, 22, rnd), ring(cx, cy, r * 1.65, .6, 30, 60, 22, rnd), ring(cx, cy, r * 1.9, .38, -48, 66, 21, rnd),
             ring(cx, cy, r * 1.55, .9, 76, 54, 19, rnd), ring(cx, cy, r * 2.2, .2, 4, 84, 22, rnd)]
    sh_back, sh_front, opens = shell(cx, cy, r * 1.18, rnd, tilt=25, spin=.6, holes=.35, dlat=20, dlon=20,
                                     missing=lambda la, lo: la > 20)
    b += ''.join(x[0] for x in rings)
    b += shafts(cx, cy, r * 1.18, opens, 800, 6, rnd)
    b += sh_back + star('sc', cx, cy, r, 700, rnd) + sh_front
    b += ''.join(x[1] for x in rings)
    b += ship(1640, 760, 1.2, 200, 150) + ship(900, 300, 1.0, -30, 120) + ship(1720, 200, .9, 160, 110, '#ffd27a')
    # frog floating in a helmet, holding a tiny Earth
    fx, fy = 560, 955
    b += f'<circle cx="{fx + 5}" cy="{fy - 70}" r="150" fill="#7fc4ff" opacity=".18" filter="url(#b24)"/>'
    b += frog(fx, fy, 2.3, rot=8, look=(5, -5), mouth='O', armL='M-34 -22 q-6 -24 8 -30', armR='M38 -22 q30 -10 40 -30',
              legs=((-20, -6, -34, 10, -30), (20, -6, 34, 12, 30)), front=helmet())
    ex, ey, er = fx + 170, fy - 120, 58
    b += (f'<circle cx="{ex}" cy="{ey}" r="{er + 10}" fill="#9fe0ff" opacity=".45" filter="url(#b6)"/>'
          f'<circle cx="{ex}" cy="{ey}" r="{er}" fill="url(#eC)" stroke="{INK}" stroke-width="4"/>'
          f'<path d="M{ex - 36} {ey - 18} q14 -16 30 -6 q8 14 -8 22 q-16 4 -22 -16z M{ex + 6} {ey + 14} q18 -10 30 4 q-4 20 -22 18z" fill="#5aa060" stroke="{INK}" stroke-width="2"/>'
          f'<path d="M{ex - 30} {ey - 30} a40 40 0 0 1 26 -14" fill="none" stroke="#fff" stroke-width="4" opacity=".7"/>')
    b += spark(1000, 120, 18) + spark(1850, 420, 16) + spark(760, 620, 14) + spark(320, 640, 12)
    b += '<rect width="1920" height="1080" fill="url(#vigC)"/>'
    lines = [('ONLY', 150, 'w'), ('TYPE <span class="g">0.7?</span>', 185, 'w')]
    return page('#0a1430', svg(d, b), lines, outline='#060a1c', top=46)


for n, fn in (('A', make_A), ('B', make_B), ('C', make_C)):
    open(os.path.join(HERE, f'{n}.html'), 'w').write(fn())
print('ok')
