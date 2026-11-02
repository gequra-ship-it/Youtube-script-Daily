# Thumbnails A-C for deep-sea-giants (guideline 16-6 / 16-8, brief tools/briefs/thumb_art.md). Run: python3 videos/deep-sea-giants/thumb/make.py
# A  THE REAL KRAKEN      homage: Hokusai, The Great Wave off Kanagawa (mirrored): the wave hides a colossal squid, its arms are the foam claws,
#                         Fuji in the trough, frog in a Japanese fishing boat. Script S15-S16: "The legends were exaggerated, but the real animals behind them..."
# B  ONE EYE = 27 CM      intuitive: a colossal squid eye filling the frame, lit by the beam of a tiny submersible (frog at the dome).
#                         Script S18: "A single eye has been measured at about twenty-seven centimeters across, roughly the size of a large dinner plate."
# C  WHY SO HUGE DOWN HERE?  intuitive: giant isopod on the sea floor under falling marine snow, eyeing a garden woodlouse on the diving frog's fingertip.
#                         Script S12/S25: isopod up to about forty centimeters; "A garden woodlouse fits on your fingertip, while a deep-sea isopod needs two hands."
import os, sys, math, random
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', '..', 'tools'))
from thumb_lib import page, svg, lin, rad, spark

# ---- mascot frog (body from tools/assets/frog.svg; same helper as videos/fourth-dimension/thumb/make.py) ----
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
         brows=True, back="", front="", shadow=False, mid=""):
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
    g.append(mid)
    for a in (armL or 'M-34 -22 q-14 6 -16 22', armR or 'M38 -22 q14 6 16 22'):
        g.append(limb(a)); ex_, ey_ = end_of(a)
        g.append(f'<circle cx="{ex_:.1f}" cy="{ey_:.1f}" r="5.6" fill="{GREEN}" stroke-width="3"/>')
    g.append(front); g.append('</g>')
    return ''.join(g)



# ---------------- geometry helpers ----------------
def bez(p, t):
    (x0, y0), (x1, y1), (x2, y2), (x3, y3) = p; u = 1 - t
    return (u ** 3 * x0 + 3 * u * u * t * x1 + 3 * u * t * t * x2 + t ** 3 * x3,
            u ** 3 * y0 + 3 * u * u * t * y1 + 3 * u * t * t * y2 + t ** 3 * y3)


def tentacle(p, w0, w1, col, dark, lite, suck='#f3d9c4', n=46, side=1, sk=True):
    """Tapered squid arm along cubic p, suckers on one side (side=+1/-1)."""
    C = [bez(p, i / n) for i in range(n + 1)]
    L, R, N, W = [], [], [], []
    for i, (x, y) in enumerate(C):
        a = C[max(i - 1, 0)]; b = C[min(i + 1, n)]
        dx, dy = b[0] - a[0], b[1] - a[1]; l = math.hypot(dx, dy) or 1
        nx, ny = -dy / l, dx / l; w = w0 + (w1 - w0) * (i / n) ** .8
        L.append((x + nx * w, y + ny * w)); R.append((x - nx * w, y - ny * w)); N.append((nx, ny)); W.append(w)
    o = f'<path d="M{P(L)} L{P(R[::-1])}Z" fill="{col}" stroke="{dark}" stroke-width="5" stroke-linejoin="round"/>'
    hi = [(x - nx * w * .45 * side, y - ny * w * .45 * side) for (x, y), (nx, ny), w in zip(C, N, W)]
    o += f'<polyline points="{P(hi[:-3])}" fill="none" stroke="{lite}" stroke-width="{max(3, w0 * .28):.0f}" stroke-linecap="round" opacity=".7"/>'
    if sk:
        for i in range(3, n - 2, 2):
            (x, y), (nx, ny), w = C[i], N[i], W[i]
            r = max(2.5, w * .32); sx, sy = x + nx * w * .62 * side, y + ny * w * .62 * side
            o += f'<circle cx="{sx:.1f}" cy="{sy:.1f}" r="{r:.1f}" fill="{suck}" stroke="{dark}" stroke-width="{max(1.5, r * .35):.1f}"/>'
    return o


def P2(pts):
    return 'M' + ' L'.join(f'{a:.1f} {b:.1f}' for a, b in pts)


