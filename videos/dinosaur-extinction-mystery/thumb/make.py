# Thumbnails A-C for dinosaur-extinction-mystery (guideline 16-6 / 16-8, brief tools/briefs/thumb_art.md). Run: python3 videos/dinosaur-extinction-mystery/thumb/make.py
# A  IT RAINED / HOT GLASS     homage: Edvard Munch, "The Scream" (1893, public domain), mirrored: the frog screams on the bridge under a swirling
#                              burning sky full of glowing glass beads; fires on the hills, a sauropod on the far shore. Script: "tiny droplets of
#                              molten glass rained back down ... friction with the air made them glow", fires, "tiny glass beads in rocks".
# B  A CLUE / IN THE / CLAY    intuitive (+ detective nod): a cliff of strata cut by one thin glowing clay line; a T. rex skull fossil below it, nothing
#                              above; detective frog in a deerstalker holds a magnifier on the line (iridium sparkles). Script S03, S08-S14, S20.
# C  A / LIVING / DINOSAUR     intuitive: a sparrow on a branch in front of a sunlit wall, its shadow is a roaring T. rex; the frog on the branch
#                              stares at it. Script S04 / closing: "a living dinosaur from your window ... if a sparrow lands on a branch", birds =
#                              living branch of the feathered dinosaurs.
import os, sys, math, random
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', '..', 'tools'))
from thumb_lib import page, svg, lin, rad, spark

INK = '#1d2b1c'; GREEN = '#6aa55a'; DARKG = '#4d8a4a'; BELLY = '#9cc98a'
FILTERS = ''.join(f'<filter id="b{n}" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="{n}"/></filter>' for n in (2, 3, 6, 12, 24, 50))


def smooth(pts, closed=True, t=.5):
    """Catmull-Rom through pts -> cubic path"""
    n = len(pts); P_ = pts
    d = f'M{P_[0][0]:.1f},{P_[0][1]:.1f}'
    rng = range(n) if closed else range(n - 1)
    for i in rng:
        p0 = P_[(i - 1) % n] if closed or i > 0 else P_[0]
        p1 = P_[i]; p2 = P_[(i + 1) % n]
        p3 = P_[(i + 2) % n] if closed or i + 2 < n else P_[-1]
        c1 = (p1[0] + (p2[0] - p0[0]) * t / 3, p1[1] + (p2[1] - p0[1]) * t / 3)
        c2 = (p2[0] - (p3[0] - p1[0]) * t / 3, p2[1] - (p3[1] - p1[1]) * t / 3)
        d += f' C{c1[0]:.1f},{c1[1]:.1f} {c2[0]:.1f},{c2[1]:.1f} {p2[0]:.1f},{p2[1]:.1f}'
    return d + ('Z' if closed else '')


def tr(pts, x, y, s, flip=False):
    return [(x + (-a if flip else a) * s, y + b * s) for a, b in pts]


# ---------------- mascot frog (tools/assets/frog.svg body), posable (same as other videos) ----------------
def limb(d, w=7.5, wi=3.4):
    return f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="{w}"/><path d="{d}" fill="none" stroke="{GREEN}" stroke-width="{wi}"/>'


def end_of(d):
    n = [float(v) for v in d.replace('M', ' ').replace('q', ' ').split()]
    return n[0] + n[-2], n[1] + n[-1]


def frog(x, y, s, rot=0, flip=False, look=(0, 0), mouth='O', armL=None, armR=None, legs=None, brows=True, back="", front="", mid="", shadow=False):
    sx = -s if flip else s
    g = [f'<g transform="translate({x} {y}) rotate({rot}) scale({sx} {s})" stroke="{INK}" stroke-linejoin="round" stroke-linecap="round">', back]
    if shadow:
        g.append('<ellipse cx="0" cy="8" rx="50" ry="8" fill="#000" opacity=".25" stroke="none"/>')
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
        g.append('<ellipse cx="6" cy="-38" rx="10" ry="12" fill="#7a2f33" stroke-width="3"/><ellipse cx="6" cy="-31" rx="6" ry="4" fill="#e07b7b" stroke="none"/>')
    elif mouth == 'scream':
        g.append('<ellipse cx="6" cy="-34" rx="9" ry="16" fill="#7a2f33" stroke-width="3"/><ellipse cx="6" cy="-24" rx="5.5" ry="4.5" fill="#e07b7b" stroke="none"/>')
    else:
        g.append('<ellipse cx="6" cy="-41" rx="6" ry="7.5" fill="#7a2f33" stroke-width="3"/>')
    g.append('<ellipse cx="-18" cy="-48" rx="5" ry="3" fill="#e98a8a" stroke="none" opacity=".55"/><ellipse cx="30" cy="-48" rx="5" ry="3" fill="#e98a8a" stroke="none" opacity=".55"/>')
    g.append(mid)
    for a in (armL or 'M-34 -22 q-14 6 -16 22', armR or 'M38 -22 q14 6 16 22'):
        g.append(limb(a)); ex_, ey_ = end_of(a)
        g.append(f'<circle cx="{ex_:.1f}" cy="{ey_:.1f}" r="5.6" fill="{GREEN}" stroke-width="3"/>')
    g.append(front); g.append('</g>')
    return ''.join(g)


# the channel's own ghost costume (tools/frog.py OUTFITS['ghost'])
FROG_GHOST = '<path d="M-44 -96 q0 -46 50 -46 q50 0 50 46 v70 q-10 -8 -20 0 q-10 8 -20 0 q-10 8 -20 0 q-10 8 -20 0 q-10 8 -20 0z" fill="#f4f4f0" fill-opacity=".92" stroke-width="3.2"/><circle cx="-8" cy="-72" r="6" fill="#1d2b1c" stroke="none"/><circle cx="22" cy="-72" r="6" fill="#1d2b1c" stroke="none"/><ellipse cx="7" cy="-50" rx="6" ry="9" fill="#1d2b1c" stroke="none"/>'


