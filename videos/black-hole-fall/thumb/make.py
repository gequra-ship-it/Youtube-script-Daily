# Thumbnails A-C for black-hole-fall (guideline 16-6 / 16-8, brief tools/briefs/thumb_art.md). Run: python3 videos/black-hole-fall/thumb/make.py
# A  POINT OF NO RETURN     homage: Vertigo (1958) Saul Bass spiral poster: a red-orange spiral vortex with a small figure falling into it;
#                           here the spiral is the black hole's whirlpool and the falling figure is the astronaut frog. Script S30 "You pass
#                           through the point of no return", S31 "the moment your boots cross that mathematical threshold".
# B  MILLIONS OF GRAVITIES  intuitive: an astronaut stretched feet-first into a long thin ribbon toward a glowing black hole (suit fading white ->
#                           red: redshift); the frog floats nearby in a bubble helmet, hands on the glass. Script S42 "spikes into thousands of
#                           gravities, then millions ... stretched into long, thin ribbons of matter".
# C  WHERE DOES TIME END?   homage (painting): Dali "The Persistence of Memory": melting pocket watches over a dead branch and a stone slab,
#                           golden cliffs, but the sky holds a black hole. Script S37 "In general relativity, it is where time ends for anyone
#                           who enters", S14 "time begins to stretch".
import os, sys, math, random
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', '..', 'tools'))
from thumb_lib import page, svg, lin, rad, spark, stars

INK = '#1d2b1c'; GREEN = '#6aa55a'; DARKG = '#4d8a4a'; BELLY = '#9cc98a'; SUIT = '#eef1f5'; SUITS = '#b9c2cf'
FILTERS = ''.join(f'<filter id="b{n}" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="{n}"/></filter>' for n in (2, 3, 6, 12, 24, 50))
BODY = 'M-34 0 q-6 -64 34 -70 q40 -2 42 62 q0 10 -6 12 q-36 6 -70 -4z'
FROGDEFS = f'<clipPath id="frogbody"><path d="{BODY}"/></clipPath>'


def P(pts):
    return ' '.join(f'{a:.1f},{b:.1f}' for a, b in pts)


# ---------------- mascot frog (tools/assets/frog.svg body) in a space suit + bubble helmet ----------------
def limb(d, col=GREEN, w=7.5, wi=3.4):
    return f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="{w}"/><path d="{d}" fill="none" stroke="{col}" stroke-width="{wi}"/>'


def end_of(d):
    n = [float(v) for v in d.replace('M', ' ').replace('q', ' ').split()]
    return n[0] + n[-2], n[1] + n[-1]


