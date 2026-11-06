# Shorts thumbnails (guideline 16-9, one A.html per short) for holographic-universe-short1..5.
# Run: python3 videos/holographic-universe-short1/thumb/make_shorts.py [1 2 3 4 5]  -> videos/holographic-universe-shortN/thumb/A.html
# Reuses the posable notebook frog, filters and sphere helpers of the long-form generator (videos/holographic-universe/thumb/make.py).
# short1  FLAT, YET DEEP        the frog reaches INTO a credit card's hologram sticker that opens like a deep window (S05-S07, S14)
# short2  LOST FOREVER?         a library shelf tumbles into a black-hole whirlpool, burning books stream in (S04, S10-S13)
# short3  IT'S ALL ON THE WALLS a house whose furniture is all stuck on its outer walls and roof, rooms empty (S08, S12)
# short4  TWO BOOKS, SAME STORY two open books: gravity pop-up planet vs flat quantum lattice, gold thread links them (S07-S10)
# short5  IS SPACE WOVEN?       a glowing knitted fabric of linked threads holds a planet; the frog knits it from a yarn ball (S09-S10)
import os, sys, math, random, importlib.util
HERE = os.path.dirname(os.path.abspath(__file__))
VID = os.path.abspath(os.path.join(HERE, '..', '..'))
sys.path.insert(0, os.path.join(VID, '..', 'tools'))
from thumb_lib import page, svg, lin, rad, spark
_spec = importlib.util.spec_from_file_location('hu_long', os.path.join(VID, 'holographic-universe', 'thumb', 'make.py'))
L = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(L)
frog, FILTERS, poly, INK, GREEN = L.frog, L.FILTERS, L.poly, L.INK, L.GREEN


def quad(pts, **kw):
    a = ' '.join(f'{k.replace("_", "-")}="{v}"' for k, v in kw.items())
    return f'<path d="{poly(pts)}" {a}/>'


def bil(TL, TR, BR, BL):
    def at(u, v):
        t = (TL[0] + (TR[0] - TL[0]) * u, TL[1] + (TR[1] - TL[1]) * u)
        bt = (BL[0] + (BR[0] - BL[0]) * u, BL[1] + (BR[1] - BL[1]) * u)
        return (t[0] + (bt[0] - t[0]) * v, t[1] + (bt[1] - t[1]) * v)
    return at


def stars(rnd, n, x0=0, x1=1920, y0=0, y1=1080, col='#eef4ff'):
    return ''.join(f'<circle cx="{rnd.uniform(x0, x1):.0f}" cy="{rnd.uniform(y0, y1):.0f}" r="{rnd.choice([1.2, 1.8, 2.5])}" fill="{col}" '
                   f'opacity="{rnd.uniform(.2, .8):.2f}"/>' for _ in range(n))


