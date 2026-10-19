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
# v2 (2026-10-19, owner: "background disappointing"): a deep vortex of sunset-lit cumulus towers with a detailed landscape far below
random.seed(21)
CX, CY, SY = 1420, 730, .86
K = .115
RG = 300   # radius of the visible ground disk at the bottom of the tunnel


def hx(c):
    return tuple(int(c[i:i + 2], 16) for i in (1, 3, 5))


def mix(c1, c2, t):
    t = max(0, min(1, t)); a, b_ = hx(c1), hx(c2)
    return '#%02x%02x%02x' % tuple(round(a[i] + (b_[i] - a[i]) * t) for i in range(3))


def sp(th, ph, f=1.0):
    r = 34 * math.exp(K * th) * f
    return CX + r * math.cos(th + ph), CY + r * math.sin(th + ph) * SY, r


def band(ph, frac, th0=0, th1=35, step=.06):
    out_ = [sp(th0 + i * step, ph) for i in range(int((th1 - th0) / step) + 1)]
    f = math.exp(-math.pi * K * frac)
    in_ = [sp(th0 + i * step, ph, f) for i in range(int((th1 - th0) / step) + 1)][::-1]
    return 'M' + ' L'.join(f'{x:.1f} {y:.1f}' for x, y, _ in out_ + in_) + 'Z'


d = rad('bgA', CX, CY, 1500, [(0, '#c9d6ee', 1), (.2, '#7e86c0', 1), (.42, '#4a2f78', 1), (.75, '#2a1446', 1), (1, '#16091f', 1)])
d += rad('hazeA', 0, 0, RG, [(0, '#fff4d8', .0), (.55, '#dfe8f4', .15), (.85, '#c4d2ec', .6), (1, '#b4c4e6', .95)])
d += rad('sunA', 1800, -20, 850, [(0, '#fffbe8', .95), (.16, '#ffe6a6', .6), (.45, '#ffb070', .14), (1, '#ff9060', 0)])
d += rad('glA', 1150, 330, 330, [(0, '#fff3d6', .55), (.5, '#ffd9a0', .2), (1, '#ffd9a0', 0)])
d += rad('vigA', 960, 540, 1150, [(.6, '#000000', 0), (1, '#0e0418', .6)])
d += rad('txtA', 200, 120, 700, [(0, '#12061e', .55), (1, '#12061e', 0)])
d += f'<clipPath id="gclip"><circle cx="0" cy="0" r="{RG}"/></clipPath>'
d += '<filter id="bA"><feGaussianBlur stdDeviation="1.4"/></filter><filter id="bA2"><feGaussianBlur stdDeviation="16"/></filter>'
d += '<filter id="bA3"><feGaussianBlur stdDeviation="5"/></filter><filter id="bA4"><feGaussianBlur stdDeviation="28"/></filter>'

b = '<rect width="1920" height="1080" fill="url(#bgA)"/>'
# ---------- the ground, 10 km below: patchwork fields, forests, a river with sun glints, a lake, a small town ----------
gr = '<circle r="%d" fill="#7f9c4c"/>' % RG
FP = ['#8fae4c', '#a9b956', '#c9b25a', '#7a9a42', '#d8c27a', '#6d8a3e', '#b39a52', '#94b860', '#c4a96a', '#5f8a44']
rot = math.radians(24)
for i in range(-9, 10):
    for j in range(-9, 10):
        w_, h_ = random.uniform(34, 62), random.uniform(28, 52)
        u, v = i * 52 + random.uniform(-6, 6), j * 44 + random.uniform(-6, 6)
        pts = [(u, v), (u + w_, v + random.uniform(-4, 4)), (u + w_ + random.uniform(-5, 5), v + h_), (u + random.uniform(-4, 4), v + h_)]
        pts = [(x * math.cos(rot) - y * math.sin(rot), x * math.sin(rot) + y * math.cos(rot)) for x, y in pts]
        if min(math.hypot(x, y) for x, y in pts) > RG + 10:
            continue
        gr += '<path d="M' + ' L'.join(f'{x:.0f} {y:.0f}' for x, y in pts) + f'Z" fill="{random.choice(FP)}" stroke="#4d6a2c" stroke-width="2"/>'
        if random.random() < .3:   # plough furrows
            x0, y0 = pts[0]; x1, y1 = pts[1]
            gr += f'<path d="M{x0:.0f} {y0:.0f} L{x1:.0f} {y1:.0f}" stroke="#e6d6a0" stroke-width="1.5" opacity=".45" transform="translate({math.sin(rot) * -8:.0f} {math.cos(rot) * 8:.0f})"/>'
