# Thumbnails A-C for megalodon-extinction (guideline 16-6 / 16-8, brief tools/briefs/thumb_art.md). Run: python3 videos/megalodon-extinction/thumb/make.py
# A  KNOWN BY ITS TEETH     homage (photo): the famous 1909 American Museum of Natural History photo of a reconstructed Megalodon jaw so big that
#                           a person sits inside it; here the explorer frog stands inside the giant museum jaw, a dashed outline of the missing body
#                           on the wall. Script: "you will never find a complete Megalodon skeleton ... Nearly everything we know comes from its teeth".
# B  TOO BIG TO SURVIVE?    intuitive: a huge open-jawed Megalodon in sunlit water whose tail is crumbling into stone shards and fossil teeth that
#                           sink to the sea floor; the diving frog watches. Script: "its sheer size may have become its greatest vulnerability",
#                           "The giants of the past have returned to dust and stone".
# C  THE OCEAN TURNED COLD  homage (film): Titanic's bow pose ("I'm flying") heading for the iceberg at night: the frog in a scarf stands arms wide
#                           on the Megalodon's snout as it ploughs toward a glowing iceberg. Script: "the climate shifted toward a cooler world.
#                           Polar ice began to expand ... For a giant that favored warm seas, the comfort zone was shrinking."
import os, sys, math, random
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from mgkit import *
from thumb_lib import page, svg, lin, rad, spark, stars


def veil(d, op=.6):
    return f'<path d="{d}" fill="#000" opacity="{op}" filter="url(#b50)"/>'


def cubpath(c):
    (a, b), (c1, d1), (e, f), (g, h) = c
    return f'M{a} {b} C{c1} {d1} {e} {f} {g} {h}'


def motes(rnd, n, x0, x1, y0, y1, col='#fff0c8', op=.6):
    return ''.join(f'<circle cx="{rnd.randint(x0, x1)}" cy="{rnd.randint(y0, y1)}" r="{rnd.choice([1.5, 2.2, 3])}" fill="{col}" opacity="{rnd.uniform(.2, op):.2f}"/>' for _ in range(n))


