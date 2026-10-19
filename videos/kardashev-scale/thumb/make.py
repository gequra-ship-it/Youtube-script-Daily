import sys, os, math, random
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', 'tools'))
from thumb_lib import *
random.seed(7)
os.chdir(os.path.dirname(os.path.abspath(__file__)))


def astronaut(x, y, s, col='#0c0f1a', rim='#ffd98a', face=1):
    """small suited figure, feet at (x, y), ~120*s tall, rim light from upper-right (face=1) or upper-left (-1)"""
    g = f'<g transform="translate({x} {y}) scale({s * face} {s})"><g fill="{col}">'
    g += '<rect x="-17" y="-52" width="14" height="52" rx="6"/><rect x="3" y="-52" width="14" height="52" rx="6"/>'
    g += '<rect x="-21" y="-6" width="20" height="8" rx="4"/><rect x="1" y="-6" width="22" height="8" rx="4"/>'
    g += '<rect x="-30" y="-92" width="22" height="40" rx="7"/>'          # backpack
    g += '<rect x="-20" y="-98" width="42" height="52" rx="14"/>'           # torso
    g += '<rect x="-27" y="-92" width="12" height="40" rx="6" transform="rotate(8 -21 -92)"/><rect x="16" y="-92" width="12" height="38" rx="6" transform="rotate(-24 22 -92)"/>'
    g += '<circle cx="3" cy="-114" r="20"/></g>'
    g += '<path d="M6 -122 Q20 -122 21 -108 Q14 -104 6 -108Z" fill="#8fb8e8" opacity=".9"/>'  # visor (looking up-right)
    g += f'<path d="M14 -130 Q24 -122 22 -108" stroke="{rim}" stroke-width="3.5" fill="none" stroke-linecap="round"/>'
    g += f'<path d="M20 -94 Q24 -76 21 -50" stroke="{rim}" stroke-width="3.5" fill="none" stroke-linecap="round"/>'
    g += f'<path d="M15 -48 L16 -4" stroke="{rim}" stroke-width="3" fill="none" stroke-linecap="round" opacity=".8"/></g>'
    return g


def galaxy(cx, cy, R, tilt=-10, squash=.36, n=900, core='#fff1c8', arm='#ffd98a', arm2='#9fc4ff'):
    o = f'<g transform="translate({cx} {cy}) rotate({tilt}) scale(1 {squash})">'
    o += f'<circle r="{R * 1.05:.0f}" fill="url(#gx)"/>'
    for i in range(n):
        k = i % 2; t = random.uniform(0, 3.3 * math.pi)
        r = R * .06 * math.exp(.27 * t); r = min(r, R)
        a = t + k * math.pi + random.gauss(0, .22)
        x, y = math.cos(a) * r + random.gauss(0, R * .03), math.sin(a) * r + random.gauss(0, R * .03)
        c = arm if random.random() < .55 else arm2
        o += f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{random.choice([1.5, 2.2, 3, 4]) * (1.6 - r / R):.1f}" fill="{c}" opacity="{random.uniform(.35, .95):.2f}"/>'
    o += f'<circle r="{R * .16:.0f}" fill="{core}"/><circle r="{R * .08:.0f}" fill="#ffffff"/></g>'
    return o


def swarm(cx, cy, rings, front, dark='#2a1606', gold='#ffcf5a', hi='#fff2c0'):
    """Dyson swarm collectors on tilted ellipses; front=True draws the near half"""
    o = ''
    for a, b, tilt, n, sz in rings:
        ct, st = math.cos(math.radians(tilt)), math.sin(math.radians(tilt))
        for i in range(n):
            t = 2 * math.pi * i / n + random.uniform(-.02, .02)
            near = math.sin(t) > 0
            if near != front:
                continue
            ex, ey = a * math.cos(t), b * math.sin(t)
            x, y = cx + ex * ct - ey * st, cy + ex * st + ey * ct
            depth = .75 + .35 * math.sin(t)
            w, h = sz * depth * random.uniform(.8, 1.2), sz * depth * .62
            rot = tilt + math.degrees(math.atan2(b * math.cos(t), -a * math.sin(t))) * .3
            if front:
                o += (f'<g transform="translate({x:.1f} {y:.1f}) rotate({rot:.1f})"><rect x="{-w / 2:.1f}" y="{-h / 2:.1f}" width="{w:.1f}" height="{h:.1f}" rx="1.5" fill="{dark}" stroke="{gold}" stroke-width="{max(1.2, sz * .1):.1f}"/>'
                      f'<path d="M{-w / 2:.1f} 0 H{w / 2:.1f} M0 {-h / 2:.1f} V{h / 2:.1f}" stroke="{gold}" stroke-width="{max(.8, sz * .05):.1f}" opacity=".6"/>'
                      f'<rect x="{-w / 2:.1f}" y="{-h / 2:.1f}" width="{w:.1f}" height="{h * .32:.1f}" fill="{hi}" opacity=".55"/></g>')
            else:
                o += f'<rect transform="translate({x:.1f} {y:.1f}) rotate({rot:.1f})" x="{-w / 2:.1f}" y="{-h / 2:.1f}" width="{w:.1f}" height="{h:.1f}" fill="{gold}" opacity="{random.uniform(.45, .8):.2f}"/>'
    return o


