# sacabambaspis-meme-fish thumbnails A-C, round 3 (guideline 16-2/16-6; owner picked round-2 concept B "WAS IT A JOKE?" and
# said "develop B"; round 2 kept in round2/, round 1 in round2/round1/). run: python3 make.py
# A  WAS IT A JOKE?            B refined: huge detailed model face (silicone sheen, googly eyes with domes and highlights)
#    behind museum glass under a spotlight; a big back-lit child flings both arms up, an adult raises a phone.
#    Script S02 ("Was the model a joke, or did this little fish actually look like that?"), S03 (googly doll's eyes).
# B  A REAL ANIMAL             split gag: the same giant derpy face rolls its eyes down at a tiny brass-framed card with
#    the accurate fish. Script S01 ("this is a model of a real animal"), S44 ("This is a real animal").
# C  460 MILLION YEARS LATER   viral post: the model face pops out of a phone's social post, hearts rise from the like
#    button. Script S43 ("Four hundred and sixty million years later, its picture is on a phone screen in your hand").
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

from body import arm, shoulders, P, _v
from hands import _capsule


# ------------------------------------------------------------------ round 3: detailed model face (front, cartoon-simple)
BLOB = 'M-330,30 C-338,-150 -190,-240 0,-240 C190,-240 338,-150 330,30 C322,165 190,228 0,228 C-190,228 -322,165 -330,30 Z'