# forests
for fx, fy, n in ((-170, -120, 70), (150, 140, 60), (-60, 210, 40), (200, -170, 45), (-250, 90, 35)):
    for _ in range(n):
        x, y, r_ = fx + random.gauss(0, 42), fy + random.gauss(0, 30), random.uniform(7, 13)
        gr += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r_:.0f}" fill="{random.choice(["#2f5a2a", "#3a6a30", "#24502a"])}"/>'
    for _ in range(n // 2):
        x, y = fx + random.gauss(0, 40), fy + random.gauss(0, 28)
        gr += f'<circle cx="{x + 2:.0f}" cy="{y - 2:.0f}" r="4" fill="#6f9a48" opacity=".8"/>'
# lake
gr += '<path d="M60 -240 C130 -270 210 -230 200 -170 C190 -120 110 -130 80 -160 C40 -190 10 -220 60 -240Z" fill="#2f6a94" stroke="#2c4a2a" stroke-width="5"/>'
gr += '<path d="M90 -230 C140 -245 180 -220 175 -195" stroke="#fff6d8" stroke-width="5" fill="none" opacity=".8" stroke-linecap="round"/>'
# river (meandering, glinting in the low sun)
RV = 'M-340 40 C-260 0 -220 90 -150 60 S-60 -40 0 10 S80 120 150 70 S240 -60 340 -20'
gr += f'<path d="{RV}" stroke="#3d5a34" stroke-width="26" fill="none"/><path d="{RV}" stroke="#4f8ec0" stroke-width="16" fill="none"/>'
gr += f'<path d="{RV}" stroke="#e8f8ff" stroke-width="4" fill="none" stroke-dasharray="30 50 8 60" opacity=".85"/>'
# roads + town
for rd in ('M-330 -60 Q-120 -40 -20 -10 T330 110', 'M-40 -330 Q-20 -120 -10 0 T30 330', 'M120 -300 Q60 -120 20 0'):
    gr += f'<path d="{rd}" stroke="#efe6cc" stroke-width="3.5" fill="none" opacity=".85"/>'
for _ in range(70):
    x, y = random.gauss(-20, 30), random.gauss(-10, 24)
    gr += f'<rect x="{x:.0f}" y="{y:.0f}" width="{random.randint(4, 9)}" height="{random.randint(4, 8)}" fill="{random.choice(["#efe4cc", "#c97a5a", "#b8b4c0", "#e0a070"])}" transform="rotate(24 {x:.0f} {y:.0f})"/>'
# little cumulus over the ground and their shadows
for _ in range(16):
    a_, rr = random.uniform(0, 6.28), random.uniform(40, RG - 30)
    x, y, s_ = math.cos(a_) * rr, math.sin(a_) * rr, random.uniform(8, 18)
    gr += f'<ellipse cx="{x - 14:.0f}" cy="{y + 12:.0f}" rx="{s_ * 1.6:.0f}" ry="{s_:.0f}" fill="#1e2e1a" opacity=".28"/>'
    gr += ''.join(f'<circle cx="{x + dx * s_:.0f}" cy="{y + dy * s_:.0f}" r="{s_ * q:.0f}" fill="#ffffff" opacity=".92"/>' for dx, dy, q in ((-.8, .2, .7), (0, 0, 1), (.8, .2, .7), (.3, -.5, .6)))
gr += f'<circle r="{RG}" fill="url(#hazeA)"/>'
b += f'<g transform="translate({CX} {CY}) scale(1 {SY})"><circle r="{RG + 14}" fill="#c4d2ec" filter="url(#bA3)"/><g clip-path="url(#gclip)">{gr}</g></g>'

# ---------- the vortex: two spiral arms of towering cumulus, far = hazy blue, near = sunset gold/violet ----------
LIT = ('#b8587a', '#f29a78', '#ffe4bc')     # shade, body, highlight on the walls facing the sun
DRK = ('#2a1046', '#6a3488', '#f2a6a0')     # walls turned away (warm rim on top)
HZ_ = ('#8e98c8', '#b4bce0', '#e4e8f6')
L = (.6, -.8)   # light comes from the top-right


def cpuff(x, y, r, lit, hz):
    e = max(0, math.hypot((x - 960) / 960, (y - 540) / 540) - .75) * .55 + max(0, 1 - math.hypot((x - 420) / 520, (y - 260) / 330)) * .3   # baked-in vignette + calmer text area
    cols = [mix(mix(mix(DRK[i], LIT[i], lit), HZ_[i], hz), '#1a0828', e) for i in range(3)]
    return (f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r:.0f}" fill="{cols[0]}"/>'
            f'<circle cx="{x + L[0] * r * .2:.0f}" cy="{y + L[1] * r * .2:.0f}" r="{r * .8:.0f}" fill="{cols[2]}"/>'
            f'<circle cx="{x - L[0] * r * .02:.0f}" cy="{y - L[1] * r * .02:.0f}" r="{r * .8:.0f}" fill="{cols[1]}"/>')


