# usage: SLUG=<slug> [MIYA_WORK=...] python3 tools/pivotlive.py   (needs a built render/<slug>/index.html; exit 1 when a hinge turns about the wrong point)
# LIVE pivot check (miya 2026-10-29): pivcheck/attachcheck judge the static drawing, this judges what the timeline really does.
# For every group with data-pivot (mv-joint / chain / rotor / swing / flip / ...) it seeks the real page twice inside the unit, reads the group's current transform matrix,
# measures how far the pivot point itself is carried by the group's matrix (a hinge leaves its pivot where it is: < 10 px) and also prints the fixed point of the rotation. Groups whose angle is ~0 at both samples are skipped (nothing to measure).
import os, sys, json, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from paths import *
from playwright.sync_api import sync_playwright
vert = SLUG.endswith(tuple(f'short{i}' for i in range(1, 10))); W, H = (1080, 1920) if vert else (1920, 1080)
bd = json.load(open(f'{wdir()}/build/build_data.json')); cuts = bd['cuts']
JS = r'''([t]) => { Object.values(window.__timelines).forEach(tl => { tl.pause(); tl.seek(t, false); });
 const out = [];
 document.querySelectorAll('[data-pivot]').forEach((g, idx) => {
   const tt = g.closest('.t'); if (!tt) return; const cs = getComputedStyle(tt); if (cs.display === 'none') return;
   const p = (g.getAttribute('data-pivot') || '').trim().split(/[\s,]+/).map(Number); if (p.length !== 2 || p.some(isNaN)) return;
   let M = null; try { M = g.transform.baseVal.consolidate(); M = M && M.matrix; } catch (e) {}
   if (!M) return;
   const want = miyaPv(g, p[0], p[1]).split(' ').map(Number);
   out.push({i: idx, vis: [...document.querySelectorAll('.t')].filter(e => getComputedStyle(e).display !== 'none').length, cls: (g.getAttribute('class') || '').replace('mv ', ''), M: [M.a, M.b, M.c, M.d, M.e, M.f], want});
 });
 return out; }'''
def fixed(M):
    a, b, c, d, e, f = M; det = (1 - a) * (1 - d) - c * b   # (I - A) p = t
    if abs(det) < 1e-4: return None
    x = ((1 - d) * e + c * f) / det; y = ((1 - a) * f + b * e) / det; return x, y
bad = 0; seen = {}; measured = 0; stuck = 0; total_pivots = open(f'{REPO}/render/{SLUG}/index.html', encoding='utf-8').read().count('data-pivot=')
with sync_playwright() as p:
    b = p.chromium.launch(executable_path=chrome(), args=['--no-sandbox']); pg = b.new_page(viewport={'width': W, 'height': H})
    errs = []; pg.on('pageerror', lambda e: errs.append(str(e)[:200]))
    pg.goto(f'file://{REPO}/render/{SLUG}/index.html'); pg.wait_for_timeout(1500)
    nf = pg.evaluate('() => (window.MIYA_FOLLOW || []).length'); want_f = open(f'{REPO}/render/{SLUG}/index.html', encoding='utf-8').read().count('miyaFollow(tl,"')
    if errs: print(SLUG, 'pivotlive: JS ERRORS on page load:', errs[:3]); bad += 1
    if nf != want_f: print(SLUG, f'pivotlive: {want_f} labels should follow objects but only {nf} are registered (label follow broken)'); bad += 1
    for c in cuts:
        t0, t1 = c['t0'], c['t1']; ts = [t0 + 1.2, (t0 + t1) / 2 + 0.9]
        res = [pg.evaluate(JS, [t]) for t in ts]
        by = {}
        for k, rs in enumerate(res):
            for r in rs: by.setdefault(r['i'], []).append(r)
        for i, rs in by.items():
            best = None
            for r in rs:
                a, b_, c_, d, e, f = r['M']; ang = math.degrees(math.atan2(b_, a))
                if r.get('vis', 1) > 3: stuck += 1   # more than a couple of pictures visible at once = the page itself is broken (a picture stuck on top)
                if abs(ang) < 2.5: continue          # too small to solve reliably
                measured += 1
                fp = fixed(r['M'])
                wx, wy = r['want']; dx = a * wx + c_ * wy + e - wx; dy = b_ * wx + d * wy + f - wy; err = math.hypot(dx, dy)   # how far the pivot point itself is carried: a part that hinges at its pivot leaves it where it is
                if best is None or err > best[0]: best = (err, fp or (0, 0), r['want'], ang, r['cls'])
            if best and best[0] > 10 and (c['id'], best[4]) not in seen:
                seen[(c['id'], best[4])] = 1; bad += 1
                print(f"{SLUG} {c['id']} {best[4]}: its pivot point {best[2][0]:.0f},{best[2][1]:.0f} is carried {best[0]:.0f} px when the part turns {best[3]:.0f} deg (it really turns about {best[1][0]:.0f},{best[1][1]:.0f}): the part leaves its body")
    b.close()
if stuck: print(SLUG, 'pivotlive: BROKEN PAGE, several pictures visible at once at', stuck, 'samples'); bad += 1
if measured < 1 and total_pivots: print(SLUG, f'pivotlive: no hinge sample could be measured (page has data-pivot groups): the check could not see the pictures (seek broken?)'); bad += 1
print(SLUG, 'pivotlive:', bad, 'problems;', measured, 'hinge samples measured'); sys.exit(1 if bad else 0)
