# VERTICAL shorts thumbnails (1080x1920, text centred) for space-nuke-short1..5 (guideline 16-9, brief tools/briefs/thumb_art.md 'Shorts thumbnails').
# Replaces the old landscape make.py (2026-11-06, miya: shorts thumbnails must be 9:16 with centred text).
# One shared generator: writes videos/space-nuke-shortN/thumb/A.html for N = 1..5.
# Reuses frog(), trefoil(), GLOW from the long-form generator videos/space-nuke/thumb/make.py (helpers only, not its pages).
# Layout: scene top (y 250-720) / centred text (~y 600-1300) / scene + frog bottom (y 1300-1670); top/bottom ~250px kept free of key things.
# 1 NOT A SOUND          - blue-white flash above; frog in helmet at the bottom presses a brass ear trumpet to its visor, sound wave flatlines.
# 2 NO MUSHROOM CLOUD    - glowing amber plasma sphere above; dashed ghost mushroom (struck through, crumbling) below, frog staring up.
# 3 THE INVISIBLE KILLER - flash top-right, ghostly X-ray waves down to a big spacecraft hull below: skin vaporizes, cracks; frog peeks through a porthole.
# 4 1962: WE NUKED SPACE - Starfish Prime flash high above the night Pacific horizon, island chain, frog with binoculars on the near island.
# 5 A GHOST AROUND EARTH - frog in helmet floating top-left with a fried satellite; glowing man-made radiation belt around Earth at the bottom.
# run: python3 make_v.py
import os, sys, math, random
HERE = os.path.dirname(os.path.abspath(__file__))
VID = os.path.abspath(os.path.join(HERE, '..', '..'))
sys.path.insert(0, os.path.join(VID, '..', 'tools'))
from thumb_lib import vpage, vsvg, lin, rad, spark
_src = open(os.path.join(VID, 'space-nuke', 'thumb', 'make.py')).read()
exec(_src[_src.index("INK = "):_src.index('# ====')])   # INK/GREEN..., arm, hand_dot, frog, GLOW, trefoil
W, H = 1080, 1920


def vstars(n, y0=20, y1=1900, col='#e8f4ff', op=.5):
    return ''.join(f'<circle cx="{random.randint(10, W - 10)}" cy="{random.randint(y0, y1)}" r="{random.choice([1.4, 2, 2.8])}" '
                   f'fill="{col}" opacity="{op * random.random() + .15:.2f}"/>' for _ in range(n))


def flare(cx, cy, n, L1, L2, col='#fff', w=5, op=.55, off=0):
    return ''.join(f'<line x1="{cx}" y1="{cy}" x2="{cx + (L1 if k % 2 == 0 else L2) * math.cos(math.radians(off + k * 360 / n)):.0f}" '
                   f'y2="{cy + (L1 if k % 2 == 0 else L2) * math.sin(math.radians(off + k * 360 / n)):.0f}" stroke="{col}" stroke-width="{w}" '
                   f'stroke-linecap="round" opacity="{op}" filter="url(#b4)"/>' for k in range(n))


def streaks(cx, cy, n, r0a, r0b, la, lb, cols):
    o = ''
    for _ in range(n):
        a = random.uniform(0, 2 * math.pi); r0 = random.uniform(r0a, r0b); r1 = r0 + random.uniform(la, lb)
        o += (f'<line x1="{cx + r0 * math.cos(a):.0f}" y1="{cy + r0 * math.sin(a):.0f}" x2="{cx + r1 * math.cos(a):.0f}" y2="{cy + r1 * math.sin(a):.0f}" '
              f'stroke="{random.choice(cols)}" stroke-width="{random.choice([1.5, 2, 3])}" opacity="{random.uniform(.08, .3):.2f}"/>')
    return o


