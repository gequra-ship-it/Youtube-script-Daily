# Shorts thumbnails (style B, guideline 16-9) for human-temperature-limits-short1..5. VERTICAL 1080x1920, glowing subject in the top half,
# hook centred on a dark band (y ~860-1240), frog in a bottom corner. Tasteful: no bodies, no gore.
# Run: python3 videos/human-temperature-limits-short1/thumb/make_all.py [1 2 3 4 5] -> videos/human-temperature-limits-shortN/thumb/A.html
# 1 SWEAT STOPS WORKING  wet-bulb thermometer (wet cloth on the bulb, drips) glowing in steamy saturated night air; sweaty frog with a fan
# 2 WHY STRIP IN SNOW?   coat, scarf and glove left on night snow, a warm orange heat-wave plume rising from them; shivering frog in beanie
# 3 NOT DEAD UNTIL WARM  brain sealed in a glowing ice block (cold protects the brain), heartbeat line below; paramedic frog with warm mug
# 4 THEY CRAWL TO HIDE   frosty moonlit bedroom, frost hand prints crawling into the glowing gap under the bed; frog in nightcap with candle
# 5 ONLY 14 DEGREES      big dial from -89 (Antarctica) to 56 (Death Valley), the narrow 28-42 living window glows, needle at 37; frog in goggles
import os, sys, math, random, shutil
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
sys.path.insert(0, os.path.join(REPO, 'tools'))
sys.path.insert(0, os.path.join(REPO, 'videos', 'trilobite-extinction', 'thumb'))
from make import frog, FILTERS, INK, GREEN   # shared posable frog (eye white #f4f5ea, pupil kept inside)
from thumb_lib import vpage, vsvg, lin, rad, spark, fireflies, halo, darkband

W, H = 1080, 1920
Y = lambda w: f'<span class="g">{w}</span>'


def vig(id='vig', a=.75):
    return rad(id, 540, 960, 1250, [(0, '#000', 0), (.5, '#000', 0), (1, '#000', a)])


def save(n, bg, d, b, lines, outline, top):
    out = os.path.join(REPO, 'videos', f'human-temperature-limits-short{n}', 'thumb'); os.makedirs(out, exist_ok=True)
    for f in os.listdir(os.path.join(REPO, 'tools', 'assets', 'thumb_v')):
        shutil.copy(os.path.join(REPO, 'tools', 'assets', 'thumb_v', f), out)
    open(os.path.join(out, 'A.html'), 'w').write(vpage(bg, vsvg(d, b), lines, outline=outline, top=top))


def drop(x, y, s, fill='#cdeeff', line='#1a3a4a', sw=4):
    return (f'<path d="M{x} {y - 1.6 * s:.0f} q{s * .9:.0f} {s * 1.2:.0f} {s * .9:.0f} {s * 1.9:.0f} a{s * .9:.0f} {s * .9:.0f} 0 0 1 {-s * 1.8:.0f} 0 '
            f'q0 {-s * .7:.0f} {s * .9:.0f} {-s * 1.9:.0f}z" fill="{fill}" stroke="{line}" stroke-width="{sw}"/>'
            f'<ellipse cx="{x - s * .35:.0f}" cy="{y + s * .1:.0f}" rx="{s * .2:.0f}" ry="{s * .35:.0f}" fill="#fff" opacity=".8"/>')


def text(x, y, s, t, col, anchor='middle', op=1):
    return (f'<text x="{x}" y="{y}" font-family="Fredoka" font-weight="700" font-size="{s}" text-anchor="{anchor}" fill="{col}" '
            f'stroke="#050b18" stroke-width="{s * .14:.0f}" paint-order="stroke" opacity="{op}">{t}</text>')


