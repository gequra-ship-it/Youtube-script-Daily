# Shorts thumbnails (guideline 16-9) for hollow-skyscraper-short1..5 (Burj Khalifa). Opus thumb agent 2026-11-06.
# One generator for all five: writes videos/hollow-skyscraper-shortN/thumb/A.html (N = 1..5), reusing the long-form helpers
# (frog, tower) from videos/hollow-skyscraper/thumb/make.py. Long-form A/B/C used: paper tube + books, snowshoes, wind monster.
# short1 S04 "Nature found this trick long ago" -> bamboo (cut open, hollow with rings) + hollow bird bone with struts. NATURE'S / HOLLOW / TRICK
# short2 S03-S05 "close to two hundred concrete piles... a long concrete root", raft on top, weak sandstone -> underground cut-away. CONCRETE / ROOTS
# short3 S07-S10 "look down on it from above and you see a letter Y... a stable tripod with a hollow heart" -> aerial Y plan, frog in a balloon. A STABLE / TRIPOD
# short4 S03-S05 skier plants ski poles wide "keeps the body from tumbling" = outriggers -> the tower plants giant ski poles, frog skier. IT WON'T / TUMBLE
# short5 S02-S07 vortex shedding, "tested small models of the tower while air blasted past... initial design would not work" -> wind tunnel. FIRST TEST: / FAILED
import os, sys, math, random, shutil, importlib.util
HERE = os.path.dirname(os.path.abspath(__file__))
VID = os.path.dirname(os.path.dirname(HERE))
LONG = os.path.join(VID, 'hollow-skyscraper', 'thumb')
sys.path.insert(0, os.path.join(VID, '..', 'tools'))
spec = importlib.util.spec_from_file_location('longmake', os.path.join(LONG, 'make.py'))
L = importlib.util.module_from_spec(spec); spec.loader.exec_module(L)
from thumb_lib import svg, lin, rad, spark
frog, tower, page, FILTERS, HARDHAT, INK = L.frog, L.tower, L.page, L.FILTERS, L.HARDHAT, L.INK


def cloud(x, y, s, col='#ffffff', op=.9):
    return (f'<g opacity="{op}" fill="{col}"><ellipse cx="{x}" cy="{y}" rx="{90 * s}" ry="{20 * s}"/><ellipse cx="{x - 30 * s}" cy="{y - 14 * s}" rx="{44 * s}" ry="{22 * s}"/>'
            f'<ellipse cx="{x + 30 * s}" cy="{y - 18 * s}" rx="{40 * s}" ry="{24 * s}"/></g>')


def spiral(cx, cy, r, turns=1.6, cw=1, a0=0):
    pts = []
    n = 60
    for i in range(n + 1):
        t = i / n; a = a0 + cw * t * turns * 2 * math.pi; rr = r * (1 - .85 * t)
        pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    return 'M' + ' L'.join(f'{x:.1f} {y:.1f}' for x, y in pts)


