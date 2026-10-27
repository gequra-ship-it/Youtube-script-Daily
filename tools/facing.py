# -*- coding: utf-8 -*-
# Direction sanity for travelling objects (2026-10-27, miya: "the fish in the whale video swims backwards; check direction and interactions
# everywhere, not only the axes"). A creature or vehicle that travels sideways must move the way it faces.
#   facing  = data-face="left|right" on the group, else the EYES: small filled circles/ellipses inside the group; their mean x against the
#             group's centre (>= 12 % of the width off centre) says which way the head points. No eyes, no attribute -> unknown, left alone.
#   travel  = path: first -> last point of data-path (x change >= 40 px and >= 35 % of the path's extent, else "mostly vertical", left alone);
#             swim / rollby / creep: sign of data-dist (default +); scroll: -data-dist; magnet: data-dx.
#   fix     = facing and travel disagree -> the DRAWING is mirrored about its body centre (a wrapper <g> inside the group; inner data-pivot x
#             mirrored too). The travel, the composition and whatever the object moves toward stay as drawn. miyaPath turns relative to the
#             start tangent, so a mirrored sprite stays upright. The frog is injected later and faces the travel (frog_place).
#   eyeless pointed things (rocket, arrow, ship, probe ...; POINTED names): the narrower end of the body outline is the front ('taper').
#   context(): per picture -> travel (sign of the widest travelling group), wind (sidecar "wind", else against the travel, else left->right),
#             attractor (centre of a hole / vortex / magnet / drain group, or sidecar "attractor": [x, y]) -- build3 turns particles, wind lines,
#             rain slant, fog drift and the drift camera with it; frog_place puts the pushing frog on the back side.
#   apply() also: mv-magnet-* pulled TOWARD the attractor (data-dx/dy), paths named sink/fall/drop/... must end lower (rise/ascend/... higher),
#             paths toward an attractor must end nearer to it (else the path is reversed when it is a plain M/L/C/Q path).
# Used by build3 (facing.compute -> context / apply on the inlined SVG, log "direction sanity") and by frog_place (travel_sign).
import os, re, json
import sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
TRAVEL = ('path', 'swim', 'rollby', 'creep', 'magnet', 'slide')   # scroll = a background layer, no facing
POINTED = re.compile(r'rocket|arrow|dart|missile|probe|plane|jet|torpedo|comet|spear|needle|pencil|bullet|shuttle|lander|voyager|pioneer|ship|boat|canoe|kayak|sub\b|submarine|sled|train|car\b|bus\b|truck|bike', re.I)
ATTR = re.compile(r'hole|^bh|black(?!board)|singular|vortex|whirl|drain|magnet|gravity|(?<!s)well$|funnel|mouth|maw|attract|sun$|star$', re.I)
DOWNN = re.compile(r'sink|fall|drop|descend|plunge|dive|settle', re.I)  # direction verbs only; vehicle names (lander, carcass) say nothing about the path
UPN = re.compile(r'rise|ascend|climb|launch|lift|soar|up\b|bubble|float|balloon|escape', re.I)
TOWARDN = re.compile(r'pull|suck|spiral|drain|inward|toward|into|capture|fall-?in|plunge', re.I)
NUM = r'-?\d*\.?\d+(?:e-?\d+)?'
# second round (miya 2026-10-27 "자동 아닌 것도 규격화", guideline 4-4 B): gears mesh, flags/smoke lean with the wind, drawn characters look at the focus, shadows sit away from the light, the frog orbits the way the whirl spins
GEAR = re.compile(r'gear|cog|sprocket', re.I)
FLAG = re.compile(r'flag|banner|pennant|windsock|sail\b|streamer', re.I)
LEAN = re.compile(r'smoke|steam|plume|exhaust|hair|scarf|cape|spray|mane|vapou?r|mist|grass|reed|wheat|kelp|seaweed|flame|fire\b|torchfire|candle', re.I)
GAZE = re.compile(r'person|people|crowd|\bman\b|woman|human|figure|\bkid|child|\bboy|girl|scientist|astronaut|sailor|farmer|hunter|villager|monk|doctor|nurse|chef|worker|student|teacher|king|queen|knight|soldier|explorer|diver|pilot|\bface|\bhead|\bowl\b|\bcat|\bdog|bear|\bfox|wolf|deer|horse|\bcow|bird|whale|shark|fish|lion|tiger|mouse|rabbit|monkey|penguin|turtle|octopus|dolphin|eagle|crow\b|snake|lizard|dino', re.I)
LIGHT = re.compile(r'\bsun\b|sun$|lamp|lantern|candle|torch|moon|bulb|fire\b|flame|campfire|spotlight|headlight|window', re.I)
SHADOWN = re.compile(r'shadow|shade', re.I); HILITEN = re.compile(r'highlight|glint|shine|specular|rim-?light', re.I)
CACHE_V = 'v2'


def kind_of(gid):
    m = re.match(r'mv-([a-z]+)-', gid or '')
    return m.group(1) if m else None


