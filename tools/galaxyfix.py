# usage: python3 tools/galaxyfix.py <slug>... [--report]
# (2026-10-30 miya) A galaxy drawn tilted (flattened ellipse) must spin IN ITS OWN PLANE about its centre axis, clockwise, like a disc seen at an angle, not rotate as a flat picture.
# For every spin-type galaxy group (mv-core-spin-*, mv-spin-*, mv-rotor-* with 'galax' in the name) whose drawing is flattened (minor/major < .88) this rewrites the group id to
# mv-disc-galaxy[-x] with data-tilt / data-ratio / data-cx / data-cy measured from the rendered shape (alpha moments); motions.obj_js 'disc' does the in-plane turn. Idempotent.
import os, re, sys, io
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from paths import REPO, chrome
from playwright.sync_api import sync_playwright
from PIL import Image
import numpy as np
SPIN = re.compile(r'mv-(core-spin|spin|rotor)-?[a-z0-9-]*galax[a-z0-9-]*|mv-(core-spin|spin|rotor)-galax[a-z0-9-]*')


def measure(pg, svg_text, gid, W, H):
    pg.set_viewport_size({'width': W, 'height': H})
    css = '<style>html,body{margin:0;background:transparent}svg *{visibility:hidden}#%s,#%s *{visibility:visible}</style>' % (gid, gid)
    pg.set_content('<html><head>' + css + '</head><body>' + svg_text + '</body></html>')
    im = Image.open(io.BytesIO(pg.screenshot(omit_background=True))).convert('RGBA')
    al = np.array(im)[:, :, 3]
    ys, xs = np.nonzero(al > 128)
    if len(xs) < 200: return None
    cx, cy = xs.mean(), ys.mean(); dx, dy = xs - cx, ys - cy
    cov = np.array([[np.mean(dx * dx), np.mean(dx * dy)], [np.mean(dx * dy), np.mean(dy * dy)]])
    w, v = np.linalg.eigh(cov); major = v[:, 1]
    ang = float(np.degrees(np.arctan2(major[1], major[0])))
    return dict(cx=float(cx), cy=float(cy), tilt=ang, ratio=float(np.sqrt(max(w[0], 1e-6) / max(w[1], 1e-6))))


def main(slugs, report=False):
    n = 0
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path=chrome(), args=['--no-sandbox']); pg = b.new_page()
        for slug in slugs:
            vert = 'short' in slug; W, H = (1080, 1920) if vert else (1920, 1080)
            d = f'{REPO}/videos/{slug}/art3'
            for fn in sorted(os.listdir(d)):
                if not fn.endswith('.svg'): continue
                t = open(f'{d}/{fn}', encoding='utf-8').read()
                for m in re.finditer(r'<g id="(mv-(?:core-spin|spin|rotor)-[a-z0-9-]*)"([^>]*)>', t):
                    gid, rest = m.group(1), m.group(2)
                    if 'galax' not in gid or 'transform=' in rest: continue
                    me = measure(pg, t, gid, W, H)
                    if not me: continue
                    flat = me['ratio'] < .88
                    print(f'{slug} {fn[:-4]} {gid} ratio {me["ratio"]:.2f} tilt {me["tilt"]:.0f} {"-> disc" if flat else "(face-on, plain spin)"}')
                    if not flat or report: continue
                    per = re.search(r'data-per="([\d.]+)"', rest); per = per.group(1) if per else '24'
                    new = f'<g id="mv-disc-galaxy{gid.split("galaxy", 1)[1]}" data-tilt="{me["tilt"]:.1f}" data-ratio="{me["ratio"]:.3f}" data-cx="{me["cx"]:.1f}" data-cy="{me["cy"]:.1f}" data-per="{per}" data-dir="1" data-pivot="{me["cx"]:.0f} {me["cy"]:.0f}" data-keep="1">'
                    t = t.replace(m.group(0), new, 1); n += 1
                    open(f'{d}/{fn}', 'w', encoding='utf-8').write(t)
        b.close()
    print('galaxyfix:', n, 'galaxies converted')


if __name__ == '__main__':
    a = [x for x in sys.argv[1:] if not x.startswith('--')]
    main(a, '--report' in sys.argv)