def face3(gid, tr, look_l=(-20, 30), look_r=(-20, 30), mouth=1.1, seed=3, glare=True):
    """Helsinki model face, front view, local centre 0,0 (660 x 468). Silvery foam/silicone glaze with sheen, mould seam,
    googly doll eyes (plastic rim, white disc, loose black pupil, clear dome with highlights), small dark open mouth."""
    rnd = random.Random(seed)
    d = (rg(gid + 'm', [(0, '#ffffff', 1), (.18, '#eef2f2', 1), (.45, '#bcc6ca', 1), (.75, '#808c92', 1), (1, '#3d464b', 1)], cx=.40, cy=.22, r=.85)
         + rg(gid + 'w', [(0, '#ffffff', 1), (.7, '#f4f4f1', 1), (.92, '#d9dbd8', 1), (1, '#a9adad', 1)], cx=.42, cy=.36, r=.62)
         + rg(gid + 'dome', [(0, '#ffffff', 0), (.78, '#ffffff', 0), (.93, '#9fb4c4', .35), (1, '#4a5a66', .55)], cx=.5, cy=.5, r=.5)
         + rg(gid + 'k', [(0, '#5a1c1c', 1), (.55, '#2a0b0d', 1), (1, '#070304', 1)], cx=.5, cy=.18, r=.8)
         + rg(gid + 'p', [(0, '#3a3a3e', 1), (.6, '#0c0c0e', 1), (1, '#000000', 1)], cx=.35, cy=.3, r=.7)
         + f'<clipPath id="{gid}c"><path d="{BLOB}"/></clipPath>'
         + blur(gid + 'b3', 3) + blur(gid + 'b8', 8) + blur(gid + 'b20', 20) + blur(gid + 'b40', 40))
    o = f'<g transform="{tr}">'
    o += f'<path d="{BLOB}" fill="url(#{gid}m)"/>'
    o += f'<g clip-path="url(#{gid}c)">'
    # bounce light from below (cool, from the glass/floor) and warm spotlight wash from above
    o += f'<ellipse cx="40" cy="250" rx="360" ry="110" fill="#8fc3e6" opacity=".35" filter="url(#{gid}b40)"/>'
    o += f'<ellipse cx="-40" cy="-230" rx="300" ry="90" fill="#fff0cc" opacity=".55" filter="url(#{gid}b40)"/>'
    # cheeks: darker turning planes at the sides
    o += f'<ellipse cx="-330" cy="40" rx="90" ry="230" fill="#2c3438" opacity=".35" filter="url(#{gid}b20)"/>'
    o += f'<ellipse cx="335" cy="40" rx="100" ry="240" fill="#232b30" opacity=".45" filter="url(#{gid}b20)"/>'
    # foam / silicone texture: soft mottling + fine orange-peel dots
    for _ in range(140):
        x, y = rnd.uniform(-320, 320), rnd.uniform(-235, 225)
        c = rnd.choice(['#ffffff', '#5a666c', '#c9d2d6'])
        o += f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{rnd.uniform(6, 22):.0f}" ry="{rnd.uniform(4, 14):.0f}" fill="{c}" opacity="{rnd.uniform(.03, .07):.2f}"/>'
    for _ in range(260):
        x, y = rnd.uniform(-320, 320), rnd.uniform(-235, 225)
        o += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{rnd.uniform(1, 2.4):.1f}" fill="{rnd.choice(["#ffffff", "#3c464b"])}" opacity="{rnd.uniform(.12, .3):.2f}"/>'
    # mould seam of the silicone cast, running over the side of the head
    o += '<path d="M250,-170 C300,-90 318,20 296,120 C280,170 250,200 210,214" fill="none" stroke="#ffffff" stroke-width="3" opacity=".45"/>'
    o += '<path d="M256,-168 C306,-88 324,22 302,122 C286,172 256,202 216,216" fill="none" stroke="#38424a" stroke-width="3" opacity=".45"/>'
    # faint edge of the head shield above the mouth, like the real fish's plan
    o += '<path d="M-250,130 C-150,175 150,175 250,130" fill="none" stroke="#56626a" stroke-width="5" opacity=".35"/>'
    # sheen: big soft glaze band, sharp specular streaks, a tiny reflection of the spotlight
    o += f'<path d="M-270,-110 C-210,-200 -90,-226 40,-222 C150,-218 230,-190 280,-140" fill="none" stroke="#ffffff" stroke-width="46" stroke-linecap="round" opacity=".45" filter="url(#{gid}b8)"/>'
    o += '<path d="M-240,-128 C-185,-196 -80,-218 20,-216" fill="none" stroke="#ffffff" stroke-width="11" stroke-linecap="round" opacity=".95"/>'
    o += '<path d="M60,-215 C110,-212 150,-204 180,-194" fill="none" stroke="#ffffff" stroke-width="7" stroke-linecap="round" opacity=".8"/>'
    o += '<path d="M-300,-10 C-306,60 -290,120 -250,160" fill="none" stroke="#ffffff" stroke-width="9" stroke-linecap="round" opacity=".4"/>'
    o += '<g fill="#ffffff" opacity=".9"><rect x="-150" y="-205" width="20" height="13" rx="3"/><rect x="-126" y="-207" width="20" height="13" rx="3"/></g>'
    if glare:   # the glass case reflected as a dim stripe
        o += '<path d="M120,-260 L170,-260 L60,260 L10,260 Z" fill="#ffffff" opacity=".08"/>'
    o += '</g>'
    o += f'<path d="{BLOB}" fill="none" stroke="{LINE}" stroke-width="7"/>'
    # warm rim light on the crown
    o += '<path d="M-300,-90 C-240,-200 -120,-236 0,-237 C120,-236 240,-200 300,-90" fill="none" stroke="#fff3d2" stroke-width="7" stroke-linecap="round" opacity=".9" transform="translate(0 5)"/>'
    # googly eyes
    for sx, look in ((-1, look_l), (1, look_r)):
        ex, ey, R = sx * 110, -64, 98
        o += f'<ellipse cx="{ex + 10}" cy="{ey + 22}" rx="{R + 6}" ry="{R}" fill="#1c2328" opacity=".45" filter="url(#{gid}b8)"/>'
        o += f'<circle cx="{ex}" cy="{ey}" r="{R}" fill="#d4d9da" stroke="{LINE}" stroke-width="6"/>'           # plastic rim
        o += f'<circle cx="{ex}" cy="{ey}" r="{R - 9}" fill="url(#{gid}w)"/>'
        px, py = ex + look[0], ey + look[1]
        o += f'<circle cx="{px + 5:.0f}" cy="{py + 9:.0f}" r="47" fill="#6d7478" opacity=".45" filter="url(#{gid}b3)"/>'   # pupil shadow
        o += f'<circle cx="{px:.0f}" cy="{py:.0f}" r="46" fill="url(#{gid}p)"/>'
        o += f'<circle cx="{px - 15:.0f}" cy="{py - 17:.0f}" r="9" fill="#ffffff" opacity=".55"/>'
        o += f'<circle cx="{ex}" cy="{ey}" r="{R - 9}" fill="url(#{gid}dome)"/>'                                  # clear dome
        o += (f'<path d="M{ex - 64},{ey - 22} A68,68 0 0 1 {ex - 6},{ey - 74}" fill="none" stroke="#ffffff" stroke-width="15" stroke-linecap="round" opacity=".95"/>'
              f'<circle cx="{ex + 30}" cy="{ey - 56}" r="9" fill="#ffffff"/>'
              f'<path d="M{ex + 40},{ey + 62} A72,72 0 0 0 {ex + 70},{ey + 22}" fill="none" stroke="#ffe7b8" stroke-width="8" stroke-linecap="round" opacity=".7"/>'
              '')
        o += f'<circle cx="{ex}" cy="{ey}" r="{R}" fill="none" stroke="#ffffff" stroke-width="2.5" opacity=".6" stroke-dasharray="40 300" transform="rotate(200 {ex} {ey})"/>'
    # mouth: small dark open mouth with a glossy lower lip
    m = mouth
    md = f'M-64,96 C-30,86 30,86 64,96 C44,{96 + 70 * m:.0f} 18,{100 + 92 * m:.0f} 0,{102 + 96 * m:.0f} C-18,{100 + 92 * m:.0f} -44,{96 + 70 * m:.0f} -64,96 Z'
    o += f'<path d="M-72,92 C-30,80 30,80 72,92" fill="none" stroke="#2b3236" stroke-width="12" opacity=".35" stroke-linecap="round"/>'
    o += f'<path d="{md}" fill="url(#{gid}k)" stroke="{LINE}" stroke-width="6.5" stroke-linejoin="round"/>'
    o += f'<path d="M-30,{112 + 20 * m:.0f} C-14,{150 + 30 * m:.0f} 14,{150 + 30 * m:.0f} 30,{112 + 20 * m:.0f}" fill="#7a2a2c" opacity=".55"/>'
    o += '<path d="M-48,98 C-20,92 20,92 48,98" fill="none" stroke="#ffffff" stroke-width="4" opacity=".5" stroke-linecap="round" transform="translate(0 -9)"/>'
    return d, o + '</g>'


