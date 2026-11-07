# Shorts thumbnails for deep-sea-giants, VERTICAL 1080x1920 (guideline 16-9 as corrected 2026-11-06: centred text in the middle, picture above and below).
# ONE file writes all five:  python3 videos/deep-sea-giants-short1/thumb/make.py  -> videos/deep-sea-giants-short{1..5}/thumb/A.html
# Helpers (frog, isopod, tentacle) copied from videos/deep-sea-giants/thumb/make.py (long-form, not edited).
# 1  40 CM / PILLBUG       pendant lamp above; giant isopod curled in a cat bed below, frog dangling a feather toy. short1: "about forty centimeters long ... roughly the size of a house cat"
# 2  EYES LIKE / PLATES    squid eye as a china dinner plate between fork and knife above; sperm whale shadow below, frog with bib. short2: "a large dinner plate"; "shadow of a hunting sperm whale"
# 3  MEALS / MONTHS / APART  whale fall sinking above; lone isopod waiting on the mud, frog with hourglass below. short3: "meals come months, or even years, apart"; "a whale fall"
# 4  WHY NOT / CRUSHED?    submarine crumpled like a soda can above; calm unharmed fish below. short4: "crumple like an empty soda can"; "without being crushed"
# 5  TINY / OR / GIANT?    tiny abyssal snail under the frog's magnifier above; towering giant isopod below. short5: giant isopods vs "deep-sea dwarfism ... abyssal snails"
import os, sys, math, random
HERE = os.path.dirname(os.path.abspath(__file__))
VID = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(VID, '..', 'tools'))
from thumb_lib import vpage, vsvg, lin, rad, spark

INK = '#1d2b1c'; GREEN = '#6aa55a'; DARKG = '#4d8a4a'; BELLY = '#9cc98a'
FILTERS = ''.join(f'<filter id="b{n}" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="{n}"/></filter>' for n in (3, 6, 12, 24, 50))


def P(pts):
    return ' '.join(f'{a:.1f},{b:.1f}' for a, b in pts)


def limb(d, w=7.5, wi=3.4):
    return f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="{w}"/><path d="{d}" fill="none" stroke="{GREEN}" stroke-width="{wi}"/>'


def end_of(d):
    n = [float(v) for v in d.replace('M', ' ').replace('q', ' ').split()]
    return n[0] + n[-2], n[1] + n[-1]


def frog(x, y, s, rot=0, flip=False, look=(0, 0), mouth='O', armL=None, armR=None, legs=None, helmet=False,
         brows=True, back="", front="", shadow=False, mid=""):
    sx = -s if flip else s
    g = [f'<g transform="translate({x} {y}) rotate({rot}) scale({sx} {s})" stroke="{INK}" stroke-linejoin="round" stroke-linecap="round">', back]
    if shadow:
        g.append('<ellipse cx="0" cy="8" rx="50" ry="8" fill="#000" opacity=".25" stroke="none"/>')
    if helmet:
        g.append('<rect x="-50" y="-58" width="20" height="42" rx="7" fill="#c9ced8" stroke-width="3"/><rect x="-46" y="-52" width="5" height="30" rx="2" fill="#fff" stroke="none" opacity=".6"/>')
    for hx, hy, fx, fy, fa in (legs or ((-20, -6, -22, 4, 0), (20, -6, 22, 4, 0))):
        if abs(fx - hx) + abs(fy - hy) > 14:
            g.append(limb(f'M{hx} {hy} L{fx} {fy}', 15, 9))
        g.append(f'<ellipse cx="{fx}" cy="{fy}" rx="16" ry="9" transform="rotate({fa} {fx} {fy})" fill="{DARKG}" stroke-width="3.2"/>')
    g.append(f'<path d="M-34 0 q-6 -64 34 -70 q40 -2 42 62 q0 10 -6 12 q-36 6 -70 -4z" fill="{GREEN}" stroke-width="4"/>')
    g.append(f'<ellipse cx="2" cy="-12" rx="22" ry="20" fill="{BELLY}" stroke="none" opacity=".7"/>')
    g.append('<path d="M-24 -50 q6 -14 18 -16" fill="none" stroke="#b6dea0" stroke-width="3" opacity=".8"/>')
    lx, ly = look
    # pupil must stay fully inside the white (eye r 13.5, pupil r 4.4): clamp the offset (miya 2026-11-07, small Shorts screens)
    _ox, _oy = 1 + lx, ly; _m = math.hypot(_ox, _oy)
    if _m > 7.5: _ox, _oy = _ox * 7.5 / _m, _oy * 7.5 / _m
    lx, ly = _ox - 1, _oy
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
    g.append(mid)
    if helmet:
        g.append('<circle cx="6" cy="-58" r="45" fill="#bfe6ff" fill-opacity=".13" stroke="#e8f6ff" stroke-width="3.4" stroke-opacity=".95"/>')
        g.append('<path d="M-26 -82 q12 -18 32 -21" fill="none" stroke="#fff" stroke-width="5" opacity=".8"/><path d="M42 -40 q6 -10 6 -22" fill="none" stroke="#fff" stroke-width="3" opacity=".5"/>')
        g.append('<ellipse cx="6" cy="-16" rx="40" ry="9" fill="#d3d9e3" stroke-width="3.2"/><path d="M-30 -18 q36 8 72 0" fill="none" stroke="#fff" stroke-width="2.2" opacity=".8"/>')
    for a in (armL or 'M-34 -22 q-14 6 -16 22', armR or 'M38 -22 q14 6 16 22'):
        g.append(limb(a)); ex_, ey_ = end_of(a)
        g.append(f'<circle cx="{ex_:.1f}" cy="{ey_:.1f}" r="5.6" fill="{GREEN}" stroke-width="3"/>')
    g.append(front); g.append('</g>')
    return ''.join(g)


def hand_at(x, y, s, arm, flip=False):
    ex, ey = end_of(arm)
    return (x - ex * s, y + ey * s) if flip else (x + ex * s, y + ey * s)


def bez(p, t):
    (x0, y0), (x1, y1), (x2, y2), (x3, y3) = p; u = 1 - t
    return (u ** 3 * x0 + 3 * u * u * t * x1 + 3 * u * t * t * x2 + t ** 3 * x3,
            u ** 3 * y0 + 3 * u * u * t * y1 + 3 * u * t * t * y2 + t ** 3 * y3)


def tentacle(p, w0, w1, col, dark, lite, suck='#f3d9c4', n=46, side=1, sk=True):
    C = [bez(p, i / n) for i in range(n + 1)]
    L, R, N, W = [], [], [], []
    for i, (x, y) in enumerate(C):
        a = C[max(i - 1, 0)]; b = C[min(i + 1, n)]
        dx, dy = b[0] - a[0], b[1] - a[1]; l = math.hypot(dx, dy) or 1
        nx, ny = -dy / l, dx / l; w = w0 + (w1 - w0) * (i / n) ** .8
        L.append((x + nx * w, y + ny * w)); R.append((x - nx * w, y - ny * w)); N.append((nx, ny)); W.append(w)
    o = f'<path d="M{P(L)} L{P(R[::-1])}Z" fill="{col}" stroke="{dark}" stroke-width="5" stroke-linejoin="round"/>'
    hi = [(x - nx * w * .45 * side, y - ny * w * .45 * side) for (x, y), (nx, ny), w in zip(C, N, W)]
    o += f'<polyline points="{P(hi[:-3])}" fill="none" stroke="{lite}" stroke-width="{max(3, w0 * .28):.0f}" stroke-linecap="round" opacity=".7"/>'
    if sk:
        for i in range(3, n - 2, 2):
            (x, y), (nx, ny), w = C[i], N[i], W[i]
            r = max(2.5, w * .32); sx, sy = x + nx * w * .62 * side, y + ny * w * .62 * side
            o += f'<circle cx="{sx:.1f}" cy="{sy:.1f}" r="{r:.1f}" fill="{suck}" stroke="{dark}" stroke-width="{max(1.5, r * .35):.1f}"/>'
    return o