def litf(x, y):
    ux, uy = x - CX, (y - CY) / SY; n = math.hypot(ux, uy) or 1
    return .5 + .5 * ((ux * -.6 + uy * .8) / n)   # lower-left walls face the sun


# soft body of each arm under the puffs
g = ''
for ph in (0, math.pi):
    g += f'<path d="{band(ph, .5, 17)}" fill="#7a5a96"/>'
b += f'<g filter="url(#bA2)" opacity=".85">{g}</g>'
P = []
for ph in (0, math.pi):
    th = 17.5
    while th < 35:
        x0, y0, r0 = sp(th, ph, .9)
        for _ in range(4):
            f2 = random.uniform(.82, .99)
            x, y, r = sp(th + random.uniform(-.04, .04), ph, f2)
            pr = r * random.uniform(.045, .1) * (1.15 if f2 > .93 else 1)
            P.append((r, x, y, pr))
        th += .06 + 11 / (r0 + 60)
P.sort()   # far (small radius) first, near on top
pf = ''
for r, x, y, pr in P:
    hz = max(0, 1 - (r - RG) / 420)
    pf += cpuff(x, y, pr, litf(x, y), hz * .85)
b += f'<g filter="url(#bA2)" opacity=".75">' + ''.join(f'<path d="{band(ph - .05, .22, 17)}" fill="#140828" transform="translate({CX} {CY}) scale(.86) translate({-CX} {-CY})"/>' for ph in (0, math.pi)) + '</g>'
b += pf
# sunlit edges on the sun-facing walls
hl = ''.join(f'<path d="{band(ph + .12, .16, 19, 35)}" fill="#fff0d0" opacity=".35"/>' for ph in (0, math.pi))
b += f'<g filter="url(#bA2)">{hl}</g>'
# god rays from the sun (top-right) into the tunnel
rays = ''
for a0, w0, op in ((200, 5, .16), (212, 3, .12), (222, 6, .14), (236, 4, .1), (190, 3, .1)):
    a1, a2 = math.radians(a0 - w0 / 2), math.radians(a0 + w0 / 2)
    rays += f'<path d="M1800 -20 L{1800 + math.cos(a1) * 1900:.0f} {-20 - math.sin(a1) * 1900 * -1:.0f} L{1800 + math.cos(a2) * 1900:.0f} {-20 - math.sin(a2) * 1900 * -1:.0f}Z" fill="#fff2cc" opacity="{op}"/>'
b += f'<g filter="url(#bA4)">{rays}</g>'
b += '<rect x="900" width="1020" height="860" fill="url(#sunA)"/>'
# radial speed streaks rushing toward the centre
for k in range(14):
    a = random.uniform(0, 2 * math.pi); r0 = random.uniform(360, 620); r1 = r0 + random.uniform(160, 460)
    b += f'<path d="M{CX + math.cos(a) * r0:.0f} {CY + math.sin(a) * r0 * SY:.0f} L{CX + math.cos(a) * r1:.0f} {CY + math.sin(a) * r1 * SY:.0f}" stroke="#fff6ea" stroke-width="{random.choice([2, 3, 4])}" stroke-linecap="round" opacity="{random.uniform(.15, .45):.2f}"/>'
# the faller
b += '<rect width="1920" height="1080" fill="url(#glA)"/>'
b += f'<g transform="translate(1150 330) rotate(-16) scale(.98)">' + faller() + '</g>'
b += spark(1560, 300, 22) + spark(980, 820, 16) + spark(1640, 690, 14) + spark(1450, 190, 12, op=.6)
open('A.html', 'w', encoding='utf-8').write(page('#2a1446', svg(d, b), [('ABOUT', 116, 'w'), ('2.5 MIN', 236, 'y'), ('OF FALLING', 136, 'w')], '#16061e', top=44))

