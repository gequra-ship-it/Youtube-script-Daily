import sys, math, random
sys.path.insert(0, '/home/user/rp/tools')
from thumb_lib import *
random.seed(21)


def palm(x, y, h, lean=0, trunk='#5a3a1a', leaf='#3fae5a', edge='#1f6a38', sw=3, fronds=7, span=1.0):
    """date palm, base at (x, y), height h; returns svg"""
    tx, ty = x + lean, y - h
    o = f'<path d="M{x - h * .035:.0f} {y} Q{x + lean * .4:.0f} {y - h * .55:.0f} {tx - h * .02:.0f} {ty} L{tx + h * .02:.0f} {ty} Q{x + lean * .4 + h * .05:.0f} {y - h * .5:.0f} {x + h * .035:.0f} {y}Z" fill="{trunk}"/>'
    for k in range(1, 9):  # trunk rings
        t = k / 9; px = x + (tx - x) * t; py = y - h * t
        o += f'<path d="M{px - h * .03:.0f} {py:.0f} q{h * .03:.0f} {h * .015:.0f} {h * .06:.0f} 0" stroke="#2a1a0c" stroke-width="{max(1, h * .008):.1f}" fill="none" opacity=".5"/>'
    L = h * .55 * span
    for k in range(fronds):
        a = math.radians(-170 + k * (160 / (fronds - 1)))
        ex, ey = tx + math.cos(a) * L, ty + math.sin(a) * L * .55 + L * .35 * abs(math.cos(a))
        mx, my = tx + math.cos(a) * L * .55, ty - L * .25 + L * .1 * abs(math.cos(a))
        o += f'<path d="M{tx:.0f} {ty:.0f} Q{mx:.0f} {my - L * .12:.0f} {ex:.0f} {ey:.0f} Q{mx:.0f} {my + L * .1:.0f} {tx:.0f} {ty + L * .05:.0f}Z" fill="{leaf}" stroke="{edge}" stroke-width="{sw}" stroke-linejoin="round"/>'
    o += f'<circle cx="{tx:.0f}" cy="{ty + h * .03:.0f}" r="{h * .03:.0f}" fill="#b5602a"/>'
    return o


# ======================= A: MIRAGE OR REAL?  (homage: Lawrence of Arabia, the rider out of the mirage) =======================
d = lin('sk', [(0, '#c0703c'), (.45, '#efc58a'), (.9, '#fff1d2'), (1, '#fffaf0')])
d += lin('sd', [(0, '#f1d39c'), (.25, '#e2b57a'), (1, '#8e5428')])
d += rad('sun', 1500, 250, 520, [(0, '#ffffff', 1), (.12, '#fffbe8', 1), (.2, '#fff0c0', .7), (.5, '#ffd890', .25), (1, '#ffd890', 0)])
d += '<linearGradient id="mir" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff6e2" stop-opacity="0"/><stop offset=".35" stop-color="#d9eef2" stop-opacity=".95"/><stop offset=".7" stop-color="#a9d4e0" stop-opacity=".9"/><stop offset="1" stop-color="#e9c48c" stop-opacity="0"/></linearGradient>'
d += '<linearGradient id="rf" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff" stop-opacity=".75"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient><mask id="rm"><rect x="0" y="700" width="1920" height="260" fill="url(#rf)"/></mask>'
d += '<filter id="heat" x="-20%" y="-20%" width="140%" height="140%"><feTurbulence type="fractalNoise" baseFrequency="0.004 0.09" numOctaves="2" seed="4"/><feDisplacementMap in="SourceGraphic" scale="14" xChannelSelector="R" yChannelSelector="G"/></filter>'
d += '<filter id="heat2" x="-20%" y="-20%" width="140%" height="140%"><feTurbulence type="fractalNoise" baseFrequency="0.003 0.06" numOctaves="2" seed="9"/><feDisplacementMap in="SourceGraphic" scale="34" xChannelSelector="R" yChannelSelector="G"/></filter>'
d += '<filter id="bl"><feGaussianBlur stdDeviation="2.2"/></filter>'
H = 700
b = '<rect width="1920" height="1080" fill="url(#sk)"/><rect width="1920" height="1080" fill="url(#sun)"/>'
b += '<circle cx="1500" cy="250" r="74" fill="#fffef6"/>'
b += ''.join(f'<path d="M{1500 + math.cos(a) * 110:.0f} {250 + math.sin(a) * 110:.0f} L{1500 + math.cos(a) * 190:.0f} {250 + math.sin(a) * 190:.0f}" stroke="#fff8dc" stroke-width="5" stroke-linecap="round" opacity=".55"/>' for a in [k * math.pi / 8 for k in range(16)])
b += f'<path d="M0 {H - 18} C200 {H - 50} 360 {H - 30} 520 {H - 12} L520 {H} L0 {H}Z" fill="#d8b48a" opacity=".7"/>'
b += f'<path d="M1650 {H} C1720 {H - 40} 1820 {H - 52} 1920 {H - 30} L1920 {H}Z" fill="#d6ad80" opacity=".7"/>'
b += f'<rect x="0" y="{H}" width="1920" height="{1080 - H}" fill="url(#sd)"/>'
b += blobs(120, 0, H + 60, 1920, 1080, '#7a4420', .05, .14, 20, 90) + blobs(80, 0, H + 20, 1920, 1080, '#ffe6b8', .05, .12, 10, 60)
grove = ''.join(palm(x, H + 6, h, lean=l, trunk='#4a3a32', leaf='#4e7a5e', edge='#3a5a48', sw=2, span=1.05) for x, h, l in ((1130, 150, -6), (1190, 200, 8), (1260, 140, -4), (1320, 180, 10), (1400, 120, 4), (1460, 165, -8), (1530, 125, 6)))
b += f'<g filter="url(#heat)"><rect x="0" y="{H - 30}" width="1920" height="90" fill="url(#mir)"/>'
b += f'<g opacity=".8">{grove}</g><g transform="translate(0 {2 * H + 12}) scale(1 -1)" opacity=".45">{grove}</g>'
b += ''.join(f'<path d="M{random.randint(0, 1900)} {random.randint(H - 10, H + 40)} h{random.randint(60, 260)}" stroke="#ffffff" stroke-width="3" opacity="{random.uniform(.35, .8):.2f}"/>' for _ in range(40)) + '</g>'


