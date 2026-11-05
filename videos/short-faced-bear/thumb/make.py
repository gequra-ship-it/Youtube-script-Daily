# Thumbnails A-C for short-faced-bear (guideline 16-6 / 16-8, brief tools/briefs/thumb_art.md). Run: python3 videos/short-faced-bear/thumb/make.py
# A  TOO BIG TO SURVIVE?  homage: Caspar David Friedrich, "Wanderer above the Sea of Fog" (1818, public domain): the giant bear stands on its
#                         hind legs on a crag, back to us, over a sea of fog where spruce forest pokes through; dawn sun behind it; the frog
#                         (scarf) sits on a ledge looking up. Script S47-S48 ("the very traits that made Arctodus so formidable may have helped
#                         doom it"), S50-S52 (steppe gives way to forests), S72 lesson. Question form keeps it hedged.
# B  ABOUT 3.5 M TALL     intuitive: the bear rearing beside a small snow cabin, a person and a red-white snow pole for scale; the frog
#                         (beanie) peeks from the doorway. Script S17-S18 ("may have stood around three and a half meters tall", rough figures).
# C  ICE AGE BULLY?       intuitive: the bear emerges from the mist and puts a paw on the dire wolves' kill (drawn as a cartoon meat bone, no
#                         gore); the wolves back off with tails down; the frog peeks from behind a rock. Script S36-S41 (kleptoparasite
#                         hypothesis, "greatest bully of the Ice Age", "a possibility, not something the fossils prove") -> question mark.
import os, sys, math, random
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', '..', 'tools'))
from thumb_lib import page, svg, lin, rad, spark
from figlib import person

INK = '#1d2b1c'; GREEN = '#6aa55a'; DARKG = '#4d8a4a'; BELLY = '#9cc98a'
BINK = '#1c1009'
FILTERS = ''.join(f'<filter id="b{n}" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="{n}"/></filter>' for n in (2, 3, 6, 12, 24, 50, 80))


# ---------------- mascot frog (tools/assets/frog.svg body), posable ----------------
def limb(d, w=7.5, wi=3.4):
    return f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="{w}"/><path d="{d}" fill="none" stroke="{GREEN}" stroke-width="{wi}"/>'


def end_of(d):
    n = [float(v) for v in d.replace('M', ' ').replace('q', ' ').split()]
    return n[0] + n[-2], n[1] + n[-1]


SCARF = ('<path d="M-36 -26 q38 14 80 -2 l2 14 q-42 16 -84 2z" fill="#c8483a" stroke-width="3"/>'
         '<path d="M-30 -18 q36 10 70 -2" fill="none" stroke="#f2a08a" stroke-width="2.4" opacity=".8"/>'
         '<path d="M-26 -16 l-12 34 l14 3 l8 -30z" fill="#b23c30" stroke-width="3"/>'
         '<path d="M-36 14 l2 8 M-30 15 l1 8 M-24 16 l0 7" fill="none" stroke-width="2"/>')
BEANIE = ('<path d="M-30 -80 q4 -44 38 -46 q34 0 38 46z" fill="#3f6fb0" stroke-width="3.4"/>'
          '<path d="M-14 -118 q4 -10 14 -10" fill="none" stroke="#9cc0ee" stroke-width="3" opacity=".8"/>'
          '<rect x="-34" y="-86" width="80" height="16" rx="7" fill="#e8eef6" stroke-width="3.2"/>'
          '<circle cx="8" cy="-130" r="11" fill="#e8eef6" stroke-width="3"/>'
          '<path d="M-14 -96 l0 -14 M0 -100 l0 -16 M16 -100 l0 -16 M30 -96 l0 -12" fill="none" stroke="#2c548c" stroke-width="2.4"/>')


def frog(x, y, s, rot=0, flip=False, look=(0, 0), mouth='O', armL=None, armR=None, legs=None, brows=True, back="", front="", shadow=False, mid="", head=""):
    sx = -s if flip else s
    g = [f'<g transform="translate({x} {y}) rotate({rot}) scale({sx} {s})" stroke="{INK}" stroke-linejoin="round" stroke-linecap="round">', back]
    if shadow:
        g.append('<ellipse cx="0" cy="8" rx="52" ry="8" fill="#000" opacity=".28" stroke="none"/>')
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
        g.append('<ellipse cx="6" cy="-38" rx="9" ry="11" fill="#7a2f33" stroke-width="3"/><ellipse cx="6" cy="-32" rx="5.5" ry="3.6" fill="#e07b7b" stroke="none"/>')
    else:
        g.append('<ellipse cx="6" cy="-41" rx="6" ry="7.5" fill="#7a2f33" stroke-width="3"/>')
    g.append('<ellipse cx="-18" cy="-48" rx="5" ry="3" fill="#e98a8a" stroke="none" opacity=".55"/><ellipse cx="30" cy="-48" rx="5" ry="3" fill="#e98a8a" stroke="none" opacity=".55"/>')
    g.append(head)
    g.append(mid)
    for a in (armL or 'M-34 -22 q-14 6 -16 22', armR or 'M38 -22 q14 6 16 22'):
        g.append(limb(a)); ex_, ey_ = end_of(a)
        g.append(f'<circle cx="{ex_:.1f}" cy="{ey_:.1f}" r="5.6" fill="{GREEN}" stroke-width="3"/>')
    g.append(front); g.append('</g>')
    return ''.join(g)


# ---------------- furred shape helper: gradient body, clipped fur strokes, inner rim light, ink outline ----------------
def furred(uid, d, bbox, base, dark, light, rim, light_dir, rnd, n=260, lw=6, rimw=18, rimop=1.0, fur_len=(14, 30), flow=90, extra=''):
    """d = path; bbox = (x0,y0,x1,y1); light_dir = (dx,dy) unit-ish vector pointing TO the light; flow = mean fur stroke angle (deg, 90 = down)."""
    x0, y0, x1, y1 = bbox; cx, cy = (x0 + x1) / 2, (y0 + y1) / 2; hw, hh = (x1 - x0) / 2, (y1 - y0) / 2
    lx, ly = light_dir
    gx1, gy1, gx2, gy2 = cx + lx * hw, cy + ly * hh, cx - lx * hw, cy - ly * hh
    defs = (f'<clipPath id="c{uid}"><path d="{d}"/></clipPath>'
            f'<linearGradient id="g{uid}" gradientUnits="userSpaceOnUse" x1="{gx1:.0f}" y1="{gy1:.0f}" x2="{gx2:.0f}" y2="{gy2:.0f}">'
            f'<stop offset="0" stop-color="{light}"/><stop offset=".45" stop-color="{base}"/><stop offset="1" stop-color="{dark}"/></linearGradient>'
            f'<linearGradient id="r{uid}" gradientUnits="userSpaceOnUse" x1="{gx1:.0f}" y1="{gy1:.0f}" x2="{cx:.0f}" y2="{cy:.0f}">'
            f'<stop offset="0" stop-color="{rim}" stop-opacity="{rimop}"/><stop offset=".55" stop-color="{rim}" stop-opacity="{rimop * .35:.2f}"/><stop offset="1" stop-color="{rim}" stop-opacity="0"/></linearGradient>')
    o = f'<path d="{d}" fill="url(#g{uid})"/>'
    o += f'<g clip-path="url(#c{uid})">'
    for _ in range(n):
        x = rnd.uniform(x0, x1); y = rnd.uniform(y0, y1)
        a = math.radians(flow + rnd.uniform(-28, 28)); L = rnd.uniform(*fur_len)
        bend = rnd.uniform(-6, 6)
        # stroke colour by side: lit side gets light hairs, shade side dark
        side = ((x - cx) / hw) * lx + ((y - cy) / hh) * ly
        col = light if (side > .15 and rnd.random() < .7) else dark
        op = rnd.uniform(.25, .6)
        o += (f'<path d="M{x:.0f} {y:.0f} q{L * .5 * math.cos(a) + bend:.1f} {L * .5 * math.sin(a):.1f} {L * math.cos(a):.1f} {L * math.sin(a):.1f}" '
              f'fill="none" stroke="{col}" stroke-width="{rnd.choice([2.6, 3.4, 4.2])}" stroke-linecap="round" opacity="{op:.2f}"/>')
    o += extra
    o += f'<path d="{d}" fill="none" stroke="url(#r{uid})" stroke-width="{rimw}"/>'
    o += '</g>'
    o += f'<path d="{d}" fill="none" stroke="{BINK}" stroke-width="{lw}" stroke-linejoin="round"/>'
    return defs, o


