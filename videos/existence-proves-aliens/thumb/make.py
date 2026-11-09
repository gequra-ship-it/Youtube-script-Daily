# Thumbnails A-C for existence-proves-aliens (guideline 16-6 / 16-8, brief tools/briefs/thumb_art.md). Run: python3 videos/existence-proves-aliens/thumb/make.py
# A  WHERE IS / EVERYBODY?   homage: Close Encounters of the Third Kind poster (lone straight road at night running to a horizon that
#                            glows from behind); the frog stands at the roadside shading its eyes. Question form = Fermi's lunch
#                            question quoted in S41 ("where is everybody?"); no claim that anything is there.
# B  ONE / IS NOT / ZERO     intuitive: the script's handful-of-sand image (S21-S24): a hand scoops wet sand on an endless night
#                            shoreline and a tiny glowing sea creature wriggles in it; the frog rides on the forearm. S24-S25
#                            ("a sample size of one is infinitely greater than a sample size of zero").
# C  THE CLUE / IS YOU       intuitive: a giant human head made of stars and a spiral galaxy rises over a dark hill, the Milky Way
#                            streams into it (S07-S09 made of star material, S64 "the cosmos waking up"); detective frog with a
#                            magnifying glass looks at it. Script's last line S66 "The clue is you."
import os, sys, math, random
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', '..', 'tools'))
from thumb_lib import page, svg, lin, rad, spark, blobs

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


from figlib import hand


def starfield(rnd, n, x0, x1, y0, y1, col='#eaf2ff', rmax=2.6, omax=.9):
    o = ''
    for _ in range(n):
        r = rnd.choice([1.0, 1.4, 1.9, rmax])
        o += f'<circle cx="{rnd.uniform(x0, x1):.0f}" cy="{rnd.uniform(y0, y1):.0f}" r="{r}" fill="{col}" opacity="{rnd.uniform(.2, omax):.2f}"/>'
    return o


def milky(rnd, pts, width, n, col='#dfe8ff', haze='#7f8fd8'):
    """a Milky Way band along pts: soft haze + many small stars + dark dust lane"""
    o = f'<path d="{smooth(pts)}" fill="none" stroke="{haze}" stroke-width="{width * 1.6:.0f}" opacity=".16" filter="url(#b50)"/>'
    o += f'<path d="{smooth(pts)}" fill="none" stroke="{col}" stroke-width="{width * .7:.0f}" opacity=".14" filter="url(#b24)"/>'
    samp = cr_sample(pts, 30)
    for _ in range(n):
        x, y = samp[rnd.randrange(len(samp))]
        g = rnd.gauss(0, width * .35)
        o += f'<circle cx="{x + g * .6:.0f}" cy="{y + g:.0f}" r="{rnd.choice([.9, 1.2, 1.6, 2.2])}" fill="{col}" opacity="{rnd.uniform(.25, .9):.2f}"/>'
    o += f'<path d="{smooth([(x + 14, y + 10) for x, y in pts])}" fill="none" stroke="#05040f" stroke-width="{width * .18:.0f}" opacity=".35" filter="url(#b12)"/>'
    return o


