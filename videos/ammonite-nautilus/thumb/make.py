# ammonite-nautilus thumbnails A-C (guideline 16-6). run: python3 make.py  (writes A.html B.html C.html here)
# A  ERASED IN A BLINK     homage: Avengers: Infinity War (2018) "the snap" - one of two look-alikes crumbles into drifting dust,
#    the other stays whole. Ammonite turns to bronze dust, the nautilus floats on intact.
#    script: "A group that had existed for more than three hundred million years was erased, in geological terms, in a blink."
# B  1 MM VS 3 CM          intuitive: a big leathery nautilus egg on a reef rock (cutaway: miniature nautilus inside) next to a
#    speck-sized ammonite hatchling, a magnifier shows the speck. script: "An ammonite hatchling was only about one millimeter
#    across. A nautilus egg is about three centimeters long."
# C  WHY DID IT SURVIVE?   intuitive: split sea - the asteroid burning the sky, the sunlit layer dark with falling ash and
#    sinking ammonites; far below, the calm twilight zone (200-700 m in the script) where the nautilus waits by the reef slope.
#    script: "In the twilight zone, the effects of the disaster were probably slower and weaker. The nautilus lived there".
import os, sys, math, random
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', '..', 'tools'))
from thumb_lib import *

TAU = math.pi * 2


def P(pts, close=False):
    return 'M' + ' L'.join(f'{x:.1f},{y:.1f}' for x, y in pts) + ('Z' if close else '')


def smooth(pts, close=False):
    """Catmull-Rom -> cubic bezier path"""
    n = len(pts)
    if n < 3:
        return P(pts, close)
    d = f'M{pts[0][0]:.1f},{pts[0][1]:.1f}'
    rng = range(n) if close else range(n - 1)
    for i in rng:
        p0 = pts[(i - 1) % n] if (close or i > 0) else pts[i]
        p1 = pts[i]; p2 = pts[(i + 1) % n]
        p3 = pts[(i + 2) % n] if (close or i + 2 < n) else p2
        c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
        d += f' C{c1[0]:.1f},{c1[1]:.1f} {c2[0]:.1f},{c2[1]:.1f} {p2[0]:.1f},{p2[1]:.1f}'
    return d + ('Z' if close else '')


def taper(pts, w0, w1):
    """filled tapered stroke along pts (width w0 at start -> w1 at end)"""
    L = []; Rr = []; n = len(pts)
    for i, (x, y) in enumerate(pts):
        a = pts[max(0, i - 1)]; b = pts[min(n - 1, i + 1)]
        dx, dy = b[0] - a[0], b[1] - a[1]; m = math.hypot(dx, dy) or 1
        nx, ny = -dy / m, dx / m; w = (w0 + (w1 - w0) * i / (n - 1)) / 2
        L.append((x + nx * w, y + ny * w)); Rr.append((x - nx * w, y - ny * w))
    return smooth(L + Rr[::-1], True)


FILTERS = ('<filter id="soft" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="22"/></filter>'
           '<filter id="soft2" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="8"/></filter>'
           '<filter id="soft3" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="3"/></filter>'
           '<filter id="huge" x="-80%" y="-80%" width="260%" height="260%"><feGaussianBlur stdDeviation="60"/></filter>')


