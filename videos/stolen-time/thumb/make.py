# Thumbnails A-C for stolen-time (guideline 16-6 / 16-8, brief tools/briefs/thumb_art.md). Run: python3 videos/stolen-time/thumb/make.py
# A  3 HOURS = 23 YEARS   owner request (miya 2026-10-25): redraw of her favourite (wave wall, shallow sea, ringed black hole), the white astronaut
#                         replaced by the notebook frog in a space helmet RUNNING from the wave (S01, S52-S53; the planet is a theoretical model, S04)
# B  TIME IS ELASTIC      homage: the clock-hanging scene of Safety Last! (1923, public domain): the frog dangles from the bent minute hand of a
#                         drooping (elastic) building clock above a black-hole whirlpool (S07-S08 "time is elastic ... stretched, slowed")
# C  WHO STOLE MY TIME?   intuitive: a pocket watch stretched like taffy into a black hole, the frog in a helmet clinging to its chain (S42, S83 "stolen")
import os, sys, math, random
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', '..', 'tools'))
from thumb_lib import page, svg, lin, rad, spark

INK = '#1d2b1c'; GREEN = '#6aa55a'; DARKG = '#4d8a4a'; BELLY = '#9cc98a'

FILTERS = ''.join(f'<filter id="b{n}" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="{n}"/></filter>' for n in (3, 6, 12, 24, 50))


def P(pts):
    return ' '.join(f'{a:.1f},{b:.1f}' for a, b in pts)


# ---------------- mascot frog (tools/assets/frog.svg body), posable ----------------
def limb(d, w=7.5, wi=3.4):
    return f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="{w}"/><path d="{d}" fill="none" stroke="{GREEN}" stroke-width="{wi}"/>'


def end_of(d):
    n = [float(v) for v in d.replace('M', ' ').replace('q', ' ').split()]
    return n[0] + n[-2], n[1] + n[-1]


def frog(x, y, s, rot=0, flip=False, look=(0, 0), mouth='O', armL=None, armR=None, legs=None, helmet=False, hat=False,
         brows=True, back='', front='', shadow=False):
    sx = -s if flip else s
    g = [f'<g transform="translate({x} {y}) rotate({rot}) scale({sx} {s})" stroke="{INK}" stroke-linejoin="round" stroke-linecap="round">', back]
    if shadow:
        g.append('<ellipse cx="0" cy="8" rx="50" ry="8" fill="#000" opacity=".2" stroke="none"/>')
    if helmet:   # small life-support pack behind the body
        g.append('<rect x="-50" y="-58" width="20" height="42" rx="7" fill="#c9ced8" stroke-width="3"/><rect x="-46" y="-52" width="5" height="30" rx="2" fill="#fff" stroke="none" opacity=".6"/>')
    # legs: (hip x, hip y, foot x, foot y, foot angle)
    for hx, hy, fx, fy, fa in (legs or ((-20, -6, -22, 4, 0), (20, -6, 22, 4, 0))):
        if abs(fx - hx) + abs(fy - hy) > 14:
            g.append(limb(f'M{hx} {hy} L{fx} {fy}', 15, 9))
        g.append(f'<ellipse cx="{fx}" cy="{fy}" rx="16" ry="9" transform="rotate({fa} {fx} {fy})" fill="{DARKG}" stroke-width="3.2"/>')
    g.append(f'<path d="M-34 0 q-6 -64 34 -70 q40 -2 42 62 q0 10 -6 12 q-36 6 -70 -4z" fill="{GREEN}" stroke-width="4"/>')
    g.append(f'<ellipse cx="2" cy="-12" rx="22" ry="20" fill="{BELLY}" stroke="none" opacity=".7"/>')
    g.append('<path d="M-24 -50 q6 -14 18 -16" fill="none" stroke="#b6dea0" stroke-width="3" opacity=".8"/>')
    lx, ly = look
    for ex in (-10, 22):   # big round eyes, small pupils = surprised
        g.append(f'<circle cx="{ex}" cy="-66" r="13.5" fill="#f4f5ea" stroke-width="3.2"/>')
        g.append(f'<circle cx="{ex + 1 + lx}" cy="{-66 + ly}" r="4.4" fill="{INK}" stroke="none"/>')
        g.append(f'<circle cx="{ex + 2.4 + lx}" cy="{-67.6 + ly}" r="1.5" fill="#fff" stroke="none"/>')
    if brows:
        g.append('<path d="M-22 -88 q12 -9 24 -1 M10 -89 q12 -8 24 1" fill="none" stroke-width="3.4"/>')
    if mouth == 'O':   # wide-open surprised mouth with tongue
        g.append('<ellipse cx="6" cy="-38" rx="10" ry="12" fill="#7a2f33" stroke-width="3"/><ellipse cx="6" cy="-31" rx="6" ry="4" fill="#e07b7b" stroke="none"/>')
    else:
        g.append('<ellipse cx="6" cy="-41" rx="6" ry="7.5" fill="#7a2f33" stroke-width="3"/>')
    g.append('<ellipse cx="-18" cy="-48" rx="5" ry="3" fill="#e98a8a" stroke="none" opacity=".55"/><ellipse cx="30" cy="-48" rx="5" ry="3" fill="#e98a8a" stroke="none" opacity=".55"/>')
    if helmet:   # glass bubble around the head + silver collar
        g.append('<circle cx="6" cy="-58" r="45" fill="#bfe6ff" fill-opacity=".13" stroke="#e8f6ff" stroke-width="3.4" stroke-opacity=".95"/>')
        g.append('<path d="M-26 -82 q12 -18 32 -21" fill="none" stroke="#fff" stroke-width="5" opacity=".8"/><path d="M42 -40 q6 -10 6 -22" fill="none" stroke="#fff" stroke-width="3" opacity=".5"/>')
        g.append('<ellipse cx="6" cy="-16" rx="40" ry="9" fill="#d3d9e3" stroke-width="3.2"/><path d="M-30 -18 q36 8 72 0" fill="none" stroke="#fff" stroke-width="2.2" opacity=".8"/>')
    if hat:      # straw boater, knocked off the head
        g.append('<g transform="translate(40 -104) rotate(24)"><ellipse cx="0" cy="8" rx="40" ry="9" fill="#e7c77c" stroke-width="3.2"/>'
                 '<path d="M-24 8 L-22 -14 Q0 -20 22 -14 L24 8 Z" fill="#efd590" stroke-width="3.2"/><path d="M-23 -2 L23 -2 L23.5 5 L-23.5 5Z" fill="#2e2a4a" stroke-width="2"/>'
                 '<path d="M-30 6 q30 6 60 0" fill="none" stroke="#fff6d0" stroke-width="2" opacity=".7"/></g>')
    for a in (armL or 'M-34 -22 q-14 6 -16 22', armR or 'M38 -22 q14 6 16 22'):
        g.append(limb(a)); ex_, ey_ = end_of(a)
        g.append(f'<circle cx="{ex_:.1f}" cy="{ey_:.1f}" r="5.6" fill="{GREEN}" stroke-width="3"/>')
    g.append(front); g.append('</g>')
    return ''.join(g)


