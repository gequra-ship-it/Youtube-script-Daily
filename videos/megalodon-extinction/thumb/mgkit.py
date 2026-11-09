# Shared drawing kit for the megalodon-extinction thumbnails (long A-C: ./make.py, shorts: ../../megalodon-extinction-shortN/thumb/make.py).
# frog(): channel notebook frog (tools/assets/frog.svg body, guideline 16-8), pupils kept inside the eye whites (16-9, tools/eyecheck.py).
# shark(): detailed side-view Megalodon (countershading, rim light, gills, open/closed jaws, serrated teeth).
import os, sys, math, random
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', '..', 'tools'))
from thumb_lib import lin, rad, spark

INK = '#1d2b1c'; GREEN = '#6aa55a'; DARKG = '#4d8a4a'; BELLY = '#9cc98a'
FILTERS = ''.join(f'<filter id="b{n}" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="{n}"/></filter>' for n in (2, 3, 6, 12, 24, 50))


def P(pts):
    return ' '.join(f'{a:.1f},{b:.1f}' for a, b in pts)


# ------------------------------------------------------------------ frog ------------------------------------------------------------------
def limb(d, col=GREEN, w=7.5, wi=3.4):
    return f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="{w}"/><path d="{d}" fill="none" stroke="{col}" stroke-width="{wi}"/>'


def end_of(d):
    n = [float(v) for v in d.replace('M', ' ').replace('q', ' ').split()]
    return n[0] + n[-2], n[1] + n[-1]


def frog(x, y, s, rot=0, flip=False, look=(0, 0), mouth='O', armL=None, armR=None, legs=None, helmet=False,
         back='', mid='', front='', head='', shadow=False):
    """feet at (x, y), ~90 units tall * s. back: behind body; mid: over body, under arms; head: over the head (hats); front: last."""
    lx, ly = look
    assert math.hypot(lx + 1, ly) + 4.4 <= 13.5 - 2.2, 'pupil would leave the eye white'
    sx = -s if flip else s
    g = [f'<g transform="translate({x} {y}) rotate({rot}) scale({sx} {s})" stroke="{INK}" stroke-linejoin="round" stroke-linecap="round">', back]
    if shadow:
        g.append('<ellipse cx="0" cy="8" rx="52" ry="8" fill="#000" opacity=".25" stroke="none"/>')
    if helmet:
        g.append('<rect x="-52" y="-60" width="20" height="44" rx="7" fill="#d9b25a" stroke-width="3"/><rect x="-48" y="-54" width="5" height="30" rx="2" fill="#fff" stroke="none" opacity=".6"/>')
    for hx, hy, fx, fy, fa in (legs or ((-20, -6, -22, 4, 0), (20, -6, 22, 4, 0))):
        if abs(fx - hx) + abs(fy - hy) > 14:
            g.append(limb(f'M{hx} {hy} L{fx} {fy}', GREEN, 15, 9))
        g.append(f'<ellipse cx="{fx}" cy="{fy}" rx="16" ry="9" transform="rotate({fa} {fx} {fy})" fill="{DARKG}" stroke-width="3.2"/>')
    g.append(f'<path d="M-34 0 q-6 -64 34 -70 q40 -2 42 62 q0 10 -6 12 q-36 6 -70 -4z" fill="{GREEN}" stroke-width="4"/>')
    g.append(f'<ellipse cx="2" cy="-12" rx="22" ry="20" fill="{BELLY}" stroke="none" opacity=".7"/>')
    g.append('<path d="M-24 -50 q6 -14 18 -16" fill="none" stroke="#b6dea0" stroke-width="3" opacity=".8"/>')
    g.append(mid)
    for ex in (-10, 22):
        g.append(f'<circle cx="{ex}" cy="-66" r="13.5" fill="#f4f5ea" stroke-width="3.2"/>')
        g.append(f'<circle cx="{ex + 1 + lx}" cy="{-66 + ly}" r="4.4" fill="{INK}" stroke="none"/>')
        g.append(f'<circle cx="{ex + 2.4 + lx}" cy="{-67.6 + ly}" r="1.5" fill="#fff" stroke="none"/>')
    g.append('<path d="M-22 -88 q12 -9 24 -1 M10 -89 q12 -8 24 1" fill="none" stroke-width="3.4"/>')
    if mouth == 'O':
        g.append('<ellipse cx="6" cy="-38" rx="10" ry="12" fill="#7a2f33" stroke-width="3"/><ellipse cx="6" cy="-31" rx="6" ry="4" fill="#e07b7b" stroke="none"/>')
    else:
        g.append('<ellipse cx="6" cy="-41" rx="6" ry="7.5" fill="#7a2f33" stroke-width="3"/>')
    g.append('<ellipse cx="-18" cy="-48" rx="5" ry="3" fill="#e98a8a" stroke="none" opacity=".55"/><ellipse cx="30" cy="-48" rx="5" ry="3" fill="#e98a8a" stroke="none" opacity=".55"/>')
    g.append(head)
    if helmet:
        g.append('<circle cx="6" cy="-58" r="46" fill="#bfe6ff" fill-opacity=".14" stroke="#e8f6ff" stroke-width="3.4" stroke-opacity=".95"/>')
        g.append('<path d="M-26 -82 q12 -18 32 -21" fill="none" stroke="#fff" stroke-width="5" opacity=".8"/><path d="M43 -40 q6 -10 6 -22" fill="none" stroke="#fff" stroke-width="3" opacity=".5"/>')
        g.append('<ellipse cx="6" cy="-15" rx="41" ry="9" fill="#d9b25a" stroke-width="3.2"/><path d="M-30 -17 q36 8 72 0" fill="none" stroke="#fff3c8" stroke-width="2.2" opacity=".8"/>')
    for a in (armL or 'M-34 -22 q-14 6 -16 22', armR or 'M38 -22 q14 6 16 22'):
        g.append(limb(a)); ex_, ey_ = end_of(a)
        g.append(f'<circle cx="{ex_:.1f}" cy="{ey_:.1f}" r="5.6" fill="{GREEN}" stroke-width="3"/>')
    g.append(front); g.append('</g>')
    return ''.join(g)


