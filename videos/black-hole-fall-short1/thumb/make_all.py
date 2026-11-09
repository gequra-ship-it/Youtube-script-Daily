# Shorts thumbnails (style B, guideline 16-9) for black-hole-fall-short1..5. VERTICAL 1080x1920, glow hero top half, hook centred y 860-1240, frog bottom.
# Run: python3 videos/black-hole-fall-short1/thumb/make_all.py [1 2 3 4 5] -> videos/black-hole-fall-shortN/thumb/A.html
# 1 NOTHING CASTS A SHADOW  pure-black shadow ringed by the photon ring and lensed starlight arcs; frog astronaut tethered to the spacecraft (short1 S01-S07)
# 2 YOU FREEZE              astronaut trail at the horizon: white -> orange -> crimson -> ghost (redshift, slow-down); frog friend at the telescope on the mother ship (short2 S02-S07)
# 3 NO COMING BACK          inside the horizon: the outside universe squeezed into a bright blue circular window behind, dark funnel ahead; frog looks back over its shoulder (short3 S01, S08-S12)
# 4 STRETCHED INTO RIBBONS  feet-first astronaut stretched into a thin thread toward a small black hole, converging field lines, ribbons of matter; frog in shock (short4 S04-S11)
# 5 NO ONE KNOWS YET        black hole with faint Hawking glow, particle pairs splitting at the edge, DNA / atom / memory photo spiralling in and misting away; puzzled frog (short5 S05-S14)
import os, sys, math, random, shutil
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
sys.path.insert(0, os.path.join(REPO, 'tools'))
sys.path.insert(0, os.path.join(REPO, 'videos', 'trilobite-extinction', 'thumb'))
from make import frog, FILTERS, INK, GREEN   # shared posable frog (eye white #f4f5ea, pupil kept inside)
from thumb_lib import vpage, vsvg, lin, rad, spark, fireflies, halo, darkband

W, H = 1080, 1920
Y = '<span class="g">%s</span>'


def vig(id='vig', a=.8):
    return rad(id, 540, 900, 1250, [(0, '#000', 0), (.5, '#000', 0), (1, '#000', a)])


def stars(rnd, n, y0=0, y1=H, col='#e8f0ff', big=8):
    o = ''.join(f'<circle cx="{rnd.uniform(0, W):.0f}" cy="{rnd.uniform(y0, y1):.0f}" r="{rnd.choice([1.1, 1.6, 2.2])}" fill="{col}" opacity="{rnd.uniform(.25, .9):.2f}"/>' for _ in range(n))
    for _ in range(big):
        x, y = rnd.uniform(30, W - 30), rnd.uniform(y0 + 20, y1 - 20)
        o += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="9" fill="{col}" opacity=".25" filter="url(#b6)"/>' + spark(x, y, rnd.choice([10, 14, 18]), col='#f4f8ff', op=.8)
    return o


def arc(cx, cy, r, a0, a1):
    x0, y0 = cx + r * math.cos(math.radians(a0)), cy + r * math.sin(math.radians(a0))
    x1, y1 = cx + r * math.cos(math.radians(a1)), cy + r * math.sin(math.radians(a1))
    return f'M{x0:.1f} {y0:.1f} A{r} {r} 0 {1 if abs(a1 - a0) > 180 else 0} 1 {x1:.1f} {y1:.1f}'


def space_helmet(tint='#cfe8ff'):
    """glass bubble helmet + collar for the frog (frog-local coords, drawn as front layer)"""
    return (f'<circle cx="6" cy="-58" r="47" fill="{tint}" fill-opacity=".13" stroke="#eef4ff" stroke-width="4.5"/>'
            '<path d="M-28 -82 q12 -18 32 -21" fill="none" stroke="#fff" stroke-width="5" opacity=".85"/><path d="M44 -42 q6 -10 6 -22" fill="none" stroke="#fff" stroke-width="3" opacity=".5"/>'
            '<ellipse cx="6" cy="-14" rx="40" ry="9" fill="#d9dee8" stroke-width="3.2"/><path d="M-30 -16 q36 8 72 0" fill="none" stroke="#fff" stroke-width="2.2" opacity=".8"/>')


