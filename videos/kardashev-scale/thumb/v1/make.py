# Thumbnails A-C for kardashev-scale (guideline 16-6 / 16-8, brief tools/briefs/thumb_art.md). Run: python3 videos/kardashev-scale/thumb/make.py
# A  ONLY TYPE 0.7        intuitive: a glowing cosmic ladder, planet / star / galaxy on its three big rungs (S13, S15-S16, S19-S20 "ladder with
#                         huge rungs"); the frog clings to a rung BELOW the planet (S30 Sagan "somewhere around Type zero point seven", S35)
# B  SWALLOW A STAR?      homage: the binary-sunset scene of Star Wars (1977): the frog in a desert cloak on a dune watches two suns set, one
#                         of them wrapped in a swarm of solar collectors (S39 "swallow the light of a star", S41-S42 swarm, S40 none ever found)
# C  THE SKY IS SILENT    homage: Contact (1997), the listener on the car hood with headphones in front of a field of radio dishes at dusk;
#                         the frog listens, nothing comes (S54 "why is the cosmos so silent", S58 "we have not detected a signal")
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


# =========================== A: the cosmic ladder, frog below rung one ===========================
def lx(y):   # ladder centre line
    return 880 + .62 * (1120 - y)


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


def make_A():
    rnd = random.Random(7)
    d = FILTERS
    d += lin('skyA', [(0, '#0b0820'), (.5, '#160f3a'), (1, '#07051a')], x2=1, y2=1)
    d += rad('nebA', 1400, 380, 900, [(0, '#5a3aa0', .45), (.45, '#2c2370', .2), (1, '#000', 0)])
    d += rad('sunA', 0, 0, 1, [(0, '#fffbe8', 1), (.45, '#ffe08a', 1), (.8, '#ffad3a', 1), (1, '#e8761e', 1)])
    d += rad('sunHalo', 1300, 470, 420, [(0, '#ffcf70', .55), (.35, '#ff9a3a', .18), (1, '#000', 0)])
    d += rad('earthA', -30, -40, 140, [(0, '#5fb4ff', 1), (.6, '#1f6fc8', 1), (1, '#0b2f6a', 1)])
    d += lin('railA', [(0, '#fff0b8'), (.5, '#f2c45a'), (1, '#9a6a1a')], x2=1, y2=0)
    d += '<clipPath id="eclip"><circle r="104"/></clipPath>'
    d += rad('vigA', 960, 540, 1150, [(0, '#000', 0), (.7, '#000', 0), (1, '#000', .55)])
    b = '<rect width="1920" height="1080" fill="url(#skyA)"/><rect width="1920" height="1080" fill="url(#nebA)"/>'
    b += starfield(rnd, 320, (0, 0, 1920, 1080), '#eef0ff', corner)
    # faint distant galaxies for depth
    for gx, gy, r_ in ((260, 760, 40), (1820, 620, 30), (620, 980, 26)):
        b += f'<ellipse cx="{gx}" cy="{gy}" rx="{r_}" ry="{r_ * .35:.0f}" fill="#b9a8ff" opacity=".35" transform="rotate(-20 {gx} {gy})" filter="url(#b3)"/>'
    b += '<rect width="1920" height="1080" fill="url(#sunHalo)"/>'
    HW = 150
    # ---- ladder rails (behind the objects), glowing gold ----
    ys = [1120, -40]
    for side in (-1, 1):
        x0, x1 = lx(ys[0]) + side * HW, lx(ys[1]) + side * HW
        b += f'<path d="M{x0:.0f} {ys[0]} L{x1:.0f} {ys[1]}" stroke="#ffd27a" stroke-width="44" opacity=".25" filter="url(#b12)"/>'
        b += f'<path d="M{x0:.0f} {ys[0]} L{x1:.0f} {ys[1]}" stroke="#3a2406" stroke-width="26"/>'
        b += f'<path d="M{x0:.0f} {ys[0]} L{x1:.0f} {ys[1]}" stroke="url(#railA)" stroke-width="18"/>'
        b += f'<path d="M{x0 - 4:.0f} {ys[0]} L{x1 - 4:.0f} {ys[1]}" stroke="#fffbe0" stroke-width="4" opacity=".8"/>'
    # small rungs everywhere, big glowing "tier" rungs under each object
    tiers = (740, 470, 200)
    for y in list(range(870, -40, -90)) + [1060, 965]:
        if any(abs(y - t) < 40 for t in tiers): continue
        x = lx(y)
        b += f'<path d="M{x - HW:.0f} {y} L{x + HW:.0f} {y}" stroke="#3a2406" stroke-width="16" stroke-linecap="round"/><path d="M{x - HW:.0f} {y} L{x + HW:.0f} {y}" stroke="#d9a94e" stroke-width="9" stroke-linecap="round"/>'
    for y in tiers:
        x = lx(y)
        b += f'<path d="M{x - HW - 30:.0f} {y} L{x + HW + 30:.0f} {y}" stroke="#ffe39a" stroke-width="40" opacity=".45" filter="url(#b12)"/>'
        b += f'<path d="M{x - HW - 24:.0f} {y} L{x + HW + 24:.0f} {y}" stroke="#3a2406" stroke-width="26" stroke-linecap="round"/>'
        b += f'<path d="M{x - HW - 24:.0f} {y} L{x + HW + 24:.0f} {y}" stroke="url(#railA)" stroke-width="16" stroke-linecap="round"/>'
        b += f'<path d="M{x - HW - 18:.0f} {y - 4} L{x + HW + 18:.0f} {y - 4}" stroke="#fffbe0" stroke-width="3" opacity=".85"/>'
    # ---- tier 1: the planet ----
    ex, ey = lx(740), 740 - 112
    e = f'<g transform="translate({ex:.0f} {ey})">'
    e += '<circle r="128" fill="#7fc4ff" opacity=".35" filter="url(#b12)"/>'
    e += '<circle r="104" fill="url(#earthA)"/>'
    e += '<g clip-path="url(#eclip)">'
    for (cx_, cy_, rx_, ry_, r_) in ((-40, -30, 46, 30, -20), (-10, 10, 26, 40, 15), (38, -50, 40, 18, 10), (50, 30, 30, 22, -30), (-70, 50, 30, 16, 20), (10, 80, 50, 14, 0)):
        e += f'<ellipse cx="{cx_}" cy="{cy_}" rx="{rx_}" ry="{ry_}" transform="rotate({r_} {cx_} {cy_})" fill="#5aa04a"/><ellipse cx="{cx_ - 6}" cy="{cy_ - 5}" rx="{rx_ * .6:.0f}" ry="{ry_ * .5:.0f}" transform="rotate({r_} {cx_} {cy_})" fill="#8cc068" opacity=".7"/>'
    e += '<ellipse cx="0" cy="-96" rx="70" ry="18" fill="#f4fbff" opacity=".9"/>'
    for k in range(7):
        cy_ = -70 + k * 24
        e += f'<path d="M{-100 + k * 7} {cy_} q50 {-12 + k * 3} {110 + k * 6} 4" stroke="#ffffff" stroke-width="{rnd.uniform(5, 9):.0f}" fill="none" opacity=".55" stroke-linecap="round"/>'
    e += '<path d="M20 -110 A110 110 0 0 1 20 110 A70 110 0 0 0 20 -110" fill="#020818" opacity=".55" transform="translate(28 0)"/>'
    for _ in range(26):   # city lights on the night side
        a = rnd.uniform(-1.1, 1.1); r_ = rnd.uniform(40, 98)
        e += f'<circle cx="{r_ * math.cos(a) + 18:.0f}" cy="{r_ * math.sin(a):.0f}" r="{rnd.uniform(1.4, 2.8):.1f}" fill="#ffd27a"/>'
    e += '</g><circle r="104" fill="none" stroke="#bfe6ff" stroke-width="5" opacity=".8"/>'
    e += '<path d="M-82 -56 A100 100 0 0 1 -30 -96" fill="none" stroke="#fff" stroke-width="6" opacity=".7" stroke-linecap="round"/></g>'
    b += e
    # ---- tier 2: the star ----
    sx_, sy_ = lx(470), 470 - 138
    s = f'<g transform="translate({sx_:.0f} {sy_})">'
    s += '<circle r="230" fill="#ffb54a" opacity=".35" filter="url(#b50)"/><circle r="165" fill="#ffd27a" opacity=".55" filter="url(#b24)"/>'
    for k in range(18):   # corona rays
        a = k * 20 + rnd.uniform(-6, 6); L = rnd.uniform(175, 235)
        s += f'<path d="M0 0 L{L * math.cos(math.radians(a - 3)):.0f} {L * math.sin(math.radians(a - 3)):.0f} L{L * math.cos(math.radians(a + 3)):.0f} {L * math.sin(math.radians(a + 3)):.0f}Z" fill="#ffe7a8" opacity=".3" filter="url(#b6)"/>'
    s += '<g transform="scale(126)"><circle r="1" fill="url(#sunA)"/></g>'
    for _ in range(80):   # granulation
        a = rnd.uniform(0, 2 * math.pi); r_ = 120 * math.sqrt(rnd.random())
        s += f'<circle cx="{r_ * math.cos(a):.0f}" cy="{r_ * math.sin(a):.0f}" r="{rnd.uniform(4, 10):.0f}" fill="#fff6cf" opacity="{rnd.uniform(.15, .4):.2f}"/>'
    s += '<circle cx="34" cy="28" r="9" fill="#c0601a" opacity=".6"/><circle cx="48" cy="20" r="5" fill="#c0601a" opacity=".5"/>'
    s += '<path d="M-110 -60 q-50 -70 10 -88" fill="none" stroke="#ffcf6a" stroke-width="9" opacity=".75" filter="url(#b2)"/>'
    s += '<path d="M96 70 q70 20 50 -40" fill="none" stroke="#ffcf6a" stroke-width="7" opacity=".6" filter="url(#b2)"/></g>'
    b += s
    # ---- tier 3: the galaxy (wider than the ladder) ----
    b += galaxy(lx(200) + 20, 200 - 92, 300, 96, -12, rnd)
    b += spark(1150, 640, 18) + spark(1760, 380, 20) + spark(1640, 820, 14) + spark(800, 600, 14, '#fff6d6', .6)
    # ---- the frog, clinging to a low rung, looking up ----
    ry = 870
    fx, fy, fs = lx(ry) - 10, ry + 96 * 2.3, 2.3
    b += f'<circle cx="{fx}" cy="{fy - 150}" r="220" fill="#9fe0a0" opacity=".12" filter="url(#b24)"/>'
    b += frog(fx, fy, fs, rot=0, look=(4, -7), mouth='O',
              armL='M-34 -40 q-20 -30 -14 -56', armR='M38 -40 q18 -30 12 -56',
              legs=((-18, -6, -34, 2, 20), (20, -10, 40, -22, -30)))
    # gripping hands over the rung
    for hx in (-48, 50):
        b += f'<circle cx="{fx + hx * fs:.0f}" cy="{ry + 2}" r="15" fill="{GREEN}" stroke="{INK}" stroke-width="7"/>'
    b += '<rect width="1920" height="1080" fill="url(#vigA)"/>'
    lines = [('ONLY', 170, 'w'), ('TYPE <span class="g">0.7</span>', 230, 'w')]
    return page('#0b0820', svg(d, b), lines, outline='#07051a', top=46)


