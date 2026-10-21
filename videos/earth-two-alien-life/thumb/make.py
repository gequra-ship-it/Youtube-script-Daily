import sys, os, math, random
TOOLS = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', 'tools')
sys.path.insert(0, TOOLS)
from thumb_lib import *
os.chdir(os.path.dirname(os.path.abspath(__file__)))
# earth-two-alien-life thumbnails (2026-10-21, Opus thumbnail agent, brief tools/briefs/thumb_art.md + guideline 16-6).
# A = homage (Star Wars "binary sunset" hill: lone figure watching the low suns) -> TRAPPIST-1e sky (S21-S23): ruddy red-dwarf sun + 6 sister worlds.
# B = intuitive: tidally locked world, blazing day side / frozen night side, glowing twilight ring (S18-S19: "no rhythm of sunrise and sunset").
# C = homage (Apollo 8 "Earthrise" photo): Earth rising over the grey lunar horizon, tiny distant worlds (S40: "There is currently no planet B").
FR = 'x="-60%" y="-60%" width="220%" height="220%"'
FX = (f'<filter id="bl" {FR}><feGaussianBlur stdDeviation="8"/></filter><filter id="bl2" {FR}><feGaussianBlur stdDeviation="26"/></filter>'
      f'<filter id="bl3" {FR}><feGaussianBlur stdDeviation="3"/></filter><filter id="bl5" {FR}><feGaussianBlur stdDeviation="60"/></filter>'
      '<filter id="bl1"><feGaussianBlur stdDeviation="1.4"/></filter>')


def lit_path(cx, cy, r, t):
    """lit region of a sphere lit from +x (before rotation). t = terminator x offset at the equator / r (-1 full .. +1 new)."""
    rx = max(abs(t) * r, .5)
    sweep = 1 if t < 0 else 0
    return f'M{cx} {cy - r} A{r} {r} 0 0 1 {cx} {cy + r} A{rx:.1f} {r} 0 0 {sweep} {cx} {cy - r}Z'


def term_arc(cx, cy, r, t):
    rx = max(abs(t) * r, .5); sweep = 1 if t < 0 else 0
    return f'M{cx} {cy + r} A{rx:.1f} {r} 0 0 {sweep} {cx} {cy - r}'


def shade(id, cx, cy, r, t, ang, dark, op=.93, soft=10):
    """defs + overlay that darkens the unlit part; light comes from angle ang (deg, 0 = +x, -90 = up)."""
    dfs = (f'<mask id="{id}" maskUnits="userSpaceOnUse" x="0" y="0" width="1920" height="1080"><circle cx="{cx}" cy="{cy}" r="{r}" fill="#fff"/>'
           f'<path d="{lit_path(cx, cy, r, t)}" fill="#000" transform="rotate({ang} {cx} {cy})" filter="url(#sf{id})"/></mask>'
           f'<filter id="sf{id}" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="{soft}"/></filter>')
    return dfs, f'<rect width="1920" height="1080" fill="{dark}" opacity="{op}" mask="url(#{id})"/>'


def bands(cx, cy, r, n, col='#fff', tilt=.16, wmin=3, wmax=12, omin=.3, omax=.75):
    """broken cloud streaks following the sphere's latitude lines (front half of each latitude ellipse)"""
    o = ''
    for k in range(n):
        ph = math.asin(-.92 + 1.84 * (k + random.uniform(.2, .8)) / n)
        yc = cy + r * math.sin(ph) - r * math.cos(ph) * tilt * .3; hw = r * math.cos(ph); ry = hw * tilt
        dash = ' '.join(f'{random.uniform(60, 260):.0f} {random.uniform(20, 110):.0f}' for _ in range(3))
        o += (f'<path d="M{cx - hw:.0f} {yc:.0f} A{hw:.0f} {ry:.0f} 0 0 0 {cx + hw:.0f} {yc:.0f}" stroke="{col}" stroke-width="{random.uniform(wmin, wmax):.0f}" '
              f'fill="none" stroke-linecap="round" stroke-dasharray="{dash}" stroke-dashoffset="{random.uniform(0, 200):.0f}" opacity="{random.uniform(omin, omax):.2f}" filter="url(#bl3)"/>')
    return o


