# Thumbnails A-C for eating-humans-deadly-bet (guideline 16-6/16-8, brief tools/briefs/thumb_art.md). Run: python3 videos/eating-humans-deadly-bet/thumb/make.py
# Sensitive topic: metaphor objects only (no bodies, blood, bones, people eating).
# A  CAN YOU COOK IT?          homage: The Last Supper (Leonardo; long table, central figure = frog under the bright window, one covered dish).  S12 "Can You Cook It?"
# B  THE LAUGHING DEATH        intuitive: sponge brain full of holes + a chain of keys bending one another (S03 nickname, S07 spongiform, S10 bent key)
# C  HALF A DAY VS 2 MONTHS    intuitive: balance scale, a woolly mammoth outweighs an empty plate (S24: muscle lasts about half a day, a mammoth about two months)
import os, sys, math, random
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../tools'))
from thumb_lib import page, svg, lin, rad, spark

INK = '#1d2b1c'; GREEN = '#6aa55a'

FILTERS = ''.join(f'<filter id="b{d}" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="{d}"/></filter>' for d in (3, 6, 12, 24, 50))


# ---------------- mascot frog (tools/assets/frog.svg body; outfit layers vary) ----------------
def frog(x, y, s, mouth='o', arms=('q-14 6 -16 22', 'q14 6 16 22'), look=(2, 0), back='', torso='', head='', front='', flip=False, sweat=False):
    sx = -s if flip else s
    g = f'<g transform="translate({x} {y}) scale({sx} {s})" stroke="{INK}" stroke-linejoin="round" stroke-linecap="round">'
    g += back
    g += '<ellipse cx="-22" cy="4" rx="16" ry="9" fill="#4d8a4a" stroke-width="3.2"/><ellipse cx="22" cy="4" rx="16" ry="9" fill="#4d8a4a" stroke-width="3.2"/>'
    g += f'<path d="M-34 0 q-6 -64 34 -70 q40 -2 42 62 q0 10 -6 12 q-36 6 -70 -4z" fill="{GREEN}" stroke-width="4"/>'
    g += '<ellipse cx="2" cy="-12" rx="22" ry="20" fill="#9cc98a" stroke="none" opacity=".7"/>'
    g += '<path d="M-26 -50 q6 -16 22 -18" fill="none" stroke="#b9e0a6" stroke-width="3" opacity=".7"/>'
    g += torso
    dx, dy = look
    for ex in (-10, 22):
        g += f'<circle cx="{ex}" cy="-66" r="13" fill="#e3e5d6" stroke-width="3.2"/><circle cx="{ex + dx}" cy="{-66 + dy}" r="5" fill="{INK}" stroke="none"/>'
        g += f'<circle cx="{ex + 2 + dx * .6}" cy="{-68 + dy}" r="1.7" fill="#fff" stroke="none"/>'
    g += '<ellipse cx="-18" cy="-46" rx="5" ry="3" fill="#e98a8a" stroke="none" opacity=".55"/><ellipse cx="30" cy="-46" rx="5" ry="3" fill="#e98a8a" stroke="none" opacity=".55"/>'
    if mouth == 'o':
        g += '<ellipse cx="6" cy="-42" rx="6.5" ry="8" fill="#7a2f33" stroke-width="3"/><ellipse cx="6" cy="-38" rx="3.5" ry="2.6" fill="#e07b7b" stroke="none"/>'
    elif mouth == 'yuck':   # wavy, queasy mouth + small tongue
        g += '<path d="M-7 -42 q4 -5 7 0 q4 5 7 0 q4 -5 7 0 q4 5 6 1" fill="none" stroke-width="3.2"/>'
    else:
        g += '<path d="M-8 -45 q14 14 28 0 q-14 4 -28 0z" fill="#7a2f33" stroke-width="3"/>'
    if sweat:
        g += '<path d="M40 -84 q6 9 0 13 q-6 -4 0 -13z" fill="#bfe8ff" stroke-width="2.2"/>'
    g += head
    la, ra = arms
    for st, path in (('M-32 -22', la), ('M38 -22', ra)):
        g += f'<path d="{st} {path}" fill="none" stroke-width="7.5"/><path d="{st} {path}" fill="none" stroke="{GREEN}" stroke-width="3.4"/>'
        sx0, sy0 = map(float, st[1:].split()); q = [float(v) for v in path[1:].split()]
        g += f'<circle cx="{sx0 + q[2]}" cy="{sy0 + q[3]}" r="5.5" fill="{GREEN}" stroke-width="3"/>'
    g += front
    return g + '</g>'


