import sys, math, random
sys.path.insert(0, '/home/user/rp/tools')
from thumb_lib import *
random.seed(11)
W = 'w'


def scales(n, x0, y0, x1, y1, col, op=(.15, .4), r=(4, 9)):
    """small scale arcs for skin texture (clip outside)"""
    o = ''
    for _ in range(n):
        x, y, rr = random.randint(x0, x1), random.randint(y0, y1), random.uniform(*r)
        o += f'<path d="M{x - rr:.0f} {y:.0f} q{rr:.0f} {-rr * .9:.0f} {2 * rr:.0f} 0" fill="none" stroke="{col}" stroke-width="2.4" opacity="{random.uniform(*op):.2f}"/>'
    return o


BLUR = '<filter id="bl" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="18"/></filter>' \
       '<filter id="bl2" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="6"/></filter>'

# =====================================================================================
# A  (intuitive): New Year's Eve 1853 - dinner inside the half-finished Iguanodon model (script S07)
# =====================================================================================
d = BLUR + lin('sky', [(0, '#081a2e'), (.55, '#123a4f'), (.8, '#1d4d52')]) + lin('gr', [(0, '#10261d'), (1, '#050d09')])
d += rad('warm', 1330, 560, 620, [(0, '#ffc66b', .75), (.35, '#ff9d3d', .32), (1, '#ff8a2a', 0)])
d += rad('inner', 1330, 560, 330, [(0, '#fff0c4', 1), (.5, '#ffbf62', 1), (1, '#d9762c', 1)])
d += lin('stone', [(0, '#a7b29a'), (.5, '#7c8a73'), (1, '#4c5a4a')]) + lin('stone2', [(0, '#8d9a82'), (1, '#3f4b3e')])
d += rad('moon', 420, 170, 260, [(0, '#e9f3ff', .35), (1, '#e9f3ff', 0)])
BODY = 'M985 600 C990 470 1100 372 1300 360 C1480 350 1620 420 1668 540 C1700 620 1690 720 1640 790 C1560 850 1150 860 1040 800 C995 760 982 680 985 600Z'
d += f'<clipPath id="cb"><path d="{BODY}"/></clipPath>'
d += '<clipPath id="cut"><path d="M1040 600 C1060 470 1160 410 1300 404 C1460 398 1580 450 1620 600Z"/></clipPath>'
b = '<rect width="1920" height="1080" fill="url(#sky)"/><rect width="1920" height="1080" fill="url(#moon)"/>' + stars(70, 470, 0, '#e8f4ff', .6, 0)
# the Crystal Palace glass hall far behind (faint)
b += '<g opacity=".32" fill="#5f8fa0">'
b += '<path d="M120 760 L120 640 Q520 560 920 640 L920 760Z"/><path d="M380 640 Q520 520 660 640Z" fill="#8fbccc"/>'
b += ''.join(f'<rect x="{x}" y="650" width="6" height="110" fill="#2b4f5e"/>' for x in range(140, 920, 34)) + '</g>'
# tree silhouettes
for x, h, r in [(60, 560, 120), (230, 600, 90), (560, 610, 100), (1810, 520, 140), (1700, 580, 90), (880, 620, 80)]:
    b += f'<rect x="{x - 9}" y="{h}" width="18" height="{760 - h}" fill="#071510"/><ellipse cx="{x}" cy="{h - r * .4:.0f}" rx="{r}" ry="{r * 1.15:.0f}" fill="#0a1f18"/>'
b += '<rect width="1920" height="1080" fill="url(#warm)"/>'
# ground
b += '<path d="M0 772 Q960 740 1920 772 L1920 1080 L0 1080Z" fill="url(#gr)"/>' + blobs(26, 0, 800, 1500, 1060, '#030806', .25, .5, 70, 220)
b += '<ellipse cx="1330" cy="905" rx="520" ry="46" fill="#ffb760" opacity=".22" filter="url(#bl)"/>'
# lantern string across the garden
b += '<path d="M1640 400 Q1780 470 1930 420" fill="none" stroke="#2d3b33" stroke-width="3"/>'
for x, y in [(1700, 428), (1780, 446), (1860, 438)]:
    b += f'<circle cx="{x}" cy="{y + 14}" r="22" fill="#ffcf7a" opacity=".35" filter="url(#bl2)"/><rect x="{x - 9}" y="{y}" width="18" height="26" rx="6" fill="#ffd98a" stroke="#5a3a1a" stroke-width="2.5"/>'
