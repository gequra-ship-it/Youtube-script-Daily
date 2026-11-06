# Shorts thumbnails (guideline 16-9) for hollow-skyscraper-short1..5 (Burj Khalifa). Opus thumb agent 2026-11-06, v2 VERTICAL.
# Owner 2026-11-06: shorts thumbnails are 9:16 (1080x1920), text centred (horizontal centre, vertically near the middle),
# no bottom-right-empty / top-left rule; frog kept; nothing important at the very top/bottom (YouTube UI).
# Layout for all five: main picture in the upper part (y ~150-860), centred text band (~y 860-1320), frog + second element below (~1320-1700).
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
TOOLS = os.path.join(VID, '..', 'tools')
LONG = os.path.join(VID, 'hollow-skyscraper', 'thumb')
sys.path.insert(0, TOOLS)
spec = importlib.util.spec_from_file_location('longmake', os.path.join(LONG, 'make.py'))
L = importlib.util.module_from_spec(spec); spec.loader.exec_module(L)
from thumb_lib import vsvg, lin, rad, spark
frog, tower, FILTERS, HARDHAT, INK, HEAD = L.frog, L.tower, L.FILTERS, L.HARDHAT, L.INK, L.HEAD


def vpage(bg, art, lines, outline='#0b0f24', top=880):
    """Vertical page, text centred. lines: [(size, [(text, 'w'|'y'), ...]), ...] - one yellow word."""
    css = (f'body{{background:{bg}}}.o{{-webkit-text-stroke:17px {outline};paint-order:stroke fill}}.g{{color:#F2D27A}}')
    html = ''; y = top
    for k, (sz, segs) in enumerate(lines):
        css += (f'#t{k}{{left:0;width:1080px;text-align:center;top:{y}px;font-size:{sz}px;letter-spacing:3px;line-height:1;'
                f'filter:drop-shadow(0 10px 12px rgba(0,0,0,.5))}}')
        inner = ''.join(f'<span class="g">{t}</span>' if c == 'y' else t for t, c in segs)
        html += f'<div class="txt o" id="t{k}">{inner}</div>'
        y += int(sz * 0.98)
    return HEAD % css + art + html + '</div></body></html>'


