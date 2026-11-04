# Thumbnails A-C for deep-time-bedtime (guideline 16-6, brief tools/briefs/thumb_art.md). Run: python3 videos/deep-time-bedtime/thumb/make.py
# A  THE SKY FELL            homage: Night at the Museum (2006) - the T. rex skeleton in the museum hall at night; frog = night guard with a torch.
#                            Script S-T.rex/asteroid: "Did they know the sky was about to fall?" (asteroid streak seen through the skylight)
# B  HUMANS = LAST SECONDS   intuitive: twin-bell alarm clock whose 24-hour dial is coloured by eons/eras (proportional to 4.54 billion years);
#                            the gold sliver at midnight = us. Script S05: "a single twenty-four-hour day ... final few seconds before midnight"
# C  WHAT'S UNDER YOUR BED?  intuitive: cut-away of the ground under a bed, layers of deep time (fossils, coal, banded iron, magma at the bottom).
#                            Script closing: "The ground under your bed is not just stone and soil; it is part of a billions-of-years-old monument"
# No hands are visible (frog arms only), so tools/hands.py is imported but not drawn.
import os, sys, math, random
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../tools'))
from thumb_lib import page, svg, lin, rad, spark, stars, blobs
import hands  # noqa: F401  (brief: every visible hand via hands.py; none visible here)

INK = '#1d2b1c'; GREEN = '#6aa55a'
F = ''.join(f'<filter id="b{s}" x="-60%" y="-60%" width="220%" height="220%"><feGaussianBlur stdDeviation="{s}"/></filter>' for s in (3, 6, 12, 24, 50))


def P(v):
    return ' '.join(f'{a:.1f},{b:.1f}' for a, b in v)


def cr(pts, n=12):
    """Catmull-Rom smoothing of a point list -> dense list"""
    out = []
    p = [pts[0]] + pts + [pts[-1]]
    for i in range(1, len(p) - 2):
        p0, p1, p2, p3 = p[i - 1], p[i], p[i + 1], p[i + 2]
        for k in range(n):
            t = k / n; t2 = t * t; t3 = t2 * t
            out.append(tuple(.5 * (2 * p1[j] + (-p0[j] + p2[j]) * t + (2 * p0[j] - 5 * p1[j] + 4 * p2[j] - p3[j]) * t2 + (-p0[j] + 3 * p1[j] - 3 * p2[j] + p3[j]) * t3) for j in (0, 1)))
    out.append(pts[-1]); return out


def at(dense, u):
    """point + unit tangent at fraction u along a dense polyline"""
    L = [0]
    for a, b in zip(dense, dense[1:]): L.append(L[-1] + math.dist(a, b))
    s = u * L[-1]
    for i in range(1, len(L)):
        if L[i] >= s:
            a, b = dense[i - 1], dense[i]; f = (s - L[i - 1]) / ((L[i] - L[i - 1]) or 1)
            d = math.dist(a, b) or 1
            return (a[0] + (b[0] - a[0]) * f, a[1] + (b[1] - a[1]) * f), ((b[0] - a[0]) / d, (b[1] - a[1]) / d)
    return dense[-1], (1, 0)


# ---------------- mascot frog (tools/assets/frog.svg body; hat / props per thumbnail) ----------------
ARMS = {'down': ('q-14 6 -16 22', 'q14 6 16 22'), 'up': ('q-14 6 -16 22', 'q22 -4 30 -26'),
        'hold': ('q-10 10 -2 26', 'q10 10 2 26'), 'edge': ('q-10 14 -4 34', 'q10 14 4 34')}


def frog(x, y, s, mouth='o', arms='down', look=(2, 0), hat='', front='', back='', flip=False, legs=True):
    la, ra = ARMS[arms]; sx = -s if flip else s
    g = f'<g transform="translate({x} {y}) scale({sx} {s})" stroke="{INK}" stroke-linejoin="round" stroke-linecap="round">' + back
    if legs:
        g += '<ellipse cx="-22" cy="4" rx="16" ry="9" fill="#4d8a4a" stroke-width="3.2"/><ellipse cx="22" cy="4" rx="16" ry="9" fill="#4d8a4a" stroke-width="3.2"/>'
    g += f'<path d="M-34 0 q-6 -64 34 -70 q40 -2 42 62 q0 10 -6 12 q-36 6 -70 -4z" fill="{GREEN}" stroke-width="4"/>'
    g += '<ellipse cx="2" cy="-12" rx="22" ry="20" fill="#9cc98a" stroke="none" opacity=".7"/>'
    g += '<path d="M-26 -50 q6 -16 22 -18" fill="none" stroke="#b9e0a6" stroke-width="3" opacity=".7"/>'
    g += hat
    dx, dy = look
    for ex in (-10, 22):
        g += f'<circle cx="{ex}" cy="-66" r="13" fill="#e3e5d6" stroke-width="3.2"/><circle cx="{ex + dx}" cy="{-66 + dy}" r="5" fill="{INK}" stroke="none"/>'
        g += f'<circle cx="{ex + 2 + dx}" cy="{-68 + dy}" r="1.7" fill="#fff" stroke="none"/>'
    g += '<ellipse cx="-18" cy="-46" rx="5" ry="3" fill="#e98a8a" stroke="none" opacity=".55"/><ellipse cx="30" cy="-46" rx="5" ry="3" fill="#e98a8a" stroke="none" opacity=".55"/>'
    if mouth == 'o':
        g += '<ellipse cx="6" cy="-42" rx="6.5" ry="8" fill="#7a2f33" stroke-width="3"/><ellipse cx="6" cy="-38" rx="3.5" ry="2.6" fill="#e07b7b" stroke="none"/>'
    else:
        g += '<path d="M-8 -45 q14 14 28 0 q-14 4 -28 0z" fill="#7a2f33" stroke-width="3"/>'
    for st, path in (('M-34 -22', la), ('M38 -22', ra)):
        g += f'<path d="{st} {path}" fill="none" stroke-width="7.5"/><path d="{st} {path}" fill="none" stroke="{GREEN}" stroke-width="3.4"/>'
        sx0, sy0 = map(float, st[1:].split()); q = [float(v) for v in path[1:].split()]
        g += f'<circle cx="{sx0 + q[2]}" cy="{sy0 + q[3]}" r="5.5" fill="{GREEN}" stroke-width="3"/>'
    return g + front + '</g>'


GUARD_CAP = ('<path d="M-20 -82 C-24 -110 36 -114 34 -82 Z" fill="#23315e" stroke-width="3.2"/>'
             '<path d="M-21 -84 L35 -84 L35 -77 L-21 -77 Z" fill="#141c38" stroke-width="2.6"/>'
             '<path d="M30 -80 q22 0 30 6 q-14 6 -32 2 z" fill="#141c38" stroke-width="2.8"/>'
             '<path d="M7 -101 l3 6 l6 1 l-4.5 4 l1.2 6 l-5.7 -3 l-5.7 3 l1.2 -6 l-4.5 -4 l6 -1 z" fill="#f2d27a" stroke-width="1.6"/>'
             '<path d="M-14 -100 q8 -8 18 -8" fill="none" stroke="#5b6ea8" stroke-width="2.4"/>')


