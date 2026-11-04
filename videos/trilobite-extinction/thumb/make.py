# Thumbnails A-C for trilobite-extinction (guideline 16-6 / 16-8, brief tools/briefs/thumb_art.md). Run: python3 videos/trilobite-extinction/thumb/make.py
# A  RULED FOR 270 MILLION YEARS  homage: Planet of the Apes (1968) ending: a colossal trilobite fossil slab half-buried in a beach at dusk,
#                         surf at its foot, cliffs behind, the tiny frog (hat blown off) staring up. Script S02/S05/S57: "ruled it for roughly
#                         two hundred and seventy million years"; S01/S64 stone with a pattern on a beach.
# B  EYES OF STONE        intuitive: a giant phacopid head seen from the side, its tower eye made of glowing calcite lenses; a diving frog
#                         is reflected in the lenses. Script S15-S17 ("Eyes of Stone", calcite lenses, phacopids).
# C  THE GREAT DYING      intuitive: the last trilobite curled into its ball on a poisoned seafloor, volcanic red glow above, gas bubbles,
#                         dissolving shells; the diving frog shines a lamp on it. Script S42-S43, S47-S50, S53 ("curling into its defensive ball").
import os, sys, math, random
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', '..', 'tools'))
from thumb_lib import page, svg, lin, rad, spark

INK = '#1d2b1c'; GREEN = '#6aa55a'; DARKG = '#4d8a4a'; BELLY = '#9cc98a'
FILTERS = ''.join(f'<filter id="b{n}" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="{n}"/></filter>' for n in (2, 3, 6, 12, 24, 50))


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


# ---------------- trilobite (dorsal view), phacopid-like: 3 lobes, head shield + eyes, 11 thorax segments, tail shield ----------------
def hexlenses(cx, cy, rx, ry, r, rot=0):
    """lens centres in a hex grid inside an ellipse"""
    out = []; dy = r * 1.75; dx = r * 2.02; j = 0; y = -ry
    while y <= ry:
        off = (j % 2) * dx / 2; x = -rx + off
        while x <= rx:
            if (x / rx) ** 2 + (y / ry) ** 2 <= .78:
                a = math.radians(rot); out.append((cx + x * math.cos(a) - y * math.sin(a), cy + x * math.sin(a) + y * math.cos(a)))
            x += dx
        y += dy; j += 1
    return out


def trilo_dorsal(u, N=11):
    """parts in local px (head toward -y, length ~u). Returns dict name -> list of path d."""
    R = {k: [] for k in ('ceph', 'border', 'glab', 'occ', 'eye', 'lens', 'axial', 'pleura', 'pfur', 'pyg', 'pygax', 'pygrib', 'furrow')}
    # head shield with genal spines
    R['ceph'].append(f'M{-.44*u:.1f} {-.15*u:.1f} C{-.50*u:.1f} {-.38*u:.1f} {-.30*u:.1f} {-.53*u:.1f} 0 {-.53*u:.1f} '
                     f'C{.30*u:.1f} {-.53*u:.1f} {.50*u:.1f} {-.38*u:.1f} {.44*u:.1f} {-.15*u:.1f} '
                     f'L{.50*u:.1f} {.06*u:.1f} L{.40*u:.1f} {-.14*u:.1f} L{-.40*u:.1f} {-.14*u:.1f} L{-.50*u:.1f} {.06*u:.1f} Z')
    R['border'].append(f'M{-.41*u:.1f} {-.17*u:.1f} C{-.45*u:.1f} {-.37*u:.1f} {-.28*u:.1f} {-.495*u:.1f} 0 {-.495*u:.1f} '
                       f'C{.28*u:.1f} {-.495*u:.1f} {.45*u:.1f} {-.37*u:.1f} {.41*u:.1f} {-.17*u:.1f}')
    # glabella widening forward + occipital ring
    R['glab'].append(f'M{-.085*u:.1f} {-.195*u:.1f} C{-.10*u:.1f} {-.27*u:.1f} {-.185*u:.1f} {-.35*u:.1f} {-.17*u:.1f} {-.42*u:.1f} '
                     f'C{-.15*u:.1f} {-.50*u:.1f} {.15*u:.1f} {-.50*u:.1f} {.17*u:.1f} {-.42*u:.1f} '
                     f'C{.185*u:.1f} {-.35*u:.1f} {.10*u:.1f} {-.27*u:.1f} {.085*u:.1f} {-.195*u:.1f} Z')
    R['occ'].append(f'M{-.10*u:.1f} {-.185*u:.1f} Q0 {-.20*u:.1f} {.10*u:.1f} {-.185*u:.1f} L{.11*u:.1f} {-.145*u:.1f} Q0 {-.135*u:.1f} {-.11*u:.1f} {-.145*u:.1f} Z')
    for sgn in (-1, 1):
        R['furrow'].append(f'M{sgn*.12*u:.1f} {-.27*u:.1f} q{-sgn*.03*u:.1f} {.01*u:.1f} {-sgn*.04*u:.1f} {.035*u:.1f}')
        R['furrow'].append(f'M{sgn*.14*u:.1f} {-.33*u:.1f} q{-sgn*.03*u:.1f} {.005*u:.1f} {-sgn*.045*u:.1f} {.03*u:.1f}')
        # facial suture
        R['furrow'].append(f'M{sgn*.14*u:.1f} {-.47*u:.1f} Q{sgn*.17*u:.1f} {-.40*u:.1f} {sgn*.22*u:.1f} {-.38*u:.1f} M{sgn*.27*u:.1f} {-.22*u:.1f} Q{sgn*.33*u:.1f} {-.18*u:.1f} {sgn*.40*u:.1f} {-.16*u:.1f}')
        ex, ey = sgn * .245 * u, -.30 * u
        R['eye'].append((ex, ey, .062 * u, .088 * u, sgn * 18))
    # thorax
    y0, y1 = -.14 * u, .27 * u; h = (y1 - y0) / N
    for i in range(N):
        t = i / (N - 1); y = y0 + i * h
        a = (.115 - .04 * t) * u; xe = (.43 - .09 * t ** 1.6) * u
        R['axial'].append(f'M{-a:.1f} {y + h*.12:.1f} Q0 {y - h*.25:.1f} {a:.1f} {y + h*.12:.1f} L{a*.96:.1f} {y + h*.86:.1f} Q0 {y + h*.55:.1f} {-a*.96:.1f} {y + h*.86:.1f} Z')
        for s in (-1, 1):
            g0 = a + .012 * u
            R['pleura'].append(f'M{s*g0:.1f} {y + h*.08:.1f} L{s*xe:.1f} {y + h*.22:.1f} Q{s*(xe + .025*u):.1f} {y + h*.5:.1f} {s*(xe + .01*u):.1f} {y + h*1.35:.1f} '
                               f'Q{s*(xe - .02*u):.1f} {y + h*.95:.1f} {s*(xe - .04*u):.1f} {y + h*.9:.1f} L{s*g0:.1f} {y + h*.86:.1f} Z')
            R['pfur'].append(f'M{s*(g0 + .01*u):.1f} {y + h*.42:.1f} L{s*(xe - .03*u):.1f} {y + h*.62:.1f}')
    # tail shield
    a = .07 * u
    R['pyg'].append(f'M{-.37*u:.1f} {y1:.1f} C{-.38*u:.1f} {.40*u:.1f} {-.16*u:.1f} {.47*u:.1f} 0 {.47*u:.1f} C{.16*u:.1f} {.47*u:.1f} {.38*u:.1f} {.40*u:.1f} {.37*u:.1f} {y1:.1f} Z')
    R['pygax'].append(f'M{-a:.1f} {y1 + .005*u:.1f} Q0 {y1 - .01*u:.1f} {a:.1f} {y1 + .005*u:.1f} L{.025*u:.1f} {.42*u:.1f} Q0 {.435*u:.1f} {-.025*u:.1f} {.42*u:.1f} Z')
    for k in range(1, 6):
        yy = y1 + k * .026 * u; ww = a - k * .009 * u
        R['pygrib'].append(f'M{-ww:.1f} {yy:.1f} Q0 {yy - .008*u:.1f} {ww:.1f} {yy:.1f}')
    for k in range(5):
        yy = y1 + .015 * u + k * .03 * u
        for s in (-1, 1):
            R['pygrib'].append(f'M{s*(a + .01*u - k*.008*u):.1f} {yy:.1f} Q{s*(.2*u):.1f} {yy + .02*u + k*.012*u:.1f} {s*(.29*u - k*.05*u):.1f} {yy + .04*u + k*.022*u:.1f}')
    return R


