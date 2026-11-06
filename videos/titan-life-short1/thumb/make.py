# Shorts thumbnails for titan-life, VERTICAL 1080x1920 (guideline 16-9: centred text around mid-height, picture above and below).
# ONE file writes all five:  python3 videos/titan-life-short1/thumb/make.py  -> videos/titan-life-short{1..5}/thumb/A.html
# Frog helpers copied from videos/deep-sea-giants-short1/thumb/make.py (not edited).
# 1  IT RAINS / METHANE        methane clouds pour rain over a glowing river valley; frog in helmet with umbrella. short1: "Clouds of methane ... pour down as alien rain", "rivers carving valleys"
# 2  WHAT'S / UNDER THE / SMOG?  Huygens under its parachute above; golden smog; coastline, channels, pebbles below, frog pointing up. short2: "golden smog", "coastlines, drainage channels ... rounded pebbles", tholins drifting down
# 3  LIFE / WITHOUT / WATER?   frog in a boat on a methane lake lowers a camera; a dashed, imagined "?" cell below. short3: "hypothesis", "beneath our robotic cameras"
# 4  A HIDDEN / OCEAN          cutaway: orange surface, icy crust, glowing water ocean below with diving frog. short4: "global ocean of liquid water ... beneath its icy crust"
# 5  FLYING / ON TITAN         Dragonfly rotorcraft over dunes with frog riding on top. short5: "rotorcraft called Dragonfly ... fly across Titan's dunes and craters"
import os, sys, math, random
HERE = os.path.dirname(os.path.abspath(__file__))
VID = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(VID, '..', 'tools'))
from thumb_lib import vpage, vsvg, lin, rad, spark

INK = '#1d2b1c'; GREEN = '#6aa55a'; DARKG = '#4d8a4a'; BELLY = '#9cc98a'
FILTERS = ''.join(f'<filter id="b{n}" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="{n}"/></filter>' for n in (3, 6, 12, 24, 50))
VIG = rad('vig', 540, 960, 1150, [(0, '#000', 0), (.62, '#000', 0), (1, '#000', .6)])
PEB = ('<radialGradient id="peb" cx=".38" cy=".3" r=".75"><stop offset="0" stop-color="#e8b27a"/><stop offset=".55" stop-color="#9a5a2a"/>'
       '<stop offset="1" stop-color="#3a1a08"/></radialGradient>')


def P(pts):
    return ' '.join(f'{a:.1f},{b:.1f}' for a, b in pts)


def limb(d, w=7.5, wi=3.4):
    return f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="{w}"/><path d="{d}" fill="none" stroke="{GREEN}" stroke-width="{wi}"/>'


def end_of(d):
    n = [float(v) for v in d.replace('M', ' ').replace('q', ' ').split()]
    return n[0] + n[-2], n[1] + n[-1]


def frog(x, y, s, rot=0, flip=False, look=(0, 0), mouth='O', armL=None, armR=None, legs=None, helmet=False,
         brows=True, back="", front="", shadow=False, mid=""):
    sx = -s if flip else s
    g = [f'<g transform="translate({x} {y}) rotate({rot}) scale({sx} {s})" stroke="{INK}" stroke-linejoin="round" stroke-linecap="round">', back]
    if shadow:
        g.append('<ellipse cx="0" cy="8" rx="50" ry="8" fill="#000" opacity=".25" stroke="none"/>')
    if helmet:
        g.append('<rect x="-50" y="-58" width="20" height="42" rx="7" fill="#c9ced8" stroke-width="3"/><rect x="-46" y="-52" width="5" height="30" rx="2" fill="#fff" stroke="none" opacity=".6"/>')
    for hx, hy, fx, fy, fa in (legs or ((-20, -6, -22, 4, 0), (20, -6, 22, 4, 0))):
        if abs(fx - hx) + abs(fy - hy) > 14:
            g.append(limb(f'M{hx} {hy} L{fx} {fy}', 15, 9))
        g.append(f'<ellipse cx="{fx}" cy="{fy}" rx="16" ry="9" transform="rotate({fa} {fx} {fy})" fill="{DARKG}" stroke-width="3.2"/>')
    g.append(f'<path d="M-34 0 q-6 -64 34 -70 q40 -2 42 62 q0 10 -6 12 q-36 6 -70 -4z" fill="{GREEN}" stroke-width="4"/>')
    g.append(f'<ellipse cx="2" cy="-12" rx="22" ry="20" fill="{BELLY}" stroke="none" opacity=".7"/>')
    g.append('<path d="M-24 -50 q6 -14 18 -16" fill="none" stroke="#b6dea0" stroke-width="3" opacity=".8"/>')
    lx, ly = look
    for ex in (-10, 22):
        g.append(f'<circle cx="{ex}" cy="-66" r="13.5" fill="#f4f5ea" stroke-width="3.2"/>')
        g.append(f'<circle cx="{ex + 1 + lx}" cy="{-66 + ly}" r="4.4" fill="{INK}" stroke="none"/>')
        g.append(f'<circle cx="{ex + 2.4 + lx}" cy="{-67.6 + ly}" r="1.5" fill="#fff" stroke="none"/>')
    if brows:
        g.append('<path d="M-22 -88 q12 -9 24 -1 M10 -89 q12 -8 24 1" fill="none" stroke-width="3.4"/>')
    if mouth == 'O':
        g.append('<ellipse cx="6" cy="-38" rx="10" ry="12" fill="#7a2f33" stroke-width="3"/><ellipse cx="6" cy="-31" rx="6" ry="4" fill="#e07b7b" stroke="none"/>')
    else:
        g.append('<ellipse cx="6" cy="-41" rx="6" ry="7.5" fill="#7a2f33" stroke-width="3"/>')
    g.append('<ellipse cx="-18" cy="-48" rx="5" ry="3" fill="#e98a8a" stroke="none" opacity=".55"/><ellipse cx="30" cy="-48" rx="5" ry="3" fill="#e98a8a" stroke="none" opacity=".55"/>')
    g.append(mid)
    if helmet:
        g.append('<circle cx="6" cy="-58" r="45" fill="#bfe6ff" fill-opacity=".13" stroke="#e8f6ff" stroke-width="3.4" stroke-opacity=".95"/>')
        g.append('<path d="M-26 -82 q12 -18 32 -21" fill="none" stroke="#fff" stroke-width="5" opacity=".8"/><path d="M42 -40 q6 -10 6 -22" fill="none" stroke="#fff" stroke-width="3" opacity=".5"/>')
        g.append('<ellipse cx="6" cy="-16" rx="40" ry="9" fill="#d3d9e3" stroke-width="3.2"/><path d="M-30 -18 q36 8 72 0" fill="none" stroke="#fff" stroke-width="2.2" opacity=".8"/>')
    for a in (armL or 'M-34 -22 q-14 6 -16 22', armR or 'M38 -22 q14 6 16 22'):
        g.append(limb(a)); ex_, ey_ = end_of(a)
        g.append(f'<circle cx="{ex_:.1f}" cy="{ey_:.1f}" r="5.6" fill="{GREEN}" stroke-width="3"/>')
    g.append(front); g.append('</g>')
    return ''.join(g)


def hand_at(x, y, s, arm, flip=False):
    ex, ey = end_of(arm)
    return (x - ex * s, y + ey * s) if flip else (x + ex * s, y + ey * s)


def bez(p, t):
    (x0, y0), (x1, y1), (x2, y2), (x3, y3) = p; u = 1 - t
    return (u ** 3 * x0 + 3 * u * u * t * x1 + 3 * u * t * t * x2 + t ** 3 * x3,
            u ** 3 * y0 + 3 * u * u * t * y1 + 3 * u * t * t * y2 + t ** 3 * y3)



