# Shorts thumbnails (style B, guideline 16-9) for tromelin-sandbank-short1..5. VERTICAL 1080x1920, glow hero top half, hook centred y 860-1240, frog bottom corner.
# Run: python3 videos/tromelin-sandbank-short1/thumb/make_all.py [1 2 3 4 5] -> videos/tromelin-sandbank-shortN/thumb/A.html
# Ad-friendly: no people, no chains, no water peril; the ship / boat / sail / fire / lantern stand in for the story (metaphor).
# 1 THE HIDDEN REEF     Utile aground on a glowing coral reef at night, lightning, surf; frog sailor with lantern (short1 S10-S11: reef nobody knew was there)
# 2 TOO SMALL FOR EVERYONE  the little Providence on moonlit sand beside the dark ribs of the wreck; frog carpenter with hammer (short2 S12-S14)
# 3 NEVER CAME BACK     a lone sail shrinking into a huge sunset on an empty horizon, footprints at the waterline; frog with spyglass (short3 S04, S11)
# 4 15 YEARS OF FIRE    one big flame inside low sandstone/coral walls on a flat sand island at night; frog with driftwood (short4 S05-S06, S11)
# 5 A SAIL AT LAST      the corvette La Dauphine, lanterns lit, coming in at dawn; frog cheering on the beach (short5 S01-S02)
import os, sys, math, random, shutil
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
sys.path.insert(0, os.path.join(REPO, 'tools'))
sys.path.insert(0, os.path.join(REPO, 'videos', 'trilobite-extinction', 'thumb'))
from make import frog, FILTERS, INK, GREEN   # shared posable frog (eye white #f4f5ea r13.5, pupil r4.4 at +1+look)
from thumb_lib import vpage, vsvg, lin, rad, spark, fireflies, halo, darkband

W, H = 1080, 1920
Y = '<span class="g">%s</span>'


def vig(id='vig', a=.75):
    return rad(id, 540, 960, 1250, [(0, '#000', 0), (.5, '#000', 0), (1, '#000', a)])


def stars(rnd, n, y1, col='#eaf4ff'):
    return ''.join(f'<circle cx="{rnd.uniform(0, W):.0f}" cy="{rnd.uniform(20, y1):.0f}" r="{rnd.choice([1.2, 1.8, 2.5])}" fill="{col}" opacity="{rnd.uniform(.25, .9):.2f}"/>' for _ in range(n))


def save(n, bg, d, b, lines, outline, top):
    out = os.path.join(REPO, 'videos', f'tromelin-sandbank-short{n}', 'thumb'); os.makedirs(out, exist_ok=True)
    for f in ('common.css', 'Fredoka-700.woff2'):
        shutil.copy(os.path.join(REPO, 'tools', 'assets', 'thumb_v', f), out)
    open(os.path.join(out, 'A.html'), 'w').write(vpage(bg, vsvg(d, b), lines, outline=outline, top=top))


