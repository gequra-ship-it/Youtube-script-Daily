# Thumbnails A-C for giant-mold (guideline 16-6 / 16-8, brief tools/briefs/thumb_art.md). Run: python3 videos/giant-mold/thumb/make.py
# A  WHAT WAS / THIS / GIANT?      homage: 2001: A Space Odyssey ("Dawn of Man" monolith): one lone pale Prototaxites pillar on a barren
#                                  plain, the dawn sun rising right over its top; frog time-traveller in a helmet reaching towards it.
#                                  Script S08-S11: "massive, stone-colored pillars ... So what was this silent giant?"; family tree stays open (S39).
# B  8 METERS / TALL BEFORE / TREES   intuitive: worm's-eye view of one huge pillar, ankle-high Cooksonia-like plants, millipede, springtail,
#                                  spider relative, burrows at the base; surveyor frog runs a tape up the trunk.
#                                  Script S06-S07 (plants barely reach your ankles), S10 ("eight meters"), S45-S47 (arthropods, tunnels).
# C  FUNGI WENT / UNDERGROUND      intuitive: cross-section, a tall Archaeopteris above, a small pale mushroom at its foot, a glowing white
#                                  mycorrhizal network wrapping the roots below; miner frog with a headlamp. Script S59-S61, S70-S75.
import os, sys, math, random
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', '..', 'tools'))
from thumb_lib import page, svg, lin, rad, spark

INK = '#1d2b1c'; GREEN = '#6aa55a'; DARKG = '#4d8a4a'; BELLY = '#9cc98a'
FILTERS = ''.join(f'<filter id="b{n}" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="{n}"/></filter>' for n in (2, 4, 8, 14, 26, 50, 90))


def P(pts):
    return ' '.join(f'{a:.1f},{b:.1f}' for a, b in pts)


# ---------------- mascot frog (tools/assets/frog.svg body), posable ----------------
def limb(d, w=7.5, wi=3.4):
    return f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="{w}"/><path d="{d}" fill="none" stroke="{GREEN}" stroke-width="{wi}"/>'


def end_of(d):
    n = [float(v) for v in d.replace('M', ' ').replace('q', ' ').split()]
    return n[0] + n[-2], n[1] + n[-1]


def frog(x, y, s, rot=0, flip=False, look=(0, 0), mouth='O', armL=None, armR=None, helmet=False,
         brows=True, back="", front="", shadow=False, mid="", top=""):
    sx = -s if flip else s
    g = [f'<g transform="translate({x} {y}) rotate({rot}) scale({sx} {s})" stroke="{INK}" stroke-linejoin="round" stroke-linecap="round">', back]
    if shadow:
        g.append('<ellipse cx="0" cy="8" rx="54" ry="9" fill="#000" opacity=".3" stroke="none"/>')
    for fx, fy in ((-22, 4), (22, 4)):
        g.append(f'<ellipse cx="{fx}" cy="{fy}" rx="16" ry="9" fill="{DARKG}" stroke-width="3.2"/>')
    g.append(f'<path d="M-34 0 q-6 -64 34 -70 q40 -2 42 62 q0 10 -6 12 q-36 6 -70 -4z" fill="{GREEN}" stroke-width="4"/>')
    g.append(f'<ellipse cx="2" cy="-12" rx="22" ry="20" fill="{BELLY}" stroke="none" opacity=".7"/>')
    g.append('<path d="M-24 -50 q6 -14 18 -16" fill="none" stroke="#b6dea0" stroke-width="3" opacity=".8"/>')
    g.append(mid)
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
    g.append(top)
    if helmet:
        g.append('<circle cx="6" cy="-58" r="45" fill="#d8f4ff" fill-opacity=".14" stroke="#f4fbff" stroke-width="3.4" stroke-opacity=".95"/>')
        g.append('<path d="M-26 -82 q12 -18 32 -21" fill="none" stroke="#fff" stroke-width="5" opacity=".8"/>')
        g.append('<path d="M30 -92 q12 10 14 26" fill="none" stroke="#ffd98a" stroke-width="3.4" opacity=".8"/>')
        g.append('<ellipse cx="6" cy="-15" rx="38" ry="6" fill="#c8ccd6" stroke-width="3"/>')
    for a in (armL or 'M-34 -22 q-14 6 -16 22', armR or 'M38 -22 q14 6 16 22'):
        g.append(limb(a)); ex_, ey_ = end_of(a)
        g.append(f'<circle cx="{ex_:.1f}" cy="{ey_:.1f}" r="5.6" fill="{GREEN}" stroke-width="3"/>')
    g.append(front); g.append('</g>')
    return ''.join(g)


