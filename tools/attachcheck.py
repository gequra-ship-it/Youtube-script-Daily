# usage: python3 tools/attachcheck.py <slug> [uid ...]   (works on videos/<slug>/art3/*.svg, no build needed; exit 1 when something is flagged)
# Static check of every moving part against the rule "a hinge sits where the part touches the body" (guideline 4-7, art_spec 7 "Attachment rules", miya 2026-10-29):
#   JOINT/CHAIN/SWING/ROTOR with data-pivot : the pivot must lie ON the part (<= 12 px) AND ON the body/support it hangs from (<= 12 px; for chain/joint also the parent link)
#       -> windmill blades floating next to the tower, tails/legs/necks hinged in empty space, nets whose pole is not where the bag swings
#   ROTOR on a round face (clock, wheel, gear) : the pivot must be the centre of the smallest round shape that holds it (<= 12 px)
#   TOUCHING GEARS (two mv-rotor/spin gears whose rims are < 6 px apart or overlap) : pivots must be the gear centres and the rim distance must equal the radii sum (+-8 px)
#   MOVING CREATURE vs TAIL : a chain/joint group (tail, fin, leg) whose parent figure has NO moving group of its own is fine; but if the part's pivot body shape sits OUTSIDE every
#       mv-path/creep/swim/core group while the part itself is inside one, the body would stay while the tail moves -> flagged
#   AUTO-AXIS plants/signs/trees (mv-sway/tilt/swing-<tree|grass|reed|sign|post|pole|mast|flag|lamp|tower ...) : the group must not contain ground/shadow/water pieces wider than 1.6x its tallest
#       element's width (the base pivot would sit in the middle of the ground patch), and its box bottom must touch something below it
#   LABELS : a name/say label whose `to` point is within 45 px of a moving group but not inside it (+-12 px) would stay behind when the object moves
# --fix : labels pointing just beside a moving group (<= 45 px) get their pointer moved inside it (the .json is rewritten).
# Prints one line per problem: <slug> <uid> <group> <problem>.
import os, sys, json, glob
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from paths import *
from playwright.sync_api import sync_playwright
import axis_lib

