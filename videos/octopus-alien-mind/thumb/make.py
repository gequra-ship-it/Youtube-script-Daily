# octopus-alien-mind thumbnails A-C (guideline 16-6). run: python3 make.py  (writes A.html B.html C.html here)
# A  EARTH'S TRUE ALIEN?   homage: Arrival (huge misty glass wall, small suited figure with a hand on it, an octopus behind the
#    glass touching the same spot, a round ink ring floating in the mist; no letters). Script S02 (Godfrey-Smith "closest we
#    will come to meeting an intelligent alien"), S46 closing question "do you think the octopus is Earth's true alien?"
# B  ARMS THAT THINK      intuitive: an octopus seen from the front, every arm lit by a glowing neuron net, only a small
#    donut-shaped glow in the head. Script S08-S09 ("only about one-third ... central brain, wraps around the esophagus like a
#    donut", "two-thirds are spread through the eight arms", "the arms do a lot of their own thinking").
# C  3 HEARTS, BLUE BLOOD  intuitive: a glass-like octopus jetting through dark water, three glowing hearts (two small gill
#    hearts beside the gills, one bigger systemic heart) and glowing blue vessels. Script S01, S31-S34.
import os, sys, math, random
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', '..', 'tools'))
from thumb_lib import *
from hands import hand


def P(pts, close=False):
    return 'M' + ' L'.join(f'{x:.1f},{y:.1f}' for x, y in pts) + (' Z' if close else '')


# ------------------------------------------------------------------ octopus parts
def curve(x0, y0, th0, L, a, b, n=90, wav=0, wf=3, w0=60, taper=.9):
    """arm centre line: heading th0 (deg, 0 = right, 90 = down), turning rate a + b*u^2 (+ a small wave); returns
    list of (x, y, theta, u, half_width)"""
    th = math.radians(th0); x, y = x0, y0; out = []
    for i in range(n + 1):
        u = i / n
        h = w0 / 2 * ((1 - u) ** taper) * (1 + .12 * math.exp(-u * 18)) + 1.2
        out.append((x, y, th, u, h))
        dth = (a + b * u * u + wav * math.cos(u * wf * math.pi)) / n
        th += dth; x += math.cos(th) * L / n; y += math.sin(th) * L / n
    return out


def off(C, f, i0=0, i1=None):
    return [(x - math.sin(t) * f * h, y + math.cos(t) * f * h) for x, y, t, u, h in C[i0:i1]]


def band(C, f0, f1, i0=0, i1=None):
    return P(off(C, f0, i0, i1) + off(C, f1, i0, i1)[::-1], True)


def arm(C, col, side=None, line='#07121a', lw=4, suckers=True, seed=1, spots=10, rim=None, op=1):
    """one tapered arm with cylinder shading, a rim-lit back edge and a row of suckers on the underside edge"""
    rnd = random.Random(seed)
    if side is None:   # suckers on the inside of the tip curl (the underside faces the curl)
        side = 1 if (C[-1][2] - C[-12][2]) >= 0 else -1
    o = f'<g opacity="{op}">'
    o += f'<path d="{band(C, 1, -1)}" fill="{col["sh"]}" stroke="{line}" stroke-width="{lw}" stroke-linejoin="round"/>'
    o += f'<path d="{band(C, -side * .92, side * .30)}" fill="{col["mid"]}"/>'
    o += f'<path d="{band(C, -side * .80, -side * .40, 0, -3)}" fill="{col["hi"]}" opacity=".55"/>'
    for _ in range(spots):   # mottled skin
        x, y, t, u, h = C[rnd.randint(3, int(len(C) * .75))]
        f = rnd.uniform(-.5, .2) * side
        o += f'<ellipse cx="{x - math.sin(t) * f * h:.1f}" cy="{y + math.cos(t) * f * h:.1f}" rx="{h * rnd.uniform(.12, .25):.1f}" ry="{h * rnd.uniform(.08, .15):.1f}" transform="rotate({math.degrees(t):.0f} {x - math.sin(t) * f * h:.1f} {y + math.cos(t) * f * h:.1f})" fill="{col["sh"]}" opacity=".5"/>'
    if rim:
        o += f'<path d="{P(off(C, -side * .97, 1, -4))}" fill="none" stroke="{rim}" stroke-width="{max(2.5, C[0][4] * .12):.1f}" stroke-linecap="round" opacity=".9"/>'
    if suckers:   # walk along the arc and drop a sucker every ~2 sucker radii on the underside edge
        s = 0; nxt = C[0][4] * .5; px, py = C[0][0], C[0][1]
        for x, y, t, u, h in C[1:]:
            s += math.hypot(x - px, y - py); px, py = x, y
            if s >= nxt and u < .96:
                r = h * .52
                cx, cy = x - math.sin(t) * side * h * .78, y + math.cos(t) * side * h * .78
                a = math.degrees(t)
                o += (f'<g transform="translate({cx:.1f} {cy:.1f}) rotate({a:.1f})"><ellipse rx="{r:.1f}" ry="{r * .78:.1f}" fill="{col["suck"]}" stroke="{line}" stroke-width="{max(1.2, lw * .55):.1f}"/>'
                      f'<ellipse cx="0" cy="{side * r * .12:.1f}" rx="{r * .5:.1f}" ry="{r * .36:.1f}" fill="{col["cup"]}"/>'
                      f'<ellipse cx="{-r * .25:.1f}" cy="{-side * r * .35:.1f}" rx="{r * .35:.1f}" ry="{r * .15:.1f}" fill="#fff" opacity=".45"/></g>')
                nxt = s + r * 2.05
    return o + '</g>'


