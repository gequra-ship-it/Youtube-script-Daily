# usage: python3 tools/armfix.py <slug>... [--report]        (no slug = every videos/<slug>)
# (2026-11-01 miya) A person's arm raised above the shoulder must curve like the frog's: the ELBOW bulges OUTWARD (away from the body), the forearm folds up and in, so two raised arms
# make a "(O)" / "ヽOﾉ" shape, never an inward ")O(" (miya 2026-11-01 correction). Needs the -l/-r pair of the figure to know which way is outward. Frog arms already do this (frog_rig.arm_bend_pass); this is the same rule for the
# people drawn with tools/body.py (mv-limb-<name>-1 / -2 groups).
# One-shape arm (mv-limb-<n>-1 only): when the wrist is above the shoulder and the arm bulges to the wrong side of the shoulder->wrist line, the whole arm (sleeve, cuff, hand) is
# mirrored across that line (the bulge flips, the hand follows the mirrored tangent). Two-link arm (mv-limb-<n>-1 with mv-limb-<n>-2 inside): the forearm link (content only, it keeps its
# pivot) is mirrored across the upper-arm line through the elbow, so the forearm folds to the other side. Idempotent: after the fix the test passes and nothing more happens.
# --report prints the arms that would change and writes nothing. Exit code 1 in --check mode when any arm is still wrong (used by final_check).
import os, re, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from paths import REPO, chrome
from playwright.sync_api import sync_playwright

JS = r'''
() => {
 const svg = document.querySelector('svg'); const out = [];
 const num = s => (s || '').trim().split(/[ ,]+/).map(Number);
 const toFrame = (g, el, x, y) => { const M = g.parentNode.getCTM().inverse().multiply(el.getCTM()); const q = new DOMPoint(x, y).matrixTransform(M); return [q.x, q.y]; };
 const idOf = g => g.id || [...g.classList].find(c => /^mv-limb-/.test(c)) || '';
 svg.querySelectorAll('g[id^="mv-limb-"], g[class*="mv-limb-"]').forEach(g => {
   const gid = idOf(g); if (!/^mv-limb-.*-1$/.test(gid)) return;
   const S = num(g.getAttribute('data-pivot')); if (S.length !== 2 || S.some(isNaN)) return;
   const g2 = [...g.children].find(c => c.tagName === 'g' && /^mv-limb-/.test(idOf(c)));
   let W = null, E = null, mean = null, two = false;
   const lastCircle = el => { const c = [...el.querySelectorAll('circle')]; return c.length ? c[c.length - 1] : null; };
   if (g2) { const e = num(g2.getAttribute('data-pivot')); if (e.length !== 2 || e.some(isNaN)) return; E = e; two = true;
     const c = lastCircle(g2); if (!c) return; W = toFrame(g, c, +c.getAttribute('cx'), +c.getAttribute('cy'));
     mean = E; }
   else { const c = lastCircle(g); if (!c) return; W = toFrame(g, c, +c.getAttribute('cx'), +c.getAttribute('cy'));
     const p = g.querySelector('path'); if (!p) return;
     // the true wrist = middle of the round end cap of the silhouette (the hand circle sits a little beyond it along the tangent)
     const m = (p.getAttribute('d') || '').match(/L\s*(-?[\d.]+),(-?[\d.]+)\s+A\s*[\d.]+,[\d.]+\s+0\s+0\s+0\s+(-?[\d.]+),(-?[\d.]+)/);
     if (m) W = toFrame(g, p, (+m[1] + +m[3]) / 2, (+m[2] + +m[4]) / 2); const L = p.getTotalLength(); let sx = 0, sy = 0, n = 0;
     for (let i = 0; i <= 40; i++) { const q = p.getPointAtLength(L * i / 40), f = toFrame(g, p, q.x, q.y); sx += f[0]; sy += f[1]; n++; } mean = [sx / n, sy / n]; }
   // body centre of a lone arm: the nearest ancestor that holds drawn shapes which are not arms (torso, head ...), centre x of their union box, in the arm's parent frame
   let fx = null; for (let A = g.parentNode; A && A !== svg && fx === null; A = A.parentNode) {
     const ks = [...A.children].filter(k => k !== g && !k.matches('defs,style,title,desc') && !(k.matches('[class*="mv-limb-"],[id^="mv-limb-"]') || k.querySelector('[class*="mv-limb-"],[id^="mv-limb-"]')));
     let x0 = 1e9, x1 = -1e9; ks.forEach(k => { try { const b = k.getBBox(); if (!(b.width + b.height)) return; const M = g.parentNode.getCTM().inverse().multiply(k.getCTM());
       [[b.x, b.y], [b.x + b.width, b.y + b.height]].forEach(([x, y]) => { const q = new DOMPoint(x, y).matrixTransform(M); x0 = Math.min(x0, q.x); x1 = Math.max(x1, q.x); }); } catch (e) {} });
     if (x1 > x0) fx = (x0 + x1) / 2; }
   out.push({id: gid, S, W, E, mean, two, fx});
 });
 return out;
}
'''


