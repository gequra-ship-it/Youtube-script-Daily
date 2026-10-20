import sys, os, math, random
TOOLS = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', 'tools')
sys.path.insert(0, TOOLS)
from thumb_lib import *
from hands import hand
from body import arm, P
os.chdir(os.path.dirname(os.path.abspath(__file__)))
FX = ('<filter id="bl"><feGaussianBlur stdDeviation="8"/></filter><filter id="bl2"><feGaussianBlur stdDeviation="26"/></filter>'
      '<filter id="bl3"><feGaussianBlur stdDeviation="3"/></filter><filter id="bl5"><feGaussianBlur stdDeviation="60"/></filter>')


def rock_blobs(n, x0, y0, x1, y1, cols, rmin, rmax, op=(.2, .6)):
    o = ''
    for _ in range(n):
        x, y = random.uniform(x0, x1), random.uniform(y0, y1); r = random.uniform(rmin, rmax)
        o += f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{r:.0f}" ry="{r * random.uniform(.35, .7):.0f}" fill="{random.choice(cols)}" opacity="{random.uniform(*op):.2f}" transform="rotate({random.uniform(-20, 20):.0f} {x:.0f} {y:.0f})"/>'
    return o


# ======================= A: IS IT ALL A PROJECTION?  (homage: Plato's cave — a figure facing a wall that shows a deep world as a flat projection) =======================
random.seed(3)
d = lin('cave', [(0, '#0a0607'), (.55, '#1a100c'), (1, '#0c0706')])
d += lin('flrA', [(0, '#2a1a12'), (.4, '#140c08'), (1, '#060403')])
d += rad('fire', 300, 960, 700, [(0, '#ffb45a', .75), (.25, '#e0702a', .32), (.6, '#6a2a10', .1), (1, '#000', 0)])
d += rad('wallglow', 1340, 440, 900, [(0, '#7fe8ff', .45), (.4, '#2a7aa8', .18), (1, '#000', 0)])
d += '<linearGradient id="beamA" gradientUnits="userSpaceOnUse" x1="330" y1="880" x2="1500" y2="420"><stop offset="0" stop-color="#ffd9a0" stop-opacity=".55"/><stop offset=".5" stop-color="#ffe9c8" stop-opacity=".16"/><stop offset="1" stop-color="#bff6ff" stop-opacity=".08"/></linearGradient>'
# projected scene gradients (local wall coords 0..980 x 0..660)
d += lin('psky', [(0, '#081436'), (.5, '#1a2a6a'), (1, '#3a5aa0')])
d += rad('door', 490, 300, 220, [(0, '#fff6d6', 1), (.25, '#ffd98a', .8), (.6, '#f2a04a', .25), (1, '#000', 0)])
d += rad('pl', 690, 150, 150, [(0, '#ffe6b0', 1), (.45, '#e09a5a', 1), (.85, '#6a3a4a', 1), (1, '#2a1a3a', 1)])
d += lin('pfloor', [(0, '#3a4a8a'), (1, '#0a1230')])
d += '<mask id="wallclip" maskUnits="userSpaceOnUse" x="-200" y="-200" width="1400" height="1100"><rect x="40" y="40" width="900" height="580" rx="60" fill="#fff" filter="url(#bl2)"/></mask>'
d += rad('figrimA', 760, 820, 220, [(0, '#bff6ff', .0), (1, '#bff6ff', 0)])
d += FX
b = '<rect width="1920" height="1080" fill="url(#cave)"/>'
b += rock_blobs(70, 0, 0, 1920, 820, ['#2a1a12', '#1e120c', '#3a2418', '#0a0605'], 40, 160, (.25, .6))
# cave ceiling overhang (darker band at the top, ragged edge) + stalactites on the right
pts = ' '.join(f'L{x} {60 + 40 * math.sin(x / 90) + random.uniform(-14, 14):.0f}' for x in range(0, 1960, 40))
b += f'<path d="M0 0 {pts} L1920 0Z" fill="#050303" opacity=".85"/>'
for x in (1180, 1310, 1460, 1620, 1760, 1880):
    h = random.randint(40, 90)
    b += f'<path d="M{x - 26} 60 Q{x} {60 + h * 1.4} {x + 4} {60 + h * 1.6} Q{x + 8} {60 + h * 1.4} {x + 26} 60Z" fill="#0a0605"/><path d="M{x + 12} 66 Q{x + 8} {60 + h} {x + 5} {60 + h * 1.5}" stroke="#5ac8e8" stroke-width="2" fill="none" opacity=".35"/>'
b += '<rect width="1920" height="1080" fill="url(#wallglow)"/>'
# floor
b += '<path d="M0 840 Q500 800 960 815 T1920 800 L1920 1080 L0 1080Z" fill="url(#flrA)"/>'
b += rock_blobs(40, 0, 850, 1920, 1080, ['#0a0605', '#2a1a12', '#3a2418'], 10, 50, (.4, .8))
b += '<path d="M600 820 Q1100 790 1840 800" stroke="#7fe8ff" stroke-width="3" fill="none" opacity=".25"/>'
# light beam from the fire to the wall
b += '<path d="M330 880 L850 130 L1830 91 L1830 751Z" fill="url(#beamA)"/>'
for _ in range(70):   # dust motes in the beam
    t = random.random(); s = random.random()
    x = 330 + t * (1300 * s + 520 * (1 - s)); y = 880 - t * (800 * (1 - s) + 300 * s) + random.uniform(-30, 30)
    b += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{random.choice([1.5, 2, 3])}" fill="#fff0d0" opacity="{random.uniform(.2, .7):.2f}"/>'