def ghost_sheet(armL, armR):
    """white bed-sheet ghost costume for the frog (local frog coords): hood + floor-length scalloped hem, big face hole so the frog stays recognisable,
    green arms poking out of the sheet"""
    out = ('M-62 4 C-66 -40 -58 -112 6 -118 C70 -120 74 -36 70 4 '
           'q-8 12 -18 0 q-8 12 -18 0 q-8 12 -18 0 q-8 12 -18 0 q-8 12 -18 0 q-8 12 -18 0 Z')
    hole = 'M6 -104 a42 44 0 1 0 0.1 0 Z'
    g = (f'<path d="{out} {hole}" fill="#f4f1ea" fill-rule="evenodd" stroke="{INK}" stroke-width="4"/>'
         '<path d="M-52 -20 q4 14 2 24 M-30 -10 q2 10 0 16 M30 -8 q-2 10 0 16 M52 -22 q-4 14 -2 24" fill="none" stroke="#cfc8b8" stroke-width="3" opacity=".8"/>')
    for a in (armL, armR):
        g += limb(a); ex_, ey_ = end_of(a)
        g += f'<circle cx="{ex_:.1f}" cy="{ey_:.1f}" r="5.6" fill="{GREEN}" stroke-width="3"/>'
    return g


def frog_silhouette(x, y, s, col, op):
    return (f'<g transform="translate({x} {y}) scale({s})" fill="{col}" opacity="{op}">'
            '<path d="M-34 0 q-6 -64 34 -70 q40 -2 42 62 q0 10 -6 12 q-36 6 -70 -4z"/><circle cx="-10" cy="-66" r="15"/><circle cx="22" cy="-66" r="15"/>'
            '<ellipse cx="-22" cy="4" rx="17" ry="10"/><ellipse cx="22" cy="4" rx="17" ry="10"/>'
            '<path d="M-34 -22 q-18 -14 -20 -38 M38 -22 q18 -14 22 -38" fill="none" stroke="' + col + '" stroke-width="9" stroke-linecap="round"/></g>')