# =====================================================================================
# 1: NOT A SOUND
# =====================================================================================
def make_1():
    random.seed(101)
    FX, FY = 540, 480
    d = GLOW
    d += rad('h1', FX, FY, 1000, [(0, '#ffffff', .75), (.12, '#d8f2ff', .5), (.32, '#5fb8ff', .16), (.6, '#2a4fb0', .05), (1, '#0a1030', 0)])
    d += rad('c1', FX, FY, 230, [(0, '#ffffff', 1), (.25, '#ffffff', .98), (.5, '#cfeeff', .7), (.8, '#7cc6ff', .2), (1, '#7cc6ff', 0)])
    d += lin('brass', [(0, '#fff1b8'), (.3, '#f0c45a'), (.7, '#b07a22'), (1, '#6a4410')])
    d += rad('bell', 0, 0, 34, [(0, '#2a1806', 1), (.7, '#6a4410', 1), (1, '#f0c45a', 1)])
    d += lin('fl1', [(0, '#02040c'), (1, '#0a1838')])
    b = f'<rect width="{W}" height="{H}" fill="#02040c"/>'
    b += vstars(320, col='#dfeaff')
    b += f'<rect y="1300" width="{W}" height="620" fill="url(#fl1)"/>'
    b += f'<circle cx="{FX}" cy="{FY}" r="1000" fill="url(#h1)"/>'
    for r, op in ((340, .2), (430, .11), (530, .06)):
        b += f'<circle cx="{FX}" cy="{FY}" r="{r}" fill="none" stroke="#bfe6ff" stroke-width="6" opacity="{op}" filter="url(#b4)"/>'
    b += streaks(FX, FY, 80, 110, 230, 300, 900, ["#e8f6ff", "#cfe8ff", "#fffbe8"])
    b += f'<circle cx="{FX}" cy="{FY}" r="270" fill="#9fdcff" opacity=".35" filter="url(#b60)"/>'
    b += f'<circle cx="{FX}" cy="{FY}" r="230" fill="url(#c1)"/>'
    b += flare(FX, FY, 8, 500, 300, w=9, op=.7, off=22)
    b += flare(FX, FY, 16, 230, 160, w=3, op=.5, off=11)
    b += f'<circle cx="{FX}" cy="{FY}" r="80" fill="#fff" filter="url(#b12)"/>'
    b += f'<ellipse cx="{FX}" cy="{FY}" rx="540" ry="10" fill="#d8f2ff" opacity=".6" filter="url(#b4)"/>'
    # ---- sound wave: loud at the flash, curving down the right side, flat dead line into the trumpet ----
    P0, P1, P2 = (720, 600), (1130, 960), (900, 1400)
    pts = []
    N = 300
    for i in range(N + 1):
        t = i / N
        x = (1 - t) ** 2 * P0[0] + 2 * (1 - t) * t * P1[0] + t * t * P2[0]
        y = (1 - t) ** 2 * P0[1] + 2 * (1 - t) * t * P1[1] + t * t * P2[1]
        dx = 2 * (1 - t) * (P1[0] - P0[0]) + 2 * t * (P2[0] - P1[0]); dy = 2 * (1 - t) * (P1[1] - P0[1]) + 2 * t * (P2[1] - P1[1])
        L = math.hypot(dx, dy); nx, ny = -dy / L, dx / L
        o = 95 * max(0, 1 - t / .55) ** 1.4 * math.sin(t * 46)
        pts.append((x + nx * o, y + ny * o))
    path = 'M' + ' L'.join(f'{x:.1f} {y:.1f}' for x, y in pts)
    b += f'<path d="{path}" fill="none" stroke="#7fd6ff" stroke-width="22" opacity=".35" filter="url(#b12)"/>'
    b += f'<path d="{path}" fill="none" stroke="#e8f8ff" stroke-width="10" stroke-linejoin="round"/>'
    # ---- frog in helmet pressing a brass ear trumpet to the visor ----
    horn = ('<g>'
            '<path d="M56 -50 Q90 -54 118 -76 L150 -112 Q168 -78 160 -50 L120 -52 Q92 -44 58 -40Z" fill="url(#brass)" stroke-width="3.4"/>'
            '<g transform="translate(156 -82) rotate(-35)"><ellipse rx="22" ry="38" fill="url(#bell)" stroke-width="3.4"/></g>'
            '<path d="M64 -48 Q92 -50 120 -70" fill="none" stroke="#fff6d0" stroke-width="3" opacity=".8"/>'
            '<rect x="50" y="-54" width="10" height="16" rx="3" fill="#8a5a1a" stroke-width="2.6"/></g>')
    b += '<ellipse cx="350" cy="1660" rx="170" ry="18" fill="#7fd6ff" opacity=".1"/>'
    b += frog(340, 1650, 3.3, look=(5, -2), mouth='wow', helmet=True, rot=4,
              armL='M-34 -22 q-18 10 -14 28', armR='M38 -22 q30 4 62 -26', front=horn)
    b += '<text x="960" y="1600" font-family="Fredoka" font-weight="700" font-size="96" fill="#e8f8ff" stroke="#050b18" stroke-width="8" paint-order="stroke" opacity=".9">?</text>'
    for x, y, s in ((120, 300, 18), (980, 290, 22), (90, 1180, 14), (1000, 1760, 12), (160, 820, 12)):
        b += spark(x, y, s)
    return vpage('#02040c', vsvg(d, b), [('NOT A', 200, 'w'), ('SOUND', 230, 'y')], top=780)