# ================= A: The Great Wave hides the Kraken =================
def wave_boat(x, y, L, ang, rnd, rowers=True):
    o = f'<g transform="translate({x} {y}) rotate({ang})">'
    o += f'<path d="M{-L / 2} 0 Q{-L / 2 + 30} 30 {-L / 2 + 70} 34 L{L / 2 - 40} 34 Q{L / 2} 24 {L / 2 + 20} -14 Q{L / 2 - 20} 6 {L / 2 - 60} 8 L{-L / 2 + 20} 8 Z" fill="#e8d6a0" stroke="#2b2416" stroke-width="5" stroke-linejoin="round"/>'
    o += f'<path d="M{-L / 2 + 30} 16 L{L / 2 - 50} 18" stroke="#b79a5c" stroke-width="5"/>'
    if rowers:
        for k in range(5):
            rx = -L / 2 + 70 + k * (L - 140) / 4
            o += (f'<path d="M{rx - 18} 8 Q{rx - 16} -22 {rx} -26 Q{rx + 16} -22 {rx + 18} 8Z" fill="#2c4f7c" stroke="#13233a" stroke-width="3"/>'
                  f'<circle cx="{rx}" cy="-30" r="8" fill="#e9cfa2" stroke="#13233a" stroke-width="2.5"/>')
    return o + '</g>'


def small_wave(x0, x1, ybase, peak, col, rnd, curl=1):
    """foreground wave with claw foam (Hokusai)"""
    w = x1 - x0; px = x0 + w * .55
    d = f'M{x0} {ybase} Q{x0 + w * .3} {ybase - peak * .3} {px - w * .12} {ybase - peak * .95} Q{px} {ybase - peak * 1.08} {px + w * .12} {ybase - peak * .92} Q{x1 - w * .15} {ybase - peak * .4} {x1} {ybase} Z'
    o = f'<path d="{d}" fill="{col}" stroke="#0b1a33" stroke-width="5"/>'
    for k in range(1, 5):
        o += f'<path d="M{x0 + w * .1 + k * 18} {ybase - k * 6} Q{x0 + w * .32 + k * 10} {ybase - peak * .35 + k * 14} {px - w * .1 + k * 6} {ybase - peak * .85 + k * 22}" fill="none" stroke="#9cc0e0" stroke-width="5" opacity=".55"/>'
    # foam claws on the crest
    for k in range(7):
        t = k / 6; cx = px - w * .14 + t * w * .26; cy = ybase - peak * 1.0 + abs(t - .5) * peak * .25
        o += f'<path d="M{cx - 14} {cy + 6} Q{cx - 6} {cy - 26} {cx + 12} {cy - 22} Q{cx + 2} {cy - 12} {cx + 8} {cy - 2} Z" fill="#f4eedc" stroke="#0b1a33" stroke-width="3"/>'
    return o


