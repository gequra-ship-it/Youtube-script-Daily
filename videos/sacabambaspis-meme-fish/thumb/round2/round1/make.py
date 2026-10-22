# sacabambaspis-meme-fish thumbnails A-C (guideline 16-6). run: python3 make.py  (writes A.html B.html C.html here)
# A  WHY THIS FACE?       homage: the Mona Lisa in the Louvre (famous portrait behind glass, crowd of raised phones): the
#    portrait is the googly-eyed Helsinki model posed like the Mona Lisa in front of a hazy sfumato landscape.
#    Script S02 (model in the Finnish Museum of Natural History, viral photo 2022), S40 ("why did a fish model become an
#    internet star? Part of the answer is the face").
# B  PART SCIENCE, PART ART   intuitive: one face split down the middle: left = the fossil fish (small eyes in bony rings
#    at the very front, slit mouth, armor with oak-leaf bumps, warm shallow sea); right = the smooth silvery museum model with
#    a googly doll eye and open mouth under a gallery spotlight. Script S11-S12 ("The goofy look is partly science and
#    partly art"), S03 (silvery glaze, craft-store googly doll's eyes), S19 (oak-leaf bumps).
# C  A SINGLE BAD DAY     homage: Hokusai, "The Great Wave off Kanagawa" (public domain): a muddy storm wave curls over a
#    shallow sea, small fish tumble in it like the boats, a barren cone in place of Fuji, a large accurate Sacabambaspis in
#    the trough. Script S26-S27 (30+ fish packed together, "probably caused by a powerful storm", "a rare snapshot of a single
#    bad day", flood of muddy fresh water); also nods to S02 (the 2023 Japanese boom).
import os, sys, math, random
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', '..', 'tools'))
from thumb_lib import *
from hands import hand

LINE = '#1b2022'


def blur(id, sd):
    return f'<filter id="{id}" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="{sd}"/></filter>'


def rg(id, stops, cx=.5, cy=.5, r=.5, fx=None, fy=None):
    f = f' fx="{fx}" fy="{fy}"' if fx is not None else ''
    return f'<radialGradient id="{id}" cx="{cx}" cy="{cy}" r="{r}"{f}>' + ''.join(
        f'<stop offset="{o}" stop-color="{c}" stop-opacity="{a}"/>' for o, c, a in stops) + '</radialGradient>'


# ------------------------------------------------------------------ the accurate fish, side view (art_brief sheet)
# local units: snout at x=0 facing LEFT, tail tip at x~1060, belly +y. Head shield ~1/3 of the length, eyes at the very
# front close together in bony rings, slit mouth, no jaws/teeth/side fins, thin whip-like tail with a tiny tail fin.
SHIELD = 'M0,5 C0,-70 60,-118 150,-124 C240,-128 315,-108 350,-80 C365,-30 368,30 352,78 C300,108 200,118 130,112 C55,104 5,70 0,5 Z'
BODY = 'M330,-88 C450,-92 560,-62 690,-30 C780,-18 880,-10 952,-7 L952,7 C880,10 780,18 690,30 C560,64 450,98 330,92 Z'
FIN = 'M940,-6 C982,-34 1030,-32 1052,-14 C1043,-1 1047,18 1062,40 C1016,40 978,24 940,8 Z'