def wrong_side(S, W, B, ox):
    """True when the bulge point B (the elbow side of the arm) lies on the INNER side of the shoulder->wrist line for an arm whose wrist is above the shoulder.
    ox = +1 / -1: the outward direction on screen (away from the body centre line). Frog rule: raised arms bend OUTWARD ("(O)"), never inward ")O(" (screen y grows downward)."""
    cx, cy = W[0] - S[0], W[1] - S[1]; L = math.hypot(cx, cy)
    if L < 1 or (S[1] - W[1]) < 0.2 * L: return False           # not raised above the shoulder
    nx, ny = -cy / L, cx / L                                      # unit normal
    if nx * ox < 0: nx, ny = -nx, -ny                             # make it point OUTWARD (away from the body)
    if nx * ox < 0.35: return False                               # chord nearly horizontal: out/in is ambiguous, leave it
    mx, my = (S[0] + W[0]) / 2, (S[1] + W[1]) / 2
    side = (B[0] - mx) * nx + (B[1] - my) * ny                    # > 0 = bulge outward, < 0 = inward (wrong)
    return side < -4


def centres(arms):
    """body centre x for every arm id: the mean shoulder x of the -l / -r pair of one figure (None when the figure has only one arm)"""
    g = {}
    for a in arms:
        m = re.match(r'^(mv-limb-.*)-(l|r)-1$', a['id'])
        if m: g.setdefault(m.group(1), {})[m.group(2)] = a['S'][0]
    out = {}
    for a in arms:
        m = re.match(r'^(mv-limb-.*)-(l|r)-1$', a['id'])
        d = g.get(m.group(1)) if m else None
        if d and len(d) == 2 and abs(d['l'] - d['r']) > 4: out[a['id']] = (d['l'] + d['r']) / 2
        else: out[a['id']] = a.get('fx') if a.get('fx') is not None and abs(a['S'][0] - a['fx']) > 4 else None
    return out



TOK = re.compile(r'([MLAZCQmlazcqHVhvSsTt])|(-?\d*\.?\d+(?:e-?\d+)?)')


def map_path(d, f):
    """apply the point map f to an absolute M/L/A/C/Q path (A: only the end point); None when the path uses commands this cannot map"""
    out = []; cmd = None; buf = []
    need = {'M': 2, 'L': 2, 'A': 7, 'C': 6, 'Q': 4, 'Z': 0}
    def flush():
        nonlocal buf
        if cmd is None or (not buf and cmd != 'Z'): return
        if cmd == 'A': x, y = f(buf[5], buf[6]); out.append(f'A{buf[0]:.2f},{buf[1]:.2f} {buf[2]:g} {int(buf[3])} {int(buf[4])} {x:.2f},{y:.2f}')
        elif cmd in 'MLCQ':
            pts = [f(buf[i], buf[i + 1]) for i in range(0, len(buf), 2)]
            out.append(cmd + ' '.join(f'{x:.2f},{y:.2f}' for x, y in pts))
        elif cmd == 'Z': out.append('Z')
        buf = []
    for m in TOK.finditer(d):
        if m.group(1):
            c = m.group(1)
            if c not in need: return None
            flush(); cmd = c; buf = []
            if c == 'Z': flush(); cmd = None
        else:
            if cmd is None: return None
            buf.append(float(m.group(2)))
            if len(buf) == need[cmd]: flush(); cmd = cmd if cmd != 'M' else 'L'; buf = []
    flush(); return ' '.join(out)


class _Held:   # a held group: .group(n) like a regex match, whole text in group(0)
    def __init__(self, m, txt): self.m, self.txt = m, txt
    def group(self, n): return self.txt if n == 0 else self.m.group(n)