# ================= 1: SWEAT STOPS WORKING =================
def make_1():
    rnd = random.Random(1)
    TX, T0, T1, BY, BR = 540, 120, 640, 700, 92
    d = FILTERS + rad('bg1', 540, 520, 1500, [(0, '#5a1a12', 1), (.35, '#2a0a0c', 1), (1, '#060204', 1)]) + vig()
    d += halo('h1', TX, 470, 560, inner='#fff2c8', outer='#ff6a2a')
    d += lin('glass', [(0, '#ffffff'), (.25, '#dff4ff'), (.7, '#9ec8dc'), (1, '#5f8aa0')], x2=1, y2=0)
    d += lin('merc', [(0, '#ff9a6a'), (.5, '#ff2a1a'), (1, '#a0100a')], x2=1, y2=0)
    d += lin('cloth', [(0, '#f4fbff'), (.5, '#b8d4e2'), (1, '#6e93a8')], x2=1, y2=.3)
    b = f'<rect width="{W}" height="{H}" fill="url(#bg1)"/>'
    b += f'<ellipse cx="{TX}" cy="470" rx="600" ry="600" fill="url(#h1)" opacity=".85"/>'
    # humid steam: soft drifting clouds + rising wisps
    for _ in range(16):
        b += f'<ellipse cx="{rnd.randint(-60, 1140)}" cy="{rnd.randint(80, 1850)}" rx="{rnd.randint(140, 300)}" ry="{rnd.randint(40, 90)}" fill="#ffd8c0" opacity="{rnd.uniform(.05, .13):.2f}" filter="url(#b24)"/>'
    for x in (150, 290, 800, 930):
        y0 = rnd.randint(560, 760)
        b += f'<path d="M{x} {y0} q-40 -70 0 -140 q40 -70 0 -140 q-40 -70 0 -140" fill="none" stroke="#ffe6d0" stroke-width="16" opacity=".22" filter="url(#b6)"/>'
    # thermometer: glass tube + scale + red column almost at the top
    b += f'<rect x="{TX - 60}" y="{T0 - 20}" width="120" height="{T1 - T0 + 80}" rx="60" fill="#fff0c0" opacity=".35" filter="url(#b24)"/>'
    b += f'<rect x="{TX - 44}" y="{T0}" width="88" height="{T1 - T0 + 40}" rx="44" fill="url(#glass)" stroke="#1a0a08" stroke-width="10"/>'
    b += f'<rect x="{TX - 16}" y="{T0 + 40}" width="32" height="{T1 - T0}" rx="16" fill="#f4e8e0" opacity=".6"/>'
    b += f'<rect x="{TX - 14}" y="{T0 + 52}" width="28" height="{T1 - T0}" rx="14" fill="url(#merc)"/>'
    b += f'<rect x="{TX - 14}" y="{T0 + 52}" width="28" height="{T1 - T0}" rx="14" fill="#ff5a3a" opacity=".5" filter="url(#b12)"/>'
    for k in range(13):
        y = T0 + 70 + k * 38; L = 34 if k % 2 == 0 else 20
        b += f'<path d="M{TX + 44 + 10} {y} l{L} 0" stroke="#ffe8d8" stroke-width="6" stroke-linecap="round" opacity=".85"/>'
    b += f'<path d="M{TX - 30} {T0 + 30} L{TX - 30} {T1}" stroke="#fff" stroke-width="9" stroke-linecap="round" opacity=".8"/>'
    # bulb wrapped in a wet cloth (wick), tied with string
    b += f'<circle cx="{TX}" cy="{BY}" r="{BR + 40}" fill="#ffb07a" opacity=".45" filter="url(#b24)"/>'
    cl = f'M{TX - 50} {BY - 92} Q{TX - 112} {BY - 40} {TX - 96} {BY + 30} Q{TX - 80} {BY + 96} {TX} {BY + 100} Q{TX + 84} {BY + 96} {TX + 98} {BY + 26} Q{TX + 110} {BY - 44} {TX + 50} {BY - 92}Z'
    b += f'<path d="{cl}" fill="url(#cloth)" stroke="#1a0a08" stroke-width="10" stroke-linejoin="round"/>'
    for p in (f'M{TX - 60} {BY - 70} q-10 70 20 150', f'M{TX - 10} {BY - 88} q-14 90 6 180', f'M{TX + 40} {BY - 84} q22 80 -4 176', f'M{TX + 78} {BY - 40} q8 60 -18 110'):
        b += f'<path d="{p}" fill="none" stroke="#5a7c90" stroke-width="5" opacity=".7"/>'
    for x, y, rx, ry in ((TX - 40, BY + 20, 26, 40), (TX + 36, BY + 50, 30, 26), (TX + 10, BY - 30, 18, 24)):
        b += f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{ry}" fill="#4e7488" opacity=".35"/>'
    b += f'<path d="M{TX - 60} {BY - 52} q-20 36 -12 82" fill="none" stroke="#fff" stroke-width="8" stroke-linecap="round" opacity=".85"/>'
    b += f'<path d="M{TX - 56} {BY - 84} q56 18 112 0" fill="none" stroke="#1a0a08" stroke-width="14"/><path d="M{TX - 56} {BY - 84} q56 18 112 0" fill="none" stroke="#e8c070" stroke-width="7"/>'
    # drips pooling and falling uselessly (stay above the text zone)
    for x, y, s in ((TX - 30, BY + 128, 14), (TX + 34, BY + 120, 11), (TX + 4, 830, 12)):
        b += drop(x, y, s, sw=3.5)
    # sweat-like drops and glints
    for x, y, s in ((210, 300, 22), (880, 250, 18), (840, 560, 26), (230, 610, 16)):
        b += drop(x, y, s, fill='#d6f2ff', sw=4)
    for sx, sy, ss in ((TX + 120, 170, 26), (TX - 150, 380, 18), (TX + 160, 520, 16), (TX - 130, 740, 20)):
        b += spark(sx, sy, ss, col='#fff4d8')
    b += fireflies(42, 140, 1820, col='#ffcfa0', core='#fff4e0', seed=11)
    b += darkband(860, 1240, .55)
    # lower: steamy jungle leaves
    for x, y, r, s in ((60, 1600, -30, 1.5), (1020, 1520, 210, 1.7), (980, 1860, 200, 1.3), (130, 1880, -10, 1.2), (760, 1900, 230, 1.1)):
        b += (f'<g transform="translate({x} {y}) rotate({r}) scale({s})"><path d="M0 0 q120 -90 260 -20 q-120 70 -260 20z" fill="#1c3a20" stroke="#081408" stroke-width="5"/>'
              '<path d="M10 -2 q120 -30 240 -16" fill="none" stroke="#3a6a3a" stroke-width="4"/></g>')
    # frog: sweating hard, fanning itself with a paper fan
    fan = ('<g transform="translate(70 -88) rotate(18)"><path d="M0 30 L-34 -26 A66 66 0 0 1 34 -26Z" fill="#f2d27a" stroke-width="3.2"/>'
           '<path d="M0 30 L-17 -32 M0 30 L0 -36 M0 30 L17 -32" fill="none" stroke="#a87a2a" stroke-width="2.4"/>'
           '<path d="M0 30 L0 48" stroke-width="5"/></g>')
    sweat = ''.join(drop(x, y, s, fill='#cdeeff', line=INK, sw=2.2) for x, y, s in ((-42, -78, 6), (-38, -54, 4.5), (46, -96, 5)))
    b += '<ellipse cx="280" cy="1620" rx="240" ry="200" fill="#ffb07a" opacity=".16" filter="url(#b24)"/>'
    b += frog(280, 1770, 3.3, look=(2, -5), mouth='O', shadow=True, armR='M38 -22 q24 -10 30 -36', armL='M-34 -22 q-14 6 -16 22', front=fan + sweat)
    b += f'<rect width="{W}" height="{H}" fill="url(#vig)"/>'
    save(1, '#060204', d, b, [(Y('SWEAT'), 236, 'w'), ('STOPS WORKING', 118, 'w')], '#140406', 876)


