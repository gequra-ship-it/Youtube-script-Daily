# Thumbnails A-C for pluto-not-a-planet (guideline 16-6 / 16-8, brief tools/briefs/thumb_art.md). Run: python3 videos/pluto-not-a-planet/thumb/make.py
# A  SMALLER / THAN THE / MOON   homage: The Little Prince (Saint-Exupery's boy on asteroid B-612): the frog with a long golden scarf stands on
#                                a tiny Pluto (pale heart) beside the Moon drawn 1.46x larger (S17: 2,376 km vs 3,474 km).
# B  NINE / BECAME / EIGHT       intuitive: a classroom solar-system mobile at night, eight planets still hang from the brass hoop, the ninth
#                                string has snapped and little Pluto lies on the floor; frog in a school cap stares (S01 nine, S42 "trimmed down to eight").
# C  IT HAS / A HEART            homage: the NASA New Horizons 2015 Pluto portrait (public photo): big Pluto with the glowing pale heart
#                                (Tombaugh Regio / Sputnik Planitia, S46), the probe flies past, frog in a helmet rides its dish (S44).
import os, sys, math, random
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', '..', 'tools'))
from thumb_lib import page, svg, lin, rad, spark

INK = '#1d2b1c'; GREEN = '#6aa55a'; DARKG = '#4d8a4a'; BELLY = '#9cc98a'
FILTERS = ''.join(f'<filter id="b{n}" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="{n}"/></filter>'
                  for n in (1, 2, 3, 6, 12, 24, 50, 80))


def poly(pts):
    return 'M' + ' L'.join(f'{x:.1f},{y:.1f}' for x, y in pts) + 'Z'


def smooth(pts, closed=False, t=.5):
    """Catmull-Rom through pts -> cubic bezier path."""
    P = list(pts); n = len(P)
    d = f'M{P[0][0]:.1f},{P[0][1]:.1f}'
    rng = range(n) if closed else range(n - 1)
    for i in rng:
        p0 = P[(i - 1) % n] if (closed or i > 0) else P[i]
        p1 = P[i]; p2 = P[(i + 1) % n]
        p3 = P[(i + 2) % n] if (closed or i + 2 < n) else p2
        c1 = (p1[0] + (p2[0] - p0[0]) * t / 3, p1[1] + (p2[1] - p0[1]) * t / 3)
        c2 = (p2[0] - (p3[0] - p1[0]) * t / 3, p2[1] - (p3[1] - p1[1]) * t / 3)
        d += f' C{c1[0]:.1f},{c1[1]:.1f} {c2[0]:.1f},{c2[1]:.1f} {p2[0]:.1f},{p2[1]:.1f}'
    return d + ('Z' if closed else '')


def cr_sample(pts, n=10):
    """points along the Catmull-Rom curve through pts (n per segment)."""
    out = []
    for i in range(len(pts) - 1):
        p0 = pts[max(i - 1, 0)]; p1 = pts[i]; p2 = pts[i + 1]; p3 = pts[min(i + 2, len(pts) - 1)]
        for k in range(n):
            t = k / n; t2 = t * t; t3 = t2 * t
            out.append(tuple(.5 * (2 * p1[j] + (-p0[j] + p2[j]) * t + (2 * p0[j] - 5 * p1[j] + 4 * p2[j] - p3[j]) * t2 + (-p0[j] + 3 * p1[j] - 3 * p2[j] + p3[j]) * t3) for j in (0, 1)))
    out.append(pts[-1])
    return out


def bez(p0, p1, p2, p3, t):
    u = 1 - t
    return (u ** 3 * p0[0] + 3 * u * u * t * p1[0] + 3 * u * t * t * p2[0] + t ** 3 * p3[0],
            u ** 3 * p0[1] + 3 * u * u * t * p1[1] + 3 * u * t * t * p2[1] + t ** 3 * p3[1])


# ---------------- mascot frog (tools/assets/frog.svg body), posable ----------------
def limb(d, w=7.5, wi=3.4, col=GREEN):
    return f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="{w}"/><path d="{d}" fill="none" stroke="{col}" stroke-width="{wi}"/>'


def end_of(d):
    n = [float(v) for v in d.replace('M', ' ').replace('q', ' ').split()]
    return n[0] + n[-2], n[1] + n[-1]


