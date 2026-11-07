# STYLE B shorts thumbnails for giant-mold (guideline 16-9 B, miya 2026-11-07): dark scene, ONE big glowing concrete subject in the top half
# (y 180-840), centred 2-line hook on a dark band (y 860-1240), frog + foreground in the bottom third. Hooks from the short scripts only.
# Reuses helpers of videos/giant-mold/thumb/make.py and tubes() of ./make.py (old style, kept).
#   python3 videos/giant-mold-short1/thumb/make_b.py   -> videos/giant-mold-short{1..5}/thumb/A.html
# short1 TALLEST / ON LAND     one glowing pale pillar at night over ankle-high plants (S: "tallest thing on land", "eight meters")
# short2 NOT WOOD              glowing cut log end full of woven tubes (S: "no wood cells and no growth rings", "interwoven tubes")
# short3 WHY BUILD / A TOWER?  pillar top releasing glowing spores into the high wind (S: spore dispersal hypothesis, hedged -> question)
# short4 A HOME AND / A MEAL?  cut-away window into the pillar: tunnels, millipede, springtails (S: "both a home and a meal", hedged -> ?)
# short5 OUTGROWN / BY TREES   tall Archaeopteris vs small cracked pillar, gold crown falling (S: "could not compete in this new world")
import os, sys, math, random, shutil
HERE = os.path.dirname(os.path.abspath(__file__))
VID = os.path.abspath(os.path.join(HERE, '..', '..'))
TOOLS = os.path.abspath(os.path.join(VID, '..', 'tools'))
sys.path.insert(0, TOOLS)
_old = open(os.path.join(HERE, 'make.py')).read().split('\nfor n, fn in ((1, make_1)')[0]
G = {'__file__': os.path.join(HERE, 'make.py'), '__name__': 'giantmold_old'}
exec(_old, G)
pillar, cooksonia, millipede, springtail, trigono, moss, rock, frond, P = (G[k] for k in ('pillar', 'cooksonia', 'millipede', 'springtail', 'trigono', 'moss', 'rock', 'frond', 'P'))
_frog, tubes, dust, crown = G['frog'], G['tubes'], G['dust'], G['crown']
FILTERS = G['FILTERS'] + '<filter id="b6" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="6"/></filter>'
from thumb_lib import vpage, vsvg, lin, rad, spark, fireflies, halo, darkband
W, H = 1080, 1920
HZ = 860


def frog(x, y, s, look=(0, 0), **kw):
    lx, ly = look; ox, oy = 1 + lx, ly; m = math.hypot(ox, oy)
    if m > 6.3: k = 6.3 / m; lx, ly = ox * k - 1, oy * k
    return _frog(x, y, s, look=(lx, ly), **kw)


def VIG(a=.7):
    return rad('vig', 540, 960, 1250, [(0, '#000', 0), (.55, '#000', 0), (1, '#000', a)])


def finish(d, b, lines, bg, top, outline, band=.5):
    b += darkband(HZ, 1250, band)
    b += f'<rect width="{W}" height="{H}" fill="url(#vig)"/>'
    return vpage(bg, vsvg(d, b), lines, outline=outline, top=top)


def ground(rnd, c0, c1, rim, moss_cols, spc, n=40):
    d = lin('gnd', [(0, c0), (.4, c1), (1, '#04060a')])
    b = f'<rect y="{HZ}" width="{W}" height="{H - HZ}" fill="url(#gnd)"/><path d="M0 {HZ} L{W} {HZ}" stroke="{rim}" stroke-width="3" opacity=".5"/>'
    b += moss(0, W, HZ + 4, HZ + 60, 120, rnd, moss_cols, 3, 10) + moss(0, W, HZ + 60, H, 260, rnd, moss_cols, 6, 30, (.3, .75))
    for _ in range(n):
        y = rnd.uniform(HZ + 10, 1890); x = rnd.uniform(0, W)
        b += cooksonia(x, y, 8 + (y - HZ) * .09, rnd, col=moss_cols[0], spc=spc)
    return d, b