# ------------------------------------------------------------------ shark ------------------------------------------------------------------
BODY_CLOSED = ('M1000 12 C995 -20 960 -55 900 -80 C820 -112 720 -130 600 -132 C470 -130 360 -110 260 -75 C190 -50 130 -30 82 -18 L82 16 '
               'C130 26 200 50 280 78 C380 110 480 132 600 134 C720 132 810 110 870 82 C930 60 975 45 1000 12 Z')
BODY_OPEN = ('M1000 12 C995 -20 960 -55 900 -80 C820 -112 720 -130 600 -132 C470 -130 360 -110 260 -75 C190 -50 130 -30 82 -18 L82 16 '
             'C130 26 200 50 280 78 C380 110 480 132 600 134 C680 134 740 150 800 176 C850 198 896 212 926 202 L934 188 '
             'C902 150 862 112 822 86 C870 78 920 64 958 48 C980 40 996 30 1000 12 Z')
CAUDAL = 'M86 -16 C60 -70 10 -150 -82 -248 C-50 -160 -32 -80 -8 -2 C-32 60 -56 120 -76 182 C-10 122 40 62 86 14 Z'
DORSAL = 'M612 -128 C586 -205 540 -272 448 -314 C468 -236 452 -166 410 -112 Z'
DORSAL2 = 'M262 -70 C250 -90 238 -105 218 -114 C224 -96 222 -76 214 -58 Z'
PECT = 'M722 86 C694 172 622 258 542 318 C590 246 612 176 614 120 Z'
PELV = 'M342 96 C320 132 292 160 256 170 C270 142 276 110 272 82 Z'
ANAL = 'M224 62 C214 80 202 96 182 102 C188 86 188 70 186 54 Z'


def cub(p0, p1, p2, p3, t):
    u = 1 - t
    return (u ** 3 * p0[0] + 3 * u * u * t * p1[0] + 3 * u * t * t * p2[0] + t ** 3 * p3[0],
            u ** 3 * p0[1] + 3 * u * u * t * p1[1] + 3 * u * t * t * p2[1] + t ** 3 * p3[1])


