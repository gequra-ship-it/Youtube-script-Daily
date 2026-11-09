# Shorts thumbnails (guideline 16-9 style B, brief tools/briefs/thumb_art.md) for pluto-not-a-planet-short1..5, one A.html each.
# Run: python3 videos/pluto-not-a-planet-short1/thumb/make_all.py [1 2 3 4 5]  -> videos/pluto-not-a-planet-shortN/thumb/A.html
# 1 ONE SPECK JUMPED   blink comparator: two backlit glass plates, same stars, one speck jumps. short1 S03-S05.
# 2 THE MOON IS BIGGER Moon vs Pluto side by side, 3,474 km vs 2,376 km. short2 S01-S02.
# 3 A COSMIC REBEL     tilted oval orbit cutting inside Neptune's circle. short3 S02, S05 ("like a cosmic rebel").
# 4 PLUTO GOT VOTED OUT Prague hall, Pluto in the spotlight, raised voting cards. short4 S04-S06.
# 5 PLUTO HAS A HEART  heart-shaped nitrogen basin, blue haze, New Horizons fly-by. short5 S02-S05.
import os, sys, math, random, shutil
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
sys.path.insert(0, REPO + '/tools')
from thumb_lib import lin, rad, spark, vpage, vsvg, fireflies, halo, darkband

W, H = 1080, 1920
INK = '#1d2b1c'; GREEN = '#6aa55a'; DARKG = '#4d8a4a'; BELLY = '#9cc98a'
FILTERS = ''.join(f'<filter id="b{n}" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="{n}"/></filter>' for n in (2, 3, 6, 12, 24, 50))
VIG = rad('vig', 540, 960, 1250, [(0, '#000', 0), (.55, '#000', 0), (1, '#000', .7)])


# ---------------- mascot frog (tools/assets/frog.svg body), posable ----------------
def limb(d, w=7.5, wi=3.4):
    return f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="{w}"/><path d="{d}" fill="none" stroke="{GREEN}" stroke-width="{wi}"/>'


def end_of(d):
    n = [float(v) for v in d.replace('M', ' ').replace('q', ' ').split()]
    return n[0] + n[-2], n[1] + n[-1]


def frog(x, y, s, rot=0, flip=False, look=(0, 0), mouth='O', armL=None, armR=None, legs=None, helmet=False,
         back='', front='', mid='', hat=''):
    lx, ly = look; m = math.hypot(lx + 1, ly)
    if m > 6.4: lx, ly = (lx + 1) * 6.4 / m - 1, ly * 6.4 / m          # pupil stays inside the white (guideline 16-9)
    sx = -s if flip else s
    g = [f'<g transform="translate({x} {y}) rotate({rot}) scale({sx} {s})" stroke="{INK}" stroke-linejoin="round" stroke-linecap="round">', back]
    if helmet:
        g.append('<rect x="-50" y="-58" width="20" height="42" rx="7" fill="#d9dde6" stroke-width="3"/><rect x="-46" y="-52" width="5" height="30" rx="2" fill="#fff" stroke="none" opacity=".7"/>')
    for hx, hy, fx, fy, fa in (legs or ((-20, -6, -22, 4, 0), (20, -6, 22, 4, 0))):
        if abs(fx - hx) + abs(fy - hy) > 14:
            g.append(limb(f'M{hx} {hy} L{fx} {fy}', 15, 9))
        g.append(f'<ellipse cx="{fx}" cy="{fy}" rx="16" ry="9" transform="rotate({fa} {fx} {fy})" fill="{DARKG}" stroke-width="3.2"/>')
    g.append(f'<path d="M-34 0 q-6 -64 34 -70 q40 -2 42 62 q0 10 -6 12 q-36 6 -70 -4z" fill="{GREEN}" stroke-width="4"/>')
    g.append(f'<ellipse cx="2" cy="-12" rx="22" ry="20" fill="{BELLY}" stroke="none" opacity=".7"/>')
    g.append('<path d="M-24 -50 q6 -14 18 -16" fill="none" stroke="#b6dea0" stroke-width="3" opacity=".8"/>')
    for ex in (-10, 22):
        g.append(f'<circle cx="{ex}" cy="-66" r="13.5" fill="#f4f5ea" stroke-width="3.2"/>')
        g.append(f'<circle cx="{ex + 1 + lx:.1f}" cy="{-66 + ly:.1f}" r="4.4" fill="{INK}" stroke="none"/>')
        g.append(f'<circle cx="{ex + 2.4 + lx:.1f}" cy="{-67.6 + ly:.1f}" r="1.5" fill="#fff" stroke="none"/>')
    g.append('<path d="M-22 -88 q12 -9 24 -1 M10 -89 q12 -8 24 1" fill="none" stroke-width="3.4"/>')
    if mouth == 'O':
        g.append('<ellipse cx="6" cy="-38" rx="10" ry="12" fill="#7a2f33" stroke-width="3"/><ellipse cx="6" cy="-31" rx="6" ry="4" fill="#e07b7b" stroke="none"/>')
    elif mouth == 'o':
        g.append('<ellipse cx="6" cy="-41" rx="6" ry="7.5" fill="#7a2f33" stroke-width="3"/>')
    g.append('<ellipse cx="-18" cy="-48" rx="5" ry="3" fill="#e98a8a" stroke="none" opacity=".55"/><ellipse cx="30" cy="-48" rx="5" ry="3" fill="#e98a8a" stroke="none" opacity=".55"/>')
    g.append(hat)
    if helmet:
        g.append('<circle cx="6" cy="-56" r="47" fill="#cfeaff" fill-opacity=".13" stroke="#eef6ff" stroke-width="4.5"/>')
        g.append('<path d="M-28 -80 q12 -18 32 -21" fill="none" stroke="#fff" stroke-width="5" opacity=".8"/>')
        g.append('<ellipse cx="6" cy="-12" rx="42" ry="9" fill="#e6eaf2" stroke-width="3.2"/>')
    g.append(mid)
    for a in (armL or 'M-34 -22 q-14 6 -16 22', armR or 'M38 -22 q14 6 16 22'):
        g.append(limb(a)); ex_, ey_ = end_of(a)
        g.append(f'<circle cx="{ex_:.1f}" cy="{ey_:.1f}" r="5.6" fill="{GREEN}" stroke-width="3"/>')
    g.append(front); g.append('</g>')
    return ''.join(g)


