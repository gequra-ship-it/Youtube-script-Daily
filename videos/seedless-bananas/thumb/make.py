# seedless-bananas thumbnails A-C (guideline 16-6). run: python3 make.py  (writes A.html B.html C.html here)
# A  THE LOST BANANA       homage: Raiders of the Lost Ark idol swap (golden Gros Michel on the pedestal, a hand brings a plain Cavendish)
#    script S04 "a banana that the world largely lost", S18-S25 Gros Michel -> Cavendish (no 'extinct').
# B  NO SEEDS?             intuitive: a supermarket banana cut open (only tiny specks) vs a wild banana packed with hard seeds, magnifier
#    script S02, S06.
# C  SLIGHTLY RADIOACTIVE  intuitive: a glowing banana, a detector needle swinging, a port detector gate with a banana truck behind
#    script S33-S36 ("naturally radioactive. Not dangerously, but measurably", "can set off radiation detectors at ports").
import os, sys, math, random
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', '..', 'tools'))
from thumb_lib import *
from hands import hand


def P(pts):
    return 'M' + ' L'.join(f'{x:.1f},{y:.1f}' for x, y in pts)


def bcurve(L, sag, w, n=48, tail=.10):
    """banana centre line + half thickness; local coords, stem end at -x, tip at +x, middle sags down (+y)"""
    out = []
    for i in range(n + 1):
        u = i / n
        x = L * (u - .5); y = sag * (1 - 4 * (u - .5) ** 2)
        dy = -sag * 8 * (u - .5) / L
        nx, ny = -dy, 1.0; m = math.hypot(nx, ny); nx, ny = nx / m, ny / m
        t = w * (math.sin(math.pi * min(max((u - .02) / .96, 0), 1)) ** .55) * (1 - tail * u)
        out.append((x, y, nx, ny, t))
    return out


def banana(x, y, L, rot=0, sag=None, w=None, gid='b', col=('#fff3a6', '#f2cf3c', '#c98f16'), tip='#3a2a12', stem='#7f8f3a',
           rim='#fff7cf', glow=None, ridge=True, spots=0, seed=1):
    """a whole banana, centre (x, y), length L, rotation deg; returns (defs, svg)"""
    sag = sag if sag is not None else L * .17; w = w if w is not None else L * .085
    C = bcurve(L, sag, w)
    top = [(px - nx * t, py - ny * t) for px, py, nx, ny, t in C]
    bot = [(px + nx * t, py + ny * t) for px, py, nx, ny, t in C]
    body = P(top + bot[::-1]) + 'Z'
    d = (f'<linearGradient id="{gid}g" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{col[0]}"/>'
         f'<stop offset=".45" stop-color="{col[1]}"/><stop offset="1" stop-color="{col[2]}"/></linearGradient>')
    o = f'<g transform="translate({x} {y}) rotate({rot})">'
    if glow:
        o += f'<path d="{body}" fill="none" stroke="{glow}" stroke-width="{w * 1.3:.0f}" opacity=".35" filter="url(#soft)"/>'
    o += f'<path d="{body}" fill="url(#{gid}g)" stroke="#3b2a0c" stroke-width="{max(3, L * .006):.1f}" stroke-linejoin="round"/>'
    if ridge:   # facet ridges along the peel
        for f, op in ((-.42, .55), (.30, .28)):
            o += f'<path d="{P([(px + nx * t * f, py + ny * t * f) for px, py, nx, ny, t in C[3:-3]])}" fill="none" stroke="{col[2]}" stroke-width="{L * .005:.1f}" opacity="{op}"/>'
    # rim light on the upper edge, soft highlight band
    o += f'<path d="{P([(px - nx * t * .80, py - ny * t * .80) for px, py, nx, ny, t in C[6:-8]])}" fill="none" stroke="{rim}" stroke-width="{w * .22:.1f}" stroke-linecap="round" opacity=".75"/>'
    o += f'<path d="{P([(px - nx * t * .25, py - ny * t * .25) for px, py, nx, ny, t in C[10:-12]])}" fill="none" stroke="#ffffff" stroke-width="{w * .12:.1f}" stroke-linecap="round" opacity=".35"/>'
    rnd = random.Random(seed)
    for _ in range(spots):
        px, py, nx, ny, t = C[rnd.randint(8, 40)]; f = rnd.uniform(-.6, .6)
        o += f'<ellipse cx="{px + nx * t * f:.1f}" cy="{py + ny * t * f:.1f}" rx="{rnd.uniform(.006, .014) * L:.1f}" ry="{rnd.uniform(.004, .009) * L:.1f}" fill="#6a4a14" opacity=".55"/>'
    # stem (at -x end) and dark tip (at +x end)
    sx, sy = C[0][0], C[0][1]; ang = math.atan2(C[1][1] - C[0][1], C[1][0] - C[0][0])
    ex, ey = sx - math.cos(ang) * L * .09, sy - math.sin(ang) * L * .09
    o += f'<path d="M{sx:.1f},{sy:.1f} L{ex:.1f},{ey:.1f}" stroke="#3b2a0c" stroke-width="{w * .62:.1f}" stroke-linecap="round"/>'
    o += f'<path d="M{sx:.1f},{sy:.1f} L{ex:.1f},{ey:.1f}" stroke="{stem}" stroke-width="{w * .44:.1f}" stroke-linecap="round"/>'
    o += f'<ellipse cx="{ex:.1f}" cy="{ey:.1f}" rx="{w * .26:.1f}" ry="{w * .30:.1f}" fill="#4a3a1a"/>'
    tx, ty = C[-1][0], C[-1][1]
    o += f'<circle cx="{tx:.1f}" cy="{ty:.1f}" r="{w * .2:.1f}" fill="{tip}"/>'
    o += '</g>'
    return d, o


