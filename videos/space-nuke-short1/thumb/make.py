# Shorts thumbnails for space-nuke-short1..5 (guideline 16-9, brief tools/briefs/thumb_art.md 'Shorts thumbnails').
# One shared generator: writes videos/space-nuke-shortN/thumb/A.html for N = 1..5.
# Reuses frog(), trefoil(), GLOW from the long-form generator videos/space-nuke/thumb/make.py (helpers only, not its pages).
# 1 NOT A SOUND          - blue-white flash, frog in helmet presses a brass ear trumpet to its visor, sound wave flatlines.
# 2 NO MUSHROOM CLOUD    - dashed ghost mushroom (struck through, fading) vs a glowing amber plasma sphere ("a miniature, temporary star").
# 3 THE INVISIBLE KILLER - ghostly X-ray waves hit a big spacecraft hull: skin vaporizes, blows off, cracks; frog peeks through a porthole.
# 4 1962: WE NUKED SPACE - Starfish Prime seen from high above the night Pacific: flash over the Earth's edge, island chain below, frog with binoculars.
# 5 A GHOST AROUND EARTH - glowing man-made radiation belt (doughnut) trapped around Earth, sparking satellites, frog in helmet with a dead satellite.
# run: python3 make.py
import os, sys, math, random
HERE = os.path.dirname(os.path.abspath(__file__))
VID = os.path.abspath(os.path.join(HERE, '..', '..'))
sys.path.insert(0, os.path.join(VID, '..', 'tools'))
from thumb_lib import page, svg, lin, rad, stars, spark, blobs
_src = open(os.path.join(VID, 'space-nuke', 'thumb', 'make.py')).read()
exec(_src[_src.index("INK = "):_src.index('# ====')])   # INK/GREEN..., arm, hand_dot, frog, GLOW, trefoil


def flare(cx, cy, n, L1, L2, col='#fff', w=5, op=.55, off=0):
    return ''.join(f'<line x1="{cx}" y1="{cy}" x2="{cx + (L1 if k % 2 == 0 else L2) * math.cos(math.radians(off + k * 360 / n)):.0f}" '
                   f'y2="{cy + (L1 if k % 2 == 0 else L2) * math.sin(math.radians(off + k * 360 / n)):.0f}" stroke="{col}" stroke-width="{w}" '
                   f'stroke-linecap="round" opacity="{op}" filter="url(#b4)"/>' for k in range(n))


# =====================================================================================
# 1: NOT A SOUND
# =====================================================================================
def make_1():
    random.seed(101)
    FX, FY = 1330, 400
    d = GLOW
    d += rad('h1', FX, FY, 1000, [(0, '#ffffff', .75), (.12, '#d8f2ff', .5), (.32, '#5fb8ff', .16), (.6, '#2a4fb0', .05), (1, '#0a1030', 0)])
    d += rad('c1', FX, FY, 260, [(0, '#ffffff', 1), (.25, '#ffffff', .98), (.5, '#cfeeff', .7), (.8, '#7cc6ff', .2), (1, '#7cc6ff', 0)])
    d += lin('brass', [(0, '#fff1b8'), (.3, '#f0c45a'), (.7, '#b07a22'), (1, '#6a4410')])
    d += rad('bell', 0, 0, 34, [(0, '#2a1806', 1), (.7, '#6a4410', 1), (1, '#f0c45a', 1)])
    b = '<rect width="1920" height="1080" fill="#02040c"/>'
    b += stars(230, 1070, col='#dfeaff', op=.5, sparks=0)
    b += f'<circle cx="{FX}" cy="{FY}" r="1000" fill="url(#h1)"/>'
    # ring shells of light
    for r, op in ((380, .18), (470, .1), (570, .06)):
        b += f'<circle cx="{FX}" cy="{FY}" r="{r}" fill="none" stroke="#bfe6ff" stroke-width="6" opacity="{op}" filter="url(#b4)"/>'
    # long light streaks
    for k in range(70):
        a = random.uniform(0, 2 * math.pi); r0 = random.uniform(120, 260); r1 = r0 + random.uniform(300, 1000)
        b += (f'<line x1="{FX + r0 * math.cos(a):.0f}" y1="{FY + r0 * math.sin(a):.0f}" x2="{FX + r1 * math.cos(a):.0f}" y2="{FY + r1 * math.sin(a):.0f}" '
              f'stroke="{random.choice(["#e8f6ff", "#cfe8ff", "#fffbe8"])}" stroke-width="{random.choice([1.5, 2, 3])}" opacity="{random.uniform(.08, .3):.2f}"/>')
    b += f'<circle cx="{FX}" cy="{FY}" r="300" fill="#9fdcff" opacity=".35" filter="url(#b60)"/>'
    b += f'<circle cx="{FX}" cy="{FY}" r="260" fill="url(#c1)"/>'
    b += flare(FX, FY, 8, 560, 330, w=9, op=.7, off=22)
    b += flare(FX, FY, 16, 260, 180, w=3, op=.5, off=11)
    b += f'<circle cx="{FX}" cy="{FY}" r="90" fill="#fff" filter="url(#b12)"/>'
    # horizontal anamorphic streak
    b += f'<ellipse cx="{FX}" cy="{FY}" rx="560" ry="10" fill="#d8f2ff" opacity=".6" filter="url(#b4)"/>'
    # ---- the sound wave: loud near the flash, flattening to a dead line before the trumpet ----
    x0, y0, x1, y1 = FX - 200, FY + 60, 960, 730
    pts = []
    N = 260
    for i in range(N + 1):
        t = i / N
        x = x0 + (x1 - x0) * t; y = y0 + (y1 - y0) * t
        amp = 120 * max(0, 1 - t / .7) ** 1.4
        nx, ny = -(y1 - y0), (x1 - x0); L = math.hypot(nx, ny); nx /= L; ny /= L
        o = amp * math.sin(t * 40)
        pts.append((x + nx * o, y + ny * o))
    path = 'M' + ' L'.join(f'{x:.1f} {y:.1f}' for x, y in pts)
    b += f'<path d="{path}" fill="none" stroke="#7fd6ff" stroke-width="22" opacity=".35" filter="url(#b12)"/>'
    b += f'<path d="{path}" fill="none" stroke="#e8f8ff" stroke-width="10" stroke-linejoin="round"/>'
    # dead end of the line: dotted, fading

    # ---- frog in helmet pressing a brass ear trumpet to the visor ----
    horn = ('<g>'
            '<path d="M56 -50 Q90 -54 118 -76 L150 -112 Q168 -78 160 -50 L120 -52 Q92 -44 58 -40Z" fill="url(#brass)" stroke-width="3.4"/>'
            '<g transform="translate(156 -82) rotate(-35)"><ellipse rx="22" ry="38" fill="url(#bell)" stroke-width="3.4"/></g>'
            '<path d="M64 -48 Q92 -50 120 -70" fill="none" stroke="#fff6d0" stroke-width="3" opacity=".8"/>'
            '<rect x="50" y="-54" width="10" height="16" rx="3" fill="#8a5a1a" stroke-width="2.6"/></g>')
    b += '<ellipse cx="420" cy="1020" rx="150" ry="16" fill="#7fd6ff" opacity=".08"/>'
    b += frog(400, 1000, 3.05, look=(5, -2), mouth='wow', helmet=True, rot=4,
              armL='M-34 -22 q-18 10 -14 28', armR='M38 -22 q30 4 62 -26', front=horn)
    # tiny "?" floating by the bell
    b += '<text x="600" y="640" font-family="Fredoka" font-weight="700" font-size="90" fill="#e8f8ff" stroke="#050b18" stroke-width="8" paint-order="stroke" opacity=".9">?</text>'
    for x, y, s in ((1000, 130, 18), (1780, 120, 22), (1820, 640, 14), (900, 470, 12)):
        b += spark(x, y, s)
    return page('#02040c', svg(d, b), [('NOT A', 170, 'w'), ('SOUND', 270, 'y')], top=50)