def mantle(x, y, rx, ry, rot, col, gid, line='#07121a', lw=5, rim=None, seed=3, op=1, light=(.32, .28), part='full'):
    """the bulb-shaped mantle (looks like the head). local: base at +y, round top at -y"""
    rnd = random.Random(seed)
    d = (f'<radialGradient id="{gid}" cx="{light[0]}" cy="{light[1]}" r=".85"><stop offset="0" stop-color="{col["hi"]}"/>'
         f'<stop offset=".45" stop-color="{col["mid"]}"/><stop offset="1" stop-color="{col["sh"]}"/></radialGradient>')
    shape = (f'M0,{ry:.0f} C{-rx * .62:.0f},{ry:.0f} {-rx * 1.04:.0f},{ry * .35:.0f} {-rx:.0f},{-ry * .2:.0f} '
             f'C{-rx * .95:.0f},{-ry * .8:.0f} {-rx * .5:.0f},{-ry * 1.02:.0f} 0,{-ry:.0f} '
             f'C{rx * .5:.0f},{-ry * 1.02:.0f} {rx * .95:.0f},{-ry * .8:.0f} {rx:.0f},{-ry * .2:.0f} '
             f'C{rx * 1.04:.0f},{ry * .35:.0f} {rx * .62:.0f},{ry:.0f} 0,{ry:.0f}Z')
    o = f'<g transform="translate({x} {y}) rotate({rot})" opacity="{op}">'
    if part == 'outline':
        return d, o + f'<path d="{shape}" fill="{line}" stroke="{line}" stroke-width="{lw * 2}"/></g>'
    o += f'<path d="{shape}" fill="url(#{gid})"' + (f' stroke="{line}" stroke-width="{lw}"/>' if part == 'full' else '/>')
    for k in range(5):   # soft skin folds
        yy = -ry * .55 + k * ry * .28; ww = rx * (.55 + .1 * math.sin(k))
        o += f'<path d="M{-ww:.0f},{yy:.0f} Q0,{yy + ry * .09:.0f} {ww:.0f},{yy - ry * .03:.0f}" fill="none" stroke="{col["sh"]}" stroke-width="{rx * .025:.1f}" opacity=".35" stroke-linecap="round"/>'
    for _ in range(26):   # papillae bumps
        a = rnd.uniform(0, 6.28); rr = rnd.uniform(.1, .85)
        bx, by = math.cos(a) * rx * rr, math.sin(a) * ry * rr * .9 - ry * .05
        s = rnd.uniform(.02, .045) * rx
        o += f'<circle cx="{bx:.0f}" cy="{by:.0f}" r="{s:.1f}" fill="{col["sh"]}" opacity=".45"/><circle cx="{bx - s * .3:.0f}" cy="{by - s * .35:.0f}" r="{s * .5:.1f}" fill="{col["hi"]}" opacity=".5"/>'
    o += f'<ellipse cx="{-rx * .35:.0f}" cy="{-ry * .5:.0f}" rx="{rx * .22:.0f}" ry="{ry * .12:.0f}" transform="rotate(-30 {-rx * .35:.0f} {-ry * .5:.0f})" fill="#fff" opacity=".28"/>'
    if rim:
        o += (f'<path d="M{rx * .2:.0f},{-ry * .98:.0f} C{rx * .75:.0f},{-ry * .9:.0f} {rx * 1.0:.0f},{-ry * .5:.0f} {rx * .98:.0f},{ry * .05:.0f}" '
              f'fill="none" stroke="{rim}" stroke-width="{rx * .05:.1f}" stroke-linecap="round" opacity=".85"/>')
    return d, o + '</g>'


def eye(x, y, r, rot=0, skin='#c8553a', iris='#f0c24a', line='#07121a', look=(0, 0)):
    """raised eye bulge, gold iris, horizontal slit pupil (octopus)"""
    o = f'<g transform="translate({x} {y}) rotate({rot})">'
    o += f'<ellipse rx="{r * 1.45:.1f}" ry="{r * 1.25:.1f}" fill="{skin}" stroke="{line}" stroke-width="{max(2, r * .08):.1f}"/>'
    o += f'<path d="M{-r * 1.3:.1f},{-r * .55:.1f} Q0,{-r * 1.55:.1f} {r * 1.3:.1f},{-r * .55:.1f}" fill="none" stroke="#000" stroke-width="{r * .2:.1f}" opacity=".25"/>'
    o += f'<circle r="{r:.1f}" fill="{iris}" stroke="{line}" stroke-width="{max(2, r * .1):.1f}"/>'
    o += f'<circle r="{r * .8:.1f}" fill="none" stroke="#8a5a10" stroke-width="{r * .1:.1f}" opacity=".45"/>'
    lx, ly = look
    o += f'<rect x="{-r * .62 + lx * r:.1f}" y="{-r * .17 + ly * r:.1f}" width="{r * 1.24:.1f}" height="{r * .34:.1f}" rx="{r * .17:.1f}" fill="#06080a"/>'
    o += f'<circle cx="{-r * .38:.1f}" cy="{-r * .45:.1f}" r="{r * .16:.1f}" fill="#fff" opacity=".9"/>'
    o += f'<path d="M{-r * 1.25:.1f},{-r * .2:.1f} Q0,{-r * 1.35:.1f} {r * 1.25:.1f},{-r * .2:.1f}" fill="none" stroke="{skin}" stroke-width="{r * .32:.1f}" stroke-linecap="round"/>'   # upper lid
    return o + '</g>'


