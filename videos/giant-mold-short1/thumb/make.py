# VERTICAL (9:16, 1080x1920) thumbnail A for each of the five giant-mold shorts (guideline 16-9, 2026-11-06: text centred, no empty corner).
# Run: python3 videos/giant-mold-short1/thumb/make.py  -> videos/giant-mold-short{1..5}/thumb/A.html (+ common.css, Fredoka-700.woff2 from tools/assets/thumb_v)
# Reuses the pillar / frog / small-life helpers of videos/giant-mold/thumb/make.py (executed up to its first thumbnail, no side effects).
# Layout for every short: tall subject runs through the frame, text block centred around mid-height, frog in the lower third,
#   nothing important above y~200 or below y~1760 (YouTube UI).
# short1 EARTH / LOOKED / ALIEN      violet dusk plain, a tall pale pillar rising through the frame, smaller pillars, moon; tourist frog.
# short2 NOT / WOOD / AT ALL         glowing cut end of a fossil log with woven tubes (no rings); detective frog with magnifier.
# short3 WHY BUILD / A / TOWER?      tall pillar in a windy sky, goggles/scarf frog on top, spores streaming on the high wind.
# short4 A HOME / AND A / MEAL?      cut-away window into the pillar base: tunnels, millipede, springtails; frog with bib and fork (hedged -> ?).
# short5 OUTGROWN / BY / TREES       tall Archaeopteris over a small cracked pillar whose gold crown falls; leaf-hat frog catches it.
import os, sys, math, random, shutil
HERE = os.path.dirname(os.path.abspath(__file__))
VID = os.path.abspath(os.path.join(HERE, '..', '..'))
TOOLS = os.path.abspath(os.path.join(VID, '..', 'tools'))
SRC = os.path.join(VID, 'giant-mold', 'thumb', 'make.py')
_s = open(SRC).read()
G = {'__file__': SRC, '__name__': 'giantmold_helpers'}
exec(_s.split('# ================= A:')[0], G)
exec(_s[_s.index('def frond('):_s.index('def make_C(')], G)
pillar, frog, cooksonia, millipede, springtail, trigono, moss, rock, frond, P = (G[k] for k in (
    'pillar', 'frog', 'cooksonia', 'millipede', 'springtail', 'trigono', 'moss', 'rock', 'frond', 'P'))
FILTERS = G['FILTERS']
sys.path.insert(0, TOOLS)
from thumb_lib import vpage, vsvg, lin, rad, spark

W, H = 1080, 1920
VIG = lambda col, a=.75: rad('vig', 540, 960, 1250, [(0, '#000', 0), (.6, '#000', 0), (1, col, a)])


def dust(rnd, n, cx, sx, y0, y1, col='#fff0c8'):
    return ''.join(f'<circle cx="{rnd.gauss(cx, sx):.0f}" cy="{rnd.uniform(y0, y1):.0f}" r="{rnd.choice([1.4, 2, 2.8])}" fill="{col}" opacity="{rnd.uniform(.2, .7):.2f}"/>' for _ in range(n))