# =========================== B: binary sunset (Star Wars homage) ===========================
def dune(pts):
    return 'M' + ' L'.join(f'{x:.0f} {y:.0f}' for x, y in pts)


def make_B():
    rnd = random.Random(19)
    d = FILTERS
    d += lin('skyB', [(0, '#1f2a5a'), (.35, '#6a3f6e'), (.62, '#e0784a'), (.78, '#ffc27a'), (1, '#ffe6b0')])
    d += rad('glowB', 1240, 640, 900, [(0, '#fff0c0', .6), (.3, '#ffb060', .25), (1, '#000', 0)])
    d += rad('sun1', 0, 0, 1, [(0, '#ffffff', 1), (.5, '#fff6d0', 1), (1, '#ffd27a', 1)])
    d += rad('sun2', 0, 0, 1, [(0, '#fffbe8', 1), (.5, '#ffd27a', 1), (1, '#ff9a3a', 1)])
    d += lin('duneFar', [(0, '#c9875a'), (1, '#8a4f3a')])
    d += lin('duneMid', [(0, '#a8613e'), (1, '#5a2f28')])
    d += lin('duneNear', [(0, '#6a3a2c'), (1, '#24120f')])
    d += lin('panel', [(0, '#fff3c8'), (.4, '#e8b04a'), (1, '#6a4410')], x2=1, y2=1)
    d += rad('vigB', 960, 540, 1150, [(0, '#000', 0), (.72, '#000', 0), (1, '#000', .5)])
    b = '<rect width="1920" height="1080" fill="url(#skyB)"/>'
    b += starfield(rnd, 90, (0, 0, 1920, 330), '#fff4e8')
    b += '<rect width="1920" height="1080" fill="url(#glowB)"/>'
    # thin cloud streaks lit from below
    for k in range(9):
        y = rnd.uniform(380, 560); x = rnd.uniform(500, 1900); w = rnd.uniform(160, 420)
        b += f'<path d="M{x:.0f} {y:.0f} q{w / 2:.0f} -8 {w:.0f} 0" stroke="#ffd2a0" stroke-width="{rnd.uniform(3, 7):.0f}" fill="none" opacity=".45" stroke-linecap="round"/>'
    HZ = 735
    # ---- sun 1 (plain, smaller) ----
    s1x, s1y, s1r = 1000, 650, 62
    b += f'<circle cx="{s1x}" cy="{s1y}" r="{s1r * 2.6:.0f}" fill="#fff0c0" opacity=".45" filter="url(#b24)"/>'
    b += f'<g transform="translate({s1x} {s1y}) scale({s1r})"><circle r="1" fill="url(#sun1)"/></g>'
    # ---- sun 2 (bigger), wrapped in a swarm of collectors ----
    cx, cy, R = 1390, 545, 128
    b += f'<circle cx="{cx}" cy="{cy}" r="{R * 3:.0f}" fill="#ffc46a" opacity=".4" filter="url(#b50)"/>'
    # light leaking between panels as rays
    for k in range(14):
        a = k * 360 / 14 + rnd.uniform(-8, 8); L = rnd.uniform(300, 430)
        b += f'<path d="M{cx} {cy} L{cx + L * math.cos(math.radians(a - 2)):.0f} {cy + L * math.sin(math.radians(a - 2)):.0f} L{cx + L * math.cos(math.radians(a + 2)):.0f} {cy + L * math.sin(math.radians(a + 2)):.0f}Z" fill="#fff0c0" opacity=".22" filter="url(#b3)"/>'
    b += f'<g transform="translate({cx} {cy}) scale({R})"><circle r="1" fill="url(#sun2)"/></g>'
    # orbital rings of panels: back halves first, then sun dims, then front halves
    rings = [(R * 1.75, R * .34, -14), (R * 1.6, R * .5, 30), (R * 1.95, R * .26, 6)]
    def panels(front):
        o = ''
        for i, (rx_, ry_, rot) in enumerate(rings):
            ca, sa = math.cos(math.radians(rot)), math.sin(math.radians(rot))
            o += f'<g transform="translate({cx} {cy}) rotate({rot})"><path d="M{-rx_:.0f} 0 A{rx_:.0f} {ry_:.0f} 0 0 {0 if front else 1} {rx_:.0f} 0" fill="none" stroke="#ffe7a8" stroke-width="2" opacity=".55"/></g>'
            n = 26
            for k in range(n):
                t = 2 * math.pi * (k + .5 * (i % 2)) / n
                u, v = rx_ * math.cos(t), ry_ * math.sin(t)
                if (v > 0) != front: continue
                px, py = cx + u * ca - v * sa, cy + u * sa + v * ca
                w = 15 + 5 * math.sin(t) * (1 if front else -1)
                ang = rot + math.degrees(t) * .4
                lit = 'url(#panel)' if front else '#7a4a1e'
                o += f'<rect x="{px - w / 2:.1f}" y="{py - w * .32:.1f}" width="{w:.1f}" height="{w * .64:.1f}" rx="2" transform="rotate({ang:.0f} {px:.1f} {py:.1f})" fill="{lit}" stroke="#2a1606" stroke-width="2.2"/>'
                if front and rnd.random() < .35:
                    o += spark(round(px), round(py), rnd.choice([7, 9, 11]), '#fffbe8', .9)
        return o
    b += panels(False)
    b += panels(True)
    # ---- dunes ----
    far = [(0, HZ)] + [(x, HZ - 18 * math.sin(x / 210) - 10 * math.sin(x / 77)) for x in range(0, 1941, 30)] + [(1940, 1080), (0, 1080)]
    b += f'<path d="{dune(far)}Z" fill="url(#duneFar)"/>'
    b += f'<path d="M0 {HZ - 2} ' + ' '.join(f'L{x} {HZ - 18 * math.sin(x / 210) - 10 * math.sin(x / 77) - 2:.0f}' for x in range(0, 1941, 30)) + '" stroke="#ffd09a" stroke-width="4" fill="none" opacity=".7"/>'
    # small dome homestead far left
    b += '<path d="M250 742 a46 34 0 0 1 92 0z" fill="#b97a52" stroke="#5a2f22" stroke-width="3"/><rect x="284" y="724" width="22" height="18" rx="6" fill="#3a1e18"/><path d="M262 726 a40 30 0 0 1 34 -20" stroke="#ffd8a8" stroke-width="3" fill="none" opacity=".7"/>'
    b += '<path d="M392 742 L392 690 M380 700 L404 700 M384 714 L400 714" stroke="#4a2820" stroke-width="5"/>'
    mid = [(0, 820)] + [(x, 800 + 40 * math.sin(x / 300 + 1) + 14 * math.sin(x / 110)) for x in range(0, 1941, 30)] + [(1940, 1080), (0, 1080)]
    b += f'<path d="{dune(mid)}Z" fill="url(#duneMid)"/>'
    b += f'<path d="M0 {mid[1][1]:.0f} ' + ' '.join(f'L{x:.0f} {y:.0f}' for x, y in mid[1:-2]) + '" stroke="#f0a070" stroke-width="3" fill="none" opacity=".55"/>'
    # near dune: a ridge rising to the left where the frog stands
    near = [(x, 880 + 170 * ((x - 560) / 900) ** 2 + 8 * math.sin(x / 60)) for x in range(-20, 1960, 20)]
    b += f'<path d="M-20 1080 L{dune(near)[1:]} L1960 1080Z" fill="url(#duneNear)"/>'
    b += f'<path d="{dune(near)}" stroke="#ffb27a" stroke-width="5" fill="none" opacity=".75"/>'
    for _ in range(40):   # wind ripples on the lit side
        x = rnd.uniform(0, 1400); y = 880 + 170 * ((x - 560) / 900) ** 2 + rnd.uniform(20, 160)
        if corner(x, y): continue
        b += f'<path d="M{x:.0f} {y:.0f} q30 -6 60 0" stroke="#c07a52" stroke-width="2.5" fill="none" opacity=".45"/>'
    # ---- frog on the ridge, side-on, gazing at the two suns ----
    fx, fy, fs = 560, 884, 2.5
    b += f'<path d="M{fx} {fy + 4} L{fx - 520} {fy + 40} L{fx - 520} {fy + 70} Z" fill="#0e0605" opacity=".45" filter="url(#b6)"/>'   # long shadow
    b += f'<circle cx="{fx + 10}" cy="{fy - 140}" r="210" fill="#ffe0b0" opacity=".14" filter="url(#b24)"/>'
    b += frog(fx, fy, fs, look=(6, -2), mouth='o', robe=True, shadow=True,
              armL='M-34 -22 q-10 14 -6 26', armR='M38 -22 q18 0 26 -18')
    # warm rim light on the sunward edge of the frog
    b += f'<path d="M{fx + 6 * fs} {fy - 70 * fs} q{40 * fs} -2 {42 * fs} {62 * fs}" stroke="#ffd59a" stroke-width="5" fill="none" opacity=".8"/>'
    b += spark(1720, 330, 18) + spark(800, 520, 14, '#fff6d6', .7) + spark(1640, 760, 14)
    b += '<rect width="1920" height="1080" fill="url(#vigB)"/>'
    lines = [('SWALLOW', 200, 'w'), ('A <span class="g">STAR?</span>', 230, 'w')]
    return page('#1f2a5a', svg(d, b), lines, outline='#1a0c18', top=46)


