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
# Used by build3 (facing.compute -> facing.apply on the inlined SVG, log "direction sanity") and by frog_place (travel_sign).
import os, re, json
import sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
TRAVEL = ('path', 'swim', 'rollby', 'creep', 'magnet')   # scroll = a background layer, no facing
NUM = r'-?\d*\.?\d+(?:e-?\d+)?'


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
    return 0


JS = r"""() => {
  const svg = document.querySelector('svg'); if (!svg) return [];
  const lum = c => { const m = (c || '').match(/\d+(\.\d+)?/g); if (!m || m.length < 3) return 1; return (0.299*m[0] + 0.587*m[1] + 0.114*m[2]) / 255; };
  const inLocal = (g, el, x, y) => { const p = svg.createSVGPoint(); p.x = x; p.y = y; return p.matrixTransform(g.getCTM().inverse().multiply(el.getCTM())); };
  const out = [];
  for (const g of document.querySelectorAll('g[id^="mv-"]')) {
    const k = (g.id.match(/^mv-([a-z]+)-/) || [])[1]; if (!['path','swim','rollby','creep','magnet'].includes(k)) continue;
    const gb = g.getBBox(); if (gb.width < 20) continue;
    // body = the largest opaque filled shape (beams, glows and shadows are translucent); pupils = small DARK filled circles inside the body's x range
    let body = null, area = 0;
    for (const e of g.querySelectorAll('path,ellipse,rect,circle,polygon')) {
      if (e.closest('[id^="fg"]')) continue;
      const cs = getComputedStyle(e); if (!cs.fill || cs.fill === 'none') continue;
      let op = 1, n = e; while (n && n !== g) { op *= parseFloat(getComputedStyle(n).opacity || 1); n = n.parentElement; }
      op *= parseFloat(cs.fillOpacity || 1); if (op < 0.5) continue;
      const b = e.getBBox(); const q0 = inLocal(g, e, b.x, b.y), q1 = inLocal(g, e, b.x + b.width, b.y + b.height);
      const a = Math.abs(q1.x - q0.x) * Math.abs(q1.y - q0.y); if (a > area) { area = a; body = [Math.min(q0.x, q1.x), Math.max(q0.x, q1.x), Math.min(q0.y, q1.y), Math.max(q0.y, q1.y)]; }
    }
    if (!body) continue;
    const bw = body[1] - body[0], eyes = [];
    for (const e of g.querySelectorAll('circle,ellipse')) {
      if (e.closest('[id^="fg"]')) continue;
      const cs = getComputedStyle(e); if (!cs.fill || cs.fill === 'none' || lum(cs.fill) > 0.35) continue;
      const b = e.getBBox(); const q0 = inLocal(g, e, b.x, b.y), q1 = inLocal(g, e, b.x + b.width, b.y + b.height);
      const w = Math.abs(q1.x - q0.x), cx = (q0.x + q1.x) / 2, cy = (q0.y + q1.y) / 2;
      if (w < 1.5 || w > Math.max(14, bw * 0.08)) continue;
      if (cx < body[0] || cx > body[1] || cy < body[2] || cy > body[3]) continue;
      eyes.push(cx);
    }
    out.push({id: g.id, x0: body[0], x1: body[1], eyes, face: g.getAttribute('data-face') || '', text: !!g.querySelector('text'), tf: !!g.getAttribute('transform')});
  }
  return out;
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
        k = f'{os.path.abspath(f)}|{os.path.getmtime(f)}'
        if k in old: res[f] = old[k]
        else: todo.append(f)
    if todo:
        with sync_playwright() as p:
            b = p.chromium.launch(executable_path=chrome(), args=['--no-sandbox'])
            pg = b.new_page(viewport={'width': W, 'height': H})
            for f in todo:
                s = open(f, encoding='utf-8').read()
                if not re.search(r'id="mv-(path|swim|rollby|creep|magnet)-', s): res[f] = []; continue
                pg.goto('file://' + os.path.abspath(f)); res[f] = pg.evaluate(JS)
            b.close()
    if cache:
        json.dump({f'{os.path.abspath(f)}|{os.path.getmtime(f)}': v for f, v in res.items()}, open(cache, 'w'))
    return res


def facing_sign(e):
    if e.get('face') in ('left', 'right'): return 1 if e['face'] == 'right' else -1
    if not e.get('eyes') or len(e['eyes']) > 4: return 0
    cx = (e['x0'] + e['x1']) / 2; w = max(e['x1'] - e['x0'], 1); m = sum(e['eyes']) / len(e['eyes'])
    return 0 if abs(m - cx) < .12 * w else (1 if m > cx else -1)


def decide(entries, svg_text):
    """[(gid, facing, travel)] for the groups whose facing and travel disagree"""
    out = []
    for e in entries:
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


def apply(svg_text, entries, log=None):
    """mirror the DRAWING of every disagreeing group about its body centre (the travel, the composition and any target it moves toward stay);
    inner data-pivot x values are mirrored too. Returns the new text and [(gid, note)]. Skipped (noted, not changed): groups with their own
    transform attribute or with text inside."""
    fixed = []
    for gid, fs, ts in decide(entries, svg_text):
        e = next(x for x in entries if x['id'] == gid)
        m = re.search(rf'<g [^>]*\bid="{re.escape(gid)}"[^>]*>', svg_text)
        if e.get('tf') or e.get('text'): fixed.append((gid, 'NOT flipped (group has transform/text); faces %s, moves %s' % ('right' if fs > 0 else 'left', 'right' if ts > 0 else 'left'))); continue
        end = _close(svg_text, m.start())
        if end is None: continue
        cx = (e['x0'] + e['x1']) / 2
        inner = svg_text[m.end():end - 4]
        inner = re.sub(r'data-pivot="(-?[\d.]+)[ ,](-?[\d.]+)"', lambda mm: f'data-pivot="{2 * cx - float(mm.group(1)):g} {mm.group(2)}"', inner)
        svg_text = svg_text[:m.end()] + f'<g transform="translate({2 * cx:g} 0) scale(-1 1)" data-facefix="1">' + inner + '</g>' + svg_text[end - 4:]
        fixed.append((gid, 'drawing mirrored (faced %s, moves %s)' % ('right' if fs > 0 else 'left', 'right' if ts > 0 else 'left')))
    return svg_text, fixed


if __name__ == '__main__':   # python3 tools/facing.py <slug>: report (no files changed)
    slug = sys.argv[1]; d = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'videos', slug, 'art3')
    files = sorted(os.path.join(d, f) for f in os.listdir(d) if f.endswith('.svg'))
    res = compute(files); n = 0; unk = 0
    for f, ents in res.items():
        s = open(f, encoding='utf-8').read()
        for e in ents:
            tag = re.search(rf'<g [^>]*\bid="{re.escape(e["id"])}"[^>]*>', s); ts = travel_sign(tag.group(0)) if tag else 0; fs = facing_sign(e); n += 1
            if ts and not fs: unk += 1
            flag = 'WRONG' if fs and ts and fs != ts else ('unknown facing' if ts and not fs else 'ok' if ts else 'vertical/none')
            print(os.path.basename(f), e['id'], 'face', fs, 'travel', ts, 'eyes', len(e['eyes']), flag)
    print('groups', n, 'unknown facing', unk)