def frog(x, y, s, rot=0, flip=False, look=(0, 0), mouth='O', armL=None, armR=None, legs=None, helmet=False,
         back='', front='', mid='', hat='', sleeve=None):
    sx = -s if flip else s
    g = [f'<g transform="translate({x} {y}) rotate({rot}) scale({sx} {s})" stroke="{INK}" stroke-linejoin="round" stroke-linecap="round">', back]
    if helmet:
        g.append('<rect x="-50" y="-58" width="20" height="42" rx="7" fill="#d9dde6" stroke-width="3"/><rect x="-46" y="-52" width="5" height="30" rx="2" fill="#fff" stroke="none" opacity=".7"/>')
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
    g.append('<path d="M-22 -88 q12 -9 24 -1 M10 -89 q12 -8 24 1" fill="none" stroke-width="3.4"/>')
    if mouth == 'O':
        g.append('<ellipse cx="6" cy="-38" rx="10" ry="12" fill="#7a2f33" stroke-width="3"/><ellipse cx="6" cy="-31" rx="6" ry="4" fill="#e07b7b" stroke="none"/>')
    else:
        g.append('<ellipse cx="6" cy="-41" rx="6" ry="7.5" fill="#7a2f33" stroke-width="3"/>')
    g.append('<ellipse cx="-18" cy="-48" rx="5" ry="3" fill="#e98a8a" stroke="none" opacity=".55"/><ellipse cx="30" cy="-48" rx="5" ry="3" fill="#e98a8a" stroke="none" opacity=".55"/>')
    g.append(hat)
    if helmet:
        g.append('<circle cx="6" cy="-56" r="47" fill="#cfeaff" fill-opacity=".13" stroke="#eef6ff" stroke-width="4.5"/>')
        g.append('<path d="M-28 -80 q12 -18 32 -21" fill="none" stroke="#fff" stroke-width="5" opacity=".8"/><path d="M44 -40 q6 -10 6 -22" fill="none" stroke="#fff" stroke-width="3" opacity=".5"/>')
        g.append('<ellipse cx="6" cy="-12" rx="42" ry="9" fill="#e6eaf2" stroke-width="3.2"/><path d="M-30 -14 q36 8 72 0" fill="none" stroke="#fff" stroke-width="2.2" opacity=".8"/>')
    g.append(mid)
    for a in (armL or 'M-34 -22 q-14 6 -16 22', armR or 'M38 -22 q14 6 16 22'):
        if sleeve:
            g.append(f'<path d="{a}" fill="none" stroke="{INK}" stroke-width="13"/><path d="{a}" fill="none" stroke="{sleeve}" stroke-width="8.5"/>')
        else:
            g.append(limb(a))
        ex_, ey_ = end_of(a)
        g.append(f'<circle cx="{ex_:.1f}" cy="{ey_:.1f}" r="5.6" fill="{GREEN}" stroke-width="3"/>')
    g.append(front); g.append('</g>')
    return ''.join(g)


def heart(cx, cy, s, rot=0, fill='#fbf1dc', op=1.0, extra=''):
    """Tombaugh Regio heart (point down). Left lobe = Sputnik Planitia (brighter, smooth)."""
    d = 'M0,62 C-34,40 -86,6 -80,-34 C-75,-66 -36,-74 -12,-46 C-4,-38 0,-30 2,-26 C10,-56 40,-80 72,-58 C98,-38 84,0 52,28 C34,44 14,54 0,62Z'
    left = 'M0,62 C-34,40 -86,6 -80,-34 C-75,-66 -36,-74 -12,-46 C-4,-38 0,-30 2,-26 C4,4 4,34 0,62Z'
    return (f'<g transform="translate({cx} {cy}) rotate({rot}) scale({s})" opacity="{op}">'
            f'<path d="{d}" fill="{fill}" opacity=".9"/>'
            f'<path d="{left}" fill="#fffaf0"/>{extra}</g>')


def pluto(cx, cy, r, uid, heart_at=(.32, .2), heart_s=None, rot=-8, light=(-.45, -.45), haze=True, detail=True):
    """Pluto globe: tan/cream surface, dark red-brown equatorial band (left), pale heart, terminator shade, blue haze rim."""
    rnd = random.Random(uid)
    lx, ly = light
    d = rad(f'pl{uid}', cx + lx * r * .6, cy + ly * r * .6, r * 1.5, [(0, '#f3dcc0', 1), (.45, '#d2a77f', 1), (1, '#6b4330', 1)])
    d += rad(f'ps{uid}', cx + lx * r * .9, cy + ly * r * .9, r * 2.05, [(.5, '#0b0710', 0), (.8, '#0b0710', .55), (1, '#0b0710', .92)])
    d += f'<clipPath id="pc{uid}"><circle cx="{cx}" cy="{cy}" r="{r}"/></clipPath>'
    o = ''
    if haze:
        o += f'<circle cx="{cx}" cy="{cy}" r="{r * 1.06:.0f}" fill="none" stroke="#7fb8ff" stroke-width="{r * .05:.0f}" opacity=".55" filter="url(#b12)"/>'
        o += f'<circle cx="{cx}" cy="{cy}" r="{r * 1.012:.1f}" fill="none" stroke="#b9dcff" stroke-width="{max(2, r * .012):.1f}" opacity=".8"/>'
    o += f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="url(#pl{uid})"/>'
    g = f'<g clip-path="url(#pc{uid})">'
    # dark reddish band (Cthulhu-like) on the left/equator
    g += f'<path d="{smooth([(cx - r * 1.1, cy + r * .05), (cx - r * .7, cy - r * .02), (cx - r * .35, cy + r * .12), (cx - r * .05, cy + r * .35), (cx + r * .05, cy + r * .6), (cx - r * .2, cy + r * .62), (cx - r * .6, cy + r * .45), (cx - r * 1.1, cy + r * .5)], closed=True)}" fill="#7a3a26" opacity=".75" filter="url(#b3)"/>'
    g += f'<path d="{smooth([(cx + r * .55, cy + r * .5), (cx + r * .9, cy + r * .42), (cx + r * 1.1, cy + r * .6), (cx + r * .8, cy + r * .75)], closed=True)}" fill="#8a4a2e" opacity=".55" filter="url(#b3)"/>'
    if detail:
        for _ in range(int(r / 5)):
            a = rnd.uniform(0, 2 * math.pi); q = r * math.sqrt(rnd.random()) * .95
            x = cx + q * math.cos(a); y = cy + q * math.sin(a); cr = rnd.uniform(r * .008, r * .03)
            g += f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{cr:.1f}" fill="#5a3426" opacity="{rnd.uniform(.12, .3):.2f}"/>'
            g += f'<circle cx="{x - cr * .3:.1f}" cy="{y - cr * .3:.1f}" r="{cr * .7:.1f}" fill="#fff1dc" opacity=".12"/>'
    hs = heart_s or r / 170
    hx, hy = cx + heart_at[0] * r, cy + heart_at[1] * r
    g += f'<ellipse cx="{hx}" cy="{hy}" rx="{90 * hs:.0f}" ry="{70 * hs:.0f}" fill="#fff6e6" opacity=".35" filter="url(#b24)"/>'
    g += heart(hx, hy, hs, rot)
    # polar light cap
    g += f'<ellipse cx="{cx - r * .1}" cy="{cy - r * .9}" rx="{r * .55}" ry="{r * .25}" fill="#f6e6d2" opacity=".35" filter="url(#b12)"/>'
    g += f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="url(#ps{uid})"/>'
    g += '</g>'
    return d, o + g