# =========================== C: the listening field (Contact homage) ===========================
def dish(cx, cy, s, sky=True):
    """radio dish facing up-left; (cx, cy) = dish centre, s = scale (1 = rim rx 270)."""
    nx, ny = -.42, -.91          # face normal (projected)
    ux, uy = .91, -.42           # rim long axis
    rx, ry = 270 * s, 120 * s
    o = ''
    # pedestal + yoke
    bx, by = cx + 60 * s * .42, cy + 60 * s * .91
    o += f'<path d="M{bx - 34 * s:.0f} {by:.0f} L{bx - 60 * s:.0f} {by + 340 * s:.0f} L{bx + 60 * s:.0f} {by + 340 * s:.0f} L{bx + 34 * s:.0f} {by:.0f}Z" fill="#20263a" stroke="#0a0c16" stroke-width="{max(2, 4 * s):.1f}"/>'
    o += f'<path d="M{bx - 26 * s:.0f} {by + 10 * s:.0f} L{bx - 44 * s:.0f} {by + 330 * s:.0f}" stroke="#ff9a7a" stroke-width="{max(1.5, 5 * s):.1f}" opacity=".55"/>'
    o += f'<rect x="{bx - 74 * s:.0f}" y="{by + 330 * s:.0f}" width="{148 * s:.0f}" height="{22 * s:.0f}" fill="#141826"/>'
    # back shell
    o += f'<ellipse cx="{cx - nx * 40 * s:.0f}" cy="{cy - ny * 40 * s:.0f}" rx="{rx * .96:.0f}" ry="{ry * 1.25:.0f}" transform="rotate(-25 {cx - nx * 40 * s:.0f} {cy - ny * 40 * s:.0f})" fill="#2a3048" stroke="#0a0c16" stroke-width="{max(2, 5 * s):.1f}"/>'
    # concave face
    o += f'<ellipse cx="{cx}" cy="{cy}" rx="{rx:.0f}" ry="{ry:.0f}" transform="rotate(-25 {cx} {cy})" fill="url(#dishFace)" stroke="#0a0c16" stroke-width="{max(2, 5 * s):.1f}"/>'
    for k in range(16):   # panel ribs
        t = 2 * math.pi * k / 16
        px = cx + rx * math.cos(t) * ux - ry * math.sin(t) * ux * 0 + ry * math.sin(t) * (-uy) * 0
        # rotated ellipse point
        ca, sa = math.cos(math.radians(-25)), math.sin(math.radians(-25))
        ex_, ey_ = rx * math.cos(t), ry * math.sin(t)
        px, py = cx + ex_ * ca - ey_ * sa, cy + ex_ * sa + ey_ * ca
        o += f'<path d="M{cx} {cy} L{px:.0f} {py:.0f}" stroke="#4a5272" stroke-width="{max(1, 2.4 * s):.1f}" opacity=".8"/>'
    for f in (.4, .7):
        o += f'<ellipse cx="{cx}" cy="{cy}" rx="{rx * f:.0f}" ry="{ry * f:.0f}" transform="rotate(-25 {cx} {cy})" fill="none" stroke="#4a5272" stroke-width="{max(1, 2.4 * s):.1f}" opacity=".8"/>'
    # rim highlight (dusk light from the lower left)
    o += f'<ellipse cx="{cx}" cy="{cy}" rx="{rx:.0f}" ry="{ry:.0f}" transform="rotate(-25 {cx} {cy})" fill="none" stroke="#ffb08a" stroke-width="{max(1.5, 5 * s):.1f}" stroke-dasharray="{rx * 1.6:.0f} {rx * 9:.0f}" stroke-dashoffset="{-rx * 2.4:.0f}" opacity=".9"/>'
    # feed: tripod to the focus
    fx, fy = cx + nx * 230 * s, cy + ny * 230 * s
    ca, sa = math.cos(math.radians(-25)), math.sin(math.radians(-25))
    for t in (math.pi * .5, math.pi * 1.2, math.pi * 1.8):
        ex_, ey_ = rx * .92 * math.cos(t), ry * .92 * math.sin(t)
        px, py = cx + ex_ * ca - ey_ * sa, cy + ex_ * sa + ey_ * ca
        o += f'<path d="M{px:.0f} {py:.0f} L{fx:.0f} {fy:.0f}" stroke="#0c0f1a" stroke-width="{max(1.5, 7 * s):.1f}"/><path d="M{px:.0f} {py:.0f} L{fx:.0f} {fy:.0f}" stroke="#5a6488" stroke-width="{max(.8, 2.5 * s):.1f}"/>'
    o += f'<rect x="{fx - 18 * s:.0f}" y="{fy - 24 * s:.0f}" width="{36 * s:.0f}" height="{48 * s:.0f}" rx="{6 * s:.0f}" transform="rotate(-25 {fx:.0f} {fy:.0f})" fill="#30364e" stroke="#0a0c16" stroke-width="{max(1.5, 4 * s):.1f}"/>'
    if sky:
        o += f'<circle cx="{fx:.0f}" cy="{fy:.0f}" r="{5 * s:.1f}" fill="#ff5a4a"/><circle cx="{fx:.0f}" cy="{fy:.0f}" r="{16 * s:.1f}" fill="#ff5a4a" opacity=".4" filter="url(#b6)"/>'
    return o


