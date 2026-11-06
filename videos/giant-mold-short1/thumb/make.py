# One thumbnail (A) for each of the five giant-mold shorts (guideline 16-6 / 16-8, brief tools/briefs/thumb_art.md).
# Run: python3 videos/giant-mold-short1/thumb/make.py  -> videos/giant-mold-short{1..5}/thumb/A.html (+ common.css, Fredoka-700.woff2)
# Reuses the pillar / frog / small-life helpers of videos/giant-mold/thumb/make.py (executed up to its first thumbnail, no side effects).
# short1 EARTH / LOOKED / ALIEN      dusk valley full of pale pillars of many heights, big moon, river; tourist frog with camera.
#                                     Script S02 "our planet looked completely alien", S04 ankle-high plants, S07 pillars.
# short2 NOT / WOOD / AT ALL          polished cut end of a fossil log showing woven tubes (no rings); detective frog with magnifier.
#                                     Script: "only to find it was never made of wood at all", "millions of tightly interwoven tubes".
# short3 WHY BUILD / A / TOWER?       bright windy sky, frog with goggles on top of a pillar, spores streaming away on fast high wind.
#                                     Script: "Why would a fungus invest so much energy into building a tower"; spore dispersal = ONE hypothesis.
# short4 A HOME / AND A / MEAL?       cut-away of the pillar base with tunnels and chambers, millipede, springtails, spider relative; bib frog.
#                                     Script: "If that is right, the giant was both a home and a meal." (hedged -> question mark)
# short5 OUTGROWN / BY / TREES        a huge Archaeopteris towering over a small cracked pillar whose gold crown is falling; frog catching it.
#                                     Script: Archaeopteris ~30 m, nearly four times the tallest Prototaxites; pillars vanished by the Late Devonian.
import os, sys, math, random, shutil
HERE = os.path.dirname(os.path.abspath(__file__))
VID = os.path.abspath(os.path.join(HERE, '..', '..'))
SRC = os.path.join(VID, 'giant-mold', 'thumb', 'make.py')
_s = open(SRC).read()
G = {'__file__': SRC, '__name__': 'giantmold_helpers'}
exec(_s.split('# ================= A:')[0], G)
_f = _s[_s.index('def frond('):_s.index('def make_C(')]
exec(_f, G)
pillar, frog, cooksonia, millipede, springtail, trigono, moss, rock, frond, P, limb = (G[k] for k in (
    'pillar', 'frog', 'cooksonia', 'millipede', 'springtail', 'trigono', 'moss', 'rock', 'frond', 'P', 'limb'))
INK, GREEN = G['INK'], G['GREEN']
FILTERS = G['FILTERS']
sys.path.insert(0, os.path.join(VID, '..', 'tools'))
from thumb_lib import page, svg, lin, rad, spark

CORNER = '<mask id="cor" maskUnits="userSpaceOnUse" x="0" y="0" width="1920" height="1080"><rect width="1920" height="1080" fill="#fff"/><rect x="1590" y="890" width="500" height="300" rx="60" fill="#000" filter="url(#b26)"/></mask>'


def dust(rnd, n, cx, sx, y0, y1, col='#fff0c8'):
    return ''.join(f'<circle cx="{rnd.gauss(cx, sx):.0f}" cy="{rnd.uniform(y0, y1):.0f}" r="{rnd.choice([1.4, 2, 2.8])}" fill="{col}" opacity="{rnd.uniform(.2, .7):.2f}"/>' for _ in range(n))