# ======================= A: The Last Supper =======================
def thumb_A():
    random.seed(3)
    VX, VY = 1180, 470
    defs = FILTERS
    defs += lin('wallA', [(0, '#7b6a52'), (1, '#4a3d2e')])
    defs += lin('ceilA', [(0, '#1c1712'), (1, '#3a3026')])
    defs += lin('skyA', [(0, '#a9cfd8'), (.7, '#f3e6c2'), (1, '#ffe9b5')])
    defs += lin('clothA', [(0, '#f4ecdc'), (1, '#b9ab93')])
    defs += lin('cloche', [(0, '#ffffff'), (.35, '#d9dde2'), (.7, '#8c939c'), (1, '#4c525a')], x2=1, y2=0)
    defs += rad('haloA', 1180, 440, 520, [(0, '#fff2c8', .85), (.3, '#ffd98a', .35), (1, '#ffd98a', 0)])
    defs += rad('vigA', 960, 540, 1150, [(0, '#000', 0), (.65, '#000', 0), (1, '#000', .6)])
    b = '<rect width="1920" height="1080" fill="#2a221a"/>'
    # back wall + coffered ceiling + side walls in one-point perspective (vanishing point behind the frog's head)
    BW = (760, 200, 1600, 700)
    b += f'<rect x="{BW[0]}" y="{BW[1]}" width="{BW[2] - BW[0]}" height="{BW[3] - BW[1]}" fill="url(#wallA)"/>'
    b += f'<path d="M0 0 L1920 0 L{BW[2]} {BW[1]} L{BW[0]} {BW[1]} Z" fill="url(#ceilA)"/>'
    for i in range(1, 9):   # coffer beams converging
        x0 = i * 1920 / 9; x1 = BW[0] + (BW[2] - BW[0]) * i / 9
        b += f'<path d="M{x0:.0f} 0 L{x1:.0f} {BW[1]}" stroke="#57483a" stroke-width="{7 - i * .3:.1f}" opacity=".8"/>'
    for t in (.25, .5, .72, .88):   # cross beams
        y = BW[1] * t; xl = BW[0] * t; xr = 1920 - (1920 - BW[2]) * t
        b += f'<path d="M{xl:.0f} {y:.0f} L{xr:.0f} {y:.0f}" stroke="#57483a" stroke-width="{10 * (1 - t) + 3:.0f}" opacity=".8"/>'
    b += f'<path d="M0 0 L{BW[0]} {BW[1]} L{BW[0]} {BW[3]} L0 1080 Z" fill="#3a3027"/>'
    b += f'<path d="M1920 0 L{BW[2]} {BW[1]} L{BW[2]} {BW[3]} L1920 1080 Z" fill="#3f342a"/>'
    # tapestries on the side walls (receding dark panels with gold borders)
    def panel(side, t0, t1):
        def pt(t, v):   # t: depth 0 (front) .. 1 (back wall); v: 0 top .. 1 bottom
            if side < 0:
                x = BW[0] * t; top = BW[1] * t; bot = 1080 - (1080 - BW[3]) * t
            else:
                x = 1920 - (1920 - BW[2]) * t; top = BW[1] * t; bot = 1080 - (1080 - BW[3]) * t
            y = top + (bot - top) * (.18 + .5 * v)
            return f'{x:.0f},{y:.0f}'
        return (f'<polygon points="{pt(t0, 0)} {pt(t1, 0)} {pt(t1, 1)} {pt(t0, 1)}" fill="#2b2c36" stroke="#b8924e" stroke-width="5"/>'
                f'<polygon points="{pt(t0 + .02, .15)} {pt(t1 - .02, .15)} {pt(t1 - .02, .85)} {pt(t0 + .02, .85)}" fill="none" stroke="#6c5a3c" stroke-width="3"/>')
    for t0, t1 in ((.62, .74), (.78, .86), (.89, .95)):
        b += panel(1, t0, t1)
    for t0, t1 in ((.62, .74), (.78, .86), (.89, .95)):
        b += panel(-1, t0, t1)
    # three windows, the centre one bright behind the frog's head
    def window(x0, y0, x1, y1, arch=False):
        w = ''
        w += f'<rect x="{x0 - 14}" y="{y0 - 14}" width="{x1 - x0 + 28}" height="{y1 - y0 + 28}" fill="#3a2f24"/>'
        w += f'<rect x="{x0}" y="{y0}" width="{x1 - x0}" height="{y1 - y0}" fill="url(#skyA)"/>'
        hy = y0 + (y1 - y0) * .72
        w += f'<path d="M{x0} {hy} Q{x0 + (x1 - x0) * .3} {hy - 40} {x0 + (x1 - x0) * .55} {hy - 12} T{x1} {hy - 20} L{x1} {y1} L{x0} {y1} Z" fill="#6f96a4" opacity=".85"/>'
        w += f'<path d="M{x0} {hy + 30} Q{x0 + (x1 - x0) * .5} {hy - 6} {x1} {hy + 24} L{x1} {y1} L{x0} {y1} Z" fill="#4f7480"/>'
        for k in range(4):
            tx = x0 + (x1 - x0) * (.15 + .22 * k); ty = hy + 22 - (k % 2) * 8
            w += f'<path d="M{tx:.0f} {ty:.0f} l-6 -20 l6 -14 l6 14 z" fill="#3c5a50"/>'
        if arch:
            cx = (x0 + x1) / 2; r = (x1 - x0) / 2 + 40
            w += f'<path d="M{cx - r} {y0 - 14} A{r} {r * .55} 0 0 1 {cx + r} {y0 - 14}" fill="none" stroke="#8a7350" stroke-width="16"/>'
        return w
    b += window(860, 300, 990, 600) + window(1370, 300, 1500, 600)
    b += '<rect width="1920" height="1080" fill="url(#haloA)"/>'
    b += window(1060, 270, 1300, 660, arch=True)
    b += '<ellipse cx="1180" cy="440" rx="190" ry="210" fill="#fff6dc" opacity=".35" filter="url(#b50)"/>'
    # floor
    b += '<path d="M0 1080 L760 700 L1600 700 L1920 1080 Z" fill="#241c15"/>'
    for i in range(-8, 9):
        b += f'<path d="M{VX + i * 52:.0f} 700 L{VX + i * 260:.0f} 1080" stroke="#33281e" stroke-width="3"/>'
    # the frog, red tunic + blue mantle (the painting's colours), arms spread on the table
    robe = ('<path d="M-30 -36 q32 14 64 0 l6 40 q-38 8 -74 -2z" fill="#b2392f" stroke-width="3.4"/>'
            '<path d="M-6 -30 l12 18 l12 -18" fill="none" stroke="#f2d27a" stroke-width="2.6"/>'
            '<path d="M14 -38 q30 -4 34 30 l-4 18 q-20 -6 -26 -30z" fill="#3e5f9e" stroke-width="3.2"/>'
            '<path d="M22 -30 q16 2 20 22" fill="none" stroke="#7fa2dc" stroke-width="2.4"/>')
    b += frog(1170, 712, 4.3, mouth='yuck', arms=('q-34 4 -62 25', 'q34 4 62 25'), look=(1, 5), torso=robe, sweat=True)
    # table: top surface + hanging cloth with folds
    TL, TR, TY = 230, 1760, 712
    b += f'<path d="M{TL + 30} {TY - 26} L{TR - 30} {TY - 26} L{TR} {TY + 14} L{TL} {TY + 14} Z" fill="#efe6d4"/>'
    b += f'<rect x="{TL}" y="{TY + 14}" width="{TR - TL}" height="210" fill="url(#clothA)"/>'
    for i in range(0, 40):
        x = TL + 20 + i * (TR - TL - 40) / 39
        b += f'<path d="M{x:.0f} {TY + 18} q{random.uniform(-8, 8):.0f} 100 {random.uniform(-6, 6):.0f} 202" stroke="#a49478" stroke-width="{random.uniform(2, 5):.1f}" fill="none" opacity=".55"/>'
    for yy in (TY + 70, TY + 84):   # blue woven stripes
        b += f'<path d="M{TL} {yy} L{TR} {yy}" stroke="#6b84a8" stroke-width="5" opacity=".7"/>'
    b += ''.join(f'<path d="M{TL + 40 + k * 76} {TY + 77} l16 -6 l16 6 l-16 6z" fill="#6b84a8" opacity=".6"/>' for k in range(20))
    b += f'<path d="M{TL} {TY + 224} Q{(TL + TR) / 2} {TY + 236} {TR} {TY + 224}" stroke="#7e6f58" stroke-width="5" fill="none"/>'
    # untouched place settings left and right
    def setting(x, y, sc):
        g = f'<g transform="translate({x} {y}) scale({sc})">'
        g += '<ellipse cx="0" cy="0" rx="46" ry="10" fill="#cfc6b2" stroke="#7a6a52" stroke-width="2.5"/><ellipse cx="0" cy="-1" rx="30" ry="6" fill="#e8e1d0"/>'
        g += '<path d="M54 2 l4 -34 q-12 -2 -14 -20 l28 0 q-2 18 -14 20 l4 34 z" fill="#a8b8b4" stroke="#56615e" stroke-width="2.5" opacity=".9"/>'
        g += '<ellipse cx="-62" cy="-4" rx="18" ry="11" fill="#c98c4c" stroke="#6b4423" stroke-width="2.5"/><path d="M-72 -8 q10 -6 20 0" stroke="#f0c48a" stroke-width="2" fill="none"/>'
        return g + '</g>'
    for x in (330, 470, 610, 750, 890):
        b += setting(x, TY - 6, .9)
    for x in (1460, 1600):
        b += setting(x, TY - 6, .9)
    b += '<g transform="translate(1690 640)"><path d="M-22 64 q-12 -40 6 -62 l-4 -14 l40 0 l-4 14 q18 22 6 62z" fill="#8a6a44" stroke="#3e2c19" stroke-width="3"/><path d="M-10 10 q-6 20 0 40" stroke="#d9b07a" stroke-width="4" fill="none"/></g>'
    # light shafts from the windows onto the table
    b += '<path d="M1060 270 L1300 270 L1520 712 L840 712 Z" fill="#fff1c8" opacity=".10" filter="url(#b12)"/>'
    b += f'<ellipse cx="1180" cy="600" rx="260" ry="150" fill="#fff6dc" opacity=".25" filter="url(#b50)"/>'
    # the covered dish in front of the frog (uneaten), lit from the window behind
    CX, CY = 1180, TY - 4
    b += f'<ellipse cx="{CX}" cy="{CY + 8}" rx="190" ry="26" fill="#000" opacity=".35" filter="url(#b6)"/>'
    b += f'<ellipse cx="{CX}" cy="{CY}" rx="176" ry="26" fill="#e6e8ea" stroke="#4c525a" stroke-width="4"/>'
    b += f'<path d="M{CX - 146} {CY - 6} C{CX - 146} {CY - 160} {CX + 146} {CY - 160} {CX + 146} {CY - 6} Q{CX} {CY + 14} {CX - 146} {CY - 6} Z" fill="url(#cloche)" stroke="#3e434a" stroke-width="4"/>'
    b += f'<path d="M{CX - 112} {CY - 40} C{CX - 112} {CY - 110} {CX - 40} {CY - 126} {CX - 10} {CY - 124}" stroke="#fff" stroke-width="10" fill="none" opacity=".8" stroke-linecap="round"/>'
    b += f'<path d="M{CX - 138} {CY - 60} C{CX - 120} {CY - 134} {CX + 120} {CY - 134} {CX + 138} {CY - 60}" stroke="#fff4cf" stroke-width="5" fill="none" opacity=".9" filter="url(#b3)"/>'
    b += f'<path d="M{CX - 146} {CY - 6} Q{CX} {CY + 14} {CX + 146} {CY - 6}" stroke="#9aa1aa" stroke-width="8" fill="none"/>'
    b += f'<ellipse cx="{CX}" cy="{CY - 120}" rx="22" ry="9" fill="#c4c9cf" stroke="#3e434a" stroke-width="3.5"/><circle cx="{CX}" cy="{CY - 134}" r="13" fill="#e9ecef" stroke="#3e434a" stroke-width="3.5"/>'
    # steam leaking from under the lid, carrying tiny bent purple proteins that survive the heat
    for sx, dirn in ((CX - 150, -1), (CX + 150, 1)):
        b += f'<path d="M{sx} {CY - 8} c{dirn * 30} -40 {dirn * -10} -80 {dirn * 24} -130 s{dirn * -20} -90 {dirn * 10} -130" stroke="#fff" stroke-width="14" fill="none" opacity=".35" filter="url(#b6)" stroke-linecap="round"/>'
    for (px, py, r) in ((CX - 205, 560, 0), (CX + 215, 520, 40), (CX - 170, 450, -30), (CX + 190, 410, 20)):
        b += f'<g transform="translate({px} {py}) rotate({r})"><circle r="26" fill="#c46cff" opacity=".45" filter="url(#b6)"/><path d="M-16 8 q-6 -16 6 -18 q14 -2 10 10 q-4 10 10 6 l6 -16" stroke="#e5b2ff" stroke-width="6" fill="none" stroke-linecap="round" stroke-linejoin="round"/></g>'
    b += spark(1420, 300, 22) + spark(1560, 420, 14) + spark(940, 250, 16) + spark(1330, 560, 12)
    b += '<rect width="1920" height="1080" fill="url(#vigA)"/>'
    lines = [('CAN YOU', 150, 'w'), ('<span class="g">COOK</span> IT?', 214, 'w')]
    return page('#2a221a', svg(defs, b), lines, outline='#120c06')


