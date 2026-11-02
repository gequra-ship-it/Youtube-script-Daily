# Thumbnails A-C for sharpest-blade-fastest-gun (guideline 16-6, brief tools/briefs/thumb_art.md).
# A = homage to The Matrix bullet-time: frog in a long coat bends back in the LHC tunnel as glowing protons pass (S32-S33: 99.9999991% of light speed)
# B = intuitive: a magnifier bubble over a kitchen-knife edge shows a jagged steel mountain range; a single-atom needle tip glows above it (S02, S18-S19)
# C = homage to 2001: A Space Odyssey bone-to-satellite match cut: a thrown flint knife tumbles toward the LHC ring floating like the wheel station (S39, S31)
# run: python3 make.py
import os, sys, math, random
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', '..', 'tools'))
from thumb_lib import page, svg, lin, rad, spark

INK = '#1d2b1c'; GREEN = '#6aa55a'; DARKG = '#4d8a4a'; BELLY = '#9cc98a'
SOFT = ('<filter id="soft" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="3"/></filter>'
        '<filter id="blur6" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="6"/></filter>'
        '<filter id="blur12" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="12"/></filter>'
        '<filter id="blur30" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="30"/></filter>')


def corner(x, y):   # bottom-right stays empty (duration badge)
    return x > 1540 and y > 820


def starfield(rnd, n, box, skip=None, col='#eef4ff', omax=.7):
    x0, y0, x1, y1 = box; out = ''
    for _ in range(n):
        x, y = rnd.randint(x0, x1), rnd.randint(y0, y1)
        if skip and skip(x, y): continue
        out += f'<circle cx="{x}" cy="{y}" r="{rnd.choice([1, 1.4, 1.9, 2.6])}" fill="{col}" opacity="{.12 + omax * rnd.random():.2f}"/>'
    return out


def rot(px, py, a, s=1.0):   # rotate a frog-local point by a degrees (SVG clockwise), scale s
    t = math.radians(a)
    return (px * s * math.cos(t) - py * s * math.sin(t), px * s * math.sin(t) + py * s * math.cos(t))


# ---------- mascot frog (tools/assets/frog.svg), posable ----------
def arm(d):
    return (f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="7.5"/>'
            f'<path d="{d}" fill="none" stroke="{GREEN}" stroke-width="3.4"/>')


def frog(x, y, s, flip=False, look=(0, 0), mouth='o', armL=None, armR=None, feet=None, rot_=0,
         back='', front='', helmet=None, nofeet=False):
    sx = -s if flip else s
    g = [f'<g transform="translate({x} {y}) rotate({rot_}) scale({sx} {s})" stroke="{INK}" stroke-linejoin="round" stroke-linecap="round">', back]
    if not nofeet:
        fl, fr = feet or ((-22, 4, 0), (22, 4, 0))
        for fx, fy, fa in (fl, fr):
            g.append(f'<ellipse cx="{fx}" cy="{fy}" rx="16" ry="9" transform="rotate({fa} {fx} {fy})" fill="{DARKG}" stroke-width="3.2"/>')
    g.append(f'<path d="M-34 0 q-6 -64 34 -70 q40 -2 42 62 q0 10 -6 12 q-36 6 -70 -4z" fill="{GREEN}" stroke-width="4"/>')
    g.append(f'<ellipse cx="2" cy="-12" rx="22" ry="20" fill="{BELLY}" stroke="none" opacity=".7"/>')
    g.append(f'<path d="M-24 -50 q6 -14 18 -16" fill="none" stroke="#a9d692" stroke-width="3" opacity=".8"/>')
    lx, ly = look
    for ex in (-10, 22):
        g.append(f'<circle cx="{ex}" cy="-66" r="13" fill="#f4f5ea" stroke-width="3.2"/>')
        g.append(f'<circle cx="{ex + 2 + lx}" cy="{-66 + ly}" r="5.4" fill="{INK}" stroke="none"/>')
        g.append(f'<circle cx="{ex + 3.6 + lx}" cy="{-68 + ly}" r="1.7" fill="#fff" stroke="none"/>')
    if mouth == 'o':
        g.append('<ellipse cx="6" cy="-42" rx="5.5" ry="6.5" fill="#3a1d1d" stroke-width="2.6"/>')
    else:
        g.append('<path d="M-8 -44 q14 12 28 0" fill="none" stroke-width="3.4"/>')
    g.append('<ellipse cx="-16" cy="-50" rx="5" ry="3" fill="#e88f86" stroke="none" opacity=".55"/><ellipse cx="28" cy="-50" rx="5" ry="3" fill="#e88f86" stroke="none" opacity=".55"/>')
    g.append(front)
    aL = armL or 'M-34 -22 q-14 6 -16 22'
    aR = armR or 'M38 -22 q14 6 16 22'
    g.append(arm(aL)); g.append(arm(aR))
    for a in (aL, aR):
        nums = [float(v) for v in a.replace('M', ' ').replace('q', ' ').split()]
        g.append(f'<circle cx="{nums[0] + nums[-2]}" cy="{nums[1] + nums[-1]}" r="4.2" fill="{GREEN}" stroke="{INK}" stroke-width="2.4"/>')
    if helmet: g.append(helmet)
    g.append('</g>')
    return ''.join(g)


