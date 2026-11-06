# Shorts thumbnails (guideline 16-9, brief tools/briefs/thumb_art.md) for dark-matter-96-percent-short1..5, one A.html each.
# Run: python3 videos/dark-matter-96-percent-short1/thumb/make_all.py [1 2 3 4 5]  -> videos/dark-matter-96-percent-shortN/thumb/A.html
# Frog and helpers copied from videos/dark-matter-96-percent/thumb/make.py (long-form A/B/C: Titanic iceberg, galaxy halo, cosmic pie: not reused here).
# 1 ALL THIS IS UNDER 5%   desk under a lamp is solid, the rest of the room is a ghost outline. short1 S01, S04-S07 ("adds up to just under 5 percent").
# 2 WHO LEFT THESE?        footprints in the snow, nobody there, frog detective. short2 S09-S10 ("detective who finds footprints in the snow").
# 3 NOT BLACK. INVISIBLE   frog sails a boat on an invisible ocean, only the wake shows. short3 S01-S02, S07-S08 ("dark does not mean a dark color").
# 4 IT'S SPEEDING UP       a thrown ball that rises faster and faster, galaxies racing apart. short4 S02-S04 ("It is speeding up").
# 5 WE CAN READ 5 PAGES    huge library, only five glowing pages readable. short5 S03 ("you can read merely five pages").
import os, sys, math, random
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', '..', 'tools'))
from thumb_lib import page, svg, lin, rad, spark, vpage, vsvg

INK = '#1d2b1c'; GREEN = '#6aa55a'; DARKG = '#4d8a4a'; BELLY = '#9cc98a'
FILTERS = ''.join(f'<filter id="b{n}" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="{n}"/></filter>' for n in (2, 3, 6, 12, 24, 50))


def poly(pts):
    return 'M' + ' L'.join(f'{x:.1f},{y:.1f}' for x, y in pts) + 'Z'


def path(pts):
    return 'M' + ' L'.join(f'{x:.1f},{y:.1f}' for x, y in pts)


# ---------------- mascot frog (tools/assets/frog.svg body), posable ----------------
def limb(d, w=7.5, wi=3.4):
    return f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="{w}"/><path d="{d}" fill="none" stroke="{GREEN}" stroke-width="{wi}"/>'


def end_of(d):
    n = [float(v) for v in d.replace('M', ' ').replace('q', ' ').split()]
    return n[0] + n[-2], n[1] + n[-1]


def frog(x, y, s, rot=0, flip=False, look=(0, 0), mouth='O', armL=None, armR=None, legs=None, helmet=False,
         back='', front='', mid='', hat=''):
    sx = -s if flip else s
    g = [f'<g transform="translate({x} {y}) rotate({rot}) scale({sx} {s})" stroke="{INK}" stroke-linejoin="round" stroke-linecap="round">', back]
    if helmet:   # backpack
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
    if helmet:   # space helmet bubble
        g.append('<circle cx="6" cy="-56" r="47" fill="#cfeaff" fill-opacity=".13" stroke="#eef6ff" stroke-width="4.5"/>')
        g.append('<path d="M-28 -80 q12 -18 32 -21" fill="none" stroke="#fff" stroke-width="5" opacity=".8"/><path d="M44 -40 q6 -10 6 -22" fill="none" stroke="#fff" stroke-width="3" opacity=".5"/>')
        g.append('<ellipse cx="6" cy="-12" rx="42" ry="9" fill="#e6eaf2" stroke-width="3.2"/><path d="M-30 -14 q36 8 72 0" fill="none" stroke="#fff" stroke-width="2.2" opacity=".8"/>')
    g.append(mid)
    for a in (armL or 'M-34 -22 q-14 6 -16 22', armR or 'M38 -22 q14 6 16 22'):
        g.append(limb(a)); ex_, ey_ = end_of(a)
        g.append(f'<circle cx="{ex_:.1f}" cy="{ey_:.1f}" r="5.6" fill="{GREEN}" stroke-width="3"/>')
    g.append(front); g.append('</g>')
    return ''.join(g)


def mini_galaxy(cx, cy, r, rot, col='#fff2c8', arms=2, n=70, rnd=None, op=1.0):
    rnd = rnd or random.Random(1)
    o = f'<g transform="translate({cx} {cy}) rotate({rot}) scale(1 .45)">'
    o += f'<circle r="{r * .9:.0f}" fill="{col}" opacity="{.25 * op:.2f}" filter="url(#b6)"/>'
    for a in range(arms):
        for k in range(n):
            t = k / n
            ang = a * 2 * math.pi / arms + t * 3.6
            rr = r * (.12 + .95 * t)
            x, y = rr * math.cos(ang) + rnd.gauss(0, r * .05), rr * math.sin(ang) + rnd.gauss(0, r * .05)
            o += f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{rnd.uniform(.8, 2.4) * (1 - t * .5) * max(1, r / 60):.1f}" fill="{col}" opacity="{op * rnd.uniform(.5, 1):.2f}"/>'
    o += f'<circle r="{r * .2:.0f}" fill="#fff" opacity="{op:.2f}" filter="url(#b3)"/><circle r="{r * .1:.0f}" fill="#fff" opacity="{op:.2f}"/></g>'
    return o


