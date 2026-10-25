# usage: python3 tools/frog_auto2.py <slug>...   (2026-10-25, miya) The frog no longer stands beside a picture pointing at things (that stays on the chalkboard only).
# In picture units it either sits ON a moving object (rides along: inside that group, so it follows its motion/turns) or, when there is no
# fitting object, sits small in a bottom corner of the background. Keeps moods/outfit from the sidecar; drops points/moves.
import sys, os, glob, json, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from paths import *
from playwright.sync_api import sync_playwright
OK = re.compile(r'^mv-(core-(swell|heartbeat|wobble|sway|glide|approach|drop|ping|tremble)|path|slide|swing)')
JS = '''()=>{const o=[];for(const g of document.querySelectorAll('g[id^="mv-"]')){const b=g.getBBox();if(b.width<8)continue;o.push([g.id,b.x,b.y,b.width,b.height])}return o}'''
n = 0
with sync_playwright() as p:
    b = p.chromium.launch(executable_path=chrome(), args=['--no-sandbox']); pg = b.new_page()
    for slug in sys.argv[1:]:
        vert = 'short' in slug; W, H = (1080, 1920) if vert else (1920, 1080)
        for fn in sorted(glob.glob(f'{REPO}/videos/{slug}/art3/U*.json')):
            d = json.load(open(fn)); f = d.get('frog')
            if not isinstance(f, dict): continue
            pg.set_content('<body style="margin:0">' + open(fn[:-5] + '.svg').read() + '</body>')
            gs = {g[0]: g for g in pg.evaluate(JS)}
            pick = f.get('ride') or f.get('point_obj')
            if pick not in gs or not OK.match(pick or ''):
                cand = [g for g in gs.values() if OK.match(g[0]) and 60 <= g[3] <= W * .8 and g[4] >= 40]
                cand.sort(key=lambda g: -g[3] * g[4]); pick = cand[0][0] if cand else None
            keep = {k: f[k] for k in ('moods', 'outfit') if k in f}
            if pick:
                _, x, y, w, h = gs[pick]
                s = round(min(1.5, max(.9, w / 170)), 2); cx = x + w / 2
                keep.update(ride=pick, x=round(cx), y=round(y + 8 * s), s=s, flip=1 if cx < W / 2 else -1, kind='ride')
            else:
                n += 1; left = n % 2 == 1
                keep.update(x=150 if left else W - 150, y=(H - 150) if vert else (H - 40), s=1.7 if vert else 1.35, flip=1 if left else -1, kind='bg')
            d['frog'] = keep
            json.dump(d, open(fn, 'w'), ensure_ascii=False, indent=1)
            print(slug, os.path.basename(fn), keep.get('kind'), pick, keep['x'], keep['y'], keep['s'])
    b.close()