def tri_paint(R, col, line, lw, eyecol='#3a2a1a', lensfill='#6a5236', glint=None, lensr=None):
    """paint a dorsal trilobite (dict from trilo_dorsal) with fills (col: dict part -> fill)"""
    o = ''
    st = f'stroke="{line}" stroke-width="{lw}" stroke-linejoin="round"'
    o += ''.join(f'<path d="{d}" fill="{col["ceph"]}" {st}/>' for d in R['ceph'])
    o += ''.join(f'<path d="{d}" fill="none" stroke="{line}" stroke-width="{lw*.8}" opacity=".7"/>' for d in R['border'])
    o += ''.join(f'<path d="{d}" fill="{col["pyg"]}" {st}/>' for d in R['pyg'])
    o += ''.join(f'<path d="{d}" fill="{col["pleura"]}" {st}/>' for d in R['pleura'])
    o += ''.join(f'<path d="{d}" fill="{col["axial"]}" {st}/>' for d in R['axial'])
    o += ''.join(f'<path d="{d}" fill="{col["axial"]}" {st}/>' for d in R['pygax'])
    o += ''.join(f'<path d="{d}" fill="none" stroke="{line}" stroke-width="{lw*.7}" stroke-linecap="round" opacity=".75"/>' for d in R['pygrib'] + R['pfur'] + R['furrow'])
    o += ''.join(f'<path d="{d}" fill="{col["glab"]}" {st}/>' for d in R['glab'])
    o += ''.join(f'<path d="{d}" fill="{col["axial"]}" {st}/>' for d in R['occ'])
    for ex, ey, rx, ry, rot in R['eye']:
        o += f'<ellipse cx="{ex:.1f}" cy="{ey:.1f}" rx="{rx:.1f}" ry="{ry:.1f}" transform="rotate({rot} {ex:.1f} {ey:.1f})" fill="{eyecol}" {st}/>'
        lr = lensr or rx * .14
        for lx, ly in hexlenses(ex, ey, rx, ry, lr, rot):
            o += f'<circle cx="{lx:.1f}" cy="{ly:.1f}" r="{lr*.82:.1f}" fill="{lensfill}"/>'
            if glint:
                o += f'<circle cx="{lx - lr*.3:.1f}" cy="{ly - lr*.3:.1f}" r="{lr*.28:.1f}" fill="{glint}"/>'
    return o


def tri_height(R):
    """grey height map of the same trilobite (white = high) for the relief lighting filter"""
    o = ''.join(f'<path d="{d}" fill="#7a7a7a"/>' for d in R['ceph'] + R['pyg'])
    o += ''.join(f'<path d="{d}" fill="#8a8a8a"/>' for d in R['pleura'])
    o += ''.join(f'<path d="{d}" fill="#d0d0d0"/>' for d in R['axial'] + R['pygax'] + R['occ'])
    o += ''.join(f'<path d="{d}" fill="none" stroke="#3a3a3a" stroke-width="9"/>' for d in R['border'] + R['pfur'] + R['pygrib'] + R['furrow'])
    o += ''.join(f'<path d="{d}" fill="#ffffff"/>' for d in R['glab'])
    for ex, ey, rx, ry, rot in R['eye']:
        o += f'<ellipse cx="{ex:.1f}" cy="{ey:.1f}" rx="{rx:.1f}" ry="{ry:.1f}" transform="rotate({rot} {ex:.1f} {ey:.1f})" fill="#f0f0f0"/>'
    return o


def relief_filter(id, az, el=38, scale=9, blur=5, grain=.0, freq=.035):
    g = ''
    if grain:
        g = (f'<feTurbulence type="fractalNoise" baseFrequency="{freq}" numOctaves="4" seed="7" result="n"/>'
             f'<feColorMatrix in="n" type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  1 0 0 0 0" result="na"/>'
             f'<feComposite in="h0" in2="na" operator="arithmetic" k1="0" k2="1" k3="{grain}" k4="{-grain/2}" result="h1"/>'
             f'<feComposite in="h1" in2="SourceAlpha" operator="in" result="h"/>')
    else:
        g = '<feComposite in="h0" in2="SourceAlpha" operator="in" result="h"/>'
    return (f'<filter id="{id}" x="-5%" y="-5%" width="110%" height="110%" color-interpolation-filters="sRGB">'
            f'<feColorMatrix in="SourceGraphic" type="luminanceToAlpha" result="a"/>'
            f'<feGaussianBlur in="a" stdDeviation="{blur}" result="h0"/>' + g +
            f'<feDiffuseLighting in="h" surfaceScale="{scale}" diffuseConstant="1.3" lighting-color="#fff" result="d"><feDistantLight azimuth="{az}" elevation="{el}"/></feDiffuseLighting>'
            f'<feComposite in="d" in2="SourceAlpha" operator="in"/></filter>'
            f'<filter id="{id}s" x="-5%" y="-5%" width="110%" height="110%" color-interpolation-filters="sRGB">'
            f'<feColorMatrix in="SourceGraphic" type="luminanceToAlpha" result="a"/>'
            f'<feGaussianBlur in="a" stdDeviation="{blur}" result="h"/>'
            f'<feSpecularLighting in="h" surfaceScale="{scale}" specularConstant=".8" specularExponent="20" lighting-color="#ffd9a8" result="s"><feDistantLight azimuth="{az}" elevation="{el}"/></feSpecularLighting>'
            f'<feComposite in="s" in2="SourceAlpha" operator="in"/></filter>')


def jag(cx, cy, pts, rnd, amp):
    """irregular closed polygon from a coarse outline, with small random breaks"""
    out = []
    for k in range(len(pts)):
        (x0, y0), (x1, y1) = pts[k], pts[(k + 1) % len(pts)]
        n = max(2, int(math.hypot(x1 - x0, y1 - y0) / 40))
        for j in range(n):
            t = j / n
            out.append((cx + x0 + (x1 - x0) * t + rnd.uniform(-amp, amp), cy + y0 + (y1 - y0) * t + rnd.uniform(-amp, amp)))
    return 'M' + ' L'.join(f'{x:.1f} {y:.1f}' for x, y in out) + 'Z'


