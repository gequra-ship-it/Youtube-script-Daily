# Shorts thumbnails, VERTICAL 1080x1920 (guideline 16-9, miya 2026-11-06 correction: shorts ratio, text centred, no empty corner).
# Run: python3 videos/seedless-banana/thumb/shorts_make_v.py  -> videos/seedless-banana-shortN/thumb/A.html (N=1..5)
# then: SLUG=seedless-banana-shortN python3 tools/thumb_shot.py
# Same scene ideas as shorts_make.py (old 16:9 version), recomposed for 9:16: art above and below a centred text band,
# nothing important in the top ~200px / bottom ~300px (YouTube UI).
# short1  3 SETS = / SEEDLESS        two chromosomes + glowing 3rd above, big seedless banana below; lab frog.
# short2  ALREADY / EXTINCT / ONCE   sunset, wilted plantation, tombstone "R.I.P. BIG MIKE"; mourning frog.
# short3  SAVED BY / A DUKE          night, glowing Victorian greenhouse with a banana plant; frog in top hat + monocle.
# short4  A BANANA / IS A / BERRY    strawberry + raspberry flung out of a "BERRIES" crate holding a prize banana; detective frog.
# short5  NOT A / TREE!              cutaway banana plant: onion-ring pseudostem slice, underground corm with pups; miner frog.
import os, sys, math, random, shutil
HERE = os.path.dirname(os.path.abspath(__file__))
VID = os.path.dirname(os.path.dirname(HERE))
TOOLS = os.path.join(VID, '..', 'tools')
_src = open(os.path.join(HERE, 'shorts_make.py')).read().split('\nfor n, fn in enumerate(')[0]
exec(_src)  # frog, banana, frame, off, leaf, chrom, dead_plant, strawberry, raspberry, FILTERS, P, lin, rad, spark, INK, RIPE
sys.path.insert(0, TOOLS)
from thumb_lib import vpage, vsvg

W, H = 1080, 1920
VV = lambda i, c='#000', a=.8: rad(i, 540, 960, 1250, [(0, c, 0), (.6, c, 0), (1, c, a)])


def dust(rnd, n, x0, x1, y0, y1, col):
    return ''.join(f'<circle cx="{rnd.uniform(x0, x1):.0f}" cy="{rnd.uniform(y0, y1):.0f}" r="{rnd.choice([1.5, 2.2, 3])}" fill="{col}" opacity="{rnd.uniform(.2, .7):.2f}"/>' for _ in range(n))


def v1():
    rnd = random.Random(11)
    d = FILTERS + lin('bg1', [(0, '#0a1a30'), (.45, '#1b1a4a'), (1, '#0a0a20')])
    d += rad('halo1', 540, 470, 520, [(0, '#ffe68a', .45), (.45, '#f2b23a', .14), (1, '#000', 0)])
    d += rad('halo1b', 560, 1260, 560, [(0, '#ffe68a', .45), (.45, '#f2b23a', .14), (1, '#000', 0)])
    d += lin('table1', [(0, '#2a3666'), (1, '#0a0e24')]) + VV('vig1', '#05061a')
    b = f'<rect width="{W}" height="{H}" fill="url(#bg1)"/>'
    for k in range(2):
        pts = [(x, 300 + k * 70 + 70 * math.sin(x / 110 + k * math.pi)) for x in range(-20, 1100, 20)]
        b += f'<polyline points="{P(pts)}" fill="none" stroke="#5ad0ff" stroke-width="5" opacity=".16"/>'
    b += f'<rect width="{W}" height="{H}" fill="url(#halo1)"/><rect width="{W}" height="{H}" fill="url(#halo1b)"/>'
    b += dust(rnd, 50, 20, 1060, 200, 1200, '#fff4c8')
    # chromosomes above the text: two plain + the extra glowing gold one
    b += chrom(240, 480, 1.05, -12, '#ff8fc8', '#b0407a')
    b += chrom(520, 440, 1.05, 10, '#7ac8ff', '#2a6aa8')
    b += chrom(820, 470, 1.3, -6, '#ffe070', '#c08a10', glow='#fff2a0')
    b += '<text x="380" y="500" text-anchor="middle" font-family="Fredoka" font-weight="700" font-size="80" fill="#fff" opacity=".85">+</text>'
    b += '<text x="665" y="500" text-anchor="middle" font-family="Fredoka" font-weight="700" font-size="80" fill="#fff" opacity=".85">+</text>'
    b += spark(960, 300, 26, '#fffbe0') + spark(690, 610, 16) + spark(110, 330, 14, '#ffe9ff')
    # table + big banana under the text
    b += '<path d="M0 1340 L1080 1310 L1080 1920 L0 1920Z" fill="url(#table1)"/><path d="M0 1340 L1080 1310" stroke="#6a7ad0" stroke-width="4" opacity=".5"/>'
    b += '<ellipse cx="660" cy="1400" rx="360" ry="40" fill="#000" opacity=".5" filter="url(#b14)"/>'
    art, _ = banana(((330, 1150), (440, 1380), (860, 1420), (1000, 1120)), 130, RIPE, line='#3a1c04', lw=7, stem=True, spots=10, rnd=rnd, glow='#ffd84a')
    b += art + spark(1010, 1190, 20, '#fffbe0') + spark(600, 1170, 14)
    coat = ('<path d="M-36 -40 Q-44 -6 -36 4 L-4 4 L-2 -34 Z" fill="#f2f0f8" stroke-width="3.4"/>'
            '<path d="M44 -40 Q52 -6 46 4 L14 4 L12 -34 Z" fill="#f2f0f8" stroke-width="3.4"/>')
    goggles = ('<path d="M-30 -94 Q6 -104 42 -94" fill="none" stroke="#2a2a3a" stroke-width="6"/>'
               '<ellipse cx="-6" cy="-96" rx="14" ry="10" fill="#9ae8ff" stroke-width="3.4"/><ellipse cx="24" cy="-96" rx="14" ry="10" fill="#9ae8ff" stroke-width="3.4"/>')
    b += '<circle cx="170" cy="1440" r="150" fill="#9ae8ff" opacity=".14" filter="url(#b50)"/>'
    b += frog(165, 1590, 2.5, rot=3, look=(10, -6), mouth='O', shadow=True, mid=coat, top=goggles,
              armL='M-34 -22 q-18 4 -22 22', armR='M38 -22 q26 -14 34 -46')
    b += f'<rect width="{W}" height="{H}" fill="url(#vig1)"/>'
    return vpage('#0a1a30', vsvg(d, b), [('3 SETS =', 150, 'w'), ('SEEDLESS', 176, 'y')], outline='#060a1c', top=690)


