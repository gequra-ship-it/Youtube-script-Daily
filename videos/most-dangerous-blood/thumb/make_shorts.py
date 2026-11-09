# VERTICAL shorts thumbnails (guideline 16-9 B: dark scene + one glowing concrete subject + centred hook) for most-dangerous-blood-short1..5.
# Run: python3 videos/most-dangerous-blood/thumb/make_shorts.py   then  SLUG=most-dangerous-blood-shortN python3 tools/thumb_shot.py
# short1 MOLECULAR / HANDCUFFS   two red cells with antigen flags locked together by glowing handcuffs, antibodies around (sh1: "Antibodies lock onto
#                                the foreign flags like molecular handcuffs"); frog = coastal patrol with cap + flashlight
# short2 TYPE O / REJECTS / TYPE O  two type-O bags clash, antibodies + red sparks between them (sh2: "How can a type O patient reject type O blood?");
#                                frog in scrub cap, sweating
# short3 50+ / RH ANTIGENS       microscope field: one red cell bristling with many different antigen flags, one big golden D flag (sh3: "a large family
#                                of more than fifty antigens"; D = "the strongest immune trigger"); frog with magnifier
# short4 GOLDEN / BLOOD          golden vial in frost glow above the night Earth, shipping arc (sh4: "known as golden blood", "frozen blood has been shipped
#                                from one country to another"); frog with a cool box
# short5 NO MATCH / ON THE SHELF empty glowing blood-bank fridge on a lonely night road (sh5: "a serious accident on a lonely road. The local hospital
#                                cannot pull a matching unit from its shelves"); frog paramedic with an empty bag
import os, sys, math, random
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from make import *
from thumb_lib import vpage, vsvg, fireflies, halo, darkband, spark, lin, rad

W, H = 1080, 1920
VD = os.path.dirname(os.path.dirname(HERE))


def vvig(id, a=.7):
    return rad(id, 540, 900, 1250, [(0, '#000', 0), (.55, '#000', 0), (1, '#000', a)])


def stars_v(n, y0, y1, col='#eaf4ff'):
    return ''.join(f'<circle cx="{random.randint(0, W)}" cy="{random.randint(y0, y1)}" r="{random.choice([1.2, 1.8, 2.6])}" fill="{col}" opacity="{random.uniform(.3, .9):.2f}"/>' for _ in range(n))


def cap(c='#24365a'):
    return (f'<path d="M-26 -80 q2 -34 34 -36 q34 0 38 34 q-36 -8 -72 2z" fill="{c}" stroke-width="3.2"/>'
            f'<path d="M-30 -78 q40 -10 80 0 q14 2 22 10 q-50 -4 -102 -10z" fill="#1a2640" stroke-width="3"/>'
            '<path d="M2 -104 l6 -6 l6 6 l-6 6z" fill="#f2d27a" stroke-width="2"/>')


def write(n, html):
    open(f'{VD}/most-dangerous-blood-short{n}/thumb/A.html', 'w').write(html)