# ================= short1 =================
def make_1():
    rnd = random.Random(401)
    d = FILTERS; hz = 1360
    d += lin('sky', [(0, '#14163a'), (.3, '#2e2e64'), (.55, '#6a5088'), (.7, '#c88088'), (.71, '#ffc590'), (1, '#ffc590')])
    d += rad('glow', 760, 1360, 900, [(0, '#ffd8a0', .8), (.2, '#ff9f80', .35), (.6, '#a06090', .08), (1, '#000', 0)])
    d += lin('gnd', [(0, '#3a3a52'), (.25, '#26303a'), (1, '#0c1014')])
    d += lin('riv', [(0, '#ffc8a0'), (.4, '#a07aa0'), (1, '#3a3a6a')])
    d += VIG('#06050e')
    b = f'<rect width="{W}" height="{H}" fill="url(#sky)"/><rect width="{W}" height="{H}" fill="url(#glow)"/>'
    for _ in range(150):
        y = rnd.uniform(10, 1000)
        b += f'<circle cx="{rnd.uniform(0, W):.0f}" cy="{y:.0f}" r="{rnd.choice([1, 1.5, 2.2])}" fill="#eef" opacity="{rnd.uniform(.2, .8) * (1 - y / 1250):.2f}"/>'
    mx, my = 250, 430
    b += f'<circle cx="{mx}" cy="{my}" r="230" fill="#ffe8d8" opacity=".25" filter="url(#b50)"/><circle cx="{mx}" cy="{my}" r="128" fill="#f6e6e4"/>'
    for cx, cy, r in ((-40, -30, 22), (40, 40, 16), (30, -40, 10), (-60, 50, 12), (80, -10, 9)):
        b += f'<circle cx="{mx + cx}" cy="{my + cy}" r="{r}" fill="#d8c4cc" opacity=".8"/><circle cx="{mx + cx + 2}" cy="{my + cy + 2}" r="{r * .7:.0f}" fill="#c8b0bc" opacity=".6"/>'
    b += f'<path d="M{mx - 100} {my - 60} a128 128 0 0 0 40 170" fill="none" stroke="#fff" stroke-width="5" opacity=".6"/>'
    for _ in range(8):
        b += f'<ellipse cx="{rnd.uniform(0, W):.0f}" cy="{rnd.uniform(1000, 1320):.0f}" rx="{rnd.uniform(160, 340):.0f}" ry="{rnd.uniform(6, 14):.0f}" fill="#ffc0a8" opacity="{rnd.uniform(.15, .35):.2f}" filter="url(#b8)"/>'
    b += f'<path d="M0 {hz - 12} L70 {hz - 52} L170 {hz - 48} L200 {hz - 26} L430 {hz - 22} L470 {hz - 50} L590 {hz - 54} L620 {hz - 30} L1080 {hz - 24} L1080 {hz + 20} L0 {hz + 20}Z" fill="#5a4a78" opacity=".85"/>'
    b += f'<path d="M0 {hz + 6} Q300 {hz - 14} 600 {hz + 2} T1080 {hz} L1080 {hz + 30} L0 {hz + 30}Z" fill="#46405e"/>'
    b += f'<rect x="0" y="{hz}" width="{W}" height="{H - hz}" fill="url(#gnd)"/>'
    b += (f'<path d="M370 1364 Q330 1400 420 1440 Q560 1500 480 1580 Q400 1660 470 1760 Q520 1840 500 1920 L780 1920 Q700 1820 650 1750 '
          f'Q590 1670 650 1590 Q730 1490 530 1430 Q430 1400 412 1364Z" fill="url(#riv)" opacity=".9"/>')
    b += '<path d="M470 1450 Q560 1490 540 1550 M560 1690 Q600 1760 640 1820" fill="none" stroke="#fff0e0" stroke-width="3" opacity=".6"/>'
    b += moss(0, W, hz + 6, hz + 50, 160, rnd, ['#3a6a5a', '#4a7a62', '#2e5a4c'], 3, 10)
    b += moss(0, W, hz + 50, H, 300, rnd, ['#2a5a4a', '#3c6e58', '#22483c', '#4e8a6a'], 6, 30, (.35, .8))
    pil = [(1020, hz + 4, 120, 10), (590, hz + 6, 150, 12), (330, hz + 8, 220, 17), (90, hz + 10, 300, 22), (1000, hz + 26, 380, 28), (470, hz + 40, 300, 22)]
    for i, (x, yb, h, w) in enumerate(pil):
        dd, oo, *_ = pillar(f's1f{i}', x, yb, h, w, w * .85, rnd.uniform(-8, 8), rnd,
                            [(0, '#4a4262'), (.45, '#8a7e98'), (.85, '#d0b8b8'), (1, '#ffd0a8')], rim='#ffc8a0', rim_side=1,
                            detail=.25 + h / 600, tex_dark='#2a2238', tex_light='#ffe8e0')
        d += dd; b += f'<g opacity="{.65 + h / 1100:.2f}">{oo}</g>'
    b += '<ellipse cx="800" cy="900" rx="230" ry="640" fill="#ffc8a8" opacity=".18" filter="url(#b90)"/>'
    dd, oo, C, Wd, _ = pillar('s1m', 820, 1600, 1290, 128, 98, -40, rnd,
                              [(0, '#3e3654'), (.3, '#6e6480'), (.62, '#a898a8'), (.86, '#e6c8bc'), (1, '#ffd8b0')],
                              rim='#ffd0a8', rim_side=1, detail=2.0, tex_dark='#241c30', tex_light='#ffeee6')
    d += dd; b += oo
    b += f'<polyline points="{P([(C(i / 70)[0] - Wd[i], C(i / 70)[1]) for i in range(4, 71)])}" fill="none" stroke="#b8a8ff" stroke-width="3" opacity=".55"/>'
    tx, ty = C(1)
    b += f'<circle cx="{tx:.0f}" cy="{ty:.0f}" r="120" fill="#ffe0c0" opacity=".3" filter="url(#b26)"/>'
    b += moss(660, 990, 1585, 1615, 120, rnd, ['#4a8a6a', '#5a9a78', '#3a7058'], 4, 12)
    for _ in range(14):
        b += cooksonia(rnd.uniform(680, 980), rnd.uniform(1592, 1616), rnd.uniform(18, 34), rnd, col='#3e7a5a', spc='#ffc070')
    for _ in range(46):
        y = rnd.uniform(hz + 10, 1880); sc = (y - hz) / (H - hz); x = rnd.uniform(0, W)
        if 60 < x < 400 and y > 1450: continue
        if 380 < x < 760 and y > 1430: continue
        b += cooksonia(x, y, 8 + sc * 70, rnd, col='#3a7458', spc='#ffbc6a')
    for _ in range(26):
        y = rnd.uniform(hz + 20, 1880); sc = ((y - hz) / (H - hz)) ** 1.3; x = rnd.uniform(0, W)
        if 60 < x < 400 and y > 1450: continue
        b += rock(x, y, 3 + sc * rnd.uniform(10, 26), rnd, base='#3a3a50', hi='#ffc0a0', sh='#14121e')
    b += millipede(880, 1614, .6, 180, rnd, col='#4a3040', hi='#d88a9a')
    b += spark(mx, my, 34, '#fff6f0') + spark(tx + 90, ty - 40, 22) + spark(960, 560, 14) + spark(120, 1000, 14)
    hat = ('<g transform="translate(6 -95) rotate(-6)"><path d="M-30 4 Q-28 -30 0 -32 Q28 -30 30 4Z" fill="#e8b84a" stroke-width="3.4"/>'
           '<path d="M-50 6 Q0 -8 50 6 Q46 18 0 14 Q-46 18 -50 6Z" fill="#d8a43a" stroke-width="3.2"/><path d="M-28 -4 Q0 -10 28 -4" fill="none" stroke="#c0503a" stroke-width="5"/></g>')
    strap = '<path d="M-30 -38 Q6 0 44 -38" fill="none" stroke="#3a2a1a" stroke-width="3"/>'
    cam = ('<g transform="translate(64 -62) rotate(-14)"><rect x="-26" y="-18" width="52" height="36" rx="6" fill="#2a2a34" stroke-width="3"/>'
           '<rect x="-14" y="-26" width="18" height="10" rx="3" fill="#3a3a44" stroke-width="2.4"/><circle cx="2" cy="0" r="12" fill="#5a6a8a" stroke-width="3"/>'
           '<circle cx="-1" cy="-3" r="4" fill="#cfe0ff" stroke="none"/><circle cx="18" cy="-11" r="3" fill="#ffe08a" stroke="none"/></g>')
    b += '<circle cx="220" cy="1600" r="190" fill="#ffd0b0" opacity=".16" filter="url(#b50)"/>'
    b += frog(220, 1712, 2.5, rot=2, look=(10, -12), mouth='O', shadow=True, mid=strap, top=hat,
              armL='M-34 -22 q-18 6 -20 24', armR='M38 -22 q16 -6 24 -36', front=cam)
    b += f'<g opacity=".9">{dust(rnd, 50, 760, 260, 200, 1500, "#ffe8e0")}</g>'
    b += f'<rect width="{W}" height="{H}" fill="url(#vig)"/>'
    return vpage('#14163a', vsvg(d, b), [('EARTH', 180, 'w'), ('LOOKED', 180, 'w'), ('ALIEN', 270, 'y')], outline='#0c0a1a', top=660)


