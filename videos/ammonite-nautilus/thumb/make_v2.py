# ammonite-nautilus thumbnails D-F (v2, owner feedback 2026-10-22: "C's text is good and A's picture is good; mix the two").
# run: python3 make_v2.py  (writes D.html E.html F.html here; A-C from make.py stay untouched)
# All three: text WHY DID IT / SURVIVE? (C) + picture of A (homage: Avengers: Infinity War "the snap"):
#   the bronze ammonite crumbles into drifting golden dust while the striped nautilus swims on unharmed.
# D  teal sunlit sea (A's light), dust drifts up-left.
# E  C's burning asteroid + ash sky above the sea surface, the ammonite's dust falls/sinks with the ash.
# F  dark twilight blue, a bright shaft of light from above glows on the nautilus, the dust rises toward the light.
# script: "How could a dominant, widespread group disappear completely, while its lookalike survived?"
# nautilus anatomy (script S13): lens-less pinhole eyes, up to ~90 thin tentacles (cirri, no suckers), leathery hood.
import os, sys, math, random
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, '..', '..', '..', 'tools'))
from thumb_lib import *
from make import P, smooth, taper, FILTERS, ammonite, TAU

TEXT = [('WHY DID IT', 128, 'w'), ('SURVIVE?', 206, 'y')]


def lerp(a, b, t):
    return (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t)


