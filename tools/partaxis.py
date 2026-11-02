# usage: python3 tools/partaxis.py <slug> [--fix] [uid ...]      (miya 2026-11-02: squid arms hinged at their free ends, a jaw hinged at its tip, a jellyfish squashing 6x per half second)
# For every hinged creature part (mv-joint/chain/swing/tilt group whose name has arm|tentacle|leg|feeler|antenna|jaw|tail|fin|flipper|claw|limb|neck|wing|palp)
# the pivot must sit on the END of the part that is NEAREST the creature body (centre of the sibling groups that share the name prefix; for a lone part: the drawing's nearest bigger group).
# Reports a part whose pivot is mid-part or at the far end; --fix rewrites data-pivot to the correct end. Also flags mv-wiggle with data-amp > .3 (scale fraction) or a period < .6.
import os, sys, re, json, glob, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from paths import *
from playwright.sync_api import sync_playwright
PART = r'(arm|tentacle|leg|feeler|antenna|jaw|tail|fin|flipper|claw|limb|neck|wing|palp)s?'
JS = r'''() => {
 const out = [];
 const gs = [...document.querySelectorAll('g[id^="mv-"]')];
 const info = g => { const r = g.getBoundingClientRect(); return {id: g.id, x: r.x, y: r.y, w: r.width, h: r.height}; };
 const all = gs.map(info);
 for (const g of gs) {
   const m = g.id.match(/^mv-(joint|chain)-(.+)$/); if (!m) continue; if (m[1] === 'chain' && !/-1$/.test(m[2])) continue;
   const name = m[2]; const pm = name.match(/(^|-)(%PART%)(-|$)/); if (!pm) continue;
   const pv = (g.getAttribute('data-pivot') || '').trim().split(/[\s,]+/).map(Number); if (pv.length !== 2 || pv.some(isNaN)) continue;
   const pc = g.parentNode.getCTM ? g.parentNode.getCTM() : null; const pp = pc ? new DOMPoint(pv[0], pv[1]).matrixTransform(pc) : {x: pv[0], y: pv[1]}; const ic = pc ? pc.inverse() : null;
   const pts = []; g.querySelectorAll('path,line,polyline,polygon,rect,ellipse,circle').forEach(e => {
     const ctm = e.getCTM(), root = document.querySelector('svg').getCTM();
     try { if (e.getTotalLength) { const L = e.getTotalLength(), n = Math.max(8, Math.min(60, Math.round(L / 12))); for (let i = 0; i <= n; i++) { const p = e.getPointAtLength(L * i / n); const q = new DOMPoint(p.x, p.y).matrixTransform(ctm); pts.push([q.x, q.y]); } } } catch (er) {}
   });
   const prefix = name.slice(0, pm.index).replace(/-$/, '');
   const sib = all.filter(o => o.id !== g.id && prefix && o.id.includes(prefix) && !new RegExp('(^|-)(%PART%)(-|$)').test(o.id));
   out.push({id: g.id, pv: [pp.x, pp.y], inv: ic ? [ic.a, ic.b, ic.c, ic.d, ic.e, ic.f] : [1, 0, 0, 1, 0, 0], pts, prefix, sib: sib.map(o => [o.x + o.w / 2, o.y + o.h / 2, o.w * o.h]), r: g.getBoundingClientRect().toJSON()});
 }
 const ws = [...document.querySelectorAll('g[id^="mv-wiggle"]')].map(g => ({id: g.id, amp: g.getAttribute('data-amp'), per: g.getAttribute('data-per')}));
 return {parts: out, wig: ws, big: all.filter(o => !/^mv-(joint|chain|swing)/.test(o.id)).map(o => [o.x + o.w / 2, o.y + o.h / 2, o.w * o.h])}; }'''.replace('%PART%', PART)