def starfield(rnd, n, y0, y1, col='#eaf2ff', big=False):
    o = ''
    for _ in range(n):
        o += f'<circle cx="{rnd.uniform(0, W):.0f}" cy="{rnd.uniform(y0, y1):.0f}" r="{rnd.choice([1.1, 1.6, 2.2] + ([3] if big else []))}" fill="{col}" opacity="{rnd.uniform(.25, .9):.2f}"/>'
    return o


def out(n, bg, defs, body, lines, outline='#05070f', top=870):
    d = f'{ROOT}/pluto-not-a-planet-short{n}/thumb'; os.makedirs(d, exist_ok=True)
    for f in ('common.css', 'Fredoka-700.woff2'):
        shutil.copy(f'{REPO}/tools/assets/thumb_v/{f}', d)
    open(f'{d}/A.html', 'w').write(vpage(bg, vsvg(FILTERS + VIG + defs, body + f'<rect width="{W}" height="{H}" fill="url(#vig)"/>'), lines, outline=outline, top=top))


ROOT = REPO + '/videos'


# ============ 1. blink comparator: the speck that jumped ============
def make_1():
    rnd = random.Random(11)
    d = lin('room1', [(0, '#0a1024'), (.5, '#0b0f1e'), (1, '#120c0c')])
    d += lin('plate1', [(0, '#16304a'), (1, '#0a1a2c')])
    d += lin('brass1', [(0, '#6a4a1c'), (.45, '#e6c071'), (1, '#7a5420')], x2=1, y2=0)
    d += lin('wood1', [(0, '#4a2a16'), (1, '#24140a')])
    d += halo('h1', 540, 520, 560, inner='#dff6ff', outer='#5fc8ff')
    d += rad('lamp1', 300, 1560, 420, [(0, '#ffd890', .5), (1, '#ffd890', 0)])
    b = f'<rect width="{W}" height="{H}" fill="url(#room1)"/>'
    # dome slit with the night sky
    b += '<path d="M380 0 L700 0 L660 300 L420 300Z" fill="#0d1838"/>'
    b += '<g clip-path="url(#slit1)">' + starfield(rnd, 70, 0, 300, big=True) + '</g>'
    d += '<clipPath id="slit1"><path d="M380 0 L700 0 L660 300 L420 300Z"/></clipPath>'
    b += '<path d="M380 0 L420 300 M700 0 L660 300" stroke="#2a3048" stroke-width="10"/>'
    b += f'<ellipse cx="540" cy="540" rx="620" ry="520" fill="url(#h1)" opacity=".55"/>'
    # stand
    b += '<path d="M60 800 L1020 800 L1060 860 L20 860Z" fill="url(#wood1)" stroke="#120a04" stroke-width="5"/>'
    b += '<rect x="20" y="860" width="1040" height="26" fill="#1c1008"/>'
    # eyepiece housing and tube
    b += '<rect x="430" y="262" width="220" height="70" rx="14" fill="url(#brass1)" stroke="#2a1a08" stroke-width="5"/>'
    b += '<rect x="500" y="130" width="80" height="140" rx="10" fill="url(#brass1)" stroke="#2a1a08" stroke-width="5"/>'
    b += '<rect x="480" y="100" width="120" height="44" rx="12" fill="#1c140c" stroke="#2a1a08" stroke-width="5"/><ellipse cx="540" cy="104" rx="46" ry="10" fill="#0a0a0a"/>'
    for yy in (180, 220):
        b += f'<rect x="496" y="{yy}" width="88" height="10" fill="#8a6428" stroke="#2a1a08" stroke-width="3"/>'
    # two backlit plates
    stars_rel = [(rnd.uniform(.06, .94), rnd.uniform(.06, .94), rnd.choice([2, 2.5, 3.2, 4.2])) for _ in range(85)]
    spk = {0: (.50, .52), 1: (.62, .45)}
    for k, (x0, y0) in enumerate(((70, 340), (570, 340))):
        pw, ph = 440, 420
        b += f'<rect x="{x0 - 26}" y="{y0 - 26}" width="{pw + 52}" height="{ph + 52}" rx="12" fill="#bfe8ff" opacity=".45" filter="url(#b24)"/>'
        b += f'<rect x="{x0}" y="{y0}" width="{pw}" height="{ph}" fill="url(#plate1)"/>'
        b += f'<rect x="{x0}" y="{y0}" width="{pw}" height="{ph}" fill="#8fd8ff" opacity=".12"/>'
        for sx, sy, r in stars_rel:
            b += f'<circle cx="{x0 + sx * pw:.0f}" cy="{y0 + sy * ph:.0f}" r="{r}" fill="#eaf6ff"/>'
        for sx, sy, r in stars_rel[:6]:
            b += f'<circle cx="{x0 + sx * pw:.0f}" cy="{y0 + sy * ph:.0f}" r="{r * 4}" fill="#bfe8ff" opacity=".25" filter="url(#b3)"/>'
        px, py = x0 + spk[k][0] * pw, y0 + spk[k][1] * ph
        b += f'<circle cx="{px:.0f}" cy="{py:.0f}" r="60" fill="#ffe68a" opacity=".55" filter="url(#b12)"/>'
        b += f'<circle cx="{px:.0f}" cy="{py:.0f}" r="44" fill="none" stroke="#F2D27A" stroke-width="7"/>'
        b += f'<circle cx="{px:.0f}" cy="{py:.0f}" r="9" fill="#fff6c8"/>'
        if k == 0:   # ghost of where it will be
            pass
        # brass frame + clips
        b += f'<rect x="{x0}" y="{y0}" width="{pw}" height="{ph}" fill="none" stroke="#120a04" stroke-width="22"/>'
        b += f'<rect x="{x0}" y="{y0}" width="{pw}" height="{ph}" fill="none" stroke="url(#brass1)" stroke-width="13"/>'
        for cx in (x0 + 60, x0 + pw - 60):
            b += f'<rect x="{cx - 16}" y="{y0 + ph + 4}" width="32" height="60" fill="#5a3e18" stroke="#120a04" stroke-width="4"/>'
        b += f'<path d="M{x0 + pw / 2:.0f} {y0} L{x0 + pw / 2 + (1 if k else -1) * 70:.0f} 330" stroke="#2a1a08" stroke-width="16"/><path d="M{x0 + pw / 2:.0f} {y0} L{x0 + pw / 2 + (1 if k else -1) * 70:.0f} 330" stroke="url(#brass1)" stroke-width="9"/>'
    # jump arc from speck A to speck B
    ax, ay = 70 + .50 * 440, 340 + .52 * 420; bx, by = 570 + .62 * 440, 340 + .45 * 420
    arc = f'M{ax + 30:.0f} {ay - 40:.0f} Q{(ax + bx) / 2:.0f} {ay - 260:.0f} {bx - 34:.0f} {by - 34:.0f}'
    b += f'<path d="{arc}" fill="none" stroke="#ffe68a" stroke-width="22" opacity=".35" filter="url(#b6)"/>'
    b += f'<path d="{arc}" fill="none" stroke="#fff3b0" stroke-width="7" stroke-dasharray="20 14" stroke-linecap="round"/>'
    b += f'<path d="M{bx - 34:.0f} {by - 34:.0f} l-40 -4 M{bx - 34:.0f} {by - 34:.0f} l-10 -38" stroke="#fff3b0" stroke-width="9" stroke-linecap="round"/>'
    b += spark(ax - 70, ay - 70, 22) + spark(bx + 70, by - 60, 26) + spark(980, 300, 18, '#e8f6ff') + spark(110, 300, 16, '#e8f6ff')
    # ---- lower: floor, homemade telescope, frog farm boy ----
    b += '<path d="M0 1520 L1080 1520 L1080 1920 L0 1920Z" fill="#1a0f08"/>'
    for k in range(9):
        b += f'<path d="M{-200 + k * 180} 1920 L{140 + k * 100} 1520" stroke="#2c1a0e" stroke-width="5"/>'
    b += '<rect width="1080" height="1920" fill="url(#lamp1)"/>'
    # homemade telescope (wooden tube on a tripod) at the right
    b += '<g stroke="#140a04" stroke-linejoin="round" stroke-linecap="round">'
    b += '<path d="M800 1440 L700 1760 M800 1440 L900 1770 M800 1440 L820 1790" stroke-width="20"/><path d="M800 1440 L700 1760 M800 1440 L900 1770 M800 1440 L820 1790" stroke="#8a5a2e" stroke-width="10"/>'
    b += '<g transform="rotate(-38 800 1440)"><rect x="620" y="1400" width="420" height="84" rx="12" fill="#a8703a" stroke-width="6"/>'
    b += '<rect x="660" y="1400" width="20" height="84" fill="#6a4420" stroke-width="3"/><rect x="900" y="1400" width="20" height="84" fill="#6a4420" stroke-width="3"/>'
    b += '<rect x="1030" y="1390" width="40" height="104" rx="8" fill="#5a3a1c" stroke-width="5"/><rect x="580" y="1418" width="44" height="48" rx="6" fill="#3a2a1a" stroke-width="5"/></g>'
    b += '<circle cx="800" cy="1440" r="20" fill="#d9b06a" stroke-width="5"/></g>'
    b += f'<ellipse cx="300" cy="1800" rx="230" ry="26" fill="#000" opacity=".45" filter="url(#b12)"/>'
    straw = ('<path d="M-46 -84 q52 -20 104 0 q-52 12 -104 0z" fill="#e8c46a" stroke-width="3.4"/>'
             '<path d="M-24 -86 q30 -46 60 0z" fill="#f2d27a" stroke-width="3.4"/><path d="M-22 -90 q28 -6 56 0" stroke="#b5562a" stroke-width="5" fill="none"/>')
    overall = ('<path d="M-30 -30 q36 10 68 0 L36 6 L-28 6Z" fill="#4a6a9a" stroke-width="3.2"/>'
               '<path d="M-24 -30 L-30 -52 M32 -30 L38 -52" stroke="#4a6a9a" stroke-width="6"/>')
    b += frog(300, 1790, 3.7, look=(5, -5), mouth='O', hat=straw,
              armL='M-34 -24 q-22 -12 -26 -40', armR='M38 -24 q16 6 18 24')
    b += fireflies(26, 380, 1850, col='#ffe9a8', seed=3)
    b += darkband(850, 1290, .5)
    return out(1, '#0a1024', d, b, [('ONE SPECK', 160, 'w'), ('JUMPED', 250, 'y')], top=880)


