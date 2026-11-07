# STYLE B shorts thumbnails for neptune-mysteries-short1..5 (guideline 16-9 B, miya 2026-11-07): reuses each shortN/thumb/make.py scene (make() of that file),
# adds halo + fireflies + dark band behind the hook, redraws the scene frog last with pupils clamped inside the eye white.
# Hooks are the existing script-derived ones (no numbers): 1 WHY SO BLUE?  2 WEAKEST SUN/STRONGEST/WINDS  3 A HIDDEN FIRE?  4 DIAMOND HAIL INSIDE?  5 A MOON RIPPED APART
# run: python3 videos/neptune-mysteries/thumb/make_b.py [n..] ; then SLUG=neptune-mysteries-shortN python3 tools/thumb_shot.py
import os, sys, math, shutil
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, '../../..')); sys.path.insert(0, os.path.join(REPO, 'tools'))
import thumb_lib
from thumb_lib import rad, halo, darkband, fireflies
FROGS = []
def clamp(look, lim=5.4):   # this frog: eye white r13 (inner 11.4), pupil r5, offset = look: hypot(look)+5 <= 11.4 -> keep hypot <= 5.4
    m = math.hypot(*look)
    return look if m <= lim else (look[0] * lim / m, look[1] * lim / m)
# n: tint, tint opacity, (halo cx, cy, r), inner, outer, halo opacity, fireflies (col, core)
C = {1: ('#0a0a30', .1, (560, 520, 560), '#bfe0ff', '#3a6cff', .75, ('#bcd8ff', '#fff')),
     2: ('#030a2c', .1, (540, 480, 520), '#e8f6ff', '#4a8cff', .6, ('#cfe6ff', '#fff')),
     3: ('#05061c', .1, (540, 520, 520), '#fff0c0', '#ff6a30', .75, ('#ffc890', '#fff3e0')),
     4: ('#05162e', .1, (540, 520, 520), '#e8fbff', '#58c8ff', .6, ('#c8f0ff', '#fff')),
     5: ('#040516', .1, (540, 480, 520), '#fff3d8', '#ff8040', .6, ('#ffd9b0', '#fff6e8'))}
def run(n):
    tint, ta, (hx, hy, hr), hi, ho, hop, ff = C[n]
    path = os.path.join(REPO, 'videos', f'neptune-mysteries-short{n}', 'thumb', 'make.py')
    src = open(path).read(); src = src[:src.index("open(os.path.join(HERE, 'A.html')")]
    ns = {'__file__': path}; exec(compile(src, path, 'exec'), ns)
    fr = ns['frog']; FROGS.clear()
    def frog_defer(*a, **kw):
        kw['look'] = clamp(kw.get('look', (0, 0))); FROGS.append((a, kw)); return ''
    ns['frog'] = frog_defer
    box = {}
    def vpage(bg, svg, lines, outline='#050b18', top=700):
        box['l'] = (lines, top, outline); box['bg'] = bg; return ''
    ns['vpage'] = vpage
    def vsvg(defs, body):
        box['d'] = defs; box['b'] = body; return ''
    ns['vsvg'] = vsvg
    ns['make']()
    lines, top, outline = box['l']
    y1 = top + sum(int(s * .97) for _, s, _ in lines[:-1]) + lines[-1][1]
    defs = box['d'] + halo('hB', hx, hy, hr, inner=hi, outer=ho) + rad('vB', 540, 960, 1250, [(0, '#000', 0), (.6, '#000', 0), (1, '#05060a', .6)])
    o = box['b'] + f'<rect width="1080" height="1920" fill="{tint}" opacity="{ta}"/>'
    o += f'<ellipse cx="{hx}" cy="{hy}" rx="{hr}" ry="{hr}" fill="url(#hB)" opacity="{hop}"/>'
    o += darkband(top - 10, y1 + 10, .5) + fireflies(30, 120, 1850, col=ff[0], core=ff[1], seed=n)
    for a, kw in FROGS: o += fr(*a, **kw)
    o += '<rect width="1080" height="1920" fill="url(#vB)"/>'
    return thumb_lib.vpage(box['bg'], thumb_lib.vsvg(defs, o), lines, outline=outline, top=top)
if __name__ == '__main__':
    for n in map(int, sys.argv[1:] or '12345'):
        html = run(n)
        out = os.path.join(REPO, 'videos', f'neptune-mysteries-short{n}', 'thumb')
        for f in ('common.css', 'Fredoka-700.woff2'): shutil.copy(os.path.join(REPO, 'tools/assets/thumb_v', f), out)
        open(os.path.join(out, 'A.html'), 'w').write(html); print('short', n, 'ok')