def glass_case(gid, x0, y0, x1, y1, seed=2, handprint=None):
    """front glass of a museum case (over the exhibit): metal frame, tint, soft and sharp reflections, a spot glare, dust"""
    rnd = random.Random(seed)
    d = (lin(gid + 'gt', [(0, '#cfeaff'), (1, '#7aa9d4')], x2=1, y2=1)
         + lin(gid + 'fr', [(0, '#3a3550'), (.5, '#8b86a6'), (1, '#2a2640')], x2=0, y2=1)
         + lin(gid + 'st', [(0, '#ffffff'), (1, '#ffffff')], x2=1, y2=0)
         + blur(gid + 'gb6', 6) + blur(gid + 'gb30', 30))
    w, h = x1 - x0, y1 - y0
    o = f'<rect x="{x0}" y="{y0}" width="{w}" height="{h}" fill="url(#{gid}gt)" opacity=".07"/>'
    for (x, ww, op) in ((x0 + 120, 130, .10), (x0 + 270, 34, .16), (x0 + 900, 170, .08), (x0 + 1090, 40, .15)):   # diagonal glare bands
        o += f'<path d="M{x},{y0} L{x + ww},{y0} L{x + ww - 300},{y1} L{x - 300},{y1} Z" fill="#ffffff" opacity="{op}" filter="url(#{gid}gb6)"/>'
    o += f'<path d="M{x0 + 300},{y0} L{x0 + 309},{y0} L{x0 + 9},{y1} L{x0},{y1} Z" fill="#ffffff" opacity=".55"/>'                      # sharp streak
    o += f'<path d="M{x0 + 1130},{y0} L{x0 + 1136},{y0} L{x0 + 836},{y1} L{x0 + 830},{y1} Z" fill="#ffffff" opacity=".45"/>'
    o += f'<ellipse cx="{x0 + 520}" cy="{y0 + 70}" rx="120" ry="40" fill="#fff7e2" opacity=".35" filter="url(#{gid}gb30)"/>'           # spotlight glare
    o += ''.join(f'<circle cx="{rnd.uniform(x0, x1):.0f}" cy="{rnd.uniform(y0, y1):.0f}" r="{rnd.choice([1.5, 2, 2.5])}" fill="#ffffff" opacity="{rnd.uniform(.15, .45):.2f}"/>' for _ in range(60))
    if handprint:   # a child's smudged handprint on the glass
        hx, hy, s = handprint
        o += f'<g opacity=".16" filter="url(#{gid}gb6)">' + hand(hx, hy, -8, s, 'R', 'palm', 'flat', skin='#ffffff', line='#ffffff', creases=False) + '</g>'
        o += f'<g opacity=".12">' + hand(hx, hy, -8, s, 'R', 'palm', 'flat', skin='#ffffff', line='#ffffff', creases=False) + '</g>'
    # frame: top rail + left post with a glass edge highlight (thick glass reads green-cyan on its edge)
    o += f'<rect x="{x0 - 16}" y="{y0 - 22}" width="{w + 40}" height="26" fill="url(#{gid}fr)" stroke="#120f20" stroke-width="4"/>'
    o += f'<rect x="{x0 - 16}" y="{y0 - 22}" width="20" height="{h + 26}" fill="url(#{gid}fr)" stroke="#120f20" stroke-width="4"/>'
    o += f'<path d="M{x0 + 8},{y0 + 6} L{x0 + 8},{y1}" stroke="#bff3e6" stroke-width="5" opacity=".7"/>'
    o += f'<path d="M{x0 + 8},{y0 + 8} L{x1 + 20},{y0 + 8}" stroke="#bff3e6" stroke-width="4" opacity=".55"/>'
    return d, o