# =====================================================================================
# 2: NO MUSHROOM CLOUD
# =====================================================================================
def make_2():
    random.seed(202)
    CX, CY, R = 540, 480, 250
    d = GLOW
    d += rad('h2', CX, CY, 950, [(0, '#fff6dc', .6), (.22, '#ffcf7a', .25), (.5, '#ff7a3a', .07), (1, '#3a0f10', 0)])
    d += rad('s2', CX, CY, R, [(0, '#ffffff', .95), (.25, '#fff1c4', .8), (.55, '#ffc062', .55), (.82, '#ff8a3a', .5), (.95, '#ffe0a0', .9), (1, '#fff', 0)])
    d += rad('k2', CX, CY, 120, [(0, '#ffffff', 1), (.5, '#fff5d0', .9), (1, '#ffd070', 0)])
    b = f'<rect width="{W}" height="{H}" fill="#05040a"/>'
    b += vstars(320, col='#f0e8ff')
    b += f'<circle cx="{CX}" cy="{CY}" r="950" fill="url(#h2)"/>'
    b += streaks(CX, CY, 70, R * .85, R * 1.05, 200, 650, ["#fff3d0", "#ffd9a0", "#ffffff"])
    for k in range(100):
        a = random.uniform(0, 2 * math.pi); r = R * random.uniform(1.05, 1.75)
        b += f'<circle cx="{CX + r * math.cos(a):.0f}" cy="{CY + r * math.sin(a):.0f}" r="{random.choice([2, 3, 4])}" fill="#ffd9a0" opacity="{random.uniform(.25, .7):.2f}"/>'
    b += f'<circle cx="{CX}" cy="{CY}" r="{R + 50}" fill="#ff9a4a" opacity=".25" filter="url(#b30)"/>'
    b += f'<circle cx="{CX}" cy="{CY}" r="{R}" fill="url(#s2)"/>'
    fil = ''
    for k in range(80):
        a = random.uniform(0, 2 * math.pi); rr = R * random.uniform(.2, .95)
        a2 = a + random.uniform(.3, 1.0); rr2 = R * random.uniform(.3, .96)
        qx = CX + (rr + rr2) * .6 * math.cos((a + a2) / 2); qy = CY + (rr + rr2) * .6 * math.sin((a + a2) / 2)
        fil += (f'<path d="M{CX + rr * math.cos(a):.0f} {CY + rr * math.sin(a):.0f} Q{qx:.0f} {qy:.0f} {CX + rr2 * math.cos(a2):.0f} {CY + rr2 * math.sin(a2):.0f}" '
                f'fill="none" stroke="{random.choice(["#fff4dc", "#ffcf8a", "#ff9e5a", "#fff"])}" stroke-width="{random.choice([2, 3, 5])}" opacity="{random.uniform(.15, .45):.2f}"/>')
    b += f'<g filter="url(#b4)">{fil}</g>'
    b += f'<circle cx="{CX}" cy="{CY}" r="{R - 6}" fill="none" stroke="#fff4dc" stroke-width="12" opacity=".6" filter="url(#b4)"/>'
    b += f'<circle cx="{CX}" cy="{CY}" r="120" fill="url(#k2)"/>'
    b += f'<circle cx="{CX}" cy="{CY}" r="55" fill="#fff" filter="url(#b12)"/>'
    b += flare(CX, CY, 8, 290, 180, w=6, op=.6, off=0)
    # expansion arrows in every direction (except straight down into the title)
    for ang in range(0, 360, 45):
        a = math.radians(ang + 22.5)
        if math.sin(a) > .5:
            continue
        r0, r1 = R + 40, R + 120
        x0, y0, x2, y2 = CX + r0 * math.cos(a), CY + r0 * math.sin(a), CX + r1 * math.cos(a), CY + r1 * math.sin(a)
        hx, hy = math.cos(a), math.sin(a)
        b += (f'<line x1="{x0:.0f}" y1="{y0:.0f}" x2="{x2:.0f}" y2="{y2:.0f}" stroke="#fff1c8" stroke-width="7" stroke-linecap="round" opacity=".8"/>'
              f'<path d="M{x2 + hx * 22:.0f} {y2 + hy * 22:.0f} L{x2 - hy * 16:.0f} {y2 + hx * 16:.0f} L{x2 + hy * 16:.0f} {y2 - hx * 16:.0f}Z" fill="#fff1c8" opacity=".8"/>')
    # ---- ghost mushroom cloud below the title (dashed outline, faint fill, struck through, crumbling) ----
    MX, MY, BASE = 690, 1470, 1760
    mush = (f'M{MX - 70} {BASE} L{MX - 50} {MY + 160} Q{MX - 60} {MY + 130} {MX - 150} {MY + 132} '
            f'Q{MX - 250} {MY + 120} {MX - 240} {MY + 50} Q{MX - 250} {MY - 10} {MX - 180} {MY - 30} '
            f'Q{MX - 150} {MY - 100} {MX - 60} {MY - 90} Q{MX} {MY - 140} {MX + 70} {MY - 92} '
            f'Q{MX + 160} {MY - 100} {MX + 190} {MY - 30} Q{MX + 260} {MY - 10} {MX + 250} {MY + 50} '
            f'Q{MX + 260} {MY + 120} {MX + 160} {MY + 132} Q{MX + 60} {MY + 130} {MX + 50} {MY + 160} L{MX + 70} {BASE}Z')
    b += f'<path d="{mush}" fill="#c8d8ff" opacity=".07"/><path d="{mush}" fill="none" stroke="#9fb8ff" stroke-width="30" opacity=".12" filter="url(#b12)"/>'
    b += f'<path d="{mush}" fill="none" stroke="#c8d8ff" stroke-width="7" stroke-dasharray="26 18" stroke-linecap="round" opacity=".8"/>'
    b += f'<path d="M{MX - 150} {MY + 40} q60 -30 120 0 q60 -30 120 0" fill="none" stroke="#c8d8ff" stroke-width="5" stroke-dasharray="14 14" opacity=".45"/>'
    b += f'<path d="M{MX - 50} {MY + 210} q50 20 100 0" fill="none" stroke="#c8d8ff" stroke-width="5" stroke-dasharray="14 14" opacity=".4"/>'
    b += f'<path d="M{MX - 190} {MY + 230} Q{MX + 10} {MY + 80} {MX + 240} {MY - 110}" fill="none" stroke="#050b18" stroke-width="30" stroke-linecap="round" opacity=".7"/>'
    b += f'<path d="M{MX - 190} {MY + 230} Q{MX + 10} {MY + 80} {MX + 240} {MY - 110}" fill="none" stroke="#f4f0e6" stroke-width="14" stroke-linecap="round"/>'
    b += f'<path d="M{MX - 172} {MY + 246} Q{MX + 20} {MY + 100} {MX + 230} {MY - 90}" fill="none" stroke="#f4f0e6" stroke-width="5" stroke-linecap="round" opacity=".6"/>'
    r2 = random.Random(7)
    for k in range(16):
        x = MX + 250 + r2.randint(10, 110); y = MY - 60 + r2.randint(-40, 160)
        b += f'<rect x="{x}" y="{y}" width="{r2.randint(10, 22)}" height="6" rx="3" fill="#c8d8ff" opacity="{r2.uniform(.15, .5):.2f}" transform="rotate({r2.randint(-40, 40)} {x} {y})"/>'
    # ---- frog in helmet beside the ghost stem, staring up at the sphere ----
    b += frog(205, 1680, 3.0, look=(4, -6), mouth='wow', helmet=True, rot=4,
              armL='M-34 -22 q-18 8 -16 26', armR='M38 -24 q14 -4 18 -30')
    for x, y, s in ((110, 300, 18), (980, 300, 22), (1000, 820, 14), (80, 1200, 14)):
        b += spark(x, y, s)
    return vpage('#05040a', vsvg(d, b), [('NO', 210, 'y'), ('MUSHROOM', 150, 'w'), ('CLOUD', 200, 'w')], top=770)


