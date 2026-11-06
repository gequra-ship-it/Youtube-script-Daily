# Shorts thumbnails (guideline 16-9): ONE per short, written to videos/trilobite-extinction-shortN/thumb/A.html.
# Run: python3 videos/trilobite-extinction/thumb/make_shorts.py [1 2 3 4 5]   (reuses the frog / trilobite helpers of make.py here)
# 1 EYES MADE OF ROCK     intuitive: microscope field (polarised light) through a thin section of a phacopid eye: doublet calcite lens
#                         + lower bowl focusing light rays. short1 S01 ("eyes made of literal rock"), S08 (two-layer lens), S11 (slice through).
# 2 LONGER THAN DINOSAURS intuitive: rock-strata 'time pillars' as a podium: trilobite (crowned) on the tallest, T. rex skeleton on a shorter
#                         one, a tiny human on a sliver. short2 S02-S05 (300 thousand / 165 million / 270 million years).
# 3 A BALL OF ARMOR       intuitive: enrolled trilobite (side view) in front of the open jaws of an armoured jawed fish, sea scorpion on the
#                         floor, the frog holds a pill bug. short3 S01, S02, S06, S08, S11 ("A ball of armor").
# 4 OCEAN TOO ACIDIC      intuitive: a trilobite fizzing away like a tablet inside a giant beaker of acid-green sea, Siberian fissure
#                         eruptions behind. short4 S01 ("too acidic"), S04-S07.
# 5 ONLY ONE SURVIVED     intuitive: a pruned family tree at night, every branch sawn off with ghost fossils of spiny / spade-nosed
#                         trilobites, one living branch with a small oval proetid. short5 S04-S06, S11.
import os, sys, math, random
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, '..', '..', '..', 'tools'))
from make import (frog, trilo_dorsal, tri_paint, hexlenses, FILTERS, P, poly, limb, INK, GREEN)
from thumb_lib import page, svg, lin, rad, spark

VID = os.path.join(HERE, '..', '..')
NS = 'vector-effect="non-scaling-stroke"'


def goggles(col='#3a3a44', glass='#bfe8ff'):
    return (f'<path d="M-36 -64 L-48 -60 M40 -64 L52 -60" stroke-width="5" fill="none"/>'
            + ''.join(f'<circle cx="{ex}" cy="-66" r="18" fill="{glass}" fill-opacity=".22" stroke="{col}" stroke-width="5.5"/>'
                      f'<path d="M{ex - 10} -74 q6 -6 14 -6" stroke="#fff" stroke-width="3" fill="none" opacity=".85"/>' for ex in (-10, 22))
            + f'<path d="M8 -68 q4 -4 2 0" stroke="{col}" stroke-width="5" fill="none"/>')


def bubbles(rnd, n, x0, x1, y0, y1, col='#e8fbff', rmin=3, rmax=12, op=.7, skip=None):
    o = ''
    for _ in range(n):
        x, y = rnd.uniform(x0, x1), rnd.uniform(y0, y1)
        if skip and skip(x, y):
            continue
        r_ = rnd.uniform(rmin, rmax)
        o += (f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r_:.1f}" fill="{col}" fill-opacity=".1" stroke="{col}" stroke-width="{max(1.5, r_ * .22):.1f}" opacity="{op}"/>'
              f'<circle cx="{x - r_ * .35:.1f}" cy="{y - r_ * .35:.1f}" r="{r_ * .25:.1f}" fill="#fff" opacity="{op}"/>')
    return o


def taper(x0, y0, x1, y1, w0, w1, bend=0):
    """tapered branch / bone as a closed path, bend = sideways bulge of the midline in px"""
    dx, dy = x1 - x0, y1 - y0; L = math.hypot(dx, dy) or 1; nx, ny = -dy / L, dx / L
    mx, my = (x0 + x1) / 2 + nx * bend, (y0 + y1) / 2 + ny * bend; wm = (w0 + w1) / 4
    return (f'M{x0 + nx * w0 / 2:.1f} {y0 + ny * w0 / 2:.1f} Q{mx + nx * wm:.1f} {my + ny * wm:.1f} {x1 + nx * w1 / 2:.1f} {y1 + ny * w1 / 2:.1f} '
            f'L{x1 - nx * w1 / 2:.1f} {y1 - ny * w1 / 2:.1f} Q{mx - nx * wm:.1f} {my - ny * wm:.1f} {x0 - nx * w0 / 2:.1f} {y0 - ny * w0 / 2:.1f} Z')


# ================= 1: EYES MADE OF ROCK =================
def lens(cx, cy, w, rot, rays=True, bright=1.0, idn='1'):
    up = ('M-.5 0 C-.45 -.30 -.22 -.42 0 -.42 C.22 -.42 .45 -.30 .5 0 C.40 .02 .30 .02 .22 .06 C.12 .14 .06 .16 0 .16 '
          'C-.06 .16 -.12 .14 -.22 .06 C-.30 .02 -.40 .02 -.5 0 Z')
    bowl = ('M-.40 .012 C-.30 .02 -.24 .05 -.22 .06 C-.12 .14 -.06 .16 0 .16 C.06 .16 .12 .14 .22 .06 C.24 .05 .30 .02 .40 .012 '
            'C.36 .22 .18 .33 0 .33 C-.18 .33 -.36 .22 -.40 .012 Z')
    g = f'<g transform="translate({cx} {cy}) rotate({rot}) scale({w})">'
    g += f'<ellipse cx="0" cy="-.05" rx=".62" ry=".52" fill="#fff1c0" opacity="{.25 * bright:.2f}" filter="url(#b24)"/>'
    g += f'<path d="{bowl}" fill="url(#bowl1)" stroke="#0c1820" stroke-width="5" {NS}/>'
    g += f'<path d="{up}" fill="url(#calc1)" stroke="#2a1606" stroke-width="5" {NS}/>'
    # interference fringes inside the calcite (polarised light), clipped to the upper unit
    g += f'<clipPath id="cl{idn}"><path d="{up}"/></clipPath><g clip-path="url(#cl{idn})">'
    for k, c in enumerate(['#ff7fc0', '#7fe0ff', '#fff07a', '#b48aff', '#7fffb0', '#ff9f6a']):
        g += f'<ellipse cx="0" cy=".22" rx="{.18 + k * .085:.3f}" ry="{.13 + k * .07:.3f}" fill="none" stroke="{c}" stroke-width="7" {NS} opacity=".28"/>'
    g += '</g>'
    # bowl fringes
    g += f'<path d="M-.30 .10 C-.16 .24 .16 .24 .30 .10" fill="none" stroke="#9ff6ff" stroke-width="4" {NS} opacity=".55"/>'
    g += f'<path d="M-.44 -.10 C-.38 -.30 -.2 -.40 -.02 -.40" fill="none" stroke="#fffbe8" stroke-width="7" {NS} stroke-linecap="round" opacity=".9"/>'
    if rays:
        fy = .78
        for k in range(7):
            t = (k - 3) / 3 * .34
            ys = -.42 * math.sqrt(max(0, 1 - (2 * t) ** 2)) * .98
            ray = f'M{t:.3f} -1.9 L{t:.3f} {ys:.3f} L0 {fy}'
            g += f'<path d="{ray}" fill="none" stroke="#fff6c8" stroke-width="14" {NS} opacity="{.18 * bright:.2f}" filter="url(#b6)"/>'
            g += f'<path d="{ray}" fill="none" stroke="#fffdf0" stroke-width="3.2" {NS} opacity="{.9 * bright:.2f}"/>'
            g += f'<path d="M0 {fy} L{-t * .55:.3f} {fy + .35}" fill="none" stroke="#fffdf0" stroke-width="2.4" {NS} opacity="{.35 * bright:.2f}"/>'
        g += f'<circle cx="0" cy="{fy}" r=".09" fill="#fff6c8" opacity="{.8 * bright:.2f}" filter="url(#b12)"/><circle cx="0" cy="{fy}" r=".03" fill="#fff"/>'
    return g + '</g>'