# =============================== A: The Scream homage, glowing glass rain ===============================
def make_A():
    rnd = random.Random(11)
    d = FILTERS
    d += rad('focA', 1380, 300, 900, [(0, '#fff6c8', 1), (.18, '#ffd65a', .9), (.45, '#ff7a1e', .55), (1, '#c2261a', 0)])
    d += lin('skyA', [(0, '#5a0f12'), (.35, '#b8301a'), (.62, '#ff8a2a'), (.78, '#ffc25a'), (1, '#7a2a14')])
    d += lin('fjordA', [(0, '#16233e'), (1, '#070b18')])
    d += lin('deckA', [(0, '#6a3a1e'), (1, '#24120a')])
    d += lin('railA', [(0, '#8a5530'), (1, '#3a1e0e')], x2=1, y2=0)
    d += rad('vigA', 1000, 480, 1250, [(0, '#000', 0), (.62, '#000', 0), (1, '#000', .6)])
    d += rad('frogGlow', 880, 860, 300, [(0, '#ffcf7a', .45), (1, '#ffcf7a', 0)])
    b = '<rect width="1920" height="1080" fill="url(#skyA)"/>'
    # --- swirling sky bands (Munch-like wavy ribbons) ---
    cols = ['#6e1414', '#9a2416', '#c43a18', '#e05a1c', '#f07e26', '#ffa23a', '#ffc45a', '#ffdc84', '#f39a34', '#d0501c']
    for i in range(26):
        y0 = -40 + i * 26; amp = 18 + 22 * math.sin(i * .7); ph = i * .9; c = cols[i % len(cols)]
        pts = []
        for k in range(0, 21):
            x = -100 + k * 106
            pts.append((x, y0 + amp * math.sin(k * .55 + ph) + 40 * math.sin(k * .18 + i * .3)))
        top = smooth(pts, closed=False)
        b += f'<path d="{top} L2020,{y0 + 140} L-100,{y0 + 140}Z" fill="{c}" opacity=".55"/>'
    # swirl strokes (brush-like)
    for i in range(60):
        y0 = rnd.uniform(20, 640); x0 = rnd.uniform(-100, 1800); L = rnd.uniform(220, 520)
        pts = [(x0 + L * t, y0 + 30 * math.sin(t * 4 + i) + 60 * t * math.sin(i)) for t in (0, .25, .5, .75, 1)]
        c = rnd.choice(['#ffe2a0', '#ff9a3a', '#c8341a', '#ffcf6a', '#7a1a14'])
        b += f'<path d="{smooth(pts, closed=False)}" fill="none" stroke="{c}" stroke-width="{rnd.uniform(4, 12):.1f}" stroke-linecap="round" opacity="{rnd.uniform(.25, .55):.2f}"/>'
    # focal glow (upper right) - the brightest part of the sky
    b += '<rect width="1920" height="1080" fill="url(#focA)"/>'
    # --- glowing glass beads streaking down (light source = friction glow) ---
    for i in range(95):
        x = rnd.uniform(640, 1900) if i < 70 else rnd.uniform(0, 1900); y = rnd.uniform(-20, 700)
        if x < 980 and y < 520: continue          # keep the text zone calmer
        L = rnd.uniform(60, 170); ang = math.radians(rnd.uniform(62, 72)); w = rnd.uniform(2.5, 5.5)
        x2, y2 = x - L * math.cos(ang), y - L * math.sin(ang)
        b += f'<line x1="{x2:.0f}" y1="{y2:.0f}" x2="{x:.0f}" y2="{y:.0f}" stroke="#ffb040" stroke-width="{w * 4:.1f}" stroke-linecap="round" opacity=".22" filter="url(#b6)"/>'
        b += f'<line x1="{x2:.0f}" y1="{y2:.0f}" x2="{x:.0f}" y2="{y:.0f}" stroke="#ffe7a8" stroke-width="{w:.1f}" stroke-linecap="round" opacity=".75"/>'
        b += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{w * 1.3:.1f}" fill="#fffbe6"/>'
    # --- far hills with fires (horizon y ~ 640-700) ---
    hills = smooth([(-60, 720), (200, 650), (420, 680), (640, 610), (900, 660), (1120, 600), (1380, 655), (1640, 610), (1980, 640), (1980, 760), (-60, 760)], closed=True, t=.4)
    b += f'<path d="{hills}" fill="#2a0d14"/>'
    for i in range(18):
        x = rnd.uniform(60, 1880); yb = 655 + 25 * math.sin(x / 140)
        h = rnd.uniform(26, 60)
        b += f'<ellipse cx="{x:.0f}" cy="{yb:.0f}" rx="{h * 1.6:.0f}" ry="{h:.0f}" fill="#ff6a1a" opacity=".45" filter="url(#b12)"/>'
        b += (f'<path d="M{x - h * .4:.0f},{yb + 6:.0f} q{h * .1:.0f},{-h * .7:.0f} {h * .3:.0f},{-h:.0f} q{h * .05:.0f},{h * .5:.0f} {h * .22:.0f},{h * .4:.0f} '
              f'q{h * .08:.0f},{-h * .35:.0f} {h * .2:.0f},{-h * .55:.0f} q{h * .2:.0f},{h * .6:.0f} {-h * .05:.0f},{h * 1.15:.0f}Z" fill="#ffd66a" opacity=".9"/>')
    # smoke from fires drifting into the sky
    for i in range(10):
        x = rnd.uniform(100, 1800)
        b += f'<ellipse cx="{x:.0f}" cy="{rnd.uniform(520, 600):.0f}" rx="{rnd.uniform(90, 180):.0f}" ry="{rnd.uniform(25, 45):.0f}" fill="#3a1414" opacity=".35" filter="url(#b24)"/>'
    # sauropod silhouette on the far shore, neck raised toward the sky
    sx, sy, ss = 1250, 648, 1.0
    sau = [(0, 0), (-20, -30), (-30, -60), (-26, -110), (-14, -150), (2, -168), (16, -166), (12, -156), (2, -150), (-6, -112), (6, -70), (40, -50), (90, -48), (130, -40), (180, -20), (240, 0), (180, -6), (130, -10), (126, 8), (110, 8), (108, -6), (60, -6), (56, 8), (40, 8), (36, -4), (10, -4), (8, 8), (-8, 8)]
    b += f'<path d="{smooth(tr(sau, sx, sy, ss), t=.3)}" fill="#1a0810"/>'
    # --- fjord (dark water swirling, left/middle) ---
    fj = smooth([(-60, 700), (300, 690), (700, 720), (980, 760), (1300, 745), (1700, 720), (1980, 730), (1980, 1080), (-60, 1080)], closed=True)
    b += f'<path d="{fj}" fill="url(#fjordA)"/>'
    for i in range(14):   # reflections of the burning sky
        y = 735 + i * 9; x0 = rnd.uniform(100, 1500); L = rnd.uniform(120, 360)
        b += f'<path d="M{x0:.0f},{y} q{L / 2:.0f},{rnd.uniform(-8, 8):.0f} {L:.0f},0" stroke="#ff9a3a" stroke-width="{rnd.uniform(2, 5):.1f}" fill="none" opacity="{rnd.uniform(.25, .6):.2f}"/>'
    # --- bridge deck + railing (mirrored Scream: runs from lower left to the right distance) ---
    b += '<path d="M-60,900 L1980,700 L1980,1080 L-60,1080Z" fill="url(#deckA)"/>'
    for i in range(16):   # deck planks
        t = i / 15.0
        x = -60 + t * 2040
        b += f'<line x1="{x:.0f}" y1="{900 - 200 * t:.0f}" x2="{x - 160 + 160 * t:.0f}" y2="1080" stroke="#1a0c06" stroke-width="3" opacity=".45"/>'
    # railing posts and bars (vanishing to the right)
    for i in range(14):
        t = (i / 13.0) ** 1.6
        x = -40 + t * 2000; ytop = 640 + (1 - t) * 0 ; yl = 905 - 205 * t
        top = 600 + 195 * (1 - t) * .0
        hgt = 300 * (1 - t) + 70 * t
        b += f'<rect x="{x - 9 * (1 - t) - 3:.0f}" y="{yl - hgt:.0f}" width="{18 * (1 - t) + 6:.0f}" height="{hgt:.0f}" fill="#2a140a"/>'
    b += '<path d="M-60,600 L1980,630 L1980,644 L-60,630Z" fill="url(#railA)" stroke="#1a0c06" stroke-width="3"/>'
    b += '<path d="M-60,760 L1980,675 L1980,684 L-60,780Z" fill="#4a2814" stroke="#1a0c06" stroke-width="2"/>'
    b += '<path d="M-60,601 L1980,631" stroke="#ffc46a" stroke-width="3" opacity=".7"/>'
    # --- frog in the Scream pose ---
    # small ghost-frog drifting in the meteor-shower sky (miya 2026-11-09)
    b += '<circle cx="1747" cy="421" r="80" fill="#fff1c8" opacity=".25" filter="url(#b12)"/>'
    b += frog(1747, 468, 0.85, rot=-10, look=(0, -5), mouth='scream',
              armL='M-32 -18 q-18 -8 -5 -31', armR='M38 -18 q18 -8 6 -31',
              legs=((-20, -6, -16, 12, 12), (20, -6, 16, 12, -12)),
              front=FROG_GHOST)
    # a few glowing beads very close (foreground depth)
    for x, y, L in ((1380, 330, 260), (1640, 470, 220), (1150, 180, 200)):
        ang = math.radians(66); x2, y2 = x - L * math.cos(ang), y - L * math.sin(ang)
        b += f'<line x1="{x2:.0f}" y1="{y2:.0f}" x2="{x}" y2="{y}" stroke="#ffcf6a" stroke-width="30" stroke-linecap="round" opacity=".3" filter="url(#b12)"/>'
        b += f'<line x1="{x2:.0f}" y1="{y2:.0f}" x2="{x}" y2="{y}" stroke="#fff3c8" stroke-width="8" stroke-linecap="round"/>'
        b += f'<circle cx="{x}" cy="{y}" r="13" fill="#fffef4"/><circle cx="{x}" cy="{y}" r="34" fill="#ffe08a" opacity=".45" filter="url(#b6)"/>'
    b += spark(1500, 250, 22) + spark(1760, 140, 16) + spark(1240, 420, 14)
    b += '<rect width="1920" height="1080" fill="url(#vigA)"/>'
    lines = [('IT RAINED', 150, 'w'), ('HOT', 150, 'w'), ('GLASS', 210, 'y')]
    return page('#3a0c0c', svg(d, b), lines, outline='#1a0505', top=40)