def rider(col):
    # camel walking left with a robed rider; feet at y=0, ~300 tall
    o = f'<g fill="{col}">'
    o += '<ellipse cx="0" cy="-150" rx="80" ry="36"/><ellipse cx="6" cy="-180" rx="46" ry="34"/>'
    o += '<path d="M-62 -168 Q-96 -170 -104 -205 Q-110 -228 -128 -232 L-150 -228 Q-160 -220 -150 -212 L-132 -214 Q-120 -190 -112 -160 Q-100 -140 -60 -132Z"/>'
    o += '<path d="M-150 -226 l-6 -10 l8 2Z"/>'
    for lx, sw in ((-52, -10), (-30, 8), (40, -6), (62, 10)):
        o += f'<path d="M{lx - 7} -140 L{lx + 7} -140 L{lx + sw * .6 + 5} -70 L{lx + sw + 4} 0 L{lx + sw - 6} 0 L{lx + sw * .6 - 5} -70Z"/><ellipse cx="{lx + sw * .6}" cy="-72" rx="8" ry="7"/>'
    o += '<path d="M78 -160 Q96 -130 88 -105" stroke="' + col + '" stroke-width="7" fill="none"/>'
    o += '<path d="M-20 -200 L20 -200 L14 -262 Q4 -276 -8 -268 L-22 -230Z"/>'
    o += '<circle cx="2" cy="-284" r="17"/><path d="M-14 -290 Q2 -312 20 -290 L58 -250 Q80 -232 96 -236 Q72 -214 40 -228 L12 -262Z"/>'
    o += '<path d="M10 -260 Q60 -248 100 -212 Q120 -190 132 -196 Q116 -170 86 -180 Q50 -196 14 -224Z" opacity=".85"/>'
    o += '<path d="M-14 -246 L-44 -232" stroke="' + col + '" stroke-width="9" stroke-linecap="round"/>'
    return o + '</g>'


