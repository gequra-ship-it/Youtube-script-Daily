# sacabambaspis-meme-fish thumbnails A-C, round 2 (guideline 16-6; round 1 kept in round1/). run: python3 make.py
# A  NOT OUR ANCESTOR        homage: Zallinger's "March of Progress" (walking silhouettes, crawler -> ape -> human) against a
#    sunset; the googly-eyed Helsinki model sits in the shallows turned away from the line, side-eyeing it. Script S36
#    ("Sacabambaspis is not our grandparent ... the fish is not our ancestor"), S42 ("Evolution is not a ladder").
# B  WAS IT A JOKE?          intuitive: huge close-up of the model's face pressed behind museum glass under a spotlight,
#    tiny visitors below (one raises a phone, a child jumps back). Script S02 ("Was the model a joke, or did this little
#    fish actually look like that?"), S03 (craft-store googly doll's eyes).
# C  460 MILLION YEARS LATER intuitive: the accurate fish swims out of a glowing phone whose screen is the Ordovician sea
#    (nautiloid, trilobites), hearts and chat bubbles rise. Script S43 ("Four hundred and sixty million years later, its
#    picture is on a phone screen in your hand").
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




# ------------------------------------------------------------------ the Helsinki museum model, side view (cartoon-simple)
# same plan and local units as saca(): snout at x=0 facing LEFT. Smooth silvery glaze, two googly doll eyes at the very
# front (far one peeks above the near one), small dark triangular open mouth, tiny tail fin. No fins, no jaws, no teeth.
def model_side(gid, tr, look=(10, 6)):
    d = (rg(gid + 'sg', [(0, '#ffffff', 1), (.3, '#dfe6e8', 1), (.72, '#8d999f', 1), (1, '#465056', 1)], cx=.32, cy=.2, r=.9)
         + lin(gid + 'bg', [(0, '#e9eeef'), (.45, '#a9b3b7'), (1, '#4a5459')])
         + rg(gid + 'w', [(0, '#ffffff', 1), (.75, '#f3f3f0', 1), (1, '#b9bcbc', 1)], cx=.4, cy=.35, r=.65))
    o = f'<g transform="{tr}">'
    o += f'<path d="{FIN}" fill="url(#{gid}bg)" stroke="{LINE}" stroke-width="5" stroke-linejoin="round"/>'
    o += f'<path d="{BODY}" fill="url(#{gid}bg)" stroke="{LINE}" stroke-width="6" stroke-linejoin="round"/>'
    o += f'<path d="{SHIELD}" fill="url(#{gid}sg)" stroke="{LINE}" stroke-width="6.5" stroke-linejoin="round"/>'
    # glaze highlights
    o += '<path d="M40,-70 C90,-112 200,-122 300,-100" fill="none" stroke="#fff" stroke-width="16" stroke-linecap="round" opacity=".6"/>'
    o += '<path d="M380,-70 C500,-70 620,-46 760,-22" fill="none" stroke="#fff" stroke-width="9" stroke-linecap="round" opacity=".5"/>'
    o += '<path d="M330,-86 C346,-30 348,30 334,84" fill="none" stroke="#5c676c" stroke-width="5" opacity=".6"/>'   # shield edge seam
    o += '<path d="M40,96 C150,118 260,112 345,86" fill="none" stroke="#30383c" stroke-width="10" opacity=".35"/>'
    # googly eyes: far one behind/above, near one in front
    for (ex, ey, r) in ((92, -96, 50), (56, -48, 64)):
        o += f'<circle cx="{ex + 4}" cy="{ey + 8}" r="{r + 4}" fill="#1d2326" opacity=".35"/>'
        o += f'<circle cx="{ex}" cy="{ey}" r="{r}" fill="url(#{gid}w)" stroke="{LINE}" stroke-width="5.5"/>'
        px, py = ex + look[0] * r / 64, ey + look[1] * r / 64 + r * .18
        o += f'<circle cx="{px:.1f}" cy="{py:.1f}" r="{r * .5:.1f}" fill="#0b0b0c"/><circle cx="{px - r * .16:.1f}" cy="{py - r * .18:.1f}" r="{r * .13:.1f}" fill="#fff"/>'
        o += f'<ellipse cx="{ex - r * .35:.1f}" cy="{ey - r * .5:.1f}" rx="{r * .28:.1f}" ry="{r * .12:.1f}" fill="#fff" transform="rotate(-25 {ex - r * .35:.1f} {ey - r * .5:.1f})"/>'
    # small dark open mouth at the very front
    o += f'<path d="M-2,26 C16,22 40,24 58,30 C46,52 26,66 10,70 C4,56 0,40 -2,26 Z" fill="#170a0b" stroke="{LINE}" stroke-width="5" stroke-linejoin="round"/>'
    return d, o + '</g>'


