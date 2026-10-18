# Thumbnails for left-handed-ten-percent (guideline 16-6, brief tools/briefs/thumb_art.md, 2026-10-18 v2)
# A  intuitive / odd-one-out ("Where's Waldo"-style): a lecture hall of hands up, nine right arms, one left arm in the spotlight  (S01)
# B  film homage: ROCKY (1976) - the boxer at the top of the museum steps, arms up at sunrise; the left glove glows  (S27 southpaws)
# C  intuitive: an Ice Age artist presses a left hand on a torch-lit wall covered in mostly left-hand stencils  (S03)
import sys, math, random
sys.path.insert(0, '/home/user/rp/tools')
from thumb_lib import *
from hands import hand
from body import arm, shoulders, P

GLOW = '<filter id="bl{0}" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="{0}"/></filter>'
def blur(*s): return ''.join(GLOW.format(v) for v in s)


def _v(a):
    a = math.radians(a); return math.sin(a), math.cos(a)


def wrist(sx, sy, H, upper, bend, bdir, kind='cute'):
    p = P[kind]; ux, uy = _v(upper); E = (sx + ux * p['upper'] * H, sy + uy * p['upper'] * H)
    fa = upper + bend * (1 if bdir >= 0 else -1); fx, fy = _v(fa)
    return (E[0] + fx * p['fore'] * H, E[1] + fy * p['fore'] * H), fa


# =====================================================================================================
# A: ONE LEFT HAND IN A HALL OF RIGHT HANDS
random.seed(11)
LINE = '#171a2c'