def saca(gid, tr, seed=1, armor='#9aa5a8', body='#7d7a5c', bump='#dcb766', rim='#fff0c4', line=LINE, detail=1.0, op=1):
    rnd = random.Random(seed)
    d = (rg(gid + 'sg', [(0, '#eef3f0', 1), (.35, armor, 1), (.8, '#56626a', 1), (1, '#323b40', 1)], cx=.3, cy=.22, r=.85)
         + lin(gid + 'bg', [(0, '#c4bd94'), (.38, body), (1, '#2c2a20')])
         + lin(gid + 'fg', [(0, '#d8d2ae'), (1, '#5f5c44')])
         + f'<clipPath id="{gid}cs"><path d="{SHIELD}"/></clipPath><clipPath id="{gid}cb"><path d="{BODY}"/></clipPath>')
    o = f'<g transform="{tr}" opacity="{op}">'
    # tail fin + body
    o += f'<path d="{FIN}" fill="url(#{gid}fg)" stroke="{line}" stroke-width="4" stroke-linejoin="round"/>'
    o += ''.join(f'<path d="M948,{a * .2:.0f} L{1030 + abs(a) * .2:.0f},{a:.0f}" stroke="#4a4836" stroke-width="2" opacity=".6"/>' for a in (-26, -14, -2, 12, 26))
    o += f'<path d="{BODY}" fill="url(#{gid}bg)" stroke="{line}" stroke-width="5" stroke-linejoin="round"/>'
    sc = ''
    for i in range(-14, 34):     # diamond scale lattice
        x0 = 300 + i * 22
        sc += f'<path d="M{x0},-110 l130,220 M{x0 + 130},-110 l-130,220"/>'
    o += f'<g clip-path="url(#{gid}cb)"><g stroke="#2b2a1e" stroke-width="2.4" opacity=".55" fill="none">{sc}</g>'
    if detail > .5:
        o += ''.join(f'<ellipse cx="{340 + k * 22 + (j % 2) * 11}" cy="{-70 + j * 13}" rx="4" ry="2.2" fill="#f4ecc8" opacity=".35"/>' for k in range(16) for j in range(0, 6))
    o += f'<rect x="300" y="15" width="700" height="100" fill="#1e1c14" opacity=".35"/></g>'
    # head shield
    o += f'<path d="{SHIELD}" fill="url(#{gid}sg)" stroke="{line}" stroke-width="5.5" stroke-linejoin="round"/>'
    o += f'<g clip-path="url(#{gid}cs)">'
    o += f'<path d="M20,110 C120,60 250,58 380,70 L380,140 L0,140 Z" fill="#20282c" opacity=".45"/>'   # belly shadow
    # branchial band of small plates + gill openings between dorsal and ventral shields
    o += '<path d="M50,34 C150,22 260,24 360,28 L360,54 C260,50 150,52 54,58 Z" fill="#46525a" opacity=".85"/>'
    o += ''.join(f'<path d="M{x},{31 - (x - 50) * .02:.1f} l-2,24" stroke="{line}" stroke-width="2" opacity=".7"/>' for x in range(70, 360, 18))
    o += ''.join(f'<ellipse cx="{x}" cy="42" rx="5.5" ry="8" fill="#0c1012"/>' for x in range(236, 352, 17))
    # oak-leaf bumps
    n = int(190 * detail)
    for _ in range(n):
        x = rnd.uniform(14, 352); y = rnd.uniform(-126, 112)
        if ((x - 180) / 182) ** 2 + (y / 122) ** 2 > 1 or 22 < y < 60: continue
        a = math.degrees(math.atan2(y + 10, x + 40)) + rnd.uniform(-20, 20)
        sh = .55 + .45 * (1 - (y + 126) / 240)
        s = rnd.uniform(.8, 1.25)
        o += (f'<g transform="translate({x:.0f} {y:.0f}) rotate({a:.0f}) scale({s:.2f})">'
              f'<path d="M-8,0 C-6,-4 -2,-4 0,-2 C2,-5 6,-4 8,0 C6,4 2,5 0,2 C-2,4 -6,4 -8,0Z" fill="#20282c" opacity=".5" transform="translate(1.5 2)"/>'
              f'<path d="M-8,0 C-6,-4 -2,-4 0,-2 C2,-5 6,-4 8,0 C6,4 2,5 0,2 C-2,4 -6,4 -8,0Z" fill="{bump}" opacity="{sh:.2f}"/></g>')
    # sensory canals with pores, two small pits near the front
    o += f'<g fill="none" stroke="{line}" stroke-width="2.4" stroke-dasharray="2 9" stroke-linecap="round" opacity=".75"><path d="M60,-70 C150,-100 250,-98 345,-66"/><path d="M50,-4 C140,-20 260,-18 352,0"/><path d="M110,84 C190,96 280,90 350,66"/></g>'
    o += f'<ellipse cx="100" cy="-96" rx="6" ry="4" fill="#161b1d"/><ellipse cx="122" cy="-102" rx="6" ry="4" fill="#161b1d"/>'
    o += '</g>'
    # eyes at the very front, close together, each in a bony ring (far eye peeks above the near one)
    for (ex, ey, r) in ((30, -60, 21), (52, -34, 27)):
        o += (f'<circle cx="{ex}" cy="{ey}" r="{r + 9}" fill="#c9bf98" stroke="{line}" stroke-width="4"/>'
              f'<circle cx="{ex}" cy="{ey}" r="{r + 9}" fill="none" stroke="#f3ead0" stroke-width="3" stroke-dasharray="4 5" opacity=".8"/>'
              f'<circle cx="{ex}" cy="{ey}" r="{r}" fill="#0c1114" stroke="{line}" stroke-width="2.5"/>'
              f'<circle cx="{ex - r * .35:.1f}" cy="{ey - r * .38:.1f}" r="{r * .3:.1f}" fill="#fff" opacity=".95"/>'
              f'<circle cx="{ex + r * .32:.1f}" cy="{ey + r * .3:.1f}" r="{r * .12:.1f}" fill="#bfe8ff" opacity=".8"/>')
    # narrow slit mouth with a thin lower lip of tiny scale strips (no jaw, no teeth)
    o += f'<path d="M3,28 C25,34 55,36 86,34 C62,46 28,46 3,28 Z" fill="#0e0f10" stroke="{line}" stroke-width="3"/>'
    o += ''.join(f'<path d="M{10 + i * 9},{45 + i * .3:.1f} l-2,10" stroke="#e6dcbc" stroke-width="2" opacity=".6"/>' for i in range(8))
    # rim light along the back
    o += f'<path d="M4,-30 C14,-85 70,-118 150,-124 C240,-128 315,-108 350,-80 M362,-88 C460,-90 560,-62 690,-30 C780,-18 880,-10 950,-8" fill="none" stroke="{rim}" stroke-width="6" stroke-linecap="round" opacity=".9"/>'
    o += f'<ellipse cx="150" cy="-78" rx="80" ry="22" fill="#ffffff" opacity=".28" transform="rotate(-8 150 -78)"/>'
    return d, o + '</g>'


# ------------------------------------------------------------------ the Helsinki museum model, front face (cartoon-simple)
def model_face(gid, tr, look=(0, 0), mouth=1.0):
    """local: face centre 0,0, about 660 wide and 470 tall. Smooth silvery glaze, two googly doll eyes close together at
    the front top, small dark open mouth."""
    d = (rg(gid + 'm', [(0, '#ffffff', 1), (.25, '#dfe6e8', 1), (.65, '#9aa6ab', 1), (1, '#4b555b', 1)], cx=.36, cy=.28, r=.8)
         + rg(gid + 'w', [(0, '#ffffff', 1), (.75, '#f1f1ee', 1), (1, '#b9bcbc', 1)], cx=.4, cy=.35, r=.65)
         + rg(gid + 'k', [(0, '#3a1212', 1), (1, '#0b0607', 1)], cx=.5, cy=.3, r=.7))
    o = f'<g transform="{tr}">'
    o += f'<path d="M-330,30 C-338,-150 -190,-240 0,-240 C190,-240 338,-150 330,30 C322,165 190,228 0,228 C-190,228 -322,165 -330,30 Z" fill="url(#{gid}m)" stroke="{LINE}" stroke-width="7"/>'
    o += '<path d="M-250,-120 C-200,-200 -90,-222 10,-220" fill="none" stroke="#fff" stroke-width="16" stroke-linecap="round" opacity=".55"/>'
    for sx in (-1, 1):
        ex, ey = sx * 108, -70
        o += f'<circle cx="{ex}" cy="{ey + 6}" r="98" fill="#2a3034" opacity=".35"/>'
        o += f'<circle cx="{ex}" cy="{ey}" r="94" fill="url(#{gid}w)" stroke="{LINE}" stroke-width="6"/>'
        px, py = ex + look[0] * sx * -1 + (sx * -18), ey + 28 + look[1]
        o += f'<circle cx="{px:.0f}" cy="{py:.0f}" r="44" fill="#0b0b0c"/><circle cx="{px - 14:.0f}" cy="{py - 16:.0f}" r="11" fill="#fff"/>'
        o += f'<ellipse cx="{ex - 30}" cy="{ey - 48}" rx="26" ry="12" fill="#fff" opacity=".9" transform="rotate(-25 {ex - 30} {ey - 48})"/>'
    m = mouth
    o += f'<path d="M-62,{96} C-30,{88} 30,{88} 62,{96} C42,{96 + 70 * m:.0f} 18,{100 + 92 * m:.0f} 0,{102 + 96 * m:.0f} C-18,{100 + 92 * m:.0f} -42,{96 + 70 * m:.0f} -62,96 Z" fill="url(#{gid}k)" stroke="{LINE}" stroke-width="6" stroke-linejoin="round"/>'
    return d, o + '</g>'


