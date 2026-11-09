# Thumbnails A-C for tromelin-sandbank (guideline 16-6 / 16-8, brief tools/briefs/thumb_art.md). Run: python3 videos/tromelin-sandbank/thumb/make.py
# A  LEFT / BEHIND   (declarative)  homage: Gericault, The Raft of the Medusa (public domain, 1819): a pyramid of tiny castaways on a coral-stone
#    heap, the top one waving a cloth toward a distant sail in a break of light; a broken mast with a torn sail on the left. Script: "The Malagasy
#    survivors were told they had to remain behind"; "people who spent every day watching the sea for a sail"; low stone buildings, the wreck.
# B  THEY KEPT / THE / FIRE   (statement)  intuitive: night, a tiny flat sand island inside its reef ring in a huge dark ocean, one fire glowing at
#    its centre, low stone huts, terns; sailor frog on a little sheep-head caravel (miya 2026-11-09). Script: "the survivors kept a fire burning for fifteen years"; "hope is a flame best kept alive together".
# C  15 YEARS / ON SAND   (number)  intuitive: a giant hourglass at dusk; the falling sand builds the island in the lower bulb (sea, stone hut,
#    fire); the frog scratches 15 tally marks on the base. Script: "a fire burning for fifteen years"; "a flat strip of white sand and coral".
import os, sys, math, random
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', '..', 'tools'))
from thumb_lib import page, svg, lin, rad, spark

INK = '#1d2b1c'; GREEN = '#6aa55a'; DARKG = '#4d8a4a'; BELLY = '#9cc98a'
FILTERS = ''.join(f'<filter id="b{n}" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="{n}"/></filter>' for n in (2, 4, 8, 14, 26, 50, 90))


def P(pts):
    return ' '.join(f'{a:.1f},{b:.1f}' for a, b in pts)


def hx(c):
    c = c.lstrip('#'); return [int(c[i:i + 2], 16) for i in (0, 2, 4)]


def mix(a, b, t):
    t = max(0, min(1, t)); A, B = hx(a), hx(b)
    return '#' + ''.join(f'{round(A[i] + (B[i] - A[i]) * t):02x}' for i in range(3))


# ---------------- mascot frog (tools/assets/frog.svg body), posable; pupils clamped inside the whites (eyecheck) ----------------
def limb(d, w=7.5, wi=3.4):
    return f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="{w}"/><path d="{d}" fill="none" stroke="{GREEN}" stroke-width="{wi}"/>'


def end_of(d):
    n = [float(v) for v in d.replace('M', ' ').replace('q', ' ').split()]
    return n[0] + n[-2], n[1] + n[-1]


def frog(x, y, s, rot=0, flip=False, look=(0, 0), mouth='O', armL=None, armR=None, brows=True, back='', front='', mid='', top='', shadow=False):
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
    _d = math.hypot(1 + lx, ly)
    if _d > 6.9: _k = 6.9 / _d; lx, ly = (1 + lx) * _k - 1, ly * _k
    for ex in (-10, 22):
        g.append(f'<circle cx="{ex}" cy="-66" r="13.5" fill="#f4f5ea" stroke-width="3.2"/>')
        g.append(f'<circle cx="{ex + 1 + lx:.2f}" cy="{-66 + ly:.2f}" r="4.4" fill="{INK}" stroke="none"/>')
        g.append(f'<circle cx="{ex + 2.4 + lx:.2f}" cy="{-67.6 + ly:.2f}" r="1.5" fill="#fff" stroke="none"/>')
    if brows:
        g.append('<path d="M-22 -88 q12 -9 24 -1 M10 -89 q12 -8 24 1" fill="none" stroke-width="3.4"/>')
    if mouth == 'O':
        g.append('<ellipse cx="6" cy="-38" rx="10" ry="12" fill="#7a2f33" stroke-width="3"/><ellipse cx="6" cy="-31" rx="6" ry="4" fill="#e07b7b" stroke="none"/>')
    else:
        g.append('<ellipse cx="6" cy="-41" rx="6" ry="7.5" fill="#7a2f33" stroke-width="3"/>')
    g.append('<ellipse cx="-18" cy="-48" rx="5" ry="3" fill="#e98a8a" stroke="none" opacity=".55"/><ellipse cx="30" cy="-48" rx="5" ry="3" fill="#e98a8a" stroke="none" opacity=".55"/>')
    g.append(top)
    for a in (armL or 'M-34 -22 q-14 6 -16 22', armR or 'M38 -22 q14 6 16 22'):
        g.append(limb(a)); ex_, ey_ = end_of(a)
        g.append(f'<circle cx="{ex_:.1f}" cy="{ey_:.1f}" r="5.6" fill="{GREEN}" stroke-width="3"/>')
    g.append(front); g.append('</g>')
    return ''.join(g)




# ---------------- small gentle castaway figure (feet at 0,0; ~72 units tall) ----------------
def person(x, y, s=1.0, pose='down', cloth='#a2563a', skin='#5a3424', ink='#1a1008', rim='#ffd08a', flip=False, wrap='#d9b77a', sit=False):
    sx = -s if flip else s
    g = f'<g transform="translate({x:.1f} {y:.1f}) scale({sx} {s})" stroke="{ink}" stroke-linejoin="round" stroke-linecap="round">'
    arms = {'down': ('M-10 -42 q-7 14 -6 28', 'M10 -42 q7 14 6 28'),
            'up': ('M-10 -42 q-10 -18 -8 -40', 'M10 -42 q10 -18 8 -40'),
            'wave': ('M-10 -42 q-8 14 -7 26', 'M10 -42 q12 -16 14 -40'),
            'point': ('M-10 -42 q-7 14 -6 28', 'M10 -42 q20 -6 30 -16'),
            'carry': ('M-10 -42 q-4 10 6 16', 'M10 -42 q4 10 -4 16')}[pose]
    if sit:
        g += f'<path d="M-12 -30 Q-15 -6 -12 0 L18 0 Q20 -8 12 -30 Q0 -36 -12 -30Z" fill="{cloth}" stroke-width="3"/>'
        hy = -42
    else:
        g += f'<path d="M-6 -6 L-6 0 M6 -6 L6 0" stroke="{skin}" stroke-width="5"/>'
        g += f'<path d="M-11 -44 Q-15 -16 -13 -6 L13 -6 Q15 -16 11 -44 Q0 -50 -11 -44Z" fill="{cloth}" stroke-width="3"/>'
        g += f'<path d="M-12 -24 Q0 -20 13 -26" fill="none" stroke="{wrap}" stroke-width="4"/>'
        hy = -56
    for a in arms:
        if sit: a = a.replace('-42', '-30')
        g += f'<path d="{a}" fill="none" stroke="{ink}" stroke-width="7"/><path d="{a}" fill="none" stroke="{skin}" stroke-width="3.6"/>'
    g += f'<circle cx="0" cy="{hy}" r="10" fill="{skin}" stroke-width="3"/>'
    g += f'<path d="M-9 {hy - 3} Q-8 {hy - 13} 0 {hy - 12} Q9 {hy - 13} 9 {hy - 3} Q4 {hy - 8} -9 {hy - 3}Z" fill="#20140c" stroke="none"/>'
    # rim light on the side facing the light (right in local coords)
    g += f'<path d="M9 {hy - 6} Q12 {hy} 8 {hy + 6}" fill="none" stroke="{rim}" stroke-width="2.6" opacity=".95"/>'
    if not sit:
        g += f'<path d="M11 -40 Q14 -18 12 -8" fill="none" stroke="{rim}" stroke-width="2.6" opacity=".85"/>'
    g += '</g>'
    return g


