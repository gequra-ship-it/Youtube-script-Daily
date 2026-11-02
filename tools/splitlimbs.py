# usage: python3 tools/splitlimbs.py <slug> [uid ...] [--dry]       (miya 2026-11-02: one data-pivot for a whole bundle of tentacles / arms / feelers swings the strands about the wrong point and they leave the body)
# Finds mv-joint groups whose name has a limb word (tentacle|arm|leg|feeler|antenna|whisker|filament|frond|claw|palp|tendril) and that hold SEVERAL separate strands (direct children)
# whose body-side ends are > 25 px apart, and splits the group into one mv-joint group per strand, each hinged at ITS OWN body-side end (the strand end nearest the creature body:
# centre of the sibling groups that share the name prefix, else the nearest bigger group). Amp/per are kept, the phase is staggered. Strands that share one root (<= 25 px) are left alone.
import os, sys, re, glob, math
import xml.etree.ElementTree as ET
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from paths import *
from playwright.sync_api import sync_playwright
LIMB = r'(tentacle|arm|leg|feeler|antenna|whisker|filament|frond|claw|palp|tendril)s?'
JS = r'''() => {
 const out = [], gs = [...document.querySelectorAll('g[id^="mv-joint-"]')];
 const box = g => { const r = g.getBoundingClientRect(); return [r.x + r.width / 2, r.y + r.height / 2, r.width * r.height]; };
 const allb = [...document.querySelectorAll('g[id^="mv-"]')].map(g => [g.id, ...box(g)]);
 for (const g of gs) {
   const name = g.id.replace(/^mv-joint-/, ''); const pm = name.match(/(^|-)(%LIMB%)(-|$|\d)/); if (!pm) continue;
   const kids = [...g.children].filter(e => /^(path|g|line|polyline|polygon)$/.test(e.tagName)); if (kids.length < 2) continue;
   const prefix = name.slice(0, pm.index).replace(/-$/, ''); const lim = new RegExp('(^|-)(%LIMB%)(-|$|\\d)');
   let sib = allb.filter(o => o[0] !== g.id && prefix && o[0].includes(prefix) && !lim.test(o[0].replace(/^mv-[a-z]+-/, '')));
   const gr = g.getBoundingClientRect(); let cx, cy;
   if (sib.length) { const tot = sib.reduce((a, o) => a + o[3], 0) || 1; cx = sib.reduce((a, o) => a + o[1] * o[3], 0) / tot; cy = sib.reduce((a, o) => a + o[2] * o[3], 0) / tot; }
   else { const px = [gr.x + gr.width / 2, gr.y + gr.height / 2]; const big = allb.filter(o => o[0] !== g.id && o[3] > gr.width * gr.height * 1.2 && o[3] < innerWidth * innerHeight * .6); if (!big.length) continue; const s = big.sort((a, b) => Math.hypot(a[1] - px[0], a[2] - px[1]) - Math.hypot(b[1] - px[0], b[2] - px[1]))[0]; cx = s[1]; cy = s[2]; }
   const ends = kids.map(k => { const ps = k.tagName === 'path' || k.tagName === 'line' ? [k] : [...k.querySelectorAll('path')]; if (!ps.length || !ps[0].getTotalLength) return null;
     const f = ps[0], l = ps[ps.length - 1], c0 = f.getCTM(), c1 = l.getCTM(); const a = f.getPointAtLength(0), b = l.getPointAtLength(l.getTotalLength());
     const A = new DOMPoint(a.x, a.y).matrixTransform(c0), B = new DOMPoint(b.x, b.y).matrixTransform(c1); return [A.x, A.y, B.x, B.y]; });
   const pc = g.getCTM(), inv = pc ? pc.inverse() : null;
   out.push({id: g.id, cx, cy, ends, inv: inv ? [inv.a, inv.b, inv.c, inv.d, inv.e, inv.f] : [1, 0, 0, 1, 0, 0]});
 }
 return out; }'''.replace('%LIMB%', LIMB)
def run(slug, uids=None, dry=False):
    vert = slug.endswith(tuple(f'short{i}' for i in range(1, 10))); W, H = (1080, 1920) if vert else (1920, 1080); total = 0
    ET.register_namespace('', 'http://www.w3.org/2000/svg'); ET.register_namespace('xlink', 'http://www.w3.org/1999/xlink')
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path=chrome(), args=['--no-sandbox']); pg = b.new_page(viewport={'width': W, 'height': H})
        for f in sorted(glob.glob(f'{REPO}/videos/{slug}/art3/U*.svg')):
            uid = os.path.basename(f)[:-4]
            if uids and uid not in uids: continue
            svg = open(f, encoding='utf-8').read(); pg.set_content(f'<html><body style="margin:0">{svg}</body></html>')
            pg.evaluate('()=>{const s=document.querySelector("svg");s.setAttribute("width",%d);s.setAttribute("height",%d)}' % (W, H)); res = pg.evaluate(JS)
            todo = []
            for r in res:
                pts = []
                for e in r['ends']:
                    if not e: pts.append(None); continue
                    a, bb = (e[0], e[1]), (e[2], e[3])
                    pts.append(a if math.hypot(a[0] - r['cx'], a[1] - r['cy']) <= math.hypot(bb[0] - r['cx'], bb[1] - r['cy']) else bb)
                ok = [q for q in pts if q]
                if len(ok) < 2: continue
                spread = max(math.hypot(a[0] - c[0], a[1] - c[1]) for a in ok for c in ok)
                if spread > 25: todo.append((r, pts, spread))
            if not todo: continue
            root = ET.fromstring(svg); parent = {c: p_ for p_ in root.iter() for c in p_}
            for r, pts, spread in todo:
                g = next((e for e in root.iter() if e.get('id') == r['id']), None)
                if g is None or g.get('transform'): print(f'{slug} {uid} {r["id"]}: skipped (has a transform)'); continue
                total += 1; print(f'{slug} {uid} {r["id"]}: {len(g)} strands, root spread {spread:.0f}px -> split into {len(g)} hinges')
                if dry: continue
                par = parent[g]; idx = list(par).index(g); par.remove(g); kids = list(g); inv = r['inv']
                base = re.sub(r'^mv-joint-', '', r['id']); base = re.sub(LIMB + r'$', lambda m: m.group(1), base)   # tentacles -> tentacle
                amp = g.get('data-amp'); per = g.get('data-per')
                for i, (k, q) in enumerate(zip(kids, pts)):
                    ng = ET.Element('{http://www.w3.org/2000/svg}g'); ng.set('id', f'mv-joint-{base}-{i + 1}')
                    if q: ng.set('data-pivot', '%d %d' % (round(inv[0] * q[0] + inv[2] * q[1] + inv[4]), round(inv[1] * q[0] + inv[3] * q[1] + inv[5])))
                    if amp: ng.set('data-amp', amp)
                    if per: ng.set('data-per', per)
                    ng.set('data-phase', '%.2f' % ((i * 0.9) % 6.28)); ng.append(k); par.insert(idx + i, ng)
            if not dry: open(f, 'w', encoding='utf-8').write(ET.tostring(root, encoding='unicode'))
        b.close()
    print(f'{slug} splitlimbs: {total} group(s)'); return total
if __name__ == '__main__':
    a = [x for x in sys.argv[1:] if not x.startswith('--')]; run(a[0], set(a[1:]) or None, '--dry' in sys.argv)
