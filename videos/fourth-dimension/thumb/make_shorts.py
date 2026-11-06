# Shorts thumbnails for fourth-dimension-short1..5 (guideline 16-9: one 1920x1080 thumbnail per short, frog, bottom-right empty).
# Run: python3 videos/fourth-dimension/thumb/make_shorts.py  -> videos/fourth-dimension-shortN/thumb/A.html (+ common.css, Fredoka-700.woff2)
# then: for N in 1 2 3 4 5; do SLUG=fourth-dimension-shortN python3 tools/thumb_shot.py; done
# 1 A 4D SHADOW?          short1 S05-S07: "the shadow of a four-dimensional object is a ... three-dimensional solid" / "smaller cube ... inside a larger cube"
#                         lamp-lit tesseract shadow (cube in cube + 8 struts) on a violet stage; frog with a flashlight
# 2 THEY SEE A CIRCLE     short2 S05-S08: an apple pushed through a paper world; flat shapes see only a circle; frog with magnifier on the paper
# 3 HUNDREDS OF FLAT SLICES  short3 S03-S06: scanner builds its picture from a stack of thin 2D cross-sections (often hundreds); slices stack into a head;
#                         frog in blue scrubs holding one slice (a slicing trick, no claim of a 4D machine)
# 4 STACK EVERY PHOTO     short4 S04-S07: stack every photograph of you -> a solid track, the worldline (relativity view); frog photographer
# 5 BUILT FOR 3D ONLY     short5 S05-S09: brains shaped for a 3D world on the savannah; a hypercube short-circuits a brain; frog in safari hat in the grass
import os, sys, math, random, shutil
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
sys.path.insert(0, os.path.join(REPO, 'tools'))
from thumb_lib import page, svg, lin, rad, spark
src = open(os.path.join(HERE, 'make.py')).read()
exec(src[src.index('INK = '):src.index('# ================= A:')])   # frog, tess_screen, tess_draw, hull, starfield, jag, P, FILTERS