L = 'stroke="#283528" stroke-width="5" stroke-linejoin="round" stroke-linecap="round"'
# far legs (darker)
b += f'<g {L} fill="#3f4b3e"><path d="M1110 760 L1100 905 Q1135 918 1170 905 L1175 760Z"/><path d="M1540 760 L1535 900 Q1572 914 1608 900 L1610 750Z"/></g>'
# tail
b += f'<path d="M1640 640 C1740 650 1820 700 1930 690 L1930 742 C1820 760 1720 740 1630 740Z" fill="url(#stone2)" {L}/>'
# ridge spikes on neck and tail
b += ''.join(f'<path d="M{x} {y} l12 -26 l12 26Z" fill="#9aa68e" {L}/>' for x, y in [(1700, 648), (1750, 656), (1800, 668), (1850, 676), (1890, 676)])
b += ''.join(f'<path d="M{x} {y} l10 -24 l12 22Z" fill="#9aa68e" {L}/>' for x, y in [(900, 586), (940, 570), (980, 562)])
# neck + head (Crystal Palace style: low head, horn on the nose)
b += f'<path d="M1010 560 C940 560 880 590 850 640 L905 700 C940 680 980 670 1030 680Z" fill="url(#stone)" {L}/>'
b += f'<path d="M700 676 C705 640 750 612 810 606 C870 600 925 620 935 660 C945 700 910 728 860 734 C800 742 735 735 712 718 C700 708 698 690 700 676Z" fill="url(#stone)" {L}/>'
b += f'<path d="M742 616 L752 548 L782 610Z" fill="#d7dccb" {L}/>'  # the famous nose horn
b += f'<path d="M712 700 C760 708 820 712 900 704" fill="none" {L}/>'
b += '<circle cx="868" cy="640" r="12" fill="#1a1a14"/><circle cx="872" cy="636" r="4" fill="#fff"/><path d="M846 624 Q868 612 892 624" fill="none" stroke="#283528" stroke-width="5" stroke-linecap="round"/>'
b += '<path d="M716 650 C740 628 790 616 840 616" fill="none" stroke="#e7ead9" stroke-width="5" opacity=".5" stroke-linecap="round"/>'
# body shell
b += f'<path d="{BODY}" fill="url(#stone)" {L}/>'
b += f'<g clip-path="url(#cb)">{scales(260, 980, 600, 1700, 860, "#2f3a2e", (.2, .45), (6, 12))}' \
     '<path d="M985 760 C1150 850 1500 850 1690 740 L1700 900 L980 900Z" fill="#1f2a20" opacity=".45"/></g>'
# the cut-open back: warm room inside
b += '<path d="M1040 600 C1060 470 1160 410 1300 404 C1460 398 1580 450 1620 600Z" fill="url(#inner)"/>'
b += '<g clip-path="url(#cut)">'
b += '<path d="M1040 410 L1620 410 L1620 470 Q1330 520 1040 470Z" fill="#c7672a" opacity=".55"/>'  # canopy shadow
for x in range(1080, 1620, 60):
    b += f'<path d="M{x} 404 Q{x + 30} 440 {x + 60} 404" fill="#f7e2b0" opacity=".55" stroke="#b2662e" stroke-width="2"/>'  # bunting
# chandelier
b += '<path d="M1330 404 L1330 452" stroke="#5a3a1a" stroke-width="4"/><path d="M1280 470 Q1330 492 1380 470" fill="none" stroke="#5a3a1a" stroke-width="5"/>'
for x in (1280, 1310, 1350, 1380):
    b += f'<circle cx="{x}" cy="462" r="13" fill="#fff6d0" filter="url(#bl2)"/><circle cx="{x}" cy="462" r="5" fill="#fff"/>'