# =========================== short1: nature's hollow trick ===========================
def s1():
    rnd = random.Random(11); d = FILTERS; HZ = 800
    d += lin('sky', [(0, '#123f52'), (.45, '#2f7d86'), (.8, '#9fcf9a'), (1, '#f6dc96')])
    d += lin('gnd', [(0, '#7aa04a'), (.4, '#4f7a34'), (1, '#1f3818')])
    d += rad('sun', 1120, 380, 620, [(0, '#fffbe0', .95), (.2, '#fff0b0', .55), (.6, '#ffe08a', .15), (1, '#ffe08a', 0)])
    b = f'<rect width="1920" height="{HZ}" fill="url(#sky)"/><rect width="1920" height="{HZ}" fill="url(#sun)"/>'
    for (x, y, s) in ((1500, 170, 1.2), (1800, 290, .8), (620, 560, .9)):
        b += cloud(x, y, s, '#f4fff6', .7)
    # distant hills + desert city
    b += f'<path d="M0 {HZ - 60} Q300 {HZ - 120} 640 {HZ - 50} T1300 {HZ - 70} T1920 {HZ - 40} V{HZ + 5} H0Z" fill="#5f8f78" opacity=".7"/>'
    x = 1180
    while x < 1920:
        w = rnd.randint(14, 34); h = rnd.randint(16, 70)
        b += f'<rect x="{x}" y="{HZ - h}" width="{w}" height="{h + 4}" fill="#4e7d74" opacity=".8"/>'
        x += w + rnd.randint(3, 16)
    b += f'<rect y="{HZ}" width="1920" height="{1080 - HZ}" fill="url(#gnd)"/>'
    b += f'<path d="M0 {HZ + 20} Q500 {HZ - 10} 1000 {HZ + 30} T1920 {HZ + 10}" fill="none" stroke="#d6e98a" stroke-width="4" opacity=".6"/>'
    for k in range(70):   # grass tufts
        gx = rnd.randint(0, 1900); gy = rnd.randint(HZ + 20, 1070)
        if gx > 1640 and gy > 940: continue
        b += f'<path d="M{gx} {gy} l-6 -{rnd.randint(14, 26)} M{gx} {gy} l2 -{rnd.randint(18, 30)} M{gx} {gy} l9 -{rnd.randint(12, 22)}" stroke="#a8cf62" stroke-width="3" opacity=".7"/>'

    # ---- Burj Khalifa in the back right, glowing ----
    cx, base, H, W = 1600, 905, 760, 270
    d2, b2 = tower(cx, base, H, W, dict(
        faces=[('#5f8aa0', '#c0e2ea'), ('#78a2b6', '#e2f4f6'), ('#4a7488', '#9cc4cf'), ('#3a6074', '#80a8b6')],
        edge='#163040', rim='#fff2c0', rimside='L', band='#2a4a5a', line='#244252', glow='#fff2b0', glowop=.5), 'tw')
    d += d2; b += b2

    # ---- giant bamboo stalk, cut open on the front ----
    bx, bw = 1130, 168
    d += lin('bam', [(0, '#2f5a1c'), (.18, '#5d9a34'), (.42, '#b8e27a'), (.6, '#86c04c'), (1, '#2b4f18')], x2=1, y2=0)
    d += lin('bin', [(0, '#a88a4a'), (.2, '#e6d39a'), (.5, '#fff4cc'), (.8, '#e0c98a'), (1, '#9a7c40')], x2=1, y2=0)
    b += f'<ellipse cx="{bx}" cy="560" rx="300" ry="520" fill="#fff6c0" opacity=".35" filter="url(#blur60)"/>'
    b += f'<rect x="{bx - bw / 2}" y="-20" width="{bw}" height="{HZ + 160}" fill="url(#bam)" stroke="{INK}" stroke-width="6"/>'
    nodes = [40, 250, 470, 700, 930]
    # cut-away window (lower two segments) showing the hollow inside and the solid rings
    wy0, wy1 = 300, 880
    b += f'<rect x="{bx - bw / 2 + 22}" y="{wy0}" width="{bw - 44}" height="{wy1 - wy0}" rx="10" fill="url(#bin)" stroke="#3a4a18" stroke-width="5"/>'
    b += f'<rect x="{bx - bw / 2 + 22}" y="{wy0}" width="18" height="{wy1 - wy0}" fill="#6a5424" opacity=".35"/>'
    for ny in nodes:
        if wy0 < ny < wy1:   # diaphragm (solid ring) across the hollow
            b += f'<ellipse cx="{bx}" cy="{ny}" rx="{bw / 2 - 22}" ry="14" fill="#c8a85a" stroke="#5a4418" stroke-width="4"/>'
            b += f'<ellipse cx="{bx}" cy="{ny - 4}" rx="{bw / 2 - 34}" ry="7" fill="#f6e2a8"/>'
    for (yy, s) in ((380, .5), (600, .6), (800, .45)):   # empty air inside
        b += spark(bx, yy, 20 * s + 8, '#ffffff', .9)
    for ny in nodes:   # outer node rings
        b += f'<path d="M{bx - bw / 2 - 6} {ny} Q{bx} {ny + 22} {bx + bw / 2 + 6} {ny}" fill="none" stroke="{INK}" stroke-width="9"/>'
        b += f'<path d="M{bx - bw / 2 - 2} {ny - 6} Q{bx} {ny + 14} {bx + bw / 2 + 2} {ny - 6}" fill="none" stroke="#d6f29a" stroke-width="4"/>'
    b += f'<path d="M{bx - 34} -20 V{wy0 - 8} M{bx - 34} {wy1 + 10} V{HZ + 140}" stroke="#eaffc0" stroke-width="10" opacity=".55" stroke-linecap="round"/>'
    # leaves sprouting from the nodes
    for (ny, side, ang) in ((250, 1, -20), (40, -1, 10), (470, 1, 15)):
        lx = bx + side * bw / 2
        for k in range(3):
            a = ang + k * 22 * side
            b += (f'<g transform="translate({lx} {ny}) rotate({a}) scale({side} 1)"><path d="M0 0 q90 -40 210 -6 q-110 26 -210 6z" fill="#5e9a34" stroke="{INK}" stroke-width="4"/>'
                  f'<path d="M10 -2 q90 -18 190 -4" fill="none" stroke="#b8e27a" stroke-width="3"/></g>')
    b += f'<ellipse cx="{bx}" cy="{HZ + 140}" rx="140" ry="20" fill="#16280f" opacity=".5" filter="url(#blur8)"/>'

    # ---- big hollow bird bone lying in the grass, cut open with struts inside ----
    gx, gy, ang = 520, 860, -8
    d += lin('bone', [(0, '#fffaf0'), (.35, '#f3e6c8'), (.8, '#d8c39a'), (1, '#a8916a')])
    bone = f'<g transform="translate({gx} {gy}) rotate({ang})">'
    bone += '<ellipse cx="20" cy="70" rx="440" ry="34" fill="#1a2c12" opacity=".5" filter="url(#blur8)"/>'
    # shaft + knobby left end + open right end
    bone += f'<path d="M-330 -42 Q-60 -30 290 -48 L290 48 Q-60 34 -330 42Z" fill="url(#bone)" stroke="{INK}" stroke-width="6"/>'
    bone += f'<circle cx="-370" cy="-40" r="62" fill="url(#bone)" stroke="{INK}" stroke-width="6"/><circle cx="-372" cy="38" r="58" fill="url(#bone)" stroke="{INK}" stroke-width="6"/>'
    bone += '<path d="M-330 -40 Q-310 0 -330 40" fill="url(#bone)" stroke="none"/><rect x="-350" y="-36" width="40" height="72" fill="url(#bone)"/>'
    bone += '<path d="M-400 -76 q30 -18 60 -2" fill="none" stroke="#ffffff" stroke-width="7" stroke-linecap="round"/>'
    # cut-away window along the shaft: hollow inside with zig-zag struts
    bone += '<path d="M-210 -22 Q20 -14 200 -26 L200 26 Q20 16 -210 22Z" fill="#7a4a3a" stroke="#4a2a20" stroke-width="4"/>'
    bone += '<path d="M-210 -22 Q20 -14 200 -26 L200 -14 Q20 -4 -210 -12Z" fill="#a8685a" opacity=".6"/>'
    zz = 'M-200 18 ' + ' '.join(f'L{-200 + 40 * k} {(-16 if k % 2 else 18)}' for k in range(1, 11))
    bone += f'<path d="{zz}" fill="none" stroke="#3a2015" stroke-width="12" stroke-linejoin="round"/><path d="{zz}" fill="none" stroke="#f6e8cc" stroke-width="7" stroke-linejoin="round"/>'
    # open end (cross-section ring)
    bone += f'<ellipse cx="290" cy="0" rx="30" ry="50" fill="#f3e6c8" stroke="{INK}" stroke-width="6"/>'
    bone += '<ellipse cx="292" cy="0" rx="20" ry="38" fill="#5a3226"/>'
    bone += '<path d="M276 -30 L306 26 M300 -34 L282 30" stroke="#f6e8cc" stroke-width="5"/>'
    bone += '<path d="M-300 -30 Q-60 -22 260 -36" fill="none" stroke="#ffffff" stroke-width="6" opacity=".8" stroke-linecap="round"/>'
    bone += '</g>'
    b += bone
    # ---- frog explorer sitting on the bone with a magnifying glass ----
    hat = ('<path d="M-40 -82 q46 -14 92 0 q-8 8 -46 8 q-38 0 -46 -8z" fill="#c9a060" stroke-width="3"/>'
           '<path d="M-22 -84 q28 -40 56 0z" fill="#d8b070" stroke-width="3"/><path d="M-20 -88 q28 6 52 0" fill="none" stroke="#7a4a1c" stroke-width="5"/>')
    lens = ('<path d="M54 -6 L80 -60" stroke="#5a3a1a" stroke-width="9" stroke-linecap="round"/>'
            '<circle cx="92" cy="-84" r="28" fill="#bfeaff" fill-opacity=".45" stroke="#3a2a14" stroke-width="7"/>'
            '<path d="M78 -94 q8 -10 20 -8" fill="none" stroke="#ffffff" stroke-width="4"/>')
    b += frog(440, 834, 2.7, look=(5, 4), mouth='o', armL='M-34 -24 q-24 -6 -28 -34', armR='M38 -22 q16 6 18 18', top=hat + lens)
    for (x, y, s) in ((880, 760, 18), (1330, 300, 22), (1420, 640, 16), (760, 560, 14)):
        b += spark(x, y, s, '#fffbe0', .9)
    return page('#123f52', svg(d, b), [(132, [("NATURE'S", 'w')]), (176, [('HOLLOW', 'y')]), (132, [('TRICK', 'w')])], outline='#0a2028')


