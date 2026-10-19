import sys, os, math, random
TOOLS = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))), 'tools')
sys.path.insert(0, TOOLS)
from thumb_lib import *
from hands import hand
os.chdir(os.path.dirname(os.path.abspath(__file__)))
random.seed(7)
LINE = '#160c18'


def limb(d, w, col, line=LINE, ow=7):
    return (f'<path d="{d}" stroke="{line}" stroke-width="{w + ow}" fill="none" stroke-linecap="round" stroke-linejoin="round"/>'
            f'<path d="{d}" stroke="{col}" stroke-width="{w}" fill="none" stroke-linecap="round" stroke-linejoin="round"/>')


def faller(suit='#2c5d7c', suit2='#1d3f58', rim='#ffd98a', skin='#e2a77c', hair='#3a2216', shoe='#2a2a33', sole='#c9c2b6', glint=True):
    """belly-down spread-eagle person seen from above (we see the back); local coords, head toward -y, ~400 x 380"""
    o = ''
    # legs (behind torso), soles of the shoes face the viewer
    for s in (-1, 1):
        d = f'M{26 * s} 40 Q{98 * s} 92 {104 * s} 190'
        o += limb(d, 40, suit2)
        o += f'<path d="M{36 * s} 52 Q{96 * s} 98 {100 * s} 176" stroke="{suit}" stroke-width="12" fill="none" stroke-linecap="round" opacity=".55"/>'
        o += f'<ellipse cx="{106 * s}" cy="{214}" rx="23" ry="31" fill="{shoe}" stroke="{LINE}" stroke-width="6" transform="rotate({-8 * s} {106 * s} 214)"/>'
        o += f'<ellipse cx="{106 * s}" cy="{216}" rx="15" ry="22" fill="{sole}" transform="rotate({-8 * s} {106 * s} 214)"/>'
        o += ''.join(f'<path d="M{(98 + k * 0) * s} {204 + k * 9} h{16 * s}" stroke="{shoe}" stroke-width="2.5" opacity=".6"/>' for k in range(3))
    # arms: one smooth tapered curve each, forearms raised (box position)
    for s, side in ((-1, 'L'), (1, 'R')):
        d = f'M{46 * s} -60 Q{158 * s} -58 {156 * s} -148'
        o += limb(d, 32, suit)
        o += f'<path d="M{60 * s} -70 Q{146 * s} -72 {146 * s} -140" stroke="{rim if s > 0 else suit2}" stroke-width="5" fill="none" stroke-linecap="round" opacity=".7"/>'
        o += f'<ellipse cx="{156 * s}" cy="-150" rx="19" ry="10" fill="{suit2}" stroke="{LINE}" stroke-width="5"/>'
        o += hand(156 * s, -152, angle=14 * s, size=31, side=side, view='back', pose='open', skin=skin, line=LINE)
    # torso (back of a jacket)
    t = 'M-54 -76 C-64 -30 -46 26 -36 54 L36 54 C46 26 64 -30 54 -76 Q0 -94 -54 -76Z'
    o += f'<path d="{t}" fill="{suit}" stroke="{LINE}" stroke-width="7" stroke-linejoin="round"/>'
    o += f'<path d="M0 -84 L0 50" stroke="{suit2}" stroke-width="4" opacity=".8"/>'
    o += f'<path d="M-36 54 L36 54 L38 40 L-38 40Z" fill="{suit2}"/>'
    o += f'<path d="M-50 -60 C-56 -20 -42 20 -32 46" stroke="{suit2}" stroke-width="10" fill="none" opacity=".6"/>'
    o += f'<path d="M50 -70 C60 -30 46 22 36 50" stroke="{rim}" stroke-width="6" fill="none" opacity=".85"/>'
    o += f'<path d="M-30 -84 Q0 -70 30 -84" stroke="{suit2}" stroke-width="9" fill="none"/>'  # collar
    # head (back of the head) with ears and fluttering hair
    o += f'<ellipse cx="-40" cy="-108" rx="8" ry="12" fill="{skin}" stroke="{LINE}" stroke-width="4"/><ellipse cx="40" cy="-108" rx="8" ry="12" fill="{skin}" stroke="{LINE}" stroke-width="4"/>'
    o += f'<circle cx="0" cy="-114" r="42" fill="{hair}" stroke="{LINE}" stroke-width="7"/>'
    for a_ in (-160, -125, -90, -55, -20):   # soft tufts on the edge of the hair
        r_ = math.radians(a_)
        o += f'<circle cx="{math.cos(r_) * 38:.0f}" cy="{-114 + math.sin(r_) * 38:.0f}" r="13" fill="{hair}" stroke="{LINE}" stroke-width="5"/>'
    o += f'<circle cx="0" cy="-114" r="38" fill="{hair}"/>'
    o += f'<path d="M14 -146 Q34 -136 36 -112" stroke="{rim}" stroke-width="6" fill="none" stroke-linecap="round" opacity=".8"/>'
    o += '<path d="M-18 -130 Q-6 -140 8 -136" stroke="#7a4a30" stroke-width="5" fill="none" stroke-linecap="round" opacity=".7"/>'
    return o


