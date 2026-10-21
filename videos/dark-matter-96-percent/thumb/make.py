import sys, os, math, random
TOOLS = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', 'tools')
sys.path.insert(0, TOOLS)
from thumb_lib import *
os.chdir(os.path.dirname(os.path.abspath(__file__)))
# dark-matter-96-percent thumbnails (2026-10-21, Opus thumbnail agent, brief tools/briefs/thumb_art.md + guideline 16-6).
# A = homage (Hokusai, "The Great Wave off Kanagawa", public domain; mirrored): a huge translucent indigo wave of the unseen ocean,
#     its claws of foam made of stars and tiny galaxies, a bright spiral galaxy where Mt Fuji stands (S38: "tiny specks of bright foam
#     floating on top of a vast, unseen ocean").  Text: STARS ARE JUST FOAM.
# B = intuitive: a cosmic iceberg - a small sunlit tip above the waterline, a vast translucent blue-indigo hidden mass with a faint web
#     inside, a tiny submarine shining a light on it (S33/S34: about five percent ordinary matter, the rest dark).  Text: WE SEE ONLY 5%.
# C = intuitive: a book of 100 pages with only 5 readable - one glowing gold page, the others translucent indigo "invisible ink" pages
#     fluttering up, in a dim library (S35 "The Invisible Ink").  Text: WHAT'S IN THE OTHER 95%?
# Dark matter is only ever drawn as translucent blue-indigo haze; dark energy (A, B sky) as a faint cool teal outward push.
FR = 'x="-60%" y="-60%" width="220%" height="220%"'
FX = (f'<filter id="bl" {FR}><feGaussianBlur stdDeviation="8"/></filter><filter id="bl2" {FR}><feGaussianBlur stdDeviation="26"/></filter>'
      f'<filter id="bl3" {FR}><feGaussianBlur stdDeviation="3"/></filter><filter id="bl5" {FR}><feGaussianBlur stdDeviation="60"/></filter>'
      f'<filter id="bl1" {FR}><feGaussianBlur stdDeviation="1.4"/></filter>')


def cub(p0, p1, p2, p3, t):
    u = 1 - t
    return (u ** 3 * p0[0] + 3 * u * u * t * p1[0] + 3 * u * t * t * p2[0] + t ** 3 * p3[0],
            u ** 3 * p0[1] + 3 * u * u * t * p1[1] + 3 * u * t * t * p2[1] + t ** 3 * p3[1])


def sample(segs, n):
    """segs: list of (p0,p1,p2,p3); returns n points per seg with unit normals (left of travel direction)"""
    pts = []
    for s in segs:
        for k in range(n):
            t = k / n
            a = cub(*s, t); b = cub(*s, min(1, t + .01))
            dx, dy = b[0] - a[0], b[1] - a[1]; L = math.hypot(dx, dy) or 1
            pts.append((a[0], a[1], dy / L, -dx / L))
    return pts


def mini_galaxy(x, y, s, rot, col='#fff1c8', op=1):
    o = f'<g transform="translate({x:.0f} {y:.0f}) rotate({rot:.0f})" opacity="{op:.2f}">'
    o += f'<ellipse rx="{s * 2.4:.1f}" ry="{s * .8:.1f}" fill="{col}" opacity=".35" filter="url(#bl3)"/>'
    o += f'<path d="M{-s * 2:.1f} 0 Q{-s:.1f} {-s * .9:.1f} 0 0 Q{s:.1f} {s * .9:.1f} {s * 2:.1f} 0" stroke="{col}" stroke-width="{max(1, s * .35):.1f}" fill="none" opacity=".8"/>'
    o += f'<circle r="{s * .45:.1f}" fill="#fff"/></g>'
    return o


def spiral_galaxy(cx, cy, R, tilt, squash, n, core='#fff3d0', arm='#ffd98a', arm2='#9fc4ff'):
    o = f'<g transform="translate({cx} {cy}) rotate({tilt}) scale(1 {squash})">'
    o += f'<circle r="{R * 1.15:.0f}" fill="{arm}" opacity=".18" filter="url(#bl2)"/>'
    for k in range(n):
        arm_i = k % 2; t = random.random() ** .7
        ang = arm_i * math.pi + t * 3.6 + random.gauss(0, .22)
        r = t * R + random.gauss(0, R * .03)
        x, y = r * math.cos(ang), r * math.sin(ang)
        c = random.choice([arm, arm, '#ffffff', arm2])
        o += f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{random.choice([1.2, 1.8, 2.6]) * (1.4 - t * .5):.1f}" fill="{c}" opacity="{random.uniform(.35, .95):.2f}"/>'
    o += f'<circle r="{R * .32:.0f}" fill="{core}" opacity=".85" filter="url(#bl)"/><circle r="{R * .12:.0f}" fill="#fff"/></g>'
    return o


