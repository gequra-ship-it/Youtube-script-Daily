import sys, os, math, random
TOOLS = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', 'tools')
sys.path.insert(0, TOOLS)
from thumb_lib import *
from hands import hand
os.chdir(os.path.dirname(os.path.abspath(__file__)))
# dark-matter-96-percent thumbnails v5 (2026-10-21, Opus thumbnail agent; v4 -> v5: B telescope redrawn in shaded 3/4 view, C rebuilt as a
# simulation-style large-scale structure with DARK MATTER / VOID callouts, owner feedback on v4).  History:  v1 (Great Wave / iceberg / book), v2 (plain halo / arcs / Bullet
# Cluster) and v3 (Project Hail Mary ship / lens / quasar) were rejected or partly rejected.  Owner on v3: develop B further; C showed only a
# quasar, no dark matter; A must be a really FAMOUS scene and dark matter must be the visible hero.
# A = homage: Caspar David Friedrich, "Wanderer above the Sea of Fog" (1818, public domain): the sea of fog is a glowing sea of dark matter
#     with tiny gold galaxies floating on it like foam (S45, S17).  Text: AN UNSEEN OCEAN (S45 "a vast, unseen ocean").
# B = intuitive: gravitational lensing computed with the point-lens equation (six lensed galaxies -> arcs / partial rings, bent star field)
#     around an unseen mass inside a blue dark-matter halo and web; telescope + tethered astronaut (S12-S13).  Text: AN INVISIBLE LENS.
# C = intuitive: the dark-matter cosmic web, galaxies as gold lanterns on its knots, a hero halo holding a spiral galaxy (S22).
#     Text: THE HIDDEN WEB (S22 "an enormous web of invisible filaments").
# Dark matter = translucent blue-indigo haze / glow only; ordinary matter = warm gold-white.
R1 = 'x="-100%" y="-100%" width="300%" height="300%"'
FX = ''.join(f'<filter id="b{s}" {R1}><feGaussianBlur stdDeviation="{s}"/></filter>' for s in [1, 2, 3, 5, 8, 14, 24, 40, 70, 120])
FX += ''.join(f'<filter id="u{s}" filterUnits="userSpaceOnUse" x="-200" y="-200" width="2320" height="1480"><feGaussianBlur stdDeviation="{s}"/></filter>'
              for s in [1, 2, 3, 6, 10, 20, 24])


def haze(id, f1, f2, seed, disp=120, blur=16, rgb=(.30, .40, 1.0), gain=1.7, bias=-.45, oct=(4, 3)):
    """translucent blue-indigo dark-matter haze: shape displaced by noise, blurred, then filled with clumpy coloured noise"""
    r, g, b_ = rgb
    return (f'<filter id="{id}" filterUnits="userSpaceOnUse" x="-200" y="-200" width="2320" height="1480">'
            f'<feTurbulence type="fractalNoise" baseFrequency="{f1}" numOctaves="{oct[0]}" seed="{seed}" result="n"/>'
            f'<feDisplacementMap in="SourceGraphic" in2="n" scale="{disp}" xChannelSelector="R" yChannelSelector="G" result="d"/>'
            f'<feGaussianBlur in="d" stdDeviation="{blur}" result="db"/>'
            f'<feTurbulence type="fractalNoise" baseFrequency="{f2}" numOctaves="{oct[1]}" seed="{seed + 3}" result="n2"/>'
            f'<feColorMatrix in="n2" type="matrix" values="0 0 0 0 {r}  0 0 0 0 {g}  0 0 0 0 {b_}  {gain} 0 0 0 {bias}" result="c"/>'
            f'<feComposite in="c" in2="db" operator="in"/></filter>')


def bg_stars(n, x0=0, x1=1920, y0=0, y1=1080, col='#dfe8ff', op=.6):
    o = ''
    for _ in range(n):
        o += (f'<circle cx="{random.uniform(x0, x1):.0f}" cy="{random.uniform(y0, y1):.0f}" r="{random.choice([.8, 1.1, 1.1, 1.5, 2.0, 2.6])}" '
              f'fill="{random.choice([col, col, "#fff3d8", "#c8d6ff"])}" opacity="{random.uniform(.15, op):.2f}"/>')
    return o


def far_gal(x, y, s, rot, col='#ffe6c0', op=.7):
    return (f'<g transform="translate({x:.0f} {y:.0f}) rotate({rot:.0f})" opacity="{op:.2f}"><ellipse rx="{s * 2.4:.1f}" ry="{s * .8:.1f}" fill="{col}" opacity=".45" filter="url(#b3)"/>'
            f'<ellipse rx="{s:.1f}" ry="{s * .35:.1f}" fill="{col}"/><circle r="{s * .3:.1f}" fill="#fff"/></g>')


def flare(x, y, L, w=3, col='#fff4dc', op=.9, ang=0, n=2):
    """diffraction-spike sparkle: n thin tapered spikes + soft dot"""
    o = f'<g transform="translate({x:.0f} {y:.0f}) rotate({ang})" style="mix-blend-mode:screen">'
    for k in range(n):
        a = k * 180 / n
        o += f'<ellipse rx="{L:.0f}" ry="{w:.1f}" fill="{col}" opacity="{op * .55:.2f}" transform="rotate({a})" filter="url(#b2)"/>'
        o += f'<ellipse rx="{L * .55:.0f}" ry="{w * .45:.1f}" fill="#fff" opacity="{op:.2f}" transform="rotate({a})"/>'
    o += f'<circle r="{w * 4:.1f}" fill="{col}" opacity="{op * .5:.2f}" filter="url(#b5)"/><circle r="{w * 1.4:.1f}" fill="#fff"/></g>'
    return o


def corner_dark(op=.9):
    return f'<ellipse cx="1900" cy="1080" rx="460" ry="270" fill="#010208" opacity="{op}" filter="url(#b70)"/>'


def W(name, d, b, lines, outline, bg='#02030a'):
    open(name, 'w', encoding='utf-8').write(page(bg, svg(FX + d, b), lines, outline))


def P(pts):
    return 'M' + ' L'.join(f'{x:.1f} {y:.1f}' for x, y in pts)



def astronaut(x, y, sc=1.0, rot=0, point_ang=25):
    """small cute astronaut (feet at x,y), right arm raised pointing; gloves drawn with hands.py"""
    a = f'<g transform="translate({x} {y}) rotate({rot}) scale({sc})">'
    a += '<rect x="-26" y="-92" width="22" height="40" rx="8" fill="#9aa2b8" stroke="#141826" stroke-width="3"/>'
    a += '<path d="M-13 -40 L-15 -3 L-3 -3 L-1 -30 L3 -30 L5 -3 L17 -3 L15 -40Z" fill="#e8ecf4" stroke="#141826" stroke-width="3" stroke-linejoin="round"/>'
    a += '<rect x="-17" y="-96" width="36" height="60" rx="14" fill="#f2f4fa" stroke="#141826" stroke-width="3"/>'
    a += '<path d="M14 -86 Q34 -104 40 -128" stroke="#141826" stroke-width="15" fill="none" stroke-linecap="round"/><path d="M14 -86 Q34 -104 40 -128" stroke="#eef1f8" stroke-width="9" fill="none" stroke-linecap="round"/>'
    a += hand(40, -128, angle=point_ang, size=9, side='R', view='back', pose='point', skin='#eef1f8', line='#141826', lw=2.2)
    a += '<path d="M-14 -84 Q-24 -64 -20 -46" stroke="#141826" stroke-width="15" fill="none" stroke-linecap="round"/><path d="M-14 -84 Q-24 -64 -20 -46" stroke="#e2e6f0" stroke-width="9" fill="none" stroke-linecap="round"/>'
    a += hand(-20, -46, angle=185, size=8, side='L', view='back', pose='fist', skin='#e2e6f0', line='#141826', lw=2.2)
    a += '<circle cx="2" cy="-114" r="22" fill="#f4f6fb" stroke="#141826" stroke-width="3"/>'
    a += '<path d="M2 -128 Q24 -126 22 -108 Q14 -98 2 -102 Z" fill="#2a2140"/><path d="M8 -124 Q20 -122 20 -112" stroke="#ffd690" stroke-width="3" fill="none" opacity=".9"/>'
    a += '<path d="M19 -130 Q26 -116 21 -100" stroke="#ffd690" stroke-width="2.5" fill="none" opacity=".85"/><path d="M19 -92 L19 -40" stroke="#ffd690" stroke-width="2.5" fill="none" opacity=".7"/>'
    return a + '</g>'