def moon(cx, cy, r, uid):
    rnd = random.Random(uid)
    d = rad(f'mo{uid}', cx - r * .35, cy - r * .35, r * 1.5, [(0, '#f4f4ef', 1), (.5, '#c9c8c2', 1), (1, '#55565e', 1)])
    d += rad(f'ms{uid}', cx - r * .6, cy - r * .55, r * 2.1, [(.52, '#05060c', 0), (.82, '#05060c', .55), (1, '#05060c', .9)])
    d += f'<clipPath id="mc{uid}"><circle cx="{cx}" cy="{cy}" r="{r}"/></clipPath>'
    o = f'<circle cx="{cx}" cy="{cy}" r="{r * 1.25:.0f}" fill="#dfe6ff" opacity=".22" filter="url(#b50)"/>'
    o += f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="url(#mo{uid})"/><g clip-path="url(#mc{uid})">'
    for mx, my, rx, ry, a in ((-.35, -.3, .32, .22, .55), (.05, -.42, .22, .16, .5), (-.05, .05, .28, .2, .45), (.35, -.05, .2, .26, .4), (-.45, .2, .18, .14, .4), (.15, .38, .26, .14, .35)):
        o += f'<ellipse cx="{cx + mx * r:.0f}" cy="{cy + my * r:.0f}" rx="{rx * r:.0f}" ry="{ry * r:.0f}" fill="#7d7f88" opacity="{a}" filter="url(#b6)"/>'
    for _ in range(40):
        a = rnd.uniform(0, 2 * math.pi); q = r * math.sqrt(rnd.random()) * .95
        x = cx + q * math.cos(a); y = cy + q * math.sin(a); cr = rnd.uniform(r * .012, r * .05)
        o += f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{cr:.1f}" fill="#6d6e76" opacity=".35"/><path d="M{x - cr:.1f} {y:.1f} a{cr:.1f} {cr:.1f} 0 0 1 {2 * cr:.1f} 0" fill="none" stroke="#fbfbf6" stroke-width="{max(1, cr * .25):.1f}" opacity=".45" transform="rotate(-40 {x:.1f} {y:.1f})"/>'
    # Tycho with rays
    tx, ty = cx + r * .1, cy + r * .62
    for k in range(14):
        a = k * 2 * math.pi / 14 + .2
        o += f'<path d="M{tx:.0f} {ty:.0f} L{tx + math.cos(a) * r * .5:.0f} {ty + math.sin(a) * r * .5:.0f}" stroke="#fff" stroke-width="3" opacity=".12"/>'
    o += f'<circle cx="{tx:.0f}" cy="{ty:.0f}" r="{r * .03:.0f}" fill="#fff" opacity=".7"/>'
    o += f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="url(#ms{uid})"/></g>'
    return d, o


def starfield(rnd, n, x0=0, x1=1920, y0=0, y1=1080, col='#eef3ff'):
    o = ''
    for _ in range(n):
        o += f'<circle cx="{rnd.uniform(x0, x1):.0f}" cy="{rnd.uniform(y0, y1):.0f}" r="{rnd.choice([1.2, 1.6, 2.2, 2.8])}" fill="{col}" opacity="{rnd.uniform(.25, .9):.2f}"/>'
    return o


