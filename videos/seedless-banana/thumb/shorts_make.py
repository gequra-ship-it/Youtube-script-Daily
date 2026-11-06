# Shorts thumbnails (guideline 16-9): one A.html per short -> videos/seedless-banana-shortN/thumb/A.html. Run: python3 videos/seedless-banana/thumb/shorts_make.py
# Reuses frog()/banana()/leaf() from make.py (long thumbs A=TR4 Alien egg, B=wild seeds, C=radioactive) without re-writing those pages.
# short1  3 SETS = / SEEDLESS        intuitive: big seedless banana + 2 chromosomes and a glowing 3rd one; lab frog. Script: "three sets of chromosomes instead of two" ... "soft, pillowy, seedless fruit".
# short2  ALREADY / EXTINCT / ONCE   intuitive: tombstone "R.I.P. BIG MIKE" among wilted plantations; mourning frog. Script: "already experienced a ... banana extinction once before"; Gros Michel "Big Mike".
# short3  SAVED BY / A DUKE          intuitive: glowing Victorian greenhouse with a banana plant at night; frog in top hat + monocle. Script: "salvation ... came from ... the private greenhouse of an English aristocrat" (Duke of Devonshire).
# short4  A BANANA / IS A / BERRY    intuitive: banana lying in a "BERRIES" crate, strawberry and raspberry tumbling out; frog with magnifier. Script: "a banana is a berry, but a strawberry is not ... raspberries fail".
# short5  NOT A / TREE!              intuitive: cutaway banana plant: pseudostem slice with onion rings, underground corm with pups; miner frog. Script: "not a tree", "pseudostem", "layers of an onion", "corm", "suckers or pups".
import os, sys, math, random, shutil
HERE = os.path.dirname(os.path.abspath(__file__))
VID = os.path.dirname(os.path.dirname(HERE))
src = open(os.path.join(HERE, 'make.py')).read()
src = src.split('# ================= A:')[0]
exec(src + '\n' + open(os.path.join(HERE, 'make.py')).read().split('def make_B')[0].split('def leaf')[0][:0] + 'def leaf' + open(os.path.join(HERE, 'make.py')).read().split('def leaf')[1].split('def make_B')[0])  # frog, banana, frame, off, leaf, FILTERS, P, page, svg, lin, rad, spark, INK, GREEN

RIPE = ('#d89a1a', '#f6c932', '#fff08a', '#fff8c8')
VIG = lambda i, c='#000', a=.75: rad(i, 960, 540, 1150, [(0, c, 0), (.62, c, 0), (1, c, a)])


def chrom(x, y, s, rot, col, dark, glow=None):
    """X-shaped chromosome: two banded chromatids crossing at the centromere."""
    o = f'<g transform="translate({x} {y}) rotate({rot}) scale({s})">'
    if glow:
        o += f'<circle r="120" fill="{glow}" opacity=".55" filter="url(#b26)"/>'
    for a in (-24, 24):
        o += (f'<g transform="rotate({a})"><rect x="-26" y="-110" width="52" height="220" rx="26" fill="{col}" stroke="#1a1030" stroke-width="7"/>'
              f'<rect x="-14" y="-98" width="12" height="196" rx="6" fill="#fff" opacity=".35"/>')
        for by in (-70, -40, 38, 72):
            o += f'<rect x="-24" y="{by}" width="48" height="9" fill="{dark}" opacity=".55"/>'
        o += '</g>'
    o += f'<ellipse rx="22" ry="14" fill="{dark}" stroke="#1a1030" stroke-width="5"/></g>'
    return o