# ------------------------------------------------------------------ simple walking silhouettes (March of Progress style)
def _ik(ax, ay, bx, by, l1, l2, fwd):
    """2-link joint; fwd=True picks the candidate with the larger x (knees), False the smaller x (elbows)"""
    dx, dy = bx - ax, by - ay; dd = math.hypot(dx, dy) or 1e-6
    dd2 = min(dd, (l1 + l2) * .999)
    a = (l1 * l1 - l2 * l2 + dd2 * dd2) / (2 * dd2); h = math.sqrt(max(0, l1 * l1 - a * a))
    ux, uy = dx / dd, dy / dd
    mx, my = ax + ux * a, ay + uy * a
    c1, c2 = (mx - uy * h, my + ux * h), (mx + uy * h, my - ux * h)
    return max(c1, c2) if fwd else min(c1, c2)


def fig(x, G, H, lean=0, stride=.16, armf=(.13, .33), armb=(-.12, .32), legk=.96, armlen=.36, head=.07, headfwd=0, bulk=1.0):
    """walking silhouette (facing +x) as round-capped strokes + filled masses; returns list of parts"""
    out = []
    legL = .47 * H
    hip = (x, G - legL * legk)
    L = math.radians(lean)
    ux, uy = math.sin(L), -math.cos(L)
    sh = (hip[0] + ux * .30 * H, hip[1] + uy * .30 * H)
    for s in (-1, 1):
        ft = (x + s * stride * H, G - .03 * H)
        kn = _ik(hip[0], hip[1], ft[0], ft[1], legL / 2, legL / 2, True)
        out.append((f'M{hip[0]:.0f},{hip[1]:.0f} L{kn[0]:.0f},{kn[1]:.0f}', .105 * H * bulk))
        out.append((f'M{kn[0]:.0f},{kn[1]:.0f} L{ft[0]:.0f},{ft[1]:.0f}', .075 * H * bulk))
        out.append((f'M{ft[0] - .02 * H:.0f},{ft[1] + .005 * H:.0f} L{ft[0] + .075 * H:.0f},{ft[1] + .015 * H:.0f}', .04 * H))
    # torso: hips -> chest, wider at the chest
    out.append((f'M{hip[0]:.0f},{hip[1]:.0f} L{hip[0] + ux * .12 * H:.0f},{hip[1] + uy * .12 * H:.0f}', .15 * H * bulk))
    out.append((f'M{hip[0] + ux * .1 * H:.0f},{hip[1] + uy * .1 * H:.0f} L{sh[0] - ux * .03 * H:.0f},{sh[1] - uy * .03 * H:.0f}', .17 * H * bulk))
    hd = (sh[0] + ux * .085 * H + headfwd * H, sh[1] + uy * .085 * H - .03 * H)
    out.append((f'M{sh[0]:.0f},{sh[1]:.0f} L{hd[0]:.0f},{hd[1]:.0f}', .065 * H))
    out.append(('C', hd, head * H))
    if headfwd > .02:   # ape muzzle
        out.append((f'M{hd[0]:.0f},{hd[1]:.0f} L{hd[0] + head * H * 1.0:.0f},{hd[1] + head * H * .45:.0f}', head * H * 1.1))
    for t in (armb, armf):
        hx, hy = sh[0] + t[0] * H, sh[1] + t[1] * H
        el = _ik(sh[0], sh[1], hx, hy, armlen * H / 2, armlen * H / 2, False)
        out.append((f'M{sh[0]:.0f},{sh[1]:.0f} L{el[0]:.0f},{el[1]:.0f}', .07 * H * bulk))
        out.append((f'M{el[0]:.0f},{el[1]:.0f} L{hx:.0f},{hy:.0f}', .055 * H * bulk))
        out.append(('C', (hx, hy), .035 * H * bulk))
    return out