# ======================= B: sponge brain + bending keys =======================
BRAIN = ('M-400 20 C-430 -150 -300 -290 -120 -300 C0 -330 180 -320 290 -230 C390 -160 430 -40 380 60 '
         'C350 120 290 140 230 130 C200 170 120 180 60 160 C0 190 -120 190 -200 160 C-320 150 -390 100 -400 20 Z')


def key(x, y, ang, bend, col, hi, s=1.0, glow='#ffd36b'):
    g = f'<g transform="translate({x} {y}) rotate({ang}) scale({s})" stroke-linecap="round" stroke-linejoin="round">'
    a = math.radians(bend); L1, L2 = 70, 90
    kx, ky = 38 + L1, 0; ex, ey = kx + L2 * math.cos(a), L2 * math.sin(a)
    nx, ny = -math.sin(a), math.cos(a)   # teeth hang on the side
    teeth = ''.join(f'M{kx + (ex - kx) * t:.1f} {ky + (ey - ky) * t:.1f} l{nx * 26:.1f} {ny * 26:.1f}' for t in (.55, .8))
    shaft = f'M30 0 L{kx} {ky} L{ex:.1f} {ey:.1f}'
    g += f'<path d="{shaft} {teeth}" stroke="{glow}" stroke-width="40" fill="none" opacity=".35" filter="url(#b12)"/>'
    g += f'<circle cx="0" cy="0" r="36" fill="none" stroke="{glow}" stroke-width="30" opacity=".35" filter="url(#b12)"/>'
    for w, c in ((24, '#2a1606'), (15, col)):
        g += f'<circle cx="0" cy="0" r="32" fill="none" stroke="{c}" stroke-width="{w + 6}"/>'
        g += f'<path d="{shaft} {teeth}" stroke="{c}" stroke-width="{w}" fill="none"/>'
    g += f'<path d="M-22 -16 A28 28 0 0 1 10 -28" stroke="{hi}" stroke-width="6" fill="none"/><path d="M40 -4 L{kx - 4} -4" stroke="{hi}" stroke-width="4" fill="none"/>'
    return g + '</g>'