def nightcap(col='#6f6fc8', stripe='#c8c8f4'):
    g = (f'<path d="M-24 -80 C-30 -118 30 -132 70 -116 C84 -108 90 -92 92 -78 C70 -98 46 -104 36 -82 Z" fill="{col}" stroke-width="3.2"/>'
         f'<path d="M-10 -105 C10 -116 30 -118 46 -112 M20 -122 C34 -122 52 -118 64 -112 M60 -111 C72 -104 80 -96 86 -86" fill="none" stroke="{stripe}" stroke-width="5" opacity=".9"/>'
         f'<path d="M-26 -84 C-6 -90 18 -90 38 -82 L38 -76 C18 -82 -6 -82 -26 -77 Z" fill="#f3efe0" stroke-width="2.8"/>'
         f'<circle cx="94" cy="-76" r="9" fill="#f3efe0" stroke-width="2.8"/>')
    return g


# ====================================================================== A  (Night at the Museum homage)
BONE_C, BONE_D, BONE_H = '#e8dcc0', '#2a2118', '#fff8e6'


def bone(d, w, col=BONE_C, line=BONE_D, hl=True, op=1):
    s = f'<path d="{d}" fill="none" stroke="{line}" stroke-width="{w + 7}" stroke-linecap="round" stroke-linejoin="round" opacity="{op}"/>'
    s += f'<path d="{d}" fill="none" stroke="{col}" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round" opacity="{op}"/>'
    if hl:
        s += f'<path d="{d}" transform="translate({-w * .18:.1f} {-w * .22:.1f})" fill="none" stroke="{BONE_H}" stroke-width="{max(1.5, w * .28):.1f}" stroke-linecap="round" opacity=".75"/>'
    return s


def knob(x, y, r, col=BONE_C):
    return f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r + 3.5}" fill="{BONE_D}"/><circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{col}"/><circle cx="{x - r * .3:.1f}" cy="{y - r * .3:.1f}" r="{r * .35:.1f}" fill="{BONE_H}" opacity=".7"/>'


def rex_skull(x, y, s, rot, jaw=14):
    g = f'<g transform="translate({x} {y}) rotate({rot}) scale({s})" stroke="{BONE_D}" stroke-linejoin="round" stroke-linecap="round">'
    # lower jaw (opened about its hinge)
    g += f'<g transform="rotate({jaw} 34 80)">'
    g += f'<path d="M20 72 C80 88 180 84 256 66 L262 78 C200 106 110 120 42 114 C20 110 10 92 20 72 Z" fill="{BONE_C}" stroke-width="4.5"/>'
    g += ''.join(f'<path d="M{tx} {74 + (tx - 60) * -.03:.1f} l5 -15 l6 15 z" fill="#fffaf0" stroke-width="2"/>' for tx in range(66, 250, 16))
    g += '<ellipse cx="66" cy="96" rx="16" ry="7" fill="#3a2e22" stroke-width="2.5"/>'
    g += '<path d="M60 106 C120 112 190 100 250 78" fill="none" stroke="#b9a782" stroke-width="3"/></g>'
    # cranium
    g += f'<path d="M0 22 C8 -12 60 -22 112 -14 C172 -6 232 10 264 30 L270 54 C250 62 200 68 150 72 L64 82 C32 84 6 72 0 50 Z" fill="{BONE_C}" stroke-width="4.5"/>'
    g += ''.join(f'<path d="M{tx} {68 - (tx - 70) * .07:.1f} l6 18 l6 -18 z" fill="#fffaf0" stroke-width="2"/>' for tx in range(72, 262, 15))
    g += '<path d="M14 6 C60 -14 150 -10 250 22" fill="none" stroke="#fff8e6" stroke-width="5" opacity=".8"/>'
    g += '<path d="M40 70 C100 74 200 64 262 50" fill="none" stroke="#b9a782" stroke-width="3"/>'
    for cx, cy, rx, ry in ((28, 40, 15, 20), (72, 22, 15, 15), (150, 34, 36, 15), (242, 30, 10, 6)):
        g += f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="#1a1520" stroke-width="3"/>'
    g += '<circle cx="74" cy="24" r="4" fill="#ffe9a8" stroke="none" opacity=".9"/>'  # glint in the orbit
    return g + '</g>'


