# Thumbnails A-C for hollow-skyscraper (Burj Khalifa, 828 m, mostly air). Opus thumb agent 2026-11-03, brief tools/briefs/thumb_art.md.
# A = homage: the famous tower-climb shot (climber on the glass facade high above the desert city), frog as tiny climber with glowing grip gloves.
#     Text WHY DOESN'T IT FALL? (S01: "Why does a tower that is mostly empty space not crush itself?")
# B = intuitive: cut-away tower, the inside is sky and clouds, gold concrete spine (S18), raft + ~200 piles under the sand (S10-S14);
#     frog in a hard hat with a rolled paper tube (S03). Text 828 M / MOSTLY AIR (S01: "rises 828 meters ... most of it is air").
# C = homage: Wizard of Oz twister on the plain (sepia storm), tower in a sunbeam breaks the wind into small eddies (S31-S39);
#     frog at the fence with a gingham kerchief and basket. Text CONFUSE THE WIND (S38, museum exhibit's three words).
import os, sys, math, random
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', '..', 'tools'))
from thumb_lib import page, svg, lin, rad, spark

INK = '#1d2b1c'; GREEN = '#6aa55a'; DARKG = '#4d8a4a'; BELLY = '#9cc98a'
FILTERS = ''.join(f'<filter id="blur{s}" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="{s}"/></filter>'
                  for s in (2, 4, 8, 14, 30, 60))


# ---------- mascot frog (tools/assets/frog.svg), posable ----------
def arm(d):
    return (f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="7.5"/>'
            f'<path d="{d}" fill="none" stroke="{GREEN}" stroke-width="3.4"/>')


def frog(x, y, s, flip=False, look=(0, 0), mouth='o', armL=None, armR=None, feet=None, rot_=0,
         back='', front='', helmet=None, hands=True, eyes_skip=()):
    sx = -s if flip else s
    g = [f'<g transform="translate({x} {y}) rotate({rot_}) scale({sx} {s})" stroke="{INK}" stroke-linejoin="round" stroke-linecap="round">', back]
    fl, fr = feet or ((-22, 4, 0), (22, 4, 0))
    for fx, fy, fa in (fl, fr):
        g.append(f'<ellipse cx="{fx}" cy="{fy}" rx="16" ry="9" transform="rotate({fa} {fx} {fy})" fill="{DARKG}" stroke-width="3.2"/>')
    g.append(f'<path d="M-34 0 q-6 -64 34 -70 q40 -2 42 62 q0 10 -6 12 q-36 6 -70 -4z" fill="{GREEN}" stroke-width="4"/>')
    g.append(f'<ellipse cx="2" cy="-12" rx="22" ry="20" fill="{BELLY}" stroke="none" opacity=".7"/>')
    g.append(f'<path d="M-24 -50 q6 -14 18 -16" fill="none" stroke="#a9d692" stroke-width="3" opacity=".8"/>')
    lx, ly = look
    for ex in (-10, 22):
        if ex in eyes_skip: continue
        g.append(f'<circle cx="{ex}" cy="-66" r="13" fill="#f4f5ea" stroke-width="3.2"/>')
        g.append(f'<circle cx="{ex + 2 + lx}" cy="{-66 + ly}" r="5.4" fill="{INK}" stroke="none"/>')
        g.append(f'<circle cx="{ex + 3.6 + lx}" cy="{-68 + ly}" r="1.7" fill="#fff" stroke="none"/>')
    if mouth == 'o':
        g.append('<ellipse cx="6" cy="-42" rx="5.5" ry="6.5" fill="#3a1d1d" stroke-width="2.6"/>')
    else:
        g.append('<path d="M-8 -44 q14 12 28 0" fill="none" stroke-width="3.4"/>')
    g.append('<ellipse cx="-16" cy="-50" rx="5" ry="3" fill="#e88f86" stroke="none" opacity=".55"/><ellipse cx="28" cy="-50" rx="5" ry="3" fill="#e88f86" stroke="none" opacity=".55"/>')
    g.append(front)
    aL = armL or 'M-34 -22 q-14 6 -16 22'
    aR = armR or 'M38 -22 q14 6 16 22'
    g.append(arm(aL)); g.append(arm(aR))
    if hands:
        for a in (aL, aR):
            nums = [float(v) for v in a.replace('M', ' ').replace('q', ' ').split()]
            g.append(f'<circle cx="{nums[0] + nums[-2]}" cy="{nums[1] + nums[-1]}" r="4.2" fill="{GREEN}" stroke="{INK}" stroke-width="2.4"/>')
    if helmet: g.append(helmet)
    g.append('</g>')
    return ''.join(g)


def handpos(a, x, y, s):   # end point of an arm path in page coords
    nums = [float(v) for v in a.replace('M', ' ').replace('q', ' ').split()]
    return x + (nums[0] + nums[-2]) * s, y + (nums[1] + nums[-1]) * s


# ---------- Burj Khalifa, front elevation ----------
# (x0, x1, top) in units of W (width) and H (height to spire tip); outer wings first so inner ones overlap them
SLABS = [(-.50, -.44, .07), (.45, .50, .09), (-.44, -.38, .15), (.39, .45, .18), (-.38, -.31, .25), (.32, .39, .29),
         (-.31, -.24, .36), (.25, .32, .41), (-.24, -.17, .47), (.17, .25, .53), (-.17, -.09, .58), (.09, .17, .63),
         (-.09, .09, .68), (-.06, .06, .75), (-.035, .035, .81)]