# ---- the wall: a deep 3D world shown as a flat projection ----
W = ''
W += '<rect width="980" height="660" fill="url(#psky)"/>'
for _ in range(90):
    W += f'<circle cx="{random.uniform(0, 980):.0f}" cy="{random.uniform(0, 330):.0f}" r="{random.choice([1.2, 1.8, 2.6])}" fill="#e8f4ff" opacity="{random.uniform(.3, .9):.2f}"/>'
W += '<ellipse cx="300" cy="120" rx="260" ry="70" fill="#8a5ad0" opacity=".25" filter="url(#bl2)"/>'
# ringed planet
W += '<ellipse cx="690" cy="150" rx="215" ry="40" fill="none" stroke="#f2d27a" stroke-width="10" opacity=".55" transform="rotate(-14 690 150)"/>'
W += '<circle cx="690" cy="150" r="110" fill="url(#pl)"/>'
for k, yy in enumerate((105, 135, 165, 195)):
    W += f'<path d="M{600 + k * 4} {yy} Q690 {yy + 14} {785 - k * 6} {yy - 6}" stroke="#7a3a2a" stroke-width="7" fill="none" opacity=".35"/>'
W += '<path d="M600 210 A110 110 0 0 0 790 130" stroke="#2a1a3a" stroke-width="40" fill="none" opacity=".35"/>'
W += '<path d="M475 150 A215 40 0 0 0 905 150" stroke="#ffe9a8" stroke-width="10" fill="none" opacity=".85" transform="rotate(-14 690 150)"/>'
# horizon + receding checker floor toward the vanishing point (490, 330)
VX, VY = 490, 330
W += f'<path d="M0 {VY} L980 {VY} L980 660 L0 660Z" fill="url(#pfloor)"/>'
for k in range(-14, 15):
    W += f'<path d="M{VX} {VY} L{VX + k * 110} 660" stroke="#9fd8ff" stroke-width="2" opacity=".35"/>'
for k in range(1, 12):
    y = VY + (660 - VY) * (k / 11) ** 2.2
    W += f'<path d="M0 {y:.0f} L980 {y:.0f}" stroke="#9fd8ff" stroke-width="2" opacity="{.15 + k * .025:.2f}"/>'
# columns receding on both sides
for k in range(6):
    t = 1 - k / 6; s = .25 + .75 * t
    for side in (-1, 1):
        x = VX + side * (60 + 380 * t ** 1.3); top = VY - 260 * s; bot = VY + 300 * s * .9
        w = 46 * s
        W += f'<rect x="{x - w / 2:.0f}" y="{top:.0f}" width="{w:.0f}" height="{bot - top:.0f}" fill="#24306a"/>'
        W += f'<rect x="{x - w / 2 + (0 if side > 0 else w * .62):.0f}" y="{top:.0f}" width="{w * .38:.0f}" height="{bot - top:.0f}" fill="#ffd98a" opacity=".45"/>'
        W += f'<rect x="{x - w * .7:.0f}" y="{top - 10 * s:.0f}" width="{w * 1.4:.0f}" height="{12 * s:.0f}" fill="#3a4a8a"/>'
# glowing door at the vanishing point, stairs rising to it
W += f'<rect width="980" height="660" fill="url(#door)"/>'
W += f'<rect x="{VX - 34}" y="{VY - 96}" width="68" height="100" rx="4" fill="#fff8e0"/>'
N = 13
for k in range(N, -1, -1):
    t = k / N; w = 360 * (1 - .82 * t); y = 650 - 320 * t ** .85; h = 32 * (1 - .75 * t)
    W += f'<path d="M{VX - w / 2:.0f} {y:.0f} L{VX + w / 2:.0f} {y:.0f} L{VX + w / 2:.0f} {y + h:.0f} L{VX - w / 2:.0f} {y + h:.0f}Z" fill="#1a2458"/>'
    W += f'<path d="M{VX - w / 2:.0f} {y:.0f} L{VX + w / 2:.0f} {y:.0f} L{VX + w / 2 - 8 * (1 - t):.0f} {y - h * .45:.0f} L{VX - w / 2 + 8 * (1 - t):.0f} {y - h * .45:.0f}Z" fill="#ffd98a" opacity="{.35 + .5 * t:.2f}"/>'