def W(name, d, b, lines, outline, top=40, bg='#03040c'):
    open(name, 'w', encoding='utf-8').write(page(bg, svg(FX + d, b), lines, outline, top=top))


# ======================= A: STARS ARE JUST FOAM  (homage: Hokusai, The Great Wave off Kanagawa, mirrored) =======================
random.seed(11)
d = lin('skyA', [(0, '#05061a'), (.55, '#0c1640'), (.8, '#173064'), (1, '#1d3a6a')])
d += lin('wave', [(0, '#5d86ff'), (.25, '#2f4fc8'), (.6, '#16237a'), (1, '#080c34')], x2=.3, y2=1)
d += lin('seaA', [(0, '#10204e'), (1, '#03061a')])
d += rad('fuji', 560, 790, 520, [(0, '#ffe2a0', .55), (.3, '#ffb35a', .18), (1, '#ff9a3a', 0)])
d += rad('teal', 1500, 600, 1100, [(0, '#3fe0d0', .0), (.6, '#3fe0d0', .07), (1, '#3fe0d0', 0)])
HZ = 840
b = '<rect width="1920" height="1080" fill="url(#skyA)"/><rect width="1920" height="1080" fill="url(#teal)"/>'
b += stars(260, HZ, col='#e8f0ff', op=.55, sparks=0)
b += '<rect width="1920" height="1080" fill="url(#fuji)"/>'
# "Mt Fuji": the bright spiral galaxy on the horizon - our glowing island
b += spiral_galaxy(560, 770, 210, -8, .34, 900)
b += f'<rect x="0" y="{HZ}" width="1920" height="{1080 - HZ}" fill="url(#seaA)"/>'
b += f'<ellipse cx="560" cy="{HZ + 30}" rx="260" ry="26" fill="#ffd98a" opacity=".35" filter="url(#bl)"/>'
for k in range(14):   # glints of the galaxy on the sea
    y = HZ + 18 + k * 14; w = 220 - k * 10
    b += f'<rect x="{560 - w / 2 + random.uniform(-30, 30):.0f}" y="{y}" width="{w:.0f}" height="3" rx="1.5" fill="#ffe2a0" opacity="{.5 - k * .03:.2f}"/>'
for k in range(26):   # far ripples
    x = random.uniform(0, 1100); y = random.uniform(HZ + 10, 1060)
    b += f'<path d="M{x:.0f} {y:.0f} q30 -10 60 0 t60 0" stroke="#5d7ad8" stroke-width="2" fill="none" opacity="{random.uniform(.15, .35):.2f}"/>'
# the great wave: outline, mirrored (hollow faces left, lip curls to the left)
TIP = (950, 505)
FACE = 'M560 1080 C760 960 1060 860 1150 680 C1210 560 1170 440 1080 430 C1030 432 975 455 950 505'
OUT = [((950, 505), (935, 400), (1000, 280), (1120, 210)), ((1120, 210), (1250, 135), (1430, 120), (1560, 175)),
       ((1560, 175), (1700, 235), (1820, 360), (1920, 430))]
WP = FACE + ' C935 400 1000 280 1120 210 C1250 135 1430 120 1560 175 C1700 235 1820 360 1920 430 L1920 1080Z'
d += f'<clipPath id="wclip"><path d="{WP}"/></clipPath>'
b += f'<path d="{WP}" fill="#4a6cff" opacity=".55" filter="url(#bl2)"/>'
b += f'<path d="{WP}" fill="url(#wave)" opacity=".9"/>'
# inner bands following the crest (Hokusai's lined water: alternating light / dark bands), clipped to the wave
g = '<g clip-path="url(#wclip)">'
pts = sample(OUT, 40)
for k, off in enumerate(range(30, 620, 34)):
    q = [(x - nx * off, y - ny * off) for x, y, nx, ny in pts]
    dd = 'M' + ' L'.join(f'{x:.0f} {y:.0f}' for x, y in q)
    light = k % 2 == 0
    g += f'<path d="{dd}" stroke="{"#4f74f0" if light else "#0a1050"}" stroke-width="{16 if light else 12}" fill="none" opacity="{max(.12, (.55 if light else .45) - k * .025):.2f}"/>'
    if light:
        g += f'<path d="{dd}" stroke="#c9d7ff" stroke-width="3" fill="none" opacity="{max(.1, .45 - k * .025):.2f}" stroke-dasharray="{random.randint(90, 220)} {random.randint(20, 60)}"/>'
# white foam band hugging the crest
g += '<path d="M950 505 C935 400 1000 280 1120 210 C1250 135 1430 120 1560 175 C1700 235 1820 360 1920 430" stroke="#f1f5ff" stroke-width="44" fill="none" opacity=".95"/>'
g += '<path d="M950 505 C935 400 1000 280 1120 210 C1250 135 1430 120 1560 175 C1700 235 1820 360 1920 430" stroke="#1a2a8a" stroke-width="56" fill="none" opacity=".0"/>'
for x, y, nx, ny in sample(OUT, 50):
    g += f'<circle cx="{x - nx * 22:.0f}" cy="{y - ny * 22:.0f}" r="{random.uniform(3, 7):.1f}" fill="#1c2c94" opacity=".7"/>'