# ======================= short1: the sticker window =======================
def make_1():
    rnd = random.Random(3)
    d = FILTERS
    d += rad('bg1', 1300, 420, 1300, [(0, '#1f5262', 1), (.45, '#0e2632', 1), (1, '#04090d', 1)])
    d += rad('lamp1', 1780, 60, 760, [(0, '#ffc07a', .5), (1, '#ffc07a', 0)])
    d += lin('desk1', [(0, '#3d2618'), (1, '#0f0805')])
    d += lin('card1', [(0, '#22607a'), (.5, '#123b52'), (1, '#0a1f30')], x2=1, y2=1)
    d += lin('rb1', [(0, '#ff6ad5'), (.2, '#ffb26b'), (.4, '#fff38a'), (.6, '#6bffb8'), (.8, '#6bc8ff'), (1, '#b46bff')], x2=1, y2=1)
    d += lin('sky1', [(0, '#160c3a'), (.55, '#4a2a7a'), (1, '#ff9a7a')])
    d += rad('vig1', 1200, 520, 1250, [(0, '#000', 0), (.62, '#000', 0), (1, '#000', .7)])
    d += rad('pl1', 0, 0, 1, [(0, '#fff6d8', 1), (.5, '#ffd27a', 1), (1, '#e0783a', 1)])
    b = '<rect width="1920" height="1080" fill="url(#bg1)"/><rect width="1920" height="1080" fill="url(#lamp1)"/>'
    for _ in range(22):
        b += f'<circle cx="{rnd.uniform(800, 1900):.0f}" cy="{rnd.uniform(20, 300):.0f}" r="{rnd.uniform(12, 40):.0f}" fill="{rnd.choice(["#ffd88a", "#9be8ff", "#ff9be8"])}" opacity="{rnd.uniform(.05, .16):.2f}" filter="url(#b6)"/>'
    HY = 870
    b += f'<rect y="{HY}" width="1920" height="{1080 - HY}" fill="url(#desk1)"/><rect y="{HY - 2}" width="1920" height="3" fill="#ffd0a0" opacity=".25"/>'
    for i in range(7):
        y = HY + 16 + i * i * 4.5
        b += f'<path d="M0 {y:.0f} Q960 {y + 6:.0f} 1920 {y - 4:.0f}" stroke="#55331f" stroke-width="2" fill="none" opacity=".5"/>'
    # card leaning back on the desk
    TL, TR, BR, BL = (800, 318), (1690, 292), (1728, 852), (772, 872)
    at = bil(TL, TR, BR, BL)
    b += f'<path d="{poly([(BL[0] + 30, BL[1]), (BR[0] + 40, BR[1]), (BR[0] + 120, BR[1] + 40), (BL[0] + 80, BL[1] + 46)])}" fill="#000" opacity=".55" filter="url(#b12)"/>'
    b += quad([BL, BR, (BR[0] + 2, BR[1] + 14), (BL[0] + 2, BL[1] + 14)], fill='#071119', stroke='#02060a', stroke_width='3')
    b += quad([TR, BR, (BR[0] + 12, BR[1] + 12), (TR[0] + 12, TR[1] + 10)], fill='#0b1b26', stroke='#02060a', stroke_width='3')
    b += quad([TL, TR, BR, BL], fill='url(#card1)', stroke='#02060a', stroke_width='5', stroke_linejoin='round')
    b += quad([at(0, .45), at(.28, 0), at(.42, 0), at(.1, 1), at(0, 1)], fill='#fff', opacity='.06')
    b += f'<path d="M{TL[0] + 8} {TL[1] + 3} L{TR[0] - 8} {TR[1] + 3}" stroke="#a8e6ff" stroke-width="3" opacity=".6"/>'
    chip = [at(.07, .3), at(.2, .3), at(.2, .55), at(.07, .55)]
    b += quad(chip, fill='#e2b85a', stroke='#6a4a14', stroke_width='3')
    for v in (.38, .47):
        p0, p1 = at(.07, v), at(.2, v); b += f'<path d="M{p0[0]:.0f} {p0[1]:.0f} L{p1[0]:.0f} {p1[1]:.0f}" stroke="#8a6420" stroke-width="2.4"/>'
    p0, p1 = at(.135, .3), at(.135, .55); b += f'<path d="M{p0[0]:.0f} {p0[1]:.0f} L{p1[0]:.0f} {p1[1]:.0f}" stroke="#8a6420" stroke-width="2.4"/>'
    for g in range(3):
        for k in range(4):
            x, y = at(.07 + g * .12 + k * .025, .78); b += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="5" fill="#cfe6f2" opacity=".75"/>'
    p0, p1 = at(.07, .9), at(.3, .9); b += f'<path d="M{p0[0]:.0f} {p0[1]:.0f} L{p1[0]:.0f} {p1[1]:.0f}" stroke="#cfe6f2" stroke-width="7" stroke-linecap="round" opacity=".4"/>'
    # ---- the sticker opens like a deep window ----
    O = [at(.47, .12), at(.93, .12), at(.93, .84), at(.47, .84)]
    Cx = sum(p[0] for p in O) / 4 + 30; Cy = sum(p[1] for p in O) / 4 - 20
    k = .5
    I = [(Cx + (x - Cx) * k, Cy + (y - Cy) * k) for x, y in O]
    d += f'<clipPath id="win1"><path d="{poly(O)}"/></clipPath><clipPath id="inn1"><path d="{poly(I)}"/></clipPath>'
    w = f'<path d="{poly(O)}" fill="#0a0820"/>'
    walls = [((O[0], O[1], I[1], I[0]), '#7a5ac8', .9), ((O[1], O[2], I[2], I[1]), '#3a6ab8', .8), ((O[2], O[3], I[3], I[2]), '#2a1a5a', .9), ((O[3], O[0], I[0], I[3]), '#5a2a8a', .9)]
    for pts, col, op in walls:
        w += quad(pts, fill=col, opacity=op)
        for t in (.2, .4, .6, .8):   # diffraction stripes running into the depth
            a = (pts[0][0] + (pts[1][0] - pts[0][0]) * t, pts[0][1] + (pts[1][1] - pts[0][1]) * t)
            c = (pts[3][0] + (pts[2][0] - pts[3][0]) * t, pts[3][1] + (pts[2][1] - pts[3][1]) * t)
            w += f'<path d="M{a[0]:.0f} {a[1]:.0f} L{c[0]:.0f} {c[1]:.0f}" stroke="url(#rb1)" stroke-width="5" opacity=".55"/>'
        for t in (.3, .6, .85):      # depth rings
            q = [(p[0] + (r[0] - p[0]) * t, p[1] + (r[1] - p[1]) * t) for p, r in zip(O, I)]
            w += f'<path d="{poly(q)}" fill="none" stroke="#e8f8ff" stroke-width="{3 - 2 * t:.1f}" opacity="{.35 - .2 * t:.2f}"/>'
    # far landscape inside the inner opening
    ix0, iy0 = min(p[0] for p in I), min(p[1] for p in I); ix1, iy1 = max(p[0] for p in I), max(p[1] for p in I)
    sc = f'<rect x="{ix0 - 5:.0f}" y="{iy0 - 5:.0f}" width="{ix1 - ix0 + 10:.0f}" height="{iy1 - iy0 + 10:.0f}" fill="url(#sky1)"/>'
    sc += stars(rnd, 50, ix0, ix1, iy0, iy0 + (iy1 - iy0) * .55)
    px, py = ix0 + (ix1 - ix0) * .62, iy0 + (iy1 - iy0) * .36
    sc += f'<circle cx="{px:.0f}" cy="{py:.0f}" r="60" fill="#ffd27a" opacity=".45" filter="url(#b12)"/>'
    sc += f'<circle cx="{px:.0f}" cy="{py:.0f}" r="30" fill="#ffe4a0" stroke="#fff6d8" stroke-width="2"/><circle cx="{px + 8:.0f}" cy="{py + 8:.0f}" r="26" fill="#e0783a" opacity=".35"/>'
    hz = iy0 + (iy1 - iy0) * .66
    mt = f'M{ix0 - 5:.0f} {hz:.0f}'
    x = ix0 - 5
    while x < ix1 + 10:
        x += rnd.uniform(18, 34); mt += f' L{x:.0f} {hz - rnd.uniform(6, 40):.0f}'
    sc += f'<path d="{mt} L{ix1 + 10:.0f} {iy1 + 10:.0f} L{ix0 - 5:.0f} {iy1 + 10:.0f}Z" fill="#2a1848"/>'
    sc += f'<rect x="{ix0 - 5:.0f}" y="{hz:.0f}" width="{ix1 - ix0 + 10:.0f}" height="{iy1 - hz + 10:.0f}" fill="#120a26"/>'
    vx = (ix0 + ix1) / 2
    for kx in range(-8, 9):
        sc += f'<line x1="{vx + kx * 6:.0f}" y1="{hz:.0f}" x2="{vx + kx * 60:.0f}" y2="{iy1 + 10:.0f}" stroke="#7fe0ff" stroke-width="1.5" opacity=".45"/>'
    yy, st_ = hz, 3
    while yy < iy1 + 10:
        sc += f'<line x1="{ix0 - 5:.0f}" y1="{yy:.0f}" x2="{ix1 + 10:.0f}" y2="{yy:.0f}" stroke="#7fe0ff" stroke-width="1.5" opacity=".4"/>'; st_ *= 1.5; yy += st_
    sc += f'<rect x="{ix0 - 5:.0f}" y="{hz - 3:.0f}" width="{ix1 - ix0 + 10:.0f}" height="5" fill="#ffd0e0" opacity=".6" filter="url(#b3)"/>'
    w += f'<g clip-path="url(#inn1)">{sc}</g>'
    w += f'<path d="{poly(I)}" fill="none" stroke="#fff" stroke-width="2" opacity=".5"/>'
    b += f'<path d="{poly(O)}" fill="none" stroke="#c8f0ff" stroke-width="40" opacity=".35" filter="url(#b24)"/>'
    b += f'<g clip-path="url(#win1)">{w}</g>'
    b += f'<path d="{poly(O)}" fill="none" stroke="url(#rb1)" stroke-width="16" stroke-linejoin="round"/>'
    b += f'<path d="{poly(O)}" fill="none" stroke="#02060a" stroke-width="3" stroke-linejoin="round"/>'
    for _ in range(36):
        t = rnd.random(); e = rnd.choice([0, 1, 2, 3]); p, q = O[e], O[(e + 1) % 4]
        x, y = p[0] + (q[0] - p[0]) * t + rnd.uniform(-30, 30), p[1] + (q[1] - p[1]) * t + rnd.uniform(-30, 30)
        b += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{rnd.uniform(1.5, 4):.1f}" fill="#fffbe8" opacity="{rnd.uniform(.4, .9):.2f}"/>'
    # ---- frog reaching into the window ----
    fx, fy, fs = 1120, 1010, 3.1
    hx, hy = 1300, 735
    lx, ly = (hx - fx) / fs, (hy - fy) / fs
    arm = f'M38 -24 q{(lx - 38) * .25:.1f} {(ly + 24) * .75:.1f} {lx - 38:.1f} {ly + 24:.1f}'
    for r, op in ((26, .8), (44, .45), (64, .25)):
        b += f'<ellipse cx="{hx}" cy="{hy}" rx="{r}" ry="{r * .7:.0f}" fill="none" stroke="#c8f0ff" stroke-width="3" opacity="{op}"/>'
    b += f'<ellipse cx="{fx + 10}" cy="{fy + 6}" rx="130" ry="16" fill="#000" opacity=".5" filter="url(#b3)"/>'
    b += f'<circle cx="{fx}" cy="{fy - 130}" r="170" fill="#bff0ff" opacity=".1" filter="url(#b24)"/>'
    b += frog(fx, fy, fs, look=(8, -4), mouth='O', armR=arm, armL='M-34 -22 q-22 4 -26 26',
              legs=((-20, -6, -26, 4, -8), (20, -6, 26, 4, 8)))
    b += f'<circle cx="{hx}" cy="{hy}" r="40" fill="#e8fbff" opacity=".5" filter="url(#b12)"/>'
    b += spark(hx + 40, hy - 50, 20) + spark(1500, 200, 22, '#e8fbff') + spark(1760, 560, 18) + spark(880, 760, 16, '#e8fbff')
    b += '<rect width="1920" height="1080" fill="url(#vig1)"/>'
    lines = [('FLAT,', 214, 'w'), ('YET', 128, 'w'), ('DEEP', 236, 'y')]
    return page('#0e2632', svg(d, b), lines, outline='#03090d', top=40)


