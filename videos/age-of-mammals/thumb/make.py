# age-of-mammals thumbnails A-C (guideline 16-6). run: python3 make.py  (writes A.html B.html C.html here)
# A  SMALL WAS A SUPERPOWER  intuitive: a shrew-sized mammal at its burrow looks up at the incoming fireball, sauropod silhouettes on the horizon
#    script S03, S05, S07, S11 ("Being small suddenly becomes the greatest superpower on Earth", "the size of a shrew").
# B  FROM SHREW TO YOU       homage: "The March of Progress" (Zallinger's famous walking line-up), redrawn as shrew -> early primate ->
#    ape -> hominin -> human, walking out of the ash into daylight with footprints. script S05, S11, S18, S36-S37, S49-S51.
# C  BRAINS ROUGHLY TRIPLED  homage: 2001: A Space Odyssey "Dawn of Man" (hominin among bones, arm raised, against the rising sun);
#    here the raised hand holds a stone tool over a cracked long bone with glowing marrow. script S36, S38 ("roughly triple").
import os, sys, math, random
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', '..', 'tools'))
from thumb_lib import *
from hands import hand

R = math.radians


def cap(x0, y0, x1, y1, w, col, op=1):
    return f'<line x1="{x0:.1f}" y1="{y0:.1f}" x2="{x1:.1f}" y2="{y1:.1f}" stroke="{col}" stroke-width="{w:.1f}" stroke-linecap="round" opacity="{op}"/>'


def taper(x0, y0, x1, y1, w0, w1, col):
    dx, dy = x1 - x0, y1 - y0; L = math.hypot(dx, dy) or 1; nx, ny = -dy / L, dx / L
    return (f'<path d="M{x0 + nx * w0 / 2:.1f},{y0 + ny * w0 / 2:.1f} L{x1 + nx * w1 / 2:.1f},{y1 + ny * w1 / 2:.1f} '
            f'A{w1 / 2:.1f},{w1 / 2:.1f} 0 0 0 {x1 - nx * w1 / 2:.1f},{y1 - ny * w1 / 2:.1f} L{x0 - nx * w0 / 2:.1f},{y0 - ny * w0 / 2:.1f} '
            f'A{w0 / 2:.1f},{w0 / 2:.1f} 0 0 0 {x0 + nx * w0 / 2:.1f},{y0 + ny * w0 / 2:.1f}Z" fill="{col}"/>')


def ik(h, f, a, b, fwd=1):
    dx, dy = f[0] - h[0], f[1] - h[1]; d = min(math.hypot(dx, dy), a + b - 0.5)
    base = math.atan2(dy, dx); al = math.acos(max(-1, min(1, (a * a + d * d - b * b) / (2 * a * d))))
    c = [(h[0] + a * math.cos(base + s * al), h[1] + a * math.sin(base + s * al)) for s in (1, -1)]
    return max(c, key=lambda p: p[0] * fwd)


def filt(n, col, dil=0, blur=0):
    s = f'<filter id="{n}" x="-30%" y="-30%" width="160%" height="160%"><feFlood flood-color="{col}" result="f"/><feComposite in="f" in2="SourceAlpha" operator="in" result="s"/>'
    if dil: s += f'<feMorphology in="s" operator="dilate" radius="{dil}" result="s"/>'
    if blur: s += f'<feGaussianBlur in="s" stdDeviation="{blur}"/>'
    return s + '</filter>'


def lit(gid, halo=None, rim=None, rdx=4, rdy=-3, extra=''):
    """draw <g id=gid> (in defs) with a soft halo, a rim-light sliver toward (rdx, rdy), and the dark figure on top"""
    s = ''
    if halo: s += f'<use href="#{gid}" filter="url(#{halo})" opacity=".9"/>'
    if rim: s += f'<use href="#{gid}" filter="url(#{rim})" transform="translate({rdx} {rdy})"/>'
    return s + f'<use href="#{gid}"/>' + extra


# ---------------- figures ----------------
def biped(x, fy, H, col, lean=4, stride=.20, arm=1.0, head=.068, jaw=0, hip=.49, a_near=(-24, -8), a_far=(22, 40), brow=0):
    """side-view walking figure facing +x; returns svg (all one colour, for silhouettes)"""
    s = ''; L1 = L2 = .255 * H
    hp = (x, fy - hip * H)
    ff = (x + stride * H * .5, fy - .035 * H); bf = (x - stride * H * .5, fy - .035 * H)
    for f in (bf, ff):
        k = ik(hp, f, L1, L2, 1)
        s += taper(*hp, *k, .10 * H, .072 * H, col) + taper(*k, *f, .068 * H, .044 * H, col)
        s += taper(f[0] - .025 * H, f[1] + .01 * H, f[0] + .085 * H, fy - .008 * H, .05 * H, .03 * H, col)
    sh = (hp[0] + math.sin(R(lean)) * .30 * H, hp[1] - math.cos(R(lean)) * .30 * H)
    tw = .15 if jaw else .125
    s += taper(*hp, *sh, tw * H, (tw + .01) * H, col)
    s += f'<ellipse cx="{(hp[0] + sh[0]) / 2 + .02 * H:.1f}" cy="{(hp[1] + sh[1]) / 2 - .03 * H:.1f}" rx="{(tw - .06) * H:.1f}" ry="{.13 * H:.1f}" fill="{col}" transform="rotate({lean} {(hp[0] + sh[0]) / 2:.1f} {(hp[1] + sh[1]) / 2:.1f})"/>'
    hr = head * H; na = R(lean + 14 + jaw * 40)
    hc = (sh[0] + math.sin(na) * (.045 * H + hr), sh[1] - math.cos(na) * (.045 * H + hr))
    s += taper(*sh, *hc, .06 * H, .055 * H, col)
    s += f'<circle cx="{hc[0]:.1f}" cy="{hc[1]:.1f}" r="{hr:.1f}" fill="{col}"/>'
    if jaw:   # protruding hominin face
        s += f'<ellipse cx="{hc[0] + hr * .75:.1f}" cy="{hc[1] + hr * .45:.1f}" rx="{hr * .62:.1f}" ry="{hr * .5:.1f}" fill="{col}"/>'
    else:     # nose + chin + hair
        s += f'<ellipse cx="{hc[0] - hr * .2:.1f}" cy="{hc[1] - hr * .35:.1f}" rx="{hr * 1.08:.1f}" ry="{hr * .82:.1f}" fill="{col}" transform="rotate(-15 {hc[0]:.1f} {hc[1]:.1f})"/>'
        s += f'<path d="M{hc[0] - hr * 1.1:.1f},{hc[1] - hr * .2:.1f} q{-hr * .2:.1f},{hr * .7:.1f} {hr * .25:.1f},{hr * 1.0:.1f}" stroke="{col}" stroke-width="{hr * .5:.1f}" fill="none" stroke-linecap="round"/>'
        s += f'<path d="M{hc[0] + hr * .85:.1f},{hc[1] - hr * .1:.1f} l{hr * .32:.1f},{hr * .42:.1f} l{-hr * .3:.1f},{hr * .08:.1f}Z" fill="{col}"/>'
        s += f'<ellipse cx="{hc[0] + hr * .55:.1f}" cy="{hc[1] + hr * .65:.1f}" rx="{hr * .42:.1f}" ry="{hr * .35:.1f}" fill="{col}"/>'
    if brow:
        s += f'<ellipse cx="{hc[0] + hr * .7:.1f}" cy="{hc[1] - hr * .25:.1f}" rx="{hr * .45:.1f}" ry="{hr * .22:.1f}" fill="{col}"/>'
    U, F = .17 * H * arm, .15 * H * arm
    for a1, a2 in (a_far, a_near):
        e = (sh[0] + math.sin(R(a1)) * U, sh[1] + math.cos(R(a1)) * U)
        w = (e[0] + math.sin(R(a2)) * F, e[1] + math.cos(R(a2)) * F)
        s += taper(*sh, *e, .065 * H, .05 * H, col) + taper(*e, *w, .05 * H, .036 * H, col)
        s += hand(w[0], w[1], 180 - a2, .055 * H, 'R', 'back', 'flat', skin=col, line=col, creases=False)
    return s


