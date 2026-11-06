# Shorts thumbnails, VERTICAL 1080x1920 (guideline 16-9, 2026-11-06): text centred mid-frame, subject above, frog + props below.
# Run from anywhere: python3 videos/trilobite-extinction/thumb/make_shorts.py [1 2 3 4 5]
# -> videos/trilobite-extinction-shortN/thumb/A.html ; render: SLUG=trilobite-extinction-shortN python3 tools/thumb_shot.py
# Drawing helpers (lens, column, trex, enrolled_side, eurypterid, ghost_trilo...) live in shorts_parts.py (first landscape pass).
import os, sys, math, random
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, '..', '..', '..', 'tools'))
from make import frog, trilo_dorsal, tri_paint, FILTERS, P, poly
from shorts_parts import goggles, bubbles, taper, lens, column, trex, tiny_human, enrolled_side, eurypterid, ghost_trilo
from thumb_lib import vpage, vsvg, lin, rad, spark

VID = os.path.join(HERE, '..', '..')
W, H = 1080, 1920


def dust(rnd, n, x0, x1, y0, y1, col, o0=.15, o1=.6):
    return ''.join(f'<circle cx="{rnd.uniform(x0, x1):.0f}" cy="{rnd.uniform(y0, y1):.0f}" r="{rnd.choice([1.4, 2, 2.8])}" fill="{col}" '
                   f'opacity="{rnd.uniform(o0, o1):.2f}"/>' for _ in range(n))


def text_shade(y0, y1, col, op=.45):
    """soft dark band behind the centred text so it stays readable over busy art"""
    return f'<ellipse cx="540" cy="{(y0 + y1) / 2:.0f}" rx="560" ry="{(y1 - y0) / 2:.0f}" fill="{col}" opacity="{op}" filter="url(#b50)"/>'


# ================= 1: EYES MADE OF ROCK =================
def make_1():
    rnd = random.Random(101)
    FX, FY, R = 540, 480, 336
    k = R / 468; LY = 440
    d = FILTERS
    d += rad('bg1', 540, 760, 1500, [(0, '#2a2046', 1), (.45, '#120e22', 1), (1, '#040308', 1)])
    d += lin('pol1', [(0, '#3a1460'), (.35, '#7a2378'), (.62, '#2a4f8a'), (1, '#0c5a6a')], x2=.6, y2=1)
    d += lin('cut1', [(0, '#5a3418'), (.5, '#3a200e'), (1, '#1c0e06')])
    d += ('<radialGradient id="calc1" cx=".5" cy=".7" r=".75" fx=".42" fy=".45"><stop offset="0" stop-color="#fffbe6"/><stop offset=".35" stop-color="#ffe08a"/>'
          '<stop offset=".75" stop-color="#e09a3a"/><stop offset="1" stop-color="#8a4a14"/></radialGradient>')
    d += ('<radialGradient id="bowl1" cx=".5" cy=".2" r=".9"><stop offset="0" stop-color="#bff8ff"/><stop offset=".45" stop-color="#36b8d0"/>'
          '<stop offset="1" stop-color="#0c4a70"/></radialGradient>')
    d += lin('ring1', [(0, '#e8eef4'), (.3, '#8a96a4'), (.55, '#2a323c'), (1, '#6a7684')], x2=1, y2=1)
    d += ('<filter id="grain1" x="0" y="0" width="100%" height="100%"><feTurbulence type="fractalNoise" baseFrequency=".9" numOctaves="2" seed="4"/>'
          '<feColorMatrix type="matrix" values="0 0 0 0 .9  0 0 0 0 .7  0 0 0 0 .5  0 0 0 .55 -.18"/><feComposite in2="SourceGraphic" operator="in"/></filter>')
    d += f'<clipPath id="field1"><circle cx="{FX}" cy="{FY}" r="{R}"/></clipPath>'
    d += lin('slab1', [(0, '#8a7a6a'), (.5, '#5a4c40'), (1, '#2a221c')], x2=.3, y2=1)
    d += lin('table1', [(0, '#3a2c4a'), (1, '#120c1a')])
    b = f'<rect width="{W}" height="{H}" fill="url(#bg1)"/>'
    b += dust(rnd, 70, 0, W, 0, H, '#d8c8ff', .1, .45)
    # lab light behind the eyepiece
    b += f'<circle cx="{FX}" cy="{FY}" r="{R + 150}" fill="#8a5aff" opacity=".28" filter="url(#b50)"/>'
    b += f'<circle cx="{FX}" cy="{FY}" r="{R + 60}" fill="#5ae0ff" opacity=".14" filter="url(#b24)"/>'
    f = '<g clip-path="url(#field1)">'
    f += f'<rect x="{FX - R}" y="{FY - R}" width="{2 * R}" height="{2 * R}" fill="url(#pol1)"/>'
    for cx, cy, rx, ry, c, op in ((1050, 260, 260, 120, '#ff5fb0', .35), (1580, 330, 240, 140, '#5fe0ff', .3), (1300, 140, 300, 90, '#ffd36a', .22),
                                  (1150, 880, 360, 160, '#3a1a6a', .5), (1560, 860, 260, 160, '#0a3a4a', .5)):
        f += f'<ellipse cx="{FX + (cx - 1310) * k:.0f}" cy="{FY + (cy - 548) * k:.0f}" rx="{rx * k:.0f}" ry="{ry * k:.0f}" fill="{c}" opacity="{op}" filter="url(#b50)"/>'
    # the cut cuticle band with the lenses set in it
    xs = range(FX - R - 20, FX + R + 21, 14)
    top = [(x, LY - 60 + ((x - FX) / 330) ** 2 * 90) for x in xs]
    bot = [(x, LY + 130 + ((x - FX) / 330) ** 2 * 90) for x in reversed(xs)]
    f += f'<path d="{poly(top + bot)}" fill="url(#cut1)"/><path d="{poly(top + bot)}" fill="#fff" filter="url(#grain1)" opacity=".5"/>'
    f += f'<polyline points="{P(top)}" fill="none" stroke="#ffcf8a" stroke-width="5" opacity=".7"/>'
    for j in range(5):
        y = LY + 165 + j * 30
        f += f'<path d="M{FX - R} {y} Q{FX} {y + 50} {FX + R} {y}" fill="none" stroke="#c89aff" stroke-width="2" opacity=".2"/>'
    f += lens(FX - 300, LY + 36, 220, -18, bright=.55, idn='a') + lens(FX + 300, LY + 36, 220, 18, bright=.55, idn='b')
    f += lens(FX, LY, 310, 0, bright=1.0, idn='c')
    for j in range(-6, 7):
        f += f'<path d="M{FX + j * 36} {FY + R - 64} l0 {14 if j % 3 else 26}" stroke="#e8f8ff" stroke-width="2" opacity=".4"/>'
    f += f'<circle cx="{FX}" cy="{FY}" r="{R}" fill="none" stroke="#000" stroke-width="70" opacity=".45" filter="url(#b24)"/></g>'
    b += f
    b += f'<circle cx="{FX}" cy="{FY}" r="{R + 22}" fill="none" stroke="#06050a" stroke-width="40"/>'
    b += f'<circle cx="{FX}" cy="{FY}" r="{R + 14}" fill="none" stroke="url(#ring1)" stroke-width="18"/>'
    b += f'<path d="M{FX - R * .7:.0f} {FY - R * .74:.0f} A{R + 14} {R + 14} 0 0 1 {FX + R * .25:.0f} {FY - R - 12:.0f}" fill="none" stroke="#fff" stroke-width="5" opacity=".7"/>'
    b += spark(FX - 140, 330, 24) + spark(FX + 250, 250, 20, '#e8fbff') + spark(160, 230, 16) + spark(930, 760, 14, '#ffe8f8')
    # ---- below the text: lab table, fossil slab with a trilobite (its eye glowing), the frog in goggles with the thin-section slide ----
    b += f'<path d="M0 1560 Q540 1530 1080 1560 L1080 {H} L0 {H}Z" fill="url(#table1)"/>'
    b += '<path d="M0 1560 Q540 1530 1080 1560" fill="none" stroke="#a88aff" stroke-width="4" opacity=".45"/>'
    b += '<ellipse cx="300" cy="1690" rx="250" ry="40" fill="#000" opacity=".5" filter="url(#b12)"/>'
    slab = [(70, 1640), (120, 1520), (260, 1470), (440, 1490), (530, 1560), (510, 1680), (380, 1720), (160, 1710)]
    b += f'<path d="{poly(slab)}" fill="url(#slab1)" stroke="#1a1410" stroke-width="6" stroke-linejoin="round"/>'
    b += f'<path d="M120 1520 L260 1470 L440 1490" fill="none" stroke="#e8dcc8" stroke-width="5" opacity=".55"/>'
    u = 250; Rt = trilo_dorsal(u, N=11)
    stone = {'ceph': '#a89078', 'pyg': '#94806a', 'pleura': '#9a8670', 'axial': '#b8a088', 'glab': '#c4ac92'}
    b += (f'<g transform="translate(300 1592) rotate(-72) scale(1 .78)"><ellipse rx="{u * .45:.0f}" ry="{u * .55:.0f}" fill="#2a2018" opacity=".35" filter="url(#b6)"/>'
          + tri_paint(Rt, stone, '#3a2c20', 3.5, eyecol='#5a4630', lensfill='#ffd890', glint='#fffbe8') + '</g>')
    # glow on the fossil eye (the one in the slide)
    b += '<circle cx="232" cy="1520" r="46" fill="#ffd36a" opacity=".55" filter="url(#b12)"/>' + spark(214, 1494, 18)
    slide = ('<g transform="translate(66 -74) rotate(-24) scale(.62)"><rect x="-44" y="-16" width="88" height="32" rx="3" fill="#dff4ff" fill-opacity=".45" stroke-width="3"/>'
             '<ellipse cx="0" cy="0" rx="16" ry="10" fill="#8a5a2a" stroke="none"/><circle cx="-4" cy="-2" r="3" fill="#ffd36a" stroke="none"/><circle cx="5" cy="1" r="3" fill="#ffd36a" stroke="none"/>'
             '<path d="M-38 -10 L-20 -10" stroke="#fff" stroke-width="3" opacity=".9"/></g>')
    b += '<ellipse cx="770" cy="1600" rx="220" ry="220" fill="#a88aff" opacity=".2" filter="url(#b50)"/>'
    b += frog(760, 1760, 3.25, look=(-9, -9), mouth='O', shadow=True, mid=goggles(), armR='M38 -22 q22 -10 30 -44', armL='M-34 -22 q-18 4 -22 24', front=slide)
    lines = [('EYES', 178, 'w'), ('MADE OF', 120, 'w'), ('ROCK', 236, 'y')]
    return vpage('#120e22', vsvg(d, b), lines, outline='#0a0614', top=862)