# ======================= short2: the library falls in =======================
def make_2():
    rnd = random.Random(8)
    d = FILTERS
    d += rad('bg2', 1380, 620, 1300, [(0, '#3a1030', 1), (.45, '#160818', 1), (1, '#05030a', 1)])
    d += rad('neb2a', 1650, 220, 600, [(0, '#5a3aff', .28), (1, '#5a3aff', 0)])
    d += rad('core2', 1380, 620, 240, [(0, '#000', 1), (.55, '#000', 1), (1, '#000', 0)])
    d += rad('vig2', 1200, 520, 1250, [(0, '#000', 0), (.6, '#000', 0), (1, '#000', .75)])
    d += rad('fade2', 1380, 620, 700, [(0, '#fff', 1), (.7, '#fff', 1), (1, '#fff', 0)])
    d += '<mask id="m2"><rect width="1920" height="1080" fill="url(#fade2)"/></mask>'
    d += '<linearGradient id="fl2" x1="0" y1="1" x2="0" y2="0"><stop offset="0" stop-color="#ffec9a"/><stop offset=".45" stop-color="#ff8a2a"/><stop offset="1" stop-color="#ff3a1a" stop-opacity="0"/></linearGradient>'
    b = '<rect width="1920" height="1080" fill="url(#bg2)"/><rect width="1920" height="1080" fill="url(#neb2a)"/>' + stars(rnd, 230)
    CX, CY, SQ, ROT = 1380, 620, .5, -14
    cr, sr = math.cos(math.radians(ROT)), math.sin(math.radians(ROT))

    def sp(r, th):
        x, y = r * math.cos(th), r * math.sin(th) * SQ
        return CX + x * cr - y * sr, CY + x * sr + y * cr

    # whirlpool arms
    arms = ''
    for a in range(7):
        ph = a * 2 * math.pi / 7
        for layer, (wmul, op, blur, col) in enumerate(((3.2, .22, 12, '#ff6a3a'), (1.6, .5, 3, '#ffb04a'), (.6, .9, 0, '#fff0c8'))):
            pts = []
            for i in range(140):
                th = ph + i * .05
                r = 680 * math.exp(-.12 * i * .05 * 6)
                if r < 128:
                    break
                pts.append((sp(r, -th), r))
            for j in range(len(pts) - 1):
                (p, r), (q, _) = pts[j], pts[j + 1]
                wdt = (4 + 24 * (1 - r / 680)) * wmul
                o = op * min(1, (680 - r) / 180)
                f_ = f' filter="url(#b{blur})"' if blur else ''
                arms += f'<path d="M{p[0]:.0f} {p[1]:.0f} L{q[0]:.0f} {q[1]:.0f}" stroke="{col}" stroke-width="{wdt:.1f}" stroke-linecap="round" opacity="{o:.2f}"{f_}/>'
    b += f'<g mask="url(#m2)">{arms}</g>'
    b += f'<ellipse cx="{CX}" cy="{CY}" rx="330" ry="200" transform="rotate({ROT} {CX} {CY})" fill="#ffcf7a" opacity=".25" filter="url(#b24)"/>'
    b += f'<circle cx="{CX}" cy="{CY}" r="240" fill="url(#core2)"/>'
    b += f'<circle cx="{CX}" cy="{CY}" r="150" fill="#000"/>'
    b += f'<circle cx="{CX}" cy="{CY}" r="154" fill="none" stroke="#fff2c8" stroke-width="5" opacity=".9"/>'
    b += f'<circle cx="{CX}" cy="{CY}" r="160" fill="none" stroke="#ffb04a" stroke-width="16" opacity=".45" filter="url(#b6)"/>'

    def book(x, y, w, h, rot, col, fire=False, stretch=1.0):
        o = f'<g transform="translate({x:.0f} {y:.0f}) rotate({rot:.0f}) scale({stretch:.2f} 1)" stroke="#1a0a08" stroke-width="3.2" stroke-linejoin="round">'
        o += f'<rect x="{-w / 2:.0f}" y="{-h / 2:.0f}" width="{w:.0f}" height="{h:.0f}" rx="4" fill="{col}"/>'
        o += f'<rect x="{w / 2 - 7:.0f}" y="{-h / 2 + 4:.0f}" width="6" height="{h - 8:.0f}" fill="#fff4dc" stroke-width="1.6"/>'
        o += f'<path d="M{-w / 2 + 6:.0f} {-h / 2 + h * .2:.0f} H{w / 2 - 12:.0f} M{-w / 2 + 6:.0f} {h / 2 - h * .2:.0f} H{w / 2 - 12:.0f}" stroke="#f2d27a" stroke-width="2.4"/>'
        o += f'<path d="M{-w / 2 + 4:.0f} {-h / 2 + 4:.0f} V{h / 2 - 4:.0f}" stroke="#fff" stroke-width="2.4" opacity=".35"/>'
        o += '</g>'
        if fire:
            fh = h * 1.3
            o += (f'<g transform="translate({x:.0f} {y - h * .3:.0f})"><ellipse cx="0" cy="{-fh * .3:.0f}" rx="{w * .9:.0f}" ry="{fh * .7:.0f}" fill="#ff7a2a" opacity=".35" filter="url(#b12)"/>'
                  f'<path d="M{-w * .45:.0f} 0 Q{-w * .5:.0f} {-fh * .5:.0f} {-w * .1:.0f} {-fh:.0f} Q{-w * .05:.0f} {-fh * .55:.0f} {w * .15:.0f} {-fh * .7:.0f} Q{w * .3:.0f} {-fh * .4:.0f} {w * .2:.0f} {-fh * .85:.0f} Q{w * .55:.0f} {-fh * .45:.0f} {w * .45:.0f} 0Z" fill="url(#fl2)" stroke="none"/></g>')
        return o

    cols = ['#b23a3a', '#3a6ab2', '#3a8a5a', '#c88a2a', '#7a3a9a', '#2a7a8a', '#d0603a']
    # shelf tumbling in (upper right)
    SX, SY = 1700, 215
    sh = f'<g transform="translate({SX} {SY}) rotate(32)" stroke="#1a0a08" stroke-width="4" stroke-linejoin="round">'
    sh += '<ellipse cx="0" cy="0" rx="200" ry="220" fill="#ffb04a" opacity=".18" filter="url(#b24)" stroke="none"/>'
    sh += '<rect x="-120" y="-150" width="240" height="300" rx="6" fill="#6a3a22"/><rect x="-104" y="-136" width="208" height="272" fill="#2a140c"/>'
    for row, y0 in enumerate((-136, -46, 44)):
        x = -100
        while x < 90:
            wdt = rnd.choice([16, 18, 22, 26]); hh = rnd.choice([70, 76, 82])
            if rnd.random() < (.75 if row else .45):
                sh += f'<rect x="{x}" y="{y0 + 88 - hh}" width="{wdt}" height="{hh}" fill="{rnd.choice(cols)}" stroke-width="2.4"/>'
                sh += f'<path d="M{x + 3} {y0 + 88 - hh + 12} h{wdt - 6}" stroke="#f2d27a" stroke-width="2"/>'
            x += wdt + 2
        sh += f'<rect x="-104" y="{y0 + 86}" width="208" height="8" fill="#8a5232" stroke-width="2.4"/>'
    sh += '<path d="M-118 -146 L118 -146" stroke="#c88a5a" stroke-width="3" opacity=".7"/></g>'
    # books streaming from the shelf toward the core along a spiral
    stream = ''
    for i in range(16):
        t = i / 15
        r = 600 * (1 - t) + 170 * t
        th = -0.95 - t * 2.3
        x, y = sp(r, th)
        x += (1 - t) * 60; y -= (1 - t) * 20
        s = 1 - .65 * t
        stream += book(x, y, 58 * s, 80 * s, rnd.uniform(-60, 60), rnd.choice(cols), fire=(i % 3 == 1), stretch=1 + .9 * t)
        for _ in range(3):
            stream += f'<path transform="translate({x + rnd.uniform(-70, 70):.0f} {y + rnd.uniform(-60, 60):.0f}) rotate({rnd.uniform(0, 90):.0f})" d="M-9 -6 L9 -8 L10 6 L-8 8Z" fill="#fff4dc" opacity="{.5 + .4 * (1 - t):.2f}" stroke="#3a2010" stroke-width="1.2"/>'
    embers = ''.join(f'<circle cx="{rnd.uniform(1100, 1850):.0f}" cy="{rnd.uniform(120, 760):.0f}" r="{rnd.uniform(2, 5):.1f}" fill="{rnd.choice(["#ffd27a", "#ff8a3a", "#fff0c8"])}" opacity="{rnd.uniform(.4, .9):.2f}"/>' for _ in range(60))
    b += embers + sh + stream
    # frog riding a flying open book, astronaut helmet
    fx, fy, fs = 820, 900, 2.35
    ob = (f'<g transform="translate({fx} {fy + 20}) rotate(-8)" stroke="#1a0a08" stroke-width="4" stroke-linejoin="round">'
          '<path d="M-170 6 Q-90 -26 0 4 Q90 -26 170 6 L176 30 Q90 4 0 34 Q-90 4 -176 30Z" fill="#7a2a2a"/>'
          '<path d="M-160 0 Q-86 -30 0 -2 L0 22 Q-86 -6 -164 20Z" fill="#fff4dc"/><path d="M160 0 Q86 -30 0 -2 L0 22 Q86 -6 164 20Z" fill="#f2e2c0"/>'
          '<path d="M-140 -2 Q-80 -22 -20 -2 M-140 8 Q-80 -12 -20 8 M140 -2 Q80 -22 20 -2 M140 8 Q80 -12 20 8" fill="none" stroke="#b8a07a" stroke-width="2.4"/></g>')
    b += f'<ellipse cx="{fx}" cy="{fy - 100}" rx="230" ry="200" fill="#ffb04a" opacity=".12" filter="url(#b50)"/>'
    b += ''.join(f'<path d="M{fx - 180 - k * 40} {fy + 30 + k * 18} q-60 10 -120 0" stroke="#ffe8c0" stroke-width="{5 - k}" fill="none" opacity="{.5 - k * .1:.2f}" stroke-linecap="round"/>' for k in range(4))
    b += ob
    suit = ('<path d="M-38 -20 Q-46 0 -40 8 L44 8 Q50 0 42 -20 Q4 -30 -38 -20Z" fill="#eef0f4" stroke-width="3.4"/>'
            '<rect x="-14" y="-14" width="30" height="16" rx="4" fill="#9aa6b8" stroke-width="2.6"/><circle cx="-6" cy="-6" r="3" fill="#ff6a6a" stroke="none"/>')
    helm = ('<circle cx="6" cy="-58" r="48" fill="#bfe6ff" fill-opacity=".16" stroke="#e8eef6" stroke-width="5"/>'
            '<path d="M-28 -84 q12 -18 34 -22" fill="none" stroke="#fff" stroke-width="5" opacity=".85"/>'
            '<path d="M40 -86 q8 6 10 18" fill="none" stroke="#ffb04a" stroke-width="4" opacity=".8"/>')
    b += frog(fx - 10, fy + 6, fs, rot=-8, look=(9, -3), mouth='O', mid=suit, front=helm,
              armL='M-34 -22 q-24 2 -40 22', armR='M38 -22 q26 -14 40 -44', legs=((-20, -6, -28, 4, -10), (20, -6, 28, 4, 10)))
    b += spark(CX - 240, CY - 330, 24) + spark(1820, 520, 18, '#ffe8c8') + spark(1060, 820, 16)
    b += '<rect width="1920" height="1080" fill="url(#vig2)"/>'
    lines = [('LOST', 236, 'y'), ('FOREVER?', 164, 'w')]
    return page('#160818', svg(d, b), lines, outline='#07030c', top=40)


