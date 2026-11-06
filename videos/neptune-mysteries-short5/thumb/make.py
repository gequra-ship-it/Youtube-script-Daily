# Shorts thumbnail A for neptune-mysteries-short5 (guideline 16-9; brief tools/briefs/thumb_art.md). Run: python3 videos/neptune-mysteries-short5/thumb/make.py
# A  A MOON / RIPPED / APART   intuitive: Triton has crossed the red dashed danger line (Roche limit) and cracks into glowing pieces; its debris
#                              spreads along the old orbit into a new ring around Neptune; the frog in a space helmet clings to the biggest chunk
#                              (S12-S15: "Triton will be ripped apart ... fragmenting into countless icy boulders ... forming a bright ring system")
import os, math, random
HERE = os.path.dirname(os.path.abspath(__file__))
LONG = os.path.join(HERE, '../../neptune-mysteries/thumb/make.py')   # shared helpers (frog, neptune, diamond) from the long-form thumbs
_src = open(LONG).read(); _g = {'__file__': LONG}; exec(_src[:_src.index('def thumb_A')], _g); globals().update({k: v for k, v in _g.items() if not k.startswith('__') and k != 'HERE'})

CX, CY = 1160, 655
ROT = math.radians(-12)


def ell(rx, ry, t):
    x, y = rx * math.cos(t), ry * math.sin(t)
    return CX + x * math.cos(ROT) - y * math.sin(ROT), CY + x * math.sin(ROT) + y * math.cos(ROT)


def rock(x, y, s, col, rot):
    pts = []
    for k in range(7):
        a = 2 * math.pi * k / 7; r = s * random.uniform(.7, 1.1)
        pts.append(f'{x + r * math.cos(a):.1f} {y + r * .8 * math.sin(a):.1f}')
    return f'<path d="M{" L".join(pts)}Z" fill="{col}" stroke="#2a1a24" stroke-width="{max(1.2, s * .18):.1f}" stroke-linejoin="round" transform="rotate({rot:.0f} {x:.0f} {y:.0f})"/>'


def ring_part(front, RX, RY, TT):
    o = ''
    # soft glowing band (the ring that is forming)
    t0, t1 = (0, math.pi) if front else (math.pi, 2 * math.pi)
    pts = [ell(RX, RY, t0 + (t1 - t0) * i / 80) for i in range(81)]
    path = 'M' + ' L'.join(f'{x:.0f} {y:.0f}' for x, y in pts)
    o += f'<path d="{path}" fill="none" stroke="#ffe2c0" stroke-width="44" opacity=".2" filter="url(#b6)"/>'
    o += f'<path d="{path}" fill="none" stroke="#fff1de" stroke-width="6" opacity=".5"/>'
    random.seed(5 if front else 6)
    for _ in range(1100):
        side = 1 if random.random() < .62 else -1
        dt = side * random.expovariate(1 / .9)   # radians away from Triton along the orbit
        t = (TT + dt) % (2 * math.pi)
        if (math.sin(t) >= 0) != front:
            continue
        near = math.exp(-abs(dt) / .8)
        rr = 1 + random.gauss(0, .035 + .03 * near)
        x, y = ell(RX * rr, RY * rr, t)
        s = random.uniform(1.4, 4.5) + 10 * near * random.random()
        col = random.choice(['#e8d2c6', '#c9a8a0', '#f6ead8', '#a88078'])
        if s > 5:
            o += rock(x, y, s, col, random.uniform(0, 360))
        else:
            o += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{s * .6:.1f}" fill="{col}" opacity="{random.uniform(.5, 1):.2f}"/>'
    return o