# =============================== B: a clue in the clay (cliff + magnifier) ===============================
SKULL = [(0, 62), (12, 44), (60, 30), (120, 22), (165, 22), (190, 16), (215, 22), (245, 32), (268, 48), (278, 72), (270, 100), (256, 122),
         (236, 132), (190, 134), (120, 128), (50, 118), (12, 108), (4, 96)]

LINE_Y = 590
CLIFF = [(1010, 300), (1200, 270), (1420, 285), (1640, 255), (1980, 270), (1980, 1080), (790, 1080), (800, 900), (830, 760), (860, 600), (930, 430)]


def strata(rnd, glow=True):
    """rock layers of the cliff face; the boundary clay line at LINE_Y"""
    o = ''
    lay = [(270, 360, '#a7a093'), (360, 450, '#b9b1a2'), (450, 520, '#9d978b'), (520, LINE_Y - 7, '#c3b9a6'),
           (LINE_Y + 7, 660, '#e3b8a2'), (660, 760, '#d9a48c'), (760, 860, '#e8c2ae'), (860, 960, '#cf9a84'), (960, 1080, '#e0b29c')]
    for y0, y1, c in lay:
        pts = [(780 + k * 100, y0 + 8 * math.sin(k * .8 + y0)) for k in range(14)]
        o += f'<path d="{smooth(pts, closed=False)} L2080,{y1} L780,{y1}Z" fill="{c}"/>'
        o += f'<path d="{smooth(pts, closed=False)}" fill="none" stroke="#5a4636" stroke-width="2.5" opacity=".35"/>'
    for i in range(220):   # grain / pebbles
        x = rnd.uniform(800, 1920); y = rnd.uniform(280, 1080)
        if abs(y - LINE_Y) < 12: continue
        o += f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{rnd.uniform(2, 7):.1f}" ry="{rnd.uniform(1.5, 4):.1f}" fill="{rnd.choice(["#6a5442", "#fff4e6", "#8a6a56"])}" opacity="{rnd.uniform(.15, .45):.2f}"/>'
    for i in range(16):    # cracks
        x = rnd.uniform(900, 1900); y = rnd.uniform(300, 1000)
        o += f'<path d="M{x:.0f},{y:.0f} l{rnd.uniform(-20, 20):.0f},{rnd.uniform(20, 50):.0f} l{rnd.uniform(-15, 15):.0f},{rnd.uniform(15, 40):.0f}" stroke="#4a3628" stroke-width="2" fill="none" opacity=".35"/>'
    # THE clay line: dark, a few centimetres thick, faint gold glow
    pts = [(780 + k * 100, LINE_Y + 5 * math.sin(k * .7)) for k in range(14)]
    path = smooth(pts, closed=False)
    if glow:
        o += f'<path d="{path}" fill="none" stroke="#ffd25a" stroke-width="56" opacity=".6" filter="url(#b12)"/>'
    o += f'<path d="{path}" fill="none" stroke="#3a2a2a" stroke-width="15"/>'
    o += f'<path d="{path}" fill="none" stroke="#6a4a3e" stroke-width="5" opacity=".8" transform="translate(0 -3)"/>'
    for i in range(70):
        x = rnd.uniform(820, 1920); y = LINE_Y + 5 * math.sin((x - 780) / 100 * .7) + rnd.uniform(-5, 5)
        o += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{rnd.choice([1.6, 2.2, 3])}" fill="#ffe9a0" opacity="{rnd.uniform(.5, 1):.2f}"/>'
    return o


def skull(x, y, s):
    o = f'<g transform="translate({x} {y}) scale({s})">'
    o += f'<path d="{smooth(SKULL, t=.35)}" fill="#f2e6c8" stroke="#5a4028" stroke-width="4"/>'
    o += f'<path d="{smooth(SKULL, t=.35)}" fill="none" stroke="#fffaf0" stroke-width="3" opacity=".7" transform="translate(-2 -3)" clip-path="url(#skc)"/>'
    o += '<path d="M40 112 Q140 128 250 116 L256 122 Q236 132 190 134 Q120 128 50 118Z" fill="#c9b48e" opacity=".8"/>'
    for cx, cy, rx, ry, a in ((125, 62, 32, 18, -6), (196, 48, 14, 15, 0), (237, 70, 17, 22, 8), (216, 116, 14, 6, 0), (24, 60, 8, 5, -10)):
        o += f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" transform="rotate({a} {cx} {cy})" fill="#4a3426" stroke="#5a4028" stroke-width="3"/>'
    o += '<path d="M6 94 Q70 98 140 104 Q200 108 252 104" fill="none" stroke="#5a4028" stroke-width="4"/>'
    for k in range(11):   # upper teeth
        tx = 16 + k * 15; ty = 94 + k * .9
        o += f'<path d="M{tx},{ty} l5,{14 - k * .4:.1f} l6,{-14 + k * .4:.1f}Z" fill="#fff8e4" stroke="#5a4028" stroke-width="2"/>'
    for k in range(9):    # lower teeth
        tx = 24 + k * 15; ty = 100 + k * 1
        o += f'<path d="M{tx},{ty} l5,-9 l5,9Z" fill="#efe2c2" stroke="#5a4028" stroke-width="1.8"/>'
    o += '<path d="M60 34 Q120 26 180 24" fill="none" stroke="#fffaf0" stroke-width="4" opacity=".8"/>'
    return o + '</g>'


