# Thumbnails A-C for titan-life (guideline 16-6 / 16-8, brief tools/briefs/thumb_art.md). Run: python3 videos/titan-life/thumb/make.py
# A  A SEA OF METHANE        homage: Hokusai "The Great Wave off Kanagawa" (mirrored): a huge teal methane wave with claw foam curls over
#                            a small boat (frog in a space helmet) under an amber Titan sky; Saturn sits low under the curl where Fuji was.
#                            Script S14 ("a slow wave roll across a sea of liquid methane and ethane"), S13 ("immense polar seas").
# B  OCEAN UNDER THE ICE?    intuitive: Titan cut open like a fruit: orange hazy globe, the cut shows the ice shell and a glowing
#                            water ocean inside; the parka frog on top shines a torch into the cut. Question form keeps the hedge
#                            ("strongly suggest", S35-S40).
# C  FLYING AT -180°C        homage: Van Gogh "The Starry Night": swirling amber haze, Saturn instead of the crescent moon, a dark
#                            ice spire instead of the cypress; NASA's Dragonfly rotorcraft (frog riding on top) over dunes.
#                            Script S02/S08 ("around minus one hundred and eighty degrees Celsius"), S41-S45 (Dragonfly, flying on Titan).
import os, sys, math, random
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', '..', 'tools'))
from thumb_lib import page, svg, lin, rad, spark

INK = '#1d2b1c'; GREEN = '#6aa55a'; DARKG = '#4d8a4a'; BELLY = '#9cc98a'
FILTERS = ''.join(f'<filter id="b{n}" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="{n}"/></filter>'
                  for n in (1, 2, 3, 6, 12, 24, 50, 80))


def poly(pts):
    return 'M' + ' L'.join(f'{x:.1f},{y:.1f}' for x, y in pts) + 'Z'


def smooth(pts, closed=False, t=.5):
    """Catmull-Rom through pts -> cubic bezier path."""
    P = list(pts); n = len(P)
    d = f'M{P[0][0]:.1f},{P[0][1]:.1f}'
    rng = range(n) if closed else range(n - 1)
    for i in rng:
        p0 = P[(i - 1) % n] if (closed or i > 0) else P[i]
        p1 = P[i]; p2 = P[(i + 1) % n]
        p3 = P[(i + 2) % n] if (closed or i + 2 < n) else p2
        c1 = (p1[0] + (p2[0] - p0[0]) * t / 3, p1[1] + (p2[1] - p0[1]) * t / 3)
        c2 = (p2[0] - (p3[0] - p1[0]) * t / 3, p2[1] - (p3[1] - p1[1]) * t / 3)
        d += f' C{c1[0]:.1f},{c1[1]:.1f} {c2[0]:.1f},{c2[1]:.1f} {p2[0]:.1f},{p2[1]:.1f}'
    return d + ('Z' if closed else '')


def cr_sample(pts, n=10):
    """points along the Catmull-Rom curve through pts (n per segment)."""
    out = []
    for i in range(len(pts) - 1):
        p0 = pts[max(i - 1, 0)]; p1 = pts[i]; p2 = pts[i + 1]; p3 = pts[min(i + 2, len(pts) - 1)]
        for k in range(n):
            t = k / n; t2 = t * t; t3 = t2 * t
            out.append(tuple(.5 * (2 * p1[j] + (-p0[j] + p2[j]) * t + (2 * p0[j] - 5 * p1[j] + 4 * p2[j] - p3[j]) * t2 + (-p0[j] + 3 * p1[j] - 3 * p2[j] + p3[j]) * t3) for j in (0, 1)))
    out.append(pts[-1])
    return out


def bez(p0, p1, p2, p3, t):
    u = 1 - t
    return (u ** 3 * p0[0] + 3 * u * u * t * p1[0] + 3 * u * t * t * p2[0] + t ** 3 * p3[0],
            u ** 3 * p0[1] + 3 * u * u * t * p1[1] + 3 * u * t * t * p2[1] + t ** 3 * p3[1])


# ---------------- mascot frog (tools/assets/frog.svg body), posable ----------------
def limb(d, w=7.5, wi=3.4, col=GREEN):
    return f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="{w}"/><path d="{d}" fill="none" stroke="{col}" stroke-width="{wi}"/>'


def end_of(d):
    n = [float(v) for v in d.replace('M', ' ').replace('q', ' ').split()]
    return n[0] + n[-2], n[1] + n[-1]


def frog(x, y, s, rot=0, flip=False, look=(0, 0), mouth='O', armL=None, armR=None, legs=None, helmet=False,
         back='', front='', mid='', hat='', sleeve=None):
    sx = -s if flip else s
    g = [f'<g transform="translate({x} {y}) rotate({rot}) scale({sx} {s})" stroke="{INK}" stroke-linejoin="round" stroke-linecap="round">', back]
    if helmet:
        g.append('<rect x="-50" y="-58" width="20" height="42" rx="7" fill="#d9dde6" stroke-width="3"/><rect x="-46" y="-52" width="5" height="30" rx="2" fill="#fff" stroke="none" opacity=".7"/>')
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
    g.append('<path d="M-22 -88 q12 -9 24 -1 M10 -89 q12 -8 24 1" fill="none" stroke-width="3.4"/>')
    if mouth == 'O':
        g.append('<ellipse cx="6" cy="-38" rx="10" ry="12" fill="#7a2f33" stroke-width="3"/><ellipse cx="6" cy="-31" rx="6" ry="4" fill="#e07b7b" stroke="none"/>')
    else:
        g.append('<ellipse cx="6" cy="-41" rx="6" ry="7.5" fill="#7a2f33" stroke-width="3"/>')
    g.append('<ellipse cx="-18" cy="-48" rx="5" ry="3" fill="#e98a8a" stroke="none" opacity=".55"/><ellipse cx="30" cy="-48" rx="5" ry="3" fill="#e98a8a" stroke="none" opacity=".55"/>')
    g.append(hat)
    if helmet:
        g.append('<circle cx="6" cy="-56" r="47" fill="#cfeaff" fill-opacity=".13" stroke="#eef6ff" stroke-width="4.5"/>')
        g.append('<path d="M-28 -80 q12 -18 32 -21" fill="none" stroke="#fff" stroke-width="5" opacity=".8"/><path d="M44 -40 q6 -10 6 -22" fill="none" stroke="#fff" stroke-width="3" opacity=".5"/>')
        g.append('<ellipse cx="6" cy="-12" rx="42" ry="9" fill="#e6eaf2" stroke-width="3.2"/><path d="M-30 -14 q36 8 72 0" fill="none" stroke="#fff" stroke-width="2.2" opacity=".8"/>')
    g.append(mid)
    for a in (armL or 'M-34 -22 q-14 6 -16 22', armR or 'M38 -22 q14 6 16 22'):
        if sleeve:
            g.append(f'<path d="{a}" fill="none" stroke="{INK}" stroke-width="13"/><path d="{a}" fill="none" stroke="{sleeve}" stroke-width="8.5"/>')
        else:
            g.append(limb(a))
        ex_, ey_ = end_of(a)
        g.append(f'<circle cx="{ex_:.1f}" cy="{ey_:.1f}" r="5.6" fill="{GREEN}" stroke-width="3"/>')
    g.append(front); g.append('</g>')
    return ''.join(g)