SOFT = '<filter id="soft" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="18"/></filter>'
BL = '<filter id="bl" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="40"/></filter>'
BL6 = '<filter id="bl6" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="6"/></filter>'


def leaf(x, y, L, rot, col, vein, op=1, filt=''):
    """big banana leaf: long blade with midrib and parallel side veins (torn here and there)"""
    o = f'<g transform="translate({x} {y}) rotate({rot})" opacity="{op}"{filt}>'
    W = L * .17
    o += f'<path d="M0,0 C{L * .2:.0f},{-W:.0f} {L * .8:.0f},{-W:.0f} {L:.0f},0 C{L * .8:.0f},{W:.0f} {L * .2:.0f},{W:.0f} 0,0Z" fill="{col}"/>'
    o += f'<path d="M0,0 L{L:.0f},0" stroke="{vein}" stroke-width="{L * .012:.1f}"/>'
    for k in range(1, 22):
        t = k / 22; px = L * t; hw = W * .75 * math.sin(math.pi * t) ** .7
        o += f'<path d="M{px:.0f},0 l{L * .03:.0f},{-hw:.0f} M{px:.0f},0 l{L * .03:.0f},{hw:.0f}" stroke="{vein}" stroke-width="{L * .003:.1f}" opacity=".55"/>'
    o += '</g>'
    return o


# =========================== A: THE LOST BANANA (Raiders of the Lost Ark: idol on the pedestal) ===========================
random.seed(7)
d = SOFT + BL + BL6
d += lin('aw', [(0, '#0c1710'), (.55, '#16271a'), (1, '#070d09')])
d += lin('afl', [(0, '#2b3a22'), (1, '#0a120b')])
d += rad('ashaft', 1240, 640, 600, [(0, '#fff2b0', .55), (.45, '#f2d27a', .18), (1, '#f2d27a', 0)])
d += rad('ahalo', 1240, 540, 420, [(0, '#fff6c4', .95), (.25, '#ffe27a', .55), (.6, '#f2c23a', .18), (1, '#f2c23a', 0)])
d += rad('atun', 380, 760, 300, [(0, '#3a4a2c', 1), (.6, '#1a2616', 1), (1, '#0c140d', 1)])
d += lin('apil', [(0, '#5a5a3c'), (.35, '#9a9468'), (.6, '#7a7650'), (1, '#2e3020')], x2=1, y2=0)
d += lin('ashaftg', [(0, '#fff7d0'), (1, '#fff7d0')])
d += ('<linearGradient id="ash" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff4c0" stop-opacity=".55"/>'
      '<stop offset=".8" stop-color="#f2d27a" stop-opacity=".16"/><stop offset="1" stop-color="#f2d27a" stop-opacity="0"/></linearGradient>')
d += rad('abld', 420, 720, 170, [(0, '#8a8a62', 1), (.7, '#4a4a32', 1), (1, '#262818', 1)])
H = 880   # floor line
b = '<rect width="1920" height="1080" fill="url(#aw)"/>'
# stone block wall
for r in range(0, 12):
    yy = r * 72 - 10; off = (r % 2) * 90
    for c in range(-1, 12):
        xx = c * 180 + off; sh = random.uniform(.0, .12)
        b += f'<rect x="{xx + 4}" y="{yy + 4}" width="172" height="64" rx="6" fill="#2c3a24" opacity="{.25 + sh:.2f}"/>'
        b += f'<path d="M{xx + 8} {yy + 66} h164" stroke="#050a06" stroke-width="5" opacity=".5"/>'
# carved frieze of banana-leaf reliefs high on the wall
for k in range(9):
    b += leaf(1000 + k * 110, 70, 120, -60, '#3a4a2e', '#24301c', op=.55)