# ---------------- Prototaxites pillar ----------------
def pillar(pid, x, yb, H, w0, w1, lean, rnd, stops, rim='#ffe2a0', rim_side=-1, detail=1.0, cap=.85, tex_dark='#3a2c1e', tex_light='#fff1d6'):
    """tall rounded stone-coloured column. stops = horizontal gradient (left->right). rim_side -1 = lit from the left, +1 from the right."""
    n = 70
    def C(t):
        u = 1 - t; cx, cy = x + lean * .25, yb - H * .5; tx, ty = x + lean, yb - H
        return u * u * x + 2 * u * t * cx + t * t * tx, u * u * yb + 2 * u * t * cy + t * t * ty
    ph = rnd.uniform(0, 6)
    L = []; R = []; W = []
    for i in range(n + 1):
        t = i / n; cx, cy = C(t)
        w = (w0 + (w1 - w0) * t) * (1 + .035 * math.sin(t * 21 + ph) + .02 * math.sin(t * 47 + ph * 2)) + w0 * .35 * math.exp(-t * 16)
        L.append((cx - w, cy)); R.append((cx + w, cy)); W.append(w)
    wt = W[-1]
    tx_, ty_ = C(1); topp = []
    for k in range(1, 12):
        a = math.pi + k * math.pi / 12; j = rnd.uniform(.9, 1.08)
        topp.append((tx_ + math.cos(a) * wt, ty_ + math.sin(a) * wt * cap * j))
    d = f'M{P(L)} L{P(topp)} L{P(R[::-1])}Z'
    defs = lin(pid + 'g', stops, x2=1, y2=0) + f'<clipPath id="{pid}c"><path d="{d}"/></clipPath>'
    defs += lin(pid + 'ao', [(0, '#000'), (.75, '#000'), (1, '#000')])
    o = f'<path d="{d}" fill="url(#{pid}g)"/>'
    tex = ''
    # fibrous vertical streaks (woven tubes)
    for _ in range(int(70 * detail)):
        u = rnd.uniform(-.95, .95); t0 = rnd.uniform(0, .9); t1 = min(1, t0 + rnd.uniform(.05, .35))
        pts = []
        for k in range(9):
            t = t0 + (t1 - t0) * k / 8; cx, cy = C(t); w = W[int(t * n)]
            pts.append((cx + u * w + rnd.uniform(-1.5, 1.5), cy))
        dark = rnd.random() < .6
        tex += (f'<polyline points="{P(pts)}" fill="none" stroke="{tex_dark if dark else tex_light}" stroke-width="{rnd.uniform(1.5, 4.5) * max(1, w0 / 120):.1f}" '
                f'opacity="{rnd.uniform(.08, .26):.2f}" stroke-linecap="round"/>')
    # lumpy horizontal bulges (cylindrical arcs)
    for _ in range(int(5 * detail)):
        t = rnd.uniform(.03, .95); cx, cy = C(t); w = W[int(t * n)]
        sag = w * rnd.uniform(.08, .2)
        tex += f'<path d="M{cx - w:.0f} {cy:.0f} Q{cx:.0f} {cy + sag:.0f} {cx + w:.0f} {cy:.0f}" fill="none" stroke="{tex_dark}" stroke-width="{rnd.uniform(2, 5) * max(1, w0 / 150):.1f}" opacity="{rnd.uniform(.12, .28):.2f}"/>'
        tex += f'<path d="M{cx - w:.0f} {cy + 5:.0f} Q{cx:.0f} {cy + sag + 5:.0f} {cx + w:.0f} {cy + 5:.0f}" fill="none" stroke="{tex_light}" stroke-width="2" opacity="{rnd.uniform(.1, .22):.2f}"/>'
    # lichen-like blotches
    for _ in range(int(40 * detail)):
        t = rnd.uniform(0, .97); cx, cy = C(t); w = W[int(t * n)]; u = rnd.uniform(-1, 1)
        col = rnd.choice(['#c9b98a', '#a8a07a', '#8e8a68', '#d8cba4', '#7b6c52', '#b9c1a0'])
        r = rnd.uniform(.05, .18) * w
        tex += f'<ellipse cx="{cx + u * w:.0f}" cy="{cy:.0f}" rx="{r * 1.3:.1f}" ry="{r:.1f}" fill="{col}" opacity="{rnd.uniform(.15, .45):.2f}"/>'
    # small cracks
    for _ in range(int(14 * detail)):
        t = rnd.uniform(.05, .9); cx, cy = C(t); w = W[int(t * n)]; px = cx + rnd.uniform(-.8, .8) * w; py = cy
        pts = [(px, py)]
        for k in range(4):
            px += rnd.uniform(-w * .08, w * .08); py += rnd.uniform(w * .05, w * .14); pts.append((px, py))
        tex += f'<polyline points="{P(pts)}" fill="none" stroke="#2a1e14" stroke-width="{2.4 * max(1, w0 / 150):.1f}" opacity=".45"/>'
    # base ambient occlusion
    bx, by = C(0)
    tex += f'<ellipse cx="{bx:.0f}" cy="{by + 10:.0f}" rx="{w0 * 2.2:.0f}" ry="{H * .1:.0f}" fill="#1a120a" opacity=".55" filter="url(#b26)"/>'
    o += f'<g clip-path="url(#{pid}c)">{tex}</g>'
    # rim light
    side = L if rim_side < 0 else R
    o += f'<polyline points="{P(side[3:])}" fill="none" stroke="{rim}" stroke-width="{max(10, w0 * .14):.0f}" opacity=".55" filter="url(#b8)"/>'
    o += f'<polyline points="{P(side[3:])}" fill="none" stroke="{rim}" stroke-width="{max(2.5, w0 * .03):.1f}" opacity=".9"/>'
    o += f'<path d="{d}" fill="none" stroke="#1c140c" stroke-width="{max(2, w0 * .025):.1f}" opacity=".55"/>'
    return defs, o, C, W, d


# ---------------- small life ----------------
def cooksonia(x, y, h, rnd, col='#5f7a2e', spc='#c99a3a', lw=None):
    lw = lw or max(1.4, h * .045)
    def br(x0, y0, L, a, depth):
        x1 = x0 + math.sin(a) * L; y1 = y0 - math.cos(a) * L
        s = f'<path d="M{x0:.1f} {y0:.1f} Q{(x0 + x1) / 2 + rnd.uniform(-L * .12, L * .12):.1f} {(y0 + y1) / 2:.1f} {x1:.1f} {y1:.1f}" fill="none" stroke="{col}" stroke-width="{lw * (.7 ** (3 - depth)):.1f}" stroke-linecap="round"/>'
        if depth == 0:
            r = h * .065
            s += f'<ellipse cx="{x1:.1f}" cy="{y1 - r * .6:.1f}" rx="{r * 1.1:.1f}" ry="{r:.1f}" fill="{spc}" stroke="#3a2a10" stroke-width="{max(1, lw * .4):.1f}"/>'
            s += f'<ellipse cx="{x1 - r * .35:.1f}" cy="{y1 - r * .95:.1f}" rx="{r * .35:.1f}" ry="{r * .25:.1f}" fill="#fff2c0" opacity=".7"/>'
            return s
        sp = rnd.uniform(.3, .5)
        return s + br(x1, y1, L * .72, a - sp, depth - 1) + br(x1, y1, L * .72, a + sp, depth - 1)
    return br(x, y, h * .42, rnd.uniform(-.15, .15), 2)