def head(x, y, rx, ry, rot, col, gid, line='#07121a', lw=5, part='full', light=(.4, .3), crease=None):
    """the head (eye region) below the mantle: a soft oval; part='outline' draws only the silhouette rim"""
    d = (f'<radialGradient id="{gid}" cx="{light[0]}" cy="{light[1]}" r=".8"><stop offset="0" stop-color="{col["hi"]}"/>'
         f'<stop offset=".5" stop-color="{col["mid"]}"/><stop offset="1" stop-color="{col["sh"]}"/></radialGradient>')
    if part == 'outline':
        return d, f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{ry}" transform="rotate({rot} {x} {y})" fill="{line}" stroke="{line}" stroke-width="{lw * 2}"/>'
    o = f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{ry}" transform="rotate({rot} {x} {y})" fill="url(#{gid})"/>'
    if crease:   # soft neck crease where the mantle meets the head
        o += f'<path d="{crease}" fill="none" stroke="{col["sh"]}" stroke-width="6" opacity=".55" stroke-linecap="round"/>'
    return d, o


def siphon(x, y, L, ang, w, col, line='#07121a'):
    """the funnel: a short tube with a lighter rim at the opening"""
    a = math.radians(ang); ex, ey = x + math.cos(a) * L, y + math.sin(a) * L
    nx, ny = -math.sin(a), math.cos(a)
    mx, my = (x + ex) / 2 + nx * w * .25, (y + ey) / 2 + ny * w * .25
    tube = f'M{x:.1f},{y:.1f} Q{mx:.1f},{my:.1f} {ex:.1f},{ey:.1f}'
    o = f'<path d="{tube}" fill="none" stroke="{line}" stroke-width="{w + 8:.0f}" stroke-linecap="round"/>'
    o += f'<path d="{tube}" fill="none" stroke="{col["mid"]}" stroke-width="{w:.0f}" stroke-linecap="round"/>'
    o += f'<path d="M{x - nx * w * .25:.1f},{y - ny * w * .25:.1f} Q{mx - nx * w * .25:.1f},{my - ny * w * .25:.1f} {ex - nx * w * .2:.1f},{ey - ny * w * .2:.1f}" fill="none" stroke="{col["hi"]}" stroke-width="{w * .2:.1f}" opacity=".6" stroke-linecap="round"/>'
    o += f'<ellipse cx="{ex:.1f}" cy="{ey:.1f}" rx="{w * .2:.1f}" ry="{w * .45:.1f}" transform="rotate({ang:.0f} {ex:.1f} {ey:.1f})" fill="{col["sh"]}" stroke="{line}" stroke-width="4"/>'
    o += f'<ellipse cx="{ex:.1f}" cy="{ey:.1f}" rx="{w * .1:.1f}" ry="{w * .3:.1f}" transform="rotate({ang:.0f} {ex:.1f} {ey:.1f})" fill="#05080a"/>'
    return o


def web(pts, col, line='#07121a', op=1):
    """the skin web between arm bases"""
    return f'<path d="{P(pts, True)}" fill="{col}" stroke="{line}" stroke-width="3" stroke-linejoin="round" opacity="{op}"/>'


def bubbles(rnd, n, x0, y0, x1, y1, col='#dff8ff', op=.6):
    o = ''
    for _ in range(n):
        x, y, r = rnd.uniform(x0, x1), rnd.uniform(y0, y1), rnd.choice([3, 4, 6, 8, 11])
        o += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r}" fill="none" stroke="{col}" stroke-width="2" opacity="{op * rnd.uniform(.4, 1):.2f}"/>'
        o += f'<circle cx="{x - r * .35:.0f}" cy="{y - r * .35:.0f}" r="{r * .25:.1f}" fill="{col}" opacity="{op:.2f}"/>'
    return o


def rays(x, y, angs, L, w, col, op, filt='bl'):
    o = ''
    for a, ww in zip(angs, w):
        r = math.radians(a); ex, ey = x + math.cos(r) * L, y + math.sin(r) * L
        nx, ny = -math.sin(r), math.cos(r)
        o += f'<path d="M{x - nx * ww * .15:.0f},{y - ny * ww * .15:.0f} L{x + nx * ww * .15:.0f},{y + ny * ww * .15:.0f} L{ex + nx * ww:.0f},{ey + ny * ww:.0f} L{ex - nx * ww:.0f},{ey - ny * ww:.0f}Z" fill="{col}" opacity="{op}" filter="url(#{filt})"/>'
    return o


def F(id, sd, pad=60):
    return f'<filter id="{id}" x="-{pad}%" y="-{pad}%" width="{100 + 2 * pad}%" height="{100 + 2 * pad}%"><feGaussianBlur stdDeviation="{sd}"/></filter>'


FILTERS = F('bl', 40) + F('soft', 18) + F('bl6', 6) + F('bl3', 3) + F('bl12', 12)
INK = ('<filter id="ink" x="-30%" y="-30%" width="160%" height="160%"><feTurbulence type="fractalNoise" baseFrequency=".018" numOctaves="3" seed="4"/>'
       '<feDisplacementMap in="SourceGraphic" scale="22" xChannelSelector="R" yChannelSelector="G"/><feGaussianBlur stdDeviation="1.6"/></filter>')


# =========================== A: EARTH'S TRUE ALIEN? (homage: Arrival, the glass wall) ===========================
rnd = random.Random(11)
d = FILTERS + INK
d += rad('amist', 1330, 430, 1100, [(0, '#f4fffb', 1), (.35, '#cdeee9', 1), (.7, '#7fb9b8', 1), (1, '#2f6168', 1)])
d += lin('afloor', [(0, '#0d1f22'), (1, '#030809')])
GL = 880   # bottom edge of the glass wall
b = '<rect width="1920" height="1080" fill="url(#amist)"/>'
for _ in range(26):   # drifting fog banks
    b += f'<ellipse cx="{rnd.randint(-100, 2000)}" cy="{rnd.randint(0, GL)}" rx="{rnd.randint(160, 420)}" ry="{rnd.randint(40, 110)}" fill="#ffffff" opacity="{rnd.uniform(.08, .22):.2f}" filter="url(#bl)"/>'