# ============ 2. the Moon is bigger ============
def make_2():
    rnd = random.Random(22)
    d = lin('sky2', [(0, '#040814'), (.6, '#0a1230'), (1, '#10183a')])
    d += rad('moon2', 300, 470, 300, [(0, '#f6f6f2', 1), (.7, '#cfd0cc', 1), (1, '#8a8c90', 1)])
    d += rad('plu2', 760, 560, 210, [(0, '#f4d9b6', 1), (.6, '#c99a72', 1), (1, '#6a4230', 1)])
    d += halo('hm2', 300, 470, 520, inner='#ffffff', outer='#9fd0ff')
    d += halo('hp2', 790, 570, 340, inner='#ffe2b8', outer='#ffb070')
    d += lin('hill2', [(0, '#0c1a2a'), (1, '#04080e')])
    b = f'<rect width="{W}" height="{H}" fill="url(#sky2)"/>' + starfield(rnd, 220, 0, 1900, big=True)
    b += f'<ellipse cx="300" cy="470" rx="560" ry="560" fill="url(#hm2)" opacity=".6"/>'
    b += f'<ellipse cx="790" cy="570" rx="360" ry="360" fill="url(#hp2)" opacity=".55"/>'
    MX, MY, MR = 310, 470, 280
    PX, PY, PR = 812, 590, round(280 * 2376 / 3474)
    b += f'<circle cx="{MX}" cy="{MY}" r="{MR}" fill="url(#moon2)"/>'
    d += f'<clipPath id="mc2"><circle cx="{MX}" cy="{MY}" r="{MR}"/></clipPath><clipPath id="pc2"><circle cx="{PX}" cy="{PY}" r="{PR}"/></clipPath>'
    b += '<g clip-path="url(#mc2)">'
    for cx, cy, rx, ry, op in ((230, 360, 120, 80, .5), (370, 420, 90, 110, .45), (260, 560, 110, 70, .4), (420, 300, 60, 50, .4), (150, 470, 50, 70, .35), (390, 600, 60, 40, .35)):
        b += f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="#7a7e88" opacity="{op}"/>'
    for _ in range(26):
        cx, cy, r = rnd.uniform(MX - MR, MX + MR), rnd.uniform(MY - MR, MY + MR), rnd.uniform(6, 24)
        b += f'<circle cx="{cx:.0f}" cy="{cy:.0f}" r="{r:.0f}" fill="#8a8c92" opacity=".45"/><circle cx="{cx - r * .2:.0f}" cy="{cy - r * .2:.0f}" r="{r * .7:.0f}" fill="#e6e6e2" opacity=".5"/>'
    b += f'<circle cx="{MX + 120}" cy="{MY + 90}" r="{MR + 60}" fill="none" stroke="#000" stroke-width="140" opacity=".35" filter="url(#b24)"/>'
    b += '</g>'
    b += f'<circle cx="{MX}" cy="{MY}" r="{MR}" fill="none" stroke="#fff" stroke-width="4" opacity=".6"/>'
    # Pluto
    b += f'<circle cx="{PX}" cy="{PY}" r="{PR}" fill="url(#plu2)"/>'
    b += '<g clip-path="url(#pc2)">'
    b += f'<path d="M{PX - 190} {PY + 40} q60 -40 140 -10 q60 30 140 0 q40 -10 60 10 L{PX + 260} {PY + 200} L{PX - 260} {PY + 200}Z" fill="#6a3424" opacity=".55"/>'
    b += f'<path d="M{PX - 20} {PY - 20} q-40 -60 -10 -90 q30 -10 40 30 q20 -50 60 -30 q30 30 -10 90 q-30 40 -50 60 q-30 -30 -30 -60z" fill="#fff4e0" opacity=".55"/>'
    for _ in range(10):
        b += f'<circle cx="{rnd.uniform(PX - PR, PX + PR):.0f}" cy="{rnd.uniform(PY - PR, PY - 40):.0f}" r="{rnd.uniform(5, 14):.0f}" fill="#8a5a40" opacity=".35"/>'
    b += f'<circle cx="{PX + 90}" cy="{PY + 70}" r="{PR + 50}" fill="none" stroke="#000" stroke-width="110" opacity=".4" filter="url(#b24)"/>'
    b += '</g>'
    b += f'<circle cx="{PX}" cy="{PY}" r="{PR}" fill="none" stroke="#ffe8c8" stroke-width="4" opacity=".6"/>'
    # measuring bars + labels
    def bar(x0, x1, y, lab):
        o = f'<path d="M{x0} {y} H{x1} M{x0} {y - 16} V{y + 16} M{x1} {y - 16} V{y + 16}" stroke="#0a0f1e" stroke-width="12" stroke-linecap="round"/>'
        o += f'<path d="M{x0} {y} H{x1} M{x0} {y - 16} V{y + 16} M{x1} {y - 16} V{y + 16}" stroke="#bfe6ff" stroke-width="5" stroke-linecap="round"/>'
        o += (f'<text x="{(x0 + x1) / 2}" y="{y + 62}" text-anchor="middle" font-family="Fredoka" font-weight="700" font-size="44" fill="#fff" '
              f'stroke="#05070f" stroke-width="10" paint-order="stroke" letter-spacing="2">{lab}</text>')
        return o
    b += bar(MX - MR, MX + MR, 120 - 40, '') if False else ''
    b += bar(MX - MR + 4, MX + MR - 4, MY + MR + 34, '3,474 KM')
    b += bar(PX - PR + 4, PX + PR - 4, PY + PR + 34, '2,376 KM')
    b += spark(960, 200, 26) + spark(80, 820, 18, '#e8f0ff') + spark(1000, 330, 14, '#e8f0ff') + spark(600, 140, 16)
    # ---- lower: hilltop, frog with a long tape measure ----
    b += '<path d="M0 1560 q300 -110 560 -60 q280 50 520 -10 L1080 1920 L0 1920Z" fill="url(#hill2)"/>'
    b += '<path d="M0 1560 q300 -110 560 -60 q280 50 520 -10" fill="none" stroke="#5a8ab8" stroke-width="4" opacity=".5"/>'
    for _ in range(40):
        x = rnd.uniform(0, W); y0 = 1560 - 80 * math.sin(x / W * math.pi) + rnd.uniform(0, 20)
        b += f'<path d="M{x:.0f} {y0 + 40:.0f} q{rnd.uniform(-8, 8):.0f} -20 {rnd.uniform(-10, 10):.0f} -38" stroke="#0a1a24" stroke-width="5" fill="none"/>'
    # tape measure: yellow case in the frog's hands, tape stretched up-right to the edge
    b += f'<ellipse cx="290" cy="1780" rx="220" ry="24" fill="#000" opacity=".4" filter="url(#b12)"/>'
    b += '<path d="M410 1590 L1100 1330" stroke="#140c00" stroke-width="34" stroke-linecap="round"/><path d="M410 1590 L1100 1330" stroke="#f2d27a" stroke-width="24" stroke-linecap="round"/>'
    for k in range(1, 30):
        x = 410 + k * 24; y = 1590 - k * 24 * 260 / 690
        b += f'<path d="M{x:.0f} {y:.0f} l{4:.0f} {10 if k % 5 else 15}" stroke="#3a2a00" stroke-width="3"/>'
    front = ('<rect x="20" y="-46" width="44" height="40" rx="9" fill="#f2c94c" stroke-width="3.4"/><circle cx="42" cy="-26" r="9" fill="#d9a83a" stroke-width="2.6"/>')
    b += frog(290, 1770, 3.7, look=(4, -5), mouth='O', front=front,
              armL='M-34 -24 q-18 -2 -22 20', armR='M38 -24 q4 -4 8 -2')
    b += fireflies(20, 300, 1850, col='#cfe6ff', core='#f4faff', seed=5)
    b += darkband(860, 1260, .45)
    return out(2, '#040814', d, b, [('THE MOON IS', 150, 'w'), ('BIGGER', 250, 'y')], top=890)