# ---------------- short1: molecular handcuffs ----------------
def short1():
    random.seed(101)
    d = FILTERS + CELL_DEFS + lin('s1bg', [(0, '#0a0614'), (.5, '#1c0a1e'), (1, '#07040c')])
    d += halo('s1h', 540, 520, 520, inner='#fff6d6', outer='#7fd8ff') + vvig('s1v') + lin('s1metal', [(0, '#ffffff'), (.5, '#b8c8d8'), (1, '#6a7a8a')])
    d += rad('s1beam', 760, 1640, 700, [(0, '#fff6c8', .5), (1, '#fff6c8', 0)])
    b = f'<rect width="{W}" height="{H}" fill="url(#s1bg)"/>'
    # far drifting cells (the river)
    for _ in range(26):
        b += rbc(random.randint(-40, 1120), random.randint(120, 1860), random.randint(26, 60), .5, random.randint(-40, 40), 'x', random.uniform(.35, .7))
    b += f'<ellipse cx="540" cy="520" rx="560" ry="520" fill="url(#s1h)"/>'
    # two cells with flags
    for cx, cy, rot, cols in ((290, 560, -18, ('#7fd0e6', '#7fd0e6', '#7fd0e6')), (800, 520, 16, ('#f2d27a', '#f2d27a', '#f2d27a'))):
        b += rbc(cx, cy, 220, .52, rot, 'r', sw=6, hl=.7)
        for k, c in enumerate(cols):
            fx = cx + (k - 1) * 110; fy = cy - 40 + (k - 1) * 110 * math.tan(math.radians(rot)) - (30 if k == 1 else 0)
            b += flag(fx, fy, 120, c, sw=5)
    # handcuffs: ring around the inner flag poles + chain
    for rx_, ry_ in ((400, 420), (690, 400)):
        b += f'<ellipse cx="{rx_}" cy="{ry_}" rx="58" ry="40" fill="none" stroke="#0a0a14" stroke-width="28"/><ellipse cx="{rx_}" cy="{ry_}" rx="58" ry="40" fill="none" stroke="url(#s1metal)" stroke-width="16"/>'
        b += f'<path d="M{rx_ - 40} {ry_ - 30} a50 34 0 0 1 60 -8" fill="none" stroke="#fff" stroke-width="5" opacity=".9"/>'
    for k in range(5):
        x = 458 + k * 44; y = 410 - math.sin(k / 4 * math.pi) * 22
        b += f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="22" ry="13" fill="none" stroke="#0a0a14" stroke-width="14"/><ellipse cx="{x:.0f}" cy="{y:.0f}" rx="22" ry="13" fill="none" stroke="url(#s1metal)" stroke-width="7"/>'
    b += '<ellipse cx="545" cy="400" rx="200" ry="90" fill="#bff0ff" opacity=".25" filter="url(#b24)"/>'
    # antibodies swarming the foreign (right) cell
    for ax, ay, rot in ((930, 360, 30), (1000, 520, 80), (640, 270, -20), (880, 700, 160), (700, 700, 200), (980, 660, 120)):
        b += antibody(ax, ay, 2.0, rot)
    for sx, sy, ss in ((540, 300, 34), (150, 380, 22), (960, 260, 26), (420, 760, 20), (1010, 820, 18)):
        b += spark(sx, sy, ss, col='#fffbe0')
    b += fireflies(40, 200, 1850, col='#ffd6e0', core='#fff0f4')
    b += darkband(860, 1240, .5)
    # frog patrol with flashlight beam (bottom right)
    b += '<path d="M690 1560 L120 1360 L180 1840Z" fill="url(#s1beam)" opacity=".55"/>'
    torch = '<g transform="translate(-58 -40) rotate(200)"><rect x="-8" y="-28" width="16" height="34" rx="4" fill="#3a3a44" stroke-width="2.6"/><rect x="-12" y="-34" width="24" height="10" rx="3" fill="#d8d8e0" stroke-width="2.6"/></g>'
    b += frog(800, 1700, 3.4, mouth='o', look=(-4, -3), la='q-16 -4 -24 -16', ra='q14 6 16 22', head=cap(), front=torch)
    b += f'<rect width="{W}" height="{H}" fill="url(#s1v)"/>'
    write(1, vpage('#0a0614', vsvg(d, b), [('MOLECULAR', 148, 'w'), ('HANDCUFFS', 162, 'y')], outline='#06040c', top=920))