# =========================== A: Close Encounters poster homage ===========================
def make_A():
    rnd = random.Random(11)
    VX, HY = 1190, 772
    d = FILTERS
    d += lin('skyA', [(0, '#03040d'), (.45, '#0a1236'), (.8, '#22306e'), (1, '#4d5fa8')])
    d += rad('glowA', VX, HY, 900, [(0, '#ffffff', 1), (.06, '#fffbe8', .95), (.16, '#d8ecff', .7), (.38, '#6f8ee0', .32), (.7, '#3a3a9a', .1), (1, '#20206a', 0)])
    d += lin('roadA', [(0, '#7f90c8'), (.12, '#3a4672'), (.5, '#141a30'), (1, '#07090f')])
    d += lin('groundA', [(0, '#1a2550'), (.15, '#0c1230'), (1, '#020308')])
    d += rad('vigA', 960, 540, 1150, [(0, '#000', 0), (.65, '#000', 0), (1, '#000', .7)])
    b = '<rect width="1920" height="1080" fill="url(#skyA)"/>'
    b += milky(rnd, [(1960, 40), (1600, 200), (1330, 420), (1210, 700)], 150, 900)
    b += starfield(rnd, 520, 0, 1920, 0, 720)
    b += '<rect width="1920" height="1080" fill="url(#glowA)"/>'
    # light rays fanning up from behind the horizon
    for a in (-78, -62, -48, -33, -18, -4, 12, 28, 44, 60, 76):
        r = math.radians(a - 90); L = 1100; w = 4.5
        x1, y1 = VX + math.cos(math.radians(a - 90 - w)) * L, HY + math.sin(math.radians(a - 90 - w)) * L
        x2, y2 = VX + math.cos(math.radians(a - 90 + w)) * L, HY + math.sin(math.radians(a - 90 + w)) * L
        b += f'<path d="M{VX},{HY} L{x1:.0f},{y1:.0f} L{x2:.0f},{y2:.0f}Z" fill="#e6f2ff" opacity="{.05 + .04 * (abs(a) < 40):.2f}" filter="url(#b12)"/>'
    b += f'<ellipse cx="{VX}" cy="{HY}" rx="760" ry="70" fill="#eef6ff" opacity=".55" filter="url(#b24)"/>'
    b += f'<ellipse cx="{VX}" cy="{HY - 10}" rx="230" ry="120" fill="#ffffff" opacity=".9" filter="url(#b50)"/>'
    b += f'<ellipse cx="{VX}" cy="{HY}" rx="120" ry="26" fill="#fff" filter="url(#b6)"/>'
    # low far hills on the horizon with lit rims
    hills = [(-20, HY + 4), (220, HY - 18), (470, HY - 6), (700, HY - 30), (930, HY - 8), (1080, HY - 3), (1300, HY - 2), (1460, HY - 22), (1700, HY - 10), (1940, HY - 34)]
    b += f'<path d="{smooth(hills)} L1940,{HY + 40} L-20,{HY + 40}Z" fill="#0d1330"/>'
    b += f'<path d="{smooth(hills)}" fill="none" stroke="#cfe2ff" stroke-width="3" opacity=".55"/>'
    b += f'<rect x="0" y="{HY + 2}" width="1920" height="{1080 - HY}" fill="url(#groundA)"/>'
    # desert scrub texture on the ground
    for _ in range(260):
        y = HY + 8 + (rnd.random() ** 1.7) * (1080 - HY)
        k = (y - HY) / (1080 - HY)
        x = rnd.uniform(0, 1920)
        b += f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{2 + 26 * k:.1f}" ry="{1 + 6 * k:.1f}" fill="#000" opacity="{.25 + .3 * k:.2f}"/>'
    # the road
    LB, RB = 560, 1820
    b += f'<path d="M{VX - 6},{HY} L{VX + 6},{HY} L{RB},1080 L{LB},1080Z" fill="url(#roadA)"/>'
    b += f'<path d="M{VX - 6},{HY} L{LB},1080 M{VX + 6},{HY} L{RB},1080" stroke="#c8d8ff" stroke-width="5" opacity=".7"/>'
    b += f'<path d="M{VX - 6},{HY} L{LB + 70},1080 M{VX + 6},{HY} L{RB - 70},1080" stroke="#f6e7b0" stroke-width="3" opacity=".25"/>'
    # perspective centre dashes
    t = .02
    while t < 1.05:
        t2 = t + .045 * (1 + t * 3) * .35
        y1, y2 = HY + (1080 - HY) * t ** 1.6, HY + (1080 - HY) * min(t2, 1.1) ** 1.6
        cx1 = VX + (VX + (LB + RB) / 2 - 2 * VX) * 0  # straight
        w1, w2 = 1 + 12 * t, 1 + 12 * t2
        b += f'<path d="M{VX - w1 / 2:.1f},{y1:.1f} L{VX + w1 / 2:.1f},{y1:.1f} L{VX + w2 / 2:.1f},{y2:.1f} L{VX - w2 / 2:.1f},{y2:.1f}Z" fill="#fff4cc" opacity=".85"/>'
        t = t2 + .05 * (1 + t * 3) * .35
    # glow sheen on the road toward the horizon
    b += f'<path d="M{VX - 6},{HY} L{VX + 6},{HY} L{VX + 160},960 L{VX - 160},960Z" fill="#dfe9ff" opacity=".18" filter="url(#b24)"/>'
    # roadside fence posts receding
    for k in range(12):
        tt = (k + 1) / 12.5
        y = HY + (1080 - HY) * tt ** 1.5
        x = VX + (LB - 150 - VX) * tt ** 1.5
        h = 6 + 120 * tt ** 1.5
        b += f'<rect x="{x - 1 - 4 * tt:.0f}" y="{y - h:.0f}" width="{2 + 8 * tt:.1f}" height="{h:.0f}" fill="#05070f"/>'
        b += f'<rect x="{x + 3 * tt:.0f}" y="{y - h:.0f}" width="{1 + 2 * tt:.1f}" height="{h:.0f}" fill="#9fb6ff" opacity=".45"/>'
    b += f'<path d="{" ".join(f"M{VX + (LB - 150 - VX) * ((k + 1) / 12.5) ** 1.5:.0f},{HY + (1080 - HY) * ((k + 1) / 12.5) ** 1.5 - (6 + 120 * ((k + 1) / 12.5) ** 1.5) * .8:.0f} L{VX + (LB - 150 - VX) * ((k + 2) / 12.5) ** 1.5:.0f},{HY + (1080 - HY) * ((k + 2) / 12.5) ** 1.5 - (6 + 120 * ((k + 2) / 12.5) ** 1.5) * .8:.0f}" for k in range(11))}" stroke="#05070f" stroke-width="3" fill="none"/>'
    # frog at the roadside, backlit, shading its eyes
    fx, fy, fs = 600, 1010, 2.75
    b += f'<ellipse cx="{fx + 10}" cy="{fy - 120}" rx="200" ry="190" fill="#bcd4ff" opacity=".28" filter="url(#b50)"/>'
    b += f'<ellipse cx="{fx + 10}" cy="{fy + 12}" rx="120" ry="18" fill="#000" opacity=".6" filter="url(#b6)"/>'
    pack = '<path d="M-38 -48 q-20 4 -20 30 q0 18 14 20 l12 -2Z" fill="#c2603a" stroke-width="3.4"/><path d="M-52 -30 h12" stroke-width="3"/>'
    strap = '<path d="M-30 -50 q20 22 2 46" fill="none" stroke="#7a3520" stroke-width="5"/>'
    b += frog(fx, fy, fs, rot=4, look=(5, -2), mouth='O',
              armR='M38 -22 q30 -30 -6 -70', armL='M-34 -22 q-16 8 -16 26')
    # cool rim light on the frog's right side
    b += f'<path d="M{fx + 60},{fy - 60} q20 -70 -20 -150" fill="none" stroke="#e8f2ff" stroke-width="7" opacity=".55" filter="url(#b3)"/>'
    b += spark(1420, 300, 22, '#ffffff') + spark(1700, 520, 16, '#e8f2ff') + spark(980, 600, 14)
    b += '<rect width="1920" height="1080" fill="url(#vigA)"/>'
    lines = [('WHERE IS', 140, 'w'), ('EVERYBODY?', 158, 'y')]
    return page('#050818', svg(d, b), lines, outline='#03040e', top=44)


