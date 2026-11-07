# STYLE B shorts thumbnails for hollow-skyscraper-short1..5 (guideline 16-9 B, miya 2026-11-07): reuses make.py scenes, darkens them (tint),
# adds halo + fireflies + dark band behind the hook, redraws the scene frog last (pupils clamped inside the eye white).
# Hooks = script words (existing): 1 NATURE'S HOLLOW TRICK  2 CONCRETE ROOTS  3 A STABLE TRIPOD  4 IT WON'T TUMBLE  5 FIRST TEST: FAILED
# run: python3 videos/hollow-skyscraper-short1/thumb/make_b.py ; then SLUG=hollow-skyscraper-shortN python3 tools/thumb_shot.py
import os, sys, math, shutil
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, '../../..')); sys.path.insert(0, os.path.join(REPO, 'tools'))
import thumb_lib
from thumb_lib import rad, halo, darkband, fireflies
src = open(os.path.join(HERE, 'make.py')).read(); src = src[:src.index("if __name__ == '__main__':")]
NS = {'__file__': os.path.join(HERE, 'make.py'), '__name__': 'mk'}
FROGS = []
def clamp(look, lim=5.0):   # eye white r13 (inner ~11.4), pupil r5.4, offset = (2+lx, ly): keep hypot <= lim (limit 6.0)
    lx, ly = look; dx = 2 + lx; h = math.hypot(dx, ly)
    if h <= lim: return look
    k = lim / h; return (dx * k - 2, ly * k)
def run(n, tint, ta, halo_c, ff, band):
    ns = dict(NS); exec(compile(src, 'make.py', 'exec'), ns)
    fr = ns['frog']; FROGS.clear()
    def frog_defer(*a, **kw):
        kw['look'] = clamp(kw.get('look', (0, 0))); FROGS.append((a, kw)); return ''
    ns['frog'] = frog_defer
    def vsvg(defs, body):
        hx, hy, hr = halo_c[0]
        defs += halo('hB', hx, hy, hr, inner=halo_c[1], outer=halo_c[2])
        defs += rad('vB', 540, 960, 1250, [(0, '#000', 0), (.6, '#000', 0), (1, '#05060a', .6)])
        defs += '<filter id="b6" x="-200%" y="-200%" width="500%" height="500%"><feGaussianBlur stdDeviation="6"/></filter><filter id="b50" x="-20%" y="-100%" width="140%" height="300%"><feGaussianBlur stdDeviation="50"/></filter>'
        o = body
        o += f'<rect width="1080" height="1920" fill="{tint}" opacity="{ta}"/>'
        o += f'<ellipse cx="{hx}" cy="{hy}" rx="{hr}" ry="{hr}" fill="url(#hB)" opacity=".85"/>'
        o += darkband(band[0], band[1], band[2]) + fireflies(30, 120, 1850, col=ff[0], core=ff[1], seed=n)
        for a, kw in FROGS: o += fr(*a, **kw)
        o += '<rect width="1080" height="1920" fill="url(#vB)"/>'
        return thumb_lib.vsvg(defs, o)
    ns['vsvg'] = vsvg
    return ns['s%d' % n]()
# n: tint, tint opacity, [(halo cx,cy,r), inner, outer], fireflies (col, core), band (y0, y1, a)
C = {1: ('#06140a', .5, [(540, 520, 520), '#fff3cf', '#7fe08a'], ('#d8ffb8', '#fff'), (900, 1300, .5)),
     2: ('#120a04', .5, [(540, 800, 520), '#fff3cf', '#ffb060'], ('#ffe9a8', '#fff6e0'), (900, 1300, .5)),
     3: ('#10100a', .5, [(540, 560, 500), '#fff3cf', '#ffd070'], ('#ffe9a8', '#fff6e0'), (900, 1300, .5)),
     4: ('#06142a', .5, [(540, 600, 520), '#e8f4ff', '#7fb8ff'], ('#cfeaff', '#fff'), (900, 1300, .5)),
     5: ('#02060c', .4, [(540, 560, 520), '#e8fbff', '#7fd6e6'], ('#bff6ff', '#fff'), (900, 1300, .5))}
if __name__ == '__main__':
    for n in map(int, sys.argv[1:] or '12345'):
        html = run(n, *C[n])
        out = os.path.join(REPO, 'videos', f'hollow-skyscraper-short{n}', 'thumb'); os.makedirs(out, exist_ok=True)
        for f in ('common.css', 'Fredoka-700.woff2'): shutil.copy(os.path.join(REPO, 'tools/assets/thumb_v', f), out)
        open(os.path.join(out, 'A.html'), 'w').write(html); print('short', n, 'ok')