def airliner():
    """white twin-engine airliner, 3/4 view from slightly below, nose to the left; local coords ~ -330..330 x -190..170"""
    o = ''
    # far wing (behind the fuselage, swept back and up) + far engine peeking under the fuselage
    o += f'<path d="M-40 -18 L150 -150 L192 -152 L110 -14Z" fill="url(#wingF)" stroke="{LINE}" stroke-width="6" stroke-linejoin="round"/>'
    o += f'<path d="M92 -96 L118 -126" stroke="#8a98ac" stroke-width="4"/>'
    # far horizontal stabiliser
    o += f'<path d="M232 -20 L300 -86 L326 -86 L292 -16Z" fill="url(#wingF)" stroke="{LINE}" stroke-width="5" stroke-linejoin="round"/>'
    # tail fin
    o += f'<path d="M206 -26 L268 -176 L314 -180 L326 -40Z" fill="url(#finB)" stroke="{LINE}" stroke-width="6" stroke-linejoin="round"/>'
    o += f'<path d="M262 -150 L300 -152 L310 -60" stroke="#ffd98a" stroke-width="5" fill="none" opacity=".7" stroke-linecap="round"/>'
    # fuselage (long white tube, rounded nose, tapered tail)
    F = 'M-300 6 C-300 -26 -270 -38 -220 -40 L230 -40 C268 -40 300 -36 336 -26 L336 -16 C300 12 260 32 220 34 L-220 34 C-276 34 -300 26 -300 6Z'
    o += f'<path d="{F}" fill="url(#fusB)" stroke="{LINE}" stroke-width="7" stroke-linejoin="round"/>'
    o += '<path d="M-286 -12 C-270 -30 -240 -34 -210 -34 L230 -34" stroke="#ffffff" stroke-width="6" fill="none" opacity=".9" stroke-linecap="round"/>'
    # cheatline stripe + belly shade
    o += '<path d="M-296 12 C-260 16 -230 16 -200 16 L250 16 C280 12 300 4 322 -6" stroke="#2f6fb8" stroke-width="7" fill="none"/>'
    o += '<path d="M-260 28 L220 28" stroke="#9aa8bc" stroke-width="6" opacity=".6"/>'
    # cockpit windows
    o += f'<path d="M-282 -10 L-262 -24 L-238 -24 L-240 -10Z" fill="#20304a" stroke="{LINE}" stroke-width="3"/>'
    o += f'<path d="M-234 -24 L-210 -24 L-212 -10 L-236 -10Z" fill="#20304a" stroke="{LINE}" stroke-width="3"/>'
    o += '<path d="M-274 -12 L-262 -21" stroke="#9fd0ff" stroke-width="3"/>'
    # passenger windows (one long row) + doors
    o += ''.join(f'<rect x="{x}" y="-17" width="10" height="13" rx="4" fill="#20304a"/>' for x in range(-186, 222, 21))
    for dx in (-200, 150):
        o += f'<rect x="{dx}" y="-30" width="20" height="48" rx="6" fill="none" stroke="#8a98ac" stroke-width="3"/>'
    # near horizontal stabiliser
    o += f'<path d="M238 8 L314 74 L340 74 L300 2Z" fill="url(#wingN)" stroke="{LINE}" stroke-width="5" stroke-linejoin="round"/>'
    # near wing: big, swept back, coming toward the viewer
    W = 'M-70 18 L150 196 L204 200 L100 22Z'
    o += f'<path d="{W}" fill="url(#wingN)" stroke="{LINE}" stroke-width="7" stroke-linejoin="round"/>'
    o += '<path d="M-56 26 L156 192" stroke="#ffffff" stroke-width="5" opacity=".8"/>'
    o += f'<path d="M150 196 L162 176 L186 178 L204 200Z" fill="#2f6fb8" stroke="{LINE}" stroke-width="4" stroke-linejoin="round"/>'  # winglet tip
    o += '<path d="M60 70 L120 136 M104 30 L190 186" stroke="#a8b4c6" stroke-width="3" opacity=".7"/>'
    # engines hanging under the wings (turbofan nacelles, intake to the left)
    for ex, ey, s_ in ((-8, 46, .78), (40, 112, 1.0)):
        o += f'<g transform="translate({ex} {ey}) scale({s_})">'
        o += f'<path d="M-6 -20 L40 -34 L64 -30 L30 -8Z" fill="#c8d2de" stroke="{LINE}" stroke-width="5" stroke-linejoin="round"/>'   # pylon
        o += f'<path d="M-50 -10 C-50 -34 -36 -40 0 -40 L74 -34 C96 -32 104 -22 104 -10 C104 2 96 12 74 14 L0 20 C-36 20 -50 14 -50 -10Z" fill="url(#engB)" stroke="{LINE}" stroke-width="6"/>'
        o += f'<ellipse cx="-48" cy="-10" rx="13" ry="29" fill="#2a3446" stroke="{LINE}" stroke-width="5"/>'
        o += '<ellipse cx="-46" cy="-10" rx="6" ry="16" fill="#5a6a82"/><circle cx="-46" cy="-10" r="4" fill="#c8d2de"/>'
        o += '<path d="M-30 -32 L70 -28" stroke="#ffffff" stroke-width="5" opacity=".85" stroke-linecap="round"/>'
        o += '</g>'
    return o