# ================= A: Planet of the Apes ending -> colossal trilobite fossil on the beach =================
def make_A():
    rnd = random.Random(5)
    u = 740; ang = -24; CX, CY = 1390, 585
    d = FILTERS + relief_filter('rlfA', az=230, grain=.06, freq=.08)
    d += lin('skyA', [(0, '#1f3550'), (.38, '#5b6f86'), (.62, '#d79a66'), (.72, '#f6c785'), (1, '#f6c785')])
    d += lin('seaA', [(0, '#7c8798'), (.3, '#4d5f75'), (1, '#27384c')])
    d += lin('sandA', [(0, '#c49a6a'), (.25, '#a77d55'), (1, '#4d3727')])
    d += lin('wetA', [(0, '#8f8a86'), (1, '#6d5c4c')])
    d += lin('cliffA', [(0, '#5a4a48'), (1, '#2a2026')], x2=1, y2=.3)
    d += lin('slabA', [(0, '#b08c66'), (.5, '#8f6c4e'), (1, '#5a4232')], x2=.6, y2=1)
    d += lin('fosA', [(0, '#6e4428'), (1, '#3a2214')], x2=.4, y2=1)
    d += rad('sunA', 430, 660, 700, [(0, '#fff2c8', .95), (.12, '#ffd38a', .7), (.4, '#f0a060', .25), (1, '#f0a060', 0)])
    d += rad('vigA', 960, 540, 1200, [(0, '#000', 0), (.65, '#000', 0), (1, '#0a0606', .5)])
    b = '<rect width="1920" height="1080" fill="url(#skyA)"/>'
    b += '<rect width="1920" height="1080" fill="url(#sunA)"/>'
    # long dusk clouds
    for y, x0, x1, op in ((210, -50, 900, .25), (300, 200, 1300, .3), (420, -40, 760, .35), (520, 600, 1700, .3), (585, 100, 520, .4)):
        b += f'<path d="M{x0} {y} Q{(x0 + x1) / 2} {y - 22} {x1} {y} Q{(x0 + x1) / 2} {y + 14} {x0} {y}Z" fill="#f4b67e" opacity="{op}"/>'
        b += f'<path d="M{x0 + 40} {y + 6} Q{(x0 + x1) / 2} {y + 18} {x1 - 40} {y + 6}" fill="none" stroke="#6b5a6e" stroke-width="5" opacity="{op}"/>'
    b += '<circle cx="430" cy="664" r="46" fill="#fff6dc"/><circle cx="430" cy="664" r="90" fill="#ffe1a0" opacity=".35" filter="url(#b12)"/>'
    # far headland + cliffs (right) behind the fossil
    b += '<path d="M0 668 L120 650 L260 660 L340 676 L0 680Z" fill="#6e6070" opacity=".75"/>'
    b += ('<path d="M1480 690 L1500 520 L1560 430 L1600 300 L1680 250 L1760 180 L1860 160 L1920 150 L1920 760 L1480 760Z" fill="url(#cliffA)"/>')
    for k in range(9):
        x = 1520 + k * 46
        b += f'<path d="M{x} {700 - k * 30} l{rnd.randint(-10, 10)} {-rnd.randint(80, 200)}" stroke="#7a6566" stroke-width="5" opacity=".55"/>'
    b += '<path d="M1600 300 L1680 250 L1760 180 L1860 160 L1920 150" fill="none" stroke="#f3b67c" stroke-width="6" opacity=".7"/>'
    # sea with glitter path from the sun
    b += '<rect x="0" y="672" width="1920" height="140" fill="url(#seaA)"/>'
    for k in range(70):
        y = rnd.uniform(678, 800); w = rnd.uniform(20, 90) * (1 + (y - 670) / 120)
        x = 430 + rnd.gauss(0, 60 + (y - 670) * 1.6)
        b += f'<rect x="{x - w / 2:.0f}" y="{y:.0f}" width="{w:.0f}" height="{rnd.choice([2, 3, 4])}" rx="2" fill="#ffe1a8" opacity="{rnd.uniform(.35, .85):.2f}"/>'
    for k in range(5):
        y = 700 + k * 22
        b += f'<path d="M0 {y} Q480 {y - 8} 960 {y} T1920 {y}" fill="none" stroke="#c4cbd2" stroke-width="2.5" opacity=".35"/>'
    # beach: wet sand band + surf
    b += '<path d="M0 800 Q500 784 960 800 Q1400 812 1920 796 L1920 1080 L0 1080Z" fill="url(#sandA)"/>'
    b += '<path d="M0 800 Q500 784 960 800 Q1400 812 1920 796 L1920 850 Q1300 868 900 846 Q420 826 0 848Z" fill="url(#wetA)" opacity=".85"/>'
    b += '<path d="M0 836 Q300 816 640 834 Q860 846 1060 828" fill="none" stroke="#ffe7c0" stroke-width="5" opacity=".55"/>'
    b += '<path d="M0 800 Q300 790 600 806 Q800 815 1000 802 Q1300 790 1500 808" fill="none" stroke="#f4f0e8" stroke-width="7" opacity=".85"/>'
    b += '<path d="M40 812 Q260 800 520 818" fill="none" stroke="#fff" stroke-width="3" opacity=".6"/>'
    # back glow behind the fossil
    b += f'<ellipse cx="{CX - 40}" cy="{CY}" rx="520" ry="560" fill="#ffd9a0" opacity=".28" filter="url(#b50)"/>'
    # ---- the fossil slab ----
    R = trilo_dorsal(u)
    slab = [(-.5 * u, -.6 * u), (-.15 * u, -.68 * u), (.28 * u, -.64 * u), (.58 * u, -.46 * u), (.62 * u, .1 * u), (.56 * u, .66 * u), (-.58 * u, .7 * u), (-.62 * u, -.05 * u)]
    sp = jag(0, 0, slab, rnd, 14)
    g = f'<g transform="translate({CX} {CY}) rotate({ang})">'
    g += f'<path d="{sp}" transform="translate(-34 26)" fill="#3e2c22"/>'          # slab thickness (shadow side)
    g += f'<path d="{sp}" transform="translate(-16 12)" fill="#6d5440"/>'
    g += f'<path d="{sp}" fill="url(#slabA)"/>'
    for _ in range(14):    # pits and lichen speckle
        x, y = rnd.uniform(-.6 * u, .6 * u), rnd.uniform(-.65 * u, .6 * u)
        g += f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{rnd.uniform(6, 22):.0f}" ry="{rnd.uniform(4, 12):.0f}" fill="#6b5844" opacity=".35"/>'
    col = {'ceph': 'url(#fosA)', 'pyg': '#5a3820', 'pleura': '#5e3b22', 'axial': '#7a4f2e', 'glab': '#875a34'}
    g += tri_paint(R, col, '#24140c', 3, eyecol='#3c2616', lensfill='#8a6440', glint='#ffd9a0')
    # relief lighting overlay (height map of slab + trilobite)
    hm = f'<path d="{sp}" fill="#202020"/>' + tri_height(R)
    g += f'<g filter="url(#rlfA)" style="mix-blend-mode:overlay">{hm}</g>'
    g += f'<g filter="url(#rlfAs)" style="mix-blend-mode:screen" opacity=".9">{hm}</g>'
    # cracks across the slab
    g += f'<path d="M{-.66 * u:.0f} {.18 * u:.0f} l90 -14 l60 22 l80 -6" fill="none" stroke="#2e2018" stroke-width="5" opacity=".7"/>'
    g += f'<path d="M{.62 * u:.0f} {-.30 * u:.0f} l-70 30 l-30 60" fill="none" stroke="#2e2018" stroke-width="4" opacity=".6"/>'
    # rim light on the sun-facing (left) edge
    g += f'<path d="{sp}" fill="none" stroke="#ffd59a" stroke-width="5" opacity=".55" stroke-dasharray="900 2600" stroke-dashoffset="-2350"/>'
    g += '</g>'
    b += g
    # sand mound burying the lower part, surf foam around it
    b += ('<path d="M840 1080 Q880 900 1040 860 Q1200 822 1380 850 Q1580 800 1760 860 Q1880 900 1920 960 L1920 1080Z" fill="url(#sandA)"/>')
    b += '<path d="M940 880 Q1060 840 1220 838 Q1400 852 1560 820 Q1700 820 1820 880" fill="none" stroke="#e7c391" stroke-width="7" opacity=".7"/>'
    b += '<path d="M1000 870 Q1200 850 1400 862 Q1600 840 1800 900 L1800 930 Q1500 880 1000 900Z" fill="#2a1a10" opacity=".35" filter="url(#b12)"/>'
    b += '<path d="M880 915 Q1010 872 1120 880 Q1200 888 1270 868" fill="none" stroke="#fffaf0" stroke-width="6" opacity=".8"/>'
    b += '<path d="M1500 870 Q1640 846 1800 905" fill="none" stroke="#fffaf0" stroke-width="5" opacity=".7"/>'
    for _ in range(26):   # foam dots
        x = rnd.uniform(900, 1800); y = 880 + rnd.uniform(-20, 30) + abs(x - 1350) * .03
        b += f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{rnd.uniform(4, 12):.0f}" ry="{rnd.uniform(2, 5):.0f}" fill="#fff" opacity="{rnd.uniform(.4, .8):.2f}"/>'
    # sand grain
    for _ in range(120):
        x = rnd.uniform(0, 1920); y = rnd.uniform(810, 1080)
        b += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{rnd.choice([1, 1.4, 2])}" fill="{rnd.choice(["#e8c79a", "#5a4030"])}" opacity="{rnd.uniform(.2, .5):.2f}"/>'
    # small shells + frog footprints
    for x, y, s in ((300, 930, 1), (560, 1010, .8), (1060, 1000, .9)):
        b += (f'<g transform="translate({x} {y}) scale({s})"><path d="M-18 6 Q-16 -16 0 -18 Q16 -16 18 6 Z" fill="#efe0c8" stroke="#5a4030" stroke-width="3"/>'
              f'<path d="M0 -16 L0 5 M-9 -12 L-6 5 M9 -12 L6 5" stroke="#b49a7a" stroke-width="2.5"/></g>')
    for k in range(6):
        x = 120 + k * 92; y = 1040 - k * 14 + (k % 2) * 18
        b += f'<ellipse cx="{x}" cy="{y}" rx="16" ry="7" fill="#6a4c34" opacity=".55"/>'
    # the frog (Taylor on the beach), hat blown off, staring up at the fossil
    b += '<ellipse cx="680" cy="1010" rx="120" ry="18" fill="#2a1a10" opacity=".35"/>'
    b += '<circle cx="660" cy="880" r="130" fill="#ffe2a8" opacity=".25" filter="url(#b24)"/>'
    b += frog(680, 1010, 2.45, rot=4, look=(9, -7), mouth='O', hat=True,
              armL='M-34 -22 q-26 -10 -34 -40', armR='M38 -22 q24 -14 30 -44')
    b += spark(1190, 160, 22) + spark(1560, 610, 18) + spark(1010, 560, 14, '#fff6d6', .7)
    b += '<rect width="1920" height="1080" fill="url(#vigA)"/>'
    lines = [('RULED FOR', 112, 'w'), ('270 MILLION', 150, 'y'), ('YEARS', 132, 'w')]
    return page('#1f3550', svg(d, b), lines, outline='#120c10', top=44)



