# Thumbnails A-C for space-nuke (guideline 16-6, brief tools/briefs/thumb_art.md).
# A = homage to Dr. Strangelove (rider on a falling bomb, waving a hat): the frog rides a warhead high above the Pacific.
#     Text "WHERE'S THE BOOM?" (script: "You would hear nothing. No roar, no rumble, no thunder. Just a silent flash.")
# B = intuitive: the silent flash. Translucent plasma sphere in the black void, X-rays hit a small spacecraft
#     (blow-off puffs), the frog in a helmet covers its ears and hears nothing. Text "A SILENT FLASH" (S01, "The Sound of Nothing").
# C = intuitive: Starfish Prime seen from a Hawaiian beach: flash 400 km up, red/green artificial auroras,
#     streetlights going dark (EMP). Text "400 KM UP, LIGHTS OUT" (script: exploded about 400 km up; hundreds of streetlights went dark).
# run: python3 make.py
import os, sys, math, random
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', '..', 'tools'))
from thumb_lib import page, svg, lin, rad, stars, spark, blobs

INK = '#1d2b1c'; GREEN = '#6aa55a'; DARKG = '#4d8a4a'; BELLY = '#9cc98a'


# ---------- mascot frog (tools/assets/frog.svg), posable ----------
def arm(d):
    return (f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="7.5"/>'
            f'<path d="{d}" fill="none" stroke="{GREEN}" stroke-width="3.4"/>')


def hand_dot(x, y):
    return f'<circle cx="{x}" cy="{y}" r="4.2" fill="{GREEN}" stroke="{INK}" stroke-width="2.4"/>'


def frog(x, y, s, flip=False, look=(0, 0), mouth='o', armL=None, armR=None, feet=None, helmet=False,
         rot=0, back='', front='', mid='', pupil=5.4):
    sx = -s if flip else s
    g = [f'<g transform="translate({x} {y}) rotate({rot}) scale({sx} {s})" stroke="{INK}" stroke-linejoin="round" stroke-linecap="round">', back]
    if helmet:
        g.append(f'<rect x="-46" y="-52" width="20" height="40" rx="6" fill="#c9ced8" stroke-width="3"/>')
    fl, fr = feet or ((-22, 4, 0), (22, 4, 0))
    for fx, fy, fa in (fl, fr):
        g.append(f'<ellipse cx="{fx}" cy="{fy}" rx="16" ry="9" transform="rotate({fa} {fx} {fy})" fill="{DARKG}" stroke-width="3.2"/>')
    g.append(f'<path d="M-34 0 q-6 -64 34 -70 q40 -2 42 62 q0 10 -6 12 q-36 6 -70 -4z" fill="{GREEN}" stroke-width="4"/>')
    g.append(f'<ellipse cx="2" cy="-12" rx="22" ry="20" fill="{BELLY}" stroke="none" opacity=".7"/>')
    g.append(f'<path d="M-24 -50 q6 -14 18 -16" fill="none" stroke="#a9d692" stroke-width="3" opacity=".8"/>')
    lx, ly = look
    for ex in (-10, 22):
        g.append(f'<circle cx="{ex}" cy="-66" r="13" fill="#f4f5ea" stroke-width="3.2"/>')
        g.append(f'<circle cx="{ex + 2 + lx}" cy="{-66 + ly}" r="{pupil}" fill="{INK}" stroke="none"/>')
        g.append(f'<circle cx="{ex + 3.6 + lx}" cy="{-68 + ly}" r="1.7" fill="#fff" stroke="none"/>')
    if mouth == 'o':
        g.append(f'<ellipse cx="6" cy="-42" rx="5.5" ry="6.5" fill="#3a1d1d" stroke-width="2.6"/>')
    elif mouth == 'wow':
        g.append(f'<ellipse cx="6" cy="-38" rx="9" ry="12" fill="#3a1d1d" stroke-width="2.8"/><ellipse cx="6" cy="-32" rx="5" ry="5" fill="#e07a7a" stroke="none"/>')
    elif mouth == 'grin':
        g.append(f'<path d="M-8 -46 q14 14 28 0 z" fill="#3a1d1d" stroke-width="2.8"/>')
    else:
        g.append(f'<path d="M-8 -44 q14 12 28 0" fill="none" stroke-width="3.4"/>')
    g.append(f'<ellipse cx="-16" cy="-50" rx="5" ry="3" fill="#e88f86" stroke="none" opacity=".55"/><ellipse cx="28" cy="-50" rx="5" ry="3" fill="#e88f86" stroke="none" opacity=".55"/>')
    g.append(mid)
    aL = armL or 'M-34 -22 q-14 6 -16 22'
    aR = armR or 'M38 -22 q14 6 16 22'
    if helmet:
        g.append(f'<ellipse cx="4" cy="-4" rx="44" ry="9" fill="#d8dde6" stroke-width="3"/>')
        g.append(f'<circle cx="4" cy="-48" r="52" fill="#bfe6ff" fill-opacity=".14" stroke="#e8f6ff" stroke-width="3.2" stroke-opacity=".9"/>')
        g.append(f'<path d="M-30 -78 q14 -18 38 -20" fill="none" stroke="#fff" stroke-width="5" opacity=".75"/>')
        g.append(f'<path d="M40 -30 q6 -10 6 -22" fill="none" stroke="#fff" stroke-width="3" opacity=".45"/>')
    g.append(arm(aL)); g.append(arm(aR))
    for a in (aL, aR):
        nums = [float(v) for v in a.replace('M', ' ').replace('q', ' ').split()]
        g.append(hand_dot(nums[0] + nums[-2], nums[1] + nums[-1]))
    g.append(front); g.append('</g>')
    return ''.join(g)


