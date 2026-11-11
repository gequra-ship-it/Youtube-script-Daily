# Thumbnails A-C for everest-tallest-mountain (guideline 16-6 / 16-8, brief tools/briefs/thumb_art.md). Run: python3 videos/everest-tallest-mountain/thumb/make.py
# A  ONLY FROM / SEA LEVEL   (declarative)  homage (photo): the 1953 first-ascent summit photo (climber on the top of Everest raising an ice axe
#    hung with a string of flags; no person, the frog takes the pose). Snow plume, sea of clouds, distant Himalaya. Script S01/S05/S08/S23:
#    "Measure from sea level, and Everest wins", "8,848 meters above sea level", "Define height by sea level, and Everest is the champion."
# B  TALLER / THAN / EVEREST?  (question)  intuitive: "an iceberg of stone": Mauna Kea in an ocean cut-away, small sunset summit with observatory
#    domes above the waves, a huge basalt body below, a glowing measuring tape from seafloor to peak; diver frog on the seafloor looking up.
#    Script S15-S16: "measured from the seafloor, it rises roughly 10,210 meters, well over a thousand meters taller than Everest"; observatories S12.
# C  21-22 KM / ON MARS   (number)  intuitive: Olympus Mons, a broad shield volcano with caldera and basal cliff, a small snowy Everest at its foot
#    for scale, astronaut frog in the foreground. Script S30: "towers approximately twenty-one to twenty-two kilometers ... about two and a half
#    times the height of Everest"; S32 shield volcano, gentle slope; S28 red deserts of Mars.
import os, sys, math, random
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', '..', 'tools'))
from thumb_lib import page, svg, lin, rad, spark

INK = '#1d2b1c'; GREEN = '#6aa55a'; DARKG = '#4d8a4a'; BELLY = '#9cc98a'
FILTERS = ''.join(f'<filter id="b{n}" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="{n}"/></filter>' for n in (2, 4, 8, 14, 26, 50, 90))


def P(pts):
    return ' '.join(f'{a:.1f},{b:.1f}' for a, b in pts)


def limb(d, w=7.5, wi=3.4, col=GREEN):
    return f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="{w}"/><path d="{d}" fill="none" stroke="{col}" stroke-width="{wi}"/>'


def end_of(d):
    n = [float(v) for v in d.replace('M', ' ').replace('q', ' ').split()]
    return n[0] + n[-2], n[1] + n[-1]


def frog(x, y, s, rot=0, flip=False, look=(0, 0), mouth='O', armL=None, armR=None, brows=True, back='', front='', mid='', top='', sleeve=GREEN):
    sx = -s if flip else s
    g = [f'<g transform="translate({x} {y}) rotate({rot}) scale({sx} {s})" stroke="{INK}" stroke-linejoin="round" stroke-linecap="round">', back]
    for fx, fy in ((-22, 4), (22, 4)):
        g.append(f'<ellipse cx="{fx}" cy="{fy}" rx="16" ry="9" fill="{DARKG}" stroke-width="3.2"/>')
    g.append(f'<path d="M-34 0 q-6 -64 34 -70 q40 -2 42 62 q0 10 -6 12 q-36 6 -70 -4z" fill="{GREEN}" stroke-width="4"/>')
    g.append(f'<ellipse cx="2" cy="-12" rx="22" ry="20" fill="{BELLY}" stroke="none" opacity=".7"/>')
    g.append('<path d="M-24 -50 q6 -14 18 -16" fill="none" stroke="#b6dea0" stroke-width="3" opacity=".8"/>')
    g.append(mid)
    lx, ly = look
    _d = math.hypot(1 + lx, ly)
    if _d > 6.9: _k = 6.9 / _d; lx, ly = (1 + lx) * _k - 1, ly * _k
    for ex in (-10, 22):
        g.append(f'<circle cx="{ex}" cy="-66" r="13.5" fill="#f4f5ea" stroke-width="3.2"/>')
        g.append(f'<circle cx="{ex + 1 + lx:.2f}" cy="{-66 + ly:.2f}" r="4.4" fill="{INK}" stroke="none"/>')
        g.append(f'<circle cx="{ex + 2.4 + lx:.2f}" cy="{-67.6 + ly:.2f}" r="1.5" fill="#fff" stroke="none"/>')
    if brows:
        g.append('<path d="M-22 -88 q12 -9 24 -1 M10 -89 q12 -8 24 1" fill="none" stroke-width="3.4"/>')
    if mouth == 'O':
        g.append('<ellipse cx="6" cy="-38" rx="10" ry="12" fill="#7a2f33" stroke-width="3"/><ellipse cx="6" cy="-31" rx="6" ry="4" fill="#e07b7b" stroke="none"/>')
    else:
        g.append('<ellipse cx="6" cy="-41" rx="6" ry="7.5" fill="#7a2f33" stroke-width="3"/>')
    g.append('<ellipse cx="-18" cy="-48" rx="5" ry="3" fill="#e98a8a" stroke="none" opacity=".55"/><ellipse cx="30" cy="-48" rx="5" ry="3" fill="#e98a8a" stroke="none" opacity=".55"/>')
    g.append(top)
    for a in (armL or 'M-34 -22 q-14 6 -16 22', armR or 'M38 -22 q14 6 16 22'):
        g.append(limb(a, col=sleeve)); ex_, ey_ = end_of(a)
        g.append(f'<circle cx="{ex_:.1f}" cy="{ey_:.1f}" r="5.6" fill="{GREEN}" stroke-width="3"/>')
    g.append(front); g.append('</g>')
    return ''.join(g)