def frog(x, y, s, rot=0, flip=False, look=(0, 0), mouth='O', armL=None, armR=None, legs=None, suit=True, helmet=True, back='', front=''):
    lx, ly = look
    assert math.hypot(lx + 1, ly) + 4.4 <= 13.5 - 2.2, 'pupil would leave the eye white'
    sx = -s if flip else s
    g = [f'<g transform="translate({x} {y}) rotate({rot}) scale({sx} {s})" stroke="{INK}" stroke-linejoin="round" stroke-linecap="round">', back]
    for hx, hy, fx, fy, fa in (legs or ((-20, -6, -22, 4, 0), (20, -6, 22, 4, 0))):
        if abs(fx - hx) + abs(fy - hy) > 14:
            g.append(limb(f'M{hx} {hy} L{fx} {fy}', SUIT if suit else GREEN, 15, 9))
        g.append(f'<ellipse cx="{fx}" cy="{fy}" rx="16" ry="9" transform="rotate({fa} {fx} {fy})" fill="{"#d9dee6" if suit else DARKG}" stroke-width="3.2"/>')
    g.append(f'<path d="{BODY}" fill="{GREEN}" stroke-width="4"/>')
    g.append(f'<ellipse cx="2" cy="-12" rx="22" ry="20" fill="{BELLY}" stroke="none" opacity=".7"/>')
    if suit:   # white suit over the lower body (clipped to the body), chest panel with lights
        g.append(f'<g clip-path="url(#frogbody)"><rect x="-50" y="-27" width="110" height="40" fill="{SUIT}" stroke="none"/>'
                 f'<path d="M-50 -2 q50 14 110 0 v20 h-110z" fill="{SUITS}" stroke="none"/></g>')
        g.append(f'<path d="{BODY}" fill="none" stroke-width="4"/>')
        g.append('<rect x="-6" y="-18" width="22" height="12" rx="3" fill="#5a6b80" stroke-width="2"/>'
                 '<circle cx="0" cy="-12" r="2.2" fill="#ff6a4a" stroke="none"/><circle cx="7" cy="-12" r="2.2" fill="#7fe0ff" stroke="none"/>')
    g.append('<path d="M-24 -50 q6 -14 18 -16" fill="none" stroke="#b6dea0" stroke-width="3" opacity=".8"/>')
    for ex in (-10, 22):
        g.append(f'<circle cx="{ex}" cy="-66" r="13.5" fill="#f4f5ea" stroke-width="3.2"/>')
        g.append(f'<circle cx="{ex + 1 + lx}" cy="{-66 + ly}" r="4.4" fill="{INK}" stroke="none"/>')
        g.append(f'<circle cx="{ex + 2.4 + lx}" cy="{-67.6 + ly}" r="1.5" fill="#fff" stroke="none"/>')
    g.append('<path d="M-22 -88 q12 -9 24 -1 M10 -89 q12 -8 24 1" fill="none" stroke-width="3.4"/>')
    if mouth == 'O':
        g.append('<ellipse cx="6" cy="-40" rx="8" ry="10" fill="#7a2f33" stroke-width="3"/><ellipse cx="6" cy="-34" rx="5" ry="3.4" fill="#e07b7b" stroke="none"/>')
    else:
        g.append('<ellipse cx="6" cy="-41" rx="6" ry="7.5" fill="#7a2f33" stroke-width="3"/>')
    g.append('<ellipse cx="-18" cy="-48" rx="5" ry="3" fill="#e98a8a" stroke="none" opacity=".55"/><ellipse cx="30" cy="-48" rx="5" ry="3" fill="#e98a8a" stroke="none" opacity=".55"/>')
    if helmet:   # glass bubble helmet + collar ring
        g.append('<circle cx="6" cy="-60" r="50" fill="#cfefff" fill-opacity=".13" stroke="#e9eef4" stroke-width="5"/>')
        g.append('<circle cx="6" cy="-60" r="50" fill="none" stroke="' + INK + '" stroke-width="1.6" opacity=".8"/>')
        g.append('<path d="M-30 -84 q14 -22 40 -24" fill="none" stroke="#fff" stroke-width="5.5" opacity=".85"/><path d="M44 -44 q7 -10 7 -24" fill="none" stroke="#fff" stroke-width="3" opacity=".5"/>')
        g.append(f'<ellipse cx="5" cy="-17" rx="38" ry="8" fill="#c7ced8" stroke-width="3"/><path d="M-28 -19 q33 7 66 0" fill="none" stroke="#fff" stroke-width="2" opacity=".8"/>')
    for a in (armL or 'M-34 -22 q-14 6 -16 22', armR or 'M38 -22 q14 6 16 22'):
        g.append(limb(a, SUIT if suit else GREEN)); ex_, ey_ = end_of(a)
        g.append(f'<circle cx="{ex_:.1f}" cy="{ey_:.1f}" r="5.8" fill="{"#dfe4ea" if suit else GREEN}" stroke-width="3"/>')
    g.append(front); g.append('</g>')
    return ''.join(g)


def veil(d, op=.6):
    return f'<path d="{d}" fill="#000" opacity="{op}" filter="url(#b50)"/>'