# ================= 2: WHY STRIP IN SNOW? =================
def make_2():
    rnd = random.Random(2)
    d = FILTERS + lin('sky2', [(0, '#050a1e'), (.5, '#0e2348'), (1, '#1a3a64')]) + vig()
    d += lin('snow2', [(0, '#dceaff'), (.4, '#8eaad0'), (1, '#2a4268')])
    d += halo('h2', 540, 560, 520, inner='#fff0c0', outer='#ff7a2a')
    d += lin('coat', [(0, '#d0503a'), (1, '#7a1e18')], x2=.4, y2=1)
    b = f'<rect width="{W}" height="{H}" fill="url(#sky2)"/>'
    for _ in range(80):
        b += f'<circle cx="{rnd.randint(0, W)}" cy="{rnd.randint(0, 420)}" r="{rnd.choice([1.2, 1.8, 2.4])}" fill="#eaf4ff" opacity="{rnd.uniform(.3, .9):.2f}"/>'
    # pine silhouettes on the horizon
    for x, h in ((40, 220), (140, 300), (230, 200), (860, 260), (960, 330), (1050, 230)):
        b += f'<path d="M{x} {470 - h} L{x - h * .28:.0f} 480 L{x + h * .28:.0f} 480Z" fill="#081428"/>'
    b += '<path d="M0 470 q270 -60 540 -20 q270 -40 540 10 L1080 1920 L0 1920Z" fill="url(#snow2)"/>'
    b += '<path d="M0 470 q270 -60 540 -20 q270 -40 540 10" fill="none" stroke="#f4faff" stroke-width="5" opacity=".7"/>'
    # warm halo + heat-wave plume rising from the clothes
    b += '<ellipse cx="540" cy="560" rx="560" ry="560" fill="url(#h2)" opacity=".85"/>'
    b += '<ellipse cx="540" cy="660" rx="380" ry="120" fill="#ffb060" opacity=".5" filter="url(#b50)"/>'
    for k, x in enumerate((340, 420, 500, 580, 660, 740)):
        h = 380 + (k % 3) * 60
        b += (f'<path d="M{x} 620 q-34 -{h / 6:.0f} 0 -{h / 3:.0f} q34 -{h / 6:.0f} 0 -{h / 3:.0f} q-34 -{h / 6:.0f} 0 -{h / 3:.0f}" fill="none" stroke="#ff9a40" stroke-width="22" opacity=".35" filter="url(#b6)"/>'
              f'<path d="M{x} 620 q-34 -{h / 6:.0f} 0 -{h / 3:.0f} q34 -{h / 6:.0f} 0 -{h / 3:.0f} q-34 -{h / 6:.0f} 0 -{h / 3:.0f}" fill="none" stroke="#ffe0a0" stroke-width="6" opacity=".75"/>')
    # coat lying open on the snow (slightly foreshortened)
    S = '#2a0806'
    b += '<ellipse cx="540" cy="740" rx="320" ry="44" fill="#1a2a48" opacity=".55" filter="url(#b12)"/>'
    b += f'<path d="M380 560 L250 690 Q235 720 270 730 L370 650Z" fill="url(#coat)" stroke="{S}" stroke-width="9" stroke-linejoin="round"/>'
    b += f'<path d="M700 560 L840 660 Q870 690 840 712 L712 650Z" fill="url(#coat)" stroke="{S}" stroke-width="9" stroke-linejoin="round"/>'
    b += f'<path d="M400 540 Q540 510 680 540 L720 740 Q540 770 360 740Z" fill="url(#coat)" stroke="{S}" stroke-width="10" stroke-linejoin="round"/>'
    b += f'<path d="M540 528 L540 752" stroke="{S}" stroke-width="6"/><path d="M420 548 L470 600 L540 532 L610 600 L660 548" fill="#a02a22" stroke="{S}" stroke-width="7" stroke-linejoin="round"/>'
    for y in (620, 670, 715):
        b += f'<circle cx="560" cy="{y}" r="9" fill="#f2d27a" stroke="{S}" stroke-width="3"/>'
    b += f'<path d="M420 640 l70 0 M600 640 l70 0" stroke="{S}" stroke-width="5"/>'
    b += '<path d="M415 560 Q400 650 380 730" fill="none" stroke="#ff9a7a" stroke-width="6" opacity=".6"/>'
    b += '<path d="M260 700 l40 22 M836 702 l-30 14" stroke="#fff" stroke-width="5" opacity=".35"/>'
    # scarf (yellow/red stripes) trailing to the left
    sc = 'M470 560 Q360 600 300 650 Q220 720 140 760'
    b += f'<path d="{sc}" fill="none" stroke="{S}" stroke-width="54" stroke-linecap="round"/><path d="{sc}" fill="none" stroke="#f2c84a" stroke-width="40" stroke-linecap="round"/>'
    b += f'<path d="{sc}" fill="none" stroke="#c0302a" stroke-width="40" stroke-dasharray="22 34" />'
    for k in range(5):
        b += f'<path d="M{122 + k * 9} {752 + k * 7} l-26 22" stroke="#f2c84a" stroke-width="7" stroke-linecap="round"/>'
    # glove lying to the right
    b += (f'<g transform="translate(920 760) rotate(-24)"><path d="M-40 10 q-6 -40 6 -50 l0 -40 q10 -10 18 0 l2 36 l6 -46 q10 -10 18 0 l-2 46 l10 -40 q10 -8 16 2 l-6 44 '
          f'l18 -24 q12 -4 14 8 l-26 46 q-12 26 -40 26 q-22 2 -34 -8z" fill="#3a6ac0" stroke="{S}" stroke-width="7" stroke-linejoin="round"/>'
          f'<path d="M-42 6 q24 14 60 6" fill="none" stroke="#e8f0ff" stroke-width="12"/></g>')
    for sx, sy, ss in ((540, 180, 30), (300, 300, 18), (790, 340, 20), (200, 600, 14), (900, 560, 16)):
        b += spark(sx, sy, ss, col='#fff0d0')
    b += fireflies(60, 80, 1840, col='#dbeaff', core='#ffffff', seed=21)
    b += darkband(860, 1240, .5)
    # lower: snow drift + pines
    b += '<path d="M0 1500 q300 -70 600 -10 q260 50 480 -20 L1080 1920 L0 1920Z" fill="#b6cbe8" opacity=".55"/>'
    for x, y, h in ((90, 1560, 300), (200, 1600, 220), (990, 1520, 280)):
        b += f'<path d="M{x} {y - h} L{x - h * .3:.0f} {y} L{x + h * .3:.0f} {y}Z" fill="#0b1c34" opacity=".9"/>'
    # frog: shivering in a beanie and scarf, breath puff
    head = ('<path d="M-30 -80 q36 -58 72 0z" fill="#3a6ac0" stroke-width="3.4"/><path d="M-32 -80 q38 -10 76 0" fill="none" stroke-width="10"/>'
            '<path d="M-32 -80 q38 -10 76 0" fill="none" stroke="#e8f0ff" stroke-width="6"/><circle cx="6" cy="-122" r="10" fill="#e8f0ff" stroke-width="3"/>')
    mid = '<path d="M-30 -30 q36 12 70 0 l2 14 q-38 12 -74 0z" fill="#f2c84a" stroke-width="3.2"/><path d="M26 -22 l4 34 l14 -2 l-6 -32z" fill="#c0302a" stroke-width="3"/>'
    front = '<g fill="#eaf4ff" stroke="none" opacity=".75"><circle cx="58" cy="-40" r="8"/><circle cx="72" cy="-48" r="10"/><circle cx="86" cy="-44" r="7"/></g>'
    shiv = '<path d="M-50 -60 l-8 4 l6 4 M-52 -40 l-8 3 l7 4" fill="none" stroke="#eaf4ff" stroke-width="2.6"/>'
    b += '<ellipse cx="800" cy="1640" rx="240" ry="200" fill="#ffb060" opacity=".14" filter="url(#b24)"/>'
    b += frog(800, 1770, 3.3, look=(-6, -4), mouth='o', shadow=True, mid=head + mid, front=front + shiv,
              armL='M-34 -22 q16 6 30 0', armR='M38 -22 q-14 8 -30 2')
    b += f'<rect width="{W}" height="{H}" fill="url(#vig)"/>'
    save(2, '#050a1e', d, b, [('WHY STRIP', 160, 'w'), (Y('IN SNOW?'), 196, 'w')], '#040a18', 880)