# =============================== A: the museum jaw (AMNH 1909 photo) ===============================
def make_A():
    rnd = random.Random(21)
    JX, JY = 1370, 520
    d = FILTERS
    d += lin('wallA', [(0, '#3a281c'), (.6, '#1e140e'), (1, '#0e0906')])
    d += lin('floorA', [(0, '#2a1c13'), (1, '#070504')])
    d += rad('spotA', JX, JY, 620, [(0, '#ffe7b0', .95), (.35, '#e8a75a', .45), (1, '#a05a20', 0)])
    d += rad('vigA', 960, 540, 1150, [(0, '#000', 0), (.6, '#000', 0), (1, '#000', .75)])
    d += f'<linearGradient id="carA" x1="0" y1="{JY - 320}" x2="0" y2="{JY + 380}" gradientUnits="userSpaceOnUse"><stop offset="0" stop-color="#f3e2bf"/><stop offset=".5" stop-color="#d8bb88"/><stop offset="1" stop-color="#8a6a44"/></linearGradient>'
    d += lin('woodA', [(0, '#5a3a22'), (1, '#24160c')])
    d += lin('coneA', [(0, '#fff2cf'), (1, '#fff2cf')])
    b = '<rect width="1920" height="1080" fill="url(#wallA)"/>'
    # wall panels / pilasters
    for px in (180, 640, 2100):
        b += f'<rect x="{px}" y="0" width="60" height="960" fill="#2c1e15" opacity=".7"/><rect x="{px + 6}" y="0" width="8" height="960" fill="#5a4030" opacity=".5"/>'
    b += '<rect x="0" y="930" width="1920" height="34" fill="#3a281c"/><rect x="0" y="930" width="1920" height="5" fill="#7a5a3e" opacity=".7"/>'
    b += '<rect x="0" y="964" width="1920" height="120" fill="url(#floorA)"/>'
    # spotlight cone from the ceiling
    b += f'<path d="M{JX - 90} -20 L{JX + 90} -20 L{JX + 620} 1000 L{JX - 620} 1000Z" fill="#ffe8b8" opacity=".09" filter="url(#b24)"/>'
    b += f'<path d="M{JX - 40} -20 L{JX + 40} -20 L{JX + 380} 1000 L{JX - 380} 1000Z" fill="#fff2d0" opacity=".07" filter="url(#b12)"/>'
    b += f'<ellipse cx="{JX}" cy="{JY + 30}" rx="640" ry="560" fill="url(#spotA)"/>'
    b += f'<ellipse cx="{JX}" cy="985" rx="560" ry="40" fill="#ffdc9a" opacity=".22" filter="url(#b24)"/>'
    # dashed outline of the missing body on the wall (museum wall graphic)
    b += motes(rnd, 70, JX - 500, JX + 500, 20, 940)
    # ---------- jaw (front view) ----------
    oU = ((JX - 470, JY), (JX - 450, JY - 420), (JX + 450, JY - 420), (JX + 470, JY))
    oL = ((JX + 470, JY), (JX + 430, JY + 500), (JX - 430, JY + 500), (JX - 470, JY))
    iU = ((JX - 360, JY - 10), (JX - 330, JY - 280), (JX + 330, JY - 280), (JX + 360, JY - 10))
    iL = ((JX + 360, JY + 4), (JX + 320, JY + 360), (JX - 320, JY + 360), (JX - 360, JY + 4))
    ring = (f'M{oU[0][0]} {oU[0][1]} C{oU[1][0]} {oU[1][1]} {oU[2][0]} {oU[2][1]} {oU[3][0]} {oU[3][1]} '
            f'C{oL[1][0]} {oL[1][1]} {oL[2][0]} {oL[2][1]} {oL[3][0]} {oL[3][1]} Z '
            f'M{iU[0][0]} {iU[0][1]} C{iU[1][0]} {iU[1][1]} {iU[2][0]} {iU[2][1]} {iU[3][0]} {iU[3][1]} '
            f'L{iL[0][0]} {iL[0][1]} C{iL[1][0]} {iL[1][1]} {iL[2][0]} {iL[2][1]} {iL[3][0]} {iL[3][1]} Z')
    b += f'<path d="{ring}" fill="#000" opacity=".55" fill-rule="evenodd" transform="translate(18 22)" filter="url(#b12)"/>'
    b += f'<path d="{ring}" fill="url(#carA)" fill-rule="evenodd" stroke="#1a0f08" stroke-width="6"/>'
    # cartilage texture + highlight
    b += f'<path d="{cubpath(((JX - 430, JY - 40), (JX - 400, JY - 370), (JX + 400, JY - 370), (JX + 430, JY - 40)))}" fill="none" stroke="#fff8e6" stroke-width="7" opacity=".6"/>'
    b += f'<path d="{cubpath(((JX - 440, JY + 60), (JX - 380, JY + 440), (JX + 380, JY + 440), (JX + 440, JY + 60)))}" fill="none" stroke="#5a4028" stroke-width="5" opacity=".5"/>'
    for _ in range(60):
        a = rnd.uniform(0, 2 * math.pi); r = rnd.uniform(.84, .97)
        px, py = JX + 420 * r * math.cos(a), JY + (370 if math.sin(a) < 0 else 420) * r * math.sin(a)
        b += f'<circle cx="{px:.0f}" cy="{py:.0f}" r="{rnd.choice([2, 3, 4])}" fill="#6a4a2a" opacity="{rnd.uniform(.2, .45):.2f}"/>'
    # back tooth rows (on the jaw band, smaller, darker)
    tA = dict(col=['#4a525e', '#54483e', '#3e4652'], shade='#1c2128', line='#0c0a08', lw=2.4, bour='#2a1c12')
    b += teeth_on(((JX - 400, JY - 20), (JX - 372, JY - 330), (JX + 372, JY - 330), (JX + 400, JY - 20)), 15, 34, 1, **tA)
    b += teeth_on(((JX - 400, JY + 20), (JX - 360, JY + 410), (JX + 360, JY + 410), (JX + 400, JY + 20)), 14, 34, -1, **tA)
    # gum strip
    b += f'<path d="{cubpath(iU)}" fill="none" stroke="#b9876a" stroke-width="12" opacity=".8"/>'
    b += f'<path d="{cubpath(iL)}" fill="none" stroke="#b9876a" stroke-width="12" opacity=".8"/>'
    # frog inside the jaw (explorer helmet), behind the lower front teeth
    hat = ('<path d="M-30 -84 Q-30 -128 6 -130 Q42 -128 42 -84Z" fill="#e8d6a6" stroke-width="3.4"/><path d="M-30 -92 L42 -92 L42 -84 L-30 -84Z" fill="#6a4a2a" stroke-width="2.4"/>'
           '<ellipse cx="6" cy="-83" rx="50" ry="10" fill="#d9c38c" stroke-width="3.4"/><path d="M-18 -116 q14 -10 30 -8" fill="none" stroke="#fff8e0" stroke-width="4" opacity=".8"/>')
    bag = '<path d="M-28 -46 L34 -6" stroke="#6a4a2a" stroke-width="5" fill="none"/><rect x="24" y="-14" width="26" height="20" rx="4" fill="#8a6a3a" stroke-width="3"/>'
    b += f'<ellipse cx="{JX}" cy="{JY + 250}" rx="140" ry="40" fill="#000" opacity=".3" filter="url(#b12)"/>'
    b += frog(JX, JY + 258, 2.55, look=(1, -5), armL='M-34 -24 q-30 -10 -40 -44', armR='M38 -24 q30 -10 40 -44', head=hat, mid=bag)
    # front tooth rows (big, glossy, serrated) with a warm rim from the spotlight
    tB = dict(col=['#6a7482', '#7a6a5a', '#5e6876', '#86786a'], shade='#262b33', line='#0a0806', lw=3, bour='#2a1c12', seed=4)
    b += teeth_on(iU, 12, 96, 1, t0=.04, t1=.96, wid=1.12, **tB)
    b += teeth_on(iL, 11, 86, -1, t0=.05, t1=.95, wid=1.12, **tB)
    # stand: brass rods + plinth
    for sg in (-1, 1):
        b += f'<rect x="{JX + sg * 200 - 7}" y="{JY + 400}" width="14" height="{980 - JY - 400}" fill="#b08a4a" stroke="#1a0f08" stroke-width="3"/>'
    b += f'<rect x="{JX - 300}" y="965" width="600" height="40" rx="6" fill="url(#woodA)" stroke="#120a05" stroke-width="4"/>'
    b += f'<rect x="{JX - 70}" y="975" width="140" height="20" rx="3" fill="#d9b25a" stroke="#3a2a10" stroke-width="2"/>'
    # single fossil tooth on a small plinth (left foreground)
    tdef, tg = tooth(470, 735, 1.25, rot=-8, idp='tA')
    d += tdef
    b += '<path d="M420 -20 L520 -20 L700 960 L240 960Z" fill="#fff2d0" opacity=".05" filter="url(#b12)"/>'
    b += '<ellipse cx="470" cy="740" rx="230" ry="210" fill="#ffd890" opacity=".22" filter="url(#b50)"/>'
    b += '<path d="M330 880 L610 880 L640 990 L300 990Z" fill="url(#woodA)" stroke="#120a05" stroke-width="4"/><rect x="310" y="866" width="320" height="22" rx="4" fill="#6a4a2e" stroke="#120a05" stroke-width="4"/>'
    b += tg
    b += '<path d="M330 600 L330 866 M610 600 L610 866 M330 600 L610 600" fill="none" stroke="#d8f0ff" stroke-width="3" opacity=".35"/>'
    b += '<rect x="330" y="600" width="280" height="266" fill="#cfeeff" opacity=".05"/><path d="M350 620 L400 620 L350 700Z" fill="#fff" opacity=".15"/>'
    for sx_, sy_, ss in ((JX - 520, 200, 20), (JX + 520, 260, 22), (JX + 380, 120, 16), (620, 640, 16), (JX - 300, 900, 14), (JX + 560, 700, 16)):
        b += spark(sx_, sy_, ss, col='#fff1c8')
    b += '<rect width="1920" height="1080" fill="url(#vigA)"/>'
    b += veil('M0 0 H920 Q900 330 640 450 Q340 540 0 500Z', .62)
    b += veil('M1580 880 H1920 V1080 H1580Z', .4)
    return page('#0e0906', svg(d, b), [('KNOWN BY ITS', 112, 'w'), ('TEETH', 250, 'y')], outline='#120a05')