def person_back(cx, ground, H, kind, col, rim, arms, step=0, lean=0, hair='short', rimw=7, glowid=None):
    """generic visitor seen FROM BEHIND (no face), cute proportions (body.P), back-lit: dark body with a warm rim.
    arms = [(upper, bend, bend_dir, pose, fingers)] for the viewer-left and viewer-right arm."""
    p = P[kind]; tot = p['height'] * H; top = ground - tot
    hip_y = top + tot * .52; sh_y = top + H + p['neck'] * H
    sw = p['shoulder_w'] * H
    def body(fill, stroke, lw):
        s = f'<g transform="rotate({lean} {cx} {ground})">'
        # legs (capsules), one stepping back
        for k, sx in enumerate((-1, 1)):
            fx = cx + sx * .32 * H + (step * H if k == 0 else 0)
            s += f'<path d="{_capsule(cx + sx * .28 * H, hip_y, fx, ground - .18 * H, .52 * H, .36 * H)}" fill="{fill}" stroke="{stroke}" stroke-width="{lw}"/>'
            s += f'<ellipse cx="{fx + sx * .06 * H:.1f}" cy="{ground - .1 * H:.1f}" rx="{.3 * H:.1f}" ry="{.16 * H:.1f}" fill="{fill}" stroke="{stroke}" stroke-width="{lw}"/>'
        # torso (rounded), skirt-like flare for the child
        flare = .25 * H if kind == 'cute_child' else .05 * H
        s += (f'<path d="M{cx - sw / 2:.1f},{sh_y + .25 * H:.1f} C{cx - sw / 2:.1f},{sh_y - .05 * H:.1f} {cx - sw * .3:.1f},{sh_y - .08 * H:.1f} {cx},{sh_y - .08 * H:.1f} '
              f'C{cx + sw * .3:.1f},{sh_y - .08 * H:.1f} {cx + sw / 2:.1f},{sh_y - .05 * H:.1f} {cx + sw / 2:.1f},{sh_y + .25 * H:.1f} '
              f'L{cx + sw * .42 + flare:.1f},{hip_y + .25 * H:.1f} C{cx + .2 * H:.1f},{hip_y + .34 * H:.1f} {cx - .2 * H:.1f},{hip_y + .34 * H:.1f} {cx - sw * .42 - flare:.1f},{hip_y + .25 * H:.1f} Z" '
              f'fill="{fill}" stroke="{stroke}" stroke-width="{lw}" stroke-linejoin="round"/>')
        # neck + head (back of the head, hair)
        s += f'<rect x="{cx - .17 * H:.1f}" y="{top + H * .8:.1f}" width="{.34 * H:.1f}" height="{.4 * H:.1f}" fill="{fill}" stroke="{stroke}" stroke-width="{lw}"/>'
        s += f'<ellipse cx="{cx}" cy="{top + H * .52:.1f}" rx="{.47 * H:.1f}" ry="{.52 * H:.1f}" fill="{fill}" stroke="{stroke}" stroke-width="{lw}"/>'
        if hair == 'tails':   # two pigtails flying up/out (startled)
            for sx in (-1, 1):
                s += f'<path d="{_capsule(cx + sx * .38 * H, top + .45 * H, cx + sx * .95 * H, top + .05 * H, .3 * H, .2 * H)}" fill="{fill}" stroke="{stroke}" stroke-width="{lw}"/>'
                s += f'<circle cx="{cx + sx * .98 * H:.1f}" cy="{top + .02 * H:.1f}" r="{.17 * H:.1f}" fill="{fill}" stroke="{stroke}" stroke-width="{lw}"/>'
        if hair == 'bun':
            s += f'<circle cx="{cx + .05 * H:.1f}" cy="{top + .02 * H:.1f}" r="{.22 * H:.1f}" fill="{fill}" stroke="{stroke}" stroke-width="{lw}"/>'
        L, R = shoulders(cx, top, H, kind)
        for (sx, sy), (up, bend, bd, pose, fing) in zip((L, R), arms):
            s += arm(sx, sy, H, upper=up, bend=bend, bend_dir=bd, name='v', side='R' if sx < cx else 'L', view='back', pose=pose,
                     sleeve=fill, skin=fill, line=stroke, kind=kind, lw=lw, fingers=fing)
        return s + '</g>'
    o = ''
    if glowid:
        o += f'<g filter="url(#{glowid})" opacity=".8">{body(rim, rim, rimw * 2.4)}</g>'
    o += body(rim, rim, rimw)
    o += body(col, col, 1.5)
    return o, (L if False else None), top


def wrist(sx, sy, H, upper, bend, bd, kind):
    p = P[kind]; ux, uy = _v(upper); E = (sx + ux * p['upper'] * H, sy + uy * p['upper'] * H)
    fx, fy = _v(upper + bend * (1 if bd >= 0 else -1)); return (E[0] + fx * p['fore'] * H, E[1] + fy * p['fore'] * H)


def spotlight(gid, x, top_w, x_bot0, x_bot1, y_bot, op=.12):
    d = lin(gid + 'cone', [(0, '#fff3d6'), (1, '#fff3d6')]) + blur(gid + 'cb', 30) + lin(gid + 'cf', [(0, '#fff6dc'), (1, '#fff6dc')])
    o = f'<path d="M{x - top_w},0 L{x + top_w},0 L{x_bot1},{y_bot} L{x_bot0},{y_bot} Z" fill="#ffeac0" opacity="{op}" filter="url(#{gid}cb)"/>'
    o += f'<path d="M{x - top_w * .5},0 L{x + top_w * .5},0 L{(x_bot1 + x) / 2 + 80},{y_bot} L{(x_bot0 + x) / 2 - 80},{y_bot} Z" fill="#fff5dc" opacity="{op * .8}" filter="url(#{gid}cb)"/>'
    # the lamp itself, cut by the top edge
    o += f'<path d="M{x - 70},-10 L{x + 70},-10 L{x + 52},34 L{x - 52},34 Z" fill="#1c1830" stroke="#0a0814" stroke-width="4"/>'
    o += f'<ellipse cx="{x}" cy="36" rx="54" ry="11" fill="#fffaf0"/><ellipse cx="{x}" cy="40" rx="120" ry="40" fill="#fff3d0" opacity=".5" filter="url(#{gid}cb)"/>'
    return d, o


def hall(gid, seed=1, col='#1a1438'):
    """dim museum hall behind: far display cases with faint glows, a dark floor with a soft sheen"""
    rnd = random.Random(seed)
    d = lin(gid + 'hw', [(0, '#1b1538'), (.55, '#2a2050'), (1, '#140f28')]) + lin(gid + 'hf', [(0, '#2d2346'), (1, '#0b0817')]) + blur(gid + 'hb', 10)
    o = f'<rect width="1920" height="1080" fill="url(#{gid}hw)"/>'
    o += f'<g filter="url(#{gid}hb)">'
    for (x, y, w, h, c) in ((60, 470, 210, 300, '#4d6fa6'), (300, 520, 150, 240, '#7a5aa6'), (-40, 560, 120, 220, '#5a7fb0')):
        o += f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="#241c44" stroke="#3c3466" stroke-width="6"/>'
        o += f'<rect x="{x + 14}" y="{y + 14}" width="{w - 28}" height="{h - 60}" fill="{c}" opacity=".35"/>'
        o += f'<ellipse cx="{x + w / 2}" cy="{y + h * .45}" rx="{w * .3}" ry="{h * .18}" fill="#cfe2ff" opacity=".18"/>'
    o += '</g>'
    o += f'<rect y="930" width="1920" height="150" fill="url(#{gid}hf)"/>'
    return d, o


