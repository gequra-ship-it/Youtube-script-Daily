# Thumbnails A-C for edge-of-universe (guideline 16-6, brief tools/briefs/thumb_art.md).
# A = homage to the Pale Blue Dot photo (Voyager 1 looks back; S05-S07: 75,000 years to Proxima Centauri)
# B = intuitive: the cosmic treadmill (S23-S25)
# C = intuitive: the Local Group sealed in a snow globe while outside galaxies drift away (S33, S40)
# run: python3 make.py   (from this folder or anywhere)
import os, sys, math, random
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', '..', 'tools'))
from thumb_lib import page, svg, lin, rad, stars, spark, blobs

INK = '#1d2b1c'; GREEN = '#6aa55a'; DARKG = '#4d8a4a'; BELLY = '#9cc98a'


# ---------- mascot frog (tools/assets/frog.svg), posable ----------
def arm(d):
    return (f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="7.5"/>'
            f'<path d="{d}" fill="none" stroke="{GREEN}" stroke-width="3.4"/>')


def hand_dot(x, y):   # round frog finger pad
    return f'<circle cx="{x}" cy="{y}" r="4.2" fill="{GREEN}" stroke="{INK}" stroke-width="2.4"/>'


def frog(x, y, s, flip=False, look=(0, 0), mouth='o', armL=None, armR=None, feet=None, helmet=False,
         rot=0, back='', front=''):
    sx = -s if flip else s
    g = [f'<g transform="translate({x} {y}) rotate({rot}) scale({sx} {s})" stroke="{INK}" stroke-linejoin="round" stroke-linecap="round">', back]
    if helmet:   # backpack behind the body
        g.append(f'<rect x="-46" y="-52" width="20" height="40" rx="6" fill="#c9ced8" stroke-width="3"/>')
    fl, fr = feet or ((-22, 4, 0), (22, 4, 0))
    for fx, fy, fa in (fl, fr):
        g.append(f'<ellipse cx="{fx}" cy="{fy}" rx="16" ry="9" transform="rotate({fa} {fx} {fy})" fill="{DARKG}" stroke-width="3.2"/>')
    g.append(f'<path d="M-34 0 q-6 -64 34 -70 q40 -2 42 62 q0 10 -6 12 q-36 6 -70 -4z" fill="{GREEN}" stroke-width="4"/>')
    g.append(f'<ellipse cx="2" cy="-12" rx="22" ry="20" fill="{BELLY}" stroke="none" opacity=".7"/>')
    g.append(f'<path d="M-24 -50 q6 -14 18 -16" fill="none" stroke="#a9d692" stroke-width="3" opacity=".8"/>')
    lx, ly = look
    for ex in (-10, 22):
        g.append(f'<circle cx="{ex}" cy="-66" r="13" fill="#f4f5ea" stroke-width="3.2"/>')
        g.append(f'<circle cx="{ex + 2 + lx}" cy="{-66 + ly}" r="5.4" fill="{INK}" stroke="none"/>')
        g.append(f'<circle cx="{ex + 3.6 + lx}" cy="{-68 + ly}" r="1.7" fill="#fff" stroke="none"/>')
    if mouth == 'o':
        g.append(f'<ellipse cx="6" cy="-42" rx="5.5" ry="6.5" fill="#3a1d1d" stroke-width="2.6"/>')
    elif mouth == 'grit':
        g.append(f'<path d="M-6 -44 h24 v6 h-24z" fill="#fff" stroke-width="2.6"/><path d="M0 -44v6M6 -44v6M12 -44v6" stroke-width="1.4"/>')
    else:
        g.append(f'<path d="M-8 -44 q14 12 28 0" fill="none" stroke-width="3.4"/>')
    g.append(f'<ellipse cx="-16" cy="-50" rx="5" ry="3" fill="#e88f86" stroke="none" opacity=".55"/><ellipse cx="28" cy="-50" rx="5" ry="3" fill="#e88f86" stroke="none" opacity=".55"/>')
    aL = armL or 'M-34 -22 q-14 6 -16 22'
    aR = armR or 'M38 -22 q14 6 16 22'
    g.append(arm(aL)); g.append(arm(aR))
    for a in (aL, aR):   # finger pads at the arm ends
        nums = [float(v) for v in a.replace('M', ' ').replace('q', ' ').replace('Q', ' ').replace('l', ' ').split()]
        x0, y0 = nums[0], nums[1]; ex_, ey_ = x0 + nums[-2], y0 + nums[-1]
        g.append(hand_dot(ex_, ey_))
    if helmet:   # glass bubble helmet + collar ring
        g.append(f'<ellipse cx="4" cy="-4" rx="44" ry="9" fill="#d8dde6" stroke-width="3"/>')
        g.append(f'<circle cx="4" cy="-48" r="52" fill="#bfe6ff" fill-opacity=".14" stroke="#e8f6ff" stroke-width="3.2" stroke-opacity=".9"/>')
        g.append(f'<path d="M-30 -78 q14 -18 38 -20" fill="none" stroke="#fff" stroke-width="5" opacity=".75"/>')
        g.append(f'<path d="M40 -30 q6 -10 6 -22" fill="none" stroke="#fff" stroke-width="3" opacity=".45"/>')
    g.append(front); g.append('</g>')
    return ''.join(g)