# ================= short1 =================
def make_1():
    rnd = random.Random(501)
    d = FILTERS + VIG(.75)
    d += lin('sky', [(0, '#080a24'), (.5, '#1d1d4e'), (.85, '#4a3a78'), (1, '#7a5a88')])
    d += halo('h1', 540, 520, 520, inner='#ffe9c0', outer='#a07aff')
    b = f'<rect width="{W}" height="{HZ + 4}" fill="url(#sky)"/>'
    for _ in range(120):
        b += f'<circle cx="{rnd.randint(0, W)}" cy="{rnd.randint(10, HZ - 60)}" r="{rnd.choice([1, 1.5, 2.2])}" fill="#eef" opacity="{rnd.uniform(.25, .9):.2f}"/>'
    b += '<circle cx="190" cy="300" r="64" fill="#f6f2ea"/><circle cx="170" cy="284" r="12" fill="#d6d0e0" opacity=".7"/><circle cx="212" cy="326" r="16" fill="#d6d0e0" opacity=".6"/><circle cx="190" cy="300" r="140" fill="#cfd0ff" opacity=".25" filter="url(#b26)"/>'
    b += f'<ellipse cx="540" cy="520" rx="520" ry="520" fill="url(#h1)"/>'
    b += f'<path d="M0 {HZ - 10} L90 {HZ - 40} L240 {HZ - 34} L420 {HZ - 20} L700 {HZ - 36} L900 {HZ - 24} L1080 {HZ - 30} L1080 {HZ + 10} L0 {HZ + 10}Z" fill="#3a2f62" opacity=".9"/>'
    g, gb = ground(rnd, '#2a2a4a', '#10122a', '#c8b0ff', ['#3a6a5a', '#4a7a62', '#2e5a4c'], '#ffc070'); d += g
    b += gb
    for i, (x, h, w) in enumerate(((120, 190, 14), (330, 120, 10), (790, 150, 12), (960, 230, 17))):
        dd, oo, *_ = pillar(f'b1f{i}', x, HZ + 6, h, w, w * .85, rnd.uniform(-6, 6), rnd, [(0, '#3a3560'), (.5, '#7a70a0'), (1, '#c8b0c8')], rim='#d0c0ff', rim_side=1, detail=.3)
        d += dd; b += f'<g opacity=".8">{oo}</g>'
    dd, oo, C, Wd, _ = pillar('b1m', 540, HZ + 10, 640, 74, 56, -14, rnd,
                              [(0, '#4a4268'), (.3, '#8a80a8'), (.65, '#d0c0d8'), (.9, '#fff0e0'), (1, '#fff8f0')],
                              rim='#fff0d8', rim_side=1, detail=1.6, tex_dark='#2a2240', tex_light='#fff4e8')
    d += dd; b += oo
    tx, ty = C(1)
    b += f'<circle cx="{tx:.0f}" cy="{ty:.0f}" r="110" fill="#fff0d0" opacity=".35" filter="url(#b26)"/>'
    for _ in range(9):
        b += cooksonia(rnd.uniform(430, 660), rnd.uniform(HZ + 6, HZ + 22), rnd.uniform(5, 11), rnd, col='#4a8a6a', spc='#ffc070')
    # tiny ankle-high plants right at the foot, for scale
    b += spark(tx + 70, ty - 20, 26, '#fffbe8') + spark(250, 520, 14) + spark(900, 420, 16)
    b += fireflies(46, 120, 1800, col='#d8c8ff', core='#ffffff', seed=11)
    hat = ('<g transform="translate(6 -95) rotate(-6)"><path d="M-30 4 Q-28 -30 0 -32 Q28 -30 30 4Z" fill="#e8b84a" stroke-width="3.4"/>'
           '<path d="M-50 6 Q0 -8 50 6 Q46 18 0 14 Q-46 18 -50 6Z" fill="#d8a43a" stroke-width="3.2"/><path d="M-28 -4 Q0 -10 28 -4" fill="none" stroke="#c0503a" stroke-width="5"/></g>')
    cam = ('<g transform="translate(64 -62) rotate(-14)"><rect x="-26" y="-18" width="52" height="36" rx="6" fill="#2a2a34" stroke-width="3"/>'
           '<rect x="-14" y="-26" width="18" height="10" rx="3" fill="#3a3a44" stroke-width="2.4"/><circle cx="2" cy="0" r="12" fill="#5a6a8a" stroke-width="3"/>'
           '<circle cx="-1" cy="-3" r="4" fill="#cfe0ff" stroke="none"/><circle cx="18" cy="-11" r="3" fill="#ffe08a" stroke="none"/></g>')
    strap = '<path d="M-30 -38 Q6 0 44 -38" fill="none" stroke="#3a2a1a" stroke-width="3"/>'
    b += '<circle cx="250" cy="1680" r="190" fill="#d8c8ff" opacity=".16" filter="url(#b50)"/>'
    b += frog(250, 1760, 2.5, rot=2, look=(5, -5), mouth='O', shadow=True, mid=strap, top=hat, armL='M-34 -22 q-18 6 -20 24', armR='M38 -22 q16 -6 24 -36', front=cam)
    return finish(d, b, [('TALLEST', 200, 'y'), ('ON LAND', 200, 'w')], '#080a24', 880, '#0c0a1a')


