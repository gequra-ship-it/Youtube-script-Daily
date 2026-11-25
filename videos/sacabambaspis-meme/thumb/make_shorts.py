# Shorts thumbnails (guideline 16-9, style B) for sacabambaspis-meme-short1..5. Run: python3 videos/sacabambaspis-meme/thumb/make_shorts.py
# writes videos/sacabambaspis-meme-shortN/thumb/A.html (+ common.css, Fredoka-700.woff2 from tools/assets/thumb_v)
# 1 HELSINKI'S FAMOUS FACE  museum case under a spotlight (short1 S01-S02: the model in the Finnish Museum of Natural History, Helsinki)
# 2 NO SIDE FINS            top view: smooth armoured sides, power only from the tail (short2 S01/S03 "no side fins", "no paired fins")
# 3 ARMOR LIKE A SANDWICH   cut block of the armour: thin base, spongy middle, hard ridged top (short3 S03)
# 4 BURIED FAST             mud surge rolling over a group of fish and brachiopods (short4 S03-S04 "Sudden burial is the key"; flood/mud = "probably")
# 5 THEN CAME THE ICE       glacier over a shrinking shallow sea, a small fish in the last pool (short5 S01/S03)
import os, sys, math, random, shutil
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '../../..'))
sys.path.insert(0, HERE); sys.path.insert(0, REPO + '/tools')
from thumb_lib import vpage, vsvg, lin, rad, spark, fireflies, halo, darkband
from saca_lib import *
W, H = 1080, 1920
VIG = rad('vig', 540, 960, 1250, [(0, '#000', 0), (.55, '#000', 0), (1, '#000', .72)])