def ring_glow(cx, cy, r, col, op=.2):
    return f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{col}" opacity="{op}" filter="url(#b50)"/>'


# ================= 1: A 4D SHADOW? =================
def make_1():
    rnd = random.Random(11)
    d = FILTERS + lin('wall1', [(0, '#1a0f3a'), (.7, '#2c1658'), (1, '#160a2c')])
    d += lin('floor1', [(0, '#24124a'), (1, '#07030f')])
    d += '<linearGradient id="cone1" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ffe7a8" stop-opacity=".55"/><stop offset="1" stop-color="#ffcf70" stop-opacity="0"/></linearGradient>'
    d += '<linearGradient id="beam1" x1="0" y1="1" x2="1" y2="0"><stop offset="0" stop-color="#fff2c0" stop-opacity=".75"/><stop offset="1" stop-color="#ffd27a" stop-opacity="0"/></linearGradient>'
    d += rad('vig1', 960, 540, 1150, [(0, '#000', 0), (.62, '#000', 0), (1, '#000', .75)])
    b = '<rect width="1920" height="1080" fill="url(#wall1)"/>'
    # stage curtain folds behind
    for k in range(0, 1920, 90):
        b += f'<path d="M{k} 0 Q{k + 45} 380 {k + 10} 780 L{k + 60} 780 Q{k + 90} 380 {k + 50} 0Z" fill="#3a1e6e" opacity=".35"/>'
    b += '<rect y="770" width="1920" height="310" fill="url(#floor1)"/>'
    for k in range(-14, 15):
        b += f'<line x1="{1230 + k * 90}" y1="770" x2="{1230 + k * 300}" y2="1080" stroke="#8a5ad8" stroke-width="2" opacity=".18"/>'
    for yy in (800, 850, 920, 1010):
        b += f'<line x1="0" y1="{yy}" x2="1920" y2="{yy}" stroke="#8a5ad8" stroke-width="2" opacity=".14"/>'
    # hanging lamp + cone of light
    cx, cy = 1330, 480
    b += '<path d="M1190 60 L1470 60 L1780 900 L880 900Z" fill="url(#cone1)"/>'
    b += '<line x1="1330" y1="0" x2="1330" y2="34" stroke="#0a0614" stroke-width="8"/>'
    b += '<path d="M1250 70 Q1330 20 1410 70 L1430 84 L1230 84Z" fill="#3a3550" stroke="#0a0614" stroke-width="5"/>'
    b += '<ellipse cx="1330" cy="84" rx="100" ry="14" fill="#fff6d6"/>' + ring_glow(1330, 90, 140, '#ffe9a8', .55)
    # shadow of the shadow on the floor
    b += '<ellipse cx="1340" cy="860" rx="330" ry="48" fill="#05020c" opacity=".7" filter="url(#b12)"/>'
    # the 3D shadow of a tesseract: cube inside cube, 8 struts; smoky dark faces + bright edges
    sp, ed = tess_screen(0.0, 0.62, -0.42, cx, cy, 285, d4=3.0)
    outer = [(p[0], p[1]) for i, p in enumerate(sp) if i & 1]
    inner = [(p[0], p[1]) for i, p in enumerate(sp) if not i & 1]
    b += ring_glow(cx, cy, 380, '#b07aff', .35)
    b += f'<polygon points="{P(hull(outer))}" fill="#120626" opacity=".72"/>'
    b += f'<polygon points="{P(hull(inner))}" fill="#3a1670" opacity=".75"/>'
    b += ring_glow(cx, cy, 120, '#ffe08a', .55)
    b += tess_draw(sp, ed, '#ffd77a', '#c89aff', '#ff8ad8', w=9, gcol='#a070ff', core='#fff8e8')
    b += spark(cx + 330, cy - 300, 26) + spark(cx - 360, cy + 200, 18, '#f0e0ff') + spark(1700, 560, 16, '#fff6d6', .7)
    for _ in range(40):
        a = rnd.uniform(0, 6.28); r = rnd.uniform(330, 470)
        x, y = cx + r * math.cos(a), cy + r * math.sin(a) * .85
        if x < 950 and y < 470: continue
        b += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{rnd.uniform(2, 4.5):.1f}" fill="#f0e0ff" opacity="{rnd.uniform(.3, .85):.2f}"/>'
    # frog usher with a flashlight, pointing it up at the shadow
    vest = ('<path d="M-37 -2 Q-40 -30 -28 -44 Q6 -30 44 -44 Q50 -30 44 -2 Q6 6 -37 -2Z" fill="#7a2a8a" stroke-width="3.2"/>'
            '<circle cx="6" cy="-26" r="3.5" fill="#f2d27a" stroke="none"/><circle cx="6" cy="-14" r="3.5" fill="#f2d27a" stroke="none"/>')
    torch = ('<g transform="translate(62 -78) rotate(-40)"><rect x="-9" y="-6" width="18" height="44" rx="5" fill="#3a3a48" stroke-width="3"/>'
             '<path d="M-14 -6 L14 -6 L18 -22 L-18 -22Z" fill="#c8c8d8" stroke-width="3"/><ellipse cx="0" cy="-22" rx="18" ry="5" fill="#fff6c8" stroke-width="2.5"/></g>')
    b += '<path d="M780 760 L1100 390 L1240 490 Z" fill="url(#beam1)" opacity=".8"/>'
    b += '<ellipse cx="640" cy="1000" rx="150" ry="22" fill="#000" opacity=".5" filter="url(#b6)"/>'
    b += frog(640, 1000, 2.9, look=(8, -6), mouth='O', mid=vest, front=torch,
              armL='M-34 -22 q-20 4 -24 26', armR='M38 -22 q20 -14 26 -44',
              legs=((-20, -6, -24, 4, -6), (20, -6, 24, 4, 6)))
    b += '<rect width="1920" height="1080" fill="url(#vig1)"/>'
    lines = [('A 4D', 200, 'w'), ('<span class="g">SHADOW?</span>', 230, 'w')]
    return page('#1a0f3a', svg(d, b), lines, outline='#0a0418', top=52)


# ================= 2: THEY SEE A CIRCLE =================
def make_2():
    rnd = random.Random(22)
    d = FILTERS + lin('sky2', [(0, '#5fb8d8'), (.6, '#a8dcea'), (1, '#e8f4ee')])
    d += lin('paper2', [(0, '#fff8e6'), (1, '#f0dfb8')], x2=1, y2=1)
    d += '<radialGradient id="apple2" cx=".36" cy=".32" r=".8"><stop offset="0" stop-color="#ff8a7a"/><stop offset=".35" stop-color="#e8322e"/><stop offset=".8" stop-color="#a8141e"/><stop offset="1" stop-color="#6a0a12"/></radialGradient>'
    d += rad('vig2', 960, 540, 1150, [(0, '#000', 0), (.7, '#000', 0), (1, '#103040', .45)])
    b = '<rect width="1920" height="1080" fill="url(#sky2)"/>'
    for x, y, s in ((1500, 150, 1.2), (1820, 300, .8), (980, 520, .9), (300, 720, 1.1)):
        b += (f'<g transform="translate({x} {y}) scale({s})" fill="#ffffff" opacity=".75"><ellipse cx="0" cy="0" rx="120" ry="40"/>'
              f'<circle cx="-40" cy="-20" r="46"/><circle cx="30" cy="-34" r="56"/><circle cx="80" cy="-6" r="36"/></g>')
    # the paper world (a flat sheet in perspective)
    Q = [(980, 520), (1870, 540), (1560, 900), (600, 870)]   # far-left, far-right, near-right, near-left
    b += f'<polygon points="{P([(x + 10, y + 40) for x, y in Q])}" fill="#2a5a6a" opacity=".35" filter="url(#b12)"/>'
    b += f'<polygon points="{P([Q[3], Q[2], (Q[2][0], Q[2][1] + 14), (Q[3][0], Q[3][1] + 14)])}" fill="#c8b48a" stroke="#5a4a2a" stroke-width="4"/>'
    b += f'<polygon points="{P(Q)}" fill="url(#paper2)" stroke="#5a4a2a" stroke-width="5" stroke-linejoin="round"/>'
    for k in range(1, 9):   # notebook lines on the paper
        a, c = bil(Q, 0, k / 9), bil(Q, 1, k / 9)
        b += f'<line x1="{a[0]:.0f}" y1="{a[1]:.0f}" x2="{c[0]:.0f}" y2="{c[1]:.0f}" stroke="#8ab8d8" stroke-width="2.4" opacity=".55"/>'
    a, c = bil(Q, .08, 0), bil(Q, .08, 1)
    b += f'<line x1="{a[0]:.0f}" y1="{a[1]:.0f}" x2="{c[0]:.0f}" y2="{c[1]:.0f}" stroke="#e88a8a" stroke-width="3" opacity=".7"/>'
    # apple pushed down through the sheet: only the part above the paper is visible
    ax, ay, R = 1320, 520, 210
    ey, erx, ery = 640, 186, 50
    d += (f'<clipPath id="above2"><rect x="0" y="0" width="1920" height="{ey}"/><ellipse cx="{ax}" cy="{ey}" rx="{erx}" ry="{ery}"/></clipPath>')
    b += f'<ellipse cx="{ax}" cy="{ey}" rx="{erx + 70}" ry="{ery + 26}" fill="#ff5a3a" opacity=".35" filter="url(#b24)"/>'
    b += f'<ellipse cx="{ax}" cy="{ey}" rx="{erx}" ry="{ery}" fill="#5a1010"/>'
    ap = (f'<path d="M{ax} {ay - R + 40} C{ax + 90} {ay - R - 20} {ax + R + 20} {ay - R + 60} {ax + R} {ay + 10} '
          f'C{ax + R - 10} {ay + R - 10} {ax + 80} {ay + R + 20} {ax} {ay + R - 20} '
          f'C{ax - 80} {ay + R + 20} {ax - R + 10} {ay + R - 10} {ax - R} {ay + 10} '
          f'C{ax - R - 20} {ay - R + 60} {ax - 90} {ay - R - 20} {ax} {ay - R + 40}Z"')
    b += f'<g clip-path="url(#above2)"><path {ap} fill="url(#apple2)" stroke="#3a0608" stroke-width="7"/>'
    b += f'<ellipse cx="{ax - 85}" cy="{ay - 95}" rx="48" ry="26" transform="rotate(-35 {ax - 85} {ay - 95})" fill="#fff" opacity=".7" filter="url(#b3)"/>'
    b += f'<path d="M{ax + 150} {ay - 60} Q{ax + 190} {ay + 40} {ax + 160} {ay + 130}" fill="none" stroke="#ffb090" stroke-width="8" opacity=".5"/></g>'
    b += f'<path d="M{ax} {ay - R + 44} Q{ax + 6} {ay - R - 20} {ax + 24} {ay - R - 50}" fill="none" stroke="#4a2a10" stroke-width="12" stroke-linecap="round"/>'
    b += (f'<path d="M{ax + 20} {ay - R - 30} Q{ax + 90} {ay - R - 90} {ax + 140} {ay - R - 40} Q{ax + 80} {ay - R + 10} {ax + 20} {ay - R - 30}Z" '
          f'fill="#5aa83a" stroke="#1d3a10" stroke-width="5"/><path d="M{ax + 30} {ay - R - 30} Q{ax + 80} {ay - R - 50} {ax + 130} {ay - R - 42}" fill="none" stroke="#a8e07a" stroke-width="3"/>')
    # what the flat world sees: a glowing circle on the paper
    b += f'<ellipse cx="{ax}" cy="{ey}" rx="{erx + 6}" ry="{ery + 3}" fill="none" stroke="#ffe08a" stroke-width="10" opacity=".9" filter="url(#b6)"/>'
    b += f'<ellipse cx="{ax}" cy="{ey}" rx="{erx + 4}" ry="{ery + 2}" fill="none" stroke="#fff4c8" stroke-width="5"/>'
    # flatlanders lying in the paper (skewed shapes with eyes)
    def flat(u, v, shape, col, s=1.0):
        x, y = bil(Q, u, v)
        if shape == 'tri': pts = [(-40, 14), (40, 14), (0, -14)]
        elif shape == 'sq': pts = [(-34, -12), (34, -12), (34, 12), (-34, 12)]
        else: pts = [(math.cos(a) * 40, math.sin(a) * 14) for a in [k * 6.283 / 5 - 1.57 for k in range(5)]]
        o = f'<polygon points="{P([(x + px * s, y + py * s) for px, py in pts])}" fill="{col}" stroke="#2a2a3a" stroke-width="4" stroke-linejoin="round"/>'
        for ex in (-10, 10):
            o += f'<ellipse cx="{x + ex * s:.0f}" cy="{y - 2:.0f}" rx="{7 * s:.0f}" ry="{3.4 * s:.1f}" fill="#fff" stroke="#2a2a3a" stroke-width="2"/><circle cx="{x + ex * s + 2:.0f}" cy="{y - 2:.0f}" r="{2.2 * s:.1f}" fill="#2a2a3a"/>'
        return o
    b += flat(.30, .62, 'tri', '#5a8ae8', 2.2) + flat(.86, .30, 'sq', '#f2a83a', 1.9) + flat(.66, .84, 'pent', '#c86ad8', 2.2)
    b += spark(1530, 300, 24, '#ffffff') + spark(1020, 420, 16, '#ffffff') + spark(1440, 760, 14, '#fff6d6')
    # frog sitting on the near-left corner of the paper with a magnifying glass
    lens = ('<g transform="translate(70 -70) rotate(20)"><line x1="0" y1="20" x2="0" y2="64" stroke="#6a4a2a" stroke-width="9" stroke-linecap="round"/>'
            '<circle cx="0" cy="0" r="24" fill="#d8f4ff" fill-opacity=".45" stroke="#3a3a48" stroke-width="6"/><path d="M-12 -10 q8 -8 16 -8" fill="none" stroke="#fff" stroke-width="3"/></g>')
    b += '<ellipse cx="770" cy="880" rx="120" ry="16" fill="#000" opacity=".25" filter="url(#b6)"/>'
    b += frog(770, 880, 2.6, look=(9, -2), mouth='O', front=lens,
              armL='M-34 -22 q-18 4 -20 24', armR='M38 -22 q22 -2 30 -10',
              legs=((-20, -6, -24, 4, -6), (20, -6, 24, 4, 6)))
    b += '<rect width="1920" height="1080" fill="url(#vig2)"/>'
    lines = [('THEY SEE', 170, 'w'), ('A <span class="g">CIRCLE</span>', 205, 'w')]
    return page('#5fb8d8', svg(d, b), lines, outline='#0a2030', top=52)


# ================= 3: HUNDREDS OF FLAT SLICES =================
def make_3():
    rnd = random.Random(33)
    d = FILTERS + lin('wall3', [(0, '#cfeee8'), (1, '#8fcfc8')])
    d += lin('ring3', [(0, '#ffffff'), (1, '#b8c8d0')], x2=1, y2=1)
    d += rad('hole3', 1300, 520, 330, [(0, '#1a6a8a', 1), (1, '#0a2a40', 1)])
    d += rad('vig3', 960, 540, 1150, [(0, '#000', 0), (.65, '#000', 0), (1, '#0a3040', .55)])
    b = '<rect width="1920" height="1080" fill="url(#wall3)"/>'
    for k in range(0, 1920, 160):
        b += f'<rect x="{k}" y="0" width="4" height="790" fill="#ffffff" opacity=".35"/>'
    b += '<rect y="790" width="1920" height="290" fill="#5a9aa0"/><rect y="790" width="1920" height="8" fill="#e8fffa" opacity=".6"/>'
    # CT / MRI ring behind the slices
    cx = 1300
    b += '<ellipse cx="1300" cy="880" rx="520" ry="50" fill="#0a2a30" opacity=".35" filter="url(#b12)"/>'
    b += '<rect x="900" y="760" width="800" height="120" rx="30" fill="url(#ring3)" stroke="#2a4a58" stroke-width="6"/>'
    b += f'<circle cx="{cx}" cy="500" r="430" fill="url(#ring3)" stroke="#2a4a58" stroke-width="7"/>'
    b += f'<circle cx="{cx}" cy="500" r="430" fill="none" stroke="#ffffff" stroke-width="6" opacity=".7" transform="translate(-6 -6)"/>'
    b += f'<circle cx="{cx}" cy="500" r="330" fill="url(#hole3)" stroke="#2a4a58" stroke-width="7"/>'
    b += f'<circle cx="{cx}" cy="500" r="380" fill="none" stroke="#5ad8e8" stroke-width="6" opacity=".55"/>'
    b += ring_glow(cx, 500, 300, '#5ae8ff', .45)
    # stack of scan slices that together build a head (exploded vertically)
    prof = [(178, 70), (222, 140), (266, 170), (310, 182), (354, 186), (398, 184), (442, 176), (486, 166), (530, 150), (574, 122), (618, 82), (662, 76), (706, 76), (750, 78)]
    slices = ''
    for k, (y, r) in enumerate(prof):
        yy = y
        ry = r * .26
        key = k in (3, 6, 9)
        op = 1 if key else .82
        slices += f'<ellipse cx="{cx}" cy="{yy}" rx="{r}" ry="{ry:.1f}" fill="#0c3a50" fill-opacity=".7" stroke="#7af0ff" stroke-width="{4 if key else 2.6}" opacity="{op}"/>'
        if r > 60:   # grey anatomy inside each slice
            inner = r * (.78 if k < 9 else .5)
            slices += f'<ellipse cx="{cx - (0 if k < 9 else r * .15):.0f}" cy="{yy}" rx="{inner:.0f}" ry="{inner * .26:.1f}" fill="#d8e8ec" opacity=".55"/>'
            if k < 9:
                slices += f'<path d="M{cx} {yy - inner * .24:.0f} L{cx} {yy + inner * .24:.0f}" stroke="#4a7080" stroke-width="2.5"/>'
                for s in (-1, 1):
                    slices += f'<path d="M{cx + s * inner * .25:.0f} {yy - inner * .12:.0f} q{s * inner * .2:.0f} {inner * .1:.0f} {s * inner * .45:.0f} 0" fill="none" stroke="#7a98a8" stroke-width="2.4"/>'
            else:
                slices += f'<ellipse cx="{cx + r * .3:.0f}" cy="{yy}" rx="{r * .14:.0f}" ry="{r * .05:.0f}" fill="#ffffff" opacity=".9"/>'
    head = (f'M{cx - 150} 520 Q{cx - 200} 300 {cx - 120} 210 Q{cx - 20} 130 {cx + 90} 180 Q{cx + 170} 230 {cx + 175} 340 '
            f'L{cx + 210} 420 Q{cx + 214} 432 {cx + 190} 436 L{cx + 180} 470 Q{cx + 192} 482 {cx + 178} 494 Q{cx + 186} 530 {cx + 150} 560 '
            f'Q{cx + 110} 590 {cx + 60} 600 L{cx + 60} 790 L{cx - 90} 790 L{cx - 90} 640 Q{cx - 150} 600 {cx - 150} 520Z')
    b += f'<path d="{head}" fill="#7af0ff" opacity=".22"/><path d="{head}" fill="none" stroke="#bffaff" stroke-width="5" opacity=".8" stroke-dasharray="2 10" stroke-linecap="round"/>'
    b += f'<g filter="url(#b3)" opacity=".6">{slices}</g>' + slices
    # bright scan plane passing through the stack
    yy = prof[6][0]
    b += f'<ellipse cx="{cx}" cy="{yy}" rx="300" ry="78" fill="#7af0ff" opacity=".18"/><ellipse cx="{cx}" cy="{yy}" rx="300" ry="78" fill="none" stroke="#bffaff" stroke-width="4" stroke-dasharray="14 10"/>'
    b += spark(cx + 260, 210, 24, '#ffffff') + spark(cx - 280, 640, 16, '#e8ffff') + spark(1720, 260, 16, '#ffffff', .8)
    # frog radiologist in blue scrubs + cap, holding one slice film up
    scrubs = ('<path d="M-37 -2 Q-42 -30 -28 -44 Q6 -30 44 -44 Q50 -30 44 -2 Q6 6 -37 -2Z" fill="#3a8ad8" stroke-width="3.2"/>'
              '<path d="M-8 -36 L6 -22 L20 -36" fill="none" stroke="#1a4a8a" stroke-width="3"/>')
    capm = ('<path d="M-30 -84 Q6 -112 46 -84 Q40 -76 6 -78 Q-26 -76 -30 -84Z" fill="#3a8ad8" stroke-width="3.2"/>'
            '<g transform="translate(-74 -92) rotate(-12)"><rect x="-34" y="-30" width="68" height="60" rx="5" fill="#0c2a3a" stroke-width="3.5"/>'
            '<ellipse cx="0" cy="0" rx="24" ry="20" fill="#d8e8ec" stroke="none" opacity=".8"/><path d="M0 -18 V18 M-14 -6 q6 4 12 0 M14 -6 q-6 4 -12 0" stroke="#4a7080" stroke-width="2.4" fill="none"/></g>')
    b += '<ellipse cx="600" cy="1000" rx="150" ry="22" fill="#000" opacity=".3" filter="url(#b6)"/>'
    b += frog(600, 1000, 2.9, look=(9, -4), mouth='O', mid=scrubs, front=capm, brows=False,
              armL='M-34 -22 q-24 -10 -34 -40', armR='M38 -22 q18 6 18 26',
              legs=((-20, -6, -24, 4, -6), (20, -6, 24, 4, 6)))
    b += '<rect width="1920" height="1080" fill="url(#vig3)"/>'
    lines = [('HUNDREDS OF', 140, 'w'), ('FLAT', 190, 'w'), ('<span class="g">SLICES</span>', 230, 'w')]
    return page('#cfeee8', svg(d, b), lines, outline='#06222a', top=40)


# ================= 4: STACK EVERY PHOTO =================
def make_4():
    rnd = random.Random(44)
    d = FILTERS + lin('sky4', [(0, '#0a0a2a'), (.6, '#2a1450'), (1, '#5a2a5a')])
    d += lin('rib4', [(0, '#ffb07a'), (.5, '#f2d27a'), (1, '#ff8ad0')], x2=1, y2=-1)
    d += rad('vig4', 960, 540, 1150, [(0, '#000', 0), (.65, '#000', 0), (1, '#000', .7)])
    b = '<rect width="1920" height="1080" fill="url(#sky4)"/>' + starfield(rnd, 220, (0, 0, 1920, 1080))
    # a few planets (the worldline snakes through the solar system)
    b += '<circle cx="1660" cy="760" r="70" fill="#c8704a"/><circle cx="1636" cy="740" r="70" fill="#e8946a" opacity=".5"/>'
    b += '<circle cx="1000" cy="900" r="34" fill="#5a8ae8"/><path d="M970 890 q20 -10 40 4" stroke="#8ad86a" stroke-width="8" fill="none"/>'
    b += '<circle cx="1560" cy="120" r="44" fill="#d8b87a"/><ellipse cx="1560" cy="120" rx="80" ry="16" fill="none" stroke="#f2e0b0" stroke-width="5" transform="rotate(-18 1560 120)"/>'
    # worldline: a curve from bottom-left (infant) to top-right (now)
    def C(t):
        p0, p1, p2, p3 = (820, 900), (1150, 980), (1050, 380), (1480, 330)
        p4, p5 = (1760, 300), (1800, 140)
        if t < .6:
            u = t / .6
            return tuple((1 - u) ** 3 * a + 3 * (1 - u) ** 2 * u * b_ + 3 * (1 - u) * u * u * c + u ** 3 * e for a, b_, c, e in zip(p0, p1, p2, p3))
        u = (t - .6) / .4
        q1 = (2 * p3[0] - p2[0], 2 * p3[1] - p2[1])
        return tuple((1 - u) ** 3 * a + 3 * (1 - u) ** 2 * u * b_ + 3 * (1 - u) * u * u * c + u ** 3 * e for a, b_, c, e in zip(p3, q1, p4, p5))
    pts = [C(k / 120) for k in range(121)]
    path = 'M' + ' L'.join(f'{x:.1f} {y:.1f}' for x, y in pts)
    b += f'<path d="{path}" fill="none" stroke="#f2d27a" stroke-width="90" opacity=".25" filter="url(#b24)"/>'
    b += f'<path d="{path}" fill="none" stroke="url(#rib4)" stroke-width="18" stroke-linecap="round" opacity=".9"/>'
    # continuous stack of photo frames along the line (thin edges), then key photos
    def ang(k):
        (x0, y0), (x1, y1) = pts[max(0, k - 1)], pts[min(120, k + 1)]
        return math.degrees(math.atan2(y1 - y0, x1 - x0))
    for k in range(4, 118, 2):
        x, y = pts[k]; s = .55 + .55 * (1 - k / 120)
        b += (f'<rect x="{-40 * s:.1f}" y="{-50 * s:.1f}" width="{80 * s:.1f}" height="{100 * s:.1f}" rx="3" fill="#fff6e8" fill-opacity=".1" stroke="#fff0d8" stroke-width="2" opacity=".45" '
              f'transform="translate({x:.1f} {y:.1f}) rotate({ang(k) + 90:.1f}) skewY(-20)"/>')
    def kid(h, col):   # simple pictogram person of height h (0..1)
        hh = 60 * h
        return (f'<circle cx="0" cy="{24 - hh - 12:.1f}" r="{7 + 5 * h:.1f}" fill="{col}"/>'
                f'<path d="M{-9 - 6 * h:.1f} 26 Q{-9 - 6 * h:.1f} {26 - hh:.1f} 0 {26 - hh:.1f} Q{9 + 6 * h:.1f} {26 - hh:.1f} {9 + 6 * h:.1f} 26Z" fill="{col}"/>')
    keys = [(10, .25, '#f2a8c8', 'crib'), (36, .5, '#8ad8f2', ''), (62, .75, '#a8e88a', ''), (90, .95, '#f2c27a', ''), (116, 1, '#ffd0a0', '')]
    for k, h, col, extra in keys:
        x, y = pts[k]; s = 1.25 - .35 * k / 120
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
        g += '</g>'
        b += g
    # the bead of "now" sliding on the line
    bx, by = pts[100]
    b += ring_glow(int(bx), int(by), 70, '#ffffff', .5) + f'<circle cx="{bx:.0f}" cy="{by:.0f}" r="20" fill="#fff6d6" stroke="#f2d27a" stroke-width="5"/>'
    b += spark(1260, 220, 22, '#ffffff') + spark(1840, 420, 16) + spark(900, 760, 14)
    # frog photographer (camera) at the start of the line
    cam = ('<g transform="translate(56 -78) rotate(-12)"><rect x="-26" y="-18" width="52" height="36" rx="6" fill="#2a2a34" stroke-width="3.5"/>'
           '<rect x="-10" y="-26" width="20" height="10" rx="2" fill="#2a2a34" stroke-width="3"/><circle cx="0" cy="0" r="12" fill="#5a7ad8" stroke-width="3"/>'
           '<circle cx="-3" cy="-3" r="4" fill="#fff" stroke="none"/><circle cx="18" cy="-10" r="3.4" fill="#ff5a5a" stroke="none"/></g>')
    scarf = '<path d="M-30 -30 Q6 -18 44 -30 L46 -20 Q6 -6 -32 -20Z" fill="#e85a6a" stroke-width="3"/><path d="M30 -24 L40 2 L28 2 L22 -20Z" fill="#e85a6a" stroke-width="3"/>'
    b += '<ellipse cx="560" cy="1000" rx="140" ry="22" fill="#000" opacity=".45" filter="url(#b6)"/>'
    b += ring_glow(560, 900, 170, '#ff9ad0', .18)
    b += frog(560, 1000, 2.8, look=(9, -6), mouth='O', mid=scarf, front=cam,
              armL='M-34 -22 q-18 6 -20 26', armR='M38 -22 q14 -18 22 -46',
              legs=((-20, -6, -24, 4, -6), (20, -6, 24, 4, 6)))
    b += '<rect width="1920" height="1080" fill="url(#vig4)"/>'
    lines = [('STACK', 190, 'w'), ('EVERY', 190, 'w'), ('<span class="g">PHOTO</span>', 230, 'w')]
    return page('#0a0a2a', svg(d, b), lines, outline='#080418', top=36)


# ================= 5: BUILT FOR 3D ONLY =================
def make_5():
    rnd = random.Random(55)
    d = FILTERS + lin('sky5', [(0, '#3a1a4a'), (.45, '#d8603a'), (.8, '#f2a84a'), (1, '#f8d080')])
    d += '<radialGradient id="brain5" cx=".38" cy=".3" r=".85"><stop offset="0" stop-color="#ffd0dc"/><stop offset=".45" stop-color="#f08aa8"/><stop offset="1" stop-color="#b04a72"/></radialGradient>'
    d += rad('sun5', 1250, 560, 520, [(0, '#fff2b0', .95), (.25, '#ffd070', .7), (1, '#ff8a3a', 0)])
    d += rad('vig5', 960, 540, 1150, [(0, '#000', 0), (.65, '#000', 0), (1, '#1a0a10', .7)])
    b = '<rect width="1920" height="1080" fill="url(#sky5)"/><rect width="1920" height="1080" fill="url(#sun5)"/>'
    b += '<circle cx="1250" cy="600" r="250" fill="#ffe08a" opacity=".85"/>'
    # savannah horizon, acacias
    b += '<path d="M0 790 Q400 760 800 780 T1920 770 L1920 1080 L0 1080Z" fill="#6a3418"/>'
    b += '<path d="M0 830 Q500 800 1000 830 T1920 820 L1920 1080 L0 1080Z" fill="#3a1c0c"/>'
    def acacia(x, y, s):
        return (f'<g transform="translate({x} {y}) scale({s})" fill="#24100a"><path d="M-6 0 L-4 -120 Q-30 -150 -60 -160 L-56 -166 Q-24 -156 0 -132 Q20 -160 50 -168 L52 -162 Q24 -150 6 -120 L8 0Z"/>'
                f'<ellipse cx="0" cy="-176" rx="130" ry="26"/><ellipse cx="-60" cy="-168" rx="70" ry="18"/><ellipse cx="70" cy="-170" rx="70" ry="16"/></g>')
    b += acacia(1720, 790, 1.4) + acacia(860, 790, .7) + acacia(1900, 780, .8)
    for k in range(5):   # birds
        x, y = 1500 + k * 46, 320 + (k % 2) * 30
        b += f'<path d="M{x - 12} {y} q6 -8 12 0 q6 -8 12 0" fill="none" stroke="#3a1a1a" stroke-width="3"/>'
    # the brain
    bx, by = 1330, 580
    b += f'<ellipse cx="{bx}" cy="{by + 300}" rx="300" ry="34" fill="#1a0a06" opacity=".55" filter="url(#b12)"/>'
    b += f'<path d="M{bx + 120} {by + 170} Q{bx + 140} {by + 260} {bx + 110} {by + 300} L{bx + 60} {by + 300} Q{bx + 80} {by + 250} {bx + 60} {by + 180}Z" fill="#c8607a" stroke="#4a1428" stroke-width="6"/>'
    b += f'<ellipse cx="{bx + 190}" cy="{by + 150}" rx="110" ry="70" fill="#d8708e" stroke="#4a1428" stroke-width="6"/>'
    for k in range(-3, 4):
        b += f'<path d="M{bx + 110} {by + 150 + k * 16} Q{bx + 190} {by + 140 + k * 18} {bx + 280} {by + 150 + k * 14}" fill="none" stroke="#9a3a5a" stroke-width="3"/>'
    lobes = [(0, -30, 300, 210)] + [(bx_ - bx, by_ - by, 80, 70) for bx_, by_ in []]
    blob = f'<ellipse cx="{bx}" cy="{by - 20}" rx="320" ry="215"/>'
    for a in range(0, 360, 24):
        r = math.radians(a)
        blob += f'<circle cx="{bx + 290 * math.cos(r):.0f}" cy="{by - 20 + 190 * math.sin(r):.0f}" r="62"/>'
    d += f'<clipPath id="bclip5">{blob}</clipPath>'
    b += f'<g stroke="#4a1428" stroke-width="14">{blob}</g>'.replace('<ellipse', '<ellipse fill="#4a1428"').replace('<circle', '<circle fill="#4a1428"')
    b += f'<g fill="url(#brain5)" clip-path="url(#bclip5)"><rect x="{bx - 400}" y="{by - 300}" width="800" height="560"/>'
    for j in range(10):   # gyri: rows of sinuous folds
        y0 = by - 230 + j * 46; ph = rnd.uniform(0, 6.28); amp = rnd.uniform(12, 20)
        pts_ = [(x, y0 + amp * math.sin(x / 34 + ph) + 8 * math.sin(x / 13 + j)) for x in range(bx - 360, bx + 361, 12)]
        dd = 'M' + ' L'.join(f'{x:.0f} {y:.0f}' for x, y in pts_)
        b += f'<path d="{dd}" fill="none" stroke="#a8406a" stroke-width="8" stroke-linecap="round" stroke-linejoin="round"/>'
        b += f'<path d="{dd}" fill="none" stroke="#ffd8e4" stroke-width="3" opacity=".5" transform="translate(-2 -7)"/>'
    b += f'<path d="M{bx - 330} {by - 10} Q{bx - 100} {by + 50} {bx + 140} {by - 30}" fill="none" stroke="#7a2448" stroke-width="10"/>'
    b += f'<ellipse cx="{bx - 120}" cy="{by - 150}" rx="120" ry="50" fill="#fff" opacity=".35" filter="url(#b12)"/></g>'
    # a hypercube (cube inside cube + 8 struts) hovering above, short-circuiting the brain
    sp, ed = tess_screen(0.0, 0.55, -0.4, 1600, 250, 140, d4=3.0)
    b += ring_glow(1600, 250, 200, '#8af0ff', .45)
    b += tess_draw(sp, ed, '#8af0ff', '#5ac8ff', '#c89aff', w=6, gcol='#5ac8ff', core='#ffffff')
    for ang, L in ((2.5, 260), (2.1, 230), (2.9, 240)):
        b += f'<polyline points="{jag(rnd, 1520, 330, ang, L, 7, 20)}" fill="none" stroke="#bff8ff" stroke-width="7" stroke-linejoin="round" opacity=".95"/>'
        b += f'<polyline points="{jag(rnd, 1520, 330, ang, L, 7, 20)}" fill="none" stroke="#5ae8ff" stroke-width="16" opacity=".4" filter="url(#b6)"/>'
    for x, y in ((1330, 380), (1440, 440), (1260, 420)):
        b += spark(x, y, 26, '#ffffff', .95)
    for k in range(3):   # smoke wisps
        x = 1060 + k * 110
        b += f'<path d="M{x} 360 q-30 -50 0 -90 q30 -40 0 -90" fill="none" stroke="#5a4a5a" stroke-width="{22 - k * 4}" stroke-linecap="round" opacity=".45" filter="url(#b6)"/>'
    # frog in a safari hat peeking out of the tall grass, a snake nearby
    hat = ('<path d="M-46 -78 Q6 -92 58 -78 Q60 -70 6 -72 Q-46 -70 -46 -78Z" fill="#c8a060" stroke-width="3.2"/>'
           '<path d="M-26 -78 Q-24 -112 6 -114 Q38 -112 40 -78Z" fill="#d8b878" stroke-width="3.2"/><path d="M-26 -84 L40 -84" stroke="#7a4a20" stroke-width="6"/>')
    b += frog(600, 1000, 2.9, look=(9, -6), mouth='O', front=hat, brows=False,
              armL='M-34 -22 q-10 -8 -12 -18', armR='M38 -22 q10 -8 12 -18')
    b += '<path d="M330 1040 C380 980 420 1040 470 990 C510 950 540 990 520 1020" fill="none" stroke="#2a3a10" stroke-width="22" stroke-linecap="round"/>'
    b += '<path d="M330 1040 C380 980 420 1040 470 990 C510 950 540 990 520 1020" fill="none" stroke="#6a8a2a" stroke-width="13" stroke-linecap="round"/>'
    b += '<circle cx="520" cy="1018" r="16" fill="#6a8a2a" stroke="#2a3a10" stroke-width="5"/><circle cx="524" cy="1012" r="4" fill="#fff"/><path d="M534 1024 l14 4 m-14 -4 l12 -4" stroke="#d83a3a" stroke-width="3"/>'
    for k in range(70):   # tall grass in front
        x = rnd.uniform(250, 980); h = rnd.uniform(90, 200)
        col = rnd.choice(['#8a6a2a', '#a8803a', '#6a4a1a', '#c89a4a'])
        b += f'<path d="M{x:.0f} 1080 Q{x + rnd.uniform(-10, 10):.0f} {1080 - h * .6:.0f} {x + rnd.uniform(-30, 30):.0f} {1080 - h:.0f}" fill="none" stroke="{col}" stroke-width="{rnd.uniform(4, 8):.1f}" stroke-linecap="round"/>'
    b += '<rect width="1920" height="1080" fill="url(#vig5)"/>'
    lines = [('BUILT FOR', 180, 'w'), ('<span class="g">3D</span> ONLY', 230, 'w')]
    return page('#3a1a4a', svg(d, b), lines, outline='#1a0608', top=52)


for n, fn in enumerate((make_1, make_2, make_3, make_4, make_5), 1):
    out = os.path.join(REPO, 'videos', f'fourth-dimension-short{n}', 'thumb')
    os.makedirs(out, exist_ok=True)
    for f in ('common.css', 'Fredoka-700.woff2'):
        shutil.copy(os.path.join(HERE, f), out)
    open(os.path.join(out, 'A.html'), 'w').write(fn())
print('ok')