b += rays(1330, -80, [70, 82, 95, 108, 120], 1100, [60, 90, 70, 90, 60], '#ffffff', .22)
# --- the octopus behind the glass (deep teal, hazed by the mist) ---
oc = dict(sh='#0b2e36', mid='#1d4e57', hi='#4f8a8c', suck='#86b0ac', cup='#2c5a60')
ocb = dict(oc, mid='#174650', hi='#35696e')
HX, HY = 1335, 560
far = ''
arms_back = [   # (x0, y0, heading, length, a, b, width, wave)
    (HX + 80, HY + 20, 55, 360, .4, 6.0, 64, .4),
    (HX + 110, HY - 10, 18, 420, -.2, -5.5, 62, .3),
    (HX + 120, HY - 40, -15, 400, -.6, -6.5, 58, .3),
]
for i, (x0, y0, th, L, a, bb, w, wv) in enumerate(arms_back):
    far += arm(curve(x0, y0, th, L, a, bb, w0=w, wav=wv), ocb, seed=i, rim='#d8fff8', lw=3)
arms_front = [
    (HX - 50, HY + 60, 108, 300, .2, -6.0, 72, .3),
    (HX + 10, HY + 70, 84, 290, -.3, 6.5, 72, .3),
    (HX + 70, HY + 50, 52, 330, .1, 7.0, 68, .3),
    (HX - 100, HY + 40, 148, 330, -.2, -6.5, 68, .4),
]
for i, (x0, y0, th, L, a, bb, w, wv) in enumerate(arms_front):
    far += arm(curve(x0, y0, th, L, a, bb, w0=w, wav=wv), oc, seed=10 + i, rim='#e9fffb', lw=3)
# the reaching arm: long, out of the haze, tip pressed on the glass where the hand is
reach = curve(HX - 90, HY + 30, 176, 460, .35, -.2, w0=66, taper=.8, wav=.25, wf=2)
far += arm(reach, oc, side=1, seed=40, rim='#f4fffc', lw=3)
# mantle (behind and above) + head as one silhouette, then fills, crease, eyes, siphon
dm, mo = mantle(1450, 330, 170, 225, 25, oc, 'amant', lw=4, part='outline')
dh, ho = head(HX, HY, 150, 108, -12, oc, 'ahead', lw=4, part='outline')
_, mf = mantle(1450, 330, 170, 225, 25, oc, 'amant', rim='#e9fffb', lw=4, part='fill')
_, hf = head(HX, HY, 150, 108, -12, oc, 'ahead', crease=f'M{HX - 30},{HY - 92} Q{HX + 60},{HY - 60} {HX + 140},{HY - 120}')
d += dm + dh
far += mo + ho + mf + hf
far += siphon(HX + 120, HY + 30, 60, 20, 40, oc)
far += eye(HX - 70, HY - 10, 30, -12, skin=oc['mid'], iris='#f2d27a', look=(-.15, 0))
far += eye(HX + 60, HY - 36, 26, -12, skin=oc['mid'], iris='#e4c46a', look=(-.15, 0))
b += f'<g>{far}</g>'
b += '<ellipse cx="1470" cy="500" rx="360" ry="400" fill="#e8fbf7" opacity=".22" filter="url(#bl)"/>'   # mist over the body
tipx, tipy = reach[-1][0], reach[-1][1]
for k, (dx, dy, r) in enumerate([(0, 0, 12), (20, 12, 14), (42, 20, 16)]):   # flattened suckers pressed on the glass
    b += f'<circle cx="{tipx + dx:.0f}" cy="{tipy + dy:.0f}" r="{r}" fill="#b3d6d1" stroke="#0b2e36" stroke-width="3"/><circle cx="{tipx + dx:.0f}" cy="{tipy + dy:.0f}" r="{r * .45:.1f}" fill="#3b6a70"/>'
# --- the round ink ring floating in the mist (no letters) ---
ix, iy, ir = 1030, 290, 125
b += f'<circle cx="{ix}" cy="{iy}" r="{ir + 10}" fill="none" stroke="#f2d27a" stroke-width="90" opacity=".6" filter="url(#bl)"/>'
b += f'<circle cx="{ix}" cy="{iy}" r="{ir}" fill="none" stroke="#fff3c8" stroke-width="30" opacity=".75" filter="url(#bl12)"/>'
ink = ''
for k in range(80):   # thick, uneven brush ring
    a = k / 80 * 6.283; th = 16 + 8 * math.sin(a * 3 + 1) + 6 * math.sin(a * 7)
    ink += f'<circle cx="{ix + math.cos(a) * ir:.1f}" cy="{iy + math.sin(a) * ir:.1f}" r="{th:.1f}" fill="#0a1c22"/>'
for a, L, w in [(.4, 40, 12), (1.9, 30, 9), (2.7, 52, 13), (3.9, 28, 9), (4.8, 46, 12), (5.6, 34, 9)]:   # short tendrils
    x0, y0 = ix + math.cos(a) * ir, iy + math.sin(a) * ir
    x1, y1 = ix + math.cos(a + .12) * (ir + L), iy + math.sin(a + .12) * (ir + L)
    ink += f'<path d="M{x0:.0f},{y0:.0f} L{x1:.0f},{y1:.0f}" stroke="#0a1c22" stroke-width="{w}" stroke-linecap="round" fill="none"/><circle cx="{x1:.0f}" cy="{y1:.0f}" r="{w * .75:.0f}" fill="#0a1c22"/>'