# ================= short2 =================
def make_2():
    rnd = random.Random(1859)
    d = FILTERS + VIG(.8)
    cx, cy, rx, ry = 540, 520, 300, 300
    d += lin('bg', [(0, '#06141a'), (.5, '#0e2a30'), (1, '#050c10')])
    d += halo('h2', cx, cy, 560, inner='#ffe6b0', outer='#f2a040')
    d += lin('bark', [(0, '#3a2e24'), (.35, '#6a5644'), (.6, '#8a7458'), (1, '#2a2018')])
    d += rad('face', cx, cy, 340, [(0, '#fff0c8', 1), (.55, '#e8c078', 1), (.9, '#b8843e', 1), (1, '#6a4826', 1)])
    d += rad('lens', 380, 1560, 140, [(0, '#fff6dc', .12), (.8, '#bfe8ff', .08), (1, '#bfe8ff', .3)])
    d += lin('tbl', [(0, '#3a2a1c'), (.2, '#22170f'), (1, '#0a0705')])
    b = f'<rect width="{W}" height="{H}" fill="url(#bg)"/><ellipse cx="{cx}" cy="{cy}" rx="560" ry="560" fill="url(#h2)"/>'
    # log body going away to the right-back
    body = f'M{cx - 20} {cy - ry + 10} L1120 {cy - 190} L1120 {cy + 210} L{cx + 40} {cy + ry - 8}Z'
    b += f'<path d="{body}" fill="url(#bark)" stroke="#120c08" stroke-width="5"/>'
    for k in range(12):
        t = k / 11; y0 = cy - ry + 30 + t * (2 * ry - 60); y1 = cy - 180 + t * 380
        b += f'<path d="M{cx + 40:.0f} {y0:.0f} Q800 {(y0 + y1) / 2 + rnd.uniform(-14, 14):.0f} 1100 {y1:.0f}" fill="none" stroke="{rnd.choice(["#2a2018", "#a8906c", "#4a3a2a"])}" stroke-width="{rnd.uniform(2, 6):.1f}" opacity=".5"/>'
    b += f'<ellipse cx="{cx}" cy="{cy}" rx="{rx + 50}" ry="{ry + 50}" fill="#ffd890" opacity=".4" filter="url(#b26)"/>'
    b += f'<ellipse cx="{cx}" cy="{cy}" rx="{rx + 16}" ry="{ry + 14}" fill="#4a3624" stroke="#120c08" stroke-width="5"/>'
    b += f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="url(#face)"/>'
    d += f'<clipPath id="fc"><ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}"/></clipPath>'
    tx = tubes(rnd, cx, cy, rx, ry, 170, 3, 7, ['#fff6dc', '#f6e2b4', '#fff0d0', '#e8c88a']) + tubes(rnd, cx, cy, rx, ry, 70, 6, 11, ['#fff8e6', '#f6dca0'])
    b += f'<g clip-path="url(#fc)">{tx}<ellipse cx="{cx - 80}" cy="{cy - 110}" rx="170" ry="120" fill="#fff" opacity=".22" filter="url(#b26)"/></g>'
    b += f'<path d="M{cx - rx + 10} {cy - 60} A{rx} {ry} 0 0 1 {cx + 60} {cy - ry + 4}" fill="none" stroke="#fff4d0" stroke-width="7" opacity=".9"/>'
    b += spark(cx + 250, cy - 250, 28, '#fffbe6') + spark(120, 400, 16) + spark(960, 760, 16)
    b += f'<path d="M0 1500 Q540 1470 1080 1490 L1080 1920 L0 1920Z" fill="url(#tbl)"/><path d="M0 1500 Q540 1470 1080 1490" fill="none" stroke="#c8925a" stroke-width="4" opacity=".5"/>'
    b += fireflies(40, 120, 1800, col='#ffe6a0', core='#fffbe0', seed=21)
    # magnifier + frog, bottom third
    mx, my, mr = 640, 1590, 105
    b += f'<circle cx="{mx}" cy="{my}" r="{mr + 30}" fill="#bfe8ff" opacity=".18" filter="url(#b26)"/>'
    d += f'<clipPath id="lc"><circle cx="{mx}" cy="{my}" r="{mr}"/></clipPath>'
    zoom = f'<circle cx="{mx}" cy="{my}" r="{mr}" fill="#e8c88a"/>' + tubes(random.Random(7), mx, my, mr, mr, 30, 12, 20, ['#fff2d6', '#f0d098', '#f8e0b0'])
    b += f'<g clip-path="url(#lc)">{zoom}<circle cx="{mx}" cy="{my}" r="{mr}" fill="url(#lens)"/></g>'
    b += f'<path d="M{mx - 74} {my - 44} Q{mx - 56} {my - 80} {mx - 20} {my - 90}" fill="none" stroke="#fff" stroke-width="9" opacity=".75"/>'
    b += f'<circle cx="{mx}" cy="{my}" r="{mr}" fill="none" stroke="#1a1008" stroke-width="22"/><circle cx="{mx}" cy="{my}" r="{mr}" fill="none" stroke="#d8a648" stroke-width="13"/>'
    hx0, hy0, hx1, hy1 = mx - 70, my + 82, mx - 128, my + 200
    b += f'<path d="M{hx0} {hy0} L{hx1} {hy1}" stroke="#1a1008" stroke-width="32" stroke-linecap="round"/><path d="M{hx0} {hy0} L{hx1} {hy1}" stroke="#6a3a1c" stroke-width="22" stroke-linecap="round"/>'
    cap = ('<g transform="translate(6 -96) rotate(-4)"><path d="M-36 6 Q-34 -32 0 -34 Q34 -32 36 6Z" fill="#a8885a" stroke-width="3.4"/>'
           '<path d="M-36 -2 Q0 -12 36 -2 M-30 -16 Q0 -26 30 -16" fill="none" stroke="#6a5030" stroke-width="2.4"/>'
           '<path d="M30 2 Q52 2 58 14 Q40 12 30 8Z M-30 2 Q-52 2 -58 14 Q-40 12 -30 8Z" fill="#8a6a40" stroke-width="3"/><circle cx="0" cy="-34" r="5" fill="#8a6a40" stroke-width="2.4"/></g>')
    coat = '<path d="M-34 -24 Q6 -6 44 -24 L40 2 Q6 10 -30 2Z" fill="#8a6a40" stroke-width="3" opacity=".9"/>'
    fx, fy, fs = 190, 1790, 2.3
    ax, ay = (hx1 - fx) / fs - 38, (hy1 - fy) / fs + 22
    b += '<circle cx="190" cy="1690" r="170" fill="#ffe0a8" opacity=".14" filter="url(#b50)"/>'
    b += frog(fx, fy, fs, look=(5, -5), mouth='O', shadow=True, mid=coat, top=cap, armL='M-34 -22 q-18 6 -20 24', armR=f'M38 -22 q{ax * .6:.0f} {ay * .2:.0f} {ax:.0f} {ay:.0f}')
    return finish(d, b, [('NOT', 150, 'w'), ('WOOD', 280, 'y')], '#06141a', 880, '#081012')


