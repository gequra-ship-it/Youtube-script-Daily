# Thumbnails A-C for sacabambaspis-meme (guideline 16-6, brief tools/briefs/thumb_art.md). Run: python3 videos/sacabambaspis-meme/thumb/make.py
# A  ONE ARTIST'S GUESS   homage: The Scream (Munch 1893, public domain): swirling sunset sky, bridge railing, the frog in the hands-on-cheeks pose,
#                         the shocked stylised fish as the screaming figure. Text from S16/S25 "The meme face is one artist's guess" / "The face is a guess by an artist".
# B  DOZENS IN ONE ROCK   intuitive: a Bolivian rock slab packed with articulated fossil fish, frog paleontologist with a brush and lantern.
#                         S01 "one disaster may have frozen dozens of these fish in stone", S17 "about thirty specimens were packed into a very small space".
# C  IT COULDN'T BITE BACK  intuitive: armoured jawless fish (small round mouth, no paired fins) with a big sea scorpion's spiny claws reaching for it.
#                         S15 "A fish that could not bite back could still make itself hard to bite"; S12 sea scorpions = hedged "one idea" (picture only, no text claim).
import os, sys, math, random
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, '../../../tools'))
from thumb_lib import page, svg, lin, rad, spark
from saca_lib import *


def wave_path(x0, x1, y, amp, wl, ph, step=20):
    pts = [(x, y + amp * math.sin((x / wl) * 2 * math.pi + ph)) for x in range(x0, x1 + step, step)]
    return 'M' + ' L'.join(f'{a:.0f},{b:.0f}' for a, b in pts)