# the dark tunnel on the left with the famous rolling boulder waiting in it
b += '<path d="M110 880 L110 760 Q110 600 380 590 Q650 600 650 760 L650 880Z" fill="url(#atun)" opacity=".9"/>'
b += '<path d="M110 880 L110 760 Q110 600 380 590 Q650 600 650 760 L650 880" fill="none" stroke="#4e5c3a" stroke-width="22"/>'
b += '<path d="M150 880 L150 770 Q150 640 380 632 Q610 640 610 770 L610 880Z" fill="#050906"/>'
b += '<circle cx="380" cy="770" r="160" fill="url(#abld)"/>'
for k in range(14):
    a = random.uniform(0, 6.28); rr = random.uniform(40, 170)
    b += f'<path d="M{380 + math.cos(a) * rr * .85:.0f} {770 + math.sin(a) * rr * .85:.0f} q{random.randint(-30, 30)} {random.randint(-20, 20)} {random.randint(20, 50)} {random.randint(-10, 20)}" stroke="#1a1c10" stroke-width="5" fill="none" opacity=".6"/>'
b += '<path d="M440 625 Q510 650 535 730" stroke="#e8d79a" stroke-width="10" fill="none" opacity=".45" stroke-linecap="round"/>'
b += '<circle cx="380" cy="770" r="160" fill="none" stroke="#0a0c06" stroke-width="6"/>'
# hanging vines and roots
for vx in (90, 150, 790, 860, 1820, 1880):
    pts = []; yy = 0
    while yy < random.randint(300, 620):
        pts.append((vx + 18 * math.sin(yy / 60 + vx), yy)); yy += 20
    b += f'<path d="{P(pts)}" stroke="#2f5a2a" stroke-width="9" fill="none"/>'
    for px, py in pts[2::3]:
        b += f'<ellipse cx="{px + 14:.0f}" cy="{py:.0f}" rx="20" ry="8" transform="rotate(30 {px + 14:.0f} {py:.0f})" fill="#4e8a3a"/>'
# floor
b += f'<rect x="0" y="{H}" width="1920" height="{1080 - H}" fill="url(#afl)"/>'
for k in range(16):
    b += f'<path d="M{k * 140 - 40} {H} L{k * 170 - 360} 1080" stroke="#050a06" stroke-width="5" opacity=".55"/>'
for yy in (920, 990):
    b += f'<path d="M0 {yy} H1920" stroke="#050a06" stroke-width="4" opacity=".45"/>'
# light shaft from a hole in the ceiling onto the pedestal
b += '<path d="M1080 0 L1400 0 L1600 900 L880 900Z" fill="url(#ash)"/>'
b += '<rect width="1920" height="1080" fill="url(#ashaft)"/>'
for _ in range(70):
    yy = random.randint(20, 860); spread = 150 + yy * .22
    b += f'<circle cx="{1240 + random.uniform(-spread, spread):.0f}" cy="{yy}" r="{random.choice([1.5, 2.2, 3])}" fill="#fff4c8" opacity="{random.uniform(.3, .9):.2f}"/>'
# floor pressure tiles + pool of light
b += '<ellipse cx="1240" cy="915" rx="380" ry="54" fill="#f2d27a" opacity=".22"/>'
# pedestal (stepped stone column)
b += '<path d="M1030 950 L1450 950 L1425 895 L1055 895Z" fill="#3a3c28" stroke="#16180e" stroke-width="5"/>'
b += '<rect x="1095" y="650" width="290" height="250" fill="url(#apil)" stroke="#16180e" stroke-width="5"/>'
for yy in (710, 780, 845):
    b += f'<path d="M1100 {yy} h280" stroke="#2e3020" stroke-width="4" opacity=".6"/>'
b += '<path d="M1140 670 l0 220 M1340 670 l0 220" stroke="#ccc690" stroke-width="3" opacity=".35"/>'
b += '<path d="M1060 622 L1420 622 L1395 660 L1085 660Z" fill="#b8b07a" stroke="#16180e" stroke-width="5"/>'
b += '<rect x="1050" y="604" width="380" height="24" rx="4" fill="#e2d9a0" stroke="#16180e" stroke-width="5"/>'
# the golden idol banana (Gros Michel: a little thicker) with halo
b += '<rect width="1920" height="1080" fill="url(#ahalo)"/>'
gd, gb = banana(1268, 505, 470, rot=-5, w=50, sag=84, gid='gold', col=('#fff8c8', '#f2c23a', '#a8700e'), tip='#6a4a10', stem='#c79a2a', rim='#ffffff', glow='#ffe27a')
d += gd
b += '<ellipse cx="1240" cy="604" rx="210" ry="12" fill="#3a2a08" opacity=".5"/>' + gb
for sx, sy, s in ((1060, 400, 24), (1490, 400, 20), (1350, 330, 14), (1130, 320, 14), (1530, 560, 12)):
    b += spark(sx, sy, s, '#fff8d8', .95)
