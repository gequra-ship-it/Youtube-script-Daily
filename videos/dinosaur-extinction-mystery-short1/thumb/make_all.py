# Shorts thumbnails (style B, guideline 16-9) for dinosaur-extinction-mystery-short1..5. VERTICAL 1080x1920, one glowing subject,
# hook centred on a dark band (y ~860-1240), notebook frog in a bottom corner. Facts from each short's script only.
# Run: python3 videos/dinosaur-extinction-mystery-short1/thumb/make_all.py [1 2 3 4 5] -> videos/dinosaur-extinction-mystery-shortN/thumb/A.html
# 1 THE CLUE IN CLAY        cliff cross-section, thin clay seam glowing (iridium), dinosaur fossils only below it; geologist frog w/ hammer
# 2 IT RAINED GLASS         orange furnace sky, glowing molten-glass droplets streaking down, forests catching fire; frog under umbrella
# 3 SIZE BECAME A TRAP      giant sauropod silhouette under a soot-dimmed sun; below, a rat-sized mammal glowing in its burrow; frog w/ lantern
# 4 ASTEROID OR VOLCANOES?  blazing asteroid above, Deccan-style stepped lava flows glowing below; frog pointing up
# 5 A LIVING DINOSAUR       glowing sparrow on a branch with a ghostly T. rex silhouette behind; frog on the windowsill with morning coffee
import os, sys, math, random, shutil
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
sys.path.insert(0, os.path.join(REPO, 'tools'))
sys.path.insert(0, os.path.join(REPO, 'videos', 'trilobite-extinction', 'thumb'))
from make import frog, FILTERS, INK, GREEN   # shared posable frog (pupil kept inside the white)
from thumb_lib import vpage, vsvg, lin, rad, spark, fireflies, halo, darkband

W, H = 1080, 1920
Y = lambda w: f'<span class="g">{w}</span>'


def vig(id='vig', a=.75):
    return rad(id, 540, 960, 1250, [(0, '#000', 0), (.5, '#000', 0), (1, '#000', a)])


def save(n, bg, d, b, lines, outline):
    out = os.path.join(REPO, 'videos', f'dinosaur-extinction-mystery-short{n}', 'thumb'); os.makedirs(out, exist_ok=True)
    for f in os.listdir(os.path.join(REPO, 'tools', 'assets', 'thumb_v')):
        shutil.copy(os.path.join(REPO, 'tools', 'assets', 'thumb_v', f), out)
    hgt = sum(int(s * .97) for _, s, _ in lines[:-1]) + lines[-1][1]
    open(os.path.join(out, 'A.html'), 'w').write(vpage(bg, vsvg(d, b), lines, outline=outline, top=int(1050 - hgt / 2 - 12)))


def wavy(y, amp, rnd, ph=None, step=40):
    ph = rnd.uniform(0, 6) if ph is None else ph
    return [(x, y + amp * math.sin(x / 170 + ph) + amp * .4 * math.sin(x / 61 + ph * 2)) for x in range(-40, W + 81, step)]


def band(top, bot):
    return 'M' + ' L'.join(f'{x:.0f} {y:.0f}' for x, y in top) + ' L' + ' L'.join(f'{x:.0f} {y:.0f}' for x, y in reversed(bot)) + 'Z'


def tf(g, x, y, s, flip=False):
    return f'<g transform="translate({x} {y}) scale({-s if flip else s} {s})">{g}</g>'


# ---- silhouettes (local units, feet at y=0) ----
TREX = ('M-230 -150 Q-120 -175 -40 -195 Q40 -215 95 -215 L120 -245 Q160 -262 205 -250 L228 -232 L226 -214 L178 -212 L222 -200 L220 -190 '
        'Q170 -180 140 -185 Q115 -170 105 -150 L128 -138 L132 -128 L122 -130 L102 -140 Q85 -110 50 -100 L55 -60 L40 -10 L72 -4 L72 4 L8 4 '
        'L15 -50 Q-20 -80 -50 -110 Q-130 -140 -230 -150Z')
TREX_FAR = 'M-10 -110 L-5 -55 L-22 -8 L8 -4 L8 3 L-42 3 L-30 -55 Q-40 -90 -30 -110Z'
SAURO = ('M-330 -470 Q-350 -480 -366 -470 L-374 -458 Q-360 -448 -336 -452 Q-280 -380 -200 -232 Q-170 -160 -150 -130 L-150 0 L-104 0 '
         'L-102 -108 Q-20 -94 60 -104 L70 0 L116 0 L122 -120 Q200 -140 300 -110 Q400 -80 470 -58 Q400 -112 300 -172 Q200 -244 60 -252 '
         'Q-100 -262 -172 -302 Q-246 -410 -330 -470Z')
SAURO_FAR = 'M-120 -130 L-124 0 L-86 0 L-80 -110Z M90 -110 L96 0 L136 0 L140 -120Z'