# =========================== A: Matrix bullet-time in the LHC tunnel ===========================
def proton(x, y, r, vx, vy, gid, n=7, tint='#9ff7c9'):
    L = math.hypot(vx, vy); TL = min(r * 26, L * .85); ux, uy = vx / L, vy / L; ang = math.degrees(math.atan2(uy, ux))
    d = rad(f'{gid}h', x, y, r * 5, [(0, '#ffffff', 1), (.12, '#fff3c0', .95), (.3, '#F2D27A', .45), (.6, tint, .14), (1, tint, 0)])
    d += (f'<linearGradient id="{gid}t" x1="{x}" y1="{y}" x2="{x - ux * TL:.0f}" y2="{y - uy * TL:.0f}" gradientUnits="userSpaceOnUse">'
          f'<stop offset="0" stop-color="#fff6d0" stop-opacity=".9"/><stop offset=".3" stop-color="{tint}" stop-opacity=".35"/><stop offset="1" stop-color="{tint}" stop-opacity="0"/></linearGradient>')
    b = ''
    # wake: tapering streak behind the proton
    nx, ny = -uy, ux; w = r * .9; tx, ty = x - ux * TL, y - uy * TL
    b += f'<polygon points="{x + nx * w:.0f},{y + ny * w:.0f} {tx:.0f},{ty:.0f} {x - nx * w:.0f},{y - ny * w:.0f}" fill="url(#{gid}t)"/>'
    # bullet-time air ripples: rings seen almost edge-on, growing and fading behind
    for i in range(1, n + 1):
        dd = r * (1.6 + i * 2.9)
        if dd > TL * .8: break
        cx, cy = x - ux * dd, y - uy * dd
        ry = r * (1.25 + .42 * i); rx = r * (.34 + .06 * i); op = .75 * (1 - i / (n + 1.5))
        b += (f'<ellipse cx="{cx:.0f}" cy="{cy:.0f}" rx="{rx:.1f}" ry="{ry:.1f}" transform="rotate({ang:.1f} {cx:.0f} {cy:.0f})" fill="none" '
              f'fill="#e9fff2" fill-opacity="{op * .08:.3f}" stroke="#f4fff8" stroke-width="{max(2.2, r * .22):.1f}" opacity="{min(1, op * 1.2):.2f}"/>')
        b += (f'<ellipse cx="{cx - ux * r * .4:.0f}" cy="{cy - uy * r * .4:.0f}" rx="{rx * 1.15:.1f}" ry="{ry * 1.05:.1f}" transform="rotate({ang:.1f} {cx:.0f} {cy:.0f})" fill="none" '
              f'stroke="{tint}" stroke-width="{max(1.2, r * .1):.1f}" opacity="{op * .6:.2f}"/>')
    b += f'<circle cx="{x}" cy="{y}" r="{r * 5}" fill="url(#{gid}h)"/>'
    b += f'<circle cx="{x}" cy="{y}" r="{r}" fill="#fffaf0"/>'
    # quark-ish texture inside the proton (three soft lobes)
    for k, c in enumerate(('#ffd27a', '#ffe9b0', '#fff')):
        a = k * 2.1 + .4
        b += f'<circle cx="{x + math.cos(a) * r * .38:.1f}" cy="{y + math.sin(a) * r * .38:.1f}" r="{r * .36:.1f}" fill="{c}" opacity=".7"/>'
    return d, b