# ================= 3: NOT DEAD UNTIL WARM =================
def brain(cx, cy, s, fill='#f2a8c0', line='#7a2a4a'):
    g = f'<g transform="translate({cx} {cy}) scale({s})" stroke-linecap="round" stroke-linejoin="round">'
    outline = ('M-120 10 q-30 -10 -20 -50 q-4 -50 46 -66 q20 -40 74 -30 q30 -26 74 -6 q50 -8 66 34 q46 14 34 62 q24 34 -6 64 q-6 40 -54 42 '
               'q-24 26 -64 12 q-30 20 -66 0 q-46 8 -60 -26 q-40 -6 -24 -36z')
    g += f'<path d="{outline}" fill="{fill}" stroke="{line}" stroke-width="9"/>'
    for p in ('M-100 -20 q30 -10 30 20 q0 26 30 22', 'M-60 -76 q-6 30 24 34 q30 4 26 34', 'M10 -96 q-10 30 18 40 q28 8 22 40',
              'M70 -70 q-20 26 4 46 q24 18 2 44', 'M110 -10 q-30 0 -30 30 q0 26 -30 30', 'M-90 50 q30 -14 50 6 q20 22 46 6',
              'M20 40 q20 -20 46 -4', 'M-30 -30 q20 -10 30 10'):
        g += f'<path d="{p}" fill="none" stroke="{line}" stroke-width="7"/>'
    g += f'<path d="M0 -100 q-10 60 4 150" fill="none" stroke="{line}" stroke-width="8"/>'
    g += '<path d="M-110 -30 q10 -40 50 -56" fill="none" stroke="#fff" stroke-width="7" opacity=".6"/>'
    return g + '</g>'


