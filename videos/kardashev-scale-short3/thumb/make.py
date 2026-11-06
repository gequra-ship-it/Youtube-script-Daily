# Shorts thumbnail A for kardashev-scale-short3 (guideline 16-9: VERTICAL 1080x1920, text centred). Run: python3 make.py
# Layout: galaxy + black hole fill the top, text centred in the middle, the star-to-star train climbs across the bottom.
# HARVEST / A GALAXY   intuitive: a huge spiral galaxy whose stars are wrapped in tiny golden collector swarms, golden threads of
#                      power running to a supermassive black hole at the centre; in front, a star-to-star "morning train" on a
#                      glowing rail with the frog in a conductor's cap riding the locomotive.
#                      (script: "harvest hundreds of billions of stars across a galaxy", "vast swarm of solar collectors",
#                       "rotational energy from supermassive black holes" (theoretical), "as routine ... as taking a morning train")
# Different from the long thumbs (single-star Dyson shell / swarm): here the subject is the whole galaxy.
import os, sys, math, random
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
sys.path.insert(0, os.path.join(REPO, 'tools'))
LONG = os.path.join(REPO, 'videos', 'kardashev-scale', 'thumb', 'make.py')
G = {'__file__': LONG}; exec(open(LONG).read().split('\nfor n, fn in')[0], G)
frog, starfield, nebula, FILTERS, P, INK = G['frog'], G['starfield'], G['nebula'], G['FILTERS'], G['P'], G['INK']
from thumb_lib import vpage, vsvg, lin, rad, spark


def cap():
    return ('<path d="M-30 -84 q2 -34 38 -36 q36 2 40 36z" fill="#2a3a7a" stroke-width="4"/>'
            '<path d="M-22 -100 q10 -14 26 -16" fill="none" stroke="#8aa0e8" stroke-width="3.5" opacity=".8"/>'
            '<path d="M-34 -84 h86 q-2 10 -8 10 h-72 q-6 0 -6 -10z" fill="#1a2550" stroke-width="3.4"/>'
            '<path d="M44 -82 q24 2 30 12 q-14 6 -34 0z" fill="#1a2550" stroke-width="3"/>'
            '<circle cx="8" cy="-98" r="7" fill="#f2c25a" stroke-width="2.6"/>')


