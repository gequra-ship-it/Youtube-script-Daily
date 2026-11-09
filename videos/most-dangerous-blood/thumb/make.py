# Thumbnails A-C for most-dangerous-blood (guideline 16-6, brief tools/briefs/thumb_art.md). Run: python3 videos/most-dangerous-blood/thumb/make.py
# A  FEWER THAN / 50 / PEOPLE   homage: Raiders of the Lost Ark (1981) golden idol on the temple pedestal in a shaft of light -> a glowing
#                               GOLDEN blood bag on the pedestal; frog explorer in a fedora holds the sandbag for the swap ("hardest to replace").
#                               Script: "Commonly cited estimates say fewer than fifty people in the world" (Rh-null, "golden blood").
# B  TYPE O'S / HIDDEN / TRAP   intuitive: a type-O blood bag drips into a test tube where the red cells clump into a glowing knot,
#                               next to a smooth normal tube. Script: Bombay phenotype "is a hidden trap"; "the samples clump together in the test tube".
# C  TOO RARE / TO / SAVE       homage: Hokusai, The Great Wave off Kanagawa (public domain): the boats are red-cell "ships" with antigen flags,
#                               one golden cell with no flags, Mt Fuji replaced by a blood-drop peak. Script: "being too rare for the world to save you";
#                               "each cell ... a small ship", "identification flags".
# Frog: A fedora + sandbag; B surgical cap + goggles behind the rack; C straw hat clinging to the golden cell boat.
import os, sys, math, random
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../tools'))
from thumb_lib import page, svg, lin, rad, spark

INK = '#1d2b1c'; GREEN = '#6aa55a'
FILTERS = ''.join(f'<filter id="b{s}" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="{s}"/></filter>'
                  for s in (2, 4, 6, 10, 16, 24, 50))


def orad(id, stops, cx=.5, cy=.5, r=.5, fx=None, fy=None):
    f = f' fx="{fx}" fy="{fy}"' if fx is not None else ''
    return (f'<radialGradient id="{id}" cx="{cx}" cy="{cy}" r="{r}"{f}>' +
            ''.join(f'<stop offset="{o}" stop-color="{c}" stop-opacity="{a}"/>' for o, c, a in stops) + '</radialGradient>')


# ---------------- red cells, flags, antibodies, bags, vials ----------------
CELL_DEFS = (orad('rBody', [(0, '#7d0d1c', 1), (.55, '#b81f31', 1), (.82, '#ec5763', 1), (.93, '#ff8a8a', 1), (1, '#b51c2e', 1)], cy=.46)
             + orad('rDim', [(0, '#4e0410', .9), (.6, '#6e0a18', .55), (1, '#7a0c1a', 0)])
             + orad('gBody', [(0, '#b9781a', 1), (.55, '#f0b53a', 1), (.82, '#ffe38a', 1), (.93, '#fffbe0', 1), (1, '#e0a12a', 1)], cy=.46)
             + orad('gDim', [(0, '#8a5408', .85), (.6, '#b07a14', .45), (1, '#c08a20', 0)])
             + orad('xBody', [(0, '#3a0a10', 1), (.6, '#6a1420', 1), (.85, '#92303a', 1), (1, '#5a1018', 1)], cy=.46)
             + orad('xDim', [(0, '#1a0206', .9), (1, '#2a0408', 0)]))
CELL = {'r': ('#6a0b18', '#3a0610', '#ffd0d0'), 'g': ('#a26a12', '#5a3606', '#fffbe6'), 'x': ('#2a060c', '#14020a', '#ff8080')}


def rbc(x, y, r, tilt=.5, rot=0, k='r', op=1, sw=None, hl=.5):
    """red blood cell (biconcave disc) seen at an angle; k: r red, g golden, x dark/clumped"""
    dk, ink, hc = CELL[k]; sw = sw or max(1.6, r * .035); ry = r * tilt
    g = f'<g transform="translate({x:.1f} {y:.1f}) rotate({rot})" opacity="{op}">'
    g += f'<ellipse cx="0" cy="{ry * .22:.1f}" rx="{r:.1f}" ry="{ry:.1f}" fill="{dk}" stroke="{ink}" stroke-width="{sw:.1f}"/>'
    g += f'<ellipse cx="0" cy="0" rx="{r:.1f}" ry="{ry:.1f}" fill="url(#{k}Body)" stroke="{ink}" stroke-width="{sw:.1f}"/>'
    g += f'<ellipse cx="{r * .02:.1f}" cy="{ry * .06:.1f}" rx="{r * .54:.1f}" ry="{ry * .5:.1f}" fill="url(#{k}Dim)"/>'
    g += f'<path d="M{-r * .42:.1f} {ry * .3:.1f} A{r * .5:.1f} {ry * .42:.1f} 0 0 0 {r * .42:.1f} {ry * .3:.1f}" fill="none" stroke="{hc}" stroke-width="{max(1.5, r * .04):.1f}" stroke-linecap="round" opacity=".35"/>'
    g += f'<path d="M{-r * .8:.1f} {-ry * .3:.1f} A{r * .86:.1f} {ry * .82:.1f} 0 0 1 {r * .5:.1f} {-ry * .66:.1f}" fill="none" stroke="{hc}" stroke-width="{max(1.8, r * .06):.1f}" stroke-linecap="round" opacity="{hl}"/>'
    return g + '</g>'


def flag(x, y, h, col, w=None, ink='#2a0a0e', sw=3, wave=1):
    w = w or h * .55
    g = f'<path d="M{x} {y} L{x} {y - h}" stroke="{ink}" stroke-width="{sw + 2}" stroke-linecap="round"/><path d="M{x} {y} L{x} {y - h}" stroke="#e8e0d0" stroke-width="{sw}" stroke-linecap="round"/>'
    g += (f'<path d="M{x} {y - h} q{w * .5:.1f} {-h * .12 * wave:.1f} {w:.1f} 0 l0 {h * .36:.1f} q{-w * .5:.1f} {-h * .12 * wave:.1f} {-w:.1f} 0z" '
          f'fill="{col}" stroke="{ink}" stroke-width="{sw * .8:.1f}" stroke-linejoin="round"/>')
    return g