def saca_top(x, y, s, rot=0, sway=1.0, P=None, glow=None):
    """top view (head up): oval dorsal shield, both eyes on the front edge, smooth sides (no paired fins), S-curving scaly tail + fin"""
    P = P or PAL['glow']
    gid = uid('tg'); cid = uid('tc'); bid = uid('tb')
    o = f'<g transform="translate({x} {y}) rotate({rot}) scale({s})">'
    N = 36; L = []; R = []
    for i in range(N + 1):
        t = i / N; cx = 70 * sway * math.sin(t * math.pi * 1.2) * t; cy = 150 + 470 * t; w = 120 * (1 - t) ** .85 + 10
        L.append((cx - w, cy)); R.append((cx + w, cy))
    body = 'M' + ' L'.join(f'{a:.1f},{b:.1f}' for a, b in L) + ' L' + ' L'.join(f'{a:.1f},{b:.1f}' for a, b in reversed(R)) + 'Z'
    tx, ty = 70 * sway * math.sin(math.pi * 1.2), 620
    o += f'<defs><radialGradient id="{gid}" cx=".4" cy=".35" r=".75"><stop offset="0" stop-color="{P["hi"]}"/><stop offset=".6" stop-color="{P["mid"]}"/><stop offset="1" stop-color="{P["lo"]}"/></radialGradient>'
    o += f'<linearGradient id="{bid}" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{P["tail_lo"]}"/><stop offset=".45" stop-color="{P["tail"]}"/><stop offset="1" stop-color="{P["tail_lo"]}"/></linearGradient><clipPath id="{cid}"><path d="{body}"/></clipPath></defs>'
    if glow:
        o += f'<ellipse cx="0" cy="180" rx="330" ry="470" fill="{glow}" opacity=".45" filter="url(#b50)"/>'
    o += (f'<path d="M{tx:.0f},{ty - 20:.0f} C{tx - 40:.0f},{ty + 40:.0f} {tx - 110:.0f},{ty + 90:.0f} {tx - 130:.0f},{ty + 150:.0f} C{tx - 60:.0f},{ty + 120:.0f} {tx - 20:.0f},{ty + 110:.0f} {tx:.0f},{ty + 80:.0f} '
          f'C{tx + 20:.0f},{ty + 110:.0f} {tx + 60:.0f},{ty + 120:.0f} {tx + 130:.0f},{ty + 150:.0f} C{tx + 110:.0f},{ty + 90:.0f} {tx + 40:.0f},{ty + 40:.0f} {tx:.0f},{ty - 20:.0f}Z" fill="{P["fin"]}" stroke="{P["edge"]}" stroke-width="5"/>')
    o += ''.join(f'<path d="M{tx:.0f},{ty:.0f} l{-110 + k * 44},{130 - abs(k - 2.5) * 14:.0f}" stroke="{P["tail_lo"]}" stroke-width="2.4" opacity=".6"/>' for k in range(6))
    o += f'<path d="{body}" fill="url(#{bid})" stroke="{P["edge"]}" stroke-width="5.5"/>'
    sc = ''
    for i in range(1, 30):
        t = i / 30; cx = 70 * sway * math.sin(t * math.pi * 1.2) * t; cy = 150 + 470 * t; w = 120 * (1 - t) ** .85 + 10
        for j in range(-4, 5):
            sc += f'M{cx + j * w / 4.5 - 9:.0f},{cy - 6:.0f} q9 10 18 0 '
    o += f'<g clip-path="url(#{cid})"><path d="{sc}" fill="none" stroke="{P["tail_lo"]}" stroke-width="2.2" opacity=".7"/></g>'
    shield = 'M0,-190 C110,-190 172,-110 172,10 C172,130 110,200 0,210 C-110,200 -172,130 -172,10 C-172,-110 -110,-190 0,-190Z'
    hid = uid('hs')
    o += f'<path d="{shield}" fill="url(#{gid})" stroke="{P["edge"]}" stroke-width="6"/>'
    random.seed(4)
    o += f'<defs><clipPath id="{hid}"><path d="{shield}"/></clipPath></defs><g clip-path="url(#{hid})">'
    o += f'<g fill="{P["tub"]}" opacity=".5">' + ''.join(f'<circle cx="{random.uniform(-170, 170):.0f}" cy="{random.uniform(-190, 210):.0f}" r="{random.choice([2, 2.6, 3.2])}"/>' for _ in range(170)) + '</g>'
    o += f'<path d="M-120,-80 C-60,-60 60,-60 120,-80 M-140,20 C-60,40 60,40 140,20 M-110,120 C-50,136 50,136 110,120 M0,-150 L0,190" fill="none" stroke="{P["groove"]}" stroke-width="3" opacity=".5" stroke-dasharray="12 6"/>'
    o += f'<path d="M-130,-110 C-90,-170 -20,-184 30,-180" fill="none" stroke="#fff" stroke-width="16" opacity=".3"/></g>'
    o += f'<path d="M-150,-90 C-110,-176 -30,-192 20,-190" fill="none" stroke="{P["rim"]}" stroke-width="5" opacity=".9"/>'
    for ex in (-58, 58):   # eyes on the very front edge
        o += f'<circle cx="{ex}" cy="-176" r="34" fill="{P["lo"]}" stroke="{P["edge"]}" stroke-width="4"/>'
        o += f'<circle cx="{ex}" cy="-180" r="27" fill="#f8f6ea" stroke="{P["edge"]}" stroke-width="4"/><circle cx="{ex}" cy="-190" r="12" fill="#141414"/><circle cx="{ex - 4}" cy="-195" r="4" fill="#fff"/>'
    return o + '</g>'


def write(n, defs, body, lines, bg, outline='#04101a', top=860):
    d = f'{REPO}/videos/sacabambaspis-meme-short{n}/thumb'; os.makedirs(d, exist_ok=True)
    for f in ('common.css', 'Fredoka-700.woff2'):
        shutil.copy(f'{REPO}/tools/assets/thumb_v/{f}', d)
    open(f'{d}/A.html', 'w').write(vpage(bg, vsvg(defs, body), lines, outline=outline, top=top))
    print('short', n, 'ok')