def quad(x, fy, L, col, h=.5, tail=(-.9, .1, -1.2, -.25), headr=.17, snout=.22, ear=.07, legl=.28, step=.12):
    """small side-view four-legged mammal facing +x (shrew / early primate)"""
    s = ''; by = fy - legl * L - .14 * L
    for lx, ph in ((-.30, 1), (-.22, -1), (.24, -1), (.32, 1)):
        hx = x + lx * L; fx = hx + ph * step * L
        k = (hx + ph * step * L * .2 - .03 * L, by + legl * L * .55)
        s += taper(hx, by, *k, .11 * L, .07 * L, col) + taper(*k, fx, fy - .01 * L, .06 * L, .045 * L, col)
    s += f'<ellipse cx="{x:.1f}" cy="{by:.1f}" rx="{.42 * L:.1f}" ry="{.17 * L:.1f}" fill="{col}"/>'
    hx, hy = x + .45 * L, by - .08 * L
    s += taper(x + .3 * L, by, hx, hy, .22 * L, .2 * L, col)
    s += f'<circle cx="{hx:.1f}" cy="{hy:.1f}" r="{headr * L * .6:.1f}" fill="{col}"/>'
    s += taper(hx, hy, hx + snout * L, hy + .05 * L, .14 * L, .03 * L, col)
    s += f'<ellipse cx="{hx - .03 * L:.1f}" cy="{hy - .09 * L:.1f}" rx="{ear * L:.1f}" ry="{ear * L * 1.1:.1f}" fill="{col}"/>'
    t0 = (x - .40 * L, by - .02 * L)
    s += (f'<path d="M{t0[0]:.1f},{t0[1]:.1f} C{x + tail[0] * L * .6:.1f},{by + tail[1] * L:.1f} {x + tail[2] * L:.1f},{by + tail[3] * L * .3:.1f} '
          f'{x + tail[2] * L:.1f},{by + tail[3] * L:.1f}" fill="none" stroke="{col}" stroke-width="{.045 * L:.1f}" stroke-linecap="round"/>')
    return s


def ape(x, fy, H, col):
    """knuckle-walking ape facing +x"""
    s = ''; hp = (x - .20 * H, fy - .45 * H); sh = (x + .10 * H, fy - .62 * H)
    for fx in (x - .30 * H, x - .10 * H):
        k = ik(hp, (fx, fy - .03 * H), .25 * H, .24 * H, 1)
        s += taper(*hp, *k, .13 * H, .08 * H, col) + taper(*k, fx, fy - .03 * H, .075 * H, .05 * H, col)
        s += taper(fx - .02 * H, fy - .01 * H, fx + .08 * H, fy - .01 * H, .05 * H, .03 * H, col)
    s += taper(*hp, *sh, .22 * H, .26 * H, col)
    s += f'<ellipse cx="{x - .02 * H:.1f}" cy="{fy - .58 * H:.1f}" rx="{.2 * H:.1f}" ry="{.12 * H:.1f}" fill="{col}" transform="rotate(-25 {x:.1f} {fy - .58 * H:.1f})"/>'
    hc = (sh[0] + .14 * H, sh[1] - .02 * H); hr = .075 * H
    s += taper(*sh, *hc, .12 * H, .1 * H, col)
    s += f'<circle cx="{hc[0]:.1f}" cy="{hc[1]:.1f}" r="{hr:.1f}" fill="{col}"/>'
    s += f'<ellipse cx="{hc[0] + hr * .8:.1f}" cy="{hc[1] + hr * .45:.1f}" rx="{hr * .65:.1f}" ry="{hr * .55:.1f}" fill="{col}"/>'
    s += f'<ellipse cx="{hc[0] + hr * .55:.1f}" cy="{hc[1] - hr * .4:.1f}" rx="{hr * .55:.1f}" ry="{hr * .25:.1f}" fill="{col}"/>'
    for wx in (x + .06 * H, x + .24 * H):
        e = ((sh[0] + wx) / 2 - .02 * H, (sh[1] + fy) / 2)
        s += taper(*sh, *e, .1 * H, .075 * H, col) + taper(*e, wx, fy - .07 * H, .075 * H, .06 * H, col)
        s += hand(wx, fy - .07 * H, 175, .065 * H, 'R', 'back', 'fist', skin=col, line=col, creases=False)
    return s


def sauropod(x, gy, s, col, flip=1):
    p = lambda X, Y: f'{x + flip * X * s:.1f},{gy + Y * s:.1f}'
    body = (f'<path d="M{p(-120, -95)} C{p(-80, -150)} {p(60, -160)} {p(110, -110)} C{p(150, -170)} {p(190, -260)} {p(240, -300)} '
            f'C{p(262, -316)} {p(292, -312)} {p(296, -296)} C{p(298, -286)} {p(280, -282)} {p(262, -284)} C{p(222, -250)} {p(185, -150)} {p(140, -70)} '
            f'C{p(120, -45)} {p(40, -40)} {p(-60, -48)} C{p(-140, -50)} {p(-250, -40)} {p(-340, -10)} C{p(-260, -60)} {p(-170, -70)} {p(-120, -95)}Z" fill="{col}"/>')
    legs = ''.join(taper(x + flip * lx * s, gy - 70 * s, x + flip * (lx + d) * s, gy, 34 * s, 28 * s, col) for lx, d in ((-95, -8), (-60, 10), (55, 8), (95, -6)))
    return legs + body