def v2():
    rnd = random.Random(22)
    d = FILTERS + lin('sky2', [(0, '#140f26'), (.35, '#3a2648'), (.62, '#a8524a'), (.7, '#e89a5a'), (1, '#e89a5a')])
    d += rad('sun2', 560, 1220, 560, [(0, '#ffd890', .95), (.35, '#f29a5a', .4), (1, '#f29a5a', 0)])
    d += lin('stone2', [(0, '#b0b0bc'), (.5, '#7a7a88'), (1, '#4a4a58')], x2=1, y2=.3)
    d += lin('ground2', [(0, '#2a1e22'), (1, '#0c080a')]) + VV('vig2', '#08040a')
    b = f'<rect width="{W}" height="{H}" fill="url(#sky2)"/><rect width="{W}" height="{H}" fill="url(#sun2)"/>'
    b += dust(rnd, 60, 20, 1060, 180, 700, '#ffe8f0')
    b += '<circle cx="860" cy="330" r="46" fill="#ffe8e0" opacity=".85"/><circle cx="860" cy="330" r="90" fill="#ffe8e0" opacity=".15" filter="url(#b26)"/>'
    far = ''.join(dead_plant(x, 1270, rnd.uniform(150, 210), rnd, '#3a2632', '#4a2e3a') for x in range(-20, 1120, 150))
    b += f'<g opacity=".8">{far}</g>'
    b += dead_plant(70, 1340, 470, rnd, '#2a1c1e', '#3a2a22') + dead_plant(1010, 1330, 420, rnd, '#2a1c1e', '#3a2a22')
    b += '<path d="M0 1270 Q540 1240 1080 1280 L1080 1920 L0 1920Z" fill="url(#ground2)"/>'
    # tombstone under the text
    sx, top, bot, hw = 600, 1060, 1560, 230
    stone = f'M{sx - hw} {bot} L{sx - hw} {top + 170} Q{sx - hw} {top} {sx} {top} Q{sx + hw} {top} {sx + hw} {top + 170} L{sx + hw} {bot}Z'
    b += f'<ellipse cx="{sx}" cy="{bot + 6}" rx="320" ry="36" fill="#000" opacity=".55" filter="url(#b14)"/>'
    b += f'<path d="{stone}" fill="#2a2a34" transform="translate(14 10)"/>'
    b += f'<path d="{stone}" fill="url(#stone2)" stroke="#1a1a22" stroke-width="10" stroke-linejoin="round"/>'
    b += f'<path d="M{sx - hw + 24} {top + 170} Q{sx - hw + 24} {top + 26} {sx} {top + 26}" fill="none" stroke="#fff" stroke-width="10" opacity=".35" stroke-linecap="round"/>'
    b += f'<path d="M{sx + hw - 22} {top + 230} l-30 50 l20 30 l-26 60" fill="none" stroke="#2a2a34" stroke-width="5"/>'
    p = ((sx - 110, top + 130), (sx - 70, top + 220), (sx + 70, top + 230), (sx + 130, top + 110))
    F = frame(p, 44)
    b += f'<path d="M{P(off(F, 1))} L{P(off(F, -1)[::-1])}Z" fill="#5a5a68" stroke="#2a2a34" stroke-width="6" transform="translate(4 5)"/>'
    b += f'<path d="M{P(off(F, 1))} L{P(off(F, -1)[::-1])}Z" fill="#9a9aa8" stroke="#4a4a58" stroke-width="5"/>'
    b += (f'<text x="{sx}" y="{top + 350}" text-anchor="middle" font-family="Fredoka" font-weight="700" font-size="84" fill="#3a3a46" stroke="#cfcfd8" stroke-width="2">R.I.P.</text>'
          f'<text x="{sx}" y="{top + 460}" text-anchor="middle" font-family="Fredoka" font-weight="700" font-size="80" fill="#3a3a46" stroke="#cfcfd8" stroke-width="2">BIG MIKE</text>')
    b += ''.join(f'<ellipse cx="{x}" cy="{y}" rx="{r}" ry="{r * .6:.0f}" fill="#5a7a3a" opacity=".85"/>' for x, y, r in ((sx - hw + 10, 1540, 34), (sx - hw + 50, 1552, 24), (sx + hw - 10, 1546, 30)))
    # grave mound with an old spotted banana + flowers
    b += f'<path d="M{sx - 220} 1620 Q{sx} 1540 {sx + 220} 1620Z" fill="#3a2a22" stroke="#1a1010" stroke-width="5"/>'
    art, _ = banana(((sx - 80, 1592), (sx - 40, 1622), (sx + 70, 1618), (sx + 110, 1578)), 28, ('#8a6a1a', '#c8a03a', '#e8c86a', '#f0d890'), line='#2a1804', lw=4, stem=True, spots=12, rnd=rnd)
    b += art
    for x, c in ((sx - 160, '#f2d27a'), (sx - 130, '#ff8a9a'), (sx + 160, '#f2d27a')):
        b += f'<path d="M{x} 1610 q-4 -30 2 -50" stroke="#4a7a3a" stroke-width="5" fill="none"/>'
        b += ''.join(f'<circle cx="{x + 2 + 10 * math.cos(a):.0f}" cy="{1558 + 10 * math.sin(a):.0f}" r="8" fill="{c}"/>' for a in (0, 1.26, 2.51, 3.77, 5.03)) + f'<circle cx="{x + 2}" cy="1558" r="6" fill="#fff6c0"/>'
    b += spark(880, 1110, 20, '#fff0e0') + spark(330, 1150, 14)
    hat = ('<g transform="translate(6 -88) rotate(-6)"><ellipse cx="0" cy="6" rx="44" ry="9" fill="#1a1a1a" stroke-width="3.4"/>'
           '<path d="M-26 6 Q-28 -34 0 -34 Q28 -34 26 6Z" fill="#2a2a2a" stroke-width="3.4"/><path d="M-26 0 L26 0" stroke="#8a2a3a" stroke-width="6"/></g>')
    flower = ('<path d="M54 -60 q4 -30 -2 -56" stroke="#4a7a3a" stroke-width="3" fill="none"/>'
              + ''.join(f'<circle cx="{52 + 7 * math.cos(a):.1f}" cy="{-120 + 7 * math.sin(a):.1f}" r="6" fill="#ff8a9a" stroke-width="2"/>' for a in (0, 1.26, 2.51, 3.77, 5.03)) + '<circle cx="52" cy="-120" r="4" fill="#fff6c0" stroke="none"/>')
    tear = '<path d="M-12 -50 q-4 8 0 12 q4 -4 0 -12z" fill="#9ae8ff" stroke="none"/>'
    b += '<circle cx="180" cy="1480" r="140" fill="#ffd0a0" opacity=".12" filter="url(#b50)"/>'
    b += frog(185, 1640, 2.4, rot=2, look=(12, -4), mouth='o', shadow=True, top=hat + tear, brows=True,
              armL='M-34 -22 q-18 4 -22 22', armR='M38 -22 q18 -10 16 -40', front=flower)
    b += f'<rect width="{W}" height="{H}" fill="url(#vig2)"/>'
    return vpage('#140f26', vsvg(d, b), [('ALREADY', 128, 'w'), ('EXTINCT', 196, 'y'), ('ONCE', 128, 'w')], outline='#0c0614', top=560)