# ================= short1: alien dusk valley of pillars =================
def make_1():
    rnd = random.Random(401)
    d = FILTERS + CORNER
    hz = 742
    d += lin('sky', [(0, '#16183a'), (.35, '#35356a'), (.65, '#7a5a8e'), (.86, '#d88a86'), (1, '#ffc590')])
    d += rad('glow', 1500, 742, 900, [(0, '#ffd8a0', .8), (.2, '#ff9f80', .35), (.6, '#a06090', .08), (1, '#000', 0)])
    d += lin('gnd', [(0, '#3a3a52'), (.25, '#26303a'), (1, '#0c1014')])
    d += lin('riv', [(0, '#ffc8a0'), (.4, '#a07aa0'), (1, '#3a3a6a')])
    d += rad('vig', 960, 540, 1150, [(0, '#000', 0), (.6, '#000', 0), (1, '#06050e', .75)])
    b = '<rect width="1920" height="1080" fill="url(#sky)"/><rect width="1920" height="1080" fill="url(#glow)"/>'
    for _ in range(140):
        y = rnd.uniform(10, 520)
        b += f'<circle cx="{rnd.uniform(0, 1920):.0f}" cy="{y:.0f}" r="{rnd.choice([1, 1.5, 2.2])}" fill="#eef" opacity="{rnd.uniform(.2, .8) * (1 - y / 700):.2f}"/>'
    # big pale moon with craters
    b += '<circle cx="1560" cy="250" r="230" fill="#ffe8d8" opacity=".25" filter="url(#b50)"/>'
    b += '<circle cx="1560" cy="250" r="128" fill="#f6e6e4"/>'
    for cx, cy, r in ((1520, 220, 22), (1600, 290, 16), (1590, 210, 10), (1500, 300, 12), (1640, 240, 9)):
        b += f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="#d8c4cc" opacity=".8"/><circle cx="{cx + 2}" cy="{cy + 2}" r="{r * .7:.0f}" fill="#c8b0bc" opacity=".6"/>'
    b += '<path d="M1460 190 a128 128 0 0 0 40 170" fill="none" stroke="#fff" stroke-width="5" opacity=".6"/>'
    # thin glowing clouds
    for _ in range(7):
        b += f'<ellipse cx="{rnd.uniform(0, 1920):.0f}" cy="{rnd.uniform(380, 660):.0f}" rx="{rnd.uniform(200, 420):.0f}" ry="{rnd.uniform(6, 14):.0f}" fill="#ffc0a8" opacity="{rnd.uniform(.15, .35):.2f}" filter="url(#b8)"/>'
    # far mesas
    b += '<path d="M0 730 L90 690 L210 694 L240 716 L520 720 L560 690 L700 686 L740 712 L1100 718 L1180 680 L1330 676 L1370 708 L1920 712 L1920 760 L0 760Z" fill="#5a4a78" opacity=".85"/>'
    b += '<path d="M0 748 Q400 728 800 744 T1920 740 L1920 770 L0 770Z" fill="#46405e"/>'
    b += f'<rect x="0" y="{hz}" width="1920" height="{1080 - hz}" fill="url(#gnd)"/>'
    # winding river reflecting the dusk
    b += '<path d="M1460 744 Q1380 770 1260 790 Q1040 830 1000 880 Q960 940 700 990 Q560 1020 420 1080 L660 1080 Q760 1030 1000 990 Q1180 940 1220 880 Q1260 830 1430 790 Q1500 770 1520 744Z" fill="url(#riv)" opacity=".9"/>'
    b += '<path d="M1300 790 Q1150 820 1100 860 M1080 900 Q980 950 820 980" fill="none" stroke="#fff0e0" stroke-width="3" opacity=".6"/>'
    # glowing teal-green carpets of tiny plants
    b += moss(0, 1920, hz + 6, hz + 50, 260, rnd, ['#3a6a5a', '#4a7a62', '#2e5a4c'], 3, 10)
    b += moss(0, 1600, hz + 50, 1080, 360, rnd, ['#2a5a4a', '#3c6e58', '#22483c', '#4e8a6a'], 6, 26, (.35, .8))
    # pillars of many heights receding along the valley (far to near)
    pil = [(1840, hz + 6, 110, 10), (1100, hz + 4, 90, 8), (1300, hz + 8, 150, 13), (1720, hz + 14, 210, 18), (960, hz + 10, 130, 11),
           (1520, hz + 30, 330, 30), (880, hz + 60, 260, 24)]
    for i, (x, yb, h, w) in enumerate(pil):
        dd, oo, *_ = pillar(f's1f{i}', x, yb, h, w, w * .85, rnd.uniform(-8, 8), rnd,
                            [(0, '#4a4262'), (.45, '#8a7e98'), (.85, '#d0b8b8'), (1, '#ffd0a8')], rim='#ffc8a0', rim_side=1,
                            detail=.25 + h / 600, tex_dark='#2a2238', tex_light='#ffe8e0')
        d += dd; b += f'<g opacity="{.65 + h / 900:.2f}">{oo}</g>'
    # main pillar (closest, biggest)
    b += '<ellipse cx="1200" cy="520" rx="220" ry="440" fill="#ffc8a8" opacity=".18" filter="url(#b90)"/>'
    dd, oo, C, W, _ = pillar('s1m', 1190, 930, 760, 104, 86, -26, rnd,
                             [(0, '#3e3654'), (.3, '#6e6480'), (.62, '#a898a8'), (.86, '#e6c8bc'), (1, '#ffd8b0')],
                             rim='#ffd0a8', rim_side=1, detail=1.4, tex_dark='#241c30', tex_light='#ffeee6')
    d += dd; b += oo
    b += f'<polyline points="{P([(C(i / 70)[0] - W[i], C(i / 70)[1]) for i in range(4, 71)])}" fill="none" stroke="#b8a8ff" stroke-width="3" opacity=".55"/>'
    b += moss(1060, 1330, 914, 942, 120, rnd, ['#4a8a6a', '#5a9a78', '#3a7058'], 4, 11)
    for _ in range(14):
        b += cooksonia(rnd.uniform(1060, 1330), rnd.uniform(924, 948), rnd.uniform(16, 30), rnd, col='#3e7a5a', spc='#ffc070')
    # ankle-high plants in the foreground
    for _ in range(46):
        y = rnd.uniform(hz + 10, 1070); sc = (y - hz) / (1080 - hz); x = rnd.uniform(0, 1580)
        if 380 < x < 700 and y > 860: continue
        b += cooksonia(x, y, 8 + sc * 66, rnd, col='#3a7458', spc='#ffbc6a')
    for _ in range(28):
        y = rnd.uniform(hz + 20, 1060); sc = ((y - hz) / (1080 - hz)) ** 1.3; x = rnd.uniform(0, 1560)
        b += rock(x, y, 3 + sc * rnd.uniform(10, 26), rnd, base='#3a3a50', hi='#ffc0a0', sh='#14121e')
    b += millipede(1240, 940, .5, 180, rnd, col='#4a3040', hi='#d88a9a')
    b += spark(1560, 250, 34, '#fff6f0') + spark(1240, 120, 18) + spark(700, 640, 14) + spark(1400, 560, 16)
    # tourist frog with bucket hat and camera, bottom left
    hat = ('<g transform="translate(6 -95) rotate(-6)"><path d="M-30 4 Q-28 -30 0 -32 Q28 -30 30 4Z" fill="#e8b84a" stroke-width="3.4"/>'
           '<path d="M-50 6 Q0 -8 50 6 Q46 18 0 14 Q-46 18 -50 6Z" fill="#d8a43a" stroke-width="3.2"/><path d="M-28 -4 Q0 -10 28 -4" fill="none" stroke="#c0503a" stroke-width="5"/></g>')
    strap = '<path d="M-30 -38 Q6 0 44 -38" fill="none" stroke="#3a2a1a" stroke-width="3"/>'
    cam = ('<g transform="translate(64 -62) rotate(-14)"><rect x="-26" y="-18" width="52" height="36" rx="6" fill="#2a2a34" stroke-width="3"/>'
           '<rect x="-14" y="-26" width="18" height="10" rx="3" fill="#3a3a44" stroke-width="2.4"/><circle cx="2" cy="0" r="12" fill="#5a6a8a" stroke-width="3"/>'
           '<circle cx="-1" cy="-3" r="4" fill="#cfe0ff" stroke="none"/><circle cx="18" cy="-11" r="3" fill="#ffe08a" stroke="none"/></g>')
    b += '<circle cx="520" cy="920" r="170" fill="#ffd0b0" opacity=".16" filter="url(#b50)"/>'
    b += frog(520, 1022, 2.35, rot=2, look=(10, -9), mouth='O', shadow=True, mid=strap, top=hat,
              armL='M-34 -22 q-18 6 -20 24', armR='M38 -22 q16 -6 24 -36', front=cam)
    b += f'<g opacity=".9">{dust(rnd, 50, 1300, 320, 100, 900, "#ffe8e0")}</g>'
    b += '<rect width="1920" height="1080" fill="url(#vig)"/>'
    lines = [('EARTH', 160, 'w'), ('LOOKED', 160, 'w'), ('ALIEN', 250, 'y')]
    return page('#16183a', svg(d, b), lines, outline='#0c0a1a', top=36)