# ---------------- 1: museum case ----------------
def short1():
    random.seed(1)
    defs = FILTERS + VIG + lin('wall1', [(0, '#0a0c18'), (1, '#1c1a2e')]) + halo('h1', 540, 520, 520)
    defs += lin('cone', [(0, '#fff6d0'), (1, '#fff6d0')])
    defs += lin('ped', [(0, '#3a3650'), (.5, '#5a5674'), (1, '#2a2840')], x2=1, y2=0)
    b = f'<rect width="{W}" height="{H}" fill="url(#wall1)"/>'
    b += '<rect y="1240" width="1080" height="680" fill="#141220"/><path d="M0,1240 L1080,1240" stroke="#3a3650" stroke-width="4"/>'
    for k in range(-6, 8):
        b += f'<path d="M540,1240 L{540 + k * 260},{1940}" stroke="#2a2840" stroke-width="3"/>'
    # spotlight cone
    b += '<path d="M470,-20 L610,-20 L860,860 L220,860Z" fill="#fff6d0" opacity=".10"/>'
    b += '<path d="M500,-20 L580,-20 L760,860 L320,860Z" fill="#fff6d0" opacity=".08"/>'
    b += '<rect x="480" y="-20" width="120" height="40" rx="8" fill="#2a2a34" stroke="#0a0a10" stroke-width="4"/>'
    b += '<ellipse cx="540" cy="520" rx="520" ry="470" fill="url(#h1)"/>'
    b += fireflies(26, 120, 840, col='#fff3c8', core='#fffbe6', seed=3)
    # glass case + fish model
    b += saca_front(540, 430, .74, mouth='O', look=(0, 3), sway=35, length=300, P=PAL['live'])
    b += '<rect x="290" y="210" width="500" height="640" rx="10" fill="#cfefff" opacity=".08" stroke="#e6f8ff" stroke-width="6" stroke-opacity=".7"/>'
    b += '<path d="M320,240 L420,240 L320,420Z" fill="#fff" opacity=".18"/><path d="M760,600 L760,820 L690,820Z" fill="#fff" opacity=".1"/>'
    b += '<rect x="260" y="845" width="560" height="30" rx="6" fill="url(#ped)" stroke="#0a0a10" stroke-width="4"/>'
    for sx, sy, ss in ((230, 300, 30), (850, 420, 26), (820, 230, 18), (250, 640, 18)):
        b += spark(sx, sy, ss, col='#fffbe0')
    b += darkband(860, 1240, .45)
    # floor: pedestal reflection + frog visitor with a camera (flash)
    b += '<ellipse cx="540" cy="1300" rx="380" ry="40" fill="#fff6d0" opacity=".12" filter="url(#b24)"/>'
    cam = ('<g transform="translate(64 -82)"><rect x="-22" y="-16" width="44" height="30" rx="6" fill="#2a2a34" stroke-width="3"/><circle cx="0" cy="-1" r="9" fill="#5a6a8a" stroke-width="2.6"/>'
           '<rect x="8" y="-22" width="10" height="6" rx="2" fill="#fff8d0" stroke-width="2"/></g>')
    b += '<circle cx="980" cy="1440" r="70" fill="#fffbe6" opacity=".55" filter="url(#b24)"/>' if False else ''
    b += '<ellipse cx="760" cy="1772" rx="190" ry="26" fill="#000" opacity=".5" filter="url(#b12)"/>'
    b += frog(760, 1760, 3.2, mouth='o', arms=('q-14 6 -16 22', 'q20 -14 26 -60'), look=(-4, -4), front=cam, flip=True)
    fx, fy = 760 - 64 * 3.2 + 14, 1760 - 104 * 3.2
    b += f'<circle cx="{fx:.0f}" cy="{fy:.0f}" r="60" fill="#fffbe6" opacity=".6" filter="url(#b24)"/>' + spark(int(fx), int(fy), 40, col='#ffffff')
    b += f'<rect width="{W}" height="{H}" fill="url(#vig)"/>'
    write(1, defs, b, [("HELSINKI'S", 128, 'w'), ('FAMOUS', 196, 'y'), ('FACE', 128, 'w')], '#0a0c18', top=872)


