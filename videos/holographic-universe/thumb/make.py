# Thumbnails A-C for holographic-universe (guideline 16-6 / 16-8, brief tools/briefs/thumb_art.md). Run: python3 videos/holographic-universe/thumb/make.py
# A  IS DEPTH AN ILLUSION?  homage: The Matrix (1999) "red pill or blue pill" offer in falling green code: the frog in a long black coat holds out
#                           a red and a blue pill while the code rain assembles into a glowing 3D globe. Script S01-S03 ("what if all of this depth
#                           is actually a vast cosmic illusion?") and the closing "stream of digital code creates a rich world on your flat screen".
# B  2D = 3D?               intuitive: a flat credit card whose hologram security sticker projects a glowing 3D Earth into the air; the frog stands
#                           on the card with a magnifying glass. Script: credit-card security sticker, "a flat thing has produced ... a 3D thing".
# C  SURFACE, NOT VOLUME    intuitive: a black hole whose event-horizon sphere is tiled with glowing bits, a falling book shedding bits onto it;
#                           the astronaut frog measures the surface with a tape. Script: "information scales strictly with surface area. Not volume."
import os, sys, math, random
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', '..', 'tools'))
from thumb_lib import page, svg, lin, rad, spark
from hands import hand

INK = '#1d2b1c'; GREEN = '#6aa55a'; DARKG = '#4d8a4a'; BELLY = '#9cc98a'
FILTERS = ''.join(f'<filter id="b{n}" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="{n}"/></filter>' for n in (2, 3, 6, 12, 24, 50))
MONO = "font-family=\"'DejaVu Sans Mono',monospace\" font-weight=\"bold\""
GLYPHS = '0123456789ABCDEFXZ<>=+*:#$%'


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
        g.append('<ellipse cx="0" cy="8" rx="50" ry="8" fill="#000" opacity=".25" stroke="none"/>')
    if helmet:
        g.append('<rect x="-50" y="-58" width="20" height="42" rx="7" fill="#c9a24e" stroke-width="3"/><rect x="-46" y="-52" width="5" height="30" rx="2" fill="#fff" stroke="none" opacity=".6"/>')
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
    if brows:
        g.append('<path d="M-22 -88 q12 -9 24 -1 M10 -89 q12 -8 24 1" fill="none" stroke-width="3.4"/>')
    if mouth == 'O':
        g.append('<ellipse cx="6" cy="-38" rx="10" ry="12" fill="#7a2f33" stroke-width="3"/><ellipse cx="6" cy="-31" rx="6" ry="4" fill="#e07b7b" stroke="none"/>')
    else:
        g.append('<ellipse cx="6" cy="-41" rx="6" ry="7.5" fill="#7a2f33" stroke-width="3"/>')
    g.append('<ellipse cx="-18" cy="-48" rx="5" ry="3" fill="#e98a8a" stroke="none" opacity=".55"/><ellipse cx="30" cy="-48" rx="5" ry="3" fill="#e98a8a" stroke="none" opacity=".55"/>')
    if helmet:   # brass diving helmet with glass bubble
        g.append('<circle cx="6" cy="-58" r="45" fill="#bfe6ff" fill-opacity=".14" stroke="#f0d78a" stroke-width="5"/>')
        g.append('<path d="M-26 -82 q12 -18 32 -21" fill="none" stroke="#fff" stroke-width="5" opacity=".8"/><path d="M42 -40 q6 -10 6 -22" fill="none" stroke="#fff" stroke-width="3" opacity=".5"/>')
        g.append('<ellipse cx="6" cy="-16" rx="40" ry="9" fill="#c9a24e" stroke-width="3.2"/><path d="M-30 -18 q36 8 72 0" fill="none" stroke="#fff3c4" stroke-width="2.2" opacity=".8"/>')
        for bx in (-26, 6, 38):
            g.append(f'<circle cx="{bx}" cy="-16" r="3" fill="#f6e6b0" stroke-width="1.5"/>')
    if hat:      # straw hat blown off the head
        g.append('<g transform="translate(46 -112) rotate(28)"><ellipse cx="0" cy="8" rx="40" ry="9" fill="#e7c77c" stroke-width="3.2"/>'
                 '<path d="M-24 8 L-22 -14 Q0 -20 22 -14 L24 8 Z" fill="#efd590" stroke-width="3.2"/><path d="M-23 -2 L23 -2 L23.5 5 L-23.5 5Z" fill="#a8402e" stroke-width="2"/>'
                 '<path d="M-30 6 q30 6 60 0" fill="none" stroke="#fff6d0" stroke-width="2" opacity=".7"/></g>')
    g.append(mid)
    for a in (armL or 'M-34 -22 q-14 6 -16 22', armR or 'M38 -22 q14 6 16 22'):
        g.append(limb(a)); ex_, ey_ = end_of(a)
        g.append(f'<circle cx="{ex_:.1f}" cy="{ey_:.1f}" r="5.6" fill="{GREEN}" stroke-width="3"/>')
    g.append(front); g.append('</g>')
    return ''.join(g)



# ---------------- sphere projection ----------------
def sph(lat, lon, R, cx, cy, tilt=0.0, rot=0.0):
    """lat/lon in radians -> (x, y, z); z > 0 faces the viewer. tilt rotates about the x axis (shows the north pole)."""
    x0 = math.cos(lat) * math.sin(lon + rot); y0 = -math.sin(lat); z0 = math.cos(lat) * math.cos(lon + rot)
    y = y0 * math.cos(tilt) - z0 * math.sin(tilt); z = y0 * math.sin(tilt) + z0 * math.cos(tilt)
    return cx + R * x0, cy + R * y, z


def poly(pts):
    return 'M' + ' L'.join(f'{x:.1f},{y:.1f}' for x, y in pts) + 'Z'