# =====================================================================================
# 3: THE INVISIBLE KILLER
# =====================================================================================
def make_3():
    random.seed(303)
    FX, FY = 900, 330
    HX, HY, HR, HS = 500, 1600, -28, .85   # hull group transform
    d = GLOW
    d += rad('h3', FX, FY, 900, [(0, '#ffffff', .7), (.15, '#e6d8ff', .35), (.45, '#7a5cff', .08), (1, '#140a30', 0)])
    d += lin('hull', [(0, '#f4f4f0'), (.22, '#d6d8dc'), (.6, '#8d929b'), (.88, '#4a4f58'), (1, '#262a31')])
    d += lin('foil', [(0, '#fff2b0'), (.4, '#e2b24a'), (.8, '#9a6a1c'), (1, '#5a3a0c')])
    d += rad('hot', 0, 0, 200, [(0, '#ffffff', 1), (.2, '#fff2c0', .95), (.5, '#ff9a3a', .6), (1, '#ff5a1a', 0)])
    d += rad('win', 0, 0, 120, [(0, '#2a3a5a', 1), (.8, '#141c30', 1), (1, '#0a0f1c', 1)])
    d += '<clipPath id="port"><circle cx="0" cy="0" r="104"/></clipPath>'
    b = f'<rect width="{W}" height="{H}" fill="#04030b"/>'
    b += vstars(320, col='#e6e2ff')
    b += f'<circle cx="{FX}" cy="{FY}" r="900" fill="url(#h3)"/>'
    b += f'<circle cx="{FX}" cy="{FY}" r="130" fill="#e6d8ff" opacity=".5" filter="url(#b30)"/>'
    b += f'<circle cx="{FX}" cy="{FY}" r="70" fill="#fff" filter="url(#b12)"/>'
    b += flare(FX, FY, 8, 240, 140, w=5, op=.6, off=10)
    # struck end of the hull in screen coords
    a = math.radians(HR)
    def g2s(lx, ly):
        return HX + HS * (lx * math.cos(a) - ly * math.sin(a)), HY + HS * (lx * math.sin(a) + ly * math.cos(a))
    tx, ty = g2s(470, 0)
    # ---- ghostly X-ray waves (barely visible, dashed sine) flowing down to the hull ----
    waves = ''
    for k in range(9):
        off = (k - 4) * 40
        sx, sy = FX + off * .5, FY + 70
        ex, ey = tx + off * 1.3, ty - 40 + off * .5
        L = math.hypot(ex - sx, ey - sy); ux, uy = (ex - sx) / L, (ey - sy) / L; nx, ny = -uy, ux
        p = []
        for i in range(141):
            t = i / 140; o = 20 * math.sin(t * 36 + k)
            p.append((sx + (ex - sx) * t + nx * o, sy + (ey - sy) * t + ny * o))
        pd = 'M' + ' L'.join(f'{x:.0f} {y:.0f}' for x, y in p)
        waves += f'<path d="{pd}" fill="none" stroke="#e2d6ff" stroke-width="5" stroke-dasharray="3 14" stroke-linecap="round" opacity="{.55 if k % 2 else .35}"/>'
        waves += f'<path d="{pd}" fill="none" stroke="#b49cff" stroke-width="16" opacity=".07"/>'
    b += f'<g filter="url(#b4)">{waves}</g>'
    # ---- the hull ----
    h = f'<g transform="translate({HX} {HY}) rotate({HR}) scale({HS})">'
    h += '<ellipse cx="-560" cy="0" rx="70" ry="210" fill="#3a3f48" stroke="#0b0d14" stroke-width="6"/>'
    h += '<path d="M-560 -210 L470 -210 L470 210 L-560 210Z" fill="url(#hull)" stroke="#0b0d14" stroke-width="6"/>'
    for sx in range(-460, 470, 120):
        h += f'<line x1="{sx}" y1="-210" x2="{sx}" y2="210" stroke="#3b4048" stroke-width="4" opacity=".6"/>'
        for ry in range(-190, 200, 32):
            h += f'<circle cx="{sx + 10}" cy="{ry}" r="3.4" fill="#2c3036" opacity=".55"/>'
    h += '<rect x="-80" y="40" width="380" height="120" fill="url(#foil)" opacity=".85" stroke="#0b0d14" stroke-width="4"/>'
    h += ''.join(f'<path d="M{-80 + k * 38} 40 l12 120" stroke="#6a4a10" stroke-width="2" opacity=".5"/>' for k in range(10))
    h += '<path d="M-560 -184 L470 -184" stroke="#fff" stroke-width="12" opacity=".7" stroke-linecap="round"/>'
    h += '<path d="M-560 196 L470 196" stroke="#8a7cff" stroke-width="6" opacity=".35"/>'
    h += '<ellipse cx="470" cy="0" rx="70" ry="210" fill="#c9cdd4" stroke="#0b0d14" stroke-width="6"/>'
    h += '<g transform="translate(400 -40)"><circle r="200" fill="url(#hot)"/></g>'
    h += '<ellipse cx="470" cy="0" rx="70" ry="210" fill="#ffb060" opacity=".45"/>'
    for path in ('M420 -120 l-60 30 l-30 -20 l-70 40 l-40 -10', 'M430 40 l-50 -10 l-40 40 l-90 0 l-30 30', 'M380 -10 l-70 -40 l-60 10',
                 'M440 140 l-60 10 l-30 30'):
        h += f'<path d="{path}" fill="none" stroke="#1a0c04" stroke-width="9" stroke-linejoin="round"/>'
        h += f'<path d="{path}" fill="none" stroke="#ffb040" stroke-width="3.5" stroke-linejoin="round"/>'
    h += '<path d="M460 -200 q60 -40 120 -110 l14 30 q-50 70 -110 96z" fill="#d6d8dc" stroke="#0b0d14" stroke-width="5"/>'
    h += '<path d="M500 60 q80 -10 150 -70 l6 34 q-64 52 -140 62z" fill="#c2c6cc" stroke="#0b0d14" stroke-width="5"/>'
    # porthole + peeking frog (counter-rotated so the frog stands upright)
    h += '<circle cx="-300" cy="-40" r="122" fill="#5d636c" stroke="#0b0d14" stroke-width="6"/>'
    h += ''.join(f'<circle cx="{-300 + 112 * math.cos(math.radians(q)):.0f}" cy="{-40 + 112 * math.sin(math.radians(q)):.0f}" r="5" fill="#2c3036"/>' for q in range(0, 360, 30))
    h += f'<g transform="translate(-300 -40) rotate({-HR})"><circle r="104" fill="url(#win)"/><g clip-path="url(#port)">'
    h += frog(-6, 150, 2.7, look=(6, -5), mouth='wow', rot=0, pupil=6, armL='M-34 -22 q-10 -10 -4 -32', armR='M38 -22 q10 -10 4 -32')
    h += '<path d="M-80 -40 q30 -50 90 -60" fill="none" stroke="#fff" stroke-width="10" opacity=".35"/><circle r="104" fill="#9fc6ff" opacity=".12"/></g>'
    h += '<circle r="104" fill="none" stroke="#c9ced8" stroke-width="8"/></g>'
    h += '</g>'
    b += h
    # vaporised metal bursting out toward the source (blow-off) + shock arcs
    bx_, by_ = g2s(500, -60)
    puff = ''
    r3 = random.Random(31)
    for k in range(60):
        ang = math.radians(r3.uniform(-140, -20)); dist = r3.uniform(20, 240)
        puff += (f'<circle cx="{bx_ + dist * math.cos(ang):.0f}" cy="{by_ + dist * math.sin(ang):.0f}" r="{r3.randint(8, 28)}" '
                 f'fill="{r3.choice(["#fff1d6", "#ffd090", "#ffa050", "#ffffff"])}" opacity="{r3.uniform(.2, .6):.2f}"/>')
    b += f'<g filter="url(#b4)">{puff}</g>'
    b += f'<circle cx="{bx_:.0f}" cy="{by_:.0f}" r="110" fill="#ffd090" opacity=".4" filter="url(#b30)"/>'
    for r, op in ((140, .5), (195, .3), (250, .15)):
        b += f'<path d="M{bx_ - r * .95:.0f} {by_ - r * .1:.0f} A{r} {r} 0 0 1 {bx_ + r * .6:.0f} {by_ - r * .8:.0f}" fill="none" stroke="#ffe6b0" stroke-width="6" opacity="{op}"/>'
    for x, y, s in ((120, 320, 16), (300, 520, 14), (60, 1160, 12), (1010, 640, 18)):
        b += spark(x, y, s)
    return vpage('#04030b', vsvg(d, b), [('THE', 130, 'w'), ('INVISIBLE', 160, 'y'), ('KILLER', 210, 'w')], top=650)


