import sys, os, math, random
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', 'tools'))
from thumb_lib import *
random.seed(11)
os.chdir(os.path.dirname(os.path.abspath(__file__)))
BLUR = '<filter id="bl"><feGaussianBlur stdDeviation="8"/></filter><filter id="bl2"><feGaussianBlur stdDeviation="24"/></filter><filter id="bl3"><feGaussianBlur stdDeviation="3"/></filter>'


def gear(cx, cy, r, n, dep, rot=0):
    pts = []
    for i in range(n * 4):
        a = math.radians(rot) + 2 * math.pi * i / (n * 4)
        rr = r if (i % 4) in (1, 2) else r - dep
        pts.append(f'{cx + math.cos(a) * rr:.1f} {cy + math.sin(a) * rr:.1f}')
    return 'M' + ' L'.join(pts) + 'Z'


# ======================= A: CAN ANYTHING KNOW EVERYTHING?  (homage: Inception, spinning top on a table while the room dissolves) =======================
TX, TIP = 1340, 935
K = 1.38
d = lin('wall', [(0, '#1a0f0a'), (.6, '#2e1a10'), (1, '#3a2214')])
d += rad('lamp', 1330, 470, 900, [(0, '#ffd9a0', .55), (.3, '#c87a3a', .22), (1, '#000', 0)])
d += rad('void', 1330, 330, 560, [(0, '#bff6ff', .9), (.25, '#3fd0f0', .5), (.6, '#1a4a8a', .25), (1, '#050a1a', 0)])
d += lin('tbl', [(0, '#6a3a1c'), (.25, '#3e2010'), (1, '#120804')])
d += lin('metal', [(0, '#3a3e48'), (.18, '#8a90a0'), (.34, '#f4f6ff'), (.48, '#b8bfcc'), (.7, '#4a505e'), (.9, '#20232c'), (1, '#ffcf8a')], x2=1, y2=0)
d += lin('stem', [(0, '#2a2e38'), (.35, '#e8ecf6'), (.7, '#50566a'), (1, '#ffcf8a')], x2=1, y2=0)
d += rad('sh', TX, TIP + 6, 220, [(0, '#000', .75), (1, '#000', 0)])
d += BLUR
b = '<rect width="1920" height="1080" fill="url(#wall)"/>'
# room: back wall panels + door frames in perspective
for x in (180, 520, 860, 1600, 1840):
    b += f'<rect x="{x}" y="120" width="12" height="680" fill="#120a06" opacity=".6"/>'
b += '<path d="M0 120 H1920" stroke="#4a2c18" stroke-width="10" opacity=".7"/>'
b += '<rect x="1560" y="250" width="240" height="550" fill="#120804" opacity=".7"/><rect x="1575" y="265" width="210" height="535" fill="#24140a"/>'
# dissolving hole in the room: void with probability rings
b += '<rect width="1920" height="1080" fill="url(#void)"/>'
for k in range(1, 9):
    b += f'<circle cx="{TX}" cy="330" r="{k * 62}" fill="none" stroke="#9ff0ff" stroke-width="{4 - k * .3:.1f}" opacity="{.5 - k * .05:.2f}"/>'
# floating wall fragments (cubes) drifting up around the void edge
for _ in range(95):
    a = random.uniform(0, 2 * math.pi); r = random.uniform(330, 760)
    x, y = TX + math.cos(a) * r * 1.15, 330 + math.sin(a) * r * .75
    if x < 760 and y < 600 or y > 780 or x > 1900:
        continue
    s = random.uniform(14, 60) * (1.2 - r / 1000)
    rot = random.uniform(-40, 40)
    lit = random.random()
    b += (f'<g transform="translate({x:.0f} {y:.0f}) rotate({rot:.0f})"><rect x="{-s / 2:.0f}" y="{-s / 2:.0f}" width="{s:.0f}" height="{s:.0f}" fill="#3a2214"/>'
          f'<rect x="{-s / 2:.0f}" y="{-s / 2:.0f}" width="{s:.0f}" height="{s * .25:.0f}" fill="#d8a070" opacity="{.4 + lit * .4:.2f}"/>'
          f'<rect x="{-s / 2:.0f}" y="{-s / 2:.0f}" width="{s:.0f}" height="{s:.0f}" fill="none" stroke="#9ff0ff" stroke-width="2" opacity="{.25 + lit * .4:.2f}"/></g>')