def make_C():
    rnd = random.Random(29)
    d = FILTERS
    d += lin('skyC', [(0, '#050a22'), (.4, '#13205a'), (.62, '#4a2f78'), (.74, '#c0507a'), (.82, '#ff9a6a'), (1, '#ffcf8a')])
    d += lin('dishFace', [(0, '#b8c2e0'), (.5, '#6c7698'), (1, '#353c58')], x2=1, y2=1)
    d += lin('groundC', [(0, '#2a1e3a'), (.4, '#140e22'), (1, '#07050e')])
    d += lin('carC', [(0, '#5a3a4a'), (1, '#1e1420')])
    d += rad('vigC', 960, 540, 1150, [(0, '#000', 0), (.72, '#000', 0), (1, '#000', .55)])
    b = '<rect width="1920" height="1080" fill="url(#skyC)"/>'
    # Milky Way band across the upper right
    mw = ''
    for _ in range(900):
        t = rnd.random(); x = 600 + 1400 * t; y = 520 - 560 * t + rnd.gauss(0, 55)
        mw += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{rnd.choice([.9, 1.3, 1.8, 2.4])}" fill="{rnd.choice(["#fff", "#e0e8ff", "#ffe8f4"])}" opacity="{rnd.uniform(.2, .9):.2f}"/>'
    b += '<path d="M600 520 L2000 -40" stroke="#b8a8ff" stroke-width="170" opacity=".16" filter="url(#b50)"/>'
    b += '<path d="M640 500 L1980 -30" stroke="#ffd6f0" stroke-width="60" opacity=".12" filter="url(#b24)"/>'
    b += mw + starfield(rnd, 220, (0, 0, 1920, 640), '#eef2ff')
    HZ = 790
    b += f'<ellipse cx="560" cy="{HZ}" rx="900" ry="120" fill="#ffd09a" opacity=".45" filter="url(#b50)"/>'
    # distant mountains
    m = [(x, HZ - 30 - 40 * abs(math.sin(x / 260)) - 18 * math.sin(x / 90)) for x in range(-20, 1961, 30)]
    b += f'<path d="M-20 {HZ + 10} L' + ' L'.join(f'{x:.0f} {y:.0f}' for x, y in m) + f' L1960 {HZ + 10}Z" fill="#3a2a58" opacity=".85"/>'
    b += f'<rect x="0" y="{HZ}" width="1920" height="{1080 - HZ}" fill="url(#groundC)"/>'
    b += f'<path d="M0 {HZ} L1920 {HZ}" stroke="#ffb08a" stroke-width="3" opacity=".5"/>'
    # row of dishes receding to the left, all aimed at the same patch of sky
    for x, s in ((150, .12), (260, .15), (390, .19), (560, .25), (790, .34)):
        b += dish(x, HZ - 360 * s, s)
    # the big foreground dish
    b += '<circle cx="1440" cy="410" r="330" fill="#9a8aff" opacity=".12" filter="url(#b50)"/>'
    b += dish(1430, 400, 1.08)
    # road / gravel
    b += f'<path d="M260 1080 L700 {HZ + 40} L780 {HZ + 40} L900 1080Z" fill="#1c1428" opacity=".9"/>'
    for _ in range(80):
        x = rnd.uniform(0, 1500); y = rnd.uniform(HZ + 20, 1075)
        b += f'<path d="M{x:.0f} {y:.0f} l{rnd.uniform(6, 16):.0f} 0" stroke="#6a4a6a" stroke-width="2" opacity=".5"/>'
    # ---- old car seen side-on, frog sitting on the hood ----
    cxo, cyo = 300, 990   # car rear-bottom
    car = f'<g transform="translate({cxo} {cyo})">'
    car += '<ellipse cx="300" cy="18" rx="330" ry="22" fill="#000" opacity=".5" filter="url(#b6)"/>'
    car += '<path d="M0 -20 L0 -110 Q10 -130 40 -132 L120 -136 L190 -222 Q205 -236 230 -236 L380 -236 Q404 -236 418 -220 L470 -140 L600 -128 Q640 -122 646 -96 L650 -20 Z" fill="url(#carC)" stroke="#0a0610" stroke-width="6"/>'
    car += '<path d="M214 -140 L246 -216 L322 -216 L322 -140Z M338 -140 L338 -216 L392 -216 L436 -140Z" fill="#ff9a7a" opacity=".35" stroke="#0a0610" stroke-width="4"/>'
    car += '<path d="M40 -128 L470 -136 L600 -124" stroke="#ffb69a" stroke-width="4" fill="none" opacity=".6"/>'
    car += '<path d="M10 -70 L640 -70" stroke="#d07a7a" stroke-width="3" opacity=".5"/>'
    for wx in (130, 520):
        car += f'<circle cx="{wx}" cy="-16" r="52" fill="#0c0810" stroke="#000" stroke-width="5"/><circle cx="{wx}" cy="-16" r="24" fill="#8a7a90"/><circle cx="{wx}" cy="-16" r="10" fill="#2a2030"/>'
        car += f'<path d="M{wx - 70} -40 Q{wx} -100 {wx + 70} -40" fill="none" stroke="#0a0610" stroke-width="8"/>'
    car += '<rect x="628" y="-108" width="20" height="18" rx="4" fill="#ffe9b0"/><path d="M640 -100 L760 -140 L760 -60Z" fill="#ffe9b0" opacity=".12"/>'
    car += '</g>'
    b += car
    fx, fy, fs = cxo + 560, cyo - 122, 2.3
    b += f'<circle cx="{fx}" cy="{fy - 140}" r="200" fill="#c0d4ff" opacity=".13" filter="url(#b24)"/>'
    b += frog(fx, fy, fs, look=(4, -8), mouth='O', phones=True,
              armL='M-34 -22 q-20 -16 -6 -50', armR='M38 -22 q22 -12 12 -48',
              legs=((-18, -6, -30, 26, 60), (20, -6, 20, 30, 70)))
    # tiny laptop beside the frog, flat line on its screen = no signal
    lpx, lpy = fx - 170, fy - 4
    b += f'<path d="M{lpx} {lpy} l90 0 l14 -6 l-90 0z" fill="#3a3f52" stroke="#0a0610" stroke-width="3"/><path d="M{lpx + 14} {lpy - 6} l-14 -60 l90 0 l14 60z" fill="#1a2240" stroke="#0a0610" stroke-width="3"/>'
    b += f'<path d="M{lpx + 6} {lpy - 34} l86 0" stroke="#7affc8" stroke-width="3"/><path d="M{lpx + 6} {lpy - 34} l86 0" stroke="#7affc8" stroke-width="9" opacity=".3" filter="url(#b3)"/>'
    b += spark(1120, 120, 20) + spark(1820, 320, 16) + spark(980, 620, 14, '#fff6d6', .7) + spark(1700, 680, 12)
    b += '<rect width="1920" height="1080" fill="url(#vigC)"/>'
    lines = [('THE SKY', 170, 'w'), ('IS <span class="g">SILENT</span>', 200, 'w')]
    return page('#050a22', svg(d, b), lines, outline='#050716', top=50)


for n, fn in (('A', make_A), ('B', make_B), ('C', make_C)):
    open(os.path.join(HERE, f'{n}.html'), 'w').write(fn())
print('ok')