# the swap: a hand from the right brings a plain Cavendish
b += '<path d="M1960 520 L1830 560 Q1810 610 1830 660 L1960 700Z" fill="#6a5034" stroke="#1d140a" stroke-width="5"/>'   # sleeve
b += '<path d="M1830 560 Q1810 610 1830 660" stroke="#3a2a18" stroke-width="10" fill="none"/>'
b += hand(1838, 612, angle=-84, size=130, side='R', view='back', pose='open', skin='#c98f63', line='#2a1c14')
cd, cb = banana(1665, 548, 290, rot=-12, w=30, sag=46, gid='cav', col=('#f4f0a0', '#d9c64a', '#8f8a2a'), tip='#3a3014', stem='#7f9a3a')
d += cd; b += cb
# edge darkening for depth
d += rad('avig', 960, 540, 1150, [(0, '#000', 0), (.6, '#000', 0), (1, '#000', .7)])
b += '<rect width="1920" height="1080" fill="url(#avig)"/>'
open(os.path.join(HERE, 'A.html'), 'w').write(page('#0c1710', svg(d, b), [('THE', 130, 'w'), ('LOST', 250, 'y'), ('BANANA', 205, 'w')], outline='#07100a'))


# =========================== B: NO SEEDS? (cut-open banana vs wild banana packed with seeds) ===========================
random.seed(11)
d = SOFT + BL + BL6
d += lin('bsky', [(0, '#2f6a32'), (.5, '#5c9a3e'), (1, '#9cc25a')], x2=1, y2=.4)
d += rad('bsun', 1650, 120, 900, [(0, '#fff6c8', .85), (.3, '#f2e08a', .35), (1, '#f2e08a', 0)])
d += lin('bwood', [(0, '#c48a4e'), (.4, '#a86c36'), (1, '#5a3518')])
d += lin('bflesh', [(0, '#fffbe6'), (.6, '#f7ecc0'), (1, '#e2cf8a')])
d += lin('bpeel', [(0, '#ffe066'), (.5, '#f0c232'), (1, '#b88412')])
d += lin('bwflesh', [(0, '#f2ead0'), (1, '#cdbb8a')])
d += lin('bwpeel', [(0, '#c9d27a'), (.5, '#8fb55a'), (1, '#4e6e2a')])
b = '<rect width="1920" height="1080" fill="url(#bsky)"/>'
# blurred plantation behind: big leaves out of focus
b += '<g filter="url(#bl)">'
for x, y, L, r, c in ((-60, 380, 700, -20, '#1f4a22'), (380, 120, 800, 15, '#2c5e28'), (900, 40, 900, -35, '#3f7a30'), (1200, 300, 800, 20, '#2a5a26'),
                      (1500, 80, 700, 40, '#4e8a36'), (700, 520, 900, -10, '#1c4220'), (1350, 560, 800, -25, '#244e22')):
    b += leaf(x, y, L, r, c, '#16361a', op=.85)
b += '</g>'
b += '<rect width="1920" height="1080" fill="url(#bsun)"/>'
for _ in range(14):   # bokeh dots
    b += f'<circle cx="{random.randint(900, 1880)}" cy="{random.randint(30, 420)}" r="{random.randint(16, 46)}" fill="#fff8c8" opacity="{random.uniform(.12, .3):.2f}"/>'
# cutting board (table top in perspective)
b += '<path d="M0 640 L1920 590 L1920 1080 L0 1080Z" fill="#3a2410"/>'
b += '<path d="M120 700 L1880 650 L1920 1080 L60 1080Z" fill="url(#bwood)"/>'
b += '<path d="M120 700 L1880 650" stroke="#e2b07a" stroke-width="8" opacity=".7"/>'
for k in range(14):
    yy = 720 + k * 26
    b += f'<path d="M{100 - k * 3} {yy} C 600 {yy - 20 + random.randint(-8, 8)} 1200 {yy - 30} {1900} {yy - 40 + random.randint(-8, 8)}" stroke="#6a4020" stroke-width="{random.choice([2, 3, 4])}" fill="none" opacity=".35"/>'