# ---------------- shared Titan helpers ----------------
def sample(segs, n=26):
    pts = []
    for k, s in enumerate(segs):
        for i in range(0 if k == 0 else 1, n + 1):
            pts.append(bez(s, i / n))
    return pts


def ribbon(pts, w0, w1):
    L, R = [], []; m = len(pts) - 1
    for i, (x, y) in enumerate(pts):
        a = pts[max(i - 1, 0)]; b = pts[min(i + 1, m)]
        dx, dy = b[0] - a[0], b[1] - a[1]; l = math.hypot(dx, dy) or 1
        nx, ny = -dy / l, dx / l; w = w0 + (w1 - w0) * (i / m) ** 1.4
        L.append((x + nx * w, y + ny * w)); R.append((x - nx * w, y - ny * w))
    return f'M{P(L)} L{P(R[::-1])}Z'


def line(pts):
    return 'M' + P(pts)


def haze(rnd, n, x0, x1, y0, y1, col, o0, o1, r0, r1, f=50):
    return f'<g filter="url(#b{f})">' + ''.join(
        f'<ellipse cx="{rnd.randint(x0, x1)}" cy="{rnd.randint(y0, y1)}" rx="{rnd.randint(r0, r1)}" ry="{rnd.randint(r0 // 3, r1 // 3)}" fill="{col}" opacity="{rnd.uniform(o0, o1):.2f}"/>'
        for _ in range(n)) + '</g>'


def specks(rnd, n, x0, x1, y0, y1, cols, o0=.3, o1=.85, r0=1.5, r1=4.5, trail=0):
    o = ''
    for _ in range(n):
        x, y, r = rnd.uniform(x0, x1), rnd.uniform(y0, y1), rnd.uniform(r0, r1); c = rnd.choice(cols); op = rnd.uniform(o0, o1)
        if trail:
            o += f'<path d="M{x:.0f} {y:.0f} l{-trail * .15:.1f} {-trail:.0f}" stroke="{c}" stroke-width="{r * .8:.1f}" opacity="{op * .4:.2f}" stroke-linecap="round"/>'
        o += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r:.1f}" fill="{c}" opacity="{op:.2f}"/>'
    return o


def cloud_bank(rnd, n, x0, x1, y0, y1, r0, r1, dark, lit, rim_dy=26):
    C = [(rnd.randint(x0, x1), rnd.randint(y0, y1), rnd.randint(r0, r1)) for _ in range(n)]
    o = ''.join(f'<circle cx="{x}" cy="{y + rim_dy}" r="{r}" fill="{lit}"/>' for x, y, r in C)
    o += ''.join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{dark}"/>' for x, y, r in C)
    return o


def pebble(x, y, rx, ry, rot=0):
    return (f'<g transform="translate({x:.0f} {y:.0f}) rotate({rot})"><ellipse cx="4" cy="{ry * .55:.0f}" rx="{rx * 1.05:.0f}" ry="{ry * .45:.0f}" fill="#1a0a03" opacity=".55"/>'
            f'<ellipse rx="{rx:.0f}" ry="{ry:.0f}" fill="url(#peb)" stroke="#2a1205" stroke-width="3"/>'
            f'<ellipse cx="{-rx * .35:.0f}" cy="{-ry * .45:.0f}" rx="{rx * .3:.0f}" ry="{ry * .16:.0f}" fill="#ffe2b0" opacity=".55"/></g>')


# ---------------- 1: IT RAINS / METHANE ----------------
def umbrella():
    sc = ''.join(f'Q{x + 27.5:.1f} -14 {x:.1f} 0 ' for x in (82.5, 27.5, -27.5, -82.5))
    can = f'M-110 0 Q-104 -92 0 -98 Q104 -92 110 0 Q{110 - 13.75} -14 82.5 0 ' + sc.replace('Q82.5+27.5', '')
    can = 'M-110 0 Q-104 -92 0 -98 Q104 -92 110 0 ' + ''.join(f'Q{x - 27.5:.1f} -16 {x - 55:.1f} 0 ' for x in (110, 55, 0, -55)) + 'Z'
    o = '<g transform="translate(66 -150) rotate(-10)">'
    o += f'<path d="{can}" fill="#25a891" stroke="{INK}" stroke-width="4" stroke-linejoin="round"/>'
    for x in (-55, 55):
        o += f'<path d="M0 -98 Q{x * .55:.0f} -60 {x} 0" fill="none" stroke="#147a68" stroke-width="3"/>'
    o += '<path d="M0 -98 L0 0" stroke="#147a68" stroke-width="3"/>'
    o += '<path d="M-96 -18 Q-88 -78 -20 -90" fill="none" stroke="#bff8ec" stroke-width="7" opacity=".75" stroke-linecap="round"/>'
    o += f'<circle cx="0" cy="-102" r="6" fill="#f2d27a" stroke="{INK}" stroke-width="3"/>'
    o += f'<path d="M0 0 L-4 98 q-2 16 -16 14" fill="none" stroke="{INK}" stroke-width="7" stroke-linecap="round"/><path d="M0 0 L-4 98 q-2 16 -16 14" fill="none" stroke="#f2d27a" stroke-width="3" stroke-linecap="round"/>'
    for sx, sy in ((-80, -60), (-30, -100), (40, -96), (90, -50), (-110, -10), (112, -6)):
        o += f'<path d="M{sx} {sy - 4} l-7 -12 M{sx + 4} {sy - 6} l3 -13 M{sx + 8} {sy - 3} l10 -8" stroke="#d6fff6" stroke-width="2.6" stroke-linecap="round" opacity=".9"/>'
    return o + '</g>'