def orbit(cx, cy, a, b, tilt, col='#ffcf5a', op=.25, sw=2):
    return f'<ellipse cx="{cx}" cy="{cy}" rx="{a}" ry="{b}" transform="rotate({tilt} {cx} {cy})" fill="none" stroke="{col}" stroke-width="{sw}" opacity="{op}"/>'


# ======================= A: WHY SO SILENT?  (homage: 2001: A Space Odyssey, monolith under the aligned planet-sun) =======================
CX = 1330
d = lin('sk', [(0, '#020308'), (.6, '#060b1c'), (1, '#0d1430')])
d += rad('sg', CX, 320, 700, [(0, '#fff4d0', .55), (.18, '#ffd98a', .25), (.5, '#3a4a8a', .08), (1, '#000', 0)])
d += rad('gx', 0, 0, 230, [(0, '#ffe6a8', .6), (.5, '#7a8ad8', .18), (1, '#000', 0)])
d += rad('st', CX, 320, 120, [(0, '#ffffff', 1), (.45, '#fff6d8', 1), (.75, '#ffd06a', .9), (1, '#ffb040', 0)])
d += lin('mono', [(0, '#1a1c24'), (.12, '#07080c'), (1, '#000000')], x2=1, y2=0)
d += lin('gnd', [(0, '#8a8c96'), (.25, '#4a4c58'), (1, '#0c0d14')])
d += rad('gl', CX, 900, 500, [(0, '#ffe6a8', .35), (1, '#ffe6a8', 0)])
d += '<filter id="bl"><feGaussianBlur stdDeviation="6"/></filter><filter id="bl2"><feGaussianBlur stdDeviation="18"/></filter>'
d += f'<clipPath id="ec"><circle cx="{CX}" cy="548" r="70"/></clipPath>'
b = '<rect width="1920" height="1080" fill="url(#sk)"/>' + stars(260, 820, 0, '#dfe8ff', .55, 0)
b += '<rect width="1920" height="1080" fill="url(#sg)"/>'
b += f'<rect x="{CX - 70}" y="0" width="140" height="900" fill="#fff0c8" opacity=".07" filter="url(#bl2)"/>'   # alignment beam
b += galaxy(CX, 128, 265, n=1300)
# star with Dyson swarm
b += swarm(CX, 320, [(200, 46, -8, 54, 15), (168, 70, 22, 42, 13)], False)
b += f'<circle cx="{CX}" cy="320" r="120" fill="url(#st)"/><circle cx="{CX}" cy="320" r="58" fill="#ffffff"/>'
b += f'<path d="M{CX - 520} 320 L{CX + 520} 320" stroke="#fff6dc" stroke-width="5" opacity=".7" filter="url(#bl)"/><path d="M{CX - 300} 320 L{CX + 300} 320" stroke="#ffffff" stroke-width="2.5" opacity=".9"/>'
b += f'<path d="M{CX} 150 L{CX} 470" stroke="#ffffff" stroke-width="2" opacity=".5"/>'
b += ''.join(f'<path d="M{CX + math.cos(a) * 80:.0f} {320 + math.sin(a) * 80:.0f} L{CX + math.cos(a) * 175:.0f} {320 + math.sin(a) * 175:.0f}" stroke="#fff6dc" stroke-width="3" opacity=".35" stroke-linecap="round"/>' for a in [k * math.pi / 6 + .26 for k in range(12)])
b += swarm(CX, 320, [(200, 46, -8, 54, 15), (168, 70, 22, 42, 13)], True)
# crescent Earth, lit from above
EY, ER = 548, 70
b += f'<circle cx="{CX}" cy="{EY}" r="{ER}" fill="#05070e"/>'
b += f'<g clip-path="url(#ec)"><circle cx="{CX}" cy="{EY - 20}" r="{ER + 4}" fill="#3a8ae8"/><circle cx="{CX}" cy="{EY - 22}" r="{ER + 4}" fill="#7fc0ff" opacity=".5"/><circle cx="{CX}" cy="{EY + 22}" r="{ER + 4}" fill="#05070e"/>'
b += f'<path d="M{CX - 48} {EY - 56} q24 -10 48 -2 q16 4 36 -2" stroke="#ffffff" stroke-width="6" fill="none" opacity=".8"/><path d="M{CX - 60} {EY - 38} q12 -7 26 -2" stroke="#e8fff0" stroke-width="5" fill="none" opacity=".6"/></g>'
b += f'<path d="M{CX - ER + 1} {EY - 8} A{ER} {ER} 0 0 1 {CX + ER - 1} {EY - 8}" stroke="#bfe0ff" stroke-width="4" fill="none" opacity=".9"/>'
b += f'<path d="M{CX - ER - 8} {EY - 8} A{ER + 8} {ER + 8} 0 0 1 {CX + ER + 8} {EY - 8}" stroke="#7fc0ff" stroke-width="10" fill="none" opacity=".35" filter="url(#bl)"/>'
# lunar ground
b += '<path d="M0 860 C300 836 700 850 1000 842 C1300 834 1600 848 1920 838 L1920 1080 L0 1080Z" fill="url(#gnd)"/>'
b += '<rect width="1920" height="1080" fill="url(#gl)"/>'
for x, y, rx in ((240, 900, 90), (620, 960, 140), (1660, 900, 70), (980, 1020, 180), (1500, 990, 110), (420, 1040, 120)):
    b += f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{rx * .18:.0f}" fill="#1a1b24" opacity=".7"/><path d="M{x - rx} {y} A{rx} {rx * .18:.0f} 0 0 0 {x + rx} {y}" stroke="#b8bac4" stroke-width="3" fill="none" opacity=".45"/>'