def make_A():
    rnd = random.Random(11)
    d = FILTERS
    d += lin('skyA', [(0, '#a8916a'), (.35, '#d8c69c'), (1, '#efe4c8')])
    d += lin('waveA', [(0, '#2f6197'), (.45, '#1b3d6e'), (1, '#091a35')])
    d += lin('seaA', [(0, '#2b5a8e'), (1, '#0a1b36')])
    d += lin('fujiA', [(0, '#4e6688'), (1, '#203450')])
    d += rad('eyeGA', 1640, 560, 300, [(0, '#ffd66a', .95), (.35, '#ff9a3a', .45), (1, '#ff7a2a', 0)])
    d += rad('vigA', 960, 540, 1150, [(0, '#000', 0), (.7, '#000', 0), (1, '#1a1206', .35)])
    WP = ('M2000 1080 L2000 480 C1900 260 1700 120 1450 130 C1230 140 1080 230 1035 345 '
          'C1100 295 1190 300 1235 360 C1285 425 1245 520 1180 600 C1110 690 1020 790 890 870 Q800 920 740 1080 Z')
    d += f'<clipPath id="wclip"><path d="{WP}"/></clipPath>'
    b = '<rect width="1920" height="1080" fill="url(#skyA)"/>'
    # paper grain + soft cloud bands
    for _ in range(500):
        b += f'<circle cx="{rnd.uniform(0, 1920):.0f}" cy="{rnd.uniform(0, 860):.0f}" r="{rnd.choice([1, 1.5, 2])}" fill="#7a6440" opacity="{rnd.uniform(.05, .2):.2f}"/>'
    b += '<path d="M180 610 Q420 590 660 612 Q520 628 260 626Z" fill="#c4ae84" opacity=".55"/><path d="M500 540 Q700 525 880 545 Q760 556 560 556Z" fill="#c4ae84" opacity=".45"/>'
    # distant sea + Fuji in the trough
    b += '<rect x="0" y="830" width="1920" height="260" fill="url(#seaA)"/>'
    b += ('<path d="M560 838 L700 742 Q735 722 770 742 L930 838Z" fill="url(#fujiA)" stroke="#13233a" stroke-width="4"/>'
          '<path d="M685 753 L700 742 Q735 722 770 742 L786 754 L772 764 L756 752 L738 770 L720 754 L702 766Z" fill="#f6f1e2" stroke="#13233a" stroke-width="3"/>')
    for k in range(9):
        x = 420 + k * 70
        b += f'<path d="M{x} 846 q18 -14 36 0" fill="none" stroke="#a9c6e2" stroke-width="3" opacity=".6"/>'
    # second boat in the trough under the wave
    b += wave_boat(905, 860, 300, 14, rnd)
    # ---- the great wave, hiding the colossal squid ----
    g = f'<g transform="translate(40 20)">'
    g += f'<path d="{WP}" fill="url(#waveA)"/>'
    inner = f'<g clip-path="url(#wclip)">'
    # squid head + mantle glimpsed inside the wave
    inner += '<ellipse cx="1660" cy="640" rx="330" ry="250" fill="#8a2420" opacity=".55" filter="url(#b12)"/>'
    inner += '<path d="M1500 760 Q1560 520 1760 470 Q1980 440 2000 620 L2000 900 Q1800 820 1500 760Z" fill="#a8322a" opacity=".5"/>'
    for _ in range(70):
        inner += f'<circle cx="{rnd.uniform(1480, 1990):.0f}" cy="{rnd.uniform(470, 860):.0f}" r="{rnd.uniform(4, 11):.0f}" fill="#d0563a" opacity="{rnd.uniform(.15, .45):.2f}"/>'
    # Hokusai striations following the back of the wave
    back = 'M2000 480 C1900 260 1700 120 1450 130 C1230 140 1080 230 1035 345'
    for k in range(1, 15):
        inner += f'<path d="{back}" transform="translate({k * 16} {k * 46})" fill="none" stroke="#86afd8" stroke-width="{7 - k * .3:.1f}" opacity="{.6 - k * .03:.2f}"/>'
        inner += f'<path d="{back}" transform="translate({k * 16 + 8} {k * 46 + 18})" fill="none" stroke="#0c2142" stroke-width="5" opacity=".35"/>'
    inner += '<circle cx="1640" cy="560" r="300" fill="url(#eyeGA)"/>'
    inner += '</g>'
    g += inner
    g += f'<path d="{WP}" fill="none" stroke="#0b1a33" stroke-width="7"/>'
    # the eye (focal), looking down at the boats
    g += ('<ellipse cx="1640" cy="560" rx="96" ry="84" fill="#5a120e" stroke="#2a0606" stroke-width="6"/>'
          '<circle cx="1630" cy="566" r="66" fill="#ffe6a0"/><circle cx="1630" cy="566" r="66" fill="none" stroke="#e39a2c" stroke-width="12"/>'
          '<circle cx="1618" cy="576" r="40" fill="#120404"/><ellipse cx="1600" cy="548" rx="16" ry="11" fill="#fff" transform="rotate(-30 1600 548)"/>'
          '<circle cx="1640" cy="590" r="5" fill="#fff" opacity=".8"/>'
          '<path d="M1546 520 Q1640 456 1734 522" fill="none" stroke="#2a0606" stroke-width="10" stroke-linecap="round"/>')
    # foam band along the crest
    g += f'<path d="M1950 400 C1880 240 1700 140 1450 150 C1250 158 1110 238 1065 330" fill="none" stroke="#f4eedc" stroke-width="30" stroke-linecap="round"/>'
    g += f'<path d="M1950 400 C1880 240 1700 140 1450 150 C1250 158 1110 238 1065 330" fill="none" stroke="#0b1a33" stroke-width="4" transform="translate(0 16)" opacity=".7"/>'
    # squid arms bursting from the crest = the claws of the wave
    arms = [((1800, 230), (1840, 60), (1640, 10), (1600, 120), 34, 5, -1),
            ((1620, 160), (1600, 10), (1400, -10), (1380, 100), 36, 5, -1),
            ((1450, 150), (1400, 30), (1220, 30), (1210, 150), 34, 5, -1),
            ((1290, 180), (1220, 90), (1100, 110), (1120, 230), 30, 4, -1),
            ((1150, 250), (1080, 190), (1010, 260), (1060, 330), 26, 4, -1)]
    for p0, p1, p2, p3, w0, w1, sd in arms:
        g += tentacle((p0, p1, p2, p3), w0, w1, '#c84a34', '#3a0c08', '#f19a70', side=sd)
    # curled tip hooks
    for x, y, r in ((1600, 120, 22), (1380, 100, 24), (1210, 150, 20), (1120, 230, 16)):
        g += f'<path d="M{x} {y} q{-r} {r * .4} {-r * .4} {r * 1.2} q{r * .7} {r * .2} {r * .5} {-r * .5}" fill="none" stroke="#3a0c08" stroke-width="5" stroke-linecap="round"/>'
    # spray (Hokusai snow) off the crest
    for _ in range(90):
        x = rnd.uniform(1000, 1900); y = rnd.uniform(20, 330) + (x - 1000) * -.05
        b2 = rnd.uniform(3, 8)
        g += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{b2:.1f}" fill="#fbf7ea" stroke="#0b1a33" stroke-width="1.6" opacity=".95"/>'
    g += '</g>'
    b += g
    # foreground wave + boat with the frog (bottom-left)
    b += small_wave(-40, 760, 1080, 260, 'url(#waveA)', rnd)
    band = ('<path d="M-30 -80 Q6 -92 44 -80" fill="none" stroke="#2c4f7c" stroke-width="10"/>'
            '<path d="M-30 -80 q-16 -4 -26 8 M-30 -80 q-12 8 -26 16" fill="none" stroke="#2c4f7c" stroke-width="6"/>')
    b += f'<circle cx="400" cy="820" r="170" fill="#fff6d6" opacity=".35" filter="url(#b50)"/>'
    b += frog(400, 950, 2.9, rot=-6, look=(9, -5), mouth='O', back='', mid=band, brows=False,
              armL='M-34 -22 q-24 -10 -34 -36', armR='M38 -22 q20 -16 26 -40')
    b += wave_boat(360, 950, 560, -8, rnd, rowers=False)
    b += small_wave(140, 760, 1110, 120, 'url(#waveA)', rnd)
    b += spark(560, 700, 22, '#ffffff') + spark(980, 470, 16, '#ffffff')
    b += '<rect width="1920" height="1080" fill="url(#vigA)"/>'
    lines = [('THE REAL', 150, 'w'), ('KRAKEN', 228, 'y')]
    return page('#d8c69c', svg(d, b), lines, outline='#0b1a33', top=46)