def split_banana(x, y, L, rot, sag, w, peel, flesh, seeds, seed_r, rim='#fff7cf', seed_col='#1a120a', specks=0, gid='s'):
    """banana sliced lengthwise, seen from the cut face: peel rim, flesh, seeds or specks in the centre"""
    C = bcurve(L, sag, w)
    top = [(px - nx * t, py - ny * t) for px, py, nx, ny, t in C]; bot = [(px + nx * t, py + ny * t) for px, py, nx, ny, t in C]
    ti = [(px - nx * t * .80, py - ny * t * .80) for px, py, nx, ny, t in C]; bi = [(px + nx * t * .80, py + ny * t * .80) for px, py, nx, ny, t in C]
    o = f'<g transform="translate({x} {y}) rotate({rot})">'
    o += f'<path d="{P([(px + 14, py + 26) for px, py in top + bot[::-1]])}Z" fill="#1a0e04" opacity=".45" filter="url(#bl6)"/>'   # shadow
    o += f'<path d="{P(top + bot[::-1])}Z" fill="url(#{peel})" stroke="#3b2a0c" stroke-width="5" stroke-linejoin="round"/>'
    o += f'<path d="{P(ti[1:-1] + bi[1:-1][::-1])}Z" fill="url(#{flesh})" stroke="#c9a85a" stroke-width="3"/>'
    # wet sheen on the cut face
    o += f'<path d="{P([(px - nx * t * .5, py - ny * t * .5) for px, py, nx, ny, t in C[6:-10]])}" fill="none" stroke="#ffffff" stroke-width="{w * .14:.1f}" stroke-linecap="round" opacity=".55"/>'
    o += f'<path d="{P([(px - nx * t * .9, py - ny * t * .9) for px, py, nx, ny, t in C[4:-6]])}" fill="none" stroke="{rim}" stroke-width="5" opacity=".8"/>'
    # three faint segment lines of the fruit
    for f in (-.25, .25):
        o += f'<path d="{P([(px + nx * t * f, py + ny * t * f) for px, py, nx, ny, t in C[4:-4]])}" fill="none" stroke="#d8c48a" stroke-width="3" opacity=".7"/>'
    rnd = random.Random(5)
    for i in range(seeds):
        u = 3 + (len(C) - 7) * (i + .5) / seeds; px, py, nx, ny, t = C[int(u)]
        for row in ((-.38, 0) if seeds > 10 else (0,)) if False else ((-.36, .36) if seeds > 12 else (0,)):
            cx_, cy_ = px + nx * t * row + rnd.uniform(-4, 4), py + ny * t * row
            o += f'<ellipse cx="{cx_:.1f}" cy="{cy_:.1f}" rx="{seed_r * 1.1:.1f}" ry="{seed_r * .9:.1f}" fill="{seed_col}"/>'
            o += f'<ellipse cx="{cx_ - seed_r * .35:.1f}" cy="{cy_ - seed_r * .35:.1f}" rx="{seed_r * .35:.1f}" ry="{seed_r * .22:.1f}" fill="#8a7a60" opacity=".8"/>'
    for i in range(specks):
        u = 4 + (len(C) - 9) * i / max(1, specks - 1); px, py, nx, ny, t = C[int(u)]
        o += f'<circle cx="{px + rnd.uniform(-3, 3):.1f}" cy="{py + rnd.uniform(-3, 3):.1f}" r="{rnd.uniform(2.2, 3.6):.1f}" fill="#5a3e1e" opacity=".85"/>'
    # stem and tip
    sx, sy = C[0][0], C[0][1]
    o += f'<path d="M{sx:.0f},{sy:.0f} l{-L * .07:.0f},{-L * .03:.0f}" stroke="#3b2a0c" stroke-width="{w * .6:.0f}" stroke-linecap="round"/><path d="M{sx:.0f},{sy:.0f} l{-L * .07:.0f},{-L * .03:.0f}" stroke="#8f9a3a" stroke-width="{w * .42:.0f}" stroke-linecap="round"/>'
    o += f'<circle cx="{C[-1][0]:.0f}" cy="{C[-1][1]:.0f}" r="{w * .18:.0f}" fill="#3a2a12"/></g>'
    return o


# big supermarket banana, cut open: almost nothing inside
b += '<ellipse cx="1220" cy="740" rx="580" ry="170" fill="#fff6c8" opacity=".18" filter="url(#soft)"/>'
b += split_banana(1200, 600, 1100, -4, 150, 116, 'bpeel', 'bflesh', 0, 0, specks=34)
# the other half lying behind-right? keep it simple: a few round slices in front
for k, (sx, sy) in enumerate(((930, 965), (1095, 990))):
    b += f'<ellipse cx="{sx + 8}" cy="{sy + 18}" rx="78" ry="34" fill="#1a0e04" opacity=".4" filter="url(#bl6)"/>'
    b += f'<ellipse cx="{sx}" cy="{sy + 8}" rx="78" ry="36" fill="#d9b23a" stroke="#3b2a0c" stroke-width="4"/>'
    b += f'<ellipse cx="{sx}" cy="{sy}" rx="76" ry="34" fill="#f2c232" stroke="#3b2a0c" stroke-width="4"/>'
    b += f'<ellipse cx="{sx}" cy="{sy}" rx="64" ry="27" fill="url(#bflesh)"/>'
    b += f'<path d="M{sx} {sy} l-30 -10 M{sx} {sy} l30 -10 M{sx} {sy} l0 22" stroke="#d8c48a" stroke-width="3"/>'
    for a in (0, 2.1, 4.2):
        b += f'<circle cx="{sx + math.cos(a) * 9:.0f}" cy="{sy + math.sin(a) * 4:.0f}" r="2.6" fill="#5a3e1e"/>'
