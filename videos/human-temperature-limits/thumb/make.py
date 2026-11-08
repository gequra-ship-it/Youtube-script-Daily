# Thumbnails A-C for human-temperature-limits (guideline 16-6, brief tools/briefs/thumb_art.md). Run: python3 videos/human-temperature-limits/thumb/make.py
# A  NOT DEAD / UNTIL / WARM     homage: The Shining (1980) snowy hedge maze at night (high view into the lit maze, lodge on the horizon).
#                                Script: "a hypothermia patient is not dead until they are warm and dead" (famous saying of emergency medicine).
# B  ONLY A / 14° / WINDOW        intuitive: a glowing human in a narrow golden gap between a wall of ice and a wall of fire.
#                                Script: "A window of roughly fourteen degrees Celsius separates a living body from the edge of death" (28 -> 42).
# C  NEAR 42°C / PROTEINS / FAIL  intuitive: an egg turning white in a hot pan (script: denaturation = egg whites turning solid in a hot pan;
#                                "When your core approaches forty-two degrees, proteins and vital organs begin to fail").
# Frog: A scarf + beanie + lantern peeking over the hedge; B scarf, shivering on the ice side; C sweating with a paper fan on the pan rim.
import os, sys, math, random
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../tools'))
from thumb_lib import page, svg, lin, rad, spark

INK = '#1d2b1c'; GREEN = '#6aa55a'


def P(v):
    return ' '.join(f'{a:.1f},{b:.1f}' for a, b in v)


def mix(c1, c2, t):
    a = [int(c1[i:i + 2], 16) for i in (1, 3, 5)]; b = [int(c2[i:i + 2], 16) for i in (1, 3, 5)]
    return '#%02x%02x%02x' % tuple(int(a[k] + (b[k] - a[k]) * t) for k in range(3))


FILTERS = ''.join(f'<filter id="b{s}" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="{s}"/></filter>'
                  for s in (2, 4, 6, 10, 24, 50))


# ---------------- mascot frog (tools/assets/frog.svg body; outfits per scene) ----------------
def frog(x, y, s, mouth='o', look=(0, 0), la='q-14 6 -16 22', ra='q14 6 16 22', back='', front='', hands=True, flip=False, extra=''):
    sx = -s if flip else s
    g = f'<g transform="translate({x} {y}) scale({sx} {s})" stroke="{INK}" stroke-linejoin="round" stroke-linecap="round">' + back
    g += '<ellipse cx="-22" cy="4" rx="16" ry="9" fill="#4d8a4a" stroke-width="3.2"/><ellipse cx="22" cy="4" rx="16" ry="9" fill="#4d8a4a" stroke-width="3.2"/>'
    g += f'<path d="M-34 0 q-6 -64 34 -70 q40 -2 42 62 q0 10 -6 12 q-36 6 -70 -4z" fill="{GREEN}" stroke-width="4"/>'
    g += '<ellipse cx="2" cy="-12" rx="22" ry="20" fill="#9cc98a" stroke="none" opacity=".7"/>'
    g += '<path d="M-26 -50 q6 -16 22 -18" fill="none" stroke="#b9e0a6" stroke-width="3" opacity=".7"/>'
    dx, dy = look   # pupil r=5 inside white r=13.5: |look| <= 6 keeps it inside (tools/eyecheck.py)
    for ex in (-10, 22):
        g += f'<circle cx="{ex}" cy="-66" r="13.5" fill="#f4f5ea" stroke-width="3.2"/><circle cx="{ex + dx}" cy="{-66 + dy}" r="5" fill="{INK}" stroke="none"/>'
        g += f'<circle cx="{ex + dx + 1.6}" cy="{-66 + dy - 1.8}" r="1.6" fill="#fff" stroke="none"/>'
    g += '<ellipse cx="-18" cy="-46" rx="5" ry="3" fill="#e98a8a" stroke="none" opacity=".6"/><ellipse cx="30" cy="-46" rx="5" ry="3" fill="#e98a8a" stroke="none" opacity=".6"/>'
    if mouth == 'o':
        g += '<ellipse cx="6" cy="-42" rx="6.5" ry="8" fill="#7a2f33" stroke-width="3"/><ellipse cx="6" cy="-38" rx="3.5" ry="2.6" fill="#e07b7b" stroke="none"/>'
    elif mouth == 'chatter':
        g += '<rect x="-6" y="-48" width="24" height="10" rx="4" fill="#f4f5ea" stroke-width="3"/><path d="M0 -48 v10 M6 -48 v10 M12 -48 v10 M-6 -43 h24" stroke-width="1.6"/>'
    else:
        g += '<path d="M-8 -45 q14 14 28 0 q-14 4 -28 0z" fill="#7a2f33" stroke-width="3"/>'
    g += extra
    for st, path in (('M-34 -22', la), ('M38 -22', ra)):
        g += f'<path d="{st} {path}" fill="none" stroke-width="7.5"/><path d="{st} {path}" fill="none" stroke="{GREEN}" stroke-width="3.4"/>'
        if hands:
            sx0, sy0 = map(float, st[1:].split()); q = [float(v) for v in path[1:].split()]
            g += f'<circle cx="{sx0 + q[2]}" cy="{sy0 + q[3]}" r="5.5" fill="{GREEN}" stroke-width="3"/>'
    return g + front + '</g>'


