# usage: python3 tools/mvcheck.py <new.svg> [<original.svg>] [outdir]
# 1) static render of new.svg must equal original.svg pixel for pixel (grouping must not change the picture)
# 2) for every id="mv-<type>-*" group: apply the pose the video uses (amplified x2 for visibility) and report changed pixels
# 3) writes <outdir>/<name>_static.png and <name>_pose.png (all groups posed at once) for a visual check
import sys, os, re, json
from playwright.sync_api import sync_playwright
import numpy as np
from PIL import Image
import io
new = sys.argv[1]; orig = sys.argv[2] if len(sys.argv) > 2 and sys.argv[2] != '-' else None
out = sys.argv[3] if len(sys.argv) > 3 else '/tmp/mvcheck'; os.makedirs(out, exist_ok=True)
name = os.path.splitext(os.path.basename(new))[0]
POSE = {'breathe': ('50% 100%', 'scaleY(1.06)'), 'nod': ('50% 100%', 'rotate(6deg)'), 'lean': ('50% 100%', 'rotate(4deg)'),
        'arm': ('50% 0%', 'rotate(28deg)'), 'hand': ('50% 100%', 'translateY(-20px) rotate(12deg)'), 'walk': ('50% 50%', 'translateX(120px)')}
def page_html(svg): return f'<html><body style="margin:0;background:#fff">{svg}</body></html>'
def shot(pg, svg, js=''):
    pg.set_content(page_html(svg)); pg.evaluate('document.documentElement.style.width="1920px"')
    if js: pg.evaluate(js)
    return np.array(Image.open(io.BytesIO(pg.screenshot(clip={'x': 0, 'y': 0, 'width': 1920, 'height': 1080}))).convert('RGB')).astype(int)
def read(p): return re.sub(r'<\?xml[^>]*\?>', '', open(p, encoding='utf-8').read()).strip()
svg = read(new); res = {}
with sync_playwright() as p:
    b = p.chromium.launch(args=['--disable-gpu']); pg = b.new_page(viewport={'width': 1920, 'height': 1080}); pg.set_default_timeout(90000)
    st = shot(pg, svg); Image.fromarray(st.astype('uint8')).save(f'{out}/{name}_static.png')
    if orig:
        o = shot(pg, read(orig)); d = int((np.abs(st - o).sum(2) > 0).sum()); res['static_diff_pixels_vs_original'] = d
    ids = re.findall(r'id="(mv-([a-z]+)-[^"]+)"', svg); groups = []
    allpose = ''
    for gid, typ in ids:
        if typ not in POSE: continue
        org, tr = POSE[typ]
        js = f'(()=>{{const e=document.getElementById("{gid}");e.style.transformBox="fill-box";e.style.transformOrigin="{org}";e.style.transform="{tr}";}})()'
        im = shot(pg, svg, js); ch = int((np.abs(im - st).sum(2) > 24).sum())
        bb = pg.evaluate(f'(()=>{{const r=document.getElementById("{gid}").getBoundingClientRect();return [Math.round(r.x),Math.round(r.y),Math.round(r.width),Math.round(r.height)]}})()')
        groups.append(dict(id=gid, type=typ, changed_px=ch, bbox=bb)); allpose += '{' + js.replace('(()=>{', '').replace('})()', '') + '}'
    res['groups'] = groups
    if allpose:
        im = shot(pg, svg, '(()=>{' + allpose + '})()'); Image.fromarray(im.astype('uint8')).save(f'{out}/{name}_pose.png')
    b.close()
print(json.dumps(res, indent=1))