GLOW = ('<filter id="b4" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="4"/></filter>'
        '<filter id="b12" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="12"/></filter>'
        '<filter id="b30" x="-60%" y="-60%" width="220%" height="220%"><feGaussianBlur stdDeviation="30"/></filter>'
        '<filter id="b60" x="-80%" y="-80%" width="260%" height="260%"><feGaussianBlur stdDeviation="60"/></filter>')


def trefoil(cx, cy, r, bg, fg):
    o = f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{bg}" stroke="#2a2a22" stroke-width="3"/>'
    for k in range(3):
        a0 = math.radians(-90 + k * 120 - 30); a1 = math.radians(-90 + k * 120 + 30)
        ri, ro = r * .24, r * .86
        o += (f'<path d="M{cx + ri * math.cos(a0):.1f} {cy + ri * math.sin(a0):.1f} L{cx + ro * math.cos(a0):.1f} {cy + ro * math.sin(a0):.1f} '
              f'A{ro} {ro} 0 0 1 {cx + ro * math.cos(a1):.1f} {cy + ro * math.sin(a1):.1f} L{cx + ri * math.cos(a1):.1f} {cy + ri * math.sin(a1):.1f} '
              f'A{ri} {ri} 0 0 0 {cx + ri * math.cos(a0):.1f} {cy + ri * math.sin(a0):.1f}Z" fill="{fg}"/>')
    return o + f'<circle cx="{cx}" cy="{cy}" r="{r * .15}" fill="{fg}"/>'