def saturn(cx, cy, r, tilt=-14, glow=True, op=1.0):
    o = f'<g opacity="{op}">'
    if glow:
        o += f'<circle cx="{cx}" cy="{cy}" r="{r * 2.2:.0f}" fill="#ffe2a0" opacity=".35" filter="url(#b50)"/>'
    o += f'<g transform="translate({cx} {cy}) rotate({tilt})">'
    ring = lambda k, w, c, opa: f'<ellipse rx="{r * k:.1f}" ry="{r * k * .22:.1f}" fill="none" stroke="{c}" stroke-width="{r * w:.1f}" opacity="{opa}"/>'
    back = ''.join(ring(k, w, c, a) for k, w, c, a in ((2.15, .26, '#e8c98a', .85), (1.78, .3, '#f6dfa8', .95), (1.48, .12, '#c8a46a', .7)))
    o += f'<clipPath id="satTop{cx}"><rect x="{-r * 3}" y="{-r * 3}" width="{r * 6}" height="{r * 3}"/></clipPath>'
    o += f'<g clip-path="url(#satTop{cx})">{back}</g>'
    o += f'<circle r="{r}" fill="url(#satG)"/>'
    for k, (yy, h, c, a) in enumerate(((-.55, .12, '#c99a55', .5), (-.2, .16, '#e9c98a', .55), (.15, .1, '#b98a4a', .45), (.42, .14, '#d8b070', .4))):
        o += f'<clipPath id="sb{cx}{k}"><circle r="{r}"/></clipPath><rect x="{-r}" y="{r * yy:.1f}" width="{r * 2}" height="{r * h:.1f}" fill="{c}" opacity="{a}" clip-path="url(#sb{cx}{k})"/>'
    o += f'<circle r="{r}" fill="url(#satShade)"/>'
    o += f'<clipPath id="satBot{cx}"><rect x="{-r * 3}" y="0" width="{r * 6}" height="{r * 3}"/></clipPath>'
    o += f'<g clip-path="url(#satBot{cx})">{back}</g>'
    o += '</g></g>'
    return o


SATDEFS = ('<radialGradient id="satG" cx=".38" cy=".32" r=".8"><stop offset="0" stop-color="#fff3cf"/><stop offset=".6" stop-color="#ecc988"/><stop offset="1" stop-color="#a87a3c"/></radialGradient>'
           + '<radialGradient id="satShade" cx=".3" cy=".25" r="1"><stop offset=".55" stop-color="#3a1a06" stop-opacity="0"/><stop offset="1" stop-color="#3a1a06" stop-opacity=".7"/></radialGradient>')


def claw(x, y, s, rot, col='#fff4dc', edge='#0e3a44'):
    # one Hokusai foam lobe: a thick tongue curling back, ending in small grasping fingers
    w = 2.4 / s
    return (f'<g transform="translate({x:.1f} {y:.1f}) rotate({rot:.1f}) scale({s:.2f})" fill="{col}" stroke="{edge}" stroke-width="{w:.2f}" stroke-linejoin="round">'
            '<path d="M6,-14 C-14,-34 -54,-36 -66,-10 C-74,8 -60,26 -42,20 C-52,10 -48,-6 -36,-8 C-22,-10 -12,4 -8,16 L8,12Z"/>'
            '<path d="M-60,16 c-8,6 -18,2 -16,-6 c4,4 10,4 12,0Z"/><path d="M-46,22 c-4,9 -14,9 -16,2 c5,2 10,1 12,-3Z"/>'
            '<path d="M-68,0 c-9,2 -15,-6 -10,-12 c1,5 6,8 11,6Z"/></g>')