def band(y0, y1, col='#000000', op=.35):
    """soft dark band behind the text so it pops (depth)."""
    return f'<ellipse cx="540" cy="{(y0 + y1) / 2}" rx="620" ry="{(y1 - y0) / 2 + 40}" fill="{col}" opacity="{op}" filter="url(#blur60)"/>'


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
    rnd = random.Random(11); d = FILTERS; HZ = 1300
    d += lin('sky', [(0, '#0f3a4c'), (.35, '#2f7d86'), (.75, '#9fcf9a'), (1, '#f6dc96')])
    d += lin('gnd', [(0, '#7aa04a'), (.4, '#4f7a34'), (1, '#1f3818')])
    d += rad('sun', 540, 470, 640, [(0, '#fffbe0', .95), (.2, '#fff0b0', .55), (.6, '#ffe08a', .15), (1, '#ffe08a', 0)])
    b = f'<rect width="1080" height="{HZ}" fill="url(#sky)"/><rect width="1080" height="{HZ}" fill="url(#sun)"/>'
    for (x, y, s) in ((180, 260, 1.0), (930, 380, .8), (160, 700, .7)):
        b += cloud(x, y, s, '#f4fff6', .6)
    # distant hills + the Burj Khalifa far behind, glowing
    b += f'<path d="M0 {HZ - 60} Q260 {HZ - 130} 540 {HZ - 50} T1080 {HZ - 70} V{HZ + 5} H0Z" fill="#5f8f78" opacity=".7"/>'
    d2, b2 = tower(860, HZ - 40, 900, 250, dict(
        faces=[('#5f8aa0', '#c0e2ea'), ('#78a2b6', '#e2f4f6'), ('#4a7488', '#9cc4cf'), ('#3a6074', '#80a8b6')],
        edge='#163040', rim='#fff2c0', rimside='L', band='#2a4a5a', line='#244252', glow='#fff2b0', glowop=.35), 'tw')
    d += d2; b += f'<g opacity=".8">{b2}</g>'
    b += f'<rect y="{HZ}" width="1080" height="{1920 - HZ}" fill="url(#gnd)"/>'
    b += f'<path d="M0 {HZ + 20} Q300 {HZ - 10} 600 {HZ + 30} T1080 {HZ + 10}" fill="none" stroke="#d6e98a" stroke-width="4" opacity=".6"/>'
    for k in range(60):   # grass tufts
        gx = rnd.randint(0, 1070); gy = rnd.randint(HZ + 30, 1900)
        b += f'<path d="M{gx} {gy} l-6 -{rnd.randint(14, 26)} M{gx} {gy} l2 -{rnd.randint(18, 30)} M{gx} {gy} l9 -{rnd.randint(12, 22)}" stroke="#a8cf62" stroke-width="3" opacity=".7"/>'

    # ---- giant bamboo stalk, cut open in the upper part (main picture) ----
    bx, bw = 420, 230
    d += lin('bam', [(0, '#2f5a1c'), (.18, '#5d9a34'), (.42, '#b8e27a'), (.6, '#86c04c'), (1, '#2b4f18')], x2=1, y2=0)
    d += lin('bin', [(0, '#a88a4a'), (.2, '#e6d39a'), (.5, '#fff4cc'), (.8, '#e0c98a'), (1, '#9a7c40')], x2=1, y2=0)
    b += f'<ellipse cx="{bx}" cy="520" rx="330" ry="560" fill="#fff6c0" opacity=".38" filter="url(#blur60)"/>'
    b += f'<rect x="{bx - bw / 2}" y="-20" width="{bw}" height="{HZ + 60}" fill="url(#bam)" stroke="{INK}" stroke-width="7"/>'
    nodes = [70, 330, 610, 900, 1180]
    wy0, wy1 = 170, 800
    b += f'<rect x="{bx - bw / 2 + 26}" y="{wy0}" width="{bw - 52}" height="{wy1 - wy0}" rx="12" fill="url(#bin)" stroke="#3a4a18" stroke-width="6"/>'
    b += f'<rect x="{bx - bw / 2 + 26}" y="{wy0}" width="22" height="{wy1 - wy0}" fill="#6a5424" opacity=".35"/>'
    for ny in nodes:
        if wy0 < ny < wy1:   # diaphragm (solid ring) across the hollow
            b += f'<ellipse cx="{bx}" cy="{ny}" rx="{bw / 2 - 26}" ry="17" fill="#c8a85a" stroke="#5a4418" stroke-width="5"/>'
            b += f'<ellipse cx="{bx}" cy="{ny - 5}" rx="{bw / 2 - 40}" ry="8" fill="#f6e2a8"/>'
    for (yy, s) in ((240, .6), (470, .8), (730, .55)):   # empty air inside
        b += spark(bx, yy, 24 * s + 10, '#ffffff', .9)
    for ny in nodes:   # outer node rings
        b += f'<path d="M{bx - bw / 2 - 7} {ny} Q{bx} {ny + 26} {bx + bw / 2 + 7} {ny}" fill="none" stroke="{INK}" stroke-width="10"/>'
        b += f'<path d="M{bx - bw / 2 - 2} {ny - 7} Q{bx} {ny + 16} {bx + bw / 2 + 2} {ny - 7}" fill="none" stroke="#d6f29a" stroke-width="5"/>'
    b += f'<path d="M{bx - 46} {wy1 + 14} V{HZ + 20}" stroke="#eaffc0" stroke-width="12" opacity=".5" stroke-linecap="round"/>'
    for (ny, side, ang) in ((330, 1, -24), (70, -1, 12), (610, 1, 18), (900, -1, -14)):   # leaves
        lx = bx + side * bw / 2
        for k in range(3):
            a = ang + k * 22 * side
            b += (f'<g transform="translate({lx} {ny}) rotate({a}) scale({side} 1)"><path d="M0 0 q90 -40 220 -6 q-114 26 -220 6z" fill="#5e9a34" stroke="{INK}" stroke-width="4"/>'
                  f'<path d="M10 -2 q90 -18 200 -4" fill="none" stroke="#b8e27a" stroke-width="3"/></g>')

    # ---- hollow bird bone lying in the grass below the text, frog explorer on it ----
    gx, gy, ang = 600, 1600, -5
    d += lin('bone', [(0, '#fffaf0'), (.35, '#f3e6c8'), (.8, '#d8c39a'), (1, '#a8916a')])
    bone = f'<g transform="translate({gx} {gy}) rotate({ang})">'
    bone += '<ellipse cx="20" cy="66" rx="420" ry="30" fill="#1a2c12" opacity=".5" filter="url(#blur8)"/>'
    bone += f'<path d="M-300 -42 Q-60 -30 300 -48 L300 48 Q-60 34 -300 42Z" fill="url(#bone)" stroke="{INK}" stroke-width="6"/>'
    bone += f'<circle cx="-340" cy="-40" r="60" fill="url(#bone)" stroke="{INK}" stroke-width="6"/><circle cx="-342" cy="38" r="56" fill="url(#bone)" stroke="{INK}" stroke-width="6"/>'
    bone += '<path d="M-300 -40 Q-280 0 -300 40" fill="url(#bone)" stroke="none"/><rect x="-320" y="-36" width="40" height="72" fill="url(#bone)"/>'
    bone += '<path d="M-370 -76 q30 -18 60 -2" fill="none" stroke="#ffffff" stroke-width="7" stroke-linecap="round"/>'
    bone += '<path d="M-160 -22 Q40 -14 210 -26 L210 26 Q40 16 -160 22Z" fill="#7a4a3a" stroke="#4a2a20" stroke-width="4"/>'
    bone += '<path d="M-160 -22 Q40 -14 210 -26 L210 -14 Q40 -4 -160 -12Z" fill="#a8685a" opacity=".6"/>'
    zz = 'M-150 18 ' + ' '.join(f'L{-150 + 36 * k} {(-16 if k % 2 else 18)}' for k in range(1, 11))
    bone += f'<path d="{zz}" fill="none" stroke="#3a2015" stroke-width="12" stroke-linejoin="round"/><path d="{zz}" fill="none" stroke="#f6e8cc" stroke-width="7" stroke-linejoin="round"/>'
    bone += f'<ellipse cx="300" cy="0" rx="30" ry="50" fill="#f3e6c8" stroke="{INK}" stroke-width="6"/>'
    bone += '<ellipse cx="302" cy="0" rx="20" ry="38" fill="#5a3226"/>'
    bone += '<path d="M286 -30 L316 26 M310 -34 L292 30" stroke="#f6e8cc" stroke-width="5"/>'
    bone += '<path d="M-270 -30 Q-60 -22 270 -36" fill="none" stroke="#ffffff" stroke-width="6" opacity=".8" stroke-linecap="round"/>'
    bone += '</g>'
    b += f'<ellipse cx="{gx}" cy="{gy}" rx="460" ry="120" fill="#fff6c0" opacity=".25" filter="url(#blur30)"/>' + bone
    hat = ('<path d="M-40 -82 q46 -14 92 0 q-8 8 -46 8 q-38 0 -46 -8z" fill="#c9a060" stroke-width="3"/>'
           '<path d="M-22 -84 q28 -40 56 0z" fill="#d8b070" stroke-width="3"/><path d="M-20 -88 q28 6 52 0" fill="none" stroke="#7a4a1c" stroke-width="5"/>')
    lens = ('<path d="M54 -6 L80 -60" stroke="#5a3a1a" stroke-width="9" stroke-linecap="round"/>'
            '<circle cx="92" cy="-84" r="28" fill="#bfeaff" fill-opacity=".45" stroke="#3a2a14" stroke-width="7"/>'
            '<path d="M78 -94 q8 -10 20 -8" fill="none" stroke="#ffffff" stroke-width="4"/>')
    b += frog(330, 1584, 2.35, look=(5, 4), mouth='o', armL='M-34 -24 q-24 -6 -28 -34', armR='M38 -22 q16 6 18 18', top=hat + lens)
    for (x, y, s) in ((760, 600, 20), (700, 240, 16), (920, 1500, 16), (200, 520, 14)):
        b += spark(x, y, s, '#fffbe0', .9)
    b += band(860, 1300, '#06202a', .45)
    return vpage('#0f3a4c', vsvg(d, b), [(140, [("NATURE'S", 'w')]), (200, [('HOLLOW', 'y')]), (140, [('TRICK', 'w')])], outline='#0a2028', top=840)