# ======================= A: The Scream =======================
def thumb_A():
    random.seed(3)
    W, H = 1920, 1080
    rail = lambda x: 610 + 330 * x / W          # railing top line (upper-left -> lower-right, as in the painting)
    defs = FILTERS
    defs += rad('sun', 1290, 300, 760, [(0, '#fff6c8', .95), (.25, '#ffd27a', .55), (1, '#ff8a3a', 0)])
    defs += rad('vigA', 960, 540, 1250, [(0, '#000', 0), (.6, '#000', 0), (1, '#1a0500', .55)])
    defs += lin('walk', [(0, '#b8642e'), (1, '#6a3418')])
    b = '<rect width="1920" height="1080" fill="#c8482a"/>'
    # swirling sky bands
    cols = ['#e8762c', '#c8382a', '#f2a03d', '#d9472f', '#f6c35a', '#e05a2a', '#b8302a', '#f08a34']
    for i in range(22):
        y = -10 + i * 30
        b += f'<path d="{wave_path(-40, 1960, y, 22 + i % 3 * 6, 520 + i * 13, i * .9)}" fill="none" stroke="{cols[i % len(cols)]}" stroke-width="44" stroke-linecap="round" opacity=".95"/>'
    for i in range(46):
        y = random.randint(0, 620)
        x0 = random.randint(-100, 1700)
        b += f'<path d="{wave_path(x0, x0 + random.randint(200, 600), y, 14, 380, random.random() * 6)}" fill="none" stroke="{random.choice(["#ffd27a", "#9a2a22", "#f6b04a", "#e86a30"])}" stroke-width="{random.choice([5, 8, 12])}" opacity=".55" stroke-linecap="round"/>'
    b += '<rect width="1920" height="1080" fill="url(#sun)"/>'
    # fjord + hills (above the railing)
    b += '<path d="M640,560 C760,520 900,540 1040,520 C1220,494 1420,520 1600,500 C1760,484 1860,500 1960,490 L1960,980 L640,980Z" fill="#20407a"/>'
    for i in range(14):
        y = 520 + i * 22
        b += f'<path d="{wave_path(620 + i * 10, 1960, y, 10 + i % 3 * 4, 300 + i * 20, i * 1.3)}" fill="none" stroke="{["#2d5aa0", "#16305e", "#3a6ab0", "#1e3c78", "#4a5f9a"][i % 5]}" stroke-width="16" opacity=".9" stroke-linecap="round"/>'
    b += '<path d="M640,560 C760,520 900,540 1040,520 C1220,494 1420,520 1600,500" fill="none" stroke="#ffcf7a" stroke-width="6" opacity=".6"/>'
    # far shore (dark green swirl) on the left, a headland on the right
    b += '<path d="M-40,470 C120,430 300,450 470,500 C600,540 700,600 760,700 C700,740 400,760 -40,760Z" fill="#2c4a34"/>'
    for i in range(10):
        b += f'<path d="M{-40 + i * 6},{480 + i * 26} C{200},{450 + i * 30} {480},{500 + i * 28} {740 - i * 12},{640 + i * 22}" fill="none" stroke="{["#3f6a40", "#1e3424", "#5a7a3a", "#2a4a52"][i % 4]}" stroke-width="14" opacity=".85" stroke-linecap="round"/>'
    b += '<path d="M1560,520 C1680,480 1800,470 1960,480 L1960,560 C1840,560 1700,560 1560,520Z" fill="#2a3a5a"/>'
    b += '<path d="M1500,545 l20,-6 l14,6 z M1530,538 l0,-18" stroke="#1a2440" stroke-width="3" fill="#1a2440"/>'
    # walkway (below the railing)
    b += f'<path d="M0,{rail(0):.0f} L1920,{rail(1920):.0f} L1920,1080 L0,1080Z" fill="url(#walk)"/>'
    for k in range(-6, 30):   # planks converging to the upper-left
        b += f'<path d="M-260,520 L{k * 90},{1120}" stroke="#4a2410" stroke-width="3" opacity=".35"/>'
    for i in range(18):
        y = 700 + i * 24
        b += f'<path d="{wave_path(-20, 1940, y, 8, 700, i)}" fill="none" stroke="{["#d07a3a", "#8a4422", "#e09048"][i % 3]}" stroke-width="10" opacity=".4"/>'
    # railing
    for x in range(-40, 1960, 120):
        b += f'<path d="M{x},{rail(x) + 4:.0f} L{x - 6},{rail(x) + 70 + x * .04:.0f}" stroke="#3a1a0e" stroke-width="10"/>'
    b += f'<path d="M-20,{rail(-20) + 46:.0f} L1940,{rail(1940) + 62:.0f}" stroke="#3a1a0e" stroke-width="9"/>'
    b += f'<path d="M-20,{rail(-20):.0f} L1940,{rail(1940):.0f}" stroke="#2a1008" stroke-width="22" stroke-linecap="round"/>'
    b += f'<path d="M-20,{rail(-20) - 5:.0f} L1940,{rail(1940) - 5:.0f}" stroke="#e8904a" stroke-width="6" opacity=".8"/>'
    # two tiny far walkers -> skipped (text area); swirl light streaks
    # glow + the shocked fish as the screaming figure
    b += '<ellipse cx="1290" cy="330" rx="430" ry="360" fill="#fff0b0" opacity=".45" filter="url(#b50)"/>'
    b += saca_front(1290, 380, 1.02, mouth='O', look=(0, 4), sway=55, length=420)
    for sx, sy, ss in ((1010, 230, 26), (1580, 170, 30), (1610, 470, 20), (990, 520, 18), (1470, 90, 16), (1700, 330, 18)):
        b += spark(sx, sy, ss, col='#fff8dc')
    # the frog: hands on its cheeks (the painting's pose), Munch-style hat + coat
    torso = '<path d="M-35 -4 q-2 -22 4 -28 q36 -8 72 0 q6 8 4 28 q-40 10 -80 0z" fill="#2b2a3a" stroke-width="3.4"/><path d="M-30 -30 q36 8 70 0" fill="none" stroke="#7a3a3a" stroke-width="6"/>'
    hat = '<g transform="translate(0 12)"><path d="M-20 -100 l4 -34 q22 -7 42 0 l4 34z" fill="#1e1c26" stroke-width="3.4"/><path d="M-38 -97 q44 -13 88 0 q-44 9 -88 0z" fill="#2a2834" stroke-width="3.4"/><path d="M-17 -106 q22 -6 42 0" stroke="#7a3a3a" stroke-width="6" fill="none"/></g>'
    arms = ('q-16 -6 4 -28', 'q16 -6 -6 -28')
    b += '<ellipse cx="330" cy="1046" rx="190" ry="26" fill="#2a1008" opacity=".45" filter="url(#b12)"/>'
    b += frog(330, 1040, 2.55, mouth='O', arms=arms, look=(5, -2), torso=torso, head=hat)
    b += '<rect width="1920" height="1080" fill="url(#vigA)"/>'
    lines = [("ONE ARTIST'S", 124, 'w'), ('GUESS', 264, 'y')]
    return page('#c8482a', svg(defs, b), lines, outline='#1a0805', left=70, top=46)


