# Shorts thumbnails (style B, guideline 16-9) for everest-tallest-mountain-short1..5. VERTICAL 1080x1920, glowing hero top half,
# centred hook y 860-1240 on a darkband, frog bottom corner.
# Run: python3 videos/everest-tallest-mountain-short1/thumb/make_all.py [1 2 3 4 5] -> videos/everest-tallest-mountain-shortN/thumb/A.html
# 1 3 RULERS, 3 WINNERS  moonlit Everest, a golden crown slipping off its summit, three glowing rulers around it; climber frog (short1 S01-S02)
# 2 10,210 M TALL        night cut-away: Mauna Kea summit domes above the sea, glowing rim of its hidden body down to the seafloor,
#                        hotspot plume below; diver frog (short2 S03-S07)
# 3 CLOSEST TO THE STARS Earth bulging at the equator, icy Chimborazo on the bulge, a golden beam from the centre to its summit; astronaut frog (short3 S01-S07)
# 4 DEEPER THAN EVEREST  Everest sinking into the dark Challenger Deep, summit still far below the surface; frog in a diving helmet (short4 S02-S03)
# 5 2.5x EVEREST         Mars from space, Olympus Mons on the limb next to a small Everest at the same scale; astronaut frog on red dunes (short5 S01)
import os, sys, math, random, shutil
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
sys.path.insert(0, os.path.join(REPO, 'tools'))
sys.path.insert(0, os.path.join(REPO, 'videos', 'trilobite-extinction', 'thumb'))
from make import frog, FILTERS, INK, GREEN
from thumb_lib import vpage, vsvg, lin, rad, spark, fireflies, halo, darkband

W, H = 1080, 1920
Y = '<span class="g">%s</span>'


def vig(id='vig', a=.8):
    return rad(id, 540, 900, 1250, [(0, '#000', 0), (.5, '#000', 0), (1, '#000', a)])


def stars(rnd, n, y0=0, y1=H, col='#e8f0ff', big=8):
    o = ''.join(f'<circle cx="{rnd.uniform(0, W):.0f}" cy="{rnd.uniform(y0, y1):.0f}" r="{rnd.choice([1.1, 1.6, 2.2])}" fill="{col}" opacity="{rnd.uniform(.25, .9):.2f}"/>' for _ in range(n))
    for _ in range(big):
        x, y = rnd.uniform(30, W - 30), rnd.uniform(y0 + 20, y1 - 20)
        o += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="9" fill="{col}" opacity=".25" filter="url(#b6)"/>' + spark(x, y, rnd.choice([10, 14, 18]), col='#f4f8ff', op=.8)
    return o


def PL(pts):
    return 'M' + ' L'.join(f'{x:.0f} {y:.0f}' for x, y in pts)


def mount_draw(pts, n, fill, line, w):
    return f'<path d="{P(pts)}" fill="{fill}"/><path d="{PL(pts[1:n + 2])}" fill="none" stroke="{line}" stroke-width="{w}" stroke-linejoin="round"/>'


def P(pts):
    return 'M' + ' L'.join(f'{x:.0f} {y:.0f}' for x, y in pts) + 'Z'


def ridge(rnd, x0, y0, x1, y1, n, j):
    pts = []
    for k in range(n + 1):
        t = k / n
        pts.append((x0 + (x1 - x0) * t + (rnd.uniform(-j, j) if 0 < k < n else 0), y0 + (y1 - y0) * t + (rnd.uniform(-j, j) if 0 < k < n else 0)))
    return pts


def peak(rnd, cx, top, base, half, lit='#eef6ff', shade='#5a6e9a', rock='#24304e', rockd='#151c33', snow=.55, line='#0a0f22'):
    """big snowy peak: left face in shadow, right face lit; snow above `snow` fraction of the height"""
    L = ridge(rnd, cx, top, cx - half, base, 9, 18); R = ridge(rnd, cx, top, cx + half, base, 9, 18)
    o = f'<path d="{P(L + R[::-1])}" fill="{rock}" stroke="{line}" stroke-width="5"/>'
    o += f'<path d="{P(R[::-1] + [(cx + 10, base)])}" fill="{rockd}" opacity=".0"/>'
    sy = top + (base - top) * snow
    # snow fields: lit right, shaded left, with jagged lower edge
    sl = [(cx, top)] + [p for p in L if p[1] < sy] + [(cx - half * (sy - top) / (base - top), sy)]
    edge = []
    for k in range(9):
        t = k / 8; x = cx - half * (sy - top) / (base - top) * (1 - t); edge.append((x, sy + (40 if k % 2 else -10) * rnd.uniform(.5, 1.2)))
    o += f'<path d="{P(sl + edge[1:] + [(cx + 6, sy - 60)])}" fill="{shade}" stroke="{line}" stroke-width="3.5"/>'
    sr = [(cx, top)] + [p for p in R if p[1] < sy] + [(cx + half * (sy - top) / (base - top), sy)]
    edge = []
    for k in range(9):
        t = k / 8; x = cx + half * (sy - top) / (base - top) * (1 - t); edge.append((x, sy + (50 if k % 2 else -8) * rnd.uniform(.5, 1.2)))
    o += f'<path d="{P(sr + edge[1:] + [(cx + 6, sy - 60)])}" fill="{lit}" stroke="{line}" stroke-width="3.5"/>'
    # couloirs / ridge lines
    for k in range(5):
        x = cx + rnd.uniform(-half * .45, half * .45); y = top + (base - top) * rnd.uniform(.25, .5)
        o += f'<path d="M{x:.0f} {y:.0f} l{rnd.uniform(-30, 30):.0f} {rnd.uniform(60, 140):.0f}" stroke="{line}" stroke-width="3" opacity=".45"/>'
    o += f'<path d="M{cx} {top} L{cx + 8} {top + (base - top) * .5}" stroke="#fff" stroke-width="4" opacity=".5"/>'
    return o