# =============================== A: The Great Wave (methane) ===============================
def make_A():
    rnd = random.Random(7)
    d = FILTERS + SATDEFS
    d += lin('skyA', [(0, '#6e2a0c'), (.35, '#b5561c'), (.7, '#e79a45'), (1, '#f6c77c')])
    d += lin('seaA', [(0, '#3d5a52'), (.15, '#1b3e40'), (1, '#071a1d')])
    d += lin('waveA', [(0, '#2a8a8e'), (.45, '#13595f'), (1, '#062429')], x2=1, y2=.6)
    d += lin('faceA', [(0, '#3fb0aa'), (.5, '#1a6d70'), (1, '#0a3238')], x2=1, y2=0)
    d += lin('boatA', [(0, '#c7864a'), (1, '#6a3a18')])
    d += rad('hazeA', 980, 560, 700, [(0, '#ffe2a6', .75), (.5, '#f6b968', .25), (1, '#f6b968', 0)])
    d += rad('cornerA', 1920, 1080, 560, [(0, '#03100f', .9), (.6, '#03100f', .45), (1, '#03100f', 0)])
    d += rad('vigA', 960, 540, 1150, [(.6, '#000', 0), (1, '#1a0700', .55)])
    b = '<rect width="1920" height="1080" fill="url(#skyA)"/>'
    b += '<rect width="1920" height="1080" fill="url(#hazeA)"/>'
    # Hokusai-style flat cloud bands in the haze
    for cx, cy, w, h, a in ((520, 560, 520, 26, .35), (1180, 470, 600, 20, .3), (300, 640, 380, 16, .3), (900, 650, 420, 14, .3), (160, 470, 300, 18, .25)):
        b += f'<rect x="{cx - w / 2}" y="{cy}" width="{w}" height="{h}" rx="{h / 2}" fill="#fff0cf" opacity="{a}"/>'
    # methane rain streaks far away (left), very faint
    for _ in range(60):
        x = rnd.uniform(40, 600); y = rnd.uniform(420, 760)
        b += f'<path d="M{x:.0f} {y:.0f} l-8 34" stroke="#fff3da" stroke-width="2" opacity="{rnd.uniform(.08, .22):.2f}"/>'
    # Saturn low on the horizon where Fuji stood
    b += saturn(770, 712, 50, tilt=-12)
    # far sea
    b += '<rect x="0" y="770" width="1920" height="310" fill="url(#seaA)"/>'
    b += '<rect x="0" y="768" width="1920" height="5" fill="#ffe0a0" opacity=".55"/>'
    for _ in range(40):
        x = rnd.uniform(0, 1400); y = rnd.uniform(782, 860)
        b += f'<path d="M{x:.0f} {y:.0f} q20 -6 40 0" stroke="#f6c77c" stroke-width="2" fill="none" opacity="{rnd.uniform(.2, .5):.2f}"/>'
    # ---- the big wave (curls leftward) ----
    W = 125
    face = [(640, 1080), (770, 930), (890, 790), (990, 650), (1070, 530), (1110, 440), (1100, 375), (1060, 338), (1010, 342), (978, 376), (968, 425)]
    lip = [(968, 425), (950, 350), (975, 265), (1050, 190), (1160, 140), (1300, 115), (1450, 130), (1600, 195), (1750, 290), (1920, 390)]
    face = [(x + W, y) for x, y in face]; lip = [(x + W, y) for x, y in lip]
    body = smooth(face + lip[1:]) + ' L1920,1080 Z'
    b += f'<clipPath id="waveClip"><path d="{body}"/></clipPath>'
    b += f'<path d="{smooth(lip)}" fill="none" stroke="#fff4d6" stroke-width="110" opacity=".5" filter="url(#b24)"/>'
    b += f'<path d="{body}" fill="url(#waveA)"/>'
    g = '<g clip-path="url(#waveClip)">'
    g += f'<path d="{smooth([(x + 40, y + 10) for x, y in face[:-3]])}" fill="none" stroke="url(#faceA)" stroke-width="170" opacity=".9" filter="url(#b12)"/>'
    # Hokusai stripes: the wave outline shrunk toward its foot, so they follow body and curl
    outline = cr_sample(face[1:6] + [(1210, 300)] + lip[4:9], 12)
    ax, ay = 1980, 1180
    for k in range(1, 15):
        f = 1 - k * .062
        pts = [(ax + (x - ax) * f, ay + (y - ay) * f) for x, y in outline]
        dd = 'M' + ' L'.join(f'{x:.1f},{y:.1f}' for x, y in pts)
        g += f'<path d="{dd}" fill="none" stroke="#04181b" stroke-width="7" opacity=".35" transform="translate(8 8)"/>'
        g += f'<path d="{dd}" fill="none" stroke="#86dcd2" stroke-width="{6.5 - k * .3:.1f}" opacity="{.62 - k * .03:.2f}"/>'
    # tube shadow under the lip
    g += f'<path d="{smooth([(x + 30, y + 30) for x, y in face[4:9]])}" fill="none" stroke="#03161a" stroke-width="70" opacity=".5" filter="url(#b12)"/>'
    g += '<rect x="1300" y="700" width="620" height="380" fill="url(#cornerA)"/>'
    g += '</g>'
    b += g
    # foam crest band along the lip
    foam = smooth(lip[:9])
    b += f'<path d="{foam}" fill="none" stroke="#0e3a44" stroke-width="64" stroke-linecap="round"/>'
    b += f'<path d="{foam}" fill="none" stroke="#fff1d2" stroke-width="54" stroke-linecap="round"/>'
    b += f'<path d="{smooth([(x + 10, y + 18) for x, y in lip[1:9]])}" fill="none" stroke="#a9ddd6" stroke-width="12" opacity=".75"/>'
    # claw fingers along the outer crest, pointing outward and curling forward
    pts = cr_sample(lip[:8], 10)
    for i in range(2, len(pts) - 1, 2):
        (x0, y0), (x1, y1) = pts[i - 1], pts[i + 1]
        L = math.hypot(x1 - x0, y1 - y0) or 1
        nx, ny = (y1 - y0) / L, -(x1 - x0) / L        # outward (left-hand) normal
        x, y = pts[i]
        th = math.degrees(math.atan2(-ny, -nx))
        u = i / len(pts)
        s = (1.25 - u * .7 if u > .3 else 1.0) + rnd.uniform(-.1, .1)
        off = 22 if u > .3 else 12
        b += claw(x + nx * off, y + ny * off, max(.42, s), th + rnd.uniform(-10, 10))
    # big grasping claws at the lip tip
    tx, ty = lip[0]
    for dx, dy, s, r in ((-6, 6, 1.9, 255), (-30, -20, 1.5, 220), (16, 24, 1.4, 285), (-36, -60, 1.3, 195), (30, 40, 1.0, 300), (-20, -100, 1.15, 180)):
        b += claw(tx + dx, ty + dy, s, r)
    # spray falling from the lip (Hokusai's snow-like foam)
    for _ in range(160):
        x = rnd.gauss(tx - 10, 70); y = rnd.uniform(380, 650)
        if x < 860 or x > tx + 90: continue
        r = rnd.choice([3, 4, 5, 6, 8])
        b += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r}" fill="#fff4dc" stroke="#0e3a44" stroke-width="1.5" opacity="{rnd.uniform(.6, 1):.2f}"/>'
    # small front wave (left bottom) with its own curl
    fw = [(0, 1080), (0, 930), (160, 880), (320, 860), (450, 890), (520, 940), (500, 990), (460, 975)]
    b += f'<path d="{smooth(fw)} L560,1080Z" fill="url(#waveA)"/>'
    for k in range(1, 6):
        b += f'<path d="{smooth([(0, 960 + k * 22), (200, 920 + k * 22), (380, 920 + k * 20), (520, 1010 + k * 10)])}" fill="none" stroke="#86dcd2" stroke-width="4" opacity=".35"/>'
    b += f'<path d="{smooth([(10, 925), (170, 878), (320, 858), (450, 888), (515, 940)])}" fill="none" stroke="#0e3a44" stroke-width="30" stroke-linecap="round"/>'
    b += f'<path d="{smooth([(10, 925), (170, 878), (320, 858), (450, 888), (515, 940)])}" fill="none" stroke="#fff1d2" stroke-width="22" stroke-linecap="round"/>'
    for x, y, r in ((524, 948, 250), (498, 978, 280), (450, 878, 200), (370, 852, 190), (260, 860, 180), (150, 880, 170)):
        b += claw(x, y, .7, r)
    # long slim boat with the frog sliding down the wave face
    bx, by, br = 1140, 945, -24
    hull = 'M-230,-10 Q-110,30 10,30 Q140,28 240,-36 Q236,-14 226,0 Q130,62 10,62 Q-120,62 -222,16Z'
    boat = (f'<g transform="translate({bx} {by}) rotate({br})">'
            f'<ellipse cx="0" cy="56" rx="240" ry="22" fill="#03181b" opacity=".55" filter="url(#b6)"/>'
            '<path d="M-226,-8 Q-110,10 10,10 Q140,8 238,-34 Q130,24 10,30 Q-110,30 -226,-8Z" fill="#3a1c0a" stroke="#2a1306" stroke-width="4"/>')
    boat += frog(-20, 40, 2.1, rot=12, look=(-7, -6), mouth='O', helmet=True,
                 armL='M-34 -22 q-24 -6 -36 -30', armR='M38 -22 q18 4 24 26')
    boat += '<path d="M-150,-60 L80,90" stroke="#2a1306" stroke-width="13" stroke-linecap="round"/><path d="M-150,-60 L80,90" stroke="#d0a06a" stroke-width="6" stroke-linecap="round"/>'
    boat += (f'<path d="{hull}" fill="url(#boatA)" stroke="#2a1306" stroke-width="5" stroke-linejoin="round"/>'
             '<path d="M-222,-6 Q-110,34 10,34 Q140,32 236,-32" fill="none" stroke="#ffe0b0" stroke-width="5" opacity=".9"/>'
             '<path d="M-150,40 Q-60,56 60,54" fill="none" stroke="#ffe0b0" stroke-width="3" opacity=".45"/></g>')
    b += boat
    for _ in range(30):
        x = bx + rnd.uniform(-240, 240); y = by + rnd.uniform(50, 120) - (x - bx) * .4
        b += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{rnd.choice([3, 4, 6])}" fill="#fff4dc" opacity=".85"/>'
    b += spark(1500, 60, 26) + spark(1080, 110, 16) + spark(640, 600, 14) + spark(1200, 560, 12, '#e8fbff')
    b += '<rect width="1920" height="1080" fill="url(#vigA)"/>'
    lines = [('A SEA OF', 150, 'w'), ('METHANE', 176, 'y')]
    return page('#6e2a0c', svg(d, b), lines, outline='#2a0f04', top=44)