def short1():
    rnd = random.Random(11)
    d = FILTERS + lin('bg1', [(0, '#0f2c44'), (.6, '#1b1a4a'), (1, '#0a0a20')])
    d += rad('halo1', 1250, 660, 640, [(0, '#ffe68a', .55), (.4, '#f2b23a', .18), (1, '#000', 0)])
    d += rad('gold1', 1690, 270, 260, [(0, '#fff6c0', .9), (.4, '#f2d27a', .35), (1, '#f2d27a', 0)])
    d += lin('table1', [(0, '#24305a'), (1, '#0c1028')]) + VIG('vig1', '#05061a', .8)
    b = '<rect width="1920" height="1080" fill="url(#bg1)"/>'
    # soft DNA-ish background helix lines
    for k in range(2):
        pts = [(x, 140 + k * 60 + 60 * math.sin(x / 120 + k * math.pi)) for x in range(900, 1940, 20)]
        b += f'<polyline points="{P(pts)}" fill="none" stroke="#5ad0ff" stroke-width="4" opacity=".18"/>'
    b += '<rect width="1920" height="1080" fill="url(#halo1)"/>'
    b += '<path d="M0 860 L1920 840 L1920 1080 L0 1080Z" fill="url(#table1)"/><path d="M0 860 L1920 840" stroke="#6a7ad0" stroke-width="4" opacity=".5"/>'
    # banana on the table
    b += '<ellipse cx="1180" cy="880" rx="430" ry="40" fill="#000" opacity=".5" filter="url(#b14)"/>'
    p = ((700, 700), (900, 900), (1380, 930), (1640, 640))
    art, F = banana(p, 150, RIPE, line='#3a1c04', lw=7, stem=True, spots=10, rnd=rnd, glow='#ffd84a')
    b += art
    # chromosomes: two plain + the extra glowing gold one
    b += '<rect width="1920" height="1080" fill="url(#gold1)"/>'
    b += chrom(1230, 330, 1.05, -12, '#ff8fc8', '#b0407a')
    b += chrom(1480, 250, 1.05, 10, '#7ac8ff', '#2a6aa8')
    b += chrom(1730, 320, 1.25, -6, '#ffe070', '#c08a10', glow='#fff2a0')
    b += spark(1800, 150, 26, '#fffbe0') + spark(1580, 420, 18) + spark(1090, 470, 16, '#ffe9ff') + spark(1760, 470, 14)
    for _ in range(40):
        b += f'<circle cx="{rnd.uniform(950, 1900):.0f}" cy="{rnd.uniform(40, 800):.0f}" r="{rnd.choice([1.5, 2.2, 3])}" fill="#fff4c8" opacity="{rnd.uniform(.2, .7):.2f}"/>'
    # lab frog pointing up at the third chromosome
    coat = ('<path d="M-36 -40 Q-44 -6 -36 4 L-4 4 L-2 -34 Z" fill="#f2f0f8" stroke-width="3.4"/>'
            '<path d="M44 -40 Q52 -6 46 4 L14 4 L12 -34 Z" fill="#f2f0f8" stroke-width="3.4"/>')
    goggles = ('<path d="M-30 -94 Q6 -104 42 -94" fill="none" stroke="#2a2a3a" stroke-width="6"/>'
               '<ellipse cx="-6" cy="-96" rx="14" ry="10" fill="#9ae8ff" stroke-width="3.4"/><ellipse cx="24" cy="-96" rx="14" ry="10" fill="#9ae8ff" stroke-width="3.4"/>')
    b += '<circle cx="420" cy="820" r="170" fill="#9ae8ff" opacity=".14" filter="url(#b50)"/>'
    b += frog(420, 1000, 2.8, rot=3, look=(10, -9), mouth='O', shadow=True, mid=coat, top=goggles,
              armL='M-34 -22 q-18 4 -22 22', armR='M38 -22 q26 -24 30 -66')
    b += '<rect width="1920" height="1080" fill="url(#vig1)"/>'
    return page('#0f2c44', svg(d, b), [('3 SETS =', 150, 'w'), ('SEEDLESS', 190, 'y')], outline='#060a1c', top=44)


def dead_plant(x, y, h, rnd, col='#4a3a26', leafc='#6a5430'):
    o = f'<path d="M{x - 26} {y} L{x - 16} {y - h} L{x + 16} {y - h} L{x + 26} {y}Z" fill="{col}"/>'
    for a, L in ((-150, 260), (-30, 240), (-110, 200), (160, 210), (20, 230)):
        rr = math.radians(a); ex, ey = x + math.cos(rr) * L * .6, y - h + math.sin(rr) * L * .4
        o += f'<path d="M{x} {y - h} Q{ex:.0f} {ey - 40:.0f} {ex + math.cos(rr) * 40:.0f} {ey + 140 + rnd.uniform(0, 60):.0f}" fill="none" stroke="{leafc}" stroke-width="{rnd.uniform(26, 38):.0f}" stroke-linecap="round"/>'
    return o