def ship(x, y, s, rot=0, wreck=False, hull='#3a2414', hull2='#5e3a1e', sail='#f4ead0', edge='#ffe9b0', lanterns=False, flip=False):
    """18th-c. three-masted ship, side view, bow to the right (flip for left). Origin = waterline centre."""
    sx = -s if flip else s
    g = f'<g transform="translate({x} {y}) rotate({rot}) scale({sx} {s})" stroke="#120a06" stroke-linejoin="round" stroke-linecap="round">'
    masts = ((-150, 330), (20, 400), (175, 310))
    if wreck:
        masts = ((-150, 330), (20, 190), (175, 300))
    # rigging behind
    for mx, mh in masts:
        g += f'<path d="M{mx} {-mh + 10} L-300 -60 M{mx} {-mh + 10} L330 -50" stroke="#2a1a10" stroke-width="2" opacity=".5" fill="none"/>'
    g += '<path d="M175 -300 L380 -70" stroke="#2a1a10" stroke-width="3" fill="none"/>'
    # masts + square sails
    for k, (mx, mh) in enumerate(masts):
        g += f'<path d="M{mx} -40 L{mx} {-mh}" stroke-width="13"/><path d="M{mx} -40 L{mx} {-mh}" stroke="#7a4e28" stroke-width="7"/>'
        rows = 3 if mh > 250 else 1
        for r in range(rows):
            top = -mh + 30 + r * (mh - 90) / rows; h = (mh - 110) / rows; wdt = 120 - r * -14 - (20 if k == 2 else 0)
            yb = top + h
            if wreck and (k + r) % 2 == 0:   # torn: jagged lower edge, hanging slack
                d = f'M{mx - wdt / 2} {top} L{mx + wdt / 2} {top} L{mx + wdt / 2 - 6} {yb - 10} L{mx + 20} {yb - 34} L{mx + 6} {yb + 6} L{mx - 18} {yb - 26} L{mx - wdt / 2 + 4} {yb}Z'
            else:
                d = f'M{mx - wdt / 2} {top} Q{mx} {top - 10} {mx + wdt / 2} {top} Q{mx + wdt / 2 + 14} {top + h / 2} {mx + wdt / 2} {yb} Q{mx} {yb + 14} {mx - wdt / 2} {yb} Q{mx - wdt / 2 + 10} {top + h / 2} {mx - wdt / 2} {top}Z'
            g += f'<path d="M{mx - wdt / 2 - 6} {top} L{mx + wdt / 2 + 6} {top}" stroke-width="6"/>'
            g += f'<path d="{d}" fill="{sail}" stroke-width="4"/>'
            g += f'<path d="M{mx + wdt / 2 - 14} {top + 8} Q{mx + wdt / 2} {top + h / 2} {mx + wdt / 2 - 12} {yb - 8}" fill="none" stroke="{edge}" stroke-width="4" opacity=".8"/>'
    if wreck:   # broken top of the main mast hanging over the side
        g += '<path d="M20 -190 L120 -330" stroke-width="12"/><path d="M20 -190 L120 -330" stroke="#7a4e28" stroke-width="6"/>'
        g += '<path d="M60 -250 L150 -230 L170 -300 L110 -320Z" fill="' + sail + '" stroke-width="4" opacity=".9"/>'
    # jib
    g += f'<path d="M180 -290 L370 -72 L200 -70Z" fill="{sail}" stroke-width="4"/>'
    # hull
    hp = 'M-300 -70 L-280 -10 Q-250 70 -170 92 L190 92 Q290 70 340 -50 L330 -62 L-300 -70Z'
    g += f'<path d="{hp}" fill="{hull}" stroke-width="6"/>'
    g += '<path d="M-292 -46 L336 -38" stroke="' + hull2 + '" stroke-width="16" fill="none"/>'
    g += '<path d="M-292 -46 L336 -38" stroke="#c89a4a" stroke-width="3" fill="none" opacity=".9"/>'
    for k in range(9):
        g += f'<rect x="{-230 + k * 58}" y="-36" width="18" height="16" rx="3" fill="{"#ffcf6a" if lanterns else "#1a0e08"}" stroke-width="3"/>'
    for yy in (8, 40, 70):
        g += f'<path d="M{-270 + yy * .5} {yy} L{300 - yy * .6} {yy}" stroke="#20120a" stroke-width="3" fill="none" opacity=".7"/>'
    g += '<path d="M-300 -70 L-330 -110 L-300 -112 L-290 -70Z" fill="' + hull2 + '" stroke-width="4"/>'   # stern
    g += '<path d="M330 -62 L410 -84" stroke-width="10"/><path d="M330 -62 L410 -84" stroke="#7a4e28" stroke-width="5"/>'   # bowsprit
    g += '<path d="M-280 -66 L330 -58" stroke="' + edge + '" stroke-width="3" fill="none" opacity=".75"/>'   # moonlit rail
    if lanterns:
        for lx, ly in ((-312, -120), (404, -90), (20, -410)):
            g += f'<circle cx="{lx}" cy="{ly}" r="40" fill="#ffd27a" opacity=".55" filter="url(#b12)" stroke="none"/><circle cx="{lx}" cy="{ly}" r="11" fill="#fff6c8" stroke-width="3"/>'
    return g + '</g>'


def surf(rnd, x0, x1, y, n, col='#e8fff8', op=.8, k=.5):
    o = ''
    for _ in range(n):
        x = rnd.uniform(x0, x1); r = rnd.uniform(14, 34) * k
        o += f'<circle cx="{x:.0f}" cy="{y + rnd.uniform(-20, 12):.0f}" r="{r:.0f}" fill="{col}" opacity="{op * rnd.uniform(.5, 1):.2f}"/>'
    return o


def lantern(x, y, s=1):
    return (f'<g transform="translate({x} {y}) scale({s})" stroke="{INK}" stroke-width="3">'
            '<circle cx="0" cy="8" r="34" fill="#ffd27a" opacity=".55" filter="url(#b12)" stroke="none"/>'
            '<path d="M-8 -22 q8 -10 16 0" fill="none"/><rect x="-13" y="-14" width="26" height="6" rx="2" fill="#5a3a1a"/>'
            '<rect x="-11" y="-8" width="22" height="28" rx="5" fill="#fff0b0"/><rect x="-13" y="20" width="26" height="6" rx="2" fill="#5a3a1a"/>'
            '<path d="M0 10 q-5 -6 0 -13 q5 7 0 13z" fill="#ff9a2a" stroke="none"/></g>')