def cosmic_web(nodes, rnd, glow='#b46bff', core='#f0e0ff', knot='#ffffff', w=1.0, k=3, maxd=260, dots=26, op=1.0):
    """Large-scale structure: glowing filaments between nearest nodes, bright knots at the nodes, dark voids between."""
    edges = set()
    for i, (x, y) in enumerate(nodes):
        near = sorted(((math.hypot(x - u, y - v), j) for j, (u, v) in enumerate(nodes) if j != i))[:k]
        for dd, j in near:
            if dd < maxd:
                edges.add((min(i, j), max(i, j)))
    lo = hi = dt = ''
    for i, j in edges:
        (x0, y0), (x1, y1) = nodes[i], nodes[j]
        L = math.hypot(x1 - x0, y1 - y0); bend = rnd.uniform(-.18, .18) * L
        mx, my = (x0 + x1) / 2 - (y1 - y0) / L * bend, (y0 + y1) / 2 + (x1 - x0) / L * bend
        dpath = f'M{x0:.0f} {y0:.0f} Q{mx:.0f} {my:.0f} {x1:.0f} {y1:.0f}'
        lo += f'<path d="{dpath}" stroke-width="{16 * w:.1f}"/>'
        hi += f'<path d="{dpath}" stroke-width="{2.6 * w:.1f}"/>'
        for _ in range(int(dots * L / 200)):
            t = rnd.random()
            px = (1 - t) ** 2 * x0 + 2 * t * (1 - t) * mx + t * t * x1 + rnd.gauss(0, 5 * w)
            py = (1 - t) ** 2 * y0 + 2 * t * (1 - t) * my + t * t * y1 + rnd.gauss(0, 5 * w)
            dt += f'<circle cx="{px:.0f}" cy="{py:.0f}" r="{rnd.uniform(.8, 2.2) * w:.1f}"/>'
    o = f'<g opacity="{op}">'
    o += f'<g fill="none" stroke="{glow}" opacity=".45" filter="url(#b6)" stroke-linecap="round">{lo}</g>'
    o += f'<g fill="none" stroke="{core}" opacity=".8" stroke-linecap="round">{hi}</g>'
    o += f'<g fill="{core}" opacity=".75">{dt}</g>'
    for x, y in nodes:
        r0 = rnd.uniform(5, 11) * w
        o += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r0 * 2.6:.0f}" fill="{glow}" opacity=".5" filter="url(#b6)"/><circle cx="{x:.0f}" cy="{y:.0f}" r="{r0 * .55:.1f}" fill="{knot}"/>'
    return o + '</g>'


def scatter(n, rnd, x0, y0, x1, y1, inside, gap=70):
    pts = []
    for _ in range(n * 60):
        if len(pts) >= n:
            break
        x, y = rnd.uniform(x0, x1), rnd.uniform(y0, y1)
        if inside(x, y) and all(math.hypot(x - u, y - v) > gap for u, v in pts):
            pts.append((x, y))
    return pts


def in_poly(x, y, P_):
    c = False
    for i in range(len(P_)):
        (x0, y0), (x1, y1) = P_[i], P_[i - 1]
        if (y0 > y) != (y1 > y) and x < (x1 - x0) * (y - y0) / (y1 - y0) + x0:
            c = not c
    return c

def big_galaxy(GX, GY, Rr, ROT, TILT, rnd, cols=('#fff2c8', '#ffd6f0', '#c8d8ff', '#9fe8ff'), n=420, glow='#8a5cff'):
    """Detailed spiral galaxy (like long-form B): dense small stars, arm glow lanes, pink knots, bright core."""
    k_ = Rr / 366
    g = f'<g transform="translate({GX} {GY}) rotate({ROT}) scale({k_:.3f} {k_ * TILT:.3f})">'
    g += f'<circle r="420" fill="{glow}" opacity=".2" filter="url(#b50)"/><circle r="240" fill="#ff8fd0" opacity=".18" filter="url(#b24)"/>'
    for a in range(2):
        pts = [((36 + 330 * t) * math.cos(a * math.pi + t * 4.6), (36 + 330 * t) * math.sin(a * math.pi + t * 4.6)) for t in [i / 40 for i in range(41)]]
        g += f'<path d="{path(pts)}" fill="none" stroke="#ffb8e8" stroke-width="50" opacity=".18" filter="url(#b12)"/>'
        g += f'<path d="{path(pts)}" fill="none" stroke="#e0d0ff" stroke-width="16" opacity=".25" filter="url(#b6)"/>'
        for k in range(n):
            t = k / n; ang = a * math.pi + t * 4.6; rr = 36 + 330 * t
            x = rr * math.cos(ang) + rnd.gauss(0, 10 + 22 * t); y = rr * math.sin(ang) + rnd.gauss(0, 10 + 22 * t)
            g += f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{rnd.uniform(1.4, 3.8) * (1.1 - t * .5):.1f}" fill="{rnd.choice(cols)}" opacity="{rnd.uniform(.45, 1):.2f}"/>'
    for _ in range(50):
        t = rnd.random(); a = rnd.randint(0, 1); ang = a * math.pi + t * 4.6; rr = 36 + 330 * t
        g += f'<circle cx="{rr * math.cos(ang):.1f}" cy="{rr * math.sin(ang):.1f}" r="{rnd.uniform(3, 6):.1f}" fill="#ff7ac8" opacity=".65"/>'
    g += '<circle r="110" fill="#fff6d8" opacity=".55" filter="url(#b24)"/><ellipse rx="70" ry="60" fill="#fffaf0" filter="url(#b6)"/><ellipse rx="44" ry="38" fill="#fff"/></g>'
    return g


# ---- portrait (1080x1920) output, guideline 16-9 (owner correction 2026-11-06): each landscape scene is re-framed ----
V = True          # True: shorts are vertical 1080x1920, text centred mid-frame
CUR = {}
# per scene: scale, tx, ty (landscape -> portrait), text top, text lines (sized for 1080 width), extra portrait-space art
VCFG = {
    1: dict(s=1.25, tx=-1025, ty=613, top=480, lines=[('ALL THIS', 150, 'w'), ('IS UNDER', 140, 'w'), ('5%', 250, 'y')]),
    2: dict(s=1.0, tx=-500, ty=760, top=510, lines=[('WHO LEFT', 150, 'w'), ('THESE?', 200, 'y')]),
    3: dict(s=1.15, tx=-897, ty=693, top=560, lines=[('NOT BLACK.', 125, 'w'), ('INVISIBLE', 160, 'y')]),
    4: dict(s=1.0, tx=-330, ty=900, top=640, lines=[("IT'S", 150, 'w'), ('SPEEDING', 165, 'y'), ('UP!', 190, 'w')]),
    5: dict(s=1.0, tx=-700, ty=650, top=560, lines=[('WE CAN READ', 120, 'w'), ('5 PAGES', 220, 'y')]),
}


def out(bg, d, b, lines, outline, top):
    if not V:
        return page(bg, svg(d, b), lines, outline=outline, top=top)
    import re
    c = VCFG[CUR['n']]
    b = re.sub(r'<rect width="1920" height="1080" fill="url\(#vig\d\)"/>', '', b)
    b = b.replace('<rect width="1920" height="1080"', '<rect x="-3000" y="-3000" width="8000" height="8000"')
    rnd = random.Random(900 + CUR['n'])
    top_stars = ''.join(f'<circle cx="{rnd.uniform(0, 1080):.0f}" cy="{rnd.uniform(0, c["ty"]):.0f}" r="{rnd.choice([1.2, 1.8, 2.5])}" fill="#eef0ff" opacity="{rnd.uniform(.2, .8):.2f}"/>' for _ in range(int(c['ty'] / 5)))
    top_stars += spark(rnd.randint(80, 300), rnd.randint(120, 300), 22) + spark(rnd.randint(780, 1000), rnd.randint(150, 380), 18, '#e8f0ff')
    d += rad('vigV', 540, 1100, 1250, [(0, '#000', 0), (.6, '#000', 0), (1, '#000', .6)])
    body = (f'<rect width="1080" height="1920" fill="{bg}"/><g transform="translate({c["tx"]} {c["ty"]}) scale({c["s"]})">{b}</g>'
            + CUR.get('extra', '') + top_stars + '<rect width="1080" height="1920" fill="url(#vigV)"/>')
    return vpage(bg, vsvg(d, body), c['lines'], outline=outline, top=c['top'])


ROOT = os.path.abspath(os.path.join(HERE, '..', '..'))   # videos/
GHOST = '#b9a6ff'


def ghost(dd, w=3, op=.55, dash='14 10'):
    return (f'<path d="{dd}" fill="none" stroke="{GHOST}" stroke-width="{w * 5}" opacity="{op * .25:.2f}" filter="url(#b6)"/>'
            f'<path d="{dd}" fill="none" stroke="#d8ccff" stroke-width="{w}" stroke-dasharray="{dash}" stroke-linejoin="round" opacity="{op}"/>')


def R(x, y, w, h):
    return f'M{x} {y} h{w} v{h} h{-w}Z'


def glasses():
    return ('<g fill="#dff4ff" fill-opacity=".18" stroke="#5a3a1c" stroke-width="3.4"><circle cx="-10" cy="-66" r="17"/><circle cx="22" cy="-66" r="17"/></g>'
            '<path d="M7 -68 q-1 -5 -4 0" fill="none" stroke="#5a3a1c" stroke-width="3"/>'
            '<path d="M-22 -76 q4 -4 9 -4 M10 -76 q4 -4 9 -4" fill="none" stroke="#fff" stroke-width="2.4" opacity=".8"/>')


# =============================== 1: only the lit desk is real ===============================
def make_1():
    rnd = random.Random(101)
    d = FILTERS
    d += rad('bg1', 1260, 560, 1300, [(0, '#2a1846', 1), (.5, '#140b2a', 1), (1, '#05030d', 1)])
    d += rad('lamp1', 1380, 580, 560, [(0, '#ffe8b8', .95), (.3, '#ffb466', .42), (1, '#ff9040', .05)])
    d += rad('m1', 1270, 640, 470, [(0, '#fff', 1), (.68, '#fff', 1), (1, '#fff', 0)])
    d += '<mask id="real1"><rect width="1920" height="1080" fill="url(#m1)"/></mask>'
    d += lin('wood1', [(0, '#b07a48'), (1, '#7a4e2c')])
    d += lin('woodF1', [(0, '#6a4226'), (1, '#3e2614')])
    d += lin('wall1', [(0, '#3a2a40'), (1, '#4e3a46')])
    d += lin('scr1', [(0, '#7fd0ff'), (1, '#2a5aa8')])
    d += rad('vig1', 1200, 560, 1250, [(0, '#000', 0), (.6, '#000', 0), (1, '#000', .72)])
    b = '<rect width="1920" height="1080" fill="url(#bg1)"/>'
    for _ in range(200):
        b += f'<circle cx="{rnd.uniform(0, 1920):.0f}" cy="{rnd.uniform(0, 1080):.0f}" r="{rnd.choice([1.1, 1.6, 2.2])}" fill="#efe6ff" opacity="{rnd.uniform(.15, .65):.2f}"/>'
    # ---- room geometry (one-point perspective) ----
    VX, VY = 1260, 400
    room = []      # (d, fill) drawn as ghost everywhere and solid inside the lamp light
    room.append((R(700, 110, 1120, 450), 'url(#wall1)'))                     # back wall
    floor = poly([(700, 560), (1820, 560), (2300, 1080), (-300, 1080)])
    room.append((floor, '#3a2420'))
    for x0 in range(810, 1820, 110):
        room.append((f'M{x0} 560 L{VX + (x0 - VX) * 4.25:.0f} 1080', None))   # floorboards
    room.append((f'M700 110 L{700 - 540 * 2:.0f} {110 - 290 * 2:.0f} M700 560 L0 773 M1820 110 L1920 58 M1820 560 L1920 588', None))
    room.append((R(990, 160, 250, 260), '#0b1030'))                          # window
    room.append(('M1115 160 V420 M990 290 H1240', None))
    room.append((R(1470, 150, 230, 410), '#4a2e22'))                         # bookshelf
    for k in range(1, 5):
        room.append((f'M1470 {150 + k * 82} H1700', None))
    for k in range(4):
        x = 1480
        while x < 1680:
            w = rnd.choice([16, 20, 24]); h = rnd.choice([56, 62, 68])
            room.append((R(x, 150 + (k + 1) * 82 - h, w, h), rnd.choice(['#8a3a3a', '#3a5a8a', '#c9a24a', '#4a7a4a'])))
            x += w + 4
    room.append((R(1290, 190, 130, 100), '#2a2030'))                         # picture frame
    room.append(('M1300 280 L1340 230 L1365 255 L1385 225 L1410 280', None))
    rug = '<ellipse cx="1260" cy="930" rx="560" ry="90"/>'
    room.append(('M700 930 a560 90 0 1 0 1120 0 a560 90 0 1 0 -1120 0', '#5a2a3a'))
    # chair (left, front)
    room.append((poly([(720, 760), (860, 760), (850, 600), (730, 600)]), '#5a3a26'))
    room.append((poly([(700, 760), (880, 760), (890, 790), (690, 790)]), '#6a4430'))
    room.append(('M700 790 L705 1000 M880 790 L875 1000 M740 790 L745 940 M845 790 L840 940', None))
    # desk
    top = poly([(900, 700), (1620, 700), (1560, 630), (960, 630)])
    room.append((top, 'url(#wood1)'))
    room.append((poly([(900, 700), (1620, 700), (1620, 734), (900, 734)]), 'url(#woodF1)'))
    for lx in (912, 1584):
        room.append((R(lx, 734, 28, 236), 'url(#woodF1)'))
    for lx in (975, 1525):
        room.append((R(lx, 734, 20, 130), '#3e2614'))
    # laptop
    room.append((poly([(1150, 682), (1350, 682), (1334, 652), (1166, 652)]), '#9aa3b6'))
    room.append((poly([(1166, 652), (1334, 652), (1346, 498), (1178, 498)]), '#2a2f3c'))
    room.append((poly([(1178, 640), (1324, 640), (1334, 510), (1188, 510)]), 'url(#scr1)'))
    # mug
    room.append(('M1388 632 h46 l-4 56 q-19 8 -38 0z', '#e8e2d6'))
    room.append(('M1432 646 q22 0 18 20 q-3 14 -20 14', None))
    # lamp
    room.append(('M1478 676 a46 12 0 1 0 92 0 a46 12 0 1 0 -92 0', '#c9a24a'))
    room.append(('M1524 668 L1548 520 L1470 448', None))
    room.append((poly([(1428, 404), (1506, 430), (1482, 500), (1392, 474)]), '#d9a640'))
    # ---- ghost pass (everything) ----
    gl = ''
    for dd, fill in room:
        gl += ghost(dd, 3, .5)
    b += f'<g>{gl}</g>'
    # ---- solid pass inside the light ----
    s = '<rect width="1920" height="1080" fill="#160d20"/>'
    for dd, fill in room:
        if fill:
            s += f'<path d="{dd}" fill="{fill}" stroke="#120a10" stroke-width="4" stroke-linejoin="round"/>'
        else:
            s += f'<path d="{dd}" fill="none" stroke="#120a10" stroke-width="4" stroke-linecap="round"/>'
    for k in range(9):    # wood grain
        y = 640 + k * 7
        s += f'<path d="M{965 - k * 6} {y} Q1260 {y + rnd.uniform(-4, 4):.0f} {1555 + k * 6} {y}" stroke="#5a3a1c" stroke-width="1.6" fill="none" opacity=".35"/>'
    for _ in range(18):   # window stars
        s += f'<circle cx="{rnd.uniform(1000, 1230):.0f}" cy="{rnd.uniform(170, 410):.0f}" r="{rnd.uniform(1, 2.4):.1f}" fill="#fff" opacity=".8"/>'
    s += mini_galaxy(1256, 575, 62, -12, '#fff2c8', n=46, rnd=random.Random(6))     # galaxy on the laptop screen
    s += '<path d="M1188 512 L1334 512 L1330 560 Q1260 520 1192 600Z" fill="#fff" opacity=".12"/>'
    for k in range(3):    # mug steam
        s += f'<path d="M{1398 + k * 14} 622 q-12 -24 0 -44 q10 -18 -2 -40" fill="none" stroke="#fff" stroke-width="5" stroke-linecap="round" opacity=".35"/>'
    s += '<rect width="1920" height="1080" fill="url(#lamp1)"/>'
    s += '<path d="M1392 474 L1482 500 L1660 700 L1120 700Z" fill="#ffe9b0" opacity=".16" filter="url(#b12)"/>'
    b += f'<g mask="url(#real1)">{s}</g>'
    b += '<ellipse cx="1440" cy="494" rx="40" ry="20" transform="rotate(18 1440 494)" fill="#fff8d8"/><circle cx="1440" cy="494" r="70" fill="#ffd890" opacity=".55" filter="url(#b24)"/>'
    b += '<ellipse cx="1360" cy="690" rx="230" ry="24" fill="#ffe2a8" opacity=".25" filter="url(#b12)"/>'
    # dissolving edge: bits drifting from the solid island into the ghost room
    for _ in range(90):
        a = rnd.uniform(0, 2 * math.pi); rr = rnd.uniform(330, 560)
        x, y = 1270 + rr * math.cos(a), 620 + rr * .8 * math.sin(a)
        if x < 940 and y < 640:
            continue
        sz = rnd.uniform(3, 9) * (1 - (rr - 330) / 400)
        b += f'<rect x="{x:.0f}" y="{y:.0f}" width="{sz:.1f}" height="{sz:.1f}" transform="rotate({rnd.uniform(0, 90):.0f} {x:.0f} {y:.0f})" fill="{rnd.choice(["#c9a07a", "#d8ccff", "#ffe2a8"])}" opacity="{rnd.uniform(.35, .8):.2f}"/>'
    b += spark(1600, 260, 22, '#e8dcff') + spark(960, 560, 16, '#e8dcff') + spark(1480, 330, 14)
    # ---- frog sitting on the desk, staring at the ghost room ----
    b += f'<ellipse cx="1050" cy="694" rx="90" ry="12" fill="#000" opacity=".35" filter="url(#b3)"/>'
    b += frog(1045, 692, 2.35, look=(-7, -5), mouth='O', armL='M-34 -22 q-22 -12 -26 -42', armR='M38 -22 q16 6 18 22',
              legs=((-20, -6, -26, 4, -8), (20, -6, 28, 4, 8)))
    b += '<rect width="1920" height="1080" fill="url(#vig1)"/>'
    lines = [('ALL THIS', 160, 'w'), ('IS UNDER', 150, 'w'), ('5%', 290, 'y')]
    return out('#05030d', d, b, lines, '#07030f', 40)


# =============================== 2: footprints in the snow, nobody there ===============================
def make_2():
    rnd = random.Random(202)
    HY = 600
    d = FILTERS
    d += lin('sky2', [(0, '#050a22'), (.55, '#13235a'), (1, '#3a4f8f')])
    d += lin('snow2', [(0, '#7f93c8'), (.35, '#a9bbe6'), (1, '#dfe8ff')])
    GXg = 1200 if V else 1420
    d += rad('gal2', GXg, 250, 520, [(0, '#c8d8ff', .55), (.4, '#8aa0ff', .16), (1, '#5a70ff', 0)])
    LX, LY = (600, 1000) if V else (420, 1000)
    FXo = 40 if V else 0
    d += rad('lant2', LX + 180, 930, 460, [(0, '#ffd68a', .75), (.4, '#ffaa55', .25), (1, '#ff9040', 0)])
    d += rad('vig2', 1100, 560, 1250, [(0, '#000', 0), (.62, '#000', 0), (1, '#000', .62)])
    b = f'<rect width="1920" height="{HY + 40}" fill="url(#sky2)"/>'
    for _ in range(230):
        b += f'<circle cx="{rnd.uniform(0, 1920):.0f}" cy="{rnd.uniform(0, HY):.0f}" r="{rnd.choice([1.1, 1.6, 2.3])}" fill="#eef4ff" opacity="{rnd.uniform(.2, .85):.2f}"/>'
    b += '<rect width="1920" height="1080" fill="url(#gal2)"/>'
    b += big_galaxy(GXg, 250, 250, -16, .42, random.Random(7), n=360)
    # fast outer stars with short trails
    for ang0 in (20, 150, 230, 320):
        a = math.radians(ang0); pts = []
        for i in range(12):
            aa = a - i * .03; x, y = 235 * math.cos(aa), 235 * .45 * math.sin(aa)
            c, s_ = math.cos(math.radians(-16)), math.sin(math.radians(-16))
            pts.append((GXg + x * c - y * s_, 250 + x * s_ + y * c))
        b += f'<path d="{path(pts)}" stroke="#fff2c8" stroke-width="5" fill="none" stroke-linecap="round" opacity=".6"/><circle cx="{pts[0][0]:.0f}" cy="{pts[0][1]:.0f}" r="5" fill="#fff"/>'
    # hills + snowy pines on the horizon
    b += f'<path d="M0 {HY - 30} Q300 {HY - 110} 640 {HY - 40} Q980 {HY - 120} 1340 {HY - 30} Q1640 {HY - 90} 1920 {HY - 40} L1920 {HY + 20} L0 {HY + 20}Z" fill="#5a6ea6" opacity=".9"/>'
    b += f'<path d="M0 {HY - 30} Q300 {HY - 110} 640 {HY - 40} Q980 {HY - 120} 1340 {HY - 30} Q1640 {HY - 90} 1920 {HY - 40}" fill="none" stroke="#cfdcff" stroke-width="4" opacity=".7"/>'
    for x in list(range(30, 900, 46)) + list(range(1560, 1920, 42)):
        h = rnd.uniform(60, 120); y = HY - 4 + rnd.uniform(-6, 6)
        b += f'<path d="M{x} {y - h:.0f} L{x + h * .32:.0f} {y:.0f} L{x - h * .32:.0f} {y:.0f}Z" fill="#1c2a52"/>'
        b += f'<path d="M{x} {y - h:.0f} L{x + h * .14:.0f} {y - h * .55:.0f} L{x - h * .14:.0f} {y - h * .55:.0f}Z" fill="#e6eeff" opacity=".85"/>'
    # snowfield
    b += f'<path d="M0 {HY} Q960 {HY - 30} 1920 {HY} L1920 {1500 if V else 1080} L0 {1500 if V else 1080}Z" fill="url(#snow2)"/>'
    for k in range(7):
        y = HY + 40 + k * k * 9
        b += f'<path d="M0 {y} Q600 {y - 20} 1200 {y + 6} T1920 {y - 4}" stroke="#ffffff" stroke-width="{2 + k * .6:.1f}" fill="none" opacity=".25"/>'
    for _ in range(140):
        y = rnd.uniform(HY + 10, 1075); x = rnd.uniform(0, 1920)
        b += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{rnd.uniform(.8, 2.2) * (y - HY + 80) / 300:.1f}" fill="#fff" opacity="{rnd.uniform(.4, .95):.2f}"/>'
    b += '<rect width="1920" height="1080" fill="url(#lant2)"/>'
    # ---- the footprints: from the far hills to the frog ----
    P0, P1, P2 = ((1450, HY + 40), (1480, 880), (1150, 990)) if V else ((1560, HY + 40), (1560, 880), (1110, 990))
    def bez(t):
        return ((1 - t) ** 2 * P0[0] + 2 * t * (1 - t) * P1[0] + t * t * P2[0], (1 - t) ** 2 * P0[1] + 2 * t * (1 - t) * P1[1] + t * t * P2[1])
    steps = []; acc = 0; px, py = bez(0); t = 0; nxt = 0
    while t <= 1:
        x, y = bez(t); acc += math.hypot((x - px), (y - py) / .55); px, py = x, y
        sc = .3 + 1.3 * ((y - HY) / (990 - HY)) ** 1.1
        if acc >= nxt:
            steps.append(t); nxt = acc + 92 * sc
        t += .002
    for i, t in enumerate(steps):
        x, y = bez(t); x2, y2 = bez(min(1, t + .01)); x0, y0 = bez(max(0, t - .01))
        ang = math.degrees(math.atan2((y2 - y0) / .55, x2 - x0)) + 90
        sc = .3 + 1.3 * ((y - HY) / (990 - HY)) ** 1.1
        side = 1 if i % 2 else -1
        nx, ny = -(y2 - y0) / .55, (x2 - x0); L = math.hypot(nx, ny) or 1
        x += side * 26 * sc * nx / L; y += side * 26 * sc * ny / L * .55
        fp = (f'<g transform="translate({x:.0f} {y:.0f}) scale({sc:.2f} {sc * .55:.2f}) rotate({ang:.0f})">'
              '<ellipse cx="0" cy="-30" rx="34" ry="46" fill="#b48cff" opacity=".45" filter="url(#b12)"/>'
              '<path d="M-26 -44 Q-28 -92 2 -96 Q30 -94 28 -46 Q26 -14 0 -12 Q-24 -14 -26 -44Z" fill="#4e62a0"/>'
              '<path d="M-22 18 Q-22 -2 0 -2 Q22 -2 22 18 Q22 40 0 40 Q-22 40 -22 18Z" fill="#4e62a0"/>'
              '<path d="M-26 -44 Q-28 -92 2 -96 Q30 -94 28 -46" fill="none" stroke="#2a3870" stroke-width="10"/>'
              '<path d="M-22 18 Q-22 -2 0 -2 Q22 -2 22 18" fill="none" stroke="#2a3870" stroke-width="10"/>'
              '<path d="M-24 -40 Q-22 -16 0 -12 Q24 -16 26 -42 M-20 24 Q-14 40 0 41 Q16 40 20 24" fill="none" stroke="#ffffff" stroke-width="7" opacity=".9"/>'
              + ''.join(f'<path d="M-16 {yy} h32" stroke="#6a7cc0" stroke-width="5" opacity=".7"/>' for yy in (-74, -58, -42, -26, 10, 26)) +
              '</g>')
        b += fp
    # fresh snow puff where the next invisible step just landed
    for _ in range(22):
        a = rnd.uniform(math.pi * 1.05, math.pi * 1.95); r0 = rnd.uniform(30, 120)
        b += f'<circle cx="{1010 + FXo + r0 * math.cos(a):.0f}" cy="{1000 + r0 * .5 * math.sin(a):.0f}" r="{rnd.uniform(3, 8):.1f}" fill="#fff" opacity="{rnd.uniform(.5, .95):.2f}"/>'
    b += f'<ellipse cx="{1010 + FXo}" cy="1020" rx="120" ry="30" fill="#ffffff" opacity=".35" filter="url(#b6)"/>'
    # ---- lantern on the snow ----
    b += f'<circle cx="{LX}" cy="{LY - 60}" r="110" fill="#ffcf7a" opacity=".45" filter="url(#b24)"/>'
    b += (f'<g transform="translate({LX} {LY})" stroke="#2a1a0c" stroke-width="4" stroke-linejoin="round">'
          '<path d="M-22 -118 Q0 -150 22 -118" fill="none"/><rect x="-34" y="-116" width="68" height="14" rx="4" fill="#3a2a1a"/>'
          '<rect x="-28" y="-102" width="56" height="86" rx="8" fill="#ffe7a8"/><ellipse cx="0" cy="-58" rx="14" ry="24" fill="#fffbe8" stroke="none"/>'
          '<path d="M-28 -60 H28 M0 -102 V-16" stroke-width="3" opacity=".6"/><rect x="-36" y="-18" width="72" height="18" rx="5" fill="#3a2a1a"/></g>')
    # ---- frog detective, crouched, magnifier on the last print ----
    hat = ('<g transform="translate(6 -84) rotate(-6) scale(.78)" stroke-width="3.6">'
           '<path d="M-42 6 Q-40 -38 0 -40 Q40 -38 42 6Z" fill="#9a6a3c"/>'
           '<path d="M-28 -32 L-24 4 M-12 -39 L-10 4 M6 -40 L6 4 M22 -37 L20 4 M34 -28 L30 4 M-40 -14 H40" stroke="#5a3a1c" stroke-width="2" opacity=".7"/>'
           '<path d="M38 2 Q62 0 70 10 Q50 14 34 10Z" fill="#7a5028"/><path d="M-38 2 Q-62 0 -70 10 Q-50 14 -34 10Z" fill="#7a5028"/>'
           '<path d="M-2 -40 q4 -10 10 -6" fill="none"/></g>')
    cape = '<path d="M-36 -30 Q-56 10 -40 6 L44 6 Q56 10 40 -30 Q2 -14 -36 -30Z" fill="#a8763e" stroke-width="3"/>'
    mag = ('<g transform="translate(86 -4) rotate(30)"><rect x="-6" y="-46" width="12" height="40" rx="5" fill="#6a3e1c" stroke-width="3"/>'
           '<circle cx="0" cy="-74" r="30" fill="#dff4ff" fill-opacity=".35" stroke="#c9a24a" stroke-width="7"/>'
           '<circle cx="0" cy="-74" r="30" fill="none" stroke-width="2.4"/><path d="M-16 -86 q8 -10 20 -10" fill="none" stroke="#fff" stroke-width="4"/></g>')
    b += f'<ellipse cx="{760 + FXo}" cy="1010" rx="150" ry="22" fill="#2a3870" opacity=".35" filter="url(#b6)"/>'
    b += frog(760 + FXo, 1004, 2.75, rot=6, look=(9, 4), mouth='O', back=cape, hat=hat,
              armR='M38 -22 q26 4 46 22', armL='M-34 -22 q-20 6 -22 24', front=mag,
              legs=((-20, -6, -34, 4, -10), (20, -6, 32, 4, 10)))
    b += spark(1190, 120, 24) + spark(1700, 470, 18) + spark(1000, 380, 14, '#e8f0ff')
    b += '<rect width="1920" height="1080" fill="url(#vig2)"/>'
    lines = [('WHO LEFT', 175, 'w'), ('THESE?', 230, 'y')]
    return out('#050a22', d, b, lines, '#050a1c', 46)


# =============================== 3: sailing an invisible ocean ===============================
def make_3():
    rnd = random.Random(303)
    HY = 560          # far edge of the invisible sea
    WL = 820          # boat waterline
    d = FILTERS
    d += rad('bg3', 1400, 480, 1300, [(0, '#163a5c', 1), (.45, '#0b1a36', 1), (1, '#030814', 1)])
    d += rad('lant3', 1235, 560, 420, [(0, '#ffd68a', .6), (.4, '#ffaa55', .2), (1, '#ff9040', 0)])
    d += lin('hull3', [(0, '#9a5a2c'), (1, '#4e2a12')])
    d += lin('sail3', [(0, '#fffaf0'), (1, '#e8dcc0')], x2=1, y2=1)
    d += lin('sub3', [(0, '#5fe0ff'), (1, '#1a4a7a')])
    d += rad('vig3', 1150, 540, 1250, [(0, '#000', 0), (.6, '#000', 0), (1, '#000', .7)])
    b = '<rect width="1920" height="1080" fill="url(#bg3)"/>'
    for _ in range(300):
        b += f'<circle cx="{rnd.uniform(0, 1920):.0f}" cy="{rnd.uniform(0, 1080):.0f}" r="{rnd.choice([1.1, 1.6, 2.3])}" fill="#e8f6ff" opacity="{rnd.uniform(.15, .8):.2f}"/>'
    for _ in range(10):
        b += f'<ellipse cx="{rnd.uniform(900, 1900):.0f}" cy="{rnd.uniform(40, 1000):.0f}" rx="{rnd.uniform(80, 180):.0f}" ry="{rnd.uniform(30, 80):.0f}" fill="{rnd.choice(["#5fe0ff", "#6b8cff", "#b46bff"])}" opacity="{rnd.uniform(.05, .1):.2f}" filter="url(#b24)"/>'
    # the galaxy floating half-sunk in the invisible sea (back right)
    GX, GY = 1560, 400
    b += f'<circle cx="{GX}" cy="{GY}" r="260" fill="#ffd8f0" opacity=".18" filter="url(#b50)"/>'
    b += big_galaxy(GX, GY, 300, -8, .4, random.Random(31), n=420)
    # the part below the surface is tinted and wavy (seen through the water)
    b += f'<path d="M1180 {HY - 140} Q1560 {HY - 110} 1920 {HY - 150} L1920 1080 L1180 1080Z" fill="#2ac0ff" opacity=".0"/>'
    # ripple rings around the galaxy where it touches the surface
    for k in range(6):
        rx, ry = 300 + k * 70, 34 + k * 9
        b += f'<ellipse cx="{GX}" cy="{GY + 40}" rx="{rx}" ry="{ry}" fill="none" stroke="#9ff0ff" stroke-width="{4 - k * .5:.1f}" opacity="{.6 - k * .08:.2f}" stroke-dasharray="{60 + k * 20} {18 + k * 6}"/>'
    b += f'<ellipse cx="{GX}" cy="{GY + 40}" rx="300" ry="34" fill="none" stroke="#9ff0ff" stroke-width="16" opacity=".25" filter="url(#b6)"/>'
    # faint surface glints far away (the only hint of the water plane)
    for _ in range(40):
        x = rnd.uniform(950, 1900); y = rnd.uniform(HY - 60, WL + 200)
        w = rnd.uniform(20, 60) * (y - HY + 200) / 400
        b += f'<path d="M{x:.0f} {y:.0f} q{w / 2:.0f} -5 {w:.0f} 0" stroke="#bff8ff" stroke-width="2" fill="none" opacity="{rnd.uniform(.15, .4):.2f}"/>'
    # ---- the wake: the only proof of the water ----
    BOW, STERN = (1520, WL), (940, WL)
    for k in range(9):
        t = k / 8
        for sgn in (-1, 1):
            x0 = STERN[0] - 40 - t * 820; y0 = WL + sgn * (10 + t * 150) * .6 + t * 40
            b += f'<path d="M{x0 + 50:.0f} {y0 - sgn * 10:.0f} q-30 {sgn * 14:.0f} -70 {sgn * 18:.0f}" stroke="#bff8ff" stroke-width="{6 - t * 3:.1f}" fill="none" stroke-linecap="round" opacity="{.9 - t * .55:.2f}"/>'
    wake = f'M{STERN[0]} {WL - 6} Q{STERN[0] - 400} {WL - 40} 80 {WL - 30} M{STERN[0]} {WL + 14} Q{STERN[0] - 400} {WL + 120} 80 {WL + 230}'
    b += f'<path d="{wake}" stroke="#5fe0ff" stroke-width="30" fill="none" opacity=".25" filter="url(#b12)"/>'
    b += f'<path d="{wake}" stroke="#dffaff" stroke-width="5" fill="none" stroke-dasharray="40 16" opacity=".85"/>'
    b += f'<path d="M{STERN[0]} {WL + 4} Q{STERN[0] - 380} {WL + 40} 120 {WL + 90}" stroke="#9ff0ff" stroke-width="40" fill="none" opacity=".12" filter="url(#b12)"/>'
    # ---- boat ----
    hull_above = f'M{STERN[0] - 30} {WL - 70} L{BOW[0] + 40} {WL - 90} Q{BOW[0] + 10} {WL - 20} {BOW[0] - 30} {WL} L{STERN[0] + 10} {WL} Q{STERN[0] - 20} {WL - 30} {STERN[0] - 30} {WL - 70}Z'
    hull_below = f'M{STERN[0] + 10} {WL} L{BOW[0] - 30} {WL} Q{BOW[0] - 120} {WL + 90} {1200} {WL + 100} Q{STERN[0] + 60} {WL + 90} {STERN[0] + 10} {WL}Z'
    b += f'<path d="{hull_below}" fill="url(#sub3)" opacity=".55" stroke="#9ff0ff" stroke-width="3" stroke-dasharray="10 8"/>'
    b += f'<path d="M1180 {WL + 100} L1180 {WL + 150} L1240 {WL + 100}Z" fill="#5fe0ff" opacity=".4"/>'
    # mast + sails
    MX = 1210
    b += f'<path d="M{MX} {WL - 80} L{MX} 250" stroke="#3a1e0c" stroke-width="16"/><path d="M{MX - 3} {WL - 80} L{MX - 3} 250" stroke="#8a5a2c" stroke-width="6"/>'
    b += f'<path d="M{MX + 10} 270 Q{MX + 260} 470 {MX + 250} {WL - 110} L{MX + 10} {WL - 105}Z" fill="url(#sail3)" stroke="#2a1a0c" stroke-width="5" stroke-linejoin="round"/>'
    b += f'<path d="M{MX - 10} 300 Q{MX - 170} 500 {MX - 200} {WL - 112} L{MX - 10} {WL - 108}Z" fill="url(#sail3)" stroke="#2a1a0c" stroke-width="5" stroke-linejoin="round"/>'
    for k in range(1, 4):
        y = 270 + k * (WL - 380) / 4
        b += f'<path d="M{MX + 10} {y:.0f} Q{MX + 130} {y + 20:.0f} {MX + 30 + k * 60} {y + 4:.0f}" stroke="#c9b48a" stroke-width="2.4" fill="none"/>'
    b += f'<path d="M{MX} 250 L{MX + 30} 258 L{MX + 60} 246 L{MX + 30} 270Z" fill="#d94a4a" stroke="#2a1a0c" stroke-width="3"/>'
    # hull above the water
    b += f'<path d="{hull_above}" fill="url(#hull3)" stroke="#1a0c04" stroke-width="5" stroke-linejoin="round"/>'
    for k in range(1, 4):
        b += f'<path d="M{STERN[0] - 24 + k * 6} {WL - 70 + k * 17} L{BOW[0] + 20 - k * 16} {WL - 88 + k * 22}" stroke="#3a1e0c" stroke-width="2.4" opacity=".7"/>'
    b += f'<path d="M{STERN[0] - 30} {WL - 70} L{BOW[0] + 40} {WL - 90}" stroke="#e6c08a" stroke-width="6"/>'
    for k in range(5):
        b += f'<circle cx="{1040 + k * 95}" cy="{WL - 52 - k * 4}" r="11" fill="#2a1a0c" stroke="#e6c08a" stroke-width="3"/><circle cx="{1040 + k * 95}" cy="{WL - 52 - k * 4}" r="6" fill="#ffd68a" opacity=".85"/>'
    # bow spray
    for _ in range(26):
        a = rnd.uniform(-2.6, -.4); r0 = rnd.uniform(20, 90)
        b += f'<circle cx="{BOW[0] - 20 + r0 * math.cos(a) + 30:.0f}" cy="{WL + r0 * .6 * math.sin(a):.0f}" r="{rnd.uniform(2.5, 6):.1f}" fill="#dffaff" opacity="{rnd.uniform(.5, .95):.2f}"/>'
    b += f'<path d="M{BOW[0] - 40} {WL + 2} Q{BOW[0] + 40} {WL - 10} {BOW[0] + 120} {WL + 30}" stroke="#dffaff" stroke-width="6" fill="none" opacity=".8"/>'
    # lantern on the mast (light source)
    b += '<rect width="1920" height="1080" fill="url(#lant3)"/>'
    b += f'<path d="M{MX} 520 L{MX + 40} 528" stroke="#2a1a0c" stroke-width="5"/><circle cx="{MX + 44}" cy="560" r="80" fill="#ffd890" opacity=".5" filter="url(#b24)"/>'
    b += f'<g transform="translate({MX + 44} 528)" stroke="#2a1a0c" stroke-width="3.4"><rect x="-16" y="0" width="32" height="10" rx="3" fill="#3a2a1a"/><rect x="-13" y="10" width="26" height="40" rx="5" fill="#ffe7a8"/><ellipse cx="0" cy="30" rx="7" ry="12" fill="#fffbe8" stroke="none"/><rect x="-16" y="48" width="32" height="8" rx="3" fill="#3a2a1a"/></g>'
    # ---- frog sailor at the stern, holding the tiller, leaning to look over the side ----
    hat = ('<g transform="translate(4 -88) rotate(-10)" stroke-width="3.2"><path d="M-30 4 Q-30 -26 2 -28 Q34 -26 34 4Z" fill="#fbfbf6"/>'
           '<rect x="-34" y="-2" width="72" height="12" rx="5" fill="#2a4a8a"/><path d="M-30 4 Q2 12 34 4" fill="none"/></g>')
    collar = '<path d="M-30 -24 L-6 -6 L6 -24 L18 -6 L40 -24 Q4 -14 -30 -24Z" fill="#2a4a8a" stroke-width="2.6"/>'
    tiller = f'<path d="M-50 -10 L-110 18" stroke="#6a3e1c" stroke-width="9"/>'
    b += frog(990, WL - 80, 2.05, rot=-6, look=(-6, 7), mouth='O', hat=hat, mid=collar,
              armL='M-34 -22 q-24 4 -42 18', armR='M38 -22 q22 -6 34 -30',
              legs=((-20, -6, -24, 4, 0), (20, -6, 26, 4, 0)))
    b += spark(1780, 200, 24) + spark(1350, 140, 18, '#e8fbff') + spark(1700, 700, 16, '#e8fbff')
    b += '<rect width="1920" height="1080" fill="url(#vig3)"/>'
    lines = [('NOT BLACK.', 150, 'w'), ('INVISIBLE', 175, 'y')]
    return out('#030814', d, b, lines, '#030814', 48)


# =============================== 4: the ball that speeds up ===============================
def make_4():
    rnd = random.Random(404)
    CX, CY = (870, 60) if V else (1250, 470)
    d = FILTERS
    d += rad('bg4', CX, CY, 1300, [(0, '#3a1c5c', 1), (.45, '#160c33', 1), (1, '#05030f', 1)])
    d += rad('ball4', 0, 0, 1, [(0, '#fff', 1), (1, '#fff', 1)])
    d += lin('hill4', [(0, '#3f7a3a'), (1, '#142a14')])
    d += rad('vig4', 1100, 540, 1250, [(0, '#000', 0), (.62, '#000', 0), (1, '#000', .68)])
    d += '<radialGradient id="bb4" cx=".38" cy=".35" r=".7"><stop offset="0" stop-color="#ffffff"/><stop offset=".5" stop-color="#fff0c0"/><stop offset="1" stop-color="#e8a040"/></radialGradient>'
    b = '<rect width="1920" height="1080" fill="url(#bg4)"/>'
    for _ in range(200):
        b += f'<circle cx="{rnd.uniform(0, 1920):.0f}" cy="{rnd.uniform(0, 1080):.0f}" r="{rnd.choice([1.1, 1.6, 2.2])}" fill="#efe6ff" opacity="{rnd.uniform(.15, .65):.2f}"/>'
    # galaxies racing apart: farther ones move faster (longer trails)
    for _ in range(80 if V else 46):
        a = rnd.uniform(0, 2 * math.pi); dist = rnd.uniform(140, 1000)
        x, y = CX + dist * (.75 if V else 1) * math.cos(a), CY + dist * (1 if V else .75) * math.sin(a)
        if (V and (not (330 < x < 1410 and -900 < y < 1000) or math.hypot(x - 560, y - 700) < 230)) or (not V and ((x < 980 and y < 640) or not (0 < x < 1920 and 0 < y < 1080) or (x > 1600 and y > 880))):
            continue
        L = dist * .22; ux, uy = ((.75 * math.cos(a), math.sin(a)) if V else (math.cos(a), .75 * math.sin(a)))
        r0 = rnd.uniform(14, 30)
        col = rnd.choice(['#ffd6f0', '#c8d8ff', '#fff2c8', '#b8ffef'])
        b += f'<path d="M{x:.0f} {y:.0f} L{x - ux * L:.0f} {y - uy * L:.0f}" stroke="{col}" stroke-width="{r0 * .9:.1f}" stroke-linecap="round" opacity=".18" filter="url(#b3)"/>'
        b += f'<path d="M{x:.0f} {y:.0f} L{x - ux * L * .6:.0f} {y - uy * L * .6:.0f}" stroke="{col}" stroke-width="2.4" stroke-linecap="round" opacity=".5"/>'
        b += mini_galaxy(x, y, r0, rnd.uniform(0, 180), col, n=18, rnd=rnd, op=.9)
    for k in range(5):
        r0 = 150 + k * 170
        b += f'<ellipse cx="{CX}" cy="{CY}" rx="{r0 * (.75 if V else 1):.0f}" ry="{r0 * (1 if V else .75):.0f}" fill="none" stroke="#b9a6ff" stroke-width="2" stroke-dasharray="6 18" opacity="{.28 - k * .04:.2f}"/>'
    # ---- the little planet hill ----
    b += '<path d="M-40 840 Q520 700 1230 1100 L-40 1100Z" fill="url(#hill4)" stroke="#9fe08a" stroke-width="5"/>'
    b += '<path d="M-40 840 Q520 700 1230 1100" fill="none" stroke="#c8ffb0" stroke-width="16" opacity=".25" filter="url(#b6)"/>'
    for _ in range(70):
        t = rnd.random(); x = (1 - t) ** 2 * -40 + 2 * t * (1 - t) * 520 + t * t * 1230; y = (1 - t) ** 2 * 840 + 2 * t * (1 - t) * 700 + t * t * 1100
        b += f'<path d="M{x:.0f} {y + 4:.0f} l{rnd.uniform(-6, 6):.0f} {-rnd.uniform(10, 22):.0f}" stroke="#6ab85a" stroke-width="3" stroke-linecap="round"/>'
    for fx_, fy_ in ((150, 812), (330, 786), (1000, 975)):
        b += f'<circle cx="{fx_}" cy="{fy_}" r="7" fill="#ffd6f0" stroke="#1d2b1c" stroke-width="2"/><circle cx="{fx_}" cy="{fy_}" r="2.5" fill="#f2d27a"/>'
    # ---- ball path: spacing grows = speeding up ----
    P0, P1, P2 = ((760, 610), (1060, 320), (1130, -560)) if V else ((760, 610), (1010, 480), (1500, 215))
    def bez(t):
        return ((1 - t) ** 2 * P0[0] + 2 * t * (1 - t) * P1[0] + t * t * P2[0], (1 - t) ** 2 * P0[1] + 2 * t * (1 - t) * P1[1] + t * t * P2[1])
    trail = [bez(i / 60) for i in range(61)]
    b += f'<path d="{path(trail)}" stroke="#ffd890" stroke-width="40" fill="none" stroke-linecap="round" opacity=".18" filter="url(#b12)"/>'
    b += f'<path d="{path(trail)}" stroke="#fff2c8" stroke-width="5" fill="none" stroke-dasharray="4 14" stroke-linecap="round" opacity=".7"/>'
    ts = [.0, .08, .19, .34, .54, .78]
    for k, t in enumerate(ts):
        x, y = bez(t); r0 = 26 + k * 4
        b += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r0}" fill="#fff0c0" opacity="{.16 + k * .07:.2f}" stroke="#fff6d8" stroke-width="3" stroke-opacity="{.25 + k * .08:.2f}"/>'
    BX, BY = bez(1.0)
    # speed lines + fire trail behind the final ball
    qx, qy = bez(.96); ux, uy = BX - qx, BY - qy; L = math.hypot(ux, uy); ux, uy = ux / L, uy / L; nx, ny = -uy, ux
    for k in range(7):
        off = (k - 3) * 16
        x0, y0 = BX - ux * 300 + nx * off, BY - uy * 300 + ny * off
        x1, y1 = BX - ux * 82 + nx * off * .6, BY - uy * 82 + ny * off * .6
        b += f'<path d="M{x0:.0f} {y0:.0f} L{x1:.0f} {y1:.0f}" stroke="#fff6d8" stroke-width="{6 - abs(k - 3):.0f}" stroke-linecap="round" opacity=".8"/>'
    b += f'<path d="M{BX - ux * 390:.0f} {BY - uy * 390:.0f} L{BX} {BY}" stroke="#ff9a4a" stroke-width="80" fill="none" opacity=".35" filter="url(#b24)" stroke-linecap="round"/>'
    b += f'<circle cx="{BX}" cy="{BY}" r="190" fill="#ffd890" opacity=".45" filter="url(#b50)"/>'
    b += f'<circle cx="{BX}" cy="{BY}" r="70" fill="url(#bb4)" stroke="#7a4214" stroke-width="5"/>'
    b += f'<path d="M{BX - 52} {BY - 40} Q{BX - 10} {BY} {BX - 40} {BY + 52}" stroke="#d94a4a" stroke-width="5" fill="none" stroke-dasharray="7 6"/>'
    b += f'<path d="M{BX + 50} {BY - 44} Q{BX + 14} {BY} {BX + 44} {BY + 50}" stroke="#d94a4a" stroke-width="5" fill="none" stroke-dasharray="7 6"/>'
    b += f'<path d="M{BX - 40} {BY - 30} q14 -20 40 -24" stroke="#fff" stroke-width="7" fill="none" stroke-linecap="round" opacity=".9"/>'
    # up-arrows ahead of it
    for k in range(3):
        ax, ay = BX + ux * (100 + k * 50), BY + uy * (100 + k * 50); rr = math.degrees(math.atan2(uy, ux)) + 90
        b += f'<path d="M{ax - 20:.0f} {ay + 14:.0f} L{ax:.0f} {ay - 4:.0f} L{ax + 20:.0f} {ay + 14:.0f}" stroke="#f2d27a" stroke-width="{9 - k * 2}" fill="none" stroke-linecap="round" stroke-linejoin="round" opacity="{.95 - k * .25:.2f}" transform="rotate({rr:.0f} {ax:.0f} {ay:.0f})"/>'
    b += spark(BX + 150, BY + 80, 26) + spark(BX - 160, BY - 60, 18) + spark(1300, 600, 16, '#e8dcff')
    # ---- frog pitcher on the hill ----
    cap = ('<g transform="translate(6 -84) rotate(-8)" stroke-width="3.2"><path d="M-30 4 Q-28 -34 4 -36 Q36 -34 38 4Z" fill="#d94a4a"/>'
           '<path d="M32 2 Q60 -2 72 8 Q54 14 32 10Z" fill="#b83a3a"/><circle cx="4" cy="-35" r="4" fill="#b83a3a"/>'
           '<path d="M-14 -30 q-6 14 -6 32" fill="none" stroke-width="2" opacity=".5"/></g>')
    glove = '<g transform="translate(-58 -6)"><ellipse cx="0" cy="0" rx="22" ry="18" fill="#b0743c" stroke-width="3"/><path d="M-10 -6 q10 6 20 0" fill="none" stroke-width="2.4"/></g>'
    b += f'<ellipse cx="560" cy="784" rx="110" ry="14" fill="#000" opacity=".35" filter="url(#b3)"/>'
    b += frog(560, 782, 2.45, rot=4, look=(9, -9), mouth='O', hat=cap, front=glove,
              armR='M38 -24 q28 -14 42 -52', armL='M-34 -22 q-16 6 -22 16',
              legs=((-20, -6, -30, 4, -12), (20, -6, 28, 2, 10)))
    b += '<rect width="1920" height="1080" fill="url(#vig4)"/>'
    lines = [("IT'S", 165, 'w'), ('SPEEDING', 175, 'y'), ('UP!', 200, 'w')]
    return out('#05030f', d, b, lines, '#07030f', 36)