JS = r'''
([W, H, uid]) => {
 const svg = document.querySelector('svg'); const NS = 'http://www.w3.org/2000/svg';
 const SH = 'path,circle,ellipse,rect,polygon,polyline,line';
 const out = [];
 const all = [...svg.querySelectorAll(SH)].filter(e => !e.closest('defs,clipPath,mask,pattern,marker,symbol'));
 const bbs = new Map(); const bb = e => { if (!bbs.has(e)) { try { bbs.set(e, e.getBBox()); } catch (x) { bbs.set(e, {x:0,y:0,width:0,height:0}); } } return bbs.get(e); };
 const rootCTM = svg.getScreenCTM();
 const scr = (e) => { // element bbox in picture coords (axis-aligned, via CTM)
   const b = bb(e), m = e.getScreenCTM(); const inv = rootCTM.inverse(); const M = inv.multiply(m); const P = [[b.x,b.y],[b.x+b.width,b.y],[b.x,b.y+b.height],[b.x+b.width,b.y+b.height]].map(([x,y]) => new DOMPoint(x,y).matrixTransform(M));
   const xs = P.map(p=>p.x), ys = P.map(p=>p.y); return {x:Math.min(...xs), y:Math.min(...ys), w:Math.max(...xs)-Math.min(...xs), h:Math.max(...ys)-Math.min(...ys)}; };
 const BGRE = /(^|[-_ ])(bg|backdrop|sky|haze|mist|fog|vignette|background)([-_ ]|$)/i;
 const isBig = e => { const s = scr(e); return s.w * s.h > 0.25 * W * H; };
 const isBg = e => isBig(e) || (e.closest('[id]') && [...(function*(){ let n = e; while (n && n !== svg) { if (n.id) yield n.id; n = n.parentNode; } })()].some(i => BGRE.test(i)));
 const paintable = (e) => { const cs = getComputedStyle(e); return {fill: cs.fill !== 'none' && cs.fillOpacity !== '0' && !/^url/.test('') , stroke: cs.stroke !== 'none' && parseFloat(cs.strokeWidth) > 0}; };
 const hit = (e, x, y) => { // point (picture coords) on element e (fill or stroke)?
   const m = e.getScreenCTM(); if (!m) return false; const q = new DOMPoint(x, y).matrixTransform(rootCTM).matrixTransform(m.inverse()); const cs = getComputedStyle(e);
   try { if (cs.fill !== 'none' && e.tagName !== 'line' && e.tagName !== 'polyline' && e.isPointInFill(q)) return true; } catch (z) {}
   try { if (cs.stroke !== 'none' && e.isPointInStroke(q)) return true; } catch (z) {}
   return false; };
 const R = [0, 3, 6, 9, 12, 18, 26, 40], DIR = 12;
 const dist = (set, x, y, maxr) => { for (const r of R) { if (r > maxr) break; const n = r === 0 ? 1 : DIR; for (let k = 0; k < n; k++) { const a = 2 * Math.PI * k / DIR, px = x + r * Math.cos(a), py = y + r * Math.sin(a);
     for (const e of set) if (hit(e, px, py)) return r; } } return 999; };
 const kindOf = id => (id.match(/^mv-([a-z]+)/) || [])[1];
 const groups = [...svg.querySelectorAll('[id^="mv-"]')];
 const shapesIn = g => [...g.querySelectorAll(SH)].filter(e => !e.closest('defs,clipPath,mask,pattern,marker,symbol'));
 const pvOf = g => { const a = (g.getAttribute('data-pivot') || '').trim().split(/\s+/).map(Number); if (a.length !== 2 || a.some(isNaN)) return null;
   // picture coords, or inner coords of the parent (the build accepts both and takes the one nearer the part)
   const part = shapesIn(g); const near = (x, y) => { let d = 1e9; for (const e of part) { const s = scr(e); d = Math.min(d, Math.hypot(Math.max(s.x - x, 0, x - s.x - s.w), Math.max(s.y - y, 0, y - s.y - s.h))); } return d; };
   const pm = g.parentNode.getScreenCTM ? g.parentNode.getScreenCTM() : null; let alt = null; if (pm) { const q = new DOMPoint(a[0], a[1]).matrixTransform(pm).matrixTransform(rootCTM.inverse()); alt = [q.x, q.y]; }
   if (alt && near(alt[0], alt[1]) + 4 < near(a[0], a[1])) return alt; return a; };
 const HINGE = new Set(['joint', 'chain', 'swing', 'rotor', 'pendulum', 'shackle', 'flap', 'wiggle']);
 const MOVER = /^mv-(path|creep|swim|rollby|hop|float|hover|core-(glide|orbit|drop|sway|wobble|drift|roll|spin|flip|tremble)|skid|slide|toss|magnet|bouncing)/;   // a flicker / pulse / reveal 'core' stays in place
 for (const g of groups) {
   const kind = kindOf(g.id); const part = shapesIn(g); if (!part.length) continue; const pv = pvOf(g);
   const body = all.filter(e => !g.contains(e) && !isBg(e));
   if (pv && HINGE.has(kind)) {
     const dp = dist(part, pv[0], pv[1], 12), db = dist(body, pv[0], pv[1], 12);
     if (dp > 12) out.push([g.id, `pivot (${pv.map(Math.round)}) is ${dp > 40 ? 'far' : '>12px'} from the part itself`]);
     else if (db > 12 && !part.some(e => e.tagName === 'circle' && scr(e).w < 40 && hit(e, pv[0], pv[1])) && !(pv[0] <= 2 || pv[1] <= 2 || pv[0] >= W - 2 || pv[1] >= H - 2)) out.push([g.id, `pivot (${pv.map(Math.round)}) lies in empty space: no body/support shape within 12 px (part would hinge away from the body; put the pivot where it touches the body, or move the part onto the body)`]);
     if (kind === 'rotor' && dp <= 12 && !/gear|cog|sprocket/i.test(g.id)) { // round face: pivot must be its centre
       let best = null; for (const e of body) { const t = e.tagName; if (!(t === 'circle' || t === 'ellipse')) continue; if (!hit(e, pv[0], pv[1])) continue; const s = scr(e); if (s.w > 0.6 * W) continue; if (!best || s.w * s.h < best.a) best = {a: s.w * s.h, cx: s.x + s.w / 2, cy: s.y + s.h / 2, id: e.parentNode.id || e.id}; }
       if (best && Math.hypot(best.cx - pv[0], best.cy - pv[1]) > 12) out.push([g.id, `rotor pivot is ${Math.round(Math.hypot(best.cx - pv[0], best.cy - pv[1]))} px off the centre (${Math.round(best.cx)},${Math.round(best.cy)}) of the round face it turns on`]);
     }
   }
   // tail / leg / neck whose body stays still while the part is inside a mover
   if (pv && (kind === 'chain' || kind === 'joint')) {
     let inMover = false; for (let a = g.parentNode; a && a !== svg; a = a.parentNode) if (a.id && MOVER.test(a.id)) inMover = true;
     if (!inMover) { // body shapes touching the pivot: are they inside some mover group?
       const bodyHit = body.filter(e => hit(e, pv[0], pv[1]) || dist([e], pv[0], pv[1], 12) < 999);
       const anyMoverAround = groups.some(m => MOVER.test(m.id) && m !== g && !g.contains(m) && bodyHit.some(e => m.contains(e)));
       if (anyMoverAround && !inMover) out.push([g.id, 'the body it hangs from moves (mv-path/creep/swim/core) but this part is outside that group: the body would travel without its tail/leg/neck; put the part INSIDE the moving group']);
     }
   }
   // plants/signs/trees with auto axis: only the thing itself in the group
   if (!pv && /^mv-(core-)?(sway|tilt|swing|pendulum|wobble)-/.test(g.id) && /(^|-)(tree|trees|grass|reed|reeds|sign|signpost|post|pole|mast|lamp|tower|flower|plant|bush|stalk|cattail|palm|flag|fence)(-|$)/i.test(g.id)) {
     const s = (() => { let x0 = 1e9, y0 = 1e9, x1 = -1e9, y1 = -1e9; for (const e of part) { const t = scr(e); x0 = Math.min(x0, t.x); y0 = Math.min(y0, t.y); x1 = Math.max(x1, t.x + t.w); y1 = Math.max(y1, t.y + t.h); } return {x: x0, y: y0, w: x1 - x0, h: y1 - y0}; })();
     let widest = 0; for (const e of part) { const t = scr(e); if (t.h > 0.5 * s.h) widest = Math.max(widest, t.w); }
     if (s.w > 1.6 * Math.max(widest, 0.35 * s.h) && s.w > 160) out.push([g.id, `group is ${Math.round(s.w)} px wide but the ${g.id.split('-').pop()} itself is only about ${Math.round(Math.max(widest, 1))} px: ground/shadow/water pieces inside it move the base pivot away from the trunk/stem; keep only the plant/sign in the group`]);
     const below = all.filter(e => !g.contains(e) && !isBg(e)).some(e => { const t = scr(e); return t.y <= s.y + s.h + 14 && t.y + t.h >= s.y + s.h - 14 && t.x <= s.x + s.w && t.x + t.w >= s.x; });
     if (!below && s.y + s.h < H - 120) out.push([g.id, 'its bottom edge (base pivot) touches nothing: the plant/sign floats; extend it to the ground or add the ground piece (outside the group)']);
   }
 }
 // touching gears
 const gears = groups.filter(g => /^mv-(rotor|spin|core-spin|core-turn)-.*(gear|cog|sprocket)/i.test(g.id) || /gear|cog|sprocket/i.test(g.id) && /^mv-(rotor|spin|core)/.test(g.id));
 const gb = gears.map(g => { let x0 = 1e9, y0 = 1e9, x1 = -1e9, y1 = -1e9; for (const e of shapesIn(g)) { const t = scr(e); x0 = Math.min(x0, t.x); y0 = Math.min(y0, t.y); x1 = Math.max(x1, t.x + t.w); y1 = Math.max(y1, t.y + t.h); } return {g, cx: (x0 + x1) / 2, cy: (y0 + y1) / 2, r: Math.max(x1 - x0, y1 - y0) / 2, pv: pvOf(g)}; });
 for (const a of gb) { if (a.pv && Math.hypot(a.pv[0] - a.cx, a.pv[1] - a.cy) > 12) out.push([a.g.id, `gear pivot (${a.pv.map(Math.round)}) is ${Math.round(Math.hypot(a.pv[0] - a.cx, a.pv[1] - a.cy))} px off the gear centre (${Math.round(a.cx)},${Math.round(a.cy)})`]); }
 for (let i = 0; i < gb.length; i++) for (let j = i + 1; j < gb.length; j++) { const a = gb[i], b = gb[j], d = Math.hypot(a.cx - b.cx, a.cy - b.cy), gap = d - a.r - b.r;
   if ((gap > 8 && gap < 40) || (gap < -0.3 * Math.min(a.r, b.r))) out.push([a.g.id + ' + ' + b.g.id, `neighbouring gears do not mesh: rim gap ${Math.round(gap)} px (should be 0 +-8, or overlap by about one tooth depth: centres ${Math.round(d)} px apart, radii ${Math.round(a.r)} + ${Math.round(b.r)})`]); }
 // moving things that should be one rigid piece: a swing group whose pivot is outside its own box by > 60 px (pole + bag) -> flag (net pole + bag)
 for (const g of groups) { if (kindOf(g.id) !== 'swing') continue; const pv = pvOf(g); if (!pv) continue; const part = shapesIn(g); let x0 = 1e9, y0 = 1e9, x1 = -1e9, y1 = -1e9; for (const e of part) { const t = scr(e); x0 = Math.min(x0, t.x); y0 = Math.min(y0, t.y); x1 = Math.max(x1, t.x + t.w); y1 = Math.max(y1, t.y + t.h); }
   const d = Math.hypot(Math.max(x0 - pv[0], 0, pv[0] - x1), Math.max(y0 - pv[1], 0, pv[1] - y1)); if (d > 30) out.push([g.id, `swing pivot is ${Math.round(d)} px outside its group: the thing swings about a point that is not part of it (the handle/pole must be in the group, or hinge at the junction)`]); }
 return out;
}
'''