# diners in top hats (heads and shoulders above the shell rim)
skins = ['#f1cfa6', '#e8bf93', '#f3d6b3', '#ddb088', '#f0c9a0', '#e9c39b', '#f2d0aa']
for i, x in enumerate(range(1100, 1600, 72)):
    lift = -14 if i == 3 else 0
    s = skins[i]
    b += f'<g transform="translate({x} {lift})">'
    b += '<path d="M-38 610 C-38 572 -22 556 0 556 C22 556 38 572 38 610Z" fill="#1d1d24" stroke="#0c0c10" stroke-width="3"/>'
    b += '<path d="M-8 560 L0 584 L8 560Z" fill="#f7f2e6"/>'
    b += f'<circle cx="0" cy="534" r="24" fill="{s}" stroke="#5a3a24" stroke-width="3"/>'
    b += f'<circle cx="-8" cy="532" r="3" fill="#2a1c14"/><circle cx="8" cy="532" r="3" fill="#2a1c14"/><path d="M-7 545 Q0 551 7 545" fill="none" stroke="#7a3a2a" stroke-width="2.5" stroke-linecap="round"/>'
    if i % 2 == 0:
        b += '<path d="M-22 524 Q-24 506 -16 512 M22 524 Q24 506 16 512" fill="none" stroke="#6b4a2a" stroke-width="4"/>'
    b += '<rect x="-30" y="508" width="60" height="7" rx="3" fill="#111"/><rect x="-19" y="466" width="38" height="46" rx="3" fill="#15151a"/><rect x="-19" y="500" width="38" height="6" fill="#6d2a2a"/>'
    b += '</g>'
# table
b += '<rect x="1060" y="584" width="560" height="22" rx="4" fill="#fffaf0"/>'
for x in (1180, 1330, 1480):
    b += f'<rect x="{x - 5}" y="548" width="10" height="36" fill="#fff4d6"/><ellipse cx="{x}" cy="540" rx="7" ry="12" fill="#ffb03a"/><circle cx="{x}" cy="540" r="18" fill="#ffd77a" opacity=".5" filter="url(#bl2)"/>'
for x in (1130, 1255, 1405, 1545):
    b += f'<path d="M{x - 7} 560 L{x + 7} 560 L{x + 3} 576 L{x - 3} 576Z" fill="#fff" opacity=".85"/><rect x="{x - 1}" y="576" width="2" height="9" fill="#fff"/>'
b += '</g>'
# iron frame ribs over the opening (half-finished shell)
b += '<g fill="none" stroke="#2c241c" stroke-width="7" stroke-linecap="round">'
b += '<path d="M1040 600 C1060 470 1160 410 1300 404 C1460 398 1580 450 1620 600"/>'
for x0, x1 in [(1120, 1170), (1220, 1250), (1420, 1400), (1530, 1500)]:
    b += f'<path d="M{x0} 600 L{x1} {420 if x0 < 1300 else 418}" opacity=".5" stroke-width="5"/>'
b += '</g>'
# rim (thick shell edge lit by the room)
b += '<path d="M1030 604 Q1330 640 1630 604" fill="none" stroke="#283528" stroke-width="14" stroke-linecap="round"/>'
b += '<path d="M1030 598 Q1330 632 1630 598" fill="none" stroke="#ffd58a" stroke-width="6" stroke-linecap="round" opacity=".9"/>'
b += '<path d="M1000 560 C1020 470 1120 395 1290 384" fill="none" stroke="#ffd58a" stroke-width="5" opacity=".35" stroke-linecap="round"/>'
# near legs
b += f'<g {L} fill="url(#stone)"><path d="M1040 740 L1030 912 Q1072 928 1114 912 L1112 760Z"/><path d="M1470 760 L1462 912 Q1504 928 1546 912 L1550 750Z"/></g>'
for x in (1072, 1504):
    b += ''.join(f'<path d="M{x + k} 912 l0 -14" stroke="#283528" stroke-width="4"/>' for k in (-22, 0, 22))