# ================= short2: fossil log cut open, woven tubes, detective frog =================
def tubes(rnd, cx, cy, rx, ry, n, wmin, wmax, cols, glow=None):
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
    d = FILTERS + CORNER
    d += lin('bg', [(0, '#0e2228'), (.6, '#16343a'), (1, '#0a1416')])
    d += rad('spot', 1260, 560, 820, [(0, '#ffe6b0', .55), (.35, '#f2b860', .18), (1, '#000', 0)])
    d += lin('bark', [(0, '#3a2e24'), (.35, '#6a5644'), (.6, '#8a7458'), (1, '#2a2018')])
    d += rad('face', 1220, 560, 360, [(0, '#f8dca0', 1), (.55, '#d8a868', 1), (.9, '#a8783e', 1), (1, '#6a4826', 1)])
    d += rad('lens', 900, 800, 150, [(0, '#fff6dc', .12), (.8, '#bfe8ff', .08), (1, '#bfe8ff', .3)])
    d += lin('tbl', [(0, '#4a3422'), (.2, '#2e2016'), (1, '#120c08')])
    d += rad('vig', 960, 540, 1150, [(0, '#000', 0), (.58, '#000', 0), (1, '#040808', .8)])
    b = '<rect width="1920" height="1080" fill="url(#bg)"/>'
    # cliff strata behind (Canadian shore cliff, soft)
    for k in range(9):
        y = 120 + k * 80 + rnd.uniform(-15, 15)
        b += f'<path d="M0 {y:.0f} Q500 {y + rnd.uniform(-30, 30):.0f} 1000 {y:.0f} T1920 {y + rnd.uniform(-20, 20):.0f}" fill="none" stroke="#2a4a50" stroke-width="{rnd.uniform(6, 18):.0f}" opacity=".35"/>'
    b += '<rect width="1920" height="1080" fill="url(#spot)"/>'
    # light cone from the top right
    b += '<path d="M1500 -20 L1760 -20 L1640 980 L860 980Z" fill="#fff0c8" opacity=".07"/>'
    # table / rock shelf
    b += '<path d="M0 880 Q900 850 1920 870 L1920 1080 L0 1080Z" fill="url(#tbl)"/>'
    b += '<path d="M0 880 Q900 850 1920 870" fill="none" stroke="#c8925a" stroke-width="4" opacity=".55"/>'
    # log body receding to the upper right (perspective), then the cut face facing the viewer
    cx, cy, rx, ry = 1220, 560, 300, 330
    body = f'M{cx - 40} {cy - ry + 6} L1800 230 Q1880 330 1860 470 L{cx + 60} {cy + ry - 2}Z'
    b += f'<ellipse cx="1500" cy="880" rx="520" ry="40" fill="#000" opacity=".55" filter="url(#b26)"/>'
    b += f'<path d="{body}" fill="url(#bark)" stroke="#120c08" stroke-width="5"/>'
    for k in range(16):
        t = k / 15; y0 = cy - ry + 30 + t * (2 * ry - 60); y1 = 250 + t * 210
        b += f'<path d="M{cx + 60:.0f} {y0:.0f} Q1500 {(y0 + y1) / 2 + rnd.uniform(-20, 20):.0f} 1840 {y1:.0f}" fill="none" stroke="{rnd.choice(["#2a2018", "#a8906c", "#4a3a2a"])}" stroke-width="{rnd.uniform(2, 6):.1f}" opacity=".5"/>'
    for _ in range(26):
        x = rnd.uniform(1350, 1800); y = rnd.uniform(260, 820) - (x - 1300) * .25
        b += f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{rnd.uniform(8, 26):.0f}" ry="{rnd.uniform(4, 10):.0f}" fill="{rnd.choice(["#b8a07a", "#6a7458", "#c8b48a"])}" opacity="{rnd.uniform(.2, .45):.2f}"/>'
    b += f'<path d="M{cx - 30} {cy - ry + 8} L1790 236" stroke="#ffe0a0" stroke-width="6" opacity=".7"/>'
    # cut face
    b += f'<ellipse cx="{cx}" cy="{cy}" rx="{rx + 40}" ry="{ry + 40}" fill="#ffd890" opacity=".35" filter="url(#b26)"/>'
    b += f'<ellipse cx="{cx}" cy="{cy}" rx="{rx + 16}" ry="{ry + 14}" fill="#4a3624" stroke="#120c08" stroke-width="5"/>'
    b += f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="url(#face)"/>'
    d += f'<clipPath id="fc"><ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}"/></clipPath>'
    tx = tubes(rnd, cx, cy, rx, ry, 150, 3, 7, ['#f6e2b4', '#e8c88a', '#fff0d0', '#d8b070'])
    tx += tubes(rnd, cx, cy, rx, ry, 60, 6, 11, ['#fff2d6', '#f0d098'])
    b += f'<g clip-path="url(#fc)">{tx}<ellipse cx="{cx - 80}" cy="{cy - 120}" rx="160" ry="110" fill="#fff" opacity=".18" filter="url(#b26)"/>'
    b += f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="none" stroke="#6a4020" stroke-width="40" opacity=".35" filter="url(#b14)"/></g>'
    b += f'<path d="M{cx - rx + 10} {cy - 60} A{rx} {ry} 0 0 1 {cx + 60} {cy - ry + 4}" fill="none" stroke="#fff4d0" stroke-width="7" opacity=".85"/>'
    # cracks at the cut edge
    for a0 in (.6, 2.3, 4.1):
        x0 = cx + math.cos(a0) * (rx + 10); y0 = cy + math.sin(a0) * (ry + 10); pts = [(x0, y0)]
        for _ in range(4):
            x0 -= math.cos(a0) * rnd.uniform(10, 24); y0 -= math.sin(a0) * rnd.uniform(10, 24); x0 += rnd.uniform(-8, 8); pts.append((x0, y0))
        b += f'<polyline points="{P(pts)}" fill="none" stroke="#2a1608" stroke-width="3.4"/>'
    # chips and a geologist hammer on the shelf
    for _ in range(18):
        b += rock(rnd.uniform(620, 1560), rnd.uniform(890, 1010), rnd.uniform(6, 18), rnd, base='#6a5440', hi='#ffd090', sh='#1a1008')
    b += ('<g transform="translate(1320 960) rotate(-12)"><rect x="-150" y="-9" width="230" height="18" rx="8" fill="#8a5a30" stroke="#1a0e06" stroke-width="4"/>'
          '<path d="M60 -38 L118 -30 L118 30 L96 26 L60 18Z" fill="#7a8490" stroke="#1a0e06" stroke-width="4"/><path d="M66 -32 L112 -26" stroke="#e8f0ff" stroke-width="4" opacity=".8"/></g>')
    # detective frog with deerstalker cap, holding a big magnifier up to the cut face
    mx, my, mr = 940, 770, 118
    b += f'<circle cx="{mx}" cy="{my}" r="{mr + 30}" fill="#bfe8ff" opacity=".18" filter="url(#b26)"/>'
    d += f'<clipPath id="lc"><circle cx="{mx}" cy="{my}" r="{mr}"/></clipPath>'
    zoom = f'<circle cx="{mx}" cy="{my}" r="{mr}" fill="#e8c88a"/>' + tubes(random.Random(7), mx, my, mr, mr, 30, 12, 20, ['#fff2d6', '#f0d098', '#f8e0b0'])
    b += f'<g clip-path="url(#lc)">{zoom}<circle cx="{mx}" cy="{my}" r="{mr}" fill="url(#lens)"/></g>'
    b += f'<path d="M{mx - 80} {my - 50} Q{mx - 60} {my - 86} {mx - 20} {my - 96}" fill="none" stroke="#fff" stroke-width="9" opacity=".75"/>'
    b += f'<circle cx="{mx}" cy="{my}" r="{mr}" fill="none" stroke="#1a1008" stroke-width="22"/><circle cx="{mx}" cy="{my}" r="{mr}" fill="none" stroke="#d8a648" stroke-width="13"/>'
    b += f'<path d="M{mx - 84} {my + 84} L{mx - 190} {my + 190}" stroke="#1a1008" stroke-width="32" stroke-linecap="round"/><path d="M{mx - 84} {my + 84} L{mx - 190} {my + 190}" stroke="#6a3a1c" stroke-width="22" stroke-linecap="round"/>'
    cap = ('<g transform="translate(6 -96) rotate(-4)"><path d="M-36 6 Q-34 -32 0 -34 Q34 -32 36 6Z" fill="#a8885a" stroke-width="3.4"/>'
           '<path d="M-36 -2 Q0 -12 36 -2 M-30 -16 Q0 -26 30 -16 M-6 -34 L-4 4 M12 -32 L10 4" fill="none" stroke="#6a5030" stroke-width="2.4"/>'
           '<path d="M30 2 Q52 2 58 14 Q40 12 30 8Z M-30 2 Q-52 2 -58 14 Q-40 12 -30 8Z" fill="#8a6a40" stroke-width="3"/>'
           '<circle cx="0" cy="-34" r="5" fill="#8a6a40" stroke-width="2.4"/></g>')
    coat = '<path d="M-34 -24 Q6 -6 44 -24 L40 2 Q6 10 -30 2Z" fill="#8a6a40" stroke-width="3" opacity=".9"/>'
    b += '<circle cx="640" cy="930" r="170" fill="#ffe0a8" opacity=".14" filter="url(#b50)"/>'
    b += frog(640, 1030, 2.35, rot=-2, look=(12, -6), mouth='O', shadow=True, mid=coat, top=cap,
              armL='M-34 -22 q-18 6 -20 24', armR='M38 -22 q40 -14 64 -36')
    b += spark(1060, 300, 22) + spark(1540, 200, 16) + spark(1400, 760, 14) + spark(880, 620, 18, '#e8f8ff')
    b += f'<g mask="url(#cor)">{dust(rnd, 60, 1300, 300, 60, 880, "#fff0c8")}</g>'
    b += '<rect width="1920" height="1080" fill="url(#vig)"/>'
    lines = [('NOT', 170, 'w'), ('WOOD', 260, 'y'), ('AT ALL', 170, 'w')]
    return page('#0e2228', svg(d, b), lines, outline='#081012', top=40)