def puff(x, y, r, base, hi, op=1.0):
    return (f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r:.0f}" fill="{base}" opacity="{op:.2f}"/>'
            f'<circle cx="{x + r * .22:.0f}" cy="{y - r * .24:.0f}" r="{r * .72:.0f}" fill="{hi}" opacity="{op * .9:.2f}"/>')


def crown(x, y, r, pal, lx=.3, ly=-.45, sw=3):
    """cauliflower-like tree crown lit from (lx, ly); pal = (outline, dark, mid, light)"""
    o = ''
    subs = [(random.uniform(-.55, .55) * r, random.uniform(-.35, .3) * r, r * random.uniform(.42, .62)) for _ in range(6)]
    subs.sort(key=lambda t: t[1], reverse=True)
    o += ''.join(f'<circle cx="{x + a:.0f}" cy="{y + c:.0f}" r="{q + sw:.0f}" fill="{pal[0]}"/>' for a, c, q in subs)
    o += ''.join(f'<circle cx="{x + a:.0f}" cy="{y + c:.0f}" r="{q:.0f}" fill="{pal[1]}"/>' for a, c, q in subs)
    o += ''.join(f'<circle cx="{x + a + q * lx * .5:.0f}" cy="{y + c + q * ly * .5:.0f}" r="{q * .62:.0f}" fill="{pal[2]}"/>' for a, c, q in subs)
    o += ''.join(f'<circle cx="{x + a + q * lx:.0f}" cy="{y + c + q * ly:.0f}" r="{q * .26:.0f}" fill="{pal[3]}" opacity=".9"/>' for a, c, q in subs[-3:])
    return o


# ======================= A: ABOUT 2.5 MIN OF FALLING  (homage: Vertigo, the spiral poster with a falling figure) =======================
CX, CY, SY = 1330, 700, .86
d = rad('bgA', CX, CY, 1300, [(0, '#3a0a12', 1), (.18, '#7a1820', 1), (.5, '#c2381f', 1), (1, '#f07a2a', 1)])
d += rad('bandA', CX, CY, 1250, [(0, '#5a3a5a', 1), (.12, '#b07a8a', 1), (.35, '#f2b48a', 1), (.7, '#ffe2c0', 1), (1, '#fff4e4', 1)])
d += rad('sunA', 1760, 60, 900, [(0, '#fffbe8', .95), (.25, '#ffe8b0', .55), (1, '#ffd890', 0)])
d += rad('holeA', CX, CY, 120, [(0, '#bfe8a0', 1), (.5, '#6aa070', 1), (1, '#2a3a40', 1)])
d += rad('glA', 1220, 400, 330, [(0, '#fff3d6', .65), (.5, '#ffd9a0', .25), (1, '#ffd9a0', 0)])
d += rad('vigA', 960, 540, 1150, [(.55, '#000000', 0), (1, '#1a0408', .55)])
d += '<filter id="cl" x="-10%" y="-10%" width="120%" height="120%"><feTurbulence type="fractalNoise" baseFrequency="0.012" numOctaves="2" seed="3"/><feDisplacementMap in="SourceGraphic" scale="46" xChannelSelector="R" yChannelSelector="G"/></filter>'
d += '<filter id="bA"><feGaussianBlur stdDeviation="1.2"/></filter><filter id="bA2"><feGaussianBlur stdDeviation="14"/></filter>'
K = .115


def sp(th, ph, f=1.0):
    r = 34 * math.exp(K * th) * f
    return CX + r * math.cos(th + ph), CY + r * math.sin(th + ph) * SY, r