def limb_mount(cx, cy, rx, ry, a0, half, h, shape, n=40, inner=14, rnd=None, jag=0):
    """mountain profile standing on an ellipse limb: centre angle a0 (deg, screen coords), half-width `half` deg,
    radial height h * shape(t) for t in -1..1. Returns (outline points, summit point, fn(t, hh) -> point)."""
    def pt(t, hh):
        a = math.radians(a0 + half * t); nx, ny = math.cos(a), math.sin(a)
        return cx + rx * nx + hh * nx, cy + ry * ny + hh * ny
    out = [pt(-1, -inner)]
    for k in range(n + 1):
        t = -1 + 2 * k / n
        out.append(pt(t, h * shape(t) + (rnd.uniform(-jag, jag) if rnd and 0 < k < n else 0)))
    out += [pt(1 - 2 * k / n, -inner) for k in range(n + 1)]
    return out, pt(0, h * shape(0)), pt


def save(n, bg, d, b, lines, outline, top):
    out = os.path.join(REPO, 'videos', f'everest-tallest-mountain-short{n}', 'thumb'); os.makedirs(out, exist_ok=True)
    for f in ('common.css', 'Fredoka-700.woff2'):
        if not os.path.exists(os.path.join(out, f)):
            shutil.copy(os.path.join(REPO, 'tools', 'assets', 'thumb_v', f), out)
    open(os.path.join(out, 'A.html'), 'w').write(vpage(bg, vsvg(d, b), lines, outline=outline, top=top))


def ruler(x, y0, y1, col, w=34, rot=0):
    """glowing measuring stick, bottom y0 top y1"""
    h = y0 - y1
    o = f'<g transform="rotate({rot} {x} {y0})">'
    o += f'<rect x="{x - w}" y="{y1 - 10}" width="{w * 2}" height="{h + 20}" rx="10" fill="{col}" opacity=".35" filter="url(#b12)"/>'
    o += f'<rect x="{x - w / 2}" y="{y1}" width="{w}" height="{h}" rx="6" fill="{col}" stroke="#0a0f22" stroke-width="4"/>'
    o += f'<rect x="{x - w / 2 + 4}" y="{y1 + 4}" width="6" height="{h - 8}" rx="3" fill="#fff" opacity=".55"/>'
    k = 0; yy = y0 - 12
    while yy > y1 + 8:
        o += f'<path d="M{x + w / 2} {yy:.0f} l{-(w * .6 if k % 5 == 0 else w * .3):.0f} 0" stroke="#0a0f22" stroke-width="3"/>'
        yy -= 18; k += 1
    return o + '</g>'


