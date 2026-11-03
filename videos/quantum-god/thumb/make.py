# Thumbnails A-C for quantum-god (guideline 16-6, brief tools/briefs/thumb_art.md). Run: python3 videos/quantum-god/thumb/make.py
# A  DOES GOD / PLAY / DICE?        intuitive: a huge glowing die in a nebula, ghost copies of it in superposition (S09 Einstein quote, S19 randomness)
# B  DEAD / AND / ALIVE?            homage: Pulp Fiction (glowing case opened, face lit gold, contents unseen) -> Schroedinger's box (S46-S47, "would be")
# C  SPOOKY / ACTION AT / A DISTANCE  homage: Star Wars binary sunset (twin suns, lone figure on a dune) -> entangled pair (S30-S31, S35-S36)
import os, sys, math, random
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../tools'))
from thumb_lib import page, svg, lin, rad, spark

INK = '#1d2b1c'; GREEN = '#6aa55a'
FILTERS = ''.join(f'<filter id="b{s}" x="-60%" y="-60%" width="220%" height="220%"><feGaussianBlur stdDeviation="{s}"/></filter>'
                  for s in (3, 6, 12, 24, 50, 90))
BODY = 'M-34 0 q-6 -64 34 -70 q40 -2 42 62 q0 10 -6 12 q-36 6 -70 -4z'


def lina(id, stops, x2=0, y2=1):   # linear gradient with stop opacity
    return f'<linearGradient id="{id}" x1="0" y1="0" x2="{x2}" y2="{y2}">' + ''.join(f'<stop offset="{o}" stop-color="{c}" stop-opacity="{a}"/>' for o, c, a in stops) + '</linearGradient>'


def stars(n, x0, y0, x1, y1, col='#f2ecff', omax=.8):
    o = ''
    for _ in range(n):
        o += f'<circle cx="{random.uniform(x0, x1):.0f}" cy="{random.uniform(y0, y1):.0f}" r="{random.choice([1.1, 1.6, 2.2, 2.8]):.1f}" fill="{col}" opacity="{random.uniform(.15, omax):.2f}"/>'
    return o


# ---------------- mascot frog (body from tools/assets/frog.svg; outfits per thumbnail) ----------------
def frog(x, y, s, mouth='o', arms='down', look=(2, 0), outfit='', light=None, flip=False, face=None):
    sx = -s if flip else s
    g = f'<g transform="translate({x} {y}) scale({sx:.2f} {s:.2f})" stroke="{INK}" stroke-linejoin="round" stroke-linecap="round">'
    if outfit == 'space':   # backpack behind
        g += '<rect x="-50" y="-60" width="100" height="50" rx="14" fill="#cfd6e6" stroke-width="3.2"/>'
    if outfit == 'desert':  # hood behind the head
        g += '<path d="M-48 -26 C-58 -92 -14 -108 6 -108 C34 -108 66 -92 56 -26 Z" fill="#c99a62" stroke-width="3.6"/>'
        g += '<path d="M-38 -40 C-44 -86 -10 -98 6 -98 C28 -98 52 -86 46 -40" fill="none" stroke="#e8c48e" stroke-width="3" opacity=".8"/>'
    g += '<ellipse cx="-22" cy="4" rx="16" ry="9" fill="#4d8a4a" stroke-width="3.2"/><ellipse cx="22" cy="4" rx="16" ry="9" fill="#4d8a4a" stroke-width="3.2"/>'
    g += f'<path d="{BODY}" fill="{GREEN}" stroke-width="4"/>'
    g += '<ellipse cx="2" cy="-12" rx="22" ry="20" fill="#9cc98a" stroke="none" opacity=".7"/>'
    g += '<path d="M-26 -50 q6 -16 22 -18" fill="none" stroke="#b9e0a6" stroke-width="3" opacity=".7"/>'
    if light:
        g += f'<path d="{BODY}" fill="url(#{light})" stroke="none"/>'
    if outfit == 'tie':     # white collar + slim black tie
        g += '<path d="M-14 -34 L4 -26 L22 -34 L18 -22 L4 -24 L-10 -22 Z" fill="#f4f1ea" stroke-width="2.4"/>'
        g += '<path d="M1 -26 L7 -26 L9 -8 L4 -2 L-1 -8 Z" fill="#14121a" stroke-width="2.2"/>'
    if outfit == 'desert':  # scarf with a tail blowing in the wind
        g += '<path d="M-36 -36 Q4 -22 44 -36 L44 -24 Q4 -10 -36 -24 Z" fill="#b5834c" stroke-width="3"/>'
        g += '<path d="M-30 -28 q-26 2 -46 -10 q6 14 -4 22 q26 4 50 -4" fill="#b5834c" stroke-width="3"/>'
        g += '<path d="M-28 -32 Q4 -20 40 -32" fill="none" stroke="#e2b880" stroke-width="2.2"/>'
    dx, dy = look
    g += f'<circle cx="-10" cy="-66" r="13" fill="#e3e5d6" stroke-width="3.2"/><circle cx="{-10 + dx}" cy="{-66 + dy}" r="5" fill="{INK}" stroke="none"/>'
    g += f'<circle cx="22" cy="-66" r="13" fill="#e3e5d6" stroke-width="3.2"/><circle cx="{22 + dx}" cy="{-66 + dy}" r="5" fill="{INK}" stroke="none"/>'
    g += f'<circle cx="{-8 + dx}" cy="{-68 + dy}" r="1.7" fill="#fff" stroke="none"/><circle cx="{24 + dx}" cy="{-68 + dy}" r="1.7" fill="#fff" stroke="none"/>'
    g += '<ellipse cx="-18" cy="-46" rx="5" ry="3" fill="#e98a8a" stroke="none" opacity=".55"/><ellipse cx="30" cy="-46" rx="5" ry="3" fill="#e98a8a" stroke="none" opacity=".55"/>'
    if mouth == 'o':
        g += '<ellipse cx="6" cy="-42" rx="6.5" ry="8" fill="#7a2f33" stroke-width="3"/><ellipse cx="6" cy="-38" rx="3.5" ry="2.6" fill="#e07b7b" stroke="none"/>'
    else:
        g += '<path d="M-8 -45 q14 14 28 0 q-14 4 -28 0z" fill="#7a2f33" stroke-width="3"/>'
    A = {'down': ('M-34 -22 q-14 6 -16 22', 'M38 -22 q14 6 16 22'),
         'reach': ('M-34 -22 q-14 6 -16 22', 'M38 -24 q22 -6 30 -34'),
         'rim': ('M-34 -24 q-6 -14 4 -30', 'M38 -24 q8 -14 -2 -30')}[arms]
    for d in A:
        g += f'<path d="{d}" fill="none" stroke-width="7.5"/><path d="{d}" fill="none" stroke="{GREEN}" stroke-width="3.4"/>'
    if outfit == 'space':   # bubble helmet + collar
        g += '<circle cx="6" cy="-54" r="50" fill="#bfe6ff" fill-opacity=".13" stroke="#e8eef8" stroke-width="4"/>'
        g += '<path d="M-30 -84 A44 44 0 0 1 10 -100" fill="none" stroke="#fff" stroke-width="5.5" opacity=".8"/><circle cx="40" cy="-30" r="3.4" fill="#fff" stroke="none" opacity=".7"/>'
        g += '<path d="M46 -70 A44 44 0 0 1 40 -22" fill="none" stroke="#ff8fe0" stroke-width="3" opacity=".7"/>'
        g += '<ellipse cx="5" cy="-10" rx="42" ry="9" fill="#aeb7cc" stroke-width="3.2"/><path d="M-32 -12 q37 8 74 0" fill="none" stroke="#f2f6ff" stroke-width="2.2" opacity=".8"/>'
    if face:   # warm light falling on the face from the right (gold glow + rim line)
        g += f'<path d="{BODY}" fill="url(#{face})" stroke="none"/>'
        g += '<path d="M36 -46 q6 18 4 36" fill="none" stroke="#ffe7a0" stroke-width="3.4" opacity=".9"/>'
        g += '<circle cx="28" cy="-71" r="3" fill="#fff6d6" stroke="none"/><circle cx="-4" cy="-71" r="3" fill="#fff6d6" stroke="none"/>'
    return g + '</g>'