# ---------------- short2: O rejects O ----------------
def short2():
    random.seed(202)
    d = FILTERS + CELL_DEFS + lin('s2bg', [(0, '#040c14'), (.5, '#0c1c26'), (1, '#04080c')])
    d += halo('s2h', 540, 520, 480, inner='#fff2c8', outer='#ff5a4a') + vvig('s2v')
    d += lin('s2liq', [(0, '#e8323e'), (.5, '#a8121e'), (1, '#5e0610')])
    b = f'<rect width="{W}" height="{H}" fill="url(#s2bg)"/>'
    for _ in range(18):
        b += rbc(random.randint(-40, 1120), random.randint(1260, 1880), random.randint(26, 50), .5, random.randint(-40, 40), 'x', random.uniform(.3, .6))
    b += f'<ellipse cx="540" cy="520" rx="520" ry="480" fill="url(#s2h)"/>'
    b += f'<g transform="rotate(-14 260 460)">{bloodbag("s2a", 260, 210, 300, 440, "url(#s2liq)", level=.15, tag="O")}</g>'
    b += f'<g transform="rotate(14 820 460)">{bloodbag("s2b", 820, 210, 300, 440, "url(#s2liq)", level=.15, tag="O")}</g>'
    # clash burst between the bags
    b += '<ellipse cx="540" cy="470" rx="120" ry="160" fill="#ffd0a0" opacity=".6" filter="url(#b24)"/>'
    bolt = 'M560 260 L500 400 L566 420 L494 560 L600 400 L536 382 L590 260Z'
    b += f'<path d="{bolt}" fill="#fff4d0" stroke="#3a0a06" stroke-width="7" stroke-linejoin="round"/>'
    for ax, ay, rot in ((430, 330, 70), (440, 610, 110), (650, 330, -70), (650, 610, -110), (540, 700, 180), (540, 220, 0)):
        b += antibody(ax, ay, 1.8, rot)
    for k in range(10):
        a = math.radians(k * 36 + 10); r0, r1 = 150, 210
        b += f'<path d="M{540 + r0 * math.cos(a):.0f} {470 + r0 * math.sin(a) * 1.2:.0f} L{540 + r1 * math.cos(a):.0f} {470 + r1 * math.sin(a) * 1.2:.0f}" stroke="#ffe0b0" stroke-width="6" stroke-linecap="round" opacity=".6"/>'
    for sx, sy, ss in ((540, 180, 26), (380, 760, 22), (720, 760, 22), (90, 220, 18), (1000, 240, 18)):
        b += spark(sx, sy, ss, col='#fffbe0')
    b += fireflies(36, 200, 1850, col='#ffcfb0', core='#fff4e8')
    b += darkband(840, 1300, .55)
    b += frog(270, 1720, 3.4, mouth='o', look=(4, -3), la='q-10 -10 -4 -30', ra='q20 -8 26 -30', head=scrubcap(), extra=goggles(), front=sweat(-36, -96))
    b += f'<rect width="{W}" height="{H}" fill="url(#s2v)"/>'
    write(2, vpage('#040c14', vsvg(d, b), [('TYPE O', 140, 'w'), ('REJECTS', 176, 'y'), ('TYPE O', 140, 'w')], outline='#03080c', top=860))


# ---------------- short3: the Rh family (50+ antigens) ----------------
def short3():
    random.seed(303)
    d = FILTERS + CELL_DEFS + lin('s3bg', [(0, '#06060f'), (1, '#0a0614')])
    d += rad('s3field', 540, 540, 500, [(0, '#3a2a5a', .9), (.8, '#2a1a44', .6), (1, '#1a0e2a', 0)])
    d += halo('s3h', 540, 520, 440, inner='#ffe9f0', outer='#ff7aa0') + vvig('s3v') + rad('s3gold', 760, 270, 160, [(0, '#fff3a8', .95), (1, '#ffd760', 0)])
    b = f'<rect width="{W}" height="{H}" fill="url(#s3bg)"/>'
    b += '<circle cx="540" cy="540" r="500" fill="url(#s3field)"/><circle cx="540" cy="540" r="470" fill="none" stroke="#9a8ac8" stroke-width="4" opacity=".35"/>'
    b += f'<ellipse cx="540" cy="540" rx="440" ry="420" fill="url(#s3h)"/>'
    cx, cy, r, tilt = 540, 580, 300, .58
    b += rbc(cx, cy, r, tilt, -6, 'r', sw=7, hl=.75)
    cols = ['#7fd0e6', '#9be08a', '#e66a9a', '#c79bff', '#ffa05a', '#7fe0c8', '#f08080', '#a0c0ff']
    # antigens: little flags / knobs standing all over the rim
    pts = []
    for k in range(22):
        a = math.radians(-180 + k * 360 / 22)
        pts.append((cx + r * .96 * math.cos(a), cy + r * tilt * .96 * math.sin(a) - 4))
    for k, (x, y) in enumerate(sorted(pts, key=lambda p: p[1])):
        c = cols[k % len(cols)]
        if k % 3 == 0:
            b += f'<path d="M{x:.0f} {y:.0f} l0 -50" stroke="#2a0a0e" stroke-width="8" stroke-linecap="round"/><circle cx="{x:.0f}" cy="{y - 58:.0f}" r="19" fill="{c}" stroke="#2a0a0e" stroke-width="4"/>'
        elif k % 3 == 1:
            b += flag(round(x), round(y), 96, c, sw=5)
        else:
            b += antibody(x, y, 1.6, 0, col=c, ink='#2a0a0e')
    for k in range(12):   # a few on the top surface too
        x = cx + random.uniform(-.6, .6) * r; y = cy + random.uniform(-.45, .35) * r * tilt
        b += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="14" fill="{cols[k % 8]}" stroke="#2a0a0e" stroke-width="4"/>'
    # the big golden D flag
    b += '<ellipse cx="760" cy="270" rx="160" ry="150" fill="url(#s3gold)"/>'
    b += flag(700, 470, 300, '#f2d27a', w=200, sw=9)
    for sx, sy, ss in ((900, 180, 30), (600, 170, 20), (880, 380, 18), (170, 330, 22), (950, 760, 18)):
        b += spark(sx, sy, ss, col='#fffbe0')
    b += fireflies(34, 200, 1850, col='#e0c8ff', core='#f8f0ff')
    b += darkband(860, 1260, .55)
    lens = ('<g transform="translate(64 -40)"><path d="M-8 6 L-30 34" stroke-width="12"/><path d="M-8 6 L-30 34" stroke="#8a5a2e" stroke-width="7"/>'
            '<circle cx="8" cy="-14" r="24" fill="#bfe8ff" fill-opacity=".45" stroke-width="7"/><circle cx="8" cy="-14" r="24" fill="none" stroke="#d8d8e0" stroke-width="3"/></g>')
    b += frog(800, 1720, 3.4, mouth='o', look=(-4, -3), la='q-14 6 -16 22', ra='q12 -6 16 -22', front=lens, head=fedora('#6a5a8a', '#2a2040'))
    b += f'<rect width="{W}" height="{H}" fill="url(#s3v)"/>'
    write(3, vpage('#06060f', vsvg(d, b), [('50+', 250, 'y'), ('RH ANTIGENS', 124, 'w')], outline='#06040c', top=880))