b += blobs(70, 0, 870, 1920, 1080, '#22232e', .3, .7, 4, 16)
b += '<path d="M0 860 C300 836 700 850 1000 842 C1300 834 1600 848 1920 838" stroke="#d8d4c8" stroke-width="3" fill="none" opacity=".55"/>'
# monolith with long shadow toward the viewer
MB, MT, MW = 912, 640, 120
b += f'<path d="M{CX - MW / 2} {MB} L{CX + MW / 2} {MB} L{CX + 150} 1080 L{CX - 210} 1080Z" fill="#000" opacity=".55"/>'
b += f'<path d="M{CX - MW / 2} {MT} L{CX + MW / 2 - 20} {MT - 6} L{CX + MW / 2} {MT} L{CX + MW / 2} {MB} L{CX - MW / 2} {MB}Z" fill="url(#mono)"/>'
b += f'<path d="M{CX + MW / 2 - 20} {MT - 6} L{CX + MW / 2 + 10} {MT - 2} L{CX + MW / 2 + 10} {MB - 4} L{CX + MW / 2} {MB}  L{CX + MW / 2} {MT}Z" fill="#000"/>'
b += f'<path d="M{CX - MW / 2} {MT} L{CX + MW / 2 - 20} {MT - 6} L{CX + MW / 2 + 10} {MT - 2}" stroke="#ffe6a8" stroke-width="4" fill="none"/>'
b += f'<path d="M{CX - MW / 2} {MT} L{CX - MW / 2} {MB}" stroke="#ffe6a8" stroke-width="2.5" opacity=".55"/>'
b += f'<path d="M{CX - MW / 2 + 14} {MT + 10} L{CX - MW / 2 + 14} {MB - 20}" stroke="#4a5070" stroke-width="2" opacity=".35"/>'
b += f'<ellipse cx="{CX}" cy="{MB + 2}" rx="90" ry="10" fill="#000" opacity=".6"/>'
b += astronaut(CX - 170, 918, .62, rim='#ffe6a8')
b += f'<ellipse cx="{CX - 170}" cy="920" rx="22" ry="4" fill="#000" opacity=".5"/>'
b += spark(1640, 520, 18) + spark(1010, 420, 14, op=.6) + spark(1720, 200, 16)
open('A.html', 'w', encoding='utf-8').write(page('#020308', svg(d, b), [('WHY SO', 200, 'w'), ('SILENT?', 230, 'y')], '#000000', top=60))