def trex(ox=0, oy=0):
    """mounted T. rex skeleton, head up toward the skylight (facing right)"""
    sp = [(560, 800), (700, 742), (860, 660), (1010, 586), (1140, 548), (1260, 536), (1370, 540), (1450, 520), (1510, 470), (1546, 410), (1560, 352)]
    sp = [(a + ox, b + oy) for a, b in sp]
    D = cr(sp, 14)
    out = ''
    hip = at(D, .47)[0]
    # far legs (darker)
    dark = '#a99c84'
    hx, hy = hip
    far = [(hx - 30, hy + 30), (hx - 40, hy + 166), (hx - 110, hy + 270), (hx - 70, hy + 312)]
    out += bone(f'M{far[0][0]} {far[0][1]} L{far[1][0]} {far[1][1]}', 30, dark, hl=False) + bone(f'M{far[1][0]} {far[1][1]} L{far[2][0]} {far[2][1]}', 22, dark, hl=False)
    out += bone(f'M{far[2][0]} {far[2][1]} L{far[3][0]} {far[3][1]}', 14, dark, hl=False)
    for dx in (-26, 6, 34):
        out += bone(f'M{far[3][0]} {far[3][1]} l{dx + 30} 8', 9, dark, hl=False)
    # far ribs
    for i in range(9):
        u = .52 + i * .033
        (px, py), (tx, ty) = at(D, u); L = 130 + 70 * math.sin(math.pi * (i + 1) / 10)
        out += bone(f'M{px + 8:.0f} {py:.0f} Q{px + 60:.0f} {py + L * .4:.0f} {px + 26:.0f} {py + L:.0f}', 7, dark, hl=False, op=.9)
    # tail chevrons + vertebrae, back spines
    N = 46
    for i in range(N):
        u = i / (N - 1) * .985
        (px, py), (tx, ty) = at(D, u)
        nx, ny = ty, -tx  # up normal (tangent goes right/up)
        if ny > 0: nx, ny = -nx, -ny
        size = 7 + 15 * math.sin(math.pi * min(1, u / .9)) if u < .8 else 15
        size = max(6, size)
        if u < .46:   # chevrons under the tail
            out += bone(f'M{px:.0f} {py:.0f} l{-nx * size * 2.2 - tx * 6:.0f} {-ny * size * 2.2:.0f}', max(3, size * .35), hl=False)
        if u < .82:   # neural spines
            out += bone(f'M{px:.0f} {py:.0f} l{nx * size * 2 - tx * 4:.0f} {ny * size * 2:.0f}', max(3, size * .4), hl=False)
        out += f'<ellipse cx="{px:.1f}" cy="{py:.1f}" rx="{size * .9 + 3.5:.1f}" ry="{size * .62 + 3.5:.1f}" transform="rotate({math.degrees(math.atan2(ty, tx)):.0f} {px:.1f} {py:.1f})" fill="{BONE_D}"/>'
        out += f'<ellipse cx="{px:.1f}" cy="{py:.1f}" rx="{size * .9:.1f}" ry="{size * .62:.1f}" transform="rotate({math.degrees(math.atan2(ty, tx)):.0f} {px:.1f} {py:.1f})" fill="{BONE_C}"/>'
        out += f'<ellipse cx="{px - 1:.1f}" cy="{py - size * .25:.1f}" rx="{size * .45:.1f}" ry="{size * .18:.1f}" fill="{BONE_H}" opacity=".8"/>'
    # pelvis: ilium blade, pubis boot, ischium
    out += f'<path d="M{hx - 90} {hy - 10} C{hx - 80} {hy - 60} {hx + 70} {hy - 70} {hx + 96} {hy - 14} C{hx + 60} {hy + 30} {hx - 60} {hy + 30} {hx - 90} {hy - 10} Z" fill="{BONE_C}" stroke="{BONE_D}" stroke-width="4.5"/>'
    out += f'<path d="M{hx - 70} {hy - 22} C{hx - 30} {hy - 50} {hx + 40} {hy - 50} {hx + 80} {hy - 24}" fill="none" stroke="{BONE_H}" stroke-width="4" opacity=".8"/>'
    out += bone(f'M{hx + 30} {hy + 14} L{hx + 92} {hy + 160}', 18) + f'<ellipse cx="{hx + 104}" cy="{hy + 168}" rx="34" ry="13" fill="{BONE_C}" stroke="{BONE_D}" stroke-width="4"/>'
    out += bone(f'M{hx - 30} {hy + 14} L{hx - 92} {hy + 130}', 14)
    # near ribs + gastralia
    for i in range(10):
        u = .505 + i * .034
        (px, py), _ = at(D, u); L = 150 + 80 * math.sin(math.pi * (i + 1) / 11)
        out += bone(f'M{px:.0f} {py:.0f} Q{px + 70:.0f} {py + L * .38:.0f} {px + 34:.0f} {py + L:.0f}', 10)
    for i in range(8):
        x0 = hx + 110 + i * 30; y0 = hy + 168 - i * 9
        out += bone(f'M{x0} {y0} q16 6 30 -6', 5, hl=False)
    # tiny arms
    (sx, sy), _ = at(D, .79)
    out += bone(f'M{sx + 10:.0f} {sy + 60:.0f} l40 46', 11) + bone(f'M{sx + 50:.0f} {sy + 106:.0f} l34 -8', 8)
    out += bone(f'M{sx + 84:.0f} {sy + 98:.0f} l12 -12 M{sx + 84:.0f} {sy + 98:.0f} l14 4', 4, hl=False)
    # near leg
    near = [(hx + 10, hy + 20), (hx + 62, hy + 160), (hx + 6, hy + 272), (hx + 44, hy + 312)]
    out += bone(f'M{near[0][0]} {near[0][1]} Q{hx + 70} {hy + 90} {near[1][0]} {near[1][1]}', 40)
    out += bone(f'M{near[1][0]} {near[1][1]} L{near[2][0]} {near[2][1]}', 28) + bone(f'M{near[1][0] - 14} {near[1][1] + 6} L{near[2][0] - 18} {near[2][1] - 4}', 9, hl=False)
    out += bone(f'M{near[2][0]} {near[2][1]} L{near[3][0]} {near[3][1]}', 18)
    out += knob(*near[1], 22) + knob(*near[2], 14)
    for dx in (-30, 10, 46):
        ex, ey = near[3][0] + dx + 34, near[3][1] + 6
        out += bone(f'M{near[3][0]} {near[3][1]} L{ex} {ey}', 12)
        out += f'<path d="M{ex} {ey - 8} q16 2 20 12 q-12 -2 -20 2 z" fill="#fffaf0" stroke="{BONE_D}" stroke-width="3"/>'
    # neck top + skull
    tip = sp[-1]
    out += rex_skull(tip[0] - 30, tip[1] - 56, 1.12, -14)
    return out, hip


