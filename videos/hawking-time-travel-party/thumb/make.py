# Thumbnails A-C for hawking-time-travel-party (guideline 16-6 / 16-8, brief tools/briefs/thumb_art.md).
# Run: python3 videos/hawking-time-travel-party/thumb/make.py   then   SLUG=hawking-time-travel-party python3 tools/build/thumb_shot.py
# Title: "Hawking's Party for Time Travelers: Nobody Came" -> texts avoid the title words.
# A  JUNE 28, / 2009 / AT NOON  (date)  homage: Harold Lloyd "Safety Last!" (1923, public domain) -> the frog in a straw boater
#    hangs from the minute hand of a huge glowing tower clock at noon above a night city (Cambridge spires), boater falling.
#    Script: "At noon, Universal Time, on June twenty-eighth, 2009, a reception was set up inside Gonville and Caius College".
# B  INVITES SENT / AFTERWARD  (declarative)  intuitive: the empty reception: long table, champagne on ice, glasses, balloons,
#    bunting, empty chairs; at the end a door glowing with starlight and a clock above it at 12; party-hat frog waits.
#    Script: "champagne on ice, balloons, and a banner"; "Hawking had not sent out a single invitation before the party ...
#    afterward, with the date, the time, and the map coordinates of the room."
# C  NATURE / BLOWS / IT UP?  (question, hedged)  intuitive: a wormhole (funnel diagram) whose throat blows apart in rings of
#    feedback; astronaut frog holds a microphone, a loudspeaker floats opposite.
#    Script: "Think of a microphone held too close to a loudspeaker ... a similar feedback loop in spacetime ... wreck the
#    wormhole. In that picture, nature blows up the bridge before anyone can cross it."
# No real person is drawn (no Hawking figure, no wheelchair).
import os, sys, math, random
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', '..', 'tools'))
from thumb_lib import page, svg, lin, rad, spark

INK = '#1d2b1c'; GREEN = '#6aa55a'; DARKG = '#4d8a4a'; BELLY = '#9cc98a'
FILTERS = ''.join(f'<filter id="b{n}" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="{n}"/></filter>' for n in (2, 4, 8, 14, 26, 50, 90))


def P(pts):
    return ' '.join(f'{a:.1f},{b:.1f}' for a, b in pts)


def limb(d, w=7.5, wi=3.4, col=GREEN):
    return f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="{w}"/><path d="{d}" fill="none" stroke="{col}" stroke-width="{wi}"/>'


def end_of(d):
    n = [float(v) for v in d.replace('M', ' ').replace('q', ' ').split()]
    return n[0] + n[-2], n[1] + n[-1]


def frog(x, y, s, rot=0, flip=False, look=(0, 0), mouth='O', armL=None, armR=None, brows=True, back='', front='', mid='', top='', sleeve=GREEN, hands=''):
    sx = -s if flip else s
    g = [f'<g transform="translate({x} {y}) rotate({rot}) scale({sx} {s})" stroke="{INK}" stroke-linejoin="round" stroke-linecap="round">', back]
    for fx, fy in ((-22, 4), (22, 4)):
        g.append(f'<ellipse cx="{fx}" cy="{fy}" rx="16" ry="9" fill="{DARKG}" stroke-width="3.2"/>')
    g.append(f'<path d="M-34 0 q-6 -64 34 -70 q40 -2 42 62 q0 10 -6 12 q-36 6 -70 -4z" fill="{GREEN}" stroke-width="4"/>')
    g.append(f'<ellipse cx="2" cy="-12" rx="22" ry="20" fill="{BELLY}" stroke="none" opacity=".7"/>')
    g.append('<path d="M-24 -50 q6 -14 18 -16" fill="none" stroke="#b6dea0" stroke-width="3" opacity=".8"/>')
    g.append(mid)
    lx, ly = look
    _d = math.hypot(1 + lx, ly)
    if _d > 6.9: _k = 6.9 / _d; lx, ly = (1 + lx) * _k - 1, ly * _k
    for ex in (-10, 22):
        g.append(f'<circle cx="{ex}" cy="-66" r="13.5" fill="#f4f5ea" stroke-width="3.2"/>')
        g.append(f'<circle cx="{ex + 1 + lx:.2f}" cy="{-66 + ly:.2f}" r="4.4" fill="{INK}" stroke="none"/>')
        g.append(f'<circle cx="{ex + 2.4 + lx:.2f}" cy="{-67.6 + ly:.2f}" r="1.5" fill="#fff" stroke="none"/>')
    if brows:
        g.append('<path d="M-22 -88 q12 -9 24 -1 M10 -89 q12 -8 24 1" fill="none" stroke-width="3.4"/>')
    if mouth == 'O':
        g.append('<ellipse cx="6" cy="-38" rx="10" ry="12" fill="#7a2f33" stroke-width="3"/><ellipse cx="6" cy="-31" rx="6" ry="4" fill="#e07b7b" stroke="none"/>')
    else:
        g.append('<ellipse cx="6" cy="-41" rx="6" ry="7.5" fill="#7a2f33" stroke-width="3"/>')
    g.append('<ellipse cx="-18" cy="-48" rx="5" ry="3" fill="#e98a8a" stroke="none" opacity=".55"/><ellipse cx="30" cy="-48" rx="5" ry="3" fill="#e98a8a" stroke="none" opacity=".55"/>')
    g.append(top)
    g.append(hands)
    for a in (armL or 'M-34 -22 q-14 6 -16 22', armR or 'M38 -22 q14 6 16 22'):
        g.append(limb(a, col=sleeve)); ex_, ey_ = end_of(a)
        g.append(f'<circle cx="{ex_:.1f}" cy="{ey_:.1f}" r="5.6" fill="{GREEN}" stroke-width="3"/>')
    g.append(front); g.append('</g>')
    return ''.join(g)


def sparkles(lst, col='#fff6d6'):
    return ''.join(spark(x, y, s, col) for x, y, s in lst)


def hx(c):
    c = c.lstrip('#'); return tuple(int(c[i:i + 2], 16) for i in (0, 2, 4))


def mix(cols, t):
    t = max(0, min(1, t)) * (len(cols) - 1); i = min(int(t), len(cols) - 2); f = t - i
    a, b = hx(cols[i]), hx(cols[i + 1])
    return '#%02x%02x%02x' % tuple(round(a[k] + (b[k] - a[k]) * f) for k in range(3))


def lina(id, stops, x2=0, y2=1, x1=0, y1=0):
    return f'<linearGradient id="{id}" x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}">' + ''.join(f'<stop offset="{o}" stop-color="{c}" stop-opacity="{a}"/>' for o, c, a in stops) + '</linearGradient>'


def starfield(r, n, x0, y0, x1, y1, col='#eef4ff'):
    out = ''
    for _ in range(n):
        x, y = r.uniform(x0, x1), r.uniform(y0, y1); rr = r.choice([1.1, 1.6, 2.2, 2.8])
        out += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{rr}" fill="{col}" opacity="{r.uniform(.25, .9):.2f}"/>'
    return out