def isopod(cx, yb, L, H, rnd, grad='isoG', ants=None, legs_near=True, shadow=True):
    """side-view giant isopod, head on the left (from the long-form make.py, antennae configurable)"""
    x0, x1 = cx - L, cx + L
    k_ = L / 500

    def top(x):
        u = max(0.0, 1 - ((x - cx) / L) ** 2)
        return yb - H * u ** .55

    o = ''
    if shadow:
        o += f'<ellipse cx="{cx}" cy="{yb + 95 * k_:.0f}" rx="{L * 1.02:.0f}" ry="{40 * k_:.0f}" fill="#020c10" opacity=".55" filter="url(#b12)"/>'
    for k in range(7):
        lx = x0 + (150 + k * 95) * k_
        o += f'<path d="M{lx:.0f} {yb} l{-18 * k_:.0f} {50 * k_:.0f} l{-26 * k_:.0f} {40 * k_:.0f}" fill="none" stroke="#3c2a3c" stroke-width="{16 * k_:.0f}" stroke-linecap="round" stroke-linejoin="round"/>'
    e0 = x0 + 95 * k_
    edges = [e0] + [e0 + 96 * k_ * k for k in range(1, 8)] + [e0 + 96 * k_ * 7 + 30 * k_ * k for k in range(1, 5)]
    segs = list(zip(edges[:-1], edges[1:]))
    tx = edges[-1]
    o += f'<path d="M{tx - 10} {top(tx) - 6:.0f} Q{x1 - 20} {top(x1 - 60 * k_):.0f} {x1 + 30 * k_:.0f} {yb + 10} Q{x1 - 60 * k_:.0f} {yb + 40 * k_:.0f} {tx - 10} {yb + 30 * k_:.0f} Z" fill="url(#{grad})" stroke="#2c1a2c" stroke-width="6"/>'
    o += f'<path d="M{x1 - 40 * k_:.0f} {yb + 10} q{60 * k_:.0f} {10 * k_:.0f} {90 * k_:.0f} {50 * k_:.0f} q{-50 * k_:.0f} 0 {-100 * k_:.0f} {-28 * k_:.0f}z" fill="#a98ea2" stroke="#2c1a2c" stroke-width="5"/>'
    for a, bx in reversed(segs):
        pts = [(x, top(x) - 4) for x in [a + (bx + 16 * k_ - a) * i / 12 for i in range(13)]]
        e = bx + 16 * k_
        path = f'M{a:.0f} {yb + 34 * k_:.0f} L{a:.0f} {top(a):.0f} ' + ' '.join(f'L{x:.0f} {y:.0f}' for x, y in pts) + f' Q{e + 8:.0f} {(top(e) + yb) / 2:.0f} {e:.0f} {yb + 40 * k_:.0f} L{e - 10:.0f} {yb + 58 * k_:.0f} Z'
        o += f'<path d="{path}" fill="url(#{grad})" stroke="#2c1a2c" stroke-width="6" stroke-linejoin="round"/>'
        o += f'<path d="M{e - 4:.0f} {top(e) + 4:.0f} Q{e + 4:.0f} {(top(e) + yb) / 2:.0f} {e - 4:.0f} {yb + 30 * k_:.0f}" fill="none" stroke="#fbf0f4" stroke-width="5" opacity=".55"/>'
        o += f'<path d="M{a + 6:.0f} {top(a + 6) + 6:.0f} ' + ' '.join(f'L{x:.0f} {y + 6:.0f}' for x, y in pts[1:-2]) + '" fill="none" stroke="#ffffff" stroke-width="7" opacity=".7" stroke-linecap="round"/>'
        mx = (a + bx) / 2
        o += f'<ellipse cx="{mx:.0f}" cy="{top(mx) + 40 * k_:.0f}" rx="{(bx - a) * .28:.0f}" ry="{14 * k_:.0f}" fill="#ffffff" opacity=".45"/>'
        for _ in range(int((bx - a) / 6)):
            px = rnd.uniform(a + 8, bx - 4); py = rnd.uniform(top(px) + 30 * k_, yb + 20 * k_)
            o += f'<circle cx="{px:.0f}" cy="{py:.0f}" r="{rnd.uniform(1.5, 3.5):.1f}" fill="#6a4e66" opacity=".35"/>'
    hx = e0; ht = top(hx) + 60 * k_
    o += (f'<path d="M{hx + 20 * k_:.0f} {ht:.0f} Q{x0 + 10 * k_:.0f} {ht - 6:.0f} {x0 - 20 * k_:.0f} {yb - 20 * k_:.0f} Q{x0 - 26 * k_:.0f} {yb + 34 * k_:.0f} {x0 + 30 * k_:.0f} {yb + 42 * k_:.0f} L{hx + 20 * k_:.0f} {yb + 42 * k_:.0f} Z" '
          f'fill="url(#{grad})" stroke="#2c1a2c" stroke-width="6"/>')
    o += f'<path d="M{x0 - 4:.0f} {yb - 40 * k_:.0f} Q{x0 + 20 * k_:.0f} {ht + 8:.0f} {hx + 10:.0f} {ht + 8:.0f}" fill="none" stroke="#ffffff" stroke-width="6" opacity=".6"/>'
    ex, ey = x0 + 46 * k_, yb - 30 * k_
    o += f'<ellipse cx="{ex:.0f}" cy="{ey:.0f}" rx="{40 * k_:.0f}" ry="{30 * k_:.0f}" fill="#1e1c26" stroke="#120c14" stroke-width="5" transform="rotate(-15 {ex:.0f} {ey:.0f})"/>'
    for i in range(-4, 5):
        for j in range(-3, 4):
            px = ex + (i * 9 + (j % 2) * 4.5) * k_; py = ey + j * 8 * k_
            if ((px - ex) / (36 * k_)) ** 2 + ((py - ey) / (26 * k_)) ** 2 < 1:
                o += f'<circle cx="{px:.0f}" cy="{py:.0f}" r="{3 * k_:.1f}" fill="#9fc0cc" opacity=".4"/>'
    o += f'<ellipse cx="{ex - 12 * k_:.0f}" cy="{ey - 10 * k_:.0f}" rx="{12 * k_:.0f}" ry="{7 * k_:.0f}" fill="#ffffff" opacity=".9" transform="rotate(-15 {ex - 12 * k_:.0f} {ey - 10 * k_:.0f})"/>'
    for dpath, w in (ants or ((f'M{x0 - 15} {yb + 5} C{x0 - 110 * k_} {yb - 90 * k_} {x0 - 190 * k_} {yb - 40 * k_} {x0 - 225 * k_} {yb + 50 * k_}', 13),
                              (f'M{x0 - 10} {yb + 25} C{x0 - 80 * k_} {yb + 20} {x0 - 120 * k_} {yb + 80 * k_} {x0 - 110 * k_} {yb + 130 * k_}', 11))):
        o += f'<path d="{dpath}" fill="none" stroke="#2c1a2c" stroke-width="{w}" stroke-linecap="round"/>'
        o += f'<path d="{dpath}" fill="none" stroke="#c7aabb" stroke-width="{w - 6}" stroke-dasharray="16 4" stroke-linecap="round"/>'
    if legs_near:
        for k in range(7):
            lx = x0 + (130 + k * 95) * k_
            d_ = f'M{lx:.0f} {yb + 30 * k_:.0f} l{(-10 + k * 2) * k_:.0f} {46 * k_:.0f} l{-30 * k_:.0f} {40 * k_:.0f}'
            o += f'<path d="{d_}" fill="none" stroke="#2c1a2c" stroke-width="{20 * k_:.0f}" stroke-linecap="round" stroke-linejoin="round"/>'
            o += f'<path d="{d_}" fill="none" stroke="#b497a8" stroke-width="{10 * k_:.0f}" stroke-linecap="round" stroke-linejoin="round"/>'
    return o


def snow(rnd, n, x0, x1, y0, y1, o0=.1, o1=.6, col='#eafff8'):
    return ''.join(f'<circle cx="{rnd.uniform(x0, x1):.0f}" cy="{rnd.uniform(y0, y1):.0f}" r="{rnd.choice([1.4, 2, 2.8, 3.6])}" fill="{col}" opacity="{rnd.uniform(o0, o1):.2f}"/>' for _ in range(n))


def seabed(rnd, y, c0, c1, id_):
    d = lin(id_, [(0, c0), (1, c1)])
    b = f'<path d="M0 {y} Q480 {y - 30} 960 {y - 5} Q1440 {y + 15} 1920 {y - 15} L1920 1080 L0 1080Z" fill="url(#{id_})"/>'
    for _ in range(110):
        b += f'<ellipse cx="{rnd.uniform(0, 1920):.0f}" cy="{rnd.uniform(y + 10, 1080):.0f}" rx="{rnd.uniform(3, 14):.0f}" ry="{rnd.uniform(2, 6):.0f}" fill="#050f14" opacity="{rnd.uniform(.2, .5):.2f}"/>'
    return d, b


ISO_GRAD = lin('isoG', [(0, '#fbeef0'), (.3, '#e2c3cc'), (.7, '#a87f95'), (1, '#4e3049')])


def fork(x, y0, y1, s=1):
    o = f'<g transform="translate({x} {y0}) scale({s})" stroke="#1c2430" stroke-width="5" stroke-linejoin="round">'
    o += '<path d="M-44 0 L-44 120 Q-44 180 -14 196 L-12 470 Q0 488 12 470 L14 196 Q44 180 44 120 L44 0 L32 0 L30 120 L16 120 L14 0 L6 0 L4 120 L-4 120 L-6 0 L-14 0 L-16 120 L-30 120 L-32 0 Z" fill="url(#steel)"/>'
    o += '<path d="M-36 130 Q-30 170 -8 186 L-6 440" fill="none" stroke="#ffffff" stroke-width="6" opacity=".7"/>'
    return o + '</g>'

def knife(x, y0, s=1):
    o = f'<g transform="translate({x} {y0}) scale({s})" stroke="#1c2430" stroke-width="5" stroke-linejoin="round">'
    o += '<path d="M-10 0 Q36 30 34 250 L34 270 L-22 270 L-22 20 Q-22 0 -10 0Z" fill="url(#steel)"/>'
    o += '<path d="M-14 30 L-14 250" fill="none" stroke="#ffffff" stroke-width="6" opacity=".75"/>'
    for k in range(9):
        o += f'<path d="M30 {60 + k * 20} l6 6" stroke-width="2.4"/>'
    o += '<rect x="-26" y="270" width="64" height="20" rx="6" fill="#c8ced8"/>'
    o += '<path d="M-24 290 L36 290 L32 500 Q6 520 -20 500 Z" fill="#3a2a22"/><circle cx="6" cy="340" r="7" fill="#d8dde6"/><circle cx="6" cy="450" r="7" fill="#d8dde6"/>'
    o += '<path d="M-12 300 L-10 490" fill="none" stroke="#8a6a52" stroke-width="5"/>'
    return o + '</g>'