def thumb_A():
    random.seed(7)
    defs = F + lin('wallA', [(0, '#1c2550'), (.6, '#121838'), (1, '#0a0e22')])
    defs += lin('floorA', [(0, '#1e2546'), (1, '#07091a')])
    defs += lin('skyA', [(0, '#0c1640'), (1, '#2a2f6a')])
    defs += lin('stoneA', [(0, '#5a6286'), (1, '#2b3052')])
    defs += rad('moonA', 1350, 300, 700, [(0, '#bcd2ff', .45), (.4, '#8fa8ff', .14), (1, '#8fa8ff', 0)])
    defs += '<linearGradient id="beamA" x1="560" y1="860" x2="1300" y2="560" gradientUnits="userSpaceOnUse"><stop offset="0" stop-color="#fff1bf" stop-opacity=".65"/><stop offset="1" stop-color="#ffe7a6" stop-opacity=".04"/></linearGradient>'
    defs += '<linearGradient id="shaftA" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#cfe0ff" stop-opacity=".28"/><stop offset="1" stop-color="#cfe0ff" stop-opacity="0"/></linearGradient>'
    defs += rad('vigA', 960, 540, 1150, [(0, '#000', 0), (.68, '#000', 0), (1, '#000', .6)])
    defs += '<clipPath id="winA"><path d="M1060 470 L1060 230 A290 290 0 0 1 1640 230 L1640 470 Z"/></clipPath>'
    b = '<rect width="1920" height="1080" fill="url(#wallA)"/>'
    # back-wall columns
    for cx in (130, 560, 1850):
        b += f'<rect x="{cx - 46}" y="60" width="92" height="760" fill="#1a2148"/><rect x="{cx - 60}" y="40" width="120" height="30" fill="#232b58"/><rect x="{cx - 60}" y="800" width="120" height="30" fill="#151b3c"/>'
        b += ''.join(f'<rect x="{cx - 40 + k * 16}" y="72" width="5" height="728" fill="#10152f" opacity=".8"/>' for k in range(6))
        b += f'<rect x="{cx - 46}" y="60" width="14" height="760" fill="#3b4580" opacity=".5"/>'
    # tall arched window with night sky, moon, asteroid streak
    b += '<g clip-path="url(#winA)"><rect x="1050" y="0" width="600" height="480" fill="url(#skyA)"/>'
    b += ''.join(f'<circle cx="{random.randint(1070, 1630)}" cy="{random.randint(-50, 460)}" r="{random.choice([1.4, 2, 2.6])}" fill="#eef3ff" opacity="{random.uniform(.3, .9):.2f}"/>' for _ in range(70))
    b += '<circle cx="1500" cy="110" r="46" fill="#f3f0dc"/><circle cx="1486" cy="100" r="9" fill="#d9d4ba"/><circle cx="1514" cy="124" r="6" fill="#d9d4ba"/>'
    # asteroid streaking down-left
    b += '<path d="M1600 20 L1250 250" stroke="#ffb35a" stroke-width="30" stroke-linecap="round" opacity=".35" filter="url(#b12)"/>'
    b += '<path d="M1600 20 L1262 242" stroke="#ffe0a0" stroke-width="9" stroke-linecap="round" opacity=".9" filter="url(#b3)"/>'
    b += '<circle cx="1256" cy="248" r="34" fill="#ff9a40" opacity=".55" filter="url(#b12)"/><circle cx="1256" cy="248" r="15" fill="#fff4d0"/>'
    b += '</g>'
    b += '<path d="M1060 470 L1060 230 A290 290 0 0 1 1640 230 L1640 470" fill="none" stroke="#2d3566" stroke-width="22"/>'
    b += '<path d="M1350 -60 L1350 470 M1060 300 L1640 300 M1060 390 L1640 390 M1155 470 L1155 70 M1545 470 L1545 70" stroke="#2d3566" stroke-width="9" fill="none" clip-path="url(#winA)"/>'
    b += '<rect width="1920" height="1080" fill="url(#moonA)"/>'
    b += '<path d="M1060 470 L1640 470 L1800 900 L860 900 Z" fill="url(#shaftA)"/>'
    # floor
    b += '<path d="M0 820 L1920 820 L1920 1080 L0 1080 Z" fill="url(#floorA)"/>'
    for k in range(-8, 16):
        b += f'<path d="M{960 + k * 140} 820 L{960 + k * 420} 1080" stroke="#2c3462" stroke-width="2" opacity=".6"/>'
    for yy in (860, 920, 1000):
        b += f'<path d="M0 {yy} L1920 {yy}" stroke="#2c3462" stroke-width="2" opacity=".5"/>'
    b += '<ellipse cx="1350" cy="980" rx="380" ry="40" fill="#9fb6ff" opacity=".10" filter="url(#b24)"/>'
    # plinth
    b += '<path d="M600 880 L1760 880 L1790 940 L570 940 Z" fill="url(#stoneA)" stroke="#11152c" stroke-width="4"/>'
    b += '<path d="M600 880 L1760 880 L1752 868 L608 868 Z" fill="#7d86ad"/>'
    b += '<ellipse cx="1150" cy="874" rx="560" ry="10" fill="#000" opacity=".35" filter="url(#b6)"/>'
    # skeleton (with a soft moon rim glow behind)
    sk, hip = trex(0, 0)
    b += '<ellipse cx="1300" cy="520" rx="460" ry="300" fill="#a8c0ff" opacity=".12" filter="url(#b50)"/>'
    b += sk
    # torch beam from the frog onto the ribs (drawn on top, additive feel)
    b += '<path d="M750 800 L1180 470 L1400 760 Z" fill="url(#beamA)" filter="url(#b12)" style="mix-blend-mode:screen"/>'
    b += '<ellipse cx="1290" cy="640" rx="130" ry="100" fill="#ffe7a6" opacity=".16" filter="url(#b24)"/>'
    # rope barrier
    for px in (470, 880):
        b += f'<rect x="{px - 7}" y="900" width="14" height="110" rx="5" fill="#c99a3e" stroke="#2a1d0c" stroke-width="3"/><circle cx="{px}" cy="896" r="14" fill="#e6bd5e" stroke="#2a1d0c" stroke-width="3"/><ellipse cx="{px}" cy="1012" rx="30" ry="9" fill="#a57c2c" stroke="#2a1d0c" stroke-width="3"/>'
    b += '<path d="M470 910 Q675 990 880 910" fill="none" stroke="#2a0d14" stroke-width="16"/><path d="M470 910 Q675 990 880 910" fill="none" stroke="#a32638" stroke-width="10"/>'
    b += '<path d="M480 914 Q675 984 870 914" fill="none" stroke="#e0606e" stroke-width="2.5" opacity=".7"/>'
    b += spark(1720, 300, 20) + spark(1000, 560, 14) + spark(1660, 640, 12) + spark(1210, 150, 16, op=.7)
    # frog night guard with a torch, standing in front of the rope
    torch = ('<g transform="translate(70 -50) rotate(-34)"><rect x="-8" y="-9" width="42" height="18" rx="5" fill="#59606e" stroke-width="3"/>'
             '<rect x="30" y="-13" width="13" height="26" rx="3" fill="#c9ced6" stroke-width="3"/><ellipse cx="44" cy="0" rx="3.5" ry="11" fill="#fff6c8" stroke="none"/></g>')
    vest = '<path d="M-30 -30 q34 10 66 0 l4 26 q-36 10 -74 0 z" fill="#23315e" stroke-width="3"/><circle cx="-14" cy="-20" r="4" fill="#f2d27a" stroke-width="1.6"/>'
    b += '<ellipse cx="420" cy="1040" rx="110" ry="16" fill="#000" opacity=".45" filter="url(#b6)"/>'
    b += frog(420, 1036, 3.1, mouth='o', arms='up', look=(4, -4), hat=GUARD_CAP, front=torch, back='')
    b += f'<g transform="translate(420 1036) scale(3.1)" stroke="{INK}">{vest}</g>'
    b += '<rect width="1920" height="1080" fill="url(#vigA)"/>'
    lines = [('THE SKY', 170, 'w'), ('FELL', 290, 'y')]
    return page('#121838', svg(defs, b), lines, outline='#060816')


# ====================================================================== B  (alarm clock of deep time)
ERAS = [  # (name, start Ga, end Ga, fill, light)
    ('Hadean', 4.54, 4.0, '#e2532e', '#ffb070'),
    ('Archean', 4.0, 2.5, '#3f8f7a', '#8fd6b8'),
    ('Proterozoic', 2.5, .541, '#4f86c6', '#bfe0ff'),
    ('Paleozoic', .541, .252, '#5e9a3a', '#b8e07a'),
    ('Mesozoic', .252, .066, '#b07a3a', '#f0c27a'),
    ('Cenozoic', .066, 0, '#f2d27a', '#fff6d0'),
]


def wedge(cx, cy, r0, r1, a0, a1):
    def pt(r, a):
        t = math.radians(a - 90); return cx + r * math.cos(t), cy + r * math.sin(t)
    large = 1 if a1 - a0 > 180 else 0
    p0, p1, p2, p3 = pt(r1, a0), pt(r1, a1), pt(r0, a1), pt(r0, a0)
    return f'M{p0[0]:.1f} {p0[1]:.1f} A{r1} {r1} 0 {large} 1 {p1[0]:.1f} {p1[1]:.1f} L{p2[0]:.1f} {p2[1]:.1f} A{r0} {r0} 0 {large} 0 {p3[0]:.1f} {p3[1]:.1f} Z'


def polar(cx, cy, r, a):
    t = math.radians(a - 90); return cx + r * math.cos(t), cy + r * math.sin(t)