# ======================= B: WHERE WOULD YOU LAND?  (intuitive: lake / forest canopy / deep snow slope) =======================
random.seed(11)
HZ = 520
d = lin('skB', [(0, '#2a5a94'), (.55, '#7fb2d8'), (1, '#e6f2f6')])
d += rad('sunB', 1860, 60, 760, [(0, '#fffbe8', 1), (.12, '#fff3c8', .9), (.4, '#ffe8b0', .3), (1, '#ffe8b0', 0)])
d += lin('lakeB', [(0, '#5f8ab0'), (.35, '#1f4a72'), (1, '#0a1e36')])
d += lin('snowB', [(0, '#ffffff'), (.6, '#e2eef8'), (1, '#9fbcd8')], x2=1, y2=1)
d += rad('glowT', 960, 760, 380, [(0, '#fff2b0', .55), (1, '#fff2b0', 0)])
d += rad('glowS', 1560, 640, 420, [(0, '#fffbe0', .6), (1, '#fffbe0', 0)])
d += lin('fusB', [(0, '#ffffff'), (.55, '#eef2f7'), (1, '#b9c4d4')])
d += lin('wingN', [(0, '#f4f7fb'), (1, '#c4cedc')], x2=1, y2=1)
d += lin('wingF', [(0, '#c9d2de'), (1, '#e6ebf2')])
d += lin('finB', [(0, '#3a80cc'), (1, '#1f4f8e')], x2=1, y2=1)
d += lin('engB', [(0, '#ffffff'), (.6, '#e2e8f0'), (1, '#9aa8bc')])
d += '<filter id="bB"><feGaussianBlur stdDeviation="6"/></filter><filter id="bB2"><feGaussianBlur stdDeviation="2"/></filter>'
b = '<rect width="1920" height="1080" fill="url(#skB)"/><rect width="1920" height="1080" fill="url(#sunB)"/>'
b += '<circle cx="1860" cy="60" r="52" fill="#fffef6"/>'
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
for x0, y0, x1, y1, cx_, cy_ in ((1185, 470, 420, 820, 780, 560), (1215, 510, 960, 780, 1110, 620), (1250, 500, 1560, 650, 1440, 520)):
    b += f'<path d="M{x0} {y0} Q{cx_} {cy_} {x1} {y1}" stroke="#ffffff" stroke-width="7" stroke-dasharray="2 22" stroke-linecap="round" fill="none" opacity=".75"/>'
b += spark(960, 760, 28) + spark(1560, 640, 28) + spark(1040, 820, 16) + spark(1660, 560, 16) + spark(820, 760, 14, op=.7)
b += f'<g transform="translate(1215 420) rotate(10) scale(.6)">' + faller(suit='#d8572e', suit2='#9a3218', rim='#fff2c0') + '</g>'
# the airliner high above (where the fall begins), with contrails and a dotted drop line to the faller
b += '<path d="M1360 250 Q1290 300 1245 345" stroke="#ffffff" stroke-width="7" stroke-dasharray="2 22" stroke-linecap="round" fill="none" opacity=".8"/>'
b += f'<g transform="translate(1470 215) rotate(-8) scale(.78)"><g filter="url(#bB)" opacity=".6"><path d="M80 38 L700 60" stroke="#ffffff" stroke-width="16" stroke-linecap="round"/><path d="M150 104 L720 150" stroke="#ffffff" stroke-width="20" stroke-linecap="round"/></g>' + airliner() + '</g>'
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