b += '<rect width="1920" height="1080" fill="url(#lamp)"/>'
# table
b += '<path d="M0 790 L1920 770 L1920 1080 L0 1080Z" fill="url(#tbl)"/>'
for k in range(14):
    y = 800 + k * k * 1.6 + k * 4
    b += f'<path d="M0 {y + 6:.0f} C500 {y - 6:.0f} 1100 {y + 10:.0f} 1920 {y - 14:.0f}" stroke="#1e0e06" stroke-width="{2 + k * .3:.1f}" fill="none" opacity=".45"/>'
b += '<path d="M0 790 L1920 770" stroke="#ffcf8a" stroke-width="4" opacity=".7"/>'
b += '<path d="M0 1080 L1920 1080 L1920 960 Q1700 1000 1500 1080Z" fill="#000" opacity=".35"/>'
# reflection of the top on the polished table
b += f'<ellipse cx="{TX}" cy="{TIP + 6}" rx="300" ry="40" fill="url(#sh)"/>'
b += f'<ellipse cx="{TX}" cy="{TIP + 10}" rx="140" ry="16" fill="#bff6ff" opacity=".18" filter="url(#bl)"/>'


def top(dx, rot, op, tint=None):
    g = f'<g transform="translate({TX} {TIP}) scale({K}) translate({-TX} {-TIP}) rotate({rot} {TX} {TIP}) translate({dx} 0)" opacity="{op}">'
    body = (f'M{TX} {TIP} C{TX - 60} {TIP - 60} {TX - 205} {TIP - 120} {TX - 205} {TIP - 200} C{TX - 205} {TIP - 260} {TX - 90} {TIP - 300} {TX} {TIP - 300} '
            f'C{TX + 90} {TIP - 300} {TX + 205} {TIP - 260} {TX + 205} {TIP - 200} C{TX + 205} {TIP - 120} {TX + 60} {TIP - 60} {TX} {TIP}Z')
    if tint:
        return g + f'<path d="{body}" fill="{tint}"/><rect x="{TX - 20}" y="{TIP - 470}" width="40" height="190" rx="14" fill="{tint}"/></g>'
    g += f'<rect x="{TX - 20}" y="{TIP - 470}" width="40" height="190" rx="14" fill="url(#stem)"/>'
    g += f'<ellipse cx="{TX}" cy="{TIP - 470}" rx="20" ry="7" fill="#f4f6ff"/>'
    g += f'<path d="{body}" fill="url(#metal)"/>'
    for yy, rx in ((TIP - 285, 150), (TIP - 250, 192), (TIP - 200, 205), (TIP - 150, 180), (TIP - 95, 112)):
        g += f'<path d="M{TX - rx} {yy} Q{TX} {yy + 26} {TX + rx} {yy}" stroke="#1a1d24" stroke-width="3" fill="none" opacity=".55"/>'
        g += f'<path d="M{TX - rx} {yy + 4} Q{TX} {yy + 30} {TX + rx} {yy + 4}" stroke="#ffffff" stroke-width="1.6" fill="none" opacity=".35"/>'
    g += f'<path d="M{TX + 205} {TIP - 200} C{TX + 205} {TIP - 120} {TX + 60} {TIP - 60} {TX} {TIP}" stroke="#ffcf8a" stroke-width="6" fill="none"/>'
    g += f'<path d="M{TX + 90} {TIP - 300} C{TX + 150} {TIP - 290} {TX + 205} {TIP - 260} {TX + 205} {TIP - 200}" stroke="#ffe6b8" stroke-width="5" fill="none"/>'
    g += f'<path d="M{TX - 120} {TIP - 260} Q{TX - 60} {TIP - 290} {TX - 10} {TIP - 292}" stroke="#ffffff" stroke-width="8" stroke-linecap="round" fill="none" opacity=".75"/>'
    g += f'<path d="M{TX + 15} {TIP - 460} L{TX + 15} {TIP - 300}" stroke="#ffcf8a" stroke-width="4" opacity=".8"/>'
    return g + '</g>'


