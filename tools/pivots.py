# -*- coding: utf-8 -*-
# Pivot points for arm/hand motion groups (fix 2026-10-11: user saw whole arms swinging away from the shoulder).
# Before, build3 rotated every mv-arm group around the top-centre of its bounding box. For a raised or diagonal arm that point
# is the hand or the middle of the arm, so the shoulder end swung off the body.
# Now: the pivot of an arm is the end of its first drawn line/path that lies closest to the body (the nearest mv-breathe /
# mv-lean / mv-walk group, else the picture's figure-free centre is not used and the path start is taken).
# Hands rotate a little around their own centre (no translation), so they stay on the wrist.
# Result per arm: [ox, oy, X, Y] = pivot in px from the group's local bounding-box corner (GSAP transformOrigin) and in root units.
import os, json
import sys; sys.path.insert(0, __import__('os').path.dirname(__import__('os').path.abspath(__file__))); from paths import chrome
from playwright.sync_api import sync_playwright

JS = r'''() => {
  const root = document.documentElement;
  const inv = root.getScreenCTM().inverse();
  const toRoot = (el, x, y) => { const p = root.createSVGPoint(); p.x = x; p.y = y;
      return p.matrixTransform(el.getScreenCTM()).matrixTransform(inv); };
  const box = el => { const b = el.getBBox(); const pts = [[b.x,b.y],[b.x+b.width,b.y],[b.x,b.y+b.height],[b.x+b.width,b.y+b.height]].map(q => toRoot(el, q[0], q[1]));
      const xs = pts.map(p => p.x), ys = pts.map(p => p.y);
      return {x0: Math.min(...xs), y0: Math.min(...ys), x1: Math.max(...xs), y1: Math.max(...ys)}; };
  const bodies = [...document.querySelectorAll('[id^="mv-breathe"],[id^="mv-lean"],[id^="mv-walk"]')].map(b => {
      const r = box(b); return {el: b, cx: (r.x0 + r.x1) / 2, cy: r.y0 + (r.y1 - r.y0) * 0.35}; });   // upper torso
  const out = {};
  for (const g of document.querySelectorAll('[id^="mv-arm"]')) {
    const r = box(g);
    if (g.id.startsWith('mv-hand')) continue;
    const gc = [(r.x0 + r.x1) / 2, (r.y0 + r.y1) / 2];
    // body: an ancestor body group, else the nearest body group
    let body = bodies.find(b => b.el.contains(g)) || null;
    if (!body && bodies.length) body = bodies.reduce((a, b) => Math.hypot(a.cx - gc[0], a.cy - gc[1]) < Math.hypot(b.cx - gc[0], b.cy - gc[1]) ? a : b);
    const el = g.matches('path,line,polyline,polygon') ? g : g.querySelector('path,line,polyline,polygon');
    let ends = [];
    if (el) {
      if (el.tagName === 'path') { const L = el.getTotalLength(); const a = el.getPointAtLength(0), b = el.getPointAtLength(L);
                                   ends = [toRoot(el, a.x, a.y), toRoot(el, b.x, b.y)]; }
      else if (el.tagName === 'line') ends = [toRoot(el, el.x1.baseVal.value, el.y1.baseVal.value), toRoot(el, el.x2.baseVal.value, el.y2.baseVal.value)];
      else { const P = el.points; if (P.numberOfItems) { const a = P.getItem(0), b = P.getItem(P.numberOfItems - 1); ends = [toRoot(el, a.x, a.y), toRoot(el, b.x, b.y)]; } }
    }
    if (ends.length === 2 && Math.hypot(ends[0].x - ends[1].x, ends[0].y - ends[1].y) < 6) ends = [];   // closed outline: its start point means nothing
    if (!ends.length) {   // only rects/ellipses: use the bounding-box point nearest the body
      ends = [[r.x0,r.y0],[(r.x0+r.x1)/2,r.y0],[r.x1,r.y0],[r.x0,(r.y0+r.y1)/2],[r.x1,(r.y0+r.y1)/2],[r.x0,r.y1],[(r.x0+r.x1)/2,r.y1],[r.x1,r.y1]].map(q => ({x: q[0], y: q[1]}));
    }
    let best = ends[0];
    if (body) best = ends.reduce((a, b) => Math.hypot(a.x - body.cx, a.y - body.cy) <= Math.hypot(b.x - body.cx, b.y - body.cy) ? a : b);
    // GSAP transformOrigin for SVG is in px from the group's own bounding-box corner (local coordinates)
    const q = root.createSVGPoint(); q.x = best.x; q.y = best.y;
    const l = q.matrixTransform(root.getScreenCTM()).matrixTransform(g.getScreenCTM().inverse());
    const lb = g.getBBox();
    out[g.id] = [l.x - lb.x, l.y - lb.y, best.x, best.y];
  }
  return out;
}'''


def compute(files, W=1920, H=1080, cache=None):
    """{svg path: {mv-id: [x, y]}} for every mv-arm*/mv-hand* group. cache: json path keyed by file + mtime."""
    old = {}
    if cache and os.path.exists(cache):
        try: old = json.load(open(cache))
        except Exception: old = {}
    res, todo = {}, []
    for f in files:
        k = f'{os.path.abspath(f)}|{os.path.getmtime(f)}'
        if k in old: res[f] = old[k]
        else: todo.append(f)
    if todo:
        with sync_playwright() as p:
            b = p.chromium.launch(executable_path=chrome())
            pg = b.new_page(viewport={'width': W, 'height': H})
            for f in todo:
                s = open(f, encoding='utf-8').read()
                if 'mv-arm' not in s and 'mv-hand' not in s: res[f] = {}; continue
                pg.goto('file://' + os.path.abspath(f)); res[f] = pg.evaluate(JS)
            b.close()
    if cache:
        json.dump({f'{os.path.abspath(f)}|{os.path.getmtime(f)}': v for f, v in res.items()}, open(cache, 'w'))
    return res