def icon(kind, x, y, s):
    g = f'<g transform="translate({x:.1f} {y:.1f}) scale({s})" stroke="#1b1730" stroke-width="2.4" stroke-linejoin="round" stroke-linecap="round">'
    if kind == 'Hadean':      # volcano with lava
        g += '<path d="M-22 14 L-6 -10 L6 -10 L22 14 Z" fill="#6b2a1a"/><path d="M-6 -10 q6 -14 12 0" fill="#ffcf5a"/><path d="M-2 -10 L-6 6 M3 -10 L6 4" stroke="#ffcf5a" stroke-width="3"/>'
    elif kind == 'Archean':   # stromatolite domes
        g += '<path d="M-24 14 q0 -22 14 -22 q14 0 14 22 z M0 14 q0 -16 12 -16 q12 0 12 16 z" fill="#d7c59a"/><path d="M-18 6 q8 -10 16 0 M5 8 q7 -7 14 0" fill="none" stroke="#8a7a52"/>'
    elif kind == 'Proterozoic':  # snowflake (Snowball Earth)
        g += ''.join(f'<path d="M0 0 L0 -18 M0 -11 l-5 -5 M0 -11 l5 -5" transform="rotate({k * 60})" fill="none" stroke="#ffffff" stroke-width="3.2"/>' for k in range(6))
    elif kind == 'Paleozoic':  # trilobite
        g += '<path d="M0 -18 C14 -18 16 -6 14 8 C12 16 4 20 0 20 C-4 20 -12 16 -14 8 C-16 -6 -14 -18 0 -18 Z" fill="#c9b48a"/><path d="M-14 -8 q14 -6 28 0" fill="none"/><path d="M0 -6 L0 18" />' + ''.join(f'<path d="M-13 {k} L13 {k}" stroke-width="1.6"/>' for k in (0, 6, 12))
    elif kind == 'Mesozoic':  # dinosaur head + neck silhouette (sauropod)
        g += '<path d="M-18 18 C-14 0 -6 -14 4 -18 C10 -20 18 -18 20 -14 C16 -12 10 -12 8 -10 C4 -4 0 8 -2 18 Z" fill="#3c2a18"/><circle cx="12" cy="-15" r="1.6" fill="#fff" stroke="none"/>'
    return g + '</g>'