# =====================================================================================
# A: Dr. Strangelove homage - the frog rides a warhead over the Pacific, waving a cowboy hat
# =====================================================================================
def make_A():
    random.seed(11)
    d = GLOW
    d += lin('aSky', [(0, '#03040b'), (.6, '#070b1d'), (1, '#0b1838')])
    d += lin('aBody', [(0, '#f4f1e6'), (.18, '#d9d6c8'), (.5, '#9d9c8e'), (.8, '#5a5b55'), (1, '#2b2d2e')])
    d += lin('aNose', [(0, '#6b6f73'), (.25, '#4a4e52'), (.7, '#24272b'), (1, '#121416')])
    d += lin('aFin', [(0, '#dcd8c8'), (.5, '#8e8c7e'), (1, '#3c3d39')])
    d += lin('aGold', [(0, '#fff0b8'), (.35, '#F2D27A'), (.8, '#a8812f'), (1, '#5e4718')])
    d += lin('aOcean', [(0, '#5fb6ff'), (.12, '#1f6fc4'), (.5, '#0e3f86'), (1, '#071d45')])
    d += rad('aAtm', 900, 2900, 2140, [(0, '#000', 0), (.955, '#2a7ddb', 0), (.968, '#7cc8ff', .9), (.985, '#2a6fd0', .35), (1, '#0b1838', 0)])
    d += rad('aSun', 1840, 70, 520, [(0, '#ffffff', 1), (.06, '#fff4cf', .95), (.2, '#ffd98a', .35), (.55, '#ff9e4a', .08), (1, '#ff9e4a', 0)])
    d += rad('aHalo', 0, 0, 640, [(0, '#fff2c8', .32), (.5, '#ffd27a', .1), (1, '#ffd27a', 0)])
    d += '<clipPath id="aEarth"><circle cx="900" cy="2900" r="2050"/></clipPath>'
    b = '<rect width="1920" height="1080" fill="url(#aSky)"/>'
    b += stars(170, 820, col='#eaf2ff', op=.55, sparks=0)
    # sun (light source) top right
    b += '<circle cx="1840" cy="70" r="520" fill="url(#aSun)"/>'
    for ang in range(0, 360, 30):
        a = math.radians(ang); L = 260 if ang % 60 == 0 else 150
        b += f'<line x1="1840" y1="70" x2="{1840 + L * math.cos(a):.0f}" y2="{70 + L * math.sin(a):.0f}" stroke="#fff6dc" stroke-width="3" opacity=".35"/>'
    # Earth limb (Pacific, daytime)
    b += '<circle cx="900" cy="2900" r="2140" fill="url(#aAtm)"/>'
    b += '<circle cx="900" cy="2900" r="2050" fill="url(#aOcean)"/>'
    eg = '<g clip-path="url(#aEarth)">'
    r2 = random.Random(5)
    for _ in range(46):   # cloud bands
        x = r2.randint(-200, 2100); y = r2.randint(860, 1100); rx = r2.randint(60, 220)
        eg += f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{rx * .16:.0f}" fill="#f2f8ff" opacity="{r2.uniform(.2, .55):.2f}" filter="url(#b12)"/>'
    eg += '<path d="M1200 975 q30 -8 48 4 q-18 10 -48 -4z M1268 990 q16 -4 24 4 q-10 6 -24 -4z" fill="#3e7a3a" opacity=".8"/>'  # tiny islands
    eg += '<circle cx="900" cy="2900" r="2050" fill="none" stroke="#bfe6ff" stroke-width="10" opacity=".6"/>'
    eg += '</g>'
    b += eg
    # speed streaks (from the tail, upper right)
    for k in range(14):
        x = 1120 + k * 52 + random.randint(-20, 20); y = 120 + k * 38 + random.randint(-30, 30)
        L = random.randint(120, 260)
        b += f'<line x1="{x}" y1="{y}" x2="{x + L * .82:.0f}" y2="{y - L * .57:.0f}" stroke="#cfe3ff" stroke-width="{random.choice([2, 3, 4])}" stroke-linecap="round" opacity="{random.uniform(.15, .4):.2f}"/>'
    # ---- warhead (local: nose at -x, tail at +x, top = -y) ----
    CX, CY, ROT = 1300, 560, -35
    w = f'<g transform="translate({CX} {CY}) rotate({ROT})">'
    w += '<ellipse cx="0" cy="0" rx="560" ry="200" fill="#ffe7b0" opacity=".10" filter="url(#b60)"/>'
    # back fin (seen behind the body, pointing down-away)
    w += '<path d="M300 40 L470 170 L520 170 L480 40Z" fill="#4a4b46" stroke="#15171a" stroke-width="5" stroke-linejoin="round"/>'
    # tail cone
    w += '<path d="M330 -118 L450 -72 L450 72 L330 118Z" fill="url(#aBody)" stroke="#15171a" stroke-width="6" stroke-linejoin="round"/>'
    w += '<rect x="446" y="-78" width="22" height="156" rx="6" fill="#3d3f3c" stroke="#15171a" stroke-width="5"/>'
    # body cylinder
    w += '<path d="M-250 -120 L330 -120 L330 120 L-250 120Z" fill="url(#aBody)" stroke="#15171a" stroke-width="6"/>'
    # nose ogive
    w += '<path d="M-250 -120 C-360 -118 -440 -70 -478 0 C-440 70 -360 118 -250 120Z" fill="url(#aBody)" stroke="#15171a" stroke-width="6" stroke-linejoin="round"/>'
    w += '<path d="M-400 -82 C-430 -60 -460 -30 -478 0 C-460 30 -430 60 -400 82 Q-414 0 -400 -82Z" fill="url(#aNose)" stroke="#15171a" stroke-width="5"/>'
    # gold bands
    for bx in (-262, 300):
        w += f'<rect x="{bx}" y="-122" width="30" height="244" fill="url(#aGold)" stroke="#15171a" stroke-width="5"/>'
    # panel seams + rivets
    for sx in (-120, 40, 190):
        w += f'<line x1="{sx}" y1="-120" x2="{sx}" y2="120" stroke="#3a3b38" stroke-width="3" opacity=".7"/>'
        for ry in range(-104, 110, 26):
            w += f'<circle cx="{sx - 9}" cy="{ry}" r="3" fill="#2f302d" opacity=".55"/>'
    w += '<path d="M-250 -96 L330 -96" stroke="#fffdf2" stroke-width="10" opacity=".75" stroke-linecap="round"/>'  # sun highlight
    w += '<path d="M-250 -96 C-330 -92 -400 -60 -440 -18" stroke="#fffdf2" stroke-width="8" fill="none" opacity=".55" stroke-linecap="round"/>'
    w += '<path d="M-250 112 L330 112" stroke="#7cc8ff" stroke-width="6" opacity=".55"/>'  # earthshine rim
    w += trefoil(-20, 10, 62, '#F2D27A', '#1a1a16')
    # hazard stripes on tail cone
    for k in range(5):
        w += f'<path d="M{350 + k * 20} -110 l14 0 l-6 220 l-14 0z" fill="#1a1a16" opacity=".55"/>'
    # front fin (towards viewer, down) and top fin
    w += '<path d="M320 70 L520 250 L590 250 L500 70Z" fill="url(#aFin)" stroke="#15171a" stroke-width="6" stroke-linejoin="round"/>'
    w += '<path d="M320 -70 L520 -250 L590 -250 L500 -70Z" fill="url(#aFin)" stroke="#15171a" stroke-width="6" stroke-linejoin="round"/>'
    w += '<path d="M352 -84 L520 -236" stroke="#fffaf0" stroke-width="5" opacity=".6"/>'
    w += '</g>'
    b += w
    # ---- frog astride the bomb, waving a cowboy hat (Strangelove) ----
    # seat point on the bomb top (local 150,-120)
    a = math.radians(ROT)
    sxp = CX + 150 * math.cos(a) - (-120) * math.sin(a); syp = CY + 150 * math.sin(a) + (-120) * math.cos(a)
    hat = ('<g transform="translate(66 -86) rotate(18)">'
           '<path d="M-34 6 q34 14 68 0 q8 -4 4 -8 q-36 10 -76 0 q-4 4 4 8z" fill="#8a5a2b" stroke-width="3"/>'
           '<path d="M-20 0 q-2 -24 8 -28 q8 4 12 -2 q4 6 12 2 q10 4 8 28 q-20 6 -40 0z" fill="#a06a35" stroke-width="3"/>'
           '<path d="M-19 -6 q20 5 38 0" fill="none" stroke="#5a3a1a" stroke-width="5"/></g>')
    leg = ('<path d="M-28 -4 q-12 8 -12 20" fill="none" stroke="#1d2b1c" stroke-width="10"/>'
           '<path d="M-28 -4 q-12 8 -12 20" fill="none" stroke="#4d8a4a" stroke-width="5"/>'
           '<ellipse cx="-44" cy="18" rx="15" ry="8" transform="rotate(-25 -44 18)" fill="#4d8a4a" stroke-width="3.2"/>')
    b += frog(round(sxp + 6), round(syp + 18), 3.1, look=(4, -3), mouth='grin', helmet=True, rot=-12,
              feet=((-22, 4, 0), (22, 4, 0)),
              armL='M-34 -22 q-10 14 -2 30', armR='M38 -24 q22 -18 24 -54',
              front=hat, back=leg)
    for x, y, s in ((1010, 180, 20), (1560, 640, 16), (960, 520, 14), (1750, 470, 18), (1180, 90, 12)):
        b += spark(x, y, s)
    return page('#03040b', svg(d, b), [("WHERE'S", 190, 'w'), ('THE', 120, 'w'), ('BOOM?', 250, 'y')], top=48)