# ================= 1: THE CLUE IN CLAY =================
def make_1():
    rnd = random.Random(11)
    SY = 470   # clay seam
    d = FILTERS + vig() + lin('sky1', [(0, '#050a1c'), (1, '#16203a')])
    d += halo('h1', 540, SY, 700, inner='#fff3c0', outer='#5fe8d0')
    d += lin('seam1', [(0, '#7ff5d8'), (.5, '#fffbe0'), (1, '#7ff5d8')], x2=1, y2=0)
    b = f'<rect width="{W}" height="{H}" fill="url(#sky1)"/>'
    b += ''.join(f'<circle cx="{rnd.randint(0, W)}" cy="{rnd.randint(10, 150)}" r="{rnd.choice([1.4, 2, 2.6])}" fill="#eaf4ff" opacity="{rnd.uniform(.3, .9):.2f}"/>' for _ in range(40))
    # strata from the cliff top down: younger grey rock above the seam, older pinkish limestone below
    ys = [175, 230, 300, 360, 420, SY - 13, SY + 13, 540, 610, 700, 800, 905, 1010, 1130, 1260, 1380, 1500, 1620, 1760, 1990]
    cols = ['#3e3c48', '#4a4652', '#3a3844', '#4c4854', '#423e4a', '#1c1614', '#6a4a46', '#5e4040', '#6e5048', '#5a3e3a', '#664844',
            '#583c38', '#624642', '#523834', '#5c403c', '#4c3430', '#563c38', '#46302c', '#4e3632']
    tops = [wavy(y, 10 if k else 18, rnd, step=40) for k, y in enumerate(ys)]
    tops[5] = [(x, y - 1) for x, y in wavy(SY - 13, 6, rnd, ph=1.0)]; tops[6] = [(x, y) for x, y in wavy(SY + 13, 6, rnd, ph=1.0)]
    for k in range(len(ys) - 1):
        b += f'<path d="{band(tops[k], tops[k + 1])}" fill="{cols[k]}"/>'
        if k != 5:
            b += f'<path d="M' + ' L'.join(f'{x:.0f} {y:.0f}' for x, y in tops[k + 1]) + '" stroke="#1a1214" stroke-width="3" fill="none" opacity=".5"/>'
    # pebbles / grain
    for _ in range(160):
        y = rnd.randint(190, 1900)
        if abs(y - SY) < 30: continue
        b += f'<ellipse cx="{rnd.randint(0, W)}" cy="{y}" rx="{rnd.randint(3, 10)}" ry="{rnd.randint(2, 5)}" fill="{rnd.choice(["#2a2022", "#8a7470", "#1e1a1c"])}" opacity="{rnd.uniform(.25, .6):.2f}"/>'
    b += f'<rect width="{W}" height="{H}" fill="url(#h1)" opacity=".55"/>'
    # fossils only BELOW the seam: dinosaur skull, vertebrae, ammonite
    sk = ('<path d="M0 70 Q10 40 60 30 Q140 8 220 20 Q262 30 264 72 Q256 112 220 126 L150 128 Q120 142 80 132 L20 112 Q0 100 0 70Z" fill="#e9dcc0" stroke="#3a2c1c" stroke-width="6"/>'
          '<ellipse cx="34" cy="62" rx="12" ry="8" fill="#3a2a22"/><ellipse cx="98" cy="64" rx="30" ry="19" fill="#3a2a22"/><circle cx="172" cy="52" r="17" fill="#3a2a22"/>'
          '<ellipse cx="228" cy="74" rx="17" ry="25" fill="#3a2a22"/><path d="M12 100 Q110 114 232 104" fill="none" stroke="#3a2c1c" stroke-width="5"/>'
          + ''.join(f'<path d="M{x} {100 + (x - 10) * .09:.0f} l6 14 l6 -14z" fill="#fff6dc" stroke="#3a2c1c" stroke-width="2.5"/>' for x in range(18, 150, 16))
          + '<path d="M40 40 Q120 18 210 26" fill="none" stroke="#fffaf0" stroke-width="5" opacity=".8"/>')
    b += f'<ellipse cx="640" cy="690" rx="230" ry="110" fill="#ffe8b0" opacity=".14" filter="url(#b24)"/>'
    b += tf(sk, 480, 610, 1.25)
    for k in range(7):
        x = 110 + k * 46; y = 760 - k * 10
        b += f'<path d="M{x} {y} l6 -34" stroke="#3a2c1c" stroke-width="13" stroke-linecap="round"/><path d="M{x} {y} l6 -34" stroke="#e2d4b6" stroke-width="7" stroke-linecap="round"/>'
        b += f'<ellipse cx="{x}" cy="{y}" rx="22" ry="15" fill="#e2d4b6" stroke="#3a2c1c" stroke-width="4.5"/>'
    for k in range(3):
        x = 150 + k * 50
        b += f'<path d="M{x} {775 - k * 9} q-16 34 4 66" fill="none" stroke="#3a2c1c" stroke-width="11" stroke-linecap="round"/><path d="M{x} {775 - k * 9} q-16 34 4 66" fill="none" stroke="#d8c8a8" stroke-width="5" stroke-linecap="round"/>'
    am = '<circle r="62" fill="#c8b08a" stroke="#3a2c1c" stroke-width="5"/>' + ''.join(f'<circle r="{r}" fill="none" stroke="#5a4430" stroke-width="3.5"/>' for r in (44, 28, 14))
    am += ''.join(f'<path d="M{44 * math.cos(a):.1f} {44 * math.sin(a):.1f} L{60 * math.cos(a):.1f} {60 * math.sin(a):.1f}" stroke="#5a4430" stroke-width="3"/>' for a in [i * math.pi / 9 for i in range(18)])
    b += f'<g transform="translate(930 640)">{am}</g>'
    # THE seam: dark clay ribbon with a glowing line
    seam = 'M' + ' L'.join(f'{x:.0f} {y:.0f}' for x, y in wavy(SY, 6, rnd, ph=1.0))
    b += f'<path d="{seam}" stroke="#7ff5d8" stroke-width="90" fill="none" opacity=".5" filter="url(#b24)"/>'
    b += f'<path d="{seam}" stroke="#fff3c0" stroke-width="26" fill="none" opacity=".7" filter="url(#b6)"/>'
    b += f'<path d="{seam}" stroke="url(#seam1)" stroke-width="10" fill="none"/>'
    for x in range(30, W, 90):
        b += spark(x + rnd.randint(-20, 20), SY + 6 * math.sin(x / 170 + 1) + rnd.randint(-14, 14), rnd.choice([12, 16, 22]), col='#fffbe0')
    b += fireflies(26, 200, 820, col='#9ff0e0', core='#effffa', seed=5)
    b += darkband(860, 1240, .5)
    # rubble at the cliff foot + frog geologist
    b += '<path d="M-20 1790 q120 -60 260 -40 q160 -50 300 10 q200 -40 560 0 L1100 1940 L-20 1940z" fill="#2a1e1e"/>'
    for x, y, r in ((620, 1770, 40), (720, 1790, 26), (960, 1760, 50), (880, 1800, 22), (40, 1790, 30)):
        b += f'<ellipse cx="{x}" cy="{y}" rx="{r * 1.3:.0f}" ry="{r}" fill="#4a3634" stroke="#140e0e" stroke-width="4"/>'
    hat = ('<path d="M-30 -88 q36 -54 72 0z" fill="#f2c94c" stroke-width="3.4"/><ellipse cx="6" cy="-88" rx="48" ry="8" fill="#e0b23a" stroke-width="3.4"/>'
           '<circle cx="6" cy="-112" r="8" fill="#fffbe0" stroke-width="2.5"/>')
    ham = ('<path d="M62 -48 L74 -108" stroke="#5a3a1e" stroke-width="7"/><path d="M62 -48 L74 -108" stroke="#b07a40" stroke-width="3.6"/>'
           '<path d="M58 -116 L92 -104 L94 -112 L60 -124z" fill="#9aa4ae" stroke-width="3"/>')
    b += '<circle cx="270" cy="1420" r="60" fill="#fffbe0" opacity=".35" filter="url(#b24)"/>'
    b += frog(250, 1790, 3.3, look=(3, -5), mouth='O', shadow=True, brows=False, mid=hat, front=ham,
              armR='M38 -22 q18 -4 24 -26', armL='M-34 -22 q-14 6 -16 22')
    b += f'<rect width="{W}" height="{H}" fill="url(#vig)"/>'
    save(1, '#050a1c', d, b, [('THE CLUE IN', 140, 'w'), ('CLAY', 250, 'y')], '#0a0606')