# ---------------------------------------------------------------- nautilus (head on the right)
def nautilus(gid, cx, cy, R, rim='#bfefff', glow=None, tent_wave=0.0, seed=3, scale_tent=1.0, light=1.0):
    """chambered nautilus, side view, coil centre (cx, cy), outer radius R at the aperture. Head + tentacles to the right."""
    b = math.log(3.0) / TAU            # whorl expansion ~3x per turn
    T = math.radians(80)               # aperture ray (pointing down, a bit left), mirrored spiral -> growth to the right

    def pt(t, r=None):
        rr = R * math.exp(b * (t - T)) if r is None else r
        return (cx - rr * math.cos(t), cy + rr * math.sin(t))

    def rad_(t):
        return R * math.exp(b * (t - T))
    N = 140
    outer = [pt(T - TAU + TAU * i / N) for i in range(N + 1)]
    shell = smooth(outer) + 'Z'
    rin = rad_(T - TAU)
    d = (f'<radialGradient id="{gid}sh" cx="{cx - R * .25:.0f}" cy="{cy - R * .45:.0f}" r="{R * 1.5:.0f}" gradientUnits="userSpaceOnUse">'
         f'<stop offset="0" stop-color="#fffaf0"/><stop offset=".45" stop-color="#f3e6cf"/><stop offset=".8" stop-color="#cdb593"/>'
         f'<stop offset="1" stop-color="#8d7458"/></radialGradient>'
         f'<clipPath id="{gid}cl"><path d="{shell}"/></clipPath>'
         f'<linearGradient id="{gid}hd" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#e9b48f"/><stop offset=".6" stop-color="#c98a68"/><stop offset="1" stop-color="#8f5a44"/></linearGradient>'
         f'<linearGradient id="{gid}hood" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#9c5a3a"/><stop offset="1" stop-color="#5e3020"/></linearGradient>')
    o = ''
    if glow:
        o += f'<circle cx="{cx + R * .3:.0f}" cy="{cy:.0f}" r="{R * 1.35:.0f}" fill="{glow}" opacity=".35" filter="url(#huge)"/>'
    rnd = random.Random(seed)
    # ---- tentacles behind (back row, darker)
    ap_in = pt(T, rin); ap_out = pt(T)
    hx0 = (ap_in[0] + ap_out[0]) / 2; hy0 = (ap_in[1] + ap_out[1]) / 2
    head_c = (hx0 + R * .30, hy0 - R * .02)

    def tentacles(n, col, wid, spread, length, yoff, dark=False):
        s = ''
        for i in range(n):
            u = i / max(1, n - 1)
            ang = math.radians(-22 + spread * u) + rnd.uniform(-.06, .06)
            L = R * length * rnd.uniform(.7, 1.1) * scale_tent
            sx = head_c[0] + R * .20 + rnd.uniform(-.02, .02) * R
            sy = head_c[1] + R * (yoff + .26 * u) + rnd.uniform(-.02, .02) * R
            pts = []
            ph = rnd.uniform(0, TAU)
            for k in range(11):
                f = k / 10
                a = ang + .40 * f * math.sin(ph + f * 3.0 + tent_wave) + .12 * f
                pts.append((sx + math.cos(a) * L * f, sy + math.sin(a) * L * f))
            w = wid * R * rnd.uniform(.8, 1.15)
            s += f'<path d="{taper(pts, w + 4, w * .45 + 3)}" fill="#3a1e14" opacity=".6"/>'
            s += f'<path d="{taper(pts, w, w * .45)}" fill="{col}"/>'
            if not dark:
                hp = [(x, y - w * .22) for x, y in pts[:8]]
                s += f'<path d="{smooth(hp)}" fill="none" stroke="#ffe8d6" stroke-width="{w * .25:.1f}" stroke-linecap="round" opacity=".55"/>'
        return s
    o += tentacles(16, '#a0604a', .034, 66, .78, -.10, dark=True)
    # ---- shell
    o += f'<path d="{shell}" fill="url(#{gid}sh)" stroke="#3b2618" stroke-width="{R * .018:.1f}" stroke-linejoin="round"/>'
    # tiger stripes (older part of the whorl only; the youngest ~quarter near the aperture is plain cream)
    st = f'<g clip-path="url(#{gid}cl)">'
    nst = 17
    for i in range(nst):
        t0 = T - TAU + .25 + (TAU * .74) * i / nst + rnd.uniform(-.04, .04)
        wdt = rnd.uniform(.11, .17) * (1.0 - .45 * i / nst)
        left = []; right = []
        for k in range(13):
            f = k / 12
            r = rin * .55 + (rad_(t0) * 1.05 - rin * .55) * f
            wob = .10 * math.sin(f * 5.5 + i) * f + .22 * f   # stripes sweep backwards, wavy
            ta = t0 - wob
            ww = wdt * (0.35 + .9 * f)
            left.append(pt(ta - ww / 2, r)); right.append(pt(ta + ww / 2, r))
        st += f'<path d="{smooth(left + right[::-1], True)}" fill="#8e3b1e" opacity="{rnd.uniform(.72, .9):.2f}"/>'
    st += '</g>'
    o += st
    # growth lines + shading inside clip
    sh = f'<g clip-path="url(#{gid}cl)">'
    for i in range(36):
        t0 = T - TAU + TAU * i / 36
        ln = [pt(t0 - .2 * f, rin * .5 + (rad_(t0) * 1.05 - rin * .5) * f) for f in [k / 8 for k in range(9)]]
        sh += f'<path d="{smooth(ln)}" fill="none" stroke="#6b4a2e" stroke-width="{R * .004:.1f}" opacity=".25"/>'
    # darker underside (light comes from top-left)
    sh += f'<ellipse cx="{cx + R * .2:.0f}" cy="{cy + R * .75:.0f}" rx="{R * 1.1:.0f}" ry="{R * .55:.0f}" fill="#2a1a10" opacity=".35" filter="url(#soft)"/>'
    # pearly highlight
    sh += f'<ellipse cx="{cx - R * .35:.0f}" cy="{cy - R * .45:.0f}" rx="{R * .35:.0f}" ry="{R * .18:.0f}" fill="#ffffff" opacity="{.45 * light:.2f}" filter="url(#soft2)" transform="rotate(-30 {cx - R * .35:.0f} {cy - R * .45:.0f})"/>'
    sh += '</g>'
    o += sh
    # rim light on the outer edge (top-left arc)
    rl = [pt(t) for t in [T - TAU * .62 + TAU * .32 * k / 30 for k in range(31)]]
    o += f'<path d="{smooth(rl)}" fill="none" stroke="{rim}" stroke-width="{R * .03:.1f}" stroke-linecap="round" opacity=".8"/>'
    o += f'<path d="{smooth(rl)}" fill="none" stroke="{rim}" stroke-width="{R * .09:.1f}" stroke-linecap="round" opacity=".25" filter="url(#soft2)"/>'
    # umbilical callus
    o += f'<circle cx="{cx:.0f}" cy="{cy:.0f}" r="{R * .07:.1f}" fill="#d9c7aa" stroke="#4a3220" stroke-width="{R * .012:.1f}"/>'
    o += f'<circle cx="{cx - R * .015:.0f}" cy="{cy - R * .02:.0f}" r="{R * .03:.1f}" fill="#fff6e6" opacity=".7"/>'
    # aperture shadow lip
    o += f'<path d="M{ap_in[0]:.1f},{ap_in[1]:.1f} L{ap_out[0]:.1f},{ap_out[1]:.1f}" stroke="#2a160c" stroke-width="{R * .05:.1f}" stroke-linecap="round" opacity=".6"/>'
    # ---- head
    hx, hy = head_c
    head = smooth([(ap_in[0] - R * .02, ap_in[1] + R * .02), (hx + R * .05, hy - R * .2), (hx + R * .28, hy - R * .08),
                   (hx + R * .30, hy + R * .18), (hx + R * .10, hy + R * .33), (ap_out[0] + R * .02, ap_out[1] - R * .04),
                   (ap_out[0] - R * .03, (ap_out[1] + ap_in[1]) / 2)], True)
    # funnel (rolled tube) under the head, pointing forward-down
    fx, fy = hx + R * .02, hy + R * .30
    o += (f'<path d="M{fx - R * .10:.1f},{fy - R * .03:.1f} Q{fx + R * .04:.1f},{fy + R * .01:.1f} {fx + R * .10:.1f},{fy + R * .06:.1f} '
          f'L{fx + R * .07:.1f},{fy + R * .11:.1f} Q{fx:.1f},{fy + R * .07:.1f} {fx - R * .12:.1f},{fy + R * .05:.1f}Z" fill="#c07a5c" stroke="#3a1e14" stroke-width="{R * .012:.1f}"/>')
    
    o += f'<path d="{head}" fill="url(#{gid}hd)" stroke="#3a1e14" stroke-width="{R * .014:.1f}"/>'
    # hood: leathery cap over the top of the head, with pale blotches
    hood = smooth([(ap_in[0] - R * .06, ap_in[1] - R * .03), (hx - R * .02, hy - R * .30), (hx + R * .27, hy - R * .20),
                   (hx + R * .34, hy - R * .02), (hx + R * .18, hy - R * .06), (hx - R * .02, hy - R * .08), (ap_in[0] + R * .02, ap_in[1] + R * .08)], True)
    o += f'<path d="{hood}" fill="url(#{gid}hood)" stroke="#2a140c" stroke-width="{R * .014:.1f}"/>'
    for k in range(9):
        bx = hx - R * .05 + rnd.uniform(0, R * .32); by = hy - R * .22 + rnd.uniform(0, R * .14)
        o += f'<ellipse cx="{bx:.1f}" cy="{by:.1f}" rx="{R * rnd.uniform(.012, .028):.1f}" ry="{R * rnd.uniform(.008, .016):.1f}" fill="#f0d8c0" opacity=".55"/>'
    o += f'<path d="{smooth([(hx - R * .02, hy - R * .27), (hx + R * .15, hy - R * .25), (hx + R * .27, hy - R * .17)])}" fill="none" stroke="#e8b08c" stroke-width="{R * .015:.1f}" stroke-linecap="round" opacity=".7"/>'
    # pinhole eye (dark open pit, no lens highlight) with a soft socket
    ex, ey = hx + R * .07, hy + R * .06
    o += f'<ellipse cx="{ex:.1f}" cy="{ey:.1f}" rx="{R * .075:.1f}" ry="{R * .062:.1f}" fill="#b0705a" stroke="#5a2e20" stroke-width="{R * .01:.1f}"/>'
    o += f'<circle cx="{ex:.1f}" cy="{ey:.1f}" r="{R * .026:.1f}" fill="#120806"/>'
    # ---- front tentacles (many, thin, no suckers)
    o += tentacles(22, '#e8aa8a', .030, 72, .72, -.06)
    return d, o


