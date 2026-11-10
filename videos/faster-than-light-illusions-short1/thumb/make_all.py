# STYLE B shorts thumbnails for faster-than-light-illusions-short1..5 (guideline 16-9 B): dark scene, ONE big glowing subject in the
# top half, centred hook on a dark band (y ~900-1220), small frog low. Writes videos/faster-than-light-illusions-shortN/thumb/A.html.
# 1 LASER / BEATS LIGHT?       red laser dot streaking across the full Moon (short1: "Can a laser pointer break the speed of light?")
# 2 CUT FASTER / THAN LIGHT?   giant scissors, the cut point races along the blades past Mars; a hand shadow sweeps the dust cloud behind
# 3 IT OVERTOOK / LIGHT        blue Cherenkov glow of a fuel bundle in water, electron with a cone wake ("merely overtook light that had been slowed down")
# 4 SPOOKY / BUT NO MESSAGE    entangled pair: particle at Earth (spin up) and near Saturn's rings (spin down), linked; no signal
# 5 SPACE / IS STRETCHING      raisin bread loaf rising in space, the raisins are galaxies moving apart
# run: python3 videos/faster-than-light-illusions-short1/thumb/make_all.py [n..] ; then SLUG=faster-than-light-illusions-shortN python3 tools/thumb_shot.py
import os, sys, math, random
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, '../../..'))
sys.path.insert(0, os.path.join(REPO, 'videos/faster-than-light-illusions/thumb'))
from ftl_art import *


def out(n, bg, d, b, frog_svg, lines, top, hal, ff=('#cfe6ff', '#ffffff')):
    hx, hy, hr, hi, ho, hop = hal
    d = FILTERS + FROG_DEFS + d + halo(f'h{n}', hx, hy, hr, hi, ho) + rad(f'v{n}', 540, 960, 1200, [(.5, '#000', 0), (1, '#000', .8)])
    o = f'<rect width="1080" height="1920" fill="{bg}"/>'
    o += f'<circle cx="{hx}" cy="{hy}" r="{hr}" fill="url(#h{n})" opacity="{hop}"/>' + b
    y1 = top + sum(int(s * .97) for _, s, _ in lines)
    o += darkband(top - 30, y1 + 30, .55) + fireflies(34, 140, 1820, col=ff[0], core=ff[1], seed=n)
    o += f'<rect width="1080" height="1920" fill="url(#v{n})"/>' + frog_svg
    return vpage(bg, vsvg(d, o), lines, top=top)


def sky(rnd, n=260, y1=1900):
    return starfield(rnd, n, x1=1080, y1=y1)