def make_1():
    rnd = random.Random(101)
    FX, FY, R = 1310, 548, 468
    d = FILTERS
    d += rad('bg1', 1310, 548, 1300, [(0, '#1c1830', 1), (.5, '#0e0c1a', 1), (1, '#040308', 1)])
    d += lin('pol1', [(0, '#3a1460'), (.35, '#7a2378'), (.62, '#2a4f8a'), (1, '#0c5a6a')], x2=.6, y2=1)
    d += lin('cut1', [(0, '#5a3418'), (.5, '#3a200e'), (1, '#1c0e06')])
    d += ('<radialGradient id="calc1" cx=".5" cy=".7" r=".75" fx=".42" fy=".45"><stop offset="0" stop-color="#fffbe6"/><stop offset=".35" stop-color="#ffe08a"/>'
          '<stop offset=".75" stop-color="#e09a3a"/><stop offset="1" stop-color="#8a4a14"/></radialGradient>')
    d += ('<radialGradient id="bowl1" cx=".5" cy=".2" r=".9"><stop offset="0" stop-color="#bff8ff"/><stop offset=".45" stop-color="#36b8d0"/>'
          '<stop offset="1" stop-color="#0c4a70"/></radialGradient>')
    d += lin('ring1', [(0, '#e8eef4'), (.3, '#8a96a4'), (.55, '#2a323c'), (1, '#6a7684')], x2=1, y2=1)
    d += ('<filter id="grain1" x="0" y="0" width="100%" height="100%"><feTurbulence type="fractalNoise" baseFrequency=".9" numOctaves="2" seed="4"/>'
          '<feColorMatrix type="matrix" values="0 0 0 0 .9  0 0 0 0 .7  0 0 0 0 .5  0 0 0 .55 -.18"/><feComposite in2="SourceGraphic" operator="in"/></filter>')
    d += f'<clipPath id="field1"><circle cx="{FX}" cy="{FY}" r="{R}"/></clipPath>'
    b = '<rect width="1920" height="1080" fill="url(#bg1)"/>'
    # dim lab light behind: microscope stage glow
    b += f'<circle cx="{FX}" cy="{FY}" r="{R + 140}" fill="#8a5aff" opacity=".22" filter="url(#b50)"/>'
    b += f'<circle cx="{FX}" cy="{FY}" r="{R + 60}" fill="#5ae0ff" opacity=".12" filter="url(#b24)"/>'
    for _ in range(40):
        b += f'<circle cx="{rnd.uniform(0, 1920):.0f}" cy="{rnd.uniform(0, 1080):.0f}" r="{rnd.choice([1.4, 2, 2.8])}" fill="#d8c8ff" opacity="{rnd.uniform(.1, .45):.2f}"/>'
    f = f'<g clip-path="url(#field1)">'
    f += f'<rect x="{FX - R}" y="{FY - R}" width="{2 * R}" height="{2 * R}" fill="url(#pol1)"/>'
    for cx, cy, rx, ry, c, op in ((1050, 260, 260, 120, '#ff5fb0', .35), (1580, 330, 240, 140, '#5fe0ff', .3), (1300, 140, 300, 90, '#ffd36a', .22),
                                  (1150, 880, 360, 160, '#3a1a6a', .5), (1560, 860, 260, 160, '#0a3a4a', .5)):
        f += f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="{c}" opacity="{op}" filter="url(#b50)"/>'
    # eye surface: band of cuticle (the cut section) arcing across the field, lenses embedded
    arc_top = [(x, 470 + ((x - FX) / 520) ** 2 * 120) for x in range(780, 1850, 20)]
    arc_bot = [(x, 700 + ((x - FX) / 520) ** 2 * 120) for x in range(1840, 770, -20)]
    f += f'<path d="{poly(arc_top + arc_bot)}" fill="url(#cut1)"/>'
    f += f'<path d="{poly(arc_top + arc_bot)}" fill="#fff" filter="url(#grain1)" opacity=".5"/>'
    f += f'<polyline points="{P(arc_top)}" fill="none" stroke="#ffcf8a" stroke-width="5" opacity=".7"/>'
    # inner (body) side below the cuticle: darker, with faint sclera fibres
    for k in range(6):
        y = 760 + k * 34
        f += f'<path d="M780 {y} Q{FX} {y + 60} 1850 {y}" fill="none" stroke="#c89aff" stroke-width="2" opacity=".18"/>'
    # side lenses (partly cut by the field) then the main lens
    f += lens(FX - 420, 566, 250, -16, bright=.55, idn='a')
    f += lens(FX + 420, 566, 250, 16, bright=.55, idn='b')
    f += lens(FX, 540, 360, 0, bright=1.0, idn='c')
    # reticle
    f += f'<path d="M{FX - R} {FY} L{FX - 120} {FY} M{FX + 220} {FY} L{FX + R} {FY} M{FX} {FY - R} L{FX} {FY - 360}" stroke="#e8f8ff" stroke-width="2" opacity=".3"/>'
    for k in range(-8, 9):
        f += f'<path d="M{FX + k * 40} {FY + R - 70} l0 {16 if k % 4 else 30}" stroke="#e8f8ff" stroke-width="2" opacity=".35"/>'
    f += f'<circle cx="{FX}" cy="{FY}" r="{R}" fill="none" stroke="#000" stroke-width="90" opacity=".45" filter="url(#b24)"/>'
    f += '</g>'
    b += f
    # eyepiece ring
    b += f'<circle cx="{FX}" cy="{FY}" r="{R + 22}" fill="none" stroke="#06050a" stroke-width="40"/>'
    b += f'<circle cx="{FX}" cy="{FY}" r="{R + 14}" fill="none" stroke="url(#ring1)" stroke-width="18"/>'
    b += f'<path d="M{FX - R * .62:.0f} {FY - R * .82:.0f} A{R + 14} {R + 14} 0 0 1 {FX + R * .3:.0f} {FY - R - 10:.0f}" fill="none" stroke="#fff" stroke-width="5" opacity=".7"/>'
    b += spark(FX - 150, 420, 24) + spark(FX + 330, 300, 20, '#e8fbff') + spark(FX - 330, 330, 16) + spark(1080, 220, 14, '#ffe8f8')
    # frog with goggles holding a thin-section slide up to the light
    slide = ('<g transform="translate(66 -74) rotate(-24) scale(.62)"><rect x="-44" y="-16" width="88" height="32" rx="3" fill="#dff4ff" fill-opacity=".45" stroke-width="3"/>'
             '<ellipse cx="0" cy="0" rx="16" ry="10" fill="#8a5a2a" stroke="none"/><circle cx="-4" cy="-2" r="3" fill="#ffd36a" stroke="none"/><circle cx="5" cy="1" r="3" fill="#ffd36a" stroke="none"/>'
             '<path d="M-38 -10 L-20 -10" stroke="#fff" stroke-width="3" opacity=".9"/></g>')
    b += '<ellipse cx="640" cy="860" rx="190" ry="200" fill="#a88aff" opacity=".18" filter="url(#b50)"/>'
    b += frog(620, 1052, 2.75, look=(9, -7), mouth='O', shadow=True, mid=goggles(), armR='M38 -22 q22 -10 30 -44', armL='M-34 -22 q-18 4 -22 24', front=slide)
    lines = [('EYES', 190, 'w'), ('MADE OF', 122, 'w'), ('ROCK', 230, 'y')]
    return page('#0e0c1a', svg(d, b), lines, outline='#0a0614', top=36)


# ================= 2: LONGER THAN DINOSAURS =================
def column(x0, x1, top, base, bands, rnd, light='#fff2c8'):
    w = x1 - x0; ry = w * .14
    o = f'<ellipse cx="{(x0 + x1) / 2}" cy="{base + 6}" rx="{w * .62:.0f}" ry="{ry * .9:.0f}" fill="#2a3a20" opacity=".45" filter="url(#b6)"/>'
    o += f'<path d="M{x0 - 30} {base + 4} L{x0 - 250} {base + 40} L{x0 - 230} {base + 64} L{x1 - 60} {base + 20}Z" fill="#1c2a14" opacity=".28" filter="url(#b6)"/>'
    H = base - top; y = base; n = len(bands)
    for k, c in enumerate(bands):
        h = H / n; yt = y - h
        o += f'<path d="M{x0} {yt} L{x0} {y} A{w / 2} {ry} 0 0 0 {x1} {y} L{x1} {yt} Z" fill="{c}" stroke="#2a1e14" stroke-width="3"/>'
        for _ in range(int(w / 40)):   # pebbles / fossil specks in the layer
            px, py = rnd.uniform(x0 + 10, x1 - 10), rnd.uniform(yt + 6, y - 4)
            o += f'<ellipse cx="{px:.0f}" cy="{py:.0f}" rx="{rnd.uniform(3, 9):.0f}" ry="{rnd.uniform(2, 4):.0f}" fill="#000" opacity=".16"/>'
        y = yt
    # lit right face, shaded left face (sun upper right)
    o += f'<path d="M{x0} {top} L{x0} {base} A{w / 2} {ry} 0 0 0 {x0 + w * .3} {base + ry * .92} L{x0 + w * .3} {top + ry * .92}Z" fill="#1a1020" opacity=".32"/>'
    o += f'<path d="M{x1 - w * .2} {top + ry * .97} L{x1 - w * .2} {base + ry * .97} A{w / 2} {ry} 0 0 0 {x1} {base} L{x1} {top}Z" fill="{light}" opacity=".22"/>'
    o += f'<path d="M{x1 - 4} {top} L{x1 - 4} {base}" stroke="{light}" stroke-width="6" opacity=".7"/>'
    o += f'<ellipse cx="{(x0 + x1) / 2}" cy="{top}" rx="{w / 2}" ry="{ry}" fill="#e8d4a8" stroke="#2a1e14" stroke-width="3"/>'
    o += f'<ellipse cx="{(x0 + x1) / 2 + w * .08}" cy="{top - ry * .1}" rx="{w * .34}" ry="{ry * .6}" fill="#fff6dc" opacity=".55"/>'
    return o