def v3():
    rnd = random.Random(33)
    d = FILTERS + lin('sky3', [(0, '#050c22'), (.6, '#13285a'), (1, '#1e3a6a')])
    d += rad('glow3', 540, 1230, 640, [(0, '#ffe2a0', .6), (.4, '#f2b04a', .22), (1, '#f2b04a', 0)])
    d += lin('in3', [(0, '#fff2c0'), (1, '#f2b84a')])
    d += lin('lawn3', [(0, '#183a24'), (1, '#06120a')]) + VV('vig3', '#02060e')
    b = f'<rect width="{W}" height="{H}" fill="url(#sky3)"/>'
    b += dust(rnd, 140, 0, 1080, 160, 1000, '#e8f0ff')
    b += '<circle cx="820" cy="340" r="62" fill="#fff6dc" opacity=".95"/><circle cx="820" cy="340" r="120" fill="#fff6dc" opacity=".15" filter="url(#b26)"/>'
    b += f'<rect width="{W}" height="{H}" fill="url(#glow3)"/>'
    b += '<path d="M0 1520 Q540 1490 1080 1525 L1080 1920 L0 1920Z" fill="url(#lawn3)"/>'
    for x, h in ((40, 420), (1050, 480)):
        b += f'<rect x="{x - 14}" y="{1520 - h * .4:.0f}" width="28" height="{h * .4:.0f}" fill="#0a1a12"/>'
        b += ''.join(f'<circle cx="{x + dx}" cy="{1520 - h * .45 - dy:.0f}" r="{r}" fill="#0c2216"/>' for dx, dy, r in ((-60, 60, 90), (50, 70, 100), (0, 160, 110), (-30, 250, 80), (40, 250, 70)))
    # glasshouse (same drawing as the 16:9 version), scaled into the lower half
    gh = ''
    body = 'M1000 860 L1000 560 Q1000 520 1040 520 L1580 520 Q1620 520 1620 560 L1620 860Z'
    dome = 'M1150 520 Q1150 250 1310 220 Q1470 250 1470 520Z'
    gh += '<ellipse cx="1310" cy="620" rx="420" ry="360" fill="#ffe2a0" opacity=".2" filter="url(#b50)"/>'
    gh += f'<path d="{body}" fill="url(#in3)" opacity=".92"/><path d="{dome}" fill="url(#in3)" opacity=".95"/>'
    plant = '<path d="M1290 860 L1296 460 L1326 460 L1332 860Z" fill="#3a6a2a"/>'
    for x, y, L, a in ((1310, 470, 300, -150), (1310, 470, 300, -30), (1310, 450, 260, -105), (1310, 450, 250, -70), (1310, 500, 280, 175), (1310, 500, 280, 5)):
        plant += leaf(x, y, L, a, '#3f8a30', '#24501a', .2)
    for k in range(5):
        bx, by = 1340, 560 + k * 26
        plant += f'<path d="M{bx} {by} q30 -6 50 -40" fill="none" stroke="#c8d43a" stroke-width="18" stroke-linecap="round"/><path d="M{bx} {by} q30 -6 50 -40" fill="none" stroke="#2a3a08" stroke-width="2" opacity=".5"/>'
    plant += '<path d="M1340 540 L1350 700" stroke="#6a5a2a" stroke-width="8"/><ellipse cx="1352" cy="720" rx="16" ry="24" fill="#7a2a4a"/>'
    gh += f'<g opacity=".95">{plant}</g>'
    bars = ''.join(f'<line x1="{x}" y1="520" x2="{x}" y2="860"/>' for x in range(1000, 1621, 62))
    bars += '<line x1="1000" y1="690" x2="1620" y2="690"/><line x1="1000" y1="600" x2="1620" y2="600"/>'
    bars += ''.join(f'<path d="M{1310 + k * 40} 520 Q{1310 + k * 34} 330 1310 222" fill="none"/>' for k in range(-4, 5))
    bars += ''.join(f'<path d="M{1310 - (y - 200) * 1.4:.0f} {y} Q1310 {y - 40} {1310 + (y - 200) * 1.4:.0f} {y}" fill="none"/>' for y in (300, 380, 450))
    gh += f'<g stroke="#f8f0e0" stroke-width="5" opacity=".85">{bars}</g>'
    gh += f'<path d="{body}" fill="none" stroke="#e8e0d0" stroke-width="10"/><path d="{dome}" fill="none" stroke="#e8e0d0" stroke-width="10"/>'
    gh += '<path d="M1310 222 L1310 180" stroke="#e8e0d0" stroke-width="8"/><circle cx="1310" cy="174" r="12" fill="#f2d27a" stroke="#8a6a2a" stroke-width="3"/>'
    gh += '<path d="M1270 860 L1270 760 Q1310 720 1350 760 L1350 860Z" fill="#fff6d0" stroke="#e8e0d0" stroke-width="8"/>'
    gh += '<path d="M1000 860 L1620 860" stroke="#c8bca0" stroke-width="16"/>'
    gh += '<path d="M1270 868 L1350 868 L1460 1000 L1160 1000Z" fill="#ffe2a0" opacity=".22"/>'
    s = .9
    b += f'<g transform="translate(560 {1530 - 686 * s:.0f}) scale({s}) translate(-1310 -174)">{gh}</g>'
    b += spark(900, 1060, 22, '#fffbe0') + spark(250, 1180, 16) + spark(880, 1300, 14)
    hat = ('<g transform="translate(6 -92) rotate(-5)"><ellipse cx="0" cy="8" rx="44" ry="9" fill="#141414" stroke-width="3.4"/>'
           '<rect x="-26" y="-58" width="52" height="66" rx="5" fill="#1e1e22" stroke-width="3.4"/><rect x="-26" y="-6" width="52" height="10" fill="#7a2a3a" stroke-width="2"/>'
           '<path d="M-18 -50 L-18 -14" stroke="#fff" stroke-width="4" opacity=".35"/></g>')
    mono = '<circle cx="22" cy="-66" r="16" fill="none" stroke="#f2d27a" stroke-width="3.4"/><path d="M36 -60 q10 20 2 44" fill="none" stroke="#f2d27a" stroke-width="2"/>'
    bow = '<path d="M-6 -24 L-20 -32 L-20 -16Z M18 -24 L32 -32 L32 -16Z" fill="#7a2a3a" stroke-width="2.6"/><circle cx="6" cy="-24" r="5" fill="#7a2a3a" stroke-width="2.4"/>'
    ban, _ = banana(((-48, -64), (-58, -110), (-90, -140), (-118, -140)), 11, RIPE, line=INK, lw=2.6, stem=True)
    b += '<circle cx="150" cy="1520" r="150" fill="#ffe2a0" opacity=".14" filter="url(#b50)"/>'
    b += frog(150, 1680, 2.4, rot=-2, look=(12, -6), mouth='O', shadow=True, mid=bow, top=mono + hat, brows=True,
              armL='M-34 -22 q-16 -14 -14 -42', armR='M38 -22 q18 4 22 22', back=ban)
    b += f'<rect width="{W}" height="{H}" fill="url(#vig3)"/>'
    return vpage('#050c22', vsvg(d, b), [('SAVED BY', 140, 'w'), ('A DUKE', 210, 'y')], outline='#040818', top=560)


