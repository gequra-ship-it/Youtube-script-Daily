# Thumbnail D for edge-of-universe (guideline 16-6/16-7, brief tools/briefs/thumb_art.md). A-C stay in make.py (untouched).
# D = film homage to The Truman Show (miya's reference): the frog's little rocket reaches the cosmic event horizon,
#     drawn as a faint curved grid "wall" across space (S25-S26: even light never bridges the gap); a ghostly stair
#     climbs to a glowing door with galaxies beyond. Text from S36: "we can see light ... but we can never visit them".
# run: python3 d_make.py
import os, math, random
from make import HERE, INK, frog, galaxy, small_gal, SOFT, grain, starfield, corner
from thumb_lib import page, svg, lin, rad, spark

HZ = 770   # horizon line (where the wall meets the nebula sea), ~71% of height


def wall_grid():
    # the horizon is a sphere around us: draw it as the inside of a huge globe (curved meridians and parallels)
    cx = 1300; p = ''
    for k in range(-8, 9):
        x = cx + k * 190
        bend = k * 26   # meridians bow outward away from the centre
        p += f'M{x} -40 Q{x + bend} {HZ / 2:.0f} {x} {HZ + 10}'
    for j, y in enumerate((70, 230, 400, 580)):
        sag = 36 - j * 8   # parallels arch upward, flatter near the horizon
        p += f'M-40 {y + sag} Q{cx} {y - sag * 2} 1960 {y + sag}'
    p += f'M-40 {HZ} H1960'
    return p


def cloud_sea(rnd):
    # calm deep-blue sea: navy gradient, thin horizontal glints, golden reflection under the door
    d = lin('seaG', [(0, '#4a6f9e'), (.08, '#2c4a78'), (.45, '#1a2f55'), (1, '#0b1630')])
    out = f'<rect x="0" y="{HZ}" width="1920" height="{1080 - HZ}" fill="url(#seaG)"/>'
    for _ in range(520):
        y = rnd.randint(HZ + 4, 1075); f = (y - HZ) / (1080 - HZ)
        x = rnd.randint(-40, 1900); L = rnd.randint(14, 70) * (1 + f * 1.6)
        col = rnd.choice(['#9fc4ea', '#6f97c8', '#c9def2', '#4d74a8'])
        out += f'<rect x="{x}" y="{y}" width="{L:.0f}" height="{1.6 + f * 2.2:.1f}" rx="1" fill="{col}" opacity="{(.45 - f * .25) * rnd.uniform(.4, 1):.2f}"/>'
    # gold reflection column of the door
    for i in range(28):
        y = HZ + 6 + i * 6.5; w = 60 + i * 5 + rnd.randint(-20, 20)
        out += f'<rect x="{1650 - w / 2 + rnd.randint(-14, 14):.0f}" y="{y:.0f}" width="{w}" height="3" rx="1.5" fill="#ffe2a0" opacity="{.55 * (1 - i / 28):.2f}"/>'
    return d, out