def antibody(x, y, s, rot, col='#f2d27a', ink='#3a2a08', op=1):
    d = 'M0 0 L0 -22 M0 -22 L-13 -38 M0 -22 L13 -38'
    return (f'<g transform="translate({x:.1f} {y:.1f}) rotate({rot}) scale({s})" opacity="{op}" fill="none" stroke-linecap="round" stroke-linejoin="round">'
            f'<path d="{d}" stroke="{ink}" stroke-width="10"/><path d="{d}" stroke="{col}" stroke-width="5.5"/></g>')


def bagpath(x, y, w, h):
    hw = w / 2
    return (f'M{x - hw + 26} {y} L{x + hw - 26} {y} Q{x + hw} {y} {x + hw} {y + 30} L{x + hw} {y + h - 70} Q{x + hw} {y + h} {x + hw - 70} {y + h} '
            f'L{x - hw + 70} {y + h} Q{x - hw} {y + h} {x - hw} {y + h - 70} L{x - hw} {y + 30} Q{x - hw} {y} {x - hw + 26} {y}Z')


def bloodbag(id, x, y, w, h, liq, ink='#2a0508', level=.18, tag='O', tagcol='#f4efe2', sw=6, port=True):
    """blood bag, (x, y) = top centre. liq = fill (gradient url); tag 'O' = a label with a big ring (type O), None = plain label"""
    P = bagpath(x, y, w, h)
    g = f'<clipPath id="{id}"><path d="{P}"/></clipPath>'
    if port:
        for dx in (-w * .18, w * .18):
            g += f'<path d="M{x + dx:.1f} {y + h - 4} l0 {h * .14:.1f}" stroke="{ink}" stroke-width="{w * .1 + 6:.1f}" stroke-linecap="round"/><path d="M{x + dx:.1f} {y + h - 4} l0 {h * .14:.1f}" stroke="#d9d4cc" stroke-width="{w * .1:.1f}" stroke-linecap="round"/>'
    g += f'<path d="{P}" fill="#eef0f2" opacity=".35"/>'
    g += f'<g clip-path="url(#{id})"><path d="M{x - w} {y + h * level} q{w * .5:.1f} {-h * .05:.1f} {w} 0 t{w} 0 L{x + w} {y + h + 10} L{x - w} {y + h + 10}Z" fill="{liq}"/>'
    g += f'<rect x="{x - w / 2 + w * .1:.1f}" y="{y + h * .2:.1f}" width="{w * .09:.1f}" height="{h * .66:.1f}" rx="{w * .045:.1f}" fill="#fff" opacity=".45"/>'
    g += f'<rect x="{x + w / 2 - w * .16:.1f}" y="{y + h * .25:.1f}" width="{w * .05:.1f}" height="{h * .5:.1f}" rx="{w * .025:.1f}" fill="#fff" opacity=".18"/></g>'
    g += f'<path d="{P}" fill="none" stroke="{ink}" stroke-width="{sw}"/>'
    g += f'<rect x="{x - w / 2 + 10:.1f}" y="{y + 8}" width="{w - 20:.1f}" height="{h * .06:.1f}" rx="6" fill="#e6e2da" stroke="{ink}" stroke-width="{sw * .6:.1f}"/>'
    g += f'<circle cx="{x}" cy="{y + h * .03 + 8:.1f}" r="{w * .05:.1f}" fill="#1a1012" stroke="{ink}" stroke-width="2"/>'
    if tag:
        tw, th = w * .56, h * .36; tx, ty = x - tw / 2, y + h * .36
        g += f'<rect x="{tx:.1f}" y="{ty:.1f}" width="{tw:.1f}" height="{th:.1f}" rx="10" fill="{tagcol}" stroke="{ink}" stroke-width="{sw * .6:.1f}"/>'
        g += f'<rect x="{tx + 10:.1f}" y="{ty + 10:.1f}" width="{tw - 20:.1f}" height="{th * .16:.1f}" rx="4" fill="#c8303a"/>'
        if tag == 'O':
            g += f'<ellipse cx="{x}" cy="{ty + th * .6:.1f}" rx="{tw * .2:.1f}" ry="{th * .26:.1f}" fill="none" stroke="#1c1416" stroke-width="{tw * .1:.1f}"/>'
        elif tag == 'lines':
            for k in range(3):
                g += f'<rect x="{tx + 14:.1f}" y="{ty + th * (.36 + k * .2):.1f}" width="{(tw - 28) * (1 - k * .25):.1f}" height="{th * .08:.1f}" rx="3" fill="#8a8078" opacity=".7"/>'
    return g