# ================= short3 =================
def make_3():
    rnd = random.Random(26)
    d = FILTERS + VIG(.75)
    d += lin('sky', [(0, '#050a22'), (.45, '#0e2a5a'), (.85, '#2a5a88'), (1, '#5a8aa0')])
    d += halo('h3', 600, 360, 520, inner='#fff3c0', outer='#7ac8ff')
    b = f'<rect width="{W}" height="{HZ + 4}" fill="url(#sky)"/>'
    for _ in range(130):
        b += f'<circle cx="{rnd.randint(0, W)}" cy="{rnd.randint(10, HZ - 60)}" r="{rnd.choice([1, 1.5, 2.2])}" fill="#eef" opacity="{rnd.uniform(.25, .9):.2f}"/>'
    # high wind streaks
    for k in range(9):
        y = 180 + k * 62 + rnd.uniform(-10, 10); x0 = rnd.uniform(560, 760); L = rnd.uniform(260, 420)
        b += f'<path d="M{x0:.0f} {y:.0f} Q{x0 + L * .5:.0f} {y - 36:.0f} {x0 + L:.0f} {y - 14:.0f}" fill="none" stroke="#cfe8ff" stroke-width="{rnd.uniform(3, 6):.1f}" opacity="{rnd.uniform(.25, .55):.2f}" stroke-linecap="round"/>'
    b += f'<ellipse cx="600" cy="380" rx="520" ry="520" fill="url(#h3)"/>'
    g, gb = ground(rnd, '#3a4a2a', '#141c12', '#bfe0a0', ['#4e6a26', '#5e7a30', '#3e5a20'], '#e0a848')
    d += g; b += gb
    dd, oo, C, Wd, _ = pillar('b3m', 470, HZ + 8, 560, 70, 62, 70, rnd,
                              [(0, '#5a5a70'), (.3, '#9a9aa8'), (.62, '#d8d0c0'), (.88, '#fff4dc'), (1, '#ffffff')],
                              rim='#ffffff', rim_side=1, detail=1.5, tex_dark='#2a2a3a', tex_light='#fffaf0')
    d += dd; b += oo
    tx, ty = C(1)
    sp = ''
    for k in range(5):
        a0 = -.15 - k * .1
        for i in range(80):
            t = i / 80; L = 60 + t * 560
            x = tx + 30 + math.cos(a0) * L + rnd.gauss(0, 10 + t * 46); y = ty - 10 + math.sin(a0) * L - t * t * 110 + rnd.gauss(0, 8 + t * 36)
            if x > 1070 or y < 120: continue
            r = rnd.choice([3, 4, 5.5, 7]) * (1.2 - t * .5)
            sp += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r:.1f}" fill="{rnd.choice(["#fff3c0", "#f2d27a", "#ffe8a0"])}" opacity="{rnd.uniform(.65, 1) * (1 - t * .4):.2f}"/>'
    b += f'<g filter="url(#b6)" opacity=".7">{sp}</g>{sp}'
    b += f'<ellipse cx="{tx + 140:.0f}" cy="{ty - 50:.0f}" rx="200" ry="70" fill="#fff2c0" opacity=".4" filter="url(#b26)" transform="rotate(-18 {tx + 140:.0f} {ty - 50:.0f})"/>'
    b += spark(tx + 320, ty - 150, 28, '#fffbe6') + spark(160, 300, 16) + spark(940, 640, 16)
    b += fireflies(40, 120, 1800, col='#ffe6a0', core='#fffbe0', seed=31)
    gog = ('<path d="M-34 -96 Q6 -108 48 -96" fill="none" stroke="#5a3a20" stroke-width="6"/>'
           '<g fill="#9ad8f0" stroke-width="3.4"><ellipse cx="-6" cy="-100" rx="13" ry="10"/><ellipse cx="22" cy="-100" rx="13" ry="10"/></g>'
           '<path d="M-10 -104 l6 -3 M18 -104 l6 -3" stroke="#fff" stroke-width="3"/>')
    scarf = ('<path d="M-30 -24 Q6 -10 42 -24 L42 -12 Q6 2 -30 -12Z" fill="#e0503a" stroke-width="3"/>'
             '<path d="M40 -20 Q80 -34 120 -24 Q100 -12 130 -2 Q90 2 44 -10Z" fill="#e0503a" stroke-width="3"/>')
    b += '<circle cx="250" cy="1680" r="190" fill="#cfe8ff" opacity=".14" filter="url(#b50)"/>'
    b += frog(250, 1770, 2.4, rot=-3, look=(5, -6), mouth='O', shadow=True, top=gog, mid=scarf, armL='M-34 -22 q-22 6 -28 30', armR='M38 -22 q30 -18 44 -54')
    return finish(d, b, [('WHY BUILD', 150, 'w'), ('A TOWER?', 185, 'y')], '#050a22', 900, '#0a1626')