def short2():
    rnd = random.Random(22)
    d = FILTERS + lin('sky2', [(0, '#1c1630'), (.55, '#4a2e4e'), (.8, '#c0604a'), (1, '#e89a5a')])
    d += rad('sun2', 1300, 760, 520, [(0, '#ffd890', .9), (.35, '#f29a5a', .35), (1, '#f29a5a', 0)])
    d += lin('stone2', [(0, '#a8a8b4'), (.5, '#7a7a88'), (1, '#4a4a58')], x2=1, y2=.3)
    d += lin('ground2', [(0, '#2a1e22'), (1, '#0c080a')]) + VIG('vig2', '#08040a', .8)
    b = '<rect width="1920" height="1080" fill="url(#sky2)"/><rect width="1920" height="1080" fill="url(#sun2)"/>'
    b += ''.join(f'<circle cx="{rnd.uniform(900, 1900):.0f}" cy="{rnd.uniform(20, 380):.0f}" r="{rnd.choice([1.4, 2, 2.6])}" fill="#ffe8f0" opacity="{rnd.uniform(.2, .6):.2f}"/>' for _ in range(40))
    # rows of wilted plantation silhouettes on the horizon
    far = ''.join(dead_plant(x, 790, rnd.uniform(140, 200), rnd, '#3a2632', '#4a2e3a') for x in range(900, 1960, 170))
    b += f'<g opacity=".75" transform="translate(0 0) scale(1)">{far}</g>'
    b += dead_plant(1820, 840, 420, rnd, '#2a1c1e', '#3a2a22') + dead_plant(880, 830, 360, rnd, '#2a1c1e', '#3a2a22')
    b += '<path d="M0 800 Q900 760 1920 810 L1920 1080 L0 1080Z" fill="url(#ground2)"/>'
    # tombstone
    b += '<ellipse cx="1310" cy="905" rx="360" ry="40" fill="#000" opacity=".55" filter="url(#b14)"/>'
    b += '<path d="M1065 900 L1065 470 Q1065 300 1310 300 Q1555 300 1555 470 L1555 900Z" fill="#2a2a34" transform="translate(16 10)"/>'
    b += '<path d="M1065 900 L1065 470 Q1065 300 1310 300 Q1555 300 1555 470 L1555 900Z" fill="url(#stone2)" stroke="#1a1a22" stroke-width="10" stroke-linejoin="round"/>'
    b += '<path d="M1090 470 Q1090 326 1310 326" fill="none" stroke="#fff" stroke-width="10" opacity=".35" stroke-linecap="round"/>'
    b += '<path d="M1530 520 l-30 50 l20 30 l-26 60" fill="none" stroke="#2a2a34" stroke-width="5"/>'
    b += ''.join(f'<ellipse cx="{x}" cy="{y}" rx="{r}" ry="{r * .6:.0f}" fill="#5a7a3a" opacity=".85"/>' for x, y, r in ((1080, 880, 34), (1120, 892, 26), (1540, 884, 30), (1080, 600, 14)))
    # carved banana relief + inscription
    p = ((1200, 470), (1240, 560), (1380, 570), (1440, 450))
    F = frame(p, 46)
    b += f'<path d="M{P(off(F, 1))} L{P(off(F, -1)[::-1])}Z" fill="#5a5a68" stroke="#2a2a34" stroke-width="6" transform="translate(4 5)"/>'
    b += f'<path d="M{P(off(F, 1))} L{P(off(F, -1)[::-1])}Z" fill="#9a9aa8" stroke="#4a4a58" stroke-width="5"/>'
    b += ('<text x="1310" y="690" text-anchor="middle" font-family="Fredoka" font-weight="700" font-size="86" fill="#3a3a46" stroke="#cfcfd8" stroke-width="2">R.I.P.</text>'
          '<text x="1310" y="800" text-anchor="middle" font-family="Fredoka" font-weight="700" font-size="84" fill="#3a3a46" stroke="#cfcfd8" stroke-width="2">BIG MIKE</text>')
    # grave mound with an old spotted banana + flowers
    b += '<path d="M1090 960 Q1310 880 1530 960Z" fill="#3a2a22" stroke="#1a1010" stroke-width="5"/>'
    art, _ = banana(((1230, 930), (1270, 965), (1380, 960), (1420, 915)), 30, ('#8a6a1a', '#c8a03a', '#e8c86a', '#f0d890'), line='#2a1804', lw=4, stem=True, spots=12, rnd=rnd)
    b += art
    for x, c in ((1160, '#f2d27a'), (1190, '#ff8a9a'), (1470, '#f2d27a')):
        b += f'<path d="M{x} 950 q-4 -30 2 -50" stroke="#4a7a3a" stroke-width="5" fill="none"/>'
        b += ''.join(f'<circle cx="{x + 2 + 10 * math.cos(a):.0f}" cy="{898 + 10 * math.sin(a):.0f}" r="8" fill="{c}"/>' for a in (0, 1.26, 2.51, 3.77, 5.03)) + f'<circle cx="{x + 2}" cy="898" r="6" fill="#fff6c0"/>'
    b += spark(1600, 330, 22, '#fff0e0') + spark(1020, 420, 14)
    # mourning frog with bowler hat and a flower
    hat = ('<g transform="translate(6 -88) rotate(-6)"><ellipse cx="0" cy="6" rx="44" ry="9" fill="#1a1a1a" stroke-width="3.4"/>'
           '<path d="M-26 6 Q-28 -34 0 -34 Q28 -34 26 6Z" fill="#2a2a2a" stroke-width="3.4"/><path d="M-26 0 L26 0" stroke="#8a2a3a" stroke-width="6"/></g>')
    flower = ('<path d="M54 -60 q4 -30 -2 -56" stroke="#4a7a3a" stroke-width="3" fill="none"/>'
              + ''.join(f'<circle cx="{52 + 7 * math.cos(a):.1f}" cy="{-120 + 7 * math.sin(a):.1f}" r="6" fill="#ff8a9a" stroke-width="2"/>' for a in (0, 1.26, 2.51, 3.77, 5.03)) + '<circle cx="52" cy="-120" r="4" fill="#fff6c0" stroke="none"/>')
    tear = '<path d="M-12 -50 q-4 8 0 12 q4 -4 0 -12z" fill="#9ae8ff" stroke="none"/>'
    b += '<circle cx="760" cy="860" r="150" fill="#ffd0a0" opacity=".12" filter="url(#b50)"/>'
    b += frog(760, 1010, 2.6, rot=2, look=(12, -4), mouth='o', shadow=True, top=hat + tear, brows=True,
              armL='M-34 -22 q-18 4 -22 22', armR='M38 -22 q18 -10 16 -40', front=flower)
    b += '<rect width="1920" height="1080" fill="url(#vig2)"/>'
    return page('#1c1630', svg(d, b), [('ALREADY', 124, 'w'), ('EXTINCT', 200, 'y'), ('ONCE', 124, 'w')], outline='#0c0614', top=40)