# =========================== short2: concrete roots ===========================
def s2():
    rnd = random.Random(21); d = FILTERS; GY = 640
    d += lin('sky', [(0, '#1a6fb0'), (.6, '#6ec0e6'), (1, '#ffe2a8')])
    d += rad('sun', 880, 260, 300, [(0, '#fffbe6', 1), (.15, '#fff1b8', .8), (1, '#ffe08a', 0)])
    b = f'<rect width="1080" height="{GY}" fill="url(#sky)"/><rect width="1080" height="{GY}" fill="url(#sun)"/><circle cx="880" cy="260" r="44" fill="#fffbe8"/>'
    for (x, y, s) in ((170, 330, 1.0), (920, 480, .8)):
        b += cloud(x, y, s)
    x = 0
    while x < 1080:
        w = rnd.randint(14, 30); h = rnd.randint(12, 50)
        if not (300 < x < 780):
            b += f'<rect x="{x}" y="{GY - h}" width="{w}" height="{h + 4}" fill="#8fb0c4" opacity=".75"/>'
        x += w + rnd.randint(3, 14)
    layers = [('#e8b878', 0), ('#c89660', 120), ('#b07f50', 360), ('#94673f', 640), ('#7a5434', 920)]
    for k, (col, top) in enumerate(layers):
        y = GY + top
        b += f'<path d="M0 {y} Q270 {y - 18} 540 {y + 12} T1080 {y - 6} V1920 H0Z" fill="{col}"/>'
        if k:
            b += f'<path d="M0 {y} Q270 {y - 18} 540 {y + 12} T1080 {y - 6}" fill="none" stroke="#5a3a20" stroke-width="3" opacity=".45"/>'
    for k in range(260):   # grains (weak rock)
        px, py = rnd.randint(0, 1070), rnd.randint(GY + 30, 1910)
        b += f'<circle cx="{px}" cy="{py}" r="{rnd.choice([2, 3, 4])}" fill="{rnd.choice(["#f2cf98", "#5e3e24", "#d8a870"])}" opacity="{rnd.uniform(.3, .7):.2f}"/>'
    for k in range(18):
        px, py = rnd.randint(0, 1000), rnd.randint(GY + 80, 1880)
        b += f'<path d="M{px} {py} l{rnd.randint(10, 30)} {rnd.randint(-8, 8)} l{rnd.randint(10, 26)} {rnd.randint(-10, 10)}" fill="none" stroke="#4a2e18" stroke-width="2.5" opacity=".5"/>'
    b += f'<path d="M0 {GY} Q270 {GY - 10} 540 {GY + 6} T1080 {GY - 4} V{GY + 24} H0Z" fill="#f6d090"/>'
    b += f'<path d="M0 {GY} Q270 {GY - 10} 540 {GY + 6} T1080 {GY - 4}" fill="none" stroke="#fff0c8" stroke-width="4"/>'
    for px in (90, 960):
        b += f'<path d="M{px} {GY} q4 -50 10 -80" stroke="#7a5228" stroke-width="8" fill="none"/>'
        for (dx, dy) in ((-40, 10), (40, 6), (-30, -16), (34, -18), (0, -30)):
            b += f'<path d="M{px + 10} {GY - 80} q{dx * .5} {dy - 20} {dx} {dy + 10}" fill="none" stroke="#3f7a32" stroke-width="9" stroke-linecap="round"/>'
    cx = 540
    # ---- piles: long concrete roots ----
    d += lin('pile', [(0, '#7d7a72'), (.3, '#d8d4ca'), (.55, '#f4f1ea'), (1, '#8a867c')], x2=1, y2=0)
    d += rad('rglow', cx, GY + 300, 700, [(0, '#ffe4a0', .7), (.5, '#ffd27a', .25), (1, '#ffd27a', 0)])
    b += f'<ellipse cx="{cx}" cy="{GY + 480}" rx="560" ry="640" fill="url(#rglow)"/>'
    xs = [cx - 330 + 660 * i / 10 for i in range(11)]
    for i, x in enumerate(xs):
        depth = 1520 + rnd.randint(-20, 50) - abs(i - 5) * 16
        top = GY + 62; w = 36
        b += f'<rect x="{x - w / 2 - 6}" y="{top}" width="{w + 12}" height="{depth - top}" fill="#3a2a1a" opacity=".35" rx="16"/>'
        b += f'<path d="M{x - w / 2} {top} V{depth} Q{x} {depth + 30} {x + w / 2} {depth} V{top}Z" fill="url(#pile)" stroke="#2e2a24" stroke-width="4"/>'
        for k in range(3):
            a = rnd.uniform(-1, 1)
            b += f'<path d="M{x} {depth + 16} q{a * 18:.0f} 22 {a * 34:.0f} {rnd.randint(34, 56)}" fill="none" stroke="#c9c2b2" stroke-width="3.5" stroke-linecap="round"/>'
        b += f'<path d="M{x - 4} {top + 6} V{depth - 10}" stroke="#ffe7a0" stroke-width="6" opacity=".8" stroke-dasharray="30 20"/>'
    # ---- raft (thick concrete mat) ----
    rw, rt, rh = 380, GY + 6, 60
    d += lin('raft', [(0, '#fff6dc'), (.4, '#e2dccd'), (1, '#9a9488')])
    b += f'<rect x="{cx - rw - 20}" y="{rt - 16}" width="{2 * rw + 40}" height="{rh + 32}" rx="20" fill="#ffd27a" opacity=".6" filter="url(#blur14)"/>'
    b += f'<rect x="{cx - rw}" y="{rt}" width="{2 * rw}" height="{rh}" rx="8" fill="url(#raft)" stroke="#2e2a24" stroke-width="5"/>'
    b += f'<path d="M{cx - rw + 10} {rt + 8} H{cx + rw - 10}" stroke="#ffffff" stroke-width="5" opacity=".9"/>'
    for k in range(1, 12):
        b += f'<path d="M{cx - rw + k * 2 * rw / 12} {rt + 4} v{rh - 8}" stroke="#8a8478" stroke-width="2" opacity=".5"/>'
    # ---- tower standing on the raft ----
    d2, b2 = tower(cx, GY + 8, 500, 250, dict(
        faces=[('#6d8eb3', '#bfe0f5'), ('#86a8cc', '#dff1fb'), ('#9ec0de', '#f0fbff'), ('#b8d6ec', '#ffffff')],
        edge='#22344e', rim='#ffffff', rimside='R', band='#3d5a7c', line='#2c4766', glow='#fff3c4', glowop=.45), 'tw')
    d += d2; b += b2
    # ---- frog miner in a little cave bottom-left, headlamp on the root tips ----
    fx, fy = 200, 1660
    b += f'<ellipse cx="{fx + 10}" cy="{fy - 70}" rx="200" ry="140" fill="#3a2414"/><ellipse cx="{fx + 10}" cy="{fy - 80}" rx="184" ry="124" fill="#5a3a20"/>'
    b += f'<path d="M{fx - 180} {fy - 10} Q{fx} {fy + 30} {fx + 190} {fy - 10} L{fx + 190} {fy + 30} Q{fx} {fy + 70} {fx - 180} {fy + 30}Z" fill="#7a5434"/>'
    b += f'<path d="M{fx + 80} {fy - 230} L{fx + 560} {fy - 260} L{fx + 520} {fy - 70} Z" fill="#fff4c0" opacity=".3" filter="url(#blur14)"/>'
    lamp = HARDHAT + '<circle cx="34" cy="-86" r="9" fill="#fff8d0" stroke-width="3"/>'
    pick = ('<path d="M-60 -10 L-96 -90" stroke="#7a4a1c" stroke-width="8" stroke-linecap="round"/>'
            '<path d="M-130 -84 Q-96 -112 -58 -96" fill="none" stroke="#7d8790" stroke-width="10" stroke-linecap="round"/>')
    b += frog(fx, fy, 2.5, look=(5, -2), mouth='o', armL='M-34 -24 q-18 4 -24 14', armR='M38 -24 q22 -12 30 -34', back=pick, top=lamp)
    for (x, y, s) in ((cx - 420, GY - 50, 18), (cx + 420, GY - 30, 18), (cx + 150, 1640, 20), (cx + 380, 1500, 14)):
        b += spark(x, y, s, '#fff6d0', .9)
    b += band(890, 1300, '#2a1608', .45)
    return vpage('#1a6fb0', vsvg(d, b), [(176, [('CONCRETE', 'w')]), (236, [('ROOTS', 'y')])], outline='#1c1008', top=890)