# ================= short4 =================
def make_4():
    rnd = random.Random(404)
    d = FILTERS + VIG(.8)
    d += lin('bg', [(0, '#1a0e08'), (.5, '#3a2210'), (1, '#0a0604')])
    d += halo('h4', 540, 520, 520, inner='#ffd890', outer='#ff9a40')
    d += rad('cave', 1250, 760, 260, [(0, '#ffc870', .9), (.5, '#c87a3a', .45), (1, '#4a2a14', 0)])
    d += lin('bark', [(0, '#6a5644'), (.4, '#a08a68'), (1, '#3a2c20')], x2=1, y2=0)
    b = f'<rect width="{W}" height="{H}" fill="url(#bg)"/>'
    # pillar flank filling the top half (the cut-away window sits in it)
    dd, oo, *_ = pillar('b4m', 540, HZ + 40, 760, 470, 440, 0, rnd, [(0, '#3a3024'), (.25, '#8a7458'), (.55, '#c8a878'), (.85, '#8a7050'), (1, '#3a2c20')], rim='#ffe8b0', rim_side=-1, detail=2.6)
    d += dd; b += oo
    b += f'<ellipse cx="540" cy="520" rx="520" ry="520" fill="url(#h4)"/>'
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
    for w, c, op in ((30, '#fff0c8', .7), (22, '#3a1e0c', 1), (11, '#6a3a1a', .7)):
        for t_ in tun:
            inner += f'<path d="{t_}" fill="none" stroke="{c}" stroke-width="{w}" opacity="{op}" stroke-linecap="round"/>'
    for (x, y, rx_, ry_) in ch:
        inner += f'<ellipse cx="{x}" cy="{y}" rx="{rx_ + 8}" ry="{ry_ + 8}" fill="#fff0c8" opacity=".6"/><ellipse cx="{x}" cy="{y}" rx="{rx_}" ry="{ry_}" fill="#4a240e" stroke="#2a1206" stroke-width="3"/>'
        inner += f'<ellipse cx="{x}" cy="{y}" rx="{rx_ * .8:.0f}" ry="{ry_ * .7:.0f}" fill="#ffb860" opacity=".35" filter="url(#b8)"/>'
    inner += millipede(1196, 874, .62, -2, rnd, col='#6a3a1e', hi='#e09858') + springtail(1320, 652, 2.0) + springtail(1384, 800, 1.7, -1) + trigono(1150, 660, 1.6)
    inner += f'<path d="{cut}" fill="none" stroke="#2a1408" stroke-width="30" opacity=".45" filter="url(#b8)"/>'
    sc, wx, wy = 1.5, 540, 520
    b += f'<ellipse cx="{wx}" cy="{wy}" rx="330" ry="350" fill="#ffd890" opacity=".35" filter="url(#b26)"/>'
    b += (f'<g transform="translate({wx} {wy}) scale({sc}) translate(-1258 -761)"><g clip-path="url(#cw)">{inner}</g>'
          f'<path d="{cut}" fill="none" stroke="#2a1608" stroke-width="7"/><path d="{cut}" fill="none" stroke="#fff2d0" stroke-width="3" opacity=".8" transform="translate(-4 -4)"/></g>')
    b += spark(wx + 330, wy - 260, 26) + spark(140, 380, 16) + spark(960, 800, 16)
    g, gb = ground(rnd, '#3a2a18', '#120c06', '#ffd890', ['#7a8434', '#62702c', '#8e9a40'], '#e8a84a', n=20)
    d += g; b += gb
    b += millipede(640, 1700, .9, -170, rnd, col='#5a3420', hi='#d08a52') + springtail(930, 1740, 1.8, -1)
    b += fireflies(40, 120, 1800, col='#ffd890', core='#fff4d0', seed=41)
    bib = ('<path d="M-22 -30 Q6 -22 34 -30 L30 2 Q6 10 -18 2Z" fill="#fff8f0" stroke-width="3"/><path d="M-14 -20 L26 -20 M-12 -8 L24 -8" stroke="#e05a4a" stroke-width="3"/>')
    fork = ('<g transform="translate(72 -86) rotate(14)"><rect x="-3" y="0" width="6" height="56" rx="3" fill="#cfd6e0" stroke-width="2.4"/>'
            '<path d="M-10 0 L-10 -24 M-3 0 L-3 -26 M3 0 L3 -26 M10 0 L10 -24 M-10 0 Q0 8 10 0" fill="none" stroke="#cfd6e0" stroke-width="3.4"/></g>')
    b += '<circle cx="230" cy="1690" r="170" fill="#fff0c0" opacity=".2" filter="url(#b50)"/>'
    b += frog(230, 1780, 2.3, rot=3, look=(5, -5), mouth='O', shadow=True, mid=bib, armL='M-34 -22 q-18 6 -20 24', armR='M38 -22 q22 -10 34 -34', front=fork)
    return finish(d, b, [('A HOME AND', 140, 'w'), ('A MEAL?', 205, 'y')], '#1a0e08', 890, '#1a0c04')