# ======================= B: AROUND TYPE 0.7  (intuitive: a giant power gauge stuck short of the full planet) =======================
GX, GY, R = 1360, 880, 480
d = lin('sk', [(0, '#050a1e'), (.7, '#0b1838'), (1, '#122450')])
d += rad('face', GX, GY, R, [(0, '#16244a', 1), (.7, '#0c1530', 1), (1, '#060b1c', 1)])
d += lin('bez', [(0, '#e8d6a8'), (.35, '#8a7a58'), (.6, '#d8c28a'), (1, '#4a3e28')], x2=1, y2=1)
d += lin('arc', [(0, '#4fd8f0'), (.6, '#9fe8c8'), (1, '#ffd25a')], x2=1, y2=0)
d += lin('base', [(0, '#3a3424'), (.15, '#1e1c18'), (1, '#0a0a0c')])
d += rad('halo', GX, GY, 700, [(0, '#ffd25a', .22), (.5, '#4fd8f0', .06), (1, '#000', 0)])
d += rad('eg', GX + 392, GY - 64, 150, [(0, '#bfe8ff', .9), (.4, '#5fb0ff', .35), (1, '#5fb0ff', 0)])
d += '<filter id="bl"><feGaussianBlur stdDeviation="9"/></filter><filter id="bl3"><feGaussianBlur stdDeviation="3"/></filter>'
d += f'<clipPath id="fc"><path d="M{GX - R + 18} {GY} A{R - 18} {R - 18} 0 0 1 {GX + R - 18} {GY}Z"/></clipPath>'
d += f'<clipPath id="ec2"><circle cx="{GX + 392}" cy="{GY - 64}" r="40"/></clipPath>'
b = '<rect width="1920" height="1080" fill="url(#sk)"/>' + stars(220, 700, 0, '#dfe8ff', .55, 0)
b += '<rect width="1920" height="1080" fill="url(#halo)"/>'


def P(v, r):  # point on the dial for value v in [0, 1]
    a = math.radians(180 - v * 180)
    return GX + math.cos(a) * r, GY - math.sin(a) * r


# housing
b += f'<path d="M{GX - R - 34} {GY} A{R + 34} {R + 34} 0 0 1 {GX + R + 34} {GY}Z" fill="#000" opacity=".45" filter="url(#bl)"/>'
b += f'<path d="M{GX - R - 26} {GY} A{R + 26} {R + 26} 0 0 1 {GX + R + 26} {GY}Z" fill="url(#bez)"/>'
b += f'<path d="M{GX - R - 26} {GY} A{R + 26} {R + 26} 0 0 1 {GX + R + 26} {GY}" stroke="#fff4d0" stroke-width="3" fill="none" opacity=".7"/>'
b += f'<path d="M{GX - R} {GY} A{R} {R} 0 0 1 {GX + R} {GY}Z" fill="#2a2418"/>'
b += f'<path d="M{GX - R + 18} {GY} A{R - 18} {R - 18} 0 0 1 {GX + R - 18} {GY}Z" fill="url(#face)"/>'
for k in range(15):  # rivets on bezel
    x, y = P(k / 14, R + 13)
    b += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="5" fill="#4a3e28"/><circle cx="{x - 1.5:.0f}" cy="{y - 1.5:.0f}" r="2.2" fill="#fff4d0" opacity=".8"/>'