# faint web filaments and knots inside the dark water (dark matter haze)
for _ in range(30):
    x0, y0 = random.uniform(1200, 1900), random.uniform(380, 1040)
    x1, y1 = x0 + random.uniform(-160, 160), y0 + random.uniform(-120, 120)
    g += f'<path d="M{x0:.0f} {y0:.0f} Q{(x0 + x1) / 2 + random.uniform(-40, 40):.0f} {(y0 + y1) / 2 + random.uniform(-40, 40):.0f} {x1:.0f} {y1:.0f}" stroke="#8da2ff" stroke-width="3" fill="none" opacity=".22" filter="url(#bl1)"/>'
    g += f'<circle cx="{x0:.0f}" cy="{y0:.0f}" r="{random.uniform(5, 12):.0f}" fill="#9fb3ff" opacity=".25" filter="url(#bl3)"/>'
# hollow face: darker, with white streams running up into the curl
g += '<path d="M560 1080 C760 960 1060 860 1150 680 C1210 560 1170 440 1080 430 C1250 520 1330 800 1240 1080Z" fill="#040720" opacity=".55" filter="url(#bl5)"/>'
for k in range(7):
    o = 18 + k * 30
    g += (f'<path d="M{600 + o * 1.4:.0f} 1080 C{790 + o:.0f} {960 - o * .2:.0f} {1070 + o * .6:.0f} {860 - o * .3:.0f} {1150 + o * .5:.0f} {680 - o * .1:.0f} '
          f'C{1205 + o * .3:.0f} {560 - o * .1:.0f} {1170 + o * .2:.0f} {445 + o * .1:.0f} {1085 + o * .1:.0f} {440 + o * .15:.0f}" stroke="#b9cbff" stroke-width="{5 - k * .5:.1f}" '
          f'fill="none" opacity="{.5 - k * .05:.2f}" stroke-dasharray="{random.randint(60, 140)} {random.randint(20, 50)}"/>')
g += '</g>'
b += g
b += '<path d="M560 1080 C760 960 1060 860 1150 680 C1210 560 1170 440 1080 430 C1030 432 975 455 950 505" stroke="#e6eeff" stroke-width="6" fill="none" opacity=".8"/>'
# rim light along the crest
b += '<path d="M950 505 C935 400 1000 280 1120 210 C1250 135 1430 120 1560 175 C1700 235 1820 360 1920 430" stroke="#d8e4ff" stroke-width="18" fill="none" opacity=".5" filter="url(#bl)"/>'
# foam claws made of stars: big hooked fingers reaching out and curling down (Hokusai's claws)


def claw(x, y, a, L, sw):
    """one tapered, hooked foam finger from (x, y), start direction a, length L; curls down at the end (filled shape)"""
    n = 16; cen = []; px, py, ang = x, y, a
    for k in range(n + 1):
        t = k / n; cen.append((px, py, ang, sw * (1 - t) ** .8 + 1.5))
        ang -= 2.6 * t * t / n * 3     # curvature grows toward the tip
        px += L / n * math.cos(ang); py += L / n * math.sin(ang)
    lft = [(cx + w / 2 * math.sin(an), cy - w / 2 * math.cos(an)) for cx, cy, an, w in cen]
    rgt = [(cx - w / 2 * math.sin(an), cy + w / 2 * math.cos(an)) for cx, cy, an, w in cen]
    poly = lft + rgt[::-1]
    dd = 'M' + ' L'.join(f'{p:.0f} {q:.0f}' for p, q in poly) + 'Z'
    o = f'<path d="{dd}" fill="#2a40b8" transform="translate(3 5)" opacity=".8"/>'
    o += f'<path d="{dd}" fill="#f6f8ff"/>'
    ex, ey = cen[-1][0], cen[-1][1]
    o += f'<circle cx="{ex:.0f}" cy="{ey:.0f}" r="{sw * .45:.1f}" fill="#fff3c8"/><circle cx="{ex:.0f}" cy="{ey:.0f}" r="{sw * .9:.1f}" fill="#ffe2a0" opacity=".45" filter="url(#bl3)"/>'
    return o


cl = ''
cpts = sample([OUT[0], OUT[1]], 6)
for i, (x, y, nx, ny) in reversed(list(enumerate(cpts[:8]))):
    base = math.atan2(ny, nx) - .45
    big = 1.35 - i * .06
    for f in range(4):
        a = base + (f - 1.5) * .3 + random.uniform(-.06, .06)
        cl += claw(x - nx * 16, y - ny * 16, a, random.uniform(80, 130) * big, random.uniform(20, 26) * big)