# ================= 1: THE HIDDEN REEF =================
def make_1():
    rnd = random.Random(101)
    HZ = 700
    d = FILTERS + lin('sky1', [(0, '#05061a'), (.5, '#1a1a46'), (1, '#2e3a6a')]) + lin('sea1', [(0, '#123a52'), (.3, '#08202e'), (1, '#02080e')]) + vig()
    d += halo('h1', 540, 560, 560, inner='#f0fbff', outer='#5ad8ff')
    d += rad('coral1', 540, 760, 560, [(0, '#7affe0', .9), (.5, '#20c8b0', .4), (1, '#20c8b0', 0)])
    b = f'<rect width="{W}" height="{HZ + 20}" fill="url(#sky1)"/>' + stars(rnd, 60, 400)
    # storm clouds
    for cx, cy, rx, ry, col in ((180, 170, 300, 90, '#20244a'), (820, 140, 340, 100, '#1c2044'), (520, 90, 360, 80, '#262a56'), (980, 300, 220, 70, '#1a1e3e')):
        b += f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="{col}" opacity=".95"/>'
    b += '<ellipse cx="220" cy="210" rx="260" ry="50" fill="#6a78c8" opacity=".35" filter="url(#b24)"/>'
    bolt = 'M190 150 L150 280 L196 284 L120 450 L240 262 L192 258 L236 150Z'
    b += f'<path d="{bolt}" fill="#e8f0ff" opacity=".8" filter="url(#b12)"/><path d="{bolt}" fill="#fbfdff"/>'
    b += '<path d="M150 280 L90 340 M200 360 L250 400" stroke="#dfe8ff" stroke-width="4" opacity=".7"/>'
    b += f'<ellipse cx="540" cy="560" rx="600" ry="520" fill="url(#h1)" opacity=".75"/>'
    b += f'<rect y="{HZ}" width="{W}" height="{H - HZ}" fill="url(#sea1)"/>'
    for _ in range(40):
        yy = rnd.uniform(HZ + 10, 1850)
        b += f'<path d="M{rnd.uniform(-40, 1080):.0f} {yy:.0f} q30 -12 60 0 q30 12 60 0" fill="none" stroke="#7fe0ff" stroke-width="{2 + (yy - HZ) / 500:.1f}" opacity=".18"/>'
    # glowing reef ring at the waterline
    b += '<ellipse cx="540" cy="760" rx="620" ry="140" fill="url(#coral1)"/>'
    for _ in range(26):
        x = rnd.uniform(40, 1040); yy = 740 + rnd.uniform(-20, 50); s = rnd.uniform(18, 40)
        col = rnd.choice(['#5affd8', '#ff8ac8', '#ffd86a', '#7ad8ff'])
        b += f'<path d="M{x:.0f} {yy:.0f} q{-s * .6:.0f} {-s:.0f} {-s * .2:.0f} {-s * 1.6:.0f} M{x:.0f} {yy:.0f} q{s * .1:.0f} {-s * 1.2:.0f} {s * .5:.0f} {-s * 1.8:.0f} M{x:.0f} {yy:.0f} q{s * .7:.0f} {-s * .6:.0f} {s:.0f} {-s * 1.2:.0f}" stroke="{col}" stroke-width="8" fill="none" stroke-linecap="round" opacity=".85"/>'
    b += ship(530, 700, 1.05, rot=-11, wreck=True, sail='#e8eef4', edge='#bfefff')
    b += surf(rnd, 200, 900, 800, 16, op=.55)
    b += '<path d="M60 744 q120 -40 240 0 q120 40 240 0 q120 -40 240 0 q120 40 240 0" fill="none" stroke="#f4fffc" stroke-width="7" opacity=".85"/>'
    for sx, sy, ss in ((880, 380, 22), (120, 560, 16), (960, 640, 18), (660, 220, 16)):
        b += spark(sx, sy, ss, col='#f0fbff')
    b += fireflies(40, 180, 1820, col='#8af0ff', core='#efffff', seed=1)
    b += darkband(860, 1240, .55)
    # foreground coral below the text
    for _ in range(18):
        x = rnd.uniform(520, 1060); yy = rnd.uniform(1560, 1820); s = rnd.uniform(30, 60)
        col = rnd.choice(['#2ac8a8', '#ff6ab0', '#ffc84a'])
        b += f'<path d="M{x:.0f} {yy:.0f} q{-s * .6:.0f} {-s:.0f} {-s * .2:.0f} {-s * 1.6:.0f} M{x:.0f} {yy:.0f} q{s * .1:.0f} {-s * 1.2:.0f} {s * .5:.0f} {-s * 1.8:.0f} M{x:.0f} {yy:.0f} q{s * .7:.0f} {-s * .6:.0f} {s:.0f} {-s * 1.2:.0f}" stroke="{col}" stroke-width="12" fill="none" stroke-linecap="round" opacity=".75"/>'
    b += '<path d="M20 1800 q40 -110 250 -120 q210 0 250 120z" fill="#24343e" stroke="#0a1418" stroke-width="5"/>'
    b += '<ellipse cx="270" cy="1580" rx="240" ry="200" fill="#8af0ff" opacity=".14" filter="url(#b24)"/>'
    cap = ('<path d="M-28 -84 q34 -30 70 0z" fill="#1e2e5a" stroke-width="3.4"/><path d="M-34 -84 q40 -8 82 0 q-40 8 -82 0z" fill="#2a3e78" stroke-width="3.2"/>'
           '<circle cx="7" cy="-92" r="5" fill="#f2d27a" stroke-width="2"/>')
    b += frog(270, 1790, 3.3, look=(3, -4), mouth='O', mid=cap, armR='M38 -22 q24 -6 30 -40', armL='M-34 -22 q-14 6 -16 22')
    b += lantern(270 + 3.3 * 68, 1790 - 3.3 * 82, 1.6)
    b += f'<rect width="{W}" height="{H}" fill="url(#vig)"/>'
    save(1, '#03050e', d, b, [('THE HIDDEN', 140, 'w'), ('REEF', 250, 'y')], '#03060e', 872)