# =========================== A: The Little Prince homage ===========================
def make_A():
    rnd = random.Random(11)
    d = FILTERS
    d += lin('skyA', [(0, '#0d1238'), (.55, '#1b2457'), (1, '#2b2550')])
    d += rad('glowA', 1060, 620, 520, [(0, '#ffd99a', .35), (.5, '#f2a96b', .12), (1, '#f2a96b', 0)])
    d += rad('vigA', 960, 540, 1150, [(.55, '#000', 0), (1, '#03030c', .6)])
    pd, po = pluto(1060, 735, 200, 'A', heart_at=(.18, .3), rot=-6, light=(-.5, -.5))
    md, mo = moon(1580, 520, 292, 'A')      # 3,474 / 2,376 = 1.46x Pluto
    d += pd + md
    b = '<rect width="1920" height="1080" fill="url(#skyA)"/>'
    b += starfield(rnd, 160)
    # milky storybook swirl
    b += f'<path d="{smooth([(-40, 980), (400, 760), (820, 690), (1300, 620), (1960, 380)])}" fill="none" stroke="#9fb3ff" stroke-width="160" opacity=".07" filter="url(#b50)"/>'
    for x, y, s in ((1240, 140, 22), (760, 610, 16), (1860, 860, 14), (1150, 330, 14), (620, 900, 18), (1420, 920, 12)):
        b += spark(x, y, s)
    b += '<rect width="1920" height="1080" fill="url(#glowA)"/>'
    b += mo
    b += po
    # the Little Prince frog: long golden scarf streaming in the wind, standing on top, looking up at the bigger Moon
    sc = (f'<path d="M-30 -24 C-60 -40 -96 -20 -130 -46 C-150 -60 -170 -44 -196 -62 C-176 -30 -150 -40 -126 -22 C-96 -2 -62 -24 -32 -10Z" fill="#f2d27a" stroke-width="3.2"/>'
          f'<path d="M-120 -38 C-140 -48 -158 -40 -176 -50" fill="none" stroke="#c99a3a" stroke-width="2.4"/>')
    scarf = (f'<path d="M-32 -26 q36 12 72 -2 l2 12 q-38 14 -76 2z" fill="#f2d27a" stroke-width="3.2"/>')
    coat = ('<path d="M-30 -6 q34 10 68 0 l4 8 q-38 12 -76 0z" fill="#3f6fb8" stroke-width="3" opacity=".95"/>')
    b += frog(1060, 538, 2.75, flip=True, look=(-3.2, -3.4), mouth='O', back=sc, mid=scarf,
              armL='M-34 -22 q-18 -8 -24 -30', armR='M38 -22 q16 8 18 26')
    b += '<rect width="1920" height="1080" fill="url(#vigA)"/>'
    return page('#0d1238', svg(d, b), [('SMALLER', 196, 'y'), ('THAN THE', 112, 'w'), ('MOON', 196, 'w')])


# =========================== B: intuitive: the classroom planet mobile, string snapped ===========================
def ball(cx, cy, r, c0, c1, c2, uid, bands=None, ring=False):
    d = rad(f'bl{uid}', cx - r * .4, cy - r * .45, r * 1.6, [(0, c0, 1), (.5, c1, 1), (1, c2, 1)])
    o = ''
    if ring:
        o += f'<ellipse cx="{cx}" cy="{cy}" rx="{r * 2.0:.0f}" ry="{r * .5:.0f}" fill="none" stroke="#3a2a1a" stroke-width="{r * .5 + 6:.0f}" transform="rotate(-12 {cx} {cy})" clip-path="url(#rt{uid})"/>'
        o += f'<ellipse cx="{cx}" cy="{cy}" rx="{r * 2.0:.0f}" ry="{r * .5:.0f}" fill="none" stroke="#e7cf98" stroke-width="{r * .5:.0f}" transform="rotate(-12 {cx} {cy})" clip-path="url(#rt{uid})"/>'
        d += f'<clipPath id="rt{uid}"><rect x="{cx - r * 3}" y="{cy - r * 3}" width="{r * 6}" height="{r * 3}" transform="rotate(-12 {cx} {cy})"/></clipPath>'
        d += f'<clipPath id="rb{uid}"><rect x="{cx - r * 3}" y="{cy}" width="{r * 6}" height="{r * 3}" transform="rotate(-12 {cx} {cy})"/></clipPath>'
    o += f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="url(#bl{uid})" stroke="#241a14" stroke-width="3"/>'
    if bands:
        d += f'<clipPath id="bc{uid}"><circle cx="{cx}" cy="{cy}" r="{r}"/></clipPath>'
        o += f'<g clip-path="url(#bc{uid})">' + ''.join(f'<rect x="{cx - r}" y="{cy + r * yy:.1f}" width="{2 * r}" height="{r * hh:.1f}" fill="{c}" opacity="{a}"/>' for yy, hh, c, a in bands) + '</g>'
    o += f'<ellipse cx="{cx - r * .35:.1f}" cy="{cy - r * .42:.1f}" rx="{r * .28:.1f}" ry="{r * .16:.1f}" fill="#fff" opacity=".55" transform="rotate(-30 {cx - r * .35:.1f} {cy - r * .42:.1f})"/>'
    if ring:
        o += f'<ellipse cx="{cx}" cy="{cy}" rx="{r * 2.0:.0f}" ry="{r * .5:.0f}" fill="none" stroke="#3a2a1a" stroke-width="{r * .5 + 6:.0f}" transform="rotate(-12 {cx} {cy})" clip-path="url(#rb{uid})"/>'
        o += f'<ellipse cx="{cx}" cy="{cy}" rx="{r * 2.0:.0f}" ry="{r * .5:.0f}" fill="none" stroke="#f3dfae" stroke-width="{r * .5:.0f}" transform="rotate(-12 {cx} {cy})" clip-path="url(#rb{uid})"/>'
        o += f'<ellipse cx="{cx}" cy="{cy}" rx="{r * 1.75:.0f}" ry="{r * .42:.0f}" fill="none" stroke="#b8975e" stroke-width="3" transform="rotate(-12 {cx} {cy})" clip-path="url(#rb{uid})"/>'
    return d, o


