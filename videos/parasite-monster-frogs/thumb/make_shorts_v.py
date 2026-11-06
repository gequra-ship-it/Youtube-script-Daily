# VERTICAL shorts thumbnails (guideline 16-9, miya 2026-11-06 correction: 9:16 1080x1920, text centred) for parasite-monster-frogs-short1..5.
# Run: python3 videos/parasite-monster-frogs/thumb/make_shorts_v.py   then  SLUG=parasite-monster-frogs-shortN python3 tools/thumb_shot.py
# Same scene ideas as the old landscape make_shorts.py, redrawn for the tall frame: subject above the text band (~y 840-1240), scene + mascot below.
# short1 SHOULD NOT EXIST   dip net lifted over the marsh holds a glowing many-legged frog (sh1 S01-S03); mascot in field-trip hat
# short2 IT WAS A PARASITE  big magnifier shows cysts with worms inside; deformed frog + small snail below (sh2 S04-S06); mascot detective
# short3 TARGET: LEGS       fork-tailed cercariae swarm at a tadpole's limb buds in a crosshair, snail below (sh3 S04-S06); mascot diving helmet
# short4 IT STEERS THE FROG puppet stage: brainless flatworm works a frog marionette, heron painted on the backdrop (sh4 S04, S09); mascot in a seat
# short5 AN ALGAE BUFFET    fertilizer sack pours pellets in the rain, algae blanket, snails in napkin bibs graze (sh5 S02-S03); mascot with bib + fork
import os, sys, math, random, shutil
HERE = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(HERE, 'make.py')).read()
src = src[:src.index("for n, fn in (('A', thumb_A)")]
NS = {'__file__': os.path.join(HERE, 'make.py')}
exec(compile(src, 'make.py', 'exec'), NS)
globals().update({k: v for k, v in NS.items() if not k.startswith('__')})
from thumb_lib import vpage, vsvg, stars

W, H = 1080, 1920
SHELL = ('<radialGradient id="shellG" cx="-40" cy="-80" r="190" gradientUnits="userSpaceOnUse"><stop offset="0" stop-color="#f0a46a"/>'
         '<stop offset=".55" stop-color="#a2512c"/><stop offset="1" stop-color="#4a1d0e"/></radialGradient>')
TAD = ('<radialGradient id="tadG" cx="-30" cy="-30" r="120" gradientUnits="userSpaceOnUse"><stop offset="0" stop-color="#9a9a5a"/>'
       '<stop offset="1" stop-color="#4a4a26"/></radialGradient>')


def vig(id, a=.55):
    return rad(id, 540, 960, 1250, [(0, '#000', 0), (.6, '#000', 0), (1, '#000', a)])


def tband(id, y0, y1, a=.35):
    """soft dark band behind the text for readability"""
    return f'<rect x="-50" y="{y0}" width="1180" height="{y1 - y0}" fill="#000" opacity="{a}" filter="url(#b50)"/>'


def reeds(n, x0, x1, ybase, hmin, hmax, col, w=4, op=1):
    out = ''
    for _ in range(n):
        x = random.randint(x0, x1); h = random.randint(hmin, hmax); bend = random.randint(-30, 30)
        out += f'<path d="M{x} {ybase} q{bend / 3:.0f} {-h / 2:.0f} {bend} {-h}" stroke="{col}" stroke-width="{w}" fill="none" opacity="{op}" stroke-linecap="round"/>'
        if random.random() < .25:
            out += f'<ellipse cx="{x + bend}" cy="{ybase - h + 18}" rx="7" ry="22" fill="#6b4a2a" opacity="{op}"/>'
    return out


def lily(lx, ly, lr, col='#4f8a3e'):
    return f'<path d="M{lx} {ly} m{lr} 0 a{lr} {lr * .38:.0f} 0 1 1 -8 -10 l-{lr - 8} 10z" fill="{col}" stroke="#1d3a1c" stroke-width="3"/>'