# ================= 2: LONGER THAN DINOSAURS =================
def make_2():
    rnd = random.Random(202)
    BASE = 830
    T1 = 340; D1 = BASE - (BASE - T1) * 165 / 270
    d = FILTERS
    d += lin('sky2', [(0, '#3a86d0'), (.5, '#8cc8ee'), (.85, '#f8dcae'), (1, '#ffd9a0')])
    d += rad('sun2', 1000, 170, 800, [(0, '#fffbe8', 1), (.08, '#fff2c0', .9), (.3, '#ffd88a', .35), (1, '#ffd88a', 0)])
    d += lin('grass2', [(0, '#8cba5a'), (1, '#4a7a34')])
    d += lin('cliff2', [(0, '#7a5a3e'), (.3, '#4e3828'), (1, '#1e1610')])
    d += rad('gold2', 300, 270, 300, [(0, '#fff3b0', .9), (.4, '#ffd36a', .4), (1, '#ffd36a', 0)])
    b = f'<rect width="{W}" height="{BASE + 40}" fill="url(#sky2)"/><rect width="{W}" height="{BASE + 40}" fill="url(#sun2)"/>'
    for j in range(9):
        a = math.radians(115 + j * 10)
        b += f'<path d="M1000 170 L{1000 + math.cos(a - .03) * 1300:.0f} {170 + math.sin(a - .03) * 1300:.0f} L{1000 + math.cos(a + .03) * 1300:.0f} {170 + math.sin(a + .03) * 1300:.0f}Z" fill="#fff6d8" opacity=".09"/>'
    for cx, cy, w in ((180, 600, 200), (760, 450, 170), (980, 640, 160), (560, 240, 130)):
        b += (f'<g opacity=".8" filter="url(#b3)"><ellipse cx="{cx}" cy="{cy}" rx="{w}" ry="{w * .18:.0f}" fill="#fff"/><ellipse cx="{cx - w * .3:.0f}" cy="{cy - w * .1:.0f}" rx="{w * .4:.0f}" ry="{w * .18:.0f}" fill="#fff"/>'
              f'<ellipse cx="{cx + w * .25:.0f}" cy="{cy - w * .12:.0f}" rx="{w * .3:.0f}" ry="{w * .16:.0f}" fill="#fff"/></g>')
    b += f'<path d="M0 {BASE - 40} Q260 {BASE - 100} 540 {BASE - 50} Q800 {BASE - 110} 1080 {BASE - 50} L1080 {BASE + 40} L0 {BASE + 40}Z" fill="#7aa0b8" opacity=".55"/>'
    # ground: a grass lip and a cliff cross-section below (rock layers going down in time)
    b += f'<path d="M0 {BASE} Q540 {BASE - 20} 1080 {BASE + 4} L1080 {H} L0 {H}Z" fill="url(#cliff2)"/>'
    bands = ['#8a6a4a', '#a8784a', '#6a5240', '#94704e', '#5a4434', '#7a5a42', '#4a382a', '#6a4e38', '#3a2c20', '#54402e']
    y = BASE + 70
    for j, c in enumerate(bands):
        h = 90 + (j % 3) * 18
        b += f'<path d="M0 {y} Q300 {y - 14 + j % 2 * 10} 600 {y + 4} T1080 {y - 6} L1080 {y + h} Q700 {y + h + 12} 300 {y + h - 6} T0 {y + h}Z" fill="{c}" opacity=".55"/>'
        for _ in range(10):
            b += f'<ellipse cx="{rnd.uniform(0, W):.0f}" cy="{rnd.uniform(y + 8, y + h - 8):.0f}" rx="{rnd.uniform(4, 12):.0f}" ry="{rnd.uniform(2, 5):.0f}" fill="#000" opacity=".18"/>'
        y += h
    b += f'<path d="M0 {BASE} Q540 {BASE - 20} 1080 {BASE + 4} L1080 {BASE + 46} Q540 {BASE + 30} 0 {BASE + 52}Z" fill="url(#grass2)"/>'
    for _ in range(80):
        x = rnd.uniform(0, W); yy = BASE + rnd.uniform(-4, 40)
        b += f'<path d="M{x:.0f} {yy:.0f} l-3 -12 M{x:.0f} {yy:.0f} l4 -10" stroke="#2e4a22" stroke-width="2.5" opacity="{rnd.uniform(.3, .7):.2f}"/>'
    # fossils in the lower layers: dinosaur bone up high, trilobites deep down
    b += ('<g transform="translate(300 1480) rotate(-14)" opacity=".85"><path d="M-90 -8 L90 -8 L90 8 L-90 8Z" fill="#e8dcc0" stroke="#2a1e14" stroke-width="4"/>'
          '<circle cx="-92" cy="-12" r="16" fill="#e8dcc0" stroke="#2a1e14" stroke-width="4"/><circle cx="-92" cy="12" r="16" fill="#e8dcc0" stroke="#2a1e14" stroke-width="4"/>'
          '<circle cx="92" cy="-12" r="16" fill="#e8dcc0" stroke="#2a1e14" stroke-width="4"/><circle cx="92" cy="12" r="16" fill="#e8dcc0" stroke="#2a1e14" stroke-width="4"/>'
          '<path d="M-80 -8 L80 -8" stroke="#fff" stroke-width="3" opacity=".7"/></g>')
    stone = {'ceph': '#c0a27a', 'pyg': '#a88a66', 'pleura': '#b0926c', 'axial': '#d0b28a', 'glab': '#dcbe96'}
    for x, yy, u, rot in ((200, 1700, 170, -24), (380, 1760, 110, 30)):
        b += f'<g transform="translate({x} {yy}) rotate({rot}) scale(1 .8)">' + tri_paint(trilo_dorsal(u, N=10), stone, '#3a2a1a', 3, eyecol='#5a4630', lensfill='#e8c890') + '</g>'
    # the three time pillars
    paleo = ['#7a5a8a', '#9a6a4a', '#b8864e', '#7a8a5a', '#a87048', '#c49a5a', '#8a6a4a', '#b07850', '#9a7a5a', '#c08a5a']
    meso = ['#b06a4a', '#c88a5a', '#9a7a62', '#d0a070', '#a86a50', '#c49064']
    b += '<ellipse cx="300" cy="300" rx="240" ry="190" fill="url(#gold2)"/>'
    b += column(150, 450, T1, BASE, paleo, rnd)
    b += column(590, 810, D1, BASE, meso, rnd)
    b += f'<ellipse cx="940" cy="{BASE + 2}" rx="34" ry="6" fill="#e8d4a8" stroke="#2a1e14" stroke-width="2.5"/>'
    b += tiny_human(940, BASE, 1.2)
    b += f'<ellipse cx="700" cy="{D1 + 4:.0f}" rx="120" ry="14" fill="#3a2a1a" opacity=".35" filter="url(#b3)"/>'
    b += trex(676, D1 - 2 - 1.36 * 88, 88)
    u = 250; R = trilo_dorsal(u)
    col = {'ceph': '#c47a3a', 'pyg': '#a8642e', 'pleura': '#b06a32', 'axial': '#d48a48', 'glab': '#e09a58'}
    b += f'<ellipse cx="300" cy="{T1 + 4}" rx="130" ry="20" fill="#3a2a1a" opacity=".4" filter="url(#b3)"/>'
    b += f'<g transform="translate(300 {T1 - 52}) scale(1 .62)">' + tri_paint(R, col, '#2a1408', 4, eyecol='#3a2410', lensfill='#e8b860', glint='#fff6d8') + '</g>'
    b += f'<g transform="translate(300 {T1 - 52}) scale(1 .62)"><path d="{R["ceph"][0]}" fill="none" stroke="#fff2c0" stroke-width="5" opacity=".55" transform="translate(-3 -4)"/></g>'
    cy_ = T1 - 52 - .53 * u * .62
    b += (f'<g transform="translate(300 {cy_ - 4:.0f}) scale(.82)" stroke="#5a3a08" stroke-width="4" stroke-linejoin="round"><path d="M-60 0 L-66 -60 L-34 -30 L0 -74 L34 -30 L66 -60 L60 0Z" fill="#ffd34a"/>'
          f'<path d="M-60 0 L60 0 L60 -12 L-60 -12Z" fill="#e8a820"/><circle cx="0" cy="-34" r="9" fill="#e0405a"/><circle cx="-36" cy="-18" r="6" fill="#4ac0e8"/><circle cx="36" cy="-18" r="6" fill="#4ac0e8"/>'
          f'<path d="M-48 -8 L-52 -46" stroke="#fff8c8" stroke-width="4" opacity=".8"/></g>')
    b += spark(470, 170, 26) + spark(130, 250, 18) + spark(440, 330, 14) + spark(860, 380, 16, '#fff')
    b += text_shade(870, 1340, '#140c06', .5)
    # frog with a tape measure, pulled out along a layer
    b += '<path d="M440 1660 L640 1640" stroke="#2a1e14" stroke-width="22" stroke-linecap="round"/><path d="M440 1660 L640 1640" stroke="#ffd34a" stroke-width="15"/>'
    for xx in range(450, 640, 20):
        b += f'<path d="M{xx} {1660 - (xx - 440) * .1:.0f} l0 {-9 if (xx // 20) % 5 else -14}" stroke="#2a1e14" stroke-width="2.5"/>'
    tape = ('<g transform="translate(-58 -42) scale(.8)"><circle r="24" fill="#e8b020" stroke-width="3.5"/><circle r="9" fill="#5a4030" stroke-width="3"/>'
            '<path d="M-10 -18 q8 -6 18 -2" stroke="#fff" stroke-width="3" fill="none" opacity=".8"/></g>')
    b += '<ellipse cx="800" cy="1640" rx="200" ry="180" fill="#ffd88a" opacity=".16" filter="url(#b50)"/>'
    b += frog(800, 1770, 3.25, look=(-6, -10), mouth='O', shadow=True, armR='M38 -22 q22 -6 26 -40', armL='M-34 -22 q-20 0 -26 -14', front=tape)
    lines = [('LONGER', 196, 'y'), ('THAN', 122, 'w'), ('DINOSAURS', 146, 'w')]
    return vpage('#8cc8ee', vsvg(d, b), lines, outline='#14223a', top=884)