def person(cx, top, H, raise_side, shirt, skin, hair, style, lw=None):
    lw = lw or H * 0.05
    out = ''
    if style == 'long':
        out += f'<ellipse cx="{cx}" cy="{top + .62 * H:.1f}" rx="{.56 * H:.1f}" ry="{.66 * H:.1f}" fill="{hair}" stroke="{LINE}" stroke-width="{lw:.1f}"/>'
    out += f'<rect x="{cx - .78 * H:.1f}" y="{top + 1.08 * H:.1f}" width="{1.56 * H:.1f}" height="{1080 - top:.1f}" rx="{.42 * H:.1f}" fill="{shirt}" stroke="{LINE}" stroke-width="{lw:.1f}"/>'
    out += f'<path d="M{cx - .22 * H:.1f},{top + 1.1 * H:.1f} Q{cx:.1f},{top + 1.38 * H:.1f} {cx + .22 * H:.1f},{top + 1.1 * H:.1f}" fill="none" stroke="{LINE}" stroke-width="{lw * .8:.1f}" opacity=".5"/>'
    (lx, ly), (rx, ry) = shoulders(cx, top, H)
    if raise_side == 'R':   # the person's right arm is on the viewer's left
        out += arm(lx, ly, H, upper=-166, bend=10, bend_dir=-1, side='R', view='palm', pose='flat', sleeve=shirt, skin=skin, line=LINE, fingers=True, lw=lw)
        out += arm(rx, ry, H, upper=8, bend=10, bend_dir=1, side='L', sleeve=shirt, skin=skin, line=LINE, lw=lw)
    else:
        out += arm(rx, ry, H, upper=166, bend=10, bend_dir=1, side='L', view='palm', pose='flat', sleeve=shirt, skin=skin, line=LINE, fingers=True, lw=lw)
        out += arm(lx, ly, H, upper=-8, bend=10, bend_dir=-1, side='R', sleeve=shirt, skin=skin, line=LINE, lw=lw)
    hy = top + .55 * H
    out += f'<rect x="{cx - .14 * H:.1f}" y="{top + .9 * H:.1f}" width="{.28 * H:.1f}" height="{.3 * H:.1f}" fill="{skin}" stroke="{LINE}" stroke-width="{lw:.1f}"/>'
    out += f'<ellipse cx="{cx}" cy="{hy:.1f}" rx="{.46 * H:.1f}" ry="{.5 * H:.1f}" fill="{skin}" stroke="{LINE}" stroke-width="{lw:.1f}"/>'
    if style in ('short', 'long'):
        out += (f'<path d="M{cx - .47 * H:.1f},{hy + .02 * H:.1f} C{cx - .52 * H:.1f},{top - .12 * H:.1f} {cx + .52 * H:.1f},{top - .12 * H:.1f} {cx + .47 * H:.1f},{hy + .02 * H:.1f} '
                f'Q{cx + .25 * H:.1f},{top + .22 * H:.1f} {cx - .05 * H:.1f},{top + .3 * H:.1f} Q{cx - .32 * H:.1f},{top + .32 * H:.1f} {cx - .47 * H:.1f},{hy + .02 * H:.1f}Z" fill="{hair}" stroke="{LINE}" stroke-width="{lw:.1f}"/>')
    elif style == 'bun':
        out += f'<circle cx="{cx}" cy="{top - .05 * H:.1f}" r="{.2 * H:.1f}" fill="{hair}" stroke="{LINE}" stroke-width="{lw:.1f}"/>'
        out += (f'<path d="M{cx - .47 * H:.1f},{hy:.1f} C{cx - .5 * H:.1f},{top - .08 * H:.1f} {cx + .5 * H:.1f},{top - .08 * H:.1f} {cx + .47 * H:.1f},{hy:.1f} '
                f'Q{cx:.1f},{top + .18 * H:.1f} {cx - .47 * H:.1f},{hy:.1f}Z" fill="{hair}" stroke="{LINE}" stroke-width="{lw:.1f}"/>')
    else:   # curly
        for k in range(7):
            a = math.radians(-170 + k * 27); out += f'<circle cx="{cx + math.cos(a) * .42 * H:.1f}" cy="{hy - .08 * H + math.sin(a) * .42 * H:.1f}" r="{.17 * H:.1f}" fill="{hair}" stroke="{LINE}" stroke-width="{lw * .8:.1f}"/>'
    ey = hy + .08 * H
    out += ''.join(f'<ellipse cx="{cx + s * .17 * H:.1f}" cy="{ey:.1f}" rx="{.045 * H:.1f}" ry="{.06 * H:.1f}" fill="{LINE}"/>' for s in (-1, 1))
    out += ''.join(f'<circle cx="{cx + s * .28 * H:.1f}" cy="{ey + .12 * H:.1f}" r="{.07 * H:.1f}" fill="#ff8f86" opacity=".45"/>' for s in (-1, 1))
    out += f'<path d="M{cx - .1 * H:.1f},{ey + .15 * H:.1f} Q{cx:.1f},{ey + .25 * H:.1f} {cx + .1 * H:.1f},{ey + .15 * H:.1f}" fill="none" stroke="{LINE}" stroke-width="{lw * .9:.1f}" stroke-linecap="round"/>'
    return out


d = (lin('wall', [(0, '#141b36'), (.6, '#1f2a4d'), (1, '#2a2440')]) + lin('desk', [(0, '#6b4430'), (.12, '#4a2c1f'), (1, '#1e110b')])
     + rad('dim', 1745, 560, 1150, [(0, '#0a0f22', 0), (.16, '#0a0f22', 0), (.3, '#0a0f22', .5), (1, '#0a0f22', .62)])
     + rad('spot', 1745, 560, 430, [(0, '#ffe6a0', .55), (.5, '#ffd27a', .22), (1, '#ffd27a', 0)])
     + rad('hglow', 1858, 420, 200, [(0, '#fff2c0', .95), (.4, '#F2D27A', .5), (1, '#F2D27A', 0)])
     + '<linearGradient id="cn" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff3cc" stop-opacity=".42"/><stop offset="1" stop-color="#ffe2a0" stop-opacity=".05"/></linearGradient>'
     + blur(6, 18))