# ================= short3: frog on top of a pillar, spores on fast high wind =================
def make_3():
    rnd = random.Random(26)
    d = FILTERS + CORNER
    hz = 860
    d += lin('sky', [(0, '#1e5e9a'), (.45, '#4f9ac8'), (.8, '#a8d6e4'), (1, '#e8f0d8')])
    d += rad('sun', 300, 120, 700, [(0, '#fffbe8', .9), (.2, '#fff0c0', .4), (1, '#fff0c0', 0)])
    d += lin('gnd', [(0, '#8a7a56'), (.3, '#5e5238'), (1, '#2a2418')])
    d += rad('vig', 960, 540, 1150, [(0, '#000', 0), (.62, '#000', 0), (1, '#06101a', .6)])
    b = '<rect width="1920" height="1080" fill="url(#sky)"/><rect width="1920" height="1080" fill="url(#sun)"/>'
    # clouds streaming with the wind
    for _ in range(10):
        x = rnd.uniform(-100, 1900); y = rnd.uniform(80, 640); w = rnd.uniform(220, 480)
        b += f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{w:.0f}" ry="{w * .1:.0f}" fill="#ffffff" opacity="{rnd.uniform(.25, .5):.2f}" filter="url(#b14)"/>'
        b += f'<ellipse cx="{x - w * .2:.0f}" cy="{y - w * .05:.0f}" rx="{w * .45:.0f}" ry="{w * .09:.0f}" fill="#fff" opacity=".35" filter="url(#b8)"/>'
    # far hills + small far pillars
    b += '<path d="M0 840 Q300 806 620 830 T1260 818 T1920 826 L1920 880 L0 880Z" fill="#7a9a96" opacity=".7"/>'
    for i, (x, h, w) in enumerate(((560, 120, 10), (1720, 150, 12), (1500, 80, 7), (300, 70, 6))):
        dd, oo, *_ = pillar(f's3f{i}', x, hz + 2, h, w, w * .85, rnd.uniform(-5, 5), rnd, [(0, '#f0e2c8'), (.4, '#b8a88e'), (1, '#7a6a58')], rim='#fff', detail=.15)
        d += dd; b += f'<g opacity=".7">{oo}</g>'
    b += f'<rect x="0" y="{hz}" width="1920" height="{1080 - hz}" fill="url(#gnd)"/>'
    b += moss(0, 1920, hz + 4, hz + 40, 220, rnd, ['#7a8a3a', '#62722c', '#8e9a44'], 3, 10)
    b += moss(0, 1560, hz + 40, 1080, 260, rnd, ['#5a6a2a', '#6a7a32', '#4a5824'], 6, 22, (.4, .8))
    for _ in range(40):
        y = rnd.uniform(hz + 8, 1070); x = rnd.uniform(0, 1560)
        b += cooksonia(x, y, 8 + (y - hz) * .3, rnd, col='#4e6a26', spc='#e0a848')
    # wind: slow short puffs near the ground, long fast streaks high up
    for _ in range(9):
        x = rnd.uniform(80, 1500); y = rnd.uniform(hz - 40, hz + 30)
        b += f'<path d="M{x:.0f} {y:.0f} q30 -8 60 0" fill="none" stroke="#fff" stroke-width="3" opacity=".5" stroke-linecap="round"/>'
    for k in range(9):
        y = 120 + k * 52 + rnd.uniform(-10, 10); x0 = rnd.uniform(1150, 1300); L = rnd.uniform(380, 640)
        b += f'<path d="M{x0:.0f} {y:.0f} Q{x0 + L * .5:.0f} {y - 40:.0f} {x0 + L:.0f} {y - 20:.0f}" fill="none" stroke="#ffffff" stroke-width="{rnd.uniform(3, 6):.1f}" opacity="{rnd.uniform(.4, .75):.2f}" stroke-linecap="round"/>'
    # the tower
    b += '<ellipse cx="1080" cy="620" rx="200" ry="420" fill="#fff8e0" opacity=".25" filter="url(#b90)"/>'
    dd, oo, C, W, _ = pillar('s3m', 1250, 980, 640, 120, 104, 10, rnd,
                             [(0, '#fff6dc'), (.08, '#f0dcb4'), (.3, '#ccb490'), (.6, '#9a8468'), (.9, '#665646'), (1, '#463a2e')],
                             rim='#ffffff', rim_side=-1, detail=1.6)
    d += dd; b += oo
    tx, ty = C(1)
    b += moss(960, 1180, 960, 990, 110, rnd, ['#7a8a34', '#62722c', '#8e9a40'], 4, 12)
    for _ in range(12):
        b += cooksonia(rnd.uniform(950, 1190), rnd.uniform(968, 994), rnd.uniform(14, 30), rnd, col='#4e6a26', spc='#e8a84a')
    # spore clouds streaming off the top, up and to the right, on the high wind
    sp = ''
    for k in range(5):
        a0 = -.15 - k * .09
        for i in range(70):
            t = i / 70; L = 80 + t * 900
            x = tx + 40 + math.cos(a0) * L + rnd.gauss(0, 14 + t * 60); y = ty - 30 + math.sin(a0) * L - t * t * 140 + rnd.gauss(0, 10 + t * 50)
            if x > 1910 or y < 10: continue
            r = rnd.choice([2.2, 3, 4.2, 5.4]) * (1.2 - t * .5)
            sp += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r:.1f}" fill="{rnd.choice(["#fff3c0", "#f2d27a", "#ffe8a0"])}" opacity="{rnd.uniform(.6, 1) * (1 - t * .45):.2f}"/>'
    b += f'<g filter="url(#b4)" opacity=".6">{sp}</g>{sp}'
    b += f'<ellipse cx="{tx + 160:.0f}" cy="{ty - 70:.0f}" rx="200" ry="70" fill="#fff2c0" opacity=".35" filter="url(#b26)" transform="rotate(-16 {tx + 160:.0f} {ty - 70:.0f})"/>'
    # aviator frog sitting on the top, holding on, scarf flying in the wind
    gog = (
           '<path d="M-34 -96 Q6 -108 48 -96" fill="none" stroke="#5a3a20" stroke-width="6"/>'
           '<g fill="#9ad8f0" stroke-width="3.4"><ellipse cx="-6" cy="-100" rx="13" ry="10"/><ellipse cx="22" cy="-100" rx="13" ry="10"/></g>'
           '<path d="M-10 -104 l6 -3 M18 -104 l6 -3" stroke="#fff" stroke-width="3"/>')
    scarf = ('<path d="M-30 -24 Q6 -10 42 -24 L42 -12 Q6 2 -30 -12Z" fill="#e0503a" stroke-width="3"/>'
             '<path d="M40 -20 Q80 -34 120 -24 Q100 -12 130 -2 Q90 2 44 -10Z" fill="#e0503a" stroke-width="3"/>')
    b += frog(tx - 6, ty + 10, 2.0, rot=-4, look=(12, -8), mouth='O', top=gog, mid=scarf,
              armL='M-34 -22 q-22 6 -28 30', armR='M38 -22 q30 -18 44 -54')
    b += spark(tx + 300, ty - 160, 26, '#fffbe6') + spark(1600, 180, 20) + spark(1820, 330, 16) + spark(900, 520, 14)
    b += '<rect width="1920" height="1080" fill="url(#vig)"/>'
    lines = [('WHY BUILD', 150, 'w'), ('A', 120, 'w'), ('TOWER?', 250, 'y')]
    return page('#1e5e9a', svg(d, b), lines, outline='#0a1626', top=40)