# ---------- spiral galaxy ----------
def galaxy(cx, cy, r, tilt, rotd, core, arm1, arm2, knot, arms=2, n=260, seed=1, gid='gx', wind=3.0):
    rnd = random.Random(seed)
    d = rad(f'{gid}h', 0, 0, r * 1.25, [(0, core, .55), (.25, arm1, .22), (1, arm1, 0)])
    d += rad(f'{gid}c', 0, 0, r * .38, [(0, '#ffffff', 1), (.25, core, .95), (1, core, 0)])
    b = f'<g transform="translate({cx} {cy}) rotate({rotd}) scale(1 {tilt})">'
    b += f'<circle r="{r * 1.25}" fill="url(#{gid}h)"/>'
    dots = ''; dust = ''; base = ''
    for k in range(arms):
        pts = []
        for i in range(60):
            t = i / 59; th = t * wind * math.pi + k * 2 * math.pi / arms; rr = r * (0.1 + 0.9 * t)
            pts.append(f'{rr * math.cos(th):.1f},{rr * math.sin(th):.1f}')
        base += f'<polyline points="{" ".join(pts)}" fill="none" stroke="{arm1}" stroke-width="{r * .16:.1f}" stroke-linecap="round" opacity=".38"/>'
        base += f'<polyline points="{" ".join(pts)}" fill="none" stroke="{arm2}" stroke-width="{r * .06:.1f}" stroke-linecap="round" opacity=".45"/>'
    b += f'<g filter="url(#blur12)">{base}</g>'
    for k in range(arms):
        for i in range(n * 2):
            t = i / (n * 2)
            th = t * wind * math.pi + k * 2 * math.pi / arms
            rr = r * (0.1 + 0.9 * t)
            jx, jy = rnd.gauss(0, r * .05 * (1 - t * .3)), rnd.gauss(0, r * .05)
            x, y = rr * math.cos(th) + jx, rr * math.sin(th) + jy
            col = arm1 if rnd.random() < .6 else arm2
            sz = (1 - t) * r * .018 + rnd.random() * r * .01 + 1.0
            dots += f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{sz:.1f}" fill="{col}" opacity="{.35 + .55 * rnd.random() * (1 - t * .5):.2f}"/>'
            if rnd.random() < .08:
                dots += f'<circle cx="{x + rnd.gauss(0, 4):.1f}" cy="{y + rnd.gauss(0, 4):.1f}" r="{rnd.uniform(1.6, 3.2):.1f}" fill="{knot}" opacity=".95"/>'
            if rnd.random() < .3 and t > .12:
                th2 = th - .22
                dust += f'<circle cx="{rr * .94 * math.cos(th2):.1f}" cy="{rr * .94 * math.sin(th2):.1f}" r="{sz * 1.4:.1f}" fill="#120a14" opacity=".28"/>'
    for _ in range(int(n * .9)):   # diffuse disc stars
        a = rnd.random() * 2 * math.pi; rr = abs(rnd.gauss(0, r * .45))
        dots += f'<circle cx="{rr * math.cos(a):.1f}" cy="{rr * math.sin(a):.1f}" r="{rnd.uniform(.8, 2.2):.1f}" fill="#fff" opacity="{rnd.uniform(.15, .6):.2f}"/>'
    b += f'{dust}<g filter="url(#soft)" opacity=".8">{dots}</g>{dots}'
    b += f'<circle r="{r * .38}" fill="url(#{gid}c)"/></g>'
    return d, b