RX, RY, RS = 900, H + 95, 1.08
b += f'<g filter="url(#heat2)" mask="url(#rm)"><g transform="translate({RX} {RY + 2}) scale({RS} {-RS * 1.6})" opacity=".55">{rider("#3a2418")}</g></g>'
b += f'<ellipse cx="{RX}" cy="{RY + 4}" rx="90" ry="9" fill="#5a3218" opacity=".35" filter="url(#bl)"/>'
b += f'<g filter="url(#heat)"><g transform="translate({RX} {RY}) scale({RS})">{rider("#2a1810")}</g></g>'
b += f'<g transform="translate({RX + 3} {RY - 2}) scale({RS})" opacity=".55" filter="url(#bl)"><path d="M14 -262 Q20 -290 6 -300" stroke="#fff3c0" stroke-width="5" fill="none"/><path d="M50 -186 Q86 -170 80 -150" stroke="#fff3c0" stroke-width="5" fill="none"/></g>'
for k in range(14):
    t = k / 13; x = RX - 40 - t * 640 + math.sin(k * 1.3) * 18 * (1 + t * 3); y = RY + 30 + (t ** 1.4) * 330
    s = 6 + t * 30; side = -1 if k % 2 else 1
    b += f'<ellipse cx="{x + side * s * .9:.0f}" cy="{y:.0f}" rx="{s:.0f}" ry="{s * .42:.0f}" fill="#7a4420" opacity="{.25 + t * .35:.2f}"/><ellipse cx="{x + side * s * .9:.0f}" cy="{y - s * .12:.0f}" rx="{s * .8:.0f}" ry="{s * .28:.0f}" fill="#f6d9a6" opacity="{.15 + t * .25:.2f}"/>'
for k in range(9):
    y = 830 + k * 30
    b += f'<path d="M{-40 + k * 30} {y} C{300 + k * 40} {y - 30} {700} {y + 20} {1100 - k * 20} {y - 10}" stroke="#fbe3b4" stroke-width="{3 + k * .6:.1f}" fill="none" opacity="{.18 + k * .03:.2f}"/>'
b += f'<rect x="0" y="960" width="1920" height="120" fill="#5a3014" opacity=".25"/>'
b += spark(1080, 640, 20) + spark(1390, 600, 16) + spark(860, 520, 14, op=.6)
open('A.html', 'w', encoding='utf-8').write(page('#c0703c', svg(d, b), [('MIRAGE', 230, 'y'), ('OR REAL?', 190, 'w')], '#3a1a0a', top=50))