def starfield(rnd, n, box, col='#eef4ff', skip=None):
    x0, y0, x1, y1 = box; o = ''
    for _ in range(n):
        x = rnd.uniform(x0, x1); y = rnd.uniform(y0, y1)
        if skip and skip(x, y): continue
        o += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{rnd.choice([1.1, 1.6, 2.2, 2.8])}" fill="{col}" opacity="{rnd.uniform(.2, .85):.2f}"/>'
    return o


def corner(x, y):
    return x > 1540 and y > 850


# =========================== A: wave wall (owner's redraw) ===========================
def crest(x):
    return 520 - 72 * math.exp(-((x - 820) / 430) ** 2) + 78 * max(0, (x - 1280) / 640) ** 1.5 + 10 * math.sin(x / 93)


def make_A():
    rnd = random.Random(11)
    d = FILTERS
    d += lin('skyA', [(0, '#0a1430'), (.45, '#13234a'), (.8, '#0b1a30'), (1, '#071220')])
    d += rad('nebA', 430, 260, 620, [(0, '#33489a', .55), (.5, '#22356f', .2), (1, '#000', 0)])
    d += rad('haloA', 1490, 290, 520, [(0, '#ffd9a0', .35), (.35, '#f2a85a', .12), (1, '#000', 0)])
    d += lin('waveA', [(0, '#1b5c63'), (.1, '#0e3a42'), (.3, '#061b22'), (.65, '#030c11'), (1, '#020609')])
    d += lin('seaA', [(0, '#16505a'), (.25, '#0d3740'), (1, '#03141a')])
    d += lin('ringA', [(0, '#c0562a'), (.25, '#f0a050'), (.5, '#fff1c8'), (.75, '#f0a050'), (1, '#c0562a')], x2=1, y2=0)
    d += rad('reflA', 1490, 960, 460, [(0, '#f6c27a', .28), (.5, '#e09a50', .08), (1, '#000', 0)])
    d += rad('vigA', 960, 540, 1150, [(0, '#000', 0), (.72, '#000', 0), (1, '#000', .5)])
    b = '<rect width="1920" height="1080" fill="url(#skyA)"/><rect width="1920" height="1080" fill="url(#nebA)"/>'
    b += starfield(rnd, 260, (0, 0, 1920, 560))
    b += '<rect width="1920" height="1080" fill="url(#haloA)"/>'
    # ---- ringed black hole ----
    cx, cy = 1490, 290
    ring = lambda arc, w, col, op, f='': (f'<g transform="translate({cx} {cy}) rotate(-8)"><path d="{arc}" fill="none" stroke="{col}" stroke-width="{w}" opacity="{op}" {f}/></g>')
    back = 'M-420 0 A420 80 0 0 1 420 0'; front = 'M-420 0 A420 80 0 0 0 420 0'
    b += ring(back, 46, 'url(#ringA)', .35, 'filter="url(#b12)"') + ring(back, 16, 'url(#ringA)', .9) + ring(back, 4, '#fff6dc', .9)
    b += f'<circle cx="{cx}" cy="{cy}" r="200" fill="#ffb66a" opacity=".35" filter="url(#b24)"/>'
    b += f'<circle cx="{cx}" cy="{cy}" r="176" fill="none" stroke="#f6c47a" stroke-width="14" opacity=".55" filter="url(#b6)"/>'
    b += f'<circle cx="{cx}" cy="{cy}" r="170" fill="#000"/>'
    b += f'<circle cx="{cx}" cy="{cy}" r="172" fill="none" stroke="#ffe3a8" stroke-width="5"/><circle cx="{cx}" cy="{cy}" r="184" fill="none" stroke="#e8a85e" stroke-width="2" opacity=".6"/>'
    b += ring(front, 50, 'url(#ringA)', .4, 'filter="url(#b12)"') + ring(front, 18, 'url(#ringA)', 1) + ring(front, 5, '#fffaf0', 1)
    b += spark(1110, 90, 22) + spark(1830, 520, 16) + spark(260, 470, 16) + spark(1700, 90, 12)
    # ---- the wall of black water ----
    xs = list(range(0, 1941, 20))
    b += f'<path d="M0 {crest(0):.1f} ' + ' '.join(f'L{x} {crest(x):.1f}' for x in xs) + ' L1940 880 L0 880 Z" fill="url(#waveA)"/>'
    # backlit translucent band just under the crest (light of the ring)
    b += f'<path d="M0 {crest(0) + 10:.1f} ' + ' '.join(f'L{x} {crest(x) + 10:.1f}' for x in xs) + ' ' + ' '.join(f'L{x} {crest(x) + 70:.1f}' for x in reversed(xs)) + 'Z" fill="#3fa3a6" opacity=".22" filter="url(#b12)"/>'
    for _ in range(170):   # streaks running down the face
        x = rnd.uniform(0, 1920); y0 = crest(x) + rnd.uniform(20, 60); L = rnd.uniform(80, 330)
        b += f'<path d="M{x:.0f} {y0:.0f} q{rnd.uniform(-4, 4):.1f} {L / 2:.0f} {rnd.uniform(-6, 6):.1f} {L:.0f}" stroke="#4fb0b2" stroke-width="{rnd.choice([1.5, 2, 2.5])}" fill="none" opacity="{rnd.uniform(.12, .35):.2f}"/>'
    for _ in range(40):   # dark vertical shadow folds
        x = rnd.uniform(0, 1920); y0 = crest(x) + 80
        b += f'<path d="M{x:.0f} {y0:.0f} l{rnd.uniform(-10, 10):.0f} {rnd.uniform(150, 300):.0f}" stroke="#000" stroke-width="{rnd.uniform(8, 22):.0f}" opacity=".18" filter="url(#b6)"/>'
    # foam crest
    foam = ''
    for x in range(-20, 1960, 15):
        r = rnd.uniform(13, 30); yy = crest(x) + rnd.uniform(-10, 8)
        foam += f'<circle cx="{x + rnd.uniform(-5, 5):.0f}" cy="{yy:.0f}" r="{r:.0f}" fill="#b9d6da"/>'
    b += f'<g opacity=".95">{foam}</g>'
    for x in range(-20, 1960, 13):
        r = rnd.uniform(9, 22); yy = crest(x) + rnd.uniform(-20, 0)
        b += f'<circle cx="{x + rnd.uniform(-5, 5):.0f}" cy="{yy:.0f}" r="{r:.0f}" fill="#f2fbfc" opacity="{rnd.uniform(.75, 1):.2f}"/>'
    for _ in range(320):   # spray above the crest
        x = rnd.uniform(0, 1920); yy = crest(x) - rnd.uniform(15, 120) ** 1.0
        if x < 1080 and yy < 440: continue   # keep the text clean
        b += f'<circle cx="{x:.0f}" cy="{yy:.0f}" r="{rnd.uniform(1.5, 5):.1f}" fill="#eaf8fa" opacity="{rnd.uniform(.3, .9):.2f}"/>'
    # whitewater at the foot of the wall
    for x in range(-20, 1960, 22):
        b += f'<ellipse cx="{x:.0f}" cy="{868 + rnd.uniform(-8, 6):.0f}" rx="{rnd.uniform(18, 40):.0f}" ry="{rnd.uniform(6, 13):.0f}" fill="#cfe7ea" opacity="{rnd.uniform(.35, .7):.2f}"/>'
    # ---- shallow sea ----
    b += '<rect x="0" y="874" width="1920" height="206" fill="url(#seaA)"/>'
    b += '<path d="M0 876 C400 868 900 882 1300 872 C1600 866 1800 874 1920 870" stroke="#8fd0d0" stroke-width="3" fill="none" opacity=".55"/>'
    b += '<rect x="0" y="874" width="1920" height="206" fill="url(#reflA)"/>'
    b += '<ellipse cx="1490" cy="960" rx="26" ry="70" fill="#ffe2a8" opacity=".25" filter="url(#b12)"/>'
    for _ in range(90):
        x = rnd.uniform(0, 1920); y = rnd.uniform(895, 1070); w = rnd.uniform(30, 120)
        b += f'<path d="M{x:.0f} {y:.0f} q{w / 2:.0f} -5 {w:.0f} 0" stroke="#5fb0b4" stroke-width="2" fill="none" opacity="{rnd.uniform(.15, .45):.2f}"/>'
    # ---- frog running away from the wave (toward the viewer, to the left) ----
    fx, fy = 600, 1012
    b += f'<ellipse cx="{fx + 20}" cy="{fy + 14}" rx="190" ry="26" fill="#aee6e8" opacity=".25" filter="url(#b6)"/>'
    b += f'<circle cx="{fx}" cy="{fy - 150}" r="210" fill="#bfefff" opacity=".12" filter="url(#b24)"/>'
    # splash kicked up behind the raised foot
    spx, spy = fx + 150, fy - 6
    spl = f'<ellipse cx="{spx}" cy="{spy + 12}" rx="110" ry="20" fill="#e8fbfc" opacity=".8"/>'
    for k in range(9):   # spray fingers
        a = math.radians(-128 + k * 14); L = rnd.uniform(130, 240)
        ex, ey = spx + math.cos(a) * L, spy + 10 + math.sin(a) * L
        spl += f'<path d="M{spx + math.cos(a) * 18:.0f} {spy + 8:.0f} Q{spx + math.cos(a) * L * .5:.0f} {spy + math.sin(a) * L * .9:.0f} {ex:.0f} {ey:.0f}" stroke="#e8fbfc" stroke-width="{rnd.uniform(5, 9):.1f}" fill="none" opacity=".8"/>'
        spl += f'<circle cx="{ex:.0f}" cy="{ey:.0f}" r="{rnd.uniform(6, 10):.1f}" fill="#f4feff"/>'
    for _ in range(26):
        a = math.radians(rnd.uniform(-130, -5)); L = rnd.uniform(60, 260)
        spl += f'<circle cx="{spx + math.cos(a) * L:.0f}" cy="{spy + math.sin(a) * L:.0f}" r="{rnd.uniform(3, 8):.1f}" fill="#e8fbfc" opacity="{rnd.uniform(.5, 1):.2f}"/>'
    b += spl
    # little ripple rings where the planted foot hits the water
    b += ''.join(f'<ellipse cx="{fx - 50}" cy="{fy + 6}" rx="{r}" ry="{r * .22:.0f}" fill="none" stroke="#bfeef0" stroke-width="3" opacity="{o}"/>' for r, o in ((70, .6), (120, .35), (170, .2)))
    # speed lines
    b += ''.join(f'<path d="M{fx + a} {fy - c} l{w} 0" stroke="#e6fbff" stroke-width="7" stroke-linecap="round" opacity=".55"/>' for a, c, w in ((150, 210, 110), (170, 160, 80), (140, 260, 70)))
    b += frog(fx, fy, 3.05, rot=-9, look=(5, -4), mouth='O', helmet=True, shadow=False,
              armL='M-34 -22 q-30 -8 -40 -46', armR='M38 -22 q28 4 44 -14',
              legs=((-18, -8, -30, 6, -10), (22, -10, 60, -4, -35)))
    b += '<rect width="1920" height="1080" fill="url(#vigA)"/>'
    lines = [('3 HOURS =', 186, 'w'), ('<span class="g">23</span> YEARS', 186, 'w')]
    return page('#0a1430', svg(d, b), lines, outline='#050b18', top=46)