# =========================== B: the handful of sand ===========================
def make_B():
    rnd = random.Random(22)
    HY = 600
    d = FILTERS
    d += lin('skyB', [(0, '#02060f'), (.6, '#0a2236'), (1, '#1c4a5e')])
    d += lin('seaB', [(0, '#0f3346'), (1, '#04121c')])
    d += lin('sandB', [(0, '#3a3a40'), (.4, '#2a2622'), (1, '#120e0b')])
    d += rad('crB', 1085, 548, 420, [(0, '#eafff6', .95), (.12, '#7ff5d8', .6), (.45, '#2fb8a8', .18), (1, '#0c4a58', 0)])
    d += rad('vigB', 960, 540, 1150, [(0, '#000', 0), (.62, '#000', 0), (1, '#000', .72)])
    d += lin('skinB', [(0, '#f0c39a'), (1, '#b07c58')])
    b = '<rect width="1920" height="1080" fill="url(#skyB)"/>'
    b += milky(rnd, [(-40, 120), (500, 60), (1100, 140), (1960, 330)], 140, 900, col='#e8f6ff', haze='#6fb0c8')
    b += starfield(rnd, 420, 0, 1920, 0, HY - 10)
    b += f'<rect x="0" y="{HY}" width="1920" height="{1080 - HY}" fill="url(#seaB)"/>'
    b += f'<path d="M0,{HY} L1920,{HY}" stroke="#7fc8d8" stroke-width="2" opacity=".5"/>'
    # milky-way glitter on the sea
    for _ in range(140):
        x = rnd.uniform(0, 1920); y = rnd.uniform(HY + 4, 760)
        b += f'<rect x="{x:.0f}" y="{y:.0f}" width="{rnd.uniform(6, 40):.0f}" height="2" fill="#bfe8f0" opacity="{rnd.uniform(.1, .45):.2f}"/>'
    # endless shoreline receding to the left, glowing surf lines
    shore = [(1970, 900), (1500, 770), (1000, 690), (600, 645), (250, 622), (-50, 612)]
    b += f'<path d="{smooth(shore)} L-50,1090 L1970,1090Z" fill="url(#sandB)"/>'
    for k, (off, op, wd) in enumerate(((0, .95, 7), (-18, .6, 5), (-40, .4, 4), (-70, .25, 3))):
        pts = [(x, y + off * (y - 600) / 300) for x, y in shore]
        b += f'<path d="{smooth(pts)}" fill="none" stroke="#7ff5d8" stroke-width="{wd * 4}" opacity="{op * .35:.2f}" filter="url(#b12)"/>'
        b += f'<path d="{smooth(pts)}" fill="none" stroke="#c8fff0" stroke-width="{wd}" opacity="{op:.2f}"/>'
    # wet sand reflection + footprints along the beach
    b += f'<path d="{smooth([(x, y + 14 * (y - 600) / 300) for x, y in shore])}" fill="none" stroke="#3fd0c0" stroke-width="40" opacity=".12" filter="url(#b24)"/>'
    for k in range(9):
        tt = k / 9
        x = 380 + 560 * tt ** 1.2; y = 650 + 300 * tt ** 1.8
        s = .3 + tt
        b += f'<ellipse cx="{x + (14 if k % 2 else -14) * s:.0f}" cy="{y:.0f}" rx="{9 * s:.1f}" ry="{4 * s:.1f}" fill="#000" opacity=".35"/>'
    for _ in range(160):
        y = 640 + rnd.random() ** 1.5 * 440; x = rnd.uniform(0, 1920)
        if y > 640 + (1920 - x) * .0:  # sparkles in the sand
            b += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{rnd.choice([1, 1.5, 2])}" fill="#bff6ea" opacity="{rnd.uniform(.1, .5):.2f}"/>'
    # creature glow behind the hand
    b += '<rect width="1920" height="1080" fill="url(#crB)"/>'
    # the arm (sleeve) from bottom-left to the wrist
    WX, WY, HS = 1010, 820, 330
    sl = f'M{WX - 120},{WY + 30} L{WX - 520},{WY + 380}'
    b += f'<path d="{sl}" stroke="#0a1418" stroke-width="236" stroke-linecap="round"/>'
    b += f'<path d="{sl}" stroke="#2b4a66" stroke-width="222" stroke-linecap="round"/>'
    b += f'<path d="M{WX - 190},{WY - 50} L{WX - 560},{WY + 270}" stroke="#4f7ea4" stroke-width="30" opacity=".6" filter="url(#b6)"/>'
    b += f'<path d="M{WX - 130},{WY - 60} q-26 100 26 186" fill="none" stroke="#0a1418" stroke-width="10"/>'  # cuff
    b += f'<path d="M{WX - 115},{WY - 40} q-20 80 22 150" fill="none" stroke="#6d9cc4" stroke-width="5" opacity=".7"/>'
    # the hand (figlib cupped palm), fingers to the right
    b += hand('cup', WX, WY, size=HS, side='L', skin='#e2b088', line='#2e2218', lw=8)
    sc = HS / 30
    P = lambda u, v: (WX + u * sc, WY + v * sc)
    # wet sand heaped in the palm, spilling a little between fingers
    mound = [P(-17, -11), P(-15, -21), P(-9, -28), P(-3, -32), P(4, -33), P(10, -30), P(15, -23), P(18, -13), P(12, -10), P(2, -9), P(-9, -9)]
    b += f'<path d="{smooth(mound, closed=True)}" fill="#000" opacity=".35" transform="translate(10 14)" filter="url(#b6)"/>'
    b += f'<path d="{smooth(mound, closed=True)}" fill="#9c845c" stroke="#2e2218" stroke-width="6"/>'
    b += f'<path d="{smooth([P(-12, -20), P(-4, -27), P(4, -29), P(12, -25)])}" fill="none" stroke="#d8c08c" stroke-width="10" opacity=".7"/>'
    for _ in range(90):
        u, v = rnd.uniform(-12, 14), rnd.uniform(-27, -15)
        x, y = P(u, v)
        b += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{rnd.choice([1.5, 2, 3])}" fill="{rnd.choice(["#6f5a3a", "#c8ae7a", "#7a6444"])}" opacity=".8"/>'
    for k in range(3):
        x, y = P(-4 + k * 9, -10)
        b += f'<path d="M{x:.0f},{y + 40:.0f} q4 30 0 60" stroke="#b0966a" stroke-width="5" stroke-dasharray="4 10" fill="none" opacity=".7"/>'
    # tiny glowing sea creature wriggling on the sand
    CX, CY = P(2, -34)
    b += f'<circle cx="{CX:.0f}" cy="{CY:.0f}" r="150" fill="#7ff5d8" opacity=".35" filter="url(#b50)"/>'
    b += f'<circle cx="{CX:.0f}" cy="{CY:.0f}" r="60" fill="#d8fff4" opacity=".55" filter="url(#b24)"/>'
    body = [(CX - 100, CY + 46), (CX - 60, CY + 6), (CX - 14, CY + 4), (CX + 32, CY - 16), (CX + 74, CY - 2)]
    samp = cr_sample(body, 6)
    for i, (x, y) in enumerate(samp):
        r = 21 - abs(i - len(samp) * .6) * .7
        b += f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{max(r, 8):.1f}" fill="#58e6c8" stroke="#0a3a40" stroke-width="3"/>'
    for i, (x, y) in enumerate(samp):
        r = 21 - abs(i - len(samp) * .6) * .7
        b += f'<circle cx="{x - 2:.1f}" cy="{y - 5:.1f}" r="{max(r, 8) * .45:.1f}" fill="#e8fff8" opacity=".85"/>'
        if i % 2 == 0:
            b += f'<path d="M{x:.0f},{y + max(r, 6):.0f} l-4 9 M{x:.0f},{y - max(r, 6):.0f} l-3 -9" stroke="#bffaea" stroke-width="2.5"/>'
    hx, hy = samp[-1]
    b += f'<circle cx="{hx + 14:.0f}" cy="{hy:.0f}" r="21" fill="#58e6c8" stroke="#0a3a40" stroke-width="3"/>'
    b += f'<circle cx="{hx + 20:.0f}" cy="{hy - 5:.0f}" r="6" fill="#062428"/><circle cx="{hx + 21:.0f}" cy="{hy - 7:.0f}" r="2.2" fill="#fff"/>'
    b += f'<path d="M{hx + 28:.0f},{hy - 16:.0f} q18 -34 46 -30 M{hx + 20:.0f},{hy - 18:.0f} q2 -40 28 -48" fill="none" stroke="#bffaea" stroke-width="3"/>'
    b += f'<path d="M{CX - 90:.0f},{CY + 40:.0f} q-14 -8 -28 0 M{CX + 90:.0f},{CY - 40:.0f} q14 -6 22 4" stroke="#c8fff0" stroke-width="3" fill="none" opacity=".8"/>'
    # teal rim light on the fingers from the creature
    b += f'<path d="{smooth([P(16, -20), P(30, -22), P(40, -30)])}" fill="none" stroke="#9ff8e4" stroke-width="7" opacity=".55" filter="url(#b3)"/>'
    b += spark(CX + 120, CY - 90, 20, '#e8fff8') + spark(CX - 150, CY - 60, 14, '#e8fff8') + spark(CX + 40, CY - 150, 12)
    # frog riding on the forearm, peering at the creature
    fx, fy, fs = 668, 905, 2.4
    b += frog(fx, fy, fs, rot=-14, look=(5, -3), mouth='O',
              armR='M38 -22 q20 -10 28 -28', armL='M-34 -22 q-12 10 -10 26',
              legs=((-20, -6, -24, 4, -10), (20, -6, 20, 4, -10)))
    b += '<rect width="1920" height="1080" fill="url(#vigB)"/>'
    lines = [('ONE', 230, 'y'), ('IS NOT', 128, 'w'), ('ZERO', 190, 'w')]
    return page('#04121c', svg(d, b), lines, outline='#03121a', top=26)