def scarf(c1='#c8423a', c2='#f1e3c8'):
    g = f'<path d="M-30 -30 q34 14 70 -2 l2 10 q-38 16 -74 2z" fill="{c1}" stroke-width="3"/>'
    g += ''.join(f'<path d="M{-22 + k * 14} -26 l3 10" stroke="{c2}" stroke-width="4" fill="none"/>' for k in range(5))
    g += f'<path d="M24 -24 l6 34 l-12 2 l-4 -30z" fill="{c1}" stroke-width="3"/><path d="M19 4 l12 -2" stroke="{c2}" stroke-width="4"/>'
    return g


def beanie(c='#3f6fb0'):
    return (f'<path d="M-24 -78 q4 -32 34 -34 q32 0 36 32 q-34 -8 -70 2z" fill="{c}" stroke-width="3.2"/>'
            '<path d="M-26 -76 q36 -12 74 -2 l-1 9 q-36 -10 -72 2z" fill="#f1e3c8" stroke-width="3"/>'
            '<circle cx="10" cy="-114" r="8" fill="#f1e3c8" stroke-width="3"/>')


def snowflake(x, y, r, col='#e8f6ff', op=.8, w=3):
    g = f'<g transform="translate({x} {y})" stroke="{col}" stroke-width="{w}" stroke-linecap="round" opacity="{op}" fill="none">'
    for k in range(6):
        a = math.radians(k * 60); ex, ey = r * math.cos(a), r * math.sin(a)
        g += f'<path d="M0 0 L{ex:.1f} {ey:.1f}"/>'
        for f in (.55,):
            bx, by = ex * f, ey * f
            for d in (-35, 35):
                b = a + math.radians(180 + d); g += f'<path d="M{bx:.1f} {by:.1f} l{r * .3 * math.cos(b):.1f} {r * .3 * math.sin(b):.1f}"/>'
    return g + '</g>'


def snowfall(n, seed, ymax=1080, xmin=0):
    random.seed(seed); out = ''
    for _ in range(n):
        x, y = random.randint(xmin, 1920), random.randint(0, ymax); r = random.choice([1.6, 2.2, 3, 4, 5.5])
        out += f'<circle cx="{x}" cy="{y}" r="{r}" fill="#f2f8ff" opacity="{random.uniform(.35, .9):.2f}"{" filter=\"url(#b2)\"" if r > 4 else ""}/>'
    return out


