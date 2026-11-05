# Thumbnails A-C for neptune-mysteries (guideline 16-6, 16-8; brief tools/briefs/thumb_art.md). Run: python3 videos/neptune-mysteries/thumb/make.py
# A  IT RAINS / DIAMONDS?   homage: Singin' in the Rain (1952) lamppost pose; frog in a fedora swings off a lamppost deep inside Neptune
#                           while diamonds fall (S37-S39: "scientists suspect diamonds may be forming ... drift downward like heavy hail"; question keeps the hedge)
# B  MATH = / A PLANET      intuitive: a giant pencil's tip finishes the drawn orbit and Neptune appears in the crosshair; frog astronomer with
#                           a brass telescope (S10-S12: found with pure mathematics, "found with the tip of a pencil before it was found with the eye")
# C  IT ORBITS / BACKWARD   intuitive: Neptune spins one way (white arrows), Triton's orbit runs the other way (orange arrows); frog in a space
#                           helmet rides Triton looking back (S48-S49: retrograde orbit, no other large moon circles backward)
import os, sys, math, random
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../tools'))
from thumb_lib import page, svg, lin, rad, spark

INK = '#1d2b1c'; GREEN = '#6aa55a'; GOLD = '#F2D27A'

FILTERS = ''.join(f'<filter id="b{s}" x="-60%" y="-60%" width="220%" height="220%"><feGaussianBlur stdDeviation="{s}"/></filter>' for s in (3, 6, 12, 24, 50))


# ---------------- mascot frog (tools/assets/frog.svg body; outfits/props per thumbnail) ----------------
def frog(x, y, s, la='q-14 6 -16 22', ra='q14 6 16 22', mouth='o', look=(2, 0), front='', back='', flip=False, hat='', helmet=False, tilt=0):
    sx = -s if flip else s
    g = f'<g transform="translate({x} {y}) rotate({tilt}) scale({sx} {s})" stroke="{INK}" stroke-linejoin="round" stroke-linecap="round">'
    g += back
    g += '<ellipse cx="-22" cy="4" rx="16" ry="9" fill="#4d8a4a" stroke-width="3.2"/><ellipse cx="22" cy="4" rx="16" ry="9" fill="#4d8a4a" stroke-width="3.2"/>'
    g += f'<path d="M-34 0 q-6 -64 34 -70 q40 -2 42 62 q0 10 -6 12 q-36 6 -70 -4z" fill="{GREEN}" stroke-width="4"/>'
    g += '<ellipse cx="2" cy="-12" rx="22" ry="20" fill="#9cc98a" stroke="none" opacity=".7"/>'
    g += '<path d="M-26 -50 q6 -16 22 -18" fill="none" stroke="#b9e0a6" stroke-width="3" opacity=".7"/>'
    dx, dy = look
    g += f'<circle cx="-10" cy="-66" r="13" fill="#e3e5d6" stroke-width="3.2"/><circle cx="{-10 + dx}" cy="{-66 + dy}" r="5" fill="{INK}" stroke="none"/>'
    g += f'<circle cx="22" cy="-66" r="13" fill="#e3e5d6" stroke-width="3.2"/><circle cx="{22 + dx}" cy="{-66 + dy}" r="5" fill="{INK}" stroke="none"/>'
    g += f'<circle cx="{-8 + dx}" cy="{-68 + dy}" r="1.6" fill="#fff" stroke="none"/><circle cx="{24 + dx}" cy="{-68 + dy}" r="1.6" fill="#fff" stroke="none"/>'
    g += '<ellipse cx="-18" cy="-46" rx="5" ry="3" fill="#e98a8a" stroke="none" opacity=".55"/><ellipse cx="30" cy="-46" rx="5" ry="3" fill="#e98a8a" stroke="none" opacity=".55"/>'
    if mouth == 'o':
        g += '<ellipse cx="6" cy="-42" rx="6.5" ry="8" fill="#7a2f33" stroke-width="3"/><ellipse cx="6" cy="-38" rx="3.5" ry="2.6" fill="#e07b7b" stroke="none"/>'
    else:
        g += '<path d="M-8 -45 q14 14 28 0 q-14 4 -28 0z" fill="#7a2f33" stroke-width="3"/>'
    g += hat
    for st, path in (('M-32 -22', la), ('M38 -22', ra)):
        g += f'<path d="{st} {path}" fill="none" stroke-width="7.5"/><path d="{st} {path}" fill="none" stroke="{GREEN}" stroke-width="3.4"/>'
        sx0, sy0 = map(float, st[1:].split()); q = [float(v) for v in path[1:].split()]
        g += f'<circle cx="{sx0 + q[2]}" cy="{sy0 + q[3]}" r="5.5" fill="{GREEN}" stroke-width="3"/>'
    if helmet:
        g += '<circle cx="6" cy="-50" r="50" fill="#cfeaff" fill-opacity=".13" stroke="#e8eef6" stroke-width="5"/>'
        g += '<circle cx="6" cy="-50" r="45" fill="none" stroke="#fff" stroke-width="1.6" opacity=".35"/>'
        g += '<path d="M-28 -78 A40 40 0 0 1 10 -94" fill="none" stroke="#fff" stroke-width="5.5" opacity=".8"/><circle cx="38" cy="-24" r="3.2" fill="#fff" stroke="none" opacity=".6"/>'
        g += '<ellipse cx="6" cy="-4" rx="40" ry="8" fill="#c9d2de" stroke-width="3"/><path d="M-28 -6 q34 7 68 0" fill="none" stroke="#fff" stroke-width="2" opacity=".7"/>'
    g += front
    return g + '</g>'