b += cl
# foam dots on the crest body (stars riding the water)
for x, y, nx, ny in sample(OUT, 30):
    for _ in range(3):
        dd = random.uniform(30, 90)
        b += f'<circle cx="{x + nx * dd:.0f}" cy="{y + ny * dd:.0f}" r="{random.uniform(2, 5):.1f}" fill="#fff6dc" opacity="{random.uniform(.4, .95):.2f}"/>'
# spray: falling specks of stars and tiny galaxies off the lip and crest
for _ in range(170):
    x = random.uniform(820, 1650); y = random.uniform(60, 820)
    inside = (x > 1000 and y > 240 + (x - 1000) * .1) and not (x < 1180 and y > 440)
    if inside or (y < 520 and x < 900) or (x > 1250 and y > 230): continue
    if random.random() < .08:
        b += mini_galaxy(x, y, random.uniform(4, 7), random.uniform(-40, 40))
    else:
        r = random.choice([1.6, 2.4, 3.4, 4.6])
        b += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r}" fill="#fff4d6" opacity="{random.uniform(.5, 1):.2f}"/>'
        if r > 3: b += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r * 3:.0f}" fill="#ffe2a0" opacity=".3" filter="url(#bl3)"/>'
for (x, y, s) in [(1000, 160, 8), (1300, 90, 8), (1180, 120, 6), (1500, 110, 7), (900, 560, 6)]:
    b += mini_galaxy(x, y, s, random.uniform(-30, 30))
b += spark(1060, 180, 28) + spark(1400, 80, 20) + spark(895, 640, 16) + spark(1660, 160, 14)
# boats riding the face (tiny rowers for scale)


def boat(x, y, ang, L=230, n=7):
    o = f'<g transform="translate({x} {y}) rotate({ang})">'
    o += f'<path d="M{-L / 2} -6 Q0 22 {L / 2} -14 L{L / 2 - 10} -2 Q0 34 {-L / 2 + 6} 4Z" fill="#000" opacity=".35" filter="url(#bl3)"/>'
    o += f'<path d="M{-L / 2} -8 Q0 18 {L / 2} -18 L{L / 2 - 14} -4 Q0 30 {-L / 2 + 8} 4Z" fill="#c9b07a" stroke="#2a1d10" stroke-width="3"/>'
    o += f'<path d="M{-L / 2 + 10} -4 Q0 20 {L / 2 - 16} -12" stroke="#ffe7b0" stroke-width="2.5" fill="none" opacity=".8"/>'
    for k in range(n):
        px = -L / 2 + 30 + k * (L - 60) / (n - 1); py = 4 - 6 * math.sin(k / (n - 1) * math.pi)
        o += f'<path d="M{px - 7:.0f} {py:.0f} Q{px:.0f} {py - 26:.0f} {px + 7:.0f} {py:.0f}Z" fill="#141a33"/><circle cx="{px:.0f}" cy="{py - 22:.0f}" r="6" fill="#141a33"/>'
        o += f'<circle cx="{px + 2:.0f}" cy="{py - 23:.0f}" r="2.4" fill="#ffd98a" opacity=".6"/>'
    o += '</g>'
    return o


b += boat(890, 920, -26, 300, 8) + boat(330, 1000, 6, 200, 6)
# foreground small wave (left) with a little claw crest
b += '<path d="M0 1080 L0 960 C120 900 240 880 320 905 C380 925 400 965 370 975 C420 990 520 1030 640 1080Z" fill="#1a2c8a" opacity=".9"/>'
b += '<path d="M0 960 C120 900 240 880 320 905 C380 925 400 965 370 975" stroke="#dce6ff" stroke-width="7" fill="none" opacity=".75"/>'
for k in range(8):
    x = 120 + k * 32; y = 905 - 20 * math.sin(k / 7 * math.pi) + 5
    b += f'<circle cx="{x}" cy="{y - 6:.0f}" r="{random.uniform(5, 9):.0f}" fill="#f4f7ff" opacity=".9"/>'
# keep bottom-right calm
b += '<rect x="1540" y="840" width="460" height="300" fill="#02030f" opacity=".55" filter="url(#bl2)"/>'
W('A.html', d, b, [('STARS ARE', 142, 'w'), ('JUST', 142, 'w'), ('FOAM', 236, 'y')], '#03051a')