b += top(0, -9, .22, '#7ff0ff') + top(0, 7, .22, '#7ff0ff')
b += f'<path d="M{TX - 360} {TIP - 320} A370 80 0 0 0 {TX + 360} {TIP - 320}" stroke="#9ff0ff" stroke-width="5" fill="none" opacity=".55" filter="url(#bl3)"/>'
b += top(0, 3, 1)
b += f'<path d="M{TX - 345} {TIP - 240} A360 95 0 0 0 {TX + 165} {TIP - 155}" stroke="#ffffff" stroke-width="4" fill="none" opacity=".7" stroke-linecap="round"/>'
b += f'<path d="M{TX + 205} {TIP - 400} A345 85 0 0 1 {TX + 370} {TIP - 283}" stroke="#ffffff" stroke-width="4" fill="none" opacity=".6" stroke-linecap="round"/>'
b += f'<circle cx="{TX}" cy="{TIP}" r="26" fill="#bff6ff" opacity=".7" filter="url(#bl)"/>'
b += spark(1010, 250, 20) + spark(1720, 180, 18) + spark(1640, 620, 14, op=.7) + spark(980, 680, 14, op=.6)
open('A.html', 'w', encoding='utf-8').write(page('#1a0f0a', svg(d, b), [('CAN ANYTHING', 118, 'w'), ('KNOW', 190, 'w'), ('EVERYTHING?', 150, 'y')], '#0a0402', top=48))

# ======================= B: IT CHANGES WHEN RECORDED  (intuitive: a detector eye over two glowing slits, striped screen) =======================
d = lin('sk', [(0, '#06041a'), (.7, '#120a34'), (1, '#1a0e3e')])
d += lin('wallf', [(0, '#2a2650'), (.5, '#16143a'), (1, '#0a0820')], x2=1, y2=0)
d += lin('flr', [(0, '#140c34'), (1, '#030210')])
d += rad('slitg', 1200, 540, 420, [(0, '#bff6ff', .55), (.4, '#3fd0f0', .2), (1, '#000', 0)])
d += '<linearGradient id="beam" x1="0" y1="0" x2="1" y2="-.3"><stop offset="0" stop-color="#3fd0f0" stop-opacity="0"/><stop offset="1" stop-color="#bff6ff" stop-opacity=".9"/></linearGradient>'
d += rad('eyeg', 1230, 210, 300, [(0, '#ff6a5a', .6), (.4, '#ff3a3a', .2), (1, '#000', 0)])
d += rad('iris', 1230, 222, 70, [(0, '#fff0d0', 1), (.2, '#ffb08a', 1), (.5, '#e0302a', 1), (.85, '#4a0810', 1), (1, '#100004', 1)])
d += lin('house', [(0, '#5a5f78'), (.3, '#2a2e44'), (1, '#0c0e1a')])
d += BLUR
b = '<rect width="1920" height="1080" fill="url(#sk)"/>' + stars(160, 760, 700, '#cfd8ff', .4, 0)
b += '<path d="M0 820 L1920 790 L1920 1080 L0 1080Z" fill="url(#flr)"/>'
for k in range(12):  # floor grid
    b += f'<path d="M{-400 + k * 220} 1080 L{820 + k * 70} 800" stroke="#3a2a7a" stroke-width="2" opacity=".35"/>'
for y in (840, 900, 980):
    b += f'<path d="M0 {y} L1920 {y - 30}" stroke="#3a2a7a" stroke-width="2" opacity=".3"/>'