def person(x, y, h, col='#05070c', rim=None, robe=False):
    """small standing figure seen from behind (no face), feet at (x, y), height h"""
    k = h / 100
    o = f'<g transform="translate({x} {y}) scale({k:.3f})" fill="{col}">'
    o += '<ellipse cx="0" cy="-88" rx="9" ry="10"/>'
    if robe:   # hooded long coat, wind-blown hem
        o += '<path d="M-13 -80 Q-15 -104 0 -106 Q15 -104 13 -80Z"/>'
        o += '<path d="M-14 -78 Q0 -82 14 -78 L18 -30 L26 -2 Q8 2 0 -1 Q-10 2 -20 -2 L-17 -30Z"/>'
        o += '<path d="M-14 -76 L-21 -40 L-16 -39 L-10 -66Z M14 -76 L21 -40 L16 -39 L10 -66Z"/>'
        o += '<path d="M-9 -2 L-9 2 L-2 2 L-2 -2Z M3 -2 L3 2 L10 2 L10 -2Z"/>'
    else:
        o += '<path d="M-13 -76 Q0 -80 13 -76 L16 -40 Q0 -36 -16 -40Z"/>'
        o += '<path d="M-15 -74 L-21 -38 L-16 -37 L-10 -66Z M15 -74 L21 -38 L16 -37 L10 -66Z"/>'
        o += '<path d="M-13 -42 L-11 0 L-3 0 L-1 -36 L1 -36 L3 0 L11 0 L13 -42Z"/>'
    if rim:
        o += f'<path d="M9 -96 Q13 -88 9 -80 M14 -76 L18 -30 L26 -2" stroke="{rim}" stroke-width="2.6" fill="none" opacity=".95"/>'
    return o + '</g>'


def astronaut(x, y, h, col='#0b0d12', rim='#cfe6ff'):
    """tiny spacesuit figure from behind, feet at (x, y)"""
    k = h / 100
    o = f'<g transform="translate({x} {y}) scale({k:.3f})" fill="{col}">'
    o += '<circle cx="0" cy="-84" r="15"/><rect x="-20" y="-72" width="40" height="40" rx="12"/>'
    o += '<rect x="-17" y="-80" width="34" height="34" rx="6" opacity=".9"/>'   # backpack
    o += '<path d="M-20 -66 L-28 -36 L-21 -34 L-14 -58Z M20 -66 L28 -36 L21 -34 L14 -58Z"/>'
    o += '<path d="M-17 -36 L-15 0 L-4 0 L-2 -28 L2 -28 L4 0 L15 0 L17 -36Z"/>'
    o += '</g>'
    o += (f'<path transform="translate({x} {y}) scale({k:.3f})" d="M15 -97 Q24 -86 16 -72 M20 -66 L28 -36 M17 -36 L15 0" '
          f'stroke="{rim}" stroke-width="3" fill="none" opacity=".9"/>')
    return o


# ======================= A: 7 WORLDS, ONE STAR  (homage: Star Wars binary-sunset hill -> TRAPPIST-1e sky) =======================
random.seed(5)
SX, SY, SR = 1170, 738, 165          # ruddy red-dwarf sun, low on the horizon
PX, PY, PR = 1530, 452, 205          # big neighbouring world rising, "larger than the full Moon looks"
HZ = 770
d = lin('skyA', [(0, '#1c0b2e'), (.35, '#4a1a46'), (.62, '#a8424a'), (.8, '#e8783e'), (1, '#ffb45a')])
d += rad('sunGa', SX, SY, 900, [(0, '#ffb070', .75), (.25, '#ff6a3a', .35), (.6, '#a8304a', .12), (1, '#000', 0)])
d += rad('sunD', SX - 30, SY - 30, SR * 1.05, [(0, '#fff3d8', 1), (.5, '#ffb070', 1), (.85, '#ff6a32', 1), (1, '#e04a2a', 1)])
d += rad('ocA', PX - 70, PY + 60, PR * 1.25, [(0, '#5ac8d0', 1), (.45, '#2a7a9a', 1), (1, '#0e2a4a', 1)])
d += lin('mesa1', [(0, '#b0524e'), (1, '#7a3048')])
d += lin('mesa2', [(0, '#6a2640'), (1, '#3e1530')])
d += lin('grA', [(0, '#3a1428'), (1, '#12060e')])
d += lin('ridge', [(0, '#1a0812'), (1, '#060205')])
d += FX
d += f'<clipPath id="cpA"><circle cx="{PX}" cy="{PY}" r="{PR}"/></clipPath>'
sd, sov = shade('shA', PX, PY, PR, -.18, 150, '#12081e', .9, 22)
d += sd
b = '<rect width="1920" height="1080" fill="url(#skyA)"/>'
b += stars(160, 420, 0, '#ffe8f0', .55, 0)
b += '<rect width="1920" height="1080" fill="url(#sunGa)"/>'
# thin high clouds streaked across the sky, lit from below
for k in range(9):
    y = random.uniform(300, 640); x = random.uniform(500, 1900); w = random.uniform(220, 520)
    b += f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{w:.0f}" ry="{random.uniform(5, 12):.0f}" fill="#ffb08a" opacity="{random.uniform(.12, .28):.2f}" filter="url(#bl3)"/>'
