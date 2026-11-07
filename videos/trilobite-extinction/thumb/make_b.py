# STYLE B shorts thumbnails for trilobite-extinction (guideline 16-9 B, miya 2026-11-07): reuses make_shorts.py pictures (subject top half, frog bottom),
# adds halo + fireflies + darkband, 2-line hook on band y 880-1250, frog pupils clamped inside the eye white. Hooks only from the short scripts, no numbers.
#   python3 videos/trilobite-extinction/thumb/make_b.py -> videos/trilobite-extinction-short{1..5}/thumb/A.html ; then SLUG=trilobite-extinction-shortN python3 tools/thumb_shot.py
# short1 EYES MADE / OF ROCK  short2 LONGER THAN / DINOSAURS  short3 A BALL / OF ARMOR  short4 OCEAN TOO / ACIDIC  short5 ONLY ONE / SURVIVED
import os, sys, math, shutil
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import make_shorts as M
from thumb_lib import fireflies, darkband, halo
REPO = os.path.abspath(os.path.join(HERE, '../../..'))
_frog = M.frog
def frog(x, y, s, look=(0, 0), **kw):
    dx, dy = look; m = math.hypot(dx, dy)
    if m > 5.4: dx, dy = dx * 5.4 / m, dy * 5.4 / m
    return _frog(x, y, s, look=(dx, dy), **kw)
M.frog = frog
_vpage = M.vpage
HOOK = {1: [('EYES MADE', 165, 'w'), ('OF ROCK', 215, 'y')], 2: [('LONGER THAN', 138, 'w'), ('DINOSAURS', 160, 'y')],
        3: [('A BALL', 200, 'w'), ('OF ARMOR', 190, 'y')], 4: [('OCEAN TOO', 165, 'w'), ('ACIDIC', 220, 'y')], 5: [('ONLY ONE', 190, 'w'), ('SURVIVED', 175, 'y')]}
HALO = {1: ('#fff3cf', '#c89aff', 540, 480), 2: ('#ffffff', '#9ad8ff', 540, 450), 3: ('#fff3cf', '#7ff5d8', 540, 450),
        4: ('#fff3cf', '#ff7a50', 540, 450), 5: ('#fff3cf', '#ffc060', 830, 560)}
FF = {1: ('#d8c8ff', '#fff'), 2: ('#fffbe0', '#fff'), 3: ('#a8ffe0', '#fff'), 4: ('#ffb080', '#fff3e0'), 5: ('#ffd27a', '#fff6e0')}
cur = [0]
def vpage(bg, svg, lines, outline='#050b18', top=700):
    n = cur[0]; hi, ho, hx, hy = HALO[n]
    svg = svg.replace('</defs>', halo('hb', hx, hy, 560, inner=hi, outer=ho) + '</defs>', 1)
    k = svg.index('</defs>') + 7
    i = svg.index('/>', k) + 2   # after the first drawn element (background)
    if not svg[k:i].lstrip().startswith(('<rect', '<path')): i = k
    svg = svg[:i] + f'<ellipse cx="{hx}" cy="{hy}" rx="560" ry="560" fill="url(#hb)" opacity=".5"/>' + svg[i:]
    add = darkband(860, 1250, .5) + fireflies(36, 120, 1800, col=FF[n][0], core=FF[n][1], seed=n)
    j = svg.rindex('</svg>'); svg = svg[:j] + add + svg[j:]
    h = _vpage(bg, svg, HOOK[n], outline=outline, top=880)
    if n == 5:   # SURVIVED: V-I-V merged at 3px tracking, open it up
        h = h.replace('#t1{left:0;width:1080px;text-align:center;', '#t1{left:0;width:1080px;text-align:center;word-spacing:0;', 1)
        h = h.replace('font-size:175px;letter-spacing:3px', 'font-size:175px;letter-spacing:12px', 1)
    return h
M.vpage = vpage
for n in range(1, 6):
    cur[0] = n
    d = os.path.join(REPO, 'videos', f'trilobite-extinction-short{n}', 'thumb'); os.makedirs(d, exist_ok=True)
    for f in ('common.css', 'Fredoka-700.woff2'):
        shutil.copy(os.path.join(REPO, 'tools/assets/thumb_v', f), d)
    open(os.path.join(d, 'A.html'), 'w').write(getattr(M, f'make_{n}')())
print('ok')