def astro(x, y, s, suit='#f4f6fa', shade='#c3cad6', visor='#1a2a44', op=1, wave=0, beacon='#ff5040', line='#151a26'):
    """cute astronaut, origin between the boots; wave 0..1 lifts the right arm"""
    lw = 4.2
    g = f'<g transform="translate({x} {y}) scale({s})" opacity="{op}" stroke="{line}" stroke-width="{lw}" stroke-linejoin="round" stroke-linecap="round">'
    g += f'<rect x="-48" y="-122" width="96" height="84" rx="16" fill="{shade}"/>'                                   # backpack
    g += f'<rect x="-31" y="-44" width="26" height="40" rx="9" fill="{suit}"/><rect x="5" y="-44" width="26" height="40" rx="9" fill="{suit}"/>'
    g += f'<ellipse cx="-19" cy="-2" rx="19" ry="10" fill="{shade}"/><ellipse cx="19" cy="-2" rx="19" ry="10" fill="{shade}"/>'
    g += f'<rect x="-38" y="-116" width="76" height="82" rx="24" fill="{suit}"/>'
    g += f'<path d="M-38 -60 q38 12 76 0" fill="none" stroke="{shade}" stroke-width="6"/>'
    g += f'<rect x="-18" y="-96" width="36" height="24" rx="5" fill="{shade}"/><circle cx="-8" cy="-84" r="4" fill="#5ad0ff" stroke="none"/><circle cx="6" cy="-84" r="4" fill="#ffd060" stroke="none"/>'
    g += f'<path d="M-34 -104 q-26 20 -26 56" fill="none" stroke="{line}" stroke-width="26"/><path d="M-34 -104 q-26 20 -26 56" fill="none" stroke="{suit}" stroke-width="17"/>'
    g += f'<circle cx="-60" cy="-46" r="12" fill="{shade}"/>'
    ax, ay = 34 + 30 * (1 - wave), -104 + 56 * (1 - wave) - 70 * wave
    g += f'<path d="M34 -104 Q{40 + 40 * wave:.0f} {-110 - 10 * wave:.0f} {ax:.0f} {ay:.0f}" fill="none" stroke="{line}" stroke-width="26"/><path d="M34 -104 Q{40 + 40 * wave:.0f} {-110 - 10 * wave:.0f} {ax:.0f} {ay:.0f}" fill="none" stroke="{suit}" stroke-width="17"/>'
    g += f'<circle cx="{ax:.0f}" cy="{ay:.0f}" r="12" fill="{shade}"/>'
    g += f'<circle cx="0" cy="-152" r="44" fill="{suit}"/>'
    g += f'<ellipse cx="2" cy="-150" rx="31" ry="25" fill="{visor}"/><path d="M-16 -162 q8 -9 22 -9" fill="none" stroke="#fff" stroke-width="4" opacity=".75"/>'
    if beacon:
        g += f'<rect x="-6" y="-206" width="12" height="12" rx="3" fill="{shade}"/><circle cx="0" cy="-208" r="22" fill="{beacon}" opacity=".45" stroke="none" filter="url(#b6)"/><circle cx="0" cy="-208" r="7" fill="{beacon}"/>'
    return g + '</g>'


def save(n, bg, d, b, lines, outline, top):
    out = os.path.join(REPO, 'videos', f'black-hole-fall-short{n}', 'thumb'); os.makedirs(out, exist_ok=True)
    for f in ('common.css', 'Fredoka-700.woff2'):
        if not os.path.exists(os.path.join(out, f)):
            shutil.copy(os.path.join(REPO, 'tools', 'assets', 'thumb_v', f), out)
    open(os.path.join(out, 'A.html'), 'w').write(vpage(bg, vsvg(d, b), lines, outline=outline, top=top))