# =============================== B: Titan cut open ===============================
def make_B():
    rnd = random.Random(3)
    CX, CY, R = 1250, 640, 425
    YAW, PITCH = math.radians(-32), math.radians(24)

    def P(x, y, z, r=1.0):
        x, y, z = x * r, y * r, z * r
        x1 = x * math.cos(YAW) + z * math.sin(YAW); z1 = -x * math.sin(YAW) + z * math.cos(YAW)
        y2 = y * math.cos(PITCH) - z1 * math.sin(PITCH)
        return (CX + R * x1, CY - R * y2)
    d = FILTERS + SATDEFS
    d += lin('spaceB', [(0, '#2a120a'), (.6, '#170906'), (1, '#0c0504')])
    d += f'<radialGradient id="globeB" cx="{CX - 150}" cy="{CY - 170}" r="{R * 1.25:.0f}" gradientUnits="userSpaceOnUse"><stop offset="0" stop-color="#ffd083"/><stop offset=".4" stop-color="#e8903a"/><stop offset=".75" stop-color="#a24c14"/><stop offset="1" stop-color="#4a1c06"/></radialGradient>'
    d += rad('limbB', CX, CY, R + 80, [(.78, '#ffb560', 0), (.84, '#ffb560', .6), (1, '#ffb560', 0)])
    d += rad('vigB', 960, 540, 1150, [(.6, '#000', 0), (1, '#000', .6)])
    d += rad('cornerB', 1920, 1080, 480, [(0, '#0c0504', .9), (1, '#0c0504', 0)])
    b = '<rect width="1920" height="1080" fill="url(#spaceB)"/>'
    for _ in range(190):
        b += f'<circle cx="{rnd.uniform(0, 1920):.0f}" cy="{rnd.uniform(0, 1080):.0f}" r="{rnd.choice([1.2, 1.6, 2.2])}" fill="#ffe9cc" opacity="{rnd.uniform(.15, .7):.2f}"/>'
    b += saturn(1760, 170, 120, tilt=-18, op=.9)
    # hazy atmosphere glow
    b += f'<circle cx="{CX}" cy="{CY}" r="{R + 80}" fill="url(#limbB)"/>'
    b += f'<circle cx="{CX}" cy="{CY}" r="{R + 30}" fill="#ffa040" opacity=".45" filter="url(#b24)"/>'
    b += f'<circle cx="{CX}" cy="{CY}" r="{R}" fill="url(#globeB)"/>'
    b += f'<clipPath id="gB"><circle cx="{CX}" cy="{CY}" r="{R}"/></clipPath>'
    g = '<g clip-path="url(#gB)">'
    for k in range(7):
        g += f'<ellipse cx="{CX - 40}" cy="{CY - R + 70 + k * 105}" rx="{R * 1.05:.0f}" ry="16" fill="#ffd79a" opacity=".12" filter="url(#b6)"/>'
    # dark methane lakes near the north pole (front-left)
    for lo, la, sz in ((-150, 70, 46), (-120, 62, 34), (-170, 60, 26), (-100, 74, 22), (-140, 55, 18), (-80, 66, 16)):
        x, y = P(math.cos(math.radians(la)) * math.cos(math.radians(lo)), math.sin(math.radians(la)), math.cos(math.radians(la)) * -math.sin(math.radians(lo)))
        g += f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{sz}" ry="{sz * .45:.0f}" transform="rotate(-8 {x:.0f} {y:.0f})" fill="#2e1a0e" opacity=".85"/>'
        g += f'<ellipse cx="{x - sz * .2:.0f}" cy="{y - sz * .1:.0f}" rx="{sz * .5:.0f}" ry="{sz * .15:.0f}" fill="#7cc6bc" opacity=".45"/>'
    # equatorial dune belt
    for k in range(40):
        t = math.radians(rnd.uniform(110, 300)); la = math.radians(rnd.uniform(-14, 8))
        x, y = P(math.cos(la) * math.cos(t), math.sin(la), math.cos(la) * math.sin(t))
        g += f'<path d="M{x:.0f},{y:.0f} q30 -8 64 2" stroke="#7a320c" stroke-width="5" fill="none" opacity=".3" filter="url(#b1)"/>'
    g += f'<circle cx="{CX + 170}" cy="{CY + 170}" r="{R}" fill="#200800" opacity=".55" filter="url(#b50)"/>'
    g += '</g>'
    b += g
    # ---- the cut-away octant: three quarter-disk faces looking into the notch ----
    layers = [(1.0, '#b65a1c'), (.965, '#e4eef5'), (.86, '#1cc0e0'), (.58, '#8ea6bc'), (.42, '#ec6a22')]
    faces = [(lambda t: (0, math.sin(t), math.cos(t)), .62),      # wall facing right
             (lambda t: (math.cos(t), 0, math.sin(t)), 1.0),      # equatorial floor (lit from above)
             (lambda t: (math.cos(t), math.sin(t), 0), .8)]       # back wall facing the viewer

    def shade(hexc, f):
        r, g_, b_ = int(hexc[1:3], 16), int(hexc[3:5], 16), int(hexc[5:7], 16)
        return '#%02x%02x%02x' % (min(255, int(r * f)), min(255, int(g_ * f)), min(255, int(b_ * f)))
    ts = [math.radians(v) for v in range(0, 91, 3)]
    for fn, br in faces:
        for i, (r1, col) in enumerate(layers):
            r2 = layers[i + 1][0] if i + 1 < len(layers) else 0
            outer = [P(*fn(t), r=r1) for t in ts]
            inner = [P(*fn(t), r=r2) for t in reversed(ts)] if r2 else [P(0, 0, 0)]
            b += f'<path d="{poly(outer + inner)}" fill="{shade(col, br)}" stroke="{shade(col, br)}" stroke-width="1"/>'
            if col == '#1cc0e0':
                mid = [P(*fn(t), r=.72) for t in ts]
                b += f'<path d="{poly(mid)[:-1]}" fill="none" stroke="#9ffcff" stroke-width="10" opacity=".55" filter="url(#b6)"/>'
                for _ in range(10):
                    t = rnd.uniform(.08, 1.5); rr = rnd.uniform(.61, .83)
                    x, y = P(*fn(t), r=rr)
                    b += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{rnd.choice([2, 3, 4])}" fill="none" stroke="#eaffff" stroke-width="1.6" opacity=".8"/>'
            if col == '#ec6a22':
                b += f'<path d="{poly(outer + inner)}" fill="#ff9a40" opacity=".3"/>'
                for _ in range(5):
                    t = rnd.uniform(.15, 1.4); rr = rnd.uniform(.12, .36)
                    x, y = P(*fn(t), r=rr)
                    b += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{rnd.choice([5, 7, 9])}" fill="#6a2a12" opacity=".5"/>'
        for r1, _ in layers[1:]:
            b += f'<path d="{poly([P(*fn(t), r=r1) for t in ts])[:-1]}" fill="none" stroke="#1a0a04" stroke-width="2.5" opacity=".45"/>'
    # warm core glow and ocean glow
    cx0, cy0 = P(0, 0, 0)
    b += f'<circle cx="{cx0:.0f}" cy="{cy0:.0f}" r="110" fill="#ffb060" opacity=".6" filter="url(#b24)"/>'
    # edges of the notch
    for v in ((1, 0, 0), (0, 1, 0), (0, 0, 1)):
        x, y = P(*v)
        b += f'<path d="M{cx0:.1f},{cy0:.1f} L{x:.1f},{y:.1f}" stroke="#1a0a04" stroke-width="7" stroke-linecap="round"/>'
        b += f'<path d="M{cx0:.1f},{cy0:.1f} L{x:.1f},{y:.1f}" stroke="#ffe8c0" stroke-width="2" opacity=".55"/>'
    for fn, br in faces:
        b += f'<path d="{poly([P(*fn(t)) for t in ts])[:-1]}" fill="none" stroke="#1a0a04" stroke-width="6" stroke-linecap="round"/>'
        b += f'<path d="{poly([P(*fn(t), r=.99) for t in ts])[:-1]}" fill="none" stroke="#ffcf8a" stroke-width="2.5" opacity=".8"/>'
    # light spilling from the ocean
    oc = [P(.5, .35, .5)]
    b += f'<circle cx="{oc[0][0]:.0f}" cy="{oc[0][1]:.0f}" r="200" fill="#40e0f0" opacity=".18" filter="url(#b50)"/>'
    b += spark(*P(.05, .72, .2), 22, '#e8ffff') + spark(*P(.72, .02, .3), 18, '#e8ffff') + spark(*P(.7, .25, 0), 16, '#e8ffff')
    # frog in a parka at the rim (left of the notch), torch shining into the cut
    fx, fy = P(-.18, .93, .3)
    fs = 2.2
    hoodback = '<path d="M-46 -30 Q-58 -118 6 -122 Q70 -118 58 -30Z" fill="#23808a" stroke-width="3.4"/><path d="M-30 -100 Q6 -116 44 -100" fill="none" stroke="#5fc0c8" stroke-width="4" opacity=".7"/>'
    hood = ('<path d="M-42 -40 Q-50 -110 6 -112 Q62 -110 54 -40" fill="none" stroke="#1d2b1c" stroke-width="17"/>'
            '<path d="M-42 -40 Q-50 -110 6 -112 Q62 -110 54 -40" fill="none" stroke="#fff6ea" stroke-width="12"/>'
            '<path d="M-42 -40 Q-50 -110 6 -112 Q62 -110 54 -40" fill="none" stroke="#d9cdb8" stroke-width="3" stroke-dasharray="3 7"/>')
    coat = ('<path d="M-34 -2 Q-40 -30 -30 -40 Q6 -26 44 -40 Q50 -24 40 4 Q4 12 -34 -2Z" fill="#2a8f9a" stroke-width="3.2"/>'
            '<path d="M6 -28 L6 6" stroke-width="2.4"/><circle cx="6" cy="-18" r="2.6" fill="#f2d27a"/><circle cx="6" cy="-6" r="2.6" fill="#f2d27a"/>'
            '<path d="M-32 -38 Q6 -24 42 -38" fill="none" stroke="#fff6ea" stroke-width="7"/>')
    torch = ('<g transform="translate(62 -22) rotate(40)"><rect x="-6" y="-8" width="34" height="16" rx="4" fill="#3b3f4a" stroke-width="2.6"/>'
             '<rect x="24" y="-11" width="10" height="22" rx="3" fill="#cfd5e0" stroke-width="2.6"/><circle cx="34" cy="0" r="7" fill="#fff8d0" stroke="none"/></g>')
    tx, ty = fx + 90 * fs, fy - 2 * fs
    ex, ey = P(.35, .45, .55)
    b += f'<path d="M{tx:.0f},{ty - 10:.0f} L{ex + 90:.0f},{ey - 40:.0f} L{ex - 20:.0f},{ey + 80:.0f} L{tx:.0f},{ty + 10:.0f}Z" fill="#fff6c8" opacity=".3" filter="url(#b6)"/>'
    b += f'<ellipse cx="{fx}" cy="{fy + 4}" rx="70" ry="12" fill="#000" opacity=".4" filter="url(#b3)"/>'
    b += frog(fx, fy, fs, rot=4, look=(8, 7), mouth='O', armL='M-34 -22 q-20 0 -26 20', armR='M38 -22 q18 2 26 4',
              mid=coat, hat=hood, back=hoodback, front=torch, sleeve='#2a8f9a')
    b += '<rect width="1920" height="1080" fill="url(#cornerB)"/>'
    b += '<rect width="1920" height="1080" fill="url(#vigB)"/>'
    lines = [('OCEAN', 210, 'y'), ('UNDER', 150, 'w'), ('THE ICE?', 150, 'w')]
    return page('#160906', svg(d, b), lines, outline='#120602', top=40)