# ====================================================================== A  (Safety Last! homage: hanging from the clock at noon)
def thumb_A():
    r = random.Random(11)
    CX, CY, CR = 1190, 450, 290
    HZ = 640          # horizon of the city far below
    defs = FILTERS
    defs += lin('skyA', [(0, '#070722'), (.45, '#1a1650'), (.8, '#4a2f6e'), (1, '#c0705a')])
    defs += lin('groundA', [(0, '#2a1d3c'), (.25, '#120e26'), (1, '#05050f')])
    defs += rad('faceA', CX - 60, CY - 70, 360, [(0, '#fffdf2', 1), (.55, '#fbeec4', 1), (1, '#e7c983', 1)])
    defs += rad('haloA', CX, CY, 720, [(0, '#ffe7a0', .75), (.3, '#ffb85a', .35), (.7, '#ff7a4a', .08), (1, '#ff7a4a', 0)])
    defs += rad('vigA', 960, 540, 1150, [(0, '#000', 0), (.62, '#000', 0), (1, '#000', .65)])
    defs += lin('stoneA', [(0, '#5c4a62'), (.5, '#3d3048'), (1, '#1d1626')], x2=1, y2=0)
    defs += lin('goldA', [(0, '#fff0b0'), (.4, '#e2b34a'), (1, '#8a5a1a')], x2=1, y2=1)
    b = '<rect width="1920" height="1080" fill="url(#skyA)"/>'
    b += starfield(r, 160, 0, 0, 1920, HZ - 120)
    # soft nebula / time swirl behind the tower
    for k in range(9):
        rr = 380 + k * 70
        b += f'<ellipse cx="{CX}" cy="{CY}" rx="{rr}" ry="{rr * .82:.0f}" fill="none" stroke="{mix(["#ffe2a0", "#ff9a6a", "#9a6ae0"], k / 8)}" stroke-width="{10 - k * .8:.1f}" opacity="{.42 - k * .035:.2f}" stroke-dasharray="{120 + k * 40} {60 + k * 30}" transform="rotate({k * 23} {CX} {CY})" filter="url(#b4)"/>'
    b += f'<circle cx="{CX}" cy="{CY}" r="720" fill="url(#haloA)"/>'
    # ---- city far below: horizon glow, spires, streets of light converging ----
    b += f'<rect x="0" y="{HZ - 40}" width="1920" height="80" fill="#ffb07a" opacity=".35" filter="url(#b26)"/>'
    sil = f'M0 {HZ} '
    x = 0
    while x < 1920:
        w = r.randint(40, 110); h = r.randint(14, 46)
        if r.random() < .22:   # gothic spire / chapel pinnacles
            sil += f'L{x} {HZ - h} L{x + w * .2:.0f} {HZ - h} L{x + w * .25:.0f} {HZ - h - 50} L{x + w * .3:.0f} {HZ - h} L{x + w * .7:.0f} {HZ - h} L{x + w * .75:.0f} {HZ - h - 50} L{x + w * .8:.0f} {HZ - h} L{x + w} {HZ - h} '
        else:
            sil += f'L{x} {HZ - h} L{x + w} {HZ - h} '
        x += w
    sil += f'L1920 {HZ} Z'
    b += f'<path d="{sil}" fill="#1b1430"/>'
    b += f'<rect x="0" y="{HZ}" width="1920" height="{1080 - HZ}" fill="url(#groundA)"/>'
    VPx = CX
    for k in range(-14, 15):
        x1 = VPx + k * 260
        b += f'<line x1="{VPx + k * 14}" y1="{HZ}" x2="{x1}" y2="1080" stroke="#ffb35a" stroke-width="{1.2 + abs(k) * .12:.1f}" opacity=".35"/>'
        for j in range(1, 14):
            t = (j / 14) ** 1.7
            px, py = VPx + k * 14 + (x1 - VPx - k * 14) * t, HZ + (1080 - HZ) * t
            rr = .8 + 3.2 * t
            b += f'<circle cx="{px:.0f}" cy="{py:.0f}" r="{rr * 3:.1f}" fill="#ffb35a" opacity=".18" filter="url(#b4)"/><circle cx="{px:.0f}" cy="{py:.0f}" r="{rr:.1f}" fill="#ffe2a8" opacity=".85"/>'
    for j in range(1, 9):   # cross streets
        t = (j / 9) ** 1.7; y = HZ + (1080 - HZ) * t
        b += f'<line x1="0" y1="{y:.0f}" x2="1920" y2="{y:.0f}" stroke="#ff9a4a" stroke-width="{.8 + 2 * t:.1f}" opacity=".22"/>'
    # window lights in rows of blocks
    for _ in range(260):
        t = r.random() ** 1.6; y = HZ + 8 + (1080 - HZ) * t; x = r.uniform(0, 1920)
        b += f'<rect x="{x:.0f}" y="{y:.0f}" width="{2 + 6 * t:.1f}" height="{1.5 + 4 * t:.1f}" fill="{r.choice(["#ffd88a", "#ffefc0", "#9ad0ff"])}" opacity="{r.uniform(.3, .8):.2f}"/>'
    b += f'<rect x="0" y="{HZ}" width="1920" height="60" fill="#3a2a50" opacity=".45" filter="url(#b14)"/>'
    # ---- the tower (seen slightly from above: edges lean in toward the street) ----
    TL0, TR0, TL1, TR1 = 860, 1520, 935, 1445
    b += f'<path d="M{TL0} -10 L{TR0} -10 L{TR1} 1090 L{TL1} 1090Z" fill="url(#stoneA)"/>'
    for k in range(1, 32):   # stone courses
        y = k * 36; t = y / 1080
        xl, xr = TL0 + (TL1 - TL0) * t, TR0 + (TR1 - TR0) * t
        b += f'<line x1="{xl:.0f}" y1="{y}" x2="{xr:.0f}" y2="{y}" stroke="#1a1222" stroke-width="2" opacity=".55"/>'
        off = 0 if k % 2 else 40
        for xx in range(int(xl) + off, int(xr), 80):
            b += f'<line x1="{xx}" y1="{y}" x2="{xx}" y2="{y + 36}" stroke="#1a1222" stroke-width="1.6" opacity=".35"/>'
    # tower edge highlights (lit by the clock glow)
    b += f'<path d="M{TL0} -10 L{TL1} 1090" stroke="#ffcf8a" stroke-width="6" opacity=".55"/><path d="M{TR0} -10 L{TR1} 1090" stroke="#ffcf8a" stroke-width="6" opacity=".45"/>'
    # gothic windows below the clock (lit)
    for row, (y, h) in enumerate(((835, 120), (1000, 110))):
        for xx in (1010, 1135, 1245, 1370):
            t = y / 1080; w = 62 - row * 4
            b += f'<path d="M{xx - w / 2:.0f} {y + h} v{-h * .7:.0f} q{w / 2:.0f} {-h * .5:.0f} {w} 0 v{h * .7:.0f}z" fill="#ffc46a" stroke="#1a1222" stroke-width="6"/>'
            b += f'<path d="M{xx} {y + h} v{-h * .9:.0f} M{xx - w / 2:.0f} {y + h * .55:.0f} h{w}" stroke="#4a2a18" stroke-width="4"/>'
            b += f'<ellipse cx="{xx}" cy="{y + h * .6:.0f}" rx="{w}" ry="{h * .7:.0f}" fill="#ffb04a" opacity=".25" filter="url(#b14)"/>'
    # ledge (cornice) under the clock
    b += f'<path d="M{TL0 + 8} 780 L{TR0 - 8} 780 L{TR0 + 10} 812 L{TL0 - 10} 812Z" fill="#6a5670" stroke="#160f1e" stroke-width="4"/>'
    b += f'<path d="M{TL0 - 10} 812 L{TR0 + 10} 812 L{TR0} 830 L{TL0} 830Z" fill="#2a1f34"/>'
    b += f'<path d="M{TL0 + 8} 782 L{TR0 - 8} 782" stroke="#ffd59a" stroke-width="4" opacity=".7"/>'
    # ---- the clock ----
    b += f'<rect x="{CX - 330}" y="{CY - 330}" width="660" height="660" rx="18" fill="#4a3a56" stroke="#140d1c" stroke-width="6"/>'
    for cx_, cy_ in ((CX - 300, CY - 300), (CX + 300, CY - 300), (CX - 300, CY + 300), (CX + 300, CY + 300)):
        b += f'<circle cx="{cx_}" cy="{cy_}" r="18" fill="#e2b34a" stroke="#3a2410" stroke-width="4"/>'
    b += f'<circle cx="{CX}" cy="{CY}" r="{CR + 34}" fill="url(#goldA)" stroke="#2a1606" stroke-width="6"/>'
    b += f'<circle cx="{CX}" cy="{CY}" r="{CR + 12}" fill="#3a2410"/>'
    b += f'<circle cx="{CX}" cy="{CY}" r="{CR + 70}" fill="#ffd27a" opacity=".22" filter="url(#b26)"/>'
    b += f'<circle cx="{CX}" cy="{CY}" r="{CR}" fill="url(#faceA)"/>'
    b += f'<circle cx="{CX}" cy="{CY}" r="{CR - 70}" fill="none" stroke="#c8a060" stroke-width="3"/>'
    b += f'<circle cx="{CX}" cy="{CY}" r="{CR - 18}" fill="none" stroke="#7a5420" stroke-width="3"/>'
    for k in range(60):
        a = k * math.pi / 30
        r1, r2 = (CR - 18, CR - 40) if k % 5 == 0 else (CR - 18, CR - 28)
        b += f'<line x1="{CX + r1 * math.sin(a):.1f}" y1="{CY - r1 * math.cos(a):.1f}" x2="{CX + r2 * math.sin(a):.1f}" y2="{CY - r2 * math.cos(a):.1f}" stroke="#3a2410" stroke-width="{5 if k % 5 == 0 else 2.2}"/>'
    rom = ['XII', 'I', 'II', 'III', 'IIII', 'V', 'VI', 'VII', 'VIII', 'IX', 'X', 'XI']
    for k, t in enumerate(rom):
        a = k * math.pi / 6; rr = CR - 82
        x_, y_ = CX + rr * math.sin(a), CY - rr * math.cos(a)
        b += (f'<text x="{x_:.1f}" y="{y_:.1f}" font-family="Georgia, \'DejaVu Serif\', serif" font-size="54" font-weight="700" fill="#2a1a0a" '
              f'text-anchor="middle" dominant-baseline="central" transform="rotate({k * 30} {x_:.1f} {y_:.1f})">{t}</text>')
    # glass sheen
    b += f'<path d="M{CX - 230} {CY - 120} A250 250 0 0 1 {CX - 40} {CY - 250}" fill="none" stroke="#fff" stroke-width="22" opacity=".5" stroke-linecap="round"/>'
    # hour hand at XII
    b += f'<path d="M{CX - 12} {CY + 30} L{CX - 9} {CY - 120} L{CX - 30} {CY - 150} L{CX} {CY - 195} L{CX + 30} {CY - 150} L{CX + 9} {CY - 120} L{CX + 12} {CY + 30}Z" fill="#1a1008" stroke="#e2b34a" stroke-width="2"/>'
    # minute hand pulled down to the right by the frog, bending out past the rim
    ang = math.radians(61); ux, uy = math.sin(ang), -math.cos(ang); nx, ny = -uy, ux
    pts = []
    for d, w in ((-50, 13), (0, 11), (240, 9), (330, 8), (420, 6)):
        pts.append((CX + ux * d + nx * w, CY + uy * d + ny * w))
    tip = (CX + ux * 470, CY + uy * 470 + 6)
    pts2 = [(CX + ux * d - nx * w, CY + uy * d - ny * w) for d, w in ((420, 6), (330, 8), (240, 9), (0, 11), (-50, 13))]
    b += f'<polygon points="{P(pts + [tip] + pts2)}" fill="#1a1008" stroke="#e2b34a" stroke-width="2.5"/>'
    b += f'<circle cx="{CX}" cy="{CY}" r="22" fill="#e2b34a" stroke="#2a1606" stroke-width="4"/><circle cx="{CX}" cy="{CY}" r="8" fill="#2a1606"/>'
    # ---- frog hanging from the minute hand (straw boater falling) ----
    FS = 2.55
    gl = (-14, -110)  # left hand grip, local
    g1 = (CX + ux * 300, CY + uy * 300)
    FX, FY = g1[0] - FS * gl[0], g1[1] - FS * gl[1]
    legs = (limb('M-24 2 q-4 30 -16 56', w=8, wi=3.8) + limb('M24 2 q8 28 20 52', w=8, wi=3.8)
            + f'<path d="M-40 58 q-12 6 -18 16 q10 2 18 -4 q2 8 8 10 q2 -12 -8 -22z" fill="{DARKG}" stroke-width="3"/>'
            + f'<path d="M44 54 q10 8 12 18 q-10 0 -16 -6 q-4 8 -10 8 q0 -12 14 -20z" fill="{DARKG}" stroke-width="3"/>')
    bowtie = '<path d="M2 -14 l-14 -8 v16z M6 -14 l14 -8 v16z" fill="#c0392b" stroke-width="2.6"/><circle cx="4" cy="-14" r="4" fill="#8a1e1e" stroke-width="2"/>'
    b += frog(FX, FY, FS, look=(0, 6), mouth='O', back=legs, mid=bowtie,
              armL='M-34 -26 q-16 -48 20 -84', armR='M38 -26 q18 -56 -8 -106')
    # wind/motion lines + falling boater hat
    for x, y, L in ((FX - 150, FY - 40, 70), (FX + 150, FY - 10, 60), (FX + 170, FY + 60, 80)):
        b += f'<path d="M{x:.0f} {y:.0f} v{L}" stroke="#fff3d6" stroke-width="5" stroke-linecap="round" opacity=".5"/>'
    hx_, hy_ = FX + 150, FY + 190
    b += (f'<g transform="translate({hx_:.0f} {hy_:.0f}) rotate(28)" stroke="#2a1606" stroke-width="5" stroke-linejoin="round">'
          '<ellipse cx="0" cy="18" rx="92" ry="22" fill="#e8c56a"/>'
          '<path d="M-52 18 q-4 -52 8 -58 q44 -12 88 0 q12 6 8 58z" fill="#f2d27a"/>'
          '<path d="M-50 0 q50 10 100 0 v14 q-50 10 -100 0z" fill="#2a2a3a"/>'
          '<path d="M-36 -30 q30 -8 70 -2" fill="none" stroke="#fff6d0" stroke-width="5" opacity=".8"/></g>')
    b += sparkles([(1640, 160, 20), (720, 560, 14), (1720, 520, 16), (1010, 120, 14), (560, 700, 12)], '#fff1c8')
    b += '<rect width="1920" height="1080" fill="url(#vigA)"/>'
    lines = [('JUNE 28,', 130, 'w'), ('2009', 250, 'y'), ('AT NOON', 130, 'w')]
    return page('#070722', svg(defs, b), lines, outline='#0a0618', top=50)