def rocket(x, y, s):
    # the frog's little rocket, pointing right; nose tip at (x, y)
    g = f'<g transform="translate({x} {y}) scale({s})" stroke="#140c18" stroke-width="5" stroke-linejoin="round" stroke-linecap="round">'
    # engine flame (stuck at full thrust)
    g += '<path d="M-520 -30 Q-640 -6 -700 0 Q-640 6 -520 30 Z" fill="#7fe3ff" stroke="none" opacity=".35" filter="url(#soft)"/>'
    g += '<path d="M-520 -22 Q-610 -4 -650 0 Q-610 4 -520 22 Z" fill="#c9f6ff" stroke="none" opacity=".9"/>'
    g += '<path d="M-520 -12 Q-575 -2 -595 0 Q-575 2 -520 12 Z" fill="#fff" stroke="none"/>'
    # back fins
    g += '<path d="M-430 -48 L-520 -150 L-470 -150 L-360 -56 Z" fill="#e0625a"/>'
    g += '<path d="M-430 -48 L-520 -150 L-470 -150 Z" fill="#ff8f7f" stroke="none" opacity=".6"/>'
    # body
    g += ('<path d="M-520 -40 Q-520 -72 -470 -72 L-150 -72 Q-20 -70 0 0 Q-20 70 -150 72 L-470 72 Q-520 72 -520 40 Z" '
          'fill="url(#hull)"/>')
    g += '<path d="M-470 -58 L-140 -58 Q-150 -58 -150 -58" fill="none" stroke="#fff" stroke-width="6" opacity=".8"/>'
    g += '<path d="M-470 56 L-130 56" fill="none" stroke="#8d8aa6" stroke-width="5" opacity=".7"/>'
    # gold band + nose cone
    g += '<path d="M-150 -72 Q-20 -70 0 0 Q-20 70 -150 72 Z" fill="url(#nose)"/>'
    g += '<path d="M-140 -54 Q-60 -50 -24 -14" fill="none" stroke="#fff6d0" stroke-width="7" opacity=".8"/>'
    g += '<path d="M-150 -72 L-150 72" stroke-width="5"/>'
    g += '<rect x="-330" y="-74" width="30" height="148" rx="6" fill="#F2D27A"/>'
    g += '<rect x="-470" y="-74" width="20" height="148" rx="6" fill="#F2D27A"/>'
    g += '<path d="M-520 18 L-150 18 Q-60 18 -6 4" fill="none" stroke="#140c18" stroke-width="14"/><path d="M-520 18 L-150 18 Q-60 18 -6 4" fill="none" stroke="#F2D27A" stroke-width="8"/>'
    # porthole
    g += '<circle cx="-240" cy="0" r="38" fill="#d9dce8"/><circle cx="-240" cy="0" r="27" fill="url(#port)"/>'
    g += '<path d="M-256 -14 q10 -10 24 -10" fill="none" stroke="#fff" stroke-width="5" opacity=".85"/>'
    for a in range(0, 360, 45):
        t = math.radians(a)
        g += f'<circle cx="{-240 + 33 * math.cos(t):.1f}" cy="{33 * math.sin(t):.1f}" r="2.4" fill="#5a5870" stroke="none"/>'
    # rivets
    g += ''.join(f'<circle cx="{-430 + i * 40}" cy="-40" r="3" fill="#7d7a96" stroke="none"/>' for i in range(3))
    # lower fin (in front)
    g += '<path d="M-430 48 L-530 160 L-475 160 L-350 60 Z" fill="#c84c48"/>'
    # exhaust bell
    g += '<path d="M-520 -40 L-548 -52 L-548 52 L-520 40 Z" fill="#5a5870"/>'
    g += '</g>'
    return g


def stairs():
    # translucent glass steps rising from the touch point to the door; each tile glows warmer as it climbs
    out = ''
    x0, y0 = 1330, HZ - 4; n = 8; w = 42; h = 43
    out += f'<path d="M{x0} {y0} L{x0 + n * w + 20} {y0 - n * h}" stroke="#ffe7a8" stroke-width="60" opacity=".18" filter="url(#blur12)"/>'
    for i in range(n):
        x = x0 + i * w; y = y0 - (i + 1) * h
        t = i / (n - 1)
        col = f'#{int(120 + 90 * t):02x}{int(190 + 40 * t):02x}{int(245 - 5 * t):02x}'
        op = .35 + .45 * t
        # riser and tread of the step, slight 3/4 depth
        out += (f'<path d="M{x} {y + h} L{x} {y} L{x + w} {y} L{x + w + 26} {y - 14} L{x + 26} {y - 14} L{x} {y}" fill="{col}" fill-opacity="{.55 + op * .35:.2f}" '
                f'stroke="#ffffff" stroke-opacity=".95" stroke-width="5" stroke-linejoin="round"/>')
        out += f'<path d="M{x} {y + h} L{x} {y}" stroke="#3d66b0" stroke-width="3" opacity="{.45 + .5 * t:.2f}"/>'
    # stringer under the steps
    out += f'<path d="M{x0} {y0} L{x0 + n * w} {y0 - n * h}" stroke="#bfefff" stroke-width="2.5" opacity=".45" stroke-dasharray="10 9"/>'
    return out, (x0 + n * w, y0 - n * h)