def make_A():
    rnd = random.Random(5)
    d = SOFT
    d += lin('aBg', [(0, '#020c06'), (.55, '#06180d'), (1, '#020805')])
    body = '<rect width="1920" height="1080" fill="url(#aBg)"/>'
    VX, VY, R = 1490, 470, 760
    # light at the end of the tunnel
    d += rad('vpG', VX, VY, 520, [(0, '#d9ffe6', .85), (.08, '#7dffb0', .45), (.35, '#1f8a4c', .14), (1, '#000', 0)])
    body += f'<rect width="1920" height="1080" fill="url(#vpG)"/>'
    # tunnel: rings receding into the vanishing point, with a flat floor
    FL = .45; s1 = math.sqrt(1 - FL * FL)
    fs = [.03 * 1.32 ** k for k in range(16)]
    d += lin('floorG', [(0, '#0b2a17'), (1, '#020a05')])
    far = fs[0]
    body += (f'<polygon points="{VX - R * far * s1:.0f},{VY + R * .9 * far * FL:.0f} {VX + R * far * s1:.0f},{VY + R * .9 * far * FL:.0f} '
             f'{VX + R * 6 * s1:.0f},{VY + R * .9 * 6 * FL:.0f} {VX - R * 6 * s1:.0f},{VY + R * .9 * 6 * FL:.0f}" fill="url(#floorG)"/>')
    for f in fs:
        rx, ry = R * f, R * .9 * f; fy = VY + ry * FL; xl, xr = VX - rx * s1, VX + rx * s1
        op = min(.9, .18 + f * .5)
        body += (f'<path d="M{xl:.0f} {fy:.0f} A{rx:.0f} {ry:.0f} 0 1 1 {xr:.0f} {fy:.0f}" fill="none" stroke="#020805" stroke-width="{4 + f * 22:.0f}" opacity=".9"/>'
                 f'<path d="M{xl:.0f} {fy:.0f} A{rx:.0f} {ry:.0f} 0 1 1 {xr:.0f} {fy:.0f}" fill="none" stroke="#2f9d5c" stroke-width="{1 + f * 5:.1f}" opacity="{op:.2f}"/>')
        body += f'<path d="M{xl:.0f} {fy:.0f} H{xr:.0f}" stroke="#3fbf73" stroke-width="{1 + f * 2:.1f}" opacity="{op * .35:.2f}"/>'
        # ceiling lamp
        body += f'<rect x="{VX - 26 * f:.0f}" y="{VY - ry - 3 * f:.0f}" width="{52 * f:.0f}" height="{8 * f + 1:.0f}" rx="{3 * f:.1f}" fill="#d8ffe6" opacity="{min(1, .4 + f):.2f}"/>'
        body += f'<ellipse cx="{VX}" cy="{VY - ry + 10 * f:.0f}" rx="{90 * f:.0f}" ry="{30 * f:.0f}" fill="#7dffb0" opacity=".10" filter="url(#blur12)"/>'
        # cable trays on the right wall
        a = math.radians(-28); cx_, cy_ = VX + rx * math.cos(a) * .97, VY + ry * math.sin(a) * .97
        body += f'<rect x="{cx_ - 6 * f:.0f}" y="{cy_ - 2 * f:.0f}" width="{12 * f:.0f}" height="{60 * f:.0f}" fill="#123d24" opacity=".8"/>'
    # cables running along the right wall
    for k, a0 in enumerate((-24, -16, -9)):
        a = math.radians(a0); p = []
        for f in (fs[0], 6):
            p.append((VX + R * f * math.cos(a) * .96, VY + R * .9 * f * math.sin(a) * .96))
        body += f'<path d="M{p[0][0]:.0f} {p[0][1]:.0f} L{p[1][0]:.0f} {p[1][1]:.0f}" stroke="{["#1c5a34", "#2a7a46", "#174a2c"][k]}" stroke-width="7" opacity=".8"/>'
    # the LHC magnet line on the left of the floor (blue cryostat tube, tinted by the green light)
    d += lin('tube', [(0, '#7fe0ff'), (.25, '#2a8fb8'), (.7, '#0d4a6c'), (1, '#052235')])
    TX, TH, TW = .58, .2, .17   # offset (fraction of rx), height and width (fraction of ry)

    def tp(f, dx, dy):
        rx, ry = R * f, R * .9 * f
        return VX - rx * TX + rx * dx, VY + ry * FL - ry * dy
    q = [tp(.035, -TW / 2, TH), tp(4, -TW / 2, TH), tp(4, -TW / 2, 0), tp(.035, -TW / 2, 0)]
    body += '<polygon points="' + ' '.join(f'{a:.0f},{b:.0f}' for a, b in q) + '" fill="#06283c"/>'
    q = [tp(.035, -TW / 2, TH), tp(4, -TW / 2, TH), tp(4, TW / 2, TH * 1.08), tp(.035, TW / 2, TH * 1.08)]
    body += '<polygon points="' + ' '.join(f'{a:.0f},{b:.0f}' for a, b in q) + '" fill="url(#tube)" stroke="#02121c" stroke-width="3"/>'
    for f in fs[3:]:   # magnet joints
        a, b = tp(f, -TW / 2, TH); c, e = tp(f, TW / 2, TH * 1.08); g, h = tp(f, -TW / 2, 0)
        body += f'<path d="M{g:.0f} {h:.0f} L{a:.0f} {b:.0f} L{c:.0f} {e:.0f}" fill="none" stroke="#c9f4ff" stroke-width="{1 + f * 2:.1f}" opacity=".22"/>'
    a, b = tp(.035, 0, TH * 1.04); c, e = tp(4, 0, TH * 1.04)
    body += f'<path d="M{a:.0f} {b:.0f} L{c:.0f} {e:.0f}" stroke="#e6fbff" stroke-width="5" opacity=".45"/>'
    # code-rain streaks (abstract dashes, no glyphs)
    for _ in range(170):
        x = rnd.randint(0, 1920); y = rnd.randint(-100, 1000); L = rnd.randint(30, 180)
        if corner(x, y + L): continue
        o = rnd.uniform(.05, .22) * (0.5 if x < 1000 and y < 470 else 1)
        body += f'<path d="M{x} {y} v{L}" stroke="#4dff8f" stroke-width="{rnd.choice([2, 3, 4])}" stroke-dasharray="6 7" opacity="{o:.2f}"/>'
        body += f'<rect x="{x - 2}" y="{y + L}" width="5" height="7" fill="#d7ffe4" opacity="{o * 2.2:.2f}"/>'
    # ---- frog: long black coat, bending back (bullet-time pose) ----
    PX, PY, S, A = 1300, 880, 3.4, -50
    W = lambda lx, ly: (PX + rot(lx, ly, A, S)[0], PY + rot(lx, ly, A, S)[1])
    hipw = [W(-20, -4), W(20, -4)]
    feetw = [(1280, 1012), (1452, 1014)]
    knees = [(1330, 990), (1480, 880)]
    body += '<ellipse cx="1340" cy="1026" rx="250" ry="22" fill="#000" opacity=".55" filter="url(#blur12)"/>'
    d += lin('coat', [(0, '#22362a'), (.5, '#0a120d'), (1, '#030604')], x2=1, y2=1)
    bs, bh, fs_, fh = W(-36, -46), W(-34, 0), W(44, -46), W(42, 4)
    coat = (f'<path d="M{bs[0]:.0f} {bs[1]:.0f} C{bs[0] - 40:.0f} {bs[1] + 60:.0f} 1010 980 930 1012 L1030 1008 L1060 1034 L1150 1016 L1180 1036 L{bh[0]:.0f} {bh[1]:.0f} '
            f'L{fh[0]:.0f} {fh[1]:.0f} L1500 860 L1458 858 L1490 912 L1410 860 Q{fs_[0] + 90:.0f} {fs_[1] + 60:.0f} {fs_[0]:.0f} {fs_[1]:.0f} Z" '
            f'fill="url(#coat)" stroke="#010302" stroke-width="6" stroke-linejoin="round"/>'
            f'<path d="M{bs[0]:.0f} {bs[1]:.0f} C{bs[0] - 40:.0f} {bs[1] + 60:.0f} 1010 980 930 1012 M{fh[0]:.0f} {fh[1]:.0f} L1500 860" fill="none" stroke="#5dff9a" stroke-width="4" opacity=".6"/>')
    body += coat
    legs = ''
    for (hx, hy), (kx, ky), (fx, fy) in zip(hipw, knees, feetw):
        dd = f'M{hx:.0f} {hy:.0f} Q{kx} {ky} {fx} {fy - 10}'
        legs += f'<path d="{dd}" fill="none" stroke="{INK}" stroke-width="42" stroke-linecap="round"/><path d="{dd}" fill="none" stroke="{GREEN}" stroke-width="29" stroke-linecap="round"/>'
    for fx, fy in feetw:
        legs += f'<ellipse cx="{fx}" cy="{fy}" rx="56" ry="24" fill="{DARKG}" stroke="{INK}" stroke-width="10"/>'
    body += legs
    lapels = ('<path d="M-36 -2 q-5 -22 -1 -36 l13 3 q4 18 6 34 z" fill="url(#coat)" stroke="#010302" stroke-width="3"/>'
              '<path d="M42 0 q5 -22 1 -36 l-13 3 q-3 18 -4 34 z" fill="url(#coat)" stroke="#010302" stroke-width="3"/>'
              '<path d="M-36 -36 l-6 -10 l18 4 z M43 -36 l6 -10 l-18 4 z" fill="#0a120d" stroke="#010302" stroke-width="2.5"/>')
    body += frog(PX, PY, S, rot_=A, look=(4, -4), mouth='o', nofeet=True, front=lapels,
                 armL='M-36 -26 q-30 0 -46 22', armR='M42 -28 q24 -12 30 -40')
    # ---- protons fired from the far end, flying past above the frog ----
    for (x, y, r, gid) in ((1340, 372, 15, 'p3'), (1010, 560, 34, 'p1'), (660, 715, 26, 'p2')):
        pd, pb = proton(x, y, r, x - VX, y - VY, gid, n=6 if r > 20 else 5)
        d += pd; body += pb
    body += spark(1630, 300, 16, '#e9fff2', .7) + spark(860, 540, 14, '#fff6d6', .8) + spark(1700, 640, 12, '#d8ffe6', .6)
    d += rad('vig', 960, 540, 1150, [(0, '#000', 0), (.65, '#000', 0), (1, '#000', .7)])
    body += '<rect width="1920" height="1080" fill="url(#vig)"/>'
    lines = [('BULLETS AT', 118, 'w'), ('99.9999991%', 150, 'y'), ('LIGHT SPEED', 118, 'w')]
    return page('#020c06', svg(d, body), lines, outline='#01140a')