def sperm_whale(x, y, s, col, rim):
    return (f'<g transform="translate({x} {y}) scale({s})">'
            f'<path d="M-160 -40 Q-170 -60 -120 -62 L40 -58 Q120 -50 170 -10 Q200 10 230 14 L262 -14 Q256 14 266 40 L232 22 Q190 36 130 40 Q20 50 -110 40 Q-170 34 -168 0 Z" fill="{col}"/>'
            f'<path d="M-158 -42 Q-120 -64 40 -58 Q120 -50 170 -10" fill="none" stroke="{rim}" stroke-width="5" opacity=".9"/>'
            f'<path d="M-150 34 L-40 36" stroke="{rim}" stroke-width="4" opacity=".5"/><path d="M-40 34 q20 40 50 46 q-10 -30 -10 -44" fill="{col}"/>'
            f'<circle cx="-70" cy="10" r="5" fill="{rim}" opacity=".7"/></g>')

def whale(x, y, s, rot):
    o = f'<g transform="translate({x} {y}) rotate({rot}) scale({s})" stroke="#0c1a26" stroke-width="6" stroke-linejoin="round">'
    body = 'M0 0 Q-10 -70 80 -100 Q260 -150 470 -110 Q620 -80 720 -30 Q770 -10 800 -14 L810 6 Q760 20 700 40 Q560 100 380 110 Q160 120 60 80 Q0 56 0 0Z'
    o += f'<path d="M790 -6 Q840 -80 900 -90 Q870 -40 830 0 Q880 50 920 70 Q850 70 790 14Z" fill="url(#whaleG)"/>'
    o += f'<path d="{body}" fill="url(#whaleG)"/>'
    # ventral pleats (lit belly side)
    o += '<path d="M40 60 Q200 112 420 96" fill="none" stroke="#a9c4d8" stroke-width="5" opacity=".7"/>'
    for k in range(6):
        o += f'<path d="M{50 + k * 6} {40 + k * 8} Q{220} {98 + k * 4} {430 - k * 20} {80 + k * 2}" fill="none" stroke="#c8dcea" stroke-width="3" opacity=".45"/>'
    # back highlight from the light above
    o += '<path d="M30 -50 Q140 -132 470 -106 Q620 -80 720 -30" fill="none" stroke="#eaf8ff" stroke-width="12" opacity=".75" stroke-linecap="round"/>'
    # pectoral fin
    o += '<path d="M220 70 Q260 170 330 200 Q330 140 280 74Z" fill="#7a96ac"/>'
    # closed eye and mouth line
    o += '<path d="M120 10 q14 8 28 0" fill="none" stroke-width="5"/>'
    o += '<path d="M10 30 Q80 50 150 30" fill="none" stroke-width="4" opacity=".7"/>'
    # barnacles
    for bx, by in ((60, -60), (90, -78), (130, -90), (40, -34)):
        o += f'<circle cx="{bx}" cy="{by}" r="9" fill="#d8dcd0" stroke-width="3"/>'
    return o + '</g>'

def hourglass(x, y, s):
    o = f'<g transform="translate({x} {y}) scale({s})" stroke="#1c1208" stroke-width="5" stroke-linejoin="round">'
    o += '<rect x="-70" y="-180" width="140" height="22" rx="8" fill="#a8743a"/><rect x="-70" y="-6" width="140" height="22" rx="8" fill="#a8743a"/>'
    o += '<path d="M-56 -158 L-56 -150 Q-56 -110 -10 -86 Q-10 -80 -10 -78 Q-56 -54 -56 -14 L-56 -6 L56 -6 L56 -14 Q56 -54 10 -78 Q10 -80 10 -86 Q56 -110 56 -150 L56 -158Z" fill="#cfefff" fill-opacity=".25"/>'
    o += '<path d="M-20 -110 Q0 -102 20 -110 Q10 -92 0 -86 Q-10 -92 -20 -110Z" fill="#f2d27a" stroke="none"/>'   # a little sand left on top
    o += '<path d="M-52 -8 Q-40 -56 0 -60 Q40 -56 52 -8Z" fill="#f2d27a" stroke="none"/>'
    o += '<path d="M0 -86 L0 -60" stroke="#f2d27a" stroke-width="3"/>'
    o += '<path d="M-44 -146 Q-44 -116 -16 -96" fill="none" stroke="#ffffff" stroke-width="5" opacity=".7"/>'
    for xx in (-62, 62):
        o += f'<rect x="{xx - 6}" y="-160" width="12" height="156" rx="5" fill="#7a4e22"/>'
    return o + '</g>'

def amphipod(x, y, s, rot):
    o = f'<g transform="translate({x} {y}) rotate({rot}) scale({s})" stroke="#3a1a10" stroke-width="2">'
    o += '<path d="M0 0 Q10 -14 30 -12 Q46 -8 50 6 Q36 2 26 6 Q12 10 0 0Z" fill="#f0a070"/>'
    o += '<path d="M2 -2 q-10 -12 -18 -10 M4 -4 q-6 -16 -14 -18" fill="none"/>'
    o += '<path d="M14 4 l-2 8 M22 4 l-1 8 M30 4 l0 8" fill="none"/>'
    return o + '</g>'