# ================= 3: A BALL OF ARMOR =================
def make_3():
    rnd = random.Random(303)
    CX, CY, r = 290, 500, 186
    FXo, FYo = -760, 40
    d = FILTERS
    d += lin('sea3', [(0, '#7fe6e0'), (.18, '#2aa8b0'), (.55, '#0f5a70'), (1, '#062838')])
    d += lin('sand3', [(0, '#5a8a80'), (.3, '#3a6460'), (1, '#122a2c')])
    d += lin('seg3', [(0, '#c47840'), (1, '#7a3e1c')], x2=1, y2=1)
    d += lin('head3', [(0, '#d08a50'), (1, '#7a4020')], x2=.4, y2=1)
    d += lin('glab3', [(0, '#e8a86a'), (1, '#9a5a2a')])
    d += '<radialGradient id="lens3" cx=".4" cy=".35" r=".7"><stop offset="0" stop-color="#fffbe0"/><stop offset=".5" stop-color="#ffc860"/><stop offset="1" stop-color="#6a3a10"/></radialGradient>'
    d += rad('shade3', CX - 84, CY - 100, 310, [(0, '#fff', .18), (.45, '#000', 0), (1, '#000', .55)])
    d += lin('armor3', [(0, '#7a9aa8'), (.35, '#4a6270'), (1, '#1c2830')], x2=.2, y2=1)
    d += lin('jaw3', [(0, '#5a7480'), (1, '#16222a')], x2=.1, y2=1)
    d += rad('mouth3', 1420, 470, 260, [(0, '#3a0a10', 1), (1, '#0a0204', 1)])
    d += rad('vig3', 540, 900, 1250, [(0, '#000', 0), (.6, '#000', 0), (1, '#021018', .55)])
    b = f'<rect width="{W}" height="{H}" fill="url(#sea3)"/>'
    for x0, w, op in ((40, 90, .18), (300, 140, .2), (560, 100, .16), (860, 150, .12)):
        b += f'<path d="M{x0} -20 L{x0 + w} -20 L{x0 + w + 260} 1500 L{x0 + 140} 1500Z" fill="#e8fff8" opacity="{op}" filter="url(#b12)"/>'
    for _ in range(26):
        x, y = rnd.uniform(0, W), rnd.uniform(0, 150)
        b += f'<path d="M{x:.0f} {y:.0f} q30 -12 60 0 q30 12 60 0" fill="none" stroke="#e8fffc" stroke-width="3" opacity="{rnd.uniform(.12, .35):.2f}"/>'
    # seafloor below the text
    b += '<path d="M0 1400 Q300 1370 600 1410 Q850 1430 1080 1400 L1080 1920 L0 1920Z" fill="#1f5a62" opacity=".7"/>'
    for x, hh in ((70, 150), (170, 100), (930, 120), (1030, 170)):
        b += f'<path d="M{x} 1420 l0 {-hh} m0 {hh * .4} l{-hh * .3} {-hh * .4} m{hh * .3} {hh * .55} l{hh * .3} {-hh * .35}" stroke="#2e7a7a" stroke-width="10" stroke-linecap="round" fill="none" opacity=".8"/>'
    b += '<path d="M0 1500 Q400 1470 700 1496 Q900 1510 1080 1490 L1080 1920 L0 1920Z" fill="url(#sand3)"/>'
    for _ in range(22):
        x, y = rnd.uniform(0, W), rnd.uniform(1520, 1880)
        b += f'<path d="M{x:.0f} {y:.0f} q20 -8 40 0 q20 8 40 0" fill="none" stroke="#bff8ee" stroke-width="2.5" opacity="{rnd.uniform(.12, .3):.2f}"/>'
    # ---- armoured jawed fish (placoderm) from the right, jaws open at the ball ----
    fish = f'<g transform="translate({FXo} {FYo})">'
    fish += '<path d="M1600 420 C1760 400 1900 420 1960 440 L1960 700 C1840 690 1720 640 1620 560Z" fill="#2a3c46"/>'
    fish += '<path d="M1300 352 C1400 372 1520 392 1640 424 L1640 452 C1520 500 1420 566 1312 602 Z" fill="url(#mouth3)"/>'
    fish += '<path d="M1330 372 C1420 400 1500 420 1600 436 M1340 584 C1420 540 1500 500 1600 462" fill="none" stroke="#7a2030" stroke-width="10" opacity=".5"/>'
    fish += ('<path d="M1300 352 C1296 300 1330 220 1420 168 C1520 118 1700 104 1960 120 L1960 440 C1860 420 1760 410 1640 424 C1520 392 1400 370 1300 352Z" '
             'fill="url(#armor3)" stroke="#0a1418" stroke-width="7" stroke-linejoin="round"/>')
    fish += ('<path d="M1430 170 C1470 240 1520 300 1600 330 M1600 330 C1680 300 1760 250 1820 112 M1600 330 C1640 370 1660 400 1660 424 '
             'M1720 112 C1700 180 1660 240 1600 330" fill="none" stroke="#0a1418" stroke-width="5" opacity=".75"/>')
    for _ in range(40):
        x, y = rnd.uniform(1360, 1900), rnd.uniform(140, 400)
        if y < 352 + (x - 1300) * .2 - 10:
            fish += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{rnd.uniform(3, 6):.1f}" fill="#9ab8c4" opacity=".35"/>'
    fish += '<path d="M1310 330 C1320 260 1360 210 1430 172 C1520 130 1640 116 1780 112" fill="none" stroke="#c8f4ff" stroke-width="7" opacity=".7"/>'
    fish += '<path d="M1296 340 L1286 420 L1340 362Z" fill="#e8eef0" stroke="#0a1418" stroke-width="5" stroke-linejoin="round"/>'
    fish += '<path d="M1360 368 L1356 418 L1396 378Z" fill="#d8e0e4" stroke="#0a1418" stroke-width="4" stroke-linejoin="round"/>'
    fish += '<circle cx="1490" cy="236" r="44" fill="#1a262c" stroke="#0a1418" stroke-width="6"/><circle cx="1490" cy="236" r="30" fill="#e8c040"/>'
    fish += '<circle cx="1482" cy="238" r="16" fill="#0a0a0a"/><circle cx="1474" cy="228" r="6" fill="#fff"/>'
    fish += '<path d="M1440 196 Q1490 176 1540 206" fill="none" stroke="#0a1418" stroke-width="9"/>'
    fish += ('<path d="M1312 602 C1420 566 1520 500 1640 452 C1760 450 1880 470 1960 480 L1960 720 C1820 700 1700 680 1580 660 C1460 650 1360 650 1300 632 Z" '
             'fill="url(#jaw3)" stroke="#0a1418" stroke-width="7" stroke-linejoin="round"/>')
    fish += '<path d="M1320 612 L1306 540 L1366 592Z" fill="#e8eef0" stroke="#0a1418" stroke-width="5" stroke-linejoin="round"/>'
    fish += '<path d="M1400 570 L1398 524 L1436 556Z" fill="#d8e0e4" stroke="#0a1418" stroke-width="4" stroke-linejoin="round"/>'
    fish += '<path d="M1330 640 C1480 660 1640 680 1900 700" fill="none" stroke="#0a1418" stroke-width="4" opacity=".6"/>'
    fish += '<path d="M1330 606 C1440 574 1540 520 1640 470" fill="none" stroke="#b8e8f4" stroke-width="5" opacity=".45"/>'
    b += fish + '</g>'
    # the enrolled trilobite, glowing
    b += f'<circle cx="{CX}" cy="{CY}" r="{r + 90}" fill="#e8fff4" opacity=".38" filter="url(#b50)"/>'
    b += enrolled_side(CX, CY, r, rnd)
    b += spark(CX - r - 10, CY - r + 30, 26) + spark(CX + r - 20, CY - r - 20, 20, '#e8fffc') + spark(CX - 40, CY + r + 34, 14)
    b += bubbles(rnd, 22, 40, 1040, 140, 800, skip=lambda x, y: (x - CX) ** 2 + (y - CY) ** 2 < (r + 40) ** 2 or (x > 520 and y > 150))
    # sea scorpion creeping in on the floor (head to the left, toward the frog)
    b += '<ellipse cx="760" cy="1650" rx="210" ry="26" fill="#04181c" opacity=".45" filter="url(#b6)"/>'
    b += eurypterid(660, 1620, 104, rot=186)
    # frog in a diving helmet holding a curled pill bug
    pill = ('<g transform="translate(72 -64)"><circle r="17" fill="#6a6e78" stroke-width="3"/>'
            + ''.join(f'<path d="M{-15 + j * 6} -8 Q{-14 + j * 6} 0 {-15 + j * 6} 8" fill="none" stroke-width="2"/>' for j in range(1, 5))
            + '<path d="M-8 -10 q8 -6 16 -2" stroke="#fff" stroke-width="2.5" fill="none" opacity=".8"/></g>')
    b += '<ellipse cx="250" cy="1640" rx="200" ry="180" fill="#bff8ee" opacity=".16" filter="url(#b50)"/>'
    b += frog(230, 1770, 3.25, look=(10, -6), mouth='O', helmet=True, shadow=True, armR='M38 -22 q24 -6 30 -40', armL='M-34 -22 q-18 6 -22 24', front=pill)
    b += bubbles(rnd, 5, 250, 320, 1350, 1500)
    b += f'<rect width="{W}" height="{H}" fill="url(#vig3)"/>'
    lines = [('A BALL', 182, 'w'), ('OF', 116, 'w'), ('ARMOR', 214, 'y')]
    return vpage('#2aa8b0', vsvg(d, b), lines, outline='#062030', top=850)