# screen on the right (receding), with interference stripes
SX0, SX1 = 1560, 1830
b += f'<path d="M{SX0} 150 L{SX1} 90 L{SX1} 860 L{SX0} 800Z" fill="#0c0a24" stroke="#5a58a0" stroke-width="4"/>'
for k in range(13):
    t = k / 12; cx = SX0 + 18 + t * (SX1 - SX0 - 36)
    inten = math.cos((t - .5) * math.pi * 5.5) ** 2 * math.exp(-((t - .5) * 2.2) ** 2)
    top_y, bot_y = 150 - (cx - SX0) * 60 / 320 + 14, 800 + (cx - SX0) * 60 / 320 - 14
    w = 16
    b += f'<path d="M{cx - w:.0f} {top_y:.0f} L{cx + w:.0f} {top_y - 3:.0f} L{cx + w:.0f} {bot_y + 3:.0f} L{cx - w:.0f} {bot_y:.0f}Z" fill="#9ff0ff" opacity="{inten * .95:.2f}"/>'
    b += f'<rect x="{cx - w * 2:.0f}" y="{top_y:.0f}" width="{w * 4}" height="{bot_y - top_y:.0f}" fill="#3fd0f0" opacity="{inten * .35:.2f}" filter="url(#bl)"/>'
for _ in range(220):  # electron dots
    t = random.random(); inten = math.cos((t - .5) * math.pi * 5.5) ** 2 * math.exp(-((t - .5) * 2.2) ** 2)
    if random.random() < inten:
        x = SX0 + 18 + t * (SX1 - SX0 - 36) + random.gauss(0, 4)
        b += f'<circle cx="{x:.0f}" cy="{random.uniform(180, 780):.0f}" r="2.6" fill="#ffffff" opacity=".85"/>'
# waves from the slits to the screen
for k in range(1, 9):
    for sy in (430, 650):
        b += f'<path d="M{1310 + k * 38} {sy - k * 40} A{k * 44} {k * 46} 0 0 1 {1110 + k * 38} {sy + k * 40}" stroke="#7fe8ff" stroke-width="3" fill="none" opacity="{.6 - k * .05:.2f}"/>'
# incoming beam from the electron gun (lower left)
b += '<path d="M470 760 L1160 590 L1160 470 L470 730Z" fill="url(#beam)" filter="url(#bl3)"/>'
b += '<path d="M470 745 L1160 540" stroke="#ffffff" stroke-width="3" opacity=".8"/>'
for k in range(9):
    t = k / 9; b += f'<circle cx="{470 + t * 690:.0f}" cy="{745 - t * 205:.0f}" r="{5 + t * 3:.0f}" fill="#ffffff" opacity="{.4 + t * .5:.2f}"/>'
# gun
b += '<g transform="rotate(-21 430 760)"><rect x="250" y="720" width="190" height="84" rx="14" fill="url(#house)" stroke="#8a90b0" stroke-width="3"/><rect x="430" y="738" width="40" height="48" rx="6" fill="#3a3e58"/><rect x="250" y="720" width="190" height="16" rx="8" fill="#a8b0d8" opacity=".5"/><circle cx="470" cy="762" r="14" fill="#bff6ff"/></g>'
b += '<circle cx="472" cy="752" r="40" fill="#3fd0f0" opacity=".4" filter="url(#bl)"/>'
# barrier wall with two slits (front face + side for depth)
b += '<rect width="1920" height="1080" fill="url(#slitg)"/>'
WX = 1210
b += f'<path d="M{WX} 250 L{WX + 90} 226 L{WX + 90} 884 L{WX} 908Z" fill="#0c0a24"/>'
b += f'<path d="M{WX - 70} 266 L{WX} 250 L{WX} 908 L{WX - 70} 892Z" fill="url(#wallf)"/>'
b += ''.join(f'<circle cx="{WX - 52 + (k % 2) * 34}" cy="{300 + k * 76}" r="4" fill="#8a90c8" opacity=".6"/>' for k in range(8))
b += f'<path d="M{WX} 250 L{WX + 70} 230" stroke="#bfc6ff" stroke-width="3" opacity=".7"/>'
for sy in (430, 650):
    b += f'<rect x="{WX - 40}" y="{sy - 75}" width="80" height="150" rx="10" fill="#3fd0f0" opacity=".8" filter="url(#bl)"/>'
    b += f'<path d="M{WX - 50} {sy - 62} L{WX - 22} {sy - 68} L{WX - 22} {sy + 60} L{WX - 50} {sy + 66}Z" fill="#e8fdff"/>'
    b += f'<path d="M{WX - 22} {sy - 68} L{WX} {sy - 72} L{WX} {sy + 56}" stroke="#7fe8ff" stroke-width="3" fill="none"/>'