# ================= 2: IT RAINED GLASS =================
def make_2():
    rnd = random.Random(22)
    d = FILTERS + vig(a=.7) + lin('sky2', [(0, '#1a0306'), (.3, '#5a1208'), (.62, '#b8400e'), (.78, '#ff9a3a'), (.8, '#ffb85a')])
    d += halo('h2', 520, 500, 520, inner='#fffbe0', outer='#ff8a2a')
    d += ('<radialGradient id="bead" cx=".4" cy=".35" r=".7"><stop offset="0" stop-color="#ffffff"/><stop offset=".3" stop-color="#fff2a8"/>'
          '<stop offset=".7" stop-color="#ffa030"/><stop offset="1" stop-color="#c8400a"/></radialGradient>')
    d += '<linearGradient id="trail" x1="0" y1="1" x2="1" y2="0"><stop offset="0" stop-color="#fff6c0" stop-opacity=".95"/><stop offset=".4" stop-color="#ff9a3a" stop-opacity=".55"/><stop offset="1" stop-color="#ff5a1a" stop-opacity="0"/></linearGradient>'
    b = f'<rect width="{W}" height="{H}" fill="url(#sky2)"/>'
    for _ in range(14):
        b += f'<ellipse cx="{rnd.randint(-60, 1140)}" cy="{rnd.randint(60, 1400)}" rx="{rnd.randint(160, 320)}" ry="{rnd.randint(40, 90)}" fill="#2a0806" opacity="{rnd.uniform(.12, .3):.2f}" filter="url(#b24)"/>'
    # falling glowing droplets (down-left), trails up-right
    for _ in range(46):
        x, y = rnd.randint(-40, 1120), rnd.randint(60, 1560)
        if 860 < y < 1240 and rnd.random() < .7: continue
        if math.hypot(x - 520, y - 500) < 200: continue
        r = rnd.choice([4, 5, 6, 8, 10]); L = r * rnd.randint(14, 22)
        b += f'<path d="M{x} {y} L{x + L * .42:.0f} {y - L}" stroke="#ffcf7a" stroke-width="{r * 1.2:.1f}" stroke-linecap="round" opacity=".45"/>'
        b += f'<circle cx="{x}" cy="{y}" r="{r * 3}" fill="#ffb050" opacity=".45" filter="url(#b6)"/><circle cx="{x}" cy="{y}" r="{r}" fill="#fff6d0"/>'
    # hero bead
    BX, BY, R = 520, 500, 100
    b += f'<ellipse cx="{BX}" cy="{BY}" rx="560" ry="560" fill="url(#h2)" opacity=".9"/>'
    b += f'<path d="M{BX - R * .9:.0f} {BY - R * .4:.0f} L1000 -60 L1180 -60 L1180 40 L{BX + R * .4:.0f} {BY + R * .9:.0f}Z" fill="url(#trail)" filter="url(#b6)"/>'
    b += f'<path d="M{BX - R * .5:.0f} {BY - R * .2:.0f} L1080 -40 L1120 0 L{BX + R * .2:.0f} {BY + R * .5:.0f}Z" fill="#fffbe0" opacity=".55" filter="url(#b12)"/>'
    b += f'<circle cx="{BX}" cy="{BY}" r="{R + 50}" fill="#ffe08a" opacity=".55" filter="url(#b24)"/>'
    b += f'<circle cx="{BX}" cy="{BY}" r="{R}" fill="url(#bead)" stroke="#5a1404" stroke-width="7"/>'
    b += f'<ellipse cx="{BX - 34}" cy="{BY - 38}" rx="30" ry="18" fill="#fff" opacity=".9" transform="rotate(-35 {BX - 34} {BY - 38})"/>'
    b += f'<path d="M{BX + 40} {BY + 66} q40 -30 46 -76" fill="none" stroke="#fff" stroke-width="7" stroke-linecap="round" opacity=".6"/>'
    for sx, sy, ss in ((BX - 220, BY - 120, 30), (BX + 230, BY + 150, 24), (BX - 180, BY + 210, 20), (BX + 200, BY - 220, 22), (BX - 300, BY + 40, 16)):
        b += spark(sx, sy, ss, col='#fffbe0')
    # horizon: forests catching fire, soot rising
    HZ = 1530
    hills = 'M-20 1560 q160 -70 320 -30 q170 -60 330 -6 q180 -50 470 10 L1100 1940 L-20 1940z'
    b += f'<path d="{hills}" fill="#1a0604"/>'
    for x in (90, 170, 260, 420, 520, 600, 690, 940, 1010):
        h = rnd.randint(110, 190); base = 1560 - (20 if 300 < x < 650 else 0)
        b += f'<path d="M{x} {base} L{x - 34} {base} L{x} {base - h} L{x + 34} {base}Z" fill="#120402"/>'
        if rnd.random() < .7:
            fy = base - h * .5
            b += f'<ellipse cx="{x}" cy="{fy:.0f}" rx="60" ry="{h * .7:.0f}" fill="#ff7a1a" opacity=".45" filter="url(#b24)"/>'
            b += f'<path d="M{x - 26} {base - 20} q-10 -60 14 -{h * .8:.0f} q4 40 14 30 q10 -40 4 -70 q30 50 20 {h * .55:.0f} q6 30 -52 40z" fill="#ffb03a"/>'
            b += f'<path d="M{x - 10} {base - 24} q-4 -40 10 -{h * .5:.0f} q16 40 6 {h * .45:.0f}z" fill="#fff0a0"/>'
            b += f'<path d="M{x} {base - h} q-40 -120 20 -240 q50 -100 0 -200" fill="none" stroke="#2a0e0a" stroke-width="40" opacity=".45" filter="url(#b12)"/>'
    b += darkband(860, 1240, .5)
    b += '<path d="M-20 1830 q300 -40 640 -10 q260 -20 500 10 L1100 1940 L-20 1940z" fill="#0c0302"/>'
    # frog sheltering under an umbrella (shaft in its right hand), droplets bouncing off
    can = ('<g transform="translate(18 -150) rotate(-14)"><path d="M-92 18 Q-80 -50 0 -54 Q80 -50 92 18 Q76 8 61 18 Q46 8 30 18 Q15 8 0 18 Q-15 8 -30 18 Q-46 8 -61 18 Q-76 8 -92 18Z" '
           'fill="#2f8f9a" stroke-width="4"/><path d="M0 -54 Q-30 -20 -30 18 M0 -54 Q30 -20 30 18 M0 -54 L0 18 M0 -54 Q-62 -24 -61 18 M0 -54 Q62 -24 61 18" fill="none" stroke="#1d5a62" stroke-width="2.6"/>'
           '<path d="M-60 -30 Q-30 -50 0 -50" fill="none" stroke="#bff6ff" stroke-width="4" opacity=".7"/><circle cx="0" cy="-58" r="5" fill="#d8c070" stroke-width="2.5"/></g>')
    shaft = '<path d="M22 -136 L56 -40" stroke="#3a2c1c" stroke-width="5"/><path d="M56 -40 q4 12 -8 14" fill="none" stroke="#3a2c1c" stroke-width="5"/>'
    sweat = '<path d="M-36 -86 q6 10 0 16 q-6 -6 0 -16z" fill="#cdeeff" stroke-width="2"/>'
    b += frog(740, 1830, 2.9, look=(-5, -4), mouth='O', shadow=True, back=shaft + can, front=sweat,
              armR='M38 -22 q18 -2 18 -20', armL='M-34 -22 q-16 -4 -18 -26')
    for x, y in ((700, 1300), (930, 1322), (650, 1360)):
        b += f'<circle cx="{x}" cy="{y}" r="16" fill="#ffb050" opacity=".5" filter="url(#b6)"/><circle cx="{x}" cy="{y}" r="6" fill="#fff6d0"/>'
        b += spark(x, y, 14, col='#fffbe0')
    b += f'<rect width="{W}" height="{H}" fill="url(#vig)"/>'
    save(2, '#1a0306', d, b, [('IT RAINED', 160, 'w'), ('GLASS', 260, 'y')], '#160404')