# ======================= short1: the net =======================
def short1():
    random.seed(21)
    defs = FILTERS + lin('sky1', [(0, '#6fb8d0'), (.6, '#cfe9d8'), (1, '#f6efc4')])
    defs += lin('water1', [(0, '#6fae9a'), (.3, '#3f7f6c'), (1, '#0f2a24')])
    defs += rad('sun1', 540, 470, 620, [(0, '#fff6d0', .9), (.3, '#ffe9a0', .35), (1, '#ffe9a0', 0)])
    defs += lin('pole1', [(0, '#8a5a2e'), (.5, '#d9a066'), (1, '#6a3e1c')], x2=1, y2=0)
    defs += vig('vig1', .55)
    HZ = 700
    b = f'<rect width="{W}" height="{HZ}" fill="url(#sky1)"/>'
    for _ in range(7):
        b += f'<ellipse cx="{random.randint(0, 1080)}" cy="{random.randint(120, 420)}" rx="{random.randint(120, 240)}" ry="{random.randint(30, 60)}" fill="#ffffff" opacity=".55" filter="url(#b24)"/>'
    b += f'<rect width="{W}" height="{H}" fill="url(#sun1)"/>'
    b += f'<path d="M0 {HZ - 60} q200 -60 380 -20 q240 -60 420 -10 q160 -30 280 0 L{W} {HZ} L0 {HZ}z" fill="#6f9a62" opacity=".8"/>'
    b += f'<path d="M0 {HZ - 18} q300 -30 560 -6 q300 -20 520 4 L{W} {HZ} L0 {HZ}z" fill="#466e44"/>'
    b += reeds(60, 0, W, HZ + 4, 30, 90, '#3a5e36', 3)
    b += f'<rect y="{HZ}" width="{W}" height="{H - HZ}" fill="url(#water1)"/>'
    b += f'<path d="M0 {HZ} L{W} {HZ}" stroke="#fff6d0" stroke-width="4" opacity=".8"/>'
    for _ in range(50):
        y = random.randint(HZ + 10, 1880)
        b += f'<path d="M{random.randint(-40, 1080)} {y} l{random.randint(30, 50 + (y - HZ) // 8)} 0" stroke="#e6fff4" stroke-width="{2 + (y - HZ) / 600:.1f}" opacity=".28"/>'
    b += '<ellipse cx="540" cy="1380" rx="300" ry="90" fill="#fff2a8" opacity=".22" filter="url(#b50)"/>'   # reflection of the glow
    for lx, ly, lr in ((860, 1360, 78), (950, 1500, 60), (120, 1290, 54), (720, 1720, 96), (980, 1760, 70)):
        b += lily(lx, ly, lr)
    b += '<circle cx="880" cy="1336" r="20" fill="#f6c6d8" stroke="#6a2a40" stroke-width="3"/><circle cx="880" cy="1336" r="8" fill="#ffe08a"/>'
    # ripple rings where the drips fall
    for r in (50, 95, 150):
        b += f'<ellipse cx="540" cy="1310" rx="{r * 1.4:.0f}" ry="{r * .26:.0f}" fill="none" stroke="#e6fff4" stroke-width="3" opacity="{.7 - r / 260:.2f}"/>'
    # ---- the dip net, lifted high: pole from the top-right corner
    HX, HY, HRX, HRY = 540, 300, 350, 108
    b += f'<path d="M{HX + HRX - 24} {HY - 14} L1180 -60" stroke="#2a180a" stroke-width="44" stroke-linecap="round"/>'
    b += f'<path d="M{HX + HRX - 24} {HY - 14} L1180 -60" stroke="url(#pole1)" stroke-width="32" stroke-linecap="round"/>'
    b += f'<path d="M{HX + HRX - 12} {HY - 26} L1180 -70" stroke="#ffe0b0" stroke-width="5" opacity=".6"/>'
    bag = f'M{HX - HRX} {HY} C{HX - HRX + 10} {HY + 290} {HX - 150} {HY + 450} {HX} {HY + 450} C{HX + 160} {HY + 450} {HX + HRX - 10} {HY + 290} {HX + HRX} {HY} Z'
    defs += f'<clipPath id="bag1"><path d="{bag}"/></clipPath>'
    b += f'<ellipse cx="{HX}" cy="{HY + 200}" rx="470" ry="380" fill="#d8ffe0" opacity=".45" filter="url(#b50)"/>'   # halo
    b += f'<path d="{bag}" fill="#0f2a22" opacity=".35"/>'
    mesh = lambda off, col, op: (f'<g clip-path="url(#bag1)" stroke="{col}" stroke-width="2.6" opacity="{op}">' +
                                 ''.join(f'<path d="M{HX - 560 + off + k * 36} {HY - 40} l460 580 M{HX + 560 - off - k * 36} {HY - 40} l-460 580"/>' for k in range(-20, 34)) + '</g>')
    b += mesh(0, '#d8e6d0', .45)
    b += f'<path d="M{HX - HRX} {HY} A{HRX} {HRY} 0 0 1 {HX + HRX} {HY}" stroke="#1c2226" stroke-width="22" fill="none"/>'
    b += f'<path d="M{HX - HRX} {HY} A{HRX} {HRY} 0 0 1 {HX + HRX} {HY}" stroke="#8d98a0" stroke-width="13" fill="none"/>'
    b += monster(HX, HY + 360, 3.3, extra=4, mouth='smile', look=(-2, 2), glow='#fff2a8')
    b += mesh(20, '#f4fbf0', .36)
    b += f'<path d="{bag}" fill="none" stroke="#e8f2e0" stroke-width="4" opacity=".7"/>'
    b += f'<path d="M{HX - HRX} {HY} A{HRX} {HRY} 0 0 0 {HX + HRX} {HY}" stroke="#1c2226" stroke-width="26" fill="none"/>'
    b += f'<path d="M{HX - HRX} {HY} A{HRX} {HRY} 0 0 0 {HX + HRX} {HY}" stroke="#a9b4bc" stroke-width="16" fill="none"/>'
    b += f'<path d="M{HX - HRX + 40} {HY + 50} A{HRX} {HRY} 0 0 0 {HX + 130} {HY + HRY - 4}" stroke="#ffffff" stroke-width="5" fill="none" opacity=".8"/>'
    for dx, dy in ((HX - 40, HY + 480), (HX + 30, HY + 520), (HX - 10, HY + 590), (HX + 70, HY + 470), (HX - 100, HY + 460)):
        b += f'<path d="M{dx} {dy - 14} q9 14 0 21 q-9 -7 0 -21z" fill="#dff6ff" stroke="#2c5a6a" stroke-width="2.6"/>'
    for sx_, sy_, ss in ((HX - 400, HY + 40, 24), (HX + 420, HY + 230, 20), (HX - 380, HY + 380, 16), (HX + 150, HY - 110, 16)):
        b += spark(sx_, sy_, ss, col='#fffbe0')
    b += tband('t1', 860, 1240, .3)
    # mascot frog: field-trip bucket hat + backpack, on a mossy rock lower-left, looking up at the net
    b += '<path d="M40 1720 q14 -130 230 -140 q230 -6 260 140z" fill="#55604a" stroke="#1d2b1c" stroke-width="5"/>'
    b += '<path d="M90 1620 q90 -56 220 -46" stroke="#8fa070" stroke-width="7" fill="none" opacity=".7"/>'
    b += '<ellipse cx="290" cy="1724" rx="300" ry="26" fill="#000" opacity=".25" filter="url(#b12)"/>'
    back = '<rect x="-52" y="-58" width="34" height="52" rx="10" fill="#d9733a" stroke-width="3.2"/>'
    torso = '<path d="M-26 -40 q4 22 -2 40 M34 -40 q-4 22 2 40" stroke="#b5562a" stroke-width="6" fill="none"/>'
    hat = ('<path d="M-30 -84 q34 -48 70 0z" fill="#f2c94c" stroke-width="3.4"/>'
           '<path d="M-44 -82 q50 -14 98 0 q-50 10 -98 0z" fill="#e8b93a" stroke-width="3.4"/>')
    b += frog(290, 1600, 3.3, mouth='o', arms=('q-18 -6 -22 -30', 'q18 -6 22 -30'), look=(5, -6), back=back, torso=torso, head=hat, sweat=True)
    b += f'<rect width="{W}" height="{H}" fill="url(#vig1)"/>'
    lines = [('SHOULD NOT', 150, 'w'), ('EXIST', 250, 'y')]
    return vpage('#0f2a24', vsvg(defs, b), lines, outline='#0a1a16', top=870)