def tufts(pts, col, rnd, w=4, L=(10, 20)):
    """little fur spikes sticking out along a list of (x, y, nx, ny) normal points"""
    o = ''
    for x, y, nx, ny in pts:
        Lz = rnd.uniform(*L)
        o += (f'<path d="M{x - ny * 6:.0f} {y + nx * 6:.0f} L{x + nx * Lz:.0f} {y + ny * Lz:.0f} L{x + ny * 6:.0f} {y - nx * 6:.0f}" '
              f'fill="{col}" stroke="{BINK}" stroke-width="{w}" stroke-linejoin="round"/>')
    return o


def claws(pts, col='#efe4cc', line=BINK, s=1.0):
    o = ''
    for x, y, ang in pts:
        o += (f'<path transform="translate({x} {y}) rotate({ang}) scale({s})" d="M-6 0 Q-6 18 4 30 Q2 14 6 0 Z" fill="{col}" stroke="{line}" stroke-width="3" stroke-linejoin="round"/>')
    return o


def snow_spruce(x, base, h, col, snow=None, op=1.0):
    w = h * .38; o = f'<g opacity="{op}">'
    o += f'<rect x="{x - h * .03:.0f}" y="{base - h * .12:.0f}" width="{h * .06:.0f}" height="{h * .12:.0f}" fill="{col}"/>'
    for k in range(4):
        t = k / 4; yy = base - h * .1 - t * h * .8; ww = w * (1 - t * .7)
        o += f'<path d="M{x - ww:.0f} {yy:.0f} L{x:.0f} {yy - h * .35:.0f} L{x + ww:.0f} {yy:.0f} Z" fill="{col}"/>'
        if snow:
            o += f'<path d="M{x - ww * .55:.0f} {yy - h * .1:.0f} L{x:.0f} {yy - h * .33:.0f} L{x + ww * .3:.0f} {yy - h * .14:.0f} Z" fill="{snow}" opacity=".85"/>'
    return o + '</g>'