def mini_gal(x, y, s, rot=0, col='#ffcf70', op=1.0, tilt=.45):
    """a small glowing gold spiral galaxy (a 'lantern')"""
    o = f'<g transform="translate({x:.0f} {y:.0f}) rotate({rot:.0f})" opacity="{op:.2f}">'
    o += f'<ellipse rx="{s * 3.2:.1f}" ry="{s * 3.2 * tilt:.1f}" fill="{col}" opacity=".35" filter="url(#b8)"/>'
    for arm in (0, 1):
        pts = [((.15 + t / 20 * .9) * s * 1.6 * math.cos(arm * math.pi + t / 20 * 3), (.15 + t / 20 * .9) * s * 1.6 * math.sin(arm * math.pi + t / 20 * 3) * tilt) for t in range(21)]
        o += f'<path d="{P(pts)}" stroke="{col}" stroke-width="{max(1, s * .35):.1f}" fill="none" opacity=".8" stroke-linecap="round"/>'
    o += f'<ellipse rx="{s * .7:.1f}" ry="{s * .7 * max(tilt, .5):.1f}" fill="#fff4dc"/><circle r="{s * .3:.1f}" fill="#fff"/></g>'
    return o


# ======================= A: AN UNSEEN OCEAN  (homage: Caspar David Friedrich, "Wanderer above the Sea of Fog", 1818) =======================
# The sea of fog is drawn as a vast glowing sea of dark matter (blue-indigo haze); tiny gold galaxies float on it like foam (script S45:
# "tiny specks of bright foam floating on top of a vast, unseen ocean"; S17 "a much larger, invisible sea").
random.seed(4401)
HZ = 470   # horizon
d = haze('hzF', .0035, .007, 61, disp=90, blur=14, rgb=(.42, .55, 1.0), gain=1.9, bias=-.35)
d += haze('hzF2', .006, .016, 71, disp=40, blur=4, rgb=(.70, .78, 1.0), gain=2.4, bias=-1.05)
d += lin('aSky', [(0, '#03030c'), (.45, '#0c0c2c'), (.8, '#22245e'), (1, '#4a4a8a')])
d += lin('aRock', [(0, '#2a2433'), (.25, '#14111c'), (1, '#050409')])
d += f'<linearGradient id="rimG" x1="0" y1="0" x2="1920" y2="0" gradientUnits="userSpaceOnUse"><stop offset="0" stop-color="#9fb4ff"/><stop offset=".45" stop-color="#ffe2a8"/><stop offset=".62" stop-color="#ffe9c0"/><stop offset="1" stop-color="#9fb4ff"/></linearGradient>'
b = f'<rect width="1920" height="{HZ + 40}" fill="url(#aSky)"/><rect y="{HZ}" width="1920" height="{1080 - HZ}" fill="#141640"/>'
b += bg_stars(380, y1=HZ - 20)
# milky band of stars across the sky
mb = ''
for _ in range(700):
    t = random.random(); x = 1920 - t * 2100; y = 40 + t * 330 + random.gauss(0, 45)
    if y < HZ - 30:
        mb += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{random.choice([.7, 1, 1, 1.4, 1.9])}" fill="{random.choice(["#fff", "#dfe6ff", "#ffe9d0"])}" opacity="{random.uniform(.2, .8):.2f}"/>'
b += f'<path d="M1950 30 L-150 380" stroke="#7a6cc0" stroke-width="160" opacity=".13" filter="url(#b40)"/>{mb}'
for _ in range(6):
    b += far_gal(random.uniform(900, 1880), random.uniform(40, 380), random.uniform(3, 6), random.uniform(0, 180), op=.6)
# the light beyond the sea: a blazing gold-white glow on the horizon behind the wanderer
GLX = 1180
b += f'<g style="mix-blend-mode:screen"><ellipse cx="{GLX}" cy="{HZ}" rx="1000" ry="260" fill="#6a5ab8" opacity=".35" filter="url(#b70)"/>'
b += f'<ellipse cx="{GLX}" cy="{HZ}" rx="620" ry="150" fill="#ffb868" opacity=".45" filter="url(#b70)"/>'
b += f'<ellipse cx="{GLX}" cy="{HZ}" rx="320" ry="60" fill="#ffe0a8" opacity=".8" filter="url(#b24)"/>'
b += f'<ellipse cx="{GLX}" cy="{HZ}" rx="140" ry="18" fill="#fff" opacity=".95" filter="url(#b5)"/>'
for k in range(16):   # faint rays fanning up from the horizon
    a = math.radians(-170 + k * (160 / 15) + random.uniform(-3, 3)); L = random.uniform(500, 900)
    b += f'<path d="M{GLX - 14} {HZ} L{GLX + L * math.cos(a):.0f} {HZ + L * math.sin(a):.0f} L{GLX + 14} {HZ}Z" fill="#ffe2b0" opacity="{random.uniform(.04, .09):.2f}"/>'
b += '</g>'
# distant mountain ridges on both sides of the horizon (as in the painting), fading into the sea
b += f'<path d="M-20 {HZ + 10} L-20 {HZ - 60} L90 {HZ - 95} L170 {HZ - 70} L260 {HZ - 120} L360 {HZ - 60} L470 {HZ - 40} L560 {HZ + 10}Z" fill="#2a2c62" opacity=".9"/>'
b += f'<path d="M1430 {HZ + 10} L1520 {HZ - 50} L1600 {HZ - 40} L1700 {HZ - 105} L1790 {HZ - 70} L1940 {HZ - 90} L1940 {HZ + 10}Z" fill="#2a2c62" opacity=".9"/>'
b += f'<path d="M90 {HZ - 95} L170 {HZ - 70} L260 {HZ - 120} L360 {HZ - 60}" stroke="#8fa0ff" stroke-width="2" fill="none" opacity=".5"/>'
b += f'<path d="M1520 {HZ - 50} L1600 {HZ - 40} L1700 {HZ - 105} L1790 {HZ - 70} L1940 {HZ - 90}" stroke="#ffd8a8" stroke-width="2" fill="none" opacity=".5"/>'


def billow(y0, amp, step, seed):
    """top edge of a fog bank: chain of soft round billows"""
    rnd = random.Random(seed); x = -120; o = f'M-120 1100 L-120 {y0}'
    while x < 2040:
        w = step * rnd.uniform(.35, 1.7); h = amp * rnd.uniform(.2, 1.9)
        o += f' Q{x + w / 2:.0f} {y0 - h * 2:.0f} {x + w:.0f} {y0 + rnd.uniform(-amp * .9, amp * .9):.0f}'
        x += w
    return o + ' L2040 1100Z'


# fog banks of dark matter, far (pale, thin) to near (deep, big billows); crags poke through between them
banks = [(HZ + 8, 10, 120, '#5a64b8', .9), (HZ + 45, 16, 170, '#4c58b0', .9), (HZ + 110, 26, 230, '#3e4aa6', .92),
         (HZ + 200, 38, 300, '#33409c', .94), (HZ + 320, 52, 380, '#2a3590', .95), (HZ + 470, 70, 460, '#222c80', .96)]