b = '<rect width="1920" height="1080" fill="url(#wall)"/>'
b += '<rect x="560" y="150" width="1300" height="300" rx="12" fill="#18322e" stroke="#3a2a20" stroke-width="16" opacity=".75"/>'
b += '<path d="M640 260 q60 -30 120 0 t120 0 M1500 330 l160 -40 M1520 380 l120 -30" stroke="#b9d3c8" stroke-width="5" fill="none" opacity=".18" stroke-linecap="round"/>'
b += '<circle cx="1740" cy="300" r="48" fill="none" stroke="#b9d3c8" stroke-width="5" opacity=".14"/>'
b += stars(26, 420, xmin=500, col='#cfe0ff', op=.25, sparks=0)
crowd_back = [(1075, '#6f86a8', '#e7b994', '#3b2a22', 'short'), (1255, '#a2736f', '#8a5a3c', '#1d1612', 'curly'),
              (1435, '#6c9a86', '#f1cdb0', '#a8662f', 'bun'), (1615, '#8a78ad', '#c78c62', '#2a1d18', 'long'), (1790, '#b49a5c', '#f0c8a6', '#5b3a26', 'short')]
for x, sh, sk, hr, st in crowd_back:
    b += person(x, 405, 88, 'R', sh, sk, hr, st)
crowd_front = [(905, '#c26a58', '#d9a37a', '#2a1d18', 'long'), (1110, '#4f7fa6', '#7a4e33', '#14100e', 'curly'),
               (1320, '#9a8a50', '#f2c9a6', '#6b4426', 'short'), (1530, '#5f8f6c', '#b67c55', '#1f1915', 'bun')]
for x, sh, sk, hr, st in crowd_front:
    b += person(x, 525, 116, 'R', sh, sk, hr, st)
b += '<rect width="1920" height="1080" fill="url(#dim)"/>'
b += '<path d="M1680 -10 L1880 -10 L1960 1000 L1520 1000Z" fill="url(#cn)" filter="url(#bl18)"/>'
b += '<rect width="1920" height="1080" fill="url(#spot)"/>'
b += '<circle cx="1858" cy="420" r="200" fill="url(#hglow)"/>'
b += person(1745, 512, 124, 'L', '#2fa39a', '#f0c49c', '#3a2418', 'short')
b += '<rect x="0" y="930" width="1920" height="150" fill="url(#desk)"/><path d="M0 932 H1920" stroke="#a87552" stroke-width="5" opacity=".7"/>'
b += '<g opacity=".9"><rect x="1250" y="902" width="190" height="34" rx="4" fill="#efe7d6" stroke="#171a2c" stroke-width="4" transform="rotate(-4 1345 917)"/><path d="M1270 914 L1430 904" stroke="#7a8db0" stroke-width="3" transform="rotate(-4 1345 917)"/></g>'
b += spark(1760, 300, 26) + spark(1880, 250, 14) + spark(1690, 420, 14) + spark(1840, 560, 12)
open('A.html', 'w', encoding='utf-8').write(page('#141b36', svg(d, b), [('WHY ONLY', 150, 'w'), ('1 IN 10?', 270, 'y')], '#0b0f22'))

# =====================================================================================================
# B: ROCKY homage - the steps at sunrise, the LEFT glove raised and glowing
random.seed(5)
d = (lin('sky', [(0, '#251d4a'), (.35, '#5d3566'), (.62, '#c85e66'), (.82, '#f59a5e'), (1, '#ffd08a')])
     + rad('sun', 1420, 330, 175, [(0, '#fffbe6', 1), (.6, '#ffe7a6', 1), (1, '#ffc46e', 1)])
     + rad('sunglow', 1420, 330, 720, [(0, '#ffd890', .85), (.35, '#ff9e62', .35), (1, '#ff9e62', 0)])
     + rad('gglow', 1500, 160, 170, [(0, '#fff3c4', .95), (.45, '#F2D27A', .5), (1, '#F2D27A', 0)])
     + '<linearGradient id="shade" x1="0" y1="0" x2="0" y2="1"><stop offset=".55" stop-color="#140a1a" stop-opacity="0"/><stop offset="1" stop-color="#140a1a" stop-opacity=".62"/></linearGradient>'
     + lin('plaza', [(0, '#e7a98e'), (1, '#9c5f6c')]) + blur(4, 10))
b = '<rect width="1920" height="1080" fill="url(#sky)"/>' + stars(30, 260, col='#ffe9f0', op=.35, sparks=0)
b += '<rect width="1920" height="1080" fill="url(#sunglow)"/>'
b += blobs(9, 300, 120, 1900, 300, '#ffd2c0', .08, .18, 90, 240)
b += '<circle cx="1420" cy="330" r="175" fill="url(#sun)"/>'


