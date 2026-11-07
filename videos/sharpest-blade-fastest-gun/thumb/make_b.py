# STYLE B shorts thumbnails for sharpest-blade-fastest-gun-short1..5 (guideline 16-9 B, miya 2026-11-07): reuses make_shorts.py scenes,
# adds vignette + halo behind the focal object + fireflies + dark band behind the hook; scene frog pupils clamped inside the eye white.
# Hooks are the existing script-word hooks: 1 SHARPNESS IS AN ILLUSION  2 2,000 SLICES = ONE HAIR  3 IT ENDS IN ONE ATOM  4 A FLECK OF PAINT VS. A WINDOW  5 99.9999991% OF LIGHT SPEED
# run: python3 videos/sharpest-blade-fastest-gun/thumb/make_b.py ; then SLUG=sharpest-blade-fastest-gun-shortN python3 tools/thumb_shot.py
import os, sys, math, shutil, importlib.util
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, '../../..')); sys.path.insert(0, os.path.join(REPO, 'tools'))
import thumb_lib
from thumb_lib import rad, halo, darkband, fireflies
spec = importlib.util.spec_from_file_location('ms', os.path.join(HERE, 'make_shorts.py')); ms = importlib.util.module_from_spec(spec); spec.loader.exec_module(ms)
F = '<filter id="b6" x="-200%" y="-200%" width="500%" height="500%"><feGaussianBlur stdDeviation="6"/></filter><filter id="b50" x="-20%" y="-100%" width="140%" height="300%"><feGaussianBlur stdDeviation="50"/></filter>'
orig_frog = ms.frog
def clamp(look, lim=5.0):   # eye white r13 (inner ~11.4), pupil r5.4, offset = (2+lx, ly): keep hypot <= lim (limit 6.0)
    lx, ly = look; dx = 2 + lx; h = math.hypot(dx, ly)
    if h <= lim: return look
    k = lim / h; return (dx * k - 2, ly * k)
def frog_c(*a, **kw):
    kw['look'] = clamp(kw.get('look', (0, 0))); return orig_frog(*a, **kw)
ms.frog = frog_c
def run(n, hc, ff, band):
    def vsvg(defs, body):
        hx, hy, hr = hc[0]
        defs += F + halo('hB', hx, hy, hr, inner=hc[1], outer=hc[2]) + rad('vB', 540, 960, 1250, [(0, '#000', 0), (.6, '#000', 0), (1, '#05060a', .65)])
        o = f'<ellipse cx="{hx}" cy="{hy}" rx="{hr}" ry="{hr}" fill="url(#hB)" opacity=".5"/>' + body
        o += darkband(band[0], band[1], band[2]) + fireflies(28, 120, 1850, col=ff[0], core=ff[1], seed=n)
        o += '<rect width="1080" height="1920" fill="url(#vB)"/>'
        return thumb_lib.vsvg(defs, o)
    ms.vsvg = vsvg
    return getattr(ms, 'make_%d' % n)()
# n: [(halo cx,cy,r), inner, outer], fireflies (col, core), band (y0, y1, a)
C = {1: ([(560, 1420, 420), '#fff3cf', '#7fc8ff'], ('#cfeaff', '#fff'), (690, 1090, .5)),
     2: ([(870, 1400, 420), '#e6fbff', '#5ad2e8'], ('#bff6ff', '#fff'), (650, 1030, .5)),
     3: ([(700, 1290, 380), '#e8fff4', '#7ff5d8'], ('#bff6ff', '#fff'), (680, 1020, .5)),
     4: ([(660, 1310, 420), '#fff3cf', '#ffb060'], ('#ffe9a8', '#fff6e0'), (590, 1010, .5)),
     5: ([(540, 1630, 520), '#fff3cf', '#6ab4ff'], ('#bff6ff', '#fff'), (710, 1090, .5))}
if __name__ == '__main__':
    for n in map(int, sys.argv[1:] or '12345'):
        html = run(n, *C[n])
        out = os.path.join(REPO, 'videos', f'sharpest-blade-fastest-gun-short{n}', 'thumb'); os.makedirs(out, exist_ok=True)
        for f in ('common.css', 'Fredoka-700.woff2'): shutil.copy(os.path.join(REPO, 'tools/assets/thumb_v', f), out)
        open(os.path.join(out, 'A.html'), 'w').write(html); print('short', n, 'ok')