def crushed_sub(rnd):
    """yellow submarine (round nose left, tail fins right) crumpled in the middle like a soda can, centred ~ (1250, 600)"""
    cx, cy, L, R = 1250, 600, 400, 150

    def prof(x):   # half-height of an intact hull at x
        u = (x - cx) / L
        if u < -.75: return R * math.sqrt(max(0, 1 - ((u + .75) / .25) ** 2))
        if u > .35: return R * max(.18, 1 - ((u - .35) / .65) ** 1.4 * .82)
        return R

    def squeeze(x):  # crumple strength along the hull
        return math.exp(-((x - cx + 10) / 150) ** 2)

    xs = [cx - L + i * (2 * L) / 80 for i in range(81)]
    topP, botP = [], []
    for i, x in enumerate(xs):
        h = prof(x); q = squeeze(x)
        zz = (1 if i % 2 else -1) * 22 * q
        topP.append((x + rnd.uniform(-6, 6) * q, cy - h * (1 - .42 * q) + zz + rnd.uniform(-4, 4) * q))
        botP.append((x + rnd.uniform(-6, 6) * q, cy + h * (1 - .36 * q) - zz * .8 + rnd.uniform(-4, 4) * q))
    hull = f'M{P(topP)} L{P(botP[::-1])}Z'
    o = f'<ellipse cx="{cx}" cy="{cy + 250}" rx="430" ry="40" fill="#000" opacity=".45" filter="url(#b12)"/>'
    # tail fins (behind) + bent propeller
    tx = cx + L - 20
    o += f'<path d="M{tx - 70} {cy - 20} L{tx + 10} {cy - 120} L{tx + 40} {cy - 116} L{tx + 20} {cy - 10}Z" fill="#e8a428" stroke="#2a1c06" stroke-width="6"/>'
    o += f'<path d="M{tx - 70} {cy + 20} L{tx + 20} {cy + 112} L{tx + 46} {cy + 104} L{tx + 20} {cy + 10}Z" fill="#c88a1c" stroke="#2a1c06" stroke-width="6"/>'
    o += f'<rect x="{tx + 6}" y="{cy - 12}" width="40" height="24" rx="6" fill="#888" stroke="#2a1c06" stroke-width="5"/>'
    o += (f'<g transform="translate({tx + 54} {cy}) rotate(14)"><path d="M0 0 Q30 -70 6 -96 Q-14 -60 0 0Z M0 0 Q36 60 10 92 Q-12 50 0 0Z" fill="#b0b6c0" stroke="#2a1c06" stroke-width="5"/>'
          '<circle r="12" fill="#6c7888" stroke="#2a1c06" stroke-width="4"/></g>')
    # sail tower (bent over) with a soda-can ring pull on the hatch
    sx = cx + 120
    o += (f'<g transform="rotate(-16 {sx} {cy - 90})"><path d="M{sx - 80} {cy - 70} L{sx - 60} {cy - 190} Q{sx} {cy - 210} {sx + 60} {cy - 190} L{sx + 80} {cy - 70}Z" fill="url(#subG)" stroke="#2a1c06" stroke-width="6" stroke-linejoin="round"/>'
          f'<path d="M{sx - 58} {cy - 180} Q{sx} {cy - 198} {sx + 40} {cy - 186}" fill="none" stroke="#fff4c0" stroke-width="8" opacity=".8" stroke-linecap="round"/>'
          f'<path d="M{sx - 66} {cy - 120} l26 18 l-12 22 l28 14" fill="none" stroke="#7a5208" stroke-width="4"/>'
          f'<ellipse cx="{sx}" cy="{cy - 202}" rx="52" ry="12" fill="#c8ced8" stroke="#2a1c06" stroke-width="5"/>'
          f'<g transform="translate({sx + 6} {cy - 210}) rotate(-24)"><path d="M-18 -10 Q-30 -42 0 -48 Q30 -42 18 -10 Q30 6 0 10 Q-30 6 -18 -10Z" fill="#dfe4ec" stroke="#2a1c06" stroke-width="5"/>'
          '<ellipse cx="0" cy="-26" rx="10" ry="9" fill="#0c1a26" stroke="#2a1c06" stroke-width="3"/><path d="M-12 -40 Q0 -46 12 -40" fill="none" stroke="#fff" stroke-width="3"/></g></g>')
    o += f'<path d="{hull}" fill="url(#subG)" stroke="#2a1c06" stroke-width="7" stroke-linejoin="round"/>'
    # vertical crumple folds in the squeezed middle (dark fold + lit edge), like a crushed can
    for k in range(11):
        x = cx - 190 + k * 36
        q = squeeze(x)
        if q < .25: continue
        h0 = prof(x) * (1 - .42 * q) - 6; h1 = prof(x) * (1 - .36 * q) - 6
        zz = [(x + (12 if j % 2 else -12) * q + rnd.uniform(-4, 4), cy - h0 + j * (h0 + h1) / 6) for j in range(7)]
        o += f'<polyline points="{P(zz)}" fill="none" stroke="#7a5208" stroke-width="6" opacity=".75" stroke-linejoin="round"/>'
        o += f'<polyline points="{P([(a + 8, b) for a, b in zz])}" fill="none" stroke="#fff0a8" stroke-width="4" opacity=".75" stroke-linejoin="round"/>'
    # intact-looking ends: highlights, panel lines, rivets
    o += f'<path d="M{cx - L + 30} {cy - 60} Q{cx - L + 80} {cy - R + 14} {cx - 210} {cy - R + 16}" fill="none" stroke="#fff4c0" stroke-width="12" opacity=".8" stroke-linecap="round"/>'
    o += f'<path d="M{cx + 200} {cy - R + 26} Q{cx + 290} {cy - R + 30} {cx + 340} {cy - 70}" fill="none" stroke="#fff4c0" stroke-width="9" opacity=".7" stroke-linecap="round"/>'
    o += f'<path d="M{cx - L + 20} {cy + 70} Q{cx - 260} {cy + R - 4} {cx - 200} {cy + R - 6}" fill="none" stroke="#6a4204" stroke-width="18" opacity=".45" stroke-linecap="round"/>'
    o += f'<path d="M{cx - 250} {cy - R + 6} L{cx - 250} {cy + R - 6} M{cx + 240} {cy - R + 12} L{cx + 240} {cy + R - 14}" stroke="#9a6a12" stroke-width="4" opacity=".7"/>'
    for x in (cx - 280, cx + 270):
        for j in range(6):
            o += f'<circle cx="{x}" cy="{cy - 110 + j * 44}" r="5" fill="#7a5208"/><circle cx="{x - 1.5}" cy="{cy - 111.5 + j * 44}" r="2" fill="#fff4c0"/>'
    # red stripe, kinked through the crush
    st = [(x, cy + 30 + (18 * squeeze(x) * (1 if i % 2 else -1))) for i, x in enumerate(xs[3:-8])]
    o += f'<polyline points="{P(st)}" fill="none" stroke="#c8423a" stroke-width="18" stroke-linejoin="round"/>'
    # cracked porthole on the nose
    px, py = cx - 300, cy - 20
    o += f'<circle cx="{px}" cy="{py}" r="58" fill="#9aa4b0" stroke="#2a1c06" stroke-width="6"/><circle cx="{px}" cy="{py}" r="42" fill="#14314a" stroke="#2a1c06" stroke-width="4"/>'
    o += f'<path d="M{px - 26} {py - 26} Q{px - 10} {py - 38} {px + 10} {py - 34}" fill="none" stroke="#bfe6ff" stroke-width="6" opacity=".7" stroke-linecap="round"/>'
    o += f'<path d="M{px - 30} {py - 14} L{px - 2} {py + 4} L{px + 22} {py - 24} M{px - 2} {py + 4} L{px + 10} {py + 36} M{px - 2} {py + 4} L{px - 36} {py + 20}" fill="none" stroke="#e8f6ff" stroke-width="3"/>'
    for k in range(8):
        a_ = k / 8 * 2 * math.pi
        o += f'<circle cx="{px + 50 * math.cos(a_):.0f}" cy="{py + 50 * math.sin(a_):.0f}" r="4" fill="#4a3a20"/>'
    # headlamp, dimmed
    o += f'<circle cx="{cx - L + 20}" cy="{cy + 50}" r="16" fill="#fffbe0" stroke="#2a1c06" stroke-width="4"/>'
    # popped rivets flying out + escaping bubbles
    for k in range(6):
        x = cx - 60 + k * 30 + rnd.uniform(-10, 10); y = cy - 170 - rnd.uniform(0, 60)
        o += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="6" fill="#9a6a12" stroke="#2a1c06" stroke-width="2"/>'
    for k in range(14):
        x = cx - 40 + rnd.uniform(-60, 80); y = cy - 220 - k * 26 + rnd.uniform(-10, 10)
        o += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{rnd.uniform(5, 15):.0f}" fill="none" stroke="#e8fbff" stroke-width="3" opacity=".75"/>'
    return o

def gauge(x, y, r):
    o = f'<g transform="translate({x} {y})">'
    o += f'<circle r="{r + 60}" fill="#ff5a3a" opacity=".2" filter="url(#b24)"/>'
    o += f'<circle r="{r + 16}" fill="#9aa4b0" stroke="#141a22" stroke-width="7"/><circle r="{r}" fill="#f4f1e6" stroke="#141a22" stroke-width="5"/>'

    def arc(a0, a1, col, w=22):
        rr = r - 26
        p0 = (rr * math.cos(math.radians(a0)), rr * math.sin(math.radians(a0))); p1 = (rr * math.cos(math.radians(a1)), rr * math.sin(math.radians(a1)))
        return f'<path d="M{p0[0]:.1f} {p0[1]:.1f} A{rr} {rr} 0 0 1 {p1[0]:.1f} {p1[1]:.1f}" fill="none" stroke="{col}" stroke-width="{w}"/>'
    o += arc(135, 240, '#5cb85c') + arc(240, 330, '#f2b632') + arc(330, 405, '#d9382a')
    for k in range(28):
        a = math.radians(135 + k * 10); r0 = r - 50 if k % 3 == 0 else r - 40
        o += f'<line x1="{r0 * math.cos(a):.1f}" y1="{r0 * math.sin(a):.1f}" x2="{(r - 14) * math.cos(a):.1f}" y2="{(r - 14) * math.sin(a):.1f}" stroke="#141a22" stroke-width="{5 if k % 3 == 0 else 3}"/>'
    a = math.radians(418)   # pinned past the red end
    o += f'<path d="M{-14 * math.cos(a + 1.57):.1f} {-14 * math.sin(a + 1.57):.1f} L{(r - 20) * math.cos(a):.1f} {(r - 20) * math.sin(a):.1f} L{14 * math.cos(a + 1.57):.1f} {14 * math.sin(a + 1.57):.1f}Z" fill="#c8241a" stroke="#141a22" stroke-width="3"/>'
    o += '<circle r="20" fill="#141a22"/><circle r="8" fill="#9aa4b0"/>'
    for k in range(3):
        aa = math.radians(400 - k * 9)
        o += f'<path d="M{(r - 40) * math.cos(aa):.1f} {(r - 40) * math.sin(aa):.1f} A{r - 40} {r - 40} 0 0 0 {(r - 40) * math.cos(aa - .3):.1f} {(r - 40) * math.sin(aa - .3):.1f}" fill="none" stroke="#c8241a" stroke-width="4" opacity="{.6 - k * .15:.2f}"/>'
    o += f'<path d="M{-r * .7:.0f} {-r * .3:.0f} Q{-r * .5:.0f} {-r * .75:.0f} {-r * .05:.0f} {-r * .8:.0f}" fill="none" stroke="#ffffff" stroke-width="12" opacity=".7" stroke-linecap="round"/>'
    o += f'<path d="M{r * .2:.0f} {-r * .9:.0f} L{r * .05:.0f} {-r * .4:.0f} L{r * .3:.0f} {-r * .1:.0f}" fill="none" stroke="#5a6470" stroke-width="3"/>'
    return o + '</g>'

def calm_fish(x, y, s, rnd):
    o = f'<g transform="translate({x} {y}) scale({s})" stroke="#3a2030" stroke-width="5" stroke-linejoin="round">'
    o += '<ellipse cx="40" cy="70" rx="200" ry="22" fill="#000" opacity=".35" stroke="none" filter="url(#b12)"/>'
    o += '<path d="M60 -10 Q160 -40 330 -6 Q260 0 330 10 Q160 40 60 30Z" fill="#e6b8c8" opacity=".75"/>'   # long fringed tail fin
    o += '<path d="M-110 -10 Q-110 -80 -20 -84 Q60 -84 120 -36 Q200 -10 330 0 Q200 14 120 34 Q60 70 -20 70 Q-110 64 -110 -10Z" fill="url(#fishG)"/>'
    o += '<path d="M-96 -30 Q-70 -76 -10 -78 Q60 -76 110 -40" fill="none" stroke="#fff4f8" stroke-width="9" opacity=".8" stroke-linecap="round"/>'
    for _ in range(26):
        o += f'<circle cx="{rnd.uniform(-90, 120):.0f}" cy="{rnd.uniform(-50, 50):.0f}" r="{rnd.uniform(2, 5):.1f}" fill="#b4748e" stroke="none" opacity=".4"/>'
    o += '<path d="M20 30 Q50 80 90 70 Q70 40 40 22Z" fill="#f0c8d6" opacity=".9" stroke-width="3"/>'   # pectoral fin
    o += '<circle cx="-56" cy="-18" r="16" fill="#1a1020" stroke-width="3"/><circle cx="-61" cy="-23" r="6" fill="#fff" stroke="none"/>'
    o += '<path d="M-104 16 q14 12 30 4" fill="none" stroke-width="4"/>'   # relaxed little smile
    return o + '</g>'