# ======================= B: UP TO 1 MILLION YEARS OLD  (intuitive: fossil water under the dunes) =======================
S = 520
d = lin('sk', [(0, '#2a1640'), (.55, '#a84a4a'), (1, '#f2a860')])
d += lin('l1', [(0, '#e9b56e'), (1, '#c8843e')]) + lin('l2', [(0, '#a85a34'), (1, '#7a3a22')])
d += lin('aq', [(0, '#1a6a78'), (.5, '#0f4a5a'), (1, '#0a2a38')]) + lin('l5', [(0, '#3a2a2c'), (1, '#140c10')])
d += rad('ag', 1150, 860, 620, [(0, '#8ff8ea', .9), (.35, '#4fd8d0', .45), (1, '#4fd8d0', 0)])
d += rad('sg', 1460, S - 10, 220, [(0, '#bff8ff', .8), (1, '#bff8ff', 0)])
d += '<filter id="gl"><feGaussianBlur stdDeviation="10"/></filter>'
AQ = 'M0 790 C400 740 800 770 1200 745 C1500 728 1750 760 1920 750 L1920 940 C1600 965 1200 950 800 975 C500 990 200 960 0 975Z'
d += f'<clipPath id="aqc"><path d="{AQ}"/></clipPath>'
b = '<rect width="1920" height="1080" fill="url(#sk)"/>' + stars(60, 300, 0, '#ffe8d0', .6, 3)
b += '<circle cx="1720" cy="150" r="46" fill="#fff4dc"/><circle cx="1738" cy="138" r="44" fill="#4a2244"/>'
b += f'<path d="M0 {S} C200 {S - 60} 420 {S - 90} 640 {S - 20} C800 {S - 110} 1000 {S - 130} 1180 {S - 10} L1920 {S + 10} L1920 {S + 30} L0 {S + 30}Z" fill="#d9a060"/>'
b += f'<path d="M640 {S - 20} C800 {S - 110} 1000 {S - 130} 1180 {S - 10}" stroke="#ffd79a" stroke-width="4" fill="none"/>'
b += f'<path d="M0 {S + 20} C500 {S + 5} 1300 {S + 20} 1920 {S + 10} L1920 640 C1400 660 700 640 0 660Z" fill="url(#l1)"/>'
b += '<path d="M0 660 C700 640 1400 660 1920 640 L1920 760 C1500 768 1200 735 800 772 C400 752 200 790 0 800Z" fill="url(#l2)"/>'
b += blobs(60, 0, 670, 1920, 760, '#4a1e10', .15, .3, 6, 22)
b += '<path d="M0 800 C200 790 400 752 800 772 C1200 735 1500 768 1920 750 L1920 760 C1750 770 1500 738 1200 755 C800 780 400 750 0 810Z" fill="#5a4a50"/>'
b += f'<path d="{AQ}" fill="url(#aq)"/>'
b += '<g clip-path="url(#aqc)"><rect width="1920" height="1080" fill="url(#ag)"/>'
b += ''.join(f'<circle cx="{random.randint(0, 1920)}" cy="{random.randint(740, 990)}" r="{random.choice([3, 4, 5, 7, 9])}" fill="#d8fff8" opacity="{random.uniform(.25, .85):.2f}"/>' for _ in range(260))
b += ''.join(f'<ellipse cx="{random.randint(0, 1920)}" cy="{random.randint(760, 980)}" rx="{random.randint(10, 26)}" ry="{random.randint(7, 15)}" fill="#0a2a34" opacity="{random.uniform(.3, .6):.2f}" stroke="#8ff8ea" stroke-width="1.5" stroke-opacity=".4"/>' for _ in range(90))
b += ''.join(f'<path d="M{x} {y} q30 -8 60 0 q30 8 60 0" stroke="#bff8ff" stroke-width="3" fill="none" opacity=".55"/>' for x, y in ((300, 860), (700, 900), (1000, 820), (1350, 880), (520, 930), (1600, 830)))
b += '</g><path d="M0 790 C400 740 800 770 1200 745 C1500 728 1750 760 1920 750" stroke="#8ff8ea" stroke-width="4" fill="none" opacity=".8"/>'
b += '<path d="M0 975 C200 960 500 990 800 975 C1200 950 1600 965 1920 940 L1920 1080 L0 1080Z" fill="url(#l5)"/>'
crack = f'M1300 770 C1330 700 1400 690 1390 640 C1380 590 1450 580 1455 {S + 12}'
b += f'<path d="{crack}" stroke="#1a0c08" stroke-width="30" fill="none" stroke-linejoin="round"/><path d="{crack}" stroke="#8ff8ea" stroke-width="30" fill="none" filter="url(#gl)" stroke-linejoin="round"/><path d="{crack}" stroke="#e6fffb" stroke-width="12" fill="none" stroke-linejoin="round"/>'
for x, y in ((1340, 715), (1402, 625), (1432, 575)):
    b += f'<path d="M{x - 30} {y + 22} L{x - 20} {y + 4} L{x - 10} {y + 22}" stroke="#ffffff" stroke-width="5" fill="none" stroke-linecap="round"/><path d="M{x + 10} {y + 22} L{x + 20} {y + 4} L{x + 30} {y + 22}" stroke="#ffffff" stroke-width="5" fill="none" stroke-linecap="round"/>'
b += '<rect width="1920" height="1080" fill="url(#sg)"/>'
b += f'<ellipse cx="1460" cy="{S + 12}" rx="130" ry="16" fill="#5fd0e0" stroke="#e6fffb" stroke-width="3"/>'
for x, h, l in ((1330, 150, -18), (1380, 200, -6), (1540, 180, 14), (1600, 130, 20), (1470, 120, 4)):
    b += palm(x, S + 14, h, lean=l, trunk='#3a2410', leaf='#3a9a52', edge='#16502a', sw=3)
for k, x in enumerate((1700, 1760, 1820)):
    y = S + 14
    b += f'<g transform="translate({x} {y}) scale(.22)" fill="#2a1424"><ellipse cx="0" cy="-150" rx="80" ry="36"/><ellipse cx="6" cy="-180" rx="46" ry="34"/><path d="M-62 -168 Q-100 -175 -110 -220 L-140 -228 L-130 -212 Q-120 -180 -60 -132Z"/>' + ''.join(f'<rect x="{lx}" y="-140" width="14" height="140"/>' for lx in (-58, -34, 34, 56)) + '</g>'
b += spark(1200, 820, 20, '#e6fffb') + spark(600, 870, 16, '#e6fffb') + spark(1560, 400, 16)
open('B.html', 'w', encoding='utf-8').write(page('#2a1640', svg(d, b), [('UP TO', 110, 'w'), ('1 MILLION', 190, 'y'), ('YEARS OLD', 150, 'w')], '#140818', top=36))

