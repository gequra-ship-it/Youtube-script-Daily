# STYLE B shorts thumbnails for dark-matter-96-percent-short1..5 (guideline 16-9 B, miya 2026-11-07): reuses make_all.py scenes, replaces out()
# (tint + halo behind the focal subject + fireflies + dark band behind the hook + vignette), redraws the frog last with pupils clamped inside the eye white.
# Hooks unchanged (script words): 1 ALL THIS IS UNDER 5%  2 WHO LEFT THESE?  3 NOT BLACK. INVISIBLE  4 IT'S SPEEDING UP!  5 WE CAN READ 5 PAGES
# run: python3 videos/dark-matter-96-percent-short1/thumb/make_b.py [n..] ; then SLUG=dark-matter-96-percent-shortN python3 tools/thumb_shot.py
import os, sys, math, re, random
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, '../../..')); sys.path.insert(0, os.path.join(REPO, 'tools'))
import thumb_lib
from thumb_lib import rad, halo, darkband, fireflies
src = open(os.path.join(HERE, 'make_all.py')).read(); src = src[:src.index("if __name__ == '__main__':")]
ns = {'__file__': os.path.join(HERE, 'make_all.py'), '__name__': 'dm_all'}; exec(compile(src, 'make_all.py', 'exec'), ns)
LIM = 6.6   # white r13.5, stroke margin 2.1 -> pupil (r4.4) centre may be <= 7.0 from the eye centre; centre offset = (1+lx, ly)
FROGS = []
orig_frog = ns['frog']
def frog_defer(*a, **kw):
    lx, ly = kw.get('look', (0, 0)); dx, dy = 1 + lx, ly; m = math.hypot(dx, dy)
    if m > LIM: dx, dy = dx * LIM / m, dy * LIM / m
    kw['look'] = (dx - 1, dy); FROGS.append((a, kw)); return ''
ns['frog'] = frog_defer
# n: tint, tint opacity, (halo cx, cy, r), inner, outer, halo opacity, fireflies (col, core)
C = {1: ('#0a0420', .12, (760, 1180, 470), '#fff0c0', '#ff9a40', .7, ('#ffd9a0', '#fff6e0')),
     2: ('#030a2c', .1, (650, 1000, 430), '#e8f0ff', '#8a6cff', .6, ('#d0d8ff', '#fff')),
     3: ('#030a1c', .1, (560, 1250, 460), '#fff4d0', '#5a8cff', .55, ('#c8dcff', '#fff')),
     4: ('#0a0420', .1, (800, 330, 420), '#fff6d0', '#ff7a3a', .75, ('#ffd0a0', '#fff6e0')),
     5: ('#0a0510', .1, (540, 1300, 520), '#fff0c0', '#ffa050', .7, ('#ffe0b0', '#fff8e8'))}
def out(bg, d, b, lines, outline, top):
    n = ns['CUR']['n']; c = ns['VCFG'][n]; tint, ta, (hx, hy, hr), hi, ho, hop, ff = C[n]
    b = re.sub(r'<rect width="1920" height="1080" fill="url\(#vig\d\)"/>', '', b)
    b = b.replace('<rect width="1920" height="1080"', '<rect x="-3000" y="-3000" width="8000" height="8000"')
    rnd = random.Random(900 + n)
    top_stars = ''.join(f'<circle cx="{rnd.uniform(0, 1080):.0f}" cy="{rnd.uniform(0, c["ty"]):.0f}" r="{rnd.choice([1.2, 1.8, 2.5])}" fill="#eef0ff" opacity="{rnd.uniform(.2, .8):.2f}"/>' for _ in range(int(c['ty'] / 5)))
    top_stars += ns['spark'](rnd.randint(80, 300), rnd.randint(120, 300), 22) + ns['spark'](rnd.randint(780, 1000), rnd.randint(150, 380), 18, '#e8f0ff')
    L, top = c['lines'], c['top']
    y1 = top + sum(int(s * .97) for _, s, _ in L[:-1]) + L[-1][1]
    d += halo('hB', hx, hy, hr, inner=hi, outer=ho) + rad('vB', 540, 960, 1250, [(0, '#000', 0), (.6, '#000', 0), (1, '#05060a', .6)])
    o = f'<rect width="1080" height="1920" fill="{bg}"/><g transform="translate({c["tx"]} {c["ty"]}) scale({c["s"]})">{b}</g>' + ns['CUR'].get('extra', '') + top_stars
    o += f'<rect width="1080" height="1920" fill="{tint}" opacity="{ta}"/><ellipse cx="{hx}" cy="{hy}" rx="{hr}" ry="{hr}" fill="url(#hB)" opacity="{hop}"/>'
    o += darkband(top - 10, y1 + 10, .5) + fireflies(30, 120, 1850, col=ff[0], core=ff[1], seed=n)
    o += f'<g transform="translate({c["tx"]} {c["ty"]}) scale({c["s"]})">' + ''.join(orig_frog(*a, **kw) for a, kw in FROGS) + '</g>'
    FROGS.clear()
    o += '<rect width="1080" height="1920" fill="url(#vB)"/>'
    return thumb_lib.vpage(bg, thumb_lib.vsvg(d, o), L, outline=outline, top=top)
ns['out'] = out
if __name__ == '__main__':
    import shutil
    for n in map(int, sys.argv[1:] or '12345'):
        ns['CUR'].clear(); ns['CUR']['n'] = n; FROGS.clear()
        html = ns[f'make_{n}']()
        o = os.path.join(REPO, 'videos', f'dark-matter-96-percent-short{n}', 'thumb')
        for f in ('common.css', 'Fredoka-700.woff2'): shutil.copy(os.path.join(REPO, 'tools/assets/thumb_v', f), o)
        open(os.path.join(o, 'A.html'), 'w').write(html); print('short', n, 'ok')