def make_B():
    rnd = random.Random(5)
    d = FILTERS
    d += lin('skyB', [(0, '#7fb8dc'), (.55, '#cfe2e6'), (1, '#f6dcb0')])
    d += rad('sunB', 260, 140, 700, [(0, '#fff6d8', .9), (.3, '#ffe7a8', .4), (1, '#ffe7a8', 0)])
    d += rad('lensG', 965, 595, 240, [(0, '#fff2b0', .55), (1, '#fff2b0', 0)])
    d += rad('vigB', 1100, 560, 1250, [(0, '#000', 0), (.65, '#000', 0), (1, '#000', .45)])
    d += lin('cliffShade', [(0, '#000', ), (1, '#000')], x2=1, y2=0)
    d += f'<clipPath id="cliffc"><path d="{smooth(CLIFF, t=.25)}"/></clipPath>'
    d += f'<clipPath id="skc"><path d="{smooth(SKULL, t=.35)}"/></clipPath>'
    LX, LY, LR = 965, 595, 118
    d += f'<clipPath id="lensc"><circle cx="{LX}" cy="{LY}" r="{LR}"/></clipPath>'
    d += lin('brass', [(0, '#fff0b0'), (.4, '#d9a840'), (1, '#7a5418')])
    d += lin('groundB', [(0, '#8a7a58'), (1, '#4a3e2a')])
    b = '<rect width="1920" height="1080" fill="url(#skyB)"/><rect width="1920" height="1080" fill="url(#sunB)"/>'
    # distant hills (Italian countryside) and soft clouds
    b += f'<path d="{smooth([(-60, 640), (200, 560), (420, 600), (640, 540), (900, 590), (900, 1080), (-60, 1080)], t=.4)}" fill="#8fa98a" opacity=".7"/>'
    b += f'<path d="{smooth([(-60, 720), (260, 650), (520, 690), (900, 650), (900, 1080), (-60, 1080)], t=.4)}" fill="#6f8f62"/>'
    for cx, cy, w in ((560, 200, 220), (1500, 130, 260), (1180, 200, 160)):
        b += f'<ellipse cx="{cx}" cy="{cy}" rx="{w}" ry="{w * .22:.0f}" fill="#fff" opacity=".6" filter="url(#b12)"/>'
    # a faint streak in the sky: the visitor from space (top right)
    b += '<line x1="1560" y1="40" x2="1760" y2="150" stroke="#fff3c8" stroke-width="14" stroke-linecap="round" opacity=".4" filter="url(#b6)"/>'
    b += '<line x1="1600" y1="62" x2="1760" y2="150" stroke="#fffaf0" stroke-width="4" stroke-linecap="round" opacity=".9"/><circle cx="1762" cy="151" r="7" fill="#fff"/>'
    # cliff
    b += f'<path d="{smooth(CLIFF, t=.25)}" fill="#c9b9a2"/>'
    b += f'<g clip-path="url(#cliffc)">{strata(random.Random(9))}'
    # T. rex skull fossil below the line, a few vertebrae
    b += skull(1110, 650, 1.62)
    for k in range(5):
        vx = 1600 + k * 46; vy = 760 + k * 10
        b += f'<g transform="rotate({8 + k * 3} {vx} {vy})"><rect x="{vx - 17}" y="{vy - 14}" width="34" height="28" rx="9" fill="#efe0bf" stroke="#5a4028" stroke-width="3"/><path d="M{vx - 6} {vy - 12} L{vx - 2} {vy - 34} L{vx + 6} {vy - 34} L{vx + 6} {vy - 12}Z" fill="#efe0bf" stroke="#5a4028" stroke-width="2.5"/></g>'
    b += '<path d="M1580 860 q60 -40 150 -20" fill="none" stroke="#5a4028" stroke-width="14" stroke-linecap="round"/><path d="M1580 860 q60 -40 150 -20" fill="none" stroke="#efe0bf" stroke-width="8" stroke-linecap="round"/>'
    # light from the upper left on the cliff, shade to the right
    b += '<rect x="780" y="250" width="1200" height="830" fill="#2a1a10" opacity=".0"/>'
    b += f'<path d="M1600,250 L1980,250 L1980,1080 L1450,1080Z" fill="#3a2414" opacity=".18" filter="url(#b50)"/>'
    b += '</g>'
    # cliff top grass and rim light on its left edge
    b += f'<path d="{smooth(CLIFF[:5], closed=False, t=.25)}" fill="none" stroke="#4f7a3a" stroke-width="22" stroke-linecap="round"/>'
    for i in range(70):
        x = rnd.uniform(1010, 1960); y = 300 - 30 * ((x - 1010) / 950) + 10 * math.sin(x / 90) - 16
        b += f'<path d="M{x:.0f},{y + 14:.0f} q{rnd.uniform(-6, 6):.0f},-14 {rnd.uniform(-8, 8):.0f},-{rnd.uniform(16, 30):.0f}" stroke="#5f9a46" stroke-width="4" fill="none"/>'
    b += f'<path d="{smooth(CLIFF[6:] + [CLIFF[0]], closed=False, t=.25)}" fill="none" stroke="#fff3d6" stroke-width="6" opacity=".7"/>'
    # ground and boulder at the foot of the cliff
    b += f'<path d="{smooth([(-60, 940), (400, 905), (800, 920), (1200, 960), (1980, 970), (1980, 1080), (-60, 1080)], t=.4)}" fill="url(#groundB)"/>'
    b += f'<path d="{smooth([(500, 960), (520, 910), (600, 885), (720, 880), (800, 900), (820, 950), (780, 985), (560, 990)], t=.4)}" fill="#8f8574" stroke="#4a4034" stroke-width="4"/>'
    b += '<path d="M540 925 q60 -34 160 -34" stroke="#d6cdbb" stroke-width="5" fill="none" opacity=".8"/>'
    for i in range(30):
        x = rnd.uniform(0, 1900); y = rnd.uniform(960, 1070)
        b += f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{rnd.uniform(6, 16):.0f}" ry="{rnd.uniform(3, 7):.0f}" fill="#3a3022" opacity=".5"/>'
    # --- magnifier: glow, magnified copy of the cliff, rim ---
    b += f'<circle cx="{LX}" cy="{LY}" r="240" fill="url(#lensG)"/>'
    mag = 2.0
    b += (f'<g clip-path="url(#lensc)"><rect x="{LX - LR}" y="{LY - LR}" width="{2 * LR}" height="{2 * LR}" fill="#c9b9a2"/>'
          f'<g transform="translate({LX} {LY}) scale({mag}) translate({-LX} {-LY})">{strata(random.Random(9), glow=True)}</g>')
    rr = random.Random(3)
    for i in range(16):
        x = LX + rr.uniform(-LR, LR); y = LY + rr.uniform(-8, 8)
        b += spark(round(x), round(y), rr.choice([7, 9, 12]), col='#fff6c0', op=.95)
    b += f'<ellipse cx="{LX - 40}" cy="{LY - 55}" rx="60" ry="26" fill="#fff" opacity=".35" transform="rotate(-30 {LX - 40} {LY - 55})"/></g>'
    b += f'<circle cx="{LX}" cy="{LY}" r="{LR + 9}" fill="none" stroke="#3a2a10" stroke-width="26"/><circle cx="{LX}" cy="{LY}" r="{LR + 9}" fill="none" stroke="url(#brass)" stroke-width="16"/>'
    b += f'<circle cx="{LX}" cy="{LY}" r="{LR + 3}" fill="none" stroke="#fff6d0" stroke-width="2.5" opacity=".7"/>'
    # handle from the rim down-left to the frog's hand
    fx, fy, fs = 660, 905, 3.1
    hx, hy = fx + 70 * fs, fy - 66 * fs
    ang = math.atan2(hy - LY, hx - LX); rx0, ry0 = LX + (LR + 20) * math.cos(ang), LY + (LR + 20) * math.sin(ang)
    b += f'<line x1="{rx0:.0f}" y1="{ry0:.0f}" x2="{hx + 14 * math.cos(ang):.0f}" y2="{hy + 14 * math.sin(ang):.0f}" stroke="#2a1608" stroke-width="30" stroke-linecap="round"/>'
    b += f'<line x1="{rx0:.0f}" y1="{ry0:.0f}" x2="{hx + 14 * math.cos(ang):.0f}" y2="{hy + 14 * math.sin(ang):.0f}" stroke="#7a3e1a" stroke-width="20" stroke-linecap="round"/>'
    b += f'<line x1="{rx0:.0f}" y1="{ry0:.0f}" x2="{(rx0 + hx) / 2:.0f}" y2="{(ry0 + hy) / 2:.0f}" stroke="#c87a3a" stroke-width="5" stroke-linecap="round" opacity=".8"/>'
    # --- detective frog (deerstalker + cape) on the boulder ---
    hat = ('<g transform="translate(6 -98)">'
           '<path d="M-38 6 Q-34 -26 0 -28 Q34 -26 38 6 Z" fill="#b08a5a" stroke-width="3.4"/>'
           '<path d="M-30 -8 L30 -8 M-34 0 L34 0 M-22 -22 L-22 6 M-8 -27 L-8 6 M8 -27 L8 6 M22 -22 L22 6" stroke="#6a4a2a" stroke-width="2" fill="none" opacity=".8"/>'
           '<path d="M34 2 q26 -2 36 12 q-20 4 -38 -2z" fill="#9a764a" stroke-width="3"/>'
           '<path d="M-34 2 q-26 -2 -36 12 q20 4 38 -2z" fill="#9a764a" stroke-width="3"/>'
           '<path d="M-6 -28 q6 -8 12 0" fill="none" stroke-width="3"/><circle cx="0" cy="-30" r="3.5" fill="#6a4a2a" stroke-width="2"/></g>')
    cape = ('<path d="M-36 -26 Q-58 -6 -46 6 L50 6 Q62 -6 40 -26 Q4 -16 -36 -26Z" fill="#9a764a" stroke-width="3.4"/>'
            '<path d="M-40 -14 L44 -14" stroke="#6a4a2a" stroke-width="2" opacity=".8"/><path d="M-44 -2 L48 -2" stroke="#6a4a2a" stroke-width="2" opacity=".8"/>'
            '<path d="M-12 -26 L4 -14 L18 -26" fill="#7a5a36" stroke-width="2.6"/>')
    b += f'<ellipse cx="{fx}" cy="{fy + 6}" rx="130" ry="14" fill="#000" opacity=".25" filter="url(#b6)"/>'
    b += frog(fx, fy, fs, rot=4, look=(4, -3), mouth='O', mid=cape, front=hat,
              armR='M38 -24 q26 -6 32 -42', armL='M-34 -22 q-18 4 -18 22',
              legs=((-20, -6, -24, 4, -4), (20, -6, 26, 4, 4)))
    b += '<rect width="1920" height="1080" fill="url(#vigB)"/>'
    lines = [('A CLUE', 160, 'w'), ('IN THE', 120, 'w'), ('CLAY', 230, 'y')]
    return page('#7fb8dc', svg(d, b), lines, outline='#0e1a24', top=36)