def tooth_shape(w, h, col, shade, line, lw, bour=None):
    """one crown in a local frame: base on the x axis (-w/2..w/2), tip at (0, h)."""
    o = (f'<path d="M{-w / 2:.1f} 0 Q{-w * .3:.1f} {h * .5:.1f} 0 {h:.1f} Q{w * .3:.1f} {h * .5:.1f} {w / 2:.1f} 0 Q0 {h * .08:.1f} {-w / 2:.1f} 0Z" '
         f'fill="{col}" stroke="{line}" stroke-width="{lw}" stroke-linejoin="round"/>')
    o += f'<path d="M0 {h * .06:.1f} L0 {h:.1f} Q{w * .3:.1f} {h * .5:.1f} {w / 2 - lw:.1f} {lw:.1f}Z" fill="{shade}" opacity=".6"/>'
    o += f'<path d="M{-w * .2:.1f} {h * .14:.1f} Q{-w * .14:.1f} {h * .5:.1f} {-w * .03:.1f} {h * .82:.1f}" fill="none" stroke="#fff" stroke-width="{max(1.5, w * .06):.1f}" opacity=".45" stroke-linecap="round"/>'
    if bour:
        o += f'<path d="M{-w * .44:.1f} {h * .05:.1f} Q0 {h * .2:.1f} {w * .44:.1f} {h * .05:.1f}" fill="none" stroke="{bour}" stroke-width="{max(2, w * .1):.1f}" opacity=".8"/>'
    return o


def teeth_on(curve, n, ln, inward, t0=.08, t1=.95, col='#f6f1e2', shade='#c9c0a6', line='#1a1210', lw=2.2, wid=1.0, bour=None, seed=1):
    """serrated Megalodon crowns along a cubic curve; inward = +1/-1 picks the normal side the tips point to. col may be a list."""
    rnd = random.Random(seed); out = ''
    for i in range(n):
        t = t0 + (t1 - t0) * (i + .5) / n; dt = (t1 - t0) / n * .5
        a = cub(*curve, t - dt); b = cub(*curve, t + dt); m = cub(*curve, t)
        dx, dy = b[0] - a[0], b[1] - a[1]; L = math.hypot(dx, dy) or 1
        nx, ny = -dy / L * inward, dx / L * inward
        h = ln * (.75 + .5 * math.sin(math.pi * (i + .5) / n))
        w = L * 1.12 * wid
        ang = math.degrees(math.atan2(-nx, ny)) + rnd.uniform(-4, 4)
        c = rnd.choice(col) if isinstance(col, (list, tuple)) else col
        out += f'<g transform="translate({m[0]:.1f} {m[1]:.1f}) rotate({ang:.1f})">' + tooth_shape(w, h, c, shade, line, lw, bour) + '</g>'
    return out