def make():
    random.seed(55)
    RX, RY = 540, 150
    TT = math.radians(-22) % (2 * math.pi)
    TX, TY = ell(RX, RY, TT)
    d = FILTERS
    nd, nb = neptune(CX, CY, 250, 'np', spot=True, light=(-.4, -.5))
    d += nd
    d += lin('bg', [(0, '#040516'), (1, '#0b0f2c')])
    d += rad('tri', TX - 30, TY - 40, 140, [(0, '#fbeee4', 1), (.5, '#d8b1a6', 1), (1, '#8a5f5a', 1)])
    d += rad('hot', TX, TY, 230, [(0, '#ffd2a0', .55), (1, '#ff8a5a', 0)])
    b = '<rect width="1920" height="1080" fill="url(#bg)"/>' + starfield(220, seed=9, op=.7)
    # Roche limit: red dashed danger line, just outside Neptune, Triton is crossing it
    LX, LY = RX + 40, RY + 14
    lim = [ell(LX, LY, 2 * math.pi * i / 120) for i in range(121)]
    lpath = 'M' + ' L'.join(f'{x:.0f} {y:.0f}' for x, y in lim)
    b += f'<path d="{lpath}" fill="none" stroke="#ff4a3a" stroke-width="10" opacity=".25" filter="url(#b6)"/>'
    b += f'<path d="{lpath}" fill="none" stroke="#ff6a4a" stroke-width="5" stroke-dasharray="26 18" opacity=".85"/>'
    b += ring_part(False, RX, RY, TT)
    b += nb
    # the front of the Roche line must pass in front of Neptune
    flim = [ell(LX, LY, math.pi * i / 60) for i in range(61)]
    b += '<path d="M' + ' L'.join(f'{x:.0f} {y:.0f}' for x, y in flim) + '" fill="none" stroke="#ff6a4a" stroke-width="5" stroke-dasharray="26 18" opacity=".85"/>'
    b += ring_part(True, RX, RY, TT)
    # Triton breaking apart: wedges pushed outward with hot glowing cracks
    b += f'<circle cx="{TX:.0f}" cy="{TY:.0f}" r="230" fill="url(#hot)"/>'
    TR = 118
    b += f'<circle cx="{TX:.0f}" cy="{TY:.0f}" r="{TR + 10}" fill="#ffb060" filter="url(#b12)"/>'
    b += f'<circle cx="{TX:.0f}" cy="{TY:.0f}" r="{TR - 20}" fill="#fff0c0"/>'
    random.seed(7)
    cuts = [0, 62, 130, 200, 255, 310, 360]
    for i in range(len(cuts) - 1):
        a0, a1 = math.radians(cuts[i]), math.radians(cuts[i + 1])
        am = (a0 + a1) / 2; push = 16 + 10 * (i % 3)
        ox, oy = TX + push * math.cos(am), TY + push * math.sin(am)
        # jagged inner edge
        p = f'M{ox:.1f} {oy:.1f}'
        for k in range(1, 4):
            r = TR * k / 4; a = a0 + random.uniform(-.08, .08)
            p += f' L{ox + r * math.cos(a):.1f} {oy + r * math.sin(a):.1f}'
        p += f' L{ox + TR * math.cos(a0):.1f} {oy + TR * math.sin(a0):.1f} A{TR} {TR} 0 0 1 {ox + TR * math.cos(a1):.1f} {oy + TR * math.sin(a1):.1f}Z'
        b += f'<path d="{p}" fill="url(#tri)" stroke="#2a1a24" stroke-width="5" stroke-linejoin="round"/>'
        for _ in range(5):  # cantaloupe dimples
            rr = random.uniform(.35, .85) * TR; aa = random.uniform(a0 + .1, a1 - .1)
            b += f'<circle cx="{ox + rr * math.cos(aa):.0f}" cy="{oy + rr * math.sin(aa):.0f}" r="{random.uniform(5, 10):.0f}" fill="none" stroke="#8a5f5a" stroke-width="2" opacity=".45"/>'
    b += f'<circle cx="{TX:.0f}" cy="{TY:.0f}" r="34" fill="#ffe6b0" opacity=".85" filter="url(#b12)"/>'
    for k in range(10):  # flying shards
        a = random.uniform(0, 2 * math.pi); r = random.uniform(150, 230)
        b += rock(TX + r * math.cos(a), TY + r * .8 * math.sin(a), random.uniform(7, 14), '#e8d2c6', random.uniform(0, 360))
    # frog in a space helmet clinging to the top-left chunk
    b += frog(TX - 40, TY - 108, 2.15, la='q-28 -24 -36 -54', ra='q28 -24 36 -54', mouth='o', look=(-4, 2), helmet=True, tilt=-14)
    for x, y, s in ((1000, 150, 18), (1480, 120, 22), (1820, 240, 14), (700, 960, 16)):
        b += spark(x, y, s)
    return page('#040516', svg(d, b), [('A MOON', 150, 'w'), ('RIPPED', 196, 'w'), ('APART', 226, 'y')], outline='#040516')


open(os.path.join(HERE, 'A.html'), 'w').write(make())
print('wrote A')