def trex(x, y, s):
    """T. rex skeleton facing left, hips at (x, y), s = px per unit; feet at about y + 1.33 s"""
    B, L = '#f6eedb', '#3a2c1c'
    def bone(d, w):
        return f'<path d="{d}" fill="none" stroke="{L}" stroke-width="{w + 6}" stroke-linecap="round" stroke-linejoin="round"/><path d="{d}" fill="none" stroke="{B}" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round"/>'
    def T(px, py):
        return x + px * s, y + py * s
    o = ''
    # far leg (darker)
    for fx_, shade in ((.16, '#c8bca0'), (0, None)):
        pts = [T(.02 + fx_, -.02), T(-.10 + fx_, .55), T(.12 + fx_, 1.05), T(.0 + fx_, 1.30)]
        d = 'M' + ' L'.join(f'{a:.0f} {b_:.0f}' for a, b_ in pts)
        if shade:
            o += f'<path d="{d}" fill="none" stroke="{L}" stroke-width="{.16 * s + 6:.0f}" stroke-linecap="round" stroke-linejoin="round"/><path d="{d}" fill="none" stroke="{shade}" stroke-width="{.16 * s:.0f}" stroke-linecap="round" stroke-linejoin="round"/>'
        else:
            o += bone(d, .17 * s)
        for k, (tx, ty) in enumerate(((-.30, 1.36), (-.24, 1.38), (-.16, 1.37))):
            a, b_ = T(fx_, 1.30); c, e = T(tx + fx_, ty)
            o += bone(f'M{a:.0f} {b_:.0f} L{c:.0f} {e:.0f}', .05 * s)
        a, b_ = T(fx_, 1.30); c, e = T(.14 + fx_, 1.36)
        o += bone(f'M{a:.0f} {b_:.0f} L{c:.0f} {e:.0f}', .045 * s)
    # spine: neck - back - tail
    sp = [(-1.30, -.42), (-1.10, -.52), (-.90, -.50), (-.60, -.42), (-.30, -.34), (0, -.28), (.40, -.26), (.80, -.24), (1.2, -.18), (1.6, -.08), (1.95, .04)]
    pts = [T(*p) for p in sp]
    # ribs
    for k in range(9):
        t = k / 8; px = -.92 + t * .78; py = -.48 + t * .17
        a, b_ = T(px, py); L_ = (.52 - .2 * abs(t - .35)) * s
        o += bone(f'M{a:.0f} {b_:.0f} q{-.10 * s:.0f} {L_ * .5:.0f} {.02 * s:.0f} {L_:.0f}', .035 * s)
    # gastralia hint
    a, b_ = T(-.95, .02); c, e = T(-.18, .08)
    o += f'<path d="M{a:.0f} {b_:.0f} Q{(a + c) / 2:.0f} {e + .12 * s:.0f} {c:.0f} {e:.0f}" fill="none" stroke="{L}" stroke-width="3" stroke-dasharray="10 8" opacity=".6"/>'
    # pelvis
    a, b_ = T(0, -.22)
    o += f'<ellipse cx="{a:.0f}" cy="{b_:.0f}" rx="{.36 * s:.0f}" ry="{.14 * s:.0f}" fill="{B}" stroke="{L}" stroke-width="4"/>'
    c, e = T(-.12, .38)
    o += bone(f'M{a - .05 * s:.0f} {b_ + .08 * s:.0f} L{c:.0f} {e:.0f} l{-.12 * s:.0f} {.03 * s:.0f}', .07 * s)
    c, e = T(.22, .25)
    o += bone(f'M{a + .1 * s:.0f} {b_ + .08 * s:.0f} L{c:.0f} {e:.0f}', .05 * s)
    # vertebrae + neural spines along the chain
    sd = 'M' + ' L'.join(f'{a_:.0f} {b__:.0f}' for a_, b__ in pts)
    o += bone(sd, .07 * s)
    for i in range(len(pts) - 1):
        for t in (0, .5):
            px = pts[i][0] + (pts[i + 1][0] - pts[i][0]) * t; py = pts[i][1] + (pts[i + 1][1] - pts[i][1]) * t
            r_ = .055 * s * (1 - i / 14)
            o += f'<circle cx="{px:.0f}" cy="{py:.0f}" r="{r_:.1f}" fill="{B}" stroke="{L}" stroke-width="2.5"/>'
            if 2 <= i <= 8:
                o += bone(f'M{px:.0f} {py:.0f} l{.03 * s:.0f} {-.11 * s * (1 - i / 12):.0f}', .025 * s)
    # tiny arm
    a, b_ = T(-.78, -.18); c, e = T(-.70, .02)
    o += bone(f'M{a:.0f} {b_:.0f} L{c:.0f} {e:.0f} l{-.07 * s:.0f} {.04 * s:.0f}', .035 * s)
    # skull (facing left), jaw open a little
    hx, hy = T(-1.30, -.42)
    sk = f'<g transform="translate({hx:.0f} {hy:.0f}) scale({s / 100:.3f})">'
    sk += (f'<path d="M8 -8 C0 -30 -30 -34 -60 -26 L-92 -12 C-98 -6 -96 4 -88 6 L-50 10 L-10 22 L14 14 Z" fill="{B}" stroke="{L}" stroke-width="5" stroke-linejoin="round"/>'
           f'<path d="M-86 10 L-48 16 L-8 30 L10 22 L4 40 C-20 44 -60 32 -84 20 Z" fill="#ece0c2" stroke="{L}" stroke-width="5" stroke-linejoin="round"/>'
           f'<ellipse cx="-12" cy="-12" rx="9" ry="10" fill="#3a2c1c"/><path d="M-52 -14 C-44 -22 -30 -20 -28 -10 C-36 -4 -48 -4 -52 -14Z" fill="#5a4630"/>'
           f'<path d="M-6 -2 C0 -4 6 2 4 10 C-2 12 -8 6 -6 -2Z" fill="#5a4630"/>')
    for k in range(7):
        tx = -86 + k * 11
        sk += f'<path d="M{tx} 6 l3 9 l3 -9" fill="#fff" stroke="{L}" stroke-width="1.6"/><path d="M{tx + 2} 20 l3 -8 l3 8" fill="#fff" stroke="{L}" stroke-width="1.6"/>'
    sk += '<path d="M-80 -20 C-50 -30 -20 -30 0 -20" fill="none" stroke="#fff" stroke-width="3" opacity=".8"/></g>'
    return o + sk


def tiny_human(x, y, s):
    """cute small person (2.5-head proportions) waving, feet at (x, y)"""
    return (f'<g transform="translate({x} {y}) scale({s})" stroke="#1e1a24" stroke-width="3" stroke-linejoin="round" stroke-linecap="round">'
            f'<path d="M-6 0 L-5 -14 M6 0 L5 -14" stroke-width="6"/><path d="M-10 -12 L-11 -34 Q0 -40 11 -34 L10 -12Z" fill="#e0574a"/>'
            f'<path d="M10 -32 L22 -50" stroke-width="5"/><circle cx="23" cy="-52" r="3.4" fill="#f2c9a0"/>'
            f'<path d="M-10 -32 L-16 -18" stroke-width="5"/>'
            f'<circle cx="0" cy="-50" r="13" fill="#f2c9a0"/><path d="M-13 -52 Q-12 -66 2 -64 Q14 -62 13 -52 Q6 -58 -13 -52Z" fill="#4a2e1e"/>'
            f'<circle cx="-4" cy="-50" r="1.8" fill="#1e1a24" stroke="none"/><circle cx="5" cy="-50" r="1.8" fill="#1e1a24" stroke="none"/>'
            f'<ellipse cx="0" cy="-44" rx="2.4" ry="3" fill="#7a2f33" stroke="none"/></g>')