# ---------------------------------------------------------------- ammonite (flat coiled ribbed disc with keel)
def ammonite(gid, cx, cy, R, rot=0, body=True, whorls=7, rim='#ffe2a8', seed=5, ribs=True, dull=0.0):
    """evolute planispiral ammonite, outer radius R; aperture at the right, head + short tentacles to the right."""
    k = 1.48                                # whorl expansion per turn
    b = math.log(k) / TAU
    T = math.radians(70)
    rmin = R / k ** whorls

    def rr(t):
        return R * math.exp(b * (t - T))

    def pt(t, r):
        return (cx - r * math.cos(t), cy + r * math.sin(t))
    t0 = T - whorls * TAU
    N = int(whorls * 90)
    ts = [t0 + (T - t0) * i / N for i in range(N + 1)]
    outer = [pt(t, rr(t)) for t in ts]
    inner_r = lambda t: rr(t) / k * 1.0
    d = (f'<radialGradient id="{gid}g" cx="{cx - R * .3:.0f}" cy="{cy - R * .4:.0f}" r="{R * 1.6:.0f}" gradientUnits="userSpaceOnUse">'
         f'<stop offset="0" stop-color="#ffd9a0"/><stop offset=".35" stop-color="#d89a58"/><stop offset=".75" stop-color="#9c6230"/>'
         f'<stop offset="1" stop-color="#4f2c12"/></radialGradient>'
         f'<linearGradient id="{gid}ir" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#9fe8ff" stop-opacity=".0"/>'
         f'<stop offset=".45" stop-color="#b9f5e6" stop-opacity=".22"/><stop offset=".55" stop-color="#f6c6ff" stop-opacity=".16"/>'
         f'<stop offset="1" stop-color="#ffe0a0" stop-opacity="0"/></linearGradient>'
         f'<linearGradient id="{gid}hd" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#e6b8a0"/><stop offset="1" stop-color="#9a6050"/></linearGradient>')
    disc = f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{R:.1f}"/>'
    whole = smooth(outer[-91:] if False else [pt(t, rr(t)) for t in [T - TAU + TAU * i / 120 for i in range(121)]]) + 'Z'
    d += f'<clipPath id="{gid}cl"><path d="{whole}"/></clipPath>'
    rnd = random.Random(seed)
    o = f'<g transform="rotate({rot} {cx:.1f} {cy:.1f})">'
    # tentacles behind
    ap_o = pt(T, R); ap_i = pt(T, R / k)
    hc = ((ap_o[0] + ap_i[0]) / 2 + R * .12, (ap_o[1] + ap_i[1]) / 2)
    if body:
        for i in range(10):
            a = math.radians(-35 + 75 * i / 9) + rnd.uniform(-.06, .06)
            L = R * rnd.uniform(.28, .42)
            sx, sy = hc[0] + R * .1, hc[1] + R * (-.08 + .18 * i / 9)
            pts = [(sx + math.cos(a + .3 * f * math.sin(i + f * 3)) * L * f, sy + math.sin(a + .3 * f * math.sin(i + f * 3)) * L * f) for f in [j / 6 for j in range(7)]]
            o += f'<path d="{smooth(pts)}" fill="none" stroke="#4a2418" stroke-width="{R * .05:.1f}" stroke-linecap="round" opacity=".6"/>'
            o += f'<path d="{smooth(pts)}" fill="none" stroke="#d99a86" stroke-width="{R * .036:.1f}" stroke-linecap="round"/>'
    # disc body
    o += f'<path d="{whole}" fill="url(#{gid}g)" stroke="#2e1708" stroke-width="{R * .018:.1f}"/>'
    g = f'<g clip-path="url(#{gid}cl)">'
    # whorl seams (each earlier whorl's outer edge) + shadow below each seam
    for w in range(1, whorls + 1):
        seg = [pt(t, rr(t) / k ** w) for t in [T - TAU + TAU * i / 100 for i in range(101)]]
        g += f'<path d="{smooth(seg)}" fill="none" stroke="#2e1708" stroke-width="{max(1.5, R * .03 / w ** .5):.1f}" opacity=".85"/>'
        g += f'<path d="{smooth(seg)}" fill="none" stroke="#fff0c8" stroke-width="{max(1, R * .008 / w ** .3):.1f}" opacity=".5" transform="translate({-R * .006:.1f} {-R * .008:.1f})"/>'
    # ribs: radial, slightly curved, across each whorl band
    if ribs:
        for w in range(0, whorls):
            n = max(10, int(46 - w * 4))
            for i in range(n):
                t = T - TAU + TAU * (i + .5) / n
                r1 = rr(t) / k ** w; r0 = r1 / k
                if r1 < R * .04:
                    continue
                pts = [pt(t + .10 * (f - .5) ** 2 - .05 * f, r0 + (r1 - r0) * f) for f in [j / 6 for j in range(7)]]
                g += f'<path d="{smooth(pts)}" fill="none" stroke="#5a3214" stroke-width="{max(1.2, (r1 - r0) * .07):.1f}" stroke-linecap="round" opacity=".7"/>'
                g += f'<path d="{smooth(pts)}" fill="none" stroke="#ffe0b0" stroke-width="{max(.8, (r1 - r0) * .03):.1f}" stroke-linecap="round" opacity=".5" transform="translate({-(r1 - r0) * .04:.1f} {-(r1 - r0) * .05:.1f})"/>'
    # iridescent pearly sheen + shadow
    g += f'<rect x="{cx - R:.0f}" y="{cy - R:.0f}" width="{2 * R:.0f}" height="{2 * R:.0f}" fill="url(#{gid}ir)"/>'
    g += f'<ellipse cx="{cx + R * .3:.0f}" cy="{cy + R * .7:.0f}" rx="{R:.0f}" ry="{R * .5:.0f}" fill="#1a0c04" opacity=".35" filter="url(#soft)"/>'
    if dull:
        g += f'<rect x="{cx - R:.0f}" y="{cy - R:.0f}" width="{2 * R:.0f}" height="{2 * R:.0f}" fill="#2a2420" opacity="{dull:.2f}"/>'
    g += '</g>'
    o += g
    # keel: a ridge along the outer edge
    kl = [pt(t, rr(t) * 1.0) for t in [T - TAU + TAU * i / 120 for i in range(121)]]
    o += f'<path d="{smooth(kl)}" fill="none" stroke="#3a1c08" stroke-width="{R * .045:.1f}" opacity=".9"/>'
    o += f'<path d="{smooth(kl)}" fill="none" stroke="#f0b870" stroke-width="{R * .018:.1f}" opacity=".9"/>'
    rl = [pt(t, rr(t) * .995) for t in [T - TAU * .62 + TAU * .3 * i / 30 for i in range(31)]]
    o += f'<path d="{smooth(rl)}" fill="none" stroke="{rim}" stroke-width="{R * .022:.1f}" stroke-linecap="round" opacity=".9"/>'
    # head with two large round eyes
    if body:
        hx, hy = hc
        o += f'<path d="{smooth([ap_i, (hx + R * .05, hy - R * .16), (hx + R * .2, hy - R * .02), (hx + R * .14, hy + R * .14), ap_o], True)}" fill="url(#{gid}hd)" stroke="#3a1e14" stroke-width="{R * .014:.1f}"/>'
        ex, ey = hx + R * .06, hy - R * .03
        o += f'<circle cx="{ex:.1f}" cy="{ey:.1f}" r="{R * .07:.1f}" fill="#f8f0e0" stroke="#3a1e14" stroke-width="{R * .01:.1f}"/>'
        o += f'<circle cx="{ex + R * .015:.1f}" cy="{ey + R * .005:.1f}" r="{R * .04:.1f}" fill="#1a0c08"/>'
        o += f'<circle cx="{ex + R * .028:.1f}" cy="{ey - R * .012:.1f}" r="{R * .013:.1f}" fill="#ffffff"/>'
    o += '</g>'
    return d, o


