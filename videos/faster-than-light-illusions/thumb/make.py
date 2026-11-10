# Thumbnails A-C for faster-than-light-illusions (guideline 16-6 / 16-8, brief tools/briefs/thumb_art.md).
# Run: python3 videos/faster-than-light-illusions/thumb/make.py ; then SLUG=faster-than-light-illusions python3 tools/thumb_shot.py
# A  FASTER / THAN LIGHT?   homage: Star Wars "jump to lightspeed" (stars stretch into starlines toward one bright point); a small
#                           generic ship (not any film ship) dives in, the frog in a space helmet clings to its back. Script: c is the
#                           cosmic limit, "Nothing can travel faster than this speed" -> question.
# B  IT BROKE / PHYSICS?    intuitive: rooftop at night, a person flicks a laser pointer; the red dot races across a huge full Moon
#                           (script: "Has your laser pointer just broken the ultimate law of physics?"); frog in pyjamas + nightcap.
# C  LIGHT'S / SONIC BOOM   intuitive: looking down into a reactor pool, fuel rods glow Cherenkov blue, an electron streaks through
#                           the water with a cone-shaped shock wake (script: optical shock wave like an aircraft's sonic boom);
#                           frog in a yellow hazard suit and hard hat at the railing.
import os, sys, math, random
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from ftl_art import *


# =========================== A: Star Wars jump-to-lightspeed homage ===========================
def ship(x, y, s, rot):
    o = f'<g transform="translate({x} {y}) rotate({rot}) scale({s})" stroke="#141a2a" stroke-width="3.2" stroke-linejoin="round">'
    # side wings
    for sx in (-1, 1):
        o += f'<path d="M{sx * 60} -6 L{sx * 178} 26 L{sx * 186} 46 L{sx * 70} 34 Z" fill="#9aa6bd"/>'
        o += f'<path d="M{sx * 120} 16 L{sx * 176} 30" stroke="#e9eef8" stroke-width="2.4" opacity=".7"/>'
        o += f'<rect x="{sx * 186 - 9}" y="12" width="18" height="44" rx="7" fill="#c3ccdc"/>'
        o += f'<circle cx="{sx * 186}" cy="58" r="7" fill="#9fe6ff" stroke="none"/>'
    # hull (seen from behind, slightly above)
    o += '<path d="M-92 20 C-96 -40 -50 -74 0 -76 C50 -74 96 -40 92 20 C80 54 -80 54 -92 20 Z" fill="url(#hullA)"/>'
    o += '<path d="M-70 -30 C-40 -60 40 -60 70 -30" fill="none" stroke="#ffffff" stroke-width="3" opacity=".6"/>'
    for px in (-48, -16, 16, 48):
        o += f'<path d="M{px} -52 L{px * 1.15:.0f} 30" stroke="#5f6b84" stroke-width="2" opacity=".7"/>'
    o += '<path d="M-86 0 C-40 12 40 12 86 0" fill="none" stroke="#5f6b84" stroke-width="2"/>'
    o += '<rect x="-30" y="-44" width="22" height="12" rx="3" fill="#d6453d" stroke-width="2"/><rect x="10" y="-40" width="26" height="8" rx="3" fill="#f2d27a" stroke-width="2"/>'
    # engines (glowing toward the viewer)
    for ex in (-46, 0, 46):
        o += f'<ellipse cx="{ex}" cy="34" rx="24" ry="16" fill="#2a3346"/>'
        o += f'<ellipse cx="{ex}" cy="36" rx="18" ry="11" fill="#7fe0ff" stroke="none"/>'
        o += f'<ellipse cx="{ex}" cy="36" rx="9" ry="5" fill="#ffffff" stroke="none"/>'
    o += '</g>'
    glow = ''.join(f'<circle cx="{x + (ex * math.cos(math.radians(rot)) - 36 * math.sin(math.radians(rot))) * s:.0f}" cy="{y + (ex * math.sin(math.radians(rot)) + 36 * math.cos(math.radians(rot))) * s:.0f}" r="{46 * s:.0f}" fill="#6fd8ff" opacity=".55" filter="url(#b24)"/>' for ex in (-46, 0, 46))
    return o + glow