def make_2():
    rnd = random.Random(202)
    BASE = 880
    d = FILTERS
    d += lin('sky2', [(0, '#3f8fd6'), (.45, '#8cc8ee'), (.78, '#f8dcae'), (1, '#ffd9a0')])
    d += rad('sun2', 1840, 90, 900, [(0, '#fffbe8', 1), (.08, '#fff2c0', .9), (.3, '#ffd88a', .35), (1, '#ffd88a', 0)])
    d += lin('grass2', [(0, '#8cba5a'), (.3, '#6a9a44'), (1, '#2e4a22')])
    d += rad('gold2', 1110, 230, 340, [(0, '#fff3b0', .85), (.4, '#ffd36a', .35), (1, '#ffd36a', 0)])
    b = '<rect width="1920" height="1080" fill="url(#sky2)"/><rect width="1920" height="1080" fill="url(#sun2)"/>'
    for k in range(10):   # sun rays
        a = math.radians(110 + k * 9)
        b += f'<path d="M1840 90 L{1840 + math.cos(a - .03) * 1500:.0f} {90 + math.sin(a - .03) * 1500:.0f} L{1840 + math.cos(a + .03) * 1500:.0f} {90 + math.sin(a + .03) * 1500:.0f}Z" fill="#fff6d8" opacity=".09"/>'
    for cx, cy, w in ((420, 640, 300), (760, 720, 220), (1500, 640, 260), (200, 760, 180)):
        b += f'<g opacity=".8" filter="url(#b3)"><ellipse cx="{cx}" cy="{cy}" rx="{w}" ry="{w * .18:.0f}" fill="#fff"/><ellipse cx="{cx - w * .3:.0f}" cy="{cy - w * .1:.0f}" rx="{w * .4:.0f}" ry="{w * .18:.0f}" fill="#fff"/><ellipse cx="{cx + w * .25:.0f}" cy="{cy - w * .12:.0f}" rx="{w * .3:.0f}" ry="{w * .16:.0f}" fill="#fff"/></g>'
    # distant hills + ground
    b += f'<path d="M0 {BASE - 40} Q300 {BASE - 110} 600 {BASE - 50} Q900 {BASE - 120} 1300 {BASE - 40} Q1600 {BASE - 100} 1920 {BASE - 50} L1920 1080 L0 1080Z" fill="#7aa0b8" opacity=".55"/>'
    b += f'<path d="M0 {BASE} Q500 {BASE - 30} 960 {BASE - 8} Q1400 {BASE + 14} 1920 {BASE - 16} L1920 1080 L0 1080Z" fill="url(#grass2)"/>'
    for _ in range(120):
        x, y = rnd.uniform(0, 1920), rnd.uniform(BASE + 10, 1075)
        b += f'<path d="M{x:.0f} {y:.0f} l-3 -12 M{x:.0f} {y:.0f} l4 -10" stroke="#2e4a22" stroke-width="2.5" opacity="{rnd.uniform(.25, .6):.2f}"/>'
    # three time pillars (rock strata)
    T1, D1 = 300, BASE - (BASE - 300) * 165 / 270
    paleo = ['#7a5a8a', '#9a6a4a', '#b8864e', '#7a8a5a', '#a87048', '#c49a5a', '#8a6a4a', '#b07850', '#9a7a5a', '#c08a5a']
    meso = ['#b06a4a', '#c88a5a', '#9a7a62', '#d0a070', '#a86a50', '#c49064']
    b += f'<ellipse cx="1110" cy="300" rx="260" ry="200" fill="url(#gold2)"/>'
    b += column(960, 1260, T1, BASE, paleo, rnd)
    b += column(1340, 1580, D1, BASE, meso, rnd)
    b += f'<ellipse cx="1700" cy="{BASE + 2}" rx="40" ry="7" fill="#e8d4a8" stroke="#2a1e14" stroke-width="2.5"/>'
    # T. rex skeleton on the dinosaur pillar
    b += f'<ellipse cx="1470" cy="{D1 + 4:.0f}" rx="150" ry="16" fill="#3a2a1a" opacity=".35" filter="url(#b3)"/>'
    b += trex(1488, D1 - 146, 110)
    # crowned trilobite on the tallest pillar (dorsal, seen from above at an angle)
    u = 300; R = trilo_dorsal(u)
    col = {'ceph': '#c47a3a', 'pyg': '#a8642e', 'pleura': '#b06a32', 'axial': '#d48a48', 'glab': '#e09a58'}
    b += f'<ellipse cx="1110" cy="{T1 + 4}" rx="150" ry="22" fill="#3a2a1a" opacity=".4" filter="url(#b3)"/>'
    b += f'<g transform="translate(1110 {T1 - 64}) scale(1 .62)">' + tri_paint(R, col, '#2a1408', 4, eyecol='#3a2410', lensfill='#e8b860', glint='#fff6d8') + '</g>'
    b += f'<g transform="translate(1110 {T1 - 64}) scale(1 .62)"><path d="{R["ceph"][0]}" fill="none" stroke="#fff2c0" stroke-width="5" opacity=".55" transform="translate(-3 -4)"/></g>'
    cy_ = T1 - 64 - .53 * u * .62
    b += (f'<g transform="translate(1110 {cy_ - 6:.0f})" stroke="#5a3a08" stroke-width="4" stroke-linejoin="round"><path d="M-60 0 L-66 -60 L-34 -30 L0 -74 L34 -30 L66 -60 L60 0Z" fill="#ffd34a"/>'
          f'<path d="M-60 0 L60 0 L60 -12 L-60 -12Z" fill="#e8a820"/><circle cx="0" cy="-34" r="9" fill="#e0405a"/><circle cx="-36" cy="-18" r="6" fill="#4ac0e8"/><circle cx="36" cy="-18" r="6" fill="#4ac0e8"/>'
          f'<path d="M-48 -8 L-52 -46" stroke="#fff8c8" stroke-width="4" opacity=".8"/></g>')
    b += spark(1270, 120, 26) + spark(950, 180, 18) + spark(1230, 250, 14) + spark(1600, 360, 16, '#fff')
    # tiny human (300 thousand years: a sliver)
    b += tiny_human(1700, BASE - 2, 1.25)
    # frog with a tape measure up the tall pillar
    b += f'<path d="M950 {BASE - 120} L950 {T1 + 30}" stroke="#2a1e14" stroke-width="22"/><path d="M950 {BASE - 120} L950 {T1 + 30}" stroke="#ffd34a" stroke-width="16"/>'
    for yy in range(T1 + 40, BASE - 120, 22):
        b += f'<path d="M943 {yy} l{10 if (yy // 22) % 5 else 15} 0" stroke="#2a1e14" stroke-width="2.5"/>'
    tape = ('<g transform="translate(66 -66) scale(.7)"><circle r="24" fill="#e8b020" stroke-width="3.5"/><circle r="9" fill="#5a4030" stroke-width="3"/>'
            '<path d="M-10 -18 q8 -6 18 -2" stroke="#fff" stroke-width="3" fill="none" opacity=".8"/></g>')
    b += frog(820, 1050, 2.7, look=(7, -9), mouth='O', shadow=True, armR='M38 -22 q22 -6 26 -40', armL='M-34 -22 q-18 4 -22 24', front=tape)
    lines = [('LONGER', 196, 'y'), ('THAN', 122, 'w'), ('DINOSAURS', 142, 'w')]
    return page('#8cc8ee', svg(d, b), lines, outline='#14223a', top=36)


# ================= 3: A BALL OF ARMOR =================
def enrolled_side(CX, CY, r, rnd):
    """enrolled trilobite seen from the side: big head shield (left) with crescent eye; 11 thorax segments fanning over the top
    and back from the neck; the tail shield closes against the head's front rim at the bottom"""
    o = '<g>'
    o += f'<circle cx="{CX}" cy="{CY}" r="{r}" fill="#4a2410"/>'
    px, py = CX - .12 * r, CY + .05 * r      # fan pivot (behind the head's back border)
    def pt(a, rr=1.0):
        a = math.radians(a); return CX + math.cos(a) * r * rr, CY + math.sin(a) * r * rr
    a0, a1 = 262, 400; n = 11; da = (a1 - a0) / n
    for k in range(n):
        s0, s1 = a0 + k * da, a0 + (k + 1) * da
        outer = [pt(s0 + (s1 - s0) * t / 8, 1.0) for t in range(9)]
        o += f'<path d="{poly(outer + [(px, py)])}" fill="url(#seg3)" stroke="#1a0a04" stroke-width="4.5" stroke-linejoin="round"/>'
        m = pt((s0 + s1) / 2, .97); q = (px + (m[0] - px) * .5, py + (m[1] - py) * .5)
        o += f'<path d="M{q[0]:.0f} {q[1]:.0f} L{m[0]:.0f} {m[1]:.0f}" stroke="#2a1006" stroke-width="3.5" opacity=".6"/>'
        e0 = pt(s0 + 1.5, .97); e1 = (px + (e0[0] - px) * .45, py + (e0[1] - py) * .45)
        o += f'<path d="M{e0[0]:.0f} {e0[1]:.0f} L{e1[0]:.0f} {e1[1]:.0f}" stroke="#ffc890" stroke-width="4" opacity=".6"/>'
        bx, by = pt((s0 + s1) / 2, 1.0)    # axial ring knob on the outer rim (the back of the animal)
        o += f'<ellipse cx="{bx:.0f}" cy="{by:.0f}" rx="{r * .07:.1f}" ry="{r * .05:.1f}" transform="rotate({(s0 + s1) / 2 + 90:.0f} {bx:.0f} {by:.0f})" fill="#d8955a" stroke="#1a0a04" stroke-width="3"/>'
    # tail shield (bottom right -> bottom)
    tail = [pt(a, 1.0) for a in range(40, 104, 4)]
    o += f'<path d="{poly(tail + [(px, py)])}" fill="#8a4a24" stroke="#1a0a04" stroke-width="5" stroke-linejoin="round"/>'
    for k in range(4):
        m = pt(48 + k * 14, .96); q = (px + (m[0] - px) * .45, py + (m[1] - py) * .45)
        o += f'<path d="M{q[0]:.0f} {q[1]:.0f} L{m[0]:.0f} {m[1]:.0f}" stroke="#2a1006" stroke-width="3" opacity=".6"/>'
    # head shield: rim from bottom (100 deg) round the front (180) to the neck at the top (262), back border bulging to the right
    head = [pt(a, 1.03) for a in range(98, 266, 4)]
    t0 = pt(262, 1.0)
    head += [(t0[0] + .02 * r, t0[1] + .12 * r), (CX + .06 * r, CY - .35 * r), (CX + .08 * r, CY + .05 * r), (CX - .02 * r, CY + .5 * r), pt(100, .99)]
    o += f'<path d="{poly(head)}" fill="url(#head3)" stroke="#1a0a04" stroke-width="6" stroke-linejoin="round"/>'
    # border furrow + glabella bulging at the front rim
    o += f'<path d="M{pt(118, .9)[0]:.0f} {pt(118, .9)[1]:.0f} A{r * .9:.0f} {r * .9:.0f} 0 0 1 {pt(246, .9)[0]:.0f} {pt(246, .9)[1]:.0f}" fill="none" stroke="#2a1006" stroke-width="4" opacity=".55"/>'
    gx, gy = pt(186, .9)
    o += f'<ellipse cx="{gx:.0f}" cy="{gy:.0f}" rx="{r * .14:.0f}" ry="{r * .36:.0f}" fill="url(#glab3)" stroke="#1a0a04" stroke-width="5"/>'
    for k in range(10):
        o += f'<circle cx="{gx + rnd.uniform(-.06, .08) * r:.0f}" cy="{gy + rnd.uniform(-.3, .3) * r:.0f}" r="{rnd.uniform(3, 6.5):.1f}" fill="#f6c08a" opacity=".75"/>'
    # big crescent compound eye on the cheek (calcite lenses)
    ex, ey = CX - .38 * r, CY - .1 * r
    o += f'<ellipse cx="{ex + .03 * r:.0f}" cy="{ey:.0f}" rx="{r * .17:.0f}" ry="{r * .3:.0f}" fill="#f6c08a" opacity=".5" filter="url(#b6)"/>'
    eye = (f'M{ex - .04 * r:.0f} {ey - .3 * r:.0f} C{ex + .22 * r:.0f} {ey - .26 * r:.0f} {ex + .24 * r:.0f} {ey + .24 * r:.0f} {ex - .02 * r:.0f} {ey + .3 * r:.0f} '
           f'C{ex + .06 * r:.0f} {ey + .1 * r:.0f} {ex + .06 * r:.0f} {ey - .1 * r:.0f} {ex - .04 * r:.0f} {ey - .3 * r:.0f}Z')
    o += f'<path d="{eye}" fill="#2a1408" stroke="#1a0a04" stroke-width="4"/>'
    o += f'<clipPath id="eye3"><path d="{eye}"/></clipPath><g clip-path="url(#eye3)">'
    for lx, ly in hexlenses(ex + .08 * r, ey, .14 * r, .32 * r, .026 * r):
        o += f'<circle cx="{lx:.1f}" cy="{ly:.1f}" r="{.022 * r:.1f}" fill="url(#lens3)"/>'
    o += '</g>'
    # light: top-left rim, shade bottom-right
    o += f'<circle cx="{CX}" cy="{CY}" r="{r}" fill="url(#shade3)"/>'
    o += f'<path d="M{pt(170, 1.02)[0]:.0f} {pt(170, 1.02)[1]:.0f} A{r * 1.02:.0f} {r * 1.02:.0f} 0 0 1 {pt(300, 1.02)[0]:.0f} {pt(300, 1.02)[1]:.0f}" fill="none" stroke="#c8fff4" stroke-width="7" opacity=".75"/>'
    return o + '</g>'