# five more sister worlds of the system, small, all lit from the low sun (lower left of each)
sis = [(1810, 150, 52, -.35), (1240, 250, 34, .1), (1700, 760 - 120, 0, 0), (1400, 110, 22, .4), (1880, 380, 26, -.1), (880, 330, 16, .3)]
sis = [s for s in sis if s[2] > 0]
for i, (x, y, r, t) in enumerate(sis):
    ang = math.degrees(math.atan2(SY - y, SX - x))
    col = random.choice(['#e8b88a', '#bcd8e0', '#d89a7a', '#f0d8b0', '#a8c0d8'])
    sdd, sovv = shade(f'sis{i}', x, y, r, t, ang, '#1a0a24', .92, max(2, r / 10))
    d += sdd
    b += f'<circle cx="{x}" cy="{y}" r="{r * 1.9:.0f}" fill="{col}" opacity=".16" filter="url(#bl)"/>'
    b += f'<circle cx="{x}" cy="{y}" r="{r}" fill="{col}"/>'
    for _ in range(4):
        b += f'<ellipse cx="{x + random.uniform(-.5, .5) * r:.0f}" cy="{y + random.uniform(-.5, .5) * r:.0f}" rx="{r * random.uniform(.2, .45):.0f}" ry="{r * .12:.0f}" fill="#fff" opacity=".3"/>'
    b += sovv
# --- the big neighbouring world: ocean, continents, cloud bands, ice cap ---
b += f'<circle cx="{PX}" cy="{PY}" r="{PR + 60}" fill="#7ad8ff" opacity=".22" filter="url(#bl2)"/>'
P = f'<g clip-path="url(#cpA)"><circle cx="{PX}" cy="{PY}" r="{PR}" fill="url(#ocA)"/>'
for k in range(7):   # continents
    cx_ = PX + random.uniform(-.75, .6) * PR; cy_ = PY + random.uniform(-.55, .7) * PR
    pts = []
    n = 11; rr = random.uniform(.16, .3) * PR
    for j in range(n):
        a = j / n * 6.283; q = rr * random.uniform(.55, 1.25)
        pts.append((cx_ + math.cos(a) * q * 1.4, cy_ + math.sin(a) * q * .8))
    pth = 'M' + ' '.join(f'{(pts[j][0] + pts[(j + 1) % n][0]) / 2:.0f} {(pts[j][1] + pts[(j + 1) % n][1]) / 2:.0f} Q{pts[(j + 1) % n][0]:.0f} {pts[(j + 1) % n][1]:.0f}' for j in range(n)) + 'Z'
    pth = pth.replace('M', 'M', 1)
    P += f'<path d="M{(pts[0][0] + pts[1][0]) / 2:.0f} {(pts[0][1] + pts[1][1]) / 2:.0f} ' + ' '.join(f'Q{pts[(j + 1) % n][0]:.0f} {pts[(j + 1) % n][1]:.0f} {(pts[(j + 1) % n][0] + pts[(j + 2) % n][0]) / 2:.0f} {(pts[(j + 1) % n][1] + pts[(j + 2) % n][1]) / 2:.0f}' for j in range(n)) + 'Z" fill="{}" opacity=".95"/>'.format(random.choice(['#6a8a4a', '#8a7a4a', '#4a7a4a', '#a8864e']))
P += bands(PX, PY, PR, 14, '#fff', .2, 10, 24, .3, .6) + bands(PX, PY, PR, 10, '#fff', .2, 3, 6, .5, .85)
for _ in range(0):  # cyclone spirals (dropped: read as doodles)
    cx_ = PX + random.uniform(-.6, .4) * PR; cy_ = PY + random.uniform(-.4, .6) * PR; s = random.uniform(14, 26)
    P += f'<path d="M{cx_:.0f} {cy_:.0f} m{-s} 0 a{s} {s * .7:.0f} 0 1 1 {s * 1.4:.0f} {s * .5:.0f} a{s * .6:.0f} {s * .4:.0f} 0 1 1 {-s * .8:.0f} {-s * .4:.0f}" stroke="#fff" stroke-width="5" fill="none" opacity=".7"/>'