crags = {2: f'<path d="M180 {HZ + 150} L250 {HZ + 70} L290 {HZ + 90} L340 {HZ + 30} L380 {HZ + 55} L430 {HZ + 40} L520 {HZ + 150}Z" fill="#1a1838"/>'
           f'<path d="M250 {HZ + 70} L290 {HZ + 90} L340 {HZ + 30} L380 {HZ + 55} L430 {HZ + 40}" stroke="#c8d2ff" stroke-width="2.5" fill="none" opacity=".6"/>',
         3: f'<path d="M1500 {HZ + 260} L1560 {HZ + 150} L1620 {HZ + 120} L1660 {HZ + 150} L1720 {HZ + 100} L1800 {HZ + 180} L1860 {HZ + 260}Z" fill="#15132e"/>'
            f'<path d="M1560 {HZ + 150} L1620 {HZ + 120} L1660 {HZ + 150} L1720 {HZ + 100} L1800 {HZ + 180}" stroke="#ffd8a8" stroke-width="2.5" fill="none" opacity=".55"/>',
         4: f'<path d="M-20 {HZ + 420} L-20 {HZ + 250} L60 {HZ + 230} L130 {HZ + 180} L200 {HZ + 230} L260 {HZ + 300} L300 {HZ + 420}Z" fill="#100e22"/>'
            f'<path d="M-20 {HZ + 250} L60 {HZ + 230} L130 {HZ + 180} L200 {HZ + 230} L260 {HZ + 300}" stroke="#aabaff" stroke-width="3" fill="none" opacity=".55"/>'}
foam = ''
for i, (y0, amp, step, col, op) in enumerate(banks):
    pth = billow(y0, amp, step, 900 + i)
    if i in crags:
        b += crags[i]
    d += f'<linearGradient id="fg{i}" x1="0" y1="{y0 - amp * 2}" x2="0" y2="{y0 + 260}" gradientUnits="userSpaceOnUse"><stop offset="0" stop-color="#c4ceff"/><stop offset=".18" stop-color="{col}"/><stop offset="1" stop-color="#0c0f36"/></linearGradient>'
    b += f'<path d="{pth}" fill="url(#fg{i})" opacity="{op}" filter="url(#b{3 if i < 2 else 8})"/>'
    b += f'<g filter="url(#hzF2)" opacity="{.35 + i * .05:.2f}"><path d="{pth}" fill="#fff"/></g>'
    b += f'<path d="{pth}" fill="none" stroke="url(#rimG)" stroke-width="{2 + i * .6:.1f}" opacity="{.6 - i * .09:.2f}" filter="url(#b{2 if i < 3 else 5})"/>'
    b += f'<path d="{pth}" fill="none" stroke="url(#rimG)" stroke-width="{10 + i * 4}" opacity=".18" filter="url(#b8)"/>'
    # tiny galaxies floating on this bank (smaller further away), like foam on the sea
    for _ in range(12 + i * 4):
        x = random.uniform(-20, 1940); yy = y0 + random.uniform(-amp * 1.2, 40 + i * 20); s = (1.5 + i * 1.5) * random.uniform(.6, 1.4)
        if 1560 < x and yy > 860: continue
        if 820 < x < 1520 and yy > 640: continue   # leave the foreground crag area clean
        foam += mini_gal(x, yy, s, random.uniform(-25, 25), random.choice(['#ffcf70', '#ffd890', '#ffe0a8', '#a8c4ff']), random.uniform(.6, 1))
    b += foam; foam = ''
b += f'<g filter="url(#hzF)" opacity=".55"><rect x="-50" y="{HZ + 60}" width="2020" height="{1080 - HZ}" fill="#fff"/></g>'
# a deep blue glow of the whole dark sea + light reflected on it under the horizon glow
b += f'<g style="mix-blend-mode:screen"><ellipse cx="{GLX}" cy="{HZ + 60}" rx="700" ry="110" fill="#ffcf90" opacity=".18" filter="url(#b40)"/>'
b += '<ellipse cx="960" cy="860" rx="1100" ry="260" fill="#4a5cff" opacity=".18" filter="url(#b70)"/></g>'
for x, y, L in [(260, 640, 40), (1640, 700, 46), (620, 760, 34), (1760, 560, 30), (480, 560, 28)]:
    b += flare(x, y, L, 1.8, '#ffe8c0', .8)
# the foreground crag the wanderer stands on
WX, WY = 1160, 712
CR = f'M760 1090 L800 990 L860 950 L905 880 L960 850 L1010 800 L1062 770 L1100 728 L1135 716 L1205 712 L1222 676 L1258 670 L1278 694 L1300 742 L1352 772 L1400 838 L1452 870 L1500 950 L1540 1000 L1560 1090Z'
b += f'<path d="{CR}" fill="#ffc070" opacity=".35" filter="url(#b8)"/>'
b += f'<path d="{CR}" fill="url(#aRock)"/>'
b += '<path d="M800 990 L860 950 L905 880 L960 850 L1010 800 L1062 770 L1100 728 L1135 716 L1205 712 L1222 676 L1258 670 L1278 694 L1300 742 L1352 772 L1400 838 L1452 870 L1500 950" stroke="#ffd9a0" stroke-width="3.5" fill="none" opacity=".9" filter="url(#b1)"/>'
for p in ['M960 850 L990 920 L970 1000', 'M1300 742 L1280 820 L1320 900', 'M1100 728 L1120 800 L1090 880 L1110 960', 'M1400 838 L1390 920', 'M1205 712 L1200 780 L1230 850']:
    b += f'<path d="{p}" stroke="#2c2638" stroke-width="3" fill="none" opacity=".8"/><path d="{p}" stroke="#ffd9a0" stroke-width="1.2" fill="none" opacity=".22" transform="translate(2 -1)"/>'
# the wanderer: back turned, dark coat, walking stick, wind in the hair; back-lit (gold rim all around)


def wanderer():
    o = ''
    o += '<path d="M-14 -150 L-22 -70 L-30 -2 L-12 -2 L-4 -70 L2 -150Z"/>'                       # viewer-left leg
    o += '<path d="M6 -150 L30 -92 L52 -60 L70 -38 L56 -26 L34 -50 L10 -88 Z"/>'                  # viewer-right leg, stepping up
    o += '<path d="M-36 -6 L-6 -6 L-4 2 L-40 2Z M52 -40 L78 -44 L80 -34 L54 -28Z"/>'              # boots
    o += '<path d="M-46 -298 C-52 -262 -54 -206 -50 -170 L-62 -116 C-30 -108 30 -108 66 -116 L52 -170 C56 -206 54 -262 46 -298 Q0 -314 -46 -298Z"/>'  # coat
    o += '<path d="M-44 -292 C-60 -262 -66 -226 -62 -196 L-50 -194 C-48 -224 -42 -252 -34 -276Z"/>'  # left arm
    o += '<path d="M44 -292 C60 -262 66 -228 66 -200 L54 -198 C52 -228 46 -254 36 -276Z"/>'        # right arm
    o += '<path d="M-14 -306 L14 -306 L12 -320 L-12 -320Z"/>'                                     # collar / neck
    o += '<ellipse cx="0" cy="-336" rx="21" ry="25"/>'                                           # head
    o += '<path d="M-23 -336 C-26 -350 -18 -366 -4 -364 C2 -370 14 -368 18 -360 C24 -360 28 -354 26 -348 C30 -344 28 -338 24 -336 C26 -330 22 -326 18 -326 Z"/>'  # tousled hair
    return o