# ======================= short3: the furniture on the outer walls =======================
def make_3():
    rnd = random.Random(5)
    d = FILTERS
    d += lin('sky3', [(0, '#1c2a6a'), (.5, '#5a3e8e'), (.82, '#d97a7a'), (1, '#f6b27a')])
    d += lin('hill3', [(0, '#3a6a3e'), (1, '#122a18')])
    d += lin('front3', [(0, '#f6e2b8'), (1, '#c9a878')])
    d += lin('side3', [(0, '#b8916a'), (1, '#7a5a40')])
    d += rad('glow3', 1390, 560, 700, [(0, '#ffd8a0', .45), (1, '#ffd8a0', 0)])
    d += rad('vig3', 1200, 520, 1250, [(0, '#000', 0), (.62, '#000', 0), (1, '#000', .6)])
    b = '<rect width="1920" height="1080" fill="url(#sky3)"/>' + stars(rnd, 90, 0, 1920, 0, 420, '#fff6e8')
    b += '<circle cx="1760" cy="150" r="56" fill="#fff4d8"/><circle cx="1782" cy="138" r="50" fill="#5a3e8e" opacity=".9"/><circle cx="1760" cy="150" r="110" fill="#fff4d8" opacity=".15" filter="url(#b24)"/>'
    b += '<path d="M0 800 Q500 740 900 790 T1920 770 V1080 H0Z" fill="#2c4a5a" opacity=".6"/>'
    b += '<rect width="1920" height="1080" fill="url(#glow3)"/>'
    b += '<path d="M0 880 Q600 820 1100 850 Q1500 870 1920 830 V1080 H0Z" fill="url(#hill3)"/>'
    for _ in range(80):
        x = rnd.uniform(0, 1920); y = rnd.uniform(860, 1060)
        b += f'<path d="M{x:.0f} {y:.0f} l-4 -14 M{x:.0f} {y:.0f} l5 -12" stroke="#5a8a4a" stroke-width="2.4" opacity=".6"/>'
    OL = '#2a1810'
    # house geometry
    F = [(1060, 500), (1500, 500), (1500, 862), (1060, 862)]
    S = [(1500, 500), (1730, 444), (1730, 808), (1500, 862)]
    b += '<ellipse cx="1400" cy="868" rx="420" ry="26" fill="#000" opacity=".35" filter="url(#b12)"/>'
    b += quad(S, fill='url(#side3)', stroke=OL, stroke_width='5')
    for k in range(1, 9):
        y0 = 500 + k * 40; y1 = 444 + k * 40
        b += f'<path d="M1500 {y0} L1730 {y1}" stroke="#6a4a32" stroke-width="2.4" opacity=".5"/>'
    b += quad(F, fill='url(#front3)', stroke=OL, stroke_width='5')
    for y in range(540, 862, 40):
        b += f'<path d="M1060 {y} H1500" stroke="#c09a6a" stroke-width="2.4" opacity=".55"/>'
    # roof
    b += quad([(1280, 268), (1500, 212), (1756, 448), (1522, 508)], fill='#8a3a30', stroke=OL, stroke_width='5')
    for k in range(1, 7):
        t = k / 7
        a = (1280 + (1522 - 1280) * t, 268 + (508 - 268) * t); c = (1500 + (1756 - 1500) * t, 212 + (448 - 212) * t)
        b += f'<path d="M{a[0]:.0f} {a[1]:.0f} L{c[0]:.0f} {c[1]:.0f}" stroke="#5a2018" stroke-width="3" opacity=".6"/>'
    b += quad([(1036, 508), (1280, 262), (1524, 508)], fill='#e9d3a6', stroke=OL, stroke_width='5')
    b += f'<path d="M1028 514 L1280 252 L1532 514" fill="none" stroke="#a8463a" stroke-width="22" stroke-linejoin="round"/><path d="M1028 514 L1280 252 L1532 514" fill="none" stroke="{OL}" stroke-width="4" stroke-linejoin="round" transform="translate(0 -11)"/>'
    b += f'<rect x="1600" y="230" width="44" height="90" fill="#7a3a30" stroke="{OL}" stroke-width="4" transform="skewY(-14)" transform-origin="1600 300"/>'
    # windows: empty rooms inside (bare bulb, nothing else)
    for wx in (1100, 1350):
        b += f'<rect x="{wx}" y="560" width="110" height="120" rx="4" fill="#2a2030" stroke="{OL}" stroke-width="5"/>'
        b += f'<path d="M{wx + 4} 652 L{wx + 106} 652" stroke="#4a3a40" stroke-width="3"/><path d="M{wx + 55} 564 V600" stroke="#8a8070" stroke-width="2"/>'
        b += f'<circle cx="{wx + 55}" cy="606" r="7" fill="#ffe8a0"/><circle cx="{wx + 55}" cy="606" r="26" fill="#ffe8a0" opacity=".25" filter="url(#b6)"/>'
        b += f'<path d="M{wx + 55} 560 V680 M{wx} 620 H{wx + 110}" stroke="{OL}" stroke-width="4"/>'
    b += f'<rect x="1500" y="540" width="0" height="0"/>'
    b += f'<path d="M1244 862 V740 Q1244 724 1260 724 H1300 Q1316 724 1316 740 V862Z" fill="#6a3a2a" stroke="{OL}" stroke-width="5"/><circle cx="1302" cy="796" r="5" fill="#f2d27a"/>'
    # ---- furniture stuck on the OUTSIDE ----
    def nail(x, y):
        return f'<circle cx="{x}" cy="{y}" r="4" fill="#c8c8d0" stroke="{OL}" stroke-width="2"/>'
    fur = ''
    # sofa hung sideways on the front wall, left of the door
    fur += (f'<g transform="translate(1150 790) rotate(-6)" stroke="{OL}" stroke-width="4" stroke-linejoin="round">'
            '<rect x="-80" y="-44" width="160" height="50" rx="14" fill="#c8463a"/><rect x="-86" y="-16" width="172" height="40" rx="12" fill="#e05a4a"/>'
            '<rect x="-96" y="-30" width="24" height="56" rx="10" fill="#b23a30"/><rect x="72" y="-30" width="24" height="56" rx="10" fill="#b23a30"/>'
            '<path d="M-60 24 v10 M60 24 v10" stroke-width="5"/><path d="M-70 -36 H70" stroke="#ff9a8a" stroke-width="3" opacity=".7"/></g>')
    fur += nail(1080, 760) + nail(1220, 752)
    # wall clock + framed picture above the windows
    fur += f'<circle cx="1280" cy="440" r="38" fill="#fff8e8" stroke="{OL}" stroke-width="5"/><path d="M1280 440 V414 M1280 440 L1298 450" stroke="{OL}" stroke-width="4" stroke-linecap="round"/>'
    fur += (f'<g transform="translate(1155 530) rotate(-4)"><rect x="-46" y="-24" width="92" height="44" fill="#e2b85a" stroke="{OL}" stroke-width="4"/>'
            f'<rect x="-36" y="-15" width="72" height="27" fill="#6ab0d8"/><path d="M-36 12 L-12 -6 L6 8 L20 -2 L36 12Z" fill="#3a8a5a"/></g>')
    fur += f'<g transform="translate(1405 528) rotate(5)"><rect x="-40" y="-22" width="80" height="40" rx="4" fill="#3a6ab2" stroke="{OL}" stroke-width="4"/><path d="M-30 -10 H30 M-30 2 H18" stroke="#cfe6ff" stroke-width="4"/></g>'
    # floor lamp lying flat across the right of the front wall, lit
    fur += (f'<g transform="translate(1420 800) rotate(-80)" stroke="{OL}" stroke-width="4"><path d="M0 0 V-120" stroke-width="7"/><ellipse cx="0" cy="2" rx="24" ry="8" fill="#5a4a3a"/>'
            '<path d="M-30 -120 L-20 -160 L20 -160 L30 -120Z" fill="#f6d27a"/></g><circle cx="1576" cy="772" r="40" fill="#ffe8a0" opacity=".3" filter="url(#b12)"/>')
    fur += nail(1420, 790)
    # side wall: a bookcase and a chair, in perspective (skewed)
    fur += (f'<g transform="translate(1530 500) skewY(-13.7)" stroke="{OL}" stroke-width="4"><rect x="0" y="40" width="96" height="170" fill="#8a5232"/>'
            '<rect x="8" y="48" width="80" height="154" fill="#3a2014"/>'
            + ''.join(f'<rect x="{10 + i * 13}" y="{56 + r * 52}" width="11" height="42" fill="{c}" stroke-width="2"/>' for r in range(3) for i, c in enumerate(["#b23a3a", "#3a6ab2", "#e2b85a", "#3a8a5a", "#7a3a9a", "#2a7a8a"]))
            + ''.join(f'<rect x="8" y="{98 + r * 52}" width="80" height="6" fill="#a8683a" stroke-width="2"/>' for r in range(3))
            + '</g>')
    fur += (f'<g transform="translate(1640 540) skewY(-13.7) rotate(12)" stroke="{OL}" stroke-width="4" stroke-linejoin="round"><rect x="0" y="0" width="56" height="70" rx="6" fill="#3a8a7a"/>'
            '<rect x="-6" y="62" width="68" height="18" rx="6" fill="#4aa08a"/><path d="M4 80 v40 M52 80 v40" stroke-width="6"/></g>')
    # a bed lying on the roof slope
    fur += (f'<g transform="translate(1520 330) rotate(42)" stroke="{OL}" stroke-width="4" stroke-linejoin="round"><rect x="-70" y="-22" width="150" height="40" rx="8" fill="#f4f0ff"/>'
            '<rect x="-84" y="-40" width="18" height="64" rx="5" fill="#8a5232"/><rect x="78" y="-28" width="16" height="52" rx="5" fill="#8a5232"/>'
            '<rect x="-60" y="-16" width="36" height="22" rx="8" fill="#fff"/><path d="M-20 -22 H80 V18 H-20Z" fill="#6a8ad8"/></g>')
    # a potted plant on the chimney side
    fur += f'<g transform="translate(1690 420)" stroke="{OL}" stroke-width="3.4"><path d="M-16 0 L16 0 L12 26 L-12 26Z" fill="#c8683a"/><path d="M0 0 q-18 -30 -6 -50 M0 0 q14 -28 4 -54 M0 0 q26 -14 22 -36" fill="none" stroke="#3a8a3a" stroke-width="7"/></g>'
    b += fur
    # glowing bits along the outer walls (information on the boundary)
    for _ in range(40):
        e = rnd.choice([0, 1, 2])
        if e == 0:
            x, y = 1060 + rnd.uniform(-8, 8), rnd.uniform(500, 860)
        elif e == 1:
            t = rnd.random(); x, y = 1730 + rnd.uniform(-8, 8), 444 + 364 * t
        else:
            t = rnd.random(); x, y = 1036 + 244 * t, 508 - 246 * t
        s = rnd.choice([6, 8, 10])
        b += f'<rect x="{x:.0f}" y="{y:.0f}" width="{s}" height="{s}" fill="{rnd.choice(["#f2d27a", "#9ff0ff", "#ffb0d0"])}" opacity="{rnd.uniform(.5, .95):.2f}"/>'
    # ---- frog on the grass, lifting a chair up to the wall ----
    fx, fy, fs = 900, 1000, 2.6
    chair = ('<g transform="translate(6 -128) rotate(-12)" stroke-width="3"><rect x="-26" y="-12" width="52" height="12" rx="3" fill="#e2b85a"/>'
             '<path d="M-22 0 v24 M22 0 v24" stroke-width="5"/><rect x="-24" y="-44" width="8" height="34" fill="#c89a3a"/><rect x="16" y="-44" width="8" height="34" fill="#c89a3a"/>'
             '<rect x="-26" y="-52" width="52" height="12" rx="4" fill="#e2b85a"/></g>')
    b += f'<ellipse cx="{fx + 6}" cy="{fy + 6}" rx="120" ry="15" fill="#000" opacity=".4" filter="url(#b3)"/>'
    b += f'<circle cx="{fx}" cy="{fy - 160}" r="170" fill="#ffe8c0" opacity=".12" filter="url(#b24)"/>'
    b += frog(fx, fy, fs, look=(9, -7), mouth='O', armL='M-34 -26 q-14 -30 2 -84', armR='M38 -26 q16 -30 6 -86', front=chair, brows=True)
    b += ''.join(f'<path d="M{fx + 120 + k * 22} {fy - 360 - k * 6} q8 -12 0 -24" stroke="#fff" stroke-width="5" fill="none" stroke-linecap="round" opacity=".8"/>' for k in range(2))
    b += spark(1300, 180, 22) + spark(980, 720, 16, '#fff6e8') + spark(1700, 640, 18)
    b += '<rect width="1920" height="1080" fill="url(#vig3)"/>'
    lines = [("IT'S ALL", 146, 'w'), ('ON THE', 146, 'w'), ('WALLS', 222, 'y')]
    return page('#1c2a6a', svg(d, b), lines, outline='#0e0a24', top=40)


