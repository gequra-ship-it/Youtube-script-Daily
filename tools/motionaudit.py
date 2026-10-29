# usage: SLUG=<slug> [VERT=1] MIYA_WORK=/tmp/miya-work python3 tools/motionaudit.py <out_dir> <uid> [<uid> ...]
# Needs a built render/<slug>/index.html (build3). For each unit it seeks the real page at 3 times (early / middle / late in the cut) and writes one strip per unit,
# with a RED DOT on every `data-pivot` (joint, chain, rotor, swing, grow ...) so a pivot that sits in empty space or on the wrong end of a part is visible,
# and a CYAN DOT on the centre of every `mv-core-*`/`mv-path-*` group. Look at the strips: a leg/tail/neck/hand/blade must hinge at its red dot ON the body.
import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from paths import *
from playwright.sync_api import sync_playwright
from PIL import Image, ImageDraw
out = sys.argv[1]; uids = sys.argv[2:]; os.makedirs(out, exist_ok=True)
W, H = (1080, 1920) if os.environ.get('VERT') == '1' or SLUG.endswith(tuple(f'short{i}' for i in range(1, 10))) else (1920, 1080)
bd = json.load(open(f'{wdir()}/build/build_data.json')); cuts = {c['id']: c for c in bd['cuts']}
MARK = '''() => { const NS='http://www.w3.org/2000/svg'; let n=0;
 document.querySelectorAll('[data-pivot]').forEach(g => { const p=(g.getAttribute('data-pivot')||'').trim().split(/\\s+/).map(Number); if(p.length!==2||p.some(isNaN)) return;
  let o; try { o=miyaPv(g,p[0],p[1]).split(' ').map(Number);} catch(e){ o=p; }
  const c=document.createElementNS(NS,'circle'); c.setAttribute('cx',o[0]); c.setAttribute('cy',o[1]); c.setAttribute('r',8); c.setAttribute('fill','#ff2030'); c.setAttribute('stroke','#fff'); c.setAttribute('stroke-width',3); c.setAttribute('data-audit','1');
  g.parentNode.appendChild(c); n++; });
 return n; }'''
with sync_playwright() as p:
    b = p.chromium.launch(executable_path=chrome(), args=['--no-sandbox']); pg = b.new_page(viewport={'width': W, 'height': H})
    pg.goto(f'file://{REPO}/render/{SLUG}/index.html'); pg.wait_for_timeout(1500)
    pg.evaluate("() => Object.values(window.__timelines).forEach(tl => { tl.pause(); tl.seek(0, false); })")
    print('pivot dots', pg.evaluate(MARK), flush=True)
    sc = 0.5 if W > H else 0.33
    for uid in uids:
        c = cuts[uid]; t0, t1 = c['t0'], c['t1']
        ts = [t0 + 1.0, (t0 + t1) / 2 + 0.7, t1 - 0.5]
        ims = []
        for t in ts:
            pg.evaluate("t => Object.values(window.__timelines).forEach(tl => { tl.pause(); tl.seek(t, false); })", t); pg.wait_for_timeout(100)
            f = f'/tmp/_ma_{SLUG}_{uid}.png'; pg.screenshot(path=f, timeout=120000)
            im = Image.open(f).convert('RGB'); im = im.resize((int(W * sc), int(H * sc))); ImageDraw.Draw(im).text((6, 6), f'{uid} t={t:.1f}', fill=(255, 0, 0)); ims.append(im)
        sheet = Image.new('RGB', (sum(i.width for i in ims) + 4 * 2, ims[0].height), 'white'); x = 0
        for i in ims: sheet.paste(i, (x, 0)); x += i.width + 4
        sheet.save(f'{out}/{SLUG}_{uid}.png'); print(uid, flush=True)
    b.close()