def wing(x0, x1, ytop, ybot, n, col='#e3a596'):
    w = x1 - x0; o = '<g opacity=".78">'
    o += f'<path d="M{x0 - 20} {ytop} L{(x0 + x1) / 2} {ytop - 70} L{x1 + 20} {ytop}Z" fill="{col}" stroke="#7d4a5e" stroke-width="4"/>'
    o += f'<path d="M{x0 + 40} {ytop - 10} L{(x0 + x1) / 2} {ytop - 52} L{x1 - 40} {ytop - 10}Z" fill="#c98185"/>'
    o += f'<rect x="{x0 - 26}" y="{ytop}" width="{w + 52}" height="26" fill="{col}" stroke="#7d4a5e" stroke-width="4"/>'
    for k in range(n):
        cx = x0 + 20 + k * (w - 40) / (n - 1)
        o += f'<rect x="{cx - 17:.0f}" y="{ytop + 26}" width="34" height="{ybot - ytop - 46}" fill="{col}" stroke="#7d4a5e" stroke-width="3"/>'
        o += f'<rect x="{cx + 4:.0f}" y="{ytop + 26}" width="13" height="{ybot - ytop - 46}" fill="#b0707c" opacity=".7"/>'
        o += f'<rect x="{cx - 23:.0f}" y="{ybot - 22}" width="46" height="14" fill="{col}" stroke="#7d4a5e" stroke-width="3"/>'
    o += f'<rect x="{x0 - 30}" y="{ybot - 10}" width="{w + 60}" height="16" fill="#c98a8a" stroke="#7d4a5e" stroke-width="3"/></g>'
    return o


b += wing(830, 1150, 400, 610, 5) + wing(1700, 2010, 400, 610, 5)
b += '<rect x="560" y="600" width="1400" height="44" fill="url(#plaza)"/><path d="M560 600 H1960" stroke="#ffd1a6" stroke-width="4" opacity=".7"/>'
cx0, n = 1420, 15
ys = [644 + 436 * (k / n) ** 1.3 for k in range(n + 1)]
def hw(y): return 250 + (y - 644) / 436 * 330
for k in range(n):
    y0, y1 = ys[k], ys[k + 1]; t = y0 + (y1 - y0) * .38
    a0, a1 = hw(y0), hw(y1)
    b += f'<path d="M{cx0 - a0:.0f} {y0:.0f} L{cx0 + a0:.0f} {y0:.0f} L{cx0 + a0 + (a1 - a0) * .38:.0f} {t:.0f} L{cx0 - a0 - (a1 - a0) * .38:.0f} {t:.0f}Z" fill="#c98493"/>'
    b += f'<path d="M{cx0 - a0 - (a1 - a0) * .38:.0f} {t:.0f} L{cx0 + a0 + (a1 - a0) * .38:.0f} {t:.0f} L{cx0 + a1:.0f} {y1:.0f} L{cx0 - a1:.0f} {y1:.0f}Z" fill="#62364f"/>'
    b += f'<path d="M{cx0 - a0:.0f} {y0:.0f} L{cx0 + a0:.0f} {y0:.0f}" stroke="#ffc9a6" stroke-width="3" opacity=".55"/>'
for s in (-1, 1):
    b += f'<path d="M{cx0 + s * 250} 600 L{cx0 + s * 300} 600 L{cx0 + s * 650} 1080 L{cx0 + s * 580} 1080Z" fill="#7f4a62" stroke="#4a2638" stroke-width="4"/>'
    b += f'<path d="M{cx0 + s * 250} 600 L{cx0 + s * 300} 600" stroke="#ffc9a6" stroke-width="5"/>'
    b += f'<rect x="{cx0 + s * 275 - 34}" y="560" width="68" height="44" fill="#a36676" stroke="#4a2638" stroke-width="4"/>'