def slab_path(cx, base, W, H, s):
    x0, x1, t = cx + s[0] * W, cx + s[1] * W, base - s[2] * H
    w = x1 - x0; r = w * .75
    # scalloped shoulder: the outer side curves up into the inner side
    if s[0] < -.05:      # left wing: inner side is x1
        return f'M{x0:.1f} {base} V{t + r:.1f} Q{x0:.1f} {t:.1f} {x1:.1f} {t - w * .1:.1f} V{base} Z', t
    if s[1] > .05:       # right wing
        return f'M{x0:.1f} {base} V{t - w * .1:.1f} Q{x1:.1f} {t:.1f} {x1:.1f} {t + r:.1f} V{base} Z', t
    return f'M{x0:.1f} {base} V{t + w * .3:.1f} Q{x0 + w / 2:.1f} {t - w * .3:.1f} {x1:.1f} {t + w * .3:.1f} V{base} Z', t


def tower(d, cx, base, H, W, p, tag):
    """p: dict lit=(c0,c1), core=(c0,c1), shade=(c0,c1), rim, band, line, glow"""
    d += lin(f'{tag}L', [(0, p['lit'][0]), (1, p['lit'][1])], x2=1, y2=0)
    d += lin(f'{tag}C', [(0, p['core'][0]), (.45, p['core'][1]), (1, p['shade'][0])], x2=1, y2=0)
    d += lin(f'{tag}S', [(0, p['shade'][0]), (1, p['shade'][1])], x2=1, y2=0)
    d += lin(f'{tag}V', [(0, '#ffffff'), (.6, '#ffffff'), (1, '#000000')])
    d += (f'<pattern id="{tag}fl" width="10" height="{max(4, H / 150):.1f}" patternUnits="userSpaceOnUse">'
          f'<rect width="10" height="1.3" fill="{p["line"]}" opacity=".32"/></pattern>')
    b = ''
    b += f'<ellipse cx="{cx}" cy="{base - H * .45}" rx="{W * 1.1}" ry="{H * .55}" fill="{p["glow"]}" opacity=".35" filter="url(#blur60)"/>'
    clip = ''
    for s in SLABS:
        path, t = slab_path(cx, base, W, H, s)
        clip += f'<path d="{path}"/>'
        fill = f'{tag}C' if abs(s[0] + s[1]) < .01 else (f'{tag}L' if s[0] < 0 else f'{tag}S')
        b += f'<path d="{path}" fill="url(#{fill})" stroke="{p["edge"]}" stroke-width="{max(1.5, W / 120):.1f}"/>'
        b += f'<path d="{path}" fill="url(#{tag}fl)"/>'
        x0, x1 = cx + s[0] * W, cx + s[1] * W
        # mullions
        for k in range(1, 3):
            xm = x0 + (x1 - x0) * k / 3
            b += f'<path d="M{xm:.1f} {base} V{t + (x1 - x0) * .6:.1f}" stroke="{p["rim"]}" stroke-width="1" opacity=".22"/>'
        # rim light on the sunny edge
        xr = x0 + 2 if p.get('sun', 'L') == 'L' else x1 - 2
        b += f'<path d="M{xr:.1f} {base} V{t + (x1 - x0) * .5:.1f}" stroke="{p["rim"]}" stroke-width="{max(2, W / 90):.1f}" opacity=".75"/>'
        # mechanical floors (dark bands, where the outrigger walls are)
        for fy in (.06, .15, .245, .335, .43, .52, .61, .70):
            y = base - fy * H
            if y > t + (x1 - x0) * .9:
                b += f'<rect x="{x0:.1f}" y="{y:.1f}" width="{x1 - x0:.1f}" height="{max(3, H / 160):.1f}" fill="{p["band"]}" opacity=".55"/>'
    # spire
    t0 = base - .81 * H; tip = base - H
    b += f'<polygon points="{cx - .03 * W:.1f},{t0 + 4} {cx + .03 * W:.1f},{t0 + 4} {cx + .006 * W:.1f},{tip + H * .06:.1f} {cx:.1f},{tip} {cx - .006 * W:.1f},{tip + H * .06:.1f}" fill="url(#{tag}S)" stroke="{p["edge"]}" stroke-width="1.5"/>'
    b += f'<polygon points="{cx - .03 * W:.1f},{t0 + 4} {cx:.1f},{t0 + 4} {cx:.1f},{tip} {cx - .006 * W:.1f},{tip + H * .06:.1f}" fill="{p["lit"][0]}" opacity=".85"/>'
    for k in range(1, 6):
        y = t0 - (t0 - tip) * k / 6.5; hw = .03 * W * (1 - k / 6.5) + 1
        b += f'<path d="M{cx - hw:.1f} {y:.1f} H{cx + hw:.1f}" stroke="{p["edge"]}" stroke-width="1.6" opacity=".6"/>'
    d += f'<clipPath id="{tag}clip">{clip}</clipPath>'
    return d, b, tip


