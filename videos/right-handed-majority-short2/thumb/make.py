# Shorts thumbnail (VERTICAL 1080x1920, text centred) for right-handed-majority-short2 (guideline 16-9, brief tools/briefs/thumb_art.md 'Shorts thumbnails').
# SAME DNA, DIFFERENT HAND   intuitive: identical twins (same face, hair, clothes) on both sides of a big glowing DNA helix;
#                            one raises a crayon in the RIGHT hand, the other in the LEFT hand, both stare at each other.
#                            Frog in a lab coat and goggles at the lab bench (script: identical twins share 100% of their
#                            nuclear DNA, yet roughly one in five identical pairs are discordant; no single left-handed gene).
import os, sys, math, random, importlib.util
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', '..', 'tools'))
_s = importlib.util.spec_from_file_location('rhm_thumb', os.path.join(HERE, '..', '..', 'right-handed-majority', 'thumb', 'make.py'))
L = importlib.util.module_from_spec(_s); _s.loader.exec_module(L)
from thumb_lib import vpage, vsvg, lin, rad, spark
from body import shoulders
LINE, BODY = L.LINE, L.BODY


def helix(cx, y0, y1, A, per, w):
    """returns (back, front) svg of a double helix"""
    back = front = ''
    n = 120
    pts1 = []; pts2 = []
    for i in range(n + 1):
        y = y0 + (y1 - y0) * i / n; ph = 2 * math.pi * (y - y0) / per
        pts1.append((cx + A * math.sin(ph), y, math.cos(ph))); pts2.append((cx - A * math.sin(ph), y, -math.cos(ph)))
    # rungs
    for i in range(0, n, 4):
        (x1, y, z1), (x2, _, z2) = pts1[i], pts2[i]
        col = ['#F2D27A', '#7affc8', '#ff8ac8', '#8ac8ff'][(i // 4) % 4]
        seg = f'<line x1="{x1:.0f}" y1="{y:.0f}" x2="{x2:.0f}" y2="{y:.0f}" stroke="{col}" stroke-width="{w * .45:.0f}" stroke-linecap="round" opacity=".85"/>'
        back += seg
    for pts, col in ((pts1, '#5fe0ff'), (pts2, '#ff7ac8')):
        for i in range(n):
            (xa, ya, za), (xb, yb, zb) = pts[i], pts[i + 1]
            seg = f'<line x1="{xa:.1f}" y1="{ya:.1f}" x2="{xb:.1f}" y2="{yb:.1f}" stroke="{col}" stroke-width="{w:.0f}" stroke-linecap="round"/>'
            if za > 0:
                front += seg
            else:
                back += seg.replace('/>', ' opacity=".55"/>')
    return back, front


def make():
    rnd = random.Random(8)
    d = L.FILTERS
    d += lin('bg2', [(0, '#120a2e'), (.6, '#1c1546'), (1, '#0a0820')])
    d += rad('halo2', 540, 1000, 800, [(0, '#9ae8ff', .5), (.35, '#6a7aff', .22), (1, '#000', 0)])
    d += rad('vig2', 540, 960, 1250, [(0, '#000', 0), (.6, '#000', 0), (1, '#000', .6)])
    d += lin('floor2', [(0, '#1e1a40'), (1, '#0c0a1e')])
    b = '<rect width="1080" height="1920" fill="url(#bg2)"/>'
    for x in range(0, 1080, 120):
        b += f'<line x1="{x}" y1="0" x2="{x}" y2="1680" stroke="#fff" stroke-width="2" opacity=".04"/>'
    for y in range(0, 1680, 120):
        b += f'<line x1="0" y1="{y}" x2="1080" y2="{y}" stroke="#fff" stroke-width="2" opacity=".04"/>'
    b += '<rect width="1080" height="1920" fill="url(#halo2)"/>'
    b += '<rect y="1680" width="1080" height="240" fill="url(#floor2)"/>'
    b += '<path d="M0 1680 L1080 1680" stroke="#6a7aff" stroke-width="4" opacity=".4"/>'
    hb, hf = helix(540, 110, 1800, 130, 360, 22)
    b += f'<g filter="url(#b16)" opacity=".8">{hf}</g>'
    b += hb
    # twins
    H = 128; TOP = 1150; kind = 'cute_child'
    SK = '#e8b48c'; HAIR = ('pony', '#5a2e14'); SHIRT = '#f2a03a'
    for cx, raise_side, look in ((250, 'L', (1.5, -.2)), (830, 'R', (-1.5, -.2))):
        (lx, ly), (rx, ry) = shoulders(cx, TOP, H, kind)
        if raise_side == 'L':    # figure's RIGHT hand (viewer left) raised
            S, T, bd = (lx, ly), (lx - 110, TOP + 90), 1
            O, OT, obd = (rx, ry), (rx + 40, ry + 1.25 * H), -1
            pen = L.pencil(T[0] + 88, T[1] - 225, 174, 240, 38)
        else:                    # figure's LEFT hand (viewer right) raised
            S, T, bd = (rx, ry), (rx + 110, TOP + 90), -1
            O, OT, obd = (lx, ly), (lx - 40, ly + 1.25 * H), 1
            pen = L.pencil(T[0] - 88, T[1] - 225, 186, 240, 38)
        glow = f'<ellipse cx="{T[0] + (100 if raise_side == "L" else -100)}" cy="{T[1] - 180}" rx="110" ry="130" fill="#ffe08a" opacity=".5" filter="url(#b32)"/>'
        up = L.limb_to(S, T, H, kind, bd, f'tw{cx}u', SHIRT, SK, 'short')
        down = L.limb_to(O, OT, H, kind, obd, f'tw{cx}d', SHIRT, SK, 'short')
        b += f'<ellipse cx="{cx}" cy="{TOP + 4.12 * H}" rx="130" ry="20" fill="#000" opacity=".4"/>'
        b += L.person(cx, TOP, H, kind, SK, HAIR, SHIRT, '#3a4f8c', '#1d1d24', look=look, mouth='o', brows='up', props_back=glow,
                      props_front=down + pen + up, sleeve_len='short', rim=(1 if cx < 540 else -1, '#9ae8ff'))
        b += spark(T[0] + (-60 if raise_side == 'L' else 60), TOP - 200, 24) + spark(T[0] + (50 if raise_side == 'L' else -50), TOP - 120, 14)
    # wall shelves at the top with glowing flasks; frog scientist sits on the left shelf
    for x0, x1, y in ((0, 400, 470), (700, 1080, 400)):
        b += f'<rect x="{x0 - 10}" y="{y}" width="{x1 - x0 + 10}" height="26" rx="6" fill="#3a3f6a" stroke="{LINE}" stroke-width="6"/>'
    for x, y, col, h in ((60, 470, '#7affc8', 120), (350, 470, '#ff8ac8', 90), (780, 400, '#5fe0ff', 140), (880, 400, '#F2D27A', 100), (980, 400, '#ff8ac8', 120)):
        b += (f'<ellipse cx="{x}" cy="{y - h * .35}" rx="60" ry="60" fill="{col}" opacity=".35" filter="url(#b16)"/>'
              f'<path d="M{x - 12} {y - h} L{x - 12} {y - h * .55} L{x - 42} {y - 4} L{x + 42} {y - 4} L{x + 12} {y - h * .55} L{x + 12} {y - h}Z" fill="#dfe8ff" fill-opacity=".25" stroke="{LINE}" stroke-width="5" stroke-linejoin="round"/>'
              f'<path d="M{x - 30} {y - 20} L{x + 30} {y - 20} L{x + 40} {y - 6} L{x - 40} {y - 6}Z" fill="{col}"/>')
    goggles = ('<path d="M-30 -84 Q8 -104 46 -84" fill="none" stroke="#3a3a4a" stroke-width="7"/>'
               '<ellipse cx="-6" cy="-96" rx="15" ry="11" fill="#bfe6ff" stroke="#3a3a4a" stroke-width="5"/><ellipse cx="24" cy="-96" rx="15" ry="11" fill="#bfe6ff" stroke="#3a3a4a" stroke-width="5"/>'
               '<path d="M-12 -100 l6 -3 M18 -100 l6 -3" stroke="#fff" stroke-width="3"/>')
    coat = f'<g clip-path="url(#fbody)"><rect x="-50" y="-44" width="110" height="70" fill="#f4f6fb" stroke-width="3"/><path d="M-2 -44 L8 -10 L18 -44" fill="#6aa55a" stroke-width="2.6"/><path d="M8 -10 L8 20" stroke-width="2.4"/></g><path d="{BODY}" fill="none" stroke-width="4"/>'
    b += L.frog(205, 472, 2.3, look=(6, -3), mouth='O', armL='M-34 -24 q-18 -4 -26 16', armR='M38 -24 q22 -14 26 -42', top=goggles, mid=coat, shadow=False)
    b += L.qmark(330, 170, 70, '#F2D27A', 12)
    b += '<ellipse cx="540" cy="790" rx="500" ry="230" fill="#0a0618" opacity=".6" filter="url(#b32)"/>'
    b += '<rect width="1080" height="1920" fill="url(#vig2)"/>'
    lines = [('SAME DNA,', 140, 'y'), ('DIFFERENT', 130, 'w'), ('HAND', 150, 'w')]
    return vpage('#120a2e', vsvg(d, b), lines, outline='#0a0618', top=580)


if __name__ == '__main__':
    open(os.path.join(HERE, 'A.html'), 'w').write(make()); print('ok')