# ================= B: an eye the size of a dinner plate =================
def submarine(x, y, s, rnd):
    o = f'<g transform="translate({x} {y}) scale({s})" stroke="#1d1a10" stroke-linejoin="round" stroke-width="5">'
    o += '<rect x="-150" y="40" width="300" height="26" rx="10" fill="#6b6b6b"/>'  # skid
    o += '<path d="M-200 -10 Q-210 -90 -120 -100 L120 -100 Q200 -90 200 -10 Q200 50 120 56 L-120 56 Q-210 50 -200 -10Z" fill="#f2b632"/>'
    o += '<path d="M-180 -30 Q-170 -82 -110 -86 L110 -86" fill="none" stroke="#ffe08a" stroke-width="9" opacity=".9"/>'
    o += '<path d="M-200 0 Q-200 50 -120 56 L120 56 Q200 50 200 0" fill="#b9801c" stroke="none" opacity=".7"/>'
    o += '<rect x="-60" y="-140" width="120" height="44" rx="12" fill="#e7a52a"/>'   # tower
    o += '<rect x="-250" y="-40" width="60" height="50" rx="12" fill="#888"/><path d="M-250 -60 L-262 -15 L-250 30" fill="none"/>'  # thruster
    for k in range(3):
        o += f'<circle cx="{-120 + k * 50}" cy="10" r="12" fill="#3a3a3a"/><circle cx="{-124 + k * 50}" cy="6" r="4" fill="#fff" stroke="none" opacity=".6"/>'
    o += '<path d="M150 40 L230 70 L260 40" fill="none" stroke-width="12"/><path d="M150 40 L230 70 L260 40" fill="none" stroke="#9a9a9a" stroke-width="6"/>'
    o += '<path d="M250 30 l20 -6 M255 46 l22 4" stroke-width="6"/>'
    o += '</g>'
    return o