def thumb_B():
    random.seed(7)
    defs = FILTERS
    defs += lin('bgB', [(0, '#1b0f2e'), (.6, '#120a22'), (1, '#07050d')])
    defs += rad('glowB', 1360, 500, 620, [(0, '#b04cff', .55), (.5, '#7a2cc9', .18), (1, '#7a2cc9', 0)])
    defs += rad('spotB', 1500, -100, 1100, [(0, '#bff6ff', .35), (.5, '#7fe0ff', .08), (1, '#7fe0ff', 0)])
    defs += ('<radialGradient id="brainG" cx="1250" cy="380" r="560" gradientUnits="userSpaceOnUse"><stop offset="0" stop-color="#f7c2f1"/>'
             '<stop offset=".45" stop-color="#c672d6"/><stop offset=".85" stop-color="#76318f"/><stop offset="1" stop-color="#43175a"/></radialGradient>')
    defs += f'<clipPath id="brainClip"><path transform="translate(1400 485)" d="{BRAIN}"/></clipPath>'
    defs += rad('vigB', 960, 540, 1150, [(0, '#000', 0), (.65, '#000', 0), (1, '#000', .6)])
    b = '<rect width="1920" height="1080" fill="url(#bgB)"/>'
    # faint lab grid + shelves in the back
    b += ''.join(f'<path d="M{x} 0 L{x} 1080" stroke="#2a1d44" stroke-width="2" opacity=".5"/>' for x in range(0, 1920, 120))
    b += ''.join(f'<path d="M0 {y} L1920 {y}" stroke="#2a1d44" stroke-width="2" opacity=".5"/>' for y in range(0, 1080, 120))
    b += '<rect width="1920" height="1080" fill="url(#spotB)"/>'
    b += '<rect width="1920" height="1080" fill="url(#glowB)"/>'
    # floor / bench
    b += '<path d="M0 780 L1920 740 L1920 1080 L0 1080 Z" fill="#0d0818"/>'
    b += '<path d="M0 780 L1920 740" stroke="#5a3d86" stroke-width="3" opacity=".7"/>'
    # glass dish under the brain
    b += '<ellipse cx="1400" cy="785" rx="520" ry="70" fill="#000" opacity=".5" filter="url(#b24)"/>'
    b += '<ellipse cx="1400" cy="745" rx="480" ry="62" fill="#9fe8ff" fill-opacity=".10" stroke="#9fe8ff" stroke-width="4" stroke-opacity=".7"/>'
    b += '<path d="M920 745 L920 775 A480 62 0 0 0 1880 775 L1880 745" fill="#9fe8ff" fill-opacity=".08" stroke="#9fe8ff" stroke-width="3" stroke-opacity=".5"/>'
    b += '<path d="M980 767 A460 50 0 0 0 1340 805" stroke="#fff" stroke-width="5" fill="none" opacity=".55"/>'
    T = 'translate(1400 485)'
    # cerebellum + brainstem (behind)
    b += f'<g transform="{T}"><path d="M150 150 C150 230 120 260 110 300 L190 300 C190 260 210 220 220 150 Z" fill="#8c4aa3" stroke="#2a0d3a" stroke-width="5"/>'
    b += '<ellipse cx="250" cy="150" rx="125" ry="72" fill="#9b55b2" stroke="#2a0d3a" stroke-width="5"/>'
    b += ''.join(f'<path d="M{150 + k * 6} {110 + k * 16} Q250 {96 + k * 18} {360 - k * 8} {120 + k * 14}" stroke="#4a1b62" stroke-width="4" fill="none"/>' for k in range(6))
    b += '</g>'
    b += f'<path transform="{T}" d="{BRAIN}" fill="#c46cff" opacity=".6" filter="url(#b24)"/>'
    b += f'<path transform="{T}" d="{BRAIN}" fill="url(#brainG)" stroke="#2a0d3a" stroke-width="7"/>'
    # gyri: packed rounded folds (dark outline under a gradient fill, later folds overlap earlier ones)
    gy = '<g clip-path="url(#brainClip)">'
    gy += f'<path transform="{T}" d="{BRAIN}" fill="#5a2272"/>'
    seeds = [(x + random.uniform(-25, 25), y + random.uniform(-25, 25)) for y in range(-320, 200, 62) for x in range(-430, 420, 70)]
    random.shuffle(seeds)
    for sx_, sy_ in seeds:
        h = random.uniform(0, 6.28); pts = [(sx_, sy_)]
        for k in range(4):
            h += random.uniform(-.9, .9); pts.append((pts[-1][0] + 40 * math.cos(h), pts[-1][1] + 40 * math.sin(h)))
        d = f'M{pts[0][0] + 1400:.0f} {pts[0][1] + 485:.0f} ' + ' '.join(f'Q{pts[i][0] + 1400:.0f} {pts[i][1] + 485:.0f} {(pts[i][0] + pts[i + 1][0]) / 2 + 1400:.0f} {(pts[i][1] + pts[i + 1][1]) / 2 + 485:.0f}' for i in range(1, 4))
        gy += f'<path d="{d}" stroke="#3a0f50" stroke-width="58" fill="none" stroke-linecap="round" stroke-linejoin="round"/>'
        gy += f'<path d="{d}" stroke="url(#brainG)" stroke-width="44" fill="none" stroke-linecap="round" stroke-linejoin="round"/>'
        gy += f'<path d="{d}" transform="translate(-5 -7)" stroke="#ffe0fb" stroke-width="7" fill="none" opacity=".55" stroke-linecap="round"/>'
    gy += '<path d="M1000 555 C1140 495 1290 495 1460 455 C1540 435 1600 445 1660 405" stroke="#3a0f50" stroke-width="16" fill="none" stroke-linecap="round"/>'
    gy += '<path d="M1330 195 C1340 275 1310 345 1340 435" stroke="#3a0f50" stroke-width="12" fill="none" stroke-linecap="round"/>'
    # sponge holes: dark pit with a lit lower inner wall
    holes = []
    while len(holes) < 34:
        x = random.uniform(-370, 360); y = random.uniform(-270, 150)
        if (x / 390) ** 2 + ((y + 70) / 240) ** 2 > .85:
            continue
        r = random.choice([12, 16, 20, 24, 30, 36, 44])
        if any(math.hypot(x - hx, y - hy) < r + hr + 6 for hx, hy, hr in holes):
            continue
        holes.append((x, y, r))
    for x, y, r in holes:
        X, Y = x + 1400, y + 485
        gy += f'<ellipse cx="{X:.0f}" cy="{Y:.0f}" rx="{r * 1.1 + 5:.0f}" ry="{r * .85 + 5:.0f}" fill="#2a0a3a"/>'
        gy += f'<ellipse cx="{X:.0f}" cy="{Y + r * .2:.0f}" rx="{r * .95:.0f}" ry="{r * .62:.0f}" fill="#e9a6ec"/>'
        gy += f'<ellipse cx="{X:.0f}" cy="{Y - r * .12:.0f}" rx="{r * .98:.0f}" ry="{r * .66:.0f}" fill="#1a0626"/>'
    gy += '<path d="M980 310 C1140 130 1540 110 1740 270" stroke="#fff" stroke-width="40" fill="none" opacity=".18" filter="url(#b24)"/>'
    gy += '</g>'
    b += gy
    # neon rim light
    b += f'<path transform="{T}" d="{BRAIN}" fill="none" stroke="#7ff3ff" stroke-width="14" opacity=".5" filter="url(#b12)"/>'
    b += f'<path transform="{T}" d="{BRAIN}" fill="none" stroke="#b9fbff" stroke-width="3.5" opacity=".9"/>'
    # chain of keys: straight gold keys bend each other, the last one red and twisted, entering the brain
    ks = [(560, 900, -8, 0, '#f2c14e', '#fff2b0', '#ffd36b'),
          (760, 880, -14, 18, '#eaa548', '#ffe0a0', '#ffb35b'),
          (940, 830, -24, 42, '#e0783e', '#ffc39a', '#ff8a4b'),
          (1110, 755, -40, 70, '#d8433b', '#ff9d94', '#ff4b4b')]
    for x, y, a, bnd, c, h, gl in ks:
        b += key(x, y, a, bnd, c, h, 1.0, gl)
    # tiny shock marks between keys
    for x, y in ((700, 870), (880, 830), (1030, 760)):
        b += f'<path d="M{x} {y - 30} l8 14 l-10 4 l10 16" stroke="#fff3b0" stroke-width="4" fill="none" stroke-linecap="round" opacity=".9"/>'
    # frog in a lab coat with goggles and magnifying glass, bottom-left
    coat = ('<path d="M-34 -2 q-4 -26 4 -34 l24 22 l10 -12 l12 12 l20 -20 q12 14 6 34 q-36 8 -76 -2z" fill="#f4f6f8" stroke-width="3.4"/>'
            '<path d="M-6 -18 l0 18 M18 -18 l0 18" stroke="#b8c0c8" stroke-width="2.4"/><rect x="22" y="-16" width="12" height="9" rx="2" fill="#7ad0ff" stroke-width="2"/>')
    goggles = ('<path d="M-30 -86 q36 -16 72 0" fill="none" stroke-width="7"/><path d="M-30 -86 q36 -16 72 0" fill="none" stroke="#e0a43c" stroke-width="3"/>'
               '<circle cx="-10" cy="-90" r="9" fill="#9fe8ff" stroke-width="3"/><circle cx="22" cy="-90" r="9" fill="#9fe8ff" stroke-width="3"/>')
    mag = ('<g transform="translate(58 -46) rotate(-30)"><rect x="-4" y="0" width="9" height="34" rx="4" fill="#6b3b1e" stroke-width="3"/>'
           '<circle cx="0" cy="-16" r="18" fill="#cfefff" fill-opacity=".35" stroke="#c9a05a" stroke-width="5"/><path d="M-10 -24 a12 12 0 0 1 10 -6" stroke="#fff" stroke-width="3" fill="none"/></g>')
    b += '<ellipse cx="320" cy="1030" rx="160" ry="22" fill="#000" opacity=".5" filter="url(#b6)"/>'
    b += frog(320, 1025, 3.5, mouth='o', arms=('q-14 6 -16 22', 'q16 -4 24 -26'), look=(5, -1), torso=coat, head=goggles, front=mag)
    b += spark(1780, 220, 22) + spark(1660, 120, 14) + spark(1050, 210, 16) + spark(1810, 600, 12) + spark(620, 760, 12)
    b += ''.join(f'<circle cx="{random.randint(950, 1880)}" cy="{random.randint(80, 700)}" r="{random.choice([2, 3, 4])}" fill="#e6c4ff" opacity="{random.uniform(.3, .8):.2f}"/>' for _ in range(40))
    b += '<rect width="1920" height="1080" fill="url(#vigB)"/>'
    lines = [('THE', 130, 'w'), ('LAUGHING', 196, 'y'), ('DEATH', 196, 'w')]
    return page('#120a22', svg(defs, b), lines, outline='#0b0414')


