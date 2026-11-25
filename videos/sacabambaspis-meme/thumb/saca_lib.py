# Shared drawing helpers for the sacabambaspis-meme thumbnails (long make.py + make_shorts.py).
# Stylised (cute) Sacabambaspis: jawless, armoured front half (dorsal + ventral shield, row of small plates on the seam),
# eyes at the very front of the head, mouth = simple opening ringed by small plates, no paired fins, scaly tail ending in a fin.
# Mascot frog = tools/assets/frog.svg body (eye whites #f4f5ea r13.5 so tools/check/eyecheck.py can read them).
import math, random, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../../tools'))
from thumb_lib import lin, rad, spark

INK = '#1d2b1c'; GREEN = '#6aa55a'
FILTERS = ''.join(f'<filter id="b{d}" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="{d}"/></filter>' for d in (2, 3, 4, 6, 10, 12, 24, 50))
_uid = [0]


def uid(p='u'):
    _uid[0] += 1
    return f'{p}{_uid[0]}'


# ---------------- mascot frog ----------------
def frog(x, y, s, mouth='o', arms=('q-14 6 -16 22', 'q14 6 16 22'), look=(2, 0), back='', torso='', head='', front='', flip=False, sweat=False):
    sx = -s if flip else s
    dx, dy = look; d = math.hypot(dx, dy)
    if d > 6: dx, dy = dx * 6 / d, dy * 6 / d
    g = f'<g transform="translate({x} {y}) scale({sx} {s})" stroke="{INK}" stroke-linejoin="round" stroke-linecap="round">'
    g += back
    g += '<ellipse cx="-22" cy="4" rx="16" ry="9" fill="#4d8a4a" stroke-width="3.2"/><ellipse cx="22" cy="4" rx="16" ry="9" fill="#4d8a4a" stroke-width="3.2"/>'
    g += f'<path d="M-34 0 q-6 -64 34 -70 q40 -2 42 62 q0 10 -6 12 q-36 6 -70 -4z" fill="{GREEN}" stroke-width="4"/>'
    g += '<ellipse cx="2" cy="-12" rx="22" ry="20" fill="#9cc98a" stroke="none" opacity=".7"/>'
    g += '<path d="M-26 -50 q6 -16 22 -18" fill="none" stroke="#b9e0a6" stroke-width="3" opacity=".7"/>'
    g += torso
    for ex in (-10, 22):
        g += f'<circle cx="{ex}" cy="-66" r="13.5" fill="#f4f5ea" stroke-width="3.2"/><circle cx="{ex + dx:.1f}" cy="{-66 + dy:.1f}" r="5" fill="{INK}" stroke="none"/>'
        g += f'<circle cx="{ex + 1.6 + dx * .6:.1f}" cy="{-67.8 + dy * .6:.1f}" r="1.7" fill="#fff" stroke="none"/>'
    g += '<ellipse cx="-18" cy="-46" rx="5" ry="3" fill="#e98a8a" stroke="none" opacity=".55"/><ellipse cx="30" cy="-46" rx="5" ry="3" fill="#e98a8a" stroke="none" opacity=".55"/>'
    if mouth == 'o':
        g += '<ellipse cx="6" cy="-42" rx="6.5" ry="8" fill="#7a2f33" stroke-width="3"/><ellipse cx="6" cy="-38" rx="3.5" ry="2.6" fill="#e07b7b" stroke="none"/>'
    elif mouth == 'O':
        g += '<ellipse cx="6" cy="-40" rx="8" ry="11" fill="#7a2f33" stroke-width="3"/><ellipse cx="6" cy="-35" rx="4.5" ry="3.2" fill="#e07b7b" stroke="none"/>'
    else:
        g += '<path d="M-8 -45 q14 14 28 0 q-14 4 -28 0z" fill="#7a2f33" stroke-width="3"/>'
    if sweat:
        g += '<path d="M40 -84 q6 9 0 13 q-6 -4 0 -13z" fill="#bfe8ff" stroke-width="2.2"/>'
    g += head
    la, ra = arms
    for st, path in (('M-32 -22', la), ('M38 -22', ra)):
        g += f'<path d="{st} {path}" fill="none" stroke-width="7.5"/><path d="{st} {path}" fill="none" stroke="{GREEN}" stroke-width="3.4"/>'
        sx0, sy0 = map(float, st[1:].split()); q = [float(v) for v in path[1:].split()]
        g += f'<circle cx="{sx0 + q[2]}" cy="{sy0 + q[3]}" r="5.5" fill="{GREEN}" stroke-width="3"/>'
    g += front
    return g + '</g>'