def vial(id, x, y, w, h, liq, cap='#c8303a', ink='#2a1a08', level=.32, sw=5):
    """glass vial, (x, y) = bottom centre"""
    P = f'M{x - w / 2} {y - h} L{x - w / 2} {y - w / 2} A{w / 2} {w / 2} 0 0 0 {x + w / 2} {y - w / 2} L{x + w / 2} {y - h}Z'
    g = f'<clipPath id="{id}"><path d="{P}"/></clipPath><path d="{P}" fill="#e8f4ff" opacity=".22"/>'
    g += f'<g clip-path="url(#{id})"><path d="M{x - w} {y - h * (1 - level)} q{w * .5} {-w * .12} {w} 0 t{w} 0 L{x + w} {y + 4} L{x - w} {y + 4}Z" fill="{liq}"/>'
    g += f'<rect x="{x - w * .34:.1f}" y="{y - h * .9:.1f}" width="{w * .12:.1f}" height="{h * .82:.1f}" rx="{w * .06:.1f}" fill="#fff" opacity=".6"/>'
    g += f'<rect x="{x + w * .2:.1f}" y="{y - h * .8:.1f}" width="{w * .06:.1f}" height="{h * .6:.1f}" rx="{w * .03:.1f}" fill="#fff" opacity=".3"/></g>'
    g += f'<path d="{P}" fill="none" stroke="{ink}" stroke-width="{sw}"/>'
    g += f'<rect x="{x - w * .62:.1f}" y="{y - h - w * .5:.1f}" width="{w * 1.24:.1f}" height="{w * .56:.1f}" rx="{w * .12:.1f}" fill="{cap}" stroke="{ink}" stroke-width="{sw}"/>'
    g += f'<rect x="{x - w * .5:.1f}" y="{y - h - w * .42:.1f}" width="{w * .3:.1f}" height="{w * .12:.1f}" rx="4" fill="#fff" opacity=".45"/>'
    return g


# ---------------- mascot frog (tools/assets/frog.svg body; outfits per scene) ----------------
def frog(x, y, s, mouth='o', look=(0, 0), la='q-14 6 -16 22', ra='q14 6 16 22', back='', front='', hands=True, flip=False, extra='', head=''):
    sx = -s if flip else s
    g = f'<g transform="translate({x} {y}) scale({sx} {s})" stroke="{INK}" stroke-linejoin="round" stroke-linecap="round">' + back
    g += '<ellipse cx="-22" cy="4" rx="16" ry="9" fill="#4d8a4a" stroke-width="3.2"/><ellipse cx="22" cy="4" rx="16" ry="9" fill="#4d8a4a" stroke-width="3.2"/>'
    g += f'<path d="M-34 0 q-6 -64 34 -70 q40 -2 42 62 q0 10 -6 12 q-36 6 -70 -4z" fill="{GREEN}" stroke-width="4"/>'
    g += '<ellipse cx="2" cy="-12" rx="22" ry="20" fill="#9cc98a" stroke="none" opacity=".7"/>'
    g += '<path d="M-26 -50 q6 -16 22 -18" fill="none" stroke="#b9e0a6" stroke-width="3" opacity=".7"/>'
    dx, dy = look   # pupil r=5 inside white r=13.5: |look| <= 6 keeps it inside (tools/eyecheck.py)
    for ex in (-10, 22):
        g += f'<circle cx="{ex}" cy="-66" r="13.5" fill="#f4f5ea" stroke-width="3.2"/><circle cx="{ex + dx}" cy="{-66 + dy}" r="5" fill="{INK}" stroke="none"/>'
        g += f'<circle cx="{ex + dx + 1.6}" cy="{-66 + dy - 1.8}" r="1.6" fill="#fff" stroke="none"/>'
    g += '<ellipse cx="-18" cy="-46" rx="5" ry="3" fill="#e98a8a" stroke="none" opacity=".6"/><ellipse cx="30" cy="-46" rx="5" ry="3" fill="#e98a8a" stroke="none" opacity=".6"/>'
    if mouth == 'o':
        g += '<ellipse cx="6" cy="-42" rx="6.5" ry="8" fill="#7a2f33" stroke-width="3"/><ellipse cx="6" cy="-38" rx="3.5" ry="2.6" fill="#e07b7b" stroke="none"/>'
    else:
        g += '<path d="M-8 -45 q14 14 28 0 q-14 4 -28 0z" fill="#7a2f33" stroke-width="3"/>'
    g += extra + head
    for st, path in (('M-34 -22', la), ('M38 -22', ra)):
        g += f'<path d="{st} {path}" fill="none" stroke-width="7.5"/><path d="{st} {path}" fill="none" stroke="{GREEN}" stroke-width="3.4"/>'
        if hands:
            sx0, sy0 = map(float, st[1:].split()); q = [float(v) for v in path[1:].split()]
            g += f'<circle cx="{sx0 + q[2]}" cy="{sy0 + q[3]}" r="5.5" fill="{GREEN}" stroke-width="3"/>'
    return g + front + '</g>'


def hand_at(la):
    q = [float(v) for v in la[1:].split()]; return q[2], q[3]


def fedora(c='#8a6a44', band='#3a2616'):
    return (f'<path d="M-46 -80 q52 -16 104 0 q-52 14 -104 0z" fill="{c}" stroke-width="3.2"/>'
            f'<path d="M-24 -82 q-2 -34 12 -40 q14 6 18 0 q18 -4 20 40 q-26 6 -50 0z" fill="{c}" stroke-width="3.2"/>'
            f'<path d="M-24 -90 q26 6 50 0 l0 -8 q-26 6 -50 0z" fill="{band}" stroke-width="2.4"/>'
            '<path d="M-16 -116 q6 -4 12 2" fill="none" stroke="#c9a77a" stroke-width="2.4" opacity=".8"/>')


def scrubcap(c='#3f8fb0'):
    return (f'<path d="M-26 -80 q2 -36 34 -38 q34 0 38 36 q-36 -8 -72 2z" fill="{c}" stroke-width="3.2"/>'
            f'<path d="M-28 -78 q38 -12 78 -2 l-1 8 q-38 -10 -76 2z" fill="#2c6f8c" stroke-width="2.8"/>'
            '<path d="M-6 -106 q8 -4 16 0 M18 -110 q6 0 10 4" fill="none" stroke="#9fd2e6" stroke-width="2.4"/>')


def goggles():
    g = ''
    for ex in (-10, 22):
        g += f'<circle cx="{ex}" cy="-66" r="17.5" fill="none" stroke="{INK}" stroke-width="7"/><circle cx="{ex}" cy="-66" r="17.5" fill="none" stroke="#9fd8e6" stroke-width="3"/>'
    return g + f'<path d="M3.5 -68 l5 0" stroke="{INK}" stroke-width="4"/><path d="M-27 -66 l-9 2 M39 -66 l9 2" stroke="{INK}" stroke-width="4"/>'