# ================= short5 =================
def make_5():
    rnd = random.Random(505)
    d = FILTERS + VIG(.75)
    d += lin('sky', [(0, '#05160c'), (.5, '#0e3a24'), (.9, '#2a6a3e'), (1, '#4a8a50')])
    d += halo('h5', 540, 450, 540, inner='#e8ffc0', outer='#5ad08a')
    b = f'<rect width="{W}" height="{HZ + 4}" fill="url(#sky)"/><ellipse cx="540" cy="450" rx="540" ry="540" fill="url(#h5)"/>'
    for k in range(7):
        x = 70 + k * 160
        b += f'<path d="M{x} -20 L{x + 60} {HZ} L{x + 100} {HZ}Z" fill="#d8ffb8" opacity=".05"/>'
    g, gb = ground(rnd, '#26402a', '#0a1a0e', '#bff0a8', ['#3a7a4a', '#4a8a56', '#2e6a3c'], '#d8e070', n=24)
    d += g; b += gb
    # tall Archaeopteris: trunk + fronds
    tx0, tb, th = 760, HZ + 12, 600
    b += f'<path d="M{tx0 - 34} {tb} Q{tx0 - 24} {tb - th * .5} {tx0 - 16} {tb - th} L{tx0 + 16} {tb - th} Q{tx0 + 26} {tb - th * .5} {tx0 + 34} {tb}Z" fill="#6a4426" stroke="#1a0e06" stroke-width="4"/>'
    b += f'<path d="M{tx0 - 22} {tb - 20} Q{tx0 - 14} {tb - th * .5} {tx0 - 8} {tb - th}" fill="none" stroke="#c08a58" stroke-width="6" opacity=".7"/>'
    for k in range(7):
        yy = tb - th + k * 40; ang = [-160, -20, -150, -30, -165, -15, -140][k]
        b += frond(tx0, yy + 10, 250 - k * 14, ang, rnd, '#4aa85a', '#9ae070', 5)
    b += frond(tx0, tb - th, 220, -90, rnd, '#58b868', '#b0f080', 5)
    b += f'<ellipse cx="{tx0}" cy="{tb - th + 40}" rx="300" ry="190" fill="#c8ffa0" opacity=".2" filter="url(#b50)"/>'
    # small cracked pillar, falling crown
    dd, oo, C, Wd, _ = pillar('b5p', 270, HZ + 14, 170, 40, 34, 6, rnd, [(0, '#d8d0b0'), (.25, '#a8a088'), (.6, '#7a7262'), (1, '#4a4438')], rim='#e8f0b0', rim_side=1, detail=.9, cap=.6)
    d += dd; b += oo
    cx_, cy_ = C(1)
    b += f'<path d="M{cx_ - 24:.0f} {cy_ + 10:.0f} l12 22 l-8 18 l12 26 M{cx_ + 16:.0f} {cy_ + 6:.0f} l-8 20 l6 16" fill="none" stroke="#1e1a12" stroke-width="3.4"/>'
    kx, ky = cx_ + 20, cy_ - 250
    b += f'<path d="M{cx_ + 4:.0f} {cy_ - 22:.0f} Q{cx_ + 40:.0f} {cy_ - 120:.0f} {kx:.0f} {ky + 70:.0f}" fill="none" stroke="#fff4c0" stroke-width="5" stroke-dasharray="12 12" opacity=".8"/>'
    b += f'<circle cx="{kx:.0f}" cy="{ky:.0f}" r="120" fill="#ffe080" opacity=".42" filter="url(#b26)"/>'
    b += crown(kx, ky, 2.4, -22)
    b += spark(kx - 90, ky - 50, 22, '#fff8c0') + spark(kx + 90, ky + 40, 16, '#fff8c0') + spark(tx0 + 220, 260, 20, '#fffbe6') + spark(130, 760, 14)
    b += fireflies(46, 120, 1800, col='#e8ffb0', core='#ffffff', seed=51)
    leaf = ('<g transform="translate(4 -100) rotate(-10)"><path d="M-40 6 Q-10 -40 40 -10 Q10 18 -40 6Z" fill="#7ab84a" stroke-width="3.2"/>'
            '<path d="M-36 4 Q0 -10 34 -10" fill="none" stroke="#3a6a24" stroke-width="2.4"/></g>')
    b += '<circle cx="250" cy="1690" r="170" fill="#e8ffc0" opacity=".16" filter="url(#b50)"/>'
    b += frog(250, 1780, 2.3, rot=4, look=(5, -6), mouth='O', shadow=True, top=leaf, armL='M-34 -22 q-24 -10 -30 -42', armR='M38 -22 q24 -14 30 -46')
    return finish(d, b, [('OUTGROWN', 150, 'w'), ('BY TREES', 200, 'y')], '#05160c', 890, '#081008')


for n, fn in ((1, make_1), (2, make_2), (3, make_3), (4, make_4), (5, make_5)):
    out = os.path.join(VID, f'giant-mold-short{n}', 'thumb'); os.makedirs(out, exist_ok=True)
    for f in ('common.css', 'Fredoka-700.woff2'):
        shutil.copyfile(os.path.join(TOOLS, 'assets', 'thumb_v', f), os.path.join(out, f))
    open(os.path.join(out, 'A.html'), 'w').write(fn())
print('ok')