# =============================== A: Vertigo spiral ===============================
def make_A():
    random.seed(11)
    cx, cy = 1330, 540
    d = FILTERS + FROGDEFS
    d += rad('bgA', cx, cy, 1300, [(0, '#5a1208', 1), (.35, '#2a0806', 1), (1, '#070102', 1)])
    d += rad('armA', cx, cy, 980, [(0, '#fffbe8', 1), (.1, '#ffd88a', 1), (.24, '#ff8a36', 1), (.45, '#e0401e', 1), (.7, '#8a1210', 1), (1, '#2a0404', 1)])
    d += rad('haloA', cx, cy, 330, [(0, '#fff3cf', .9), (.4, '#ffb050', .45), (1, '#ff6020', 0)])
    d += rad('vigA', 960, 540, 1150, [(0, '#000', 0), (.65, '#000', 0), (1, '#000', .7)])
    b = '<rect width="1920" height="1080" fill="url(#bgA)"/>'
    b += stars(160, 1070, col='#ffe8d8', op=.55, sparks=0)
    b0 = math.log(1150 / 100) / (5 * math.pi)
    arms, lines = '', ''
    for k in range(3):
        phi = k * 2 * math.pi / 3
        out, inn, mid = [], [], []
        for i in range(361):
            th = i / 360 * 5 * math.pi
            r = 100 * math.exp(b0 * th); w = r * .2; a = -th + phi
            ca, sa = math.cos(a), math.sin(a) * .9
            out.append((cx + (r + w / 2) * ca, cy + (r + w / 2) * sa)); inn.append((cx + (r - w / 2) * ca, cy + (r - w / 2) * sa))
            mid.append((cx + (r + w * .32) * ca, cy + (r + w * .32) * sa))
        arms += f'<polygon points="{P(out + inn[::-1])}"/>'
        lines += f'<polyline points="{P(mid)}" fill="none"/>'
    b += f'<g fill="url(#armA)" opacity=".7" filter="url(#b24)">{arms}</g>'
    b += f'<g fill="url(#armA)" stroke="#1a0303" stroke-width="3">{arms}</g>'
    b += f'<g stroke="#fff6e0" stroke-width="3" opacity=".55">{lines}</g>'
    # thin dark spiral seams in the gaps (Vertigo line work)
    b += f'<ellipse cx="{cx}" cy="{cy}" rx="330" ry="300" fill="url(#haloA)"/>'
    b += f'<circle cx="{cx}" cy="{cy}" r="104" fill="#fff0c0" filter="url(#b12)"/>'
    b += f'<circle cx="{cx}" cy="{cy}" r="96" fill="#000"/>'
    b += f'<circle cx="{cx}" cy="{cy}" r="100" fill="none" stroke="#fffbe8" stroke-width="5"/>'
    for i in range(10):
        b += spark(cx + random.randint(-420, 420), cy + random.randint(-380, 380), random.choice([12, 16, 20]), op=.8)
    # debris falling in along the spiral
    for i in range(26):
        th = random.uniform(.6, 4.2) * math.pi; r = 100 * math.exp(b0 * th); a = -th + random.random() * 6.28
        x, y = cx + r * math.cos(a), cy + r * math.sin(a) * .9
        b += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{random.choice([3, 4, 5])}" fill="#fff4d8" opacity=".85"/>'
    # tiny mother ship far away (the friend watching)
    b += ('<g transform="translate(1735 150) rotate(-12)" stroke="#2a0a06" stroke-width="2.5">'
          '<rect x="-46" y="-12" width="92" height="24" rx="12" fill="#d9dde4"/><rect x="-70" y="-6" width="24" height="12" fill="#8a96a8"/>'
          '<rect x="46" y="-6" width="24" height="12" fill="#8a96a8"/><circle cx="18" cy="0" r="6" fill="#ffd77a"/></g>')
    b += '<circle cx="1753" cy="150" r="30" fill="#ffd77a" opacity=".25" filter="url(#b12)"/>'
    b += '<rect width="1920" height="1080" fill="url(#vigA)"/>'
    b += veil('M0 0 H1050 Q1010 360 760 520 Q440 640 0 600Z', .72)
    b += veil('M1560 880 H1920 V1080 H1560Z', .5)
    # frog falling head-first into the whirl, arms flailing
    fx, fy = 1010, 860
    b += ''.join(f'<path d="M{fx - 40 - i * 30} {fy + 70 + i * 18} l-{90 + i * 20} {60 + i * 8}" stroke="#ffe2c0" stroke-width="5" stroke-linecap="round" opacity="{.5 - i * .12:.2f}"/>' for i in range(3))
    b += frog(fx, fy, 3.0, rot=48, look=(3, -3), armL='M-34 -22 q-26 -6 -34 -36', armR='M38 -22 q26 -6 34 -36',
              legs=((-20, -6, -34, 12, 25), (20, -6, 38, 10, -25)))
    return page('#070102', svg(d, b), [('POINT OF NO', 132, 'w'), ('RETURN', 236, 'y')])


# =============================== B: stretched astronaut ===============================
def bez(t, p0, p1, p2):
    u = 1 - t
    return (u * u * p0[0] + 2 * u * t * p1[0] + t * t * p2[0], u * u * p0[1] + 2 * u * t * p1[1] + t * t * p2[1])