# =========================== short2: concrete roots ===========================
def s2():
    rnd = random.Random(21); d = FILTERS; GY = 560
    d += lin('sky', [(0, '#1a6fb0'), (.6, '#6ec0e6'), (1, '#ffe2a8')])
    d += rad('sun', 1700, 120, 300, [(0, '#fffbe6', 1), (.15, '#fff1b8', .8), (1, '#ffe08a', 0)])
    b = f'<rect width="1920" height="{GY}" fill="url(#sky)"/><rect width="1920" height="{GY}" fill="url(#sun)"/><circle cx="1700" cy="120" r="46" fill="#fffbe8"/>'
    for (x, y, s) in ((560, 470, 1.1), (1600, 380, .9)):
        b += cloud(x, y, s)
    x = 0
    while x < 1920:
        w = rnd.randint(14, 34); h = rnd.randint(12, 60)
        if not (900 < x < 1600):
            b += f'<rect x="{x}" y="{GY - h}" width="{w}" height="{h + 4}" fill="#8fb0c4" opacity=".75"/>'
        x += w + rnd.randint(3, 16)
    # ---- underground strata: weak sandstone / siltstone layers ----
    layers = [('#e8b878', 0), ('#c89660', 70), ('#b07f50', 190), ('#94673f', 330), ('#7a5434', 460)]
    for k, (col, top) in enumerate(layers):
        y = GY + top
        b += f'<path d="M0 {y} Q480 {y - 18} 960 {y + 12} T1920 {y - 6} V1080 H0Z" fill="{col}"/>'
        if k:
            b += f'<path d="M0 {y} Q480 {y - 18} 960 {y + 12} T1920 {y - 6}" fill="none" stroke="#5a3a20" stroke-width="3" opacity=".45"/>'
    for k in range(260):   # grains and cracks (weak rock)
        px, py = rnd.randint(0, 1900), rnd.randint(GY + 30, 1070)
        b += f'<circle cx="{px}" cy="{py}" r="{rnd.choice([2, 3, 4])}" fill="{rnd.choice(["#f2cf98", "#5e3e24", "#d8a870"])}" opacity="{rnd.uniform(.3, .7):.2f}"/>'
    for k in range(18):
        px, py = rnd.randint(0, 1900), rnd.randint(GY + 80, 1060)
        b += f'<path d="M{px} {py} l{rnd.randint(10, 30)} {rnd.randint(-8, 8)} l{rnd.randint(10, 26)} {rnd.randint(-10, 10)}" fill="none" stroke="#4a2e18" stroke-width="2.5" opacity=".5"/>'
    # salty groundwater sheen
    b += f'<path d="M0 {GY + 260} Q500 {GY + 240} 960 {GY + 270} T1920 {GY + 250} V{GY + 300} Q1400 {GY + 320} 960 {GY + 300} T0 {GY + 300}Z" fill="#7fc6d0" opacity=".25"/>'
    # surface crust + palms
    b += f'<path d="M0 {GY} Q480 {GY - 10} 960 {GY + 6} T1920 {GY - 4} V{GY + 22} H0Z" fill="#f6d090"/>'
    b += f'<path d="M0 {GY} Q480 {GY - 10} 960 {GY + 6} T1920 {GY - 4}" fill="none" stroke="#fff0c8" stroke-width="4"/>'
    for px in (300, 720, 1720):
        b += f'<path d="M{px} {GY} q4 -50 10 -80" stroke="#7a5228" stroke-width="8" fill="none"/>'
        for (dx, dy) in ((-40, 10), (40, 6), (-30, -16), (34, -18), (0, -30)):
            b += f'<path d="M{px + 10} {GY - 80} q{dx * .5} {dy - 20} {dx} {dy + 10}" fill="none" stroke="#3f7a32" stroke-width="9" stroke-linecap="round"/>'

    cx = 1250
    # ---- piles: long concrete roots ----
    d += lin('pile', [(0, '#7d7a72'), (.3, '#d8d4ca'), (.55, '#f4f1ea'), (1, '#8a867c')], x2=1, y2=0)
    d += rad('rglow', cx, GY + 140, 520, [(0, '#ffe4a0', .7), (.5, '#ffd27a', .25), (1, '#ffd27a', 0)])
    b += f'<ellipse cx="{cx}" cy="{GY + 250}" rx="560" ry="330" fill="url(#rglow)"/>'
    piles = ''
    xs = [cx - 340 + 680 * i / 14 for i in range(15)]
    for i, x in enumerate(xs):
        depth = 900 + rnd.randint(-20, 70) - abs(i - 7) * 8
        top = GY + 58; w = 30
        piles += f'<rect x="{x - w / 2 - 5}" y="{top}" width="{w + 10}" height="{depth - top}" fill="#3a2a1a" opacity=".35" rx="14"/>'
        piles += f'<path d="M{x - w / 2} {top} V{depth} Q{x} {depth + 26} {x + w / 2} {depth} V{top}Z" fill="url(#pile)" stroke="#2e2a24" stroke-width="3.5"/>'
        # little root hairs at the tips
        for k in range(3):
            a = rnd.uniform(-1, 1)
            piles += f'<path d="M{x} {depth + 14} q{a * 16:.0f} 20 {a * 30:.0f} {rnd.randint(30, 50)}" fill="none" stroke="#c9c2b2" stroke-width="3" stroke-linecap="round"/>'
        # load glowing down each pile
        piles += f'<path d="M{x - 3} {top + 6} V{depth - 10}" stroke="#ffe7a0" stroke-width="5" opacity=".8" stroke-dasharray="26 18"/>'
    b += piles
    # ---- raft (thick concrete mat) ----
    rw, rt, rh = 380, GY + 6, 56
    d += lin('raft', [(0, '#fff6dc'), (.4, '#e2dccd'), (1, '#9a9488')])
    b += f'<rect x="{cx - rw - 20}" y="{rt - 16}" width="{2 * rw + 40}" height="{rh + 32}" rx="20" fill="#ffd27a" opacity=".6" filter="url(#blur14)"/>'
    b += f'<rect x="{cx - rw}" y="{rt}" width="{2 * rw}" height="{rh}" rx="8" fill="url(#raft)" stroke="#2e2a24" stroke-width="5"/>'
    b += f'<path d="M{cx - rw + 10} {rt + 8} H{cx + rw - 10}" stroke="#ffffff" stroke-width="5" opacity=".9"/>'
    for k in range(1, 12):
        b += f'<path d="M{cx - rw + k * 2 * rw / 12} {rt + 4} v{rh - 8}" stroke="#8a8478" stroke-width="2" opacity=".5"/>'
    # ---- tower standing on the raft ----
    d2, b2 = tower(cx, GY + 8, 520, 230, dict(
        faces=[('#6d8eb3', '#bfe0f5'), ('#86a8cc', '#dff1fb'), ('#9ec0de', '#f0fbff'), ('#b8d6ec', '#ffffff')],
        edge='#22344e', rim='#ffffff', rimside='R', band='#3d5a7c', line='#2c4766', glow='#fff3c4', glowop=.45), 'tw')
    d += d2; b += b2
    # ---- frog miner in a little cave at bottom-left, headlamp on the roots ----
    b += '<ellipse cx="430" cy="935" rx="300" ry="135" fill="#3a2414"/><ellipse cx="430" cy="925" rx="280" ry="118" fill="#5a3a20"/>'
    b += '<path d="M150 960 Q430 1000 710 960 L710 1000 Q430 1040 150 1000Z" fill="#7a5434"/>'
    b += '<path d="M520 830 L1010 700 L1010 900 Z" fill="#fff4c0" opacity=".28" filter="url(#blur14)"/>'
    lamp = HARDHAT + '<circle cx="34" cy="-86" r="9" fill="#fff8d0" stroke-width="3"/>'
    pick = ('<path d="M-60 -10 L-96 -90" stroke="#7a4a1c" stroke-width="8" stroke-linecap="round"/>'
            '<path d="M-130 -84 Q-96 -112 -58 -96" fill="none" stroke="#7d8790" stroke-width="10" stroke-linecap="round"/>')
    b += frog(420, 990, 2.8, look=(5, 0), mouth='o', armL='M-34 -24 q-18 4 -24 14', armR='M38 -24 q22 -12 30 -34', back=pick, top=lamp)
    for (x, y, s) in ((cx - 420, GY - 40, 20), (cx + 430, GY - 20, 18), (cx, 1010, 22), (cx + 300, 760, 14)):
        b += spark(x, y, s, '#fff6d0', .9)
    return page('#1a6fb0', svg(d, b), [(170, [('CONCRETE', 'w')]), (190, [('ROOTS', 'y')])], outline='#0e2238')