def make_B():
    rnd = random.Random(5)
    d = FILTERS
    d += lin('wallB', [(0, '#1a1633'), (.7, '#2a2148'), (1, '#3a2a4a')])
    d += lin('floorB', [(0, '#6b4127'), (.25, '#4a2b19'), (1, '#1c100a')])
    d += lin('coneB', [(0, '#ffe6b0'), (1, '#ffe6b0')], x2=0, y2=1)
    d += rad('poolB', 1280, 360, 760, [(0, '#ffd894', .55), (.45, '#e8a860', .18), (1, '#e8a860', 0)])
    d += rad('floorPool', 1230, 900, 520, [(0, '#ffcf80', .45), (1, '#ffcf80', 0)])
    d += rad('vigB', 1100, 520, 1150, [(.5, '#000', 0), (1, '#05030a', .7)])
    b = '<rect width="1920" height="1080" fill="url(#wallB)"/>'
    # glow-in-the-dark stars stuck on the wall (classroom), faint
    for _ in range(26):
        x, y = rnd.uniform(60, 1880), rnd.uniform(40, 760)
        b += spark(x, y, rnd.choice([7, 9, 11]), col='#d8ffb0', op=rnd.uniform(.12, .3))
    # Milky Way band across the wall (miya 2026-11-09: richer, more colourful galaxy background)
    gx = ''
    gx += '<g transform="rotate(-24 960 380)">'
    gx += '<ellipse cx="960" cy="380" rx="1250" ry="170" fill="#7a4bd6" opacity=".38" filter="url(#b24)"/>'
    gx += '<ellipse cx="760" cy="400" rx="900" ry="105" fill="#e056a8" opacity=".30" filter="url(#b24)"/>'
    gx += '<ellipse cx="1180" cy="350" rx="760" ry="90" fill="#35b8d8" opacity=".30" filter="url(#b24)"/>'
    gx += '<ellipse cx="960" cy="380" rx="1050" ry="46" fill="#ffe3a8" opacity=".30" filter="url(#b24)"/>'
    for _ in range(520):
        x = rnd.gauss(960, 430); y = rnd.gauss(380, 62)
        gx += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{rnd.choice([.9, 1.2, 1.6, 2.1])}" fill="{rnd.choice(["#ffffff", "#ffe9c4", "#cfe3ff", "#ffd0ec"])}" opacity="{rnd.uniform(.35, .95):.2f}"/>'
    gx += '</g>'
    for _ in range(140):
        gx += f'<circle cx="{rnd.uniform(0, 1920):.0f}" cy="{rnd.uniform(0, 800):.0f}" r="{rnd.choice([1, 1.4, 1.9, 2.6])}" fill="#fff" opacity="{rnd.uniform(.25, .85):.2f}"/>'
    for _ in range(9):
        gx += spark(rnd.uniform(80, 1840), rnd.uniform(40, 700), rnd.choice([12, 16, 20]), col='#fff6d8', op=rnd.uniform(.55, .9))
    b += gx
    b += '<rect width="1920" height="1080" fill="url(#poolB)"/>'
    # floor boards (horizon 76%)
    b += '<rect x="0" y="820" width="1920" height="260" fill="url(#floorB)"/>'
    b += '<rect x="0" y="816" width="1920" height="10" fill="#2a1a12"/><rect x="0" y="816" width="1920" height="3" fill="#8a5a38" opacity=".6"/>'
    for k in range(-12, 26):
        x0 = 1150 + k * 110
        b += f'<path d="M{1150 + k * 40} 826 L{x0 + (x0 - 1150) * .9:.0f} 1080" stroke="#1c0f08" stroke-width="3" opacity=".55"/>'
    for y in (870, 935, 1015):
        b += f'<path d="M0 {y} H1920" stroke="#1c0f08" stroke-width="2" opacity=".35"/>'
    b += '<ellipse cx="1230" cy="900" rx="620" ry="120" fill="url(#floorPool)"/>'
    # light cone from the ceiling lamp
    b += '<path d="M1200 -10 L1330 -10 L1760 1000 L760 1000Z" fill="#ffe6b0" opacity=".07" filter="url(#b24)"/>'
    # ---- the mobile: brass hoop hanging from a ceiling hook ----
    HX, HY, RX, RY = 1265, 150, 440, 46
    b += f'<path d="M{HX} -10 L{HX} 40" stroke="#c9a15a" stroke-width="6"/><circle cx="{HX}" cy="44" r="9" fill="none" stroke="#c9a15a" stroke-width="5"/>'
    for a in (200, 270 + 50, 340):
        px, py = HX + RX * math.cos(math.radians(a)), HY + RY * math.sin(math.radians(a))
    for px in (HX - RX * .8, HX + RX * .8, HX):
        pass
    # three suspension strings from hook to hoop
    for t in (math.pi * .93, math.pi * .07, math.pi * 1.5):
        px, py = HX + RX * math.cos(t), HY - RY * math.sin(t) * (-1 if t > math.pi else 1)
    sus = [(HX - RX * .93, HY - 15), (HX + RX * .93, HY - 15), (HX - 30, HY - RY + 4)]
    for px, py in sus:
        b += f'<path d="M{HX} 50 L{px:.0f} {py:.0f}" stroke="#e8dcc0" stroke-width="2.4" opacity=".8"/>'
    # back half of hoop
    b += f'<path d="M{HX - RX} {HY} A{RX} {RY} 0 0 1 {HX + RX} {HY}" fill="none" stroke="#6e5226" stroke-width="12"/>'
    # hanging planets: (angle on hoop in deg, string length, radius, colours, extras)
    P = [
        (196, 250, 22, ('#f0ece6', '#a9a39c', '#4e4a46'), {}),                       # Mercury
        (214, 330, 34, ('#fff2c8', '#e3c27a', '#7a5a2a'), {}),                        # Venus
        (236, 210, 38, ('#c8f0ff', '#3c8ed8', '#123566'), {'earth': 1}),              # Earth
        (258, 400, 28, ('#ffc6a0', '#cf5a32', '#5a1e0e'), {}),                        # Mars
        (292, 250, 92, ('#fff0d8', '#d9a777', '#6a3e22'), {'bands': ((-.6, .14, '#b07a4c', .55), (-.25, .16, '#f6e2c4', .5), (.05, .14, '#a86c42', .55), (.36, .1, '#c9905e', .5), (.24, .1, '#e07050', .0))}),  # Jupiter
        (318, 420, 58, ('#fff6dc', '#e8cf96', '#8a6a36'), {'ring': 1}),               # Saturn
        (336, 270, 40, ('#e6ffff', '#86d8e0', '#2c6a78'), {}),                        # Uranus
        (350, 360, 40, ('#d6e6ff', '#4a72e0', '#16245e'), {}),                        # Neptune
    ]
    front = ''; strings = ''
    for k, (ang, L, r, cols, ex) in enumerate(P):
        t = math.radians(ang)
        px = HX + RX * math.cos(t); py = HY - RY * math.sin(t)  # ang 180..360 -> front half (lower)
        cy = py + L
        strings += f'<path d="M{px:.0f} {py:.0f} L{px:.0f} {cy - r:.0f}" stroke="#efe6d0" stroke-width="2.4" opacity=".85"/>'
        dd, oo = ball(px, cy, r, *cols, uid=f'B{k}', bands=ex.get('bands'), ring=ex.get('ring'))
        d += dd
        if ex.get('earth'):
            d += f'<clipPath id="ec{k}"><circle cx="{px:.0f}" cy="{cy:.0f}" r="{r}"/></clipPath>'
            oo += f'<g clip-path="url(#ec{k})" opacity=".85"><path d="{smooth([(px - r * .6, cy - r * .5), (px - r * .1, cy - r * .7), (px + r * .1, cy - r * .2), (px - r * .3, cy + r * .2), (px - r * .7, cy)], closed=True)}" fill="#5dbb5a"/><path d="{smooth([(px + r * .3, cy + r * .1), (px + r * .8, cy), (px + r * .6, cy + r * .6), (px + r * .2, cy + r * .5)], closed=True)}" fill="#5dbb5a"/></g>'
            oo += f'<ellipse cx="{px - r * .35:.1f}" cy="{cy - r * .42:.1f}" rx="{r * .28:.1f}" ry="{r * .16:.1f}" fill="#fff" opacity=".45"/>'
        front += f'<ellipse cx="{px:.0f}" cy="{cy + r + 2:.0f}" rx="{r * .7:.0f}" ry="{r * .1 + 2:.0f}" fill="#000" opacity="0"/>' + oo
    b += strings
    # the ninth hook: the string snapped, a short frayed end still swings
    t = math.radians(212 - 4 + 160)  # = 8 deg -> right front end of the hoop
    px = HX + RX * math.cos(math.radians(186)); py = HY - RY * math.sin(math.radians(186))
    snap_x, snap_y = HX + RX * math.cos(math.radians(366 - 6)), HY - RY * math.sin(math.radians(366 - 6))
    sx, sy = HX + RX * math.cos(math.radians(184)), HY - RY * math.sin(math.radians(184))
    b += f'<path d="M{sx:.0f} {sy:.0f} q-10 50 12 96" fill="none" stroke="#fff3d6" stroke-width="3.6"/>'
    b += f'<path d="M{sx + 12:.0f} {sy + 96:.0f} l-10 12 M{sx + 12:.0f} {sy + 96:.0f} l2 15 M{sx + 12:.0f} {sy + 96:.0f} l12 8" stroke="#fff3d6" stroke-width="2.4"/>'
    b += spark(sx + 34, sy + 104, 14, col='#fff3d0')
    b += front
    # front half of the hoop
    b += f'<path d="M{HX - RX} {HY} A{RX} {RY} 0 0 0 {HX + RX} {HY}" fill="none" stroke="#3a2a10" stroke-width="16"/>'
    b += f'<path d="M{HX - RX} {HY} A{RX} {RY} 0 0 0 {HX + RX} {HY}" fill="none" stroke="#d9b264" stroke-width="10"/>'
    b += f'<path d="M{HX - RX + 40} {HY + 22} A{RX} {RY} 0 0 0 {HX + RX - 120} {HY + 30}" fill="none" stroke="#fff2c2" stroke-width="3" opacity=".6"/>'
    # little hooks on the hoop
    for ang in [p[0] for p in P] + [184]:
        t = math.radians(ang); px, py = HX + RX * math.cos(t), HY - RY * math.sin(t)
        b += f'<circle cx="{px:.0f}" cy="{py + 4:.0f}" r="5" fill="none" stroke="#e8c47a" stroke-width="3"/>'
    # ---- Pluto fallen on the floor, its broken string beside it, glowing a little ----
    PX, PY, PR = 860, 896, 50
    b += f'<ellipse cx="{PX + 6}" cy="{PY + PR - 2}" rx="{PR * 1.2:.0f}" ry="10" fill="#120806" opacity=".7" filter="url(#b3)"/>'
    b += f'<circle cx="{PX}" cy="{PY}" r="{PR * 2.4:.0f}" fill="#ffe6c0" opacity=".25" filter="url(#b24)"/>'
    pd, po = pluto(PX, PY, PR, 'B', heart_at=(.12, .18), rot=0, haze=False, detail=False)
    d += pd; b += po
    b += f'<circle cx="{PX}" cy="{PY}" r="{PR}" fill="none" stroke="#241a14" stroke-width="3"/>'
    b += f'<circle cx="{PX}" cy="{PY - PR - 3}" r="5" fill="none" stroke="#e8c47a" stroke-width="3"/>'
    b += f'<path d="M{PX} {PY - PR - 8} C{PX + 10} {PY - PR - 60} {PX + 90} {PY - 50} {PX + 120} {PY + 6} C{PX + 140} {PY + 34} {PX + 190} {PY + 30} {PX + 230} {PY + 34}" fill="none" stroke="#efe6d0" stroke-width="2.6"/>'
    # motion bumps (it just dropped)
    b += f'<path d="M{PX - 70} {PY + 28} q-14 -10 -26 -4 M{PX - 64} {PY + 6} q-16 -6 -26 2" fill="none" stroke="#ffe6c0" stroke-width="4" stroke-linecap="round" opacity=".7"/>'
    for x, y, s in ((PX - 20, PY - 80, 16), (PX + 60, PY - 66, 12), (PX - 90, PY - 30, 10)):
        b += spark(x, y, s, col='#fff3d0')
    # ---- the frog in a school cap, sitting on the floor, hands on cheeks, staring at fallen Pluto ----
    cap = ('<path d="M-30 -84 q34 -34 74 0 z" fill="#d6463c" stroke-width="3.2"/><path d="M-30 -84 q-20 2 -34 10 q20 4 40 -4z" fill="#b2332b" stroke-width="3"/>'
           '<circle cx="8" cy="-100" r="4" fill="#f2d27a" stroke-width="2"/>')
    tie = '<path d="M0 -24 l-14 -8 l0 16z M12 -24 l14 -8 l0 16z" fill="#f2d27a" stroke-width="2.6"/><circle cx="6" cy="-24" r="5" fill="#f2d27a" stroke-width="2.6"/>'
    b += frog(1120, 952, 2.9, flip=True, look=(-3.4, 3.2), mouth='O', hat=cap, mid=tie,
              armL='M-34 -22 q-8 -14 -6 -24', armR='M38 -22 q8 -14 4 -24',
              legs=((-20, -6, -30, 4, -8), (20, -6, 30, 4, 8)))
    b += '<rect width="1920" height="1080" fill="url(#vigB)"/>'
    return page('#1a1633', svg(d, b), [('NINE', 206, 'w'), ('BECAME', 124, 'w'), ('EIGHT', 206, 'y')])