# ================= 1: NOTHING CASTS A SHADOW =================
def make_1():
    rnd = random.Random(21)
    CX, CY, R = 540, 480, 230
    d = FILTERS + rad('bg1', CX, CY, 1500, [(0, '#2a1e10', 1), (.35, '#0c0a16', 1), (1, '#020208', 1)]) + vig()
    d += halo('h1', CX, CY, 560, inner='#fff4d0', outer='#e0a040')
    b = f'<rect width="{W}" height="{H}" fill="url(#bg1)"/>' + stars(rnd, 260, big=10)
    b += f'<circle cx="{CX}" cy="{CY}" r="560" fill="url(#h1)" opacity=".55"/>'
    # lensed starlight: tangential arcs crowding the ring, brighter close in
    for _ in range(170):
        r = R + 18 + abs(rnd.gauss(0, 85))
        a0 = rnd.uniform(0, 360); span = rnd.uniform(6, 40) * (1.4 - min(1, (r - R) / 300))
        col = rnd.choice(['#fff6dc', '#ffe0a0', '#cfe2ff', '#ffffff', '#ffcf80'])
        w = rnd.choice([1.6, 2.4, 3.4]) * (1.3 if r < R + 60 else 1)
        op = max(.25, 1 - (r - R) / 330)
        b += f'<path d="{arc(CX, CY, r, a0, a0 + span)}" fill="none" stroke="{col}" stroke-width="{w}" stroke-linecap="round" opacity="{op:.2f}"/>'
    # the big mirrored arcs (Einstein-ring pieces), glowing
    for r, a0, a1, w in ((292, 200, 335, 9), (300, 20, 160, 8), (340, 240, 300, 5), (350, 60, 115, 5)):
        b += f'<path d="{arc(CX, CY, r, a0, a1)}" fill="none" stroke="#ffd890" stroke-width="{w * 4}" opacity=".35" filter="url(#b12)" stroke-linecap="round"/>'
        b += f'<path d="{arc(CX, CY, r, a0, a1)}" fill="none" stroke="#fff8e8" stroke-width="{w}" stroke-linecap="round"/>'
    # photon ring
    b += f'<circle cx="{CX}" cy="{CY}" r="{R + 14}" fill="none" stroke="#ffc860" stroke-width="44" opacity=".55" filter="url(#b12)"/>'
    b += f'<circle cx="{CX}" cy="{CY}" r="{R + 12}" fill="none" stroke="#fff2c8" stroke-width="10"/>'
    b += f'<circle cx="{CX}" cy="{CY}" r="{R + 26}" fill="none" stroke="#ffe6a8" stroke-width="2.5" opacity=".8"/>'
    # duplicated stars on the ring
    for k in range(26):
        a = math.radians(rnd.uniform(0, 360)); r = R + rnd.uniform(30, 120)
        b += spark(CX + r * math.cos(a), CY + r * math.sin(a), rnd.choice([7, 9, 12]), col='#fffbe8', op=.9)
    # the shadow: absolute darkness
    b += f'<circle cx="{CX}" cy="{CY}" r="{R}" fill="#000"/>'
    for sx, sy, ss in ((CX - 330, CY - 300, 26), (CX + 360, CY - 210, 22), (CX + 300, CY + 330, 24), (CX - 380, CY + 250, 20)):
        b += spark(sx, sy, ss, col='#fff6dc')
    b += darkband(860, 1250, .45)
    # spacecraft (right) with a tether to the frog (left)
    SX, SY = 790, 1560
    b += f'<ellipse cx="{SX}" cy="{SY}" rx="230" ry="150" fill="#ffd890" opacity=".10" filter="url(#b24)"/>'
    tether = f'M{SX - 150} {SY + 20} C{SX - 260} {SY + 120} 470 1520 370 1640'
    b += f'<path d="{tether}" fill="none" stroke="#0a0a12" stroke-width="9"/><path d="{tether}" fill="none" stroke="#e8c070" stroke-width="4"/>'
    b += (f'<g transform="translate({SX} {SY}) rotate(-14)" stroke="#12141c" stroke-width="5" stroke-linejoin="round">'
          '<path d="M110 -30 L170 -48 L170 48 L110 30Z" fill="#6a7080"/><ellipse cx="176" cy="0" rx="12" ry="50" fill="#3a3e4a"/>'
          '<path d="M-150 0 Q-150 -78 -60 -84 L110 -70 L110 70 L-60 84 Q-150 78 -150 0Z" fill="#dfe3ea"/>'
          '<path d="M-140 30 Q-60 70 110 52" fill="none" stroke="#a9b0bc" stroke-width="8"/>'
          '<rect x="-20" y="-80" width="10" height="160" fill="#c1c7d2" stroke-width="3"/><rect x="50" y="-74" width="10" height="148" fill="#c1c7d2" stroke-width="3"/>'
          '<ellipse cx="-92" cy="-10" rx="34" ry="30" fill="#ffe4a0"/><ellipse cx="-92" cy="-10" rx="34" ry="30" fill="#fff4c8" opacity=".9" filter="url(#b6)" stroke="none"/>'
          '<path d="M-110 -26 q10 -10 26 -8" fill="none" stroke="#fff" stroke-width="4"/>'
          '<path d="M10 -84 L30 -130 L46 -130" fill="none" stroke-width="5"/><circle cx="46" cy="-130" r="7" fill="#ff6a50"/></g>')
    b += '<ellipse cx="300" cy="1610" rx="230" ry="200" fill="#ffe0a0" opacity=".12" filter="url(#b24)"/>'
    b += frog(300, 1720, 3.3, rot=-10, look=(3, -4), mouth='O', front=space_helmet(),
              armR='M38 -22 q24 -10 30 -44', armL='M-34 -22 q-24 -2 -34 -26', legs=((-20, -6, -34, 10, -20), (20, -6, 30, 14, 20)))
    b += f'<rect width="{W}" height="{H}" fill="url(#vig)"/>'
    save(1, '#020208', d, b, [('NOTHING CASTS', 116, 'w'), ('A ' + Y % 'SHADOW', 184, 'w')], '#05040a', 872)