# =====================================================================================
# 4: 1962: WE NUKED SPACE
# =====================================================================================
def make_4():
    random.seed(404)
    FX, FY = 600, 430
    HZ = 1340                       # horizon height
    EX, ER = 540, 3020; EY = HZ + ER
    d = GLOW
    d += rad('atm4', EX, EY, ER + 90, [(0, '#000', 0), (.96, '#1d4fa0', 0), (.975, '#5fa8ff', .7), (.99, '#2a5fc0', .25), (1, '#000', 0)])
    d += rad('sea4', EX, EY, ER, [(0, '#020812', 1), (.9, '#06142c', 1), (.985, '#0c2a56', 1), (1, '#2a5fa0', 1)])
    d += rad('f4', FX, FY, 760, [(0, '#ffffff', 1), (.06, '#f4fbff', .95), (.18, '#c8e6ff', .5), (.45, '#6aa0ff', .12), (1, '#6aa0ff', 0)])
    d += lin('isl', [(0, '#2c3a2c'), (1, '#0b120c')])
    d += f'<clipPath id="e4"><circle cx="{EX}" cy="{EY}" r="{ER}"/></clipPath>'
    b = f'<rect width="{W}" height="{H}" fill="#02030a"/>'
    b += vstars(300, 20, HZ, col='#e8eeff', op=.55)
    b += f'<circle cx="{EX}" cy="{EY}" r="{ER + 90}" fill="url(#atm4)"/>'
    au = ''
    for dx, col, w, op in ((-560, '#ff4f6e', 26, .35), (-400, '#7dffb0', 22, .45), (-250, '#ff5f7e', 18, .35),
                           (240, '#7dffb0', 22, .45), (380, '#ff4f6e', 26, .35), (520, '#7dffb0', 16, .3)):
        au += f'<path d="M{FX + dx * .2:.0f} {FY + 30} Q{FX + dx * 1.1:.0f} {FY + 120} {FX + dx * .8:.0f} {HZ + 10}" fill="none" stroke="{col}" stroke-width="{w}" opacity="{op}"/>'
    b += f'<g filter="url(#b12)">{au}</g>'
    b += f'<circle cx="{EX}" cy="{EY}" r="{ER}" fill="url(#sea4)"/>'
    eg = '<g clip-path="url(#e4)">'
    eg += f'<ellipse cx="{FX}" cy="{HZ + 70}" rx="480" ry="70" fill="#bfe0ff" opacity=".22" filter="url(#b30)"/>'
    for i in range(50):
        y = HZ + 14 + i * 9; w = 30 + i * 9
        eg += f'<rect x="{FX - w / 2 + random.randint(-30, 30):.0f}" y="{y}" width="{w:.0f}" height="3" fill="#dff1ff" opacity="{max(.04, .45 - i * .009):.2f}"/>'
    for i in range(80):
        x = random.randint(0, W); y = random.randint(HZ + 10, 1900)
        eg += f'<rect x="{x}" y="{y}" width="{random.randint(14, 50)}" height="3" fill="{random.choice(["#5dff9a", "#ff5f7e"])}" opacity="{random.uniform(.06, .2):.2f}"/>'
    r2 = random.Random(4)
    for _ in range(22):
        x = r2.randint(-100, 1180); y = r2.randint(HZ + 10, HZ + 180); rx = r2.randint(40, 150)
        eg += f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{rx * .12:.0f}" fill="#9fb8e0" opacity="{r2.uniform(.06, .16):.2f}" filter="url(#b4)"/>'
    eg += '</g>'
    b += eg
    b += f'<circle cx="{EX}" cy="{EY}" r="{ER}" fill="none" stroke="#9fd0ff" stroke-width="5" opacity=".6"/>'
    # island chain receding toward the horizon
    for x, y, s in ((860, HZ + 14, .16), (760, HZ + 30, .22), (900, HZ + 58, .3), (760, HZ + 100, .42)):
        b += f'<path d="M{x - 120 * s:.0f} {y} Q{x - 40 * s:.0f} {y - 50 * s:.0f} {x:.0f} {y - 70 * s:.0f} Q{x + 50 * s:.0f} {y - 40 * s:.0f} {x + 130 * s:.0f} {y}Z" fill="url(#isl)" stroke="#9fd0ff" stroke-width="1.5" stroke-opacity=".4"/>'
        for k in range(int(10 * s) + 2):
            b += f'<circle cx="{x + random.uniform(-90, 90) * s:.0f}" cy="{y - random.uniform(2, 12) * s:.0f}" r="{max(1.4, 4 * s):.1f}" fill="#ffd27a" opacity=".9"/>'
    # near island (foreground, bottom-left): volcano slope, palms, surf
    b += '<g transform="translate(0 800)"><path d="M-40 1120 L-40 900 Q120 820 260 760 Q330 735 380 770 Q520 860 700 900 Q780 930 820 1120Z" fill="url(#isl)"/>'
    b += '<path d="M200 790 Q260 760 300 752 Q340 748 380 770" fill="none" stroke="#7fe0b0" stroke-width="4" opacity=".35"/>'
    b += '<path d="M-40 900 Q120 820 260 760 Q330 735 380 770 Q520 860 700 900 Q780 930 820 1120" fill="none" stroke="#ff9db0" stroke-width="3" opacity=".25"/>'
    b += '<path d="M700 905 q60 10 110 40 M760 950 q40 20 70 60" fill="none" stroke="#dff1ff" stroke-width="4" opacity=".35"/>'
    for px, py, hgt, lean in ((560, 880, 170, 14), (650, 900, 130, 22)):
        qx, qy = px + lean, py - hgt
        b += f'<path d="M{px} {py} Q{px + lean * .3:.0f} {py - hgt * .6:.0f} {qx} {qy}" fill="none" stroke="#0a0f0a" stroke-width="12" stroke-linecap="round"/>'
        for ang in (-170, -130, -60, -20, 20, 160):
            q = math.radians(ang); L = hgt * .5
            b += f'<path d="M{qx} {qy} Q{qx + L * .6 * math.cos(q):.0f} {qy + L * .6 * math.sin(q) - 24:.0f} {qx + L * math.cos(q):.0f} {qy + L * math.sin(q) + 18:.0f}" fill="none" stroke="#0a0f0a" stroke-width="10" stroke-linecap="round"/>'
    b += '</g>'
    # ---- the flash, far above the edge of the Earth ----
    b += f'<circle cx="{FX}" cy="{FY}" r="760" fill="url(#f4)"/>'
    b += f'<circle cx="{FX}" cy="{FY}" r="130" fill="#e6f4ff" opacity=".6" filter="url(#b30)"/>'
    b += f'<circle cx="{FX}" cy="{FY}" r="70" fill="#fff" filter="url(#b12)"/>'
    b += flare(FX, FY, 12, 320, 180, w=5, op=.55, off=15)
    b += f'<circle cx="{FX}" cy="{FY}" r="220" fill="none" stroke="#e8f4ff" stroke-width="5" opacity=".35" filter="url(#b4)"/>'
    # ---- frog on the near island, binoculars up at the flash ----
    bino = ('<g transform="translate(0 64) rotate(-12 6 -66)">'
            '<rect x="-24" y="-80" width="24" height="56" rx="8" fill="#2b2f36" stroke-width="3.2"/>'
            '<rect x="10" y="-80" width="24" height="56" rx="8" fill="#2b2f36" stroke-width="3.2"/>'
            '<rect x="-2" y="-62" width="14" height="14" fill="#444a54" stroke-width="2.6"/>'
            '<ellipse cx="-12" cy="-80" rx="12" ry="5" fill="#8fd0ff" stroke-width="2.6"/><ellipse cx="22" cy="-80" rx="12" ry="5" fill="#8fd0ff" stroke-width="2.6"/>'
            '<path d="M-18 -74 l0 40 M16 -74 l0 40" stroke="#6a7280" stroke-width="3" opacity=".7"/></g>')
    flower = ('<g transform="translate(-30 -82)">' + ''.join(
        f'<circle cx="{9 * math.cos(math.radians(q)):.1f}" cy="{9 * math.sin(math.radians(q)):.1f}" r="7" fill="#ff7aa8" stroke-width="2"/>' for q in range(0, 360, 72))
        + '<circle r="5" fill="#ffd35a" stroke-width="2"/></g>')
    b += '<ellipse cx="320" cy="1560" rx="100" ry="13" fill="#000" opacity=".35"/>'
    b += frog(320, 1556, 2.9, look=(6, -8), mouth='wow', rot=-8,
              armL='M-34 -22 q8 4 22 8', armR='M38 -22 q-6 4 -12 10', front=bino + flower)
    for x, y, s in ((110, 300, 18), (990, 300, 20), (1000, 900, 14), (70, 1150, 12)):
        b += spark(x, y, s)
    return vpage('#02030a', vsvg(d, b), [('1962:', 200, 'y'), ('WE NUKED', 165, 'w'), ('SPACE', 210, 'w')], top=720)