b += '<g clip-path="url(#fc)">'
b += ''.join(f'<circle cx="{GX + random.randint(-440, 440)}" cy="{GY - random.randint(10, 440)}" r="{random.choice([1, 1.5, 2])}" fill="#9fc4ff" opacity="{random.uniform(.1, .4):.2f}"/>' for _ in range(90))
# scale arc: lit part 0..0.7, dark part 0.7..1
RA = 370
x0, y0 = P(0, RA); x7, y7 = P(.7, RA); x1, y1 = P(1, RA)
lit = f'M{x0:.0f} {y0:.0f} A{RA} {RA} 0 0 1 {x7:.1f} {y7:.1f}'
b += f'<path d="M{x7:.1f} {y7:.1f} A{RA} {RA} 0 0 1 {x1:.0f} {y1:.0f}" stroke="#2a3456" stroke-width="44" fill="none"/>'
b += f'<path d="M{x7:.1f} {y7:.1f} A{RA} {RA} 0 0 1 {x1:.0f} {y1:.0f}" stroke="#ff8a6a" stroke-width="3" fill="none" stroke-dasharray="10 12" opacity=".7"/>'
b += f'<path d="{lit}" stroke="url(#arc)" stroke-width="60" fill="none" opacity=".55" filter="url(#bl)"/>'
b += f'<path d="{lit}" stroke="url(#arc)" stroke-width="44" fill="none"/>'
b += f'<path d="{lit}" stroke="#ffffff" stroke-width="6" fill="none" opacity=".55" transform="translate(0 -2)"/>'
for k in range(41):
    v = k / 40; big = k % 4 == 0
    xa, ya = P(v, RA + 34); xb, yb = P(v, RA + (70 if big else 52))
    col = '#ffe6a8' if v <= .7 else '#5a6488'
    b += f'<path d="M{xa:.1f} {ya:.1f} L{xb:.1f} {yb:.1f}" stroke="{col}" stroke-width="{6 if big else 3}" stroke-linecap="round"/>'
for k in range(11):
    xa, ya = P(k / 10, RA - 36); b += f'<circle cx="{xa:.1f}" cy="{ya:.1f}" r="{5 if k % 5 == 0 else 3}" fill="#9fb4e8" opacity=".55"/>'
b += '</g>'
# full-planet target at 1.0: a glowing Earth (Type One = the whole planet)
EX, EY = GX + 392, GY - 64
b += f'<circle cx="{EX}" cy="{EY}" r="150" fill="url(#eg)"/>'
b += f'<circle cx="{EX}" cy="{EY}" r="40" fill="#2a6ad0"/><g clip-path="url(#ec2)"><path d="M{EX - 34} {EY - 18} q16 -14 30 -4 q8 10 -4 18 q-14 4 -20 16 q-10 -6 -6 -30Z M{EX + 6} {EY + 8} q18 -8 26 6 q-6 18 -22 20 q-8 -12 -4 -26Z" fill="#4fbf6a"/>'
b += f'<path d="M{EX - 40} {EY - 4} q30 -12 80 6" stroke="#ffffff" stroke-width="4" fill="none" opacity=".75"/><circle cx="{EX + 20}" cy="{EY + 14}" r="44" fill="#020610" opacity=".45"/></g>'
b += f'<circle cx="{EX}" cy="{EY}" r="40" fill="none" stroke="#cfe8ff" stroke-width="3"/>'
# spark at 0
sx, sy = P(0, RA)
b += spark(int(sx), int(sy), 14, '#bff4ff')
# needle stuck at 0.7 (jitter ghosts)
for dv, op in ((-.012, .18), (.012, .18), (-.006, .3)):
    xt, yt = P(.7 + dv, 400)
    b += f'<path d="M{GX} {GY} L{xt:.1f} {yt:.1f}" stroke="#ff6a4a" stroke-width="10" stroke-linecap="round" opacity="{op}"/>'
