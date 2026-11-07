# STYLE B shorts thumbnails for space-nuke-short1..5 (guideline 16-9 B, miya 2026-11-07): reuses make_v.py scenes, light tint,
# halo + fireflies + dark band behind the hook, scene frog redrawn last (pupils clamped inside the eye white; porthole frog in short3 stays in place).
# Hooks (script words): 1 ABSOLUTE SILENCE  2 NO MUSHROOM CLOUD  3 INVISIBLE ATTACK  4 STARFISH PRIME  5 MAN-MADE RADIATION BELT
# run: python3 videos/space-nuke-short1/thumb/make_b.py ; then SLUG=space-nuke-shortN python3 tools/thumb_shot.py
import os, sys, math, shutil
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, '../../..')); sys.path.insert(0, os.path.join(REPO, 'tools'))
import thumb_lib
from thumb_lib import rad, halo, darkband, fireflies
src = open(os.path.join(HERE, 'make_v.py')).read(); src = src[:src.index("for n, fn in ((1, make_1)")]
a_ = "translate(0 64) rotate(-12 6 -66)"; assert a_ in src
src = src.replace(a_, "translate(0 30) rotate(-12 6 -66)")   # binoculars at chest level, hands on the barrels (not below the belly)
NS = {'__file__': os.path.join(HERE, 'make_v.py'), '__name__': 'mk'}
FROGS = []
HOOK = {1: ([('ABSOLUTE', 160, 'w'), ('SILENCE', 230, 'y')], 800),
        2: ([('NO', 210, 'y'), ('MUSHROOM', 150, 'w'), ('CLOUD', 200, 'w')], 770),
        3: ([('INVISIBLE', 170, 'y'), ('ATTACK', 230, 'w')], 760),
        4: ([('STARFISH', 190, 'y'), ('PRIME', 240, 'w')], 760),
        5: ([('MAN-MADE', 170, 'w'), ('RADIATION', 160, 'y'), ('BELT', 230, 'w')], 650)}


def clamp(look, lim=5.0):   # eye white r13, pupil offset = (2+lx, ly): keep hypot <= lim
    lx, ly = look; dx = 2 + lx; h = math.hypot(dx, ly)
    if h <= lim: return look
    k = lim / h; return (dx * k - 2, ly * k)


def run(n, tint, ta, halo_c, ff, defer=True):
    ns = dict(NS); exec(compile(src, 'make_v.py', 'exec'), ns)
    fr = ns['frog']; FROGS.clear()
    def frog_w(*a, **kw):
        kw['look'] = clamp(kw.get('look', (0, 0)), 4.6 if kw.get('pupil', 5.4) > 5.4 else 5.0); kw['pupil'] = min(kw.get('pupil', 5.4), 5.4)
        if not defer: return fr(*a, **kw)
        FROGS.append((a, kw)); return ''
    ns['frog'] = frog_w
    lines, top = HOOK[n]
    ns['vpage'] = lambda bg, svg, _lines, top=0: thumb_lib.vpage(bg, svg, lines, top=top_)
    top_ = top
    band = (top - 40, top + int(sum(l[1] for l in lines) * .97) + 40, .5)
    def vsvg(defs, body):
        hx, hy, hr = halo_c[0]
        defs += halo('hB', hx, hy, hr, inner=halo_c[1], outer=halo_c[2])
        defs += rad('vB', 540, 960, 1250, [(0, '#000', 0), (.6, '#000', 0), (1, '#05060a', .6)])
        defs += '<filter id="b6" x="-200%" y="-200%" width="500%" height="500%"><feGaussianBlur stdDeviation="6"/></filter><filter id="b50" x="-20%" y="-100%" width="140%" height="300%"><feGaussianBlur stdDeviation="50"/></filter>'
        o = body
        o += f'<rect width="1080" height="1920" fill="{tint}" opacity="{ta}"/>'
        o += f'<ellipse cx="{hx}" cy="{hy}" rx="{hr}" ry="{hr}" fill="url(#hB)" opacity=".7"/>'
        o += darkband(*band) + fireflies(30, 120, 1850, col=ff[0], core=ff[1], seed=n)
        for a, kw in FROGS: o += fr(*a, **kw)
        o += '<rect width="1080" height="1920" fill="url(#vB)"/>'
        return thumb_lib.vsvg(defs, o)
    ns['vsvg'] = vsvg
    return ns['make_%d' % n]()
# n: tint, tint opacity, [(halo cx,cy,r), inner, outer], fireflies (col, core), defer frog?
C = {1: ('#040a1c', .2, [(540, 480, 520), '#e8fbff', '#5fb8ff'], ('#bff6ff', '#fff')),
     2: ('#120a04', .2, [(540, 480, 520), '#fff3cf', '#ffb060'], ('#ffe9a8', '#fff6e0')),
     3: ('#0a0610', .2, [(900, 360, 480), '#f4eaff', '#9a7cff'], ('#e2d6ff', '#fff')),
     4: ('#04101e', .2, [(600, 430, 520), '#e8f4ff', '#7fb8ff'], ('#cfeaff', '#fff')),
     5: ('#02060c', .2, [(540, 1440, 560), '#e8fbff', '#5fffd0'], ('#bff6ff', '#fff'))}
if __name__ == '__main__':
    for n in map(int, sys.argv[1:] or '12345'):
        html = run(n, *C[n], defer=(n != 3))
        out = os.path.join(REPO, 'videos', f'space-nuke-short{n}', 'thumb'); os.makedirs(out, exist_ok=True)
        for f in ('common.css', 'Fredoka-700.woff2'): shutil.copy(os.path.join(REPO, 'tools/assets/thumb_v', f), out)
        open(os.path.join(out, 'A.html'), 'w').write(html); print('short', n, 'ok')