# =====================================================================================
# 5: A GHOST AROUND EARTH
# =====================================================================================
def make_5():
    random.seed(505)
    CX, CY, ER = 540, 1440, 210
    RX, RY, ROT = 470, 135, -12
    d = GLOW
    d += rad('earth5', CX - 70, CY - 80, ER * 1.3, [(0, '#7fc8ff', 1), (.4, '#2a7ad0', 1), (.8, '#103e84', 1), (1, '#061a3c', 1)])
    d += rad('atm5', CX, CY, ER + 40, [(0, '#000', 0), (.85, '#5fb0ff', 0), (.9, '#8fd0ff', .7), (1, '#2a6fd0', 0)])
    d += rad('night5', CX + 140, CY + 100, ER * 1.2, [(0, '#000814', .85), (.6, '#000814', .45), (1, '#000814', 0)])
    d += rad('g5', CX, CY, 900, [(0, '#5fffd0', .18), (.4, '#3a8aff', .07), (1, '#000', 0)])
    d += f'<clipPath id="ec5"><circle cx="{CX}" cy="{CY}" r="{ER}"/></clipPath>'
    d += f'<clipPath id="front5"><rect x="{CX - 1000}" y="{CY}" width="2000" height="600"/></clipPath>'
    d += f'<clipPath id="back5"><rect x="{CX - 1000}" y="{CY - 600}" width="2000" height="600"/></clipPath>'
    b = f'<rect width="{W}" height="{H}" fill="#02040a"/>'
    b += vstars(340, col='#e2f0ff')
    b += f'<circle cx="{CX}" cy="{CY}" r="900" fill="url(#g5)"/>'

    def belt(clip):
        o = f'<g transform="rotate({ROT} {CX} {CY})" clip-path="url(#{clip})">'
        o += f'<ellipse cx="{CX}" cy="{CY}" rx="{RX}" ry="{RY}" fill="none" stroke="#3affc8" stroke-width="140" opacity=".16" filter="url(#b30)"/>'
        o += f'<ellipse cx="{CX}" cy="{CY}" rx="{RX}" ry="{RY}" fill="none" stroke="#8a6aff" stroke-width="84" opacity=".16" filter="url(#b12)"/>'
        o += f'<ellipse cx="{CX}" cy="{CY}" rx="{RX}" ry="{RY}" fill="none" stroke="#9fffe0" stroke-width="38" opacity=".35" filter="url(#b12)"/>'
        o += f'<ellipse cx="{CX}" cy="{CY}" rx="{RX}" ry="{RY}" fill="none" stroke="#eafff8" stroke-width="8" opacity=".7" filter="url(#b4)"/>'
        for rx, ry, op in ((RX - 55, RY - 28, .4), (RX + 55, RY + 24, .3)):
            o += f'<ellipse cx="{CX}" cy="{CY}" rx="{rx}" ry="{ry}" fill="none" stroke="#bfffee" stroke-width="3" stroke-dasharray="4 18" opacity="{op}"/>'
        r = random.Random(11 if clip == 'back5' else 12)
        for k in range(100):
            t = r.uniform(0, 2 * math.pi); s = r.uniform(.86, 1.14)
            x = CX + RX * s * math.cos(t); y = CY + RY * s * math.sin(t)
            tx_, ty_ = -RX * math.sin(t), RY * math.cos(t); L = math.hypot(tx_, ty_); tx_ /= L; ty_ /= L
            o += f'<line x1="{x:.0f}" y1="{y:.0f}" x2="{x - tx_ * 22:.0f}" y2="{y - ty_ * 22:.0f}" stroke="#d8fff4" stroke-width="3" stroke-linecap="round" opacity="{r.uniform(.3, .9):.2f}"/>'
        for k in range(14):
            t = r.uniform(0, 2 * math.pi)
            x = CX + RX * 1.05 * math.cos(t); y = CY + RY * 1.05 * math.sin(t)
            o += f'<path d="M{x:.0f} {y:.0f} q{30 * math.cos(t):.0f} -40 {70 * math.cos(t):.0f} -30 q{30 * math.cos(t):.0f} 10 {50 * math.cos(t):.0f} -40" fill="none" stroke="#bfffee" stroke-width="5" stroke-linecap="round" opacity=".25" filter="url(#b4)"/>'
        return o + '</g>'

    fl = ''
    for k in (1.5, 2.0, 2.5):
        for sgn in (-1, 1):
            pts = []
            for i in range(61):
                th = math.radians(18 + i * (144 / 60))
                r_ = ER * k * math.sin(th) ** 2
                pts.append((CX + sgn * r_ * math.sin(th), CY - r_ * math.cos(th)))
            fl += '<path d="M' + ' L'.join(f'{x:.0f} {y:.0f}' for x, y in pts) + f'" fill="none" stroke="#9fc8ff" stroke-width="3" stroke-dasharray="3 12" stroke-linecap="round" opacity=".32" transform="rotate({ROT} {CX} {CY})"/>'
    b += fl
    b += belt('back5')
    b += f'<circle cx="{CX}" cy="{CY}" r="{ER + 40}" fill="url(#atm5)"/>'
    b += f'<circle cx="{CX}" cy="{CY}" r="{ER}" fill="url(#earth5)"/>'
    e = '<g clip-path="url(#ec5)">'
    e += (f'<path d="M{CX - 170} {CY - 100} q50 -50 120 -34 q34 26 17 68 q-50 34 -85 8 q-42 8 -52 -42z '
          f'M{CX + 34} {CY + 17} q68 -25 110 17 q17 50 -25 76 q-60 8 -85 -34z M{CX - 100} {CY + 94} q34 -17 60 8 q0 34 -34 42 q-34 -17 -26 -50z" fill="#4f9a5a" opacity=".85"/>')
    r2 = random.Random(3)
    for _ in range(26):
        x = r2.randint(CX - ER, CX + ER); y = r2.randint(CY - ER, CY + ER); rx = r2.randint(26, 90)
        e += f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{rx * .2:.0f}" fill="#f2f8ff" opacity="{r2.uniform(.2, .5):.2f}" filter="url(#b4)"/>'
    e += f'<circle cx="{CX}" cy="{CY}" r="{ER}" fill="url(#night5)"/>'
    e += f'<path d="M{CX - ER + 26} {CY - 50} A{ER} {ER} 0 0 1 {CX - 50} {CY - ER + 26}" fill="none" stroke="#fff" stroke-width="9" opacity=".4" filter="url(#b4)"/>'
    e += '</g>'
    b += e
    b += f'<circle cx="{CX}" cy="{CY}" r="{ER}" fill="none" stroke="#bfe6ff" stroke-width="4" opacity=".7"/>'
    b += belt('front5')

    def sat(x, y, rot, s, dead=False):
        o = f'<g transform="translate({x} {y}) rotate({rot}) scale({s})">'
        o += '<rect x="-62" y="-12" width="44" height="24" fill="#2a4a8a" stroke="#0b0f1c" stroke-width="3"/><rect x="18" y="-12" width="44" height="24" fill="#2a4a8a" stroke="#0b0f1c" stroke-width="3"/>'
        o += '<line x1="-18" y1="0" x2="18" y2="0" stroke="#999" stroke-width="4"/><rect x="-16" y="-18" width="32" height="36" rx="4" fill="#d9b860" stroke="#0b0f1c" stroke-width="3"/>'
        o += '<path d="M0 -18 l0 -14 m0 0 q-10 -4 -16 2" fill="none" stroke="#ccc" stroke-width="3"/>'
        for k in range(4):
            q = math.radians(-120 + k * 70); r0 = 26
            o += (f'<path d="M{r0 * math.cos(q):.0f} {r0 * math.sin(q):.0f} l{14 * math.cos(q) + 6:.0f} {14 * math.sin(q):.0f} l-8 5 l{16 * math.cos(q) + 4:.0f} {16 * math.sin(q):.0f}" '
                  f'fill="none" stroke="#ffe46a" stroke-width="4" stroke-linejoin="round"/>')
        if dead:
            o += '<path d="M-6 -6 l12 12 M6 -6 l-12 12" stroke="#1a1a1a" stroke-width="3"/>'
        return o + '</g>' + f'<circle cx="{x}" cy="{y}" r="{40 * s:.0f}" fill="#ffe46a" opacity=".18" filter="url(#b12)"/>'
    a = math.radians(ROT)
    for t, s, dead in ((200, .95, False), (330, .8, True), (30, .9, False), (120, .75, True)):
        tt = math.radians(t); lx, ly = RX * math.cos(tt), RY * math.sin(tt)
        x = CX + lx * math.cos(a) - ly * math.sin(a); y = CY + lx * math.sin(a) + ly * math.cos(a)
        b += sat(round(x), round(y), random.randint(-30, 30), s, dead)
    # a dead satellite drifting away up-right, trailing smoke
    for k in range(9):
        b += f'<circle cx="{870 - k * 24}" cy="{400 + k * 16}" r="{8 + k * 2}" fill="#7a8090" opacity="{.35 - k * .035:.2f}"/>'
    b += sat(890, 388, 40, .9, True)
    # ---- frog in helmet floating top-left, holding a fried little satellite, startled, looking down at the belt ----
    held = ('<g transform="translate(78 -10) rotate(-20) scale(.55)">'
            '<rect x="-62" y="-12" width="44" height="24" fill="#2a4a8a" stroke-width="4"/><rect x="18" y="-12" width="44" height="24" fill="#2a4a8a" stroke-width="4"/>'
            '<rect x="-16" y="-18" width="32" height="36" rx="4" fill="#d9b860" stroke-width="4"/>'
            '<path d="M-10 -26 q6 -14 0 -26 q10 10 4 26" fill="#6a6f7a" stroke="none" opacity=".7"/></g>')
    b += frog(250, 580, 2.9, look=(5, 4), mouth='wow', helmet=True, rot=-10,
              armL='M-34 -22 q-24 -6 -28 -34', armR='M38 -22 q22 4 34 2', feet=((-26, 8, -24), (26, 6, 26)), front=held)
    for x, y, s in ((980, 650, 18), (100, 760, 14), (60, 1760, 12), (1010, 1700, 14)):
        b += spark(x, y, s)
    return vpage('#02040a', vsvg(d, b), [('A <span class="g">GHOST</span>', 175, 'w'), ('AROUND', 165, 'w'), ('EARTH', 200, 'w')], top=640)


for n, fn in ((1, make_1), (2, make_2), (3, make_3), (4, make_4), (5, make_5)):
    open(os.path.join(VID, f'space-nuke-short{n}', 'thumb', 'A.html'), 'w').write(fn())
print('ok')
