# usage: python3 tools/frog_obj.py <slug>...   For every frog unit with a "point", finds the moving picture group the arm points at and
# writes it as "point_obj" into the sidecar (frog.py then makes the arm follow that group's motion). Rest-pose bbox, smallest group containing
# the point, else the nearest centre within 220 px. Skips scenery groups (drift, scroll, glint, dash, ticks, smoke, lamp, fade, track).
import sys, os, glob, json, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from paths import *
from playwright.sync_api import sync_playwright
SKIP = re.compile(r'^mv-(drift|scroll|glint|dash|ticks|smoke|lamp|fade|track|breathe|nod|lean|arm|hand|walk)')
JS = '''()=>{const o=[];for(const g of document.querySelectorAll('g[id^="mv-"]')){const b=g.getBBox();if(b.width<8)continue;const m=g.getCTM();o.push([g.id,b.x,b.y,b.width,b.height])}return o}'''
with sync_playwright() as p:
    b = p.chromium.launch(executable_path=chrome(), args=['--no-sandbox']); pg = b.new_page()
    for slug in sys.argv[1:]:
        for fn in sorted(glob.glob(f'{REPO}/videos/{slug}/art3/U*.json')):
            d = json.load(open(fn)); f = d.get('frog')
            if not isinstance(f, dict) or not f.get('point'): continue
            pg.set_content('<body style="margin:0">' + open(fn[:-5] + '.svg').read() + '</body>')
            gs = [g for g in pg.evaluate(JS) if not SKIP.match(g[0])]
            px, py = f['point']; best = None
            for gid, x, y, w, h in gs:
                if x <= px <= x + w and y <= py <= y + h:
                    a = w * h
                    if best is None or a < best[0]: best = (a, gid)
            if best is None:
                near = sorted(((x + w / 2 - px) ** 2 + (y + h / 2 - py) ** 2, gid) for gid, x, y, w, h in gs)
                if near and near[0][0] < 220 ** 2: best = (0, near[0][1])
            if best: f['point_obj'] = best[1]
            else: f.pop('point_obj', None)
            json.dump(d, open(fn, 'w'), ensure_ascii=False, indent=1)
            print(slug, os.path.basename(fn), f['point'], '->', f.get('point_obj'))
    b.close()