# a little ladder up to the opening
b += '<g stroke="#5b3d22" stroke-width="7" stroke-linecap="round"><path d="M1196 916 L1236 640"/><path d="M1262 916 L1296 640"/>' + ''.join(f'<path d="M{1199 + k * 4.6:.0f} {880 - k * 32} L{1265 + k * 4.4:.0f} {880 - k * 32}"/>' for k in range(8)) + '</g>'
b += spark(1690, 420, 18) + spark(960, 470, 14) + spark(1580, 330, 12) + spark(1760, 600, 10)
A = page('#081a2e', svg(d, b), [('DINNER', 175, W), ('INSIDE A', 120, W), ('DINOSAUR', 180, 'y')], '#06121c', top=36)
open('A.html', 'w', encoding='utf-8').write(A)

# =====================================================================================
# B  (film homage: the JAWS poster - a swimmer at the surface, a monster rising from the deep)
#     Elasmosaurus as Cope drew it in 1869 (script S10): the head at the tip of the tail, the long neck left headless
# =====================================================================================
d = BLUR + lin('sea', [(0, '#bff4f2'), (.17, '#5fc6cf'), (.2, '#2a8ea5'), (.55, '#0d4a6a'), (1, '#021424')])
d += rad('lit', 1260, 200, 760, [(0, '#c9fff6', .5), (1, '#c9fff6', 0)])
d += lin('skin', [(0, '#7fb6a6'), (.5, '#3f7d78'), (1, '#173c45')], 1, 1)
b = '<rect width="1920" height="1080" fill="url(#sea)"/><rect width="1920" height="1080" fill="url(#lit)"/>'
# light rays from the surface
for x, w, o in [(980, 120, .16), (1180, 80, .2), (1380, 140, .14), (1560, 70, .12), (760, 90, .1), (1700, 110, .1)]:
    b += f'<path d="M{x} 210 L{x + w} 210 L{x + w * 2.6 - 260:.0f} 1080 L{x - 300} 1080Z" fill="#dffff6" opacity="{o}" filter="url(#bl2)"/>'
# surface (seen from below)
b += '<path d="M0 214 Q120 196 240 214 T480 214 T720 214 T960 214 T1200 214 T1440 214 T1680 214 T1920 214 L1920 0 L0 0Z" fill="#a7ecea" opacity=".55"/>'
b += '<path d="M0 214 Q120 196 240 214 T480 214 T720 214 T960 214 T1200 214 T1440 214 T1680 214 T1920 214" fill="none" stroke="#f2fffd" stroke-width="5" opacity=".8"/>'
b += ''.join(f'<path d="M{x} {y} q30 -10 60 0" fill="none" stroke="#ffffff" stroke-width="3" opacity=".45"/>' for x, y in [(820, 150), (1500, 120), (1100, 90), (1700, 170), (960, 60), (1350, 160)])
# swimmer silhouette at the surface
SW = 'fill="none" stroke="#13242e" stroke-linecap="round" stroke-linejoin="round"'
b += '<g transform="translate(1440 236) rotate(-4)">'
b += f'<path d="M-60 0 L60 4" {SW} stroke-width="46"/><circle cx="-92" cy="-2" r="25" fill="#13242e"/>'
b += f'<path d="M-50 -14 Q-110 -60 -175 -52" {SW} stroke-width="17"/><circle cx="-180" cy="-52" r="11" fill="#13242e"/>'
b += f'<path d="M-46 16 Q-70 60 -60 110" {SW} stroke-width="17"/><circle cx="-60" cy="114" r="11" fill="#13242e"/>'
b += f'<path d="M56 -6 Q120 -20 190 -40" {SW} stroke-width="21"/><path d="M188 -40 l26 -8" {SW} stroke-width="14"/>'
b += f'<path d="M56 12 Q120 34 182 70" {SW} stroke-width="21"/><path d="M182 70 l22 14" {SW} stroke-width="14"/></g>'
b += '<ellipse cx="1330" cy="230" rx="300" ry="34" fill="#ffffff" opacity=".18" filter="url(#bl2)"/>'
# bubbles / particles
for _ in range(70):
    x, y = random.randint(600, 1900), random.randint(240, 1040)
    b += f'<circle cx="{x}" cy="{y}" r="{random.choice([2, 3, 4, 6])}" fill="none" stroke="#dffaff" stroke-width="2" opacity="{random.uniform(.15, .5):.2f}"/>'
