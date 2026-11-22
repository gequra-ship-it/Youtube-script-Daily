# Shared helpers for the kola-superdeep-borehole-short1..5 Shorts thumbnails (style B, guideline 16-9).
# Reuses frog / hard hat / plankton / jag helpers from the long-form thumbnails (videos/kola-superdeep-borehole/thumb/make.py)
# without running that file's A-C writer. Each videos/kola-superdeep-borehole-shortN/thumb/make.py imports this and writes A.html.
import os, sys, math, random, shutil
_HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(_HERE, '..', '..', '..'))
sys.path.insert(0, os.path.join(REPO, 'tools'))
_LF = os.path.join(REPO, 'videos', 'kola-superdeep-borehole', 'thumb', 'make.py')
_src = open(_LF).read(); _src = _src[:_src.index("for n, fn in (('A', thumb_A)")]
_NS = {'__file__': _LF}; exec(compile(_src, _LF, 'exec'), _NS)
frog, hardhat, jag, P, mix, lina = _NS['frog'], _NS['hardhat'], _NS['jag'], _NS['P'], _NS['mix'], _NS['lina']
radiolarian, foram, diatom = _NS['radiolarian'], _NS['foram'], _NS['diatom']
INK, GREEN = _NS['INK'], _NS['GREEN']
FILTERS = _NS['FILTERS'] + '<filter id="b6" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="6"/></filter>' \
          '<filter id="b12" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="12"/></filter>' \
          '<filter id="b24" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="24"/></filter>'
from thumb_lib import vpage, vsvg, lin, rad, spark, fireflies, halo, darkband

W, H = 1080, 1920


def vig(id='vig', a=.75):
    return rad(id, 540, 900, 1250, [(0, '#000', 0), (.52, '#000', 0), (1, '#000', a)])


def stars(rnd, n, y0=0, y1=H, col='#e8f0ff', big=6):
    o = ''.join(f'<circle cx="{rnd.uniform(0, W):.0f}" cy="{rnd.uniform(y0, y1):.0f}" r="{rnd.choice([1.1, 1.6, 2.2])}" fill="{col}" opacity="{rnd.uniform(.25, .9):.2f}"/>' for _ in range(n))
    for _ in range(big):
        x, y = rnd.uniform(30, W - 30), rnd.uniform(y0 + 20, y1 - 20)
        o += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="9" fill="{col}" opacity=".25" filter="url(#b6)"/>' + spark(x, y, rnd.choice([10, 14, 18]), col='#f4f8ff', op=.8)
    return o


def aurora(x0s, y=120, h=300, col='#5cf2b0', id='aur'):
    """green aurora curtains in the night sky (defs must contain lina(id,...))"""
    o = ''
    for k, (x0, amp, op) in enumerate(x0s):
        d = f'M{x0} {y} C {x0 + 150} {y + amp}, {x0 + 230} {y - 60}, {x0 + 400} {y + 10} L {x0 + 400} {y + h} C {x0 + 230} {y + h - 80}, {x0 + 150} {y + h + amp}, {x0} {y + h - 30} Z'
        o += f'<path d="{d}" fill="url(#{id})" opacity="{op}" filter="url(#b14)"/>'
        for j in range(12):
            xx = x0 + 24 + j * 30
            o += f'<path d="M{xx} {y + 30 + 26 * math.sin(j * .7 + k):.0f} v{h * .6 + 40 * math.sin(j * 1.3):.0f}" stroke="#a8ffd8" stroke-width="3" opacity="{op * .35:.2f}" filter="url(#b2)"/>'
    return o


def sparkles(lst, col='#fff6d6'):
    return ''.join(spark(x, y, s, col) for x, y, s in lst)