def thumb_B():
    random.seed(21)
    cx, cy = 1372, 600
    defs = F + lin('wallB', [(0, '#231a4e'), (.55, '#1a1440'), (1, '#0e0b26')])
    defs += lin('brass', [(0, '#ffe6a0'), (.35, '#d9a84a'), (.7, '#9a6a22'), (1, '#5a3a10')], x2=1, y2=1)
    defs += lin('brassD', [(0, '#c9933a'), (1, '#4e320c')], x2=1, y2=1)
    defs += lin('tableB', [(0, '#5a3a2a'), (1, '#2a1812')])
    defs += rad('faceB', cx - 60, cy - 80, 360, [(0, '#fffaf0', 1), (.6, '#f6ead0', 1), (1, '#e3cfa6', 1)])
    defs += rad('haloB', cx, cy, 760, [(0, '#ffd98a', .45), (.4, '#ffb85a', .14), (1, '#ffb85a', 0)])
    defs += rad('nowB', cx, cy - 330, 130, [(0, '#fff6c8', .95), (.35, '#ffd86a', .55), (1, '#ffd86a', 0)])
    defs += rad('candleB', 760, 830, 380, [(0, '#ffcf7a', .45), (1, '#ffcf7a', 0)])
    defs += rad('vigB', 960, 540, 1150, [(0, '#000', 0), (.7, '#000', 0), (1, '#000', .55)])
    b = '<rect width="1920" height="1080" fill="url(#wallB)"/>'
    b += stars(110, 760, 0, '#f2ecff', .5, 0)
    b += '<path d="M1760 120 a70 70 0 1 0 60 108 a56 56 0 1 1 -60 -108 z" fill="#f6efd2" opacity=".9"/>'
    b += blobs(10, 900, 120, 1900, 300, '#3a2f7a', .25, .5, 90, 200)
    b += '<rect width="1920" height="1080" fill="url(#haloB)"/>'
    # nightstand
    b += '<path d="M0 990 L1920 990 L1920 1080 L0 1080 Z" fill="url(#tableB)"/><path d="M0 984 L1920 984 L1920 996 L0 996 Z" fill="#7a5238"/>'
    b += '<ellipse cx="1372" cy="1000" rx="360" ry="16" fill="#000" opacity=".45" filter="url(#b6)"/>'
    # bells + hammer (behind the case)
    for sgn in (-1, 1):
        bx, by = polar(cx, cy, 418, 34 * sgn)
        rot = 34 * sgn
        b += f'<g transform="translate({bx:.0f} {by:.0f}) rotate({rot})"><path d="M-112 30 C-112 -70 -60 -112 0 -112 C60 -112 112 -70 112 30 Z" fill="url(#brass)" stroke="#2a1a06" stroke-width="6"/>'
        b += '<path d="M-80 0 C-80 -60 -44 -88 -6 -92" fill="none" stroke="#fff4c8" stroke-width="10" opacity=".6"/><rect x="-14" y="-132" width="28" height="26" rx="6" fill="url(#brassD)" stroke="#2a1a06" stroke-width="5"/></g>'
        lx, ly = polar(cx, cy, 380, 180 - 40 * sgn)
        b += f'<path d="M{lx:.0f} {ly - 20:.0f} L{lx + 40 * sgn:.0f} {ly + 70:.0f}" stroke="#2a1a06" stroke-width="30" stroke-linecap="round"/><path d="M{lx:.0f} {ly - 20:.0f} L{lx + 40 * sgn:.0f} {ly + 70:.0f}" stroke="url(#brassD)" stroke-width="20" stroke-linecap="round"/>'
    b += f'<path d="M{cx} {cy - 380} L{cx} {cy - 470}" stroke="#2a1a06" stroke-width="16"/><path d="M{cx} {cy - 380} L{cx} {cy - 470}" stroke="#c9933a" stroke-width="8"/>'
    b += f'<ellipse cx="{cx}" cy="{cy - 478}" rx="36" ry="16" fill="url(#brass)" stroke="#2a1a06" stroke-width="5"/>'
    # case
    b += f'<circle cx="{cx}" cy="{cy}" r="392" fill="#2a1a06"/><circle cx="{cx}" cy="{cy}" r="384" fill="url(#brass)"/>'
    b += f'<circle cx="{cx}" cy="{cy}" r="352" fill="#3a2610"/>'
    b += f'<path d="M{cx - 300} {cy - 220} A372 372 0 0 1 {cx + 120} {cy - 360}" fill="none" stroke="#fff6d4" stroke-width="10" opacity=".7"/>'
    # era band (proportional to time, Hadean from midnight clockwise)
    T = 4.54
    for name, s0, s1, fill, light in ERAS:
        a0 = (T - s0) / T * 360; a1 = (T - s1) / T * 360
        b += f'<path d="{wedge(cx, cy, 262, 344, a0, a1)}" fill="{fill}" stroke="#1b1730" stroke-width="4"/>'
        b += f'<path d="{wedge(cx, cy, 330, 344, a0, a1)}" fill="{light}" opacity=".55"/>'
        if a1 - a0 > 12:
            m = (a0 + a1) / 2; ix, iy = polar(cx, cy, 303, m)
            b += icon(name, ix, iy, 1.25)
    # extra icons in the long eons
    for name, a in (('Archean', 70), ('Archean', 140), ('Proterozoic', 200), ('Proterozoic', 280)):
        ix, iy = polar(cx, cy, 303, a); b += icon(name, ix, iy, 1.1)
    # the "now" sliver at midnight
    b += f'<circle cx="{cx}" cy="{cy - 302}" r="130" fill="url(#nowB)"/>'
    b += f'<path d="{wedge(cx, cy, 256, 350, 357.5, 360)}" fill="#fffbe6" stroke="#1b1730" stroke-width="3"/>'
    b += spark(cx + 4, cy - 372, 30, '#fffbe6', .95) + spark(cx + 74, cy - 340, 14) + spark(cx - 60, cy - 352, 12)
    # dial face
    b += f'<circle cx="{cx}" cy="{cy}" r="258" fill="url(#faceB)" stroke="#1b1730" stroke-width="4"/>'
    for h in range(24):
        a = h * 15; big = h % 6 == 0
        x0, y0 = polar(cx, cy, 246, a); x1, y1 = polar(cx, cy, 246 - (34 if big else 18), a)
        b += f'<path d="M{x0:.1f} {y0:.1f} L{x1:.1f} {y1:.1f}" stroke="#3a2c4e" stroke-width="{9 if big else 4}" stroke-linecap="round"/>'
    for m in range(0, 360, 3):
        x0, y0 = polar(cx, cy, 250, m); b += f'<circle cx="{x0:.1f}" cy="{y0:.1f}" r="1.6" fill="#8a7a8e"/>'
    # tiny Earth on the dial centre-low (calm)
    b += f'<circle cx="{cx}" cy="{cy + 120}" r="46" fill="#3b78c4" stroke="#1b1730" stroke-width="3"/><path d="M{cx - 30} {cy + 104} q16 -14 30 -2 q10 14 -6 22 q-14 4 -24 -20 z M{cx + 10} {cy + 132} q20 -6 26 6 q-8 14 -26 -6 z" fill="#6aa55a"/>'
    b += f'<path d="M{cx - 30} {cy + 92} a46 46 0 0 1 50 -8" fill="none" stroke="#e6f2ff" stroke-width="4" opacity=".7"/>'
    # hands: 23:58:57 - hour (short), minute (long), second (red)
    def hand_(a, L, w, col, tail=40):
        x1, y1 = polar(cx, cy, L, a); x0, y0 = polar(cx, cy, -tail, a)
        return (f'<path d="M{x0:.1f} {y0:.1f} L{x1:.1f} {y1:.1f}" stroke="#1b1730" stroke-width="{w + 8}" stroke-linecap="round"/>'
                f'<path d="M{x0:.1f} {y0:.1f} L{x1:.1f} {y1:.1f}" stroke="{col}" stroke-width="{w}" stroke-linecap="round"/>')
    b += hand_(359.5, 170, 22, '#2e2448') + hand_(354, 236, 13, '#2e2448') + hand_(342, 244, 5, '#d8433a', 60)
    b += f'<circle cx="{cx}" cy="{cy}" r="20" fill="#d9a84a" stroke="#1b1730" stroke-width="5"/>'
    b += f'<path d="M{cx - 200} {cy - 120} A240 240 0 0 1 {cx - 40} {cy - 236}" fill="none" stroke="#fff" stroke-width="12" opacity=".5"/>'
    # candle glow + frog in a nightcap sitting on the nightstand, looking up at midnight
    b += '<rect width="1920" height="1080" fill="url(#candleB)"/>'
    b += '<ellipse cx="760" cy="996" rx="120" ry="14" fill="#000" opacity=".4" filter="url(#b6)"/>'
    b += '<g transform="translate(600 0)"><ellipse cx="0" cy="986" rx="42" ry="10" fill="#c9933a" stroke="#2a1a06" stroke-width="3"/>'
    b += '<rect x="-16" y="900" width="32" height="84" rx="5" fill="#f6efdc" stroke="#2a1a06" stroke-width="3"/><path d="M0 900 L0 888" stroke="#2a1a06" stroke-width="3"/>'
    b += '<ellipse cx="0" cy="870" rx="30" ry="40" fill="#ffb84a" opacity=".55" filter="url(#b6)"/><path d="M0 846 C14 866 10 886 0 890 C-10 886 -14 866 0 846 Z" fill="#ffe7a0" stroke="#e08a2a" stroke-width="2"/></g>'
    pj = '<path d="M-31 -30 q36 10 68 0 l4 24 q-38 10 -76 0 z" fill="#7a7ad8" stroke-width="3"/><path d="M-24 -26 l0 22 M-6 -24 l0 24 M12 -24 l0 24 M28 -26 l0 22" stroke="#c8c8f4" stroke-width="4" opacity=".9"/>'
    b += frog(800, 990, 3.0, mouth='o', arms='up', look=(5, -4), hat=nightcap(), front=pj)
    b += '<rect width="1920" height="1080" fill="url(#vigB)"/>'
    lines = [('HUMANS =', 150, 'w'), ('LAST', 150, 'w'), ('SECONDS', 205, 'y')]
    return page('#1a1440', svg(defs, b), lines, outline='#0b0820', top=60)


# ====================================================================== C  (what's under your bed)
def wav(y, amp, seed, x0=-20, x1=1940, n=9):
    r = random.Random(seed); pts = [(x0 + (x1 - x0) * i / n, y + r.uniform(-amp, amp)) for i in range(n + 1)]
    d = cr(pts, 8)
    return d


def band(top, bot, fill):
    d = top + list(reversed(bot))
    return f'<path d="M{P(d)} Z" fill="{fill}"/>'


def ammonite(x, y, r, rot=0):
    g = f'<g transform="translate({x} {y}) rotate({rot})">'
    g += f'<circle r="{r + 4}" fill="#2a1e12"/><circle r="{r}" fill="#e7d3a6"/>'
    pts = [(math.cos(t) * r * math.exp(-.18 * t) * .95, math.sin(t) * r * math.exp(-.18 * t) * .95) for t in [k * .15 for k in range(0, 90)]]
    g += f'<polyline points="{P(pts)}" fill="none" stroke="#7a5a32" stroke-width="{r * .07:.1f}"/>'
    for k in range(0, 80, 4):
        t = k * .15; rr = r * math.exp(-.18 * t) * .95; rr2 = rr * .78
        g += f'<path d="M{math.cos(t) * rr2:.1f} {math.sin(t) * rr2:.1f} L{math.cos(t) * rr:.1f} {math.sin(t) * rr:.1f}" stroke="#9a7a4a" stroke-width="{r * .04:.1f}"/>'
    g += f'<path d="M{-r * .7:.1f} {-r * .5:.1f} A{r * .85:.1f} {r * .85:.1f} 0 0 1 {r * .3:.1f} {-r * .8:.1f}" fill="none" stroke="#fff4d6" stroke-width="{r * .1:.1f}" opacity=".7"/>'
    return g + '</g>'