def strawhat():
    g = '<path d="M-54 -78 q60 -64 120 0 q-60 12 -120 0z" fill="#e2b866" stroke-width="3.2"/>'
    g += ''.join(f'<path d="M6 -112 L{-48 + k * 18} {-79 + abs(k - 3) * .2}" stroke="#b58a3a" stroke-width="1.8" fill="none"/>' for k in range(7))
    return g + '<path d="M-20 -76 q-4 18 4 30 M32 -76 q4 18 -4 30" stroke="#8a5a2a" stroke-width="2.2" fill="none"/>'


def sweat(x, y, s=1):
    return f'<path d="M{x} {y} q{7 * s} {12 * s} 0 {18 * s} q{-7 * s} {-6 * s} 0 {-18 * s}z" fill="#dff6ff" stroke="{INK}" stroke-width="2.4"/>'


def vignette(id, a=.6, w=1920, h=1080):
    return rad(id, w / 2, h / 2, max(w, h) * .72, [(0, '#000', 0), (.6, '#000', 0), (1, '#000', a)])


def dust(n, x0, x1, y0, y1, col='#fff1c0', op=(.2, .8)):
    out = ''
    for _ in range(n):
        out += f'<circle cx="{random.randint(x0, x1)}" cy="{random.randint(y0, y1)}" r="{random.choice([1.4, 2, 2.8, 3.6])}" fill="{col}" opacity="{random.uniform(*op):.2f}"/>'
    return out