# =========================== short3: a stable tripod (Y plan from above) ===========================
def s3():
    rnd = random.Random(31); d = FILTERS
    cx, cy, sc = 540, 560, .82
    d += rad('sand', cx, 900, 1300, [(0, '#f2cf92', 1), (.6, '#dca866', 1), (1, '#9a6a3a', 1)])
    b = '<rect width="1080" height="1920" fill="url(#sand)"/>'
    # roads
    for (path, w) in ((f'M-40 1180 Q300 1120 560 1240 T1120 1200', 44), (f'M140 -40 Q200 400 -40 760', 40), (f'M1120 120 Q900 380 1000 900 T1120 1500', 40)):
        b += f'<path d="{path}" fill="none" stroke="#6a6a72" stroke-width="{w}"/><path d="{path}" fill="none" stroke="#f6f0d8" stroke-width="3" stroke-dasharray="22 18"/>'
    # lake below
    b += (f'<path d="M80 1450 Q260 1330 540 1380 Q820 1420 980 1360 Q1040 1520 900 1640 Q640 1740 380 1700 Q120 1660 80 1450Z" fill="#3fb0c0" stroke="#1d6a78" stroke-width="5"/>'
          f'<path d="M180 1480 Q400 1420 620 1470 T940 1440" fill="none" stroke="#bff2f6" stroke-width="5" opacity=".7"/>')
    # park around the tower
    b += f'<circle cx="{cx}" cy="{cy}" r="440" fill="#7fae5a" opacity=".55"/><circle cx="{cx}" cy="{cy}" r="440" fill="none" stroke="#5a8a40" stroke-width="6" opacity=".6"/>'
    for k in range(60):
        a = rnd.uniform(0, 6.28); r = rnd.uniform(380, 430)
        x, y = cx + r * math.cos(a), cy + r * math.sin(a)
        b += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{rnd.randint(9, 14)}" fill="#3f7a32" stroke="#22461c" stroke-width="2"/>'
    # long shadow to the upper right
    b += f'<path d="M{cx - 40} {cy - 40} L{cx + 520} {cy - 520} L{cx + 570} {cy - 480} L{cx + 50} {cy + 40}Z" fill="#3a2414" opacity=".3" filter="url(#blur14)"/>'
    tiers = [(470, 96), (400, 84), (335, 72), (270, 62), (210, 52), (152, 44), (100, 38), (60, 32)]
    cols = ['#3c5a80', '#4d6d94', '#5f80a8', '#7393bb', '#88a8cc', '#a0bede', '#bcd4ec', '#dcebfa']
    wings = (270, 30, 150)   # one wing up, two down-diagonal
    hexr = 70 * sc
    for t, ((Lw, hw), col) in enumerate(zip(tiers, cols)):
        Lw *= sc; hw *= sc
        shapes = []
        for k, a in enumerate(wings):
            Lk = Lw - (k * 18 if t % 3 else 0) - (t % 3) * 8 * k
            shapes.append(f'<g transform="translate({cx} {cy}) rotate({a - 90})"><rect x="{-hw:.1f}" y="0" width="{2 * hw:.1f}" height="{Lk:.1f}" rx="{hw * .9:.0f}"/></g>')
        rr = hexr + (40 - t * 3) * sc
        hexpts = ' '.join(f'{cx + rr * math.cos(math.radians(60 * i)):.1f},{cy + rr * math.sin(math.radians(60 * i)):.1f}' for i in range(6))
        shapes.append(f'<polygon points="{hexpts}"/>')
        b += f'<g fill="none" stroke="{INK}" stroke-width="11">{"".join(shapes)}</g>'
        b += f'<g fill="{col}" stroke="none">{"".join(shapes)}</g>'
        b += f'<g fill="none" stroke="#ffffff" stroke-width="3" opacity=".35" transform="translate(-3 3)">{"".join(shapes)}</g>'
    for a in wings:
        for r in range(120, 380, 28):
            x, y = cx + r * math.cos(math.radians(a)), cy + r * math.sin(math.radians(a))
            b += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="3" fill="#ffffff" opacity=".35"/>'
    # glowing hexagonal core + wings bracing it
    hexpts = ' '.join(f'{cx + hexr * math.cos(math.radians(60 * i)):.1f},{cy + hexr * math.sin(math.radians(60 * i)):.1f}' for i in range(6))
    b += f'<circle cx="{cx}" cy="{cy}" r="180" fill="#ffd27a" opacity=".45" filter="url(#blur30)"/>'
    for a in wings:
        x2, y2 = cx + 360 * math.cos(math.radians(a)), cy + 360 * math.sin(math.radians(a))
        b += f'<path d="M{cx} {cy} L{x2:.0f} {y2:.0f}" stroke="#ffd27a" stroke-width="24" opacity=".45" filter="url(#blur8)"/>'
        b += f'<path d="M{cx} {cy} L{x2:.0f} {y2:.0f}" stroke="#fff1c2" stroke-width="7" stroke-linecap="round"/>'
    b += f'<polygon points="{hexpts}" fill="#f6d488" stroke="#6a4416" stroke-width="6" opacity=".95"/>'
    b += f'<circle cx="{cx}" cy="{cy}" r="14" fill="#ffffff"/>' + spark(cx, cy, 42, '#fffbe8', 1)
    for (x, y, c) in ((80, 1170, '#c0443e'), (180, 1150, '#2f6fa8'), (980, 1215, '#e0a531')):
        b += f'<rect x="{x}" y="{y}" width="26" height="14" rx="4" fill="{c}" stroke="{INK}" stroke-width="2"/>'
    # ---- frog in a hot-air balloon, lower right, peeking at the Y ----
    bxc, byc, s = 175, 330, .6
    d += rad('bal', bxc - 40, byc - 60, 190, [(0, '#ffe7a0', 1), (.5, '#f2a64a', 1), (1, '#b8562a', 1)])
    g = f'<g transform="translate({bxc} {byc}) scale({s}) translate({-bxc} {-byc})">'
    g += f'<path d="M{bxc - 160} {byc} C{bxc - 170} {byc - 220} {bxc + 170} {byc - 220} {bxc + 160} {byc} C{bxc + 150} {byc + 90} {bxc + 50} {byc + 150} {bxc + 40} {byc + 190} L{bxc - 40} {byc + 190} C{bxc - 50} {byc + 150} {bxc - 150} {byc + 90} {bxc - 160} {byc}Z" fill="url(#bal)" stroke="{INK}" stroke-width="6"/>'
    for off in (-90, 0, 90):
        g += f'<path d="M{bxc + off * .2} {byc - 168} C{bxc + off * 1.4} {byc - 120} {bxc + off * 1.3} {byc + 80} {bxc + off * .35} {byc + 188}" fill="none" stroke="#c0443e" stroke-width="16" opacity=".8"/>'
    g += f'<path d="M{bxc - 110} {byc - 110} q30 -50 90 -60" fill="none" stroke="#fff6d8" stroke-width="10" stroke-linecap="round" opacity=".8"/>'
    for sx in (-38, 38):
        g += f'<path d="M{bxc + sx} {byc + 190} L{bxc + sx * 1.6} {byc + 270}" stroke="#5a3a1a" stroke-width="4"/>'
    goggles = ('<path d="M-26 -84 q32 -14 62 0" fill="none" stroke="#5a3a1a" stroke-width="7"/>'
               '<circle cx="-8" cy="-86" r="10" fill="#7fd6e6" stroke-width="3.5"/><circle cx="22" cy="-86" r="10" fill="#7fd6e6" stroke-width="3.5"/>')
    g += frog(bxc + 4, byc + 330, 2.3, look=(6, 6), mouth='o', armL='M-34 -24 q-14 0 -16 14', armR='M38 -24 q26 -4 34 6', top=goggles)
    bt = byc + 268
    g += f'<path d="M{bxc - 82} {bt} H{bxc + 82} L{bxc + 66} {bt + 90} H{bxc - 66}Z" fill="#b07a3c" stroke="{INK}" stroke-width="6"/>'
    for k in range(1, 6):
        g += f'<path d="M{bxc - 82 + k * 27} {bt + 4} L{bxc - 80 + k * 26} {bt + 86}" stroke="#7a4a1c" stroke-width="3"/>'
    g += f'<path d="M{bxc - 86} {bt} H{bxc + 86}" stroke="#7a4a1c" stroke-width="14" stroke-linecap="round"/></g>'
    b += f'<ellipse cx="{bxc + 140}" cy="{byc + 380}" rx="70" ry="16" fill="#3a2414" opacity=".2" filter="url(#blur8)"/>' + g
    for (x, y, s2) in ((cx - 340, 240, 20), (cx + 330, 330, 22), (cx - 330, 820, 16)):
        b += spark(x, y, s2, '#fffbe8', .9)
    b += band(980, 1330, '#2a1a0c', .4)
    return vpage('#dca866', vsvg(d, b), [(146, [('A STABLE', 'w')]), (226, [('TRIPOD', 'y')])], outline='#2a1a0c', top=990)


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
    rnd = random.Random(41); d = FILTERS; HZ = 860
    d += lin('sky', [(0, '#0f4c8a'), (.55, '#4fa3e0'), (1, '#d8f0ff')])
    d += lin('snow', [(0, '#ffffff'), (.5, '#e4f1fb'), (1, '#a9c8e4')])
    b = f'<rect width="1080" height="{HZ + 40}" fill="url(#sky)"/>'
    b += '<circle cx="900" cy="250" r="50" fill="#fffbe8"/><circle cx="900" cy="250" r="160" fill="#fff4c0" opacity=".35" filter="url(#blur30)"/>'
    for (pts, col) in (([(380, 880), (560, 560), (700, 700), (860, 520), (1100, 820)], '#6f95c4'),
                        ([(-20, 880), (160, 600), (330, 740), (480, 880)], '#86a8d4')):
        pp = ' '.join(f'{x},{y}' for x, y in pts)
        b += f'<polygon points="{pp}" fill="{col}"/>'
        for i in range(1, len(pts) - 1):
            x, y = pts[i]
            b += f'<path d="M{x - 60} {y + 70} L{x} {y} L{x + 60} {y + 70} L{x + 30} {y + 55} L{x + 5} {y + 78} L{x - 25} {y + 56}Z" fill="#f4faff"/>'
    for (x, y, s) in ((180, 420, .9), (880, 520, .7)):
        b += cloud(x, y, s)
    b += f'<path d="M0 {HZ - 10} Q300 {HZ + 30} 600 {HZ - 10} T1080 {HZ + 10} V1920 H0Z" fill="url(#snow)"/>'
    b += f'<path d="M0 {HZ - 10} Q300 {HZ + 30} 600 {HZ - 10} T1080 {HZ + 10}" fill="none" stroke="#ffffff" stroke-width="5"/>'
    for k in range(16):
        x = rnd.randint(-100, 900); y = rnd.randint(HZ + 60, 1880)
        b += f'<path d="M{x} {y} q{rnd.randint(60, 140)} -12 {rnd.randint(160, 300)} 4" fill="none" stroke="#9fbde0" stroke-width="3" opacity=".5"/>'
    # ---- the tower, planting two giant ski poles ----
    cx, base, H, W = 540, 880, 760, 300
    b += f'<ellipse cx="{cx}" cy="{base + 10}" rx="440" ry="40" fill="#7fa3cc" opacity=".55" filter="url(#blur8)"/>'
    yatt = base - .28 * H
    d2, b2 = tower(cx, base, H, W, dict(
        faces=[('#4f6f96', '#a8c8ea'), ('#6688b0', '#cfe4f8'), ('#3e5c84', '#86a8d0'), ('#2f4c74', '#6a8cb8')],
        edge='#13233c', rim='#fff4c8', rimside='L', band='#1c3456', line='#18304e', glow='#fff6d0', glowop=.5), 'tw')
    d += d2; b += b2
    b += f'<rect x="{cx - 160}" y="{yatt - 16}" width="320" height="32" fill="#ffd27a" opacity=".7" filter="url(#blur8)"/>'
    b += f'<rect x="{cx - 120}" y="{yatt - 8}" width="240" height="16" rx="6" fill="#ffe7a0" stroke="#6a4416" stroke-width="3"/>'
    b += pole(cx - 70, yatt, cx - 400, base + 24, 16, 44) + pole(cx + 70, yatt, cx + 400, base + 18, 16, 44)
    for (x, y) in ((cx - 400, base + 28), (cx + 400, base + 22)):
        b += f'<ellipse cx="{x}" cy="{y}" rx="70" ry="16" fill="#ffffff" filter="url(#blur4)"/>'
        for k in range(6):
            b += f'<circle cx="{x + rnd.randint(-60, 60)}" cy="{y - rnd.randint(4, 34)}" r="{rnd.randint(4, 8)}" fill="#ffffff" stroke="#9fbde0" stroke-width="2"/>'
    for y in (300, 400, 510):   # wind from the left
        b += f'<path d="M30 {y} q100 -20 200 0 q50 8 74 -10" fill="none" stroke="#ffffff" stroke-width="6" stroke-linecap="round" opacity=".75"/>'
    # ---- frog skier below the text, poles planted wide ----
    fx, fy, fs = 520, 1620, 2.5
    skis = (f'<path d="M-60 8 L100 0 q18 -2 24 -16" fill="none" stroke="{INK}" stroke-width="15" stroke-linecap="round"/>'
            f'<path d="M-60 8 L100 0 q18 -2 24 -16" fill="none" stroke="#2f6fa8" stroke-width="8" stroke-linecap="round"/>'
            f'<path d="M-74 18 L86 12 q18 -2 24 -16" fill="none" stroke="{INK}" stroke-width="15" stroke-linecap="round"/>'
            f'<path d="M-74 18 L86 12 q18 -2 24 -16" fill="none" stroke="#2f6fa8" stroke-width="8" stroke-linecap="round"/>')
    beanie = ('<path d="M-28 -78 q32 -40 66 0z" fill="#c0443e" stroke-width="3"/><rect x="-32" y="-82" width="74" height="12" rx="5" fill="#f4f1ea" stroke-width="2.6"/>'
              '<circle cx="6" cy="-112" r="10" fill="#f4f1ea" stroke-width="2.6"/>')
    scarf = ('<path d="M-30 -30 q36 12 70 -2" fill="none" stroke="#1d2b1c" stroke-width="15" stroke-linecap="round"/>'
             '<path d="M-30 -30 q36 12 70 -2" fill="none" stroke="#e0a531" stroke-width="10" stroke-linecap="round"/>'
             '<path d="M-28 -30 q-30 -4 -54 -22 q-6 10 4 18 q22 12 48 10z" fill="#e0a531" stroke-width="3"/>')
    fpoles = (f'<path d="M-62 -6 L-96 34" stroke="{INK}" stroke-width="9" stroke-linecap="round"/><path d="M-62 -6 L-96 34" stroke="#d64a3e" stroke-width="5" stroke-linecap="round"/>'
              f'<ellipse cx="-92" cy="30" rx="14" ry="5" fill="none" stroke="#f2b632" stroke-width="3.5"/>'
              f'<path d="M66 -6 L104 34" stroke="{INK}" stroke-width="9" stroke-linecap="round"/><path d="M66 -6 L104 34" stroke="#d64a3e" stroke-width="5" stroke-linecap="round"/>'
              f'<ellipse cx="100" cy="30" rx="14" ry="5" fill="none" stroke="#f2b632" stroke-width="3.5"/>')
    b += f'<ellipse cx="{fx + 30}" cy="{fy + 40}" rx="300" ry="26" fill="#9fbde0" opacity=".6" filter="url(#blur8)"/>'
    b += frog(fx, fy, fs, look=(5, -5), mouth='o', rot_=-4, armL='M-34 -22 q-18 0 -28 16', armR='M38 -22 q18 0 28 16',
              feet=((-22, 6, -10), (22, 6, 10)), back=skis, front=scarf, top=beanie + fpoles)
    for k in range(14):
        b += f'<circle cx="{fx - 330 + rnd.randint(0, 110)}" cy="{fy + rnd.randint(-70, 30)}" r="{rnd.randint(5, 12)}" fill="#ffffff" stroke="#b8d0ea" stroke-width="2"/>'
    for (x, y, s) in ((cx - 230, 240, 18), (cx + 260, 380, 22), (880, 1500, 16)):
        b += spark(x, y, s, '#ffffff', .95)
    b += band(940, 1320, '#0a1a33', .35)
    return vpage('#0f4c8a', vsvg(d, b), [(160, [("IT WON'T", 'w')]), (226, [('TUMBLE', 'y')])], outline='#0a1a33', top=950)