# wild banana: short, stubby, packed with big hard seeds (front left, lower)
b += split_banana(470, 870, 520, 6, 70, 92, 'bwpeel', 'bwflesh', 15, 15)
# magnifying glass over the big banana's centre line
mx, my, mr = 1300, 735, 150
d += f'<clipPath id="lens"><circle cx="{mx}" cy="{my}" r="{mr}"/></clipPath>'
b += f'<path d="M{mx + mr * .72:.0f} {my + mr * .72:.0f} L{mx + mr * 1.6:.0f} {my + mr * 1.75:.0f}" stroke="#1b120a" stroke-width="62" stroke-linecap="round"/>'
b += f'<path d="M{mx + mr * .72:.0f} {my + mr * .72:.0f} L{mx + mr * 1.6:.0f} {my + mr * 1.75:.0f}" stroke="#7a3a1e" stroke-width="44" stroke-linecap="round"/>'
b += f'<path d="M{mx + mr * .8:.0f} {my + mr * .74:.0f} L{mx + mr * 1.58:.0f} {my + mr * 1.62:.0f}" stroke="#c0704a" stroke-width="10" stroke-linecap="round" opacity=".7"/>'
b += f'<g clip-path="url(#lens)"><rect x="{mx - mr}" y="{my - mr}" width="{2 * mr}" height="{2 * mr}" fill="#f7ecc0"/>'
b += f'<path d="M{mx - mr} {my - 40} Q{mx} {my - 52} {mx + mr} {my - 44} M{mx - mr} {my + 52} Q{mx} {my + 40} {mx + mr} {my + 46}" stroke="#d8c48a" stroke-width="7" fill="none"/>'
for k, (ox, oy, r) in enumerate(((-90, 2, 9), (-40, -4, 11), (12, 3, 8), (60, -2, 12), (105, 4, 9))):
    b += f'<ellipse cx="{mx + ox}" cy="{my + oy}" rx="{r}" ry="{r * .75:.0f}" fill="#5a3e1e"/><ellipse cx="{mx + ox - 3}" cy="{my + oy - 3}" rx="{r * .35:.0f}" ry="{r * .25:.0f}" fill="#a88a5a"/>'
b += f'<ellipse cx="{mx - 50}" cy="{my - 60}" rx="70" ry="34" fill="#ffffff" opacity=".35" transform="rotate(-30 {mx - 50} {my - 60})"/></g>'
b += f'<circle cx="{mx}" cy="{my}" r="{mr}" fill="none" stroke="#1b120a" stroke-width="30"/>'
b += f'<circle cx="{mx}" cy="{my}" r="{mr}" fill="none" stroke="#d9b56a" stroke-width="18"/>'
b += f'<path d="M{mx - mr * .7:.0f} {my - mr * .72:.0f} A{mr} {mr} 0 0 1 {mx + mr * .2:.0f} {my - mr * .98:.0f}" stroke="#fff4d0" stroke-width="7" fill="none" stroke-linecap="round"/>'
for sx, sy, s in ((1640, 300, 22), (1460, 220, 14), (1580, 560, 14), (1760, 430, 12), (300, 690, 12)):
    b += spark(sx, sy, s, '#fffbe0', .9)
d += rad('bvig', 960, 540, 1150, [(0, '#000', 0), (.65, '#000', 0), (1, '#000', .55)])
b += '<rect width="1920" height="1080" fill="url(#bvig)"/>'
open(os.path.join(HERE, 'B.html'), 'w').write(page('#2f6a32', svg(d, b), [('NO', 250, 'w'), ('SEEDS?', 250, 'y')], outline='#0a1a0c'))


# =========================== C: SLIGHTLY RADIOACTIVE (glowing banana, detector, port gate) ===========================
random.seed(23)
d = SOFT + BL + BL6
d += lin('csky', [(0, '#041410'), (.6, '#0b2a22'), (1, '#123a2c')])
d += rad('cglow', 1240, 640, 640, [(0, '#e8ff9a', .55), (.3, '#9cf07a', .25), (.7, '#3fcf7a', .07), (1, '#3fcf7a', 0)])
d += lin('cground', [(0, '#10261e'), (1, '#040c09')])
d += lin('cbox', [(0, '#f2d24a'), (.5, '#d9a82a'), (1, '#7a5a10')], x2=1, y2=1)
d += rad('cdial', 0, 0, 100, [(0, '#f8f6e6', 1), (.85, '#e2dcc0', 1), (1, '#9a9478', 1)])
H = 780
b = '<rect width="1920" height="1080" fill="url(#csky)"/>'
# port at night far behind: container stacks, cranes, lamps
for k in range(22):
    cx_ = 40 + k * 88; h_ = random.choice([60, 90, 120, 150])
    b += f'<rect x="{cx_}" y="{H - h_}" width="84" height="{h_}" fill="{random.choice(["#173a30", "#1c4436", "#14302a", "#21483a"])}"/>'
    for yy in range(H - h_, H, 30):
        b += f'<path d="M{cx_} {yy} h84" stroke="#0a1a14" stroke-width="3"/>'
