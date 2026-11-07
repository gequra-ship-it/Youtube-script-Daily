# STYLE B shorts thumbnails for holographic-universe-short1..5 (guideline 16-9 B, miya 2026-11-07): reuses make_shorts.py scenes, darkens them,
# adds halo + fireflies + dark band behind the hook, redraws the scene frog last (pupils clamped inside the eye white).
# Hooks use script words only, no numbers: 1 FLAT, YET DEEP  2 LOST FOREVER?  3 ONLY THE OUTER SKIN  4 TWO BOOKS, SAME STORY  5 FABRIC OF SPACE?
# run: python3 videos/holographic-universe-short1/thumb/make_b.py ; then SLUG=holographic-universe-shortN python3 tools/thumb_shot.py
import os, sys, math, shutil
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, '../../..')); sys.path.insert(0, os.path.join(REPO, 'tools'))
import thumb_lib
from thumb_lib import rad, halo, darkband, fireflies
src = open(os.path.join(HERE, 'make_shorts.py')).read(); src = src[:src.index("if __name__ == '__main__'")]
NS = {'__file__': os.path.join(HERE, 'make_shorts.py')}
FROGS = []
HOP = {2: .3, 3: .4}   # halo opacity overrides: keep the black hole black / the house colours
def clamp(look, lim=5.0):   # eye white r13.5, pupil r4.4, offset = (1+lx, ly): keep hypot <= lim
    lx, ly = look; dx = 1 + lx; h = math.hypot(dx, ly)
    if h <= lim: return look
    k = lim / h; return (dx * k - 1, ly * k)
def run(n, tint, ta, halo_c, ff, band, hook_lines=None, hook_top=None):
    ns = dict(NS); exec(compile(src, 'make_shorts.py', 'exec'), ns)
    fr = ns['frog']; FROGS.clear()
    def frog_defer(*a, **kw):
        kw['look'] = clamp(kw.get('look', (0, 0))); FROGS.append((a, kw)); return ''
    ns['frog'] = frog_defer
    def vsvg(defs, body):
        hx, hy, hr = halo_c[0]
        defs += halo('hB', hx, hy, hr, inner=halo_c[1], outer=halo_c[2])
        defs += rad('vB', 540, 960, 1250, [(0, '#000', 0), (.6, '#000', 0), (1, '#05060a', .6)])
        o = body
        if ta: o += f'<rect width="1080" height="1920" fill="{tint}" opacity="{ta}"/>'
        o += f'<ellipse cx="{hx}" cy="{hy}" rx="{hr}" ry="{hr}" fill="url(#hB)" opacity="{HOP.get(n, .85)}"/>'
        o += darkband(band[0], band[1], band[2]) + fireflies(30, 120, 1850, col=ff[0], core=ff[1], seed=n)
        for a, kw in FROGS: o += fr(*a, **kw)
        o += '<rect width="1080" height="1920" fill="url(#vB)"/>'
        return thumb_lib.vsvg(defs, o)
    def vpage(bg, svg, lines, outline='#050b18', top=700):
        return thumb_lib.vpage(bg, svg, hook_lines or lines, outline=outline, top=hook_top or top)
    ns['vsvg'] = vsvg; ns['vpage'] = vpage
    return ns['make_%d' % n]()
# n: tint, tint opacity, [(halo cx,cy,r), inner, outer], fireflies (col, core), band (y0, y1, a), hook lines, hook top
C = {1: ('#10082a', .25, [(720, 1300, 520), '#f4e8ff', '#9a6aff'], ('#e8d0ff', '#fff'), (600, 1120, .5), None, None),
     2: ('#0a0818', .15, [(555, 500, 480), '#fff3cf', '#ff8a40'], ('#ffd9a0', '#fff6e0'), (880, 1250, .5), None, None),
     3: ('#0a1030', .3, [(540, 1330, 520), '#fff3cf', '#ffb060'], ('#ffe9a8', '#fff6e0'), (440, 940, .5),
         [('ONLY THE', 146, 'w'), ('OUTER', 150, 'w'), ('SKIN', 222, 'y')], None),
     4: ('#04201c', .3, [(510, 430, 420), '#fff3cf', '#ffa850'], ('#ffd27a', '#fff6e0'), (890, 1390, .5), None, None),
     5: ('#120a2e', .2, [(540, 1420, 480), '#e8fbff', '#6ab0ff'], ('#b8d8ff', '#fff'), (650, 1050, .5),
         [('FABRIC OF', 150, 'w'), ('SPACE?', 214, 'y')], None)}
if __name__ == '__main__':
    for n in map(int, sys.argv[1:] or '12345'):
        tint, ta, hc, ff, band, hl, ht = C[n]
        html = run(n, tint, ta, hc, ff, band, hl, ht)
        out = os.path.join(REPO, 'videos', f'holographic-universe-short{n}', 'thumb'); os.makedirs(out, exist_ok=True)
        for f in ('common.css', 'Fredoka-700.woff2'): shutil.copy(os.path.join(REPO, 'tools/assets/thumb_v', f), out)
        open(os.path.join(out, 'A.html'), 'w').write(html); print('short', n, 'ok')