b += f'<g filter="url(#ink)" opacity=".94">{ink}</g>'
for sx, sy, s in ((1190, 170, 18), (1700, 160, 20), (1660, 440, 14), (1110, 470, 12)):
    b += spark(sx, sy, s, '#fffbe8', .9)
for gx, gw, go in ((300, 80, .06), (520, 30, .08), (1560, 120, .05), (1790, 40, .07)):   # glass reflections
    b += f'<rect x="{gx}" y="0" width="{gw}" height="{GL}" fill="#ffffff" opacity="{go}" transform="skewX(-8)"/>'
# --- the dark viewing room in front of the glass ---
b += f'<rect x="0" y="{GL}" width="1920" height="{1080 - GL}" fill="url(#afloor)"/>'
b += f'<rect x="0" y="{GL - 6}" width="1920" height="12" fill="#040b0d"/><rect x="0" y="{GL + 6}" width="1920" height="3" fill="#bfeee8" opacity=".35"/>'
b += f'<ellipse cx="1150" cy="{GL + 40}" rx="760" ry="34" fill="#bfeee8" opacity=".16" filter="url(#soft)"/>'
# the small figure in a hazard suit, seen from behind, right glove flat on the glass
fx, fy = 700, 950   # feet centre
suit, dk, rimc, glove = '#9a4a16', '#5a2a0c', '#ffd8a0', '#c98a2a'
wx, wy = tipx - 22, tipy + 40   # wrist, so the flat glove lies just left of the pressed suckers
fig = f'<ellipse cx="{fx + 10}" cy="{fy + 6}" rx="130" ry="16" fill="#000" opacity=".55"/>'
for sx in (-1, 1):   # legs + boots
    fig += f'<path d="M{fx + sx * 8},{fy - 165} L{fx + sx * 56},{fy - 165} L{fx + sx * 52},{fy - 18} L{fx + sx * 10},{fy - 18}Z" fill="{dk}"/>'
    fig += f'<rect x="{fx + (sx - 1) * 30 + sx * 6 + 2}" y="{fy - 30}" width="56" height="34" rx="10" fill="#241208"/>'
fig += f'<path d="M{fx - 78},{fy - 300} C{fx - 92},{fy - 240} {fx - 70},{fy - 190} {fx - 62},{fy - 150} L{fx + 62},{fy - 150} C{fx + 70},{fy - 190} {fx + 92},{fy - 240} {fx + 78},{fy - 300} Q{fx},{fy - 330} {fx - 78},{fy - 300}Z" fill="{suit}"/>'   # torso
fig += f'<path d="M{fx - 20},{fy - 300} L{fx - 20},{fy - 150} M{fx - 62},{fy - 200} Q{fx},{fy - 186} {fx + 62},{fy - 200}" stroke="{dk}" stroke-width="5" opacity=".6" fill="none"/>'
fig += f'<rect x="{fx - 46}" y="{fy - 290}" width="92" height="110" rx="20" fill="{dk}"/><rect x="{fx - 36}" y="{fy - 280}" width="72" height="14" rx="7" fill="{suit}" opacity=".6"/>'   # air pack
fig += f'<path d="M{fx - 78},{fy - 300} C{fx - 92},{fy - 240} {fx - 70},{fy - 190} {fx - 62},{fy - 150}" stroke="{rimc}" stroke-width="6" fill="none"/>'
fig += f'<path d="M{fx - 80},{fy - 292} C{fx - 104},{fy - 240} {fx - 100},{fy - 190} {fx - 94},{fy - 150}" stroke="{suit}" stroke-width="40" stroke-linecap="round" fill="none"/>'   # left arm down
fig += f'<path d="M{fx - 100},{fy - 280} C{fx - 122},{fy - 240} {fx - 118},{fy - 190} {fx - 113},{fy - 160}" stroke="{rimc}" stroke-width="5" fill="none"/>'
fig += hand(fx - 94, fy - 140, 182, 30, 'L', 'back', 'open', skin=glove, line='#2a1406')
fig += f'<path d="M{fx + 66},{fy - 292} Q{fx + 104},{fy - 340} {wx:.0f},{wy + 6:.0f}" stroke="{suit}" stroke-width="40" stroke-linecap="round" fill="none"/>'   # right arm up to the glass
fig += f'<path d="M{fx + 86},{fy - 296} Q{fx + 122},{fy - 342} {wx + 16:.0f},{wy:.0f}" stroke="{rimc}" stroke-width="5" fill="none"/>'
fig += hand(wx, wy, 6, 36, 'R', 'back', 'flat', skin=glove, line='#2a1406')
fig += f'<path d="M{fx - 62},{fy - 296} C{fx - 72},{fy - 400} {fx + 72},{fy - 400} {fx + 62},{fy - 296} Q{fx},{fy - 280} {fx - 62},{fy - 296}Z" fill="{suit}"/>'   # hood
fig += f'<path d="M{fx - 62},{fy - 300} C{fx - 72},{fy - 402} {fx + 72},{fy - 402} {fx + 62},{fy - 300}" stroke="{rimc}" stroke-width="6" fill="none"/>'
fig += f'<path d="M{fx - 40},{fy - 330} Q{fx},{fy - 318} {fx + 40},{fy - 330}" stroke="{dk}" stroke-width="5" fill="none" opacity=".6"/>'
b += fig
b += f'<circle cx="{tipx:.0f}" cy="{tipy:.0f}" r="70" fill="#fff6d0" opacity=".5" filter="url(#soft)"/>'   # glow where the two touch
b += spark(int(tipx) + 4, int(tipy) - 60, 18, '#fffbe8', .95)
d += rad('avig', 960, 540, 1150, [(0, '#000', 0), (.65, '#000', 0), (1, '#021015', .55)])
b += '<rect width="1920" height="1080" fill="url(#avig)"/>'
open(os.path.join(HERE, 'A.html'), 'w').write(page('#9fd3d0', svg(d, b), [("EARTH'S", 140, 'w'), ('TRUE', 140, 'w'), ('ALIEN?', 205, 'y')], outline='#06191d'))