def diving_helmet():
    """front layer for frog(): glass dome + brass collar (local frog coords)"""
    g = '<circle cx="6" cy="-56" r="42" fill="#bfe6ff" fill-opacity=".14" stroke="#d6a94f" stroke-width="4.5"/>'
    g += '<circle cx="6" cy="-56" r="37.5" fill="none" stroke="#fff" stroke-width="1.6" opacity=".35"/>'
    g += '<path d="M-24 -78 A34 34 0 0 1 8 -92" fill="none" stroke="#fff" stroke-width="5" opacity=".75"/>'
    g += '<ellipse cx="5" cy="-16" rx="38" ry="9" fill="#c48d38" stroke-width="3.2"/><path d="M-30 -18 q35 8 70 0" fill="none" stroke="#f4d58a" stroke-width="2.2" opacity=".8"/>'
    g += ''.join(f'<circle cx="{c}" cy="-15" r="2.4" fill="#ffe7a6" stroke="none"/>' for c in (-24, -9, 6, 21, 34))
    return g


def air_tank():
    return ('<rect x="-56" y="-62" width="22" height="52" rx="10" fill="#e3ab3e" stroke-width="3.2"/><rect x="-52" y="-56" width="5" height="40" rx="2" fill="#fff3c4" stroke="none" opacity=".7"/>'
            '<path d="M-46 -62 q-6 -34 22 -38" fill="none" stroke-width="8"/><path d="M-46 -62 q-6 -34 22 -38" fill="none" stroke="#6b6f78" stroke-width="4"/>')


def bubbles(x, y, n, spread=30, rise=220, s=1.0, col='#dff6ff'):
    out = ''
    for i in range(n):
        yy = y - rise * i / n - random.uniform(0, 16); xx = x + math.sin(i * 1.7) * spread * i / n
        r = (4 + 7 * random.random()) * s
        out += f'<circle cx="{xx:.0f}" cy="{yy:.0f}" r="{r:.1f}" fill="{col}" fill-opacity=".12" stroke="{col}" stroke-width="2" stroke-opacity=".7"/>'
        out += f'<circle cx="{xx - r * .35:.0f}" cy="{yy - r * .35:.0f}" r="{r * .25:.1f}" fill="#fff" opacity=".8"/>'
    return out


def motes(n, x0, y0, x1, y1, col='#dfeee8', omax=.55, rmax=2.6):
    return ''.join(f'<circle cx="{random.uniform(x0, x1):.0f}" cy="{random.uniform(y0, y1):.0f}" r="{random.uniform(.8, rmax):.1f}" fill="{col}" opacity="{random.uniform(.1, omax):.2f}"/>' for _ in range(n))


# ---------------- Sacabambaspis, side view ----------------
# local coords: nose at x~10 (facing -x), armour to x=276, tail fin tip x~646; height about -96..80.
ARMOR = 'M14,8 C4,-38 46,-92 132,-96 C204,-98 254,-76 276,-48 L278,54 C240,76 160,84 96,76 C44,70 8,48 14,8Z'
SEAM = 'M16,16 C80,26 180,24 278,10'
PAL = {
    'live': dict(hi='#f0d29a', mid='#c9965a', lo='#6e4426', edge='#2a160c', belly='#e6c58e', tail='#8fa6a0', tail_lo='#4c5f5c', fin='#a9c4bc',
                 rim='#bff6ff', tub='#fff0c8', groove='#5a3218', plate='#d9b27a'),
    'fossil': dict(hi='#efe0bf', mid='#cdb487', lo='#8a6a46', edge='#4a3220', belly='#dcc79c', tail='#b49a72', tail_lo='#7a5e40', fin='#c8b088',
                   rim='#fff4dc', tub='#fff8e6', groove='#6e5236', plate='#e2cfa6'),
    'glow': dict(hi='#fff3c4', mid='#e9b46a', lo='#8a5228', edge='#2a160c', belly='#ffe0a0', tail='#9fd8d0', tail_lo='#3e6e72', fin='#c6fff4',
                 rim='#d6fff8', tub='#fffbe6', groove='#6a3a18', plate='#f4cc8a'),
}