# ============================================================ A: WAS IT A JOKE?  (B refined: face behind glass + shocked child)
def build_A():
    random.seed(5)
    d, b = hall('ah')
    d += (rad('aspot', 1300, 360, 900, [(0, '#fff2cf', .75), (.35, '#f6c98a', .28), (1, '#f6c98a', 0)])
          + lin('aplinth', [(0, '#efe6d6'), (1, '#9c8f7c')]) + blur('ab4', 4) + blur('ab10', 10) + blur('ab30', 30) + blur('ab80', 80)
          + lin('acase', [(0, '#2a2048'), (1, '#1a1432')]))
    b += '<rect x="610" y="100" width="1360" height="810" fill="url(#acase)"/>'          # case interior back wall
    b += '<rect width="1920" height="1080" fill="url(#aspot)"/>'
    dd, s = spotlight('al', 1330, 150, 560, 2100, 980, op=.13); d += dd; b += s
    b += '<rect x="590" y="900" width="1380" height="66" fill="url(#aplinth)" stroke="#2a1f3a" stroke-width="4"/>'
    b += '<rect x="590" y="964" width="1380" height="16" fill="#000" opacity=".35"/>'
    b += '<ellipse cx="1330" cy="905" rx="560" ry="34" fill="#000" opacity=".35" filter="url(#ab10)"/>'
    # the model: body going back on the right, then the huge face
    b += '<ellipse cx="1320" cy="520" rx="660" ry="470" fill="#fff0c8" opacity=".30" filter="url(#ab80)"/>'
    b += '<path d="M1800,470 C1870,480 1920,540 1960,600 L1960,880 L1760,890 Z" fill="#76828a" stroke="#1b2022" stroke-width="6"/>'
    b += '<path d="M1820,500 C1850,510 1910,560 1950,610" fill="none" stroke="#ffffff" stroke-width="8" opacity=".4" stroke-linecap="round"/>'
    dd, f = face3('am', 'translate(1400 552) scale(1.54)', look_l=(-26, 34), look_r=(-34, 30), mouth=1.15, seed=3)
    d += dd; b += f
    # glass front + a child's handprint
    dd, g = glass_case('ag', 610, 110, 1960, 902, handprint=(760, 780, 40)); d += dd; b += g
    # dust in the beam + sparkles
    b += '<g fill="#fff3d6">' + ''.join(f'<circle cx="{random.randint(1000, 1700)}" cy="{random.randint(60, 300)}" r="{random.choice([2, 3, 4])}" opacity="{random.uniform(.25, .65):.2f}"/>' for _ in range(40)) + '</g>'
    for (x, y, s) in ((1000, 150, 22), (1720, 170, 18)):
        b += spark(x, y, s)
    # ---- visitors, seen from behind, back-lit by the case
    col, rim = '#0c0918', '#ffcf8a'
    b += '<ellipse cx="560" cy="1066" rx="420" ry="26" fill="#000" opacity=".45" filter="url(#ab10)"/>'
    # adult raising a phone (further back, smaller)
    H2, k2, g2, x2 = 60, 'cute', 1000, 760
    up2 = ((-12, 10, 1, 'flat', False), (168, 8, 1, 'flat', False))
    s2, _, top2 = person_back(x2, g2, H2, k2, col, rim, up2, hair='bun', rimw=6, glowid='ab4')
    b += s2
    L2, R2 = shoulders(x2, top2, H2, k2)
    wx, wy = wrist(R2[0], R2[1], H2, 168, 8, 1, k2)
    # phone: screen faces us (the visitor looks at it), showing the face; a glow around it
    b += f'<circle cx="{wx:.0f}" cy="{wy - 46:.0f}" r="80" fill="#fff6dc" opacity=".45" filter="url(#ab30)"/>'
    b += f'<g transform="translate({wx:.0f} {wy - 44:.0f}) rotate(6)"><rect x="-30" y="-48" width="60" height="96" rx="9" fill="#0c0918" stroke="#ffd9a0" stroke-width="3"/>'
    b += '<rect x="-25" y="-42" width="50" height="84" rx="5" fill="#cfe4f2"/><ellipse cx="0" cy="2" rx="21" ry="16" fill="#aab6bc" stroke="#1b2022" stroke-width="2"/>'
    b += '<circle cx="-7" cy="-3" r="6" fill="#fff" stroke="#1b2022" stroke-width="1.5"/><circle cx="7" cy="-3" r="6" fill="#fff" stroke="#1b2022" stroke-width="1.5"/>'
    b += '<circle cx="-8" cy="-1" r="2.6" fill="#000"/><circle cx="6" cy="-1" r="2.6" fill="#000"/><path d="M-4,7 L4,7 L0,13Z" fill="#2a0b0d"/></g>'
    b += f'<circle cx="{wx:.0f}" cy="{wy + 2:.0f}" r="{.2 * H2:.0f}" fill="{col}"/>'
    # the shocked child in front: arms flung up, pigtails flying, stepping back
    H1, k1, x1, g1 = 92, 'cute_child', 430, 1072
    up1 = ((-142, 30, 1, 'open', True), (142, 30, -1, 'open', True))
    s1, _, top1 = person_back(x1, g1, H1, k1, col, rim, up1, step=-.25, lean=-5, hair='tails', rimw=8, glowid='ab4')
    b += s1
    # shock marks around the child's head
    hx, hy = x1 - 10, top1 + 30
    b += '<g fill="none" stroke="#fff3cf" stroke-width="9" stroke-linecap="round">'
    for a in (-60, -30, 0, 30, 60):
        r0, r1 = 120, 165
        ax, ay = math.sin(math.radians(a)), -math.cos(math.radians(a))
        b += f'<path d="M{hx + ax * r0:.0f},{hy + ay * r0:.0f} L{hx + ax * r1:.0f},{hy + ay * r1:.0f}"/>'
    b += '</g>'
    return d, b