# =============================== A_v1 (kept, superseded 2026-11-04): The Matrix homage in code rain ===============================
def make_A_v1():
    rnd = random.Random(7)
    d = FILTERS
    d += rad('haloA', 1370, 420, 520, [(0, '#d8ffe0', .55), (.35, '#3dff8a', .28), (1, '#00ff66', 0)])
    d += rad('coreA', 1300, 330, 360, [(0, '#0f4a26', 1), (.7, '#03150a', 1), (1, '#010804', 1)])
    d += lin('floorA', [(0, '#03140a'), (1, '#000302')])
    d += lin('fadeL', [(0, '#010603'), (.5, '#010603'), (1, '#010603')], x2=1, y2=0)
    d += rad('vigA', 1300, 480, 1250, [(0, '#000', 0), (.6, '#000', 0), (1, '#000', .75)])
    d += '<radialGradient id="pillR" cx=".35" cy=".3" r=".8"><stop offset="0" stop-color="#ffd0c8"/><stop offset=".35" stop-color="#ff3a2e"/><stop offset="1" stop-color="#7a0a08"/></radialGradient>'
    d += '<radialGradient id="pillB" cx=".35" cy=".3" r=".8"><stop offset="0" stop-color="#d8ecff"/><stop offset=".35" stop-color="#2f86ff"/><stop offset="1" stop-color="#08245e"/></radialGradient>'
    b = '<rect width="1920" height="1080" fill="#010804"/>'
    # floor plane with perspective grid (horizon y=800)
    HY = 800
    b += f'<rect y="{HY}" width="1920" height="{1080 - HY}" fill="url(#floorA)"/>'
    for i in range(-14, 30):
        x0 = 1300 + i * 60; x1 = 1300 + i * 400
        b += f'<line x1="{x0}" y1="{HY}" x2="{x1}" y2="1080" stroke="#1fff70" stroke-width="2" opacity=".16"/>'
    yy = HY; k = 8
    while yy < 1080:
        b += f'<line x1="0" y1="{yy:.0f}" x2="1920" y2="{yy:.0f}" stroke="#1fff70" stroke-width="2" opacity="{.08 + (yy - HY) / 1600:.2f}"/>'
        k *= 1.35; yy += k
    b += f'<rect y="{HY - 3}" width="1920" height="6" fill="#5dff9a" opacity=".35" filter="url(#b6)"/>'
    # code rain: three depth layers
    def column(x, size, op, blur, ylo, yhi, n):
        o = ''
        y_end = rnd.uniform(ylo, yhi)
        for j in range(n):
            y = y_end - j * size * 1.05
            if y < -20:
                break
            ch = rnd.choice(GLYPHS)
            if j == 0:
                o += f'<text x="{x}" y="{y:.0f}" font-size="{size}" fill="#effff2" opacity="{min(1, op * 1.6):.2f}" {MONO}>{ch}</text>'
            else:
                a = op * (1 - j / n) ** .8
                col = '#5dff8e' if j < 4 else '#18c450'
                o += f'<text x="{x}" y="{y:.0f}" font-size="{size}" fill="{col}" opacity="{a:.2f}" {MONO}>{ch}</text>'
        return f'<g filter="url(#b{blur})">{o}</g>' if blur else o
    far = ''.join(column(x, 18, .38, 0, 200, 1000, rnd.randint(10, 30)) for x in range(6, 1920, 22) if rnd.random() < .75)
    b += f'<g opacity=".7">{far}</g>'
    mid = ''.join(column(x, 28, .7, 0, 150, 950, rnd.randint(8, 22)) for x in range(10, 1920, 40) if rnd.random() < .6)
    b += mid
    # dark veil behind the title so the letters stay readable
    b += '<path d="M0 0 H1020 Q980 380 760 560 Q500 680 0 640Z" fill="#010603" opacity=".62" filter="url(#b50)"/>'
    b += '<rect x="1560" y="860" width="360" height="220" fill="#000" opacity=".55" filter="url(#b50)"/>'
    # ---- focal: a globe assembled from glowing code ----
    CX, CY, R = 1370, 420, 300
    b += f'<circle cx="{CX}" cy="{CY}" r="{R * 1.75:.0f}" fill="url(#haloA)"/>'
    b += f'<circle cx="{CX}" cy="{CY}" r="{R}" fill="url(#coreA)"/>'
    # streams of code falling into the globe from the top
    for x in range(CX - 240, CX + 260, 34):
        top = rnd.uniform(-40, 60)
        dy = math.sqrt(max(0, R * R - (x - CX) ** 2))
        y = top
        while y < CY - dy + 10:
            fade = (y - top) / max(1, CY - dy - top)
            b += f'<text x="{x}" y="{y:.0f}" font-size="26" fill="#9dffbe" opacity="{.15 + .75 * fade:.2f}" {MONO} text-anchor="middle">{rnd.choice(GLYPHS)}</text>'
            y += 29
    land = lambda la, lo: (math.sin(lo * 2.1 + 1.0) * math.cos(la * 2.8) + .6 * math.sin(lo * 3.7 - la * 2.2 + 2) + .35 * math.cos(lo * 6.1 + la * 5)) > .35
    back, front = '', ''
    nl = 26
    for i in range(nl):
        la = -math.pi / 2 + (i + .5) * math.pi / nl
        nlon = max(6, int(56 * math.cos(la)))
        for j in range(nlon):
            lo = j * 2 * math.pi / nlon
            x, y, z = sph(la, lo, R, CX, CY, tilt=.32, rot=.6)
            isl = land(la, lo)
            ch = rnd.choice(GLYPHS)
            if z < 0:
                if rnd.random() < .5:
                    back += f'<text x="{x:.0f}" y="{y + 7:.0f}" font-size="15" fill="#1aa848" opacity="{.18 + .2 * (1 + z):.2f}" {MONO} text-anchor="middle">{ch}</text>'
                continue
            # light from the upper left
            nx, ny = (x - CX) / R, (y - CY) / R
            lit = max(0, .55 + .5 * (-nx * .55 - ny * .6 + z * .6))
            sz = 14 + 14 * z
            if isl:
                col = '#effff2' if lit > .85 else ('#a8ffc4' if lit > .6 else '#4fe07e')
                op = .55 + .45 * min(1, lit)
            else:
                col = '#1c9a48' if lit > .6 else '#0f6a2e'
                op = .22 + .3 * min(1, lit)
            front += f'<text x="{x:.0f}" y="{y + sz * .35:.0f}" font-size="{sz:.0f}" fill="{col}" opacity="{op:.2f}" {MONO} text-anchor="middle">{ch}</text>'
    b += back
    b += f'<g filter="url(#b6)" opacity=".55">{front}</g>' + front
    # rim light + equator orbit ring
    b += f'<circle cx="{CX}" cy="{CY}" r="{R}" fill="none" stroke="#b8ffd0" stroke-width="5" opacity=".75"/>'
    b += f'<circle cx="{CX}" cy="{CY}" r="{R + 6}" fill="none" stroke="#5dff9a" stroke-width="22" opacity=".35" filter="url(#b12)"/>'
    b += f'<path d="M{CX - R * 1.35:.0f} {CY + 40} A{R * 1.35:.0f} {R * .3:.0f} -10 0 0 {CX + R * 1.35:.0f} {CY - 60}" fill="none" stroke="#c8ffd8" stroke-width="4" opacity=".7"/>'
    b += f'<path d="M{CX - R * 1.35:.0f} {CY + 40} A{R * 1.35:.0f} {R * .3:.0f} -10 0 0 {CX + R * 1.35:.0f} {CY - 60}" fill="none" stroke="#5dff9a" stroke-width="16" opacity=".35" filter="url(#b6)"/>'
    b += spark(CX - 190, CY - 200, 26, '#f4fff6') + spark(CX + 250, CY - 230, 18, '#f4fff6') + spark(CX + 330, CY + 150, 22, '#e8fff0')
    # glow of the globe on the floor
    b += f'<ellipse cx="{CX}" cy="{HY + 40}" rx="520" ry="60" fill="#5dff9a" opacity=".22" filter="url(#b24)"/>'
    # near layer: a few big blurred glyph columns in the foreground for depth
    near = ''.join(column(x, 54, .5, 3, 300, 1100, rnd.randint(4, 9)) for x in (1060, 1700))
    b += near
    # ---- the frog in a long black coat, offering a red and a blue pill ----
    fx, fy, fs = 860, 1035, 3.1
    coat_back = ('<path d="M-40 -24 Q-56 -4 -60 10 L64 10 Q60 -4 46 -24 Q4 -36 -40 -24Z" fill="#0b0f0d" stroke-width="3.6"/>')
    coat = ('<path d="M-36 -30 Q-46 -10 -50 8 L-8 8 L-2 -6 L8 -6 L14 8 L54 8 Q50 -10 40 -30 L22 -26 L6 -4 L-12 -26Z" fill="#121614" stroke-width="3.6"/>'
            '<path d="M-12 -26 L-2 -8 L-20 -16Z M22 -26 L10 -8 L30 -16Z" fill="#1f2622" stroke-width="2.6"/>'
            '<path d="M-44 -6 Q-40 -18 -32 -26" fill="none" stroke="#5dff9a" stroke-width="2.4" opacity=".7"/>'
            '<path d="M48 -6 Q46 -18 38 -26" fill="none" stroke="#5dff9a" stroke-width="2.4" opacity=".7"/>'
            # small round sunglasses pushed up on the forehead
            '<g transform="translate(0 -86)"><circle cx="-8" cy="0" r="7" fill="#050807" stroke-width="2.4"/><circle cx="18" cy="0" r="7" fill="#050807" stroke-width="2.4"/>'
            '<path d="M-1 0 h12 M-15 0 l-14 6 M25 0 l14 6" fill="none" stroke-width="2.4"/><path d="M-12 -3 l5 -2 M14 -3 l5 -2" stroke="#c8ffd8" stroke-width="2"/></g>')
    pills = ('<g transform="translate(-82 -34) rotate(-20)"><ellipse cx="0" cy="0" rx="26" ry="18" fill="#ff3a2e" opacity=".6" filter="url(#b6)" stroke="none"/>'
             '<rect x="-18" y="-9" width="36" height="18" rx="9" fill="url(#pillR)" stroke-width="2.6"/><path d="M-11 -4 h14" stroke="#fff" stroke-width="3" opacity=".8"/></g>'
             '<g transform="translate(94 -34) rotate(20)"><ellipse cx="0" cy="0" rx="26" ry="18" fill="#2f86ff" opacity=".6" filter="url(#b6)" stroke="none"/>'
             '<rect x="-18" y="-9" width="36" height="18" rx="9" fill="url(#pillB)" stroke-width="2.6"/><path d="M-11 -4 h14" stroke="#fff" stroke-width="3" opacity=".8"/></g>')
    b += f'<ellipse cx="{fx + 20}" cy="{fy + 12}" rx="200" ry="22" fill="#000" opacity=".6" filter="url(#b6)"/>'
    b += f'<ellipse cx="{fx + 20}" cy="{fy - 120}" rx="230" ry="190" fill="#5dff9a" opacity=".12" filter="url(#b50)"/>'
    b += frog(fx, fy, fs, look=(5, -5), mouth='O', back=coat_back, mid=coat,
              armL='M-34 -22 q-26 -6 -48 -14', armR='M38 -22 q26 -6 48 -14', front=pills)
    # green rim light on the frog's right side (from the globe)
    b += '<rect width="1920" height="1080" fill="url(#vigA)"/>'
    lines = [('IS DEPTH', 140, 'w'), ('AN', 108, 'w'), ('ILLUSION?', 178, 'y')]
    return page('#010804', svg(d, b), lines, outline='#000000', top=44)


# =============================== A (v2, 2026-11-04, miya's reference D): the street dissolving into a hologram ===============================
# A  THE WORLD MIGHT BE PROJECTED  homage: The Matrix (1999) red pill / blue pill, offered in two open hands, while the city street behind
#                           breaks up into wireframe and pixel bits toward a bright projector-like vanishing point; the frog sits on the
#                           right thumb between the pills. Script S01 ("Could our entire three-dimensional reality be nothing more than a
#                           projection?"), movie-projector analogy, closing "physics might project our universe".
def _mix(c1, c2, t):
    a = [int(c1[i:i + 2], 16) for i in (1, 3, 5)]; b = [int(c2[i:i + 2], 16) for i in (1, 3, 5)]
    return '#' + ''.join(f'{round(x + (y - x) * t):02x}' for x, y in zip(a, b))


