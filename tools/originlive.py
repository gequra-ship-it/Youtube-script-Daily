# usage: SLUG=<slug> python3 tools/originlive.py   (needs a built render/<slug>/index.html; exit 1 when a group without data-pivot turns about a point other than its own centre)
# LIVE origin check (miya 2026-10-29, short3 black hole): a spin/turn/roll/flip/wobble group that has no data-pivot must turn about the CENTRE of its own box (the check flags the frozen-corner failure: fixed point at a bbox corner and centre carried > 10 px).
# GSAP freezes a percent origin ("50% 50%") when the tween is first rendered; if that happens while the picture is display:none the bbox is empty and the origin becomes the box corner,
# so a big round object swung across the frame. build3 now defers percent-origin tweens (HINGE_JS), this check proves it on the built page: for every visible group that is rotated
# (> 2.5 deg) and not translated by GSAP, the group's own centre must stay where it is (< 10 px; a group that is deliberately carried has gsap x/y != 0 and is skipped).
import os, sys, json, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from paths import *
from playwright.sync_api import sync_playwright
vert = SLUG.endswith(tuple(f'short{i}' for i in range(1, 10))); W, H = (1080, 1920) if vert else (1920, 1080)
bd = json.load(open(f'{wdir()}/build/build_data.json')); cuts = bd['cuts']
JS = r'''([t]) => { Object.values(window.__timelines).forEach(tl => { tl.pause(); tl.seek(t, false); });
 const out = [];
 document.querySelectorAll('svg .mv').forEach((g, idx) => {
   const tt = g.closest('.t'); if (!tt || getComputedStyle(tt).display === 'none') return;
   if (g.hasAttribute('data-pivot') || g.querySelector(':scope > [data-pivot]')) return;   // the build wraps a pivoted core group: the pivot sits on the wrapper's child
   let M = null; try { M = g.transform.baseVal.consolidate(); M = M && M.matrix; } catch (e) {}
   if (!M) return;
   const gx = +gsap.getProperty(g, 'x') || 0, gy = +gsap.getProperty(g, 'y') || 0;
   if (Math.abs(gx) > 0.5 || Math.abs(gy) > 0.5) return;
   let b = null; try { b = g.getBBox(); } catch (e) {} if (!b || !(b.width + b.height)) return;
   const cx = b.x + b.width / 2, cy = b.y + b.height / 2;
   const det = (1 - M.a) * (1 - M.d) - M.c * M.b; let fx = null, fy = null;
   if (Math.abs(det) > 1e-4) { fx = ((1 - M.d) * M.e + M.c * M.f) / det; fy = ((1 - M.a) * M.f + M.b * M.e) / det; }
   const tol = 0.15 * Math.max(b.width, b.height);   // frozen origin = a bbox CORNER; hinges that turn about an edge/neck (nod, flip) are legitimate
   const corner = fx !== null && [[b.x, b.y], [b.x + b.width, b.y], [b.x, b.y + b.height], [b.x + b.width, b.y + b.height]].some(q => Math.hypot(q[0] - fx, q[1] - fy) < tol);
   out.push({i: idx, corner, cls: (g.getAttribute('class') || '').replace('mv ', ''), ang: Math.atan2(M.b, M.a) * 180 / Math.PI,
             carried: Math.hypot(M.a * cx + M.c * cy + M.e - cx, M.b * cx + M.d * cy + M.f - cy), box: Math.max(b.width, b.height)});
 });
 return out; }'''
bad = 0; seen = set(); measured = 0
with sync_playwright() as p:
    b = p.chromium.launch(executable_path=chrome(), args=['--no-sandbox']); pg = b.new_page(viewport={'width': W, 'height': H})
    pg.goto(f'file://{REPO}/render/{SLUG}/index.html'); pg.wait_for_timeout(1500)
    for c in cuts:
        for t in (c['t0'] + 1.2, (c['t0'] + c['t1']) / 2 + 0.9):
            for r in pg.evaluate(JS, [t]):
                if abs(r['ang']) < 2.5: continue
                measured += 1
                if r['carried'] > 10 and r['corner'] and (c['id'], r['cls']) not in seen:
                    seen.add((c['id'], r['cls'])); bad += 1
                    print(f'{SLUG} {c["id"]} {r["cls"]}: turns {r["ang"]:.0f} deg but its own centre is carried {r["carried"]:.0f} px (box {r["box"]:.0f}) -> origin is not the centre; give it a data-pivot at its centre')
    b.close()
print(f'originlive {SLUG}: measured {measured} rotated groups, {bad} problems'); sys.exit(1 if bad else 0)