def short3():
    rnd = random.Random(33)
    d = FILTERS + lin('sky3', [(0, '#06102a'), (.7, '#13285a'), (1, '#1e3a6a')])
    d += rad('glow3', 1310, 560, 620, [(0, '#ffe2a0', .65), (.4, '#f2b04a', .25), (1, '#f2b04a', 0)])
    d += lin('in3', [(0, '#fff2c0'), (1, '#f2b84a')])
    d += lin('lawn3', [(0, '#183a24'), (1, '#06120a')]) + VIG('vig3', '#02060e', .8)
    b = '<rect width="1920" height="1080" fill="url(#sky3)"/>'
    b += ''.join(f'<circle cx="{rnd.uniform(0, 1920):.0f}" cy="{rnd.uniform(10, 520):.0f}" r="{rnd.choice([1.3, 1.9, 2.6])}" fill="#e8f0ff" opacity="{rnd.uniform(.2, .8):.2f}"/>' for _ in range(110))
    b += '<circle cx="1760" cy="140" r="58" fill="#fff6dc" opacity=".95"/><circle cx="1760" cy="140" r="110" fill="#fff6dc" opacity=".15" filter="url(#b26)"/>'
    b += '<rect width="1920" height="1080" fill="url(#glow3)"/>'
    b += '<path d="M0 840 Q900 800 1920 850 L1920 1080 L0 1080Z" fill="url(#lawn3)"/>'
    # dark trees either side for depth
    for x, h in ((870, 300), (1760, 360)):
        b += f'<rect x="{x - 12}" y="{850 - h * .4:.0f}" width="24" height="{h * .4:.0f}" fill="#0a1a12"/>'
        b += ''.join(f'<circle cx="{x + dx}" cy="{850 - h * .45 - dy:.0f}" r="{r}" fill="#0c2216"/>' for dx, dy, r in ((-60, 60, 80), (50, 70, 90), (0, 150, 100), (-30, 230, 70), (40, 230, 60)))
    # glasshouse: wings + central dome
    gh = ''
    body = 'M1000 860 L1000 560 Q1000 520 1040 520 L1580 520 Q1620 520 1620 560 L1620 860Z'
    dome = 'M1150 520 Q1150 250 1310 220 Q1470 250 1470 520Z'
    gh += f'<path d="{body}" fill="url(#in3)" opacity=".92"/><path d="{dome}" fill="url(#in3)" opacity=".95"/>'
    # banana plant inside, silhouetted green against the glow
    plant = '<path d="M1290 860 L1296 460 L1326 460 L1332 860Z" fill="#3a6a2a"/>'
    for x, y, L, a in ((1310, 470, 300, -150), (1310, 470, 300, -30), (1310, 450, 260, -105), (1310, 450, 250, -70), (1310, 500, 280, 175), (1310, 500, 280, 5)):
        plant += leaf(x, y, L, a, '#3f8a30', '#24501a', .2)
    for k in range(5):
        bx, by = 1340, 560 + k * 26
        plant += f'<path d="M{bx} {by} q30 -6 50 -40" fill="none" stroke="#c8d43a" stroke-width="18" stroke-linecap="round"/><path d="M{bx} {by} q30 -6 50 -40" fill="none" stroke="#2a3a08" stroke-width="2" opacity=".5"/>'
    plant += '<path d="M1340 540 L1350 700" stroke="#6a5a2a" stroke-width="8"/><ellipse cx="1352" cy="720" rx="16" ry="24" fill="#7a2a4a"/>'
    gh += f'<g opacity=".95">{plant}</g>'
    # glazing bars
    bars = ''
    for x in range(1000, 1621, 62):
        bars += f'<line x1="{x}" y1="520" x2="{x}" y2="860"/>'
    bars += '<line x1="1000" y1="690" x2="1620" y2="690"/><line x1="1000" y1="600" x2="1620" y2="600"/>'
    for k in range(-4, 5):
        bars += f'<path d="M{1310 + k * 40} 520 Q{1310 + k * 34} 330 1310 222" fill="none"/>'
    for y in (300, 380, 450):
        bars += f'<path d="M{1310 - (y - 200) * 1.4:.0f} {y} Q1310 {y - 40} {1310 + (y - 200) * 1.4:.0f} {y}" fill="none"/>'
    gh += f'<g stroke="#f8f0e0" stroke-width="5" opacity=".85">{bars}</g>'
    gh += f'<path d="{body}" fill="none" stroke="#e8e0d0" stroke-width="10"/><path d="{dome}" fill="none" stroke="#e8e0d0" stroke-width="10"/>'
    gh += '<path d="M1310 222 L1310 180" stroke="#e8e0d0" stroke-width="8"/><circle cx="1310" cy="174" r="12" fill="#f2d27a" stroke="#8a6a2a" stroke-width="3"/>'
    gh += '<path d="M1270 860 L1270 760 Q1310 720 1350 760 L1350 860Z" fill="#fff6d0" stroke="#e8e0d0" stroke-width="8"/>'
    gh += '<path d="M1000 860 L1620 860" stroke="#c8bca0" stroke-width="16"/>'
    b += '<ellipse cx="1310" cy="620" rx="420" ry="360" fill="#ffe2a0" opacity=".18" filter="url(#b50)"/>' + gh
    # light spilling on the lawn
    b += '<path d="M1270 868 L1350 868 L1460 1080 L1160 1080Z" fill="#ffe2a0" opacity=".22"/>'
    b += spark(1520, 300, 22, '#fffbe0') + spark(1100, 420, 16) + spark(1650, 470, 14)
    # duke frog: top hat, monocle, holding a banana
    hat = ('<g transform="translate(6 -92) rotate(-5)"><ellipse cx="0" cy="8" rx="44" ry="9" fill="#141414" stroke-width="3.4"/>'
           '<rect x="-26" y="-58" width="52" height="66" rx="5" fill="#1e1e22" stroke-width="3.4"/><rect x="-26" y="-6" width="52" height="10" fill="#7a2a3a" stroke-width="2"/>'
           '<path d="M-18 -50 L-18 -14" stroke="#fff" stroke-width="4" opacity=".35"/></g>')
    mono = '<circle cx="22" cy="-66" r="16" fill="none" stroke="#f2d27a" stroke-width="3.4"/><path d="M36 -60 q10 20 2 44" fill="none" stroke="#f2d27a" stroke-width="2"/>'
    bow = '<path d="M-6 -24 L-20 -32 L-20 -16Z M18 -24 L32 -32 L32 -16Z" fill="#7a2a3a" stroke-width="2.6"/><circle cx="6" cy="-24" r="5" fill="#7a2a3a" stroke-width="2.4"/>'
    ban, _ = banana(((48, -64), (58, -110), (90, -140), (118, -140)), 11, RIPE, line=INK, lw=2.6, stem=True)
    b += '<circle cx="760" cy="860" r="170" fill="#ffe2a0" opacity=".14" filter="url(#b50)"/>'
    b += frog(760, 1010, 2.8, rot=-2, look=(12, -6), mouth='O', shadow=True, mid=bow, top=mono + hat, brows=True,
              armL='M-34 -22 q-18 4 -22 22', armR='M38 -22 q16 -14 14 -42', front=ban)
    b += '<rect width="1920" height="1080" fill="url(#vig3)"/>'
    return page('#06102a', svg(d, b), [('SAVED BY', 136, 'w'), ('A DUKE', 220, 'y')], outline='#040818', top=44)