# =========================== C: New Horizons heart photo (NASA 2015) + the probe flying past ===========================
def probe(x, y, s, rot):
    """New Horizons: gold-foil triangular body, big white dish, black RTG on a strut."""
    o = f'<g transform="translate({x} {y}) rotate({rot}) scale({s})" stroke="#1a1408" stroke-linejoin="round" stroke-width="3">'
    # RTG strut + cylinder
    o += '<path d="M40 30 L150 92" stroke-width="8"/><path d="M40 30 L150 92" stroke="#9aa0a8" stroke-width="4"/>'
    o += '<g transform="translate(160 98) rotate(30)"><rect x="-14" y="-40" width="28" height="80" rx="6" fill="#2a2c33"/>'
    o += ''.join(f'<path d="M-24 {yy} H24" stroke="#4a4d58" stroke-width="6"/>' for yy in (-26, -10, 6, 22)) + '<rect x="-10" y="-38" width="6" height="74" fill="#7b808c" stroke="none" opacity=".6"/></g>'
    # body (gold foil)
    o += '<path d="M-70 10 L60 -8 L84 54 L-40 92Z" fill="url(#foilC)"/>'
    o += '<path d="M-70 10 L-40 92 L-60 104 L-92 24Z" fill="#8a6418"/>'
    o += '<path d="M-40 92 L84 54 L74 72 L-60 104Z" fill="#6e4e10"/>'
    for a, b_ in ((-30, 30), (10, 22), (40, 40), (-10, 70)):
        o += f'<path d="M{a} {b_} l18 -4 l-6 12z" fill="#fff4c0" stroke="none" opacity=".5"/>'
    # instruments
    o += '<rect x="-20" y="60" width="26" height="18" rx="3" fill="#cfd3da"/><circle cx="-7" cy="69" r="6" fill="#20232a"/>'
    o += '<rect x="30" y="40" width="22" height="16" rx="3" fill="#cfd3da"/>'
    # high-gain dish, tilted up-left like a satellite dish, feed horn on a tripod
    o += '<g transform="translate(-66 -22) rotate(-52)">'
    o += '<path d="M-20 30 L-8 62 M20 30 L8 62" stroke-width="7"/><path d="M-20 30 L-8 62 M20 30 L8 62" stroke="#cfd3da" stroke-width="3"/>'
    o += '<path d="M-118 0 Q0 80 118 0Z" fill="#9aa3b0" stroke-width="4"/>'
    o += '<ellipse cx="0" cy="0" rx="118" ry="30" fill="url(#dishC)" stroke-width="4"/>'
    o += '<ellipse cx="0" cy="2" rx="96" ry="22" fill="#eef1f6" stroke="none" opacity=".8"/>'
    o += '<ellipse cx="0" cy="4" rx="46" ry="11" fill="none" stroke="#b9c0ca" stroke-width="2"/>'
    o += '<path d="M-60 6 L0 -70 M60 6 L0 -70" stroke-width="5"/><path d="M-60 6 L0 -70 M60 6 L0 -70" stroke="#d9dde4" stroke-width="2.2"/><circle cx="0" cy="-74" r="9" fill="#e8ebf0"/>'
    o += '<path d="M-90 -8 q50 -18 110 -14" fill="none" stroke="#fff" stroke-width="4" opacity=".85"/></g>'
    o += '</g>'
    return o


