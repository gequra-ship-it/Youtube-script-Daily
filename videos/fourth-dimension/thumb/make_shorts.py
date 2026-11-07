# Shorts thumbnails for fourth-dimension-short1..5 (guideline 16-9, corrected 2026-11-06: VERTICAL 1080x1920, text centred, frog, no edge-glued items).
# Run: python3 videos/fourth-dimension/thumb/make_shorts.py  -> videos/fourth-dimension-shortN/thumb/A.html (+ tools/assets/thumb_v/ css + font)
# then: for N in 1 2 3 4 5; do SLUG=fourth-dimension-shortN python3 tools/thumb_shot.py; done
# 1 A 4D SHADOW?          short1 S05-S07: "the shadow of a four-dimensional object is a ... three-dimensional solid" / "smaller cube ... inside a larger cube"
#                         lamp-lit tesseract shadow (cube in cube + 8 struts) on a violet stage; frog usher with a flashlight
# 2 THEY SEE A CIRCLE     short2 S05-S08: an apple pushed through a paper world; flat shapes see only a circle; frog with magnifier on the paper
# 3 HUNDREDS OF FLAT SLICES  short3 S03-S06: scanner builds its picture from a stack of thin 2D cross-sections (often hundreds); slices stack into a head;
#                         frog in blue scrubs holding one slice (a slicing trick, no claim of a 4D machine)
# 4 STACK EVERY PHOTO     short4 S04-S07: stack every photograph of you -> a solid track, the worldline (relativity view); frog photographer
# 5 BUILT FOR 3D ONLY     short5 S05-S09: brains shaped for a 3D world on the savannah; a hypercube short-circuits a brain; frog in safari hat in the grass
import os, sys, math, random, shutil
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
sys.path.insert(0, os.path.join(REPO, 'tools'))
from thumb_lib import vpage, vsvg, lin, rad, spark
src = open(os.path.join(HERE, 'make.py')).read()
exec(src[src.index('INK = '):src.index('# ================= A:')])   # frog, tess_screen, tess_draw, hull, starfield, jag, bil, P, FILTERS
W, H = 1080, 1920