# =========================== short3: a stable tripod (Y plan from above) ===========================
def s3():
    rnd = random.Random(31); d = FILTERS
    cx, cy = 1280, 630
    d += rad('sand', cx, cy, 1200, [(0, '#f2cf92', 1), (.6, '#dca866', 1), (1, '#9a6a3a', 1)])
    b = '<rect width="1920" height="1080" fill="url(#sand)"/>'
    # lake + park around the tower, roads
    b += f'<path d="M{cx - 520} {cy + 260} Q{cx - 300} {cy + 470} {cx + 80} {cy + 450} Q{cx + 420} {cy + 430} {cx + 520} {cy + 230} Q{cx + 380} {cy + 330} {cx} {cy + 340} Q{cx - 360} {cy + 350} {cx - 520} {cy + 260}Z" fill="#3fb0c0" stroke="#1d6a78" stroke-width="5"/>'
    b += f'<path d="M{cx - 420} {cy + 320} Q{cx} {cy + 410} {cx + 400} {cy + 300}" fill="none" stroke="#bff2f6" stroke-width="5" opacity=".7"/>'
    b += f'<circle cx="{cx}" cy="{cy}" r="500" fill="#7fae5a" opacity=".55"/><circle cx="{cx}" cy="{cy}" r="500" fill="none" stroke="#5a8a40" stroke-width="6" opacity=".6"/>'
    for (path, w) in ((f'M-40 {cy - 380} Q600 {cy - 300} {cx - 300} {cy - 560} L{cx - 240} -40', 46), (f'M{cx + 520} -40 Q{cx + 560} {cy} 1960 {cy + 120}', 46)):
        b += f'<path d="{path}" fill="none" stroke="#6a6a72" stroke-width="{w}"/><path d="{path}" fill="none" stroke="#f6f0d8" stroke-width="3" stroke-dasharray="22 18"/>'
    for k in range(70):   # trees (dots) in the park
        a = rnd.uniform(0, 6.28); r = rnd.uniform(420, 490)
        x, y = cx + r * math.cos(a), cy + r * math.sin(a)
        if x > 1640 and y > 930: continue
        b += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{rnd.randint(9, 14)}" fill="#3f7a32" stroke="#22461c" stroke-width="2"/>'
    # long shadow cast to the upper right
    b += f'<path d="M{cx - 60} {cy - 40} L{cx + 640} {cy - 600} L{cx + 700} {cy - 560} L{cx + 70} {cy + 40}Z" fill="#3a2414" opacity=".35" filter="url(#blur14)"/>'
    # ---- stepped Y tiers (each wing steps back, spiralling) ----
    tiers = [(470, 96), (400, 84), (335, 72), (270, 62), (210, 52), (152, 44), (100, 38), (60, 32)]
    cols = ['#3c5a80', '#4d6d94', '#5f80a8', '#7393bb', '#88a8cc', '#a0bede', '#bcd4ec', '#dcebfa']
    wings = (90, 210, 330)
    hexr = 70
    for t, ((Lw, hw), col) in enumerate(zip(tiers, cols)):
        shapes = []
        for k, a in enumerate(wings):
            Lk = Lw - (k * 22 if t % 3 else 0) - (t % 3) * 10 * k
            shapes.append(f'<g transform="translate({cx} {cy}) rotate({a - 90})"><rect x="{-hw}" y="0" width="{2 * hw}" height="{Lk}" rx="{hw * .9:.0f}"/></g>')
        hexpts = ' '.join(f'{cx + (hexr + 40 - t * 3) * math.cos(math.radians(30 + 60 * i)):.1f},{cy + (hexr + 40 - t * 3) * math.sin(math.radians(30 + 60 * i)):.1f}' for i in range(6))
        shapes.append(f'<polygon points="{hexpts}"/>')
        b += f'<g fill="none" stroke="{INK}" stroke-width="12">{"".join(shapes)}</g>'
        b += f'<g fill="{col}" stroke="none">{"".join(shapes)}</g>'
        # lit edge (light from lower-left)
        b += f'<g fill="none" stroke="#ffffff" stroke-width="3" opacity=".35" transform="translate(-3 3)">{"".join(shapes)}</g>'
    # window grid hint on the lowest tier wings
    for a in wings:
        for r in range(140, 460, 30):
            x, y = cx + r * math.cos(math.radians(a)), cy + r * math.sin(math.radians(a))
            b += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="3" fill="#ffffff" opacity=".35"/>'
    # ---- x-ray glowing hexagonal core + wings bracing it ----
    hexpts = ' '.join(f'{cx + hexr * math.cos(math.radians(30 + 60 * i)):.1f},{cy + hexr * math.sin(math.radians(30 + 60 * i)):.1f}' for i in range(6))
    b += f'<circle cx="{cx}" cy="{cy}" r="200" fill="#ffd27a" opacity=".45" filter="url(#blur30)"/>'
    for a in wings:
        x2, y2 = cx + 430 * math.cos(math.radians(a)), cy + 430 * math.sin(math.radians(a))
        b += f'<path d="M{cx} {cy} L{x2:.0f} {y2:.0f}" stroke="#ffd27a" stroke-width="26" opacity=".45" filter="url(#blur8)"/>'
        b += f'<path d="M{cx} {cy} L{x2:.0f} {y2:.0f}" stroke="#fff1c2" stroke-width="7" stroke-linecap="round"/>'
    b += f'<polygon points="{hexpts}" fill="#f6d488" stroke="#6a4416" stroke-width="6" opacity=".95"/>'
    b += f'<polygon points="{hexpts}" fill="none" stroke="#fff7d8" stroke-width="3" transform="translate(-4 4)"/>'
    b += f'<circle cx="{cx}" cy="{cy}" r="16" fill="#ffffff"/>' + spark(cx, cy, 46, '#fffbe8', 1)
    # tiny cars on the road for scale
    for (x, y, c) in ((420, 250, '#c0443e'), (520, 260, '#2f6fa8'), (1820, 760, '#e0a531')):
        b += f'<rect x="{x}" y="{y}" width="26" height="14" rx="4" fill="{c}" stroke="{INK}" stroke-width="2"/>'
    # ---- frog in a hot-air balloon, peeking down ----
    bxc, byc = 400, 640
    d += rad('bal', bxc - 50, byc - 70, 230, [(0, '#ffe7a0', 1), (.5, '#f2a64a', 1), (1, '#b8562a', 1)])
    b += f'<ellipse cx="{bxc + 30}" cy="{byc + 470}" rx="120" ry="24" fill="#3a2414" opacity=".25" filter="url(#blur8)"/>'
    b += f'<path d="M{bxc - 160} {byc} C{bxc - 170} {byc - 220} {bxc + 170} {byc - 220} {bxc + 160} {byc} C{bxc + 150} {byc + 90} {bxc + 50} {byc + 150} {bxc + 40} {byc + 190} L{bxc - 40} {byc + 190} C{bxc - 50} {byc + 150} {bxc - 150} {byc + 90} {bxc - 160} {byc}Z" fill="url(#bal)" stroke="{INK}" stroke-width="6"/>'
    for k, off in enumerate((-90, 0, 90)):
        b += f'<path d="M{bxc + off * .2} {byc - 168} C{bxc + off * 1.4} {byc - 120} {bxc + off * 1.3} {byc + 80} {bxc + off * .35} {byc + 188}" fill="none" stroke="#c0443e" stroke-width="16" opacity=".8"/>'
    b += f'<path d="M{bxc - 110} {byc - 110} q30 -50 90 -60" fill="none" stroke="#fff6d8" stroke-width="10" stroke-linecap="round" opacity=".8"/>'
    for sx in (-38, 38):
        b += f'<path d="M{bxc + sx} {byc + 190} L{bxc + sx * 1.6} {byc + 270}" stroke="#5a3a1a" stroke-width="4"/>'
    goggles = ('<path d="M-26 -84 q32 -14 62 0" fill="none" stroke="#5a3a1a" stroke-width="7"/>'
               '<circle cx="-8" cy="-86" r="10" fill="#7fd6e6" stroke-width="3.5"/><circle cx="22" cy="-86" r="10" fill="#7fd6e6" stroke-width="3.5"/>')
    b += frog(bxc + 4, byc + 330, 2.3, look=(5, 5), mouth='o', armL='M-34 -24 q-14 0 -16 14', armR='M38 -24 q26 -4 34 6', top=goggles)
    # basket in front of the frog's body
    bt = byc + 268
    b += f'<path d="M{bxc - 82} {bt} H{bxc + 82} L{bxc + 66} {bt + 90} H{bxc - 66}Z" fill="#b07a3c" stroke="{INK}" stroke-width="6"/>'
    for k in range(1, 6):
        b += f'<path d="M{bxc - 82 + k * 27} {bt + 4} L{bxc - 80 + k * 26} {bt + 86}" stroke="#7a4a1c" stroke-width="3"/>'
    b += f'<path d="M{bxc - 86} {bt} H{bxc + 86}" stroke="#7a4a1c" stroke-width="14" stroke-linecap="round"/>'
    for (x, y, s) in ((cx - 380, 220, 20), (cx + 400, 380, 24), (cx + 330, 820, 16)):
        b += spark(x, y, s, '#fffbe8', .9)
    return page('#dca866', svg(d, b), [(130, [('A STABLE', 'w')]), (196, [('TRIPOD', 'y')])], outline='#2a1a0c')