FEDORA = ('<path d="M-30 -84 q36 -14 72 0 q4 6 -4 8 q-32 -8 -64 0 q-8 -2 -4 -8z" fill="#20253a" stroke-width="3.2"/>'
          '<path d="M-18 -84 q2 -26 26 -28 q22 2 24 28 q-24 -6 -50 0z" fill="#2c3350" stroke-width="3.2"/>'
          '<path d="M-17 -88 q25 -6 49 0" fill="none" stroke="#b5413f" stroke-width="5"/><path d="M-6 -104 q10 -6 22 0" fill="none" stroke="#6b7598" stroke-width="2.4"/>')
SCHOLAR = ('<ellipse cx="7" cy="-86" rx="30" ry="9" fill="#5a3b25" stroke-width="3"/><path d="M-14 -88 q20 -22 42 0z" fill="#7a5233" stroke-width="3"/>'
           '<circle cx="-10" cy="-66" r="15" fill="none" stroke="#c99b45" stroke-width="2.6"/><circle cx="22" cy="-66" r="15" fill="none" stroke="#c99b45" stroke-width="2.6"/>'
           '<path d="M5 -67 h2" stroke="#c99b45" stroke-width="2.6"/>')


# ---------------- shared objects ----------------
def diamond(x, y, s, rot=0, op=1.0, glow=True):
    # brilliant cut, table up; s = half width
    w = s; h1 = s * .42; h2 = s * 1.05
    o = f'<g transform="translate({x:.0f} {y:.0f}) rotate({rot:.0f})" opacity="{op:.2f}">'
    if glow:
        o += f'<circle cx="0" cy="0" r="{s * 1.6:.0f}" fill="#bfe8ff" opacity=".22" filter="url(#b12)"/>'
    o += f'<path d="M{-w * .55:.1f} {-h1:.1f} L{w * .55:.1f} {-h1:.1f} L{w:.1f} 0 L0 {h2:.1f} L{-w:.1f} 0Z" fill="url(#dia)" stroke="#e9fbff" stroke-width="{max(1.2, s * .05):.1f}" stroke-linejoin="round"/>'
    # crown facets
    o += f'<path d="M{-w * .55:.1f} {-h1:.1f} L{-w * .25:.1f} 0 L0 {-h1:.1f} L{w * .25:.1f} 0 L{w * .55:.1f} {-h1:.1f}" fill="none" stroke="#ffffff" stroke-width="{max(1, s * .035):.1f}" opacity=".8"/>'
    o += f'<path d="M{-w:.1f} 0 L{w:.1f} 0" stroke="#ffffff" stroke-width="{max(1, s * .04):.1f}" opacity=".85"/>'
    o += f'<path d="M{-w * .25:.1f} 0 L0 {h2:.1f} L{w * .25:.1f} 0 M{-w * .62:.1f} 0 L0 {h2:.1f} L{w * .62:.1f} 0" fill="none" stroke="#d6f4ff" stroke-width="{max(1, s * .03):.1f}" opacity=".6"/>'
    o += f'<path d="M{-w * .55:.1f} {-h1:.1f} L0 {-h1:.1f} L{-w * .25:.1f} 0 L{-w:.1f} 0Z" fill="#ffffff" opacity=".55"/>'
    o += f'<path d="M0 0 L{w * .25:.1f} 0 L0 {h2:.1f}Z" fill="#ffffff" opacity=".35"/>'
    o += f'<path d="M{w * .25:.1f} 0 L{w:.1f} 0 L0 {h2:.1f}Z" fill="#2a5fa8" opacity=".35"/>'
    o += '</g>'
    if glow and s > 18:
        o += spark(x - s * .35, y - h1, s * .5, '#ffffff', .95)
    return o