# ---------------- 3D die ----------------
def rot(p, ax, ay, az):
    x, y, z = p
    c, s = math.cos(ax), math.sin(ax); y, z = y * c - z * s, y * s + z * c
    c, s = math.cos(ay), math.sin(ay); x, z = x * c + z * s, -x * s + z * c
    c, s = math.cos(az), math.sin(az); x, y = x * c - y * s, x * s + y * c
    return (x, y, z)


PIPS = {1: [(0, 0)], 2: [(-.5, -.5), (.5, .5)], 3: [(-.5, -.5), (0, 0), (.5, .5)], 4: [(-.5, -.5), (.5, -.5), (-.5, .5), (.5, .5)],
        5: [(-.5, -.5), (.5, -.5), (0, 0), (-.5, .5), (.5, .5)], 6: [(-.5, -.55), (.5, -.55), (-.5, 0), (.5, 0), (-.5, .55), (.5, .55)]}
FACES = [((0, 0, -1), (1, 0, 0), (0, 1, 0), 1), ((0, 0, 1), (-1, 0, 0), (0, 1, 0), 6), ((1, 0, 0), (0, 0, 1), (0, 1, 0), 3),
         ((-1, 0, 0), (0, 0, -1), (0, 1, 0), 4), ((0, 1, 0), (1, 0, 0), (0, 0, 1), 2), ((0, -1, 0), (1, 0, 0), (0, 0, -1), 5)]


def mix(c1, c2, t):
    a = [int(c1[i:i + 2], 16) for i in (1, 3, 5)]; b = [int(c2[i:i + 2], 16) for i in (1, 3, 5)]
    return '#' + ''.join(f'{int(a[i] + (b[i] - a[i]) * t):02x}' for i in range(3))


def die(cx, cy, scale, ang, face='#fffaf0', dark='#5a3c8c', pip='#22163f', one='#d8344f', op=1.0, rim='#ff7ad6', glow=True, edge=True):
    D = 7.0
    L = (0.55, 0.62, -0.56); ln = math.sqrt(sum(v * v for v in L)); L = tuple(v / ln for v in L)

    def pr(p):
        q = rot(p, *ang); f = scale * D / (q[2] + D)
        return (cx + q[0] * f, cy - q[1] * f, q[2])
    out = []
    for n, u, v, val in FACES:
        nr = rot(n, *ang); c3 = rot(n, *ang)
        if nr[0] * c3[0] + nr[1] * c3[1] + nr[2] * (c3[2] + D) >= 0:
            continue
        lam = max(0, sum(nr[i] * L[i] for i in range(3)))
        col = mix(dark, face, .45 + .55 * lam)
        corners = []
        for a, b in ((-1, -1), (1, -1), (1, 1), (-1, 1)):
            p = tuple(n[i] + a * u[i] * .985 + b * v[i] * .985 for i in range(3)); corners.append(pr(p))
        depth = sum(c[2] for c in corners) / 4
        pts = ' '.join(f'{c[0]:.1f},{c[1]:.1f}' for c in corners)
        g = f'<polygon points="{pts}" fill="{col}" stroke="{col}" stroke-width="{scale * .16:.1f}" stroke-linejoin="round"/>'
        # soft inner highlight toward the light
        if lam > .5:
            g += f'<polygon points="{pts}" fill="#ffffff" opacity="{(lam - .5) * .35:.2f}"/>'
        for (a, b) in PIPS[val]:
            ring = []
            for k in range(22):
                t = 2 * math.pi * k / 22
                pa, pb = a * .98 + .2 * math.cos(t), b * .98 + .2 * math.sin(t)
                p = tuple(n[i] * 1.001 + pa * u[i] + pb * v[i] for i in range(3)); ring.append(pr(p))
            pc = one if val == 1 else pip
            g += f'<polygon points="{" ".join(f"{c[0]:.1f},{c[1]:.1f}" for c in ring)}" fill="{mix(pc, "#000000", .2 * (1 - lam))}"/>'
            # tiny highlight inside each pip (pips are hollows)
            hp = [pr(tuple(n[i] * 1.002 + (a * .98 + .07) * u[i] + (b * .98 - .1) * v[i] for i in range(3)))]
            g += f'<circle cx="{hp[0][0]:.1f}" cy="{hp[0][1]:.1f}" r="{scale * .035:.1f}" fill="#ffffff" opacity=".18"/>'
        out.append((depth, g, corners, lam))
    out.sort(key=lambda t: -t[0])
    body = ''.join(g for _, g, _, _ in out)
    sil = ''
    if edge:   # bright rim-light strokes on the edges of the lit faces
        for _, _, cs, lam in out:
            if lam > .35:
                sil += f'<polyline points="{cs[3][0]:.1f},{cs[3][1]:.1f} {cs[0][0]:.1f},{cs[0][1]:.1f} {cs[1][0]:.1f},{cs[1][1]:.1f}" fill="none" stroke="#ffffff" stroke-width="{scale * .03:.1f}" opacity=".55" stroke-linecap="round"/>'
    halo = f'<circle cx="{cx}" cy="{cy}" r="{scale * 2.0:.0f}" fill="{rim}" opacity=".35" filter="url(#b50)"/>' if glow else ''
    return f'<g opacity="{op}">{halo}{body}{sil}</g>'