def strawberry(x, y, s, rot):
    o = f'<g transform="translate({x} {y}) rotate({rot}) scale({s})" stroke="#3a0810" stroke-width="5" stroke-linejoin="round">'
    o += '<path d="M0 -60 Q60 -64 62 -10 Q58 50 0 80 Q-58 50 -62 -10 Q-60 -64 0 -60Z" fill="#e8343a"/>'
    o += '<path d="M-40 -30 Q-44 10 -20 50" fill="none" stroke="#ff8a8a" stroke-width="8" opacity=".7"/>'
    o += ''.join(f'<ellipse cx="{sx}" cy="{sy}" rx="3.4" ry="5" fill="#f8e070" stroke="none"/>' for sx, sy in ((-30, -20), (0, -30), (30, -20), (-20, 10), (14, 6), (40, 14), (-36, 26), (0, 36), (24, 42), (-10, 60)))
    o += '<path d="M0 -60 L-40 -78 L-14 -66 L-20 -92 L0 -70 L20 -92 L14 -66 L40 -78Z" fill="#4aa040"/></g>'
    return o


def raspberry(x, y, s, rot):
    o = f'<g transform="translate({x} {y}) rotate({rot}) scale({s})" stroke="#3a0820" stroke-width="3">'
    for r, n, yy in ((0, 1, -30), (20, 5, -10), (26, 6, 14), (18, 5, 36)):
        for k in range(n):
            a = k / n * 2 * math.pi
            o += f'<circle cx="{r * math.cos(a):.0f}" cy="{yy + r * .3 * math.sin(a):.0f}" r="14" fill="#d8285a"/>'
    o += '<path d="M0 -44 L-16 -56 M0 -44 L16 -56 M0 -44 L0 -60" stroke="#4aa040" stroke-width="6"/></g>'
    return o