def band(ph, frac, th0=0, th1=31, step=.07):
    out_ = [sp(th0 + i * step, ph) for i in range(int((th1 - th0) / step) + 1)]
    f = math.exp(-math.pi * K * frac)
    in_ = [sp(th0 + i * step, ph, f) for i in range(int((th1 - th0) / step) + 1)][::-1]
    return 'M' + ' L'.join(f'{x:.1f} {y:.1f}' for x, y, _ in out_ + in_) + 'Z'


b = '<rect width="1920" height="1080" fill="url(#bgA)"/>'
# hole: the ground far below
b += f'<ellipse cx="{CX}" cy="{CY}" rx="120" ry="{120 * SY:.0f}" fill="url(#holeA)"/>'
b += f'<g opacity=".7">' + ''.join(f'<rect x="{CX + random.randint(-70, 50)}" y="{CY + random.randint(-55, 40)}" width="{random.randint(10, 26)}" height="{random.randint(8, 18)}" fill="{random.choice(["#8ab060", "#c9b46a", "#5f8a50"])}" transform="rotate(20 {CX} {CY})"/>' for _ in range(26)) + '</g>'
b += f'<path d="M{CX - 90} {CY + 30} C{CX - 40} {CY + 10} {CX - 10} {CY + 40} {CX + 30} {CY + 5} S{CX + 70} {CY - 30} {CX + 95} {CY - 20}" stroke="#d8f0ff" stroke-width="4" fill="none" opacity=".8"/>'
# spiral cloud bands (two arms), shaded puffs, highlight band
g = ''
for ph in (0, math.pi):
    g += f'<path d="{band(ph, .62)}" fill="url(#bandA)"/>'
b += f'<g filter="url(#cl)">{g}</g>'
pf = ''
for ph in (0, math.pi):
    th = 4.0
    while th < 31:
        x, y, r = sp(th, ph, .93)
        if r > 60 and random.random() < .8:
            fade = min(1, (r - 60) / 260)
            for _ in range(2):
                f2 = random.uniform(.88, 1.0)
                x, y, r = sp(th + random.uniform(-.05, .05), ph, f2)
                pf += puff(x, y, r * random.uniform(.06, .16), '#d98a7a' if r < 500 else '#f2b49a', '#fff2e2', .3 + .6 * fade)
        th += .12 + 12 / (r + 40)
b += f'<g filter="url(#bA)">{pf}</g>'
hl = ''.join(f'<path d="{band(ph + .1, .18, 8, 31)}" fill="#fffaf2" opacity=".45"/>' for ph in (0, math.pi))
b += f'<g filter="url(#bA2)">{hl}</g>'
b += '<rect width="1920" height="1080" fill="url(#sunA)"/>'
# radial speed streaks (rushing toward the centre)
for k in range(30):
    a = random.uniform(0, 2 * math.pi); r0 = random.uniform(330, 600); r1 = r0 + random.uniform(160, 420)
    b += f'<path d="M{CX + math.cos(a) * r0:.0f} {CY + math.sin(a) * r0 * SY:.0f} L{CX + math.cos(a) * r1:.0f} {CY + math.sin(a) * r1 * SY:.0f}" stroke="#fff6ea" stroke-width="{random.choice([2, 3, 4])}" stroke-linecap="round" opacity="{random.uniform(.15, .45):.2f}"/>'
b += '<rect width="1920" height="1080" fill="url(#vigA)"/>'
# the faller
b += '<rect width="1920" height="1080" fill="url(#glA)"/>'
b += f'<g transform="translate(1225 420) rotate(-16) scale(1.08)">' + faller() + '</g>'
b += spark(1560, 300, 22) + spark(980, 820, 16) + spark(1640, 690, 14) + spark(1450, 190, 12, op=.6)
open('A.html', 'w', encoding='utf-8').write(page('#7a1820', svg(d, b), [('ABOUT', 116, 'w'), ('2.5 MIN', 236, 'y'), ('OF FALLING', 136, 'w')], '#2a0610', top=44))