# ================= 1: 3 RULERS, 3 WINNERS =================
def make_1():
    rnd = random.Random(11)
    d = FILTERS + vig() + lin('sky', [(0, '#050a22'), (.45, '#13204e'), (1, '#24346e')])
    d += halo('h1', 540, 420, 560, '#fff6c8', '#8fb4ff') + rad('moon', 820, 230, 260, [(0, '#f4f8ff', .9), (.3, '#a8c4ff', .3), (1, '#a8c4ff', 0)])
    b = f'<rect width="{W}" height="{H}" fill="url(#sky)"/>' + stars(rnd, 140, 0, 900, big=6)
    b += f'<rect width="{W}" height="{H}" fill="url(#moon)"/><circle cx="820" cy="230" r="58" fill="#f4f8ff"/><circle cx="800" cy="215" r="12" fill="#d0dcf0"/><circle cx="838" cy="248" r="9" fill="#d0dcf0"/>'
    b += f'<ellipse cx="540" cy="460" rx="620" ry="520" fill="url(#h1)"/>'
    # distant ranges
    b += f'<path d="{P(ridge(rnd, -20, 760, 1100, 700, 14, 40) + [(1100, 1920), (-20, 1920)])}" fill="#1a2550"/>'
    # three glowing rulers behind / beside the mountain (sea level, true base, centre of the planet)
    b += ruler(150, 860, 330, '#62e6ff', rot=-6) + ruler(930, 860, 290, '#ff8ad0', rot=6)
    b += ruler(540, 900, 150, '#ffd54a', w=30)
    # Everest
    b += peak(rnd, 540, 300, 860, 480)
    # snow plume blowing right from the summit
    for k in range(6):
        b += f'<ellipse cx="{620 + k * 60}" cy="{300 + k * 8}" rx="{70 + k * 20}" ry="{18 + k * 4}" fill="#f4f8ff" opacity="{.5 - k * .07:.2f}" filter="url(#b12)"/>'
    # glacier foreground + clouds below the peak
    b += f'<path d="M-20 820 q200 -60 420 -10 q170 30 340 -16 q200 -40 360 10 L1100 1920 L-20 1920z" fill="#0e1636"/>'
    for k in range(9):
        b += f'<ellipse cx="{rnd.uniform(0, W):.0f}" cy="{rnd.uniform(780, 860):.0f}" rx="{rnd.uniform(120, 220):.0f}" ry="30" fill="#c8d8ff" opacity=".22" filter="url(#b24)"/>'
    # golden crown slipping off the summit
    CX, CY = 600, 228
    b += f'<ellipse cx="{CX}" cy="{CY}" rx="150" ry="110" fill="#ffd54a" opacity=".35" filter="url(#b24)"/>'
    crown = ('<path d="M-70 30 L-80 -40 L-38 -6 L0 -60 L38 -6 L80 -40 L70 30Z" fill="#ffcf3a" stroke="#3a2406" stroke-width="6"/>'
             '<rect x="-74" y="22" width="148" height="24" rx="6" fill="#f2b21e" stroke="#3a2406" stroke-width="6"/>'
             '<circle cx="0" cy="34" r="8" fill="#ff4f6a" stroke="#3a2406" stroke-width="3"/><circle cx="-42" cy="34" r="6" fill="#5ad0ff" stroke="#3a2406" stroke-width="3"/><circle cx="42" cy="34" r="6" fill="#5ad0ff" stroke="#3a2406" stroke-width="3"/>'
             '<circle cx="-80" cy="-44" r="8" fill="#fff2a8" stroke="#3a2406" stroke-width="3"/><circle cx="0" cy="-64" r="8" fill="#fff2a8" stroke="#3a2406" stroke-width="3"/><circle cx="80" cy="-44" r="8" fill="#fff2a8" stroke="#3a2406" stroke-width="3"/>'
             '<path d="M-56 18 L-62 -22 M-10 14 L0 -40" stroke="#fff6c8" stroke-width="5" opacity=".7"/>')
    b += f'<g transform="translate({CX} {CY}) rotate(24)">{crown}</g>'
    for k, (dx, dy) in enumerate(((-120, 40), (-150, 70), (-175, 105))):
        b += f'<path d="M{CX + dx} {CY + dy} q-20 6 -36 22" stroke="#fff6c8" stroke-width="5" fill="none" opacity="{.7 - k * .2:.2f}"/>'
    for sx, sy, ss in ((420, 170, 22), (760, 150, 18), (300, 420, 16), (860, 500, 20), (690, 340, 14)):
        b += spark(sx, sy, ss, col='#fffbe0')
    b += fireflies(26, 120, 800, col='#dfe8ff', core='#ffffff', seed=3)
    b += darkband(850, 1250, .5)
    # climber frog (wool hat, goggles on the forehead, little rope) bottom left
    FX, FY = 270, 1720
    b += f'<ellipse cx="{FX}" cy="{FY - 120}" rx="230" ry="190" fill="#9fc0ff" opacity=".16" filter="url(#b24)"/>'
    b += f'<path d="M0 1700 q280 -50 560 0 q260 40 540 -10 L1100 1940 L-20 1940z" fill="#dfe8ff" opacity=".9"/><path d="M0 1700 q280 -50 560 0 q260 40 540 -10" stroke="#9fb4e6" stroke-width="6" fill="none"/>'
    hat = ('<path d="M-30 -84 q36 -50 72 0z" fill="#e2483e" stroke-width="3.4"/><path d="M-32 -86 q38 -10 76 0 l0 10 q-38 -10 -76 0z" fill="#f2f2f2" stroke-width="3"/>'
           '<circle cx="6" cy="-128" r="10" fill="#f2f2f2" stroke-width="3"/>')
    axe = ('<g transform="translate(66 -40) rotate(-18)"><path d="M0 0 L0 -90" stroke="#5a3a1a" stroke-width="7"/>'
           '<path d="M-26 -88 q26 -12 44 4 l-6 6 q-16 -8 -38 -2z" fill="#c9d2e0" stroke-width="3"/></g>')
    b += frog(FX, FY, 3.3, rot=-4, look=(3, -4), mouth='O', shadow=True, back=axe, front=hat,
              armL='M-34 -22 q-14 6 -16 22', armR='M38 -22 q22 -8 26 -24')
    b += f'<rect width="{W}" height="{H}" fill="url(#vig)"/>'
    save(1, '#050a22', d, b, [('3 RULERS,', 170, 'w'), ('3 ' + Y % 'WINNERS', 170, 'w')], '#060a1c', 880)