# =============================== C: sparrow with a T. rex shadow ===============================
TREX = [(0, 38), (14, 28), (40, 22), (60, 19), (70, 15), (80, 19), (92, 28), (112, 44), (140, 50), (175, 46), (205, 48), (245, 56), (300, 72), (302, 76),
        (245, 70), (215, 74), (208, 86), (203, 108), (198, 140), (214, 151), (218, 156), (186, 156), (184, 148), (186, 138), (180, 112), (170, 100),
        (152, 100), (148, 126), (146, 148), (160, 152), (162, 157), (128, 157), (130, 148), (132, 126), (126, 104), (114, 94), (112, 98), (118, 104),
        (113, 107), (104, 96), (96, 84), (88, 70), (72, 64), (44, 62), (14, 61), (6, 56), (40, 51), (62, 47), (60, 42), (30, 44), (4, 44)]


def trex_path(x, y, s):
    """polygon with smoothed long runs; sharp points kept at the jaws/toes"""
    pts = tr(TREX, x, y, s)
    return 'M' + ' L'.join(f'{a:.1f},{b:.1f}' for a, b in pts) + 'Z'


def sparrow(x, y, s):
    """house sparrow facing left, perched; feet at (x, y)"""
    o = f'<g transform="translate({x} {y}) scale({s})" stroke="#2a1a10" stroke-linejoin="round" stroke-linecap="round">'
    # tail
    o += '<path d="M36 -44 L128 -8 Q134 4 124 14 L110 22 L28 -18Z" fill="#6a4428" stroke-width="3"/>'
    o += '<path d="M44 -34 L126 0 M40 -26 L118 14" stroke="#3a2414" stroke-width="2" fill="none"/>'
    # body
    o += '<path d="M-58 -70 Q-70 -30 -40 -8 Q-10 8 30 -6 Q66 -22 60 -56 Q50 -90 0 -92 Q-40 -92 -58 -70Z" fill="#c9b8a0" stroke-width="3.4"/>'
    o += '<path d="M-56 -50 Q-50 -16 -16 -6 Q12 0 30 -10 Q-10 -12 -30 -30 Q-46 -44 -56 -50Z" fill="#e6dccb" stroke="none"/>'
    # wing
    o += '<path d="M-20 -78 Q30 -92 70 -60 Q86 -40 74 -24 Q30 -14 -6 -36 Q-24 -52 -20 -78Z" fill="#8a5a32" stroke-width="3.2"/>'
    for k in range(5):
        o += f'<path d="M{-4 + k * 15} {-74 + k * 3} q10 18 26 {28 - k * 2}" fill="none" stroke="#2a1608" stroke-width="5"/>'
        o += f'<path d="M{2 + k * 15} {-76 + k * 3} q10 16 24 {24 - k * 2}" fill="none" stroke="#c8925a" stroke-width="3"/>'
    o += '<path d="M-6 -50 Q30 -44 60 -38" fill="none" stroke="#fff6e8" stroke-width="5"/>'
    o += '<path d="M30 -30 L86 -22 L78 -14 L24 -20Z" fill="#4a2e18" stroke-width="2.6"/>'
    # head
    o += '<circle cx="-62" cy="-100" r="40" fill="#b0a898" stroke-width="3.4"/>'
    o += '<path d="M-96 -118 Q-80 -146 -46 -138 Q-24 -128 -24 -104 Q-40 -116 -62 -120 Q-82 -122 -96 -118Z" fill="#8a8478" stroke="none"/>'
    o += '<path d="M-44 -132 Q-18 -118 -24 -88 Q-30 -76 -40 -80 Q-36 -104 -50 -118Z" fill="#8a4a22" stroke="none"/>'   # chestnut nape
    o += '<path d="M-98 -96 Q-90 -76 -68 -72 Q-56 -72 -50 -84 Q-70 -84 -84 -96Z" fill="#f3efe6" stroke="none"/>'          # pale cheek
    o += '<path d="M-100 -88 Q-96 -62 -78 -56 Q-70 -66 -76 -80 Q-90 -82 -100 -88Z" fill="#1e1612" stroke="none"/>'        # black bib
    o += '<circle cx="-62" cy="-100" r="40" fill="none" stroke-width="3.4"/>'
    o += '<path d="M-102 -98 L-128 -92 L-104 -84Z" fill="#3a3028" stroke-width="2.6"/><path d="M-104 -94 L-124 -92" stroke="#7a6a5a" stroke-width="1.5"/>'
    o += '<circle cx="-80" cy="-106" r="7.5" fill="#120c08" stroke="none"/><circle cx="-82" cy="-108.5" r="2.6" fill="#fff" stroke="none"/>'
    o += '<path d="M-96 -112 Q-82 -116 -66 -112" fill="none" stroke="#8a4a22" stroke-width="3" opacity=".8"/>'
    # rim light from the left (the sun)
    o += '<path d="M-100 -118 Q-92 -140 -62 -141" fill="none" stroke="#fff3c4" stroke-width="5" opacity=".9"/>'
    o += '<path d="M-58 -70 Q-70 -30 -40 -8" fill="none" stroke="#fff3c4" stroke-width="4" opacity=".7"/>'
    # legs gripping the branch
    o += '<path d="M-24 -6 L-28 6 M10 -6 L12 6" stroke="#b98a6a" stroke-width="5"/>'
    o += '<path d="M-38 8 q10 -6 22 0 M0 8 q10 -6 22 0" stroke="#b98a6a" stroke-width="4" fill="none"/>'
    return o + '</g>'