b += f'<g transform="translate({WX} {WY}) scale(1.12)">'
b += f'<line x1="72" y1="-196" x2="104" y2="-6" stroke="#ffd9a0" stroke-width="9" opacity=".5" filter="url(#b3)"/>'
b += f'<g fill="#ffd090" opacity=".85" filter="url(#b3)" transform="translate(0 -1) scale(1.02)">{wanderer()}</g>'
b += f'<g fill="#ffe6b8" transform="translate(0 0) scale(1.012)">{wanderer()}</g>'
b += f'<g fill="#0b120f">{wanderer()}</g>'
b += '<path d="M-30 -290 C-34 -240 -36 -200 -34 -160" stroke="#24342a" stroke-width="3" fill="none" opacity=".7"/><path d="M0 -170 L2 -112" stroke="#24342a" stroke-width="3" opacity=".8"/>'
b += '<line x1="72" y1="-196" x2="104" y2="-6" stroke="#1a120c" stroke-width="5" stroke-linecap="round"/>'
b += hand(62, -200, angle=165, size=13, side='R', view='back', pose='hold', skin='#e2c4a0', line='#120c08', lw=2)
b += hand(-56, -196, angle=190, size=12, side='L', view='back', pose='fist', skin='#e2c4a0', line='#120c08', lw=2)
b += '</g>'
# drifting dark-matter mist in front of the crag (depth)
b += '<g filter="url(#hzF)" opacity=".6"><path d="M600 1100 C760 1000 900 1040 1000 1020 C1150 990 1300 1060 1500 1100Z" fill="#fff"/></g>'
b += corner_dark(.6)
W('A.html', d, b, [('AN', 120, 'w'), ('UNSEEN', 150, 'w'), ('OCEAN', 220, 'y')], '#05061e')


# ======================= B: AN INVISIBLE LENS  (point-lens equation: arcs + partial rings around an unseen mass) =======================
random.seed(7702)
CX, CY, TE = 1290, 500, 250
d = haze('hzB', .004, .006, 21, disp=120, blur=26, rgb=(.32, .42, 1.0), gain=1.9, bias=-.4)
d += haze('hzB2', .008, .012, 31, disp=50, blur=10, rgb=(.50, .62, 1.0), gain=2.4, bias=-.95)
d += rad('bBg', CX, CY, 1400, [(0, '#1c1a48', 1), (.3, '#0f0e30', 1), (.65, '#060718', 1), (1, '#020309', 1)])
d += rad('bVoid', CX, CY, TE * .92, [(0, '#000000', 1), (.6, '#020210', .95), (1, '#0a0c2a', 0)])
d += lin('tube', [(0, '#e8eef8'), (.25, '#aab4c8'), (.6, '#4c5468'), (1, '#1a1d2a')])
d += lin('foil', [(0, '#fff0b0'), (.3, '#e0b048'), (.7, '#9a6a1c'), (1, '#4a3008')])
d += lin('panel', [(0, '#6a5cd0'), (.5, '#2e2c80'), (1, '#141238')], 1, 1)


def lens(bx, by):
    """point lens: source offset (bx,by) -> two images [(x, y, tangential stretch, radial stretch, angle_deg, sign, |theta|)]"""
    bb = math.hypot(bx, by) or 1e-3; s = math.sqrt(bb * bb + 4 * TE * TE); ux, uy = bx / bb, by / bb
    out = []
    for th, sg in [((bb + s) / 2, 1), ((bb - s) / 2, -1)]:
        a = abs(th); q = (TE / a) ** 2
        out.append((CX + ux * th, CY + uy * th, min(1 / max(abs(1 - q), 1e-3), 30), 1 / (1 + q), math.degrees(math.atan2(uy, ux)) + 90, sg, a))
    return out


def galaxy_pts(n, R, rot, incl, cols, arms=2, wind=2.6, core=.25):
    pts = []
    for k in range(n):
        if random.random() < core:
            r = abs(random.gauss(0, R * .22)); a = random.uniform(0, 2 * math.pi); c = cols[0]; w = 1.0
        else:
            arm = random.randrange(arms); t = random.random() ** .9; a = arm * 2 * math.pi / arms + t * wind + random.gauss(0, .2)
            r = (.15 + t * .85) * R + random.gauss(0, R * .06); c = random.choice(cols); w = .8
        x, y = r * math.cos(a), r * math.sin(a) * incl
        cr, sr = math.cos(rot), math.sin(rot)
        pts.append((x * cr - y * sr, x * sr + y * cr, c, w))
    return pts


b = '<rect width="1920" height="1080" fill="url(#bBg)"/>'
# dark-matter halo + web of the lens: translucent blue-indigo haze, darkest at the centre
web = [(f'M{CX} {CY} C1000 700 700 760 250 1150', 170), (f'M{CX} {CY} C1600 300 1750 120 2100 -60', 180), (f'M{CX} {CY} C1700 640 1900 660 2150 760', 130),
       (f'M{CX} {CY} C1100 200 1000 0 960 -200', 130), (f'M{CX} {CY} C900 450 500 380 -100 300', 110), (f'M{CX} {CY} C1450 800 1500 1000 1480 1200', 120)]
b += f'<g filter="url(#hzB)" opacity=".95"><circle cx="{CX}" cy="{CY}" r="{TE * 2.0:.0f}" fill="#fff"/>' + ''.join(f'<path d="{p}" stroke="#fff" stroke-width="{w}" fill="none"/>' for p, w in web) + '</g>'
b += f'<g filter="url(#hzB2)" opacity=".55"><circle cx="{CX}" cy="{CY}" r="{TE * 1.65:.0f}" fill="none" stroke="#fff" stroke-width="160"/>' + ''.join(f'<path d="{p}" stroke="#fff" stroke-width="36" fill="none"/>' for p, w in web) + '</g>'
b += ''.join(f'<path d="{p}" stroke="#9fb2ff" stroke-width="3" fill="none" opacity=".22" filter="url(#b3)"/>' for p, w in web)
b += f'<circle cx="{CX}" cy="{CY}" r="{TE * 2.05:.0f}" fill="none" stroke="#a8b8ff" stroke-width="10" opacity=".18" filter="url(#b14)"/>'
# cluster galaxies glowing inside the halo and along the web (ordinary matter, gold)
for _ in range(30):
    a = random.uniform(0, 2 * math.pi); r = random.uniform(TE * 1.25, TE * 2.1)
    x, y = CX + r * math.cos(a), CY + r * math.sin(a) * .9
    if x < 820 and y < 560: continue
    if x > 1600 and y > 860: continue
    s = random.uniform(2.5, 6)
    b += f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{s * 4:.0f}" ry="{s * 3:.0f}" fill="#ffc870" opacity=".3" filter="url(#b5)"/><ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{s:.1f}" ry="{s * .75:.1f}" fill="#ffe8b8"/>'
b += f'<circle cx="{CX}" cy="{CY}" r="{TE * .92:.0f}" fill="url(#bVoid)"/>'
# background star field bent around the lens: stars near the ring are stretched into short arcs (drawn over the transparent haze)
st = ''
for _ in range(2200):
    bx, by = random.uniform(-1380, 720), random.uniform(-600, 660)
    r0 = random.choice([.9, 1.2, 1.2, 1.6, 2.1, 2.8]); op = random.uniform(.25, .9); col = random.choice(['#e4ecff', '#e4ecff', '#fff1d6', '#bcd0ff'])
    for x, y, tg, rd, ang, sg, a in lens(bx, by):
        if not (0 <= x <= 1920 and 0 <= y <= 1080): continue
        o2 = op if sg > 0 else op * min(1, .3 * (a / TE) ** 4)
        if o2 < .06: continue
        st += f'<ellipse cx="{x:.1f}" cy="{y:.1f}" rx="{r0 * min(tg, 10):.1f}" ry="{max(.6, r0 * rd):.1f}" transform="rotate({ang:.0f} {x:.1f} {y:.1f})" fill="{col}" opacity="{o2:.2f}"/>'
b += st
# warm light behind the arcs
b += f'<circle cx="{CX}" cy="{CY}" r="{TE * 1.45:.0f}" fill="#ffaa50" opacity=".13" filter="url(#b70)" style="mix-blend-mode:screen"/>'
# lensed background galaxies: several distinct sources -> arcs, counter-images and partial rings (deep gold and blue)
SRC = [((48, -40), 88, .5, .6, ['#fff0c0', '#ffb848', '#ffc860', '#ffa838', '#ffd890'], 3600, .62),
       ((-26, 22), 40, 1.0, .7, ['#e8f0ff', '#8fb0ff', '#a8c4ff', '#7a9cff'], 1800, .6),
       ((-125, 82), 52, 1.2, .55, ['#ffe0b0', '#ff9a40', '#ffb060', '#ff8a30'], 1500, .65),
       ((112, 132), 46, 2.2, .5, ['#f0f4ff', '#a8c4ff', '#cfe0ff', '#8fb0ff'], 1300, .65),
       ((-68, -150), 42, .3, .6, ['#fff0c8', '#ffc860', '#ffd890'], 1200, .65),
       ((175, -55), 30, 1.8, .6, ['#ffe0c0', '#ff8f60', '#ffb080'], 800, .6)]