def millipede(x, y, s, ang, rnd, col='#5a3a22', hi='#c78a52'):
    a = math.radians(ang); o = ''
    segs = []
    for k in range(16):
        t = k * 9 * s
        px = x + math.cos(a) * t + math.sin(k * .55) * 3 * s * -math.sin(a)
        py = y + math.sin(a) * t + math.sin(k * .55) * 3 * s * math.cos(a)
        segs.append((px, py))
    nx, ny = -math.sin(a), math.cos(a)
    for k, (px, py) in enumerate(segs):
        for sgn in (1, -1):
            L = 9 * s; ph = (k % 2) * 3 * s
            o += f'<path d="M{px:.1f} {py:.1f} l{nx * sgn * L + math.cos(a) * ph:.1f} {ny * sgn * L + math.sin(a) * ph:.1f}" stroke="#2a1a10" stroke-width="{1.6 * s:.1f}" stroke-linecap="round"/>'
    for k, (px, py) in enumerate(segs[::-1]):
        r = 6.2 * s * (1 if k < 14 else .85)
        o += f'<circle cx="{px:.1f}" cy="{py:.1f}" r="{r:.1f}" fill="{col}" stroke="#1a100a" stroke-width="{1.3 * s:.1f}"/>'
        o += f'<circle cx="{px - nx * r * .35:.1f}" cy="{py - ny * r * .35:.1f}" r="{r * .35:.1f}" fill="{hi}" opacity=".7"/>'
    hx, hy = segs[-1]
    hx += math.cos(a) * 6 * s; hy += math.sin(a) * 6 * s
    for sgn in (1, -1):
        o += f'<path d="M{hx:.1f} {hy:.1f} q{math.cos(a) * 10 * s + nx * sgn * 6 * s:.1f} {math.sin(a) * 10 * s + ny * sgn * 6 * s:.1f} {math.cos(a) * 16 * s + nx * sgn * 12 * s:.1f} {math.sin(a) * 16 * s + ny * sgn * 12 * s:.1f}" fill="none" stroke="#1a100a" stroke-width="{1.4 * s:.1f}"/>'
    return o


def springtail(x, y, s, flip=1):
    return (f'<g transform="translate({x} {y}) scale({s * flip} {s})" stroke="#1a1408" stroke-linecap="round">'
            '<path d="M-8 0 q0 -9 10 -9 q12 0 14 8 q-12 4 -24 1z" fill="#8a7a9a" stroke-width="1.4"/>'
            '<circle cx="13" cy="-6" r="4" fill="#6a5a7a" stroke-width="1.2"/><circle cx="14.5" cy="-7" r="1.2" fill="#fff" stroke="none"/>'
            '<path d="M15 -9 q6 -8 12 -8 M14 -9 q2 -10 8 -13" fill="none" stroke-width="1.2"/>'
            '<path d="M-2 0 l-2 5 M4 0 l0 5 M9 -1 l2 5 M-8 -1 q-6 6 2 7" fill="none" stroke-width="1.3"/>'
            '<path d="M-2 -7 q6 -3 12 -1" fill="none" stroke="#d8c8e8" stroke-width="1.6" opacity=".8"/></g>')


def trigono(x, y, s):
    o = f'<g transform="translate({x} {y}) scale({s})" stroke="#140c06" stroke-linecap="round" stroke-linejoin="round">'
    for k, (a, b2) in enumerate(((-150, -1), (-125, -1), (-60, 1), (-30, 1))):
        for sgn in (1, -1):
            ax = 14 * sgn; o += f'<path d="M{sgn * 4} -6 Q{ax + sgn * (6 + k * 3)} {-22 + k * 6} {ax + sgn * (12 + k * 4)} 2" fill="none" stroke-width="1.8"/>'
    o += '<ellipse cx="0" cy="-6" rx="8" ry="6" fill="#4a3020" stroke-width="1.4"/>'
    o += '<ellipse cx="0" cy="6" rx="12" ry="10" fill="#6a4228" stroke-width="1.6"/>'
    o += '<path d="M-10 4 h20 M-11 8 h22 M-9 12 h18" stroke="#2a1a10" stroke-width="1" opacity=".7"/>'
    o += '<ellipse cx="-4" cy="2" rx="4" ry="2.5" fill="#c08a5a" stroke="none" opacity=".7"/>'
    o += '<circle cx="-2" cy="-9" r="1.4" fill="#ffe" stroke="none"/><circle cx="2" cy="-9" r="1.4" fill="#ffe" stroke="none"/></g>'
    return o


def moss(x0, x1, y0, y1, n, rnd, cols, rmin, rmax, op=(.5, .95)):
    o = ''
    for _ in range(n):
        x = rnd.uniform(x0, x1); y = rnd.uniform(y0, y1); r = rnd.uniform(rmin, rmax)
        o += f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{r:.1f}" ry="{r * .5:.1f}" fill="{rnd.choice(cols)}" opacity="{rnd.uniform(*op):.2f}"/>'
    return o


def rock(x, y, r, rnd, base='#7a6248', hi='#d8b888', sh='#3a2a1c'):
    pts = []
    for k in range(9):
        a = math.pi + k * math.pi / 8; rr = r * rnd.uniform(.75, 1.1)
        pts.append((x + math.cos(a) * rr * 1.3, y + math.sin(a) * rr * .8))
    o = f'<path d="M{P(pts)}Z" fill="{base}" stroke="{sh}" stroke-width="{max(1, r * .06):.1f}"/>'
    o += f'<path d="M{P(pts[:5])}" fill="none" stroke="{hi}" stroke-width="{max(1.2, r * .12):.1f}" opacity=".7"/>'
    o += f'<ellipse cx="{x + r * .2:.0f}" cy="{y:.0f}" rx="{r * 1.4:.0f}" ry="{r * .18:.0f}" fill="#000" opacity=".35"/>'
    return o