# ====================================================================== A  The Shining homage: snowy hedge maze at night
def thumb_A():
    random.seed(7)
    C, R = 15, 14
    # maze (DFS)
    vis = [[False] * R for _ in range(C)]; hw = {(i, j) for i in range(C) for j in range(R + 1)}; vw = {(i, j) for i in range(C + 1) for j in range(R)}
    st = [(7, 0)]; vis[7][0] = True
    while st:
        i, j = st[-1]; nb = [(i + a, j + b) for a, b in ((1, 0), (-1, 0), (0, 1), (0, -1)) if 0 <= i + a < C and 0 <= j + b < R and not vis[i + a][j + b]]
        if not nb: st.pop(); continue
        ni, nj = random.choice(nb); vis[ni][nj] = True
        if ni != i: vw.discard((max(i, ni), j))
        else: hw.discard((i, max(j, nj)))
        st.append((ni, nj))
    hw.discard((7, 0))   # entrance
    # path entrance -> centre (BFS)
    goal = (8, 8); prev = {(7, 0): None}; q = [(7, 0)]
    while q:
        c = q.pop(0)
        if c == goal: break
        i, j = c
        for a, b in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            n = (i + a, j + b)
            if not (0 <= n[0] < C and 0 <= n[1] < R) or n in prev: continue
            if a == 1 and (i + 1, j) in vw or a == -1 and (i, j) in vw or b == 1 and (i, j + 1) in hw or b == -1 and (i, j) in hw: continue
            prev[n] = c; q.append(n)
    path = []; c = goal
    while c: path.append(c); c = prev[c]
    path.reverse()

    F, CX, HOR, CAMH = 600, 1290, 290, 5.2
    X0, Z0, Hh, T = -7.5, 5.0, 1.45, .34

    def pr(X, Y, Z):
        return (CX + F * X / Z, HOR + F * (CAMH - Y) / Z)

    fogc = '#6d86a8'

    def boxsvg(a, b, c, d, h):
        zc = (c + d) / 2; fog = min(1, max(0, (zc - 6) / 13)) ** 1.1 * .85
        top = mix('#e9f3ff', fogc, fog * .6); front = mix('#1f3b3c', fogc, fog); side = mix('#16292c', fogc, fog)
        g = ''
        if b < 0: g += f'<polygon points="{P([pr(b, 0, c), pr(b, 0, d), pr(b, h, d), pr(b, h, c)])}" fill="{side}"/>'
        elif a > 0: g += f'<polygon points="{P([pr(a, 0, c), pr(a, 0, d), pr(a, h, d), pr(a, h, c)])}" fill="{side}"/>'
        g += f'<polygon points="{P([pr(a, 0, c), pr(b, 0, c), pr(b, h, c), pr(a, h, c)])}" fill="{front}"/>'
        if zc < 12:   # leaf texture on near faces
            for _ in range(int(14 * (b - a) + 3)):
                u, v = random.random(), random.uniform(.12, .9)
                px, py = pr(a + (b - a) * u, h * v, c)
                rr = F * .05 / c
                g += f'<circle cx="{px:.1f}" cy="{py:.1f}" r="{rr * random.uniform(.6, 1.3):.1f}" fill="{random.choice(["#2e5650", "#132628", "#3b6a60"])}" opacity="{(1 - fog) * .8:.2f}"/>'
        g += f'<polygon points="{P([pr(a, h, c), pr(b, h, c), pr(b, h, d), pr(a, h, d)])}" fill="{top}"/>'
        # snow cap overhang along the front edge
        n = max(2, int((b - a) * 4))
        for k in range(n):
            px, py = pr(a + (b - a) * (k + .5) / n, h, c)
            rr = F * .07 / c
            g += f'<ellipse cx="{px:.1f}" cy="{py:.1f}" rx="{rr * 1.4:.1f}" ry="{rr * random.uniform(.7, 1.3):.1f}" fill="{top}"/>'
        return g

    items = []
    for (i, j) in hw:
        a, b, z = X0 + i - T / 2, X0 + i + 1 + T / 2, Z0 + j
        items.append((z, abs(X0 + i + .5), boxsvg(a, b, z - T / 2, z + T / 2, Hh)))
    for (i, j) in vw:
        x, c = X0 + i, Z0 + j
        items.append((c + .5, abs(x), boxsvg(x - T / 2, x + T / 2, c, c + 1, Hh)))

    # warm lamps on a few posts
    lamps = []
    for (i, j) in ((3, 4), (11, 3), (5, 10), (12, 9), (9, 6)):
        x, z = X0 + i, Z0 + j
        lx, ly = pr(x, Hh + .35, z); sc = F / z
        lamps.append((z, (lx, ly, sc)))
    for z, (lx, ly, sc) in lamps:
        g = (f'<line x1="{lx:.1f}" y1="{ly:.1f}" x2="{lx:.1f}" y2="{ly + sc * .35:.1f}" stroke="#0d1718" stroke-width="{max(2, sc * .05):.1f}"/>'
             f'<circle cx="{lx:.1f}" cy="{ly:.1f}" r="{sc * .5:.1f}" fill="url(#lampG)" style="mix-blend-mode:screen"/>'
             f'<circle cx="{lx:.1f}" cy="{ly:.1f}" r="{sc * .08:.1f}" fill="#fff4cf"/>')
        items.append((z - .01, 0, g))

    # frog peeking over the front hedge, scarf + beanie + lantern
    fx, fy, fs = 1120, 1060, 3.0
    lant = ('<g transform="translate(70 -44)"><path d="M0 -18 v-10" stroke-width="3" fill="none"/>'
            '<circle cx="0" cy="8" r="40" fill="url(#lanG)" stroke="none"/>'
            '<rect x="-11" y="-18" width="22" height="34" rx="5" fill="#ffd77a" stroke-width="3"/>'
            '<path d="M-11 -6 h22 M-11 6 h22 M0 -18 v34" stroke-width="2" fill="none" opacity=".6"/>'
            '<rect x="-14" y="-22" width="28" height="6" rx="2" fill="#3a2a1e" stroke-width="2.5"/><rect x="-14" y="16" width="28" height="6" rx="2" fill="#3a2a1e" stroke-width="2.5"/></g>')
    shiver = ''.join(f'<path d="M{-50 + k * 4} {-70 + k * 22} q-6 4 0 8 q6 4 0 8" fill="none" stroke="#e8f6ff" stroke-width="2.6" opacity=".9"/>' for k in range(2))
    frg = frog(0, 0, 1, mouth='o', look=(4, -2), la='q-14 6 -16 22', ra='q22 -4 32 -30', back=shiver,
               extra=scarf() + beanie(), front=lant)
    frg = (f'<g transform="translate({fx} {fy}) scale({fs})">{frg}</g>'
           f'<ellipse cx="{fx + 70 * fs}" cy="{fy - 40 * fs}" rx="230" ry="190" fill="url(#lanG2)" style="mix-blend-mode:screen"/>')
    items.append((1.0, 0, frg))

    items.sort(key=lambda t: (-t[0], -t[1]))
    gx0, gy0 = pr(X0 + goal[0] + .5, Hh, Z0 + goal[1] + .5)
    items.insert(len(items) - 1, (0, 0, f'<ellipse cx="{gx0:.0f}" cy="{gy0:.0f}" rx="260" ry="130" fill="url(#goalG)" opacity=".75" style="mix-blend-mode:screen"/>' + spark(gx0, gy0 - 30, 22)))

    # ground: snow plane with footprints + centre glow
    gq = [pr(X0 - 6, 0, Z0 - .3), pr(X0 + C + 6, 0, Z0 - .3), pr(X0 + C + 300, 0, Z0 + 400), pr(X0 - 300, 0, Z0 + 400)]
    ground = f'<polygon points="{P(gq)}" fill="url(#snowG)"/>'
    gx, gy = pr(X0 + goal[0] + .5, 0, Z0 + goal[1] + .5)
    ground += f'<ellipse cx="{gx:.0f}" cy="{gy:.0f}" rx="420" ry="170" fill="url(#goalG)" style="mix-blend-mode:screen"/>'
    fp = ''
    pts = [(X0 + i + .5, Z0 + j + .5) for i, j in path]
    k = 0
    for (x1, z1), (x2, z2) in zip(pts, pts[1:]):
        for t in (0, .33, .66):
            x, z = x1 + (x2 - x1) * t, z1 + (z2 - z1) * t
            off = .09 if k % 2 else -.09
            if x1 == x2: x += off
            else: z += off
            px, py = pr(x, 0, z); sc = F / z
            fp += f'<ellipse cx="{px:.1f}" cy="{py:.1f}" rx="{sc * .05:.1f}" ry="{sc * .025:.1f}" fill="#3d5a82" opacity=".75"/>'
            k += 1

    # sky, mountains, lodge
    sky = '<rect width="1920" height="1080" fill="url(#skyA)"/>'
    sky += '<ellipse cx="1500" cy="300" rx="700" ry="200" fill="url(#hazeA)"/>'
    mt = '<path d="M0 330 L160 250 L300 300 L470 210 L640 290 L820 230 L980 300 L1150 200 L1320 270 L1500 190 L1700 260 L1920 210 L1920 360 L0 360Z" fill="#253a5e"/>'
    mt += '<path d="M1150 200 L1190 228 L1172 230 L1206 250 L1130 236Z M1500 190 L1550 222 L1528 222 L1566 246 L1470 220Z M470 210 L505 236 L440 236Z" fill="#a9c2e0" opacity=".55"/>'
    mt += '<path d="M0 345 L250 300 L520 330 L760 296 L1000 330 L1300 300 L1600 318 L1920 296 L1920 380 L0 380Z" fill="#1a2b48"/>'
    lodge = '<g transform="translate(1290 268)"><rect x="0" y="0" width="420" height="44" fill="#0f1a2c"/><path d="M-20 0 L60 -26 L360 -26 L440 0Z" fill="#14223a"/><rect x="170" y="-48" width="80" height="26" fill="#0f1a2c"/>'
    for r in range(2):
        for c in range(14):
            if (r * 7 + c * 3) % 5:
                lodge += f'<rect x="{14 + c * 29}" y="{8 + r * 16}" width="12" height="8" fill="#ffcf7a" opacity="{.6 + .4 * ((c + r) % 2)}"/>'
    lodge += '</g><ellipse cx="1500" cy="290" rx="300" ry="60" fill="url(#lodgeG)" style="mix-blend-mode:screen"/>'

    defs = FILTERS + lin('skyA', [(0, '#060c1c'), (.55, '#16284a'), (1, '#3c5a86')]) \
        + rad('hazeA', 1500, 300, 700, [(0, '#8aa6cf', .45), (1, '#8aa6cf', 0)]) \
        + lin('snowG', [(0, '#3a5480'), (.3, '#5e7aa6'), (1, '#8ea8cc')]) \
        + rad('goalG', 0, 0, 1, [(0, '#ffd88a', .85), (.4, '#ffb85a', .35), (1, '#ff9a3a', 0)]).replace('gradientUnits="userSpaceOnUse"', '') \
        + rad('lampG', 0, 0, 1, [(0, '#ffe3a0', .9), (.3, '#ffbe62', .4), (1, '#ff9a3a', 0)]).replace('gradientUnits="userSpaceOnUse"', '') \
        + rad('lanG', 0, 8, 40, [(0, '#fff0b8', .95), (.5, '#ffc45e', .4), (1, '#ff9a3a', 0)]) \
        + rad('lanG2', 0, 0, 1, [(0, '#ffcf7a', .35), (1, '#ff9a3a', 0)]).replace('gradientUnits="userSpaceOnUse"', '') \
        + rad('lodgeG', 0, 0, 1, [(0, '#ffcf7a', .35), (1, '#ffcf7a', 0)]).replace('gradientUnits="userSpaceOnUse"', '') \
        + rad('vigA', 960, 520, 1150, [(0, '#000', 0), (.65, '#000', 0), (1, '#02040c', .75)])
    for gid in ('goalG', 'lampG', 'lanG2', 'lodgeG'):
        defs = defs.replace(f'<radialGradient id="{gid}" cx="0" cy="0" r="1" >', f'<radialGradient id="{gid}">')
    body = sky + mt + lodge + ground + fp + ''.join(t[2] for t in items)
    body += snowfall(260, 11) + '<rect width="1920" height="1080" fill="url(#vigA)"/>'
    body += '<rect x="1560" y="880" width="360" height="200" fill="#030612" opacity=".35" filter="url(#b50)"/>'
    body += '<ellipse cx="420" cy="260" rx="560" ry="300" fill="#040914" opacity=".45" filter="url(#b50)"/>'
    return page('#0b1426', svg(defs, body), [('NOT DEAD', 190, 'w'), ('UNTIL', 150, 'w'), ('WARM', 250, 'y')], top=44)