# ============================================================ A: Wanderer above the Sea of Fog ============================================
def make_A():
    rnd = random.Random(11)
    d = FILTERS
    d += lin('skyA', [(0, '#2c3a5c'), (.3, '#5d6a8a'), (.52, '#c99a8e'), (.66, '#f4cf98'), (1, '#f8e2b0')])
    d += rad('sunA', 1290, 470, 760, [(0, '#fff8de', 1), (.1, '#ffe7a8', .85), (.3, '#f6c27a', .45), (.6, '#e89a6a', .15), (1, '#e89a6a', 0)])
    d += lin('rockA', [(0, '#4a3d44'), (.5, '#2c2228'), (1, '#140e12')])
    d += lin('fogA', [(0, '#fbe9cc'), (1, '#c9c4d0')])
    d += rad('vigA', 960, 540, 1150, [(0, '#000', 0), (.7, '#000', 0), (1, '#0a0610', .55)])
    b = '<rect width="1920" height="1080" fill="url(#skyA)"/>'
    b += '<rect width="1920" height="1080" fill="url(#sunA)"/>'
    # thin dawn cloud streaks
    for y, x0, x1, op in ((150, 900, 1900, .25), (230, 1150, 1920, .3), (310, 700, 1500, .22), (390, 1450, 1920, .3), (120, 300, 1000, .18)):
        b += f'<path d="M{x0} {y} Q{(x0 + x1) / 2} {y - 18} {x1} {y} Q{(x0 + x1) / 2} {y + 12} {x0} {y}Z" fill="#ffd9a8" opacity="{op}"/>'
    # distant mountains (left and right) half drowned in fog
    b += '<path d="M-20 640 L90 520 L170 560 L260 450 L330 500 L420 430 L520 520 L620 560 L720 620 L-20 700Z" fill="#8f8aa6" opacity=".75"/>'
    b += '<path d="M260 450 L300 480 L330 500 M420 430 L460 470" fill="none" stroke="#fff0d8" stroke-width="5" opacity=".6"/>'
    b += '<path d="M1500 640 L1580 540 L1650 570 L1740 470 L1820 520 L1880 480 L1940 500 L1940 700 L1500 700Z" fill="#9a90a8" opacity=".7"/>'
    b += '<path d="M1580 540 L1620 556 M1740 470 L1780 500" fill="none" stroke="#fff0d8" stroke-width="5" opacity=".6"/>'
    # far fog sea
    b += '<rect x="0" y="600" width="1920" height="480" fill="url(#fogA)" opacity=".55"/>'
    for _ in range(26):
        x = rnd.uniform(-100, 2000); y = rnd.uniform(600, 760)
        b += f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{rnd.uniform(140, 320):.0f}" ry="{rnd.uniform(30, 60):.0f}" fill="#fff3dc" opacity="{rnd.uniform(.3, .6):.2f}" filter="url(#b12)"/>'
    # spruce forest poking through the fog (the forest that replaced the open steppe)
    for k in range(34):
        x = rnd.uniform(0, 1920)
        if 1080 < x < 1480:
            continue
        base = rnd.uniform(700, 760); h = rnd.uniform(60, 120)
        b += snow_spruce(x, base, h, '#5d6278', op=.75)
    for _ in range(22):
        x = rnd.uniform(-100, 2000); y = rnd.uniform(720, 900)
        b += f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{rnd.uniform(160, 360):.0f}" ry="{rnd.uniform(36, 70):.0f}" fill="#fff6e6" opacity="{rnd.uniform(.4, .75):.2f}" filter="url(#b12)"/>'
    # near spruce tips (bigger, darker)
    for x, base, h in ((620, 860, 170), (720, 880, 210), (1650, 870, 200), (1760, 860, 160), (90, 900, 190), (1880, 900, 230)):
        b += snow_spruce(x, base, h, '#433f52', op=.85)
    for _ in range(14):
        x = rnd.uniform(-100, 2000); y = rnd.uniform(860, 1080)
        b += f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{rnd.uniform(200, 420):.0f}" ry="{rnd.uniform(40, 80):.0f}" fill="#fff8ee" opacity="{rnd.uniform(.5, .8):.2f}" filter="url(#b12)"/>'
    # halo behind the bear
    b += '<circle cx="1290" cy="470" r="70" fill="#fffbe8"/>'
    b += '<circle cx="1290" cy="470" r="150" fill="#fff0c0" opacity=".55" filter="url(#b24)"/>'
    for k in range(14):  # sun rays
        a = math.radians(k * 360 / 14 + 8)
        b += (f'<path d="M1290 470 L{1290 + math.cos(a - .05) * 900:.0f} {470 + math.sin(a - .05) * 900:.0f} L{1290 + math.cos(a + .05) * 900:.0f} {470 + math.sin(a + .05) * 900:.0f}Z" '
              f'fill="#fff2cc" opacity=".09"/>')
    # ---- the crag (bear group scaled up 1.15 around the crag base) ----
    b += '<g transform="translate(1240 900) scale(1.15) translate(-1240 -900)">'
    crag = 'M860 1080 L900 1000 L960 950 L1000 912 L1080 908 L1110 860 L1150 815 L1200 806 L1330 806 L1380 830 L1430 880 L1500 930 L1560 990 L1610 1080 Z'
    b += f'<path d="{crag}" fill="url(#rockA)" stroke="#0e0a0c" stroke-width="6" stroke-linejoin="round"/>'
    for f_ in ('M1150 815 L1200 806 L1240 860 L1180 900 Z', 'M1330 806 L1380 830 L1350 900 L1290 870 Z', 'M960 950 L1000 912 L1080 908 L1060 980 L980 1000 Z',
               'M1430 880 L1500 930 L1450 980 L1400 940 Z', 'M1180 900 L1240 860 L1290 870 L1350 900 L1300 980 L1200 990 Z'):
        b += f'<path d="{f_}" fill="#5a4a50" opacity=".55"/>'
    for f_ in ('M1110 860 L1150 815 L1180 900 L1120 950 Z', 'M1300 980 L1350 900 L1400 940 L1380 1040 Z', 'M900 1000 L960 950 L980 1000 L930 1060 Z'):
        b += f'<path d="{f_}" fill="#0c080a" opacity=".5"/>'
    b += '<path d="M1110 860 L1150 815 L1200 806 L1330 806 L1380 830 L1430 880 L1500 930" fill="none" stroke="#ffcf8a" stroke-width="5" opacity=".75"/>'
    b += '<path d="M960 950 L1000 912 L1080 908" fill="none" stroke="#ffcf8a" stroke-width="4" opacity=".6"/>'
    for _ in range(40):
        x = rnd.uniform(930, 1520); y = rnd.uniform(880, 1060)
        b += f'<path d="M{x:.0f} {y:.0f} l{rnd.uniform(-30, 30):.0f} {rnd.uniform(6, 22):.0f}" stroke="#0b0709" stroke-width="3" opacity=".45"/>'
    # ---- the bear, standing on its hind legs, seen from behind, head turned right (Wanderer pose) ----
    bd = ''
    body = ('M1150 812 C1135 760 1118 700 1110 650 C1098 590 1096 520 1104 470 C1090 420 1094 360 1130 318 '
            'C1165 285 1205 272 1240 274 C1280 276 1320 290 1345 320 C1372 360 1375 420 1362 470 C1372 530 1372 600 1360 650 '
            'C1352 700 1340 760 1326 812 L1262 812 C1258 762 1250 724 1238 706 C1226 724 1220 762 1216 812 Z')
    df, of = furred('Abody', body, (1090, 270, 1380, 812), '#4a2c18', '#24140b', '#8a5634', '#ffd28a', (0, -1), rnd, n=520, rimw=26, flow=95)
    d += df
    bd += f'<path d="{body}" fill="none" stroke="#ffe0a0" stroke-width="30" opacity=".55" filter="url(#b12)"/>'
    bd += of
    # rump / leg split shading
    bd += '<path d="M1238 706 C1236 650 1238 600 1240 560" fill="none" stroke="#1a0e07" stroke-width="5" opacity=".6"/>'
    bd += '<path d="M1150 660 Q1190 690 1236 700 Q1290 690 1330 660" fill="none" stroke="#1a0e07" stroke-width="5" opacity=".45"/>'
    # hind paws (heels), claws hidden
    bd += '<path d="M1146 806 Q1180 822 1218 810" fill="none" stroke="#0e0805" stroke-width="10"/><path d="M1262 810 Q1296 824 1330 806" fill="none" stroke="#0e0805" stroke-width="10"/>'
    # arms hanging at the sides (huge forepaws)
    armL = 'M1124 336 C1082 380 1066 470 1066 560 C1066 606 1090 626 1116 614 C1130 540 1136 450 1156 386 Z'
    armR = 'M1350 336 C1392 380 1408 470 1408 560 C1408 606 1384 626 1358 614 C1344 540 1338 450 1318 386 Z'
    for k, a in (('AarmL', armL), ('AarmR', armR)):
        df, of = furred(k, a, (1060, 330, 1410, 630), '#3e2414', '#1e1008', '#7a4a2a', '#ffd28a', (0, -1) if k == 'AarmL' else (0, -1), rnd, n=140, rimw=16, flow=92)
        d += df; bd += of
    bd += claws([(1078, 602, 10), (1092, 610, 4), (1106, 612, -4)], col='#f1e2c2', s=1.1)
    bd += claws([(1396, 602, -10), (1382, 610, -4), (1368, 612, 4)], col='#f1e2c2', s=1.1)
    # shoulder hump fur tufts lit by the sun
    bd += tufts([(1180 + k * 22, 282 - math.sin(k / 6 * math.pi) * 8, 0, -1) for k in range(7)], '#5a3620', rnd, w=3.5, L=(10, 18))
    # head turned to the right: round back of head + short broad muzzle
    head = 'M1170 226 C1166 180 1198 160 1240 160 C1282 160 1306 180 1316 204 C1340 210 1356 226 1356 244 C1356 262 1340 274 1312 276 C1290 292 1250 296 1222 290 C1186 282 1172 258 1170 226 Z'
    df, of = furred('Ahead', head, (1165, 155, 1360, 296), '#4a2c18', '#24140b', '#9a6440', '#ffe0a0', (0.3, -1), rnd, n=170, rimw=20, flow=100)
    d += df
    bd += f'<path d="{head}" fill="none" stroke="#ffe8b0" stroke-width="26" opacity=".55" filter="url(#b12)"/>'
    bd += of
    bd += '<path d="M1316 210 C1336 216 1352 230 1354 246" fill="none" stroke="#c48a5a" stroke-width="10" opacity=".8"/>'
    bd += '<ellipse cx="1352" cy="240" rx="10" ry="8" fill="#0e0805"/><circle cx="1349" cy="236" r="2.5" fill="#fff4d0"/>'
    bd += '<path d="M1316 262 Q1334 268 1350 256" fill="none" stroke="#0e0805" stroke-width="4"/>'
    bd += '<ellipse cx="1298" cy="214" rx="5" ry="6" fill="#0e0805"/><circle cx="1300" cy="212" r="1.8" fill="#ffe8b0"/>'
    for ex, ey, r in ((1196, 168, 26), (1262, 158, 23)):
        bd += f'<circle cx="{ex}" cy="{ey}" r="{r}" fill="#3a2214" stroke="{BINK}" stroke-width="5"/>'
        bd += f'<path d="M{ex - r * .8:.0f} {ey - r * .5:.0f} A{r} {r} 0 0 1 {ex + r * .8:.0f} {ey - r * .5:.0f}" fill="none" stroke="#ffd28a" stroke-width="5" opacity=".9"/>'
    b += bd
    b += frog(1020, 912, 2.4, flip=True, look=(-5, -6), mouth='O', shadow=True, mid=SCARF,
              armL='M-34 -22 q-16 4 -20 22', armR='M38 -22 q16 -10 18 -34')
    b += '</g>'
    # tiny loose snow sparkles
    for _ in range(50):
        b += f'<circle cx="{rnd.uniform(900, 1920):.0f}" cy="{rnd.uniform(60, 760):.0f}" r="{rnd.choice([1.4, 2, 2.6])}" fill="#fff8e8" opacity="{rnd.uniform(.25, .7):.2f}"/>'
    b += spark(1420, 300, 24, '#fff6d6') + spark(1520, 520, 16) + spark(1060, 420, 18) + spark(1600, 240, 14)
    b += '<rect width="1920" height="1080" fill="url(#vigA)"/>'
    lines = [('TOO', 132, 'w'), ('BIG', 250, 'y'), ('TO SURVIVE?', 124, 'w')]
    return d, b, lines, '#120c14'