P += f'<ellipse cx="{PX + 30}" cy="{PY - PR + 18}" rx="{PR * .55:.0f}" ry="44" fill="#f4fbff" opacity=".9" filter="url(#bl3)"/>'  # ice cap
P += sov
P += f'<ellipse cx="{PX - PR * .45:.0f}" cy="{PY + PR * .35:.0f}" rx="{PR * .5:.0f}" ry="{PR * .35:.0f}" fill="#ffd8a8" opacity=".22" filter="url(#bl2)"/>'  # warm sun glint
P += '</g>'
b += P
b += f'<path d="{term_arc(PX, PY, PR, 1)}" transform="rotate(150 {PX} {PY})" stroke="#ffcf9a" stroke-width="7" fill="none" opacity=".75" filter="url(#bl3)"/>'
b += f'<circle cx="{PX}" cy="{PY}" r="{PR}" fill="none" stroke="#9ae6ff" stroke-width="3" opacity=".35"/>'
# --- the ruddy sun, low, half behind the far mesas, heat shimmer ---
b += f'<circle cx="{SX}" cy="{SY}" r="{SR * 2.2:.0f}" fill="#ff7a3a" opacity=".45" filter="url(#bl5)"/>'
b += f'<circle cx="{SX}" cy="{SY}" r="{SR + 26}" fill="#ffb070" opacity=".55" filter="url(#bl2)"/>'
b += f'<circle cx="{SX}" cy="{SY}" r="{SR}" fill="url(#sunD)"/>'
for _ in range(14):   # star spots and granulation
    a = random.uniform(0, 6.28); q = random.uniform(.1, .8) * SR
    b += f'<circle cx="{SX + math.cos(a) * q:.0f}" cy="{SY + math.sin(a) * q:.0f}" r="{random.uniform(4, 13):.0f}" fill="#d8502a" opacity="{random.uniform(.15, .35):.2f}" filter="url(#bl3)"/>'
b += f'<path d="M{SX - SR - 30} {SY - 42} h{SR * 2 + 60}" stroke="#7a2a3a" stroke-width="5" opacity=".2"/><path d="M{SX - SR - 60} {SY - 12} h{SR * 2 + 120}" stroke="#7a2a3a" stroke-width="8" opacity=".18"/>'
# --- far mesas (hazy), middle mesas, plain ---
def ridge_line(y0, amp, step, x0=-20, x1=1960):
    pts = []; x = x0; y = y0
    while x < x1:
        if random.random() < .11:   # flat-topped butte
            w = random.uniform(80, 220); h = random.uniform(.6, 1) * amp
            pts += [(x, y0 - h * .15), (x + random.uniform(8, 30), y0 - h * random.uniform(.85, 1))]
            for j in range(3): pts.append((x + w * (j + 1) / 4, y0 - h * random.uniform(.88, 1.02)))
            pts += [(x + w - random.uniform(8, 30), y0 - h * random.uniform(.8, .95)), (x + w, y0 - h * .1)]; x += w
        else:
            pts.append((x, y0 - random.uniform(0, amp * .25))); x += step
    return pts
for layer, (y0, amp, fill, op) in enumerate([(HZ - 4, 70, 'url(#mesa1)', .85), (HZ + 26, 110, 'url(#mesa2)', 1)]):
    pts = ridge_line(y0, amp, 40)
    b += '<path d="M-20 1080 L' + ' L'.join(f'{x:.0f} {y:.0f}' for x, y in pts) + ' L1960 1080Z" fill="' + fill + f'" opacity="{op}"/>'
    # rim light on the mesa tops facing the sun
    b += '<path d="M' + ' L'.join(f'{x:.0f} {y:.0f}' for x, y in pts) + f'" stroke="#ffb07a" stroke-width="{3 - layer}" fill="none" opacity="{.6 - layer * .2:.2f}"/>'
b += f'<rect x="0" y="{HZ + 40}" width="1920" height="{1080 - HZ - 40}" fill="url(#grA)"/>'
# sun reflection on a dark glass-like plain (volcanic glass shore, S42)
for k in range(22):
    y = HZ + 52 + k * 11; w = (190 - k * 6) * random.uniform(.7, 1.2)
    b += f'<path d="M{SX - w / 2:.0f} {y} h{w:.0f}" stroke="#ff9a5a" stroke-width="{4 - k * .12:.1f}" opacity="{.6 - k * .025:.2f}"/>'
# --- foreground hill / ridge where the lone figure stands ---
ridge = 'M-20 1080 L-20 820 C200 800 380 790 520 822 C600 838 660 846 760 850 C900 856 1000 900 1120 960 C1240 1020 1300 1080 1300 1080Z'
b += f'<path d="{ridge}" fill="url(#ridge)"/>'
b += '<path d="M-20 820 C200 800 380 790 520 822 C600 838 660 846 760 850 C900 856 1000 900 1120 960" stroke="#ff9a5a" stroke-width="4" fill="none" opacity=".75"/>'
for _ in range(26):   # rocks / pebbles on the ridge with rim light
    x = random.uniform(40, 1050); y = 860 + random.uniform(10, 200) + max(0, (x - 760)) * .2
    r = random.uniform(6, 22)
    b += f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{r:.0f}" ry="{r * .55:.0f}" fill="#1c0a14"/><path d="M{x - r * .3:.0f} {y - r * .5:.0f} q{r * .6:.0f} -2 {r:.0f} {r * .3:.0f}" stroke="#ff9a5a" stroke-width="2" fill="none" opacity=".55"/>'