# ---------------- short4: golden blood vial above the night Earth ----------------
def short4():
    random.seed(404)
    d = FILTERS + CELL_DEFS + lin('s4bg', [(0, '#03050e'), (1, '#0a1020')])
    d += halo('s4h', 540, 470, 520, inner='#fff6d0', outer='#ffc94a') + vvig('s4v')
    d += lin('s4gold', [(0, '#fff6c8'), (.3, '#ffd760'), (.7, '#e7a12a'), (1, '#9a5a10')], x2=1, y2=1)
    d += lin('s4earth', [(0, '#123a5a'), (.25, '#0a1e34'), (1, '#03070e')])
    b = f'<rect width="{W}" height="{H}" fill="url(#s4bg)"/>' + stars_v(120, 0, 800)
    # Earth (night side) with atmosphere rim
    b += '<ellipse cx="540" cy="2500" rx="1700" ry="1720" fill="url(#s4earth)"/>'
    b += '<ellipse cx="540" cy="2500" rx="1700" ry="1720" fill="none" stroke="#7fd8ff" stroke-width="10" opacity=".7" filter="url(#b6)"/>'
    b += '<ellipse cx="540" cy="2500" rx="1700" ry="1720" fill="none" stroke="#cff4ff" stroke-width="3" opacity=".8"/>'
    for _ in range(160):   # city lights
        x = random.randint(0, W); y = random.randint(820, 1880)
        b += f'<circle cx="{x}" cy="{y}" r="{random.choice([1.6, 2.2, 3])}" fill="#ffd98a" opacity="{random.uniform(.3, .9):.2f}"/>'
    # shipping arc country to country
    b += '<path d="M90 1500 Q540 560 990 1460" fill="none" stroke="#9fe8ff" stroke-width="6" stroke-dasharray="18 16" opacity=".55"/>'
    for px, py in ((90, 1500), (990, 1460)):
        b += f'<circle cx="{px}" cy="{py}" r="16" fill="#9fe8ff" opacity=".9"/><circle cx="{px}" cy="{py}" r="40" fill="#9fe8ff" opacity=".25" filter="url(#b10)"/>'
    b += f'<ellipse cx="540" cy="470" rx="540" ry="520" fill="url(#s4h)"/>'
    # frost mist ring around the vial (frozen storage)
    for k in range(9):
        a = math.radians(k * 40); b += f'<ellipse cx="{540 + 220 * math.cos(a):.0f}" cy="{720 + 40 * math.sin(a):.0f}" rx="120" ry="34" fill="#e8f8ff" opacity=".22" filter="url(#b16)"/>'
    b += '<g transform="rotate(-10 540 760)">' + vial('s4vial', 540, 760, 200, 520, 'url(#s4gold)', cap='#e8eef4', ink='#3a2206', level=.15, sw=8) + '</g>'
    b += '<ellipse cx="540" cy="470" rx="140" ry="300" fill="#ffd760" opacity=".2" filter="url(#b24)" transform="rotate(-10 540 760)"/>'
    for cx, cy, r, rot in ((250, 330, 40, 20), (850, 420, 34, -25), (800, 220, 26, 10), (290, 640, 26, -10)):
        b += rbc(cx, cy, r, .5, rot, 'g', .95)
    for sx, sy, ss in ((360, 200, 34), (760, 330, 28), (720, 640, 22), (330, 500, 22), (560, 120, 18), (920, 600, 18)):
        b += spark(sx, sy, ss, col='#fffbe0')
    b += fireflies(36, 200, 1850, col='#fff3a8', core='#fffbd0')
    b += darkband(860, 1250, .5)
    box = ('<g transform="translate(0 -6)"><rect x="-56" y="-46" width="112" height="70" rx="10" fill="#e8f2f8" stroke-width="3.4"/>'
           '<rect x="-56" y="-46" width="112" height="16" rx="6" fill="#4aa0c8" stroke-width="3"/><path d="M-20 -6 l40 0 M0 -26 l0 40 M-14 -20 l28 28 M14 -20 l-28 28" stroke="#9fd8ec" stroke-width="3"/></g>')
    b += frog(780, 1720, 3.4, mouth='o', look=(-4, -3), la='q-6 14 4 22', ra='q4 14 -6 22', front=box, head=beanie_s())
    b += f'<rect width="{W}" height="{H}" fill="url(#s4v)"/>'
    write(4, vpage('#03050e', vsvg(d, b), [('GOLDEN', 210, 'y'), ('BLOOD', 190, 'w')], outline='#06040c', top=860))