# detector eye above, with a red scanning cone onto the slits
b += f'<path d="M1230 280 L{WX - 90} 730 L{WX + 60} 730Z" fill="#ff4a3a" opacity=".12"/>'
b += f'<path d="M1230 280 L{WX - 80} 720" stroke="#ff7a6a" stroke-width="2" opacity=".5"/><path d="M1230 280 L{WX + 50} 720" stroke="#ff7a6a" stroke-width="2" opacity=".5"/>'
b += '<rect width="1920" height="1080" fill="url(#eyeg)"/>'
b += '<path d="M1230 0 L1230 110" stroke="#2a2e44" stroke-width="22"/><path d="M1222 0 L1222 110" stroke="#8a90b0" stroke-width="3"/>'
b += '<path d="M1110 150 Q1230 80 1350 150 L1340 250 Q1230 300 1120 250Z" fill="url(#house)" stroke="#9aa0c8" stroke-width="3"/>'
b += '<ellipse cx="1230" cy="225" rx="98" ry="64" fill="#06040c" stroke="#bfc6ff" stroke-width="4"/>'
b += '<ellipse cx="1230" cy="225" rx="82" ry="52" fill="#1a0a14"/>'
b += '<circle cx="1230" cy="228" r="46" fill="url(#iris)"/><circle cx="1230" cy="230" r="17" fill="#080004"/>'
b += '<ellipse cx="1210" cy="210" rx="14" ry="9" fill="#ffffff" opacity=".9"/><ellipse cx="1252" cy="246" rx="6" ry="4" fill="#ffffff" opacity=".6"/>'
b += '<path d="M1118 168 Q1230 104 1342 168" stroke="#e8ecff" stroke-width="3" fill="none" opacity=".6"/>'
b += '<circle cx="1330" cy="140" r="7" fill="#ff5a4a"/><circle cx="1330" cy="140" r="16" fill="#ff5a4a" opacity=".4" filter="url(#bl3)"/>'
b += spark(1460, 120, 18) + spark(1880, 40, 14, op=.7) + spark(880, 540, 14, op=.6)
open('B.html', 'w', encoding='utf-8').write(page('#06041a', svg(d, b), [('IT CHANGES', 140, 'w'), ('WHEN', 150, 'w'), ('RECORDED', 175, 'y')], '#03020c', top=44))

# ======================= C: CLOCKWORK OR DICE?  (intuitive: a glowing die of light bursting up out of brass clockwork) =======================
d = lin('sk', [(0, '#0a0614'), (.6, '#160c26'), (1, '#1c1022')])
d += rad('burst', 1300, 420, 760, [(0, '#f2e6ff', .7), (.2, '#b88aff', .35), (.55, '#4a2a8a', .12), (1, '#000', 0)])
d += lin('brass', [(0, '#fff0b8'), (.25, '#d8a84a'), (.6, '#8a5a1c'), (1, '#2a1606')], x2=.6, y2=1)
d += lin('brass2', [(0, '#c89a40'), (.5, '#6a4214'), (1, '#1e1004')], x2=.6, y2=1)
d += lin('df', [(0, '#ffffff'), (.5, '#e6d8ff'), (1, '#a888ff')], x2=.3, y2=1)
d += lin('dl', [(0, '#c8b0ff'), (1, '#6a48d8')], x2=1, y2=1)
d += lin('dr', [(0, '#8a68f0'), (1, '#3a1e9a')], x2=1, y2=1)
d += BLUR
b = '<rect width="1920" height="1080" fill="url(#sk)"/>' + stars(180, 900, 600, '#efe4ff', .5, 0)
b += '<rect width="1920" height="1080" fill="url(#burst)"/>'
# light rays from the die
for k in range(16):
    a = math.radians(k * 22.5 + 8)
    b += f'<path d="M1300 420 L{1300 + math.cos(a - .05) * 900:.0f} {420 + math.sin(a - .05) * 900:.0f} L{1300 + math.cos(a + .05) * 900:.0f} {420 + math.sin(a + .05) * 900:.0f}Z" fill="#e6d8ff" opacity=".05"/>'