def flame(x, y, s=1.0, sway=0):
    def tear(h, w, c, dx=0):
        return f'<path d="M{dx - w},0 C{dx - w},{-h * .45:.0f} {dx + sway - w * .2:.0f},{-h * .7:.0f} {dx + sway},{-h} C{dx + sway + w * .3:.0f},{-h * .65:.0f} {dx + w},{-h * .45:.0f} {dx + w},0 Q{dx},{h * .14:.0f} {dx - w},0Z" fill="{c}"/>'
    g = f'<g transform="translate({x} {y}) scale({s})">'
    g += tear(120, 46, '#ff5a1f') + tear(84, 30, '#ff9a2a', -14) + tear(96, 34, '#ffb43a', 10) + tear(64, 22, '#ffe27a', 2) + tear(34, 12, '#fffbe6', 2)
    g += '</g>'
    return g


def logs(x, y, s=1.0):
    g = f'<g transform="translate({x} {y}) scale({s})" stroke="#1a0e08" stroke-width="4" stroke-linecap="round">'
    g += '<path d="M-60 10 L50 -6" stroke-width="16"/><path d="M-60 10 L50 -6" stroke="#6b4428" stroke-width="10"/>'
    g += '<path d="M-50 -8 L62 10" stroke-width="16"/><path d="M-50 -8 L62 10" stroke="#7d5232" stroke-width="10"/>'
    g += ''.join(f'<ellipse cx="{cx}" cy="{cy}" rx="11" ry="9" fill="#5f5a52" stroke-width="3"/>' for cx, cy in ((-74, 14), (-46, 22), (-14, 26), (20, 25), (52, 20), (78, 12)))
    g += '</g>'
    return g


def foam(d, w=8, op=.85, col='#f2fbff'):
    return f'<path d="{d}" fill="none" stroke="{col}" stroke-width="{w}" stroke-linecap="round" opacity="{op}"/>'


def waves(rnd, n, x0, x1, y0, y1, col, op=(.25, .7), wmin=40, wmax=120, sw=4):
    o = ''
    for _ in range(n):
        x, y, w = rnd.randint(x0, x1), rnd.randint(y0, y1), rnd.randint(wmin, wmax)
        k = (y - y0) / max(1, y1 - y0) * .9 + .4
        w = int(w * k)
        o += f'<path d="M{x},{y} q{w * .25:.0f},{-w * .12:.0f} {w * .5:.0f},0 q{w * .25:.0f},{w * .1:.0f} {w * .5:.0f},0" fill="none" stroke="{col}" stroke-width="{sw * k:.1f}" stroke-linecap="round" opacity="{rnd.uniform(*op):.2f}"/>'
    return o


def tern(x, y, s, col='#1a1a22', under=None):
    d = f'M{x - 30 * s:.0f},{y - 6 * s:.0f} Q{x - 12 * s:.0f},{y - 16 * s:.0f} {x},{y} Q{x + 12 * s:.0f},{y - 16 * s:.0f} {x + 30 * s:.0f},{y - 6 * s:.0f} Q{x + 12 * s:.0f},{y - 8 * s:.0f} {x},{y + 4 * s:.0f} Q{x - 12 * s:.0f},{y - 8 * s:.0f} {x - 30 * s:.0f},{y - 6 * s:.0f}Z'
    o = f'<path d="{d}" fill="{col}"/>'
    if under:
        o += f'<path d="M{x - 18 * s:.0f},{y - 4 * s:.0f} Q{x},{y + 6 * s:.0f} {x + 18 * s:.0f},{y - 4 * s:.0f}" fill="none" stroke="{under}" stroke-width="{max(1.5, 2.5 * s):.1f}" stroke-linecap="round" opacity=".9"/>'
    return o


def straw_hat(c='#e8c46a'):
    return ('<g transform="translate(0 -10)">' +f'<path d="M-44 -82 Q6 -100 56 -82 Q50 -72 6 -74 Q-38 -72 -44 -82Z" fill="{c}" stroke-width="3.4"/>'
            f'<path d="M-18 -84 Q-16 -112 6 -112 Q28 -112 30 -84 Z" fill="{c}" stroke-width="3.4"/>'
            '<path d="M-17 -90 Q6 -84 29 -90" fill="none" stroke="#b5462f" stroke-width="6"/>'
            '<path d="M-30 -80 l6 -3 M-14 -78 l6 -3 M30 -78 l6 -3 M44 -80 l6 -3" stroke="#a7802e" stroke-width="2"/>'
            '<path d="M-8 -106 q8 -4 18 -1" fill="none" stroke="#fff6d0" stroke-width="3" opacity=".8"/></g>')