# ======================= short2: the magnifier =======================
def cyst(x, y, r, a=0):
    g = f'<g transform="translate({x} {y}) rotate({a})">'
    g += f'<circle r="{r * 1.35:.0f}" fill="#fff4c0" opacity=".35" filter="url(#b12)"/>'
    g += f'<circle r="{r}" fill="#f6efd6" fill-opacity=".75" stroke="{INK}" stroke-width="5"/>'
    g += f'<circle r="{r - 9}" fill="#fbe7d0" stroke="#c9b48a" stroke-width="4"/>'
    s = r / 50
    g += (f'<g transform="scale({s:.2f})" stroke="{INK}" stroke-linecap="round" stroke-linejoin="round">'
          '<path d="M-22 18 q-14 -30 8 -42 q26 -12 34 12 q6 22 -14 28 q-16 4 -18 -10" fill="none" stroke-width="15"/>'
          '<path d="M-22 18 q-14 -30 8 -42 q26 -12 34 12 q6 22 -14 28 q-16 4 -18 -10" fill="none" stroke="#f2a0a0" stroke-width="10"/>'
          '<circle cx="-20" cy="20" r="3" fill="' + INK + '" stroke="none"/><circle cx="-12" cy="22" r="3" fill="' + INK + '" stroke="none"/></g>')
    g += f'<path d="M{-r * .6:.0f} {-r * .55:.0f} q{r * .3:.0f} {-r * .3:.0f} {r * .7:.0f} {-r * .2:.0f}" stroke="#fff" stroke-width="5" fill="none" opacity=".8"/>'
    return g + '</g>'


