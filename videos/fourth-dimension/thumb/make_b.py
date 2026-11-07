# STYLE B shorts thumbnails for fourth-dimension-short1..5 (guideline 16-9 B, miya 2026-11-07): reuses make_shorts.py scenes, darkens them,
# adds halo + fireflies + dark band behind the hook, redraws the scene frog last (pupils clamped inside the eye white).
# Hooks from short scripts, no numbers: 1 A 4D SHADOW?  2 THEY SEE A CIRCLE  3 HUNDREDS OF FLAT SLICES  4 STACK EVERY PHOTO  5 BUILT FOR 3D ONLY
# run: python3 videos/fourth-dimension/thumb/make_b.py ; then SLUG=fourth-dimension-shortN python3 tools/thumb_shot.py
import os, sys, math, shutil
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, '../../..')); sys.path.insert(0, os.path.join(REPO, 'tools'))
import thumb_lib
from thumb_lib import rad, halo, darkband, fireflies
src = open(os.path.join(HERE, 'make_shorts.py')).read(); src = src[:src.index('for n, fn in enumerate(')]
NS = {'__file__': os.path.join(HERE, 'make_shorts.py')}
FROGS = []
def clamp(look, lim=5.0):   # eye white r13.5, pupil r4.4, offset = (1+lx, ly): keep hypot <= lim
    lx, ly = look; dx = 1 + lx; h = math.hypot(dx, ly)
    if h <= lim: return look
    k = lim / h; return (dx * k - 1, ly * k)
def run(n, tint, ta, halo_c, ff, band, hook_top, hook_lines=None):
    ns = dict(NS); exec(compile(src, 'make_shorts.py', 'exec'), ns)
    fr = ns['frog']; FROGS.clear()
    def frog_defer(*a, **kw):
        kw['look'] = clamp(kw.get('look', (0, 0))); FROGS.append((a, kw)); return ''
    ns['frog'] = frog_defer
    cap = {}
    def vsvg(defs, body):
        hx, hy, hr = halo_c[0]
        defs += halo('hB', hx, hy, hr, inner=halo_c[1], outer=halo_c[2])
        defs += rad('vB', 540, 960, 1250, [(0, '#000', 0), (.6, '#000', 0), (1, '#05060a', .6)])
        o = body
        if ta: o += f'<rect width="1080" height="1920" fill="{tint}" opacity="{ta}"/>'
        o += f'<ellipse cx="{hx}" cy="{hy}" rx="{hr}" ry="{hr}" fill="url(#hB)" opacity=".85"/>'
        o += darkband(band[0], band[1], band[2]) + fireflies(30, 120, 1850, col=ff[0], core=ff[1], seed=n)
        for a, kw in FROGS: o += fr(*a, **kw)
        o += '<rect width="1080" height="1920" fill="url(#vB)"/>'
        return thumb_lib.vsvg(defs, o)
    def vpage(bg, svg, lines, outline='#050b18', top=700):
        return thumb_lib.vpage(bg, svg, hook_lines or lines, outline=outline, top=hook_top or top)
    ns['vsvg'] = vsvg; ns['vpage'] = vpage
    return ns['make_%d' % n]()
# n: tint, tint opacity, [(halo cx,cy,r), inner, outer], fireflies (col, core), band (y0, y1, a), hook top override
C = {1: ('#1a0f3a', 0, [(540, 560, 560), '#fff3cf', '#b07aff'], ('#e8d0ff', '#fff'), (880, 1250, .5), None),
     2: ('#0a1838', .4, [(600, 1380, 600), '#fff3cf', '#ffa060'], ('#ffe9a8', '#fff6e0'), (610, 880, .5), None),
     3: ('#04202c', .3, [(540, 520, 520), '#e8fff4', '#7ff5d8'], ('#a8ffe0', '#fff'), (940, 1330, .5), None),
     4: ('#0a0a2a', .1, [(700, 900, 520), '#fff3cf', '#ff9ad0'], ('#ffd27a', '#fff6e0'), (690, 1130, .5), None),
     5: ('#1a0a24', .28, [(540, 640, 600), '#fff3cf', '#ffa850'], ('#ffd27a', '#fff6e0'), (870, 1130, .5), None)}
if __name__ == '__main__':
    for n in map(int, sys.argv[1:] or '12345'):
        tint, ta, hc, ff, band, ht = C[n]
        html = run(n, tint, ta, hc, ff, band, ht)
        out = os.path.join(REPO, 'videos', f'fourth-dimension-short{n}', 'thumb'); os.makedirs(out, exist_ok=True)
        for f in ('common.css', 'Fredoka-700.woff2'): shutil.copy(os.path.join(REPO, 'tools/assets/thumb_v', f), out)
        open(os.path.join(out, 'A.html'), 'w').write(html); print('short', n, 'ok')