def tail_path(bend):
    """tail outline from the armour back (x 276) to the fin; bend = vertical sway of the tail tip (px)"""
    b = bend
    top = f'M272,-46 C350,{-40 + b * .2:.0f} 440,{-20 + b * .6:.0f} 530,{-6 + b:.0f}'
    fin = (f'C560,{-34 + b * 1.1:.0f} 604,{-46 + b * 1.15:.0f} 650,{-44 + b * 1.2:.0f} C618,{-18 + b * 1.15:.0f} 606,{0 + b * 1.1:.0f} 610,{6 + b * 1.1:.0f} '
           f'C628,{30 + b * 1.1:.0f} 648,{56 + b * 1.15:.0f} 654,{76 + b * 1.2:.0f} C604,{62 + b * 1.1:.0f} 562,{34 + b:.0f} 530,{12 + b:.0f}')
    bot = f'C440,{24 + b * .6:.0f} 350,{46 + b * .2:.0f} 276,54 Z'
    return top + ' ' + fin + ' ' + bot


def saca(x, y, s, flip=False, rot=0, pal='live', mouth='O', look=(4, 0), bend=0, glow=None, rim=True, eyes=True, detail=1.0, shadow=True):
    """side-view Sacabambaspis. flip=False faces LEFT. glow = colour of a soft halo behind it."""
    P = PAL[pal] if isinstance(pal, str) else pal
    cid = uid('sc'); tid = uid('st'); gid = uid('sg')
    sx = -s if flip else s
    out = f'<g transform="translate({x} {y}) rotate({rot}) scale({sx} {s})">'
    defs = (f'<clipPath id="{cid}"><path d="{ARMOR}"/></clipPath><clipPath id="{tid}"><path d="{tail_path(bend)}"/></clipPath>'
            f'<linearGradient id="{gid}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{P["hi"]}"/><stop offset=".55" stop-color="{P["mid"]}"/><stop offset="1" stop-color="{P["lo"]}"/></linearGradient>')
    out += f'<defs>{defs}</defs>'
    if glow:
        out += f'<ellipse cx="300" cy="0" rx="420" ry="190" fill="{glow}" opacity=".35" filter="url(#b50)"/>'
    if shadow:
        out += '<ellipse cx="300" cy="96" rx="300" ry="20" fill="#000" opacity=".22" filter="url(#b12)"/>'
    # tail
    tp = tail_path(bend)
    out += f'<path d="{tp}" fill="{P["tail"]}" stroke="{P["edge"]}" stroke-width="5" stroke-linejoin="round"/>'
    sc = ''
    for i in range(18):
        xx = 286 + i * 19
        for j in range(-4, 5):
            yy = j * 15 + bend * max(0, (xx - 276)) / 260 * .8 + (i % 2) * 7
            sc += f'M{xx},{yy - 7:.0f} q8 7 0 14 '
    out += f'<g clip-path="url(#{tid})"><path d="{sc}" fill="none" stroke="{P["tail_lo"]}" stroke-width="2.2" opacity=".75"/>'
    out += f'<path d="M272,30 C360,40 450,{30 + bend * .7:.0f} 540,{18 + bend:.0f} L560,{90 + bend:.0f} L270,90Z" fill="{P["tail_lo"]}" opacity=".45"/>'
    out += f'<path d="M530,{-6 + bend:.0f} C580,{-30 + bend * 1.1:.0f} 620,{-40 + bend * 1.15:.0f} 650,{-44 + bend * 1.2:.0f} M530,{12 + bend:.0f} C580,{40 + bend * 1.1:.0f} 630,{64 + bend * 1.15:.0f} 654,{76 + bend * 1.2:.0f}" stroke="{P["fin"]}" stroke-width="3" fill="none" opacity=".8"/>'
    for k in range(7):   # fin rays
        a = -40 + k * 18
        out += f'<path d="M548,{4 + bend * 1.05:.0f} l{math.cos(math.radians(a)) * 90:.0f},{math.sin(math.radians(a)) * 60:.0f}" stroke="{P["tail_lo"]}" stroke-width="2" opacity=".55"/>'
    out += '</g>'
    if rim:
        out += f'<path d="M272,-46 C350,{-40 + bend * .2:.0f} 440,{-20 + bend * .6:.0f} 530,{-6 + bend:.0f}" fill="none" stroke="{P["rim"]}" stroke-width="3.5" opacity=".8"/>'
    # armour
    out += f'<path d="{ARMOR}" fill="url(#{gid})"/>'
    a = f'<g clip-path="url(#{cid})">'
    a += f'<path d="{SEAM} L290,120 L0,120Z" fill="{P["belly"]}" opacity=".55"/>'   # ventral shield tone
    a += f'<path d="{SEAM} L290,120 L0,120Z" fill="{P["lo"]}" opacity=".35"/>'
    random.seed(int(x * 7 + y * 3) % 9973)
    tub = ''
    for _ in range(int(150 * detail)):
        tx, ty = random.uniform(20, 276), random.uniform(-96, 78)
        tub += f'<circle cx="{tx:.0f}" cy="{ty:.0f}" r="{random.choice([1.6, 2.2, 2.8])}" />'
    a += f'<g fill="{P["tub"]}" opacity=".55">{tub}</g>'
    # ridges / lateral line grooves
    a += f'<path d="M60,-70 C120,-80 200,-78 270,-60 M70,-46 C130,-56 210,-54 274,-34 M40,40 C110,52 190,52 274,38 M90,-20 C150,-26 220,-22 276,-12" fill="none" stroke="{P["groove"]}" stroke-width="2.6" opacity=".55" stroke-dasharray="10 5"/>'
    a += f'<path d="M14,8 C4,-38 46,-92 132,-96 C204,-98 254,-76 276,-48" fill="none" stroke="{P["hi"]}" stroke-width="16" opacity=".55" transform="translate(4 8)"/>'
    a += f'<ellipse cx="150" cy="-62" rx="70" ry="16" fill="#fff" opacity=".22"/>'
    a += '</g>'
    out += a
    out += f'<path d="{SEAM}" fill="none" stroke="{P["edge"]}" stroke-width="3.2"/>'
    # small plates along the seam (branchial plates)
    for i in range(9):
        px = 104 + i * 19; py = 18 + (i / 8) * -8
        out += f'<rect x="{px - 7}" y="{py - 13:.0f}" width="15" height="24" rx="5" fill="{P["plate"]}" stroke="{P["edge"]}" stroke-width="2.6"/>'
    out += f'<path d="{ARMOR}" fill="none" stroke="{P["edge"]}" stroke-width="5.5" stroke-linejoin="round"/>'
    if rim:
        out += f'<path d="M24,-30 C50,-82 100,-94 150,-95 C210,-96 252,-76 272,-50" fill="none" stroke="{P["rim"]}" stroke-width="4" opacity=".9"/>'
    # mouth (simple opening ringed by small plates)
    if mouth:
        mrx, mry = (13, 18) if mouth == 'O' else (8, 9)
        mx, my = 22, 30
        for k in range(10):
            ang = math.radians(k * 36)
            out += f'<circle cx="{mx + math.cos(ang) * (mrx + 6):.1f}" cy="{my + math.sin(ang) * (mry + 6):.1f}" r="4.6" fill="{P["plate"]}" stroke="{P["edge"]}" stroke-width="2"/>'
        out += f'<ellipse cx="{mx}" cy="{my}" rx="{mrx}" ry="{mry}" fill="#3a1414" stroke="{P["edge"]}" stroke-width="3"/>'
        out += f'<ellipse cx="{mx + 2}" cy="{my + mry * .45:.1f}" rx="{mrx * .55:.1f}" ry="{mry * .3:.1f}" fill="#8a3a3a" opacity=".8"/>'
    if eyes:
        dx, dy = look
        for ex, ey, r, far in ((50, -50, 15, True), (30, -40, 19, False)):
            if far:
                out += f'<circle cx="{ex}" cy="{ey}" r="{r + 4}" fill="{P["lo"]}" stroke="{P["edge"]}" stroke-width="3"/>'
            out += f'<circle cx="{ex}" cy="{ey}" r="{r}" fill="#f8f6ea" stroke="{P["edge"]}" stroke-width="3.4"/>'
            out += f'<circle cx="{ex - abs(dx) * .9 - 2:.1f}" cy="{ey + dy:.1f}" r="{r * .5:.1f}" fill="#141414"/>'
            out += f'<circle cx="{ex - abs(dx) * .9 - 2 - r * .18:.1f}" cy="{ey + dy - r * .2:.1f}" r="{r * .17:.1f}" fill="#fff"/>'
    elif pal == 'fossil':
        out += f'<circle cx="34" cy="-42" r="16" fill="{P["lo"]}" stroke="{P["edge"]}" stroke-width="3"/><circle cx="54" cy="-52" r="12" fill="{P["lo"]}" stroke="{P["edge"]}" stroke-width="3" opacity=".8"/>'
    return out + '</g>'