# ---------------- 1: laser dot across the Moon ----------------
def s1():
    rnd = random.Random(1); MX, MY, MR = 540, 470, 330
    d, mo = moon(MX, MY, MR, 's1')
    d += lin('roof1', [(0, '#262c45'), (1, '#0c0f1c')])
    b = '<rect width="1080" height="1920" fill="#070b24"/>' + sky(rnd)
    b += f'<circle cx="{MX}" cy="{MY}" r="{MR * 1.5:.0f}" fill="#bcd0ff" opacity=".2" filter="url(#b80)"/>' + mo
    p0, p1, p2 = (MX - 260, MY + 140), (MX - 20, MY - 30), (MX + 230, MY - 80)
    q = lambda t: ((1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * p1[0] + t * t * p2[0], (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * p1[1] + t * t * p2[1])
    SX, SY = 640, 1530
    for t in (0, .33, .66):
        x, y = q(t); b += f'<path d="M{SX} {SY} L{x:.0f} {y:.0f}" stroke="#ff3b3b" stroke-width="3" opacity="{.1 + t * .15:.2f}"/>'
    hx, hy = q(1)
    b += glow_line(SX, SY, hx, hy, '#ff3030', 5, 24, 1)
    b += f'<path d="M{p0[0]} {p0[1]} Q{p1[0]} {p1[1]} {p2[0]} {p2[1]}" fill="none" stroke="#ff2a2a" stroke-width="44" opacity=".4" filter="url(#b12)" stroke-linecap="round"/>'
    for k in range(12):
        t = k / 12; x, y = q(t); b += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{7 + 10 * t:.0f}" fill="#ff3b30" opacity="{.15 + .5 * t:.2f}"/>'
    b += f'<circle cx="{hx:.0f}" cy="{hy:.0f}" r="100" fill="#ff2a2a" opacity=".6" filter="url(#b24)"/><circle cx="{hx:.0f}" cy="{hy:.0f}" r="32" fill="#ff4a3a"/><circle cx="{hx:.0f}" cy="{hy:.0f}" r="15" fill="#fff4ec"/>'
    for k in range(3):
        b += f'<path d="M{hx + 52:.0f} {hy - 40 + k * 40:.0f} l{60 - k * 10} {-6 + k * 4}" stroke="#ffd0c8" stroke-width="5" stroke-linecap="round" opacity=".75"/>'
    b += spark(hx + 30, hy - 60, 30, '#ffffff')
    # rooftop + person with laser at the bottom
    b += '<path d="M-20 1940 L-20 1620 L1100 1560 L1100 1940 Z" fill="url(#roof1)" stroke="#05070f" stroke-width="5"/>'
    b += '<path d="M-20 1620 L1100 1560" stroke="#7d86b8" stroke-width="4" opacity=".7"/>'
    b += person(600, 1594, H=24, pose='hold', skin='#d9a37a', hair='#2a1d14', shirt='#3f5f8a', pants='#1f2433', name='laser_person')
    f = frog(250, 1640, 2.4, look=(4, -4), mouth='O', hat=NIGHTCAP, mid=suit('#9fb8e8', '#6f8fd0'), sleeve='#9fb8e8',
             armL='M-34 -22 q-18 -4 -24 -26', armR='M38 -22 q18 -6 22 -30')
    return out(1, '#070b24', d, b, f, [('LASER', 170, 'w'), ('BEATS LIGHT?', 128, 'y')], 920, (hx, hy, 330, '#ffd6c8', '#ff5a4a', .55), ('#ffc8c0', '#fff'))


# ---------------- 2: giant scissors, cut point racing; hand shadow on the dust cloud ----------------
def s2():
    rnd = random.Random(2)
    d = rad('neb2', 620, 380, 620, [(0, '#e0784a', .75), (.5, '#8a3a5a', .45), (1, '#1a0a24', 0)])
    b = '<rect width="1080" height="1920" fill="#0c0618"/>' + sky(rnd, 220)
    b += '<rect width="1080" height="1100" fill="url(#neb2)"/>'
    for _ in range(26):
        b += f'<ellipse cx="{rnd.uniform(200, 1050):.0f}" cy="{rnd.uniform(80, 760):.0f}" rx="{rnd.uniform(60, 180):.0f}" ry="{rnd.uniform(30, 90):.0f}" fill="{rnd.choice(["#ffb07a", "#d0607a", "#7a3a8a"])}" opacity="{rnd.uniform(.08, .2):.2f}" filter="url(#b24)"/>'
    # hand shadow sweeping across the cloud (three motion ghosts)
    for k, (dx, op) in enumerate(((-140, .3), (-70, .5), (0, .85))):
        b += f'<g transform="translate({700 + dx} 300) rotate(-12) scale(4)" opacity="{op}" filter="url(#b3)">{hand("open", 0, 40, size=40, skin="#12060e", line="#12060e")}</g>'
    # scissors
    sd, so = scissors(250, 700, 760, -48, 16, 's2')
    d += sd; b += so
    a = math.radians(-48)
    px, py = 250 + math.cos(a) * 250, 700 + math.sin(a) * 250
    tx, ty = 250 + math.cos(a) * 720, 700 + math.sin(a) * 720
    b += glow_line(px, py, tx, ty, '#fff2b0', 6, 40, .9, 'b12')
    b += f'<circle cx="{px:.0f}" cy="{py:.0f}" r="90" fill="#fff0a8" opacity=".75" filter="url(#b24)"/><circle cx="{px:.0f}" cy="{py:.0f}" r="18" fill="#fff"/>'
    b += spark(px, py, 60, '#ffffff', .95)
    # Mars beside the blade tips
    b += f'<circle cx="930" cy="190" r="46" fill="#d0603a"/><circle cx="918" cy="178" r="40" fill="#e88a5a" opacity=".5"/><circle cx="930" cy="190" r="70" fill="#ff8a5a" opacity=".25" filter="url(#b12)"/>'
    f = frog(800, 1700, 2.4, look=(-4, -4), mouth='O', helmet=True, armL='M-34 -22 q-20 -6 -26 -30', armR='M38 -22 q20 -6 24 -30')
    return out(2, '#0c0618', d, b, f, [('CUT FASTER', 140, 'w'), ('THAN LIGHT?', 140, 'y')], 920, (px, py, 360, '#fff6d0', '#ffb070', .6), ('#ffd8b0', '#fff6e0'))


# ---------------- 3: Cherenkov blue glow ----------------
def s3():
    rnd = random.Random(3); CX, CY = 540, 520
    d = rad('w3', CX, CY, 700, [(0, '#e8fbff', 1), (.15, '#6fe0ff', .9), (.45, '#1478e0', .5), (1, '#020a24', 0)])
    b = '<rect width="1080" height="1920" fill="#020a24"/>'
    for k in range(1, 9):
        r = 90 * k
        b += f'<rect x="{CX - r}" y="{CY - r}" width="{2 * r}" height="{2 * r}" fill="none" stroke="#3a90ff" stroke-width="2" opacity="{.25 - k * .02:.2f}"/>'
    for k in range(-6, 7):
        b += f'<path d="M{CX} {CY} L{CX + k * 180} -400 M{CX} {CY} L{CX + k * 180} 1500" stroke="#3a90ff" stroke-width="2" opacity=".12"/>'
    b += '<rect width="1080" height="1920" fill="url(#w3)"/>'
    core = ''
    for i in range(-3, 4):
        for j in range(-3, 4):
            if abs(i) + abs(j) > 4: continue
            x, y = CX + i * 66 - 27, CY + j * 66 - 27; op = max(.3, 1 - math.hypot(i, j) * .18)
            core += f'<rect x="{x}" y="{y}" width="54" height="54" rx="5" fill="#9fe8ff" stroke="#0a3a8a" stroke-width="3" opacity="{op:.2f}"/>'
            for u in range(3):
                for v in range(3):
                    core += f'<circle cx="{x + 11 + u * 16}" cy="{y + 11 + v * 16}" r="4.6" fill="#fff" opacity="{op:.2f}"/>'
    b += core + f'<g filter="url(#b12)" opacity=".8">{core}</g>'
    for k in range(30):
        a = k / 30 * 2 * math.pi; L = rnd.uniform(350, 650)
        b += f'<path d="M{CX} {CY} L{CX + math.cos(a - .03) * L:.0f} {CY + math.sin(a - .03) * L:.0f} L{CX + math.cos(a + .03) * L:.0f} {CY + math.sin(a + .03) * L:.0f} Z" fill="#9fe8ff" opacity="{rnd.uniform(.05, .12):.2f}"/>'
    EX, EY = 300, 330; ang = math.atan2(-1, 1.6) + math.pi; half = math.radians(18); L = 520
    # head upper-left, moving up-left; wake opens back toward lower-right
    ang = math.atan2(330 - 130, 300 - 960) + math.pi  # direction from head back toward the tail
    ang = math.atan2(EY - 120, EX - 60) * 0 + math.radians(20)
    for kk in range(4):
        hh = half * (1 - kk * .14)
        for sgn in (-1, 1):
            q2 = (EX + math.cos(ang + sgn * hh) * L * (1 - kk * .1), EY + math.sin(ang + sgn * hh) * L * (1 - kk * .1))
            b += glow_line(EX, EY, q2[0], q2[1], '#d8fbff', 4.5 - kk * .8, 18, .9 - kk * .15)
    b += glow_line(EX, EY, EX + math.cos(ang) * 560, EY + math.sin(ang) * 560, '#ffffff', 6, 34, 1, 'b12')
    b += f'<circle cx="{EX}" cy="{EY}" r="70" fill="#bff6ff" opacity=".75" filter="url(#b24)"/><circle cx="{EX}" cy="{EY}" r="16" fill="#fff"/>' + spark(EX, EY, 50, '#ffffff', .95)
    for _ in range(50):
        b += f'<circle cx="{rnd.uniform(40, 1040):.0f}" cy="{rnd.uniform(80, 1850):.0f}" r="{rnd.choice([3, 5, 7])}" fill="none" stroke="#d8f6ff" stroke-width="1.6" opacity="{rnd.uniform(.25, .55):.2f}"/>'
    f = frog(270, 1720, 2.4, look=(4, -5), mouth='O', hat=HARDHAT, mid=suit('#f2c230', None, -34), sleeve='#f2c230',
             armL='M-34 -22 q-10 -12 -6 -34', armR='M38 -22 q18 -8 26 -30')
    return out(3, '#020a24', d, b, f, [('IT OVERTOOK', 132, 'w'), ('LIGHT', 210, 'y')], 900, (CX, CY, 520, '#e8fbff', '#3ab8ff', .7), ('#bfefff', '#fff'))


# ---------------- 4: entangled pair, Earth and Saturn ----------------
def s4():
    rnd = random.Random(4)
    d = rad('earth4', 220, 620, 200, [(0, '#8fd0ff', 1), (.6, '#2a6ac0', 1), (1, '#0a1a40', 1)])
    d += rad('sat4', 760, 260, 200, [(0, '#fff0c8', 1), (.6, '#d8b070', 1), (1, '#5a4020', 1)])
    d += '<clipPath id="e4"><circle cx="250" cy="650" r="150"/></clipPath>'
    b = '<rect width="1080" height="1920" fill="#05061a"/>' + sky(rnd, 300)
    # Saturn (back ring half, globe, front ring half)
    ring = lambda part: f'<path d="{part}" fill="none" stroke="#e8d2a0" stroke-width="22" opacity=".85"/><path d="{part}" fill="none" stroke="#b89a68" stroke-width="8" opacity=".9"/>'
    b += f'<g transform="rotate(-18 780 280)">{ring("M560 280 A220 60 0 0 1 1000 280")}</g>'
    b += '<circle cx="780" cy="280" r="130" fill="url(#sat4)"/>'
    b += '<g opacity=".25"><path d="M660 250 q120 -20 240 0" stroke="#8a6a3a" stroke-width="12" fill="none"/><path d="M655 300 q125 -16 250 0" stroke="#8a6a3a" stroke-width="10" fill="none"/></g>'
    b += f'<g transform="rotate(-18 780 280)">{ring("M560 280 A220 60 0 0 0 1000 280")}</g>'
    # Earth
    b += '<circle cx="250" cy="650" r="170" fill="#6fb8ff" opacity=".3" filter="url(#b24)"/><circle cx="250" cy="650" r="150" fill="url(#earth4)"/>'
    b += '<g clip-path="url(#e4)"><path d="M150 560 q40 -30 80 0 q30 30 0 70 q-40 20 -70 -10 q-30 -30 -10 -60z M260 650 q50 -20 80 20 q10 50 -40 80 q-40 10 -50 -30z" fill="#5aa35a" opacity=".9"/>'
    b += '<path d="M120 700 q80 -20 170 10" stroke="#fff" stroke-width="10" fill="none" opacity=".5" filter="url(#b3)"/></g>'
    # the link between the two particles (two twisted glowing strands)
    A, B = (420, 600), (640, 400)
    for ph, col in ((0, '#9ff6ff'), (math.pi, '#e0a8ff')):
        pts = []
        for k in range(41):
            t = k / 40; x = A[0] + (B[0] - A[0]) * t; y = A[1] + (B[1] - A[1]) * t
            off = math.sin(t * 4 * math.pi + ph) * 22; nx, ny = .67, .74
            pts.append((x + nx * off, y + ny * off))
        b += f'<path d="{smooth(pts)}" fill="none" stroke="{col}" stroke-width="14" opacity=".4" filter="url(#b6)"/><path d="{smooth(pts)}" fill="none" stroke="{col}" stroke-width="4"/>'
    for (x, y), col, up in ((A, '#7ff0ff', True), (B, '#d79bff', False)):
        b += f'<circle cx="{x}" cy="{y}" r="80" fill="{col}" opacity=".6" filter="url(#b24)"/><circle cx="{x}" cy="{y}" r="34" fill="{col}" stroke="#fff" stroke-width="4"/><circle cx="{x - 10}" cy="{y - 10}" r="10" fill="#fff" opacity=".8"/>'
        s = -1 if up else 1
        b += f'<path d="M{x} {y + 46 * -s} L{x} {y + 100 * s}" stroke="#fff" stroke-width="8" stroke-linecap="round"/><path d="M{x - 18} {y + 80 * s} L{x} {y + 104 * s} L{x + 18} {y + 80 * s}" fill="none" stroke="#fff" stroke-width="8" stroke-linecap="round" stroke-linejoin="round"/>'
    f = frog(780, 1700, 2.4, look=(-3, -5), mouth='O', helmet=True, armL='M-34 -22 q-20 -6 -26 -30', armR='M38 -22 q20 -6 24 -30')
    return out(4, '#05061a', d, b, f, [('SPOOKY', 190, 'y'), ('BUT NO MESSAGE', 108, 'w')], 900, (530, 500, 420, '#f4e8ff', '#9a7aff', .5), ('#e0d0ff', '#fff'))


# ---------------- 5: raisin-bread universe ----------------
def s5():
    rnd = random.Random(5)
    d = lin('crust5', [(0, '#f6c27a'), (.5, '#c97a36'), (1, '#6a3a18')])
    d += rad('in5', 540, 520, 420, [(0, '#fff2c8', .9), (1, '#f0b060', 0)])
    d += '<clipPath id="loaf5"><path d="M110 800 C100 420 300 230 540 230 C780 230 980 420 970 800 Z"/></clipPath>'
    b = '<rect width="1080" height="1920" fill="#0a0716"/>' + sky(rnd, 300)
    b += '<path d="M110 800 C100 420 300 230 540 230 C780 230 980 420 970 800 Z" fill="#ffb060" opacity=".35" filter="url(#b50)"/>'
    b += '<path d="M110 800 C100 420 300 230 540 230 C780 230 980 420 970 800 Z" fill="url(#crust5)" stroke="#3a1e0a" stroke-width="6"/>'
    b += '<g clip-path="url(#loaf5)"><ellipse cx="540" cy="520" rx="420" ry="300" fill="url(#in5)"/>'
    for k in range(3):
        x = 330 + k * 210
        b += f'<path d="M{x - 70} {380 + abs(k - 1) * 40} q70 -50 140 0" fill="none" stroke="#8a4a1e" stroke-width="10" opacity=".55"/><path d="M{x - 66} {372 + abs(k - 1) * 40} q66 -44 132 0" fill="none" stroke="#ffe0a0" stroke-width="4" opacity=".6"/>'
    b += '<path d="M150 760 q390 40 780 0" stroke="#3a1e0a" stroke-width="8" fill="none" opacity=".4"/></g>'
    # raisin galaxies + outward arrows from the centre
    G = [(540, 520, 46, '#d8e6ff'), (330, 470, 38, '#ffd8b0'), (760, 450, 40, '#c8f0ff'), (250, 680, 34, '#e8d0ff'), (820, 660, 36, '#ffe6c0'), (430, 680, 30, '#cfe0ff'), (650, 330, 30, '#ffd0e0'), (560, 720, 26, '#d0ffe8')]
    for i, (x, y, r, c) in enumerate(G):
        b += f'<circle cx="{x}" cy="{y}" r="{r * .9:.0f}" fill="#1a0c22" opacity=".85"/>'
        b += galaxy(x, y, r, rnd.uniform(0, 180), c, uid=f'g5{i}', tilt=.6)
        if i:
            dx, dy = x - 540, y - 520; m = math.hypot(dx, dy); ux, uy = dx / m, dy / m
            sx, sy = x + ux * (r + 8), y + uy * (r + 8); ex, ey = sx + ux * 46, sy + uy * 46
            b += f'<path d="M{sx:.0f} {sy:.0f} L{ex:.0f} {ey:.0f}" stroke="#fff6e0" stroke-width="6" stroke-linecap="round"/>'
            b += f'<path d="M{ex - uy * 10 - ux * 12:.0f} {ey + ux * 10 - uy * 12:.0f} L{ex + ux * 4:.0f} {ey + uy * 4:.0f} L{ex + uy * 10 - ux * 12:.0f} {ey - ux * 10 - uy * 12:.0f}" fill="none" stroke="#fff6e0" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/>'
    for x, y, s in ((140, 260, 24), (950, 300, 20), (980, 760, 16)):
        b += spark(x, y, s)
    f = frog(260, 1700, 2.4, look=(4, -5), mouth='O', hat=CHEFHAT, armL='M-34 -22 q-20 -6 -26 -30', armR='M38 -22 q20 -6 24 -30')
    return out(5, '#0a0716', d, b, f, [('SPACE', 190, 'w'), ('IS STRETCHING', 112, 'y')], 900, (540, 520, 520, '#fff0c8', '#ffa050', .6), ('#ffe0b0', '#fff8e8'))


if __name__ == '__main__':
    for n in [int(a) for a in sys.argv[1:]] or [1, 2, 3, 4, 5]:
        p = os.path.join(REPO, f'videos/faster-than-light-illusions-short{n}/thumb/A.html')
        open(p, 'w').write(globals()[f's{n}']())
    print('ok')
