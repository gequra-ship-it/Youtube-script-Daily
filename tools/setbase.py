# usage: python3 tools/setbase.py <slug> [<uid> ...]      (no uid = every picture)
# Writes data-pivot = the FOOT of the stem / trunk / post for every standing thing that sways (mv-sway / mv-core-sway / mv-tilt / mv-wobble with a ground-standing name: tree, reed,
# grass, cattail, flower, plant, bush, sign, post, pole, mast, lamp post, tower, fence) that has no data-pivot yet (miya 2026-10-29: 'tree / grass / sign axis').
# Foot = x-centre of the narrow shapes that touch the bottom of the group (wide shapes such as a shadow or a pond are ignored), y = bottom of those shapes.
# A group that holds SEVERAL clumps far apart (reeds left + right) is split into one group per clump first.
import os, sys, re, glob
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from paths import *
from playwright.sync_api import sync_playwright
NAMES = re.compile(r'(^|-)(tree|trees|oak|pine|palm|grass|reed|reeds|cattail|cattails|flower|flowers|plant|plants|bush|stalk|sign|signpost|post|pole|mast|tower|fence|lamppost)(-|$)', re.I)
JS = r'''() => { const svg = document.querySelector('svg'); const R = svg.getScreenCTM().inverse(); const pt = (x, y) => new DOMPoint(x, y).matrixTransform(R);
 const box = e => { const b = e.getBoundingClientRect(), a = pt(b.x, b.y), c = pt(b.x + b.width, b.y + b.height); return {x0: a.x, y0: a.y, x1: c.x, y1: c.y}; };
 const out = [];
 svg.querySelectorAll('[id^="mv-"]').forEach(g => {
   if (!/^mv-(core-)?(sway|tilt|wobble)-/.test(g.id) || g.getAttribute('data-pivot')) return; const tail = g.id.replace(/^mv-(core-)?[a-z]+-/, ''); if (!NAMES.test(tail)) return;
   const parts = [...g.querySelectorAll('path,line,polyline,polygon,circle,ellipse,rect')].filter(e => !e.closest('defs,clipPath,mask')).map(e => ({e, b: box(e)})).filter(o => o.b.x1 - o.b.x0 > 0 || o.b.y1 - o.b.y0 > 0);
   if (!parts.length) return; const gb = box(g); const gw = gb.x1 - gb.x0, gh = gb.y1 - gb.y0;
   // narrow shapes (not shadows / ponds): width < 0.5 of the group width or < 60 px
   const narrow = parts.filter(o => (o.b.x1 - o.b.x0) < Math.max(60, 0.5 * gw) || (o.b.y1 - o.b.y0) > 0.4 * gh);
   const pool = narrow.length ? narrow : parts; const yb = Math.max(...pool.map(o => o.b.y1)); const foot = pool.filter(o => o.b.y1 > yb - Math.max(8, 0.04 * gh));
   // clusters along x (gap > 90 px) -> several clumps?
   const ps = foot.map(o => ({x: (o.b.x0 + o.b.x1) / 2, y: o.b.y1, e: o.e})).sort((a, b) => a.x - b.x); const cl = []; ps.forEach(p => { const L = cl[cl.length - 1]; if (L && p.x - L[L.length - 1].x < 90) L.push(p); else cl.push([p]); });
   out.push({id: g.id, gw, gh, clusters: cl.length, x: ps.reduce((s, p) => s + p.x, 0) / ps.length, y: yb});
 });
 return out; }'''.replace('NAMES.test(tail)', '/(^|-)(tree|trees|oak|pine|palm|grass|reed|reeds|cattail|cattails|flower|flowers|plant|plants|bush|stalk|sign|signpost|post|pole|mast|tower|fence|lamppost)(-|$)/i.test(tail)')
def main():
    slug = sys.argv[1]; uids = sys.argv[2:]; vert = slug.endswith(tuple(f'short{i}' for i in range(1, 10)))
    files = sorted(glob.glob(f'{vdir(slug)}/art3/U*.svg')); files = [f for f in files if not uids or os.path.basename(f)[:-4] in uids]; n = 0
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path=chrome(), args=['--no-sandbox']); pg = b.new_page(viewport={'width': 1080 if vert else 1920, 'height': 1920 if vert else 1080})
        for f in files:
            pg.goto('file://' + f); res = pg.evaluate(JS)
            if not res: continue
            s = open(f).read()
            for r in res:
                m = re.search(r'<g id="%s"' % re.escape(r['id']), s)
                if not m: continue
                s = s[:m.end()] + f' data-pivot="{r["x"]:.0f} {r["y"]:.0f}"' + s[m.end():]; n += 1
                print(f"{os.path.basename(f)[:-4]} {r['id']}: foot {r['x']:.0f},{r['y']:.0f} (group {r['gw']:.0f}x{r['gh']:.0f}){'  [' + str(r['clusters']) + ' clumps in one group: consider splitting]' if r['clusters'] > 1 else ''}")
            open(f, 'w').write(s)
        b.close()
    print('setbase:', n, 'pivots written')
main()