# ================= A: 2001 "Dawn of Man" monolith -> a lone Prototaxites at sunrise =================
def make_A():
    rnd = random.Random(2001)
    d = FILTERS
    hz = 800
    d += lin('skyA', [(0, '#1c3a40'), (.35, '#3d6464'), (.62, '#b98a58'), (.8, '#f0b860'), (1, '#ffe2a0')])
    d += rad('sunA', 1232, 104, 760, [(0, '#fff8e0', 1), (.06, '#ffeab0', .95), (.2, '#f7c46a', .45), (.55, '#e0904a', .12), (1, '#e0904a', 0)])
    d += lin('groundA', [(0, '#8a6440'), (.2, '#5e4430'), (1, '#1e150e')])
    d += rad('vigA', 960, 520, 1200, [(0, '#000', 0), (.62, '#000', 0), (1, '#0a0604', .7)])
    b = '<rect width="1920" height="1080" fill="url(#skyA)"/>'
    # thin high clouds catching the light
    for _ in range(9):
        y = rnd.uniform(240, 600); x = rnd.uniform(-100, 1900)
        b += f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{rnd.uniform(180, 420):.0f}" ry="{rnd.uniform(6, 16):.0f}" fill="#ffd8a0" opacity="{rnd.uniform(.12, .3):.2f}" filter="url(#b8)"/>'
    b += '<rect width="1920" height="1080" fill="url(#sunA)"/>'
    # sun rays fanning from behind the top of the pillar
    for k in range(22):
        a = -math.pi + k * math.pi / 21 + rnd.uniform(-.03, .03); L = 1500; wa = rnd.uniform(.012, .03)
        b += (f'<path d="M1232 104 L{1232 + math.cos(a - wa) * L:.0f} {104 + math.sin(a - wa) * L:.0f} L{1232 + math.cos(a + wa) * L:.0f} {104 + math.sin(a + wa) * L:.0f}Z" '
              f'fill="#fff0c0" opacity="{rnd.uniform(.05, .13):.2f}"/>')
    b += '<circle cx="1232" cy="104" r="58" fill="#fffaf0"/>'
    b += '<circle cx="1232" cy="104" r="96" fill="#fff4d0" opacity=".6" filter="url(#b26)"/>'
    # far mesas / hills
    b += '<path d="M0 760 L120 742 L260 748 L300 728 L420 730 L470 752 L700 756 L860 744 L980 760 L1500 760 L1560 738 L1700 734 L1760 752 L1920 748 L1920 820 L0 820Z" fill="#a07a5a" opacity=".55"/>'
    b += '<path d="M0 784 L200 776 L520 786 L900 778 L1400 788 L1920 780 L1920 830 L0 830Z" fill="#8a6446" opacity=".7"/>'
    # ground
    b += f'<rect x="0" y="{hz}" width="1920" height="{1080 - hz}" fill="url(#groundA)"/>'
    b += f'<ellipse cx="1250" cy="{hz + 6}" rx="700" ry="26" fill="#ffd090" opacity=".45" filter="url(#b14)"/>'
    # distant pillars on the horizon (smaller, hazy)
    for i, (x, h, w) in enumerate(((1660, 150, 13), (1790, 96, 9), (820, 92, 9), (560, 62, 6), (1490, 70, 7))):
        dd, oo, *_ = pillar(f'fa{i}', x, hz + 4, h, w, w * .85, rnd.uniform(-6, 6), rnd, [(0, '#e8c48a'), (.3, '#a88a6a'), (1, '#6a5240')], rim='#ffe0a0', rim_side=1 if x < 1250 else -1, detail=.15)
        d += dd; b += f'<g opacity=".8">{oo}</g>'
    # long shadow of the main pillar running towards the viewer
    b += '<path d="M1188 828 L1312 828 L1450 1080 L1030 1080Z" fill="#120a06" opacity=".55" filter="url(#b8)"/>'
    # pebbles and rocks with low sun rims, growing toward the front
    for _ in range(70):
        y = rnd.uniform(hz + 10, 1070); sc = ((y - hz) / (1080 - hz)) ** 1.4
        x = rnd.uniform(0, 1920)
        if x > 1560 and y > 880: continue
        b += rock(x, y, 3 + sc * rnd.uniform(14, 40), rnd, base='#6e5038', hi='#ffc880', sh='#2a1c10')
    # ankle-high plant tufts and moss patches spreading out from the base
    b += moss(900, 1600, 820, 860, 160, rnd, ['#5d6a2a', '#738032', '#4a5a24'], 4, 14)
    for _ in range(60):
        y = rnd.uniform(hz + 12, 1060); sc = ((y - hz) / (1080 - hz))
        x = rnd.uniform(0, 1920)
        if x > 1560 and y > 880: continue
        if 1030 < x < 1460 and y > 830: continue
        b += cooksonia(x, y, 8 + sc * 70, rnd, col='#53662a', spc='#e0a848')
    # the main pillar (backlit stone, warm bounce light on the front)
    dd, oo, C, W, _ = pillar('pa', 1250, 832, 610, 112, 92, -18, rnd,
                             [(0, '#fff0c8'), (.06, '#e0c69c'), (.3, '#b49c7e'), (.62, '#8a7660'), (.9, '#5e4e3e'), (1, '#ffd890')],
                             rim='#fff0c0', rim_side=-1, detail=1.3, cap=.4)
    d += dd
    b += '<ellipse cx="1250" cy="500" rx="190" ry="420" fill="#ffd890" opacity=".22" filter="url(#b50)"/>'
    b += oo
    # right rim too (backlight wraps both edges)
    b += f'<polyline points="{P([(C(i / 70)[0] + W[i], C(i / 70)[1]) for i in range(4, 71)])}" fill="none" stroke="#ffe0a0" stroke-width="3" opacity=".8"/>'
    # sun flare spilling over the top of the pillar
    b += spark(1232, 104, 70, '#fffbea', .95) + spark(1080, 360, 18) + spark(1450, 420, 14) + spark(1580, 260, 20)
    # base moss and tiny plants hugging the foot of the pillar
    b += moss(1130, 1370, 818, 842, 120, rnd, ['#6e7e30', '#879838', '#56682a'], 4, 11)
    for _ in range(14):
        b += cooksonia(rnd.uniform(1120, 1380), rnd.uniform(828, 846), rnd.uniform(14, 26), rnd, col='#5a6e2a', spc='#f0b850')
    b += millipede(1300, 836, .55, 175, rnd)
    # dust in the light
    for _ in range(70):
        b += f'<circle cx="{rnd.gauss(1250, 300):.0f}" cy="{rnd.uniform(80, 800):.0f}" r="{rnd.choice([1.4, 2, 2.8])}" fill="#fff0c8" opacity="{rnd.uniform(.2, .7):.2f}"/>'
    # frog time-traveller (helmet + suit) in the foreground, reaching toward the pillar
    suit = ('<path d="M-34 -10 Q-38 4 -30 8 L42 8 Q48 2 42 -10 Q4 -4 -34 -10Z" fill="#eef0f4" stroke-width="3.4"/>'
            '<rect x="-4" y="-6" width="20" height="11" rx="3" fill="#c8ccd6" stroke-width="2.4"/>'
            '<circle cx="2" cy="-1" r="2.4" fill="#e04a3a" stroke="none"/><circle cx="10" cy="-1" r="2.4" fill="#4ad0e0" stroke="none"/>')
    b += '<circle cx="700" cy="900" r="170" fill="#ffd890" opacity=".18" filter="url(#b50)"/>'
    b += frog(690, 1018, 2.6, rot=3, look=(11, -8), mouth='O', helmet=True, shadow=True, mid=suit, brows=True,
              armL='M-34 -22 q-18 6 -22 24', armR='M38 -22 q26 -16 40 -44')
    b += '<path d="M612 878 q50 -22 112 -4" fill="none" stroke="#ffe8b0" stroke-width="5" opacity=".75"/>'
    b += '<rect width="1920" height="1080" fill="url(#vigA)"/>'
    lines = [('WHAT WAS', 150, 'w'), ('THIS', 150, 'w'), ('GIANT?', 250, 'y')]
    return page('#1c3a40', svg(d, b), lines, outline='#120c08', top=40)