# ======================= A: SMALL WAS A SUPERPOWER =======================
random.seed(11)
d = (lin('askyA', [(0, '#060a1c'), (.45, '#1b1640'), (.75, '#6a2a3c'), (.9, '#d0603a'), (1, '#f39a4a')])
     + rad('fbA', 1690, 190, 620, [(0, '#fff6d8', .95), (.12, '#ffd27a', .7), (.4, '#ff8a3a', .28), (1, '#ff5a2a', 0)])
     + rad('horA', 1300, 760, 900, [(0, '#ffb060', .55), (1, '#ff6030', 0)])
     + '<linearGradient id="trailA" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#fff3d0"/><stop offset=".35" stop-color="#ffb15a" stop-opacity=".7"/><stop offset="1" stop-color="#ff7a30" stop-opacity="0"/></linearGradient>'
     + lin('groundA', [(0, '#1a1118'), (1, '#07050a')])
     + lin('furA', [(0, '#ffc07a'), (.18, '#a8653c'), (.55, '#5a3424'), (1, '#24140f')], x2=-.6, y2=1)
     + lin('bellyA', [(0, '#ffd9a0'), (1, '#8a5a3a')], x2=-.3, y2=1)
     + filt('haloA', '#ff9a50', 2, 7) + filt('rimA', '#ffb870')
     + '<filter id="blurA" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="18"/></filter>'
     + '<filter id="blur6" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="5"/></filter>')
b = '<rect width="1920" height="1080" fill="url(#askyA)"/>'
b += stars(90, 520, xmin=900, col='#dfe8ff', op=.5, sparks=0)
b += '<rect width="1920" height="1080" fill="url(#horA)"/><rect width="1920" height="1080" fill="url(#fbA)"/>'
# fireball + trail (from upper right toward lower left)
b += '<g transform="rotate(-32 1690 190)"><path d="M1690,160 L2430,110 L2430,270 L1690,220Z" fill="url(#trailA)" filter="url(#blurA)"/>'
b += '<path d="M1690,172 L2330,150 L2330,230 L1690,208Z" fill="url(#trailA)" opacity=".9" filter="url(#blur6)"/></g>'
b += '<circle cx="1690" cy="190" r="140" fill="#ffcf80" opacity=".6" filter="url(#blurA)"/><circle cx="1690" cy="190" r="70" fill="#fff8e6"/><circle cx="1678" cy="200" r="46" fill="#ffffff"/>'
b += '<circle cx="1690" cy="190" r="86" fill="none" stroke="#ffe4a8" stroke-width="10" opacity=".6" filter="url(#blur6)"/>'
for _ in range(14):   # fragments
    fx, fy_ = random.randint(1450, 1900), random.randint(60, 420); L = random.randint(30, 80)
    b += cap(fx, fy_, fx + L * .85, fy_ - L * .53, random.choice([3, 4, 5]), '#ffd08a', .55)
b += spark(1690, 190, 70, '#fffaf0', .7) + spark(1480, 110, 22) + spark(1840, 420, 18) + spark(1280, 230, 16)
# distant hills + sauropods (middle ground) with rim light from the fireball
b += '<path d="M0,770 C200,740 420,760 640,735 C860,710 1100,745 1320,725 C1540,705 1760,740 1920,720 L1920,1080 L0,1080Z" fill="#2a1626"/>'
d += '<g id="sauros">' + sauropod(770, 770, 1.15, '#140b18') + sauropod(1560, 742, .62, '#140b18', -1) + sauropod(1780, 752, .48, '#140b18', -1) + '</g>'
b += lit('sauros', 'haloA', 'rimA', 5, -4)
b += blobs(10, 0, 690, 1920, 790, '#ff9a60', .03, .07, 80, 220)   # dust haze
# foreground mound and burrow
b += '<path d="M0,900 C260,850 560,860 820,840 C1000,826 1180,812 1360,830 C1560,850 1760,880 1920,900 L1920,1080 L0,1080Z" fill="url(#groundA)"/>'
b += '<path d="M820,840 C1000,826 1180,812 1360,830" fill="none" stroke="#ff9a5a" stroke-width="5" opacity=".55"/>'
b += '<ellipse cx="1000" cy="905" rx="120" ry="58" fill="#030204"/><path d="M880,905 C900,850 1100,840 1120,905" fill="none" stroke="#5a3a3a" stroke-width="10" opacity=".7"/>'
for gx in list(range(40, 820, 38)) + list(range(1400, 1640, 40)):   # dead fern / grass silhouettes
    gy = 905 - (gx < 820) * 20 + random.randint(-10, 10); hgt = random.randint(30, 80)
    b += f'<path d="M{gx},{gy + 30} q{random.randint(-20, 20)},{-hgt / 2} {random.randint(-30, 30)},{-hgt}" stroke="#1d1218" stroke-width="5" fill="none"/>'
b += '<g opacity=".9">' + ''.join(f'<ellipse cx="{random.randint(900, 1500)}" cy="{random.randint(925, 1000)}" rx="{random.randint(10, 26)}" ry="{random.randint(6, 12)}" fill="#24161c"/>' for _ in range(12)) + '</g>'
# the shrew (sitting up, looking at the fireball)
BODY = 'M-120,0 C-150,-80 -130,-190 -60,-245 C-20,-280 45,-275 78,-238 C118,-190 128,-90 108,0 C60,18 -70,18 -120,0Z'
HEAD = 'M-30,-245 C-50,-305 -10,-352 45,-356 C90,-362 132,-382 188,-410 C202,-416 208,-404 198,-394 C152,-352 120,-316 98,-272 C76,-236 15,-222 -30,-245Z'
sh = '<clipPath id="cbA"><path d="' + BODY + '"/></clipPath><clipPath id="chA"><path d="' + HEAD + '"/></clipPath>'
d += sh
s = '<g transform="translate(1330 930) scale(1.32)">'
s += f'<path d="M-110,-6 C-200,10 -260,0 -330,-30" fill="none" stroke="#3a2218" stroke-width="12" stroke-linecap="round"/>'
s += f'<path d="{BODY}" fill="#ffb870" transform="translate(3 -3)" filter="url(#blur6)" opacity=".8"/>'
s += f'<g clip-path="url(#cbA)"><path d="{BODY}" fill="#ffc583"/><path d="{BODY}" fill="url(#furA)" transform="translate(-7 6)"/>'
s += '<ellipse cx="72" cy="-110" rx="48" ry="100" fill="url(#bellyA)" opacity=".75"/>'
for _ in range(260):
    fx, fy_ = random.uniform(-140, 120), random.uniform(-270, 0); a = random.uniform(95, 120)
    l = random.uniform(10, 22); c = '#1c0f0a' if random.random() < .6 else '#d79a62'
    s += cap(fx, fy_, fx + math.cos(R(a)) * l, fy_ + math.sin(R(a)) * l, 2.2, c, .45)
s += '</g>'
s += f'<path d="{HEAD}" fill="#ffb870" transform="translate(3 -3)" filter="url(#blur6)" opacity=".8"/>'
s += f'<g clip-path="url(#chA)"><path d="{HEAD}" fill="#ffd296"/><path d="{HEAD}" fill="url(#furA)" transform="translate(-7 7)"/>'
for _ in range(120):
    fx, fy_ = random.uniform(-40, 190), random.uniform(-410, -230); a = random.uniform(150, 175)
    l = random.uniform(8, 16); c = '#1c0f0a' if random.random() < .6 else '#e5ac70'
    s += cap(fx, fy_, fx + math.cos(R(a)) * l, fy_ + math.sin(R(a)) * l, 2, c, .45)