# ================= 2: 10,210 M TALL =================
def make_2():
    rnd = random.Random(22)
    WL = 470
    d = FILTERS + vig() + lin('sky', [(0, '#060824'), (1, '#1d2a5e')]) + lin('sea', [(0, '#0f4a72'), (.4, '#0a2c4c'), (1, '#030a18')])
    d += halo('h2', 540, 330, 480, '#fff2c0', '#7fd8ff') + rad('plume', 540, 1900, 700, [(0, '#ffd27a', .95), (.3, '#ff6a2a', .55), (1, '#ff3a1a', 0)])
    d += lin('rock', [(0, '#5a4a6e'), (.5, '#33284a'), (1, '#1a1020')])
    b = f'<rect width="{W}" height="{WL}" fill="url(#sky)"/>' + stars(rnd, 120, 0, WL - 60, big=5)
    # milky way band
    b += f'<path d="M-40 120 Q540 40 1120 300" stroke="#c8d0ff" stroke-width="120" opacity=".12" filter="url(#b24)" fill="none"/>'
    b += f'<ellipse cx="540" cy="330" rx="520" ry="300" fill="url(#h2)"/>'
    b += f'<rect y="{WL}" width="{W}" height="{H - WL}" fill="url(#sea)"/>'
    # Mauna Kea: broad shield; summit above water, huge body below
    SX, ST = 540, 300
    body = f'M{SX - 150} {ST + 40} Q{SX} {ST - 30} {SX + 150} {ST + 40} L{SX + 260} {WL} Q{SX + 420} 900 {SX + 600} 1560 L{SX - 600} 1560 Q{SX - 420} 900 {SX - 260} {WL}Z'
    b += f'<path d="{body}" fill="url(#rock)" stroke="#7fe0ff" stroke-width="7" opacity=".95"/>'
    b += f'<path d="{body}" fill="none" stroke="#7fe0ff" stroke-width="26" opacity=".25" filter="url(#b12)"/>'
    # lava layers (shield built layer after layer)
    for k in range(1, 9):
        y = WL + k * 120; hw = 260 + (y - WL) * .52
        b += f'<path d="M{SX - hw:.0f} {y} q{hw:.0f} -30 {2 * hw:.0f} 0" stroke="#ff9a5a" stroke-width="4" fill="none" opacity="{.5 - k * .03:.2f}"/>'
    # above-water lit cap (sunset rim) and observatory domes
    b += f'<path d="M{SX - 150} {ST + 40} Q{SX} {ST - 30} {SX + 150} {ST + 40} L{SX + 260} {WL} L{SX - 260} {WL}Z" fill="#4a3a5a" stroke="#0a0f22" stroke-width="5"/>'
    b += f'<path d="M{SX + 20} {ST + 6} Q{SX + 120} {ST + 20} {SX + 150} {ST + 40} L{SX + 260} {WL} L{SX + 120} {WL}Z" fill="#c07a6a" opacity=".55"/>'
    for dx, r in ((-70, 34), (10, 44), (90, 30)):
        x = SX + dx; y = ST + 8 + abs(dx) * .18
        b += f'<path d="M{x - r} {y} a{r} {r} 0 0 1 {2 * r} 0z" fill="#eef2ff" stroke="#0a0f22" stroke-width="4"/><rect x="{x - r}" y="{y}" width="{2 * r}" height="12" fill="#c8d0e8" stroke="#0a0f22" stroke-width="4"/>'
        b += f'<path d="M{x - 4} {y - r + 4} l0 {r - 6} l8 0 l0 {-(r - 6)}z" fill="#ffe28a"/>'
    b += f'<path d="M{SX + 10} {ST - 34} L{SX + 210} 40" stroke="#ffe28a" stroke-width="5" opacity=".7"/><path d="M{SX + 10} {ST - 34} L{SX + 210} 40" stroke="#ffe28a" stroke-width="18" opacity=".25" filter="url(#b6)"/>'
    # water surface line + shimmer
    b += f'<path d="M0 {WL} L{W} {WL}" stroke="#bff0ff" stroke-width="5" opacity=".8"/>'
    for _ in range(26):
        y = rnd.uniform(WL + 10, WL + 260); b += f'<path d="M{rnd.uniform(-40, W):.0f} {y:.0f} l{rnd.uniform(30, 90):.0f} 0" stroke="#9fe6ff" stroke-width="3" opacity=".25"/>'
    # seafloor + hotspot plume below
    b += f'<path d="M0 1560 L{W} 1560 L{W} {H} L0 {H}z" fill="#1a1012"/>'
    b += f'<rect width="{W}" height="{H}" fill="url(#plume)" opacity=".9"/>'
    b += f'<path d="M470 {H} Q500 1700 520 1560 L560 1560 Q580 1700 610 {H}z" fill="#ffb24a" opacity=".85" filter="url(#b6)"/>'
    b += f'<path d="M0 1560 L{W} 1560" stroke="#3a2a2a" stroke-width="8"/>'
    b += f'<path d="M520 1560 Q500 1300 540 1000" stroke="#ff8a3a" stroke-width="18" fill="none" opacity=".55" filter="url(#b6)"/><path d="M520 1560 Q500 1300 540 1000" stroke="#ffd27a" stroke-width="5" fill="none" opacity=".8"/>'
    b += fireflies(40, 520, 1540, col='#8fe8ff', core='#dffaff', seed=8)
    for sx, sy, ss in ((300, 220, 18), (800, 180, 20), (240, 560, 16), (860, 640, 18)):
        b += spark(sx, sy, ss, col='#fffbe0')
    b += darkband(850, 1250, .5)
    # diver frog at the seafloor, bottom right, looking up
    FX, FY = 830, 1560
    b += f'<ellipse cx="{FX}" cy="{FY - 120}" rx="200" ry="170" fill="#8fe8ff" opacity=".16" filter="url(#b24)"/>'
    for k in range(5):
        b += f'<circle cx="{FX + 30 + k * 6}" cy="{FY - 330 - k * 46}" r="{6 + k * 2}" fill="none" stroke="#cff4ff" stroke-width="3" opacity=".7"/>'
    b += frog(FX, FY, 3.0, rot=4, look=(-3, -4), mouth='O', helmet=True, shadow=True,
              armL='M-34 -22 q-24 -16 -20 -44', armR='M38 -22 q14 6 16 22')
    b += f'<rect width="{W}" height="{H}" fill="url(#vig)"/>'
    save(2, '#060824', d, b, [(Y % '10,210 M', 196, 'w'), ('TALL', 176, 'w')], '#04101c', 870)