def fig_svg(parts, col, glow=None, gw=10, flt=''):
    def draw(c, extra):
        s = ''
        for p in parts:
            if p[0] == 'C':
                (cx, cy), r = p[1], p[2]
                s += f'<circle cx="{cx:.0f}" cy="{cy:.0f}" r="{r + extra / 2:.1f}" fill="{c}"/>'
            else:
                s += f'<path d="{p[0]}" stroke="{c}" stroke-width="{p[1] + extra:.1f}" fill="none" stroke-linecap="round" stroke-linejoin="round"/>'
        return s
    o = ''
    if glow:
        o += f'<g filter="{flt}" opacity=".9">{draw(glow, gw * 2.2)}</g>' + draw(glow, gw)
    return o + draw(col, 0)


# ============================================================ A: NOT OUR ANCESTOR  (homage: the March of Progress)
def build_A():
    random.seed(21)
    d = (lin('asky', [(0, '#1d2c4a'), (.38, '#6b3f5e'), (.62, '#e0744a'), (.8, '#ffc56e'), (1, '#fff0c0')])
         + rad('asun', 1440, 720, 520, [(0, '#fffbe6', 1), (.12, '#ffe7a3', .95), (.4, '#ffb15e', .45), (1, '#ff8a4a', 0)])
         + lin('aground', [(0, '#5a2e22'), (.25, '#2c1712'), (1, '#120807')])
         + lin('asea', [(0, '#f6b46a'), (.18, '#b8706a'), (.6, '#3c4a66'), (1, '#16203a')])
         + blur('ab4', 4) + blur('ab10', 10) + blur('ab26', 26) + blur('ab60', 60))
    b = '<rect width="1920" height="1080" fill="url(#asky)"/>'
    b += stars(40, 260, xmin=900, col='#ffe9d0', op=.45, sparks=0)
    # long horizontal clouds lit from below
    for (x, y, w, h, o) in ((980, 300, 700, 26, .5), (1250, 360, 620, 18, .55), (860, 420, 520, 16, .45), (1500, 230, 420, 14, .35), (300, 520, 600, 20, .3)):
        b += f'<ellipse cx="{x}" cy="{y}" rx="{w / 2}" ry="{h}" fill="#3a2442" opacity="{o}"/>'
        b += f'<ellipse cx="{x}" cy="{y + h * .55:.0f}" rx="{w / 2 - 30}" ry="{h * .35:.0f}" fill="#ffb27a" opacity="{o * .9:.2f}"/>'
    b += '<rect width="1920" height="1080" fill="url(#asun)"/>'
    b += '<circle cx="1440" cy="742" r="150" fill="#fff6d4" filter="url(#ab10)"/>'
    # far mountains (barren) + the ridge the figures walk on
    b += '<path d="M700,760 L820,700 L900,728 L1010,676 L1110,722 L1180,700 L1240,740 L1330,710 L1400,752 L1920,744 L1920,800 L700,800 Z" fill="#8a4a4a" opacity=".55"/>'
    G = 800
    b += f'<path d="M640,{G} C900,{G - 8} 1300,{G - 14} 1920,{G - 6} L1920,1080 L640,1080 Z" fill="url(#aground)"/>'
    b += f'<path d="M640,{G} C900,{G - 8} 1300,{G - 14} 1920,{G - 6}" fill="none" stroke="#ffcf8a" stroke-width="5" opacity=".8"/>'
    # shallow sea in the foreground-left: the fish lives here
    b += f'<path d="M0,742 C300,744 700,750 900,766 C990,776 1030,800 1050,860 C1080,940 1120,1010 1140,1080 L0,1080 Z" fill="url(#asea)"/>'
    b += '<path d="M0,742 C300,744 700,750 900,766 C990,776 1030,800 1050,860 C1080,940 1120,1010 1140,1080" fill="none" stroke="#ffe3a8" stroke-width="5" opacity=".7"/>'
    for i in range(46):   # sun glitter on the water
        x = random.randint(40, 860); y = random.randint(760, 1060)
        if x > 1000 - (1080 - y) * .2: continue
        b += f'<rect x="{x}" y="{y}" width="{random.randint(20, 70)}" height="3" rx="1.5" fill="#ffe7b0" opacity="{random.uniform(.25, .7):.2f}"/>'
    # ---- the march: lobe-fin crawler, knuckle-walker, stooped ape, early human, modern human (generic silhouettes)
    col = '#1a0e0c'
    gl = '#ffd27a'
    # crawler: a low lobe-finned animal leaving the water
    cr = ('<g transform="translate(1060 778)">'
          '<path d="M-110,10 C-70,-26 20,-34 70,-22 C96,-16 110,-6 116,8 C96,18 60,24 20,22 C-40,22 -90,22 -150,26 C-130,20 -118,16 -110,10 Z"/>'
          '<path d="M-30,16 L-46,34 L-30,36 Z"/><path d="M40,18 L58,32 L68,30 Z"/><path d="M-80,20 L-96,34 L-82,34 Z"/><path d="M76,10 L96,26 L104,22 Z"/></g>')
    b += f'<g fill="{gl}" stroke="{gl}" stroke-width="10" stroke-linejoin="round" filter="url(#ab10)" opacity=".9">{cr}</g>' + f'<g fill="{gl}" stroke="{gl}" stroke-width="7" stroke-linejoin="round">{cr}</g>'
    b += f'<g fill="{col}">{cr}</g>'
    figs = [
        fig(1215, G - 8, 270, lean=66, stride=.15, armf=(.26, .38), armb=(.10, .40), legk=.70, armlen=.5, head=.09, headfwd=.05, bulk=1.15),
        fig(1395, G - 10, 380, lean=36, stride=.15, armf=(.18, .44), armb=(-.02, .44), legk=.84, armlen=.48, head=.08, headfwd=.03, bulk=1.1),
        fig(1585, G - 10, 470, lean=14, stride=.16, armf=(.12, .38), armb=(-.10, .36), legk=.92, armlen=.40, head=.072, headfwd=.0),
        fig(1785, G - 8, 530, lean=3, stride=.17, armf=(.12, .33), armb=(-.11, .32), legk=.97, armlen=.36, head=.066),
    ]
    for p in figs:
        b += fig_svg(p, col, glow=gl, gw=8, flt='url(#ab10)')
    # dust puffs at the feet + long shadows toward the viewer
    for x in (1060, 1215, 1395, 1585, 1785):
        b += f'<ellipse cx="{x}" cy="{G + 6}" rx="60" ry="8" fill="#000" opacity=".45"/>'
    # ---- the meme model in the shallows, turned AWAY from the march, side-eyeing it
    b += '<ellipse cx="520" cy="840" rx="560" ry="230" fill="#ffd9a0" opacity=".28" filter="url(#ab60)"/>'
    dd, f = model_side('am', 'translate(84 800) rotate(-2) scale(.84 1.16)', look=(26, -10))
    d += dd; b += f
    # water line over the lower body (it sits in the shallows)
    b += '<path d="M0,950 C140,938 300,944 460,950 C620,956 800,950 1060,962 L1140,1080 L0,1080 Z" fill="#203050" opacity=".55"/>'
    b += '<path d="M0,950 C140,938 300,944 460,950 C620,956 800,950 1060,962" fill="none" stroke="#ffe6b0" stroke-width="5" opacity=".75"/>'
    for (x, y, w) in ((120, 960, 140), (380, 980, 180), (640, 966, 150), (240, 1010, 120), (520, 1030, 160)):
        b += f'<path d="M{x},{y} q{w / 4},-10 {w / 2},0 t{w / 2},0" fill="none" stroke="#ffd9a0" stroke-width="3" opacity=".45"/>'
    # rim light on the fish from the sun (right)
    for (x, y, s) in ((1080, 600, 18), (1700, 600, 14), (880, 700, 14), (640, 690, 16)):
        b += f'<circle cx="{x}" cy="{y}" r="{s * 2}" fill="#fff3d0" opacity=".35" filter="url(#ab4)"/>' + spark(x, y, s)
    return d, b