def _pill(x, y, rot, L, W, grad, glow, dark):
    h = W / 2; e = L / 2
    half = f'M0 {-h} H{e - h} A{h} {h} 0 0 1 {e - h} {h} H0Z'
    return (f'<g transform="translate({x:.0f} {y:.0f}) rotate({rot})">'
            f'<ellipse cx="0" cy="0" rx="{e * 1.2:.0f}" ry="{W * .95:.0f}" fill="{glow}" opacity=".4" filter="url(#b24)"/>'
            f'<ellipse cx="10" cy="{h * .9:.0f}" rx="{e * .95:.0f}" ry="{h * .55:.0f}" fill="{dark}" opacity=".45" filter="url(#b6)"/>'
            f'<rect x="{-e}" y="{-h}" width="{L}" height="{W}" rx="{h}" fill="url(#{grad})" stroke="#170a10" stroke-width="6"/>'
            f'<path d="{half}" fill="#000" opacity=".16"/>'
            f'<path d="M0 {-h + 3} V{h - 3}" stroke="#170a10" stroke-width="3.5" opacity=".55"/>'
            f'<path d="M{-e + h * .8:.0f} {-h * .45:.0f} H{e * .55:.0f}" stroke="#fff" stroke-width="{W * .13:.1f}" stroke-linecap="round" opacity=".8"/>'
            f'<path d="M{-e + h * .6:.0f} {h * .35:.0f} q{e * .3:.0f} {h * .3:.0f} {e * .9:.0f} {h * .2:.0f}" fill="none" stroke="#fff" stroke-width="3" opacity=".3"/>'
            '</g>')


def make_A_v2():
    return make_A('frog')