# ================= 2: YOU FREEZE =================
def make_2():
    rnd = random.Random(32)
    BX, BY, BR = 1010, -280, 640
    d = FILTERS + rad('bg2', 600, 300, 1700, [(0, '#3a0c10', 1), (.4, '#120612', 1), (1, '#04030a', 1)]) + vig()
    d += rad('rim2', BX, BY, BR + 200, [(0, '#ff3020', 0), (.74, '#ff3020', 0), (.77, '#ff6a3a', .9), (.84, '#c01818', .35), (1, '#c01818', 0)])
    b = f'<rect width="{W}" height="{H}" fill="url(#bg2)"/>' + stars(rnd, 230, big=8)
    b += f'<circle cx="{BX}" cy="{BY}" r="{BR + 200}" fill="url(#rim2)"/>'
    b += f'<circle cx="{BX}" cy="{BY}" r="{BR + 6}" fill="none" stroke="#ffb070" stroke-width="5" opacity=".9"/>'
    b += f'<circle cx="{BX}" cy="{BY}" r="{BR}" fill="#000"/>'
    # astronaut trail: white -> orange -> crimson -> ghost, slower (closer together) toward the horizon
    trail = ((235, 800, 1.45, '#f6f8fc', '#c6cdd9', 1, '#ffffff'), (520, 650, 1.25, '#ffb46a', '#d9803c', .92, '#ffb060'),
             (760, 520, 1.08, '#e0402e', '#9e2418', .78, '#ff4030'), (925, 430, .92, '#8a1a1a', '#5a1010', .42, '#c01818'))
    for k, (x, y, s, su, sh, op, gl) in enumerate(trail):
        b += f'<ellipse cx="{x}" cy="{y - 110 * s:.0f}" rx="{150 * s:.0f}" ry="{170 * s:.0f}" fill="{gl}" opacity="{.28 * op:.2f}" filter="url(#b24)"/>'
    for k, (x, y, s, su, sh, op, gl) in reversed(list(enumerate(trail))):
        b += astro(x, y, s * 1.12, suit=su, shade=sh, op=op, wave=.9 - .2 * k, beacon=['#ffffff', '#ffb060', '#ff4a30', '#a01010'][k], visor=['#1a2a44', '#3a1a10', '#3a0808', '#200404'][k])
    b += spark(330, 420, 26, col='#ffffff') + spark(120, 560, 18, col='#ffe0d0') + spark(560, 330, 16, col='#ffd0c0')
    b += darkband(860, 1250, .45)
    # mother ship deck + telescope + frog friend
    DY = 1790
    b += f'<path d="M0 {DY} L{W} {DY - 40} L{W} {H} L0 {H}Z" fill="#2a2e3a" stroke="#0c0e14" stroke-width="6"/>'
    b += f'<path d="M0 {DY + 24} L{W} {DY - 16}" stroke="#4a5060" stroke-width="5"/>'
    for x in range(60, W, 140):
        b += f'<rect x="{x}" y="{DY + 40 - x * 40 / W:.0f}" width="70" height="22" rx="6" fill="#ffd27a" opacity=".85"/>'
    b += f'<path d="M0 {DY - 70} L{W} {DY - 110}" stroke="#0c0e14" stroke-width="10"/><path d="M0 {DY - 70} L{W} {DY - 110}" stroke="#6a7080" stroke-width="5"/>'
    for x in range(40, W, 120):
        b += f'<path d="M{x} {DY - 70 - x * 40 / W:.0f} L{x} {DY - x * 40 / W:.0f}" stroke="#0c0e14" stroke-width="9"/><path d="M{x} {DY - 70 - x * 40 / W:.0f} L{x} {DY - x * 40 / W:.0f}" stroke="#6a7080" stroke-width="4"/>'
    FX, FY, S = 830, 1750, 3.0
    ex, ey = 776, 1566          # eyepiece at the frog's left eye
    ux, uy = -0.54, -0.84; L = 250
    ox, oy = ex + ux * L, ey + uy * L
    mx, my = ex + ux * 110, ey + uy * 110
    for lx in (mx - 120, mx + 20, mx + 110):
        b += f'<path d="M{mx:.0f} {my:.0f} L{lx:.0f} {DY - 20 - lx * 40 / W:.0f}" stroke="#0c0e14" stroke-width="12" stroke-linecap="round"/><path d="M{mx:.0f} {my:.0f} L{lx:.0f} {DY - 20 - lx * 40 / W:.0f}" stroke="#9aa2b2" stroke-width="5" stroke-linecap="round"/>'
    b += frog(FX, FY, S, look=(-5, -4), mouth='O', shadow=True, armL='M-34 -22 q-14 -30 -2 -66', armR='M38 -22 q16 6 18 24')
    ang = math.degrees(math.atan2(uy, ux))
    b += (f'<g transform="translate({ex} {ey}) rotate({ang:.1f})" stroke="#0c0e14" stroke-width="5" stroke-linejoin="round">'
          f'<rect x="-6" y="-10" width="30" height="20" rx="4" fill="#3a3e4a"/>'
          f'<path d="M22 -20 L{L - 30} -30 L{L - 30} 30 L22 20Z" fill="#c8ccd6"/><path d="M30 -12 L{L - 34} -18" stroke="#fff" stroke-width="4" opacity=".7"/>'
          f'<rect x="{L - 34}" y="-36" width="44" height="72" rx="8" fill="#5a6070"/><ellipse cx="{L + 10}" cy="0" rx="9" ry="34" fill="#ffd2b0"/></g>')
    b += f'<ellipse cx="{ox:.0f}" cy="{oy:.0f}" rx="40" ry="40" fill="#ffb090" opacity=".5" filter="url(#b12)"/>'
    b += f'<rect width="{W}" height="{H}" fill="url(#vig)"/>'
    save(2, '#04030a', d, b, [('YOU', 150, 'w'), (Y % 'FREEZE', 240, 'w')], '#0a0306', 868)