# ======================= C: THE SAHARA WAS GREEN  (homage: The Lion King opening, animals before the giant sun) =======================
HZ = 760
d = lin('sk', [(0, '#7a2a3a'), (.35, '#d8603a'), (.7, '#f6a646'), (1, '#ffd88a')])
d += rad('sn', 1150, HZ - 60, 760, [(0, '#fff2c0', 1), (.3, '#ffcf6a', .7), (.6, '#ff9a40', .25), (1, '#ff9a40', 0)])
d += lin('gr', [(0, '#6a8a2a'), (.4, '#3f6a24'), (1, '#16280e')]) + lin('lk', [(0, '#ffd88a'), (1, '#c8603a')])
b = '<rect width="1920" height="1080" fill="url(#sk)"/><rect width="1920" height="1080" fill="url(#sn)"/>'
b += f'<circle cx="1150" cy="{HZ - 40}" r="340" fill="#ffe7a0" opacity=".95"/><circle cx="1150" cy="{HZ - 40}" r="300" fill="#fff4cc"/>'
for y, x, w in ((470, 820, 520), (520, 1200, 420), (580, 760, 380), (395, 1250, 300)):
    b += f'<rect x="{x}" y="{y}" width="{w}" height="10" rx="5" fill="#d8603a" opacity=".55"/>'
b += spark(560, 520, 18) + spark(1700, 360, 20) + stars(14, 340, 900, '#fff0d0', .5, 0)
b += f'<path d="M0 {HZ} C200 {HZ - 40} 420 {HZ - 20} 600 {HZ - 6} C760 {HZ - 30} 900 {HZ - 10} 1920 {HZ} L1920 {HZ + 10} L0 {HZ + 10}Z" fill="#8a3a30" opacity=".75"/>'


def acacia(x, y, s, col):
    return (f'<g fill="{col}"><path d="M{x - 6 * s} {y} L{x - 2 * s} {y - 60 * s} L{x - 30 * s} {y - 95 * s} L{x - 26 * s} {y - 99 * s} L{x} {y - 70 * s} L{x + 28 * s} {y - 104 * s} L{x + 32 * s} {y - 100 * s} L{x + 4 * s} {y - 60 * s} L{x + 6 * s} {y}Z"/>'
            f'<ellipse cx="{x}" cy="{y - 108 * s}" rx="{85 * s}" ry="{16 * s}"/><ellipse cx="{x - 30 * s}" cy="{y - 116 * s}" rx="{45 * s}" ry="{11 * s}"/><ellipse cx="{x + 34 * s}" cy="{y - 114 * s}" rx="{42 * s}" ry="{10 * s}"/></g>')


b += acacia(260, HZ, 1.1, '#4a1a20') + acacia(620, HZ + 4, .7, '#5a2226') + acacia(1820, HZ, .9, '#4a1a20')
b += f'<path d="M1430 {HZ + 10} L1460 640 L1500 560 L1560 520 L1700 500 L1840 470 L1870 486 L1760 540 L1720 600 L1740 680 L1780 {HZ + 10}Z" fill="#3a1a1c"/>'
b += '<path d="M1560 520 L1700 500 L1840 470 L1870 486" stroke="#ffcf6a" stroke-width="6" fill="none" stroke-linejoin="round"/><path d="M1500 560 L1560 520" stroke="#ffcf6a" stroke-width="4" fill="none"/>'
b += f'<path d="M560 {HZ + 18} C800 {HZ + 6} 1500 {HZ + 8} 1700 {HZ + 24} C1500 {HZ + 70} 800 {HZ + 72} 560 {HZ + 18}Z" fill="url(#lk)"/>'
b += ''.join(f'<rect x="{1150 - w // 2}" y="{HZ + 22 + k * 8}" width="{w}" height="4" rx="2" fill="#fff4cc" opacity=".8"/>' for k, w in enumerate((420, 360, 300, 230, 160)))


