import sys, math, random
sys.path.insert(0, '/home/user/rp/tools')
from thumb_lib import *
random.seed(5)

# ---- A: dinner inside a dinosaur (Crystal Palace Iguanodon, New Year's Eve 1853) ----
d = lin('bg', [(0, '#0d2a40'), (.45, '#1f5a66'), (.7, '#f2b865'), (.71, '#16301f'), (1, '#0a1a12')]) + lin('bd', [(0, '#a9b59f'), (1, '#6f7d68')]) + lin('am', [(0, '#ffd98a'), (1, '#e5883a')]) + rad('lg', 1400, 680, 520, [(0, '#ffcf7a', .5), (1, '#ffcf7a', 0)])
b = '<rect width="1920" height="1080" fill="url(#bg)"/>' + stars(45, 420) + '<rect width="1920" height="1080" fill="url(#lg)"/>'
b += '<path d="M0 790 L1920 790 L1920 1080 L0 1080Z" fill="#12281a"/>' + blobs(40, 0, 800, 1920, 1060, '#0a1a12', .2, .5, 60, 200)
b += '<g stroke="#3d4a3b" stroke-width="5" stroke-linejoin="round">'
b += '<path d="M1830 660 Q1920 700 1940 820 Q1800 790 1740 790Z" fill="#7b8873"/>'
b += '<rect x="1270" y="840" width="130" height="120" rx="46" fill="#7b8873"/><rect x="1580" y="840" width="130" height="120" rx="46" fill="#7b8873"/>'
b += '<path d="M1130 690 C1100 650 1070 620 1040 600" stroke="#7b8873" stroke-width="120" fill="none" stroke-linecap="round"/>'
b += '<ellipse cx="1460" cy="710" rx="450" ry="220" fill="url(#bd)"/>'
b += '<ellipse cx="1010" cy="590" rx="112" ry="62" transform="rotate(-18 1010 590)" fill="#8e9b86"/><path d="M950 542 L972 490 L995 548Z" fill="#cfd6c6"/>'
b += '<circle cx="1046" cy="570" r="13" fill="#1a1a1a"/></g>'
b += '<rect x="1190" y="585" width="520" height="215" rx="28" fill="url(#am)" stroke="#3d4a3b" stroke-width="6"/>'
for i in range(6):
    x = 1262 + i * 74
    b += f'<g transform="translate({x} 700) scale(1.25)"><rect x="-13" y="-62" width="26" height="9" fill="#111"/><rect x="-9" y="-82" width="18" height="22" fill="#111"/><circle cx="0" cy="-36" r="15" fill="#f1cfa6"/><rect x="-17" y="-21" width="34" height="46" rx="8" fill="#1b1b1b"/></g>'
b += '<rect x="1208" y="738" width="484" height="26" rx="6" fill="#f7efdc"/>'
for x in (1360, 1540):
    b += f'<rect x="{x - 6}" y="700" width="12" height="38" fill="#fff1c9"/><ellipse cx="{x}" cy="690" rx="8" ry="14" fill="#ff9a2e"/>'
open('A.html', 'w', encoding='utf-8').write(page('#0d2a40', svg(d, b), [('DINNER', 170, 'w'), ('INSIDE A', 130, 'w'), ('DINOSAUR', 190, 'y')], '#06121c'))