# ================= short2 =================
def tubes(rnd, cx, cy, rx, ry, n, wmin, wmax, cols):
    o = ''
    for _ in range(n):
        x = rnd.uniform(cx - rx * 1.1, cx + rx * 1.1); y = rnd.uniform(cy - ry * 1.1, cy + ry * 1.1)
        a = rnd.uniform(0, 2 * math.pi); pts = [(x, y)]; seg = rx * rnd.uniform(.05, .09)
        for _ in range(rnd.randint(8, 16)):
            a += rnd.uniform(-.55, .55); x += math.cos(a) * seg; y += math.sin(a) * seg; pts.append((x, y))
        w = rnd.uniform(wmin, wmax); c = rnd.choice(cols)
        o += f'<polyline points="{P(pts)}" fill="none" stroke="#3a2412" stroke-width="{w + 2.5:.1f}" stroke-linecap="round" stroke-linejoin="round" opacity=".7"/>'
        o += f'<polyline points="{P(pts)}" fill="none" stroke="{c}" stroke-width="{w:.1f}" stroke-linecap="round" stroke-linejoin="round"/>'
        o += f'<polyline points="{P([(px - w * .2, py - w * .25) for px, py in pts])}" fill="none" stroke="#fff8e8" stroke-width="{w * .3:.1f}" stroke-linecap="round" opacity=".55"/>'
    return o


def make_2():
    rnd = random.Random(1859)
    d = FILTERS
    cx, cy, rx, ry = 600, 1330, 300, 310
    d += lin('bg', [(0, '#0e2228'), (.6, '#16343a'), (1, '#0a1416')])
    d += rad('spot', cx, cy, 900, [(0, '#ffe6b0', .55), (.35, '#f2b860', .18), (1, '#000', 0)])
    d += lin('bark', [(0, '#3a2e24'), (.35, '#6a5644'), (.6, '#8a7458'), (1, '#2a2018')])
    d += rad('face', cx, cy, 360, [(0, '#f8dca0', 1), (.55, '#d8a868', 1), (.9, '#a8783e', 1), (1, '#6a4826', 1)])
    d += rad('lens', 420, 1440, 150, [(0, '#fff6dc', .12), (.8, '#bfe8ff', .08), (1, '#bfe8ff', .3)])
    d += lin('tbl', [(0, '#4a3422'), (.2, '#2e2016'), (1, '#120c08')])
    d += VIG('#040808', .8)
    b = f'<rect width="{W}" height="{H}" fill="url(#bg)"/>'
    for k in range(20):
        y = 120 + k * 80 + rnd.uniform(-15, 15)
        b += f'<path d="M0 {y:.0f} Q300 {y + rnd.uniform(-30, 30):.0f} 560 {y:.0f} T1080 {y + rnd.uniform(-20, 20):.0f}" fill="none" stroke="#2a4a50" stroke-width="{rnd.uniform(6, 18):.0f}" opacity=".35"/>'
    b += f'<rect width="{W}" height="{H}" fill="url(#spot)"/>'
    b += '<path d="M860 -20 L1100 -20 L1000 1700 L380 1700Z" fill="#fff0c8" opacity=".07"/>'
    b += '<path d="M0 1640 Q540 1610 1080 1630 L1080 1920 L0 1920Z" fill="url(#tbl)"/><path d="M0 1640 Q540 1610 1080 1630" fill="none" stroke="#c8925a" stroke-width="4" opacity=".55"/>'
    body = f'M{cx - 40} {cy - ry + 6} L1120 1000 L1120 1560 L{cx + 60} {cy + ry - 2}Z'
    b += f'<ellipse cx="760" cy="1640" rx="420" ry="34" fill="#000" opacity=".55" filter="url(#b26)"/>'
    b += f'<path d="{body}" fill="url(#bark)" stroke="#120c08" stroke-width="5"/>'
    for k in range(14):
        t = k / 13; y0 = cy - ry + 30 + t * (2 * ry - 60); y1 = 1010 + t * 540
        b += f'<path d="M{cx + 60:.0f} {y0:.0f} Q900 {(y0 + y1) / 2 + rnd.uniform(-20, 20):.0f} 1100 {y1:.0f}" fill="none" stroke="{rnd.choice(["#2a2018", "#a8906c", "#4a3a2a"])}" stroke-width="{rnd.uniform(2, 6):.1f}" opacity=".5"/>'
    b += f'<path d="M{cx - 30} {cy - ry + 8} L1100 1006" stroke="#ffe0a0" stroke-width="6" opacity=".7"/>'
    b += f'<ellipse cx="{cx}" cy="{cy}" rx="{rx + 44}" ry="{ry + 44}" fill="#ffd890" opacity=".35" filter="url(#b26)"/>'
    b += f'<ellipse cx="{cx}" cy="{cy}" rx="{rx + 16}" ry="{ry + 14}" fill="#4a3624" stroke="#120c08" stroke-width="5"/>'
    b += f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="url(#face)"/>'
    d += f'<clipPath id="fc"><ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}"/></clipPath>'
    tx = tubes(rnd, cx, cy, rx, ry, 150, 3, 7, ['#f6e2b4', '#e8c88a', '#fff0d0', '#d8b070'])
    tx += tubes(rnd, cx, cy, rx, ry, 60, 6, 11, ['#fff2d6', '#f0d098'])
    b += f'<g clip-path="url(#fc)">{tx}<ellipse cx="{cx - 80}" cy="{cy - 120}" rx="160" ry="110" fill="#fff" opacity=".18" filter="url(#b26)"/>'
    b += f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="none" stroke="#6a4020" stroke-width="40" opacity=".35" filter="url(#b14)"/></g>'
    b += f'<path d="M{cx - rx + 10} {cy - 60} A{rx} {ry} 0 0 1 {cx + 60} {cy - ry + 4}" fill="none" stroke="#fff4d0" stroke-width="7" opacity=".85"/>'
    for a0 in (.6, 2.3, 4.1):
        x0 = cx + math.cos(a0) * (rx + 10); y0 = cy + math.sin(a0) * (ry + 10); pts = [(x0, y0)]
        for _ in range(4):
            x0 -= math.cos(a0) * rnd.uniform(10, 24); y0 -= math.sin(a0) * rnd.uniform(10, 24); x0 += rnd.uniform(-8, 8); pts.append((x0, y0))
        b += f'<polyline points="{P(pts)}" fill="none" stroke="#2a1608" stroke-width="3.4"/>'
    for _ in range(16):
        b += rock(rnd.uniform(380, 1040), rnd.uniform(1650, 1760), rnd.uniform(6, 16), rnd, base='#6a5440', hi='#ffd090', sh='#1a1008')
    b += ('<g transform="translate(860 1700) rotate(-12) scale(.8)"><rect x="-150" y="-9" width="230" height="18" rx="8" fill="#8a5a30" stroke="#1a0e06" stroke-width="4"/>'
          '<path d="M60 -38 L118 -30 L118 30 L96 26 L60 18Z" fill="#7a8490" stroke="#1a0e06" stroke-width="4"/><path d="M66 -32 L112 -26" stroke="#e8f0ff" stroke-width="4" opacity=".8"/></g>')
    mx, my, mr = 420, 1440, 108
    b += f'<circle cx="{mx}" cy="{my}" r="{mr + 30}" fill="#bfe8ff" opacity=".18" filter="url(#b26)"/>'
    d += f'<clipPath id="lc"><circle cx="{mx}" cy="{my}" r="{mr}"/></clipPath>'
    zoom = f'<circle cx="{mx}" cy="{my}" r="{mr}" fill="#e8c88a"/>' + tubes(random.Random(7), mx, my, mr, mr, 30, 12, 20, ['#fff2d6', '#f0d098', '#f8e0b0'])
    b += f'<g clip-path="url(#lc)">{zoom}<circle cx="{mx}" cy="{my}" r="{mr}" fill="url(#lens)"/></g>'
    b += f'<path d="M{mx - 76} {my - 46} Q{mx - 58} {my - 82} {mx - 20} {my - 92}" fill="none" stroke="#fff" stroke-width="9" opacity=".75"/>'
    b += f'<circle cx="{mx}" cy="{my}" r="{mr}" fill="none" stroke="#1a1008" stroke-width="22"/><circle cx="{mx}" cy="{my}" r="{mr}" fill="none" stroke="#d8a648" stroke-width="13"/>'
    hx0, hy0, hx1, hy1 = mx - 70, my + 84, mx - 128, my + 214
    b += f'<path d="M{hx0} {hy0} L{hx1} {hy1}" stroke="#1a1008" stroke-width="32" stroke-linecap="round"/><path d="M{hx0} {hy0} L{hx1} {hy1}" stroke="#6a3a1c" stroke-width="22" stroke-linecap="round"/>'
    cap = ('<g transform="translate(6 -96) rotate(-4)"><path d="M-36 6 Q-34 -32 0 -34 Q34 -32 36 6Z" fill="#a8885a" stroke-width="3.4"/>'
           '<path d="M-36 -2 Q0 -12 36 -2 M-30 -16 Q0 -26 30 -16 M-6 -34 L-4 4 M12 -32 L10 4" fill="none" stroke="#6a5030" stroke-width="2.4"/>'
           '<path d="M30 2 Q52 2 58 14 Q40 12 30 8Z M-30 2 Q-52 2 -58 14 Q-40 12 -30 8Z" fill="#8a6a40" stroke-width="3"/>'
           '<circle cx="0" cy="-34" r="5" fill="#8a6a40" stroke-width="2.4"/></g>')
    coat = '<path d="M-34 -24 Q6 -6 44 -24 L40 2 Q6 10 -30 2Z" fill="#8a6a40" stroke-width="3" opacity=".9"/>'
    fx, fy, fs = 170, 1740, 2.3
    ax, ay = (hx1 - fx) / fs - 38, (hy1 - fy) / fs + 22
    b += '<circle cx="170" cy="1640" r="170" fill="#ffe0a8" opacity=".14" filter="url(#b50)"/>'
    b += frog(fx, fy, fs, rot=0, look=(12, -10), mouth='O', shadow=True, mid=coat, top=cap,
              armL='M-34 -22 q-18 6 -20 24', armR=f'M38 -22 q{ax * .6:.0f} {ay * .2:.0f} {ax:.0f} {ay:.0f}')
    b += spark(cx + 180, cy - 260, 22) + spark(980, 1100, 16) + spark(900, 1500, 14) + spark(330, 1330, 18, '#e8f8ff')
    b += dust(rnd, 60, 700, 260, 300, 1600, '#fff0c8')
    b += f'<rect width="{W}" height="{H}" fill="url(#vig)"/>'
    return vpage('#0e2228', vsvg(d, b), [('NOT', 160, 'w'), ('WOOD', 250, 'y'), ('AT ALL', 160, 'w')], outline='#081012', top=470)