# ============================================================ B: size comparison ==========================================================
GROUND_B = 950; M = 230   # px per metre


def make_B():
    rnd = random.Random(23)
    d = FILTERS
    d += lin('skyB', [(0, '#6fa3d4'), (.55, '#b9d6ee'), (.85, '#eaf3fa'), (1, '#f4f8fb')])
    d += rad('sunB', 380, 120, 900, [(0, '#fff8e0', .9), (.25, '#fff2c8', .4), (1, '#fff2c8', 0)])
    d += lin('snowB', [(0, '#f6fbff'), (1, '#c6d8ea')])
    d += lin('logB', [(0, '#a8744a'), (1, '#6a4428')])
    d += rad('vigB', 960, 540, 1150, [(0, '#000', 0), (.72, '#000', 0), (1, '#0a1830', .4)])
    b = '<rect width="1920" height="1080" fill="url(#skyB)"/><rect width="1920" height="1080" fill="url(#sunB)"/>'
    # mountains + far spruce line
    b += '<path d="M-20 760 L180 560 L300 640 L470 480 L640 620 L820 540 L1000 660 L1200 520 L1400 640 L1600 500 L1800 620 L1940 560 L1940 820 L-20 820Z" fill="#9cb6d4"/>'
    b += '<path d="M180 560 L230 610 L260 600 M470 480 L520 540 L560 530 M1200 520 L1250 570 L1290 560 M1600 500 L1650 550 L1690 540" fill="none" stroke="#f4f8fc" stroke-width="10" stroke-linejoin="round"/>'
    for k in range(60):
        x = k * 33 + rnd.uniform(-10, 10)
        b += snow_spruce(x, 830 + rnd.uniform(-8, 8), rnd.uniform(70, 120), '#5f7c96', snow='#eef5fb', op=.9)
    b += '<rect x="0" y="820" width="1920" height="40" fill="#e6f0f8" opacity=".7" filter="url(#b6)"/>'
    # snow field
    b += f'<path d="M-20 {GROUND_B - 30} Q600 {GROUND_B - 60} 1100 {GROUND_B - 20} Q1500 {GROUND_B} 1940 {GROUND_B - 40} L1940 1080 L-20 1080Z" fill="url(#snowB)"/>'
    # ---- cabin (door = about 2 m, for scale) ----
    cx0, cx1, wt = 860, 1180, GROUND_B - 2.25 * M
    cab = f'<rect x="{cx0}" y="{wt:.0f}" width="{cx1 - cx0}" height="{GROUND_B - wt:.0f}" fill="url(#logB)" stroke="{BINK}" stroke-width="6"/>'
    for k in range(1, 12):
        y = wt + k * (GROUND_B - wt) / 12
        cab += f'<path d="M{cx0} {y:.0f} L{cx1} {y:.0f}" stroke="#4a2e18" stroke-width="4"/><path d="M{cx0} {y + 4:.0f} L{cx1} {y + 4:.0f}" stroke="#c8925e" stroke-width="2" opacity=".6"/>'
        cab += f'<circle cx="{cx0 - 4}" cy="{y - 10:.0f}" r="9" fill="#c8925e" stroke="{BINK}" stroke-width="3"/><circle cx="{cx1 + 4}" cy="{y - 10:.0f}" r="9" fill="#8a5a34" stroke="{BINK}" stroke-width="3"/>'
    door_t = GROUND_B - 2 * M; dx0, dx1 = 930, 1110
    cab += f'<rect x="{dx0}" y="{door_t}" width="{dx1 - dx0}" height="{2 * M}" fill="#2a1a10" stroke="{BINK}" stroke-width="6"/>'
    cab += f'<rect x="{dx0 + 10}" y="{door_t + 10}" width="{dx1 - dx0 - 20}" height="{2 * M - 10}" fill="#ffcf7a" opacity=".35"/>'   # warm light inside
    cab += f'<path d="M{dx1} {door_t} L{dx1 + 64} {door_t + 22} L{dx1 + 64} {GROUND_B + 14} L{dx1} {GROUND_B}Z" fill="#8a5a34" stroke="{BINK}" stroke-width="6" stroke-linejoin="round"/>'
    cab += f'<path d="M{dx1 + 14} {door_t + 60} L{dx1 + 50} {door_t + 72} M{dx1 + 14} {GROUND_B - 120} L{dx1 + 50} {GROUND_B - 112}" stroke="#4a2e18" stroke-width="6"/>'
    ap = wt - 140
    cab += f'<path d="M{cx0 - 40} {wt + 16:.0f} L{(cx0 + cx1) / 2:.0f} {ap:.0f} L{cx1 + 40} {wt + 16:.0f} Z" fill="#6a3c22" stroke="{BINK}" stroke-width="6" stroke-linejoin="round"/>'
    cab += f'<path d="M{cx0 - 52} {wt + 18:.0f} Q{cx0 - 30} {wt - 10:.0f} {(cx0 + cx1) / 2:.0f} {ap - 18:.0f} Q{cx1 + 30} {wt - 10:.0f} {cx1 + 52} {wt + 18:.0f} Q{cx1 + 10} {wt + 4:.0f} {(cx0 + cx1) / 2:.0f} {ap + 20:.0f} Q{cx0 - 10} {wt + 4:.0f} {cx0 - 52} {wt + 18:.0f}Z" fill="#f6fbff" stroke="{BINK}" stroke-width="5" stroke-linejoin="round"/>'
    cab += f'<rect x="{cx1 - 90}" y="{ap - 10:.0f}" width="36" height="80" fill="#7a5040" stroke="{BINK}" stroke-width="5"/>'
    for k in range(3):
        cab += f'<circle cx="{cx1 - 72 + k * 18}" cy="{ap - 40 - k * 40:.0f}" r="{16 + k * 8}" fill="#eef2f6" opacity="{.7 - k * .18:.2f}"/>'
    b += cab
    b += f'<ellipse cx="{(cx0 + cx1) / 2 + 60:.0f}" cy="{GROUND_B + 6}" rx="230" ry="16" fill="#8aa6c4" opacity=".55"/>'
    # ---- snow pole with red/white 0.5 m bands up to 3.5 m ----
    px = 1712; top = GROUND_B - 3.5 * M
    b += f'<ellipse cx="{px + 30}" cy="{GROUND_B + 4}" rx="60" ry="10" fill="#8aa6c4" opacity=".6"/>'
    for k in range(7):
        y0 = GROUND_B - (k + 1) * .5 * M
        b += f'<rect x="{px - 13}" y="{y0:.0f}" width="26" height="{.5 * M:.0f}" fill="{"#d8443a" if k % 2 == 0 else "#f8f6f2"}" stroke="{BINK}" stroke-width="4"/>'
    b += f'<path d="M{px - 6} {top + 6:.0f} L{px - 6} {GROUND_B - 6}" stroke="#fff" stroke-width="3" opacity=".6"/>'
    b += f'<circle cx="{px}" cy="{top - 6:.0f}" r="14" fill="#f2d27a" stroke="{BINK}" stroke-width="4"/>'
    # ---- the bear, rearing up, front view ----
    bx = 1390; bd = ''
    legL = 'M1290 740 C1268 820 1262 900 1270 948 L1366 952 C1366 900 1362 820 1352 760 Z'
    legR = 'M1490 740 C1512 820 1518 900 1510 948 L1414 952 C1414 900 1418 820 1428 760 Z'
    for k, lg in (('BlegL', legL), ('BlegR', legR)):
        df, of = furred(k, lg, (1260, 730, 1520, 955), '#6a4024', '#3a2010', '#a8703e', '#fff0c8', (-.7, -.6), rnd, n=110, rimw=16)
        d += df; bd += of
    for fx_ in (1310, 1470):
        bd += f'<ellipse cx="{fx_}" cy="{GROUND_B + 2}" rx="62" ry="20" fill="#4a2a16" stroke="{BINK}" stroke-width="5"/>'
        bd += claws([(fx_ - 36 + j * 18, GROUND_B + 8, -80 + j * 8 if fx_ < bx else 100 - j * 8) for j in range(5)], s=.75)
    torso = 'M1292 330 C1228 384 1222 520 1238 640 C1254 760 1310 812 1390 814 C1470 812 1526 760 1542 640 C1558 520 1552 384 1488 330 C1448 300 1332 300 1292 330 Z'
    df, of = furred('Btorso', torso, (1222, 300, 1558, 814), '#6a4024', '#3a2010', '#b07a48', '#fff0c8', (-.7, -.6), rnd, n=420, rimw=22, flow=92)
    d += df; bd += of
    bd += '<ellipse cx="1392" cy="600" rx="96" ry="160" fill="#c08a58" opacity=".35"/>'
    for k in range(10):   # chest fur chevrons
        y = 430 + k * 34
        bd += f'<path d="M{1350 + rnd.uniform(-6, 6):.0f} {y} q12 14 22 0 M{1406 + rnd.uniform(-6, 6):.0f} {y + 14} q12 14 22 0" fill="none" stroke="#3a2010" stroke-width="3.5" opacity=".45"/>'
    # raised arms + big paws with claws
    armL = 'M1300 344 C1250 330 1196 300 1164 262 C1140 236 1110 254 1120 290 C1138 342 1200 404 1262 430 Z'
    armR = 'M1480 344 C1530 330 1584 300 1616 262 C1640 236 1670 254 1660 290 C1642 342 1580 404 1518 430 Z'
    for k, a in (('BarmL', armL), ('BarmR', armR)):
        df, of = furred(k, a, (1108, 230, 1672, 432), '#6a4024', '#3a2010', '#b07a48', '#fff0c8', (-.7, -.6), rnd, n=120, rimw=16, flow=60 if k == 'BarmL' else 120)
        d += df; bd += of
    for px_, sgn in ((1132, -1), (1648, 1)):
        bd += f'<ellipse cx="{px_}" cy="262" rx="44" ry="40" fill="#5a341c" stroke="{BINK}" stroke-width="5"/>'
        bd += f'<ellipse cx="{px_}" cy="272" rx="22" ry="18" fill="#2a1810" opacity=".7"/>'
        bd += claws([(px_ + sgn * (10 + j * 4) - sgn * 30 + j * 0, 228 - (2 - abs(j - 2)) * 6, sgn * (-150 + j * 14) if sgn < 0 else 150 - j * 14) for j in range(5)], s=1.0)
    # head: broad, short face
    head = 'M1290 236 C1290 176 1332 140 1390 140 C1448 140 1490 176 1490 236 C1490 290 1450 330 1390 332 C1330 330 1290 290 1290 236 Z'
    df, of = furred('Bhead', head, (1288, 138, 1492, 334), '#6a4024', '#3a2010', '#b07a48', '#fff0c8', (-.7, -.7), rnd, n=170, rimw=20, flow=100)
    d += df
    for ex, ey in ((1312, 164), (1468, 164)):
        bd += f'<circle cx="{ex}" cy="{ey}" r="30" fill="#5a341c" stroke="{BINK}" stroke-width="5"/><circle cx="{ex}" cy="{ey + 4}" r="15" fill="#2a1810" opacity=".7"/>'
    bd += of
    bd += '<path d="M1338 270 C1338 236 1360 222 1390 222 C1420 222 1442 236 1442 270 C1442 304 1420 318 1390 318 C1360 318 1338 304 1338 270 Z" fill="#c69466" stroke="#3a2010" stroke-width="3" opacity=".95"/>'
    bd += '<ellipse cx="1390" cy="248" rx="26" ry="17" fill="#120a06"/><ellipse cx="1382" cy="242" rx="8" ry="4" fill="#fff" opacity=".7"/>'
    bd += '<path d="M1390 264 L1390 280 M1366 290 Q1390 312 1414 290" fill="none" stroke="#120a06" stroke-width="5" stroke-linecap="round"/>'
    bd += '<path d="M1372 294 Q1390 318 1408 294 Q1390 302 1372 294Z" fill="#7a2f33"/>'
    for ex in (1346, 1434):   # eyes looking down-left at the frog
        bd += f'<circle cx="{ex}" cy="208" r="11" fill="#f3ecd8" stroke="{BINK}" stroke-width="3.5"/><circle cx="{ex - 4}" cy="212" r="6" fill="#120a06"/><circle cx="{ex - 2}" cy="209" r="2" fill="#fff"/>'
    bd += '<path d="M1330 188 L1360 182 M1420 182 L1450 188" stroke="#120a06" stroke-width="5" stroke-linecap="round"/>'
    bd += tufts([(1250 + k * 25, 330 + (k - 3) ** 2 * 3, 0, -1) for k in range(1, 6)], '#6a4024', rnd, w=3, L=(8, 14))
    b += f'<path d="M1420 {GROUND_B + 8} Q1600 {GROUND_B + 30} 1800 {GROUND_B + 20} L1700 {GROUND_B + 2} Z" fill="#8aa6c4" opacity=".5"/>'
    b += bd
    # dashed height line from the top of the head to the pole top
    b += f'<path d="M1440 {top:.0f} L{px - 18} {top:.0f}" stroke="#fff" stroke-width="7" stroke-dasharray="18 14" opacity=".95"/>'
    b += f'<path d="M1440 {top:.0f} L{px - 18} {top:.0f}" stroke="{BINK}" stroke-width="2" stroke-dasharray="18 14" opacity=".5"/>'
    # bear paw prints in the snow
    for x, y, s in ((1560, 1010, 1.0), (1440, 1050, 1.1)):
        b += f'<ellipse cx="{x}" cy="{y}" rx="{34 * s:.0f}" ry="{14 * s:.0f}" fill="#a8bed6"/>' + ''.join(f'<ellipse cx="{x - 30 * s + j * 15 * s:.0f}" cy="{y - 18 * s:.0f}" rx="{6 * s:.0f}" ry="{4 * s:.0f}" fill="#a8bed6"/>' for j in range(5))
    # person for scale (about 1.7 m)
    b += f'<ellipse cx="760" cy="{GROUND_B + 4}" rx="80" ry="12" fill="#8aa6c4" opacity=".6"/>'
    b += person(760, GROUND_B, H=1.7 * M / 5.5, pose='shrug', skin='#e6b48c', hair='#3a2a1e', shirt='#c85a3a', pants='#2b3446',
                hair_style='cap', face='surprise', name='hiker')
    # frog in the doorway with a beanie, looking up at the bear
    b += frog(1022, GROUND_B - 4, 2.75, look=(6, -7), mouth='O', shadow=True, head=BEANIE, brows=False,
              armL='M-34 -22 q-18 -6 -22 -30', armR='M38 -22 q14 6 16 22')
    b += spark(1560, 150, 22, '#fffbe8') + spark(1180, 200, 16, '#fffbe8') + spark(1780, 400, 14, '#fffbe8')
    for _ in range(40):
        b += f'<circle cx="{rnd.uniform(900, 1900):.0f}" cy="{rnd.uniform(40, 900):.0f}" r="{rnd.choice([2, 2.8, 3.6])}" fill="#fff" opacity="{rnd.uniform(.35, .85):.2f}"/>'
    b += '<rect width="1920" height="1080" fill="url(#vigB)"/>'
    lines = [('ABOUT', 128, 'w'), ('3.5 M', 236, 'y'), ('TALL', 150, 'w')]
    return d, b, lines, '#0c1a2c'