# ---------------------------------------------------------------- nautilus v2 (rounded hood, soft body, pinhole eye, many thin cirri)
def nautilus2(gid, cx, cy, R, rim='#bfefff', rim2=None, glow=None, seed=3, wave=0.0, light=1.0, tent_len=1.0):
    b = math.log(3.0) / TAU
    T = math.radians(80)

    def rad_(t):
        return R * math.exp(b * (t - T))

    def pt(t, r=None):
        rr = rad_(t) if r is None else r
        return (cx - rr * math.cos(t), cy + rr * math.sin(t))
    N = 160
    outer = [pt(T - TAU + TAU * i / N) for i in range(N + 1)]
    shell = smooth(outer) + 'Z'
    rin = rad_(T - TAU)
    rnd = random.Random(seed)
    d = (f'<radialGradient id="{gid}sh" cx="{cx - R * .25:.0f}" cy="{cy - R * .45:.0f}" r="{R * 1.5:.0f}" gradientUnits="userSpaceOnUse">'
         f'<stop offset="0" stop-color="#fffdf6"/><stop offset=".4" stop-color="#f6ead4"/><stop offset=".78" stop-color="#d2ba96"/>'
         f'<stop offset="1" stop-color="#8a6e50"/></radialGradient>'
         f'<clipPath id="{gid}cl"><path d="{shell}"/></clipPath>'
         f'<radialGradient id="{gid}bd" cx="{cx + R * .05:.0f}" cy="{cy + R * .45:.0f}" r="{R * .6:.0f}" gradientUnits="userSpaceOnUse">'
         f'<stop offset="0" stop-color="#f4c6a8"/><stop offset=".55" stop-color="#d9957a"/><stop offset="1" stop-color="#9a5a46"/></radialGradient>'
         f'<radialGradient id="{gid}hood" cx="{cx + R * .05:.0f}" cy="{cy + R * .18:.0f}" r="{R * .55:.0f}" gradientUnits="userSpaceOnUse">'
         f'<stop offset="0" stop-color="#c9805a"/><stop offset=".6" stop-color="#9a5232"/><stop offset="1" stop-color="#5c2c18"/></radialGradient>'
         f'<linearGradient id="{gid}iri" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#bff4ff" stop-opacity="0"/>'
         f'<stop offset=".45" stop-color="#c8f6ec" stop-opacity=".18"/><stop offset=".6" stop-color="#f4d0ff" stop-opacity=".14"/><stop offset="1" stop-color="#ffe2b0" stop-opacity="0"/></linearGradient>')
    o = ''
    if glow:
        o += f'<circle cx="{cx + R * .25:.0f}" cy="{cy + R * .1:.0f}" r="{R * 1.45:.0f}" fill="{glow}" opacity=".38" filter="url(#huge)"/>'
    ap_in = pt(T, rin); ap_out = pt(T)

    def Q(x, y):   # head coordinates in units of R relative to the coil centre
        return (cx + x * R, cy + y * R)
    hood_top = [pt(t, rad_(t - TAU) * 1.03) for t in [T - .08 + .78 * k / 10 for k in range(11)]]   # rests on the older whorl
    hood_top = [Q(*p) for p in ((-.12, .33), (-.03, .255), (.10, .21), (.25, .205), (.38, .24), (.48, .31))]
    hood_out = [Q(-.18, .44)] + hood_top + [Q(.545, .41), Q(.54, .51), Q(.47, .585), Q(.33, .615), Q(.17, .625), Q(.03, .645), Q(-.10, .62), Q(-.17, .54)]
    body = [Q(*p) for p in ((-.12, .50), (.10, .56), (.30, .58), (.41, .61), (.43, .70), (.37, .80), (.24, .90), (.08, .95),
                            (-.08, .975), (-.17, .90), (-.16, .60))]
    root_curve = [Q(*p) for p in ((.42, .60), (.43, .68), (.40, .76), (.34, .83), (.26, .885))]
    roots = [None] * 14
    for k in range(14):
        f = k / 13 * 4; i = min(3, int(f)); roots[k] = lerp(root_curve[i], root_curve[i + 1], f - i)

    def cirri(n, col, edge, wmin, wmax, Lmin, Lmax, a0, a1, op=1.0, hl=True):
        s = ''
        for i in range(n):
            u = (i + rnd.uniform(-.4, .4)) / max(1, n - 1)
            sx, sy = roots[min(13, max(0, int(u * 13 + rnd.uniform(-1.2, 1.2))))]
            sx += rnd.uniform(-.015, .015) * R; sy += rnd.uniform(-.015, .015) * R
            ang = math.radians(a0 + (a1 - a0) * u + rnd.uniform(-7, 7))
            L = R * rnd.uniform(Lmin, Lmax) * tent_len
            ph = rnd.uniform(0, TAU); amp = rnd.uniform(.25, .5); curl = rnd.choice([-1, 1]) * rnd.uniform(.6, 1.6)
            pts = [(sx, sy)]
            for k in range(1, 19):
                f = k / 18
                a = ang + amp * math.sin(ph + f * 4.2 + wave) * f ** .8 + curl * max(0, f - .7) ** 1.5 * 3
                pts.append((pts[-1][0] + math.cos(a) * L / 18, pts[-1][1] + math.sin(a) * L / 18))
            w = R * rnd.uniform(wmin, wmax)
            s += f'<path d="{taper(pts, w + R * .009, R * .008)}" fill="{edge}" opacity="{.8 * op:.2f}"/>'
            s += f'<path d="{taper(pts, w, R * .004)}" fill="{col}" opacity="{op:.2f}"/>'
            if hl:
                hp = [(x, y - w * .18) for x, y in pts[1:9]]
                s += f'<path d="{smooth(hp)}" fill="none" stroke="#fff2e6" stroke-width="{w * .26:.1f}" stroke-linecap="round" opacity=".55"/>'
        return s
    # back cirri (darker, behind the shell lip)
    o += cirri(16, '#a8644e', '#3c1c12', .016, .022, .55, .95, -28, 50, op=.95, hl=False)
    # ---- shell
    o += f'<path d="{shell}" fill="url(#{gid}sh)" stroke="#3b2618" stroke-width="{R * .016:.1f}" stroke-linejoin="round"/>'
    st = f'<g clip-path="url(#{gid}cl)">'
    nst = 19
    for i in range(nst):
        t0 = T - TAU + .25 + (TAU * .74) * i / nst + rnd.uniform(-.04, .04)
        wdt = rnd.uniform(.10, .16) * (1.0 - .45 * i / nst)
        left = []; right = []
        for k in range(15):
            f = k / 14
            r = rin * .55 + (rad_(t0) * 1.05 - rin * .55) * f
            wob = .10 * math.sin(f * 5.5 + i) * f + .22 * f
            ta = t0 - wob
            ww = wdt * (0.3 + .95 * f)
            left.append(pt(ta - ww / 2, r)); right.append(pt(ta + ww / 2, r))
        col = rnd.choice(['#8e3b1e', '#9a4524', '#7e3218'])
        st += f'<path d="{smooth(left + right[::-1], True)}" fill="{col}" opacity="{rnd.uniform(.75, .92):.2f}"/>'
    st += '</g>'
    o += st
    sh = f'<g clip-path="url(#{gid}cl)">'
    for i in range(44):
        t0 = T - TAU + TAU * i / 44
        ln = [pt(t0 - .2 * f, rin * .5 + (rad_(t0) * 1.05 - rin * .5) * f) for f in [k / 8 for k in range(9)]]
        sh += f'<path d="{smooth(ln)}" fill="none" stroke="#6b4a2e" stroke-width="{R * .0035:.1f}" opacity=".28"/>'
    # inner whorl shadow (the older whorl tucks in), underside shade, pearly sheen + highlight
    inner = [pt(t, rin) for t in [T - TAU + TAU * k / 60 for k in range(61)]]
    sh += f'<path d="{smooth(inner)}" fill="none" stroke="#3a2414" stroke-width="{R * .05:.1f}" opacity=".35" filter="url(#soft2)"/>'
    sh += f'<ellipse cx="{cx + R * .2:.0f}" cy="{cy + R * .78:.0f}" rx="{R * 1.1:.0f}" ry="{R * .55:.0f}" fill="#2a1a10" opacity=".38" filter="url(#soft)"/>'
    sh += f'<rect x="{cx - R * 1.2:.0f}" y="{cy - R * 1.2:.0f}" width="{R * 2.4:.0f}" height="{R * 2.4:.0f}" fill="url(#{gid}iri)"/>'
    sh += f'<ellipse cx="{cx - R * .38:.0f}" cy="{cy - R * .48:.0f}" rx="{R * .36:.0f}" ry="{R * .16:.0f}" fill="#ffffff" opacity="{.55 * light:.2f}" filter="url(#soft2)" transform="rotate(-32 {cx - R * .38:.0f} {cy - R * .48:.0f})"/>'
    sh += f'<ellipse cx="{cx - R * .62:.0f}" cy="{cy - R * .1:.0f}" rx="{R * .05:.0f}" ry="{R * .18:.0f}" fill="#ffffff" opacity="{.3 * light:.2f}" filter="url(#soft3)" transform="rotate(20 {cx - R * .62:.0f} {cy - R * .1:.0f})"/>'
    sh += '</g>'
    o += sh
    # rim light (top-left arc) + optional second rim (right side, back light)
    rl = [pt(t) for t in [T - TAU * .64 + TAU * .34 * k / 30 for k in range(31)]]
    o += f'<path d="{smooth(rl)}" fill="none" stroke="{rim}" stroke-width="{R * .028:.1f}" stroke-linecap="round" opacity=".85"/>'
    o += f'<path d="{smooth(rl)}" fill="none" stroke="{rim}" stroke-width="{R * .10:.1f}" stroke-linecap="round" opacity=".28" filter="url(#soft2)"/>'
    if rim2:
        r2 = [pt(t) for t in [T - TAU * .30 + TAU * .22 * k / 30 for k in range(31)]]
        o += f'<path d="{smooth(r2)}" fill="none" stroke="{rim2}" stroke-width="{R * .02:.1f}" stroke-linecap="round" opacity=".7"/>'
    # umbilicus
    o += f'<circle cx="{cx:.0f}" cy="{cy:.0f}" r="{R * .07:.1f}" fill="#dccaae" stroke="#4a3220" stroke-width="{R * .011:.1f}"/>'
    o += f'<circle cx="{cx - R * .015:.0f}" cy="{cy - R * .02:.0f}" r="{R * .03:.1f}" fill="#fff6e6" opacity=".75"/>'
    # aperture dark interior
    o += f'<path d="{smooth([ap_in, (ap_in[0] + R * .06, (ap_in[1] + ap_out[1]) / 2), ap_out], False)}" fill="none" stroke="#24120a" stroke-width="{R * .07:.1f}" opacity=".55"/>'
    # ---- funnel (rolled tube under the head, pointing forward-down)
    fpts = [Q(*p) for p in ((-.06, .90), (.10, .89), (.22, .93), (.27, .99), (.22, 1.03), (.10, 1.00), (-.06, 1.0))]
    o += f'<path d="{smooth(fpts, True)}" fill="#c8846a" stroke="#3a1e14" stroke-width="{R * .011:.1f}"/>'
    o += f'<path d="{smooth([Q(-.02, .925), Q(.12, .925), Q(.22, .965)])}" fill="none" stroke="#f0b496" stroke-width="{R * .012:.1f}" stroke-linecap="round" opacity=".7"/>'
    o += f'<ellipse cx="{Q(.255, .99)[0]:.1f}" cy="{Q(.255, .99)[1]:.1f}" rx="{R * .02:.1f}" ry="{R * .035:.1f}" fill="#4a2018" transform="rotate(-30 {Q(.255, .99)[0]:.1f} {Q(.255, .99)[1]:.1f})"/>'
    # ---- body (soft, rounded) + shading
    bp = smooth(body, True)
    d += f'<clipPath id="{gid}bc"><path d="{bp}"/></clipPath>'
    o += f'<path d="{bp}" fill="url(#{gid}bd)" stroke="#3a1e14" stroke-width="{R * .012:.1f}"/>'
    o += (f'<g clip-path="url(#{gid}bc)"><ellipse cx="{Q(.05, .95)[0]:.1f}" cy="{Q(.05, .95)[1]:.1f}" rx="{R * .3:.1f}" ry="{R * .12:.1f}" fill="#5a2a1a" opacity=".4" filter="url(#soft2)"/>'
          f'<ellipse cx="{Q(.0, .62)[0]:.1f}" cy="{Q(.0, .62)[1]:.1f}" rx="{R * .3:.1f}" ry="{R * .06:.1f}" fill="#3a1408" opacity=".45" filter="url(#soft2)"/>'
          f'<ellipse cx="{Q(.18, .72)[0]:.1f}" cy="{Q(.18, .72)[1]:.1f}" rx="{R * .12:.1f}" ry="{R * .07:.1f}" fill="#ffe0cc" opacity=".25" filter="url(#soft2)"/></g>')
    o += f'<path d="{smooth([ap_in, Q(-.03, .62), ap_out])}" fill="none" stroke="#2a160c" stroke-width="{R * .035:.1f}" opacity=".4" filter="url(#soft3)" transform="translate({R * .03:.1f} 0)"/>'
    # tentacle sheath lobes (soft rounded collar where the cirri start)
    for k in range(8):
        p = roots[1 + int(k * 11 / 7)]
        o += f'<ellipse cx="{p[0] - R * .005:.1f}" cy="{p[1]:.1f}" rx="{R * .045:.1f}" ry="{R * .036:.1f}" fill="#e6a488" stroke="#5a2c1e" stroke-width="{R * .007:.1f}"/>'
    # mid cirri
    o += cirri(18, '#d8937a', '#4a2418', .017, .023, .55, .95, -18, 58)
    # ---- hood: rounded leathery dome resting on the older whorl, pale blotches, soft top highlight, shadow under the rim
    hp = smooth(hood_out, True)
    d += f'<clipPath id="{gid}hc"><path d="{hp}"/></clipPath>'
    o += f'<path d="{smooth([Q(-.10, .64), Q(.1, .66), Q(.3, .64), Q(.48, .56)])}" fill="none" stroke="#2a120a" stroke-width="{R * .05:.1f}" opacity=".35" filter="url(#soft3)"/>'
    o += f'<path d="{hp}" fill="url(#{gid}hood)" stroke="#2a140c" stroke-width="{R * .013:.1f}" stroke-linejoin="round"/>'
    hb = f'<g clip-path="url(#{gid}hc)">'
    for k in range(34):
        bx, by = Q(rnd.uniform(-.12, .52), rnd.uniform(.20, .62))
        hb += f'<ellipse cx="{bx:.1f}" cy="{by:.1f}" rx="{R * rnd.uniform(.012, .032):.1f}" ry="{R * rnd.uniform(.008, .02):.1f}" fill="#f6e2cc" opacity="{rnd.uniform(.3, .65):.2f}" transform="rotate({rnd.uniform(-30, 30):.0f} {bx:.1f} {by:.1f})"/>'
    hx, hy = Q(.20, .27)
    hb += f'<ellipse cx="{hx:.1f}" cy="{hy:.1f}" rx="{R * .2:.1f}" ry="{R * .045:.1f}" fill="#ffe0c4" opacity=".55" filter="url(#soft3)" transform="rotate(6 {hx:.1f} {hy:.1f})"/>'
    hb += f'<path d="{smooth([Q(-.12, .62), Q(.1, .62), Q(.32, .61), Q(.52, .50)])}" fill="none" stroke="#2a120a" stroke-width="{R * .06:.1f}" opacity=".45" filter="url(#soft2)"/>'
    hb += '</g>'
    o += hb
    o += f'<path d="{smooth(hood_top[1:] + [Q(.545, .41)])}" fill="none" stroke="{rim}" stroke-width="{R * .012:.1f}" stroke-linecap="round" opacity=".55"/>'
    # pinhole eye: rounded bump under the hood rim with a pin-sized dark hole (no lens, no shine)
    ex, ey = Q(.15, .71)
    o += f'<ellipse cx="{ex:.1f}" cy="{ey:.1f}" rx="{R * .058:.1f}" ry="{R * .052:.1f}" fill="#c98468" stroke="#5a2c1e" stroke-width="{R * .009:.1f}"/>'
    o += f'<ellipse cx="{ex - R * .012:.1f}" cy="{ey - R * .02:.1f}" rx="{R * .028:.1f}" ry="{R * .013:.1f}" fill="#fad2b6" opacity=".6"/>'
    o += f'<circle cx="{ex + R * .004:.1f}" cy="{ey + R * .004:.1f}" r="{R * .012:.1f}" fill="#100604"/>'
    # front cirri (light, thin)
    o += cirri(16, '#f2b89a', '#5a2c1e', .018, .024, .45, .85, -10, 66)
    return d, o