b += '<rect width="1920" height="1080" fill="url(#shade)"/>'
H, bx, feet = 92, 1420, 650
top = feet - 5.5 * H
RIM, BODY, SKIN = '#ffb16e', '#3a2236', '#5b3540'
hip = top + 2.75 * H
g = f'<g filter="url(#bl10)" opacity=".7"><ellipse cx="{bx}" cy="{(top + feet) / 2:.0f}" rx="{1.4 * H:.0f}" ry="{2.9 * H:.0f}" fill="#ffd28a"/></g>'
for s in (-1, 1):
    g += f'<path d="M{bx + s * .12 * H:.0f} {hip:.0f} L{bx + s * .62 * H:.0f} {hip:.0f} L{bx + s * .72 * H:.0f} {feet - 18:.0f} L{bx + s * .2 * H:.0f} {feet - 18:.0f}Z" fill="{SKIN}" stroke="{RIM}" stroke-width="4" stroke-linejoin="round"/>'
    g += f'<path d="M{bx + s * .14 * H:.0f} {feet - 40:.0f} L{bx + s * .76 * H:.0f} {feet - 40:.0f} Q{bx + s * .95 * H:.0f} {feet:.0f} {bx + s * .7 * H:.0f} {feet:.0f} L{bx + s * .14 * H:.0f} {feet:.0f}Z" fill="#2a1828" stroke="{RIM}" stroke-width="4"/>'
g += f'<path d="M{bx - .8 * H:.0f} {hip - .25 * H:.0f} L{bx + .8 * H:.0f} {hip - .25 * H:.0f} L{bx + .9 * H:.0f} {hip + .95 * H:.0f} L{bx + .05 * H:.0f} {hip + .95 * H:.0f} L{bx:.0f} {hip + .55 * H:.0f} L{bx - .05 * H:.0f} {hip + .95 * H:.0f} L{bx - .9 * H:.0f} {hip + .95 * H:.0f}Z" fill="#4a2a44" stroke="{RIM}" stroke-width="4" stroke-linejoin="round"/>'
g += f'<rect x="{bx - .82 * H:.0f}" y="{hip - .3 * H:.0f}" width="{1.64 * H:.0f}" height="{.2 * H:.0f}" rx="6" fill="#6a3a50" stroke="{RIM}" stroke-width="3"/>'
(lx, ly), (rx, ry) = shoulders(bx, top, H)
for sx, sy, up, bd, glove in ((lx, ly, -150, -1, '#7a2630'), (rx, ry, 150, 1, '#e8443c')):
    lit = glove == '#e8443c'; gl = '#3a1018' if lit else RIM
    g += arm(sx, sy, H, upper=up, bend=12, bend_dir=bd, sleeve=SKIN, skin=SKIN, line=RIM, sleeve_len='short', lw=4)
    (wx, wy), fa = wrist(sx, sy, H, up, 12, bd)
    ux, uy = _v(fa); gx, gy = wx + ux * .42 * H, wy + uy * .42 * H; rot = 180 - fa
    if lit:
        g += f'<circle cx="{gx:.0f}" cy="{gy:.0f}" r="170" fill="url(#gglow)"/>'
    g += f'<g transform="translate({gx:.1f} {gy:.1f}) rotate({rot:.1f})">'
    g += f'<rect x="{-.3 * H:.1f}" y="{.3 * H:.1f}" width="{.6 * H:.1f}" height="{.3 * H:.1f}" rx="6" fill="#f2efe6" stroke="{gl}" stroke-width="4"/>'
    g += f'<ellipse cx="0" cy="0" rx="{.5 * H:.1f}" ry="{.56 * H:.1f}" fill="{glove}" stroke="{gl}" stroke-width="5"/>'
    th = -1 if lit else 1
    g += f'<ellipse cx="{th * .42 * H:.1f}" cy="{.12 * H:.1f}" rx="{.16 * H:.1f}" ry="{.28 * H:.1f}" fill="{glove}" stroke="{gl}" stroke-width="4"/>'
    if lit:
        g += f'<ellipse cx="{-.18 * H:.1f}" cy="{-.22 * H:.1f}" rx="{.14 * H:.1f}" ry="{.22 * H:.1f}" fill="#ffd0b0" opacity=".75"/>'
    g += '</g>'