def neptune(cx, cy, r, cid, spot=True, light=(-.45, -.45)):
    lx, ly = cx + light[0] * r, cy + light[1] * r
    d = rad(f'{cid}g', lx, ly, r * 1.7, [(0, '#8fc0ff', 1), (.25, '#3f78ea', 1), (.6, '#1f4bc2', 1), (1, '#06123d', 1)])
    d += f'<clipPath id="{cid}c"><circle cx="{cx}" cy="{cy}" r="{r}"/></clipPath>'
    d += rad(f'{cid}h', cx, cy, r * 1.35, [(0, '#5aa8ff', 0), (.72, '#5aa8ff', 0), (.76, '#6fb6ff', .55), (1, '#2c66ff', 0)])
    d += rad(f'{cid}s', cx + r * .55, cy + r * .5, r * 1.25, [(0, '#000820', .0), (.5, '#000820', .0), (1, '#000820', .85)])
    o = f'<circle cx="{cx}" cy="{cy}" r="{r * 1.35:.0f}" fill="url(#{cid}h)"/>'
    o += f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="url(#{cid}g)"/>'
    o += f'<g clip-path="url(#{cid}c)">'
    random.seed(cid)
    for k in range(9):
        yy = cy - r + (k + .5) * 2 * r / 9 + random.uniform(-8, 8) * r / 300
        o += f'<ellipse cx="{cx}" cy="{yy:.0f}" rx="{r * 1.1:.0f}" ry="{r * random.uniform(.03, .07):.0f}" fill="{random.choice(["#6aa2ff", "#173a9e", "#2b5fd8", "#88b8ff"])}" opacity="{random.uniform(.18, .4):.2f}" transform="rotate(-8 {cx} {cy})"/>'
    if spot:
        o += f'<ellipse cx="{cx - r * .18:.0f}" cy="{cy + r * .32:.0f}" rx="{r * .2:.0f}" ry="{r * .1:.0f}" fill="#0a1a5c" opacity=".85" transform="rotate(-8 {cx} {cy})"/>'
        o += f'<path d="M{cx - r * .42:.0f} {cy + r * .25:.0f} q{r * .25:.0f} {-r * .1:.0f} {r * .48:.0f} {-r * .03:.0f}" fill="none" stroke="#f2f8ff" stroke-width="{r * .035:.1f}" stroke-linecap="round" opacity=".85" filter="url(#b3)"/>'
    for (u, v, L) in ((-.35, -.35, .5), (.1, -.05, .42), (-.55, .05, .3), (.25, .55, .35), (.05, -.62, .28)):
        o += f'<path d="M{cx + u * r:.0f} {cy + v * r:.0f} q{L * r * .5:.0f} {-r * .04:.0f} {L * r:.0f} {-r * .02:.0f}" fill="none" stroke="#ffffff" stroke-width="{r * .03:.1f}" stroke-linecap="round" opacity=".75" filter="url(#b3)"/>'
    o += f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="url(#{cid}s)"/>'
    o += '</g>'
    o += f'<circle cx="{cx}" cy="{cy}" r="{r - 2}" fill="none" stroke="#bfe0ff" stroke-width="{max(2, r * .012):.1f}" opacity=".55"/>'
    return d, o


def arrowhead(x, y, ang, s, col, op=1):
    a = math.radians(ang)
    p1 = (x + s * math.cos(a), y + s * math.sin(a))
    p2 = (x + s * .7 * math.cos(a + 2.4), y + s * .7 * math.sin(a + 2.4))
    p3 = (x + s * .7 * math.cos(a - 2.4), y + s * .7 * math.sin(a - 2.4))
    return f'<path d="M{p1[0]:.1f} {p1[1]:.1f} L{p2[0]:.1f} {p2[1]:.1f} L{x:.1f} {y:.1f} L{p3[0]:.1f} {p3[1]:.1f}Z" fill="{col}" opacity="{op}" stroke="#0a0f24" stroke-width="3" stroke-linejoin="round"/>'


def starfield(n, x0=0, x1=1920, y0=0, y1=1080, seed=1, op=.7):
    random.seed(seed)
    return ''.join(f'<circle cx="{random.uniform(x0, x1):.0f}" cy="{random.uniform(y0, y1):.0f}" r="{random.choice([1, 1.4, 1.9, 2.5])}" fill="#e8f1ff" opacity="{random.uniform(.15, op):.2f}"/>' for _ in range(n))


DIA = lin('dia', [(0, '#ffffff'), (.35, '#cfefff'), (.7, '#7fc4f0'), (1, '#3a7cc8')], 0.4, 1)