def path_ends(d):
    """(x0, y0, x1, y1, xmin, xmax) of a path's drawn points (absolute commands as agents write them; relative ones accumulated roughly)"""
    pts = []; cur = (0.0, 0.0); start = None
    for cmd, args in re.findall(r'([MmLlHhVvCcSsQqTtAaZz])([^MmLlHhVvCcSsQqTtAaZz]*)', d):
        nums = [float(x) for x in re.findall(NUM, args)]
        rel = cmd.islower(); c = cmd.upper()
        if c == 'Z':
            if start: cur = start
            continue
        if c == 'H':
            for v in nums: cur = ((cur[0] + v) if rel else v, cur[1]); pts.append(cur)
            continue
        if c == 'V':
            for v in nums: cur = (cur[0], (cur[1] + v) if rel else v); pts.append(cur)
            continue
        step = {'M': 2, 'L': 2, 'T': 2, 'C': 6, 'S': 4, 'Q': 4, 'A': 7}[c]
        for i in range(0, len(nums) - step + 1, step):
            x, y = nums[i + step - 2], nums[i + step - 1]
            cur = ((cur[0] + x) if rel else x, (cur[1] + y) if rel else y); pts.append(cur)
            if c == 'M' and start is None: start = cur
    if len(pts) < 2: return None
    xs = [p[0] for p in pts]
    return pts[0][0], pts[0][1], pts[-1][0], pts[-1][1], min(xs), max(xs)


def mirror_path(d, cx):
    """the same path mirrored about x = cx (absolute x -> 2cx - x, relative dx -> -dx, arc sweep flag flipped)"""
    out = []
    for cmd, args in re.findall(r'([MmLlHhVvCcSsQqTtAaZz])([^MmLlHhVvCcSsQqTtAaZz]*)', d):
        nums = [float(x) for x in re.findall(NUM, args)]
        rel = cmd.islower(); c = cmd.upper(); o = []
        if c == 'Z': out.append(cmd); continue
        if c == 'V': o = nums
        elif c == 'H': o = [(-v if rel else 2 * cx - v) for v in nums]
        elif c == 'A':
            for i in range(0, len(nums) - 6, 7):
                rx, ry, rot, la, sw, x, y = nums[i:i + 7]
                o += [rx, ry, -rot, la, 1 - sw, (-x if rel else 2 * cx - x), y]
        else:
            for i, v in enumerate(nums): o.append(v if i % 2 else (-v if rel else 2 * cx - v))
        out.append(cmd + ' '.join(f'{v:g}' for v in o))
    return ' '.join(out)


def travel_sign(tag):
    """+1 right / -1 left / 0 unknown or mostly vertical, from one <g ...> start tag of a travelling group"""
    gid = re.search(r'\bid="([^"]+)"', tag); kind = kind_of(gid.group(1) if gid else '')
    def f(k, dflt):
        m = re.search(rf'\bdata-{k}="({NUM})"', tag); return float(m.group(1)) if m else dflt
    if kind == 'path':
        m = re.search(r'\bdata-path="([^"]*)"', tag); e = path_ends(m.group(1)) if m else None
        if not e: return 0
        dx = e[2] - e[0]; ext = max(e[5] - e[4], 1)
        return 0 if abs(dx) < 40 or abs(dx) < .35 * ext else (1 if dx > 0 else -1)
    if kind in ('swim', 'rollby', 'creep'): return 1 if f('dist', {'swim': 400, 'rollby': 600, 'creep': 60}[kind]) > 0 else -1
    if kind == 'scroll': return -1 if f('dist', 160) > 0 else 1
    if kind == 'magnet': v = f('dx', -200); return 0 if v == 0 else (1 if v > 0 else -1)
    if kind == 'slide':   # enters from data-dx (default -960 = from the left, moving right); data-dir="out" leaves toward data-dx
        v = f('dx', -960); out = 'data-dir="out"' in tag
        if abs(v) < 40: return 0
        return (1 if v > 0 else -1) if out else (-1 if v > 0 else 1)
    return 0