# ================= 3: CLOSEST TO THE STARS =================
def make_3():
    rnd = random.Random(33)
    EX, EY, RX, RY = 450, 560, 400, 350
    d = FILTERS + vig() + lin('sp', [(0, '#03041a'), (1, '#0b0f30')])
    d += rad('ocean', EX - 140, EY - 140, 560, [(0, '#5ab8ff', 1), (.55, '#1a5aa8', 1), (1, '#06183a', 1)])
    d += rad('atm', EX, EY, 470, [(0, '#5ad0ff', 0), (.84, '#5ad0ff', 0), (.9, '#8fe0ff', .6), (1, '#8fe0ff', 0)])
    d += f'<clipPath id="ec"><ellipse cx="{EX}" cy="{EY}" rx="{RX}" ry="{RY}"/></clipPath>'
    b = f'<rect width="{W}" height="{H}" fill="url(#sp)"/>' + stars(rnd, 220, 0, H, big=10)
    b += f'<ellipse cx="{EX}" cy="{EY}" rx="{RX + 70}" ry="{RY + 70}" fill="url(#atm)" transform="translate(0 0) scale(1 1)"/>'
    b += f'<ellipse cx="{EX}" cy="{EY}" rx="{RX + 30}" ry="{RY + 30}" fill="#5ad0ff" opacity=".18" filter="url(#b24)"/>'
    b += f'<ellipse cx="{EX}" cy="{EY}" rx="{RX}" ry="{RY}" fill="url(#ocean)" stroke="#0a1838" stroke-width="5"/>'
    land = ''
    for cx, cy, rx, ry in ((EX + 150, EY + 10, 120, 210), (EX - 120, EY - 160, 170, 90), (EX - 220, EY + 120, 90, 120), (EX + 40, EY - 260, 130, 50)):
        pts = [(cx + rx * math.cos(a) * rnd.uniform(.7, 1.1), cy + ry * math.sin(a) * rnd.uniform(.7, 1.1)) for a in [k * math.pi / 8 for k in range(16)]]
        land += f'<path d="{P(pts)}" fill="#4f9a5a" stroke="#1d3a22" stroke-width="3"/>'
    b += f'<g clip-path="url(#ec)">{land}<ellipse cx="{EX + 200}" cy="{EY + 90}" rx="{RX}" ry="{RY + 40}" fill="#02081c" opacity=".45"/>'
    b += f'<ellipse cx="{EX - 150}" cy="{EY - 150}" rx="160" ry="110" fill="#fff" opacity=".18" filter="url(#b24)"/></g>'
    # equator (dashed) and polar radius vs equatorial radius
    b += f'<ellipse cx="{EX}" cy="{EY}" rx="{RX}" ry="40" fill="none" stroke="#ffe7a0" stroke-width="4" stroke-dasharray="16 12" opacity=".75"/>'
    b += f'<path d="M{EX} {EY} L{EX} {EY - RY}" stroke="#bfe8ff" stroke-width="6" stroke-dasharray="14 10" opacity=".8"/>'
    b += f'<circle cx="{EX}" cy="{EY}" r="12" fill="#ffd27a" stroke="#3a2406" stroke-width="3"/><circle cx="{EX}" cy="{EY}" r="30" fill="#ffd27a" opacity=".4" filter="url(#b6)"/>'
    # Chimborazo on the bulge (right limb, exaggerated)
    MX, MY = EX + RX + 2, EY + 40
    b += f'<circle cx="{MX + 70}" cy="{MY - 5}" r="120" fill="#fff2b0" opacity=".28" filter="url(#b24)"/>'
    cone = lambda t: max(0, 1 - abs(t)) ** 1.25
    pts, (SX, SY), pt = limb_mount(EX, EY, RX, RY, 6.5, 15, 165, cone, rnd=rnd, jag=5)
    b += mount_draw(pts, 40, '#7a6a78', '#0a0f22', 5)
    snow = [pt(-1 + 2 * k / 24 * .42 + .58 * 0, 0) for k in range(0)]
    up = [pt(t / 20, 165 * cone(t / 20)) for t in range(-9, 10)]
    lo = [pt(t / 20, 165 * cone(t / 20) - (38 if t % 2 else 52)) for t in range(9, -10, -1)]
    b += f'<path d="{P(up + lo)}" fill="#f4faff" stroke="#0a0f22" stroke-width="4"/>'
    b += f'<path d="M{pt(-.2, 40)[0]:.0f} {pt(-.2, 40)[1]:.0f} L{pt(-.05, 100)[0]:.0f} {pt(-.05, 100)[1]:.0f}" stroke="#0a0f22" stroke-width="3" opacity=".5"/>'
    MX, MY = SX - 112, SY + 5
    # golden beam centre -> summit -> beyond
    b += f'<path d="M{EX} {EY} L{MX + 112} {MY - 5}" stroke="#ffd27a" stroke-width="22" opacity=".35" filter="url(#b6)"/><path d="M{EX} {EY} L{MX + 112} {MY - 5}" stroke="#fff2b0" stroke-width="7"/>'
    b += f'<path d="M{MX + 112} {MY - 5} L1100 {MY - 25}" stroke="#fff2b0" stroke-width="4" stroke-dasharray="10 10" opacity=".7"/>'
    b += spark(MX + 118, MY - 6, 44, col='#fffbe0', op=.95)
    for sx, sy, ss in ((170, 170, 22), (900, 150, 26), (980, 820, 18), (120, 820, 16)):
        b += spark(sx, sy, ss, col='#fff6d6')
    b += darkband(850, 1250, .5)
    # astronaut frog floating bottom left, looking up at the peak
    FX, FY = 300, 1700
    b += f'<ellipse cx="{FX}" cy="{FY - 120}" rx="220" ry="180" fill="#8fd0ff" opacity=".14" filter="url(#b24)"/>'
    helm = ('<circle cx="6" cy="-58" r="47" fill="#cfe8ff" fill-opacity=".13" stroke="#eef4ff" stroke-width="4.5"/>'
            '<path d="M-28 -82 q12 -18 32 -21" fill="none" stroke="#fff" stroke-width="5" opacity=".85"/>'
            '<ellipse cx="6" cy="-14" rx="40" ry="9" fill="#d9dee8" stroke-width="3.2"/>')
    pack = '<rect x="-56" y="-62" width="30" height="52" rx="8" fill="#e8ecf4" stroke-width="3.2"/>'
    b += frog(FX, FY, 3.2, rot=12, look=(4, -4), mouth='O', back=pack, front=helm,
              armL='M-34 -22 q-18 8 -20 26', armR='M38 -22 q20 -14 22 -40',
              legs=((-20, -6, -34, 10, -20), (20, -6, 30, 14, 20)))
    b += f'<path d="M{FX - 60} {FY - 40} q-120 60 -260 30" stroke="#dfe8ff" stroke-width="5" fill="none" opacity=".6"/>'
    b += f'<rect width="{W}" height="{H}" fill="url(#vig)"/>'
    save(3, '#03041a', d, b, [('CLOSEST TO', 150, 'w'), ('THE ' + Y % 'STARS', 176, 'w')], '#04061a', 880)


