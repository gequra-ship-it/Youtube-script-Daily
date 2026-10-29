# usage: python3 tools/grpinfo.py <slug> <uid> [<uid> ...]   -> every mv- group of the picture: bbox (picture coords), data-pivot, nesting parent mv group.
import os, sys, glob
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from paths import *
from playwright.sync_api import sync_playwright
JS = '''() => { const svg = document.querySelector('svg'); const R = svg.getScreenCTM().inverse(); const out = [];
 svg.querySelectorAll('[id^="mv-"]').forEach(g => { let b; try { b = g.getBoundingClientRect(); } catch (e) { return; } const a = new DOMPoint(b.x, b.y).matrixTransform(R), c = new DOMPoint(b.x + b.width, b.y + b.height).matrixTransform(R);
  const p = g.parentNode.closest && g.parentNode.closest('[id^="mv-"]'); out.push([g.id, Math.round(a.x), Math.round(a.y), Math.round(c.x), Math.round(c.y), g.getAttribute('data-pivot') || '', p ? p.id : '']); });
 return out; }'''
slug = sys.argv[1]; vert = slug.endswith(tuple(f'short{i}' for i in range(1, 10)))
with sync_playwright() as p:
    b = p.chromium.launch(executable_path=chrome(), args=['--no-sandbox']); pg = b.new_page(viewport={'width': 1080 if vert else 1920, 'height': 1920 if vert else 1080})
    for uid in sys.argv[2:]:
        pg.goto(f'file://{vdir(slug)}/art3/{uid}.svg'); print(uid)
        for r in pg.evaluate(JS): print(f'  {r[0]:42s} box {r[1]:5d},{r[2]:5d} - {r[3]:5d},{r[4]:5d}  pivot {r[5] or "-":10s} in {r[6]}')
    b.close()