def eurypterid(x, y, s, rot=0):
    """sea scorpion seen from above (squashed for the seafloor), head toward +x"""
    L = '#1a1414'
    g = f'<g transform="translate({x} {y}) rotate({rot}) scale({s} {s * .55:.2f})" stroke="{L}" stroke-linejoin="round" stroke-linecap="round">'
    for sg in (-1, 1):   # walking legs (spiny) and swimming paddles
        for k in range(4):
            bx = .55 - k * .16
            g += f'<path d="M{bx:.2f} {sg * .3:.2f} L{bx + .25 + k * .02:.2f} {sg * (.62 + k * .05):.2f} L{bx + .42:.2f} {sg * (.72 + k * .03):.2f}" fill="none" stroke-width="6" {NS}/>'
            g += f'<path d="M{bx + .1:.2f} {sg * .45:.2f} l.06 {sg * -.06:.2f}" fill="none" stroke-width="3" {NS}/>'
        g += f'<path d="M.02 {sg * .34:.2f} Q-.25 {sg * .8:.2f} -.62 {sg * .95:.2f}" fill="none" stroke-width="10" {NS}/>'
        g += f'<ellipse cx="-.72" cy="{sg * .98:.2f}" rx=".22" ry=".13" transform="rotate({sg * -10} -.72 {sg * .98:.2f})" fill="#7a5040" stroke-width="3.5" {NS}/>'
    segs = 12; xx = 0
    for k in range(segs):
        w = (.46 + .16 * math.sin(min(k, 5) / 5 * math.pi / 2)) if k < 7 else .62 - (k - 6) * .085
        h = .26 if k < 7 else .3
        g += f'<path d="M{xx:.2f} {-w:.2f} L{xx - h:.2f} {-w * .96:.2f} Q{xx - h - .04:.2f} 0 {xx - h:.2f} {w * .96:.2f} L{xx:.2f} {w:.2f} Q{xx + .04:.2f} 0 {xx:.2f} {-w:.2f}Z" fill="{"#8a5a44" if k % 2 else "#7a4c3a"}" stroke-width="3.5" {NS}/>'
        g += f'<path d="M{xx - .03:.2f} {-w * .8:.2f} L{xx - h + .02:.2f} {-w * .8:.2f}" stroke="#d8a080" stroke-width="2.5" {NS} opacity=".7"/>'
        xx -= h
    g += f'<path d="M{xx:.2f} -.1 L{xx - 1.05:.2f} 0 L{xx:.2f} .1Z" fill="#6a3c2c" stroke-width="3.5" {NS}/>'
    g += f'<path d="M0 -.48 L.75 -.42 Q.98 -.3 .98 0 Q.98 .3 .75 .42 L0 .48 Q.05 0 0 -.48Z" fill="#9a6a50" stroke-width="4" {NS}/>'
    for sg in (-1, 1):
        g += f'<ellipse cx=".58" cy="{sg * .3:.2f}" rx=".13" ry=".08" fill="#1a1010" stroke-width="2" {NS}/><circle cx=".62" cy="{sg * .3 - .02:.2f}" r=".025" fill="#ffd8a0" stroke="none"/>'
        g += f'<path d="M.96 {sg * .08:.2f} l.14 {sg * .04:.2f}" stroke-width="5" {NS}/>'
    g += f'<path d="M.05 -.4 L.7 -.36" stroke="#e8c0a0" stroke-width="3" {NS} opacity=".7"/>'
    return g + '</g>'


def make_3():
    rnd = random.Random(303)
    CX, CY, r = 1060, 540, 200
    d = FILTERS
    d += lin('sea3', [(0, '#7fe6e0'), (.25, '#2aa8b0'), (.65, '#0f5a70'), (1, '#062838')])
    d += lin('sand3', [(0, '#5a8a80'), (.3, '#3a6460'), (1, '#122a2c')])
    d += lin('seg3', [(0, '#c47840'), (1, '#7a3e1c')], x2=1, y2=1)
    d += lin('head3', [(0, '#d08a50'), (1, '#7a4020')], x2=.4, y2=1)
    d += lin('glab3', [(0, '#e8a86a'), (1, '#9a5a2a')])
    d += ('<radialGradient id="lens3" cx=".4" cy=".35" r=".7"><stop offset="0" stop-color="#fffbe0"/><stop offset=".5" stop-color="#ffc860"/><stop offset="1" stop-color="#6a3a10"/></radialGradient>')
    d += rad('shade3', CX - 90, CY - 110, 330, [(0, '#fff', .18), (.45, '#000', 0), (1, '#000', .55)])
    d += lin('armor3', [(0, '#7a9aa8'), (.35, '#4a6270'), (1, '#1c2830')], x2=.2, y2=1)
    d += lin('jaw3', [(0, '#5a7480'), (1, '#16222a')], x2=.1, y2=1)
    d += rad('mouth3', 1420, 470, 260, [(0, '#3a0a10', 1), (1, '#0a0204', 1)])
    d += rad('vig3', 960, 540, 1150, [(0, '#000', 0), (.6, '#000', 0), (1, '#021018', .55)])
    b = '<rect width="1920" height="1080" fill="url(#sea3)"/>'
    # sun shafts from the surface
    for x0, w, op in ((300, 90, .18), (700, 140, .2), (1000, 100, .16), (1500, 160, .12), (1800, 80, .1)):
        b += f'<path d="M{x0} -20 L{x0 + w} -20 L{x0 + w + 200} 1080 L{x0 + 120} 1080Z" fill="#e8fff8" opacity="{op}" filter="url(#b12)"/>'
    # caustic ripples near the top
    for _ in range(40):
        x, y = rnd.uniform(0, 1920), rnd.uniform(0, 160)
        b += f'<path d="M{x:.0f} {y:.0f} q30 -12 60 0 q30 12 60 0" fill="none" stroke="#e8fffc" stroke-width="3" opacity="{rnd.uniform(.12, .35):.2f}"/>'
    # far reef / seafloor
    b += '<path d="M0 760 Q300 720 600 770 Q900 800 1300 760 Q1600 730 1920 770 L1920 1080 L0 1080Z" fill="#1f5a62" opacity=".7"/>'
    for x, h in ((140, 160), (240, 110), (1620, 120), (1760, 170)):
        b += f'<path d="M{x} 780 l0 {-h} m0 {h * .4} l{-h * .3} {-h * .4} m{h * .3} {h * .55} l{h * .3} {-h * .35}" stroke="#2e7a7a" stroke-width="10" stroke-linecap="round" fill="none" opacity=".8"/>'
    b += '<path d="M0 860 Q500 830 960 856 Q1400 880 1920 846 L1920 1080 L0 1080Z" fill="url(#sand3)"/>'
    for _ in range(26):   # caustic light on the floor
        x, y = rnd.uniform(0, 1920), rnd.uniform(880, 1060)
        b += f'<path d="M{x:.0f} {y:.0f} q20 -8 40 0 q20 8 40 0" fill="none" stroke="#bff8ee" stroke-width="2.5" opacity="{rnd.uniform(.12, .3):.2f}"/>'
    # ---- armoured jawed fish (placoderm), mouth open toward the ball ----
    fish = '<g>'
    fish += '<path d="M1600 420 C1760 400 1900 420 1960 440 L1960 700 C1840 690 1720 640 1620 560Z" fill="#2a3c46"/>'
    fish += '<path d="M1300 352 C1400 372 1520 392 1640 424 L1640 452 C1520 500 1420 566 1312 602 Z" fill="url(#mouth3)"/>'
    fish += '<path d="M1330 372 C1420 400 1500 420 1600 436 M1340 584 C1420 540 1500 500 1600 462" fill="none" stroke="#7a2030" stroke-width="10" opacity=".5"/>'
    # upper head armour
    fish += ('<path d="M1300 352 C1296 300 1330 220 1420 168 C1520 118 1700 104 1960 120 L1960 440 C1860 420 1760 410 1640 424 C1520 392 1400 370 1300 352Z" '
             'fill="url(#armor3)" stroke="#0a1418" stroke-width="7" stroke-linejoin="round"/>')
    fish += ('<path d="M1430 170 C1470 240 1520 300 1600 330 M1600 330 C1680 300 1760 250 1820 112 M1600 330 C1640 370 1660 400 1660 424 '
             'M1720 112 C1700 180 1660 240 1600 330" fill="none" stroke="#0a1418" stroke-width="5" opacity=".75"/>')
    for _ in range(40):   # bony tubercles on the plates
        x, y = rnd.uniform(1360, 1900), rnd.uniform(140, 400)
        if y < 352 + (x - 1300) * .2 - 10:
            fish += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{rnd.uniform(3, 6):.1f}" fill="#9ab8c4" opacity=".35"/>'
    fish += '<path d="M1310 330 C1320 260 1360 210 1430 172 C1520 130 1640 116 1780 112" fill="none" stroke="#c8f4ff" stroke-width="7" opacity=".7"/>'
    # shearing fang plates
    fish += '<path d="M1296 340 L1286 420 L1340 362Z" fill="#e8eef0" stroke="#0a1418" stroke-width="5" stroke-linejoin="round"/>'
    fish += '<path d="M1360 368 L1356 418 L1396 378Z" fill="#d8e0e4" stroke="#0a1418" stroke-width="4" stroke-linejoin="round"/>'
    # eye with bony ring
    fish += '<circle cx="1490" cy="236" r="44" fill="#1a262c" stroke="#0a1418" stroke-width="6"/><circle cx="1490" cy="236" r="30" fill="#e8c040"/>'
    fish += '<circle cx="1482" cy="238" r="16" fill="#0a0a0a"/><circle cx="1474" cy="228" r="6" fill="#fff"/>'
    fish += '<path d="M1440 196 Q1490 176 1540 206" fill="none" stroke="#0a1418" stroke-width="9"/>'
    # lower jaw
    fish += ('<path d="M1312 602 C1420 566 1520 500 1640 452 C1760 450 1880 470 1960 480 L1960 720 C1820 700 1700 680 1580 660 C1460 650 1360 650 1300 632 Z" '
             'fill="url(#jaw3)" stroke="#0a1418" stroke-width="7" stroke-linejoin="round"/>')
    fish += '<path d="M1320 612 L1306 540 L1366 592Z" fill="#e8eef0" stroke="#0a1418" stroke-width="5" stroke-linejoin="round"/>'
    fish += '<path d="M1400 570 L1398 524 L1436 556Z" fill="#d8e0e4" stroke="#0a1418" stroke-width="4" stroke-linejoin="round"/>'
    fish += '<path d="M1330 640 C1480 660 1640 680 1900 700" fill="none" stroke="#0a1418" stroke-width="4" opacity=".6"/>'
    fish += '<path d="M1330 606 C1440 574 1540 520 1640 470" fill="none" stroke="#b8e8f4" stroke-width="5" opacity=".45"/>'
    fish += '</g>'
    b += fish
    # glow + the enrolled trilobite
    b += f'<circle cx="{CX}" cy="{CY}" r="{r + 90}" fill="#e8fff4" opacity=".35" filter="url(#b50)"/>'
    b += f'<ellipse cx="{CX + 20}" cy="880" rx="{r * 1.1:.0f}" ry="30" fill="#04181c" opacity=".55" filter="url(#b12)"/>'
    b += enrolled_side(CX, CY, r, rnd)
    b += spark(CX - r - 20, CY - r + 30, 26) + spark(CX + r - 10, CY - r - 20, 20, '#e8fffc') + spark(CX - 40, CY + r + 30, 14)
    # sea scorpion creeping in on the floor
    b += '<ellipse cx="840" cy="965" rx="230" ry="28" fill="#04181c" opacity=".45" filter="url(#b6)"/>'
    b += eurypterid(980, 940, 112, rot=-6)
    # bubbles
    b += bubbles(rnd, 30, 700, 1250, 80, 760, skip=lambda x, y: (x - CX) ** 2 + (y - CY) ** 2 < (r + 30) ** 2 or (x < 800 and y < 520))
    # frog in a diving helmet holding a curled pill bug
    pill = ('<g transform="translate(72 -64)"><circle r="17" fill="#6a6e78" stroke-width="3"/>'
            + ''.join(f'<path d="M{-15 + k * 6} -8 Q{-14 + k * 6} 0 {-15 + k * 6} 8" fill="none" stroke-width="2"/>' for k in range(1, 5))
            + '<path d="M-8 -10 q8 -6 16 -2" stroke="#fff" stroke-width="2.5" fill="none" opacity=".8"/></g>')
    b += frog(360, 1050, 2.75, look=(10, -5), mouth='O', helmet=True, shadow=True, armR='M38 -22 q24 -6 30 -40', armL='M-34 -22 q-18 6 -22 24', front=pill)
    b += bubbles(rnd, 4, 380, 430, 640, 760)
    b += '<rect width="1920" height="1080" fill="url(#vig3)"/>'
    lines = [('A BALL', 176, 'w'), ('OF', 112, 'w'), ('ARMOR', 206, 'y')]
    return page('#2aa8b0', svg(d, b), lines, outline='#062030', top=36)