def make_1():
    rnd = random.Random(11)
    d = FILTERS + VIG + PEB
    d += lin('s1', [(0, '#240c04'), (.2, '#4e1e08'), (.42, '#9a4616'), (.6, '#dc8430'), (.69, '#f6be66'), (.72, '#c87030'), (1, '#3a1606')])
    d += rad('sun1', 760, 1320, 760, [(0, '#fff0b8', .75), (.3, '#ffb050', .3), (1, '#000', 0)])
    d += lin('riv', [(0, '#57d8c4'), (1, '#1d8f80')])
    d += lin('gnd1', [(0, '#7a3612'), (.3, '#4a1e08'), (1, '#1e0b03')])
    b = '<rect width="1080" height="1920" fill="url(#s1)"/><rect width="1080" height="1920" fill="url(#sun1)"/>'
    # rain curtains under the clouds
    for x in (80, 330, 620, 900):
        b += f'<path d="M{x - 90} 520 L{x + 90} 520 L{x - 60} 1340 L{x - 300} 1340Z" fill="#4a3a30" opacity=".22" filter="url(#b24)"/>'
    # cloud deck: dark methane clouds, underside lit amber
    b += '<g filter="url(#b3)">' + cloud_bank(rnd, 26, -120, 1200, 120, 300, 90, 170, '#2e1206', '#6a2e10', 20)
    b += cloud_bank(rnd, 30, -120, 1200, 260, 440, 80, 150, '#4a1e0a', '#b8602a', 30) + '</g>'
    b += cloud_bank(rnd, 22, -80, 1160, 400, 500, 50, 95, '#6a2c0e', '#e08a40', 22)
    b += haze(rnd, 10, 0, 1080, 520, 640, '#e8a050', .2, .4, 160, 300, 24)
    # horizon ridges
    b += '<path d="M0 1330 Q140 1290 260 1312 T520 1300 T800 1318 T1080 1296 L1080 1400 L0 1400Z" fill="#b8682e" opacity=".85"/>'
    b += '<path d="M0 1372 Q100 1330 220 1350 Q330 1366 420 1344 L470 1380 Q560 1352 700 1376 Q860 1340 1080 1360 L1080 1460 L0 1460Z" fill="#8a3e16"/>'
    b += '<path d="M0 1440 Q160 1400 330 1428 Q460 1446 520 1420 L600 1440 Q760 1400 1080 1430 L1080 1920 L0 1920Z" fill="url(#gnd1)"/>'
    # river valley: river winding from the horizon into a lake
    segs = [((560, 1364), (520, 1392), (640, 1410), (590, 1440)),
            ((590, 1440), (530, 1480), (700, 1520), (640, 1580)),
            ((640, 1580), (580, 1640), (820, 1700), (800, 1800))]
    pts = sample(segs)
    b += f'<path d="{ribbon(pts, 10, 120)}" fill="#1a0803" opacity=".8" filter="url(#b6)"/>'
    trib = [((300, 1450), (380, 1480), (460, 1470), (600, 1500)), ((980, 1470), (900, 1520), (800, 1540), (660, 1560))]
    for t in trib:
        tp = sample([t]); b += f'<path d="{ribbon(tp, 4, 26)}" fill="#1a0803" opacity=".7" filter="url(#b3)"/>'
    b += f'<path d="{ribbon(pts, 6, 80)}" fill="#7ff0dc" opacity=".55" filter="url(#b24)"/>'
    for t in trib:
        tp = sample([t]); b += f'<path d="{ribbon(tp, 2, 14)}" fill="url(#riv)" stroke="#0d4a40" stroke-width="2"/>'
    b += f'<path d="{ribbon(pts, 4, 62)}" fill="url(#riv)" stroke="#0d4a40" stroke-width="3"/>'
    b += f'<path d="{line(pts[::2])}" fill="none" stroke="#e6fffa" stroke-width="4" opacity=".55"/>'
    b += '<ellipse cx="820" cy="1855" rx="380" ry="110" fill="#7ff0dc" opacity=".45" filter="url(#b24)"/>'
    b += '<ellipse cx="820" cy="1860" rx="340" ry="90" fill="url(#riv)" stroke="#0d4a40" stroke-width="4"/>'
    b += '<path d="M560 1840 Q760 1800 1000 1830" fill="none" stroke="#e6fffa" stroke-width="5" opacity=".5"/>'
    # raindrop ripples on the water
    for _ in range(26):
        t = rnd.random(); x, y = pts[int(t * (len(pts) - 1))]
        if y < 1500 and rnd.random() < .6: continue
        r = rnd.uniform(6, 16) * (y - 1300) / 300
        b += f'<ellipse cx="{x + rnd.uniform(-20, 20):.0f}" cy="{y:.0f}" rx="{r:.1f}" ry="{r * .35:.1f}" fill="none" stroke="#e6fffa" stroke-width="2" opacity=".7"/>'
    for _ in range(22):
        x, y = rnd.uniform(520, 1100), rnd.uniform(1800, 1920); r = rnd.uniform(10, 26)
        b += f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{r:.0f}" ry="{r * .32:.1f}" fill="none" stroke="#e6fffa" stroke-width="2.4" opacity=".7"/>'
    # boulders with rim light
    for x, y, rx, ry in ((930, 1560, 70, 44), (1010, 1600, 50, 34), (440, 1640, 46, 28), (120, 1830, 120, 70)):
        b += pebble(x, y, rx, ry)
    # rain streaks (teal-white), drifting left
    for _ in range(420):
        x, y, L = rnd.uniform(-40, 1180), rnd.uniform(470, 1900), rnd.uniform(46, 120)
        b += f'<path d="M{x:.0f} {y:.0f} l{-L * .26:.0f} {L:.0f}" stroke="#d6fff6" stroke-width="{rnd.choice([2.2, 3, 3.8])}" opacity="{rnd.uniform(.25, .7):.2f}" stroke-linecap="round"/>'
    # frog on a rock in a helmet, holding an umbrella
    b += pebble(220, 1772, 130, 46)
    arm = 'M38 -26 q18 -6 24 -36'
    b += frog(220, 1740, 2.3, look=(-6, -10), mouth='O', helmet=True, shadow=False, armL='M-34 -24 q-22 -4 -30 -26', armR=arm, front=umbrella())
    b += spark(130, 1280, 18, '#d6fff6') + spark(980, 1270, 16, '#fff6d6') + spark(900, 640, 14)
    b += '<rect width="1080" height="1920" fill="url(#vig)"/>'
    lines = [('IT RAINS', 190, 'w'), ('METHANE', 202, 'y')]
    return vpage('#3a1606', vsvg(d, b), lines, outline='#1a0802', top=740)


# ---------------- 2: WHAT'S UNDER THE SMOG? ----------------
def parachute(cx, cy, w, h):
    x0, x1 = cx - w / 2, cx + w / 2; n = 10; dx = w / n
    sc = ''.join(f'Q{x1 - dx * (i + .5):.1f} {cy - 18} {x1 - dx * (i + 1):.1f} {cy} ' for i in range(n))
    dome = f'M{x0} {cy} C{x0} {cy - h * 1.3} {x1} {cy - h * 1.3} {x1} {cy} {sc}Z'
    o = f'<clipPath id="pc"><path d="{dome}"/></clipPath>'
    o += f'<path d="{dome}" fill="#ffe8b0" opacity=".5" filter="url(#b24)" transform="translate(0 -6)"/>'
    o += f'<path d="{dome}" fill="#f4e7c8"/>'
    o += '<g clip-path="url(#pc)">'
    apex = (cx, cy - h * 1.6)
    for i in range(n):
        if i % 2 == 0:
            o += f'<path d="M{apex[0]} {apex[1]} L{x0 + dx * i:.1f} {cy + 10} L{x0 + dx * (i + 1):.1f} {cy + 10}Z" fill="#d8482a"/>'
    o += f'<ellipse cx="{cx}" cy="{cy - h * .2}" rx="{w * .62}" ry="{h * 1.1}" fill="none" stroke="#5a1a08" stroke-width="120" opacity=".28" filter="url(#b24)"/>'
    o += f'<ellipse cx="{cx - w * .18}" cy="{cy - h * .78}" rx="{w * .2}" ry="{h * .22}" fill="#fff8e0" opacity=".55" filter="url(#b12)"/>'
    o += '</g>'
    for i in range(1, n):
        o += f'<path d="M{apex[0]} {apex[1] + 30} Q{x0 + dx * i:.1f} {cy - h * .8} {x0 + dx * i:.1f} {cy}" fill="none" stroke="#6a2a10" stroke-width="2" opacity=".5"/>'
    o += f'<ellipse cx="{cx}" cy="{cy - h * .98}" rx="{w * .05}" ry="{h * .05}" fill="#b9701e" opacity=".8"/>'
    o += f'<path d="{dome}" fill="none" stroke="#3a1606" stroke-width="5" stroke-linejoin="round"/>'
    return o, [(x0 + dx * i, cy) for i in range(n + 1)]