# ============ 3. a cosmic rebel: tilted oval orbit crossing Neptune ============
def ell_pts(a, e, sy, rot, cx, cy, n=200):
    c = a * e; bb = a * math.sqrt(1 - e * e); r = math.radians(rot); pts = []
    for i in range(n + 1):
        t = 2 * math.pi * i / n
        x, y = -c + a * math.cos(t), bb * math.sin(t) * sy
        pts.append((cx + x * math.cos(r) - y * math.sin(r), cy + x * math.sin(r) + y * math.cos(r)))
    return pts


def make_3():
    rnd = random.Random(33)
    d = rad('bg3', 540, 480, 1300, [(0, '#1a1040', 1), (.5, '#0a0820', 1), (1, '#04030c', 1)])
    d += halo('sun3', 540, 480, 300, inner='#fff6d0', outer='#ffb040')
    d += rad('nep3', 800, 1520, 520, [(0, '#8fe0ff', 1), (.55, '#3a7ad8', 1), (1, '#13306a', 1)])
    d += halo('pg3', 0, 0, 120, inner='#ffe8c0', outer='#ff9a4a')
    b = f'<rect width="{W}" height="{H}" fill="url(#bg3)"/>' + starfield(rnd, 240, 0, 1900, big=True)
    # Milky-way haze
    b += '<path d="M-100 300 Q540 120 1200 260 L1200 380 Q540 260 -100 440Z" fill="#9a7cff" opacity=".10" filter="url(#b24)"/>'
    CX, CY, SQ = 540, 500, .30
    # orbits of the eight planets: flat, neat circles
    planets = [(70, '#c9b8a0', 6), (105, '#f0c890', 8), (145, '#6ab8ff', 9), (185, '#ff8a5a', 8), (260, '#e8b878', 18), (330, '#f2dca0', 15), (395, '#a8f0f0', 12), (450, '#5a8aff', 13)]
    for k, (r, col, pr) in enumerate(planets):
        st = '#7ac8ff' if k == 7 else '#a8b8ff'
        b += f'<ellipse cx="{CX}" cy="{CY}" rx="{r}" ry="{r * SQ:.0f}" fill="none" stroke="{st}" stroke-width="{6 if k == 7 else 2.5}" opacity="{.85 if k == 7 else .45}"/>'
    b += f'<ellipse cx="{CX}" cy="{CY}" rx="450" ry="{450 * SQ:.0f}" fill="none" stroke="#7ac8ff" stroke-width="22" opacity=".25" filter="url(#b6)"/>'
    b += f'<circle cx="{CX}" cy="{CY}" r="300" fill="url(#sun3)"/>'
    b += f'<circle cx="{CX}" cy="{CY}" r="46" fill="#fff8e0"/><circle cx="{CX}" cy="{CY}" r="70" fill="#ffd070" opacity=".5" filter="url(#b12)"/>'
    for k, (r, col, pr) in enumerate(planets):
        t = 1.1 + k * 1.37
        x, y = CX + r * math.cos(t), CY + r * SQ * math.sin(t)
        b += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{pr}" fill="{col}" stroke="#0a0a1a" stroke-width="2.5"/>'
        if k == 5:
            b += f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{pr * 2.1:.0f}" ry="{pr * .55:.0f}" fill="none" stroke="#f2dca0" stroke-width="3" transform="rotate(-12 {x:.0f} {y:.0f})"/>'
    # Pluto's tilted oval orbit (17 degrees), sun at one focus, cutting inside Neptune's
    pts = ell_pts(400, .30, .62, -17, CX + 20, CY)
    pth = 'M' + ' L'.join(f'{x:.1f},{y:.1f}' for x, y in pts)
    b += f'<path d="{pth}" fill="none" stroke="#ff9a4a" stroke-width="30" opacity=".35" filter="url(#b12)"/>'
    b += f'<path d="{pth}" fill="none" stroke="#ffc27a" stroke-width="7" stroke-dasharray="26 12" stroke-linecap="round"/>'
    # crossing points with Neptune's circle: mark with sparks
    def onnep(x, y): return ((x - CX) / 450) ** 2 + ((y - CY) / (450 * SQ)) ** 2
    cross = []
    for i in range(len(pts) - 1):
        a, c = onnep(*pts[i]) - 1, onnep(*pts[i + 1]) - 1
        if a * c < 0: cross.append(pts[i])
    for x, y in cross:
        b += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="40" fill="#fff0b0" opacity=".5" filter="url(#b12)"/>' + spark(x, y, 30, '#fffbe0', 1)
    # Pluto on its orbit (near perihelion side, inside Neptune's lane)
    i = int(len(pts) * .03); px, py = pts[i]
    b += f'<g transform="translate({px:.0f} {py:.0f})"><circle r="120" fill="url(#pg3)"/></g>'
    b += f'<circle cx="{px:.0f}" cy="{py:.0f}" r="46" fill="#e8c8a0" stroke="#3a2010" stroke-width="4"/><path d="M{px - 14:.0f} {py:.0f} q8 -14 16 -2 q8 -14 14 0 q-4 12 -15 18 q-12 -6 -15 -16z" fill="#fff4e0" opacity=".8"/>'
    b += f'<circle cx="{px - 10:.0f}" cy="{py - 12:.0f}" r="8" fill="#fff" opacity=".5"/>'
    # tilt angle mark at the sun
    b += f'<path d="M{CX + 60} {CY} L{CX + 250} {CY}" stroke="#fff" stroke-width="3" opacity=".5" stroke-dasharray="8 8"/>'
    b += spark(120, 160, 24) + spark(970, 150, 20, '#e8f0ff') + spark(160, 760, 16, '#ffe8c0') + spark(930, 780, 18)
    # ---- lower: Neptune rising bottom-right, frog traffic cop on a little rock ----
    b += f'<circle cx="960" cy="1700" r="360" fill="#5ab0ff" opacity=".35" filter="url(#b24)"/>'
    b += f'<circle cx="960" cy="1700" r="330" fill="url(#nep3)"/>'
    d += '<clipPath id="nc3"><circle cx="960" cy="1700" r="330"/></clipPath>'
    b += '<g clip-path="url(#nc3)">'
    for yy, op in ((1480, .25), (1560, .2), (1650, .25), (1760, .2), (1840, .15)):
        b += f'<path d="M600 {yy} q360 -30 720 0" stroke="#bff0ff" stroke-width="18" fill="none" opacity="{op}"/>'
    b += '<ellipse cx="900" cy="1590" rx="60" ry="26" fill="#0e2a6a" opacity=".7"/>'
    b += '<circle cx="1230" cy="1990" r="420" fill="none" stroke="#020818" stroke-width="300" opacity=".55" filter="url(#b24)"/></g>'
    b += '<circle cx="960" cy="1700" r="330" fill="none" stroke="#cff4ff" stroke-width="5" opacity=".7"/>'
    b += '<path d="M60 1840 q20 -110 200 -120 q190 -6 240 110 q10 30 -20 40 L80 1880Z" fill="#3a3448" stroke="#14101e" stroke-width="6"/>'
    b += '<path d="M120 1760 q60 -30 120 -20" stroke="#6a6480" stroke-width="5" fill="none"/>'
    b += f'<ellipse cx="290" cy="1730" rx="220" ry="200" fill="#ffd080" opacity=".12" filter="url(#b24)"/>'
    cap = ('<path d="M-30 -88 q36 -34 74 0 z" fill="#2a3a6a" stroke-width="3.4"/><path d="M-36 -86 q40 -8 84 0 q-4 10 -44 10 q-36 0 -40 -10z" fill="#1a2448" stroke-width="3.4"/>'
           '<circle cx="7" cy="-102" r="7" fill="#f2d27a" stroke-width="2.6"/>')
    whistle = ('<path d="M10 -40 L-2 -34" stroke="#c9ccd4" stroke-width="2"/>'
               '<rect x="4" y="-46" width="24" height="12" rx="5" fill="#d9dde6" stroke-width="3"/><circle cx="28" cy="-38" r="9" fill="#d9dde6" stroke-width="3"/>')
    b += frog(290, 1740, 3.6, look=(6, -3), mouth='none', hat=cap, front=whistle,
              armR='M38 -24 q24 -14 30 -46', armL='M-34 -22 q-14 6 -16 22')
    b += fireflies(18, 280, 1850, col='#ffd8a8', seed=9)
    b += darkband(860, 1260, .45)
    return out(3, '#04030c', d, b, [('A COSMIC', 160, 'w'), ('REBEL', 260, 'y')], top=880)