# ======================= short4: two books, one story =======================
def make_4():
    rnd = random.Random(14)
    d = FILTERS
    d += rad('bg4', 1380, 420, 1300, [(0, '#1f4e4a', 1), (.45, '#0e2624', 1), (1, '#040b0a', 1)])
    d += rad('lamp4', 1380, 120, 800, [(0, '#ffd08a', .4), (1, '#ffd08a', 0)])
    d += lin('desk4', [(0, '#4a2c1a'), (1, '#120a06')])
    d += rad('planet4', 1090, 430, 90, [(0, '#fff0c0', 1), (.35, '#f2b25a', 1), (1, '#9a4a1a', 1)])
    d += rad('vig4', 1200, 520, 1250, [(0, '#000', 0), (.62, '#000', 0), (1, '#000', .7)])
    b = '<rect width="1920" height="1080" fill="url(#bg4)"/>'
    # blurred library shelves in the back
    sh = ''
    for row in range(5):
        y = 40 + row * 150; x = 0
        while x < 1920:
            w = rnd.choice([18, 22, 28, 34]); h = rnd.choice([90, 104, 118])
            sh += f'<rect x="{x}" y="{y + 130 - h}" width="{w}" height="{h}" fill="{rnd.choice(["#5a2a2a", "#2a4a6a", "#5a4a2a", "#2a5a3a", "#4a2a5a"])}"/>'
            x += w + 3
        sh += f'<rect x="0" y="{y + 130}" width="1920" height="14" fill="#2a160c"/>'
    b += f'<g opacity=".32" filter="url(#b6)">{sh}</g>'
    b += '<rect width="1920" height="1080" fill="url(#lamp4)"/>'
    b += '<path d="M0 0 H1000 Q960 380 760 560 Q480 640 0 610Z" fill="#040b0a" opacity=".55" filter="url(#b50)"/>'
    HY = 790
    b += f'<rect y="{HY}" width="1920" height="{1080 - HY}" fill="url(#desk4)"/><rect y="{HY - 2}" width="1920" height="3" fill="#ffd8a0" opacity=".25"/>'
    OL = '#1a0e08'

    def openbook(cx, y0, y1, w, cover, glow):
        o = f'<ellipse cx="{cx}" cy="{y1 + 26}" rx="{w * .6:.0f}" ry="24" fill="#000" opacity=".5" filter="url(#b12)"/>'
        o += f'<ellipse cx="{cx}" cy="{(y0 + y1) / 2:.0f}" rx="{w * .55:.0f}" ry="{(y1 - y0) * .7:.0f}" fill="{glow}" opacity=".18" filter="url(#b24)"/>'
        o += quad([(cx - w * .47, y0 + 8), (cx, y0 + 26), (cx + w * .47, y0 + 8), (cx + w * .53, y1 + 14), (cx, y1 + 30), (cx - w * .53, y1 + 14)], fill=cover, stroke=OL, stroke_width='5')
        for side in (-1, 1):
            o += (f'<path d="M{cx} {y0 + 16} Q{cx + side * w * .22:.0f} {y0 - 12} {cx + side * w * .44:.0f} {y0} L{cx + side * w * .5:.0f} {y1} '
                  f'Q{cx + side * w * .25:.0f} {y1 - 14} {cx} {y1 + 18}Z" fill="{"#fbf1da" if side < 0 else "#f1e3c2"}" stroke="{OL}" stroke-width="4" stroke-linejoin="round"/>')
        return o

    # left book (gravity), right book (boundary quantum lattice)
    LX, RX, Y0, Y1, W = 1090, 1590, 650, 790, 500
    b += openbook(LX, Y0, Y1, W, '#8a2a2a', '#ffb45a')
    b += openbook(RX, Y0, Y1, W - 40, '#1f4a7a', '#7fe8ff')
    # squiggle "text" lines on the pages (no real words)
    for cx, ww in ((LX, W), (RX, W - 40)):
        for side in (-1, 1):
            for k in range(5):
                t = .18 + k * .15
                yA = Y0 + 10 + (Y1 - Y0) * t
                xa, xb = cx + side * ww * .08, cx + side * ww * (.4 + .06 * t)
                b += f'<path d="M{xa:.0f} {yA + 10:.0f} Q{(xa + xb) / 2:.0f} {yA - 4:.0f} {xb:.0f} {yA + 2:.0f}" fill="none" stroke="#b8a07a" stroke-width="3" opacity=".55"/>'
    # pop-up above the left book: curved gravity well with a planet and a falling comet
    PX, PY = LX, 470
    well = ''
    for k in range(9):
        r = 40 + k * 28
        dy = 120 * math.exp(-k / 2.6)
        well += f'<ellipse cx="{PX}" cy="{PY + 60 + 160 - dy - k * 6:.0f}" rx="{r * 1.0:.0f}" ry="{r * .3:.0f}" fill="none" stroke="#ffcf8a" stroke-width="{3 - k * .2:.1f}" opacity="{.85 - k * .07:.2f}"/>'
    for a in range(0, 360, 30):
        t = math.radians(a)
        pts = []
        for k in range(9):
            r = 40 + k * 28; dy = 120 * math.exp(-k / 2.6)
            pts.append((PX + r * math.cos(t), PY + 60 + 160 - dy - k * 6 + r * .3 * math.sin(t)))
        well += '<path d="M' + ' L'.join(f'{x:.0f},{y:.0f}' for x, y in pts) + '" fill="none" stroke="#ffcf8a" stroke-width="2" opacity=".45"/>'
    b += f'<g>{well}</g>'
    b += f'<path d="M{PX - 230} {Y0 + 10} L{PX - 200} {PY + 210} M{PX + 230} {Y0 + 10} L{PX + 200} {PY + 210}" stroke="#ffcf8a" stroke-width="2" opacity=".4" stroke-dasharray="6 8"/>'
    b += f'<circle cx="{PX}" cy="{PY + 40}" r="150" fill="#ffb45a" opacity=".3" filter="url(#b24)"/>'
    b += f'<circle cx="{PX}" cy="{PY + 40}" r="84" fill="url(#planet4)" stroke="{OL}" stroke-width="4"/>'
    b += f'<path d="M{PX - 70} {PY + 30} Q{PX} {PY + 54} {PX + 72} {PY + 26} M{PX - 60} {PY + 78} Q{PX} {PY + 96} {PX + 58} {PY + 76}" fill="none" stroke="#c86a2a" stroke-width="7" opacity=".55"/>'
    b += f'<path d="M{PX - 54} {PY - 10} A70 70 0 0 1 {PX - 4} {PY - 34}" fill="none" stroke="#fff" stroke-width="7" stroke-linecap="round" opacity=".7"/>'
    b += f'<ellipse cx="{PX}" cy="{PY + 50}" rx="150" ry="36" fill="none" stroke="#fff0c0" stroke-width="3" opacity=".7" transform="rotate(-10 {PX} {PY + 50})"/>'
    b += f'<circle cx="{PX + 138}" cy="{PY + 14}" r="16" fill="#e8e0ff" stroke="{OL}" stroke-width="3"/>'
    b += f'<path d="M{PX - 240} {PY - 120} Q{PX - 170} {PY - 70} {PX - 130} {PY - 20}" stroke="#bff4ff" stroke-width="9" fill="none" stroke-linecap="round" opacity=".5" filter="url(#b3)"/><circle cx="{PX - 128}" cy="{PY - 18}" r="11" fill="#fff"/>'
    # flat lattice glowing on the right pages: dots + wavy links
    nodes = []
    for i in range(6):
        for j in range(4):
            u = -.42 + i * .168; v = .2 + j * .2
            x = RX + u * (W - 40) * (1 + .12 * v); y = Y0 + 10 + (Y1 - Y0 - 10) * v - 26 * (1 - abs(u) * 2) * (1 - v) * .6
            nodes.append((i, j, x, y))
    lat = ''
    for i, j, x, y in nodes:
        for i2, j2, x2, y2 in nodes:
            if (i2 == i + 1 and j2 == j) or (i2 == i and j2 == j + 1):
                mx, my = (x + x2) / 2, (y + y2) / 2 - 8
                lat += f'<path d="M{x:.0f} {y:.0f} Q{mx:.0f} {my - 6:.0f} {x2:.0f} {y2:.0f}" fill="none" stroke="#3ad8ff" stroke-width="3" opacity=".8"/>'
    for i, j, x, y in nodes:
        lat += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="7" fill="#c8f8ff" stroke="#0a3a5a" stroke-width="2"/>'
    b += f'<g filter="url(#b6)" opacity=".8">{lat}</g>' + lat
    gx, gy = [(x, y) for i, j, x, y in nodes if i == 2 and j == 1][0]
    b += f'<circle cx="{gx:.0f}" cy="{gy:.0f}" r="30" fill="#f2d27a" opacity=".6" filter="url(#b6)"/><circle cx="{gx:.0f}" cy="{gy:.0f}" r="12" fill="#ffe8a0" stroke="#6a4a14" stroke-width="3"/>'
    for k in range(3):   # little quantum ripples rising from the page
        b += f'<path d="M{RX - 160 + k * 120} {Y0 - 40 - k * 18} q20 -16 40 0 t40 0 t40 0" fill="none" stroke="#9ff0ff" stroke-width="3" opacity="{.6 - k * .12:.2f}"/>'
    # gold thread linking the planet to its matching point on the boundary page
    thr = f'M{PX + 80} {PY + 10} C{PX + 260} {PY - 180} {gx - 120:.0f} {gy - 340:.0f} {gx:.0f} {gy:.0f}'
    b += f'<path d="{thr}" fill="none" stroke="#f2d27a" stroke-width="22" opacity=".35" filter="url(#b12)"/><path d="{thr}" fill="none" stroke="#ffe8a0" stroke-width="6" stroke-linecap="round"/>'
    b += f'<path d="{thr}" fill="none" stroke="#fff" stroke-width="2.5" stroke-dasharray="4 14" stroke-linecap="round"/>'
    # frog between the books with reading glasses
    fx, fy, fs = 1340, 1000, 2.45
    glasses = ('<g fill="#bff4ff" fill-opacity=".2" stroke="#c9a24e" stroke-width="3.4"><circle cx="-10" cy="-66" r="16.5"/><circle cx="22" cy="-66" r="16.5"/>'
               '<path d="M6.5 -68 q0 -5 0 0" fill="none"/><path d="M5 -69 Q6 -74 7.5 -69" fill="none"/></g><path d="M-18 -74 l7 -3 M14 -74 l7 -3" stroke="#fff" stroke-width="2.4" opacity=".8"/>')
    b += f'<ellipse cx="{fx + 6}" cy="{fy + 6}" rx="120" ry="15" fill="#000" opacity=".5" filter="url(#b3)"/>'
    b += f'<circle cx="{fx}" cy="{fy - 140}" r="170" fill="#ffe8c0" opacity=".1" filter="url(#b24)"/>'
    b += frog(fx, fy, fs, look=(-8, -6), mouth='O', armL='M-34 -24 q-24 -12 -40 -40', armR='M38 -24 q24 -12 40 -40', front=glasses)
    b += spark(1360, 300, 22) + spark(1800, 520, 18, '#e8fbff') + spark(870, 640, 16)
    b += '<rect width="1920" height="1080" fill="url(#vig4)"/>'
    lines = [('TWO BOOKS,', 128, 'w'), ('SAME', 210, 'y'), ('STORY', 170, 'w')]
    return page('#0e2624', svg(d, b), lines, outline='#030a09', top=40)