# ---------------------------------------------------------------- ammonite crumbling to dust in direction phi (deg, svg coords)
def dissolve(gid, cx, cy, R, phi, rot, front0=-.15, n_dust=1000, spread=14, dist=(450, 900), drift=(0, -110), seed=21,
             cols=('#c88a4a', '#a8682e', '#e0aa62', '#7a4a22', '#f2d27a', '#5a3418', '#ffe2a0'), rim='#ffe2a8', glint='#fff3c8'):
    da, a = ammonite(gid, cx, cy, R, seed=7, rot=rot, rim=rim)
    rnd = random.Random(seed)
    dx, dy = math.cos(math.radians(phi)), math.sin(math.radians(phi))
    nx, ny = -dy, dx

    def W(u, v):
        return (cx + u * dx + v * nx, cy + u * dy + v * ny)

    def front(v):   # u (along dust direction) of the dissolve front; shell remains where u < front
        return R * front0 + R * .2 * math.sin(v / R * 2.3 + .6) + R * .06 * math.sin(v / R * 7.1) + rnd.uniform(-1, 1) * R * .03
    m = f'<mask id="{gid}m" maskUnits="userSpaceOnUse" x="0" y="0" width="1920" height="1080"><rect width="1920" height="1080" fill="#fff"/>'
    pts = [W(front(v), v) for v in [-R * 1.25 + R * 2.5 * k / 50 for k in range(51)]]
    m += f'<path d="{P(pts)} L{W(R * 2, R * 1.25)[0]:.0f},{W(R * 2, R * 1.25)[1]:.0f} L{W(R * 2, -R * 1.25)[0]:.0f},{W(R * 2, -R * 1.25)[1]:.0f}Z" fill="#000"/>'
    for _ in range(320):
        v = rnd.uniform(-R, R); u = front(v) - abs(rnd.gauss(0, R * .13)); x, y = W(u, v); s_ = rnd.uniform(4, 16)
        m += f'<rect x="{x:.1f}" y="{y:.1f}" width="{s_:.1f}" height="{s_ * rnd.uniform(.5, 1.2):.1f}" fill="#000" transform="rotate({rnd.uniform(0, 90):.0f} {x:.1f} {y:.1f})"/>'
    for _ in range(120):
        v = rnd.uniform(-R, R); u = front(v) + abs(rnd.gauss(0, R * .10)); x, y = W(u, v); s_ = rnd.uniform(5, 17)
        m += f'<rect x="{x:.1f}" y="{y:.1f}" width="{s_:.1f}" height="{s_ * .8:.1f}" fill="#fff" transform="rotate({rnd.uniform(0, 90):.0f} {x:.1f} {y:.1f})"/>'
    m += '</mask>'
    da += m
    o = f'<ellipse cx="{cx}" cy="{cy}" rx="{R * 1.25:.0f}" ry="{R * 1.05:.0f}" fill="#ffcf86" opacity=".2" filter="url(#huge)"/>'
    o += f'<g mask="url(#{gid}m)">{a}</g>'
    # glowing ember edge along the front
    for k in range(80):
        v = -R * .98 + R * 1.96 * k / 79; x, y = W(front(v), v)
        if (x - cx) ** 2 + (y - cy) ** 2 < (R * .97) ** 2:
            o += f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{rnd.uniform(3, 7.5):.1f}" fill="#ffd98a" opacity="{rnd.uniform(.45, .9):.2f}"/>'
            if k % 3 == 0:
                o += f'<circle cx="{x:.1f}" cy="{y:.1f}" r="14" fill="#ffc860" opacity=".35" filter="url(#soft3)"/>'
    # dust streams
    for _ in range(n_dust):
        v = rnd.uniform(-R * .95, R * .95); u0 = front(v) + rnd.uniform(-R * .05, R * .25)
        x0, y0 = W(u0, v)
        if (x0 - cx) ** 2 + (y0 - cy) ** 2 > (R * 1.05) ** 2:
            continue
        t = rnd.random() ** 1.5
        L = t * rnd.uniform(*dist)
        ang = math.radians(phi + rnd.uniform(-spread, spread))
        x = x0 + math.cos(ang) * L + nx * math.sin(t * 6 + v / 40) * 30 * t + drift[0] * t * t
        y = y0 + math.sin(ang) * L + ny * math.sin(t * 6 + v / 40) * 30 * t + drift[1] * t * t
        if x < -20 or y < -20 or x > 1940 or y > 1100:
            continue
        s_ = rnd.uniform(3, 14) * (1 - .6 * t)
        op = (1 - t) * .95 + .05
        o += f'<rect x="{x:.1f}" y="{y:.1f}" width="{s_:.1f}" height="{s_ * rnd.uniform(.5, 1):.1f}" fill="{rnd.choice(cols)}" opacity="{op:.2f}" transform="rotate({rnd.uniform(0, 90):.0f} {x:.1f} {y:.1f})"/>'
    for _ in range(55):
        t = rnd.uniform(.05, .65); v = rnd.uniform(-R * .8, R * .8); x0, y0 = W(front(v), v)
        ang = math.radians(phi + rnd.uniform(-spread, spread)); L = t * (dist[0] + dist[1]) / 2
        x = x0 + math.cos(ang) * L + drift[0] * t * t; y = y0 + math.sin(ang) * L + drift[1] * t * t
        o += f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{rnd.uniform(2, 4.2):.1f}" fill="{glint}" opacity=".95"/><circle cx="{x:.1f}" cy="{y:.1f}" r="11" fill="#ffe6a0" opacity=".28" filter="url(#soft3)"/>'
    return da, o