# ======================= B: WHERE WOULD YOU LAND?  (intuitive: lake / forest canopy / deep snow slope) =======================
random.seed(11)
HZ = 520
d = lin('skB', [(0, '#2a5a94'), (.55, '#7fb2d8'), (1, '#e6f2f6')])
d += rad('sunB', 1640, 110, 700, [(0, '#fffbe8', 1), (.12, '#fff3c8', .9), (.4, '#ffe8b0', .3), (1, '#ffe8b0', 0)])
d += lin('lakeB', [(0, '#5f8ab0'), (.35, '#1f4a72'), (1, '#0a1e36')])
d += lin('snowB', [(0, '#ffffff'), (.6, '#e2eef8'), (1, '#9fbcd8')], x2=1, y2=1)
d += rad('glowT', 960, 760, 380, [(0, '#fff2b0', .55), (1, '#fff2b0', 0)])
d += rad('glowS', 1560, 640, 420, [(0, '#fffbe0', .6), (1, '#fffbe0', 0)])
d += '<filter id="bB"><feGaussianBlur stdDeviation="6"/></filter><filter id="bB2"><feGaussianBlur stdDeviation="2"/></filter>'
b = '<rect width="1920" height="1080" fill="url(#skB)"/><rect width="1920" height="1080" fill="url(#sunB)"/>'
b += '<circle cx="1640" cy="110" r="52" fill="#fffef6"/>'
b += blobs(14, 700, 160, 1500, 380, '#ffffff', .25, .5, 60, 160).replace('<ellipse', '<ellipse filter="url(#bB)"')
# far mountains
b += f'<path d="M0 {HZ} L120 430 L220 470 L360 380 L470 455 L600 400 L740 470 L860 420 L980 {HZ} Z" fill="#7d97b8"/>'
b += f'<path d="M360 380 L400 410 L380 418 L420 440 L330 410Z M600 400 L640 430 L560 428Z" fill="#eef6fb"/>'
b += f'<path d="M820 {HZ} L960 410 L1060 450 L1180 360 L1300 {HZ}Z" fill="#6f8aae"/><path d="M1180 360 L1222 398 L1196 400 L1214 420 L1150 392Z" fill="#eef6fb"/>'
b += f'<rect x="0" y="{HZ - 6}" width="1920" height="40" fill="#c8dcec" opacity=".6" filter="url(#bB)"/>'
# forest canopy (middle): dense cauliflower crowns, layered back to front
fo = '<path d="M600 1080 L640 600 C800 575 1100 580 1480 560 L1060 1080Z" fill="#12321e"/>'
y = 585
while y < 1130:
    rr = 30 + (y - 585) * .11
    x = 600 + random.uniform(0, rr)
    while x < 1500 - (y - 520) * .79 + rr * .3:
        fo += crown(x, y + random.uniform(-.2, .2) * rr, rr * random.uniform(.85, 1.2), random.choice((('#0c2414', '#1d5a2c', '#3f9440', '#9ad86a'), ('#0c2414', '#245a26', '#4f9a3a', '#b4e070'), ('#0c2414', '#1a4e34', '#358a52', '#8fd48a'))))
        x += rr * random.uniform(1.0, 1.35)
    y += rr * .62
b += fo
# lake (left): flat, hard, glassy
b += f'<path d="M0 {HZ + 40} C200 {HZ + 30} 420 {HZ + 46} 640 {HZ + 70} C700 {HZ + 120} 690 900 600 1080 L0 1080Z" fill="url(#lakeB)" stroke="#3a5a3a" stroke-width="8"/>'
b += ''.join(f'<path d="M{x} {y} h{w}" stroke="#e8f6ff" stroke-width="{s}" stroke-linecap="round" opacity="{o}"/>' for x, y, w, s, o in
             ((80, 640, 260, 4, .7), (300, 700, 220, 3, .5), (40, 780, 420, 5, .55), (180, 880, 300, 4, .45), (60, 980, 360, 5, .35), (420, 610, 140, 3, .6)))