s += '</g>'
s += '<ellipse cx="6" cy="-322" rx="30" ry="36" fill="#4a2a1e" transform="rotate(-20 6 -322)"/><ellipse cx="9" cy="-320" rx="18" ry="24" fill="#c97a6a" transform="rotate(-20 9 -320)"/>'
s += '<path d="M-22,-338 C-12,-362 20,-366 34,-346" stroke="#ffc888" stroke-width="5" fill="none" opacity=".8"/>'
s += '<circle cx="200" cy="-404" r="9" fill="#3a1a1a"/><circle cx="202" cy="-407" r="3" fill="#ffd6b0"/>'
s += '<ellipse cx="82" cy="-326" rx="17" ry="15" fill="#0a0506"/><circle cx="88" cy="-332" r="6" fill="#fff4dc"/><circle cx="76" cy="-321" r="2.5" fill="#ffb060"/>'
s += '<ellipse cx="82" cy="-326" rx="22" ry="20" fill="none" stroke="#2a150e" stroke-width="3"/>'
for k in range(6):
    s += f'<path d="M178,-388 q{30 + k * 6},{-24 + k * 10} {70 + k * 8},{-36 + k * 16}" stroke="#ffe2b8" stroke-width="1.6" fill="none" opacity=".7"/>'
s += '<path d="M78,-200 C100,-205 120,-215 128,-232 C134,-244 120,-250 110,-240 C100,-226 88,-222 76,-218Z" fill="#5a3424" stroke="#ffb470" stroke-width="3"/>'
s += '<path d="M60,-178 C84,-178 104,-190 110,-206 C114,-218 100,-222 92,-212 C84,-200 72,-196 58,-194Z" fill="#4a2a1e" stroke="#ffb470" stroke-width="2.5" opacity=".9"/>'
s += '<ellipse cx="60" cy="-4" rx="62" ry="16" fill="#3a2218"/><path d="M10,-12 C40,-24 100,-22 122,-6" stroke="#ffb470" stroke-width="3" fill="none"/>'
s += '</g>'
b += s
b += ''.join(f'<circle cx="{random.randint(1000, 1880)}" cy="{random.randint(420, 880)}" r="{random.choice([2, 3, 4])}" fill="#ffb070" opacity="{random.uniform(.3, .8):.2f}"/>' for _ in range(40))
open(os.path.join(HERE, 'A.html'), 'w').write(page('#060a1c', svg(d, b), [('SMALL', 235, 'w'), ('WAS A', 150, 'w'), ('SUPERPOWER', 160, 'y')], outline='#07050f'))

# ======================= B: FROM SHREW TO YOU =======================
from body import arm as body_arm
random.seed(22)
FIG, FAR = '#1a1410', '#2c2119'


def shrew(x, fy, L, col):
    """cute side-view shrew facing +x: round body, big round head, SHORT snout, round ear, short tail"""
    s = ''; by = fy - .30 * L
    for lx, ph in ((-.26, 1), (-.16, -1), (.18, -1), (.28, 1)):
        hx = x + lx * L; fx = hx + ph * .07 * L
        s += taper(hx, by, fx, fy - .02 * L, .12 * L, .07 * L, col)
        s += f'<ellipse cx="{fx + .03 * L:.1f}" cy="{fy - .02 * L:.1f}" rx="{.06 * L:.1f}" ry="{.025 * L:.1f}" fill="{col}"/>'
    s += f'<ellipse cx="{x:.1f}" cy="{by - .04 * L:.1f}" rx="{.40 * L:.1f}" ry="{.22 * L:.1f}" fill="{col}"/>'
    hx, hy = x + .38 * L, by - .12 * L; hr = .2 * L
    s += f'<circle cx="{hx:.1f}" cy="{hy:.1f}" r="{hr:.1f}" fill="{col}"/>'
    s += taper(hx + .05 * L, hy - .01 * L, hx + .33 * L, hy + .07 * L, .25 * L, .07 * L, col)       # short snout
    s += f'<circle cx="{hx + .33 * L:.1f}" cy="{hy + .07 * L:.1f}" r="{.05 * L:.1f}" fill="{col}"/>'
    s += f'<circle cx="{hx - .07 * L:.1f}" cy="{hy - .17 * L:.1f}" r="{.085 * L:.1f}" fill="{col}"/>'  # round ear
    s += (f'<path d="M{x - .38 * L:.1f},{by - .02 * L:.1f} C{x - .6 * L:.1f},{by + .05 * L:.1f} {x - .75 * L:.1f},{by - .02 * L:.1f} '
          f'{x - .9 * L:.1f},{by - .1 * L:.1f}" fill="none" stroke="{col}" stroke-width="{.05 * L:.1f}" stroke-linecap="round"/>')
    return s


def furline(x0, y0, x1, y1, n, l, col, a=-150, w=4):
    o = ''
    for k in range(n):
        t = k / max(1, n - 1); px, py = x0 + (x1 - x0) * t, y0 + (y1 - y0) * t; aa = R(a + random.uniform(-15, 15)); ll = l * random.uniform(.7, 1.2)
        o += cap(px, py, px + math.cos(aa) * ll, py + math.sin(aa) * ll, w, col)
    return o