# ================= 2: TOO SMALL FOR EVERYONE =================
def make_2():
    rnd = random.Random(202)
    HZ = 560
    d = FILTERS + lin('sky2', [(0, '#040a1e'), (.6, '#0e2a4a'), (1, '#1e5068')]) + lin('sea2', [(0, '#1e5a6a'), (1, '#05141c')])
    d += lin('sand2', [(0, '#d8cfae'), (.4, '#8a8470'), (1, '#1a1a1a')]) + vig()
    d += halo('h2', 560, 600, 520, inner='#fff3c8', outer='#ffb85a')
    d += rad('moon2', 860, 190, 360, [(0, '#f4fbff', .9), (.3, '#a8d8ff', .35), (1, '#a8d8ff', 0)])
    b = f'<rect width="{W}" height="{H}" fill="url(#sky2)"/>' + stars(rnd, 90, HZ - 40)
    b += f'<rect width="{W}" height="{H}" fill="url(#moon2)"/><circle cx="860" cy="190" r="72" fill="#f6fbff"/><circle cx="840" cy="176" r="14" fill="#d4e4ee"/>'
    b += f'<rect y="{HZ}" width="{W}" height="300" fill="url(#sea2)"/><path d="M0 {HZ} L{W} {HZ}" stroke="#cfefff" stroke-width="3" opacity=".7"/>'
    b += f'<rect x="800" y="{HZ}" width="120" height="180" fill="#dff4ff" opacity=".18" filter="url(#b12)"/>'
    b += f'<path d="M0 640 Q300 600 560 610 Q820 600 1080 650 L1080 {H} L0 {H}Z" fill="url(#sand2)"/>'
    b += '<path d="M0 640 Q300 600 560 610 Q820 600 1080 650" fill="none" stroke="#f4fffa" stroke-width="6" opacity=".7"/>'
    # wreck ribs (the Utile) dark on the left, half sunk in sand
    for k in range(7):
        x = 40 + k * 46
        b += f'<path d="M{x} 680 Q{x - 30 + k * 4} {520 - k * 6} {x + 20 + k * 6} {420 + k * 8}" fill="none" stroke="#0e0a08" stroke-width="22" stroke-linecap="round"/>'
        b += f'<path d="M{x} 680 Q{x - 30 + k * 4} {520 - k * 6} {x + 20 + k * 6} {420 + k * 8}" fill="none" stroke="#3a2a1e" stroke-width="10" stroke-linecap="round"/>'
    b += '<path d="M20 676 L360 690" stroke="#0e0a08" stroke-width="26" stroke-linecap="round"/>'
    b += f'<ellipse cx="560" cy="600" rx="560" ry="460" fill="url(#h2)"/>'
    # the Providence: small single-mast boat on the sand, planks + nails glowing
    BX, BY = 600, 720
    g = f'<g transform="translate({BX} {BY})" stroke="#140a04" stroke-linejoin="round" stroke-linecap="round">'
    g += '<ellipse cx="0" cy="34" rx="300" ry="26" fill="#000" opacity=".35" stroke="none"/>'
    g += '<path d="M0 -40 L0 -470" stroke-width="16"/><path d="M0 -40 L0 -470" stroke="#9a6a34" stroke-width="8"/>'
    g += '<path d="M-6 -450 L-200 -60" stroke="#3a2a1e" stroke-width="3"/><path d="M6 -450 L250 -50" stroke="#3a2a1e" stroke-width="3"/>'
    g += '<path d="M8 -440 Q130 -300 190 -90 L8 -90Z" fill="#f4ead0" stroke-width="5"/><path d="M20 -420 Q130 -290 176 -104" fill="none" stroke="#fff6d8" stroke-width="5" opacity=".9"/>'
    g += '<path d="M-8 -400 Q-90 -260 -150 -96 L-8 -96Z" fill="#e8dcc0" stroke-width="5"/>'
    for yy, c in ((-60, '#8a5a2a'), (-30, '#a8743a'), (0, '#7a4a22')):
        g += f'<path d="M{-270 + (yy + 60) * .8} {yy} L{270 - (yy + 60) * .5} {yy}" stroke-width="34"/><path d="M{-270 + (yy + 60) * .8} {yy} L{270 - (yy + 60) * .5} {yy}" stroke="{c}" stroke-width="26"/>'
    g += '<path d="M-270 -60 Q-300 -86 -312 -110" stroke-width="16" fill="none"/><path d="M-270 -60 Q-300 -86 -312 -110" stroke="#a8743a" stroke-width="9" fill="none"/>'
    g += '<path d="M270 -60 Q300 -90 300 -126" stroke-width="16" fill="none"/><path d="M270 -60 Q300 -90 300 -126" stroke="#a8743a" stroke-width="9" fill="none"/>'
    g += '<path d="M-262 -74 L268 -74" stroke="#ffd88a" stroke-width="4" opacity=".9"/>'
    for k in range(12):
        g += f'<circle cx="{-230 + k * 40}" cy="{-44 + (k % 2) * 30}" r="4" fill="#ffe8a8" stroke="none"/>'
    g += '</g>'
    b += g
    b += lantern(BX + 6, BY - 300, 1.8)
    b += f'<text x="{BX - 120}" y="{BY - 6}" font-family="Fredoka" font-weight="700" font-size="34" fill="#3a2006" opacity=".85">PROVIDENCE</text>'
    for sx, sy, ss in ((BX + 300, 340, 24), (BX - 250, 300, 18), (BX + 220, 160, 16), (BX - 60, 140, 18)):
        b += spark(sx, sy, ss, col='#fff6d6')
    b += fireflies(40, 150, 1820, col='#ffd88a', core='#fff8e0', seed=2)
    b += darkband(860, 1240, .55)
    # foreground sand: planks, nails, hammer, crab tracks
    for x, yy, a in ((640, 1560, -8), (820, 1650, 12), (700, 1740, 4)):
        b += f'<rect x="{x}" y="{yy}" width="260" height="34" rx="6" transform="rotate({a} {x} {yy})" fill="#8a5a2a" stroke="#140a04" stroke-width="5"/>'
    for _ in range(10):
        x, yy = rnd.uniform(580, 1040), rnd.uniform(1480, 1820)
        b += f'<path d="M{x:.0f} {yy:.0f} l18 -4" stroke="#c8ccd2" stroke-width="5" stroke-linecap="round"/>'
    b += '<ellipse cx="800" cy="1560" rx="260" ry="160" fill="#ffd88a" opacity=".10" filter="url(#b24)"/>'
    b += '<ellipse cx="270" cy="1600" rx="240" ry="200" fill="#ffd88a" opacity=".14" filter="url(#b24)"/>'
    hat = ('<path d="M-30 -84 q34 -40 72 0z" fill="#c8a060" stroke-width="3.4"/><path d="M-46 -82 q52 -12 102 0 q-52 10 -102 0z" fill="#b08848" stroke-width="3.2"/>'
           '<path d="M-26 -84 L40 -84" stroke="#7a3a2a" stroke-width="4"/>')
    hammer = ('<path d="M72 -62 L60 -128" stroke-width="9"/><path d="M72 -62 L60 -128" stroke="#a8743a" stroke-width="5"/>'
              '<rect x="42" y="-146" width="40" height="18" rx="4" transform="rotate(-8 62 -137)" fill="#9aa0a8" stroke-width="3.2"/>')
    b += frog(270, 1790, 3.3, look=(3, -4), mouth='O', mid=hat, front=hammer, armR='M38 -22 q24 -6 32 -40', armL='M-34 -22 q-14 6 -16 22')
    b += f'<rect width="{W}" height="{H}" fill="url(#vig)"/>'
    save(2, '#02060e', d, b, [('TOO ' + Y % 'SMALL', 168, 'w'), ('FOR EVERYONE', 124, 'w')], '#03060e', 900)


