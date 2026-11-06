# Shorts thumbnail A for neptune-mysteries-short5 (guideline 16-9: vertical 1080x1920, centred text; brief tools/briefs/thumb_art.md).
# Run: python3 videos/neptune-mysteries-short5/thumb/make.py
# A  A MOON / RIPPED / APART   intuitive: top: Triton has crossed the red dashed danger line (Roche limit) in front of Neptune and cracks into glowing
#                              pieces, its debris spreading along the old orbit into a new ring; text in the middle; foreground below: the frog in a
#                              space helmet clings to a big chunk flung toward the camera (S12-S15: "Triton will be ripped apart ... fragmenting into
#                              countless icy boulders ... forming a bright ring system")
import os, sys, math, random
HERE = os.path.dirname(os.path.abspath(__file__))
LONG = os.path.join(HERE, '../../neptune-mysteries/thumb/make.py')   # shared helpers (frog, neptune, diamond, starfield) from the long-form thumbs
_src = open(LONG).read(); _g = {'__file__': LONG}; exec(_src[:_src.index('def thumb_A')], _g); globals().update({k: v for k, v in _g.items() if not k.startswith('__') and k != 'HERE'})
from thumb_lib import vpage, vsvg, blobs

CX, CY = 560, 400
ROT = math.radians(10)


def ell(rx, ry, t):
    x, y = rx * math.cos(t), ry * math.sin(t)
    return CX + x * math.cos(ROT) - y * math.sin(ROT), CY + x * math.sin(ROT) + y * math.cos(ROT)


def rock(x, y, s, col, rot, n=7, sw=None):
    pts = []
    for k in range(n):
        a = 2 * math.pi * k / n; r = s * random.uniform(.7, 1.1)
        pts.append(f'{x + r * math.cos(a):.1f} {y + r * .8 * math.sin(a):.1f}')
    return f'<path d="M{" L".join(pts)}Z" fill="{col}" stroke="#2a1a24" stroke-width="{sw or max(1.2, s * .18):.1f}" stroke-linejoin="round" transform="rotate({rot:.0f} {x:.0f} {y:.0f})"/>'


def ring_part(front, RX, RY, TT):
    o = ''
    t0, t1 = (0, math.pi) if front else (math.pi, 2 * math.pi)
    pts = [ell(RX, RY, t0 + (t1 - t0) * i / 80) for i in range(81)]
    path = 'M' + ' L'.join(f'{x:.0f} {y:.0f}' for x, y in pts)
    o += f'<path d="{path}" fill="none" stroke="#ffe2c0" stroke-width="36" opacity=".2" filter="url(#b6)"/>'
    o += f'<path d="{path}" fill="none" stroke="#fff1de" stroke-width="5" opacity=".5"/>'
    random.seed(5 if front else 6)
    for _ in range(1000):
        side = 1 if random.random() < .55 else -1
        dt = side * random.expovariate(1 / .9)   # radians away from Triton along the orbit
        t = (TT + dt) % (2 * math.pi)
        if (math.sin(t) >= 0) != front:
            continue
        near = math.exp(-abs(dt) / .8)
        rr = 1 + random.gauss(0, .035 + .03 * near)
        x, y = ell(RX * rr, RY * rr, t)
        s = random.uniform(1.4, 4) + 8 * near * random.random()
        col = random.choice(['#e8d2c6', '#c9a8a0', '#f6ead8', '#a88078'])
        if s > 5:
            o += rock(x, y, s, col, random.uniform(0, 360))
        else:
            o += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{s * .6:.1f}" fill="{col}" opacity="{random.uniform(.5, 1):.2f}"/>'
    return o