def make_C():
    rnd = random.Random(21)
    d = FILTERS
    d += lin('wallC', [(0, '#ffe2b8'), (.5, '#f3c792'), (1, '#d79a6a')], x2=1, y2=.45)
    d += rad('sunC', 120, 300, 1300, [(0, '#fff6dc', .85), (.35, '#ffe0a8', .35), (1, '#ffe0a8', 0)])
    d += rad('vigC', 1000, 520, 1250, [(0, '#000', 0), (.6, '#000', 0), (1, '#3a1a08', .55)])
    d += rad('birdGlow', 1060, 650, 300, [(0, '#fff3c0', .7), (1, '#fff3c0', 0)])
    d += lin('branchC', [(0, '#7a4e2e'), (1, '#3e2414')], x2=0, y2=1)
    SH = '#6a3e2a'
    b = '<rect width="1920" height="1080" fill="url(#wallC)"/>'
    # stucco texture + brick hints
    for i in range(380):
        b += f'<circle cx="{rnd.uniform(0, 1920):.0f}" cy="{rnd.uniform(0, 1080):.0f}" r="{rnd.uniform(1, 3.5):.1f}" fill="{rnd.choice(["#fff4e0", "#b8784a"])}" opacity="{rnd.uniform(.1, .3):.2f}"/>'
    for y in range(120, 1080, 140):
        b += f'<path d="M0 {y} L1920 {y}" stroke="#c48a5a" stroke-width="3" opacity=".18"/>'
    b += '<rect width="1920" height="1080" fill="url(#sunC)"/>'
    # window frame edge on the far left (we are looking out of / along the house)
    # ---- shadows on the wall (sun low on the left -> shadows cast up and to the right) ----
    TX, TY, TS = 1060, 250, 2.45
    b += f'<g filter="url(#b3)" opacity=".86">'
    b += f'<path d="M560,742 Q1100,690 1980,610" stroke="{SH}" stroke-width="30" fill="none" stroke-linecap="round"/>'
    b += f'<path d="M1300,668 q60 -50 130 -70 M820,718 q40 -60 30 -110" stroke="{SH}" stroke-width="12" fill="none" stroke-linecap="round"/>'
    b += f'<path d="{trex_path(TX, TY, TS)}" fill="{SH}" stroke="{SH}" stroke-width="10" stroke-linejoin="round"/>'
    for k in range(6):  # teeth in the open jaws of the shadow
        tx = TX + (12 + k * 8) * TS; ty = TY + 44 * TS
        b += f'<path d="M{tx:.0f},{ty:.0f} l{4 * TS:.0f},{5 * TS:.0f} l{4 * TS:.0f},{-5 * TS:.0f}Z" fill="{SH}"/>'
    b += '</g>'
    # ---- the real branch (foreground) with leaves ----
    br = 'M-40,890 Q300,850 620,830 Q900,808 1240,760 Q1300,752 1330,742'
    b += f'<path d="{br}" stroke="#2a160a" stroke-width="44" fill="none" stroke-linecap="round"/>'
    b += f'<path d="{br}" stroke="url(#branchC)" stroke-width="34" fill="none" stroke-linecap="round"/>'
    b += f'<path d="M-40,880 Q300,840 620,820 Q900,798 1240,750" stroke="#c89060" stroke-width="6" fill="none" opacity=".7"/>'
    b += '<path d="M760,818 q40 -60 30 -120" stroke="#3e2414" stroke-width="12" fill="none" stroke-linecap="round"/>'
    b += '<path d="M1150,772 q60 -50 130 -70" stroke="#3e2414" stroke-width="12" fill="none" stroke-linecap="round"/>'
    for i in range(10):
        b += f'<path d="M{rnd.uniform(0, 1200):.0f},{rnd.uniform(830, 880):.0f} q8 2 14 -2" stroke="#2a160a" stroke-width="3" fill="none" opacity=".6"/>'
    for (lx, ly, a, s) in ((790, 700, -30, 1.1), (770, 730, 200, .9), (1280, 700, -10, 1.0), (1240, 712, 150, .8), (420, 845, 120, .9), (560, 830, -60, .8), (180, 870, 140, .9)):
        b += (f'<g transform="translate({lx} {ly}) rotate({a}) scale({s})"><path d="M0 0 Q30 -26 70 0 Q30 26 0 0Z" fill="#7dbb4a" stroke="#2f5a1e" stroke-width="3"/>'
              f'<path d="M4 0 L64 0" stroke="#2f5a1e" stroke-width="2"/><path d="M6 -4 Q30 -18 60 -4" stroke="#d8f0a0" stroke-width="2.5" fill="none" opacity=".8"/></g>')
    # ---- sparrow (the living dinosaur), glow behind it ----
    b += '<rect width="1920" height="1080" fill="url(#birdGlow)"/>'
    b += sparrow(1080, 770, 1.55)
    b += spark(980, 520, 18) + spark(1190, 560, 12) + spark(1500, 200, 16)
    # ---- frog on the branch, startled, staring at the shadow ----
    b += frog(640, 832, 2.6, rot=-6, look=(4, -4), mouth='O',
              armL='M-34 -22 q-20 -12 -22 -38', armR='M38 -22 q20 -12 24 -38',
              legs=((-20, -6, -24, 4, -4), (20, -6, 24, 4, 4)))
    b += '<rect width="1920" height="1080" fill="url(#vigC)"/>'
    lines = [('A', 120, 'w'), ('LIVING', 200, 'y'), ('DINOSAUR', 170, 'w')]
    return page('#f3c792', svg(d, b), lines, outline='#2a1408', top=40)


if __name__ == '__main__':
    which = sys.argv[1:] or ['A', 'B', 'C']
    for n in which:
        open(os.path.join(HERE, f'{n}.html'), 'w').write(globals()[f'make_{n}']())
    print('ok')