# ================= short3 =================
def make_3():
    rnd = random.Random(26)
    d = FILTERS; hz = 1560
    d += lin('sky', [(0, '#1e5e9a'), (.45, '#4f9ac8'), (.8, '#a8d6e4'), (1, '#e8f0d8')])
    d += rad('sun', 150, 260, 800, [(0, '#fffbe8', .9), (.2, '#fff0c0', .4), (1, '#fff0c0', 0)])
    d += lin('gnd', [(0, '#8a7a56'), (.3, '#5e5238'), (1, '#2a2418')])
    d += VIG('#06101a', .6)
    b = f'<rect width="{W}" height="{H}" fill="url(#sky)"/><rect width="{W}" height="{H}" fill="url(#sun)"/>'
    b += '<circle cx="150" cy="260" r="60" fill="#fffef4"/><circle cx="150" cy="260" r="120" fill="#fff4c0" opacity=".6" filter="url(#b26)"/>'
    for _ in range(12):
        x = rnd.uniform(-100, 1100); y = rnd.uniform(220, 1400); w = rnd.uniform(200, 420)
        b += f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{w:.0f}" ry="{w * .1:.0f}" fill="#ffffff" opacity="{rnd.uniform(.25, .5):.2f}" filter="url(#b14)"/>'
        b += f'<ellipse cx="{x - w * .2:.0f}" cy="{y - w * .05:.0f}" rx="{w * .45:.0f}" ry="{w * .09:.0f}" fill="#fff" opacity=".35" filter="url(#b8)"/>'
    b += f'<path d="M0 {hz - 20} Q200 {hz - 54} 420 {hz - 30} T800 {hz - 40} T1080 {hz - 30} L1080 {hz + 20} L0 {hz + 20}Z" fill="#7a9a96" opacity=".7"/>'
    for i, (x, h, w) in enumerate(((150, 160, 12), (980, 200, 15), (330, 90, 7), (860, 80, 6))):
        dd, oo, *_ = pillar(f's3f{i}', x, hz + 2, h, w, w * .85, rnd.uniform(-5, 5), rnd, [(0, '#f0e2c8'), (.4, '#b8a88e'), (1, '#7a6a58')], rim='#fff', detail=.15)
        d += dd; b += f'<g opacity=".7">{oo}</g>'
    b += f'<rect x="0" y="{hz}" width="{W}" height="{H - hz}" fill="url(#gnd)"/>'
    b += moss(0, W, hz + 4, hz + 40, 160, rnd, ['#7a8a3a', '#62722c', '#8e9a44'], 3, 10)
    b += moss(0, W, hz + 40, H, 240, rnd, ['#5a6a2a', '#6a7a32', '#4a5824'], 6, 24, (.4, .8))
    for _ in range(36):
        y = rnd.uniform(hz + 8, 1890); x = rnd.uniform(0, W)
        if 440 < x < 760 and y < 1680: continue
        b += cooksonia(x, y, 8 + (y - hz) * .28, rnd, col='#4e6a26', spc='#e0a848')
    for _ in range(8):
        x = rnd.uniform(60, 900); y = rnd.uniform(hz - 40, hz + 30)
        b += f'<path d="M{x:.0f} {y:.0f} q30 -8 60 0" fill="none" stroke="#fff" stroke-width="3" opacity=".5" stroke-linecap="round"/>'
    b += '<ellipse cx="600" cy="1000" rx="220" ry="640" fill="#fff8e0" opacity=".25" filter="url(#b90)"/>'
    dd, oo, C, Wd, _ = pillar('s3m', 600, 1650, 1150, 130, 112, 40, rnd,
                              [(0, '#fff6dc'), (.08, '#f0dcb4'), (.3, '#ccb490'), (.6, '#9a8468'), (.9, '#665646'), (1, '#463a2e')],
                              rim='#ffffff', rim_side=-1, detail=2.2)
    d += dd; b += oo
    tx, ty = C(1)
    for k in range(10):
        y = ty - 120 + k * 46 + rnd.uniform(-10, 10); x0 = rnd.uniform(tx + 90, tx + 160); L = rnd.uniform(260, 420)
        b += f'<path d="M{x0:.0f} {y:.0f} Q{x0 + L * .5:.0f} {y - 40:.0f} {x0 + L:.0f} {y - 20:.0f}" fill="none" stroke="#ffffff" stroke-width="{rnd.uniform(3, 6):.1f}" opacity="{rnd.uniform(.4, .75):.2f}" stroke-linecap="round"/>'
    b += moss(430, 780, 1630, 1664, 110, rnd, ['#7a8a34', '#62722c', '#8e9a40'], 4, 12)
    for _ in range(12):
        b += cooksonia(rnd.uniform(440, 770), rnd.uniform(1640, 1668), rnd.uniform(16, 32), rnd, col='#4e6a26', spc='#e8a84a')
    sp = ''
    for k in range(5):
        a0 = -.2 - k * .1
        for i in range(70):
            t = i / 70; L = 70 + t * 620
            x = tx + 40 + math.cos(a0) * L + rnd.gauss(0, 12 + t * 50); y = ty - 30 + math.sin(a0) * L - t * t * 120 + rnd.gauss(0, 10 + t * 40)
            if x > 1070 or y < 150: continue
            r = rnd.choice([2.6, 3.4, 4.6, 6]) * (1.2 - t * .5)
            sp += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r:.1f}" fill="{rnd.choice(["#fff3c0", "#f2d27a", "#ffe8a0"])}" opacity="{rnd.uniform(.6, 1) * (1 - t * .45):.2f}"/>'
    b += f'<g filter="url(#b4)" opacity=".6">{sp}</g>{sp}'
    b += f'<ellipse cx="{tx + 150:.0f}" cy="{ty - 70:.0f}" rx="190" ry="70" fill="#fff2c0" opacity=".35" filter="url(#b26)" transform="rotate(-20 {tx + 150:.0f} {ty - 70:.0f})"/>'
    gog = ('<path d="M-34 -96 Q6 -108 48 -96" fill="none" stroke="#5a3a20" stroke-width="6"/>'
           '<g fill="#9ad8f0" stroke-width="3.4"><ellipse cx="-6" cy="-100" rx="13" ry="10"/><ellipse cx="22" cy="-100" rx="13" ry="10"/></g>'
           '<path d="M-10 -104 l6 -3 M18 -104 l6 -3" stroke="#fff" stroke-width="3"/>')
    scarf = ('<path d="M-30 -24 Q6 -10 42 -24 L42 -12 Q6 2 -30 -12Z" fill="#e0503a" stroke-width="3"/>'
             '<path d="M40 -20 Q80 -34 120 -24 Q100 -12 130 -2 Q90 2 44 -10Z" fill="#e0503a" stroke-width="3"/>')
    b += frog(tx - 6, ty + 12, 2.2, rot=-4, look=(12, -8), mouth='O', top=gog, mid=scarf,
              armL='M-34 -22 q-22 6 -28 30', armR='M38 -22 q30 -18 44 -54')
    b += spark(tx + 300, ty - 140, 26, '#fffbe6') + spark(980, 330, 18) + spark(120, 900, 14) + spark(940, 1300, 14)
    b += f'<rect width="{W}" height="{H}" fill="url(#vig)"/>'
    return vpage('#1e5e9a', vsvg(d, b), [('WHY BUILD', 150, 'w'), ('A', 120, 'w'), ('TOWER?', 260, 'y')], outline='#0a1626', top=760)