def short4():
    rnd = random.Random(44)
    d = FILTERS + lin('bg4', [(0, '#4a0e30'), (.6, '#7a1a44'), (1, '#2a0618')])
    d += rad('spot4', 1240, 560, 640, [(0, '#ffe8a0', .6), (.4, '#ff9a6a', .2), (1, '#000', 0)])
    d += lin('wood4', [(0, '#c8884a'), (1, '#7a4a22')]) + lin('woodS', [(0, '#8a5a2a'), (1, '#4a2a12')])
    d += lin('floor4', [(0, '#3a0a22'), (1, '#12030a')]) + VIG('vig4', '#12030a', .8)
    b = '<rect width="1920" height="1080" fill="url(#bg4)"/>'
    b += ''.join(f'<circle cx="{rnd.uniform(800, 1900):.0f}" cy="{rnd.uniform(0, 700):.0f}" r="{rnd.uniform(20, 70):.0f}" fill="#ff7aa8" opacity="{rnd.uniform(.04, .12):.2f}"/>' for _ in range(18))
    b += '<rect width="1920" height="1080" fill="url(#spot4)"/>'
    b += '<path d="M0 860 L1920 840 L1920 1080 L0 1080Z" fill="url(#floor4)"/>'
    # crate (back wall, banana, front face)
    b += '<ellipse cx="1240" cy="880" rx="420" ry="40" fill="#000" opacity=".55" filter="url(#b14)"/>'
    b += '<path d="M920 640 L980 560 L1560 560 L1620 640Z" fill="url(#woodS)" stroke="#2a1606" stroke-width="7" stroke-linejoin="round"/>'
    art, _ = banana(((860, 560), (1030, 720), (1480, 720), (1720, 360)), 140, RIPE, line='#3a1c04', lw=7, stem=True, spots=8, rnd=rnd, glow='#ffd84a')
    b += art
    face = '<path d="M920 640 L1620 640 L1600 880 L940 880Z" fill="url(#wood4)" stroke="#2a1606" stroke-width="8" stroke-linejoin="round"/>'
    for y in (700, 760, 820):
        face += f'<path d="M{928 + (y - 640) * .08:.0f} {y} L{1612 - (y - 640) * .08:.0f} {y}" stroke="#5a3214" stroke-width="5" opacity=".7"/>'
    face += '<path d="M940 650 L1600 650" stroke="#f0c088" stroke-width="6" opacity=".6"/>'
    face += '<rect x="1090" y="700" width="360" height="110" rx="14" fill="#f8ecd0" stroke="#2a1606" stroke-width="6"/>'
    face += '<text x="1270" y="782" text-anchor="middle" font-family="Fredoka" font-weight="700" font-size="76" fill="#8a1a3a">BERRIES</text>'
    for x, y in ((960, 668), (1580, 668), (972, 856), (1568, 856)):
        face += f'<circle cx="{x}" cy="{y}" r="7" fill="#3a2a1a"/>'
    b += face
    b += '<circle cx="1660" cy="300" r="100" fill="#fff6c0" opacity=".25" filter="url(#b26)"/>'
    # gold rosette on the banana: winner
    b += '<g transform="translate(1290 600)"><path d="M-22 10 L-34 70 L-10 56 L0 80 L10 20Z M22 10 L34 70 L10 56 L0 80 L-10 20Z" fill="#c03a4a" stroke="#3a0810" stroke-width="4"/>'
    b += ''.join(f'<circle cx="{34 * math.cos(a * math.pi / 6):.0f}" cy="{34 * math.sin(a * math.pi / 6):.0f}" r="14" fill="#f2d27a" stroke="#8a6a1a" stroke-width="3"/>' for a in range(12))
    b += '<circle r="32" fill="#f2d27a" stroke="#8a6a1a" stroke-width="4"/><path d="M-14 -4 L-4 8 L16 -12" fill="none" stroke="#8a1a3a" stroke-width="7" stroke-linecap="round"/></g>'
    # strawberry + raspberry tumbling out of the crate
    b += strawberry(820, 640, 1.25, -38) + raspberry(700, 770, 1.0, 30)
    for k in range(3):
        b += f'<path d="M{900 - k * 14} {560 + k * 30} q-30 10 -50 40" fill="none" stroke="#ffd0d8" stroke-width="5" stroke-linecap="round" opacity="{.7 - k * .18:.2f}"/>'
    b += spark(1780, 220, 26, '#fffbe0') + spark(1500, 470, 18) + spark(1060, 500, 16, '#ffe9ff')
    # detective frog with magnifier
    glass = ('<g transform="translate(70 -108) rotate(-20)"><rect x="-6" y="30" width="12" height="54" rx="5" fill="#7a4a22" stroke-width="3"/>'
             '<circle r="32" fill="#cfefff" fill-opacity=".35" stroke="#c8a040" stroke-width="7"/><path d="M-16 -14 q8 -10 20 -10" stroke="#fff" stroke-width="4" fill="none"/></g>')
    cap = ('<g transform="translate(6 -90) rotate(-8)"><path d="M-36 6 Q-34 -30 0 -32 Q34 -30 36 6Z" fill="#a07a4a" stroke-width="3.4"/>'
           '<path d="M-36 6 L-58 10 L-36 -2Z M36 6 L58 10 L36 -2Z" fill="#8a6a3a" stroke-width="3"/><path d="M-30 -8 L30 -8 M-26 -20 L26 -20" stroke="#6a4a2a" stroke-width="2.4"/></g>')
    b += '<circle cx="400" cy="840" r="160" fill="#ffe8a0" opacity=".12" filter="url(#b50)"/>'
    b += frog(400, 1000, 2.7, rot=3, look=(11, -6), mouth='O', shadow=True, top=cap, brows=True,
              armL='M-34 -22 q-18 4 -22 22', armR='M38 -22 q22 -14 26 -40', front=glass)
    b += '<rect width="1920" height="1080" fill="url(#vig4)"/>'
    return page('#4a0e30', svg(d, b), [('A BANANA', 124, 'w'), ('IS A', 112, 'w'), ('BERRY', 236, 'y')], outline='#1a0410', top=36)