# ======================= B: WE SEE ONLY 5%  (intuitive: cosmic iceberg) =======================
random.seed(22)
WL = 470
d = lin('skyB', [(0, '#04051a'), (.7, '#0c1a46'), (1, '#1b3d6a')])
d += lin('seaB', [(0, '#0e2a5a'), (.35, '#071538'), (1, '#02040f')])
d += rad('sunB', 1760, 110, 700, [(0, '#fff3cf', .9), (.08, '#ffd98a', .55), (.35, '#ff9d4a', .12), (1, '#ff9d4a', 0)])
d += rad('haze', 1200, 760, 560, [(0, '#6a7dff', .55), (.55, '#3640c8', .4), (1, '#1c1f86', .2)])
d += rad('tealB', 960, 300, 1100, [(0, '#3fe0d0', 0), (.7, '#3fe0d0', .06), (1, '#3fe0d0', 0)])
d += lin('iceL', [(0, '#9fbbe8'), (1, '#3e5c9e')]) + lin('iceR', [(0, '#fffaf0'), (.6, '#ffe2a8'), (1, '#e8b870')])
b = '<rect width="1920" height="1080" fill="url(#skyB)"/><rect width="1920" height="1080" fill="url(#tealB)"/>'
b += stars(220, WL - 20, col='#e8f0ff', op=.55, sparks=0)
b += f'<rect width="1920" height="{WL}" fill="url(#sunB)"/>'
b += '<circle cx="1760" cy="110" r="26" fill="#fffaf0"/>' + spark(1760, 110, 90, '#fff6dc', .9)
# far horizon galaxies / bergs
b += mini_galaxy(300, 420, 9, -10, op=.7) + mini_galaxy(980, 380, 7, 20, op=.6)
# underwater
b += f'<rect x="0" y="{WL}" width="1920" height="{1080 - WL}" fill="url(#seaB)"/>'
for k in range(9):   # light rays from the surface
    x = 700 + k * 130 + random.uniform(-30, 30)
    b += f'<path d="M{x:.0f} {WL} L{x + 70:.0f} {WL} L{x - 160:.0f} 1080 L{x - 320:.0f} 1080Z" fill="#bcd6ff" opacity="{random.uniform(.03, .07):.2f}" filter="url(#bl)"/>'
# the hidden mass: translucent blue-indigo haze, much bigger than the tip
HIDP = [(1080, WL), (960, 520), (840, 560), (760, 640), (690, 700), (660, 790), (700, 880), (780, 950), (900, 1010), (1040, 1050),
        (1180, 1070), (1330, 1055), (1440, 1010), (1530, 940), (1600, 860), (1690, 790), (1740, 700), (1720, 610), (1680, 540), (1640, WL)]
HID = 'M' + ' L'.join(f'{x} {y}' for x, y in HIDP) + 'Z'
d += f'<clipPath id="hclip"><path d="{HID}"/></clipPath>'
b += f'<path d="{HID}" fill="#4a5cff" opacity=".45" filter="url(#bl5)"/>'
b += f'<path d="{HID}" fill="url(#haze)" opacity=".85" filter="url(#bl3)"/>'
g = '<g clip-path="url(#hclip)">'
g += '<rect x="600" y="470" width="560" height="620" fill="#0a0e50" opacity=".35" filter="url(#bl5)"/>'
g += '<rect x="1350" y="470" width="420" height="620" fill="#9fb0ff" opacity=".14" filter="url(#bl5)"/>'
INN = [(1000, 640), (1150, 600), (1330, 640), (1500, 620), (900, 820), (1100, 830), (1300, 860), (1480, 800), (1150, 980), (1380, 990)]
for (x0, y0) in HIDP:   # crystal ridges from the outline to the nearest inner points
    for (x1, y1) in sorted(INN, key=lambda p: (p[0] - x0) ** 2 + (p[1] - y0) ** 2)[:1]:
        g += f'<path d="M{x0} {y0} L{x1} {y1}" stroke="#c4cfff" stroke-width="3" opacity=".22"/>'
for (x0, y0) in INN:
    for (x1, y1) in sorted(INN, key=lambda p: (p[0] - x0) ** 2 + (p[1] - y0) ** 2)[1:3]:
        g += f'<path d="M{x0} {y0} L{x1} {y1}" stroke="#c4cfff" stroke-width="2.5" opacity=".16"/>'
for k in range(10):   # crystal facets, faint
    x0 = random.uniform(700, 1650); y0 = random.uniform(WL, 1040)
    g += f'<path d="M{x0:.0f} {y0:.0f} l{random.uniform(-260, 260):.0f} {random.uniform(60, 240):.0f}" stroke="#b9c6ff" stroke-width="3" opacity=".18"/>'
nodes = [(random.uniform(720, 1660), random.uniform(WL + 40, 1030)) for _ in range(40)]
for i, (x0, y0) in enumerate(nodes):   # cosmic web inside
    near = sorted(nodes, key=lambda p: (p[0] - x0) ** 2 + (p[1] - y0) ** 2)[1:3]
    for (x1, y1) in near:
        g += f'<path d="M{x0:.0f} {y0:.0f} Q{(x0 + x1) / 2 + random.uniform(-30, 30):.0f} {(y0 + y1) / 2 + random.uniform(-30, 30):.0f} {x1:.0f} {y1:.0f}" stroke="#a9b8ff" stroke-width="3" fill="none" opacity=".35" filter="url(#bl1)"/>'
    g += f'<circle cx="{x0:.0f}" cy="{y0:.0f}" r="{random.uniform(8, 16):.0f}" fill="#c4ceff" opacity=".35" filter="url(#bl3)"/><circle cx="{x0:.0f}" cy="{y0:.0f}" r="2.4" fill="#eef1ff" opacity=".8"/>'
