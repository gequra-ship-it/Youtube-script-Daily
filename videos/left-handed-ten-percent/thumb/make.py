import sys, math, random
sys.path.insert(0, '/home/user/rp/tools')
from thumb_lib import *
from hands import hand
random.seed(3)

# ---- A: 3 of 4 cave hands are left (Ice Age hand stencils) ----
WALL = '#7a4424'; PIG = '#b8402a'
def stencil(x, y, size, side, angle):
    halo = hand(x, y, angle, size, side, 'palm', 'open', PIG, PIG, lw=size * .34, creases=False)
    core = hand(x, y, angle, size, side, 'palm', 'open', WALL, WALL, lw=2, creases=False)
    return f'<g filter="url(#sp)" opacity=".92">{halo}</g>{core}'
d = rad('wl', 1350, 600, 1000, [(0, '#c0773f', 1), (.5, '#7a4424', 1), (1, '#2a140d', 1)]) + '<filter id="sp" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="9"/></filter>'
b = '<rect width="1920" height="1080" fill="url(#wl)"/>' + blobs(220, 0, 0, 1920, 1080, '#1a0a05', .03, .08, 14, 60) + blobs(160, 0, 0, 1920, 1080, '#e0a070', .03, .07, 8, 36)
b += ''.join(f'<path d="M{x} {y} q{random.randint(-60, 60)} {random.randint(40, 120)} {random.randint(-40, 40)} {random.randint(140, 260)}" stroke="#1a0a05" stroke-width="3" fill="none" opacity=".35"/>' for x, y in [(random.randint(0, 1900), random.randint(0, 600)) for _ in range(9)])
b += stencil(1420, 880, 205, 'L', 0) + stencil(1010, 905, 125, 'L', -14) + stencil(1780, 640, 120, 'L', 14) + stencil(1130, 560, 115, 'R', 8)
b += spark(1500, 330, 20)
open('A.html', 'w', encoding='utf-8').write(page('#2a140d', svg(d, b), [('3 OF 4', 250, 'y'), ('CAVE HANDS', 150, 'w'), ('ARE LEFT', 150, 'w')], '#1c0b05'))

# ---- B: Leonardo wrote backwards (Vitruvian-style diagram + right-to-left script) ----
d = lin('bg', [(0, '#0b1d33'), (1, '#173a58')]) + rad('gl', 1380, 520, 600, [(0, '#F2D27A', .45), (1, '#F2D27A', 0)]) + lin('pp', [(0, '#f0dcae'), (1, '#d9bf86')], 1, 1)
b = '<rect width="1920" height="1080" fill="url(#bg)"/>' + stars(60, 500) + '<rect width="1920" height="1080" fill="url(#gl)"/>'
b += '<g transform="translate(1420 590) scale(.82) rotate(-3) translate(-1380 -560)"><rect x="940" y="150" width="880" height="800" rx="22" fill="url(#pp)" stroke="#6b4a26" stroke-width="6"/>'
cx, cy = 1380, 430
b += f'<g fill="none" stroke="#4a3418" stroke-width="5"><circle cx="{cx}" cy="{cy}" r="190"/><rect x="{cx - 160}" y="{cy - 160}" width="320" height="320"/>'
b += f'<circle cx="{cx}" cy="{cy - 105}" r="26"/><path d="M{cx} {cy - 78} L{cx} {cy + 55} M{cx - 125} {cy - 20} L{cx + 125} {cy - 20} M{cx - 105} {cy - 70} L{cx + 105} {cy - 10} M{cx} {cy + 55} L{cx - 70} {cy + 160} M{cx} {cy + 55} L{cx + 70} {cy + 160}"/></g>'
for k in range(5):
    y = 700 + k * 48; w = random.randint(560, 740)
    pts = ''.join(f'q{-14} {random.choice([-14, 14])} {-28} 0 ' for _ in range(w // 28))
    b += f'<path d="M1780 {y} {pts}" stroke="#4a3418" stroke-width="5" fill="none" stroke-linecap="round" opacity=".8"/>'
b += '</g>'
b += '<path d="M1700 672 L1100 672" stroke="#F2D27A" stroke-width="12" stroke-linecap="round"/><path d="M1140 636 L1090 672 L1140 708" stroke="#F2D27A" stroke-width="12" fill="none" stroke-linecap="round" stroke-linejoin="round"/>'
open('B.html', 'w', encoding='utf-8').write(page('#0b1d33', svg(d, b), [('LEONARDO', 150, 'w'), ('WROTE', 150, 'w'), ('BACKWARDS', 150, 'y')], '#050d1a'))

# ---- C: 1 in 10 is left-handed (odd one out in a crowd) ----
d = lin('bg', [(0, '#2a1450'), (.6, '#6a2a6a'), (1, '#c4578a')]) + rad('sp', 1700, 700, 380, [(0, '#F2D27A', .8), (.5, '#F2D27A', .22), (1, '#F2D27A', 0)])
b = '<rect width="1920" height="1080" fill="url(#bg)"/>' + stars(50, 420, 0, '#ffe8f4')
def bust(x, y, s, col, hi=False):
    o = f'<g transform="translate({x} {y}) scale({s})">'
    o += f'<path d="M-62 0 C-62 -78 62 -78 62 0 L62 70 L-62 70Z" fill="{col}"/><circle cx="0" cy="-92" r="46" fill="{col}"/>'
    if hi: o += '<circle cx="-16" cy="-98" r="6" fill="#2a1450"/><circle cx="16" cy="-98" r="6" fill="#2a1450"/><path d="M-14 -78 q14 12 28 0" stroke="#2a1450" stroke-width="5" fill="none" stroke-linecap="round"/>'
    return o + '</g>'
k = 0
for r in range(2):
    for c in range(5):
        k += 1; x = 900 + c * 190 + (r * 95); y = 580 + r * 262
        if k == 10: b += f'<circle cx="{x}" cy="{y - 70}" r="260" fill="url(#sp)"/>' + bust(x, y, 1.45, '#ffe7b0', True) + '<g transform="translate(%d %d) rotate(25)"><rect x="-8" y="-70" width="16" height="120" rx="4" fill="#e8584a"/><path d="M-8 -70 L0 -100 L8 -70Z" fill="#f2d27a"/></g>' % (x - 90, y + 20) + spark(x + 120, y - 190, 20)
        else: b += bust(x, y, 1.3, '#3a2a78')
open('C.html', 'w', encoding='utf-8').write(page('#2a1450', svg(d, b), [('1 IN 10', 290, 'y'), ('IS LEFT-HANDED', 112, 'w')], '#14082a'))