# ---------------- 2: no side fins (top view) ----------------
def short2():
    random.seed(2)
    defs = FILTERS + VIG + lin('sea2', [(0, '#0a3a4a'), (.5, '#06202e'), (1, '#030c14')]) + halo('h2', 540, 470, 560)
    b = f'<rect width="{W}" height="{H}" fill="url(#sea2)"/>'
    for x0 in (120, 380, 640, 880):
        b += f'<path d="M{x0},-20 L{x0 + 90},-20 L{x0 - 100},1300 L{x0 - 220},1300Z" fill="#bff6ee" opacity=".05"/>'
    b += '<ellipse cx="540" cy="470" rx="560" ry="560" fill="url(#h2)"/>'
    b += fireflies(50, 120, 1850, col='#9ff0e0', core='#e8fff8', seed=5)
    # water swirls from the tail beat
    for k in range(4):
        b += f'<path d="M{430 - k * 30},{860 + k * 40} q110 -40 220 0" fill="none" stroke="#dff6ff" stroke-width="5" opacity="{.6 - k * .12:.2f}"/>'
    b += saca_top(540, 262, .78, rot=0, sway=1.0, glow='#fff3a8')
    # smooth sides: soft cyan sheen along the flanks where paired fins would be
    for sx, sy, ss in ((260, 260, 30), (830, 300, 28), (250, 520, 18), (850, 600, 20), (540, 90, 16)):
        b += spark(sx, sy, ss, col='#fffbe0')
    b += darkband(860, 1240, .45)
    # sea floor + frog diver bottom-left
    b += '<path d="M0,1640 C200,1600 420,1630 620,1610 C820,1590 960,1620 1080,1600 L1080,1920 L0,1920Z" fill="#0c2a30"/>'
    for x, y, s in ((560, 1680, 1.3), (700, 1720, 1.0), (900, 1660, 1.2)):
        b += brachiopod(x, y, s, col='#c8b48a', dark='#2a2418')
    b += frog(270, 1740, 3.2, mouth='O', arms=('q-30 -6 -48 -30', 'q14 6 16 22'), look=(4, -5), back=air_tank(), front=diving_helmet())
    b += bubbles(290, 1420, 6, s=1.2)
    b += f'<rect width="{W}" height="{H}" fill="url(#vig)"/>'
    write(2, defs, b, [('NO SIDE', 180, 'w'), ('FINS', 270, 'y')], '#06202e', top=860)