def huygens(cx, cy):
    o = f'<ellipse cx="{cx}" cy="{cy}" rx="200" ry="120" fill="#fff0c0" opacity=".45" filter="url(#b24)"/>'
    o += f'<path d="M{cx - 135} {cy - 6} L{cx - 135} {cy + 36} Q{cx} {cy + 82} {cx + 135} {cy + 36} L{cx + 135} {cy - 6}Z" fill="url(#foil)" stroke="#2a1a08" stroke-width="5" stroke-linejoin="round"/>'
    for k in range(-4, 5):
        x = cx + k * 30
        o += f'<path d="M{x} {cy + 6 + abs(k) * -1} L{x} {cy + 52 - abs(k) * 4}" stroke="#6a5020" stroke-width="2" opacity=".6"/>'
    o += f'<ellipse cx="{cx}" cy="{cy - 6}" rx="135" ry="36" fill="url(#lid)" stroke="#2a1a08" stroke-width="5"/>'
    o += f'<ellipse cx="{cx}" cy="{cy - 12}" rx="70" ry="18" fill="#c7b48a" stroke="#2a1a08" stroke-width="3"/>'
    o += f'<rect x="{cx - 96}" y="{cy - 26}" width="34" height="18" rx="4" fill="#3a3a44" stroke="#111" stroke-width="2.5"/>'
    o += f'<rect x="{cx + 52}" y="{cy - 30}" width="40" height="20" rx="4" fill="#d9d2c0" stroke="#2a1a08" stroke-width="2.5"/>'
    o += f'<circle cx="{cx + 20}" cy="{cy + 52}" r="9" fill="#9fe0ff" stroke="#111" stroke-width="2.5"/><circle cx="{cx + 20}" cy="{cy + 52}" r="20" fill="#bfe8ff" opacity=".5" filter="url(#b6)"/>'
    o += f'<path d="M{cx - 135} {cy + 8} l-40 18 M{cx + 135} {cy + 8} l42 14" stroke="#2a1a08" stroke-width="5" stroke-linecap="round"/>'
    o += f'<path d="M{cx - 120} {cy - 16} Q{cx - 60} {cy - 40} {cx + 10} {cy - 40}" fill="none" stroke="#fffbe6" stroke-width="5" opacity=".8" stroke-linecap="round"/>'
    return o


def make_2():
    rnd = random.Random(22)
    d = FILTERS + VIG + PEB
    d += lin('s2', [(0, '#6a2c0c'), (.14, '#b45a1a'), (.33, '#e49a3e'), (.48, '#f7cb6c'), (.62, '#f0b456'), (.71, '#d48a40'), (.74, '#8a4a20'), (1, '#2a1006')])
    d += rad('top2', 540, 300, 700, [(0, '#fff2c0', .55), (.5, '#ffd080', .15), (1, '#000', 0)])
    d += lin('foil', [(0, '#5a4418'), (.3, '#e8c870'), (.55, '#b08a3a'), (1, '#3a2a10')], 1, 0)
    d += lin('lid', [(0, '#f0e6cc'), (1, '#9a8a6a')])
    d += lin('lake2', [(0, '#5a44a8'), (1, '#2a1a60')])
    d += lin('gnd2', [(0, '#a8602a'), (.25, '#6a3414'), (1, '#1c0a03')])
    b = '<rect width="1080" height="1920" fill="url(#s2)"/><rect width="1080" height="1920" fill="url(#top2)"/>'
    b += haze(rnd, 8, 0, 1080, 60, 300, '#ffe6a8', .2, .4, 200, 360)
    # parachute + probe
    b += '<g transform="translate(540 420) scale(1.14) translate(-540 -420)">'
    pc, edge = parachute(540, 330, 600, 180)
    conf = (540, 540)
    for x, y in edge:
        b += f'<path d="M{x:.0f} {y} L{conf[0]} {conf[1]}" stroke="#3a1a08" stroke-width="2.4" opacity=".75"/>'
    b += pc
    b += f'<path d="M540 540 L540 585" stroke="#3a1a08" stroke-width="4"/>'
    b += huygens(540, 612)
    b += '</g>'
    b += spark(250, 200, 20, '#fff6d6') + spark(860, 520, 16, '#fff6d6')
    # thick golden smog around the text
    b += haze(rnd, 22, -100, 1180, 700, 1330, '#ffd890', .18, .42, 220, 420)
    b += haze(rnd, 10, -100, 1180, 1250, 1400, '#f2b060', .3, .5, 200, 400)
    # the surface below: coastline + channels in the distance
    b += '<path d="M0 1388 Q300 1370 540 1384 T1080 1380 L1080 1920 L0 1920Z" fill="#c07a3c"/>'
    lake = 'M0 1398 L120 1396 Q170 1408 140 1418 Q220 1424 300 1414 Q340 1430 280 1446 Q380 1456 470 1440 Q520 1452 470 1470 Q560 1478 620 1462 L640 1474 Q560 1500 420 1506 Q300 1516 0 1520Z'
    b += f'<path d="{lake}" fill="#8a70e0" opacity=".5" filter="url(#b12)"/><path d="{lake}" fill="url(#lake2)" stroke="#1a1040" stroke-width="3"/>'
    b += '<path d="M10 1420 Q200 1430 300 1426 M40 1470 Q260 1480 420 1474" fill="none" stroke="#c8b8ff" stroke-width="3" opacity=".6"/>'
    b += '<ellipse cx="210" cy="1470" rx="34" ry="8" fill="#a8602a" stroke="#4a2008" stroke-width="2"/>'
    # dendritic drainage channels flowing into the lake
    def chan(x, y, ang, L, w, dep):
        if dep == 0 or L < 12: return ''
        x2, y2 = x + math.cos(ang) * L, y + math.sin(ang) * L * .45
        o = f'<path d="M{x:.0f} {y:.0f} L{x2:.0f} {y2:.0f}" stroke="#4a2410" stroke-width="{w:.1f}" stroke-linecap="round"/>'
        for da in (-.5, .45):
            o += chan(x2, y2, ang + da + rnd.uniform(-.2, .2), L * .7, w * .7, dep - 1)
        return o
    b += chan(640, 1468, -.25, 90, 7, 5) + chan(560, 1490, .15, 80, 6, 4)
    # linear dunes mid-ground right
    for k in range(7):
        y = 1500 + k * 22
        b += f'<path d="M{650 - k * 30} {y} Q{860} {y - 14} {1100} {y - 4}" fill="none" stroke="#6a3412" stroke-width="{6 + k}" opacity=".8"/>'
        b += f'<path d="M{650 - k * 30} {y - 6} Q{860} {y - 20} {1100} {y - 10}" fill="none" stroke="#e8a860" stroke-width="{2 + k * .5:.1f}" opacity=".7"/>'
    b += '<path d="M0 1580 Q300 1560 600 1600 T1080 1590 L1080 1920 L0 1920Z" fill="url(#gnd2)"/>'
    # rounded pebbles, bigger in front
    P_ = []
    for _ in range(46):
        y = rnd.uniform(1600, 1890); s = (y - 1560) / 330
        P_.append((rnd.uniform(-20, 1100), y, rnd.uniform(14, 40) * s + 6, s))
    for x, y, r, s in sorted(P_, key=lambda p: p[1]):
        if 640 < x < 1000 and y > 1620: continue
        b += pebble(x, y, r, r * .62, rnd.uniform(-20, 20))
    b += pebble(820, 1790, 150, 52)
    # tholin dust drifting down everywhere
    b += specks(rnd, 260, 0, 1080, 80, 1880, ['#7a3a14', '#a8581e', '#f0b870'], .25, .8, 1.5, 4.5, trail=14)
    b += frog(820, 1760, 2.5, look=(-9, -11), mouth='O', helmet=True, shadow=True,
              armL='M-34 -26 q-20 -16 -22 -48', armR='M38 -22 q16 6 18 22')
    b += '<rect width="1080" height="1920" fill="url(#vig)"/>'
    lines = [("WHAT'S", 168, 'w'), ('UNDER THE', 168, 'w'), ('SMOG?', 236, 'y')]
    return vpage('#6a2c0c', vsvg(d, b), lines, outline='#2a0e02', top=716)


