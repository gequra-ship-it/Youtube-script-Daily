# STYLE B shorts thumbnails for short-faced-bear (guideline 16-9 B, miya 2026-11-07): reuses the sfb_shorts pictures (bear scene shifted to the top half,
# ground ~y 830), scene frog suppressed and redrawn big in the bottom third (pupils clamped), halo + fireflies + dark band, hook on band y 880-1250.
# Hooks only from the short scripts, no numbers.  python3 videos/short-faced-bear/thumb/make_b.py ; then SLUG=short-faced-bear-shortN python3 tools/thumb_shot.py
# 1 STAND YOUR / GROUND?  2 RUNNING / BEAR?  3 WHAT DID / IT EAT?  4 SLOW / SQUEEZE  5 LIVING / COUSIN
import os, sys, math, random, shutil, importlib.util
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, '../../..')); sys.path.insert(0, os.path.join(REPO, 'tools'))
from thumb_lib import vpage, vsvg, lin, rad, spark, fireflies, darkband, halo
p = os.path.join(REPO, 'videos', 'short-faced-bear-short1', 'thumb', 'sfb_shorts.py')
s = importlib.util.spec_from_file_location('sfb_shorts', p); m = importlib.util.module_from_spec(s); s.loader.exec_module(m)
_frog = m.frog; CAP = {}
def frog_scene(x, y, sc, **kw):          # suppress the scene frog, remember its costume
    CAP.clear(); CAP.update(kw); return ''
m.frog = frog_scene
def clamp(look, lim=5.4):
    dx, dy = look; h = math.hypot(dx, dy)
    return look if h <= lim else (dx * lim / h, dy * lim / h)
# n: scale, scene-centre x, ground y in scene coords, ground target on screen, sky/bottom colours, halo (cx, cy, inner, outer), fireflies, hook
C = {1: dict(s=.84, cx=1170, G=935, top='#231a3a', bot='#140c12', halo=(560, 560, '#fff3cf', '#ff9a50'), ff=('#ffd27a', '#fff6e0'), hook=[('STAND YOUR', 170, 'w'), ('GROUND?', 215, 'y')]),
     2: dict(s=1.0, cx=1330, G=905, top='#3d78b8', bot='#4a3e24', halo=(560, 560, '#fff3cf', '#ffd27a'), ff=('#fff3a8', '#fffbd0'), hook=[('RUNNING', 200, 'y'), ('BEAR?', 230, 'w')]),
     3: dict(s=1.0, cx=1320, G=900, top='#0e1e2a', bot='#2a180c', halo=(600, 600, '#e8fff4', '#7ff5d8'), ff=('#a8ffe0', '#fff'), hook=[('WHAT DID', 160, 'w'), ('IT EAT?', 230, 'y')]),
     4: dict(s=.94, cx=1150, G=860, top='#1a2a2c', bot='#0e0c08', halo=(520, 600, '#fff3cf', '#ffc060'), ff=('#ffd27a', '#fff6e0'), hook=[('SLOW', 200, 'w'), ('SQUEEZE', 190, 'y')]),
     5: dict(s=1.0, cx=1220, G=800, top='#1e3a3a', bot='#2a4a3a', halo=(560, 640, '#fff3cf', '#7ff5d8'), ff=('#a8ffe0', '#fff'), hook=[('LIVING', 190, 'w'), ('COUSIN', 210, 'y')])}
GY = 840
def build(n):
    c = C[n]; fn = getattr(m, f'make_{n}'); dd, bb, _, outline = fn()
    bb = bb.replace(f'<rect width="1920" height="1080" fill="url(#vig{n})"/>', '')
    sc = c['s']; ty = GY - c['G'] * sc; tx = 540 - c['cx'] * sc; bot_y = ty + 1080 * sc
    dd += rad('vvig', 540, 960, 1250, [(0, '#000', 0), (.62, '#000', 0), (1, '#05060a', .6)])
    hx, hy, hi, ho = c['halo']; dd += halo('hb', hx, hy, 560, inner=hi, outer=ho)
    dd += f'<linearGradient id="gfade" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{c["bot"]}" stop-opacity="0"/><stop offset=".35" stop-color="{c["bot"]}" stop-opacity=".85"/><stop offset="1" stop-color="{c["bot"]}"/></linearGradient>'
    o = f'<rect width="1080" height="1920" fill="{c["top"]}"/>'
    o += f'<g transform="translate({tx:.1f} {ty:.1f}) scale({sc})">{bb}</g>'
    o += f'<ellipse cx="{hx}" cy="{hy}" rx="560" ry="560" fill="url(#hb)" opacity=".35"/>'
    o += f'<rect x="0" y="{bot_y - 1:.0f}" width="1080" height="{1922 - bot_y:.0f}" fill="{c["bot"]}"/>'
    o += f'<rect x="0" y="{GY - 60}" width="1080" height="420" fill="url(#gfade)"/>'
    o += darkband(870, 1260, .55) + fireflies(34, 120, 1850, col=c['ff'][0], core=c['ff'][1], seed=n)
    kw = dict(CAP); kw['look'] = clamp(kw.get('look', (0, 0))); kw['flip'] = False
    o += f'<ellipse cx="540" cy="1804" rx="215" ry="24" fill="#000" opacity=".4"/>'
    o += _frog(540, 1800, 3.8, **kw)
    o += '<rect width="1080" height="1920" fill="url(#vvig)"/>'
    out = os.path.join(REPO, 'videos', f'short-faced-bear-short{n}', 'thumb'); os.makedirs(out, exist_ok=True)
    for f in ('common.css', 'Fredoka-700.woff2'): shutil.copy(os.path.join(REPO, 'tools/assets/thumb_v', f), out)
    open(os.path.join(out, 'A.html'), 'w').write(vpage('#101010', vsvg(dd, o), c['hook'], outline=outline, top=885))
    print('short', n, 'ok')
if __name__ == '__main__':
    for n in (sys.argv[1:] or '12345'): build(int(n))