# ================= 3: NEVER CAME BACK =================
def make_3():
    rnd = random.Random(303)
    HZ = 700
    d = FILTERS + lin('sky3', [(0, '#0a0620'), (.45, '#3a1440'), (.8, '#b0402a'), (1, '#ff9a3a')]) + lin('sea3', [(0, '#7a2a20'), (.15, '#2a0e1e'), (1, '#05030a')]) + vig()
    d += halo('h3', 540, HZ, 620, inner='#fff2c0', outer='#ff7a3a')
    d += f'<clipPath id="above3"><rect width="{W}" height="{HZ}"/></clipPath>'
    b = f'<rect width="{W}" height="{HZ}" fill="url(#sky3)"/>' + stars(rnd, 50, 300, '#ffe8f0')
    for cx, cy, rx in ((200, 420, 260), (860, 360, 300), (560, 520, 380)):
        b += f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="22" fill="#ff8a5a" opacity=".35"/>'
    b += f'<ellipse cx="540" cy="{HZ}" rx="680" ry="560" fill="url(#h3)"/>'
    b += f'<g clip-path="url(#above3)"><circle cx="540" cy="{HZ + 40}" r="260" fill="#ffd27a" opacity=".6" filter="url(#b24)"/><circle cx="540" cy="{HZ + 40}" r="230" fill="#ffe7a0"/></g>'
    for k, yy in enumerate((HZ - 60, HZ - 110, HZ - 155)):
        b += f'<rect x="0" y="{yy}" width="{W}" height="{6 + k}" fill="#3a1430" opacity=".5"/>'
    b += f'<rect y="{HZ}" width="{W}" height="{H - HZ}" fill="url(#sea3)"/><path d="M0 {HZ} L{W} {HZ}" stroke="#ffe0a0" stroke-width="4"/>'
    for j in range(26):   # glitter path toward viewer
        yy = HZ + 10 + j * 22 + j * j * 1.4; w = 120 + j * 22
        b += f'<rect x="{540 - w / 2 + rnd.uniform(-20, 20):.0f}" y="{yy:.0f}" width="{w:.0f}" height="{3 + j * .4:.1f}" rx="2" fill="#ffd88a" opacity="{.8 - j * .025:.2f}"/>'
    # the lone sail in front of the sun (silhouette with a gold rim)
    SX, SY = 560, HZ - 4
    g = f'<g transform="translate({SX} {SY}) scale(1.25)" stroke="#1a0808" stroke-linejoin="round">'
    g += '<path d="M-70 -10 L70 -10 L54 8 L-58 8Z" fill="#1a0808"/>'
    g += '<path d="M0 -10 L0 -190" stroke-width="6"/><path d="M4 -180 Q66 -110 80 -18 L4 -18Z" fill="#2a0e12" stroke-width="3"/><path d="M-4 -160 Q-46 -100 -60 -20 L-4 -20Z" fill="#2a0e12" stroke-width="3"/>'
    g += '<path d="M8 -172 Q66 -110 76 -24" fill="none" stroke="#fff2b0" stroke-width="3" opacity=".9"/>'
    g += '</g>'
    b += g
    b += '<path d="M380 340 q20 -16 40 0 q20 -16 40 0" fill="none" stroke="#2a0e1e" stroke-width="5"/><path d="M700 300 q14 -12 28 0 q14 -12 28 0" fill="none" stroke="#2a0e1e" stroke-width="4"/>'
    for sx, sy, ss in ((360, 560, 18), (760, 500, 22), (860, 640, 14), (220, 640, 14)):
        b += spark(sx, sy, ss, col='#fff2c8')
    b += fireflies(30, 150, 1820, col='#ffc87a', core='#fff4d8', seed=3)
    b += darkband(860, 1240, .55)
    # foreground beach: wet sand edge, footprints to the water, shells
    b += '<path d="M0 1500 Q300 1440 600 1470 Q860 1490 1080 1430 L1080 1920 L0 1920Z" fill="#3a2a26"/>'
    b += '<path d="M0 1500 Q300 1440 600 1470 Q860 1490 1080 1430" fill="none" stroke="#ffd8a0" stroke-width="7" opacity=".75"/>'
    b += '<path d="M0 1520 Q300 1470 600 1494 Q860 1510 1080 1456" fill="none" stroke="#ffb07a" stroke-width="3" opacity=".4"/>'
    for k in range(7):
        x = 620 + k * 52 + (k % 2) * 20; yy = 1830 - k * 52
        b += f'<ellipse cx="{x}" cy="{yy}" rx="{14 - k}" ry="{24 - k * 1.6:.0f}" fill="#1a100e" opacity=".75"/>'
    b += '<ellipse cx="820" cy="1660" rx="300" ry="160" fill="#ffb07a" opacity=".08" filter="url(#b24)"/>'
    b += '<ellipse cx="800" cy="1620" rx="240" ry="200" fill="#ffc87a" opacity=".14" filter="url(#b24)"/>'
    scarf = '<path d="M-28 -30 q30 14 62 0 l4 12 q-34 14 -70 0z" fill="#3a6ab0" stroke-width="3"/>'
    scope = ('<path d="M-36 -64 L-110 -92" stroke-width="22"/><path d="M-36 -64 L-110 -92" stroke="#c8a04a" stroke-width="15"/>'
             '<path d="M-80 -80 L-110 -92" stroke="#8a6a2a" stroke-width="15"/><circle cx="-112" cy="-93" r="9" fill="#ffe8a0" stroke-width="3"/>')
    b += frog(800, 1800, 3.3, flip=True, look=(3, -4), mouth='m', mid=scarf, front='', armR='M38 -22 q22 -20 6 -64', armL='M-34 -22 q-14 6 -16 22')
    b += f'<rect width="{W}" height="{H}" fill="url(#vig)"/>'
    save(3, '#05030a', d, b, [(Y % 'NEVER', 236, 'w'), ('CAME BACK', 150, 'w')], '#06030a', 866)