# ================= short4: cut-away of the pillar base, tunnels and residents =================
def make_4():
    rnd = random.Random(404)
    d = FILTERS + CORNER
    hz = 820
    d += lin('sky', [(0, '#c8742e'), (.5, '#e8a850'), (1, '#f8dc98')])
    d += rad('sun', 220, 90, 900, [(0, '#fffbe6', 1), (.12, '#fff0b0', .7), (.4, '#ffd070', .25), (1, '#ffd070', 0)])
    d += lin('gnd', [(0, '#c0884a'), (.3, '#8a5a30'), (1, '#3a2414')])
    d += rad('cave', 1250, 760, 260, [(0, '#ffc870', .9), (.5, '#c87a3a', .45), (1, '#4a2a14', 0)])
    d += rad('vig', 960, 540, 1150, [(0, '#000', 0), (.6, '#000', 0), (1, '#1a0a04', .7)])
    b = '<rect width="1920" height="1080" fill="url(#sky)"/><rect width="1920" height="1080" fill="url(#sun)"/>'
    for k in range(18):
        a = .1 + k * .085
        b += f'<path d="M220 90 L{220 + math.cos(a - .015) * 2000:.0f} {90 + math.sin(a - .015) * 2000:.0f} L{220 + math.cos(a + .015) * 2000:.0f} {90 + math.sin(a + .015) * 2000:.0f}Z" fill="#fff6d0" opacity=".08"/>'
    b += '<circle cx="220" cy="90" r="70" fill="#fffef4"/><circle cx="220" cy="90" r="140" fill="#fff4c0" opacity=".6" filter="url(#b26)"/>'
    # heat haze, far rocky plain with far pillars
    b += '<path d="M0 800 L180 778 L300 790 L520 770 L760 792 L1000 780 L1300 796 L1600 774 L1920 790 L1920 840 L0 840Z" fill="#c89060" opacity=".7"/>'
    for i, (x, h, w) in enumerate(((620, 110, 9), (1760, 170, 14), (1880, 90, 8), (480, 70, 6))):
        dd, oo, *_ = pillar(f's4f{i}', x, hz + 2, h, w, w * .85, rnd.uniform(-5, 5), rnd, [(0, '#fff0c8'), (.4, '#c8a47a'), (1, '#7a5a3e')], rim='#fff4c8', detail=.15)
        d += dd; b += f'<g opacity=".7">{oo}</g>'
    b += f'<rect x="0" y="{hz}" width="1920" height="{1080 - hz}" fill="url(#gnd)"/>'
    for _ in range(40):
        y = rnd.uniform(hz + 10, 1070); sc = ((y - hz) / (1080 - hz)) ** 1.3; x = rnd.uniform(0, 1560)
        b += rock(x, y, 3 + sc * rnd.uniform(10, 28), rnd, base='#8a5a34', hi='#ffd890', sh='#2a160a')
    for _ in range(20):
        y = rnd.uniform(hz + 10, 1060); x = rnd.uniform(0, 900)
        b += cooksonia(x, y, 8 + (y - hz) * .2, rnd, col='#5a6a2a', spc='#e8a040')
    # cool shade cast to the right of the tower
    b += '<path d="M1180 1000 L1420 990 L1760 1040 L1700 1080 L1220 1080Z" fill="#2a1a2a" opacity=".45" filter="url(#b14)"/>'
    # the tower (cropped by the top edge)
    dd, oo, C, W, path = pillar('s4m', 1260, 1010, 1180, 250, 220, -20, rnd,
                                [(0, '#fff4d8'), (.06, '#f6dcae'), (.25, '#dcbc8c'), (.55, '#b0906a'), (.85, '#7a6248'), (1, '#4a3a2c')],
                                rim='#fffbe6', rim_side=-1, detail=2.2)
    d += dd; b += oo
    # cut-away window into the base
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
    # residents: millipede curled in a chamber munching, springtails, spider relative
    inner += millipede(1196, 874, .62, -2, rnd, col='#6a3a1e', hi='#e09858')
    inner += '<path d="M1300 872 l10 -6 l-2 10 z M1306 862 l6 4" fill="#e8d0a0" stroke="#3a2010" stroke-width="1.4"/>'
    inner += springtail(1320, 652, 2.0) + springtail(1384, 800, 1.7, -1)
    inner += trigono(1150, 660, 1.6)
    inner += f'<path d="{cut}" fill="none" stroke="#2a1408" stroke-width="30" opacity=".45" filter="url(#b8)"/>'
    b += f'<g clip-path="url(#cw)">{inner}</g>'
    b += f'<path d="{cut}" fill="none" stroke="#2a1608" stroke-width="7"/><path d="{cut}" fill="none" stroke="#fff2d0" stroke-width="3" opacity=".8" transform="translate(-4 -4)"/>'
    # outside: millipede climbing towards a tunnel mouth, springtail on the ground in the shade
    b += millipede(1460, 980, .9, -100, rnd, col='#5a3420', hi='#d08a52')
    b += f'<ellipse cx="1452" cy="760" rx="16" ry="20" fill="#1a0c06" stroke="#3a2412" stroke-width="3"/>'
    b += springtail(1520, 1012, 1.6, -1)
    b += moss(1060, 1460, 990, 1020, 140, rnd, ['#7a8434', '#62702c', '#8e9a40'], 4, 12)
    for _ in range(12):
        b += cooksonia(rnd.uniform(1040, 1470), rnd.uniform(996, 1022), rnd.uniform(14, 30), rnd, col='#4e6226', spc='#e8a84a')
    # frog with a napkin bib and a fork, amazed
    bib = ('<path d="M-22 -30 Q6 -22 34 -30 L30 2 Q6 10 -18 2Z" fill="#fff8f0" stroke-width="3"/>'
           '<path d="M-14 -20 L26 -20 M-12 -8 L24 -8" stroke="#e05a4a" stroke-width="3"/>')
    fork = ('<g transform="translate(72 -86) rotate(14)"><rect x="-3" y="0" width="6" height="56" rx="3" fill="#cfd6e0" stroke-width="2.4"/>'
            '<path d="M-10 0 L-10 -24 M-3 0 L-3 -26 M3 0 L3 -26 M10 0 L10 -24 M-10 0 Q0 8 10 0" fill="none" stroke="#cfd6e0" stroke-width="3.4"/></g>')
    b += '<circle cx="600" cy="930" r="170" fill="#fff0c0" opacity=".2" filter="url(#b50)"/>'
    b += frog(600, 1030, 2.35, rot=3, look=(12, -8), mouth='O', shadow=True, mid=bib,
              armL='M-34 -22 q-18 6 -20 24', armR='M38 -22 q22 -10 34 -34', front=fork)
    b += spark(1250, 640, 18) + spark(1400, 580, 14) + spark(980, 420, 16) + spark(1560, 260, 20)
    b += f'<g mask="url(#cor)">{dust(rnd, 40, 1200, 300, 80, 1000, "#fff4d0")}</g>'
    b += '<rect width="1920" height="1080" fill="url(#vig)"/>'
    lines = [('A HOME', 170, 'w'), ('AND A', 130, 'w'), ('MEAL?', 250, 'y')]
    return page('#c8742e', svg(d, b), lines, outline='#1a0c04', top=40)