# ================= 3: SIZE BECAME A TRAP =================
def mammal():
    return ('<path d="M-88 12 Q-140 30 -176 58" fill="none" stroke="#2a1a10" stroke-width="12" stroke-linecap="round"/><path d="M-88 12 Q-140 30 -176 58" fill="none" stroke="#d89a8a" stroke-width="6" stroke-linecap="round"/>'
            '<ellipse cx="-40" cy="50" rx="26" ry="10" fill="#d89a8a" stroke="#2a1a10" stroke-width="4"/>'
            '<ellipse cx="0" cy="0" rx="92" ry="56" fill="#8a6040" stroke="#2a1a10" stroke-width="6"/><ellipse cx="14" cy="26" rx="60" ry="22" fill="#c8a07a" opacity=".8"/>'
            '<path d="M-60 -36 Q0 -60 60 -40" fill="none" stroke="#c89a70" stroke-width="6" opacity=".7"/>'
            '<ellipse cx="70" cy="-56" rx="20" ry="25" fill="#a87458" stroke="#2a1a10" stroke-width="5"/><ellipse cx="70" cy="-54" rx="10" ry="14" fill="#e8a49a"/>'
            '<ellipse cx="86" cy="-14" rx="50" ry="40" fill="#8a6040" stroke="#2a1a10" stroke-width="6"/>'
            '<path d="M112 -34 Q160 -12 168 0 Q152 14 112 16Z" fill="#8a6040" stroke="#2a1a10" stroke-width="6" stroke-linejoin="round"/>'
            '<circle cx="168" cy="0" r="8" fill="#e07b7b" stroke="#2a1a10" stroke-width="3"/>'
            '<circle cx="106" cy="-22" r="10" fill="#140a06"/><circle cx="109" cy="-25" r="3.5" fill="#fff"/>'
            '<path d="M150 4 l40 -10 M150 6 l42 4 M150 8 l36 16" stroke="#f4e6d0" stroke-width="2.4" opacity=".8"/>'
            '<ellipse cx="150" cy="36" rx="16" ry="11" fill="#f2c94c" stroke="#2a1a10" stroke-width="4"/>'
            '<ellipse cx="128" cy="34" rx="12" ry="8" fill="#a87458" stroke="#2a1a10" stroke-width="4"/><ellipse cx="166" cy="44" rx="10" ry="7" fill="#a87458" stroke="#2a1a10" stroke-width="4"/>')