def shark(x, y, s, rot=0, flip=False, mouth='closed', idp='sk', top='#34505f', mid='#6c8896', belly='#eef2f2', line='#0b161d',
          rim='#bff2ff', glow=None, glow_op=.55, mask=None, scars=True, eye_glint=True, gill_col=None, seed=3):
    """Megalodon side view, facing right (flip=True faces left). (x, y) = body centre; length ~1080 units * s (tail tip to nose)."""
    rnd = random.Random(seed)
    sx = -s if flip else s
    body = BODY_OPEN if mouth == 'open' else BODY_CLOSED
    d = (lin(idp + 'g', [(0, top), (.55, mid), (1, mid)]).replace('x2="0" y2="1"', 'x2="0" y2="1"')
         .replace('<linearGradient', '<linearGradient gradientUnits="userSpaceOnUse"').replace('x1="0" y1="0" x2="0" y2="1"', 'x1="0" y1="-320" x2="0" y2="140"'))
    d += (f'<linearGradient id="{idp}m" gradientUnits="userSpaceOnUse" x1="830" y1="60" x2="980" y2="140"><stop offset="0" stop-color="#1a0606"/>'
          f'<stop offset=".6" stop-color="#5a1418"/><stop offset="1" stop-color="#8a2a2a"/></linearGradient>')
    d += f'<clipPath id="{idp}c"><path d="{body}"/></clipPath>'
    g = [f'<g transform="translate({x} {y}) rotate({rot}) scale({sx} {s}) translate(-500 0)"' + (f' mask="url(#{mask})"' if mask else '') + '>']
    if glow:
        g.append(f'<g filter="url(#b24)" opacity="{glow_op}" fill="{glow}" stroke="{glow}" stroke-width="30">'
                 f'<path d="{CAUDAL}"/><path d="{DORSAL}"/><path d="{body}"/><path d="{PECT}"/></g>')
    F = f'fill="url(#{idp}g)" stroke="{line}" stroke-width="5" stroke-linejoin="round"'
    for fin in (CAUDAL, DORSAL, DORSAL2):
        g.append(f'<path d="{fin}" {F}/>')
    # rim light on the back edges of fins
    g.append(f'<path d="M86 -16 C60 -70 10 -150 -82 -248" fill="none" stroke="{rim}" stroke-width="5" opacity=".75"/>')
    g.append(f'<path d="M612 -128 C586 -205 540 -272 448 -314" fill="none" stroke="{rim}" stroke-width="6" opacity=".85"/>')
    if mouth == 'open':
        g.append(f'<path d="M822 86 C870 78 920 64 958 48 L934 188 C902 150 862 112 822 86 Z" fill="url(#{idp}m)" stroke="{line}" stroke-width="4"/>')
        g.append('<path d="M838 90 C880 84 920 72 950 60 L930 172 C900 140 868 112 838 90Z" fill="#2a0607" opacity=".6"/>')
        g.append(teeth_on(((836, 90), (876, 84), (916, 74), (948, 62)), 6, 20, 1, col='#bdb39a', shade='#8a806a', lw=1.6))
    g.append(f'<path d="{body}" {F}/>')
    clip = [f'<g clip-path="url(#{idp}c)">']
    clip.append(f'<path d="M1012 44 C960 52 900 34 840 44 C760 58 690 46 600 62 C500 78 420 66 340 56 C260 46 180 30 60 18 L60 320 L1012 320Z" fill="{belly}"/>')
    clip.append(f'<path d="M1012 44 C960 52 900 34 840 44 C760 58 690 46 600 62 C500 78 420 66 340 56 C260 46 180 30 60 18" fill="none" stroke="{mid}" stroke-width="10" opacity=".55" filter="url(#b3)"/>')
    clip.append(f'<ellipse cx="560" cy="160" rx="520" ry="60" fill="#0a1a24" opacity=".28" filter="url(#b12)"/>')
    clip.append(f'<ellipse cx="640" cy="-150" rx="420" ry="50" fill="{rim}" opacity=".35" filter="url(#b12)"/>')
    if scars:
        for _ in range(26):
            px, py = rnd.randint(260, 900), rnd.randint(-110, 10)
            clip.append(f'<circle cx="{px}" cy="{py}" r="{rnd.choice([2, 3, 4])}" fill="#dff4ff" opacity="{rnd.uniform(.12, .3):.2f}"/>')
        for _ in range(5):
            px, py = rnd.randint(360, 820), rnd.randint(-95, -10)
            clip.append(f'<path d="M{px} {py} l{rnd.randint(30, 60)} {rnd.randint(-8, 8)}" stroke="#d9eef7" stroke-width="3" opacity=".3" stroke-linecap="round"/>')
    clip.append('</g>')
    g += clip
    g.append(f'<path d="M1000 12 C995 -20 960 -55 900 -80 C820 -112 720 -130 600 -132 C470 -130 360 -110 260 -75 C190 -50 130 -30 82 -18" fill="none" stroke="{rim}" stroke-width="6" opacity=".9"/>')
    gc = gill_col or line
    for i in range(5):
        gx = 770 - i * 24
        g.append(f'<path d="M{gx} {-28 + i * 3} q12 44 -2 {92 - i * 6}" fill="none" stroke="{gc}" stroke-width="5" stroke-linecap="round" opacity=".8"/>'
                 f'<path d="M{gx + 5} {-24 + i * 3} q11 40 -1 {84 - i * 6}" fill="none" stroke="{rim}" stroke-width="2" opacity=".45"/>')
    if mouth == 'open':
        up = ((822, 86), (870, 78), (920, 64), (958, 48))
        lo = ((822, 86), (862, 112), (902, 150), (934, 188))
        g.append(f'<path d="M822 86 C870 78 920 64 958 48" fill="none" stroke="#c96a6a" stroke-width="9" opacity=".9"/>')
        g.append(f'<path d="M822 86 C862 112 902 150 934 188" fill="none" stroke="#c96a6a" stroke-width="9" opacity=".9"/>')
        g.append(teeth_on(up, 7, 30, -1))
        g.append(teeth_on(lo, 6, 28, 1, t0=.12))
    else:
        mc = ((964, 46), (930, 62), (880, 76), (826, 82))
        g.append(f'<path d="M964 46 C930 62 880 76 826 82" fill="none" stroke="{line}" stroke-width="5" stroke-linecap="round"/>')
        g.append(teeth_on(mc, 7, 13, 1, t0=.06, t1=.8, lw=1.6))
    g.append(f'<path d="M968 -2 q10 -4 16 2" fill="none" stroke="{line}" stroke-width="4" stroke-linecap="round"/>')
    g.append(f'<circle cx="902" cy="-20" r="12" fill="#04080b" stroke="#2b3a44" stroke-width="3"/>')
    if eye_glint:
        g.append('<circle cx="906" cy="-24" r="3.6" fill="#fff"/>')
    for fin in (PECT, PELV, ANAL):
        g.append(f'<path d="{fin}" fill="url(#{idp}g)" stroke="{line}" stroke-width="5" stroke-linejoin="round"/>')
    g.append(f'<path d="M722 86 C694 172 622 258 542 318" fill="none" stroke="{rim}" stroke-width="4" opacity=".6"/>')
    g.append('</g>')
    return d, ''.join(g)