g += f'<rect x="600" y="{WL}" width="1300" height="70" fill="#9fb8ff" opacity=".18" filter="url(#bl)"/>'
g += '</g>'
b += g
b += f'<path d="{HID}" fill="none" stroke="#8ea0ff" stroke-width="4" opacity=".5" filter="url(#bl3)"/>'
for _ in range(60):   # bubbles / specks
    x = random.uniform(150, 1550); y = random.uniform(WL + 20, 1060)
    if x > 1500 and y > 860: continue
    b += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{random.uniform(1.5, 4):.1f}" fill="none" stroke="#cfe0ff" stroke-width="1.5" opacity="{random.uniform(.2, .5):.2f}"/>'
# the visible tip, sunlit from the upper right, studded with stars
TIPP = [(1100, WL), (1170, 400), (1235, 300), (1330, 140), (1395, 225), (1455, 195), (1525, 320), (1590, 410), (1615, WL)]
b += '<path d="M' + ' L'.join(f'{x} {y}' for x, y in TIPP) + 'Z" fill="#ffe2a0" opacity=".45" filter="url(#bl2)"/>'
faces = [([(1100, WL), (1170, 400), (1235, 300), (1330, 140), (1290, 300), (1300, WL)], 'url(#iceL)'),
         ([(1330, 140), (1395, 225), (1420, 330), (1480, WL), (1300, WL), (1290, 300)], 'url(#iceR)'),
         ([(1395, 225), (1455, 195), (1440, 300), (1420, 330)], '#c9d8f4'),
         ([(1455, 195), (1525, 320), (1590, 410), (1615, WL), (1480, WL), (1420, 330), (1440, 300)], 'url(#iceR)')]
for poly, fill in faces:
    b += '<path d="M' + ' L'.join(f'{x} {y}' for x, y in poly) + f'Z" fill="{fill}" stroke="#ffffff" stroke-opacity=".35" stroke-width="2"/>'
b += '<path d="M1330 140 L1290 300 L1300 470" stroke="#fffaf0" stroke-width="5" fill="none" opacity=".9"/>'
b += '<path d="M1455 195 L1440 300 L1420 330 L1480 470" stroke="#fff3d0" stroke-width="4" fill="none" opacity=".8"/>'
b += '<path d="M1330 140 L1395 225 L1455 195 L1525 320 L1590 410" stroke="#fffdf4" stroke-width="6" fill="none" opacity=".9" filter="url(#bl1)"/>'
for _ in range(16):   # cracks on the shadow side
    x = random.uniform(1150, 1280); y = random.uniform(330, 460)
    b += f'<path d="M{x:.0f} {y:.0f} l{random.uniform(10, 40):.0f} {random.uniform(-30, 10):.0f}" stroke="#2a3f78" stroke-width="2" opacity=".6"/>'
for _ in range(26):   # stars embedded in the visible tip
    x = random.uniform(1180, 1580); y = random.uniform(240, 460)
    b += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{random.uniform(1.5, 3.5):.1f}" fill="#ffffff" opacity="{random.uniform(.5, 1):.2f}"/>'
b += spark(1330, 140, 34) + spark(1525, 318, 18) + spark(1250, 300, 14)
# waterline: bright skin and the tip's reflection
b += f'<rect x="0" y="{WL - 2}" width="1920" height="5" fill="#cfe6ff" opacity=".7"/>'
b += f'<rect x="1060" y="{WL - 6}" width="600" height="14" fill="#fff0c4" opacity=".5" filter="url(#bl3)"/>'
for k in range(10):
    b += f'<rect x="{1150 + random.uniform(-30, 60):.0f}" y="{WL + 8 + k * 9}" width="{380 - k * 30:.0f}" height="3" fill="#ffe7b0" opacity="{.45 - k * .04:.2f}"/>'