def short2():
    random.seed(32)
    defs = FILTERS + SHELL + lin('sky2', [(0, '#1c2c40'), (.5, '#4a5f6e'), (1, '#c9a46a')])
    defs += lin('water2', [(0, '#3d5a52'), (.5, '#1c302b'), (1, '#0c1715')])
    defs += lin('brass', [(0, '#7a5414'), (.4, '#f2d27a'), (.6, '#fff0c0'), (1, '#6a4410')], x2=1, y2=1)
    defs += lin('woodH', [(0, '#5a2e14'), (.5, '#a8643a'), (1, '#4a2410')], x2=1, y2=0)
    defs += rad('lamp2', 540, 480, 640, [(0, '#fff2c0', .5), (.4, '#ffd98a', .16), (1, '#ffd98a', 0)])
    defs += rad('lamp2b', 620, 1560, 420, [(0, '#fff2c0', .35), (1, '#ffd98a', 0)])
    defs += vig('vig2', .6)
    HZ = 760
    b = f'<rect width="{W}" height="{HZ}" fill="url(#sky2)"/>'
    b += ''.join(f'<circle cx="{random.randint(10, 1070)}" cy="{random.randint(120, 520)}" r="{random.choice([1.3, 1.9, 2.6])}" fill="#e8f4ff" opacity="{.4 * random.random() + .15:.2f}"/>' for _ in range(50))
    b += f'<path d="M0 {HZ - 40} q260 -60 520 -20 q300 -60 560 -6 L{W} {HZ} L0 {HZ}z" fill="#2b3a34"/>'
    b += reeds(60, 0, W, HZ + 2, 40, 110, '#1e2b26', 4)
    b += f'<rect y="{HZ}" width="{W}" height="{H - HZ}" fill="url(#water2)"/>'
    for _ in range(30):
        b += f'<path d="M{random.randint(-40, 1080)} {random.randint(HZ + 10, 1400)} l{random.randint(40, 120)} 0" stroke="#c9a46a" stroke-width="2" opacity=".28"/>'
    b += f'<rect width="{W}" height="{H}" fill="url(#lamp2)"/>'
    # ---- the lens (top): magnified hip skin with cysts + worms
    LX, LY, LR = 540, 480, 300
    defs += f'<clipPath id="lens2"><circle cx="{LX}" cy="{LY}" r="{LR}"/></clipPath>'
    L = f'<g clip-path="url(#lens2)"><rect x="{LX - LR}" y="{LY - LR}" width="{2 * LR}" height="{2 * LR}" fill="#9cc26a"/>'
    L += f'<circle cx="{LX - 70}" cy="{LY - 100}" r="260" fill="#c4de8e" opacity=".6" filter="url(#b50)"/>'
    for _ in range(11):
        L += f'<ellipse cx="{random.randint(LX - LR, LX + LR)}" cy="{random.randint(LY - LR, LY + LR)}" rx="{random.randint(36, 62)}" ry="{random.randint(28, 48)}" fill="#3f5a26" stroke="#c9dd9a" stroke-width="3" opacity=".8"/>'
    for _ in range(80):
        L += f'<circle cx="{random.randint(LX - LR, LX + LR)}" cy="{random.randint(LY - LR, LY + LR)}" r="{random.choice([3, 4, 5])}" fill="#7a9a4a" opacity=".6"/>'
    for cx_, cy_, r, a in ((-80, -50, 76, 10), (100, -110, 60, -30), (70, 90, 80, 40), (-130, 130, 54, -10), (195, 25, 46, 80), (-10, 210, 44, 20), (-180, -180, 42, 60), (-200, 20, 40, -40)):
        L += cyst(LX + cx_, LY + cy_, r, a)
    L += f'<path d="M{LX - LR + 36} {LY - 70} a{LR - 36} {LR - 36} 0 0 1 {LR + 70} {-LR + 110}" stroke="#fff" stroke-width="26" fill="none" opacity=".28" stroke-linecap="round"/>'
    L += '</g>'
    b += f'<circle cx="{LX}" cy="{LY}" r="{LR + 70}" fill="#fff4c0" opacity=".25" filter="url(#b24)"/>'
    b += f'<circle cx="{LX + 16}" cy="{LY + 22}" r="{LR + 26}" fill="#000" opacity=".35" filter="url(#b12)"/>'
    # handle out to the right edge (stays above the text band)
    a = math.radians(38); hx0, hy0 = LX + (LR + 20) * math.cos(a), LY + (LR + 20) * math.sin(a)
    hx1, hy1 = 1160, hy0 + (1160 - hx0) * .42
    b += f'<path d="M{hx0:.0f} {hy0:.0f} L{hx1:.0f} {hy1:.0f}" stroke="#1a0e06" stroke-width="64" stroke-linecap="round"/>'
    b += f'<path d="M{hx0:.0f} {hy0:.0f} L{hx1:.0f} {hy1:.0f}" stroke="url(#woodH)" stroke-width="48" stroke-linecap="round"/>'
    b += f'<path d="M{hx0:.0f} {hy0 - 16:.0f} L{hx1:.0f} {hy1 - 16:.0f}" stroke="#e0a070" stroke-width="5" opacity=".6"/>'
    b += L
    b += f'<circle cx="{LX}" cy="{LY}" r="{LR + 16}" fill="none" stroke="#2a1a06" stroke-width="48"/>'
    b += f'<circle cx="{LX}" cy="{LY}" r="{LR + 16}" fill="none" stroke="url(#brass)" stroke-width="32"/>'
    b += f'<path d="M{LX - LR - 2} {LY - 80} a{LR + 16} {LR + 16} 0 0 1 {LR - 40} {-LR + 76}" stroke="#fffbe0" stroke-width="7" fill="none" opacity=".85"/>'
    for sx_, sy_, ss in ((LX + 380, LY - 250, 24), (LX - 400, LY - 200, 18), (LX - 420, LY + 160, 14)):
        b += spark(sx_, sy_, ss, col='#fff6d0')
    b += tband('t2', 860, 1220, .3)
    # ---- below: the deformed frog on the mud bank, hip circled (the lens view), a ramshorn snail clue
    b += '<path d="M-20 1920 L-20 1600 q120 -150 420 -180 q400 -30 620 60 q80 40 80 120 L1100 1920z" fill="#3e3222" stroke="#1a140c" stroke-width="5"/>'
    b += '<path d="M120 1560 q240 -110 600 -90" stroke="#6a5638" stroke-width="8" fill="none" opacity=".6"/>'
    b += f'<rect width="{W}" height="{H}" fill="url(#lamp2b)"/>'
    FX, FY = 700, 1640
    b += f'<ellipse cx="{FX}" cy="{FY + 10}" rx="260" ry="26" fill="#000" opacity=".35" filter="url(#b6)"/>'
    b += monster(FX, FY, 2.9, pick=[0, 1, 2, 3], mouth='flat', look=(-3, 1))
    b += f'<circle cx="{FX}" cy="{FY - 20}" r="130" fill="none" stroke="#F2D27A" stroke-width="7" stroke-dasharray="30 18" opacity=".9"/>'
    b += snail(990, 1500, .3)
    # mascot detective: deerstalker hat + cape, pointing up at the lens
    cape = ('<path d="M-36 -36 q40 18 82 0 l10 40 q-50 12 -102 0z" fill="#8a6a44" stroke-width="3.2"/>'
            '<path d="M-30 -20 l70 0 M-24 -6 l58 0" stroke="#5a4428" stroke-width="2.4" opacity=".7"/>')
    hat = ('<path d="M-30 -84 q36 -50 72 0 q-36 8 -72 0z" fill="#a7865a" stroke-width="3.4"/>'
           '<path d="M-42 -86 q-14 6 -10 -2 l20 -6z M54 -86 q14 6 10 -2 l-20 -6z" fill="#8a6a44" stroke-width="3"/>'
           '<path d="M-20 -94 l50 -8 M-14 -104 l38 -6" stroke="#6a4f30" stroke-width="2.6"/>')
    b += frog(165, 1690, 3.1, mouth='o', arms=('q-14 6 -16 22', 'q20 -14 22 -40'), look=(7, -5), torso=cape, head=hat)
    b += f'<rect width="{W}" height="{H}" fill="url(#vig2)"/>'
    lines = [('IT WAS A', 140, 'w'), ('PARASITE', 200, 'y')]
    return vpage('#0c1715', vsvg(defs, b), lines, outline='#081010', top=880)


