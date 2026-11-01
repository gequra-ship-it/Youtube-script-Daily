# usage: python3 tools/scalefix.py <slug>... [--report]          (library: scalefix.plan(svg_text, W, H, names, centre) used by build3)
# (2026-11-01 miya) A BALANCE SCALE (천칭) must move like one: ONLY the beam turns, about the middle of the beam; the pans hang from the beam ends and stay upright (they go up and
# down and a hair sideways, never tilt, never slide off the string); the stand / hook line / hanging point never moves. The old pictures were one group swung as a pendulum from the
# hook (mv-swing-scale, mv-tilt-balance-scale ...): the pans tilted with the beam and slid sideways, the stand rotated, "the pans came off the beam".
# plan() looks at the DIRECT children of a scale group in the rendered picture and sorts them:
#   beam    the widest flat child (+ the hub jewel on it + loads that sit on top of a see-saw beam) -> rotates about the beam centre
#   hang L/R  children below the beam on the left / right (strings, bowls, things in the bowls)   -> follow the beam end (x, y), no rotation
#   static  hook line / hanging dot above the beam in the middle, stand / pillar below it in the middle -> never move
# build3 then emits one seek-safe proxy tween (fxlib miyaScaleP/miyaScaleM). Nothing is rewritten in the art files. Groups whose structure cannot be read (no flat beam) keep the
# old motion. --report prints the plan of every scale group of a video.
import os, re, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

NAME = re.compile(r'(^|-)(scales?|balance|libra|seesaw|teeter|weighing)(-|$)')
BEAMY = re.compile(r'(^|-)(beam|bar|plank|arm)(-|$)')
KINDS = re.compile(r'^mv-(swing|tilt|joint|chain|sway|wobble|pendulum|core-(sway|wobble|swing|tilt)|rotor)-')
CENTRE = re.compile(r'balance scale|scales? of justice|seesaw|see-saw|weighing scale|\bscales\b|libra', re.I)

JS = r'''
([names, W, H]) => {
 const svg = document.querySelector('svg'); const out = [];
 const frame = (g, el, b) => { const M = g.parentNode.getCTM().inverse().multiply(el.getCTM());
   const P = [[b.x, b.y], [b.x + b.width, b.y], [b.x, b.y + b.height], [b.x + b.width, b.y + b.height]].map(([x, y]) => new DOMPoint(x, y).matrixTransform(M));
   const xs = P.map(p => p.x), ys = P.map(p => p.y); const x0 = Math.min(...xs), x1 = Math.max(...xs), y0 = Math.min(...ys), y1 = Math.max(...ys);
   return {cx: (x0 + x1) / 2, cy: (y0 + y1) / 2, w: x1 - x0, h: y1 - y0, x0, x1, y0, y1}; };
 for (const [name, kk] of names) {
   const g = svg.querySelectorAll('.' + CSS.escape(name))[kk]; if (!g) continue;
   const kids = [...g.children]; const info = kids.map((el, i) => {
     if (/^(defs|style|title|desc|lineargradient|radialgradient|clippath|mask|pattern|filter)$/i.test(el.tagName)) return null;
     let b; try { b = el.getBBox(); } catch (e) { return null; } if (!(b.width + b.height)) return null;
     const f = frame(g, el, b); const cs = getComputedStyle(el); f.i = i; f.tag = el.tagName; f.fill = cs.fill; return f; });
   const ok = info.filter(Boolean); if (ok.length < 3) continue;
   const x0 = Math.min(...ok.map(f => f.x0)), x1 = Math.max(...ok.map(f => f.x1)), y0 = Math.min(...ok.map(f => f.y0)), y1 = Math.max(...ok.map(f => f.y1));
   const Wt = x1 - x0, Ht = y1 - y0;
   const flat = ok.filter(f => f.w > 0.4 * Wt && f.h < 0.16 * f.w);
   if (!flat.length) { out.push({name, kk, err: 'no flat beam child'}); continue; }
   flat.sort((a, b) => b.w - a.w); const beam = flat[0];
   let cx = beam.cx, cy = beam.cy;
   // a small round hub on the beam centre is the real pivot
   const hub = ok.find(f => f.tag.toLowerCase() === 'circle' && f.w < 0.08 * Wt + 12 && Math.hypot(f.cx - beam.cx, f.cy - beam.cy) < 0.06 * Wt + 12 && f !== beam);
   if (hub) { cx = hub.cx; cy = hub.cy; }
   const near = 0.14 * Wt, tol = Math.max(8, 0.012 * Ht);
   const cls = {beam: [beam.i], L: [], R: [], stat: []};
   for (const f of ok) { if (f === beam) continue;
     const dx = f.cx - cx;
     if (Math.abs(dx) < near) { if (Math.abs(f.cy - cy) <= tol + f.h / 2 && f.h < 0.1 * Ht + 30) cls.beam.push(f.i); else cls.stat.push(f.i); }
     else if (f.cy < cy - tol) cls.beam.push(f.i);               // a load standing on the beam end (see-saw)
     else (dx < 0 ? cls.L : cls.R).push(f.i); }
   const mid = side => { const m = ok.filter(f => cls[side].includes(f.i)); if (!m.length) return null; const a = Math.min(...m.map(f => f.x0)), z = Math.max(...m.map(f => f.x1)); return (a + z) / 2; };
   const lx = mid('L'), rx = mid('R');
   out.push({name, kk, cx, cy, beam: cls.beam, L: cls.L, R: cls.R, stat: cls.stat, rl: lx === null ? 0 : lx - cx, rr: rx === null ? 0 : rx - cx, Wt, Ht});
 }
 return out;
}
'''