# =============================== B: a giant crumbling into stone ===============================
def make_B():
    rnd = random.Random(8)
    SX, SY, SS, SR = 1180, 470, 1.25, -9
    d = FILTERS
    d += lin('seaB', [(0, '#1d8fb0'), (.35, '#0f5a7e'), (.75, '#06263e'), (1, '#030f1c')])
    d += rad('sunB', 1250, -80, 900, [(0, '#e9fdff', .85), (.4, '#7fe0f0', .3), (1, '#2aa0c8', 0)])
    d += rad('haloB', SX + 120, SY, 760, [(0, '#c8fbff', .55), (.4, '#5fd0e8', .25), (1, '#1a6a8a', 0)])
    d += rad('vigB', 960, 540, 1150, [(0, '#000', 0), (.6, '#000', 0), (1, '#000', .7)])
    # fade mask for the tail (in shark-local units: nose x=1000, tail tip x=-82)
    d += ('<linearGradient id="fadeB" gradientUnits="userSpaceOnUse" x1="-160" y1="0" x2="430" y2="0"><stop offset="0" stop-color="#000"/>'
          '<stop offset=".5" stop-color="#808080"/><stop offset="1" stop-color="#fff"/></linearGradient>')
    d += ('<filter id="dissB" filterUnits="userSpaceOnUse" x="-400" y="-500" width="2000" height="1000">'
          '<feTurbulence type="fractalNoise" baseFrequency=".028" numOctaves="3" seed="6" result="n"/><feColorMatrix in="n" type="matrix" '
          'values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  1 0 0 0 0" result="na"/>'
          '<feComposite in="SourceGraphic" in2="n" operator="arithmetic" k1="0" k2="1" k3="1.5" k4="-.36" result="c"/>'
          '<feComponentTransfer in="c"><feFuncR type="discrete" tableValues="0 1"/><feFuncG type="discrete" tableValues="0 1"/>'
          '<feFuncB type="discrete" tableValues="0 1"/><feFuncA type="discrete" tableValues="1"/></feComponentTransfer></filter>')
    d += ('<mask id="mB" maskUnits="userSpaceOnUse" x="-400" y="-500" width="2000" height="1000">'
          '<rect x="-400" y="-500" width="2000" height="1000" fill="url(#fadeB)" filter="url(#dissB)"/></mask>')
    b = '<rect width="1920" height="1080" fill="url(#seaB)"/>'
    b += '<rect width="1920" height="1080" fill="url(#sunB)"/>'
    # god rays
    for x0, w, o in ((700, 120, .07), (980, 180, .08), (1300, 140, .09), (1560, 200, .06), (420, 120, .05)):
        b += f'<path d="M{x0} -20 L{x0 + w} -20 L{x0 + w - 260} 1100 L{x0 - 420} 1100Z" fill="#dffcff" opacity="{o}"/>'
    # surface ripples
    for i in range(30):
        x = rnd.randint(-40, 1920); b += f'<path d="M{x} {rnd.randint(4, 40)} q30 -8 60 0" stroke="#eaffff" stroke-width="3" fill="none" opacity=".35"/>'
    # distant school of fish (depth)
    for _ in range(40):
        x, y = rnd.randint(1450, 1880), rnd.randint(150, 330)
        b += f'<path d="M{x} {y} q8 -4 16 0 q-8 4 -16 0z M{x + 16} {y} l6 -4 v8z" fill="#9fd8e8" opacity=".35"/>'
    # sea floor
    b += '<path d="M0 930 Q300 890 640 912 Q980 940 1300 905 Q1620 880 1920 915 V1080 H0Z" fill="#0a2430"/>'
    b += '<path d="M0 960 Q400 930 800 958 Q1200 985 1920 950 V1080 H0Z" fill="#06161e"/>'
    for _ in range(30):
        x = rnd.randint(0, 1500); b += f'<ellipse cx="{x}" cy="{rnd.randint(935, 1060)}" rx="{rnd.randint(8, 30)}" ry="{rnd.randint(4, 10)}" fill="#1a3a44" opacity=".7"/>'
    b += f'<ellipse cx="{SX + 120}" cy="{SY}" rx="900" ry="620" fill="url(#haloB)"/>'
    sd, sg = shark(SX, SY, SS, rot=SR, mouth='open', idp='sB', top='#2a4656', mid='#6a8a98', rim='#d8fbff', glow='#9ff0ff', glow_op=.45, mask='mB')
    d += sd
    b += sg
    # stone chunks breaking off the tail end, sinking to the floor
    for i in range(70):
        lx = rnd.uniform(-120, 260); u = (260 - lx) / 380
        ly = rnd.uniform(-100, 110)
        gx, gy = shark_pt(SX, SY, SS, SR, False, lx, ly)
        gx -= u * rnd.uniform(60, 300); gy += u * u * rnd.uniform(40, 420)
        r = rnd.uniform(9, 24) * (1 - .3 * u); a = rnd.uniform(0, 360)
        c = rnd.choice(['#3e5a6a', '#5a7a8a', '#6c8896', '#d8e2e4', '#4a6676'])
        pts = [(gx + r * rnd.uniform(.7, 1.2) * math.cos(math.radians(a + k * 90 + rnd.uniform(-20, 20))), gy + r * rnd.uniform(.7, 1.2) * math.sin(math.radians(a + k * 90 + rnd.uniform(-20, 20)))) for k in range(4)]
        b += f'<polygon points="{P(pts)}" fill="{c}" stroke="#0b161d" stroke-width="3" stroke-linejoin="round" opacity="{max(.35, 1 - u * .5):.2f}"/>'
    # dust trail
    for i in range(70):
        lx = rnd.uniform(-120, 200); gx, gy = shark_pt(SX, SY, SS, SR, False, lx, rnd.uniform(-120, 120))
        b += f'<circle cx="{gx - rnd.uniform(60, 360):.0f}" cy="{gy + rnd.uniform(0, 420):.0f}" r="{rnd.choice([2, 3, 4])}" fill="#e6f6ff" opacity="{rnd.uniform(.2, .55):.2f}"/>'
    # fossil teeth already lying on the floor (what remains)
    for i, (tx, ty, ts, tr) in enumerate(((560, 975, .42, 70), (720, 995, .36, -40), (960, 968, .46, 15), (430, 1015, .34, 120), (1170, 992, .36, -70))):
        td, tg = tooth(tx, ty, ts, rot=tr, idp=f'tB{i}'); d += td
        b += f'<ellipse cx="{tx}" cy="{ty + 18}" rx="{ts * 120:.0f}" ry="{ts * 24:.0f}" fill="#000" opacity=".35"/>' + tg
    # bubbles from the gape
    for i in range(14):
        gx, gy = shark_pt(SX, SY, SS, SR, False, 980 + rnd.uniform(-40, 40), 60 - i * 26)
        b += f'<circle cx="{gx + rnd.uniform(-20, 40):.0f}" cy="{gy - i * 14:.0f}" r="{rnd.choice([5, 7, 9])}" fill="none" stroke="#eaffff" stroke-width="2.4" opacity=".6"/>'
    for sx_, sy_, ss in ((1620, 210, 22), (900, 260, 18), (1720, 560, 16), (1080, 760, 16), (560, 620, 14)):
        b += spark(sx_, sy_, ss, col='#f4ffff')
    b += '<rect width="1920" height="1080" fill="url(#vigB)"/>'
    b += veil('M0 0 H980 Q960 330 700 450 Q380 540 0 500Z', .62)
    b += veil('M1580 880 H1920 V1080 H1580Z', .45)
    # diving frog, lower left, watching the tail crumble
    b += ''.join(f'<circle cx="{250 + k * 8}" cy="{640 - k * 46}" r="{6 + k}" fill="none" stroke="#eaffff" stroke-width="2.4" opacity=".55"/>' for k in range(4))
    b += frog(260, 900, 2.6, rot=8, look=(4, -3), helmet=True, armL='M-34 -24 q-22 -14 -24 -40', armR='M38 -24 q24 -4 34 -30',
              legs=((-20, -6, -34, 14, 20), (20, -6, 30, 18, -20)))
    return page('#06263e', svg(d, b), [('TOO BIG', 190, 'y'), ('TO SURVIVE?', 132, 'w')])