xt, yt = P(.7, 406); xb_, yb_ = P(.7, -60)
nx, ny = (yt - GY) / 406, -(xt - GX) / 406
b += f'<path d="M{xb_:.1f} {yb_:.1f} L{GX + nx * 16:.1f} {GY + ny * 16:.1f} L{xt:.1f} {yt:.1f} L{GX - nx * 16:.1f} {GY - ny * 16:.1f}Z" fill="#000" opacity=".4" transform="translate(10 12)" filter="url(#bl3)"/>'
b += f'<path d="M{xb_:.1f} {yb_:.1f} L{GX + nx * 16:.1f} {GY + ny * 16:.1f} L{xt:.1f} {yt:.1f} L{GX - nx * 16:.1f} {GY - ny * 16:.1f}Z" fill="#ff5a3a"/>'
b += f'<path d="M{GX + nx * 6:.1f} {GY + ny * 6:.1f} L{xt:.1f} {yt:.1f}" stroke="#ffd0b8" stroke-width="3" opacity=".9"/>'
b += f'<circle cx="{xt:.1f}" cy="{yt:.1f}" r="22" fill="#ffd25a" opacity=".5" filter="url(#bl)"/>'
for k in range(5):  # strain marks near the tip
    a = math.radians(30 + k * 14); px, py = P(.73, 424)
    b += f'<path d="M{px + math.cos(a) * 18:.0f} {py - math.sin(a) * 18:.0f} l{math.cos(a) * 20:.0f} {-math.sin(a) * 20:.0f}" stroke="#fff4d0" stroke-width="4" stroke-linecap="round" opacity=".8"/>'
b += f'<circle cx="{GX}" cy="{GY}" r="44" fill="url(#bez)"/><circle cx="{GX}" cy="{GY}" r="26" fill="#2a2418"/><circle cx="{GX - 6}" cy="{GY - 64}" r="9" fill="#fff4d0" opacity=".7"/>'
# glass reflection
b += f'<g clip-path="url(#fc)"><path d="M{GX - 380} {GY - 140} Q{GX - 180} {GY - 410} {GX + 70} {GY - 460} L{GX + 130} {GY - 436} Q{GX - 160} {GY - 370} {GX - 330} {GY - 104}Z" fill="#ffffff" opacity=".07"/></g>'
# base plate / console deck
b += f'<path d="M{GX - R - 70} {GY} L{GX + R + 70} {GY} L{GX + R + 40} {GY + 46} L{GX - R - 40} {GY + 46}Z" fill="url(#base)"/>'
b += f'<path d="M{GX - R - 70} {GY} L{GX + R + 70} {GY}" stroke="#ffe6a8" stroke-width="4" opacity=".8"/>'
b += f'<rect x="0" y="{GY + 46}" width="1920" height="{1080 - GY - 46}" fill="#05070f"/>'
b += f'<path d="M0 {GY + 46} H1920" stroke="#2a3a6a" stroke-width="3"/>'
b += ''.join(f'<rect x="{x}" y="{GY + 70}" width="60" height="10" rx="5" fill="#1a2444"/>' for x in range(40, 1560, 120))
b += astronaut(GX - R - 110, GY, .78, rim='#ffd25a')
b += f'<ellipse cx="{GX - R - 110}" cy="{GY + 2}" rx="26" ry="4" fill="#000" opacity=".5"/>'
b += spark(1800, 200, 18) + spark(960, 300, 14, op=.55) + spark(1700, 420, 12, op=.6)
open('B.html', 'w', encoding='utf-8').write(page('#050a1e', svg(d, b), [('AROUND', 130, 'w'), ('TYPE', 200, 'w'), ('0.7', 300, 'y')], '#03050e', top=40))