def isopod_front(cx, cy, W, H, rnd):
    """giant isopod seen from the front, towering: dome of plates, head with two big compound eyes, antennae, legs"""
    o = f'<ellipse cx="{cx}" cy="{cy + H * .62:.0f}" rx="{W * .62:.0f}" ry="60" fill="#020a10" opacity=".6" filter="url(#b24)"/>'
    # legs splayed on both sides: 3 thick jointed walking legs per side at clearly different angles (back leg first)
    for side in (-1, 1):
        for (hx_, hy_, kx_, ky_, fx_, fy_, w, col) in ((.30, .02, .62, -.10, .80, .46, 22, '#8e7488'),
                                                      (.30, .12, .60, .04, .66, .56, 26, '#a68aa0'),
                                                      (.28, .24, .50, .20, .46, .64, 30, '#b99db0')):
            x0, y0 = cx + side * W * hx_, cy + H * hy_
            kx, ky = cx + side * W * kx_, cy + H * ky_
            fx, fy = cx + side * W * fx_, cy + H * fy_
            d_ = f'M{x0:.0f} {y0:.0f} L{kx:.0f} {ky:.0f} L{fx:.0f} {fy:.0f}'
            o += f'<path d="{d_}" fill="none" stroke="#2c1a2c" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round"/>'
            o += f'<path d="{d_}" fill="none" stroke="{col}" stroke-width="{w - 12}" stroke-linecap="round" stroke-linejoin="round"/>'
            o += f'<path d="M{x0 + side * 20:.0f} {y0 - 4:.0f} L{kx - side * 6:.0f} {ky - 6:.0f}" stroke="#f4e4ec" stroke-width="4" opacity=".6" stroke-linecap="round"/>'
            o += f'<circle cx="{kx:.0f}" cy="{ky:.0f}" r="{w * .55:.0f}" fill="{col}" stroke="#2c1a2c" stroke-width="4"/>'
            o += f'<path d="M{fx:.0f} {fy:.0f} l{side * 22} 12" stroke="#2c1a2c" stroke-width="8" stroke-linecap="round"/>'
    # dome of overlapping plates, back (top) to front (bottom)
    n = 8
    for k in range(n):
        t = k / (n - 1)
        rx = W * (.40 + .10 * math.sin(t * math.pi * .9))
        top = cy - H * .55 + t * H * .48
        bot = top + H * .32
        o += (f'<path d="M{cx - rx:.0f} {bot:.0f} Q{cx - rx * 1.02:.0f} {top + 10:.0f} {cx} {top:.0f} Q{cx + rx * 1.02:.0f} {top + 10:.0f} {cx + rx:.0f} {bot:.0f} '
              f'Q{cx} {bot + 40:.0f} {cx - rx:.0f} {bot:.0f}Z" fill="url(#isoF)" stroke="#2c1a2c" stroke-width="6" stroke-linejoin="round"/>')
        o += f'<path d="M{cx - rx * .7:.0f} {top + 30:.0f} Q{cx} {top + 4:.0f} {cx + rx * .7:.0f} {top + 30:.0f}" fill="none" stroke="#ffffff" stroke-width="8" opacity=".6" stroke-linecap="round"/>'
        o += f'<path d="M{cx + rx * .72:.0f} {top + 40:.0f} Q{cx + rx * .98:.0f} {top + 80:.0f} {cx + rx * .96:.0f} {bot - 10:.0f}" fill="none" stroke="#6fd6ff" stroke-width="6" opacity=".45" stroke-linecap="round"/>'
        for _ in range(26):
            a = rnd.uniform(-.85, .85)
            o += f'<circle cx="{cx + a * rx:.0f}" cy="{top + 40 + rnd.uniform(0, 60) + abs(a) * 30:.0f}" r="{rnd.uniform(1.5, 3.6):.1f}" fill="#6a4e66" opacity=".35"/>'
    # head
    hy = cy + H * .30; hw = W * .30
    o += f'<path d="M{cx - hw:.0f} {hy - 20:.0f} Q{cx} {hy - 70:.0f} {cx + hw:.0f} {hy - 20:.0f} Q{cx + hw + 10:.0f} {hy + 70:.0f} {cx} {hy + 90:.0f} Q{cx - hw - 10:.0f} {hy + 70:.0f} {cx - hw:.0f} {hy - 20:.0f}Z" fill="url(#isoF)" stroke="#2c1a2c" stroke-width="6"/>'
    o += f'<path d="M{cx - hw * .6:.0f} {hy - 30:.0f} Q{cx} {hy - 56:.0f} {cx + hw * .6:.0f} {hy - 30:.0f}" fill="none" stroke="#ffffff" stroke-width="7" opacity=".6" stroke-linecap="round"/>'
    # mouthparts
    o += f'<path d="M{cx - 40} {hy + 40} Q{cx} {hy + 90} {cx + 40} {hy + 40}" fill="#7a5468" stroke="#2c1a2c" stroke-width="5"/>'
    o += f'<path d="M{cx - 14} {hy + 50} l0 30 M{cx + 14} {hy + 50} l0 30" stroke="#2c1a2c" stroke-width="5"/>'
    # big compound eyes on the sides of the head
    for side in (-1, 1):
        ex, ey = cx + side * hw * .78, hy + 10
        o += f'<ellipse cx="{ex:.0f}" cy="{ey:.0f}" rx="58" ry="44" fill="#1e1c26" stroke="#120c14" stroke-width="6" transform="rotate({side * 25} {ex:.0f} {ey:.0f})"/>'
        for i in range(-6, 7):
            for j in range(-4, 5):
                px = ex + i * 9 + (j % 2) * 4.5; py = ey + j * 8
                if ((px - ex) / 52) ** 2 + ((py - ey) / 38) ** 2 < 1:
                    o += f'<circle cx="{px:.0f}" cy="{py:.0f}" r="3" fill="#9fc0cc" opacity=".45"/>'
        o += f'<ellipse cx="{ex - side * 14:.0f}" cy="{ey - 14:.0f}" rx="16" ry="9" fill="#ffffff" opacity=".9" transform="rotate({side * 25} {ex - side * 14:.0f} {ey - 14:.0f})"/>'
    # antennae: long pair sweeping out, short pair
    for side in (-1, 1):
        for dpath, w in ((f'M{cx + side * 50} {hy + 30} C{cx + side * 160} {hy + 140} {cx + side * 300} {hy + 120} {cx + side * 420} {hy + 230}', 15),
                         (f'M{cx + side * 26} {hy + 40} C{cx + side * 60} {hy + 110} {cx + side * 110} {hy + 120} {cx + side * 140} {hy + 170}', 11)):
            o += f'<path d="{dpath}" fill="none" stroke="#2c1a2c" stroke-width="{w}" stroke-linecap="round"/>'
            o += f'<path d="{dpath}" fill="none" stroke="#c7aabb" stroke-width="{w - 6}" stroke-dasharray="18 4" stroke-linecap="round"/>'
    return o

def snail(x, y, s):
    o = f'<g transform="translate({x} {y}) scale({s})" stroke="#2a1a10" stroke-width="3" stroke-linejoin="round">'
    o += '<path d="M-30 0 Q-34 -10 -20 -12 L30 -12 Q44 -14 46 -26 Q50 -36 44 -38 Q40 -30 36 -22 Q30 -4 24 0Z" fill="#e8d0b0"/>'
    o += '<path d="M42 -36 l6 -16 M46 -34 l12 -12" fill="none" stroke-width="2.5"/><circle cx="48" cy="-52" r="2.5" fill="#2a1a10"/><circle cx="58" cy="-46" r="2.5" fill="#2a1a10"/>'
    o += '<circle cx="0" cy="-30" r="24" fill="url(#shellG)"/>'
    o += '<path d="M0 -30 m-2 0 a4 4 0 1 1 8 0 a8 8 0 1 1 -14 4 a13 13 0 1 1 22 6 a19 19 0 1 1 -32 6" fill="none" stroke-width="2.6"/>'
    o += '<path d="M-14 -46 Q-4 -54 8 -52" fill="none" stroke="#ffffff" stroke-width="3" opacity=".8"/>'
    return o + '</g>'


def vbed(y, c0, c1, id_, rnd):
    d = lin(id_, [(0, c0), (1, c1)])
    b = f'<path d="M0 {y} Q270 {y - 24} 540 {y - 4} Q810 {y + 14} 1080 {y - 10} L1080 1920 L0 1920Z" fill="url(#{id_})"/>'
    for _ in range(70):
        b += f'<ellipse cx="{rnd.uniform(0, 1080):.0f}" cy="{rnd.uniform(y + 10, 1920):.0f}" rx="{rnd.uniform(3, 14):.0f}" ry="{rnd.uniform(2, 6):.0f}" fill="#050f14" opacity="{rnd.uniform(.2, .5):.2f}"/>'
    return d, b


def bubbles(x, y):
    return ''.join(f'<circle cx="{x + dx}" cy="{y - dy}" r="{r}" fill="none" stroke="#e8fbff" stroke-width="3" opacity=".7"/>' for dx, dy, r in ((0, 0, 10), (22, 50, 14), (4, 106, 9)))


VIG = rad('vig', 540, 960, 1150, [(0, '#000', 0), (.6, '#000', 0), (1, '#000', .65)])