# ======================= A: ERASED IN A BLINK  (homage: Avengers: Infinity War, "the snap" - one look-alike turns to dust) =======================
def scene_A():
    random.seed(11)
    W, H = 1920, 1080
    d = FILTERS + lin('Asea', [(0, '#3fa3b2'), (.35, '#1b6c80'), (.7, '#0c3a4c'), (1, '#061e2a')])
    d += rad('Asun', 1500, -80, 900, [(0, '#fff2c4', .85), (.35, '#ffd27a', .35), (1, '#ffd27a', 0)])
    d += lin('Afloor', [(0, '#123848'), (1, '#04131b')])
    b = f'<rect width="{W}" height="{H}" fill="url(#Asea)"/><rect width="{W}" height="{H}" fill="url(#Asun)"/>'
    # surface caustic shimmer near the top
    for i in range(26):
        y = random.randint(8, 150); x = random.randint(600, 1920); L = random.randint(60, 200)
        b += f'<path d="M{x},{y} q{L / 4:.0f},{-10} {L / 2:.0f},0 t{L / 2:.0f},0" fill="none" stroke="#fff4d0" stroke-width="{random.choice([2, 3, 4])}" opacity="{random.uniform(.15, .4):.2f}"/>'
    # distant reef / sea-floor silhouettes (background depth)
    fl = [(0, 1000), (200, 975), (420, 990), (650, 960), (900, 985), (1150, 970), (1400, 990), (1650, 975), (1920, 995), (1920, 1080), (0, 1080)]
    b += f'<path d="{smooth(fl[:9])} L1920,1080 L0,1080Z" fill="url(#Afloor)" opacity=".9"/>'
    for x0 in (1050, 1120, 1720):   # sea lilies
        hh = random.randint(110, 170)
        b += f'<path d="M{x0},985 q{random.randint(-20, 20)},{-hh / 2:.0f} {random.randint(-10, 30)},{-hh}" stroke="#0a2c3a" stroke-width="7" fill="none"/>'
        b += f'<circle cx="{x0 + 10}" cy="{985 - hh}" r="16" fill="#0a2c3a"/>'
    # floating motes
    b += stars(70, 1000, col='#d8fbff', op=.35, sparks=0)
    # ---------- nautilus (intact, glowing)
    dn, n = nautilus('n', 1290, 455, 285, rim='#fff1c0', glow='#9ff0ff', seed=4)
    d += dn
    b += f'<ellipse cx="1420" cy="560" rx="520" ry="420" fill="#a8f4ff" opacity=".22" filter="url(#huge)"/>'
    b += n
    # ---------- ammonite crumbling into dust (left part gone, turning into drifting bronze flakes)
    cx, cy, R = 690, 770, 255
    da, a = ammonite('am', cx, cy, R, seed=7, rot=-62)
    d += da
    rnd = random.Random(21)

    def front(y):   # x of the dissolve front at height y (jagged)
        return cx - R * .12 + R * .22 * math.sin((y - cy) / R * 2.2) + rnd.uniform(-1, 1) * R * .05
    m = f'<mask id="Adust" maskUnits="userSpaceOnUse" x="0" y="0" width="1920" height="1080"><rect width="1920" height="1080" fill="#fff"/>'
    pts = []
    for k in range(41):
        y = cy - R * 1.15 + R * 2.3 * k / 40
        pts.append((front(y), y))
    m += f'<path d="{P(pts)} L-10,{cy + R * 1.2:.0f} L-10,{cy - R * 1.2:.0f}Z" fill="#000"/>'
    holes = ''
    for _ in range(260):   # holes eating into the shell just right of the front
        y = rnd.uniform(cy - R, cy + R); fx = front(y)
        x = fx + abs(rnd.gauss(0, R * .14))
        s_ = rnd.uniform(4, 15)
        holes += f'<rect x="{x:.1f}" y="{y:.1f}" width="{s_:.1f}" height="{s_ * rnd.uniform(.5, 1.2):.1f}" fill="#000" transform="rotate({rnd.uniform(0, 90):.0f} {x:.1f} {y:.1f})"/>'
    m += holes
    for _ in range(90):    # islands of shell still hanging on left of the front
        y = rnd.uniform(cy - R, cy + R); fx = front(y)
        x = fx - abs(rnd.gauss(0, R * .10))
        s_ = rnd.uniform(5, 16)
        m += f'<rect x="{x:.1f}" y="{y:.1f}" width="{s_:.1f}" height="{s_ * .8:.1f}" fill="#fff" transform="rotate({rnd.uniform(0, 90):.0f} {x:.1f} {y:.1f})"/>'
    m += '</mask>'
    d += m
    b += f'<ellipse cx="{cx}" cy="{cy}" rx="{R * 1.2:.0f}" ry="{R:.0f}" fill="#ffcf86" opacity=".18" filter="url(#huge)"/>'
    b += f'<g mask="url(#Adust)">{a}</g>'
    # glowing ember edge along the front
    for k in range(60):
        y = cy - R * .95 + R * 1.9 * k / 59
        x = front(y)
        if (x - cx) ** 2 + (y - cy) ** 2 < (R * .98) ** 2:
            b += f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{rnd.uniform(3, 7):.1f}" fill="#ffd98a" opacity="{rnd.uniform(.4, .85):.2f}"/>'
    # dust flakes drifting up-left in streams
    cols = ['#c88a4a', '#a8682e', '#e0aa62', '#7a4a22', '#f2d27a', '#5a3418']
    for _ in range(900):
        y0 = rnd.uniform(cy - R * .95, cy + R * .95)
        x0 = front(y0) - rnd.uniform(0, R * .3)
        if (x0 - cx) ** 2 + (y0 - cy) ** 2 > R ** 2:
            continue
        t = rnd.random() ** 1.6                 # travel fraction
        dist = t * rnd.uniform(500, 900)
        ang = math.radians(rnd.uniform(195, 222))
        x = x0 + math.cos(ang) * dist + math.sin(t * 6 + y0) * 30 * t
        y = y0 + math.sin(ang) * dist - 120 * t * t
        if x < -20 or y < -20:
            continue
        s_ = rnd.uniform(3, 13) * (1 - .6 * t)
        op = (1 - t) * .95 + .05
        b += f'<rect x="{x:.1f}" y="{y:.1f}" width="{s_:.1f}" height="{s_ * rnd.uniform(.5, 1):.1f}" fill="{rnd.choice(cols)}" opacity="{op:.2f}" transform="rotate({rnd.uniform(0, 90):.0f} {x:.1f} {y:.1f})"/>'
    for _ in range(40):    # a few glinting flakes
        t = rnd.uniform(.05, .6); y0 = rnd.uniform(cy - R * .8, cy + R * .8); x0 = front(y0)
        ang = math.radians(rnd.uniform(195, 222)); dist = t * 700
        x = x0 + math.cos(ang) * dist; y = y0 + math.sin(ang) * dist - 120 * t * t
        b += f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{rnd.uniform(2, 4):.1f}" fill="#fff3c8" opacity=".9"/><circle cx="{x:.1f}" cy="{y:.1f}" r="10" fill="#ffe6a0" opacity=".25" filter="url(#soft3)"/>'
    b += spark(1560, 260, 22) + spark(985, 395, 16) + spark(1745, 470, 14)
    # vignette
    d += rad('Avig', 960, 540, 1150, [(0, '#000', 0), (.7, '#000', 0), (1, '#000', .45)])
    b += f'<rect width="{W}" height="{H}" fill="url(#Avig)"/>'
    return page('#0c3a4c', svg(d, b), [('ERASED', 182, 'w'), ('IN A', 112, 'w'), ('BLINK', 206, 'y')], outline='#06161e')