# ======================= C: SWALLOW A STAR  (intuitive: tiny human on a ledge under a star wrapped in a golden swarm) =======================
SX, SY, SR = 1400, 410, 215
d = lin('sk', [(0, '#12061e'), (.5, '#1e0a2e'), (1, '#2a0e22')], x2=1, y2=1)
d += rad('cor', SX, SY, 760, [(0, '#fff2c0', .9), (.25, '#ffb84a', .45), (.5, '#e05a2a', .14), (1, '#000', 0)])
d += rad('sun', SX - 50, SY - 60, SR * 1.15, [(0, '#ffffff', 1), (.35, '#fff6d0', 1), (.7, '#ffd25a', 1), (.92, '#ff9a30', 1), (1, '#e0601a', 1)])
d += lin('rock', [(0, '#2a1420'), (1, '#07030a')])
d += f'<clipPath id="sc"><circle cx="{SX}" cy="{SY}" r="{SR}"/></clipPath>'
d += '<filter id="bl"><feGaussianBlur stdDeviation="8"/></filter><filter id="bl2"><feGaussianBlur stdDeviation="22"/></filter>'
RINGS = [(470, 120, -14, 70, 28), (400, 190, 24, 60, 24), (330, 92, 62, 46, 20), (520, 70, 4, 76, 22)]
b = '<rect width="1920" height="1080" fill="url(#sk)"/>' + stars(240, 1000, 0, '#ffe8f0', .5, 0)
b += '<rect width="1920" height="1080" fill="url(#cor)"/>'
b += ''.join(orbit(SX, SY, a, bb, t, op=.18) for a, bb, t, _, _ in RINGS)
b += swarm(SX, SY, RINGS, False)
b += f'<circle cx="{SX}" cy="{SY}" r="{SR + 40}" fill="#ffcf6a" opacity=".5" filter="url(#bl2)"/>'
b += f'<circle cx="{SX}" cy="{SY}" r="{SR}" fill="url(#sun)"/>'
b += f'<g clip-path="url(#sc)">' + blobs(160, SX - SR, SY - SR, SX + SR, SY + SR, '#ff9a30', .08, .22, 6, 22) + blobs(80, SX - SR, SY - SR, SX + SR, SY + SR, '#ffffff', .1, .3, 4, 14) + '</g>'
for a0, h in ((200, 60), (300, 44), (20, 50)):  # prominences on the limb
    a = math.radians(a0); bx, by = SX + math.cos(a) * SR, SY + math.sin(a) * SR
    a2 = math.radians(a0 + 14); cx2, cy2 = SX + math.cos(a2) * SR, SY + math.sin(a2) * SR
    mx, my = SX + math.cos(math.radians(a0 + 7)) * (SR + h * 1.6), SY + math.sin(math.radians(a0 + 7)) * (SR + h * 1.6)
    b += f'<path d="M{bx:.0f} {by:.0f} Q{mx:.0f} {my:.0f} {cx2:.0f} {cy2:.0f}" stroke="#ff7a2a" stroke-width="12" fill="none" opacity=".75"/><path d="M{bx:.0f} {by:.0f} Q{mx:.0f} {my:.0f} {cx2:.0f} {cy2:.0f}" stroke="#ffd25a" stroke-width="4" fill="none"/>'
b += ''.join(orbit(SX, SY, a, bb, t, col='#ffe6a8', op=.35, sw=1.5) for a, bb, t, _, _ in RINGS)
b += swarm(SX, SY, RINGS, True)
# light beams from the star down toward the human
b += f'<path d="M{SX - 120} {SY + 120} L640 900 L840 900Z" fill="#ffd98a" opacity=".07" filter="url(#bl)"/>'
# distant ledge layers and the foreground ledge
b += '<path d="M0 820 C200 800 360 812 520 790 C640 774 760 800 900 812 L900 1080 L0 1080Z" fill="#3a1830" opacity=".7"/>'
LEDGE = 'M0 900 L120 884 L240 892 L360 872 L470 880 L560 862 L660 870 L760 856 L860 862 L940 880 L980 920 L960 980 L1000 1080 L0 1080Z'
b += f'<path d="{LEDGE}" fill="url(#rock)"/>'
b += '<path d="M0 900 L120 884 L240 892 L360 872 L470 880 L560 862 L660 870 L760 856 L860 862 L940 880 L980 920" stroke="#ffb84a" stroke-width="5" fill="none" stroke-linejoin="round" opacity=".9"/>'
b += ''.join(f'<path d="M{x} {y} l{random.randint(-30, 30)} {random.randint(30, 90)}" stroke="#4a2232" stroke-width="3" opacity=".7"/>' for x, y in ((150, 900), (330, 890), (520, 880), (700, 875), (900, 885), (420, 960), (820, 960)))
b += f'<path d="M940 880 L980 920 L960 980 L1000 1080" stroke="#ff9a40" stroke-width="3" fill="none" opacity=".5"/>'
b += astronaut(800, 860, 1.05, rim='#ffcf6a')
b += '<ellipse cx="790" cy="862" rx="40" ry="6" fill="#000" opacity=".5"/>'
b += spark(1060, 760, 18) + spark(1820, 140, 20) + spark(980, 180, 14, op=.6) + spark(1760, 700, 14, op=.7)
open('C.html', 'w', encoding='utf-8').write(page('#12061e', svg(d, b), [('SWALLOW', 180, 'w'), ('A', 130, 'w'), ('STAR', 270, 'y')], '#0a0310', top=40))
print('ok')