# =============================== C: Starry Night + Dragonfly ===============================
def flow(x, y, vort):
    vx, vy = 1.0, .12 * math.sin(x / 160) + .15 * math.sin(y / 90)
    for cx, cy, r, s in vort:
        dx, dy = x - cx, y - cy; dd = math.hypot(dx, dy) + 1
        w = s * math.exp(-(dd / r) ** 2) * 3.2
        vx += -dy / dd * w; vy += dx / dd * w
    return math.atan2(vy, vx)


def dragonfly(x, y, s, rnd):
    o = f'<g transform="translate({x} {y}) scale({s})" stroke-linejoin="round" stroke-linecap="round">'
    L = '#20140c'

    def rotor(px, py, sc, op=1):
        r = f'<rect x="{px - 13 * sc:.0f}" y="{py - 30}" width="{26 * sc:.0f}" height="48" rx="8" fill="#cfd3d6" stroke="{L}" stroke-width="4"/>'
        r += f'<rect x="{px - 7 * sc:.0f}" y="{py - 26}" width="{6 * sc:.0f}" height="40" rx="3" fill="#fff" opacity=".6"/>'
        for dy in (-34, 20):
            rx, ry = 128 * sc, 22 * sc
            r += f'<ellipse cx="{px}" cy="{py + dy}" rx="{rx:.0f}" ry="{ry:.0f}" fill="#fff2d0" opacity="{.3 * op:.2f}"/>'
            r += f'<ellipse cx="{px}" cy="{py + dy}" rx="{rx:.0f}" ry="{ry:.0f}" fill="none" stroke="#fffaf0" stroke-width="3" opacity="{.75 * op:.2f}"/>'
            r += f'<path d="M{px - rx * .9:.0f},{py + dy - ry * .3:.0f} A{rx:.0f},{ry:.0f} 0 0 0 {px + rx * .5:.0f},{py + dy + ry * .85:.0f}" fill="none" stroke="#fffaf0" stroke-width="6" opacity="{.6 * op:.2f}"/>'
            r += f'<path d="M{px - rx * .95:.0f},{py + dy + 4} L{px + rx * .95:.0f},{py + dy - 4}" stroke="#2b2622" stroke-width="{6 * sc:.1f}" opacity=".35"/>'
            r += f'<ellipse cx="{px}" cy="{py + dy}" rx="{12 * sc:.0f}" ry="{7 * sc:.0f}" fill="#8d877e" stroke="{L}" stroke-width="3"/>'
        return r
    # back arms + rotors (smaller, higher: perspective)
    for sx in (-1, 1):
        o += f'<path d="M{sx * 90},-40 L{sx * 225},-120" stroke="{L}" stroke-width="20"/><path d="M{sx * 90},-40 L{sx * 225},-120" stroke="#b9b2a6" stroke-width="11"/>'
        o += rotor(sx * 225, -120, .78, .8)
    # landing skids
    for sx in (-1, 1):
        o += f'<path d="M{sx * 70},50 L{sx * 110},112 M{sx * 150},40 L{sx * 140},112" stroke="{L}" stroke-width="12"/>'
        o += f'<path d="M{sx * 70},50 L{sx * 110},112 M{sx * 150},40 L{sx * 140},112" stroke="#9b958c" stroke-width="5"/>'
    o += f'<path d="M-200,116 L200,116" stroke="{L}" stroke-width="16"/><path d="M-196,114 L196,114" stroke="#c9c3b8" stroke-width="7"/>'
    # RTG power unit at the back (right side, finned)
    o += f'<g transform="translate(205 -10) rotate(-12)"><rect x="0" y="-26" width="96" height="52" rx="10" fill="#7a7068" stroke="{L}" stroke-width="5"/>'
    for k in range(6):
        o += f'<rect x="{8 + k * 15}" y="-40" width="7" height="80" rx="2" fill="#a59a8e" stroke="{L}" stroke-width="3"/>'
    o += '<circle cx="104" cy="0" r="10" fill="#ff8a3a" stroke="#20140c" stroke-width="3"/><circle cx="104" cy="0" r="22" fill="#ff8a3a" opacity=".5" filter="url(#b6)"/></g>'
    # body
    o += f'<path d="M-200,-50 Q-206,-78 -170,-82 L170,-82 Q206,-78 202,-50 L190,48 Q186,66 160,66 L-160,66 Q-186,66 -190,48Z" fill="url(#hullC)" stroke="{L}" stroke-width="6"/>'
    o += '<path d="M-186,-62 L186,-62" stroke="#fff8ea" stroke-width="5" opacity=".8"/>'
    o += '<path d="M-188,40 Q0,56 188,40" stroke="#4fd0d0" stroke-width="6" fill="none" opacity=".6"/>'  # teal rim light from the lake
    # gold thermal panel + vents
    o += f'<rect x="-150" y="-40" width="160" height="70" rx="10" fill="url(#goldC)" stroke="{L}" stroke-width="4"/>'
    for k in range(5):
        o += f'<path d="M{-140 + k * 30},-34 l14 58" stroke="#fff3c0" stroke-width="3" opacity=".45"/>'
    for k in range(4):
        o += f'<rect x="{40 + k * 30}" y="-34" width="18" height="56" rx="5" fill="#b2aaa0" stroke="{L}" stroke-width="3"/>'
    # front camera eye + lights
    o += f'<circle cx="-170" cy="6" r="22" fill="#18222a" stroke="{L}" stroke-width="5"/><circle cx="-170" cy="6" r="12" fill="#4fe0f0"/><circle cx="-175" cy="1" r="4" fill="#fff"/>'
    o += '<circle cx="-170" cy="6" r="34" fill="#4fe0f0" opacity=".5" filter="url(#b6)"/>'
    for lx in (-120, 160):
        o += f'<circle cx="{lx}" cy="50" r="6" fill="#fffbe0"/><circle cx="{lx}" cy="50" r="18" fill="#fffbe0" opacity=".5" filter="url(#b6)"/>'
    # front arms + rotors (bigger, lower)
    for sx in (-1, 1):
        o += f'<path d="M{sx * 150},-10 L{sx * 300},-46" stroke="{L}" stroke-width="24"/><path d="M{sx * 150},-10 L{sx * 300},-46" stroke="#cfc8bc" stroke-width="13"/>'
        o += rotor(sx * 300, -46, 1.0)
    # high-gain antenna dish on top (rear)
    o += f'<path d="M60,-82 L70,-130" stroke="{L}" stroke-width="12"/><path d="M60,-82 L70,-130" stroke="#bdb6aa" stroke-width="5"/>'
    o += f'<g transform="translate(78 -150) rotate(-22)"><ellipse rx="62" ry="24" fill="url(#dishC)" stroke="{L}" stroke-width="5"/><path d="M0,0 L0,-30" stroke="{L}" stroke-width="5"/><circle cx="0" cy="-32" r="6" fill="#ffe08a" stroke="{L}" stroke-width="3"/></g>'
    o += '</g>'
    return o