# ====================================================================== B  (the empty reception)
def thumb_B():
    r = random.Random(5)
    VX, VY, F = 1230, 560, 900
    def pr(X, Y, Z): return (VX + F * X / Z, VY + F * Y / Z)
    FLOOR, CEIL, BZ, WL, WR = 1.6, -2.0, 6.5, -3.6, 3.4
    defs = FILTERS
    defs += lin('wallB', [(0, '#2a1a22'), (1, '#4a2e2a')])
    defs += lin('sideB', [(0, '#1c1016'), (1, '#3a2420')], x2=1, y2=0)
    defs += lin('sideB2', [(0, '#3a2420'), (1, '#160c12')], x2=1, y2=0)
    defs += lin('floorB', [(0, '#3a2418'), (1, '#140a08')])
    defs += lin('clothB', [(0, '#e9e2d6'), (1, '#fffaf0')])
    defs += rad('doorB', 0, 0, 1, [(0, '#ffffff', 1), (.3, '#c8ecff', 1), (.7, '#6a8cff', 1), (1, '#3a2a8a', 1)]).replace('gradientUnits="userSpaceOnUse"', '')
    defs += rad('glowB', 0, 0, 1, [(0, '#bfe6ff', .85), (.4, '#8ab8ff', .35), (1, '#8ab8ff', 0)]).replace('gradientUnits="userSpaceOnUse"', '')
    defs += lina('spillB', [(0, '#bfe6ff', .55), (1, '#bfe6ff', 0)])
    defs += rad('vigB', 960, 540, 1150, [(0, '#000', 0), (.6, '#000', 0), (1, '#000', .7)])
    defs += rad('warmB', 700, 300, 900, [(0, '#ffb86a', .22), (1, '#ffb86a', 0)])
    b = ''
    # room shell
    bl, br_, tl, tr = pr(WL, FLOOR, BZ), pr(WR, FLOOR, BZ), pr(WL, CEIL, BZ), pr(WR, CEIL, BZ)
    b += f'<rect width="1920" height="1080" fill="#120a0e"/>'
    b += f'<polygon points="{P([(0, 1080), (0, -10), tl, bl])}" fill="url(#sideB)"/>'
    b += f'<polygon points="{P([(1930, 1080), (1930, -10), tr, br_])}" fill="url(#sideB2)"/>'
    b += f'<polygon points="{P([(0, -10), (1930, -10), tr, tl])}" fill="#1a0f14"/>'
    b += f'<polygon points="{P([(0, 1090), (1930, 1090), br_, bl])}" fill="url(#floorB)"/>'
    b += f'<polygon points="{P([tl, tr, br_, bl])}" fill="url(#wallB)"/>'
    # floor boards
    for k in range(-14, 16):
        X = k * .45
        b += f'<line x1="{pr(X, FLOOR, BZ)[0]:.0f}" y1="{pr(X, FLOOR, BZ)[1]:.0f}" x2="{pr(X, FLOOR, 1.0)[0]:.0f}" y2="{pr(X, FLOOR, 1.0)[1]:.0f}" stroke="#0e0604" stroke-width="2" opacity=".5"/>'
    # wood panelling on walls (back wall + side walls)
    for k in range(1, 9):
        X = WL + k * (WR - WL) / 9
        a, c = pr(X, .4, BZ), pr(X, FLOOR, BZ)
        b += f'<line x1="{a[0]:.0f}" y1="{a[1]:.0f}" x2="{c[0]:.0f}" y2="{c[1]:.0f}" stroke="#1a0d0a" stroke-width="3" opacity=".6"/>'
    a, c = pr(WL, .4, BZ), pr(WR, .4, BZ)
    b += f'<line x1="{a[0]:.0f}" y1="{a[1]:.0f}" x2="{c[0]:.0f}" y2="{c[1]:.0f}" stroke="#7a4a2a" stroke-width="5"/>'
    for X in (WL, WR):
        for Z in (1.6, 2.4, 3.4, 4.6):
            a, c = pr(X, .4, Z), pr(X, FLOOR, Z)
            b += f'<line x1="{a[0]:.0f}" y1="{a[1]:.0f}" x2="{c[0]:.0f}" y2="{c[1]:.0f}" stroke="#120806" stroke-width="4" opacity=".6"/>'
        a, c = pr(X, .4, 1.0), pr(X, .4, BZ)
        b += f'<line x1="{a[0]:.0f}" y1="{a[1]:.0f}" x2="{c[0]:.0f}" y2="{c[1]:.0f}" stroke="#7a4a2a" stroke-width="6"/>'
    # tall dark windows on the left wall with stars
    for Z0, Z1 in ((1.9, 2.6), (3.3, 4.2)):
        q = [pr(WL, -1.4, Z0), pr(WL, -1.4, Z1), pr(WL, .1, Z1), pr(WL, .1, Z0)]
        b += f'<polygon points="{P(q)}" fill="#0a1030" stroke="#6a4a2a" stroke-width="6"/>'
    b += f'<rect width="1920" height="1080" fill="url(#warmB)"/>'
    # ---- the door at the end: open, starlight pouring in ----
    DX0, DX1, DT = -.75, .75, -.75
    d0, d1, d2, d3 = pr(DX0, DT, BZ), pr(DX1, DT, BZ), pr(DX1, FLOOR, BZ), pr(DX0, FLOOR, BZ)
    dcx, dcy = (d0[0] + d1[0]) / 2, (d0[1] + d2[1]) / 2
    b += f'<ellipse cx="{dcx:.0f}" cy="{dcy:.0f}" rx="420" ry="380" fill="url(#glowB)"/>'
    b += f'<polygon points="{P([(d0[0] - 18, d0[1] - 70), (d1[0] + 18, d1[1] - 70), (d2[0] + 18, d2[1]), (d3[0] - 18, d3[1])])}" fill="#5a3420" stroke="#1a0c06" stroke-width="5"/>'
    b += f'<path d="M{d0[0] - 18:.0f} {d0[1] - 70:.0f} Q{dcx:.0f} {d0[1] - 150:.0f} {d1[0] + 18:.0f} {d1[1] - 70:.0f}" fill="#5a3420" stroke="#1a0c06" stroke-width="5"/>'
    b += f'<polygon points="{P([d0, d1, d2, d3])}" fill="url(#doorB)"/>'
    # stars + swirl inside the doorway
    rr2 = random.Random(9)
    for _ in range(70):
        x, y = rr2.uniform(d0[0] + 6, d1[0] - 6), rr2.uniform(d0[1] + 6, d2[1] - 6)
        b += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{rr2.choice([1.2, 1.8, 2.6])}" fill="#fff" opacity="{rr2.uniform(.4, 1):.2f}"/>'
    for k in range(5):
        b += f'<ellipse cx="{dcx:.0f}" cy="{dcy + 20:.0f}" rx="{30 + k * 22}" ry="{50 + k * 34}" fill="none" stroke="#ffffff" stroke-width="{4 - k * .6:.1f}" opacity="{.6 - k * .1:.2f}" stroke-dasharray="{60 + k * 30} {40 + k * 20}" transform="rotate({k * 37} {dcx:.0f} {dcy + 20:.0f})"/>'
    b += f'<circle cx="{dcx:.0f}" cy="{dcy + 20:.0f}" r="34" fill="#fff" filter="url(#b14)"/>'
    # open door leaf swung inward-right
    leaf = [d1, pr(DX1 + .05, DT, BZ - .75), pr(DX1 + .05, FLOOR, BZ - .75), d2]
    b += f'<polygon points="{P(leaf)}" fill="#6a3c22" stroke="#1a0c06" stroke-width="5"/>'
    lp = lambda t, s: (leaf[0][0] + (leaf[1][0] - leaf[0][0]) * t, leaf[0][1] + (leaf[3][1] - leaf[0][1]) * s + (leaf[1][1] - leaf[0][1]) * t * (1 - s) + (leaf[2][1] - leaf[3][1]) * t * s)
    for s0, s1 in ((.08, .45), (.55, .92)):
        b += f'<polygon points="{P([lp(.2, s0), lp(.8, s0), lp(.8, s1), lp(.2, s1)])}" fill="none" stroke="#3a1e10" stroke-width="4"/>'
    b += f'<polygon points="{P([leaf[0], (leaf[0][0] + 8, leaf[0][1]), (leaf[3][0] + 8, leaf[3][1]), leaf[3]])}" fill="#dff2ff" opacity=".9"/>'
    # light spill on the floor toward us
    sp = [d3, d2, pr(1.6, FLOOR, 1.6), pr(-1.8, FLOOR, 1.6)]
    b += f'<polygon points="{P(sp)}" fill="#bfe6ff" opacity=".22" filter="url(#b8)"/>'
    b += f'<polygon points="{P([d3, d2, pr(.9, FLOOR, 3.2), pr(-1.0, FLOOR, 3.2)])}" fill="#e6f6ff" opacity=".25" filter="url(#b8)"/>'
    # rays
    for k in range(7):
        a = -.9 + k * .3
        b += f'<path d="M{dcx:.0f} {dcy:.0f} L{dcx + 1400 * math.sin(a) - 30:.0f} {dcy + 1400 * math.cos(a):.0f} L{dcx + 1400 * math.sin(a) + 30:.0f} {dcy + 1400 * math.cos(a):.0f}Z" fill="#cfeaff" opacity=".05"/>'
    # ---- bunting across the ceiling (blank flags) ----
    for Z, sag, cols in ((5.6, .35, ['#f2d27a', '#e0566a', '#5ab4e0', '#8ad06a']), (3.4, .45, ['#e0566a', '#f2d27a', '#8ad06a', '#5ab4e0'])):
        N = 16; pts = []
        for i in range(N + 1):
            t = i / N; X = -1.6 + (WR + 1.6) * t; Y = CEIL + .35 + sag * math.sin(math.pi * t)
            pts.append(pr(X, Y, Z))
        b += f'<polyline points="{P(pts)}" fill="none" stroke="#e8d8b8" stroke-width="2.5"/>'
        for i in range(N):
            p0, p1 = pts[i], pts[i + 1]; L = (p1[0] - p0[0])
            b += f'<path d="M{p0[0] + L * .1:.0f} {p0[1]:.0f} L{p1[0] - L * .1:.0f} {p1[1]:.0f} L{(p0[0] + p1[0]) / 2:.0f} {(p0[1] + p1[1]) / 2 + abs(L) * .9:.0f}Z" fill="{cols[i % 4]}" stroke="#2a1606" stroke-width="2"/>'
    # ---- clock above the door, at 12 ----
    ccx, ccy, cr = dcx, d0[1] - 170, 78
    b += f'<circle cx="{ccx:.0f}" cy="{ccy:.0f}" r="{cr + 60}" fill="#ffe2a0" opacity=".35" filter="url(#b26)"/>'
    b += f'<circle cx="{ccx:.0f}" cy="{ccy:.0f}" r="{cr + 12}" fill="#c99a3a" stroke="#2a1606" stroke-width="5"/>'
    b += f'<circle cx="{ccx:.0f}" cy="{ccy:.0f}" r="{cr}" fill="#fff8e0" stroke="#5a3a10" stroke-width="3"/>'
    for k in range(12):
        a = k * math.pi / 6
        b += f'<line x1="{ccx + (cr - 8) * math.sin(a):.1f}" y1="{ccy - (cr - 8) * math.cos(a):.1f}" x2="{ccx + (cr - 20) * math.sin(a):.1f}" y2="{ccy - (cr - 20) * math.cos(a):.1f}" stroke="#2a1606" stroke-width="{5 if k % 3 == 0 else 2.6}"/>'
    b += f'<path d="M{ccx:.0f} {ccy + 8:.0f} V{ccy - 44:.0f} M{ccx + 4:.0f} {ccy + 8:.0f} V{ccy - 62:.0f}" stroke="#1a0c06" stroke-width="7" stroke-linecap="round"/>'
    b += f'<circle cx="{ccx:.0f}" cy="{ccy:.0f}" r="7" fill="#c99a3a" stroke="#1a0c06" stroke-width="3"/>'
    b += f'<path d="M{ccx - 52:.0f} {ccy - 30:.0f} A62 62 0 0 1 {ccx - 10:.0f} {ccy - 62:.0f}" fill="none" stroke="#fff" stroke-width="8" opacity=".7" stroke-linecap="round"/>'
    # ---- the long table (one point perspective) ----
    TY, TX0, TX1, TZ0, TZ1 = .82, .1, 1.05, 2.05, 5.4
    def chair(X, Z, side):
        sc = F / Z
        seat = [pr(X - .22, 1.1, Z - .22), pr(X + .22, 1.1, Z - .22), pr(X + .22, 1.1, Z + .22), pr(X - .22, 1.1, Z + .22)]
        bx = X - .22 if side < 0 else X + .22
        backp = [pr(bx, 1.1, Z - .22), pr(bx, .1, Z - .22), pr(bx, .1, Z + .22), pr(bx, 1.1, Z + .22)]
        g = ''
        for xx, zz in ((X - .2, Z - .2), (X + .2, Z - .2), (X - .2, Z + .2), (X + .2, Z + .2)):
            a, c = pr(xx, 1.1, zz), pr(xx, FLOOR, zz)
            g += f'<line x1="{a[0]:.0f}" y1="{a[1]:.0f}" x2="{c[0]:.0f}" y2="{c[1]:.0f}" stroke="#2a140a" stroke-width="{max(2, sc * .045):.1f}"/>'
        g += f'<polygon points="{P(seat)}" fill="#8a2a2a" stroke="#2a0c0c" stroke-width="{max(1.5, sc * .01):.1f}"/>'
        g += f'<polygon points="{P(backp)}" fill="#6a3a20" stroke="#2a140a" stroke-width="{max(1.5, sc * .012):.1f}"/>'
        inner = [pr(bx, .9, Z - .14), pr(bx, .3, Z - .14), pr(bx, .3, Z + .14), pr(bx, .9, Z + .14)]
        g += f'<polygon points="{P(inner)}" fill="#8a2a2a" stroke="#2a140a" stroke-width="{max(1, sc * .008):.1f}"/>'
        return g
    far_chairs = ''.join(chair(TX1 + .45, z, 1) for z in (5.0, 4.2, 3.4))
    near_side = ''.join(chair(TX0 - .45, z, -1) for z in (5.0, 4.2, 3.4, 2.6))
    b += far_chairs
    # table body (cloth drape)
    top = [pr(TX0, TY, TZ1), pr(TX1, TY, TZ1), pr(TX1, TY, TZ0), pr(TX0, TY, TZ0)]
    drapeL = [pr(TX0, TY, TZ1), pr(TX0, TY, TZ0), pr(TX0, TY + .55, TZ0), pr(TX0, TY + .55, TZ1)]
    drapeF = [pr(TX0, TY, TZ0), pr(TX1, TY, TZ0), pr(TX1, TY + .55, TZ0), pr(TX0, TY + .55, TZ0)]
    b += near_side
    b += f'<polygon points="{P(drapeL)}" fill="#cfc6b8" stroke="#3a2a20" stroke-width="3"/>'
    for k in range(1, 10):
        z = TZ0 + (TZ1 - TZ0) * k / 10; a, c = pr(TX0, TY + .05, z), pr(TX0, TY + .55, z)
        b += f'<line x1="{a[0]:.0f}" y1="{a[1]:.0f}" x2="{c[0]:.0f}" y2="{c[1]:.0f}" stroke="#a89a88" stroke-width="2"/>'
    b += f'<polygon points="{P(top)}" fill="url(#clothB)" stroke="#3a2a20" stroke-width="3"/>'
    b += f'<polygon points="{P(drapeF)}" fill="#ddd4c6" stroke="#3a2a20" stroke-width="3"/>'
    for k in range(1, 8):
        x = TX0 + (TX1 - TX0) * k / 8; a, c = pr(x, TY + .05, TZ0), pr(x, TY + .55, TZ0)
        b += f'<path d="M{a[0]:.0f} {a[1]:.0f} L{c[0]:.0f} {c[1]:.0f}" stroke="#b5aa98" stroke-width="3"/>'
    # cool rim light from the door along the far edge of the cloth
    b += f'<line x1="{top[0][0]:.0f}" y1="{top[0][1]:.0f}" x2="{top[1][0]:.0f}" y2="{top[1][1]:.0f}" stroke="#dff2ff" stroke-width="4"/>'
    # plates, flutes along the table
    def flute(X, Z, full=True):
        a = pr(X, TY, Z); sc = F / Z * .0011
        h, w = 230 * sc, 46 * sc
        g = f'<ellipse cx="{a[0]:.1f}" cy="{a[1]:.1f}" rx="{w * .55:.1f}" ry="{w * .16:.1f}" fill="#dff2ff" opacity=".8"/>'
        g += f'<line x1="{a[0]:.1f}" y1="{a[1]:.1f}" x2="{a[0]:.1f}" y2="{a[1] - h * .45:.1f}" stroke="#e6f6ff" stroke-width="{max(1.2, w * .1):.1f}"/>'
        g += f'<path d="M{a[0] - w / 2:.1f} {a[1] - h:.1f} Q{a[0] - w / 2:.1f} {a[1] - h * .42:.1f} {a[0]:.1f} {a[1] - h * .45:.1f} Q{a[0] + w / 2:.1f} {a[1] - h * .42:.1f} {a[0] + w / 2:.1f} {a[1] - h:.1f}Z" fill="#cfeaff" fill-opacity=".25" stroke="#e6f6ff" stroke-width="{max(1, w * .06):.1f}"/>'
        if full:
            g += f'<path d="M{a[0] - w * .44:.1f} {a[1] - h * .82:.1f} Q{a[0] - w * .4:.1f} {a[1] - h * .46:.1f} {a[0]:.1f} {a[1] - h * .47:.1f} Q{a[0] + w * .4:.1f} {a[1] - h * .46:.1f} {a[0] + w * .44:.1f} {a[1] - h * .82:.1f}Z" fill="#f2c95a" opacity=".9"/>'
            for _ in range(3):
                g += f'<circle cx="{a[0] + r.uniform(-w * .25, w * .25):.1f}" cy="{a[1] - h * r.uniform(.55, .78):.1f}" r="{max(.8, w * .05):.1f}" fill="#fff8d0"/>'
        g += f'<path d="M{a[0] - w * .35:.1f} {a[1] - h * .95:.1f} q{-w * .05:.1f} {h * .25:.1f} {w * .05:.1f} {h * .4:.1f}" fill="none" stroke="#fff" stroke-width="{max(1, w * .08):.1f}" opacity=".8"/>'
        return g
    def plate(X, Z):
        a = pr(X, TY, Z); sc = F / Z
        return f'<ellipse cx="{a[0]:.1f}" cy="{a[1]:.1f}" rx="{sc * .14:.1f}" ry="{sc * .045:.1f}" fill="#fbf7ee" stroke="#a89a88" stroke-width="1.5"/><ellipse cx="{a[0]:.1f}" cy="{a[1]:.1f}" rx="{sc * .09:.1f}" ry="{sc * .028:.1f}" fill="none" stroke="#c9a65a" stroke-width="1.5"/>'
    items = []
    for z in (5.0, 4.2, 3.4, 2.6):
        items.append((z, plate(TX0 + .3, z) + flute(TX0 + .52, z - .1)))
        items.append((z - .01, plate(TX1 - .3, z) + flute(TX1 - .1, z - .1)))
    # cake stand mid table
    def cake(X, Z):
        a = pr(X, TY, Z); sc = F / Z
        g = f'<path d="M{a[0] - sc * .03:.0f} {a[1]:.0f} h{sc * .06:.0f} l{-sc * .02:.0f} {-sc * .12:.0f} h{-sc * .02:.0f}z" fill="#d8c8a8"/>'
        g += f'<ellipse cx="{a[0]:.0f}" cy="{a[1] - sc * .12:.0f}" rx="{sc * .2:.0f}" ry="{sc * .05:.0f}" fill="#f4eee2" stroke="#8a7a60" stroke-width="2"/>'
        for k in range(5):
            g += f'<circle cx="{a[0] - sc * .14 + k * sc * .07:.0f}" cy="{a[1] - sc * .16:.0f}" r="{sc * .035:.0f}" fill="{["#e88aa8", "#f2d27a", "#8ad0e0", "#e88aa8", "#c8e08a"][k]}" stroke="#5a3a2a" stroke-width="1.5"/>'
        return g
    items.append((3.8, cake((TX0 + TX1) / 2, 3.8)))
    for z, s in sorted(items, key=lambda t: -t[0]):
        b += s
    # champagne on ice (near end of the table)
    ia = pr(.62, TY, 2.4); sc = F / 2.4
    bw, bh = sc * .26, sc * .3
    bx, by = ia
    # bottle behind the rim
    b += (f'<g transform="translate({bx + sc * .02:.0f} {by - bh * .55:.0f}) rotate(14)" stroke="#06100a" stroke-width="4" stroke-linejoin="round">'
          f'<path d="M-{sc * .05:.0f} 0 v{-sc * .22:.0f} q0 {-sc * .06:.0f} {sc * .03:.0f} {-sc * .1:.0f} v{-sc * .1:.0f} h{sc * .04:.0f} v{sc * .1:.0f} q{sc * .03:.0f} {sc * .04:.0f} {sc * .03:.0f} {sc * .1:.0f} v{sc * .22:.0f}z" fill="#163a24"/>'
          f'<path d="M-{sc * .022:.0f} {-sc * .42:.0f} h{sc * .044:.0f} v{-sc * .07:.0f} h{-sc * .044:.0f}z" fill="#e2b34a"/>'
          f'<rect x="-{sc * .05:.0f}" y="{-sc * .2:.0f}" width="{sc * .1:.0f}" height="{sc * .08:.0f}" fill="#f6ecd0"/>'
          f'<path d="M-{sc * .032:.0f} {-sc * .3:.0f} v{sc * .26:.0f}" stroke="#bfe6ff" stroke-width="6" opacity=".7"/></g>')
    b += (f'<path d="M{bx - bw / 2:.0f} {by - bh:.0f} L{bx + bw / 2:.0f} {by - bh:.0f} L{bx + bw * .4:.0f} {by:.0f} Q{bx:.0f} {by + bw * .12:.0f} {bx - bw * .4:.0f} {by:.0f}Z" fill="#b8c2cc" stroke="#2a2f36" stroke-width="4"/>')
    b += f'<ellipse cx="{bx:.0f}" cy="{by - bh:.0f}" rx="{bw / 2:.0f}" ry="{bw * .14:.0f}" fill="#e6eef6" stroke="#2a2f36" stroke-width="4"/>'
    for _ in range(9):   # ice cubes
        ix, iy = bx + r.uniform(-bw * .38, bw * .38), by - bh + r.uniform(-bw * .1, bw * .02)
        s_ = r.uniform(14, 22)
        b += f'<rect x="{ix - s_ / 2:.0f}" y="{iy - s_ / 2:.0f}" width="{s_:.0f}" height="{s_:.0f}" rx="4" fill="#e9f8ff" stroke="#9ac8e0" stroke-width="2" transform="rotate({r.randint(-30, 30)} {ix:.0f} {iy:.0f})"/>'
    b += f'<path d="M{bx - bw * .36:.0f} {by - bh * .8:.0f} L{bx - bw * .3:.0f} {by - bh * .1:.0f}" stroke="#fff" stroke-width="8" opacity=".7" stroke-linecap="round"/>'
    b += f'<path d="M{bx - bw * .45:.0f} {by - bh * .55:.0f} q{bw * .45:.0f} {bw * .1:.0f} {bw * .9:.0f} 0" fill="none" stroke="#2a2f36" stroke-width="3"/>'
    for k in range(4):   # condensation drops
        b += f'<ellipse cx="{bx + bw * (-.2 + k * .14):.0f}" cy="{by - bh * (.3 + .1 * (k % 2)):.0f}" rx="3" ry="5" fill="#fff" opacity=".8"/>'
    b += flute(.92, 2.35) + flute(.82, 2.6)
    # ---- balloons tied to the far chair, floating up ----
    anchor = pr(TX1 + .45, .1, 3.4)
    for (X, Y, Z, col, hi) in ((1.7, -1.2, 3.9, '#e0566a', '#ffb3be'), (2.15, -.95, 3.5, '#f2d27a', '#fff3c2'), (2.05, -1.5, 4.5, '#5ab4e0', '#c8ecff'), (2.55, -1.3, 4.2, '#9a6ae0', '#dccbff')):
        c = pr(X, Y, Z); rr = F / Z * .26
        b += f'<path d="M{anchor[0]:.0f} {anchor[1]:.0f} Q{(anchor[0] + c[0]) / 2 - 30:.0f} {(anchor[1] + c[1]) / 2:.0f} {c[0]:.0f} {c[1] + rr * 1.15:.0f}" fill="none" stroke="#e8e0d0" stroke-width="2"/>'
        b += f'<ellipse cx="{c[0]:.0f}" cy="{c[1]:.0f}" rx="{rr:.0f}" ry="{rr * 1.18:.0f}" fill="{col}" stroke="#2a1606" stroke-width="4"/>'
        b += f'<path d="M{c[0] - 8:.0f} {c[1] + rr * 1.15:.0f} l8 {-12} l8 12z" fill="{col}" stroke="#2a1606" stroke-width="3"/>'
        b += f'<ellipse cx="{c[0] - rr * .35:.0f}" cy="{c[1] - rr * .45:.0f}" rx="{rr * .22:.0f}" ry="{rr * .35:.0f}" fill="{hi}" opacity=".9" transform="rotate(-25 {c[0] - rr * .35:.0f} {c[1] - rr * .45:.0f})"/>'
        b += f'<path d="M{c[0] - rr * .9:.0f} {c[1] + rr * .2:.0f} a{rr:.0f} {rr * 1.18:.0f} 0 0 0 {rr * .6:.0f} {rr * .85:.0f}" fill="none" stroke="#dff2ff" stroke-width="4" opacity=".5"/>'
    # ---- frog: party hat, horn, sitting on the near-left chair, looking at the door ----
    FX, FY, FS = 760, 905, 2.45
    b += chair(TX0 - .55, 1.65, -1).replace('', '') if False else ''
    seatc = (FX, FY + 6)
    b += f'<path d="M{FX - 120} {FY + 8} L{FX + 120} {FY + 8} L{FX + 150} {FY + 40} L{FX - 150} {FY + 40}Z" fill="#8a2a2a" stroke="#2a0c0c" stroke-width="4"/>'
    b += f'<rect x="{FX - 150}" y="{FY + 40}" width="300" height="22" fill="#5a1a1a" stroke="#2a0c0c" stroke-width="4"/>'
    for lx in (FX - 140, FX + 128):
        b += f'<rect x="{lx}" y="{FY + 62}" width="14" height="140" fill="#3a1a0c" stroke="#1a0a04" stroke-width="3"/>'
    b += f'<path d="M{FX - 150} {FY + 40} L{FX - 160} {FY - 220} L{FX - 120} {FY - 230} L{FX - 112} {FY + 8}Z" fill="#6a3a20" stroke="#2a140a" stroke-width="4"/>'
    hat = ('<path d="M-22 -86 L4 -168 L34 -86z" fill="#5ab4e0" stroke-width="3.4"/>'
           '<path d="M-14 -110 L26 -110 M-6 -134 L18 -134" stroke="#f2d27a" stroke-width="7"/>'
           '<circle cx="4" cy="-170" r="9" fill="#f2d27a" stroke-width="3"/>'
           '')
    horn = ('<g transform="translate(58 -30) rotate(-18)"><path d="M0 -5 L46 -12 L46 12 L0 5z" fill="#e0566a" stroke-width="3"/>'
            '<path d="M14 -7 v14 M28 -9 v18" stroke="#f2d27a" stroke-width="4"/><ellipse cx="48" cy="0" rx="5" ry="13" fill="#f2d27a" stroke-width="3"/></g>')
    b += frog(FX, FY, FS, flip=False, look=(6, -1), mouth='o', top=hat, front=horn,
              armR='M38 -24 q16 2 22 -6', armL='M-34 -22 q-14 6 -16 22')
    # confetti on the floor / table
    for _ in range(70):
        x, y = r.uniform(380, 1560), r.uniform(720, 1060)
        if x > 1600 and y > 880: continue
        b += f'<rect x="{x:.0f}" y="{y:.0f}" width="{r.uniform(6, 12):.0f}" height="{r.uniform(3, 6):.0f}" fill="{r.choice(["#f2d27a", "#e0566a", "#5ab4e0", "#8ad06a"])}" opacity=".85" transform="rotate({r.randint(0, 180)} {x:.0f} {y:.0f})"/>'
    # dust in the door light
    for _ in range(50):
        x, y = r.uniform(dcx - 300, dcx + 360), r.uniform(dcy - 260, dcy + 360)
        b += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r.choice([1.4, 2, 2.8])}" fill="#e8f6ff" opacity="{r.uniform(.3, .8):.2f}"/>'
    b += sparkles([(dcx + 160, dcy - 150, 22), (dcx - 190, dcy + 40, 16), (ccx + 120, ccy - 20, 16), (1560, 300, 14)], '#eaf6ff')
    b += '<rect width="1920" height="1080" fill="url(#vigB)"/>'
    lines = [('INVITES SENT', 104, 'w'), ('AFTERWARD', 140, 'y')]
    return page('#120a0e', svg(defs, b), lines, outline='#12060a', top=48)