def door(bx, by):
    # arched door standing in the wall; base centre at (bx, by), leaf swung inward-left
    W, H = 150, 250
    x, y = bx - 10, by - H
    d = rad('doorHalo', bx + 60, by - 120, 420, [(0, '#ffe7a8', .75), (.25, '#F2D27A', .35), (.6, '#ff9a6a', .08), (1, '#000', 0)])
    d += rad('doorIn', bx + 60, by - 110, 190, [(0, '#ffffff', 1), (.35, '#fff3c6', 1), (.8, '#F2D27A', 1), (1, '#e6a24a', 1)])
    o = f'<circle cx="{bx + 60}" cy="{by - 120}" r="420" fill="url(#doorHalo)"/>'
    arch = f'M{x} {by} L{x} {y + 70} A{W / 2} {W / 2 + 10} 0 0 1 {x + W} {y + 70} L{x + W} {by} Z'
    # frame (thick ink + gold trim)
    o += f'<path d="{arch}" fill="url(#doorIn)" stroke="#140c18" stroke-width="16"/>'
    o += f'<path d="{arch}" fill="none" stroke="#F2D27A" stroke-width="6"/>'
    # a tiny red-shifted spiral seen through the doorway (the galaxies beyond the horizon)
    o += f'<g transform="translate({x + W * .4} {y + 120}) rotate(-25) scale(1 .5)" opacity=".8">'
    o += '<ellipse rx="40" ry="26" fill="#ff9a6a" opacity=".45"/>'
    o += '<path d="M0 0 q34 -8 30 22 M0 0 q-34 8 -30 -22" fill="none" stroke="#e0624a" stroke-width="7" stroke-linecap="round"/>'
    o += '<circle r="8" fill="#fff"/></g>'
    # open leaf, swung toward us on the left hinge
    o += (f'<path d="M{x + W} {by} L{x + W - 40} {by - 22} L{x + W - 40} {y + 64} Q{x + W - 28} {y + 30} {x + W} {y + 66} Z" fill="#3a2f6e" '
          f'stroke="#140c18" stroke-width="6" stroke-linejoin="round"/>')
    o += f'<circle cx="{x + W - 30}" cy="{by - 120}" r="5" fill="#F2D27A" stroke="#140c18" stroke-width="2"/>'
    o += f'<path d="M{x + 8} {by - 2} H{x + W - 44}" stroke="#fff" stroke-width="5" opacity=".7"/>'
    # light spilling down the stairs
    o += (f'<polygon points="{x + 4},{by} {x + W - 4},{by} {x - 130},{HZ} {x - 300},{HZ}" fill="#ffe7a8" opacity=".10" filter="url(#blur12)"/>')
    return d, o