# =========================== short4: it won't tumble (ski poles = outriggers) ===========================
def pole(x1, y1, x2, y2, w=14, basket=40):
    dx, dy = x2 - x1, y2 - y1; Ln = math.hypot(dx, dy); ux, uy = dx / Ln, dy / Ln
    bx, by = x2 - ux * basket * 1.4, y2 - uy * basket * 1.4
    o = f'<path d="M{x1:.0f} {y1:.0f} L{x2:.0f} {y2:.0f}" stroke="{INK}" stroke-width="{w + 7}" stroke-linecap="round"/>'
    o += f'<path d="M{x1:.0f} {y1:.0f} L{x2:.0f} {y2:.0f}" stroke="#d64a3e" stroke-width="{w}" stroke-linecap="round"/>'
    o += f'<path d="M{x1 - uy * 3:.0f} {y1 + ux * 3:.0f} L{x2 - uy * 3:.0f} {y2 + ux * 3:.0f}" stroke="#ff9a8a" stroke-width="{w * .3:.0f}" stroke-linecap="round"/>'
    o += f'<ellipse cx="{bx:.0f}" cy="{by:.0f}" rx="{basket}" ry="{basket * .32:.0f}" fill="none" stroke="{INK}" stroke-width="{w * .9:.0f}"/>'
    o += f'<ellipse cx="{bx:.0f}" cy="{by:.0f}" rx="{basket}" ry="{basket * .32:.0f}" fill="none" stroke="#f2b632" stroke-width="{w * .45:.0f}"/>'
    return o