# =========================== short5: first test failed (wind tunnel) ===========================
def s5():
    rnd = random.Random(51); d = FILTERS
    d += lin('lab', [(0, '#0b1626'), (.7, '#16304a'), (1, '#0a1420')])
    d += lin('win', [(0, '#bfeaf6'), (.5, '#e8fbff'), (1, '#9fd6e8')])
    b = '<rect width="1080" height="1920" fill="url(#lab)"/>'
    for k in range(6):
        b += f'<rect x="{k * 200 - 20}" y="0" width="190" height="1500" fill="#1b3550" opacity=".35" stroke="#0a1626" stroke-width="4"/>'
    b += '<path d="M0 150 H1080" stroke="#2c4a68" stroke-width="20"/><path d="M0 144 H1080" stroke="#4f7090" stroke-width="4"/>'
    b += '<rect y="1500" width="1080" height="420" fill="#0c1a2a"/><path d="M0 1500 H1080" stroke="#2c4a68" stroke-width="5"/>'
    # ---- test section window ----
    x0, y0, x1, y1 = 70, 250, 1010, 860
    b += f'<rect x="{x0 - 30}" y="{y0 - 30}" width="{x1 - x0 + 60}" height="{y1 - y0 + 60}" rx="30" fill="#4f6478" stroke="{INK}" stroke-width="7"/>'
    b += f'<rect x="{x0 - 30}" y="{y0 - 30}" width="{x1 - x0 + 60}" height="16" rx="8" fill="#9fb4c8"/>'
    for t in range(12):
        bx = x0 - 14 + t * (x1 - x0 + 28) / 11
        b += f'<circle cx="{bx:.0f}" cy="{y0 - 14}" r="5" fill="#c8d6e2" stroke="{INK}" stroke-width="2"/><circle cx="{bx:.0f}" cy="{y1 + 14}" r="5" fill="#c8d6e2" stroke="{INK}" stroke-width="2"/>'
    b += f'<clipPath id="wc"><rect x="{x0}" y="{y0}" width="{x1 - x0}" height="{y1 - y0}" rx="14"/></clipPath>'
    inner = f'<rect x="{x0}" y="{y0}" width="{x1 - x0}" height="{y1 - y0}" fill="url(#win)"/>'
    inner += f'<ellipse cx="{x0 + 330}" cy="{y0 + 300}" rx="380" ry="300" fill="#ffffff" opacity=".6" filter="url(#blur60)"/>'
    for r in range(0, 22):   # honeycomb inlet on the left
        for c in range(2):
            hx, hy = x0 + 16 + c * 26 + (13 if r % 2 else 0), y0 + 14 + r * 28
            inner += f'<polygon points="' + ' '.join(f'{hx + 12 * math.cos(math.radians(60 * i)):.0f},{hy + 12 * math.sin(math.radians(60 * i)):.0f}' for i in range(6)) + '" fill="#d8e8f0" stroke="#6a8aa0" stroke-width="2"/>'
    mcx, mbase = 360, 820
    inner += f'<rect x="{x0}" y="{mbase}" width="{x1 - x0}" height="{y1 - mbase}" fill="#7d93a8"/>'
    inner += f'<ellipse cx="{mcx}" cy="{mbase + 6}" rx="170" ry="24" fill="#c8d6e2" stroke="{INK}" stroke-width="4"/>'
    for k, y in enumerate(range(y0 + 50, mbase - 20, 46)):   # smoke streamlines
        pth = f'M{x0 + 70} {y} C{x0 + 140} {y + 6} {mcx - 170} {y - 4} {mcx - 90} {y + (8 if k % 2 else -8)}'
        inner += f'<path d="{pth}" fill="none" stroke="#ffffff" stroke-width="16" opacity=".45" filter="url(#blur4)"/>'
        inner += f'<path d="{pth}" fill="none" stroke="#5a7fa0" stroke-width="4" opacity=".7" stroke-dasharray="30 12"/>'
    vs = [(520, 420, 70, 1), (640, 650, 85, -1), (770, 400, 95, 1), (890, 660, 100, -1), (1000, 420, 100, 1)]   # vortex shedding
    for (vx, vy, r, cw) in vs:
        sp = spiral(vx, vy, r, 1.7, cw, 0 if cw > 0 else math.pi)
        inner += f'<path d="{sp}" fill="none" stroke="#ffffff" stroke-width="30" opacity=".55" filter="url(#blur8)"/>'
        inner += f'<path d="{sp}" fill="none" stroke="#3f6a90" stroke-width="7" stroke-linecap="round"/>'
        inner += f'<path d="{sp}" fill="none" stroke="#ffffff" stroke-width="3" stroke-linecap="round" opacity=".8"/>'
    inner += f'<path d="M{mcx + 50} 470 C460 430 480 410 520 420 M{mcx + 50} 620 C520 660 580 650 640 650" fill="none" stroke="#3f6a90" stroke-width="6" opacity=".7"/>'
    b += f'<g clip-path="url(#wc)">{inner}'
    d2, b2 = tower(mcx, mbase, 540, 190, dict(
        faces=[('#8a9aa8', '#dfe8ee'), ('#a0b0bc', '#f2f8fb'), ('#76889a', '#c4d2dc'), ('#647688', '#a8b8c6')],
        edge='#1d2b3a', rim='#ffffff', rimside='L', band='#5a6c7e', line='#4a5c6e', glow='#ffffff', glowop=.3), 'md')
    d += d2
    b += f'<g transform="rotate(4 {mcx} {mbase})">{b2}</g>'
    for k in (1, 2):   # sway marks
        b += f'<path d="M{mcx - 50 - k * 26} {mbase - 450 + k * 10} q-14 50 0 100" fill="none" stroke="#c0443e" stroke-width="7" stroke-linecap="round" opacity=".85"/>'
        b += f'<path d="M{mcx + 50 + k * 26} {mbase - 450 + k * 10} q14 50 0 100" fill="none" stroke="#c0443e" stroke-width="7" stroke-linecap="round" opacity=".85"/>'
    b += '</g>'
    b += f'<path d="M{x0 + 600} {y0 + 30} L{x0 + 780} {y0 + 30} L{x0 + 660} {y1 - 30} L{x0 + 560} {y1 - 30}Z" fill="#ffffff" opacity=".10"/>'
    # warning lamp on the frame (pulsing red glow)
    b += f'<circle cx="{x1 - 70}" cy="{y0 - 70}" r="46" fill="#ff5a4a" opacity=".6" filter="url(#blur14)"/><rect x="{x1 - 92}" y="{y0 - 94}" width="44" height="40" rx="10" fill="#ff7a6a" stroke="{INK}" stroke-width="4"/>'
    b += f'<rect x="{x0}" y="{y1 + 30}" width="{x1 - x0}" height="60" fill="#ff5a4a" opacity=".12" filter="url(#blur30)"/>'
    # ---- control desk + frog scientist below the text ----
    b += '<path d="M560 1500 L1040 1500 L1000 1700 L600 1700Z" fill="#26405c" stroke="#081220" stroke-width="5"/><path d="M560 1500 H1040" stroke="#5a7fa0" stroke-width="5"/>'
    for (gx, col) in ((680, '#7fd6e6'), (800, '#ff7a6a'), (920, '#ffd27a')):   # gauges
        b += f'<circle cx="{gx}" cy="1580" r="40" fill="#0b1626" stroke="#9fb4c8" stroke-width="5"/><path d="M{gx} 1580 l26 -22" stroke="{col}" stroke-width="6" stroke-linecap="round"/>'
        b += f'<circle cx="{gx}" cy="1580" r="40" fill="{col}" opacity=".18" filter="url(#blur8)"/>'
    coat = ('<path d="M-33 -34 q-4 30 -2 38 q36 10 76 0 q2 -10 -2 -38 q-36 12 -72 0z" fill="#f4f6fa" stroke-width="3.2"/>'
            '<path d="M2 -32 l-12 24 M10 -32 l12 24" stroke="#9aa8b8" stroke-width="3"/><rect x="24" y="-18" width="12" height="10" fill="#7fd6e6" stroke-width="2"/>')
    gog = ('<path d="M-26 -84 q32 -14 62 0" fill="none" stroke="#3a3a3a" stroke-width="7"/>'
           '<circle cx="-8" cy="-86" r="11" fill="#ffd27a" fill-opacity=".7" stroke-width="3.5"/><circle cx="22" cy="-86" r="11" fill="#ffd27a" fill-opacity=".7" stroke-width="3.5"/>')
    clip = ('<rect x="-92" y="-40" width="44" height="58" rx="5" fill="#b07a3c" stroke-width="3"/><rect x="-86" y="-30" width="32" height="42" fill="#ffffff" stroke-width="2"/>'
            '<path d="M-82 -20 h22 M-82 0 h22 M-82 10 h16" stroke="#9aa8b8" stroke-width="2.5"/>')
    b += f'<ellipse cx="320" cy="1660" rx="200" ry="24" fill="#000000" opacity=".4" filter="url(#blur8)"/>'
    b += frog(320, 1650, 2.6, look=(5, -6), mouth='o', armL='M-34 -22 q-20 4 -24 18', armR='M38 -24 q24 -14 34 -40', front=coat, back=clip, top=gog)
    for (x, y, s) in ((540, 200, 16), (160, 1420, 14), (980, 1420, 14)):
        b += spark(x, y, s, '#e8fbff', .9)
    b += band(940, 1310, '#02060c', .45)
    return vpage('#0b1626', vsvg(d, b), [(140, [('FIRST TEST:', 'w')]), (226, [('FAILED', 'y')])], outline='#050b18', top=950)


if __name__ == '__main__':
    for n, f in ((1, s1), (2, s2), (3, s3), (4, s4), (5, s5)):
        out = os.path.join(VID, f'hollow-skyscraper-short{n}', 'thumb'); os.makedirs(out, exist_ok=True)
        for fn in ('common.css', 'Fredoka-700.woff2'):   # vertical common.css (1080x1920) from tools/assets/thumb_v
            shutil.copy(os.path.join(TOOLS, 'assets', 'thumb_v', fn), out)
        open(os.path.join(out, 'A.html'), 'w').write(f())
    print('ok')