def trilobite(x, y, s, rot=0):
    g = f'<g transform="translate({x} {y}) rotate({rot}) scale({s})" stroke="#2a1e12" stroke-width="2.6" stroke-linejoin="round">'
    g += '<path d="M0 -30 C24 -30 30 -14 26 -4 L20 26 C12 36 -12 36 -20 26 L-26 -4 C-30 -14 -24 -30 0 -30 Z" fill="#d8c8a0"/>'
    g += '<path d="M-26 -6 C-10 -14 10 -14 26 -6" fill="none"/><path d="M-7 -6 L-6 32 M7 -6 L6 32" fill="none" stroke-width="2"/>'
    g += ''.join(f'<path d="M-22 {k} L22 {k}" stroke-width="1.6"/>' for k in range(2, 30, 5))
    g += '<ellipse cx="0" cy="-18" rx="8" ry="8" fill="#e8dcb8"/><circle cx="-13" cy="-14" r="3" fill="#2a1e12"/><circle cx="13" cy="-14" r="3" fill="#2a1e12"/>'
    return g + '</g>'


def fern(x, y, s, rot=0):
    g = f'<g transform="translate({x} {y}) rotate({rot}) scale({s})" stroke="#8a8f7a" fill="none" stroke-linecap="round">'
    g += '<path d="M0 0 C10 -40 30 -80 60 -110" stroke-width="3"/>'
    for k in range(1, 12):
        t = k / 12; px, py = 60 * t ** 1.2 * .9 + 4 * t, -110 * t
        L = 26 * (1 - t) + 6
        g += f'<path d="M{px:.1f} {py:.1f} q{-L * .6:.1f} {-L * .2:.1f} {-L:.1f} {L * .1:.1f} M{px:.1f} {py:.1f} q{L * .5:.1f} {L * .1:.1f} {L:.1f} {L * .4:.1f}" stroke-width="2.4"/>'
    return g + '</g>'


def fishfossil(x, y, s, rot=0):
    g = f'<g transform="translate({x} {y}) rotate({rot}) scale({s})" stroke="#e8dcc0" fill="none" stroke-linecap="round">'
    g += '<path d="M-70 0 C-40 -26 30 -26 60 0 C30 24 -40 24 -70 0 Z" stroke="#3a1a12" stroke-width="7"/><path d="M-70 0 C-40 -26 30 -26 60 0 C30 24 -40 24 -70 0 Z" stroke-width="3.5"/>'
    g += '<path d="M-60 0 L50 0" stroke-width="4"/>' + ''.join(f'<path d="M{k} -16 Q{k + 6} 0 {k} 16" stroke-width="2.2"/>' for k in range(-44, 40, 10))
    g += '<path d="M60 0 L86 -18 L80 0 L86 18 Z" fill="#e8dcc0" stroke="#3a1a12" stroke-width="2"/><circle cx="-50" cy="-5" r="5" fill="#3a1a12"/>'
    g += '<path d="M-72 -8 C-62 -22 -46 -20 -40 -12" stroke-width="5"/>'
    return g + '</g>'