def jag(p0, p1, n, amp, seed):
    """jagged polyline from p0 to p1 (n segments, perpendicular noise amp)"""
    r = random.Random(seed); pts = [p0]
    dx, dy = p1[0] - p0[0], p1[1] - p0[1]; L = math.hypot(dx, dy); nx, ny = -dy / L, dx / L
    for i in range(1, n):
        t = i / n; a = r.uniform(-amp, amp) * math.sin(math.pi * t) ** .5
        pts.append((p0[0] + dx * t + nx * a, p0[1] + dy * t + ny * a))
    return pts + [p1]


def sparkles(lst, col='#fff6d6'):
    return ''.join(spark(x, y, s, col) for x, y, s in lst)


# ====================================================================== A  (1953 summit photo homage)
def range_peaks(seed, y0, ymin, ymax, col, colL, n=7, x0=-40, x1=1960):
    r = random.Random(seed); out = ''
    xs = sorted(r.uniform(x0, x1) for _ in range(n))
    for x in xs:
        h = r.uniform(ymin, ymax); wl, wr = r.uniform(140, 260), r.uniform(140, 260)
        L = jag((x - wl, y0), (x, h), 6, 14, r.random()); R = jag((x, h), (x + wr, y0), 6, 14, r.random())
        out += f'<polygon points="{P(L + R[1:])}" fill="{col}"/>'
        out += f'<polygon points="{P(R + [(x + wr * .2, y0), (x + 6, h + 30)])}" fill="{colL}"/>'
    return out


def cloudbank(seed, n, x0, x1, y0, y1, col, o0, o1, rx0, rx1):
    r = random.Random(seed)
    return ''.join(f'<ellipse cx="{r.uniform(x0, x1):.0f}" cy="{r.uniform(y0, y1):.0f}" rx="{r.uniform(rx0, rx1):.0f}" ry="{r.uniform(rx0, rx1) * .32:.0f}" fill="{col}" opacity="{r.uniform(o0, o1):.2f}"/>' for _ in range(n))


