# usage: python3 tools/armfix.py <slug>... [--report]        (no slug = every videos/<slug>)
# (2026-11-01 miya) A person's arm raised above the shoulder must curve the way a real arm does: the ELBOW stays low and out, the forearm folds up and in, so two raised arms
# make a "ヽOﾉ" shape. The curve of a raised arm must never bulge up (elbow above the shoulder-wrist line). Frog arms already do this (frog_rig.arm_bend_pass); this is the same rule for the
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
   out.push({id: gid, S, W, E, mean, two});
 });
 return out;
}
'''


def wrong_side(S, W, B):
    """True when the bulge point B lies on the wrong side of S->W for an arm whose wrist is above the shoulder (screen y grows downward)."""
    cx, cy = W[0] - S[0], W[1] - S[1]; L = math.hypot(cx, cy)
    if L < 1 or (S[1] - W[1]) < 0.2 * L: return False           # not raised above the shoulder
    nx, ny = -cy / L, cx / L                                      # unit normal
    if ny < 0: nx, ny = -nx, -ny                                  # make it point DOWN on screen
    if ny < 0.35: return False                                    # chord nearly vertical: down/out is ambiguous, leave it
    mx, my = (S[0] + W[0]) / 2, (S[1] + W[1]) / 2
    side = (B[0] - mx) * nx + (B[1] - my) * ny                    # > 0 = bulge down (right), < 0 = elbow above the chord (wrong)
    return side < -4


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


def fix_text(t, arms, report=False):
    """returns (new_text, [fixed arm ids]); the arm list comes from the page"""
    fixed = []
    for a in arms:
        S, Wr = a['S'], a['W']
        if a['two']:
            E = a['E']; bad = wrong_side(S, Wr, E)
        else:
            bad = wrong_side(S, Wr, a['mean'])
        if not bad: continue
        if report: fixed.append(a['id']); continue
        if a['two']:
            g2id = re.sub(r'-1$', '-2', a['id'])
            if g2id == a['id']: continue
            sp = inner_span(t, g2id)
            if not sp: continue
            tr = refl(E, (E[0] - S[0], E[1] - S[1]))
            t = t[:sp[0]] + f'<g {tr}>' + t[sp[0]:sp[1]] + '</g>' + t[sp[1]:]
        else:
            sp = inner_span(t, a['id'])
            if not sp: continue
            tr = refl(S, (Wr[0] - S[0], Wr[1] - S[1]))
            t = t[:sp[0]] + f'<g {tr}>' + t[sp[0]:sp[1]] + '</g>' + t[sp[1]:]
        fixed.append(a['id'])
    return t, fixed


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
                arms = arms_of(pg, t, W, H)
                # fix from the last arm to the first so earlier spans stay valid (each fix only grows the text after its own start)
                t2, fx = fix_text(t, arms, report=report or check)
                for a in fx: print(f'{slug} {fn[:-4]} {a}: raised arm bulges the wrong way' + ('' if (report or check) else ' -> mirrored'))
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