# ====================================================================== A  Singin' in the Rain homage
def thumb_A():
    random.seed(7)
    PX = 1180; GY = 870
    d = FILTERS + DIA
    d += lin('skyA', [(0, '#050a2a'), (.55, '#0c1d5c'), (1, '#16337a')])
    d += lin('floorA', [(0, '#0c1b4a'), (1, '#03081c')])
    d += rad('lampA', PX, 205, 900, [(0, '#ffe9b0', .55), (.25, '#ffd27a', .22), (.6, '#8bb7ff', .06), (1, '#000', 0)])
    d += rad('heatA', 960, 1250, 900, [(0, '#ff8a3c', .5), (.5, '#c2402a', .15), (1, '#000', 0)])
    d += '<linearGradient id="coneA" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ffe8b0" stop-opacity=".55"/><stop offset="1" stop-color="#ffe8b0" stop-opacity="0"/></linearGradient>'
    d += lin('post', [(0, '#05081a'), (.45, '#2b3558'), (.6, '#6a7aa8'), (1, '#0a1030')], 1, 0)
    d += lin('umb', [(0, '#2a2f4a'), (1, '#0c0f1f')])
    b = '<rect width="1920" height="1080" fill="url(#skyA)"/>'
    # distant slush "fog" layers
    for k in range(5):
        b += f'<ellipse cx="{random.randint(200, 1700)}" cy="{random.randint(500, 820)}" rx="{random.randint(300, 600)}" ry="{random.randint(40, 90)}" fill="#2a4ea0" opacity=".14" filter="url(#b24)"/>'
    b += '<rect width="1920" height="1080" fill="url(#lampA)"/>'
    # floor (wet slush, reflective)
    b += f'<rect x="0" y="{GY}" width="1920" height="{1080 - GY}" fill="url(#floorA)"/>'
    b += f'<rect x="0" y="{GY - 30}" width="1920" height="260" fill="url(#heatA)"/>'
    b += f'<path d="M0 {GY} H1920" stroke="#5f86d8" stroke-width="2" opacity=".5"/>'
    # lamp light cone + reflection on the floor
    b += f'<path d="M{PX - 60} 250 L{PX - 420} {GY + 40} L{PX + 470} {GY + 40} L{PX + 60} 250Z" fill="url(#coneA)" filter="url(#b12)" opacity=".75"/>'
    b += f'<ellipse cx="{PX + 20}" cy="{GY + 60}" rx="460" ry="60" fill="#ffe2a0" opacity=".28" filter="url(#b24)"/>'
    b += f'<rect x="{PX - 12}" y="{GY + 10}" width="24" height="180" fill="#ffd98a" opacity=".25" filter="url(#b6)"/>'
    # background falling diamonds (streaks + small gems)
    for _ in range(140):
        x = random.uniform(0, 1920); y = random.uniform(0, GY)
        if x > 1560 and y > 820: continue
        L = random.uniform(18, 50)
        b += f'<path d="M{x:.0f} {y:.0f} l{-L * .18:.1f} {L:.1f}" stroke="#bfe6ff" stroke-width="{random.choice([1.2, 1.8, 2.4])}" opacity="{random.uniform(.12, .45):.2f}" stroke-linecap="round"/>'
    for _ in range(60):
        x = random.uniform(40, 1880); y = random.uniform(30, GY - 30)
        if (x > 1560 and y > 800): continue
        near = abs(x - PX) < 450 and y > 250
        s = random.uniform(6, 14) * (1.5 if near else 1)
        b += diamond(x, y, s, random.uniform(-25, 25), random.uniform(.35, .7) * (1.3 if near else 1), glow=near)
    # splashes on the floor
    for _ in range(26):
        x = random.uniform(300, 1540); y = GY + random.uniform(10, 90)
        b += f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{random.uniform(14, 34):.0f}" ry="{random.uniform(3, 7):.0f}" fill="none" stroke="#bfe6ff" stroke-width="2" opacity="{random.uniform(.25, .6):.2f}"/>'
    # diamonds lying in the puddles
    for (x, y, s, r) in ((760, 905, 16, -10), (930, 935, 20, 15), (1420, 920, 15, 8), (640, 960, 12, 30), (1080, 985, 18, -20), (1310, 1000, 13, 12)):
        b += diamond(x, y, s, r, .95)
    # ---- lamppost ----
    b += f'<ellipse cx="{PX}" cy="{GY + 18}" rx="120" ry="16" fill="#000" opacity=".5"/>'
    b += f'<path d="M{PX - 78} {GY + 16} L{PX - 58} {GY - 70} L{PX + 58} {GY - 70} L{PX + 78} {GY + 16}Z" fill="url(#post)" stroke="#05081a" stroke-width="4"/>'
    b += f'<rect x="{PX - 70}" y="{GY - 92}" width="140" height="26" rx="6" fill="url(#post)" stroke="#05081a" stroke-width="4"/>'
    b += f'<path d="M{PX - 36} {GY - 92} L{PX - 22} {GY - 300} L{PX + 22} {GY - 300} L{PX + 36} {GY - 92}Z" fill="url(#post)" stroke="#05081a" stroke-width="4"/>'
    b += f'<rect x="{PX - 16}" y="270" width="32" height="{GY - 570}" fill="url(#post)" stroke="#05081a" stroke-width="4"/>'
    for yy in (330, 470, 560):
        b += f'<rect x="{PX - 24}" y="{yy}" width="48" height="16" rx="5" fill="url(#post)" stroke="#05081a" stroke-width="3.5"/>'
    b += f'<path d="M{PX + 10} 300 q0 -40 30 -40" fill="none" stroke="#ffd98a" stroke-width="3" opacity=".6"/>'
    # rim light from lamp on post
    b += f'<path d="M{PX + 8} 300 V{GY - 300}" stroke="#ffe2a0" stroke-width="5" opacity=".55"/>'
    # lantern
    b += f'<circle cx="{PX}" cy="205" r="210" fill="#ffd27a" opacity=".22" filter="url(#b50)"/>'
    b += f'<path d="M{PX - 30} 272 L{PX + 30} 272 L{PX + 40} 250 L{PX - 40} 250Z" fill="#141a33" stroke="#05081a" stroke-width="4"/>'
    b += f'<path d="M{PX - 40} 250 L{PX - 56} 160 L{PX + 56} 160 L{PX + 40} 250Z" fill="#fff0c2" stroke="#141a33" stroke-width="6"/>'
    b += f'<path d="M{PX} 160 V250 M{PX - 48} 205 H{PX + 48}" stroke="#141a33" stroke-width="3" opacity=".6"/>'
    b += f'<circle cx="{PX}" cy="205" r="38" fill="#fff" opacity=".9" filter="url(#b12)"/>'
    b += f'<path d="M{PX - 68} 160 L{PX} 112 L{PX + 68} 160Z" fill="#1b2140" stroke="#05081a" stroke-width="5" stroke-linejoin="round"/>'
    b += f'<circle cx="{PX}" cy="104" r="11" fill="#1b2140" stroke="#05081a" stroke-width="4"/>'
    b += f'<path d="M{PX - 62} 158 L{PX} 116" stroke="#ffd98a" stroke-width="3" opacity=".6"/>'
    # ---- frog: one hand on the post, leaning out, umbrella held wide (mirror: faces left toward the post) ----
    s = 2.75; fx = PX + 132; fy = GY + 8
    umb = ('<g transform="translate(-102 -32) rotate(-12)">'
           '<path d="M0 0 V-120" stroke="#1d2b1c" stroke-width="7"/><path d="M0 0 V-120" stroke="#c9a46a" stroke-width="3"/>'
           '<path d="M0 0 q0 14 -10 14" fill="none" stroke="#1d2b1c" stroke-width="6"/>'
           '<path d="M-72 -110 Q-70 -170 0 -178 Q70 -170 72 -110 q-12 -10 -24 0 q-12 -10 -24 0 q-12 -10 -24 0 q-12 -10 -24 0 q-12 -10 -24 0 q-12 -10 -24 0z" fill="url(#umb)" stroke-width="4"/>'
           '<path d="M-48 -110 Q-36 -160 0 -178 M48 -110 Q36 -160 0 -178 M0 -110 V-178" fill="none" stroke="#3c4566" stroke-width="2.4"/>'
           '<path d="M-60 -135 Q-50 -168 -6 -175" fill="none" stroke="#ffe2a0" stroke-width="4" opacity=".7"/>'
           '<path d="M0 -178 v-10" stroke-width="5"/></g>')
    b += f'<ellipse cx="{fx}" cy="{fy + 10}" rx="110" ry="14" fill="#000" opacity=".45"/>'
    b += frog(fx, fy, s, la='q-30 -2 -70 -10', ra='q14 -18 8 -52', mouth='o', look=(-4, -4), flip=True, hat=FEDORA,
              front=umb.replace('translate(-102 -32)', 'translate(-102 -32)'))
    # diamonds bouncing off the umbrella
    ux, uy = fx + 102 * s + 60, fy - 32 * s - 520
    for (dx, dy, ss, rr) in ((-120, -40, 22, -20), (40, -90, 28, 18), (150, 30, 18, 35), (-30, 60, 14, -40), (210, -60, 16, 10)):
        b += diamond(ux + dx, uy + dy, ss, rr, .95)
    # big hero diamonds falling in the light
    for (x, y, ss, rr) in ((960, 500, 70, -12), (1420, 200, 56, 14), (800, 740, 44, 22), (1560, 560, 50, -18), (1060, 690, 32, 30), (1700, 130, 40, 0), (640, 560, 30, -30), (1280, 420, 28, 8)):
        b += diamond(x, y, ss, rr, 1)
    return page('#050a2a', svg(d, b), [('IT RAINS', 150, 'w'), ('DIAMONDS?', 178, 'y')], outline='#040820')