def short5():
    rnd = random.Random(55)
    d = FILTERS + lin('sky5', [(0, '#2a5a5a'), (.7, '#7ab08a'), (1, '#e8e0a0')])
    d += rad('sun5', 1500, 640, 600, [(0, '#fff6c0', .8), (.3, '#f2d27a', .3), (1, '#f2d27a', 0)])
    d += lin('soil5', [(0, '#5a3a20'), (.5, '#3a2412'), (1, '#1a0e06')])
    d += rad('corm5', 1150, 820, 300, [(0, '#f0e0b0', 1), (.6, '#c8a870', 1), (1, '#8a6a3a', 1)])
    d += lin('stem5', [(0, '#6a9a3a'), (.5, '#a8c860'), (1, '#4a7a2a')], x2=1, y2=0) + VIG('vig5', '#0a0604', .75)
    b = '<rect width="1920" height="1080" fill="url(#sky5)"/><rect width="1920" height="1080" fill="url(#sun5)"/>'
    # far hills
    b += '<path d="M0 690 Q300 620 700 660 Q1100 600 1500 650 Q1750 620 1920 650 L1920 720 L0 720Z" fill="#3a6a4a" opacity=".6"/>'
    # soil cutaway
    b += '<path d="M0 700 Q900 680 1920 705 L1920 1080 L0 1080Z" fill="url(#soil5)"/>'
    b += '<path d="M0 700 Q900 680 1920 705" fill="none" stroke="#4a8a3a" stroke-width="18"/>'
    b += ''.join(f'<ellipse cx="{rnd.uniform(0, 1920):.0f}" cy="{rnd.uniform(740, 1070):.0f}" rx="{rnd.uniform(6, 16):.0f}" ry="{rnd.uniform(4, 9):.0f}" fill="#7a5a3a" opacity="{rnd.uniform(.3, .7):.2f}"/>' for _ in range(70))
    # roots
    for _ in range(14):
        a = rnd.uniform(.2, 2.9); L = rnd.uniform(120, 220)
        x0, y0 = 1200 + math.cos(a) * 200, 880 + math.sin(a) * 70
        b += f'<path d="M{x0:.0f} {y0:.0f} q{math.cos(a) * L * .5:.0f} {L * .4:.0f} {math.cos(a) * L:.0f} {L * .6:.0f}" fill="none" stroke="#c8a870" stroke-width="5" opacity=".7"/>'
    # corm
    b += '<ellipse cx="1200" cy="870" rx="250" ry="120" fill="#000" opacity=".35" filter="url(#b14)"/>'
    b += '<path d="M960 860 Q960 760 1200 750 Q1440 760 1440 860 Q1430 960 1200 975 Q970 960 960 860Z" fill="url(#corm5)" stroke="#3a2410" stroke-width="9"/>'
    b += ''.join(f'<path d="M{1000 + k * 60} {800 + (k % 2) * 30} q30 20 60 0" fill="none" stroke="#8a6a3a" stroke-width="4" opacity=".7"/>' for k in range(7))
    b += '<path d="M1010 820 Q1080 770 1180 768" fill="none" stroke="#fff6dc" stroke-width="10" opacity=".55" stroke-linecap="round"/>'
    b += '<circle cx="1200" cy="860" r="260" fill="#fff0b0" opacity=".12" filter="url(#b50)"/>'
    # pups: small shoots from the corm sides
    for x, top, s in ((900, 560, 1), (1500, 590, .85)):
        b += f'<path d="M{1200 + (x - 1200) * .45:.0f} 860 Q{x:.0f} 840 {x} 760 L{x} 700" fill="none" stroke="#3a2410" stroke-width="30" stroke-linecap="round"/>'
        b += f'<path d="M{1200 + (x - 1200) * .45:.0f} 860 Q{x:.0f} 840 {x} 760 L{x} 700" fill="none" stroke="#b8c870" stroke-width="20" stroke-linecap="round"/>'
        b += leaf(x, 700, 170 * s, -120, '#5aa040', '#2a5a18', .24) + leaf(x, 700, 160 * s, -60, '#4a9038', '#2a5a18', .24) + leaf(x, 700, 120 * s, -92, '#6ab048', '#2a5a18', .24)
    # pseudostem (no wood) with a cut gap and a floating slice showing onion rings
    b += '<path d="M1140 770 L1150 470 L1250 470 L1260 770Z" fill="url(#stem5)" stroke="#2a3a14" stroke-width="8" stroke-linejoin="round"/>'
    b += '<path d="M1146 400 L1160 160 L1240 160 L1254 400Z" fill="url(#stem5)" stroke="#2a3a14" stroke-width="8" stroke-linejoin="round"/>'
    for k in range(4):
        b += f'<path d="M{1156 + k * 26} {760} Q{1150 + k * 26} 620 {1162 + k * 24} 480" fill="none" stroke="#3a5a1a" stroke-width="3" opacity=".5"/>'
    b += '<ellipse cx="1200" cy="470" rx="50" ry="12" fill="#e8f0b0" stroke="#2a3a14" stroke-width="5"/>'
    # crown of leaves + bunch
    for x, y, L, a in ((1200, 170, 420, -160), (1200, 170, 420, -20), (1200, 150, 360, -115), (1200, 150, 360, -65), (1200, 190, 380, 175), (1200, 190, 400, 8)):
        b += leaf(x, y, L, a, '#4a9a3a', '#24501a', .2)
    for k in range(4):
        b += f'<path d="M1250 {230 + k * 30} q40 -4 64 -44" fill="none" stroke="#c8d43a" stroke-width="22" stroke-linecap="round"/><path d="M1250 {230 + k * 30} q40 -4 64 -44" fill="none" stroke="#3a4a08" stroke-width="2.4" opacity=".5"/>'
    # floating slice (cross section) with concentric leaf sheaths
    sl = '<g transform="translate(1530 380) rotate(-12)">'
    sl += '<ellipse cx="10" cy="30" rx="150" ry="70" fill="#4a7a2a" stroke="#2a3a14" stroke-width="8"/>'
    sl += '<rect x="-140" y="0" width="300" height="30" fill="#4a7a2a"/>'
    sl += '<ellipse cx="10" cy="0" rx="150" ry="70" fill="#7aaa48" stroke="#2a3a14" stroke-width="8"/>'
    for k, r in enumerate((128, 106, 84, 62, 40, 20)):
        sl += f'<ellipse cx="{10 + k * 2}" cy="0" rx="{r}" ry="{r * .46:.0f}" fill="{["#a8d070", "#c8e090", "#dceca8", "#e8f2c0", "#f0f6d0", "#fafbe8"][k]}" stroke="#4a6a2a" stroke-width="4"/>'
    sl += '<path d="M-110 -30 Q-40 -66 60 -60" fill="none" stroke="#fff" stroke-width="7" opacity=".55" stroke-linecap="round"/></g>'
    b += '<circle cx="1530" cy="380" r="200" fill="#fff6c0" opacity=".3" filter="url(#b50)"/>' + sl
    b += '<path d="M1280 430 Q1360 380 1400 390" fill="none" stroke="#fffbe6" stroke-width="6" stroke-dasharray="14 12" stroke-linecap="round"/>'
    b += spark(1700, 250, 24, '#fffbe0') + spark(1380, 300, 16) + spark(1080, 800, 18, '#fff6dc')
    # miner frog underground with a head lamp pointing at the corm
    helm = ('<g transform="translate(6 -90) rotate(-6)"><path d="M-40 8 Q-40 -36 0 -38 Q40 -36 40 8Z" fill="#f2c21a" stroke-width="3.4"/>'
            '<path d="M-46 8 L46 8" stroke-width="7" stroke="#d8a810"/><rect x="-12" y="-28" width="24" height="18" rx="5" fill="#fffbe0" stroke-width="3"/></g>')
    b += '<path d="M610 815 L960 790 L960 940 L620 845Z" fill="#fff6c0" opacity=".22"/>'
    b += '<circle cx="560" cy="930" r="150" fill="#fff0b0" opacity=".12" filter="url(#b50)"/>'
    b += frog(560, 1040, 2.6, rot=4, look=(12, -2), mouth='O', shadow=True, top=helm, brows=True,
              armL='M-34 -22 q-18 4 -22 22', armR='M38 -22 q22 -8 30 -30')
    b += '<rect width="1920" height="1080" fill="url(#vig5)"/>'
    return page('#2a5a5a', svg(d, b), [('NOT A', 160, 'w'), ('TREE!', 260, 'y')], outline='#081410', top=40)


for n, fn in enumerate((short1, short2, short3, short4, short5), 1):
    out = os.path.join(VID, f'seedless-banana-short{n}', 'thumb'); os.makedirs(out, exist_ok=True)
    for f in ('common.css', 'Fredoka-700.woff2'):
        shutil.copy(os.path.join(HERE, f), out)
    open(os.path.join(out, 'A.html'), 'w').write(fn())
print('ok')