# ================= short4 =================
def make_4():
    rnd = random.Random(404)
    d = FILTERS; hz = 1520
    d += lin('sky', [(0, '#b8642a'), (.5, '#e8a850'), (1, '#f8dc98')])
    d += rad('sun', 170, 240, 1000, [(0, '#fffbe6', 1), (.12, '#fff0b0', .7), (.4, '#ffd070', .25), (1, '#ffd070', 0)])
    d += lin('gnd', [(0, '#c0884a'), (.3, '#8a5a30'), (1, '#3a2414')])
    d += rad('cave', 1250, 760, 260, [(0, '#ffc870', .9), (.5, '#c87a3a', .45), (1, '#4a2a14', 0)])
    d += VIG('#1a0a04', .7)
    b = f'<rect width="{W}" height="{H}" fill="url(#sky)"/><rect width="{W}" height="{H}" fill="url(#sun)"/>'
    for k in range(16):
        a = .2 + k * .09
        b += f'<path d="M170 240 L{170 + math.cos(a - .015) * 2400:.0f} {240 + math.sin(a - .015) * 2400:.0f} L{170 + math.cos(a + .015) * 2400:.0f} {240 + math.sin(a + .015) * 2400:.0f}Z" fill="#fff6d0" opacity=".08"/>'
    b += '<circle cx="170" cy="240" r="70" fill="#fffef4"/><circle cx="170" cy="240" r="140" fill="#fff4c0" opacity=".6" filter="url(#b26)"/>'
    b += f'<path d="M0 {hz - 20} L180 {hz - 42} L300 {hz - 30} L520 {hz - 50} L760 {hz - 28} L1080 {hz - 40} L1080 {hz + 20} L0 {hz + 20}Z" fill="#c89060" opacity=".7"/>'
    for i, (x, h, w) in enumerate(((120, 130, 10), (1010, 190, 15), (180, 80, 7))):
        dd, oo, *_ = pillar(f's4f{i}', x, hz + 2, h, w, w * .85, rnd.uniform(-5, 5), rnd, [(0, '#fff0c8'), (.4, '#c8a47a'), (1, '#7a5a3e')], rim='#fff4c8', detail=.15)
        d += dd; b += f'<g opacity=".7">{oo}</g>'
    b += f'<rect x="0" y="{hz}" width="{W}" height="{H - hz}" fill="url(#gnd)"/>'
    for _ in range(34):
        y = rnd.uniform(hz + 10, 1890); sc = ((y - hz) / (H - hz)) ** 1.3; x = rnd.uniform(0, W)
        if 30 < x < 300 and 1540 < y < 1800: continue
        b += rock(x, y, 3 + sc * rnd.uniform(10, 28), rnd, base='#8a5a34', hi='#ffd890', sh='#2a160a')
    for _ in range(16):
        y = rnd.uniform(hz + 10, 1880); x = rnd.choice([rnd.uniform(0, 250), rnd.uniform(950, 1080)])
        b += cooksonia(x, y, 8 + (y - hz) * .16, rnd, col='#5a6a2a', spc='#e8a040')
    b += f'<path d="M900 1680 L1080 1690 L1080 1760 L920 1760Z" fill="#2a1a2a" opacity=".45" filter="url(#b14)"/>'
    yb = 1680
    dd, oo, C, Wd, _ = pillar('s4m', 600, yb, 1950, 330, 280, -30, rnd,
                              [(0, '#fff4d8'), (.06, '#f6dcae'), (.25, '#dcbc8c'), (.55, '#b0906a'), (.85, '#7a6248'), (1, '#4a3a2c')],
                              rim='#fffbe6', rim_side=-1, detail=3.0)
    d += dd; b += oo
    cut = 'M1090 600 Q1120 560 1250 556 Q1390 560 1420 610 L1436 880 Q1400 960 1260 966 Q1110 962 1080 880Z'
    d += f'<clipPath id="cw"><path d="{cut}"/></clipPath>'
    inner = '<rect x="1060" y="540" width="400" height="440" fill="#f0d6a6"/>'
    for _ in range(90):
        x = rnd.uniform(1070, 1450); y0 = rnd.uniform(540, 940); pts = [(x, y0)]
        for k in range(6):
            x += rnd.uniform(-6, 6); pts.append((x, y0 + (k + 1) * 9))
        inner += f'<polyline points="{P(pts)}" fill="none" stroke="{rnd.choice(["#b89060", "#fff2d6", "#c8a070"])}" stroke-width="{rnd.uniform(1.5, 3.5):.1f}" opacity=".6"/>'
    inner += '<rect x="1060" y="540" width="400" height="440" fill="url(#cave)" opacity=".55"/>'
    ch = [(1150, 650, 46, 32), (1330, 640, 58, 38), (1380, 790, 46, 32), (1250, 870, 70, 42), (1130, 800, 38, 28), (1260, 740, 34, 24)]
    links = [(0, 5), (5, 1), (1, 2), (5, 3), (2, 3), (0, 4), (4, 3)]
    tun = []
    for i, j in links:
        (x0, y0, *_), (x3, y3, *_) = ch[i], ch[j]
        tun.append(f'M{x0} {y0} C{x0 + rnd.uniform(-60, 60):.0f} {y0 + rnd.uniform(-40, 60):.0f} {x3 + rnd.uniform(-60, 60):.0f} {y3 + rnd.uniform(-60, 40):.0f} {x3} {y3}')
    for (x0, y0, *_) in ch[:5]:
        a = rnd.uniform(0, 6.28); L = rnd.uniform(50, 90)
        tun.append(f'M{x0} {y0} q{math.cos(a) * L * .6 + rnd.uniform(-20, 20):.0f} {math.sin(a) * L * .6:.0f} {math.cos(a) * L:.0f} {math.sin(a) * L:.0f}')
    for w, c, op in ((30, '#fff0c8', .7), (22, '#3a1e0c', 1), (11, '#6a3a1a', .7)):
        for t_ in tun:
            inner += f'<path d="{t_}" fill="none" stroke="{c}" stroke-width="{w}" opacity="{op}" stroke-linecap="round"/>'
    for (x, y, rx_, ry_) in ch:
        inner += f'<ellipse cx="{x}" cy="{y}" rx="{rx_ + 8}" ry="{ry_ + 8}" fill="#fff0c8" opacity=".6"/><ellipse cx="{x}" cy="{y}" rx="{rx_}" ry="{ry_}" fill="#4a240e" stroke="#2a1206" stroke-width="3"/>'
        inner += f'<ellipse cx="{x}" cy="{y}" rx="{rx_ * .8:.0f}" ry="{ry_ * .7:.0f}" fill="#ffb860" opacity=".35" filter="url(#b8)"/>'
    inner += millipede(1196, 874, .62, -2, rnd, col='#6a3a1e', hi='#e09858')
    inner += '<path d="M1300 872 l10 -6 l-2 10 z M1306 862 l6 4" fill="#e8d0a0" stroke="#3a2010" stroke-width="1.4"/>'
    inner += springtail(1320, 652, 2.0) + springtail(1384, 800, 1.7, -1)
    inner += trigono(1150, 660, 1.6)
    inner += f'<path d="{cut}" fill="none" stroke="#2a1408" stroke-width="30" opacity=".45" filter="url(#b8)"/>'
    sc, wx, wy = 1.32, 610, 1390
    b += f'<ellipse cx="{wx}" cy="{wy}" rx="290" ry="320" fill="#ffd890" opacity=".3" filter="url(#b26)"/>'
    b += (f'<g transform="translate({wx} {wy}) scale({sc}) translate(-1258 -761)"><g clip-path="url(#cw)">{inner}</g>'
          f'<path d="{cut}" fill="none" stroke="#2a1608" stroke-width="7"/><path d="{cut}" fill="none" stroke="#fff2d0" stroke-width="3" opacity=".8" transform="translate(-4 -4)"/></g>')
    b += f'<ellipse cx="900" cy="1500" rx="16" ry="22" fill="#1a0c06" stroke="#3a2412" stroke-width="3"/>'
    b += millipede(930, 1690, .9, -96, rnd, col='#5a3420', hi='#d08a52')
    b += springtail(1010, 1730, 1.8, -1)
    b += moss(300, 960, 1660, 1700, 140, rnd, ['#7a8434', '#62702c', '#8e9a40'], 4, 12)
    for _ in range(12):
        b += cooksonia(rnd.uniform(300, 900), rnd.uniform(1668, 1700), rnd.uniform(16, 32), rnd, col='#4e6226', spc='#e8a84a')
    bib = ('<path d="M-22 -30 Q6 -22 34 -30 L30 2 Q6 10 -18 2Z" fill="#fff8f0" stroke-width="3"/>'
           '<path d="M-14 -20 L26 -20 M-12 -8 L24 -8" stroke="#e05a4a" stroke-width="3"/>')
    fork = ('<g transform="translate(72 -86) rotate(14)"><rect x="-3" y="0" width="6" height="56" rx="3" fill="#cfd6e0" stroke-width="2.4"/>'
            '<path d="M-10 0 L-10 -24 M-3 0 L-3 -26 M3 0 L3 -26 M10 0 L10 -24 M-10 0 Q0 8 10 0" fill="none" stroke="#cfd6e0" stroke-width="3.4"/></g>')
    b += '<circle cx="150" cy="1660" r="160" fill="#fff0c0" opacity=".22" filter="url(#b50)"/>'
    b += frog(150, 1770, 2.0, rot=3, look=(14, -10), mouth='O', shadow=True, mid=bib,
              armL='M-34 -22 q-18 6 -20 24', armR='M38 -22 q22 -10 34 -34', front=fork)
    b += spark(wx - 60, wy - 150, 18) + spark(wx + 160, wy - 220, 14) + spark(980, 520, 16) + spark(420, 380, 20)
    b += dust(rnd, 40, 600, 260, 200, 1700, '#fff4d0')
    b += f'<rect width="{W}" height="{H}" fill="url(#vig)"/>'
    return vpage('#b8642a', vsvg(d, b), [('A HOME', 170, 'w'), ('AND A', 130, 'w'), ('MEAL?', 250, 'y')], outline='#1a0c04', top=560)