# =============================== 5: the library of invisible ink ===============================
def make_5():
    rnd = random.Random(505)
    VX, VY = 1240, 470
    d = FILTERS
    d += rad('bg5', VX, VY, 1200, [(0, '#2a1e3a', 1), (.5, '#140c20', 1), (1, '#06040a', 1)])
    d += rad('win5', VX, 420, 260, [(0, '#bfe6ff', .9), (.4, '#6aa0ff', .35), (1, '#3060ff', 0)])
    d += rad('cand5', 1460, 700, 560, [(0, '#ffd68a', .65), (.35, '#ffaa55', .22), (1, '#ff9040', 0)])
    d += lin('tab5', [(0, '#7a4e2c'), (1, '#4a2e18')])
    d += lin('page5', [(0, '#fff8e4'), (1, '#e8dcc0')], x2=1, y2=0)
    d += rad('vig5', 1150, 560, 1250, [(0, '#000', 0), (.55, '#000', 0), (1, '#000', .75)])
    b = '<rect width="1920" height="1080" fill="url(#bg5)"/>'

    def P(W, Y, z):
        return VX + W / z, VY + Y / z
    ZF, ZB = 1.0, 4.6
    TOP, FLOOR = (-1500, 420) if V else (-620, 420)
    # back wall + tall arched window
    bl, bt = P(-1250, TOP, ZB); br, bb = P(700, FLOOR, ZB)
    b += f'<rect x="{bl:.0f}" y="{bt:.0f}" width="{br - bl:.0f}" height="{bb - bt:.0f}" fill="#24182e"/>'
    b += f'<path d="M{VX - 70} {VY + 70} V{VY - 70} A70 70 0 0 1 {VX + 70} {VY - 70} V{VY + 70}Z" fill="#0c1430" stroke="#5a4a6a" stroke-width="6"/>'
    b += f'<path d="M{VX} {VY - 140} V{VY + 70} M{VX - 70} {VY - 20} H{VX + 70}" stroke="#5a4a6a" stroke-width="4"/>'
    b += f'<circle cx="{VX + 25}" cy="{VY - 80}" r="18" fill="#f4f8ff"/>'
    b += '<rect width="1920" height="1080" fill="url(#win5)"/>'
    # floor
    fl = [P(-1250, FLOOR, ZB), P(700, FLOOR, ZB), P(700, FLOOR, .55), P(-1250, FLOOR, .55)]
    b += f'<path d="{poly(fl)}" fill="#2a1a20"/>'
    for W in range(-1250, 701, 160):
        (x0, y0), (x1, y1) = P(W, FLOOR, ZB), P(W, FLOOR, .55)
        b += f'<path d="M{x0:.0f} {y0:.0f} L{x1:.0f} {y1:.0f}" stroke="#4a3040" stroke-width="2" opacity=".6"/>'
    # moonlight beam on the floor
    b += f'<path d="M{VX - 70} {VY + 70} L{VX + 70} {VY + 70} L{VX + 420} 1080 L{VX - 300} 1080Z" fill="#9fc8ff" opacity=".07" filter="url(#b12)"/>'

    def wall(W, dark):
        o = ''
        rows = 15 if V else 7
        for k in range(rows + 1):          # shelf boards
            Y = TOP + (FLOOR - TOP) * k / rows
            (x0, y0), (x1, y1) = P(W, Y, ZB), P(W, Y, ZF)
            o += f'<path d="M{x0:.0f} {y0:.0f} L{x1:.0f} {y1:.0f}" stroke="#5a3a24" stroke-width="{3 + 10 * (k / rows):.0f}" opacity="{.5 if dark else .9}"/>'
        for k in range(rows):
            Y0 = TOP + (FLOOR - TOP) * (k + 1) / rows; gap = (FLOOR - TOP) / rows
            z = ZB
            while z > ZF + .02:
                dz = rnd.uniform(.035, .07) * z * z / 3
                z1 = max(ZF, z - dz)
                h = gap * rnd.uniform(.62, .9)
                q = [P(W, Y0 - 6, z), P(W, Y0 - 6, z1), P(W, Y0 - h, z1), P(W, Y0 - h, z)]
                col = rnd.choice(['#3a2e5a', '#4a3a6a', '#2e4058', '#5a3a50', '#3a4a4a', '#4e4466'])
                o += f'<path d="{poly(q)}" fill="{col}" stroke="#120a14" stroke-width="1.5" opacity="{.55 if dark else .95}"/>'
                if rnd.random() < .5 and z < 2.2:   # blank label: invisible ink shimmer
                    (lx0, ly0), (lx1, ly1) = P(W, Y0 - h * .55, z), P(W, Y0 - h * .55, z1)
                    o += f'<path d="M{lx0:.0f} {ly0:.0f} L{lx1:.0f} {ly1:.0f}" stroke="#d8ccff" stroke-width="{3 / z:.1f}" stroke-dasharray="3 5" opacity=".35"/>'
                z = z1
        return o
    b += wall(-1250, True)
    b += wall(700, False)
    # ghostly invisible-ink shimmer floating from the shelves
    for _ in range(70):
        x = rnd.uniform(1300, 1900); y = rnd.uniform(60, 900)
        b += f'<path d="M{x:.0f} {y:.0f} q8 -8 16 0 t16 0" stroke="#c9b8ff" stroke-width="2" fill="none" opacity="{rnd.uniform(.12, .35):.2f}"/>'
    # ---- reading table ----
    b += f'<g transform="translate({130 if V else 0} 0)">'
    b += '<path d="M640 860 L1560 860 L1600 930 L600 930Z" fill="url(#tab5)" stroke="#1a0c04" stroke-width="5" stroke-linejoin="round"/>'
    b += '<path d="M600 930 L1600 930 L1600 975 L600 975Z" fill="#3a2212" stroke="#1a0c04" stroke-width="5"/>'
    b += '<path d="M640 975 V1080 M1560 975 V1080" stroke="#2a1608" stroke-width="34"/>'
    b += '<rect width="1920" height="1080" fill="url(#cand5)"/>'
    # ---- the huge open book: thick blank page block ----
    BX = 1110 + (0 if not V else 0)
    b += f'<ellipse cx="{BX}" cy="905" rx="330" ry="26" fill="#000" opacity=".45" filter="url(#b6)"/>'
    b += f'<path d="M{BX - 300} 880 L{BX - 300} 840 Q{BX - 150} 820 {BX} 850 Q{BX + 150} 820 {BX + 300} 840 L{BX + 300} 880 Q{BX + 150} 862 {BX} 892 Q{BX - 150} 862 {BX - 300} 880Z" fill="#7a2a2a" stroke="#1a0c04" stroke-width="4"/>'
    for k in range(6):
        y = 838 - k * 7
        b += f'<path d="M{BX - 290 + k * 4} {y} Q{BX - 150} {y - 22} {BX} {y + 8} Q{BX + 150} {y - 22} {BX + 290 - k * 4} {y}" fill="none" stroke="#d8ccb0" stroke-width="3"/>'
    # open pages: each page arcs up from the spine
    for sgn in (-1, 1):
        o = BX + sgn * 300
        pg = (f'M{BX} 842 Q{BX + sgn * 60} 760 {BX + sgn * 170} 752 Q{BX + sgn * 250} 750 {o} 778 L{o} 836 '
              f'Q{BX + sgn * 250} 812 {BX + sgn * 170} 814 Q{BX + sgn * 60} 818 {BX} 862Z')
        b += f'<path d="{pg}" fill="url(#page5)" stroke="#4a3a2a" stroke-width="3.5" stroke-linejoin="round"/>'
        for k in range(1, 4):   # page edges at the outer side
            b += f'<path d="M{o - sgn * k * 5} {778 + k * 3} L{o - sgn * k * 5} {836 + k * 3}" stroke="#c9b48a" stroke-width="2"/>'
        for k in range(6):      # invisible ink: faint dotted lines
            y = 772 + k * 8
            b += f'<path d="M{BX + sgn * 50} {y + 16 - k} Q{BX + sgn * 150} {y - 8} {BX + sgn * 270} {y + 6}" stroke="#a48cff" stroke-width="2.4" stroke-dasharray="2 7" fill="none" opacity=".5"/>'
    b += f'<path d="M{BX} 842 L{BX} 862" stroke="#4a3a2a" stroke-width="4"/>'
    b += f'<path d="M{BX - 30} 830 Q{BX} 850 {BX + 30} 830" stroke="#000" stroke-width="16" fill="none" opacity=".18" filter="url(#b6)"/>'
    # ---- five glowing readable pages rising from the book ----
    b += f'<circle cx="{BX + 60}" cy="560" r="300" fill="#ffd890" opacity=".22" filter="url(#b50)"/>'
    pages = [(BX - 150, 690, -16, .85), (BX - 10, 600, 8, .95), (BX + 170, 650, 20, .9), (BX + 70, 430, -10, 1.0), (BX + 300, 470, 14, .9)]
    for x, y, rot, sc in pages:
        o = f'<g transform="translate({x} {y}) rotate({rot}) scale({sc})">'
        o += '<rect x="-78" y="-100" width="156" height="200" rx="6" fill="#ffd890" opacity=".55" filter="url(#b12)"/>'
        o += '<path d="M-70 -92 L70 -92 L70 92 L-50 92 L-70 72Z" fill="#fffaf0" stroke="#8a6a3a" stroke-width="3"/>'
        o += '<path d="M-70 72 L-50 72 L-50 92" fill="#e8dcc0" stroke="#8a6a3a" stroke-width="2"/>'
        for k in range(9):
            w = rnd.uniform(70, 116)
            o += f'<path d="M-52 {-70 + k * 17} h{w:.0f}" stroke="#c9902a" stroke-width="5" stroke-linecap="round" opacity=".9"/>'
        o += '</g>'
        b += o
    b += spark(BX + 400, 360, 24) + spark(BX - 230, 560, 18) + spark(BX + 180, 330, 16) + spark(BX - 60, 470, 14)
    # candle (light source) on the table, right
    CXc, CYc = 1500, 880
    b += f'<circle cx="{CXc}" cy="{CYc - 150}" r="110" fill="#ffcf7a" opacity=".5" filter="url(#b24)"/>'
    b += f'<ellipse cx="{CXc}" cy="{CYc}" rx="50" ry="12" fill="#c9a24a" stroke="#2a1a0c" stroke-width="4"/>'
    b += f'<rect x="{CXc - 18}" y="{CYc - 110}" width="36" height="108" rx="6" fill="#f4ecd8" stroke="#2a1a0c" stroke-width="4"/>'
    b += f'<path d="M{CXc} {CYc - 110} l0 -12" stroke="#2a1a0c" stroke-width="3"/>'
    b += f'<path d="M{CXc} {CYc - 170} q16 22 0 46 q-16 -24 0 -46Z" fill="#ffe08a" stroke="#d9802a" stroke-width="3"/><ellipse cx="{CXc}" cy="{CYc - 136}" rx="5" ry="9" fill="#fff"/>'
    # ---- frog reader with glasses, leaning on the table at the left of the book ----
    b += frog(745, 862, 2.5, rot=4, look=(9, -6), mouth='O', hat=glasses(),
              armR='M38 -22 q22 -10 34 -34', armL='M-34 -22 q-18 4 -22 22',
              legs=((-20, -6, -24, 4, 0), (20, -6, 26, 4, 0)))
    b += '</g>'
    b += '<rect width="1920" height="1080" fill="url(#vig5)"/>'
    lines = [('WE CAN READ', 140, 'w'), ('5 PAGES', 250, 'y')]
    return out('#06040a', d, b, lines, '#07030c', 48)


if __name__ == '__main__':
    for n in (sys.argv[1:] or ['1', '2', '3', '4', '5']):
        if f'make_{n}' in globals():
            CUR.clear(); CUR['n'] = int(n)
            open(f'{ROOT}/dark-matter-96-percent-short{n}/thumb/A.html', 'w').write(globals()[f'make_{n}']())
    print('ok')