# =========================== C: the head made of stars ===========================
def make_C():
    rnd = random.Random(33)
    d = FILTERS
    d += lin('skyC', [(0, '#05030f'), (.55, '#140a34'), (1, '#2a1250')])
    d += rad('headC', 1360, 420, 620, [(0, '#3b2a8a', .95), (.5, '#22185e', .9), (1, '#0d0a2a', .85)])
    d += rad('galC', 1390, 340, 260, [(0, '#fff6d6', 1), (.12, '#f2d27a', .85), (.4, '#d06ac8', .35), (1, '#5a2aa0', 0)])
    d += rad('vigC', 960, 540, 1150, [(0, '#000', 0), (.62, '#000', 0), (1, '#000', .7)])
    b = '<rect width="1920" height="1080" fill="url(#skyC)"/>'
    # rich nebula clouds: magenta, cyan, gold, violet (kept off the text corner by xmin)
    for col, n, x0, x1, y0, y1, o0, o1, r0, r1 in (('#e0309a', 9, 760, 1900, 0, 900, .22, .42, 140, 340), ('#16c8e8', 8, 760, 1900, 100, 1000, .18, .36, 130, 300),
                                                    ('#ffb62e', 6, 1000, 1900, 60, 700, .16, .32, 100, 240), ('#7a3cff', 8, 500, 1900, 0, 1000, .22, .4, 160, 340),
                                                    ('#ff5a7a', 4, 1100, 1900, 500, 1000, .14, .28, 120, 260)):
        b += blobs(n, x0, y0, x1, y1, col, o0, o1, r0, r1).replace('<ellipse', '<ellipse filter="url(#b50)"')
    b += starfield(rnd, 900, 0, 1920, 0, 1000, rmax=3.4, omax=1)
    # light rays from the galaxy in the head
    for a in range(0, 360, 20):
        w = 3.2
        x1, y1 = 1390 + math.cos(math.radians(a - w)) * 1500, 340 + math.sin(math.radians(a - w)) * 1500
        x2, y2 = 1390 + math.cos(math.radians(a + w)) * 1500, 340 + math.sin(math.radians(a + w)) * 1500
        b += f'<path d="M1390,340 L{x1:.0f},{y1:.0f} L{x2:.0f},{y2:.0f}Z" fill="#ffe6ff" opacity=".10" filter="url(#b12)"/>'
    # three big Milky Way streams flowing into the head
    b += milky(rnd, [(1960, -40), (1820, 80), (1660, 190), (1520, 290), (1420, 340)], 200, 1100, col='#fff2d8', haze='#ff7ad8')
    b += milky(rnd, [(1960, 330), (1820, 330), (1700, 360), (1580, 400)], 150, 600, col='#d8f6ff', haze='#2fd8f0')
    b += milky(rnd, [(900, -30), (1060, 90), (1220, 180), (1340, 250)], 130, 600, col='#fff6c8', haze='#ffc23a')
    b += f'<ellipse cx="1390" cy="340" rx="760" ry="520" fill="#ff8ae0" opacity=".16" filter="url(#b80)"/>'
    # head in profile facing left
    prof = [(1250, 1020), (1236, 880), (1170, 838), (1110, 812), (1078, 770), (1083, 726), (1064, 700), (1072, 676), (1058, 650),
            (1076, 626), (1066, 596), (1022, 560), (1046, 520), (1092, 446), (1100, 370), (1130, 260), (1210, 160), (1340, 108),
            (1490, 120), (1610, 200), (1680, 330), (1690, 470), (1650, 600), (1580, 700), (1560, 820), (1580, 1020)]
    hp = smooth(prof, closed=True, t=.45)
    d += f'<clipPath id="hdC"><path d="{hp}"/></clipPath>'
    b += f'<path d="{hp}" fill="none" stroke="#ff9af0" stroke-width="70" opacity=".5" filter="url(#b50)"/>'
    b += f'<path d="{hp}" fill="none" stroke="#5fe8ff" stroke-width="34" opacity=".6" filter="url(#b24)"/>'
    b += f'<path d="{hp}" fill="#9a7aff" opacity=".5" filter="url(#b50)"/>'
    b += f'<path d="{hp}" fill="url(#headC)"/>'
    inner = f'<g clip-path="url(#hdC)">'
    inner += blobs(14, 1100, 150, 1700, 950, '#b04ab8', .1, .25, 60, 180).replace('<ellipse', '<ellipse filter="url(#b24)"')
    inner += blobs(10, 1100, 150, 1700, 950, '#2fb0c8', .08, .2, 60, 160).replace('<ellipse', '<ellipse filter="url(#b24)"')
    inner += starfield(rnd, 700, 1000, 1720, 90, 1040, col='#fff8e8', rmax=3.2, omax=1)
    # spiral galaxy in the brain
    GX, GY = 1390, 340
    inner += f'<ellipse cx="{GX}" cy="{GY}" rx="300" ry="190" fill="url(#galC)"/>'
    for arm in range(2):
        for i in range(260):
            th = i / 260 * 3.4 * math.pi + arm * math.pi
            rr = 12 + i * .95
            x = GX + math.cos(th) * rr * 1.25 + rnd.gauss(0, 7); y = GY + math.sin(th) * rr * .72 + rnd.gauss(0, 5)
            inner += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{rnd.choice([1.2, 1.8, 2.4, 3])}" fill="{rnd.choice(["#fff6d6", "#f2d27a", "#ffd0f0", "#c8f0ff"])}" opacity="{rnd.uniform(.4, 1):.2f}"/>'
    inner += f'<ellipse cx="{GX}" cy="{GY}" rx="60" ry="38" fill="#fffbe8" filter="url(#b12)"/>'
    inner += f'<ellipse cx="{GX}" cy="{GY}" rx="26" ry="16" fill="#fff"/>'
    # heart-like warm star cluster in the chest/neck
    inner += f'<circle cx="1400" cy="960" r="80" fill="#f2d27a" opacity=".25" filter="url(#b24)"/>'
    inner += '</g>'
    b += inner
    # glowing eye (a star) and neon rim along the profile
    EX, EY = 1150, 440
    b += f'<circle cx="{EX}" cy="{EY}" r="46" fill="#cfefff" opacity=".5" filter="url(#b12)"/>'
    b += f'<path d="M{EX - 26},{EY} q26 -18 52 2 q-26 14 -52 -2Z" fill="#e8f8ff"/>'
    b += f'<circle cx="{EX + 2}" cy="{EY}" r="9" fill="#2a1a6a"/>' + spark(EX + 2, EY, 26, '#ffffff')
    b += f'<path d="M{EX - 30},{EY - 34} q28 -14 60 -4" fill="none" stroke="#cfe8ff" stroke-width="5" opacity=".8"/>'
    b += f'<path d="{hp}" fill="none" stroke="#7fe8ff" stroke-width="22" opacity=".7" filter="url(#b6)"/>'
    b += f'<path d="{hp}" fill="none" stroke="#ffffff" stroke-width="5" opacity="1"/>'
    # ear hint
    b += f'<path d="M1490,470 q40 -30 50 30 q4 50 -40 70" fill="none" stroke="#bfe8ff" stroke-width="4" opacity=".6"/>'
    # stardust streaming from the Milky Way into the head
    for k in range(60):
        tt = rnd.random()
        x = 1900 - tt * 420 + rnd.gauss(0, 30); y = 20 + tt * 300 + rnd.gauss(0, 30)
        b += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{rnd.choice([1.5, 2.5, 3.5])}" fill="#fff2c8" opacity="{rnd.uniform(.4, .95):.2f}"/>'
    # dark hill in front
    hill = [(-30, 1000), (300, 965), (650, 975), (950, 960), (1250, 975), (1600, 1000), (1950, 990)]
    b += f'<path d="{smooth(hill)} L1950,1090 L-30,1090Z" fill="#07040e"/>'
    b += f'<path d="{smooth(hill)}" fill="none" stroke="#9a7aff" stroke-width="4" opacity=".5"/>'
    for _ in range(70):
        x = rnd.uniform(0, 1900); y = 985 + rnd.uniform(-10, 20)
        b += f'<path d="M{x:.0f},{y:.0f} l{rnd.uniform(-5, 5):.0f},{-rnd.uniform(8, 22):.0f}" stroke="#07040e" stroke-width="3"/>'
    # detective frog with a magnifying glass on the hill
    fx, fy, fs = 760, 978, 2.55
    b += f'<ellipse cx="{fx + 60}" cy="{fy - 140}" rx="220" ry="200" fill="#8a6aff" opacity=".22" filter="url(#b50)"/>'
    lens = ('<path d="M66 -70 L92 -104" stroke-width="9"/><path d="M66 -70 L92 -104" stroke="#8a5a2a" stroke-width="5"/>'
            '<circle cx="112" cy="-130" r="32" fill="#cff4ff" fill-opacity=".35" stroke="#e8c070" stroke-width="7"/>'
            '<circle cx="112" cy="-130" r="32" fill="none" stroke-width="2"/>'
            '<path d="M96 -146 q12 -12 28 -8" fill="none" stroke="#fff" stroke-width="4" opacity=".9"/>'
            '<circle cx="118" cy="-122" r="3" fill="#fff6d6" stroke="none"/><circle cx="104" cy="-128" r="2" fill="#fff6d6" stroke="none"/>'
            '<circle cx="122" cy="-138" r="2.2" fill="#fff6d6" stroke="none"/>')
    cape = '<path d="M-36 -30 q-18 26 -8 34 l84 -2 q8 -10 -6 -34" fill="#8a6a44" stroke-width="3.4" opacity=".0"/>'
    hat = ('<path d="M-14 -86 q20 -26 44 0 q-2 6 -22 6 q-20 0 -22 -6Z" fill="#9a7a50" stroke-width="3.2"/>'
           '<path d="M-14 -86 q22 6 44 0" fill="none" stroke="#5a4428" stroke-width="3"/><path d="M8 -102 l0 -6" stroke-width="3"/>')
    b += frog(fx, fy, fs, rot=-4, look=(5, -3), mouth='O', mid=lens, hat=hat,
              armR='M38 -22 q24 -10 28 -48', armL='M-34 -22 q-14 8 -16 24')
    b += spark(1000, 860, 14, '#e8f2ff') + spark(1770, 640, 18) + spark(980, 120, 16, '#e8f2ff')
    b += '<rect width="1920" height="1080" fill="url(#vigC)"/>'
    lines = [('THE CLUE', 150, 'w'), ('IS', 120, 'w'), ('YOU', 260, 'y')]
    return page('#0a0620', svg(d, b), lines, outline='#07031a', top=40)


if __name__ == '__main__':
    which = sys.argv[1:] or ['A', 'B', 'C']
    for n in which:
        open(os.path.join(HERE, f'{n}.html'), 'w').write(globals()[f'make_{n}']())
    print('ok')