arcs = ''
for (sx, sy), R, rot, incl, cols, n, op in SRC:
    for px, py, c, w in galaxy_pts(n, R, rot, incl, cols):
        for x, y, tg, rd, ang, sg, a in lens(sx + px, sy + py):
            if sg < 0 and a < TE * .4: continue
            o2 = op * w * (1 if sg > 0 else .75)
            arcs += f'<ellipse cx="{x:.1f}" cy="{y:.1f}" rx="{2.2 * min(tg, 14):.1f}" ry="{max(1.4, 2.4 * rd):.1f}" transform="rotate({ang:.0f} {x:.1f} {y:.1f})" fill="{c}" opacity="{o2:.2f}"/>'
b += f'<g id="arcs" filter="url(#u1)">{arcs}</g>'
b += '<use href="#arcs" filter="url(#u6)" opacity=".55" style="mix-blend-mode:screen"/>'
b += '<use href="#arcs" filter="url(#u20)" opacity=".75" style="mix-blend-mode:screen"/>'
b += f'<circle cx="{CX}" cy="{CY}" r="{TE}" fill="none" stroke="#ffb850" stroke-width="26" opacity=".22" filter="url(#b14)" style="mix-blend-mode:screen"/>'
b += f'<circle cx="{CX}" cy="{CY}" r="{TE}" fill="none" stroke="#ffe0a0" stroke-width="1.6" opacity=".35"/>'
# lens glints on the brightest knots
g1 = lens(48, -40)[0]; g2 = lens(-26, 22)[0]; g3 = lens(-125, 82)[0]
b += flare(g1[0], g1[1], 160, 3.2, '#ffe2a8', .95, 8) + flare(g2[0], g2[1], 90, 2.4, '#d8e4ff', .8, 30) + flare(g3[0], g3[1], 70, 2.2, '#ffd8a0', .8, 20)
b += f'<ellipse cx="{g1[0]:.0f}" cy="{g1[1]:.0f}" rx="800" ry="4" fill="#ffe8c0" opacity=".45" filter="url(#b2)" style="mix-blend-mode:screen"/>'
b += f'<ellipse cx="{g1[0]:.0f}" cy="{g1[1]:.0f}" rx="600" ry="22" fill="#90b0ff" opacity=".12" filter="url(#b14)" style="mix-blend-mode:screen"/>'
b += flare(1720, 130, 50, 2, '#dfe8ff', .7) + flare(960, 900, 36, 1.8, '#dfe8ff', .6) + spark(1830, 560, 14, '#d6dfff') + spark(870, 640, 12)
# the space telescope, lower left, aimed at the ring (3/4 view: aperture toward the lens, barrel shaded as a cylinder, rim light
# from the lens glow on the upper edge, blue bounce light from the haze below); a tethered astronaut points at the arcs (scale)
TX, TY, TA = 470, 805, -30
TR_, RX_ = 66, 21          # barrel radius, perspective half-width of the round ends
d += (f'<linearGradient id="tBar" x1="0" y1="{-TR_}" x2="0" y2="{TR_}" gradientUnits="userSpaceOnUse">'
      '<stop offset="0" stop-color="#fff0d0"/><stop offset=".05" stop-color="#f4f2ee"/><stop offset=".2" stop-color="#cdd3df"/><stop offset=".45" stop-color="#8a92a6"/>'
      '<stop offset=".75" stop-color="#3e4558"/><stop offset=".93" stop-color="#22283a"/><stop offset="1" stop-color="#4c5c9a"/></linearGradient>')
d += (f'<linearGradient id="tFoil" x1="0" y1="{-TR_ - 8}" x2="0" y2="{TR_ + 8}" gradientUnits="userSpaceOnUse">'
      '<stop offset="0" stop-color="#fff6c8"/><stop offset=".08" stop-color="#f6cf68"/><stop offset=".35" stop-color="#c8902e"/><stop offset=".7" stop-color="#6c4412"/>'
      '<stop offset=".93" stop-color="#3a2408"/><stop offset="1" stop-color="#6a5a8a"/></linearGradient>')
d += lin('tPan', [(0, '#5a4ccc'), (.45, '#2c2a86'), (1, '#16144a')], 1, 1)
d += lin('tDoor', [(0, '#fff2d8'), (.3, '#d8dce6'), (1, '#5a6276')], 1, 1)
d += rad('tAp', 0, 0, TR_, [(0, '#1a2244', 1), (.7, '#070a18', 1), (1, '#02030a', 1)])
d += lin('tDish', [(0, '#ffffff'), (.5, '#c8cedc'), (1, '#5a6276')], 1, 1)


def cyl(x0, x1, R, rx, fill, stroke='#0b0d18'):
    """cylinder side seen 3/4 from the +x end: rectangle with the hidden far end bulging toward -x"""
    return f'<path d="M{x1} {-R} L{x0} {-R} A{rx} {R} 0 0 0 {x0} {R} L{x1} {R} Z" fill="{fill}" stroke="{stroke}" stroke-width="2.5"/>'


def wing(p, shade):
    """solar wing as a perspective quad p = [inner-top, inner-bottom, outer-bottom, outer-top] with a 3 x 8 cell grid"""
    (ax, ay), (bx, by), (cx_, cy_), (dx, dy) = p
    o = f'<path d="M{ax} {ay} L{bx} {by} L{cx_} {cy_} L{dx} {dy}Z" fill="#b8c0d2" stroke="#0b0d18" stroke-width="3"/>'
    def at(u, v):   # u across (a->b), v outward (inner->outer)
        x0, y0 = ax + (dx - ax) * v, ay + (dy - ay) * v; x1, y1 = bx + (cx_ - bx) * v, by + (cy_ - by) * v
        return x0 + (x1 - x0) * u, y0 + (y1 - y0) * u
    for i in range(3):
        for j in range(8):
            g = .06
            q = [at(i / 3 + g / 3, j / 8 + g / 8), at((i + 1) / 3 - g / 3, j / 8 + g / 8), at((i + 1) / 3 - g / 3, (j + 1) / 8 - g / 8), at(i / 3 + g / 3, (j + 1) / 8 - g / 8)]
            o += f'<path d="{P(q)}Z" fill="url(#tPan)"/>'
            o += f'<path d="M{q[0][0]:.1f} {q[0][1]:.1f} L{q[1][0]:.1f} {q[1][1]:.1f}" stroke="#a8a4ff" stroke-width="1" opacity=".45"/>'
    sx0, sy0 = at(0, .15); sx1, sy1 = at(1, .55)   # diagonal sheen of the glow on the cells
    o += f'<path d="M{at(0, .05)[0]:.0f} {at(0, .05)[1]:.0f} L{at(.6, 0)[0]:.0f} {at(.6, 0)[1]:.0f} L{at(1, .35)[0]:.0f} {at(1, .35)[1]:.0f} L{at(.4, .6)[0]:.0f} {at(.4, .6)[1]:.0f}Z" fill="#ffe0b0" opacity="{shade}" filter="url(#b8)"/>'
    o += f'<path d="M{ax} {ay} L{dx} {dy}" stroke="#ffe6b8" stroke-width="2.5" opacity=".8"/>'
    return o