# =========================== B: ARMS THAT THINK (intuitive: neuron nets in every arm, a small donut in the head) ===========================
rnd = random.Random(5)
d = FILTERS
d += lin('bbg', [(0, '#1a1050'), (.55, '#0c0a30'), (1, '#05051a')])
d += rad('bhalo', 1240, 520, 760, [(0, '#5a3aa8', .55), (.5, '#2a1a6a', .25), (1, '#0c0a30', 0)])
b = '<rect width="1920" height="1080" fill="url(#bbg)"/><rect width="1920" height="1080" fill="url(#bhalo)"/>'
b += rays(1300, -120, [72, 84, 96, 108], 1100, [70, 110, 90, 70], '#a99cff', .16)
b += stars(70, 1000, col='#cfd8ff', op=.45, sparks=0)
oc = dict(sh='#6a1c18', mid='#c4472f', hi='#f39468', suck='#f7d2bc', cup='#b8664e')
CX, CY = 1240, 560
spec = [   # (dx, dy, heading, length, a, b, width) arms radiating from below the eyes
    (-70, 40, 192, 560, .3, 5.5, 74),     # far left, tip curls up
    (-60, 70, 155, 560, .2, -5.0, 78),    # left-down
    (-30, 90, 118, 470, -.3, 6.0, 80),    # down-left
    (10, 95, 92, 420, -.6, -6.5, 80),     # down
    (50, 85, 62, 380, -.4, -7.0, 78),     # down-right, curls back to the left
    (70, 60, 25, 470, -.6, -6.0, 76),     # right
    (75, 30, -8, 470, -.5, -6.5, 72),     # right-up
    (-75, 10, 215, 520, .4, 6.0, 70),     # left-up
]
order = [7, 6, 0, 5, 1, 4, 2, 3]
curves = {i: curve(CX + s[0], CY + s[1], s[2], s[3], s[4], s[5], w0=s[6], wav=.3, wf=2.5) for i, s in enumerate(spec)}