def small_gal(rnd, x, y, s, col, kind):
    if kind == 'e':
        return (f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{s:.1f}" ry="{s * rnd.uniform(.5, .9):.1f}" transform="rotate({rnd.randint(0, 180)} {x:.0f} {y:.0f})" fill="{col}" opacity=".85" filter="url(#soft)"/>'
                f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{s * .35:.1f}" fill="#fff" opacity=".85"/>')
    a = rnd.randint(0, 180)
    return (f'<g transform="translate({x:.0f} {y:.0f}) rotate({a}) scale(1 {rnd.uniform(.35, .8):.2f})" opacity=".9">'
            f'<ellipse rx="{s:.1f}" ry="{s * .55:.1f}" fill="{col}" opacity=".5" filter="url(#soft)"/>'
            f'<path d="M0 0 q{s * .9:.1f} {-s * .2:.1f} {s * .7:.1f} {s * .7:.1f} M0 0 q{-s * .9:.1f} {s * .2:.1f} {-s * .7:.1f} {-s * .7:.1f}" fill="none" stroke="{col}" stroke-width="{max(1.5, s * .22):.1f}" stroke-linecap="round"/>'
            f'<circle r="{s * .28:.1f}" fill="#fff6dc"/></g>')


SOFT = '<filter id="soft" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="3"/></filter>' \
       '<filter id="blur12" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="12"/></filter>' \
       '<filter id="blur30" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="30"/></filter>'


def grain(rnd, n, col='#fff', op=.05):
    return ''.join(f'<rect x="{rnd.randint(0, 1919)}" y="{rnd.randint(0, 1079)}" width="2" height="2" fill="{col}" opacity="{op * rnd.random():.3f}"/>' for _ in range(n))


def starfield(rnd, n, box, skip=None, col='#eef4ff'):
    x0, y0, x1, y1 = box; out = ''
    for _ in range(n):
        x, y = rnd.randint(x0, x1), rnd.randint(y0, y1)
        if skip and skip(x, y): continue
        out += f'<circle cx="{x}" cy="{y}" r="{rnd.choice([1, 1.4, 1.9, 2.6])}" fill="{col}" opacity="{.15 + .6 * rnd.random():.2f}"/>'
    return out


def corner(x, y):   # bottom-right corner stays empty (duration badge)
    return x > 1560 and y > 840


# =========================== A: Pale Blue Dot ===========================
def make_A():
    rnd = random.Random(7)
    d = SOFT
    d += lin('aBg', [(0, '#0d0907'), (.6, '#120b09'), (1, '#0a0706')])
    body = '<rect width="1920" height="1080" fill="url(#aBg)"/>'
    # scattered-sunlight rays of the 1990 photo: broad slanted bands, soft edges
    bands = [(300, 560, '#c27a3e', .34), (700, 830, '#7d8fb0', .20), (930, 1090, '#b46a7a', .17), (1560, 1760, '#c58b4c', .16)]
    for i, (a, b, c, o) in enumerate(bands):
        d += lin(f'band{i}', [(0, c), (.5, c), (1, c)], x2=1, y2=0)
        d += (f'<linearGradient id="bm{i}" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{c}" stop-opacity="0"/>'
              f'<stop offset=".5" stop-color="{c}" stop-opacity="{o}"/><stop offset="1" stop-color="{c}" stop-opacity="0"/></linearGradient>')
        body += f'<polygon points="{a},1080 {b},1080 {b + 330},0 {a + 330},0" fill="url(#bm{i})"/>'
        # thin bright streak inside the band
        m = (a + b) / 2
        body += f'<polygon points="{m - 6},1080 {m + 6},1080 {m + 336},0 {m + 324},0" fill="{c}" opacity="{o * .6:.2f}"/>'
    body += grain(rnd, 2600, '#ffdcb0', .10)
    body += starfield(rnd, 160, (0, 0, 1920, 1080), corner, '#f3e6d6')
    # sun glare from off-frame left (source of the rays)
    d += rad('aSun', -160, 980, 700, [(0, '#ffcf8a', .45), (.4, '#d48a4a', .12), (1, '#000', 0)])
    body += '<rect width="1920" height="1080" fill="url(#aSun)"/>'
    # the pale blue dot (Earth), inside the warm band
    px, py = 470, 840
    d += rad('dotG', px, py, 90, [(0, '#cfe9ff', .9), (.12, '#8fc2ff', .5), (.5, '#5d8fd6', .12), (1, '#000', 0)])
    body += f'<circle cx="{px}" cy="{py}" r="90" fill="url(#dotG)"/>'
    body += f'<circle cx="{px}" cy="{py}" r="13" fill="#7fb2f0"/><circle cx="{px - 3}" cy="{py - 3}" r="6" fill="#d8ecff"/>'
    body += f'<circle cx="{px}" cy="{py}" r="44" fill="none" stroke="#bfe0ff" stroke-width="2.5" opacity=".4"/>'

    # ---- Voyager 1 ----
    cx, cy, rx, ry, th = 1290, 540, 250, 210, -30
    # magnetometer boom (13 m) to the upper right, truss
    bx, by = 1540, 470
    ex, ey = 1960, 70
    truss = ''
    L = math.hypot(ex - bx, ey - by); ux, uy = (ex - bx) / L, (ey - by) / L; nx, ny = -uy, ux
    for k in range(0, int(L), 26):
        p1 = (bx + ux * k + nx * 6, by + uy * k + ny * 6); p2 = (bx + ux * (k + 26) - nx * 6, by + uy * (k + 26) - ny * 6)
        truss += f'M{p1[0]:.0f} {p1[1]:.0f}L{p2[0]:.0f} {p2[1]:.0f}'
    body += (f'<path d="M{bx + nx * 6:.0f} {by + ny * 6:.0f}L{ex + nx * 6:.0f} {ey + ny * 6:.0f}M{bx - nx * 6:.0f} {by - ny * 6:.0f}L{ex - nx * 6:.0f} {ey - ny * 6:.0f}{truss}" '
             f'stroke="#7a6a58" stroke-width="2.6" fill="none"/>')
    body += f'<path d="M{bx + nx * 6:.0f} {by + ny * 6:.0f}L{ex + nx * 6:.0f} {ey + ny * 6:.0f}" stroke="#f0c896" stroke-width="1.6" opacity=".7"/>'
    # RTG boom down-left behind the dish, three finned RTG cylinders peeking below the dish
    body += '<path d="M1450 600 L1215 905 M1462 612 L1228 915" stroke="#6d5f50" stroke-width="5"/>'
    for i in range(3):
        rx0, ry0 = 1300 - i * 46, 800 + i * 58
        body += (f'<g transform="translate({rx0} {ry0}) rotate(38)">'
                 f'<rect x="-30" y="-22" width="60" height="44" rx="6" fill="#3d342d" stroke="#120c0a" stroke-width="3"/>'
                 + ''.join(f'<rect x="{-28 + j * 12}" y="-34" width="5" height="68" fill="#5a4b3e" stroke="#120c0a" stroke-width="1.5"/>' for j in range(5))
                 + '<rect x="-30" y="-22" width="60" height="10" fill="#c8915a" opacity=".55"/></g>')
    # science boom to the right with the scan platform (cameras)
    body += '<path d="M1600 520 L1790 440 M1604 534 L1794 454" stroke="#7a6a58" stroke-width="5"/>'
    body += ('<g transform="translate(1800 430) rotate(-10)">'
             '<rect x="-40" y="-36" width="80" height="62" rx="6" fill="#4a3e33" stroke="#120c0a" stroke-width="3"/>'
             '<rect x="-40" y="-36" width="80" height="14" fill="#d9a25f" opacity=".6"/>'
             '<rect x="-18" y="-80" width="36" height="50" rx="5" fill="#2c2520" stroke="#120c0a" stroke-width="3"/>'
             '<circle cx="0" cy="-80" r="16" fill="#1b2635" stroke="#120c0a" stroke-width="3"/><circle cx="-4" cy="-84" r="5" fill="#9ec8ff" opacity=".8"/>'
             '<rect x="24" y="-66" width="26" height="34" rx="4" fill="#2c2520" stroke="#120c0a" stroke-width="3"/>'
             '<circle cx="37" cy="-66" r="10" fill="#1b2635" stroke="#120c0a" stroke-width="2.5"/></g>')
    # bus: ten-sided box, gold thermal blanket, Golden Record
    d += lin('foil', [(0, '#f6d48a'), (.35, '#b07a33'), (.7, '#e0aa5c'), (1, '#6e4518')], x2=1, y2=1)
    body += ('<polygon points="1430,430 1560,410 1640,450 1650,560 1580,610 1450,620 1400,560" fill="url(#foil)" stroke="#1a110a" stroke-width="5"/>')
    for _ in range(26):   # foil crinkles
        x = rnd.randint(1420, 1630); y = rnd.randint(430, 600)
        body += f'<path d="M{x} {y} l{rnd.randint(-22, 22)} {rnd.randint(-14, 14)}" stroke="#fff3c8" stroke-width="1.6" opacity=".45"/>'
    body += '<path d="M1560 410 L1580 610 M1430 430 L1450 620" stroke="#5c3a14" stroke-width="2.5" opacity=".6"/>'
    d += rad('rec', 1610, 528, 38, [(0, '#fff4c8', 1), (.4, '#F2D27A', 1), (1, '#a8761f', 1)])
    body += '<ellipse cx="1612" cy="530" rx="30" ry="38" fill="url(#rec)" stroke="#3a2507" stroke-width="3"/>'
    body += ''.join(f'<ellipse cx="1612" cy="530" rx="{r * .79:.1f}" ry="{r:.1f}" fill="none" stroke="#8a5f17" stroke-width="1" opacity=".55"/>' for r in (12, 18, 24, 30))
    body += '<circle cx="1612" cy="530" r="4" fill="#3a2507"/>'
    # dish: back shell crescent then the bright interior (light from the low-left, where the sun is)
    d += rad('dishIn', cx - 120, cy + 120, 430, [(0, '#ffffff', 1), (.45, '#ece6dc', 1), (.8, '#b7ada0', 1), (1, '#7d7266', 1)])
    d += lin('dishBack', [(0, '#5a5048'), (1, '#2a231f')], x2=1, y2=1)
    body += f'<ellipse cx="{cx + 46}" cy="{cy - 36}" rx="{rx}" ry="{ry}" transform="rotate({th} {cx + 46} {cy - 36})" fill="url(#dishBack)" stroke="#120c0a" stroke-width="6"/>'
    body += f'<ellipse cx="{cx}" cy="{cy}" rx="{rx + 30}" ry="{ry + 30}" transform="rotate({th} {cx} {cy})" fill="#ffd9a8" opacity=".10" filter="url(#blur12)"/>'
    body += f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" transform="rotate({th} {cx} {cy})" fill="url(#dishIn)" stroke="#120c0a" stroke-width="6"/>'
    # ribs and rim
    ribs = ''
    for k in range(16):
        t = k * 2 * math.pi / 16
        px_ = rx * math.cos(t); py_ = ry * math.sin(t)
        ribs += f'M0 0L{px_:.0f} {py_:.0f}'
    body += f'<g transform="translate({cx} {cy}) rotate({th})"><path d="{ribs}" stroke="#9a8f82" stroke-width="2" opacity=".55"/>'
    body += ''.join(f'<ellipse rx="{rx * f:.0f}" ry="{ry * f:.0f}" fill="none" stroke="#a69a8c" stroke-width="1.6" opacity=".45"/>' for f in (.33, .66))
    body += f'<ellipse rx="{rx - 8}" ry="{ry - 8}" fill="none" stroke="#fff" stroke-width="4" opacity=".55" stroke-dasharray="500 1400" stroke-dashoffset="-700"/></g>'
    # feed struts and subreflector, standing out of the dish toward the viewer
    sx_, sy_ = cx - 70, cy + 58
    for t in (0.6, 2.7, 4.5):
        x = cx + rx * .92 * math.cos(t) * .866 - ry * .92 * math.sin(t) * -.5
        y = cy + rx * .92 * math.cos(t) * -.5 + ry * .92 * math.sin(t) * .866
        body += f'<path d="M{x:.0f} {y:.0f}L{sx_} {sy_}" stroke="#3a322b" stroke-width="7"/><path d="M{x:.0f} {y:.0f}L{sx_} {sy_}" stroke="#d9cfc2" stroke-width="2.5"/>'
    body += f'<ellipse cx="{sx_}" cy="{sy_}" rx="34" ry="26" transform="rotate(-30 {sx_} {sy_})" fill="#efe9df" stroke="#120c0a" stroke-width="4"/>'
    body += f'<ellipse cx="{sx_ - 6}" cy="{sy_ + 4}" rx="16" ry="11" transform="rotate(-30 {sx_} {sy_})" fill="#fff"/>'
    body += f'<path d="M{cx} {cy}L{sx_} {sy_}" stroke="#2a231f" stroke-width="12" opacity=".35"/>'
    # warm rim light on the lower-left edge of the dish
    body += (f'<ellipse cx="{cx}" cy="{cy}" rx="{rx + 2}" ry="{ry + 2}" transform="rotate({th} {cx} {cy})" fill="none" stroke="#ffd29a" stroke-width="7" '
             f'stroke-dasharray="420 1600" stroke-dashoffset="-560" opacity=".9"/>')
    body += spark(1088, 690, 26, '#fff1d6', .95)
    # frog on the dish rim, bubble helmet, pointing back at the dot
    fx, fy = 1468, 360
    body += frog(fx, fy, 2.75, look=(-4, 4), mouth='o', helmet=True,
                 armL='M-34 -22 q-24 -2 -40 18', armR='M38 -22 q12 10 12 22', feet=((-22, 4, -8), (22, 6, 10)))
    body += spark(1290, 170, 18) + spark(780, 620, 14, '#ffe8c8', .7) + spark(1750, 250, 16)
    lines = [('NEXT STAR:', 112, 'w'), ('75,000', 220, 'y'), ('YEARS', 150, 'w')]
    return page('#0b0807', svg(d, body), lines, outline='#120a06')


# =========================== B: cosmic treadmill ===========================
def make_B():
    rnd = random.Random(11)
    d = SOFT
    d += lin('bBg', [(0, '#120a2a'), (.55, '#1d0f38'), (1, '#07040f')])
    body = '<rect width="1920" height="1080" fill="url(#bBg)"/>'
    body += blobs(16, 1100, 60, 1900, 600, '#8a3fb8', .05, .12, 120, 260)
    body += blobs(10, 1200, 100, 1800, 500, '#e0619b', .04, .09, 80, 200)
    body += starfield(rnd, 260, (0, 0, 1920, 1080), corner)
    gd, gb = galaxy(1450, 300, 330, .5, -18, '#fff0c8', '#a7b4ff', '#d78cff', '#ff8fb8', arms=2, n=300, seed=3, gid='gB')
    d += gd
    body += gb
    body += spark(1150, 140, 22) + spark(1790, 470, 18) + spark(1700, 120, 14)
    # treadmill (3/4 view, running toward the galaxy on the right)
    FL, FR, BR, BL = (230, 880), (1420, 880), (1500, 790), (330, 790)
    d += lin('belt', [(0, '#2b2160'), (1, '#120c2c')])
    d += lin('skirt', [(0, '#8d97b3'), (.3, '#4b536d'), (1, '#1f2333')])
    d += f'<clipPath id="beltClip"><polygon points="{BL[0]},{BL[1]} {BR[0]},{BR[1]} {FR[0]},{FR[1]} {FL[0]},{FL[1]}"/></clipPath>'
    # shadow and legs
    body += '<ellipse cx="860" cy="985" rx="720" ry="40" fill="#000" opacity=".5" filter="url(#blur12)"/>'
    for lx in (300, 1380):
        body += f'<rect x="{lx}" y="920" width="34" height="58" rx="6" fill="#2a2f40" stroke="#06070c" stroke-width="4"/>'
    # back rail post and back handrail (behind belt)
    body += '<path d="M1488 792 L1468 540" stroke="#06070c" stroke-width="22" stroke-linecap="round"/><path d="M1488 792 L1468 540" stroke="#7c86a3" stroke-width="12" stroke-linecap="round"/>'
    body += '<path d="M1468 560 L1210 560" stroke="#06070c" stroke-width="18" stroke-linecap="round"/><path d="M1468 560 L1210 560" stroke="#8e98b5" stroke-width="8" stroke-linecap="round"/>'
    # belt surface
    body += f'<polygon points="{BL[0]},{BL[1]} {BR[0]},{BR[1]} {FR[0]},{FR[1]} {FL[0]},{FL[1]}" fill="url(#belt)"/>'
    bt = '<g clip-path="url(#beltClip)">'
    for k in range(-2, 26):   # belt slats (skewed)
        x = 230 + k * 52
        bt += f'<path d="M{x} 880 L{x + 100} 790" stroke="#3d3486" stroke-width="3" opacity=".7"/>'
    for _ in range(90):   # stars on the belt, streaked backward (moving left)
        y = rnd.randint(795, 878); x = rnd.randint(240, 1500); L = rnd.randint(30, 160)
        c = rnd.choice(['#ffffff', '#cfd8ff', '#ffc3e1', '#F2D27A'])
        bt += f'<path d="M{x} {y} h{L}" stroke="{c}" stroke-width="{rnd.choice([1.5, 2.2, 3])}" opacity="{rnd.uniform(.25, .7):.2f}" stroke-linecap="round"/>'
        bt += f'<circle cx="{x}" cy="{y}" r="{rnd.choice([2, 2.6, 3.4])}" fill="#fff" opacity=".9"/>'
    for k in range(5):    # glowing chevrons showing the belt direction
        x = 420 + k * 230; y = 836
        bt += f'<path d="M{x + 34} {y - 24} L{x} {y} L{x + 34} {y + 24}" fill="none" stroke="#ff6fae" stroke-width="9" stroke-linecap="round" stroke-linejoin="round" opacity=".55"/>'
    bt += '</g>'
    body += bt
    body += f'<path d="M{BL[0]} {BL[1]} L{BR[0]} {BR[1]}" stroke="#a4add0" stroke-width="3" opacity=".6"/>'
    # front skirt and end caps (rollers)
    body += f'<polygon points="{FL[0]},{FL[1]} {FR[0]},{FR[1]} {FR[0]},{FR[1] + 50} {FL[0]},{FL[1] + 50}" fill="url(#skirt)" stroke="#06070c" stroke-width="5"/>'
    body += f'<path d="M{FL[0] + 6} {FL[1] + 6} H{FR[0] - 6}" stroke="#d7def5" stroke-width="3" opacity=".8"/>'
    body += f'<polygon points="{FR[0]},{FR[1]} {BR[0]},{BR[1]} {BR[0]},{BR[1] + 50} {FR[0]},{FR[1] + 50}" fill="#2a2f40" stroke="#06070c" stroke-width="5"/>'
    body += f'<ellipse cx="{FL[0] + 4}" cy="{FL[1] + 2}" rx="26" ry="50" transform="rotate(-48 {FL[0] + 4} {FL[1] + 2})" fill="#5a6380" stroke="#06070c" stroke-width="5"/>'
    for k in range(4):   # neon strip on the skirt
        body += f'<rect x="{360 + k * 270}" y="{FL[1] + 20}" width="120" height="8" rx="4" fill="#ff6fae" opacity=".7"/>'
    # stars spilling off the back (left) end into the dark
    for i in range(16):
        x = 220 - rnd.randint(0, 200); y = 860 + rnd.randint(0, 210)
        L = rnd.randint(20, 60)
        body += f'<path d="M{x} {y} l{L} {-L * .7:.0f}" stroke="#cfd8ff" stroke-width="2" opacity="{rnd.uniform(.2, .55):.2f}" stroke-linecap="round"/><circle cx="{x}" cy="{y}" r="2.6" fill="#fff" opacity=".7"/>'
    d += rad('voidL', 0, 1000, 520, [(0, '#000', .85), (1, '#000', 0)])
    body += '<rect width="1920" height="1080" fill="url(#voidL)"/>'
    # runner: the frog in a bubble helmet, sprinting right, sweating
    fx, fy = 960, 850
    sweat = ''.join(f'<path d="M{x} {y} q-5 9 0 13 q5 -4 0 -13z" fill="#bfe6ff" stroke="{INK}" stroke-width="1.8"/>' for x, y in ((-58, -84), (-66, -60), (64, -92)))
    body += f'<ellipse cx="{fx}" cy="{fy + 6}" rx="100" ry="14" fill="#000" opacity=".45"/>'
    body += frog(fx, fy, 3.0, look=(5, -2), mouth='grit', helmet=True, rot=10,
                 armL='M-34 -22 q-20 -6 -30 -26', armR='M38 -22 q18 4 30 -10',
                 feet=((-34, -6, -40), (30, 6, 20)), front=sweat)
    for k in range(4):   # speed lines (he runs right, but the belt wins)
        body += f'<path d="M{760 - k * 18} {640 + k * 46} h{-90 - k * 20}" stroke="#ffffff" stroke-width="5" opacity="{.5 - k * .08:.2f}" stroke-linecap="round"/>'
    # front post, console, front handrail (in front of the belt)
    body += '<path d="M1410 882 L1392 560" stroke="#06070c" stroke-width="24" stroke-linecap="round"/><path d="M1410 882 L1392 560" stroke="#a3acc7" stroke-width="13" stroke-linecap="round"/>'
    body += '<path d="M1395 600 L1190 600" stroke="#06070c" stroke-width="20" stroke-linecap="round"/><path d="M1395 600 L1190 600" stroke="#b5bed8" stroke-width="9" stroke-linecap="round"/>'
    body += '<path d="M1395 596 L1200 596" stroke="#fff" stroke-width="2.4" opacity=".7"/>'
    body += '<polygon points="1340,520 1530,478 1548,540 1360,590" fill="#2c3246" stroke="#06070c" stroke-width="6"/>'
    body += '<polygon points="1366,530 1514,498 1526,536 1378,570" fill="#12051a"/>'
    for k in range(9):   # speed bars, all lit, last ones red
        c = '#ff3b5c' if k > 5 else '#ff9ec4'
        h = 6 + k * 2.6
        x = 1378 + k * 15; y = 562 - k * 3.4
        body += f'<rect x="{x}" y="{y - h:.0f}" width="9" height="{h:.0f}" fill="{c}"/>'
    body += '<polygon points="1366,530 1514,498 1526,536 1378,570" fill="#ff3b5c" opacity=".12" filter="url(#blur12)"/>'
    body += spark(1530, 486, 16, '#ffc1d6', .9)
    lines = [('CAN YOU', 128, 'w'), ('OUTRUN', 212, 'y'), ('SPACE?', 168, 'w')]
    return page('#120a2a', svg(d, body), lines, outline='#0a0418')


# =========================== C: snow globe ===========================
def make_C():
    rnd = random.Random(23)
    d = SOFT
    d += lin('cBg', [(0, '#04101a'), (.6, '#071a24'), (1, '#030a10')])
    body = '<rect width="1920" height="1080" fill="url(#cBg)"/>'
    body += starfield(rnd, 220, (0, 0, 1920, 1080), corner, '#e6fbff')
    gx, gy, gr = 1310, 520, 318
    # distant galaxies outside the globe: redder and fainter the farther out, streaking away
    for _ in range(70):
        a = rnd.uniform(0, 2 * math.pi); dist = rnd.uniform(gr + 60, 1100)
        x, y = gx + dist * math.cos(a), gy + dist * math.sin(a)
        if not (0 < x < 1920 and 0 < y < 1080) or corner(x, y) or (x < 1000 and y < 470): continue
        f = min(1, (dist - gr) / 700)
        col = ['#fff1c8', '#ffc98a', '#ff8a5c', '#d8443a'][min(3, int(f * 4))]
        s = rnd.uniform(8, 24) * (1 - f * .4)
        L = 20 + f * 70
        body += (f'<path d="M{x:.0f} {y:.0f} l{L * math.cos(a):.0f} {L * math.sin(a):.0f}" stroke="{col}" stroke-width="{s * .6:.1f}" '
                 f'stroke-linecap="round" opacity="{.18 * (1 - f) + .06:.2f}"/>')
        body += small_gal(rnd, x, y, s, col, rnd.choice('es'))
    # a few bigger receding galaxies with red glow
    for (x, y, s, a) in ((1800, 150, 44, 30), (1820, 600, 36, -10), (700, 880, 42, 60), (330, 760, 34, 0), (1000, 1010, 28, 0)):
        if s == 0: continue
        body += f'<circle cx="{x}" cy="{y}" r="{s * 2.4}" fill="#ff6a4a" opacity=".14" filter="url(#blur12)"/>'
        body += small_gal(rnd, x, y, s, '#ff9a6a', 's')
    # ghost of a larger globe (the reachable region shrinks), with inward chevrons
    body += f'<circle cx="{gx}" cy="{gy}" r="{gr + 110}" fill="none" stroke="#7fe3ff" stroke-width="3" stroke-dasharray="4 16" stroke-linecap="round" opacity=".45"/>'
    for a in (-150, -30, 15, 160):
        t = math.radians(a); x, y = gx + (gr + 70) * math.cos(t), gy + (gr + 70) * math.sin(t)
        body += (f'<g transform="translate({x:.0f} {y:.0f}) rotate({a + 180})"><path d="M-14 -18 L10 0 L-14 18" fill="none" stroke="#7fe3ff" '
                 f'stroke-width="7" stroke-linecap="round" stroke-linejoin="round" opacity=".7"/></g>')
    # globe interior: our Local Group
    d += rad('gIn', gx, gy - 40, gr, [(0, '#1b3d63', 1), (.7, '#0f2440', 1), (1, '#0a1626', 1)])
    d += f'<clipPath id="gClip"><circle cx="{gx}" cy="{gy}" r="{gr - 4}"/></clipPath>'
    body += f'<circle cx="{gx}" cy="{gy}" r="{gr + 40}" fill="#7fe3ff" opacity=".18" filter="url(#blur30)"/>'
    body += f'<circle cx="{gx}" cy="{gy}" r="{gr}" fill="url(#gIn)"/>'
    inner = f'<g clip-path="url(#gClip)">'
    inner += starfield(rnd, 140, (gx - gr, gy - gr, gx + gr, gy + gr), None, '#fff')
    g1d, g1b = galaxy(gx - 70, gy - 70, 175, .62, -25, '#fff1cc', '#8fc8ff', '#c7a8ff', '#ff9ec0', arms=2, n=240, seed=5, gid='mw')
    g2d, g2b = galaxy(gx + 150, gy - 175, 82, .38, 32, '#ffe9c0', '#b8d4ff', '#e3c7ff', '#ffb0c8', arms=2, n=120, seed=9, gid='an')
    g3d, g3b = galaxy(gx + 165, gy + 40, 46, .55, -60, '#fff3d0', '#9fdcff', '#c9e6ff', '#ffc0d0', arms=2, n=70, seed=13, gid='tr')
    d += g1d + g2d + g3d
    inner += g2b + g3b + g1b
    for _ in range(9):   # dwarf satellite galaxies
        x, y = gx + rnd.randint(-230, 230), gy + rnd.randint(-230, 150)
        inner += f'<circle cx="{x}" cy="{y}" r="{rnd.randint(5, 10)}" fill="#cfe9ff" opacity=".55" filter="url(#soft)"/><circle cx="{x}" cy="{y}" r="2" fill="#fff"/>'
    # "snow": drifting glitter stars
    for _ in range(40):
        x, y = gx + rnd.randint(-300, 300), gy + rnd.randint(-300, 300)
        inner += f'<circle cx="{x}" cy="{y}" r="{rnd.uniform(1.5, 3.6):.1f}" fill="#ffffff" opacity="{rnd.uniform(.4, .9):.2f}"/>'
    # floor mound inside the globe
    inner += f'<ellipse cx="{gx}" cy="{gy + gr + 30}" rx="{gr * .95:.0f}" ry="120" fill="#20304a"/>'
    inner += f'<ellipse cx="{gx}" cy="{gy + gr - 70}" rx="{gr * .8:.0f}" ry="24" fill="#3a5578" opacity=".6"/>'
    inner += '</g>'
    body += inner
    # frog inside the globe, palm on the glass, looking out at the fleeing galaxies
    fx, fy = 1400, 800
    body += frog(fx, fy, 2.6, look=(5, -3), mouth='o',
                 armR='M38 -22 q20 -16 34 -40', armL='M-34 -22 q-14 6 -16 22', feet=((-22, 4, 0), (24, 4, 12)))
    # glass: rim, reflections, highlight
    d += rad('glass', gx - 120, gy - 150, gr * 1.3, [(0, '#ffffff', .0), (.75, '#bdf1ff', .05), (.95, '#bdf1ff', .12), (1, '#e9fbff', .28)])
    body += f'<circle cx="{gx}" cy="{gy}" r="{gr}" fill="url(#glass)" stroke="#d6f6ff" stroke-width="5" stroke-opacity=".85"/>'
    body += f'<path d="M{gx - 250} {gy - 120} A{gr - 40} {gr - 40} 0 0 1 {gx - 60} {gy - gr + 44}" fill="none" stroke="#fff" stroke-width="16" stroke-linecap="round" opacity=".55"/>'
    body += f'<path d="M{gx - 268} {gy - 40} A{gr - 40} {gr - 40} 0 0 1 {gx - 262} {gy - 90}" fill="none" stroke="#fff" stroke-width="10" stroke-linecap="round" opacity=".45"/>'
    body += f'<path d="M{gx + 230} {gy + 170} A{gr - 30} {gr - 30} 0 0 1 {gx + 120} {gy + 250}" fill="none" stroke="#bff3ff" stroke-width="6" stroke-linecap="round" opacity=".35"/>'
    # hand-print glow where the frog presses the glass
    body += f'<circle cx="{fx + 2.6 * 72:.0f}" cy="{fy - 2.6 * 62:.0f}" r="34" fill="#9ff0ff" opacity=".35" filter="url(#blur12)"/>'
    body += f'<circle cx="{fx + 2.6 * 72:.0f}" cy="{fy - 2.6 * 62:.0f}" r="22" fill="none" stroke="#c9f8ff" stroke-width="2.5" opacity=".7"/>'
    # base: brass and dark wood
    d += lin('brass', [(0, '#fff0b8'), (.3, '#F2D27A'), (.7, '#a87a2c'), (1, '#5a3c10')], x2=1, y2=0)
    d += lin('wood', [(0, '#5b3420'), (1, '#24130a')])
    by = gy + gr - 40
    body += f'<path d="M{gx - 250} {by} L{gx + 250} {by} L{gx + 300} {by + 120} L{gx - 300} {by + 120} Z" fill="url(#wood)" stroke="#120804" stroke-width="6"/>'
    body += f'<rect x="{gx - 262}" y="{by - 16}" width="524" height="34" rx="10" fill="url(#brass)" stroke="#2a1a05" stroke-width="5"/>'
    body += f'<rect x="{gx - 312}" y="{by + 112}" width="624" height="30" rx="8" fill="url(#brass)" stroke="#2a1a05" stroke-width="5"/>'
    body += f'<path d="M{gx - 230} {by + 60} H{gx + 230}" stroke="#F2D27A" stroke-width="3" opacity=".35"/>'
    body += f'<ellipse cx="{gx}" cy="{by + 150}" rx="360" ry="22" fill="#000" opacity=".5" filter="url(#blur12)"/>'
    body += spark(gx - 230, gy - 230, 26) + spark(gx + 40, gy - 330, 18, '#e9fbff') + spark(1780, 330, 16, '#ffd2b8', .7)
    lines = [('OUR REACH', 118, 'w'), ('IS', 104, 'w'), ('SHRINKING', 158, 'y')]
    return page('#04101a', svg(d, body), lines, outline='#03080e')


if __name__ == '__main__':
    for n, f in (('A', make_A), ('B', make_B), ('C', make_C)):
        open(os.path.join(HERE, f'{n}.html'), 'w').write(f())
        print('wrote', n)