JS = r"""() => {
  const svg = document.querySelector('svg'); if (!svg) return {groups: [], boxes: {}, shadows: []};
  const lum = c => { const m = (c || '').match(/\d+(\.\d+)?/g); if (!m || m.length < 3) return 1; return (0.299*m[0] + 0.587*m[1] + 0.114*m[2]) / 255; };
  const inLocal = (g, el, x, y) => { const p = svg.createSVGPoint(); p.x = x; p.y = y; return p.matrixTransform(g.getCTM().inverse().multiply(el.getCTM())); };
  const toRoot = (el, b) => { const m = el.getCTM(); const p = svg.createSVGPoint(); p.x = b.x; p.y = b.y; const q = p.matrixTransform(m); p.x = b.x + b.width; p.y = b.y + b.height; const q2 = p.matrixTransform(m); return [Math.min(q.x, q2.x), Math.max(q.x, q2.x), Math.min(q.y, q2.y), Math.max(q.y, q2.y)]; };
  const TRAVEL = ['path','swim','rollby','creep','magnet','slide'];
  const GAZE = /person|people|crowd|\bman\b|woman|human|figure|\bkid|child|\bboy|girl|scientist|astronaut|sailor|farmer|hunter|villager|monk|doctor|nurse|chef|worker|student|teacher|king|queen|knight|soldier|explorer|diver|pilot|\bface|\bhead|\bowl\b|\bcat|\bdog|bear|\bfox|wolf|deer|horse|\bcow|bird|whale|shark|fish|lion|tiger|mouse|rabbit|monkey|penguin|turtle|octopus|dolphin|eagle|crow\b|snake|lizard|dino/i;
  const LEAN = /smoke|steam|plume|exhaust|hair|scarf|cape|spray|mane|vapou?r|mist|grass|reed|wheat|kelp|seaweed|flame|fire\b|torchfire|candle/i;
  const FLAG = /flag|banner|pennant|windsock|sail\b|streamer/i;
  const opac = (e, g) => { const cs = getComputedStyle(e); if (!cs.fill || cs.fill === 'none') return 0; let op = 1, n = e; while (n && n !== g) { op *= parseFloat(getComputedStyle(n).opacity || 1); n = n.parentElement; } return op * parseFloat(cs.fillOpacity || 1); };
  const roleOf = g => { const k = (g.id.match(/^mv-([a-z]+)-/) || [])[1]; if (TRAVEL.includes(k)) return 'travel'; if (['chain','joint','limb','rotor','fill','grow','ticks'].includes(k)) return null; if (FLAG.test(g.id)) return 'flag'; if (LEAN.test(g.id)) return 'lean'; if (GAZE.test(g.id)) return 'gaze'; return null; };
  const out = [];
  for (const g of document.querySelectorAll('g[id]')) {
    const role = roleOf(g); if (!role) continue;
    if (g.closest('[id^="fg"]')) continue;
    if (role !== 'travel') { let a = g.parentElement, nest = false; while (a && a.tagName === 'g') { if (a.id && roleOf(a)) { nest = true; break; } a = a.parentElement; } if (nest) continue; }
    const gb = g.getBBox(); if (gb.width < 20 || gb.height < 4) continue;
    // body = the largest opaque filled shape (beams, glows and shadows are translucent); pupils = small DARK filled circles inside the body's x range
    let body = null, bodyEl = null, area = 0, pole = null, poleW = 0;
    for (const e of g.querySelectorAll('path,ellipse,rect,circle,polygon')) {
      if (e.closest('[id^="fg"]')) continue;
      const op = opac(e, g); if (op < 0.5) continue;
      const b = e.getBBox(); const q0 = inLocal(g, e, b.x, b.y), q1 = inLocal(g, e, b.x + b.width, b.y + b.height);
      const w = Math.abs(q1.x - q0.x), h = Math.abs(q1.y - q0.y), a = w * h;
      if (a > area) { area = a; bodyEl = e; body = [Math.min(q0.x, q1.x), Math.max(q0.x, q1.x), Math.min(q0.y, q1.y), Math.max(q0.y, q1.y)]; }
      if (role === 'flag' && h > 4 * w && h > poleW) { poleW = h; pole = (q0.x + q1.x) / 2; }   // the pole: the tallest thin shape
    }
    if (!body) continue;
    const bw = body[1] - body[0], bh = body[3] - body[2], eyes = [];
    for (const e of g.querySelectorAll('circle,ellipse')) {
      if (e.closest('[id^="fg"]')) continue;
      const cs = getComputedStyle(e); if (!cs.fill || cs.fill === 'none' || lum(cs.fill) > 0.35) continue;
      const b = e.getBBox(); const q0 = inLocal(g, e, b.x, b.y), q1 = inLocal(g, e, b.x + b.width, b.y + b.height);
      const w = Math.abs(q1.x - q0.x), cx = (q0.x + q1.x) / 2, cy = (q0.y + q1.y) / 2;
      if (w < 1.5 || w > Math.max(14, bw * 0.08)) continue;
      if (cx < body[0] || cx > body[1] || cy < body[2] || cy > body[3]) continue;
      eyes.push(cx);
    }
    // taper: height of the body outline in its left and right 20 % bands (the narrower end of a rocket / arrow / ship is the front)
    // lean: mean x of the outline in the top 30 % minus the bottom 30 % (smoke, hair, grass: which way it blows)
    let taper = null, lean = null;
    if (bodyEl && bodyEl.tagName === 'path' && bodyEl.getTotalLength) {
      const L = bodyEl.getTotalLength(); const ys = {l: [], r: []}, xs = {t: [], b: []};
      for (let i = 0; i < 160; i++) { const p = bodyEl.getPointAtLength(L * i / 160); const q = inLocal(g, bodyEl, p.x, p.y);
        if (q.x < body[0] + bw * 0.2) ys.l.push(q.y); else if (q.x > body[1] - bw * 0.2) ys.r.push(q.y);
        if (q.y < body[2] + bh * 0.3) xs.t.push(q.x); else if (q.y > body[3] - bh * 0.3) xs.b.push(q.x); }
      const h = a => a.length ? Math.max(...a) - Math.min(...a) : 0; taper = [h(ys.l), h(ys.r)];
      const mean = a => a.length ? a.reduce((s, v) => s + v, 0) / a.length : null;
      if (xs.t.length && xs.b.length) lean = mean(xs.t) - mean(xs.b);
    }
    const rc = toRoot(g, gb);
    out.push({id: g.id, role, x0: body[0], x1: body[1], y0: body[2], y1: body[3], eyes, taper, lean, pole, lb: [gb.x, gb.x + gb.width, gb.y, gb.y + gb.height],
              face: g.getAttribute('data-face') || '', text: !!g.querySelector('text'), tf: !!g.getAttribute('transform'), root: rc});
  }
  const boxes = {};
  for (const g of document.querySelectorAll('g[id]')) { if (g.closest('[id^="fg"]')) continue; const b = g.getBBox(); if (b.width < 8) continue; boxes[g.id] = toRoot(g, b); }
  // shadows / highlights drawn inside an object's group: where they sit relative to the group's centre (parent-local x)
  const shadows = [];
  for (const e of document.querySelectorAll('[id],[class]')) {
    const key = (e.id || '') + ' ' + (e.getAttribute('class') || ''); const kind = /shadow|shade/i.test(key) ? 'shadow' : (/highlight|glint|shine|specular|rim-?light/i.test(key) ? 'light' : null);
    if (!kind || !['ellipse','circle','path','rect','polygon'].includes(e.tagName)) continue;
    if (e.closest('[id^="fg"]')) continue;
    const par = e.parentElement; if (!par || par.tagName !== 'g' || par === svg) continue;
    const pb = par.getBBox(); if (pb.width < 30) continue;
    const b = e.getBBox(); const q0 = inLocal(par, e, b.x, b.y), q1 = inLocal(par, e, b.x + b.width, b.y + b.height);
    const prc = toRoot(par, pb);
    shadows.push({id: e.id || '', kind, tag: e.tagName, cx: (q0.x + q1.x) / 2, w: Math.abs(q1.x - q0.x), pcx: pb.x + pb.width / 2, pw: pb.width, prcx: (prc[0] + prc[1]) / 2, tf: !!e.getAttribute('transform'), pid: par.id || ''});
  }
  return {groups: out, boxes, shadows};
}"""