g += f'<path d="M{bx - .8 * H:.0f} {top + 1.25 * H:.0f} Q{bx:.0f} {top + 1.05 * H:.0f} {bx + .8 * H:.0f} {top + 1.25 * H:.0f} L{bx + .72 * H:.0f} {hip - .2 * H:.0f} L{bx - .72 * H:.0f} {hip - .2 * H:.0f}Z" fill="{BODY}" stroke="{RIM}" stroke-width="5" stroke-linejoin="round"/>'
g += f'<rect x="{bx - .16 * H:.0f}" y="{top + .88 * H:.0f}" width="{.32 * H:.0f}" height="{.3 * H:.0f}" fill="{SKIN}" stroke="{RIM}" stroke-width="4"/>'
g += f'<ellipse cx="{bx}" cy="{top + .52 * H:.0f}" rx="{.44 * H:.0f}" ry="{.5 * H:.0f}" fill="{SKIN}" stroke="{RIM}" stroke-width="5"/>'
g += f'<path d="M{bx - .45 * H:.0f} {top + .45 * H:.0f} C{bx - .48 * H:.0f} {top - .1 * H:.0f} {bx + .48 * H:.0f} {top - .1 * H:.0f} {bx + .45 * H:.0f} {top + .45 * H:.0f} Q{bx:.0f} {top + .2 * H:.0f} {bx - .45 * H:.0f} {top + .45 * H:.0f}Z" fill="#24131f"/>'
b += g
b += spark(1760, 70, 28) + spark(1560, 40, 16) + spark(1800, 250, 14) + spark(1660, 300, 11)
for x, y in ((1150, 300), (1195, 275), (1860, 330)):
    b += f'<path d="M{x - 14} {y} q7 -8 14 0 q7 -8 14 0" stroke="#3a2236" stroke-width="3.5" fill="none" stroke-linecap="round"/>'
open('B.html', 'w', encoding='utf-8').write(page('#251d4a', svg(d, b), [('THE', 110, 'w'), ('SOUTHPAW', 190, 'y'), ('ADVANTAGE', 150, 'w')], '#1a0f24'))

# =====================================================================================================
# C: THE CAVE WALL - an Ice Age artist presses a LEFT hand among mostly left-hand stencils
random.seed(21)
TX, TY = 1318, 352   # torch flame (above the artist's right hand)
d = (rad('wall', TX, TY + 80, 1250, [(0, '#e7a462', 1), (.22, '#b8703c', 1), (.5, '#6e3a20', 1), (1, '#1b0c07', 1)])
     + rad('torch', TX, TY, 520, [(0, '#ffe9a8', .7), (.25, '#ffb054', .32), (1, '#ff8a30', 0)])
     + rad('flame', TX, TY - 10, 70, [(0, '#fffbe0', 1), (.5, '#ffd36a', 1), (1, '#ff7a22', 1)])
     + lin('floor', [(0, '#3a1d10'), (1, '#120704')]) + blur(4, 9, 14, 26))
b = '<rect width="1920" height="1080" fill="url(#wall)"/>'
for x, y, rx_, ry_ in ((1650, 330, 300, 200), (900, 820, 330, 180), (1320, 160, 260, 120), (420, 700, 260, 220), (1780, 760, 220, 160)):
    dx = (x - TX) / max(1, abs(x - TX)) * 22
    b += f'<ellipse cx="{x + dx:.0f}" cy="{y + 18}" rx="{rx_}" ry="{ry_}" fill="#2a1209" opacity=".22" filter="url(#bl26)"/>'
    b += f'<ellipse cx="{x - dx:.0f}" cy="{y - 10}" rx="{rx_ * .8:.0f}" ry="{ry_ * .7:.0f}" fill="#f0b47a" opacity=".12" filter="url(#bl26)"/>'