def main():
    global FIX; FIX = '--fix' in sys.argv; args = [a for a in sys.argv[1:] if a != '--fix']; slug = args[0]; uids = args[1:]
    vert = slug.endswith(tuple(f'short{i}' for i in range(1, 10)))
    W, H = (1080, 1920) if vert else (1920, 1080)
    d = f'{vdir(slug)}/art3'; files = sorted(glob.glob(d + '/U*.svg'))
    if uids: files = [f for f in files if os.path.basename(f)[:-4] in uids]
    bad = 0
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path=chrome(), args=['--no-sandbox']); pg = b.new_page(viewport={'width': W, 'height': H})
        for f in files:
            uid = os.path.basename(f)[:-4]; svg = open(f).read()
            pg.set_content(f'<body style="margin:0">{svg}</body>')
            for gid, msg in pg.evaluate(JS, [W, H, uid]): print(slug, uid, gid, msg); bad += 1
            # the axis catalogue (tools/axis_lib.py, 2026-10-29): the thing named in the group decides where its axis is and which kinds fit; a written pivot off that axis / a rotating water / a missing pivot is a problem
            for msg in axis_lib.problems_of(axis_lib.resolve(pg, svg, W, H)): print(slug, uid, 'catalogue', msg); bad += 1
            # labels that sit near a moving group but outside it
            try: sc = json.load(open(f[:-4] + '.json'))
            except Exception: sc = {}
            labs = sc.get('labels') or []; fixed_labels = False
            if labs:
                boxes = pg.evaluate('''() => [...document.querySelectorAll('[id^="mv-"]')].filter(g => /^mv-(path|creep|swim|rollby|hop|float|hover|slide|scroll|toss|skid|rise|bob|magnet|bouncing|drip|circle|ascend|sink|core-(glide|orbit|drop|pop))/.test(g.id)).map(g => { const b = g.getBBox(), m = g.getScreenCTM(), r = document.querySelector('svg').getScreenCTM().inverse().multiply(m); const P = [[b.x,b.y],[b.x+b.width,b.y],[b.x,b.y+b.height],[b.x+b.width,b.y+b.height]].map(([x,y]) => new DOMPoint(x,y).matrixTransform(r)); const xs = P.map(q=>q.x), ys = P.map(q=>q.y); return [g.id, Math.min(...xs), Math.min(...ys), Math.max(...xs), Math.max(...ys)]; })''')
                for L in labs:
                    to = L.get('to') or ([L.get('x'), L.get('y')] if L.get('x') is not None else None)
                    if not to or None in to: continue
                    x, y = to
                    inside = [bx for bx in boxes if bx[1] - 12 <= x <= bx[3] + 12 and bx[2] - 12 <= y <= bx[4] + 12]
                    if inside: continue
                    near = [bx for bx in boxes if bx[1] - 45 <= x <= bx[3] + 45 and bx[2] - 45 <= y <= bx[4] + 45]   # farther than 45 px = a different, standing thing

                    if near and FIX:   # --fix: move the pointer inside the moving group (nearest point of its box, pulled 20 px in) so the label travels with it
                        bx = near[0]; nx = min(max(x, bx[1] + 20), bx[3] - 20) if bx[3] - bx[1] > 40 else (bx[1] + bx[3]) / 2; ny = min(max(y, bx[2] + 20), bx[4] - 20) if bx[4] - bx[2] > 40 else (bx[2] + bx[4]) / 2
                        L['to'] = [round(nx), round(ny)]; fixed_labels = True; print(slug, uid, near[0][0], f"label moved to ({round(nx)},{round(ny)}) inside the moving group"); continue
                    if near: print(slug, uid, near[0][0], f"label {L.get('t') or L.get('text') or L.get('kind') or ''!r} points at ({round(x)},{round(y)}), {round(max(0, near[0][1]-x, x-near[0][3], near[0][2]-y, y-near[0][4]))} px beside this moving group: it will NOT follow it; move `to` inside the group's box"); bad += 1
                if fixed_labels: json.dump(sc, open(f[:-4] + '.json', 'w'), indent=1, ensure_ascii=False)
        b.close()
    print(slug, 'attachcheck:', len(files), 'units,', bad, 'problems'); sys.exit(1 if bad else 0)

FIX = False
main()