def human(x, fy, H, col, far):
    """cute (5.5 heads) side-view human walking toward +x: back leg pushing off, front heel landing, arms swinging opposite"""
    s = ''; hip = (x, fy - 2.45 * H); L1, L2 = 1.25 * H, 1.2 * H
    sh = (x + .10 * H, fy - 4.08 * H)
    # far side first (lighter): forward-swinging arm + back leg
    s += body_arm(sh[0] - .04 * H, sh[1], H, upper=30, bend=32, bend_dir=1, name='hf', side='L', view='back', pose='flat',
                  sleeve=far, skin=far, line=far, kind='cute', fingers=True, lw=1.4)
    ank, toe = (x - .92 * H, fy - .30 * H), (x - .40 * H, fy - .03 * H)
    k = ik(hip, ank, L1, L2, 1)
    s += taper(*hip, *k, .56 * H, .40 * H, far) + taper(*k, *ank, .40 * H, .28 * H, far) + taper(*ank, *toe, .34 * H, .26 * H, far)
    # pelvis + torso (slight forward lean) + neck + head
    s += f'<ellipse cx="{x + .02 * H:.1f}" cy="{hip[1] - .05 * H:.1f}" rx="{.52 * H:.1f}" ry="{.40 * H:.1f}" fill="{col}"/>'
    s += taper(x, hip[1] - .1 * H, sh[0], sh[1] + .15 * H, .98 * H, 1.02 * H, col)
    s += f'<ellipse cx="{x + .14 * H:.1f}" cy="{sh[1] + .35 * H:.1f}" rx="{.50 * H:.1f}" ry="{.55 * H:.1f}" fill="{col}"/>'   # chest
    hc = (x + .30 * H, fy - 4.92 * H); hr = .56 * H
    s += taper(sh[0] + .05 * H, sh[1] - .1 * H, hc[0] - .05 * H, hc[1] + .3 * H, .36 * H, .32 * H, col)
    s += f'<circle cx="{hc[0]:.1f}" cy="{hc[1]:.1f}" r="{hr:.1f}" fill="{col}"/>'
    s += f'<ellipse cx="{hc[0] + hr * .95:.1f}" cy="{hc[1] + hr * .12:.1f}" rx="{hr * .13:.1f}" ry="{hr * .15:.1f}" fill="{col}"/>'      # nose
    s += f'<ellipse cx="{hc[0] + hr * .42:.1f}" cy="{hc[1] + hr * .6:.1f}" rx="{hr * .42:.1f}" ry="{hr * .32:.1f}" fill="{col}"/>'      # chin / cheek
    s += f'<ellipse cx="{hc[0] - hr * .12:.1f}" cy="{hc[1] - hr * .3:.1f}" rx="{hr * 1.05:.1f}" ry="{hr * .82:.1f}" fill="{col}" transform="rotate(-12 {hc[0]:.1f} {hc[1]:.1f})"/>'  # hair
    s += f'<path d="M{hc[0] + hr * .3:.1f},{hc[1] - hr * 1.0:.1f} q{hr * .45:.1f},{-hr * .05:.1f} {hr * .62:.1f},{hr * .3:.1f}" stroke="{col}" stroke-width="{hr * .28:.1f}" fill="none" stroke-linecap="round"/>'  # fringe tuft
    # near side: front leg landing on the heel + backward-swinging arm
    ank, heel, toe = (x + .74 * H, fy - .20 * H), (x + .66 * H, fy - .06 * H), (x + 1.28 * H, fy - .16 * H)
    k = ik(hip, ank, L1, L2, 1)
    s += taper(*hip, *k, .56 * H, .40 * H, col) + taper(*k, *ank, .40 * H, .28 * H, col) + taper(*heel, *toe, .34 * H, .26 * H, col)
    s += body_arm(sh[0] + .02 * H, sh[1] + .02 * H, H, upper=-38, bend=26, bend_dir=1, name='hn', side='R', view='back', pose='flat',
                  sleeve=col, skin=col, line=col, kind='cute', fingers=True, lw=1.4)
    return s


SX, SY = 1575, 585   # the sun, just behind the human's chest
d = (lin('skyB', [(0, '#262428'), (.25, '#54463e'), (.5, '#b98a52'), (.75, '#f2c87a'), (1, '#ffe9b8')], x2=1, y2=0)
     + lin('skyVB', [(0, '#000000'), (.6, '#000000'), (1, '#ffd890')])
     + rad('sunB', SX, SY, 1100, [(0, '#fffbe8', 1), (.12, '#ffeaa8', .85), (.35, '#f6c46a', .4), (.7, '#e8a050', .12), (1, '#e8a050', 0)])
     + rad('coreB', SX, SY, 330, [(0, '#ffffff', 1), (.38, '#fff6d8', 1), (.5, '#ffe6a0', .75), (.75, '#ffd27a', .25), (1, '#ffd27a', 0)])
     + rad('pathGlowB', SX, 960, 700, [(0, '#ffe2a0', .55), (1, '#ffe2a0', 0)])
     + lin('farHillB', [(0, '#d9b47a'), (1, '#b89a62')])
     + lin('midB', [(0, '#3a2c22'), (.3, '#5e4a2c'), (.62, '#7d7a36'), (1, '#94923e')], x2=1, y2=0)
     + lin('fgB', [(0, '#1e1712'), (.45, '#3a3018'), (1, '#4c4a20')], x2=1, y2=0)
     + lin('pathB', [(0, '#3e3028'), (.6, '#a08050'), (1, '#e6c88a')], x2=1, y2=0)
     + filt('haloB', '#ffe2a0', 4, 12)
     + '<filter id="rimB" x="-20%" y="-20%" width="140%" height="140%">'
       '<feOffset in="SourceAlpha" dx="-5" dy="4" result="o"/><feComposite in="SourceAlpha" in2="o" operator="out" result="e"/>'
       '<feFlood flood-color="#fff6d2"/><feComposite in2="e" operator="in" result="c"/>'
       '<feGaussianBlur in="c" stdDeviation="7" result="cb"/><feFlood flood-color="#ffc060"/><feComposite in2="cb" operator="in" result="w0"/>'
       '<feComposite in="w0" in2="SourceAlpha" operator="out" result="warm"/>'
       '<feMerge><feMergeNode in="warm"/><feMergeNode in="warm"/><feMergeNode in="SourceGraphic"/><feMergeNode in="c"/></feMerge></filter>'
     + '<filter id="blurB" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="14"/></filter>'
     + '<filter id="blurB4" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="4"/></filter>'
     + '<filter id="blurB30" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="30"/></filter>'
     + '<filter id="grainB"><feTurbulence type="fractalNoise" baseFrequency=".9" numOctaves="2" seed="4"/>'
       '<feColorMatrix values="0 0 0 0 .1  0 0 0 0 .08  0 0 0 0 .05  0 0 0 -1.6 1.05"/><feComposite in2="SourceGraphic" operator="in"/></filter>')
b = '<rect width="1920" height="1080" fill="url(#skyB)"/><rect width="1920" height="1080" fill="url(#skyVB)" opacity=".18"/>'
# high thin clouds lit from below on the bright side
for cx_, cy_, w_ in ((1180, 180, 420), (1620, 120, 360), (1400, 300, 300), (1820, 330, 220)):
    b += f'<ellipse cx="{cx_}" cy="{cy_}" rx="{w_}" ry="{w_ * .06:.0f}" fill="#fff0c8" opacity=".16" filter="url(#blurB4)"/>'
b += '<rect width="1920" height="1080" fill="url(#sunB)"/>'
# ash clouds on the left, clear on the right
b += blobs(26, -100, 120, 760, 760, '#1c1a1e', .25, .55, 120, 300).replace('<ellipse', '<ellipse filter="url(#blurB)"')
b += blobs(8, 500, 200, 900, 700, '#3a3234', .15, .3, 100, 220).replace('<ellipse', '<ellipse filter="url(#blurB)"')
for i in range(15):   # sun rays of varying width
    a = 110 + i * 10 + random.uniform(-3, 3); w_ = random.uniform(1.5, 4.5)
    b += (f'<path d="M{SX},{SY} L{SX + math.cos(R(a)) * 1900:.0f},{SY - math.sin(R(a)) * 1900:.0f} L{SX + math.cos(R(a + w_)) * 1900:.0f},{SY - math.sin(R(a + w_)) * 1900:.0f}Z" '
          f'fill="#fff4d0" opacity="{random.uniform(.05, .11):.2f}"/>')