# =====================================================================================
# 2: NO MUSHROOM CLOUD
# =====================================================================================
def make_2():
    random.seed(202)
    CX, CY, R = 1370, 470, 330
    d = GLOW
    d += rad('h2', CX, CY, 950, [(0, '#fff6dc', .6), (.22, '#ffcf7a', .25), (.5, '#ff7a3a', .07), (1, '#3a0f10', 0)])
    d += rad('s2', CX, CY, R, [(0, '#ffffff', .95), (.25, '#fff1c4', .8), (.55, '#ffc062', .55), (.82, '#ff8a3a', .5), (.95, '#ffe0a0', .9), (1, '#fff', 0)])
    d += rad('k2', CX, CY, 140, [(0, '#ffffff', 1), (.5, '#fff5d0', .9), (1, '#ffd070', 0)])
    d += lin('gh', [(0, '#bcd2ff'), (1, '#6d84b8')])
    b = '<rect width="1920" height="1080" fill="#05040a"/>'
    b += stars(220, 1070, col='#f0e8ff', op=.5, sparks=0)
    b += f'<circle cx="{CX}" cy="{CY}" r="950" fill="url(#h2)"/>'
    for k in range(60):
        a = random.uniform(0, 2 * math.pi); r0 = R * random.uniform(.85, 1.05); r1 = r0 + random.uniform(200, 700)
        b += (f'<line x1="{CX + r0 * math.cos(a):.0f}" y1="{CY + r0 * math.sin(a):.0f}" x2="{CX + r1 * math.cos(a):.0f}" y2="{CY + r1 * math.sin(a):.0f}" '
              f'stroke="{random.choice(["#fff3d0", "#ffd9a0", "#ffffff"])}" stroke-width="{random.choice([1.5, 2, 3])}" opacity="{random.uniform(.08, .25):.2f}"/>')
    # debris flecks flying out in every direction
    for k in range(90):
        a = random.uniform(0, 2 * math.pi); r = R * random.uniform(1.05, 1.7)
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
    b += f'<circle cx="{CX}" cy="{CY}" r="140" fill="url(#k2)"/>'
    b += f'<circle cx="{CX}" cy="{CY}" r="60" fill="#fff" filter="url(#b12)"/>'
    b += flare(CX, CY, 8, 300, 190, w=6, op=.6, off=0)
    # expansion arrows (every direction at once)
    for ang in range(0, 360, 45):
        a = math.radians(ang + 22.5); r0, r1 = R + 40, R + 120
        x0, y0, x2, y2 = CX + r0 * math.cos(a), CY + r0 * math.sin(a), CX + r1 * math.cos(a), CY + r1 * math.sin(a)
        if (x2 > 1660 and y2 > 760) or x2 < 1100:
            continue   # keep bottom-right clear
        hx, hy = math.cos(a), math.sin(a)
        b += (f'<line x1="{x0:.0f}" y1="{y0:.0f}" x2="{x2:.0f}" y2="{y2:.0f}" stroke="#fff1c8" stroke-width="7" stroke-linecap="round" opacity=".8"/>'
              f'<path d="M{x2 + hx * 22:.0f} {y2 + hy * 22:.0f} L{x2 - hy * 16:.0f} {y2 + hx * 16:.0f} L{x2 + hy * 16:.0f} {y2 - hx * 16:.0f}Z" fill="#fff1c8" opacity=".8"/>')
    # ---- ghost mushroom cloud (dashed outline, faint fill, struck through, crumbling) ----
    MX, MY = 690, 640
    mush = (f'M{MX - 70} 1000 L{MX - 50} {MY + 160} Q{MX - 60} {MY + 130} {MX - 150} {MY + 132} '
            f'Q{MX - 250} {MY + 120} {MX - 240} {MY + 50} Q{MX - 250} {MY - 10} {MX - 180} {MY - 30} '
            f'Q{MX - 150} {MY - 100} {MX - 60} {MY - 90} Q{MX} {MY - 140} {MX + 70} {MY - 92} '
            f'Q{MX + 160} {MY - 100} {MX + 190} {MY - 30} Q{MX + 260} {MY - 10} {MX + 250} {MY + 50} '
            f'Q{MX + 260} {MY + 120} {MX + 160} {MY + 132} Q{MX + 60} {MY + 130} {MX + 50} {MY + 160} L{MX + 70} 1000Z')
    b += f'<path d="{mush}" fill="#c8d8ff" opacity=".07"/><path d="{mush}" fill="none" stroke="#9fb8ff" stroke-width="30" opacity=".12" filter="url(#b12)"/>'
    b += f'<path d="{mush}" fill="none" stroke="#c8d8ff" stroke-width="7" stroke-dasharray="26 18" stroke-linecap="round" opacity=".8"/>'
    b += f'<path d="M{MX - 150} {MY + 40} q60 -30 120 0 q60 -30 120 0" fill="none" stroke="#c8d8ff" stroke-width="5" stroke-dasharray="14 14" opacity=".45"/>'
    b += f'<path d="M{MX - 50} {MY + 230} q50 20 100 0 M{MX - 55} {MY + 300} q55 20 110 0" fill="none" stroke="#c8d8ff" stroke-width="5" stroke-dasharray="14 14" opacity=".4"/>'
    # hand-drawn strike (chalky double stroke)
    b += f'<path d="M{MX - 190} {MY + 250} Q{MX + 10} {MY + 90} {MX + 240} {MY - 110}" fill="none" stroke="#050b18" stroke-width="30" stroke-linecap="round" opacity=".7"/>'
    b += f'<path d="M{MX - 190} {MY + 250} Q{MX + 10} {MY + 90} {MX + 240} {MY - 110}" fill="none" stroke="#f4f0e6" stroke-width="14" stroke-linecap="round"/>'
    b += f'<path d="M{MX - 172} {MY + 266} Q{MX + 20} {MY + 110} {MX + 230} {MY - 90}" fill="none" stroke="#f4f0e6" stroke-width="5" stroke-linecap="round" opacity=".6"/>'
    # crumbling dashes drifting away from the right edge of the cap (it fades out)
    r2 = random.Random(7)
    for k in range(16):
        x = MX + 250 + r2.randint(10, 200); y = MY - 60 + r2.randint(-40, 160)
        b += f'<rect x="{x}" y="{y}" width="{r2.randint(10, 22)}" height="6" rx="3" fill="#c8d8ff" opacity="{r2.uniform(.15, .5):.2f}" transform="rotate({r2.randint(-40, 40)} {x} {y})"/>'
    # ---- frog in helmet next to the stem, staring at the sphere ----
    b += frog(250, 1000, 3.0, look=(6, -3), mouth='wow', helmet=True, rot=6,
              armL='M-34 -22 q-18 8 -16 26', armR='M38 -24 q14 -4 18 -30')
    for x, y, s in ((1000, 90, 18), (1820, 110, 22), (1840, 600, 14), (1060, 860, 14)):
        b += spark(x, y, s)
    return page('#05040a', svg(d, b), [('NO', 200, 'y'), ('MUSHROOM', 158, 'w'), ('CLOUD', 190, 'w')], top=36)