def make_3():
    rnd = random.Random(3)
    CX, CY = 540, 480
    d = FILTERS + rad('bg3', 540, 520, 1500, [(0, '#0e4a66', 1), (.35, '#062234', 1), (1, '#01060c', 1)]) + vig()
    d += halo('h3', CX, CY, 600, inner='#e8ffff', outer='#36d0ff')
    d += lin('iceF', [(0, '#d8fbff'), (.5, '#7fd4f0'), (1, '#2a8ab8')], x2=.6, y2=1)
    d += lin('iceT', [(0, '#ffffff'), (1, '#bdeeff')])
    d += lin('iceS', [(0, '#5ab8e0'), (1, '#1a5a88')])
    b = f'<rect width="{W}" height="{H}" fill="url(#bg3)"/>'
    b += f'<ellipse cx="{CX}" cy="{CY}" rx="620" ry="620" fill="url(#h3)" opacity=".9"/>'
    for x0, x1 in ((180, 330), (460, 560), (760, 900)):
        b += f'<path d="M{CX} -40 L{x0} 900 L{x1} 900Z" fill="#c8f6ff" opacity=".06"/>'
    # ice block: front face, top face, right face
    F = (CX - 250, CY - 190, CX + 190, CY + 300)   # x0, y0, x1, y1 of the front face
    x0, y0, x1, y1 = F; dx, dy = 90, -80
    b += f'<rect x="{x0 - 40}" y="{y0 - 60}" width="{x1 - x0 + 160}" height="{y1 - y0 + 120}" rx="40" fill="#9ff0ff" opacity=".35" filter="url(#b50)"/>'
    b += f'<path d="M{x1} {y0} l{dx} {dy} L{x1 + dx} {y1 + dy} L{x1} {y1}Z" fill="url(#iceS)" stroke="#04202e" stroke-width="10" stroke-linejoin="round"/>'
    b += f'<path d="M{x0} {y0} l{dx} {dy} L{x1 + dx} {y0 + dy} L{x1} {y0}Z" fill="url(#iceT)" stroke="#04202e" stroke-width="10" stroke-linejoin="round"/>'
    b += f'<rect x="{x0}" y="{y0}" width="{x1 - x0}" height="{y1 - y0}" rx="14" fill="url(#iceF)" opacity=".75"/>'
    # brain inside (glowing softly through the ice)
    b += f'<ellipse cx="{(x0 + x1) / 2}" cy="{(y0 + y1) / 2}" rx="200" ry="160" fill="#ffd0e0" opacity=".55" filter="url(#b24)"/>'
    b += brain((x0 + x1) / 2, (y0 + y1) / 2 + 10, 1.35)
    b += f'<rect x="{x0}" y="{y0}" width="{x1 - x0}" height="{y1 - y0}" rx="14" fill="#bff2ff" opacity=".28"/>'
    # frost, bubbles, cracks and highlights on the front face
    for _ in range(26):
        b += f'<circle cx="{rnd.randint(x0 + 20, x1 - 20)}" cy="{rnd.randint(y0 + 20, y1 - 20)}" r="{rnd.choice([3, 4, 6, 8])}" fill="none" stroke="#f0ffff" stroke-width="2.4" opacity=".6"/>'
    b += f'<path d="M{x0 + 30} {y0 + 40} l120 90 l-30 60 l90 70 M{x1 - 40} {y1 - 30} l-80 -60 l20 -50" fill="none" stroke="#f4ffff" stroke-width="4" opacity=".7"/>'
    b += f'<path d="M{x0 + 26} {y1 - 40} L{x0 + 26} {y0 + 30} L{x0 + 120} {y0 + 30}" fill="none" stroke="#fff" stroke-width="12" stroke-linecap="round" opacity=".85"/>'
    b += f'<path d="M{x0 + 50} {y1 - 70} L{x0 + 50} {y1 - 160}" stroke="#fff" stroke-width="7" stroke-linecap="round" opacity=".6"/>'
    b += f'<rect x="{x0}" y="{y0}" width="{x1 - x0}" height="{y1 - y0}" rx="14" fill="none" stroke="#04202e" stroke-width="10"/>'
    b += f'<path d="M{x0 + 10} {y0 + 6} L{x1 - 10} {y0 + 6}" stroke="#ffffff" stroke-width="5" opacity=".8"/>'
    # icicles dripping from the bottom edge (kept short)
    for x in range(x0 + 40, x1 - 20, 70):
        b += f'<path d="M{x - 12} {y1} L{x} {y1 + rnd.randint(30, 60)} L{x + 12} {y1}Z" fill="#dff8ff" stroke="#04202e" stroke-width="4" stroke-linejoin="round"/>'
    for sx, sy, ss in ((x1 + 120, y0 - 60, 30), (x0 - 50, y0 + 40, 22), (x1 + 90, y1 - 40, 18), (x0 - 40, y1 - 120, 16), (CX + 20, y0 - 150, 18)):
        b += spark(sx, sy, ss, col='#f0ffff')
    b += fireflies(50, 100, 1840, col='#9ff0ff', core='#efffff', seed=31)
    b += darkband(860, 1240, .5)
    # heartbeat line coming back (flat -> one beat) below the text, behind the frog
    ecg = 'M0 1420 L440 1420 L470 1390 L500 1420 L540 1420 L565 1300 L600 1520 L630 1380 L660 1420 L1080 1420'
    b += f'<path d="{ecg}" fill="none" stroke="#5aff9a" stroke-width="22" opacity=".35" filter="url(#b6)"/><path d="{ecg}" fill="none" stroke="#c8ffd8" stroke-width="7" stroke-linejoin="round"/>'
    b += '<circle cx="1080" cy="1420" r="30" fill="#5aff9a" opacity=".4" filter="url(#b12)"/>'
    # paramedic frog with a steaming warm mug
    head = '<path d="M-30 -82 q36 -40 72 0z" fill="#f4f4f4" stroke-width="3.2"/><path d="M0 -104 l12 0 M6 -110 l0 12" stroke="#d03030" stroke-width="4.5"/>'
    mug = ('<g transform="translate(64 -60)"><circle cx="0" cy="0" r="30" fill="#ffb060" opacity=".5" stroke="none" filter="url(#b12)"/>'
           '<path d="M-16 -16 l32 0 l-3 34 q-13 6 -26 0z" fill="#e86a3a" stroke-width="3.2"/><path d="M16 -8 q12 0 10 12 q-2 8 -12 6" fill="none" stroke-width="3.2"/>'
           '<path d="M-6 -24 q-6 -8 0 -16 M6 -24 q6 -8 0 -16" fill="none" stroke="#fff3d0" stroke-width="2.6" opacity=".8"/></g>')
    blanket = '<path d="M-36 -34 q40 14 80 0 l6 34 q-46 14 -92 0z" fill="#e8a03a" stroke-width="3.2"/><path d="M-30 -20 l70 0" stroke="#fff0c0" stroke-width="2.4"/>'
    b += '<ellipse cx="270" cy="1640" rx="230" ry="200" fill="#ffb060" opacity=".15" filter="url(#b24)"/>'
    b += frog(270, 1770, 3.3, look=(3, -5), mouth='O', shadow=True, mid=head + blanket, front=mug, armR='M38 -22 q16 -2 20 -32', armL='M-34 -22 q-14 6 -16 22')
    b += f'<rect width="{W}" height="{H}" fill="url(#vig)"/>'
    save(3, '#01060c', d, b, [('NOT DEAD', 172, 'w'), ('UNTIL ' + Y('WARM'), 150, 'w')], '#020a14', 890)


