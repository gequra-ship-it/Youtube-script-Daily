import sys, math, random
sys.path.insert(0, '/home/user/rp/tools')
from thumb_lib import *
random.seed(9)

# ---- A: the Sahara was green (Saharan rock art: giraffe, elephant, hippo) ----
d = rad('wl', 1400, 600, 1000, [(0, '#d99a58', 1), (.55, '#9a5a30', 1), (1, '#3a1d10', 1)]) + lin('gr', [(0, '#5aa84a'), (1, '#2f7a3a')])
b = '<rect width="1920" height="1080" fill="url(#wl)"/>' + blobs(200, 0, 0, 1920, 1080, '#2a1208', .03, .09, 14, 70) + blobs(120, 0, 0, 1920, 1080, '#f0c088', .03, .07, 8, 40)
P = '#f3e3c0'; R = '#c7502e'
b += f'<g fill="{P}" stroke="{R}" stroke-width="5" stroke-linejoin="round" stroke-linecap="round">'
# giraffe
b += '<ellipse cx="1500" cy="700" rx="130" ry="70"/><path d="M1590 660 L1650 420 L1690 430 L1640 680Z"/><ellipse cx="1690" cy="415" rx="45" ry="24" transform="rotate(-18 1690 415)"/>'
b += ''.join(f'<rect x="{x}" y="750" width="22" height="150" rx="8"/>' for x in (1405, 1445, 1540, 1580)) + '<path d="M1380 690 Q1340 730 1350 780" fill="none"/>'
# elephant
b += '<ellipse cx="1130" cy="760" rx="170" ry="115"/><circle cx="1000" cy="700" r="75"/><path d="M945 720 Q900 800 935 880 Q955 900 968 870 Q955 800 985 745Z"/><ellipse cx="1040" cy="725" rx="42" ry="62"/>'
b += ''.join(f'<rect x="{x}" y="830" width="52" height="105" rx="20"/>' for x in (1040, 1130, 1210, 1260))
# hippo
b += '<ellipse cx="1790" cy="840" rx="130" ry="70"/><ellipse cx="1700" cy="800" rx="62" ry="48"/>' + ''.join(f'<rect x="{x}" y="880" width="38" height="60" rx="14"/>' for x in (1710, 1760, 1830, 1870))
b += '</g><g fill="#2f7a3a" opacity=".92">' + ''.join(f'<path d="M{x} 960 q{random.randint(-10, 10)} -{random.randint(40, 90)} {random.randint(-4, 14)} -{random.randint(60, 120)} q-4 50 -{random.randint(0, 10)} {random.randint(60, 120)}Z"/>' for x in range(-20, 1960, 22)) + '</g>'
b += '<rect x="0" y="955" width="1920" height="125" fill="url(#gr)"/>' + spark(900, 330, 22) + spark(1850, 330, 18)
open('A.html', 'w', encoding='utf-8').write(page('#3a1d10', svg(d, b), [('THE SAHARA', 135, 'w'), ('WAS', 135, 'w'), ('GREEN', 250, 'y')], '#1f0e06'))

# ---- B: a tunnel that makes an oasis (qanat cross-section) ----
d = lin('sk', [(0, '#3a1850'), (.5, '#d8663a'), (1, '#f7c27a')]) + lin('er', [(0, '#a8683a'), (1, '#3a1d10')]) + rad('wg', 1700, 720, 340, [(0, '#7ff0e0', .55), (1, '#7ff0e0', 0)])
b = '<rect width="1920" height="560" fill="url(#sk)"/>' + stars(30, 380, 0, '#ffe8d0', .5, 3)
b += '<path d="M0 560 L900 470 L1920 720 L1920 1080 L0 1080Z" fill="url(#er)"/>'
b += '<path d="M900 470 Q1000 450 1100 490 L1920 700 L1920 720 Z" fill="#e4a860" opacity=".0"/>'
b += '<path d="M0 560 L900 470 L1920 720" fill="none" stroke="#f0c07a" stroke-width="8"/>' + blobs(40, 900, 560, 1900, 1050, '#2a1208', .15, .35, 40, 150)
b += '<path d="M930 770 L1900 748" stroke="#0e1d2b" stroke-width="64" stroke-linecap="round"/><path d="M930 770 L1900 748" stroke="#7ff0e0" stroke-width="14" stroke-linecap="round" opacity=".95"/>'
for x in (1040, 1260, 1480, 1700):
    ys = 470 + (x - 900) * (250 / 1020) - 4; yt = 770 - (x - 930) * (22 / 970)
    b += f'<path d="M{x} {ys} L{x} {yt}" stroke="#0e1d2b" stroke-width="30"/><path d="M{x - 38} {ys + 4} Q{x} {ys - 46} {x + 38} {ys + 4}Z" fill="#c68a4c" stroke="#6b3f1c" stroke-width="4"/>'