# the viewer's own shadow cast on the projection
W += '<g fill="#03050c" opacity=".55" filter="url(#bl3)"><circle cx="150" cy="430" r="58"/><path d="M60 660 Q66 520 150 500 Q234 520 240 660Z"/></g>'
# projection cues: scanlines + soft edge vignette + faint rock bumps showing through
W += ''.join(f'<rect y="{y}" width="980" height="2" fill="#000" opacity=".16"/>' for y in range(0, 660, 7))
W += rock_blobs(60, 0, 0, 980, 660, ['#000', '#3a2418'], 20, 120, (.12, .3))
W += ''.join(f'<path d="M{random.uniform(0, 980):.0f} {random.uniform(0, 660):.0f} q{random.uniform(-80, 80):.0f} {random.uniform(10, 60):.0f} {random.uniform(-120, 120):.0f} {random.uniform(40, 120):.0f}" stroke="#000" stroke-width="3" fill="none" opacity=".3"/>' for _ in range(14))
W += '<rect width="980" height="660" fill="none" stroke="#000" stroke-width="110" opacity=".8" filter="url(#bl2)"/>'
b += '<path d="M780 90 Q1300 20 1900 50 L1920 820 Q1300 860 780 840Z" fill="#24303a" opacity=".55" filter="url(#bl2)"/>' + rock_blobs(50, 820, 90, 1880, 800, ['#2a3a48', '#14161c', '#3a4a58'], 30, 110, (.15, .35))
b += '<path d="M850 130 L1830 91 L1830 751 L850 790Z" fill="#7fe8ff" opacity=".35" filter="url(#bl5)"/>'
b += f'<g transform="matrix(1 -.04 0 1 850 130)"><g mask="url(#wallclip)">{W}</g></g>'
# ---- fire (light source, lower left) ----
b += '<rect width="1920" height="1080" fill="url(#fire)"/>'
FXc, FYc = 300, 985
b += f'<ellipse cx="{FXc}" cy="{FYc + 10}" rx="130" ry="24" fill="#000" opacity=".6"/>'
for a, c in ((-14, '#4a2a18'), (16, '#3a2010'), (-2, '#5a3220')):
    b += f'<rect x="{FXc - 110}" y="{FYc - 14}" width="220" height="28" rx="14" fill="{c}" transform="rotate({a} {FXc} {FYc})" stroke="#1a0c06" stroke-width="3"/>'
for k, (s, c) in enumerate(((1, '#e0501a'), (.78, '#f28a2a'), (.55, '#ffc85a'), (.32, '#fff2c8'))):
    b += (f'<path d="M{FXc - 90 * s} {FYc - 6} C{FXc - 110 * s} {FYc - 120 * s} {FXc - 30 * s} {FYc - 150 * s} {FXc - 20 * s} {FYc - 250 * s} '
          f'C{FXc + 10 * s} {FYc - 170 * s} {FXc + 40 * s} {FYc - 200 * s} {FXc + 30 * s} {FYc - 300 * s} '
          f'C{FXc + 110 * s} {FYc - 200 * s} {FXc + 120 * s} {FYc - 90 * s} {FXc + 90 * s} {FYc - 6}Z" fill="{c}"/>')
b += f'<circle cx="{FXc}" cy="{FYc - 110}" r="150" fill="#ffb45a" opacity=".28" filter="url(#bl2)"/>'
for _ in range(16):
    b += f'<circle cx="{FXc + random.uniform(-80, 120):.0f}" cy="{FYc - random.uniform(240, 460):.0f}" r="{random.choice([2, 3, 4])}" fill="#ffd27a" opacity="{random.uniform(.4, .9):.2f}"/>'
# ---- the small viewer, seen from behind (cute proportions, H = head height) ----
H = 76; CX, TOP = 690, 572; p = P['cute']
LN = '#0a0606'; JK = '#1f4a52'; PA = '#262634'; SK = '#c98f63'
hip = TOP + p['height'] * H / 2; feet = TOP + p['height'] * H
fig = f'<ellipse cx="{CX + 70}" cy="{feet + 6:.0f}" rx="110" ry="14" fill="#000" opacity=".55"/>'
for sx in (-1, 1):   # legs + shoes
    fig += f'<rect x="{CX + sx * H * .32 - H * .25:.0f}" y="{hip - 10:.0f}" width="{H * .5:.0f}" height="{feet - hip + 4:.0f}" rx="{H * .2:.0f}" fill="{PA}" stroke="{LN}" stroke-width="3"/>'
    fig += f'<ellipse cx="{CX + sx * H * .34:.0f}" cy="{feet:.0f}" rx="{H * .34:.0f}" ry="{H * .16:.0f}" fill="#1a1414" stroke="{LN}" stroke-width="3"/>'