def vignette(gid, cy=540, a=.45):
    return rad(gid, 960, cy, 1150, [(0, '#000', 0), (.68, '#000', 0), (1, '#000', a)]), f'<rect width="1920" height="1080" fill="url(#{gid})"/>'


def seafloor(col1, col2, gid, y0=985, weeds='#0a2c3a', xs=(1060, 1130, 1700), seed=2):
    rnd = random.Random(seed)
    d = lin(gid, [(0, col1), (1, col2)])
    fl = [(0, y0 + 15), (220, y0 - 10), (440, y0 + 5), (660, y0 - 25), (900, y0), (1150, y0 - 15), (1400, y0 + 5), (1650, y0 - 10), (1920, y0 + 10)]
    b = f'<path d="{smooth(fl)} L1920,1080 L0,1080Z" fill="url(#{gid})"/>'
    for x0 in xs:   # sea lilies / sponges
        hh = rnd.randint(110, 170)
        b += f'<path d="M{x0},{y0} q{rnd.randint(-20, 20)},{-hh / 2:.0f} {rnd.randint(-10, 30)},{-hh}" stroke="{weeds}" stroke-width="7" fill="none"/>'
        b += f'<circle cx="{x0 + 10}" cy="{y0 - hh}" r="16" fill="{weeds}"/>'
    return d, b