# tiny submarine with a searchlight on the hidden mass (scale)
SX, SY = 470, 820
b += f'<path d="M{SX + 60} {SY - 6} L{SX + 520} {SY - 130} L{SX + 560} {SY + 90} L{SX + 60} {SY + 10}Z" fill="#dbe8ff" opacity=".18" filter="url(#bl)"/>'
b += f'<ellipse cx="{SX + 540}" cy="{SY - 20}" rx="70" ry="110" fill="#e6efff" opacity=".22" filter="url(#bl2)"/>'
b += f'<g transform="translate({SX} {SY}) rotate(-8)"><ellipse rx="70" ry="24" fill="#d9a441" stroke="#2a1a08" stroke-width="3"/>'
b += '<rect x="-22" y="-44" width="40" height="24" rx="8" fill="#c48f30" stroke="#2a1a08" stroke-width="3"/>'
b += '<path d="M-70 0 L-92 -16 L-92 16Z" fill="#a8782a" stroke="#2a1a08" stroke-width="3"/>'
for k in range(3): b += f'<circle cx="{-30 + k * 26}" cy="0" r="7" fill="#9fe0ff" stroke="#2a1a08" stroke-width="2.5"/>'
b += '<circle cx="66" cy="-2" r="7" fill="#fffbe8"/><path d="M-50 -14 Q0 -30 50 -14" stroke="#ffe7b0" stroke-width="3" fill="none" opacity=".8"/></g>'
b += '<rect x="1560" y="860" width="420" height="260" fill="#010309" opacity=".6" filter="url(#bl2)"/>'
W('B.html', d, b, [('WE SEE', 150, 'w'), ('ONLY <span class="g">5%</span>', 220, 'w')], '#03051a', top=50)

# ======================= C: WHAT'S IN THE OTHER 95%?  (intuitive: the book with five readable pages) =======================
random.seed(33)
d = lin('wallC', [(0, '#07081c'), (1, '#121838')])
d += rad('glowC', 1180, 560, 760, [(0, '#ffd98a', .55), (.3, '#ff9d4a', .18), (1, '#ff9d4a', 0)])
d += lin('gold', [(0, '#fff6dc'), (.5, '#ffe2a0'), (1, '#e9b56a')], x2=1, y2=1)
d += lin('inv', [(0, '#3a4adf'), (1, '#141a6a')], x2=1, y2=1)
d += lin('desk', [(0, '#3a2216'), (1, '#0e0705')])
b = '<rect width="1920" height="1080" fill="url(#wallC)"/>'
# library shelves receding in the dark
for side in (0, 1):
    for col in range(3):
        x0 = 40 + col * 260 if side == 0 else 1920 - 300 - col * 260
        if side == 0 and col == 0: x0 = 30
        op = .55 - col * .12
        b += f'<rect x="{x0}" y="0" width="240" height="900" fill="#0d1130" opacity="{op:.2f}"/>'
        for r in range(7):
            y = 40 + r * 125
            b += f'<rect x="{x0}" y="{y + 110}" width="240" height="10" fill="#1d2350" opacity="{op:.2f}"/>'
            x = x0 + 8
            while x < x0 + 225:
                w = random.randint(12, 26); h = random.randint(70, 105)
                c = random.choice(['#2a2f6a', '#3a2a5a', '#23415a', '#4a3020', '#2a3a2a'])
                b += f'<rect x="{x}" y="{y + 110 - h}" width="{w}" height="{h}" fill="{c}" opacity="{op * .9:.2f}"/>'
                x += w + 2
b += '<rect width="1920" height="1080" fill="url(#glowC)"/>'
# desk
b += '<path d="M0 860 L1920 860 L1920 1080 L0 1080Z" fill="url(#desk)"/><rect x="0" y="856" width="1920" height="6" fill="#ffcf8a" opacity=".25"/>'
# book: covers and page blocks
SX = 1180; ST = 560; SB = 860
b += f'<ellipse cx="{SX}" cy="900" rx="600" ry="40" fill="#000" opacity=".55" filter="url(#bl)"/>'
b += f'<path d="M{SX} {SB + 30} C1000 {SB + 10} 820 {SB + 10} 690 {SB + 20} L700 {ST - 10} C820 {ST - 40} 1000 {ST - 40} {SX} {ST}Z" fill="#4a1e14" stroke="#d9a441" stroke-width="4"/>'
b += f'<path d="M{SX} {SB + 30} C1360 {SB + 10} 1540 {SB + 10} 1670 {SB + 20} L1660 {ST - 10} C1540 {ST - 40} 1360 {ST - 40} {SX} {ST}Z" fill="#4a1e14" stroke="#d9a441" stroke-width="4"/>'
# page edges (thickness) along the bottom: many blue lines, five gold
for k in range(14):
    y = SB + 2 + k * 2
    b += f'<path d="M{SX} {y + 6} C1000 {y - 14} 860 {y - 14} 720 {y - 4}" stroke="#2c3790" stroke-width="1.6" fill="none"/>'
    gold = k in (2, 5, 8, 10, 12)
    b += f'<path d="M{SX} {y + 6} C1360 {y - 14} 1500 {y - 14} 1640 {y - 4}" stroke="{"#ffd98a" if gold else "#2c3790"}" stroke-width="{2.4 if gold else 1.6}" fill="none"/>'