(lx, ly), (rx_, ry_) = (CX - p['shoulder_w'] * H / 2 + p['arm_w'] * H * .45, TOP + H + p['neck'] * H + .25 * H), (CX + p['shoulder_w'] * H / 2 - p['arm_w'] * H * .45, TOP + H + p['neck'] * H + .25 * H)
fig += arm(lx, ly, H, upper=8, bend=6, bend_dir=-1, name='va', side='L', view='back', sleeve=JK, skin=SK, line=LN, amp=(0, 0))
fig += arm(rx_, ry_, H, upper=-8, bend=6, bend_dir=1, name='vb', side='R', view='back', sleeve=JK, skin=SK, line=LN, amp=(0, 0))
ty0 = TOP + H + p['neck'] * H
fig += f'<path d="M{CX - p["shoulder_w"] * H / 2:.0f} {ty0 + H * .35:.0f} Q{CX - p["shoulder_w"] * H / 2:.0f} {ty0:.0f} {CX:.0f} {ty0:.0f} Q{CX + p["shoulder_w"] * H / 2:.0f} {ty0:.0f} {CX + p["shoulder_w"] * H / 2:.0f} {ty0 + H * .35:.0f} L{CX + H * .7:.0f} {hip + 14:.0f} L{CX - H * .7:.0f} {hip + 14:.0f}Z" fill="{JK}" stroke="{LN}" stroke-width="3" stroke-linejoin="round"/>'
fig += f'<path d="M{CX:.0f} {ty0 + 30:.0f} L{CX:.0f} {hip + 8:.0f}" stroke="{LN}" stroke-width="2" opacity=".5"/>'
fig += f'<path d="M{CX - H * .4:.0f} {ty0 + 4:.0f} Q{CX:.0f} {ty0 + 26:.0f} {CX + H * .4:.0f} {ty0 + 4:.0f}" stroke="#8a9aa0" stroke-width="10" fill="none" stroke-linecap="round"/>'
fig += f'<circle cx="{CX - H * .4:.0f}" cy="{TOP + H * .55:.0f}" r="9" fill="{SK}" stroke="{LN}" stroke-width="3"/><circle cx="{CX + H * .4:.0f}" cy="{TOP + H * .55:.0f}" r="9" fill="{SK}" stroke="{LN}" stroke-width="3"/>'
fig += f'<ellipse cx="{CX}" cy="{TOP + H * .5:.0f}" rx="{H * .42:.0f}" ry="{H * .5:.0f}" fill="#1e1410" stroke="{LN}" stroke-width="3"/>'
fig += f'<path d="M{CX - 14} {TOP + 18} Q{CX} {TOP + 30} {CX + 4} {TOP + 50}" stroke="#4a3426" stroke-width="3" fill="none"/>'
# rim light: cyan from the wall (right), warm from the fire (left)
fig += f'<path d="M{CX + H * .38:.0f} {TOP + 14} Q{CX + H * .46:.0f} {TOP + H * .5:.0f} {CX + H * .34:.0f} {TOP + H * .9:.0f}" stroke="#bff6ff" stroke-width="4" fill="none" stroke-linecap="round"/>'
fig += f'<path d="M{CX + p["shoulder_w"] * H / 2 - 4:.0f} {ty0 + 10:.0f} L{CX + H * .66:.0f} {hip + 8:.0f}" stroke="#bff6ff" stroke-width="4" stroke-linecap="round" opacity=".9"/>'
fig += f'<path d="M{CX - H * .38:.0f} {TOP + 20} Q{CX - H * .46:.0f} {TOP + H * .5:.0f} {CX - H * .36:.0f} {TOP + H * .85:.0f}" stroke="#ffb45a" stroke-width="3" fill="none" stroke-linecap="round" opacity=".8"/>'
fig += f'<path d="M{CX - p["shoulder_w"] * H / 2 + 4:.0f} {ty0 + 14:.0f} L{CX - H * .66:.0f} {hip + 8:.0f}" stroke="#ffb45a" stroke-width="3" stroke-linecap="round" opacity=".7"/>'
b += fig
b += spark(1060, 300, 16, '#e8fdff', .7) + spark(1700, 650, 12, '#e8fdff', .6) + spark(560, 640, 12, '#ffd9a0', .6)
open('A.html', 'w', encoding='utf-8').write(page('#0a0607', svg(d, b), [('IS IT ALL A', 112, 'w'), ('PROJECTION?', 150, 'y')], '#050303', top=110))


# ======================= B: AREA, NOT VOLUME  (intuitive: black hole whose horizon is tiled with glowing patches) =======================
random.seed(21)
BX, BY, R = 1250, 500, 360
d = lin('skB', [(0, '#05030e'), (.6, '#0c0820'), (1, '#140a22')])
d += rad('neb1', 1500, 260, 700, [(0, '#5a2a8a', .45), (.5, '#2a1450', .2), (1, '#000', 0)])
d += rad('neb2', 600, 900, 700, [(0, '#1a4a7a', .35), (1, '#000', 0)])
d += rad('halo', BX, BY, R * 1.9, [(0, '#000', 0), (.5, '#000', 0), (.53, '#ffcf7a', .55), (.62, '#e0702a', .22), (1, '#000', 0)])
d += rad('sph', BX - 80, BY - 90, R * 1.25, [(0, '#141a30'), (.6, '#06080f'), (1, '#000')][0:0] + [(0, '#151c34', 1), (.65, '#05070e', 1), (1, '#000', 1)])
d += '<linearGradient id="diskB" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#e0702a" stop-opacity="0"/><stop offset=".25" stop-color="#ff9a3a" stop-opacity=".7"/><stop offset=".5" stop-color="#fff2c8" stop-opacity="1"/><stop offset=".75" stop-color="#ff9a3a" stop-opacity=".7"/><stop offset="1" stop-color="#e0702a" stop-opacity="0"/></linearGradient>'
d += FX
b = '<rect width="1920" height="1080" fill="url(#skB)"/><rect width="1920" height="1080" fill="url(#neb1)"/><rect width="1920" height="1080" fill="url(#neb2)"/>'
b += blobs(18, 900, 60, 1900, 500, '#7a4ac0', .05, .14, 80, 220)
b += stars(240, 1070, 0, '#e8f0ff', .55, 0)
for x, y, s in ((960, 120, 18), (1720, 160, 22), (1830, 520, 14), (820, 700, 14)):
    b += spark(x, y, s)
