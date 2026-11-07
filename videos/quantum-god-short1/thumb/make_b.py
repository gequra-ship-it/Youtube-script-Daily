# STYLE B shorts thumbnails for quantum-god-short1..5 (guideline 16-9 B, miya 2026-11-07): reuses make.py scenes, light tint,
# adds halo + fireflies + dark band behind the hook, redraws the scene frog last (pupils clamped inside the eye white).
# Hooks (script words): 1 BOTH SLITS AT ONCE?  2 SPOOKY ACTION AT A DISTANCE  3 NOTHING IS NEVER NOTHING  4 MANY WORLDS  5 IT FROM BIT?
# run: python3 videos/quantum-god-short1/thumb/make_b.py ; then SLUG=quantum-god-shortN python3 tools/thumb_shot.py
import os, sys, math, shutil
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, '../../..')); sys.path.insert(0, os.path.join(REPO, 'tools'))
import thumb_lib
from thumb_lib import rad, halo, darkband, fireflies
src = open(os.path.join(HERE, 'make.py')).read(); src = src[:src.index("if __name__ == '__main__':")]
for a, b in (("[('WAS', 160, 'w'), ('EINSTEIN', 176, 'w'), ('WRONG?', 220, 'y')]", "[('SPOOKY', 220, 'y'), ('ACTION', 200, 'w'), ('AT A DISTANCE', 112, 'w')]"),
             ("[('MORE THAN', 150, 'w'), ('ONE', 250, 'y'), ('REALITY?', 172, 'w')]", "[('MANY', 280, 'y'), ('WORLDS', 200, 'w')]")):
    assert a in src, a
    src = src.replace(a, b)
NS = {'__file__': os.path.join(HERE, 'make.py'), '__name__': 'mk'}
FROGS = []


def clamp(look, lim=5.0):   # eye white r13 (inner ~11.4), pupil r5, offset = look: keep hypot <= lim (max 6.4)
    h = math.hypot(*look)
    if h <= lim: return look
    k = lim / h
    return (look[0] * k, look[1] * k)


def run(n, tint, ta, halo_c, ff, band):
    ns = dict(NS); exec(compile(src, 'make.py', 'exec'), ns)
    fr = ns['frog']; FROGS.clear()

    def frog_defer(*a, **kw):
        kw['look'] = clamp(kw.get('look', (2, 0))); FROGS.append((a, kw)); return ''
    ns['frog'] = frog_defer

    def vsvg(defs, body):
        hx, hy, hr = halo_c[0]
        defs += halo('hB', hx, hy, hr, inner=halo_c[1], outer=halo_c[2])
        defs += rad('vB', 540, 960, 1250, [(0, '#000', 0), (.6, '#000', 0), (1, '#05060a', .6)])
        o = body
        o += f'<rect width="1080" height="1920" fill="{tint}" opacity="{ta}"/>'
        o += f'<ellipse cx="{hx}" cy="{hy}" rx="{hr}" ry="{hr}" fill="url(#hB)" opacity=".85"/>'
        o += darkband(band[0], band[1], band[2]) + fireflies(30, 120, 1850, col=ff[0], core=ff[1], seed=n)
        for a, kw in FROGS: o += fr(*a, **kw)
        o += '<rect width="1080" height="1920" fill="url(#vB)"/>'
        return thumb_lib.vsvg(defs, o)
    ns['vsvg'] = vsvg
    return ns['t%d' % n]()


# n: tint, tint opacity, [(halo cx,cy,r), inner, outer], fireflies (col, core), band (y0, y1, a)
C = {1: ('#040a1c', .25, [(540, 420, 520), '#e8fbff', '#2fd2ff'], ('#bff6ff', '#fff'), (780, 1420, .5)),
     2: ('#03161c', .25, [(540, 420, 520), '#fff3cf', '#ffd36a'], ('#ffe9a8', '#fff6e0'), (780, 1420, .5)),
     3: ('#0a0610', .25, [(540, 450, 500), '#fff3cf', '#ff9b3d'], ('#ffd9a8', '#fff6e0'), (760, 1420, .5)),
     4: ('#041218', .25, [(540, 420, 520), '#fff3cf', '#ffd36a'], ('#ffe9a8', '#fff6e0'), (780, 1420, .5)),
     5: ('#030818', .25, [(540, 420, 520), '#e8fbff', '#5ff2ff'], ('#bff6ff', '#fff'), (780, 1420, .5))}
if __name__ == '__main__':
    for n in map(int, sys.argv[1:] or '12345'):
        html = run(n, *C[n])
        out = os.path.join(REPO, 'videos', f'quantum-god-short{n}', 'thumb'); os.makedirs(out, exist_ok=True)
        for f in ('common.css', 'Fredoka-700.woff2'): shutil.copy(os.path.join(REPO, 'tools/assets/thumb_v', f), out)
        open(os.path.join(out, 'A.html'), 'w').write(html); print('short', n, 'ok')