# =====================================================================================
# 3: THE INVISIBLE KILLER
# =====================================================================================
def make_3():
    random.seed(303)
    FX, FY = 1720, 170
    d = GLOW
    d += rad('h3', FX, FY, 900, [(0, '#ffffff', .7), (.15, '#e6d8ff', .35), (.45, '#7a5cff', .08), (1, '#140a30', 0)])
    d += lin('hull', [(0, '#f4f4f0'), (.22, '#d6d8dc'), (.6, '#8d929b'), (.88, '#4a4f58'), (1, '#262a31')])
    d += lin('foil', [(0, '#fff2b0'), (.4, '#e2b24a'), (.8, '#9a6a1c'), (1, '#5a3a0c')])
    d += rad('hot', 0, 0, 200, [(0, '#ffffff', 1), (.2, '#fff2c0', .95), (.5, '#ff9a3a', .6), (1, '#ff5a1a', 0)])
    d += rad('win', 0, 0, 120, [(0, '#2a3a5a', 1), (.8, '#141c30', 1), (1, '#0a0f1c', 1)])
    d += '<clipPath id="port"><circle cx="0" cy="0" r="104"/></clipPath>'
    b = '<rect width="1920" height="1080" fill="#04030b"/>'
    b += stars(220, 1070, col='#e6e2ff', op=.5, sparks=0)
    b += f'<circle cx="{FX}" cy="{FY}" r="900" fill="url(#h3)"/>'
    b += f'<circle cx="{FX}" cy="{FY}" r="70" fill="#fff" filter="url(#b12)"/>'
    b += flare(FX, FY, 8, 220, 130, w=5, op=.6, off=10)
    # ---- ghostly X-ray waves (barely visible, dashed sine) flowing down-left to the hull ----
    tx, ty = 1240, 600   # impact zone
    waves = ''
    for k in range(9):
        off = (k - 4) * 46
        sx, sy = FX - 60 + off * .5, FY + 60 + off * .6
        ex, ey = tx + 60 - off * .4, ty + off * 2.2
        L = math.hypot(ex - sx, ey - sy); ux, uy = (ex - sx) / L, (ey - sy) / L; nx, ny = -uy, ux
        p = []
        for i in range(121):
            t = i / 120; o = 20 * math.sin(t * 30 + k)
            p.append((sx + (ex - sx) * t + nx * o, sy + (ey - sy) * t + ny * o))
        pd = 'M' + ' L'.join(f'{x:.0f} {y:.0f}' for x, y in p)
        waves += f'<path d="{pd}" fill="none" stroke="#e2d6ff" stroke-width="5" stroke-dasharray="3 14" stroke-linecap="round" opacity="{.55 if k % 2 else .35}"/>'
        waves += f'<path d="{pd}" fill="none" stroke="#b49cff" stroke-width="16" opacity=".07"/>'
    b += f'<g filter="url(#b4)">{waves}</g>'
    # ---- the hull: big cylindrical module, axis tilted, struck end facing the flash ----
    h = '<g transform="translate(760 760) rotate(-14)">'
    h += '<ellipse cx="-560" cy="0" rx="70" ry="210" fill="#3a3f48" stroke="#0b0d14" stroke-width="6"/>'
    h += '<path d="M-560 -210 L470 -210 L470 210 L-560 210Z" fill="url(#hull)" stroke="#0b0d14" stroke-width="6"/>'
    for sx in range(-460, 470, 120):   # rings and rivets
        h += f'<line x1="{sx}" y1="-210" x2="{sx}" y2="210" stroke="#3b4048" stroke-width="4" opacity=".6"/>'
        for ry in range(-190, 200, 32):
            h += f'<circle cx="{sx + 10}" cy="{ry}" r="3.4" fill="#2c3036" opacity=".55"/>'
    h += '<rect x="-520" y="40" width="380" height="120" fill="url(#foil)" opacity=".85" stroke="#0b0d14" stroke-width="4"/>'
    h += ''.join(f'<path d="M{-520 + k * 38} 40 l12 120" stroke="#6a4a10" stroke-width="2" opacity=".5"/>' for k in range(10))
    h += '<path d="M-560 -184 L470 -184" stroke="#fff" stroke-width="12" opacity=".7" stroke-linecap="round"/>'
    h += '<path d="M-560 196 L470 196" stroke="#8a7cff" stroke-width="6" opacity=".35"/>'
    h += '<text x="-20" y="150" font-family="Fredoka" font-weight="700" font-size="44" fill="#2c3036" opacity=".55" letter-spacing="6">MN-1</text>'
    # struck end: hot glowing skin, end cap
    h += '<ellipse cx="470" cy="0" rx="70" ry="210" fill="#c9cdd4" stroke="#0b0d14" stroke-width="6"/>'
    h += '<g transform="translate(400 -40)"><circle r="200" fill="url(#hot)"/></g>'
    h += '<ellipse cx="470" cy="0" rx="70" ry="210" fill="#ffb060" opacity=".45"/>'
    # cracks running back along the hull
    for path in ('M420 -120 l-60 30 l-30 -20 l-70 40 l-40 -10', 'M430 40 l-50 -10 l-40 40 l-90 0 l-30 30', 'M380 -10 l-70 -40 l-60 10',
                 'M440 140 l-60 10 l-30 30'):
        h += f'<path d="{path}" fill="none" stroke="#1a0c04" stroke-width="9" stroke-linejoin="round"/>'
        h += f'<path d="{path}" fill="none" stroke="#ffb040" stroke-width="3.5" stroke-linejoin="round"/>'
    # peeled skin flaps lifting off
    h += '<path d="M460 -200 q60 -40 120 -110 l14 30 q-50 70 -110 96z" fill="#d6d8dc" stroke="#0b0d14" stroke-width="5"/>'
    h += '<path d="M500 60 q80 -10 150 -70 l6 34 q-64 52 -140 62z" fill="#c2c6cc" stroke="#0b0d14" stroke-width="5"/>'
    # porthole frame (frog drawn after the group)
    h += '<circle cx="-300" cy="-60" r="122" fill="#5d636c" stroke="#0b0d14" stroke-width="6"/>'
    h += ''.join(f'<circle cx="{-300 + 112 * math.cos(math.radians(a)):.0f}" cy="{-60 + 112 * math.sin(math.radians(a)):.0f}" r="5" fill="#2c3036"/>' for a in range(0, 360, 30))
    h += '</g>'
    b += h
    # porthole glass + peeking frog (porthole centre in screen coords)
    a = math.radians(-14); pcx = 760 + (-300) * math.cos(a) - (-60) * math.sin(a); pcy = 760 + (-300) * math.sin(a) + (-60) * math.cos(a)
    b += f'<g transform="translate({pcx:.0f} {pcy:.0f})"><circle r="104" fill="url(#win)"/><g clip-path="url(#port)">'
    b += frog(-6, 150, 2.7, look=(6, -3), mouth='wow', rot=0, pupil=6, armL='M-34 -22 q-10 -10 -4 -32', armR='M38 -22 q10 -10 4 -32')
    b += '<path d="M-80 -40 q30 -50 90 -60" fill="none" stroke="#fff" stroke-width="10" opacity=".35"/><circle r="104" fill="#9fc6ff" opacity=".12"/></g>'
    b += '<circle r="104" fill="none" stroke="#c9ced8" stroke-width="8"/></g>'
    # vaporised metal bursting out toward the source (blow-off) + shock rings
    bx_, by_ = 760 + 470 * math.cos(a) + 30, 760 + 470 * math.sin(a) - 40
    puff = ''
    r3 = random.Random(31)
    for k in range(60):
        ang = math.radians(r3.uniform(-80, 20)); dist = r3.uniform(20, 260)
        puff += (f'<circle cx="{bx_ + dist * math.cos(ang):.0f}" cy="{by_ + dist * math.sin(ang):.0f}" r="{r3.randint(8, 30)}" '
                 f'fill="{r3.choice(["#fff1d6", "#ffd090", "#ffa050", "#ffffff"])}" opacity="{r3.uniform(.2, .6):.2f}"/>')
    b += f'<g filter="url(#b4)">{puff}</g>'
    b += f'<circle cx="{bx_:.0f}" cy="{by_:.0f}" r="120" fill="#ffd090" opacity=".4" filter="url(#b30)"/>'
    for r, op in ((150, .5), (210, .3), (270, .15)):
        b += f'<path d="M{bx_ - r * .2:.0f} {by_ - r:.0f} A{r} {r} 0 0 1 {bx_ + r * .9:.0f} {by_ + r * .3:.0f}" fill="none" stroke="#ffe6b0" stroke-width="6" opacity="{op}"/>'
    for x, y, s in ((1060, 120, 16), (1500, 520, 14), (880, 380, 12), (1840, 520, 18)):
        b += spark(x, y, s)
    return page('#04030b', svg(d, b), [('THE', 120, 'w'), ('INVISIBLE', 190, 'y'), ('KILLER', 210, 'w')], top=36)