b += '<path d="M120 600 L560 600 L520 1080 L60 1080Z" fill="#cfe6f6" opacity=".08"/>'
b += f'<path d="M0 {HZ + 40} C200 {HZ + 30} 420 {HZ + 46} 640 {HZ + 70}" stroke="#2c4a2e" stroke-width="16" fill="none"/>'
# snowy mountain slope (right)
SL = f'M1060 1080 C1200 900 1330 700 1500 520 C1600 410 1700 330 1790 250 L1920 200 L1920 1080Z'
b += f'<path d="{SL}" fill="url(#snowB)" stroke="#5a7fa8" stroke-width="5"/>'
b += f'<path d="M1790 250 C1760 420 1820 600 1920 700 L1920 200Z" fill="#a9c4de" opacity=".7"/>'
b += f'<path d="M1500 520 C1520 650 1610 780 1760 860" stroke="#b8d0e6" stroke-width="10" fill="none" opacity=".8"/>'
for k in range(10):
    y = 600 + k * 46; x = 1330 - (y - 600) * .55
    b += f'<path d="M{x + 60 + k * 10:.0f} {y} q90 -30 200 -6 q80 14 170 -24" stroke="#ffffff" stroke-width="6" fill="none" opacity=".7"/>'
b += '<rect width="1920" height="1080" fill="url(#glowS)"/>'
for x, y, s in ((1640, 372, 1), (1690, 330, .8), (1730, 300, .7), (1585, 420, .9)):
    b += f'<path d="M{x} {y - 50 * s} L{x + 18 * s} {y} L{x - 18 * s} {y}Z" fill="#1f4a3a"/><path d="M{x} {y - 50 * s} L{x + 8 * s} {y - 30 * s} L{x - 6 * s} {y - 26 * s}Z" fill="#ffffff" opacity=".8"/>'
b += '<rect width="1920" height="1080" fill="url(#glowT)" opacity=".8"/>'
# soft golden halos on the forgiving surfaces, faint dotted paths from the faller
for x0, y0, x1, y1, cx_, cy_ in ((1150, 350, 420, 820, 760, 470), (1175, 390, 960, 780, 1090, 560), (1205, 380, 1560, 650, 1440, 430)):
    b += f'<path d="M{x0} {y0} Q{cx_} {cy_} {x1} {y1}" stroke="#ffffff" stroke-width="7" stroke-dasharray="2 22" stroke-linecap="round" fill="none" opacity=".75"/>'
b += spark(960, 760, 28) + spark(1560, 640, 28) + spark(1040, 820, 16) + spark(1660, 560, 16) + spark(820, 760, 14, op=.7)
b += f'<g transform="translate(1180 300) rotate(10) scale(.62)">' + faller(suit='#d8572e', suit2='#9a3218', rim='#fff2c0') + '</g>'
open('B.html', 'w', encoding='utf-8').write(page('#2a5a94', svg(d, b), [('WHERE', 140, 'w'), ('WOULD YOU', 150, 'w'), ('LAND?', 236, 'y')], '#0a1a30', top=40))

# ======================= C: SHE FELL IN HER SEAT  (intuitive: a seat row spinning like a rotor over the rainforest) =======================
random.seed(5)
HZ = 735
SX, SYc = 1290, 470
d = lin('skC', [(0, '#1c2030'), (.5, '#3a4258'), (1, '#8a9a8a')])
d += rad('gapC', SX + 40, SYc - 60, 620, [(0, '#fff4d0', 1), (.2, '#ffe6a8', .8), (.5, '#e8c68a', .3), (1, '#e8c68a', 0)])
d += lin('fab', [(0, '#3a6cb0'), (1, '#1a3768')], x2=1, y2=0)
d += lin('hr', [(0, '#fbf6ea'), (1, '#cfc6b4')])
d += lin('canC', [(0, '#5a7a6a'), (.2, '#2e5a3a'), (1, '#0c2416')])
d += lin('mistC', [(0, '#ffffff'), (1, '#ffffff')])
d += '<filter id="bC"><feGaussianBlur stdDeviation="8"/></filter><filter id="bC2"><feGaussianBlur stdDeviation="3"/></filter>'
d += '<filter id="clC" x="-10%" y="-10%" width="120%" height="120%"><feTurbulence type="fractalNoise" baseFrequency="0.01" numOctaves="3" seed="8"/><feDisplacementMap in="SourceGraphic" scale="40" xChannelSelector="R" yChannelSelector="G"/></filter>'
b = '<rect width="1920" height="1080" fill="url(#skC)"/>'
# storm clouds: dark puffs, warm rims toward the bright gap
cl = ''
for _ in range(150):
    x = random.randint(-60, 1980); y = random.randint(-60, 420)
    dist = math.hypot(x - SX, (y - SYc) * 1.6)
    if dist < 330:
        continue
    r = random.randint(50, 130)
    rim = '#f0d49a' if dist < 650 else ('#8a8494' if dist < 900 else '#454a62')
    dx, dy = (SX - x) / dist * r * .12, (SYc - y) / dist * r * .12
    base = random.choice(["#2a2e42", "#323850", "#262a3c"])
    cl += f'<circle cx="{x}" cy="{y}" r="{r}" fill="{base}"/><circle cx="{x + dx:.0f}" cy="{y + dy:.0f}" r="{r * .8:.0f}" fill="{rim}" opacity="{.75 if dist < 650 else .45}"/><circle cx="{x - dx * .3:.0f}" cy="{y - dy * .3:.0f}" r="{r * .74:.0f}" fill="{base}" opacity=".55"/>'