# ================= B: worm's-eye view, one huge pillar vs ankle-high plants =================
def make_B():
    rnd = random.Random(88)
    d = FILTERS
    hz = 790
    d += lin('skyB', [(0, '#2e5e66'), (.45, '#6a9490'), (.8, '#d8b07a'), (1, '#f2c27a')])
    d += rad('sunB', 260, 640, 900, [(0, '#fff2c8', .9), (.18, '#f8cc80', .5), (.6, '#f0a860', .1), (1, '#f0a860', 0)])
    d += lin('groundB', [(0, '#7e6042'), (.3, '#5a4230'), (1, '#24180e')])
    d += rad('vigB', 960, 540, 1150, [(0, '#000', 0), (.62, '#000', 0), (1, '#0a0806', .72)])
    b = '<rect width="1920" height="1080" fill="url(#skyB)"/>'
    b += '<rect width="1920" height="1080" fill="url(#sunB)"/>'
    for _ in range(8):
        b += f'<ellipse cx="{rnd.uniform(0, 1920):.0f}" cy="{rnd.uniform(120, 560):.0f}" rx="{rnd.uniform(160, 380):.0f}" ry="{rnd.uniform(14, 34):.0f}" fill="#fff0d8" opacity="{rnd.uniform(.1, .25):.2f}" filter="url(#b14)"/>'
    # far hills + far pillars
    b += '<path d="M0 770 Q300 740 600 762 T1200 750 T1920 760 L1920 820 L0 820Z" fill="#9a8a70" opacity=".55"/>'
    for i, (x, h, w) in enumerate(((560, 120, 10), (700, 70, 6), (1700, 160, 13), (1840, 110, 10), (330, 80, 7))):
        dd, oo, *_ = pillar(f'fb{i}', x, hz + 2, h, w, w * .85, rnd.uniform(-5, 5), rnd, [(0, '#f0d2a0'), (.35, '#a8927a'), (1, '#6e5a48')], rim='#ffe2a8', detail=.15)
        d += dd; b += f'<g opacity=".75">{oo}</g>'
    b += f'<rect x="0" y="{hz}" width="1920" height="{1080 - hz}" fill="url(#groundB)"/>'
    b += moss(0, 1920, hz + 4, hz + 40, 260, rnd, ['#6a7a34', '#58682c', '#7e8a3c'], 3, 10)
    b += moss(0, 1920, hz + 40, 1080, 420, rnd, ['#5a6a2a', '#4a5824', '#6a7a30', '#3e4a1e'], 6, 26, (.4, .85))
    # long warm shadow cast to the right by the low sun
    b += '<path d="M1120 965 L1440 965 L1920 1010 L1920 1080 L1300 1080Z" fill="#140c06" opacity=".35" filter="url(#b14)"/>'
    # the giant
    b += '<ellipse cx="1330" cy="560" rx="380" ry="620" fill="#ffd890" opacity=".22" filter="url(#b90)"/>'
    dd, oo, C, W, path = pillar('pb', 1350, 990, 960, 190, 160, 30, rnd,
                                [(0, '#fff0c8'), (.05, '#f2d4a0'), (.22, '#d4b48a'), (.5, '#a68c70'), (.8, '#6e5c4a'), (1, '#3e3226')],
                                rim='#fff0c0', rim_side=-1, detail=2.0)
    d += dd; b += oo
    # burrows / tunnels near the base with tiny residents
    for (u, t, r) in ((-.25, .07, 26), (.35, .14, 20), (-.55, .2, 16), (.1, .26, 13)):
        cx, cy = C(t); w = W[int(t * 70)]; hx = cx + u * w
        b += f'<ellipse cx="{hx:.0f}" cy="{cy:.0f}" rx="{r * 1.2:.0f}" ry="{r:.0f}" fill="#d8c09a" opacity=".7"/>'
        b += f'<ellipse cx="{hx:.0f}" cy="{cy + 2:.0f}" rx="{r:.0f}" ry="{r * .8:.0f}" fill="#120a06" stroke="#3a2a1a" stroke-width="3"/>'
    cx, cy = C(.07); hx = cx - .25 * W[5]
    b += springtail(hx - 6, cy + 4, 1.7)
    cx, cy = C(.14); hx = cx + .35 * W[10]
    b += f'<circle cx="{hx - 4:.0f}" cy="{cy - 2:.0f}" r="3" fill="#ffe" /><circle cx="{hx + 6:.0f}" cy="{cy - 2:.0f}" r="3" fill="#ffe"/>'
    # millipede climbing the trunk
    b += millipede(1350, 820, 1.25, -78, rnd)
    # base moss skirt and ankle-high plants
    b += moss(980, 1580, 955, 1000, 220, rnd, ['#7a8a34', '#62722c', '#8e9a40', '#4e5c24'], 6, 18)
    for x, y, h in ((980, 1000, 70), (1040, 1012, 52), (1500, 1004, 64), (1540, 980, 46), (760, 1040, 90), (690, 1060, 60),
                    (1440, 1030, 80), (870, 980, 44), (600, 990, 40), (1200, 1012, 50), (520, 1040, 70)):
        b += cooksonia(x, y, h, rnd, col='#4e6a26', spc='#e8a84a', lw=max(2.6, h * .05))
    for _ in range(40):
        x = rnd.uniform(0, 1500); y = rnd.uniform(hz + 6, 960)
        b += cooksonia(x, y, 6 + (y - hz) * .22, rnd, col='#4e6226', spc='#d89a44')
    b += trigono(600, 1040, 1.9)
    b += springtail(1110, 1040, 1.5, -1)
    # surveyor frog with a hard hat, running a measuring tape all the way up the trunk
    tx = 1040; sl = 150
    tape = f'<path d="M{tx} 905 L{tx + sl} 68" stroke="#1a1408" stroke-width="20" stroke-linecap="butt"/><path d="M{tx} 905 L{tx + sl} 68" stroke="#f2c21a" stroke-width="14"/>'
    for k in range(48):
        y = 900 - k * 17.4; x = tx + sl * (900 - y) / 837
        tape += f'<path d="M{x - 6:.1f} {y:.1f} l{9 if k % 5 else 14} 0" stroke="#1a1408" stroke-width="{2 if k % 5 else 3}"/>'
    tape += f'<path d="M{tx + sl - 12} 68 l26 0 l0 16" fill="none" stroke="#1a1408" stroke-width="6"/><path d="M{tx + sl - 12} 68 l26 0 l0 16" fill="none" stroke="#c8ccd2" stroke-width="3"/>'
    b += f'<path d="M{tx + 4} 905 L{tx + sl + 4} 68" stroke="#fff4c8" stroke-width="26" opacity=".25" filter="url(#b8)"/>' + tape
    b += spark(tx + sl + 2, 64, 26, '#fffbe6') + spark(1120, 300, 16) + spark(1500, 160, 20) + spark(860, 520, 14)
    hat = ('<g transform="translate(6 -97) rotate(6)"><path d="M-36 6 Q-34 -32 0 -34 Q34 -32 36 6Z" fill="#f28a1a" stroke-width="3.4"/>'
           '<path d="M-48 6 L48 6 Q48 14 0 14 Q-48 14 -48 6Z" fill="#e07812" stroke-width="3.2"/><path d="M-4 -33 L-4 4 M4 -33 L4 4" stroke-width="2.4"/>'
           '<path d="M-24 -16 Q-14 -28 0 -28" fill="none" stroke="#ffd8a0" stroke-width="4" opacity=".85"/></g>')
    vest = '<path d="M-34 -30 L-26 4 M44 -30 L36 4" stroke="#f2c21a" stroke-width="7"/><path d="M-32 -16 L-20 -14 M42 -16 L30 -14" stroke="#e8f4ff" stroke-width="4"/>'
    case = '<g transform="translate(52 -50)"><rect x="-4" y="-16" width="34" height="32" rx="8" fill="#f2c21a" stroke-width="3.4"/><circle cx="13" cy="0" r="8" fill="#3a3a3a" stroke-width="2.4"/></g>'
    b += '<circle cx="910" cy="900" r="160" fill="#fff0c0" opacity=".22" filter="url(#b50)"/>'
    b += frog(910, 1010, 2.4, rot=-3, look=(9, -10), mouth='O', shadow=True, mid=vest, top=hat, brows=True,
              armL='M-34 -22 q-18 4 -22 22', armR='M38 -22 q18 -8 24 -20', front=case)
    for _ in range(50):
        b += f'<circle cx="{rnd.uniform(500, 1900):.0f}" cy="{rnd.uniform(40, 900):.0f}" r="{rnd.choice([1.4, 2, 2.8])}" fill="#fff4d0" opacity="{rnd.uniform(.2, .7):.2f}"/>'
    b += '<rect width="1920" height="1080" fill="url(#vigB)"/>'
    lines = [('8 METERS', 196, 'y'), ('TALL BEFORE', 124, 'w'), ('TREES', 180, 'w')]
    return page('#2e5e66', svg(d, b), lines, outline='#120c08', top=44)