def qpt(p0, p1, p2, t):
    x = (1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * p1[0] + t * t * p2[0]
    y = (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * p1[1] + t * t * p2[1]
    dx = 2 * (1 - t) * (p1[0] - p0[0]) + 2 * t * (p2[0] - p1[0]); dy = 2 * (1 - t) * (p1[1] - p0[1]) + 2 * t * (p2[1] - p1[1])
    return x, y, math.degrees(math.atan2(dy, dx))


def car(x, y, ang, s, loco=False):
    L, H = 230, 70
    o = f'<g transform="translate({x:.1f} {y:.1f}) rotate({ang:.1f}) scale({s})" stroke="{INK}" stroke-linejoin="round">'
    o += f'<ellipse cx="0" cy="{H / 2 + 14}" rx="{L / 2}" ry="10" fill="#8fe8ff" opacity=".6" filter="url(#b6)" stroke="none"/>'
    if loco:
        o += (f'<path d="M{-L / 2} {-H / 2} H{L / 2 - 40} Q{L / 2 + 70} {-H / 2 + 6} {L / 2 + 80} {H / 2} H{-L / 2} Z" fill="url(#trainG)" stroke-width="5"/>'
              f'<path d="M{L / 2 - 30} {-H / 2 + 8} Q{L / 2 + 30} {-H / 2 + 12} {L / 2 + 48} {-2} H{L / 2 - 30}z" fill="#8fe8ff" stroke-width="3"/>'
              f'<circle cx="{L / 2 + 66}" cy="{H / 2 - 12}" r="8" fill="#fff6c8" stroke-width="3"/>')
    else:
        o += f'<rect x="{-L / 2}" y="{-H / 2}" width="{L}" height="{H}" rx="18" fill="url(#trainG)" stroke-width="5"/>'
    o += f'<path d="M{-L / 2 + 10} {-H / 2 + 10} H{L / 2 - 40}" stroke="#fff" stroke-width="4" opacity=".7" fill="none"/>'
    o += f'<rect x="{-L / 2}" y="{H / 2 - 18}" width="{L + (60 if loco else 0)}" height="10" fill="#e2483a" stroke="none"/>'
    for k in range(5 if not loco else 3):
        wx = -L / 2 + 20 + k * 40
        o += f'<rect x="{wx}" y="{-H / 2 + 16}" width="28" height="24" rx="6" fill="#ffe7a8" stroke-width="3"/><rect x="{wx - 6}" y="{-H / 2 + 10}" width="40" height="36" rx="8" fill="#ffe7a8" opacity=".3" stroke="none" filter="url(#b3)"/>'
    return o + '</g>'


def make():
    rnd = random.Random(31); gx, gy, grx, gry, grot = 540, 420, 560, 330, -22
    d = FILTERS
    d += lin('sky', [(0, '#0e0626'), (.55, '#1c0a3a'), (1, '#2a0a30')], 1, 1)
    d += lin('trainG', [(0, '#f4f6ff'), (.6, '#c9d0e6'), (1, '#8a94b0')], 0, 1)
    d += rad('vig', 540, 960, 1150, [(0, '#000', 0), (.7, '#000', 0), (1, '#000', .6)])
    d += rad('core', gx, gy, 400, [(0, '#fff6dc', 1), (.3, '#ffd08a', .7), (.65, '#c05a9a', .25), (1, '#6a2a8a', 0)])
    d += lin('railG', [(0, '#8fe8ff'), (1, '#ffd27a')], 1, 0)
    d += rad('txtBg', 540, 965, 560, [(0, '#07031a', .6), (.6, '#07031a', .3), (1, '#07031a', 0)])
    b = '<rect width="1080" height="1920" fill="url(#sky)"/>'
    b += nebula(rnd, 16, (0, 0, 1080, 1920), ['#6a2a9a', '#2a3aa0', '#a03a7a', '#3a1a6a'], 160, 380)
    b += starfield(rnd, 560, (0, 0, 1080, 1920))
    # ---- galaxy ----
    ct, st = math.cos(math.radians(grot)), math.sin(math.radians(grot))
    def gp(x, y):
        return gx + x * ct - y * st, gy + x * st + y * ct
    b += f'<ellipse cx="{gx}" cy="{gy}" rx="{grx * 1.2}" ry="{gry * 1.35}" transform="rotate({grot} {gx} {gy})" fill="#a98cff" opacity=".2" filter="url(#b50)"/>'
    b += f'<circle cx="{gx}" cy="{gy}" r="380" fill="url(#core)"/>'
    arms = ''; dots = ''; hv = []
    for arm in range(2):
        ph = arm * math.pi
        pts = [gp(grx * (.1 + .95 * t) * math.cos(ph + 3.8 * t), gry * (.1 + .95 * t) * math.sin(ph + 3.8 * t)) for t in [k / 50 for k in range(51)]]
        arms += f'<polyline points="{P(pts)}" fill="none" stroke="#c9b0ff" stroke-width="120" opacity=".32" filter="url(#b24)" stroke-linecap="round"/>'
        arms += f'<polyline points="{P(pts)}" fill="none" stroke="#fff0f8" stroke-width="40" opacity=".38" filter="url(#b12)" stroke-linecap="round"/>'
        # dust lane just inside each arm
        dl = [gp(grx * (.06 + .9 * t) * math.cos(ph + 3.8 * t + .25), gry * (.06 + .9 * t) * math.sin(ph + 3.8 * t + .25)) for t in [k / 50 for k in range(8, 46)]]
        arms += f'<polyline points="{P(dl)}" fill="none" stroke="#1a0820" stroke-width="8" opacity=".3" filter="url(#b3)" stroke-linecap="round"/>'
        for i in range(700):
            t = i / 699; r = .1 + .95 * t; a = ph + 3.8 * t + rnd.gauss(0, .13)
            rr = r + rnd.gauss(0, .045)
            x, y = gp(grx * rr * math.cos(a), gry * rr * math.sin(a))
            col = rnd.choice(['#ffffff', '#cfe0ff', '#a8c4ff', '#ffd9f0', '#e9d8ff', '#ffe9c0'])
            dots += f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{rnd.uniform(1.4, 4.2) * (1.35 - t * .6):.1f}" fill="{col}" opacity="{rnd.uniform(.4, .95) * (1 - t * .45):.2f}"/>'
            if i % 34 == 17 and t > .2: hv.append((x, y, 1.3 - t * .5))
    b += arms + dots
    for _ in range(260):   # halo / disc haze stars
        a = rnd.uniform(0, 6.283); rr = abs(rnd.gauss(0, .45))
        x, y = gp(grx * rr * math.cos(a), gry * rr * math.sin(a))
        b += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{rnd.uniform(.8, 2):.1f}" fill="#fff4e0" opacity="{rnd.uniform(.3, .8):.2f}"/>'
    # golden power threads from harvested stars to the core
    th = ''
    for (x, y, s) in hv:
        mx, my = (x + gx) / 2 + (y - gy) * .35, (y + gy) / 2 - (x - gx) * .12
        th += f'M{x:.0f} {y:.0f} Q{mx:.0f} {my:.0f} {gx} {gy} '
    b += f'<path d="{th}" fill="none" stroke="#ffd27a" stroke-width="5" opacity=".35" filter="url(#b3)"/><path d="{th}" fill="none" stroke="#ffe9a8" stroke-width="1.6" opacity=".75"/>'
    for (x, y, s) in hv:   # each harvested star wrapped in a tiny collector swarm
        R = 15 * s
        b += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{R * 2.2:.0f}" fill="#ffc560" opacity=".45" filter="url(#b6)"/>'
        b += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{R * .45:.1f}" fill="#fff8e0"/>'
        for k, (fl, ro) in enumerate(((.35, -20), (.6, 35), (.9, 80))):
            b += f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{R:.1f}" ry="{R * fl:.1f}" transform="rotate({ro} {x:.0f} {y:.0f})" fill="none" stroke="#ffd27a" stroke-width="{1.8 * s:.1f}" stroke-dasharray="{2.5 * s:.1f} {2.2 * s:.1f}"/>'
    # supermassive black hole at the core, inside a bright bulge
    b += f'<ellipse cx="{gx}" cy="{gy}" rx="300" ry="150" transform="rotate({grot} {gx} {gy})" fill="#ffe2a8" opacity=".55" filter="url(#b50)"/>'
    b += f'<ellipse cx="{gx}" cy="{gy}" rx="200" ry="100" transform="rotate({grot} {gx} {gy})" fill="#fff4d8" opacity=".75" filter="url(#b24)"/>'
    b += f'<ellipse cx="{gx}" cy="{gy}" rx="190" ry="60" transform="rotate({grot} {gx} {gy})" fill="#ffd27a" opacity=".55" filter="url(#b12)"/>'
    b += f'<ellipse cx="{gx}" cy="{gy}" rx="150" ry="40" transform="rotate({grot} {gx} {gy})" fill="none" stroke="#fff3c8" stroke-width="16" opacity=".95"/>'
    b += f'<circle cx="{gx}" cy="{gy}" r="58" fill="#ffb455" opacity=".9" filter="url(#b6)"/><circle cx="{gx}" cy="{gy}" r="50" fill="#05020a"/>'
    b += f'<path d="M{gx - 150 * ct:.0f} {gy - 150 * st:.0f} A150 40 {grot} 0 0 {gx + 150 * ct:.0f} {gy + 150 * st:.0f}" fill="none" stroke="#fff8e0" stroke-width="12" transform="translate(0 6)"/>'
    b += f'<circle cx="{gx}" cy="{gy}" r="52" fill="none" stroke="#ffe7b0" stroke-width="3"/>'
    # ---- star-to-star morning train on a glowing rail ----
    b += '<rect width="1080" height="1920" fill="url(#txtBg)"/>'
    p0, p1, p2 = (-120, 1830), (420, 1790), (1180, 1310)
    rail = f'M{p0[0]} {p0[1]} Q{p1[0]} {p1[1]} {p2[0]} {p2[1]}'
    b += f'<path d="{rail}" fill="none" stroke="url(#railG)" stroke-width="40" opacity=".35" filter="url(#b12)"/>'
    b += f'<path d="{rail}" fill="none" stroke="#0a0818" stroke-width="16"/><path d="{rail}" fill="none" stroke="url(#railG)" stroke-width="7"/>'
    for k in range(18):
        x, y, a = qpt(p0, p1, p2, k / 18)
        b += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="5" fill="#fff"/>'
    b += f'<circle cx="{p2[0]}" cy="{p2[1]}" r="26" fill="#bff4ff" opacity=".7" filter="url(#b6)"/>'
    xL, yL, aL = qpt(p0, p1, p2, .68)
    b += f'<path d="M{xL + 130:.0f} {yL - 110:.0f} L{xL + 420:.0f} {yL - 420:.0f} L{xL + 520:.0f} {yL - 330:.0f}z" fill="#fff6c8" opacity=".25" filter="url(#b12)"/>'   # headlight
    for t, lo in ((.33, False), (.505, False), (.68, True)):
        x, y, a = qpt(p0, p1, p2, t)
        b += car(x - 58 * math.sin(math.radians(a)), y - 58 * math.cos(math.radians(a)) * 1, a, 1.22, lo)
    # frog with a conductor's cap riding on the locomotive roof
    b += frog(xL - 20, yL - 108, 2.45, rot=aL, look=(5, -4), mouth='O', armL='M-34 -22 q-26 -10 -30 -40', armR='M38 -22 q30 -4 40 -26',
              legs=((-20, -6, -26, 2, -6), (20, -6, 26, 2, 6)), brows=False, front=cap())
    b += spark(940, 120, 20) + spark(120, 150, 16) + spark(90, 1240, 14) + spark(990, 1700, 16) + spark(980, 820, 14)
    b += '<rect width="1080" height="1920" fill="url(#vig)"/>'
    lines = [('HARVEST', 176, 'w'), ('A <span class="g">GALAXY</span>', 176, 'w')]
    return vpage('#0e0626', vsvg(d, b), lines, outline='#07031a', top=800)


open(os.path.join(HERE, 'A.html'), 'w').write(make())
print('ok')