# ================= 1: a 40 cm pillbug in a cat bed (vertical) =================
def bed_group(rnd, feather):
    """cat bed + curled isopod in landscape coords (bed centre x 1180, bottom y ~955); antennae reach toward `feather`"""
    cx = 1180; fx, fy = feather
    b = f'<ellipse cx="{cx}" cy="870" rx="510" ry="70" fill="#000" opacity=".5" filter="url(#b12)"/>'
    b += f'<path d="M{cx - 480} 820 Q{cx - 480} 670 {cx} 660 Q{cx + 480} 670 {cx + 480} 820 Z" fill="url(#plaid)" stroke="#3a0e0c" stroke-width="7"/>'
    b += f'<path d="M{cx - 470} 812 Q{cx - 470} 680 {cx} 670 Q{cx + 470} 680 {cx + 470} 812Z" fill="#000" opacity=".25"/>'
    b += f'<path d="M{cx - 440} 700 Q{cx} 640 {cx + 440} 700" fill="none" stroke="#ffd6a0" stroke-width="10" opacity=".55" stroke-linecap="round"/>'
    b += f'<ellipse cx="{cx}" cy="805" rx="430" ry="70" fill="#e9d6b8" stroke="#5a3a24" stroke-width="5"/>'
    b += f'<ellipse cx="{cx}" cy="800" rx="380" ry="50" fill="#f6e8cf" opacity=".8"/>'
    x0 = cx + 10 - 390
    b += isopod(cx + 10, 760, 390, 270, rnd,
                ants=((f'M{x0 - 15} 765 C{x0 - 80} 700 {fx - 40} {fy + 60} {fx + 10} {fy + 20}', 13),
                      (f'M{x0 - 10} 785 C{x0 - 60} 790 {x0 - 90} 810 {x0 - 110} 840', 11)), legs_near=False, shadow=False)
    b += (f'<path d="M{cx - 500} 800 Q{cx - 505} 950 {cx} 952 Q{cx + 505} 950 {cx + 500} 800 Q{cx + 470} 870 {cx} 878 Q{cx - 470} 870 {cx - 500} 800Z" '
          f'fill="url(#plaid)" stroke="#3a0e0c" stroke-width="7"/>')
    b += f'<path d="M{cx - 480} 830 Q{cx - 440} 900 {cx} 905 Q{cx + 440} 900 {cx + 480} 830" fill="none" stroke="#ffd6a0" stroke-width="12" opacity=".5" stroke-linecap="round"/>'
    b += f'<path d="M{cx - 500} 880 Q{cx - 480} 950 {cx} 952 Q{cx + 480} 950 {cx + 500} 880" fill="none" stroke="#2a0806" stroke-width="16" opacity=".5"/>'
    b += f'<path d="M{cx - 470} 846 Q{cx - 420} 920 {cx} 924 Q{cx + 420} 920 {cx + 470} 846" fill="none" stroke="#fff3d6" stroke-width="3.5" stroke-dasharray="14 10" opacity=".8"/>'
    return b


def pet_bowl(bx, by, rnd):
    b = f'<ellipse cx="{bx}" cy="{by + 18}" rx="120" ry="20" fill="#000" opacity=".45" filter="url(#b6)"/>'
    b += f'<path d="M{bx - 110} {by - 40} L{bx - 84} {by + 10} Q{bx} {by + 26} {bx + 84} {by + 10} L{bx + 110} {by - 40} Z" fill="#3e8fc0" stroke="#0c2234" stroke-width="5"/>'
    b += f'<ellipse cx="{bx}" cy="{by - 40}" rx="110" ry="22" fill="#5fb0dc" stroke="#0c2234" stroke-width="5"/>'
    b += f'<ellipse cx="{bx}" cy="{by - 40}" rx="88" ry="14" fill="#efe6d0"/>'
    for _ in range(30):
        b += f'<circle cx="{bx + rnd.uniform(-80, 80):.0f}" cy="{by - 42 + rnd.uniform(-8, 6):.0f}" r="{rnd.uniform(2, 5):.1f}" fill="{rnd.choice(["#d9c9a6", "#fff8e6", "#b8a882"])}"/>'
    px, py = bx + 6, by - 8
    b += f'<ellipse cx="{px}" cy="{py}" rx="14" ry="11" fill="#f6efe0"/>' + ''.join(f'<circle cx="{px + ox}" cy="{py + oy}" r="6" fill="#f6efe0"/>' for ox, oy in ((-18, -14), (-6, -22), (8, -22), (20, -14)))
    return b


def make_1():
    rnd = random.Random(31)
    d = FILTERS + ISO_GRAD + VIG
    d += lin('w1', [(0, '#123a5c'), (.55, '#0a2440'), (1, '#040e1c')])
    d += rad('lamp1', 560, 1420, 640, [(0, '#ffd890', .45), (.5, '#ff9e50', .12), (1, '#000', 0)])
    d += rad('bulb1', 540, 330, 260, [(0, '#fff4c8', .9), (.4, '#ffcf80', .3), (1, '#000', 0)])
    d += lin('shade1', [(0, '#e9b84a'), (1, '#9a6a1c')], 1, 0)
    d += ('<pattern id="plaid" width="60" height="60" patternUnits="userSpaceOnUse"><rect width="60" height="60" fill="#b8423a"/>'
          '<rect x="0" y="22" width="60" height="16" fill="#8a2a26"/><rect x="22" y="0" width="16" height="60" fill="#8a2a26" opacity=".8"/>'
          '<rect x="0" y="28" width="60" height="4" fill="#f2d27a" opacity=".8"/><rect x="28" y="0" width="4" height="60" fill="#f2d27a" opacity=".6"/></pattern>')
    b = '<rect width="1080" height="1920" fill="url(#w1)"/>'
    b += snow(rnd, 220, 0, 1080, 0, 1500, .08, .4)
    sd, sb = vbed(1500, '#24404e', '#08141a', 'floor1', rnd); d += sd; b += sb
    # a cosy living-room pendant lamp hanging in the deep, lighting the bed below
    b += '<path d="M400 330 L680 330 L1060 1700 L20 1700 Z" fill="#fff1c8" opacity=".12" filter="url(#b24)"/>'
    b += '<rect width="1080" height="1920" fill="url(#lamp1)"/>'
    b += '<rect width="1080" height="1920" fill="url(#bulb1)"/>'
    b += '<path d="M540 0 L540 200" stroke="#1d1208" stroke-width="8"/>'
    b += ('<path d="M470 200 L610 200 L700 320 Q540 346 380 320 Z" fill="url(#shade1)" stroke="#2a1c06" stroke-width="7" stroke-linejoin="round"/>'
          '<path d="M480 212 L420 312" stroke="#fff0b8" stroke-width="10" opacity=".7" stroke-linecap="round"/>'
          '<ellipse cx="540" cy="326" rx="150" ry="18" fill="#3a2808" stroke="#2a1c06" stroke-width="5"/>'
          '<circle cx="540" cy="336" r="34" fill="#fffbe6"/><circle cx="540" cy="336" r="70" fill="#fff4c8" opacity=".5" filter="url(#b12)"/>')
    b += '<rect x="490" y="186" width="100" height="18" rx="6" fill="#6a4a1a" stroke="#2a1c06" stroke-width="4"/>'
    b += snow(rnd, 120, 120, 960, 360, 1500, .4, .95, '#fff4d8')
    # far rocks
    b += '<path d="M0 1490 Q120 1430 260 1460 L300 1510 L0 1510Z" fill="#0a2030" opacity=".9"/><path d="M820 1500 Q940 1440 1080 1460 L1080 1510 L820 1510Z" fill="#0a2030" opacity=".9"/>'
    # bed + isopod (landscape coords scaled into the lower half)
    s, cxv, bottom = .88, 590, 1665
    tx, ty = cxv - 1185 * s, bottom - 955 * s
    fe = (215, 1350)   # feather tip, page coords
    feo = ((fe[0] - tx) / s, (fe[1] - ty) / s)
    b += f'<g transform="translate({tx:.1f} {ty:.1f}) scale({s})">{bed_group(rnd, feo)}</g>'
    b += f'<g transform="translate(900 1716) scale(.72)">{pet_bowl(0, 0, rnd)}</g>'
    # frog dangling the feather toy
    arm = 'M38 -22 q10 -20 4 -50'
    fx, fy, fs = 150, 1735, 2.3
    hx, hy = hand_at(fx, fy, fs, arm)
    tip = (150, 1250)
    b += f'<path d="M{hx:.0f} {hy:.0f} Q{hx + 40:.0f} {hy - 200:.0f} {tip[0]} {tip[1]}" fill="none" stroke="#1d1208" stroke-width="12" stroke-linecap="round"/>'
    b += f'<path d="M{hx:.0f} {hy:.0f} Q{hx + 40:.0f} {hy - 200:.0f} {tip[0]} {tip[1]}" fill="none" stroke="#c88a46" stroke-width="6" stroke-linecap="round"/>'
    b += f'<path d="M{tip[0]} {tip[1]} Q{tip[0] + 40} {tip[1] + 20} {fe[0]} {fe[1] - 80}" fill="none" stroke="#f4eedc" stroke-width="3"/>'
    for ang, col in ((-30, '#ff6fa0'), (0, '#f2d27a'), (30, '#6fd6ff')):
        b += (f'<g transform="translate({fe[0]} {fe[1] - 80}) rotate({ang}) scale(.8)"><path d="M0 0 Q-22 40 0 96 Q22 40 0 0Z" fill="{col}" stroke="#1d1208" stroke-width="3"/>'
              f'<path d="M0 6 L0 90" stroke="#1d1208" stroke-width="2.5"/></g>')
    b += f'<circle cx="{fe[0]}" cy="{fe[1] - 50}" r="60" fill="#fff6d6" opacity=".25" filter="url(#b24)"/>'
    b += frog(fx, fy, fs, look=(10, -8), mouth='O', helmet=True, shadow=True, armL='M-34 -22 q-18 4 -24 22', armR=arm)
    b += spark(300, 1300, 18) + spark(880, 1230, 18) + spark(780, 520, 14, '#fff6d6') + spark(240, 600, 12)
    b += '<rect width="1080" height="1920" fill="url(#vig)"/>'
    lines = [('40 CM', 250, 'y'), ('PILLBUG', 172, 'w')]
    return vpage('#0a2440', vsvg(d, b), lines, outline='#03101c', top=700)