# ============ 4. Pluto got voted out in Prague ============
def make_4():
    rnd = random.Random(44)
    d = lin('hall4', [(0, '#0e0a1a'), (.6, '#1a1020'), (1, '#0a0608')])
    d += lin('beam4', [(0, '#fff2c8'), (1, '#fff2c8')])
    d += rad('plu4', 520, 560, 150, [(0, '#f6dcbc', 1), (.6, '#c99a72', 1), (1, '#5a3424', 1)])
    d += halo('h4', 540, 560, 360, inner='#fff3c0', outer='#ffcf6a')
    d += lin('win4', [(0, '#0e1c44'), (1, '#24305a')])
    d += lin('podium4', [(0, '#5a2a2a'), (1, '#2a1014')], x2=1, y2=0)
    b = f'<rect width="{W}" height="{H}" fill="url(#hall4)"/>'
    # tall arched windows with Prague night skyline
    for wx in (70, 860):
        wpath = f'M{wx} 760 V250 q75 -120 150 0 V760Z'
        d += f'<clipPath id="wc{wx}"><path d="{wpath}"/></clipPath>'
        b += f'<path d="{wpath}" fill="url(#win4)"/>'
        b += f'<g clip-path="url(#wc{wx})">' + ''.join(f'<circle cx="{wx + rnd.uniform(0, 150):.0f}" cy="{rnd.uniform(160, 560):.0f}" r="1.8" fill="#fff" opacity=".7"/>' for _ in range(16))
        b += (f'<path d="M{wx} 760 V640 h20 v-30 h14 v-60 l8 -30 l8 30 v60 h16 v20 h22 v-70 l10 -40 l10 40 v70 h20 v40 h32 V760Z" fill="#06040c"/>'
              f'<circle cx="{wx + 50}" cy="660" r="3" fill="#ffd27a"/><circle cx="{wx + 110}" cy="690" r="3" fill="#ffd27a"/></g>')
        b += f'<path d="{wpath}" fill="none" stroke="#3a2a3a" stroke-width="14"/><path d="M{wx + 75} 160 V760 M{wx} 470 H{wx + 150}" stroke="#3a2a3a" stroke-width="8"/>'
    # red curtains
    for sgn, x0 in ((1, 0), (-1, 1080)):
        b += f'<path d="M{x0} 0 L{x0 + sgn * 330} 0 q{-sgn * 60} 300 {-sgn * 160} 420 q{-sgn * 80} 60 {-sgn * 170} 60Z" fill="#6a1a22" stroke="#2a060a" stroke-width="5"/>'
        for k in range(4):
            b += f'<path d="M{x0 + sgn * (60 + k * 60)} 0 q{-sgn * 10} 240 {-sgn * (40 + k * 30)} 400" stroke="#3a0a10" stroke-width="7" fill="none" opacity=".7"/>'
    b += '<path d="M0 0 H1080 V70 q-270 40 -540 0 q-270 40 -540 0Z" fill="#7a1e28" stroke="#2a060a" stroke-width="5"/>'
    # spotlight beam
    b += '<path d="M470 0 L610 0 L800 800 L280 800Z" fill="#fff2c8" opacity=".16" filter="url(#b12)"/>'
    b += '<path d="M500 0 L580 0 L700 800 L380 800Z" fill="#fff2c8" opacity=".12" filter="url(#b6)"/>'
    b += '<ellipse cx="540" cy="560" rx="400" ry="400" fill="url(#h4)" opacity=".7"/>'
    # podium
    b += '<ellipse cx="540" cy="770" rx="280" ry="46" fill="#fff2c8" opacity=".35" filter="url(#b12)"/>'
    b += '<path d="M370 740 L710 740 L690 840 L390 840Z" fill="url(#podium4)" stroke="#1a0608" stroke-width="5"/>'
    b += '<ellipse cx="540" cy="740" rx="170" ry="26" fill="#8a3a3a" stroke="#1a0608" stroke-width="5"/>'
    b += '<path d="M440 790 H640" stroke="#f2d27a" stroke-width="5" opacity=".8"/>'
    # Pluto on the podium under the spotlight
    PX, PY, PR = 540, 580, 150
    b += f'<circle cx="{PX}" cy="{PY}" r="{PR}" fill="url(#plu4)"/>'
    d += f'<clipPath id="pc4"><circle cx="{PX}" cy="{PY}" r="{PR}"/></clipPath>'
    b += f'<g clip-path="url(#pc4)"><path d="M{PX - 150} {PY + 50} q60 -30 120 -6 q60 26 120 -4 q40 -10 60 10 L{PX + 160} {PY + 160} L{PX - 160} {PY + 160}Z" fill="#6a3424" opacity=".5"/>'
    b += f'<path d="M{PX - 14} {PY + 10} q-40 -50 -10 -76 q26 -8 34 24 q16 -40 50 -24 q24 26 -10 76 q-24 30 -40 46 q-22 -24 -24 -46z" fill="#fff4e0" opacity=".6"/>'
    b += f'<circle cx="{PX + 70}" cy="{PY + 60}" r="{PR + 40}" fill="none" stroke="#000" stroke-width="80" opacity=".35" filter="url(#b24)"/></g>'
    b += f'<circle cx="{PX}" cy="{PY}" r="{PR}" fill="none" stroke="#fff2d0" stroke-width="4" opacity=".7"/>'
    # sad little face on Pluto (eyebrows + small mouth)
    b += f'<path d="M{PX - 56} {PY - 40} q14 -14 30 -6 M{PX + 26} {PY - 46} q16 -8 30 6" stroke="#2a1408" stroke-width="7" fill="none" stroke-linecap="round"/>'
    b += f'<circle cx="{PX - 40}" cy="{PY - 14}" r="9" fill="#2a1408"/><circle cx="{PX + 40}" cy="{PY - 14}" r="9" fill="#2a1408"/>'
    b += f'<path d="M{PX - 20} {PY + 36} q20 -16 40 0" stroke="#2a1408" stroke-width="7" fill="none" stroke-linecap="round"/>'
    b += spark(330, 380, 22) + spark(760, 340, 26) + spark(720, 720, 16) + spark(300, 700, 14)
    # ---- lower: crowd of astronomers raising glowing yellow voting cards ----
    b += '<rect y="1300" width="1080" height="620" fill="#0a0608"/>'
    def card(x, y, rot, sc=1.0):
        o = f'<g transform="translate({x} {y}) rotate({rot}) scale({sc})">'
        o += '<rect x="-46" y="-34" width="92" height="64" rx="6" fill="#ffd84a" opacity=".55" filter="url(#b12)"/>'
        o += '<path d="M0 30 L0 150" stroke="#05030a" stroke-width="30" stroke-linecap="round"/>'
        o += '<rect x="-40" y="-30" width="80" height="58" rx="5" fill="#ffd84a" stroke="#3a2a00" stroke-width="4"/>'
        o += '<path d="M-28 -14 h56 M-28 0 h40" stroke="#c99a1a" stroke-width="5" stroke-linecap="round"/></g>'
        return o
    rows = [(1440, 1.0, '#140c14', 7), (1580, 1.15, '#0a060c', 6)]
    for yrow, sc, col, n in rows:
        for k in range(n):
            x = (k + .5 + rnd.uniform(-.2, .2)) * W / n
            if yrow == 1580 and x < 470: continue
            b += card(x + rnd.uniform(-20, 20), yrow - 150 * sc + rnd.uniform(-30, 30), rnd.uniform(-14, 14), sc)
            b += f'<circle cx="{x:.0f}" cy="{yrow:.0f}" r="{58 * sc:.0f}" fill="{col}"/><path d="M{x - 110 * sc:.0f} {yrow + 200 * sc:.0f} q0 -140 {110 * sc:.0f} -140 q{110 * sc:.0f} 0 {110 * sc:.0f} 140Z" fill="{col}"/>'
    b += '<rect y="1700" width="1080" height="220" fill="#06040a"/>'
    b += f'<ellipse cx="270" cy="1600" rx="230" ry="210" fill="#ffd84a" opacity=".14" filter="url(#b24)"/>'
    # frog in the audience, raising a voting card
    cardf = ('<path d="M54 -96 L54 -40" stroke="#5a3a1c" stroke-width="5"/>'
             '<rect x="22" y="-142" width="66" height="48" rx="5" fill="#ffd84a" stroke-width="3.4"/><path d="M32 -128 h44 M32 -116 h30" stroke="#c99a1a" stroke-width="4"/>')
    tie = '<path d="M2 -26 l4 -6 l4 6 l-4 22z" fill="#c43a3a" stroke-width="2.4"/>'
    b += frog(270, 1760, 3.6, look=(6, -2), mouth='O', back=cardf,
              armR='M38 -24 q12 -16 16 -40', armL='M-34 -22 q-14 6 -16 22')
    b += fireflies(18, 200, 1850, col='#ffe08a', seed=13)
    b += darkband(860, 1260, .5)
    return out(4, '#0e0a1a', d, b, [('PLUTO GOT', 160, 'w'), ('VOTED OUT', 172, 'y')], top=890)