def make_A(variant='car'):   # v3 (2026-11-04, miya): car with the frog driver; 'frog' = v2 (frog on the thumb)
    rnd = random.Random(11)
    VX, VY, F, H = 1010, 690, 900, 1.7

    def pj(X, Y, Z):
        return VX + F * X / Z, VY + F * (H - Y) / Z

    def quad(pts, **kw):
        a = ' '.join(f'{k.replace("_", "-")}="{v}"' for k, v in kw.items())
        return f'<path d="M{P(pts)}Z" {a}/>'

    d = FILTERS
    d += lin('skyA2', [(0, '#080c2c'), (.4, '#1e1a56'), (.78, '#57347a'), (1, '#b2607f')])
    d += rad('vpA2', VX, VY - 10, 760, [(0, '#ffffff', 1), (.05, '#f0fdff', .95), (.15, '#9fecff', .5), (.4, '#6c86ff', .16), (1, '#3a2a7a', 0)])
    d += lin('roadA2', [(0, '#221a34'), (.25, '#16111f'), (1, '#07050b')])
    d += rad('vigA2', 960, 520, 1250, [(0, '#000', 0), (.62, '#000', 0), (1, '#000', .62)])
    d += (f'<linearGradient id="gridA2" gradientUnits="userSpaceOnUse" x1="0" y1="{VY}" x2="0" y2="1080">'
          '<stop offset="0" stop-color="#9ff0ff" stop-opacity=".75"/><stop offset=".45" stop-color="#7fe0ff" stop-opacity=".22"/>'
          '<stop offset="1" stop-color="#7fe0ff" stop-opacity=".06"/></linearGradient>')
    d += '<radialGradient id="pR2" cx=".35" cy=".28" r=".85"><stop offset="0" stop-color="#ffd6cc"/><stop offset=".3" stop-color="#ff3b2f"/><stop offset="1" stop-color="#7a0907"/></radialGradient>'
    d += '<radialGradient id="pB2" cx=".35" cy=".28" r=".85"><stop offset="0" stop-color="#dcefff"/><stop offset=".3" stop-color="#2f84ff"/><stop offset="1" stop-color="#071f5a"/></radialGradient>'
    d += lin('sleeveA2', [(0, '#1b1726'), (1, '#07060b')])
    b = f'<rect width="1920" height="{VY + 2}" fill="url(#skyA2)"/>'
    # stars + sky "projection dome" grid centred on the vanishing point
    for _ in range(150):
        x, y = rnd.uniform(0, 1920), rnd.uniform(0, VY - 40)
        b += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{rnd.choice([1.2, 1.7, 2.4])}" fill="#e8f2ff" opacity="{rnd.uniform(.15, .7):.2f}"/>'
    dome = ''
    for k, r in enumerate((330, 560, 850, 1220, 1700)):
        dome += f'<path d="M{VX - r} {VY} A{r} {r * .62:.0f} 0 0 1 {VX + r} {VY}" fill="none" stroke="#8fe8ff" stroke-width="{2 + k * .4:.1f}" opacity="{.2 - k * .025:.2f}"{" stroke-dasharray=&quot;14 10&quot;" if k % 2 else ""}/>'
    for a in range(-84, 85, 12):
        t = math.radians(a)
        dome += f'<line x1="{VX}" y1="{VY}" x2="{VX + 2000 * math.sin(t):.0f}" y2="{VY - 1240 * math.cos(t):.0f}" stroke="#8fe8ff" stroke-width="1.6" opacity=".09"/>'
    b += dome.replace('&quot;', '"')
    # projector rays fanning out of the vanishing point
    for a in range(-80, 81, 9):
        t1, t2 = math.radians(a - 1.6), math.radians(a + 1.6)
        b += (f'<path d="M{VX} {VY} L{VX + 2200 * math.sin(t1):.0f} {VY - 1400 * math.cos(t1):.0f} L{VX + 2200 * math.sin(t2):.0f} {VY - 1400 * math.cos(t2):.0f}Z" '
              f'fill="#d8f6ff" opacity="{rnd.uniform(.025, .06):.3f}"/>')
    b += f'<circle cx="{VX}" cy="{VY - 10}" r="760" fill="url(#vpA2)"/>'
    # ground: road, sidewalks, grid that gets brighter (more "digital") toward the vanishing point
    b += f'<rect y="{VY}" width="1920" height="{1080 - VY}" fill="url(#roadA2)"/>'
    b += quad([(VX, VY), pj(6, 0, .9), pj(9, 0, .9)], fill='#3a2534')
    b += quad([(VX, VY), pj(-6, 0, .9), pj(-9, 0, .9)], fill='#241a30')
    b += f'<path d="M{VX} {VY} L{P([pj(6, 0, .9)])}" stroke="#ff9a6a" stroke-width="5" opacity=".55"/>'
    b += f'<path d="M{VX} {VY} L{P([pj(-6, 0, .9)])}" stroke="#c78aff" stroke-width="4" opacity=".35"/>'
    for X in (-9, -6, -4, -2, 0, 2, 4, 6, 8):
        b += f'<line x1="{VX}" y1="{VY}" x2="{pj(X, 0, .9)[0]:.0f}" y2="{pj(X, 0, .9)[1]:.0f}" stroke="url(#gridA2)" stroke-width="2.4"/>'
    Z = 3.6
    while Z < 160:
        (x0, y), (x1, _) = pj(-9, 0, Z), pj(8, 0, Z)
        op = .1 + .5 * (1 - min(1, (y - VY) / 390)) ** 2
        b += f'<line x1="{x0:.0f}" y1="{y:.1f}" x2="{x1:.0f}" y2="{y:.1f}" stroke="#9ff0ff" stroke-width="{max(1, 5 / Z * 4):.1f}" opacity="{op:.2f}"/>'
        Z *= 1.16
    Z = 2.2
    while Z < 90:   # centre dashes
        b += quad([pj(-.13, 0, Z), pj(.13, 0, Z), pj(.13, 0, Z + 1.4), pj(-.13, 0, Z + 1.4)], fill='#f2d27a', opacity=f'{.85 - Z / 120:.2f}')
        Z += 3.2
    b += f'<ellipse cx="{VX}" cy="{VY}" rx="430" ry="26" fill="#e8fbff" opacity=".55" filter="url(#b12)"/>'

    # ---------------- buildings: solid near the camera, breaking into wireframe + pixel bits farther away/higher up ----------------
    bits = []

    def building(side, X0, X1, Z1, Z2, T, wall, fl=3.2, colw=2.4, dim=False, bias=0.0):
        o = ''
        fog = '#6d6aa8' if not dim else '#2a2242'
        def cellq(y0, y1, z0, z1):
            return [pj(X0, y0, z0), pj(X0, y1, z0), pj(X0, y1, z1), pj(X0, y0, z1)]
        def wire(pts, Zm, op=.85):
            w = max(1.0, 34 / Zm)
            return quad(pts, fill='#7fe6ff', fill_opacity='.07', stroke='#a6f3ff', stroke_width=f'{w:.1f}', stroke_opacity=f'{op:.2f}')
        # front face (towards the camera)
        tF = min(1, Z1 / 85)
        fr = [pj(X0, 0, Z1), pj(X1, 0, Z1), pj(X1, T, Z1), pj(X0, T, Z1)]
        s_front = .9 * (Z1 / 50) + bias
        if s_front < 1.0:
            o += quad(fr, fill=_mix(_mix(wall, '#000000', .35), fog, tF * .6))
            nfx = max(1, int(T / fl)); ncx = max(1, int(abs(X1 - X0) / colw))
            for i in range(nfx):
                for j in range(ncx):
                    if rnd.random() < (.45 if dim else .3):
                        xa, xb = X0 + (X1 - X0) * (j + .25) / ncx, X0 + (X1 - X0) * (j + .75) / ncx
                        ya, yb = T * (i + .28) / nfx, T * (i + .76) / nfx
                        o += quad([pj(xa, ya, Z1), pj(xb, ya, Z1), pj(xb, yb, Z1), pj(xa, yb, Z1)], fill='#8a6a5a' if dim else '#c89a5a', opacity='.22' if dim else '.5')
        nf = max(1, int(T / fl)); nc = max(1, int((Z2 - Z1) / colw))
        for i in range(nf):
            y0, y1 = i * T / nf, (i + 1) * T / nf
            for j in range(nc):
                z0, z1 = Z1 + j * (Z2 - Z1) / nc, Z1 + (j + 1) * (Z2 - Z1) / nc
                Zm = (z0 + z1) / 2; Ym = (y0 + y1) / 2
                s = .75 * (Zm / 50) + Ym / 14 + rnd.uniform(-.14, .14) + bias
                col = _mix(wall, fog, min(1, Zm / 85) * .7)
                if s < .8:
                    o += quad(cellq(y0, y1, z0, z1), fill=col, stroke=col, stroke_width='1')
                    lit = rnd.random() < (.35 if dim else .68)
                    wc = _mix('#f2c46e' if lit else '#2a1a2c', fog, min(1, Zm / 85) * .45)
                    if dim and lit: wc = '#b9906a'
                    o += quad(cellq(y0 + (y1 - y0) * .25, y1 - (y1 - y0) * .22, z0 + (z1 - z0) * .2, z1 - (z1 - z0) * .2), fill=wc)
                    if not dim:
                        o += quad(cellq(y0, y1, z0, z1), fill='none', stroke='#a6f3ff', stroke_width=f'{max(.8, 18 / Zm):.1f}', stroke_opacity='.12')
                elif s < 1.08:   # breaking up: 3x3 sub-blocks, some gone (they fly off as pixels)
                    for a in range(3):
                        for c in range(3):
                            ya, yb = y0 + a * (y1 - y0) / 3, y0 + (a + 1) * (y1 - y0) / 3
                            za, zb = z0 + c * (z1 - z0) / 3, z0 + (c + 1) * (z1 - z0) / 3
                            q = cellq(ya, yb, za, zb)
                            if rnd.random() < .42 - (s - .8) * .8 + (.25 if a == 0 else 0):
                                o += quad(q, fill=_mix(col, '#a6f3ff', .12), stroke=col, stroke_width='1')
                            else:
                                o += wire(q, Zm, .35 if dim else .6)
                                cx = sum(p[0] for p in q) / 4; cy = sum(p[1] for p in q) / 4
                                sz = abs(q[2][0] - q[1][0]) * rnd.uniform(.6, 1.1) + abs(q[0][1] - q[1][1]) * .3
                                if rnd.random() < .7:
                                    bits.append((cx + rnd.uniform(-70, 30) * side, cy - rnd.uniform(25, 190), max(4, min(30, sz)), dim))
                else:
                    o += wire(cellq(y0, y1, z0, z1), Zm, .4 if dim else .8)
        # box edges (hologram outline)
        eop = .3 if s_front < .8 else .8
        if dim: eop *= .5
        for p1, p2 in (((X0, 0, Z1), (X0, T, Z1)), ((X0, T, Z1), (X0, T, Z2)), ((X0, 0, Z2), (X0, T, Z2)), ((X0, T, Z1), (X1, T, Z1)),
                       ((X1, 0, Z1), (X1, T, Z1)), ((X0, T, Z2), (X1, T, Z2)), ((X1, T, Z1), (X1, T, Z2))):
            (a1, b1), (a2, b2) = pj(*p1), pj(*p2)
            Zm = (p1[2] + p2[2]) / 2
            o += f'<line x1="{a1:.0f}" y1="{b1:.0f}" x2="{a2:.0f}" y2="{b2:.0f}" stroke="#c4f8ff" stroke-width="{max(1.2, 40 / Zm):.1f}" opacity="{eop:.2f}"/>'
        return o

    # left: low dark buildings (keep the text area calm)
    left = ''
    for Z1, Z2, T, wall in ((20, 27, 6.8, '#2a2140'), (27.6, 36, 8.5, '#30233f'), (36.6, 50, 7.5, '#2a2140'), (50.6, 66, 10, '#33274a'), (66.6, 90, 9, '#2a2140'), (90.6, 130, 12, '#33274a')):
        left = building(-1, -9, -24, Z1, Z2, T, wall, fl=2.6, colw=2.2, dim=True, bias=-.05) + left
    b += left
    right = ''
    for Z1, Z2, T, wall in ((5, 11, 28, '#6e3b38'), (11.6, 19, 21, '#5b3a52'), (19.6, 27, 25, '#73443a'), (27.6, 38, 17, '#4f3b63'),
                            (38.6, 52, 23, '#6e3b38'), (52.6, 70, 15, '#5b3a52'), (70.6, 96, 19, '#4f3b63'), (96.6, 140, 14, '#5b3a52')):
        right = building(1, 8, 22, Z1, Z2, T, wall) + right
    b += right
    # flying pixel bits (from the dissolving buildings, drifting into the sky)
    pal = ['#9ff0ff', '#d8fbff', '#f2d27a', '#ff9ad0', '#7fb8ff']
    for x, y, s, dim in bits:
        if dim and x < 1000 and y < 500:
            continue
        c = rnd.choice(pal)
        b += f'<rect x="{x - s / 2:.0f}" y="{y - s / 2:.0f}" width="{s:.0f}" height="{s:.0f}" fill="{c}" opacity="{rnd.uniform(.35, .85) * (.5 if dim else 1):.2f}"/>'
    for _ in range(90):   # loose bits in the sky over the right half
        x = rnd.uniform(1020, 1900); y = rnd.uniform(20, 640); s = rnd.choice([6, 8, 10, 14, 18])
        b += f'<rect x="{x:.0f}" y="{y:.0f}" width="{s}" height="{s}" fill="{rnd.choice(pal)}" opacity="{rnd.uniform(.2, .7):.2f}"/>'
    # street lamps (left)
    for Z in (26, 40, 62, 95):
        (x0, y0), (x1, y1) = pj(-8.3, 0, Z), pj(-8.3, 6.6, Z)
        hx, hy = pj(-7.0, 6.5, Z)
        w = max(2, .2 * F / Z)
        b += f'<line x1="{x0:.0f}" y1="{y0:.0f}" x2="{x1:.0f}" y2="{y1:.0f}" stroke="#0c0814" stroke-width="{w:.1f}"/>'
        b += f'<line x1="{x1:.0f}" y1="{y1:.0f}" x2="{hx:.0f}" y2="{hy:.0f}" stroke="#0c0814" stroke-width="{w * .7:.1f}" stroke-linecap="round"/>'
        b += f'<circle cx="{hx:.0f}" cy="{hy:.0f}" r="{w * 9:.0f}" fill="#ffc98a" opacity=".22" filter="url(#b24)"/>'
        b += f'<circle cx="{hx:.0f}" cy="{hy + w * .6:.0f}" r="{w * 1.3:.1f}" fill="#fff0c8"/>'
    # warm light spill on the right sidewalk
    b += f'<path d="M{VX + 60} {VY + 8} L1920 {VY + 330} L1920 {VY + 420}Z" fill="#ff9a6a" opacity=".16" filter="url(#b24)"/>'

    # dark veil behind the title
    b += '<path d="M0 0 H1060 Q1040 360 860 520 Q560 640 0 600Z" fill="#06051a" opacity=".55" filter="url(#b50)"/>'

    # ---------------- (v3) a retro car coming down the street head-on, the frog at the wheel in sunglasses ----------------
    if variant == 'car':
        r2 = random.Random(5)
        CXc, CYc, u = 1140, 1035, 1.22
        BODY, SH, OL = '#efe4cc', '#c9b896', '#1a1424'
        L = lambda x, y: (CXc + x * u, CYc + y * u)
        # headlight beams spilling toward the viewer + glow on the road
        for sx in (-1, 1):
            hx, hy = L(140 * sx, -112)
            b += f'<path d="M{hx - 26:.0f} {hy:.0f} L{hx + 26:.0f} {hy:.0f} L{hx + sx * 330 + 150:.0f} 1080 L{hx + sx * 330 - 150:.0f} 1080Z" fill="#fff6d8" opacity=".13" filter="url(#b12)"/>'
        b += f'<ellipse cx="{CXc}" cy="{CYc + 10}" rx="{260 * u:.0f}" ry="{26 * u:.0f}" fill="#000" opacity=".55" filter="url(#b12)"/>'
        b += f'<ellipse cx="{CXc}" cy="{CYc - 160 * u:.0f}" rx="{300 * u:.0f}" ry="{220 * u:.0f}" fill="#bff4ff" opacity=".1" filter="url(#b50)"/>'
        d += ('<linearGradient id="glassA3" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2c3a66"/><stop offset=".6" stop-color="#18203e"/><stop offset="1" stop-color="#0e1328"/></linearGradient>'
              '<linearGradient id="bodyA3" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fbf3df"/><stop offset=".55" stop-color="#efe4cc"/><stop offset="1" stop-color="#b8a582"/></linearGradient>'
              '<clipPath id="wsA3"><path d="M-160 -184 L-126 -300 Q-122 -309 -108 -309 L108 -309 Q122 -309 126 -300 L160 -184Z"/></clipPath>')
        c = [f'<g transform="translate({CXc} {CYc}) scale({u})" stroke="{OL}" stroke-linejoin="round" stroke-linecap="round">']
        for sx in (-1, 1):   # tyres
            c.append(f'<rect x="{min(sx * 128, sx * 186)}" y="-64" width="58" height="66" rx="14" fill="#100d16" stroke-width="5"/>')
        c.append('<ellipse cx="-206" cy="-188" rx="20" ry="13" fill="url(#bodyA3)" stroke-width="4.5"/><ellipse cx="206" cy="-188" rx="20" ry="13" fill="url(#bodyA3)" stroke-width="4.5"/>')
        c.append('<path d="M-180 -172 L-140 -312 Q-134 -328 -114 -328 L114 -328 Q134 -328 140 -312 L180 -172Z" fill="url(#bodyA3)" stroke-width="5"/>')
        c.append('<path d="M-212 -60 L-212 -140 Q-210 -168 -186 -176 L186 -176 Q210 -168 212 -140 L212 -60Z" fill="url(#bodyA3)" stroke-width="5"/>')
        c.append('<path d="M-200 -166 Q0 -184 200 -166" fill="none" stroke="#fff" stroke-width="4" opacity=".7"/>')
        # windshield with the driver
        c.append('<path d="M-160 -184 L-126 -300 Q-122 -309 -108 -309 L108 -309 Q122 -309 126 -300 L160 -184Z" fill="url(#glassA3)" stroke-width="4.5"/>')
        shades = ('<g stroke="#07060c" stroke-width="3"><ellipse cx="-10" cy="-66" rx="16.5" ry="12.5" fill="#0b0a12"/><ellipse cx="22" cy="-66" rx="16.5" ry="12.5" fill="#0b0a12"/>'
                  '<path d="M6.5 -67 q0 -4 0 0" fill="none"/><path d="M5 -68 h1" fill="none"/><path d="M4 -69 Q6 -73 8 -69" fill="none" stroke-width="3.4"/>'
                  '<path d="M-26 -68 l-10 -3 M38 -68 l8 -3" fill="none" stroke-width="3.4"/></g>'
                  '<path d="M-19 -72 l8 -3 M13 -72 l8 -3" stroke="#bff4ff" stroke-width="2.6" opacity=".9"/>'
                  '<path d="M-14 -60 l9 -2 M18 -60 l9 -2" stroke="#ff9ad0" stroke-width="2" opacity=".6"/>')
        fsl = 2.1 / u
        inner = ('<path d="M-118 -205 q0 -46 30 -50 q30 4 30 50z" fill="#0a0d1c" stroke="none" opacity=".8"/>'   # empty passenger headrest
                 + '<ellipse cx="52" cy="-250" rx="80" ry="60" fill="#7fb8ff" opacity=".28" filter="url(#b12)" stroke="none"/>'
                 + frog(54, -150, fsl, look=(0, 0), mouth='O', brows=True, front=shades)
                 + '<ellipse cx="52" cy="-185" rx="52" ry="13" fill="none" stroke="#07060c" stroke-width="9"/>'
                 + '<ellipse cx="52" cy="-185" rx="52" ry="13" fill="none" stroke="#3a3446" stroke-width="4"/>'
                 + f'<circle cx="14" cy="-190" r="10" fill="{GREEN}" stroke="{INK}" stroke-width="3"/><circle cx="92" cy="-191" r="10" fill="{GREEN}" stroke="{INK}" stroke-width="3"/>'
                 + '<rect x="-22" y="-304" width="44" height="14" rx="5" fill="#2a2838" stroke-width="3"/>'
                 + '<path d="M-150 -196 L-100 -300 L-70 -300 L-128 -196Z" fill="#cfefff" opacity=".13" stroke="none"/>'
                 + '<path d="M100 -300 L120 -300 L70 -196 L52 -196Z" fill="#cfefff" opacity=".09" stroke="none"/>')
        c.append(f'<g clip-path="url(#wsA3)">{inner}</g>')
        c.append('<path d="M-160 -184 L-126 -300 Q-122 -309 -108 -309 L108 -309 Q122 -309 126 -300 L160 -184Z" fill="none" stroke-width="5"/>')
        c.append('<path d="M-200 -176 L-170 -176 M170 -176 L200 -176" stroke-width="4"/>')
        # face: grille, headlights, bumper, plate
        c.append('<rect x="-86" y="-140" width="172" height="58" rx="16" fill="#26222f" stroke-width="4.5"/>')
        for gx in range(-66, 70, 22):
            c.append(f'<path d="M{gx} -132 V-90" stroke="#bfc4d2" stroke-width="4"/>')
        for sx in (-1, 1):
            hx = 140 * sx
            c.append(f'<circle cx="{hx}" cy="-112" r="60" fill="#fff4cf" opacity=".45" filter="url(#b12)" stroke="none"/>')
            c.append(f'<circle cx="{hx}" cy="-112" r="34" fill="#d8dce6" stroke-width="5"/><circle cx="{hx}" cy="-112" r="25" fill="#fffdf2" stroke="#c9b27a" stroke-width="3"/>')
            c.append(f'<circle cx="{hx - 8}" cy="-120" r="7" fill="#fff" stroke="none"/>')
            c.append(f'<rect x="{hx + sx * 40 - 9}" y="-152" width="18" height="12" rx="4" fill="#ffb347" stroke-width="3"/>')
        c.append('<rect x="-222" y="-78" width="444" height="30" rx="15" fill="#d6dae4" stroke-width="5"/><path d="M-206 -70 H206" stroke="#fff" stroke-width="4" opacity=".8"/>')
        c.append('<rect x="-46" y="-74" width="92" height="26" rx="5" fill="#cfefff" stroke-width="3.5"/><path d="M-34 -61 h68" stroke="#7fc7e0" stroke-width="3" stroke-dasharray="6 6"/>')
        # hologram rim light on the right edge
        c.append('<path d="M140 -312 L180 -172 Q210 -168 212 -140 L212 -60" fill="none" stroke="#9ff0ff" stroke-width="4" opacity=".75"/>')
        c.append('</g>')
        b += ''.join(c)
        # the car's back-right corner flickering into pixels like the street
        for _ in range(26):
            x = CXc + r2.uniform(150, 280) * u; y = CYc - r2.uniform(150, 360) * u; s = r2.choice([6, 8, 10, 12])
            if x < 1350:
                b += f'<rect x="{x:.0f}" y="{y:.0f}" width="{s}" height="{s}" fill="{r2.choice(["#9ff0ff", "#d8fbff", "#ff9ad0"])}" opacity="{r2.uniform(.4, .85):.2f}"/>'
        b += spark(CXc - 120 * u, CYc - 300 * u, 18, '#e8fbff')

    # ---------------- foreground: two open hands with the red and the blue pill ----------------
    K = 235
    HL = (770, 1040, -12, 'R')    # screen-left hand: palm toward us, thumb inward (right)
    HR = (1490, 1040, 12, 'L')    # screen-right hand: thumb inward (left)

    def at(hd, px, py):
        x, y, a, _ = hd; t = math.radians(a)
        return x + (px * math.cos(t) - py * math.sin(t)) * K, y + (px * math.sin(t) + py * math.cos(t)) * K

    SKIN, LINE = '#e2a77f', '#24160f'
    for nm, hd in (('L', HL), ('R', HR)):
        d += f'<mask id="m{nm}A2">{hand(hd[0], hd[1], hd[2], K, hd[3], "palm", "open", skin="#fff", line="#fff", creases=False)}</mask>'
    for hd, pc, pg in ((HL, '#ff3b2f', 'L'), (HR, '#3c8cff', 'R')):
        sl = [at(hd, -.5, -.04), at(hd, .5, -.04), at(hd, .62, .75), at(hd, -.62, .75)]
        b += f'<ellipse cx="{hd[0]}" cy="{hd[1] - 150}" rx="230" ry="260" fill="{pc}" opacity=".09" filter="url(#b50)"/>'
        b += quad(sl, fill='url(#sleeveA2)', stroke='#05040a', stroke_width='6')
        c1, c2 = at(hd, -.5, .06), at(hd, .5, .06)
        b += f'<path d="M{c1[0]:.0f} {c1[1]:.0f} L{c2[0]:.0f} {c2[1]:.0f}" stroke="#3a3350" stroke-width="5"/>'
        r1, r2 = at(hd, .52 if pg == 'R' else -.52, 0), at(hd, .64 if pg == 'R' else -.64, .75)
        b += f'<path d="M{r1[0]:.0f} {r1[1]:.0f} L{r2[0]:.0f} {r2[1]:.0f}" stroke="#8fe8ff" stroke-width="4" opacity=".55"/>'
        b += hand(hd[0], hd[1], hd[2], K, hd[3], 'palm', 'open', skin=SKIN, line=LINE)
        pcx, pcy = at(hd, 0, -.55)
        b += (f'<g mask="url(#m{pg}A2)"><rect x="{hd[0] - 400}" y="{hd[1] - 300}" width="800" height="340" fill="#2a0f1c" opacity=".0"/>'
              f'<ellipse cx="{hd[0]}" cy="{hd[1] + 40}" rx="200" ry="150" fill="#3a1a2a" opacity=".35" filter="url(#b24)"/>'
              f'<circle cx="{pcx:.0f}" cy="{pcy:.0f}" r="150" fill="{pc}" opacity=".24" filter="url(#b24)"/>'
              f'<ellipse cx="{at(hd, .55 if pg == "L" else -.55, -1.2)[0]:.0f}" cy="{at(hd, 0, -1.3)[1]:.0f}" rx="70" ry="230" fill="#bff4ff" opacity=".18" filter="url(#b24)"/></g>')
    rx_, ry_ = at(HL, .02, -.55)
    bx_, by_ = at(HR, -.02, -.55)
    b += _pill(rx_, ry_, -28, 196, 84, 'pR2', '#ff2a1a', '#5a0a10')
    b += _pill(bx_, by_, 28, 196, 84, 'pB2', '#2a7aff', '#0a1a5a')
    b += spark(rx_ + 60, ry_ - 50, 26) + spark(bx_ - 70, by_ - 52, 24, '#eef6ff')
    # ---- (v2) the frog, sitting on the left thumb, torn between the two pills ----
    if variant == 'frog':
        tx, ty = at(HL, .64, -.80)
        fs = 2.4
        fx, fy = tx + 12, ty - 34
        b += f'<ellipse cx="{tx + 4:.0f}" cy="{ty - 22:.0f}" rx="58" ry="12" fill="#24160f" opacity=".4" filter="url(#b6)"/>'
        b += f'<circle cx="{fx:.0f}" cy="{fy - 110:.0f}" r="150" fill="#bff4ff" opacity=".12" filter="url(#b24)"/>'
        b += frog(fx, fy, fs, look=(6, 3), mouth='O', armL='M-34 -22 q-16 6 -20 24', armR='M38 -24 q24 -2 40 -18',
                  legs=((-20, -6, -20, 4, 0), (20, -6, 24, 4, 0)))
        b += spark(fx - 150, fy - 230, 20, '#e8fbff') + spark(1560, 140, 22) + spark(1240, 260, 16, '#e8fbff') + spark(1780, 470, 18)
    else:
        b += spark(1560, 140, 22) + spark(1240, 260, 16, '#e8fbff') + spark(1780, 470, 18)
    b += '<rect width="1920" height="1080" fill="url(#vigA2)"/>'
    lines = [('THE WORLD', 136, 'w'), ('MIGHT BE', 136, 'w'), ('PROJECTED', 172, 'y')]
    return page('#080c2c', svg(d, b), lines, outline='#07061a', top=44)