# ====================================================================== B  pencil found it
def thumb_B():
    random.seed(11)
    NX, NY, NR = 1170, 640, 210
    d = FILTERS
    d += lin('skyB', [(0, '#081436'), (1, '#0d2154')])
    d += rad('glowB', NX, NY, 640, [(0, '#4f8bff', .45), (.5, '#2a56c8', .12), (1, '#000', 0)])
    d += lin('wood', [(0, '#f7c84b'), (.45, '#ffdc6e'), (.55, '#e0a72c'), (1, '#b97a14')], 0, 1)
    d += lin('cut', [(0, '#f3d3a2'), (1, '#c9925a')], 0, 1)
    d += lin('lead', [(0, '#5d6470'), (1, '#1d2028')], 0, 1)
    d += lin('ferr', [(0, '#e6e8ee'), (.5, '#8b93a3'), (1, '#c9ced8')], 0, 1)
    d += lin('scope', [(0, '#f2c76a'), (.5, '#b8862e'), (1, '#6e4a12')], 0, 1)
    d += lin('hill', [(0, '#13254f'), (1, '#050b1f')])
    nd, no = neptune(NX, NY, NR, 'nB')
    d += nd
    b = '<rect width="1920" height="1080" fill="url(#skyB)"/>'
    # blueprint grid
    for x in range(0, 1921, 60):
        b += f'<path d="M{x} 0 V1080" stroke="#4a78d0" stroke-width="{2 if x % 300 == 0 else 1}" opacity="{.22 if x % 300 == 0 else .1}"/>'
    for y in range(0, 1081, 60):
        b += f'<path d="M0 {y} H1920" stroke="#4a78d0" stroke-width="{2 if y % 300 == 0 else 1}" opacity="{.22 if y % 300 == 0 else .1}"/>'
    b += starfield(120, 0, 1920, 0, 900, 3, .6)
    b += '<rect width="1920" height="1080" fill="url(#glowB)"/>'
    # Sun (far left, off frame) and Uranus' drawn orbit + Neptune's drawn orbit (chalk lines)
    SX, SY = -700, 1180
    b += f'<circle cx="{SX + 1260}" cy="{SY - 450}" r="1" fill="none"/>'
    b += f'<path d="M{SX} {SY} m-1250 0 a1250 1250 0 0 1 2500 0" fill="none" stroke="#9fd0ff" stroke-width="3" opacity=".35" stroke-dasharray="4 12" transform="rotate(0)"/>'
    # Uranus on its orbit, with drawn "tug" arrow
    ua = math.radians(-58); ux, uy = SX + 1250 * math.cos(ua), SY + 1250 * math.sin(ua)
    if 0: b += f'<circle cx="{ux:.0f}" cy="{uy:.0f}" r="44" fill="#a9e3e6" stroke="#e8fbff" stroke-width="3"/>'
    if 0: b += f'<ellipse cx="{ux:.0f}" cy="{uy:.0f}" rx="12" ry="70" fill="none" stroke="#e8fbff" stroke-width="2.5" opacity=".6"/>'
    if 0: b += f'<circle cx="{ux - 12:.0f}" cy="{uy - 14:.0f}" r="18" fill="#fff" opacity=".35" filter="url(#b6)"/>'
    # Neptune's orbit drawn as a solid chalk line right up to the pencil tip
    R2 = math.hypot(NX - SX, NY - SY); a1 = math.atan2(NY - SY, NX - SX)
    TT = .17; pts = [(SX + R2 * math.cos(a1 + t), SY + R2 * math.sin(a1 + t)) for t in [-.5 + i * .01 for i in range(0, int((.5 + TT) / .01) + 1)]]
    b += '<path d="M' + ' L'.join(f'{x:.0f} {y:.0f}' for x, y in pts) + '" fill="none" stroke="#e9f4ff" stroke-width="7" stroke-linecap="round" opacity=".9"/>'
    b += '<path d="M' + ' L'.join(f'{x:.0f} {y:.0f}' for x, y in pts) + '" fill="none" stroke="#9fd0ff" stroke-width="16" stroke-linecap="round" opacity=".25" filter="url(#b6)"/>'
    # construction lines: from the Sun's direction and from Uranus to the predicted spot
    if 0: b += f'<path d="M{ux:.0f} {uy:.0f} L{NX} {NY}" stroke="#ffd98a" stroke-width="3" stroke-dasharray="14 10" opacity=".6"/>'
    for t in ():
        mx, my = ux + (NX - ux) * t, uy + (NY - uy) * t
        b += arrowhead(mx, my, math.degrees(math.atan2(NY - uy, NX - ux)), 20, '#ffd98a', .8)
    # Neptune + predicted crosshair ring
    b += no
    b += f'<circle cx="{NX}" cy="{NY}" r="{NR + 46}" fill="none" stroke="{GOLD}" stroke-width="6" stroke-dasharray="40 18"/>'
    for a in range(0, 360, 90):
        r1, r2 = NR + 30, NR + 100
        b += f'<path d="M{NX + r1 * math.cos(math.radians(a)):.0f} {NY + r1 * math.sin(math.radians(a)):.0f} L{NX + r2 * math.cos(math.radians(a)):.0f} {NY + r2 * math.sin(math.radians(a)):.0f}" stroke="{GOLD}" stroke-width="7" stroke-linecap="round"/>'
    for _ in range(5):
        b += spark(random.randint(NX - 300, NX + 300), random.randint(NY - 300, NY + 260), random.choice([14, 20, 26]))
    # ---- giant pencil from the top-right, tip resting on the crosshair ----
    tx, ty = pts[-1]; tx, ty = int(tx), int(ty)  # tip = end of the drawn orbit
    ang = math.degrees(math.atan2(-1, 1.05))  # direction to the top-right
    L = 1100; W = 120
    pen = f'<g transform="translate({tx} {ty}) rotate({ang:.1f})">'
    pen += f'<rect x="230" y="{-W / 2 + 12}" width="{L}" height="{W}" fill="#000" opacity=".35" filter="url(#b12)"/>'
    pen += f'<path d="M0 0 L60 {-W * .18:.0f} L60 {W * .18:.0f}Z" fill="url(#lead)" stroke="#0a0f24" stroke-width="5" stroke-linejoin="round"/>'
    pen += f'<path d="M60 {-W * .18:.0f} L210 {-W / 2} L210 {W / 2} L60 {W * .18:.0f}Z" fill="url(#cut)" stroke="#0a0f24" stroke-width="5" stroke-linejoin="round"/>'
    pen += f'<path d="M210 {-W / 2} L{L} {-W / 2} L{L} {W / 2} L210 {W / 2}Z" fill="url(#wood)" stroke="#0a0f24" stroke-width="6"/>'
    pen += f'<path d="M210 {-W / 6:.0f} H{L} M210 {W / 6:.0f} H{L}" stroke="#a86d12" stroke-width="3" opacity=".7"/>'
    pen += f'<path d="M230 {-W / 2 + 8} H{L - 10}" stroke="#fff3b8" stroke-width="7" opacity=".8"/>'
    pen += f'<path d="M210 {-W / 2} q-20 {W / 6:.0f} 0 {W / 3:.0f} q-20 {W / 6:.0f} 0 {W / 3:.0f} q-20 {W / 6:.0f} 0 {W / 3:.0f}" fill="none" stroke="#0a0f24" stroke-width="5"/>'
    pen += f'<rect x="{L}" y="{-W / 2 - 4}" width="110" height="{W + 8}" fill="url(#ferr)" stroke="#0a0f24" stroke-width="6"/>'
    pen += ''.join(f'<path d="M{L + k} {-W / 2 - 4} V{W / 2 + 4}" stroke="#5c6474" stroke-width="3"/>' for k in (22, 40, 70, 88))
    pen += f'<rect x="{L + 110}" y="{-W / 2}" width="120" height="{W}" rx="20" fill="#f08aa0" stroke="#0a0f24" stroke-width="6"/>'
    pen += '</g>'
    b += f'<circle cx="{tx}" cy="{ty}" r="70" fill="#fff" opacity=".45" filter="url(#b24)"/>'
    b += pen
    b += f'<circle cx="{tx}" cy="{ty}" r="16" fill="#fff" opacity=".9" filter="url(#b6)"/>'
    b += spark(tx - 30, ty + 26, 30, '#ffffff', .95)
    # ---- foreground hill with the frog astronomer and an old telescope ----
    b += '<path d="M0 930 Q300 860 640 880 Q1100 910 1920 1010 L1920 1080 L0 1080Z" fill="url(#hill)"/>'
    b += '<path d="M0 930 Q300 860 640 880 Q1100 910 1920 1010" fill="none" stroke="#5f86d8" stroke-width="3" opacity=".6"/>'
    fx, fy, s = 560, 900, 3.0
    # telescope on a tripod, pointed at Neptune, frog's eye at the eyepiece
    tpx, tpy = fx + 170, fy - 150
    ta = math.degrees(math.atan2(NY - tpy, NX - tpx))
    b += f'<path d="M{tpx} {tpy} L{tpx - 70} {fy + 10} M{tpx} {tpy} L{tpx + 60} {fy + 14} M{tpx} {tpy} L{tpx + 10} {fy + 20}" stroke="#0a0f24" stroke-width="13" stroke-linecap="round"/>'
    b += f'<path d="M{tpx} {tpy} L{tpx - 70} {fy + 10} M{tpx} {tpy} L{tpx + 60} {fy + 14} M{tpx} {tpy} L{tpx + 10} {fy + 20}" stroke="#7a5233" stroke-width="6" stroke-linecap="round"/>'
    tel = f'<g transform="translate({tpx} {tpy}) rotate({ta:.1f})">'
    tel += '<rect x="-120" y="-22" width="300" height="44" rx="8" fill="url(#scope)" stroke="#0a0f24" stroke-width="5"/>'
    tel += '<rect x="170" y="-30" width="40" height="60" rx="6" fill="url(#scope)" stroke="#0a0f24" stroke-width="5"/>'
    tel += '<rect x="-160" y="-13" width="44" height="26" rx="5" fill="#6e4a12" stroke="#0a0f24" stroke-width="4"/>'
    tel += '<path d="M-110 -12 H160" stroke="#ffeab0" stroke-width="5" opacity=".7"/>'
    tel += '<ellipse cx="210" cy="0" rx="8" ry="27" fill="#bfe0ff" stroke="#0a0f24" stroke-width="3"/>'
    tel += '</g>'
    b += tel
    b += f'<ellipse cx="{fx}" cy="{fy + 8}" rx="100" ry="14" fill="#000" opacity=".4"/>'
    b += frog(fx, fy, s, la='q-14 6 -16 22', ra='q20 -6 34 -18', mouth='o', look=(4, -3), hat=SCHOLAR, tilt=4)
    b += f'<path d="M{fx + 100} {fy - 236} q30 -30 70 -24" fill="none" stroke="#ffffff" stroke-width="5" stroke-linecap="round" opacity=".0"/>'
    return page('#081436', svg(d, b), [('MATH =', 170, 'w'), ('A PLANET', 196, 'y')], outline='#050b1f')