# =====================================================================================
# 4: 1962: WE NUKED SPACE
# =====================================================================================
def make_4():
    random.seed(404)
    FX, FY = 1360, 250
    EX, EY, ER = 960, 3700, 3020   # Earth: horizon peaks at y=680
    d = GLOW
    d += rad('atm4', EX, EY, ER + 90, [(0, '#000', 0), (.96, '#1d4fa0', 0), (.975, '#5fa8ff', .7), (.99, '#2a5fc0', .25), (1, '#000', 0)])
    d += rad('sea4', EX, EY, ER, [(0, '#020812', 1), (.9, '#06142c', 1), (.985, '#0c2a56', 1), (1, '#2a5fa0', 1)])
    d += rad('f4', FX, FY, 700, [(0, '#ffffff', 1), (.06, '#f4fbff', .95), (.18, '#c8e6ff', .5), (.45, '#6aa0ff', .12), (1, '#6aa0ff', 0)])
    d += lin('isl', [(0, '#2c3a2c'), (1, '#0b120c')])
    d += lin('aurG', [(0, '#7dffb0'), (1, '#2fd08a')])
    d += f'<clipPath id="e4"><circle cx="{EX}" cy="{EY}" r="{ER}"/></clipPath>'
    b = '<rect width="1920" height="1080" fill="#02030a"/>'
    b += stars(200, 700, col='#e8eeff', op=.55, sparks=0)
    b += f'<circle cx="{EX}" cy="{EY}" r="{ER + 90}" fill="url(#atm4)"/>'
    # field-line auroras: red/green loops from the flash down to the limb
    au = ''
    for k, (dx, col, w, op) in enumerate(((-520, '#ff4f6e', 26, .35), (-380, '#7dffb0', 22, .45), (-250, '#ff5f7e', 18, .35),
                                          (260, '#7dffb0', 22, .45), (400, '#ff4f6e', 26, .35), (540, '#7dffb0', 16, .3))):
        au += f'<path d="M{FX + dx * .25:.0f} {FY + 30} Q{FX + dx * 1.15:.0f} {FY + 40} {FX + dx:.0f} 690" fill="none" stroke="{col}" stroke-width="{w}" opacity="{op}"/>'
    b += f'<g filter="url(#b12)">{au}</g>'
    # ocean (night side) with island chain
    b += f'<circle cx="{EX}" cy="{EY}" r="{ER}" fill="url(#sea4)"/>'
    eg = f'<g clip-path="url(#e4)">'
    eg += f'<ellipse cx="{FX}" cy="760" rx="520" ry="70" fill="#bfe0ff" opacity=".22" filter="url(#b30)"/>'   # flash on the sea
    for i in range(46):
        y = 700 + i * 8; w = 30 + i * 9
        eg += f'<rect x="{FX - w / 2 + random.randint(-30, 30):.0f}" y="{y}" width="{w:.0f}" height="3" fill="#dff1ff" opacity="{max(.04, .45 - i * .009):.2f}"/>'
    for i in range(70):   # aurora glints on the sea
        x = random.randint(700, 1900); y = random.randint(700, 1060)
        eg += f'<rect x="{x}" y="{y}" width="{random.randint(14, 50)}" height="3" fill="{random.choice(["#5dff9a", "#ff5f7e"])}" opacity="{random.uniform(.06, .2):.2f}"/>'
    # cloud wisps
    r2 = random.Random(4)
    for _ in range(26):
        x = r2.randint(-100, 2000); y = r2.randint(700, 860); rx = r2.randint(40, 160)
        eg += f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{rx * .12:.0f}" fill="#9fb8e0" opacity="{r2.uniform(.06, .16):.2f}" filter="url(#b4)"/>'
    eg += '</g>'
    b += eg
    b += f'<circle cx="{EX}" cy="{EY}" r="{ER}" fill="none" stroke="#9fd0ff" stroke-width="5" opacity=".6"/>'
    # island chain receding toward the horizon (far: small with town lights)
    for x, y, s in ((1210, 724, .16), (1090, 738, .22), (950, 760, .32), (790, 800, .48)):
        b += f'<path d="M{x - 120 * s:.0f} {y} Q{x - 40 * s:.0f} {y - 50 * s:.0f} {x:.0f} {y - 70 * s:.0f} Q{x + 50 * s:.0f} {y - 40 * s:.0f} {x + 130 * s:.0f} {y}Z" fill="url(#isl)" stroke="#9fd0ff" stroke-width="1.5" stroke-opacity=".4"/>'
        for k in range(int(10 * s) + 2):
            b += f'<circle cx="{x + random.uniform(-90, 90) * s:.0f}" cy="{y - random.uniform(2, 12) * s:.0f}" r="{max(1.4, 4 * s):.1f}" fill="#ffd27a" opacity=".9"/>'
    # near island (foreground, bottom-left): volcano, palms, surf
    b += '<g transform="translate(0 120)"><path d="M-40 1080 L-40 900 Q120 820 260 760 Q330 735 380 770 Q520 860 700 900 Q780 930 820 1080Z" fill="url(#isl)"/>'
    b += '<path d="M200 790 Q260 760 300 752 Q340 748 380 770" fill="none" stroke="#7fe0b0" stroke-width="4" opacity=".35"/>'
    b += '<path d="M-40 900 Q120 820 260 760 Q330 735 380 770 Q520 860 700 900 Q780 930 820 1080" fill="none" stroke="#ff9db0" stroke-width="3" opacity=".25"/>'
    b += '<path d="M660 905 q60 10 110 40 M720 950 q40 20 70 60" fill="none" stroke="#dff1ff" stroke-width="4" opacity=".35"/>'
    for px, py, hgt, lean in ((560, 880, 170, 14), (650, 900, 130, 22)):
        tx, ty = px + lean, py - hgt
        b += f'<path d="M{px} {py} Q{px + lean * .3:.0f} {py - hgt * .6:.0f} {tx} {ty}" fill="none" stroke="#0a0f0a" stroke-width="12" stroke-linecap="round"/>'
        for ang in (-170, -130, -60, -20, 20, 160):
            a = math.radians(ang); L = hgt * .5
            b += f'<path d="M{tx} {ty} Q{tx + L * .6 * math.cos(a):.0f} {ty + L * .6 * math.sin(a) - 24:.0f} {tx + L * math.cos(a):.0f} {ty + L * math.sin(a) + 18:.0f}" fill="none" stroke="#0a0f0a" stroke-width="10" stroke-linecap="round"/>'
    b += '</g>'
    # ---- the flash, far above the edge of the Earth ----
    b += f'<circle cx="{FX}" cy="{FY}" r="700" fill="url(#f4)"/>'
    b += f'<circle cx="{FX}" cy="{FY}" r="120" fill="#e6f4ff" opacity=".6" filter="url(#b30)"/>'
    b += f'<circle cx="{FX}" cy="{FY}" r="66" fill="#fff" filter="url(#b12)"/>'
    b += flare(FX, FY, 12, 300, 170, w=5, op=.55, off=15)
    b += f'<circle cx="{FX}" cy="{FY}" r="210" fill="none" stroke="#e8f4ff" stroke-width="5" opacity=".35" filter="url(#b4)"/>'
    # dashed altitude marker (no number on it; just distance up from the sea)
    b += f'<line x1="{FX}" y1="{FY + 90}" x2="{FX}" y2="680" stroke="#e8f4ff" stroke-width="4" stroke-dasharray="6 16" stroke-linecap="round" opacity=".45"/>'
    # ---- frog on the near island, binoculars up at the flash ----
    bino = ('<g transform="translate(0 64) rotate(-12 6 -66)">'
            '<rect x="-24" y="-80" width="24" height="56" rx="8" fill="#2b2f36" stroke-width="3.2" transform="rotate(0)"/>'
            '<rect x="10" y="-80" width="24" height="56" rx="8" fill="#2b2f36" stroke-width="3.2"/>'
            '<rect x="-2" y="-62" width="14" height="14" fill="#444a54" stroke-width="2.6"/>'
            '<ellipse cx="-12" cy="-80" rx="12" ry="5" fill="#8fd0ff" stroke-width="2.6"/><ellipse cx="22" cy="-80" rx="12" ry="5" fill="#8fd0ff" stroke-width="2.6"/>'
            '<path d="M-18 -74 l0 40 M16 -74 l0 40" stroke="#6a7280" stroke-width="3" opacity=".7"/></g>')
    flower = ('<g transform="translate(-30 -82)">' + ''.join(
        f'<circle cx="{9 * math.cos(math.radians(a)):.1f}" cy="{9 * math.sin(math.radians(a)):.1f}" r="7" fill="#ff7aa8" stroke-width="2"/>' for a in range(0, 360, 72))
        + '<circle r="5" fill="#ffd35a" stroke-width="2"/></g>')
    b += '<ellipse cx="330" cy="874" rx="100" ry="13" fill="#000" opacity=".35"/>'
    b += frog(330, 868, 2.7, look=(7, -6), mouth='wow', rot=-8,
              armL='M-34 -22 q8 4 22 8', armR='M38 -22 q-6 4 -12 10', front=bino + flower)
    for x, y, s in ((960, 120, 18), (1760, 90, 20), (1820, 470, 14), (1080, 520, 12)):
        b += spark(x, y, s)
    return page('#02030a', svg(d, b), [('1962:', 200, 'y'), ('WE NUKED', 170, 'w'), ('SPACE', 210, 'w')], top=34)