# ---------------- Sacabambaspis, front view (head on, tail curving down behind like a standing figure) ----------------
def saca_front(x, y, s, mouth='O', look=(0, 0), sway=60, length=560, glow=None, P=None, wave=False):
    P = P or PAL['live']
    gid = uid('fg'); cid = uid('fc'); bid = uid('fb')
    out = f'<g transform="translate({x} {y}) scale({s})">'
    # body behind: S-curve from the head down to the tail fin
    N = 40; L = []; R = []
    for i in range(N + 1):
        t = i / N
        cx = sway * math.sin(t * math.pi * 1.3) ; cy = 90 + length * t
        w = 128 * (1 - t) ** .9 + 14
        tx = sway * math.pi * 1.3 * math.cos(t * math.pi * 1.3) / length; nx, ny = 1, -tx; nn = math.hypot(nx, ny)
        L.append((cx - w * nx / nn, cy - w * ny / nn)); R.append((cx + w * nx / nn, cy + w * ny / nn))
    body = 'M' + ' L'.join(f'{a:.1f},{b:.1f}' for a, b in L) + ' L' + ' L'.join(f'{a:.1f},{b:.1f}' for a, b in reversed(R)) + 'Z'
    tipx, tipy = sway * math.sin(math.pi * 1.3), 90 + length
    out += f'<defs><linearGradient id="{gid}" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{P["hi"]}"/><stop offset=".5" stop-color="{P["mid"]}"/><stop offset="1" stop-color="{P["lo"]}"/></linearGradient>'
    out += f'<linearGradient id="{bid}" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{P["tail_lo"]}"/><stop offset=".45" stop-color="{P["tail"]}"/><stop offset="1" stop-color="{P["tail_lo"]}"/></linearGradient>'
    out += f'<clipPath id="{cid}"><path d="{body}"/></clipPath></defs>'
    if glow:
        out += f'<ellipse cx="0" cy="-10" rx="330" ry="300" fill="{glow}" opacity=".5" filter="url(#b50)"/>'
    # tail fin at the bottom
    out += (f'<path d="M{tipx - 16:.0f},{tipy - 20:.0f} C{tipx - 90:.0f},{tipy + 10:.0f} {tipx - 120:.0f},{tipy + 60:.0f} {tipx - 110:.0f},{tipy + 96:.0f} '
            f'C{tipx - 50:.0f},{tipy + 70:.0f} {tipx - 10:.0f},{tipy + 50:.0f} {tipx:.0f},{tipy + 30:.0f} C{tipx + 20:.0f},{tipy + 60:.0f} {tipx + 70:.0f},{tipy + 84:.0f} {tipx + 120:.0f},{tipy + 90:.0f} '
            f'C{tipx + 100:.0f},{tipy + 50:.0f} {tipx + 60:.0f},{tipy + 10:.0f} {tipx + 16:.0f},{tipy - 20:.0f}Z" fill="{P["fin"]}" stroke="{P["edge"]}" stroke-width="5" stroke-linejoin="round"/>')
    for k in range(6):
        out += f'<path d="M{tipx:.0f},{tipy:.0f} l{-100 + k * 44},{70 + abs(k - 2.5) * 6:.0f}" stroke="{P["tail_lo"]}" stroke-width="2.4" opacity=".6"/>'
    out += f'<path d="{body}" fill="url(#{bid})" stroke="{P["edge"]}" stroke-width="5.5" stroke-linejoin="round"/>'
    sc = ''
    for i in range(1, 28):
        t = i / 28; cx = sway * math.sin(t * math.pi * 1.3); cy = 90 + length * t; w = 128 * (1 - t) ** .9 + 14
        for j in range(-4, 5):
            sc += f'M{cx + j * w / 4.5 - 9:.0f},{cy - 6:.0f} q9 10 18 0 '
    out += f'<g clip-path="url(#{cid})"><path d="{sc}" fill="none" stroke="{P["tail_lo"]}" stroke-width="2.4" opacity=".7"/></g>'
    # head shield
    head = 'M-176,8 C-182,-112 -86,-166 0,-166 C86,-166 182,-112 176,8 C170,112 86,156 0,156 C-86,156 -170,112 -176,8Z'
    out += f'<path d="{head}" fill="url(#{gid})" stroke="{P["edge"]}" stroke-width="6"/>'
    random.seed(11)
    tub = ''.join(f'<circle cx="{random.uniform(-170, 170):.0f}" cy="{random.uniform(-160, 150):.0f}" r="{random.choice([2, 2.6, 3.2])}"/>' for _ in range(160))
    hid = uid('hc')
    out += f'<defs><clipPath id="{hid}"><path d="{head}"/></clipPath></defs><g clip-path="url(#{hid})">'
    out += f'<g fill="{P["tub"]}" opacity=".5">{tub}</g>'
    out += f'<path d="M-176,40 C-100,70 100,70 176,40 L176,200 L-176,200Z" fill="{P["lo"]}" opacity=".35"/>'
    out += f'<path d="M-150,-60 C-120,-130 -40,-150 20,-148" fill="none" stroke="#fff" stroke-width="18" opacity=".25"/>'
    out += f'<path d="M-160,-10 C-110,-40 -60,-50 -20,-48 M160,-10 C110,-40 60,-50 20,-48 M-150,60 C-100,40 -70,40 -50,48 M150,60 C100,40 70,40 50,48" fill="none" stroke="{P["groove"]}" stroke-width="3" opacity=".55" stroke-dasharray="12 6"/>'
    out += '</g>'
    # side plates (seam)
    for side in (-1, 1):
        for i in range(6):
            px = side * (150 - i * 3); py = 30 + i * 22
            out += f'<rect x="{px - 10}" y="{py - 9}" width="20" height="18" rx="6" fill="{P["plate"]}" stroke="{P["edge"]}" stroke-width="3" transform="rotate({side * 20} {px} {py})"/>'
    # eyes at the very front
    dx, dy = look
    for ex in (-66, 66):
        out += f'<circle cx="{ex}" cy="-52" r="50" fill="{P["lo"]}" stroke="{P["edge"]}" stroke-width="4"/>'
        out += f'<circle cx="{ex}" cy="-52" r="42" fill="#f8f6ea" stroke="{P["edge"]}" stroke-width="4.5"/>'
        out += f'<circle cx="{ex + dx}" cy="{-52 + dy}" r="17" fill="#141414"/><circle cx="{ex + dx - 6}" cy="{-59 + dy}" r="6" fill="#fff"/>'
    # mouth: simple opening ringed by small plates
    mrx, mry = (38, 50) if mouth == 'O' else (20, 18)
    for k in range(14):
        ang = math.radians(k * 360 / 14)
        out += f'<circle cx="{math.cos(ang) * (mrx + 12):.1f}" cy="{66 + math.sin(ang) * (mry + 12):.1f}" r="9" fill="{P["plate"]}" stroke="{P["edge"]}" stroke-width="3"/>'
    out += f'<ellipse cx="0" cy="66" rx="{mrx}" ry="{mry}" fill="#2e0f10" stroke="{P["edge"]}" stroke-width="4"/>'
    out += f'<ellipse cx="0" cy="{66 + mry * .5:.0f}" rx="{mrx * .55:.0f}" ry="{mry * .28:.0f}" fill="#8a3a3a"/>'
    out += f'<path d="M-140,-120 C-100,-160 -40,-168 10,-166" fill="none" stroke="{P["rim"]}" stroke-width="6" opacity=".9"/>'
    return out + '</g>'