# ================= 4: 15 YEARS OF FIRE =================
def make_4():
    rnd = random.Random(404)
    HZ = 690
    d = FILTERS + lin('sky4', [(0, '#03040e'), (.7, '#0e1430'), (1, '#24243e')]) + lin('sand4', [(0, '#8a6a4a'), (.3, '#3a2a20'), (1, '#0a0806')]) + vig()
    d += halo('h4', 540, 520, 600, inner='#fff2c0', outer='#ff7a2a')
    d += lin('fl', [(0, '#fff8d0'), (.4, '#ffd04a'), (1, '#ff5a1a')], x2=0, y2=1)
    b = f'<rect width="{W}" height="{HZ + 40}" fill="url(#sky4)"/>' + stars(rnd, 140, HZ - 60)
    b += f'<path d="M0 {HZ - 6} Q540 {HZ - 26} {W} {HZ - 6} L{W} {HZ + 10} L0 {HZ + 10}Z" fill="#0a1420"/>'
    b += f'<ellipse cx="540" cy="520" rx="640" ry="560" fill="url(#h4)"/>'
    b += f'<path d="M0 {HZ} Q540 {HZ - 40} {W} {HZ} L{W} {H} L0 {H}Z" fill="url(#sand4)"/>'
    # back wall: upright sandstone slabs topped with coral blocks
    def wall(y0, x0, x1, h, light):
        o = ''; x = x0
        while x < x1:
            w = rnd.uniform(58, 86); hh = h + rnd.uniform(-14, 10)
            o += f'<path d="M{x:.0f} {y0} L{x + 4:.0f} {y0 - hh:.0f} L{x + w - 6:.0f} {y0 - hh - 4:.0f} L{x + w:.0f} {y0}Z" fill="{light}" stroke="#1a0e08" stroke-width="5" stroke-linejoin="round"/>'
            o += f'<path d="M{x + 6:.0f} {y0 - hh + 10:.0f} L{x + w - 10:.0f} {y0 - hh + 6:.0f}" stroke="#ffe0a0" stroke-width="3" opacity=".6"/>'
            for j in range(2):
                o += f'<ellipse cx="{x + w * (.3 + j * .4):.0f}" cy="{y0 - hh - 10:.0f}" rx="{w * .22:.0f}" ry="14" fill="#e8d8c0" stroke="#1a0e08" stroke-width="4"/>'
                o += f'<circle cx="{x + w * (.3 + j * .4) - 4:.0f}" cy="{y0 - hh - 12:.0f}" r="2.5" fill="#8a7a6a"/>'
            x += w + 4
        return o
    b += wall(700, 80, 1000, 110, '#9a7650')
    # driftwood pile + flame
    FX, FY = 540, 790
    b += f'<ellipse cx="{FX}" cy="{FY - 200}" rx="420" ry="360" fill="#ffb04a" opacity=".35" filter="url(#b50)"/>'
    flame = (f'M{FX} {FY - 560} C{FX + 60} {FY - 440} {FX + 220} {FY - 340} {FX + 200} {FY - 170} C{FX + 190} {FY - 60} {FX + 110} {FY - 10} {FX} {FY - 10} '
             f'C{FX - 120} {FY - 10} {FX - 200} {FY - 70} {FX - 200} {FY - 180} C{FX - 200} {FY - 300} {FX - 110} {FY - 330} {FX - 90} {FY - 440} '
             f'C{FX - 50} {FY - 380} {FX - 40} {FY - 330} {FX - 20} {FY - 320} C{FX - 30} {FY - 420} {FX - 10} {FY - 480} {FX} {FY - 560}Z')
    b += f'<path d="{flame}" fill="#ff7a2a" opacity=".7" filter="url(#b12)"/>'
    b += f'<path d="{flame}" fill="url(#fl)" stroke="#5a1a06" stroke-width="5"/>'
    inner = (f'M{FX + 10} {FY - 330} C{FX + 60} {FY - 250} {FX + 110} {FY - 190} {FX + 90} {FY - 110} C{FX + 80} {FY - 50} {FX + 40} {FY - 30} {FX} {FY - 30} '
             f'C{FX - 60} {FY - 30} {FX - 100} {FY - 70} {FX - 90} {FY - 130} C{FX - 80} {FY - 200} {FX - 20} {FY - 230} {FX + 10} {FY - 330}Z')
    b += f'<path d="{inner}" fill="#fffbe0"/>'
    for a, L in ((-14, 260), (14, 260), (-40, 200), (40, 210), (0, 180)):
        r = math.radians(a)
        x0, y0 = FX - L * .5 * math.cos(r), FY - 20 - L * .5 * math.sin(r)
        x1, y1 = FX + L * .5 * math.cos(r), FY - 20 + L * .5 * math.sin(r)
        b += f'<path d="M{x0:.0f} {y0:.0f} L{x1:.0f} {y1:.0f}" stroke="#1a0e08" stroke-width="34" stroke-linecap="round"/><path d="M{x0:.0f} {y0:.0f} L{x1:.0f} {y1:.0f}" stroke="#8a6a50" stroke-width="22" stroke-linecap="round"/>'
        b += f'<path d="M{x0:.0f} {y0 - 6:.0f} L{x1:.0f} {y1 - 6:.0f}" stroke="#ffc87a" stroke-width="5" opacity=".7" stroke-linecap="round"/>'
    b += f'<ellipse cx="{FX}" cy="{FY - 10}" rx="160" ry="24" fill="#ffd04a" opacity=".6" filter="url(#b12)"/>'
    # embers rising
    for _ in range(36):
        x = FX + rnd.gauss(0, 140); yy = rnd.uniform(140, FY - 300)
        b += f'<circle cx="{x:.0f}" cy="{yy:.0f}" r="{rnd.choice([3, 4, 6])}" fill="#ffd27a" opacity="{rnd.uniform(.5, 1):.2f}"/>'
    for sx, sy, ss in ((FX + 300, 300, 22), (FX - 320, 360, 18), (FX + 220, 160, 16), (FX - 200, 180, 16)):
        b += spark(sx, sy, ss, col='#fff2c8')
    b += fireflies(26, 900, 1820, col='#ffb04a', core='#fff2c8', seed=4)
    b += darkband(860, 1240, .55)
    # foreground: front wall stub, driftwood bundle, shells
    b += wall(1720, 600, 1080, 120, '#6a5038')
    b += '<ellipse cx="270" cy="1600" rx="240" ry="200" fill="#ffb04a" opacity=".16" filter="url(#b24)"/>'
    bundle = ''.join(f'<path d="M-70 {-30 + k * 9} L60 {-48 + k * 9}" stroke-width="10"/><path d="M-70 {-30 + k * 9} L60 {-48 + k * 9}" stroke="#9a7a5a" stroke-width="6"/>' for k in range(3))
    bundle += ''
    head = '<path d="M-34 -80 q40 -30 80 0 q-40 -6 -80 0z" fill="#d8b070" stroke-width="3.2"/><path d="M-36 -82 l-8 18 M46 -82 l8 18" stroke-width="3"/>'
    b += frog(270, 1790, 3.3, look=(3, -4), mouth='m', mid=head, front=bundle, armR='M38 -22 q16 -2 20 -26', armL='M-34 -22 q-16 -2 -20 -20')
    b += f'<rect width="{W}" height="{H}" fill="url(#vig)"/>'
    save(4, '#03040a', d, b, [('15 YEARS', 172, 'w'), ('OF ' + Y % 'FIRE', 206, 'w')], '#060304', 872)