# ======================= B: fossil slab =======================
def thumb_B():
    random.seed(21)
    defs = FILTERS
    defs += lin('skyB', [(0, '#1a1438'), (.45, '#4a2a5a'), (.75, '#c0604a'), (1, '#f0a060')])
    defs += lin('slab', [(0, '#c8875a'), (1, '#7a4a30')], x2=.3, y2=1)
    defs += lin('slabEdge', [(0, '#6a3a24'), (1, '#3a1e12')])
    defs += rad('lamp', 740, 880, 760, [(0, '#ffe2a0', .75), (.35, '#ffb860', .3), (1, '#ff9a40', 0)])
    defs += rad('vigB', 960, 540, 1200, [(0, '#000', 0), (.6, '#000', 0), (1, '#000', .6)])
    b = '<rect width="1920" height="1080" fill="url(#skyB)"/>'
    b += ''.join(f'<circle cx="{random.randint(0, 1920)}" cy="{random.randint(0, 380)}" r="{random.choice([1.2, 1.8, 2.4])}" fill="#fff4e0" opacity="{random.uniform(.3, .9):.2f}"/>' for _ in range(120))
    # Andes, three layers
    b += '<path d="M0,640 L140,520 L250,580 L400,430 L520,540 L660,470 L800,560 L960,400 L1100,520 L1250,440 L1400,540 L1560,420 L1720,520 L1920,450 L1920,760 L0,760Z" fill="#5a3a6a"/>'
    b += '<path d="M960,400 l-40,40 l30 -6 l20 26 l24 -30 l26 14z M1560,420 l-36,40 l26 -4 l16 22 l20 -26 l24 10z M400,430 l-30,34 l22 -4 l14 18 l18 -24z" fill="#e8d8f0" opacity=".75"/>'
    b += '<path d="M0,700 L180,600 L330,660 L520,560 L700,650 L880,580 L1080,660 L1300,570 L1500,650 L1700,590 L1920,650 L1920,800 L0,800Z" fill="#3e2850"/>'
    b += '<path d="M0,760 L260,700 L520,740 L800,690 L1100,740 L1400,700 L1920,740 L1920,1080 L0,1080Z" fill="#2a1a2e"/>'
    # rock slab (tilted, receding)
    slab = 'M820,560 L1880,470 C1900,700 1910,900 1940,1100 L700,1100 C740,900 790,720 820,560Z'
    b += '<path d="M700,1100 C740,900 790,720 820,560 L800,600 C760,760 700,940 650,1100Z" fill="url(#slabEdge)"/>'
    b += f'<path d="{slab}" fill="url(#slab)" stroke="#3a1e12" stroke-width="6"/>'
    defs += f'<clipPath id="slabc"><path d="{slab}"/></clipPath>'
    rock = '<g clip-path="url(#slabc)">'
    for i in range(16):   # bedding lines + cracks
        y = 520 + i * 40
        rock += f'<path d="{wave_path(700, 1940, y, 6, 500, i)}" fill="none" stroke="#5a3220" stroke-width="2.5" opacity=".35"/>'
    rock += ''.join(f'<circle cx="{random.randint(700, 1920)}" cy="{random.randint(470, 1080)}" r="{random.choice([2, 3, 4])}" fill="{random.choice(["#e8b88a", "#5a3220"])}" opacity=".4"/>' for _ in range(260))
    rock += '<path d="M1300,520 l30,90 l-20,60 l40,110 M1650,600 l-40,70 l30,50" stroke="#3a1e12" stroke-width="4" fill="none" opacity=".6"/>'
    # packed articulated fossils
    fos = [(1020, 690, .62, -14, False), (1290, 640, .58, 8, True), (1530, 640, .55, -6, False), (980, 860, .66, 6, False), (1250, 800, .6, -22, True),
           (1500, 820, .56, 6, False), (1180, 960, .64, -4, True), (870, 1010, .55, -18, False), (1460, 990, .5, 20, True), (1720, 720, .5, -30, True),
           (1700, 540, .42, 4, False), (1100, 560, .46, 10, True)]
    for fx, fy, fs, fr, ff in fos:
        rock += f'<g opacity=".95">' + saca(fx, fy, fs, flip=ff, rot=fr, pal='fossil', mouth=None, eyes=False, rim=True, shadow=False, detail=.6) + '</g>'
    rock += '<rect x="600" y="400" width="1400" height="700" fill="url(#lamp)"/>'
    rock += '<path d="M1640,880 L1960,860 L1960,1100 L1600,1100Z" fill="#6a3c26" opacity=".25"/>'
    rock += '</g>'
    b += rock
    b += '<path d="M820,560 L1880,470" stroke="#f2c48a" stroke-width="5" opacity=".8"/>'
    # tools on the slab: hammer + brush
    b += '<g transform="translate(1120 1060) rotate(-8)"><rect x="-6" y="-10" width="150" height="16" rx="6" fill="#8a5a2e" stroke="#2a160c" stroke-width="4"/><rect x="128" y="-36" width="26" height="66" rx="5" fill="#9aa4ae" stroke="#2a160c" stroke-width="4"/></g>'
    # lantern near the frog
    b += '<ellipse cx="740" cy="880" rx="300" ry="230" fill="#ffd27a" opacity=".3" filter="url(#b50)"/>'
    b += '<g transform="translate(1000 1050) rotate(-35)"><rect x="-5" y="-40" width="10" height="56" rx="4" fill="#8a5a2e" stroke="#2a160c" stroke-width="3.5"/><path d="M-9 -40 l-4 -26 h26 l-4 26z" fill="#f2d27a" stroke="#2a160c" stroke-width="3.5"/></g>'
    # frog paleontologist: pith helmet, brush in the right paw
    helmet = '<path d="M-30 -86 q36 -50 72 0z" fill="#e8d6a0" stroke-width="3.4"/><path d="M-46 -84 q52 -16 104 0 q-52 12 -104 0z" fill="#d8c088" stroke-width="3.4"/><path d="M-28 -90 q34 -8 68 0" stroke="#8a6a3a" stroke-width="4" fill="none"/>'
    torso = '<path d="M-22 -50 q2 26 -4 48 M28 -50 q-2 26 4 48" stroke="#8a6a3a" stroke-width="6" fill="none"/><rect x="14" y="-34" width="14" height="11" rx="2" fill="#b89a5a" stroke-width="2.4"/>'
    brush = ('<g transform="translate(70 -74)" stroke-width="2.6"><path d="M-8,0 q8 -10 16 0" fill="none"/><rect x="-11" y="2" width="22" height="5" rx="2" fill="#5a4a3a"/>'
             '<rect x="-9" y="7" width="18" height="24" rx="5" fill="#fff0b8"/><rect x="-12" y="30" width="24" height="5" rx="2" fill="#5a4a3a"/></g>')
    b += '<ellipse cx="560" cy="1046" rx="160" ry="22" fill="#000" opacity=".4" filter="url(#b12)"/>'
    b += frog(560, 1040, 2.5, mouth='o', arms=('q-14 6 -16 22', 'q24 -12 32 -52'), look=(5, -3), torso=torso, head=helmet, front=brush)
    for sx, sy, ss in ((1180, 520, 22), (1640, 460, 18), (900, 660, 16), (1400, 720, 14)):
        b += spark(sx, sy, ss, col='#fff4d0')
    b += '<rect width="1920" height="1080" fill="url(#vigB)"/>'
    lines = [('DOZENS', 230, 'y'), ('IN ONE ROCK', 132, 'w')]
    return page('#1a1438', svg(defs, b), lines, outline='#0c0614', left=70, top=50)