# =========================== B: Safety Last! homage ===========================
CB = (1450, 330); RF = 262   # clock centre, frame radius


def warp(u, v):
    """clock-local (u, v) -> picture coords; the lower half droops (time is elastic), more on the left"""
    if v > 0:
        t = v / RF
        v = v + 150 * t ** 2.3 * (1 + .55 * max(-1, min(1, -u / RF)))
        u = u * (1 - .06 * t)
    return CB[0] + u, CB[1] + v


def circ(r, n=120):
    return [warp(r * math.cos(2 * math.pi * k / n), r * math.sin(2 * math.pi * k / n)) for k in range(n)]


def make_B():
    rnd = random.Random(23)
    d = FILTERS
    d += lin('skyB', [(0, '#160c2e'), (.4, '#2a1550'), (.75, '#1a0c33'), (1, '#07030f')])
    d += rad('moonB', 1450, 330, 760, [(0, '#ffdca0', .30), (.4, '#c98ad8', .10), (1, '#000', 0)])
    d += lin('wallB', [(0, '#5c4a72'), (.6, '#3c2d55'), (1, '#251a38')], x2=0, y2=1)
    d += rad('faceB', 1420, 300, 330, [(0, '#fffbea', 1), (0.55, '#f6e7bf', 1), (1, '#d9bd84', 1)])
    d += lin('frameB', [(0, '#e9c47a'), (.5, '#a8772e'), (1, '#5a3a14')], x2=1, y2=1)
    d += rad('vortB', 760, 1080, 820, [(0, '#ffe9b0', 1), (.12, '#ff9c4a', .9), (.32, '#c0398a', .55), (.6, '#4a1a7a', .25), (1, '#000', 0)])
    d += rad('vigB', 960, 500, 1150, [(0, '#000', 0), (.7, '#000', 0), (1, '#000', .55)])
    b = '<rect width="1920" height="1080" fill="url(#skyB)"/>'
    b += starfield(rnd, 220, (0, 0, 1920, 900), '#f1e8ff', corner)
    # ---- the whirlpool far below (a black hole seen from above, instead of the street) ----
    vx, vy = 760, 1085
    b += f'<ellipse cx="{vx}" cy="{vy}" rx="900" ry="300" fill="url(#vortB)" opacity=".9"/>'
    sp = ''
    for k in range(7):   # spiral arms (log spirals flattened by perspective)
        ph = k * 2 * math.pi / 7; pts = []
        for i in range(70):
            t = i / 69; r = 120 + 760 * t ** 1.4; a = ph + 4.2 * t
            pts.append((vx + r * math.cos(a), vy + .3 * r * math.sin(a)))
        sp += f'<polyline points="{P(pts)}" fill="none" stroke="{["#ffd27a", "#ff8a4a", "#e05aa0"][k % 3]}" stroke-width="{9 - k % 3 * 2}" opacity=".5" stroke-linecap="round"/>'
    b += f'<g filter="url(#b3)">{sp}</g>'
    b += f'<ellipse cx="{vx}" cy="{vy}" rx="250" ry="78" fill="#ffd894" opacity=".6" filter="url(#b12)"/>'
    b += f'<ellipse cx="{vx}" cy="{vy}" rx="200" ry="62" fill="none" stroke="#fff3cf" stroke-width="7"/>'
    b += f'<ellipse cx="{vx}" cy="{vy}" rx="186" ry="56" fill="#000"/>'
    # ---- building wall with the clock ----
    wall = '<path d="M1000 0 L1920 0 L1920 690 L1000 690 Z" fill="url(#wallB)"/>'
    for i, y in enumerate(range(0, 690, 58)):   # stone courses
        wall += f'<path d="M1000 {y} L1920 {y}" stroke="#20162f" stroke-width="3" opacity=".7"/>'
        for x in range(1000 + (60 if i % 2 else 0), 1920, 120):
            wall += f'<path d="M{x} {y} l0 58" stroke="#20162f" stroke-width="3" opacity=".6"/>'
            wall += f'<path d="M{x + 4} {y + 5} l108 0" stroke="#8c7aa8" stroke-width="2" opacity=".35"/>'
    wall += '<path d="M1000 0 L1000 690" stroke="#c9b3e8" stroke-width="6" opacity=".6"/><path d="M960 0 L1000 0 L1000 690 L960 720 Z" fill="#1b1229"/>'
    wall += '<rect x="960" y="686" width="960" height="40" fill="#7c6a94" stroke="#1a1028" stroke-width="4"/><rect x="960" y="726" width="960" height="26" fill="#000" opacity=".35" filter="url(#b6)"/>'
    wall += '<rect x="964" y="690" width="952" height="8" fill="#d6c4ee" opacity=".5"/>'
    for x in range(990, 1920, 60):
        wall += f'<rect x="{x}" y="722" width="26" height="22" fill="#5d4c78" stroke="#1a1028" stroke-width="3"/>'
    b += wall
    b += '<rect width="1920" height="1080" fill="url(#moonB)"/>'
    # clock shadow on the wall, frame, face, drips
    b += f'<polygon points="{P([(x + 20, y + 24) for x, y in circ(RF)])}" fill="#000" opacity=".45" filter="url(#b12)"/>'
    b += f'<polygon points="{P(circ(RF + 30))}" fill="#ffd28a" opacity=".25" filter="url(#b24)"/>'
    b += f'<polygon points="{P(circ(RF))}" fill="url(#frameB)" stroke="#2a1606" stroke-width="7" stroke-linejoin="round"/>'
    b += f'<polygon points="{P(circ(RF - 30))}" fill="url(#faceB)" stroke="#5a3a14" stroke-width="4" stroke-linejoin="round"/>'
    # drips hanging from the drooping rim
    for u, L, w in ((-150, 120, 30), (-60, 80, 24), (40, 50, 20)):
        x0, y0 = warp(u, math.sqrt(max(0, RF ** 2 - u ** 2)) - 6)
        b += (f'<path d="M{x0 - w:.0f} {y0 - 10:.0f} C{x0 - w:.0f} {y0 + L * .6:.0f} {x0 - w * .6:.0f} {y0 + L:.0f} {x0:.0f} {y0 + L:.0f} '
              f'C{x0 + w * .6:.0f} {y0 + L:.0f} {x0 + w:.0f} {y0 + L * .6:.0f} {x0 + w:.0f} {y0 - 10:.0f} Z" fill="url(#frameB)" stroke="#2a1606" stroke-width="5"/>')
        b += f'<ellipse cx="{x0 - w * .35:.0f}" cy="{y0 + L * .55:.0f}" rx="{w * .18:.0f}" ry="{L * .2:.0f}" fill="#fff0c8" opacity=".7"/>'
    ticks = ''
    for k in range(60):
        a = 2 * math.pi * k / 60; big = k % 5 == 0; r0 = RF - 44; r1 = r0 - (40 if big else 16)
        p0 = warp(r0 * math.cos(a), r0 * math.sin(a)); p1 = warp(r1 * math.cos(a), r1 * math.sin(a))
        ticks += f'<path d="M{p0[0]:.1f} {p0[1]:.1f} L{p1[0]:.1f} {p1[1]:.1f}" stroke="#2c1a08" stroke-width="{13 if big else 4}" stroke-linecap="{"butt" if big else "round"}"/>'
    b += ticks
    b += f'<polygon points="{P(circ(RF - 98))}" fill="none" stroke="#b08a50" stroke-width="3" opacity=".6"/>'
    # hour hand (short, to about 10 o'clock)
    hx, hy = warp(-120, -78)
    b += f'<path d="M{CB[0]} {CB[1]} L{hx:.0f} {hy:.0f}" stroke="#1a0f04" stroke-width="24" stroke-linecap="round"/><path d="M{CB[0]} {CB[1]} L{hx:.0f} {hy:.0f}" stroke="#4a3418" stroke-width="10" stroke-linecap="round"/>'
    # minute hand bent outward and down under the frog's weight
    tipx, tipy = 1105, 572
    mh = f'M{CB[0]} {CB[1]} L1270 432 Q1180 480 {tipx} {tipy}'
    b += f'<path d="{mh}" stroke="#000" stroke-width="30" fill="none" stroke-linecap="round" opacity=".35" transform="translate(14 18)" filter="url(#b6)"/>'
    b += f'<path d="{mh}" stroke="#1a0f04" stroke-width="22" fill="none" stroke-linecap="round"/><path d="{mh}" stroke="#5a3e1c" stroke-width="9" fill="none" stroke-linecap="round"/>'
    b += f'<path d="M{CB[0] - 4} {CB[1] - 6} L1272 424" stroke="#c9a46a" stroke-width="3" opacity=".7"/>'
    b += f'<circle cx="{CB[0]}" cy="{CB[1]}" r="22" fill="#e7c47a" stroke="#1a0f04" stroke-width="6"/><circle cx="{CB[0] - 5}" cy="{CB[1] - 6}" r="6" fill="#fff6d6"/>'
    # frog hanging from the tip, legs dangling over the abyss, boater flying off
    s = 2.55; fx, fy = tipx - 4 * s, tipy + 122 * s
    b += f'<circle cx="{fx}" cy="{fy - 120}" r="200" fill="#ffd6a0" opacity=".14" filter="url(#b24)"/>'
    b += frog(fx, fy, s, rot=6, look=(-3, 6), mouth='O', hat=True,
              armL='M-30 -40 q-14 -40 26 -82', armR='M36 -40 q2 -44 -26 -82',
              legs=((-18, -6, -30, 14, 30), (20, -6, 30, 22, -20)))
    # grip pads over the hand
    b += f'<circle cx="{tipx - 4:.0f}" cy="{tipy + 2:.0f}" r="14" fill="{GREEN}" stroke="{INK}" stroke-width="6"/>'
    b += spark(1260, 160, 22) + spark(1840, 720, 14) + spark(560, 640, 18) + spark(1800, 120, 16) + spark(980, 900, 14, '#ffe6c0', .7)
    b += '<rect width="1920" height="1080" fill="url(#vigB)"/>'
    lines = [('TIME IS', 170, 'w'), ('ELASTIC', 236, 'y')]
    return page('#160c2e', svg(d, b), lines, outline='#0c0518', top=50)