# ============================================================ C: the kill stealer =========================================================
def wolf(x, y, s, flip=False, op=1.0, body='#7c8698', dark='#4a5162', rim='#ffd6a0'):
    sx = -s if flip else s
    st = f'stroke="#141822" stroke-width="{4 / s:.2f}" stroke-linejoin="round" stroke-linecap="round"'
    g = f'<g transform="translate({x} {y}) scale({sx} {s}) rotate(-5)" opacity="{op}">'
    # far legs
    g += f'<path d="M-82 -52 C-96 -30 -92 -14 -104 0 M62 -48 C66 -28 60 -12 66 0" fill="none" stroke="#141822" stroke-width="{20}"/>'
    g += f'<path d="M-82 -52 C-96 -30 -92 -14 -104 0 M62 -48 C66 -28 60 -12 66 0" fill="none" stroke="{dark}" stroke-width="{13}"/>'
    # tucked tail
    g += f'<path d="M-112 -82 C-140 -60 -132 -28 -100 -22" fill="none" stroke="#141822" stroke-width="22"/><path d="M-112 -82 C-140 -60 -132 -28 -100 -22" fill="none" stroke="{dark}" stroke-width="15"/>'
    # body with raised hackles
    g += (f'<path d="M-112 -92 C-80 -116 -30 -122 10 -120 L18 -132 L26 -120 L34 -134 L42 -118 L52 -128 L58 -112 C86 -104 100 -80 96 -52 '
          f'C88 -36 52 -40 22 -42 C-20 -42 -70 -38 -100 -46 C-124 -56 -128 -80 -112 -92 Z" fill="{body}" {st}/>')
    g += f'<path d="M-104 -92 C-70 -112 -20 -118 20 -116" fill="none" stroke="{rim}" stroke-width="5" opacity=".85"/>'
    g += f'<path d="M-90 -50 C-50 -46 0 -46 40 -48" fill="none" stroke="{dark}" stroke-width="10" opacity=".7"/>'
    # head low, ears flat, snarling
    g += (f'<path d="M66 -104 C92 -116 124 -104 142 -90 L186 -76 C194 -70 192 -60 182 -58 L150 -52 C128 -46 104 -54 88 -62 C74 -70 62 -88 66 -104 Z" fill="{body}" {st}/>')
    g += f'<path d="M84 -106 L62 -128 L102 -112 Z" fill="{dark}" {st}/>'
    g += f'<path d="M150 -60 L182 -62 M154 -60 l3 6 l3 -6 l3 6 l3 -6 l3 6 l3 -6" fill="none" stroke="#141822" stroke-width="2.4"/>'
    g += f'<path d="M150 -60 L180 -62 L178 -56 L152 -54 Z" fill="#f4efe2" stroke="#141822" stroke-width="1.6"/>'
    g += f'<ellipse cx="186" cy="-72" rx="6" ry="5" fill="#141822"/>'
    g += f'<path d="M116 -94 L132 -90" stroke="#141822" stroke-width="4"/><circle cx="126" cy="-88" r="3.2" fill="#ffe08a"/>'
    g += f'<path d="M72 -102 C96 -112 124 -102 140 -90" fill="none" stroke="{rim}" stroke-width="4" opacity=".85"/>'
    # near legs
    g += f'<path d="M-70 -50 C-80 -28 -76 -14 -86 0 M80 -50 C86 -28 80 -12 86 0" fill="none" stroke="#141822" stroke-width="22"/>'
    g += f'<path d="M-70 -50 C-80 -28 -76 -14 -86 0 M80 -50 C86 -28 80 -12 86 0" fill="none" stroke="{body}" stroke-width="15"/>'
    return g + '</g>'