# ======================= D: teal sunlit sea (A's light), dust drifts up-left =======================
def scene_D():
    random.seed(41)
    d = FILTERS + lin('Dsea', [(0, '#46aebb'), (.35, '#1e7287'), (.7, '#0d3d50'), (1, '#061e2a')])
    d += rad('Dsun', 1500, -120, 1000, [(0, '#fff2c4', .9), (.35, '#ffd27a', .35), (1, '#ffd27a', 0)])
    b = '<rect width="1920" height="1080" fill="url(#Dsea)"/><rect width="1920" height="1080" fill="url(#Dsun)"/>'
    for i in range(7):   # god rays from the upper right
        x = 1050 + i * 130 + random.randint(-30, 30); w = random.randint(40, 110)
        b += f'<path d="M{x},-10 L{x + w},-10 L{x - 380 + w * 2},1080 L{x - 420},1080Z" fill="#e8fbff" opacity="{random.uniform(.04, .09):.2f}"/>'
    for i in range(30):
        y = random.randint(8, 140); x = random.randint(500, 1920); L = random.randint(60, 200)
        b += f'<path d="M{x},{y} q{L / 4:.0f},-10 {L / 2:.0f},0 t{L / 2:.0f},0" fill="none" stroke="#fff4d0" stroke-width="{random.choice([2, 3, 4])}" opacity="{random.uniform(.15, .4):.2f}"/>'
    df, bf = seafloor('#123848', '#04131b', 'Dfl')
    d += df; b += bf
    b += stars(80, 1000, col='#d8fbff', op=.35, sparks=0)
    # nautilus, intact, sunlit
    b += '<ellipse cx="1450" cy="520" rx="560" ry="440" fill="#b8f6ff" opacity=".22" filter="url(#huge)"/>'
    dn, n = nautilus2('dn', 1320, 385, 340, rim='#fff1c0', rim2='#bff6ff', glow='#a8f2ff', seed=4, tent_len=.78)
    d += dn; b += n
    # ammonite turning to dust
    da, a = dissolve('da', 600, 715, 285, phi=203, rot=-88, front0=-.12, n_dust=1100, dist=(450, 820), drift=(0, -120))
    d += da; b += a
    b += spark(1640, 150, 24) + spark(1010, 520, 16) + spark(1800, 560, 14)
    dv, bv = vignette('Dvig')
    d += dv; b += bv
    return page('#0c3a4c', svg(d, b), TEXT, outline='#06161e')