def shark_pt(x, y, s, rot, flip, lx, ly):
    """global position of local shark point (lx, ly) for shark(x, y, s, rot, flip)."""
    px, py = (lx - 500) * (-s if flip else s), ly * s
    c, si = math.cos(math.radians(rot)), math.sin(math.radians(rot))
    return x + px * c - py * si, y + px * si + py * c


def silhouette(x, y, s, rot=0, flip=False, col='#000', op=1, extra=''):
    """flat shark silhouette (closed mouth) in shark() coordinates."""
    sx = -s if flip else s
    return (f'<g transform="translate({x} {y}) rotate({rot}) scale({sx} {s}) translate(-500 0)" fill="{col}" opacity="{op}" {extra}>'
            f'<path d="{CAUDAL}"/><path d="{DORSAL}"/><path d="{DORSAL2}"/><path d="{BODY_CLOSED}"/><path d="{PECT}"/><path d="{PELV}"/><path d="{ANAL}"/></g>')


def silhouette_d():
    return [CAUDAL, DORSAL, DORSAL2, BODY_CLOSED, PECT, PELV, ANAL]


def tooth(x, y, s, rot=0, idp='th', fossil=True):
    """single big Megalodon tooth (crown + root), point down. ~ 200 units tall * s; (x, y) = centre."""
    crown = '#5b6470' if fossil else '#f4efe0'; crown2 = '#2e353e' if fossil else '#cfc6ae'
    d = (f'<linearGradient id="{idp}c" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{crown2}"/><stop offset=".45" stop-color="{crown}"/>'
         f'<stop offset=".6" stop-color="#9aa6b2"/><stop offset="1" stop-color="{crown2}"/></linearGradient>')
    d += (f'<linearGradient id="{idp}r" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#4a3424"/><stop offset=".5" stop-color="#8a6446"/>'
          f'<stop offset="1" stop-color="#3a281a"/></linearGradient>')
    ser = ''.join(f'M{-98 + i * 6.8:.1f} {-28 + i * 10.6:.1f} l-5 2' for i in range(14)) + ''.join(f'M{98 - i * 6.8:.1f} {-28 + i * 10.6:.1f} l5 2' for i in range(14))
    g = f'<g transform="translate({x} {y}) rotate({rot}) scale({s})" stroke="#120d0a" stroke-linejoin="round">'
    g += '<path d="M-104 -36 C-112 -58 -98 -76 -70 -74 Q-30 -70 0 -58 Q30 -70 70 -74 C98 -76 112 -58 104 -36 Q60 -46 0 -42 Q-60 -46 -104 -36Z" fill="url(#%sr)" stroke-width="5"/>' % idp
    g += '<path d="M-60 -86 q30 8 50 -2 M20 -88 q22 8 40 0" fill="none" stroke="#c99a6a" stroke-width="3" opacity=".5"/>'
    g += '<path d="M-104 -36 Q-60 -46 0 -42 Q60 -46 104 -36 Q54 40 6 116 Q0 122 -6 116 Q-54 40 -104 -36Z" fill="url(#%sc)" stroke-width="5"/>' % idp
    g += '<path d="M-60 -34 Q-30 20 -4 92" fill="none" stroke="#e6f0f8" stroke-width="6" opacity=".55" stroke-linecap="round"/>'
    g += f'<path d="{ser}" fill="none" stroke="#120d0a" stroke-width="2" opacity=".7"/>'
    g += '<path d="M-98 -36 Q0 -46 98 -36 L0 2 Z" fill="#1e1610" opacity=".7"/>'
    g += '</g>'
    return d, g