# ---------------- 3: LIFE WITHOUT WATER? ----------------
def make_3():
    rnd = random.Random(33)
    d = FILTERS + VIG
    d += lin('s3', [(0, '#3a1206'), (.45, '#a04a18'), (.85, '#f0a24a'), (1, '#f8c472')])
    d += rad('sun3', 760, 600, 520, [(0, '#fff2c0', .8), (.35, '#ffbe60', .3), (1, '#000', 0)])
    d += lin('lk3', [(0, '#5a2a12'), (.12, '#2e1208'), (.6, '#160709'), (1, '#0a0306')])
    d += rad('cellg', 560, 1560, 300, [(0, '#ff5fb4', .32), (.6, '#c03080', .12), (1, '#000', 0)])
    d += lin('hull', [(0, '#e8e2d6'), (1, '#8a8478')])
    SURF = 610
    b = f'<rect width="1080" height="{SURF}" fill="url(#s3)"/><rect width="1080" height="{SURF}" fill="url(#sun3)"/>'
    b += '<g filter="url(#b6)">' + cloud_bank(rnd, 30, -100, 1180, 110, 210, 60, 120, '#6a2a10', '#d07a34', 20) + '</g>'
    b += haze(rnd, 6, 0, 1080, 300, 520, '#ffd890', .2, .4, 200, 340, 24)
    # far shores
    b += f'<path d="M540 {SURF} L600 560 Q700 540 760 566 Q860 520 960 548 L1080 520 L1080 {SURF}Z" fill="#8a3e18" opacity=".8"/>'
    b += f'<path d="M0 {SURF} L0 470 Q60 440 120 480 L180 470 Q240 520 300 560 L360 {SURF}Z" fill="#5a240c"/>'
    b += f'<path d="M760 {SURF} L820 580 Q900 560 960 582 L1080 560 L1080 {SURF}Z" fill="#6a2c10"/>'
    # lake body
    b += f'<rect y="{SURF}" width="1080" height="{1920 - SURF}" fill="url(#lk3)"/>'
    b += f'<path d="M0 {SURF + 4} L1080 {SURF + 4}" stroke="#ffd890" stroke-width="5" opacity=".75"/>'
    for k in range(10):
        y = SURF + 14 + k * 9; x = rnd.uniform(500, 900)
        b += f'<path d="M{x - 120 + k * 6:.0f} {y} L{x + 120 - k * 6:.0f} {y}" stroke="#ffd890" stroke-width="3" opacity="{.5 - k * .04:.2f}"/>'
    # god rays into the dark lake
    for x, w in ((640, 70), (760, 40), (880, 90), (520, 30)):
        b += f'<path d="M{x - w} {SURF} L{x + w} {SURF} L{x - 200 + w * 2} 1500 L{x - 260} 1500Z" fill="#ffb060" opacity=".08" filter="url(#b12)"/>'
    # imagined cell: dashed, sketchy, glowing magenta -> hypothetical only
    b += '<rect width="1080" height="1920" fill="url(#cellg)"/>'
    cx, cy, R = 560, 1560, 210
    pts = [(cx + (R + 18 * math.sin(a * 3 + 1) + 10 * math.cos(a * 5)) * math.cos(a), cy + (R * .82 + 14 * math.sin(a * 4)) * math.sin(a)) for a in [i * math.pi / 40 for i in range(81)]]
    cellp = 'M' + P(pts) + 'Z'
    b += f'<path d="{cellp}" fill="#ff5fb4" opacity=".14"/>'
    b += f'<path d="{cellp}" fill="none" stroke="#ff7ac4" stroke-width="22" opacity=".4" filter="url(#b12)"/>'
    b += f'<path d="{cellp}" fill="none" stroke="#ffd0ec" stroke-width="7" stroke-dasharray="28 16" stroke-linecap="round"/>'
    inner = [(cx + (x - cx) * .9, cy + (y - cy) * .88) for x, y in pts]
    b += f'<path d="M{P(inner)}Z" fill="none" stroke="#ff8fd0" stroke-width="4" stroke-dasharray="10 14" stroke-linecap="round" opacity=".85"/>'
    for a in range(0, 360, 30):
        r = math.radians(a + 8); x0, y0 = cx + (R + 12) * math.cos(r), cy + (R * .82 + 8) * math.sin(r)
        x1, y1 = cx + (R + 70) * math.cos(r + .12), cy + (R * .82 + 60) * math.sin(r + .12)
        b += f'<path d="M{x0:.0f} {y0:.0f} Q{(x0 + x1) / 2 + 14:.0f} {(y0 + y1) / 2 - 10:.0f} {x1:.0f} {y1:.0f}" fill="none" stroke="#ffb0e0" stroke-width="4" stroke-dasharray="8 10" stroke-linecap="round" opacity=".8"/>'
    for ox, oy, rr in ((-100, -60, 34), (110, 50, 26), (-60, 90, 22), (90, -90, 18)):
        b += f'<circle cx="{cx + ox}" cy="{cy + oy}" r="{rr}" fill="#ff5fb4" fill-opacity=".18" stroke="#ffc0e6" stroke-width="3.5" stroke-dasharray="7 8"/>'
    b += f'<text x="{cx + 6}" y="{cy + 70}" text-anchor="middle" font-family="Fredoka" font-weight="700" font-size="230" fill="#ff8fd0" opacity=".55" filter="url(#b12)">?</text>'
    b += f'<text x="{cx + 6}" y="{cy + 70}" text-anchor="middle" font-family="Fredoka" font-weight="700" font-size="230" fill="none" stroke="#ffe0f2" stroke-width="6" stroke-dasharray="20 12">?</text>'
    # hydrogen bubbles
    for _ in range(26):
        x, y, r = rnd.uniform(300, 900), rnd.uniform(1260, 1800), rnd.uniform(4, 13)
        if math.hypot((x - cx) / R, (y - cy) / (R * .82)) < 1.25: continue
        b += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r:.1f}" fill="#ffd0ec" fill-opacity=".12" stroke="#ffd0ec" stroke-width="2" opacity=".7"/>'
    b += specks(rnd, 120, 0, 1080, SURF + 20, 1900, ['#ffb070', '#ff9fd8'], .15, .5, 1.2, 3)
    # boat on the surface with the frog lowering a camera on a cable
    bx = 250
    cam = (110, 1390)
    b += f'<path d="M{cam[0]} 470 L{cam[0]} {cam[1] - 40}" stroke="#1a0a06" stroke-width="7"/><path d="M{cam[0]} 470 L{cam[0]} {cam[1] - 40}" stroke="#d8d0c0" stroke-width="3"/>'
    b += f'<path d="M{cam[0] + 30} {cam[1]} L{cam[0] + 420} {cam[1] + 60} L{cam[0] + 330} {cam[1] + 340}Z" fill="#fff0d0" opacity=".16" filter="url(#b12)"/>'
    b += (f'<g transform="translate({cam[0]} {cam[1]})"><rect x="-40" y="-40" width="72" height="62" rx="12" fill="#e8e2d6" stroke="#111" stroke-width="5"/>'
          f'<circle cx="30" cy="-8" r="22" fill="#2a2a36" stroke="#111" stroke-width="5"/><circle cx="34" cy="-8" r="10" fill="#9fe0ff"/><circle cx="36" cy="-12" r="4" fill="#fff"/>'
          f'<circle cx="-24" cy="-26" r="6" fill="#ff4060"/><circle cx="-24" cy="-26" r="16" fill="#ff4060" opacity=".4" filter="url(#b6)"/></g>')
    b += f'<ellipse cx="{bx}" cy="{SURF + 8}" rx="190" ry="20" fill="#000" opacity=".35" filter="url(#b6)"/>'
    arm = 'M-34 -26 q-22 -10 -30 -34'
    fx, fy, fs = bx + 30, SURF - 40, 2.35
    hx, hy = hand_at(fx, fy, fs, arm)
    b += frog(fx, fy, fs, look=(-10, 6), mouth='O', helmet=True, armL=arm, armR='M38 -22 q16 4 20 20')
    b += f'<path d="M{hx:.0f} {hy:.0f} L{cam[0]} 470" stroke="#1a0a06" stroke-width="12" stroke-linecap="round"/><path d="M{hx:.0f} {hy:.0f} L{cam[0]} 470" stroke="#c8a060" stroke-width="6" stroke-linecap="round"/>'
    b += f'<circle cx="{cam[0]}" cy="470" r="9" fill="#d8d0c0" stroke="#111" stroke-width="3"/>'
    hull = f'M{bx - 170} {SURF - 40} L{bx + 170} {SURF - 40} Q{bx + 160} {SURF + 26} {bx + 90} {SURF + 30} L{bx - 110} {SURF + 30} Q{bx - 170} {SURF + 20} {bx - 170} {SURF - 40}Z'
    b += f'<path d="{hull}" fill="url(#hull)" stroke="#111" stroke-width="6" stroke-linejoin="round"/>'
    b += f'<path d="M{bx - 170} {SURF - 22} L{bx + 168} {SURF - 22}" stroke="#ff5fb4" stroke-width="10"/>'
    b += f'<path d="M{bx - 150} {SURF - 34} L{bx + 120} {SURF - 34}" stroke="#fff" stroke-width="4" opacity=".7"/>'
    b += f'<path d="M{bx + 130} {SURF - 40} L{bx + 130} {SURF - 140}" stroke="#111" stroke-width="6"/><circle cx="{bx + 130}" cy="{SURF - 150}" r="13" fill="#ffe08a" stroke="#111" stroke-width="4"/><circle cx="{bx + 130}" cy="{SURF - 150}" r="40" fill="#ffe08a" opacity=".5" filter="url(#b12)"/>'
    b += f'<path d="M{bx - 220} {SURF + 10} Q{bx} {SURF + 30} {bx + 230} {SURF + 8}" fill="none" stroke="#ffd890" stroke-width="3" opacity=".6"/>'
    b += spark(980, 260, 18, '#fff6d6') + spark(880, 1300, 16, '#ffd0ec') + spark(240, 1680, 14, '#ffd0ec')
    b += '<rect width="1080" height="1920" fill="url(#vig)"/>'
    lines = [('LIFE', 200, 'w'), ('WITHOUT', 200, 'w'), ('WATER?', 222, 'y')]
    return vpage('#1a0806', vsvg(d, b), lines, outline='#1a0306', top=700)