# ============================================================ B: A REAL ANIMAL  (split gag: huge model face vs tiny accurate fish card)
def build_B():
    random.seed(7)
    d, b = hall('bh', seed=3)
    d += (rad('bspot', 1300, 330, 900, [(0, '#fff2cf', .7), (.35, '#f6c98a', .25), (1, '#f6c98a', 0)])
          + rad('bcardspot', 520, 780, 330, [(0, '#fff7e0', .7), (.5, '#ffe6b0', .25), (1, '#ffe6b0', 0)])
          + lin('bplinth', [(0, '#efe6d6'), (1, '#9c8f7c')]) + lin('bcase', [(0, '#2a2048'), (1, '#1a1432')])
          + lin('bcard', [(0, '#fbf3df'), (1, '#e6d6b2')]) + lin('bbrass', [(0, '#f7d98a'), (.5, '#b58a3a'), (1, '#6e4f1c')], x2=1, y2=1)
          + lin('bsea', [(0, '#bfe9e2'), (1, '#6fb7b0')]) + lin('bsand', [(0, '#efd6a2'), (1, '#c49d62')])
          + blur('bb6', 6) + blur('bb10', 10) + blur('bb30', 30) + blur('bb80', 80))
    b += '<rect x="700" y="90" width="1300" height="820" fill="url(#bcase)"/>'
    b += '<rect width="1920" height="1080" fill="url(#bspot)"/>'
    dd, s = spotlight('bl', 1320, 150, 620, 2100, 980, op=.12); d += dd; b += s
    b += '<rect x="680" y="900" width="1290" height="66" fill="url(#bplinth)" stroke="#2a1f3a" stroke-width="4"/>'
    b += '<rect x="680" y="964" width="1290" height="16" fill="#000" opacity=".35"/>'
    b += '<ellipse cx="1320" cy="560" rx="660" ry="460" fill="#fff0c8" opacity=".28" filter="url(#bb80)"/>'
    b += '<path d="M1740,470 C1850,480 1920,540 1960,600 L1960,880 L1700,890 Z" fill="#76828a" stroke="#1b2022" stroke-width="6"/>'
    # the face, bigger, eyes rolled down-left toward the little card
    dd, f = face3('bm', 'translate(1405 556) scale(1.63)', look_l=(-40, 28), look_r=(-44, 34), mouth=1.25, seed=8)
    d += dd; b += f
    dd, g = glass_case('bg', 700, 100, 1960, 902, seed=4); d += dd; b += g
    # ---- the tiny 'real fish' card on a brass stand, in its own small spotlight
    b += '<rect width="1920" height="1080" fill="url(#bcardspot)"/>'
    b += '<ellipse cx="520" cy="1040" rx="230" ry="22" fill="#000" opacity=".5" filter="url(#bb10)"/>'
    b += '<path d="M505,900 L535,900 L545,1030 L495,1030 Z" fill="url(#bbrass)" stroke="#3a2a10" stroke-width="4"/>'
    b += '<ellipse cx="520" cy="1032" rx="80" ry="16" fill="url(#bbrass)" stroke="#3a2a10" stroke-width="4"/>'
    cx0, cy0, cw, ch = 520, 770, 460, 300
    b += f'<g transform="rotate(-4 {cx0} {cy0})">'
    b += f'<rect x="{cx0 - cw / 2 + 8}" y="{cy0 - ch / 2 + 14}" width="{cw}" height="{ch}" rx="10" fill="#000" opacity=".45" filter="url(#bb10)"/>'
    b += f'<rect x="{cx0 - cw / 2 - 12}" y="{cy0 - ch / 2 - 12}" width="{cw + 24}" height="{ch + 24}" rx="12" fill="url(#bbrass)" stroke="#3a2a10" stroke-width="4"/>'
    b += f'<rect x="{cx0 - cw / 2}" y="{cy0 - ch / 2}" width="{cw}" height="{ch}" rx="6" fill="url(#bcard)" stroke="#5a4a2a" stroke-width="3"/>'
    # picture window: shallow sea with the accurate fish
    px0, py0, pw, ph = cx0 - cw / 2 + 20, cy0 - ch / 2 + 20, cw - 40, 196
    b += f'<clipPath id="bpic"><rect x="{px0}" y="{py0}" width="{pw}" height="{ph}" rx="4"/></clipPath>'
    b += f'<g clip-path="url(#bpic)"><rect x="{px0}" y="{py0}" width="{pw}" height="{ph}" fill="url(#bsea)"/>'
    b += f'<path d="M{px0},{py0 + 160} C{px0 + 120},{py0 + 150} {px0 + 280},{py0 + 166} {px0 + pw},{py0 + 152} L{px0 + pw},{py0 + ph} L{px0},{py0 + ph} Z" fill="url(#bsand)"/>'
    b += ''.join(f'<path d="M{px0 + 30 + i * 60},{py0} L{px0 + 60 + i * 60},{py0} L{px0 + 100 + i * 60},{py0 + 160} L{px0 + 70 + i * 60},{py0 + 160} Z" fill="#fff" opacity=".12"/>' for i in range(7))
    b += '</g>'
    dd, fs = saca('bf', f'translate({px0 + pw - 30} {py0 + 106}) scale(-.36 .36)', seed=6, detail=.8, rim='#fffbe8')
    d += dd; b += fs
    b += f'<rect x="{px0}" y="{py0}" width="{pw}" height="{ph}" rx="4" fill="none" stroke="#5a4a2a" stroke-width="3"/>'
    # text-free label lines
    b += f'<g stroke="#8a7a5c" stroke-width="9" stroke-linecap="round"><path d="M{px0 + 6},{py0 + ph + 30} L{px0 + 250},{py0 + ph + 30}"/><path d="M{px0 + 6},{py0 + ph + 56} L{px0 + 330},{py0 + ph + 56}"/></g>'
    b += '</g>'
    b += f'<circle cx="{cx0 + 190}" cy="{cy0 - 175}" r="40" fill="#fff6dc" opacity=".4" filter="url(#bb30)"/>' + spark(cx0 + 200, cy0 - 170, 24)
    # dust + sparkles
    b += '<g fill="#fff3d6">' + ''.join(f'<circle cx="{random.randint(1000, 1700)}" cy="{random.randint(60, 260)}" r="{random.choice([2, 3, 4])}" opacity="{random.uniform(.25, .65):.2f}"/>' for _ in range(36)) + '</g>'
    b += spark(1060, 140, 20) + spark(1730, 200, 16)
    return d, b