def compute(files, W=1920, H=1080, cache=None):
    """{svg path: [{id, x0, x1, eyes, face}]} for every travelling group (Playwright, cached by file mtime like pivots.py)"""
    from paths import chrome
    from playwright.sync_api import sync_playwright
    old = {}
    if cache and os.path.exists(cache):
        try: old = json.load(open(cache))
        except Exception: old = {}
    res, todo = {}, []
    for f in files:
        k = f'{os.path.abspath(f)}|{os.path.getmtime(f)}|{CACHE_V}'
        if k in old: res[f] = old[k]
        else: todo.append(f)
    if todo:
        with sync_playwright() as p:
            b = p.chromium.launch(executable_path=chrome(), args=['--no-sandbox'])
            pg = b.new_page(viewport={'width': W, 'height': H})
            for f in todo:
                s = open(f, encoding='utf-8').read()
                if not re.search(r'\bid="', s): res[f] = {'groups': [], 'boxes': {}, 'shadows': []}; continue
                pg.goto('file://' + os.path.abspath(f)); res[f] = pg.evaluate(JS)
            b.close()
    if cache:
        json.dump({f'{os.path.abspath(f)}|{os.path.getmtime(f)}|{CACHE_V}': v for f, v in res.items()}, open(cache, 'w'))
    return res


def groups(res_f, role='travel'):
    """the probed groups of one picture; role 'travel' (default), 'gaze', 'lean', 'flag' or None for all"""
    gs = res_f.get('groups', []) if isinstance(res_f, dict) else (res_f or [])
    return gs if role is None else [g for g in gs if g.get('role', 'travel') == role]


def facing_sign(e):
    if e.get('face') in ('left', 'right'): return 1 if e['face'] == 'right' else -1
    if e.get('eyes') and len(e['eyes']) <= 4:
        cx = (e['x0'] + e['x1']) / 2; w = max(e['x1'] - e['x0'], 1); m = sum(e['eyes']) / len(e['eyes'])
        if abs(m - cx) >= .12 * w: return 1 if m > cx else -1
    t = e.get('taper')
    if t and POINTED.search(e['id']) and max(t) > 0:
        hl, hr = t
        if hl < .6 * hr: return -1      # narrow left end = nose on the left
        if hr < .6 * hl: return 1
    return 0