# ================= 4: DEEPER THAN EVEREST =================
def make_4():
    rnd = random.Random(44)
    SURF = 170
    d = FILTERS + vig(a=.85) + lin('sea', [(0, '#1a6a9a'), (.12, '#0c3a66'), (.45, '#061a36'), (1, '#01040c')])
    d += halo('h4', 540, 520, 460, '#dffaff', '#3ad0ff')
    b = f'<rect width="{W}" height="{H}" fill="url(#sea)"/>'
    b += f'<rect width="{W}" height="{SURF}" fill="#3a8ab8"/><path d="M0 {SURF} q60 -14 120 0 t120 0 t120 0 t120 0 t120 0 t120 0 t120 0 t120 0 t120 0" stroke="#dff6ff" stroke-width="6" fill="none"/>'
    for x0, x1 in ((180, 320), (420, 480), (640, 720), (860, 980)):
        b += f'<path d="M{x0} {SURF} L{x0 - 80} 1100 L{x1 - 60} 1100 L{x1} {SURF}Z" fill="#bff0ff" opacity=".06"/>'
    # trench walls
    L = [(0, 300)] + ridge(rnd, 170, 380, 300, 1880, 16, 30) + [(0, H)]
    R = [(W, 340)] + ridge(rnd, 900, 420, 780, 1880, 16, 30) + [(W, H)]
    b += f'<path d="{P(L)}" fill="#0a1424" stroke="#2a6a8a" stroke-width="5"/><path d="{P(R)}" fill="#0a1424" stroke="#2a6a8a" stroke-width="5"/>'
    for k in range(12):
        y = 420 + k * 120; b += f'<path d="M{rnd.uniform(0, 120):.0f} {y} l{rnd.uniform(60, 140):.0f} 20" stroke="#1d3e5a" stroke-width="4" opacity=".7"/><path d="M{rnd.uniform(960, 1080):.0f} {y + 40} l{-rnd.uniform(60, 140):.0f} 20" stroke="#1d3e5a" stroke-width="4" opacity=".7"/>'
    # depth gap: surface -> summit (dashed) on the right
    b += f'<path d="M990 {SURF + 10} L990 330" stroke="#ffe28a" stroke-width="6" stroke-dasharray="12 10"/><path d="M970 {SURF + 10} l40 0 M970 330 l40 0" stroke="#ffe28a" stroke-width="6"/>'
    # Everest sinking (upright), summit well below the surface, ragged roots, bubbles streaming up
    b += f'<ellipse cx="540" cy="560" rx="460" ry="360" fill="url(#h4)"/>'
    b += peak(rnd, 540, 330, 790, 300, lit='#e8f8ff', shade='#5a86a8', rock='#2a3e5a', line='#06101c')
    roots = [(240, 790)] + [(240 + k * 30, 790 + (30 if k % 2 else 70) + rnd.uniform(-10, 10)) for k in range(1, 20)] + [(840, 790)]
    b += f'<path d="{P(roots)}" fill="#2a3e5a" stroke="#06101c" stroke-width="5"/>'
    for k in range(8):
        b += f'<circle cx="{rnd.uniform(260, 820):.0f}" cy="{rnd.uniform(890, 840):.0f}" r="{rnd.uniform(6, 14):.0f}" fill="#2a3e5a" stroke="#06101c" stroke-width="3"/>'
    for _ in range(40):
        x = rnd.uniform(300, 780); y = rnd.uniform(SURF + 30, 340); r = rnd.uniform(4, 12)
        b += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r:.0f}" fill="none" stroke="#dff6ff" stroke-width="2.5" opacity=".7"/>'
    for k in range(6):
        x = 300 + k * 95; b += f'<path d="M{x} 320 l0 -90" stroke="#bff0ff" stroke-width="4" opacity=".25"/>'
    b += fireflies(50, 380, 1850, col='#5ae0ff', core='#c8fbff', seed=9)
    for sx, sy, ss in ((400, 360, 20), (700, 420, 18), (520, 300, 14)):
        b += spark(sx, sy, ss, col='#f4feff')
    b += darkband(850, 1250, .5)
    # trench floor + frog in diving helmet with a lamp, looking up
    b += f'<path d="M250 1830 q290 -40 580 0 L830 {H} L250 {H}z" fill="#141c26" stroke="#2a4a5a" stroke-width="4"/>'
    FX, FY = 640, 1830
    b += f'<path d="M{FX + 50} {FY - 160} L{FX - 160} 1340 L{FX + 60} 1320Z" fill="#fff6c8" opacity=".12"/>'
    b += f'<ellipse cx="{FX}" cy="{FY - 120}" rx="200" ry="170" fill="#5ae0ff" opacity=".14" filter="url(#b24)"/>'
    lamp = '<g transform="translate(58 -50)"><rect x="-10" y="-14" width="22" height="28" rx="5" fill="#d9a83a" stroke-width="3"/><circle cx="1" cy="-14" r="8" fill="#fff6c8" stroke-width="2.5"/></g>'
    b += frog(FX, FY, 3.0, look=(-2, -5), mouth='O', helmet=True, shadow=True, front=lamp,
              armL='M-34 -22 q-14 6 -16 22', armR='M38 -22 q16 -6 20 -22')
    # small anglerfish glow on the left wall
    b += f'<circle cx="300" cy="1500" r="26" fill="#9ff6ff" opacity=".4" filter="url(#b12)"/><circle cx="300" cy="1500" r="7" fill="#e8ffff"/><path d="M300 1500 q30 -10 40 30" stroke="#5a7a8a" stroke-width="3" fill="none"/>'
    b += f'<rect width="{W}" height="{H}" fill="url(#vig)"/>'
    save(4, '#01040c', d, b, [('DEEPER THAN', 156, 'w'), (Y % 'EVEREST', 196, 'w')], '#020814', 880)