R = TR_
tel = f'<g transform="translate({TX} {TY}) rotate({TA})">'
tel += '<ellipse cx="0" cy="0" rx="330" ry="220" fill="#ffc070" opacity=".12" filter="url(#b40)"/>'
# far solar wing (behind the barrel) on its boom
tel += f'<rect x="-48" y="{-R - 30}" width="9" height="34" fill="#4a5064" stroke="#0b0d18" stroke-width="2"/>'
tel += wing([(-104, -R - 30), (-8, -R - 30), (16, -R - 232), (-64, -R - 232)], .3)
# aft shroud (gold foil) and the main barrel
tel += cyl(-240, -146, R + 8, RX_ + 2, 'url(#tFoil)')
for k in range(7):
    xx = -232 + k * 13
    tel += f'<path d="M{xx} {-R - 6} q{random.uniform(-4, 4):.0f} {R * .6:.0f} {random.uniform(-3, 3):.0f} {R:.0f} q{random.uniform(-4, 4):.0f} {R * .6:.0f} {random.uniform(-3, 3):.0f} {R + 4}" stroke="#5a360a" stroke-width="1.4" fill="none" opacity=".5"/>'
tel += f'<path d="M-146 {-R - 8} A{RX_ + 2} {R + 8} 0 0 0 -146 {R + 8}" stroke="#2a1a04" stroke-width="3" fill="none"/>'
tel += cyl(-150, 176, R, RX_, 'url(#tBar)')
for xx in (-96, -20, 60, 128):   # equipment-bay seams following the curvature
    tel += f'<path d="M{xx} {-R} A{RX_} {R} 0 0 0 {xx} {R}" stroke="#141826" stroke-width="3" fill="none" opacity=".75"/>'
    tel += f'<path d="M{xx + 3} {-R + 2} A{RX_} {R - 2} 0 0 0 {xx + 3} {R - 2}" stroke="#eef2fa" stroke-width="1.2" fill="none" opacity=".35"/>'
for xx in (-130, -60, 20, 96):   # small access panels and bolts
    tel += f'<rect x="{xx}" y="{-R * .2:.0f}" width="22" height="26" rx="2" fill="none" stroke="#1e2232" stroke-width="1.5" opacity=".6"/>'
    tel += ''.join(f'<circle cx="{xx + bx_}" cy="{-R * .2 + by_:.0f}" r="1.3" fill="#1e2232" opacity=".7"/>' for bx_, by_ in [(3, 3), (19, 3), (3, 23), (19, 23)])
# handrail along the top
tel += f'<path d="M-120 {-R - 7} L150 {-R - 7}" stroke="#f2d27a" stroke-width="3.5" fill="none"/>'
tel += ''.join(f'<line x1="{xx}" y1="{-R - 7}" x2="{xx}" y2="{-R}" stroke="#c8a040" stroke-width="2.5"/>' for xx in range(-110, 160, 45))
# rim light from the lens on the upper edge + bounce light on the lower edge
tel += f'<path d="M176 {-R} L-150 {-R} A{RX_} {R} 0 0 0 {-150 - RX_ * .7:.0f} {-R * .7:.0f}" stroke="#fff2d0" stroke-width="4" fill="none" opacity=".95" filter="url(#b1)"/>'
tel += f'<path d="M176 {-R} L-150 {-R}" stroke="#ffc870" stroke-width="16" fill="none" opacity=".35" filter="url(#b5)"/>'
tel += f'<path d="M-150 {R} L176 {R}" stroke="#7f9cff" stroke-width="3" fill="none" opacity=".55"/>'
# aperture: lip, dark tube interior, secondary-mirror spider, a gold reflection of the arcs in the mirror
tel += f'<ellipse cx="176" cy="0" rx="{RX_}" ry="{R}" fill="#aab2c4" stroke="#0b0d18" stroke-width="2.5"/>'
tel += f'<ellipse cx="178" cy="0" rx="{RX_ * .78:.1f}" ry="{R * .86:.1f}" fill="url(#tAp)"/>'
tel += f'<path d="M178 {-R * .86:.1f} L178 {R * .86:.1f} M{178 - RX_ * .78:.1f} 0 L{178 + RX_ * .78:.1f} 0" stroke="#3a4258" stroke-width="1.4"/>'
tel += '<ellipse cx="178" cy="0" rx="5" ry="12" fill="#2a3048" stroke="#5a6278" stroke-width="1"/>'
tel += f'<path d="M{178 - RX_ * .5:.1f} {R * .5:.0f} A{RX_ * .55:.1f} {R * .62:.1f} 0 0 1 {178 + RX_ * .1:.1f} {-R * .58:.0f}" stroke="#ffc860" stroke-width="3" fill="none" opacity=".85" filter="url(#b1)"/>'
tel += f'<path d="M{176 - RX_ * .2:.1f} {-R:.0f} A{RX_} {R} 0 0 1 {176 + RX_:.0f} 0" stroke="#fff4dc" stroke-width="3" fill="none" opacity=".95"/>'
# aperture door, hinged at the top of the opening, swung open toward the lens
tel += f'<path d="M166 {-R - 2} L182 {-R - 4} L190 {-R - 10}" stroke="#4a5064" stroke-width="6" fill="none"/><circle cx="180" cy="{-R - 3}" r="5" fill="#8a92a6" stroke="#0b0d18" stroke-width="2"/>'
tel += f'<g transform="translate(200 {-R - 50}) rotate(-62)"><ellipse rx="64" ry="20" fill="url(#tDoor)" stroke="#0b0d18" stroke-width="2.5"/>'
tel += '<ellipse rx="52" ry="13" fill="none" stroke="#7a8296" stroke-width="1.5" opacity=".7"/><path d="M-62 -6 A64 20 0 0 1 60 -8" stroke="#fff4dc" stroke-width="3" fill="none"/></g>'
# near solar wing (in front), larger: it is closer to us
tel += f'<rect x="-52" y="{R - 2}" width="10" height="34" fill="#4a5064" stroke="#0b0d18" stroke-width="2"/>'
tel += wing([(-108, R + 30), (-4, R + 30), (-6, R + 300), (-136, R + 300)], .22)
# high-gain antenna on a boom under the barrel
tel += f'<path d="M70 {R} L96 {R + 74}" stroke="#4a5064" stroke-width="5"/><path d="M70 {R} L96 {R + 74}" stroke="#c8cedc" stroke-width="1.5"/>'
tel += f'<g transform="translate(100 {R + 86}) rotate(-24)"><ellipse rx="40" ry="15" fill="url(#tDish)" stroke="#0b0d18" stroke-width="2.5"/>'
tel += '<ellipse rx="30" ry="9" fill="none" stroke="#8a92a6" stroke-width="1.2"/><line x1="0" y1="0" x2="0" y2="-22" stroke="#2a3048" stroke-width="2"/><circle cx="0" cy="-23" r="3" fill="#c8cedc"/>'
tel += '<path d="M-38 -5 A40 15 0 0 1 36 -7" stroke="#fff2d0" stroke-width="2.5" fill="none"/></g>'
# star trackers, nav lights, tiny thruster puffs with glints
tel += f'<path d="M-170 {-R - 8} l-10 -22 l22 -6 l6 20Z" fill="#8a92a6" stroke="#0b0d18" stroke-width="2"/><circle cx="-176" cy="{-R - 26}" r="3" fill="#1a2040"/>'
tel += f'<circle cx="-30" cy="{-R + 14}" r="3.5" fill="#ff6a50"/><circle cx="-30" cy="{-R + 14}" r="9" fill="#ff6a50" opacity=".45" filter="url(#b3)"/>'
tel += f'<circle cx="150" cy="{R - 16}" r="3" fill="#7affc0"/><circle cx="150" cy="{R - 16}" r="8" fill="#7affc0" opacity=".45" filter="url(#b3)"/>'
for px_, py_, ang_ in [(-240, -R + 6, 200), (-238, R - 6, 160)]:
    tel += f'<g transform="translate({px_} {py_}) rotate({ang_})"><ellipse cx="22" cy="0" rx="26" ry="6" fill="#bfe0ff" opacity=".55" filter="url(#b3)"/><ellipse cx="12" cy="0" rx="10" ry="2.5" fill="#fff" opacity=".9"/></g>'