def thumb_C():
    random.seed(33)
    FLOOR = 470
    defs = F + lin('wallC', [(0, '#2a2560'), (1, '#1a1842')])
    defs += rad('lampC', 1300, 300, 520, [(0, '#ffd890', .55), (.4, '#ffbe6a', .16), (1, '#ffbe6a', 0)])
    defs += rad('magmaC', 960, 1180, 900, [(0, '#ffcf5a', .7), (.35, '#ff7a2a', .3), (1, '#ff5a1a', 0)])
    defs += rad('vigC', 960, 540, 1150, [(0, '#000', 0), (.7, '#000', 0), (1, '#000', .5)])
    defs += lin('lavaC', [(0, '#ff8a2a'), (1, '#ffd060')])
    defs += lin('woodC', [(0, '#8a5a3a'), (1, '#4a2c1c')])
    b = '<rect width="1920" height="1080" fill="url(#wallC)"/>'
    # window with moon (bedroom, between text and bed)
    b += '<rect x="1000" y="70" width="210" height="250" rx="12" fill="#0e1640" stroke="#4a3f86" stroke-width="12"/>'
    b += ''.join(f'<circle cx="{random.randint(1012, 1198)}" cy="{random.randint(82, 310)}" r="{random.choice([1.4, 2, 2.6])}" fill="#eef3ff" opacity="{random.uniform(.4, .9):.2f}"/>' for _ in range(20))
    b += '<path d="M1140 120 a40 40 0 1 0 36 62 a32 32 0 1 1 -36 -62 z" fill="#f6efd2"/>'
    b += '<path d="M1105 70 L1105 320 M1000 195 L1210 195" stroke="#4a3f86" stroke-width="8"/>'
    b += '<path d="M980 60 q40 140 -10 280 l50 0 q-30 -140 0 -280 z M1230 60 q-40 140 10 280 l-50 0 q30 -140 0 -280 z" fill="#5a3f8a" opacity=".9"/>'
    b += '<rect width="1920" height="1080" fill="url(#lampC)"/>'
    # strata (top -> bottom); y positions of boundaries
    B = [FLOOR + 22, 540, 600, 616, 712, 748, 812, 874, 930, 1000, 1100]
    cols = ['#6b4a32', '#b7c2c9', '#2a2018', '#c99a5e', '#5a5560', '#1d1a1c', '#9a4a32', '#7d8a6e', '#8a3a2a', None]
    lines_ = [wav(y, 6 if i else 0, 100 + i) for i, y in enumerate(B)]
    lines_[0] = [(-20, B[0]), (1940, B[0])]
    for i in range(len(cols)):
        if cols[i]:
            b += band(lines_[i], lines_[i + 1], cols[i])
    for i in range(1, 9):
        b += f'<path d="M{P(lines_[i])}" fill="none" stroke="#fff6e0" stroke-width="3" opacity=".22"/>'
        b += f'<path d="M{P([(x, y - 4) for x, y in lines_[i + 1]])}" fill="none" stroke="#000" stroke-width="8" opacity=".22"/>'
    # banded iron stripes
    for k in range(6):
        t = lines_[9 - 1]; yb = 936 + k * 10
        b += f'<path d="M{P([(x, y - 930 + yb) for x, y in t])}" fill="none" stroke="{"#c9584a" if k % 2 else "#5a5560"}" stroke-width="5" opacity=".85"/>'
    # magma at the bottom
    b += band(lines_[9], [(-20, 1100), (1940, 1100)], 'url(#lavaC)')
    b += '<rect width="1920" height="1080" fill="url(#magmaC)"/>'
    for i in range(8):
        x = 60 + i * 240 + random.randint(-40, 40)
        b += f'<path d="M{x} 1080 q{random.randint(-30, 30)} -40 {random.randint(-10, 10)} -70" stroke="#fff0b0" stroke-width="4" fill="none" opacity=".6"/>'
    # layer details
    b += ''.join(f'<path d="M{x} {FLOOR + 24} q{random.randint(-20, 20)} 20 {random.randint(-14, 14)} {random.randint(20, 40)}" stroke="#3a2618" stroke-width="3" fill="none"/>' for x in range(40, 1900, 70))
    b += blobs(40, 0, 500, 1920, 535, '#8a6646', .3, .7, 6, 14)
    b += blobs(30, 0, 625, 1920, 705, '#e3bf86', .2, .5, 8, 22)
    b += blobs(50, 0, 750, 1920, 808, '#3a3438', .3, .7, 6, 16)
    # Ice Age: mammoth tusk
    b += '<path d="M300 590 C360 560 460 556 520 584" fill="none" stroke="#2a1e12" stroke-width="22" stroke-linecap="round"/><path d="M300 590 C360 560 460 556 520 584" fill="none" stroke="#fff4dc" stroke-width="14" stroke-linecap="round"/>'
    # K-Pg line sparkle (the asteroid layer) - small
    # Cretaceous: T. rex skull fossil (big) + ammonite
    b += '<ellipse cx="1110" cy="664" rx="230" ry="70" fill="#fff2c8" opacity=".45" filter="url(#b24)"/>'
    b += rex_skull(990, 622, .82, -2, 10)
    b += ammonite(640, 664, 40, 20) + ammonite(1540, 670, 30, -40)
    # Permian ash: dark band, crumbly dots
    b += blobs(30, 0, 718, 1920, 742, '#8a8590', .3, .6, 4, 10)
    # Carboniferous coal: fern imprint + scale-tree bark pattern
    b += fern(760, 806, .62, 72) + fern(1340, 806, .58, 68)
    for k in range(6):
        b += ''.join(f'<path d="M{400 + j * 18 + (k % 2) * 9} {762 + k * 8} l6 4 l-6 4 l-6 -4 z" fill="none" stroke="#4a4448" stroke-width="1.6"/>' for j in range(8))
    # Devonian: fish fossil
    b += fishfossil(560, 843, .95, -4) + fishfossil(1420, 842, .7, 6)
    # Cambrian: trilobites
    b += trilobite(320, 902, 1.0, -20) + trilobite(980, 900, 1.1, 10) + trilobite(1300, 904, .85, 70)
    # Archean stromatolite domes sitting on the magma line (left/middle only)
    for x, w in ((180, 60), (260, 40), (720, 56), (1180, 48)):
        b += f'<path d="M{x - w} 1000 q0 -46 {w} -46 q{w} 0 {w} 46 z" fill="#d7c59a" stroke="#2a1e12" stroke-width="3"/>'
        b += ''.join(f'<path d="M{x - w * k / 4:.0f} 1000 q0 {-46 * k / 4:.0f} {w * k / 4:.0f} {-46 * k / 4:.0f} q{w * k / 4:.0f} 0 {w * k / 4:.0f} {46 * k / 4:.0f}" fill="none" stroke="#8a7a52" stroke-width="2"/>' for k in (1, 2, 3))
    # floor board + front edge of the cut
    b += f'<rect x="-10" y="{FLOOR}" width="1940" height="24" fill="url(#woodC)" stroke="#2a160c" stroke-width="4"/>'
    b += ''.join(f'<path d="M{x} {FLOOR + 2} L{x} {FLOOR + 22}" stroke="#2a160c" stroke-width="3"/>' for x in range(120, 1920, 260))
    # bedside lamp
    b += f'<rect x="1230" y="{FLOOR - 120}" width="110" height="120" rx="8" fill="#6a4630" stroke="#2a160c" stroke-width="4"/>'
    b += f'<rect x="1278" y="{FLOOR - 190}" width="14" height="70" fill="#c9933a" stroke="#2a160c" stroke-width="3"/>'
    b += f'<path d="M1240 {FLOOR - 190} L1330 {FLOOR - 190} L1306 {FLOOR - 270} L1264 {FLOOR - 270} Z" fill="#ffe2a0" stroke="#2a160c" stroke-width="4"/>'
    b += f'<ellipse cx="1285" cy="{FLOOR - 200}" rx="80" ry="60" fill="#fff0c0" opacity=".45" filter="url(#b24)"/>'
    # bed (headboard right)
    b += f'<rect x="1380" y="{FLOOR - 70}" width="440" height="56" rx="8" fill="#6a4630" stroke="#2a160c" stroke-width="5"/>'
    b += f'<rect x="1392" y="{FLOOR - 14}" width="22" height="14" fill="#4a2c1c"/><rect x="1786" y="{FLOOR - 14}" width="22" height="14" fill="#4a2c1c"/>'
    b += f'<path d="M1790 {FLOOR - 14} L1790 {FLOOR - 250} Q1790 {FLOOR - 290} 1830 {FLOOR - 290} Q1870 {FLOOR - 290} 1870 {FLOOR - 250} L1870 {FLOOR - 14} Z" fill="#7a5238" stroke="#2a160c" stroke-width="5"/>'
    b += f'<rect x="1390" y="{FLOOR - 112}" width="410" height="48" rx="18" fill="#f2eee6" stroke="#2a160c" stroke-width="4"/>'
    b += f'<ellipse cx="1730" cy="{FLOOR - 124}" rx="62" ry="26" fill="#fffaf2" stroke="#2a160c" stroke-width="4"/>'
    # frog sitting up in bed, peeking over the edge at the layers below
    b += frog(1560, FLOOR - 104, 2.35, mouth='o', arms='edge', look=(-3, 5), hat=nightcap('#d86a6a', '#ffd0c8'), flip=True, legs=False)
    # blanket over the frog's lap
    b += f'<path d="M1372 {FLOOR - 120} C1450 {FLOOR - 140} 1640 {FLOOR - 150} 1700 {FLOOR - 112} L1712 {FLOOR - 50} C1600 {FLOOR - 30} 1460 {FLOOR - 30} 1366 {FLOOR - 48} Z" fill="#4f7ac0" stroke="#1a1842" stroke-width="5"/>'
    b += ''.join(f'<circle cx="{1400 + k * 46}" cy="{FLOOR - 86 + (k % 2) * 16}" r="7" fill="#f2d27a" opacity=".85"/>' for k in range(7))
    b += f'<path d="M1380 {FLOOR - 112} C1460 {FLOOR - 132} 1620 {FLOOR - 140} 1690 {FLOOR - 108}" fill="none" stroke="#a8c4f0" stroke-width="5" opacity=".8"/>'
    b += spark(1210, 380, 14) + spark(1660, 230, 18) + spark(880, 660, 16) + spark(1760, 560, 12)
    b += '<rect width="1920" height="1080" fill="url(#vigC)"/>'
    lines = [("WHAT'S", 150, 'w'), ('UNDER', 150, 'w'), ('YOUR BED?', 160, 'y')]
    return page('#1a1842', svg(defs, b), lines, outline='#0a0820', top=24)


for n, fn in (('A', thumb_A), ('B', thumb_B), ('C', thumb_C)):
    open(os.path.join(HERE, f'{n}.html'), 'w').write(fn())
print('ok')