def cub(p0, p1, p2, p3, n=24):
    out = []
    for k in range(n + 1):
        t = k / n; u_ = 1 - t
        out.append((u_ ** 3 * p0[0] + 3 * u_ * u_ * t * p1[0] + 3 * u_ * t * t * p2[0] + t ** 3 * p3[0],
                    u_ ** 3 * p0[1] + 3 * u_ * u_ * t * p1[1] + 3 * u_ * t * t * p2[1] + t ** 3 * p3[1]))
    return out


def poly(pts, close=True):
    return 'M' + ' L'.join(f'{x:.1f} {y:.1f}' for x, y in pts) + ('Z' if close else '')


def inside(pt, pts):
    x, y = pt; c = False; n = len(pts)
    for i in range(n):
        x0, y0 = pts[i]; x1, y1 = pts[(i + 1) % n]
        if (y0 > y) != (y1 > y) and x < (x1 - x0) * (y - y0) / (y1 - y0) + x0:
            c = not c
    return c


def mini_trilo(x, y, s, rot, col, op):
    """small far-away trilobite silhouette (dorsal) for depth"""
    R = trilo_dorsal(100)
    o = f'<g transform="translate({x} {y}) rotate({rot}) scale({s / 100:.3f})" opacity="{op}">'
    o += ''.join(f'<path d="{d}" fill="{col}"/>' for d in R['ceph'] + R['pyg'] + R['pleura'] + R['axial'])
    return o + '</g>'


def crinoid(x, y, h, col, sway, rnd):
    """sea lily silhouette (stalk + crown)"""
    tx, ty = x + sway, y - h
    o = f'<path d="M{x} {y} Q{x + sway * .2} {y - h * .5} {tx} {ty}" fill="none" stroke="{col}" stroke-width="7" stroke-linecap="round"/>'
    for k in range(7):
        a = math.radians(-90 + (k - 3) * 14)
        L = h * .22
        o += f'<path d="M{tx} {ty} Q{tx + math.cos(a) * L * .5 + (k - 3) * 4} {ty + math.sin(a) * L * .6} {tx + math.cos(a) * L * .6 + (k - 3) * 10} {ty + math.sin(a) * L}" fill="none" stroke="{col}" stroke-width="6" stroke-linecap="round"/>'
    return o


# ================= B: EYES OF STONE (intuitive): a living trilobite on the seafloor; the frog's magnifying glass shows its calcite-lens eye =================
def eye_lenses(eye, r, cxm, half, rnd=None, frogs=True):
    """hex-packed glowing calcite lenses inside the polygon eye (vertical files), foreshortened toward the ends"""
    xs = [p[0] for p in eye]; x = min(xs) + r * 1.2; k = 0; o = ''
    while x < max(xs) - r * .8:
        ys = [py for px, py in eye if abs(px - x) < r * .7]
        if ys:
            top, bot = min(ys), max(ys)
            y = top + r * 1.25 + (k % 2) * r * 1.02
            while y < bot - r * 1.05:
                sc = 1 - .38 * min(1, abs((x - cxm) / half)) ** 2
                o += (f'<g transform="translate({x:.1f} {y:.1f}) scale({r * sc:.2f} {r:.2f})">'
                      f'<circle r="1.12" fill="#140904"/><circle r="1" fill="url(#lensB)"/>'
                      f'<path d="M-.78 -.25 A.82 .82 0 0 1 .25 -.78" fill="none" stroke="#c8f6ff" stroke-width=".16" stroke-linecap="round" opacity=".9"/>')
                if frogs:
                    o += '<circle cx="-.36" cy=".38" r=".2" fill="#4f9a4a" opacity=".9"/><circle cx="-.43" cy=".25" r=".07" fill="#fff"/><circle cx="-.29" cy=".25" r=".07" fill="#fff"/>'
                o += '<circle cx="-.36" cy="-.4" r=".13" fill="#fff" opacity=".95"/></g>'
                y += r * 2.08
        x += r * 1.78; k += 1
    return o