def context(res_f, svg_text, side=None):
    """per-picture direction context: travel (+1/-1/0), wind (+1 left->right / -1), attractor [x, y] or None"""
    side = side or {}; best = (0, 0)
    for e in groups(res_f):
        tag = re.search(rf'<g [^>]*\bid="{re.escape(e["id"])}"[^>]*>', svg_text)
        ts = travel_sign(tag.group(0)) if tag else 0
        if ts and e.get('root') and (e['root'][1] - e['root'][0]) > best[0]: best = (e['root'][1] - e['root'][0], ts)
    travel = best[1]
    wind = {'left': -1, 'right': 1}.get(side.get('wind')) or (-travel if travel else 1)
    att = side.get('attractor')
    if not att:
        boxes = res_f.get('boxes', {}) if isinstance(res_f, dict) else {}
        cands = [(b[1] - b[0], gid, b) for gid, b in boxes.items() if ATTR.search(re.sub(r'^mv-[a-z]+-', '', gid)) and not gid.startswith('mv-path-')]
        if cands: cands.sort(reverse=True); b = cands[0][2]; att = [round((b[0] + b[1]) / 2), round((b[2] + b[3]) / 2)]
    boxes = res_f.get('boxes', {}) if isinstance(res_f, dict) else {}
    # focus = what drawn characters look at: the attractor, else the widest travelling group, else the widest mv-core group
    focus = None   # the travelling object first (what the scene is about), then the attractor, then the centre object
    if True:
        tr = [(e['root'][1] - e['root'][0], e['root']) for e in groups(res_f) if e.get('root') and travel_sign((re.search(rf'<g [^>]*\bid="{re.escape(e["id"])}"[^>]*>', svg_text) or [None]) and re.search(rf'<g [^>]*\bid="{re.escape(e["id"])}"[^>]*>', svg_text).group(0) or '')]
        if tr:
            tr.sort(reverse=True); b = tr[0][1]; focus = [round((b[0] + b[1]) / 2), round((b[2] + b[3]) / 2)]
            e0 = next((e for e in groups(res_f) if e.get('root') == b), None)
            tg = re.search(rf'<g [^>]*\bid="{re.escape(e0["id"])}"[^>]*>', svg_text) if e0 else None
            pm = re.search(r'\bdata-path="([^"]*)"', tg.group(0)) if tg else None; pe = path_ends(pm.group(1)) if pm else None
            if pe: focus = [round((pe[0] + pe[2]) / 2), round((pe[1] + pe[3]) / 2)]   # a path group is drawn at the origin and placed by GSAP: use the middle of its route
    if not focus: focus = att
    if not focus:
        cs = [(b[1] - b[0], b) for gid, b in boxes.items() if gid.startswith('mv-core-')]
        if cs: cs.sort(reverse=True); b = cs[0][1]; focus = [round((b[0] + b[1]) / 2), round((b[2] + b[3]) / 2)]
    # light: sidecar "light": "left"|"right" (-1/+1), else the widest group named like a light source -> [x, y]
    light = {'left': -1, 'right': 1}.get(side.get('light'))
    if not light:
        ls = [(b[1] - b[0], b) for gid, b in boxes.items() if LIGHT.search(re.sub(r'^mv-[a-z]+-', '', gid))]
        if ls: ls.sort(reverse=True); b = ls[0][1]; light = [round((b[0] + b[1]) / 2), round((b[2] + b[3]) / 2)]
    return dict(travel=travel, wind=wind, attractor=att, focus=focus, light=light, wind_known=bool(side.get('wind') in ('left', 'right') or travel))


def reverse_path(d):
    """the same path drawn from its end to its start (absolute M/L/C/Q/H/V, relative accumulated); None when it holds arcs/S/T"""
    segs = []; cur = (0.0, 0.0); ok = True
    for cmd, args in re.findall(r'([MmLlHhVvCcSsQqTtAaZz])([^MmLlHhVvCcSsQqTtAaZz]*)', d):
        nums = [float(x) for x in re.findall(NUM, args)]; rel = cmd.islower(); c = cmd.upper()
        ab = lambda x, y: ((cur[0] + x) if rel else x, (cur[1] + y) if rel else y)
        if c == 'Z': continue
        if c in ('A', 'S', 'T'): ok = False; break
        if c == 'H':
            for v in nums: cur = ((cur[0] + v) if rel else v, cur[1]); segs.append(('L', [cur]))
        elif c == 'V':
            for v in nums: cur = (cur[0], (cur[1] + v) if rel else v); segs.append(('L', [cur]))
        elif c in ('M', 'L'):
            for i in range(0, len(nums) - 1, 2): cur = ab(nums[i], nums[i + 1]); segs.append((c if i == 0 else 'L', [cur]))
        elif c == 'C':
            for i in range(0, len(nums) - 5, 6): p1 = ab(nums[i], nums[i + 1]); p2 = ab(nums[i + 2], nums[i + 3]); p3 = ab(nums[i + 4], nums[i + 5]); segs.append(('C', [p1, p2, p3])); cur = p3
        elif c == 'Q':
            for i in range(0, len(nums) - 3, 4): p1 = ab(nums[i], nums[i + 1]); p2 = ab(nums[i + 2], nums[i + 3]); segs.append(('Q', [p1, p2])); cur = p2
    if not ok or len(segs) < 2 or segs[0][0] != 'M': return None
    pts = [segs[0][1][0]]; out = []
    for c, ps in segs[1:]: pts.append(ps[-1])
    o = [f'M{pts[-1][0]:g},{pts[-1][1]:g}']
    for i in range(len(segs) - 1, 0, -1):
        c, ps = segs[i]; prev = pts[i - 1]
        if c == 'L': o.append(f'L{prev[0]:g},{prev[1]:g}')
        elif c == 'C': o.append(f'C{ps[1][0]:g},{ps[1][1]:g} {ps[0][0]:g},{ps[0][1]:g} {prev[0]:g},{prev[1]:g}')
        elif c == 'Q': o.append(f'Q{ps[0][0]:g},{ps[0][1]:g} {prev[0]:g},{prev[1]:g}')
    return ' '.join(o)