# ====================================================================== A  Raiders of the Lost Ark: golden blood on the pedestal
def thumb_A():
    random.seed(11)
    d = FILTERS + CELL_DEFS
    d += lin('aWall', [(0, '#120a08'), (.55, '#2a1810'), (1, '#1a0e08')])
    d += lin('aShaft', [(0, '#fff1c0'), (.7, '#f2c76a'), (1, '#f2c76a')], x2=0, y2=1)
    d += rad('aHalo', 1270, 430, 460, [(0, '#fff6d0', .95), (.25, '#ffd36a', .55), (.6, '#d88a2a', .18), (1, '#d88a2a', 0)])
    d += lin('aGold', [(0, '#fff6c8'), (.25, '#ffd760'), (.6, '#e7a12a'), (1, '#9a5a10')], x2=1, y2=1)
    d += lin('aStone', [(0, '#6a4a32'), (.45, '#a07854'), (.55, '#b88c62'), (1, '#4a3020')], x2=1, y2=0)
    d += lin('aStoneD', [(0, '#3a261a'), (.5, '#5a3e2a'), (1, '#2a1a10')], x2=1, y2=0)
    d += lin('aFloor', [(0, '#3a2618'), (1, '#120a06')])
    d += vignette('aVig', .72)
    b = '<rect width="1920" height="1080" fill="url(#aWall)"/>'
    # back wall stone blocks
    for row in range(9):
        y = row * 92; off = (row % 2) * 70
        for col in range(-1, 14):
            x = col * 150 + off; c = random.choice(['#2e1c12', '#36221a', '#2a1810', '#3a2618'])
            b += f'<rect x="{x + 3}" y="{y + 3}" width="144" height="86" rx="6" fill="{c}" opacity=".9"/>'
            b += f'<path d="M{x + 6} {y + 6} l136 0" stroke="#5a3a26" stroke-width="2" opacity=".4"/>'
    # carved red-cell reliefs on the wall
    for rx_, ry_, rr in ((1580, 240, 70), (1760, 420, 52), (940, 300, 46), (1820, 150, 40)):
        b += f'<g opacity=".55"><ellipse cx="{rx_}" cy="{ry_}" rx="{rr}" ry="{rr * .9}" fill="none" stroke="#5c3c26" stroke-width="10"/><ellipse cx="{rx_}" cy="{ry_}" rx="{rr * .45}" ry="{rr * .4}" fill="#1e120a"/>'
        b += f'<path d="M{rx_ - rr} {ry_} a{rr} {rr * .9} 0 0 1 {rr * 2} 0" fill="none" stroke="#8a6040" stroke-width="3"/></g>'
    # dark doorway arch behind the pedestal
    b += '<path d="M1010 920 L1010 330 Q1010 150 1270 140 Q1530 150 1530 330 L1530 920Z" fill="#0b0604"/>'
    b += '<path d="M1010 920 L1010 330 Q1010 150 1270 140 Q1530 150 1530 330 L1530 920" fill="none" stroke="#6a4a30" stroke-width="18"/>'
    b += '<path d="M988 920 L988 330 Q988 128 1270 116 Q1552 128 1552 330 L1552 920" fill="none" stroke="#2a1a10" stroke-width="10"/>'
    # pillars left/right of the arch
    for px in (880, 1590):
        b += f'<rect x="{px}" y="120" width="70" height="820" fill="url(#aStoneD)"/><rect x="{px - 14}" y="100" width="98" height="40" rx="6" fill="#4a3220"/>'
        for k in range(6):
            b += f'<circle cx="{px + 35}" cy="{240 + k * 120}" r="5" fill="#0a0503"/>'
    # light shaft from the ceiling
    b += '<path d="M1180 -10 L1360 -10 L1560 980 L980 980Z" fill="url(#aShaft)" opacity=".2" filter="url(#b16)"/>'
    b += '<path d="M1220 -10 L1320 -10 L1440 980 L1100 980Z" fill="#fff6d0" opacity=".12" filter="url(#b10)"/>'
    b += '<ellipse cx="1270" cy="430" rx="460" ry="460" fill="url(#aHalo)"/>'
    b += dust(90, 1060, 1480, 20, 900)
    # floor with perspective tiles
    b += '<path d="M0 900 L1920 900 L1920 1080 L0 1080Z" fill="url(#aFloor)"/>'
    for k in range(-12, 13):
        b += f'<path d="M{1270 + k * 26} 900 L{1270 + k * 190} 1080" stroke="#0a0604" stroke-width="3" opacity=".7"/>'
    for yy in (918, 944, 980, 1030):
        b += f'<path d="M0 {yy} L1920 {yy}" stroke="#0a0604" stroke-width="3" opacity=".6"/>'
    b += '<path d="M1218 944 L1322 944 L1340 980 L1200 980Z" fill="#f2c76a" opacity=".22"/>'  # the pressure-plate tile
    b += '<ellipse cx="1270" cy="960" rx="360" ry="40" fill="#f2c76a" opacity=".22" filter="url(#b16)"/>'
    # pedestal: steps, column, capital
    b += '<rect x="1040" y="930" width="460" height="50" rx="6" fill="url(#aStone)" stroke="#1a0e06" stroke-width="5"/>'
    b += '<rect x="1090" y="886" width="360" height="50" rx="6" fill="url(#aStone)" stroke="#1a0e06" stroke-width="5"/>'
    b += '<path d="M1160 890 L1170 640 L1370 640 L1380 890Z" fill="url(#aStone)" stroke="#1a0e06" stroke-width="5"/>'
    for yy in (700, 760, 820):
        b += f'<path d="M1168 {yy} L1372 {yy}" stroke="#4a3020" stroke-width="5" opacity=".7"/>'
    for k in range(4):
        b += f'<path d="M{1205 + k * 44} 712 l0 40 M{1205 + k * 44} 772 l0 40" stroke="#3a2416" stroke-width="5" opacity=".7"/>'
    b += '<rect x="1120" y="608" width="300" height="44" rx="8" fill="url(#aStone)" stroke="#1a0e06" stroke-width="5"/>'
    b += '<path d="M1130 614 L1410 614" stroke="#ffe4a0" stroke-width="4" opacity=".55"/>'
    b += '<path d="M1170 650 L1172 880" stroke="#ffe4a0" stroke-width="4" opacity=".3"/>'
    # the golden blood bag (the idol)
    b += '<ellipse cx="1270" cy="610" rx="160" ry="22" fill="#000" opacity=".45" filter="url(#b6)"/>'
    b += bloodbag('aBag', 1270, 250, 230, 340, 'url(#aGold)', ink='#3a2206', level=.12, tag='drop', tagcol='#fff4d6')
    # golden drop on the label instead of text lines
    b += '<path d="M1270 410 q34 46 0 64 q-34 -18 0 -64z" fill="#f2b33a" stroke="#3a2206" stroke-width="4"/>'
    b += '<path d="M1170 250 q100 -30 200 0" fill="none" stroke="#fff6d0" stroke-width="5" opacity=".6"/>'
    # rim light + glow on the bag
    b += '<path d="M1388 300 L1388 520" stroke="#fffbe0" stroke-width="7" opacity=".8" stroke-linecap="round"/>'
    b += '<rect x="1140" y="230" width="260" height="400" rx="40" fill="#ffd760" opacity=".14" filter="url(#b24)"/>'
    for sx, sy, ss in ((1110, 270, 26), (1440, 330, 34), (1420, 560, 18), (1120, 520, 20), (1300, 200, 22), (1500, 180, 16)):
        b += spark(sx, sy, ss, col='#fffbe0')
    # little golden red cells floating in the light
    b += rbc(1480, 450, 34, .45, 20, 'g', .9) + rbc(1060, 420, 26, .5, -15, 'g', .85) + rbc(1440, 700, 22, .5, 10, 'g', .7)
    # foreground cobwebs / dark rocks left
    b += '<path d="M600 1080 q40 -90 160 -110 q120 -10 170 110z" fill="#120a06"/>'
    # the frog explorer with the sandbag (swap!)
    sand = ('<g transform="translate(-58 -46) rotate(-12)"><path d="M-22 -8 q-6 -26 22 -28 q28 2 22 28 q-2 22 -22 22 q-20 0 -22 -22z" fill="#c9a26a" stroke-width="3.2"/>'
            '<path d="M-8 -34 l8 -10 l8 10" fill="none" stroke-width="3"/><path d="M-12 -2 q4 4 10 2 M4 4 q4 2 8 -2" fill="none" stroke="#8a6a3a" stroke-width="2"/></g>')
    whip = '<path d="M50 -4 q16 4 18 22 q2 16 -10 20 q-14 4 -14 -12" fill="none" stroke="#5a3418" stroke-width="5"/>'
    satchel = '<path d="M-30 -36 L42 -4" stroke="#6a4424" stroke-width="5"/><rect x="34" y="-14" width="22" height="18" rx="4" fill="#8a5a2e" stroke-width="2.6"/>'
    b += '<ellipse cx="800" cy="1046" rx="140" ry="18" fill="#000" opacity=".5" filter="url(#b6)"/>'
    b += frog(800, 1040, 3.0, mouth='o', look=(4, -2), la='q-16 -8 -22 -24', ra='q14 6 16 22', head=fedora(), extra=satchel + whip, front=sand)
    b += f'<rect width="1920" height="1080" fill="url(#aVig)"/>'
    lines = [('FEWER THAN', 128, 'w'), ('50', 330, 'y'), ('PEOPLE', 150, 'w')]
    return page('#120a08', svg(d, b), lines, outline='#120804', top=36)