# ================================================== A: Raft of the Medusa homage ==================================================
def thumb_A():
    rnd = random.Random(7)
    HZ = 708
    defs = FILTERS
    defs += lin('skyA', [(0, '#17140f'), (.3, '#3a2e1f'), (.55, '#7a5a34'), (.78, '#c98f48'), (1, '#f7d28a')])
    defs += rad('breakA', 1680, 690, 620, [(0, '#fffbe6', 1), (.1, '#ffe7a6', .95), (.32, '#f4b860', .5), (.7, '#c47a3a', .12), (1, '#c47a3a', 0)])
    defs += lin('seaA', [(0, '#6d6a4a'), (.1, '#3c4a3a'), (.45, '#1f2e28'), (1, '#0b1411')])
    defs += lin('sandA', [(0, '#e6c48a'), (.4, '#b58a58'), (1, '#4a3424')])
    defs += lin('sailA', [(0, '#e9d7aa'), (.6, '#b79a6a'), (1, '#6e5a3e')], x2=1, y2=.4)
    defs += rad('fireA', 1000, 770, 260, [(0, '#ffcf6a', .9), (.4, '#ff8a2a', .35), (1, '#ff6a1a', 0)])
    defs += rad('vigA', 1060, 600, 1150, [(0, '#000', 0), (.6, '#000', 0), (1, '#000', .62)])
    b = '<rect width="1920" height="1080" fill="url(#skyA)"/>'
    # heavy dark storm clouds (Gericault browns), lit edges toward the light break
    for x, y, rx, ry, c, o in ((300, 120, 620, 200, '#0c0a07', .85), (1000, 80, 700, 170, '#14100a', .85), (1600, 160, 520, 160, '#1c160e', .8),
                               (1250, 330, 520, 90, '#2a2014', .7), (520, 420, 520, 80, '#2c2216', .6), (1820, 400, 260, 70, '#3a2c1a', .55)):
        b += f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{ry}" fill="{c}" opacity="{o}" filter="url(#b50)"/>'
    for x, y, rx in ((1500, 520, 260), (1820, 560, 180), (1240, 600, 220), (1690, 610, 120)):
        b += f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{rx * .09:.0f}" fill="#ffe2a0" opacity=".55" filter="url(#b8)"/>'
    b += '<rect width="1920" height="1080" fill="url(#breakA)"/>'
    # god rays from the light break
    for a in (-160, -140, -122, -104, -60, -40):
        r = math.radians(a)
        b += f'<path d="M1680,690 L{1680 + math.cos(r - .03) * 1500:.0f},{690 + math.sin(r - .03) * 1500:.0f} L{1680 + math.cos(r + .03) * 1500:.0f},{690 + math.sin(r + .03) * 1500:.0f}Z" fill="#fff0c0" opacity=".07"/>'
    # sea
    b += f'<rect x="0" y="{HZ}" width="1920" height="{1080 - HZ}" fill="url(#seaA)"/>'
    b += f'<path d="M1560,{HZ} L1800,{HZ} L1980,1080 L1500,1080Z" fill="#ffe6a0" opacity=".14" filter="url(#b26)"/>'
    b += ''.join(f'<rect x="{rnd.randint(1450, 1900)}" y="{rnd.randint(HZ + 4, 820)}" width="{rnd.randint(20, 80)}" height="3" rx="1.5" fill="#fff1c0" opacity="{rnd.uniform(.4, .9):.2f}"/>' for _ in range(40))
    b += waves(rnd, 70, -40, 1900, HZ + 20, 1060, '#c9d6c0', (.15, .5), 50, 140, 4)
    # the distant sail in the light break (tiny three-master)
    sx, sy = 1690, HZ
    b += f'<circle cx="{sx}" cy="{sy - 20}" r="70" fill="#fffbe6" opacity=".6" filter="url(#b14)"/>'
    b += (f'<g fill="#3a2a1a" opacity=".85"><path d="M{sx - 26},{sy - 2} L{sx + 28},{sy - 2} L{sx + 20},{sy + 4} L{sx - 20},{sy + 4}Z"/>'
          f'<path d="M{sx - 12},{sy - 6} L{sx - 12},{sy - 40} Q{sx - 2},{sy - 24} {sx - 12},{sy - 6}Z M{sx + 6},{sy - 6} L{sx + 6},{sy - 50} Q{sx + 18},{sy - 30} {sx + 6},{sy - 6}Z '
          f'M{sx + 22},{sy - 6} L{sx + 22},{sy - 30} Q{sx + 30},{sy - 18} {sx + 22},{sy - 6}Z"/></g>')
    # sandbank
    b += ('<path d="M420,812 C520,770 700,752 900,748 C1100,744 1300,740 1450,756 C1530,766 1580,790 1600,812 C1500,836 1300,848 1000,850 C760,850 560,840 420,812Z" fill="url(#sandA)" stroke="#2a1c10" stroke-width="5"/>')
    b += foam('M430,814 C560,842 760,856 1000,856 C1300,854 1500,840 1600,814', 9, .8, '#eef4e6')
    b += foam('M470,832 C620,866 800,872 1000,874 C1250,872 1440,860 1560,836', 5, .45, '#eef4e6')
    b += '<path d="M600,770 C800,750 1100,744 1440,758" fill="none" stroke="#ffe8b0" stroke-width="5" opacity=".7"/>'
    b += ''.join(f'<circle cx="{rnd.randint(520, 1560)}" cy="{rnd.randint(760, 840)}" r="{rnd.choice([1.6, 2.4])}" fill="#fff3d0" opacity=".55"/>' for _ in range(90))
    # broken mast with a torn sail (from the wreck), leaning like the raft's mast
    mb, mt = (930, 790), (900, 430)
    b += f'<path d="M{mb[0]},{mb[1]} L{mt[0]},{mt[1]}" stroke="#1a0f08" stroke-width="22" stroke-linecap="round"/><path d="M{mb[0]},{mb[1]} L{mt[0]},{mt[1]}" stroke="#6b4a2c" stroke-width="13" stroke-linecap="round"/>'
    b += f'<path d="M{mb[0] + 4},{mb[1]} L{mt[0] + 4},{mt[1]}" stroke="#f0b862" stroke-width="3" opacity=".8"/>'
    b += '<path d="M800,470 L1010,452" stroke="#1a0f08" stroke-width="13" stroke-linecap="round"/><path d="M800,470 L1010,452" stroke="#7a5532" stroke-width="7" stroke-linecap="round"/>'
    b += ('<path d="M808,474 C770,540 760,600 790,660 L812,640 L826,672 L850,646 L880,690 C900,620 960,540 1004,458 Z" fill="url(#sailA)" stroke="#2a1c10" stroke-width="5" stroke-linejoin="round"/>'
          '<path d="M840,500 C820,560 822,610 840,650 M900,488 C880,560 880,620 870,670" fill="none" stroke="#7a6444" stroke-width="3" opacity=".6"/>'
          '<path d="M1000,466 C966,540 920,620 884,684" fill="none" stroke="#ffe7b0" stroke-width="5" opacity=".85"/>')
    b += '<path d="M905,440 L640,800 M905,440 L1180,790" stroke="#2a1c10" stroke-width="3" opacity=".7"/>'
    # driftwood and wreck planks on the sand
    b += '<path d="M560,808 L700,796" stroke="#1a0f08" stroke-width="14" stroke-linecap="round"/><path d="M560,808 L700,796" stroke="#7a5532" stroke-width="8" stroke-linecap="round"/>'
    b += '<path d="M1450,792 L1530,806" stroke="#1a0f08" stroke-width="12" stroke-linecap="round"/><path d="M1450,792 L1530,806" stroke="#7a5532" stroke-width="6" stroke-linecap="round"/>'
    # signal fire with smoke drifting left
    b += '<ellipse cx="1000" cy="770" rx="260" ry="120" fill="url(#fireA)"/>'
    b += ''.join(f'<ellipse cx="{1000 - k * 70}" cy="{700 - k * 55}" rx="{50 + k * 22}" ry="{30 + k * 12}" fill="#8a7a66" opacity="{.42 - k * .06:.2f}" filter="url(#b14)"/>' for k in range(6))
    b += logs(1000, 790, .7) + flame(1000, 792, .72, sway=-14)
    b += ''.join(spark(1000 + dx, 640 + dy, 7, '#ffd27a') for dx, dy in ((-30, 0), (26, -36), (-6, -70)))
    # coral-stone heap (low stone building) + pyramid of castaways, the top one waving a cloth toward the sail
    b += ('<path d="M1110,800 L1140,720 L1190,690 L1240,640 L1300,616 L1352,630 L1392,690 L1420,760 L1440,804 Z" fill="#5c5448" stroke="#1a140e" stroke-width="5" stroke-linejoin="round"/>')
    for x, y, w, h in ((1150, 730, 70, 34), (1214, 690, 80, 34), (1272, 640, 74, 30), (1320, 676, 70, 34), (1360, 724, 66, 36), (1214, 744, 90, 40), (1300, 740, 70, 40), (1150, 770, 90, 32), (1340, 770, 90, 32)):
        b += f'<rect x="{x - w / 2:.0f}" y="{y - h / 2:.0f}" width="{w}" height="{h}" rx="9" fill="#8a7e6a" stroke="#1a140e" stroke-width="3.4"/>'
        b += f'<path d="M{x - w / 2 + 8:.0f},{y - h / 2 + 4:.0f} L{x + w / 2 - 6:.0f},{y - h / 2 + 4:.0f} L{x + w / 2 - 4:.0f},{y + h / 2 - 8:.0f}" fill="none" stroke="#f0c880" stroke-width="3.4" opacity=".8"/>'
        b += ''.join(f'<circle cx="{x + rnd.randint(-w // 3, w // 3)}" cy="{y + rnd.randint(-h // 4, h // 4)}" r="2.6" fill="#4a4236" opacity=".7"/>' for _ in range(3))
    rim = '#ffd690'
    b += person(1090, 806, 1.15, 'down', '#7a4a6a', rim=rim, sit=True)
    b += person(1170, 714, 1.2, 'point', '#3f6a7a', rim=rim)
    b += person(1240, 676, 1.25, 'up', '#a2563a', rim=rim)
    b += person(1380, 712, 1.15, 'carry', '#6a7a3a', rim=rim, flip=True)
    b += person(1430, 806, 1.1, 'down', '#8a5a2a', rim=rim, sit=True, flip=True)
    tx, ty = 1308, 620
    b += person(tx, ty, 1.35, 'wave', '#c9a24a', rim=rim)
    # waving cloth on a stick
    hx_, hy_ = tx + 19, ty - 58 * 1.35 - 6
    b += f'<path d="M{hx_:.0f},{hy_:.0f} L{hx_ + 26:.0f},{hy_ - 96:.0f}" stroke="#1a0f08" stroke-width="7" stroke-linecap="round"/><path d="M{hx_:.0f},{hy_:.0f} L{hx_ + 26:.0f},{hy_ - 96:.0f}" stroke="#8a6a3a" stroke-width="3.4" stroke-linecap="round"/>'
    fx, fy = hx_ + 26, hy_ - 96
    b += f'<path d="M{fx:.0f},{fy:.0f} C{fx + 30:.0f},{fy - 14:.0f} {fx + 56:.0f},{fy + 8:.0f} {fx + 92:.0f},{fy - 4:.0f} C{fx + 80:.0f},{fy + 22:.0f} {fx + 60:.0f},{fy + 40:.0f} {fx + 84:.0f},{fy + 52:.0f} C{fx + 50:.0f},{fy + 58:.0f} {fx + 30:.0f},{fy + 34:.0f} {fx + 6:.0f},{fy + 44:.0f} Z" fill="#f4ead2" stroke="#1a0f08" stroke-width="4" stroke-linejoin="round"/>'
    b += f'<path d="M{fx + 10:.0f},{fy + 10:.0f} C{fx + 36:.0f},{fy + 4:.0f} {fx + 56:.0f},{fy + 20:.0f} {fx + 80:.0f},{fy + 10:.0f}" fill="none" stroke="#c9a46a" stroke-width="3"/>'
    b += f'<circle cx="{fx + 50:.0f}" cy="{fy + 20:.0f}" r="70" fill="#fff4cc" opacity=".22" filter="url(#b26)"/>'
    b += spark(fx + 130, fy - 30, 20) + spark(1560, 560, 14) + spark(1210, 560, 12) + spark(760, 610, 12)
    # foreground waves
    # sailor frog on a floating barrel with a spyglass aimed at the sail
    barrel = ('<g transform="translate(6 18)"><ellipse cx="0" cy="0" rx="62" ry="22" fill="#6b4428" stroke-width="4"/><path d="M-62 0 L-58 36 Q0 56 58 36 L62 0" fill="#5a3820" stroke-width="4"/>'
              '<path d="M-60 16 Q0 34 60 16" fill="none" stroke="#3a3a3a" stroke-width="6"/><path d="M-50 -6 Q0 10 50 -6" fill="none" stroke="#c9945a" stroke-width="3" opacity=".7"/></g>')
    cap = ('<path d="M-14 -90 Q6 -114 26 -90 Z" fill="#f4f1e6" stroke-width="3.4"/><path d="M-18 -90 Q6 -84 30 -90 L30 -84 Q6 -78 -18 -84Z" fill="#2c4a7a" stroke-width="3"/>'
           '<path d="M-6 -104 q8 -5 16 -2" fill="none" stroke="#fff" stroke-width="2.4"/>'
           '<path d="M-24 -20 Q6 -8 36 -20 L32 -8 Q6 2 -20 -8Z" fill="#2c4a7a" stroke-width="3"/><path d="M0 -12 l6 10 l6 -10" fill="#d23a3a" stroke-width="2.4"/>')
    scope = ('<g transform="rotate(-14 40 -30)"><rect x="34" y="-40" width="64" height="18" rx="5" fill="#8a6a3a" stroke-width="3.4"/><rect x="92" y="-44" width="30" height="26" rx="5" fill="#d9b05a" stroke-width="3.4"/>'
             '<rect x="50" y="-40" width="6" height="18" fill="#d9b05a" stroke="none"/><path d="M40 -36 L118 -36" stroke="#fff3c0" stroke-width="2.4" opacity=".7"/></g>')
    b += f'<ellipse cx="300" cy="990" rx="170" ry="20" fill="#000" opacity=".35" filter="url(#b8)"/>'
    b += frog(300, 940, 2.5, look=(5, -3), mouth='O', brows=True, back=barrel, top=cap, armR='M38 -22 q14 -4 30 -14', front=scope)
    b += foam('M100,990 C200,974 300,996 420,978 C480,970 520,982 560,988', 6, .75, '#e6efe0')
    b += '<rect width="1920" height="1080" fill="url(#vigA)"/>'
    lines = [('LEFT', 196, 'w'), ('BEHIND', 214, 'y')]
    return page('#17140f', svg(defs, b), lines, outline='#120a04')


# ================================================== B: one fire on a speck of sand (intuitive) ==================================================
def thumb_B():
    rnd = random.Random(11)
    cx, cy = 1250, 640   # island centre
    fx, fy = 1220, 618   # fire
    HZ = 300
    defs = FILTERS
    defs += lin('skyB', [(0, '#050a18'), (1, '#122544')])
    defs += lin('seaB', [(0, '#0d2340'), (.3, '#081a30'), (1, '#030a16')])
    defs += rad('glowSea', fx, fy, 820, [(0, '#ffb45a', .55), (.25, '#ff8a3a', .22), (.6, '#2a4a7a', .08), (1, '#000', 0)])
    defs += rad('lagoon', fx, fy, 640, [(0, '#6ff0e0', .95), (.35, '#2fb5c0', .75), (.75, '#0d4a6a', .6), (1, '#0a2a4a', .4)])
    defs += rad('sandB', fx, fy, 560, [(0, '#fff2c8', 1), (.18, '#ffd590', 1), (.5, '#c9905a', 1), (.85, '#5a4a52', 1), (1, '#3a3446', 1)])
    defs += rad('haloB', fx, fy - 60, 420, [(0, '#fff3c0', .9), (.2, '#ffb84a', .55), (.55, '#ff7a2a', .15), (1, '#ff7a2a', 0)])
    defs += rad('vigB', 1150, 600, 1150, [(0, '#000', 0), (.55, '#000', 0), (1, '#000', .7)])
    b = '<rect width="1920" height="1080" fill="url(#skyB)"/>'
    b += ''.join(f'<circle cx="{rnd.randint(0, 1920)}" cy="{rnd.randint(8, HZ - 10)}" r="{rnd.choice([1.2, 1.8, 2.5])}" fill="#e8f0ff" opacity="{rnd.uniform(.25, .9):.2f}"/>' for _ in range(160))
    b += f'<rect x="0" y="{HZ - 30}" width="1920" height="60" fill="#3a5a8a" opacity=".35" filter="url(#b26)"/>'
    b += f'<rect x="0" y="{HZ}" width="1920" height="{1080 - HZ}" fill="url(#seaB)"/>'
    b += f'<rect x="0" y="{HZ}" width="1920" height="{1080 - HZ}" fill="url(#glowSea)"/>'
    # ocean swell lines (perspective: thin far, thick near), warmer near the fire
    for _ in range(170):
        y = rnd.randint(HZ + 6, 1060); x = rnd.randint(-40, 1900); k = (y - HZ) / (1080 - HZ)
        w = 30 + 140 * k; d = math.hypot((x - fx) / 1.6, y - fy)
        col = '#ffcf8a' if d < 520 else '#7fa8d8'
        b += f'<path d="M{x},{y} q{w * .25:.0f},{-w * .06:.0f} {w * .5:.0f},0 q{w * .25:.0f},{w * .05:.0f} {w * .5:.0f},0" fill="none" stroke="{col}" stroke-width="{1 + 3 * k:.1f}" stroke-linecap="round" opacity="{rnd.uniform(.12, .45):.2f}"/>'
    # reef ring: dark coral + surf, lagoon inside
    RX, RY = 640, 250
    b += f'<ellipse cx="{cx}" cy="{cy + 10}" rx="{RX + 30}" ry="{RY + 18}" fill="#0a2a3a" opacity=".7" filter="url(#b14)"/>'
    b += f'<ellipse cx="{cx}" cy="{cy}" rx="{RX}" ry="{RY}" fill="url(#lagoon)"/>'
    for i in range(110):
        a = 2 * math.pi * i / 110 + rnd.uniform(-.02, .02)
        x, y = cx + math.cos(a) * RX * rnd.uniform(.98, 1.03), cy + math.sin(a) * RY * rnd.uniform(.97, 1.04)
        d = math.hypot((x - fx) / 1.4, y - fy); bright = max(.25, 1 - d / 900)
        L = rnd.randint(18, 46); t = a + math.pi / 2
        b += f'<path d="M{x - math.cos(t) * L / 2:.0f},{y - math.sin(t) * L * .4 / 2:.0f} L{x + math.cos(t) * L / 2:.0f},{y + math.sin(t) * L * .4 / 2:.0f}" stroke="#f4fbff" stroke-width="{rnd.choice([4, 6, 8])}" stroke-linecap="round" opacity="{.9 * bright:.2f}"/>'
    b += f'<ellipse cx="{cx}" cy="{cy}" rx="{RX + 6}" ry="{RY + 4}" fill="none" stroke="#bff6ff" stroke-width="10" opacity=".25" filter="url(#b8)"/>'
    # coral heads in the lagoon
    for _ in range(40):
        a = rnd.uniform(0, 2 * math.pi); r = rnd.uniform(.72, .92)
        x, y = cx + math.cos(a) * RX * r, cy + math.sin(a) * RY * r
        b += f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{rnd.randint(8, 22)}" ry="{rnd.randint(4, 9)}" fill="#0d5a66" opacity=".6"/>'
    # sand island: thickness band + top
    isl = (f'M{cx - 470},{cy + 10} C{cx - 440},{cy - 80} {cx - 220},{cy - 130} {cx + 20},{cy - 128} C{cx + 260},{cy - 126} {cx + 470},{cy - 80} {cx + 480},{cy - 6} '
           f'C{cx + 470},{cy + 70} {cx + 260},{cy + 130} {cx + 10},{cy + 128} C{cx - 240},{cy + 126} {cx - 450},{cy + 90} {cx - 470},{cy + 10}Z')
    b += f'<path d="{isl}" fill="#b2e8e0" opacity=".55" transform="translate(0 16) scale(1.02)" transform-origin="{cx} {cy}" filter="url(#b8)"/>'
    b += f'<path d="{isl}" fill="#6a5040" transform="translate(0 16)"/>'
    b += f'<path d="{isl}" fill="url(#sandB)" stroke="#1a1410" stroke-width="5"/>'
    b += f'<path d="{isl}" fill="none" stroke="#fff6dc" stroke-width="6" opacity=".55" transform="translate(0 6)" filter="url(#b2)"/>'
    b += ''.join(f'<circle cx="{cx + rnd.randint(-420, 420)}" cy="{cy + rnd.randint(-100, 100)}" r="{rnd.choice([1.6, 2.4, 3])}" fill="#fff8e0" opacity="{rnd.uniform(.3, .8):.2f}"/>' for _ in range(160))
    # sand ripples
    b += ''.join(f'<path d="M{cx + dx},{cy + dy} q40,-10 80,0" fill="none" stroke="#7a5a42" stroke-width="3" opacity=".35"/>' for dx, dy in ((-380, 20), (-300, 70), (260, 60), (330, 0), (-200, -80), (180, -90), (-60, 96), (380, -40)))
    # low stone buildings (sandstone slabs + coral blocks), lit on the fire side, long shadows away from it
    def hut(x, y, w, h, d):
        side = 1 if x > fx else -1
        o = f'<path d="M{x - w / 2},{y} L{x + w / 2},{y} L{x + w / 2 + side * 140},{y + 26} L{x - w / 2 + side * 140},{y + 26}Z" fill="#1a1410" opacity=".45" filter="url(#b4)"/>'
        o += f'<path d="M{x - w / 2},{y} L{x - w / 2},{y - h} L{x - w / 2 + d},{y - h - d * .5} L{x + w / 2 + d},{y - h - d * .5} L{x + w / 2 + d},{y - d * .5} L{x + w / 2},{y}Z" fill="#6a6058" stroke="#1a140e" stroke-width="4" stroke-linejoin="round"/>'
        o += f'<rect x="{x - w / 2}" y="{y - h}" width="{w}" height="{h}" fill="#a69580" stroke="#1a140e" stroke-width="4"/>'
        o += ''.join(f'<path d="M{x - w / 2 + k * w / 4:.0f},{y - h} L{x - w / 2 + k * w / 4:.0f},{y}" stroke="#5a5046" stroke-width="2.4"/>' for k in (1, 2, 3))
        o += f'<path d="M{x - w / 2},{y - h} L{x - w / 2 + d},{y - h - d * .5} L{x + w / 2 + d},{y - h - d * .5} L{x + w / 2},{y - h}Z" fill="#d8ccb4" stroke="#1a140e" stroke-width="4" stroke-linejoin="round"/>'
        o += ''.join(f'<circle cx="{x - w / 2 + 10 + k * (w - 4) / 5:.0f}" cy="{y - h - d * .25:.0f}" r="5" fill="#efe6d2" stroke="#6a5a4a" stroke-width="1.6"/>' for k in range(5))
        lit = 'M{0},{1} L{0},{2}'.format(x + w / 2 if x < fx else x - w / 2, y, y - h)
        o += f'<path d="{lit}" stroke="#ffd690" stroke-width="5" opacity=".9"/>'
        o += f'<rect x="{x - 12}" y="{y - h * .7:.0f}" width="24" height="{h * .7:.0f}" rx="4" fill="#2a1c12"/>'
        return o
    b += hut(1010, 590, 110, 56, 30) + hut(1440, 580, 120, 58, 30) + hut(1340, 700, 100, 50, 26) + hut(1060, 708, 96, 48, 24)
    # well (stone ring)
    b += f'<ellipse cx="1520" cy="668" rx="36" ry="14" fill="#2a1c12" stroke="#1a140e" stroke-width="4"/><ellipse cx="1520" cy="664" rx="36" ry="14" fill="none" stroke="#c9b894" stroke-width="7"/>'
    # the fire: big halo, ember column, flame
    b += f'<ellipse cx="{fx}" cy="{fy - 60}" rx="420" ry="420" fill="url(#haloB)"/>'
    b += f'<ellipse cx="{fx}" cy="{fy + 8}" rx="120" ry="34" fill="#fff0b0" opacity=".55" filter="url(#b14)"/>'
    b += logs(fx, fy + 6, .9) + flame(fx, fy + 8, 1.1, sway=8)
    for k in range(26):
        y = fy - 140 - k * rnd.randint(14, 24); x = fx + math.sin(k * .7) * (10 + k * 3) + rnd.randint(-12, 12)
        b += f'<circle cx="{x:.0f}" cy="{y}" r="{rnd.choice([2, 3, 4])}" fill="#ffd27a" opacity="{max(.15, 1 - k / 28):.2f}"/>'
    b += spark(fx - 70, fy - 210, 16, '#fff0b0') + spark(fx + 90, fy - 280, 12, '#fff0b0')
    # castaways sitting around the fire (tiny, gentle)
    rim = '#ffcf7a'
    b += person(fx - 110, fy + 40, .9, 'down', '#7a4a6a', rim=rim, sit=True)
    b += person(fx + 112, fy + 44, .9, 'down', '#3f6a7a', rim=rim, sit=True, flip=True)
    b += person(fx + 40, fy - 44, .82, 'down', '#a2563a', rim=rim, sit=True, flip=True)
    b += person(fx - 200, fy - 30, .9, 'carry', '#6a7a3a', rim=rim)
    b += '<path d="M1010,550 l22,4" stroke="#1a0f08" stroke-width="7" stroke-linecap="round"/>'
    # sooty terns lit from below
    for x, y, s in ((1100, 330, 1.2), (1300, 270, 1.0), (1420, 360, 1.4), (980, 420, .9), (1560, 300, .8), (1220, 380, .8), (1650, 420, 1.1)):
        b += tern(x, y, s, '#141826', under='#ffb45a')
    # a turtle coming ashore
    b += '<g transform="translate(830 708) rotate(-8)"><ellipse cx="0" cy="0" rx="26" ry="16" fill="#3a5a3a" stroke="#0e1a0e" stroke-width="3.4"/><path d="M-12 -6 L0 -12 L12 -6 M-16 4 L16 4" stroke="#7a9a5a" stroke-width="2.4" fill="none"/><circle cx="30" cy="-2" r="7" fill="#4a6a4a" stroke="#0e1a0e" stroke-width="3"/></g>'
    # little sheep-head caravel (generic, no flags/emblems) with the sailor frog on deck, floating near the island
    INKS = '#140c06'
    b += '<ellipse cx="360" cy="1010" rx="300" ry="30" fill="#000" opacity=".45" filter="url(#b8)"/>'
    b += '<path d="M330,1000 L700,700" stroke="#ffb45a" stroke-width="0" />'
    # mast + sail (behind hull)
    b += f'<path d="M290,912 L290,540" stroke="{INKS}" stroke-width="18" stroke-linecap="round"/><path d="M290,912 L290,540" stroke="#7a5232" stroke-width="10" stroke-linecap="round"/>'
    b += f'<path d="M200,580 L380,580" stroke="{INKS}" stroke-width="12" stroke-linecap="round"/><path d="M200,580 L380,580" stroke="#8a6040" stroke-width="6" stroke-linecap="round"/>'
    b += (f'<path d="M206,586 C240,640 236,760 210,820 L370,820 C400,760 410,650 374,586 Z" fill="#f4ecd8" stroke="{INKS}" stroke-width="5" stroke-linejoin="round"/>'
          '<path d="M260,590 C280,660 278,760 262,816 M320,590 C340,660 342,760 326,816" stroke="#c9b894" stroke-width="3" fill="none"/>'
          '<path d="M372,592 C404,660 396,760 368,816" stroke="#ffcf7a" stroke-width="6" fill="none" opacity=".9"/>'
          f'<path d="M290,540 l0,-34 l42,12 l-42,12" fill="#f2d27a" stroke="{INKS}" stroke-width="4" stroke-linejoin="round"/>')
    b += f'<path d="M290,580 L560,872 M290,580 L120,890" stroke="{INKS}" stroke-width="3" opacity=".8"/>'
    # hull
    hull = 'M110,880 L560,880 Q600,880 610,860 Q600,960 520,1002 L190,1004 Q130,980 110,880 Z'
    b += f'<path d="{hull}" fill="#8a5a32" stroke="{INKS}" stroke-width="6" stroke-linejoin="round"/>'
    b += '<path d="M118,914 L596,914 M134,950 L578,950 M158,982 L548,982" stroke="#5a3820" stroke-width="4" fill="none"/>'
    b += f'<path d="M100,872 L566,872" stroke="{INKS}" stroke-width="16" stroke-linecap="round"/><path d="M100,872 L566,872" stroke="#d9a060" stroke-width="9" stroke-linecap="round"/>'
    b += ''.join(f'<circle cx="{x}" cy="930" r="13" fill="#3a2410" stroke="{INKS}" stroke-width="4"/><circle cx="{x}" cy="930" r="6" fill="#ffd27a" opacity=".85"/>' for x in (200, 290, 380, 470))
    b += '<path d="M560,880 Q598,880 606,868 Q600,940 540,990" fill="none" stroke="#ffcf7a" stroke-width="6" opacity=".85"/>'
    # rear cabin
    b += f'<rect x="114" y="828" width="96" height="46" rx="8" fill="#a8723e" stroke="{INKS}" stroke-width="5"/><rect x="140" y="840" width="22" height="22" rx="4" fill="#ffd27a" stroke="{INKS}" stroke-width="3"/>'
    # sheep-head figurehead at the bow, facing the island
    sx_, sy_ = 640, 820
    wool = ''.join(f'<circle cx="{sx_ + dx}" cy="{sy_ + dy}" r="{r}" fill="#f6f2e6" stroke="{INKS}" stroke-width="5"/>' for dx, dy, r in
                   ((-44, 10, 30), (-30, -30, 30), (6, -48, 30), (40, -30, 28), (-50, 44, 26), (-14, 50, 28)))
    b += f'<path d="M560,880 Q600,870 {sx_ - 30},{sy_ + 40}" stroke="{INKS}" stroke-width="30" stroke-linecap="round" fill="none"/><path d="M560,880 Q600,870 {sx_ - 30},{sy_ + 40}" stroke="#f6f2e6" stroke-width="20" stroke-linecap="round" fill="none"/>'
    b += wool
    b += ''.join(f'<circle cx="{sx_ + dx}" cy="{sy_ + dy}" r="{r}" fill="#f6f2e6"/>' for dx, dy, r in ((-36, 10, 26), (-24, -26, 25), (6, -42, 25), (36, -26, 23), (-40, 40, 22), (-12, 42, 24), (-10, 0, 34)))
    b += f'<ellipse cx="{sx_ + 28}" cy="{sy_ + 10}" rx="40" ry="34" fill="#efe1c4" stroke="{INKS}" stroke-width="5"/>'
    b += f'<path d="M{sx_ + 4},{sy_ - 22} c-30,-10 -40,22 -16,30 c16,4 22,-14 8,-16" fill="none" stroke="{INKS}" stroke-width="13" stroke-linecap="round"/><path d="M{sx_ + 4},{sy_ - 22} c-30,-10 -40,22 -16,30 c16,4 22,-14 8,-16" fill="none" stroke="#c98a4a" stroke-width="7" stroke-linecap="round"/>'
    b += f'<circle cx="{sx_ + 32}" cy="{sy_ + 2}" r="5.5" fill="{INKS}"/><circle cx="{sx_ + 34}" cy="{sy_}" r="1.8" fill="#fff"/>'
    b += f'<path d="M{sx_ + 52},{sy_ + 26} q8,6 16,0" fill="none" stroke="{INKS}" stroke-width="4" stroke-linecap="round"/><ellipse cx="{sx_ + 62}" cy="{sy_ + 14}" rx="5" ry="3.4" fill="#d98a8a"/>'
    b += f'<path d="M{sx_ + 62},{sy_ - 18} q14,-8 22,6" fill="none" stroke="#ffcf7a" stroke-width="5" opacity=".9"/>'
    # sailor frog standing on deck between mast and bow
    cap = ('<path d="M-14 -90 Q6 -114 26 -90 Z" fill="#f4f1e6" stroke-width="3.4"/><path d="M-18 -90 Q6 -84 30 -90 L30 -84 Q6 -78 -18 -84Z" fill="#2c4a7a" stroke-width="3"/>'
           '<path d="M-6 -104 q8 -5 16 -2" fill="none" stroke="#fff" stroke-width="2.4"/>'
           '<path d="M-24 -20 Q6 -8 36 -20 L32 -8 Q6 2 -20 -8Z" fill="#2c4a7a" stroke-width="3"/><path d="M0 -12 l6 10 l6 -10" fill="#d23a3a" stroke-width="2.4"/>')
    b += frog(440, 868, 2.15, look=(6, -2), mouth='O', brows=True, top=cap, armL='M-34 -22 q-14 6 -16 22', armR='M38 -22 q16 -14 22 -38')
    b += foam('M70,1004 C180,990 330,1012 460,994 C540,984 600,990 660,1000', 7, .55, '#9fc6e6')
    b += foam('M600,986 q30,-12 60,-4', 5, .5, '#9fc6e6')
    b += '<rect width="1920" height="1080" fill="url(#vigB)"/>'
    lines = [('THEY KEPT', 132, 'w'), ('THE', 104, 'w'), ('FIRE', 262, 'y')]
    return page('#050a18', svg(defs, b), lines, outline='#03060f')


# ================================================== C: the hourglass island (intuitive) ==================================================
def thumb_C():
    rnd = random.Random(23)
    cx = 1330; T, N, B = 140, 548, 948   # glass top, neck, bottom
    HZ = 770
    defs = FILTERS
    defs += lin('skyC', [(0, '#1e1a4a'), (.35, '#5a3a7a'), (.62, '#c45a7a'), (.85, '#ff9a6a'), (1, '#ffd08a')])
    defs += lin('seaC', [(0, '#e0907a'), (.08, '#3a6a8a'), (.5, '#123a5a'), (1, '#071a2e')])
    defs += rad('sunC', cx, HZ - 10, 700, [(0, '#fffbe6', 1), (.1, '#ffe7a0', .9), (.35, '#ffb06a', .35), (1, '#ff8a6a', 0)])
    defs += lin('sandTop', [(0, '#ffe7a6'), (1, '#d79a52')])
    defs += lin('miniSea', [(0, '#5ff0e0'), (.5, '#1aa0b8'), (1, '#0a4a6a')])
    defs += lin('woodC', [(0, '#a26a3a'), (.5, '#6b4224'), (1, '#3a2010')])
    defs += lin('glassC', [(0, '#ffffff'), (.5, '#bfe8ff'), (1, '#ffffff')], x2=1, y2=0)
    defs += rad('vigC', 1150, 560, 1150, [(0, '#000', 0), (.6, '#000', 0), (1, '#000', .58)])
    bulb = (f'M{cx - 34},{T} C{cx - 330},{T + 30} {cx - 300},{N - 150} {cx - 16},{N} C{cx - 300},{N + 150} {cx - 330},{B - 30} {cx - 34},{B} '
            f'L{cx + 34},{B} C{cx + 330},{B - 30} {cx + 300},{N + 150} {cx + 16},{N} C{cx + 300},{N - 150} {cx + 330},{T + 30} {cx + 34},{T} Z')
    defs += f'<clipPath id="bulbC"><path d="{bulb}"/></clipPath>'
    b = '<rect width="1920" height="1080" fill="url(#skyC)"/>'
    for x, y, rx, o in ((400, 300, 420, .35), (900, 420, 360, .3), (1750, 360, 300, .35), (1600, 560, 320, .4), (500, 600, 380, .35)):
        b += f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{rx * .07:.0f}" fill="#ffc0a0" opacity="{o}" filter="url(#b8)"/>'
    b += ''.join(f'<circle cx="{rnd.randint(0, 1920)}" cy="{rnd.randint(10, 300)}" r="{rnd.choice([1.2, 1.8, 2.4])}" fill="#fff" opacity="{rnd.uniform(.2, .7):.2f}"/>' for _ in range(70))
    b += '<rect width="1920" height="1080" fill="url(#sunC)"/>'
    b += f'<rect x="0" y="{HZ}" width="1920" height="{1080 - HZ}" fill="url(#seaC)"/>'
    b += f'<path d="M{cx - 120},{HZ} L{cx + 120},{HZ} L{cx + 420},1080 L{cx - 420},1080Z" fill="#ffe0a0" opacity=".22" filter="url(#b26)"/>'
    b += ''.join(f'<rect x="{rnd.randint(cx - 380, cx + 380)}" y="{rnd.randint(HZ + 4, 1000)}" width="{rnd.randint(20, 90)}" height="3" rx="1.5" fill="#fff1c8" opacity="{rnd.uniform(.3, .85):.2f}"/>' for _ in range(60))
    b += waves(rnd, 60, -40, 1900, HZ + 14, 1060, '#bcd8ef', (.15, .45), 40, 120, 3.4)
    # distant tiny sandbanks on the horizon
    b += f'<path d="M200,{HZ} q60,-10 140,0Z M1720,{HZ} q40,-7 100,0Z" fill="#3a2a3a" opacity=".6"/>'
    for x, y, s in ((380, 560, 1.0), (470, 520, .7), (1700, 480, 1.1), (1790, 540, .8), (980, 620, .7)):
        b += tern(x, y, s, '#2a1830', under='#ffc08a')
    # sandbar the hourglass stands on
    b += ('<path d="M820,1010 C900,970 1100,958 1330,958 C1520,958 1680,972 1730,1012 C1640,1046 1500,1056 1330,1056 C1100,1056 920,1046 820,1010Z" fill="#e6c48a" stroke="#2a1c10" stroke-width="5"/>'
          + foam('M820,1012 C920,1048 1100,1060 1330,1060 C1540,1060 1660,1048 1730,1014', 8, .8, '#fff4ea'))
    # glow behind the glass (backlit by the sun)
    b += f'<ellipse cx="{cx}" cy="{N + 80}" rx="420" ry="460" fill="#fff0c0" opacity=".28" filter="url(#b90)"/>'
    # back post
    # glass contents
    g = f'<g clip-path="url(#bulbC)">'
    g += f'<rect x="{cx - 340}" y="{T}" width="680" height="{B - T}" fill="#ffe8d0" opacity=".16"/>'
    # top sand (with a dip in the middle)
    g += f'<path d="M{cx - 340},{N - 250} C{cx - 200},{N - 250} {cx - 60},{N - 200} {cx - 10},{N - 4} L{cx + 10},{N - 4} C{cx + 60},{N - 200} {cx + 200},{N - 250} {cx + 340},{N - 250} L{cx + 340},{N} L{cx - 340},{N}Z" fill="url(#sandTop)"/>'
    g += f'<path d="M{cx - 300},{N - 252} C{cx - 200},{N - 250} {cx - 60},{N - 200} {cx - 10},{N - 4}" fill="none" stroke="#fff6d8" stroke-width="5" opacity=".8"/>'
    # falling sand stream
    g += f'<path d="M{cx - 4},{N} L{cx + 4},{N} L{cx + 7},{N + 230} L{cx - 7},{N + 230}Z" fill="#ffe2a0"/><rect x="{cx - 10}" y="{N}" width="20" height="230" fill="#fff4c0" opacity=".4" filter="url(#b4)"/>'
    g += ''.join(f'<circle cx="{cx + rnd.randint(-14, 14)}" cy="{rnd.randint(N + 10, N + 230)}" r="2" fill="#fff6d0"/>' for _ in range(24))
    # the mini world in the lower bulb: sea + island + stone hut + fire + terns
    g += f'<rect x="{cx - 340}" y="{N + 280}" width="680" height="{B - N}" fill="url(#miniSea)"/>'
    g += ''.join(f'<path d="M{cx + dx},{N + dy} q12,-5 24,0 q12,5 24,0" fill="none" stroke="#dffcff" stroke-width="3" opacity=".7"/>' for dx, dy in ((-220, 310), (150, 320), (-160, 360), (200, 370), (-60, 380)))
    g += f'<path d="M{cx - 250},{N + 304} C{cx - 160},{N + 250} {cx - 50},{N + 196} {cx},{N + 190} C{cx + 60},{N + 196} {cx + 170},{N + 250} {cx + 260},{N + 304} C{cx + 140},{N + 326} {cx - 120},{N + 326} {cx - 250},{N + 304}Z" fill="#f6dca0" stroke="#3a2a14" stroke-width="4"/>'
    g += f'<path d="M{cx - 250},{N + 306} C{cx - 120},{N + 330} {cx + 140},{N + 330} {cx + 260},{N + 306}" fill="none" stroke="#fff" stroke-width="7" opacity=".85"/>'
    g += f'<path d="M{cx - 190},{N + 272} C{cx - 110},{N + 232} {cx - 40},{N + 200} {cx},{N + 196}" fill="none" stroke="#fffbe6" stroke-width="4" opacity=".8"/>'
    # hut
    hx, hy = cx - 130, N + 290
    g += f'<rect x="{hx - 50}" y="{hy - 42}" width="100" height="42" fill="#a69580" stroke="#1a140e" stroke-width="3.6"/><path d="M{hx - 50},{hy - 42} L{hx - 36},{hy - 56} L{hx + 64},{hy - 56} L{hx + 50},{hy - 42}Z" fill="#d8ccb4" stroke="#1a140e" stroke-width="3.6"/>'
    g += f'<path d="M{hx + 50},{hy - 42} L{hx + 64},{hy - 56} L{hx + 64},{hy - 14} L{hx + 50},{hy}Z" fill="#7a6e60" stroke="#1a140e" stroke-width="3.6"/>'
    g += ''.join(f'<circle cx="{hx - 40 + k * 20}" cy="{hy - 49}" r="5" fill="#efe6d2" stroke="#6a5a4a" stroke-width="1.6"/>' for k in range(5))
    g += f'<rect x="{hx - 11}" y="{hy - 30}" width="22" height="30" fill="#2a1c12"/>'
    # fire
    ffx, ffy = cx + 110, N + 280
    g += f'<circle cx="{ffx}" cy="{ffy - 30}" r="90" fill="#ffb84a" opacity=".6" filter="url(#b14)"/>'
    g += logs(ffx, ffy, .45) + flame(ffx, ffy + 2, .52, sway=4)
    g += person(ffx - 62, ffy + 14, .68, 'down', '#a2563a', rim='#ffcf7a', sit=True, flip=False)
    g += person(ffx + 70, ffy + 18, .68, 'carry', '#3f6a7a', rim='#ffcf7a', flip=True)
    for x, y, s in ((cx - 120, N + 170, .6), (cx + 140, N + 140, .5), (cx + 60, N + 200, .4)):
        g += tern(x, y, s, '#2a2a3a')
    g += '</g>'
    b += g
    # glass: tint, rim light, highlights
    b += f'<path d="{bulb}" fill="#cfefff" fill-opacity=".08" stroke="#0e1a2a" stroke-width="7"/>'
    b += f'<path d="{bulb}" fill="none" stroke="#fff6e0" stroke-width="3" opacity=".9"/>'
    b += f'<path d="M{cx - 250},{T + 80} C{cx - 280},{T + 180} {cx - 230},{N - 140} {cx - 120},{N - 70}" fill="none" stroke="#fff" stroke-width="14" stroke-linecap="round" opacity=".7"/>'
    b += f'<path d="M{cx - 250},{N + 120} C{cx - 290},{N + 220} {cx - 260},{B - 120} {cx - 180},{B - 60}" fill="none" stroke="#fff" stroke-width="12" stroke-linecap="round" opacity=".55"/>'
    b += f'<path d="M{cx + 220},{T + 110} C{cx + 250},{T + 180} {cx + 230},{N - 160} {cx + 170},{N - 110}" fill="none" stroke="#fff" stroke-width="6" stroke-linecap="round" opacity=".5"/>'
    b += f'<ellipse cx="{cx - 170}" cy="{T + 120}" rx="34" ry="16" transform="rotate(-50 {cx - 170} {T + 120})" fill="#fff" opacity=".85"/>'
    # wooden caps and front posts
    for y0 in (T - 52, B):
        b += f'<rect x="{cx - 330}" y="{y0}" width="660" height="52" rx="14" fill="url(#woodC)" stroke="#1a0e06" stroke-width="5"/>'
        b += f'<path d="M{cx - 316},{y0 + 10} L{cx + 316},{y0 + 10}" stroke="#e8b47a" stroke-width="4" opacity=".7"/>'
        b += f'<path d="M{cx - 280},{y0 + 30} q80,-6 160,0 M{cx + 40},{y0 + 34} q90,-6 180,0" stroke="#3a2010" stroke-width="2.6" fill="none" opacity=".7"/>'
    for px_ in (cx - 300, cx + 300):
        b += f'<path d="M{px_ - 13},{T} L{px_ + 13},{T} Q{px_ + 22},{N} {px_ + 13},{B} L{px_ - 13},{B} Q{px_ - 22},{N} {px_ - 13},{T}Z" fill="url(#woodC)" stroke="#1a0e06" stroke-width="4.4"/>'
        for yy in (T + 40, N, B - 40):
            b += f'<ellipse cx="{px_}" cy="{yy}" rx="22" ry="11" fill="#7a4a24" stroke="#1a0e06" stroke-width="4"/>'
        b += f'<path d="M{px_ + 8},{T + 10} Q{px_ + 14},{N} {px_ + 8},{B - 10}" stroke="#ffcf8a" stroke-width="3.4" fill="none" opacity=".8"/>'
    # 15 tally marks scratched on the bottom cap
    tal = ''
    for gi in range(3):
        x0 = cx - 250 + gi * 74
        for k in range(4):
            tal += f'M{x0 + k * 12},{B + 12} L{x0 + k * 12 - 2},{B + 42} '
        tal += f'M{x0 - 8},{B + 34} L{x0 + 46},{B + 18} '
    b += f'<path d="{tal}" stroke="#f6e2b0" stroke-width="5" stroke-linecap="round"/>'
    b += spark(cx - 360, 240, 22) + spark(cx + 390, 330, 18) + spark(cx + 60, N - 300, 14) + spark(cx + 260, B - 80, 14) + spark(940, 700, 12)
    # frog with a bandana, scratching the tallies with a shell, standing on the sandbar
    band = ('<path d="M-30 -22 Q6 -8 42 -22 L40 -10 Q6 2 -28 -10Z" fill="#d23a3a" stroke-width="3"/>'
            '<path d="M2 -8 l-10 22 l18 -4 Z" fill="#d23a3a" stroke-width="3"/><circle cx="-14" cy="-14" r="2.4" fill="#fff" stroke="none"/><circle cx="20" cy="-13" r="2.4" fill="#fff" stroke="none"/><circle cx="4" cy="-9" r="2.4" fill="#fff" stroke="none"/>')
    shell = '<path d="M62 -40 l18 -10 l4 16 Z" fill="#ffd8c0" stroke-width="3"/>'
    b += f'<ellipse cx="900" cy="1020" rx="110" ry="14" fill="#5a3a20" opacity=".45" filter="url(#b4)"/>'
    b += frog(890, 1014, 2.45, look=(6, -3), mouth='O', brows=True, mid=band, armR='M38 -22 q30 -2 44 -14', front=shell.replace('62 -40', '78 -34'))
    b += '<rect width="1920" height="1080" fill="url(#vigC)"/>'
    lines = [('15 YEARS', 182, 'y'), ('ON SAND', 168, 'w')]
    return page('#1e1a4a', svg(defs, b), lines, outline='#120a24')


for n, fn in (('A', thumb_A), ('B', thumb_B), ('C', thumb_C)):
    open(os.path.join(HERE, f'{n}.html'), 'w').write(fn())
print('ok')