# ================= 2: eyes like dinner plates (vertical) =================
def plate_eye(rnd):
    """landscape coords: plate-eye centre (1200, 610), fork at x 822, knife at x 1580"""
    b = '<circle cx="1200" cy="610" r="350" fill="#2a0608" opacity=".6" filter="url(#b24)"/>'
    b += '<circle cx="1200" cy="610" r="318" fill="#200406"/>'
    b += '<circle cx="1200" cy="610" r="300" fill="url(#china)" stroke="#5a6a7c" stroke-width="4"/>'
    b += '<circle cx="1200" cy="610" r="288" fill="none" stroke="#e0b450" stroke-width="7"/>'
    b += '<circle cx="1200" cy="610" r="238" fill="none" stroke="#e0b450" stroke-width="5"/>'
    for k in range(28):
        a = k / 28 * 2 * math.pi; r = 263
        x, y = 1200 + r * math.cos(a), 610 + r * math.sin(a)
        b += f'<g transform="translate({x:.0f} {y:.0f}) rotate({math.degrees(a) + 90:.0f})"><path d="M0 -14 Q10 -4 0 12 Q-10 -4 0 -14Z" fill="#3a6fb0"/><circle cx="12" cy="0" r="3" fill="#3a6fb0"/><circle cx="-12" cy="0" r="3" fill="#3a6fb0"/></g>'
    b += '<circle cx="1200" cy="612" r="214" fill="#2a1404"/><circle cx="1200" cy="612" r="208" fill="url(#iris2)"/>'
    for k in range(56):
        a = k / 56 * 2 * math.pi
        b += f'<line x1="{1200 + 156 * math.cos(a):.0f}" y1="{612 + 156 * math.sin(a):.0f}" x2="{1200 + 204 * math.cos(a):.0f}" y2="{612 + 204 * math.sin(a):.0f}" stroke="#f2d27a" stroke-width="3" opacity=".35"/>'
    b += '<circle cx="1185" cy="612" r="148" fill="url(#pup2)"/>'
    b += f'<g clip-path="url(#pupC)"><circle cx="1210" cy="640" r="110" fill="#1a4870" opacity=".6" filter="url(#b24)"/>{sperm_whale(1196, 636, .62, "#04101c", "#7fe0ff")}</g>'
    b += '<path d="M1080 520 Q1130 462 1220 468 Q1150 494 1110 556Z" fill="#ffffff" opacity=".85"/>'
    b += '<path d="M1460 470 Q1500 560 1470 660" fill="none" stroke="#ffffff" stroke-width="12" opacity=".5" stroke-linecap="round"/>'
    b += '<ellipse cx="830" cy="660" rx="70" ry="260" fill="#bfe6ff" opacity=".14" filter="url(#b24)"/>'
    b += fork(822, 380, 900, 1.0)
    b += knife(1580, 340, 1.0)
    return b


def make_2():
    rnd = random.Random(7)
    d = FILTERS + VIG
    d += rad('deep2', 540, 1200, 1300, [(0, '#0a2846', 1), (.6, '#040f1e', 1), (1, '#01040a', 1)])
    d += rad('skin2', 540, 420, 760, [(0, '#c0443a', 1), (.5, '#7c1e1c', 1), (1, '#2c0608', 1)])
    d += rad('china', 1200, 600, 300, [(0, '#ffffff', 1), (.8, '#e8f0f8', 1), (1, '#a8b8c8', 1)])
    d += rad('iris2', 1200, 610, 205, [(0, '#3a1e06', 1), (.7, '#8a5418', 1), (.88, '#f0b850', 1), (1, '#6a3e10', 1)])
    d += rad('pup2', 1180, 600, 150, [(0, '#0e2440', 1), (.75, '#030810', 1), (1, '#000', 1)])
    d += lin('steel', [(0, '#f4f7fb'), (.5, '#b8c2d0'), (1, '#6c7888')], 1, 0)
    d += '<clipPath id="pupC"><circle cx="1185" cy="612" r="146"/></clipPath>'
    b = '<rect width="1080" height="1920" fill="url(#deep2)"/>'
    b += snow(rnd, 200, 0, 1080, 0, 1920, .06, .3, '#cfe6ff')
    for _ in range(30):
        x, y = rnd.uniform(40, 1040), rnd.uniform(1180, 1760)
        b += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{rnd.uniform(3, 6):.1f}" fill="#6ff6ff" opacity=".8"/><circle cx="{x:.0f}" cy="{y:.0f}" r="14" fill="#6ff6ff" opacity=".25" filter="url(#b6)"/>'
    # squid mantle filling the upper half = the red "tablecloth"; arms hang down both sides past the text
    for p, w0, w1, sd in [(((90, 760), (20, 1100), (120, 1350), (40, 1640)), 50, 14, 1),
                          (((990, 760), (1070, 1080), (940, 1330), (1040, 1620)), 50, 14, -1),
]:
        b += tentacle(p, w0, w1, '#8c2622', '#2a0606', '#d1604a', suck='#e8b49a', side=sd)
    b += '<path d="M-40 -40 L1120 -40 L1120 640 Q1100 860 540 880 Q-20 860 -40 640Z" fill="url(#skin2)"/>'
    for _ in range(220):
        x = rnd.uniform(0, 1080); y = rnd.uniform(0, 860)
        if (x - 540) ** 2 + (y - 480) ** 2 < 330 ** 2 or y > 820 - abs(x - 540) * .2: continue
        if 130 < x < 230 or 860 < x < 960: continue
        b += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{rnd.uniform(4, 14):.0f}" fill="{rnd.choice(["#d44a30", "#7a1414", "#e8704a", "#4a0a0c"])}" opacity="{rnd.uniform(.25, .7):.2f}"/>'
    b += '<path d="M60 700 Q300 850 540 856 Q780 850 1020 700" fill="none" stroke="#2a0406" stroke-width="18" opacity=".55" stroke-linecap="round"/>'
    b += '<path d="M60 120 Q300 40 540 40" fill="none" stroke="#ef8a6e" stroke-width="12" opacity=".4" stroke-linecap="round"/>'
    s = .92
    b += f'<g transform="translate({540 - 1200 * s:.1f} {480 - 610 * s:.1f}) scale({s})">{plate_eye(rnd)}</g>'
    # the hunter: a sperm whale shadow far below, lit faintly by bioluminescence
    b += '<ellipse cx="640" cy="1420" rx="300" ry="90" fill="#1a4870" opacity=".35" filter="url(#b50)"/>'
    b += f'<g transform="translate(1290 0) scale(-1 1)">{sperm_whale(650, 1420, 1.25, "#0a1c2e", "#5fc8ee")}</g>'
    # frog with bib and fork, bottom-left
    bib = '<path d="M-22 -24 L30 -24 L20 4 L4 14 L-12 4 Z" fill="#ffffff" stroke-width="3"/><path d="M-22 -24 L30 -24" stroke="#c8423a" stroke-width="4"/>'
    arm = 'M38 -22 q18 -12 24 -40'
    fx, fy, fs = 330, 1730, 2.4
    b += '<circle cx="330" cy="1600" r="170" fill="#6ff6ff" opacity=".1" filter="url(#b50)"/>'
    b += frog(fx, fy, fs, look=(11, -6), mouth='O', helmet=True, shadow=True, mid=bib, armL='M-34 -22 q-18 4 -24 22', armR=arm)
    hx, hy = hand_at(fx, fy, fs, arm)
    b += f'<g transform="translate({hx:.0f} {hy:.0f}) rotate(16)">{fork(0, -150, 0, .32)}</g>'
    b += bubbles(360, 1450)
    b += spark(420, 330, 22, '#ffffff') + spark(860, 1240, 16) + spark(200, 1250, 14, '#e8fbff')
    b += '<rect width="1080" height="1920" fill="url(#vig)"/>'
    lines = [('EYES LIKE', 150, 'w'), ('PLATES', 220, 'y')]
    return vpage('#040f1e', vsvg(d, b), lines, outline='#03070f', top=930)