# ================= 5: A SAIL AT LAST =================
def make_5():
    rnd = random.Random(505)
    HZ = 760
    d = FILTERS + lin('sky5', [(0, '#060a24'), (.45, '#2a2058'), (.78, '#b0507a'), (1, '#ffc07a')]) + lin('sea5', [(0, '#c07a7a'), (.12, '#3a2a50'), (1, '#060814')]) + vig()
    d += halo('h5', 540, 520, 560, inner='#fff4d0', outer='#ffb070')
    b = f'<rect width="{W}" height="{HZ}" fill="url(#sky5)"/>' + stars(rnd, 70, 380)
    b += '<circle cx="860" cy="170" r="10" fill="#fff" opacity=".9"/>' + spark(860, 170, 34, col='#fffbe8')   # morning star
    for cx, cy, rx in ((240, 620, 280), (820, 590, 320), (520, 690, 400)):
        b += f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="20" fill="#ffb0a0" opacity=".35"/>'
    b += f'<ellipse cx="540" cy="520" rx="620" ry="540" fill="url(#h5)"/>'
    b += f'<rect y="{HZ}" width="{W}" height="{H - HZ}" fill="url(#sea5)"/><path d="M0 {HZ} L{W} {HZ}" stroke="#ffe0c0" stroke-width="4"/>'
    for j in range(16):
        yy = HZ + 14 + j * 18 + j * j; w = 200 + j * 30
        b += f'<rect x="{540 - w / 2 + rnd.uniform(-30, 30):.0f}" y="{yy:.0f}" width="{w:.0f}" height="3" rx="2" fill="#ffd8b0" opacity="{.6 - j * .03:.2f}"/>'
    b += ship(520, 790, 1.0, rot=-2, sail='#fff6e4', edge='#ffe0a0', lanterns=True, hull='#2a1a12')
    b += surf(rnd, 260, 880, 884, 10, '#fff0e0', .45)
    b += '<path d="M880 790 q40 -24 80 -6 q30 -10 60 4" fill="none" stroke="#fff4e8" stroke-width="7" opacity=".8"/>'   # bow wave
    for sx, sy, ss in ((900, 360, 22), (150, 300, 18), (980, 600, 16), (110, 560, 16)):
        b += spark(sx, sy, ss, col='#fff6e0')
    b += fireflies(34, 150, 1820, col='#ffd8a0', core='#fff8e8', seed=5)
    b += darkband(860, 1240, .55)
    # foreground: island beach, the well's stone rim and a smoking fire (life kept going), frog cheering
    b += '<path d="M0 1480 Q400 1430 700 1470 Q900 1500 1080 1460 L1080 1920 L0 1920Z" fill="#3a2e3a"/>'
    b += '<path d="M0 1480 Q400 1430 700 1470 Q900 1500 1080 1460" fill="none" stroke="#ffd8c0" stroke-width="7" opacity=".7"/>'
    b += '<ellipse cx="800" cy="1640" rx="120" ry="34" fill="#ffb04a" opacity=".5" filter="url(#b12)"/>'
    b += '<path d="M800 1630 q-30 -60 0 -110 q-20 50 20 70 q10 -30 0 -50 q40 40 -20 90z" fill="#ffc04a" stroke="#5a1a06" stroke-width="4"/>'
    b += '<path d="M800 1500 q-30 -60 10 -120 q-40 60 10 120" fill="none" stroke="#c8b8c8" stroke-width="10" opacity=".35"/>'
    b += '<path d="M740 1650 L860 1630 M750 1630 L860 1652" stroke="#1a0e08" stroke-width="18" stroke-linecap="round"/><path d="M740 1650 L860 1630 M750 1630 L860 1652" stroke="#8a6a50" stroke-width="10" stroke-linecap="round"/>'
    b += '<ellipse cx="270" cy="1600" rx="240" ry="200" fill="#ffd8a0" opacity=".16" filter="url(#b24)"/>'
    kerchief = '<path d="M-30 -84 q36 -34 74 0 q-36 8 -74 0z" fill="#e05a4a" stroke-width="3.2"/><path d="M42 -86 l14 -8 l-2 14z" fill="#e05a4a" stroke-width="2.6"/>'
    b += frog(270, 1790, 3.3, look=(3, -5), mouth='O', mid=kerchief, armR='M38 -22 q22 -10 26 -52', armL='M-34 -22 q-22 -10 -26 -52')
    b += f'<rect width="{W}" height="{H}" fill="url(#vig)"/>'
    save(5, '#060814', d, b, [('A ' + Y % 'SAIL', 230, 'w'), ('AT LAST', 160, 'w')], '#06040e', 866)


if __name__ == '__main__':
    which = sys.argv[1:] or ['1', '2', '3', '4', '5']
    for n in which:
        fn = globals().get(f'make_{n}')
        if fn: fn(); print('made', n)