# =========================== C: the watch stolen by a black hole ===========================
def make_C():
    rnd = random.Random(37)
    d = FILTERS
    d += lin('skyC', [(0, '#060a1c'), (.5, '#0d1030'), (1, '#05050e')], x2=1, y2=1)
    d += rad('nebC', 1380, 460, 900, [(0, '#ff9a5a', .30), (.25, '#b4407a', .22), (.6, '#3a1f6a', .15), (1, '#000', 0)])
    d += lin('diskC', [(0, '#7a2a6a'), (.2, '#ff7a3a'), (.5, '#fff2c8'), (.8, '#ff7a3a'), (1, '#7a2a6a')], x2=1, y2=0)
    d += rad('goldC', 0, 0, 120, [(0, '#fff3c0', 1), (.5, '#f2c45a', 1), (1, '#9a6a1a', 1)])
    d += rad('faceC', -20, -20, 110, [(0, '#ffffff', 1), (.7, '#f6eedb', 1), (1, '#d8c9a4', 1)])
    d += lin('ribC', [(0, '#f6eedb'), (.45, '#ffe2a8'), (1, '#ff8a3a')], x2=1, y2=-.4)
    d += rad('vigC', 960, 540, 1150, [(0, '#000', 0), (.7, '#000', 0), (1, '#000', .55)])
    b = '<rect width="1920" height="1080" fill="url(#skyC)"/><rect width="1920" height="1080" fill="url(#nebC)"/>'
    b += starfield(rnd, 300, (0, 0, 1920, 1080), '#f4eeff', corner)
    cx, cy = 1430, 470
    disk = lambda arc, w, col, op, f='': f'<g transform="translate({cx} {cy}) rotate(12)"><path d="{arc}" fill="none" stroke="{col}" stroke-width="{w}" opacity="{op}" {f}/></g>'
    back = 'M-460 0 A460 110 0 0 1 460 0'; front = 'M-460 0 A460 110 0 0 0 460 0'
    for w, o, f in ((120, .35, 'filter="url(#b24)"'), (60, .8, 'filter="url(#b6)"'), (22, 1, ''), (6, 1, '')):
        b += disk(back, w, 'url(#diskC)' if w > 6 else '#fff8e0', o, f)
    # ---- stretched pocket watch being pulled in ----
    wx, wy = 790, 690   # watch centre
    ang = math.degrees(math.atan2(cy - wy, cx - wx))
    # the watch face smeared into a tapering ribbon (spaghettified), drawn BEHIND the hole so it vanishes into the shadow
    c0 = (wx + 20, wy - 10); c1 = (cx - 330, cy + 190); c2 = (cx - 60, cy + 30)
    cl = []
    for i in range(61):
        t = i / 60
        cl.append(((1 - t) ** 2 * c0[0] + 2 * (1 - t) * t * c1[0] + t * t * c2[0], (1 - t) ** 2 * c0[1] + 2 * (1 - t) * t * c1[1] + t * t * c2[1], t))
    left, right = [], []
    for i, (x, y, t) in enumerate(cl):
        j = min(i + 1, 60); k = max(i - 1, 0)
        tx, ty = cl[j][0] - cl[k][0], cl[j][1] - cl[k][1]; ln = math.hypot(tx, ty) or 1; nx, ny = -ty / ln, tx / ln
        hw = 128 * (1 - t) ** 1.05 + 6
        left.append((x + nx * hw, y + ny * hw)); right.append((x - nx * hw, y - ny * hw))
    b += f'<polygon points="{P(left + right[::-1])}" fill="#ffb060" opacity=".35" filter="url(#b12)"/>'
    b += f'<polygon points="{P(left + right[::-1])}" fill="url(#ribC)" stroke="#5a3a0a" stroke-width="6" stroke-linejoin="round"/>'
    for side, col in ((left, '#f2c45a'), (right, '#f2c45a')):   # gold case edges stretched along
        b += f'<polyline points="{P(side)}" fill="none" stroke="{col}" stroke-width="14" stroke-linecap="round"/><polyline points="{P(side)}" fill="none" stroke="#fff3c0" stroke-width="3" opacity=".8"/>'
    for f in (-.55, -.25, .1, .4, .62):   # stretched hour ticks + hands smeared along the ribbon
        pts = []
        for i, (x, y, t) in enumerate(cl[4:46]):
            i += 4; j = min(i + 1, 60); k = max(i - 1, 0)
            tx, ty = cl[j][0] - cl[k][0], cl[j][1] - cl[k][1]; ln = math.hypot(tx, ty) or 1; nx, ny = -ty / ln, tx / ln
            hw = (128 * (1 - t) ** 1.05 + 6) * f
            pts.append((x + nx * hw, y + ny * hw))
        b += f'<polyline points="{P(pts[::2][:8 + int(abs(f) * 10)])}" fill="none" stroke="#2c1a08" stroke-width="{7 if abs(f) > .3 else 4}" stroke-linecap="round" stroke-dasharray="26 34" opacity=".85"/>'
    # lensed upper arc of the disk (light bent over the hole)
    b += f'<path d="M{cx - 230} {cy + 10} A230 210 0 0 1 {cx + 230} {cy + 10}" fill="none" stroke="#ffcf8a" stroke-width="16" opacity=".6" filter="url(#b6)"/>'
    b += f'<circle cx="{cx}" cy="{cy}" r="196" fill="#ff9a50" opacity=".4" filter="url(#b24)"/>'
    b += f'<circle cx="{cx}" cy="{cy}" r="178" fill="#000"/><circle cx="{cx}" cy="{cy}" r="181" fill="none" stroke="#ffe6b0" stroke-width="5"/>'
    # front half of the disk passes in front of the tail end
    for w, o, f in ((120, .35, 'filter="url(#b24)"'), (60, .8, 'filter="url(#b6)"'), (22, 1, ''), (6, 1, '')):
        b += disk(front, w, 'url(#diskC)' if w > 6 else '#fff8e0', o, f)
    # little clock pieces (ticks, a numeral dot, a tiny gear) flying into the hole
    for k in range(16):
        t = rnd.uniform(.15, .95); a = rnd.uniform(-1, 1)
        px = wx + (cx - wx) * t + rnd.uniform(-90, 90); py = wy + (cy - wy) * t + rnd.uniform(-160, 110)
        if math.hypot(px - cx, py - cy) < 200 or py < 430: continue
        if rnd.random() < .5:
            b += f'<rect x="{px:.0f}" y="{py:.0f}" width="{rnd.uniform(16, 28):.0f}" height="7" rx="3" fill="#2c1a08" stroke="#f6eedb" stroke-width="2" transform="rotate({rnd.uniform(0, 180):.0f} {px:.0f} {py:.0f})"/>'
        else:
            b += f'<circle cx="{px:.0f}" cy="{py:.0f}" r="{rnd.uniform(5, 10):.0f}" fill="#f2c45a" stroke="#5a3a0a" stroke-width="3"/>'
    gear = '<g transform="translate(1130 760) rotate(20)">' + ''.join(f'<rect x="-6" y="-38" width="12" height="16" fill="#e0b050" stroke="#5a3a0a" stroke-width="3" transform="rotate({k * 45})"/>' for k in range(8))
    gear += '<circle r="28" fill="#e8bc5a" stroke="#5a3a0a" stroke-width="4"/><circle r="9" fill="#2a1a3a" stroke="#5a3a0a" stroke-width="3"/></g>'
    b += gear
    # the watch itself, squashed along the pull direction
    w = f'<g transform="translate({wx} {wy}) rotate({ang:.1f}) scale(1.22 .86) rotate({-ang:.1f})">'
    w += '<circle r="128" fill="#ffd27a" opacity=".35" filter="url(#b24)"/>'
    w += '<rect x="-16" y="-160" width="32" height="30" rx="8" fill="url(#goldC)" stroke="#3a2406" stroke-width="5"/><circle cx="0" cy="-172" r="18" fill="none" stroke="#3a2406" stroke-width="11"/><circle cx="0" cy="-172" r="18" fill="none" stroke="#f2c45a" stroke-width="5"/>'
    w += '<circle r="122" fill="url(#goldC)" stroke="#3a2406" stroke-width="7"/><circle r="100" fill="url(#faceC)" stroke="#6a4a14" stroke-width="4"/>'
    for k in range(60):
        a = 2 * math.pi * k / 60; big = k % 5 == 0; r0 = 90; r1 = r0 - (16 if big else 6)
        w += f'<path d="M{r0 * math.cos(a):.1f} {r0 * math.sin(a):.1f} L{r1 * math.cos(a):.1f} {r1 * math.sin(a):.1f}" stroke="#2c1a08" stroke-width="{6 if big else 2}"/>'
    w += '<path d="M0 0 L-8 -64" stroke="#1a0f04" stroke-width="7" stroke-linecap="round"/><path d="M0 0 L46 22" stroke="#1a0f04" stroke-width="9" stroke-linecap="round"/><path d="M0 0 L-40 56" stroke="#c0392b" stroke-width="3"/>'
    w += '<circle r="9" fill="#2c1a08"/><path d="M-80 -40 A90 90 0 0 1 -30 -84" fill="none" stroke="#fff" stroke-width="8" opacity=".8" stroke-linecap="round"/>'
    w += '</g>'
    b += w
    # chain from the watch bow to the frog's hands
    fx, fy, s = 330, 930, 2.7
    th = math.radians(14); u, v = 86, -62   # end of armL in frog space
    handx, handy = fx + s * (math.cos(th) * u - math.sin(th) * v), fy + s * (math.sin(th) * u + math.cos(th) * v)
    bowx, bowy = wx - 70, wy - 150
    ch = ''
    for i in range(22):
        t = i / 21
        px = (1 - t) ** 2 * bowx + 2 * (1 - t) * t * ((bowx + handx) / 2) + t * t * handx
        py = (1 - t) ** 2 * bowy + 2 * (1 - t) * t * ((bowy + handy) / 2 + 40) + t * t * handy
        ch += f'<ellipse cx="{px:.0f}" cy="{py:.0f}" rx="13" ry="8" transform="rotate({(i % 2) * 70 - 20} {px:.0f} {py:.0f})" fill="none" stroke="#3a2406" stroke-width="8"/>'
        ch += f'<ellipse cx="{px:.0f}" cy="{py:.0f}" rx="13" ry="8" transform="rotate({(i % 2) * 70 - 20} {px:.0f} {py:.0f})" fill="none" stroke="#f2c45a" stroke-width="4"/>'
    b += ch
    b += f'<circle cx="{fx + 40}" cy="{fy - 140}" r="210" fill="#9fd4ff" opacity=".12" filter="url(#b24)"/>'
    b += frog(fx, fy, s, rot=14, look=(5, -3), mouth='O', helmet=True,
              armL='M-34 -22 q-26 6 -34 30', armR='M38 -22 q30 -10 48 -40',
              legs=((-18, -6, -46, 18, 40), (20, -6, 10, 26, 20)))
    b += f'<circle cx="{handx:.0f}" cy="{handy:.0f}" r="12" fill="{GREEN}" stroke="{INK}" stroke-width="6"/>'
    b += spark(1080, 250, 20) + spark(1830, 180, 16) + spark(820, 860, 16) + spark(1240, 860, 12, '#ffe6c0', .7)
    b += '<rect width="1920" height="1080" fill="url(#vigC)"/>'
    lines = [('WHO STOLE', 170, 'w'), ('MY <span class="g">TIME?</span>', 210, 'w')]
    return page('#060a1c', svg(d, b), lines, outline='#05050e', top=50)


for n, fn in (('A', make_A), ('B', make_B), ('C', make_C)):
    open(os.path.join(HERE, f'{n}.html'), 'w').write(fn())
print('ok')