def beanie_s(c='#3f6fb0'):
    return (f'<path d="M-24 -78 q4 -32 34 -34 q32 0 36 32 q-34 -8 -70 2z" fill="{c}" stroke-width="3.2"/>'
            '<path d="M-26 -76 q36 -12 74 -2 l-1 9 q-36 -10 -72 2z" fill="#f1e3c8" stroke-width="3"/><circle cx="10" cy="-114" r="8" fill="#f1e3c8" stroke-width="3"/>')


# ---------------- short5: empty blood-bank fridge on a lonely road ----------------
def short5():
    random.seed(505)
    d = FILTERS + CELL_DEFS + lin('s5sky', [(0, '#02040c'), (.7, '#0c1830'), (1, '#1a2a44')])
    d += halo('s5h', 540, 500, 540, inner='#f4fbff', outer='#7fd8ff') + vvig('s5v')
    d += lin('s5in', [(0, '#ffffff'), (1, '#bfe6f4')]) + lin('s5road', [(0, '#1a1e26'), (1, '#05060a')])
    d += rad('s5spill', 540, 820, 520, [(0, '#cff0ff', .55), (1, '#cff0ff', 0)])
    HZ = 700
    b = f'<rect width="{W}" height="{H}" fill="url(#s5sky)"/>' + stars_v(140, 0, HZ - 40)
    b += f'<path d="M0 {HZ} L{W} {HZ} L{W} {H} L0 {H}Z" fill="#06080c"/>'
    b += f'<path d="M0 {HZ - 10} q120 -50 240 -20 q140 -60 280 -10 q160 -40 300 -6 q120 -30 260 6 L{W} {HZ} L0 {HZ}z" fill="#0a1220"/>'
    # road to the horizon
    b += f'<path d="M500 {HZ} L580 {HZ} L1160 {H} L-80 {H}Z" fill="url(#s5road)"/>'
    for k in range(9):
        t0 = (k / 9) ** 1.8; t1 = ((k + .45) / 9) ** 1.8
        y0 = HZ + (H - HZ) * t0; y1 = HZ + (H - HZ) * t1; w0 = 3 + 22 * t0; w1 = 3 + 22 * t1
        b += f'<path d="M{540 - w0 / 2:.0f} {y0:.0f} L{540 + w0 / 2:.0f} {y0:.0f} L{540 + w1 / 2:.0f} {y1:.0f} L{540 - w1 / 2:.0f} {y1:.0f}Z" fill="#f2d27a" opacity=".75"/>'
    b += f'<ellipse cx="540" cy="500" rx="540" ry="520" fill="url(#s5h)"/>'
    b += '<ellipse cx="540" cy="830" rx="520" ry="160" fill="url(#s5spill)"/>'
    # fridge with the door swung open to the right
    fx, fy, fw, fh = 330, 230, 380, 560
    b += f'<ellipse cx="540" cy="{fy + fh + 10}" rx="260" ry="26" fill="#000" opacity=".6" filter="url(#b6)"/>'
    b += f'<rect x="{fx - 22}" y="{fy - 22}" width="{fw + 44}" height="{fh + 44}" rx="24" fill="#d8e2ea" stroke="#0a0e14" stroke-width="8"/>'
    b += f'<rect x="{fx}" y="{fy}" width="{fw}" height="{fh}" rx="10" fill="url(#s5in)" stroke="#0a0e14" stroke-width="6"/>'
    for k in range(1, 5):
        y = fy + k * fh / 5
        b += f'<path d="M{fx + 8} {y:.0f} L{fx + fw - 8} {y:.0f}" stroke="#7a8a96" stroke-width="7"/>'
        b += ''.join(f'<path d="M{fx + 20 + j * 30} {y - 2:.0f} l0 4" stroke="#5a6a76" stroke-width="3"/>' for j in range(12))
    # empty hooks hanging from the top shelf
    for hx in (420, 520, 620):
        b += f'<path d="M{hx} {fy + 6} l0 30 q0 14 -12 14" fill="none" stroke="#5a6a76" stroke-width="5" stroke-linecap="round"/>'
    # one leftover empty label tag
    b += f'<rect x="560" y="{fy + 3 * fh / 5 - 46:.0f}" width="70" height="40" rx="6" fill="#fff" stroke="#0a0e14" stroke-width="4" transform="rotate(-8 595 {fy + 3 * fh / 5 - 26:.0f})"/>'
    b += f'<path d="M{fx + fw + 22} {fy - 22} L{fx + fw + 190} {fy + 20} L{fx + fw + 190} {fy + fh + 2} L{fx + fw + 22} {fy + fh + 22}Z" fill="#b8c6d0" stroke="#0a0e14" stroke-width="8" stroke-linejoin="round"/>'
    b += f'<path d="M{fx + fw + 50} {fy + 20} L{fx + fw + 166} {fy + 50} L{fx + fw + 166} {fy + fh - 20} L{fx + fw + 50} {fy + fh - 10}Z" fill="#8a9aa6" stroke="#0a0e14" stroke-width="5"/>'
    # red cross on the fridge top
    b += f'<rect x="{fx + fw / 2 - 60:.0f}" y="{fy - 78}" width="120" height="44" rx="10" fill="#e8eef2" stroke="#0a0e14" stroke-width="5"/><path d="M{fx + fw / 2:.0f} {fy - 70} l0 28 M{fx + fw / 2 - 14:.0f} {fy - 56} l28 0" stroke="#d8303a" stroke-width="9"/>'
    for sx, sy, ss in ((180, 260, 26), (930, 210, 22), (900, 620, 18), (150, 640, 18)):
        b += spark(sx, sy, ss, col='#eaf8ff')
    b += fireflies(30, 200, 1850, col='#cfeeff', core='#f4fbff')
    b += darkband(860, 1260, .55)
    empty = ('<g transform="translate(-66 -40) rotate(-12)"><path d="M-22 -36 L22 -36 Q28 -36 28 -28 L28 10 Q28 20 18 20 L-18 20 Q-28 20 -28 10 L-28 -28 Q-28 -36 -22 -36Z" '
             'fill="#e8eef2" fill-opacity=".7" stroke-width="3.2"/><path d="M-20 12 q20 -6 40 0" fill="none" stroke="#c8303a" stroke-width="3"/>'
             '<rect x="-14" y="-20" width="28" height="18" rx="3" fill="#fff" stroke-width="2"/></g>')
    vest = '<path d="M-30 -30 q30 10 64 0 l4 24 q-34 10 -70 0z" fill="#f08a2a" stroke-width="3"/><path d="M-30 -18 q34 8 70 0" stroke="#f4f4c8" stroke-width="4" fill="none"/>'
    b += frog(300, 1720, 3.4, mouth='o', look=(4, -3), la='q-16 -4 -24 -16', ra='q14 6 16 22', extra=vest, front=empty, head=cap('#c8303a'))
    b += f'<rect width="{W}" height="{H}" fill="url(#s5v)"/>'
    write(5, vpage('#02040c', vsvg(d, b), [('NO MATCH', 176, 'y'), ('ON THE SHELF', 124, 'w')], outline='#04060c', top=900))


if __name__ == '__main__':
    for f in (short1, short2, short3, short4, short5):
        f()
    print('ok')