def crystals(rnd, n, x0, y0, x1, y1, cols, smin=4, smax=13, o0=.15, o1=.45, skip=None):
    o = ''
    for _ in range(n):
        x = rnd.uniform(x0, x1); y = rnd.uniform(y0, y1)
        if skip and skip(x, y): continue
        s = rnd.uniform(smin, smax)
        o += f'<path d="M{x:.0f} {y:.0f} l{s:.1f} {-s * .5:.1f} l{s * .5:.1f} {s:.1f} l{-s:.1f} {s * .3:.1f}z" fill="{rnd.choice(cols)}" opacity="{rnd.uniform(o0, o1):.2f}"/>'
    return o


# frog outfits (frog() local coords: brim of a hat at y ~ -94, body -70..0)
PARKA = ('<path d="M-38 2 q-6 -22 2 -30 q40 -8 78 0 q10 10 2 30 q-42 10 -82 0z" fill="#d2452e" stroke-width="3.6"/>'
         '<path d="M-34 -26 q40 -10 78 0" fill="none" stroke="#f4ece0" stroke-width="7"/>'
         '<path d="M4 -24 v24" stroke-width="2.6"/>'
         '<path d="M-32 -6 q36 8 72 0" fill="none" stroke="#f4ece0" stroke-width="5"/>')
FLAPS = '<path d="M-44 -78 q-6 30 2 46 q12 2 14 -8 l-2 -40z M56 -78 q6 30 -2 46 q-12 2 -14 -8 l2 -40z" fill="#8a5a3a" stroke-width="3.2"/>'
USHANKA = ('<path d="M-32 -96 q4 -38 38 -40 q34 2 38 40z" fill="#8a5a3a" stroke-width="3.6"/>'
           '<rect x="-44" y="-104" width="100" height="22" rx="11" fill="#c49a74" stroke-width="3.4"/>'
           '<path d="M-36 -98 q8 -4 14 0 M-12 -98 q8 -4 14 0 M12 -98 q8 -4 14 0 M36 -98 q8 -4 14 0" fill="none" stroke="#e9d2b4" stroke-width="2.6"/>'
           '<circle cx="6" cy="-120" r="6" fill="#f2d27a" stroke-width="2.4"/>')
OVERALLS = ('<path d="M-36 2 q-4 -22 4 -28 h66 q8 6 4 28 q-38 8 -74 0z" fill="#3c6fb4" stroke-width="3.6"/>'
            '<path d="M-26 -26 l6 -18 M30 -26 l-6 -18" stroke="#3c6fb4" stroke-width="6"/>'
            '<circle cx="-20" cy="-22" r="3" fill="#f2d27a" stroke-width="1.6"/><circle cx="24" cy="-22" r="3" fill="#f2d27a" stroke-width="1.6"/>'
            '<rect x="-6" y="-16" width="20" height="12" rx="2" fill="#2e5a96" stroke-width="2.2"/>')
LABCOAT = ('<path d="M-38 2 q-6 -22 2 -30 q12 -4 30 -4 l8 18 l8 -18 q18 0 32 4 q10 10 2 30 q-42 10 -82 0z" fill="#f2f4f6" stroke-width="3.6"/>'
           '<path d="M2 -16 v16" stroke-width="2.4"/>'
           '<rect x="16" y="-18" width="14" height="10" rx="2" fill="#dfe4ea" stroke-width="2"/><path d="M20 -22 v6" stroke="#2a6ad0" stroke-width="2.4"/>')
GOGGLES = ('<path d="M-30 -86 q36 -16 72 0" fill="none" stroke="#3a3f4c" stroke-width="6"/>'
           '<circle cx="-10" cy="-90" r="9" fill="#bfe6ff" stroke-width="3"/><circle cx="22" cy="-90" r="9" fill="#bfe6ff" stroke-width="3"/>')


def write(here, bg, defs, body, lines, outline='#050b18', top=870):
    for f in ('common.css', 'Fredoka-700.woff2'):
        shutil.copy(os.path.join(REPO, 'tools', 'assets', 'thumb_v', f), here)
    open(os.path.join(here, 'A.html'), 'w').write(vpage(bg, vsvg(defs, body), lines, outline=outline, top=top))
    print('wrote', os.path.join(here, 'A.html'))