# ================= 4: OCEAN TOO ACIDIC =================
def make_4():
    rnd = random.Random(404)
    X0, X1, TOP, BOT, SURF = 260, 820, 190, 790, 300
    HZ = 650
    u = 330; sc = u / 400
    d = FILTERS
    d += lin('sky4', [(0, '#12080a'), (.18, '#3a1210'), (.3, '#8a2a14'), (.34, '#d8541c'), (.45, '#2a0e08'), (1, '#0a0606')])
    d += rad('lavaglow4', 540, HZ, 700, [(0, '#ff8a2a', .7), (.35, '#e2481c', .3), (1, '#8a2a14', 0)])
    d += lin('acid4', [(0, '#e8ff6a'), (.35, '#a8e83a'), (1, '#3a8a2a')])
    d += lin('basalt4', [(0, '#2a1c1a'), (1, '#0a0606')])
    d += ('<mask id="erode4"><rect x="-400" y="-400" width="800" height="800" fill="#fff"/>'
          + ''.join(f'<circle cx="{rnd.uniform(-190, 190) * sc:.0f}" cy="{rnd.uniform(-190, 190) * sc:.0f}" r="{rnd.uniform(5, 16) * sc:.0f}" fill="#000"/>' for _ in range(34))
          + ''.join(f'<circle cx="{(170 + rnd.uniform(-30, 40)) * sc:.0f}" cy="{rnd.uniform(-60, 200) * sc:.0f}" r="{rnd.uniform(18, 36) * sc:.0f}" fill="#000"/>' for _ in range(9))
          + ''.join(f'<circle cx="{rnd.uniform(-60, 160) * sc:.0f}" cy="{(180 + rnd.uniform(-10, 40)) * sc:.0f}" r="{rnd.uniform(16, 30) * sc:.0f}" fill="#000"/>' for _ in range(7))
          + '</mask>')
    d += f'<clipPath id="liq4"><path d="M{X0 + 6} {SURF} L{X1 - 6} {SURF} L{X1 - 6} {BOT - 60} Q{X1 - 6} {BOT - 6} {X1 - 60} {BOT - 6} L{X0 + 60} {BOT - 6} Q{X0 + 6} {BOT - 6} {X0 + 6} {BOT - 60}Z"/></clipPath>'
    d += lin('card4', [(0, '#f4efe0'), (1, '#cfc6b0')])
    b = f'<rect width="{W}" height="{H}" fill="url(#sky4)"/>'
    for _ in range(14):
        b += f'<ellipse cx="{rnd.uniform(0, W):.0f}" cy="{rnd.uniform(60, 560):.0f}" rx="{rnd.uniform(140, 300):.0f}" ry="{rnd.uniform(50, 100):.0f}" fill="{rnd.choice(["#2a1412", "#4a1c14", "#1a0c0c"])}" opacity=".6" filter="url(#b24)"/>'
    # Siberian fissure eruptions on the horizon, both sides of the beaker
    for x, h, w in ((60, 170, 34), (190, 120, 26), (900, 230, 44), (1040, 150, 30), (520, 110, 24)):
        b += f'<path d="M{x - 90} {HZ} Q{x} {HZ - h * 2.6} {x + 120} {HZ - h * 3.4}" fill="none" stroke="#3a1a14" stroke-width="{w * 3}" opacity=".55" filter="url(#b24)"/>'
        b += f'<path d="M{x - w} {HZ} Q{x - w * .3} {HZ - h} {x} {HZ - h * 1.05} Q{x + w * .3} {HZ - h} {x + w} {HZ}Z" fill="#ffb03a" opacity=".9" filter="url(#b3)"/>'
        b += f'<path d="M{x - w * .4} {HZ} Q{x} {HZ - h * .8} {x + w * .4} {HZ}Z" fill="#fff2a0"/>'
        for _ in range(8):
            b += f'<circle cx="{x + rnd.uniform(-w * 2, w * 2):.0f}" cy="{HZ - rnd.uniform(h * .3, h * 1.2):.0f}" r="{rnd.uniform(2, 5):.1f}" fill="#ffd36a"/>'
    b += f'<rect width="{W}" height="{H}" fill="url(#lavaglow4)"/>'
    b += f'<path d="M0 {HZ} L{W} {HZ} L{W} {H} L0 {H}Z" fill="url(#basalt4)"/>'
    b += f'<path d="M0 {HZ} L{W} {HZ}" stroke="#ff9a3a" stroke-width="5" opacity=".8" filter="url(#b3)"/>'
    for j in range(12):
        y = HZ + 30 + j * 46 * (1 + j * .08); x0 = rnd.uniform(-100, 100)
        pts = [(x0 + i * 110 + rnd.uniform(-30, 30), y + rnd.uniform(-14, 14) + i * 2) for i in range(12)]
        b += f'<polyline points="{P(pts)}" fill="none" stroke="#ff7a2a" stroke-width="{2 + j * .5:.1f}" opacity="{.22 + j * .03:.2f}"/>'
        b += f'<polyline points="{P(pts)}" fill="none" stroke="#ffb03a" stroke-width="{8 + j * 1.5:.0f}" opacity=".08" filter="url(#b6)"/>'
    # ---- the beaker of acid sea ----
    b += f'<ellipse cx="{(X0 + X1) / 2}" cy="{BOT + 10}" rx="330" ry="28" fill="#000" opacity=".6" filter="url(#b12)"/>'
    b += f'<ellipse cx="{(X0 + X1) / 2}" cy="{(SURF + BOT) / 2}" rx="420" ry="440" fill="#b8ff4a" opacity=".22" filter="url(#b50)"/>'
    lq = '<g clip-path="url(#liq4)">'
    lq += f'<rect x="{X0}" y="{SURF}" width="{X1 - X0}" height="{BOT - SURF}" fill="url(#acid4)" opacity=".9"/>'
    lq += f'<rect x="{X0}" y="{BOT - 220}" width="{X1 - X0}" height="220" fill="#ff6a2a" opacity=".22" filter="url(#b24)"/>'
    R = trilo_dorsal(u)
    col = {'ceph': '#d89a5a', 'pyg': '#c4844a', 'pleura': '#cc8c50', 'axial': '#e8b070', 'glab': '#f0c080'}
    TX, TY = 540, 570
    lq += f'<g transform="translate({TX} {TY}) rotate(-18)"><ellipse cx="0" cy="0" rx="{u * .55:.0f}" ry="{u * .6:.0f}" fill="#f8ffe0" opacity=".35" filter="url(#b24)"/>'
    lq += '<g mask="url(#erode4)">' + tri_paint(R, col, '#3a2210', 4, eyecol='#3a2410', lensfill='#e8c080', glint='#fffbe8') + '</g>'
    for _ in range(70):
        a = rnd.uniform(0, 2 * math.pi); rr = rnd.uniform(.38, .55)
        lq += f'<circle cx="{math.cos(a) * u * rr * .95:.0f}" cy="{math.sin(a) * u * rr:.0f}" r="{rnd.uniform(2.5, 7.5):.1f}" fill="#fff" fill-opacity=".25" stroke="#fff" stroke-width="1.8" opacity=".85"/>'
    lq += '</g>'
    for _ in range(12):
        sx = TX + rnd.uniform(-150, 150); sy = TY + rnd.uniform(-140, 100); y = sy
        while y > SURF + 10:
            y -= rnd.uniform(22, 46); s_ = rnd.uniform(3, 8) * (1 + (sy - y) / 900)
            lq += f'<circle cx="{sx + math.sin(y / 30) * 6:.0f}" cy="{y:.0f}" r="{s_:.1f}" fill="#fff" fill-opacity=".18" stroke="#fffde8" stroke-width="2" opacity=".75"/>'
    b += lq + '</g>'
    for _ in range(60):
        b += f'<circle cx="{rnd.uniform(X0 + 14, X1 - 14):.0f}" cy="{SURF + rnd.uniform(-14, 8):.0f}" r="{rnd.uniform(6, 18):.1f}" fill="#f6ffd0" fill-opacity=".7" stroke="#8ac03a" stroke-width="2"/>'
    for _ in range(14):
        b += f'<circle cx="{rnd.uniform(X0 + 20, X1 - 20):.0f}" cy="{SURF - rnd.uniform(20, 90):.0f}" r="{rnd.uniform(2, 6):.1f}" fill="#f6ffd0" opacity=".8"/>'
    gp = f'M{X0} {TOP} L{X0} {BOT - 60} Q{X0} {BOT} {X0 + 60} {BOT} L{X1 - 60} {BOT} Q{X1} {BOT} {X1} {BOT - 60} L{X1} {TOP}'
    b += f'<path d="{gp}" fill="#fff" fill-opacity=".06" stroke="#0e0a08" stroke-width="16"/><path d="{gp}" fill="none" stroke="#f0fff4" stroke-width="7" opacity=".8"/>'
    b += f'<path d="M{X0 - 30} {TOP - 18} Q{X0 - 10} {TOP} {X0} {TOP + 20} M{X0 - 30} {TOP - 18} L{X1 + 10} {TOP - 18} Q{X1 + 16} {TOP} {X1} {TOP + 6}" fill="none" stroke="#f0fff4" stroke-width="9" stroke-linecap="round" opacity=".85"/>'
    b += f'<path d="M{X0 + 34} {TOP + 40} L{X0 + 34} {BOT - 80}" stroke="#fff" stroke-width="15" opacity=".35" stroke-linecap="round"/>'
    b += f'<path d="M{X0 + 64} {TOP + 60} L{X0 + 64} {TOP + 260}" stroke="#fff" stroke-width="6" opacity=".4" stroke-linecap="round"/>'
    b += f'<path d="M{X1 - 32} {TOP + 80} L{X1 - 32} {BOT - 110}" stroke="#ffd0a0" stroke-width="8" opacity=".35" stroke-linecap="round"/>'
    for j in range(6):
        y = SURF + 60 + j * 76
        b += f'<path d="M{X1 - 110} {y} L{X1 - 54} {y}" stroke="#fff" stroke-width="5" opacity=".6"/><path d="M{X1 - 82} {y + 38} L{X1 - 54} {y + 38}" stroke="#fff" stroke-width="3" opacity=".5"/>'
    b += spark(X0 + 30, TOP + 10, 24) + spark(X1 - 20, TOP + 110, 18) + spark(430, 470, 16, '#fffbe8')
    b += text_shade(860, 1340, '#0a0404', .45)
    # ---- below: pH colour card propped on a rock, frog in goggles holding a strip that turned red ----
    b += '<ellipse cx="300" cy="1740" rx="230" ry="34" fill="#000" opacity=".55" filter="url(#b12)"/>'
    b += '<path d="M80 1740 Q90 1650 180 1630 Q320 1600 470 1640 Q530 1680 520 1740Z" fill="#2a1e1c" stroke="#0a0606" stroke-width="5"/>'
    b += '<path d="M110 1660 Q200 1630 320 1626" fill="none" stroke="#ff9a5a" stroke-width="4" opacity=".55"/>'
    sw = ['#e0303a', '#f06a2a', '#f4b02a', '#e8e040', '#9ad040', '#40b060', '#2a9a9a', '#3a6ad0', '#5a3ab0']
    b += '<g transform="translate(300 1520) rotate(-8)"><rect x="-200" y="-90" width="400" height="180" rx="14" fill="url(#card4)" stroke="#1a1010" stroke-width="6"/>'
    for j, c in enumerate(sw):
        b += f'<rect x="{-176 + j * 39}" y="-58" width="34" height="116" rx="5" fill="{c}" stroke="#1a1010" stroke-width="2.5"/>'
    b += '<path d="M-176 -66 L-142 -66" stroke="#fff" stroke-width="0"/><path d="M-190 -78 L190 -78" stroke="#fff" stroke-width="4" opacity=".7"/>'
    b += '<path d="M-182 -70 L-130 -70 L-130 70 L-182 70Z" fill="none" stroke="#fff6a0" stroke-width="6"/></g>'
    b += spark(130, 1430, 18, '#ffe0c0')
    strip = ('<g transform="translate(66 -76) rotate(-18)"><rect x="-7" y="-58" width="14" height="70" rx="2" fill="#f4f0e0" stroke-width="3"/>'
             '<rect x="-7" y="-58" width="14" height="24" rx="2" fill="#e0303a" stroke-width="3"/></g>')
    b += '<ellipse cx="800" cy="1620" rx="210" ry="190" fill="#ff8a3a" opacity=".2" filter="url(#b50)"/>'
    b += frog(790, 1770, 3.25, look=(-10, -8), mouth='O', shadow=True, mid=goggles('#2a3a2a', '#d8ffb0'), armR='M38 -22 q22 -10 26 -42', armL='M-34 -22 q-18 4 -22 24', front=strip)
    lines = [('OCEAN', 186, 'w'), ('TOO', 128, 'w'), ('ACIDIC', 220, 'y')]
    return vpage('#3a1210', vsvg(d, b), lines, outline='#140606', top=866)