def decide(entries, svg_text):
    """[(gid, facing, travel)] for the groups whose facing and travel disagree"""
    out = []
    for e in groups(entries):
        tag = re.search(rf'<g [^>]*\bid="{re.escape(e["id"])}"[^>]*>', svg_text)
        if not tag: continue
        fs, ts = facing_sign(e), travel_sign(tag.group(0))
        if fs and ts and fs != ts: out.append((e['id'], fs, ts))
    return out


def _close(svg_text, start):
    """index just after the </g> that closes the <g ...> starting at `start`"""
    depth = 0
    for m in re.finditer(r'<g\b[^>]*?(/?)>|</g>', svg_text[start:]):
        if m.group(0).startswith('</g>'): depth -= 1
        elif not m.group(1): depth += 1
        if depth == 0: return start + m.end()
    return None


def _path_rules(svg_text, entries, ctx):
    """vertical name sanity + 'toward the attractor' for mv-path groups; mv-magnet toward the attractor. Returns (text, notes)"""
    notes = []; att = (ctx or {}).get('attractor')
    for m in list(re.finditer(r'<g [^>]*\bid="(mv-(path|magnet)-[^"]+)"[^>]*>', svg_text)):
        tag = m.group(0); gid = m.group(1); kind = m.group(2); name = gid[len('mv-' + kind + '-'):]
        if kind == 'magnet':
            if not att: continue
            box = (entries.get('boxes', {}) if isinstance(entries, dict) else {}).get(gid)
            if not box: continue
            vx, vy = att[0] - (box[0] + box[1]) / 2, att[1] - (box[2] + box[3]) / 2; L = (vx * vx + vy * vy) ** .5 or 1
            m0 = re.search(rf'\bdata-dx="({NUM})"', tag); m1 = re.search(rf'\bdata-dy="({NUM})"', tag)
            mag = ((float(m0.group(1)) if m0 else -200) ** 2 + (float(m1.group(1)) if m1 else 0) ** 2) ** .5 or 200
            ndx, ndy = vx / L * mag, vy / L * mag
            if m0 and m1 and abs(float(m0.group(1)) - ndx) < 1 and abs(float(m1.group(1)) - ndy) < 1: continue
            new = re.sub(rf'\s*data-d[xy]="{NUM}"', '', tag); new = new[:-1] + f' data-dx="{ndx:.0f}" data-dy="{ndy:.0f}">'
            svg_text = svg_text.replace(tag, new, 1); notes.append((gid, f'magnet pulled toward the attractor ({ndx:.0f},{ndy:.0f})')); continue
        pm = re.search(r'\bdata-path="([^"]*)"', tag)
        if not pm: continue
        e = path_ends(pm.group(1))
        if not e: continue
        why = None
        if DOWNN.search(name) and not UPN.search(name) and e[3] < e[1] - 30: why = 'named as going down but the path rose'
        elif UPN.search(name) and not DOWNN.search(name) and e[3] > e[1] + 30: why = 'named as going up but the path fell'
        elif att and (TOWARDN.search(name) or TOWARDN.search(tag)):
            d0 = ((e[0] - att[0]) ** 2 + (e[1] - att[1]) ** 2) ** .5; d1 = ((e[2] - att[0]) ** 2 + (e[3] - att[1]) ** 2) ** .5
            if d1 > d0 + 40: why = 'pulled toward the attractor but the path led away'
        if not why: continue
        rp = reverse_path(pm.group(1))
        if rp is None: notes.append((gid, f'NOT reversed (arc/S/T path): {why}')); continue
        new = tag[:pm.start(1)] + rp + tag[pm.end(1):]; svg_text = svg_text.replace(tag, new, 1); notes.append((gid, f'path reversed: {why}'))
    return svg_text, notes


def _mirror_group(svg_text, gid, cx):
    """mirror the contents of group gid about local x = cx (wrapper <g>, inner data-pivot x mirrored). Returns the new text or None"""
    m = re.search(rf'<g [^>]*\bid="{re.escape(gid)}"[^>]*>', svg_text)
    if not m: return None
    end = _close(svg_text, m.start())
    if end is None: return None
    inner = svg_text[m.end():end - 4]
    inner = re.sub(r'data-pivot="(-?[\d.]+)[ ,](-?[\d.]+)"', lambda mm: f'data-pivot="{2 * cx - float(mm.group(1)):g} {mm.group(2)}"', inner)
    return svg_text[:m.end()] + f'<g transform="translate({2 * cx:g} 0) scale(-1 1)" data-facefix="1">' + inner + '</g>' + svg_text[end - 4:]


def _set_attr(tag, key, val):
    tag2 = re.sub(rf'\s*\b{key}="[^"]*"', '', tag)
    return tag2[:-1].rstrip('/') + f' {key}="{val}"' + ('/>' if tag2.endswith('/>') else '>')