# =============================== B: credit-card hologram ===============================
# rough continents as (lon, lat) degree outlines
CONT = [
    [(-17, 15), (-5, 36), (10, 37), (32, 31), (43, 12), (51, 11), (40, -15), (35, -25), (20, -35), (12, -18), (9, 4), (-8, 5)],     # Africa
    [(-10, 37), (-9, 43), (-2, 48), (-5, 58), (8, 63), (25, 71), (40, 67), (60, 70), (90, 75), (140, 72), (160, 62), (140, 50), (122, 40),
     (120, 25), (105, 10), (95, 20), (80, 8), (72, 20), (57, 25), (50, 30), (35, 36), (28, 41), (15, 38), (5, 43)],                  # Eurasia
    [(-80, 9), (-77, 0), (-80, -6), (-72, -18), (-71, -30), (-74, -50), (-67, -55), (-63, -40), (-53, -34), (-48, -26), (-35, -7), (-50, 0), (-60, 8)],  # S America
    [(-168, 66), (-140, 70), (-95, 72), (-80, 64), (-60, 55), (-66, 45), (-76, 35), (-81, 26), (-97, 20), (-88, 15), (-83, 9), (-105, 22),
     (-117, 32), (-124, 42), (-125, 50), (-150, 60)],                                                                                 # N America
    [(-50, 60), (-25, 70), (-20, 80), (-55, 82), (-70, 77), (-55, 66)],                                                               # Greenland
    [(114, -22), (122, -18), (136, -12), (145, -16), (153, -27), (147, -38), (138, -35), (130, -31), (115, -34)],                     # Australia
]


