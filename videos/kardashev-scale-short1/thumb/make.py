# Shorts thumbnail A for kardashev-scale-short1 (guideline 16-9: VERTICAL 1080x1920, text centred). Run: python3 make.py
# ENERGY IS / THE RULER   intuitive: night-side Earth (top) laced with a glowing power web between cities across continents;
#                         a giant wall light switch (bottom) whose glowing cable runs up the side into Earth; the frog in an
#                         electrician hard hat flips the switch. Text sits centred in the dark space between.
#                         (script: "light switch on your wall ... invisible web stretching across entire continents",
#                          "energy gives us a ruler that works anywhere")
# Helpers (frog, starfield, nebula...) are reused from the long-form thumbnail make.py (not copied).
import os, sys, math, random
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
sys.path.insert(0, os.path.join(REPO, 'tools'))
LONG = os.path.join(REPO, 'videos', 'kardashev-scale', 'thumb', 'make.py')
G = {'__file__': LONG}; exec(open(LONG).read().split('\nfor n, fn in')[0], G)
frog, starfield, nebula, FILTERS, P, INK = G['frog'], G['starfield'], G['nebula'], G['FILTERS'], G['P'], G['INK']
from thumb_lib import vpage, vsvg, lin, rad, spark


def blob(rnd, cx, cy, r, n=14, j=.35):
    pts = []
    for k in range(n):
        a = 2 * math.pi * k / n; rr = r * (1 + rnd.uniform(-j, j))
        pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a) * .8))
    d = f'M{(pts[0][0] + pts[-1][0]) / 2:.0f} {(pts[0][1] + pts[-1][1]) / 2:.0f}'
    for k in range(n):
        p, q = pts[k], pts[(k + 1) % n]
        d += f' Q{p[0]:.0f} {p[1]:.0f} {(p[0] + q[0]) / 2:.0f} {(p[1] + q[1]) / 2:.0f}'
    return d + 'Z'


def hardhat():
    return ('<path d="M-36 -84 q2 -46 42 -48 q40 2 44 48z" fill="#f2c230" stroke-width="4"/>'
            '<path d="M-2 -130 q4 20 2 46 M14 -130 q-2 20 0 46" fill="none" stroke="#c99a1c" stroke-width="5"/>'
            '<path d="M-24 -100 q8 -22 26 -26" fill="none" stroke="#fff3c0" stroke-width="4" opacity=".8"/>'
            '<path d="M-50 -82 q56 -14 108 0 q-2 8 -6 8 q-48 -10 -96 0 q-6 0 -6 -8z" fill="#e0ad1c" stroke-width="3.6"/>')


def bez(p0, c1, c2, p3, t):
    return tuple((1 - t) ** 3 * p0[i] + 3 * (1 - t) ** 2 * t * c1[i] + 3 * (1 - t) * t * t * c2[i] + t ** 3 * p3[i] for i in (0, 1))