def v4():
    rnd = random.Random(44)
    d = FILTERS + lin('bg4', [(0, '#3a0a26'), (.5, '#7a1a44'), (1, '#2a0618')])
    d += rad('spot4', 540, 1250, 640, [(0, '#ffe8a0', .55), (.4, '#ff9a6a', .18), (1, '#000', 0)])
    d += rad('spot4b', 540, 420, 460, [(0, '#ffd0e0', .35), (1, '#000', 0)])
    d += lin('wood4', [(0, '#c8884a'), (1, '#7a4a22')]) + lin('woodS', [(0, '#8a5a2a'), (1, '#4a2a12')])
    d += lin('floor4', [(0, '#3a0a22'), (1, '#12030a')]) + VV('vig4', '#12030a')
    b = f'<rect width="{W}" height="{H}" fill="url(#bg4)"/>'
    b += ''.join(f'<circle cx="{rnd.uniform(0, 1080):.0f}" cy="{rnd.uniform(150, 1300):.0f}" r="{rnd.uniform(20, 70):.0f}" fill="#ff7aa8" opacity="{rnd.uniform(.04, .12):.2f}"/>' for _ in range(22))
    b += f'<rect width="{W}" height="{H}" fill="url(#spot4)"/><rect width="{W}" height="{H}" fill="url(#spot4b)"/>'
    b += '<path d="M0 1540 L1080 1520 L1080 1920 L0 1920Z" fill="url(#floor4)"/>'
    # strawberry + raspberry flung up out of the crate (above the text)
    for x0, y0, x1, y1 in ((330, 520, 390, 640), (360, 560, 430, 680), (760, 500, 700, 620), (720, 540, 660, 660)):
        b += f'<path d="M{x0} {y0} L{x1} {y1}" stroke="#ffd0d8" stroke-width="6" stroke-linecap="round" opacity=".55"/>'
    b += '<circle cx="290" cy="410" r="130" fill="#ff7a8a" opacity=".2" filter="url(#b26)"/>' + strawberry(290, 410, 1.7, -28)
    b += '<circle cx="800" cy="400" r="110" fill="#ff7aaa" opacity=".2" filter="url(#b26)"/>' + raspberry(800, 400, 1.5, 24)
    b += spark(560, 330, 20, '#fffbe0') + spark(960, 560, 14) + spark(120, 600, 14, '#ffe9ff')
    # crate below the text, banana lying in it
    cx0, cx1, ct, cb = 170, 910, 1290, 1530
    b += f'<ellipse cx="540" cy="{cb}" rx="420" ry="40" fill="#000" opacity=".55" filter="url(#b14)"/>'
    b += f'<path d="M{cx0} {ct} L{cx0 + 60} {ct - 80} L{cx1 - 60} {ct - 80} L{cx1} {ct}Z" fill="url(#woodS)" stroke="#2a1606" stroke-width="7" stroke-linejoin="round"/>'
    art, _ = banana(((130, 1140), (300, 1330), (760, 1330), (960, 1080)), 120, RIPE, line='#3a1c04', lw=7, stem=True, spots=8, rnd=rnd, glow='#ffd84a')
    b += art
    face = f'<path d="M{cx0} {ct} L{cx1} {ct} L{cx1 - 20} {cb} L{cx0 + 20} {cb}Z" fill="url(#wood4)" stroke="#2a1606" stroke-width="8" stroke-linejoin="round"/>'
    for y in (1350, 1410, 1470):
        face += f'<path d="M{cx0 + 8} {y} L{cx1 - 8} {y}" stroke="#5a3214" stroke-width="5" opacity=".7"/>'
    face += f'<path d="M{cx0 + 20} {ct + 10} L{cx1 - 20} {ct + 10}" stroke="#f0c088" stroke-width="6" opacity=".6"/>'
    face += '<rect x="360" y="1350" width="360" height="110" rx="14" fill="#f8ecd0" stroke="#2a1606" stroke-width="6"/>'
    face += '<text x="540" y="1432" text-anchor="middle" font-family="Fredoka" font-weight="700" font-size="76" fill="#8a1a3a">BERRIES</text>'
    for x, y in ((cx0 + 22, ct + 22), (cx1 - 22, ct + 22), (cx0 + 34, cb - 22), (cx1 - 34, cb - 22)):
        face += f'<circle cx="{x}" cy="{y}" r="7" fill="#3a2a1a"/>'
    b += face
    b += '<g transform="translate(560 1200)"><path d="M-22 10 L-34 70 L-10 56 L0 80 L10 20Z M22 10 L34 70 L10 56 L0 80 L-10 20Z" fill="#c03a4a" stroke="#3a0810" stroke-width="4"/>'
    b += ''.join(f'<circle cx="{34 * math.cos(a * math.pi / 6):.0f}" cy="{34 * math.sin(a * math.pi / 6):.0f}" r="14" fill="#f2d27a" stroke="#8a6a1a" stroke-width="3"/>' for a in range(12))
    b += '<circle r="32" fill="#f2d27a" stroke="#8a6a1a" stroke-width="4"/><path d="M-14 -4 L-4 8 L16 -12" fill="none" stroke="#8a1a3a" stroke-width="7" stroke-linecap="round"/></g>'
    b += spark(980, 1150, 22, '#fffbe0') + spark(150, 1250, 14)
    glass = ('<g transform="translate(56 -150) rotate(-35)"><rect x="-6" y="30" width="12" height="54" rx="5" fill="#7a4a22" stroke-width="3"/>'
             '<circle r="32" fill="#cfefff" fill-opacity=".35" stroke="#c8a040" stroke-width="7"/><path d="M-16 -14 q8 -10 20 -10" stroke="#fff" stroke-width="4" fill="none"/></g>')
    cap = ('<g transform="translate(6 -90) rotate(-8)"><path d="M-36 6 Q-34 -30 0 -32 Q34 -30 36 6Z" fill="#a07a4a" stroke-width="3.4"/>'
           '<path d="M-36 6 L-58 10 L-36 -2Z M36 6 L58 10 L36 -2Z" fill="#8a6a3a" stroke-width="3"/><path d="M-30 -8 L30 -8 M-26 -20 L26 -20" stroke="#6a4a2a" stroke-width="2.4"/></g>')
    b += '<circle cx="900" cy="1500" r="140" fill="#ffe8a0" opacity=".12" filter="url(#b50)"/>'
    b += frog(950, 1700, 2.2, rot=-3, flip=True, look=(11, -6), mouth='O', shadow=True, top=cap, brows=True,
              armL='M-34 -22 q-18 4 -22 22', armR='M38 -22 q22 -14 26 -40', front=glass)
    b += f'<rect width="{W}" height="{H}" fill="url(#vig4)"/>'
    return vpage('#3a0a26', vsvg(d, b), [('A BANANA', 124, 'w'), ('IS A', 110, 'w'), ('BERRY', 220, 'y')], outline='#1a0410', top=610)