# ====================================================================== B  intuitive: human in a narrow golden gap between ice and fire
def thumb_B():
    random.seed(21)
    GL, GR = 1260, 1560   # gap
    bg = '<rect width="1920" height="1080" fill="#0a1020"/>'
    # cold side
    bg += f'<rect x="0" y="0" width="{GL + 40}" height="1080" fill="url(#iceBG)"/>'
    # hot side
    bg += f'<rect x="{GR - 40}" y="0" width="{1920 - GR + 40}" height="1080" fill="url(#fireBG)"/>'
    # golden window glow
    bg += f'<rect x="{GL - 80}" y="0" width="{GR - GL + 160}" height="1080" fill="url(#goldV)" filter="url(#b24)"/>'
    bg += f'<ellipse cx="{(GL + GR) / 2}" cy="560" rx="320" ry="520" fill="url(#goldR)"/>'
    # ice wall: jagged faceted edge
    ice = ''
    y = -20; pts = [(0, -20)]
    while y < 1100:
        pts.append((GL + random.randint(-50, 10), y)); y += random.randint(50, 110)
    pts += [(GL - 10, 1100), (0, 1100)]
    ice += f'<polygon points="{P(pts)}" fill="url(#iceW)"/>'
    # facets
    for k in range(len(pts) - 3):
        x1, y1 = pts[k + 1]; x2, y2 = pts[k + 2]
        d = random.randint(140, 320)
        ice += f'<polygon points="{P([(x1, y1), (x2, y2), (x2 - d, (y1 + y2) / 2 + random.randint(-40, 40))])}" fill="{random.choice(["#bfe8ff", "#7fc4ec", "#5aa3d6", "#d9f4ff"])}" opacity="{random.uniform(.25, .6):.2f}"/>'
        ice += f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#effbff" stroke-width="4" opacity=".9"/>'
    # cracks and frost inside ice
    for _ in range(9):
        x, yy = random.randint(700, GL - 60), random.randint(500, 1050)
        ice += f'<path d="M{x} {yy} l{random.randint(-80, -20)} {random.randint(-60, 60)} l{random.randint(-70, -20)} {random.randint(-50, 50)}" stroke="#e8f8ff" stroke-width="2.5" fill="none" opacity=".5"/>'
    # icicles from the top of the ice side
    for x in range(560, GL + 20, 46):
        L = random.randint(60, 200) * (1 if x > 800 else .6)
        ice += f'<path d="M{x - 16} 0 L{x + 16} 0 L{x + random.randint(-4, 4)} {L:.0f}Z" fill="#cfefff" opacity=".85"/><path d="M{x - 6} 0 L{x} {L * .8:.0f}" stroke="#fff" stroke-width="3" opacity=".7"/>'
    # frost crystals reaching into the gap
    for (x, yy, r) in ((GL + 8, 330, 26), (GL - 20, 720, 34), (GL + 2, 920, 22), (GL - 30, 170, 20), (1050, 840, 40), (920, 640, 28)):
        ice += snowflake(x, yy, r, '#f4fcff', .9, 3.5)
    # fire side: flame tongues reaching in from the right
    fire = ''
    for k in range(16):
        yy = -40 + k * 74 + random.randint(-15, 15)
        L = random.randint(150, 280)
        x0 = GR + random.randint(0, 50)
        fire += (f'<path d="M1960 {yy + 70} C{x0 + 120} {yy + 90} {x0 - 20} {yy + 50} {x0 - L * .25:.0f} {yy - 20} '
                 f'C{x0 + 70} {yy + 6} {x0 + 140} {yy - 10} 1960 {yy - 40}Z" fill="url(#flameG)" opacity=".95"/>')
    for k in range(14):
        yy = -10 + k * 82 + random.randint(-10, 10); x0 = GR + 40 + random.randint(0, 60)
        fire += (f'<path d="M1960 {yy + 40} C{x0 + 90} {yy + 50} {x0 + 10} {yy + 20} {x0 - 30} {yy - 20} C{x0 + 60} {yy} {x0 + 110} {yy - 6} 1960 {yy - 20}Z" '
                 f'fill="url(#flameY)" opacity=".9"/>')
    for _ in range(60):
        x, yy = random.randint(GR - 60, 1900), random.randint(0, 1050)
        fire += f'<circle cx="{x}" cy="{yy}" r="{random.choice([2, 3, 4])}" fill="#ffd27a" opacity="{random.uniform(.5, 1):.2f}"/>'
    # glass tube outline of the window (thermometer feel) + ticks
    cx = (GL + GR) / 2
    tube = f'<rect x="{cx - 125}" y="70" width="250" height="840" rx="125" fill="#fff6d8" fill-opacity=".07" stroke="#fff3c8" stroke-width="5" opacity=".85"/>'
    tube += f'<path d="M{cx - 92} 170 L{cx - 92} 800" stroke="#fff" stroke-width="10" stroke-linecap="round" opacity=".25"/>'
    for k in range(15):
        yy = 150 + k * 50; w = 34 if k % 7 == 0 else 18
        tube += f'<line x1="{cx + 125 - w}" y1="{yy}" x2="{cx + 125}" y2="{yy}" stroke="#fff3c8" stroke-width="4" opacity=".75"/>'
    # human silhouette, glowing gold with a furnace core
    hx, foot = cx, 900
    hum = (f'<g transform="translate({hx} {foot})">'
           '<circle cx="0" cy="-640" r="60" fill="url(#humG)" stroke="#fff1c0" stroke-width="7"/>'
           '<path d="M-78 -560 Q0 -585 78 -560 Q100 -548 100 -510 L104 -330 Q104 -312 88 -312 Q74 -312 72 -330 L66 -470 L62 -260 L54 -10 Q52 10 30 10 Q10 10 10 -12 L4 -250 L-4 -250 L-10 -12 Q-10 10 -30 10 Q-52 10 -54 -10 L-62 -260 L-66 -470 L-72 -330 Q-74 -312 -88 -312 Q-104 -312 -104 -330 L-100 -510 Q-100 -548 -78 -560Z" fill="url(#humG)" stroke="#fff1c0" stroke-width="7"/>'
           '<ellipse cx="0" cy="-440" rx="54" ry="70" fill="url(#coreG)"/>'
           '<path d="M-60 -540 Q0 -560 60 -540" stroke="#ffe9b0" stroke-width="6" fill="none" opacity=".7"/>'
           '</g>')
    humglow = f'<ellipse cx="{hx}" cy="{foot - 330}" rx="150" ry="400" fill="#fffbe8" opacity=".9" filter="url(#b24)"/>' + f'<ellipse cx="{hx}" cy="{foot - 330}" rx="190" ry="440" fill="#ffd77a" opacity=".45" filter="url(#b50)"/>'
    floor = f'<ellipse cx="{hx}" cy="{foot + 14}" rx="150" ry="22" fill="#fff0c0" opacity=".55" filter="url(#b10)"/>'
    # frog on the ice side: scarf + beanie, chattering, shiver lines
    shiver = ''.join(f'<path d="M{-56 - k * 8} {-80 + k * 26} q-7 4 0 8 q7 4 0 8" fill="none" stroke="#e8f6ff" stroke-width="2.8"/>' for k in range(3))
    frost = '<path d="M-26 -50 q-6 -10 2 -16 M44 -30 q8 -4 4 -14" stroke="#e8f6ff" stroke-width="3" fill="none"/>'
    fr = frog(1060, 1010, 2.7, mouth='chatter', look=(5, -2), la='q-8 -2 -2 14', ra='q-10 4 -30 8', back=shiver, extra=scarf('#2f6fb3', '#f1e3c8') + beanie('#c8423a') + frost)
    ledge = '<path d="M820 1010 Q1060 980 1240 1012 L1260 1080 L800 1080Z" fill="#d6f0ff"/><path d="M820 1010 Q1060 980 1240 1012" stroke="#fff" stroke-width="5" fill="none"/>'
    defs = FILTERS + lin('iceBG', [(0, '#06101f'), (.6, '#0d2a4c'), (1, '#2a6fa8')], 1, 0) \
        + lin('fireBG', [(0, '#ff8a2a'), (.35, '#b8261a'), (1, '#2a0606')], 1, 0) \
        + lin('iceW', [(0, '#0b2240'), (.7, '#2c6fa6'), (1, '#9fd8ff')], 1, 0) \
        + lin('goldV', [(0, '#ffcf6a'), (.5, '#fff6d8'), (1, '#ffcf6a')], 1, 0) \
        + rad('goldR', cx, 560, 520, [(0, '#fff3c8', .55), (1, '#ffcf6a', 0)]) \
        + lin('flameG', [(0, '#fff0a0'), (.25, '#ffb43a'), (.7, '#e8401c'), (1, '#7a0f0a')], 1, 0) \
        + lin('flameY', [(0, '#fffbe0'), (.4, '#ffd25a'), (1, '#ff7a2a')], 1, 0) \
        + rad('humG', 0, -360, 520, [(0, '#c4561c', 1), (.6, '#8a2e12', 1), (1, '#5a1a0a', 1)]) \
        + rad('coreG', 0, -440, 70, [(0, '#ffffff', 1), (.5, '#ff9a3a', .8), (1, '#ff6a2a', 0)]) \
        + rad('vigB', 1100, 540, 1150, [(0, '#000', 0), (.7, '#000', 0), (1, '#000', .7)])
    body = bg + fire + ice + humglow + tube + floor + hum + ledge + fr
    for _ in range(40):
        body += f'<circle cx="{random.randint(40, GL - 40)}" cy="{random.randint(20, 1060)}" r="{random.choice([2, 3, 4])}" fill="#eaf8ff" opacity="{random.uniform(.3, .8):.2f}"/>'
    body += spark(cx + 150, 200, 22) + spark(cx - 170, 640, 16) + spark(cx + 160, 780, 14)
    body += '<rect width="1920" height="1080" fill="url(#vigB)"/>'
    body += '<rect x="1600" y="890" width="320" height="190" fill="#120202" opacity=".55" filter="url(#b50)"/>'
    body += '<ellipse cx="380" cy="300" rx="480" ry="300" fill="#030812" opacity=".5" filter="url(#b50)"/>'
    return page('#0a1020', svg(defs, body), [('ONLY A', 170, 'w'), ('14°', 330, 'y'), ('WINDOW', 180, 'w')], top=40)