# ======================= C: claws vs armour =======================
def thumb_C():
    random.seed(5)
    defs = FILTERS
    defs += lin('seaC', [(0, '#2a9aa0'), (.4, '#0f5a6e'), (1, '#062236')])
    defs += rad('lightC', 1120, -80, 1100, [(0, '#e8fff6', .7), (.4, '#8ff0e0', .2), (1, '#8ff0e0', 0)])
    defs += lin('floorC', [(0, '#3a5a50'), (1, '#0e2028')])
    defs += rad('vigC', 960, 540, 1200, [(0, '#000', 0), (.6, '#000', 0), (1, '#00060c', .7)])
    b = '<rect width="1920" height="1080" fill="url(#seaC)"/><rect width="1920" height="1080" fill="url(#lightC)"/>'
    for x0, x1 in ((700, 860), (980, 1080), (1220, 1380), (1500, 1580), (400, 480)):
        b += f'<path d="M{x0 + 200},-10 L{x0 - 120},1080 L{x1 - 120},1080 L{x1 + 200},-10Z" fill="#c8fff0" opacity=".07"/>'
    b += '<path d="M0,0 L1920,0 L1920,40 C1600,60 1300,30 960,50 C600,70 300,40 0,60Z" fill="#bff6ee" opacity=".18"/>'
    # far reef silhouettes
    b += '<path d="M0,900 C200,860 380,880 520,850 C700,820 900,870 1100,840 C1300,810 1600,860 1920,830 L1920,1080 L0,1080Z" fill="#0c3a48" opacity=".8"/>'
    b += crinoid(1180, 890, 220, .9, col='#7aa0a8', dark='#1e4a56', lean=-16)
    b += crinoid(1700, 880, 260, 1.0, col='#7aa0a8', dark='#1e4a56', lean=14)
    # sea floor
    b += '<path d="M0,960 C300,930 600,950 900,935 C1200,920 1500,950 1920,930 L1920,1080 L0,1080Z" fill="url(#floorC)"/>'
    b += motes(160, 0, 0, 1920, 1080, '#dff6ee', .5, 2.4)
    # the sea scorpion from the upper right, claws reaching down-left
    b += '<ellipse cx="1600" cy="160" rx="560" ry="300" fill="#04141e" opacity=".35" filter="url(#b50)"/>'
    b += eurypterid(1430, 330, 1.0, rot=-42, claw_open=1.0)
    # fish: big, glowing, swimming left/down away from the claws, eyes looking back
    b += '<ellipse cx="1180" cy="700" rx="430" ry="200" fill="#fff3a8" opacity=".3" filter="url(#b50)"/>'
    b += saca(830, 720, 1.12, flip=False, rot=4, pal='glow', mouth='O', look=(3, -4), bend=-26, glow='#fff3a8')
    # motion swirls behind the tail
    b += ''.join(f'<path d="M{1640 + k * 30},{700 + k * 26} q30 -20 60 0" fill="none" stroke="#dff6ff" stroke-width="4" opacity=".5"/>' for k in range(3))
    for sx, sy, ss in ((960, 560, 22), (1260, 590, 18), (1450, 820, 16), (1060, 880, 14)):
        b += spark(sx, sy, ss, col='#fffbe0')
    # sea floor bits (left)
    for x, y, s, r in ((620, 990, 1.1, -10), (700, 1010, .9, 12), (180, 1000, 1, 6), (560, 1030, .8, -4), (1300, 1000, 1, 8)):
        b += brachiopod(x, y, s, rot=r)
    b += crinoid(600, 1000, 300, 1.15, col='#d87a9a', dark='#4a1a2a', lean=18)
    # frog diver peeking from behind a sponge
    b += '<path d="M60,1080 C40,960 80,860 150,840 C230,830 260,900 250,1080Z" fill="#c89a4a" stroke="#3a2412" stroke-width="5"/>'
    b += ''.join(f'<ellipse cx="{random.randint(80, 230)}" cy="{random.randint(880, 1060)}" rx="7" ry="9" fill="#6a4a22" opacity=".7"/>' for _ in range(18))
    b += frog(330, 1050, 2.45, mouth='O', arms=('q-30 -6 -48 -30', 'q14 6 16 22'), look=(5, -4), back=air_tank(), front=diving_helmet())
    b += bubbles(345, 830, 6, s=1.0)
    b += '<rect width="1920" height="1080" fill="url(#vigC)"/>'
    lines = [("IT COULDN'T", 140, 'w'), ('BITE', 270, 'y'), ('BACK', 140, 'w')]
    return page('#062236', svg(defs, b), lines, outline='#03121c', left=70, top=36)


if __name__ == '__main__':
    import shutil
    for f in ('common.css', 'Fredoka-700.woff2'):
        if not os.path.exists(f'{HERE}/{f}'):
            shutil.copy(os.path.join(HERE, '../../../videos/whale-fall/thumb', f) if f == 'common.css' else os.path.join(HERE, '../../../tools/assets', f), f'{HERE}/{f}')
    for n, fn in (('A', thumb_A), ('B', thumb_B), ('C', thumb_C)):
        open(f'{HERE}/{n}.html', 'w').write(fn())
        print(n, 'ok')