for i in range(8):
    a = -40 + i * 12 + random.uniform(-3, 3); w_ = random.uniform(2, 4)
    b += (f'<path d="M{SX},{SY} L{SX + math.cos(R(a)) * 900:.0f},{SY - math.sin(R(a)) * 900:.0f} L{SX + math.cos(R(a + w_)) * 900:.0f},{SY - math.sin(R(a + w_)) * 900:.0f}Z" '
          f'fill="#fff4d0" opacity=".07"/>')
# sun: big bloom, corona, bright disc
b += f'<circle cx="{SX}" cy="{SY}" r="330" fill="url(#coreB)"/>'
b += f'<circle cx="{SX}" cy="{SY}" r="150" fill="#fffdf2" filter="url(#blurB4)"/><circle cx="{SX}" cy="{SY}" r="128" fill="#ffffff"/>'
b += spark(SX, SY, 260, '#ffffff', .55) + spark(SX, SY, 120, '#ffffff', .8)
# far hills (pale, hazy) with a few acacias = depth
b += '<path d="M600,790 C760,760 900,768 1040,752 C1180,736 1300,748 1420,735 C1560,722 1700,736 1920,728 L1920,800 L600,800Z" fill="url(#farHillB)" opacity=".75"/>'
for tx, ts in ((1030, .7), (1760, 1.0), (1860, .6)):
    ty = 742 - (tx - 1000) * .01
    b += cap(tx, ty, tx + 4 * ts, ty - 48 * ts, 5 * ts, '#b0905c', .9)
    b += f'<ellipse cx="{tx + 4 * ts:.0f}" cy="{ty - 52 * ts:.0f}" rx="{48 * ts:.0f}" ry="{11 * ts:.0f}" fill="#b0905c" opacity=".9"/>'
b += f'<rect x="0" y="690" width="1920" height="140" fill="#ffe8b0" opacity=".18" filter="url(#blurB30)"/>'
# middle ground
b += '<path d="M0,800 C300,780 520,795 800,775 C1100,752 1400,770 1700,752 C1800,746 1880,748 1920,748 L1920,1080 L0,1080Z" fill="url(#midB)"/>'
b += '<path d="M800,775 C1100,752 1400,770 1700,752 C1800,746 1880,748 1920,748" stroke="#fff0b8" stroke-width="4" fill="none" opacity=".6"/>'
b += '<path d="M0,800 C300,780 520,795 800,775" stroke="#ffe7a8" stroke-width="3" fill="none" opacity=".25"/>'
for gx in range(0, 1920, 18):   # dead stumps on the ash side, grass with sunlit tips on the living side
    gy = 790 - gx * .025 + random.randint(-6, 10)
    if gx < 650:
        b += cap(gx, gy, gx + random.randint(-4, 4), gy - random.randint(10, 40), 4, '#221a16', .8)
    else:
        for _ in range(3):
            h_ = random.randint(22, 58); dx_ = random.randint(-16, 16); x_ = gx + random.randint(-8, 8)
            b += f'<path d="M{x_},{gy + 10} q{random.randint(-6, 6)},{-h_ * .4:.0f} {dx_},{-h_}" stroke="#4a5420" stroke-width="3" fill="none"/>'
            if gx > 900 and random.random() < .5:
                b += cap(x_ + dx_ * .8, gy + 10 - h_ * .85, x_ + dx_, gy + 10 - h_, 3, '#ffeaa0', .8)
b += blobs(10, 900, 820, 1900, 900, '#c8b85a', .12, .25, 60, 160)
# ground texture: pebbles and specks
for _ in range(260):
    px, py = random.randint(0, 1900), random.randint(800, 1075)
    c_ = '#14100c' if random.random() < .65 else '#d8c48a'
    b += f'<circle cx="{px}" cy="{py}" r="{random.choice([1.5, 2, 2.5, 3])}" fill="{c_}" opacity="{random.uniform(.2, .5):.2f}"/>'
# the path, glowing where the sun hits it
b += '<path d="M0,960 C400,930 900,935 1500,925 C1700,922 1850,930 1920,935 L1920,1000 C1600,985 900,990 0,1010Z" fill="url(#pathB)" opacity=".9"/>'
b += '<rect x="0" y="860" width="1920" height="220" fill="url(#pathGlowB)"/>'
for i in range(26):   # footprints / paw prints trail
    fx = 200 + i * 52; fy_ = 975 - i * 1.6 + (i % 2) * 14; r = 4 + i * .35
    b += f'<ellipse cx="{fx}" cy="{fy_:.0f}" rx="{r * 1.6:.1f}" ry="{r * .7:.1f}" fill="#2a1e16" opacity=".55"/>'
    b += f'<path d="M{fx - r * 1.4:.1f},{fy_ - r * .4:.1f} q{r * 1.4:.1f},{-r * .6:.1f} {r * 2.8:.1f},0" stroke="#ffe0a0" stroke-width="1.5" fill="none" opacity=".35"/>'
# foreground lip (darker, nearest to us) on the left two thirds only (bottom-right stays empty)
b += '<path d="M0,1030 C200,1012 500,1016 800,1030 C1000,1040 1150,1060 1250,1080 L0,1080Z" fill="url(#fgB)" opacity=".85"/>'
for gx in range(0, 1180, 14):
    gy = 1040 + random.randint(-12, 25) + gx * .02
    for _ in range(2):
        h_ = random.randint(25, 70)
        b += f'<path d="M{gx + random.randint(-6, 6)},{gy + 30} q{random.randint(-8, 8)},{-h_ * .5:.0f} {random.randint(-20, 20)},{-h_}" stroke="#15110c" stroke-width="4" fill="none"/>'
FY = 950
d += '<g id="march">'
d += shrew(300, FY + 10, 150, FIG)
d += quad(565, FY + 6, 210, FIG, legl=.32, tail=(-.9, -.3, -1.15, -1.0), snout=.12, ear=.06, headr=.2)
d += furline(470, FY - 105, 640, FY - 112, 12, 16, FIG)
d += ape(845, FY, 300, FIG)
d += furline(760, FY - 170, 900, FY - 205, 12, 18, FIG, a=-140, w=5)
d += biped(1110, FY - 4, 360, FIG, lean=10, stride=.22, arm=1.18, head=.075, jaw=1, hip=.45, a_near=(-18, -2), a_far=(20, 34), brow=1)
d += human(1405, FY - 8, 104, FIG, FAR)
d += '</g>'
# dust motes drifting in the light
b += ''.join(f'<circle cx="{random.randint(950, 1880)}" cy="{random.randint(300, 900)}" r="{random.choice([1.5, 2, 3])}" fill="#fff4d0" opacity="{random.uniform(.3, .8):.2f}"/>' for _ in range(45))
# long shadows thrown toward us and to the left (sun low behind them)
b += (f'<g opacity=".5" filter="url(#blurB4)"><use href="#march" transform="matrix(1 0 0.75 -0.16 {-0.75 * FY:.0f} {1.16 * FY:.0f})" '
      f'style="fill:#1a1008"/></g>')