def _dir_rules2(svg_text, entries, ctx):
    """guideline 4-4 B (2026-10-27): (1) touching gears turn opposite ways (data-dir, a mv-core gear is the reference), (2) flags blow away from the pole
    and smoke/hair/grass lean with the wind (mirrored when drawn the other way), (3) drawn characters look toward the picture's focus,
    (4) shadows sit away from the light source and highlights toward it (mirrored inside their object's group). Returns (text, notes)."""
    notes = []; ctx = ctx or {}
    boxes = entries.get('boxes', {}) if isinstance(entries, dict) else {}
    # (1) gears
    gears = []
    for gid, b in boxes.items():
        k = kind_of(gid); nm = re.sub(r'^mv-[a-z]+-', '', gid)
        if k in ('spin', 'rotor', 'core') and GEAR.search(nm): gears.append((gid, k, b))
    if len(gears) >= 2:
        tagof = lambda gid: re.search(rf'<g [^>]*\bid="{re.escape(gid)}"[^>]*>', svg_text)
        cur = {}
        for gid, k, b in gears:
            m = tagof(gid); cur[gid] = 1 if (k == 'core' or not m or not re.search(r'\bdata-dir="-', m.group(0))) else -1
        rad = {gid: ((b[1] - b[0]) + (b[3] - b[2])) / 4 for gid, k, b in gears}; cen = {gid: ((b[0] + b[1]) / 2, (b[2] + b[3]) / 2) for gid, k, b in gears}
        adj = {gid: [] for gid, _, _ in gears}
        for i in range(len(gears)):
            for j in range(i + 1, len(gears)):
                a, b_ = gears[i][0], gears[j][0]; d = ((cen[a][0] - cen[b_][0]) ** 2 + (cen[a][1] - cen[b_][1]) ** 2) ** .5; rs = rad[a] + rad[b_]
                if .72 * rs <= d <= 1.15 * rs: adj[a].append(b_); adj[b_].append(a)
        want = {}; order = [g for g in adj if kind_of(g) == 'core'] + [g for g in adj if kind_of(g) != 'core']
        for s in order:
            if s in want or not adj[s]: continue
            want[s] = cur[s]; q = [s]
            while q:
                a = q.pop(0)
                for b_ in adj[a]:
                    if b_ not in want: want[b_] = -want[a]; q.append(b_)
                    elif want[b_] == want[a]: notes.append((b_, f'gear mesh conflict with {a} (odd loop or two fixed cores): left as drawn'))
        for gid, w in want.items():
            if w == cur[gid] or kind_of(gid) == 'core': continue
            m = tagof(gid)
            if not m: continue
            svg_text = svg_text.replace(m.group(0), _set_attr(m.group(0), 'data-dir', str(w)), 1); notes.append((gid, f'gear turned the other way (data-dir {w}) to mesh with its neighbour'))
    wind = ctx.get('wind') or 1
    # (2) flags and leaning things: only when the wind is known (sidecar `wind` or a travelling object); a still picture keeps what was drawn
    for e in (groups(entries, 'flag') if ctx.get('wind_known') else []):
        if e.get('tf') or e.get('text'): continue
        px = e.get('pole'); lb = e['lb']
        if px is None: px = lb[0]; drawn = 1                       # no pole found: by convention the pole is the left edge and the cloth blows right
        else: drawn = 1 if ((e['x0'] + e['x1']) / 2) >= px else -1   # cloth centre vs pole
        if drawn != wind:
            new = _mirror_group(svg_text, e['id'], px)
            if new: svg_text = new; notes.append((e['id'], f'flag mirrored about its pole to blow {"right" if wind > 0 else "left"} with the wind'))
    for e in (groups(entries, 'lean') if ctx.get('wind_known') else []):
        if e.get('tf') or e.get('text') or e.get('lean') is None: continue
        bh = max(e['y1'] - e['y0'], 1)
        if abs(e['lean']) < .08 * bh: continue
        drawn = 1 if e['lean'] > 0 else -1
        if drawn != wind:
            new = _mirror_group(svg_text, e['id'], (e['x0'] + e['x1']) / 2)
            if new: svg_text = new; notes.append((e['id'], f'leaning shape mirrored to blow {"right" if wind > 0 else "left"} with the wind'))
    # (3) gaze
    focus = ctx.get('focus')
    if focus:
        for e in groups(entries, 'gaze'):
            fs = facing_sign(e)
            if not fs or e.get('tf') or e.get('text') or not e.get('root'): continue
            gcx = (e['root'][0] + e['root'][1]) / 2; dx = focus[0] - gcx
            if abs(dx) < 150 or abs(dx) < .6 * (e['root'][1] - e['root'][0]): continue   # the focus is this group itself or right above/below it
            want = 1 if dx > 0 else -1
            if want != fs:
                new = _mirror_group(svg_text, e['id'], (e['x0'] + e['x1']) / 2)
                if new: svg_text = new; notes.append((e['id'], f'character turned to look {"right" if want > 0 else "left"} toward the focus'))
    # (4) shadows and highlights
    light = ctx.get('light')
    if light:
        for sh in (entries.get('shadows', []) if isinstance(entries, dict) else []):
            if not sh.get('id') or sh.get('tf'): continue
            s = light if isinstance(light, int) else (1 if light[0] > sh['prcx'] else -1)
            off = sh['cx'] - sh['pcx']
            if abs(off) < .08 * sh['pw'] or sh['w'] > .9 * sh['pw']: continue   # centred ground shadow / full-size layer: nothing to say
            want = -s if sh['kind'] == 'shadow' else s
            if (1 if off > 0 else -1) == want: continue
            m = re.search(rf'<{sh["tag"]}\b[^>]*\bid="{re.escape(sh["id"])}"[^>]*/>', svg_text)
            if not m: notes.append((sh['id'], f'{sh["kind"]} on the lit side, NOT moved (not a self-closing element)')); continue
            svg_text = svg_text[:m.start()] + f'<g transform="translate({2 * sh["pcx"]:g} 0) scale(-1 1)" data-facefix="1">' + m.group(0) + '</g>' + svg_text[m.end():]
            notes.append((sh['id'], f'{sh["kind"]} mirrored to the {"far" if sh["kind"] == "shadow" else "lit"} side of the light'))
    return svg_text, notes