# ================= short5: Archaeopteris dwarfs a small pillar, its crown falls =================
def crown(x, y, s, rot):
    return (f'<g transform="translate({x} {y}) rotate({rot}) scale({s})" stroke="#3a2406" stroke-width="3.4" stroke-linejoin="round">'
            '<path d="M-40 16 L-46 -26 L-24 -6 L0 -36 L24 -6 L46 -26 L40 16Z" fill="#f2c23a"/>'
            '<path d="M-40 16 L40 16 L40 26 L-40 26Z" fill="#e0a82a"/>'
            '<path d="M-36 8 L-40 -16 M-18 -2 L0 -26" fill="none" stroke="#fff4b0" stroke-width="4"/>'
            '<circle cx="0" cy="8" r="6" fill="#e04a5a"/><circle cx="-24" cy="10" r="4.5" fill="#4ab0e0"/><circle cx="24" cy="10" r="4.5" fill="#4ab0e0"/>'
            '<circle cx="-46" cy="-28" r="4" fill="#fff0a0"/><circle cx="0" cy="-38" r="4" fill="#fff0a0"/><circle cx="46" cy="-28" r="4" fill="#fff0a0"/></g>')


def make_5():
    rnd = random.Random(30)
    d = FILTERS + CORNER
    hz = 880
    d += lin('sky', [(0, '#1e3a24'), (.5, '#3e6a3e'), (1, '#9ab878')])
    d += rad('sun', 1500, 120, 900, [(0, '#fffbd8', .9), (.18, '#f2e098', .45), (1, '#f2e098', 0)])
    d += lin('gnd', [(0, '#4a5a2a'), (.3, '#33401e'), (1, '#121808')])
    d += lin('trunk', [(0, '#2a1a0e'), (.3, '#6a4a2a'), (.55, '#8a6238'), (.8, '#4a321c'), (1, '#20140a')], x2=1, y2=0)
    d += rad('vig', 960, 540, 1150, [(0, '#000', 0), (.6, '#000', 0), (1, '#040a04', .75)])
    b = '<rect width="1920" height="1080" fill="url(#sky)"/><rect width="1920" height="1080" fill="url(#sun)"/>'
    # background forest of Archaeopteris (soft silhouettes)
    for k in range(14):
        x = rnd.uniform(0, 1920); h = rnd.uniform(420, 760); w = rnd.uniform(10, 18)
        b += f'<path d="M{x:.0f} {hz} L{x + 4:.0f} {hz - h:.0f}" stroke="#2e4a30" stroke-width="{w:.0f}" opacity=".55"/>'
        for j in range(6):
            yy = hz - h + j * h * .1
            b += f'<ellipse cx="{x + 4:.0f}" cy="{yy:.0f}" rx="{70 + j * 16:.0f}" ry="{18 + j * 3:.0f}" fill="#36603e" opacity=".45" filter="url(#b4)"/>'
    for k in range(6):
        x = 1300 + k * 120
        b += f'<path d="M{x} -20 L{x + 60} -20 L{x - 320} {hz} L{x - 440} {hz}Z" fill="#fff8c8" opacity=".08"/>'
    b += f'<rect x="0" y="{hz}" width="1920" height="{1080 - hz}" fill="url(#gnd)"/>'
    b += moss(0, 1920, hz + 4, hz + 40, 240, rnd, ['#5a7a2a', '#4a6a24', '#6e8a34'], 3, 10)
    b += moss(0, 1560, hz + 40, 1080, 260, rnd, ['#3e5a20', '#4e6a28', '#2e4818'], 6, 24, (.4, .85))
    # the huge Archaeopteris: trunk rising past the top, roots spreading
    tx = 1330
    trunk = f'M{tx - 120} {hz + 70} Q{tx - 80} 600 {tx - 60} -20 L{tx + 60} -20 Q{tx + 80} 600 {tx + 130} {hz + 70}Z'
    for (ang, L, w) in ((2.8, 260, 36), (2.4, 200, 30), (.5, 180, 30), (.25, 170, 24), (1.6, 120, 26)):
        x0 = tx + math.cos(ang) * 60; y0 = hz + 50
        pts = [(x0, y0)]; a = ang
        for s in range(5):
            a += rnd.uniform(-.15, .15); pts.append((pts[-1][0] + math.cos(a) * L / 5, pts[-1][1] + math.sin(a) * L / 5 * .35 + 3))
        pts = [(min(px, 1560), py) for px, py in pts]
        b += f'<polyline points="{P(pts)}" fill="none" stroke="#1a0e06" stroke-width="{w + 7}" stroke-linecap="round"/><polyline points="{P(pts)}" fill="none" stroke="#6a4a2a" stroke-width="{w}" stroke-linecap="round"/>'
    b += f'<path d="{trunk}" fill="url(#trunk)" stroke="#120a04" stroke-width="5"/>'
    for _ in range(40):
        y0 = rnd.uniform(0, hz + 40); x0 = tx + rnd.uniform(-70, 70)
        b += f'<path d="M{x0:.0f} {y0:.0f} q{rnd.uniform(-6, 6):.0f} {rnd.uniform(30, 90):.0f} {rnd.uniform(-4, 4):.0f} {rnd.uniform(60, 160):.0f}" fill="none" stroke="{rnd.choice(["#1a0e06", "#a07848"])}" stroke-width="{rnd.uniform(2, 5):.1f}" opacity=".5"/>'
    b += f'<path d="M{tx + 50} -20 Q{tx + 70} 600 {tx + 118} {hz + 60}" fill="none" stroke="#ffe8a0" stroke-width="7" opacity=".7"/>'
    # canopy: big fern-like fronds filling the top right
    for k in range(13):
        y = 40 + k * 46; L = 260 + k * 22 + rnd.uniform(-30, 30)
        for side, base in ((1, -12), (-1, 192)):
            ang = base + side * rnd.uniform(-8, 10) + side * k * 1.2
            if side < 0 and k < 5: L2 = L * .55
            else: L2 = L
            b += frond(tx + side * 30, y, L2, ang, rnd, '#3e7a34', '#78b04a', lw=5)
    for _ in range(30):
        b += f'<ellipse cx="{rnd.uniform(1050, 1900):.0f}" cy="{rnd.uniform(0, 640):.0f}" rx="{rnd.uniform(40, 90):.0f}" ry="{rnd.uniform(10, 22):.0f}" fill="#c8f080" opacity="{rnd.uniform(.08, .2):.2f}" filter="url(#b8)"/>'
    # the small Prototaxites in the deep shade, cracked, crown falling
    b += '<ellipse cx="960" cy="800" rx="120" ry="180" fill="#fff0b0" opacity=".12" filter="url(#b50)"/>'
    dd, oo, C, W, _ = pillar('s5p', 960, hz + 60, 240, 48, 40, 8, rnd,
                             [(0, '#d8d0b0'), (.25, '#a8a088'), (.6, '#7a7262'), (1, '#4a4438')], rim='#e8f0b0', rim_side=1, detail=1.0, cap=.6)
    d += dd; b += oo
    cx_, cy_ = C(1)
    b += f'<path d="M{cx_ - 30:.0f} {cy_ + 10:.0f} l14 22 l-8 18 l14 26 M{cx_ + 20:.0f} {cy_ + 6:.0f} l-10 20 l8 16" fill="none" stroke="#1e1a12" stroke-width="3.4"/>'
    for k in range(6):
        b += rock(cx_ + rnd.uniform(-80, 80), hz + 64 + rnd.uniform(-6, 10), rnd.uniform(5, 12), rnd, base='#8a8270', hi='#e8e0c0', sh='#2a261c')
    # crown tumbling off with motion arcs
    kx, ky = cx_ - 110, cy_ - 90
    b += f'<path d="M{cx_ - 10:.0f} {cy_ - 30:.0f} Q{cx_ - 40:.0f} {cy_ - 110:.0f} {kx + 30:.0f} {ky - 20:.0f}" fill="none" stroke="#fff4c0" stroke-width="5" stroke-dasharray="12 12" opacity=".8"/>'
    b += f'<circle cx="{kx:.0f}" cy="{ky:.0f}" r="90" fill="#ffe080" opacity=".35" filter="url(#b26)"/>'
    b += crown(kx, ky, 2.1, -34)
    b += spark(kx - 60, ky - 50, 18, '#fff8c0') + spark(kx + 70, ky + 30, 12, '#fff8c0')
    # frog with a leaf hat, arms up to catch the crown
    leaf = ('<g transform="translate(4 -100) rotate(-10)"><path d="M-40 6 Q-10 -40 40 -10 Q10 18 -40 6Z" fill="#7ab84a" stroke-width="3.2"/>'
            '<path d="M-36 4 Q0 -10 34 -10" fill="none" stroke="#3a6a24" stroke-width="2.4"/></g>')
    b += '<circle cx="640" cy="930" r="170" fill="#e8ffc0" opacity=".14" filter="url(#b50)"/>'
    b += frog(640, 1032, 2.35, rot=4, look=(12, -12), mouth='O', shadow=True, top=leaf,
              armL='M-34 -22 q-24 -10 -30 -42', armR='M38 -22 q24 -14 30 -46')
    for _ in range(50):
        b += f'<circle cx="{rnd.uniform(900, 1880):.0f}" cy="{rnd.uniform(40, 860):.0f}" r="{rnd.choice([1.4, 2, 2.8])}" fill="#fff8d0" opacity="{rnd.uniform(.2, .7):.2f}"/>'
    b += spark(1500, 120, 30, '#fffbe6') + spark(1700, 420, 16)
    b += '<rect width="1920" height="1080" fill="url(#vig)"/>'
    lines = [('OUTGROWN', 170, 'y'), ('BY', 130, 'w'), ('TREES', 230, 'w')]
    return page('#1e3a24', svg(d, b), lines, outline='#081008', top=40)


for n, fn in ((1, make_1), (2, make_2), (3, make_3), (4, make_4), (5, make_5)):
    out = os.path.join(VID, f'giant-mold-short{n}', 'thumb'); os.makedirs(out, exist_ok=True)
    for f in ('common.css', 'Fredoka-700.woff2'):
        shutil.copyfile(os.path.join(VID, 'giant-mold', 'thumb', f), os.path.join(out, f))
    open(os.path.join(out, 'A.html'), 'w').write(fn())
print('ok')