# ================= 4: THEY CRAWL TO HIDE =================
def handprint(x, y, s, rot, col='#dff6ff'):
    g = f'<g transform="translate({x} {y}) rotate({rot}) scale({s})" fill="{col}">'
    g += '<ellipse cx="0" cy="0" rx="14" ry="16"/>'
    for fx, fy, fr in ((-12, -22, -20), (-4, -28, -6), (5, -27, 6), (13, -20, 20), (-20, -2, -60)):
        g += f'<ellipse cx="{fx}" cy="{fy}" rx="4" ry="9" transform="rotate({fr} {fx} {fy})"/>'
    return g + '</g>'


def make_4():
    rnd = random.Random(4)
    d = FILTERS + lin('wall4', [(0, '#0a1430'), (1, '#142a50')]) + vig()
    d += lin('floor4', [(0, '#24324c'), (1, '#0a1020')])
    d += halo('h4', 560, 600, 380, inner='#fff0c0', outer='#ff9a40')
    d += lin('blk4', [(0, '#5a7ac0'), (1, '#2a3a78')])
    b = f'<rect width="{W}" height="{H}" fill="url(#wall4)"/>'
    # window with moon and frost, cold beam
    b += '<rect x="90" y="110" width="300" height="300" rx="10" fill="#0c2a50" stroke="#050a18" stroke-width="12"/>'
    b += '<circle cx="250" cy="230" r="60" fill="#f0fbff"/><circle cx="250" cy="230" r="120" fill="#bfe8ff" opacity=".35" filter="url(#b24)"/>'
    b += '<path d="M240 110 L240 410 M90 260 L390 260" stroke="#050a18" stroke-width="12"/>'
    for _ in range(14):
        x, y = rnd.choice([(rnd.randint(95, 150), rnd.randint(115, 405)), (rnd.randint(95, 385), rnd.randint(360, 405))])
        b += spark(x, y, rnd.choice([8, 10, 14]), col='#eaf8ff', op=.8)
    b += '<path d="M90 410 L390 410 L640 720 L260 760Z" fill="#cfefff" opacity=".1"/>'
    # floor
    b += '<path d="M0 560 L1080 560 L1080 1920 L0 1920Z" fill="url(#floor4)"/>'
    for k in range(9):
        b += f'<path d="M0 {600 + k * k * 18} L1080 {600 + k * k * 18}" stroke="#05080f" stroke-width="5" opacity=".6"/>'
    b += '<path d="M0 560 L1080 560" stroke="#3a4a6a" stroke-width="6"/>'
    # bed (side view): legs, frame, glowing gap below, mattress, blanket draping down, pillow, headboard
    b += '<ellipse cx="600" cy="600" rx="380" ry="200" fill="url(#h4)"/>'
    b += '<rect x="300" y="560" width="600" height="120" fill="#ffb060" opacity=".75" filter="url(#b24)"/>'
    b += '<rect x="330" y="580" width="540" height="80" fill="#fff0c0" opacity=".85" filter="url(#b12)"/>'
    S = '#040814'
    for x in (250, 920):
        b += f'<rect x="{x}" y="470" width="34" height="230" rx="6" fill="#4a2e1e" stroke="{S}" stroke-width="7"/>'
    b += f'<rect x="230" y="250" width="56" height="330" rx="14" fill="#5a3a26" stroke="{S}" stroke-width="9"/>'
    b += f'<rect x="240" y="460" width="720" height="60" rx="8" fill="#5a3a26" stroke="{S}" stroke-width="9"/>'
    b += f'<rect x="270" y="380" width="680" height="90" rx="20" fill="#d8e0f0" stroke="{S}" stroke-width="9"/>'
    b += f'<path d="M300 390 q70 -50 150 -8 q10 34 -10 50 q-70 20 -140 -6z" fill="#f0f4ff" stroke="{S}" stroke-width="8"/>'
    b += f'<path d="M440 360 q240 -30 520 10 L990 560 q-30 20 -60 0 q-30 22 -60 0 q-30 22 -60 0 L860 520 L440 470Z" fill="url(#blk4)" stroke="{S}" stroke-width="9" stroke-linejoin="round"/>'
    b += '<path d="M460 380 q220 -26 480 6" fill="none" stroke="#a8c0ff" stroke-width="6" opacity=".7"/>'
    for x in range(470, 950, 90):
        b += spark(x, 395 + rnd.randint(-8, 8), 7, col='#eaf8ff', op=.7)
    # frost hand prints crawling across the floor into the gap
    for i, (x, y, r) in enumerate(((140, 830, 70), (220, 790, 60), (280, 780, 76), (350, 735, 64), (410, 720, 78), (470, 680, 66))):
        b += f'<ellipse cx="{x}" cy="{y}" rx="40" ry="30" fill="#9fe6ff" opacity=".35" filter="url(#b12)"/>'
        b += handprint(x, y, 1.5 + i * .03, r, col='#e8f8ff')
    for _ in range(30):
        b += f'<path d="M{rnd.randint(0, 1080)} {rnd.randint(570, 840)} l{rnd.randint(10, 30)} {rnd.randint(-6, 6)}" stroke="#cfefff" stroke-width="3" opacity=".35"/>'
    for sx, sy, ss in ((700, 610, 22), (520, 640, 16), (880, 280, 24), (620, 230, 16)):
        b += spark(sx, sy, ss, col='#fff4d8')
    b += fireflies(46, 90, 1840, col='#cfeaff', core='#ffffff', seed=41)
    b += darkband(860, 1240, .55)
    # lower: frosty floorboards, frog in a nightcap holding a candle, peeking toward the bed
    for _ in range(18):
        x, y = rnd.randint(0, 1080), rnd.randint(1300, 1880)
        b += spark(x, y, rnd.choice([8, 10, 12]), col='#cfefff', op=.5)
    cap = ('<path d="M-30 -80 q30 -40 72 -6 q20 20 40 6 l4 10 q-26 16 -50 -6 q-30 -20 -66 -4z" fill="#5a7ac0" stroke-width="3.2"/>'
           '<circle cx="86" cy="-70" r="9" fill="#f0f4ff" stroke-width="3"/>')
    candle = ('<g transform="translate(-58 -40)"><circle cx="0" cy="-34" r="34" fill="#ffd070" opacity=".55" stroke="none" filter="url(#b12)"/>'
              '<rect x="-7" y="-20" width="14" height="30" rx="3" fill="#f4ecd8" stroke-width="2.6"/><path d="M-16 10 l32 0 q-4 8 -16 8 q-12 0 -16 -8z" fill="#c8a040" stroke-width="2.6"/>'
              '<path d="M0 -22 q-8 -10 0 -24 q8 14 0 24z" fill="#ffd060" stroke="#c06010" stroke-width="2"/></g>')
    b += '<ellipse cx="780" cy="1630" rx="240" ry="200" fill="#ffb060" opacity=".16" filter="url(#b24)"/>'
    b += frog(790, 1770, 3.3, look=(-5, -5), mouth='O', shadow=True, mid=cap, front=candle, armL='M-34 -22 q-14 -2 -22 -20', armR='M38 -22 q14 6 16 22')
    b += f'<rect width="{W}" height="{H}" fill="url(#vig)"/>'
    save(4, '#050a18', d, b, [('THEY CRAWL', 160, 'w'), ('TO ' + Y('HIDE'), 220, 'w')], '#040814', 870)