# ---------------- sea scorpion (eurypterid), top view, head pointing -x ----------------
def eurypterid(x, y, s, rot=0, body='#7a3424', hi='#c8704a', dark='#2a0f08', rim='#bff3ff', claw_open=1.0):
    out = f'<g transform="translate({x} {y}) rotate({rot}) scale({s})" stroke-linejoin="round" stroke-linecap="round">'
    # telson spike
    out += f'<path d="M520,-18 L760,0 L520,18Z" fill="{body}" stroke="{dark}" stroke-width="5"/>'
    out += f'<path d="M520,-8 L740,0" stroke="{hi}" stroke-width="3" opacity=".6"/>'
    # swimming paddles (big, behind)
    for side in (-1, 1):
        out += f'<path d="M110,{side * 60} C150,{side * 140} 200,{side * 190} 250,{side * 210}" fill="none" stroke="{dark}" stroke-width="26"/>'
        out += f'<path d="M110,{side * 60} C150,{side * 140} 200,{side * 190} 250,{side * 210}" fill="none" stroke="{body}" stroke-width="17"/>'
        out += f'<ellipse cx="280" cy="{side * 226}" rx="62" ry="34" transform="rotate({side * 20} 280 {side * 226})" fill="{body}" stroke="{dark}" stroke-width="5"/>'
        out += f'<ellipse cx="272" cy="{side * 220}" rx="40" ry="14" transform="rotate({side * 20} 272 {side * 220})" fill="{hi}" opacity=".45"/>'
        # walking legs
        for k, (lx, ly) in enumerate(((30, 130), (70, 160), (100, 175))):
            out += f'<path d="M{50 + k * 20},{side * 50} q{-lx * .2:.0f},{side * ly * .6:.0f} {-lx * .5:.0f},{side * ly:.0f}" fill="none" stroke="{dark}" stroke-width="12"/>'
            out += f'<path d="M{50 + k * 20},{side * 50} q{-lx * .2:.0f},{side * ly * .6:.0f} {-lx * .5:.0f},{side * ly:.0f}" fill="none" stroke="{body}" stroke-width="6"/>'
    # spiny grasping front limbs reaching forward
    for side in (-1, 1):
        pts = [(0, side * 40), (-120, side * (70 + 20 * claw_open)), (-250, side * (40 + 30 * claw_open)), (-340, side * (8 + 26 * claw_open))]
        d = 'M' + ' L'.join(f'{a:.0f},{b:.0f}' for a, b in pts)
        out += f'<path d="{d}" fill="none" stroke="{dark}" stroke-width="26"/><path d="{d}" fill="none" stroke="{body}" stroke-width="16"/><path d="{d}" fill="none" stroke="{hi}" stroke-width="4" opacity=".6" transform="translate(0 {-side * 4})"/>'
        for i in range(len(pts) - 1):
            (a0, b0), (a1, b1) = pts[i], pts[i + 1]
            for k in range(1, 4):
                t = k / 4; sxp, syp = a0 + (a1 - a0) * t, b0 + (b1 - b0) * t
                out += f'<path d="M{sxp:.0f},{syp:.0f} l{-14:.0f},{-side * 38:.0f}" stroke="{dark}" stroke-width="7"/><path d="M{sxp:.0f},{syp:.0f} l{-13:.0f},{-side * 34:.0f}" stroke="{hi}" stroke-width="3"/>'
                out += f'<path d="M{sxp:.0f},{syp:.0f} l{-10:.0f},{side * 26:.0f}" stroke="{dark}" stroke-width="5"/>'
    # body segments (opisthosoma)
    for i in range(12, -1, -1):
        sx0 = 120 + i * 32; w = 168 - i * 9.5
        out += f'<path d="M{sx0},{-w / 2:.0f} C{sx0 + 26},{-w / 2:.0f} {sx0 + 46},{-w / 2.6:.0f} {sx0 + 46},0 C{sx0 + 46},{w / 2.6:.0f} {sx0 + 26},{w / 2:.0f} {sx0},{w / 2:.0f} C{sx0 - 6},{w / 4:.0f} {sx0 - 6},{-w / 4:.0f} {sx0},{-w / 2:.0f}Z" fill="{body}" stroke="{dark}" stroke-width="5"/>'
        out += f'<path d="M{sx0 + 8},{-w / 2.4:.0f} C{sx0 + 30},{-w / 2.6:.0f} {sx0 + 38},{-w / 5:.0f} {sx0 + 40},0" fill="none" stroke="{hi}" stroke-width="5" opacity=".55"/>'
    out += f'<path d="M140,-80 C300,-72 460,-40 540,-14" fill="none" stroke="{rim}" stroke-width="4" opacity=".7"/>'
    # head shield (prosoma)
    out += f'<path d="M-10,-30 C-14,-80 40,-104 120,-96 C150,-92 156,-70 156,0 C156,70 150,92 120,96 C40,104 -14,80 -10,30Z" fill="{body}" stroke="{dark}" stroke-width="6"/>'
    out += f'<path d="M0,-40 C10,-80 60,-94 120,-88" fill="none" stroke="{hi}" stroke-width="8" opacity=".6"/>'
    out += f'<path d="M-6,-46 C0,-90 60,-104 130,-94" fill="none" stroke="{rim}" stroke-width="4" opacity=".85"/>'
    for side in (-1, 1):
        out += f'<ellipse cx="60" cy="{side * 50}" rx="24" ry="13" transform="rotate({side * -18} 60 {side * 50})" fill="#1a0a06" stroke="{dark}" stroke-width="3"/>'
        out += f'<ellipse cx="54" cy="{side * 48}" rx="9" ry="4" fill="#ffd0a0" opacity=".7" transform="rotate({side * -18} 54 {side * 48})"/>'
    out += f'<circle cx="80" cy="-6" r="5" fill="#1a0a06"/><circle cx="80" cy="8" r="5" fill="#1a0a06"/>'
    return out + '</g>'