# ================= 5: ONLY ONE SURVIVED =================
def make_5():
    rnd = random.Random(505)
    d = FILTERS
    d += lin('sky5', [(0, '#0a0c24'), (.4, '#1c2050'), (.7, '#2e2a62'), (1, '#140f2a')])
    d += rad('moon5', 250, 300, 140, [(0, '#fffbe8', 1), (.85, '#f2ecd0', 1), (1, '#d8d0b0', 1)])
    d += rad('halo5', 250, 300, 520, [(0, '#e8e4ff', .45), (.4, '#b8b0ff', .15), (1, '#b8b0ff', 0)])
    d += rad('gold5', 830, 540, 280, [(0, '#fff2b0', .95), (.35, '#ffcf5a', .45), (1, '#ffcf5a', 0)])
    d += lin('live5', [(0, '#8a6a3a'), (1, '#3a2a18')])
    d += lin('bark5', [(0, '#3a3058'), (1, '#16122a')], x2=1, y2=0)
    d += lin('hill5', [(0, '#1e1a40'), (1, '#07060f')])
    b = f'<rect width="{W}" height="{H}" fill="url(#sky5)"/>'
    b += dust(rnd, 150, 0, W, 0, 1400, '#eef0ff', .2, .8)
    b += f'<rect width="{W}" height="{H}" fill="url(#halo5)"/><circle cx="250" cy="300" r="140" fill="url(#moon5)"/>'
    for cx, cy, rr in ((210, 260, 22), (290, 330, 30), (240, 350, 13), (310, 240, 15)):
        b += f'<circle cx="{cx}" cy="{cy}" r="{rr}" fill="#d8d0b0" opacity=".5"/>'
    b += '<path d="M0 1640 Q300 1600 560 1630 Q820 1600 1080 1620 L1080 1920 L0 1920Z" fill="url(#hill5)"/>'
    for _ in range(90):
        x = rnd.uniform(0, W); y = 1640 + rnd.uniform(-10, 240)
        b += f'<path d="M{x:.0f} {y:.0f} l-4 -16 M{x:.0f} {y:.0f} l5 -13" stroke="#2a2850" stroke-width="2.5" opacity=".7"/>'
    # ---- the pruned family tree: trunk runs down behind the text, crown on top ----
    TR = [(560, 1700, 540, 770, 150, 92, 12, 0),
          (540, 790, 330, 560, 80, 46, -20, 0),
          (540, 790, 570, 430, 76, 44, 16, 0),
          (340, 575, 220, 440, 44, 30, 8, 0),
          (336, 570, 370, 370, 40, 28, -10, 0),
          (566, 446, 470, 290, 40, 26, -6, 0),
          (570, 440, 690, 300, 40, 26, 10, 0),
          (546, 820, 980, 610, 56, 22, -40, 1)]          # the living branch
    tree = ''
    for x0, y0, x1, y1, w0, w1, bend, alive in TR:
        tree += f'<path d="{taper(x0, y0, x1, y1, w0, w1, bend)}" fill="{"url(#live5)" if alive else "url(#bark5)"}" stroke="#05040c" stroke-width="5" stroke-linejoin="round"/>'
        if alive:
            tree += f'<path d="{taper(x0, y0 - 6, x1, y1 - 4, w0 * .5, w1 * .4, bend)}" fill="#ffd88a" opacity=".4"/>'
    for x0, y0, x1, y1, w0, w1, bend, alive in TR:   # moonlight rim on the left edges
        dx, dy = x1 - x0, y1 - y0; L = math.hypot(dx, dy); nx, ny = -dy / L, dx / L
        if nx > 0: nx, ny = -nx, -ny
        tree += (f'<path d="M{x0 + nx * w0 * .42:.0f} {y0 + ny * w0 * .42:.0f} Q{(x0 + x1) / 2 + nx * (w0 + w1) * .22:.0f} {(y0 + y1) / 2 + ny * (w0 + w1) * .22:.0f} '
                 f'{x1 + nx * w1 * .42:.0f} {y1 + ny * w1 * .42:.0f}" fill="none" stroke="#b8b0f0" stroke-width="4" opacity=".55"/>')
    for _ in range(36):
        x, y = 550 + rnd.uniform(-48, 48), rnd.uniform(1300, 1680)
        tree += f'<path d="M{x:.0f} {y:.0f} q{rnd.uniform(-6, 6):.0f} {-rnd.uniform(20, 50):.0f} {rnd.uniform(-4, 4):.0f} {-rnd.uniform(40, 80):.0f}" fill="none" stroke="#0a0818" stroke-width="3" opacity=".6"/>'
    for ex in (330, 790, 420, 700):
        tree += f'<path d="M560 1680 Q{(560 + ex) / 2} 1700 {ex} {1720 + rnd.uniform(0, 24):.0f}" stroke="#16122a" stroke-width="24" fill="none" stroke-linecap="round"/>'
    for x0, y0, x1, y1, w0, w1, bend, alive in TR[1:]:
        if alive:
            continue
        a = math.degrees(math.atan2(y1 - y0, x1 - x0))
        tree += (f'<g transform="translate({x1} {y1}) rotate({a + 90:.0f})"><ellipse rx="{w1 * .56:.0f}" ry="{w1 * .26:.0f}" fill="#e8d6b0" stroke="#3a2a1a" stroke-width="3"/>'
                 f'<ellipse rx="{w1 * .34:.0f}" ry="{w1 * .15:.0f}" fill="none" stroke="#b8a07a" stroke-width="2"/><ellipse rx="{w1 * .14:.0f}" ry="{w1 * .06:.0f}" fill="none" stroke="#b8a07a" stroke-width="2"/></g>')
    b += tree
    # only three faint ghosts above the cut ends (calmer than the landscape pass)
    for x, y, s, rot, kind in ((150, 470, 96, -28, 'spiny'), (440, 210, 88, -8, 'spade'), (760, 230, 92, 16, 'giant')):
        b += ghost_trilo(x, y, s, rot, kind, .3)
        b += dust(rnd, 5, x - 50, x + 50, y - 70, y - 20, '#d8d4f0', .2, .5)
    # the living branch: leaves, golden glow, the small oval proetid
    b += '<ellipse cx="830" cy="560" rx="270" ry="270" fill="url(#gold5)"/>'
    for lx, ly, la in ((700, 700, -30), (760, 676, 40), (930, 636, -50), (660, 724, 60), (980, 616, 70), (990, 640, 130), (800, 668, 150), (880, 650, -20)):
        b += (f'<g transform="translate({lx} {ly}) rotate({la})"><path d="M0 0 Q16 -30 0 -60 Q-16 -30 0 0Z" fill="#7ac84a" stroke="#1a3a12" stroke-width="3.5"/>'
              f'<path d="M0 -4 L0 -54" stroke="#cfffa0" stroke-width="2.5"/></g>')
    u = 230; R = trilo_dorsal(u, N=10)
    col = {'ceph': '#d89048', 'pyg': '#c47a38', 'pleura': '#c8823e', 'axial': '#e8a45a', 'glab': '#f0b46a'}
    b += '<ellipse cx="830" cy="650" rx="110" ry="18" fill="#1a1020" opacity=".4" filter="url(#b6)"/>'
    b += '<g transform="translate(830 540) rotate(-16)">' + tri_paint(R, col, '#2a1406', 3.6, eyecol='#3a2210', lensfill='#ffd890', glint='#fffbe8') + '</g>'
    b += f'<g transform="translate(830 540) rotate(-16)"><path d="{R["ceph"][0]}" fill="none" stroke="#fff4c8" stroke-width="4" opacity=".6" transform="translate(-3 -3)"/></g>'
    b += spark(700, 400, 24) + spark(990, 450, 18) + spark(1000, 720, 14) + spark(680, 540, 12)
    b += dust(rnd, 12, 680, 1000, 420, 720, '#fff2b0', .4, .9)
    b += text_shade(850, 1350, '#06050f', .5)
    # frog watering the roots
    can = ('<g transform="translate(70 -40) rotate(-10)"><path d="M-22 -24 L22 -24 L18 18 L-18 18Z" fill="#5aa0c8" stroke-width="3.5"/>'
           '<path d="M18 -10 L58 -40 L62 -34 L22 2Z" fill="#5aa0c8" stroke-width="3.5"/><ellipse cx="62" cy="-40" rx="6" ry="10" transform="rotate(40 62 -40)" fill="#4a88b0" stroke-width="3"/>'
           '<path d="M-14 -24 Q0 -46 14 -24" fill="none" stroke-width="5"/><path d="M-16 -16 L-14 10" stroke="#d8f0ff" stroke-width="3" opacity=".8"/></g>')
    FXg, FYg, S = 220, 1790, 3.1
    b += frog(FXg, FYg, S, look=(10, -8), mouth='O', shadow=True, armR='M38 -22 q22 -2 30 -22', armL='M-34 -22 q-18 4 -22 24', front=can)
    a = math.radians(-10); sx_, sy_ = 62 * math.cos(a) + 40 * math.sin(a), 62 * math.sin(a) - 40 * math.cos(a)
    spx, spy = FXg + (70 + sx_) * S + 14, FYg + (-40 + sy_) * S
    for j in range(12):
        t = j / 11
        b += f'<ellipse cx="{spx + t * 60:.0f}" cy="{spy + t * 170 + t * t * 20:.0f}" rx="4" ry="7" fill="#bfe8ff" opacity=".85"/>'
    lines = [('ONLY', 150, 'w'), ('ONE', 232, 'y'), ('SURVIVED', 150, 'w')]
    return vpage('#1c2050', vsvg(d, b), lines, outline='#070616', top=846)


if __name__ == '__main__':
    for n in (sys.argv[1:] or ['1', '2', '3', '4', '5']):
        out = os.path.join(VID, f'trilobite-extinction-short{n}', 'thumb', 'A.html')
        open(out, 'w').write(globals()[f'make_{n}']())
    print('ok')