# ====================================================================== C  (wormhole blown up by feedback)
def thumb_C():
    r = random.Random(21)
    TX, TY = 1290, 520     # throat
    A_, K, R = 46, 78, 640
    defs = FILTERS
    defs += lin('spC', [(0, '#05030f'), (.5, '#0c0828'), (1, '#140a26')])
    defs += rad('nebC1', 1500, 260, 600, [(0, '#7a3ac8', .55), (.6, '#3a2a8a', .2), (1, '#3a2a8a', 0)])
    defs += rad('nebC2', 600, 850, 700, [(0, '#1a8ac8', .4), (1, '#1a8ac8', 0)])
    defs += rad('blastC', TX, TY, 330, [(0, '#ffffff', 1), (.12, '#fff3c0', 1), (.3, '#ffb347', .8), (.6, '#ff4a6a', .3), (1, '#ff4a6a', 0)])
    defs += rad('vigC', 960, 540, 1150, [(0, '#000', 0), (.62, '#000', 0), (1, '#000', .65)])
    b = '<rect width="1920" height="1080" fill="url(#spC)"/>'
    b += '<rect width="1920" height="1080" fill="url(#nebC1)"/><rect width="1920" height="1080" fill="url(#nebC2)"/>'
    b += starfield(r, 260, 0, 0, 1920, 1080)
    # wormhole embedding diagram: two funnel sheets meeting at the throat
    def depth(rr): return K * math.acosh(max(1.0, rr / A_))
    radii = [A_ * math.cosh(k * .26) for k in range(1, 14)]
    radii = [x for x in radii if x < R]
    def sheet(sign, col):
        g = ''
        for k, rr in enumerate(radii):
            y = TY - sign * depth(rr); fade = 1 - (rr / R) ** 2
            g += f'<ellipse cx="{TX}" cy="{y:.1f}" rx="{rr:.1f}" ry="{rr * .26:.1f}" fill="none" stroke="{col}" stroke-width="{1.5 + 2.5 * fade:.1f}" opacity="{.25 + .65 * fade:.2f}"/>'
        for k in range(24):
            a = k * math.pi / 12; pts = []
            for rr in [A_ * 1.02] + radii:
                pts.append((TX + rr * math.cos(a), TY - sign * depth(rr) + rr * .26 * math.sin(a)))
            g += f'<polyline points="{P(pts)}" fill="none" stroke="{col}" stroke-width="2" opacity=".55"/>'
        return g
    # back halves glow
    b += f'<ellipse cx="{TX}" cy="{TY - depth(R * .9):.0f}" rx="{R}" ry="{R * .3:.0f}" fill="#4ad8ff" opacity=".08" filter="url(#b26)"/>'
    b += f'<ellipse cx="{TX}" cy="{TY + depth(R * .9):.0f}" rx="{R}" ry="{R * .3:.0f}" fill="#c86aff" opacity=".1" filter="url(#b26)"/>'
    b += f'<g filter="url(#b4)" opacity=".7">{sheet(1, "#5ae0ff")}{sheet(-1, "#d07aff")}</g>'
    b += sheet(1, '#9af0ff') + sheet(-1, '#e6b0ff')
    # feedback rings around the throat (growing, each brighter)
    for k in range(7):
        rr = 70 + k * 62
        col = mix(['#ffffff', '#ffd27a', '#ff7a4a', '#ff3a7a'], k / 6)
        b += f'<ellipse cx="{TX}" cy="{TY}" rx="{rr}" ry="{rr * .55:.0f}" fill="none" stroke="{col}" stroke-width="{14 - k * 1.5:.1f}" opacity="{.95 - k * .1:.2f}" filter="url(#b4)"/>'
        b += f'<ellipse cx="{TX}" cy="{TY}" rx="{rr}" ry="{rr * .55:.0f}" fill="none" stroke="#fff6e0" stroke-width="{3 - k * .3:.1f}" opacity="{.9 - k * .1:.2f}"/>'
    # blast at the throat
    b += f'<circle cx="{TX}" cy="{TY}" r="330" fill="url(#blastC)"/>'
    for k in range(18):   # spikes
        a = k * 2 * math.pi / 18 + r.uniform(-.1, .1); L = r.uniform(140, 300)
        b += f'<path d="M{TX + 20 * math.cos(a + .2):.0f} {TY + 20 * math.sin(a + .2):.0f} L{TX + L * math.cos(a):.0f} {TY + L * math.sin(a) * .8:.0f} L{TX + 20 * math.cos(a - .2):.0f} {TY + 20 * math.sin(a - .2):.0f}Z" fill="#fff3c0" opacity=".7"/>'
    b += f'<circle cx="{TX}" cy="{TY}" r="70" fill="#fff" filter="url(#b14)"/>'
    # broken grid fragments flying out
    for _ in range(26):
        a = r.uniform(0, 2 * math.pi); d = r.uniform(180, 520)
        x, y = TX + d * math.cos(a), TY + d * math.sin(a) * .7
        if x < 700 and y < 520: continue
        s_ = r.uniform(18, 46); rot = r.randint(0, 180)
        col = r.choice(['#9af0ff', '#e6b0ff', '#ffd27a'])
        b += f'<path d="M{x:.0f} {y:.0f} l{s_:.0f} {-s_ * .3:.0f} l{-s_ * .2:.0f} {s_ * .7:.0f}z" fill="none" stroke="{col}" stroke-width="3" transform="rotate({rot} {x:.0f} {y:.0f})"/>'
    for _ in range(80):
        a = r.uniform(0, 2 * math.pi); d = r.uniform(120, 600)
        x, y = TX + d * math.cos(a), TY + d * math.sin(a) * .75
        if x < 700 and y < 520: continue
        b += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r.choice([2, 3, 4]) * 3}" fill="#ffb347" opacity=".2" filter="url(#b4)"/><circle cx="{x:.0f}" cy="{y:.0f}" r="{r.choice([1.5, 2.2, 3])}" fill="#fff3c0"/>'
    # ---- loudspeaker floating on the right, facing the throat ----
    SX, SY = 1735, 470
    b += f'<g transform="translate({SX} {SY}) rotate(-8)" stroke="#0a0a14" stroke-width="5" stroke-linejoin="round">'
    b += '<rect x="-95" y="-150" width="190" height="300" rx="16" fill="#2a2a3a"/>'
    b += '<rect x="-80" y="-136" width="160" height="272" rx="10" fill="#1a1a26" stroke-width="3"/>'
    b += '<circle cx="0" cy="40" r="66" fill="#3a3a4e"/><circle cx="0" cy="40" r="46" fill="#22222e" stroke-width="3"/><circle cx="0" cy="40" r="18" fill="#4a4a60" stroke-width="3"/>'
    b += '<circle cx="0" cy="-84" r="30" fill="#3a3a4e"/><circle cx="0" cy="-84" r="12" fill="#22222e" stroke-width="3"/>'
    b += '<path d="M-95 -120 v240" stroke="#ff9a6a" stroke-width="6" opacity=".8"/>'
    b += '<path d="M-60 -10 a66 66 0 0 0 0 100" fill="none" stroke="#ffd27a" stroke-width="5" opacity=".9"/>'
    b += '</g>'
    for k in range(4):   # sound arcs from the speaker toward the throat
        rr = 120 + k * 55
        b += f'<path d="M{SX - 60 - rr * .35:.0f} {SY - rr * .7:.0f} Q{SX - 120 - rr * .75:.0f} {SY + 30:.0f} {SX - 60 - rr * .35:.0f} {SY + rr * .8:.0f}" fill="none" stroke="#ffd27a" stroke-width="{7 - k:.0f}" opacity="{.85 - k * .15:.2f}" stroke-linecap="round"/>'
    # ---- astronaut frog holding a microphone (lower left) ----
    FX, FY, FS = 700, 900, 2.5
    helmet_back = '<circle cx="6" cy="-58" r="62" fill="#9ad8ff" fill-opacity=".14" stroke="none"/>'
    suit = ('<path d="M-36 2 q-8 -40 2 -50 q38 -12 76 0 q10 14 2 50 q-40 10 -80 0z" fill="#eef2f6" stroke-width="3.6"/>'
            '<rect x="-12" y="-30" width="34" height="20" rx="4" fill="#cfd8e2" stroke-width="2.6"/>'
            '<circle cx="-2" cy="-20" r="3.4" fill="#e0566a" stroke="none"/><circle cx="10" cy="-20" r="3.4" fill="#5ab4e0" stroke="none"/>')
    helmet = ('<circle cx="6" cy="-58" r="62" fill="none" stroke-width="4"/>'
              '<path d="M-38 -96 q24 -28 64 -22" fill="none" stroke="#fff" stroke-width="7" opacity=".75"/>'
              '<path d="M-48 -18 q54 30 108 0" fill="none" stroke="#cfd8e2" stroke-width="10"/>')
    mic = ('<g transform="translate(74 -46) rotate(-38)">'
           '<rect x="-7" y="0" width="14" height="58" rx="5" fill="#2a2a3a" stroke-width="3"/>'
           '<path d="M-14 0 h28 l-3 -10 h-22z" fill="#8a8f9c" stroke-width="3"/>'
           '<ellipse cx="0" cy="-26" rx="20" ry="24" fill="#b8bec8" stroke-width="3.4"/>'
           '<path d="M-16 -32 h32 M-18 -22 h36 M-14 -12 h28 M-6 -46 v38 M6 -46 v38" stroke="#6a707c" stroke-width="2"/>'
           '<path d="M-10 -40 q-4 10 0 22" fill="none" stroke="#fff" stroke-width="4" opacity=".8"/></g>')
    b += frog(FX, FY, FS, rot=-6, look=(6, -4), mouth='O', back=helmet_back, mid=suit, top=helmet, sleeve='#eef2f6',
              hands=mic, armR='M38 -24 q24 -6 30 -26', armL='M-34 -22 q-18 -10 -22 -36')
    # wavy feedback squiggle between mic and blast
    pts = []
    for i in range(60):
        t = i / 59; x = 960 + (TX - 120 - 960) * t; y = 690 + (TY + 60 - 690) * t
        a = 14 * math.sin(t * 34) * (0.3 + t)
        pts.append((x + a * .5, y + a))
    b += f'<polyline points="{P(pts)}" fill="none" stroke="#ff7ab0" stroke-width="5" opacity=".85" stroke-linecap="round"/>'
    b += f'<polyline points="{P(pts)}" fill="none" stroke="#ff7ab0" stroke-width="14" opacity=".25" filter="url(#b4)"/>'
    b += sparkles([(1080, 170, 20), (1640, 220, 16), (820, 620, 14), (1520, 800, 16), (1880, 200, 12)], '#fff1e0')
    b += '<rect width="1920" height="1080" fill="url(#vigC)"/>'
    lines = [('NATURE', 140, 'w'), ('BLOWS', 210, 'y'), ('IT UP?', 140, 'w')]
    return page('#05030f', svg(defs, b), lines, outline='#07041a', top=50)


for n, fn in (('A', thumb_A), ('B', thumb_B), ('C', thumb_C)):
    open(os.path.join(HERE, f'{n}.html'), 'w').write(fn())
print('ok')