# ---------------- sea floor bits ----------------
def brachiopod(x, y, s=1.0, col='#d8c49a', dark='#4a3a28', rot=0):
    g = f'<g transform="translate({x} {y}) rotate({rot}) scale({s})">'
    g += f'<path d="M-30,0 C-32,-26 -14,-38 0,-38 C14,-38 32,-26 30,0 C20,8 -20,8 -30,0Z" fill="{col}" stroke="{dark}" stroke-width="3"/>'
    g += ''.join(f'<path d="M0,-34 L{k * 7},2" stroke="{dark}" stroke-width="1.6" opacity=".6"/>' for k in range(-4, 5))
    g += f'<path d="M-24,-20 C-12,-34 12,-34 24,-20" fill="none" stroke="#fff" stroke-width="3" opacity=".4"/>'
    return g + '</g>'


def crinoid(x, y, h, s=1.0, col='#c86a8a', dark='#4a1a2a', lean=10):
    g = f'<path d="M{x},{y} q{lean},{-h * .5:.0f} {lean * 1.6:.0f},{-h}" fill="none" stroke="{dark}" stroke-width="{12 * s:.1f}" stroke-linecap="round"/>'
    g += f'<path d="M{x},{y} q{lean},{-h * .5:.0f} {lean * 1.6:.0f},{-h}" fill="none" stroke="{col}" stroke-width="{7 * s:.1f}" stroke-linecap="round" stroke-dasharray="{4 * s:.1f} {3 * s:.1f}"/>'
    tx, ty = x + lean * 1.6, y - h
    for k in range(8):
        a = math.radians(-160 + k * 20)
        L = 70 * s
        g += f'<path d="M{tx:.0f},{ty:.0f} q{math.cos(a) * L * .4:.0f},{math.sin(a) * L * .9:.0f} {math.cos(a) * L:.0f},{math.sin(a) * L * .7 + 10 * s:.0f}" fill="none" stroke="{dark}" stroke-width="{9 * s:.1f}" stroke-linecap="round"/>'
        g += f'<path d="M{tx:.0f},{ty:.0f} q{math.cos(a) * L * .4:.0f},{math.sin(a) * L * .9:.0f} {math.cos(a) * L:.0f},{math.sin(a) * L * .7 + 10 * s:.0f}" fill="none" stroke="{col}" stroke-width="{4.5 * s:.1f}" stroke-linecap="round"/>'
    g += f'<ellipse cx="{tx:.0f}" cy="{ty:.0f}" rx="{14 * s:.0f}" ry="{10 * s:.0f}" fill="{col}" stroke="{dark}" stroke-width="3"/>'
    return g