# ======================= short3: target legs =======================
def short3():
    random.seed(43)
    defs = FILTERS + TAD + SHELL + lin('water3', [(0, '#3a958a'), (.4, '#174a46'), (1, '#071818')])
    defs += rad('glow3', 600, 600, 520, [(0, '#ffe9a0', .45), (.4, '#ffd36a', .15), (1, '#ffd36a', 0)])
    defs += rad('glow3b', 860, 1640, 300, [(0, '#cff6ff', .25), (1, '#cff6ff', 0)])
    defs += vig('vig3', .6)
    b = f'<rect width="{W}" height="{H}" fill="url(#water3)"/>'
    for k in range(7):
        x0 = 100 + k * 160
        b += f'<path d="M{x0} 0 L{x0 + 80} 0 L{x0 - 260} {H} L{x0 - 380} {H}z" fill="#d8fff0" opacity=".05"/>'
    b += f'<path d="M0 0 L{W} 0 L{W} 50 q-270 26 -540 0 q-270 -26 -540 0z" fill="#9fe0d0" opacity=".35"/>'
    for _ in range(120):
        b += f'<circle cx="{random.randint(0, W)}" cy="{random.randint(0, H)}" r="{random.choice([2, 3, 4])}" fill="#d8fff0" opacity="{random.uniform(.1, .4):.2f}"/>'
    # mud + weeds at the bottom
    b += f'<path d="M0 1680 q260 -50 540 -10 q300 40 540 -20 L{W} {H} L0 {H}z" fill="#0f241e"/>'
    for px in (40, 110, 960, 1030):
        for k in range(3):
            b += f'<path d="M{px + k * 16} 1720 q{-24 + k * 12} -180 {14 + k * 6} -{300 + k * 40}" stroke="#1f4a38" stroke-width="11" fill="none" opacity=".9"/>'
    b += f'<rect width="{W}" height="{H}" fill="url(#glow3)"/>'
    b += f'<rect width="{W}" height="{H}" fill="url(#glow3b)"/>'
    # the tadpole (top half), head left, tail off the right edge
    TX, TY, TS = 400, 470, 2.6
    b += tadpole(TX, TY, TS)
    BX, BY = TX + 68 * TS, TY + 48 * TS
    b += f'<circle cx="{BX}" cy="{BY}" r="128" fill="none" stroke="#F2D27A" stroke-width="22" opacity=".3" filter="url(#b6)"/>'
    b += f'<circle cx="{BX}" cy="{BY}" r="128" fill="none" stroke="#F2D27A" stroke-width="8" stroke-dasharray="46 22"/>'
    b += f'<circle cx="{BX}" cy="{BY}" r="186" fill="none" stroke="#ff7a5a" stroke-width="5" opacity=".85"/>'
    for a in (0, 90, 180, 270):
        ca, sa = math.cos(math.radians(a)), math.sin(math.radians(a))
        b += f'<path d="M{BX + ca * 150:.0f} {BY + sa * 150:.0f} L{BX + ca * 220:.0f} {BY + sa * 220:.0f}" stroke="#ff7a5a" stroke-width="9" stroke-linecap="round"/>'
    # the swarm of cercariae diving at the buds (stays above the text band)
    k = 0
    while k < 36:
        d = random.uniform(240, 640); ang = math.radians(random.uniform(-80, 260))
        x, y = BX + d * math.cos(ang), BY + d * math.sin(ang)
        if not (30 < x < 1050 and 170 < y < 820) or ((x - TX) / 270) ** 2 + ((y - TY) / 190) ** 2 < 1 or (x > TX + 150 and TY - 90 < y < TY + 60):
            continue
        k += 1
        head = math.degrees(math.atan2(BY - y, BX - x)); s = random.uniform(2.0, 3.3)
        tx, ty = x - math.cos(math.radians(head)) * 110, y - math.sin(math.radians(head)) * 110
        b += f'<path d="M{tx:.0f} {ty:.0f} L{x:.0f} {y:.0f}" stroke="#e9fbff" stroke-width="{s * 2.2:.1f}" opacity=".18" stroke-linecap="round"/>'
        b += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{s * 9:.0f}" fill="#cff6ff" opacity=".35" filter="url(#b6)"/>'
        b += cerc(x, y, head, s=s)
    for sx_, sy_, ss in ((BX + 230, BY - 200, 20), (BX - 250, BY + 180, 14), (900, 220, 16)):
        b += spark(sx_, sy_, ss, col='#fff6d0')
    b += tband('t3', 860, 1240, .32)
    # below: the ramshorn snail on the mud releasing more fork-tailed swimmers
    b += snail(860, 1630, .62)
    for k in range(9):
        x = 760 + random.randint(-150, 170); y = 1390 - random.randint(0, 80) + k * 4
        b += cerc(x, y, random.uniform(-150, -100), s=2.2)
    # mascot frog in a brass diving helmet on the mud, lower-left
    helmet = (f'<circle cx="6" cy="-56" r="58" fill="#bfe8ff" fill-opacity=".22" stroke="#b8862e" stroke-width="9"/>'
              f'<circle cx="6" cy="-56" r="58" fill="none" stroke="{INK}" stroke-width="2.4"/>'
              '<path d="M-36 -94 q20 -22 52 -18" stroke="#fff" stroke-width="5" fill="none" opacity=".7"/>'
              '<rect x="-34" y="-8" width="80" height="14" rx="6" fill="#b8862e" stroke-width="3"/>'
              '<circle cx="-22" cy="-1" r="3" fill="#ffe6a0" stroke="none"/><circle cx="34" cy="-1" r="3" fill="#ffe6a0" stroke="none"/>')
    b += frog(300, 1700, 3.2, mouth='o', arms=('q-18 -6 -22 -30', 'q18 -6 22 -30'), look=(7, -4), front=helmet)
    for k in range(4):
        b += f'<circle cx="{330 + k * 10 + random.randint(-8, 8)}" cy="{1330 - k * 30}" r="{6 + k}" fill="none" stroke="#e8fff8" stroke-width="3" opacity=".7"/>'
    b += f'<rect width="{W}" height="{H}" fill="url(#vig3)"/>'
    lines = [('TARGET:', 170, 'w'), ('LEGS', 270, 'y')]
    return vpage('#071818', vsvg(defs, b), lines, outline='#041010', top=850)


# ======================= short4: the puppet stage =======================
def flatworm(x, y, s):
    g = f'<g transform="translate({x} {y}) scale({s})" stroke="{INK}" stroke-linejoin="round" stroke-linecap="round">'
    g += '<path d="M-90 10 q-10 -40 30 -50 q50 -12 90 -4 q60 10 70 34 q4 24 -40 28 q-60 6 -110 4 q-36 -2 -40 -12z" fill="#f2b7a8" stroke-width="5"/>'
    g += '<path d="M-70 -10 q70 -20 150 0" stroke="#d98d7c" stroke-width="5" fill="none" opacity=".8"/>'
    g += '<path d="M60 -22 q20 -20 40 -4" fill="#f2b7a8" stroke-width="4"/>'
    g += f'<circle cx="64" cy="-12" r="6" fill="{INK}" stroke="none"/><circle cx="84" cy="-10" r="6" fill="{INK}" stroke="none"/>'
    g += '<circle cx="66" cy="-14" r="2" fill="#fff" stroke="none"/><circle cx="86" cy="-12" r="2" fill="#fff" stroke="none"/>'
    g += '<path d="M66 6 q10 8 22 0" fill="none" stroke-width="3.6"/>'
    return g + '</g>'


