# Shorts thumbnail A for kardashev-scale-short4 (guideline 16-9: VERTICAL 1080x1920, text centred). Run: python3 make.py
# Layout: empty starry sky (top) with the moon, text centred in the silent sky, dish (lower right) sending rings up, frog + flat-line monitor lower left.
# WHY SO / SILENT?   intuitive: a huge radio telescope dish on a night plateau listening to an empty sky, its signal rings going
#                    out and nothing coming back; the frog in headphones beside a monitor that shows only a flat line.
#                    (script: "why is the cosmos so silent?", "The silence of the cosmos is real, in the sense that we have not
#                     detected a signal. But the explanation is open.")
import os, sys, math, random
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
sys.path.insert(0, os.path.join(REPO, 'tools'))
LONG = os.path.join(REPO, 'videos', 'kardashev-scale', 'thumb', 'make.py')
G = {'__file__': LONG}; exec(open(LONG).read().split('\nfor n, fn in')[0], G)
frog, starfield, nebula, galaxy, FILTERS, P, INK = G['frog'], G['starfield'], G['nebula'], G['galaxy'], G['FILTERS'], G['P'], G['INK']
from thumb_lib import vpage, vsvg, lin, rad, spark


def make():
    rnd = random.Random(44)
    dx, dy, drx, dry, drot = 1270, 430, 330, 150, -24      # dish bowl (opening faces up-left)
    d = FILTERS
    d += lin('sky', [(0, '#030914'), (.6, '#071a2a'), (1, '#0d2a36')], 0, 1)
    d += lin('gnd', [(0, '#0a1418'), (1, '#03070a')], 0, 1)
    d += rad('moonG', 1730, 150, 520, [(0, '#e8f6ff', .55), (.25, '#9fd4ff', .2), (1, '#4a8ab0', 0)])
    d += rad('bowl', dx + 120, dy - 60, 420, [(0, '#eaf2f8', 1), (.55, '#a8b8c8', 1), (1, '#4a5a6a', 1)])
    d += rad('scr', 975, 880, 160, [(0, '#5affb0', .6), (1, '#5affb0', 0)])
    d += rad('vig', 540, 960, 1150, [(0, '#000', 0), (.7, '#000', 0), (1, '#000', .6)])
    d += rad('moonV', 860, 260, 620, [(0, '#e8f6ff', .5), (.25, '#9fd4ff', .18), (1, '#4a8ab0', 0)])
    d += rad('txtBg', 540, 950, 560, [(0, '#02060c', .5), (.6, '#02060c', .25), (1, '#02060c', 0)])
    d += lin('skyV', [(0, '#030914'), (.7, '#071a2a'), (1, '#0d2a36')], 0, 1)
    B = '<rect width="1080" height="1920" fill="url(#skyV)"/>'
    B += nebula(rnd, 10, (0, 0, 1080, 1500), ['#1a3a5a', '#2a2a6a', '#0f4a4a'], 180, 380, (.05, .12))
    B += starfield(rnd, 700, (0, 0, 1080, 1620), col='#e6f2ff')
    B += galaxy(210, 420, 130, 40, 18, rnd).replace('<g transform', '<g opacity=".55" transform')
    B += '<rect width="1080" height="1920" fill="url(#moonV)"/>'
    B += '<circle cx="860" cy="260" r="86" fill="#cfeaff" opacity=".35" filter="url(#b12)"/><path d="M890 198 A66 66 0 1 0 903 314 A56 56 0 1 1 890 198z" fill="#f4fbff"/>'
    B += '<ellipse cx="540" cy="1610" rx="900" ry="160" fill="#2a8a9a" opacity=".28" filter="url(#b50)"/>'
    B += '<path d="M0 1600 L120 1540 L250 1570 L400 1500 L560 1560 L720 1520 L860 1570 L1080 1530 V1920 H0z" fill="#0c1c24"/>'
    B += '<path d="M0 1640 Q400 1610 700 1630 T1080 1625 V1920 H0z" fill="url(#gnd)"/>'
    B += '<path d="M0 1640 Q400 1610 700 1630 T1080 1625" fill="none" stroke="#3a6a80" stroke-width="3" opacity=".6"/>'
    fxp, fyp = 1120, 250
    FX, FY = -380 + fxp * .85, 964.5 + fyp * .85
    for k in range(1, 7):     # outgoing listening rings rise into the empty sky: nothing comes back
        r = 125 * k; a0, a1 = math.radians(-150), math.radians(-30)
        B += f'<path d="M{FX + r * math.cos(a0):.0f} {FY + r * math.sin(a0):.0f} A{r} {r} 0 0 1 {FX + r * math.cos(a1):.0f} {FY + r * math.sin(a1):.0f}" fill="none" stroke="#8fe8ff" stroke-width="{8 - k}" opacity="{.8 - k * .1:.2f}" stroke-dasharray="{34 - 3 * k} 16"/>'
    B += '<rect width="1080" height="1920" fill="url(#txtBg)"/>'
    b = ''
    # ---- the dish: pedestal, truss, bowl, feed ----
    px, py = 1320, 860
    b += f'<ellipse cx="{px}" cy="{py + 6}" rx="190" ry="20" fill="#000" opacity=".55" filter="url(#b6)"/>'
    b += f'<path d="M{px - 110} {py} L{px - 40} {py - 260} L{px + 40} {py - 260} L{px + 110} {py}z" fill="#2a3a46" stroke="#0a1418" stroke-width="6"/>'
    b += f'<path d="M{px - 80} {py - 20} L{px + 30} {py - 240} M{px + 80} {py - 20} L{px - 30} {py - 240} M{px - 95} {py - 70} H{px + 95} M{px - 60} {py - 170} H{px + 60}" stroke="#4a6070" stroke-width="5"/>'
    b += f'<path d="M{px + 40} {py - 260} L{px + 110} {py}" stroke="#9fd4ff" stroke-width="4" opacity=".55"/>'
    b += f'<rect x="{px - 70}" y="{py - 320}" width="140" height="70" rx="10" fill="#3a4c5a" stroke="#0a1418" stroke-width="5"/>'
    b += f'<circle cx="{px}" cy="{py - 300}" r="34" fill="#4a5e6c" stroke="#0a1418" stroke-width="5"/>'
    # back of the bowl (rim thickness) + inner face
    t = math.radians(drot)
    b += f'<ellipse cx="{dx + 26}" cy="{dy + 30}" rx="{drx}" ry="{dry}" transform="rotate({drot} {dx + 26} {dy + 30})" fill="#1e2a34" stroke="#0a1418" stroke-width="6"/>'
    b += f'<ellipse cx="{dx}" cy="{dy}" rx="{drx + 12}" ry="{dry + 10}" transform="rotate({drot} {dx} {dy})" fill="#cfe8ff" opacity=".35" filter="url(#b12)"/>'
    b += f'<ellipse cx="{dx}" cy="{dy}" rx="{drx}" ry="{dry}" transform="rotate({drot} {dx} {dy})" fill="url(#bowl)" stroke="#0a1418" stroke-width="7"/>'
    g = f'<g transform="rotate({drot} {dx} {dy})">'
    for k in (.25, .5, .75):
        g += f'<ellipse cx="{dx + 18 * (1 - k)}" cy="{dy + 10 * (1 - k)}" rx="{drx * k:.0f}" ry="{dry * k:.0f}" fill="none" stroke="#6a7c8c" stroke-width="2.6"/>'
    for k in range(16):
        a = 2 * math.pi * k / 16
        g += f'<path d="M{dx + 18} {dy + 10} L{dx + drx * math.cos(a):.0f} {dy + dry * math.sin(a):.0f}" stroke="#6a7c8c" stroke-width="2.2"/>'
    g += f'<path d="M{dx - drx * .92:.0f} {dy - dry * .35:.0f} A{drx} {dry} 0 0 1 {dx + drx * .5:.0f} {dy - dry * .87:.0f}" fill="none" stroke="#ffffff" stroke-width="8" opacity=".7"/>'
    g += '</g>'
    b += g
    # feed horn on three struts in front of the bowl
    rim = [(dx + drx * math.cos(a) * math.cos(t) - dry * math.sin(a) * math.sin(t), dy + drx * math.cos(a) * math.sin(t) + dry * math.sin(a) * math.cos(t)) for a in (math.radians(170), math.radians(290), math.radians(50))]
    for (rx_, ry_) in rim:
        b += f'<path d="M{rx_:.0f} {ry_:.0f} L{fxp} {fyp}" stroke="#0a1418" stroke-width="10"/><path d="M{rx_:.0f} {ry_:.0f} L{fxp} {fyp}" stroke="#8a9cac" stroke-width="5"/>'
    b += f'<rect x="{fxp - 26}" y="{fyp - 22}" width="52" height="44" rx="8" fill="#5a6c7a" stroke="#0a1418" stroke-width="5" transform="rotate({drot} {fxp} {fyp})"/>'
    b += f'<circle cx="{fxp}" cy="{fyp}" r="30" fill="#8fe8ff" opacity=".45" filter="url(#b6)"/><circle cx="{fxp - 6}" cy="{fyp - 4}" r="7" fill="#e8fbff"/>'
    # red aircraft light on top
    b += f'<circle cx="{fxp}" cy="{fyp - 34}" r="14" fill="#ff5a4a" opacity=".6" filter="url(#b3)"/><circle cx="{fxp}" cy="{fyp - 34}" r="5" fill="#ff8a7a"/>'
    DISH = b; b = ''
    # ---- monitor with a flat line + frog in headphones ----
    mx, my = 975, 880
    b += f'<circle cx="{mx}" cy="{my}" r="170" fill="url(#scr)"/>'
    b += f'<path d="M{mx + 100} {my + 60} Q{mx + 300} {my + 120} 1087 935" fill="none" stroke="#0a1418" stroke-width="10"/>'
    b += f'<rect x="{mx - 60}" y="{my + 60}" width="120" height="34" rx="6" fill="#2a343c" stroke="{INK}" stroke-width="5"/>'
    b += f'<rect x="{mx - 125}" y="{my - 85}" width="250" height="160" rx="18" fill="#3a444c" stroke="{INK}" stroke-width="6"/>'
    b += f'<rect x="{mx - 105}" y="{my - 66}" width="210" height="122" rx="10" fill="#03140c"/>'
    for k in range(1, 4):
        b += f'<path d="M{mx - 105} {my - 66 + 30.5 * k:.0f} H{mx + 105}" stroke="#0f3a24" stroke-width="2"/>'
    b += f'<path d="M{mx - 100} {my - 5} H{mx + 100}" stroke="#5affb0" stroke-width="12" opacity=".5" filter="url(#b3)"/><path d="M{mx - 100} {my - 5} H{mx + 100}" stroke="#c8ffe4" stroke-width="4"/>'
    b += f'<circle cx="{mx + 100}" cy="{my - 5}" r="7" fill="#eafff4"/>'
    b += f'<path d="M{mx - 90} {my - 56} q50 -10 90 -6" stroke="#ffffff" stroke-width="4" opacity=".25" fill="none"/>'
    # crate under the frog
    b += f'<rect x="{560}" y="{905}" width="230" height="110" rx="8" fill="#6a4a2a" stroke="{INK}" stroke-width="6"/><path d="M570 960 H780 M610 910 V1010 M740 910 V1010" stroke="#4a321c" stroke-width="5"/>'
    b += f'<path d="M566 912 H784" stroke="#a8804a" stroke-width="5"/>'
    b += frog(675, 912, 2.35, rot=-4, look=(5, -7), mouth='O', armL='M-34 -22 q-24 -18 -14 -50', armR='M38 -22 q26 -16 18 -50',
              legs=((-20, -6, -30, 4, -10), (20, -6, 30, 4, 10)), brows=True, phones=True)
    b += f'<path d="M792 790 Q830 840 {mx - 125} {my - 20}" fill="none" stroke="{INK}" stroke-width="5"/>'   # headphone cable
    FROG = b
    b = B + f'<g transform="translate(-380 964.5) scale(.85)">{DISH}</g>' + f'<g transform="translate(-560 640) scale(1.12)">{FROG}</g>'
    b += spark(980, 560, 16) + spark(100, 160, 14) + spark(680, 120, 12) + spark(1000, 1240, 14)
    b += '<rect width="1080" height="1920" fill="url(#vig)"/>'
    lines = [('WHY SO', 160, 'w'), ('<span class="g">SILENT?</span>', 206, 'w')]
    return vpage('#030914', vsvg(d, b), lines, outline='#02060c', top=790)


open(os.path.join(HERE, 'A.html'), 'w').write(make())
print('ok')