# clockwork (back gears darker, front gears lit)
GEARS = [(1520, 990, 170, 18, 26, 4, 'brass2'), (900, 1000, 210, 20, 28, 9, 'brass2'), (1270, 960, 330, 30, 34, 0, 'brass'), (1660, 760, 140, 16, 24, 6, 'brass2'), (900, 760, 130, 14, 22, 10, 'brass')]
for cx, cy, r, n, dep, rot, fill in GEARS:
    b += f'<path d="{gear(cx + 10, cy + 14, r, n, dep, rot)}" fill="#000" opacity=".5" filter="url(#bl3)"/>'
    b += f'<path d="{gear(cx, cy, r, n, dep, rot)}" fill="url(#{fill})" stroke="#2a1606" stroke-width="3"/>'
    b += f'<circle cx="{cx}" cy="{cy}" r="{r * .72:.0f}" fill="none" stroke="#3a2008" stroke-width="5" opacity=".7"/>'
    b += f'<circle cx="{cx}" cy="{cy}" r="{r * .72 - 4:.0f}" fill="none" stroke="#ffe6a0" stroke-width="2" opacity=".5"/>'
    for s in range(6):  # spokes as cut-outs
        a = math.radians(s * 60 + rot * 3)
        b += f'<path d="M{cx + math.cos(a) * r * .18:.0f} {cy + math.sin(a) * r * .18:.0f} L{cx + math.cos(a) * r * .66:.0f} {cy + math.sin(a) * r * .66:.0f}" stroke="#140a04" stroke-width="{r * .12:.0f}" opacity=".55" stroke-linecap="round"/>'
    b += f'<circle cx="{cx}" cy="{cy}" r="{r * .16:.0f}" fill="#3a2008"/><circle cx="{cx}" cy="{cy}" r="{r * .08:.0f}" fill="#ffe6a0"/>'
    b += f'<path d="{gear(cx, cy, r, n, dep, rot)}" fill="none" stroke="#f0d8ff" stroke-width="2.5" opacity=".45" transform="translate(-3 -4)" clip-path="none"/>'
# a hand-like pendulum/escapement hint: clock hands on the big gear
b += '<path d="M1270 960 L1270 720" stroke="#1a0e04" stroke-width="16" stroke-linecap="round"/><path d="M1270 960 L1420 880" stroke="#1a0e04" stroke-width="12" stroke-linecap="round"/>'
b += '<path d="M1264 955 L1264 725" stroke="#ffe6a0" stroke-width="3" opacity=".7"/>'
# cracks of light breaking out of the clockwork under the die
for x2, y2 in ((1200, 700), (1380, 690), (1300, 640), (1150, 760), (1450, 760)):
    b += f'<path d="M1300 800 L{x2} {y2}" stroke="#f2e6ff" stroke-width="5" opacity=".8" filter="url(#bl3)"/><path d="M1300 800 L{x2} {y2}" stroke="#ffffff" stroke-width="2"/>'
# floating gear teeth / screws flung out
for _ in range(26):
    x, y = random.uniform(980, 1680), random.uniform(160, 700)
    if abs(x - 1300) < 230 and abs(y - 420) < 230:
        continue
    s = random.uniform(6, 16); r = random.uniform(0, 90)
    b += f'<rect x="{x:.0f}" y="{y:.0f}" width="{s:.0f}" height="{s * .7:.0f}" fill="#d8a84a" transform="rotate({r:.0f} {x:.0f} {y:.0f})" opacity=".85"/>'