def make_B():
    rnd = random.Random(5)
    d = FILTERS
    d += rad('deepB', 1300, 500, 1300, [(0, '#0b2a4a', 1), (.6, '#04101f', 1), (1, '#010409', 1)])
    d += rad('skinB', 1380, 470, 720, [(0, '#b0382e', 1), (.55, '#6e1a1a', 1), (1, '#2a0608', 1)])
    d += rad('sclB', 1330, 470, 300, [(0, '#f5fbff', 1), (.75, '#bcd6e6', 1), (1, '#6a8aa6', 1)])
    d += rad('irisB', 1320, 500, 230, [(0, '#2a1404', 1), (.78, '#8a5418', 1), (.9, '#e0a640', 1), (1, '#5a3410', 1)])
    d += rad('pupB', 1300, 520, 180, [(0, '#0a1a30', 1), (.7, '#02060e', 1), (1, '#000', 1)])
    d += lin('beamB', [(0, '#fff8d8'), (1, '#9fe3ff')], 1, -.3)
    d += rad('vigB', 960, 540, 1150, [(0, '#000', 0), (.65, '#000', 0), (1, '#000', .7)])
    d += '<clipPath id="beamClip"><path d="M690 735 L1080 190 L1520 830 Z"/></clipPath>'
    b = '<rect width="1920" height="1080" fill="url(#deepB)"/>'
    # far marine snow
    for _ in range(260):
        b += f'<circle cx="{rnd.uniform(0, 1920):.0f}" cy="{rnd.uniform(0, 1080):.0f}" r="{rnd.choice([1, 1.5, 2.2])}" fill="#cfe6ff" opacity="{rnd.uniform(.08, .35):.2f}"/>'
    # squid head: mottled skin with chromatophores, arms trailing up/right
    b += '<path d="M960 520 Q980 140 1380 90 Q1800 60 2000 200 L2000 900 Q1700 1010 1380 930 Q1000 880 960 520Z" fill="url(#skinB)"/>'
    for p, w0, w1, sd in [(((1640, 160), (1760, -40), (1900, 220), (2040, 40)), 64, 22, 1),
                          (((1760, 300), (1900, 180), (1880, 420), (2040, 380)), 56, 24, -1),
                          (((1540, 120), (1560, -10), (1700, 60), (1760, -40)), 40, 12, 1)]:
        b += tentacle(p, w0, w1, '#8c2622', '#2a0606', '#d1604a', suck='#e8b49a', side=sd)
    for _ in range(260):
        x = rnd.uniform(980, 1990); y = rnd.uniform(90, 950)
        if (x - 1330) ** 2 + (y - 480) ** 2 < 340 ** 2: continue
        r = rnd.uniform(4, 16)
        b += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r:.0f}" fill="{rnd.choice(["#d44a30", "#7a1414", "#e8704a", "#4a0a0c"])}" opacity="{rnd.uniform(.25, .7):.2f}"/>'
    # eye socket folds
    b += '<circle cx="1330" cy="480" r="380" fill="#3a0a0c" opacity=".55" filter="url(#b24)"/>'
    b += '<path d="M960 470 Q1060 120 1340 110 Q1640 110 1720 420" fill="none" stroke="#e0705a" stroke-width="14" opacity=".55" stroke-linecap="round"/>'
    b += '<path d="M990 600 Q1130 880 1360 870 Q1600 860 1700 640" fill="none" stroke="#2a0406" stroke-width="20" opacity=".7" stroke-linecap="round"/>'
    # the eye: silvery sclera, golden iris, huge pupil
    b += '<circle cx="1330" cy="480" r="320" fill="#1a0406"/>'
    b += '<circle cx="1330" cy="480" r="300" fill="url(#sclB)"/>'
    b += '<circle cx="1320" cy="500" r="232" fill="url(#irisB)"/>'
    for k in range(48):
        a = k / 48 * 2 * math.pi; r0 = 186; r1 = 228
        b += f'<line x1="{1320 + r0 * math.cos(a):.0f}" y1="{500 + r0 * math.sin(a):.0f}" x2="{1320 + r1 * math.cos(a):.0f}" y2="{500 + r1 * math.sin(a):.0f}" stroke="#f2d27a" stroke-width="3" opacity=".35"/>'
    b += '<circle cx="1310" cy="512" r="182" fill="url(#pupB)"/>'
    # reflections in the pupil: window highlight + tiny sub with its lamp
    b += '<path d="M1190 380 Q1250 310 1350 318 Q1280 350 1236 420Z" fill="#ffffff" opacity=".85"/>'
    b += '<path d="M1160 470 Q1150 430 1170 410" fill="none" stroke="#ffffff" stroke-width="8" opacity=".5" stroke-linecap="round"/>'
    b += f'<g opacity=".8">{submarine(1250, 620, .16, rnd)}</g><circle cx="1285" cy="612" r="10" fill="#fffbe0"/>' + spark(1285, 612, 22, '#ffffff', .95)
    b += '<path d="M1580 300 Q1660 420 1630 560" fill="none" stroke="#ffffff" stroke-width="10" opacity=".45" stroke-linecap="round"/>'
    # the beam from the submersible
    b += '<path d="M690 735 L1080 190 L1520 830 Z" fill="url(#beamB)" opacity=".26" filter="url(#b12)"/>'
    b += '<path d="M690 735 L1000 330 L1300 760 Z" fill="#fffbe6" opacity=".18" filter="url(#b24)"/>'
    beam = ''
    for _ in range(170):
        beam += f'<circle cx="{rnd.uniform(680, 1520):.0f}" cy="{rnd.uniform(190, 840):.0f}" r="{rnd.choice([1.6, 2.4, 3.2, 4])}" fill="#ffffff" opacity="{rnd.uniform(.3, .9):.2f}"/>'
    b += f'<g clip-path="url(#beamClip)">{beam}</g>'
    # submersible with the frog at the dome (bottom-left/centre)
    b += '<circle cx="640" cy="760" r="240" fill="#ffe08a" opacity=".16" filter="url(#b50)"/>'
    b += submarine(480, 840, 1.0, rnd)
    b += '<circle cx="660" cy="765" r="40" fill="#fffbe0" opacity=".9" filter="url(#b12)"/><circle cx="660" cy="765" r="18" fill="#ffffff"/>'
    b += '<rect x="620" y="748" width="26" height="36" rx="6" fill="#555" stroke="#1d1a10" stroke-width="4"/>'
    # acrylic dome on top with the frog inside
    b += '<path d="M370 750 Q370 560 520 560 Q670 560 670 750Z" fill="#103048" opacity=".55" stroke="#1d1a10" stroke-width="5"/>'
    b += frog(515, 742, 2.05, look=(10, -6), mouth='O', armL='M-34 -22 q-14 -6 -18 -24', armR='M38 -22 q16 -10 26 -30')
    b += '<path d="M370 750 Q370 560 520 560 Q670 560 670 750Z" fill="#bfe8ff" opacity=".12" stroke="#e8f6ff" stroke-width="6"/>'
    b += '<path d="M400 690 Q410 600 490 582" fill="none" stroke="#ffffff" stroke-width="9" opacity=".7" stroke-linecap="round"/>'
    b += '<rect x="350" y="742" width="340" height="22" rx="8" fill="#c78a20" stroke="#1d1a10" stroke-width="5"/>'
    # a small fish for scale, fleeing past the eye
    b += '<path d="M900 860 q30 -18 60 0 q-30 18 -60 0z M960 860 l18 -12 l0 24z" fill="#9fb8cc" opacity=".8"/>'
    b += spark(1080, 230, 20, '#ffffff') + spark(1560, 210, 16) + spark(860, 610, 14, '#e8fbff')
    b += '<rect width="1920" height="1080" fill="url(#vigB)"/>'
    lines = [('ONE EYE =', 150, 'w'), ('27 CM', 270, 'y')]
    return page('#04101f', svg(d, b), lines, outline='#03070f', top=50)