# ============================================================ A: WHY THIS FACE?  (homage: Mona Lisa in the Louvre)
def build_A():
    random.seed(11)
    d = (lin('aw', [(0, '#3b1d17'), (.55, '#5a2c20'), (1, '#1d0e0a')])
         + rad('aspot', 1310, 470, 760, [(0, '#ffd9a0', .55), (.45, '#e09a5a', .18), (1, '#e09a5a', 0)])
         + lin('agold', [(0, '#fff0b8'), (.25, '#e2b452'), (.55, '#8e5f1c'), (.8, '#d9a840'), (1, '#5b3a10')], x2=1, y2=1)
         + lin('asky', [(0, '#c9cf9a'), (.45, '#a9b98d'), (1, '#6f8e7c')])
         + lin('amtn', [(0, '#8fae9d'), (1, '#4c6e66')])
         + lin('afg', [(0, '#6b5a34'), (1, '#2a2312')])
         + lin('abody', [(0, '#c9d1d3'), (.5, '#8f9a9f'), (1, '#3e474c')], x2=1, y2=0)
         + lin('afloor', [(0, '#2a140d'), (1, '#0b0504')])
         + blur('ab8', 8) + blur('ab20', 20) + blur('ab40', 40) + blur('ab3', 3)
         + '<clipPath id="abd"><path d="M1170,560 C1140,640 1150,720 1190,780 C1230,830 1400,830 1440,770 C1480,700 1470,630 1450,560 Z"/></clipPath><clipPath id="acv"><rect x="1068" y="148" width="484" height="684"/></clipPath>')
    b = '<rect width="1920" height="1080" fill="url(#aw)"/>'
    # damask-like wall pattern + wainscot
    b += '<g fill="#f2c27a" opacity=".05">' + ''.join(f'<path transform="translate({x} {y})" d="M0,-26 C14,-12 14,12 0,26 C-14,12 -14,-12 0,-26Z"/>' for x in range(40, 1920, 90) for y in range(40, 760, 90)) + '</g>'
    b += '<rect width="1920" height="1080" fill="url(#aspot)"/>'
    b += '<rect y="760" width="1920" height="320" fill="url(#afloor)"/><rect y="756" width="1920" height="8" fill="#a8703a" opacity=".5"/>'
    # spotlight cone from above
    b += '<path d="M1180,0 L1440,0 L1720,900 L900,900 Z" fill="#ffe2ad" opacity=".07" filter="url(#ab40)"/>'
    # frame shadow + glow
    b += '<rect x="1000" y="100" width="640" height="820" rx="10" fill="#000" opacity=".55" filter="url(#ab20)" transform="translate(16 22)"/>'
    b += '<rect x="990" y="76" width="640" height="830" rx="14" fill="#ffcf80" opacity=".28" filter="url(#ab40)"/>'
    # ornate gold frame (outer x 1010-1610, y 90-890)
    b += '<rect x="1010" y="90" width="600" height="800" rx="6" fill="url(#agold)" stroke="#2a1806" stroke-width="5"/>'
    b += '<rect x="1032" y="112" width="556" height="756" fill="none" stroke="#fff3c4" stroke-width="3" opacity=".6"/>'
    b += '<rect x="1048" y="128" width="524" height="724" fill="#6b4512" stroke="#2a1806" stroke-width="3"/>'
    for i in range(26):   # bead ornament along the frame
        t = i / 25
        for (x, y) in ((1030 + 560 * t, 101), (1030 + 560 * t, 879)):
            b += f'<ellipse cx="{x:.0f}" cy="{y}" rx="9" ry="6" fill="#ffe7a0" stroke="#5b3a10" stroke-width="1.5"/>'
    for i in range(34):
        t = i / 33
        for x in (1021, 1599):
            b += f'<ellipse cx="{x}" cy="{110 + 760 * t:.0f}" rx="6" ry="9" fill="#ffe7a0" stroke="#5b3a10" stroke-width="1.5"/>'
    for (x, y) in ((1010, 90), (1610, 90), (1010, 890), (1610, 890)):   # corner rosettes
        b += f'<circle cx="{x}" cy="{y}" r="30" fill="url(#agold)" stroke="#2a1806" stroke-width="4"/><circle cx="{x}" cy="{y}" r="12" fill="#fff0b8" stroke="#5b3a10" stroke-width="2"/>'
    # ---- the painting: sfumato landscape
    p = '<rect x="1068" y="148" width="484" height="684" fill="url(#asky)"/>'
    p += '<path d="M1068,440 L1110,380 L1150,410 L1190,330 L1225,370 L1250,350 L1250,520 L1068,540 Z" fill="url(#amtn)" opacity=".85"/>'
    p += '<path d="M1380,520 L1400,360 L1440,400 L1470,320 L1510,380 L1552,350 L1552,560 Z" fill="url(#amtn)" opacity=".85"/>'
    p += '<path d="M1068,540 C1130,520 1200,520 1250,540 L1250,640 L1068,660 Z" fill="#7c9a7c"/>'
    p += '<path d="M1380,560 C1440,540 1500,545 1552,560 L1552,660 L1380,650 Z" fill="#7c9a7c"/>'
    p += '<path d="M1080,640 C1120,600 1170,610 1150,560 C1140,530 1190,520 1210,500" fill="none" stroke="#d6b77c" stroke-width="7" opacity=".8"/>'   # winding road
    p += '<path d="M1440,640 C1470,610 1500,600 1530,560" fill="none" stroke="#c9d6c0" stroke-width="9" opacity=".7"/>'   # river
    p += '<path d="M1450,612 q20,-18 40,0" fill="none" stroke="#6b5a34" stroke-width="5"/>'   # little bridge
    p += '<rect x="1068" y="148" width="484" height="684" fill="#d9d39a" opacity=".18" filter="url(#ab20)"/>'
    p += '<path d="M1068,700 C1200,660 1420,660 1552,700 L1552,832 L1068,832 Z" fill="url(#afg)"/>'
    # the model posed like the portrait: body behind/below, tail curled across the front like folded hands
    p += '<path d="M1170,560 C1140,640 1150,720 1190,780 C1230,830 1400,830 1440,770 C1480,700 1470,630 1450,560 Z" fill="url(#abody)" stroke="#1b2022" stroke-width="5"/>'
    p += '<g opacity=".16" clip-path="url(#abd)" stroke="#1b2022" stroke-width="2" fill="none">' + ''.join(f'<path d="M{1150 + i * 26},860 l90,-300"/><path d="M{1200 + i * 26},860 l-90,-300"/>' for i in range(14)) + '</g>'
    p += '<path d="M1450,790 C1380,760 1280,770 1215,790 C1190,798 1175,812 1182,822 C1240,808 1330,800 1430,812 Z" fill="#c3cbce" stroke="#1b2022" stroke-width="4"/>'
    p += '<path d="M1182,822 C1160,806 1140,790 1126,800 C1130,812 1128,826 1118,840 C1140,840 1165,834 1182,822 Z" fill="#dde3e4" stroke="#1b2022" stroke-width="4"/>'   # tiny tail fin
    p += '<path d="M1200,792 C1280,772 1370,770 1440,790" fill="none" stroke="#ffffff" stroke-width="5" opacity=".5"/>'
    p += '<ellipse cx="1310" cy="440" rx="200" ry="150" fill="#fff4cf" opacity=".35" filter="url(#ab20)"/>'
    dd, face = model_face('am', 'translate(1310 450) scale(.62) rotate(-3)', look=(-6, 0), mouth=.9)
    d += dd; p += face
    p += '<rect x="1068" y="148" width="484" height="684" fill="#5c4718" opacity=".12"/>'   # old varnish
    # glass reflections over the painting
    p += '<path d="M1068,330 L1230,148 L1300,148 L1068,410 Z" fill="#fff" opacity=".13"/><path d="M1350,832 L1552,600 L1552,640 L1385,832 Z" fill="#fff" opacity=".1"/>'
    b += f'<g clip-path="url(#acv)">{p}</g>'
    b += '<rect x="1068" y="148" width="484" height="684" fill="none" stroke="#2a1806" stroke-width="5"/>'
    # ---- crowd from behind (silhouettes with warm rim light) holding up glowing phones
    people = [(90, 1070, 1.25), (330, 1045, 1.05), (560, 1085, 1.3), (790, 1040, 1.0), (1010, 1085, 1.2), (1240, 1075, 1.0)]
    arms = {330: (430, 700, -12), 790: (720, 660, 8), 1240: (1130, 720, 12), 560: (640, 760, -6)}
    cols = ['#140906', '#1b0d08', '#120705']
    out = ''
    for k, (x, y, s) in enumerate(people):
        c = cols[k % 3]
        if x in arms:   # raised arm + phone (drawn behind the head)
            hx, hy, ang = arms[x]
            out += f'<path d="M{x + (40 if hx > x else -40) * s:.0f},{y - 40 * s:.0f} C{(x + hx) / 2:.0f},{y - 120 * s:.0f} {hx:.0f},{hy + 140:.0f} {hx:.0f},{hy + 60:.0f}" fill="none" stroke="{c}" stroke-width="{46 * s:.0f}" stroke-linecap="round"/>'
            out += hand(hx, hy + 60, angle=ang, size=46 * s, side='R', view='back', pose='hold', skin=c, line='#000', creases=False)
            ph = f'translate({hx:.0f} {hy:.0f}) rotate({ang})'
            out += f'<g transform="{ph}"><rect x="-44" y="-80" width="88" height="150" rx="14" fill="#0a0a0c" stroke="#2c2c30" stroke-width="3"/>'
            out += '<rect x="-36" y="-70" width="72" height="128" rx="8" fill="#e9c88c"/><rect x="-36" y="-70" width="72" height="128" rx="8" fill="#fff6dc" opacity=".35"/>'
            out += '<rect x="-24" y="-56" width="48" height="66" fill="#b98b4a"/><ellipse cx="0" cy="-22" rx="17" ry="13" fill="#c9d1d3" stroke="#222" stroke-width="2"/>'
            out += '<circle cx="-6" cy="-26" r="5" fill="#fff" stroke="#222" stroke-width="1"/><circle cx="6" cy="-26" r="5" fill="#fff" stroke="#222" stroke-width="1"/><circle cx="-5" cy="-24" r="2" fill="#000"/><circle cx="7" cy="-24" r="2" fill="#000"/>'
            out += '</g>'
            out += f'<rect x="{hx - 70}" y="{hy - 100}" width="140" height="190" rx="30" fill="#ffd89a" opacity=".22" filter="url(#ab20)" transform="rotate({ang} {hx} {hy})"/>'
    for k, (x, y, s) in enumerate(people):
        c = cols[k % 3]
        out += f'<path d="M{x - 150 * s:.0f},1090 C{x - 150 * s:.0f},{y - 40 * s:.0f} {x - 90 * s:.0f},{y - 80 * s:.0f} {x},{y - 82 * s:.0f} C{x + 90 * s:.0f},{y - 80 * s:.0f} {x + 150 * s:.0f},{y - 40 * s:.0f} {x + 150 * s:.0f},1090 Z" fill="{c}"/>'
        out += f'<ellipse cx="{x}" cy="{y - 150 * s:.0f}" rx="{70 * s:.0f}" ry="{82 * s:.0f}" fill="{c}"/>'
        out += f'<path d="M{x - 52 * s:.0f},{y - 200 * s:.0f} C{x - 30 * s:.0f},{y - 232 * s:.0f} {x + 30 * s:.0f},{y - 232 * s:.0f} {x + 52 * s:.0f},{y - 200 * s:.0f}" fill="none" stroke="#ffb46a" stroke-width="{5 * s:.1f}" opacity=".55" stroke-linecap="round"/>'
        out += f'<path d="M{x - 140 * s:.0f},{y - 30 * s:.0f} C{x - 110 * s:.0f},{y - 70 * s:.0f} {x - 70 * s:.0f},{y - 78 * s:.0f} {x - 30 * s:.0f},{y - 80 * s:.0f}" fill="none" stroke="#ffb46a" stroke-width="{4 * s:.1f}" opacity=".35" stroke-linecap="round"/>'
    b += out
    # camera flashes + sparkles
    for (x, y, s) in ((1150, 300, 30), (1500, 230, 22), (1560, 700, 26), (880, 560, 18), (1690, 420, 20)):
        b += f'<circle cx="{x}" cy="{y}" r="{s * 2.2}" fill="#fff6d6" opacity=".35" filter="url(#ab8)"/>' + spark(x, y, s)
    b += f'<rect x="1640" y="880" width="280" height="200" fill="#000" opacity=".25" filter="url(#ab40)"/>'
    return d, b