def cracked(TX, TY, TR, seed, cuts, push0):
    random.seed(seed)
    o = f'<circle cx="{TX:.0f}" cy="{TY:.0f}" r="{TR + 10}" fill="#ffb060" filter="url(#b12)"/><circle cx="{TX:.0f}" cy="{TY:.0f}" r="{TR - 20}" fill="#fff0c0"/>'
    for i in range(len(cuts) - 1):
        a0, a1 = math.radians(cuts[i]), math.radians(cuts[i + 1])
        am = (a0 + a1) / 2; push = push0 + push0 * .6 * (i % 3)
        ox, oy = TX + push * math.cos(am), TY + push * math.sin(am)
        p = f'M{ox:.1f} {oy:.1f}'
        for k in range(1, 4):
            r = TR * k / 4; a = a0 + random.uniform(-.08, .08)
            p += f' L{ox + r * math.cos(a):.1f} {oy + r * math.sin(a):.1f}'
        p += f' L{ox + TR * math.cos(a0):.1f} {oy + TR * math.sin(a0):.1f} A{TR} {TR} 0 0 1 {ox + TR * math.cos(a1):.1f} {oy + TR * math.sin(a1):.1f}Z'
        o += f'<path d="{p}" fill="url(#tri)" stroke="#2a1a24" stroke-width="{max(3, TR * .045):.1f}" stroke-linejoin="round"/>'
        for _ in range(5):  # cantaloupe dimples
            rr = random.uniform(.35, .85) * TR; aa = random.uniform(a0 + .1, a1 - .1)
            o += f'<circle cx="{ox + rr * math.cos(aa):.0f}" cy="{oy + rr * math.sin(aa):.0f}" r="{random.uniform(.05, .09) * TR:.0f}" fill="none" stroke="#8a5f5a" stroke-width="2" opacity=".45"/>'
    return o