# ====================================================================== B  intuitive: the type-O bag that clumps in the tube
def thumb_B():
    random.seed(22)
    d = FILTERS + CELL_DEFS
    d += lin('bBg', [(0, '#041218'), (.6, '#0a2a32'), (1, '#06161a')])
    d += rad('bGlow', 1180, 720, 420, [(0, '#ff5a4a', .75), (.35, '#ff3a3a', .3), (1, '#ff3a3a', 0)])
    d += rad('bCool', 1560, 260, 420, [(0, '#9ff0ff', .35), (1, '#9ff0ff', 0)])
    d += lin('bLiq', [(0, '#e0303a'), (.5, '#a8121e'), (1, '#5e0610')])
    d += lin('bPlasma', [(0, '#ffe9a8'), (1, '#f0c26a')])
    d += lin('bMetal', [(0, '#6a7a82'), (.5, '#e2eef2'), (1, '#4a5a62')], x2=1, y2=0)
    d += lin('bRack', [(0, '#e8eef0'), (1, '#9aaab0')])
    d += vignette('bVig', .7)
    b = '<rect width="1920" height="1080" fill="url(#bBg)"/>'
    # blurred lab shelves in the background
    for k in range(4):
        y = 140 + k * 190
        b += f'<rect x="760" y="{y}" width="1200" height="10" fill="#1f4a54" opacity=".6"/>'
        for j in range(9):
            x = 800 + j * 125 + random.randint(-20, 20); hh = random.randint(50, 110)
            b += f'<rect x="{x}" y="{y - hh}" width="{random.randint(30, 60)}" height="{hh}" rx="8" fill="{random.choice(["#16404a", "#1c4e58", "#2a5a5e"])}" opacity=".55" filter="url(#b4)"/>'
    # monitor with a heartbeat line (far back)
    b += '<rect x="1680" y="560" width="200" height="140" rx="14" fill="#0a1a1e" stroke="#2a4a52" stroke-width="6" opacity=".8"/>'
    b += '<path d="M1696 640 l40 0 l12 -30 l14 54 l12 -24 l90 0" fill="none" stroke="#6af0a0" stroke-width="5" opacity=".75"/>'
    b += '<rect width="1920" height="1080" fill="url(#bCool)"/>'
    # IV pole + bag (top right)
    b += '<path d="M1490 40 L1490 990" stroke="#0a1418" stroke-width="22"/><path d="M1490 40 L1490 990" stroke="url(#bMetal)" stroke-width="14"/>'
    b += '<path d="M1490 50 L1600 50 l0 26" fill="none" stroke="#0a1418" stroke-width="14" stroke-linecap="round"/><path d="M1490 50 L1600 50 l0 26" fill="none" stroke="#c8d6dc" stroke-width="7" stroke-linecap="round"/>'
    b += '<path d="M1410 990 L1570 990 M1440 990 L1490 950 L1540 990" stroke="#c8d6dc" stroke-width="10" fill="none" stroke-linecap="round"/>'
    for wx in (1410, 1570):
        b += f'<circle cx="{wx}" cy="1004" r="14" fill="#1a2a30" stroke="#0a1418" stroke-width="4"/>'
    b += '<ellipse cx="1600" cy="300" rx="190" ry="250" fill="#ff4a4a" opacity=".12" filter="url(#b24)"/>'
    b += bloodbag('bBag', 1600, 80, 240, 360, 'url(#bLiq)', level=.16, tag='O')
    # drip tube from the bag down into the test tube
    b += '<path d="M1556 486 C1556 640 1330 560 1250 430 C1220 380 1200 330 1196 300" fill="none" stroke="#0a1418" stroke-width="16" stroke-linecap="round"/>'
    b += '<path d="M1556 486 C1556 640 1330 560 1250 430 C1220 380 1200 330 1196 300" fill="none" stroke="#c42a36" stroke-width="8" stroke-linecap="round"/>'
    b += '<path d="M1196 300 L1196 350" stroke="#0a1418" stroke-width="12" stroke-linecap="round"/><path d="M1196 300 L1196 350" stroke="#d8e6ea" stroke-width="6" stroke-linecap="round"/>'
    b += '<path d="M1196 366 q10 16 0 26 q-10 -10 0 -26z" fill="#e0303a" stroke="#2a0508" stroke-width="3"/>'
    # rack (behind the tubes' lower part)
    b += '<rect x="760" y="820" width="640" height="56" rx="12" fill="url(#bRack)" stroke="#0a1418" stroke-width="6"/>'
    b += '<rect x="760" y="950" width="640" height="40" rx="10" fill="#7a8a90" stroke="#0a1418" stroke-width="6"/>'
    for lx in (790, 1370):
        b += f'<rect x="{lx - 12}" y="860" width="24" height="100" fill="#8a9aa0" stroke="#0a1418" stroke-width="5"/>'
    # normal tube (smooth red) on the left
    b += vial('bT1', 900, 960, 92, 420, 'url(#bLiq)', cap='#5a6a70', ink='#0a1418', level=.55)
    # main tube: plasma + clumped cells, glowing alarm
    b += '<ellipse cx="1190" cy="720" rx="420" ry="420" fill="url(#bGlow)"/>'
    T = 'M1100 380 L1100 900 A90 90 0 0 0 1280 900 L1280 380Z'
    b += f'<clipPath id="bTube"><path d="{T}"/></clipPath><path d="{T}" fill="#e8f4ff" opacity=".2"/>'
    b += '<g clip-path="url(#bTube)"><path d="M1060 520 q60 -14 120 0 t120 0 L1300 1010 L1060 1010Z" fill="url(#bPlasma)" opacity=".85"/>'
    # clump: knot of cells stuck together + antibodies binding them
    clump = [(1190, 820, 48, 20), (1150, 770, 40, -30), (1232, 770, 42, 35), (1160, 870, 40, 10), (1228, 870, 44, -20), (1190, 730, 36, 5),
             (1140, 830, 34, 60), (1244, 826, 36, -55), (1192, 900, 38, 0), (1200, 780, 40, 80)]
    b += '<ellipse cx="1190" cy="820" rx="120" ry="140" fill="#ff5a3a" opacity=".55" filter="url(#b16)"/>'
    for cx, cy, r, rot in clump:
        b += rbc(cx, cy, r, .55, rot, 'r')
    for ax, ay, rot in ((1166, 790, -40), (1214, 800, 30), (1188, 858, 180), (1150, 852, -120), (1232, 840, 120), (1196, 752, 0)):
        b += antibody(ax, ay, .9, rot)
    for cx, cy, r, rot in ((1140, 580, 28, 20), (1240, 630, 24, -30), (1170, 670, 22, 50)):
        b += rbc(cx, cy, r, .5, rot, 'r', .95)
    b += '<rect x="1118" y="400" width="18" height="520" rx="9" fill="#fff" opacity=".45"/><rect x="1250" y="420" width="8" height="440" rx="4" fill="#fff" opacity=".25"/></g>'
    b += f'<path d="{T}" fill="none" stroke="#0a1418" stroke-width="7"/>'
    b += '<rect x="1086" y="362" width="208" height="26" rx="8" fill="#d8e6ea" stroke="#0a1418" stroke-width="6"/>'
    # crackle sparks around the clump
    for sx, sy, ss in ((1060, 760, 26), (1330, 700, 30), (1320, 900, 20), (1050, 900, 18), (1290, 600, 16)):
        b += spark(sx, sy, ss, col='#ffe0c0')
    for k in range(6):
        a = k * 60 + 15; r0, r1 = 120, 175
        b += f'<path d="M{1190 + r0 * math.cos(math.radians(a)):.0f} {820 + r0 * math.sin(math.radians(a)):.0f} L{1190 + r1 * math.cos(math.radians(a)):.0f} {820 + r1 * math.sin(math.radians(a)):.0f}" stroke="#ffd0a0" stroke-width="5" stroke-linecap="round" opacity=".55"/>'
    # rack front bar over the tubes
    b += '<rect x="760" y="820" width="640" height="30" rx="10" fill="url(#bRack)" stroke="#0a1418" stroke-width="6"/>'
    # frog: surgical cap + goggles, peeking from behind the rack (left)
    b += frog(640, 1010, 2.9, mouth='o', look=(5, -2), la='q-10 -10 -4 -30', ra='q20 -8 26 -30', head=scrubcap(), extra=goggles(), front=sweat(-36, -96))
    b += f'<rect width="1920" height="1080" fill="url(#bVig)"/>'
    lines = [('WHICH BLOOD', 140, 'w'), ('TYPE IS', 140, 'w'), ('DEADLY?', 170, 'y')]
    return page('#041218', svg(d, b), lines, outline='#03080c', top=40)