# ================= C: giant isopod vs garden woodlouse =================
def isopod(cx, yb, L, H, rnd):
    x0, x1 = cx - L, cx + L

    def top(x):
        u = max(0.0, 1 - ((x - cx) / L) ** 2)
        return yb - H * u ** .55

    o = ''
    # shadow + far legs
    o += f'<ellipse cx="{cx}" cy="{yb + 95}" rx="{L * 1.02:.0f}" ry="40" fill="#020c10" opacity=".55" filter="url(#b12)"/>'
    for k in range(7):
        lx = x0 + 150 + k * 95
        o += f'<path d="M{lx} {yb} l{-18} 50 l{-26} 40" fill="none" stroke="#3c2a3c" stroke-width="16" stroke-linecap="round" stroke-linejoin="round"/>'
    # segments drawn tail -> head so each front segment overlaps the next
    edges = [x0 + 95] + [x0 + 95 + 96 * k for k in range(1, 8)] + [x0 + 95 + 96 * 7 + 30 * k for k in range(1, 5)]
    segs = list(zip(edges[:-1], edges[1:]))
    # tail shield (pleotelson) + uropods
    tx = edges[-1]
    o += f'<path d="M{tx - 10} {top(tx) - 6:.0f} Q{x1 - 20} {top(x1 - 60):.0f} {x1 + 30} {yb + 10} Q{x1 - 60} {yb + 40} {tx - 10} {yb + 30} Z" fill="url(#isoG)" stroke="#2c1a2c" stroke-width="6"/>'
    o += f'<path d="M{x1 - 40} {yb + 10} q60 10 90 50 q-50 0 -100 -28z" fill="#a98ea2" stroke="#2c1a2c" stroke-width="5"/>'
    for k in range(5):
        o += f'<path d="M{x1 + 30 - k * 14} {yb + 10 + k * 6} l14 8" stroke="#2c1a2c" stroke-width="4"/>'
    for a, bx in reversed(segs):
        pts = [(x, top(x) - 4) for x in [a + (bx + 16 - a) * i / 12 for i in range(13)]]
        e = bx + 16
        path = f'M{a} {yb + 34} L{a} {top(a):.0f} ' + ' '.join(f'L{x:.0f} {y:.0f}' for x, y in pts) + f' Q{e + 8} {(top(e) + yb) / 2:.0f} {e} {yb + 40} L{e - 10} {yb + 58} Z'
        o += f'<path d="{path}" fill="url(#isoG)" stroke="#2c1a2c" stroke-width="6" stroke-linejoin="round"/>'
        o += f'<path d="M{e - 4} {top(e) + 4:.0f} Q{e + 4} {(top(e) + yb) / 2:.0f} {e - 4} {yb + 30}" fill="none" stroke="#fbf0f4" stroke-width="5" opacity=".55"/>'
        o += f'<path d="M{a + 6} {top(a + 6) + 6:.0f} ' + ' '.join(f'L{x:.0f} {y + 6:.0f}' for x, y in pts[1:-2]) + '" fill="none" stroke="#ffffff" stroke-width="7" opacity=".7" stroke-linecap="round"/>'
        mx = (a + bx) / 2
        o += f'<ellipse cx="{mx:.0f}" cy="{top(mx) + 40:.0f}" rx="{(bx - a) * .28:.0f}" ry="14" fill="#ffffff" opacity=".45"/>'
        for _ in range(int((bx - a) / 6)):
            px = rnd.uniform(a + 8, bx - 4); py = rnd.uniform(top(px) + 30, yb + 20)
            o += f'<circle cx="{px:.0f}" cy="{py:.0f}" r="{rnd.uniform(1.5, 3.5):.1f}" fill="#6a4e66" opacity=".35"/>'
    # head: small, tucked under the first plate, big reflective compound eye on its side
    hx = x0 + 95; ht = top(hx) + 60
    o += (f'<path d="M{hx + 20} {ht:.0f} Q{x0 + 10} {ht - 6:.0f} {x0 - 20} {yb - 20} Q{x0 - 26} {yb + 34} {x0 + 30} {yb + 42} L{hx + 20} {yb + 42} Z" '
          f'fill="url(#isoG)" stroke="#2c1a2c" stroke-width="6"/>')
    o += f'<path d="M{x0 - 4} {yb - 40} Q{x0 + 20} {ht + 8:.0f} {hx + 10} {ht + 8:.0f}" fill="none" stroke="#ffffff" stroke-width="6" opacity=".6"/>'
    ex, ey = x0 + 46, yb - 30
    o += f'<ellipse cx="{ex}" cy="{ey:.0f}" rx="40" ry="30" fill="#1e1c26" stroke="#120c14" stroke-width="5" transform="rotate(-15 {ex} {ey:.0f})"/>'
    for i in range(-4, 5):
        for j in range(-3, 4):
            px = ex + i * 9 + (j % 2) * 4.5; py = ey + j * 8
            if ((px - ex) / 36) ** 2 + ((py - ey) / 26) ** 2 < 1:
                o += f'<circle cx="{px:.0f}" cy="{py:.0f}" r="3" fill="#9fc0cc" opacity=".4"/>'
    o += f'<ellipse cx="{ex - 12}" cy="{ey - 10:.0f}" rx="12" ry="7" fill="#ffffff" opacity=".9" transform="rotate(-15 {ex - 12} {ey - 10:.0f})"/>'
    # antennae reaching toward the woodlouse
    for dpath, w in ((f'M{x0 - 15} {yb + 5} C{x0 - 110} {yb - 90} {x0 - 190} {yb - 40} {x0 - 225} {yb + 50}', 13),
                     (f'M{x0 - 10} {yb + 25} C{x0 - 80} {yb + 20} {x0 - 120} {yb + 80} {x0 - 110} {yb + 130}', 11)):
        o += f'<path d="{dpath}" fill="none" stroke="#2c1a2c" stroke-width="{w}" stroke-linecap="round"/>'
        o += f'<path d="{dpath}" fill="none" stroke="#c7aabb" stroke-width="{w - 6}" stroke-dasharray="16 4" stroke-linecap="round"/>'
    # near legs
    for k in range(7):
        lx = x0 + 130 + k * 95
        o += f'<path d="M{lx} {yb + 30} l{-10 + k * 2} 46 l{-30} 40" fill="none" stroke="#2c1a2c" stroke-width="20" stroke-linecap="round" stroke-linejoin="round"/>'
        o += f'<path d="M{lx} {yb + 30} l{-10 + k * 2} 46 l{-30} 40" fill="none" stroke="#b497a8" stroke-width="10" stroke-linecap="round" stroke-linejoin="round"/>'
    return o