def densify(pts, step=4):
    out = []
    for i in range(len(pts)):
        a, b_ = pts[i], pts[(i + 1) % len(pts)]
        n = max(1, int(max(abs(b_[0] - a[0]), abs(b_[1] - a[1])) / step))
        out += [(a[0] + (b_[0] - a[0]) * k / n, a[1] + (b_[1] - a[1]) * k / n) for k in range(n)]
    return out


def make_B():
    rnd = random.Random(11)
    d = FILTERS
    d += rad('bgB', 1300, 380, 1300, [(0, '#4a2a6e', 1), (.45, '#24143e', 1), (1, '#0c0716', 1)])
    d += rad('warmB', 1700, 80, 700, [(0, '#ffb470', .45), (1, '#ffb470', 0)])
    d += lin('deskB', [(0, '#2a1830'), (1, '#0d0710')])
    d += lin('cardB', [(0, '#1d5a73'), (.45, '#123a55'), (1, '#0b1d33')], x2=1, y2=1)
    d += lin('sheenB', [(0, '#ffffff', ), (1, '#ffffff')], x2=1, y2=0)
    d += lin('rainbow', [(0, '#ff6ad5'), (.2, '#ffb26b'), (.4, '#fff38a'), (.6, '#6bffb8'), (.8, '#6bc8ff'), (1, '#b46bff')], x2=1, y2=1)
    d += lin('beamB', [(0, '#fff6c8'), (.5, '#9be8ff'), (1, '#ff9be8')], x2=0, y2=1)
    d += '<linearGradient id="beamFade" x1="0" y1="1" x2="0" y2="0"><stop offset="0" stop-color="#fff" stop-opacity=".8"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>'
    d += '<mask id="beamMask"><rect width="1920" height="1080" fill="url(#beamFade)"/></mask>'
    d += rad('oceanB', 1250, 300, 330, [(0, '#8ff4ff', 1), (.45, '#2aa6d8', 1), (1, '#0c3a7a', 1)])
    d += rad('haloB', 1330, 400, 470, [(0, '#e8fbff', .6), (.45, '#7fd8ff', .25), (1, '#b46bff', 0)])
    d += rad('vigB', 1200, 500, 1250, [(0, '#000', 0), (.65, '#000', 0), (1, '#000', .7)])
    d += '<clipPath id="globeClip"><circle cx="1330" cy="390" r="235"/></clipPath>'
    b = '<rect width="1920" height="1080" fill="url(#bgB)"/><rect width="1920" height="1080" fill="url(#warmB)"/>'
    # background bokeh lights
    for _ in range(26):
        x, y, r = rnd.uniform(700, 1900), rnd.uniform(20, 640), rnd.uniform(14, 46)
        b += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r:.0f}" fill="{rnd.choice(["#ff9be8", "#9be8ff", "#ffd88a", "#c8a8ff"])}" opacity="{rnd.uniform(.06, .2):.2f}" filter="url(#b6)"/>'
    # desk
    HY = 735
    b += f'<rect y="{HY}" width="1920" height="{1080 - HY}" fill="url(#deskB)"/>'
    b += f'<rect y="{HY - 2}" width="1920" height="4" fill="#ffd0f0" opacity=".25"/>'
    for i in range(9):
        y = HY + 20 + i * i * 4.4
        b += f'<path d="M0 {y:.0f} Q960 {y + 8:.0f} 1920 {y - 4:.0f}" stroke="#3a2442" stroke-width="2" fill="none" opacity=".6"/>'
    # ---- the card in perspective ----
    TL, TR, BR, BL = (790, 805), (1490, 748), (1580, 930), (830, 1015)
    def at(u, v):   # bilinear position on the card (u along width, v along height)
        top = (TL[0] + (TR[0] - TL[0]) * u, TL[1] + (TR[1] - TL[1]) * u)
        bot = (BL[0] + (BR[0] - BL[0]) * u, BL[1] + (BR[1] - BL[1]) * u)
        return (top[0] + (bot[0] - top[0]) * v, top[1] + (bot[1] - top[1]) * v)
    b += f'<path d="{poly([(TL[0] + 10, TL[1] + 30), (TR[0] + 20, TR[1] + 26), (BR[0] + 20, BR[1] + 26), (BL[0] + 10, BL[1] + 30)])}" fill="#000" opacity=".55" filter="url(#b12)"/>'
    # card edge (thickness)
    b += f'<path d="{poly([BL, BR, (BR[0], BR[1] + 12), (BL[0], BL[1] + 12)])}" fill="#08121e" stroke="#02060c" stroke-width="3"/>'
    b += f'<path d="{poly([TL, TR, BR, BL])}" fill="url(#cardB)" stroke="#02060c" stroke-width="5" stroke-linejoin="round"/>'
    b += f'<path d="{poly([at(.0, .55), at(.35, .0), at(.55, .0), at(.12, 1.0), at(.0, 1.0)])}" fill="#ffffff" opacity=".07"/>'
    b += f'<path d="M{TL[0] + 6} {TL[1] + 2} L{TR[0] - 6} {TR[1] + 2}" stroke="#9fe0ff" stroke-width="3" opacity=".6"/>'
    # gold chip
    chip = [at(.08, .3), at(.2, .3), at(.2, .58), at(.08, .58)]
    b += f'<path d="{poly(chip)}" fill="#e2b85a" stroke="#6a4a14" stroke-width="3" stroke-linejoin="round"/>'
    for v in (.39, .49):
        p0, p1 = at(.08, v), at(.2, v)
        b += f'<path d="M{p0[0]:.0f} {p0[1]:.0f} L{p1[0]:.0f} {p1[1]:.0f}" stroke="#8a6420" stroke-width="2.4"/>'
    p0, p1 = at(.14, .3), at(.14, .58)
    b += f'<path d="M{p0[0]:.0f} {p0[1]:.0f} L{p1[0]:.0f} {p1[1]:.0f}" stroke="#8a6420" stroke-width="2.4"/>'
    # embossed dot groups (no real number) and a name bar
    for g in range(4):
        for k in range(4):
            u = .08 + g * .13 + k * .027
            x, y = at(u, .74)
            b += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="5" fill="#cfe6f2" opacity=".8"/>'
    p0, p1 = at(.08, .88), at(.36, .88)
    b += f'<path d="M{p0[0]:.0f} {p0[1]:.0f} L{p1[0]:.0f} {p1[1]:.0f}" stroke="#cfe6f2" stroke-width="7" stroke-linecap="round" opacity=".45"/>'
    # hologram sticker (flat film): rainbow foil with diffraction lines
    st = [at(.62, .32), at(.86, .32), at(.86, .8), at(.62, .8)]
    b += f'<path d="{poly(st)}" fill="url(#rainbow)" stroke="#f4f0ff" stroke-width="3" stroke-linejoin="round"/>'
    for k in range(1, 12):
        u = .62 + .24 * k / 12
        p0, p1 = at(u, .32), at(u - .03, .8)
        b += f'<path d="M{p0[0]:.0f} {p0[1]:.0f} L{p1[0]:.0f} {p1[1]:.0f}" stroke="#fff" stroke-width="2" opacity=".35"/>'
    SC = at(.74, .56)
    b += f'<ellipse cx="{SC[0]:.0f}" cy="{SC[1]:.0f}" rx="150" ry="50" fill="#fff6d8" opacity=".55" filter="url(#b24)"/>'
    # ---- light beam from the sticker up to the globe ----
    GX, GY, GR = 1330, 390, 235
    beam = f'M{st[3][0]:.0f} {st[3][1]:.0f} L{st[0][0]:.0f} {st[0][1]:.0f} L{GX - GR * 1.02:.0f} {GY + 40} L{GX + GR * 1.02:.0f} {GY + 40} L{st[1][0]:.0f} {st[1][1]:.0f} L{st[2][0]:.0f} {st[2][1]:.0f}Z'
    b += f'<g mask="url(#beamMask)"><path d="{beam}" fill="url(#rainbow)" opacity=".38" filter="url(#b12)"/><path d="{beam}" fill="url(#beamB)" opacity=".22"/></g>'
    for k in range(9):
        t = k / 8
        x0 = st[0][0] + (st[1][0] - st[0][0]) * t; y0 = st[0][1] + (st[1][1] - st[0][1]) * t
        x1 = GX - GR + 2 * GR * t
        b += f'<path d="M{x0:.0f} {y0:.0f} L{x1:.0f} {GY + 120 - 120 * abs(t - .5):.0f}" stroke="#e8fbff" stroke-width="2" opacity=".25"/>'
    # floating light motes inside the beam
    for _ in range(40):
        t = rnd.random(); h = rnd.random()
        x = (st[0][0] + 100 * t) * (1 - h) + (GX - GR + 2 * GR * t) * h; y = st[0][1] * (1 - h) + (GY + 150) * h
        b += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{rnd.uniform(1.5, 4):.1f}" fill="#fffbe8" opacity="{rnd.uniform(.4, .9):.2f}"/>'
    # ---- the holographic globe ----
    b += f'<circle cx="{GX}" cy="{GY}" r="{GR * 2:.0f}" fill="url(#haloB)"/>'
    g = f'<circle cx="{GX}" cy="{GY}" r="{GR}" fill="url(#oceanB)" opacity=".92"/>'
    TILT, ROT = .35, math.radians(-15)
    for c in CONT:
        pts = [sph(math.radians(la), math.radians(lo), GR, GX, GY, TILT, ROT) for lo, la in densify(c)]
        if max(p[2] for p in pts) < 0:
            continue
        flat = []
        for x, y, z in pts:      # points behind the limb are pushed onto the limb
            if z < 0:
                dx, dy = x - GX, y - GY; L = math.hypot(dx, dy) or 1
                x, y = GX + dx / L * GR, GY + dy / L * GR
            flat.append((x, y))
        g += f'<path d="{poly(flat)}" fill="#4fd07a" stroke="#d8fff0" stroke-width="3" stroke-linejoin="round" opacity=".95"/>'
        g += f'<path d="{poly(flat)}" fill="#d8ff9a" opacity=".25" transform="translate(-6 -6)"/>'
    # grid lines (lat / lon)
    for la in range(-60, 90, 30):
        pts = [sph(math.radians(la), math.radians(lo), GR, GX, GY, TILT, ROT) for lo in range(0, 361, 6)]
        seg = [(x, y) for x, y, z in pts if z > 0]
        if len(seg) > 2:
            g += '<path d="M' + ' L'.join(f'{x:.0f},{y:.0f}' for x, y in seg) + '" fill="none" stroke="#e8fbff" stroke-width="2" opacity=".45"/>'
    for lo in range(0, 360, 30):
        pts = [sph(math.radians(la), math.radians(lo), GR, GX, GY, TILT, ROT) for la in range(-90, 91, 6)]
        seg = [(x, y) for x, y, z in pts if z > 0]
        if len(seg) > 2:
            g += '<path d="M' + ' L'.join(f'{x:.0f},{y:.0f}' for x, y in seg) + '" fill="none" stroke="#e8fbff" stroke-width="2" opacity=".45"/>'
    # hologram scanlines + shading
    for y in range(GY - GR, GY + GR, 9):
        g += f'<rect x="{GX - GR}" y="{y}" width="{2 * GR}" height="3" fill="#ffffff" opacity=".07"/>'
    g += f'<circle cx="{GX + 80}" cy="{GY + 90}" r="{GR}" fill="#1a0a40" opacity=".35" filter="url(#b50)"/>'
    b += f'<g clip-path="url(#globeClip)">{g}</g>'
    b += f'<circle cx="{GX}" cy="{GY}" r="{GR}" fill="none" stroke="#ff9be8" stroke-width="10" opacity=".55" filter="url(#b6)"/>'
    b += f'<circle cx="{GX}" cy="{GY}" r="{GR}" fill="none" stroke="#e8fbff" stroke-width="4"/>'
    b += f'<path d="M{GX - GR * .75:.0f} {GY - GR * .45:.0f} A{GR} {GR} 0 0 1 {GX - GR * .2:.0f} {GY - GR * .93:.0f}" fill="none" stroke="#fff" stroke-width="10" stroke-linecap="round" opacity=".7"/>'
    # orbiting moon + ring of light
    b += f'<ellipse cx="{GX}" cy="{GY + 20}" rx="{GR * 1.45:.0f}" ry="{GR * .32:.0f}" transform="rotate(-12 {GX} {GY})" fill="none" stroke="#fff3c0" stroke-width="4" opacity=".75"/>'
    b += f'<ellipse cx="{GX}" cy="{GY + 20}" rx="{GR * 1.45:.0f}" ry="{GR * .32:.0f}" transform="rotate(-12 {GX} {GY})" fill="none" stroke="#ffd27a" stroke-width="16" opacity=".3" filter="url(#b6)"/>'
    b += f'<circle cx="{GX + 330}" cy="{GY - 70}" r="34" fill="#efe6ff" stroke="#fff" stroke-width="3"/><circle cx="{GX + 342}" cy="{GY - 60}" r="34" fill="#7a5ab0" opacity=".45"/>'
    b += f'<circle cx="{GX + 330}" cy="{GY - 70}" r="60" fill="#c8a8ff" opacity=".3" filter="url(#b12)"/>'
    b += spark(GX - 280, GY - 150, 30) + spark(GX + 250, GY - 250, 22, '#ffe8fa') + spark(GX + 380, GY + 120, 18) + spark(GX - 330, GY + 170, 16, '#e8fbff')
    # ---- frog standing on the card with a magnifying glass ----
    fx, fy, fs = 690, 1000, 2.6
    glass = ('<g transform="translate(70 -60) rotate(-35)"><rect x="-5" y="0" width="10" height="44" rx="4" fill="#7a4a24" stroke-width="3"/>'
             '<circle cx="0" cy="-20" r="22" fill="#cfefff" fill-opacity=".35" stroke="#e2b85a" stroke-width="6"/><path d="M-12 -28 q6 -8 14 -8" fill="none" stroke="#fff" stroke-width="3"/></g>')
    b += f'<ellipse cx="{fx + 10}" cy="{fy + 8}" rx="120" ry="16" fill="#000" opacity=".45" filter="url(#b3)"/>'
    b += frog(fx, fy, fs, look=(8, -7), mouth='O', armR='M38 -22 q20 -10 30 -34', front=glass)
    b += '<rect width="1920" height="1080" fill="url(#vigB)"/>'
    lines = [('2D', 250, 'w'), ('= <span class="g">3D?</span>', 250, 'w')]
    return page('#160c22', svg(d, b), lines, outline='#0b0514', top=36)


# =============================== C: black hole with pixel horizon ===============================
def make_C():
    rnd = random.Random(23)
    d = FILTERS
    d += rad('bgC', 1350, 480, 1300, [(0, '#3a1440', 1), (.4, '#1a0a26', 1), (1, '#07040c', 1)])
    d += rad('nebC', 1650, 250, 600, [(0, '#ff6a3a', .4), (1, '#ff3a6a', 0)])
    d += rad('neb2', 900, 900, 600, [(0, '#7a3aff', .3), (1, '#7a3aff', 0)])
    d += rad('haloC', 1340, 500, 600, [(0, '#ffcf7a', .0), (.55, '#ffcf7a', .0), (.62, '#ffb35a', .55), (.75, '#ff6a8a', .2), (1, '#ff6a8a', 0)])
    d += rad('vigC', 1200, 500, 1250, [(0, '#000', 0), (.65, '#000', 0), (1, '#000', .7)])
    d += lin('diskC', [(0, '#ff5a2a'), (.3, '#ffb04a'), (.5, '#fff2c8'), (.7, '#ffb04a'), (1, '#ff5a2a')], x2=1, y2=0)
    d += lin('tapeC', [(0, '#ffe07a'), (1, '#e2a83a')])
    b = '<rect width="1920" height="1080" fill="url(#bgC)"/><rect width="1920" height="1080" fill="url(#nebC)"/><rect width="1920" height="1080" fill="url(#neb2)"/>'
    for _ in range(220):
        b += f'<circle cx="{rnd.uniform(0, 1920):.0f}" cy="{rnd.uniform(0, 1080):.0f}" r="{rnd.choice([1.2, 1.8, 2.5])}" fill="#fff4e8" opacity="{rnd.uniform(.2, .8):.2f}"/>'
    CX, CY, R = 1330, 500, 320
    TILT, ROT = -.38, .2
    # accretion disk (tilted), back half first
    DA, DB, DROT = R * 1.85, R * .42, -14
    def disk(half):
        o = ''
        for k, (w, op, blur) in enumerate(((70, .35, 24), (34, .7, 6), (12, 1, 0), (4, 1, 0))):
            col = 'url(#diskC)' if k < 3 else '#fffbe8'
            sweep = 1 if half == 'back' else 0
            path = f'M{CX - DA:.0f} {CY} A{DA:.0f} {DB:.0f} 0 0 {sweep} {CX + DA:.0f} {CY}'
            f_ = f' filter="url(#b{blur})"' if blur else ''
            o += f'<path d="{path}" fill="none" stroke="{col}" stroke-width="{w}" opacity="{op}"{f_}/>'
        for k in range(1, 4):
            path = f'M{CX - DA * (1 + k * .09):.0f} {CY} A{DA * (1 + k * .09):.0f} {DB * (1 + k * .09):.0f} 0 0 {1 if half == "back" else 0} {CX + DA * (1 + k * .09):.0f} {CY}'
            o += f'<path d="{path}" fill="none" stroke="#ffb04a" stroke-width="3" opacity="{.4 - k * .1:.2f}"/>'
        return f'<g transform="rotate({DROT} {CX} {CY})">{o}</g>'
    b += f'<circle cx="{CX}" cy="{CY}" r="{R * 1.9:.0f}" fill="url(#haloC)"/>'
    b += disk('back')
    # the horizon sphere: dark base + tiles of bits
    b += f'<circle cx="{CX}" cy="{CY}" r="{R + 14}" fill="#ffcf7a" opacity=".55" filter="url(#b12)"/>'
    b += f'<circle cx="{CX}" cy="{CY}" r="{R}" fill="#05030a"/>'
    NLAT, NLON = 16, 32
    tiles = ''; glow = ''
    for i in range(NLAT):
        for j in range(NLON):
            la0 = -math.pi / 2 + i * math.pi / NLAT; la1 = la0 + math.pi / NLAT
            lo0 = j * 2 * math.pi / NLON; lo1 = lo0 + 2 * math.pi / NLON
            gap = .12
            cs = [(la0 + gap * (la1 - la0), lo0 + gap * (lo1 - lo0)), (la0 + gap * (la1 - la0), lo1 - gap * (lo1 - lo0)),
                  (la1 - gap * (la1 - la0), lo1 - gap * (lo1 - lo0)), (la1 - gap * (la1 - la0), lo0 + gap * (lo1 - lo0))]
            pts = [sph(a, o_, R, CX, CY, TILT, ROT) for a, o_ in cs]
            z = sum(p[2] for p in pts) / 4
            if z <= .03:
                continue
            limb = 1 - z          # brighter near the edge (rim)
            on = rnd.random() < .42
            col = rnd.choice(['#ffd27a', '#ffd27a', '#ffe9b0', '#7ae8ff', '#ff8ac8']) if on else '#2a1a3a'
            op = (.35 + .65 * limb ** .6) if on else (.5 + .3 * limb)
            path = poly([(p[0], p[1]) for p in pts])
            tiles += f'<path d="{path}" fill="{col}" opacity="{op:.2f}" stroke="#5a3a6a" stroke-width="1.2"/>'
            if on and z > .45 and rnd.random() < .35:
                mx = sum(p[0] for p in pts) / 4; my = sum(p[1] for p in pts) / 4
                tiles += f'<text x="{mx:.0f}" y="{my + 8 * z:.0f}" font-size="{22 * z:.0f}" text-anchor="middle" fill="#3a1a08" opacity=".75" {MONO}>{rnd.choice("01")}</text>'
            if on:
                glow += f'<path d="{path}" fill="{col}" opacity="{op * .8:.2f}"/>'
    b += f'<g filter="url(#b6)">{glow}</g>' + tiles
    # inner shadow: centre darker, as if the tiles sit on a curved surface
    d += rad('shadeC', CX + 30, CY + 30, R, [(0, '#05030a', .5), (.65, '#05030a', .2), (1, '#05030a', 0)])
    b += f'<circle cx="{CX}" cy="{CY}" r="{R}" fill="url(#shadeC)"/>'
    b += f'<circle cx="{CX}" cy="{CY}" r="{R}" fill="none" stroke="#fff0c8" stroke-width="4" opacity=".8"/>'
    b += disk('front')
    # a falling book shedding bits onto the horizon (upper right)
    BX, BY = 1745, 150
    b += f'<circle cx="{BX}" cy="{BY}" r="90" fill="#ffe9b0" opacity=".25" filter="url(#b24)"/>'
    b += (f'<g transform="translate({BX} {BY}) rotate(28)" stroke="#2a1408" stroke-width="4" stroke-linejoin="round">'
          '<path d="M-70 -44 L0 -34 L70 -44 L70 40 L0 50 L-70 40Z" fill="#b23a3a"/>'
          '<path d="M-62 -38 L0 -28 L0 42 L-62 34Z" fill="#fff4dc"/><path d="M62 -38 L0 -28 L0 42 L62 34Z" fill="#f4e6c4"/>'
          '<path d="M-52 -20 L-10 -14 M-52 -6 L-10 0 M-52 8 L-10 14 M52 -20 L10 -14 M52 -6 L10 0 M52 8 L10 14" stroke="#b8a07a" stroke-width="3"/></g>')
    for k in range(26):
        t = k / 25
        x = BX + (CX + R * .55 - BX) * t + rnd.uniform(-30, 30) * (1 - t)
        y = BY + 40 + (CY - R * .78 - BY - 40) * t ** 1.2 + rnd.uniform(-20, 20)
        s = 16 - 9 * t
        col = rnd.choice(['#ffd27a', '#ffe9b0', '#7ae8ff'])
        b += f'<rect x="{x - s / 2:.0f}" y="{y - s / 2:.0f}" width="{s:.0f}" height="{s:.0f}" fill="{col}" opacity="{.9 - .4 * t:.2f}" transform="rotate(20 {x:.0f} {y:.0f})"/>'
    b += spark(CX - R - 40, CY - R + 20, 26) + spark(CX + R + 60, CY + R - 20, 20, '#ffe8c8') + spark(1560, 110, 18)
    # ---- astronaut frog measuring the surface with a tape ----
    fx, fy, fs = 600, 1000, 2.5
    # tape ribbon from the frog's hand to the sphere, then hugging the limb
    hx, hy = fx + 70 * fs, fy - 58 * fs
    ax, ay = CX - R * math.cos(.5), CY + R * math.sin(.5)
    tape = f'M{hx:.0f} {hy:.0f} Q{(hx + ax) / 2:.0f} {hy - 10:.0f} {ax:.0f} {ay:.0f} A{R + 6} {R + 6} 0 0 1 {CX - R - 6} {CY - 40}'
    b += f'<path d="{tape}" fill="none" stroke="#2a1408" stroke-width="22" stroke-linecap="round"/>'
    b += f'<path d="{tape}" fill="none" stroke="url(#tapeC)" stroke-width="15" stroke-linecap="round"/>'
    b += f'<path d="{tape}" fill="none" stroke="#2a1408" stroke-width="5" stroke-dasharray="2 16" opacity=".7"/>'
    suit = ('<path d="M-38 -20 Q-46 0 -40 8 L44 8 Q50 0 42 -20 Q4 -30 -38 -20Z" fill="#eef0f4" stroke-width="3.4"/>'
            '<rect x="-14" y="-14" width="30" height="16" rx="4" fill="#9aa6b8" stroke-width="2.6"/><circle cx="-6" cy="-6" r="3" fill="#ff6a6a" stroke="none"/><circle cx="6" cy="-6" r="3" fill="#7ae8ff" stroke="none"/>')
    helm = ('<circle cx="6" cy="-58" r="48" fill="#bfe6ff" fill-opacity=".16" stroke="#e8eef6" stroke-width="5"/>'
            '<path d="M-28 -84 q12 -18 34 -22" fill="none" stroke="#fff" stroke-width="5" opacity=".85"/>'
            '<path d="M40 -86 q8 6 10 18" fill="none" stroke="#ffcf7a" stroke-width="4" opacity=".7"/>'
            '<g transform="translate(70 -58)"><rect x="-14" y="-14" width="28" height="28" rx="6" fill="#e2b85a" stroke-width="3"/><circle cx="0" cy="0" r="6" fill="#7a4a14" stroke="none"/></g>')
    b += f'<circle cx="{fx}" cy="{fy - 120}" r="160" fill="#ffd8a8" opacity=".14" filter="url(#b24)"/>'
    b += frog(fx, fy, fs, rot=-6, look=(9, -6), mouth='O', back='', mid=suit, armR='M38 -22 q22 -8 32 -36', armL='M-34 -22 q-20 -2 -26 -26',
              legs=((-20, -6, -30, 10, -20), (20, -6, 30, 6, 20)), front=helm)
    b += '<rect width="1920" height="1080" fill="url(#vigC)"/>'
    lines = [('SURFACE,', 172, 'y'), ('NOT', 108, 'w'), ('VOLUME', 172, 'w')]
    return page('#0c0614', svg(d, b), lines, outline='#07030c', top=44)


if __name__ == '__main__':
    which = sys.argv[1:] or ['A', 'B', 'C']
    for n in which:
        fn = globals().get(f'make_{n}')
        if fn:
            open(os.path.join(HERE, f'{n}.html'), 'w').write(fn())
    print('ok')