# ============ A: DOES GOD PLAY DICE? (intuitive) ============
def thumb_A():
    random.seed(11)
    defs = FILTERS + lin('skyA', [(0, '#07041a'), (.55, '#1a0b3a'), (1, '#0b0620')])
    defs += rad('neb1', 1450, 470, 760, [(0, '#ff5fc8', .55), (.45, '#8a3bb8', .28), (1, '#160a33', 0)])
    defs += rad('neb2', 1750, 820, 620, [(0, '#36d6d0', .38), (1, '#0b0620', 0)])
    defs += rad('star', 1630, 200, 260, [(0, '#ffffff', 1), (.12, '#fff3d6', .9), (.4, '#ffd27a', .25), (1, '#ffd27a', 0)])
    defs += rad('rock', 860, 1000, 320, [(0, '#5a4a7a', 1), (1, '#1d1433', 1)])
    b = '<rect width="1920" height="1080" fill="url(#skyA)"/>'
    b += '<rect width="1920" height="1080" fill="url(#neb1)"/><rect width="1920" height="1080" fill="url(#neb2)"/>'
    # nebula wisps
    for _ in range(26):
        x = random.uniform(900, 1900); y = random.uniform(80, 900)
        b += f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{random.uniform(80, 260):.0f}" ry="{random.uniform(30, 90):.0f}" transform="rotate({random.uniform(-35, 10):.0f} {x:.0f} {y:.0f})" fill="{random.choice(["#ff5fc8", "#8a6bff", "#36d6d0", "#ff9ad8"])}" opacity="{random.uniform(.06, .18):.2f}" filter="url(#b24)"/>'
    b += stars(260, 0, 0, 1920, 1080)
    # light source: bright star top-right with cross flare
    b += '<rect width="1920" height="1080" fill="url(#star)"/>'
    b += '<path d="M1630 60 L1638 192 L1770 200 L1638 208 L1630 340 L1622 208 L1490 200 L1622 192 Z" fill="#fff8e6" opacity=".9"/>'
    # probability cloud of dots around the die
    for _ in range(420):
        r = abs(random.gauss(0, 1)) * 230 + 160; t = random.uniform(0, 2 * math.pi)
        x = 1250 + r * math.cos(t) * 1.15; y = 520 + r * math.sin(t) * .85
        b += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{random.choice([1.6, 2.2, 3]):.1f}" fill="{random.choice(["#7ff3ee", "#ffb3ec", "#fff1c9"])}" opacity="{random.uniform(.2, .75):.2f}"/>'
    # orbit-like wave rings (probability wave)
    for k, rr in enumerate((330, 400, 470)):
        b += f'<ellipse cx="1250" cy="530" rx="{rr * 1.2:.0f}" ry="{rr * .42:.0f}" transform="rotate(-14 1250 530)" fill="none" stroke="{["#36d6d0", "#ff7ad6", "#8a6bff"][k]}" stroke-width="3" stroke-dasharray="2 14" stroke-linecap="round" opacity=".55"/>'
    # ghost copies: the same die in other states (superposition)
    b += die(1560, 300, 82, (0.9, 1.2, 0.5), face='#bff7f4', dark='#1b4a6a', pip='#0c2a40', one='#0c2a40', op=.42, rim='#36d6d0', edge=False)
    b += die(1690, 560, 70, (2.1, 0.3, -0.6), face='#ffd0f2', dark='#5a1f5e', pip='#3a0c3a', one='#3a0c3a', op=.38, rim='#ff5fc8', edge=False)
    b += die(1430, 220, 56, (-0.4, 2.4, 1.1), face='#fff1c9', dark='#5a4a2a', pip='#3a2a10', one='#3a2a10', op=.32, rim='#ffd27a', edge=False)
    # main die (big, lit from the star at top right)
    b += die(1250, 540, 192, (-0.42, 0.62, 0.22))
    b += spark(1010, 300, 22) + spark(1500, 760, 18) + spark(1780, 420, 14) + spark(960, 640, 14, '#bff7f4')
    # asteroid + astronaut frog in the foreground
    b += '<path d="M640 1080 C650 990 720 950 820 952 C900 950 980 970 1030 1010 C1060 1040 1066 1080 1066 1080 Z" fill="url(#rock)" stroke="#120c22" stroke-width="5"/>'
    b += '<path d="M690 990 C740 962 820 958 900 966" fill="none" stroke="#c99bff" stroke-width="5" opacity=".5"/>'
    b += '<ellipse cx="760" cy="1020" rx="26" ry="10" fill="#120c22" opacity=".6"/><ellipse cx="960" cy="1040" rx="18" ry="7" fill="#120c22" opacity=".6"/>'
    b += frog(860, 972, 3.25, mouth='o', arms='reach', look=(4, -4), outfit='space')
    lines = [('DOES GOD', 168, 'w'), ('PLAY', 150, 'w'), ('DICE?', 236, 'y')]
    return page('#07041a', svg(defs, b), lines, outline='#0a0418')


# ============ B: DEAD AND ALIVE? (homage: Pulp Fiction glowing case) ============
def cat_sit(x, y, s, col, glow, gid, op=1.0):
    """detailed ghost cat sitting, front view; col = outline/neon colour, fill = gradient gid"""
    body = ('M-74 0 C-88 -58 -70 -126 -40 -150 C-62 -166 -66 -202 -52 -224 L-60 -272 C-58 -276 -54 -276 -50 -272 L-22 -242 '
            'C-8 -248 10 -248 24 -242 L52 -272 C56 -276 60 -276 62 -272 L54 -224 C68 -202 64 -166 42 -150 C72 -126 90 -58 76 0 Z')
    tail = 'M70 -8 C130 -10 146 -70 118 -108 C110 -120 100 -116 104 -104'
    g = f'<g transform="translate({x} {y}) scale({s})" opacity="{op}">'
    g += f'<path d="{body}" fill="{glow}" opacity=".55" filter="url(#b12)"/>'
    g += f'<path d="{tail}" fill="none" stroke="{glow}" stroke-width="30" stroke-linecap="round" opacity=".5" filter="url(#b6)"/>'
    g += f'<path d="{tail}" fill="none" stroke="{col}" stroke-width="22" stroke-linecap="round"/><path d="{tail}" fill="none" stroke="url(#{gid})" stroke-width="14" stroke-linecap="round"/>'
    g += f'<path d="{body}" fill="url(#{gid})" stroke="{col}" stroke-width="6" stroke-linejoin="round"/>'
    # inner ears, chest fur, front legs, paws
    g += f'<path d="M-50 -258 L-30 -238 L-48 -228 Z M50 -258 L30 -238 L48 -228 Z" fill="{col}" opacity=".45"/>'
    g += f'<path d="M-22 -140 l8 14 l6 -12 l8 14 l6 -12 l8 14 l8 -14" fill="none" stroke="{col}" stroke-width="4" stroke-linejoin="round" opacity=".7"/>'
    g += f'<path d="M-24 -110 C-28 -60 -30 -24 -34 -2 M24 -110 C28 -60 30 -24 34 -2" fill="none" stroke="{col}" stroke-width="4" opacity=".55"/>'
    g += f'<path d="M-58 -2 q12 -14 24 0 M34 -2 q12 -14 24 0" fill="none" stroke="{col}" stroke-width="4.5"/>'
    # face: glowing eyes, nose, mouth, whiskers
    g += '<ellipse cx="-24" cy="-200" rx="11" ry="13" fill="#eaffff"/><ellipse cx="24" cy="-200" rx="11" ry="13" fill="#eaffff"/>'
    g += f'<ellipse cx="-24" cy="-200" rx="3.6" ry="10" fill="{col}"/><ellipse cx="24" cy="-200" rx="3.6" ry="10" fill="{col}"/>'
    g += f'<circle cx="-24" cy="-200" r="22" fill="#eaffff" opacity=".35" filter="url(#b6)"/><circle cx="24" cy="-200" r="22" fill="#eaffff" opacity=".35" filter="url(#b6)"/>'
    g += f'<path d="M-7 -180 L7 -180 L0 -172 Z" fill="{col}"/><path d="M0 -172 q-8 10 -16 4 M0 -172 q8 10 16 4" fill="none" stroke="{col}" stroke-width="3.2" stroke-linecap="round"/>'
    g += f'<path d="M-18 -176 L-78 -186 M-18 -170 L-76 -166 M18 -176 L78 -186 M18 -170 L76 -166" stroke="{col}" stroke-width="2.6" stroke-linecap="round" opacity=".85"/>'
    return g + '</g>'


def cat_lie(x, y, s, col, glow, gid, op=1.0):
    """detailed ghost cat lying flat on its side, eyes closed"""
    body = ('M-160 0 C-182 -8 -186 -44 -170 -66 L-182 -112 C-180 -116 -176 -116 -172 -112 L-140 -88 C-126 -94 -110 -94 -98 -88 '
            'L-66 -112 C-62 -116 -58 -114 -58 -110 L-66 -70 C-30 -84 46 -90 104 -72 C156 -58 176 -28 158 0 Z')
    tail = 'M152 -8 C200 -4 228 -26 236 -54 C238 -64 248 -64 250 -54'
    g = f'<g transform="translate({x} {y}) scale({s})" opacity="{op}">'
    g += f'<path d="{body}" fill="{glow}" opacity=".55" filter="url(#b12)"/>'
    g += f'<path d="{tail}" fill="none" stroke="{col}" stroke-width="20" stroke-linecap="round"/><path d="{tail}" fill="none" stroke="url(#{gid})" stroke-width="12" stroke-linecap="round"/>'
    g += f'<path d="{body}" fill="url(#{gid})" stroke="{col}" stroke-width="6" stroke-linejoin="round"/>'
    g += f'<path d="M-166 -102 L-150 -86 L-164 -80 Z M-70 -102 L-84 -86 L-72 -80 Z" fill="{col}" opacity=".45"/>'
    g += f'<path d="M-150 -46 q9 7 18 0 M-112 -46 q9 7 18 0" fill="none" stroke="#ffe8fb" stroke-width="4.5" stroke-linecap="round"/>'
    g += f'<path d="M-128 -30 L-116 -30 L-122 -24 Z" fill="{col}"/>'
    g += f'<path d="M-140 -26 L-196 -30 M-140 -20 L-192 -12 M-104 -26 L-50 -32 M-104 -20 L-54 -12" stroke="{col}" stroke-width="2.6" stroke-linecap="round" opacity=".85"/>'
    g += f'<path d="M-40 -6 C-20 -30 20 -34 40 -40 M40 -40 C70 -44 100 -38 120 -20" fill="none" stroke="{col}" stroke-width="4" opacity=".55"/>'
    g += f'<path d="M-60 -2 q-30 -2 -56 4 M100 -4 q34 0 60 8" fill="none" stroke="{col}" stroke-width="4.5" stroke-linecap="round" opacity=".8"/>'
    for zx, zy, zs in ((-196, -130, 16), (-222, -160, 12)):   # sleep marks drawn as tiny zig lines
        g += f'<path d="M{zx} {zy} l{zs} 0 l{-zs} {zs} l{zs} 0" fill="none" stroke="#ffe8fb" stroke-width="3.4" stroke-linejoin="round" opacity=".8"/>'
    return g + '</g>'


def thumb_B():
    random.seed(5)
    defs = FILTERS + lin('wallB', [(0, '#050414'), (.5, '#0d0f2e'), (1, '#090819')])
    defs += lin('floorB', [(0, '#211629'), (.25, '#120c1a'), (1, '#040307')])
    defs += lina('beam', [(0, '#ffe7a0', 0), (.4, '#ffd27a', .4), (.85, '#fff2c4', .9), (1, '#ffffff', 1)])
    defs += lina('beamCore', [(0, '#ffffff', 0), (.5, '#fff6d8', .5), (1, '#ffffff', 1)])
    defs += rad('pool', 1380, 690, 820, [(0, '#ffd27a', .62), (.35, '#ff9a3a', .22), (.7, '#7a2a6a', .1), (1, '#050414', 0)])
    defs += rad('floorPool', 1380, 940, 620, [(0, '#ffcf6a', .55), (.5, '#c06a2a', .15), (1, '#000', 0)])
    defs += rad('mouth', 1415, 670, 300, [(0, '#ffffff', 1), (.4, '#fff4c8', 1), (1, '#f2b84a', 1)])
    defs += rad('nebM', 380, 760, 700, [(0, '#ff3fb8', .32), (1, '#050414', 0)])
    defs += rad('nebT', 1850, 120, 640, [(0, '#1fd6d0', .3), (1, '#050414', 0)])
    defs += rad('nebV', 700, 120, 700, [(0, '#6a3bd8', .3), (1, '#050414', 0)])
    defs += lin('steelF', [(0, '#7d8496'), (.12, '#5a6072'), (.6, '#363b4a'), (1, '#1c1f2a')])
    defs += lin('steelS', [(0, '#3f4656'), (1, '#161923')], x2=1, y2=0)
    defs += lin('lidIn', [(0, '#ffe7a0'), (.35, '#b98a4a'), (1, '#2a2730')])
    defs += lina('catT', [(0, '#7ff7f0', .55), (.6, '#1a4a6a', .5), (1, '#0a2238', .55)])
    defs += lina('catM', [(0, '#ff9ae6', .55), (.6, '#6a1f6a', .5), (1, '#3a0c3a', .55)])
    defs += lina('up', [(0, '#ffe08a', .0), (1, '#ffe08a', .0)])
    defs += rad('face', 30, -50, 64, [(0, '#ffe08a', .75), (.55, '#ffc85a', .3), (1, '#ffc85a', 0)])
    b = '<rect width="1920" height="1080" fill="url(#wallB)"/>'
    b += '<rect width="1920" height="1080" fill="url(#nebV)"/><rect width="1920" height="1080" fill="url(#nebT)"/><rect width="1920" height="1080" fill="url(#nebM)"/>'
    for _ in range(18):   # nebula wisps (background depth)
        x = random.uniform(0, 1920); y = random.uniform(40, 760)
        b += f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{random.uniform(120, 300):.0f}" ry="{random.uniform(25, 70):.0f}" transform="rotate({random.uniform(-25, 15):.0f} {x:.0f} {y:.0f})" fill="{random.choice(["#ff5fc8", "#8a6bff", "#36d6d0"])}" opacity="{random.uniform(.05, .12):.2f}" filter="url(#b24)"/>'
    b += stars(220, 0, 0, 1920, 800, omax=.75)
    # floor: horizon at 76%, glossy, perspective lines converging to the box
    b += '<rect x="0" y="820" width="1920" height="260" fill="url(#floorB)"/>'
    for k in range(-9, 12):
        b += f'<path d="M{1380 + k * 40} 820 L{1380 + k * 260} 1080" stroke="#ffd27a" stroke-width="2" opacity="{max(.03, .16 - abs(k - 1) * .012):.2f}"/>'
    for k, yy in enumerate((842, 872, 914, 970, 1046)):
        b += f'<path d="M0 {yy} L1920 {yy}" stroke="#ffd27a" stroke-width="2" opacity="{.05 + k * .015:.2f}"/>'
    b += '<path d="M0 820 L1920 820" stroke="#ffcf8a" stroke-width="3" opacity=".25"/>'
    b += '<rect width="1920" height="1080" fill="url(#pool)"/><rect x="0" y="820" width="1920" height="260" fill="url(#floorPool)"/>'
    # back bokeh (out of focus, behind the beam)
    for _ in range(22):
        b += f'<circle cx="{random.uniform(950, 1900):.0f}" cy="{random.uniform(60, 760):.0f}" r="{random.uniform(14, 40):.0f}" fill="{random.choice(["#ffd27a", "#36d6d0", "#ff7ad6"])}" opacity="{random.uniform(.08, .2):.2f}" filter="url(#b6)"/>'
    # light: wide halo, fan of god-rays, core
    OY = 640
    b += f'<path d="M1110 {OY + 20} L1720 {OY + 20} L2100 -40 L760 -40 Z" fill="url(#beam)" opacity=".5" filter="url(#b50)"/>'
    b += f'<path d="M1160 {OY} L1680 {OY} L1900 -20 L940 -20 Z" fill="url(#beam)" opacity=".7" filter="url(#b24)"/>'
    for k in range(16):
        x0 = 1170 + k * 32 + random.uniform(-6, 6); spread = (x0 - 1415) * 3.4
        w0 = random.uniform(8, 22); w1 = w0 * random.uniform(3, 6)
        col = random.choice(['#fff4cc', '#fff4cc', '#ffe08a', '#bff7f4', '#ffc8ee'])
        b += f'<path d="M{x0:.0f} {OY} L{x0 + w0:.0f} {OY} L{x0 + spread + w1:.0f} -40 L{x0 + spread:.0f} -40 Z" fill="{col}" opacity="{random.uniform(.08, .22):.2f}" filter="url(#b6)"/>'
    b += f'<path d="M1260 {OY} L1570 {OY} L1640 -40 L1190 -40 Z" fill="url(#beamCore)" opacity=".35" filter="url(#b12)"/>'
    # probability rings rising in the beam (wave-like ripples)
    for k, (yy, rx) in enumerate(((600, 220), (520, 270), (430, 320), (320, 370), (200, 420))):
        b += f'<ellipse cx="1415" cy="{yy}" rx="{rx}" ry="{rx * .16:.0f}" fill="none" stroke="{["#7ff7f0", "#ff9ae6"][k % 2]}" stroke-width="3" opacity="{.5 - k * .07:.2f}" stroke-dasharray="3 12" stroke-linecap="round"/>'
    # the cat in superposition: lying cat (magenta) and sitting cat (teal) overlapped, both floating in the light
    b += cat_lie(1330, 590, 1.3, '#ff6fd0', '#ff3fb8', 'catM', .95)
    b += cat_sit(1495, 592, 1.18, '#5ff0ea', '#1fd6d0', 'catT', .92)
    # rising sparks/particles out of the box
    for _ in range(170):
        x = random.gauss(1415, 170); y = random.uniform(30, 650)
        r = random.choice([1.4, 2, 2.6, 3.4])
        b += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r}" fill="{random.choice(["#fff6d6", "#fff6d6", "#ffd27a", "#bff7f4", "#ffc8ee"])}" opacity="{random.uniform(.3, .95):.2f}"/>'
    for _ in range(10):
        b += spark(int(random.gauss(1415, 220)), random.randint(80, 600), random.choice([10, 14, 18]))
    # ---- box ----
    F = (1140, 700, 1600, 925); dx, dy = 90, -60
    b += f'<ellipse cx="1420" cy="945" rx="440" ry="36" fill="#000" opacity=".6" filter="url(#b12)"/>'
    # reflection of the box glow on the glossy floor
    b += f'<path d="M1150 930 L1690 930 L1760 1080 L1080 1080 Z" fill="#ffd27a" opacity=".12" filter="url(#b24)"/>'
    b += f'<rect x="{F[0]}" y="{F[3] + 4}" width="{F[2] - F[0]}" height="120" fill="url(#steelF)" opacity=".18" filter="url(#b6)"/>'
    # right side
    b += f'<polygon points="{F[2]},{F[1]} {F[2] + dx},{F[1] + dy} {F[2] + dx},{F[3] + dy} {F[2]},{F[3]}" fill="url(#steelS)" stroke="#07080c" stroke-width="5" stroke-linejoin="round"/>'
    b += f'<path d="M{F[2] + dx - 4} {F[1] + dy + 6} L{F[2] + dx - 4} {F[3] + dy - 6}" stroke="#5ff0ea" stroke-width="4" opacity=".55"/>'   # teal rim light
    b += f'<path d="M{F[2] + 26} {F[1] + 70} L{F[2] + 64} {F[1] + 44} L{F[2] + 64} {F[1] + 84} L{F[2] + 26} {F[1] + 110}" fill="none" stroke="#07080c" stroke-width="13" stroke-linejoin="round"/>'   # side handle
    b += f'<path d="M{F[2] + 26} {F[1] + 70} L{F[2] + 64} {F[1] + 44} L{F[2] + 64} {F[1] + 84} L{F[2] + 26} {F[1] + 110}" fill="none" stroke="#b8c0d0" stroke-width="6" stroke-linejoin="round"/>'
    # front
    b += f'<rect x="{F[0]}" y="{F[1]}" width="{F[2] - F[0]}" height="{F[3] - F[1]}" fill="url(#steelF)" stroke="#07080c" stroke-width="5"/>'
    b += f'<rect x="{F[0] + 4}" y="{F[1] + 4}" width="{F[2] - F[0] - 8}" height="18" fill="#ffd27a" opacity=".7"/>'
    b += f'<rect x="{F[0] + 28}" y="{F[1] + 42}" width="{F[2] - F[0] - 56}" height="{F[3] - F[1] - 70}" rx="10" fill="#2a2f3c" opacity=".5" stroke="#12141c" stroke-width="5"/>'
    b += f'<path d="M{F[0] + 34} {F[1] + 46} L{F[2] - 34} {F[1] + 46}" stroke="#c0c8d8" stroke-width="3" opacity=".5"/>'
    for (cx_, cy_) in ((F[0], F[1]), (F[2], F[1]), (F[0], F[3]), (F[2], F[3])):   # corner brackets
        sx_ = 1 if cx_ == F[0] else -1; sy_ = 1 if cy_ == F[1] else -1
        b += f'<path d="M{cx_} {cy_} l{44 * sx_} 0 l0 {12 * sy_} l{-32 * sx_} 0 l0 {32 * sy_} l{-12 * sx_} 0 Z" fill="#a8925a" stroke="#07080c" stroke-width="3"/>'
    for xx in range(F[0] + 60, F[2] - 40, 46):
        b += f'<circle cx="{xx}" cy="{F[1] + 30}" r="5" fill="#b8c0d0" stroke="#14161e" stroke-width="2"/><circle cx="{xx}" cy="{F[3] - 14}" r="5" fill="#5e6474" stroke="#14161e" stroke-width="2"/>'
    for k in range(6):   # scratches / brushed steel
        x0 = random.uniform(F[0] + 40, F[2] - 120); y0 = random.uniform(F[1] + 60, F[3] - 40)
        b += f'<path d="M{x0:.0f} {y0:.0f} l{random.uniform(30, 90):.0f} {random.uniform(-6, 6):.0f}" stroke="#9aa2b4" stroke-width="1.6" opacity=".35"/>'
    b += f'<rect x="1345" y="{F[1] + 12}" width="56" height="44" rx="7" fill="#d9b25a" stroke="#14161e" stroke-width="4"/><rect x="1358" y="{F[1] + 34}" width="30" height="14" rx="4" fill="#5a4220"/><path d="M1352 {F[1] + 18} l40 0" stroke="#fff1c0" stroke-width="3"/>'
    # Geiger dial with a glowing red needle
    GX, GY = 1490, 828
    b += f'<circle cx="{GX}" cy="{GY}" r="60" fill="#14161e"/><circle cx="{GX}" cy="{GY}" r="52" fill="#f1ead0" stroke="#7a6a4a" stroke-width="3"/>'
    b += f'<path d="M{GX - 40} {GY} A40 40 0 0 1 {GX + 40} {GY}" fill="none" stroke="#3a2f20" stroke-width="3"/><path d="M{GX + 20} {GY - 35} A40 40 0 0 1 {GX + 40} {GY}" fill="none" stroke="#d8344f" stroke-width="7"/>'
    b += ''.join(f'<path d="M{GX + 40 * math.cos(math.pi + k * math.pi / 8):.1f} {GY + 40 * math.sin(math.pi + k * math.pi / 8):.1f} L{GX + 31 * math.cos(math.pi + k * math.pi / 8):.1f} {GY + 31 * math.sin(math.pi + k * math.pi / 8):.1f}" stroke="#3a2f20" stroke-width="2.6"/>' for k in range(9))
    b += f'<path d="M{GX} {GY} L{GX + 30} {GY - 32}" stroke="#ff3b52" stroke-width="5" stroke-linecap="round"/><circle cx="{GX + 30}" cy="{GY - 32}" r="9" fill="#ff3b52" opacity=".5" filter="url(#b3)"/><circle cx="{GX}" cy="{GY}" r="7" fill="#14161e"/>'
    b += f'<path d="M{GX - 36} {GY - 32} A50 50 0 0 1 {GX + 16} {GY - 48}" fill="none" stroke="#fff" stroke-width="4" opacity=".7"/>'
    b += f'<circle cx="{GX - 74}" cy="{GY + 40}" r="9" fill="#5ff0ea" stroke="#14161e" stroke-width="3"/><circle cx="{GX - 74}" cy="{GY + 40}" r="16" fill="#5ff0ea" opacity=".45" filter="url(#b3)"/>'
    # opening, blazing white with a flare
    op = f'{F[0]},{F[1]} {F[2]},{F[1]} {F[2] + dx},{F[1] + dy} {F[0] + dx},{F[1] + dy}'
    b += f'<polygon points="{op}" fill="url(#mouth)" stroke="#fffbe8" stroke-width="6" stroke-linejoin="round"/>'
    b += f'<polygon points="{op}" fill="#ffffff" opacity=".85" filter="url(#b12)"/>'
    b += f'<ellipse cx="1415" cy="{F[1] - 30}" rx="360" ry="40" fill="#fff6d0" opacity=".6" filter="url(#b24)"/>'
    b += f'<path d="M1050 {F[1] - 30} L1780 {F[1] - 30}" stroke="#ffffff" stroke-width="5" opacity=".75" filter="url(#b3)"/>'
    b += spark(1415, F[1] - 30, 56, '#ffffff', .95)
    # lid leaning on the right, inner face catching the light
    b += '<polygon points="1690,600 1786,548 1820,884 1724,936" fill="#2b2f3a" stroke="#07080c" stroke-width="5" stroke-linejoin="round"/>'
    b += '<polygon points="1700,612 1778,568 1800,760 1716,800" fill="url(#lidIn)" opacity=".55"/>'
    b += '<path d="M1690 600 L1786 548" stroke="#ffe7a0" stroke-width="6"/><path d="M1708 640 L1734 900" stroke="#5ff0ea" stroke-width="3" opacity=".4"/>'
    # frog in front-left, hands on the rim, face lit gold from the box
    b += frog(1062, 952, 3.8, mouth='o', arms='rim', look=(7, 3), outfit='tie', light='up', face='face')
    # foreground bokeh for depth
    for (x, y, r, c) in ((210, 980, 60, '#ffd27a'), (560, 1040, 44, '#ff7ad6'), (90, 760, 34, '#36d6d0'), (1880, 640, 50, '#ffd27a'), (900, 1050, 30, '#bff7f4')):
        b += f'<circle cx="{x}" cy="{y}" r="{r}" fill="{c}" opacity=".22" filter="url(#b12)"/>'
    b += '<rect width="1920" height="1080" fill="url(#vigB)"/>'
    defs += rad('vigB', 1300, 560, 1250, [(0, '#000', 0), (.65, '#000', 0), (1, '#000', .55)])
    lines = [('DEAD', 196, 'w'), ('AND', 128, 'w'), ('AL<span style="margin:0 12px 0 10px">I</span>VE?', 226, 'y')]
    return page('#050414', svg(defs, b), lines, outline='#07060f')



# ============ C: SPOOKY ACTION AT A DISTANCE (homage: Star Wars binary sunset) ============
def thumb_C():
    random.seed(7)
    defs = FILTERS + lin('skyC', [(0, '#120a30'), (.32, '#4a1f63'), (.58, '#b84a6e'), (.78, '#f39a52'), (.86, '#ffd49a')])
    defs += rad('sun1', 1250, 560, 460, [(0, '#ffffff', 1), (.2, '#fff4cf', .95), (.38, '#ffd27a', .55), (1, '#ff9a4a', 0)])
    defs += rad('sun2', 1600, 660, 330, [(0, '#ffffff', 1), (.2, '#ffe0e8', .95), (.42, '#ff8ab0', .5), (1, '#ff5fc8', 0)])
    defs += rad('disk1', 1225, 530, 175, [(0, '#ffffff', 1), (.55, '#fff2c2', 1), (1, '#ffc55e', 1)])
    defs += rad('disk2', 1585, 645, 112, [(0, '#ffffff', 1), (.55, '#ffe3ec', 1), (1, '#ff98be', 1)])
    defs += lin('duneFar', [(0, '#a8507a'), (1, '#6a2c5e')])
    defs += lin('duneMid', [(0, '#5a2350'), (1, '#2a1030')])
    defs += lin('duneNear', [(0, '#7a3a3e'), (.3, '#3c1a2c'), (1, '#160914')])
    defs += rad('neb', 1600, 120, 600, [(0, '#ff5fc8', .3), (.5, '#8a6bff', .16), (1, '#120a30', 0)])
    b = '<rect width="1920" height="1080" fill="url(#skyC)"/><rect width="1920" height="1080" fill="url(#neb)"/>'
    b += stars(170, 0, 0, 1920, 360, omax=.8)
    for _ in range(14):
        x = random.uniform(1000, 1900); y = random.uniform(60, 330)
        b += f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{random.uniform(100, 260):.0f}" ry="{random.uniform(20, 60):.0f}" transform="rotate({random.uniform(-20, 8):.0f} {x:.0f} {y:.0f})" fill="{random.choice(["#ff5fc8", "#8a6bff", "#36d6d0"])}" opacity="{random.uniform(.06, .14):.2f}" filter="url(#b24)"/>'
    # twin suns with halos
    b += '<rect width="1920" height="1080" fill="url(#sun1)"/><rect width="1920" height="1080" fill="url(#sun2)"/>'
    b += '<circle cx="1250" cy="560" r="150" fill="url(#disk1)"/><circle cx="1250" cy="560" r="150" fill="none" stroke="#ffe08a" stroke-width="10" opacity=".7"/>'
    b += '<circle cx="1600" cy="660" r="96" fill="url(#disk2)"/><circle cx="1600" cy="660" r="96" fill="none" stroke="#ff9ac4" stroke-width="8" opacity=".7"/>'
    # entanglement: two braided glowing waves linking the suns
    def wave(phase, col, w, op):
        pts = []
        for k in range(61):
            t = k / 60; x = 1360 + t * 180; y = 600 + t * 50 + 40 * math.sin(t * 3 * math.pi + phase) * math.sin(t * math.pi)
            pts.append(f'{x:.1f},{y:.1f}')
        return f'<polyline points="{" ".join(pts)}" fill="none" stroke="{col}" stroke-width="{w}" stroke-linecap="round" opacity="{op}"/>'
    for ph, col in ((0, '#5ff0ea'), (math.pi, '#ff6fd0')):
        b += f'<g filter="url(#b6)">{wave(ph, col, 22, .9)}</g>' + wave(ph, col, 8, 1) + wave(ph, '#ffffff', 3.5, .95)
    # spin arrows: up in the big sun, down in the small sun (opposite, linked)
    b += '<path d="M1250 650 L1250 480 M1196 534 L1250 470 L1304 534" fill="none" stroke="#b33a2a" stroke-width="26" stroke-linecap="round" stroke-linejoin="round"/>'
    b += '<path d="M1600 600 L1600 716 M1564 684 L1600 724 L1636 684" fill="none" stroke="#a02a6a" stroke-width="18" stroke-linecap="round" stroke-linejoin="round"/>'
    b += spark(1120, 430, 20) + spark(1700, 520, 16) + spark(1420, 470, 14) + spark(1840, 300, 14)
    # dunes: far (horizon 72%), mid, near
    b += '<path d="M0 790 C200 770 380 760 560 772 C760 786 900 758 1100 762 C1320 766 1500 746 1700 760 C1800 766 1880 770 1920 768 L1920 1080 L0 1080 Z" fill="url(#duneFar)"/>'
    b += '<path d="M0 790 C200 770 380 760 560 772 C760 786 900 758 1100 762 C1320 766 1500 746 1700 760 C1800 766 1880 770 1920 768" fill="none" stroke="#ffc08a" stroke-width="4" opacity=".7"/>'
    b += '<path d="M600 1080 C760 900 980 840 1220 846 C1460 852 1640 880 1920 860 L1920 1080 Z" fill="url(#duneMid)"/>'
    b += '<path d="M780 940 C900 870 1040 846 1220 846 C1460 852 1640 880 1920 860" fill="none" stroke="#ff9a62" stroke-width="5" opacity=".75"/>'
    # tiny domed homestead on the mid dune (scale)
    b += '<path d="M1640 872 a34 26 0 0 1 68 0 Z" fill="#c9a07a" stroke="#2a1030" stroke-width="3"/><rect x="1662" y="858" width="22" height="14" rx="3" fill="#2a1030"/>'
    b += '<path d="M1730 872 L1730 820 M1720 830 L1740 830 M1724 846 L1736 846" stroke="#2a1030" stroke-width="4" stroke-linecap="round"/>'
    b += '<path d="M1642 870 a32 24 0 0 1 30 -22" fill="none" stroke="#ffd2a0" stroke-width="3" opacity=".8"/>'
    # near dune with the frog on its crest
    b += '<path d="M0 1080 L0 930 C200 900 420 900 620 950 C760 985 900 1010 1080 1080 Z" fill="url(#duneNear)"/>'
    b += '<path d="M0 930 C200 900 420 900 620 950 C760 985 900 1010 1080 1080" fill="none" stroke="#ffb07a" stroke-width="6" opacity=".85"/>'
    for k in range(8):   # sand ripples
        y0 = 980 + k * 14
        b += f'<path d="M{40 + k * 30} {y0} C{200 + k * 20} {y0 - 14} {380 + k * 10} {y0 - 10} {560 - k * 10} {y0 + 12}" fill="none" stroke="#a86a5a" stroke-width="2.5" opacity=".35"/>'
    # long shadow of the frog to the left (low suns on the right)
    b += '<ellipse cx="380" cy="944" rx="190" ry="14" fill="#160914" opacity=".55" transform="rotate(-2 380 944)"/>'
    for k in range(5):   # footprints
        b += f'<ellipse cx="{720 + k * 46}" cy="{958 + k * 10 + (6 if k % 2 else 0)}" rx="9" ry="4" fill="#2a1020" opacity=".55"/>'
    b += frog(560, 944, 3.3, mouth='o', arms='reach', look=(6, -5), outfit='desert')
    lines = [('SPOOKY', 214, 'y'), ('ACTION AT', 140, 'w'), ('A DISTANCE', 140, 'w')]
    return page('#120a30', svg(defs, b), lines, outline='#0e0620')


for n, fn in (('A', thumb_A), ('B', thumb_B), ('C', thumb_C)):
    open(os.path.join(HERE, f'{n}.html'), 'w').write(fn())
print('ok')