def make_C():
    rnd = random.Random(3)
    d = FILTERS
    d += lin('foilC', [(0, '#ffe58a'), (.5, '#d9a632'), (1, '#8a6418')], x2=1, y2=1)
    d += lin('dishC', [(0, '#ffffff'), (1, '#aab3c0')])
    d += rad('sunC', 120, 60, 900, [(0, '#fff3d6', .55), (.3, '#f0c890', .18), (1, '#f0c890', 0)])
    d += rad('vigC', 960, 540, 1150, [(.55, '#000', 0), (1, '#000', .6)])
    PX, PY, PR = 1340, 610, 430
    pd, po = pluto(PX, PY, PR, 'C', heart_at=(.3, .14), heart_s=PR / 150, rot=-10, light=(-.6, -.45))
    d += pd
    d += rad('heartGlow', PX + .3 * PR, PY + .14 * PR, 360, [(0, '#fff4dc', .55), (.5, '#ffd7a8', .15), (1, '#ffd7a8', 0)])
    b = '<rect width="1920" height="1080" fill="#05060d"/>'
    b += starfield(rnd, 220, col='#f2f6ff')
    b += '<rect width="1920" height="1080" fill="url(#sunC)"/>'
    # Charon, small and far, upper right
    cd, co = moon(1770, 120, 46, 'Ch')
    d += cd; b += co.replace('#dfe6ff', '#cfc8c0')
    b += f'<circle cx="{PX}" cy="{PY}" r="{PR * 1.35:.0f}" fill="#ffcf9a" opacity=".12" filter="url(#b80)"/>'
    b += po
    # glowing heart
    b += f'<circle cx="{PX + .3 * PR:.0f}" cy="{PY + .14 * PR:.0f}" r="360" fill="url(#heartGlow)"/>'
    hx, hy = PX + .3 * PR, PY + .14 * PR
    b += f'<g filter="url(#b6)" opacity=".7">{heart(hx, hy, PR / 150, -10, fill="#fff8ea")}</g>'
    b += heart(hx, hy, PR / 150, -10, fill='#fbefd6', extra='<path d="M-60,-30 C-50,-56 -24,-60 -10,-44" fill="none" stroke="#fff" stroke-width="3" opacity=".8"/><path d="M-74 -10 q30 4 60 -6 M-60 14 q26 2 52 -4" fill="none" stroke="#e9dcc4" stroke-width="2.4" opacity=".7"/>')
    for x, y, s in ((1120, 170, 20), (1690, 330, 14), (760, 640, 16), (1840, 620, 12), (1010, 920, 14)):
        b += spark(x, y, s)
    # probe flying past in the foreground, lit from the upper left; the frog in a space helmet rides on the dish
    b += f'<path d="M180 1000 Q520 900 760 800" fill="none" stroke="#bfe0ff" stroke-width="10" opacity=".18" filter="url(#b12)"/>'
    b += probe(820, 760, 1.55, -14)
    b += frog(904, 722, 1.8, rot=-14, look=(3.4, 2.6), mouth='O', helmet=True,
              armL='M-34 -22 q-20 -6 -30 -22', armR='M38 -22 q16 -10 26 -34',
              legs=((-20, -6, -28, 4, -10), (20, -6, 26, 4, 10)))
    b += '<rect width="1920" height="1080" fill="url(#vigC)"/>'
    return page('#05060d', svg(d, b), [('IT HAS', 132, 'w'), ('A HEART', 200, 'y')])


if __name__ == '__main__':
    which = sys.argv[1:] or ['A', 'B', 'C']
    for n in which:
        open(os.path.join(HERE, f'{n}.html'), 'w').write(globals()[f'make_{n}']())
    print('ok')