def thumb_A():
    random.seed(1)
    defs = FILTERS
    defs += lin('skyA', [(0, '#06102e'), (.35, '#14347a'), (.7, '#3f7fc8'), (1, '#a9d4f2')])
    defs += rad('sunA', 1640, 250, 520, [(0, '#ffffff', 1), (.06, '#fff8e0', .95), (.16, '#ffeec0', .45), (.4, '#d8ecff', .18), (1, '#d8ecff', 0)])
    defs += rad('vigA', 960, 560, 1150, [(0, '#000', 0), (.72, '#000', 0), (1, '#000', .5)])
    defs += lin('snowL', [(0, '#ffffff'), (1, '#dbe9f7')])
    defs += lin('snowS', [(0, '#8fa9d6'), (1, '#5e78ad')])
    defs += lin('rockS', [(0, '#2a2f4a'), (1, '#15182a')])
    defs += lin('cloudA', [(0, '#f4f9ff'), (1, '#b9cde8')])
    defs += rad('summitGlow', 1190, 470, 420, [(0, '#fff3c8', .75), (.4, '#ffe2a0', .22), (1, '#ffe2a0', 0)])
    b = '<rect width="1920" height="1080" fill="url(#skyA)"/>'
    b += ''.join(f'<circle cx="{random.randint(20, 1200)}" cy="{random.randint(10, 260)}" r="{random.choice([1.2, 1.8])}" fill="#dfe9ff" opacity="{random.uniform(.2, .6):.2f}"/>' for _ in range(60))
    b += '<rect width="1920" height="1080" fill="url(#sunA)"/>'
    # distant Himalaya above the sea of clouds
    b += range_peaks(5, 820, 600, 700, '#6f8fbf', '#a9c3e6', 9)
    b += range_peaks(9, 860, 660, 760, '#56739f', '#d6e6f6', 8)
    b += cloudbank(3, 40, -100, 2000, 780, 900, '#e9f2fc', .5, .9, 90, 220)
    b += '<rect x="0" y="860" width="1920" height="220" fill="url(#cloudA)"/>'
    b += cloudbank(4, 46, -100, 2000, 840, 1080, '#ffffff', .4, .85, 120, 260)
    # ---- the summit pyramid ----
    peak = (1190, 470)
    L = jag((330, 1110), peak, 14, 30, 11)
    R = jag(peak, (2000, 1110), 14, 26, 12)
    sil = L + R[1:]
    ridge = jag(peak, (1290, 1110), 10, 34, 13)   # dividing ridge: left = shadow, right = sunlit
    defs += f'<clipPath id="mA"><polygon points="{P(sil)}"/></clipPath>'
    b += '<g transform="translate(170 90)">'
    b += '<rect x="-400" y="-200" width="2600" height="1500" fill="url(#summitGlow)"/>'
    g = f'<polygon points="{P(sil)}" fill="url(#rockS)"/>'
    g += f'<g clip-path="url(#mA)">'
    g += f'<polygon points="{P(R + ridge[::-1])}" fill="#4a4762"/>'
    # rock bands (the summit limestone)
    for k, yy in enumerate((690, 760, 840, 930)):
        g += f'<path d="M500 {yy} Q 900 {yy - 60} 1300 {yy - 10} T 1700 {yy + 20}" fill="none" stroke="#b9a37f" stroke-width="{10 - k}" opacity=".35"/>'
    # snow: shadow-side snow everywhere above snowline, sunlit snow on the right face
    snow = jag((470, 880), (1720, 840), 22, 34, 14)
    snowpoly = [(400, 300), (1800, 300)] + snow[::-1]
    g += f'<polygon points="{P(snowpoly)}" fill="url(#snowS)"/>'
    g += f'<clipPath id="litA"><polygon points="{P(R + ridge[::-1])}"/></clipPath>'
    g += f'<polygon points="{P(snowpoly)}" fill="url(#snowL)" clip-path="url(#litA)"/>'
    # snow tongues down the gullies + dark rock ribs
    r = random.Random(21)
    for _ in range(14):
        x = r.uniform(620, 1600); y = r.uniform(850, 900); h = r.uniform(30, 80)
        g += f'<path d="M{x:.0f} {y:.0f} q{r.uniform(-12, 12):.0f} {h / 2:.0f} {r.uniform(-30, 30):.0f} {h:.0f} q14 -{h / 2:.0f} 18 -{h:.0f}z" fill="{"#dfeaf7" if x > 1200 else "#7f97c4"}" opacity=".9"/>'
    for _ in range(12):
        x = r.uniform(700, 1500); y = r.uniform(560, 760)
        g += f'<path d="M{x:.0f} {y:.0f} l{r.uniform(-20, 20):.0f} {r.uniform(40, 90):.0f}" stroke="#2b2c44" stroke-width="{r.uniform(4, 9):.0f}" opacity=".45" stroke-linecap="round"/>'
    for k in range(9):
        x = 700 + k * 120 + r.uniform(-20, 20); y = 540 + abs(x - 1190) * .62 + r.uniform(0, 30); w = r.uniform(40, 70); h = r.uniform(220, 360)
        col = '#34324e' if x < 1250 else '#5f5878'
        g += f'<path d="M{x - w * .45:.0f} {y + 6:.0f} L{x:.0f} {y:.0f} L{x + w * .5:.0f} {y + h * .45:.0f} L{x + w * .8:.0f} {y + h:.0f} L{x - w:.0f} {y + h * .95:.0f} L{x - w * .35:.0f} {y + h * .5:.0f}Z" fill="{col}" opacity=".55"/>'
        g += f'<path d="M{x:.0f} {y:.0f} L{x + w * .5:.0f} {y + h * .45:.0f} L{x + w * .8:.0f} {y + h:.0f}" fill="none" stroke="#fff2d0" stroke-width="3" opacity="{.7 if x > 1250 else .25}"/>'
    g += '<path d="M700 660 Q 1190 600 1700 640 L1700 680 Q 1190 640 700 705Z" fill="#d9b46a" opacity=".42"/>'
    g += '<path d="M700 660 Q 1190 600 1700 640" fill="none" stroke="#fff0c0" stroke-width="3" opacity=".6"/>'
    # ridge highlight (sun rim)
    g += f'<polyline points="{P(R[:5])}" fill="none" stroke="#fff6dc" stroke-width="7" opacity=".9"/>'
    g += f'<polyline points="{P(ridge[:6])}" fill="none" stroke="#ffffff" stroke-width="4" opacity=".55"/>'
    g += '</g>'
    b += g
    b += f'<polyline points="{P(L[-4:] + R[1:4])}" fill="none" stroke="#fff8e4" stroke-width="5" opacity=".8" filter="url(#b2)"/>'
    # summit cornice + footprints climbing the left ridge
    b += f'<path d="M1096 492 q94 -46 196 0 q-98 12 -196 0z" fill="#ffffff"/><path d="M1110 488 q80 -36 168 -2" fill="none" stroke="#fff3cf" stroke-width="4"/>'
    fp = jag((780, 900), (1130, 500), 11, 6, 30)
    b += ''.join(f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{7 - i * .3:.1f}" ry="{3.4 - i * .15:.1f}" fill="#4a5f8f" opacity=".75"/>' for i, (x, y) in enumerate(fp[1:-1]))
    # the famous snow plume streaming off the summit
    for k, (dy, w, o) in enumerate(((-30, 90, .55), (10, 60, .5), (-70, 50, .35), (40, 40, .3))):
        b += f'<path d="M1200 {470 + dy * .3} C 1400 {440 + dy}, 1650 {420 + dy}, 1980 {380 + dy * 1.6}" fill="none" stroke="#ffffff" stroke-width="{w}" opacity="{min(.9, o * 1.5):.2f}" stroke-linecap="round" filter="url(#b26)"/>'
    b += cloudbank(7, 30, 1260, 1980, 360, 470, '#ffffff', .12, .3, 30, 80)
    b += '</g>'
    # foreground clouds hugging the base (keeps the bottom-right corner plain)
    b += cloudbank(8, 26, 300, 2000, 1010, 1130, '#f7fbff', .6, .95, 120, 260)
    # ---- the frog in the summit pose: arm raised, ice axe hung with a string of flags ----
    tank = '<rect x="-58" y="-60" width="24" height="54" rx="10" fill="#e8b23e" stroke-width="3.2"/><rect x="-53" y="-54" width="5" height="40" rx="2" fill="#fff3c4" stroke="none" opacity=".7"/><path d="M-46 -60 q-4 -24 18 -26" fill="none" stroke="#6b6f78" stroke-width="5"/>'
    jacket = ('<path d="M-36 -2 q-6 -30 4 -44 q34 -10 68 -2 q10 14 6 46 q-40 8 -78 0z" fill="#ef7d2a" stroke-width="3.6"/>'
              '<path d="M-34 -16 q36 8 72 0 M-36 -30 q38 8 74 0" fill="none" stroke="#b9531a" stroke-width="2.6"/>'
              '<path d="M-28 -42 q10 -4 18 -2" fill="none" stroke="#ffc58c" stroke-width="3" opacity=".9"/>'
              '<path d="M4 -46 l0 44" fill="none" stroke="#b9531a" stroke-width="2.4"/>'
              '<path d="M-22 -86 q28 -40 56 0 q-28 8 -56 0z" fill="#c6303a" stroke-width="3.2"/><path d="M-24 -84 q30 8 60 0" fill="none" stroke="#f2d27a" stroke-width="5"/>'
              '<circle cx="6" cy="-112" r="8" fill="#f7f2e6" stroke-width="3"/>')
    flags = ''
    fl = [(88, -170), (120, -176), (152, -172), (184, -162), (214, -152)]
    cols = ['#3d7be0', '#f7f2e6', '#d8463f', '#5fb05a', '#f2d27a']
    flags += f'<path d="M70 -170 Q 150 -186 226 -146" fill="none" stroke="{INK}" stroke-width="2.4"/>'
    for (fx, fy), c in zip(fl, cols):
        flags += f'<path d="M{fx - 14} {fy} L{fx + 14} {fy - 2} L{fx + 6} {fy + 30} Z" fill="{c}" stroke-width="2.6"/>'
    axe = ('<path d="M58 -30 L72 -176" fill="none" stroke-width="9"/><path d="M58 -30 L72 -176" fill="none" stroke="#b78a4f" stroke-width="5"/>'
           '<path d="M46 -172 q26 -12 48 6 l-2 6 q-20 -10 -44 -2z" fill="#c9ced6" stroke-width="3.2"/>' + flags)
    b += ('<g><path d="M1236 640 L1316 584" stroke="#071233" stroke-width="9" stroke-linecap="round"/><path d="M1236 640 L1316 584" stroke="#f2d27a" stroke-width="4" stroke-linecap="round"/>'
          '<rect x="930" y="610" width="330" height="112" rx="26" fill="#0b1a45" stroke="#f2d27a" stroke-width="5" opacity=".96"/>'
          '<text x="1095" y="666" text-anchor="middle" font-family="Fredoka" font-weight="700" font-size="58" fill="#ffffff">EVEREST</text>'
          '<text x="1095" y="705" text-anchor="middle" font-family="Fredoka" font-weight="700" font-size="34" fill="#f2d27a">8,848 m</text></g>')
    b += '<ellipse cx="1366" cy="566" rx="80" ry="10" fill="#5d78ad" opacity=".5"/>'
    b += frog(1360, 562, 2.6, look=(3, -4), mouth='O', back=tank, mid=jacket, armR='M38 -26 q24 -24 22 -70', sleeve='#ef7d2a', front=axe)
    b += '<path d="M1236 572 q124 -40 250 0 q-125 16 -250 0z" fill="#ffffff"/><path d="M1250 568 q110 -30 222 -2" fill="none" stroke="#fff1c8" stroke-width="4"/>'
    b += sparkles([(1560, 500, 22), (1190, 470, 16), (1660, 660, 14), (1080, 760, 12), (1720, 360, 18)])
    b += '<rect width="1920" height="1080" fill="url(#vigA)"/>'
    lines = [('EVEREST', 160, 'w'), ("ISN'T THE", 130, 'w'), ('TALLEST?', 200, 'y')]
    return page('#14347a', svg(defs, b), lines, outline='#071233')


# ====================================================================== B  (Mauna Kea: an iceberg of stone)
def thumb_B():
    random.seed(2)
    W = 470          # waterline
    defs = FILTERS
    defs += lin('skyB', [(0, '#1b1846'), (.45, '#5b2f6a'), (.8, '#e0705a'), (1, '#ffc27a')])
    defs += lin('seaB', [(0, '#1d8aa8'), (.25, '#0f5577'), (.6, '#08304d'), (1, '#020c18')])
    defs += rad('sunB', 1730, W, 380, [(0, '#fff4c8', 1), (.12, '#ffd38a', .8), (.4, '#ff9a62', .3), (1, '#ff9a62', 0)])
    defs += lin('islandB', [(0, '#a8553a'), (1, '#5a2a24')])
    defs += lin('basaltB', [(0, '#1f4e64'), (.5, '#14334a'), (1, '#0a1a28')])
    defs += lin('rayB', [(0, '#bff4ff'), (1, '#bff4ff')], 0, 1)
    defs += rad('vigB', 960, 560, 1150, [(0, '#000', 0), (.7, '#000', 0), (1, '#000', .55)])
    defs += rad('coreB', 1250, 900, 420, [(0, '#ff8a3c', .45), (.5, '#ff5a2a', .12), (1, '#ff5a2a', 0)])
    b = '<rect width="1920" height="1080" fill="url(#seaB)"/>'
    b += f'<rect width="1920" height="{W}" fill="url(#skyB)"/>'
    b += ''.join(f'<circle cx="{random.randint(20, 1900)}" cy="{random.randint(10, 200)}" r="{random.choice([1.2, 1.8, 2.4])}" fill="#ffe9f0" opacity="{random.uniform(.2, .7):.2f}"/>' for _ in range(50))
    b += f'<rect width="1920" height="{W}" fill="url(#sunB)"/>'
    b += cloudbank(31, 16, 1000, 1950, 330, 430, '#ffb48a', .25, .5, 60, 160)
    # light rays into the water
    for x, w, o in ((300, 120, .10), (620, 80, .08), (1500, 140, .09), (1800, 90, .07), (980, 70, .06)):
        b += f'<path d="M{x} {W} L{x + w} {W} L{x + w * 2.2 - 160} 1080 L{x - 260} 1080Z" fill="#bff4ff" opacity="{o}" filter="url(#b14)"/>'
    # mountain profile: broad shield from the seafloor to a small summit above the waves
    prof = []
    for i in range(0, 61):
        t = i / 60; x = 520 + t * 1480
        # shield: summit near x=1250
        u = (x - 1250) / (730 if x < 1250 else 760)
        y = 1060 - 875 * math.exp(-(abs(u) ** 1.55) * 2.3)
        prof.append((x, y))
    r = random.Random(4)
    prof = [(x, y + (r.uniform(-7, 7) if 0 < i < 60 else 0)) for i, (x, y) in enumerate(prof)]
    sil = prof + [(2000, 1100), (520, 1100)]
    defs += f'<clipPath id="mB"><polygon points="{P(sil)}"/></clipPath>'
    b += f'<polygon points="{P(sil)}" fill="url(#basaltB)"/>'
    g = '<g clip-path="url(#mB)">'
    # stacked lava layers ("layer after layer")
    for k in range(1, 15):
        off = k * 58
        pts = [(x, y + off + 10 * math.sin(x / 90 + k)) for x, y in prof[::2]]
        g += f'<polyline points="{P(pts)}" fill="none" stroke="#5aa4c2" stroke-width="3" opacity="{.28 - k * .012:.2f}"/>'
    g += '<rect width="1920" height="1080" fill="url(#coreB)"/>'
    # hotspot conduit glow
    g += '<path d="M1250 1100 C 1240 980 1262 860 1250 700" fill="none" stroke="#ff7a3a" stroke-width="22" opacity=".35" filter="url(#b14)"/>'
    g += '<path d="M1250 1100 C 1240 980 1262 860 1250 700" fill="none" stroke="#ffc07a" stroke-width="5" opacity=".55"/>'
    # above-water part: red cinder with lit right side
    g += f'<rect x="0" y="0" width="1920" height="{W}" fill="url(#islandB)"/>'
    g += f'<path d="M1250 140 L2000 {W} L1250 {W}Z" fill="#d97650" opacity=".55"/>'
    g += ''.join(f'<ellipse cx="{r.uniform(900, 1700):.0f}" cy="{r.uniform(250, W - 10):.0f}" rx="{r.uniform(10, 30):.0f}" ry="{r.uniform(4, 9):.0f}" fill="#3e1c1a" opacity=".35"/>' for _ in range(24))
    g += f'<rect x="0" y="{W - 40}" width="1920" height="40" fill="#3f6d3a" opacity=".55"/>'  # green coastal fringe
    # water tint over the underwater body + darkening with depth
    g += f'<rect x="0" y="{W}" width="1920" height="{1080 - W}" fill="#0b6a8c" opacity=".18"/>'
    g += '</g>'
    b += g
    # rim light: warm above water, cyan below
    above = [(x, y) for x, y in prof if y <= W + 2]
    b += f'<polyline points="{P(above)}" fill="none" stroke="#ffe0a8" stroke-width="6" opacity=".9"/>'
    b += f'<polyline points="{P(prof)}" fill="none" stroke="#7fe8ff" stroke-width="14" opacity=".35" filter="url(#b8)"/>'
    b += f'<polyline points="{P([p for p in prof if p[1] > W])}" fill="none" stroke="#a8f2ff" stroke-width="3.5" opacity=".75"/>'
    # observatory domes on the summit
    top_y = min(y for x, y in prof)
    for dx, s in ((-70, 1.0), (-18, 1.25), (40, .9), (92, .8)):
        X = 1250 + dx; Y = [yy for xx, yy in prof if abs(xx - X) < 13][0] + 6
        b += f'<g transform="translate({X} {Y}) scale({s})" stroke="#2a1a1c" stroke-width="2.4"><rect x="-12" y="-14" width="24" height="14" fill="#e9e6ee"/><path d="M-14 -14 a14 14 0 0 1 28 0z" fill="#ffffff"/><path d="M-2 -27 l4 0 l0 12 l-4 0z" fill="#3a3046" stroke="none"/></g>'
    b += f'<ellipse cx="1250" cy="{top_y + 10}" rx="160" ry="60" fill="#fff0c8" opacity=".35" filter="url(#b26)"/>'
    # sea surface line + small waves
    b += f'<rect x="0" y="{W - 3}" width="1920" height="6" fill="#e9fbff" opacity=".85"/>'
    b += ''.join(f'<path d="M{x} {W - 2} q14 -10 28 0" fill="none" stroke="#ffffff" stroke-width="3" opacity=".8"/>' for x in range(30, 1900, 74))
    b += f'<rect x="0" y="{W + 3}" width="1920" height="28" fill="#bff4ff" opacity=".12"/>'
    # base-to-peak measuring tape (the ruler)
    tx, y0, y1 = 1250, 1052, top_y - 4
    b += f'<rect x="{tx - 16}" y="{y1}" width="32" height="{y0 - y1}" fill="#f2d27a" opacity=".35" filter="url(#b14)"/>'
    b += f'<rect x="{tx - 10}" y="{y1}" width="20" height="{y0 - y1}" rx="4" fill="#f2d27a" stroke="#6b4a10" stroke-width="2.5"/>'
    b += ''.join(f'<path d="M{tx - 10} {yy:.0f} l{12 if k % 5 else 20} 0" stroke="#6b4a10" stroke-width="{2 if k % 5 else 3.4}"/>' for k, yy in enumerate(range(int(y0), int(y1), -18)))
    b += f'<path d="M{tx - 26} {y0} l52 0 M{tx - 26} {y1} l52 0" stroke="#fff4c8" stroke-width="6" stroke-linecap="round"/>'
    # seafloor, rocks, sediment
    b += '<path d="M0 1000 C 300 990 450 1040 700 1050 L1920 1060 L1920 1080 L0 1080Z" fill="#06121d"/>'
    b += ''.join(f'<ellipse cx="{r.uniform(0, 700):.0f}" cy="{r.uniform(1010, 1075):.0f}" rx="{r.uniform(14, 46):.0f}" ry="{r.uniform(6, 14):.0f}" fill="#1b3442" opacity=".8"/>' for _ in range(16))
    # sea life: a fish school near the surface, a glowing jelly, a small crab
    for k in range(18):
        fx, fy = 1500 + r.uniform(-160, 220), 590 + r.uniform(-50, 70)
        b += f'<path d="M{fx:.0f} {fy:.0f} q12 -7 24 0 q-12 7 -24 0z M{fx + 24:.0f} {fy:.0f} l8 -6 l0 12z" fill="#bfe8f5" opacity=".75"/>'
    b += '<g transform="translate(700 690)"><ellipse cx="0" cy="0" rx="34" ry="24" fill="#c9a6ff" opacity=".25" filter="url(#b8)"/><path d="M-26 6 q26 -50 52 0z" fill="#d9c2ff" opacity=".8"/>' + ''.join(f'<path d="M{x} 6 q6 30 -2 62" fill="none" stroke="#e6d6ff" stroke-width="2.4" opacity=".7"/>' for x in (-18, -6, 6, 18)) + '</g>'
    b += '<g transform="translate(160 1030)" stroke="#3a1208" stroke-width="2.4"><ellipse cx="0" cy="0" rx="22" ry="13" fill="#e2643a"/><path d="M-20 -4 l-14 -12 M20 -4 l14 -12 M-16 8 l-12 8 M16 8 l12 8" fill="none"/></g>'
    b += sparkles([(1420, 210, 20), (1080, 300, 14), (1590, 300, 16), (980, 760, 14), (1450, 820, 12)])
    # ---- diver frog on the seafloor looking up the stone wall ----
    tank = '<rect x="-56" y="-62" width="22" height="52" rx="10" fill="#e3ab3e" stroke-width="3.2"/><path d="M-46 -62 q-6 -34 22 -38" fill="none" stroke="#6b6f78" stroke-width="5"/>'
    helmet = ('<circle cx="6" cy="-60" r="44" fill="#bfe6ff" fill-opacity=".14" stroke="#d6a94f" stroke-width="4.5"/>'
              '<path d="M-26 -84 A36 36 0 0 1 6 -98" fill="none" stroke="#fff" stroke-width="5" opacity=".75"/>'
              '<ellipse cx="5" cy="-17" rx="40" ry="9" fill="#c48d38" stroke-width="3.2"/>'
              + ''.join(f'<circle cx="{c}" cy="-16" r="2.4" fill="#ffe7a6" stroke="none"/>' for c in (-24, -9, 6, 21, 34)))
    torch = '<g transform="translate(66 -66) rotate(-62)"><rect x="-6" y="-9" width="40" height="18" rx="5" fill="#8a929e" stroke-width="3"/><ellipse cx="38" cy="0" rx="3" ry="11" fill="#fff6c8" stroke="none"/></g>'
    b += '<path d="M560 840 L1010 480 L1110 610 Z" fill="#fff2c2" opacity=".18" filter="url(#b14)"/>'
    b += frog(470, 1040, 2.9, look=(4, -5), mouth='O', back=tank, top=helmet, armR='M38 -22 q22 -10 28 -44', front=torch)
    b += ''.join(f'<circle cx="{510 + k * 6}" cy="{720 - k * 60}" r="{6 + k * 2}" fill="none" stroke="#dff6ff" stroke-width="2.5" opacity=".7"/>' for k in range(4))
    b += '<rect width="1920" height="1080" fill="url(#vigB)"/>'
    lines = [('TALLER', 168, 'w'), ('THAN', 108, 'w'), ('EVEREST?', 200, 'y')]
    return page('#1b1846', svg(defs, b), lines, outline='#0b0a24')


# ====================================================================== C  (Olympus Mons on Mars)
def thumb_C():
    random.seed(3)
    G = 880          # ground / base line
    defs = FILTERS
    defs += lin('skyC', [(0, '#0d0a1e'), (.45, '#3b2340'), (.8, '#a8604a'), (1, '#e6a36c')])
    defs += rad('sunC', 1700, 170, 360, [(0, '#ffffff', 1), (.07, '#eaf4ff', .95), (.25, '#9fc6ff', .35), (1, '#9fc6ff', 0)])
    defs += lin('olyS', [(0, '#8a3f2c'), (1, '#4a1f1a')])
    defs += lin('olyL', [(0, '#f0a06a'), (1, '#b65a36')], 1, 0)
    defs += lin('groundC', [(0, '#a8522e'), (1, '#3a160f')])
    defs += rad('vigC', 960, 560, 1150, [(0, '#000', 0), (.7, '#000', 0), (1, '#000', .55)])
    defs += rad('olyGlow', 1330, 400, 560, [(0, '#ffd2a0', .55), (.45, '#ff9a62', .16), (1, '#ff9a62', 0)])
    b = '<rect width="1920" height="1080" fill="url(#skyC)"/>'
    b += ''.join(f'<circle cx="{random.randint(20, 1900)}" cy="{random.randint(10, 420)}" r="{random.choice([1.2, 1.8, 2.4])}" fill="#f2ecff" opacity="{random.uniform(.2, .75):.2f}"/>' for _ in range(110))
    b += '<rect width="1920" height="1080" fill="url(#sunC)"/>'
    # Phobos
    b += '<g transform="translate(1440 130)"><ellipse cx="0" cy="0" rx="26" ry="19" fill="#8a7a6e"/><path d="M-6 -18 a26 19 0 0 1 32 18 a26 19 0 0 1 -20 18 q16 -18 -12 -36z" fill="#2a2230" opacity=".7"/><circle cx="-8" cy="-2" r="5" fill="#6a5a50"/></g>'
    b += '<rect width="1920" height="1080" fill="url(#olyGlow)"/>'
    # distant low hills
    hp = [(x, G - 30 - 22 * math.sin(x / 170) - 12 * math.sin(x / 61)) for x in range(0, 1941, 30)]
    b += f'<polygon points="{P(hp + [(1940, G + 10), (0, G + 10)])}" fill="#7d3d2c" opacity=".8"/>'
    # Olympus Mons: broad shield, flat top with caldera, basal cliff
    cx, top, wl, wr = 1330, 360, 760, 700
    prof = []
    for i in range(61):
        t = i / 60; x = cx - wl + t * (wl + wr)
        u = (x - cx) / (wl if x < cx else wr)
        y = top + (G - 70 - top) * (abs(u) ** 1.9)      # gentle shield above the cliff
        prof.append((x, y))
    r = random.Random(6)
    prof = [(x, y + r.uniform(-3, 3)) for x, y in prof]
    cliff_top = prof
    sil = [(cx - wl - 30, G)] + cliff_top + [(cx + wr + 30, G)]
    defs += f'<clipPath id="mC"><polygon points="{P(sil)}"/></clipPath>'
    b += f'<polygon points="{P(sil)}" fill="url(#olyS)"/>'
    g = '<g clip-path="url(#mC)">'
    # sunlit right flank (light from upper right)
    lit = [(cx - 40, top - 10)] + [p for p in prof if p[0] > cx - 40] + [(cx + wr + 30, G), (cx + 120, G)]
    g += f'<polygon points="{P(lit)}" fill="url(#olyL)" opacity=".95"/>'
    # radial lava flow streaks
    for k in range(34):
        a = r.uniform(-1, 1); x0 = cx + a * 180; x1 = cx + a * (wl if a < 0 else wr) * 1.05
        g += f'<path d="M{x0:.0f} {top + 30:.0f} Q {(x0 + x1) / 2 + r.uniform(-40, 40):.0f} {(top + G) / 2:.0f} {x1:.0f} {G:.0f}" fill="none" stroke="{"#5a2418" if r.random() < .6 else "#ffc08a"}" stroke-width="{r.uniform(2, 6):.1f}" opacity="{r.uniform(.15, .35):.2f}"/>'
    # basal cliff band
    cl = [(x, y) for x, y in prof if y > G - 110]
    g += f'<path d="M{cx - wl - 40} {G - 70} Q {cx} {G - 96} {cx + wr + 40} {G - 70} L {cx + wr + 40} {G} L {cx - wl - 40} {G}Z" fill="#3a1712" opacity=".75"/>'
    g += ''.join(f'<path d="M{x} {G - 78 - 18 * math.exp(-((x - cx) / 500) ** 2):.0f} l{r.uniform(-6, 6):.0f} {r.uniform(40, 80):.0f}" stroke="#1f0b08" stroke-width="3" opacity=".5"/>' for x in range(cx - wl, cx + wr, 26))
    g += f'<path d="M{cx - wl - 40} {G - 72} Q {cx} {G - 98} {cx + wr + 40} {G - 72}" fill="none" stroke="#ffb27a" stroke-width="3" opacity=".5"/>'
    g += '</g>'
    b += g
    # caldera on the summit (nested collapse pits)
    b += f'<ellipse cx="{cx + 10}" cy="{top + 10}" rx="140" ry="22" fill="#5a2a20" stroke="#ffcf9a" stroke-width="3" opacity=".95"/>'
    b += f'<ellipse cx="{cx - 20}" cy="{top + 12}" rx="70" ry="12" fill="#3a1712"/><ellipse cx="{cx + 70}" cy="{top + 8}" rx="46" ry="9" fill="#44201a"/>'
    b += f'<polyline points="{P([p for p in prof if abs(p[0] - cx) < 420])}" fill="none" stroke="#ffe0b8" stroke-width="5" opacity=".85"/>'
    b += f'<ellipse cx="{cx}" cy="{top}" rx="260" ry="70" fill="#ffe2b8" opacity=".25" filter="url(#b26)"/>'
    # thin haze band across the flanks (summit pokes above it)
    b += f'<rect x="0" y="{G - 230}" width="1920" height="120" fill="#e8a070" opacity=".22" filter="url(#b26)"/>'
    # a small snowy Everest at the foot, for scale (Olympus is about 2.5x as tall)
    eh = (G - top) / 2.5; ex = 820
    EL = jag((ex - 150, G), (ex, G - eh), 6, 10, 41); ER = jag((ex, G - eh), (ex + 140, G), 6, 10, 42)
    b += f'<polygon points="{P(EL + ER[1:])}" fill="#4b4f6e" stroke="#1d1830" stroke-width="3"/>'
    b += f'<polygon points="{P(ER + [(ex + 30, G), (ex + 4, G - eh + 30)])}" fill="#7a7f9e"/>'
    sn = jag((ex - 92, G - eh * .5), (ex + 90, G - eh * .48), 7, 12, 43)
    defs += f'<clipPath id="evC"><polygon points="{P(EL + ER[1:])}"/></clipPath>'
    b += f'<polygon points="{P([(ex - 200, G - eh - 20), (ex + 200, G - eh - 20)] + sn[::-1])}" fill="#ffffff" clip-path="url(#evC)"/>'
    b += f'<polygon points="{P([(ex - 200, G - eh - 20), (ex + 4, G - eh - 20)] + [(ex + 4, G - eh + 30)] + sn[:4][::-1])}" fill="#b9c6e6" clip-path="url(#evC)"/>'
    b += f'<polyline points="{P(EL + ER[1:])}" fill="none" stroke="#bfe8ff" stroke-width="3" opacity=".7"/>'
    # ground
    gp = [(x, G - 6 + 8 * math.sin(x / 140)) for x in range(0, 1941, 40)]
    b += f'<polygon points="{P(gp + [(1940, 1080), (0, 1080)])}" fill="url(#groundC)"/>'
    b += ''.join(f'<ellipse cx="{r.uniform(0, 1500):.0f}" cy="{r.uniform(G + 20, 1070):.0f}" rx="{r.uniform(10, 36):.0f}" ry="{r.uniform(4, 10):.0f}" fill="#2a0e09" opacity=".45"/>' for _ in range(30))
    # foreground boulders (left), lit from the right
    for bx, by, bw, bh in ((140, 1080, 260, 120), (420, 1080, 180, 70), (40, 1000, 120, 60)):
        b += f'<path d="M{bx - bw / 2} {by} q{bw * .1} -{bh} {bw * .5} -{bh} q{bw * .4} 0 {bw * .5} {bh}z" fill="#5a2418" stroke="#1f0b08" stroke-width="3"/>'
        b += f'<path d="M{bx + bw * .05} {by - bh + 4} q{bw * .38} 4 {bw * .44} {bh - 6}" fill="none" stroke="#f0a06a" stroke-width="6" opacity=".7"/>'
    # dust in the air
    b += ''.join(f'<circle cx="{r.uniform(0, 1920):.0f}" cy="{r.uniform(500, 1000):.0f}" r="{r.uniform(1.5, 3.5):.1f}" fill="#ffd6b0" opacity="{r.uniform(.2, .5):.2f}"/>' for _ in range(70))
    b += sparkles([(cx + 220, top - 70, 22), (cx - 260, top - 40, 16), (1700, 520, 14), (ex + 40, G - eh - 30, 14)])
    # ---- astronaut frog on the boulder, pointing up at the giant ----
    pack = '<rect x="-60" y="-66" width="28" height="58" rx="8" fill="#d9dde6" stroke-width="3.2"/><rect x="-55" y="-58" width="6" height="40" rx="3" fill="#ffffff" stroke="none" opacity=".7"/>'
    suit = ('<path d="M-36 -2 q-6 -30 4 -42 q34 -10 68 -2 q10 14 6 44 q-40 8 -78 0z" fill="#eef0f4" stroke-width="3.6"/>'
            '<rect x="-6" y="-34" width="22" height="14" rx="3" fill="#7d8aa3" stroke-width="2.4"/><circle cx="0" cy="-27" r="2.4" fill="#e65a4a" stroke="none"/><circle cx="9" cy="-27" r="2.4" fill="#5fc0e6" stroke="none"/>'
            '<path d="M-28 -16 q34 8 68 0" fill="none" stroke="#c9b06a" stroke-width="4"/>')
    helmet = ('<circle cx="6" cy="-62" r="46" fill="#cfe9ff" fill-opacity=".16" stroke="#e6e9f0" stroke-width="6"/>'
              '<path d="M-28 -88 A38 38 0 0 1 4 -102" fill="none" stroke="#fff" stroke-width="5" opacity=".8"/>'
              '<path d="M30 -96 a40 40 0 0 1 14 22" fill="none" stroke="#ffb27a" stroke-width="4" opacity=".7"/>')
    b += '<ellipse cx="300" cy="972" rx="90" ry="12" fill="#000" opacity=".35"/>'
    b += frog(300, 966, 3.0, look=(5, -4), mouth='O', back=pack, mid=suit, top=helmet, armR='M38 -24 q26 -18 34 -52', sleeve='#eef0f4')
    b += '<rect width="1920" height="1080" fill="url(#vigC)"/>'
    lines = [('21-22 KM', 196, 'y'), ('ON MARS', 150, 'w')]
    return page('#0d0a1e', svg(defs, b), lines, outline='#120818')


for n, fn in (('A', thumb_A), ('B', thumb_B), ('C', thumb_C)):
    open(os.path.join(HERE, f'{n}.html'), 'w').write(fn())
print('ok')