# ---------------- 3: layered armour block ----------------
def short3():
    random.seed(3)
    defs = FILTERS + VIG + lin('bg3', [(0, '#0c1420'), (1, '#1a1020')]) + halo('h3', 540, 520, 560, inner='#fff3c8', outer='#f2a860')
    b = f'<rect width="{W}" height="{H}" fill="url(#bg3)"/>'
    b += '<ellipse cx="540" cy="520" rx="580" ry="520" fill="url(#h3)"/>'
    b += fireflies(40, 100, 1850, col='#ffd9a0', core='#fff4e0', seed=8)
    # block: top face parallelogram, front face with 3 layers, right face
    X0, Y0, BW, D = 190, 430, 620, 150   # front-top-left corner, width, depth offset
    t_base, t_mid, t_top = 50, 150, 90
    yA = Y0; yB = Y0 + t_top; yC = yB + t_mid; yD = yC + t_base
    dx, dy = 130, -D
    # right side face
    b += f'<path d="M{X0 + BW},{yA} L{X0 + BW + dx},{yA + dy} L{X0 + BW + dx},{yD + dy} L{X0 + BW},{yD}Z" fill="#5a3a24" stroke="#1a0c06" stroke-width="5"/>'
    for yy, c in ((yB, '#3a2414'), (yC, '#3a2414')):
        b += f'<path d="M{X0 + BW},{yy} L{X0 + BW + dx},{yy + dy}" stroke="{c}" stroke-width="4"/>'
    # top face (hard ridged layer surface)
    top = f'M{X0},{yA} L{X0 + dx},{yA + dy} L{X0 + BW + dx},{yA + dy} L{X0 + BW},{yA}Z'
    b += f'<path d="{top}" fill="#e8c890" stroke="#1a0c06" stroke-width="5"/>'
    defs += f'<clipPath id="top3"><path d="{top}"/></clipPath>'
    rid = '<g clip-path="url(#top3)">'
    for k in range(14):
        sx = X0 - 40 + k * 52
        rid += f'<path d="M{sx},{yA} l{dx},{dy}" stroke="#a87a48" stroke-width="12" stroke-linecap="round"/><path d="M{sx - 4},{yA} l{dx},{dy}" stroke="#fff0c8" stroke-width="4" opacity=".8"/>'
    rid += ''.join(f'<circle cx="{random.randint(X0, X0 + BW + dx)}" cy="{random.randint(yA + dy, yA)}" r="{random.choice([3, 4, 5])}" fill="#fff4d8" opacity=".7"/>' for _ in range(60))
    rid += '</g>'
    b += rid
    # front face layers
    b += f'<rect x="{X0}" y="{yA}" width="{BW}" height="{t_top}" fill="#d9a868" stroke="#1a0c06" stroke-width="5"/>'
    b += ''.join(f'<path d="M{X0 + k * 40},{yA} q20 -16 40 0" fill="#e8c890" stroke="#1a0c06" stroke-width="3"/>' for k in range(BW // 40))
    b += ''.join(f'<path d="M{X0 + 10 + k * 30},{yA + 20} l0,{t_top - 30}" stroke="#a87a48" stroke-width="3" opacity=".6"/>' for k in range(BW // 30))
    b += f'<rect x="{X0}" y="{yB}" width="{BW}" height="{t_mid}" fill="#c48a52" stroke="#1a0c06" stroke-width="5"/>'
    defs += f'<clipPath id="mid3"><rect x="{X0}" y="{yB}" width="{BW}" height="{t_mid}"/></clipPath>'
    sp = '<g clip-path="url(#mid3)">'
    for _ in range(70):
        cx, cy = random.randint(X0, X0 + BW), random.randint(yB + 6, yC - 6); r = random.randint(7, 20)
        sp += f'<ellipse cx="{cx}" cy="{cy}" rx="{r}" ry="{r * .75:.0f}" fill="#5a3218" stroke="#3a1e0c" stroke-width="2"/><ellipse cx="{cx - r * .2:.0f}" cy="{cy + r * .3:.0f}" rx="{r * .6:.0f}" ry="{r * .3:.0f}" fill="#8a5a30" opacity=".6"/>'
    sp += '</g>'
    b += sp
    b += f'<rect x="{X0}" y="{yC}" width="{BW}" height="{t_base}" fill="#8a5a36" stroke="#1a0c06" stroke-width="5"/>'
    b += ''.join(f'<path d="M{X0},{yC + 12 + k * 12} L{X0 + BW},{yC + 12 + k * 12}" stroke="#5a3a20" stroke-width="3" opacity=".7"/>' for k in range(3))
    b += f'<path d="M{X0},{yA} L{X0 + dx},{yA + dy} L{X0 + BW + dx},{yA + dy}" fill="none" stroke="#fff4d0" stroke-width="5" opacity=".85"/>'
    b += f'<path d="M{X0 + BW},{yA} L{X0 + BW},{yD}" stroke="#ffd9a0" stroke-width="4" opacity=".6"/>'
    # small fish above the block (whose armour this is)
    b += saca(300, 210, .52, flip=False, rot=-4, pal='glow', mouth='O', look=(3, 0), bend=-12, glow='#fff3a8', shadow=False)
    for sx, sy, ss in ((150, 380, 24), (930, 360, 26), (900, 720, 18), (160, 740, 20)):
        b += spark(sx, sy, ss, col='#fffbe0')
    b += darkband(860, 1260, .45)
    # frog with a magnifying glass, bottom right
    mag = ('<g transform="translate(66 -60)"><path d="M0,0 L22,40" stroke-width="9"/><path d="M0,0 L22,40" stroke="#8a5a2e" stroke-width="5"/>'
           '<circle cx="-14" cy="-26" r="26" fill="#cfefff" fill-opacity=".3" stroke="#c48d38" stroke-width="6"/><path d="M-28,-36 q8 -10 20 -8" stroke="#fff" stroke-width="3" fill="none"/></g>')
    b += '<ellipse cx="800" cy="1772" rx="180" ry="24" fill="#000" opacity=".5" filter="url(#b12)"/>'
    b += frog(800, 1760, 3.2, mouth='o', arms=('q-14 6 -16 22', 'q22 -4 30 -38'), look=(-4, -5), front=mag, flip=True)
    b += f'<rect width="{W}" height="{H}" fill="url(#vig)"/>'
    write(3, defs, b, [('ARMOR', 170, 'w'), ('LIKE A', 110, 'w'), ('SANDWICH', 150, 'y')], '#0c1420', top=858)


# ---------------- 4: mud surge ----------------
def short4():
    random.seed(4)
    defs = FILTERS + VIG + lin('sea4', [(0, '#123a44'), (.6, '#0a1e26'), (1, '#05100e')]) + halo('h4', 470, 640, 470)
    defs += rad('mud', 820, 200, 760, [(0, '#8a5a34', 1), (.6, '#5a3a22', .95), (1, '#3a2414', 0)])
    b = f'<rect width="{W}" height="{H}" fill="url(#sea4)"/>'
    b += '<path d="M0,40 C200,60 400,30 600,50 C800,70 950,40 1080,60 L1080,0 L0,0Z" fill="#bff6ee" opacity=".2"/>'
    b += '<ellipse cx="470" cy="640" rx="470" ry="380" fill="url(#h4)"/>'
    # rolling mud cloud from the upper right
    for cx, cy, r, c in ((1000, 160, 300, '#4a2e1a'), (860, 80, 220, '#5a3a22'), (1060, 420, 240, '#4a2e1a'), (760, 260, 180, '#6a4428'), (920, 560, 200, '#5a3a22'), (1040, 700, 170, '#4a2e1a'), (640, 120, 150, '#6a4428')):
        b += f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{c}"/>'
        b += f'<path d="M{cx - r * .8:.0f},{cy - r * .2:.0f} A{r} {r} 0 0 1 {cx + r * .2:.0f},{cy - r * .95:.0f}" fill="none" stroke="#c89a6a" stroke-width="10" opacity=".55"/>'
    for _ in range(90):
        b += f'<circle cx="{random.randint(560, 1080)}" cy="{random.randint(0, 840)}" r="{random.randint(3, 9)}" fill="#a87a4a" opacity="{random.uniform(.3, .8):.2f}"/>'
    b += '<circle cx="900" cy="400" r="380" fill="#3a2414" opacity=".25" filter="url(#b50)"/>'
    # fish group, glowing, swimming away left
    for fx, fy, fs, fr, lk in ((130, 560, .58, -8, (3, -3)), (300, 700, .62, 6, (3, -2)), (110, 790, .5, 10, (2, 0)), (380, 470, .46, -14, (3, -3)), (440, 820, .44, 4, (2, -2))):
        b += saca(fx, fy, fs, flip=False, rot=fr, pal='glow', mouth='O', look=lk, bend=-14, glow='#fff3a8', shadow=False)
    for x, y, s, r in ((150, 840, .9, -6), (260, 850, .8, 10), (520, 846, .85, 4), (640, 852, .7, -10)):
        b += brachiopod(x, y, s, col='#e8d4a8', dark='#3a2a18', rot=r)
    for sx, sy, ss in ((560, 380, 24), (80, 420, 18), (600, 700, 18)):
        b += spark(sx, sy, ss, col='#fffbe0')
    b += fireflies(30, 120, 1850, col='#fff3a8', core='#fffbe6', seed=9)
    b += darkband(860, 1240, .5)
    # buried layer below: mud strata with fossil outlines (lower half)
    b += '<path d="M0,1500 C300,1470 700,1520 1080,1480 L1080,1920 L0,1920Z" fill="#3a2414"/>'
    b += '<path d="M0,1560 C300,1540 700,1580 1080,1550 M0,1640 C400,1610 700,1660 1080,1630" fill="none" stroke="#5a3a22" stroke-width="6"/>'
    b += saca(580, 1640, .4, rot=-4, pal='fossil', mouth=None, eyes=False, shadow=False, detail=.5)
    b += saca(760, 1720, .36, rot=8, flip=True, pal='fossil', mouth=None, eyes=False, shadow=False, detail=.5)
    helmet = '<path d="M-30 -86 q36 -50 72 0z" fill="#e8d6a0" stroke-width="3.4"/><path d="M-46 -84 q52 -16 104 0 q-52 12 -104 0z" fill="#d8c088" stroke-width="3.4"/>'
    b += frog(240, 1740, 3.2, mouth='O', arms=('q-22 -10 -28 -40', 'q22 -10 28 -40'), look=(5, -4), head=helmet, sweat=True)
    b += f'<rect width="{W}" height="{H}" fill="url(#vig)"/>'
    write(4, defs, b, [('BURIED', 200, 'w'), ('FAST', 280, 'y')], '#0a1e26', top=850)


# ---------------- 5: ice ----------------
def short5():
    random.seed(5)
    defs = FILTERS + VIG + lin('sky5', [(0, '#040818'), (.5, '#0a1a38'), (1, '#12304a')]) + halo('h5', 560, 720, 420, inner='#fff3c8', outer='#9ff0ff')
    defs += lin('ice5', [(0, '#e8fbff'), (.5, '#9fd8f0'), (1, '#4a8ab8')])
    b = f'<rect width="{W}" height="{H}" fill="url(#sky5)"/>'
    b += ''.join(f'<circle cx="{random.randint(0, 1080)}" cy="{random.randint(0, 600)}" r="{random.choice([1.4, 2, 2.6])}" fill="#eaffff" opacity="{random.uniform(.3, .9):.2f}"/>' for _ in range(110))
    for k, c in enumerate(('#5af0b0', '#7ad8ff', '#a08aff')):   # aurora
        b += f'<path d="M-40,{160 + k * 50} C200,{60 + k * 60} 420,{260 + k * 30} 700,{140 + k * 40} C860,{80 + k * 40} 980,{180 + k * 30} 1120,{120 + k * 40}" fill="none" stroke="{c}" stroke-width="{60 - k * 14}" opacity=".28" filter="url(#b24)"/>'
    # glacier wall (top half), cracks + glow
    b += '<path d="M-20,330 L120,250 L240,300 L380,210 L520,280 L640,190 L780,270 L900,220 L1100,290 L1100,640 C900,600 760,660 600,620 C420,590 260,650 -20,610Z" fill="url(#ice5)" stroke="#1a3a5a" stroke-width="5"/>'
    for x0, y0 in ((160, 300), (420, 260), (700, 250), (920, 280)):
        b += f'<path d="M{x0},{y0} l-20,90 l30,60 l-24,110" fill="none" stroke="#3a7aa8" stroke-width="4" opacity=".7"/><path d="M{x0 + 6},{y0} l-20,90 l30,60" fill="none" stroke="#fff" stroke-width="2" opacity=".7"/>'
    b += '<path d="M-20,330 L120,250 L240,300 L380,210 L520,280 L640,190 L780,270 L900,220 L1100,290" fill="none" stroke="#fff" stroke-width="6" opacity=".9"/>'
    # icicles
    b += ''.join(f'<path d="M{x},{612 + (x % 7) * 4} l12,{40 + (x % 5) * 12} l12,{-40 - (x % 5) * 12}z" fill="#cfefff" stroke="#3a7aa8" stroke-width="2"/>' for x in range(20, 1060, 70))
    # exposed sea floor with the last pool
    b += '<path d="M-20,640 C260,660 420,600 600,630 C760,660 900,610 1100,650 L1100,860 L-20,860Z" fill="#4a5a6a"/>'
    b += '<ellipse cx="560" cy="760" rx="330" ry="80" fill="#0e3a5a" stroke="#cfefff" stroke-width="5"/>'
    b += '<ellipse cx="560" cy="720" rx="420" ry="260" fill="url(#h5)"/>'
    b += '<ellipse cx="560" cy="750" rx="300" ry="60" fill="#3ab0d8" opacity=".5"/>'
    for r in (60, 120, 190):
        b += f'<ellipse cx="560" cy="760" rx="{r * 1.4:.0f}" ry="{r * .3:.0f}" fill="none" stroke="#e6fff4" stroke-width="3" opacity="{.7 - r / 400:.2f}"/>'
    b += saca(400, 724, .5, flip=False, rot=-4, pal='glow', mouth='O', look=(3, -4), bend=-10, glow='#fff3a8', shadow=False)
    b += ''.join(brachiopod(x, y, .7, col='#c8c0b0', dark='#2a2a30', rot=r) for x, y, r in ((140, 700, -8), (250, 720, 10), (900, 700, 6), (980, 730, -4)))
    for sx, sy, ss in ((300, 560, 22), (820, 540, 24), (560, 470, 18)):
        b += spark(sx, sy, ss, col='#ffffff')
    b += fireflies(40, 120, 1850, col='#dff8ff', core='#ffffff', seed=12)
    b += darkband(860, 1240, .5)
    # snowy ground + frog in a woolly hat and scarf
    b += '<path d="M0,1560 C300,1520 700,1580 1080,1530 L1080,1920 L0,1920Z" fill="#cfe4f0"/><path d="M0,1560 C300,1520 700,1580 1080,1530" fill="none" stroke="#fff" stroke-width="8"/>'
    hat = '<path d="M-30 -84 q34 -44 70 0z" fill="#d9534a" stroke-width="3.4"/><rect x="-34" y="-90" width="78" height="14" rx="6" fill="#f4f0e8" stroke-width="3"/><circle cx="6" cy="-128" r="10" fill="#f4f0e8" stroke-width="3"/>'
    scarf = '<path d="M-30 -36 q36 12 70 0 l0 12 q-36 12 -70 0z" fill="#3a8ad0" stroke-width="3"/><path d="M24 -26 l6 34 l12 -2 l-4 -32z" fill="#3a8ad0" stroke-width="3"/>'
    b += '<ellipse cx="800" cy="1772" rx="180" ry="24" fill="#5a7a9a" opacity=".5" filter="url(#b12)"/>'
    b += frog(800, 1760, 3.2, mouth='O', arms=('q-18 -4 -14 -30', 'q18 -4 14 -30'), look=(-4, -6), torso=scarf, head=hat, flip=True)
    b += ''.join(f'<circle cx="{random.randint(0, 1080)}" cy="{random.randint(100, 1850)}" r="{random.choice([2, 3, 4])}" fill="#fff" opacity=".7"/>' for _ in range(70))
    b += f'<rect width="{W}" height="{H}" fill="url(#vig)"/>'
    write(5, defs, b, [('THEN CAME THE', 116, 'w'), ('ICE', 300, 'y')], '#040818', top=868)


if __name__ == '__main__':
    for f in (short1, short2, short3, short4, short5):
        f()