# ---------------- 4: A HIDDEN OCEAN ----------------
def arc_y(x, y0, R=3600):
    return y0 + R - math.sqrt(R * R - (x - 540) ** 2)


def arc_path(y0, R=3600, step=20):
    return [(x, arc_y(x, y0, R)) for x in range(-20, 1101, step)]


def make_4():
    rnd = random.Random(44)
    d = FILTERS + VIG
    d += lin('s4', [(0, '#3a1406'), (.5, '#b8581c'), (1, '#f4b25a')])
    d += lin('ice', [(0, '#8eb0c6'), (.5, '#5a7e9c'), (1, '#3a5a7c')])
    d += lin('sea', [(0, '#3a9cff'), (.18, '#1a5cc8'), (.6, '#0a2a72'), (1, '#071438')])
    d += rad('core', 540, 2050, 700, [(0, '#ff9a3c', .7), (.4, '#e0602a', .25), (1, '#000', 0)])
    d += rad('glow4', 540, 1240, 640, [(0, '#8fd8ff', .5), (.5, '#3a9cff', .15), (1, '#000', 0)])
    SY, IY = 480, 1220
    b = f'<rect width="1080" height="{SY + 80}" fill="url(#s4)"/>'
    b += haze(rnd, 8, 0, 1080, 130, 420, '#ffd890', .2, .45, 200, 360)
    b += '<g filter="url(#b6)" opacity=".85">' + cloud_bank(rnd, 26, -100, 1180, 150, 250, 50, 100, '#7a3412', '#f0a050', 18) + '</g>'
    # surface landscape: hills + a dark methane lake, light from the hazy sky
    b += '<path d="M-20 430 Q120 360 240 400 Q330 330 430 392 L520 420 Q640 350 760 394 Q880 330 1000 380 L1100 370 L1100 560 L-20 560Z" fill="#a85a26" opacity=".9"/>'
    surf = arc_path(SY)
    b += f'<path d="M{P(surf)} L1100 480 L1100 430 Q900 412 760 440 Q620 418 500 446 Q300 420 160 450 Q60 434 -20 450Z" fill="#7a3a16"/>'
    b += '<ellipse cx="760" cy="462" rx="190" ry="20" fill="#2a1a40" stroke="#120a20" stroke-width="3"/><path d="M640 458 Q760 450 880 458" stroke="#c8a0ff" stroke-width="3" opacity=".6" fill="none"/>'
    # ice crust with strata and cracks
    ice_top = arc_path(SY); ice_bot = arc_path(IY)
    b += f'<path d="M{P(ice_top)} L{P(ice_bot[::-1])}Z" fill="url(#ice)"/>'
    b += f'<path d="M{P(ice_top)}" fill="none" stroke="#4a1e08" stroke-width="16"/><path d="M{P(arc_path(SY + 10))}" fill="none" stroke="#c88a50" stroke-width="5" opacity=".7"/>'
    for k in range(1, 7):
        st = arc_path(SY + k * 104 + rnd.randint(-20, 20))
        b += f'<path d="M{P(st)}" fill="none" stroke="#c8e4f4" stroke-width="{rnd.choice([2, 3, 4])}" opacity="{rnd.uniform(.15, .35):.2f}"/>'
    for _ in range(14):
        x, y = rnd.uniform(0, 1080), rnd.uniform(SY + 40, IY - 40); pts = [(x, y)]
        for _ in range(5):
            x += rnd.uniform(-40, 40); y += rnd.uniform(20, 60); pts.append((x, y))
        b += f'<path d="M{P(pts)}" fill="none" stroke="#e6f6ff" stroke-width="3" opacity=".45"/>'
    for _ in range(26):
        x, y, r = rnd.uniform(0, 1080), rnd.uniform(SY + 40, IY - 30), rnd.uniform(6, 22)
        b += f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{r:.0f}" ry="{r * .6:.0f}" fill="#c8e4f4" opacity=".18"/>'
    # ocean
    ocean_top = [(x, y + 18 * math.sin(x / 70) + 10 * math.sin(x / 23)) for x, y in ice_bot]
    b += f'<path d="M{P(ocean_top)} L1100 1940 L-20 1940Z" fill="url(#sea)"/>'
    b += '<rect width="1080" height="1920" fill="url(#glow4)"/>'
    b += '<rect width="1080" height="1920" fill="url(#core)"/>'
    b += f'<path d="M{P(ocean_top)}" fill="none" stroke="#bff0ff" stroke-width="18" opacity=".55" filter="url(#b12)"/>'
    b += f'<path d="M{P(ocean_top)}" fill="none" stroke="#e6fbff" stroke-width="5" opacity=".9"/>'
    # icicle-like bumps under the ice
    for x in range(10, 1080, 46):
        y = arc_y(x, IY) + 18 * math.sin(x / 70) + 10 * math.sin(x / 23); h = rnd.uniform(16, 50)
        b += f'<path d="M{x - 16} {y - 2:.0f} L{x + rnd.uniform(-4, 4):.0f} {y + h:.0f} L{x + 16} {y - 2:.0f}Z" fill="#9ccbe4" opacity=".85" stroke="#d8f2ff" stroke-width="2"/>'
    # light shafts and bubbles
    for x in (180, 420, 700, 920):
        b += f'<path d="M{x - 40} {IY + 20} L{x + 40} {IY + 20} L{x + 140} 1900 L{x - 60} 1900Z" fill="#bff0ff" opacity=".07" filter="url(#b12)"/>'
    for _ in range(46):
        x, y, r = rnd.uniform(0, 1080), rnd.uniform(IY + 60, 1880), rnd.uniform(3, 12)
        b += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r:.1f}" fill="#bff0ff" fill-opacity=".12" stroke="#d8f8ff" stroke-width="2" opacity=".75"/>'
    b += specks(rnd, 90, 0, 1080, IY + 40, 1880, ['#bff0ff', '#ffffff'], .2, .6, 1.2, 3)
    # dark rocky floor glow far below
    b += '<path d="M-20 1860 Q200 1800 380 1840 Q560 1790 760 1836 Q920 1800 1100 1840 L1100 1940 L-20 1940Z" fill="#1a0e1c"/>'
    b += '<path d="M-20 1860 Q200 1800 380 1840 Q560 1790 760 1836 Q920 1800 1100 1840" fill="none" stroke="#ff9a3c" stroke-width="5" opacity=".7"/>'
    # diving frog with a flashlight, rising toward the ice
    fx, fy, fs = 330, 1640, 2.5
    arm = 'M38 -26 q22 -6 30 -26'
    hx, hy = hand_at(fx, fy, fs, arm)
    b += f'<path d="M{hx:.0f} {hy:.0f} L{hx + 520:.0f} {hy - 180:.0f} L{hx + 430:.0f} {hy + 100:.0f}Z" fill="#fff6d0" opacity=".22" filter="url(#b12)"/>'
    tank = '<rect x="-56" y="-60" width="24" height="52" rx="10" fill="#f2d27a" stroke="#1d2b1c" stroke-width="3"/><rect x="-52" y="-54" width="6" height="36" rx="3" fill="#fff" opacity=".6" stroke="none"/>'
    torch = '<g transform="translate(68 -52) rotate(-18)"><rect x="-8" y="-9" width="34" height="18" rx="5" fill="#3a3a44" stroke="#1d2b1c" stroke-width="3"/><rect x="24" y="-12" width="10" height="24" rx="3" fill="#fff6c8" stroke="#1d2b1c" stroke-width="3"/></g>'
    b += frog(fx, fy, fs, rot=-12, look=(8, -8), mouth='O', helmet=True, armL='M-34 -24 q-22 -2 -30 18', armR=arm, back=tank, front=torch,
              legs=((-20, -6, -40, 18, -30), (20, -6, 30, 22, 20)))
    for k in range(5):
        b += f'<circle cx="{fx + 40 + k * 8}" cy="{fy - 300 - k * 40}" r="{6 + k * 2}" fill="none" stroke="#e6fbff" stroke-width="2.5" opacity=".8"/>'
    b += spark(900, 1440, 18, '#e6fbff') + spark(140, 300, 16, '#fff6d6') + spark(980, 1700, 14, '#e6fbff')
    b += '<rect width="1080" height="1920" fill="url(#vig)"/>'
    lines = [('A HIDDEN', 196, 'w'), ('OCEAN', 270, 'y')]
    return vpage('#0a2a72', vsvg(d, b), lines, outline='#06122a', top=730)