def s4():
    rnd = random.Random(41); d = FILTERS; HZ = 760
    d += lin('sky', [(0, '#0f4c8a'), (.55, '#4fa3e0'), (1, '#d8f0ff')])
    d += lin('snow', [(0, '#ffffff'), (.5, '#e4f1fb'), (1, '#a9c8e4')])
    b = f'<rect width="1920" height="{HZ + 40}" fill="url(#sky)"/>'
    b += '<circle cx="1760" cy="140" r="54" fill="#fffbe8"/><circle cx="1760" cy="140" r="160" fill="#fff4c0" opacity=".35" filter="url(#blur30)"/>'
    # snowy mountains
    for (pts, col) in (([(620, 760), (900, 430), (1080, 600), (1260, 380), (1520, 640), (1700, 470), (1980, 760)], '#6f95c4'),
                        ([(0, 760), (220, 560), (420, 680), (640, 520), (900, 760)], '#86a8d4')):
        pp = ' '.join(f'{x},{y}' for x, y in pts)
        b += f'<polygon points="{pp}" fill="{col}"/>'
        for i in range(1, len(pts) - 1):
            x, y = pts[i]
            b += f'<path d="M{x - 60} {y + 70} L{x} {y} L{x + 60} {y + 70} L{x + 30} {y + 55} L{x + 5} {y + 78} L{x - 25} {y + 56}Z" fill="#f4faff"/>'
    for (x, y, s) in ((420, 400, 1.0), (1500, 260, .8)):
        b += cloud(x, y, s)
    b += f'<path d="M0 {HZ - 20} Q600 {HZ + 40} 1200 {HZ - 10} T1920 {HZ + 20} V1080 H0Z" fill="url(#snow)"/>'
    b += f'<path d="M0 {HZ - 20} Q600 {HZ + 40} 1200 {HZ - 10} T1920 {HZ + 20}" fill="none" stroke="#ffffff" stroke-width="5"/>'
    for k in range(18):   # ski tracks / snow texture
        x = rnd.randint(0, 1500); y = rnd.randint(HZ + 60, 1060)
        b += f'<path d="M{x} {y} q{rnd.randint(60, 140)} -12 {rnd.randint(160, 300)} 4" fill="none" stroke="#9fbde0" stroke-width="3" opacity=".5"/>'
    # ---- the tower, planting two giant ski poles ----
    cx, base, H, W = 1360, 930, 880, 300
    b += f'<ellipse cx="{cx}" cy="{base + 10}" rx="420" ry="40" fill="#7fa3cc" opacity=".55" filter="url(#blur8)"/>'
    yatt = base - .28 * H
    d2, b2 = tower(cx, base, H, W, dict(
        faces=[('#4f6f96', '#a8c8ea'), ('#6688b0', '#cfe4f8'), ('#3e5c84', '#86a8d0'), ('#2f4c74', '#6a8cb8')],
        edge='#13233c', rim='#fff4c8', rimside='L', band='#1c3456', line='#18304e', glow='#fff6d0', glowop=.5), 'tw')
    d += d2
    poles = pole(cx - 70, yatt, cx - 400, base + 20, 16, 46) + pole(cx + 70, yatt, cx + 360, base + 10, 16, 46)
    b += b2
    # glowing outrigger band where the poles are held (mechanical floor)
    b += f'<rect x="{cx - 160}" y="{yatt - 16}" width="320" height="32" fill="#ffd27a" opacity=".7" filter="url(#blur8)"/>'
    b += f'<rect x="{cx - 120}" y="{yatt - 8}" width="240" height="16" rx="6" fill="#ffe7a0" stroke="#6a4416" stroke-width="3"/>'
    b += poles
    for (x, y) in ((cx - 400, base + 24), (cx + 360, base + 14)):   # snow puffs where poles plant
        b += f'<ellipse cx="{x}" cy="{y}" rx="70" ry="16" fill="#ffffff" filter="url(#blur4)"/>'
        for k in range(6):
            b += f'<circle cx="{x + rnd.randint(-60, 60)}" cy="{y - rnd.randint(4, 34)}" r="{rnd.randint(4, 8)}" fill="#ffffff" stroke="#9fbde0" stroke-width="2"/>'
    # wind lines hitting the tower from the left
    for k, y in enumerate((300, 420, 560)):
        b += f'<path d="M{cx - 560} {y} q120 -20 260 0 q60 8 90 -10" fill="none" stroke="#ffffff" stroke-width="6" stroke-linecap="round" opacity=".75"/>'
    # ---- frog skier, poles planted wide ----
    fx, fy, fs = 600, 960, 2.7
    skis = (f'<path d="M-60 8 L100 0 q18 -2 24 -16" fill="none" stroke="{INK}" stroke-width="15" stroke-linecap="round"/>'
            f'<path d="M-60 8 L100 0 q18 -2 24 -16" fill="none" stroke="#2f6fa8" stroke-width="8" stroke-linecap="round"/>'
            f'<path d="M-74 18 L86 12 q18 -2 24 -16" fill="none" stroke="{INK}" stroke-width="15" stroke-linecap="round"/>'
            f'<path d="M-74 18 L86 12 q18 -2 24 -16" fill="none" stroke="#2f6fa8" stroke-width="8" stroke-linecap="round"/>')
    beanie = ('<path d="M-28 -78 q32 -40 66 0z" fill="#c0443e" stroke-width="3"/><rect x="-32" y="-82" width="74" height="12" rx="5" fill="#f4f1ea" stroke-width="2.6"/>'
              '<circle cx="6" cy="-112" r="10" fill="#f4f1ea" stroke-width="2.6"/>'
              '')
    scarf = ('<path d="M-30 -30 q36 12 70 -2" fill="none" stroke="#1d2b1c" stroke-width="15" stroke-linecap="round"/>'
             '<path d="M-30 -30 q36 12 70 -2" fill="none" stroke="#e0a531" stroke-width="10" stroke-linecap="round"/>'
             '<path d="M-28 -30 q-30 -4 -54 -22 q-6 10 4 18 q22 12 48 10z" fill="#e0a531" stroke-width="3"/>')
    fpoles = (f'<path d="M-62 -6 L-96 34" stroke="{INK}" stroke-width="9" stroke-linecap="round"/><path d="M-62 -6 L-96 34" stroke="#d64a3e" stroke-width="5" stroke-linecap="round"/>'
              f'<ellipse cx="-92" cy="30" rx="14" ry="5" fill="none" stroke="#f2b632" stroke-width="3.5"/>'
              f'<path d="M66 -6 L104 34" stroke="{INK}" stroke-width="9" stroke-linecap="round"/><path d="M66 -6 L104 34" stroke="#d64a3e" stroke-width="5" stroke-linecap="round"/>'
              f'<ellipse cx="100" cy="30" rx="14" ry="5" fill="none" stroke="#f2b632" stroke-width="3.5"/>')
    b += f'<ellipse cx="{fx + 30}" cy="{fy + 40}" rx="300" ry="26" fill="#9fbde0" opacity=".6" filter="url(#blur8)"/>'
    b += frog(fx, fy, fs, look=(5, -3), mouth='o', rot_=-4, armL='M-34 -22 q-18 0 -28 16', armR='M38 -22 q18 0 28 16',
              feet=((-22, 6, -10), (22, 6, 10)), back=skis, front=scarf, top=beanie + fpoles)
    for k in range(14):   # snow spray behind the skier
        b += f'<circle cx="{fx - 360 + rnd.randint(0, 120)}" cy="{fy + rnd.randint(-80, 30)}" r="{rnd.randint(5, 12)}" fill="#ffffff" stroke="#b8d0ea" stroke-width="2"/>'
    for (x, y, s) in ((cx - 260, 240, 20), (cx + 300, 360, 24), (980, 620, 16)):
        b += spark(x, y, s, '#ffffff', .95)
    return page('#0f4c8a', svg(d, b), [(150, [("IT WON'T", 'w')]), (196, [('TUMBLE', 'y')])], outline='#0a1a33')