for cx_ in (200, 760):
    b += f'<path d="M{cx_} {H} L{cx_} {H - 420} L{cx_ + 40} {H - 420} L{cx_ + 40} {H} M{cx_ - 120} {H - 400} L{cx_ + 300} {H - 400}" stroke="#163a30" stroke-width="18" fill="none"/>'
    b += f'<path d="M{cx_ + 20} {H - 420} L{cx_ + 300} {H - 400} M{cx_ + 20} {H - 420} L{cx_ - 120} {H - 400}" stroke="#163a30" stroke-width="6"/>'
    b += f'<circle cx="{cx_ + 20}" cy="{H - 430}" r="6" fill="#ff6a4a"/>'
for lx in (120, 480, 980, 1500, 1800):
    b += f'<circle cx="{lx}" cy="{H - 220}" r="40" fill="#fff4c0" opacity=".12"/><circle cx="{lx}" cy="{H - 220}" r="5" fill="#fff4c0"/>'
b += stars(60, 300, col='#cfeee0', op=.4, sparks=0)
# ground (wet asphalt) with glow reflection
b += f'<rect x="0" y="{H}" width="1920" height="{1080 - H}" fill="url(#cground)"/>'
b += f'<path d="M0 {H} H1920" stroke="#2a5a46" stroke-width="4"/>'
for k in range(8):
    b += f'<path d="M{k * 260 - 100} 1080 L{820 + k * 40} {H}" stroke="#1d3a2e" stroke-width="4" opacity=".7"/>'
# radiation portal gate with a banana truck in it (middle ground, left of centre)
gx = 120
b += f'<rect x="{gx}" y="{H - 280}" width="44" height="280" fill="#cfd8d0" stroke="#0a1410" stroke-width="5"/><rect x="{gx + 420}" y="{H - 280}" width="44" height="280" fill="#cfd8d0" stroke="#0a1410" stroke-width="5"/>'
b += f'<rect x="{gx - 10}" y="{H - 310}" width="484" height="36" fill="#e2e8e0" stroke="#0a1410" stroke-width="5"/>'
b += f'<path d="M{gx + 4} {H - 280} v280 M{gx + 424} {H - 280} v280" stroke="#f2d27a" stroke-width="8" stroke-dasharray="26 22"/>'
b += f'<circle cx="{gx + 22}" cy="{H - 342}" r="26" fill="#ff5a3a"/><circle cx="{gx + 22}" cy="{H - 342}" r="70" fill="#ff5a3a" opacity=".22" filter="url(#soft)"/>'
b += f'<circle cx="{gx + 442}" cy="{H - 342}" r="26" fill="#ff5a3a"/><circle cx="{gx + 442}" cy="{H - 342}" r="70" fill="#ff5a3a" opacity=".22" filter="url(#soft)"/>'
# truck: container of banana crates
b += f'<rect x="{gx + 60}" y="{H - 250}" width="270" height="200" rx="6" fill="#2f6a5a" stroke="#0a1410" stroke-width="5"/>'
for k in range(6):
    b += f'<path d="M{gx + 80 + k * 42} {H - 240} v180" stroke="#1f4a40" stroke-width="8"/>'
b += f'<rect x="{gx + 330}" y="{H - 180}" width="80" height="130" rx="10" fill="#d9d2b0" stroke="#0a1410" stroke-width="5"/><rect x="{gx + 345}" y="{H - 168}" width="52" height="44" rx="5" fill="#8fd6c0"/>'
for wx in (gx + 110, gx + 280, gx + 370):
    b += f'<circle cx="{wx}" cy="{H - 40}" r="32" fill="#0a0f0c"/><circle cx="{wx}" cy="{H - 40}" r="13" fill="#6a7a70"/>'
# open crate of bananas in front of the truck rear
b += f'<rect x="{gx + 70}" y="{H - 300}" width="150" height="52" fill="#a8743a" stroke="#0a1410" stroke-width="4"/>'
for k in range(4):
    bd, bb = banana(gx + 105 + k * 28, H - 300, 90, rot=-8 + k * 5, w=10, sag=14, gid=f'cr{k}', ridge=False)
    d += bd; b += bb
# beta / gamma tracks from the big banana: soft dotted particle trails
cx0, cy0 = 1240, 640
b += '<rect width="1920" height="1080" fill="url(#cglow)"/>'
for k in range(18):
    a = random.uniform(0, 2 * math.pi); r0 = random.uniform(230, 280); r1 = r0 + random.uniform(140, 330); bend = random.uniform(-.35, .35)
    x0, y0 = cx0 + math.cos(a) * r0, cy0 + math.sin(a) * r0 * .7
    x1, y1 = cx0 + math.cos(a + bend) * r1, cy0 + math.sin(a + bend) * r1 * .7
    if x1 > 1600 and y1 > 860: continue
    if x1 < 1150 and y1 < 420: continue
    if x1 < 900: continue
    b += f'<path d="M{x0:.0f} {y0:.0f} Q{(x0 + x1) / 2 + random.uniform(-60, 60):.0f} {(y0 + y1) / 2 + random.uniform(-60, 60):.0f} {x1:.0f} {y1:.0f}" stroke="#c8ff8a" stroke-width="4" stroke-dasharray="2 16" stroke-linecap="round" fill="none" opacity=".75"/>'
    b += f'<circle cx="{x1:.0f}" cy="{y1:.0f}" r="7" fill="#eaffb0"/><circle cx="{x1:.0f}" cy="{y1:.0f}" r="18" fill="#c8ff8a" opacity=".3"/>'