def map_elements(inner, f):
    """apply f to every drawn element inside an arm group's inner text; None when something cannot be mapped"""
    bad = []
    def num(s, k):
        m = re.search(r'\b%s="(-?[\d.]+)"' % k, s); return float(m.group(1)) if m else None
    def rep_attr(s, k, v): return re.sub(r'\b%s="[^"]*"' % k, f'{k}="{v:.2f}"', s, count=1)
    def one(m):
        s = m.group(0); tag = m.group(1)
        if tag == 'path':
            d = re.search(r'\bd="([^"]*)"', s)
            nd = map_path(d.group(1), f) if d else None
            if nd is None: bad.append(1); return s
            return s[:d.start(1)] + nd + s[d.end(1):]
        if tag in ('circle', 'ellipse'):
            x, y = num(s, 'cx'), num(s, 'cy')
            if x is None or y is None: bad.append(1); return s
            x, y = f(x, y); return rep_attr(rep_attr(s, 'cx', x), 'cy', y)
        if tag == 'line':
            v = [num(s, k) for k in ('x1', 'y1', 'x2', 'y2')]
            if None in v: bad.append(1); return s
            (a, b), (c, d2) = f(v[0], v[1]), f(v[2], v[3])
            for k, val in zip(('x1', 'y1', 'x2', 'y2'), (a, b, c, d2)): s = rep_attr(s, k, val)
            return s
        bad.append(1); return s
    # held items / hand parts drawn in a <g transform="translate(x y) rotate(a)"> (flag, pencil, tool): rigid, moved with f and turned with the local tangent
    held = []; plain = []
    def balanced(txt, start_rx, store, tag):
        res = []; pos = 0
        while True:
            m = start_rx.search(txt, pos)
            if not m: break
            depth = 1; k = None
            for mm in re.finditer(r'<g\b[^>]*>|</g>', txt[m.end():]):
                depth += 1 if mm.group(0).startswith('<g') else -1
                if depth == 0: k = m.end() + mm.end(); break
            if k is None: break
            store.append(_Held(m, txt[m.start():k])); res.append(txt[pos:m.start()] + f'@@{tag}{len(store) - 1}@@'); pos = k
        return ''.join(res) + txt[pos:]
    held_rx = re.compile(r'<g((?: id="[^"]*")?) transform="translate\((-?[\d.]+)[ ,](-?[\d.]+)\)(?: rotate\((-?[\d.]+)\))?(?: scale\(([-\d.]+)\))?">')
    plain_rx = re.compile(r'<g(?: id="[^"]*")?>')
    inner2 = balanced(inner, held_rx, held, 'H')
    inner2 = balanced(inner2, plain_rx, plain, 'P')   # a plain group (glove, mitten, pencil): moved rigidly about its first round shape
    out = re.sub(r'<(path|circle|ellipse|line|rect|polygon|polyline)\b[^>]*?/?>', one, inner2)
    if '<g' in re.sub(r'^\s*<g transform="matrix\([^"]*\)">', '', inner2): bad.append(1)   # other nested groups
    for i, m in enumerate(held):
        x0, y0 = float(m.group(2)), float(m.group(3)); x, y = f(x0, y0); r = float(m.group(4) or 0) + (f.rot(x0, y0) if hasattr(f, 'rot') else 0)
        sc = f' scale({m.group(5)})' if m.group(5) else ''
        body = m.group(0); body = re.sub(r'^<g((?: id="[^"]*")?) transform="[^"]*">', lambda mm: f'<g{mm.group(1)} transform="translate({x:.2f} {y:.2f}) rotate({r:.2f}){sc}">', body)
        out = out.replace(f'@@H{i}@@', body)
    for i, m in enumerate(plain):
        c = re.search(r'<(?:circle|ellipse)\b[^>]*?\bcx="(-?[\d.]+)"[^>]*?\bcy="(-?[\d.]+)"', m.group(0))
        if not c: bad.append(1); continue
        ax, ay = float(c.group(1)), float(c.group(2)); x, y = f(ax, ay); r = f.rot(ax, ay) if hasattr(f, 'rot') else 0
        out = out.replace(f'@@P{i}@@', re.sub(r'^<g((?: id="[^"]*")?)>', lambda mm: f'<g{mm.group(1)} transform="translate({x:.2f} {y:.2f}) rotate({r:.2f}) translate({-ax:.2f} {-ay:.2f})">', m.group(0)))
    return None if bad else out


def bake_mirror(inner):
    """an arm mirrored by an earlier armfix run keeps <g transform="matrix(..)">..</g> as its whole content: bake the matrix into the coordinates"""
    m = re.match(r'^(\s*)<g transform="matrix\(([-\d. ]+)\)">(.*)</g>(\s*)$', inner, re.S)
    if not m: return inner
    a, b, c, d, e, f0 = map(float, m.group(2).split())
    r = map_elements(m.group(3), lambda x, y: (a * x + c * y + e, b * x + d * y + f0))
    return inner if r is None else r