def neurons(C, seed, k=18, cols=('#ffe9a0', '#7ff4ff')):
    """glowing neuron net inside an arm: a soft glowing core along the arm plus linked bright cells"""
    r = random.Random(seed)
    o = f'<path d="{P(off(C, 0, 2, -14))}" fill="none" stroke="#ffd36a" stroke-width="{C[0][4] * 1.1:.0f}" opacity=".55" filter="url(#soft)" stroke-linecap="round"/>'
    o += f'<path d="{P(off(C, 0, 2, -14))}" fill="none" stroke="#fff1b8" stroke-width="{C[0][4] * .35:.0f}" opacity=".55" filter="url(#bl6)" stroke-linecap="round"/>'
    pts = []
    for j in range(k):
        i = int(4 + (len(C) - 18) * j / k + r.uniform(-1, 1))
        x, y, t, u, h = C[i]; f = r.uniform(-.55, .55)
        pts.append((x - math.sin(t) * f * h, y + math.cos(t) * f * h, h))
    for (x0, y0, h0), (x1, y1, h1) in zip(pts, pts[1:]):
        o += f'<path d="M{x0:.0f},{y0:.0f} L{x1:.0f},{y1:.0f}" stroke="#fff1b8" stroke-width="{max(1.5, h0 * .07):.1f}" opacity=".8"/>'
    for x, y, h in pts:
        c = r.choice(cols); s = max(2.5, h * r.uniform(.11, .2))
        for _ in range(2):   # short dendrites
            a = r.uniform(0, 6.28)
            o += f'<path d="M{x:.0f},{y:.0f} l{math.cos(a) * h * .45:.0f},{math.sin(a) * h * .45:.0f}" stroke="{c}" stroke-width="{max(1.2, h * .045):.1f}" opacity=".75"/>'
        o += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{s * 2.6:.1f}" fill="{c}" opacity=".35" filter="url(#bl3)"/><circle cx="{x:.0f}" cy="{y:.0f}" r="{s:.1f}" fill="#fffbe8"/>'
    return o


# all eight arms (each lit by its own neuron net), then mantle + head as one silhouette over the arm bases
for i in order:
    b += arm(curves[i], oc, seed=i, rim='#ffc9a8', lw=4, spots=12)
    b += neurons(curves[i], 100 + i)
MXB, MYB = CX + 6, CY - 250
dm, mo = mantle(MXB, MYB, 200, 220, 4, oc, 'bmant', lw=5, part='outline')
dh, ho = head(CX, CY - 40, 165, 120, 0, oc, 'bhead', lw=5, part='outline', light=(.4, .25))
_, mf = mantle(MXB, MYB, 200, 220, 4, oc, 'bmant', rim='#ffc9a8', lw=5, part='fill', light=(.35, .25))
_, hf = head(CX, CY - 40, 165, 120, 0, oc, 'bhead', light=(.4, .25), crease=f'M{CX - 110},{CY - 140} Q{CX},{CY - 165} {CX + 110},{CY - 140}')
d += dm + dh
b += mo + ho + mf + hf
b += f'<path d="M{CX - 160},{CY - 10} Q{CX - 150},{CY + 50} {CX - 90},{CY + 72}" stroke="#ffc9a8" stroke-width="7" fill="none" opacity=".7" stroke-linecap="round"/>'
b += eye(CX - 150, CY - 70, 38, -14, skin=oc['mid'], iris='#f2d27a')   # eyes bulge out of the head outline
b += eye(CX + 150, CY - 70, 38, 14, skin=oc['mid'], iris='#f2d27a')
# the SMALL donut-shaped brain glow between the eyes (the central brain wraps the oesophagus)
b += f'<ellipse cx="{CX}" cy="{CY - 70}" rx="46" ry="28" fill="none" stroke="#ffd36a" stroke-width="20" opacity=".75" filter="url(#bl6)"/>'
b += f'<ellipse cx="{CX}" cy="{CY - 70}" rx="42" ry="25" fill="none" stroke="#fff3c2" stroke-width="8"/>'
for k in range(10):
    a = k / 10 * 6.283
    b += f'<circle cx="{CX + math.cos(a) * 42:.0f}" cy="{CY - 70 + math.sin(a) * 25:.0f}" r="4" fill="#ffffff"/>'
for sx, sy, s in ((1680, 160, 22), (980, 230, 14), (1780, 520, 16), (840, 700, 14), (1560, 760, 12)):
    b += spark(sx, sy, s, '#fff1c8', .9)
d += rad('bvig', 960, 540, 1150, [(0, '#000', 0), (.65, '#000', 0), (1, '#000', .55)])
b += '<rect width="1920" height="1080" fill="url(#bvig)"/>'
open(os.path.join(HERE, 'B.html'), 'w').write(page('#0c0a30', svg(d, b), [('ARMS', 200, 'w'), ('THAT', 120, 'w'), ('THINK', 210, 'y')], outline='#070418'))


# =========================== C: 3 HEARTS, BLUE BLOOD (intuitive: a glass-like octopus with three glowing hearts) ===========================
rnd = random.Random(9)
d = FILTERS
d += lin('cbg', [(0, '#0a2a44'), (.5, '#06182c'), (1, '#020812')])
d += rad('chalo', 1300, 420, 700, [(0, '#2a7ab8', .55), (.5, '#14456e', .25), (1, '#06182c', 0)])
b = '<rect width="1920" height="1080" fill="url(#cbg)"/><rect width="1920" height="1080" fill="url(#chalo)"/>'
b += rays(1500, -150, [95, 105, 115, 125, 135], 1250, [60, 90, 60, 80, 50], '#9fdcff', .14)
b += bubbles(rnd, 26, 900, 80, 1880, 800, op=.35)
b += stars(60, 1000, col='#bfe6ff', op=.4, sparks=0)
gc = dict(sh='#3b2f7a', mid='#7f73c9', hi='#d8d2ff', suck='#e6e0ff', cup='#8e84d0')
gcb = dict(gc, sh='#2a2160', mid='#5a4fa0', hi='#a49ae0')
MX, MY, MR = 1440, 330, -38   # mantle centre and tilt (pointing up-right: jetting mantle first)
# arms trail behind to the lower left, gently waving
base = (1215, 520)
tr = [   # (dx, dy, heading, L, a, b, w, back?)
    (-10, 30, 160, 720, -.6, 4.5, 66, 1),
    (20, 40, 138, 640, .4, -4.5, 66, 1),
    (40, 10, 128, 600, -.3, 6.0, 64, 1),
    (-40, 0, 172, 760, .2, -5.0, 70, 0),
    (-20, 40, 150, 720, -.5, 5.5, 74, 0),
    (10, 60, 135, 640, .6, -6.0, 74, 0),
    (-50, -20, 186, 640, -.4, 6.0, 64, 0),
    (40, 60, 118, 520, .2, 6.5, 66, 0),
]
cc = {}
for i, (dx, dy, th, L, a, bb, w, bk) in enumerate(tr):
    cc[i] = curve(base[0] + dx, base[1] + dy, th, L, a, bb, w0=w, wav=.6, wf=2)


def vessel(C, w, op=1, i1=-10):
    o = f'<path d="{P(off(C, .05, 0, i1))}" fill="none" stroke="#3fb4ff" stroke-width="{w * 2.6:.1f}" opacity="{.5 * op:.2f}" filter="url(#bl6)" stroke-linecap="round"/>'
    o += f'<path d="{P(off(C, .05, 0, i1))}" fill="none" stroke="#8fe4ff" stroke-width="{w:.1f}" opacity="{.95 * op:.2f}" stroke-linecap="round"/>'
    return o


for i in (0, 1, 2):
    b += arm(cc[i], gcb, seed=i, rim='#cfe9ff', lw=3, op=.85)
    b += vessel(cc[i], 4, .6)
for i in (6, 3, 4, 5, 7):
    b += arm(cc[i], gc, seed=10 + i, rim='#e8f4ff', lw=3, op=.95)
    b += vessel(cc[i], 5)
dm, mm = mantle(MX, MY, 175, 285, 90 + MR + 180 - 180, gc, 'cmant', rim='#e8f4ff', lw=4, op=.78, light=(.5, .2))
d += dm; b += mm
# inside the mantle (seen through the glassy skin): two gills, two gill hearts, one bigger systemic heart, blue vessels


def heart(x, y, s, rot=0):
    pth = f'M0,{s * .35:.1f} C{-s * .1:.1f},{s * .2:.1f} {-s:.1f},{-s * .1:.1f} {-s * .55:.1f},{-s * .6:.1f} C{-s * .25:.1f},{-s * .9:.1f} 0,{-s * .55:.1f} 0,{-s * .35:.1f} C0,{-s * .55:.1f} {s * .25:.1f},{-s * .9:.1f} {s * .55:.1f},{-s * .6:.1f} C{s:.1f},{-s * .1:.1f} {s * .1:.1f},{s * .2:.1f} 0,{s * .35:.1f}Z'
    pth = f'M0,{s * .75:.1f} C{-s * .3:.1f},{s * .45:.1f} {-s * 1.05:.1f},{s * .05:.1f} {-s * 1.0:.1f},{-s * .4:.1f} C{-s * .95:.1f},{-s * .95:.1f} {-s * .2:.1f},{-s * 1.0:.1f} 0,{-s * .5:.1f} C{s * .2:.1f},{-s * 1.0:.1f} {s * .95:.1f},{-s * .95:.1f} {s * 1.0:.1f},{-s * .4:.1f} C{s * 1.05:.1f},{s * .05:.1f} {s * .3:.1f},{s * .45:.1f} 0,{s * .75:.1f}Z'
    o = f'<g transform="translate({x} {y}) rotate({rot})">'
    o += f'<circle r="{s * 2.2:.1f}" fill="#3fb4ff" opacity=".45" filter="url(#soft)"/>'
    o += f'<path d="{pth}" fill="#2a8cff" stroke="#e8fbff" stroke-width="{s * .09:.1f}"/>'
    o += f'<path d="M{-s * .62:.1f},{-s * .55:.1f} Q{-s * .75:.1f},{-s * .1:.1f} {-s * .4:.1f},{s * .2:.1f}" stroke="#d9f6ff" stroke-width="{s * .16:.1f}" fill="none" stroke-linecap="round" opacity=".9"/>'
    o += f'<circle cx="{-s * .1:.1f}" cy="{-s * .05:.1f}" r="{s * .45:.1f}" fill="#bff0ff" opacity=".6" filter="url(#bl6)"/>'
    return o + '</g>'


def gill(x, y, L, rot):
    o = f'<g transform="translate({x} {y}) rotate({rot})" opacity=".85">'
    o += f'<path d="M0,0 L{L},0" stroke="#bfe6ff" stroke-width="5"/>'
    for k in range(1, 12):
        px = L * k / 12; hw = 22 * math.sin(math.pi * k / 12)
        o += f'<path d="M{px:.0f},0 l{-6},{-hw:.0f} M{px:.0f},0 l{-6},{hw:.0f}" stroke="#bfe6ff" stroke-width="3" opacity=".75"/>'
    return o + '</g>'


hx, hy = 1395, 395   # systemic heart
g1, g2 = (1290, 300), (1505, 475)   # gill hearts beside each gill
b += gill(g1[0] + 40, g1[1] + 5, 160, -38 - 6) + gill(g2[0] + 5, g2[1] - 60, 160, -38 + 6)
vs = [  # vessels inside the mantle: gill heart -> gill -> systemic heart -> body
    f'M{g1[0]},{g1[1]} Q{g1[0] + 60},{g1[1] - 80} {g1[0] + 140},{g1[1] - 115} Q{hx - 10},{hy - 120} {hx},{hy}',
    f'M{g2[0]},{g2[1]} Q{g2[0] + 80},{g2[1] - 40} {g2[0] + 120},{g2[1] - 120} Q{hx + 80},{hy - 60} {hx},{hy}',
    f'M{hx},{hy} Q{hx + 120},{hy - 220} {1640},{150}',
    f'M{hx},{hy} Q{1300},{460} {base[0]},{base[1] + 20}',
    f'M{g1[0]},{g1[1]} Q{1240},{400} {base[0] - 20},{base[1]}',
    f'M{g2[0]},{g2[1]} Q{1380},{540} {base[0] + 20},{base[1] + 40}',
]
for v in vs:
    b += f'<path d="{v}" fill="none" stroke="#3fb4ff" stroke-width="14" opacity=".5" filter="url(#bl6)"/><path d="{v}" fill="none" stroke="#8fe4ff" stroke-width="5"/>'
b += heart(g1[0], g1[1], 42, -20) + heart(g2[0], g2[1], 42, 10) + heart(hx, hy, 74, -8)
# head, eye and siphon at the base of the mantle
dh, hf = head(1252, 495, 140, 112, -38, gc, 'chead', light=(.6, .25))
d += dh
b += f'<ellipse cx="1252" cy="495" rx="140" ry="112" transform="rotate(-38 1252 495)" fill="none" stroke="#07121a" stroke-width="8"/>' + f'<g opacity=".95">{hf}</g>'
b += f'<path d="M1150,470 Q1170,580 1290,600" stroke="#e8f4ff" stroke-width="6" fill="none" opacity=".6" stroke-linecap="round"/>'
b += eye(1230, 462, 32, -38, skin=gc['mid'], iris='#f2d27a')
b += siphon(1310, 570, 70, 140, 40, gc)
b += bubbles(random.Random(3), 22, 1050, 560, 1240, 720, col='#e8fbff', op=.8)
for sx, sy, s in ((1760, 140, 22), (1020, 260, 14), (1700, 560, 16), (1580, 120, 12), (980, 560, 12)):
    b += spark(sx, sy, s, '#e8fbff', .9)
d += rad('cvig', 960, 540, 1150, [(0, '#000', 0), (.65, '#000', 0), (1, '#000', .6)])
b += '<rect width="1920" height="1080" fill="url(#cvig)"/>'
open(os.path.join(HERE, 'C.html'), 'w').write(page('#06182c', svg(d, b), [('3 HEARTS,', 175, 'y'), ('BLUE', 175, 'w'), ('BLOOD', 175, 'w')], outline='#020814'))
print('ok')