# the lone figure (hooded coat, from behind), long shadow toward the viewer-left
b += '<path d="M680 848 L380 900 L400 908 L690 852Z" fill="#000" opacity=".35"/>'
b += person(690, 852, 230, '#0a0408', '#ffb07a', robe=True)
b += spark(1640, 220, 22, '#fff6d6') + spark(980, 560, 14, '#ffe0c0') + spark(1880, 560, 16, '#fff0e0')
open('A.html', 'w', encoding='utf-8').write(page('#1c0b2e', svg(d, b), [('<span class="g">7</span> WORLDS,', 190, 'w'), ('ONE STAR', 150, 'w')], '#14061e', top=56))


# ======================= B: NO SUNSET, EVER  (intuitive: tidally locked world, blazing day / frozen night, twilight ring) =======================
random.seed(17)
CX, CY, R = 1250, 620, 375
ANG = -24            # light comes from the upper right
T = -.30             # terminator offset: we see a bit more day than night
STX, STY = 1960, 300
d = lin('bgB', [(0, '#0a0a26'), (.55, '#1a1238'), (1, '#07061a')], 1, 0)
d += rad('starGB', STX, STY, 1100, [(0, '#fff2d0', .95), (.12, '#ff9a4a', .65), (.4, '#c8402a', .25), (1, '#000', 0)])
d += rad('dayB', CX + 230, CY - 120, R * 1.25, [(0, '#fff6dc', 1), (.18, '#ffd27a', 1), (.5, '#e8823a', 1), (.85, '#9a3a22', 1), (1, '#5a1e1a', 1)])
d += FX
d += f'<clipPath id="cpB"><circle cx="{CX}" cy="{CY}" r="{R}"/></clipPath>'
sd, sov = shade('shB', CX, CY, R, T, ANG, '#06112a', .97, 5)
d += sd
# mask for night-side detail: only the dark part
d += (f'<mask id="nightM" maskUnits="userSpaceOnUse" x="0" y="0" width="1920" height="1080"><circle cx="{CX}" cy="{CY}" r="{R}" fill="#fff"/>'
      f'<path d="{lit_path(CX, CY, R, T)}" fill="#000" transform="rotate({ANG} {CX} {CY})"/></mask>')
b = '<rect width="1920" height="1080" fill="url(#bgB)"/>' + stars(260, 1060, 0, '#dfe8ff', .65, 0)
b += '<rect width="1920" height="1080" fill="url(#starGB)"/>'
# the star (mostly off-frame right): corona rays
for k in range(26):
    a = math.radians(140 + k * 80 / 26 + random.uniform(-1, 1))
    L = random.uniform(500, 1000)
    b += f'<path d="M{STX} {STY} L{STX + math.cos(a) * L:.0f} {STY + math.sin(a) * L:.0f}" stroke="#ffcf8a" stroke-width="{random.uniform(2, 6):.0f}" opacity="{random.uniform(.05, .15):.2f}"/>'
b += f'<circle cx="{STX}" cy="{STY}" r="190" fill="#ffd9a0" opacity=".9" filter="url(#bl2)"/><circle cx="{STX}" cy="{STY}" r="130" fill="#fff6e0"/>'
# hot glow around the day limb
b += f'<circle cx="{CX + 40}" cy="{CY - 20}" r="{R + 70}" fill="#ff8a3a" opacity=".35" filter="url(#bl5)"/>'
P = f'<g clip-path="url(#cpB)"><circle cx="{CX}" cy="{CY}" r="{R}" fill="url(#dayB)"/>'
# day side: scorched cracked plains, dark lava fields, bright sub-stellar spot
for _ in range(55):
    x = CX + random.uniform(-.2, 1) * R; y = CY + random.uniform(-1, 1) * R
    P += f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{random.uniform(14, 60):.0f}" ry="{random.uniform(6, 26):.0f}" fill="{random.choice(["#7a2a1a", "#9a3a1e", "#5a1a14"])}" opacity="{random.uniform(.18, .4):.2f}" transform="rotate({random.uniform(-40, 40):.0f} {x:.0f} {y:.0f})" filter="url(#bl3)"/>'
for _ in range(34):   # cracks
    x = CX + random.uniform(-.1, .95) * R; y = CY + random.uniform(-.95, .95) * R
    dd = f'M{x:.0f} {y:.0f}'
    for j in range(4):
        x += random.uniform(-26, 26); y += random.uniform(-26, 26); dd += f' L{x:.0f} {y:.0f}'
    P += f'<path d="{dd}" stroke="#5a1a10" stroke-width="{random.uniform(1.2, 2.4):.1f}" fill="none" opacity=".4"/>'
for _ in range(9):    # craters
    x = CX + random.uniform(0, .8) * R; y = CY + random.uniform(-.7, .8) * R; r = random.uniform(12, 30)
    P += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r:.0f}" fill="#6a2416" opacity=".45"/><path d="M{x - r:.0f} {y:.0f} a{r:.0f} {r:.0f} 0 0 1 {2 * r:.0f} 0" stroke="#ffe0a0" stroke-width="3" fill="none" opacity=".5"/>'
