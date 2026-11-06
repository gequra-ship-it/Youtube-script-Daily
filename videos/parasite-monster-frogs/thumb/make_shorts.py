# Shorts thumbnails (guideline 16-9) for parasite-monster-frogs-short1..5, one A.html each.
# Run from anywhere: python3 videos/parasite-monster-frogs/thumb/make_shorts.py   (reuses frog/monster/snail/... from make.py)
# short1 SHOULD NOT EXIST   intuitive: a dip net lifted from the marsh holds a glowing many-legged frog (sh1 S01-S03)
# short2 IT WAS A PARASITE  intuitive: detective magnifier over a deformed frog's hip shows cysts with worms inside (sh2 S05-S06)
# short3 TARGET: LEGS       intuitive: fork-tailed cercariae swarm at a tadpole's glowing limb buds inside a crosshair (sh3 S05-S06)
# short4 IT STEERS THE FROG intuitive: puppet stage, a brainless flatworm works a frog marionette with tangled legs (sh4 S09)
# short5 AN ALGAE BUFFET    intuitive: fertilizer pours into a rainy pond, snails in bibs feast on the algae blanket (sh5 S02-S03)
import os, sys, math, random, shutil
HERE = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(HERE, 'make.py')).read()
src = src[:src.index("for n, fn in (('A', thumb_A)")]
NS = {'__file__': os.path.join(HERE, 'make.py')}
exec(compile(src, 'make.py', 'exec'), NS)
globals().update({k: v for k, v in NS.items() if not k.startswith('__')})

from thumb_lib import stars
SHELL = ('<radialGradient id="shellG" cx="-40" cy="-80" r="190" gradientUnits="userSpaceOnUse"><stop offset="0" stop-color="#f0a46a"/>'
         '<stop offset=".55" stop-color="#a2512c"/><stop offset="1" stop-color="#4a1d0e"/></radialGradient>')
TAD = ('<radialGradient id="tadG" cx="-30" cy="-30" r="120" gradientUnits="userSpaceOnUse"><stop offset="0" stop-color="#9a9a5a"/>'
       '<stop offset="1" stop-color="#4a4a26"/></radialGradient>')


def vig(id, a=.55):
    return rad(id, 960, 540, 1150, [(0, '#000', 0), (.62, '#000', 0), (1, '#000', a)])


def reeds(n, x0, x1, ybase, hmin, hmax, col, w=4, op=1):
    out = ''
    for _ in range(n):
        x = random.randint(x0, x1); h = random.randint(hmin, hmax); bend = random.randint(-30, 30)
        out += f'<path d="M{x} {ybase} q{bend / 3:.0f} {-h / 2:.0f} {bend} {-h}" stroke="{col}" stroke-width="{w}" fill="none" opacity="{op}" stroke-linecap="round"/>'
        if random.random() < .25:
            out += f'<ellipse cx="{x + bend}" cy="{ybase - h + 18}" rx="7" ry="22" fill="#6b4a2a" opacity="{op}"/>'
    return out