# =========================== short5: first test failed (wind tunnel) ===========================
def s5():
    rnd = random.Random(51); d = FILTERS
    d += lin('lab', [(0, '#0b1626'), (.7, '#16304a'), (1, '#0a1420')])
    d += lin('win', [(0, '#bfeaf6'), (.5, '#e8fbff'), (1, '#9fd6e8')])
    b = '<rect width="1920" height="1080" fill="url(#lab)"/>'
    # back wall panels + pipes
    for k in range(9):
        b += f'<rect x="{k * 220 - 20}" y="0" width="210" height="900" fill="#1b3550" opacity=".35" stroke="#0a1626" stroke-width="4"/>'
    b += '<path d="M0 200 H1920" stroke="#2c4a68" stroke-width="20"/><path d="M0 194 H1920" stroke="#4f7090" stroke-width="4"/>'
    b += '<rect y="900" width="1920" height="180" fill="#0c1a2a"/><path d="M0 900 H1920" stroke="#2c4a68" stroke-width="5"/>'
    # ---- test section window ----
    x0, y0, x1, y1 = 840, 250, 1880, 860
    b += f'<rect x="{x0 - 30}" y="{y0 - 30}" width="{x1 - x0 + 60}" height="{y1 - y0 + 60}" rx="30" fill="#4f6478" stroke="{INK}" stroke-width="7"/>'
    b += f'<rect x="{x0 - 30}" y="{y0 - 30}" width="{x1 - x0 + 60}" height="16" rx="8" fill="#9fb4c8"/>'
    for t in range(14):   # bolts
        bx = x0 - 14 + t * (x1 - x0 + 28) / 13
        b += f'<circle cx="{bx:.0f}" cy="{y0 - 14}" r="5" fill="#c8d6e2" stroke="{INK}" stroke-width="2"/><circle cx="{bx:.0f}" cy="{y1 + 14}" r="5" fill="#c8d6e2" stroke="{INK}" stroke-width="2"/>'
    b += f'<clipPath id="wc"><rect x="{x0}" y="{y0}" width="{x1 - x0}" height="{y1 - y0}" rx="14"/></clipPath>'
    inner = f'<rect x="{x0}" y="{y0}" width="{x1 - x0}" height="{y1 - y0}" fill="url(#win)"/>'
    inner += f'<ellipse cx="{x0 + 380}" cy="{y0 + 300}" rx="420" ry="300" fill="#ffffff" opacity=".6" filter="url(#blur60)"/>'
    # honeycomb inlet on the left
    for r in range(0, 22):
        for c in range(3):
            hx, hy = x0 + 16 + c * 26 + (13 if r % 2 else 0), y0 + 14 + r * 28
            inner += f'<polygon points="' + ' '.join(f'{hx + 12 * math.cos(math.radians(60 * i)):.0f},{hy + 12 * math.sin(math.radians(60 * i)):.0f}' for i in range(6)) + '" fill="#d8e8f0" stroke="#6a8aa0" stroke-width="2"/>'
    # turntable floor
    mcx, mbase = 1130, 820
    inner += f'<rect x="{x0}" y="{mbase}" width="{x1 - x0}" height="{y1 - mbase}" fill="#7d93a8"/>'
    inner += f'<ellipse cx="{mcx}" cy="{mbase + 6}" rx="200" ry="26" fill="#c8d6e2" stroke="{INK}" stroke-width="4"/>'
    # smoke streamlines from the inlet toward the model
    for k, y in enumerate(range(y0 + 50, mbase - 20, 46)):
        pth = f'M{x0 + 90} {y} C{x0 + 250} {y + 6} {mcx - 260} {y - 4} {mcx - 120} {y + (8 if k % 2 else -8)}'
        inner += f'<path d="{pth}" fill="none" stroke="#ffffff" stroke-width="16" opacity=".45" filter="url(#blur4)"/>'
        inner += f'<path d="{pth}" fill="none" stroke="#5a7fa0" stroke-width="4" opacity=".7" stroke-dasharray="40 14"/>'
    # alternating vortices peeling off behind the model (vortex shedding)
    vs = [(1300, 420, 70, 1), (1440, 640, 90, 1 * -1), (1580, 400, 100, 1), (1730, 650, 110, -1), (1860, 420, 110, 1)]
    for (vx, vy, r, cw) in vs:
        sp = spiral(vx, vy, r, 1.7, cw, 0 if cw > 0 else math.pi)
        inner += f'<path d="{sp}" fill="none" stroke="#ffffff" stroke-width="30" opacity=".55" filter="url(#blur8)"/>'
        inner += f'<path d="{sp}" fill="none" stroke="#3f6a90" stroke-width="7" stroke-linecap="round"/>'
        inner += f'<path d="{sp}" fill="none" stroke="#ffffff" stroke-width="3" stroke-linecap="round" opacity=".8"/>'
    inner += f'<path d="M{mcx + 60} 470 C1240 430 1260 410 1300 420 M{mcx + 60} 620 C1300 660 1380 650 1440 640" fill="none" stroke="#3f6a90" stroke-width="6" opacity=".7"/>'
    b += f'<g clip-path="url(#wc)">{inner}'
    # the model tower on the turntable, swaying (drawn slightly tilted)
    d2, b2 = tower(mcx, mbase, 560, 190, dict(
        faces=[('#8a9aa8', '#dfe8ee'), ('#a0b0bc', '#f2f8fb'), ('#76889a', '#c4d2dc'), ('#647688', '#a8b8c6')],
        edge='#1d2b3a', rim='#ffffff', rimside='L', band='#5a6c7e', line='#4a5c6e', glow='#ffffff', glowop=.3), 'md')
    d += d2
    b += f'<g transform="rotate(4 {mcx} {mbase})">{b2}</g>'
    for k in (1, 2):   # sway marks
        b += f'<path d="M{mcx - 50 - k * 26} {mbase - 470 + k * 10} q-14 50 0 100" fill="none" stroke="#c0443e" stroke-width="7" stroke-linecap="round" opacity=".85"/>'
        b += f'<path d="M{mcx + 50 + k * 26} {mbase - 470 + k * 10} q14 50 0 100" fill="none" stroke="#c0443e" stroke-width="7" stroke-linecap="round" opacity=".85"/>'
    b += '</g>'
    b += f'<path d="M{x0 + 30} {y0 + 30} L{x0 + 260} {y0 + 30} L{x0 + 120} {y1 - 30} L{x0 + 30} {y1 - 30}Z" fill="#ffffff" opacity=".10"/>'
    # warning lamp on the frame
    b += f'<circle cx="{x1 - 40}" cy="{y0 - 60}" r="40" fill="#ff5a4a" opacity=".55" filter="url(#blur14)"/><rect x="{x1 - 60}" y="{y0 - 82}" width="40" height="36" rx="10" fill="#ff7a6a" stroke="{INK}" stroke-width="4"/>'
    # ---- frog scientist in a lab coat with goggles, pressed to the glass ----
    coat = ('<path d="M-33 -34 q-4 30 -2 38 q36 10 76 0 q2 -10 -2 -38 q-36 12 -72 0z" fill="#f4f6fa" stroke-width="3.2"/>'
            '<path d="M2 -32 l-12 24 M10 -32 l12 24" stroke="#9aa8b8" stroke-width="3"/><rect x="24" y="-18" width="12" height="10" fill="#7fd6e6" stroke-width="2"/>')
    gog = ('<path d="M-26 -84 q32 -14 62 0" fill="none" stroke="#3a3a3a" stroke-width="7"/>'
           '<circle cx="-8" cy="-86" r="11" fill="#ffd27a" fill-opacity=".7" stroke-width="3.5"/><circle cx="22" cy="-86" r="11" fill="#ffd27a" fill-opacity=".7" stroke-width="3.5"/>')
    clip = ('<rect x="-92" y="-40" width="44" height="58" rx="5" fill="#b07a3c" stroke-width="3"/><rect x="-86" y="-30" width="32" height="42" fill="#ffffff" stroke-width="2"/>'
            '<path d="M-82 -20 h22 M-82 -10 h22 M-82 0 h16" stroke="#9aa8b8" stroke-width="2.5"/>')
    b += frog(500, 1010, 3.0, look=(6, -3), mouth='o', armL='M-34 -22 q-20 4 -24 18', armR='M38 -24 q24 -14 34 -40', front=coat, back=clip, top=gog)
    for (x, y, s) in ((700, 520, 18), (1500, 280, 18), (300, 640, 14)):
        b += spark(x, y, s, '#e8fbff', .9)
    return page('#0b1626', svg(d, b), [(118, [('FIRST TEST:', 'w')]), (196, [('FAILED', 'y')])], outline='#050b18')


if __name__ == '__main__':
    for n, f in ((1, s1), (2, s2), (3, s3), (4, s4), (5, s5)):
        out = os.path.join(VID, f'hollow-skyscraper-short{n}', 'thumb'); os.makedirs(out, exist_ok=True)
        for fn in ('common.css', 'Fredoka-700.woff2'):
            if not os.path.exists(os.path.join(out, fn)): shutil.copy(os.path.join(LONG, fn), out)
        open(os.path.join(out, 'A.html'), 'w').write(f())
    print('ok')