def make_3():
    rnd = random.Random(33)
    d = FILTERS + vig(a=.8) + lin('sky3', [(0, '#16140f'), (.6, '#3a332a'), (1, '#4e4436')])
    d += rad('sun3', 690, 290, 300, [(0, '#ffd8a0', .55), (.3, '#c88a50', .25), (1, '#c88a50', 0)])
    d += lin('soil3', [(0, '#2a1a10'), (1, '#120a06')])
    d += halo('h3', 470, 1500, 300, inner='#ffd890', outer='#ff8a3a')
    b = f'<rect width="{W}" height="{H}" fill="url(#sky3)"/>'
    b += f'<rect width="{W}" height="900" fill="url(#sun3)"/><circle cx="690" cy="290" r="62" fill="#e8b880" opacity=".55" filter="url(#b12)"/>'
    for _ in range(10):
        b += f'<ellipse cx="{rnd.randint(-60, 1140)}" cy="{rnd.randint(60, 760)}" rx="{rnd.randint(180, 340)}" ry="{rnd.randint(30, 70)}" fill="#1a1612" opacity="{rnd.uniform(.25, .45):.2f}" filter="url(#b24)"/>'
    b += ''.join(f'<circle cx="{rnd.randint(0, W)}" cy="{rnd.randint(40, 840)}" r="{rnd.choice([2, 3, 4])}" fill="#a8a094" opacity="{rnd.uniform(.25, .6):.2f}"/>' for _ in range(90))
    # barren ground + dead trees
    GY = 820
    b += f'<path d="M-20 {GY + 10} q200 -26 420 -8 q260 -20 680 6 L1100 1000 L-20 1000z" fill="#1c1712"/>'
    for x, h, s in ((80, 200, 1), (980, 240, -1), (900, 120, 1)):
        b += f'<path d="M{x} {GY + 6} l4 -{h} M{x + 2} {GY - h * .55:.0f} l{34 * s} -50 M{x + 3} {GY - h * .8:.0f} l{-28 * s} -36" stroke="#100c08" stroke-width="10" stroke-linecap="round"/>'
    # giant sauropod silhouette, rim-lit by the dim sun
    sx, sy, sc = 500, GY + 4, 1.25
    b += f'<g transform="translate({sx} {sy}) scale({sc})"><path d="{SAURO}" fill="none" stroke="#e8b880" stroke-width="10" opacity=".45" filter="url(#b6)"/>'
    b += f'<path d="{SAURO_FAR}" fill="#0a0806"/><path d="{SAURO}" fill="#0e0b08" stroke="#c8925a" stroke-width="2.4" stroke-opacity=".7"/>'
    b += '<circle cx="-352" cy="-466" r="3.5" fill="#c8925a" opacity=".8"/></g>'
    b += darkband(860, 1240, .55)
    # underground cross-section
    b += f'<path d="M-20 1180 q300 -20 560 -4 q300 -16 560 6 L1100 1940 L-20 1940z" fill="url(#soil3)"/>'
    for _ in range(70):
        b += f'<ellipse cx="{rnd.randint(0, W)}" cy="{rnd.randint(1200, 1900)}" rx="{rnd.randint(4, 14)}" ry="{rnd.randint(3, 8)}" fill="#3a2818" opacity="{rnd.uniform(.4, .8):.2f}"/>'
    for x0 in (120, 700, 960):
        b += f'<path d="M{x0} 1190 q-20 80 10 160 q20 60 -10 120" fill="none" stroke="#3a2616" stroke-width="5" opacity=".7"/>'
    tunnel = 'M250 1190 Q240 1300 330 1380 Q400 1440 430 1480'
    b += f'<path d="{tunnel}" fill="none" stroke="#080402" stroke-width="80" stroke-linecap="round"/>'
    b += '<ellipse cx="480" cy="1520" rx="230" ry="130" fill="#080402"/>'
    b += '<ellipse cx="480" cy="1520" rx="560" ry="560" fill="url(#h3)" opacity=".75"/>'
    b += '<ellipse cx="480" cy="1530" rx="200" ry="105" fill="#2a160a" opacity=".85"/>'
    b += '<ellipse cx="480" cy="1610" rx="200" ry="30" fill="#4a2a16" opacity=".8"/>'
    b += tf(mammal(), 450, 1550, 1.0)
    for x, y in ((610, 1608), (628, 1600), (596, 1612), (330, 1612)):
        b += f'<ellipse cx="{x}" cy="{y}" rx="9" ry="6" fill="#e8c060" stroke="#2a1a10" stroke-width="2.5"/>'
    b += '<path d="M360 1600 l14 -8 l14 8 M366 1596 l-6 -10 M382 1596 l6 -10" stroke="#2a1a10" stroke-width="3" fill="none"/><ellipse cx="374" cy="1602" rx="14" ry="7" fill="#5a4a2a" stroke="#2a1a10" stroke-width="3"/>'
    for sxx, syy, ss in ((300, 1460, 16), (660, 1450, 18), (640, 1560, 12)):
        b += spark(sxx, syy, ss, col='#fff0c0')
    # frog with a lantern in its own side tunnel
    b += '<ellipse cx="850" cy="1720" rx="190" ry="170" fill="#080402"/><path d="M1100 1560 Q980 1580 940 1620" stroke="#080402" stroke-width="90" fill="none"/>'
    b += '<ellipse cx="740" cy="1700" rx="120" ry="120" fill="#ffc870" opacity=".35" filter="url(#b24)"/>'
    lant = ('<path d="M-58 -46 L-58 -34" stroke-width="3"/><path d="M-66 -34 L-50 -34 L-48 -28 L-68 -28Z" fill="#6a4a2a" stroke-width="2.5"/>'
            '<rect x="-68" y="-28" width="20" height="26" rx="3" fill="#fff0b0" stroke-width="2.5"/><path d="M-58 -24 l0 18" stroke="#c88a3a" stroke-width="2"/>'
            '<rect x="-70" y="-2" width="24" height="5" rx="2" fill="#6a4a2a" stroke-width="2.5"/>')
    b += frog(870, 1830, 3.0, look=(-6, -3), mouth='O', shadow=True, front=lant, armL='M-34 -22 q-18 -4 -24 -24', armR='M38 -22 q14 6 16 22')
    b += '<circle cx="696" cy="1790" r="40" fill="#fff0b0" opacity=".45" filter="url(#b12)"/>'
    b += f'<rect width="{W}" height="{H}" fill="url(#vig)"/>'
    save(3, '#16140f', d, b, [('SIZE BECAME', 140, 'w'), ('A TRAP', 240, 'y')], '#0a0806')