# ======================= short5: space woven from links =======================
def make_5():
    rnd = random.Random(21)
    d = FILTERS
    d += rad('bg5', 1400, 520, 1300, [(0, '#2a1a5a', 1), (.45, '#120a2e', 1), (1, '#04030c', 1)])
    d += rad('neb5', 1650, 240, 640, [(0, '#ff5ab0', .25), (1, '#ff5ab0', 0)])
    d += rad('pl5', 1370, 560, 95, [(0, '#e8fbff', 1), (.35, '#5ad0ff', 1), (1, '#1a3a9a', 1)])
    d += rad('yarn5', 1040, 900, 80, [(0, '#fff0c0', 1), (.5, '#f2b25a', 1), (1, '#9a5a1a', 1)])
    d += rad('vig5', 1200, 520, 1250, [(0, '#000', 0), (.62, '#000', 0), (1, '#000', .7)])
    b = '<rect width="1920" height="1080" fill="url(#bg5)"/><rect width="1920" height="1080" fill="url(#neb5)"/>' + stars(rnd, 200)
    CX = 1400

    def P3(X, Z):
        dip = 150 * math.exp(-((X - .02) ** 2 + ((Z - .5) * 1.4) ** 2) / .09)
        wave = 10 * math.sin(X * 7 + Z * 5)
        return CX + X * (470 - 210 * Z), 770 - 420 * Z + dip + wave

    NX, NZ = 22, 15
    Xs = [-1 + 2 * i / (NX - 1) for i in range(NX)]
    Zs = [j / (NZ - 1) for j in range(NZ)]
    fab = ''; glow = ''
    for j, Z in enumerate(Zs):
        pts = [P3(-1 + 2 * k / 60, Z) for k in range(61)]
        path = 'M' + ' L'.join(f'{x:.0f},{y:.0f}' for x, y in pts)
        col = '#ff7ad0' if j % 2 else '#7ae8ff'
        wd = 2 + 3 * (1 - Z)
        glow += f'<path d="{path}" fill="none" stroke="{col}" stroke-width="{wd * 3:.1f}" opacity=".35"/>'
        fab += f'<path d="{path}" fill="none" stroke="{col}" stroke-width="{wd:.1f}" opacity="{.55 + .4 * (1 - Z):.2f}"/>'
    for i, X in enumerate(Xs):
        pts = [P3(X, k / 40) for k in range(41)]
        path = 'M' + ' L'.join(f'{x:.0f},{y:.0f}' for x, y in pts)
        col = '#7ae8ff' if i % 2 else '#c8a8ff'
        glow += f'<path d="{path}" fill="none" stroke="{col}" stroke-width="9" opacity=".3"/>'
        fab += f'<path d="{path}" fill="none" stroke="{col}" stroke-width="3" opacity=".75"/>'
    knots = ''
    for i, X in enumerate(Xs):
        for j, Z in enumerate(Zs):
            x, y = P3(X, Z)
            knots += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{2.5 + 3.5 * (1 - Z):.1f}" fill="#fff6e0" opacity=".9"/>'
    # entangled pairs: gold arcs between distant knots
    links = ''
    for _ in range(9):
        X1, Z1 = rnd.choice(Xs[2:-2]), rnd.choice(Zs[1:-2]); X2, Z2 = rnd.choice(Xs[2:-2]), rnd.choice(Zs[1:-2])
        (x1, y1), (x2, y2) = P3(X1, Z1), P3(X2, Z2)
        if math.hypot(x2 - x1, y2 - y1) < 160:
            continue
        mx, my = (x1 + x2) / 2, min(y1, y2) - 120
        links += f'<path d="M{x1:.0f} {y1:.0f} Q{mx:.0f} {my:.0f} {x2:.0f} {y2:.0f}" fill="none" stroke="#f2d27a" stroke-width="3" opacity=".75" stroke-dasharray="2 9" stroke-linecap="round"/>'
        links += f'<circle cx="{x1:.0f}" cy="{y1:.0f}" r="9" fill="#f2d27a"/><circle cx="{x2:.0f}" cy="{y2:.0f}" r="9" fill="#f2d27a"/>'
        links += f'<circle cx="{x1:.0f}" cy="{y1:.0f}" r="22" fill="#f2d27a" opacity=".35" filter="url(#b6)"/><circle cx="{x2:.0f}" cy="{y2:.0f}" r="22" fill="#f2d27a" opacity=".35" filter="url(#b6)"/>'
    b += f'<g filter="url(#b6)">{glow}</g>' + fab + knots
    # planet resting in the dip
    px, py = P3(.02, .5); py -= 78
    b += f'<ellipse cx="{px:.0f}" cy="{py + 80:.0f}" rx="150" ry="34" fill="#000" opacity=".4" filter="url(#b12)"/>'
    b += f'<circle cx="{px:.0f}" cy="{py:.0f}" r="170" fill="#5ad0ff" opacity=".22" filter="url(#b24)"/>'
    d = d.replace('cx="1370" cy="560" r="95"', f'cx="{px - 25:.0f}" cy="{py - 25:.0f}" r="110"')
    b += f'<circle cx="{px:.0f}" cy="{py:.0f}" r="88" fill="url(#pl5)" stroke="#0a1a4a" stroke-width="4"/>'
    b += f'<path d="M{px - 70:.0f} {py - 10:.0f} Q{px - 20:.0f} {py - 40:.0f} {px + 30:.0f} {py - 20:.0f} Q{px + 60:.0f} {py - 8:.0f} {px + 80:.0f} {py - 30:.0f}" fill="none" stroke="#e8fbff" stroke-width="10" stroke-linecap="round" opacity=".55"/>'
    b += f'<path d="M{px - 60:.0f} {py + 36:.0f} Q{px:.0f} {py + 20:.0f} {px + 64:.0f} {py + 40:.0f}" fill="none" stroke="#e8fbff" stroke-width="8" stroke-linecap="round" opacity=".4"/>'
    b += f'<path d="M{px - 58:.0f} {py - 52:.0f} A80 80 0 0 1 {px - 6:.0f} {py - 82:.0f}" fill="none" stroke="#fff" stroke-width="7" stroke-linecap="round" opacity=".8"/>'
    b += links
    # loose threads unravelling from the front-left edge to the yarn ball and the frog's needles
    YX, YY = 1040, 905
    for i in range(0, 8):
        x0, y0 = P3(Xs[i], 0)
        col = '#7ae8ff' if i % 2 else '#c8a8ff'
        tx, ty = (YX + rnd.uniform(-40, 40), YY + rnd.uniform(-40, 30)) if i % 2 else (830 + rnd.uniform(-10, 10), 760 + rnd.uniform(-10, 10))
        c1 = (x0 - 20, y0 + 90); c2 = (tx + 60, ty - 80)
        path = f'M{x0:.0f} {y0:.0f} C{c1[0]:.0f} {c1[1]:.0f} {c2[0]:.0f} {c2[1]:.0f} {tx:.0f} {ty:.0f}'
        b += f'<path d="{path}" fill="none" stroke="{col}" stroke-width="9" opacity=".3" filter="url(#b3)"/><path d="{path}" fill="none" stroke="{col}" stroke-width="3.2" opacity=".9"/>'
    b += f'<circle cx="{YX}" cy="{YY}" r="120" fill="#f2d27a" opacity=".2" filter="url(#b24)"/>'
    b += f'<circle cx="{YX}" cy="{YY}" r="72" fill="url(#yarn5)" stroke="#3a2008" stroke-width="4"/>'
    for k in range(6):
        a = k * 30
        b += f'<ellipse cx="{YX}" cy="{YY}" rx="70" ry="{24 + k * 6}" transform="rotate({a} {YX} {YY})" fill="none" stroke="#9a5a1a" stroke-width="3" opacity=".6"/>'
    b += f'<path d="M{YX - 40} {YY - 40} A56 56 0 0 1 {YX + 6} {YY - 60}" fill="none" stroke="#fff6d8" stroke-width="6" stroke-linecap="round" opacity=".8"/>'
    # frog knitting, in a beanie
    fx, fy, fs = 760, 1000, 2.5
    beanie = ('<path d="M-30 -86 Q-26 -122 8 -124 Q42 -122 46 -86Z" fill="#d8466a" stroke-width="3.4"/>'
              '<path d="M-34 -88 Q8 -96 50 -88 L50 -78 Q8 -86 -34 -78Z" fill="#f2d27a" stroke-width="3"/>'
              '<circle cx="8" cy="-128" r="11" fill="#fff4e0" stroke-width="3"/>'
              '<path d="M-14 -112 v20 M2 -118 v24 M18 -118 v24 M32 -112 v20" stroke="#a8304e" stroke-width="2.4" opacity=".7"/>')
    needles = ('<path d="M54 -40 L96 -98" stroke="#c8c8d8" stroke-width="5" stroke-linecap="round"/><circle cx="96" cy="-98" r="5" fill="#f2d27a" stroke-width="2"/>'
               '<path d="M62 -26 L112 -66" stroke="#c8c8d8" stroke-width="5" stroke-linecap="round"/><circle cx="112" cy="-66" r="5" fill="#f2d27a" stroke-width="2"/>'
               '<path d="M58 -40 q14 6 24 -2 q8 -6 18 0" fill="none" stroke="#7ae8ff" stroke-width="3"/>')
    b += f'<ellipse cx="{fx + 6}" cy="{fy + 6}" rx="120" ry="15" fill="#000" opacity=".5" filter="url(#b3)"/>'
    b += f'<circle cx="{fx}" cy="{fy - 140}" r="170" fill="#c8a8ff" opacity=".12" filter="url(#b24)"/>'
    b += frog(fx, fy, fs, look=(7, -6), mouth='O', brows=False, mid=beanie, armR='M38 -22 q16 -4 22 -20', armL='M-34 -22 q-10 -2 -18 18', front=needles)
    b += spark(1180, 220, 22) + spark(1820, 300, 18, '#ffe8fa') + spark(1700, 700, 16) + spark(980, 640, 14, '#e8fbff')
    b += '<rect width="1920" height="1080" fill="url(#vig5)"/>'
    lines = [('IS SPACE', 150, 'w'), ('WOVEN?', 226, 'y')]
    return page('#120a2e', svg(d, b), lines, outline='#05030c', top=40)


if __name__ == '__main__':
    for n in sys.argv[1:] or ['1', '2', '3', '4', '5']:
        out = os.path.join(VID, f'holographic-universe-short{n}', 'thumb', 'A.html')
        open(out, 'w').write(globals()[f'make_{n}']())
    print('ok')