# ======================= short1: the net =======================
def short1():
    random.seed(21)
    defs = FILTERS + lin('sky1', [(0, '#7fc4d8'), (.6, '#cfe9d8'), (1, '#f6efc4')])
    defs += lin('water1', [(0, '#6fae9a'), (.35, '#3f7f6c'), (1, '#173b32')])
    defs += rad('sun1', 1240, 520, 640, [(0, '#fff6d0', .85), (.3, '#ffe9a0', .35), (1, '#ffe9a0', 0)])
    defs += lin('pole1', [(0, '#8a5a2e'), (.5, '#d9a066'), (1, '#6a3e1c')], x2=1, y2=0)
    defs += vig('vig1', .5)
    HZ = 640
    b = f'<rect width="1920" height="{HZ}" fill="url(#sky1)"/>'
    for _ in range(8):
        b += f'<ellipse cx="{random.randint(200, 1900)}" cy="{random.randint(60, 360)}" rx="{random.randint(120, 260)}" ry="{random.randint(30, 60)}" fill="#ffffff" opacity=".55" filter="url(#b24)"/>'
    b += '<rect width="1920" height="1080" fill="url(#sun1)"/>'
    b += f'<path d="M0 {HZ - 50} q200 -60 420 -20 q260 -70 520 -10 q300 -60 560 -6 q240 -40 420 6 L1920 {HZ} L0 {HZ}z" fill="#6f9a62" opacity=".8"/>'
    b += f'<path d="M0 {HZ - 16} q400 -30 900 -6 q500 -24 1020 4 L1920 {HZ} L0 {HZ}z" fill="#466e44"/>'
    b += reeds(90, 0, 1920, HZ + 4, 30, 90, '#3a5e36', 3)
    b += f'<rect y="{HZ}" width="1920" height="{1080 - HZ}" fill="url(#water1)"/>'
    b += f'<path d="M0 {HZ} L1920 {HZ}" stroke="#fff6d0" stroke-width="4" opacity=".8"/>'
    for _ in range(34):
        b += f'<path d="M{random.randint(0, 1920)} {random.randint(HZ + 10, 1060)} l{random.randint(30, 110)} 0" stroke="#e6fff4" stroke-width="2.4" opacity=".3"/>'
    b += '<ellipse cx="1240" cy="700" rx="420" ry="40" fill="#fff6d0" opacity=".35" filter="url(#b24)"/>'   # sun glitter
    # lily pads
    for lx, ly, lr in ((640, 760, 60), (820, 840, 44), (1700, 720, 50), (480, 700, 36)):
        b += f'<path d="M{lx} {ly} m{lr} 0 a{lr} {lr * .38:.0f} 0 1 1 -8 -10 l-{lr - 8} 10z" fill="#4f8a3e" stroke="#1d3a1c" stroke-width="3"/>'
    # ripple rings where the drips fall
    for r in (60, 110, 170):
        b += f'<ellipse cx="1210" cy="990" rx="{r}" ry="{r * .22:.0f}" fill="none" stroke="#e6fff4" stroke-width="3" opacity="{.7 - r / 300:.2f}"/>'
    # ---- the dip net: pole from the top-right, hoop, mesh bag
    HX, HY, HRX, HRY = 1210, 520, 300, 96
    b += f'<path d="M{HX + HRX - 20} {HY - 10} L1990 40" stroke="#2a180a" stroke-width="40" stroke-linecap="round"/>'
    b += f'<path d="M{HX + HRX - 20} {HY - 10} L1990 40" stroke="url(#pole1)" stroke-width="30" stroke-linecap="round"/>'
    b += f'<path d="M{HX + HRX - 10} {HY - 20} L1990 30" stroke="#ffe0b0" stroke-width="5" opacity=".6"/>'
    bag = f'M{HX - HRX} {HY} C{HX - HRX + 10} {HY + 260} {HX - 140} {HY + 400} {HX} {HY + 400} C{HX + 150} {HY + 400} {HX + HRX - 10} {HY + 260} {HX + HRX} {HY} Z'
    defs += f'<clipPath id="bag1"><path d="{bag}"/></clipPath>'
    b += f'<ellipse cx="{HX}" cy="{HY + 140}" rx="380" ry="320" fill="#d8ffe0" opacity=".45" filter="url(#b50)"/>'   # halo
    b += f'<path d="{bag}" fill="#0f2a22" opacity=".35"/>'
    mesh_b = '<g clip-path="url(#bag1)" stroke="#d8e6d0" stroke-width="2.4" opacity=".45">'
    for k in range(-20, 30):
        mesh_b += f'<path d="M{HX - 500 + k * 34} {HY - 40} l420 520 M{HX + 500 - k * 34} {HY - 40} l-420 520"/>'
    b += mesh_b + '</g>'
    # back half of the hoop
    b += f'<path d="M{HX - HRX} {HY} A{HRX} {HRY} 0 0 1 {HX + HRX} {HY}" stroke="#1c2226" stroke-width="20" fill="none"/>'
    b += f'<path d="M{HX - HRX} {HY} A{HRX} {HRY} 0 0 1 {HX + HRX} {HY}" stroke="#8d98a0" stroke-width="12" fill="none"/>'
    # the many-legged frog in the bag, legs poking out through the mesh
    b += monster(HX, HY + 330, 2.75, extra=5, mouth='smile', look=(-3, 1), glow='#fff2a8')
    # front mesh over the frog + bag outline
    mesh_f = '<g clip-path="url(#bag1)" stroke="#f4fbf0" stroke-width="2.6" opacity=".38">'
    for k in range(-20, 30):
        mesh_f += f'<path d="M{HX - 480 + k * 34} {HY - 30} l420 520 M{HX + 480 - k * 34} {HY - 30} l-420 520"/>'
    b += mesh_f + '</g>'
    b += f'<path d="{bag}" fill="none" stroke="#e8f2e0" stroke-width="4" opacity=".7"/>'
    # front half of the hoop (rim light from the sun)
    b += f'<path d="M{HX - HRX} {HY} A{HRX} {HRY} 0 0 0 {HX + HRX} {HY}" stroke="#1c2226" stroke-width="24" fill="none"/>'
    b += f'<path d="M{HX - HRX} {HY} A{HRX} {HRY} 0 0 0 {HX + HRX} {HY}" stroke="#a9b4bc" stroke-width="15" fill="none"/>'
    b += f'<path d="M{HX - HRX + 40} {HY + 46} A{HRX} {HRY} 0 0 0 {HX + 120} {HY + HRY - 4}" stroke="#ffffff" stroke-width="5" fill="none" opacity=".75"/>'
    # drips
    for k, (dx, dy) in enumerate(((HX - 40, HY + 430), (HX + 30, HY + 470), (HX - 10, HY + 530), (HX + 60, HY + 410), (HX - 90, HY + 400))):
        b += f'<path d="M{dx} {dy - 12} q8 12 0 18 q-8 -6 0 -18z" fill="#dff6ff" stroke="#2c5a6a" stroke-width="2.4"/>'
    for sx_, sy_, ss in ((HX - 360, HY - 40, 22), (HX + 340, HY + 160, 18), (HX - 330, HY + 290, 14), (HX + 120, HY - 90, 14)):
        b += spark(sx_, sy_, ss, col='#fffbe0')
    # mascot frog: field-trip bucket hat + backpack, on a mossy rock bottom-left
    b += '<path d="M150 1080 q10 -110 200 -120 q200 -6 230 120z" fill="#55604a" stroke="#1d2b1c" stroke-width="5"/>'
    b += '<path d="M190 990 q80 -50 200 -40" stroke="#8fa070" stroke-width="7" fill="none" opacity=".7"/>'
    back = '<rect x="-52" y="-58" width="34" height="52" rx="10" fill="#d9733a" stroke-width="3.2"/>'
    torso = '<path d="M-26 -40 q4 22 -2 40 M34 -40 q-4 22 2 40" stroke="#b5562a" stroke-width="6" fill="none"/>'
    hat = ('<path d="M-30 -84 q34 -48 70 0z" fill="#f2c94c" stroke-width="3.4"/>'
           '<path d="M-44 -82 q50 -14 98 0 q-50 10 -98 0z" fill="#e8b93a" stroke-width="3.4"/>')
    b += frog(370, 970, 3.0, mouth='o', arms=('q-18 -6 -22 -30', 'q18 -6 22 -30'), look=(6, -3), back=back, torso=torso, head=hat, sweat=True)
    b += '<rect width="1920" height="1080" fill="url(#vig1)"/>'
    lines = [('SHOULD NOT', 150, 'w'), ('EXIST', 250, 'y')]
    return page('#173b32', svg(defs, b), lines, outline='#0a1a16')


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
    defs = FILTERS + SHELL + lin('sky2', [(0, '#24364a'), (.55, '#5a6f7a'), (1, '#c9a46a')])
    defs += lin('water2', [(0, '#3d5a52'), (1, '#111f1c')])
    defs += lin('brass', [(0, '#7a5414'), (.4, '#f2d27a'), (.6, '#fff0c0'), (1, '#6a4410')], x2=1, y2=1)
    defs += lin('woodH', [(0, '#5a2e14'), (.5, '#a8643a'), (1, '#4a2410')], x2=1, y2=0)
    defs += rad('lamp2', 1300, 600, 620, [(0, '#fff2c0', .55), (.4, '#ffd98a', .18), (1, '#ffd98a', 0)])
    defs += vig('vig2', .6)
    HZ = 650
    b = f'<rect width="1920" height="{HZ}" fill="url(#sky2)"/>'
    b += stars(40, 300, 900, op=.4, sparks=0)
    b += f'<path d="M0 {HZ - 40} q300 -60 640 -20 q360 -60 700 -10 q300 -40 580 6 L1920 {HZ} L0 {HZ}z" fill="#2b3a34"/>'
    b += reeds(80, 0, 1920, HZ + 2, 40, 110, '#1e2b26', 4)
    b += f'<rect y="{HZ}" width="1920" height="{1080 - HZ}" fill="url(#water2)"/>'
    for _ in range(26):
        b += f'<path d="M{random.randint(0, 1920)} {random.randint(HZ + 10, 900)} l{random.randint(40, 120)} 0" stroke="#c9a46a" stroke-width="2" opacity=".3"/>'
    # mud bank the deformed frog sits on
    b += '<path d="M700 1080 q40 -180 300 -210 q400 -40 640 30 q200 60 280 180z" fill="#3e3222" stroke="#1a140c" stroke-width="5"/>'
    b += '<path d="M780 960 q200 -100 520 -90" stroke="#6a5638" stroke-width="8" fill="none" opacity=".6"/>'
    b += '<rect width="1920" height="1080" fill="url(#lamp2)"/>'
    # a small ramshorn snail on the bank: the first clue
    b += snail(1640, 860, .42)
    # the deformed frog
    FX, FY = 1290, 900
    b += monster(FX, FY, 3.0, pick=[0, 1, 2, 4], mouth='flat', look=(2, 1))
    # the lens: magnified hip skin with cysts
    LX, LY, LR = 1290, 610, 245
    defs += f'<clipPath id="lens2"><circle cx="{LX}" cy="{LY}" r="{LR}"/></clipPath>'
    L = f'<g clip-path="url(#lens2)"><rect x="{LX - LR}" y="{LY - LR}" width="{2 * LR}" height="{2 * LR}" fill="#9cc26a"/>'
    L += f'<circle cx="{LX - 60}" cy="{LY - 80}" r="220" fill="#c4de8e" opacity=".6" filter="url(#b50)"/>'
    for _ in range(9):
        L += f'<ellipse cx="{random.randint(LX - LR, LX + LR)}" cy="{random.randint(LY - LR, LY + LR)}" rx="{random.randint(30, 52)}" ry="{random.randint(24, 40)}" fill="#3f5a26" stroke="#c9dd9a" stroke-width="3" opacity=".8"/>'
    for _ in range(60):
        L += f'<circle cx="{random.randint(LX - LR, LX + LR)}" cy="{random.randint(LY - LR, LY + LR)}" r="{random.choice([3, 4, 5])}" fill="#7a9a4a" opacity=".6"/>'
    for cx_, cy_, r, a in ((LX - 70, LY - 40, 62, 10), (LX + 80, LY - 90, 50, -30), (LX + 60, LY + 70, 66, 40), (LX - 110, LY + 110, 44, -10), (LX + 160, LY + 20, 38, 80), (LX - 10, LY + 170, 36, 20), (LX - 150, LY - 150, 34, 60)):
        L += cyst(cx_, cy_, r, a)
    L += f'<path d="M{LX - LR + 30} {LY - 60} a{LR - 30} {LR - 30} 0 0 1 {LR + 60} {-LR + 90}" stroke="#fff" stroke-width="22" fill="none" opacity=".28" stroke-linecap="round"/>'
    L += '</g>'
    b += f'<circle cx="{LX}" cy="{LY}" r="{LR + 50}" fill="#fff4c0" opacity=".25" filter="url(#b24)"/>'
    b += f'<circle cx="{LX + 14}" cy="{LY + 18}" r="{LR + 22}" fill="#000" opacity=".35" filter="url(#b12)"/>'
    b += L
    # handle down to the mascot frog's hands (bottom-left of the lens)
    hx0, hy0 = LX - (LR + 18) * .74, LY + (LR + 18) * .67
    b += f'<path d="M{hx0:.0f} {hy0:.0f} L{hx0 - 300:.0f} {hy0 + 250:.0f}" stroke="#1a0e06" stroke-width="58" stroke-linecap="round"/>'
    b += f'<path d="M{hx0:.0f} {hy0:.0f} L{hx0 - 300:.0f} {hy0 + 250:.0f}" stroke="url(#woodH)" stroke-width="44" stroke-linecap="round"/>'
    b += f'<path d="M{hx0 - 6:.0f} {hy0 - 14:.0f} L{hx0 - 290:.0f} {hy0 + 224:.0f}" stroke="#e0a070" stroke-width="5" opacity=".6"/>'
    b += f'<circle cx="{LX}" cy="{LY}" r="{LR + 14}" fill="none" stroke="#2a1a06" stroke-width="44"/>'
    b += f'<circle cx="{LX}" cy="{LY}" r="{LR + 14}" fill="none" stroke="url(#brass)" stroke-width="30"/>'
    b += f'<path d="M{LX - LR} {LY - 70} a{LR + 14} {LR + 14} 0 0 1 {LR - 40} {-LR + 66}" stroke="#fffbe0" stroke-width="6" fill="none" opacity=".8"/>'
    for sx_, sy_, ss in ((LX + 290, LY - 220, 24), (LX - 300, LY - 180, 16), (LX + 330, LY + 40, 14)):
        b += spark(sx_, sy_, ss, col='#fff6d0')
    # mascot frog detective: deerstalker hat + cape, holding the handle
    cape = ('<path d="M-36 -36 q40 18 82 0 l10 40 q-50 12 -102 0z" fill="#8a6a44" stroke-width="3.2"/>'
            '<path d="M-30 -20 l70 0 M-24 -6 l58 0" stroke="#5a4428" stroke-width="2.4" opacity=".7"/>')
    hat = ('<path d="M-30 -84 q36 -50 72 0 q-36 8 -72 0z" fill="#a7865a" stroke-width="3.4"/>'
           '<path d="M-42 -86 q-14 6 -10 -2 l20 -6z M54 -86 q14 6 10 -2 l-20 -6z" fill="#8a6a44" stroke-width="3"/>'
           '<path d="M-20 -94 l50 -8 M-14 -104 l38 -6" stroke="#6a4f30" stroke-width="2.6"/>')
    b += frog(hx0 - 400, 1000, 3.0, mouth='o', arms=('q30 -6 50 -26', 'q20 -14 22 -34'), look=(7, -5), torso=cape, head=hat)
    b += '<rect width="1920" height="1080" fill="url(#vig2)"/>'
    lines = [('IT WAS A', 130, 'w'), ('PARASITE', 190, 'y')]
    return page('#111f1c', svg(defs, b), lines, outline='#081010')