# ============================================================ C: 460 MILLION YEARS LATER  (viral post: the face pops out of a phone)
def heart(x, y, s, c, sw=3, rot=0):
    return f'<path transform="translate({x} {y}) rotate({rot}) scale({s})" d="M0,14 C-34,-8 -30,-38 -9,-38 C-3,-38 0,-31 0,-27 C0,-31 3,-38 9,-38 C30,-38 34,-8 0,14Z" fill="{c}" stroke="#3a0a1e" stroke-width="{sw}" stroke-linejoin="round"/>'


def build_C():
    random.seed(11)
    d = (lin('cw', [(0, '#2a1146'), (.55, '#3b1758'), (1, '#160a2a')])
         + rad('cglow', 1270, 480, 900, [(0, '#ff8fc8', .55), (.35, '#b04cc8', .25), (1, '#b04cc8', 0)])
         + lin('cbez', [(0, '#4a4e66'), (.5, '#16182a'), (1, '#33384e')], x2=1, y2=1)
         + lin('cscr', [(0, '#fbfbff'), (1, '#eef0f8')])
         + lin('cphoto', [(0, '#2b2050'), (1, '#120d26')])
         + rad('cpspot', 0, -360, 460, [(0, '#fff2cf', .85), (.4, '#f6c98a', .3), (1, '#f6c98a', 0)])
         + lin('cplinth', [(0, '#efe6d6'), (1, '#9c8f7c')])
         + blur('cb4', 4) + blur('cb10', 10) + blur('cb24', 24) + blur('cb60', 60)
         + '<clipPath id="cpop"><rect x="-290" y="-350" width="580" height="410"/><rect x="-700" y="-1000" width="1400" height="670"/></clipPath>'
         + '<clipPath id="cphc"><rect x="-290" y="-340" width="580" height="400"/></clipPath>')
    b = '<rect width="1920" height="1080" fill="url(#cw)"/>'
    b += '<rect width="1920" height="1080" fill="url(#cglow)"/>'
    for _ in range(26):   # bokeh
        x, y, r = random.randint(700, 1900), random.randint(40, 1000), random.randint(14, 46)
        b += f'<circle cx="{x}" cy="{y}" r="{r}" fill="{random.choice(["#ff9ad0", "#c7a0ff", "#ffd48a"])}" opacity="{random.uniform(.08, .2):.2f}" filter="url(#cb4)"/>'
    b += '<g transform="translate(1290 700) rotate(4) scale(1.18)">'
    b += '<rect x="-310" y="-500" width="620" height="1000" rx="70" fill="#000" opacity=".55" filter="url(#cb24)" transform="translate(26 36)"/>'
    b += '<rect x="-310" y="-500" width="620" height="1000" rx="70" fill="url(#cbez)" stroke="#a6abc8" stroke-width="5"/>'
    b += '<rect x="-290" y="-480" width="580" height="960" rx="54" fill="url(#cscr)"/>'
    b += '<rect x="-60" y="-470" width="120" height="28" rx="14" fill="#0c0d16"/>'
    # post header: avatar (a tiny googly face) + name bars + menu dots
    b += '<circle cx="-236" cy="-392" r="28" fill="#b9c6cc" stroke="#22283a" stroke-width="3"/><circle cx="-244" cy="-396" r="7" fill="#fff" stroke="#22283a" stroke-width="2"/><circle cx="-228" cy="-396" r="7" fill="#fff" stroke="#22283a" stroke-width="2"/>'
    b += '<rect x="-194" y="-406" width="170" height="14" rx="7" fill="#3a3f55"/><rect x="-194" y="-384" width="110" height="11" rx="6" fill="#a9aec4"/>'
    b += '<g fill="#3a3f55"><circle cx="220" cy="-392" r="6"/><circle cx="238" cy="-392" r="6"/><circle cx="256" cy="-392" r="6"/></g>'
    # the photo: a museum case under a spotlight
    b += '<g clip-path="url(#cphc)"><rect x="-290" y="-340" width="580" height="400" fill="url(#cphoto)"/><rect x="-290" y="-340" width="580" height="400" fill="url(#cpspot)"/>'
    b += '<rect x="-290" y="-92" width="580" height="160" fill="url(#cplinth)"/><rect x="-290" y="-92" width="580" height="8" fill="#fff" opacity=".5"/><ellipse cx="0" cy="-88" rx="250" ry="18" fill="#000" opacity=".35"/>'
    b += '<rect x="-50" y="-40" width="100" height="30" rx="3" fill="#f7f2e6" stroke="#2a1f3a" stroke-width="2"/>'
    b += ''.join(f'<path d="M{x},-340 L{x + w},-340 L{x + w - 130},60 L{x - 130},60 Z" fill="#fff" opacity=".1"/>' for x, w in ((-160, 50), (150, 70)))
    b += '</g>'
    # the face pops out of the photo: bottom inside the frame, crown breaking out over the header
    b += '<ellipse cx="0" cy="-300" rx="400" ry="250" fill="#fff0c8" opacity=".35" filter="url(#cb60)"/>'
    b += '<path d="M-290,-340 L290,-340" stroke="#22283a" stroke-width="4"/>'
    b += '<g clip-path="url(#cpop)">'
    dd, f = face3('cm', 'translate(0 -296) scale(.87)', look_l=(-8, 30), look_r=(12, 24), mouth=1.15, seed=12, glare=False)
    d += dd; b += f
    b += '</g>'
    b += '<path d="M-290,60 L290,60" fill="none" stroke="#22283a" stroke-width="4"/>'
    # action row: a big filled heart, comment, share, bookmark; then text-free caption bars
    b += '<circle cx="-226" cy="124" r="60" fill="#ff5c8a" opacity=".5" filter="url(#cb10)"/>' + heart(-226, 136, 1.35, '#ff3d74', 4)
    b += '<path d="M-150,102 h56 a14,14 0 0 1 14,14 v24 a14,14 0 0 1 -14,14 h-30 l-16,14 v-14 h-10 a14,14 0 0 1 -14,-14 v-24 a14,14 0 0 1 14,-14Z" fill="none" stroke="#22283a" stroke-width="7" stroke-linejoin="round"/>'
    b += '<path d="M-30,138 L30,108 L18,168 L0,144 Z" fill="none" stroke="#22283a" stroke-width="7" stroke-linejoin="round"/>'
    b += '<path d="M226,100 h36 v60 l-18,-14 l-18,14 Z" fill="none" stroke="#22283a" stroke-width="7" stroke-linejoin="round"/>'
    b += '<g fill="#3a3f55"><rect x="-266" y="200" width="250" height="16" rx="8"/></g><g fill="#b4b8cc"><rect x="-266" y="236" width="470" height="13" rx="6"/><rect x="-266" y="262" width="380" height="13" rx="6"/><rect x="-266" y="288" width="430" height="13" rx="6"/></g>'
    b += '<g fill="#d9dcea"><rect x="-266" y="340" width="532" height="120" rx="14"/></g>'
    b += '<path d="M-290,-480 L-60,-480 L-290,-100 Z" fill="#fff" opacity=".05"/>'
    b += '</g>'
    # hearts: a stream rising out of the like button, curling up the right side of the phone
    hs = [(930, 900, .9), (850, 800, .7), (900, 700, 1.1), (790, 650, .6), (760, 920, .8), (700, 760, .9), (640, 860, .6),
          (1700, 560, 1.4), (1790, 430, 1.0), (1680, 330, 1.2), (1800, 220, 1.5), (1640, 130, .8), (1870, 640, .8), (1780, 760, .7)]
    cols = ['#ff3d74', '#ff5c8a', '#ff7aa0', '#ffb04d']
    for i, (x, y, s) in enumerate(hs):
        c = cols[i % 4]
        b += f'<circle cx="{x}" cy="{y - 12 * s:.0f}" r="{52 * s:.0f}" fill="{c}" opacity=".35" filter="url(#cb10)"/>' + heart(x, y, s * 1.3, c, 4, rot=random.randint(-18, 18))
        b += f'<path d="M{x - 14 * s:.0f},{y - 34 * s:.0f} q8,-8 18,-6" fill="none" stroke="#fff" stroke-width="{5 * s:.1f}" stroke-linecap="round" opacity=".7" transform="rotate({random.randint(-10, 10)} {x} {y})"/>'
    for (x, y, s) in ((1500, 90, 22), (1880, 420, 18), (1000, 120, 16), (960, 760, 14)):
        b += spark(x, y, s)
    return d, b

da, ba = build_A()
open(os.path.join(HERE, 'A.html'), 'w').write(page('#1a1438', svg(da, ba), [('WAS IT', 160, 'w'), ('A <span class="g">JOKE?</span>', 216, 'w')], outline='#0a0718'))
db, bb = build_B()
open(os.path.join(HERE, 'B.html'), 'w').write(page('#1a1438', svg(db, bb), [('A <span class="g">REAL</span>', 200, 'w'), ('ANIMAL', 200, 'w')], outline='#0a0718'))
dc, bc = build_C()
open(os.path.join(HERE, 'C.html'), 'w').write(page('#2a1146', svg(dc, bc), [('460', 290, 'y'), ('MILLION YEARS', 100, 'w'), ('LATER', 160, 'w')], outline='#12061e'))