# ================= 3: NO COMING BACK =================
def make_3():
    rnd = random.Random(43)
    CX, CY, R = 540, 470, 250
    d = FILTERS + rad('bg3', CX, CY, 1500, [(0, '#0a1430', 1), (.3, '#04060f', 1), (1, '#000000', 1)]) + vig(a=.9)
    d += rad('win', CX, CY, R, [(0, '#ffffff', 1), (.35, '#e4f4ff', 1), (.7, '#6ab8ff', 1), (.92, '#3a5cff', 1), (1, '#7a40ff', 1)])
    d += halo('h3', CX, CY, 620, inner='#d8f0ff', outer='#3a7aff')
    d += f'<clipPath id="wc"><circle cx="{CX}" cy="{CY}" r="{R}"/></clipPath>'
    b = f'<rect width="{W}" height="{H}" fill="url(#bg3)"/>'
    # funnel lines: space itself pointing one way, toward the dark ahead (down)
    for k in range(-9, 10):
        x0 = CX + k * 120
        b += f'<path d="M{x0} {-40} C{x0} 700 {CX + k * 50} 1300 {CX + k * 6} 2100" fill="none" stroke="#3a4a9a" stroke-width="2.4" opacity="{.35 - abs(k) * .015:.2f}"/>'
    for y in range(1000, 1920, 110):
        rx = 900 - (y - 1000) * .55
        b += f'<ellipse cx="{CX}" cy="{y}" rx="{rx:.0f}" ry="{rx * .16:.0f}" fill="none" stroke="#3a4a9a" stroke-width="2.2" opacity=".28"/>'
    b += f'<circle cx="{CX}" cy="{CY}" r="620" fill="url(#h3)" opacity=".6"/>'
    # rays leaking from the window
    for a in range(0, 360, 15):
        r0, r1 = R + 10, R + 260 + 80 * (a % 30 == 0)
        x0, y0 = CX + r0 * math.cos(math.radians(a)), CY + r0 * math.sin(math.radians(a))
        x1, y1 = CX + r1 * math.cos(math.radians(a)), CY + r1 * math.sin(math.radians(a))
        b += f'<path d="M{x0:.0f} {y0:.0f} L{x1:.0f} {y1:.0f}" stroke="#bfe0ff" stroke-width="5" opacity=".18" stroke-linecap="round"/>'
    b += f'<circle cx="{CX}" cy="{CY}" r="{R + 30}" fill="none" stroke="#7aa8ff" stroke-width="50" opacity=".55" filter="url(#b24)"/>'
    b += f'<circle cx="{CX}" cy="{CY}" r="{R}" fill="url(#win)"/>'
    # the squeezed universe inside: galaxies & stars crowding the rim
    g = ''
    for _ in range(200):
        r = R * (1 - abs(rnd.gauss(0, .28))); a = rnd.uniform(0, 2 * math.pi)
        x, y = CX + r * math.cos(a), CY + r * math.sin(a)
        g += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{rnd.choice([1.6, 2.4, 3.2])}" fill="#ffffff" opacity="{rnd.uniform(.5, 1):.2f}"/>'
    for _ in range(22):
        r = R * rnd.uniform(.5, .92); a = rnd.uniform(0, 2 * math.pi)
        x, y = CX + r * math.cos(a), CY + r * math.sin(a); s = rnd.uniform(8, 16); rot = math.degrees(a) + 90
        col = rnd.choice(['#ffffff', '#cfe6ff', '#b8a8ff'])
        g += (f'<g transform="translate({x:.0f} {y:.0f}) rotate({rot:.0f})"><ellipse rx="{s * 1.8:.0f}" ry="{s * .5:.0f}" fill="{col}" opacity=".55"/>'
              f'<ellipse rx="{s * .5:.0f}" ry="{s * .25:.0f}" fill="#fff"/></g>')
    b += f'<g clip-path="url(#wc)">{g}</g>'
    b += f'<circle cx="{CX}" cy="{CY}" r="{R}" fill="none" stroke="#e0d8ff" stroke-width="5"/>'
    # darkness closing in like jaws around the window
    jaw = ''
    for k in range(18):
        a = k * 20 + rnd.uniform(-4, 4)
        tip = R + 60 + rnd.uniform(0, 30); base = R + 260
        p = lambda rr, aa: (CX + rr * math.cos(math.radians(aa)), CY + rr * math.sin(math.radians(aa)))
        (x0, y0), (x1, y1), (x2, y2) = p(base, a - 9), p(tip, a), p(base, a + 9)
        jaw += f'<path d="M{x0:.0f} {y0:.0f} Q{(x0 + x1) / 2:.0f} {(y0 + y1) / 2:.0f} {x1:.0f} {y1:.0f} Q{(x2 + x1) / 2:.0f} {(y2 + y1) / 2:.0f} {x2:.0f} {y2:.0f}Z" fill="#02030a" opacity=".85"/>'
    b += jaw
    b += f'<circle cx="{CX}" cy="{CY}" r="{R + 520}" fill="none" stroke="#000" stroke-width="560" opacity=".55" filter="url(#b50)"/>'
    for sx, sy, ss in ((CX - 210, CY - 170, 22), (CX + 190, CY + 160, 18), (CX + 120, CY - 200, 16)):
        b += spark(sx, sy, ss, col='#ffffff')
    b += darkband(860, 1250, .5)
    # frog astronaut tumbling down, looking back up over its shoulder at the closing window; jetpack firing uselessly
    FX, FY = 760, 1680
    b += f'<ellipse cx="{FX}" cy="{FY - 120}" rx="230" ry="210" fill="#8ab8ff" opacity=".14" filter="url(#b24)"/>'
    pack = ('<rect x="-56" y="-62" width="30" height="54" rx="9" fill="#9aa4b8" stroke-width="3.2"/>'
            '<path d="M-52 -8 L-30 -8 L-34 2 L-48 2Z" fill="#5a6070" stroke-width="2.6"/>'
            '<ellipse cx="-41" cy="34" rx="16" ry="34" fill="#ff9a3a" stroke="none" opacity=".55" filter="url(#b6)"/>'
            '<path d="M-50 2 q2 46 9 66 q8 -20 9 -66z" fill="#ffb84a" stroke="#c0501a" stroke-width="2"/><path d="M-46 2 q2 26 5 38 q4 -12 5 -38z" fill="#fff6c0" stroke="none"/>')
    b += frog(FX, FY, 3.3, rot=14, look=(-4, -6), mouth='O', back=pack, front=space_helmet('#bcd8ff'),
              armL='M-34 -22 q-26 -12 -30 -48', armR='M38 -22 q22 10 24 32', legs=((-20, -6, -30, 16, -30), (20, -6, 36, 8, 30)))
    b += f'<rect width="{W}" height="{H}" fill="url(#vig)"/>'
    save(3, '#000000', d, b, [('NO COMING', 156, 'w'), (Y % 'BACK', 240, 'w')], '#02040c', 864)