def make_B():
    rnd = random.Random(21)
    u = 1040; th = -125; CX, CY, SQ = 1400, 620, .56
    d = FILTERS + relief_filter('rlfB', az=225 - th, el=40, scale=11, blur=6)
    d += lin('seaB', [(0, '#0d4a5c'), (.5, '#0a2f40'), (1, '#04131c')])
    d += lin('mudB', [(0, '#24332f'), (1, '#070c0e')])
    d += lin('cephB', [(0, '#8a4222'), (1, '#4a1c0c')])
    d += lin('scleraB', [(0, '#5a3a20'), (1, '#24150b')])
    d += ('<radialGradient id="lensB" cx=".5" cy=".5" r=".5" fx=".64" fy=".7"><stop offset="0" stop-color="#fffbe6"/><stop offset=".25" stop-color="#ffe7a6"/>'
          '<stop offset=".6" stop-color="#e8a84e"/><stop offset=".88" stop-color="#9a5a22"/><stop offset="1" stop-color="#4a2a10"/></radialGradient>')
    d += rad('shaftB', 300, -100, 1300, [(0, '#bff6ff', .35), (.5, '#7ad4e6', .08), (1, '#7ad4e6', 0)])
    d += rad('keyB', 1100, 420, 800, [(0, '#ffe7b0', .35), (1, '#ffe7b0', 0)])
    d += rad('vigB', 960, 540, 1150, [(0, '#000', 0), (.6, '#000', 0), (1, '#000', .55)])
    b = '<rect width="1920" height="1080" fill="url(#seaB)"/><rect width="1920" height="1080" fill="url(#shaftB)"/>'
    for x0, w, op in ((120, 140, .10), (420, 90, .08), (760, 170, .08), (1500, 120, .05)):
        b += f'<path d="M{x0} -20 L{x0 + w} -20 L{x0 + w + 420} 1080 L{x0 + 300} 1080Z" fill="#c8f4ff" opacity="{op}" filter="url(#b12)"/>'
    # seafloor with depth: far ridge, crinoids, small trilobites, near mud
    b += '<path d="M0 560 Q400 530 800 552 Q1300 580 1920 540 L1920 1080 L0 1080Z" fill="#123038" opacity=".9"/>'
    for x, h, sw in ((90, 300, 30), (230, 220, -20), (1700, 280, -30), (1840, 200, 20), (620, 200, 18)):
        b += crinoid(x, 570, h, '#185060', sw, rnd)
    for x, y, s, r_ in ((360, 610, 60, -70), (1600, 600, 50, 40), (980, 585, 40, 100)):
        b += mini_trilo(x, y, s, r_, '#1e4652', .9)
    b += '<path d="M0 640 Q600 610 1100 640 Q1500 660 1920 630 L1920 1080 L0 1080Z" fill="url(#mudB)"/>'
    for _ in range(60):
        x, y = rnd.uniform(0, 1920), rnd.uniform(660, 1070)
        b += f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{rnd.uniform(6, 22):.0f}" ry="{rnd.uniform(3, 8):.0f}" fill="#3a4c46" opacity="{rnd.uniform(.3, .7):.2f}"/>'
    # Cruziana-like furrow trail behind the trilobite
    b += '<path d="M1900 760 Q1800 740 1700 700" fill="none" stroke="#0a1416" stroke-width="40" opacity=".5" stroke-linecap="round"/>'
    b += '<rect width="1920" height="1080" fill="url(#keyB)"/>'
    # ---- the living trilobite, lying on the floor (dorsal view tilted away) ----
    R = trilo_dorsal(u)
    tf = f'translate({CX} {CY}) scale(1 {SQ}) rotate({th})'
    def W(px, py):
        a_ = math.radians(th); x_ = px * math.cos(a_) - py * math.sin(a_); y_ = px * math.sin(a_) + py * math.cos(a_)
        return CX + x_, CY + y_ * SQ
    b += f'<ellipse cx="{CX + 20}" cy="{CY + 70}" rx="{u * .56:.0f}" ry="{u * .22:.0f}" fill="#000" opacity=".5" filter="url(#b24)"/>'
    g = f'<g transform="{tf}">'
    col = {'ceph': 'url(#cephB)', 'pyg': '#5a2612', 'pleura': '#622a14', 'axial': '#8a3e1e', 'glab': '#9a4a24'}
    g += tri_paint(R, col, '#1e0c04', 5, eyecol='#3c2010', lensfill='#f2b860', glint='#fff4d0', lensr=u * .0085)
    hm = tri_height(R)
    g += f'<g filter="url(#rlfB)" style="mix-blend-mode:overlay" opacity=".75">{hm}</g>'
    g += f'<g filter="url(#rlfBs)" style="mix-blend-mode:screen" opacity=".5">{hm}</g>'
    # pale spots pattern on the shell
    for _ in range(80):
        px, py = rnd.uniform(-.4 * u, .4 * u), rnd.uniform(-.5 * u, .45 * u)
        g += f'<circle cx="{px:.0f}" cy="{py:.0f}" r="{rnd.uniform(3, 7):.1f}" fill="#f0c890" opacity=".22"/>'
    g += '</g>'
    b += g
    # antennae sweeping forward from under the head
    hx, hy = W(0, -.53 * u)
    for side, (c1, c2, e) in ((1, ((-90, 20), (-170, 60), (-190, 150))), (-1, ((-40, 70), (-90, 150), (-60, 200)))):
        pts = cub((hx + 10, hy + 6 * side), (hx + c1[0], hy + c1[1]), (hx + c2[0], hy + c2[1]), (hx + e[0], hy + e[1]), 26)
        for k in range(len(pts) - 1):
            w = 15 - k * .4
            b += f'<line x1="{pts[k][0]:.1f}" y1="{pts[k][1]:.1f}" x2="{pts[k + 1][0]:.1f}" y2="{pts[k + 1][1]:.1f}" stroke="#1e0c04" stroke-width="{w + 6:.1f}" stroke-linecap="round"/>'
        for k in range(len(pts) - 1):
            w = 15 - k * .4
            b += f'<line x1="{pts[k][0]:.1f}" y1="{pts[k][1]:.1f}" x2="{pts[k + 1][0]:.1f}" y2="{pts[k + 1][1]:.1f}" stroke="{"#c8703c" if k % 2 else "#8a4224"}" stroke-width="{w:.1f}"/>'
    # raised crystal eyes standing up from the head (glow)
    eyes = [W(ex, ey) for ex, ey, *_ in R['eye']]
    for ex, ey in eyes:
        b += f'<ellipse cx="{ex:.0f}" cy="{ey - 10:.0f}" rx="70" ry="44" fill="#ffd27a" opacity=".55" filter="url(#b12)"/>'
    # ---- magnifying glass over the near eye, showing the eye up close ----
    nx, ny = max(eyes, key=lambda p: p[1])
    MX, MY, MR = 975, 560, 168
    b += f'<line x1="{nx:.0f}" y1="{ny:.0f}" x2="{MX:.0f}" y2="{MY:.0f}" stroke="#fff3c8" stroke-width="3" opacity=".0"/>'
    d += f'<clipPath id="magB"><circle cx="{MX}" cy="{MY}" r="{MR}"/></clipPath>'
    zoom = f'<g clip-path="url(#magB)">'
    zoom += f'<circle cx="{MX}" cy="{MY}" r="{MR}" fill="#8a4224"/>'
    zoom += f'<circle cx="{MX - 60}" cy="{MY - 90}" r="{MR}" fill="#c8703c" opacity=".6" filter="url(#b24)"/>'
    for _ in range(40):
        x, y = rnd.uniform(MX - MR, MX + MR), rnd.uniform(MY - MR, MY - 40)
        rr = rnd.uniform(5, 11)
        zoom += f'<circle cx="{x + 2:.0f}" cy="{y + 3:.0f}" r="{rr:.1f}" fill="#3a1a0a" opacity=".5"/><circle cx="{x:.0f}" cy="{y:.0f}" r="{rr:.1f}" fill="#d07c46"/><circle cx="{x - rr * .3:.1f}" cy="{y - rr * .3:.1f}" r="{rr * .35:.1f}" fill="#ffe0b0" opacity=".8"/>'
    eye = cub((MX - 150, MY - 26), (MX - 86, MY - 104), (MX + 104, MY - 112), (MX + 160, MY - 44)) + cub((MX + 160, MY - 44), (MX + 186, MY + 60), (MX + 86, MY + 130), (MX - 8, MY + 130))[1:] + cub((MX - 8, MY + 130), (MX - 120, MY + 130), (MX - 172, MY + 52), (MX - 150, MY - 26))[1:]
    zoom += f'<path d="{poly(eye)}" transform="translate(0 22)" fill="#1a0a04"/>'
    zoom += f'<path d="{poly(eye)}" fill="#ffcf7a" opacity=".7" filter="url(#b12)"/>'
    zoom += f'<path d="{poly(eye)}" fill="url(#scleraB)" stroke="#120804" stroke-width="6"/>'
    zoom += eye_lenses(eye, 16.5, MX, 175)
    zoom += f'<path d="M{MX - 165} {MY - 34} Q{MX - 86} {MY - 130} {MX + 104} {MY - 130} Q{MX + 165} {MY - 121} {MX + 178} {MY - 52}" fill="none" stroke="#1e0c04" stroke-width="34" stroke-linecap="round"/>'
    zoom += f'<path d="M{MX - 165} {MY - 34} Q{MX - 86} {MY - 130} {MX + 104} {MY - 130} Q{MX + 165} {MY - 121} {MX + 178} {MY - 52}" fill="none" stroke="#c8703c" stroke-width="22" stroke-linecap="round"/>'
    zoom += f'<path d="M{MX - 148} {MY - 54} Q{MX - 78} {MY - 136} {MX + 95} {MY - 137}" fill="none" stroke="#ffe0a8" stroke-width="6" stroke-linecap="round" opacity=".8"/>'
    zoom += rad('glassB', MX, MY, MR, [(0, '#000', 0), (.8, '#000', 0), (.97, '#bff4ff', .25), (1, '#fff', .45)]).replace('radialGradient id', 'radialGradient id', 1)
    zoom += f'<circle cx="{MX}" cy="{MY}" r="{MR}" fill="url(#glassB)"/>'
    zoom += '</g>'
    # dotted cone from the glass to the real eye (shows what is magnified)
    b += f'<path d="M{MX + MR * .7:.0f} {MY + MR * .7:.0f} L{nx:.0f} {ny:.0f} L{MX + MR * .98:.0f} {MY + MR * .2:.0f}Z" fill="#fff1c4" opacity=".14"/>'
    b += f'<circle cx="{MX}" cy="{MY}" r="{MR + 30}" fill="#ffe2a0" opacity=".25" filter="url(#b24)"/>'
    b += zoom
    b += f'<path d="M{MX - MR * .72:.0f} {MY - MR * .45:.0f} A{MR * .85:.0f} {MR * .85:.0f} 0 0 1 {MX - MR * .2:.0f} {MY - MR * .82:.0f}" fill="none" stroke="#fff" stroke-width="12" stroke-linecap="round" opacity=".55"/>'
    b += f'<circle cx="{MX}" cy="{MY}" r="{MR}" fill="none" stroke="#1d1408" stroke-width="40"/>'
    b += f'<circle cx="{MX}" cy="{MY}" r="{MR}" fill="none" stroke="#c99a3a" stroke-width="28"/>'
    b += f'<circle cx="{MX}" cy="{MY}" r="{MR + 6}" fill="none" stroke="#ffe7a0" stroke-width="5" opacity=".8" stroke-dasharray="300 1200" stroke-dashoffset="-560"/>'
    # handle down to the frog's hand
    ha = math.radians(128); h0 = (MX + math.cos(ha) * (MR + 14), MY + math.sin(ha) * (MR + 14)); h1 = (MX + math.cos(ha) * (MR + 190), MY + math.sin(ha) * (MR + 190))
    b += f'<line x1="{h0[0]:.0f}" y1="{h0[1]:.0f}" x2="{h1[0]:.0f}" y2="{h1[1]:.0f}" stroke="#1d1408" stroke-width="44" stroke-linecap="round"/>'
    b += f'<line x1="{h0[0]:.0f}" y1="{h0[1]:.0f}" x2="{h1[0]:.0f}" y2="{h1[1]:.0f}" stroke="#7a3a1e" stroke-width="32" stroke-linecap="round"/>'
    b += f'<line x1="{h0[0] - 8:.0f}" y1="{h0[1] - 2:.0f}" x2="{h1[0] - 8:.0f}" y2="{h1[1] - 2:.0f}" stroke="#c46a3a" stroke-width="8" stroke-linecap="round"/>'
    b += spark(MX - 120, MY - 150, 30, '#ffffff', .95) + spark(1640, 380, 18, '#fff6d6') + spark(1180, 470, 16, '#e8fbff')
    for _ in range(140):
        b += f'<circle cx="{rnd.uniform(0, 1920):.0f}" cy="{rnd.uniform(0, 1000):.0f}" r="{rnd.choice([1.4, 2, 2.8])}" fill="#dffaff" opacity="{rnd.uniform(.12, .5):.2f}"/>'
    # the diving frog holding the magnifier
    fx_, fy_, fs = 520, 1030, 2.45
    hand = ((h1[0] - fx_) / fs, (h1[1] - fy_) / fs)
    armR = f'M38 -22 q{(hand[0] - 38) * .6:.1f} {(hand[1] + 22) * .2:.1f} {hand[0] - 38:.1f} {hand[1] + 22:.1f}'
    b += '<circle cx="520" cy="920" r="150" fill="#9ff0ff" opacity=".18" filter="url(#b24)"/>'
    b += frog(fx_, fy_, fs, rot=0, look=(10, -8), mouth='O', helmet=True, shadow=True, armR=armR, armL='M-34 -22 q-18 6 -22 24')
    for bx, by, rr in ((570, 760, 10), (590, 712, 13), (576, 660, 8)):
        b += f'<circle cx="{bx}" cy="{by}" r="{rr}" fill="none" stroke="#e8fbff" stroke-width="3" opacity=".7"/>'
    b += '<rect width="1920" height="1080" fill="url(#vigB)"/>'
    lines = [('EYES', 158, 'w'), ('OF', 104, 'w'), ('STONE', 200, 'y')]
    return page('#0a2f40', svg(d, b), lines, outline='#04121a', top=36)