# left page: invisible ink - translucent indigo with ghost lines
LP = f'M{SX} {ST} C1040 {ST - 50} 860 {ST - 40} 720 {ST - 10} L720 {SB - 6} C860 {SB - 30} 1040 {SB - 30} {SX} {SB}Z'
RP = f'M{SX} {ST} C1320 {ST - 50} 1500 {ST - 40} 1640 {ST - 10} L1640 {SB - 6} C1500 {SB - 30} 1320 {SB - 30} {SX} {SB}Z'
b += f'<path d="{LP}" fill="url(#inv)" opacity=".85"/><path d="{LP}" fill="none" stroke="#9fb3ff" stroke-width="3" opacity=".6"/>'
for k in range(11):
    y = ST + 30 + k * 24
    b += f'<path d="M760 {y + 4} C900 {y - 18} 1050 {y - 16} 1150 {y + 2}" stroke="#7d92ff" stroke-width="5" fill="none" opacity=".16" stroke-dasharray="{random.randint(20, 60)} 10 {random.randint(30, 80)} 14"/>'
# right page: the one readable page, glowing gold
b += f'<path d="{RP}" fill="#ffd98a" opacity=".7" filter="url(#bl2)"/>'
b += f'<path d="{RP}" fill="url(#gold)"/>'
for k in range(10):
    y = ST + 26 + k * 25
    if 3 <= k <= 6:   # a little diagram: a spiral galaxy sketch on the page
        continue
    b += f'<path d="M1215 {y + 2} C1320 {y - 18} 1480 {y - 16} 1605 {y - 2}" stroke="#6a4214" stroke-width="5" fill="none" opacity=".6" stroke-dasharray="{random.randint(24, 60)} 9 {random.randint(14, 40)} 9 {random.randint(30, 70)} 9"/>'
b += '<g transform="translate(1330 670) rotate(-6)"><ellipse rx="78" ry="34" fill="none" stroke="#6a4214" stroke-width="3" opacity=".7"/>'
b += '<path d="M-70 4 Q-30 -40 0 0 Q30 40 70 -4" stroke="#6a4214" stroke-width="4" fill="none" opacity=".8"/><circle r="8" fill="#6a4214"/></g>'
b += '<g transform="translate(1520 668)"><circle r="40" fill="none" stroke="#6a4214" stroke-width="3" opacity=".6"/><path d="M0 0 L0 -40 A40 40 0 0 1 38 -12Z" fill="#6a4214" opacity=".55"/></g>'
# fluttering invisible-ink pages rising from the spine (translucent indigo, glowing blue edges)
for k, th in enumerate([150, 135, 120, 104, 88, 72, 58, 44]):
    a = math.radians(th); Wd = 470
    tx, ty = SX + Wd * math.cos(a), ST - Wd * .78 * math.sin(a)
    bx, by = SX + Wd * math.cos(a) * .96, SB - Wd * .7 * math.sin(a)
    cu = 70 * (1 if th < 90 else -1)
    pth = (f'M{SX} {ST} Q{SX + (tx - SX) * .5 + cu * .3:.0f} {ST + (ty - ST) * .5 - 70:.0f} {tx:.0f} {ty:.0f} '
           f'Q{tx + cu * .25:.0f} {(ty + by) / 2:.0f} {bx:.0f} {by:.0f} Q{SX + (bx - SX) * .5 + cu * .3:.0f} {SB + (by - SB) * .5 - 70:.0f} {SX} {SB}Z')
    b += f'<path d="{pth}" fill="#3b4ce0" opacity=".16"/>'
    b += f'<path d="{pth}" fill="none" stroke="#a9baff" stroke-width="3" opacity=".55"/>'
    b += f'<path d="M{SX} {ST} Q{SX + (tx - SX) * .5 + cu * .3:.0f} {ST + (ty - ST) * .5 - 70:.0f} {tx:.0f} {ty:.0f}" stroke="#dfe6ff" stroke-width="4" fill="none" opacity=".75" filter="url(#bl1)"/>'
# glow over the gold page, dust motes and sparks
b += '<ellipse cx="1420" cy="560" rx="260" ry="120" fill="#ffe2a0" opacity=".25" filter="url(#bl5)"/>'
for _ in range(90):
    x = random.uniform(760, 1660); y = random.uniform(120, 560)
    c = random.choice(['#fff1c8', '#fff1c8', '#b9c6ff'])
    b += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{random.choice([1.5, 2.2, 3.2])}" fill="{c}" opacity="{random.uniform(.35, .9):.2f}"/>'
b += spark(1450, 470, 26) + spark(1010, 250, 18, '#d6dfff') + spark(1300, 180, 14, '#d6dfff') + spark(1580, 360, 16)
b += '<rect x="1560" y="880" width="420" height="240" fill="#020203" opacity=".55" filter="url(#bl2)"/>'
W('C.html', d, b, [("WHAT'S IN", 130, 'w'), ('THE OTHER', 130, 'w'), ('95%?', 240, 'y')], '#03051a')
print('ok')