STRICT = '--strict' in sys.argv
WIG = 0
def audit(slug, uids=None, fix=False):
    global WIG
    WIG = 0
    vert = slug.endswith(tuple(f'short{i}' for i in range(1, 10))); W, H = (1080, 1920) if vert else (1920, 1080)
    files = sorted(glob.glob(f'{REPO}/videos/{slug}/art3/U*.svg')); n = 0
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path=chrome(), args=['--no-sandbox']); pg = b.new_page(viewport={'width': W, 'height': H})
        for f in files:
            uid = os.path.basename(f)[:-4]
            if uids and uid not in uids: continue
            svg = open(f, encoding='utf-8').read(); changed = svg
            pg.set_content(f'<html><body style="margin:0">{svg}</body></html>'); pg.evaluate('()=>{const s=document.querySelector("svg");s.setAttribute("width",%d);s.setAttribute("height",%d)}' % (W, H))
            res = pg.evaluate(JS)
            for w in res['wig']:
                amp = float(w['amp']) if w['amp'] else .06; per = float(w['per']) if w['per'] else .35
                if amp > .3 or per < .6:
                    n += 1; WIG += 1; print(f'{slug} {uid} {w["id"]}: wiggle amp {amp} per {per} -> too violent/fast (scale fraction .06, period >= .9)')
                    if fix:
                        changed = re.sub(r'(<g id="%s")([^>]*)>' % re.escape(w['id']), lambda m: m.group(1) + re.sub(r'\s*data-(amp|per)="[^"]*"', '', m.group(2)) + ' data-amp=".06" data-per="1"' + '>', changed, count=1)
            for pt in res['parts']:
                pts = pt['pts']
                if re.search(r'<g id="%s"[^>]*data-keep="1"' % re.escape(pt['id']), svg): continue   # 2026-11-02: data-keep="1" = deliberate (body off-screen etc.)
                if len(pts) < 4: continue
                cx = cy = None
                if pt['sib']:
                    tot = sum(s[2] for s in pt['sib']) or 1; cx = sum(s[0] * s[2] for s in pt['sib']) / tot; cy = sum(s[1] * s[2] for s in pt['sib']) / tot
                else:
                    r = pt['r']; px = (r['x'] + r['width'] / 2, r['y'] + r['height'] / 2)
                    bigger = [s for s in res['big'] if s[2] > r['width'] * r['height'] * 1.2 and s[2] < W * H * .6]
                    if not bigger: continue
                    s = min(bigger, key=lambda s: math.hypot(s[0] - px[0], s[1] - px[1])); cx, cy = s[0], s[1]
                A = max(pts, key=lambda q: math.hypot(q[0] - pt['pv'][0], q[1] - pt['pv'][1]))
                B = max(pts, key=lambda q: math.hypot(q[0] - A[0], q[1] - A[1]))
                if math.hypot(A[0] - B[0], A[1] - B[1]) < 40: continue
                near, far = (A, B) if math.hypot(A[0] - cx, A[1] - cy) < math.hypot(B[0] - cx, B[1] - cy) else (B, A)
                tol = max(30, .3 * math.hypot(A[0] - B[0], A[1] - B[1]))
                d = math.hypot(near[0] - pt['pv'][0], near[1] - pt['pv'][1])
                if d > tol:
                    n += 1; why = 'at the far end' if math.hypot(far[0] - pt['pv'][0], far[1] - pt['pv'][1]) <= tol else 'mid-part'
                    print(f'{slug} {uid} {pt["id"]}: pivot {pt["pv"][0]:.0f},{pt["pv"][1]:.0f} is {why}; body-side end is {near[0]:.0f},{near[1]:.0f}')
                    if fix:
                        # near is in page px (= drawing coords: svg viewBox maps 1:1)
                        changed = re.sub(r'(<g id="%s"[^>]*?)data-pivot="[^"]*"' % re.escape(pt['id']), lambda m: m.group(1) + 'data-pivot="%d %d"' % (round(pt['inv'][0] * near[0] + pt['inv'][2] * near[1] + pt['inv'][4]), round(pt['inv'][1] * near[0] + pt['inv'][3] * near[1] + pt['inv'][5])), changed, count=1)
            if fix and changed != svg: open(f, 'w', encoding='utf-8').write(changed)
        b.close()
    print(f'{slug} partaxis: {n} problem(s) ({WIG} wiggle = hard, {n - WIG} pivot-end = advisory: the body-side estimate is a heuristic; wing/feeler roots often read as false positives, look at motionaudit)'); return WIG if not STRICT else n
if __name__ == '__main__':
    a = [x for x in sys.argv[1:] if not x.startswith('--')]; slug = a[0]; sys.exit(1 if audit(slug, set(a[1:]) or None, '--fix' in sys.argv) else 0)