# ================= 4: ASTEROID OR VOLCANOES? =================
def make_4():
    rnd = random.Random(44)
    d = FILTERS + vig(a=.7) + lin('sky4', [(0, '#04061a'), (.45, '#1a1036'), (.75, '#4a1420'), (1, '#8a2a14')])
    d += halo('h4', 650, 430, 520, inner='#fffbe0', outer='#7ff5d8')
    d += '<linearGradient id="tail4" x1="0" y1="1" x2="1" y2="0"><stop offset="0" stop-color="#fff6c0" stop-opacity=".95"/><stop offset=".35" stop-color="#ffb04a" stop-opacity=".6"/><stop offset="1" stop-color="#ff5a1a" stop-opacity="0"/></linearGradient>'
    d += ('<radialGradient id="rock4" cx=".3" cy=".7" r=".9"><stop offset="0" stop-color="#fff2c0"/><stop offset=".25" stop-color="#ffa040"/>'
          '<stop offset=".55" stop-color="#6a4a3a"/><stop offset="1" stop-color="#2a1e1a"/></radialGradient>')
    d += rad('lava4', 760, 1500, 800, [(0, '#ff9a3a', 1), (.5, '#c8300a', .5), (1, '#c8300a', 0)])
    b = f'<rect width="{W}" height="{H}" fill="url(#sky4)"/>'
    b += ''.join(f'<circle cx="{rnd.randint(0, W)}" cy="{rnd.randint(10, 820)}" r="{rnd.choice([1.3, 1.9, 2.6])}" fill="#eaf4ff" opacity="{rnd.uniform(.3, .9):.2f}"/>' for _ in range(110))
    AX, AY = 620, 450
    b += f'<ellipse cx="{AX}" cy="{AY}" rx="540" ry="540" fill="url(#h4)" opacity=".7"/>'
    b += f'<path d="M{AX - 120} {AY - 60} L1060 -80 L1200 -80 L1200 60 L{AX + 60} {AY + 120}Z" fill="url(#tail4)" filter="url(#b12)"/>'
    b += f'<path d="M{AX - 70} {AY - 20} L1100 -60 L1160 0 L{AX + 20} {AY + 70}Z" fill="#fffbe0" opacity=".5" filter="url(#b12)"/>'
    pts = []
    for k in range(16):
        a = k / 16 * 2 * math.pi; r = 150 * (1 + .14 * math.sin(3 * a + 1) + .08 * math.sin(7 * a))
        pts.append((AX + r * math.cos(a), AY + r * .86 * math.sin(a)))
    rock = 'M' + ' L'.join(f'{x:.0f} {y:.0f}' for x, y in pts) + 'Z'
    b += f'<path d="{rock}" fill="#ffb050" opacity=".6" filter="url(#b24)" transform="translate(-30 30)"/>'
    b += f'<path d="{rock}" fill="url(#rock4)" stroke="#140c0a" stroke-width="8" stroke-linejoin="round"/>'
    for cx, cy, r in ((AX + 40, AY - 50, 30), (AX + 80, AY + 40, 20), (AX - 10, AY - 90, 16), (AX + 20, AY + 10, 14)):
        b += f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="#1e1612" opacity=".55"/><path d="M{cx - r * .7:.0f} {cy + r * .5:.0f} a{r} {r} 0 0 0 {r * 1.4:.0f} 0" fill="none" stroke="#8a6a5a" stroke-width="4" opacity=".6"/>'
    b += f'<path d="M{AX - 150} {AY + 30} Q{AX - 120} {AY + 120} {AX - 30} {AY + 140}" fill="none" stroke="#fffbe0" stroke-width="12" stroke-linecap="round" filter="url(#b3)"/>'
    for sxx, syy, ss in ((AX - 280, AY - 140, 26), (AX + 250, AY + 190, 22), (AX - 260, AY + 230, 18), (AX - 380, AY + 40, 14)):
        b += spark(sxx, syy, ss, col='#fffbe0')
    # stepped lava plateaus (flood basalt) with glowing flows
    b += f'<rect y="900" width="{W}" height="1020" fill="url(#lava4)"/>'
    steps = [(1310, '#1e100c'), (1430, '#160a08'), (1560, '#120806'), (1700, '#0e0604')]
    for k, (y, c) in enumerate(steps):
        x0 = 40 + k * 60
        b += f'<path d="M-20 {y} L{x0 + 200} {y} L{x0 + 240} {y - 20} L{x0 + 520} {y - 20} L{x0 + 560} {y - 40} L1100 {y - 40} L1100 1940 L-20 1940Z" fill="{c}" stroke="#2a120c" stroke-width="3"/>'
    for k, (y, c) in enumerate(steps):   # lava pouring over each step edge
        x0 = 40 + k * 60
        b += f'<path d="M{x0 + 560} {y - 40} L1100 {y - 40}" stroke="#ff6a1a" stroke-width="18" opacity=".7" filter="url(#b6)"/><path d="M{x0 + 560} {y - 40} L1100 {y - 40}" stroke="#ffc060" stroke-width="5"/>'
    flows = ['M800 1290 L790 1370 L770 1410 L760 1520 L740 1560 L730 1660 L700 1700 L690 1940',
             'M960 1290 L955 1370 L930 1410 L925 1520', 'M560 1410 L548 1520 L520 1560 L512 1700']
    for f in flows:
        b += f'<path d="{f}" fill="none" stroke="#ff6a1a" stroke-width="60" opacity=".5" filter="url(#b12)"/>'
        b += f'<path d="{f}" fill="none" stroke="#ff8a2a" stroke-width="36" stroke-linecap="round"/><path d="{f}" fill="none" stroke="#fff0a0" stroke-width="13" stroke-linecap="round"/>'
    for x, h in ((800, 150), (960, 110), (680, 80)):
        b += f'<ellipse cx="{x}" cy="1300" rx="70" ry="{h}" fill="#ff8a2a" opacity=".5" filter="url(#b24)"/>'
        b += f'<path d="M{x - 26} 1300 Q{x - 14} {1300 - h} {x} {1300 - h - 20} Q{x + 14} {1300 - h} {x + 26} 1300Z" fill="#ffb03a"/><path d="M{x - 10} 1300 Q{x} {1300 - h * .8:.0f} {x + 10} 1300Z" fill="#fff4b0"/>'
        for _ in range(5):
            b += f'<circle cx="{x + rnd.randint(-60, 60)}" cy="{1300 - h + rnd.randint(-20, 100)}" r="{rnd.choice([4, 6])}" fill="#ffd070"/>'
    for x in (860, 980):
        b += f'<path d="M{x} 1100 q-60 -100 20 -200 q60 -80 -20 -160" fill="none" stroke="#3a1a18" stroke-width="70" opacity=".35" filter="url(#b24)"/>'
    b += darkband(860, 1240, .55)
    # frog on a dark rock ledge, pointing at the asteroid
    b += '<path d="M-20 1800 q120 -50 300 -40 q120 10 160 60 L460 1940 L-20 1940z" fill="#080404" stroke="#2a120c" stroke-width="4"/>'
    sweat = '<path d="M-36 -84 q6 10 0 16 q-6 -6 0 -16z" fill="#cdeeff" stroke-width="2"/>'
    b += frog(230, 1790, 3.2, look=(2, -5), mouth='O', shadow=True, front=sweat, armR='M38 -22 q20 -20 26 -52', armL='M-34 -22 q-14 6 -16 22')
    b += f'<rect width="{W}" height="{H}" fill="url(#vig)"/>'
    save(4, '#04061a', d, b, [('ASTEROID OR', 140, 'w'), ('VOLCANOES?', 142, 'y')], '#08040a')