def make_C():
    rnd = random.Random(37)
    d = FILTERS
    d += lin('skyC', [(0, '#1e2438'), (.4, '#3c4560'), (.7, '#8a7e8a'), (1, '#c8a48a')])
    d += rad('glowC', 1500, 330, 900, [(0, '#ffe6b0', .95), (.15, '#ffc888', .6), (.45, '#d08a6a', .22), (1, '#d08a6a', 0)])
    d += lin('groundC', [(0, '#4a4650'), (1, '#16141c')])
    d += rad('vigC', 960, 540, 1150, [(0, '#000', 0), (.65, '#000', 0), (1, '#06060c', .65)])
    d += lin('meatC', [(0, '#e88a72'), (1, '#9a3a34')])
    b = '<rect width="1920" height="1080" fill="url(#skyC)"/><rect width="1920" height="1080" fill="url(#glowC)"/>'
    b += '<circle cx="1500" cy="330" r="60" fill="#fff4d8" opacity=".9" filter="url(#b6)"/>'
    for k in range(12):
        a = math.radians(70 + k * 9)
        b += (f'<path d="M1500 330 L{1500 + math.cos(a + .03) * 1100:.0f} {330 + math.sin(a + .03) * 1100:.0f} L{1500 + math.cos(a - .03) * 1100:.0f} {330 + math.sin(a - .03) * 1100:.0f}Z" fill="#ffe0b0" opacity=".06"/>')
    # far plain: mammoth steppe horizon with distant mammoth silhouettes
    b += '<path d="M-20 700 Q400 660 900 690 Q1400 710 1940 670 L1940 760 L-20 760Z" fill="#5e5a6c" opacity=".8"/>'
    for mx, ms in ((380, 1.0), (520, .8), (1840, .9)):
        b += (f'<g transform="translate({mx} 690) scale({ms})" fill="#4a4658" opacity=".8"><path d="M-40 0 L-40 -40 C-40 -70 -10 -80 20 -76 C40 -74 52 -60 54 -40 C60 -30 62 -10 56 10 L50 10 C50 -10 46 -24 42 -30 L40 0 L28 0 L28 -20 L-24 -20 L-26 0 Z"/>'
              f'<path d="M50 -30 Q70 -20 64 -4" fill="none" stroke="#4a4658" stroke-width="5"/></g>')
    # mist layers
    for _ in range(30):
        x = rnd.uniform(-100, 2000); y = rnd.uniform(560, 820)
        b += f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{rnd.uniform(160, 380):.0f}" ry="{rnd.uniform(30, 70):.0f}" fill="#d8c8c4" opacity="{rnd.uniform(.18, .4):.2f}" filter="url(#b24)"/>'
    b += '<path d="M-20 760 Q500 730 1000 760 Q1500 780 1940 740 L1940 1080 L-20 1080Z" fill="url(#groundC)"/>'
    for _ in range(140):   # frozen grass tufts
        x = rnd.uniform(0, 1920); y = rnd.uniform(770, 1080); h = rnd.uniform(10, 30) * (1 + (y - 770) / 300)
        b += f'<path d="M{x:.0f} {y:.0f} l{rnd.uniform(-8, 8):.0f} {-h:.0f} M{x + 4:.0f} {y:.0f} l{rnd.uniform(0, 12):.0f} {-h * .8:.0f}" stroke="#8a8090" stroke-width="2.4" opacity="{rnd.uniform(.3, .7):.2f}"/>'
    # big glow behind the bear
    b += '<ellipse cx="1400" cy="520" rx="520" ry="340" fill="#ffd8a0" opacity=".28" filter="url(#b80)"/>'
    # ---- the bear, walking in from the right on all fours, paw on the kill ----
    bd = ''
    # far legs (darker)
    farF = 'M1200 590 C1160 660 1112 760 1074 828 C1060 852 1046 868 1030 878 L978 890 C970 872 984 852 1004 846 C1040 790 1080 700 1130 600 Z'
    farH = 'M1560 540 C1640 560 1660 650 1634 730 C1620 810 1624 880 1632 940 L1640 962 L1550 964 C1550 900 1548 820 1530 760 C1512 700 1512 610 1560 540 Z'
    for k, lg in (('CfarF', farF), ('CfarH', farH)):
        df, of = furred(k, lg, (970, 530, 1665, 965), '#2e1c12', '#140a06', '#5a3a24', '#ffcf90', (.4, -1), rnd, n=120, rimw=14, rimop=.6)
        d += df; bd += of
    bd += claws([(992, 884, -110), (1000, 892, -100), (1012, 896, -92)], s=1.05)
    body = ('M1090 452 C1150 362 1210 300 1290 294 C1380 290 1480 328 1580 358 C1680 388 1742 460 1736 560 C1732 620 1716 660 1692 690 '
            'C1600 722 1450 732 1330 702 C1260 690 1200 660 1160 622 C1120 592 1090 542 1080 500 Z')
    df, of = furred('Cbody', body, (1078, 288, 1742, 734), '#3e2616', '#1a0e08', '#7a4e2e', '#ffd49a', (.35, -1), rnd, n=600, rimw=28, flow=100)
    d += df
    bd += f'<path d="M1090 452 C1150 362 1210 300 1290 294 C1380 290 1480 328 1580 358 C1680 388 1742 460 1736 560" fill="none" stroke="#ffd8a0" stroke-width="34" opacity=".45" filter="url(#b12)"/>'
    bd += of
    bd += tufts([(1230 + k * 30, 300 - math.sin(k / 8 * math.pi) * 6 + k * 2, 0, -1) for k in range(9)], '#4a2e1a', rnd, w=3.5, L=(10, 20))
    bd += '<path d="M1300 420 C1360 470 1420 520 1460 640" fill="none" stroke="#120804" stroke-width="5" opacity=".35"/>'
    bd += '<ellipse cx="1450" cy="962" rx="90" ry="12" fill="#000" opacity=".35"/>'
    # near legs
    nearH = 'M1620 520 C1710 540 1730 640 1700 720 C1686 800 1690 880 1700 940 L1708 966 L1606 968 C1606 900 1606 820 1588 760 C1570 700 1570 600 1620 520 Z'
    nearF = 'M1232 560 C1292 580 1304 680 1288 760 C1280 840 1284 900 1292 950 L1300 968 L1190 968 C1196 900 1202 820 1196 740 C1186 660 1192 600 1232 560 Z'
    for k, lg in (('CnearH', nearH), ('CnearF', nearF)):
        df, of = furred(k, lg, (1185, 515, 1735, 970), '#3e2616', '#1a0e08', '#7a4e2e', '#ffd49a', (.35, -1), rnd, n=160, rimw=16, flow=92)
        d += df; bd += of
    bd += claws([(1200 + j * 22, 962, -96 + j * 4) for j in range(5)], s=1.1)
    bd += claws([(1616 + j * 20, 962, -96 + j * 4) for j in range(4)], s=.95)
    # head: short broad face, snarl, eye catching the light
    head = 'M1118 418 C1090 378 1030 372 988 392 C960 404 930 432 910 462 C898 482 892 500 898 520 C924 540 960 548 992 546 C1034 560 1082 560 1114 540 C1140 520 1146 452 1118 418 Z'
    df, of = furred('Chead', head, (890, 368, 1146, 562), '#4a2e1a', '#1a0e08', '#8a5a36', '#ffdca8', (.3, -1), rnd, n=200, rimw=22, flow=110)
    d += df
    for ex, ey, r in ((1084, 386, 26), (1046, 376, 20)):
        bd += f'<circle cx="{ex}" cy="{ey}" r="{r}" fill="#2e1c12" stroke="{BINK}" stroke-width="5"/><path d="M{ex - r * .8:.0f} {ey - r * .5:.0f} A{r} {r} 0 0 1 {ex + r * .8:.0f} {ey - r * .5:.0f}" fill="none" stroke="#ffd49a" stroke-width="5"/>'
    bd += f'<path d="{head}" fill="none" stroke="#ffd8a0" stroke-width="22" opacity=".35" filter="url(#b12)"/>'
    bd += of
    bd += '<path d="M912 470 C930 450 960 436 992 438" fill="none" stroke="#a8784e" stroke-width="12" opacity=".7"/>'   # pale short muzzle
    bd += '<ellipse cx="904" cy="496" rx="16" ry="13" fill="#0a0503"/><circle cx="900" cy="490" r="3.5" fill="#ffe8c0"/>'
    # open mouth with canines
    bd += '<path d="M908 524 C930 534 968 540 1010 536 C990 560 950 572 918 560 Z" fill="#5a1e20" stroke="#0a0503" stroke-width="4"/>'
    bd += '<path d="M928 528 L934 546 L940 530 Z M984 536 L990 554 L996 536 Z" fill="#f4ecd8" stroke="#0a0503" stroke-width="2"/>'
    bd += '<path d="M936 562 L942 548 L948 564 Z" fill="#f4ecd8" stroke="#0a0503" stroke-width="2"/>'
    bd += '<path d="M1000 432 L1036 440" stroke="#0a0503" stroke-width="6" stroke-linecap="round"/>'
    bd += '<circle cx="1018" cy="452" r="20" fill="#ffd060" opacity=".45" filter="url(#b6)"/><ellipse cx="1018" cy="452" rx="10" ry="8" fill="#ffcf5a" stroke="#0a0503" stroke-width="3"/><circle cx="1016" cy="452" r="4.5" fill="#0a0503"/><circle cx="1020" cy="449" r="2" fill="#fff"/>'
    # ---- the kill (cartoon meat on the bone, no gore) under the paw ----
    mt = ''
    mt += '<ellipse cx="1010" cy="968" rx="190" ry="22" fill="#000" opacity=".4"/>'
    for ex, ey in ((842, 950), (1172, 896)):
        mt += f'<circle cx="{ex}" cy="{ey - 16}" r="26" fill="#f4ecd8" stroke="{BINK}" stroke-width="5"/><circle cx="{ex}" cy="{ey + 16}" r="26" fill="#f4ecd8" stroke="{BINK}" stroke-width="5"/>'
    mt += f'<path d="M840 934 L1170 880 L1176 912 L846 966 Z" fill="#efe4cc" stroke="{BINK}" stroke-width="5"/>'
    mt += '<ellipse cx="1004" cy="916" rx="132" ry="68" transform="rotate(-9 1004 916)" fill="url(#meatC)" stroke="#1c1009" stroke-width="6"/>'
    mt += '<path d="M900 920 Q960 880 1080 878 M920 948 Q1000 930 1100 920" fill="none" stroke="#f6c8b0" stroke-width="7" opacity=".7"/>'
    mt += '<path d="M930 880 Q980 856 1050 858" fill="none" stroke="#fff" stroke-width="8" opacity=".5" stroke-linecap="round"/>'
    b += mt
    b += bd
    # paw resting on top of the meat (far forepaw is drawn behind; add a big near paw slab on the meat)
    paw = 'M1030 846 C1060 830 1110 832 1126 852 C1134 870 1110 884 1080 886 C1050 888 1020 878 1030 846 Z'
    b += f'<path d="{paw}" fill="#2e1c12" stroke="{BINK}" stroke-width="5"/>'
    b += claws([(1036 + j * 20, 880, -10 + j * 4) for j in range(4)], s=1.0)
    b += f'<path d="M1040 846 C1066 836 1100 838 1116 850" fill="none" stroke="#ffcf90" stroke-width="5" opacity=".8"/>'
    # mist curling in front of the bear's legs
    for _ in range(12):
        x = rnd.uniform(1100, 1900); y = rnd.uniform(860, 1000)
        b += f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{rnd.uniform(120, 260):.0f}" ry="{rnd.uniform(18, 36):.0f}" fill="#d8c8c4" opacity="{rnd.uniform(.18, .35):.2f}" filter="url(#b12)"/>'
    b += frog(1450, 962, 2.5, flip=True, look=(-8, -4), mouth='O', armL='M-34 -22 q-14 -4 -18 -26', armR='M38 -22 q14 -4 18 -26')
    # dire wolves backing off (left)
    b += wolf(300, 915, 1.05, op=.85, body='#6a7284', dark='#3e4454')
    b += wolf(90, 1050, 1.3, body='#727c8e')
    b += wolf(560, 995, 1.45)
    b += spark(1640, 220, 22, '#fff2d0') + spark(1240, 260, 16, '#fff2d0') + spark(880, 760, 14, '#fff2d0')
    for _ in range(60):
        b += f'<circle cx="{rnd.uniform(800, 1920):.0f}" cy="{rnd.uniform(40, 800):.0f}" r="{rnd.choice([1.4, 2, 2.6])}" fill="#ffe8c8" opacity="{rnd.uniform(.2, .55):.2f}"/>'
    b += '<rect width="1920" height="1080" fill="url(#vigC)"/>'
    lines = [('ICE AGE', 150, 'w'), ('BULLY?', 236, 'y')]
    return d, b, lines, '#0c0a12'


if __name__ == '__main__':
    which = sys.argv[1:] or ['A', 'B', 'C']
    for n in which:
        dd, bb, lines, outline = globals()[f'make_{n}']()
        open(os.path.join(HERE, f'{n}.html'), 'w').write(page('#1a1410', svg(dd, bb), lines, outline=outline, top=40))
    print('ok')