tel += '</g>'
b += tel
b += flare(TX + 176 * .866 + 70, TY - 176 * .5 - 30, 40, 1.8, '#fff0d0', .9, 15)
b += '<path d="M520 694 C600 650 690 690 750 676" stroke="#dfe6f2" stroke-width="2.5" fill="none" opacity=".85"/>'
b += astronaut(790, 690, .62, 20, 30)

b += corner_dark(.8)
W('B.html', d, b, [('AN', 120, 'w'), ('INVISIBLE', 150, 'y'), ('LENS', 210, 'w')], '#07061a')


# ======================= C: THE HIDDEN WEB  (cosmic large-scale structure: dark-matter filaments and knots, empty voids) =======================
# Script S22: "dark matter clumped together first, building an enormous web of invisible filaments. Ordinary gas then fell into the thickest
# knots of that web and lit up as stars and galaxies."  Look of the Millennium / IllustrisTNG renders: the web is the boundary network of
# Voronoi cells (cells = voids).  Dark matter = blue-indigo glow along filaments and knots; galaxies = gold specks in the knots.
# Two callouts (HTML labels + leader lines): DARK MATTER -> a thick filament knot, VOID (MOSTLY EMPTY) -> a void.
import numpy as np
from scipy.spatial import Voronoi
random.seed(5521); np.random.seed(5521)
VOIDC = (1245, 640)   # the labelled void


def seeds(n, mind, x0, y0, x1, y1, fixed=(), keep_out=None):
    pts = list(fixed); tries = 0
    while len(pts) < n and tries < 40000:
        tries += 1; p = (random.uniform(x0, x1), random.uniform(y0, y1))
        if keep_out and math.hypot(p[0] - keep_out[0][0], p[1] - keep_out[0][1]) < keep_out[1]: continue
        if all(math.hypot(p[0] - q[0], p[1] - q[1]) > mind for q in pts): pts.append(p)
    return pts


def edges_of(pts, clip=(-260, -260, 2180, 1340)):
    vor = Voronoi(np.array(pts)); out = []
    for (i, j) in vor.ridge_vertices:
        if i < 0 or j < 0: continue
        (xa, ya), (xb, yb) = vor.vertices[i], vor.vertices[j]
        if min(xa, xb) < clip[0] or max(xa, xb) > clip[2] or min(ya, yb) < clip[1] or max(ya, yb) > clip[3]: continue
        out.append((i, j, (xa, ya), (xb, yb)))
    return vor, out


def wiggle(a, b_, amp, n=14, rr=None):
    rr = rr or random; L = math.hypot(b_[0] - a[0], b_[1] - a[1]) or 1; nx, ny = -(b_[1] - a[1]) / L, (b_[0] - a[0]) / L
    ph = [rr.uniform(0, 6.3) for _ in range(3)]; pts = []
    for k in range(n + 1):
        t = k / n; e = math.sin(math.pi * t)
        off = amp * e * (math.sin(t * 5 + ph[0]) * .75 + math.sin(t * 9 + ph[1]) * .25)
        pts.append((a[0] + (b_[0] - a[0]) * t + nx * off, a[1] + (b_[1] - a[1]) * t + ny * off))
    return pts


d = rad('cBg', 1200, 560, 1500, [(0, '#070718', 1), (.5, '#040410', 1), (1, '#020308', 1)])
d += ('<filter id="grainW" filterUnits="userSpaceOnUse" x="-200" y="-200" width="2320" height="1480"><feTurbulence type="fractalNoise" baseFrequency=".02" numOctaves="2" seed="9"/>'
      '<feDisplacementMap in="SourceGraphic" scale="16" xChannelSelector="R" yChannelSelector="G"/></filter>')
d += haze('hzL', .005, .009, 77, disp=50, blur=16, rgb=(.30, .40, 1.0), gain=2.0, bias=-.35, oct=(2, 2))
d += rad('txtDark', 300, 260, 700, [(0, '#020308', .85), (.6, '#020308', .55), (1, '#020308', 0)])
b = '<rect width="1920" height="1080" fill="url(#cBg)"/>'
b += bg_stars(60, op=.3)

# ---- far, fine web (side filaments, small cells), dim
P2 = seeds(260, 85, -250, -250, 2170, 1330)
vor2, E2 = edges_of(P2)
far_core = ''; far_dots = ''
for i, j, a, b_ in E2:
    mx, my = (a[0] + b_[0]) / 2, (a[1] + b_[1]) / 2
    if math.hypot(mx - VOIDC[0], my - VOIDC[1]) < 230: continue
    w = random.lognormvariate(-.3, .5)
    pts = wiggle(a, b_, 6)
    far_core += f'<path d="{P(pts)}" stroke="#7a8cff" stroke-width="{.8 + w * 1.2:.1f}" fill="none" opacity="{min(.5, .15 + w * .15):.2f}"/>'
    L = math.hypot(b_[0] - a[0], b_[1] - a[1])
    for _ in range(int(L / 45 * w)):
        t = random.random(); x = a[0] + (b_[0] - a[0]) * t + random.gauss(0, 4); y = a[1] + (b_[1] - a[1]) * t + random.gauss(0, 4)
        far_dots += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{random.choice([.6, .8, 1.1])}" fill="#b8c6ff" opacity="{random.uniform(.2, .6):.2f}"/>'
b += f'<g filter="url(#u3)" opacity=".8">{far_core}</g><g style="mix-blend-mode:screen">{far_dots}</g>'

# ---- main web (big cells = voids), bright dark-matter filaments
P1 = seeds(46, 250, -300, -300, 2220, 1380, fixed=[VOIDC], keep_out=(VOIDC, 400))
vor1, E1 = edges_of(P1)
deg = {}; mass = {}
EW = []
for i, j, a, b_ in E1:
    w = min(2.8, random.lognormvariate(-.15, .65))
    EW.append((i, j, a, b_, w))
    for v in (i, j):
        deg[v] = deg.get(v, 0) + 1; mass[v] = mass.get(v, 0) + w
glow = ''; mid = ''; core = ''; dots = ''; side = ''; cloud = ''; gold_f = ''
for i, j, a, b_, w in EW:
    rr = random.Random(i * 1000 + j)
    pts = wiggle(a, b_, 18 + w * 6, 16, rr)
    pp = P(pts)
    glow += f'<path d="{pp}" stroke="#3446d8" stroke-width="{40 + w * 50:.0f}" fill="none" opacity="{.2 + w * .12:.2f}" stroke-linecap="round"/>'
    cloud += f'<path d="{pp}" stroke="#fff" stroke-width="{24 + w * 40:.0f}" fill="none" opacity="{min(1, .35 + w * .3):.2f}" stroke-linecap="round"/>'
    mid += f'<path d="{pp}" stroke="#6f86ff" stroke-width="{5 + w * 8:.0f}" fill="none" opacity="{.35 + w * .15:.2f}" stroke-linecap="round"/>'
    core += f'<path d="{pp}" stroke="#dfe8ff" stroke-width="{.8 + w * 1.6:.1f}" fill="none" opacity="{min(.9, .15 + w * .3):.2f}" stroke-linecap="round"/>'
    for _ in range(int(w * w * 3)):   # a few gold galaxies along the strong filaments too
        k_ = random.randrange(len(pts)); gx_, gy_ = pts[k_][0] + random.gauss(0, 6), pts[k_][1] + random.gauss(0, 6)
        gold_f += f'<circle cx="{gx_:.0f}" cy="{gy_:.0f}" r="4.5" fill="#ffb850" opacity=".4" filter="url(#b3)"/><circle cx="{gx_:.0f}" cy="{gy_:.0f}" r="1.6" fill="#ffe6b0"/>'
    # simulation grain along the filament: dense blue-white particles, thicker in strong filaments
    L = math.hypot(b_[0] - a[0], b_[1] - a[1])
    for _ in range(int(L / 18 * w)):
        k = random.random() * (len(pts) - 1); k0 = int(k); f = k - k0; k1 = min(k0 + 1, len(pts) - 1)
        x = pts[k0][0] + (pts[k1][0] - pts[k0][0]) * f + random.gauss(0, 3 + w * 5); y = pts[k0][1] + (pts[k1][1] - pts[k0][1]) * f + random.gauss(0, 3 + w * 5)
        dots += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{random.choice([.7, .9, 1.2, 1.6])}" fill="{random.choice(["#c8d4ff", "#e8eeff", "#9fb0ff"])}" opacity="{random.uniform(.3, .85):.2f}"/>'
    # short side filaments branching off into the voids
    for _ in range(int(w * 2)):
        t = random.uniform(.2, .8); k0 = int(t * (len(pts) - 1)); x0, y0 = pts[k0]
        ang = math.atan2(b_[1] - a[1], b_[0] - a[0]) + random.choice([-1, 1]) * random.uniform(.9, 1.6); Ls = random.uniform(40, 110)
        x1, y1 = x0 + Ls * math.cos(ang), y0 + Ls * math.sin(ang)
        if math.hypot(x1 - VOIDC[0], y1 - VOIDC[1]) < 200: continue
        sp = wiggle((x0, y0), (x1, y1), 6, 8, rr)
        side += f'<path d="{P(sp)}" stroke="#8fa2ff" stroke-width="{1 + w * .6:.1f}" fill="none" opacity=".45" stroke-linecap="round"/>'