# ======================= E: burning asteroid + ash sky, the ammonite's dust sinks with the ash =======================
def scene_E():
    random.seed(52)
    SURF = 250
    d = FILTERS + lin('Esky', [(0, '#2a0c10'), (.5, '#7a2414'), (1, '#e8702e')])
    d += lin('Esea', [(0, '#5a4a34'), (.25, '#2c3a3c'), (.6, '#142a3a'), (1, '#071422')])
    d += rad('Efire', 1640, 120, 560, [(0, '#fff2b0', 1), (.12, '#ffc35a', .9), (.4, '#ff6a20', .35), (1, '#ff4a10', 0)])
    b = f'<rect width="1920" height="{SURF + 20}" fill="url(#Esky)"/><rect y="{SURF}" width="1920" height="{1080 - SURF}" fill="url(#Esea)"/>'
    for _ in range(40):   # smoke along the horizon
        x = random.randint(-100, 1900); y = random.randint(110, SURF - 10); r = random.randint(50, 120)
        b += f'<ellipse cx="{x}" cy="{y}" rx="{r * 1.6:.0f}" ry="{r * .6:.0f}" fill="{random.choice(["#1e0c0a", "#2c1210", "#3a1a12"])}" opacity="{random.uniform(.4, .8):.2f}"/>'
    b += f'<ellipse cx="1500" cy="{SURF}" rx="560" ry="55" fill="#ff7a2a" opacity=".55" filter="url(#soft)"/>'
    b += f'<rect width="1920" height="{SURF}" fill="url(#Efire)"/>'
    ax, ay = 1650, 125
    for k in range(10):
        t = k / 9
        b += f'<path d="M{ax},{ay} L{ax + 460 - 40 * t:.0f},{ay - 300 + 30 * t:.0f}" stroke="{["#fff3c0", "#ffc760", "#ff8a30", "#c84a18"][k % 4]}" stroke-width="{80 - 60 * t:.0f}" stroke-linecap="round" opacity="{.2 + .1 * (1 - t):.2f}" filter="url(#soft2)"/>'
    b += f'<path d="M{ax - 36},{ay + 5} L{ax + 500},{ay - 330} L{ax + 530},{ay - 290}Z" fill="#ffb24a" opacity=".55" filter="url(#soft2)"/>'
    b += f'<circle cx="{ax}" cy="{ay}" r="110" fill="#ffd27a" opacity=".6" filter="url(#soft)"/>'
    rock = [(ax + 46 * math.cos(a) * random.uniform(.85, 1.1), ay + 41 * math.sin(a) * random.uniform(.85, 1.1)) for a in [TAU * i / 14 for i in range(14)]]
    b += f'<path d="{smooth(rock, True)}" fill="#3a2418" stroke="#1a0c08" stroke-width="5"/>'
    b += f'<path d="{smooth(rock[3:9])}" fill="none" stroke="#ffe08a" stroke-width="10" stroke-linecap="round"/>'
    b += f'<path d="{smooth(rock[3:9])}" fill="none" stroke="#ffb050" stroke-width="28" stroke-linecap="round" opacity=".5" filter="url(#soft3)"/>'
    wave = [(x, SURF + 7 * math.sin(x / 70) + 4 * math.sin(x / 23)) for x in range(0, 1941, 20)]
    b += f'<path d="{P(wave)} L1920,{SURF + 40} L0,{SURF + 40}Z" fill="#8a4a24" opacity=".55"/>'
    b += f'<path d="{P(wave)}" fill="none" stroke="#ffb46a" stroke-width="5" opacity=".9"/>'
    # firelight shafts down into the murky water
    for i in range(6):
        x = 1100 + i * 140 + random.randint(-30, 30); w = random.randint(40, 100)
        b += f'<path d="M{x},{SURF} L{x + w},{SURF} L{x - 300 + w * 2},1080 L{x - 340},1080Z" fill="#ffb070" opacity="{random.uniform(.04, .08):.2f}"/>'
    df, bf = seafloor('#1a2a34', '#060e16', 'Efl', weeds='#0e2230')
    d += df; b += bf
    # far, sinking dim ammonites (background depth)
    for i, (x, y, r, rt) in enumerate(((1000, 420, 34, 150), (1760, 700, 46, 200), (880, 600, 26, 60))):
        da2, a2 = ammonite(f'es{i}', x, y, r, rot=rt, whorls=6, seed=40 + i, dull=.55, rim='#d89a60', body=False)
        d += da2; b += f'<g opacity=".7">{a2}</g>'
    # ash and soot falling everywhere
    for _ in range(520):
        x = random.randint(0, 1920); y = random.randint(SURF + 5, 1070)
        b += f'<circle cx="{x}" cy="{y}" r="{random.choice([1.5, 2.2, 3])}" fill="{random.choice(["#2a1c14", "#5a4434", "#c8a07a", "#e8c8a0"])}" opacity="{random.uniform(.25, .65):.2f}"/>'
    for _ in range(160):
        x = random.randint(0, 1920); y = random.randint(0, SURF)
        b += f'<circle cx="{x}" cy="{y}" r="{random.choice([1.5, 2.5])}" fill="#ffcf9a" opacity="{random.uniform(.2, .55):.2f}"/>'
    # nautilus: calm, cool glow, unharmed
    b += '<ellipse cx="1420" cy="660" rx="520" ry="400" fill="#8fe8ff" opacity=".22" filter="url(#huge)"/>'
    dn, n = nautilus2('en', 1320, 560, 300, rim='#c8f6ff', rim2='#ffb070', glow='#7fe6ff', seed=12, wave=.8, tent_len=.72)
    d += dn; b += n
    # ammonite crumbling, dust sinking down-left
    da, a = dissolve('ea', 590, 660, 265, phi=150, rot=-88, front0=-.1, n_dust=1100, spread=16, dist=(300, 620), drift=(-60, 40), seed=33)
    d += da; b += a
    b += spark(1090, 330, 14, col='#ffe6c0') + spark(1750, 420, 14, col='#d8f8ff')
    dv, bv = vignette('Evig', a=.5)
    d += dv; b += bv
    return page('#14263a', svg(d, b), TEXT, outline='#120606')