# ======================= short3: target legs =======================
def short3():
    random.seed(43)
    defs = FILTERS + TAD + lin('water3', [(0, '#2f7f74'), (.5, '#174a46'), (1, '#0a1f20')])
    defs += rad('glow3', 1340, 760, 520, [(0, '#ffe9a0', .45), (.4, '#ffd36a', .15), (1, '#ffd36a', 0)])
    defs += vig('vig3', .6)
    b = '<rect width="1920" height="1080" fill="url(#water3)"/>'
    for k in range(8):
        x0 = 700 + k * 150
        b += f'<path d="M{x0} 0 L{x0 + 80} 0 L{x0 - 200} 1080 L{x0 - 320} 1080z" fill="#d8fff0" opacity=".05"/>'
    b += f'<path d="M0 0 L1920 0 L1920 40 q-480 24 -960 0 q-480 -24 -960 0z" fill="#9fe0d0" opacity=".35"/>'
    for _ in range(80):
        b += f'<circle cx="{random.randint(0, 1920)}" cy="{random.randint(0, 1080)}" r="{random.choice([2, 3, 4])}" fill="#d8fff0" opacity="{random.uniform(.1, .4):.2f}"/>'
    # mud + weeds at the bottom
    b += '<path d="M0 960 q300 -40 640 -6 q500 34 900 -10 q220 -14 380 6 L1920 1080 L0 1080z" fill="#0f241e"/>'
    for px in (80, 150, 230, 620, 700, 1820):
        for k in range(3):
            b += f'<path d="M{px + k * 16} 1000 q{-24 + k * 12} -180 {14 + k * 6} -{280 + k * 40}" stroke="#1f4a38" stroke-width="11" fill="none" opacity=".9"/>'
    b += '<rect width="1920" height="1080" fill="url(#glow3)"/>'
    # the tadpole, big, tail off the right edge
    TX, TY, TS = 1180, 560, 2.45
    b += tadpole(TX, TY, TS)
    BX, BY = TX + 68 * TS, TY + 48 * TS
    # crosshair on the limb buds
    b += f'<circle cx="{BX}" cy="{BY}" r="118" fill="none" stroke="#F2D27A" stroke-width="22" opacity=".3" filter="url(#b6)"/>'
    b += f'<circle cx="{BX}" cy="{BY}" r="118" fill="none" stroke="#F2D27A" stroke-width="8" stroke-dasharray="46 22"/>'
    b += f'<circle cx="{BX}" cy="{BY}" r="176" fill="none" stroke="#ff7a5a" stroke-width="5" opacity=".85"/>'
    for a in (0, 90, 180, 270):
        ca, sa = math.cos(math.radians(a)), math.sin(math.radians(a))
        b += f'<path d="M{BX + ca * 140:.0f} {BY + sa * 140:.0f} L{BX + ca * 214:.0f} {BY + sa * 214:.0f}" stroke="#ff7a5a" stroke-width="9" stroke-linecap="round"/>'
    # the swarm of cercariae diving at the buds, from the upper left
    for k in range(34):
        d = random.uniform(230, 900); ang = math.radians(random.uniform(150, 215))
        x, y = BX + d * math.cos(ang), BY + d * math.sin(ang)
        if (x < 980 and y < 470) or x < 720:   # keep the text corner and the frog clear
            continue
        head = math.degrees(math.atan2(BY - y, BX - x))
        s = random.uniform(2.0, 3.2)
        tx, ty = x - math.cos(math.radians(head)) * 120, y - math.sin(math.radians(head)) * 120
        b += f'<path d="M{tx:.0f} {ty:.0f} L{x:.0f} {y:.0f}" stroke="#e9fbff" stroke-width="{s * 2.2:.1f}" opacity=".18" stroke-linecap="round"/>'
        b += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{s * 9:.0f}" fill="#cff6ff" opacity=".35" filter="url(#b6)"/>'
        b += cerc(x, y, head, s=s)
    for sx_, sy_, ss in ((BX + 200, BY - 190, 20), (BX - 220, BY + 170, 14), (1700, 300, 16)):
        b += spark(sx_, sy_, ss, col='#fff6d0')
    # mascot frog in a brass diving helmet, sitting on the mud bottom-left
    helmet = (f'<circle cx="6" cy="-56" r="58" fill="#bfe8ff" fill-opacity=".22" stroke="#b8862e" stroke-width="9"/>'
              f'<circle cx="6" cy="-56" r="58" fill="none" stroke="{INK}" stroke-width="2.4"/>'
              '<path d="M-36 -94 q20 -22 52 -18" stroke="#fff" stroke-width="5" fill="none" opacity=".7"/>'
              '<rect x="-34" y="-8" width="80" height="14" rx="6" fill="#b8862e" stroke-width="3"/>'
              '<circle cx="-22" cy="-1" r="3" fill="#ffe6a0" stroke="none"/><circle cx="34" cy="-1" r="3" fill="#ffe6a0" stroke="none"/>')
    b += frog(330, 1000, 3.0, mouth='o', arms=('q-18 -6 -22 -30', 'q18 -6 22 -30'), look=(7, -3), front=helmet, sweat=False)
    for k in range(6):
        b += f'<circle cx="{360 + k * 10 + random.randint(-8, 8)}" cy="{690 - k * 44}" r="{6 + k}" fill="none" stroke="#e8fff8" stroke-width="3" opacity=".7"/>'
    b += '<rect width="1920" height="1080" fill="url(#vig3)"/>'
    lines = [('TARGET:', 160, 'w'), ('LEGS', 260, 'y')]
    return page('#0a1f20', svg(defs, b), lines, outline='#041010')


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
    defs += rad('spot4', 1400, 760, 420, [(0, '#fff6d0', .6), (.5, '#fff0c0', .2), (1, '#fff0c0', 0)])
    defs += lin('room4', [(0, '#1a1020'), (1, '#0a0810')])
    defs += vig('vig4', .55)
    b = '<rect width="1920" height="1080" fill="url(#room4)"/>'
    SX0, SX1, ST, SF = 980, 1860, 70, 830
    # painted backdrop: sunset pond
    b += f'<rect x="{SX0}" y="{ST}" width="{SX1 - SX0}" height="{SF - ST}" fill="url(#drop4)"/>'
    b += '<circle cx="1640" cy="520" r="80" fill="#fff4d0" opacity=".9"/>'
    b += f'<path d="M{SX0} 600 q200 -60 420 -20 q240 -50 460 0 L{SX1} {SF} L{SX0} {SF}z" fill="#7a8a52"/>'
    b += f'<path d="M{SX0} 660 L{SX1} 660 L{SX1} {SF} L{SX0} {SF}z" fill="#4f8a86"/>'
    b += f'<path d="M{SX0} 660 L{SX1} 660" stroke="#fff4d0" stroke-width="4" opacity=".7"/>'
    b += reeds(40, SX0, SX1, 664, 40, 110, '#3e5a30', 4)
    b += fly_heron(1560, 300, .75, sil='#5a3a3a')    # the bird waiting in the sky (painted)
    b += '<rect width="1920" height="1080" fill="url(#spot4)"/>'
    # stage floor
    b += f'<path d="M{SX0 - 60} {SF} L{SX1 + 60} {SF} L{SX1 + 60} {SF + 60} L{SX0 - 60} {SF + 60}z" fill="url(#floor4)" stroke="#140a04" stroke-width="5"/>'
    for k in range(1, 9):
        b += f'<path d="M{SX0 - 60 + k * 120} {SF} l0 60" stroke="#3a2010" stroke-width="3"/>'
    b += f'<path d="M{SX0 - 60} {SF + 4} L{SX1 + 60} {SF + 4}" stroke="#e0a46a" stroke-width="4" opacity=".7"/>'
    b += f'<rect x="{SX0 - 80}" y="{SF + 60}" width="{SX1 - SX0 + 160}" height="40" fill="#3a0c12" stroke="#140a04" stroke-width="4"/>'
    # marionette frog, tangled legs, hanging a little above the floor
    FX, FY = 1390, 790
    b += f'<ellipse cx="{FX}" cy="{SF + 6}" rx="240" ry="20" fill="#000" opacity=".35" filter="url(#b6)"/>'
    b += monster(FX, FY, 2.7, pick=[0, 1, 2, 3, 4], mouth='flat', look=(1, -3))
    # control bar + the brainless flatworm on the valance
    CX, CY = 1390, 230
    ends = [(CX - 220, CY), (CX + 220, CY), (CX, CY - 40), (CX, CY + 40)]
    targets = [(FX - 290, FY - 70), (FX + 300, FY - 60), (FX, FY - 220), (FX - 160, FY + 50), (FX + 160, FY + 60), (FX - 60, FY - 150), (FX + 80, FY - 150)]
    for k, (tx, ty) in enumerate(targets):
        ex, ey = (ends[0] if tx < FX - 100 else ends[1] if tx > FX + 100 else ends[2 + (k % 2)])
        b += f'<path d="M{ex} {ey} L{tx} {ty}" stroke="#fffbe8" stroke-width="3" opacity=".85"/>'
    b += f'<path d="M{CX - 230} {CY} L{CX + 230} {CY} M{CX} {CY - 50} L{CX} {CY + 50}" stroke="#2a1608" stroke-width="30" stroke-linecap="round"/>'
    b += f'<path d="M{CX - 230} {CY} L{CX + 230} {CY} M{CX} {CY - 50} L{CX} {CY + 50}" stroke="#c98a4a" stroke-width="20" stroke-linecap="round"/>'
    b += f'<path d="M{CX - 220} {CY - 5} L{CX + 220} {CY - 5}" stroke="#f0c080" stroke-width="4" opacity=".7"/>'
    # curtains + valance (drawn over the backdrop edges)
    b += f'<path d="M{SX0 - 80} {ST} L{SX0 + 90} {ST} q-40 300 -10 520 q20 160 -30 {SF - ST - 520} L{SX0 - 80} {SF}z" fill="url(#curt)" stroke="#2a0408" stroke-width="5"/>'
    b += f'<path d="M{SX1 + 80} {ST} L{SX1 - 90} {ST} q40 300 10 520 q-20 160 30 {SF - ST - 520} L{SX1 + 80} {SF}z" fill="url(#curt)" stroke="#2a0408" stroke-width="5"/>'
    b += f'<path d="M{SX0 - 90} 0 L{SX1 + 90} 0 L{SX1 + 90} {ST + 70} q-110 50 -220 0 q-110 50 -220 0 q-110 50 -220 0 q-110 50 -220 0 q-110 50 -220 0 L{SX0 - 90} {ST + 70}z" fill="#a81e28" stroke="#2a0408" stroke-width="5"/>'
    b += f'<path d="M{SX0 - 90} {ST + 66} q110 50 220 0 q110 50 220 0 q110 50 220 0 q110 50 220 0 q110 50 220 0" stroke="#F2D27A" stroke-width="9" fill="none"/>'
    # the flatworm puppeteer peeks over the valance, holding the bar with its tail
    b += f'<path d="M{CX - 60} {CY - 60} q-30 -40 -10 -80" stroke="{INK}" stroke-width="22" fill="none" stroke-linecap="round"/><path d="M{CX - 60} {CY - 60} q-30 -40 -10 -80" stroke="#f2b7a8" stroke-width="14" fill="none" stroke-linecap="round"/>'
    b += f'<ellipse cx="{CX}" cy="{CY - 150}" rx="230" ry="90" fill="#fff0c0" opacity=".25" filter="url(#b24)"/>'
    b += flatworm(CX, CY - 150, 1.35)
    for sx_, sy_, ss in ((CX + 280, CY - 120, 20), (CX - 300, CY + 140, 14), (FX + 330, FY - 260, 16)):
        b += spark(sx_, sy_, ss, col='#fff6d0')
    # mascot frog in the audience: theatre seat, popcorn
    b += '<path d="M140 1080 L140 820 q0 -40 40 -40 l380 0 q40 0 40 40 L600 1080z" fill="#7a1820" stroke="#1a0408" stroke-width="5"/>'
    b += '<path d="M170 830 q190 -30 400 0" stroke="#c0404a" stroke-width="6" fill="none" opacity=".6"/>'
    pop = ('<path d="M44 -10 l-6 -52 l52 0 l-6 52z" fill="#fff4e0" stroke-width="3.2"/>'
           '<path d="M42 -44 l4 34 M60 -60 l0 50 M78 -60 l-2 50" stroke="#d9454a" stroke-width="6"/>'
           '<circle cx="48" cy="-66" r="9" fill="#fff6c8" stroke-width="2.4"/><circle cx="64" cy="-72" r="10" fill="#fff6c8" stroke-width="2.4"/><circle cx="82" cy="-66" r="9" fill="#fff6c8" stroke-width="2.4"/>'
           '<circle cx="104" cy="-92" r="6" fill="#fff6c8" stroke-width="2"/>')
    b += frog(370, 990, 3.0, mouth='o', arms=('q-18 -8 -22 -30', 'q12 8 20 14'), look=(9, -4), front=pop, sweat=True)
    b += '<rect width="1920" height="1080" fill="url(#vig4)"/>'
    lines = [('IT', 140, 'w'), ('STEERS', 220, 'y'), ('THE FROG', 140, 'w')]
    return page('#0a0810', svg(defs, b), lines, outline='#0a0408')