# =========================== A: tower-climb homage ===========================
def make_A():
    rnd = random.Random(11); d = FILTERS
    HZ = 520
    d += lin('aSky', [(0, '#0b2550'), (.45, '#2d679b'), (.8, '#e9b679'), (1, '#ffd9a0')])
    d += lin('aGround', [(0, '#e7c08a'), (.25, '#c4935c'), (1, '#6a4527')])
    d += rad('aSun', 430, HZ - 10, 520, [(0, '#fffbe8', 1), (.08, '#ffe9b0', .9), (.3, '#ffc773', .45), (1, '#ff9d4a', 0)])
    body = f'<rect width="1920" height="{HZ}" fill="url(#aSky)"/>'
    body += f'<rect y="{HZ}" width="1920" height="{1080 - HZ}" fill="url(#aGround)"/>'
    # the Gulf on the horizon
    body += f'<rect y="{HZ}" width="1920" height="26" fill="#7fa3b8"/><rect y="{HZ + 26}" width="1920" height="10" fill="#d9c49a" opacity=".7"/>'
    # desert city far below: blocks in rows, smaller toward the horizon
    city = ''
    y = HZ + 40; row = 0
    while y < 1080:
        sc = .35 + (y - HZ) / 560 * 1.4
        x = rnd.uniform(-40, 0)
        while x < 1300:
            w = rnd.uniform(14, 40) * sc; h = rnd.uniform(8, 20) * sc
            if rnd.random() < .82:
                col = rnd.choice(['#efe0c4', '#e2cba6', '#d8bf98', '#f4ead6', '#c9b08a'])
                city += f'<rect x="{x:.0f}" y="{y:.0f}" width="{w:.0f}" height="{h:.0f}" fill="{col}" opacity=".9"/>'
                city += f'<rect x="{x + w:.0f}" y="{y + h * .3:.0f}" width="{w * .5:.0f}" height="{h * .7:.0f}" fill="#5a3a20" opacity=".35"/>'
            x += w + rnd.uniform(6, 20) * sc
        if row % 3 == 2:
            city += f'<rect x="0" y="{y + 22 * sc:.0f}" width="1300" height="{4 * sc:.1f}" fill="#4a3424" opacity=".45"/>'
        y += 26 * sc + 6; row += 1
    # a few distant towers poking up near the horizon, glinting
    for tx, th in ((150, 70), (205, 52), (610, 88), (660, 60), (720, 74), (290, 40)):
        city += f'<rect x="{tx}" y="{HZ + 30 - th}" width="11" height="{th}" fill="#4b6d8c"/><rect x="{tx}" y="{HZ + 30 - th}" width="4" height="{th}" fill="#ffe2a6" opacity=".8"/>'
    body += city
    body += f'<rect y="{HZ - 40}" width="1920" height="200" fill="#ffe4b8" opacity=".35" filter="url(#blur30)"/>'
    body += f'<rect width="1920" height="1080" fill="url(#aSun)"/>'
    body += f'<circle cx="430" cy="{HZ - 10}" r="44" fill="#fffdf2"/>'
    # wispy clouds high up
    for cx_, cy_, rx in ((240, 330, 260), (700, 250, 200), (520, 420, 320)):
        body += f'<ellipse cx="{cx_}" cy="{cy_}" rx="{rx}" ry="{rx * .09:.0f}" fill="#ffe9cc" opacity=".35" filter="url(#blur8)"/>'

    # ---- the glass facade, verticals converge toward a vanishing point far below ----
    VX, VY = 1480, 2900; X0 = 980

    def EL(y, x0=X0):
        return x0 + (VX - x0) * (y + 40) / (VY + 40)
    d += lin('aGlass', [(0, '#123a66'), (.35, '#2f6ea4'), (.6, '#79aed3'), (.8, '#2a5f8e'), (1, '#0e2a4a')], x2=.6, y2=1)
    d += lin('aGlassLow', [(0, '#1d4f7e'), (1, '#0a2038')])
    d += lin('aRim', [(0, '#fff3cf'), (.4, '#ffd27a'), (1, '#2f6ea4')], x2=1, y2=0)
    LEDGE = 850
    up = f'M{X0} -40 L1960 -40 L1960 {LEDGE} L{EL(LEDGE):.0f} {LEDGE} Z'
    body += f'<path d="{up}" fill="url(#aGlass)"/>'
    d += f'<clipPath id="aUp"><path d="{up}"/></clipPath>'
    g = ''
    # floor lines (spandrels): every second one a darker band, spacing shrinks downward
    y = -20; sp = 50; k = 0
    while y < LEDGE:
        x = EL(y)
        if k % 2 == 0:
            g += f'<polygon points="{x:.0f},{y:.0f} 1960,{y - 26:.0f} 1960,{y - 26 + sp * .35:.0f} {x:.0f},{y + sp * .35:.0f}" fill="#0a2240" opacity=".45"/>'
        g += f'<path d="M{x:.0f} {y:.0f} L1960 {y - 26:.0f}" stroke="#d7ecff" stroke-width="1.6" opacity=".35"/>'
        y += sp; sp *= .975; k += 1
    # mullions toward the vanishing point
    for i in range(1, 16):
        xt = X0 + i * 72
        g += f'<path d="M{xt} -40 L{VX + (xt - X0) * .25:.0f} {VY}" stroke="#cfe6ff" stroke-width="2.2" opacity=".42"/>'
    # sun reflection sweeping across the glass
    g += f'<path d="M980 120 L1960 -120 L1960 160 L1000 560 Z" fill="#ffe6b0" opacity=".38" filter="url(#blur30)"/>'
    g += f'<path d="M1040 230 L1960 0 L1960 60 L1050 330 Z" fill="#fff6dc" opacity=".45" filter="url(#blur14)"/>'
    # reflected clouds
    g += f'<ellipse cx="1600" cy="640" rx="260" ry="26" fill="#d8ecff" opacity=".22" filter="url(#blur8)"/>'
    body += f'<g clip-path="url(#aUp)">{g}</g>'
    # rounded wing nose with gold rim light
    rim = f'M{X0 - 30} -40 L{X0 + 34} -40 L{EL(LEDGE, X0 + 34):.0f} {LEDGE} L{EL(LEDGE, X0 - 30):.0f} {LEDGE} Z'
    body += f'<path d="{rim}" fill="url(#aRim)"/>'
    body += f'<path d="M{X0 - 22} -40 L{EL(LEDGE, X0 - 22):.0f} {LEDGE}" stroke="#fffaf0" stroke-width="5" opacity=".95"/>'
    body += f'<path d="M{X0 - 30} -40 L{EL(LEDGE, X0 - 30):.0f} {LEDGE}" stroke="#4a2c12" stroke-width="3" opacity=".6"/>'
    # setback ledge and the lower tier (wider, darker)
    lx = EL(LEDGE) - 220
    body += f'<polygon points="{lx:.0f},{LEDGE + 40} {EL(LEDGE) - 20:.0f},{LEDGE} 1960,{LEDGE - 30} 1960,{LEDGE + 8} {lx + 10:.0f},{LEDGE + 74}" fill="#f1dcae" stroke="#5a3d1c" stroke-width="3"/>'
    body += f'<polygon points="{lx + 10:.0f},{LEDGE + 74} 1960,{LEDGE + 8} 1960,1100 {lx + 140:.0f},1100" fill="url(#aGlassLow)"/>'
    body += f'<path d="M{lx + 10:.0f} {LEDGE + 74} L{lx + 140:.0f} 1100" stroke="#ffd98f" stroke-width="5" opacity=".8"/>'
    for i in range(1, 9):
        body += f'<path d="M{lx + 10 + i * 110:.0f} {LEDGE + 74 - i * 7:.0f} L{lx + 140 + i * 105:.0f} 1100" stroke="#cfe6ff" stroke-width="2" opacity=".25"/>'
    # keep the bottom-right corner quiet
    d += rad('aVig', 1920, 1080, 560, [(0, '#050c18', .75), (1, '#050c18', 0)])
    body += '<rect width="1920" height="1080" fill="url(#aVig)"/>'
    # wind streaks
    for _ in range(14):
        yy = rnd.uniform(160, 900); xx = rnd.uniform(100, 1500); L = rnd.uniform(160, 420)
        body += f'<path d="M{xx:.0f} {yy:.0f} q{L / 2:.0f} -{L * .06:.0f} {L:.0f} {L * .02:.0f}" fill="none" stroke="#ffffff" stroke-width="{rnd.uniform(2, 4):.1f}" stroke-linecap="round" opacity="{rnd.uniform(.25, .5):.2f}"/>'

    # ---- the frog climber ----
    FX, FY, S = 1390, 690, 3.6
    aL = 'M-34 -24 q-30 -6 -40 -44'; aR = 'M38 -24 q30 -6 40 -44'
    rope = f'<path d="M1395 -20 Q1360 200 {FX + 2} {FY - 20 * S:.0f}" fill="none" stroke="#1a1410" stroke-width="9"/><path d="M1395 -20 Q1360 200 {FX + 2} {FY - 20 * S:.0f}" fill="none" stroke="#e8d3a8" stroke-width="4"/>'
    body += f'<ellipse cx="{FX + 30}" cy="{FY - 120}" rx="200" ry="230" fill="#0a1a30" opacity=".35" filter="url(#blur30)"/>'
    body += rope
    for a in (aL, aR):
        hx, hy = handpos(a, FX, FY, S)
        body += f'<circle cx="{hx:.0f}" cy="{hy:.0f}" r="70" fill="#5fd8ff" opacity=".55" filter="url(#blur14)"/>'
    harness = ('<path d="M-36 -20 q38 12 78 -2" fill="none" stroke="#1b1b22" stroke-width="7"/>'
               '<path d="M-26 -38 q-4 8 -6 18 M36 -40 q4 8 4 18" fill="none" stroke="#1b1b22" stroke-width="5"/>'
               '<rect x="-2" y="-20" width="14" height="10" rx="2" fill="#c9ccd6" stroke-width="2"/>')
    body += frog(FX, FY, S, look=(-3, 3), mouth='o', armL=aL, armR=aR, feet=((-34, 2, -35), (40, 2, 35)), front=harness, hands=False)
    for a in (aL, aR):
        hx, hy = handpos(a, FX, FY, S)
        body += f'<ellipse cx="{hx:.0f}" cy="{hy:.0f}" rx="30" ry="26" fill="#2d3442" stroke="{INK}" stroke-width="7"/>'
        body += f'<ellipse cx="{hx:.0f}" cy="{hy:.0f}" rx="20" ry="16" fill="#8ff0ff"/><ellipse cx="{hx - 5:.0f}" cy="{hy - 5:.0f}" rx="7" ry="5" fill="#fff"/>'
    body += spark(FX - 190, FY - 290, 20) + spark(FX + 210, FY - 300, 16, '#c8f6ff') + spark(1180, 200, 22) + spark(1700, 120, 18)
    TEXT = [("WHY DOESN'T", 132, 'w'), ('IT <span class="g">FALL?</span>', 206, 'w')]
    return page('#0b2550', svg(d, body), TEXT, outline='#06101f', top=48)