# ====================================================================== C  intuitive: an egg turning white in a hot pan
def thumb_C():
    random.seed(33)
    PX, PY, RX, RY = 1230, 720, 500, 270
    bg = '<rect width="1920" height="1080" fill="url(#bgC)"/>'
    bg += f'<ellipse cx="{PX}" cy="{PY + 40}" rx="800" ry="520" fill="url(#heatC)"/>'
    # flames under the pan (behind it), peeking out at the front edge
    fl = ''
    for k in range(26):
        a = math.radians(200 + k * (140 / 25)); x = PX + (RX * .92) * math.cos(a) * -1
        a2 = math.pi * (k / 25); x = PX - RX * .95 * math.cos(a2); yb = PY + RY * .9 * math.sin(a2) + 40
        h = random.randint(70, 150) * (1 - .4 * abs(math.cos(a2)))
        fl += (f'<path d="M{x - 26:.0f} {yb:.0f} C{x - 30:.0f} {yb - h * .5:.0f} {x + 6:.0f} {yb - h * .6:.0f} {x + random.randint(-8, 8):.0f} {yb - h:.0f} '
               f'C{x + 14:.0f} {yb - h * .55:.0f} {x + 30:.0f} {yb - h * .4:.0f} {x + 26:.0f} {yb:.0f}Z" fill="url(#flC)"/>')
    flglow = f'<ellipse cx="{PX}" cy="{PY + RY + 10}" rx="{RX + 60}" ry="90" fill="#ff7a2a" opacity=".55" filter="url(#b24)"/>'
    # pan
    pan = f'<path d="M{PX + RX - 60} {PY - RY + 80} L1890 300 Q1915 300 1912 330 L1902 350 Q1895 365 1870 362 L{PX + RX - 10} {PY - RY + 150}Z" fill="#1a1616" stroke="#0a0808" stroke-width="4"/>'
    pan += '<path d="M1700 360 L1880 316" stroke="#5a4a44" stroke-width="5" opacity=".7"/>'
    pan += f'<ellipse cx="{PX}" cy="{PY + 26}" rx="{RX}" ry="{RY}" fill="#120e0e"/>'
    pan += f'<ellipse cx="{PX}" cy="{PY}" rx="{RX}" ry="{RY}" fill="url(#rimC)" stroke="#0a0606" stroke-width="5"/>'
    pan += f'<ellipse cx="{PX}" cy="{PY + 8}" rx="{RX - 34}" ry="{RY - 24}" fill="url(#panIn)"/>'
    pan += f'<path d="M{PX - RX + 20} {PY + 30} A{RX - 20} {RY - 14} 0 0 0 {PX + RX - 20} {PY + 30}" fill="none" stroke="#ff9a4a" stroke-width="6" opacity=".55"/>'
    pan += f'<path d="M{PX - RX + 60} {PY - 100} A{RX - 30} {RY - 20} 0 0 1 {PX - 80} {PY - RY + 10}" fill="none" stroke="#c9b6aa" stroke-width="5" opacity=".45"/>'
    # oil sheen + bubbles
    pan += f'<ellipse cx="{PX - 20}" cy="{PY + 10}" rx="{RX - 90}" ry="{RY - 70}" fill="#ffb45a" opacity=".08"/>'
    for _ in range(40):
        a = random.random() * 2 * math.pi; rr = random.uniform(.55, .85)
        x, yy = PX + (RX - 60) * rr * math.cos(a), PY + 8 + (RY - 40) * rr * math.sin(a)
        pan += f'<circle cx="{x:.0f}" cy="{yy:.0f}" r="{random.choice([3, 4, 6, 8])}" fill="none" stroke="#ffd9a0" stroke-width="2" opacity=".55"/>'
    # egg: cooked white rim (opaque), clear centre ring turning, glowing yolk
    random.seed(4)
    ex, ey = PX - 30, PY + 4
    def blob(rx, ry, jit):
        pts = []
        for k in range(18):
            a = 2 * math.pi * k / 18; r = 1 + random.uniform(-jit, jit)
            pts.append((ex + rx * r * math.cos(a), ey + ry * r * math.sin(a)))
        d = f'M{pts[0][0]:.0f} {pts[0][1]:.0f} '
        for k in range(18):
            p1, p2 = pts[k], pts[(k + 1) % 18]
            d += f'Q{p1[0]:.0f} {p1[1]:.0f} {(p1[0] + p2[0]) / 2:.0f} {(p1[1] + p2[1]) / 2:.0f} '
        return d + 'Z'
    egg = f'<path d="{blob(330, 175, .12)}" fill="#c48a5a" opacity=".55" transform="translate(0 12)" filter="url(#b6)"/>'
    egg += f'<path d="{blob(330, 175, .12)}" fill="url(#whiteC)" stroke="#e8c79a" stroke-width="4"/>'
    egg += f'<path d="{blob(205, 115, .08)}" fill="#f6f0e2" opacity=".55"/>'
    egg += f'<path d="{blob(150, 85, .06)}" fill="#e9e2cf" opacity=".5"/>'
    # browned lacy edge
    for _ in range(30):
        a = random.random() * 2 * math.pi
        egg += f'<circle cx="{ex + 320 * math.cos(a):.0f}" cy="{ey + 168 * math.sin(a):.0f}" r="{random.choice([4, 6, 8])}" fill="#d9a066" opacity=".6"/>'
    yx, yy0 = ex + 20, ey - 20
    egg += f'<ellipse cx="{yx}" cy="{yy0}" rx="140" ry="110" fill="#ffb02e" opacity=".55" filter="url(#b24)"/>'
    egg += f'<ellipse cx="{yx}" cy="{yy0 + 14}" rx="98" ry="74" fill="#c86a10" opacity=".5"/>'
    egg += f'<ellipse cx="{yx}" cy="{yy0}" rx="96" ry="76" fill="url(#yolkC)" stroke="#d27a12" stroke-width="4"/>'
    egg += f'<ellipse cx="{yx - 34}" cy="{yy0 - 30}" rx="30" ry="16" fill="#fff8dc" opacity=".85" transform="rotate(-20 {yx - 34} {yy0 - 30})"/>'
    egg += f'<circle cx="{yx + 30}" cy="{yy0 - 40}" r="6" fill="#fff" opacity=".8"/>'
    # steam & heat shimmer
    st = ''
    for k, x in enumerate((960, 1100, 1250, 1400, 1520)):
        st += (f'<path d="M{x} {560 - k % 2 * 20} c-40 -60 40 -100 0 -160 c-40 -60 40 -100 0 -170" fill="none" stroke="#fff" stroke-width="{26 - k % 2 * 8}" '
               f'stroke-linecap="round" opacity=".16" filter="url(#b10)"/>')
    for _ in range(46):
        x, yy = random.randint(760, 1860), random.randint(140, 980)
        st += f'<circle cx="{x}" cy="{yy}" r="{random.choice([2, 3, 4, 5])}" fill="#ffcf6a" opacity="{random.uniform(.4, .95):.2f}"/>'
    st += spark(1010, 300, 20) + spark(1640, 620, 16) + spark(880, 980, 14, '#ffd27a')
    # frog on the pan rim, sweating, fanning
    fan = ('<g transform="translate(-74 -76) rotate(-25)"><path d="M0 0 L-36 -60 A70 70 0 0 1 36 -60Z" fill="#f1e3c8" stroke-width="3"/>'
           + ''.join(f'<path d="M0 0 L{70 * math.sin(math.radians(a)):.1f} {-70 * math.cos(math.radians(a)):.1f}" stroke-width="1.8" fill="none" opacity=".7"/>' for a in range(-30, 31, 10))
           + '<path d="M-30 -54 A62 62 0 0 1 30 -54" fill="none" stroke="#c8423a" stroke-width="5"/><path d="M0 0 v18" stroke-width="5" stroke="#8a5a3a"/></g>')
    sweat = ''.join(f'<path d="M{x} {y} q-6 10 0 14 q6 -4 0 -14z" fill="#bfe6ff" stroke-width="2.2"/>' for x, y in ((-34, -88), (48, -84), (52, -56), (-40, -60)))
    band = '<path d="M-22 -82 q32 -16 64 0" fill="none" stroke="#f1e3c8" stroke-width="8"/><path d="M-22 -82 q32 -16 64 0" fill="none" stroke="#c8423a" stroke-width="4"/>'
    fr = frog(1610, 500, 2.5, mouth='o', look=(-5, 2), la='q-20 -10 -36 -42', ra='q14 6 16 22', front=fan + sweat, extra=band, flip=False)
    defs = FILTERS + lin('bgC', [(0, '#1a0805'), (.6, '#3a1208'), (1, '#120404')]) \
        + rad('heatC', PX, PY + 40, 800, [(0, '#ff8a2a', .55), (.45, '#c23a12', .25), (1, '#5a1206', 0)]) \
        + lin('flC', [(0, '#fff6c0'), (.35, '#ffb43a'), (1, '#e0401a')], 0, 1).replace('x2="0" y2="1"', 'x1="0" y1="1" x2="0" y2="0"') \
        + lin('rimC', [(0, '#5a4a46'), (.45, '#2a2220'), (1, '#120c0c')]) \
        + rad('panIn', PX, PY, RX, [(0, '#3a2a24', 1), (.8, '#1e1412', 1), (1, '#0e0808', 1)]) \
        + rad('whiteC', ex, ey, 340, [(0, '#fffdf6', 1), (.75, '#fbf5e8', 1), (1, '#efd6ae', 1)]) \
        + rad('yolkC', yx - 20, yy0 - 20, 110, [(0, '#fff2a0', 1), (.5, '#ffc22e', 1), (1, '#f08a12', 1)]) \
        + rad('vigC', 1100, 560, 1150, [(0, '#000', 0), (.65, '#000', 0), (1, '#000', .75)])
    # flC gradient goes bottom -> top
    defs = defs.replace('<linearGradient id="flC" x1="0" y1="0" x1="0" y1="1" x2="0" y2="0">', '<linearGradient id="flC" x1="0" y1="1" x2="0" y2="0">')
    body = bg + flglow + fl + pan + egg + st + fr
    body += '<rect width="1920" height="1080" fill="url(#vigC)"/>'
    body += '<rect x="1600" y="890" width="320" height="190" fill="#0a0202" opacity=".55" filter="url(#b50)"/>'
    body += '<ellipse cx="400" cy="280" rx="520" ry="300" fill="#080202" opacity=".5" filter="url(#b50)"/>'
    return page('#1a0805', svg(defs, body), [('NEAR 42°C', 180, 'y'), ('PROTEINS', 170, 'w'), ('FAIL', 210, 'w')], top=40, outline='#140404')


if __name__ == '__main__':
    for n, f in (('A', thumb_A), ('B', thumb_B), ('C', thumb_C)):
        open(os.path.join(HERE, f'{n}.html'), 'w', encoding='utf-8').write(f())
    print('ok')