def make():
    rnd = random.Random(5); ex, ey, er = 560, 450, 330
    d = FILTERS
    d += lin('sky', [(0, '#060a22'), (.55, '#0c0a2c'), (1, '#170a26')], 0, 1)
    d += '<radialGradient id="eN" cx=".38" cy=".4" r=".75"><stop offset="0" stop-color="#14305e"/><stop offset=".65" stop-color="#0a1a3c"/><stop offset="1" stop-color="#040a1c"/></radialGradient>'
    d += f'<clipPath id="ec"><circle cx="{ex}" cy="{ey}" r="{er}"/></clipPath>'
    d += rad('sun', 1060, 120, 560, [(0, '#fff6dc', 1), (.12, '#ffe2a0', .8), (.4, '#ffaa55', .25), (1, '#ff7a3a', 0)])
    d += rad('plateG', 0, 0, 260, [(0, '#fffaf0', 1), (.6, '#efe3c8', 1), (1, '#bfae8a', 1)])
    d += rad('glowS', 430, 1440, 520, [(0, '#ffe7a8', .5), (.5, '#ffb455', .16), (1, '#ff8a3a', 0)])
    d += rad('txtBg', 540, 930, 560, [(0, '#03050f', .55), (.6, '#03050f', .3), (1, '#03050f', 0)])
    d += rad('vig', 540, 960, 1150, [(0, '#000', 0), (.7, '#000', 0), (1, '#000', .55)])
    d += lin('cab', [(0, '#ffd27a'), (1, '#8fe8ff')], 0, 1)
    b = '<rect width="1080" height="1920" fill="url(#sky)"/>'
    b += nebula(rnd, 14, (0, 0, 1080, 1920), ['#3a2a8a', '#1a4a9a', '#7a2a6a'], 160, 360)
    b += starfield(rnd, 520, (0, 0, 1080, 1920), skip=lambda x, y: math.hypot(x - ex, y - ey) < er + 10)
    b += '<rect width="1080" height="1920" fill="url(#sun)"/>'
    # ---- Earth, night side, with a glowing power web ----
    b += f'<circle cx="{ex}" cy="{ey}" r="{er + 40}" fill="#5fb8ff" opacity=".25" filter="url(#b24)"/>'
    b += f'<circle cx="{ex}" cy="{ey}" r="{er + 12}" fill="#5fb8ff" opacity=".45" filter="url(#b12)"/>'
    b += f'<circle cx="{ex}" cy="{ey}" r="{er}" fill="url(#eN)"/>'
    g = '<g clip-path="url(#ec)">'
    k_ = er / 380
    conts = [(1190, 290, 170), (1430, 270, 150), (1570, 420, 110), (1250, 600, 120), (1510, 650, 90), (1080, 470, 70)]
    cities = []
    for cx_, cy_, r_ in conts:
        cx_, cy_, r_ = ex + (cx_ - 1370) * k_, ey + (cy_ - 455) * k_, r_ * k_
        g += f'<path d="{blob(rnd, cx_, cy_, r_, 22, .3)}" fill="#173c3c" stroke="#3f7a78" stroke-width="2.4"/>'
        g += f'<path d="{blob(rnd, cx_ - 10, cy_ - 8, r_ * .55, 16, .4)}" fill="#1f4a44" opacity=".75"/>'
        for _ in range(11):
            a = rnd.uniform(0, 6.283); dd = r_ * .7 * math.sqrt(rnd.random())
            x, y = cx_ + dd * math.cos(a), cy_ + dd * math.sin(a) * .8
            if math.hypot(x - ex, y - ey) < er - 22: cities.append((x, y))
    for (x, y) in cities:
        g += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{rnd.uniform(13, 24):.0f}" fill="#ffc86a" opacity=".4" filter="url(#b6)"/>'
        for _ in range(6):
            g += f'<circle cx="{x + rnd.uniform(-13, 13):.0f}" cy="{y + rnd.uniform(-9, 9):.0f}" r="{rnd.uniform(1.4, 3):.1f}" fill="#ffe7a8" opacity=".95"/>'
    web = ''; hubs = cities[::4]
    pairs = [(c, q) for c in cities for q in sorted(cities, key=lambda q: math.hypot(q[0] - c[0], q[1] - c[1]))[1:2]]
    pairs += [(hubs[i], hubs[j]) for i in range(len(hubs)) for j in range(i + 1, len(hubs)) if 140 < math.hypot(hubs[i][0] - hubs[j][0], hubs[i][1] - hubs[j][1]) < 290]
    for (x, y), (x2, y2) in pairs:
        mx, my = (x + x2) / 2, (y + y2) / 2 - math.hypot(x2 - x, y2 - y) * .22
        web += f'M{x:.0f} {y:.0f} Q{mx:.0f} {my:.0f} {x2:.0f} {y2:.0f} '
    g += f'<path d="{web}" fill="none" stroke="#ffd27a" stroke-width="10" opacity=".35" filter="url(#b3)"/>'
    g += f'<path d="{web}" fill="none" stroke="#fff0c0" stroke-width="2.6" opacity=".9"/>'
    for _ in range(24):
        x, y = rnd.choice(cities)
        g += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="5" fill="#fff" opacity=".9"/>'
    g += f'<circle cx="{ex + 460}" cy="{ey - 200}" r="{er + 140}" fill="#6fc0ff" opacity=".18" filter="url(#b50)"/>'
    g += f'<circle cx="{ex - 240}" cy="{ey + 180}" r="{er * 1.05}" fill="#000" opacity=".35" filter="url(#b50)"/>'
    g += '</g>'
    b += g
    b += f'<path d="M{ex + 30} {ey - er + 2} A{er - 2} {er - 2} 0 0 1 {ex + 290} {ey + 160}" fill="none" stroke="#fff3c8" stroke-width="12" opacity=".75" filter="url(#b6)"/>'
    b += f'<path d="M{ex + 30} {ey - er + 2} A{er - 2} {er - 2} 0 0 1 {ex + 290} {ey + 160}" fill="none" stroke="#ffffff" stroke-width="4"/>'
    b += f'<path d="M{ex - 290} {ey - 160} A{er} {er} 0 0 1 {ex - 50} {ey - er + 4}" fill="none" stroke="#7fd0ff" stroke-width="5" opacity=".7"/>'
    for (sx, sy, a) in ((150, 230, -20), (960, 560, 25), (180, 690, 10)):
        b += (f'<g transform="translate({sx} {sy}) rotate({a}) scale(1.2)"><rect x="-44" y="-9" width="30" height="18" fill="#2a4a9a" stroke="#0a0818" stroke-width="2"/>'
              f'<rect x="14" y="-9" width="30" height="18" fill="#2a4a9a" stroke="#0a0818" stroke-width="2"/><rect x="-12" y="-12" width="24" height="24" rx="4" fill="#d8dce8" stroke="#0a0818" stroke-width="2.4"/>'
              f'<circle cx="0" cy="0" r="22" fill="#8fe8ff" opacity=".25" filter="url(#b3)"/></g>')
    b += '<path d="M960 560 L840 520" stroke="#8fe8ff" stroke-width="3" stroke-dasharray="10 12" opacity=".8"/>'
    b += '<path d="M180 690 L290 610" stroke="#8fe8ff" stroke-width="3" stroke-dasharray="10 12" opacity=".8"/>'
    # ---- the giant light switch (bottom) and its cable up the right side into Earth ----
    px, py = 390, 1420
    plug = (ex + er * math.cos(math.radians(52)), ey + er * math.sin(math.radians(52)))
    c0, c1, c2, c3 = (px + 150, py - 120), (1010, py - 160), (1060, 980), plug
    cable = f'M{c0[0]} {c0[1]} C{c1[0]} {c1[1]} {c2[0]} {c2[1]} {c3[0]:.0f} {c3[1]:.0f}'
    b += '<rect width="1080" height="1920" fill="url(#txtBg)"/>'
    b += f'<path d="{cable}" fill="none" stroke="#000" stroke-width="40" opacity=".35" filter="url(#b6)"/>'
    b += f'<path d="{cable}" fill="none" stroke="#0e0c18" stroke-width="34"/>'
    b += f'<path d="{cable}" fill="none" stroke="#4a4668" stroke-width="26"/>'
    b += f'<path d="{cable}" fill="none" stroke="#d0d4f4" stroke-width="6" transform="translate(-6 -4)" opacity=".9"/>'
    b += f'<path d="{cable}" fill="none" stroke="url(#cab)" stroke-width="12" opacity=".6" filter="url(#b6)"/>'
    for t in (.12, .3, .5, .7, .88):
        x, y = bez(c0, c1, c2, c3, t)
        b += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="24" fill="#ffe7a8" opacity=".55" filter="url(#b6)"/><circle cx="{x:.0f}" cy="{y:.0f}" r="9" fill="#fff"/>'
    b += f'<circle cx="{plug[0]:.0f}" cy="{plug[1]:.0f}" r="44" fill="#bff4ff" opacity=".6" filter="url(#b12)"/>'
    for k in range(8):
        a = rnd.uniform(-2.6, -.2); L = rnd.uniform(30, 70)
        b += f'<path d="M{plug[0]:.0f} {plug[1]:.0f} l{L * math.cos(a + 2.2):.0f} {L * math.sin(a + 2.2):.0f}" stroke="#fff6c8" stroke-width="3" stroke-linecap="round"/>'
    b += '<rect width="1080" height="1920" fill="url(#glowS)"/>'
    w, h = 270, 390
    sw = f'<g transform="translate({px} {py}) rotate(-7) scale(1.28)">'
    sw += f'<rect x="{-w / 2 + 14}" y="{-h / 2 + 18}" width="{w}" height="{h}" rx="34" fill="#000" opacity=".45" filter="url(#b12)"/>'
    sw += f'<rect x="{-w / 2}" y="{-h / 2}" width="{w}" height="{h}" rx="34" fill="#a8977a" stroke="{INK}" stroke-width="6"/>'
    sw += f'<rect x="{-w / 2 + 10}" y="{-h / 2 + 8}" width="{w - 20}" height="{h - 22}" rx="28" fill="url(#plateG)"/>'
    sw += f'<path d="M{-w / 2 + 30} {-h / 2 + 22} q60 -6 120 -4" stroke="#fff" stroke-width="8" opacity=".8" stroke-linecap="round" fill="none"/>'
    for sy in (-h / 2 + 40, h / 2 - 40):
        sw += f'<circle cx="0" cy="{sy}" r="15" fill="#d9ccb0" stroke="#6a5c44" stroke-width="3"/><path d="M-9 {sy} H9" stroke="#6a5c44" stroke-width="4"/>'
    sw += '<rect x="-52" y="-112" width="104" height="224" rx="14" fill="#5a4c38" stroke="#2a2218" stroke-width="4"/>'
    sw += '<rect x="-44" y="-104" width="88" height="208" rx="10" fill="#e8dcc0"/><rect x="-60" y="-120" width="120" height="240" rx="18" fill="#ffe7a8" opacity=".35" filter="url(#b6)"/>'
    sw += '<path d="M-40 6 L-34 -96 Q0 -112 34 -96 L40 6 Z" fill="#fffaf0" stroke="#6a5c44" stroke-width="4"/>'   # toggle UP (on)
    sw += '<path d="M-28 -84 Q0 -98 28 -84" stroke="#fff" stroke-width="6" fill="none" opacity=".9"/>'
    sw += '<path d="M-40 6 L40 6 L44 30 L-44 30Z" fill="#b8a888" stroke="#6a5c44" stroke-width="3"/>'
    sw += '</g>'
    b += f'<circle cx="{px}" cy="{py}" r="360" fill="#ffd98a" opacity=".2" filter="url(#b50)"/>' + sw
    # frog in a hard hat beside the switch, one hand on the toggle
    b += frog(700, 1660, 2.7, rot=-4, look=(-7, -5), mouth='O', armL='M-34 -22 q-34 -22 -58 -74', armR='M38 -22 q26 -12 32 -40',
              legs=((-20, -6, -26, 2, -6), (20, -6, 26, 2, 6)), brows=True, shadow=True, front=hardhat())
    b += spark(880, 140, 20) + spark(120, 470, 16) + spark(960, 1260, 14) + spark(130, 1100, 14) + spark(990, 1780, 16)
    b += '<rect width="1080" height="1920" fill="url(#vig)"/>'
    lines = [('ENERGY IS', 128, 'w'), ('THE <span class="g">RULER</span>', 166, 'w')]
    return vpage('#060a22', vsvg(d, b), lines, outline='#050717', top=830)


open(os.path.join(HERE, 'A.html'), 'w').write(make())
print('ok')