# ======================= B: 1 MM VS 3 CM  (intuitive: huge nautilus egg vs a speck-sized ammonite hatchling) =======================
def scene_B():
    random.seed(22)
    W, H = 1920, 1080
    d = FILTERS + lin('Bsea', [(0, '#1d4f6a'), (.5, '#0f3048'), (1, '#071826')])
    d += rad('Bglow', 1240, 520, 620, [(0, '#ffcf7a', .55), (.4, '#ff9a4a', .18), (1, '#ff9a4a', 0)])
    d += lin('Brock', [(0, '#4a5560'), (.4, '#2c343c'), (1, '#10161c')])
    d += lin('Begg', [(0, '#fbf5ea'), (.5, '#e9dcc6'), (1, '#b7a486')], x2=1, y2=1)
    d += rad('Binside', 1250, 560, 300, [(0, '#ffe3a0', 1), (.55, '#f2a85a', 1), (1, '#9a5226', 1)])
    b = f'<rect width="{W}" height="{H}" fill="url(#Bsea)"/>'
    # light from upper left (soft beam of water light), plankton motes
    b += f'<ellipse cx="700" cy="-100" rx="900" ry="500" fill="#7fc8e0" opacity=".25" filter="url(#huge)"/>'
    b += stars(110, 1060, col='#cdf3ff', op=.35, sparks=0)
    # background reef slope silhouettes (depth)
    b += f'<path d="M0,900 C300,860 500,880 760,840 C1000,800 1300,840 1500,820 C1700,800 1850,830 1920,820 L1920,1080 L0,1080Z" fill="#0a1c28"/>'
    # foreground rock the egg is attached to
    rock = smooth([(820, 1080), (860, 900), (960, 830), (1120, 800), (1300, 790), (1480, 815), (1600, 870), (1680, 960), (1720, 1080)], False) + ' L820,1080Z'
    b += f'<path d="{rock}" fill="url(#Brock)" stroke="#0a0f14" stroke-width="5"/>'
    for i in range(30):   # rock texture
        x = random.randint(900, 1650); y = random.randint(840, 1060)
        b += f'<ellipse cx="{x}" cy="{y}" rx="{random.randint(8, 30)}" ry="{random.randint(4, 12)}" fill="#5c6872" opacity="{random.uniform(.15, .35):.2f}"/>'
    b += f'<path d="M960,832 C1100,800 1300,786 1480,812" stroke="#8fb4c8" stroke-width="6" fill="none" opacity=".45"/>'
    for x0, y0, sc, col in ((1560, 860, 1.0, '#1c3a44'), (880, 905, .8, '#163038'), (120, 930, 1.2, '#0e2632'), (300, 960, .8, '#0e2632')):
        for j in range(5):   # branching coral fans
            a = math.radians(-150 + 30 * j)
            L = 120 * sc * random.uniform(.7, 1.1)
            b += f'<path d="M{x0},{y0} q{math.cos(a) * L * .3:.0f},{math.sin(a) * L * .6:.0f} {math.cos(a) * L:.0f},{math.sin(a) * L:.0f}" stroke="{col}" stroke-width="{14 * sc:.0f}" fill="none" stroke-linecap="round"/>'
            b += f'<circle cx="{x0 + math.cos(a) * L:.0f}" cy="{y0 + math.sin(a) * L:.0f}" r="{12 * sc:.0f}" fill="{col}"/>'
    # warm glow of the egg
    b += f'<rect width="{W}" height="{H}" fill="url(#Bglow)"/>'
    # ---- the egg (oval, leathery, folded capsule), tilted, base attached to rock
    b += '<ellipse cx="1260" cy="520" rx="360" ry="420" fill="#ffc36a" opacity=".38" filter="url(#huge)"/>'
    ex, ey, rx, ry, rot = 1250, 520, 255, 330, 18
    eggp = f'<ellipse cx="{ex}" cy="{ey}" rx="{rx}" ry="{ry}"/>'
    d += f'<clipPath id="Begc"><ellipse cx="{ex}" cy="{ey}" rx="{rx}" ry="{ry}" transform="rotate({rot} {ex} {ey})"/></clipPath>'
    g = f'<g transform="rotate({rot} {ex} {ey})">'
    g += f'<ellipse cx="{ex + 10}" cy="{ey + 20}" rx="{rx + 10}" ry="{ry + 10}" fill="#000" opacity=".35" filter="url(#soft2)"/>'
    # attachment foot at the base (glued to the rock), drawn under the egg
    g += f'<path d="M{ex - 95},{ey + ry - 60} C{ex - 120},{ey + ry + 55} {ex + 120},{ey + ry + 55} {ex + 95},{ey + ry - 60}Z" fill="#cdbb98" stroke="#4a3a26" stroke-width="6"/>'
    g += f'<ellipse cx="{ex}" cy="{ey}" rx="{rx}" ry="{ry}" fill="url(#Begg)" stroke="#4a3a26" stroke-width="7"/>'
    g += '</g>'
    b += g
    # leathery folds (clipped)
    folds = '<g clip-path="url(#Begc)">'
    for i in range(9):
        off = -rx + 2 * rx * (i + .5) / 9
        folds += (f'<path d="M{ex + off:.0f},{ey - ry - 20} C{ex + off * .6 + 30:.0f},{ey - ry * .3:.0f} {ex + off * 1.2 - 30:.0f},{ey + ry * .3:.0f} {ex + off * .8:.0f},{ey + ry + 20}" '
                  f'fill="none" stroke="#a89070" stroke-width="5" opacity=".45" transform="rotate({rot} {ex} {ey})"/>')
    folds += '</g>'
    b += folds
    # cutaway window: ragged peeled opening showing the curled miniature nautilus
    wx, wy, wr = ex + 10, ey + 5, 170
    rag = []
    rnd = random.Random(5)
    for k in range(48):
        a = TAU * k / 48
        r = wr * (1 + .10 * math.sin(a * 5) + rnd.uniform(-.05, .05))
        rag.append((wx + math.cos(a) * r, wy + math.sin(a) * r * 1.12))
    d += f'<clipPath id="Bwin"><path d="{smooth(rag, True)}"/></clipPath>'
    b += f'<path d="{smooth(rag, True)}" fill="#3a2414" stroke="#f6eedc" stroke-width="16" stroke-linejoin="round"/>'
    b += f'<path d="{smooth(rag, True)}" fill="url(#Binside)"/>'
    dn, n = nautilus('bn', wx - 25, wy - 50, 132, rim='#fff6d8', seed=8, scale_tent=.65, tent_wave=1.4)
    d += dn
    b += f'<g clip-path="url(#Bwin)">{n}'
    b += f'<ellipse cx="{wx - 60}" cy="{wy - 110}" rx="90" ry="40" fill="#fff" opacity=".22" filter="url(#soft2)"/>'
    for _ in range(14):   # tiny yolk droplets
        b += f'<circle cx="{wx + rnd.uniform(-150, 150):.0f}" cy="{wy + rnd.uniform(-170, 170):.0f}" r="{rnd.uniform(3, 8):.1f}" fill="#fff3c8" opacity=".55"/>'
    b += '</g>'
    # inner shadow ring of the window + curled torn flaps
    b += f'<path d="{smooth(rag, True)}" fill="none" stroke="#5a3a1c" stroke-width="5" opacity=".7"/>'
    # egg rim light (top-left) + specular
    b += f'<g clip-path="url(#Begc)"><ellipse cx="{ex - 40}" cy="{ey - 40}" rx="{rx}" ry="{ry}" fill="none" stroke="#ffffff" stroke-width="26" opacity=".35" filter="url(#soft3)" transform="rotate({rot} {ex} {ey})"/>'
    b += f'<ellipse cx="{ex + 60}" cy="{ey + 60}" rx="{rx}" ry="{ry}" fill="none" stroke="#5a4428" stroke-width="40" opacity=".35" filter="url(#soft2)" transform="rotate({rot} {ex} {ey})"/></g>'
    b += f'<ellipse cx="{ex - 120}" cy="{ey - 230}" rx="60" ry="26" fill="#fff" opacity=".6" filter="url(#soft3)" transform="rotate(-30 {ex - 120} {ey - 230})"/>'
    # ---- the ammonite hatchling: a speck beside the egg, and a magnifier lens showing it
    sx, sy = 905, 640
    b += f'<circle cx="{sx}" cy="{sy}" r="34" fill="#ffe6a0" opacity=".4" filter="url(#soft3)"/>'
    b += f'<circle cx="{sx}" cy="{sy}" r="9" fill="#f6d79a" stroke="#5a3a1a" stroke-width="2"/><circle cx="{sx - 1}" cy="{sy}" r="3.5" fill="#8a5a2a"/>'
    lx, ly, lr = 560, 790, 175
    # dashed callout lines from the speck to the lens
    for a in (-.9, .9):
        b += f'<path d="M{sx},{sy} L{lx + math.cos(-.6 + a * .9) * lr:.0f},{ly + math.sin(-.6 + a * .9) * lr:.0f}" stroke="#d8f6ff" stroke-width="4" stroke-dasharray="12 10" opacity=".55"/>'
    d += f'<clipPath id="Blens"><circle cx="{lx}" cy="{ly}" r="{lr - 12}"/></clipPath>'
    d += rad('Blensbg', lx - 40, ly - 60, lr * 1.4, [(0, '#5ec2d8', 1), (1, '#0e3a52', 1)])
    b += f'<circle cx="{lx + 12}" cy="{ly + 16}" r="{lr + 14}" fill="#000" opacity=".35" filter="url(#soft2)"/>'
    b += f'<circle cx="{lx}" cy="{ly}" r="{lr}" fill="url(#Blensbg)"/>'
    da, a = ammonite('ba', lx - 20, ly + 5, 92, rot=-60, whorls=3, seed=9)
    d += da
    lens_in = f'<g clip-path="url(#Blens)">'
    for _ in range(26):
        lens_in += f'<circle cx="{lx + rnd.uniform(-160, 160):.0f}" cy="{ly + rnd.uniform(-160, 160):.0f}" r="{rnd.uniform(3, 9):.1f}" fill="#bff3e0" opacity="{rnd.uniform(.25, .6):.2f}"/>'
    lens_in += a + f'<ellipse cx="{lx - 60}" cy="{ly - 95}" rx="80" ry="34" fill="#fff" opacity=".35" filter="url(#soft3)" transform="rotate(-25 {lx - 60} {ly - 95})"/></g>'
    b += lens_in
    b += f'<circle cx="{lx}" cy="{ly}" r="{lr}" fill="none" stroke="#1b1208" stroke-width="30"/>'
    b += f'<circle cx="{lx}" cy="{ly}" r="{lr}" fill="none" stroke="#d9a24a" stroke-width="20"/>'
    b += f'<circle cx="{lx}" cy="{ly}" r="{lr - 6}" fill="none" stroke="#ffe6a8" stroke-width="5" opacity=".8" stroke-dasharray="300 900" stroke-dashoffset="-560"/>'
    b += spark(1530, 250, 24) + spark(1010, 300, 16) + spark(1600, 700, 14) + spark(sx + 30, sy - 30, 14)
    d += rad('Bvig', 960, 540, 1150, [(0, '#000', 0), (.65, '#000', 0), (1, '#000', .5)])
    b += f'<rect width="{W}" height="{H}" fill="url(#Bvig)"/>'
    return page('#0f3048', svg(d, b), [('1 MM', 196, 'w'), ('VS', 118, 'w'), ('3 CM', 216, 'y')], outline='#06121c')