# =============================== C: Titanic bow pose on the shark, iceberg ahead ===============================
def make_C():
    rnd = random.Random(31)
    WL = 600
    SX, SY, SS, SR = 790, 652, .9, -8
    d = FILTERS
    d += lin('skyC', [(0, '#030814'), (.6, '#0c2040'), (1, '#1d4468')])
    d += lin('seaC', [(0, '#0f3550'), (.4, '#082236'), (1, '#020a14')])
    d += rad('moonC', 1580, 120, 700, [(0, '#f0fbff', .6), (.25, '#9fd8f0', .2), (1, '#2a5a8a', 0)])
    d += lin('iceC', [(0, '#ffffff'), (.5, '#d8f4ff'), (1, '#7fc8e8')], x2=1, y2=1)
    d += lin('iceU', [(0, '#7fe0f8'), (.5, '#2a8ab8'), (1, '#0a3050')])
    d += rad('haloC', 1500, 620, 620, [(0, '#c8f8ff', .6), (.4, '#5ac8e8', .25), (1, '#1a5a8a', 0)])
    d += rad('vigC', 960, 540, 1150, [(0, '#000', 0), (.6, '#000', 0), (1, '#000', .7)])
    b = f'<rect width="1920" height="{WL}" fill="url(#skyC)"/>'
    b += stars(170, WL - 40, col='#eaf6ff', op=.7, sparks=0)
    b += f'<rect width="1920" height="1080" fill="url(#moonC)"/>'
    b += '<circle cx="1580" cy="120" r="46" fill="#f4fbff"/><circle cx="1566" cy="110" r="9" fill="#d0e4ee" opacity=".6"/>'
    # aurora hint (polar)
    b += '<path d="M700 120 C900 40 1100 180 1300 90 C1450 30 1600 140 1800 70" fill="none" stroke="#7affc8" stroke-width="40" opacity=".12" filter="url(#b24)"/>'
    # far ice floes on the horizon
    b += f'<path d="M0 {WL} L60 {WL - 14} L150 {WL - 10} L220 {WL} Z M820 {WL} L860 {WL - 18} L940 {WL - 12} L990 {WL}Z" fill="#9fc8de" opacity=".55"/>'
    # underwater
    b += f'<rect y="{WL}" width="1920" height="{1080 - WL}" fill="url(#seaC)"/>'
    b += f'<ellipse cx="1500" cy="640" rx="700" ry="520" fill="url(#haloC)"/>'
    # iceberg: underwater mass (big, glowing) then the tip
    b += '<g transform="translate(100 0)">'
    under = f'M1180 {WL} C1130 680 1170 780 1260 850 C1340 900 1420 920 1470 900 C1530 870 1580 850 1640 830 C1720 790 1780 720 1800 {WL}Z'
    b += f'<path d="{under}" fill="#bff4ff" opacity=".35" filter="url(#b24)"/>'
    b += f'<path d="{under}" fill="url(#iceU)" stroke="#0a2a40" stroke-width="5"/>'
    b += f'<path d="M1230 {WL + 30} C1220 700 1280 790 1360 840" fill="none" stroke="#e8fcff" stroke-width="6" opacity=".55"/>'
    b += ''.join(f'<path d="M{1260 + k * 90} {WL + 40 + (k % 2) * 60} l60 70 l-30 60" fill="none" stroke="#e8fcff" stroke-width="3" opacity=".3"/>' for k in range(6))
    tip = f'M1200 {WL} L1260 430 L1320 380 L1370 250 L1430 160 L1480 220 L1530 190 L1600 330 L1660 360 L1700 470 L1760 520 L1790 {WL}Z'
    b += f'<path d="{tip}" fill="#e8fbff" opacity=".45" filter="url(#b24)"/>'
    b += f'<path d="{tip}" fill="url(#iceC)" stroke="#0a2a40" stroke-width="5" stroke-linejoin="round"/>'
    b += f'<path d="M1430 160 L1450 330 L1400 {WL} L1500 {WL} L1480 220Z" fill="#8ac8e4" opacity=".55"/>'
    b += f'<path d="M1530 190 L1560 360 L1640 {WL} L1700 {WL} L1660 360 L1600 330Z" fill="#6ab0d4" opacity=".55"/>'
    b += '<path d="M1270 425 L1320 380 L1370 250 L1430 160" fill="none" stroke="#fff" stroke-width="6" opacity=".9"/></g>'
    # waterline
    b += f'<rect x="0" y="{WL - 3}" width="1920" height="6" fill="#bfe8ff" opacity=".7"/>'
    for _ in range(40):
        x = rnd.randint(0, 1900); b += f'<path d="M{x} {WL + rnd.randint(-6, 10)} l{rnd.randint(20, 70)} 0" stroke="#dff4ff" stroke-width="2" opacity=".35"/>'
    # moon path on the water
    b += f'<path d="M1520 {WL} L1640 {WL} L1700 1080 L1460 1080Z" fill="#dff4ff" opacity=".04"/>'
    # the shark (head and dorsal above the waterline: split view)
    sd, sg = shark(SX, SY, SS, rot=SR, mouth='closed', idp='sC', top='#3a5a70', mid='#86a6b6', rim='#eafaff', glow='#8fe8ff', glow_op=.5)
    d += sd
    d += f'<clipPath id="belowC"><rect x="0" y="{WL}" width="1920" height="600"/></clipPath><clipPath id="aboveC"><rect x="0" y="0" width="1920" height="{WL}"/></clipPath>'
    b += f'<g clip-path="url(#aboveC)">{sg}</g>'
    b += f'<g clip-path="url(#belowC)" opacity=".92">{sg}</g>'
    b += f'<rect x="0" y="{WL}" width="1920" height="480" fill="#0a3a5a" opacity=".24"/>'
    b += f'<rect x="0" y="{WL - 2}" width="1920" height="4" fill="#d8f2ff" opacity=".55"/>'
    # bow wave / spray where the shark breaks the surface
    nx, ny = shark_pt(SX, SY, SS, SR, False, 1000, 0)
    for k in range(5):
        b += f'<path d="M{nx - 40 - k * 30:.0f} {WL - 2} q{60 + k * 10} {-36 - k * 8} {130 + k * 20} -6" fill="none" stroke="#f2fbff" stroke-width="{6 - k}" opacity="{.8 - k * .12:.2f}" stroke-linecap="round"/>'
    for _ in range(30):
        b += f'<circle cx="{nx + rnd.uniform(-60, 120):.0f}" cy="{WL - rnd.uniform(0, 70):.0f}" r="{rnd.choice([2, 3, 4])}" fill="#f2fbff" opacity=".8"/>'
    fx0, fy0 = shark_pt(SX, SY, SS, SR, False, 600, -132)
    b += f'<path d="M{fx0 - 330:.0f} {WL + 2} q160 -10 330 -4 q120 2 240 -2" fill="none" stroke="#eaf8ff" stroke-width="4" opacity=".55"/>'
    # wake behind
    for k in range(6):
        b += f'<path d="M{200 - k * 30} {WL + 4 + k * 3} q200 -12 420 -2" fill="none" stroke="#eaf8ff" stroke-width="3" opacity="{.4 - k * .05:.2f}"/>'
    # frog on the snout, arms wide (the bow pose), scarf blowing back
    hx, hy = shark_pt(SX, SY, SS, SR, False, 905, -78)
    scarf = ('<path d="M-22 -30 q28 12 56 0 l2 10 q-30 12 -60 0z" fill="#d84a3a" stroke-width="3"/>'
             '<path d="M-20 -24 q-30 -6 -58 -20 l-6 14 q30 14 60 18z" fill="#e85a46" stroke-width="3"/><path d="M-76 -30 l-12 -4 M-78 -22 l-12 2" stroke-width="3"/>')
    cap = '<path d="M-24 -80 Q-20 -118 8 -120 Q36 -118 40 -80Z" fill="#3a6ab8" stroke-width="3.4"/><path d="M-26 -86 L42 -86 L42 -77 L-26 -77Z" fill="#f2f2f2" stroke-width="2.6"/><circle cx="8" cy="-124" r="9" fill="#f2f2f2" stroke-width="3"/>'
    b += frog(hx, hy + 4, 2.2, rot=SR, look=(5, -2), armL='M-34 -26 q-34 -16 -64 -16', armR='M38 -26 q30 -16 58 -20',
              legs=((-20, -6, -26, 4, 0), (20, -6, 26, 4, 0)), mid=scarf, head=cap)
    for sx_, sy_, ss in ((1430, 120, 20), (1120, 300, 16), (1760, 300, 16), (1680, 760, 18), (1240, 900, 14), (980, 200, 14)):
        b += spark(sx_, sy_, ss, col='#f2fbff')
    b += '<rect width="1920" height="1080" fill="url(#vigC)"/>'
    b += veil('M0 0 H900 Q880 360 640 480 Q340 560 0 520Z', .55)
    b += veil('M1580 880 H1920 V1080 H1580Z', .45)
    return page('#030814', svg(d, b), [('THE OCEAN', 124, 'w'), ('TURNED', 124, 'w'), ('COLD', 236, 'y')])


if __name__ == '__main__':
    for n, fn in (('A', make_A), ('B', make_B), ('C', make_C)):
        open(os.path.join(HERE, f'{n}.html'), 'w').write(fn())
    print('ok')