# =====================================================================================
# B: intuitive - the silent flash: plasma sphere, X-rays, spacecraft blow-off, frog covering ears
# =====================================================================================
def make_B():
    random.seed(23)
    CX, CY, R = 1250, 460, 350
    d = GLOW
    d += rad('bHalo', CX, CY, 900, [(0, '#fff3d6', .55), (.25, '#ffc98a', .2), (.5, '#b46cff', .07), (1, '#3b1a6b', 0)])
    d += rad('bShell', CX, CY, R, [(0, '#fffaf0', .9), (.3, '#ffe6b0', .62), (.62, '#ffb8a0', .45), (.86, '#e08cff', .55), (.96, '#ffe9ff', .85), (1, '#ffffff', 0)])
    d += rad('bCore', CX, CY, 150, [(0, '#ffffff', 1), (.3, '#fffbe8', .95), (.7, '#ffe2a0', .5), (1, '#ffcf70', 0)])
    d += lin('bPanel', [(0, '#3b5fa8'), (1, '#16284f')], x2=1, y2=1)
    d += lin('bHull', [(0, '#f1f1ec'), (.5, '#b9bcc2'), (1, '#55595f')], x2=0, y2=1)
    b = '<rect width="1920" height="1080" fill="#030308"/>'
    b += stars(220, 1070, col='#dfe8ff', op=.5, sparks=0)
    b += f'<circle cx="{CX}" cy="{CY}" r="900" fill="url(#bHalo)"/>'
    # X-ray streaks radiating
    for k in range(64):
        a = random.uniform(0, 2 * math.pi); r0 = R * random.uniform(.7, 1.0); r1 = r0 + random.uniform(250, 900)
        col = random.choice(['#e8f6ff', '#fff3d0', '#e7d0ff'])
        b += (f'<line x1="{CX + r0 * math.cos(a):.0f}" y1="{CY + r0 * math.sin(a):.0f}" x2="{CX + r1 * math.cos(a):.0f}" y2="{CY + r1 * math.sin(a):.0f}" '
              f'stroke="{col}" stroke-width="{random.choice([1.5, 2, 3])}" opacity="{random.uniform(.08, .28):.2f}"/>')
    # plasma sphere
    b += f'<circle cx="{CX}" cy="{CY}" r="{R + 40}" fill="#d48bff" opacity=".22" filter="url(#b30)"/>'
    b += f'<circle cx="{CX}" cy="{CY}" r="{R}" fill="url(#bShell)"/>'
    # filaments inside the bubble
    fil = ''
    for k in range(70):
        a = random.uniform(0, 2 * math.pi); rr = R * random.uniform(.25, .95)
        x0 = CX + rr * math.cos(a); y0 = CY + rr * math.sin(a)
        a2 = a + random.uniform(.3, .9); rr2 = R * random.uniform(.3, .96)
        x2 = CX + rr2 * math.cos(a2); y2 = CY + rr2 * math.sin(a2)
        qx = CX + (rr + rr2) * .6 * math.cos((a + a2) / 2); qy = CY + (rr + rr2) * .6 * math.sin((a + a2) / 2)
        col = random.choice(['#fff4dc', '#ffc4f0', '#ffd79a', '#e2c6ff'])
        fil += f'<path d="M{x0:.0f} {y0:.0f} Q{qx:.0f} {qy:.0f} {x2:.0f} {y2:.0f}" fill="none" stroke="{col}" stroke-width="{random.choice([2, 3, 5])}" opacity="{random.uniform(.15, .45):.2f}"/>'
    b += f'<g filter="url(#b4)">{fil}</g>'
    # bright shell rim and inner rim
    b += f'<circle cx="{CX}" cy="{CY}" r="{R - 6}" fill="none" stroke="#fff0ff" stroke-width="10" opacity=".55" filter="url(#b4)"/>'
    b += f'<circle cx="{CX}" cy="{CY}" r="{R * .62:.0f}" fill="none" stroke="#ffe7b8" stroke-width="5" opacity=".25" filter="url(#b4)"/>'
    b += f'<circle cx="{CX}" cy="{CY}" r="150" fill="url(#bCore)"/>'
    b += f'<circle cx="{CX}" cy="{CY}" r="46" fill="#fff" filter="url(#b12)"/>'
    b += f'<circle cx="{CX}" cy="{CY}" r="150" fill="#fff6d0" opacity=".55" filter="url(#b30)"/>'
    for ang in range(0, 360, 45):
        a = math.radians(ang + 22); L = 300 if ang % 90 == 0 else 190
        b += f'<line x1="{CX}" y1="{CY}" x2="{CX + L * math.cos(a):.0f}" y2="{CY + L * math.sin(a):.0f}" stroke="#fff" stroke-width="5" opacity=".55" filter="url(#b4)"/>'
    b += f'<g filter="url(#b4)" opacity=".5">' + trefoil(CX, CY, 132, '#fff3b0', '#fff3b0') + '</g>' + trefoil(CX, CY, 125, '#ffd21f', '#1b1b16')
    # ---- spacecraft (lower left of the sphere), lit hard on the sphere side, blow-off puffs ----
    SX, SY = 800, 770
    sc = f'<g transform="translate({SX} {SY}) rotate(-18)">'
    for px in (-250, 70):   # solar panels
        sc += f'<rect x="{px}" y="-34" width="180" height="68" fill="url(#bPanel)" stroke="#0b0f1c" stroke-width="4"/>'
        for gx in range(1, 6):
            sc += f'<line x1="{px + gx * 30}" y1="-34" x2="{px + gx * 30}" y2="34" stroke="#7fa3e6" stroke-width="1.6" opacity=".6"/>'
        sc += f'<line x1="{px}" y1="0" x2="{px + 180}" y2="0" stroke="#7fa3e6" stroke-width="1.6" opacity=".6"/>'
        sc += f'<rect x="{px}" y="-34" width="180" height="10" fill="#ffd6a0" opacity=".55"/>'
    sc += '<rect x="-70" y="-6" width="140" height="12" fill="#888" stroke="#0b0f1c" stroke-width="3"/>'
    sc += '<rect x="-60" y="-62" width="120" height="124" rx="10" fill="url(#bHull)" stroke="#0b0f1c" stroke-width="5"/>'
    sc += '<rect x="-60" y="-62" width="120" height="124" rx="10" fill="#c9a24a" opacity=".35"/>'  # gold foil tint
    sc += '<path d="M-40 -60 L-40 60 M0 -60 L0 60 M40 -60 L40 60" stroke="#6a5a2a" stroke-width="2" opacity=".5"/>'
    sc += '<path d="M-60 -50 Q-60 -62 -48 -62 L48 -62 Q60 -62 60 -50" fill="none" stroke="#fff3c4" stroke-width="9" opacity=".95"/>'
    sc += '<path d="M60 -50 L60 50" stroke="#ffe2a8" stroke-width="7" opacity=".85"/>'
    sc += '<path d="M10 -62 L10 -100 M10 -100 q-24 -10 -44 4" fill="none" stroke="#d8dbe2" stroke-width="5"/>'  # antenna dish
    sc += '<path d="M-36 -108 q24 -18 50 -6 q-26 16 -50 6z" fill="#e6e8ee" stroke="#0b0f1c" stroke-width="3"/>'
    sc += '</g>'
    # blow-off puffs (skin vapour bursting toward the source)
    puff = ''
    r3 = random.Random(9)
    for k in range(22):
        t = r3.uniform(0, 1); px = SX - 20 + t * 120 + r3.randint(-20, 40); py = SY - 70 - t * 30 + r3.randint(-20, 10)
        dx, dy = 60 + r3.randint(0, 90), -30 - r3.randint(0, 70)
        puff += f'<circle cx="{px + dx:.0f}" cy="{py + dy:.0f}" r="{r3.randint(8, 22)}" fill="{r3.choice(["#ffd9a8", "#fff1d6", "#ffb47a"])}" opacity="{r3.uniform(.25, .6):.2f}"/>'
    b += f'<g filter="url(#b4)">{puff}</g>' + sc
    b += f'<ellipse cx="{SX + 40}" cy="{SY - 70}" rx="80" ry="40" fill="#ffd9a0" opacity=".35" filter="url(#b12)"/>'
    # ---- frog: helmet, both arms pressed to the helmet sides (covering ears), squinting at the flash ----
    b += frog(300, 1000, 3.0, look=(5, -3), mouth='wow', helmet=True, rot=6, pupil=3.4,
              armL='M-34 -24 q-26 -10 -22 -44', armR='M38 -24 q26 -10 22 -44',
              feet=((-24, 6, -14), (24, 2, 18)))
    for ang in (-150,-120,-90,-60,-30):
        c=math.radians(ang); b += f'<line x1="{300+175*math.cos(c):.0f}" y1="{885+175*math.sin(c):.0f}" x2="{300+225*math.cos(c):.0f}" y2="{885+225*math.sin(c):.0f}" stroke="#fff3b0" stroke-width="7" stroke-linecap="round"/>'
    # dotted "sound" arcs fading out next to the frog = nothing arrives
    for k, (r, op) in enumerate(((190, .5), (240, .3), (290, .14))):
        b += f'<path d="M{300 + r * math.cos(math.radians(-40)):.0f} {850 + r * math.sin(math.radians(-40)):.0f} A{r} {r} 0 0 1 {300 + r * math.cos(math.radians(20)):.0f} {850 + r * math.sin(math.radians(20)):.0f}" fill="none" stroke="#cfe6ff" stroke-width="7" stroke-dasharray="4 22" stroke-linecap="round" opacity="{op}"/>'
    for x, y, s in ((880, 300, 18), (1650, 160, 22), (1720, 760, 16), (960, 640, 12), (560, 600, 14)):
        b += spark(x, y, s)
    return page('#030308', svg(d, b), [('A', 130, 'w'), ('SILENT', 250, 'y'), ('FLASH', 220, 'w')], top=40)