def whale(x, y, s, rot=0, flip=False, col='#3d566a', belly='#c9d6de', line='#0b161d', rim='#d8f6ff', glow=None):
    """baleen whale (humpback-like) side view facing right; (x, y) centre, ~1000 units long * s."""
    sx = -s if flip else s
    body = ('M960 10 C950 -30 900 -60 800 -72 C640 -90 460 -80 300 -55 C200 -40 120 -22 60 -8 L60 10 C140 30 230 52 340 66 '
            'C500 86 700 92 840 72 C910 60 955 44 960 10Z')
    fl = 'M60 -8 C20 -40 -30 -70 -80 -78 C-60 -50 -30 -20 -10 0 C-30 20 -60 50 -80 78 C-30 70 20 40 60 10Z'
    pec = 'M700 70 C650 150 560 230 470 270 C500 220 560 140 610 80Z'
    dors = 'M380 -62 C360 -90 340 -100 312 -104 C326 -86 326 -70 320 -56Z'
    g = f'<g transform="translate({x} {y}) rotate({rot}) scale({sx} {s}) translate(-480 0)" stroke="{line}" stroke-width="5" stroke-linejoin="round">'
    if glow:
        g += f'<g filter="url(#b24)" opacity=".6" fill="{glow}" stroke="{glow}" stroke-width="30"><path d="{body}"/><path d="{fl}"/><path d="{pec}"/></g>'
    g += f'<path d="{fl}" fill="{col}"/><path d="{dors}" fill="{col}"/><path d="{body}" fill="{col}"/>'
    g += f'<path d="M940 30 C900 60 800 84 640 88 C500 88 380 72 300 60 C420 50 600 54 760 46 C860 40 920 30 940 30Z" fill="{belly}" stroke="none" opacity=".9"/>'
    g += ''.join(f'<path d="M{900 - k * 40} {44 + k * 3} C{820 - k * 40} {60 + k * 3} {720 - k * 40} {66 + k * 2} {640 - k * 40} {68 + k}" fill="none" stroke="{line}" stroke-width="2.5" opacity=".45"/>' for k in range(5))
    g += f'<path d="M960 10 C900 22 840 28 760 28" fill="none" stroke-width="4"/>'
    g += f'<circle cx="790" cy="8" r="7" fill="#05080a" stroke="none"/><circle cx="792" cy="6" r="2" fill="#fff" stroke="none"/>'
    g += ''.join(f'<circle cx="{c}" cy="{r}" r="5" fill="{line}" stroke="none" opacity=".5"/>' for c, r in ((900, -40), (930, -20), (870, -55)))
    g += f'<path d="M960 10 C950 -30 900 -60 800 -72 C640 -90 460 -80 300 -55" fill="none" stroke="{rim}" stroke-width="5" opacity=".8"/>'
    g += f'<path d="{pec}" fill="{col}"/><path d="M700 70 C650 150 560 230 470 270" fill="none" stroke="{rim}" stroke-width="4" opacity=".6"/>'
    g += '</g>'
    return g