b += '<ellipse cx="1760" cy="745" rx="170" ry="28" fill="#7ff0e0" opacity=".55"/><rect width="1920" height="1080" fill="url(#wg)"/>'
for x, h in ((1700, 150), (1790, 190), (1860, 140)):
    b += f'<path d="M{x} 745 Q{x + 6} {745 - h * .6} {x} {745 - h}" stroke="#5a3a1a" stroke-width="11" fill="none"/><g fill="#3fae5a" stroke="#1f6a38" stroke-width="3"><path d="M{x} {745 - h} q-70 -10 -90 50 q50 -34 90 -50Z"/><path d="M{x} {745 - h} q70 -10 90 50 q-50 -34 -90 -50Z"/><path d="M{x} {745 - h} q-10 -70 -60 -80 q40 30 60 80Z"/><path d="M{x} {745 - h} q10 -70 60 -80 q-40 30 -60 80Z"/></g>'
b += spark(1100, 300, 22)
open('B.html', 'w', encoding='utf-8').write(page('#3a1850', svg(d, b), [('A TUNNEL', 135, 'w'), ('THAT MAKES', 135, 'w'), ('AN OASIS', 210, 'y')], '#1a0a24'))

# ---- C: water from thin air (fog nets of the Atacama) ----
d = lin('sk', [(0, '#143a5e'), (.5, '#6aa0b8'), (.75, '#f0c9a0'), (1, '#d8a47e')]) + rad('fg', 600, 760, 700, [(0, '#ffffff', .85), (1, '#ffffff', 0)])
b = '<rect width="1920" height="1080" fill="url(#sk)"/>' + stars(30, 300, 0, '#ffffff', .5, 3)
b += '<path d="M0 840 C300 700 600 780 900 720 C1300 640 1600 760 1920 700 L1920 1080 L0 1080Z" fill="#7a5a48"/><path d="M0 900 C400 820 900 900 1300 840 C1600 800 1800 860 1920 850 L1920 1080 L0 1080Z" fill="#5a3f33"/>'
b += ''.join(f'<ellipse cx="{random.randint(-100, 1100)}" cy="{random.randint(640, 880)}" rx="{random.randint(160, 340)}" ry="{random.randint(40, 80)}" fill="#fff" opacity="{random.uniform(.25, .55):.2f}"/>' for _ in range(16))
b += '<rect width="1920" height="1080" fill="url(#fg)" opacity=".5"/>'
x0, y0, x1, y1 = 1180, 400, 1780, 800
b += f'<g stroke="#e8f4ff" stroke-width="3" opacity=".75">' + ''.join(f'<path d="M{x0} {y} L{x1} {y}"/>' for y in range(y0, y1 + 1, 40)) + ''.join(f'<path d="M{x} {y0} L{x} {y1}"/>' for x in range(x0, x1 + 1, 40)) + '</g>'
b += f'<rect x="{x0 - 16}" y="{y0 - 30}" width="14" height="{y1 - y0 + 200}" fill="#4a3426"/><rect x="{x1 + 2}" y="{y0 - 30}" width="14" height="{y1 - y0 + 200}" fill="#4a3426"/><rect x="{x0 - 16}" y="{y0 - 34}" width="{x1 - x0 + 32}" height="12" fill="#4a3426"/>'
b += ''.join(f'<circle cx="{random.randint(x0 + 10, x1 - 10)}" cy="{random.randint(y0 + 10, y1 - 10)}" r="{random.choice([4, 5, 6, 7])}" fill="#bfe8ff" opacity=".95"/>' for _ in range(45))
b += f'<path d="M{x0 - 10} {y1 + 10} L{x1 + 10} {y1 + 10} L{x1 - 10} {y1 + 34} L{x0 + 10} {y1 + 34}Z" fill="#8fb6c8" stroke="#2f4a5a" stroke-width="4"/>'
b += f'<path d="M{x0 + 20} {y1 + 34} L{x0 + 20} {y1 + 150}" stroke="#8fb6c8" stroke-width="16"/><rect x="{x0 - 40}" y="{y1 + 140}" width="120" height="110" rx="14" fill="#3f8fc4" stroke="#1f4f74" stroke-width="5"/>'
b += ''.join(f'<path d="M{x} {y1 + 38} q-5 14 0 24" stroke="#bfe8ff" stroke-width="5" stroke-linecap="round"/>' for x in (1300, 1500, 1650)) + spark(1000, 360, 22) + spark(1840, 360, 16)
open('C.html', 'w', encoding='utf-8').write(page('#143a5e', svg(d, b), [('WATER', 175, 'w'), ('FROM', 115, 'w'), ('THIN AIR', 190, 'y')], '#081a2e'))