def short4():
    random.seed(54)
    defs = FILTERS + lin('drop4', [(0, '#f08a4a'), (.5, '#f8c27a'), (1, '#fde3a8')])
    defs += lin('curt', [(0, '#4a0c14'), (.3, '#b3242e'), (.55, '#e0444a'), (.8, '#8a1620'), (1, '#3a0810')], x2=1, y2=0)
    defs += lin('floor4', [(0, '#7a4a26'), (1, '#2a160a')])
    defs += rad('spot4', 540, 640, 460, [(0, '#fff6d0', .6), (.5, '#fff0c0', .2), (1, '#fff0c0', 0)])
    defs += lin('room4', [(0, '#1a1020'), (1, '#07060c')])
    defs += rad('spill4', 540, 900, 700, [(0, '#ffcf8a', .22), (1, '#ffcf8a', 0)])
    defs += vig('vig4', .55)
    b = f'<rect width="{W}" height="{H}" fill="url(#room4)"/>'
    SX0, SX1, ST, SF = 70, 1010, 150, 840
    # painted backdrop: sunset pond with a heron flying over it
    b += f'<rect x="{SX0}" y="{ST}" width="{SX1 - SX0}" height="{SF - ST}" fill="url(#drop4)"/>'
    b += '<circle cx="800" cy="560" r="80" fill="#fff4d0" opacity=".9"/>'
    b += f'<path d="M{SX0} 620 q200 -60 420 -20 q240 -50 520 0 L{SX1} {SF} L{SX0} {SF}z" fill="#7a8a52"/>'
    b += f'<path d="M{SX0} 680 L{SX1} 680 L{SX1} {SF} L{SX0} {SF}z" fill="#4f8a86"/>'
    b += f'<path d="M{SX0} 680 L{SX1} 680" stroke="#fff4d0" stroke-width="4" opacity=".7"/>'
    b += reeds(40, SX0, SX1, 684, 40, 110, '#3e5a30', 4)
    b += fly_heron(300, 470, .62, sil='#5a3a3a')
    b += f'<rect width="{W}" height="{H}" fill="url(#spot4)"/>'
    # stage floor + apron
    b += f'<path d="M{SX0 - 60} {SF} L{SX1 + 60} {SF} L{SX1 + 60} {SF + 50} L{SX0 - 60} {SF + 50}z" fill="url(#floor4)" stroke="#140a04" stroke-width="5"/>'
    for k in range(1, 9):
        b += f'<path d="M{SX0 - 60 + k * 120} {SF} l0 50" stroke="#3a2010" stroke-width="3"/>'
    b += f'<path d="M{SX0 - 60} {SF + 4} L{SX1 + 60} {SF + 4}" stroke="#e0a46a" stroke-width="4" opacity=".7"/>'
    b += f'<rect x="-20" y="{SF + 50}" width="1120" height="36" fill="#3a0c12" stroke="#140a04" stroke-width="4"/>'
    # marionette frog with tangled legs, hanging just above the floor
    FX, FY = 540, 745
    b += f'<ellipse cx="{FX}" cy="{SF + 6}" rx="250" ry="20" fill="#000" opacity=".35" filter="url(#b6)"/>'
    b += monster(FX, FY, 2.65, pick=[0, 1, 2, 3], mouth='flat', look=(1, -3))
    # control bar + strings
    CX, CY = 540, 380
    ends = [(CX - 230, CY), (CX + 230, CY), (CX, CY - 44), (CX, CY + 44)]
    targets = [(FX - 290, FY - 100), (FX + 300, FY - 90), (FX, FY - 190), (FX - 200, FY + 70), (FX + 210, FY + 70), (FX - 50, FY - 130), (FX + 70, FY - 130)]
    for k, (tx, ty) in enumerate(targets):
        ex, ey = (ends[0] if tx < FX - 100 else ends[1] if tx > FX + 100 else ends[2 + (k % 2)])
        b += f'<path d="M{ex} {ey} L{tx} {ty}" stroke="#fffbe8" stroke-width="3" opacity=".85"/>'
    b += f'<path d="M{CX - 240} {CY} L{CX + 240} {CY} M{CX} {CY - 54} L{CX} {CY + 54}" stroke="#2a1608" stroke-width="32" stroke-linecap="round"/>'
    b += f'<path d="M{CX - 240} {CY} L{CX + 240} {CY} M{CX} {CY - 54} L{CX} {CY + 54}" stroke="#c98a4a" stroke-width="21" stroke-linecap="round"/>'
    b += f'<path d="M{CX - 230} {CY - 5} L{CX + 230} {CY - 5}" stroke="#f0c080" stroke-width="4" opacity=".7"/>'
    # curtains + valance
    b += f'<path d="M-20 {ST} L{SX0 + 110} {ST} q-40 300 -10 460 q20 120 -40 {SF - ST - 460} L-20 {SF}z" fill="url(#curt)" stroke="#2a0408" stroke-width="5"/>'
    b += f'<path d="M1100 {ST} L{SX1 - 110} {ST} q40 300 10 460 q-20 120 40 {SF - ST - 460} L1100 {SF}z" fill="url(#curt)" stroke="#2a0408" stroke-width="5"/>'
    b += f'<path d="M-20 0 L1100 0 L1100 {ST + 80} q-112 50 -224 0 q-112 50 -224 0 q-112 50 -224 0 q-112 50 -224 0 q-112 50 -224 0 L-20 {ST + 80}z" fill="#a81e28" stroke="#2a0408" stroke-width="5"/>'
    b += f'<path d="M-20 {ST + 76} q112 50 224 0 q112 50 224 0 q112 50 224 0 q112 50 224 0 q112 50 224 0" stroke="#F2D27A" stroke-width="9" fill="none"/>'
    # the brainless flatworm puppeteer hangs under the valance, its tail curled round the bar
    b += f'<ellipse cx="{CX}" cy="{CY - 70}" rx="230" ry="90" fill="#fff0c0" opacity=".28" filter="url(#b24)"/>'
    b += f'<path d="M{CX - 70} {CY - 60} q-40 30 -10 60" stroke="{INK}" stroke-width="24" fill="none" stroke-linecap="round"/><path d="M{CX - 70} {CY - 60} q-40 30 -10 60" stroke="#f2b7a8" stroke-width="15" fill="none" stroke-linecap="round"/>'
    b += flatworm(CX + 10, CY - 74, 1.45)
    for sx_, sy_, ss in ((CX + 330, CY - 60, 20), (CX - 340, CY + 120, 14), (FX + 360, FY - 220, 16)):
        b += spark(sx_, sy_, ss, col='#fff6d0')
    b += f'<rect width="{W}" height="{H}" fill="url(#spill4)"/>'
    # auditorium: back row of seats + the mascot in a theatre seat with popcorn
    for k in range(5):
        x = 40 + k * 220
        b += f'<path d="M{x} 1920 L{x} 1560 q0 -36 36 -36 l140 0 q36 0 36 36 L{x + 212} 1920z" fill="#3a0c12" stroke="#12030a" stroke-width="4" opacity=".75"/>'
    b += '<path d="M150 1920 L150 1540 q0 -40 40 -40 l340 0 q40 0 40 40 L570 1920z" fill="#7a1820" stroke="#1a0408" stroke-width="5"/>'
    b += '<path d="M180 1550 q170 -30 360 0" stroke="#c0404a" stroke-width="6" fill="none" opacity=".6"/>'
    pop = ('<path d="M44 -10 l-6 -52 l52 0 l-6 52z" fill="#fff4e0" stroke-width="3.2"/>'
           '<path d="M42 -44 l4 34 M60 -60 l0 50 M78 -60 l-2 50" stroke="#d9454a" stroke-width="6"/>'
           '<circle cx="48" cy="-66" r="9" fill="#fff6c8" stroke-width="2.4"/><circle cx="64" cy="-72" r="10" fill="#fff6c8" stroke-width="2.4"/><circle cx="82" cy="-66" r="9" fill="#fff6c8" stroke-width="2.4"/>'
           '<circle cx="104" cy="-92" r="6" fill="#fff6c8" stroke-width="2"/>')
    b += frog(340, 1700, 3.2, mouth='o', arms=('q-18 -8 -22 -30', 'q12 8 20 14'), look=(4, -7), front=pop, sweat=True)
    b += f'<rect width="{W}" height="{H}" fill="url(#vig4)"/>'
    lines = [('IT', 130, 'w'), ('STEERS', 230, 'y'), ('THE FROG', 150, 'w')]
    return vpage('#07060c', vsvg(defs, b), lines, outline='#0a0408', top=920)