# ================= short5 =================
def crown(x, y, s, rot):
    return (f'<g transform="translate({x} {y}) rotate({rot}) scale({s})" stroke="#3a2406" stroke-width="3.4" stroke-linejoin="round">'
            '<path d="M-40 16 L-46 -26 L-24 -6 L0 -36 L24 -6 L46 -26 L40 16Z" fill="#f2c23a"/>'
            '<path d="M-40 16 L40 16 L40 26 L-40 26Z" fill="#e0a82a"/>'
            '<path d="M-36 8 L-40 -16 M-18 -2 L0 -26" fill="none" stroke="#fff4b0" stroke-width="4"/>'
            '<circle cx="0" cy="8" r="6" fill="#e04a5a"/><circle cx="-24" cy="10" r="4.5" fill="#4ab0e0"/><circle cx="24" cy="10" r="4.5" fill="#4ab0e0"/>'
            '<circle cx="-46" cy="-28" r="4" fill="#fff0a0"/><circle cx="0" cy="-38" r="4" fill="#fff0a0"/><circle cx="46" cy="-28" r="4" fill="#fff0a0"/></g>')


def make_5():
    rnd = random.Random(30)
    d = FILTERS; hz = 1600
    d += lin('sky', [(0, '#1e3a24'), (.5, '#3e6a3e'), (1, '#9ab878')])
    d += rad('sun', 960, 220, 1000, [(0, '#fffbd8', .9), (.18, '#f2e098', .45), (1, '#f2e098', 0)])
    d += lin('gnd', [(0, '#4a5a2a'), (.3, '#33401e'), (1, '#121808')])
    d += lin('trunk', [(0, '#2a1a0e'), (.3, '#6a4a2a'), (.55, '#8a6238'), (.8, '#4a321c'), (1, '#20140a')], x2=1, y2=0)
    d += VIG('#040a04', .75)
    b = f'<rect width="{W}" height="{H}" fill="url(#sky)"/><rect width="{W}" height="{H}" fill="url(#sun)"/>'
    for k in range(10):
        x = rnd.uniform(0, W); h = rnd.uniform(700, 1300); w = rnd.uniform(10, 18)
        b += f'<path d="M{x:.0f} {hz} L{x + 4:.0f} {hz - h:.0f}" stroke="#2e4a30" stroke-width="{w:.0f}" opacity=".55"/>'
        for j in range(7):
            yy = hz - h + j * h * .08
            b += f'<ellipse cx="{x + 4:.0f}" cy="{yy:.0f}" rx="{60 + j * 14:.0f}" ry="{18 + j * 3:.0f}" fill="#36603e" opacity=".45" filter="url(#b4)"/>'
    for k in range(5):
        x = 900 + k * 110
        b += f'<path d="M{x} -20 L{x + 60} -20 L{x - 520} {hz} L{x - 640} {hz}Z" fill="#fff8c8" opacity=".07"/>'
    b += f'<rect x="0" y="{hz}" width="{W}" height="{H - hz}" fill="url(#gnd)"/>'
    b += moss(0, W, hz + 4, hz + 40, 180, rnd, ['#5a7a2a', '#4a6a24', '#6e8a34'], 3, 10)
    b += moss(0, W, hz + 40, H, 240, rnd, ['#3e5a20', '#4e6a28', '#2e4818'], 6, 24, (.4, .85))
    tx = 800
    trunk = f'M{tx - 120} {hz + 70} Q{tx - 80} 900 {tx - 56} -20 L{tx + 56} -20 Q{tx + 80} 900 {tx + 130} {hz + 70}Z'
    for (ang, L, w) in ((2.8, 260, 36), (2.4, 200, 30), (.5, 180, 30), (.25, 170, 24), (1.6, 120, 26)):
        x0 = tx + math.cos(ang) * 60; y0 = hz + 50; pts = [(x0, y0)]; a = ang
        for s in range(5):
            a += rnd.uniform(-.15, .15); pts.append((pts[-1][0] + math.cos(a) * L / 5, pts[-1][1] + math.sin(a) * L / 5 * .35 + 3))
        pts = [(min(max(px, 560), 1070), py) for px, py in pts]
        b += f'<polyline points="{P(pts)}" fill="none" stroke="#1a0e06" stroke-width="{w + 7}" stroke-linecap="round"/><polyline points="{P(pts)}" fill="none" stroke="#6a4a2a" stroke-width="{w}" stroke-linecap="round"/>'
    b += f'<path d="{trunk}" fill="url(#trunk)" stroke="#120a04" stroke-width="5"/>'
    for _ in range(50):
        y0 = rnd.uniform(0, hz + 40); x0 = tx + rnd.uniform(-70, 70)
        b += f'<path d="M{x0:.0f} {y0:.0f} q{rnd.uniform(-6, 6):.0f} {rnd.uniform(30, 90):.0f} {rnd.uniform(-4, 4):.0f} {rnd.uniform(60, 160):.0f}" fill="none" stroke="{rnd.choice(["#1a0e06", "#a07848"])}" stroke-width="{rnd.uniform(2, 5):.1f}" opacity=".5"/>'
    b += f'<path d="M{tx - 44} -20 Q{tx - 70} 900 {tx - 110} {hz + 60}" fill="none" stroke="#ffe8a0" stroke-width="7" opacity=".6"/>'
    for k in range(13):
        y = 30 + k * 46; L = 220 + k * 20 + rnd.uniform(-30, 30)
        for side, base in ((1, -12), (-1, 192)):
            ang = base + side * rnd.uniform(-8, 10) + side * k * 1.2
            b += frond(tx + side * 30, y, L, ang, rnd, '#3e7a34', '#78b04a', lw=5)
    for _ in range(30):
        b += f'<ellipse cx="{rnd.uniform(200, 1080):.0f}" cy="{rnd.uniform(0, 640):.0f}" rx="{rnd.uniform(40, 90):.0f}" ry="{rnd.uniform(10, 22):.0f}" fill="#c8f080" opacity="{rnd.uniform(.08, .2):.2f}" filter="url(#b8)"/>'
    px = 380
    b += f'<ellipse cx="{px}" cy="1500" rx="120" ry="180" fill="#fff0b0" opacity=".14" filter="url(#b50)"/>'
    dd, oo, C, Wd, _ = pillar('s5p', px, hz + 60, 290, 54, 44, 8, rnd,
                              [(0, '#d8d0b0'), (.25, '#a8a088'), (.6, '#7a7262'), (1, '#4a4438')], rim='#e8f0b0', rim_side=1, detail=1.2, cap=.6)
    d += dd; b += oo
    cx_, cy_ = C(1)
    b += f'<path d="M{cx_ - 30:.0f} {cy_ + 10:.0f} l14 22 l-8 18 l14 26 M{cx_ + 20:.0f} {cy_ + 6:.0f} l-10 20 l8 16" fill="none" stroke="#1e1a12" stroke-width="3.4"/>'
    for k in range(6):
        b += rock(cx_ + rnd.uniform(-80, 80), hz + 64 + rnd.uniform(-6, 10), rnd.uniform(5, 12), rnd, base='#8a8270', hi='#e8e0c0', sh='#2a261c')
    kx, ky = cx_ - 170, cy_ - 30
    b += f'<path d="M{cx_ - 10:.0f} {cy_ - 30:.0f} Q{cx_ - 60:.0f} {cy_ - 110:.0f} {kx + 40:.0f} {ky - 40:.0f}" fill="none" stroke="#fff4c0" stroke-width="5" stroke-dasharray="12 12" opacity=".8"/>'
    b += f'<circle cx="{kx:.0f}" cy="{ky:.0f}" r="90" fill="#ffe080" opacity=".35" filter="url(#b26)"/>'
    b += crown(kx, ky, 1.9, -34)
    b += spark(kx - 60, ky - 50, 18, '#fff8c0') + spark(kx + 70, ky + 30, 12, '#fff8c0')
    leaf = ('<g transform="translate(4 -100) rotate(-10)"><path d="M-40 6 Q-10 -40 40 -10 Q10 18 -40 6Z" fill="#7ab84a" stroke-width="3.2"/>'
            '<path d="M-36 4 Q0 -10 34 -10" fill="none" stroke="#3a6a24" stroke-width="2.4"/></g>')
    b += '<circle cx="170" cy="1640" r="160" fill="#e8ffc0" opacity=".16" filter="url(#b50)"/>'
    b += frog(170, 1730, 2.2, rot=4, look=(4, -14), mouth='O', shadow=True, top=leaf,
              armL='M-34 -22 q-24 -10 -30 -42', armR='M38 -22 q24 -14 30 -46')
    for _ in range(50):
        b += f'<circle cx="{rnd.uniform(0, 1080):.0f}" cy="{rnd.uniform(200, 1560):.0f}" r="{rnd.choice([1.4, 2, 2.8])}" fill="#fff8d0" opacity="{rnd.uniform(.2, .7):.2f}"/>'
    b += spark(960, 220, 30, '#fffbe6') + spark(1000, 1300, 16)
    b += f'<rect width="{W}" height="{H}" fill="url(#vig)"/>'
    return vpage('#1e3a24', vsvg(d, b), [('OUTGROWN', 165, 'y'), ('BY', 125, 'w'), ('TREES', 240, 'w')], outline='#081008', top=690)


for n, fn in ((1, make_1), (2, make_2), (3, make_3), (4, make_4), (5, make_5)):
    out = os.path.join(VID, f'giant-mold-short{n}', 'thumb'); os.makedirs(out, exist_ok=True)
    for f in ('common.css', 'Fredoka-700.woff2'):
        shutil.copyfile(os.path.join(TOOLS, 'assets', 'thumb_v', f), os.path.join(out, f))
    open(os.path.join(out, 'A.html'), 'w').write(fn())
print('ok')