def make_map(S, Wr, ox, side, L, mirror, target=0.08):
    """point map for one raised arm: optional reflection across S->W, then a smooth outward bump (peak A) so the mean bulge reaches target*L; rotate the part beyond the wrist with the end tangent"""
    cx, cy = Wr[0] - S[0], Wr[1] - S[1]; ux, uy = cx / L, cy / L; nx, ny = -uy, ux
    if nx * ox < 0: nx, ny = -nx, -ny
    s0 = -side if mirror else side
    A = max(0.0, (target * L - s0 * L) / 0.64) if s0 < 0.05 else 0.0
    phi = math.atan2(-(A * math.pi / L), 1.0) if A else 0.0         # end tangent turns toward -n
    # rotation (about W) taking u to the turned tangent, expressed in screen coordinates
    v = (ux - nx * A * math.pi / L, uy - ny * A * math.pi / L); vl = math.hypot(*v); v = (v[0] / vl, v[1] / vl)
    ang = math.atan2(ux * v[1] - uy * v[0], ux * v[0] + uy * v[1]); ca, sa = math.cos(ang), math.sin(ang)
    def f(x, y):
        if mirror:
            dx, dy = x - S[0], y - S[1]; pr = dx * ux + dy * uy; pn = dx * nx + dy * ny
            x, y = S[0] + pr * ux - pn * nx, S[1] + pr * uy - pn * ny
        if not A: return x, y
        s = ((x - S[0]) * ux + (y - S[1]) * uy) / L
        if s <= 0: return x, y
        if s < 1:
            dl = A * math.sin(math.pi * s); return x + nx * dl, y + ny * dl
        dx, dy = x - Wr[0], y - Wr[1]; return Wr[0] + ca * dx - sa * dy, Wr[1] + sa * dx + ca * dy
    def rot(x, y):
        s = ((x - S[0]) * ux + (y - S[1]) * uy) / L
        if not A or s <= 0: return 0.0
        if s >= 1: return math.degrees(ang)
        v2 = (ux + nx * A * math.pi / L * math.cos(math.pi * s), uy + ny * A * math.pi / L * math.cos(math.pi * s))
        return math.degrees(math.atan2(ux * v2[1] - uy * v2[0], ux * v2[0] + uy * v2[1]))
    f.rot = rot
    return f, A


def refl(P, u):
    ux, uy = u; L = math.hypot(ux, uy); ux, uy = ux / L, uy / L
    a, b, c, d = 2 * ux * ux - 1, 2 * ux * uy, 2 * ux * uy, 2 * uy * uy - 1
    e = P[0] - a * P[0] - c * P[1]; f = P[1] - b * P[0] - d * P[1]
    return f'transform="matrix({a:.5f} {b:.5f} {c:.5f} {d:.5f} {e:.3f} {f:.3f})"'


def inner_span(t, gid):
    """(start, end) of the inner content of <g id=gid ...> ... </g> (balanced), or None"""
    m = re.search(r'<g\b[^>]*(?:\bid="%s"|\bclass="[^"]*\b%s\b[^"]*")[^>]*>' % (re.escape(gid), re.escape(gid)), t)
    if not m: return None
    i = m.end(); depth = 1
    for mm in re.finditer(r'<g\b[^>]*>|</g>', t[i:]):
        depth += 1 if mm.group(0).startswith('<g') else -1
        if depth == 0: return i, i + mm.start()
    return None


def arms_of(pg, svg_text, W, H):
    pg.set_viewport_size({'width': W, 'height': H}); pg.set_content('<body style="margin:0">' + svg_text + '</body>')
    return pg.evaluate(JS)


def bulge(S, Wr, B, ox):
    """outward bulge of an arm as a fraction of the shoulder->wrist length (None: wrist not above the shoulder, or the chord is nearly horizontal)"""
    cx, cy = Wr[0] - S[0], Wr[1] - S[1]; L = math.hypot(cx, cy)
    if L < 1 or (S[1] - Wr[1]) < 0.2 * L: return None
    nx, ny = -cy / L, cx / L
    if nx * ox < 0: nx, ny = -nx, -ny
    if nx * ox < 0.35: return None
    return ((B[0] - (S[0] + Wr[0]) / 2) * nx + (B[1] - (S[1] + Wr[1]) / 2) * ny) / L


MIN_OUT = 0.05      # a raised arm must bulge outward by at least this fraction of its length (frog arm: ~0.14)