# =========================== B: knife edge = mountain range, one-atom needle ===========================
def make_B():
    rnd = random.Random(17)
    d = SOFT
    d += lin('bBg', [(0, '#1a2233'), (.6, '#10172a'), (1, '#070b16')])
    body = '<rect width="1920" height="1080" fill="url(#bBg)"/>'
    d += rad('bLight', 300, 1000, 900, [(0, '#f6c98a', .35), (.5, '#a26a3a', .08), (1, '#000', 0)])
    body += '<rect width="1920" height="1080" fill="url(#bLight)"/>'
    # kitchen counter (wood) at the bottom-left
    d += lin('wood', [(0, '#6a4128'), (1, '#2a170c')])
    body += '<polygon points="0,860 1100,820 1500,1080 0,1080" fill="url(#wood)"/>'
    for k in range(9):
        y = 870 + k * 26
        body += f'<path d="M0 {y} Q500 {y - 16 - k * 2} {1120 + k * 40} {y - 30 + k * 6}" stroke="#3a2212" stroke-width="3" fill="none" opacity=".5"/>'
    # ---- kitchen knife, edge up, lying diagonally ----
    d += lin('steel', [(0, '#f4f7fb'), (.35, '#b9c3d2'), (.7, '#7d889a'), (1, '#4a5466')], x2=1, y2=1)
    d += lin('bevel', [(0, '#ffffff'), (1, '#c9d2e0')], x2=0, y2=1)
    kn = '<g transform="translate(150 1000) rotate(-28)">'
    kn += '<rect x="-150" y="-40" width="230" height="74" rx="22" fill="#2b1a12" stroke="#0c0604" stroke-width="5"/>'
    kn += ''.join(f'<circle cx="{c}" cy="-3" r="8" fill="#d8dee8" stroke="#0c0604" stroke-width="3"/>' for c in (-90, -30, 30))
    kn += '<rect x="78" y="-46" width="30" height="86" rx="8" fill="#9aa4b4" stroke="#0c0604" stroke-width="5"/>'
    kn += '<path d="M106 34 L760 34 Q860 30 900 -10 Q700 -96 106 -100 Z" fill="url(#steel)" stroke="#0c0604" stroke-width="5"/>'
    kn += '<path d="M110 -100 Q700 -96 900 -10 L860 -14 Q690 -72 110 -74 Z" fill="url(#bevel)" opacity=".85"/>'
    kn += '<path d="M130 20 L760 20" stroke="#fff" stroke-width="4" opacity=".55"/>'
    kn += '<path d="M120 -98 Q700 -94 896 -12" fill="none" stroke="#fff" stroke-width="3"/>'
    kn += '</g>'
    body += '<ellipse cx="540" cy="1010" rx="460" ry="40" fill="#000" opacity=".45" filter="url(#blur12)"/>'
    body += kn
    # zoom spot on the knife edge (local point (520,-97) -> world)
    zx, zy = 150 + 520 * math.cos(math.radians(-28)) + 97 * math.sin(math.radians(-28)), 1000 + 520 * math.sin(math.radians(-28)) - 97 * math.cos(math.radians(-28))
    BX, BY, BR = 1290, 545, 400
    # callout cone (tangent lines from the spot to the bubble)
    dx, dy = BX - zx, BY - zy; D = math.hypot(dx, dy); base = math.atan2(dy, dx); off = math.asin((BR - 38) / D)
    cone = ''
    pts = []
    for sgn in (1, -1):
        a = base + sgn * (math.pi / 2 + off)
        pts.append(((zx - 38 * math.cos(base + sgn * (math.pi / 2 + off)) * -1), 0))
    t1 = base + (math.pi / 2 - off); t2 = base - (math.pi / 2 - off)
    p1 = (zx + 38 * math.cos(t1 + math.pi), zy + 38 * math.sin(t1 + math.pi))
    q1 = (BX + BR * math.cos(t1 + math.pi), BY + BR * math.sin(t1 + math.pi))
    p2 = (zx + 38 * math.cos(t2 + math.pi), zy + 38 * math.sin(t2 + math.pi))
    q2 = (BX + BR * math.cos(t2 + math.pi), BY + BR * math.sin(t2 + math.pi))
    cone += f'<polygon points="{p1[0]:.0f},{p1[1]:.0f} {q1[0]:.0f},{q1[1]:.0f} {q2[0]:.0f},{q2[1]:.0f} {p2[0]:.0f},{p2[1]:.0f}" fill="#F2D27A" opacity=".10"/>'
    cone += f'<path d="M{p1[0]:.0f} {p1[1]:.0f} L{q1[0]:.0f} {q1[1]:.0f} M{p2[0]:.0f} {p2[1]:.0f} L{q2[0]:.0f} {q2[1]:.0f}" stroke="#F2D27A" stroke-width="4" stroke-dasharray="14 10" opacity=".8"/>'
    body += cone
    body += f'<circle cx="{zx:.0f}" cy="{zy:.0f}" r="38" fill="#F2D27A" fill-opacity=".12" stroke="#F2D27A" stroke-width="6"/>'
    # ---- the bubble: electron-microscope view ----
    d += f'<clipPath id="bub"><circle cx="{BX}" cy="{BY}" r="{BR - 6}"/></clipPath>'
    d += rad('semBg', BX + 40, BY - 120, BR * 1.1, [(0, '#2a3550', 1), (.6, '#141b30', 1), (1, '#0a0f1e', 1)])
    body += f'<circle cx="{BX}" cy="{BY}" r="{BR + 34}" fill="#9ad8ff" opacity=".16" filter="url(#blur30)"/>'
    body += f'<circle cx="{BX}" cy="{BY}" r="{BR}" fill="url(#semBg)"/>'
    inn = '<g clip-path="url(#bub)">'
    inn += starfield(rnd, 60, (BX - BR, BY - BR, BX + BR, BY), None, '#cfe4ff', .35)
    # jagged steel ridge (the knife edge up close): far range then near range
    d += lin('rockF', [(0, '#6c7a92'), (1, '#252e44')])
    d += lin('rockN', [(0, '#d6deea'), (.25, '#8c99b0'), (.7, '#3b465e'), (1, '#161c2c')])

    def ridge(y0, amp, step, seed, jag=1.0):
        r2 = random.Random(seed); x = BX - BR - 40; pts = [(x, y0)]
        while x < BX + BR + 40:
            x += r2.randint(step // 2, step); up = r2.random() < .5
            pts.append((x, y0 - r2.uniform(.2, 1) * amp * (1 if up else .35) * jag))
        return pts
    far = ridge(700, 150, 70, 3)
    inn += '<polygon points="' + ' '.join(f'{x:.0f},{y:.0f}' for x, y in far) + f' {BX + BR + 40},{BY + BR + 40} {BX - BR - 40},{BY + BR + 40}" fill="url(#rockF)" opacity=".85"/>'
    # near ridge, hand-placed so the tallest peak sits under the needle
    near = [(880, 840), (935, 760), (968, 790), (1010, 708), (1050, 742), (1100, 690), (1135, 735), (1175, 640), (1205, 690), (1240, 600),
            (1262, 560), (1290, 532), (1318, 572), (1345, 610), (1380, 590), (1420, 668), (1465, 640), (1510, 720), (1560, 690), (1610, 770), (1660, 745), (1720, 820)]
    poly = ' '.join(f'{x},{y}' for x, y in near)
    inn += f'<polygon points="{poly} 1720,1000 880,1000" fill="url(#rockN)" stroke="#0a0f1e" stroke-width="4" stroke-linejoin="round"/>'
    # lit faces: right side of each peak catches the atom's glow, chips and grinding scratches
    for i in range(1, len(near) - 1):
        (x0, y0), (x1, y1), (x2, y2) = near[i - 1], near[i], near[i + 1]
        if y1 < y0 and y1 < y2:
            inn += f'<polygon points="{x1},{y1} {x2},{y2} {x1 + (x2 - x1) * .3:.0f},{y2 + 80} {x1 - 6},{y1 + 70}" fill="#eef4ff" opacity=".22"/>'
            inn += f'<path d="M{x0} {y0} L{x1} {y1} L{x2} {y2}" fill="none" stroke="#e6f3ff" stroke-width="4" opacity=".75"/>'
    for _ in range(46):
        x = rnd.randint(890, 1700); y = rnd.randint(720, 960)
        inn += f'<path d="M{x} {y} l{rnd.randint(30, 90)} {rnd.randint(-8, 8)}" stroke="#cdd8ea" stroke-width="2" opacity="{rnd.uniform(.12, .35):.2f}"/>'
    for _ in range(14):   # chipped flakes
        x = rnd.randint(900, 1680); y = rnd.randint(760, 940); s = rnd.randint(8, 18)
        inn += f'<polygon points="{x},{y} {x + s},{y + s * .4:.0f} {x + s * .4:.0f},{y + s}" fill="#0f1424" opacity=".55"/>'
    # ---- the single-atom needle (tungsten), coming down from above ----
    TX, TY = 1290, 410    # apex atom centre
    d += lin('tung', [(0, '#3a4256'), (.35, '#9aa6bc'), (.55, '#d8e0ee'), (.8, '#5b6680'), (1, '#262c3c')], x2=1, y2=0)
    inn += f'<polygon points="{TX - 150},{BY - BR - 20} {TX + 150},{BY - BR - 20} {TX + 34},{TY - 92} {TX - 34},{TY - 92}" fill="url(#tung)" stroke="#0a0f1e" stroke-width="4"/>'
    inn += f'<path d="M{TX - 20} {BY - BR} L{TX - 6} {TY - 96}" stroke="#fff" stroke-width="5" opacity=".5"/>'
    # atoms at the apex: rows 4,3,2,1
    rows = [(4, TY - 82), (3, TY - 56), (2, TY - 30)]
    for n, y in rows:
        for k in range(n):
            x = TX + (k - (n - 1) / 2) * 25
            inn += f'<circle cx="{x:.0f}" cy="{y}" r="13" fill="#8f9bb4" stroke="#0a0f1e" stroke-width="3"/><circle cx="{x - 4:.0f}" cy="{y - 4}" r="4.5" fill="#eef3fb" opacity=".8"/>'
    inn += '</g>'
    body += inn
    # glowing apex atom with electron cloud (drawn above the clip so the glow can spill)
    d += rad('atomG', TX, TY, 150, [(0, '#ffffff', 1), (.1, '#fff1c4', .95), (.25, '#F2D27A', .55), (.55, '#62c9ff', .18), (1, '#62c9ff', 0)])
    body += f'<circle cx="{TX}" cy="{TY}" r="150" fill="url(#atomG)"/>'
    for a in (0, 60, 120):
        body += f'<ellipse cx="{TX}" cy="{TY}" rx="58" ry="18" transform="rotate({a} {TX} {TY})" fill="none" stroke="#bfe9ff" stroke-width="3" opacity=".75"/>'
    body += f'<circle cx="{TX}" cy="{TY}" r="17" fill="#fffaf0" stroke="#F2D27A" stroke-width="3"/>'
    # tunnelling sparks in the gap above the peak
    for k in range(5):
        y = TY + 30 + k * 18
        body += f'<path d="M{TX - 6 + (k % 2) * 12} {y} l{-10 + (k % 2) * 20} 9" stroke="#bfe9ff" stroke-width="3" opacity="{.85 - k * .12:.2f}" stroke-linecap="round"/>'
    # ---- frog: mountaineer on the steel ridge, looking up at the atom ----
    helmet = ('<path d="M-22 -80 q26 -26 54 0 z" fill="#f2b632" stroke-width="3"/><rect x="-26" y="-82" width="62" height="7" rx="3" fill="#e09a1c" stroke-width="2.5"/>'
              '<circle cx="6" cy="-92" r="5" fill="#fff6c8" stroke-width="2"/>')
    rope = '<path d="M-34 -30 q30 18 76 6" fill="none" stroke="#d2462f" stroke-width="5"/><path d="M-34 -30 q30 18 76 6" fill="none" stroke="#ff8a6a" stroke-width="1.6"/>'
    axe = ('<path d="M56 -40 L70 -110" stroke="#5a3a1c" stroke-width="5"/><path d="M58 -112 q12 -8 28 4 l-16 4 z" fill="#c9d2e0" stroke-width="3"/>')
    body += frog(1085, 724, 2.55, look=(5, -5), mouth='o', front=rope + axe, helmet=helmet,
                 armL='M-34 -22 q-18 -6 -26 -26', armR='M38 -24 q12 -6 18 -16', feet=((-24, 4, -20), (22, 6, 14)))
    # bubble rim (brass loupe ring)
    d += lin('ring', [(0, '#fff0b8'), (.35, '#F2D27A'), (.7, '#a87a2c'), (1, '#5a3c10')], x2=1, y2=1)
    body += f'<circle cx="{BX}" cy="{BY}" r="{BR}" fill="none" stroke="url(#ring)" stroke-width="18"/>'
    body += f'<circle cx="{BX}" cy="{BY}" r="{BR - 9}" fill="none" stroke="#2a1a05" stroke-width="3"/>'
    body += f'<path d="M{BX - 300} {BY - 230} A{BR - 40} {BR - 40} 0 0 1 {BX - 90} {BY - BR + 52}" fill="none" stroke="#fff" stroke-width="10" stroke-linecap="round" opacity=".35"/>'
    body += spark(1600, 260, 22, '#e9f4ff') + spark(1720, 560, 16, '#fff6d6', .75) + spark(990, 300, 16, '#e9f4ff', .7) + spark(1460, 380, 14)
    lines = [('SHARPNESS', 132, 'w'), ('IS AN', 100, 'w'), ('ILLUSION', 172, 'y')]
    return page('#10172a', svg(d, body), lines, outline='#070b16')


# =========================== C: 2001 match cut, flint knife -> LHC ring ===========================
def make_C():
    rnd = random.Random(29)
    d = SOFT
    d += ('<linearGradient id="cSky" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#f0a057"/><stop offset=".3" stop-color="#c8665a"/>'
          '<stop offset=".52" stop-color="#4a2a5e"/><stop offset=".72" stop-color="#120c2a"/><stop offset="1" stop-color="#04040e"/></linearGradient>')
    body = '<rect width="1920" height="1080" fill="url(#cSky)"/>'
    d += lin('cTop', [(0, '#000', ), (1, '#000')])
    d += '<linearGradient id="cDark" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#05030c" stop-opacity=".55"/><stop offset=".5" stop-color="#05030c" stop-opacity="0"/></linearGradient>'
    body += '<rect width="1920" height="1080" fill="url(#cDark)"/>'
    body += starfield(rnd, 260, (900, 0, 1920, 1080), lambda x, y: corner(x, y) or rnd.random() < (1500 - x) / 900, '#eef0ff')
    # sun rising behind the ridge at the left
    d += rad('cSun', 300, 900, 760, [(0, '#fff2c4', 1), (.06, '#ffd88a', .9), (.25, '#f39a4a', .35), (1, '#f39a4a', 0)])
    body += '<rect width="1920" height="1080" fill="url(#cSun)"/>'
    for k in range(7):   # god rays (only into the warm half of the sky)
        a = math.radians(-88 + k * 10); Lr = 1000
        body += f'<polygon points="300,900 {300 + Lr * math.cos(a - .025):.0f},{900 + Lr * math.sin(a - .025):.0f} {300 + Lr * math.cos(a + .025):.0f},{900 + Lr * math.sin(a + .025):.0f}" fill="#ffe0a8" opacity=".07"/>'
    # savanna ridge with boulders, fading out to the right
    d += lin('ridge', [(0, '#2a140c'), (1, '#0c0605')])
    body += ('<path d="M0 860 Q120 830 240 845 Q330 815 420 838 Q560 800 700 850 Q820 880 960 900 Q1100 940 1240 1080 L0 1080 Z" fill="url(#ridge)"/>')
    body += '<path d="M0 860 Q120 830 240 845 Q330 815 420 838 Q560 800 700 850 Q820 880 960 900" fill="none" stroke="#ffb066" stroke-width="4" opacity=".7"/>'
    for (x, y, w, h) in ((150, 930, 170, 90), (560, 940, 220, 110), (820, 990, 160, 70)):
        body += f'<path d="M{x - w / 2} {y + h / 2} Q{x - w / 2} {y - h / 2} {x} {y - h / 2} Q{x + w / 2} {y - h / 2 + 10} {x + w / 2} {y + h / 2} Z" fill="#1d0e08" stroke="#0a0403" stroke-width="4"/>'
        body += f'<path d="M{x - w / 3} {y - h / 2 + 8} Q{x} {y - h / 2 - 2} {x + w / 4} {y - h / 2 + 6}" fill="none" stroke="#ff9d55" stroke-width="4" opacity=".7"/>'
    # dry grass tufts
    for _ in range(40):
        x = rnd.randint(0, 900); y = rnd.randint(850, 1060)
        body += f'<path d="M{x} {y} l{rnd.randint(-8, 8)} {-rnd.randint(14, 34)} M{x} {y} l{rnd.randint(4, 14)} {-rnd.randint(10, 26)}" stroke="#4a2a14" stroke-width="2.4" opacity=".8"/>'
    # ---- LHC ring floating in space like the wheel station ----
    RX, RY, Ra, Rb, Rt = 1470, 470, 380, 135, -13
    d += rad('ringGlow', RX, RY, 520, [(0, '#5ac8ff', .0), (.55, '#5ac8ff', .16), (.75, '#a07bff', .08), (1, '#000', 0)])
    body += f'<ellipse cx="{RX}" cy="{RY}" rx="560" ry="300" transform="rotate({Rt} {RX} {RY})" fill="url(#ringGlow)"/>'
    d += lin('tubeC', [(0, '#bfeaff'), (.3, '#3a8fd0'), (.75, '#123d6e'), (1, '#071a33')])
    ring = f'<g transform="translate({RX} {RY}) rotate({Rt})">'
    # back half of the torus (behind), then front half
    ring += f'<path d="M{-Ra} 0 A{Ra} {Rb} 0 0 1 {Ra} 0" fill="none" stroke="#06142a" stroke-width="58"/>'
    ring += f'<path d="M{-Ra} 0 A{Ra} {Rb} 0 0 1 {Ra} 0" fill="none" stroke="#1d5a94" stroke-width="44"/>'
    ring += f'<path d="M{-Ra} -6 A{Ra} {Rb - 6} 0 0 1 {Ra} -6" fill="none" stroke="#8fd4ff" stroke-width="6" opacity=".55"/>'
    # proton beam inside: bright thin loop
    ring += f'<ellipse rx="{Ra}" ry="{Rb}" fill="none" stroke="#fff3c8" stroke-width="5" opacity=".9" filter="url(#soft)"/>'
    ring += f'<ellipse rx="{Ra}" ry="{Rb}" fill="none" stroke="#F2D27A" stroke-width="16" opacity=".35" filter="url(#blur6)"/>'
    ring += f'<path d="M{-Ra} 0 A{Ra} {Rb} 0 0 0 {Ra} 0" fill="none" stroke="#06142a" stroke-width="62"/>'
    ring += f'<path d="M{-Ra} 0 A{Ra} {Rb} 0 0 0 {Ra} 0" fill="none" stroke="url(#tubeC)" stroke-width="48"/>'
    ring += f'<path d="M{-Ra + 8} -10 A{Ra - 8} {Rb - 8} 0 0 0 {Ra - 8} -10" fill="none" stroke="#e6f7ff" stroke-width="5" opacity=".6"/>'
    for k in range(1, 24):   # magnet joints on the front half
        t = math.pi * k / 24; x, y = Ra * math.cos(t), Rb * math.sin(t)
        nx, ny = math.cos(t) / Ra, math.sin(t) / Rb; L = math.hypot(nx, ny); nx, ny = nx / L * 24, ny / L * 24
        ring += f'<path d="M{x - nx:.0f} {y - ny:.0f} L{x + nx:.0f} {y + ny:.0f}" stroke="#d8f1ff" stroke-width="3.5" opacity=".7"/>'
    # four experiment halls as bright pods on the ring
    for t in (.25, .95, 2.2, 2.9):
        x, y = Ra * math.cos(t), Rb * math.sin(t)
        ring += (f'<g transform="translate({x:.0f} {y:.0f})"><circle r="52" fill="#F2D27A" opacity=".3" filter="url(#blur6)"/>'
                 f'<circle r="32" fill="#2a3550" stroke="#0a0f1e" stroke-width="5"/>'
                 + ''.join(f'<path d="M0 0 L{32 * math.cos(k * math.pi / 4):.0f} {32 * math.sin(k * math.pi / 4):.0f}" stroke="#8fa6c8" stroke-width="3"/>' for k in range(8))
                 + '<circle r="32" fill="none" stroke="#F2D27A" stroke-width="5"/><circle r="12" fill="#fff1c4"/></g>')
    # one proton racing round the front with a streak
    t0 = 1.5; px, py = Ra * math.cos(t0), Rb * math.sin(t0)
    ring += f'<path d="M{Ra * math.cos(t0 + .55):.0f} {Rb * math.sin(t0 + .55):.0f} A{Ra} {Rb} 0 0 0 {px:.0f} {py:.0f}" fill="none" stroke="#fff6d6" stroke-width="10" stroke-linecap="round" opacity=".85"/>'
    ring += f'<circle cx="{px:.0f}" cy="{py:.0f}" r="44" fill="#fff1c4" opacity=".45" filter="url(#blur12)"/><circle cx="{px:.0f}" cy="{py:.0f}" r="13" fill="#fff"/>'
    ring += '</g>'
    body += ring
    body += spark(RX + 260, RY - 200, 24, '#e9f4ff') + spark(RX - 330, RY - 150, 16, '#e9f4ff', .7) + spark(1800, 760, 14, '#e9f4ff', .6)
    # the match-cut arc: dotted trajectory from the frog's throw through the knife toward the ring
    body += '<path d="M470 760 Q700 380 1000 470 T1250 430" fill="none" stroke="#fff1d0" stroke-width="5" stroke-dasharray="3 16" stroke-linecap="round" opacity=".7"/>'
    # ---- flint knife, tumbling ----
    d += lin('flint', [(0, '#6a6058'), (.4, '#3a322e'), (1, '#141010')], x2=1, y2=1)
    FX, FY, Fa = 900, 590, -38
    fk = f'<g transform="translate({FX} {FY}) rotate({Fa})">'
    fk += '<ellipse cx="0" cy="0" rx="250" ry="90" fill="#ffb066" opacity=".22" filter="url(#blur30)"/>'
    # chipped flint blade: scalloped edges made of flake scars, light facets toward the sun (left/top)
    top = [(-220, -4), (-170, -50), (-96, -72), (-20, -86), (60, -78), (140, -56), (200, -30), (256, 0)]
    bot = [(256, 0), (190, 32), (110, 60), (20, 74), (-70, 66), (-150, 50), (-200, 26)]
    pts = top + bot
    fk += '<path d="M' + ' L'.join(f'{x} {y}' for x, y in pts) + ' Z" fill="url(#flint)" stroke="#050407" stroke-width="8" stroke-linejoin="round"/>'
    ridge = [(-180, 0), (-110, -10), (-40, 4), (40, -8), (110, 2), (180, -4), (230, 0)]
    lit = ['#9a8f84', '#7d746c', '#b0a596', '#857a70', '#a39787', '#8a8076', '#968b7e']
    for i in range(len(top) - 1):   # upper flake scars (sunlit), each a scalloped shell
        (x0, y0), (x1, y1) = top[i], top[i + 1]; rx_, ry_ = ridge[min(i, len(ridge) - 1)]
        fk += f'<path d="M{x0} {y0} Q{(x0 + x1) / 2:.0f} {(y0 + y1) / 2 + 22:.0f} {x1} {y1} L{rx_ + 30} {ry_} Z" fill="{lit[i]}" stroke="#2a2420" stroke-width="2.5"/>'
        for j in (1, 2):
            fk += f'<path d="M{x0 + (rx_ - x0) * .25 * j:.0f} {y0 + (ry_ - y0) * .25 * j:.0f} Q{(x0 + x1) / 2:.0f} {(y0 + y1) / 2 + 22 + 14 * j:.0f} {x1 + (rx_ - x1) * .25 * j:.0f} {y1 + (ry_ - y1) * .25 * j:.0f}" fill="none" stroke="#e8dccb" stroke-width="2" opacity=".45"/>'
    for i in range(len(bot) - 1):   # lower flake scars (shadow side)
        (x0, y0), (x1, y1) = bot[i], bot[i + 1]; rx_, ry_ = ridge[max(0, len(ridge) - 1 - i)]
        fk += f'<path d="M{x0} {y0} Q{(x0 + x1) / 2:.0f} {(y0 + y1) / 2 - 18:.0f} {x1} {y1} L{rx_ - 20} {ry_} Z" fill="{["#2c2622", "#3a332e", "#241f1c"][i % 3]}" stroke="#120e0c" stroke-width="2.5"/>'
    fk += '<path d="M' + ' L'.join(f'{x} {y}' for x, y in top) + '" fill="none" stroke="#ffcf8a" stroke-width="6" stroke-linejoin="round" opacity=".95"/>'
    fk += '<path d="M' + ' L'.join(f'{x} {y}' for x, y in bot[:7]) + '" fill="none" stroke="#7fc8ff" stroke-width="3" opacity=".55"/>'
    fk += '<path d="M' + ' L'.join(f'{x} {y}' for x, y in ridge) + '" fill="none" stroke="#e8e0ec" stroke-width="3" opacity=".55"/>'
    fk += '</g>'
    # spin arcs around the knife
    for k, (r_, a0, a1) in enumerate(((300, 200, 250), (330, 20, 70), (270, 110, 150))):
        a0r, a1r = math.radians(a0), math.radians(a1)
        body += (f'<path d="M{FX + r_ * math.cos(a0r):.0f} {FY + r_ * .55 * math.sin(a0r):.0f} A{r_} {r_ * .55:.0f} 0 0 1 {FX + r_ * math.cos(a1r):.0f} {FY + r_ * .55 * math.sin(a1r):.0f}" '
                 f'fill="none" stroke="#fff1d0" stroke-width="{7 - k * 1.5}" stroke-linecap="round" opacity=".65"/>')
    body += fk
    body += spark(FX + 170, FY - 150, 24, '#fff1d0') + spark(FX - 230, FY + 40, 14, '#fff1d0', .7)
    # ---- frog as a cave-dweller in a fur pelt, arm up after the throw ----
    pelt = ('<path d="M22 -64 Q36 -60 42 -48 L-24 8 Q-34 6 -36 -4 Z" fill="#e2a04a" stroke-width="3.5"/>'
            '<path d="M-36 -4 l-6 10 l10 -2 l2 10 l8 -8 l6 6 l2 -10" fill="#e2a04a" stroke-width="3"/>'
            + ''.join(f'<path d="M{x - 4} {y} q2 -5 6 -3 q4 3 0 6 q-4 2 -6 -3z" fill="#4a2810" stroke="none"/>' for x, y in ((24, -52), (10, -38), (-4, -26), (-18, -12), (-26, 0))))
    body += '<ellipse cx="400" cy="900" rx="130" ry="18" fill="#000" opacity=".4" filter="url(#blur12)"/>'
    body += frog(400, 892, 3.2, look=(5, -6), mouth='o', front=pelt,
                 armR='M38 -26 q14 -24 12 -50', armL='M-34 -22 q-16 4 -20 22', feet=((-24, 4, -6), (24, 4, 8)))
    # warm rim light along the frog's sun side (left) and on the ground
    body += '<path d="M300 870 Q290 700 380 670" fill="none" stroke="#ffd59a" stroke-width="5" opacity=".55"/>'
    d += rad('cVig', 960, 540, 1150, [(0, '#000', 0), (.7, '#000', 0), (1, '#000', .55)])
    body += '<rect width="1920" height="1080" fill="url(#cVig)"/>'
    lines = [('FROM', 104, 'w'), ('FLINT', 210, 'y'), ('TO PROTONS', 128, 'w')]
    return page('#2a1a3a', svg(d, body), lines, outline='#1a0a10')


if __name__ == '__main__':
    for n, f in (('A', make_A), ('B', make_B), ('C', make_C)):
        open(os.path.join(HERE, f'{n}.html'), 'w').write(f())
        print('wrote', n)