# ============================================================ B: WAS IT A JOKE?  (intuitive: giant model face behind glass)
def build_B():
    random.seed(5)
    d = (lin('bw', [(0, '#1a1438'), (.6, '#2b2050'), (1, '#120d24')])
         + rad('bspot', 1270, 380, 820, [(0, '#fff2cf', .75), (.35, '#f6c98a', .3), (1, '#f6c98a', 0)])
         + lin('bglass', [(0, '#bfe6ff'), (1, '#6fa7d6')], x2=1, y2=1)
         + lin('bfloor', [(0, '#3a2a52'), (1, '#0d0a1c')])
         + lin('bplinth', [(0, '#efe6d6'), (1, '#9c8f7c')])
         + blur('bb4', 4) + blur('bb14', 14) + blur('bb40', 40) + blur('bb80', 80))
    b = '<rect width="1920" height="1080" fill="url(#bw)"/>'
    b += '<rect width="1920" height="1080" fill="url(#bspot)"/>'
    b += '<path d="M1060,0 L1480,0 L1880,980 L640,980 Z" fill="#ffe6b8" opacity=".10" filter="url(#bb40)"/>'   # spotlight cone
    # floor + case plinth
    b += '<rect y="930" width="1920" height="150" fill="url(#bfloor)"/>'
    b += '<rect x="560" y="900" width="1400" height="60" fill="url(#bplinth)" stroke="#2a1f3a" stroke-width="4"/>'
    b += '<rect x="560" y="958" width="1400" height="14" fill="#000" opacity=".35"/>'
    # ---- the model face: huge, filling the case
    b += '<ellipse cx="1290" cy="560" rx="640" ry="460" fill="#fff0c8" opacity=".33" filter="url(#bb80)"/>'
    b += '<path d="M1700,520 C1820,540 1900,600 1940,660 L1940,900 L1600,900 Z" fill="#7f8b91" stroke="#1b2022" stroke-width="6"/>'   # body going back
    dd, f = model_face('bm', 'translate(1350 590) scale(1.55)', look=(-36, 30), mouth=1.15)
    d += dd; b += f
    # shield rim highlight from the spotlight
    b += '<path d="M900,400 C1000,270 1170,222 1350,220 C1530,222 1700,270 1800,400" fill="none" stroke="#fff6dc" stroke-width="10" stroke-linecap="round" opacity=".75" transform="translate(0 -6)"/>'
    # ---- the glass case: frame edges + reflections
    b += '<g fill="none" stroke="#d9ecff" stroke-width="8" opacity=".6"><path d="M560,120 L1960,120"/><path d="M560,120 L560,900"/></g>'
    b += '<path d="M560,120 L1960,120 L1960,900 L560,900 Z" fill="url(#bglass)" opacity=".06"/>'
    for (x, w, o) in ((700, 70, .16), (800, 26, .2), (1520, 110, .12), (1660, 30, .18)):
        b += f'<path d="M{x},120 L{x + w},120 L{x + w - 260},900 L{x - 260},900 Z" fill="#ffffff" opacity="{o}"/>'
    # plain label card (no text)
    b += '<rect x="1250" y="912" width="150" height="36" rx="4" fill="#f7f2e6" stroke="#2a1f3a" stroke-width="3"/>'
    b += '<g stroke="#9a8f7f" stroke-width="4" stroke-linecap="round"><path d="M1264,924 L1360,924"/><path d="M1264,936 L1330,936"/></g>'
    # ---- tiny visitors (generic silhouettes) staring up: one adult with a raised phone, one child jumping back
    col = '#0b0816'; rim = '#ffd59a'
    v1 = fig(470, 1040, 230, lean=-6, stride=.05, armf=(.10, -.22), armb=(-.04, .30), armlen=.36, head=.075)
    b += fig_svg(v1, col, glow=rim, gw=6, flt='url(#bb4)')
    b += hand(470 + .10 * 230 + 2, 1040 - .47 * 230 * .96 - .30 * 230 - .22 * 230 - 6, angle=10, size=11, side='R', view='back', pose='fist', skin=col, line=col, creases=False)
    px, py = 470 + .10 * 230 + 8, 1040 - .47 * 230 * .96 - .30 * 230 - .22 * 230 - 30
    b += f'<rect x="{px - 12:.0f}" y="{py - 20:.0f}" width="26" height="42" rx="5" fill="#0b0816" stroke="#ffd59a" stroke-width="2.5" transform="rotate(12 {px:.0f} {py:.0f})"/>'
    b += f'<circle cx="{px:.0f}" cy="{py:.0f}" r="28" fill="#fff8e0" opacity=".55" filter="url(#bb14)"/>'
    v2 = fig(330, 1046, 150, lean=-14, stride=.12, armf=(.20, -.10), armb=(-.22, -.08), armlen=.36, head=.09)
    b += fig_svg(v2, col, glow=rim, gw=5, flt='url(#bb4)')
    # shock marks above the child
    b += '<g fill="none" stroke="#fff3cf" stroke-width="6" stroke-linecap="round"><path d="M310,860 l-12,-34"/><path d="M342,852 l2,-38"/><path d="M372,862 l16,-30"/></g>'
    b += '<ellipse cx="420" cy="1050" rx="200" ry="14" fill="#000" opacity=".4"/>'
    # camera flash sparkle + dust motes in the spotlight
    b += '<circle cx="497" cy="760" r="60" fill="#fffbe8" opacity=".25" filter="url(#bb14)"/>' + spark(497, 760, 26)
    b += '<g fill="#fff3d6">' + ''.join(f'<circle cx="{random.randint(900, 1700)}" cy="{random.randint(80, 520)}" r="{random.choice([2, 3, 4])}" opacity="{random.uniform(.2, .6):.2f}"/>' for _ in range(50)) + '</g>'
    for (x, y, s) in ((960, 180, 20), (1660, 250, 16), (1040, 820, 14)):
        b += spark(x, y, s)
    return d, b