# ================= 4: OCEAN TOO ACIDIC =================
def make_4():
    rnd = random.Random(404)
    X0, X1, TOP, BOT, SURF = 1010, 1570, 210, 975, 330
    d = FILTERS
    d += lin('sky4', [(0, '#12080a'), (.4, '#3a1210'), (.7, '#8a2a14'), (.78, '#d8541c'), (1, '#2a0e08')])
    d += rad('lavaglow4', 1300, 760, 900, [(0, '#ff8a2a', .7), (.35, '#e2481c', .3), (1, '#8a2a14', 0)])
    d += lin('acid4', [(0, '#e8ff6a'), (.35, '#a8e83a'), (1, '#3a8a2a')])
    d += lin('glass4', [(0, '#fff'), (.12, '#fff'), (.2, '#fff'), (1, '#fff')], x2=1, y2=0)
    d += lin('basalt4', [(0, '#2a1c1a'), (1, '#0a0606')])
    d += ('<mask id="erode4"><rect x="-400" y="-400" width="800" height="800" fill="#fff"/>'
          + ''.join(f'<circle cx="{rnd.uniform(-190, 190):.0f}" cy="{rnd.uniform(-190, 190):.0f}" r="{rnd.uniform(5, 16):.0f}" fill="#000"/>' for _ in range(34))
          + ''.join(f'<circle cx="{170 + rnd.uniform(-30, 40):.0f}" cy="{rnd.uniform(-60, 200):.0f}" r="{rnd.uniform(18, 36):.0f}" fill="#000"/>' for _ in range(9))
          + ''.join(f'<circle cx="{rnd.uniform(-60, 160):.0f}" cy="{180 + rnd.uniform(-10, 40):.0f}" r="{rnd.uniform(16, 30):.0f}" fill="#000"/>' for _ in range(7))
          + '</mask>')
    d += f'<clipPath id="liq4"><path d="M{X0 + 6} {SURF} L{X1 - 6} {SURF} L{X1 - 6} {BOT - 60} Q{X1 - 6} {BOT - 6} {X1 - 60} {BOT - 6} L{X0 + 60} {BOT - 6} Q{X0 + 6} {BOT - 6} {X0 + 6} {BOT - 60}Z"/></clipPath>'
    b = '<rect width="1920" height="1080" fill="url(#sky4)"/>'
    # ash clouds
    for _ in range(16):
        b += f'<ellipse cx="{rnd.uniform(0, 1920):.0f}" cy="{rnd.uniform(60, 520):.0f}" rx="{rnd.uniform(160, 360):.0f}" ry="{rnd.uniform(50, 110):.0f}" fill="{rnd.choice(["#2a1412", "#4a1c14", "#1a0c0c"])}" opacity=".6" filter="url(#b24)"/>'
    # fissure eruptions along the horizon (Siberian Traps) with lava fountains + plumes
    H = 760
    for x, h, w in ((90, 140, 30), (360, 190, 40), (640, 120, 26), (1180, 230, 46), (1480, 170, 34), (1760, 210, 40)):
        b += f'<path d="M{x - 90} {H} Q{x} {H - h * 2.6} {x + 120} {H - h * 3.4}" fill="none" stroke="#3a1a14" stroke-width="{w * 3}" opacity=".55" filter="url(#b24)"/>'
        b += f'<path d="M{x - w} {H} Q{x - w * .3} {H - h} {x} {H - h * 1.05} Q{x + w * .3} {H - h} {x + w} {H}Z" fill="#ffb03a" opacity=".9" filter="url(#b3)"/>'
        b += f'<path d="M{x - w * .4} {H} Q{x} {H - h * .8} {x + w * .4} {H}Z" fill="#fff2a0"/>'
        for _ in range(8):
            b += f'<circle cx="{x + rnd.uniform(-w * 2, w * 2):.0f}" cy="{H - rnd.uniform(h * .3, h * 1.2):.0f}" r="{rnd.uniform(2, 5):.1f}" fill="#ffd36a"/>'
    b += '<rect width="1920" height="1080" fill="url(#lavaglow4)"/>'
    b += f'<path d="M0 {H} L1920 {H}" stroke="#ff9a3a" stroke-width="5" opacity=".8" filter="url(#b3)"/>'
    # basalt plain with glowing lava cracks
    b += f'<path d="M0 {H} L1920 {H} L1920 1080 L0 1080Z" fill="url(#basalt4)"/>'
    for k in range(7):
        y = H + 30 + k * 42; x0 = rnd.uniform(-100, 200)
        pts = [(x0 + j * 150 + rnd.uniform(-40, 40), y + rnd.uniform(-16, 16) + j * 2) for j in range(14)]
        b += f'<polyline points="{P(pts)}" fill="none" stroke="#ff7a2a" stroke-width="{2 + k * .7:.1f}" opacity="{.25 + k * .06:.2f}"/>'
        b += f'<polyline points="{P(pts)}" fill="none" stroke="#ffb03a" stroke-width="{8 + k * 2}" opacity=".08" filter="url(#b6)"/>'
    for k in range(5):   # basalt columns step edges
        b += f'<path d="M0 {H + 110 + k * 60} L1920 {H + 104 + k * 62}" stroke="#000" stroke-width="3" opacity=".35"/>'
    # ---- giant beaker of acid sea ----
    b += f'<ellipse cx="{(X0 + X1) / 2}" cy="{BOT + 10}" rx="340" ry="28" fill="#000" opacity=".6" filter="url(#b12)"/>'
    b += f'<ellipse cx="{(X0 + X1) / 2}" cy="{(SURF + BOT) / 2}" rx="420" ry="480" fill="#b8ff4a" opacity=".22" filter="url(#b50)"/>'
    lq = f'<g clip-path="url(#liq4)">'
    lq += f'<rect x="{X0}" y="{SURF}" width="{X1 - X0}" height="{BOT - SURF}" fill="url(#acid4)" opacity=".9"/>'
    lq += f'<rect x="{X0}" y="{BOT - 260}" width="{X1 - X0}" height="260" fill="#ff6a2a" opacity=".22" filter="url(#b24)"/>'
    for _ in range(6):
        lq += f'<path d="M{rnd.uniform(X0, X1):.0f} {SURF + 20} q{rnd.uniform(-40, 40):.0f} 200 {rnd.uniform(-20, 20):.0f} 500" stroke="#f4ffb0" stroke-width="{rnd.uniform(10, 26):.0f}" opacity=".12" fill="none" filter="url(#b6)"/>'
    # the dissolving trilobite
    u = 400; R = trilo_dorsal(u)
    col = {'ceph': '#d89a5a', 'pyg': '#c4844a', 'pleura': '#cc8c50', 'axial': '#e8b070', 'glab': '#f0c080'}
    TX, TY = 1290, 690
    lq += f'<g transform="translate({TX} {TY}) rotate(-18)"><ellipse cx="0" cy="0" rx="{u * .55:.0f}" ry="{u * .6:.0f}" fill="#f8ffe0" opacity=".35" filter="url(#b24)"/>'
    lq += f'<g mask="url(#erode4)">' + tri_paint(R, col, '#3a2210', 4, eyecol='#3a2410', lensfill='#e8c080', glint='#fffbe8') + '</g>'
    for _ in range(80):   # fizz hugging the shell
        a = rnd.uniform(0, 2 * math.pi); rr = rnd.uniform(.38, .55)
        x, y = math.cos(a) * u * rr * .95, math.sin(a) * u * rr * 1.0
        s_ = rnd.uniform(2.5, 8)
        lq += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{s_:.1f}" fill="#fff" fill-opacity=".25" stroke="#fff" stroke-width="1.8" opacity=".85"/>'
    lq += '</g>'
    for _ in range(14):   # bubble streams rising to the surface
        sx = TX + rnd.uniform(-170, 170); sy = TY + rnd.uniform(-170, 120)
        y = sy
        while y > SURF + 10:
            y -= rnd.uniform(22, 50); s_ = rnd.uniform(3, 9) * (1 + (sy - y) / 900)
            lq += f'<circle cx="{sx + math.sin(y / 30) * 6:.0f}" cy="{y:.0f}" r="{s_:.1f}" fill="#fff" fill-opacity=".18" stroke="#fffde8" stroke-width="2" opacity=".75"/>'
    lq += '</g>'
    b += lq
    # foam at the surface
    for _ in range(70):
        x = rnd.uniform(X0 + 14, X1 - 14); s_ = rnd.uniform(6, 20)
        b += f'<circle cx="{x:.0f}" cy="{SURF + rnd.uniform(-14, 8):.0f}" r="{s_:.1f}" fill="#f6ffd0" fill-opacity=".7" stroke="#8ac03a" stroke-width="2"/>'
    for _ in range(18):   # spray above
        b += f'<circle cx="{rnd.uniform(X0 + 20, X1 - 20):.0f}" cy="{SURF - rnd.uniform(20, 120):.0f}" r="{rnd.uniform(2, 6):.1f}" fill="#f6ffd0" opacity=".8"/>'
    # glass
    gp = f'M{X0} {TOP} L{X0} {BOT - 60} Q{X0} {BOT} {X0 + 60} {BOT} L{X1 - 60} {BOT} Q{X1} {BOT} {X1} {BOT - 60} L{X1} {TOP}'
    b += f'<path d="{gp}" fill="#fff" fill-opacity=".06" stroke="#0e0a08" stroke-width="16"/>'
    b += f'<path d="{gp}" fill="none" stroke="#f0fff4" stroke-width="7" opacity=".8"/>'
    b += f'<path d="M{X0 - 30} {TOP - 18} Q{X0 - 10} {TOP} {X0} {TOP + 20} M{X0 - 30} {TOP - 18} L{X1 + 10} {TOP - 18} Q{X1 + 16} {TOP} {X1} {TOP + 6}" fill="none" stroke="#f0fff4" stroke-width="9" stroke-linecap="round" opacity=".85"/>'
    b += f'<path d="M{X0 + 36} {TOP + 40} L{X0 + 36} {BOT - 80}" stroke="#fff" stroke-width="16" opacity=".35" stroke-linecap="round"/>'
    b += f'<path d="M{X0 + 70} {TOP + 60} L{X0 + 70} {TOP + 300}" stroke="#fff" stroke-width="6" opacity=".4" stroke-linecap="round"/>'
    b += f'<path d="M{X1 - 34} {TOP + 80} L{X1 - 34} {BOT - 120}" stroke="#ffd0a0" stroke-width="8" opacity=".35" stroke-linecap="round"/>'
    for k in range(7):   # graduation marks
        y = SURF + 60 + k * 80
        b += f'<path d="M{X1 - 120} {y} L{X1 - 60} {y}" stroke="#fff" stroke-width="5" opacity=".6"/>'
        b += f'<path d="M{X1 - 90} {y + 40} L{X1 - 60} {y + 40}" stroke="#fff" stroke-width="3" opacity=".5"/>'
    b += spark(X0 + 40, TOP + 20, 24) + spark(X1 - 30, TOP + 120, 18) + spark(1180, 560, 16, '#fffbe8')
    # frog in goggles with a pH strip that turned red
    strip = ('<g transform="translate(66 -76) rotate(-18)"><rect x="-7" y="-58" width="14" height="70" rx="2" fill="#f4f0e0" stroke-width="3"/>'
             '<rect x="-7" y="-58" width="14" height="24" rx="2" fill="#e0303a" stroke-width="3"/></g>')
    b += '<ellipse cx="780" cy="900" rx="200" ry="170" fill="#ff8a3a" opacity=".18" filter="url(#b50)"/>'
    b += frog(770, 1052, 2.75, look=(10, -6), mouth='O', shadow=True, mid=goggles('#2a3a2a', '#d8ffb0'), armR='M38 -22 q22 -10 26 -42', armL='M-34 -22 q-18 4 -22 24', front=strip)
    lines = [('OCEAN', 176, 'w'), ('TOO', 126, 'w'), ('ACIDIC', 214, 'y')]
    return page('#3a1210', svg(d, b), lines, outline='#140606', top=36)