# ======================= short5: the algae buffet =======================
def short5():
    random.seed(65)
    defs = FILTERS + SHELL + lin('sky5', [(0, '#5d6a6e'), (.7, '#a9b4a8'), (1, '#c9d0b8')])
    defs += lin('water5', [(0, '#3f6e3e'), (.5, '#244a2c'), (1, '#0f2216')])
    defs += lin('algae', [(0, '#c6f06a'), (.5, '#7fc93a'), (1, '#3f8a22')])
    defs += lin('sack', [(0, '#e0c088'), (1, '#9a7442')], x2=1, y2=0)
    defs += rad('glow5', 1150, 720, 620, [(0, '#e6ff9a', .45), (.4, '#b8f060', .15), (1, '#b8f060', 0)])
    defs += vig('vig5', .55)
    WL = 520
    b = f'<rect width="1920" height="{WL}" fill="url(#sky5)"/>'
    for _ in range(10):
        b += f'<ellipse cx="{random.randint(700, 1920)}" cy="{random.randint(20, 220)}" rx="{random.randint(150, 300)}" ry="{random.randint(40, 80)}" fill="#3e484c" opacity=".55" filter="url(#b24)"/>'
    # far field + bank on the right with the tipped sack
    b += f'<path d="M0 {WL - 30} q300 -40 700 -16 q400 -30 700 -6 L1920 {WL} L0 {WL}z" fill="#5f7a44"/>'
    b += f'<path d="M1300 {WL + 10} q120 -120 300 -150 q200 -20 320 0 L1920 {WL + 10}z" fill="#6a5a38" stroke="#2a2010" stroke-width="5"/>'
    for k in range(9):   # crop rows
        b += f'<path d="M{1420 + k * 56} {WL - 120 + k * 4} q20 -30 6 -60" stroke="#5f8a3a" stroke-width="7" fill="none"/>'
    # rain
    for _ in range(140):
        x = random.randint(0, 1980); y = random.randint(-20, WL - 20)
        b += f'<path d="M{x} {y} l-14 34" stroke="#e8f2f4" stroke-width="2.4" opacity="{random.uniform(.25, .6):.2f}" stroke-linecap="round"/>'
    # fertilizer sack (no lettering), tipped toward the pond, pellets pouring
    b += '<g transform="translate(1620 300) rotate(-28)">'
    b += '<path d="M-90 -110 q90 -20 180 0 l14 200 q-104 24 -208 0z" fill="url(#sack)" stroke="#3a2a10" stroke-width="6" stroke-linejoin="round"/>'
    b += '<path d="M-84 -80 l170 0" stroke="#7a5a2a" stroke-width="4" stroke-dasharray="10 8"/>'
    b += '<circle cx="2" cy="10" r="46" fill="#f6ecd0" stroke="#3a2a10" stroke-width="4"/>'
    b += '<path d="M-20 30 q0 -50 40 -50 q4 46 -40 50z M-20 30 q20 -20 34 -36" fill="#5aa040" stroke="#1d3a14" stroke-width="3.4"/>'
    b += '</g>'
    for k in range(70):
        t = random.random(); x = 1530 - t * 330 + random.randint(-26, 26); y = 220 + t * t * 330 + random.randint(-14, 14)
        b += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{random.choice([5, 6, 7])}" fill="{random.choice(["#eaffb0", "#f6e6a0", "#d8f080"])}" stroke="#3a4a18" stroke-width="1.6"/>'
    b += '<ellipse cx="1300" cy="430" rx="200" ry="90" fill="#eaffb0" opacity=".25" filter="url(#b24)"/>'
    # water
    b += f'<rect y="{WL}" width="1920" height="{1080 - WL}" fill="url(#water5)"/>'
    b += '<rect width="1920" height="1080" fill="url(#glow5)"/>'
    b += '<path d="M0 980 q300 -30 640 -6 q500 30 900 -8 q240 -12 380 4 L1920 1080 L0 1080z" fill="#18281a"/>'
    # algae blanket on the surface + hanging strands
    blanket = f'M0 {WL - 6} L1920 {WL - 6} L1920 {WL + 50}'
    x = 1920
    while x > 0:
        x2 = x - random.randint(50, 110)
        blanket += f' Q{(x + x2) / 2:.0f} {WL + random.randint(70, 120)} {x2} {WL + random.randint(30, 60)}'
        x = x2
    blanket += ' Z'
    b += f'<path d="{blanket}" fill="url(#algae)" stroke="#1d3a14" stroke-width="4"/>'
    for _ in range(90):
        b += f'<circle cx="{random.randint(0, 1920)}" cy="{random.randint(WL, WL + 50)}" r="{random.randint(6, 18)}" fill="#d8ff8a" opacity="{random.uniform(.3, .7):.2f}"/>'
    strands = []
    for _ in range(26):
        sx = random.randint(560, 1900); L = random.randint(140, 340)
        strands.append((sx, L))
        b += f'<path d="M{sx} {WL + 50} q{random.randint(-40, 40)} {L / 2:.0f} {random.randint(-30, 30)} {L}" stroke="#7fc93a" stroke-width="{random.randint(10, 18)}" fill="none" stroke-linecap="round" opacity=".85"/>'
        for k in range(3):
            b += f'<circle cx="{sx + random.randint(-14, 14)}" cy="{WL + 50 + random.randint(30, L)}" r="{random.randint(7, 13)}" fill="#a8e060" opacity=".8"/>'
    # snails at the buffet (napkin bibs), the big one in front
    def bib(x, y, s):
        return (f'<g transform="translate({x} {y}) scale({s})"><path d="M-170 70 l-70 20 l40 60 z" fill="#ffffff" stroke="{INK}" stroke-width="4" stroke-linejoin="round"/>'
                f'<path d="M-205 98 l14 20 M-222 92 l26 40" stroke="#d9454a" stroke-width="4"/></g>')
    for sx_, sy_, ss in ((1640, 900, .55), (840, 900, .6), (1500, 700, .45)):
        b += snail(sx_, sy_, ss) + bib(sx_, sy_, ss)
    b += f'<ellipse cx="1180" cy="790" rx="330" ry="240" fill="#e6ff9a" opacity=".22" filter="url(#b50)"/>'
    b += snail(1200, 830, 1.35) + bib(1200, 830, 1.35)
    b += f'<path d="M{1200 - 225 * 1.35:.0f} {830 + 8 * 1.35:.0f} q-30 -140 20 -{240}" stroke="#7fc93a" stroke-width="20" fill="none" stroke-linecap="round"/>'   # strand being slurped
    for sx_, sy_, ss in ((1460, 620, 18), (880, 700, 14), (1700, 760, 14)):
        b += spark(sx_, sy_, ss, col='#f6ffd0')
    # mascot frog: a buffet guest under the algae, napkin bib + fork, on the mud bottom-left
    bibf = ('<path d="M-30 -36 q36 10 72 0 l-36 40z" fill="#ffffff" stroke-width="3.2"/>'
            '<path d="M-14 -30 l12 16 M26 -32 l-12 18" stroke="#d9454a" stroke-width="3"/>')
    fork = ('<path d="M58 -40 L58 -96" stroke-width="9"/><path d="M58 -40 L58 -96" stroke="#d8dde2" stroke-width="5"/>'
            '<path d="M48 -96 l0 -22 M58 -96 l0 -24 M68 -96 l0 -22 M46 -96 q12 8 24 0" stroke="#d8dde2" stroke-width="4" fill="none"/>'
            '<path d="M48 -96 l0 -22 M58 -96 l0 -24 M68 -96 l0 -22" stroke-width="1.4" fill="none"/>')
    b += frog(380, 1000, 3.0, mouth='o', arms=('q-18 -6 -22 -30', 'q14 -8 18 -30'), look=(8, -3), torso=bibf, front=fork)
    for k in range(5):
        b += f'<circle cx="{random.randint(120, 640)}" cy="{random.randint(WL + 120, 940)}" r="{random.randint(6, 12)}" fill="none" stroke="#d8ffd0" stroke-width="3" opacity=".5"/>'
    b += '<rect width="1920" height="1080" fill="url(#vig5)"/>'
    lines = [('AN ALGAE', 150, 'w'), ('BUFFET', 230, 'y')]
    return page('#0f2216', svg(defs, b), lines, outline='#0a1406')


ROOT = os.path.dirname(os.path.dirname(HERE))   # videos/
for n, fn in enumerate((short1, short2, short3, short4, short5), 1):
    d = os.path.join(ROOT, f'parasite-monster-frogs-short{n}', 'thumb'); os.makedirs(d, exist_ok=True)
    for f in ('common.css', 'Fredoka-700.woff2'):
        shutil.copy(os.path.join(HERE, f), d)
    open(os.path.join(d, 'A.html'), 'w').write(fn())
print('ok')