# =====================================================================================
# 5: A GHOST AROUND EARTH
# =====================================================================================
def make_5():
    random.seed(505)
    CX, CY, ER = 1260, 560, 250
    RX, RY, ROT = 600, 165, -12
    d = GLOW
    d += rad('earth5', CX - 80, CY - 90, ER * 1.3, [(0, '#7fc8ff', 1), (.4, '#2a7ad0', 1), (.8, '#103e84', 1), (1, '#061a3c', 1)])
    d += rad('atm5', CX, CY, ER + 40, [(0, '#000', 0), (.85, '#5fb0ff', 0), (.9, '#8fd0ff', .7), (1, '#2a6fd0', 0)])
    d += rad('night5', CX + 160, CY + 120, ER * 1.2, [(0, '#000814', .85), (.6, '#000814', .45), (1, '#000814', 0)])
    d += rad('g5', CX, CY, 900, [(0, '#5fffd0', .16), (.4, '#3a8aff', .06), (1, '#000', 0)])
    d += f'<clipPath id="ec5"><circle cx="{CX}" cy="{CY}" r="{ER}"/></clipPath>'
    d += f'<clipPath id="front5"><rect x="{CX - 1000}" y="{CY}" width="2000" height="600"/></clipPath>'
    d += f'<clipPath id="back5"><rect x="{CX - 1000}" y="{CY - 600}" width="2000" height="600"/></clipPath>'
    b = '<rect width="1920" height="1080" fill="#02040a"/>'
    b += stars(240, 1070, col='#e2f0ff', op=.5, sparks=0)
    b += f'<circle cx="{CX}" cy="{CY}" r="900" fill="url(#g5)"/>'

    def belt(clip):
        o = f'<g transform="rotate({ROT} {CX} {CY})" clip-path="url(#{clip})">'
        o += f'<ellipse cx="{CX}" cy="{CY}" rx="{RX}" ry="{RY}" fill="none" stroke="#3affc8" stroke-width="150" opacity=".16" filter="url(#b30)"/>'
        o += f'<ellipse cx="{CX}" cy="{CY}" rx="{RX}" ry="{RY}" fill="none" stroke="#8a6aff" stroke-width="90" opacity=".16" filter="url(#b12)"/>'
        o += f'<ellipse cx="{CX}" cy="{CY}" rx="{RX}" ry="{RY}" fill="none" stroke="#9fffe0" stroke-width="40" opacity=".35" filter="url(#b12)"/>'
        o += f'<ellipse cx="{CX}" cy="{CY}" rx="{RX}" ry="{RY}" fill="none" stroke="#eafff8" stroke-width="8" opacity=".7" filter="url(#b4)"/>'
        for rx, ry, op in ((RX - 60, RY - 30, .4), (RX + 60, RY + 26, .3)):
            o += f'<ellipse cx="{CX}" cy="{CY}" rx="{rx}" ry="{ry}" fill="none" stroke="#bfffee" stroke-width="3" stroke-dasharray="4 18" opacity="{op}"/>'
        # trapped electrons: bright specks along the ring with tiny motion streaks
        r = random.Random(11 if clip == 'back5' else 12)
        for k in range(110):
            t = r.uniform(0, 2 * math.pi); s = r.uniform(.86, 1.14)
            x = CX + RX * s * math.cos(t); y = CY + RY * s * math.sin(t)
            tx_, ty_ = -RX * math.sin(t), RY * math.cos(t); L = math.hypot(tx_, ty_); tx_ /= L; ty_ /= L
            o += f'<line x1="{x:.0f}" y1="{y:.0f}" x2="{x - tx_ * 22:.0f}" y2="{y - ty_ * 22:.0f}" stroke="#d8fff4" stroke-width="3" stroke-linecap="round" opacity="{r.uniform(.3, .9):.2f}"/>'
        # ghost wisps trailing off the outer edge
        for k in range(14):
            t = r.uniform(0, 2 * math.pi)
            x = CX + RX * 1.05 * math.cos(t); y = CY + RY * 1.05 * math.sin(t)
            o += f'<path d="M{x:.0f} {y:.0f} q{30 * math.cos(t):.0f} {-40:.0f} {70 * math.cos(t):.0f} {-30:.0f} q{30 * math.cos(t):.0f} {10:.0f} {50 * math.cos(t):.0f} {-40:.0f}" fill="none" stroke="#bfffee" stroke-width="5" stroke-linecap="round" opacity=".25" filter="url(#b4)"/>'
        return o + '</g>'

    # dipole field lines (the "cage")
    fl = ''
    for k in (1.6, 2.2, 2.9):
        for sgn in (-1, 1):
            pts = []
            for i in range(61):
                th = math.radians(18 + i * (144 / 60))
                r_ = ER * k * math.sin(th) ** 2
                pts.append((CX + sgn * r_ * math.sin(th), CY - r_ * math.cos(th)))
            fl += '<path d="M' + ' L'.join(f'{x:.0f} {y:.0f}' for x, y in pts) + f'" fill="none" stroke="#9fc8ff" stroke-width="3" stroke-dasharray="3 12" stroke-linecap="round" opacity=".35" transform="rotate({ROT} {CX} {CY})"/>'
    b += fl
    b += belt('back5')
    # Earth
    b += f'<circle cx="{CX}" cy="{CY}" r="{ER + 40}" fill="url(#atm5)"/>'
    b += f'<circle cx="{CX}" cy="{CY}" r="{ER}" fill="url(#earth5)"/>'
    e = f'<g clip-path="url(#ec5)">'
    e += (f'<path d="M{CX - 200} {CY - 120} q60 -60 140 -40 q40 30 20 80 q-60 40 -100 10 q-50 10 -60 -50z '
          f'M{CX + 40} {CY + 20} q80 -30 130 20 q20 60 -30 90 q-70 10 -100 -40z M{CX - 120} {CY + 110} q40 -20 70 10 q0 40 -40 50 q-40 -20 -30 -60z" fill="#4f9a5a" opacity=".85"/>')
    r2 = random.Random(3)
    for _ in range(30):
        x = r2.randint(CX - ER, CX + ER); y = r2.randint(CY - ER, CY + ER); rx = r2.randint(30, 110)
        e += f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{rx * .2:.0f}" fill="#f2f8ff" opacity="{r2.uniform(.2, .5):.2f}" filter="url(#b4)"/>'
    e += f'<circle cx="{CX}" cy="{CY}" r="{ER}" fill="url(#night5)"/>'
    e += f'<path d="M{CX - ER + 30} {CY - 60} A{ER} {ER} 0 0 1 {CX - 60} {CY - ER + 30}" fill="none" stroke="#fff" stroke-width="10" opacity=".4" filter="url(#b4)"/>'
    e += '</g>'
    b += e
    b += f'<circle cx="{CX}" cy="{CY}" r="{ER}" fill="none" stroke="#bfe6ff" stroke-width="4" opacity=".7"/>'
    b += belt('front5')

    # tiny satellites inside the belt, sparking / dying
    def sat(x, y, rot, s, dead=False):
        o = f'<g transform="translate({x} {y}) rotate({rot}) scale({s})">'
        o += '<rect x="-62" y="-12" width="44" height="24" fill="#2a4a8a" stroke="#0b0f1c" stroke-width="3"/><rect x="18" y="-12" width="44" height="24" fill="#2a4a8a" stroke="#0b0f1c" stroke-width="3"/>'
        o += '<line x1="-18" y1="0" x2="18" y2="0" stroke="#999" stroke-width="4"/><rect x="-16" y="-18" width="32" height="36" rx="4" fill="#d9b860" stroke="#0b0f1c" stroke-width="3"/>'
        o += '<path d="M0 -18 l0 -14 m0 0 q-10 -4 -16 2" fill="none" stroke="#ccc" stroke-width="3"/>'
        for k in range(4):
            a = math.radians(-120 + k * 70); r0 = 26
            o += (f'<path d="M{r0 * math.cos(a):.0f} {r0 * math.sin(a):.0f} l{14 * math.cos(a) + 6:.0f} {14 * math.sin(a):.0f} l-8 5 l{16 * math.cos(a) + 4:.0f} {16 * math.sin(a):.0f}" '
                  f'fill="none" stroke="#ffe46a" stroke-width="4" stroke-linejoin="round"/>')
        if dead:
            o += '<path d="M-6 -6 l12 12 M6 -6 l-12 12" stroke="#1a1a1a" stroke-width="3"/>'
        return o + '</g>' + f'<circle cx="{x}" cy="{y}" r="{40 * s:.0f}" fill="#ffe46a" opacity=".18" filter="url(#b12)"/>'
    a = math.radians(ROT)
    for t, s, dead in ((200, 1.0, False), (330, .8, True), (20, .9, False), (130, .7, True)):
        tt = math.radians(t); lx, ly = RX * math.cos(tt), RY * math.sin(tt)
        x = CX + lx * math.cos(a) - ly * math.sin(a); y = CY + lx * math.sin(a) + ly * math.cos(a)
        b += sat(round(x), round(y), random.randint(-30, 30), s, dead)
    # a dead satellite drifting away trailing smoke
    for k in range(9):
        b += f'<circle cx="{1640 - k * 26}" cy="{250 - k * 14}" r="{8 + k * 2}" fill="#7a8090" opacity="{.35 - k * .035:.2f}"/>'
    b += sat(1660, 262, 40, .9, True)
    # ---- frog in helmet floating lower left, holding a fried little satellite, startled ----
    held = ('<g transform="translate(78 -10) rotate(-20) scale(.55)">'
            '<rect x="-62" y="-12" width="44" height="24" fill="#2a4a8a" stroke-width="4"/><rect x="18" y="-12" width="44" height="24" fill="#2a4a8a" stroke-width="4"/>'
            '<rect x="-16" y="-18" width="32" height="36" rx="4" fill="#d9b860" stroke-width="4"/>'
            '<path d="M-10 -26 q6 -14 0 -26 q10 10 4 26" fill="#6a6f7a" stroke="none" opacity=".7"/></g>')
    tether = '<path d="M360 860 Q520 960 700 820 T 940 720" fill="none" stroke="#e8e2d0" stroke-width="5" opacity=".55"/>'
    b += tether
    b += frog(330, 990, 3.0, look=(6, -3), mouth='wow', helmet=True, rot=-10,
              armL='M-34 -22 q-24 -6 -28 -34', armR='M38 -22 q22 4 34 2', feet=((-26, 8, -24), (26, 6, 26)), front=held)
    for x, y, s in ((960, 130, 18), (1820, 120, 20), (1780, 760, 12), (900, 520, 12)):
        b += spark(x, y, s)
    return page('#02040a', svg(d, b), [('A <span class="g">GHOST</span>', 190, 'w'), ('AROUND', 170, 'w'), ('EARTH', 200, 'w')], top=40)


for n, fn in ((1, make_1), (2, make_2), (3, make_3), (4, make_4), (5, make_5)):
    open(os.path.join(VID, f'space-nuke-short{n}', 'thumb', 'A.html'), 'w').write(fn())
print('ok')
