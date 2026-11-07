# STYLE B shorts thumbnails for deep-time-bedtime (guideline 16-9 B, miya 2026-11-07): reuses the shorts_kit pictures (concrete glowing subject in the top half),
# adds halo + fireflies + dark band, hook on band y 880-1250, frog pupils clamped inside the eye white. Hooks only from the short scripts, no numbers.
#   python3 videos/deep-time-bedtime/thumb/make_b.py -> videos/deep-time-bedtime-short{1..5}/thumb/A.html
# short1 BORN FROM / A CRASH?  (S1 hedged: "scientists ... a body the size of Mars collided ... Moon")  short2 SNOWBALL / EARTH?
# short3 LEAVING / THE WATER (Tiktaalik)  short4 THIS COAL / WAS A TREE  short5 THE SMALL / SURVIVED
import os, sys, math, shutil
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import shorts_kit as K
from thumb_lib import fireflies, darkband, halo
REPO = os.path.abspath(os.path.join(HERE, '../../..'))
_frog = K.frog
def frog(x, y, s, look=(0, 0), **kw):
    dx, dy = look; m = math.hypot(dx, dy)
    if m > 5.4: dx, dy = dx * 5.4 / m, dy * 5.4 / m
    return _frog(x, y, s, look=(dx, dy), **kw)
K.frog = frog
_vpage = K.vpage
HOOK = {1: [('BORN FROM', 170, 'w'), ('A CRASH?', 200, 'y')], 2: [('SNOWBALL', 190, 'y'), ('EARTH?', 230, 'w')],
        3: [('LEAVING', 200, 'y'), ('THE WATER', 160, 'w')], 4: [('THIS COAL', 170, 'w'), ('WAS A TREE', 145, 'y')], 5: [('THE SMALL', 190, 'w'), ('SURVIVED', 200, 'y')]}
HALO = {1: ('#fff3cf', '#ff9a50', 420, 480), 2: ('#e8f6ff', '#7fc8ff', 540, 470), 3: ('#fff3cf', '#7ff5d8', 540, 450), 4: ('#fff3cf', '#7ff5d8', 540, 430), 5: ('#fff3cf', '#ffb060', 540, 1080)}
FF = {1: ('#ffd27a', '#fff6e0'), 2: ('#e8f6ff', '#fff'), 3: ('#fff3a8', '#fffbd0'), 4: ('#a8ffe0', '#fff'), 5: ('#ffd27a', '#fff6e0')}
cur = [0]
def vpage(bg, svg, lines, outline='#050b18', top=700):
    n = cur[0]; hi, ho, hx, hy = HALO[n]
    d = halo('hb', hx, hy, 560, inner=hi, outer=ho)
    svg = svg.replace('</defs>', d + '</defs>', 1)
    i = svg.index('/>', svg.index('<rect width="1080" height="1920"')) + 2   # after the background rect
    svg = svg[:i] + f'<ellipse cx="{hx}" cy="{hy}" rx="560" ry="560" fill="url(#hb)" opacity=".6"/>' + svg[i:]
    # darkband + fireflies before the vignette/end
    add = darkband(860, 1250, .5) + fireflies(36, 120, 1800, col=FF[n][0], core=FF[n][1], seed=n)
    j = svg.rindex('</svg>'); svg = svg[:j] + add + svg[j:]
    return _vpage(bg, svg, HOOK[n], outline=outline, top=880)
K.vpage = vpage
for n in range(1, 6):
    cur[0] = n
    d = os.path.join(REPO, 'videos', f'deep-time-bedtime-short{n}', 'thumb'); os.makedirs(d, exist_ok=True)
    for f in ('common.css', 'Fredoka-700.woff2'):
        shutil.copy(os.path.join(REPO, 'tools/assets/thumb_v', f), d)
    open(os.path.join(d, 'A.html'), 'w').write(K.SHORTS[n]())
print('ok')