def giraffe(x, y, s, col, rim):
    g = f'<g transform="translate({x} {y}) scale({s})"><g fill="{col}">'
    g += '<ellipse cx="0" cy="-175" rx="72" ry="40"/><path d="M38 -200 L62 -168 L132 -330 L108 -344Z"/><ellipse cx="128" cy="-344" rx="32" ry="13" transform="rotate(22 128 -344)"/>'
    g += '<path d="M110 -352 l-4 -22 l6 0 l4 20Z"/><path d="M122 -354 l2 -22 l6 1 l-2 21Z"/><path d="M108 -342 l-14 -10 l4 -4Z"/>'
    g += ''.join(f'<path d="M{lx - 7} -160 L{lx + 7} -160 L{lx + sw + 5} 0 L{lx + sw - 5} 0Z"/>' for lx, sw in ((-52, -14), (-30, 10), (40, -8), (58, 14)))
    g += '<path d="M-70 -185 Q-86 -150 -80 -112" stroke="' + col + '" stroke-width="5" fill="none"/></g>'
    g += f'<path d="M60 -168 L132 -330" stroke="{rim}" stroke-width="3" fill="none" opacity=".6"/><path d="M-60 -205 Q0 -222 60 -205" stroke="{rim}" stroke-width="3" fill="none" opacity=".6"/></g>'
    return g


def elephant(x, y, s, col, rim):
    g = f'<g transform="translate({x} {y}) scale({s})"><g fill="{col}">'
    g += '<ellipse cx="0" cy="-115" rx="112" ry="78"/><circle cx="96" cy="-138" r="54"/><ellipse cx="66" cy="-128" rx="38" ry="52"/>'
    g += '<path d="M136 -130 Q170 -80 150 -18 L134 -16 Q148 -80 118 -112Z"/>'
    g += ''.join(f'<rect x="{lx}" y="-70" width="34" height="70" rx="8"/>' for lx in (-86, -44, 40, 76))
    g += '<path d="M-110 -120 Q-124 -90 -118 -60" stroke="' + col + '" stroke-width="5" fill="none"/></g>'
    g += f'<path d="M126 -106 Q150 -100 158 -116" stroke="#fff4dc" stroke-width="7" fill="none" stroke-linecap="round"/>'
    g += f'<path d="M-80 -180 Q0 -205 70 -184" stroke="{rim}" stroke-width="3" fill="none" opacity=".6"/></g>'
    return g


SIL, RIM = '#2a1012', '#ffd88a'
b += giraffe(1020, HZ + 14, 1.15, SIL, RIM) + giraffe(1230, HZ + 8, .95, SIL, RIM) + giraffe(870, HZ + 6, .62, SIL, RIM)
b += elephant(700, HZ + 16, .95, SIL, RIM) + elephant(1390, HZ + 10, .6, SIL, RIM)
b += f'<g fill="{SIL}"><ellipse cx="1330" cy="{HZ + 36}" rx="70" ry="22"/><ellipse cx="1270" cy="{HZ + 26}" rx="34" ry="20"/><circle cx="1258" cy="{HZ + 8}" r="7"/><circle cx="1280" cy="{HZ + 6}" r="7"/></g>'
b += f'<path d="M0 {HZ + 30} C400 {HZ + 10} 500 {HZ + 40} 560 {HZ + 22} C900 {HZ + 90} 1500 {HZ + 80} 1720 {HZ + 26} C1800 {HZ + 20} 1900 {HZ + 30} 1920 {HZ + 28} L1920 1080 L0 1080Z" fill="url(#gr)"/>'
b += '<g fill="#2a4a18">' + ''.join(f'<path d="M{x} 1080 q{random.randint(-14, 14)} -{random.randint(60, 140)} {random.randint(-30, 30)} -{random.randint(120, 230)} q-2 90 {random.randint(14, 26)} {random.randint(120, 230)}Z"/>' for x in range(-20, 1300, 26)) + '</g>'
b += '<g fill="#9ac04a" opacity=".55">' + ''.join(f'<path d="M{x} 1080 q{random.randint(-10, 10)} -{random.randint(40, 90)} {random.randint(-20, 20)} -{random.randint(80, 150)} q-2 60 8 {random.randint(80, 150)}Z"/>' for x in range(0, 1200, 34)) + '</g>'
b += f'<path d="M0 {HZ + 30} C400 {HZ + 10} 500 {HZ + 40} 560 {HZ + 22}" stroke="#d8e070" stroke-width="4" fill="none" opacity=".7"/>'
open('C.html', 'w', encoding='utf-8').write(page('#7a2a3a', svg(d, b), [('THE SAHARA', 130, 'w'), ('WAS', 120, 'w'), ('GREEN', 240, 'y')], '#2a0c10', top=40))