# ================= 5: ONLY ONE SURVIVED =================
def ghost_trilo(x, y, s, rot, kind, op):
    """faded stone silhouette of an extinct trilobite: 'spiny', 'spade' (long front spade) or 'giant'"""
    R = trilo_dorsal(100, N=9 if kind != 'giant' else 13)
    g = f'<g transform="translate({x} {y}) rotate({rot}) scale({s / 100:.3f})" opacity="{op}">'
    if kind == 'spiny':
        for k in range(9):
            yy = -10 + k * 4.4
            g += f'<path d="M-40 {yy} L-80 {yy + 18 + k * 2} M40 {yy} L80 {yy + 18 + k * 2}" stroke="#c8c4d8" stroke-width="3" stroke-linecap="round"/>'
        g += '<path d="M-48 2 L-70 70 M48 2 L70 70 M0 -50 L0 -86" stroke="#c8c4d8" stroke-width="4" stroke-linecap="round"/>'
    if kind == 'spade':
        g += '<path d="M-10 -50 L-26 -96 Q0 -112 26 -96 L10 -50Z" fill="#c8c4d8"/>'
    if kind == 'giant':
        g += '<path d="M-48 2 L-62 60 M48 2 L62 60" stroke="#c8c4d8" stroke-width="5" stroke-linecap="round"/>'
    g += tri_paint(R, {'ceph': '#bcb8d0', 'pyg': '#a8a4c0', 'pleura': '#b0acc8', 'axial': '#c8c4dc', 'glab': '#d4d0e4'}, '#5a5670', 1.6, eyecol='#7a7690', lensfill='#9a96b0')
    return g + '</g>'