b += f'<use href="#march" filter="url(#haloB)" opacity=".55"/>'
b += f'<g filter="url(#rimB)"><use href="#march"/></g>'
b += f'<circle cx="{300 + .38 * 150 + .1 * 150:.0f}" cy="{FY + 10 - .30 * 150 - .14 * 150:.0f}" r="5" fill="#fff4d0"/>'   # shrew eye glint
b += ''.join(f'<circle cx="{random.randint(20, 700)}" cy="{random.randint(560, 900)}" r="{random.choice([2, 3])}" fill="#ff8a40" opacity="{random.uniform(.3, .8):.2f}"/>' for _ in range(30))
open(os.path.join(HERE, 'B.html'), 'w').write(page('#2b2a2e', svg(d, b), [('FROM', 150, 'w'), ('SHREW', 235, 'y'), ('TO YOU', 175, 'w')], outline='#120e0c'))

# ======================= C: BRAINS ROUGHLY TRIPLED =======================
random.seed(33)
FIG = '#120a08'
d = (lin('skyC', [(0, '#0d0a1e'), (.3, '#2c1430'), (.55, '#8a2e22'), (.72, '#e2702e'), (.74, '#f6a04a')])
     + rad('sunglowC', 1320, 720, 900, [(0, '#fff2c8', .95), (.2, '#ffc060', .6), (.55, '#ff7a30', .2), (1, '#ff5a20', 0)])
     + rad('sunC', 1320, 720, 290, [(0, '#fffdf2', 1), (.7, '#ffe9a8', 1), (1, '#ffc770', 1)])
     + rad('marrowC', 1530, 842, 120, [(0, '#fff6c8', 1), (.3, '#ffd27a', .8), (1, '#ff9a40', 0)])
     + lin('groundC', [(0, '#1c0f0a'), (1, '#060302')])
     + filt('haloC', '#ffd890', 4, 10) + filt('rimC', '#ffe9b0')
     + '<filter id="blurC" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="16"/></filter>')
b = '<rect width="1920" height="1080" fill="url(#skyC)"/>'
b += stars(60, 380, xmin=900, col='#ffe8d0', op=.45, sparks=0)
b += '<rect width="1920" height="1080" fill="url(#sunglowC)"/>'
b += '<circle cx="1320" cy="720" r="290" fill="url(#sunC)"/>'
b += blobs(8, 300, 640, 1900, 780, '#ffb070', .08, .18, 120, 300)
b += '<path d="M0,800 L1920,800 L1920,1080 L0,1080Z" fill="#2a120c"/>'
b += '<path d="M0,800 C200,790 380,760 520,778 C640,792 760,770 860,800Z" fill="#1c0c08"/><path d="M1700,800 C1760,770 1840,760 1920,775 L1920,800Z" fill="#1c0c08"/>'
b += '<path d="M0,1080 L0,890 C300,870 700,868 1000,872 C1200,858 1400,862 1500,866 C1650,870 1800,885 1920,900 L1920,1080Z" fill="url(#groundC)"/>'
b += '<path d="M1000,872 C1200,858 1400,862 1500,866 C1650,870 1800,885 1920,900" fill="none" stroke="#ff9a50" stroke-width="4" opacity=".6"/>'
# hominin kneeling (silhouette against the sun)
X, FY_, H = 1250, 872, 620
g = ''
hp = (X, FY_ - .29 * H)
kb = (X - .08 * H, FY_ - .025 * H); tb = (X - .30 * H, FY_ - .03 * H)
g += taper(*hp, *kb, .11 * H, .075 * H, FIG) + taper(*kb, *tb, .07 * H, .04 * H, FIG)
kf = (X + .22 * H, FY_ - .29 * H); ff = (X + .23 * H, FY_ - .03 * H)
g += taper(*hp, *kf, .11 * H, .075 * H, FIG) + taper(*kf, *ff, .07 * H, .045 * H, FIG)
g += taper(ff[0] - .02 * H, FY_ - .015 * H, ff[0] + .08 * H, FY_ - .01 * H, .05 * H, .03 * H, FIG)
lean = 18; sh = (hp[0] + math.sin(R(lean)) * .31 * H, hp[1] - math.cos(R(lean)) * .31 * H)
g += taper(*hp, *sh, .17 * H, .19 * H, FIG)
g += f'<ellipse cx="{(hp[0] + sh[0]) / 2 + .03 * H:.1f}" cy="{(hp[1] + sh[1]) / 2 - .02 * H:.1f}" rx="{.1 * H:.1f}" ry="{.15 * H:.1f}" fill="{FIG}" transform="rotate({lean} {(hp[0] + sh[0]) / 2:.1f} {(hp[1] + sh[1]) / 2:.1f})"/>'
hr = .078 * H; hc = (sh[0] + .11 * H, sh[1] - .06 * H)
g += taper(*sh, *hc, .08 * H, .07 * H, FIG)
g += f'<circle cx="{hc[0]:.1f}" cy="{hc[1]:.1f}" r="{hr:.1f}" fill="{FIG}"/>'
g += f'<ellipse cx="{hc[0] + hr * .8:.1f}" cy="{hc[1] + hr * .5:.1f}" rx="{hr * .62:.1f}" ry="{hr * .5:.1f}" fill="{FIG}"/>'
g += f'<ellipse cx="{hc[0] + hr * .65:.1f}" cy="{hc[1] - hr * .3:.1f}" rx="{hr * .5:.1f}" ry="{hr * .22:.1f}" fill="{FIG}"/>'
for k in range(26):   # shaggy hair along head and back
    t = k / 25; px = hc[0] - hr * .4 + (hp[0] - .06 * H - hc[0] + hr * .4) * t; py = hc[1] - hr * .8 + (hp[1] - hc[1] + hr * .8) * t
    a = R(-150 + random.uniform(-20, 20)); l = random.uniform(.02, .04) * H
    g += cap(px, py, px + math.cos(a) * l, py + math.sin(a) * l, 5, FIG)