# ---- the Elasmosaurus, rising tail-first (= head-first in Cope's version) ----
S = 'stroke="#0b2a33" stroke-width="6" stroke-linejoin="round" stroke-linecap="round"'
NECK = 'M930 760 C800 830 660 860 560 900 C440 950 400 1000 440 1030 C490 1062 570 1050 640 1036'
b += f'<path d="{NECK}" fill="none" stroke="#0b2a33" stroke-width="96" stroke-linecap="round"/>'
b += f'<path d="{NECK}" fill="none" stroke="url(#skin)" stroke-width="84" stroke-linecap="round"/>'
b += '<path d="M930 724 C800 794 660 824 560 862 C460 904 410 950 400 990" fill="none" stroke="#bfe9dc" stroke-width="8" opacity=".45" stroke-linecap="round"/>'
# where the head SHOULD be: a faint dashed ghost at the end of the long neck
b += '<ellipse cx="780" cy="1010" rx="170" ry="110" fill="#e9fff8" opacity=".16" filter="url(#bl)"/>'
b += '<g transform="translate(650 1034) rotate(-10) scale(1.2)" fill="none" stroke="#f2fffb" stroke-width="6" stroke-dasharray="16 11" stroke-linecap="round"><path d="M0 -30 C40 -46 120 -50 175 -32 C196 -24 200 4 180 20 C130 40 60 40 0 30"/><circle cx="58" cy="-12" r="11"/><path d="M90 6 L184 2"/></g>'
b += f'<path d="M1040 760 C1000 840 960 900 900 950 C960 930 1030 880 1080 810Z" fill="#244f56" {S}/>'
b += f'<path d="M1180 600 C1250 560 1320 540 1400 540 C1340 580 1280 620 1210 650Z" fill="#244f56" {S}/>'
BD = 'M900 760 C900 650 1000 560 1120 520 C1220 488 1300 500 1320 540 C1340 600 1270 700 1170 770 C1080 830 900 860 900 760Z'
b += f'<path d="{BD}" fill="url(#skin)" {S}/>'
b += '<path d="M930 800 C1000 820 1100 790 1180 740 C1250 690 1300 620 1310 560" fill="none" stroke="#d6ecd6" stroke-width="16" opacity=".35" stroke-linecap="round"/>'
b += f'<clipPath id="cbd"><path d="{BD}"/></clipPath>'
b += f'<g clip-path="url(#cbd)">' + ''.join(f'<circle cx="{random.randint(900, 1330)}" cy="{random.randint(500, 860)}" r="{random.randint(5, 12)}" fill="#1c4a50" opacity="{random.uniform(.2, .45):.2f}"/>' for _ in range(60)) + '</g>'
b += '<path d="M960 640 C1030 560 1160 500 1290 506" fill="none" stroke="#e6fff6" stroke-width="7" opacity=".55" stroke-linecap="round"/>'
b += f'<path d="M980 760 C920 800 850 830 770 840 C830 800 900 760 950 720Z" fill="#3f7d78" {S}/>'
b += f'<path d="M1240 680 C1330 690 1410 720 1470 770 C1400 760 1320 740 1230 720Z" fill="#3f7d78" {S}/>'
b += f'<path d="M1210 560 C1250 480 1290 430 1318 384 L1346 394 C1336 450 1330 520 1312 590Z" fill="url(#skin)" {S}/>'
b += '<g transform="translate(1330 380) rotate(-62)">'
b += f'<path d="M0 -26 C40 -40 110 -46 170 -30 C190 -24 200 -12 196 -4 L60 6 L0 20Z" fill="#5c9a8e" {S}/>'
b += f'<path d="M0 20 L60 14 L180 46 C170 62 120 70 60 58 C30 52 6 42 0 20Z" fill="#3d7570" {S}/>'
b += '<path d="M60 6 L196 -4 L180 46 L60 14Z" fill="#4a0f1e"/>'
b += ''.join(f'<path d="M{70 + i * 16} {5 - i * .6:.1f} l5 13 l5 -13Z" fill="#fffbe8"/>' for i in range(8))
b += ''.join(f'<path d="M{72 + i * 14} {16 + i * 3.6:.1f} l5 -13 l5 13Z" fill="#fffbe8"/>' for i in range(8))
b += '<circle cx="52" cy="-18" r="11" fill="#fff4b0"/><circle cx="55" cy="-18" r="5" fill="#111"/>'
b += '<path d="M30 -34 C60 -44 120 -48 160 -36" fill="none" stroke="#e6fff6" stroke-width="5" opacity=".7" stroke-linecap="round"/></g>'
b += '<circle cx="1420" cy="300" r="120" fill="#e9fff6" opacity=".12" filter="url(#bl)"/>'
b += spark(1580, 330, 18, '#ffffff') + spark(1180, 300, 14, '#ffffff') + spark(860, 620, 12, '#ffffff')
B = page('#0d4a6a', svg(d, b), [('HEAD', 205, W), ('ON THE', 125, W), ('TAIL', 235, 'y')], '#04202e', top=30)
open('B.html', 'w', encoding='utf-8').write(B)