P += f'<circle cx="{CX + 210}" cy="{CY - 110}" r="120" fill="#fffbe8" opacity=".55" filter="url(#bl2)"/>'
P += sov
# night side: ice sheets, glacier cracks catching starlight
N = '<g mask="url(#nightM)">'
for _ in range(40):
    x = CX + random.uniform(-1, .2) * R; y = CY + random.uniform(-1, 1) * R
    N += f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{random.uniform(20, 90):.0f}" ry="{random.uniform(8, 30):.0f}" fill="{random.choice(["#2a4a7a", "#3a6a9a", "#1a3060"])}" opacity="{random.uniform(.25, .55):.2f}" transform="rotate({random.uniform(-30, 30):.0f} {x:.0f} {y:.0f})"/>'
for _ in range(60):
    x = CX + random.uniform(-.95, .1) * R; y = CY + random.uniform(-.95, .95) * R
    dd = f'M{x:.0f} {y:.0f}'
    for j in range(3):
        x += random.uniform(-34, 34); y += random.uniform(-18, 18); dd += f' L{x:.0f} {y:.0f}'
    N += f'<path d="{dd}" stroke="#9ad0ff" stroke-width="{random.uniform(1, 2.6):.1f}" fill="none" opacity="{random.uniform(.2, .5):.2f}"/>'
N += f'<ellipse cx="{CX - R * .55:.0f}" cy="{CY - R * .55:.0f}" rx="150" ry="90" fill="#bfe4ff" opacity=".18" filter="url(#bl2)"/>'
N += '</g>'
P += N
# the twilight ring: golden band along the terminator, a thin strip of sea and green, clouds where the winds meet
ta = f'transform="rotate({ANG} {CX} {CY})"'
P += f'<path d="{term_arc(CX, CY, R, T)}" {ta} stroke="#ffb04a" stroke-width="90" fill="none" opacity=".45" filter="url(#bl2)"/>'
P += f'<path d="{term_arc(CX, CY, R, T)}" {ta} stroke="#f2d27a" stroke-width="34" fill="none" opacity=".75" filter="url(#bl)"/>'
P += f'<path d="{term_arc(CX, CY, R, T - .06)}" {ta} stroke="#1f7a8a" stroke-width="20" fill="none" opacity=".9"/>'
P += f'<path d="{term_arc(CX, CY, R, T - .025)}" {ta} stroke="#4ab86a" stroke-width="9" fill="none" opacity=".85"/>'
# clouds along the ring
rx_ = abs(T) * R
for k in range(46):
    th = math.radians(90 + k * 180 / 45)          # left half of the terminator ellipse (local coords)
    lx = CX + math.cos(th) * rx_ + random.uniform(-14, 14); ly = CY + math.sin(th) * R * .985
    a = math.radians(ANG); gx = CX + (lx - CX) * math.cos(a) - (ly - CY) * math.sin(a); gy = CY + (lx - CX) * math.sin(a) + (ly - CY) * math.cos(a)
    s = random.uniform(6, 30)
    if random.random() < .45: continue
    rot = ANG + math.degrees(th) - 90 + random.uniform(-25, 25)
    P += f'<ellipse cx="{gx:.0f}" cy="{gy:.0f}" rx="{s * 2.2:.0f}" ry="{s * .45:.0f}" fill="#fff4e0" opacity="{random.uniform(.3, .7):.2f}" transform="rotate({rot:.0f} {gx:.0f} {gy:.0f})" filter="url(#bl3)"/>'
    if random.random() < 0:   # small storm swirl (dropped: read as doodles) where warm and cold winds collide
        P += f'<path d="M{gx - s:.0f} {gy:.0f} a{s:.0f} {s * .6:.0f} 0 1 1 {s * 1.4:.0f} {s * .4:.0f} a{s * .5:.0f} {s * .35:.0f} 0 1 1 {-s * .7:.0f} {-s * .3:.0f}" stroke="#fffaf0" stroke-width="3" fill="none" opacity=".75"/>'
P += '</g>'
b += P
# atmospheric rims: hot orange on the day limb, thin cold blue on the night limb
b += f'<path d="M{CX} {CY - R} A{R} {R} 0 0 1 {CX} {CY + R}" transform="rotate({ANG} {CX} {CY})" stroke="#ffcf8a" stroke-width="9" fill="none" opacity=".85" filter="url(#bl3)"/>'
b += f'<path d="M{CX} {CY + R} A{R} {R} 0 0 1 {CX} {CY - R}" transform="rotate({ANG} {CX} {CY})" stroke="#6ab0ff" stroke-width="4" fill="none" opacity=".55"/>'
# glow where the ring meets the limb
for s in (-1, 1):
    a = math.radians(ANG + s * 90)
    gx, gy = CX + math.cos(a) * R, CY + math.sin(a) * R
    b += f'<circle cx="{gx:.0f}" cy="{gy:.0f}" r="60" fill="#f2d27a" opacity=".55" filter="url(#bl2)"/>' + spark(int(gx), int(gy), 30, '#fff6d6', .95)
