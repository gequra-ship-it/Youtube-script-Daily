# usage: SLUG=<slug> [VERT=1] python3 tools/frogshot.py <out.png> <t1,t2,...>
# Seeks the built render/<slug>/index.html timeline to the given seconds and writes a contact strip (to check the frog explainer / any frame).
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from paths import *
from playwright.sync_api import sync_playwright
from PIL import Image
out = sys.argv[1]; times = [float(x) for x in sys.argv[2].split(',')]
W, H = (1080, 1920) if os.environ.get('VERT') == '1' or SLUG.endswith(tuple(f'short{i}' for i in range(1, 10))) else (1920, 1080)
ims = []
with sync_playwright() as p:
    b = p.chromium.launch(executable_path=chrome(), args=['--no-sandbox']); pg = b.new_page(viewport={'width': W, 'height': H})
    pg.goto(f'file://{REPO}/render/{SLUG}/index.html'); pg.wait_for_timeout(1500); print('loaded', flush=True)
    for t in times:
        pg.evaluate("t => Object.values(window.__timelines).forEach(tl => { tl.pause(); tl.seek(t, false); })", t); pg.wait_for_timeout(120)
        f = f'/tmp/_fs_{t}.png'; pg.screenshot(path=f, timeout=120000); print(t, flush=True); ims.append(Image.open(f).convert('RGB'))
    b.close()
h = 640; ims = [i.resize((int(i.width * h / i.height), h)) for i in ims]
sheet = Image.new('RGB', (sum(i.width for i in ims) + 6 * (len(ims) - 1), h), 'white'); x = 0
for i in ims: sheet.paste(i, (x, 0)); x += i.width + 6
sheet.save(out); print(out, sheet.size)