# =====================================================================================
# C: intuitive - Starfish Prime from a Hawaiian beach: flash, auroras, streetlights going dark
# =====================================================================================
def make_C():
    random.seed(37)
    H = 770
    d = GLOW
    d += lin('cSky', [(0, '#03040c'), (.45, '#0a0f26'), (.8, '#1a1b3a'), (1, '#2c2140')])
    d += lin('cSea', [(0, '#141a33'), (.3, '#0a1024'), (1, '#04060f')])
    d += lin('cSand', [(0, '#2a2420'), (1, '#0e0c0b')])
    d += ('<linearGradient id="cCurt" x1="0" y1="1" x2="0" y2="0">'
          '<stop offset="0" stop-color="#7dffb0" stop-opacity=".0"/><stop offset=".08" stop-color="#7dffb0" stop-opacity=".9"/>'
          '<stop offset=".35" stop-color="#3fe08a" stop-opacity=".55"/><stop offset=".62" stop-color="#ff4f6e" stop-opacity=".5"/>'
          '<stop offset="1" stop-color="#c0306a" stop-opacity="0"/></linearGradient>')
    d += rad('cFlash', 1480, 230, 520, [(0, '#ffffff', 1), (.08, '#f4fbff', .95), (.22, '#bfe4ff', .45), (.5, '#7aa6ff', .12), (1, '#7aa6ff', 0)])
    d += rad('cLamp', 0, 0, 60, [(0, '#fff3c8', 1), (.3, '#ffc964', .6), (1, '#ffb040', 0)])
    b = '<rect width="1920" height="1080" fill="url(#cSky)"/>'
    b += stars(140, 600, col='#e6eeff', op=.5, sparks=0)
    # aurora curtains along a wave over the Pacific
    cur = ''
    for i in range(170):
        x = 760 + i * 7.2
        base = 640 + 40 * math.sin(i / 14) + 18 * math.sin(i / 5.3)
        h = 260 + 120 * math.sin(i / 9 + 1) + random.randint(-40, 40)
        cur += f'<rect x="{x:.0f}" y="{base - h:.0f}" width="{random.choice([5, 7, 9])}" height="{h:.0f}" fill="url(#cCurt)" opacity="{random.uniform(.35, .85):.2f}"/>'
    b += f'<g filter="url(#b4)">{cur}</g>'
    b += '<ellipse cx="1340" cy="620" rx="620" ry="120" fill="#43e08e" opacity=".18" filter="url(#b30)"/>'
    b += '<ellipse cx="1300" cy="430" rx="560" ry="110" fill="#ff4f6e" opacity=".14" filter="url(#b30)"/>'
    # the flash, 400 km up
    b += '<circle cx="1480" cy="230" r="520" fill="url(#cFlash)"/>'
    b += '<circle cx="1480" cy="230" r="54" fill="#fff" filter="url(#b12)"/>'
    for ang in range(0, 360, 30):
        a = math.radians(ang + 15); L = 250 if ang % 60 == 0 else 150
        b += f'<line x1="1480" y1="230" x2="{1480 + L * math.cos(a):.0f}" y2="{230 + L * math.sin(a):.0f}" stroke="#fff" stroke-width="4" opacity=".5" filter="url(#b4)"/>'
    # distant mountain island on the horizon with a few lit / dark windows
    b += f'<path d="M560 {H} Q640 {H - 90} 720 {H - 120} Q800 {H - 150} 860 {H - 96} Q930 {H - 60} 1010 {H}Z" fill="#0b0d1a"/>'
    b += f'<path d="M720 {H - 120} Q800 {H - 150} 860 {H - 96}" fill="none" stroke="#7fe0b0" stroke-width="3" opacity=".35"/>'
    for k in range(26):
        x = random.randint(600, 990); y = random.randint(H - 26, H - 4)
        on = random.random() < .3
        b += f'<circle cx="{x}" cy="{y}" r="2.6" fill="{"#ffd27a" if on else "#2a2c3a"}" opacity="{.95 if on else .9}"/>'
    # sea + reflections
    b += f'<rect x="0" y="{H}" width="1920" height="{1080 - H}" fill="url(#cSea)"/>'
    refl = ''
    for i in range(80):
        x = 780 + i * 14 + random.randint(-6, 6); y = H + random.randint(6, 220)
        col = random.choice(['#5dff9a', '#5dff9a', '#ff5f7e'])
        refl += f'<rect x="{x}" y="{y}" width="{random.randint(18, 60)}" height="3" fill="{col}" opacity="{random.uniform(.12, .35):.2f}"/>'
    for i in range(40):
        y = H + 8 + i * 7; w = 14 + i * 2.4
        refl += f'<rect x="{1480 - w / 2 + random.randint(-14, 14):.0f}" y="{y}" width="{w:.0f}" height="3" fill="#dff1ff" opacity="{.5 - i * .011:.2f}"/>'
    b += f'<g filter="url(#b4)">{refl}</g>'
    b += f'<line x1="0" y1="{H}" x2="1920" y2="{H}" stroke="#9fc6ff" stroke-width="2" opacity=".35"/>'
    # beach (foreground) - sand strip, left to centre
    b += '<path d="M0 900 Q500 860 1100 900 Q1350 925 1520 1080 L0 1080Z" fill="url(#cSand)"/>'
    b += '<path d="M0 900 Q500 860 1100 900 Q1350 925 1520 1080" fill="none" stroke="#cfe4ff" stroke-width="4" opacity=".35"/>'
    b += '<path d="M40 912 Q500 876 1080 914" fill="none" stroke="#e8f4ff" stroke-width="3" opacity=".2"/>'
    # promenade streetlights receding to the right: far ones still lit, near ones dead with sparks
    lamps = [(1130, 990, 470), (1290, 935, 300), (1390, 900, 200), (1460, 876, 140), (1510, 860, 100), (1546, 849, 74)]
    for i, (x, yb, h) in enumerate(lamps):
        s = h / 470; top = yb - h
        on = i >= 3
        b += f'<path d="M{x} {yb} L{x} {top + 30 * s:.0f} Q{x} {top:.0f} {x - 40 * s:.0f} {top:.0f} L{x - 70 * s:.0f} {top:.0f}" fill="none" stroke="#0b0b10" stroke-width="{max(3, 14 * s):.1f}" stroke-linecap="round"/>'
        b += f'<path d="M{x + 5 * s:.1f} {yb} L{x + 5 * s:.1f} {top + 30 * s:.0f}" stroke="#7fa0d0" stroke-width="{max(1, 3 * s):.1f}" opacity=".35"/>'
        hx, hy = x - 76 * s, top + 6 * s
        b += f'<path d="M{hx - 34 * s:.1f} {hy:.1f} L{hx + 22 * s:.1f} {hy:.1f} L{hx + 12 * s:.1f} {hy + 18 * s:.1f} L{hx - 24 * s:.1f} {hy + 18 * s:.1f}Z" fill="#141418" stroke="#0b0b10" stroke-width="{max(1.5, 4 * s):.1f}"/>'
        if on:
            b += f'<g transform="translate({hx - 6 * s:.1f} {hy + 24 * s:.1f}) scale({s * 1.4:.2f})"><circle r="60" fill="url(#cLamp)"/></g>'
            b += f'<ellipse cx="{hx - 6 * s:.1f}" cy="{hy + 20 * s:.1f}" rx="{20 * s:.1f}" ry="{6 * s:.1f}" fill="#fff6d6"/>'
        else:
            b += f'<ellipse cx="{hx - 6 * s:.1f}" cy="{hy + 20 * s:.1f}" rx="{20 * s:.1f}" ry="{6 * s:.1f}" fill="#3a3d48" stroke="#0b0b10" stroke-width="{max(1, 2 * s):.1f}"/>'
            # electric zaps (EMP) on the dead lamps
            zx, zy = hx - 6 * s, hy + 10 * s
            for k in range(3):
                a = math.radians(-150 + k * 60 + random.randint(-10, 10)); L = 60 * s
                b += (f'<path d="M{zx + 26 * s * math.cos(a):.0f} {zy + 26 * s * math.sin(a):.0f} l{L * .4 * math.cos(a) + 8 * s:.0f} {L * .4 * math.sin(a):.0f} '
                      f'l{-10 * s:.0f} {6 * s:.0f} l{L * .5 * math.cos(a) + 6 * s:.0f} {L * .5 * math.sin(a):.0f}" fill="none" stroke="#9fe8ff" stroke-width="{max(2, 6 * s):.1f}" stroke-linejoin="round" opacity=".9"/>')
            b += f'<circle cx="{zx:.0f}" cy="{zy:.0f}" r="{40 * s:.0f}" fill="#7fdcff" opacity=".22" filter="url(#b12)"/>'
    # ---- frog on the beach in a flower lei, looking up at the sky, one arm pointing ----
    lei = ''
    for k in range(11):
        t = k / 10; x = -30 + 70 * t; y = -30 + 16 * math.sin(math.pi * t)
        col = ['#ff7aa8', '#ffd35a', '#ffffff', '#ff9d5c'][k % 4]
        lei += f'<circle cx="{x:.1f}" cy="{y:.1f}" r="6.5" fill="{col}" stroke-width="2"/><circle cx="{x:.1f}" cy="{y:.1f}" r="2" fill="#c0306a" stroke="none"/>'
    b += '<ellipse cx="520" cy="1012" rx="130" ry="18" fill="#000" opacity=".35"/>'
    b += frog(520, 1000, 3.1, look=(5, -4), mouth='o', rot=6,
              armR='M38 -26 q22 -16 26 -56', mid=lei)
    for x, y, s in ((980, 130, 18), (1800, 520, 16), (1150, 330, 14), (1720, 90, 20)):
        b += spark(x, y, s)
    return page('#03040c', svg(d, b), [('400 KM UP,', 160, 'w'), ('LIGHTS', 230, 'y'), ('OUT', 230, 'w')], top=46)


for name, fn in (('A', make_A), ('B', make_B), ('C', make_C)):
    open(os.path.join(HERE, f'{name}.html'), 'w').write(fn())
print('ok')