# ====================================================================== C  Great Wave homage: red-cell boats, one golden
def thumb_C():
    random.seed(33)
    d = FILTERS + CELL_DEFS
    d += lin('cSky', [(0, '#e9dbb8'), (.6, '#f3e8cc'), (1, '#e6d4aa')])
    d += lin('cWave', [(0, '#3d76a6'), (.45, '#1c477a'), (1, '#0c2446')], x2=0, y2=1)
    d += lin('cWave2', [(0, '#5a92bf'), (1, '#1e4c7c')], x2=0, y2=1)
    d += lin('cDrop', [(0, '#e8505c'), (.6, '#a8121e'), (1, '#6a0814')])
    d += rad('cGold', 1000, 760, 260, [(0, '#fff3a8', .95), (.35, '#ffd760', .5), (1, '#ffd760', 0)])
    d += vignette('cVig', .45)
    b = '<rect width="1920" height="1080" fill="url(#cSky)"/>'
    for _ in range(260):   # paper grain
        b += f'<circle cx="{random.randint(0, 1920)}" cy="{random.randint(0, 1080)}" r="{random.choice([1, 1.6, 2.2])}" fill="#b89a66" opacity="{random.uniform(.08, .25):.2f}"/>'
    # soft clouds
    for cx, cy, rx in ((520, 690, 260), (300, 760, 200)):
        b += f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="34" fill="#d6c294" opacity=".7"/>'
    # distant blood-drop "Mt Fuji"
    b += '<path d="M470 880 C560 860 600 760 640 690 C680 760 720 860 810 880Z" fill="url(#cDrop)" stroke="#3a0610" stroke-width="5"/>'
    b += '<path d="M612 740 C626 712 634 700 640 690 C646 700 654 712 668 740 q-14 -8 -28 6 q-14 -14 -28 -6z" fill="#fff4e6" stroke="#3a0610" stroke-width="3"/>'
    # far trough swell (left)
    b += '<path d="M0 900 C200 830 340 840 460 880 C600 930 760 900 900 860 L900 1080 L0 1080Z" fill="url(#cWave2)" stroke="#0c2446" stroke-width="5"/>'
    for k in range(4):
        b += f'<path d="M{40 + k * 220} {930 + k * 8} q90 -40 180 -8" fill="none" stroke="#e8f0f0" stroke-width="4" opacity=".7"/>'
    # THE wave: big body on the right curling over to the left
    W1 = ('M700 1080 C860 990 1000 880 1090 720 C1170 570 1240 380 1400 250 C1520 150 1700 120 1820 170 C1900 200 1930 260 1920 320 '
          'L1920 1080Z')
    b += f'<path d="{W1}" fill="url(#cWave)" stroke="#0a1e3c" stroke-width="6"/>'
    # stripes following the body
    for k in range(9):
        o = k * 26
        b += (f'<path d="M{760 + o * 1.3:.0f} 1080 C{900 + o:.0f} {990 - o * .2:.0f} {1030 + o:.0f} {880 - o * .1:.0f} {1120 + o:.0f} {730 + o * .1:.0f} '
              f'C{1200 + o:.0f} {590 + o * .3:.0f} {1270 + o * .8:.0f} {420 + o * .7:.0f} {1420 + o * .6:.0f} {300 + o * .7:.0f}" fill="none" stroke="#7fb0d6" stroke-width="3" opacity="{.5 - k * .04:.2f}"/>')
    # the curling lip (hollow underside + overhanging crest)
    LIP = 'M1420 236 C1290 206 1150 246 1060 330 C984 404 956 486 984 566 C1024 524 1076 494 1140 484 C1180 420 1250 370 1330 342 C1380 322 1412 290 1420 236Z'
    b += f'<path d="{LIP}" fill="#2a5c8e" stroke="#0a1e3c" stroke-width="6"/>'
    b += '<path d="M1390 262 C1290 262 1180 304 1110 366 C1050 420 1010 480 1004 530" fill="none" stroke="#9cc4e2" stroke-width="5" opacity=".7"/>'
    # foam "claws" along the crest and lip
    random.seed(4)
    crest = [(1820, 170), (1720, 136), (1620, 136), (1520, 160), (1440, 210), (1360, 240), (1270, 252), (1190, 280), (1120, 310), (1060, 356), (1010, 414), (982, 480), (980, 548)]
    for i, (fx, fy) in enumerate(crest):
        for j in range(3):
            ox, oy = random.randint(-14, 14), random.randint(-10, 10); rr = random.randint(16, 26)
            b += f'<circle cx="{fx + ox}" cy="{fy + oy}" r="{rr}" fill="#f6f2e4" stroke="#0a1e3c" stroke-width="4"/>'
        if i > 4:
            for t in range(3):
                ang = math.radians(100 + t * 25 + i * 3); L = 34 + t * 6
                b += f'<path d="M{fx} {fy + 10} q{L * math.cos(ang) * .5:.0f} {L * math.sin(ang) * .3:.0f} {L * math.cos(ang):.0f} {L * math.sin(ang):.0f}" fill="none" stroke="#0a1e3c" stroke-width="12" stroke-linecap="round"/>'
                b += f'<path d="M{fx} {fy + 10} q{L * math.cos(ang) * .5:.0f} {L * math.sin(ang) * .3:.0f} {L * math.cos(ang):.0f} {L * math.sin(ang):.0f}" fill="none" stroke="#f6f2e4" stroke-width="7" stroke-linecap="round"/>'
    # spray droplets falling from the lip (foam flecks)
    for _ in range(40):
        x, y = random.randint(900, 1500), random.randint(260, 640)
        b += f'<circle cx="{x}" cy="{y}" r="{random.choice([4, 6, 8])}" fill="#f6f2e4" stroke="#0a1e3c" stroke-width="2.4"/>'
    # boats = red cells with antigen flags riding the trough
    for cx, cy, r, rot, fl in ((1350, 700, 105, -24, ('#f2d27a', '#7fd0e6')), (1560, 560, 74, -32, ('#9be08a', '#e66a9a')), (780, 880, 70, -8, ('#7fd0e6', '#f2d27a'))):
        b += rbc(cx, cy, r, .42, rot, 'r', sw=4)
        for k, c in enumerate(fl):
            fx = cx + (k - .5) * r * .8; fy = cy + (k - .5) * r * .8 * math.tan(math.radians(rot)) - r * .1
            b += flag(fx, fy, r * .7, c, sw=3)
    # golden cell boat (no flags) + frog
    b += '<ellipse cx="1000" cy="770" rx="300" ry="300" fill="url(#cGold)"/>'
    b += rbc(1000, 810, 165, .42, -12, 'g', sw=5, hl=.8)
    for sx, sy, ss in ((830, 700, 26), (1180, 690, 22), (880, 880, 16), (1150, 860, 18), (1010, 610, 16)):
        b += spark(sx, sy, ss, col='#fffbe0')
    b += frog(1000, 806, 2.05, mouth='o', look=(4, -3), la='q-18 -2 -26 18', ra='q18 -2 26 18', head=strawhat())
    b += rbc(1000, 810, 165, .42, -12, 'g', sw=5, hl=.0).replace('<g transform', '<g clip-path="url(#cFront)" transform')  # front rim over the frog's feet
    d += '<clipPath id="cFront"><rect x="820" y="812" width="380" height="140"/></clipPath>'
    # foreground swell with foam over the boats' bottoms
    b += '<path d="M500 1080 C620 980 760 930 880 950 C980 966 1060 900 1140 860 C1230 820 1300 860 1360 900 C1460 960 1600 960 1720 1000 C1800 1030 1880 1040 1920 1040 L1920 1080Z" fill="url(#cWave2)" stroke="#0a1e3c" stroke-width="5"/>'
    for fx, fy in ((880, 950), (1140, 862), (1360, 900)):
        for j in range(4):
            b += f'<circle cx="{fx - 30 + j * 20}" cy="{fy - 4 + (j % 2) * 6}" r="{12 + j % 2 * 4}" fill="#f6f2e4" stroke="#0a1e3c" stroke-width="3"/>'
    for k in range(5):
        b += f'<path d="M{620 + k * 220} {1040 - k * 6} q80 -30 160 -6" fill="none" stroke="#e8f0f0" stroke-width="4" opacity=".6"/>'
    b += f'<rect width="1920" height="1080" fill="url(#cVig)"/>'
    lines = [('TOO RARE', 172, 'w'), ('TO', 110, 'w'), ('SAVE', 250, 'y')]
    return page('#e9dbb8', svg(d, b), lines, outline='#0c1a30', top=36)


if __name__ == '__main__':
    for n, fn in (('A', thumb_A), ('B', thumb_B), ('C', thumb_C)):
        open(os.path.join(HERE, f'{n}.html'), 'w').write(fn())
    print('ok')