# ---- B: a century with the wrong head (Brontosaurus skull mix-up) ----
d = lin('bg', [(0, '#f6ead0'), (.7, '#e3d2a8'), (.71, '#c4ae80'), (1, '#a89468')]) + rad('sp', 1300, 380, 700, [(0, '#ffffff', .65), (1, '#ffffff', 0)])
b = '<rect width="1920" height="1080" fill="url(#bg)"/><rect width="1920" height="1080" fill="url(#sp)"/>'
b += '<g stroke="#2f4f4a" stroke-width="6" stroke-linejoin="round" stroke-linecap="round">'
b += '<path d="M1830 800 Q1900 840 1930 900 Q1800 880 1760 850Z" fill="#6f9a8c"/>'
for x in (1290, 1380, 1560, 1650): b += f'<rect x="{x}" y="850" width="62" height="95" rx="22" fill="#5d8a7c"/>'
b += '<ellipse cx="1500" cy="790" rx="345" ry="150" fill="#74a595"/>'
b += '<path d="M1230 760 C1130 640 1290 470 1310 340" stroke="#74a595" stroke-width="96" fill="none"/>'
b += '<rect x="1250" y="262" width="150" height="96" rx="30" fill="#e8725a"/><circle cx="1292" cy="298" r="12" fill="#222"/></g>'
b += '<g fill="none" stroke="#2f4f4a" stroke-width="6" stroke-dasharray="14 12" stroke-linecap="round"><path d="M1500 130 Q1640 90 1790 130 Q1850 150 1840 185 Q1740 215 1580 205 Q1500 195 1500 130Z"/></g>'
b += '<g fill="none" stroke="#c9532f" stroke-width="9" stroke-linecap="round" stroke-linejoin="round"><path d="M1420 250 Q1480 190 1540 215"/><path d="M1500 190 L1545 216 L1498 240"/></g>'
b += spark(1700, 250, 22, '#fff', .9) + spark(1020, 560, 16, '#fff', .8)
open('B.html', 'w', encoding='utf-8').write(page('#efe0bc', svg(d, b), [('A CENTURY', 125, 'w'), ('WITH THE', 125, 'w'), ('WRONG HEAD', 165, 'y')], '#33261a'))

# ---- C: did T. rex have lips? ----
d = lin('bg', [(0, '#2d1450'), (.5, '#b83c5a'), (.78, '#f7a24d'), (1, '#6a2a3a')]) + rad('sn', 1500, 780, 600, [(0, '#ffe2a0', .55), (1, '#ffe2a0', 0)]) + lin('hd', [(0, '#86a844'), (1, '#4f6a2a')])
b = '<rect width="1920" height="1080" fill="url(#bg)"/><rect width="1920" height="1080" fill="url(#sn)"/>' + stars(40, 480, 0, '#ffe8f0', .5, 5)
b += '<g stroke="#2c3d18" stroke-width="7" stroke-linejoin="round">'
b += '<path d="M1000 650 C1040 600 1100 575 1170 570 C1280 560 1330 500 1420 470 C1520 440 1640 430 1740 480 C1830 530 1830 700 1760 780 C1700 840 1560 830 1440 810 C1300 790 1180 760 1060 730 Z" fill="url(#hd)"/>'
b += '<path d="M1360 520 C1400 470 1500 465 1540 500 C1500 505 1420 505 1360 520Z" fill="#3f5a22"/></g>'
b += '<ellipse cx="1465" cy="538" rx="30" ry="26" fill="#f6c34a" stroke="#2c3d18" stroke-width="6"/><ellipse cx="1470" cy="538" rx="7" ry="20" fill="#1a1a1a"/><ellipse cx="1120" cy="610" rx="12" ry="8" fill="#2c3d18"/>'
b += '<path d="M1010 692 C1200 722 1450 760 1710 768" stroke="#e8808a" stroke-width="38" fill="none" stroke-linecap="round"/><path d="M1010 680 C1200 710 1450 748 1710 756" stroke="#f9bcc0" stroke-width="10" fill="none" stroke-linecap="round" opacity=".8"/>'
b += '<g fill="none" stroke="#fff" stroke-width="6" stroke-dasharray="10 8" opacity=".95">' + ''.join(f'<path d="M{1060 + i * 70} {742 + i * 4} l{14 + (i % 3) * 3} {70 - i * 3} l{14 + (i % 3) * 3} {-70 + i * 3}"/>' for i in range(9)) + '</g>'
b += spark(1000, 520, 22) + spark(1720, 330, 18)
open('C.html', 'w', encoding='utf-8').write(page('#2d1450', svg(d, b), [('DID T. REX', 135, 'w'), ('HAVE', 135, 'w'), ('LIPS?', 250, 'y')], '#1a0a2e'))