# ---------------- 5: FLYING ON TITAN ----------------
def rotor(cx, cy, rx, ry, far=False):
    op = .55 if far else .75
    o = f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="#f6efe0" opacity=".16"/>'
    o += f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="none" stroke="#fff8e8" stroke-width="3" opacity="{op}"/>'
    for a, w in ((-.35, 18), (2.8, 14)):
        o += f'<path d="M{cx} {cy} L{cx + rx * math.cos(a):.0f} {cy + ry * math.sin(a):.0f} L{cx + rx * math.cos(a + .32):.0f} {cy + ry * math.sin(a + .32):.0f}Z" fill="#2a2a30" opacity=".35"/>'
    o += f'<ellipse cx="{cx}" cy="{cy - 14}" rx="{rx * .96:.0f}" ry="{ry * .96:.0f}" fill="none" stroke="#fff8e8" stroke-width="2" opacity="{op * .6:.2f}"/>'
    o += f'<rect x="{cx - 9}" y="{cy - 24}" width="18" height="40" rx="5" fill="#4a4a54" stroke="#15151a" stroke-width="3"/>'
    o += f'<circle cx="{cx}" cy="{cy - 24}" r="8" fill="#5ef0b0" stroke="#15151a" stroke-width="2.5"/><circle cx="{cx}" cy="{cy - 24}" r="22" fill="#5ef0b0" opacity=".45" filter="url(#b6)"/>'
    return o