def make_D():
    rnd = random.Random(31)
    d = SOFT
    d += lin('dBg', [(0, '#141a52'), (.3, '#24357e'), (.52, '#3d66b0'), (.64, '#78b6e0'), (.7, '#f6e2c4'), (.72, '#f6e2c4'), (1, '#0b1630')])
    body = '<rect width="1920" height="1080" fill="url(#dBg)"/>'
    # faint nebula washes (behind the wall)
    d += rad('neb1', 1250, 260, 620, [(0, '#6a62d8', .30), (.5, '#4a4fb0', .10), (1, '#000', 0)])
    d += rad('neb2', 380, 700, 600, [(0, '#ffffff', .10), (1, '#000', 0)])
    body += '<rect width="1920" height="1080" fill="url(#neb1)"/><rect width="1920" height="1080" fill="url(#neb2)"/>'
    body += grain(rnd, 1000, '#ffffff', .08)
    body += starfield(rnd, 300, (0, 0, 1920, 500), corner, '#ffffff')
    body += starfield(rnd, 60, (0, 500, 1920, 600), corner, '#ffffff')
    # galaxies beyond the horizon: the farther, the redder and smaller
    for _ in range(26):
        x, y = rnd.randint(980, 1900), rnd.randint(30, HZ - 40)
        if 1440 < x < 1800 and 120 < y < 560: continue   # keep the door clear
        col = rnd.choice(['#ffb08a', '#ff8a6a', '#e06a5a', '#ffd2a0'])
        body += small_gal(rnd, x, y, rnd.uniform(6, 15), col, rnd.choice('es'))
    for _ in range(10):
        x, y = rnd.randint(60, 900), rnd.randint(620, HZ - 30)
        body += small_gal(rnd, x, y, rnd.uniform(6, 12), rnd.choice(['#ffffff', '#fff2d8']), rnd.choice('es'))
    gd, gb = galaxy(1180, 250, 175, .42, -16, '#fff0c8', '#b7a4ff', '#ff9ecf', '#ffb08a', arms=2, n=260, seed=17, gid='gD')
    d += gd; body += gb
    g2d, g2b = galaxy(1820, 640, 60, .5, 28, '#ffe2c0', '#ff9a7a', '#ffc0a0', '#ffd8b0', arms=2, n=80, seed=19, gid='gD2')
    d += g2d; body += g2b
    for (cx_, cy_, rx_) in ((420, 700, 260), (980, 715, 200), (1720, 690, 230), (180, 640, 120)):
        body += f'<ellipse cx="{cx_}" cy="{cy_}" rx="{rx_}" ry="{rx_ * .28:.0f}" fill="#ffffff" opacity=".35" filter="url(#blur30)"/>'
    # horizon glow line
    body += f'<rect x="0" y="{HZ - 70}" width="1920" height="90" fill="#ff9ec4" opacity=".16" filter="url(#blur30)"/>'
    # ---- the invisible wall: curved grid with a glassy sheen ----
    gp = wall_grid()
    d += ('<linearGradient id="sheen" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#9fe6ff" stop-opacity="0"/>'
          '<stop offset=".6" stop-color="#9fe6ff" stop-opacity=".04"/><stop offset="1" stop-color="#9fe6ff" stop-opacity=".10"/></linearGradient>')
    body += f'<rect width="1920" height="{HZ}" fill="url(#sheen)"/>'
    body += f'<path d="{gp}" fill="none" stroke="#1a2550" stroke-width="6" opacity=".22"/>'
    body += f'<path d="{gp}" fill="none" stroke="#aebcd8" stroke-width="2.8" opacity=".45"/>'
    # brighter where the rocket touches it (masked copy)
    tx, ty = 1290, 700
    d += rad('touchM', tx, ty, 560, [(0, '#fff', 1), (.5, '#fff', .35), (1, '#fff', 0)])
    d += f'<mask id="touchMask"><rect width="1920" height="1080" fill="url(#touchM)"/></mask>'
    body += f'<g mask="url(#touchMask)"><path d="{gp}" fill="none" stroke="#e6eefa" stroke-width="3.4" opacity=".8"/></g>'
    # ---- nebula sea below the horizon ----
    sd, so = cloud_sea(rnd)
    d += sd
    body += so
    body += f'<rect x="0" y="{HZ - 3}" width="1920" height="5" fill="#fff3dc" opacity=".8"/>'
    body += f'<ellipse cx="1560" cy="{HZ + 40}" rx="300" ry="46" fill="#ffe2a0" opacity=".25" filter="url(#blur30)"/>'
    body += ''.join(f'<circle cx="{rnd.randint(0, 1540)}" cy="{rnd.randint(HZ + 20, 1060)}" r="{rnd.choice([1.2, 1.8])}" fill="#cfe0f5" opacity="{rnd.uniform(.2, .5):.2f}"/>' for _ in range(20))
    # ---- stairs and the door ----
    st, (dx, dy) = stairs()
    dd, do = door(dx + 34, dy + 2)
    d += dd
    body += do + st
    # ---- ripples where the nose touches the wall ----
    d += f'<clipPath id="wallClip"><rect width="1920" height="{HZ}"/></clipPath>'
    body += '<g clip-path="url(#wallClip)">'
    for k, r in enumerate((26, 54, 88, 128, 172)):
        body += (f'<ellipse cx="{tx}" cy="{ty}" rx="{r * .55:.0f}" ry="{r}" fill="none" stroke="#dff8ff" stroke-width="{4 - k * .5:.1f}" '
                 f'opacity="{.9 - k * .16:.2f}" stroke-dasharray="{"none" if k < 2 else "18 12"}"/>')
    body += f'<circle cx="{tx}" cy="{ty}" r="70" fill="#bff3ff" opacity=".45" filter="url(#blur12)"/></g>'
    # ---- the rocket ----
    d += lin('hull', [(0, '#ffffff'), (.35, '#eef0f8'), (.8, '#b4bcd4'), (1, '#7a84a6')])
    d += lin('nose', [(0, '#ffffff'), (.4, '#eef0f8'), (.85, '#b4bcd4'), (1, '#7a84a6')])
    d += rad('port', -250, -10, 34, [(0, '#bff3ff', 1), (.6, '#4aa8d8', 1), (1, '#1b4a78', 1)])
    body += f'<ellipse cx="1000" cy="{HZ + 52}" rx="320" ry="26" fill="#000" opacity=".45" filter="url(#blur12)"/>'
    body += f'<ellipse cx="1000" cy="{HZ + 30}" rx="420" ry="24" fill="#cfe6ff" opacity=".18" filter="url(#blur12)"/>'
    body += rocket(tx, ty, 1.0)
    # rim light from the door on the rocket's top
    body += f'<path d="M{tx - 470} {ty - 70} L{tx - 140} {ty - 70} Q{tx - 70} {ty - 70} {tx - 20} {ty - 34}" fill="none" stroke="#ffe7a8" stroke-width="5" opacity=".7"/>'
    # frog riding on top, bubble helmet, one hand pressed flat against the wall in front of it
    fx, fy = 1010, ty - 66
    body += frog(fx, fy, 2.25, look=(5, -4), mouth='o', helmet=True,
                 armR='M38 -22 q26 -14 44 -40', armL='M-34 -22 q-14 6 -12 24', feet=((-26, 4, -10), (24, 6, 14)))
    body += spark(fx + 2.25 * 84, fy - 2.25 * 64, 14, '#e9fbff', .9)
    body += spark(1460, 90, 20) + spark(960, 130, 16, '#ffe8f2', .8) + spark(1830, 140, 18) + spark(1040, 560, 12, '#e9fbff', .7)
    lines = [('VISIBLE,', 132, 'w'), ('NEVER', 236, 'y'), ('VISITED', 150, 'w')]
    return page('#141a52', svg(d, body), lines, outline='#0a1030')


if __name__ == '__main__':
    open(os.path.join(HERE, 'D.html'), 'w').write(make_D())
    print('wrote D')