# ================= 4: STRETCHED INTO RIBBONS =================
def make_4():
    rnd = random.Random(54)
    CX, CY, R = 540, 240, 78
    d = FILTERS + rad('bg4', CX, CY, 1600, [(0, '#4a1430', 1), (.3, '#1a0820', 1), (1, '#04020a', 1)]) + vig()
    d += halo('h4', CX, CY, 420, inner='#ffe6c0', outer='#ff5a8a')
    d += lin('suit4', [(0, '#ffffff'), (.5, '#f0e6f0'), (1, '#c8b8d0')], x2=1, y2=0)
    b = f'<rect width="{W}" height="{H}" fill="url(#bg4)"/>' + stars(rnd, 200, big=7)
    # converging field lines
    for k in range(28):
        a = math.radians(40 + k * (100 / 27))
        x1, y1 = CX + 1500 * math.cos(a), CY + 1500 * math.sin(a)
        b += f'<path d="M{x1:.0f} {y1:.0f} L{CX} {CY}" stroke="#ff8ab0" stroke-width="2" opacity=".16"/>'
    b += f'<circle cx="{CX}" cy="{CY}" r="420" fill="url(#h4)" opacity=".7"/>'
    b += f'<circle cx="{CX}" cy="{CY}" r="{R + 10}" fill="none" stroke="#ffb07a" stroke-width="36" opacity=".6" filter="url(#b12)"/>'
    b += f'<circle cx="{CX}" cy="{CY}" r="{R + 6}" fill="none" stroke="#fff0d8" stroke-width="7"/>'
    # ribbons of matter streaming into the hole
    cols = ['#ffd27a', '#ff8ab0', '#ffffff', '#9fd8ff', '#ffb07a']
    for k in range(16):
        side = -1 if k % 2 else 1
        x0 = CX + side * rnd.uniform(80, 420); y0 = rnd.uniform(560, 820)
        c1 = (CX + side * rnd.uniform(40, 220), rnd.uniform(380, 600))
        path = f'M{x0:.0f} {y0:.0f} Q{c1[0]:.0f} {c1[1]:.0f} {CX + side * rnd.uniform(4, 30):.0f} {CY + R * .8:.0f}'
        col = rnd.choice(cols); w = rnd.choice([3, 4, 6])
        b += f'<path d="{path}" fill="none" stroke="{col}" stroke-width="{w * 3}" opacity=".22" filter="url(#b6)"/><path d="{path}" fill="none" stroke="{col}" stroke-width="{w}" stroke-linecap="round" opacity=".85"/>'
    b += f'<circle cx="{CX}" cy="{CY}" r="{R}" fill="#000"/>'
    # stretched astronaut, falling feet first: boots up near the hole, helmet below; shoulders squeezed narrow
    ln = '#160a18'
    b += f'<ellipse cx="{CX}" cy="{560}" rx="110" ry="320" fill="#ffd0e0" opacity=".25" filter="url(#b24)"/>'
    legs = ''
    for dx, top in ((-12, 352), (12, 346)):
        p = f'M{CX + dx * 2.2:.0f} 620 C{CX + dx * 1.8:.0f} 520 {CX + dx * 1.1:.0f} 420 {CX + dx * .7:.0f} {top}'
        legs += f'<path d="{p}" fill="none" stroke="{ln}" stroke-width="30" stroke-linecap="round"/><path d="{p}" fill="none" stroke="#f4eef6" stroke-width="20" stroke-linecap="round"/>'
        legs += f'<ellipse cx="{CX + dx * .7:.0f}" cy="{top - 18}" rx="12" ry="26" fill="#b8a8c4" stroke="{ln}" stroke-width="4"/>'
    b += legs
    # thin arms stretched up alongside the body
    for side in (-1, 1):
        p = f'M{CX + side * 34} 700 C{CX + side * 46} 600 {CX + side * 36} 520 {CX + side * 26} 460'
        b += f'<path d="{p}" fill="none" stroke="{ln}" stroke-width="20" stroke-linecap="round"/><path d="{p}" fill="none" stroke="#f4eef6" stroke-width="12" stroke-linecap="round"/>'
        b += f'<ellipse cx="{CX + side * 26}" cy="452" rx="9" ry="16" fill="#b8a8c4" stroke="{ln}" stroke-width="4"/>'
    b += f'<path d="M{CX - 46} 760 C{CX - 50} 690 {CX - 36} 640 {CX - 30} 600 L{CX + 30} 600 C{CX + 36} 640 {CX + 50} 690 {CX + 46} 760Z" fill="url(#suit4)" stroke="{ln}" stroke-width="5"/>'
    b += f'<path d="M{CX - 40} 690 q40 10 80 0" fill="none" stroke="#ff8ab0" stroke-width="6"/>'
    b += f'<rect x="{CX - 15}" y="706" width="30" height="20" rx="4" fill="#c8b8d0" stroke="{ln}" stroke-width="3"/><circle cx="{CX - 6}" cy="716" r="3.5" fill="#5ad0ff"/><circle cx="{CX + 6}" cy="716" r="3.5" fill="#ffd060"/>'
    # helmet (lowest point), visor facing the viewer, a little squashed sideways
    b += f'<ellipse cx="{CX}" cy="810" rx="50" ry="58" fill="#f4eef6" stroke="{ln}" stroke-width="5"/>'
    b += f'<ellipse cx="{CX}" cy="814" rx="34" ry="40" fill="#2a1030" stroke="{ln}" stroke-width="4"/><path d="M{CX - 18} 794 q8 -10 20 -10" fill="none" stroke="#fff" stroke-width="4" opacity=".8"/>'
    b += f'<ellipse cx="{CX + 8}" cy="822" rx="10" ry="6" fill="#ffb0d0" opacity=".6"/>'
    # stretch marks: speed streaks either side
    for k in range(8):
        y = 380 + k * 50; dx = 70 + rnd.uniform(0, 40)
        for side in (-1, 1):
            b += f'<path d="M{CX + side * dx:.0f} {y + 40} L{CX + side * (dx - 6):.0f} {y - 10}" stroke="#fff" stroke-width="3" opacity=".45" stroke-linecap="round"/>'
    for sx, sy, ss in ((CX - 330, 200, 24), (CX + 320, 330, 20), (CX - 260, 620, 18), (CX + 280, 700, 22)):
        b += spark(sx, sy, ss, col='#fff0e0')
    b += darkband(860, 1250, .45)
    b += '<ellipse cx="290" cy="1590" rx="230" ry="210" fill="#ff8ab0" opacity=".12" filter="url(#b24)"/>'
    b += frog(290, 1720, 3.3, rot=-6, look=(3, -4), mouth='O', front=space_helmet('#ffd0e0'),
              armL='M-34 -22 q-24 -10 -26 -48', armR='M38 -22 q24 -10 26 -48', brows=True)
    b += '<path d="M440 1420 q8 12 0 18 q-8 -6 0 -18z" fill="#bfe8ff" stroke="#1d2b1c" stroke-width="3"/>'
    b += f'<rect width="{W}" height="{H}" fill="url(#vig)"/>'
    save(4, '#04020a', d, b, [('STRETCHED INTO', 112, 'w'), (Y % 'RIBBONS', 210, 'w')], '#0a0310', 876)