# ================= 3: a whale fall, months apart (vertical) =================
def make_3():
    rnd = random.Random(41)
    d = FILTERS + ISO_GRAD + VIG
    d += lin('w3', [(0, '#1d5a78'), (.45, '#0b2c44'), (1, '#03101c')])
    d += lin('whaleG', [(0, '#c8dcea'), (.35, '#7896ae'), (1, '#28405a')])
    d += rad('halo3', 560, 420, 560, [(0, '#e8fbff', .45), (.5, '#9fd8f0', .12), (1, '#000', 0)])
    b = '<rect width="1080" height="1920" fill="url(#w3)"/>'
    b += '<path d="M250 -20 L900 -20 L860 1560 L300 1560 Z" fill="#e8fbff" opacity=".12" filter="url(#b24)"/>'
    b += '<path d="M440 -20 L700 -20 L660 1560 L460 1560 Z" fill="#ffffff" opacity=".07" filter="url(#b24)"/>'
    b += '<rect width="1080" height="1920" fill="url(#halo3)"/>'
    b += snow(rnd, 300, 0, 1080, 0, 1560, .08, .45)
    sd, sb = vbed(1540, '#2c4a54', '#07121a', 'floor3', rnd); d += sd; b += sb
    b += '<path d="M800 1600 q40 -30 90 -10 q30 14 50 0" fill="none" stroke="#5f8a86" stroke-width="5" opacity=".5"/>'
    # the whale fall, sinking nose-down toward the mud
    b += '<ellipse cx="560" cy="420" rx="460" ry="260" fill="#ffffff" opacity=".07" filter="url(#b50)"/>'
    b += whale(150, 600, .9, -28)
    b += snow(rnd, 120, 100, 1000, 120, 720, .4, .95, '#f8fffb')
    for ax, ay, r in ((140, 700, 20), (230, 760, 40), (90, 600, 10), (330, 690, 60), (60, 760, 30)):
        b += amphipod(ax, ay, 1.4, r)
    # lone isopod waiting on the bare mud, antennae raised toward the light
    b += '<ellipse cx="700" cy="1620" rx="320" ry="40" fill="#bfe8ff" opacity=".1" filter="url(#b24)"/>'
    b += isopod(720, 1560, 250, 170, rnd, ants=(('M455 1562 C420 1490 440 1420 500 1360', 11), ('M460 1578 C420 1560 400 1540 380 1520', 9)))
    b += hourglass(330, 1715, .95)
    b += frog(150, 1735, 2.3, look=(10, -9), mouth='O', helmet=True, shadow=True,
              armL='M-34 -22 q-20 -4 -26 -30', armR='M38 -22 q18 0 24 18')
    b += bubbles(175, 1460)
    b += spark(700, 160, 22, '#ffffff') + spark(960, 480, 16) + spark(860, 1300, 14, '#e8fbff')
    b += '<rect width="1080" height="1920" fill="url(#vig)"/>'
    lines = [('MEALS', 150, 'w'), ('MONTHS', 214, 'y'), ('APART', 150, 'w')]
    return vpage('#0b2c44', vsvg(d, b), lines, outline='#03101c', top=800)


# ================= 4: why not crushed? (vertical) =================
def make_4():
    rnd = random.Random(57)
    d = FILTERS + VIG
    d += lin('w4', [(0, '#123c58'), (.5, '#081e32'), (1, '#020a12')])
    d += lin('subG', [(0, '#ffd85a'), (.5, '#f2b632'), (1, '#9a6a12')])
    d += lin('fishG', [(0, '#fbe4ec'), (.55, '#e0a8bc'), (1, '#8a5068')])
    d += rad('lamp4', 540, 500, 600, [(0, '#ffe8a0', .25), (.5, '#ffb060', .06), (1, '#000', 0)])
    d += rad('lamp4b', 560, 1420, 420, [(0, '#ffd6e4', .16), (1, '#000', 0)])
    b = '<rect width="1080" height="1920" fill="url(#w4)"/>'
    b += '<path d="M260 -20 L820 -20 L960 1560 L120 1560 Z" fill="#e8fbff" opacity=".07" filter="url(#b24)"/>'
    b += '<rect width="1080" height="1920" fill="url(#lamp4)"/><rect width="1080" height="1920" fill="url(#lamp4b)"/>'
    b += snow(rnd, 280, 0, 1080, 0, 1560, .08, .45)
    sd, sb = vbed(1560, '#2a4450', '#06101a', 'floor4', rnd); d += sd; b += sb
    # crushed sub (landscape coords, centre 1250,600) scaled into the upper half
    s = .98
    b += f'<g transform="translate({540 - 1270 * s:.1f} {560 - 600 * s:.1f}) scale({s})">{crushed_sub(rnd)}</g>'
    # gauge on a pipe from the hull, upper-left
    b += '<path d="M200 470 Q170 400 210 330" fill="none" stroke="#141a22" stroke-width="22"/><path d="M200 470 Q170 400 210 330" fill="none" stroke="#9aa4b0" stroke-width="12"/>'
    b += gauge(230, 250, 100)
    # calm unharmed fish below the text
    b += calm_fish(560, 1400, 1.25, rnd)
    b += frog(170, 1735, 2.3, look=(12, -8), mouth='O', helmet=True, shadow=True,
              armL='M-34 -22 q-20 -6 -26 -32', armR='M38 -22 q22 -6 28 -38')
    b += bubbles(195, 1460)
    b += spark(900, 300, 18) + spark(820, 1260, 14, '#e8fbff') + spark(330, 1240, 16, '#fff6d6')
    b += '<rect width="1080" height="1920" fill="url(#vig)"/>'
    lines = [('WHY NOT', 160, 'w'), ('CRUSHED?', 164, 'y')]
    return vpage('#081e32', vsvg(d, b), lines, outline='#03101c', top=850)


# ================= 5: tiny or giant? (vertical) =================
def make_5():
    rnd = random.Random(73)
    d = FILTERS + VIG
    d += lin('w5', [(0, '#0e3448'), (.5, '#07202e'), (1, '#020a10')])
    d += lin('isoF', [(0, '#fbeef0'), (.35, '#e2c3cc'), (.75, '#a87f95'), (1, '#4e3049')])
    d += rad('shellG', -6, -38, 30, [(0, '#fff4dc', 1), (.6, '#f0a868', 1), (1, '#a85a2a', 1)])
    d += rad('halo5', 540, 1420, 620, [(0, '#8ff0e0', .26), (.6, '#3aa6a6', .06), (1, '#000', 0)])
    d += rad('spot5', 700, 600, 170, [(0, '#fff1c0', .6), (.6, '#ffd890', .15), (1, '#000', 0)])
    d += lin('rock5', [(0, '#2e4a56'), (1, '#0a1a22')])
    b = '<rect width="1080" height="1920" fill="url(#w5)"/>'
    b += '<rect width="1080" height="1920" fill="url(#halo5)"/>'
    b += snow(rnd, 280, 0, 1080, 0, 1600, .08, .5)
    sd, sb = vbed(1640, '#2a4652', '#06101a', 'floor5', rnd); d += sd; b += sb
    # TOP: a rock ledge with the tiny snail in a spotlight and the frog's magnifying glass
    b += '<path d="M640 -20 L760 -20 L820 620 L590 620 Z" fill="#fff1c0" opacity=".1" filter="url(#b24)"/>'
    b += '<path d="M-20 600 Q200 570 420 588 Q700 600 1100 578 L1100 680 Q700 700 400 690 Q150 700 -20 700Z" fill="url(#rock5)" stroke="#06121a" stroke-width="6"/>'
    b += '<path d="M20 600 Q300 576 600 594 Q800 600 1060 584" fill="none" stroke="#6f98a4" stroke-width="7" opacity=".6" stroke-linecap="round"/>'
    b += '<ellipse cx="700" cy="602" rx="150" ry="30" fill="url(#spot5)"/>'
    b += snail(705, 608, 1.15)
    arm = 'M38 -22 q24 -2 40 -14'
    fx, fy, fs = 330, 612, 2.3
    hx, hy = hand_at(fx, fy, fs, arm)
    lx, ly, lr = 695, 548, 78
    b += f'<path d="M{hx:.0f} {hy:.0f} L{lx - lr * .74:.0f} {ly + lr * .45:.0f}" stroke="#1c1208" stroke-width="22" stroke-linecap="round"/><path d="M{hx:.0f} {hy:.0f} L{lx - lr * .74:.0f} {ly + lr * .45:.0f}" stroke="#a8743a" stroke-width="13" stroke-linecap="round"/>'
    b += frog(fx, fy, fs, look=(12, -1), mouth='O', helmet=True, shadow=True, armL='M-34 -22 q-18 4 -24 22', armR=arm)
    b += f'<circle cx="{lx}" cy="{ly}" r="{lr}" fill="#dff6ff" fill-opacity=".14" stroke="#141a22" stroke-width="14"/><circle cx="{lx}" cy="{ly}" r="{lr}" fill="none" stroke="#c8ced8" stroke-width="6"/>'
    b += f'<path d="M{lx - 46} {ly - 28} Q{lx - 28} {ly - 56} {lx + 4} {ly - 58}" fill="none" stroke="#ffffff" stroke-width="8" opacity=".75" stroke-linecap="round"/>'
    b += bubbles(360, 340)
    # BOTTOM: the towering giant isopod
    b += isopod_front(540, 1500, 800, 470, rnd)
    b += spark(800, 560, 18, '#fff6d6') + spark(980, 1200, 16) + spark(110, 1240, 14, '#e8fbff')
    b += '<rect width="1080" height="1920" fill="url(#vig)"/>'
    lines = [('TINY', 200, 'w'), ('OR', 110, 'w'), ('GIANT?', 230, 'y')]
    return vpage('#07202e', vsvg(d, b), lines, outline='#03101c', top=712)


if __name__ == '__main__':
    for n, fn in enumerate((make_1, make_2, make_3, make_4, make_5), 1):
        out = os.path.join(VID, f'deep-sea-giants-short{n}', 'thumb')
        os.makedirs(out, exist_ok=True)
        open(os.path.join(out, 'A.html'), 'w').write(fn())
    print('ok')