b += '<rect width="1920" height="1080" fill="url(#gapC)"/>'
b += f'<g filter="url(#bC)">{cl}</g>'
b += ''.join(f'<path d="M{x} {y} l-{random.randint(30, 60)} {random.randint(120, 220)}" stroke="#c8d0e0" stroke-width="2" opacity="{random.uniform(.15, .4):.2f}"/>' for x, y in ((random.randint(0, 1920), random.randint(0, 700)) for _ in range(110)))
# rainforest canopy
b += f'<path d="M0 {HZ} C400 {HZ - 20} 900 {HZ + 10} 1920 {HZ - 15} L1920 1080 L0 1080Z" fill="url(#canC)"/>'
for row, (yb, rr, pal) in enumerate(((HZ + 8, 20, ('#30483e', '#4a6a5a', '#6a8a72', '#9ab494')), (HZ + 55, 34, ('#14301c', '#2a5232', '#3e7a40', '#7ab65a')),
                                      (HZ + 130, 54, ('#0c2414', '#1e4a28', '#357a36', '#86c45c')), (HZ + 240, 80, ('#0a1e10', '#163a20', '#2e6e30', '#9ad468')),
                                      (HZ + 380, 110, ('#081a0e', '#12321a', '#2a6a2c', '#a8e070')))):
    x = -40
    while x < 1980:
        r = rr * random.uniform(.85, 1.3)
        b += crown(x, yb + random.uniform(-.3, .3) * rr, r, pal, lx=.05, ly=-.6, sw=2 + row)
        x += r * random.uniform(1.0, 1.4)
    b += f'<rect x="0" y="{yb - 24}" width="1920" height="44" fill="#e6f0ea" opacity="{.22 - row * .03:.2f}" filter="url(#bC)"/>'
# rotor swooshes behind the seats
b += f'<g filter="url(#bC2)"><ellipse cx="{SX}" cy="{SYc + 70}" rx="470" ry="120" fill="none" stroke="#fff6dc" stroke-width="10" stroke-dasharray="520 260" opacity=".55"/>'
b += f'<ellipse cx="{SX}" cy="{SYc + 70}" rx="400" ry="96" fill="none" stroke="#fff6dc" stroke-width="5" stroke-dasharray="300 180" stroke-dashoffset="200" opacity=".45"/></g>'