# a small moon-like probe for scale on the night side
b += f'<g transform="translate(700 870) rotate(-18)"><rect x="-14" y="-9" width="28" height="18" rx="3" fill="#2a2e3a" stroke="#ffd9a0" stroke-width="2"/>'
b += '<rect x="-74" y="-6" width="54" height="12" fill="#1a3a6a" stroke="#9ad0ff" stroke-width="1.5"/><rect x="20" y="-6" width="54" height="12" fill="#1a3a6a" stroke="#9ad0ff" stroke-width="1.5"/>'
b += '<path d="M0 -9 V-24" stroke="#ffd9a0" stroke-width="2"/><circle cx="0" cy="-26" r="4" fill="#ffd9a0"/></g>'
b += spark(1650, 140, 20, '#fff6d6') + spark(520, 720, 14, '#cfe4ff') + spark(1720, 640, 16, '#ffe6c0')
open('B.html', 'w', encoding='utf-8').write(page('#0a0a26', svg(d, b), [('NO SUNSET,', 150, 'w'), ('EVER.', 240, 'y')], '#08061a', top=60))


# ======================= C: THERE IS NO PLANET B  (homage: Apollo 8 "Earthrise") =======================
random.seed(29)
EX, EY, ER = 1400, 420, 255
d = lin('bgC', [(0, '#020308'), (1, '#05060e')])
d += rad('ocC', EX - 80, EY - 70, ER * 1.3, [(0, '#7ad0ff', 1), (.35, '#2a7ad0', 1), (.75, '#0e3a8a', 1), (1, '#06204a', 1)])
d += lin('moonC', [(0, '#a8a49c'), (.25, '#6e6b66'), (.7, '#2e2d2c'), (1, '#0c0c0d')])
d += rad('mhl', 520, 760, 900, [(0, '#d8d2c4', .55), (.5, '#9a958a', .15), (1, '#000', 0)])
d += FX
d += f'<clipPath id="cpC"><circle cx="{EX}" cy="{EY}" r="{ER}"/></clipPath>'
sd, sov = shade('shC', EX, EY, ER, .02, 200, '#01030a', .96, 30)    # sun from the left: half-lit Earth like the photo
d += sd
b = '<rect width="1920" height="1080" fill="url(#bgC)"/>'
for _ in range(120):
    b += f'<circle cx="{random.uniform(0, 1920):.0f}" cy="{random.uniform(0, 700):.0f}" r="{random.choice([1, 1.4, 1.9])}" fill="#dfe8ff" opacity="{random.uniform(.15, .55):.2f}"/>'
# far away worlds: tiny, dim, out of reach (Proxima b red, TRAPPIST-1e rusty, Kepler-452b pale)
for x, y, r, col in [(1760, 150, 9, '#ff7a5a'), (1640, 300, 6, '#e8a070'), (1880, 470, 5, '#d8c8a0')]:
    b += f'<circle cx="{x}" cy="{y}" r="{r * 4}" fill="{col}" opacity=".18" filter="url(#bl)"/><circle cx="{x}" cy="{y}" r="{r}" fill="{col}"/><path d="M{x - r} {y} a{r} {r} 0 0 0 {r * 2} 0" fill="#000" opacity=".5"/>'
# Earth: atmosphere halo, oceans, continents, clouds, terminator
b += f'<circle cx="{EX}" cy="{EY}" r="{ER + 70}" fill="#3a9aff" opacity=".28" filter="url(#bl2)"/>'
E = f'<g clip-path="url(#cpC)"><circle cx="{EX}" cy="{EY}" r="{ER}" fill="url(#ocC)"/>'
lands = [  # rough Africa / Arabia / Europe hint, drawn freely
    'M-40 -150 C10 -175 70 -160 90 -120 C110 -90 150 -80 150 -40 C150 10 110 30 100 80 C90 130 60 180 30 200 C10 160 -10 120 -20 80 C-30 40 -80 30 -90 -10 C-100 -60 -80 -130 -40 -150Z',
    'M110 -130 C140 -150 190 -140 210 -100 C220 -70 200 -40 170 -50 C150 -60 140 -90 110 -130Z',
    'M-120 -200 C-80 -230 0 -230 40 -200 C10 -185 -40 -180 -60 -170 C-90 -160 -130 -170 -120 -200Z',
    'M-200 40 C-180 20 -150 30 -150 60 C-155 90 -190 100 -205 80Z']