_PW = {}


def _page():
    if 'pg' not in _PW:
        from paths import chrome
        from playwright.sync_api import sync_playwright
        _PW['p'] = sync_playwright().start(); _PW['b'] = _PW['p'].chromium.launch(executable_path=chrome(), args=['--no-sandbox']); _PW['pg'] = _PW['b'].new_page()
    return _PW['pg']


def is_scale(name, centre=''):
    """True when the mv- group id is an oscillating balance-scale / see-saw group"""
    if not KINDS.match(name): return False
    tail = re.sub(r'^mv-(core-)?[a-z]+-', '', name)
    return bool(NAME.search(tail)) or bool(BEAMY.search(tail) and CENTRE.search(centre or ''))


def plan(svg_text, W, H, names):
    """names = [(class name, occurrence index)] -> {(name, kk): plan or None}; plan = {cx, cy, beam, L, R, rl, rr} in the group's parent frame"""
    if not names: return {}
    pg = _page(); pg.set_viewport_size({'width': W, 'height': H}); pg.set_content('<body style="margin:0">' + svg_text + '</body>')
    res = pg.evaluate(JS, [[list(n) for n in names], W, H]); out = {}
    for r in res:
        out[(r['name'], r['kk'])] = None if r.get('err') else r
    return out


def main(slugs):
    from paths import REPO
    n = 0
    for slug in slugs:
        d = f'{REPO}/videos/{slug}/art3'; W, H = (1080, 1920) if 'short' in slug else (1920, 1080)
        for fn in sorted(os.listdir(d)) if os.path.isdir(d) else []:
            if not fn.endswith('.svg'): continue
            t = open(f'{d}/{fn}', encoding='utf-8').read(); centre = ''
            jf = f'{d}/{fn[:-4]}.json'
            if os.path.exists(jf):
                try: centre = json.load(open(jf)).get('centre') or ''
                except Exception: pass
            ids = re.findall(r'\bid="(mv-[A-Za-z0-9_-]+)"', t)
            # the report loads the raw picture, so the ids stand in for the classes build3 sees
            names = []; svg = re.sub(r'\bid="(mv-[A-Za-z0-9_-]+)"', lambda m: f'class="{m.group(1)}"', t)
            seen = {}
            for i in ids:
                kk = seen.get(i, 0); seen[i] = kk + 1
                if is_scale(i, centre): names.append((i, kk))
            for k, v in plan(svg, W, H, names).items():
                n += 1
                if v is None: print(f'{slug} {fn[:-4]} {k[0]}: no readable beam (old motion kept)')
                else: print(f'{slug} {fn[:-4]} {k[0]}: beam hub ({v["cx"]:.0f},{v["cy"]:.0f}) beam {v["beam"]} left {v["L"]} right {v["R"]} static {v["stat"]} pan offsets {v["rl"]:.0f}/{v["rr"]:.0f}')
    print(f'scalefix: {n} scale group(s)')
    if 'p' in _PW: _PW['b'].close(); _PW['p'].stop()


if __name__ == '__main__':
    a = [x for x in sys.argv[1:] if not x.startswith('--')]
    from paths import REPO
    main(a or sorted(os.listdir(f'{REPO}/videos')))