def woodlouse(x, y, s):
    o = f'<g transform="translate({x} {y}) scale({s})" stroke="#1c1c20" stroke-width="3">'
    o += '<path d="M-40 0 Q-38 -30 0 -32 Q38 -30 42 0 Z" fill="#7d8088"/>'
    for k in range(1, 7):
        xx = -40 + k * 12
        o += f'<path d="M{xx} {-math.sqrt(max(0, 1 - (xx / 41) ** 2)) * 31:.0f} L{xx + 2} 0" fill="none" stroke-width="2.5"/>'
    o += '<path d="M-30 -18 Q0 -30 30 -18" fill="none" stroke="#c8ccd4" stroke-width="3"/>'
    o += '<path d="M-40 -6 q-12 -8 -16 -20 M-40 -4 q-14 -2 -20 -10" fill="none" stroke-width="2.5"/>'
    return o + '</g>'


def make_C():
    rnd = random.Random(23)
    d = FILTERS
    d += lin('waterC', [(0, '#155e6e'), (.5, '#0a3446'), (1, '#04161f')])
    d += lin('floorC', [(0, '#3e6668'), (1, '#0c1e22')])
    d += lin('shaftC', [(0, '#e8fff6'), (1, '#e8fff6')])
    d += lin('isoG', [(0, '#fbeef0'), (.3, '#e2c3cc'), (.7, '#a87f95'), (1, '#4e3049')])
    d += rad('haloC', 1260, 520, 640, [(0, '#8ff0e0', .35), (.6, '#3aa6a6', .1), (1, '#000', 0)])
    d += rad('vigC', 960, 540, 1150, [(0, '#000', 0), (.6, '#000', 0), (1, '#000', .65)])
    b = '<rect width="1920" height="1080" fill="url(#waterC)"/>'
    b += '<path d="M940 -20 L1560 -20 L1820 820 L760 820 Z" fill="#e8fff6" opacity=".12" filter="url(#b24)"/>'
    b += '<path d="M1120 -20 L1380 -20 L1500 820 L1020 820 Z" fill="#e8fff6" opacity=".1" filter="url(#b24)"/>'
    b += '<rect width="1920" height="1080" fill="url(#haloC)"/>'
    # distant rock silhouettes
    b += '<path d="M0 760 Q120 700 260 730 Q380 690 520 740 L520 800 L0 800Z" fill="#0b2c38" opacity=".9"/>'
    b += '<path d="M1500 770 Q1650 690 1800 720 Q1880 700 1920 720 L1920 800 L1500 800Z" fill="#0b2c38" opacity=".9"/>'
    # sea floor
    b += '<path d="M0 790 Q480 760 960 785 Q1440 805 1920 775 L1920 1080 L0 1080Z" fill="url(#floorC)"/>'
    for _ in range(120):
        x = rnd.uniform(0, 1920); y = rnd.uniform(800, 1080)
        b += f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{rnd.uniform(3, 14):.0f}" ry="{rnd.uniform(2, 6):.0f}" fill="#081619" opacity="{rnd.uniform(.2, .5):.2f}"/>'
    b += '<path d="M60 1000 q40 -20 90 -4 q30 10 60 0" fill="none" stroke="#5f8a86" stroke-width="5" opacity=".5"/>'
    # brittle star + glass sponge details
    bs = '<g transform="translate(1120 980)">' + ''.join(f'<path d="M0 0 Q{40 * math.cos(a) + 10:.0f} {16 * math.sin(a) - 8:.0f} {70 * math.cos(a):.0f} {26 * math.sin(a):.0f}" fill="none" stroke="#c97a5a" stroke-width="7" stroke-linecap="round"/>' for a in [k * 2 * math.pi / 5 + .3 for k in range(5)]) + '<circle r="12" fill="#d98a66"/></g>'
    b += bs
    b += '<path d="M240 790 q-6 -90 18 -130 q20 40 14 130z" fill="#cfe2da" opacity=".5" stroke="#8fb0a6" stroke-width="3"/>'
    # the giant isopod (focal)
    b += isopod(1330, 700, 500, 320, rnd)
    # marine snow
    for _ in range(300):
        x = rnd.uniform(0, 1920); y = rnd.uniform(0, 1000)
        inshaft = 900 < x < 1700
        b += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{rnd.choice([1.4, 2, 2.8, 3.6])}" fill="#f2fff8" opacity="{rnd.uniform(.25, .9) if inshaft else rnd.uniform(.1, .45):.2f}"/>'
    # the diving frog holding up a garden woodlouse on its fingertip
    b += '<circle cx="580" cy="760" r="90" fill="#fff6c8" opacity=".35" filter="url(#b24)"/>'
    b += frog(380, 975, 2.75, flip=False, look=(9, -6), mouth='O', helmet=True, shadow=True,
              armL='M-34 -22 q-18 4 -24 22', armR='M38 -22 q26 -12 34 -52')
    b += woodlouse(578, 760, .95)
    b += spark(640, 760, 22, '#fff6d6') + spark(1560, 260, 18) + spark(1020, 330, 14, '#e8fbff')
    # bubbles from the helmet
    for k, (bx, by, r) in enumerate([(420, 640, 10), (440, 590, 14), (424, 530, 9), (452, 480, 12)]):
        b += f'<circle cx="{bx}" cy="{by}" r="{r}" fill="none" stroke="#e8fbff" stroke-width="3" opacity=".7"/>'
    b += '<rect width="1920" height="1080" fill="url(#vigC)"/>'
    lines = [('WHY SO', 160, 'w'), ('HUGE', 250, 'y'), ('DOWN HERE?', 116, 'w')]
    return page('#0a3446', svg(d, b), lines, outline='#03141c', top=40)


for n, fn in (('A', make_A), ('B', make_B), ('C', make_C)):
    open(os.path.join(HERE, f'{n}.html'), 'w').write(fn())
print('ok')