# ================= 5: ONLY 14 DEGREES =================
def make_5():
    rnd = random.Random(5)
    CX, CY, R = 540, 720, 372
    LO, HI = -89, 56
    ang = lambda t: math.radians(180 + (t - LO) / (HI - LO) * 180)   # -89 at left, 56 at right
    P = lambda t, r: (CX + r * math.cos(ang(t)), CY + r * math.sin(ang(t)))
    d = FILTERS + lin('bg5', [(0, '#0a2a5a'), (.5, '#0a0610'), (1, '#5a1a08')], x2=1, y2=0) + vig()
    d += rad('fade5', 540, 900, 1100, [(0, '#000', 0), (1, '#000', .6)])
    d += halo('h5', *P(37, R * .78), 360, inner='#fff8d0', outer='#ffd040')
    d += lin('arc5', [(0, '#5ab8ff'), (.45, '#a8e8ff'), (.6, '#ffe08a'), (1, '#ff4a1a')], x2=1, y2=0)
    b = f'<rect width="{W}" height="{H}" fill="url(#bg5)"/><rect width="{W}" height="{H}" fill="url(#fade5)"/>'
    # ice shards left, desert sun glow right
    b += '<circle cx="1060" cy="240" r="220" fill="#ff8a30" opacity=".35" filter="url(#b50)"/><circle cx="1040" cy="250" r="70" fill="#ffd08a" opacity=".8" filter="url(#b6)"/>'
    for x, h in ((0, 330), (70, 230), (130, 150)):
        b += f'<path d="M{x - 40} 820 L{x + 20} {820 - h} L{x + 70} 820Z" fill="#9fdcff" stroke="#062040" stroke-width="7" opacity=".85"/>'
    b += '<path d="M880 820 q100 -90 220 -60 L1100 820Z" fill="#c8662a" stroke="#2a0a04" stroke-width="7"/>'
    # dial face
    b += f'<path d="M{CX - R - 30} {CY} A{R + 30} {R + 30} 0 0 1 {CX + R + 30} {CY} L{CX + R + 30} {CY + 70} L{CX - R - 30} {CY + 70}Z" fill="#141a26" stroke="#04060c" stroke-width="12" stroke-linejoin="round"/>'
    b += f'<path d="M{CX - R} {CY} A{R} {R} 0 0 1 {CX + R} {CY}" fill="none" stroke="url(#arc5)" stroke-width="64"/>'
    b += f'<path d="M{CX - R} {CY} A{R} {R} 0 0 1 {CX + R} {CY}" fill="none" stroke="#000" stroke-width="64" opacity=".35"/>'
    for t in range(-80, 56, 10):
        (ax, ay), (bx, by) = P(t, R - 52), P(t, R - 82)
        b += f'<path d="M{ax:.0f} {ay:.0f} L{bx:.0f} {by:.0f}" stroke="#c8d4e8" stroke-width="5" stroke-linecap="round" opacity=".8"/>'
    # living window 28..42: glowing wedge
    (a0x, a0y), (a1x, a1y) = P(28, R + 46), P(42, R + 46)
    (b0x, b0y), (b1x, b1y) = P(28, R - 110), P(42, R - 110)
    b += f'<ellipse cx="{P(35, R)[0]:.0f}" cy="{P(35, R)[1]:.0f}" rx="200" ry="200" fill="url(#h5)" opacity=".95"/>'
    wedge = f'M{b0x:.0f} {b0y:.0f} L{a0x:.0f} {a0y:.0f} A{R + 46} {R + 46} 0 0 1 {a1x:.0f} {a1y:.0f} L{b1x:.0f} {b1y:.0f} A{R - 110} {R - 110} 0 0 0 {b0x:.0f} {b0y:.0f}Z'
    b += f'<path d="{wedge}" fill="#7fff9a" opacity=".55" filter="url(#b12)"/><path d="{wedge}" fill="#9affb0" stroke="#f0fff4" stroke-width="7" stroke-linejoin="round" opacity=".92"/>'
    for t in (-89, 56, 28, 42):
        x, y = P(t, R + 96 if t in (28, 42) else R - 140)
        lab = f'{t}°'.replace('-', '−')
        b += text(f'{x:.0f}', f'{y + 18:.0f}', 50 if t in (28, 42) else 44, lab, '#f4fff6' if t in (28, 42) else '#c8d4e8')
    b += text(CX, CY - 160, 64, '37°', '#fff3c0')
    # needle at 37
    nx, ny = P(37, R - 60)
    b += f'<path d="M{CX} {CY} L{nx:.0f} {ny:.0f}" stroke="#04060c" stroke-width="26" stroke-linecap="round"/><path d="M{CX} {CY} L{nx:.0f} {ny:.0f}" stroke="#ff5a3a" stroke-width="13" stroke-linecap="round"/>'
    b += f'<circle cx="{CX}" cy="{CY}" r="42" fill="#c8d0dc" stroke="#04060c" stroke-width="10"/><circle cx="{CX - 10}" cy="{CY - 10}" r="12" fill="#fff" opacity=".8"/>'
    for sx, sy, ss in (P(35, R + 130) + (30,), (190, 250, 18), (880, 200, 20), (CX, 180, 16)):
        b += spark(sx, sy, ss, col='#fff8d8')
    b += fireflies(26, 100, 1840, col='#bfe4ff', core='#ffffff', seed=51)[:]
    b += fireflies(22, 100, 1840, col='#ffc890', core='#fff4e0', seed=52)
    b += darkband(860, 1240, .55)
    # lower: frog in goggles with a small thermometer, pointing up
    goggles = ('<path d="M-38 -66 L-26 -66 M38 -66 L50 -66 M6 -66 L6 -66" stroke="#5a6aa8" stroke-width="5"/>'
               '<circle cx="-10" cy="-66" r="17" fill="#bfe6ff" fill-opacity=".15" stroke="#5a6aa8" stroke-width="5"/><circle cx="22" cy="-66" r="17" fill="#bfe6ff" fill-opacity=".15" stroke="#5a6aa8" stroke-width="5"/>')
    therm = ('<g transform="translate(70 -58) rotate(14)"><rect x="-6" y="-44" width="12" height="52" rx="6" fill="#f4f8ff" stroke-width="3"/>'
             '<rect x="-2.5" y="-24" width="5" height="30" fill="#ff4a2a" stroke="none"/><circle cx="0" cy="12" r="10" fill="#ff4a2a" stroke-width="3"/></g>')
    b += '<ellipse cx="280" cy="1640" rx="240" ry="200" fill="#ffd040" opacity=".14" filter="url(#b24)"/>'
    b += frog(280, 1770, 3.3, look=(3, -5), mouth='O', shadow=True, mid=goggles, front=therm, armR='M38 -22 q24 -16 30 -48', armL='M-34 -22 q-14 6 -16 22')
    b += f'<rect width="{W}" height="{H}" fill="url(#vig)"/>'
    save(5, '#0a0610', d, b, [('ONLY ' + Y('14'), 210, 'w'), ('DEGREES', 160, 'w')], '#05060c', 880)


if __name__ == '__main__':
    for n in map(int, sys.argv[1:] or '12345'):
        globals()[f'make_{n}'](); print('short', n, 'ok')