for L in lands:
    E += f'<path d="{L}" transform="translate({EX - 90} {EY + 10}) rotate(-8)" fill="#8a7a4a" opacity=".95"/>'
    E += f'<path d="{L}" transform="translate({EX - 90} {EY + 10}) rotate(-8) scale(.82)" fill="#5a7a3a" opacity=".6"/>'
E += bands(EX, EY, ER, 12, '#fff', .22, 12, 26, .35, .7) + bands(EX, EY, ER, 9, '#fff', .22, 3, 7, .5, .9)
for _ in range(0):
    x = EX + random.uniform(-.6, .3) * ER; y = EY + random.uniform(-.5, .6) * ER; s = random.uniform(16, 26)
    E += f'<path d="M{x:.0f} {y:.0f} m{-s} 0 a{s} {s * .7:.0f} 0 1 1 {s * 1.4:.0f} {s * .5:.0f} a{s * .6:.0f} {s * .4:.0f} 0 1 1 {-s * .8:.0f} {-s * .4:.0f}" stroke="#fff" stroke-width="6" fill="none" opacity=".8"/>'
E += f'<ellipse cx="{EX - 40}" cy="{EY - ER + 20}" rx="120" ry="40" fill="#f4fbff" opacity=".85" filter="url(#bl3)"/>'
E += f'<circle cx="{EX - 110}" cy="{EY - 100}" r="70" fill="#e8f8ff" opacity=".25" filter="url(#bl2)"/>'   # sun glint
E += sov + '</g>'
b += E
b += f'<path d="M{EX} {EY + ER} A{ER} {ER} 0 0 1 {EX} {EY - ER}" transform="rotate(20 {EX} {EY})" stroke="#9ad8ff" stroke-width="7" fill="none" opacity=".8" filter="url(#bl3)"/>'
# lunar horizon: big curve, craters, rubble; lit from the left, falls into shadow on the right
HY = 700
moon = f'M-40 1080 L-40 {HY + 40} C300 {HY - 30} 800 {HY - 40} 1200 {HY + 10} C1500 {HY + 50} 1750 {HY + 120} 1960 {HY + 190} L1960 1080Z'
b += f'<path d="{moon}" fill="url(#moonC)"/>'
b += '<rect width="1920" height="1080" fill="url(#mhl)"/>'
b += f'<path d="M-40 {HY + 40} C300 {HY - 30} 800 {HY - 40} 1200 {HY + 10} C1500 {HY + 50} 1750 {HY + 120} 1960 {HY + 190}" stroke="#e8e2d4" stroke-width="4" fill="none" opacity=".7"/>'
craters = []
for _ in range(60):
    x = random.uniform(-20, 1500); ymin = HY + 30 + max(0, (x - 1100)) * .1
    y = random.uniform(ymin, 1060); r = random.uniform(10, 70) * (0.5 + (y - HY) / 500)
    craters.append((y, x, r))
for y, x, r in sorted(craters):
    if x > 1450 and y > 860: continue   # keep bottom-right calm
    ry = r * (.22 + (y - HY) / 1400)
    b += f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{r:.0f}" ry="{ry:.0f}" fill="#1a1918" opacity=".55"/>'
    b += f'<path d="M{x - r:.0f} {y:.0f} a{r:.0f} {ry:.0f} 0 0 0 {2 * r:.0f} 0" stroke="#d8d2c4" stroke-width="{max(1.5, r / 18):.1f}" fill="none" opacity=".55"/>'
    b += f'<path d="M{x - r:.0f} {y:.0f} a{r:.0f} {ry:.0f} 0 0 1 {r * 1.2:.0f} {-ry * .9:.0f}" stroke="#0a0a0a" stroke-width="{max(1.5, r / 14):.1f}" fill="none" opacity=".5"/>'
for _ in range(140):   # pebbles
    x = random.uniform(0, 1400); y = random.uniform(HY + 40, 1070); r = random.uniform(1.5, 5) * (y - HY) / 200
    b += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r:.1f}" fill="#c8c2b4" opacity="{random.uniform(.2, .5):.2f}"/>'
b += '<rect x="1500" y="860" width="420" height="220" fill="#000" opacity=".35" filter="url(#bl2)"/>'
# tiny astronaut on the rim, looking at home
b += '<path d="M770 702 L640 716 L642 722 L772 706Z" fill="#000" opacity=".45"/>'
b += astronaut(780, 704, 74, '#14161c', '#e8f0ff')
b += spark(1530, 230, 20, '#e6f4ff') + spark(990, 300, 14, '#e6f4ff')
open('C.html', 'w', encoding='utf-8').write(page('#020308', svg(d, b), [('THERE IS NO', 130, 'w'), ('PLANET B', 200, 'y')], '#02030a', top=60))
print('ok')