def make_A():
    rnd = random.Random(7)
    VX, VY = 1270, 470
    d = FILTERS + FROG_DEFS
    d += rad('coreA', VX, VY, 520, [(0, '#ffffff', 1), (.08, '#e6f6ff', .95), (.3, '#5ab8ff', .45), (.7, '#1a3a9a', .15), (1, '#050818', 0)])
    d += rad('vigA', 960, 540, 1150, [(.55, '#000', 0), (1, '#000', .75)])
    d += rad('txtA', 300, 180, 700, [(0, '#02040d', .75), (1, '#02040d', 0)])
    d += lin('hullA', [(0, '#eef2fa'), (.55, '#b7c1d4'), (1, '#6c7891')])
    b = '<rect width="1920" height="1080" fill="#03050f"/>'
    b += '<rect width="1920" height="1080" fill="url(#coreA)"/>'
    lines, glow = '', ''
    for _ in range(620):
        a = rnd.uniform(0, 2 * math.pi)
        r0 = 30 + 1300 * rnd.random() ** 1.6
        r1 = r0 * rnd.uniform(1.35, 2.1) + 40
        w = .8 + r0 / 260
        c = rnd.choice(['#ffffff', '#ffffff', '#cfeeff', '#9fd2ff', '#b8b0ff'])
        x0, y0 = VX + math.cos(a) * r0, VY + math.sin(a) * r0 * .82
        x1, y1 = VX + math.cos(a) * r1, VY + math.sin(a) * r1 * .82
        op = rnd.uniform(.45, 1)
        lines += f'<path d="M{x0:.0f} {y0:.0f} L{x1:.0f} {y1:.0f}" stroke="{c}" stroke-width="{w:.1f}" stroke-linecap="round" opacity="{op:.2f}"/>'
        if rnd.random() < .35:
            glow += f'<path d="M{x0:.0f} {y0:.0f} L{x1:.0f} {y1:.0f}" stroke="#7cc8ff" stroke-width="{w * 4:.1f}" stroke-linecap="round" opacity=".5"/>'
    b += f'<g filter="url(#b6)">{glow}</g>' + lines
    # bright point + ring flash
    b += f'<circle cx="{VX}" cy="{VY}" r="70" fill="#fff" opacity=".9" filter="url(#b24)"/><circle cx="{VX}" cy="{VY}" r="22" fill="#fff"/>'
    b += f'<ellipse cx="{VX}" cy="{VY}" rx="230" ry="190" fill="none" stroke="#bfe8ff" stroke-width="6" opacity=".35" filter="url(#b3)"/>'
    b += f'<path d="M{VX - 420} {VY} L{VX + 420} {VY}" stroke="#ffffff" stroke-width="5" opacity=".7" filter="url(#b3)"/>'
    b += '<rect width="1920" height="1080" fill="url(#txtA)"/>'
    # ship diving toward the point, frog clinging on its back
    b += ship(940, 800, 1.95, -12)
    b += frog(918, 686, 2.35, rot=-13, look=(4, -2), mouth='O', helmet=True,
              armL='M-34 -22 q-24 4 -30 22', armR='M38 -22 q22 2 30 20',
              legs=((-20, -6, -34, 6, -20), (20, -6, 36, 6, 20)))
    for x, y, s in ((1580, 220, 22), (1700, 640, 16), (980, 360, 14), (1420, 820, 14)):
        b += spark(x, y, s, '#ffffff')
    b += '<rect width="1920" height="1080" fill="url(#vigA)"/>'
    return page('#03050f', svg(d, b), [('FASTER', 230, 'y'), ('THAN LIGHT?', 140, 'w')])