# accretion disk behind (tilted), glow halo
b += f'<rect width="1920" height="1080" fill="url(#halo)"/>'
b += f'<g transform="rotate(-12 {BX} {BY})"><ellipse cx="{BX}" cy="{BY}" rx="{R * 2.05:.0f}" ry="{R * .34:.0f}" fill="none" stroke="url(#diskB)" stroke-width="46" opacity=".55" filter="url(#bl)"/>'
b += f'<ellipse cx="{BX}" cy="{BY}" rx="{R * 1.8:.0f}" ry="{R * .28:.0f}" fill="none" stroke="url(#diskB)" stroke-width="14"/>'
b += f'<ellipse cx="{BX}" cy="{BY}" rx="{R * 1.5:.0f}" ry="{R * .22:.0f}" fill="none" stroke="#fff2c8" stroke-width="4" opacity=".6"/></g>'
# sphere body
b += f'<circle cx="{BX}" cy="{BY}" r="{R + 22}" fill="#ffcf7a" opacity=".5" filter="url(#bl2)"/>'
b += f'<circle cx="{BX}" cy="{BY}" r="{R}" fill="url(#sph)"/>'
# the mesh of square patches on the horizon (latitude/longitude tiles on a tilted rotating sphere)
tilt, spin = math.radians(22), math.radians(18)


def sp(lat, lon):
    x = math.cos(lat) * math.sin(lon + spin); y = math.sin(lat); z = math.cos(lat) * math.cos(lon + spin)
    y2 = y * math.cos(tilt) - z * math.sin(tilt); z2 = y * math.sin(tilt) + z * math.cos(tilt)
    return BX + x * R, BY - y2 * R, z2