# =========================== B: cut-away, mostly air ===========================
def make_B():
    rnd = random.Random(7); d = FILTERS
    GY = 790
    d += lin('bSky', [(0, '#1b1446'), (.45, '#5a2f6e'), (.78, '#e0774a'), (1, '#ffc36e')])
    d += lin('bSoil', [(0, '#a3713e'), (.4, '#6b4626'), (1, '#2a1a0e')])
    body = f'<rect width="1920" height="{GY}" fill="url(#bSky)"/>'
    d += rad('bSun', 380, GY - 30, 520, [(0, '#ffe8b0', .9), (.3, '#ffb060', .35), (1, '#ff8040', 0)])
    body += f'<rect width="1920" height="{GY}" fill="url(#bSun)"/>'
    for _ in range(70):
        body += f'<circle cx="{rnd.randint(20, 1900)}" cy="{rnd.randint(10, 300)}" r="{rnd.choice([1.2, 1.8, 2.4])}" fill="#fff" opacity="{rnd.uniform(.2, .7):.2f}"/>'
    # dunes on the horizon
    body += f'<path d="M0 {GY - 40} Q240 {GY - 90} 520 {GY - 50} T1100 {GY - 60} T1920 {GY - 70} V{GY} H0 Z" fill="#b5703f" opacity=".85"/>'
    body += f'<path d="M0 {GY - 15} Q300 {GY - 55} 700 {GY - 25} T1500 {GY - 30} T1920 {GY - 20} V{GY} H0 Z" fill="#d18c4f"/>'
    # underground cross-section: weak sandstone / siltstone layers
    body += f'<rect y="{GY}" width="1920" height="{1080 - GY}" fill="url(#bSoil)"/>'
    for k, (yy, col) in enumerate(((GY + 50, '#8a5a30'), (GY + 120, '#5e3c1f'), (GY + 190, '#4a2e17'))):
        body += f'<path d="M0 {yy} Q480 {yy - 18} 960 {yy + 6} T1920 {yy - 6} V{yy + 26} Q1440 {yy + 34} 960 {yy + 28} T0 {yy + 22} Z" fill="{col}" opacity=".7"/>'
    for _ in range(120):
        x = rnd.randint(0, 1920); y = rnd.randint(GY + 10, 1075)
        if x > 1540 and y > 820: continue
        body += f'<circle cx="{x}" cy="{y}" r="{rnd.choice([2, 3, 4])}" fill="#d9a46c" opacity="{rnd.uniform(.15, .4):.2f}"/>'
    body += f'<path d="M0 {GY} H1920" stroke="#ffd79a" stroke-width="3" opacity=".6"/>'

    CX, H, W = 1200, 770, 400
    BASE = GY
    # raft ("snowshoe") and piles
    RX0, RX1, RT, RB = CX - 330, CX + 330, GY + 6, GY + 52
    d += lin('bConc', [(0, '#f3ead8'), (.5, '#cfc3ab'), (1, '#8f8470')])
    d += lin('bPile', [(0, '#7e7562'), (.35, '#e9e0cc'), (1, '#6f6654')], x2=1, y2=0)
    body += f'<ellipse cx="{CX - 15}" cy="{GY + 140}" rx="420" ry="170" fill="#ffcf7a" opacity=".22" filter="url(#blur30)"/>'
    np_ = 17
    for i in range(np_):
        px = RX0 + 24 + i * (RX1 - RX0 - 48) / (np_ - 1)
        depth = 1040 - (i % 3) * 14
        body += f'<rect x="{px - 11:.0f}" y="{RB - 4}" width="22" height="{depth - RB:.0f}" rx="6" fill="url(#bPile)" stroke="#2a1d10" stroke-width="3"/>'
    body += f'<rect x="{RX0}" y="{RT}" width="{RX1 - RX0}" height="{RB - RT}" rx="22" fill="url(#bConc)" stroke="#2a1d10" stroke-width="4"/>'
    body += f'<path d="M{RX0 + 18} {RT + 8} H{RX1 - 18}" stroke="#fffaf0" stroke-width="4" opacity=".9"/>'
    body += f'<rect x="{RX0}" y="{RT}" width="{RX1 - RX0}" height="{RB - RT}" rx="22" fill="none" stroke="#F2D27A" stroke-width="3" opacity=".8"/>'

    p = dict(lit=('#ffe7c4', '#c98f7a'), core=('#f2d2b0', '#a98088'), shade=('#7c6a8a', '#3d3256'), rim='#fff2d6',
             band='#2a2038', line='#2a1a2c', edge='#1a1222', glow='#ffd08a', sun='L')
    d, tb, tip = tower(d, CX, BASE, H, W, p, 'bt')
    body += tb
    # ---- cut-away: right of the cut you see inside: sky, clouds, floors, gold spine ----
    CUT = CX - .07 * W
    d += lin('bIn', [(0, '#7fd0ff'), (.6, '#bfe8ff'), (1, '#e9f7ff')])
    d += lin('bCore', [(0, '#a8661c'), (.3, '#ffd77a'), (.55, '#fff3c8'), (1, '#c98a2a')], x2=1, y2=0)
    inn = f'<rect x="{CUT:.0f}" y="0" width="{1920 - CUT:.0f}" height="{BASE}" fill="url(#bIn)"/>'
    # clouds drifting inside the tower
    for (ccx, ccy, cr) in ((CX + 125, BASE - 100, 56), (CX + 70, BASE - 260, 50), (CX + 120, BASE - 400, 38), (CX + 50, BASE - 520, 26),
                           (CX + 160, BASE - 190, 30), (CX + 30, BASE - 600, 16)):
        for dx, dy, f in ((-cr * .9, 4, .6), (0, -cr * .3, 1), (cr * .9, 2, .7), (cr * .4, 6, .8)):
            inn += f'<circle cx="{ccx + dx:.0f}" cy="{ccy + dy:.0f}" r="{cr * f:.0f}" fill="#ffffff" opacity=".95"/>'
        inn += f'<ellipse cx="{ccx:.0f}" cy="{ccy + cr * .55:.0f}" rx="{cr * 1.7:.0f}" ry="{cr * .25:.0f}" fill="#9fc8e6" opacity=".6"/>'
    # thin floor slabs: almost nothing between them
    y = BASE - 10
    while y > BASE - .81 * H:
        inn += f'<rect x="{CUT:.0f}" y="{y:.0f}" width="{CX + .5 * W - CUT:.0f}" height="4" fill="#5e6f86"/><rect x="{CUT:.0f}" y="{y:.0f}" width="{CX + .5 * W - CUT:.0f}" height="1.5" fill="#fff" opacity=".8"/>'
        y -= 40
    # wing walls (thin vertical lines at the slab borders)
    for fx in (.09, .17, .25, .32, .39, .45):
        inn += f'<path d="M{CX + fx * W:.0f} {BASE} V0" stroke="#4d5f78" stroke-width="2.5" opacity=".7"/>'
    # the concrete spine, glowing
    c0, c1 = CX - .055 * W, CX + .055 * W
    inn += f'<rect x="{c0 - 20:.0f}" y="{BASE - .8 * H:.0f}" width="{c1 - c0 + 40:.0f}" height="{.8 * H:.0f}" fill="#ffd77a" opacity=".55" filter="url(#blur14)"/>'
    inn += f'<rect x="{c0:.0f}" y="{BASE - .8 * H:.0f}" width="{c1 - c0:.0f}" height="{.8 * H:.0f}" fill="url(#bCore)" stroke="#5a3608" stroke-width="3"/>'
    for k in range(1, 18):
        yy = BASE - k * .8 * H / 18
        inn += f'<path d="M{c0:.0f} {yy:.0f} H{c1:.0f}" stroke="#8a5a14" stroke-width="2" opacity=".5"/>'
    body += f'<g clip-path="url(#btclip)"><rect x="{CUT:.0f}" y="0" width="{1920 - CUT:.0f}" height="{BASE}" fill="#000"/>{inn}</g>'
    # bright cut edge
    body += f'<g clip-path="url(#btclip)"><rect x="{CUT - 5:.0f}" y="0" width="10" height="{BASE}" fill="#fff8e6"/><rect x="{CUT + 5:.0f}" y="0" width="14" height="{BASE}" fill="#000" opacity=".22"/></g>'
    body += f'<g clip-path="url(#btclip)"><path d="M0 0 H1920" /></g>'
    # outline of the whole silhouette on the cut side
    for s in SLABS:
        if s[1] > -.07:
            path, _ = slab_path(CX, BASE, W, H, s)
            body += f'<path d="{path}" fill="none" stroke="#1a1222" stroke-width="3"/>'
    body += spark(CX, tip - 6, 30, '#fff6d6', 1) + f'<circle cx="{CX}" cy="{tip}" r="26" fill="#fff2c4" opacity=".6" filter="url(#blur8)"/>'
    body += spark(CX + 230, 260, 18) + spark(CX - 240, 380, 14) + spark(CX + 170, 560, 12, '#ffffff')

    # ---- frog in a hard hat, looking through a rolled paper tube ----
    FX, FY, S = 600, 806, 3.1
    hat = ('<path d="M-22 -82 q26 -30 56 0 z" fill="#f2b632" stroke-width="3"/><rect x="-28" y="-84" width="66" height="8" rx="3" fill="#e09a1c" stroke-width="2.5"/>'
           '<path d="M-8 -96 q8 -8 16 -6" fill="none" stroke="#fff3c0" stroke-width="3"/>')
    tube = ('<g transform="rotate(-20 26 -66)"><rect x="18" y="-82" width="96" height="32" rx="6" fill="#fbf8ef" stroke-width="3.4"/>'
            '<path d="M30 -82 v32 M48 -82 v32" stroke="#d8d2c0" stroke-width="2"/>'
            '<ellipse cx="114" cy="-66" rx="8" ry="16" fill="#e8e2d0" stroke-width="3"/><path d="M114 -72 q-4 6 0 10 q5 0 4 -5" fill="none" stroke-width="2"/></g>')
    body += f'<ellipse cx="{FX}" cy="{FY + 8}" rx="120" ry="14" fill="#2a1408" opacity=".45"/>'
    body += frog(FX, FY, S, look=(3, -3), mouth='o', helmet=hat + tube, eyes_skip=(22,),
                 armR='M38 -24 q24 -10 30 -34', armL='M-34 -22 q-14 6 -18 24')
    TEXT = [('<span class="g">828 M</span>', 236, 'w'), ('MOSTLY AIR', 150, 'w')]
    return page('#1b1446', svg(d, body), TEXT, outline='#0c0718', top=40)