# ======================= C: calorie scale (mammoth vs empty plate) =======================
def mammoth(x, y, s):
    random.seed(21)
    g = f'<g transform="translate({x} {y}) scale({s})" stroke="#2a1508" stroke-linejoin="round" stroke-linecap="round">'

    def leg(lx, w, top, col):
        o = f'<path d="M{lx} {top} C{lx - 16} -100 {lx - 12} -30 {lx - 8} -4 Q{lx + w / 2} 12 {lx + w + 8} -4 C{lx + w + 12} -30 {lx + w + 16} -100 {lx + w} {top} Z" fill="{col}" stroke-width="5"/>'
        o += ''.join(f'<path d="M{lx + random.uniform(0, w):.0f} {random.uniform(-90, -40):.0f} q-3 12 -1 24" stroke="#3a1d0b" stroke-width="3" fill="none" opacity=".7"/>' for _ in range(7))
        o += f'<path d="M{lx - 4} -100 C{lx - 8} -60 {lx - 6} -30 {lx - 4} -12" stroke="#ffb35a" stroke-width="4" fill="none" opacity=".6"/>'
        o += ''.join(f'<path d="M{lx + 8 + k * (w - 16) / 3:.0f} -1 q4 -10 8 0" fill="#e8d7b4" stroke-width="3"/>' for k in range(4))
        return o
    g += leg(-170, 74, -170, '#4e2a13') + leg(110, 74, -170, '#4e2a13')   # far legs
    tail = '<path d="M-262 -200 q-34 40 -26 92" stroke-width="8" fill="none"/><path d="M-290 -116 l-10 26 l16 -8 l8 18 l4 -28z" fill="#4a2711" stroke-width="3"/>'
    g += leg(-226, 84, -160, '#7a4522') + leg(56, 84, -160, '#7a4522')   # near legs (tops hidden under the body)
    g += tail
    body = 'M-262 -120 C-292 -250 -200 -320 -70 -336 C40 -350 120 -372 180 -344 C230 -318 236 -220 210 -150 C150 -96 -100 -90 -262 -120 Z'
    g += f'<path d="{body}" fill="url(#furG)" stroke-width="6"/>'
    # shaggy fringe under the belly
    fr = 'M-258 -130 ' + ' '.join(f'L{-258 + i * 23} {-84 + (22 if i % 2 else 0) + random.randint(-5, 6)}' for i in range(1, 21)) + ' L212 -150 Z'
    g += f'<path d="{fr}" fill="#6e3d1d" stroke-width="4"/>'
    head = 'M130 -330 C126 -450 270 -466 292 -350 C302 -296 292 -244 272 -212 C240 -186 186 -194 156 -222 Z'
    g += f'<path d="{head}" fill="url(#furG)" stroke-width="6"/>'
    # fur strands on body + head
    for _ in range(240):
        fx = random.uniform(-250, 200); fy = random.uniform(-330, -110)
        if ((fx + 30) / 230) ** 2 + ((fy + 225) / 115) ** 2 > 1:
            continue
        c = random.choice(['#4a2711', '#b8743c', '#5c3317', '#d4904c', '#8c5228'])
        g += f'<path d="M{fx:.0f} {fy:.0f} q{random.uniform(-6, 6):.0f} 14 {random.uniform(-10, 2):.0f} {random.uniform(18, 34):.0f}" stroke="{c}" stroke-width="3.4" fill="none" opacity=".85"/>'
    for _ in range(80):
        fx = random.uniform(140, 290); fy = random.uniform(-440, -210)
        if ((fx - 212) / 70) ** 2 + ((fy + 330) / 100) ** 2 > 1:
            continue
        g += f'<path d="M{fx:.0f} {fy:.0f} q-4 10 -2 20" stroke="{random.choice(["#4a2711", "#c8844a", "#8c5228"])}" stroke-width="3" fill="none" opacity=".85"/>'
    # warm rim light (fire on the left) + top light
    g += '<path d="M-260 -134 C-288 -250 -200 -316 -70 -332" stroke="#ffb35a" stroke-width="10" fill="none" opacity=".9"/>'
    g += '<path d="M-60 -334 C40 -348 110 -368 170 -348" stroke="#ffd08a" stroke-width="6" fill="none" opacity=".6"/>'
    g += '<path d="M136 -340 C140 -440 260 -456 284 -360" stroke="#ffcf86" stroke-width="7" fill="none" opacity=".75"/>'
    # ear, eye (curious look)
    g += '<path d="M156 -300 q-34 8 -28 52 q26 8 42 -16z" fill="#5a3218" stroke-width="4"/>'
    g += '<ellipse cx="246" cy="-306" rx="9" ry="10" fill="#1a0c04" stroke="none"/><circle cx="249" cy="-309" r="3" fill="#fff" stroke="none"/>'
    g += '<path d="M230 -324 q16 -9 30 0" stroke-width="3.5" fill="none"/>'
    # trunk, curled at the tip
    tr = 'M270 -226 C306 -160 304 -70 280 -26 C268 -6 242 -10 240 -30 C238 -46 256 -46 258 -34 C272 -76 270 -140 238 -200 Z'
    g += f'<path d="{tr}" fill="#7a4522" stroke-width="5"/>'
    g += ''.join(f'<path d="M{252 + k * 3:.0f} {-188 + k * 22} q14 4 28 -2" stroke="#4a2711" stroke-width="3" fill="none"/>' for k in range(6))
    # tusks sweeping forward and up
    g += '<path d="M238 -210 C270 -110 360 -90 410 -170 C418 -186 404 -194 396 -180 C356 -126 286 -134 254 -218 Z" fill="#cdbb95" stroke-width="4.5"/>'
    g += '<path d="M256 -200 C290 -84 400 -66 452 -170 C460 -190 444 -198 436 -180 C392 -106 310 -112 274 -208 Z" fill="#f6ead0" stroke-width="5"/>'
    g += '<path d="M282 -160 C320 -100 390 -98 440 -168" stroke="#fffaf0" stroke-width="5" fill="none" opacity=".9"/>'
    return g + '</g>'