# ======================= C: WHY DID IT SURVIVE?  (intuitive: burning sunlit layer above, calm twilight zone below) =======================
def scene_C():
    random.seed(33)
    W, H = 1920, 1080
    SURF = 330
    d = FILTERS + lin('Csky', [(0, '#2a0c10'), (.5, '#7a2414'), (1, '#e0672a')])
    d += lin('Cup', [(0, '#6a4a2c'), (.5, '#3c3428'), (1, '#1a2a34')])
    d += lin('Cdeep', [(0, '#10283e'), (.5, '#0a1a30'), (1, '#050c1a')])
    d += rad('Cfire', 1560, 150, 520, [(0, '#fff2b0', 1), (.12, '#ffc35a', .9), (.4, '#ff6a20', .35), (1, '#ff4a10', 0)])
    d += rad('Cblue', 880, 800, 420, [(0, '#8fe8ff', .55), (.5, '#3aa8d8', .18), (1, '#3aa8d8', 0)])
    b = f'<rect width="{W}" height="{SURF + 20}" fill="url(#Csky)"/>'
    b += f'<rect width="{W}" height="{H}" y="{SURF}" fill="url(#Cdeep)"/>'
    b += f'<rect width="{W}" height="300" y="{SURF}" fill="url(#Cup)"/>'
    # soft fade between the murky sunlit layer and the deep (the layers stay distinct)
    d += '<linearGradient id="Cfade" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#1a2a34" stop-opacity="0"/><stop offset=".5" stop-color="#14263a" stop-opacity=".9"/><stop offset="1" stop-color="#10283e" stop-opacity="0"/></linearGradient>'
    b += f'<rect width="{W}" height="140" y="{SURF + 230}" fill="url(#Cfade)"/>'
    # smoke clouds along the horizon
    for _ in range(40):
        x = random.randint(-100, 1900); y = random.randint(150, 320); r = random.randint(50, 130)
        b += f'<ellipse cx="{x}" cy="{y}" rx="{r * 1.6:.0f}" ry="{r * .7:.0f}" fill="{random.choice(["#1e0c0a", "#2c1210", "#3a1a12"])}" opacity="{random.uniform(.4, .8):.2f}"/>'
    # distant wildfire glow on the horizon (right)
    b += f'<ellipse cx="1500" cy="{SURF}" rx="520" ry="60" fill="#ff7a2a" opacity=".55" filter="url(#soft)"/>'
    # asteroid with fiery trail coming from upper right
    b += f'<rect width="{W}" height="{SURF}" fill="url(#Cfire)"/>'
    ax, ay = 1530, 165
    for k in range(10):
        t = k / 9
        b += f'<path d="M{ax},{ay} L{ax + 520 - 40 * t:.0f},{ay - 330 + 30 * t:.0f}" stroke="{["#fff3c0", "#ffc760", "#ff8a30", "#c84a18"][k % 4]}" stroke-width="{90 - 70 * t:.0f}" stroke-linecap="round" opacity="{.18 + .1 * (1 - t):.2f}" filter="url(#soft2)"/>'
    b += f'<path d="M{ax - 40},{ay + 5} L{ax + 560},{ay - 360} L{ax + 590},{ay - 320}Z" fill="#ffb24a" opacity=".55" filter="url(#soft2)"/>'
    b += f'<circle cx="{ax}" cy="{ay}" r="120" fill="#ffd27a" opacity=".55" filter="url(#soft)"/>'
    rock = [(ax + 52 * math.cos(a) * random.uniform(.85, 1.1), ay + 46 * math.sin(a) * random.uniform(.85, 1.1)) for a in [TAU * i / 14 for i in range(14)]]
    b += f'<path d="{smooth(rock, True)}" fill="#3a2418" stroke="#1a0c08" stroke-width="5"/>'
    b += f'<path d="{smooth(rock[3:9])}" fill="none" stroke="#ffe08a" stroke-width="11" stroke-linecap="round"/>'
    b += f'<path d="{smooth(rock[3:9])}" fill="none" stroke="#ffb050" stroke-width="30" stroke-linecap="round" opacity=".5" filter="url(#soft3)"/>'
    for _ in range(6):
        b += f'<circle cx="{ax + random.randint(-30, 20)}" cy="{ay + random.randint(-15, 25)}" r="{random.randint(5, 10)}" fill="#24140c" opacity=".7"/>'
    # sea surface (wavy line + glare)
    wave = [(x, SURF + 8 * math.sin(x / 70) + 4 * math.sin(x / 23)) for x in range(0, 1941, 20)]
    b += f'<path d="{P(wave)} L1920,{SURF + 40} L0,{SURF + 40}Z" fill="#8a4a24" opacity=".6"/>'
    b += f'<path d="{P(wave)}" fill="none" stroke="#ffb46a" stroke-width="5" opacity=".9"/>'
    # ash and soot falling through the sunlit layer
    for _ in range(420):
        x = random.randint(0, 1920); y = random.randint(SURF + 10, SURF + 330)
        b += f'<circle cx="{x}" cy="{y}" r="{random.choice([1.5, 2.2, 3])}" fill="{random.choice(["#2a1c14", "#5a4434", "#c8a07a"])}" opacity="{random.uniform(.3, .7):.2f}"/>'
    for _ in range(140):   # ash in the sky
        x = random.randint(0, 1920); y = random.randint(0, SURF)
        b += f'<circle cx="{x}" cy="{y}" r="{random.choice([1.5, 2.5])}" fill="#ffcf9a" opacity="{random.uniform(.2, .55):.2f}"/>'
    # sinking ammonites (dimmed silhouettes, tilted) in the sunlit layer
    for i, (x, y, r, rt) in enumerate(((1090, 470, 62, 150), (1400, 555, 84, 200), (1760, 450, 54, 120), (1240, 395, 38, 60))):
        da, a = ammonite(f'cs{i}', x, y, r, rot=rt, whorls=6, seed=40 + i, dull=.5, rim='#d89a60', body=False)
        d += da
        b += f'<g opacity=".85">{a}</g>'
        b += f'<path d="M{x},{y - r - 10} l0,-40 M{x - 20},{y - r - 6} l-4,-30 M{x + 20},{y - r - 6} l4,-30" stroke="#d8c0a0" stroke-width="3" opacity=".35" stroke-linecap="round"/>'
    # ---------- twilight zone below: calm, marine snow, reef slope, the nautilus
    for _ in range(260):
        x = random.randint(0, 1920); y = random.randint(SURF + 320, 1080)
        b += f'<circle cx="{x}" cy="{y}" r="{random.choice([1.4, 2, 2.8])}" fill="#d8f2ff" opacity="{random.uniform(.15, .55):.2f}"/>'
    slope = smooth([(0, 700), (140, 760), (260, 860), (420, 930), (560, 990), (700, 1040), (760, 1080)]) + ' L0,1080Z'
    b += f'<path d="{slope}" fill="#071222" stroke="#1f4a6a" stroke-width="5"/>'
    for x0, y0 in ((120, 760), (300, 880), (480, 960)):
        for j in range(4):
            a = math.radians(-140 + 30 * j); L = random.randint(50, 90)
            b += f'<path d="M{x0},{y0} q{math.cos(a) * L * .3:.0f},{math.sin(a) * L * .6:.0f} {math.cos(a) * L:.0f},{math.sin(a) * L:.0f}" stroke="#12304a" stroke-width="10" fill="none" stroke-linecap="round"/>'
    b += f'<rect width="{W}" height="{H}" fill="url(#Cblue)"/>'
    dn, n = nautilus('cn', 830, 760, 212, rim='#c8f6ff', glow='#7fe6ff', seed=12, tent_wave=.8)
    d += dn
    b += n
    b += spark(640, 650, 18, col='#d8f8ff') + spark(1240, 720, 14, col='#d8f8ff') + spark(1010, 980, 12, col='#d8f8ff')
    d += rad('Cvig', 960, 600, 1200, [(0, '#000', 0), (.65, '#000', 0), (1, '#000', .5)])
    b += f'<rect width="{W}" height="{H}" fill="url(#Cvig)"/>'
    return page('#0a1a30', svg(d, b), [('WHY DID IT', 128, 'w'), ('SURVIVE?', 206, 'y')], outline='#120606')


def test():
    random.seed(1)
    d1, n1 = nautilus('n', 700, 520, 330, glow='#7fd6ff')
    d2, a1 = ammonite('a', 1450, 560, 300)
    s = svg(FILTERS + d1 + d2, f'<rect width="1920" height="1080" fill="#0b3a4a"/>' + n1 + a1)
    open(os.path.join(HERE, 'T.html'), 'w').write(page('#0b3a4a', s, []))


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'test':
        test()
    else:
        for k, f in (('A', scene_A), ('B', scene_B), ('C', scene_C)):
            open(os.path.join(HERE, k + '.html'), 'w').write(f())