# ======================= F: dark twilight blue, bright light on the nautilus, dust rises toward the light =======================
def scene_F():
    random.seed(63)
    d = FILTERS + lin('Fsea', [(0, '#16365e'), (.4, '#0b1f3e'), (1, '#030a1a')])
    d += rad('Flight', 1300, -60, 900, [(0, '#e8fbff', .75), (.3, '#7fd8ff', .3), (1, '#3a88c8', 0)])
    d += lin('Fbeam', [(0, '#eafcff'), (1, '#9fe0ff')])
    b = '<rect width="1920" height="1080" fill="url(#Fsea)"/><rect width="1920" height="1080" fill="url(#Flight)"/>'
    # the shaft of light from above onto the nautilus
    b += '<path d="M1120,-20 L1480,-20 L1820,980 L980,980Z" fill="url(#Fbeam)" opacity=".13" filter="url(#soft)"/>'
    b += '<path d="M1220,-20 L1380,-20 L1600,900 L1150,900Z" fill="#eafcff" opacity=".10" filter="url(#soft)"/>'
    for i in range(5):
        x = 1160 + i * 70
        b += f'<path d="M{x},-20 L{x + 26},-20 L{x + 26 + (i - 2) * 140},1000 L{x + (i - 2) * 140},1000Z" fill="#eafcff" opacity=".05"/>'
    # marine snow
    for _ in range(320):
        x = random.randint(0, 1920); y = random.randint(0, 1070)
        b += f'<circle cx="{x}" cy="{y}" r="{random.choice([1.3, 2, 2.8])}" fill="#d8f2ff" opacity="{random.uniform(.12, .5):.2f}"/>'
    # reef slope (left, dark) + floor
    slope = smooth([(0, 760), (140, 820), (300, 900), (480, 960), (700, 1010), (900, 1040), (1100, 1050)]) + ' L1100,1080 L0,1080Z'
    b += f'<path d="{slope}" fill="#040c1a" stroke="#1a3a62" stroke-width="5"/>'
    for x0, y0 in ((90, 800), (260, 885), (430, 945)):
        for j in range(4):
            a = math.radians(-140 + 30 * j); L = random.randint(50, 90)
            b += f'<path d="M{x0},{y0} q{math.cos(a) * L * .3:.0f},{math.sin(a) * L * .6:.0f} {math.cos(a) * L:.0f},{math.sin(a) * L:.0f}" stroke="#0e2440" stroke-width="10" fill="none" stroke-linecap="round"/>'
    b += '<path d="M1000,1050 C1300,1030 1600,1045 1920,1030 L1920,1080 L1000,1080Z" fill="#040c1a"/>'
    # nautilus in the light: bright halo + strong rim
    b += '<ellipse cx="1420" cy="560" rx="470" ry="400" fill="#bff2ff" opacity=".35" filter="url(#huge)"/>'
    dn, n = nautilus2('fn', 1350, 400, 335, rim='#ffffff', rim2='#bff6ff', glow='#cff8ff', seed=7, wave=1.6, light=1.3, tent_len=.75)
    d += dn; b += n
    # ammonite (bottom-left) dissolving, golden dust rising up-right toward the light
    da, a = dissolve('fa', 640, 790, 275, phi=-72, rot=-30, front0=-.12, n_dust=1150, spread=13, dist=(450, 800), drift=(160, -30), seed=44,
                     glint='#fff8dc')
    d += da; b += a
    b += spark(1240, 140, 26, col='#ffffff') + spark(960, 330, 16) + spark(1820, 400, 14, col='#d8f8ff')
    dv, bv = vignette('Fvig', a=.55)
    d += dv; b += bv
    return page('#0b1f3e', svg(d, b), TEXT, outline='#050b18')


def test():
    d1, n1 = nautilus2('n', 760, 470, 380, glow='#7fd6ff')
    s = svg(FILTERS + d1, f'<rect width="1920" height="1080" fill="#1b6c80"/>' + n1)
    open(os.path.join(HERE, 'T.html'), 'w').write(page('#1b6c80', s, []))


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'test':
        test()
    else:
        for k, f in (('D', scene_D), ('E', scene_E), ('F', scene_F)):
            open(os.path.join(HERE, k + '.html'), 'w').write(f())