def make_C():
    rnd = random.Random(11)
    d = FILTERS + SATDEFS
    d += lin('skyC', [(0, '#3a1406'), (.5, '#8a3a12'), (1, '#c86a26')])
    d += lin('hullC', [(0, '#f6efe2'), (.55, '#d2c8b6'), (1, '#7c7062')])
    d += lin('goldC', [(0, '#f6d27a'), (.5, '#c9932e'), (1, '#8a5a14')], x2=1, y2=1)
    d += lin('dishC', [(0, '#fbf7ee'), (1, '#a9a196')])
    d += lin('duneC', [(0, '#7a3610'), (1, '#2a0e04')])
    d += lin('lakeC', [(0, '#1b4a4a'), (1, '#0a1f22')])
    d += rad('vigC', 960, 540, 1150, [(.6, '#000', 0), (1, '#120400', .6)])
    d += rad('textC', 380, 200, 620, [(0, '#2a0c03', .55), (1, '#2a0c03', 0)])
    d += rad('cornerC', 1920, 1080, 520, [(0, '#120400', .85), (1, '#120400', 0)])
    b = '<rect width="1920" height="1080" fill="url(#skyC)"/>'
    vort = [(1120, 330, 190, 1.0), (1330, 380, 120, -.8), (620, 260, 150, .7), (1560, 520, 110, .6)]
    pal = ['#4a1a08', '#7a2e0e', '#a8461a', '#d06a26', '#e8913a', '#f3b55a', '#f8d483']
    strokes = []
    for gy in range(0, 820, 16):
        for gx in range(0, 1960, 22):
            x = gx + rnd.uniform(-8, 8); y = gy + rnd.uniform(-6, 6)
            a = flow(x, y, vort)
            # brightness: swirl rings + horizon glow
            v = .35 + .35 * (y / 820)
            for cx, cy, r, s in vort[:2]:
                dd = math.hypot(x - cx, y - cy)
                v += .45 * math.exp(-((dd - r * .7) / (r * .25)) ** 2) * abs(s)
            v += rnd.uniform(-.18, .18)
            if x < 900 and y < 460: v *= .62
            ci = max(0, min(len(pal) - 1, int(v * len(pal))))
            col = pal[ci]
            if rnd.random() < .045 and y < 700: col = rnd.choice(['#3fb0a8', '#5fd0c4', '#2a8a86'])
            L = rnd.uniform(16, 30)
            dx, dy = math.cos(a) * L / 2, math.sin(a) * L / 2
            strokes.append(f'<path d="M{x - dx:.0f},{y - dy:.0f} L{x + dx:.0f},{y + dy:.0f}" stroke="{col}" stroke-width="{rnd.uniform(6, 9):.1f}"/>')
    b += '<g stroke-linecap="round" opacity=".95">' + ''.join(strokes) + '</g>'
    # haze glow orbs with stroke halos (the painting's "stars")
    for ox, oy, orr in ((560, 640, 30), (1720, 640, 28), (980, 120, 26), (300, 560, 28)):
        b += f'<circle cx="{ox}" cy="{oy}" r="{orr * 3}" fill="#ffd27a" opacity=".35" filter="url(#b24)"/>'
        for ring in range(3):
            rr = orr * (1.3 + ring * .55)
            for k in range(int(rr / 5)):
                t = 2 * math.pi * k / int(rr / 5) + ring
                px, py = ox + rr * math.cos(t), oy + rr * math.sin(t)
                b += f'<path d="M{px:.0f},{py:.0f} l{-math.sin(t) * 12:.0f},{math.cos(t) * 12:.0f}" stroke="{["#fff2c0", "#f8d483", "#f3b55a"][ring]}" stroke-width="6" stroke-linecap="round" opacity=".9"/>'
        b += f'<circle cx="{ox}" cy="{oy}" r="{orr}" fill="#fff4cc"/><circle cx="{ox}" cy="{oy}" r="{orr * .55:.0f}" fill="#ffffff"/>'
    # Saturn as the crescent moon (top right) with halo strokes
    b += f'<circle cx="1700" cy="170" r="200" fill="#ffd890" opacity=".45" filter="url(#b50)"/>'
    for ring in range(4):
        rr = 120 + ring * 26
        for k in range(int(rr / 6)):
            t = 2 * math.pi * k / int(rr / 6) + ring * .3
            px, py = 1700 + rr * math.cos(t), 170 + rr * math.sin(t)
            b += f'<path d="M{px:.0f},{py:.0f} l{-math.sin(t) * 16:.0f},{math.cos(t) * 16:.0f}" stroke="{["#fff2c0", "#f8d483", "#f3b55a", "#e8913a"][ring]}" stroke-width="7" stroke-linecap="round" opacity=".85"/>'
    b += saturn(1700, 170, 72, tilt=-20, glow=False)
    # distant ridge + dunes
    b += f'<path d="{smooth([(0, 760), (240, 720), (520, 745), (800, 700), (1100, 735), (1400, 690), (1700, 730), (1920, 700)])} L1920,1080 L0,1080Z" fill="#4a1c08"/>'
    b += f'<path d="{smooth([(0, 760), (240, 720), (520, 745), (800, 700), (1100, 735), (1400, 690), (1700, 730), (1920, 700)])}" fill="none" stroke="#f3b55a" stroke-width="4" opacity=".7"/>'
    # methane lake reflecting the sky
    b += f'<path d="{smooth([(420, 800), (700, 780), (1100, 790), (1500, 785), (1700, 810), (1500, 850), (1000, 860), (600, 850)], True)}" fill="url(#lakeC)"/>'
    for _ in range(50):
        x = rnd.uniform(520, 1600); y = rnd.uniform(792, 850)
        b += f'<path d="M{x:.0f},{y:.0f} l{rnd.uniform(20, 60):.0f},0" stroke="{rnd.choice(["#f3b55a", "#5fd0c4", "#e8913a"])}" stroke-width="4" stroke-linecap="round" opacity="{rnd.uniform(.3, .8):.2f}"/>'
    # Saturn & orb reflections
    b += '<path d="M1600,800 l40,0 M1610,816 l28,0 M1616,832 l16,0" stroke="#f8d483" stroke-width="5" stroke-linecap="round" opacity=".8"/>'
    # foreground dunes with stroke texture
    for k, (yy, c) in enumerate(((870, '#6a2a0c'), (940, '#4a1a06'), (1010, '#2e0f04'))):
        pts = [(-20, yy + 20)] + [(x, yy + 30 * math.sin(x / 210 + k * 1.7) + 10 * math.sin(x / 70)) for x in range(0, 2000, 120)]
        b += f'<path d="{smooth(pts)} L1960,1080 L-20,1080Z" fill="{c}"/>'
        b += f'<path d="{smooth(pts)}" fill="none" stroke="#e8913a" stroke-width="4" opacity="{.6 - k * .15:.2f}"/>'
        for _ in range(120):
            x = rnd.uniform(0, 1920); y = rnd.uniform(yy + 30, min(1080, yy + 120))
            b += f'<path d="M{x:.0f},{y:.0f} q14 -5 28 0" stroke="#e8913a" stroke-width="4" fill="none" opacity="{rnd.uniform(.1, .35):.2f}" stroke-linecap="round"/>'
    # cypress -> a dark flame-shaped ice spire, left foreground
    sp = [(70, 1080), (60, 950), (100, 840), (80, 740), (130, 640), (125, 560), (175, 480), (200, 440), (225, 500), (255, 580), (280, 680), (270, 780), (330, 880), (350, 1000), (370, 1080)]
    b += f'<path d="{smooth(sp)}Z" fill="#14140a"/>'
    for _ in range(170):
        y = rnd.uniform(470, 1075); half = 10 + (y - 440) / 640 * 135
        x = 215 + rnd.uniform(-half, half) * .82
        bend = rnd.uniform(-14, 14); L = rnd.uniform(30, 60)
        b += f'<path d="M{x:.0f},{y:.0f} q{bend:.0f},{-L / 2:.0f} {bend * .3:.0f},{-L:.0f}" fill="none" stroke="{rnd.choice(["#2a3a1c", "#3e4a20", "#1c2c22", "#24504a", "#5a3a14", "#16201a"])}" stroke-width="{rnd.uniform(6, 10):.0f}" stroke-linecap="round"/>'
    b += f'<path d="{smooth(sp)}" fill="none" stroke="#e8913a" stroke-width="3" opacity=".4"/>'
    # downwash dust + shadow under the Dragonfly
    DX, DY, DS = 1190, 580, 1.25
    b += f'<ellipse cx="{DX}" cy="900" rx="330" ry="34" fill="#160600" opacity=".55" filter="url(#b12)"/>'
    b += f'<ellipse cx="{DX}" cy="880" rx="420" ry="60" fill="#f3b55a" opacity=".25" filter="url(#b24)"/>'
    for k in range(18):
        a = rnd.uniform(0, math.pi)
        b += f'<path d="M{DX + math.cos(a) * 250:.0f},{880 - math.sin(a) * 30:.0f} q{math.cos(a) * 80:.0f} -30 {math.cos(a) * 160:.0f} -10" stroke="#f8d483" stroke-width="5" fill="none" opacity=".35" stroke-linecap="round"/>'
    # glow behind the rotorcraft
    b += f'<ellipse cx="{DX}" cy="{DY - 40}" rx="480" ry="260" fill="#ffd890" opacity=".35" filter="url(#b50)"/>'
    b += dragonfly(DX, DY, DS, rnd)
    # frog riding on the deck, gripping the antenna mast, scarf flying
    fx, fy, fs = DX - 40, DY - 82 * DS, 2.25
    scarf = ('<path d="M-30 -24 Q6 -12 42 -24 L44 -14 Q6 0 -32 -14Z" fill="#2fb0a8" stroke-width="3"/>'
             '<path d="M-28 -20 Q-70 -40 -110 -24 Q-90 -12 -110 4 Q-66 -6 -30 -12Z" fill="#2fb0a8" stroke-width="3"/>'
             '<path d="M-60 -26 l6 14 M-84 -26 l6 14" stroke="#e8fffa" stroke-width="3"/>')
    b += frog(fx, fy, fs, rot=-6, look=(-8, -2), mouth='O', helmet=True, mid=scarf,
              armL='M-34 -22 q-22 -14 -30 -40', armR='M38 -22 q22 -6 34 -26')
    b += spark(1460, 330, 22) + spark(900, 640, 16) + spark(1560, 440, 14, '#e8fbff')
    b += '<rect width="1920" height="1080" fill="url(#cornerC)"/>'
    b += '<rect width="1920" height="1080" fill="url(#vigC)"/>'
    lines = [('FLYING AT', 150, 'w'), ('-180°C', 230, 'y')]
    return page('#3a1406', svg(d, b), lines, outline='#1a0802', top=40)


if __name__ == '__main__':
    which = sys.argv[1:] or ['A', 'B', 'C']
    for n in which:
        open(os.path.join(HERE, f'{n}.html'), 'w').write(globals()[f'make_{n}']())
    print('ok')