# ================= 5: NO ONE KNOWS YET =================
def make_5():
    rnd = random.Random(65)
    CX, CY, R = 540, 470, 170
    d = FILTERS + rad('bg5', CX, CY, 1500, [(0, '#24104a', 1), (.35, '#0c0820', 1), (1, '#020208', 1)]) + vig()
    d += halo('h5', CX, CY, 520, inner='#ffe6ff', outer='#a060ff')
    b = f'<rect width="{W}" height="{H}" fill="url(#bg5)"/>' + stars(rnd, 200, big=6, col='#efe6ff')
    # thermal mist evaporating away
    for _ in range(26):
        a = rnd.uniform(0, 2 * math.pi); r = rnd.uniform(R + 60, R + 360)
        b += f'<ellipse cx="{CX + r * math.cos(a):.0f}" cy="{CY + r * math.sin(a) * .8:.0f}" rx="{rnd.uniform(50, 120):.0f}" ry="{rnd.uniform(30, 70):.0f}" fill="{rnd.choice(["#b080ff", "#ff90d0", "#80d8ff"])}" opacity="{rnd.uniform(.06, .14):.2f}" filter="url(#b24)"/>'
    b += f'<circle cx="{CX}" cy="{CY}" r="520" fill="url(#h5)" opacity=".55"/>'
    # spiral stream of "you": dust of atoms
    for k in range(120):
        t = k / 120; a = 5.5 * t * math.pi + .6; r = R + 30 + (1 - t) * 300
        x, y = CX + r * math.cos(a), CY + r * math.sin(a) * .62
        b += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{2 + 3 * (1 - t):.1f}" fill="#ffe8a0" opacity="{.25 + .6 * (1 - t):.2f}"/>'
    b += f'<circle cx="{CX}" cy="{CY}" r="{R + 16}" fill="none" stroke="#e0a0ff" stroke-width="46" opacity=".6" filter="url(#b12)"/>'
    b += f'<circle cx="{CX}" cy="{CY}" r="{R + 8}" fill="none" stroke="#fbe8ff" stroke-width="6"/>'
    b += f'<circle cx="{CX}" cy="{CY}" r="{R}" fill="#000"/>'
    # particle pairs at the edge: one falls in, its partner escapes outward
    for ang in (-60, 30, 150, 225):
        a = math.radians(ang); ex, ey = CX + (R + 22) * math.cos(a), CY + (R + 22) * math.sin(a)
        ox, oy = CX + (R + 150) * math.cos(a), CY + (R + 150) * math.sin(a)
        ix, iy = CX + (R - 30) * math.cos(a), CY + (R - 30) * math.sin(a)
        b += f'<path d="M{ex:.0f} {ey:.0f} L{ox:.0f} {oy:.0f}" stroke="#9ff0ff" stroke-width="4" stroke-dasharray="2 10" stroke-linecap="round" opacity=".9"/>'
        b += f'<circle cx="{ox:.0f}" cy="{oy:.0f}" r="26" fill="#9ff0ff" opacity=".5" filter="url(#b6)"/><circle cx="{ox:.0f}" cy="{oy:.0f}" r="11" fill="#e8ffff"/>'
        b += f'<circle cx="{ix:.0f}" cy="{iy:.0f}" r="9" fill="#ff7ab0" opacity=".85"/>'
    # pieces of "you" being pulled in: DNA strand, an atom, a memory photo
    dna = ''
    for k in range(13):
        t = k / 12; x = 170 + 150 * t; y = 640 - 150 * t; ph = t * 2.6 * math.pi
        o1, o2 = 26 * math.sin(ph), -26 * math.sin(ph)
        nx, ny = .7, .7
        dna += f'<path d="M{x + o1 * nx:.0f} {y + o1 * ny:.0f} L{x + o2 * nx:.0f} {y + o2 * ny:.0f}" stroke="#ffe0f0" stroke-width="4" opacity=".8"/>'
    for sgn, col in ((1, '#ff7ab0'), (-1, '#7ad8ff')):
        pts = ' '.join(f'{170 + 150 * t + sgn * 26 * math.sin(t * 2.6 * math.pi) * .7:.0f},{640 - 150 * t + sgn * 26 * math.sin(t * 2.6 * math.pi) * .7:.0f}' for t in [i / 40 for i in range(41)])
        dna += f'<polyline points="{pts}" fill="none" stroke="#120820" stroke-width="13" stroke-linecap="round"/><polyline points="{pts}" fill="none" stroke="{col}" stroke-width="7" stroke-linecap="round"/>'
    b += f'<ellipse cx="245" cy="565" rx="120" ry="110" fill="#ff90d0" opacity=".18" filter="url(#b24)"/>' + dna
    for k in range(10):
        b += f'<circle cx="{330 + k * 9 + rnd.uniform(-6, 6):.0f}" cy="{480 - k * 4 + rnd.uniform(-8, 8):.0f}" r="{4 - k * .3:.1f}" fill="#ffd0f0" opacity="{.8 - k * .07:.2f}"/>'
    AX, AY = 850, 250
    b += f'<circle cx="{AX}" cy="{AY}" r="80" fill="#9ff0ff" opacity=".18" filter="url(#b12)"/>'
    for rot in (0, 60, 120):
        b += f'<ellipse cx="{AX}" cy="{AY}" rx="62" ry="22" transform="rotate({rot} {AX} {AY})" fill="none" stroke="#bff4ff" stroke-width="4"/>'
    b += f'<circle cx="{AX}" cy="{AY}" r="13" fill="#ffd27a" stroke="#120820" stroke-width="3"/>'
    PX, PY = 860, 640
    b += (f'<g transform="translate({PX} {PY}) rotate(18)"><rect x="-70" y="-62" width="140" height="124" rx="6" fill="#f4eee0" stroke="#120820" stroke-width="5"/>'
          '<rect x="-58" y="-52" width="116" height="84" fill="#7ac0e8"/><path d="M-58 32 L-58 0 L-20 -24 L10 6 L30 -10 L58 14 L58 32Z" fill="#5a9a4a"/>'
          '<circle cx="34" cy="-32" r="11" fill="#ffe08a"/><path d="M-58 -52 L58 -52 L58 32 L-58 32Z" fill="#fff" opacity=".12"/></g>')
    for k in range(10):
        b += f'<circle cx="{PX - 70 - k * 12 + rnd.uniform(-6, 6):.0f}" cy="{PY - 50 - k * 6 + rnd.uniform(-8, 8):.0f}" r="{4.5 - k * .35:.1f}" fill="#fff4dc" opacity="{.85 - k * .07:.2f}"/>'
    for sx, sy, ss in ((CX - 360, 260, 22), (CX + 140, 220, 18), (CX + 400, 470, 20), (CX - 120, 760, 16)):
        b += spark(sx, sy, ss, col='#fff0ff')
    b += darkband(860, 1250, .45)
    # puzzled frog, chin in hand, notebook held at its spine
    FX, FY = 800, 1730
    b += f'<ellipse cx="{FX}" cy="{FY - 130}" rx="230" ry="200" fill="#c0a0ff" opacity=".13" filter="url(#b24)"/>'
    book = ('<g transform="translate(-62 -14) rotate(-12)"><rect x="-26" y="-34" width="48" height="62" rx="4" fill="#e8d8a8" stroke-width="3.2"/>'
            '<rect x="-26" y="-34" width="9" height="62" fill="#b06a3a" stroke-width="3"/><path d="M-10 -20 l24 0 M-10 -10 l24 0 M-10 0 l18 0" stroke-width="2.4" opacity=".7"/></g>')
    b += frog(FX, FY, 3.3, look=(-4, -5), mouth='o', shadow=True, front=book,
              armL='M-34 -22 q-24 4 -28 -6', armR='M38 -22 q4 -10 -14 -18')
    b += f'<text x="{FX + 150}" y="{FY - 300}" font-family="Fredoka" font-weight="700" font-size="120" fill="#f2d27a" stroke="#0a0410" stroke-width="10" paint-order="stroke" transform="rotate(14 {FX + 150} {FY - 300})">?</text>'
    b += f'<rect width="{W}" height="{H}" fill="url(#vig)"/>'
    save(5, '#020208', d, b, [('NO ONE', 172, 'w'), (Y % 'KNOWS' + ' YET', 172, 'w')], '#06030c', 876)


if __name__ == '__main__':
    for n in sys.argv[1:] or ['1', '2', '3', '4', '5']:
        globals()[f'make_{n}'](); print('made', n)