# =====================================================================================
# C  (film homage: the side-mirror chase in Jurassic Park, 1993 - a T. rex charging in the mirror)
#     but with lips covering its teeth (Cullen et al. 2023, script S35; stays a question)
# =====================================================================================
GX, GY, GW, GH = 1010, 250, 760, 500  # mirror glass
d = BLUR + lin('jg', [(0, '#1e3a1c'), (.6, '#2f5a26'), (1, '#0d1a0c')]) + rad('sun', 520, 160, 900, [(0, '#ffe7a3', .55), (1, '#ffe7a3', 0)])
d += lin('msky', [(0, '#fff4cf'), (.45, '#bfe2b8'), (1, '#7fb377')]) + lin('road', [(0, '#c9a874'), (1, '#8a6a42')])
d += lin('rex', [(0, '#8c8a5a'), (.55, '#5f6640'), (1, '#353a22')]) + lin('jaw', [(0, '#a49a6c'), (1, '#6a6544')])
d += lin('door', [(0, '#7d2a22'), (1, '#36100c')]) + lin('house', [(0, '#3a3a3a'), (1, '#121212')])
d += f'<clipPath id="gl"><rect x="{GX}" y="{GY}" width="{GW}" height="{GH}" rx="70"/></clipPath>'
d += rad('mglow', GX + GW / 2, GY + GH / 2, 620, [(0, '#fff3c4', .45), (1, '#fff3c4', 0)])
b = '<rect width="1920" height="1080" fill="url(#jg)"/>'
g = ''
for _ in range(60):
    x, y = random.randint(-100, 2000), random.randint(80, 900)
    g += f'<ellipse cx="{x}" cy="{y}" rx="{random.randint(120, 320)}" ry="{random.randint(40, 120)}" fill="{random.choice(["#3c6e2c", "#264a1e", "#5b8a36", "#1a3314", "#7aa04a"])}" opacity="{random.uniform(.35, .8):.2f}"/>'
for x in range(-40, 1960, 170):
    g += f'<rect x="{x + random.randint(-30, 30)}" y="0" width="{random.randint(26, 60)}" height="1080" fill="#142810" opacity=".5"/>'