# ============================================================ C: 460 MILLION YEARS LATER  (intuitive: the fish swims out of a phone)
def build_C():
    random.seed(9)
    d = (lin('cw', [(0, '#0b1230'), (.6, '#141a3c'), (1, '#070a1c')])
         + rad('cglow', 1240, 560, 900, [(0, '#5ff0dc', .55), (.4, '#2aa8b8', .2), (1, '#2aa8b8', 0)])
         + lin('cscr', [(0, '#bff6ee'), (.3, '#52c9c3'), (.75, '#1f8a9a'), (1, '#0f5466')])
         + lin('csand', [(0, '#f1d6a0'), (1, '#b58b52')])
         + lin('cbez', [(0, '#3c4256'), (.5, '#151826'), (1, '#2c3144')], x2=1, y2=1)
         + blur('cb4', 4) + blur('cb12', 12) + blur('cb30', 30) + blur('cb70', 70)
         + '<clipPath id="ccl"><rect x="-470" y="-250" width="940" height="500" rx="26"/></clipPath>')
    b = '<rect width="1920" height="1080" fill="url(#cw)"/>'
    b += '<rect width="1920" height="1080" fill="url(#cglow)"/>'
    b += stars(30, 1000, xmin=700, col='#bff6ee', op=.3, sparks=0)
    # the phone: landscape, tilted, glowing screen = window into the Ordovician sea
    ph = 'translate(1350 545) rotate(-9) scale(.93)'
    b += f'<g transform="{ph}">'
    b += '<rect x="-520" y="-290" width="1040" height="580" rx="70" fill="#000" opacity=".5" filter="url(#cb30)" transform="translate(20 40)"/>'
    b += '<rect x="-520" y="-290" width="1040" height="580" rx="70" fill="url(#cbez)" stroke="#8b93b0" stroke-width="5"/>'
    b += '<rect x="-506" y="-276" width="1012" height="552" rx="58" fill="none" stroke="#4b5270" stroke-width="3"/>'
    b += '<g clip-path="url(#ccl)">'
    b += '<rect x="-470" y="-250" width="940" height="500" fill="url(#cscr)"/>'
    # caustic net + light shafts from the surface
    b += '<g fill="none" stroke="#e9fffa" stroke-width="4" opacity=".25">' + ''.join(f'<path d="M{-470 + i * 70},-250 q30,40 -10,80 t20,80"/>' for i in range(15)) + '</g>'
    for (x, w) in ((-300, 80), (-80, 120), (200, 70)):
        b += f'<path d="M{x},-250 L{x + w},-250 L{x + w + 140},250 L{x + 60},250 Z" fill="#ffffff" opacity=".12"/>'
    b += '<path d="M-470,150 C-300,120 -120,140 60,130 C240,120 380,140 470,128 L470,250 L-470,250 Z" fill="url(#csand)"/>'
    b += '<path d="M-470,150 C-300,120 -120,140 60,130 C240,120 380,140 470,128" fill="none" stroke="#fff3cf" stroke-width="3" opacity=".6"/>'
    # straight-shelled nautiloid drifting in the back
    b += '<g transform="translate(150 -120) rotate(-6)" opacity=".85"><path d="M0,-34 L330,-6 L330,6 L0,34 Z" fill="#efe2c2" stroke="#3a3326" stroke-width="4"/>'
    b += ''.join(f'<path d="M{40 + i * 40},{-30 + i * 3} L{40 + i * 40},{30 - i * 3}" stroke="#9a7d52" stroke-width="5"/>' for i in range(7))
    b += '<g stroke="#e2c9a8" stroke-width="6" stroke-linecap="round" fill="none"><path d="M0,-20 q-40,-10 -70,-36"/><path d="M0,-6 q-50,0 -86,-8"/><path d="M0,8 q-50,10 -80,30"/><path d="M0,22 q-36,18 -56,46"/></g></g>'
    # trilobites on the sand
    for (x, y, s) in ((-260, 170, 1), (330, 160, .8)):
        b += (f'<g transform="translate({x} {y}) scale({s})"><ellipse cx="0" cy="0" rx="46" ry="26" fill="#8a7458" stroke="#3a2e22" stroke-width="4"/>'
              f'<path d="M-46,0 C-46,-20 -30,-26 -18,-26 L-18,26 C-30,26 -46,20 -46,0Z" fill="#a38a68" stroke="#3a2e22" stroke-width="3"/>'
              f'<path d="M-14,-10 L40,-10 M-14,10 L40,10" stroke="#3a2e22" stroke-width="3"/>' + ''.join(f'<path d="M{-6 + i * 10},-24 L{-6 + i * 10},24" stroke="#3a2e22" stroke-width="2" opacity=".6"/>' for i in range(5)) + '</g>')
    b += '<g fill="#e9fffa" opacity=".7">' + ''.join(f'<circle cx="{random.randint(-440, 440)}" cy="{random.randint(-230, 100)}" r="{random.choice([3, 4, 6])}"/>' for _ in range(26)) + '</g>'
    b += '</g>'
    b += '<path d="M-470,-250 L-200,-250 L-470,30 Z" fill="#fff" opacity=".08"/>'   # glass glare
    b += '<circle cx="-494" cy="0" r="9" fill="#0a0c14" stroke="#5a6280" stroke-width="2"/>'   # camera dot
    b += '</g>'
    # notification-like hearts and bubbles rising from the phone (shapes only, no text)
    def heart(x, y, s, c):
        return f'<path transform="translate({x} {y}) scale({s})" d="M0,12 C-30,-8 -26,-34 -8,-34 C-2,-34 0,-28 0,-24 C0,-28 2,-34 8,-34 C26,-34 30,-8 0,12Z" fill="{c}" stroke="#2a0a18" stroke-width="3"/>'
    for (x, y, s, c) in ((1660, 190, 1.6, '#ff5c8a'), (1780, 300, 1.1, '#ff7aa0'), (1560, 110, .9, '#ff5c8a'), (1840, 150, .8, '#ffd27a')):
        b += f'<circle cx="{x}" cy="{y - 10}" r="{44 * s:.0f}" fill="#ff8ab0" opacity=".25" filter="url(#cb12)"/>' + heart(x, y, s, c)
    for (x, y, w) in ((1320, 140, 150), (1470, 220, 110)):
        b += f'<rect x="{x}" y="{y}" width="{w}" height="52" rx="26" fill="#f6f8ff" stroke="#1a2040" stroke-width="4"/>' + ''.join(f'<circle cx="{x + 30 + i * 28}" cy="{y + 26}" r="7" fill="#7a86b0"/>' for i in range(3))
    # water splashing out of the screen's left edge
    b += '<ellipse cx="700" cy="660" rx="300" ry="200" fill="#7ff5e2" opacity=".35" filter="url(#cb70)"/>'
    b += '<path d="M800,520 C740,540 690,600 700,660 C720,720 800,760 860,770 C820,720 800,660 830,600 Z" fill="#9ff3e6" opacity=".55"/>'
    for (x, y, r) in ((660, 520, 16), (620, 600, 11), (700, 470, 9), (580, 680, 13), (640, 760, 9), (760, 820, 12), (540, 560, 7), (720, 880, 8)):
        b += f'<circle cx="{x}" cy="{y}" r="{r}" fill="#c9fff4" stroke="#0f5466" stroke-width="3"/><circle cx="{x - r * .3:.0f}" cy="{y - r * .3:.0f}" r="{r * .3:.0f}" fill="#fff"/>'
    # the accurate fish swimming OUT of the screen toward the viewer (tail still inside)
    b += '<ellipse cx="620" cy="760" rx="420" ry="170" fill="#e8fff6" opacity=".25" filter="url(#cb30)"/>'
    dd, f = saca('cf', 'translate(300 770) rotate(-14) scale(.86)', seed=4, detail=1.0, rim='#d6fff4')
    d += dd; b += f
    for (x, y, s) in ((420, 640, 18), (1100, 860, 14), (1500, 860, 0)):
        if s: b += f'<circle cx="{x}" cy="{y}" r="{s * 2}" fill="#e8fff6" opacity=".35" filter="url(#cb4)"/>' + spark(x, y, s)
    return d, b


da, ba = build_A()
open(os.path.join(HERE, 'A.html'), 'w').write(page('#1d2c4a', svg(da, ba), [('<span class="g">NOT</span> OUR', 190, 'w'), ('ANCESTOR', 196, 'w')], outline='#160a10'))
db, bb = build_B()
open(os.path.join(HERE, 'B.html'), 'w').write(page('#1a1438', svg(db, bb), [('WAS IT', 170, 'w'), ('A <span class="g">JOKE?</span>', 240, 'w')], outline='#0a0718'))
dc, bc = build_C()
open(os.path.join(HERE, 'C.html'), 'w').write(page('#0b1230', svg(dc, bc), [('460', 290, 'y'), ('MILLION YEARS', 106, 'w'), ('LATER', 160, 'w')], outline='#050818'))
print('ok')