tiles = ''; grid = ''
NL = 30
for i in range(-NL // 2, NL // 2):
    la0, la1 = math.radians(i * 180 / NL), math.radians((i + 1) * 180 / NL)
    nlon = max(6, int(60 * math.cos((la0 + la1) / 2)))
    for j in range(nlon):
        lo0, lo1 = 2 * math.pi * j / nlon, 2 * math.pi * (j + 1) / nlon
        g = .14   # inset so patches read as separate tiles
        a0, a1 = la0 + (la1 - la0) * g, la1 - (la1 - la0) * g
        b0, b1 = lo0 + (lo1 - lo0) * g, lo1 - (lo1 - lo0) * g
        c = [sp(a0, b0), sp(a0, b1), sp(a1, b1), sp(a1, b0)]
        zc = sum(q[2] for q in c) / 4
        if zc <= 0.02:
            continue
        rim = 1 - zc   # brighter toward the limb (glow), dimmer in the middle so the sphere stays dark
        on = random.random()
        col = '#F2D27A' if on > .88 else '#7fe8ff'
        op = (.06 + .85 * rim ** 2.2) * (1.0 if on > .5 else .4)
        dd = 'M' + ' L'.join(f'{x:.1f} {y:.1f}' for x, y, _ in c) + 'Z'
        tiles += f'<path d="{dd}" fill="{col}" opacity="{op:.2f}"/>'
        grid += f'<path d="{dd}" fill="none" stroke="#bff6ff" stroke-width="1" opacity="{.08 + .45 * rim ** 2:.2f}"/>'
b += f'<g filter="url(#bl3)" opacity=".7">{tiles}</g>{tiles}{grid}'
b += f'<circle cx="{BX}" cy="{BY}" r="{R}" fill="none" stroke="#fff2c8" stroke-width="5" opacity=".9"/>'
b += f'<circle cx="{BX}" cy="{BY}" r="{R + 10}" fill="none" stroke="#ffcf7a" stroke-width="10" opacity=".5" filter="url(#bl)"/>'
b += f'<path d="M{BX - R * .78:.0f} {BY - R * .5:.0f} A{R} {R} 0 0 1 {BX + R * .2:.0f} {BY - R * .96:.0f}" stroke="#ffffff" stroke-width="6" fill="none" opacity=".6" stroke-linecap="round"/>'
# front part of the disk crossing below the equator (thin, so tiles stay visible)
b += f'<g transform="rotate(-12 {BX} {BY})"><path d="M{BX - R * 1.8:.0f} {BY} A{R * 1.8:.0f} {R * .28:.0f} 0 0 0 {BX + R * 1.8:.0f} {BY}" fill="none" stroke="url(#diskB)" stroke-width="12"/>'
b += f'<path d="M{BX - R * 2.05:.0f} {BY} A{R * 2.05:.0f} {R * .34:.0f} 0 0 0 {BX + R * 2.05:.0f} {BY}" fill="none" stroke="url(#diskB)" stroke-width="34" opacity=".35" filter="url(#bl)"/></g>'
# matter dots spiralling in
for s in range(3):
    ph = s * 2.1
    for k in range(40):
        t = k / 40; ang = ph + t * 4.2; rr = R * (2.1 - 1.0 * t)
        x = BX + math.cos(ang) * rr; y = BY + math.sin(ang) * rr * .42 - math.cos(ang) * rr * .1
        if math.hypot(x - BX, y - BY) < R + 6 or y > 860 and x > 1500:
            continue
        b += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{2 + 4 * t:.1f}" fill="#ffe9c0" opacity="{.25 + .65 * t:.2f}"/>'
# small astronaut for scale (lower left of the hole, facing it, rim lit by the glow)
AX, AY, Sc = 610, 800, 1.0
ast = f'<g transform="translate({AX} {AY}) rotate(-12) scale({Sc})">'
ast += '<rect x="-34" y="-30" width="34" height="62" rx="10" fill="#6a7088" stroke="#0a0a12" stroke-width="3"/>'   # backpack
ast += '<path d="M-14 22 Q-30 60 -22 92 L-6 92 Q-2 62 4 34Z" fill="#c8cdd8" stroke="#0a0a12" stroke-width="3"/><path d="M16 26 Q30 58 34 88 L50 84 Q44 54 30 22Z" fill="#b0b6c4" stroke="#0a0a12" stroke-width="3"/>'
ast += '<rect x="-22" y="-30" width="58" height="66" rx="22" fill="#dfe3ec" stroke="#0a0a12" stroke-width="3"/>'
ast += '<path d="M30 -18 Q62 -10 70 -36" stroke="#0a0a12" stroke-width="20" fill="none" stroke-linecap="round"/><path d="M30 -18 Q62 -10 70 -36" stroke="#d4d8e2" stroke-width="14" fill="none" stroke-linecap="round"/><circle cx="72" cy="-40" r="9" fill="#eef0f6" stroke="#0a0a12" stroke-width="3"/>'
ast += '<path d="M-14 -10 Q-28 18 -16 40" stroke="#0a0a12" stroke-width="20" fill="none" stroke-linecap="round"/><path d="M-14 -10 Q-28 18 -16 40" stroke="#c8cdd8" stroke-width="14" fill="none" stroke-linecap="round"/>'
ast += '<circle cx="8" cy="-56" r="34" fill="#eef0f6" stroke="#0a0a12" stroke-width="3"/><path d="M14 -76 Q44 -70 40 -46 Q34 -30 14 -34 Q4 -50 14 -76Z" fill="#f2b45a" stroke="#0a0a12" stroke-width="3"/><path d="M22 -70 Q34 -66 34 -56" stroke="#fff6d6" stroke-width="4" fill="none" stroke-linecap="round"/>'
ast += '<path d="M36 -70 A34 34 0 0 1 40 -40" stroke="#ffcf7a" stroke-width="4" fill="none"/><path d="M36 -28 L36 30" stroke="#ffcf7a" stroke-width="4" stroke-linecap="round"/><path d="M48 24 L54 84" stroke="#ffcf7a" stroke-width="3"/>'
ast += '<path d="M-26 -8 L-26 20" stroke="#5ac8e8" stroke-width="3" opacity=".7"/></g>'
b += f'<circle cx="{AX + 10}" cy="{AY - 10}" r="90" fill="#ffcf7a" opacity=".12" filter="url(#bl2)"/>' + ast
b += f'<path d="M{AX - 40} {AY + 40} Q{AX - 160} {AY + 120} {AX - 330} {AY + 100}" stroke="#9aa0b8" stroke-width="2" fill="none" opacity=".35" stroke-dasharray="6 8"/>'
open('B.html', 'w', encoding='utf-8').write(page('#05030e', svg(d, b), [('AREA,', 200, 'y'), ('NOT', 120, 'w'), ('VOLUME', 170, 'w')], '#05030a', top=60))


# ======================= C: A FLAT CARD = 3D  (intuitive: a hand holds a hologram card, a glowing world floats above it) =======================
random.seed(5)
d = lin('wallC', [(0, '#06131a'), (.6, '#0c2430'), (1, '#12303a')])
d += lin('deskC', [(0, '#2a1a12'), (.3, '#1a0f0a'), (1, '#070403')])
d += rad('holoG', 1180, 470, 620, [(0, '#7fe8ff', .5), (.35, '#2a9ac0', .22), (1, '#000', 0)])
d += rad('lampC', 1820, 0, 900, [(0, '#ffd9a0', .35), (1, '#000', 0)])
d += '<linearGradient id="cone" gradientUnits="userSpaceOnUse" x1="0" y1="790" x2="0" y2="260"><stop offset="0" stop-color="#bff6ff" stop-opacity=".55"/><stop offset="1" stop-color="#7fe8ff" stop-opacity="0"/></linearGradient>'
d += '<linearGradient id="cardC" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#2a3a6a"/><stop offset=".5" stop-color="#14204a"/><stop offset="1" stop-color="#0a1230"/></linearGradient>'
d += '<linearGradient id="foil" x1="0" y1="0" x2="1" y2=".6"><stop offset="0" stop-color="#ff9ad0"/><stop offset=".22" stop-color="#ffe9a8"/><stop offset=".45" stop-color="#9fffd8"/><stop offset=".68" stop-color="#8ad0ff"/><stop offset="1" stop-color="#c8a0ff"/></linearGradient>'
d += rad('plC', 1140, 380, 230, [(0, '#e8fdff', 1), (.35, '#7fe8ff', .95), (.75, '#1a6aa0', .9), (1, '#0a2a50', .85)])
d += FX
# card geometry (a tilted plate seen from above: near edge in the hand, far edge up)
C0 = (880, 880); C1 = (1440, 850); C2 = (1520, 700); C3 = (980, 726)
cpath = f'M{C0[0]} {C0[1]} L{C1[0]} {C1[1]} L{C2[0]} {C2[1]} L{C3[0]} {C3[1]}Z'


def cpt(u, v):   # point on the card: u along the near edge 0..1, v toward the far edge 0..1
    x0 = C0[0] + (C1[0] - C0[0]) * u; y0 = C0[1] + (C1[1] - C0[1]) * u
    x1 = C3[0] + (C2[0] - C3[0]) * u; y1 = C3[1] + (C2[1] - C3[1]) * u
    return x0 + (x1 - x0) * v, y0 + (y1 - y0) * v


fu = [cpt(u, v) for u, v in ((.52, .2), (.9, .2), (.9, .85), (.52, .85))]
foil = 'M' + ' L'.join(f'{x:.0f} {y:.0f}' for x, y in fu) + 'Z'
d += f'<clipPath id="foilclip"><path d="{foil}"/></clipPath>'
b = '<rect width="1920" height="1080" fill="url(#wallC)"/><rect width="1920" height="1080" fill="url(#lampC)"/>'
b += blobs(14, 700, 80, 1900, 700, '#2a6a80', .05, .12, 80, 220)
# shelves/back-room hints for depth
b += '<rect x="1560" y="250" width="360" height="12" fill="#1e3a44"/><rect x="1600" y="196" width="40" height="54" rx="4" fill="#14303a"/><rect x="1650" y="176" width="26" height="74" rx="4" fill="#183844"/><circle cx="1760" cy="226" r="24" fill="#1a3a44"/>'
b += '<rect width="1920" height="1080" fill="url(#holoG)"/>'
b += '<path d="M0 820 L1920 790 L1920 1080 L0 1080Z" fill="url(#deskC)"/><path d="M0 820 L1920 790" stroke="#ffd9a0" stroke-width="3" opacity=".35"/>'
for k in range(10):
    y = 840 + k * k * 2.4 + k * 6
    b += f'<path d="M0 {y:.0f} C600 {y - 8:.0f} 1200 {y + 6:.0f} 1920 {y - 20:.0f}" stroke="#0a0604" stroke-width="2" fill="none" opacity=".5"/>'
b += '<ellipse cx="1190" cy="900" rx="420" ry="60" fill="#7fe8ff" opacity=".18" filter="url(#bl2)"/>'
# light cone rising from the foil to the floating world
fx0, fy0 = cpt(.52, .5); fx1, fy1 = cpt(.9, .5)
b += f'<path d="M{fu[0][0]:.0f} {fu[0][1]:.0f} L{fu[1][0]:.0f} {fu[1][1]:.0f} L1400 380 L880 380Z" fill="url(#cone)"/>'
# hand gripping the near edge of the card + sleeve (from the bottom)
SK, LN = '#d9a37a', '#2a1c14'
HX, HY, HS = 1150, 1095, 185
b += f'<path d="M{HX - 80} 1080 L{HX - 70} {HY - 6} Q{HX} {HY - 26} {HX + 74} {HY - 6} L{HX + 92} 1080Z" fill="#1f4a52" stroke="{LN}" stroke-width="4"/>'
b += f'<path d="M{HX - 70} {HY + 2} Q{HX} {HY - 18} {HX + 76} {HY + 2}" stroke="#2a6a74" stroke-width="10" fill="none"/>'
b += hand(HX, HY, angle=-4, size=HS, side='R', view='palm', pose='flat', skin=SK, line=LN)
b += f'<path d="M{HX + 70} {HY - 120} Q{HX + 82} {HY - 60} {HX + 70} {HY - 10}" stroke="#bff6ff" stroke-width="4" fill="none" opacity=".7"/>'
# card
b += f'<path d="{cpath}" fill="#000" opacity=".5" transform="translate(10 26)" filter="url(#bl)"/>'
b += f'<path d="{cpath}" fill="url(#cardC)" stroke="#bff6ff" stroke-width="4" stroke-linejoin="round"/>'
b += f'<path d="M{C3[0]} {C3[1]} L{C2[0]} {C2[1]}" stroke="#ffffff" stroke-width="5" opacity=".8"/>'
b += f'<path d="M{C0[0]} {C0[1]} L{C1[0]} {C1[1]} L{C1[0]} {C1[1] + 8} L{C0[0]} {C0[1] + 8}Z" fill="#0a0f24"/>'
for u0, v0, u1 in ((.08, .62, .4), (.08, .48, .3), (.08, .3, .44)):   # plain stripes (no lettering)
    a0 = cpt(u0, v0); a1 = cpt(u1, v0)
    b += f'<path d="M{a0[0]:.0f} {a0[1]:.0f} L{a1[0]:.0f} {a1[1]:.0f}" stroke="#5a6aa0" stroke-width="7" stroke-linecap="round" opacity=".7"/>'
b += f'<path d="{foil}" fill="url(#foil)"/>'
rip = ''
for cx_, cy_ in (cpt(.62, .35), cpt(.8, .7)):
    for k in range(1, 20):
        rip += f'<ellipse cx="{cx_:.0f}" cy="{cy_:.0f}" rx="{k * 13}" ry="{k * 5}" fill="none" stroke="{"#ffffff" if k % 2 else "#2a3a8a"}" stroke-width="2.2" opacity=".55"/>'
b += f'<g clip-path="url(#foilclip)">{rip}<path d="M{fu[0][0] - 40:.0f} {fu[0][1]:.0f} L{fu[0][0] + 40:.0f} {fu[0][1]:.0f} L{fu[3][0] + 200:.0f} {fu[3][1] - 40:.0f} L{fu[3][0] + 120:.0f} {fu[3][1] - 40:.0f}Z" fill="#ffffff" opacity=".45"/></g>'
b += f'<path d="{foil}" fill="none" stroke="#ffffff" stroke-width="3" opacity=".9"/>'
b += f'<ellipse cx="{(fx0 + fx1) / 2:.0f}" cy="{fy0:.0f}" rx="140" ry="30" fill="#bff6ff" opacity=".55" filter="url(#bl)"/>'
# floating hologram: a translucent planet with a wireframe grid, a small room-cube orbiting
PX, PY, PR = 1140, 380, 200
b += f'<circle cx="{PX}" cy="{PY}" r="{PR + 40}" fill="#7fe8ff" opacity=".35" filter="url(#bl2)"/>'
b += f'<ellipse cx="{PX}" cy="{PY}" rx="{PR * 1.75:.0f}" ry="{PR * .32:.0f}" fill="none" stroke="#F2D27A" stroke-width="10" opacity=".45" transform="rotate(-10 {PX} {PY})"/>'
b += f'<circle cx="{PX}" cy="{PY}" r="{PR}" fill="url(#plC)" opacity=".92"/>'
for k in range(1, 8):   # latitude lines
    yy = -PR + k * PR * 2 / 8; rx_ = math.sqrt(PR * PR - yy * yy)
    b += f'<ellipse cx="{PX}" cy="{PY + yy:.0f}" rx="{rx_:.0f}" ry="{rx_ * .18:.0f}" fill="none" stroke="#e8fdff" stroke-width="2" opacity=".55"/>'
for k in range(6):   # meridians
    rx_ = PR * abs(math.cos(math.pi * k / 6))
    b += f'<ellipse cx="{PX}" cy="{PY}" rx="{rx_:.0f}" ry="{PR}" fill="none" stroke="#e8fdff" stroke-width="2" opacity=".45"/>'
b += blobs(9, PX - 140, PY - 120, PX + 120, PY + 130, '#e8fdff', .25, .45, 30, 70)
b += f'<path d="M{PX - PR * .7:.0f} {PY - PR * .55:.0f} A{PR} {PR} 0 0 1 {PX + PR * .3:.0f} {PY - PR * .95:.0f}" stroke="#ffffff" stroke-width="8" fill="none" stroke-linecap="round" opacity=".8"/>'
b += f'<path d="M{PX + PR * 1.75 * .99:.0f} {PY - 60} A{PR * 1.75:.0f} {PR * .32:.0f} -10 0 1 {PX - PR * 1.75 * .99:.0f} {PY + 60}" stroke="#ffe9a8" stroke-width="9" fill="none" opacity=".9" transform="rotate(0)"/>'
# small wireframe room cube floating beside the planet
def cube(cx, cy, s):
    f = [(cx - s, cy - s * .2), (cx + s * .6, cy - s * .5), (cx + s * .6, cy + s * 1.1), (cx - s, cy + s * 1.4)]
    o = ''.join(f'<path d="M{a[0]:.0f} {a[1]:.0f} L{c[0]:.0f} {c[1]:.0f}" stroke="#bff6ff" stroke-width="3" opacity=".9"/>' for a, c in zip(f, f[1:] + f[:1]))
    g = [(x + s * .7, y - s * .6) for x, y in f]
    o += ''.join(f'<path d="M{a[0]:.0f} {a[1]:.0f} L{c[0]:.0f} {c[1]:.0f}" stroke="#bff6ff" stroke-width="2" opacity=".55"/>' for a, c in zip(g, g[1:] + g[:1]))
    o += ''.join(f'<path d="M{a[0]:.0f} {a[1]:.0f} L{c[0]:.0f} {c[1]:.0f}" stroke="#bff6ff" stroke-width="2" opacity=".7"/>' for a, c in zip(f, g))
    o += f'<path d="M{f[0][0]:.0f} {f[0][1]:.0f} L{f[1][0]:.0f} {f[1][1]:.0f} L{f[2][0]:.0f} {f[2][1]:.0f} L{f[3][0]:.0f} {f[3][1]:.0f}Z" fill="#7fe8ff" opacity=".18"/>'
    o += f'<rect x="{cx - s * .55:.0f}" y="{cy + s * .3:.0f}" width="{s * .5:.0f}" height="{s * .8:.0f}" fill="#F2D27A" opacity=".8" transform="skewY(-12)" transform-origin="{cx:.0f} {cy:.0f}"/>'
    return o
b += cube(1480, 250, 48)
for _ in range(40):   # light specks rising
    x = random.uniform(fu[0][0] - 60, fu[1][0] + 60); y = random.uniform(420, 760)
    b += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{random.choice([1.6, 2.4, 3.2])}" fill="#e8fdff" opacity="{random.uniform(.3, .85):.2f}"/>'
b += spark(1420, 560, 18, '#e8fdff') + spark(840, 300, 14, '#e8fdff', .7) + spark(1560, 420, 12, '#fff6d6', .7)
open('C.html', 'w', encoding='utf-8').write(page('#06131a', svg(d, b), [('A FLAT', 120, 'w'), ('CARD', 190, 'w'), ('= 3D', 230, 'y')], '#03080c', top=60))
print('ok')