def ring_glow(cx, cy, r, col, op=.2):
    return f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{col}" opacity="{op}" filter="url(#b50)"/>'


def vig(id_, col='#000', op=.7):
    return rad(id_, 540, 960, 1150, [(0, col, 0), (.6, col, 0), (1, col, op)])


def sparks_ring(rnd, cx, cy, r0, r1, n, col, skip=None):
    o = ''
    for _ in range(n):
        a = rnd.uniform(0, 6.28); r = rnd.uniform(r0, r1)
        x, y = cx + r * math.cos(a), cy + r * math.sin(a) * .85
        if skip and skip(x, y): continue
        o += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{rnd.uniform(2, 4.5):.1f}" fill="{col}" opacity="{rnd.uniform(.3, .85):.2f}"/>'
    return o


# ================= 1: A 4D SHADOW? (subject above the text) =================
def make_1():
    rnd = random.Random(11)
    d = FILTERS + lin('wall1', [(0, '#1a0f3a'), (.5, '#2c1658'), (1, '#160a2c')])
    d += lin('floor1', [(0, '#2a145a'), (1, '#07030f')])
    d += '<linearGradient id="cone1" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ffe7a8" stop-opacity=".55"/><stop offset="1" stop-color="#ffcf70" stop-opacity="0"/></linearGradient>'
    d += '<linearGradient id="beam1" x1="0" y1="1" x2="1" y2="0"><stop offset="0" stop-color="#fff2c0" stop-opacity=".8"/><stop offset="1" stop-color="#ffd27a" stop-opacity="0"/></linearGradient>'
    d += vig('vig1', '#000', .75)
    b = '<rect width="1080" height="1920" fill="url(#wall1)"/>'
    for k in range(0, 1080, 90):
        b += f'<path d="M{k} 0 Q{k + 45} 700 {k + 10} 1300 L{k + 60} 1300 Q{k + 90} 700 {k + 50} 0Z" fill="#3a1e6e" opacity=".35"/>'
    b += '<rect y="1290" width="1080" height="630" fill="url(#floor1)"/>'
    for k in range(-10, 11):
        b += f'<line x1="{540 + k * 80}" y1="1290" x2="{540 + k * 260}" y2="1920" stroke="#8a5ad8" stroke-width="2" opacity=".2"/>'
    for yy in (1320, 1380, 1470, 1600, 1780):
        b += f'<line x1="0" y1="{yy}" x2="1080" y2="{yy}" stroke="#8a5ad8" stroke-width="2" opacity=".15"/>'
    # hanging lamp + long cone of light down to the floor
    cx, cy = 540, 560
    b += '<path d="M400 220 L680 220 L1040 1460 L40 1460Z" fill="url(#cone1)"/>'
    b += '<line x1="540" y1="120" x2="540" y2="190" stroke="#0a0614" stroke-width="8"/>'
    b += '<path d="M460 230 Q540 170 620 230 L640 244 L440 244Z" fill="#3a3550" stroke="#0a0614" stroke-width="5"/>'
    b += '<ellipse cx="540" cy="244" rx="100" ry="14" fill="#fff6d6"/>' + ring_glow(540, 250, 140, '#ffe9a8', .55)
    # the 3D shadow of a tesseract: cube inside cube, 8 struts; smoky faces + bright edges
    sp, ed = tess_screen(0.0, 0.62, -0.42, cx, cy, 250, d4=3.0)
    outer = [(p[0], p[1]) for i, p in enumerate(sp) if i & 1]
    inner = [(p[0], p[1]) for i, p in enumerate(sp) if not i & 1]
    b += ring_glow(cx, cy, 330, '#b07aff', .4)
    b += f'<polygon points="{P(hull(outer))}" fill="#120626" opacity=".72"/>'
    b += f'<polygon points="{P(hull(inner))}" fill="#3a1670" opacity=".75"/>'
    b += ring_glow(cx, cy, 100, '#ffe08a', .55)
    b += tess_draw(sp, ed, '#ffd77a', '#c89aff', '#ff8ad8', w=8, gcol='#a070ff', core='#fff8e8')
    b += spark(cx + 330, cy - 230, 26) + spark(cx - 360, cy + 180, 18, '#f0e0ff') + spark(940, 1330, 16, '#fff6d6', .7)
    b += sparks_ring(rnd, cx, cy, 290, 420, 40, '#f0e0ff')
    # its shadow pool on the stage floor
    b += '<ellipse cx="560" cy="1420" rx="330" ry="50" fill="#05020c" opacity=".7" filter="url(#b12)"/>'
    b += f'<polygon points="{P([(560 + (x - cx) * 1.1, 1420 + (y - cy) * .16) for x, y in hull(outer)])}" fill="#05020c" opacity=".55"/>'
    # frog usher with a flashlight (lower left), beam up the right side
    vest = ('<path d="M-37 -2 Q-40 -30 -28 -44 Q6 -30 44 -44 Q50 -30 44 -2 Q6 6 -37 -2Z" fill="#7a2a8a" stroke-width="3.2"/>'
            '<circle cx="6" cy="-26" r="3.5" fill="#f2d27a" stroke="none"/><circle cx="6" cy="-14" r="3.5" fill="#f2d27a" stroke="none"/>')
    torch = ('<g transform="translate(62 -78) rotate(50)"><rect x="-9" y="-6" width="18" height="44" rx="5" fill="#3a3a48" stroke-width="3"/>'
             '<path d="M-14 -6 L14 -6 L18 -22 L-18 -22Z" fill="#c8c8d8" stroke-width="3"/><ellipse cx="0" cy="-22" rx="18" ry="5" fill="#fff6c8" stroke-width="2.5"/></g>')
    b += '<path d="M557 1364 L946 894 L1088 1062 Z" fill="url(#beam1)" opacity=".7"/><ellipse cx="557" cy="1364" rx="34" ry="34" fill="#fff6c8" opacity=".6" filter="url(#b12)"/>'
    b += '<ellipse cx="320" cy="1640" rx="150" ry="22" fill="#000" opacity=".5" filter="url(#b6)"/>'
    b += frog(320, 1640, 3.0, look=(9, -5), mouth='O', mid=vest, front=torch,
              armL='M-34 -22 q-20 4 -24 26', armR='M38 -22 q20 -14 26 -44',
              legs=((-20, -6, -24, 4, -6), (20, -6, 24, 4, 6)))
    b += '<rect width="1080" height="1920" fill="url(#vig1)"/>'
    lines = [('A 4D', 200, 'w'), ('<span class="g">SHADOW?</span>', 190, 'w')]
    return vpage('#1a0f3a', vsvg(d, b), lines, outline='#0a0418', top=870)


# ================= 2: THEY SEE A CIRCLE (subject below the text) =================
def make_2():
    rnd = random.Random(22)
    d = FILTERS + lin('sky2', [(0, '#3a98c8'), (.45, '#7cc4e0'), (1, '#e8f4ee')])
    d += lin('paper2', [(0, '#fff8e6'), (1, '#f0dfb8')], x2=1, y2=1)
    d += '<radialGradient id="apple2" cx=".36" cy=".32" r=".8"><stop offset="0" stop-color="#ff8a7a"/><stop offset=".35" stop-color="#e8322e"/><stop offset=".8" stop-color="#a8141e"/><stop offset="1" stop-color="#6a0a12"/></radialGradient>'
    d += rad('sun2', 820, 330, 420, [(0, '#fffbe0', .95), (.3, '#fff0b0', .5), (1, '#fff0b0', 0)])
    d += vig('vig2', '#103040', .45)
    b = '<rect width="1080" height="1920" fill="url(#sky2)"/><rect width="1080" height="1920" fill="url(#sun2)"/>'
    b += '<circle cx="820" cy="330" r="80" fill="#fff8d0"/>'
    for x, y, s in ((220, 300, 1.1), (900, 560, .8), (140, 1180, .9), (960, 1060, .7)):
        b += (f'<g transform="translate({x} {y}) scale({s})" fill="#ffffff" opacity=".8"><ellipse cx="0" cy="0" rx="120" ry="40"/>'
              f'<circle cx="-40" cy="-20" r="46"/><circle cx="30" cy="-34" r="56"/><circle cx="80" cy="-6" r="36"/></g>')
    # the paper world (a flat sheet in perspective) in the lower half
    Q = [(170, 1340), (1010, 1360), (1050, 1720), (40, 1700)]   # far-left, far-right, near-right, near-left
    b += f'<polygon points="{P([(x + 10, y + 50) for x, y in Q])}" fill="#2a5a6a" opacity=".35" filter="url(#b12)"/>'
    b += f'<polygon points="{P([Q[3], Q[2], (Q[2][0], Q[2][1] + 16), (Q[3][0], Q[3][1] + 16)])}" fill="#c8b48a" stroke="#5a4a2a" stroke-width="4"/>'
    b += f'<polygon points="{P(Q)}" fill="url(#paper2)" stroke="#5a4a2a" stroke-width="5" stroke-linejoin="round"/>'
    for k in range(1, 9):
        a, c = bil(Q, 0, k / 9), bil(Q, 1, k / 9)
        b += f'<line x1="{a[0]:.0f}" y1="{a[1]:.0f}" x2="{c[0]:.0f}" y2="{c[1]:.0f}" stroke="#8ab8d8" stroke-width="2.4" opacity=".55"/>'
    a, c = bil(Q, .08, 0), bil(Q, .08, 1)
    b += f'<line x1="{a[0]:.0f}" y1="{a[1]:.0f}" x2="{c[0]:.0f}" y2="{c[1]:.0f}" stroke="#e88a8a" stroke-width="3" opacity=".7"/>'
    # apple pushed down through the sheet: only the part above the paper shows
    ax, ay, R = 600, 1330, 200
    ey, erx, ery = 1450, 178, 52
    d += f'<clipPath id="above2"><rect x="0" y="0" width="1080" height="{ey}"/><ellipse cx="{ax}" cy="{ey}" rx="{erx}" ry="{ery}"/></clipPath>'
    b += f'<ellipse cx="{ax}" cy="{ey}" rx="{erx + 70}" ry="{ery + 26}" fill="#ff5a3a" opacity=".35" filter="url(#b24)"/>'
    b += f'<ellipse cx="{ax}" cy="{ey}" rx="{erx}" ry="{ery}" fill="#5a1010"/>'
    ap = (f'<path d="M{ax} {ay - R + 40} C{ax + 90} {ay - R - 20} {ax + R + 20} {ay - R + 60} {ax + R} {ay + 10} '
          f'C{ax + R - 10} {ay + R - 10} {ax + 80} {ay + R + 20} {ax} {ay + R - 20} '
          f'C{ax - 80} {ay + R + 20} {ax - R + 10} {ay + R - 10} {ax - R} {ay + 10} '
          f'C{ax - R - 20} {ay - R + 60} {ax - 90} {ay - R - 20} {ax} {ay - R + 40}Z"')
    b += f'<g clip-path="url(#above2)"><path {ap} fill="url(#apple2)" stroke="#3a0608" stroke-width="7"/>'
    b += f'<ellipse cx="{ax - 85}" cy="{ay - 95}" rx="48" ry="26" transform="rotate(-35 {ax - 85} {ay - 95})" fill="#fff" opacity=".7" filter="url(#b3)"/>'
    b += f'<path d="M{ax + 140} {ay - 60} Q{ax + 180} {ay + 20} {ax + 160} {ay + 100}" fill="none" stroke="#ffb090" stroke-width="8" opacity=".5"/></g>'
    b += f'<path d="M{ax} {ay - R + 44} Q{ax + 6} {ay - R - 20} {ax + 24} {ay - R - 50}" fill="none" stroke="#4a2a10" stroke-width="12" stroke-linecap="round"/>'
    b += (f'<path d="M{ax + 20} {ay - R - 30} Q{ax + 90} {ay - R - 90} {ax + 140} {ay - R - 40} Q{ax + 80} {ay - R + 10} {ax + 20} {ay - R - 30}Z" '
          f'fill="#5aa83a" stroke="#1d3a10" stroke-width="5"/><path d="M{ax + 30} {ay - R - 30} Q{ax + 80} {ay - R - 50} {ax + 130} {ay - R - 42}" fill="none" stroke="#a8e07a" stroke-width="3"/>')
    b += f'<ellipse cx="{ax}" cy="{ey}" rx="{erx + 6}" ry="{ery + 3}" fill="none" stroke="#ffe08a" stroke-width="10" opacity=".9" filter="url(#b6)"/>'
    b += f'<ellipse cx="{ax}" cy="{ey}" rx="{erx + 4}" ry="{ery + 2}" fill="none" stroke="#fff4c8" stroke-width="5"/>'
    # dashed hint of the whole apple's path: dot -> circle -> dot (thin rings above)
    def flat(u, v, shape, col, s=1.0):
        x, y = bil(Q, u, v)
        if shape == 'tri': pts = [(-40, 14), (40, 14), (0, -14)]
        elif shape == 'sq': pts = [(-34, -12), (34, -12), (34, 12), (-34, 12)]
        else: pts = [(math.cos(a) * 40, math.sin(a) * 14) for a in [k * 6.283 / 5 - 1.57 for k in range(5)]]
        o = f'<polygon points="{P([(x + px * s, y + py * s) for px, py in pts])}" fill="{col}" stroke="#2a2a3a" stroke-width="4" stroke-linejoin="round"/>'
        for ex in (-10, 10):
            o += f'<ellipse cx="{x + ex * s:.0f}" cy="{y - 2:.0f}" rx="{7 * s:.0f}" ry="{3.4 * s:.1f}" fill="#fff" stroke="#2a2a3a" stroke-width="2"/><circle cx="{x + ex * s + 2:.0f}" cy="{y - 2:.0f}" r="{2.2 * s:.1f}" fill="#2a2a3a"/>'
        return o
    b += flat(.85, .22, 'sq', '#f2a83a', 1.9) + flat(.80, .78, 'pent', '#c86ad8', 2.2) + flat(.46, .80, 'tri', '#5a8ae8', 1.9)
    b += spark(880, 1230, 24, '#ffffff') + spark(330, 1250, 16, '#ffffff') + spark(990, 1560, 14, '#fff6d6')
    # frog sitting on the near-left part of the paper with a magnifying glass, looking at the circle
    lens = ('<g transform="translate(70 -70) rotate(20)"><line x1="0" y1="20" x2="0" y2="64" stroke="#6a4a2a" stroke-width="9" stroke-linecap="round"/>'
            '<circle cx="0" cy="0" r="24" fill="#d8f4ff" fill-opacity=".45" stroke="#3a3a48" stroke-width="6"/><path d="M-12 -10 q8 -8 16 -8" fill="none" stroke="#fff" stroke-width="3"/></g>')
    b += '<ellipse cx="230" cy="1650" rx="120" ry="16" fill="#000" opacity=".25" filter="url(#b6)"/>'
    b += frog(230, 1650, 2.7, look=(9, -3), mouth='O', front=lens,
              armL='M-34 -22 q-18 4 -20 24', armR='M38 -22 q22 -2 30 -10',
              legs=((-20, -6, -24, 4, -6), (20, -6, 24, 4, 6)))
    b += '<rect width="1080" height="1920" fill="url(#vig2)"/>'
    lines = [('THEY SEE', 180, 'w'), ('A <span class="g">CIRCLE</span>', 200, 'w')]
    return vpage('#3a98c8', vsvg(d, b), lines, outline='#0a2030', top=640)


# ================= 3: HUNDREDS OF FLAT SLICES (scanner above, frog below) =================
def make_3():
    rnd = random.Random(33)
    d = FILTERS + lin('wall3', [(0, '#cfeee8'), (1, '#8fcfc8')])
    d += lin('ring3', [(0, '#ffffff'), (1, '#b8c8d0')], x2=1, y2=1)
    d += rad('hole3', 540, 520, 310, [(0, '#1a6a8a', 1), (1, '#0a2a40', 1)])
    d += vig('vig3', '#0a3040', .55)
    b = '<rect width="1080" height="1920" fill="url(#wall3)"/>'
    for k in range(0, 1080, 160):
        b += f'<rect x="{k}" y="0" width="4" height="1490" fill="#ffffff" opacity=".35"/>'
    b += '<rect y="1490" width="1080" height="430" fill="#5a9aa0"/><rect y="1490" width="1080" height="8" fill="#e8fffa" opacity=".6"/>'
    for k in range(0, 1080, 120):
        b += f'<line x1="{k}" y1="1498" x2="{k * 1.4 - 216:.0f}" y2="1920" stroke="#4a8a90" stroke-width="3"/>'
    # CT / MRI ring behind the slices
    cx, cyr = 540, 520
    b += f'<circle cx="{cx}" cy="{cyr}" r="400" fill="url(#ring3)" stroke="#2a4a58" stroke-width="7"/>'
    b += f'<circle cx="{cx}" cy="{cyr}" r="400" fill="none" stroke="#ffffff" stroke-width="6" opacity=".7" transform="translate(-6 -6)"/>'
    b += f'<circle cx="{cx}" cy="{cyr}" r="310" fill="url(#hole3)" stroke="#2a4a58" stroke-width="7"/>'
    b += f'<circle cx="{cx}" cy="{cyr}" r="355" fill="none" stroke="#5ad8e8" stroke-width="6" opacity=".55"/>'
    b += ring_glow(cx, cyr, 300, '#5ae8ff', .45)
    # stack of scan slices that together build a head (side profile glow behind)
    o = cyr - 500   # profile designed for a ring centred at y=500
    head = (f'M{cx - 150} {520 + o} Q{cx - 200} {300 + o} {cx - 120} {210 + o} Q{cx - 20} {130 + o} {cx + 90} {180 + o} Q{cx + 170} {230 + o} {cx + 175} {340 + o} '
            f'L{cx + 210} {420 + o} Q{cx + 214} {432 + o} {cx + 190} {436 + o} L{cx + 180} {470 + o} Q{cx + 192} {482 + o} {cx + 178} {494 + o} Q{cx + 186} {530 + o} {cx + 150} {560 + o} '
            f'Q{cx + 110} {590 + o} {cx + 60} {600 + o} L{cx + 60} {790 + o} L{cx - 90} {790 + o} L{cx - 90} {640 + o} Q{cx - 150} {600 + o} {cx - 150} {520 + o}Z')
    b += f'<path d="{head}" fill="#7af0ff" opacity=".22"/><path d="{head}" fill="none" stroke="#bffaff" stroke-width="5" opacity=".8" stroke-dasharray="2 10" stroke-linecap="round"/>'
    prof = [(178, 70), (222, 140), (266, 170), (310, 182), (354, 186), (398, 184), (442, 176), (486, 166), (530, 150), (574, 122), (618, 82), (662, 76), (706, 76), (750, 78)]
    slices = ''
    for k, (y, r) in enumerate(prof):
        yy = y + o; ry = r * .26; key = k in (3, 6, 9)
        slices += f'<ellipse cx="{cx}" cy="{yy}" rx="{r}" ry="{ry:.1f}" fill="#0c3a50" fill-opacity=".7" stroke="#7af0ff" stroke-width="{4 if key else 2.6}" opacity="{1 if key else .82}"/>'
        if r > 60:
            inner = r * (.78 if k < 9 else .5)
            slices += f'<ellipse cx="{cx - (0 if k < 9 else r * .15):.0f}" cy="{yy}" rx="{inner:.0f}" ry="{inner * .26:.1f}" fill="#d8e8ec" opacity=".55"/>'
            if k < 9:
                slices += f'<path d="M{cx} {yy - inner * .24:.0f} L{cx} {yy + inner * .24:.0f}" stroke="#4a7080" stroke-width="2.5"/>'
                for s in (-1, 1):
                    slices += f'<path d="M{cx + s * inner * .25:.0f} {yy - inner * .12:.0f} q{s * inner * .2:.0f} {inner * .1:.0f} {s * inner * .45:.0f} 0" fill="none" stroke="#7a98a8" stroke-width="2.4"/>'
            else:
                slices += f'<ellipse cx="{cx + r * .3:.0f}" cy="{yy}" rx="{r * .14:.0f}" ry="{r * .05:.0f}" fill="#ffffff" opacity=".9"/>'
    b += f'<g filter="url(#b3)" opacity=".6">{slices}</g>' + slices
    yy = prof[6][0] + o
    b += f'<ellipse cx="{cx}" cy="{yy}" rx="300" ry="78" fill="#7af0ff" opacity=".18"/><ellipse cx="{cx}" cy="{yy}" rx="300" ry="78" fill="none" stroke="#bffaff" stroke-width="4" stroke-dasharray="14 10"/>'
    b += spark(cx + 300, 190, 24, '#ffffff') + spark(cx - 330, 860, 16, '#e8ffff') + spark(990, 1000, 16, '#ffffff', .8)
    # frog radiologist (lower right) holding one slice film up; light box with more films (lower left)
    for k, (x, y, rot) in enumerate(((110, 1600, -4), (250, 1585, 3), (390, 1606, -2))):
        r = 70 - k * 6
        b += (f'<g transform="translate({x} {y}) rotate({rot})"><rect x="-66" y="-80" width="132" height="160" rx="6" fill="#0c2a3a" stroke="#06222a" stroke-width="5"/>'
              f'<ellipse cx="0" cy="0" rx="{r * .8:.0f}" ry="{r * .65:.0f}" fill="#d8e8ec" opacity=".75"/><path d="M0 -{r * .6:.0f} V{r * .6:.0f}" stroke="#4a7080" stroke-width="3"/></g>')
    b += '<rect x="20" y="1505" width="470" height="10" rx="5" fill="#2a4a58"/>'
    scrubs = ('<path d="M-37 -2 Q-42 -30 -28 -44 Q6 -30 44 -44 Q50 -30 44 -2 Q6 6 -37 -2Z" fill="#3a8ad8" stroke-width="3.2"/>'
              '<path d="M-8 -36 L6 -22 L20 -36" fill="none" stroke="#1a4a8a" stroke-width="3"/>')
    capm = ('<path d="M-30 -84 Q6 -112 46 -84 Q40 -76 6 -78 Q-26 -76 -30 -84Z" fill="#3a8ad8" stroke-width="3.2"/>'
            '<g transform="translate(-74 -92) rotate(-12)"><rect x="-34" y="-30" width="68" height="60" rx="5" fill="#0c2a3a" stroke-width="3.5"/>'
            '<ellipse cx="0" cy="0" rx="24" ry="20" fill="#d8e8ec" stroke="none" opacity=".8"/><path d="M0 -18 V18 M-14 -6 q6 4 12 0 M14 -6 q-6 4 -12 0" stroke="#4a7080" stroke-width="2.4" fill="none"/></g>')
    b += '<ellipse cx="770" cy="1750" rx="150" ry="22" fill="#000" opacity=".3" filter="url(#b6)"/>'
    b += frog(770, 1750, 2.5, look=(-9, -5), mouth='O', mid=scrubs, front=capm, brows=False,
              armL='M-34 -22 q-24 -10 -34 -40', armR='M38 -22 q18 6 18 26',
              legs=((-20, -6, -24, 4, -6), (20, -6, 24, 4, 6)))
    b += '<rect width="1080" height="1920" fill="url(#vig3)"/>'
    lines = [('HUNDREDS OF', 120, 'w'), ('FLAT', 170, 'w'), ('<span class="g">SLICES</span>', 220, 'w')]
    return vpage('#cfeee8', vsvg(d, b), lines, outline='#06222a', top=950)


# ================= 4: STACK EVERY PHOTO (worldline snakes around the text) =================
def make_4():
    rnd = random.Random(44)
    d = FILTERS + lin('sky4', [(0, '#0a0a2a'), (.6, '#2a1450'), (1, '#5a2a5a')])
    d += lin('rib4', [(0, '#ffb07a'), (.5, '#f2d27a'), (1, '#ff8ad0')], x2=0, y2=-1)
    d += vig('vig4', '#000', .7)
    b = '<rect width="1080" height="1920" fill="url(#sky4)"/>' + starfield(rnd, 260, (0, 0, 1080, 1920))
    b += '<circle cx="900" cy="1180" r="60" fill="#c8704a"/><circle cx="880" cy="1162" r="60" fill="#e8946a" opacity=".5"/>'
    b += '<circle cx="140" cy="300" r="34" fill="#5a8ae8"/><path d="M110 290 q20 -10 40 4" stroke="#8ad86a" stroke-width="8" fill="none"/>'
    b += '<circle cx="880" cy="190" r="44" fill="#d8b87a"/><ellipse cx="880" cy="190" rx="80" ry="16" fill="none" stroke="#f2e0b0" stroke-width="5" transform="rotate(-18 880 190)"/>'
    # worldline: from the frog (bottom) up the right side, over the top, ending upper-left at "now"
    segs = [((620, 1560), (900, 1500), (1000, 1300), (960, 1080)),
            ((960, 1080), (920, 860), (980, 700), (760, 560)),
            ((760, 560), (560, 420), (300, 560), (240, 360))]
    pts = []
    for p0, p1, p2, p3 in segs:
        for k in range(40):
            u = k / 40
            pts.append(tuple((1 - u) ** 3 * a + 3 * (1 - u) ** 2 * u * b_ + 3 * (1 - u) * u * u * c + u ** 3 * e for a, b_, c, e in zip(p0, p1, p2, p3)))
    pts.append(segs[-1][3]); N = len(pts) - 1
    path = 'M' + ' L'.join(f'{x:.1f} {y:.1f}' for x, y in pts)
    b += f'<path d="{path}" fill="none" stroke="#f2d27a" stroke-width="90" opacity=".25" filter="url(#b24)"/>'
    b += f'<path d="{path}" fill="none" stroke="url(#rib4)" stroke-width="18" stroke-linecap="round" opacity=".9"/>'

    def ang(k):
        (x0, y0), (x1, y1) = pts[max(0, k - 1)], pts[min(N, k + 1)]
        return math.degrees(math.atan2(y1 - y0, x1 - x0))
    for k in range(3, N - 2, 2):
        x, y = pts[k]; s = .6 + .5 * (1 - k / N)
        b += (f'<rect x="{-40 * s:.1f}" y="{-50 * s:.1f}" width="{80 * s:.1f}" height="{100 * s:.1f}" rx="3" fill="#fff6e8" fill-opacity=".1" stroke="#fff0d8" stroke-width="2" opacity=".45" '
              f'transform="translate({x:.1f} {y:.1f}) rotate({ang(k) + 90:.1f}) skewY(-20)"/>')

    def kid(h, col):
        hh = 60 * h
        return (f'<circle cx="0" cy="{24 - hh - 12:.1f}" r="{7 + 5 * h:.1f}" fill="{col}"/>'
                f'<path d="M{-9 - 6 * h:.1f} 26 Q{-9 - 6 * h:.1f} {26 - hh:.1f} 0 {26 - hh:.1f} Q{9 + 6 * h:.1f} {26 - hh:.1f} {9 + 6 * h:.1f} 26Z" fill="{col}"/>')
    keys = [(6, .25, '#f2a8c8', 'crib'), (66, .5, '#8ad8f2', ''), (88, .75, '#a8e88a', ''), (104, .95, '#f2c27a', ''), (N - 2, 1, '#ffd0a0', '')]
    for k, h, col, extra in keys:
        x, y = pts[k]; s = 1.35 - .4 * k / N
        tilt = rnd.uniform(-10, 10)
        g = (f'<g transform="translate({x:.1f} {y:.1f}) rotate({tilt:.1f}) scale({s:.2f})">'
             f'<rect x="-58" y="-70" width="116" height="140" rx="6" fill="#000" opacity=".35" transform="translate(6 8)"/>'
             f'<rect x="-58" y="-70" width="116" height="140" rx="6" fill="#fffaf0" stroke="#3a2a3a" stroke-width="4"/>'
             f'<rect x="-48" y="-60" width="96" height="96" fill="#2a3a6a"/><rect x="-48" y="6" width="96" height="30" fill="#4a5a8a"/>')
        if extra == 'crib':
            g += '<path d="M-36 30 V2 M36 30 V2 M-36 14 H36 M-24 14 V30 M-12 14 V30 M0 14 V30 M12 14 V30 M24 14 V30" stroke="#f2d27a" stroke-width="3.5" fill="none"/>'
            g += '<ellipse cx="0" cy="8" rx="18" ry="9" fill="#f2a8c8"/><circle cx="-14" cy="2" r="9" fill="#f8d0b0"/>'
        else:
            g += f'<g transform="translate(0 4)">{kid(h, col)}</g>'
        b += g + '</g>'
    bx, by = pts[96]
    b += ring_glow(int(bx), int(by), 70, '#ffffff', .5) + f'<circle cx="{bx:.0f}" cy="{by:.0f}" r="20" fill="#fff6d6" stroke="#f2d27a" stroke-width="5"/>'
    b += spark(560, 300, 22, '#ffffff') + spark(160, 1400, 16) + spark(1000, 520, 14)
    # frog photographer at the start of the line (lower middle-left)
    cam = ('<g transform="translate(56 -78) rotate(-12)"><rect x="-26" y="-18" width="52" height="36" rx="6" fill="#2a2a34" stroke-width="3.5"/>'
           '<rect x="-10" y="-26" width="20" height="10" rx="2" fill="#2a2a34" stroke-width="3"/><circle cx="0" cy="0" r="12" fill="#5a7ad8" stroke-width="3"/>'
           '<circle cx="-3" cy="-3" r="4" fill="#fff" stroke="none"/><circle cx="18" cy="-10" r="3.4" fill="#ff5a5a" stroke="none"/></g>')
    scarf = '<path d="M-30 -30 Q6 -18 44 -30 L46 -20 Q6 -6 -32 -20Z" fill="#e85a6a" stroke-width="3"/><path d="M30 -24 L40 2 L28 2 L22 -20Z" fill="#e85a6a" stroke-width="3"/>'
    b += '<ellipse cx="360" cy="1660" rx="140" ry="22" fill="#000" opacity=".45" filter="url(#b6)"/>'
    b += ring_glow(360, 1560, 170, '#ff9ad0', .2)
    b += frog(360, 1660, 3.0, look=(9, -6), mouth='O', mid=scarf, front=cam,
              armL='M-34 -22 q-18 6 -20 26', armR='M38 -22 q14 -18 22 -46',
              legs=((-20, -6, -24, 4, -6), (20, -6, 24, 4, 6)))
    b += '<rect width="1080" height="1920" fill="url(#vig4)"/>'
    lines = [('STACK', 170, 'w'), ('EVERY', 170, 'w'), ('<span class="g">PHOTO</span>', 220, 'w')]
    return vpage('#0a0a2a', vsvg(d, b), lines, outline='#080418', top=700)


# ================= 5: BUILT FOR 3D ONLY (brain above, savannah + frog below) =================
def make_5():
    rnd = random.Random(55)
    d = FILTERS + lin('sky5', [(0, '#3a1a4a'), (.3, '#a8483a'), (.55, '#f2a84a'), (.7, '#f8d080'), (1, '#f8d080')])
    d += '<radialGradient id="brain5" cx=".38" cy=".3" r=".85"><stop offset="0" stop-color="#ffd0dc"/><stop offset=".45" stop-color="#f08aa8"/><stop offset="1" stop-color="#b04a72"/></radialGradient>'
    d += rad('sun5', 540, 600, 620, [(0, '#fff2b0', .95), (.25, '#ffd070', .7), (1, '#ff8a3a', 0)])
    d += vig('vig5', '#1a0a10', .7)
    b = '<rect width="1080" height="1920" fill="url(#sky5)"/><rect width="1080" height="1920" fill="url(#sun5)"/>'
    b += '<circle cx="540" cy="640" r="270" fill="#ffe08a" opacity=".85"/>'
    # savannah ground from y 1300, acacias and birds
    b += '<path d="M0 1300 Q300 1270 600 1290 T1080 1280 L1080 1920 L0 1920Z" fill="#6a3418"/>'
    b += '<path d="M0 1360 Q400 1320 760 1350 T1080 1340 L1080 1920 L0 1920Z" fill="#3a1c0c"/>'

    def acacia(x, y, s):
        return (f'<g transform="translate({x} {y}) scale({s})" fill="#24100a"><path d="M-6 0 L-4 -120 Q-30 -150 -60 -160 L-56 -166 Q-24 -156 0 -132 Q20 -160 50 -168 L52 -162 Q24 -150 6 -120 L8 0Z"/>'
                f'<ellipse cx="0" cy="-176" rx="130" ry="26"/><ellipse cx="-60" cy="-168" rx="70" ry="18"/><ellipse cx="70" cy="-170" rx="70" ry="16"/></g>')
    b += acacia(960, 1300, .6) + acacia(110, 1300, .45)
    for k in range(5):
        x, y = 140 + k * 46, 260 + (k % 2) * 30
        b += f'<path d="M{x - 12} {y} q6 -8 12 0 q6 -8 12 0" fill="none" stroke="#3a1a1a" stroke-width="3"/>'
    # the brain (upper middle), brainstem down to the horizon
    bx, by = 520, 560; sc = .95
    b += f'<g transform="translate({bx} {by}) scale({sc}) translate({-bx} {-by})">'
    b += f'<path d="M{bx + 120} {by + 170} Q{bx + 140} {by + 260} {bx + 110} {by + 300} L{bx + 60} {by + 300} Q{bx + 80} {by + 250} {bx + 60} {by + 180}Z" fill="#c8607a" stroke="#4a1428" stroke-width="6"/>'
    b += f'<ellipse cx="{bx + 190}" cy="{by + 150}" rx="110" ry="70" fill="#d8708e" stroke="#4a1428" stroke-width="6"/>'
    for k in range(-3, 4):
        b += f'<path d="M{bx + 110} {by + 150 + k * 16} Q{bx + 190} {by + 140 + k * 18} {bx + 280} {by + 150 + k * 14}" fill="none" stroke="#9a3a5a" stroke-width="3"/>'
    blob = f'<ellipse cx="{bx}" cy="{by - 20}" rx="320" ry="215"/>'
    for a in range(0, 360, 24):
        r = math.radians(a)
        blob += f'<circle cx="{bx + 290 * math.cos(r):.0f}" cy="{by - 20 + 190 * math.sin(r):.0f}" r="62"/>'
    d += f'<clipPath id="bclip5">{blob}</clipPath>'
    b += f'<g stroke="#4a1428" stroke-width="14">{blob}</g>'.replace('<ellipse', '<ellipse fill="#4a1428"').replace('<circle', '<circle fill="#4a1428"')
    b += f'<g fill="url(#brain5)" clip-path="url(#bclip5)"><rect x="{bx - 400}" y="{by - 300}" width="800" height="560"/>'
    for j in range(10):
        y0 = by - 230 + j * 46; ph = rnd.uniform(0, 6.28); amp = rnd.uniform(12, 20)
        pts_ = [(x, y0 + amp * math.sin(x / 34 + ph) + 8 * math.sin(x / 13 + j)) for x in range(bx - 360, bx + 361, 12)]
        dd = 'M' + ' L'.join(f'{x:.0f} {y:.0f}' for x, y in pts_)
        b += f'<path d="{dd}" fill="none" stroke="#a8406a" stroke-width="8" stroke-linecap="round" stroke-linejoin="round"/>'
        b += f'<path d="{dd}" fill="none" stroke="#ffd8e4" stroke-width="3" opacity=".5" transform="translate(-2 -7)"/>'
    b += f'<path d="M{bx - 330} {by - 10} Q{bx - 100} {by + 50} {bx + 140} {by - 30}" fill="none" stroke="#7a2448" stroke-width="10"/>'
    b += f'<ellipse cx="{bx - 120}" cy="{by - 150}" rx="120" ry="50" fill="#fff" opacity=".35" filter="url(#b12)"/></g></g>'
    # hypercube (cube inside cube + 8 struts) above right, zapping the brain
    hx, hy = 860, 200
    sp, ed = tess_screen(0.0, 0.55, -0.4, hx, hy, 120, d4=3.0)
    b += ring_glow(hx, hy, 180, '#8af0ff', .5)
    b += tess_draw(sp, ed, '#8af0ff', '#5ac8ff', '#c89aff', w=6, gcol='#5ac8ff', core='#ffffff')
    for ang, L in ((2.3, 240), (2.0, 220), (2.6, 230)):
        b += f'<polyline points="{jag(rnd, 800, 280, ang, L, 7, 20)}" fill="none" stroke="#bff8ff" stroke-width="7" stroke-linejoin="round" opacity=".95"/>'
        b += f'<polyline points="{jag(rnd, 800, 280, ang, L, 7, 20)}" fill="none" stroke="#5ae8ff" stroke-width="16" opacity=".4" filter="url(#b6)"/>'
    for x, y in ((640, 400), (720, 470), (590, 460)):
        b += spark(x, y, 26, '#ffffff', .95)
    for k in range(3):
        x = 300 + k * 110
        b += f'<path d="M{x} 360 q-30 -50 0 -90 q30 -40 0 -90" fill="none" stroke="#5a4a5a" stroke-width="{22 - k * 4}" stroke-linecap="round" opacity=".45" filter="url(#b6)"/>'
    # frog in a safari hat peeking out of the tall grass, a snake nearby (lower part)
    hat = ('<path d="M-46 -78 Q6 -92 58 -78 Q60 -70 6 -72 Q-46 -70 -46 -78Z" fill="#c8a060" stroke-width="3.2"/>'
           '<path d="M-26 -78 Q-24 -112 6 -114 Q38 -112 40 -78Z" fill="#d8b878" stroke-width="3.2"/><path d="M-26 -84 L40 -84" stroke="#7a4a20" stroke-width="6"/>')
    b += frog(560, 1700, 2.8, look=(-6, -8), mouth='O', front=hat, brows=False,
              armL='M-34 -22 q-10 -8 -12 -18', armR='M38 -22 q10 -8 12 -18')
    sn = 'M180 1690 C230 1630 270 1690 320 1640 C360 1600 390 1640 370 1670'
    b += f'<path d="{sn}" fill="none" stroke="#2a3a10" stroke-width="22" stroke-linecap="round"/><path d="{sn}" fill="none" stroke="#6a8a2a" stroke-width="13" stroke-linecap="round"/>'
    b += '<circle cx="370" cy="1668" r="16" fill="#6a8a2a" stroke="#2a3a10" stroke-width="5"/><circle cx="374" cy="1662" r="4" fill="#fff"/><path d="M384 1674 l14 4 m-14 -4 l12 -4" stroke="#d83a3a" stroke-width="3"/>'
    for k in range(110):
        x = rnd.uniform(60, 1020); h = rnd.uniform(90, 220); base = rnd.uniform(1700, 1760)
        if 470 < x < 650 and h > 150: h = 140
        col = rnd.choice(['#8a6a2a', '#a8803a', '#6a4a1a', '#c89a4a'])
        b += f'<path d="M{x:.0f} {base:.0f} Q{x + rnd.uniform(-10, 10):.0f} {base - h * .6:.0f} {x + rnd.uniform(-30, 30):.0f} {base - h:.0f}" fill="none" stroke="{col}" stroke-width="{rnd.uniform(4, 8):.1f}" stroke-linecap="round"/>'
    b += '<rect width="1080" height="1920" fill="url(#vig5)"/>'
    lines = [('BUILT FOR', 170, 'w'), ('<span class="g">3D</span> ONLY', 210, 'w')]
    return vpage('#3a1a4a', vsvg(d, b), lines, outline='#1a0608', top=880)


for n, fn in enumerate((make_1, make_2, make_3, make_4, make_5), 1):
    out = os.path.join(REPO, 'videos', f'fourth-dimension-short{n}', 'thumb')
    os.makedirs(out, exist_ok=True)
    for f in ('common.css', 'Fredoka-700.woff2'):
        shutil.copy(os.path.join(REPO, 'tools', 'assets', 'thumb_v', f), out)
    open(os.path.join(out, 'A.html'), 'w').write(fn())
print('ok')