def make_5():
    rnd = random.Random(505)
    d = FILTERS
    d += lin('sky5', [(0, '#0a0c24'), (.5, '#1c2050'), (.85, '#3a3270'), (1, '#4a3a78')])
    d += rad('moon5', 1300, 300, 230, [(0, '#fffbe8', 1), (.85, '#f2ecd0', 1), (1, '#d8d0b0', 1)])
    d += rad('halo5', 1300, 300, 620, [(0, '#e8e4ff', .45), (.4, '#b8b0ff', .15), (1, '#b8b0ff', 0)])
    d += rad('gold5', 1640, 480, 300, [(0, '#fff2b0', .9), (.35, '#ffcf5a', .4), (1, '#ffcf5a', 0)])
    d += lin('live5', [(0, '#7a5a34'), (1, '#3a2a18')], x2=0, y2=1)
    d += lin('bark5', [(0, '#3a3058'), (1, '#16122a')], x2=1, y2=0)
    d += lin('hill5', [(0, '#1a1838'), (1, '#07060f')])
    b = '<rect width="1920" height="1080" fill="url(#sky5)"/>'
    for _ in range(140):
        b += f'<circle cx="{rnd.uniform(0, 1920):.0f}" cy="{rnd.uniform(0, 760):.0f}" r="{rnd.choice([1.2, 1.8, 2.5])}" fill="#eef0ff" opacity="{rnd.uniform(.2, .8):.2f}"/>'
    b += '<rect width="1920" height="1080" fill="url(#halo5)"/>'
    b += '<circle cx="1300" cy="300" r="230" fill="url(#moon5)"/>'
    for cx, cy, rr in ((1230, 240, 34), (1360, 350, 46), (1280, 380, 20), (1400, 220, 24), (1190, 340, 16)):
        b += f'<circle cx="{cx}" cy="{cy}" r="{rr}" fill="#d8d0b0" opacity=".5"/>'
    # hill
    b += '<path d="M0 930 Q400 880 800 900 Q1100 860 1300 880 Q1600 900 1920 870 L1920 1080 L0 1080Z" fill="url(#hill5)"/>'
    for _ in range(140):
        x = rnd.uniform(0, 1920); y = 900 + rnd.uniform(-6, 170)
        b += f'<path d="M{x:.0f} {y:.0f} l-4 -16 M{x:.0f} {y:.0f} l5 -13" stroke="#2a2850" stroke-width="2.5" opacity=".7"/>'
    # ---- the pruned family tree ----
    TR = []   # (x0, y0, x1, y1, w0, w1, bend, alive)
    TR.append((1170, 960, 1150, 640, 150, 92, 14, 0))
    TR.append((1150, 650, 960, 430, 80, 46, -20, 0))
    TR.append((1150, 650, 1180, 300, 76, 44, 18, 0))
    TR.append((1160, 680, 1400, 520, 64, 38, -12, 0))
    TR.append((1000, 480, 890, 330, 44, 30, 8, 0))
    TR.append((990, 470, 1000, 250, 40, 28, -10, 0))
    TR.append((1176, 340, 1080, 160, 40, 26, -6, 0))
    TR.append((1182, 330, 1300, 150, 40, 26, 10, 0))
    TR.append((1380, 530, 1430, 380, 36, 24, -8, 0))
    TR.append((1390, 536, 1780, 610, 48, 22, -44, 1))   # the living branch
    TR.append((1110, 760, 940, 700, 46, 30, 10, 0))
    tree = ''
    for x0, y0, x1, y1, w0, w1, bend, alive in TR:
        tree += f'<path d="{taper(x0, y0, x1, y1, w0, w1, bend)}" fill="{"url(#live5)" if alive else "url(#bark5)"}" stroke="#05040c" stroke-width="5" stroke-linejoin="round"/>'
        if alive:
            tree += f'<path d="{taper(x0, y0 - 6, x1, y1 - 4, w0 * .5, w1 * .4, bend)}" fill="#ffd88a" opacity=".35"/>'
    # moon rim light on the right edges
    for x0, y0, x1, y1, w0, w1, bend, alive in TR:
        dx, dy = x1 - x0, y1 - y0; L = math.hypot(dx, dy); nx, ny = -dy / L, dx / L
        if nx < 0: nx, ny = -nx, -ny
        tree += f'<path d="M{x0 + nx * w0 * .42:.0f} {y0 + ny * w0 * .42:.0f} Q{(x0 + x1) / 2 + nx * (w0 + w1) * .22:.0f} {(y0 + y1) / 2 + ny * (w0 + w1) * .22:.0f} {x1 + nx * w1 * .42:.0f} {y1 + ny * w1 * .42:.0f}" fill="none" stroke="#b8b0f0" stroke-width="4" opacity=".55"/>'
    # bark texture
    for _ in range(40):
        x, y = 1130 + rnd.uniform(-50, 60), rnd.uniform(680, 940)
        tree += f'<path d="M{x:.0f} {y:.0f} q{rnd.uniform(-6, 6):.0f} {-rnd.uniform(20, 50):.0f} {rnd.uniform(-4, 4):.0f} {-rnd.uniform(40, 80):.0f}" fill="none" stroke="#0a0818" stroke-width="3" opacity=".6"/>'
    # roots
    for dx_, ex in ((-1, 980), (1, 1360), (-1, 1060), (1, 1280)):
        tree += f'<path d="M1170 940 Q{(1170 + ex) / 2} {960} {ex} {975 + rnd.uniform(0, 20):.0f}" stroke="#16122a" stroke-width="22" fill="none" stroke-linecap="round"/>'
    # sawn ends (pale cut faces with rings) on every dead branch
    for x0, y0, x1, y1, w0, w1, bend, alive in TR:
        if alive or (x0, y0) == (1170, 960):
            continue
        a = math.degrees(math.atan2(y1 - y0, x1 - x0))
        tree += (f'<g transform="translate({x1} {y1}) rotate({a + 90:.0f})"><ellipse rx="{w1 * .56:.0f}" ry="{w1 * .26:.0f}" fill="#e8d6b0" stroke="#3a2a1a" stroke-width="3"/>'
                 f'<ellipse rx="{w1 * .34:.0f}" ry="{w1 * .15:.0f}" fill="none" stroke="#b8a07a" stroke-width="2"/><ellipse rx="{w1 * .14:.0f}" ry="{w1 * .06:.0f}" fill="none" stroke="#b8a07a" stroke-width="2"/></g>')
    b += tree
    # ghost fossils of the lost branches, fading into dust
    for x, y, s, rot, kind in ((860, 270, 120, -24, 'spiny'), (1010, 180, 110, 10, 'spade'), (1080, 90, 96, -12, 'giant'), (1320, 92, 110, 18, 'spiny'),
                               (1460, 236, 110, 22, 'spade'), (900, 640, 96, -40, 'giant')):
        b += ghost_trilo(x, y, s, rot, kind, .5)
        for _ in range(10):
            b += f'<circle cx="{x + rnd.uniform(-60, 60):.0f}" cy="{y + rnd.uniform(-70, -10):.0f}" r="{rnd.uniform(1.5, 4):.1f}" fill="#d8d4f0" opacity="{rnd.uniform(.2, .6):.2f}"/>'
    # the living branch: leaves + golden glow + small oval proetid
    b += '<ellipse cx="1640" cy="480" rx="300" ry="300" fill="url(#gold5)"/>'
    for lx, ly, la in ((1480, 540, -30), (1540, 556, 40), (1730, 580, -50), (1450, 556, 60), (1770, 600, 70), (1790, 596, -10), (1760, 620, 130), (1560, 570, 150)):
        b += (f'<g transform="translate({lx} {ly}) rotate({la})"><path d="M0 0 Q16 -30 0 -60 Q-16 -30 0 0Z" fill="#7ac84a" stroke="#1a3a12" stroke-width="3.5"/>'
              f'<path d="M0 -4 L0 -54" stroke="#cfffa0" stroke-width="2.5"/></g>')
    u = 220; R = trilo_dorsal(u, N=10)
    col = {'ceph': '#d89048', 'pyg': '#c47a38', 'pleura': '#c8823e', 'axial': '#e8a45a', 'glab': '#f0b46a'}
    b += f'<g transform="translate(1640 472) rotate(-12)">' + tri_paint(R, col, '#2a1406', 3.4, eyecol='#3a2210', lensfill='#ffd890', glint='#fffbe8') + '</g>'
    b += f'<g transform="translate(1640 472) rotate(-12)"><path d="{R["ceph"][0]}" fill="none" stroke="#fff4c8" stroke-width="4" opacity=".6" transform="translate(-3 -3)"/></g>'
    b += spark(1500, 360, 24) + spark(1800, 400, 18) + spark(1830, 690, 14) + spark(1470, 470, 12)
    for _ in range(14):
        b += f'<circle cx="{rnd.uniform(1500, 1820):.0f}" cy="{rnd.uniform(400, 680):.0f}" r="{rnd.uniform(2, 4):.1f}" fill="#fff2b0" opacity="{rnd.uniform(.4, .9):.2f}"/>'
    # frog watering the roots
    can = ('<g transform="translate(70 -40) rotate(-10)"><path d="M-22 -24 L22 -24 L18 18 L-18 18Z" fill="#5aa0c8" stroke-width="3.5"/>'
           '<path d="M18 -10 L58 -40 L62 -34 L22 2Z" fill="#5aa0c8" stroke-width="3.5"/><ellipse cx="62" cy="-40" rx="6" ry="10" transform="rotate(40 62 -40)" fill="#4a88b0" stroke-width="3"/>'
           '<path d="M-14 -24 Q0 -46 14 -24" fill="none" stroke-width="5"/><path d="M-16 -16 L-14 10" stroke="#d8f0ff" stroke-width="3" opacity=".8"/></g>')
    b += frog(740, 1046, 2.75, look=(10, -8), mouth='O', shadow=True, armR='M38 -22 q22 -2 30 -22', armL='M-34 -22 q-18 4 -22 24', front=can)
    for k in range(12):   # water drops from the spout to the roots
        t = k / 11
        b += f'<ellipse cx="{1086 + t * 50:.0f}" cy="{810 + t * 140 + t * t * 10:.0f}" rx="3.5" ry="6" fill="#bfe8ff" opacity=".85"/>'
    lines = [('ONLY', 150, 'w'), ('ONE', 236, 'y'), ('SURVIVED', 150, 'w')]
    return page('#1c2050', svg(d, b), lines, outline='#070616', top=36)


if __name__ == '__main__':
    for n in (sys.argv[1:] or ['1', '2', '3', '4', '5']):
        out = os.path.join(VID, f'trilobite-extinction-short{n}', 'thumb', 'A.html')
        open(out, 'w').write(globals()[f'make_{n}']())
    print('ok')