def ribbon(f, t0, t1, wf, off=0.0, n=80):
    """polygon along curve f(t) between t0..t1 with width wf(t) and side offset off(t)"""
    L, R = [], []
    for i in range(n + 1):
        t = t0 + (t1 - t0) * i / n
        x, y = f(t); x2, y2 = f(min(1, t + 1e-3)); x1, y1 = f(max(0, t - 1e-3))
        dx, dy = x2 - x1, y2 - y1; m = math.hypot(dx, dy) or 1; nx, ny = -dy / m, dx / m
        o = off(t) if callable(off) else off; w = wf(t) / 2
        L.append((x + nx * (o + w), y + ny * (o + w))); R.append((x + nx * (o - w), y + ny * (o - w)))
    return L + R[::-1]


def make_B():
    random.seed(5)
    hx, hy, HR = 1480, 600, 160
    d = FILTERS + FROGDEFS
    d += lin('bgB', [(0, '#0a0620'), (.55, '#170b34'), (1, '#05030e')])
    d += rad('haloB', hx, hy, 640, [(0, '#ffd6ff', .55), (.3, '#b04ad8', .3), (1, '#5a1a9a', 0)])
    p0, p1, p2 = (560, 850), (960, 900), (1330, 650)
    d += f'<linearGradient id="suitB" x1="{p0[0]}" y1="{p0[1]}" x2="{p2[0]}" y2="{p2[1]}" gradientUnits="userSpaceOnUse">' + ''.join(
        f'<stop offset="{o}" stop-color="{c}"/>' for o, c in ((0, '#f6f8fb'), (.35, '#e9edf3'), (.58, '#ffd2b0'), (.8, '#ff7a44'), (1, '#e0302a'))) + '</linearGradient>'
    d += rad('visorB', 0, 0, 1, [(0, '#fff2b8', 1), (1, '#b07a1a', 1)]).replace('gradientUnits="userSpaceOnUse"', '').replace('cx="0" cy="0" r="1"', 'cx=".35" cy=".3" r=".9"')
    d += f'<clipPath id="upB"><rect x="-600" y="-600" width="3200" height="{hy + 600}"/></clipPath><clipPath id="loB"><rect x="-600" y="{hy}" width="3200" height="1200"/></clipPath>'
    b = '<rect width="1920" height="1080" fill="url(#bgB)"/>'
    b += ''.join(f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{ry}" fill="{c}" opacity="{o}" filter="url(#b50)"/>' for x, y, rx, ry, c, o in
                 ((1300, 250, 420, 160, '#5a2a9a', .35), (1750, 860, 380, 200, '#2a3a9a', .35), (500, 900, 420, 160, '#3a1a6a', .3)))
    b += stars(190, 1070, col='#efe8ff', op=.6, sparks=0)
    b += f'<ellipse cx="{hx}" cy="{hy}" rx="700" ry="520" fill="url(#haloB)"/>'

    def disk(clip):
        o = f'<g transform="rotate(-14 {hx} {hy})"><g clip-path="url(#{clip})">'
        for i, (rx, col, op, w) in enumerate(((560, '#6a2aa8', .35, 60), (500, '#b04ad8', .55, 52), (430, '#ff7ad8', .7, 48), (360, '#ffb0e8', .85, 40),
                                              (290, '#fff0ff', .95, 34), (230, '#ffffff', 1, 22))):
            ry = rx * .21
            o += f'<ellipse cx="{hx}" cy="{hy}" rx="{rx}" ry="{ry:.0f}" fill="none" stroke="{col}" stroke-width="{w}" opacity="{op}" filter="url(#b{12 if i < 3 else 6})"/>'
        for k in range(14):   # streaks in the disk
            rx = random.randint(220, 540); a0 = random.uniform(0, 360)
            o += f'<ellipse cx="{hx}" cy="{hy}" rx="{rx}" ry="{rx * .21:.0f}" fill="none" stroke="#fff" stroke-width="2" opacity=".35" stroke-dasharray="{random.randint(60, 200)} {random.randint(200, 600)}" stroke-dashoffset="{a0:.0f}"/>'
        return o + '</g></g>'
    b += disk('upB')
    b += f'<circle cx="{hx}" cy="{hy}" r="{HR + 14}" fill="#ffe0ff" filter="url(#b12)" opacity=".9"/>'
    b += f'<circle cx="{hx}" cy="{hy}" r="{HR}" fill="#000"/><circle cx="{hx}" cy="{hy}" r="{HR + 3}" fill="none" stroke="#fff6ff" stroke-width="4"/>'
    # ---- stretched astronaut (feet first into the hole) ----
    f = lambda t: bez(t, p0, p1, p2)
    def bodyw(t):
        if t < .08: return 140
        if t < .24: return 140 - (t - .08) / .16 * 34
        return max(40, 106 - (t - .24) / .24 * 62)
    ast = ''
    # arms trailing toward the hole on both sides
    for sg in (1, -1):
        poly = ribbon(f, .1, .62, lambda t: max(4, 32 - (t - .1) * 50), off=lambda t, sg=sg: sg * max(22, 82 - (t - .1) * 100))
        ast += f'<polygon points="{P(poly)}" fill="url(#suitB)" stroke="#170c2a" stroke-width="4"/>'
    for sg in (1, -1):   # legs: two long thin strands
        poly = ribbon(f, .44, 1.0, lambda t: max(3, 28 - (t - .44) * 44), off=lambda t, sg=sg: sg * max(4, 15 - (t - .44) * 20))
        ast = f'<polygon points="{P(poly)}" fill="#ff6a3a" opacity=".8" stroke="#ff8a4a" stroke-width="18" filter="url(#b12)"/>' + ast
        ast += f'<polygon points="{P(poly)}" fill="url(#suitB)" stroke="#170c2a" stroke-width="3.5"/>'
    torso = ribbon(f, .06, .5, bodyw)
    ast += f'<polygon points="{P(torso)}" fill="url(#suitB)" stroke="#170c2a" stroke-width="5"/>'
    shade = ribbon(f, .08, .5, lambda t: bodyw(t) * .35, off=lambda t: -bodyw(t) * .3)
    ast += f'<polygon points="{P(shade)}" fill="#7a6a9a" opacity=".28"/>'
    hl = ribbon(f, .1, .46, lambda t: 5, off=lambda t: bodyw(t) * .32)
    ast += f'<polygon points="{P(hl)}" fill="#fff" opacity=".7"/>'
    # stripes along the suit (show how far it is stretched)
    for t in (.16, .27, .38):
        x, y = f(t); x2, y2 = f(t + .01); ang = math.degrees(math.atan2(y2 - y, x2 - x))
        ast += f'<rect x="{x - 5:.0f}" y="{y - bodyw(t) / 2:.0f}" width="10" height="{bodyw(t):.0f}" fill="#ff8a4a" opacity=".75" transform="rotate({ang:.0f} {x:.0f} {y:.0f})"/>'
    # chest panel + helmet
    x, y = f(.12)
    ast += f'<rect x="{x - 24:.0f}" y="{y - 18:.0f}" width="48" height="34" rx="5" fill="#5a6b80" stroke="#170c2a" stroke-width="3" transform="rotate(-6 {x:.0f} {y:.0f})"/>'
    ast += f'<circle cx="{x - 8:.0f}" cy="{y - 2:.0f}" r="4" fill="#ff5a3a"/><circle cx="{x + 6:.0f}" cy="{y - 2:.0f}" r="4" fill="#7fe0ff"/>'
    hx0, hy0 = p0
    ast += f'<circle cx="{hx0 - 8}" cy="{hy0 - 2}" r="92" fill="#e9edf3" stroke="#170c2a" stroke-width="5"/>'
    ast += f'<ellipse cx="{hx0 - 14}" cy="{hy0 - 4}" rx="64" ry="55" fill="url(#visorB)" stroke="#170c2a" stroke-width="4"/>'
    ast += f'<path d="M{hx0 - 62} {hy0 - 24} q20 -32 58 -36" fill="none" stroke="#fff" stroke-width="7" stroke-linecap="round" opacity=".85"/>'
    ast += f'<path d="M{hx0 + 6} {hy0 + 32} q24 -8 32 -32" fill="none" stroke="#ff7ad8" stroke-width="5" stroke-linecap="round" opacity=".8"/>'
    b += f'<g>{ast}</g>'
    # glow around the stretched end (redshifted light)
    b += disk('loB')
    b += f'<circle cx="{hx}" cy="{hy}" r="{HR + 3}" fill="none" stroke="#fff6ff" stroke-width="4" clip-path="url(#loB)"/>'
    # debris + sparkles flowing in
    for i in range(30):
        t = random.uniform(.2, 1); x, y = f(t); x += random.randint(-90, 90); y += random.randint(-90, 90)
        b += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{random.choice([2, 3, 4])}" fill="#ffe6f6" opacity=".8"/>'
    for x, y, s in ((1230, 380, 22), (1760, 760, 18), (980, 640, 16), (1660, 470, 14), (820, 760, 14)):
        b += spark(x, y, s)
    b += veil('M0 0 H1100 Q1060 330 800 460 Q420 560 0 520Z', .7)
    b += veil('M1580 880 H1920 V1080 H1580Z', .45)
    # frog floating up right, hands on its helmet glass, staring at the astronaut
    b += f'<path d="M1610 290 q-40 30 -70 20" stroke="#efe8ff" stroke-width="3" fill="none" opacity=".4" stroke-dasharray="8 10"/>'
    b += frog(1715, 350, 2.8, rot=-10, look=(-4, 3), armL='M-34 -22 q-14 -12 -8 -34', armR='M38 -22 q14 -12 8 -34',
              legs=((-20, -6, -28, 10, 20), (20, -6, 30, 8, -15)))
    return page('#05030e', svg(d, b), [('MILLIONS', 196, 'y'), ('OF GRAVITIES', 124, 'w')])


# =============================== C: Persistence of Memory + black hole ===============================
def melt_clock(X0, Y0, R, k=1.0, drop=50, hour=11.8, minute=58, sag=.8):
    def W(u, v):
        s = (v + 1) / 2
        return (X0 + R * u * (1 - .16 * s) + 18 * k * s * s, Y0 + R * 1.02 * s * (1 + sag * s * s) + drop * ((u + 1) / 2) ** 2 * s)
    rim = [W(math.cos(a), math.sin(a)) for a in (i / 120 * 2 * math.pi for i in range(121))]
    rim2 = [W(.86 * math.cos(a), .86 * math.sin(a)) for a in (i / 120 * 2 * math.pi for i in range(121))]
    o = ''
    o += f'<polygon points="{P(rim)}" fill="#3a2410" opacity=".35" transform="translate({14 * k:.0f} {16 * k:.0f})" filter="url(#b6)"/>'
    o += f'<polygon points="{P(rim)}" fill="#c98f2a" stroke="#2a1a0a" stroke-width="{5 * k:.1f}"/>'
    o += f'<polygon points="{P(rim)}" fill="none" stroke="#ffe39a" stroke-width="{3 * k:.1f}" opacity=".6" transform="translate({-3 * k:.1f} {-3 * k:.1f})"/>'
    o += f'<polygon points="{P(rim2)}" fill="url(#faceC)" stroke="#7a5418" stroke-width="{2.5 * k:.1f}"/>'
    for h in range(60):
        a = h / 60 * 2 * math.pi - math.pi / 2; big = h % 5 == 0
        r0 = .62 if big else .72
        a1, a2 = W(r0 * math.cos(a), r0 * math.sin(a)), W(.8 * math.cos(a), .8 * math.sin(a))
        o += f'<line x1="{a1[0]:.1f}" y1="{a1[1]:.1f}" x2="{a2[0]:.1f}" y2="{a2[1]:.1f}" stroke="#2a1a0a" stroke-width="{(4.2 if big else 1.6) * k:.1f}" stroke-linecap="round"/>'
    for ang, ln, w in ((hour / 12 * 2 * math.pi, .4, 7), (minute / 60 * 2 * math.pi, .62, 4.5)):
        pts = [W(j / 12 * ln * math.sin(ang), -j / 12 * ln * math.cos(ang)) for j in range(13)]
        o += f'<polyline points="{P(pts)}" fill="none" stroke="#1a1008" stroke-width="{w * k:.1f}" stroke-linecap="round"/>'
    c = W(0, 0); o += f'<circle cx="{c[0]:.1f}" cy="{c[1]:.1f}" r="{6 * k:.1f}" fill="#1a1008"/>'
    return o, W


def make_C():
    random.seed(3)
    bx, by, BR = 1440, 330, 132
    HZ = 760
    d = FILTERS + FROGDEFS
    d += lin('skyC', [(0, '#081a28'), (.45, '#1f3f52'), (.78, '#7a8a78'), (1, '#f0c26a')])
    d += lin('groundC', [(0, '#7a5428'), (.25, '#4a3016'), (1, '#140b05')])
    d += lin('seaC', [(0, '#f3d48c'), (1, '#9ab0a8')])
    d += lin('slabTop', [(0, '#a8834a'), (1, '#7a5a30')], x2=1, y2=0)
    d += lin('slabFront', [(0, '#4a3218'), (1, '#1a0f06')])
    d += lin('cliffC', [(0, '#e8b860'), (1, '#6a4420')])
    d += rad('haloC', bx, by, 420, [(0, '#fff2cc', .8), (.3, '#ffcf7a', .35), (1, '#ffb050', 0)])
    d += '<radialGradient id="faceC" cx=".4" cy=".35" r=".8"><stop offset="0" stop-color="#fffaf0"/><stop offset=".7" stop-color="#f3e6c8"/><stop offset="1" stop-color="#cdb487"/></radialGradient>'
    b = f'<rect width="1920" height="{HZ + 20}" fill="url(#skyC)"/>'
    b += stars(130, 560, col='#f4ecd8', op=.6, sparks=0)
    b += f'<circle cx="{bx}" cy="{by}" r="420" fill="url(#haloC)"/>'
    # lensed starlight arcs around the hole
    for r, a0, a1, op, w in ((168, 200, 340, .85, 5), (190, 20, 160, .7, 4), (222, 230, 300, .55, 3), (250, 40, 120, .45, 3), (205, 320, 395, .6, 3.5), (280, 190, 240, .4, 2.5)):
        p = [(bx + r * math.cos(math.radians(a)), by + r * math.sin(math.radians(a)) * .96) for a in range(a0, a1 + 1, 4)]
        b += f'<polyline points="{P(p)}" fill="none" stroke="#fff4dc" stroke-width="{w}" opacity="{op}" stroke-linecap="round"/>'
    b += f'<circle cx="{bx}" cy="{by}" r="{BR + 14}" fill="#fff0c8" filter="url(#b12)"/>'
    b += f'<circle cx="{bx}" cy="{by}" r="{BR}" fill="#000"/><circle cx="{bx}" cy="{by}" r="{BR + 3}" fill="none" stroke="#fffaf0" stroke-width="4.5"/>'
    for x, y, s in ((1220, 170, 20), (1690, 520, 16), (1660, 140, 14), (1150, 460, 12)):
        b += spark(x, y, s)
    # sea + golden cliffs (Cap de Creus, right) + plain
    b += f'<rect y="{HZ - 30}" width="1920" height="60" fill="url(#seaC)"/>'
    b += f'<path d="M1380 {HZ + 10} L1440 {HZ - 40} L1500 {HZ - 60} L1560 {HZ - 110} L1640 {HZ - 140} L1720 {HZ - 120} L1800 {HZ - 170} L1920 {HZ - 190} V{HZ + 30} Z" fill="url(#cliffC)" stroke="#3a2410" stroke-width="3"/>'
    b += f'<path d="M1560 {HZ - 100} l40 60 M1700 {HZ - 115} l30 70 M1820 {HZ - 160} l20 90" stroke="#8a5a28" stroke-width="5" opacity=".6"/>'
    b += f'<rect y="{HZ + 20}" width="1920" height="{1080 - HZ - 20}" fill="url(#groundC)"/>'
    b += f'<path d="M0 {HZ + 20} H1920" stroke="#f3d48c" stroke-width="3" opacity=".5"/>'
    # stone slab (Dali's block) + its shadow
    b += '<path d="M700 1010 L1520 1010 L1600 1080 L640 1080Z" fill="#000" opacity=".35" filter="url(#b12)"/>'
    b += '<path d="M770 812 L1450 812 L1480 846 L740 846Z" fill="url(#slabTop)" stroke="#2a1a0a" stroke-width="4"/>'
    b += '<path d="M740 846 L1480 846 L1480 1030 L740 1030Z" fill="url(#slabFront)" stroke="#2a1a0a" stroke-width="4"/>'
    b += '<path d="M744 850 L1476 850" stroke="#c9a060" stroke-width="3" opacity=".6"/>'
    # dead branch growing out of the slab
    b += ('<path d="M1000 818 C990 740 1010 680 1050 630 C1080 595 1140 585 1300 560" fill="none" stroke="#2a1a0a" stroke-width="30" stroke-linecap="round"/>'
          '<path d="M1000 818 C990 740 1010 680 1050 630 C1080 595 1140 585 1300 560" fill="none" stroke="#5a3e24" stroke-width="22" stroke-linecap="round"/>'
          '<path d="M1004 800 C996 740 1014 690 1048 646" fill="none" stroke="#8a6a44" stroke-width="5" opacity=".7"/>'
          '<path d="M1250 568 C1262 540 1280 515 1310 498" fill="none" stroke="#2a1a0a" stroke-width="14" stroke-linecap="round"/>'
          '<path d="M1250 568 C1262 540 1280 515 1310 498" fill="none" stroke="#5a3e24" stroke-width="8" stroke-linecap="round"/>'
          '<path d="M1060 640 C1040 610 1030 590 1036 566" fill="none" stroke="#2a1a0a" stroke-width="12" stroke-linecap="round"/>'
          '<path d="M1060 640 C1040 610 1030 590 1036 566" fill="none" stroke="#5a3e24" stroke-width="6" stroke-linecap="round"/>')
    # main melting watch draped over the branch (back fold first)
    b += '<path d="M1105 588 Q1180 548 1262 572 L1258 582 Q1180 566 1110 600Z" fill="#8a5e1a" stroke="#2a1a0a" stroke-width="4"/>'
    clock, W = melt_clock(1180, 586, 146, k=1.1, drop=70, sag=.8)
    b += clock
    b += '<path d="M1080 590 Q1180 572 1282 584" fill="none" stroke="#2a1a0a" stroke-width="5" opacity=".5"/>'
    # pocket-watch crown on the left rim
    cxw, cyw = W(-1.06, -.05)
    b += f'<rect x="{cxw - 26:.0f}" y="{cyw - 9:.0f}" width="20" height="18" rx="4" fill="#c98f2a" stroke="#2a1a0a" stroke-width="4"/><circle cx="{cxw - 36:.0f}" cy="{cyw:.0f}" r="11" fill="none" stroke="#2a1a0a" stroke-width="9"/><circle cx="{cxw - 36:.0f}" cy="{cyw:.0f}" r="11" fill="none" stroke="#d9a43a" stroke-width="4.5"/>'
    # drip falling from the bottom
    dx, dy = W(.55, .9)
    b += f'<path d="M{dx - 12:.0f} {dy - 6:.0f} Q{dx:.0f} {dy + 30:.0f} {dx + 2:.0f} {dy + 46:.0f} Q{dx + 14:.0f} {dy + 24:.0f} {dx + 12:.0f} {dy - 8:.0f}Z" fill="#c98f2a" stroke="#2a1a0a" stroke-width="3.5"/>'
    b += f'<ellipse cx="{dx + 4:.0f}" cy="{dy + 78:.0f}" rx="9" ry="12" fill="#d9a43a" stroke="#2a1a0a" stroke-width="3"/>'
    # second, smaller watch melting over the slab's front edge
    clock2, W2 = melt_clock(1330, 838, 62, k=.55, drop=26, hour=3.2, minute=12, sag=1.3)
    b += '<ellipse cx="1335" cy="830" rx="62" ry="12" fill="#c98f2a" stroke="#2a1a0a" stroke-width="3"/>'
    b += clock2
    # glow on the big watch (focal)
    b += f'<circle cx="1185" cy="690" r="210" fill="#ffd98a" opacity=".12" filter="url(#b50)"/>'
    b += veil('M0 0 H1000 Q980 380 740 560 Q420 680 0 640Z', .62)
    b += veil('M1560 880 H1920 V1080 H1560Z', .5)
    # frog sitting on the plain, pointing up at the melting watch
    b += '<ellipse cx="500" cy="996" rx="150" ry="20" fill="#000" opacity=".35"/>'
    b += frog(500, 985, 3.1, rot=0, look=(4, -4), armR='M38 -22 q22 -8 34 -40', armL='M-34 -22 q-14 6 -16 22')
    return page('#081a28', svg(d, b), [('WHERE DOES', 126, 'w'), ('TIME', 236, 'y'), ('END?', 176, 'w')])


if __name__ == '__main__':
    for n, fn in (('A', make_A), ('B', make_B), ('C', make_C)):
        open(os.path.join(HERE, f'{n}.html'), 'w').write(fn())
    print('ok')