# =========================== B: laser dot racing across the Moon ===========================
def make_B():
    rnd = random.Random(11)
    MX, MY, MR = 1360, 440, 400
    d = FILTERS + FROG_DEFS
    d += lin('skyB', [(0, '#060a22'), (.6, '#121a4a'), (1, '#2a2460')])
    d += rad('vigB', 960, 540, 1150, [(.6, '#000', 0), (1, '#000', .6)])
    d += lin('roofB', [(0, '#262c45'), (1, '#0c0f1c')])
    md, mo = moon(MX, MY, MR, 'B'); d += md
    b = '<rect width="1920" height="1080" fill="url(#skyB)"/>'
    b += starfield(rnd, 260, y1=900)
    b += f'<circle cx="{MX}" cy="{MY}" r="{MR * 1.6:.0f}" fill="#bcd0ff" opacity=".18" filter="url(#b80)"/>'
    b += mo
    # distant city glow at the horizon
    b += '<rect x="0" y="930" width="1920" height="150" fill="#3a2e6a" opacity=".5" filter="url(#b24)"/>'
    for _ in range(90):
        x = rnd.uniform(560, 1900); y = rnd.uniform(960, 1060)
        b += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{rnd.choice([2, 3, 4])}" fill="{rnd.choice(["#ffd98a", "#ffe9c0", "#ffb070"])}" opacity="{rnd.uniform(.3, .8):.2f}"/>'
    # red dot path across the lunar face: arc left -> right
    p0, p1, p2 = (MX - 330, MY + 150), (MX - 20, MY - 40), (MX + 300, MY - 60)
    def q(t):
        return ((1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * p1[0] + t * t * p2[0], (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * p1[1] + t * t * p2[1])
    # laser source = the person's fist on the roof
    SX, SY = 452, 846
    for t in (0, .25, .5, .75):
        x, y = q(t)
        b += f'<path d="M{SX} {SY} L{x:.0f} {y:.0f}" stroke="#ff3b3b" stroke-width="3" opacity="{.08 + t * .14:.2f}"/>'
    hx, hy = q(1)
    b += glow_line(SX, SY, hx, hy, '#ff3030', 4.5, 22, 1, 'b6')
    b += f'<path d="M{p0[0]} {p0[1]} Q{p1[0]} {p1[1]} {p2[0]} {p2[1]}" fill="none" stroke="#ff2a2a" stroke-width="44" opacity=".35" filter="url(#b12)" stroke-linecap="round"/>'
    b += f'<path d="M{p0[0]} {p0[1]} Q{p1[0]} {p1[1]} {p2[0]} {p2[1]}" fill="none" stroke="#ff5a4a" stroke-width="10" opacity=".55" stroke-linecap="round"/>'
    for k in range(12):
        t = k / 12; x, y = q(t)
        b += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{8 + 10 * t:.0f}" fill="#ff3b30" opacity="{.15 + .5 * t:.2f}"/>'
    b += f'<circle cx="{hx:.0f}" cy="{hy:.0f}" r="90" fill="#ff2a2a" opacity=".55" filter="url(#b24)"/>'
    b += f'<circle cx="{hx:.0f}" cy="{hy:.0f}" r="30" fill="#ff4a3a"/><circle cx="{hx:.0f}" cy="{hy:.0f}" r="14" fill="#fff4ec"/>'
    for k in range(3):
        b += f'<path d="M{hx + 50:.0f} {hy - 40 + k * 40:.0f} l{70 - k * 10} {-8 + k * 4}" stroke="#ffd0c8" stroke-width="5" stroke-linecap="round" opacity=".7"/>'
    b += spark(hx + 40, hy - 50, 26, '#ffffff')
    # rooftop (foreground) with chimney and antenna
    b += '<path d="M-20 1100 L-20 900 L640 870 L1100 1100 Z" fill="url(#roofB)" stroke="#05070f" stroke-width="5"/>'
    for k in range(9):
        b += f'<path d="M{-20 + k * 40} {900 - k * 3.4:.0f} L{120 + k * 120} 1100" stroke="#0a0d1a" stroke-width="3" opacity=".6"/>'
    b += '<path d="M-20 900 L640 870" stroke="#7d86b8" stroke-width="4" opacity=".7"/>'
    b += '<rect x="560" y="770" width="64" height="104" fill="#3a2a2e" stroke="#05070f" stroke-width="5"/><rect x="550" y="760" width="84" height="18" fill="#4a3638" stroke="#05070f" stroke-width="4"/>'
    b += '<path d="M592 760 q10 -40 -10 -80 q-14 -30 6 -60" fill="none" stroke="#aab4d8" stroke-width="14" opacity=".12" filter="url(#b6)"/>'
    # person with the laser pointer (figlib person, 'hold' pose)
    b += person(410, 886, H=26, pose='hold', skin='#d9a37a', hair='#2a1d14', shirt='#3f5f8a', pants='#1f2433', name='laser_person')
    b += f'<path d="M{SX - 10} {SY + 6} L{SX + 8} {SY - 4}" stroke="#1a1a1a" stroke-width="7" stroke-linecap="round"/>'
    # frog in pyjamas + nightcap, sitting on the roof ridge, staring up at the dot
    b += frog(255, 892, 2.8, rot=-3, look=(4, -4), mouth='O', hat=NIGHTCAP,
              mid=suit('#9fb8e8', '#6f8fd0'), sleeve='#9fb8e8',
              armL='M-34 -22 q-18 -4 -24 -26', armR='M38 -22 q18 -6 22 -30',
              legs=((-20, -6, -26, 4, -8), (20, -6, 28, 4, 8)))
    for x, y, s in ((1000, 120, 18), (1820, 260, 16), (880, 520, 14)):
        b += spark(x, y, s)
    b += '<rect width="1920" height="1080" fill="url(#vigB)"/>'
    return page('#060a22', svg(d, b), [('IT BROKE', 150, 'w'), ('PHYSICS?', 210, 'y')])


# =========================== C: Cherenkov glow in a reactor pool ===========================
def make_C():
    rnd = random.Random(23)
    CX, CY = 1240, 690
    d = FILTERS + FROG_DEFS
    d += lin('waterC', [(0, '#020a24'), (.5, '#06306e'), (1, '#0a2a66')])
    d += rad('glowC', CX, CY, 760, [(0, '#e8fbff', 1), (.12, '#7fe8ff', .95), (.35, '#1fa6ff', .6), (.7, '#0a46b8', .25), (1, '#020a24', 0)])
    d += rad('vigC', 960, 540, 1150, [(.55, '#000', 0), (1, '#000', .7)])
    d += rad('txtC', 280, 170, 700, [(0, '#010614', .7), (1, '#010614', 0)])
    d += lin('railC', [(0, '#c9d2e0'), (1, '#6c7891')])
    b = '<rect width="1920" height="1080" fill="url(#waterC)"/>'
    # pool walls: tile lines converging to the core (perspective, looking down)
    W0 = [(-200, -100), (2120, -100), (2120, 1180), (-200, 1180)]
    IN = [(CX - 330, CY - 220), (CX + 330, CY - 220), (CX + 330, CY + 220), (CX - 330, CY + 220)]
    for i in range(4):
        a0, a1 = W0[i], W0[(i + 1) % 4]; c0, c1 = IN[i], IN[(i + 1) % 4]
        shade = ['#04204e', '#052a62', '#06347a', '#042658'][i]
        b += f'<path d="M{a0[0]} {a0[1]} L{a1[0]} {a1[1]} L{c1[0]} {c1[1]} L{c0[0]} {c0[1]} Z" fill="{shade}"/>'
        for k in range(1, 14):
            t = k / 14
            b += f'<path d="M{a0[0] + (a1[0] - a0[0]) * t:.0f} {a0[1] + (a1[1] - a0[1]) * t:.0f} L{c0[0] + (c1[0] - c0[0]) * t:.0f} {c0[1] + (c1[1] - c0[1]) * t:.0f}" stroke="#5fb0ff" stroke-width="2" opacity=".18"/>'
        for k in range(1, 9):
            t = 1 - (1 - k / 9) ** 1.8
            p, q2 = [(a0[0] + (c0[0] - a0[0]) * t, a0[1] + (c0[1] - a0[1]) * t), (a1[0] + (c1[0] - a1[0]) * t, a1[1] + (c1[1] - a1[1]) * t)]
            b += f'<path d="M{p[0]:.0f} {p[1]:.0f} L{q2[0]:.0f} {q2[1]:.0f}" stroke="#5fb0ff" stroke-width="2" opacity=".16"/>'
    b += f'<rect x="{CX - 340}" y="{CY - 230}" width="680" height="460" rx="20" fill="#021030" opacity=".85" filter="url(#b12)"/>'
    b += '<rect width="1920" height="1080" fill="url(#glowC)" opacity=".9"/>'
    # fuel assemblies at the bottom (grid of square tops)
    core = ''
    for i in range(9):
        for j in range(6):
            x = CX - 300 + i * 66; y = CY - 200 + j * 66
            dd = math.hypot((x + 27 - CX) / 330, (y + 27 - CY) / 220); op = max(.25, 1 - dd * .75)
            core += f'<rect x="{x}" y="{y}" width="54" height="54" rx="5" fill="#7fdcff" stroke="#0a3a8a" stroke-width="3" opacity="{op:.2f}"/>'
            for u in range(3):
                for v in range(3):
                    core += f'<circle cx="{x + 11 + u * 16}" cy="{y + 11 + v * 16}" r="4.6" fill="#ffffff" opacity="{op:.2f}"/>'
    b += f'<g opacity=".95">{core}</g><g filter="url(#b12)" opacity=".8">{core}</g>'
    b += f'<ellipse cx="{CX}" cy="{CY}" rx="460" ry="330" fill="#9ff0ff" opacity=".35" filter="url(#b50)"/>'
    # god rays rising toward the viewer
    for k in range(26):
        a = k / 26 * 2 * math.pi + rnd.uniform(-.05, .05)
        L = rnd.uniform(500, 950)
        b += f'<path d="M{CX} {CY} L{CX + math.cos(a - .03) * L:.0f} {CY + math.sin(a - .03) * L:.0f} L{CX + math.cos(a + .03) * L:.0f} {CY + math.sin(a + .03) * L:.0f} Z" fill="#9fe8ff" opacity="{rnd.uniform(.05, .12):.2f}"/>'
    # electron streak with Cherenkov cone wake (head lower-left, wake opens back toward upper-right)
    EX, EY = 1000, 500; TX, TY = 1660, 90
    ang = math.atan2(TY - EY, TX - EX); half = math.radians(17); L = 640
    pa = (EX + math.cos(ang - half) * L, EY + math.sin(ang - half) * L); pb = (EX + math.cos(ang + half) * L, EY + math.sin(ang + half) * L)
    b += f'<path d="M{EX} {EY} L{pa[0]:.0f} {pa[1]:.0f} L{pb[0]:.0f} {pb[1]:.0f} Z" fill="#7fe8ff" opacity=".22" filter="url(#b12)"/>'
    for k in range(5):
        hh = half * (1 - k * .12)
        for sgn in (-1, 1):
            q2 = (EX + math.cos(ang + sgn * hh) * L * (1 - k * .1), EY + math.sin(ang + sgn * hh) * L * (1 - k * .1))
            b += glow_line(EX, EY, q2[0], q2[1], '#d8fbff', 4 - k * .6, 18, .9 - k * .15, 'b6')
    b += glow_line(EX, EY, TX, TY, '#ffffff', 6, 36, 1, 'b12')
    b += f'<circle cx="{EX}" cy="{EY}" r="70" fill="#bff6ff" opacity=".7" filter="url(#b24)"/><circle cx="{EX}" cy="{EY}" r="16" fill="#ffffff"/>'
    b += spark(EX - 6, EY + 4, 46, '#ffffff', .95)
    # bubbles
    for _ in range(60):
        x = rnd.uniform(700, 1900); y = rnd.uniform(80, 1000); r = rnd.choice([3, 4, 6, 8])
        b += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r}" fill="none" stroke="#d8f6ff" stroke-width="1.6" opacity="{rnd.uniform(.25, .6):.2f}"/>'
    b += '<rect width="1920" height="1080" fill="url(#txtC)"/>'
    # foreground: walkway railing at the bottom-left, frog in a hazard suit leaning over, lit blue from below
    b += '<path d="M-20 1100 L-20 900 L900 1000 L940 1100 Z" fill="#141c2e" stroke="#05070f" stroke-width="5"/>'
    b += '<path d="M-20 900 L900 1000" stroke="#7fd8ff" stroke-width="5" opacity=".7"/>'
    for x in (60, 300, 560, 820):
        y = 900 + (x + 20) * 100 / 920
        b += f'<rect x="{x - 9}" y="{y - 170:.0f}" width="18" height="170" fill="url(#railC)" stroke="#05070f" stroke-width="4"/>'
    b += '<path d="M-20 730 L900 830" stroke="#05070f" stroke-width="26" stroke-linecap="round"/><path d="M-20 730 L900 830" stroke="#f2c230" stroke-width="16" stroke-linecap="round"/>'
    b += '<path d="M-20 726 L900 826" stroke="#fff3b0" stroke-width="4" opacity=".7"/>'
    b += frog(420, 800, 2.9, rot=6, look=(4, 4), mouth='O', hat=HARDHAT,
              mid=suit('#f2c230', None, -34) + '<rect x="-14" y="-26" width="34" height="14" rx="3" fill="#2a2a2a" stroke-width="2.4"/><path d="M-8 -19 l6 -4 l0 8z M8 -19 l6 -4 l0 8z" fill="#f2c230" stroke="none"/>',
              sleeve='#f2c230', armL='M-34 -22 q-10 -12 -6 -34', armR='M38 -22 q18 -8 26 -30',
              front='<path d="M-30 -60 q-6 30 4 58" fill="none" stroke="#9ff0ff" stroke-width="3" opacity=".6"/>')
    for x, y, s in ((1560, 860, 22), (900, 420, 16), (1760, 520, 16), (1300, 160, 14)):
        b += spark(x, y, s, '#e8fdff')
    b += '<rect width="1920" height="1080" fill="url(#vigC)"/>'
    return page('#020a24', svg(d, b), [("LIGHT'S", 150, 'w'), ('SONIC BOOM', 160, 'y')])


if __name__ == '__main__':
    for n in sys.argv[1:] or ['A', 'B', 'C']:
        open(os.path.join(HERE, f'{n}.html'), 'w').write(globals()[f'make_{n}']())
    print('ok')