# ======================= short5: the algae buffet =======================
def short5():
    random.seed(65)
    defs = FILTERS + SHELL + lin('sky5', [(0, '#4d5a5e'), (.7, '#a9b4a8'), (1, '#c9d0b8')])
    defs += lin('water5', [(0, '#3f6e3e'), (.45, '#1f4026'), (1, '#0b1a10')])
    defs += lin('algae', [(0, '#c6f06a'), (.5, '#7fc93a'), (1, '#3f8a22')])
    defs += lin('sack', [(0, '#e0c088'), (1, '#9a7442')], x2=1, y2=0)
    defs += rad('glow5', 560, 1560, 520, [(0, '#e6ff9a', .35), (.4, '#b8f060', .12), (1, '#b8f060', 0)])
    defs += rad('glow5t', 520, 560, 420, [(0, '#eaffb0', .3), (1, '#eaffb0', 0)])
    defs += vig('vig5', .55)
    WL = 660
    b = f'<rect width="{W}" height="{WL}" fill="url(#sky5)"/>'
    for _ in range(9):
        b += f'<ellipse cx="{random.randint(0, 1080)}" cy="{random.randint(120, 300)}" rx="{random.randint(150, 280)}" ry="{random.randint(40, 80)}" fill="#3e484c" opacity=".55" filter="url(#b24)"/>'
    # far field + bank on the right with crop rows and the tipped sack
    b += f'<path d="M0 {WL - 30} q260 -40 560 -16 q300 -30 520 -6 L{W} {WL} L0 {WL}z" fill="#5f7a44"/>'
    b += f'<path d="M560 {WL + 10} q120 -150 300 -180 q160 -16 260 -6 L1100 {WL + 10}z" fill="#6a5a38" stroke="#2a2010" stroke-width="5"/>'
    for k in range(6):
        b += f'<path d="M{760 + k * 56} {WL - 150 + k * 4} q20 -30 6 -60" stroke="#5f8a3a" stroke-width="7" fill="none"/>'
    for _ in range(130):
        x = random.randint(0, 1140); y = random.randint(110, WL - 20)
        b += f'<path d="M{x} {y} l-14 34" stroke="#e8f2f4" stroke-width="2.4" opacity="{random.uniform(.25, .6):.2f}" stroke-linecap="round"/>'
    b += f'<rect width="{W}" height="{H}" fill="url(#glow5t)"/>'
    # fertilizer sack (no lettering) tipped toward the pond, pellets pouring down-left
    b += '<g transform="translate(830 400) rotate(-30) scale(1.35)">'
    b += '<path d="M-90 -110 q90 -20 180 0 l14 200 q-104 24 -208 0z" fill="url(#sack)" stroke="#3a2a10" stroke-width="6" stroke-linejoin="round"/>'
    b += '<path d="M-84 -80 l170 0" stroke="#7a5a2a" stroke-width="4" stroke-dasharray="10 8"/>'
    b += '<circle cx="2" cy="10" r="46" fill="#f6ecd0" stroke="#3a2a10" stroke-width="4"/>'
    b += '<path d="M-20 30 q0 -50 40 -50 q4 46 -40 50z M-20 30 q20 -20 34 -36" fill="#5aa040" stroke="#1d3a14" stroke-width="3.4"/>'
    b += '</g>'
    for k in range(80):
        t = random.random(); x = 700 - t * 330 + random.randint(-28, 28); y = 300 + t * t * 370 + random.randint(-14, 14)
        b += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{random.choice([6, 7, 8])}" fill="{random.choice(["#eaffb0", "#f6e6a0", "#d8f080"])}" stroke="#3a4a18" stroke-width="1.8"/>'
    # water
    b += f'<rect y="{WL}" width="{W}" height="{H - WL}" fill="url(#water5)"/>'
    for r in (40, 80, 130):
        b += f'<ellipse cx="400" cy="{WL + 2}" rx="{r * 1.4:.0f}" ry="{r * .2:.0f}" fill="none" stroke="#eaffb0" stroke-width="3" opacity="{.7 - r / 220:.2f}"/>'
    b += f'<rect width="{W}" height="{H}" fill="url(#glow5)"/>'
    # algae blanket on the surface + short hanging strands (stop above the text band)
    blanket = f'M-10 {WL - 8} L{W + 10} {WL - 8} L{W + 10} {WL + 60}'
    x = W + 10
    while x > -10:
        x2 = x - random.randint(50, 100)
        blanket += f' Q{(x + x2) / 2:.0f} {WL + random.randint(80, 130)} {x2} {WL + random.randint(40, 70)}'
        x = x2
    blanket += ' Z'
    b += f'<path d="{blanket}" fill="url(#algae)" stroke="#1d3a14" stroke-width="4"/>'
    for _ in range(70):
        b += f'<circle cx="{random.randint(0, W)}" cy="{random.randint(WL, WL + 60)}" r="{random.randint(6, 18)}" fill="#d8ff8a" opacity="{random.uniform(.3, .7):.2f}"/>'
    for _ in range(18):
        sx = random.randint(20, 1060); L = random.randint(60, 150)
        b += f'<path d="M{sx} {WL + 60} q{random.randint(-30, 30)} {L / 2:.0f} {random.randint(-20, 20)} {L}" stroke="#7fc93a" stroke-width="{random.randint(10, 16)}" fill="none" stroke-linecap="round" opacity=".85"/>'
    b += tband('t5', 860, 1220, .3)
    # bottom: mud with an algae carpet, rocks with algae; snails in napkin bibs grazing
    b += f'<path d="M-10 1700 q300 -60 560 -20 q300 40 540 -30 L{W + 10} {H} L-10 {H}z" fill="#18281a"/>'
    for _ in range(60):
        b += f'<ellipse cx="{random.randint(0, W)}" cy="{random.randint(1680, 1740)}" rx="{random.randint(14, 34)}" ry="{random.randint(6, 12)}" fill="#7fc93a" opacity="{random.uniform(.5, .9):.2f}"/>'
    for rx_, ry_, rr in ((330, 1440, 130), (920, 1450, 115)):
        b += f'<ellipse cx="{rx_}" cy="{ry_}" rx="{rr}" ry="{rr * .42:.0f}" fill="#3a4638" stroke="#141c14" stroke-width="5"/>'
        for _ in range(16):
            b += f'<circle cx="{rx_ + random.randint(-rr + 20, rr - 20)}" cy="{ry_ - rr * .3 + random.randint(-14, 10):.0f}" r="{random.randint(10, 20)}" fill="#8fd648" opacity=".9"/>'

    def bib(x, y, s):
        return (f'<g transform="translate({x} {y}) scale({s})"><path d="M-170 70 l-70 20 l40 60 z" fill="#ffffff" stroke="{INK}" stroke-width="4" stroke-linejoin="round"/>'
                f'<path d="M-205 98 l14 20 M-222 92 l26 40" stroke="#d9454a" stroke-width="4"/></g>')
    for sx_, sy_, ss in ((390, 1340, .38), (970, 1350, .36)):
        b += snail(sx_, sy_, ss) + bib(sx_, sy_, ss)
    b += f'<ellipse cx="720" cy="1580" rx="300" ry="200" fill="#e6ff9a" opacity=".2" filter="url(#b50)"/>'
    SX, SY, SS = 660, 1620, 1.2
    b += snail(SX, SY, SS) + bib(SX, SY, SS)
    b += f'<path d="M{SX - 214 * SS:.0f} {SY + 96 * SS - 6:.0f} q-30 30 -10 {1700 - SY - 96 * SS + 30:.0f}" stroke="#7fc93a" stroke-width="18" fill="none" stroke-linecap="round"/>'   # algae strand being slurped
    for sx_, sy_, ss in ((980, 1520, 18), (560, 1290, 14), (130, 1500, 14)):
        b += spark(sx_, sy_, ss, col='#f6ffd0')
    # mascot frog: buffet guest with napkin bib + fork, lower-left on the mud
    bibf = ('<path d="M-30 -36 q36 10 72 0 l-36 40z" fill="#ffffff" stroke-width="3.2"/>'
            '<path d="M-14 -30 l12 16 M26 -32 l-12 18" stroke="#d9454a" stroke-width="3"/>')
    fork = ('<path d="M58 -40 L58 -96" stroke-width="9"/><path d="M58 -40 L58 -96" stroke="#d8dde2" stroke-width="5"/>'
            '<path d="M48 -96 l0 -22 M58 -96 l0 -24 M68 -96 l0 -22 M46 -96 q12 8 24 0" stroke="#d8dde2" stroke-width="4" fill="none"/>'
            '<path d="M48 -96 l0 -22 M58 -96 l0 -24 M68 -96 l0 -22" stroke-width="1.4" fill="none"/>')
    b += frog(150, 1745, 3.0, mouth='o', arms=('q-18 -6 -22 -30', 'q14 -8 18 -30'), look=(8, -2), torso=bibf, front=fork)
    for k in range(5):
        b += f'<circle cx="{random.randint(60, 1020)}" cy="{random.randint(1270, 1320)}" r="{random.randint(6, 12)}" fill="none" stroke="#d8ffd0" stroke-width="3" opacity=".5"/>'
    b += f'<rect width="{W}" height="{H}" fill="url(#vig5)"/>'
    lines = [('AN ALGAE', 160, 'w'), ('BUFFET', 250, 'y')]
    return vpage('#0b1a10', vsvg(defs, b), lines, outline='#0a1406', top=860)


ROOT = os.path.dirname(os.path.dirname(HERE))   # videos/
TV = os.path.join(ROOT, '..', 'tools', 'assets', 'thumb_v')
for n, fn in enumerate((short1, short2, short3, short4, short5), 1):
    d = os.path.join(ROOT, f'parasite-monster-frogs-short{n}', 'thumb'); os.makedirs(d, exist_ok=True)
    for f in ('common.css', 'Fredoka-700.woff2'):
        shutil.copy(os.path.join(TV, f), d)
    open(os.path.join(d, 'A.html'), 'w').write(fn())
print('ok')