def seatrow(fill='url(#fab)', hrc='url(#hr)', person=True, ghost=False):
    o = ''
    W, H = 150, 236
    if person:   # top of the middle passenger's head + hair streaming up in the wind (seen from behind)
        hx = 160 + W / 2
        o += f'<g stroke="{LINE}" stroke-width="5" fill="#4a2a1a">'
        for dx, h, bend, w in ((-26, 150, -150, 13), (-4, 175, -110, 15), (18, 140, -70, 12)):
            o += (f'<path d="M{hx + dx - w} -20 C{hx + dx - w + 10} {-h * .5} {hx + dx + bend + 40} {-h * .45} {hx + dx + bend} {-h} '
                  f'C{hx + dx + bend + 70} {-h * .6} {hx + dx + w + 20} {-h * .5} {hx + dx + w} -20Z"/>')
        o += f'<ellipse cx="{hx}" cy="-4" rx="50" ry="46"/></g>'
        o += f'<path d="M{hx - 4} -40 Q{hx + 22} -42 {hx + 36} -18" stroke="#c08050" stroke-width="5" fill="none" stroke-linecap="round"/>'
    for i in range(3):
        x = i * 160
        if ghost:
            o += f'<rect x="{x}" y="0" width="{W}" height="{H}" rx="28" fill="#fff6dc"/>'
            continue
        o += f'<path d="M{x + W - 10} 14 L{x + W + 16} 30 L{x + W + 16} {H + 6} L{x + W - 6} {H}Z" fill="#12244a" stroke="{LINE}" stroke-width="5" stroke-linejoin="round"/>'
        o += f'<rect x="{x}" y="0" width="{W}" height="{H}" rx="28" fill="{fill}" stroke="{LINE}" stroke-width="6"/>'
        o += f'<path d="M{x + 12} 30 Q{x + 6} {H / 2} {x + 14} {H - 20}" stroke="#7aa6e0" stroke-width="6" fill="none" opacity=".55"/>'
        o += f'<path d="M{x + W - 12} 30 Q{x + W - 4} {H / 2} {x + W - 14} {H - 20}" stroke="#ffe2a0" stroke-width="5" fill="none" opacity=".8"/>'
        o += f'<rect x="{x + 16}" y="12" width="{W - 32}" height="62" rx="14" fill="{hrc}" stroke="{LINE}" stroke-width="4"/>'
        o += f'<rect x="{x + 24}" y="92" width="{W - 48}" height="68" rx="8" fill="#c9ced8" stroke="{LINE}" stroke-width="4"/>'
        o += f'<rect x="{x + W / 2 - 12}" y="96" width="24" height="9" rx="3" fill="#6a7080"/>'
        o += f'<path d="M{x + 22} {H - 62} h{W - 44} v40 q0 8 -8 8 h{-(W - 60)} q-8 0 -8 -8Z" fill="#244a86" stroke="{LINE}" stroke-width="4"/>'
        o += f'<path d="M{x + 24} {H - 56} h{W - 48}" stroke="#7aa6e0" stroke-width="3" opacity=".7"/>'
    if not ghost:   # metal frame under the row
        o += f'<rect x="-6" y="{H - 6}" width="{480 + 12}" height="22" rx="8" fill="#9aa2b0" stroke="{LINE}" stroke-width="5"/>'
        o += f'<path d="M-4 {H} h{480 + 8}" stroke="#e8eef6" stroke-width="4" opacity=".7"/>'
        for lx in (70, 390):
            o += f'<path d="M{lx} {H + 14} L{lx - 18} {H + 82} M{lx} {H + 14} L{lx + 22} {H + 82}" stroke="{LINE}" stroke-width="20" stroke-linecap="round"/>'
            o += f'<path d="M{lx} {H + 14} L{lx - 18} {H + 82} M{lx} {H + 14} L{lx + 22} {H + 82}" stroke="#aab2c0" stroke-width="12" stroke-linecap="round"/>'
            o += f'<path d="M{lx - 26} {H + 84} h60" stroke="{LINE}" stroke-width="16" stroke-linecap="round"/><path d="M{lx - 26} {H + 84} h60" stroke="#8a92a0" stroke-width="9" stroke-linecap="round"/>'
    return o


T = f'translate({SX} {SYc}) rotate(-9) scale(1.18) translate(-240 -150)'
b += f'<g transform="translate({SX} {SYc}) scale(.55 1) translate(-{SX} -{SYc})" opacity=".3" filter="url(#bC2)"><g transform="{T}">{seatrow(person=False, ghost=True)}</g></g>'
b += f'<g transform="translate({SX + 60} {SYc}) scale(.25 1) translate(-{SX} -{SYc})" opacity=".2" filter="url(#bC2)"><g transform="{T}">{seatrow(person=False, ghost=True)}</g></g>'
b += f'<g transform="{T}">{seatrow()}</g>'
b += f'<g filter="url(#bC2)"><path d="M{SX - 470} {SYc + 70} A470 120 0 0 0 {SX + 140} {SYc + 186}" fill="none" stroke="#fff6dc" stroke-width="12" opacity=".7"/></g>'
b += f'<path d="M{SX + 140} {SYc + 186} l-34 -20 m34 20 l-30 22" stroke="#fff6dc" stroke-width="10" stroke-linecap="round" fill="none" opacity=".75"/>'
b += spark(1720, 300, 22) + spark(880, 380, 16) + spark(1600, 660, 14, op=.7)
open('C.html', 'w', encoding='utf-8').write(page('#1c2030', svg(d, b), [('SHE FELL', 168, 'w'), ('IN HER', 128, 'w'), ('SEAT', 250, 'y')], '#0a0c16', top=40))
print('ok')