def bake_all(t):
    """bake the mirror wrappers an earlier armfix run left in one-shape arms (nothing changes visually)"""
    pos = 0
    while True:
        m = re.compile(r'<g\b[^>]*\bclass="[^"]*\bmv-limb-[A-Za-z0-9_-]*-1\b[^"]*"[^>]*>|<g\b[^>]*\bid="mv-limb-[A-Za-z0-9_-]*-1"[^>]*>').search(t, pos)
        if not m: return t
        gid = re.search(r'mv-limb-[A-Za-z0-9_-]*-1\b', m.group(0)).group(0); i = m.end(); depth = 1; end = None
        for mm in re.finditer(r'<g\b[^>]*>|</g>', t[i:]):
            depth += 1 if mm.group(0).startswith('<g') else -1
            if depth == 0: end = i + mm.start(); break
        pos = m.end()
        if end is None: continue
        inner = t[i:end]
        if 'mv-limb-' in inner: continue                      # two-link arm: the forearm group stays as it is
        nb = bake_mirror(inner)
        if nb != inner: t = t[:i] + nb + t[end:]; pos = i


def fix_text(t, arms, report=False):
    """returns (new_text, [fixed arm ids]); the arm list comes from the page (one entry per arm, in document order)"""
    fixed = []; cen = centres(arms)
    # work from the last arm to the first so earlier spans stay valid
    for a in reversed(arms):
        S, Wr = a['S'], a['W']; cx0 = cen.get(a['id'])
        if cx0 is None: continue                                    # unpaired arm with no figure: the body centre is unknown, leave it
        ox = 1 if S[0] >= cx0 else -1; L = math.hypot(Wr[0] - S[0], Wr[1] - S[1])
        if a['two']:
            sd = bulge(S, Wr, a['E'], ox)
            if sd is None or sd >= -4 / max(L, 1): continue
            if report: fixed.append(a['id']); continue
            E = a['E']; g2id = re.sub(r'-1$', '-2', a['id']); sp = inner_span(t, g2id)
            if not sp: continue
            tr = refl(E, (E[0] - S[0], E[1] - S[1]))
            t = t[:sp[0]] + f'<g {tr}>' + t[sp[0]:sp[1]] + '</g>' + t[sp[1]:]
            fixed.append(a['id']); continue
        sd = bulge(S, Wr, a['mean'], ox)
        if sd is None or sd >= MIN_OUT: continue
        if report: fixed.append(a['id']); continue
        sp = inner_span(t, a['id'])
        if not sp: continue
        f, A = make_map(S, Wr, ox, sd, L, mirror=sd < -0.15)
        nt = map_elements(t[sp[0]:sp[1]], f)
        if nt is None: print(f'   armfix: {a["id"]} has content that cannot be re-bent (left alone)'); continue
        t = t[:sp[0]] + nt + t[sp[1]:]; fixed.append(a['id'])
    fixed.reverse(); return t, fixed


def main(slugs, report=False, check=False):
    total = 0
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path=chrome(), args=['--no-sandbox']); pg = b.new_page()
        for slug in slugs:
            vert = 'short' in slug; W, H = (1080, 1920) if vert else (1920, 1080)
            d = f'{REPO}/videos/{slug}/art3'
            if not os.path.isdir(d): continue
            for fn in sorted(os.listdir(d)):
                if not fn.endswith('.svg'): continue
                t = open(f'{d}/{fn}', encoding='utf-8').read()
                if 'mv-limb-' not in t: continue
                if not (report or check): t = bake_all(t)
                arms = arms_of(pg, t, W, H)
                # fix from the last arm to the first so earlier spans stay valid (each fix only grows the text after its own start)
                t2, fx = fix_text(t, arms, report=report or check)
                for a in fx: print(f'{slug} {fn[:-4]} {a}: raised arm does not bulge outward' + ('' if (report or check) else ' -> re-bent'))
                total += len(fx)
                if fx and not (report or check): open(f'{d}/{fn}', 'w', encoding='utf-8').write(t2)
        b.close()
    print(f'armfix: {total} arm(s) ' + ('wrong' if (report or check) else 'fixed'))
    return total


if __name__ == '__main__':
    a = [x for x in sys.argv[1:] if not x.startswith('--')]
    if not a: a = sorted(os.listdir(f'{REPO}/videos'))
    n = main(a, report='--report' in sys.argv, check='--check' in sys.argv)
    sys.exit(1 if (n and '--check' in sys.argv) else 0)