# the die (isometric cube of light)
DX, DY, S = 1300, 420, 190
top_ = [(DX, DY - S), (DX + S * .87, DY - S * .5), (DX, DY), (DX - S * .87, DY - S * .5)]
left = [(DX - S * .87, DY - S * .5), (DX, DY), (DX, DY + S), (DX - S * .87, DY + S * .5)]
right = [(DX, DY), (DX + S * .87, DY - S * .5), (DX + S * .87, DY + S * .5), (DX, DY + S)]
P = lambda q: 'M' + ' L'.join(f'{x:.0f} {y:.0f}' for x, y in q) + 'Z'
b += f'<circle cx="{DX}" cy="{DY + 20}" r="300" fill="#c8a8ff" opacity=".45" filter="url(#bl2)"/>'
b += f'<g transform="rotate(-12 {DX} {DY})">'
b += f'<path d="{P(top_)}" fill="url(#df)"/><path d="{P(left)}" fill="url(#dl)"/><path d="{P(right)}" fill="url(#dr)"/>'
b += f'<path d="{P(top_)}" fill="none" stroke="#ffffff" stroke-width="5" stroke-linejoin="round"/>'
b += f'<path d="M{DX} {DY} L{DX} {DY + S}" stroke="#ffffff" stroke-width="4" opacity=".8"/>'
b += f'<path d="{P(left)}" fill="none" stroke="#f2e6ff" stroke-width="3" opacity=".7"/><path d="{P(right)}" fill="none" stroke="#f2d27a" stroke-width="4" opacity=".7"/>'


def pip(u, v, face, r):
    if face == 't':
        x = DX + (u - v) * S * .87 * .5 * 2 - 0; y = DY - S + (u + v) * S * .5
        x = DX + (u - v) * S * .87; y = DY - S + (u + v) * S * .5
        return f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{r * 1.1:.0f}" ry="{r * .62:.0f}" fill="#2a1060"/><ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{r * 1.1 + 6:.0f}" ry="{r * .62 + 4:.0f}" fill="#f2d27a" opacity=".25"/>'
    if face == 'l':
        x = DX - S * .87 + u * S * .87; y = DY - S * .5 + u * S * .5 + v * S
    else:
        x = DX + u * S * .87; y = DY + v * S - u * S * .5 + 0
        y = DY + v * S - u * S * .5
    return f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{r * .62:.0f}" ry="{r:.0f}" fill="#fff6d6"/><ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{r * 1.3:.0f}" ry="{r * 1.8:.0f}" fill="#fff6d6" opacity=".3" filter="url(#bl3)"/>'


b += pip(.5, .5, 't', 22)
for u, v in ((.25, .25), (.75, .75), (.5, .5)):
    b += pip(u, v, 'l', 15)
for u, v in ((.25, .25), (.75, .25), (.5, .5), (.25, .75), (.75, .75)):
    b += pip(u, v, 'r', 13)
b += '</g>'
b += f'<path d="M{DX - 120} {DY - 150} Q{DX - 40} {DY - 210} {DX + 60} {DY - 190}" stroke="#ffffff" stroke-width="10" stroke-linecap="round" fill="none" opacity=".55"/>'
# motion arcs (tumbling)
b += f'<path d="M{DX - 300} {DY + 60} A310 260 0 0 1 {DX - 60} {DY - 280}" stroke="#e6d8ff" stroke-width="5" fill="none" opacity=".5" stroke-linecap="round"/>'
b += f'<path d="M{DX + 290} {DY - 40} A310 260 0 0 1 {DX + 80} {DY + 260}" stroke="#e6d8ff" stroke-width="5" fill="none" opacity=".4" stroke-linecap="round"/>'
b += '<path d="M1640 1080 L1920 1080 L1920 900 Q1780 980 1640 1080Z" fill="#000" opacity=".35"/>'
b += spark(1660, 200, 22) + spark(960, 330, 16, op=.7) + spark(1760, 470, 14, op=.7) + spark(1080, 640, 14)
open('C.html', 'w', encoding='utf-8').write(page('#0a0614', svg(d, b), [('CLOCKWORK', 165, 'w'), ('OR', 130, 'w'), ('DICE?', 260, 'y')], '#06030c', top=44))
print('ok')