# ================= 5: A LIVING DINOSAUR =================
def sparrow():
    return ('<path d="M90 -84 L206 -34 L196 -14 L80 -58Z" fill="#6a4a30" stroke="#1e140c" stroke-width="5" stroke-linejoin="round"/>'
            '<path d="M120 -70 L196 -30 M110 -62 L188 -22" stroke="#3a2414" stroke-width="3"/>'
            '<path d="M-20 -26 L-26 2 M12 -28 L14 2" stroke="#b08a6a" stroke-width="6" stroke-linecap="round"/>'
            '<path d="M-60 -112 Q-92 -60 -50 -26 Q0 2 70 -40 Q122 -70 102 -112 Q62 -152 -10 -152 Q-50 -146 -60 -112Z" fill="#cdbba0" stroke="#1e140c" stroke-width="6"/>'
            '<ellipse cx="-14" cy="-56" rx="48" ry="22" fill="#e4d6c0" opacity=".8"/>'
            '<path d="M-22 -132 Q60 -154 124 -96 Q92 -54 20 -56 Q-22 -80 -22 -132Z" fill="#8a5a32" stroke="#1e140c" stroke-width="5"/>'
            '<path d="M10 -120 q20 10 30 30 M40 -126 q20 12 30 34 M70 -116 q18 12 26 30" stroke="#2a1a0e" stroke-width="7" stroke-linecap="round" fill="none"/>'
            '<path d="M0 -84 Q50 -76 100 -92" stroke="#f4eee0" stroke-width="6" fill="none" stroke-linecap="round"/>'
            '<circle cx="-72" cy="-150" r="54" fill="#a8a49a" stroke="#1e140c" stroke-width="6"/>'
            '<path d="M-60 -200 Q-14 -186 -22 -140 Q-40 -130 -50 -150 Q-56 -172 -88 -186 Q-80 -200 -60 -200Z" fill="#8a4a26"/>'
            '<ellipse cx="-80" cy="-132" rx="26" ry="17" fill="#ece4d4"/>'
            '<path d="M-110 -122 Q-90 -88 -58 -108 Q-70 -124 -98 -128Z" fill="#1a1410"/>'
            '<circle cx="-92" cy="-158" r="9" fill="#100a06"/><circle cx="-89" cy="-161" r="3.2" fill="#fff"/>'
            '<path d="M-120 -156 L-152 -146 L-120 -134Z" fill="#3a3028" stroke="#1e140c" stroke-width="3" stroke-linejoin="round"/>'
            '<path d="M-38 2 q12 -10 20 0 M-6 2 q12 -10 20 0 M-30 4 l-8 8 M2 4 l-8 8" stroke="#b08a6a" stroke-width="4" fill="none" stroke-linecap="round"/>')