# ====================================================================== C  backward moon
def thumb_C():
    random.seed(21)
    NX, NY, NR = 1360, 590, 330
    OX, OY, RX, RY, ROT = NX, NY + 20, 760, 190, -10
    d = FILTERS
    d += lin('skyC', [(0, '#03061a'), (1, '#0a1338')])
    d += rad('triG', 0, 0, 1, [(0, '#000', 0)])
    d += rad('tri', -40, -40, 190, [(0, '#fff1e4', 1), (.35, '#e8c5b0', 1), (.75, '#b98a7a', 1), (1, '#4d3640', 1)])
    d += '<radialGradient id="triS" cx="0" cy="0" r="1"><stop offset="0" stop-color="#000" stop-opacity="0"/></radialGradient>'
    d += '<clipPath id="triC"><circle cx="0" cy="0" r="110"/></clipPath>'
    d += rad('sunC', 120, 160, 520, [(0, '#fff6dc', .5), (.2, '#ffd98a', .15), (1, '#000', 0)])
    nd, no = neptune(NX, NY, NR, 'nC')
    d += nd
    b = '<rect width="1920" height="1080" fill="url(#skyC)"/>'
    b += starfield(260, 0, 1920, 0, 1080, 5, .75)
    b += '<rect width="1920" height="1080" fill="url(#sunC)"/>'
    b += f'<circle cx="{NX - 60}" cy="{NY - 40}" r="{NR * 1.6:.0f}" fill="#2b5cff" opacity=".14" filter="url(#b50)"/>'

    def ell(t):
        x, y = RX * math.cos(t), RY * math.sin(t)
        a = math.radians(ROT)
        return OX + x * math.cos(a) - y * math.sin(a), OY + x * math.sin(a) + y * math.cos(a)

    # back half of Triton's orbit (behind the planet)
    back = [ell(math.pi + i * math.pi / 60) for i in range(61)]
    b += '<path d="M' + ' L'.join(f'{x:.0f} {y:.0f}' for x, y in back) + '" fill="none" stroke="#ff8a4c" stroke-width="5" opacity=".45" stroke-dasharray="18 14"/>'
    b += no
    # Neptune's spin: white arrows across the disc, all pointing right (prograde)
    for (yy, x0, x1) in ((-0.42, -.45, .35), (0.0, -.6, .5), (0.42, -.45, .35)):
        y0 = NY + yy * NR; xa, xb = NX + x0 * NR, NX + x1 * NR
        b += f'<path d="M{xa:.0f} {y0 + 14:.0f} Q{(xa + xb) / 2:.0f} {y0 + 40:.0f} {xb:.0f} {y0 + 10:.0f}" fill="none" stroke="#0a1a5c" stroke-width="22" stroke-linecap="round" opacity=".5"/>'
        b += f'<path d="M{xa:.0f} {y0 + 14:.0f} Q{(xa + xb) / 2:.0f} {y0 + 40:.0f} {xb:.0f} {y0 + 10:.0f}" fill="none" stroke="#ffffff" stroke-width="12" stroke-linecap="round" opacity=".92"/>'
        b += arrowhead(xb + 6, y0 + 8, -12, 42, '#ffffff')
    # front half of the orbit with orange arrows running the OTHER way (retrograde)
    front = [ell(i * math.pi / 60) for i in range(61)]
    pth = 'M' + ' L'.join(f'{x:.0f} {y:.0f}' for x, y in front)
    b += f'<path d="{pth}" fill="none" stroke="#ff7a3c" stroke-width="26" opacity=".35" filter="url(#b12)"/>'
    b += f'<path d="{pth}" fill="none" stroke="#ff9a52" stroke-width="9" stroke-linecap="round"/>'
    for t in (.12, .28, .42, .72, .86):
        x, y = ell(t * math.pi); x2, y2 = ell(t * math.pi + .05)
        b += arrowhead(x2, y2, math.degrees(math.atan2(y2 - y, x2 - x)), 40, '#ffa25c')
    # ---- Triton on the front of its orbit ----
    TX, TY = ell(.78 * math.pi)
    TX, TY = int(TX), int(TY)
    b += f'<circle cx="{TX}" cy="{TY}" r="230" fill="#ffb08a" opacity=".18" filter="url(#b24)"/>'
    tri = f'<g transform="translate({TX} {TY}) scale(1.35)">'
    tri += '<circle cx="0" cy="0" r="110" fill="url(#tri)" stroke="#2a1a24" stroke-width="5"/>'
    tri += '<g clip-path="url(#triC)">'
    random.seed(4)
    for _ in range(70):  # cantaloupe dimples
        x, y = random.uniform(-100, 100), random.uniform(-100, 100)
        tri += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{random.uniform(5, 11):.0f}" fill="none" stroke="#8a5f5a" stroke-width="2" opacity=".35"/>'
    tri += '<ellipse cx="-20" cy="60" rx="90" ry="40" fill="#f6ead8" opacity=".55"/>'
    tri += '<circle cx="50" cy="50" r="150" fill="none" stroke="#1a0f1c" stroke-width="120" opacity=".35"/>'
    tri += '</g>'
    # geyser plumes (dark dust) rising, bent by wind
    tri += '<path d="M-60 -78 q-10 -60 20 -120 q20 -30 10 -60" fill="none" stroke="#3a2a30" stroke-width="10" stroke-linecap="round" opacity=".65"/>'
    tri += '<path d="M-60 -78 q-10 -60 20 -120 q20 -30 10 -60" fill="none" stroke="#c8b4b0" stroke-width="3" stroke-linecap="round" opacity=".5"/>'
    tri += '</g>'
    b += tri
    # frog in a space helmet riding Triton, looking back over its shoulder at the arrows
    b += frog(TX + 30, TY - 128, 2.45, la='q-30 -6 -44 -30', ra='q20 6 24 30', mouth='o', look=(-4, -1), helmet=True, tilt=-6)
    # motion streaks behind Triton (it moves left along the front arc)
    for k, dy in enumerate((-60, -10, 40)):
        b += f'<path d="M{TX + 165} {TY + dy * 1.3:.0f} q60 {6 + k * 4} 150 {14 + k * 4}" fill="none" stroke="#ffd2b0" stroke-width="5" stroke-linecap="round" opacity=".5"/>'
    for _ in range(6):
        b += spark(random.randint(1000, 1880), random.randint(60, 300), random.choice([12, 16, 22]))
    return page('#03061a', svg(d, b), [('IT ORBITS', 150, 'w'), ('BACKWARD', 196, 'y')], outline='#03061a')


for n, fn in (('A', thumb_A), ('B', thumb_B), ('C', thumb_C)):
    open(os.path.join(HERE, f'{n}.html'), 'w').write(fn())
    print('wrote', n)
