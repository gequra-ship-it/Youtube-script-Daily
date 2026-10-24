# -*- coding: utf-8 -*-
# Preview the new object motions and the tracking camera (guideline 4-1, 2026-10-22) of single pictures without a full build.
#   SLUG=<slug> python3 tools/motion_preview.py <out_dir> <uid> [<uid> ...] [--times 0.5,1.5,2.5,3.5,4.5] [--len 5.0]
# Writes <out_dir>/<uid>_motion.png: a strip of the picture at the given seconds (picture length --len, default 5 s), using the same
# tools/motions.py code as build3.py (obj_js for the mv-<kind>-<name> groups, track_js for the tracking camera).
import os, re, sys, json, html
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import motions
import sys; sys.path.insert(0, __import__('os').path.dirname(__import__('os').path.abspath(__file__))); from paths import chrome
from playwright.sync_api import sync_playwright
from PIL import Image

SLUG = os.environ['SLUG']; ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
args = sys.argv[1:]; times = [0.5, 1.5, 2.5, 3.5, 4.5]; plen = 5.0
if '--times' in args: i = args.index('--times'); times = [float(x) for x in args[i + 1].split(',')]; del args[i:i + 2]
if '--len' in args: i = args.index('--len'); plen = float(args[i + 1]); del args[i:i + 2]
out = args[0]; uids = args[1:]; os.makedirs(out, exist_ok=True)
art = os.environ.get('ART_DIR') or f'{ROOT}/videos/{SLUG}/art3'; W, H = (1080, 1920) if SLUG.endswith(('short1', 'short2', 'short3')) else (1920, 1080)
gsap = next((f'{ROOT}/render/{d}/gsap.min.js' for d in sorted(os.listdir(f'{ROOT}/render')) if os.path.exists(f'{ROOT}/render/{d}/gsap.min.js')))

def page(uid):
    raw = open(f'{art}/{uid}.svg', encoding='utf-8').read(); raw = re.sub(r'<\?xml[^>]*\?>', '', raw).strip()
    sc = json.load(open(f'{art}/{uid}.json')) if os.path.exists(f'{art}/{uid}.json') else {}
    def mv(m):   # id="mv-x" -> class="mv mv-x" like build3.load_svg
        tag = m.group(0); name = re.search(r'\bid="(mv-[^"]+)"', tag).group(1); tag = re.sub(r'\s*\bid="mv-[^"]+"', '', tag)
        if re.search(r'\bclass="', tag): return re.sub(r'\bclass="([^"]*)"', lambda mm: f'class="{mm.group(1)} mv {name}"', tag, 1)
        return tag[:-1].rstrip('/') + f' class="mv {name}"' + ('/>' if tag.endswith('/>') else '>')
    svg = re.sub(r'<[a-zA-Z][^>]*\bid="mv-[^"]+"[^>]*>', mv, raw)
    js = [f'<script>{motions.MOTION_JS}const tl=gsap.timeline({{paused:true}});']
    cnt = {}; n = 0
    for mt in re.finditer(r'<g\b[^>]*\bclass="[^"]*\bmv (mv-[A-Za-z0-9-]+)[^"]*"[^>]*>', svg):
        nm = mt.group(1); kind = nm.split('-')[1]; kk = cnt.get(nm, 0); cnt[nm] = kk + 1
        if kind in motions.OBJ_KINDS and nm.count('-') >= 2:
            at = dict(re.findall(r'(data-[a-z0-9]+)="([^"]*)"', mt.group(0)))
            js.extend(motions.obj_js(kind, f'gsap.utils.toArray("#w .{nm}")[{kk}]', at, 0.0, 0.0, plen + .2)); n += 1
    trk = motions.track_spec(raw, sc)
    if trk: js.append(motions.track_js(trk, '#w', 0.0, plen + .2, W, H))
    js.append('window.tl=tl;</script>')
    body = (f'<!doctype html><meta charset=utf-8><style>*{{margin:0}}html,body{{width:{W}px;height:{H}px;overflow:hidden;background:#000}}'
            f'.t{{position:absolute;left:0;top:0;width:{W}px;height:{H}px;overflow:hidden}}.w{{position:absolute;left:0;top:0;width:{W}px;height:{H}px}}'
            f'.w svg{{position:absolute;left:0;top:0;width:{W}px;height:{H}px}}</style><script src="gsap.min.js"></script>'
            f'<div class="t"><div class="w" id="w">{svg}</div></div>' + '\n'.join(js))
    return body, n, bool(trk)

with sync_playwright() as p:
    b = p.chromium.launch(executable_path=chrome(), args=['--no-sandbox'])
    pg = b.new_page(viewport={'width': W, 'height': H}); errs = []; pg.on('pageerror', lambda e: errs.append(str(e)))
    for uid in uids:
        body, n, trk = page(uid); f = f'{out}/_{uid}.html'; open(f, 'w', encoding='utf-8').write(body.replace('src="gsap.min.js"', f'src="file://{gsap}"'))
        pg.goto('file://' + os.path.abspath(f)); shots = []
        for t in times:
            pg.evaluate(f'tl.seek({t}),1'); fn = f'{out}/_{uid}_{t}.png'; pg.screenshot(path=fn); shots.append(fn)
        tw = 480 if W > H else 270; th = int(tw * H / W)
        sheet = Image.new('RGB', (tw * len(shots), th))
        for i, fn in enumerate(shots): sheet.paste(Image.open(fn).resize((tw, th)), (i * tw, 0)); os.remove(fn)
        sheet.save(f'{out}/{uid}_motion.png'); os.remove(f)
        print(uid, 'object motions:', n, '| tracking camera:', trk, '|', errs or 'no page errors')