def make_5():
    rnd = random.Random(55)
    d = FILTERS + vig(a=.7) + lin('sky5', [(0, '#060c24'), (.35, '#12304a'), (.6, '#1e5a66'), (.82, '#c88a5a'), (1, '#e8a860')])
    d += halo('h5', 540, 600, 460, inner='#fff3a8', outer='#7ff5d8')
    d += lin('wood5', [(0, '#7a4e2a'), (1, '#3a2210')])
    b = f'<rect width="{W}" height="{H}" fill="url(#sky5)"/>'
    b += ''.join(f'<circle cx="{rnd.randint(0, W)}" cy="{rnd.randint(10, 640)}" r="{rnd.choice([1.3, 1.9, 2.6])}" fill="#eaffff" opacity="{rnd.uniform(.3, .9):.2f}"/>' for _ in range(70))
    # ghostly T. rex behind (facing left like the sparrow)
    g = f'<path d="{TREX_FAR}" fill="#7ff5d8" opacity=".08"/><path d="{TREX}" fill="#7ff5d8" fill-opacity=".1" stroke="#9ff8e4" stroke-width="3" stroke-opacity=".7"/>'
    b += f'<g transform="translate(560 840) scale(-2.25 2.25)"><path d="{TREX}" fill="none" stroke="#7ff5d8" stroke-width="12" opacity=".35" filter="url(#b12)"/>{g}'
    b += '<circle cx="186" cy="-236" r="6" fill="#dffff6" opacity=".8"/></g>'
    b += f'<ellipse cx="540" cy="600" rx="470" ry="470" fill="url(#h5)" opacity=".85"/>'
    # branch from the right edge
    br = 'M1100 760 Q900 740 760 752 Q600 762 420 738 Q330 728 250 700'
    b += f'<path d="{br}" fill="none" stroke="#120a06" stroke-width="40" stroke-linecap="round"/><path d="{br}" fill="none" stroke="#5a3a22" stroke-width="28" stroke-linecap="round"/>'
    b += '<path d="M1100 752 Q900 734 760 744 Q600 752 420 730" fill="none" stroke="#b08a5a" stroke-width="5" opacity=".6"/>'
    for x0, y0, x1, y1 in ((330, 726, 260, 640), (880, 748, 960, 660), (980, 752, 1060, 820)):
        b += f'<path d="M{x0} {y0} Q{(x0 + x1) / 2:.0f} {y1 + 30} {x1} {y1}" stroke="#120a06" stroke-width="16" fill="none" stroke-linecap="round"/><path d="M{x0} {y0} Q{(x0 + x1) / 2:.0f} {y1 + 30} {x1} {y1}" stroke="#5a3a22" stroke-width="8" fill="none" stroke-linecap="round"/>'
    for lx, ly, a in ((260, 640, -40), (960, 660, 30), (1060, 820, 70), (230, 700, -120), (700, 760, 120)):
        b += f'<path transform="translate({lx} {ly}) rotate({a})" d="M0 0 q24 -36 0 -76 q-24 40 0 76z" fill="#4f8a3e" stroke="#0e2a1c" stroke-width="3.5"/>'
    b += '<ellipse cx="560" cy="600" rx="260" ry="180" fill="#fff3a8" opacity=".35" filter="url(#b50)"/>'
    b += tf(sparrow(), 560, 744, 1.55)
    for sxx, syy, ss in ((260, 440, 24), (830, 470, 22), (300, 600, 16), (800, 640, 18), (640, 320, 16)):
        b += spark(sxx, syy, ss, col='#fffbe0')
    b += fireflies(34, 160, 840, seed=9)
    b += darkband(860, 1240, .5)
    # outside: dark bushes; inside: window frame + sill with frog and coffee
    for x in range(-40, 1120, 120):
        b += f'<ellipse cx="{x + rnd.randint(-20, 20)}" cy="{1640 + rnd.randint(-30, 30)}" rx="{rnd.randint(90, 140)}" ry="{rnd.randint(110, 170)}" fill="#0c2018" opacity=".95"/>'
    b += f'<rect x="0" y="0" width="34" height="{H}" fill="url(#wood5)" stroke="#120a04" stroke-width="4"/><rect x="1046" y="0" width="34" height="{H}" fill="url(#wood5)" stroke="#120a04" stroke-width="4"/>'
    b += '<rect x="-10" y="1760" width="1100" height="200" fill="url(#wood5)" stroke="#120a04" stroke-width="5"/><path d="M0 1770 L1080 1770" stroke="#c89060" stroke-width="5" opacity=".7"/>'
    mug = ('<path d="M44 -66 L80 -66 L77 -30 L47 -30Z" fill="#e8e2d4" stroke-width="3"/><path d="M80 -58 q12 2 10 14 q-2 8 -12 6" fill="none" stroke-width="3"/>'
           '<path d="M46 -62 L78 -62" stroke="#6a3e1c" stroke-width="3"/>'
           '<path d="M56 -74 q-6 -10 2 -20 q6 -10 0 -18 M68 -74 q-6 -10 2 -20" fill="none" stroke="#f4f4f0" stroke-width="2.4" opacity=".75"/>')
    b += '<ellipse cx="840" cy="1764" rx="70" ry="10" fill="#000" opacity=".3"/><path d="M790 1764 L800 1700 L880 1700 L890 1764Z" fill="#b8603a" stroke="#2a120a" stroke-width="5"/>'
    b += '<path d="M840 1700 q-50 -60 -30 -110 M840 1700 q40 -70 30 -120 M840 1700 q0 -60 6 -90" stroke="#2f6a3a" stroke-width="6" fill="none"/>'
    for lx, ly, a in ((810, 1590, -30), (870, 1580, 30), (846, 1610, 0)):
        b += f'<path transform="translate({lx} {ly}) rotate({a})" d="M0 0 q16 -24 0 -50 q-16 26 0 50z" fill="#4f8a3e" stroke="#0e2a1c" stroke-width="3"/>'
    b += frog(250, 1786, 3.2, look=(3, -5), mouth='o', shadow=True, front=mug, armR='M38 -22 q14 -4 14 -32', armL='M-34 -22 q-14 6 -16 22')
    b += f'<rect width="{W}" height="{H}" fill="url(#vig)"/>'
    save(5, '#060c24', d, b, [('A LIVING', 160, 'w'), ('DINOSAUR', 200, 'y')], '#040a14')


if __name__ == '__main__':
    for n in (sys.argv[1:] or '12345'):
        globals()[f'make_{n}']()
        print('wrote short', n)