b += f'<g filter="url(#u20)" style="mix-blend-mode:screen">{glow}</g>'
b += f'<g filter="url(#hzL)" style="mix-blend-mode:screen">{cloud}</g>'
b += f'<g filter="url(#u6)" style="mix-blend-mode:screen" opacity=".8">{mid}</g>'
b += f'<g filter="url(#u1)" style="mix-blend-mode:screen">{side}</g>'
b += f'<g filter="url(#u1)" style="mix-blend-mode:screen">{core}</g>'
b += f'<g style="mix-blend-mode:screen">{dots}{gold_f}</g>'
# knots (Voronoi vertices): dense dark-matter clumps with gold galaxies sitting in them
kn = ''; gold = ''; best = []
for v, m in mass.items():
    x, y = vor1.vertices[v]
    if not (-60 < x < 1980 and -60 < y < 1140): continue
    s = m / 3
    best.append((m, x, y))
    kn += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{50 + s * 70:.0f}" fill="#4a5cff" opacity="{min(.7, .25 + s * .18):.2f}" filter="url(#b24)"/>'
    kn += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{12 + s * 16:.0f}" fill="#b8c6ff" opacity="{min(.8, .3 + s * .2):.2f}" filter="url(#b8)"/>'
    for _ in range(int(60 * s)):
        r_ = abs(random.gauss(0, 8 + s * 10)); a_ = random.uniform(0, 6.3)
        kn += f'<circle cx="{x + r_ * math.cos(a_):.0f}" cy="{y + r_ * math.sin(a_):.0f}" r="{random.choice([.8, 1.1, 1.5])}" fill="#eef2ff" opacity="{random.uniform(.4, .95):.2f}"/>'
    for _ in range(int(3 + s * 6)):
        r_ = abs(random.gauss(0, 6 + s * 8)); a_ = random.uniform(0, 6.3); gx, gy = x + r_ * math.cos(a_), y + r_ * math.sin(a_)
        sz = random.uniform(1.5, 3.0) * (.9 + s * .35)
        gold += f'<circle cx="{gx:.0f}" cy="{gy:.0f}" r="{sz * 3:.1f}" fill="#ffb850" opacity=".45" filter="url(#b3)"/><circle cx="{gx:.0f}" cy="{gy:.0f}" r="{sz:.1f}" fill="#ffe6b0"/>'
b += f'<g style="mix-blend-mode:screen">{kn}{gold}</g>'
best.sort(reverse=True)
for m, x, y in best[:7]:
    if (x < 820 and y < 600) or (x > 1580 and y > 860): continue
    b += flare(x, y, 30 + m * 12, 1.4 + m * .25, '#ffe8c0', .85, random.uniform(0, 40))
# the void: a dark bubble with only a few faint galaxies (very little matter)
b += f'<circle cx="{VOIDC[0]}" cy="{VOIDC[1]}" r="170" fill="#010207" opacity=".55" filter="url(#b40)"/>'
for _ in range(7):
    a_ = random.uniform(0, 6.3); r_ = random.uniform(40, 150)
    b += f'<circle cx="{VOIDC[0] + r_ * math.cos(a_):.0f}" cy="{VOIDC[1] + r_ * math.sin(a_):.0f}" r="1.2" fill="#c8d4ff" opacity=".5"/>'
# depth: out-of-focus near filaments crossing close to the camera
b += '<g filter="url(#b24)" opacity=".5" style="mix-blend-mode:screen"><path d="M-120 1180 C150 1000 360 960 620 1180" stroke="#4a5cff" stroke-width="70" fill="none"/>'
b += '<path d="M1580 -120 C1680 60 1800 140 2060 180" stroke="#4a5cff" stroke-width="60" fill="none"/></g>'
b += '<g filter="url(#b8)" opacity=".7" style="mix-blend-mode:screen"><path d="M-120 1180 C150 1000 360 960 620 1180" stroke="#a8b8ff" stroke-width="10" fill="none"/></g>'
# keep the headline area calm, darken the bottom-right corner
b += '<rect width="1920" height="1080" fill="url(#txtDark)"/>'
b += corner_dark(.85)

# ---- callouts: leader lines in SVG, labels as HTML
cands = [(m, x, y) for m, x, y in best if 1300 < x < 1720 and 300 < y < 520 and math.hypot(x - VOIDC[0], y - VOIDC[1]) > 200]
DMx, DMy = (cands[0][1], cands[0][2]) if cands else (1560, 330)
LBx, LBy = max(800, DMx - 640), max(60, DMy - 260)   # DARK MATTER label up-left of the knot, leader goes down-right
VLx, VLy = VOIDC
lead = lambda x0, y0, x1, y1: (f'<path d="M{x0:.0f} {y0:.0f} L{x1:.0f} {y1:.0f}" stroke="#05061a" stroke-width="9" stroke-linecap="round"/>'
                               f'<path d="M{x0:.0f} {y0:.0f} L{x1:.0f} {y1:.0f}" stroke="#ffffff" stroke-width="3.5" stroke-linecap="round"/>'
                               f'<circle cx="{x1:.0f}" cy="{y1:.0f}" r="11" fill="none" stroke="#05061a" stroke-width="8"/><circle cx="{x1:.0f}" cy="{y1:.0f}" r="11" fill="none" stroke="#fff" stroke-width="3.5"/>')
ang = math.atan2(DMy - LBy - 30, DMx - LBx - 180)
b += lead(LBx + 330, LBy + 34, DMx - 14 * math.cos(ang), DMy - 14 * math.sin(ang))
LBL = ('<div style="position:absolute;left:{x}px;top:{y}px;font-family:Fredoka,sans-serif;font-weight:700;font-size:{s}px;letter-spacing:2px;line-height:1;'
       'color:{c};-webkit-text-stroke:10px #05061a;paint-order:stroke fill;text-align:center;white-space:nowrap">{t}</div>')
labels = LBL.format(x=LBx, y=LBy, s=62, c='#c9d6ff', t='DARK MATTER')
labels += LBL.format(x=VLx - 70, y=VLy - 40, s=64, c='#ffffff', t='VOID')
labels += LBL.format(x=VLx - 118, y=VLy + 30, s=34, c='#ffffff', t='MOSTLY EMPTY')
open('C.html', 'w', encoding='utf-8').write(page('#02030a', svg(FX + d, b) + labels, [('THE', 130, 'w'), ('HIDDEN', 150, 'w'), ('WEB', 260, 'y')], '#07061a'))
print('ok', DMx, DMy)