U, F = .18 * H, .16 * H
# raised arm with the stone tool
e = (sh[0] + math.sin(R(208)) * U, sh[1] + math.cos(R(208)) * U); w = (e[0] + math.sin(R(178)) * F, e[1] + math.cos(R(178)) * F)
g += taper(*sh, *e, .07 * H, .055 * H, FIG) + taper(*e, *w, .055 * H, .04 * H, FIG)
g += hand(w[0], w[1], 180 - 178, .06 * H, 'R', 'back', 'hold', skin=FIG, line=FIG, creases=False)
st = (w[0] + .01 * H, w[1] - .115 * H)
g += f'<path d="M{st[0] - 40:.0f},{st[1] + 18:.0f} L{st[0] - 22:.0f},{st[1] - 26:.0f} L{st[0] + 18:.0f},{st[1] - 34:.0f} L{st[0] + 46:.0f},{st[1] - 6:.0f} L{st[0] + 30:.0f},{st[1] + 26:.0f}Z" fill="{FIG}"/>'
# lower arm gripping the bone
e2 = (sh[0] + math.sin(R(40)) * U, sh[1] + math.cos(R(40)) * U); w2 = (e2[0] + math.sin(R(30)) * F, e2[1] + math.cos(R(30)) * F)
g += taper(*sh, *e2, .07 * H, .055 * H, FIG) + taper(*e2, *w2, .055 * H, .04 * H, FIG)
g += hand(w2[0], w2[1], 180 - 30, .06 * H, 'R', 'back', 'hold', skin=FIG, line=FIG, creases=False)
d += f'<g id="homC">{g}</g>'
b += f'<g filter="url(#blurC)" opacity=".5"><circle cx="{st[0]:.0f}" cy="{st[1]:.0f}" r="60" fill="#fff0c0"/></g>'
b += lit('homC', 'haloC', 'rimC', -4, -3)
# rim on the stone edge (sun behind)
b += f'<path d="M{st[0] - 22:.0f},{st[1] - 26:.0f} L{st[0] + 18:.0f},{st[1] - 34:.0f} L{st[0] + 46:.0f},{st[1] - 6:.0f}" fill="none" stroke="#fff3c8" stroke-width="4"/>'
b += spark(st[0] + 50, st[1] - 40, 34, '#fffbe8', .9)
# the long bone on an anvil boulder, cracked open with glowing marrow
gx, gy = w2[0] + .06 * H * .5, w2[1] + .06 * H * .87
x0, xc, x1 = gx - 40, gx + 120, gx + 220
b += f'<path d="M{x0 - 20:.0f},{FY_ + 4} C{x0 - 30:.0f},{gy + 40:.0f} {x0:.0f},{gy + 16:.0f} {xc:.0f},{gy + 14:.0f} C{x1 + 10:.0f},{gy + 14:.0f} {x1 + 40:.0f},{gy + 40:.0f} {x1 + 50:.0f},{FY_ + 10}Z" fill="#1c0e0a"/>'
b += f'<path d="M{x0 - 22:.0f},{gy + 50:.0f} C{x0 - 8:.0f},{gy + 18:.0f} {xc:.0f},{gy + 12:.0f} {x1 + 30:.0f},{gy + 26:.0f}" fill="none" stroke="#ffb060" stroke-width="4" opacity=".8"/>'
b += f'<circle cx="1530" cy="842" r="130" fill="url(#marrowC)" filter="url(#blurC)" transform="translate({xc - 1530:.0f} {gy - 842:.0f})"/>'
BC, BL = '#eadcbc', '#3a2416'
b += f'<path d="M{x0:.0f},{gy - 13:.0f} L{xc - 18:.0f},{gy - 15:.0f} L{xc - 6:.0f},{gy - 3:.0f} L{xc - 20:.0f},{gy + 13:.0f} L{x0:.0f},{gy + 13:.0f}Z" fill="{BC}" stroke="{BL}" stroke-width="4"/>'
b += f'<ellipse cx="{x0:.0f}" cy="{gy - 9:.0f}" rx="20" ry="18" fill="{BC}" stroke="{BL}" stroke-width="4"/><ellipse cx="{x0:.0f}" cy="{gy + 11:.0f}" rx="18" ry="15" fill="{BC}" stroke="{BL}" stroke-width="4"/>'
b += f'<path d="M{xc + 14:.0f},{gy - 15:.0f} L{x1 - 10:.0f},{gy - 13:.0f} L{x1 - 10:.0f},{gy + 13:.0f} L{xc + 16:.0f},{gy + 13:.0f} L{xc + 4:.0f},{gy + 1:.0f}Z" fill="{BC}" stroke="{BL}" stroke-width="4"/>'
b += f'<ellipse cx="{x1:.0f}" cy="{gy - 9:.0f}" rx="22" ry="18" fill="{BC}" stroke="{BL}" stroke-width="4"/><ellipse cx="{x1:.0f}" cy="{gy + 11:.0f}" rx="20" ry="15" fill="{BC}" stroke="{BL}" stroke-width="4"/>'
b += f'<ellipse cx="{xc - 4:.0f}" cy="{gy:.0f}" rx="13" ry="11" fill="#ffcf5a"/><ellipse cx="{xc + 8:.0f}" cy="{gy:.0f}" rx="12" ry="10" fill="#ffcf5a"/><ellipse cx="{xc + 2:.0f}" cy="{gy:.0f}" rx="9" ry="6" fill="#fffbe0"/>'
b += hand(w2[0], w2[1], 180 - 30, .06 * H, 'R', 'back', 'hold', skin=FIG, line='#5a2a14', creases=False)
b += spark(xc + 2, gy - 34, 34, '#fffbe8') + spark(xc + 50, gy - 80, 14) + spark(xc - 50, gy - 66, 12)
for k in range(8):
    a = R(-160 + k * 20); b += cap(xc + math.cos(a) * 26, gy + math.sin(a) * 22, xc + math.cos(a) * 50, gy + math.sin(a) * 42, 3, '#ffe6a0', .8)
# scattered bones in the foreground (2001-style), kept left of the corner
def bonepiece(x, y, L, a, col='#cdb898'):
    c, s_ = math.cos(R(a)), math.sin(R(a)); x1, y1 = x + c * L, y + s_ * L
    o = cap(x, y, x1, y1, 12, col)
    for px, py in ((x, y), (x1, y1)):
        o += f'<circle cx="{px - s_ * 8:.0f}" cy="{py + c * 8:.0f}" r="10" fill="{col}"/><circle cx="{px + s_ * 8:.0f}" cy="{py - c * 8:.0f}" r="10" fill="{col}"/>'
    return o
fb = ''
for x, y, L, a in ((340, 980, 120, -12), (520, 1010, 90, 20), (760, 960, 140, 5), (980, 1030, 100, -30), (1150, 960, 80, 60), (200, 930, 70, 40)):
    fb += bonepiece(x, y, L, a)
for k in range(5):   # ribs
    fb += f'<path d="M{620 + k * 34},950 q-30,-50 10,-90" stroke="#bfa888" stroke-width="10" fill="none" stroke-linecap="round"/>'
b += f'<g opacity=".6" transform="translate(5 7)">{fb.replace("#cdb898", "#0a0402").replace("#bfa888", "#0a0402")}</g>'
b += f'<g opacity=".85">{fb}</g>'
b += ''.join(f'<ellipse cx="{random.randint(100, 1500)}" cy="{random.randint(900, 1060)}" rx="{random.randint(8, 22)}" ry="{random.randint(5, 10)}" fill="#2e1a12"/>' for _ in range(30))
open(os.path.join(HERE, 'C.html'), 'w').write(page('#0d0a1e', svg(d, b), [('BRAINS', 210, 'w'), ('ROUGHLY', 150, 'w'), ('TRIPLED', 215, 'y')], outline='#0a0505'))
print('ok')