b += f'<g filter="url(#bl)">{g}</g>'
b += ''.join(f'<path d="M{random.randint(0, 1800)} {y} l{random.randint(160, 420)} 0" stroke="#e8f5c8" stroke-width="4" opacity=".22" stroke-linecap="round"/>' for y in range(120, 900, 46))
b += '<rect width="1920" height="1080" fill="url(#sun)"/><rect width="1920" height="1080" fill="url(#mglow)"/>'
b += '<path d="M0 900 L1500 880 Q1560 878 1600 900 L1600 1080 L0 1080Z" fill="url(#door)" stroke="#2a0a08" stroke-width="6"/>'
b += '<path d="M0 912 L1500 892" stroke="#ff9d86" stroke-width="5" opacity=".5"/>'
b += '<path d="M1200 890 L1240 760 L1300 760 L1290 890Z" fill="#1a1a1a" stroke="#000" stroke-width="5"/>'
b += f'<rect x="{GX - 30}" y="{GY - 30}" width="{GW + 60}" height="{GH + 60}" rx="96" fill="url(#house)" stroke="#000" stroke-width="7"/>'
b += f'<path d="M{GX + 40} {GY - 22} L{GX + GW - 40} {GY - 22}" stroke="#7a7a7a" stroke-width="6" opacity=".7" stroke-linecap="round"/>'
r = f'<rect x="{GX}" y="{GY}" width="{GW}" height="{GH}" fill="url(#msky)"/>'
r += f'<path d="M{GX} {GY + 250} Q{GX + 200} {GY + 200} {GX + 380} {GY + 230} Q{GX + 560} {GY + 190} {GX + GW} {GY + 240} L{GX + GW} {GY + GH} L{GX} {GY + GH}Z" fill="#4f8a3a"/>'
r += f'<path d="M{GX + 330} {GY + 225} L{GX + 420} {GY + 225} L{GX + 700} {GY + GH} L{GX + 40} {GY + GH}Z" fill="url(#road)"/>'
for x, h in [(40, 170), (110, 220), (640, 200), (720, 240), (580, 150)]:
    r += f'<rect x="{GX + x - 8}" y="{GY + 250 - h}" width="16" height="{h}" fill="#3e5a2a"/><ellipse cx="{GX + x}" cy="{GY + 250 - h}" rx="70" ry="46" fill="#5d9442"/>'