# ================= C: THE GREAT DYING (intuitive): the last trilobite rolled into its ball on a poisoned seafloor =================
def make_C():
    rnd = random.Random(31)
    CX, CY, W, RV = 1260, 600, 385, 350
    d = FILTERS
    d += lin('seaC', [(0, '#5a3a2a'), (.3, '#3c3a2a'), (.65, '#1e2420'), (1, '#0a0c0c')])
    d += rad('fireC', 1700, -60, 1100, [(0, '#ff7a2a', .85), (.25, '#e2481c', .45), (.6, '#8a2a14', .15), (1, '#8a2a14', 0)])
    d += lin('mudC', [(0, '#2a2a22'), (1, '#0a0a08')])
    d += lin('bandC', [(0, '#b0683a'), (1, '#6a3a1e')])
    d += lin('axC', [(0, '#d08a50'), (1, '#8a4e28')])
    d += rad('shadeC', CX - 130, CY - 170, 580, [(0, '#fff2d8', .22), (.3, '#fff2d8', .05), (.6, '#000', .0), (1, '#000', .62)])
    d += rad('lampC', 640, 870, 900, [(0, '#e8fff4', .45), (.4, '#bfffe0', .12), (1, '#bfffe0', 0)])
    d += ('<radialGradient id="lensC" cx=".5" cy=".5" r=".5" fx=".4" fy=".38"><stop offset="0" stop-color="#fff6d8"/><stop offset=".35" stop-color="#ffcf70"/>'
          '<stop offset=".8" stop-color="#a85a20"/><stop offset="1" stop-color="#3a1a08"/></radialGradient>')
    d += lin('glabC', [(0, '#e09a5c'), (.5, '#b06a38'), (1, '#6a3a1c')])
    d += rad('vigC', 960, 540, 1150, [(0, '#000', 0), (.6, '#000', 0), (1, '#000', .6)])
    d += f'<clipPath id="ballC"><ellipse cx="{CX}" cy="{CY}" rx="{W}" ry="{RV}"/></clipPath>'
    b = '<rect width="1920" height="1080" fill="url(#seaC)"/><rect width="1920" height="1080" fill="url(#fireC)"/>'
    # red light shafts from the burning surface
    for x0, w, op in ((1200, 120, .12), (1450, 160, .14), (1750, 120, .12), (950, 80, .07)):
        b += f'<path d="M{x0} -20 L{x0 + w} -20 L{x0 + w - 260} 1080 L{x0 - 360} 1080Z" fill="#ff8a4a" opacity="{op}" filter="url(#b12)"/>'
    # murky clouds of silt / poison
    for _ in range(18):
        b += f'<ellipse cx="{rnd.uniform(0, 1920):.0f}" cy="{rnd.uniform(200, 800):.0f}" rx="{rnd.uniform(120, 320):.0f}" ry="{rnd.uniform(40, 90):.0f}" fill="#7a8a4a" opacity="{rnd.uniform(.05, .12):.2f}" filter="url(#b24)"/>'
    # far seafloor: dead reef silhouettes
    b += '<path d="M0 700 Q300 680 600 700 Q1000 720 1400 690 Q1700 670 1920 690 L1920 1080 L0 1080Z" fill="#1c1c16"/>'
    for x, h in ((80, 140), (180, 90), (520, 120), (1700, 150), (1820, 100)):
        b += f'<path d="M{x} 705 l0 {-h} m0 {h * .4} l{-h * .3} {-h * .4} m{h * .3} {h * .55} l{h * .3} {-h * .35}" stroke="#2c2a22" stroke-width="9" stroke-linecap="round" fill="none"/>'
    b += '<path d="M0 820 Q500 780 960 810 Q1400 840 1920 800 L1920 1080 L0 1080Z" fill="url(#mudC)"/>'
    # cracked toxic mud with sulphur patches
    for _ in range(14):
        x, y = rnd.uniform(0, 1920), rnd.uniform(860, 1060)
        b += f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{rnd.uniform(40, 120):.0f}" ry="{rnd.uniform(8, 18):.0f}" fill="#c8c43a" opacity="{rnd.uniform(.08, .2):.2f}"/>'
    for _ in range(26):
        x, y = rnd.uniform(0, 1920), rnd.uniform(850, 1070)
        b += f'<path d="M{x:.0f} {y:.0f} l{rnd.uniform(-60, 60):.0f} {rnd.uniform(-8, 8):.0f} l{rnd.uniform(-40, 40):.0f} {rnd.uniform(-10, 10):.0f}" stroke="#050504" stroke-width="3" fill="none" opacity=".6"/>'
    # dissolving shells (brachiopods with holes) on the floor
    for x, y, sc, rot in ((760, 1000, 1.1, -10), (1030, 1040, .8, 20), (1720, 930, .9, -20), (1500, 1010, .7, 8), (300, 890, .7, 14)):
        b += (f'<g transform="translate({x} {y}) rotate({rot}) scale({sc})"><path d="M-40 10 Q-38 -30 0 -36 Q38 -30 40 10 Q0 22 -40 10Z" fill="#9a9070" stroke="#1a1a12" stroke-width="4"/>'
              f'<path d="M0 -34 L0 14 M-18 -28 L-12 14 M18 -28 L12 14 M-32 -14 L-26 12 M32 -14 L26 12" stroke="#5a5440" stroke-width="3"/>'
              f'<ellipse cx="-10" cy="-6" rx="9" ry="6" fill="#1a1a12"/><ellipse cx="16" cy="2" rx="6" ry="4" fill="#1a1a12"/></g>')
    # lamp beam from the frog
    b += '<rect width="1920" height="1080" fill="url(#lampC)"/>'
    d += '<linearGradient id="beamC" x1="790" y1="820" x2="1100" y2="600" gradientUnits="userSpaceOnUse"><stop offset="0" stop-color="#f4fff0" stop-opacity=".55"/><stop offset="1" stop-color="#f4fff0" stop-opacity=".0"/></linearGradient>'
    b += f'<path d="M780 830 L{CX - W * .7:.0f} {CY - RV * .75:.0f} L{CX - W * .2:.0f} {CY + RV * .9:.0f} Z" fill="url(#beamC)" filter="url(#b6)"/>'
    # shadow + red halo behind the ball
    b += f'<ellipse cx="{CX + 30}" cy="{CY + RV + 10}" rx="{W * 1.05:.0f}" ry="50" fill="#000" opacity=".7" filter="url(#b12)"/>'
    b += f'<ellipse cx="{CX + 40}" cy="{CY - 30}" rx="{W + 80}" ry="{RV + 80}" fill="#ff7a3a" opacity=".22" filter="url(#b50)"/>'
    # ---- the enrolled trilobite, seen head-on: thorax bands arching over the top, head shield below ----
    def lat(phi, s):     # point on the ball: phi = angle up from the front around the left-right axis, s = -1..1 across
        return CX + W * s, CY - RV * math.sin(math.radians(min(90, phi - 26))) * math.sqrt(max(0, 1 - s * s))
    ball = f'<g clip-path="url(#ballC)">'
    ball += f'<ellipse cx="{CX}" cy="{CY}" rx="{W}" ry="{RV}" fill="#4a2814"/>'
    PH = [16 + k * 9.2 for k in range(12)]
    SS = [i / 40 - 1 for i in range(81)]
    for k in range(len(PH) - 1):
        lo, hi = PH[k], PH[k + 1]
        up = [lat(hi, s_) for s_ in SS]; dn = [lat(lo, s_) for s_ in SS][::-1]
        ball += f'<path d="{poly(up + dn)}" fill="url(#bandC)" stroke="#1a0c04" stroke-width="5" stroke-linejoin="round"/>'
        # axial ring: the raised middle third of each band
        ax = [p for p in SS if abs(p) <= .3]
        upa = [lat(hi, s_) for s_ in ax]; dna = [lat(lo, s_) for s_ in ax][::-1]
        ball += f'<path d="{poly(upa + dna)}" fill="url(#axC)" stroke="#1a0c04" stroke-width="4"/>'
        # front-edge highlight of each segment (lit rim) + pleural furrow
        mid = [lat((lo + hi) / 2, s_) for s_ in SS if abs(s_) > .33]
        left = [p for p in mid if p[0] < CX]; right = [p for p in mid if p[0] > CX]
        for part in (left, right):
            ball += f'<polyline points="{P(part)}" fill="none" stroke="#2a1408" stroke-width="4" opacity=".7"/>'
        hl = [lat(lo + 1.8, s_) for s_ in SS[6:-6]]
        ball += f'<polyline points="{P(hl)}" fill="none" stroke="#ffc890" stroke-width="5" opacity=".55"/>'
        # small tubercles on the axial rings
        for s_ in (-.15, 0, .15):
            x_, y_ = lat((lo + hi) / 2, s_)
            ball += f'<circle cx="{x_:.0f}" cy="{y_:.0f}" r="{max(3, 9 * math.cos(math.radians((lo + hi) / 2 - 26))):.1f}" fill="#f0b47a" opacity=".7"/>'
    # axial furrows
    for s_ in (-.31, .31):
        pts = [lat(p, s_) for p in range(16, 117, 2)]
        ball += f'<polyline points="{P(pts)}" fill="none" stroke="#1a0c04" stroke-width="7"/>'
    # head shield (lower front of the ball)
    top = [lat(16, s_) for s_ in SS]
    ball += f'<path d="{poly(top + [(CX + W, CY + RV + 20), (CX - W, CY + RV + 20)])}" fill="#7a4222" stroke="#1a0c04" stroke-width="7"/>'
    ball += f'<path d="M{CX - W * .99:.0f} {CY + RV * .3:.0f} Q{CX} {CY + RV * 1.62:.0f} {CX + W * .99:.0f} {CY + RV * .3:.0f}" fill="none" stroke="#1a0c04" stroke-width="36"/>'
    ball += f'<path d="M{CX - W * .99:.0f} {CY + RV * .3:.0f} Q{CX} {CY + RV * 1.62:.0f} {CX + W * .99:.0f} {CY + RV * .3:.0f}" fill="none" stroke="#b06a38" stroke-width="24"/>'
    ball += f'<path d="M{CX - W * .9:.0f} {CY + RV * .4:.0f} Q{CX - W * .5:.0f} {CY + RV * .98:.0f} {CX:.0f} {CY + RV * .93:.0f}" fill="none" stroke="#ffd2a0" stroke-width="5" opacity=".6"/>'
    # occipital ring + glabella (inflated, widening downward = forward)
    occ = [lat(14, s_) for s_ in SS if abs(s_) <= .32]
    ball += f'<polyline points="{P(occ)}" fill="none" stroke="#1a0c04" stroke-width="10"/>'
    gl = (f'M{CX - W * .19:.0f} {CY + RV * .2:.0f} C{CX - W * .24:.0f} {CY + RV * .34:.0f} {CX - W * .4:.0f} {CY + RV * .46:.0f} {CX - W * .36:.0f} {CY + RV * .64:.0f} '
          f'C{CX - W * .3:.0f} {CY + RV * .84:.0f} {CX + W * .3:.0f} {CY + RV * .84:.0f} {CX + W * .36:.0f} {CY + RV * .64:.0f} '
          f'C{CX + W * .4:.0f} {CY + RV * .46:.0f} {CX + W * .24:.0f} {CY + RV * .34:.0f} {CX + W * .19:.0f} {CY + RV * .2:.0f} Z')
    glpts = (cub((CX - W * .19, CY + RV * .2), (CX - W * .24, CY + RV * .34), (CX - W * .4, CY + RV * .46), (CX - W * .36, CY + RV * .64))
             + cub((CX - W * .36, CY + RV * .64), (CX - W * .3, CY + RV * .84), (CX + W * .3, CY + RV * .84), (CX + W * .36, CY + RV * .64))
             + cub((CX + W * .36, CY + RV * .64), (CX + W * .4, CY + RV * .46), (CX + W * .24, CY + RV * .34), (CX + W * .19, CY + RV * .2)))
    ball += f'<path d="{gl}" transform="translate(6 12)" fill="#1a0c04" opacity=".6"/>'
    ball += f'<path d="{gl}" fill="url(#glabC)" stroke="#1a0c04" stroke-width="7"/>'
    for _ in range(90):
        x_, y_ = CX + rnd.uniform(-.36, .36) * W, CY + rnd.uniform(.2, .85) * RV
        if inside((x_, y_), glpts) and inside((x_ + 10, y_ + 10), glpts) and inside((x_ - 10, y_ - 10), glpts):
            r_ = rnd.uniform(5, 11)
            ball += f'<circle cx="{x_ + 2:.0f}" cy="{y_ + 3:.0f}" r="{r_:.1f}" fill="#3a1a0a" opacity=".5"/><circle cx="{x_:.0f}" cy="{y_:.0f}" r="{r_:.1f}" fill="#d8945a"/><circle cx="{x_ - r_ * .3:.1f}" cy="{y_ - r_ * .3:.1f}" r="{r_ * .35:.1f}" fill="#ffe2b8" opacity=".8"/>'
    ball += f'<path d="M{CX - W * .27:.0f} {CY + RV * .42:.0f} Q{CX - W * .31:.0f} {CY + RV * .56:.0f} {CX - W * .24:.0f} {CY + RV * .7:.0f}" fill="none" stroke="#fff0d0" stroke-width="8" stroke-linecap="round" opacity=".55"/>'
    # global sphere shading, then the crystal eyes on top
    ball += f'<ellipse cx="{CX}" cy="{CY}" rx="{W}" ry="{RV}" fill="url(#shadeC)"/>'
    ball += f'<ellipse cx="{CX - W * .75:.0f}" cy="{CY + 40}" rx="{W * .5:.0f}" ry="{RV * .8:.0f}" fill="#e8fff0" opacity=".16" filter="url(#b50)" style="mix-blend-mode:screen"/>'
    ball += '</g>'
    b += ball
    for sgn in (-1, 1):
        ex, ey = CX + sgn * W * .58, CY + RV * .42
        eye = [(ex + math.cos(t) * W * .15, ey + math.sin(t) * RV * .16) for t in [i * math.pi / 30 for i in range(60)]]
        eye = [(x_ + (y_ - ey) * -.35 * sgn, y_) for x_, y_ in eye]
        b += f'<path d="{poly(eye)}" fill="#ffc870" opacity=".55" filter="url(#b12)"/>'
        b += f'<path d="{poly(eye)}" fill="#24140a" stroke="#120804" stroke-width="6"/>'
        b += eye_lenses(eye, 8.5, ex, W * .16, frogs=False).replace('url(#lensB)', 'url(#lensC)')
        # palpebral lobe over the eye
        b += f'<path d="M{ex - W * .17 + sgn * 30:.0f} {ey - RV * .13:.0f} Q{ex + sgn * 10:.0f} {ey - RV * .28:.0f} {ex + W * .17 + sgn * 30:.0f} {ey - RV * .13:.0f}" fill="none" stroke="#1a0c04" stroke-width="22" stroke-linecap="round"/>'
        b += f'<path d="M{ex - W * .17 + sgn * 30:.0f} {ey - RV * .13:.0f} Q{ex + sgn * 10:.0f} {ey - RV * .28:.0f} {ex + W * .17 + sgn * 30:.0f} {ey - RV * .13:.0f}" fill="none" stroke="#b06a38" stroke-width="13" stroke-linecap="round"/>'
    # rim lights: volcanic red from the top-right, lamp light from the left
    b += f'<path d="M{CX - W * .1:.0f} {CY - RV + 2:.0f} A{W} {RV} 0 0 1 {CX + W - 2:.0f} {CY + 40:.0f}" fill="none" stroke="#ff7a3a" stroke-width="10" opacity=".85"/>'
    b += f'<path d="M{CX - W * .1:.0f} {CY - RV + 2:.0f} A{W} {RV} 0 0 1 {CX + W - 2:.0f} {CY + 40:.0f}" fill="none" stroke="#ff9a5a" stroke-width="30" opacity=".35" filter="url(#b6)"/>'
    b += f'<path d="M{CX - W + 4:.0f} {CY + 60:.0f} A{W} {RV} 0 0 1 {CX - W * .5:.0f} {CY - RV * .86:.0f}" fill="none" stroke="#dfffee" stroke-width="7" opacity=".7"/>'
    b += f'<ellipse cx="{CX}" cy="{CY}" rx="{W}" ry="{RV}" fill="none" stroke="#120804" stroke-width="6"/>'
    # rising gas bubbles (CO2 / hydrogen sulphide) and falling ash
    for _ in range(46):
        x, y = rnd.uniform(700, 1900), rnd.uniform(60, 860)
        if ((x - CX) / W) ** 2 + ((y - CY) / RV) ** 2 < 1.1:
            continue
        r_ = rnd.uniform(4, 16)
        b += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r_:.1f}" fill="#d8e070" fill-opacity=".12" stroke="#e8f0a0" stroke-width="2.5" opacity=".7"/><circle cx="{x - r_ * .35:.1f}" cy="{y - r_ * .35:.1f}" r="{r_ * .25:.1f}" fill="#fff" opacity=".7"/>'
    for _ in range(160):
        b += f'<circle cx="{rnd.uniform(0, 1920):.0f}" cy="{rnd.uniform(0, 1000):.0f}" r="{rnd.choice([1.2, 1.8, 2.4])}" fill="{rnd.choice(["#ffb07a", "#d8d0a0"])}" opacity="{rnd.uniform(.15, .5):.2f}"/>'
    b += spark(CX - W * .6, CY - 40, 22, '#fff6d6') + spark(CX + W * .55, CY - RV * .7, 26, '#ffe2c0') + spark(CX + W * .62, CY + 10, 16, '#fff6d6')
    # the diving frog with a lamp (bottom-left)
    fx_, fy_, fs = 520, 1030, 2.45
    lamp = '<g transform="translate(78 -66) rotate(-30)"><rect x="-14" y="-12" width="34" height="24" rx="5" fill="#c9a24e" stroke-width="3"/><path d="M20 -16 L34 -20 L34 20 L20 16Z" fill="#f6f0c8" stroke-width="3"/></g>'
    b += f'<circle cx="{fx_ + 200}" cy="{fy_ - 220}" r="70" fill="#efffe8" opacity=".55" filter="url(#b24)"/>'
    b += frog(fx_, fy_, fs, look=(10, -6), mouth='O', helmet=True, shadow=True, armR='M38 -22 q24 -6 34 -40', armL='M-34 -22 q-18 6 -22 24', front=lamp)
    for bx, by, rr in ((560, 770, 10), (580, 720, 13), (566, 668, 8)):
        b += f'<circle cx="{bx}" cy="{by}" r="{rr}" fill="none" stroke="#e8fbff" stroke-width="3" opacity=".7"/>'
    b += '<rect width="1920" height="1080" fill="url(#vigC)"/>'
    lines = [('THE', 112, 'w'), ('GREAT', 182, 'w'), ('DYING', 182, 'y')]
    return page('#1e2420', svg(d, b), lines, outline='#0c0604', top=40)


if __name__ == '__main__':
    which = sys.argv[1:] or ['A', 'B', 'C']
    for n in which:
        fn = globals().get(f'make_{n}')
        if fn:
            open(os.path.join(HERE, f'{n}.html'), 'w').write(fn())
    print('ok')