def make_5():
    rnd = random.Random(55)
    d = FILTERS + VIG + PEB
    d += lin('s5', [(0, '#5a220a'), (.25, '#b85c1c'), (.55, '#f0a84a'), (.7, '#fbd488'), (.72, '#d89048'), (1, '#3a1606')])
    d += rad('sun5', 300, 260, 700, [(0, '#fff2c0', .6), (.4, '#ffc060', .2), (1, '#000', 0)])
    d += lin('bodyg', [(0, '#ffffff'), (.5, '#d6d2ca'), (1, '#7a766e')])
    d += lin('dune', [(0, '#5a2c12'), (1, '#1e0c04')])
    b = '<rect width="1080" height="1920" fill="url(#s5)"/><rect width="1080" height="1920" fill="url(#sun5)"/>'
    b += haze(rnd, 10, 0, 1080, 100, 700, '#ffe2a8', .15, .35, 200, 380)
    b += haze(rnd, 12, -100, 1180, 760, 1330, '#ffd890', .2, .4, 240, 420)
    # horizon with a crater rim far right
    b += '<path d="M-20 1360 Q300 1340 600 1352 Q700 1310 820 1300 Q900 1296 960 1330 L1100 1336 L1100 1420 L-20 1420Z" fill="#c07a3c" opacity=".85"/>'
    b += '<path d="M700 1340 Q830 1290 980 1340" fill="none" stroke="#ffe0a0" stroke-width="4" opacity=".7"/>'
    # long linear dunes receding
    for k in range(10):
        y = 1370 + k ** 1.55 * 18; amp = 6 + k * 3
        c = f'M-20 {y + amp:.0f} Q270 {y - amp:.0f} 540 {y + amp * .3:.0f} T1100 {y - amp * .2:.0f}'
        b += f'<path d="{c} L1100 1940 L-20 1940Z" fill="url(#dune)" opacity=".96"/>'
        b += f'<path d="{c}" fill="none" stroke="#ffd08a" stroke-width="{3 + k * 1.1:.1f}" opacity=".9"/>'
        b += f'<path d="{c}" fill="none" stroke="#120502" stroke-width="{6 + k * 3:.1f}" opacity=".35" transform="translate(0 {8 + k * 3})" filter="url(#b6)"/>'
    # ripples in foreground sand
    for k in range(12):
        y = 1780 + k * 12 + rnd.uniform(-3, 3)
        b += f'<path d="M-20 {y:.0f} Q270 {y - 8:.0f} 540 {y:.0f} T1100 {y - 4:.0f}" fill="none" stroke="#c88848" stroke-width="2" opacity=".45"/>'
    # drone shadow on the dunes
    b += '<g filter="url(#b6)" opacity=".75"><ellipse cx="600" cy="1600" rx="210" ry="40" fill="#140602"/>'
    for x in (380, 820, 470, 730):
        b += f'<ellipse cx="{x}" cy="{1585 if x in (470, 730) else 1625}" rx="120" ry="22" fill="#140602" opacity=".75"/>'
    b += '</g>'
    # speed lines behind the drone
    for _ in range(14):
        y = rnd.uniform(220, 640); x = rnd.uniform(-40, 200)
        b += f'<path d="M{x:.0f} {y:.0f} l{rnd.uniform(80, 200):.0f} 0" stroke="#fff6dc" stroke-width="4" opacity=".45" stroke-linecap="round"/>'
    # Dragonfly rotorcraft: body + 4 arms with coaxial rotors
    b += '<g transform="translate(540 520) scale(1.16) translate(-540 -450)">'
    far = [(300, 300), (780, 300)]; near = [(160, 400), (920, 400)]
    b += '<ellipse cx="540" cy="460" rx="430" ry="230" fill="#fff0c0" opacity=".3" filter="url(#b50)"/>'
    for (hx, hy) in far:
        b += f'<path d="M{540 + (hx - 540) * .35:.0f} 440 L{hx} {hy + 10}" stroke="#15151a" stroke-width="20" stroke-linecap="round"/><path d="M{540 + (hx - 540) * .35:.0f} 440 L{hx} {hy + 10}" stroke="#9a968c" stroke-width="11" stroke-linecap="round"/>'
        b += rotor(hx, hy, 140, 26, far=True)
    # skids
    for x in (420, 660):
        b += f'<path d="M{x} 560 L{x - 30} 620 M{x + 40} 560 L{x + 60} 620" stroke="#15151a" stroke-width="10" stroke-linecap="round"/>'
    b += '<path d="M340 622 L480 622 M600 622 L760 622" stroke="#15151a" stroke-width="12" stroke-linecap="round"/><path d="M340 622 L480 622 M600 622 L760 622" stroke="#c8c4bc" stroke-width="5" stroke-linecap="round"/>'
    # body
    b += '<path d="M330 440 Q330 410 360 408 L730 408 Q770 410 776 440 L770 560 Q766 580 740 582 L360 582 Q334 580 332 556Z" fill="url(#bodyg)" stroke="#15151a" stroke-width="7" stroke-linejoin="round"/>'
    b += '<path d="M340 470 L766 470" stroke="#9a968c" stroke-width="3"/><path d="M360 420 Q520 412 740 420" stroke="#fff" stroke-width="6" opacity=".9" fill="none"/>'
    b += '<rect x="372" y="490" width="120" height="70" rx="8" fill="#c9a24a" stroke="#15151a" stroke-width="4"/><path d="M380 500 l100 0 M380 520 l100 0 M380 540 l100 0" stroke="#8a6a20" stroke-width="2.5"/>'
    b += '<path d="M776 452 L840 470 L840 540 L772 552Z" fill="#6a665e" stroke="#15151a" stroke-width="5" stroke-linejoin="round"/>'
    for y in (482, 500, 518, 536):
        b += f'<path d="M780 {y} L836 {y + 4}" stroke="#2a2a30" stroke-width="3"/>'
    b += '<circle cx="610" cy="530" r="24" fill="#22222a" stroke="#15151a" stroke-width="4"/><circle cx="610" cy="530" r="12" fill="#5ef0b0"/><circle cx="604" cy="524" r="4" fill="#fff"/><circle cx="610" cy="530" r="40" fill="#5ef0b0" opacity=".35" filter="url(#b6)"/>'
    b += '<circle cx="690" cy="530" r="14" fill="#22222a" stroke="#15151a" stroke-width="3"/><circle cx="690" cy="530" r="6" fill="#5ef0b0"/>'
    # high-gain antenna dish on top
    b += '<path d="M650 408 L660 370" stroke="#15151a" stroke-width="8"/>'
    b += '<ellipse cx="664" cy="352" rx="70" ry="28" transform="rotate(-14 664 352)" fill="#f0ece4" stroke="#15151a" stroke-width="6"/><ellipse cx="664" cy="352" rx="44" ry="15" transform="rotate(-14 664 352)" fill="#c8c4bc"/>'
    b += '<path d="M664 352 L690 320" stroke="#15151a" stroke-width="4"/><circle cx="690" cy="318" r="6" fill="#15151a"/>'
    # frog riding on top, goggles and a mint scarf flapping
    scarf = ('<path d="M-30 -20 Q-90 -40 -140 -10 Q-110 -30 -150 -50 Q-80 -60 -30 -32Z" fill="#5ef0b0" stroke="#1d2b1c" stroke-width="3" stroke-linejoin="round"/>'
             '<path d="M-32 -26 Q6 -14 44 -26 L44 -16 Q6 -2 -32 -16Z" fill="#5ef0b0" stroke="#1d2b1c" stroke-width="3" stroke-linejoin="round"/>')
    gog = ('<path d="M-30 -70 Q6 -84 42 -70" fill="none" stroke="#1d2b1c" stroke-width="5"/>'
           '<circle cx="-10" cy="-86" r="11" fill="#9fe0ff" fill-opacity=".7" stroke="#6a4a1a" stroke-width="5"/><circle cx="22" cy="-86" r="11" fill="#9fe0ff" fill-opacity=".7" stroke="#6a4a1a" stroke-width="5"/>'
           '<circle cx="-13" cy="-89" r="3" fill="#fff"/><circle cx="19" cy="-89" r="3" fill="#fff"/>')
    b += frog(470, 412, 2.25, look=(6, -2), mouth='O', armL='M-34 -26 q-20 -12 -24 -42', armR='M38 -26 q20 -12 24 -42', back=scarf, mid=gog,
              legs=((-20, -6, -24, 4, 0), (20, -6, 24, 4, 0)))
    for (hx, hy) in near:
        b += f'<path d="M{540 + (hx - 540) * .4:.0f} 460 L{hx} {hy + 10}" stroke="#15151a" stroke-width="24" stroke-linecap="round"/><path d="M{540 + (hx - 540) * .4:.0f} 460 L{hx} {hy + 10}" stroke="#bdb8ae" stroke-width="13" stroke-linecap="round"/>'
        b += rotor(hx, hy, 160, 30)
    b += '</g>'
    b += spark(980, 180, 20, '#fff6d6') + spark(120, 640, 16, '#fff6d6') + spark(900, 1500, 14, '#fff6d6')
    b += specks(rnd, 60, 0, 1080, 1300, 1900, ['#f2b868'], .2, .6, 1.5, 3.5)
    for x, y, r in ((120, 1820, 60), (210, 1850, 34), (930, 1800, 48), (1010, 1840, 70), (300, 1720, 22), (820, 1700, 26)):
        b += pebble(x, y, r, r * .6)
    b += '<rect width="1080" height="1920" fill="url(#vig)"/>'
    lines = [('FLYING', 236, 'y'), ('ON TITAN', 168, 'w')]
    return vpage('#3a1606', vsvg(d, b), lines, outline='#1a0802', top=800)


if __name__ == '__main__':
    for n, fn in enumerate((make_1, make_2, make_3, make_4, make_5), 1):
        out = os.path.join(VID, f'titan-life-short{n}', 'thumb')
        os.makedirs(out, exist_ok=True)
        open(os.path.join(out, 'A.html'), 'w').write(fn())
    print('ok')