TX, TY = GX + 40, GY + 120
t = f'<g transform="translate({TX} {TY})">'
RS = 'stroke="#1f2412" stroke-width="6" stroke-linejoin="round"'
t += f'<path d="M700 20 C780 -30 860 -80 940 -120 L960 40 C880 70 800 110 720 140Z" fill="url(#rex)" {RS}/>'  # tail (off the glass)
t += f'<ellipse cx="660" cy="140" rx="210" ry="150" fill="url(#rex)" {RS}/>'  # torso
t += f'<path d="M700 300 L650 420 L740 420 L770 300Z" fill="#4a5232" {RS}/>'  # far leg
t += f'<ellipse cx="640" cy="250" rx="100" ry="125" fill="#6b7046" {RS}/>'  # thigh
t += f'<path d="M600 330 L560 430 L650 430 L690 330Z" fill="#5f6640" {RS}/>'  # near shin
t += f'<path d="M370 10 C440 -50 540 -50 600 0 L580 250 C520 280 450 270 400 250Z" fill="url(#rex)" {RS}/>'  # neck
t += '<path d="M430 -20 C480 -44 540 -40 590 -6" fill="none" stroke="#e8e2b0" stroke-width="9" opacity=".4" stroke-linecap="round"/>'
t += ''.join(f'<path d="M{450 + k * 46} {-30 + k * 4} q16 30 4 70" fill="none" stroke="#2a2e18" stroke-width="7" opacity=".35"/>' for k in range(6))
t += '<path d="M520 270 C510 300 496 318 478 326 M478 326 l-10 14 M478 326 l4 18" fill="none" stroke="#1f2412" stroke-width="11" stroke-linecap="round"/>'  # tiny arm
HEAD = 'M0 116 C8 76 60 52 130 44 C200 36 250 4 320 -12 C384 -24 432 8 448 70 C464 140 446 222 402 252 C342 282 252 270 190 256 C120 242 50 214 20 186 C0 166 -6 142 0 116Z'
t += f'<path d="{HEAD}" fill="url(#rex)" stroke="#1f2412" stroke-width="7" stroke-linejoin="round"/>'
t += f'<clipPath id="ch"><path d="{HEAD}"/></clipPath><g clip-path="url(#ch)">'
t += '<path d="M8 150 C90 166 170 178 250 184 C320 190 390 200 460 214 L460 300 L0 300Z" fill="url(#jaw)"/>'
t += '<path d="M180 60 C240 20 300 0 360 4 L380 60 C320 50 250 70 200 90Z" fill="#3f4528" opacity=".35"/>'
t += '<path d="M330 236 C360 200 400 170 440 160" fill="none" stroke="#2a2e18" stroke-width="6" opacity=".4"/>'
t += scales(180, 0, -20, 460, 290, '#2a2e18', (.25, .5), (4, 9))
t += '<path d="M60 70 C160 60 260 40 360 30" fill="none" stroke="#e8e2b0" stroke-width="10" opacity=".45" stroke-linecap="round"/>'
t += '</g>'
t += '<path d="M10 146 C80 156 150 166 220 172 C280 177 330 186 372 200" fill="none" stroke="#1f2412" stroke-width="8" stroke-linecap="round"/>'
t += '<path d="M14 140 C80 150 150 159 220 165 C280 170 330 178 372 192" fill="none" stroke="#d6c58e" stroke-width="5" opacity=".8" stroke-linecap="round"/>'
t += ''.join(f'<path d="M{30 + k * 42} {148 + k * 5.4:.0f} q21 9 42 2" fill="none" stroke="#c9b67e" stroke-width="4" opacity=".75"/>' for k in range(8))
t += '<ellipse cx="44" cy="102" rx="14" ry="8" fill="#1f2412"/>'
t += '<path d="M268 64 C300 36 352 34 384 58" fill="none" stroke="#1f2412" stroke-width="16" stroke-linecap="round"/>'
t += '<path d="M240 40 C250 18 270 10 286 22" fill="#7a7650" stroke="#1f2412" stroke-width="5"/>'
t += '<ellipse cx="326" cy="86" rx="22" ry="18" fill="#ffcf3a" stroke="#1f2412" stroke-width="6"/><ellipse cx="330" cy="86" rx="6" ry="15" fill="#111"/><circle cx="320" cy="80" r="4" fill="#fff"/>'
t += '</g>'
r += t
r += ''.join(f'<path d="M{GX + 500 + random.randint(0, 200)} {GY + y} l{random.randint(60, 140)} 0" stroke="#fffbe6" stroke-width="4" opacity=".55" stroke-linecap="round"/>' for y in range(60, 420, 38))
r += f'<path d="M{GX + GW - 150} {GY + GH} L{GX + GW} {GY + GH - 210} L{GX + GW} {GY + GH}Z" fill="#8e2a22"/>'
r += f'<path d="M{GX + GW - 150} {GY + GH} L{GX + GW} {GY + GH - 210}" stroke="#f0a090" stroke-width="5" opacity=".7"/>'
r += f'<path d="M{GX + 380} {GY} L{GX + 470} {GY} L{GX + 250} {GY + GH} L{GX + 160} {GY + GH}Z" fill="#ffffff" opacity=".13"/>'
r += f'<path d="M{GX + 500} {GY} L{GX + 530} {GY} L{GX + 310} {GY + GH} L{GX + 280} {GY + GH}Z" fill="#ffffff" opacity=".12"/>'
b += f'<g clip-path="url(#gl)">{r}</g>'
b += f'<rect x="{GX}" y="{GY}" width="{GW}" height="{GH}" rx="70" fill="none" stroke="#d8d8d8" stroke-width="5" opacity=".6"/>'
b += spark(GX + GW + 40, GY + 40, 22) + spark(GX - 50, GY + GH - 40, 14) + spark(GX + 520, GY - 60, 14)
C = page('#1e3a1c', svg(d, b), [('DID T. REX', 150, W), ('HAVE', 120, W), ('LIPS?', 260, 'y')], '#0c1608', top=40)
open('C.html', 'w', encoding='utf-8').write(C)