# ================= 5: 2.5x EVEREST =================
def make_5():
    rnd = random.Random(55)
    MX, MY, R = 540, 720, 420
    d = FILTERS + vig() + lin('sp', [(0, '#05030e'), (1, '#120814')])
    d += rad('mars', MX - 160, MY - 260, 760, [(0, '#f29a5a', 1), (.5, '#b8482a', 1), (1, '#3a1208', 1)])
    d += halo('h5', 540, 270, 360, '#fff0d0', '#ff9a6a')
    d += f'<clipPath id="mc"><circle cx="{MX}" cy="{MY}" r="{R}"/></clipPath>'
    b = f'<rect width="{W}" height="{H}" fill="url(#sp)"/>' + stars(rnd, 200, 0, 1500, big=8)
    b += f'<ellipse cx="540" cy="300" rx="480" ry="300" fill="url(#h5)"/>'
    b += f'<circle cx="{MX}" cy="{MY}" r="{R + 26}" fill="#ff9a6a" opacity=".22" filter="url(#b24)"/>'
    b += f'<circle cx="{MX}" cy="{MY}" r="{R}" fill="url(#mars)" stroke="#2a0c06" stroke-width="5"/>'
    surf = ''
    for _ in range(14):
        cx, cy, r = rnd.uniform(MX - R, MX + R), rnd.uniform(MY - R * .6, MY + R), rnd.uniform(14, 46)
        surf += f'<circle cx="{cx:.0f}" cy="{cy:.0f}" r="{r:.0f}" fill="#7a2a14" opacity=".45"/><circle cx="{cx - r * .2:.0f}" cy="{cy - r * .2:.0f}" r="{r * .7:.0f}" fill="#d8704a" opacity=".35"/>'
    surf += f'<path d="M{MX - 420} {MY + 60} q300 60 700 -20" stroke="#6a2010" stroke-width="22" fill="none" opacity=".5"/>'
    b += f'<g clip-path="url(#mc)">{surf}<circle cx="{MX + 200}" cy="{MY + 180}" r="{R}" fill="#1a0604" opacity=".4"/></g>'
    # profile on the top limb: Olympus Mons (broad shield, caldera) and Everest at the same scale (2.5x)
    TOP = MY - R
    shield = lambda t: min(1, 1.12 * (1 - t * t) ** 1.6)
    pts, (OX, OY), pt = limb_mount(MX, MY, R, R, -104, 36, 150, shield, n=80)
    b += f'<path d="{P(pts)}" fill="#ff9a6a" opacity=".35" filter="url(#b12)"/>'
    b += mount_draw(pts, 80, '#c4583a', '#2a0c06', 5)
    lit = [pt(-1 + k / 30, 150 * shield(-1 + k / 30)) for k in range(31)] + [pt(-1 + k / 30, 150 * shield(-1 + k / 30) - 26) for k in range(30, -1, -1)]
    b += f'<path d="{P(lit)}" fill="#f2a070" opacity=".7"/>'
    cl = [pt(t / 10, 150) for t in range(-2, 3)] + [pt(t / 10, 136) for t in range(2, -3, -1)]
    b += f'<path d="{P(cl)}" fill="#5a1a0c" stroke="#2a0c06" stroke-width="3"/><path d="{P(cl)}" fill="none" stroke="#ffd27a" stroke-width="8" opacity=".5" filter="url(#b6)"/>'
    ev = lambda t: max(0, 1 - abs(t)) ** 1.1
    pts, (EVX, EVY), pte = limb_mount(MX, MY, R, R, -58, 4.5, 60, ev, n=12)
    b += mount_draw(pts, 12, '#6a6a80', '#0a0a1a', 4)
    sn = [pte(t / 10, 60 * ev(t / 10)) for t in range(-4, 5)] + [pte(t / 10, 60 * ev(t / 10) - (12 if t % 2 else 20)) for t in range(4, -5, -1)]
    b += f'<path d="{P(sn)}" fill="#f4f8ff" stroke="#0a0a1a" stroke-width="2.5"/>'
    b += f'<circle cx="{EVX:.0f}" cy="{EVY:.0f}" r="40" fill="#cfe8ff" opacity=".25" filter="url(#b12)"/>'
    # Phobos
    b += f'<ellipse cx="900" cy="170" rx="34" ry="24" fill="#8a7a6a" stroke="#1a120c" stroke-width="3"/><circle cx="890" cy="166" r="6" fill="#5a4a3a"/>'
    for sx, sy, ss in ((MX, TOP - 200, 24), (200, 300, 18), (880, 380, 16), (MX - 250, TOP - 140, 14)):
        b += spark(sx, sy, ss, col='#fff0d0')
    b += fireflies(24, 150, 820, col='#ffcf9a', core='#fff2dc', seed=12)
    b += darkband(850, 1250, .55)
    # red dunes foreground + astronaut frog planting a flag
    b += f'<path d="M-20 1640 q260 -80 560 -20 q300 60 560 -40 L1100 {H} L-20 {H}z" fill="#8a3418" stroke="#3a1006" stroke-width="5"/>'
    b += f'<path d="M-20 1760 q300 -40 600 10 q260 40 520 -20 L1100 {H} L-20 {H}z" fill="#a8441e"/>'
    FX, FY = 760, 1700
    b += f'<ellipse cx="{FX}" cy="{FY - 120}" rx="220" ry="180" fill="#ffb07a" opacity=".16" filter="url(#b24)"/>'
    helm = ('<circle cx="6" cy="-58" r="47" fill="#ffd8c0" fill-opacity=".14" stroke="#fff4ec" stroke-width="4.5"/>'
            '<path d="M-28 -82 q12 -18 32 -21" fill="none" stroke="#fff" stroke-width="5" opacity=".85"/>'
            '<ellipse cx="6" cy="-14" rx="40" ry="9" fill="#e8dcd4" stroke-width="3.2"/>')
    flag = ('<g transform="translate(-62 6)"><path d="M0 0 L0 -150" stroke="#d8d8e0" stroke-width="6"/>'
            '<path d="M0 -150 L70 -136 L0 -116Z" fill="#f2d27a" stroke-width="3"/></g>')
    b += frog(FX, FY, 3.2, look=(-4, -4), mouth='O', shadow=True, back=flag + '<rect x="-56" y="-62" width="30" height="52" rx="8" fill="#e8ecf4" stroke-width="3.2"/>', front=helm,
              armL='M-34 -22 q-20 -6 -28 -40', armR='M38 -22 q14 6 16 22')
    b += f'<rect width="{W}" height="{H}" fill="url(#vig)"/>'
    save(5, '#05030e', d, b, [(Y % '2.5&times;', 210, 'w'), ('EVEREST', 176, 'w')], '#0e0408', 860)


if __name__ == '__main__':
    for n in sys.argv[1:] or ['1', '2', '3', '4', '5']:
        globals()[f'make_{n}'](); print('made', n)