def apply(svg_text, entries, log=None, ctx=None):
    """mirror the DRAWING of every disagreeing group about its body centre (the travel, the composition and any target it moves toward stay);
    inner data-pivot x values are mirrored too. Returns the new text and [(gid, note)]. Skipped (noted, not changed): groups with their own
    transform attribute or with text inside."""
    fixed = []
    svg_text, notes = _path_rules(svg_text, entries, ctx); fixed.extend(notes)
    svg_text, notes = _dir_rules2(svg_text, entries, ctx); fixed.extend(notes)
    for gid, fs, ts in decide(entries, svg_text):
        e = next(x for x in groups(entries) if x['id'] == gid)
        m = re.search(rf'<g [^>]*\bid="{re.escape(gid)}"[^>]*>', svg_text)
        if e.get('tf') or e.get('text'): fixed.append((gid, 'NOT flipped (group has transform/text); faces %s, moves %s' % ('right' if fs > 0 else 'left', 'right' if ts > 0 else 'left'))); continue
        new = _mirror_group(svg_text, gid, (e['x0'] + e['x1']) / 2)
        if new is None: continue
        svg_text = new
        fixed.append((gid, 'drawing mirrored (faced %s, moves %s)' % ('right' if fs > 0 else 'left', 'right' if ts > 0 else 'left')))
    return svg_text, fixed


if __name__ == '__main__':   # python3 tools/facing.py <slug>: report (no files changed)
    slug = sys.argv[1]; d = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'videos', slug, 'art3')
    files = sorted(os.path.join(d, f) for f in os.listdir(d) if f.endswith('.svg'))
    res = compute(files); n = 0; unk = 0
    for f, ents in res.items():
        s = open(f, encoding='utf-8').read(); ctx = context(ents, s)
        if ctx['attractor'] or ctx['travel']: print(os.path.basename(f), 'context', ctx)
        if ctx.get('light') or groups(ents, 'gaze'): print(os.path.basename(f), 'focus', ctx.get('focus'), 'light', ctx.get('light'))
        _, notes = _path_rules(s, ents, ctx)
        for g_, w_ in notes: print(os.path.basename(f), g_, w_)
        _, notes = _dir_rules2(s, ents, ctx)
        for g_, w_ in notes: print(os.path.basename(f), g_, w_)
        for e in groups(ents, None):
            if e.get('role', 'travel') != 'travel': print(os.path.basename(f), e['id'], e['role'], 'face', facing_sign(e), 'eyes', len(e['eyes']), 'lean', None if e.get('lean') is None else round(e['lean']), 'pole', e.get('pole'))
        for e in groups(ents):
            tag = re.search(rf'<g [^>]*\bid="{re.escape(e["id"])}"[^>]*>', s); ts = travel_sign(tag.group(0)) if tag else 0; fs = facing_sign(e); n += 1
            if ts and not fs: unk += 1
            flag = 'WRONG' if fs and ts and fs != ts else ('unknown facing' if ts and not fs else 'ok' if ts else 'vertical/none')
            print(os.path.basename(f), e['id'], 'face', fs, 'travel', ts, 'eyes', len(e['eyes']), flag)
    print('groups', n, 'unknown facing', unk)


def spin_dir(svg_text, gid):
    """+1 clockwise / -1 counter-clockwise: how the whirl / ring named gid turns (its own data-dir if it is a mv-spin/rotor, else the first mv-circle/mv-spin/mv-rotor
    data-dir in the picture, else +1). The frog orbits the same way (guideline 4-4 B)."""
    m = re.search(rf'<g [^>]*\bid="{re.escape(gid)}"[^>]*>', svg_text) if gid else None
    if m and re.match(r'mv-(spin|rotor)-', gid): return -1 if re.search(r'\bdata-dir="-', m.group(0)) else 1
    for mm in re.finditer(r'<g [^>]*\bid="mv-(circle|spin|rotor)-[^"]*"[^>]*>', svg_text):
        return -1 if re.search(r'\bdata-dir="-', mm.group(0)) else 1
    return 1