def v5():
    rnd = random.Random(55)
    G = 1120  # ground line
    d = FILTERS + lin('sky5', [(0, '#1e4a52'), (.4, '#5a9a7a'), (.58, '#e8e0a0'), (1, '#e8e0a0')])
    d += rad('sun5', 820, 820, 520, [(0, '#fff6c0', .8), (.3, '#f2d27a', .3), (1, '#f2d27a', 0)])
    d += lin('soil5', [(0, '#5a3a20'), (.5, '#3a2412'), (1, '#1a0e06')])
    d += rad('corm5', 520, 1310, 300, [(0, '#f0e0b0', 1), (.6, '#c8a870', 1), (1, '#8a6a3a', 1)])
    d += lin('stem5', [(0, '#6a9a3a'), (.5, '#a8c860'), (1, '#4a7a2a')], x2=1, y2=0) + VV('vig5', '#0a0604', .75)
    b = f'<rect width="{W}" height="{H}" fill="url(#sky5)"/><rect width="{W}" height="{H}" fill="url(#sun5)"/>'
    b += f'<path d="M0 {G - 30} Q200 {G - 90} 420 {G - 50} Q700 {G - 110} 1080 {G - 50} L1080 {G + 20} L0 {G + 20}Z" fill="#3a6a4a" opacity=".6"/>'
    b += f'<path d="M0 {G} Q540 {G - 20} 1080 {G + 5} L1080 1920 L0 1920Z" fill="url(#soil5)"/>'
    b += f'<path d="M0 {G} Q540 {G - 20} 1080 {G + 5}" fill="none" stroke="#4a8a3a" stroke-width="18"/>'
    b += ''.join(f'<ellipse cx="{rnd.uniform(0, 1080):.0f}" cy="{rnd.uniform(G + 40, 1880):.0f}" rx="{rnd.uniform(6, 16):.0f}" ry="{rnd.uniform(4, 9):.0f}" fill="#7a5a3a" opacity="{rnd.uniform(.3, .7):.2f}"/>' for _ in range(80))
    cx, cy = 560, 1310
    for _ in range(16):
        a = rnd.uniform(.25, 2.9); L = rnd.uniform(140, 240)
        x0, y0 = cx + math.cos(a) * 220, cy + math.sin(a) * 80
        b += f'<path d="M{x0:.0f} {y0:.0f} q{math.cos(a) * L * .5:.0f} {L * .4:.0f} {math.cos(a) * L:.0f} {L * .6:.0f}" fill="none" stroke="#c8a870" stroke-width="5" opacity=".7"/>'
    b += f'<ellipse cx="{cx}" cy="{cy + 10}" rx="270" ry="130" fill="#000" opacity=".35" filter="url(#b14)"/>'
    b += f'<path d="M{cx - 250} {cy} Q{cx - 250} {cy - 110} {cx} {cy - 120} Q{cx + 250} {cy - 110} {cx + 250} {cy} Q{cx + 240} {cy + 110} {cx} {cy + 125} Q{cx - 240} {cy + 110} {cx - 250} {cy}Z" fill="url(#corm5)" stroke="#3a2410" stroke-width="9"/>'
    b += ''.join(f'<path d="M{cx - 200 + k * 60} {cy - 60 + (k % 2) * 30} q30 20 60 0" fill="none" stroke="#8a6a3a" stroke-width="4" opacity=".7"/>' for k in range(7))
    b += f'<path d="M{cx - 200} {cy - 40} Q{cx - 120} {cy - 95} {cx - 20} {cy - 100}" fill="none" stroke="#fff6dc" stroke-width="10" opacity=".55" stroke-linecap="round"/>'
    b += f'<circle cx="{cx}" cy="{cy}" r="280" fill="#fff0b0" opacity=".1" filter="url(#b50)"/>'
    # pups from the corm sides, poking above ground
    for x, s in ((130, .75), (960, .7)):
        path = f'M{cx + (x - cx) * .5:.0f} {cy} Q{x} {cy - 20} {x} {G - 60}'
        b += f'<path d="{path}" fill="none" stroke="#3a2410" stroke-width="30" stroke-linecap="round"/><path d="{path}" fill="none" stroke="#b8c870" stroke-width="20" stroke-linecap="round"/>'
        b += leaf(x, G - 60, 160 * s, -125, '#5aa040', '#2a5a18', .24) + leaf(x, G - 60, 150 * s, -55, '#4a9038', '#2a5a18', .24) + leaf(x, G - 60, 120 * s, -92, '#6ab048', '#2a5a18', .24)
    # pseudostem (no wood): lower part behind the text, cut gap, upper part with crown
    b += f'<path d="M{cx - 60} {cy - 110} L{cx - 50} 560 L{cx + 50} 560 L{cx + 60} {cy - 110}Z" fill="url(#stem5)" stroke="#2a3a14" stroke-width="8" stroke-linejoin="round"/>'
    for k in range(4):
        b += f'<path d="M{cx - 44 + k * 26} {cy - 120} Q{cx - 50 + k * 26} 800 {cx - 38 + k * 24} 570" fill="none" stroke="#3a5a1a" stroke-width="3" opacity=".5"/>'
    b += f'<ellipse cx="{cx}" cy="560" rx="50" ry="12" fill="#e8f0b0" stroke="#2a3a14" stroke-width="5"/>'
    b += f'<path d="M{cx - 46} 480 L{cx - 36} 300 L{cx + 36} 300 L{cx + 46} 480Z" fill="url(#stem5)" stroke="#2a3a14" stroke-width="8" stroke-linejoin="round"/>'
    for x, y, L, a in ((cx, 310, 360, -165), (cx, 310, 360, -15), (cx, 290, 250, -120), (cx, 290, 250, -60), (cx, 330, 320, 172), (cx, 330, 330, 8)):
        b += leaf(x, y, L, a, '#4a9a3a', '#24501a', .2)
    for k in range(4):
        b += f'<path d="M{cx + 40} {360 + k * 28} q40 -4 64 -44" fill="none" stroke="#c8d43a" stroke-width="22" stroke-linecap="round"/><path d="M{cx + 40} {360 + k * 28} q40 -4 64 -44" fill="none" stroke="#3a4a08" stroke-width="2.4" opacity=".5"/>'
    # floating slice with concentric leaf sheaths, beside the cut
    sl = '<g transform="translate(860 560) rotate(-10) scale(.95)">'
    sl += '<ellipse cx="10" cy="30" rx="150" ry="70" fill="#4a7a2a" stroke="#2a3a14" stroke-width="8"/><rect x="-140" y="0" width="300" height="30" fill="#4a7a2a"/>'
    sl += '<ellipse cx="10" cy="0" rx="150" ry="70" fill="#7aaa48" stroke="#2a3a14" stroke-width="8"/>'
    for k, r in enumerate((128, 106, 84, 62, 40, 20)):
        sl += f'<ellipse cx="{10 + k * 2}" cy="0" rx="{r}" ry="{r * .46:.0f}" fill="{["#a8d070", "#c8e090", "#dceca8", "#e8f2c0", "#f0f6d0", "#fafbe8"][k]}" stroke="#4a6a2a" stroke-width="4"/>'
    sl += '<path d="M-110 -30 Q-40 -66 60 -60" fill="none" stroke="#fff" stroke-width="7" opacity=".55" stroke-linecap="round"/></g>'
    b += '<circle cx="860" cy="560" r="190" fill="#fff6c0" opacity=".3" filter="url(#b50)"/>' + sl
    b += f'<path d="M{cx + 70} 520 Q{cx + 130} 470 {cx + 150} 500" fill="none" stroke="#fffbe6" stroke-width="6" stroke-dasharray="14 12" stroke-linecap="round"/>'
    b += spark(960, 380, 24, '#fffbe0') + spark(230, 420, 16) + spark(800, 1260, 18, '#fff6dc')
    helm = ('<g transform="translate(6 -90) rotate(-6)"><path d="M-40 8 Q-40 -36 0 -38 Q40 -36 40 8Z" fill="#f2c21a" stroke-width="3.4"/>'
            '<path d="M-46 8 L46 8" stroke-width="7" stroke="#d8a810"/><rect x="-12" y="-28" width="24" height="18" rx="5" fill="#fffbe0" stroke-width="3"/></g>')
    fx, fy, fs = 860, 1690, 2.3
    b += f'<path d="M{fx - 30} {fy - 330} L{cx + 140} {cy + 30} L{cx + 230} {cy + 110} L{fx - 10} {fy - 300}Z" fill="#fff6c0" opacity=".2"/>'
    b += f'<circle cx="{fx}" cy="{fy - 150}" r="140" fill="#fff0b0" opacity=".12" filter="url(#b50)"/>'
    b += frog(fx, fy, fs, rot=-4, flip=True, look=(12, -6), mouth='O', shadow=True, top=helm, brows=True,
              armL='M-34 -22 q-18 4 -22 22', armR='M38 -22 q22 -8 30 -30')
    b += f'<rect width="{W}" height="{H}" fill="url(#vig5)"/>'
    return vpage('#1e4a52', vsvg(d, b), [('NOT A', 170, 'w'), ('TREE!', 270, 'y')], outline='#081410', top=640)


for n, fn in enumerate((v1, v2, v3, v4, v5), 1):
    out = os.path.join(VID, f'seedless-banana-short{n}', 'thumb'); os.makedirs(out, exist_ok=True)
    for f in ('common.css', 'Fredoka-700.woff2'):
        shutil.copy(os.path.join(TOOLS, 'assets', 'thumb_v', f), out)
    open(os.path.join(out, 'A.html'), 'w').write(fn())
print('ok')