def make():
    random.seed(55)
    RX, RY = 410, 120
    TT = math.radians(118)
    TX, TY = ell(RX, RY, TT)
    d = FILTERS
    nd, nb = neptune(CX, CY, 200, 'np', spot=True, light=(-.4, -.5))
    d += nd
    d += lin('bg', [(0, '#040516'), (.6, '#0b0f2c'), (1, '#1a0f24')])
    d += '<radialGradient id="tri" cx=".35" cy=".3" r=".9"><stop offset="0" stop-color="#fbeee4"/><stop offset=".5" stop-color="#d8b1a6"/><stop offset="1" stop-color="#8a5f5a"/></radialGradient>'
    d += rad('hot', TX, TY, 220, [(0, '#ffd2a0', .55), (1, '#ff8a5a', 0)])
    d += rad('hot2', 560, 1700, 420, [(0, '#ffb070', .35), (1, '#ff8a5a', 0)])
    b = '<rect width="1080" height="1920" fill="url(#bg)"/>' + starfield(300, x1=1080, y1=1920, seed=9, op=.7)
    # Roche limit: red dashed danger line just outside the orbit, Triton is crossing it
    LX, LY = RX + 34, RY + 12
    lpath = 'M' + ' L'.join(f'{x:.0f} {y:.0f}' for x, y in [ell(LX, LY, 2 * math.pi * i / 120) for i in range(121)])
    b += f'<path d="{lpath}" fill="none" stroke="#ff4a3a" stroke-width="10" opacity=".25" filter="url(#b6)"/>'
    b += f'<path d="{lpath}" fill="none" stroke="#ff6a4a" stroke-width="5" stroke-dasharray="24 16" opacity=".85"/>'
    b += ring_part(False, RX, RY, TT)
    b += nb
    b += '<path d="M' + ' L'.join(f'{x:.0f} {y:.0f}' for x, y in [ell(LX, LY, math.pi * i / 60) for i in range(61)]) + '" fill="none" stroke="#ff6a4a" stroke-width="5" stroke-dasharray="24 16" opacity=".85"/>'
    b += ring_part(True, RX, RY, TT)
    # Triton breaking apart in front of Neptune
    b += f'<circle cx="{TX:.0f}" cy="{TY:.0f}" r="220" fill="url(#hot)"/>'
    b += cracked(TX, TY, 100, 7, [0, 62, 130, 200, 255, 310, 360], 12)
    b += f'<circle cx="{TX:.0f}" cy="{TY:.0f}" r="30" fill="#ffe6b0" opacity=".85" filter="url(#b12)"/>'
    random.seed(8)
    for k in range(10):  # flying shards
        a = random.uniform(0, 2 * math.pi); r = random.uniform(130, 200)
        b += rock(TX + r * math.cos(a), TY + r * .8 * math.sin(a), random.uniform(6, 12), '#e8d2c6', random.uniform(0, 360))
    for x, y, s in ((140, 180, 18), (960, 160, 22), (990, 640, 14)):
        b += spark(x, y, s)
    # foreground: a big chunk flung toward the camera with the frog clinging on, smaller shards around it (motion streaks point back up to Triton)
    KX, KY = 560, 1700
    b += f'<circle cx="{KX}" cy="{KY}" r="420" fill="url(#hot2)"/>'
    for k in range(7):
        x0 = KX - 180 + k * 60
        b += f'<path d="M{x0} {KY - 170} L{x0 - 70 + k * 10} {KY - 330}" stroke="#ffd2a0" stroke-width="{6 - abs(k - 3)}" stroke-linecap="round" opacity=".35"/>'
    random.seed(12)
    for x, y, s in ((170, 1480, 34), (930, 1460, 40), (130, 1780, 24), (960, 1790, 30), (800, 1400, 16), (300, 1380, 14)):
        b += rock(x, y, s, random.choice(['#e8d2c6', '#d8b1a6']), random.uniform(0, 360), sw=4)
    random.seed(21)   # the chunk: one jagged boulder, its fresh broken face glowing along the cracks
    pts = []
    for k in range(13):
        a = 2 * math.pi * k / 13; r = 190 * random.uniform(.8, 1.05)
        pts.append((KX + r * math.cos(a), KY + r * .62 * math.sin(a)))
    pd = 'M' + ' L'.join(f'{x:.0f} {y:.0f}' for x, y in pts) + 'Z'
    b += f'<path d="{pd}" fill="#ffb060" opacity=".7" filter="url(#b12)"/>'
    b += f'<path d="{pd}" fill="url(#tri)" stroke="#2a1a24" stroke-width="7" stroke-linejoin="round"/>'
    for (x0, y0), (x1, y1), (x2, y2) in (((KX - 150, KY - 40), (KX - 60, KY + 10), (KX - 20, KY + 90)), ((KX + 40, KY - 90), (KX + 70, KY - 10), (KX + 150, KY + 30)),
                                        ((KX - 60, KY + 10), (KX + 20, KY + 20), (KX + 70, KY - 10))):
        b += f'<path d="M{x0} {y0} L{x1} {y1} L{x2} {y2}" fill="none" stroke="#ffb060" stroke-width="16" stroke-linecap="round" stroke-linejoin="round" opacity=".6" filter="url(#b3)"/>'
        b += f'<path d="M{x0} {y0} L{x1} {y1} L{x2} {y2}" fill="none" stroke="#fff0c0" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/>'
    for _ in range(9):  # cantaloupe dimples
        b += f'<circle cx="{KX + random.uniform(-140, 140):.0f}" cy="{KY + random.uniform(-60, 70):.0f}" r="{random.uniform(9, 16):.0f}" fill="none" stroke="#8a5f5a" stroke-width="3" opacity=".5"/>'
    FX, FY, S = KX - 20, 1622, 2.4
    b += frog(FX, FY, S, la='q-28 -4 -42 22', ra='q28 -4 42 22', mouth='o', look=(-2, -5), helmet=True, tilt=-8)
    return vpage('#040516', vsvg(d, b), [('A MOON', 156, 'w'), ('RIPPED', 206, 'w'), ('APART', 246, 'y')], outline='#040516', top=730)


open(os.path.join(HERE, 'A.html'), 'w').write(make())
print('wrote A')