STN = [  # (x, y, size, side, angle, strength)  left hands seen on the wall = back-of-left-hand outline (thumb to the viewer's right)
    (1640, 470, 150, 'L', 12, 1), (1795, 255, 112, 'L', 22, .85), (1505, 240, 104, 'L', -10, .9), (1635, 820, 112, 'L', -16, .75),
    (1835, 600, 96, 'L', 28, .7), (560, 820, 100, 'L', 8, .6),
    (1240, 225, 96, 'R', -6, .8), (905, 900, 92, 'R', -18, .55)]
PIG = '#a8301f'
for i, (x, y, s, side, a, st) in enumerate(STN):
    shape = hand(x, y, a, s, side, 'back', 'open', '#000', '#000', lw=1, creases=False)
    d += f'<mask id="m{i}" maskUnits="userSpaceOnUse" x="0" y="0" width="1920" height="1080"><rect width="1920" height="1080" fill="#fff"/>{shape}</mask>'
    halo = hand(x, y, a, s, side, 'back', 'open', PIG, PIG, lw=s * .36, creases=False)
    b += f'<g mask="url(#m{i})"><g filter="url(#bl14)" opacity="{.95 * st:.2f}">{halo}</g></g>'
    b += f'<g mask="url(#m{i})"><g filter="url(#bl4)" opacity="{.35 * st:.2f}">{hand(x, y, a, s, side, "back", "open", "#5e1810", "#5e1810", lw=s * .08, creases=False)}</g></g>'
b += blobs(260, 0, 0, 1920, 1000, '#1a0a05', .03, .09, 10, 54) + blobs(170, 0, 0, 1920, 1000, '#f2c08a', .03, .07, 6, 30)
b += ''.join(f'<path d="M{x} {y} q{random.randint(-60, 60)} {random.randint(40, 120)} {random.randint(-40, 40)} {random.randint(140, 260)}" stroke="#1a0a05" stroke-width="{random.choice([2, 3, 4])}" fill="none" opacity=".3"/>' for x, y in [(random.randint(0, 1900), random.randint(0, 760)) for _ in range(12)])
H, cx = 104, 1150
top = 1050 - 5.5 * H
(lx, ly), (rx, ry) = shoulders(cx, top, H)
(hx, hy), hfa = wrist(lx, ly, H, -146, 18, -1)
b += f'<g filter="url(#bl9)" opacity=".9">{hand(hx, hy, 180 - hfa, P["cute"]["palm"] * H, "L", "back", "flat", "#d23a22", "#d23a22", lw=16, creases=False)}</g>'
b += '<rect width="1920" height="1080" fill="url(#torch)"/>'
b += '<path d="M0 1010 Q500 975 960 995 T1920 990 V1080 H0Z" fill="url(#floor)"/>'
b += blobs(30, 0, 1000, 1700, 1075, '#5a3018', .2, .4, 10, 34)
LN, SK, FUR, HAIR = '#1e0e07', '#b77650', '#7a5232', '#2a170d'
p = ''
hip = top + 2.75 * H
for s in (-1, 1):
    p += f'<rect x="{cx + s * .38 * H - .24 * H:.0f}" y="{hip:.0f}" width="{.48 * H:.0f}" height="{1050 - hip:.0f}" rx="{.2 * H:.0f}" fill="{SK}" stroke="{LN}" stroke-width="4"/>'
    p += f'<ellipse cx="{cx + s * .42 * H:.0f}" cy="1050" rx="{.36 * H:.0f}" ry="{.14 * H:.0f}" fill="#5a3520" stroke="{LN}" stroke-width="4"/>'