def thumb_C():
    random.seed(5)
    defs = FILTERS
    defs += lin('bgC', [(0, '#2d1a10'), (.6, '#1f120a'), (1, '#0b0604')])
    defs += rad('fireC', 120, 1060, 1100, [(0, '#ff9a3c', .65), (.35, '#e0611e', .25), (1, '#e0611e', 0)])
    defs += rad('glowPlate', 1700, 520, 360, [(0, '#fff3c8', .55), (.5, '#ffd98a', .15), (1, '#ffd98a', 0)])
    defs += lin('furG', [(0, '#a5642f'), (.55, '#7a4522'), (1, '#4a2711')])
    defs += lin('brass', [(0, '#fff0b8'), (.4, '#e2b25a'), (1, '#8a5e1e')], x2=1, y2=0)
    defs += lin('brassV', [(0, '#ffe7a0'), (1, '#9a6a24')])
    defs += rad('vigC', 960, 540, 1150, [(0, '#000', 0), (.65, '#000', 0), (1, '#000', .6)])
    b = '<rect width="1920" height="1080" fill="url(#bgC)"/>'
    # cave rock texture
    for _ in range(70):
        b += f'<ellipse cx="{random.randint(0, 1920)}" cy="{random.randint(0, 900)}" rx="{random.randint(60, 220)}" ry="{random.randint(30, 110)}" fill="{random.choice(["#3a2416", "#26170d", "#442b1a"])}" opacity="{random.uniform(.3, .7):.2f}" filter="url(#b12)"/>'
    # ochre cave paintings on the back wall (deer + small mammoth outline, hunters' world)
    paint = ('<g stroke="#c0582a" stroke-width="7" fill="none" stroke-linecap="round" opacity=".55">'
             '<path d="M1380 170 q60 -40 130 -10 q30 20 20 60 l-10 40 M1400 190 l-6 60 M1450 200 l4 56 M1500 200 l6 54 M1530 210 q30 -10 30 30 l-6 30"/>'
             '<path d="M1540 160 q10 -40 -10 -60 M1540 130 l24 -20"/></g>'
             '<g stroke="#a8462a" stroke-width="6" fill="none" stroke-linecap="round" opacity=".45">'
             '<path d="M1640 330 q20 -40 70 -36 q40 4 50 40 l-4 50 M1660 336 l-4 50 M1700 340 l0 50 M1744 340 l4 46 M1760 330 q24 20 10 60"/>'
             '<path d="M1640 330 q-16 10 -12 30"/></g>'
             + ''.join(f'<circle cx="{1200 + k * 34}" cy="{110 + (k % 2) * 16}" r="6" fill="#c0582a" opacity=".45"/>' for k in range(5)))
    b += paint
    b += '<rect width="1920" height="1080" fill="url(#fireC)"/>'
    # floor
    b += '<path d="M0 960 C400 940 900 960 1300 950 C1600 944 1800 950 1920 946 L1920 1080 L0 1080 Z" fill="#140b06"/>'
    b += ''.join(f'<ellipse cx="{random.randint(0, 1920)}" cy="{random.randint(965, 1070)}" rx="{random.randint(20, 70)}" ry="{random.randint(4, 10)}" fill="#2a170c" opacity=".7"/>' for _ in range(24))
    # scale geometry
    PX, PY = 1270, 410; LX, LY = 830, 500; RX_, RY_ = 1710, 320
    LPY, RPY = 950, 620
    b += '<rect width="1920" height="1080" fill="url(#glowPlate)"/>'
    # stand
    b += f'<ellipse cx="{PX}" cy="1010" rx="170" ry="26" fill="#000" opacity=".5" filter="url(#b6)"/>'
    b += f'<path d="M{PX - 150} 1004 q150 -40 300 0 l-20 -24 q-130 -30 -260 0z" fill="url(#brassV)" stroke="#4a300c" stroke-width="5"/>'
    b += f'<path d="M{PX - 70} 980 q70 -30 140 0 l-30 -40 q-40 -10 -80 0z" fill="url(#brassV)" stroke="#4a300c" stroke-width="5"/>'
    b += f'<rect x="{PX - 18}" y="{PY}" width="36" height="540" rx="10" fill="url(#brass)" stroke="#4a300c" stroke-width="5"/>'
    # beam (tilted: mammoth side down)
    b += f'<path d="M{LX} {LY} L{RX_} {RY_}" stroke="#4a300c" stroke-width="30" stroke-linecap="round"/>'
    b += f'<path d="M{LX} {LY} L{RX_} {RY_}" stroke="url(#brassV)" stroke-width="20" stroke-linecap="round"/>'
    b += f'<path d="M{LX + 10} {LY - 8} L{RX_ - 10} {RY_ - 8}" stroke="#fff3c2" stroke-width="4" stroke-linecap="round" opacity=".8"/>'
    b += f'<circle cx="{PX}" cy="{PY}" r="34" fill="url(#brass)" stroke="#4a300c" stroke-width="5"/><circle cx="{PX}" cy="{PY}" r="10" fill="#4a300c"/>'
    b += f'<path d="M{PX} {PY - 34} l0 -46" stroke="#4a300c" stroke-width="14" stroke-linecap="round"/><path d="M{PX} {PY - 34} l0 -46" stroke="#f2d27a" stroke-width="7" stroke-linecap="round"/>'

    def chains(tx, ty, cx, py, rx):
        out = ''
        for ex in (cx - rx * .96, cx + rx * .96):
            out += f'<path d="M{tx} {ty} L{ex:.0f} {py - 6}" stroke="#4a300c" stroke-width="7"/><path d="M{tx} {ty} L{ex:.0f} {py - 6}" stroke="#e8c070" stroke-width="3" stroke-dasharray="10 6"/>'
        return out

    def pan(cx, py, rx):
        return (f'<path d="M{cx - rx} {py} Q{cx} {py + rx * .42} {cx + rx} {py} Z" fill="url(#brassV)" stroke="#4a300c" stroke-width="5"/>'
                f'<ellipse cx="{cx}" cy="{py}" rx="{rx}" ry="{rx * .12:.0f}" fill="#d9a54e" stroke="#4a300c" stroke-width="5"/>'
                f'<path d="M{cx - rx * .8} {py + rx * .07} Q{cx - rx * .3} {py + rx * .19} {cx + rx * .2} {py + rx * .17}" stroke="#fff0b8" stroke-width="5" fill="none" opacity=".7"/>')
    # left pan + mammoth (heavy, down)
    b += chains(LX, LY, LX, LPY, 300)
    b += pan(LX, LPY, 300)
    b += f'<ellipse cx="{LX}" cy="{LPY}" rx="240" ry="20" fill="#000" opacity=".35" filter="url(#b6)"/>'
    b += f'<ellipse cx="{LX - 60}" cy="{LPY - 200}" rx="330" ry="220" fill="#ff8a3c" opacity=".18" filter="url(#b50)"/>'
    b += mammoth(LX - 80, LPY + 2, 1.0)
    # right pan + empty plate + frog (light, up)
    b += chains(RX_, RY_, RX_, RPY, 175)
    b += pan(RX_, RPY, 175)
    PLX = 1775
    b += f'<ellipse cx="{PLX}" cy="{RPY - 6}" rx="96" ry="22" fill="#fbfaf4" stroke="#6b5a40" stroke-width="4"/><ellipse cx="{PLX}" cy="{RPY - 8}" rx="58" ry="12" fill="#ece6d6"/>'
    b += f'<path d="M{PLX - 30} {RPY - 14} q30 -8 60 0" stroke="#fff" stroke-width="3" fill="none"/>'
    b += f'<path d="M{PLX + 2} {RPY - 12} q4 -10 10 -6 q-2 6 -10 6" fill="#7fbf5a" stroke="#2f4a1c" stroke-width="2"/>'   # a single parsley leaf: that's all
    napkin = '<path d="M-14 -30 l40 0 l-20 30z" fill="#f4f1e6" stroke-width="3"/><path d="M-4 -26 l20 0" stroke="#d24b4b" stroke-width="3"/>'
    cutlery = ('<g transform="translate(-48 -34) rotate(-14)"><rect x="-3" y="-4" width="6" height="40" rx="3" fill="#cfd6dc" stroke-width="2.5"/><path d="M-7 -4 l0 -16 M0 -4 l0 -18 M7 -4 l0 -16 M-7 -6 l14 0" stroke-width="3" fill="none"/></g>'
               '<g transform="translate(60 -34) rotate(14)"><rect x="-3" y="-4" width="6" height="40" rx="3" fill="#cfd6dc" stroke-width="2.5"/><path d="M-4 -4 q-2 -22 6 -26 l0 26z" fill="#e8edf0" stroke-width="2.5"/></g>')
    b += frog(1630, RPY - 4, 2.5, mouth='o', arms=('q-16 0 -22 -22', 'q16 0 22 -22'), look=(-5, -1), torso=napkin, front=cutlery)
    # embers
    for _ in range(26):
        ex = random.randint(40, 1300); ey = random.randint(520, 1000)
        b += f'<circle cx="{ex}" cy="{ey}" r="{random.choice([2, 3, 4])}" fill="#ffc16b" opacity="{random.uniform(.4, .95):.2f}"/>'
    b += spark(1210, 230, 20) + spark(1500, 470, 14) + spark(1840, 420, 16) + spark(1150, 640, 12)
    b += '<rect width="1920" height="1080" fill="url(#vigC)"/>'
    lines = [('HALF A DAY', 150, 'w'), ('VS', 104, 'w'), ('2 MONTHS', 196, 'y')]
    return page('#1f120a', svg(defs, b), lines, outline='#120804')


for n, fn in (('A', thumb_A), ('B', thumb_B), ('C', thumb_C)):
    open(os.path.join(HERE, f'{n}.html'), 'w').write(fn())
print('ok')
