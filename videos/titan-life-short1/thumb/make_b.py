# STYLE B shorts thumbnails for titan-life-short1..5 (guideline 16-9 B, miya 2026-11-07): reuses make.py scenes, replaces vpage()
# (dark tint + halo behind the focal subject + fireflies + dark band behind the hook), redraws the frog last with pupils clamped inside the eye white.
# Hooks unchanged (script words): 1 IT RAINS METHANE  2 WHAT'S UNDER THE SMOG?  3 LIFE WITHOUT WATER?  4 A HIDDEN OCEAN  5 FLYING ON TITAN
# run: python3 videos/titan-life-short1/thumb/make_b.py [n..] ; then SLUG=titan-life-shortN python3 tools/thumb_shot.py
import os, sys, math, shutil
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, '../../..')); sys.path.insert(0, os.path.join(REPO, 'tools'))
import thumb_lib
from thumb_lib import rad, halo, darkband, fireflies
src = open(os.path.join(HERE, 'make.py')).read(); src = src[:src.index("if __name__ == '__main__':")]
ns = {'__file__': os.path.join(HERE, 'make.py'), '__name__': 'titan_all'}; exec(compile(src, 'make.py', 'exec'), ns)
LIM = 6.6   # eye white r13.5, stroke margin 2.1 -> pupil (r4.4) centre <= 7.0 from eye centre; centre offset = (1+lx, ly)
FROGS = []; CUR = {}
orig_frog = ns['frog']
def frog_defer(*a, **kw):
    lx, ly = kw.get('look', (0, 0)); dx, dy = 1 + lx, ly; m = math.hypot(dx, dy)
    if m > LIM: dx, dy = dx * LIM / m, dy * LIM / m
    kw['look'] = (dx - 1, dy); FROGS.append((a, kw)); return ''
ns['frog'] = frog_defer
# n: tint colour, tint opacity, (halo cx, cy, r), inner, outer, halo opacity, fireflies (col, core), hook top
C = {1: ('#0a0408', .42, (780, 1660, 440), '#d8fff4', '#18c8a0', .75, ('#a8ffe8', '#f0fffa')),
     2: ('#0a0408', .30, (545, 340, 480), '#fff4d0', '#ff9a40', .9, ('#ffd9a0', '#fff6e0')),
     3: ('#06020a', .22, (540, 1500, 430), '#ffd0ee', '#ff4aa8', .7, ('#ffb8e0', '#fff0fa')),
     4: ('#020a1c', .15, (400, 1600, 460), '#e0f8ff', '#2a9aff', .65, ('#b8e8ff', '#fff')),
     5: ('#0a0408', .30, (540, 380, 560), '#fff0c0', '#ffa050', .85, ('#ffd9a0', '#fff6e0'))}
TX = {5: 'translate(540 520) scale(1.16) translate(-540 -450)'}   # make_5 draws its frog inside this group
def vpage(bg, svg, lines, outline='#050b18', top=700):
    n = CUR['n']; tint, ta, (hx, hy, hr), hi, ho, hop, ff = C[n]
    y1 = top + sum(int(s * .97) for _, s, _ in lines[:-1]) + lines[-1][1]
    fr = ''.join(orig_frog(*a, **kw) for a, kw in FROGS)
    if n in TX: fr = f'<g transform="{TX[n]}">{fr}</g>'
    FROGS.clear()
    vig = '<rect width="1080" height="1920" fill="url(#vig)"/>'
    assert vig in svg, 'vig rect missing'
    ov = (f'<rect width="1080" height="1920" fill="{tint}" opacity="{ta}"/>'
          f'<ellipse cx="{hx}" cy="{hy}" rx="{hr}" ry="{hr}" fill="url(#hB)" opacity="{hop}"/>'
          + darkband(top - 10, y1 + 10, .5) + fireflies(30, 120, 1850, col=ff[0], core=ff[1], seed=n) + fr)
    svg = svg.replace(vig, ov + vig).replace('<defs>', '<defs>' + halo('hB', hx, hy, hr, inner=hi, outer=ho), 1)
    return thumb_lib.vpage(bg, svg, lines, outline=outline, top=top)
ns['vpage'] = vpage
if __name__ == '__main__':
    for n in map(int, sys.argv[1:] or '12345'):
        CUR['n'] = n; FROGS.clear()
        html = ns[f'make_{n}']()
        o = os.path.join(REPO, 'videos', f'titan-life-short{n}', 'thumb')
        open(os.path.join(o, 'A.html'), 'w').write(html); print('short', n, 'ok')