# ============================================================ B: PART SCIENCE, PART ART  (intuitive: split face)
def build_B():
    random.seed(5)
    CX, CY, S = 1290, 640, .86
    d = (lin('bsea', [(0, '#9fe0d0'), (.45, '#3fa5a2'), (1, '#16535a')])
         + lin('bsand', [(0, '#e5cf95'), (1, '#a9864c')])
         + lin('bmus', [(0, '#3a2416'), (.6, '#24150d'), (1, '#0f0805')])
         + rad('bsun', 520, -60, 900, [(0, '#fff6cf', .85), (.4, '#d8f3dc', .25), (1, '#d8f3dc', 0)])
         + rad('bspot', 1500, 200, 700, [(0, '#ffe0a8', .7), (.5, '#e0a060', .18), (1, '#e0a060', 0)])
         + rad('bhalo', CX, CY, 560, [(0, '#fff3cf', .55), (.6, '#fff3cf', .15), (1, '#fff3cf', 0)])
         + rg('bfos', [(0, '#e8eadf', 1), (.3, '#a2aca6', 1), (.75, '#5c6865', 1), (1, '#2f3836', 1)], cx=.32, cy=.25, r=.85)
         + rg('bmod', [(0, '#ffffff', 1), (.22, '#eef2f3', 1), (.6, '#a3aeb3', 1), (1, '#4a545a', 1)], cx=.7, cy=.25, r=.85)
         + rg('bwht', [(0, '#ffffff', 1), (.75, '#f3f2ee', 1), (1, '#b7baba', 1)], cx=.42, cy=.35, r=.65)
         + rg('bmth', [(0, '#3d1414', 1), (1, '#0a0506', 1)], cx=.5, cy=.3, r=.7)
         + blur('bb6', 6) + blur('bb14', 14) + blur('bb30', 30)
         + '<clipPath id="bL"><rect x="0" y="0" width="1290" height="1080"/></clipPath><clipPath id="bR"><rect x="1290" y="0" width="630" height="1080"/></clipPath>')
    FACE = 'M-440,40 C-450,-200 -250,-320 0,-320 C250,-320 450,-200 440,40 C430,220 250,300 0,300 C-250,300 -430,220 -440,40 Z'
    tr = f'translate({CX} {CY}) scale({S})'
    # ---- left background: warm shallow Ordovician sea
    L = '<rect width="1920" height="1080" fill="url(#bsea)"/><rect width="1920" height="1080" fill="url(#bsun)"/>'
    L += '<g fill="none" stroke="#f2fff0" stroke-width="5" opacity=".22" stroke-linecap="round">'   # caustic net
    for j in range(9):
        for i in range(12):
            x, y = i * 120 + (j % 2) * 60, 60 + j * 85
            L += f'<path d="M{x},{y} q30,-26 60,0 q30,26 60,0"/>'
    L += '</g>'
    L += '<path d="M0,880 C300,850 700,860 1300,890 L1300,1080 L0,1080 Z" fill="url(#bsand)"/>'
    L += '<g fill="none" stroke="#8a6a38" stroke-width="5" opacity=".45">' + ''.join(f'<path d="M{x},{935 + (x % 3) * 30} q40,-14 80,0 q40,14 80,0"/>' for x in range(20, 1300, 190)) + '</g>'
    L += blobs(18, 0, 900, 1290, 1070, '#fff2c9', .15, .35, 6, 18)
    # a trilobite on the sand (Ordovician neighbour)
    L += '<g transform="translate(330 960) rotate(-8)"><ellipse cx="0" cy="12" rx="92" ry="20" fill="#5a4426" opacity=".4" filter="url(#bb6)"/>'
    L += '<path d="M-80,0 C-82,-42 -40,-62 0,-62 C40,-62 82,-42 80,0 C70,26 40,36 0,36 C-40,36 -70,26 -80,0Z" fill="#8a7458" stroke="#2a1d10" stroke-width="4"/>'
    L += '<path d="M-22,-60 C-24,-20 -20,20 -14,34 M22,-60 C24,-20 20,20 14,34" fill="none" stroke="#2a1d10" stroke-width="3"/>'
    L += ''.join(f'<path d="M-76,{y} Q0,{y + 8} 76,{y}" fill="none" stroke="#2a1d10" stroke-width="2.5" opacity=".7"/>' for y in range(-26, 30, 9))
    L += '<path d="M-60,-40 C-30,-60 30,-60 60,-40" fill="none" stroke="#e6d2a8" stroke-width="4" opacity=".7"/><circle cx="-30" cy="-44" r="6" fill="#1a120a"/><circle cx="30" cy="-44" r="6" fill="#1a120a"/></g>'
    L += '<g fill="#e9fff5" opacity=".6">' + ''.join(f'<circle cx="{x}" cy="{y}" r="{r}"/>' for x, y, r in ((780, 760, 7), (800, 700, 5), (770, 640, 9), (820, 580, 4), (150, 620, 6), (130, 560, 4))) + '</g>'
    # ---- right background: museum gallery with spotlight
    R = '<rect width="1920" height="1080" fill="url(#bmus)"/><rect width="1920" height="1080" fill="url(#bspot)"/>'
    R += '<path d="M1360,0 L1640,0 L1820,1000 L1290,1000 Z" fill="#ffe2ad" opacity=".08" filter="url(#bb30)"/>'
    R += '<rect x="1290" y="930" width="630" height="150" fill="#0a0503"/><rect x="1290" y="926" width="630" height="6" fill="#a8703a" opacity=".5"/>'
    b = f'<g clip-path="url(#bL)">{L}</g><g clip-path="url(#bR)">{R}</g>'
    b += f'<rect x="{CX - 470}" y="{CY - 330}" width="940" height="660" rx="330" fill="#fff3cf" opacity=".25" filter="url(#bb30)"/>'
    b += f'<ellipse cx="{CX}" cy="{CY + 300}" rx="380" ry="40" fill="#000" opacity=".35" filter="url(#bb14)"/>'
    # ---- the face, left half: the fossil fish (accurate)
    rnd = random.Random(9)
    fl = f'<path d="{FACE}" fill="url(#bfos)"/>'
    # plates: faint polygon boundaries
    fl += '<g fill="none" stroke="#283231" stroke-width="3" opacity=".45">'
    fl += '<path d="M-60,-318 C-80,-220 -100,-200 -200,-180 C-280,-170 -360,-120 -430,-60"/><path d="M-200,-180 C-220,-80 -260,-20 -440,30"/>'
    fl += '<path d="M-440,60 C-330,80 -220,90 -120,110 C-60,120 -20,120 0,118"/></g>'
    for gx in range(-440, 0, 30):   # oak-leaf bumps on a jittered grid
      for gy in range(-320, 300, 26):
        x = gx + rnd.uniform(-9, 9) + (gy // 26 % 2) * 15; y = gy + rnd.uniform(-7, 7)
        if x > -6: continue
        if (x / 442) ** 2 + ((y - 10) / 312) ** 2 > .95: continue
        if (x + 125) ** 2 + (y + 120) ** 2 < 88 ** 2 or (110 < y < 205 and x > -340): continue
        a = math.degrees(math.atan2(y + 120, x + 125)) + rnd.uniform(-15, 15)
        sh = .35 + .55 * (1 - (y + 320) / 620)
        s = rnd.uniform(1.05, 1.35)
        fl += (f'<g transform="translate({x:.0f} {y:.0f}) rotate({a:.0f}) scale({s:.2f})">'
               f'<path d="M-8,0 C-6,-4 -2,-4 0,-2 C2,-5 6,-4 8,0 C6,4 2,5 0,2 C-2,4 -6,4 -8,0Z" fill="#1f2826" opacity=".55" transform="translate(1.6 2.2)"/>'
               f'<path d="M-8,0 C-6,-4 -2,-4 0,-2 C2,-5 6,-4 8,0 C6,4 2,5 0,2 C-2,4 -6,4 -8,0Z" fill="#e2bf6e" opacity="{sh:.2f}"/>'
               f'<path d="M-5,-1 C-3,-3 3,-3 5,-1" stroke="#fff4cf" stroke-width="1" fill="none" opacity=".6"/></g>')
    fl += '<g fill="none" stroke="#141a19" stroke-width="5" stroke-dasharray="3 14" stroke-linecap="round" opacity=".75"><path d="M-40,-260 C-150,-250 -280,-190 -360,-100"/><path d="M-30,-10 C-140,0 -280,10 -410,0"/></g>'
    fl += '<ellipse cx="-60" cy="-232" rx="11" ry="7" fill="#141a19"/><ellipse cx="-30" cy="-245" rx="11" ry="7" fill="#141a19"/>'   # two small pits
    # small eye in a bony ring, close to the midline at the very front
    fl += '<circle cx="-125" cy="-120" r="80" fill="#cbbf92" stroke="#1b2022" stroke-width="7"/><circle cx="-125" cy="-120" r="80" fill="none" stroke="#f6edd0" stroke-width="5" stroke-dasharray="7 9" opacity=".8"/>'
    fl += '<circle cx="-125" cy="-120" r="52" fill="#0b1012" stroke="#1b2022" stroke-width="4"/><circle cx="-145" cy="-140" r="15" fill="#fff"/><circle cx="-108" cy="-102" r="6" fill="#bfe8ff" opacity=".8"/>'
    # narrow slit mouth + lower lip of thin scale strips
    fl += '<path d="M-330,128 C-230,140 -110,146 0,146 L0,164 C-110,166 -230,160 -330,128 Z" fill="#0c0e0e" stroke="#1b2022" stroke-width="5"/>'
    fl += '<path d="M-322,140 C-230,160 -110,168 0,168 L0,196 C-120,198 -240,184 -322,140 Z" fill="#b9b49a" stroke="#1b2022" stroke-width="4"/>'
    fl += ''.join(f'<path d="M{-300 + i * 15},{163 + i * .55:.0f} q7,9 14,0" fill="none" stroke="#5d5a48" stroke-width="2.5"/>' for i in range(20))
    fl += ''.join(f'<path d="M{-292 + i * 15},{175 + i * .45:.0f} q7,9 14,0" fill="none" stroke="#5d5a48" stroke-width="2.5" opacity=".7"/>' for i in range(19))
    fl += '<path d="M-400,-120 C-330,-240 -200,-300 -40,-312" fill="none" stroke="#fffbe6" stroke-width="12" stroke-linecap="round" opacity=".55"/>'
    # caustic light on the armor
    fl += '<g fill="none" stroke="#f4fff4" stroke-width="5" opacity=".18">' + ''.join(f'<path d="M{-420 + i * 70},{-200 + (i % 3) * 120} q25,-20 50,0 q25,20 50,0"/>' for i in range(7)) + '</g>'
    # ---- right half: the smooth silvery museum model
    fr = f'<path d="{FACE}" fill="url(#bmod)"/>'
    fr += '<path d="M40,-300 C200,-290 340,-210 400,-100" fill="none" stroke="#fff" stroke-width="22" stroke-linecap="round" opacity=".7"/>'
    fr += '<ellipse cx="300" cy="120" rx="80" ry="30" fill="#ffe4b8" opacity=".35" transform="rotate(-30 300 120)" filter="url(#bb6)"/>'
    fr += '<circle cx="150" cy="-108" r="148" fill="#2a3034" opacity=".35" transform="translate(4 12)"/>'
    fr += '<circle cx="150" cy="-112" r="142" fill="url(#bwht)" stroke="#1b2022" stroke-width="8"/>'
    fr += '<circle cx="104" cy="-72" r="66" fill="#0a0a0b"/><circle cx="82" cy="-96" r="17" fill="#fff"/>'
    fr += '<ellipse cx="108" cy="-196" rx="44" ry="16" fill="#fff" opacity=".95" transform="rotate(-20 108 -196)"/>'
    fr += '<path d="M0,112 C60,108 140,112 190,124 C160,200 90,262 0,272 Z" fill="url(#bmth)" stroke="#1b2022" stroke-width="7" stroke-linejoin="round"/>'
    fr += '<path d="M20,240 C60,230 100,214 130,190" fill="none" stroke="#7a2b2b" stroke-width="8" opacity=".6" stroke-linecap="round"/>'
    tail = 'M-330,150 C-470,200 -600,150 -700,60 C-720,40 -740,30 -760,26 L-756,8 C-735,14 -712,22 -690,40 C-590,120 -470,160 -340,100 Z'
    b += f'<g transform="{tr}"><path d="{tail}" fill="#7d7a5c" stroke="#1b2022" stroke-width="6" stroke-linejoin="round"/>'
    b += '<path d="M-340,108 C-470,165 -590,128 -690,44" fill="none" stroke="#e8e0b0" stroke-width="5" opacity=".6"/>'
    b += '<path d="M-750,16 C-800,-30 -850,-20 -870,0 C-850,10 -850,30 -858,60 C-810,58 -775,40 -750,16 Z" fill="#a39f7c" stroke="#1b2022" stroke-width="5"/>'
    b += f'<g clip-path="url(#bfl)">{fl}</g><g clip-path="url(#bfr)">{fr}</g>'
    b += f'<path d="{FACE}" fill="none" stroke="#1b2022" stroke-width="8"/>'
    # glowing seam
    b += '<path d="M0,-330 L0,310" stroke="#ffd98a" stroke-width="26" opacity=".55" filter="url(#bb14)"/><path d="M0,-330 L0,310" stroke="#fff6d8" stroke-width="7"/>'
    b += '</g>'
    d += f'<clipPath id="bfl"><rect x="-460" y="-340" width="460" height="680"/></clipPath><clipPath id="bfr"><rect x="0" y="-340" width="460" height="680"/></clipPath>'
    for (x, y, s) in ((CX, CY - 300, 34), (CX + 14, CY + 290, 22), (1700, 260, 22), (1560, 140, 14), (960, 420, 16)):
        b += f'<circle cx="{x}" cy="{y}" r="{s * 2}" fill="#fff6d6" opacity=".35" filter="url(#bb6)"/>' + spark(x, y, s)
    return d, b


# ============================================================ C: A SINGLE BAD DAY  (homage: Hokusai, The Great Wave)
def build_C():
    random.seed(21)
    d = (lin('csky', [(0, '#e9d3a8'), (.6, '#f4e2bd'), (1, '#f1d7a3')])
         + rad('cglow', 420, 120, 700, [(0, '#fff5d8', .95), (.5, '#ffe6b0', .35), (1, '#ffe6b0', 0)])
         + lin('cwave', [(0, '#5fc2bb'), (.35, '#2d8f93'), (.7, '#1d5f6b'), (1, '#123d48')], x2=.4, y2=1)
         + lin('cface', [(0, '#2a7f86'), (1, '#0f3540')])
         + lin('csea', [(0, '#6cc0b4'), (1, '#1c5864')])
         + lin('cfore', [(0, '#3a9c9a'), (.5, '#1d6670'), (1, '#0c2e38')])
         + lin('cmtn', [(0, '#efe6cf'), (.25, '#d8c6a4'), (.3, '#9a6a4c'), (1, '#6b4532')])
         + blur('cb4', 4) + blur('cb12', 12) + blur('cb30', 30))
    b = '<rect width="1920" height="1080" fill="url(#csky)"/><rect width="1920" height="1080" fill="url(#cglow)"/>'
    # storm clouds top right
    b += '<g filter="url(#cb30)">' + blobs(16, 1100, -60, 1950, 200, '#6d6670', .35, .6, 120, 260) + '</g>'
    b += '<g filter="url(#cb12)">' + blobs(10, 1300, -20, 1950, 130, '#4f4a55', .3, .5, 80, 160) + '</g>'
    b += '<g fill="none" stroke="#8a7f78" stroke-width="3" opacity=".35">' + ''.join(f'<path d="M{x},0 l-60,260"/>' for x in range(1300, 1960, 46)) + '</g>'   # rain
    # horizon sea + the barren cone (in Fuji's place)
    b += '<path d="M0,700 L1920,700 L1920,1080 L0,1080 Z" fill="url(#csea)"/>'
    b += '<path d="M690,702 L800,600 C812,590 828,590 840,600 L960,702 Z" fill="url(#cmtn)" stroke="#4a2e20" stroke-width="3"/>'
    b += '<path d="M770,630 L800,600 C812,590 828,590 840,600 L872,630 L850,622 L835,636 L818,620 L800,634 L786,624 Z" fill="#f7f1e0"/>'
    b += '<rect x="0" y="698" width="1920" height="6" fill="#e9fff6" opacity=".5"/>'
    # small far waves
    b += '<g fill="none" stroke="#e6fff6" stroke-width="4" opacity=".55">' + ''.join(f'<path d="M{x},{720 + (x * 7) % 40} q20,-14 40,0"/>' for x in range(0, 1100, 70)) + '</g>'
    # mid wave on the left (little brother wave) with foam
    b += '<path d="M-20,880 C120,820 260,760 380,748 C460,740 520,770 560,810 C600,850 660,872 760,880 L760,1080 L-20,1080 Z" fill="url(#cwave)"/>'
    for i in range(10):
        x = 300 + i * 22; y = 760 - math.sin(i / 9 * math.pi) * 18
        b += f'<path d="M{x:.0f},{y:.0f} q12,-16 24,-4 q-8,4 -6,12" fill="#fbf6e6" stroke="#0c2e38" stroke-width="2"/>'
    # ---- the great wave (mirrored): rises on the right, crest curls left over the centre
    W = ('M1920,1080 L1920,380 C1890,250 1790,150 1650,115 C1500,80 1340,110 1220,175 C1110,235 1030,300 990,380 '
         'C1040,350 1100,330 1160,340 C1230,352 1268,400 1262,460 C1256,540 1205,620 1170,700 C1130,800 1090,930 1080,1080 Z')
    b += f'<path d="{W}" fill="#0a2630" opacity=".35" filter="url(#cb30)" transform="translate(-30 30)"/>'
    b += f'<path d="{W}" fill="url(#cwave)" stroke="#0a2630" stroke-width="6"/>'
    # concave inner face under the curl
    b += '<path d="M990,380 C1040,350 1100,330 1160,340 C1230,352 1268,400 1262,460 C1256,540 1205,620 1170,700 C1130,800 1090,930 1080,1080 L1300,1080 C1300,900 1330,760 1360,640 C1400,480 1360,330 1230,300 C1130,280 1050,320 990,380 Z" fill="url(#cface)" opacity=".85"/>'
    # muddy fresh-water streaks + Hokusai water lines
    b += '<g fill="none" stroke-linecap="round">'
    for k in range(14):
        o = k * 46
        b += f'<path d="M{1960 - o * .2:.0f},{420 + o:.0f} C{1840 - o * .5:.0f},{240 + o * .9:.0f} {1560 - o * .4:.0f},{180 + o * .8:.0f} {1360 - o * .1:.0f},{260 + o * .9:.0f}" stroke="#bfe9e0" stroke-width="5" opacity=".35"/>'
    b += '</g><g filter="url(#cb30)">'
    for (x, y, rx, ry, a) in ((1560, 620, 260, 70, 35), (1700, 800, 240, 60, 55), (1450, 860, 200, 50, 70), (1780, 520, 160, 50, 25)):
        b += f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{ry}" transform="rotate({a} {x} {y})" fill="#a8783a" opacity=".38"/>'
    b += '</g><g>'
    b += '</g>'
    # foam cap along the crest + claws hanging from the lip
    crest = [(1900, 330), (1820, 200), (1700, 135), (1560, 110), (1420, 125), (1300, 165), (1200, 210), (1110, 270), (1040, 330), (995, 380)]
    pts = ' '.join(f'{x},{y}' for x, y in crest)
    cr = f'M{crest[0][0]},{crest[0][1]}'
    for i in range(len(crest) - 1):   # Catmull-Rom -> cubic, a smooth crest line
        p0 = crest[max(0, i - 1)]; p1 = crest[i]; p2 = crest[i + 1]; p3 = crest[min(len(crest) - 1, i + 2)]
        cr += f' C{p1[0] + (p2[0] - p0[0]) / 6:.0f},{p1[1] + (p2[1] - p0[1]) / 6:.0f} {p2[0] - (p3[0] - p1[0]) / 6:.0f},{p2[1] - (p3[1] - p1[1]) / 6:.0f} {p2[0]},{p2[1]}'
    b += f'<path d="{cr}" fill="none" stroke="#0a2630" stroke-width="50" stroke-linecap="round"/>'
    b += f'<path d="{cr}" fill="none" stroke="#fbf6e6" stroke-width="42" stroke-linecap="round"/>'
    b += f'<path d="{cr}" fill="none" stroke="#ffffff" stroke-width="10" stroke-linecap="round" transform="translate(4 -10)" opacity=".8"/>'
    for i in range(len(crest) - 1):   # claw fingers: hooked droplets hanging under the foam band, curling toward the lip
        (x0, y0), (x1, y1) = crest[i], crest[i + 1]
        ang = math.degrees(math.atan2(y1 - y0, x1 - x0))
        for t in (.1, .45, .8):
            x, y = x0 + (x1 - x0) * t, y0 + (y1 - y0) * t
            s = 30 + 26 * (1 - min(1, max(0, (x - 1000) / 900)))
            b += (f'<path transform="translate({x:.0f} {y:.0f}) rotate({ang:.0f}) scale(1 -1) translate(0 14)" d="M{-s * .5:.0f},0 C{-s * .5:.0f},{s * .8:.0f} {s * .5:.0f},{s * 1.2:.0f} {s * .9:.0f},{s * .7:.0f} '
                  f'C{s * .5:.0f},{s * .75:.0f} {s * .15:.0f},{s * .5:.0f} {s * .2:.0f},{s * .2:.0f} C{s * .4:.0f},{s * .3:.0f} {s * .6:.0f},{s * .3:.0f} {s * .7:.0f},0 Z" fill="#fbf6e6" stroke="#0a2630" stroke-width="3"/>')
    for (x, y, s) in ((990, 400, 40), (1040, 410, 30), (960, 440, 26), (1010, 450, 22)):   # big claws curling at the lip
        b += (f'<path transform="translate({x} {y}) rotate(20)" d="M0,-{s} C{s * 1.3:.0f},-{s} {s * 1.2:.0f},{s * .9:.0f} 0,{s} C{s * .6:.0f},{s * .4:.0f} {s * .5:.0f},-{s * .4:.0f} -{s * .3:.0f},-{s * .2:.0f} Z" fill="#fbf6e6" stroke="#0a2630" stroke-width="3"/>')
    b += '<g fill="#fbf6e6">' + ''.join(f'<circle cx="{random.randint(860, 1500)}" cy="{random.randint(60, 420)}" r="{random.choice([4, 6, 8, 10])}" opacity=".9"/>' for _ in range(70)) + '</g>'
    # small fish tumbling inside the wave (in place of the boats)
    defs = ''
    for k, (x, y, sc, rot) in enumerate(((1440, 470, .16, -30), (1600, 560, .14, 15), (1360, 640, .13, -60), (1700, 420, .12, 40), (1520, 720, .12, -10))):
        dd, f = saca(f'cs{k}', f'translate({x} {y}) rotate({rot}) scale({sc})', seed=k + 3, detail=.4, op=.9, rim='#d8fff4')
        defs += dd; b += f
    # foreground swell
    # the big fish in the trough (accurate), startled, with its shadow + glow
    b += '<ellipse cx="640" cy="760" rx="520" ry="200" fill="#fff6d8" opacity=".35" filter="url(#cb30)"/>'
    dd, f = saca('cbig', 'translate(170 800) rotate(-6) scale(.86)', seed=2, detail=1.0)
    defs += dd; b += f
    WL = 'M-20,872 C120,850 260,846 420,858 C620,872 820,866 960,880 C1060,890 1130,930 1200,990 L1200,1080 L-20,1080 Z'
    b += f'<path d="{WL}" fill="url(#cfore)" opacity=".82"/>'
    b += '<path d="M-20,872 C120,850 260,846 420,858 C620,872 820,866 960,880 C1060,890 1130,930 1200,990" fill="none" stroke="#e6fff6" stroke-width="6" opacity=".8"/>'
    b += '<path d="M-20,960 C200,930 420,940 640,960 C820,975 1000,975 1200,1040 L1200,1080 L-20,1080 Z" fill="#0c2e38" opacity=".55"/>'
    for (x, y, s) in ((150, 856, 34), (330, 850, 30), (520, 864, 30), (700, 868, 26), (880, 874, 26)):
        b += f'<path transform="translate({x} {y})" d="M-{s * 1.4:.0f},4 C-{s},-{s * .9:.0f} {s * .4:.0f},-{s * 1.1:.0f} {s},-{s * .1:.0f} C{s * .5:.0f},-{s * .45:.0f} {s * .1:.0f},-{s * .2:.0f} {s * .25:.0f},4 Z" fill="#fbf6e6" stroke="#0a2630" stroke-width="3"/>'
    b += '<g fill="#fbf6e6">' + ''.join(f'<circle cx="{x}" cy="{y}" r="{r}"/>' for x, y, r in ((120, 820, 7), (180, 806, 5), (250, 818, 6), (90, 798, 4), (560, 830, 5), (610, 820, 4))) + '</g>'
    b += '<g fill="none" stroke="#fbf6e6" stroke-width="5" stroke-linecap="round" opacity=".9"><path d="M140,640 q-14,-30 4,-56"/><path d="M190,620 q0,-34 22,-50"/><path d="M90,672 q-28,-20 -30,-50"/></g>'   # startle lines
    b += '<g fill="#e9fff5" opacity=".75">' + ''.join(f'<circle cx="{x}" cy="{y}" r="{r}"/>' for x, y, r in ((120, 610, 8), (100, 560, 6), (128, 515, 4), (60, 600, 5))) + '</g>'
    for i in range(7):   # foam on the foreground swell
        x = 120 + i * 140
        b += f'<path d="M{x},{985 + (i % 2) * 30} q22,-18 44,-4" fill="none" stroke="#bff0e4" stroke-width="4" opacity=".5"/>'
    for (x, y, s) in ((620, 520, 22), (380, 640, 16), (900, 600, 18), (1180, 120, 16)):
        b += f'<circle cx="{x}" cy="{y}" r="{s * 2}" fill="#fff6d6" opacity=".4" filter="url(#cb4)"/>' + spark(x, y, s)
    return d + defs, b


da, ba = build_A()
open(os.path.join(HERE, 'A.html'), 'w').write(page('#3b1d17', svg(da, ba), [('WHY THIS', 150, 'w'), ('FACE?', 250, 'y')], outline='#140805'))
db, bb = build_B()
open(os.path.join(HERE, 'B.html'), 'w').write(page('#3fa5a2', svg(db, bb), [('PART SCIENCE,', 112, 'w'), ('PART <span class="g">ART</span>', 200, 'w')], outline='#072a2c'))
dc, bc = build_C()
open(os.path.join(HERE, 'C.html'), 'w').write(page('#f1d7a3', svg(dc, bc), [('A SINGLE', 140, 'w'), ('<span class="g">BAD</span> DAY', 220, 'w')], outline='#0a2630'))
print('ok')