# ============ 5. Pluto has a heart ============
def make_5():
    rnd = random.Random(55)
    d = rad('bg5', 540, 520, 1300, [(0, '#0e1430', 1), (.6, '#060914', 1), (1, '#020308', 1)])
    d += rad('plu5', 470, 400, 420, [(0, '#f2d6b4', 1), (.55, '#c4906a', 1), (1, '#4a2a20', 1)])
    d += halo('haze5', 540, 500, 420, inner='#bfe6ff', outer='#5aa8ff')
    d += rad('heart5', 560, 520, 220, [(0, '#ffffff', 1), (.6, '#fff4e6', 1), (1, '#f0dcc8', 1)])
    d += lin('foil5', [(0, '#f6d27a'), (.5, '#c9902a'), (1, '#7a5418')], x2=1, y2=1)
    b = f'<rect width="{W}" height="{H}" fill="url(#bg5)"/>' + starfield(rnd, 240, 0, 1900, big=True)
    PX, PY, PR = 540, 500, 340
    # blue haze atmosphere
    b += f'<circle cx="{PX}" cy="{PY}" r="{PR + 120}" fill="url(#haze5)" opacity=".7"/>'
    b += f'<circle cx="{PX}" cy="{PY}" r="{PR + 14}" fill="none" stroke="#8fd0ff" stroke-width="26" opacity=".55" filter="url(#b6)"/>'
    b += f'<circle cx="{PX}" cy="{PY}" r="{PR}" fill="url(#plu5)"/>'
    d += f'<clipPath id="pc5"><circle cx="{PX}" cy="{PY}" r="{PR}"/></clipPath>'
    b += '<g clip-path="url(#pc5)">'
    # dark reddish tholin band (Cthulhu) along the lower left
    b += f'<path d="M{PX - 360} {PY + 60} q120 -60 220 0 q60 40 120 40 q40 70 -30 140 q-140 80 -320 40Z" fill="#5a2418" opacity=".75"/>'
    b += f'<path d="M{PX + 200} {PY + 200} q80 -30 160 10 L{PX + 360} {PY + 360} L{PX + 160} {PY + 360}Z" fill="#6a2c1e" opacity=".6"/>'
    for _ in range(14):
        b += f'<ellipse cx="{rnd.uniform(PX - PR, PX + PR):.0f}" cy="{rnd.uniform(PY - PR, PY - 120):.0f}" rx="{rnd.uniform(14, 40):.0f}" ry="{rnd.uniform(8, 20):.0f}" fill="#8a5038" opacity=".3"/>'
    # the heart (Tombaugh Regio); left lobe = Sputnik Planitia with convection cells
    HX, HY, S = 600, 520, 1.0
    heart = f'M{HX} {HY + 190} C{HX - 90} {HY + 120} {HX - 230} {HY + 40} {HX - 210} {HY - 70} C{HX - 190} {HY - 170} {HX - 60} {HY - 170} {HX} {HY - 80} C{HX + 60} {HY - 170} {HX + 200} {HY - 160} {HX + 210} {HY - 60} C{HX + 220} {HY + 40} {HX + 90} {HY + 120} {HX} {HY + 190}Z'
    b += f'<path d="{heart}" fill="#fff6e0" opacity=".9" filter="url(#b24)"/>'
    b += f'<path d="{heart}" fill="url(#heart5)"/>'
    d += f'<clipPath id="hc5"><path d="{heart}"/></clipPath>'
    b += '<g clip-path="url(#hc5)">'
    for _ in range(40):
        cx, cy = rnd.uniform(HX - 210, HX + 10), rnd.uniform(HY - 140, HY + 180)
        b += f'<path d="M{cx:.0f} {cy:.0f} m-22 0 l11 -18 h22 l11 18 l-11 18 h-22z" fill="none" stroke="#b8cce0" stroke-width="2.4" opacity=".55"/>'
    b += f'<path d="M{HX + 20} {HY - 80} q60 40 40 120 q-20 60 -40 100" stroke="#e8d4bc" stroke-width="30" fill="none" opacity=".5"/>'
    b += '</g>'
    b += f'<circle cx="{PX + 150}" cy="{PY + 110}" r="{PR + 80}" fill="none" stroke="#000" stroke-width="180" opacity=".42" filter="url(#b24)"/>'
    b += '</g>'
    b += f'<circle cx="{PX}" cy="{PY}" r="{PR}" fill="none" stroke="#dff2ff" stroke-width="4" opacity=".55"/>'
    # Charon, small, upper left
    b += '<circle cx="110" cy="150" r="46" fill="#9a9aa2" stroke="#2a2a30" stroke-width="3"/><path d="M80 130 q30 -16 60 0" stroke="#5a3a3a" stroke-width="14" fill="none" opacity=".6"/>'
    b += '<circle cx="130" cy="170" r="60" fill="none" stroke="#000" stroke-width="36" opacity=".3" filter="url(#b6)"/>'
    b += spark(HX - 40, HY - 40, 34, '#fffbe8', 1) + spark(980, 150, 24) + spark(150, 760, 18, '#cfe6ff') + spark(960, 790, 20, '#cfe6ff') + spark(840, 240, 16)
    # ---- lower: New Horizons in the foreground, frog astronaut holding the dish ----
    NX, NY = 640, 1560
    b += f'<ellipse cx="{NX}" cy="{NY}" rx="420" ry="300" fill="#ffd890" opacity=".1" filter="url(#b50)"/>'
    b += f'<g transform="translate({NX} {NY}) rotate(-12)" stroke="#140c04" stroke-linejoin="round" stroke-width="5">'
    b += '<path d="M120 60 L420 150" stroke="#2a2a30" stroke-width="18"/><path d="M120 60 L420 150" stroke="#8a8c96" stroke-width="9"/>'
    b += '<rect x="380" y="120" width="120" height="64" rx="16" fill="#3a3a42" transform="rotate(16 440 152)"/>'
    for k in range(6):
        b += f'<path d="M{392 + k * 18} 126 v56" stroke="#5a5a66" stroke-width="5" transform="rotate(16 440 152)"/>'
    b += '<path d="M-150 -20 L120 -60 L150 120 L-120 160Z" fill="url(#foil5)"/>'
    for k in range(7):
        b += f'<path d="M{-130 + k * 40} {-20 - k * 5} q10 60 0 {150 + k * 2}" stroke="#7a5418" stroke-width="3" fill="none" opacity=".7"/>'
    b += '<path d="M-150 -20 L-120 160 L-150 190 L-180 10Z" fill="#a8761e"/>'
    b += '</g>'
    # dish antenna (big white parabola facing up-left toward Pluto)
    b += f'<g transform="translate({NX - 70} {NY - 110}) rotate(-28)">'
    b += '<ellipse cx="0" cy="0" rx="230" ry="74" fill="#2a2e38" stroke="#0a0c10" stroke-width="6"/>'
    b += '<path d="M-230 0 Q0 210 230 0" fill="#e6eaf2" stroke="#0a0c10" stroke-width="6"/>'
    b += '<ellipse cx="0" cy="0" rx="222" ry="68" fill="#f4f6fa" stroke="#0a0c10" stroke-width="5"/>'
    b += '<ellipse cx="0" cy="0" rx="150" ry="44" fill="none" stroke="#c9ced8" stroke-width="3"/>'
    b += '<path d="M-130 -10 L0 -120 L130 -10 M0 -120 L0 30" fill="none" stroke="#5a5e68" stroke-width="7"/><circle cx="0" cy="-120" r="16" fill="#c9ced8" stroke="#0a0c10" stroke-width="4"/></g>'
    b += f'<path d="M{NX - 120} {NY - 260} L{NX - 330} {NY - 440}" stroke="#bfe6ff" stroke-width="10" opacity=".35" filter="url(#b6)" stroke-dasharray="20 20"/>'
    # frog astronaut sitting on the dish rim, holding the rim
    b += frog(250, 1700, 3.4, rot=-6, helmet=True, look=(3, -6), mouth='O',
              armR='M38 -22 q6 -10 -4 -20', armL='M-34 -24 q-20 -10 -24 -36')
    b += fireflies(16, 300, 1850, col='#cfe6ff', core='#f4faff', seed=21)
    b += darkband(860, 1260, .45)
    return out(5, '#020308', d, b, [('PLUTO HAS A', 150, 'w'), ('HEART', 260, 'y')], top=880)


if __name__ == '__main__':
    for n in (sys.argv[1:] or ['1', '2', '3', '4', '5']):
        globals()[f'make_{n}']()
    print('ok')