# ================= C: cross-section, tree above, glowing fungal network below =================
def frond(x, y, L, ang, rnd, col, hi, lw=4):
    a = math.radians(ang); dx, dy = math.cos(a), math.sin(a); nx, ny = -dy, dx
    droop = L * .12
    ex, ey = x + dx * L, y + dy * L + droop
    o = f'<path d="M{x:.0f} {y:.0f} Q{x + dx * L * .5:.0f} {y + dy * L * .5 - droop * .3:.0f} {ex:.0f} {ey:.0f}" fill="none" stroke="#3a2a18" stroke-width="{lw}"/>'
    n = int(L / 16)
    for k in range(1, n):
        t = k / n; px = x + dx * L * t; py = y + dy * L * t + droop * t * t
        ll = L * .16 * math.sin(math.pi * (t * .85 + .1))
        for s in (1, -1):
            qx, qy = px + (nx * s * .9 + dx * .5) * ll, py + (ny * s * .9 + dy * .5) * ll + ll * .25
            c = col if rnd.random() < .7 else hi
            o += f'<path d="M{px:.0f} {py:.0f} Q{(px + qx) / 2 + nx * s * 14 - dx * 8:.0f} {(py + qy) / 2 - 12:.0f} {qx:.0f} {qy:.0f} Q{(px + qx) / 2 - nx * s * 6 + dx * 10:.0f} {(py + qy) / 2 + 12:.0f} {px:.0f} {py:.0f}Z" fill="{c}"/>'
    return o