# the big banana itself, glowing softly
b += '<ellipse cx="1260" cy="930" rx="420" ry="40" fill="#9cf07a" opacity=".22" filter="url(#soft)"/>'
gd, gb = banana(cx0, cy0, 860, rot=-12, w=88, sag=140, gid='rad', col=('#fbffc0', '#e8d23a', '#8a9a1a'), tip='#3a3a12', stem='#6f9a3a', rim='#f4ffd0', glow='#b8ff6a', spots=7)
d += gd; b += gb
for sx, sy, s in ((1000, 470, 20), (1600, 380, 24), (1700, 640, 14), (1300, 420, 14), (1450, 860, 12)):
    b += spark(sx, sy, s, '#f4ffd0', .95)
# handheld detector (yellow box with dial and probe wand) at front left-centre, needle swung up
dx, dy = 660, 900
b += f'<ellipse cx="{dx + 20}" cy="{dy + 120}" rx="230" ry="26" fill="#000" opacity=".5"/>'
b += f'<path d="M{dx + 150} {dy - 20} C{dx + 300} {dy - 40} {dx + 280} {dy - 200} {dx + 420} {dy - 230}" stroke="#151a16" stroke-width="16" fill="none"/>'   # cable
b += f'<g transform="rotate(-28 {dx + 480} {dy - 260})"><rect x="{dx + 410}" y="{dy - 280}" width="190" height="44" rx="20" fill="#3a4440" stroke="#0a0f0c" stroke-width="5"/>'
b += f'<rect x="{dx + 560}" y="{dy - 284}" width="70" height="52" rx="10" fill="#c9d2cc" stroke="#0a0f0c" stroke-width="5"/>'
b += f'<path d="M{dx + 430} {dy - 268} h150" stroke="#7a8a84" stroke-width="5" opacity=".7"/></g>'
b += f'<rect x="{dx - 200}" y="{dy - 110}" width="360" height="230" rx="26" fill="url(#cbox)" stroke="#2a1e06" stroke-width="7"/>'
b += f'<rect x="{dx - 120}" y="{dy - 150}" width="200" height="48" rx="20" fill="none" stroke="#2a1e06" stroke-width="16"/>'
b += f'<path d="M{dx - 180} {dy - 80} h320" stroke="#fff4b0" stroke-width="6" opacity=".55" stroke-linecap="round"/>'
b += f'<g transform="translate({dx - 40} {dy + 40})"><circle r="92" fill="#2a1e06"/><circle r="82" fill="url(#cdial)"/>'
b += '<path d="M-62 0 A62 62 0 0 1 -31 -54" stroke="#5aa86a" stroke-width="14" fill="none"/><path d="M-31 -54 A62 62 0 0 1 31 -54" stroke="#e8c23a" stroke-width="14" fill="none"/><path d="M31 -54 A62 62 0 0 1 62 0" stroke="#d9573a" stroke-width="14" fill="none"/>'
for k in range(11):
    a = math.radians(180 + k * 18)
    b += f'<path d="M{math.cos(a) * 46:.0f} {math.sin(a) * 46:.0f} L{math.cos(a) * 56:.0f} {math.sin(a) * 56:.0f}" stroke="#2a2a20" stroke-width="3"/>'
b += '<path d="M0 0 L22 -60" stroke="#1a1a12" stroke-width="7" stroke-linecap="round"/><circle r="10" fill="#1a1a12"/></g>'
b += f'<circle cx="{dx + 110}" cy="{dy}" r="14" fill="#7aff6a"/><circle cx="{dx + 110}" cy="{dy}" r="36" fill="#7aff6a" opacity=".3"/>'
b += f'<circle cx="{dx + 110}" cy="{dy + 60}" r="14" fill="#3a3a2a"/>'
# click arcs next to the speaker
for r in (40, 62):
    b += f'<path d="M{dx + 190} {dy - 40 - r * .3:.0f} a{r} {r} 0 0 1 0 {r * .9:.0f}" stroke="#eaffb0" stroke-width="6" fill="none" opacity=".75" transform="translate({r * .4:.0f} 0)"/>'
d += rad('cvig', 960, 540, 1150, [(0, '#000', 0), (.6, '#000', 0), (1, '#000', .6)])
b += '<rect width="1920" height="1080" fill="url(#cvig)"/>'
open(os.path.join(HERE, 'C.html'), 'w').write(page('#041410', svg(d, b), [('SLIGHTLY', 170, 'w'), ('RADIOACTIVE', 150, 'y')], outline='#03100a'))
print('ok')