# =========================== C: twister homage, confuse the wind ===========================
def make_C():
    rnd = random.Random(5); d = FILTERS
    GY = 840
    d += lin('cSky', [(0, '#2b2219'), (.5, '#6b5638'), (1, '#b89a68')])
    d += lin('cGround', [(0, '#a8875a'), (.3, '#7a5d3a'), (1, '#2e2216')])
    body = f'<rect width="1920" height="{GY}" fill="url(#cSky)"/>'
    # storm clouds
    for _ in range(26):
        x = rnd.randint(-100, 1700); y = rnd.randint(-60, 330)
        body += f'<ellipse cx="{x}" cy="{y}" rx="{rnd.randint(160, 340)}" ry="{rnd.randint(60, 120)}" fill="{rnd.choice(["#1c150f", "#33281c", "#4a3b28"])}" opacity="{rnd.uniform(.4, .8):.2f}" filter="url(#blur30)"/>'
    # gap in the clouds, upper right: sunbeam onto the tower
    d += lin('cBeam', [(0, '#fff2c4'), (1, '#ffd36e')])
    body += f'<ellipse cx="1660" cy="40" rx="260" ry="90" fill="#ffe6a8" opacity=".75" filter="url(#blur30)"/>'
    body += f'<polygon points="1540,0 1800,0 1560,{GY} 1110,{GY}" fill="url(#cBeam)" opacity=".28" filter="url(#blur30)"/>'
    # plain + far horizon
    body += f'<rect y="{GY - 30}" width="1920" height="{1110 - GY}" fill="url(#cGround)"/>'
    body += f'<path d="M0 {GY - 30} Q500 {GY - 44} 960 {GY - 32} T1920 {GY - 36} V{GY - 20} H0 Z" fill="#8d7149"/>'
    body += f'<ellipse cx="1330" cy="{GY - 10}" rx="420" ry="40" fill="#ffdf96" opacity=".45" filter="url(#blur14)"/>'

    # ---- the twister ----
    TX = 820
    d += lin('cTw', [(0, '#2c2318'), (.4, '#6e5a3e'), (.6, '#8c7552'), (1, '#3a2e20')], x2=1, y2=0)
    pts_l = []; pts_r = []
    for k in range(41):
        t = k / 40; y = 330 + t * (GY - 340)
        w = 230 * (1 - t) ** 1.6 + 26
        xc = TX + 60 * math.sin(t * 3.0) - 120 * t
        pts_l.append((xc - w, y)); pts_r.append((xc + w, y))
    tw = 'M' + ' L'.join(f'{x:.0f} {y:.0f}' for x, y in pts_l) + ' L' + ' L'.join(f'{x:.0f} {y:.0f}' for x, y in reversed(pts_r)) + ' Z'
    body += f'<path d="{tw}" fill="#1a140d" opacity=".5" filter="url(#blur14)" transform="translate(16 0)"/>'
    body += f'<path d="{tw}" fill="url(#cTw)"/>'
    for k in range(2, 40, 2):
        (xl, y), (xr, _) = pts_l[k], pts_r[k]
        body += f'<path d="M{xl:.0f} {y:.0f} Q{(xl + xr) / 2:.0f} {y + 14:.0f} {xr:.0f} {y - 4:.0f}" fill="none" stroke="{"#c3a676" if k % 4 else "#1c150e"}" stroke-width="{3 if k % 4 else 4}" opacity=".55"/>'
    body += f'<ellipse cx="{TX - 120}" cy="{GY - 20}" rx="230" ry="60" fill="#8a7050" opacity=".7" filter="url(#blur30)"/>'
    body += f'<ellipse cx="{TX + 20}" cy="330" rx="420" ry="70" fill="#231a12" opacity=".85" filter="url(#blur30)"/>'
    for _ in range(40):   # debris specks
        a = rnd.uniform(0, 6.28); r = rnd.uniform(60, 300); y = rnd.uniform(400, GY - 20)
        body += f'<rect x="{TX - 80 + r * math.cos(a):.0f}" y="{y:.0f}" width="{rnd.uniform(4, 10):.0f}" height="{rnd.uniform(3, 6):.0f}" fill="#2a2016" opacity=".7" transform="rotate({rnd.randint(0, 90)} {TX - 80 + r * math.cos(a):.0f} {y:.0f})"/>'

    # ---- the tower in the sunbeam ----
    CX, H, W = 1330, 800, 200
    p = dict(lit=('#f4fbff', '#a9cce6'), core=('#dff0fb', '#7fa9c9'), shade=('#5f87ab', '#2c4766'), rim='#fff6d8',
             band='#1d3149', line='#1b2a3c', edge='#0e1828', glow='#ffe39a', sun='L')
    d, tb, tip = tower(d, CX, GY - 10, H, W, p, 'ct')
    body += tb
    body += spark(CX, tip, 28, '#fff6d6', 1) + f'<circle cx="{CX}" cy="{tip}" r="24" fill="#fff2c4" opacity=".7" filter="url(#blur8)"/>'
    # the wind arrives as one stream from the twister and is broken into small, mismatched eddies along the height
    for k, (yy, sd) in enumerate(((GY - 120, -1), (GY - 230, 1), (GY - 330, -1), (GY - 430, 1), (GY - 520, -1), (GY - 610, 1))):
        half = W * (.5 - (k * .07)) + 10
        body += f'<path d="M{TX + 140:.0f} {yy + 30:.0f} Q{(TX + CX) / 2:.0f} {yy - 10:.0f} {CX - half - 20:.0f} {yy:.0f}" fill="none" stroke="#fff3cf" stroke-width="5" stroke-linecap="round" opacity=".5"/>'
        # eddies on alternating sides, different sizes and heights: no shared rhythm
        for j, side in enumerate((sd, -sd)):
            ex = CX + side * (half + 40 + 26 * j); ey = yy + (14 if j else -16)
            rr = 22 + 10 * ((k + j) % 3)
            body += (f'<path d="M{ex - rr:.0f} {ey:.0f} a{rr} {rr} 0 1 1 {rr * 1.6:.0f} {rr * .4:.0f} a{rr * .6:.0f} {rr * .6:.0f} 0 1 1 -{rr * .9:.0f} -{rr * .5:.0f}" '
                     f'fill="none" stroke="#F2D27A" stroke-width="5" stroke-linecap="round" opacity=".9"/>')
            body += f'<circle cx="{ex:.0f}" cy="{ey:.0f}" r="{rr * 1.4:.0f}" fill="#ffe7a8" opacity=".18" filter="url(#blur8)"/>'
    body += spark(CX + 250, 300, 20) + spark(CX - 230, 210, 16) + spark(1700, 160, 14)

    # ---- foreground: fence, scrub, frog in a gingham kerchief with a basket ----
    body += f'<path d="M0 960 Q400 925 820 970 T1500 1080 H0 Z" fill="#3a2b1a"/>'
    body += f'<path d="M0 1000 Q500 965 900 1010 T1540 1080 H0 Z" fill="#24190f"/>'
    for i, (fx, fy, fh, fa) in enumerate(((90, 1000, 230, -6), (330, 980, 220, -3), (570, 985, 200, 4))):
        body += f'<rect x="{fx - 14}" y="{fy - fh}" width="28" height="{fh}" rx="4" fill="#5a4026" stroke="#120c06" stroke-width="5" transform="rotate({fa} {fx} {fy})"/>'
        body += f'<path d="M{fx - 8} {fy - fh + 14} v{fh - 30}" stroke="#a07a4a" stroke-width="4" opacity=".6" transform="rotate({fa} {fx} {fy})"/>'
    for yy in (840, 900):
        body += f'<path d="M60 {yy} Q330 {yy + 30} 600 {yy + 6}" fill="none" stroke="#151008" stroke-width="4"/>'
    for _ in range(18):
        x = rnd.randint(0, 1300); y = rnd.randint(990, 1070)
        body += f'<path d="M{x} {y} l-14 -30 M{x} {y} l2 -38 M{x} {y} l16 -28" stroke="#5e4a2a" stroke-width="3" stroke-linecap="round"/>'
    FX, FY, S = 470, 1010, 3.3
    kerchief = ('<path d="M-32 -36 q36 14 72 -2" fill="none" stroke="#1d2b1c" stroke-width="14"/>'
                '<path d="M-32 -36 q36 14 72 -2" fill="none" stroke="#5b8fd6" stroke-width="9"/>'
                '<path d="M-24 -33 v6 M-12 -30 v6 M0 -28 v6 M12 -28 v6 M24 -30 v6 M34 -34 v6" stroke="#fff" stroke-width="3"/>'
                '<path d="M38 -38 q22 -2 40 -18 q4 10 -6 18 q16 0 30 -6 q-6 14 -26 14 z" fill="#5b8fd6" stroke-width="3"/>'
                '<path d="M50 -38 l8 10 M64 -42 l6 10 M80 -36 l4 8" stroke="#fff" stroke-width="2.4"/>')
    basket = ('<path d="M-82 -6 q-4 -38 20 -40 q24 2 20 40" fill="none" stroke="#6a4a24" stroke-width="5"/>'
              '<path d="M-92 -6 h52 l-6 30 h-40 z" fill="#b8874a" stroke-width="3.2"/>'
              '<path d="M-90 4 h48 M-88 14 h44 M-80 -6 l2 30 M-66 -6 v30 M-52 -6 l-2 30" stroke="#6a4a24" stroke-width="2" fill="none"/>')
    body += f'<ellipse cx="{FX}" cy="{FY + 8}" rx="120" ry="14" fill="#000" opacity=".45"/>'
    body += frog(FX, FY, S, flip=True, look=(-4, -2), mouth='o', rot_=-6, front=kerchief, back=basket,
                 armR='M38 -24 q26 -10 40 -30', armL='M-34 -22 q-18 0 -24 22')
    # wind streaks across the plain
    for _ in range(12):
        yy = rnd.uniform(560, 960); xx = rnd.uniform(0, 1100); L = rnd.uniform(120, 300)
        body += f'<path d="M{xx:.0f} {yy:.0f} q{L / 2:.0f} -{L * .08:.0f} {L:.0f} 0" fill="none" stroke="#f2e2c0" stroke-width="3" stroke-linecap="round" opacity="{rnd.uniform(.25, .5):.2f}"/>'
    d += rad('cVig', 1920, 1080, 500, [(0, '#0d0905', .6), (1, '#0d0905', 0)])
    body += '<rect width="1920" height="1080" fill="url(#cVig)"/>'
    TEXT = [('CONFUSE', 196, 'w'), ('THE <span class="g">WIND</span>', 196, 'w')]
    return page('#2b2219', svg(d, body), TEXT, outline='#120c06', top=44)


if __name__ == '__main__':
    for n, f in (('A', make_A), ('B', make_B), ('C', make_C)):
        open(os.path.join(HERE, f'{n}.html'), 'w').write(f())
        print('wrote', n)