def make_C():
    rnd = random.Random(375)
    d = FILTERS
    gy = 610
    d += lin('skyC', [(0, '#2a5458'), (.6, '#7a9a86'), (1, '#e8c48a')])
    d += rad('sunC', 1500, 420, 700, [(0, '#fff2c8', .85), (.25, '#f2c27a', .4), (1, '#f2c27a', 0)])
    d += lin('soilC', [(0, '#3a2818'), (.25, '#24180e'), (1, '#0c0806')])
    d += rad('netC', 1080, 850, 620, [(0, '#bff8ff', .5), (.35, '#6ad8e0', .18), (1, '#000', 0)])
    d += rad('vigC', 960, 540, 1150, [(0, '#000', 0), (.62, '#000', 0), (1, '#050302', .78)])
    b = '<rect width="1920" height="1080" fill="url(#skyC)"/>'
    b += '<rect width="1920" height="1080" fill="url(#sunC)"/>'
    # distant forest (soft), then light rays
    for k in range(16):
        x = rnd.uniform(0, 1920); h = rnd.uniform(180, 380)
        b += f'<path d="M{x:.0f} {gy} L{x + 6:.0f} {gy - h:.0f}" stroke="#3e5a48" stroke-width="10" opacity=".55"/>'
        b += f'<ellipse cx="{x + 6:.0f}" cy="{gy - h:.0f}" rx="{rnd.uniform(60, 110):.0f}" ry="{rnd.uniform(26, 50):.0f}" fill="#3e6250" opacity=".5" filter="url(#b4)"/>'
    for k in range(5):
        x = 1300 + k * 110
        b += f'<path d="M{x} -20 L{x + 50} -20 L{x - 260} {gy} L{x - 360} {gy}Z" fill="#fff4c8" opacity=".08"/>'
    # ground surface strip (moss, ferny plants), then the cut soil
    b += f'<rect x="0" y="{gy}" width="1920" height="{1080 - gy}" fill="url(#soilC)"/>'
    # soil strata, pebbles
    for k in range(5):
        y = gy + 70 + k * 85 + rnd.uniform(-10, 10)
        b += f'<path d="M0 {y:.0f} Q480 {y + rnd.uniform(-20, 20):.0f} 960 {y:.0f} T1920 {y:.0f}" fill="none" stroke="#4a3420" stroke-width="{rnd.uniform(3, 8):.0f}" opacity=".35"/>'
    for _ in range(45):
        x = rnd.uniform(0, 1920); y = rnd.uniform(gy + 30, 1070)
        r = rnd.uniform(4, 16)
        b += f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{r * 1.3:.1f}" ry="{r:.1f}" fill="#4a3624" stroke="#1a100a" stroke-width="1.5" opacity=".8"/><ellipse cx="{x - r * .3:.0f}" cy="{y - r * .35:.0f}" rx="{r * .4:.1f}" ry="{r * .25:.1f}" fill="#8a6a4a" opacity=".6"/>'
    # glow from the network
    b += '<rect width="1920" height="1080" fill="url(#netC)"/>'
    # tree roots
    tx = 1380
    roots = []
    def root(x, y, ang, L, w, depth):
        if depth == 0 or L < 20: return
        pts = [(x, y)]; a = ang
        for s in range(6):
            a += rnd.uniform(-.25, .25); x += math.cos(a) * L / 6; y += math.sin(a) * L / 6; pts.append((x, y))
        roots.append((pts, w))
        for _ in range(2):
            root(x, y, a + rnd.uniform(-.7, .7), L * .62, w * .6, depth - 1)
        k = rnd.randint(2, 4); root(pts[k][0], pts[k][1], a + rnd.choice((-1, 1)) * rnd.uniform(.6, 1.1), L * .5, w * .5, depth - 1)
    for ang, L, w in ((2.4, 380, 34), (1.95, 360, 34), (1.35, 300, 30), (.9, 220, 26), (2.9, 330, 26)):
        root(tx + math.cos(ang) * 40, gy + 10, ang, L, w, 3)
    rt = ''
    for pts, w in roots:
        rt += f'<polyline points="{P(pts)}" fill="none" stroke="#1a0e06" stroke-width="{w + 6:.1f}" stroke-linecap="round" stroke-linejoin="round"/>'
    for pts, w in roots:
        rt += f'<polyline points="{P(pts)}" fill="none" stroke="#7a5030" stroke-width="{w:.1f}" stroke-linecap="round" stroke-linejoin="round"/>'
        rt += f'<polyline points="{P([(px - w * .2, py - w * .2) for px, py in pts])}" fill="none" stroke="#c89060" stroke-width="{w * .25:.1f}" stroke-linecap="round" opacity=".55"/>'
    # mycelium network: many fine threads, wrapping roots and spreading through the soil
    net = ''; glow = ''
    def ok(x, y):
        return gy + 8 < y < 1075 and not (x > 1640 and y > 900)
    starts = []
    for pts, w in roots:
        for px, py in pts[1::2]:
            starts.append((px, py))
    starts += [(1150, gy + 10)] * 6 + [(rnd.uniform(200, 1500), rnd.uniform(gy + 60, 1000)) for _ in range(16)]
    for (sx, sy) in starts:
        for _ in range(2):
            x, y = sx, sy; a = rnd.uniform(0, 2 * math.pi); pts = [(x, y)]
            for s in range(rnd.randint(7, 14)):
                a += rnd.uniform(-.6, .6); x += math.cos(a) * 14; y += math.sin(a) * 12
                if not ok(x, y): break
                pts.append((x, y))
            if len(pts) > 2:
                op = .9 if (abs(x - 1080) < 520 and abs(y - 850) < 260) else .5
                net += f'<polyline points="{P(pts)}" fill="none" stroke="#f0fdff" stroke-width="{rnd.choice([1.3, 1.8, 2.4])}" opacity="{op}" stroke-linecap="round"/>'
                glow += f'<polyline points="{P(pts)}" fill="none" stroke="#7ae8f0" stroke-width="7" opacity=".5" stroke-linecap="round"/>'
    # threads wrapping the roots (spirals)
    for pts, w in roots:
        if w < 8: continue
        for i in range(len(pts) - 1):
            (x0, y0), (x1, y1) = pts[i], pts[i + 1]
            for k in range(1):
                t = .5; mx = x0 + (x1 - x0) * t; my = y0 + (y1 - y0) * t
                if not ok(mx, my): continue
                net += f'<ellipse cx="{mx:.0f}" cy="{my:.0f}" rx="{w * .6:.1f}" ry="{w * .25:.1f}" transform="rotate({math.degrees(math.atan2(y1 - y0, x1 - x0)) + 90:.0f} {mx:.0f} {my:.0f})" fill="none" stroke="#f0fdff" stroke-width="1.4" opacity=".75"/>'
    d += '<mask id="corC" maskUnits="userSpaceOnUse" x="0" y="0" width="1920" height="1080"><rect width="1920" height="1080" fill="#fff"/><rect x="1580" y="880" width="500" height="300" rx="60" fill="#000" filter="url(#b50)"/></mask>'
    b += f'<g mask="url(#corC)"><g filter="url(#b4)">{glow}</g>{rt}{net}</g>'
    # nutrient sparks travelling (gold sugars down, teal minerals up)
    for _ in range(60):
        x = rnd.gauss(1080, 330); y = rnd.uniform(gy + 30, 1040)
        if not ok(x, y): continue
        c = rnd.choice(['#F2D27A', '#9af4ff', '#ffffff'])
        b += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{rnd.choice([2.4, 3.4, 4.6])}" fill="{c}" opacity="{rnd.uniform(.5, 1):.2f}"/>'
    b += spark(1000, 820, 26, '#f4feff') + spark(1250, 940, 18, '#f4feff') + spark(760, 760, 16, '#f4feff') + spark(1420, 760, 14, '#fff6d0')
    # surface: soil lip, moss and small ferny plants
    b += f'<path d="M0 {gy} Q480 {gy - 10} 960 {gy} T1920 {gy - 4} L1920 {gy + 18} Q960 {gy + 26} 0 {gy + 16}Z" fill="#5a4026"/>'
    b += f'<path d="M0 {gy} Q480 {gy - 10} 960 {gy} T1920 {gy - 4}" fill="none" stroke="#e8b878" stroke-width="3" opacity=".6"/>'
    b += moss(0, 1920, gy - 14, gy + 4, 420, rnd, ['#4e6a2a', '#62802e', '#3c5222', '#7a9438'], 5, 15)
    # the tree: tall Archaeopteris trunk running out of the top, fern-like branch sprays
    trunk = f'M{tx - 70} {gy + 6} Q{tx - 40} {gy - 160} {tx - 34} 300 L{tx - 22} -10 L{tx + 26} -10 L{tx + 36} 300 Q{tx + 44} {gy - 160} {tx + 80} {gy + 6}Z'
    d += lin('barkC', [(0, '#f2c890'), (.12, '#9a6a40'), (.5, '#6a4628'), (1, '#2a1a0e')], x2=1, y2=0)
    b += f'<path d="{trunk}" fill="url(#barkC)" stroke="#1a0e06" stroke-width="5"/>'
    for k in range(18):
        yy = rnd.uniform(0, gy - 20); xx = tx + rnd.uniform(-26, 26)
        b += f'<path d="M{xx:.0f} {yy:.0f} l{rnd.uniform(-4, 4):.0f} {rnd.uniform(30, 80):.0f}" stroke="#2a180c" stroke-width="3" opacity=".5"/>'
    b += f'<path d="M{tx - 36} 300 L{tx - 24} -10" stroke="#ffe0a8" stroke-width="5" opacity=".6"/>'
    for (y, side, L) in ((60, -1, 470), (150, 1, 430), (230, -1, 420), (40, 1, 480), (320, 1, 300), (330, -1, 300)):
        ang = 180 + 12 if side < 0 else -12
        b += frond(tx + side * 20, y, L, ang, rnd, '#3f7a34', '#7aaa48', 7)
        b += frond(tx + side * 20, y + 30, L * .7, ang + side * -18 if side < 0 else ang + 18, rnd, '#356a2c', '#6a9a40', 5)
    # small pale mushroom at the foot of the tree, its threads running down into the network
    mx, my = 1150, gy - 2
    b += f'<g transform="translate({mx} {my}) scale(1.5) translate({-mx} {-my})">'
    b += f'<ellipse cx="{mx}" cy="{my - 40}" rx="90" ry="60" fill="#fff4d8" opacity=".35" filter="url(#b26)"/>'
    b += f'<path d="M{mx - 9} {my} Q{mx - 12} {my - 30} {mx - 6} {my - 44} L{mx + 8} {my - 44} Q{mx + 12} {my - 30} {mx + 10} {my}Z" fill="#efe6d0" stroke="#3a2a1a" stroke-width="3"/>'
    b += f'<path d="M{mx - 40} {my - 40} Q{mx - 36} {my - 82} {mx} {my - 84} Q{mx + 38} {my - 82} {mx + 42} {my - 40} Q{mx} {my - 48} {mx - 40} {my - 40}Z" fill="#e8d2a8" stroke="#3a2a1a" stroke-width="3.4"/>'
    b += f'<path d="M{mx - 26} {my - 60} Q{mx - 16} {my - 76} {mx} {my - 77}" fill="none" stroke="#fffaf0" stroke-width="5" opacity=".8"/>'
    b += '</g>'
    for k in range(5):
        b += f'<path d="M{mx - 6 + k * 3} {my} q{rnd.uniform(-30, 30):.0f} 40 {rnd.uniform(-60, 60):.0f} 90" fill="none" stroke="#f0fdff" stroke-width="1.6" opacity=".85"/>'
    # ferny ground plants
    for x in (180, 330, 820, 1600, 1760, 1880, 980):
        b += frond(x, gy, 70, -110 + rnd.uniform(-20, 20), rnd, '#3e6a2a', '#6a9a3e', 3)
        b += frond(x, gy, 60, -70 + rnd.uniform(-20, 20), rnd, '#3e6a2a', '#6a9a3e', 3)
    # miner frog in a little tunnel with a headlamp, bottom-left
    b += '<ellipse cx="560" cy="985" rx="200" ry="110" fill="#0a0604"/><ellipse cx="560" cy="985" rx="200" ry="110" fill="none" stroke="#4a3420" stroke-width="8"/>'
    b += '<path d="M650 900 L1180 700 L1200 900 L660 945Z" fill="#fff4c8" opacity=".12" filter="url(#b14)"/>'
    hat = ('<g transform="translate(6 -97) rotate(-4)"><path d="M-36 6 Q-34 -32 0 -34 Q34 -32 36 6Z" fill="#f2c21a" stroke-width="3.4"/>'
           '<path d="M-48 6 L48 6 Q48 14 0 14 Q-48 14 -48 6Z" fill="#d8a812" stroke-width="3.2"/>'
           '<rect x="-10" y="-22" width="22" height="18" rx="5" fill="#d8d8d8" stroke-width="3"/><circle cx="1" cy="-13" r="6" fill="#fffbe0" stroke-width="2.4"/>'
           '<path d="M-24 -16 Q-14 -28 0 -28" fill="none" stroke="#fff2b0" stroke-width="4" opacity=".85"/></g>')
    b += frog(560, 1030, 2.5, rot=4, look=(11, -6), mouth='O', shadow=True, top=hat, brows=True,
              armL='M-34 -22 q-18 4 -22 22', armR='M38 -22 q20 -6 30 -26',
              front='<g transform="translate(70 -54) rotate(-30)"><path d="M0 0 l40 -6" stroke-width="5"/><path d="M36 -16 l14 20 l-6 4" fill="#bfc6cc" stroke-width="3"/></g>')
    b += '<circle cx="572" cy="-28" r="0"/>'
    b += '<rect width="1920" height="1080" fill="url(#vigC)"/>'
    lines = [('FUNGI', 150, 'w'), ('WENT', 150, 'w'), ('UNDERGROUND', 136, 'y')]
    return page('#2a5458', svg(d, b), lines, outline='#0a0806', top=40)


for n, fn in (('A', make_A), ('B', make_B), ('C', make_C)):
    open(os.path.join(HERE, f'{n}.html'), 'w').write(fn())
print('ok')