p += arm(lx, ly, H, upper=-146, bend=18, bend_dir=-1, side='L', view='back', pose='flat', sleeve=FUR, skin=SK, line=LN, sleeve_len='short', fingers=True, lw=4)
p += arm(rx, ry, H, upper=150, bend=14, bend_dir=1, side='R', sleeve=FUR, skin=SK, line=LN, sleeve_len='short', lw=4)
(tx0, ty0), tfa = wrist(rx, ry, H, 150, 14, 1)
p += f'<path d="M{tx0 - 6:.0f} {ty0 + 40:.0f} L{TX - 8} {TY + 34} L{TX + 8} {TY + 34} L{tx0 + 10:.0f} {ty0 + 40:.0f}Z" fill="#4a2a16" stroke="{LN}" stroke-width="4"/>'
p += f'<circle cx="{tx0:.0f}" cy="{ty0 + 4:.0f}" r="{.16 * H:.0f}" fill="{SK}" stroke="{LN}" stroke-width="4"/>'
p += f'<path d="M{cx - .85 * H:.0f} {top + 1.2 * H:.0f} Q{cx:.0f} {top + 1.0 * H:.0f} {cx + .85 * H:.0f} {top + 1.2 * H:.0f} L{cx + .95 * H:.0f} {hip + .35 * H:.0f} L{cx + .5 * H:.0f} {hip + .55 * H:.0f} L{cx + .1 * H:.0f} {hip + .3 * H:.0f} L{cx - .35 * H:.0f} {hip + .6 * H:.0f} L{cx - .95 * H:.0f} {hip + .35 * H:.0f}Z" fill="{FUR}" stroke="{LN}" stroke-width="5" stroke-linejoin="round"/>'
p += ''.join(f'<ellipse cx="{cx + random.uniform(-.6, .6) * H:.0f}" cy="{top + random.uniform(1.4, 3.0) * H:.0f}" rx="{random.randint(6, 13)}" ry="{random.randint(4, 8)}" fill="#4a2e18" opacity=".7"/>' for _ in range(14))
p += f'<path d="M{cx + .85 * H:.0f} {top + 1.25 * H:.0f} Q{cx + .95 * H:.0f} {top + 2.2 * H:.0f} {cx + .92 * H:.0f} {hip + .3 * H:.0f}" stroke="#ffcf8a" stroke-width="6" fill="none" opacity=".55"/>'
p += f'<ellipse cx="{cx}" cy="{top + .55 * H:.0f}" rx="{.48 * H:.0f}" ry="{.52 * H:.0f}" fill="{HAIR}" stroke="{LN}" stroke-width="5"/>'
p += ''.join(f'<path d="M{cx + k * .12 * H:.0f} {top + .2 * H:.0f} q{k * 6} {.5 * H:.0f} {k * 3 + 4} {.95 * H:.0f}" stroke="#4a2c18" stroke-width="5" fill="none" stroke-linecap="round"/>' for k in range(-3, 4))
p += f'<path d="M{cx + .3 * H:.0f} {top + .1 * H:.0f} Q{cx + .5 * H:.0f} {top + .5 * H:.0f} {cx + .4 * H:.0f} {top + .95 * H:.0f}" stroke="#ffcf8a" stroke-width="6" fill="none" opacity=".6"/>'
b += p
b += f'<circle cx="{TX}" cy="{TY}" r="120" fill="#ffc260" opacity=".45" filter="url(#bl26)"/>'
b += f'<path d="M{TX} {TY - 92} C{TX + 30} {TY - 50} {TX + 52} {TY - 10} {TX + 34} {TY + 22} C{TX + 20} {TY + 44} {TX - 20} {TY + 44} {TX - 34} {TY + 22} C{TX - 50} {TY - 8} {TX - 20} {TY - 40} {TX} {TY - 92}Z" fill="url(#flame)"/>'
b += f'<path d="M{TX} {TY - 40} C{TX + 14} {TY - 16} {TX + 20} {TY + 6} {TX + 10} {TY + 22} C{TX + 2} {TY + 28} {TX - 12} {TY + 26} {TX - 14} {TY + 12} C{TX - 18} {TY - 6} {TX - 6} {TY - 22} {TX} {TY - 40}Z" fill="#fffbe8"/>'
b += ''.join(f'<circle cx="{TX + random.randint(-60, 60)}" cy="{TY - random.randint(70, 200)}" r="{random.choice([2, 3, 4])}" fill="#ffd27a" opacity="{random.uniform(.5, .95):.2f}"/>' for _ in range(16))
b += spark(1500, 380, 18) + spark(1720, 150, 14)
open('C.html', 'w', encoding='utf-8').write(page('#1b0c07', svg(d, b), [('3 OF 4', 250, 'y'), ('CAVE HANDS', 150, 'w'), ('ARE LEFT', 150, 'w')], '#1c0b05'))
print('ok')
