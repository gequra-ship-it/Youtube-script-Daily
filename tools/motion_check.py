# -*- coding: utf-8 -*-
# Motion-density check (2026-10-16, guideline 20-4): finds stretches where the picture barely moves (what viewers call "boring").
# usage: python3 tools/motion_check.py render/<slug> [--step 6] [--from 0] [--to END] [--thr 0.6]
# Works on SVG pages (window.__timelines) and cine pages (via cine-test/tools/cineshot.py). For each sample time t it renders t and t+0.5 s,
# measures the mean pixel change inside the picture area (left text block, captions and HUD edges excluded) and the change against
# the previous sample (6 s earlier). A sample is LOW when both are small: motion < thr and change < 3. Runs of LOW samples are printed.
import sys, os, glob, json, subprocess, argparse, tempfile
import numpy as np
from PIL import Image
ap = argparse.ArgumentParser(); ap.add_argument('page'); ap.add_argument('--step', type=float, default=6); ap.add_argument('--from', dest='t0', type=float, default=0)
ap.add_argument('--to', dest='t1', type=float, default=None); ap.add_argument('--thr', type=float, default=0.6); a = ap.parse_args()
page = os.path.abspath(a.page); html = open(page + '/index.html').read()
m = __import__('re').search(r'data-duration="([\d.]+)"', html)
total = float(m.group(1)) if m else float(__import__('re').search(r'"total":\s*([\d.]+)', html).group(1))
t1 = a.t1 or total - 1
ts = []; t = a.t0
while t + .5 < t1: ts += [round(t, 2), round(t + .5, 2)]; t += a.step
out = tempfile.mkdtemp(prefix='mc_')
vert = 'data-width="1080"' in html or '"w": 1080' in html
if '__timelines' in html:
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path=os.environ.get('HYPERFRAMES_BROWSER_PATH', '/opt/pw-browsers/chromium'), args=['--no-sandbox'])
        pg = b.new_page(viewport={'width': 1080 if vert else 1920, 'height': 1920 if vert else 1080})
        pg.goto('file://' + page + '/index.html'); pg.wait_for_timeout(1500)
        for x in ts:
            pg.evaluate("t => Object.values(window.__timelines).forEach(tl => { tl.pause(); tl.seek(t, false); })", x)
            pg.wait_for_timeout(80); pg.screenshot(path=f'{out}/f_{x:08.2f}.png')
        b.close()
else:
    subprocess.run([sys.executable, os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/cine-test/tools/cineshot.py', page, out] + [str(x) for x in ts], check=True, capture_output=True)
fs = {round(float(os.path.basename(f)[2:-4]), 2): f for f in glob.glob(out + '/f_*.png')}
def L(f):
    im = np.asarray(Image.open(f).convert('L').resize((270, 480) if vert else (480, 270)), dtype=np.float32)
    return im[60:380, 20:250] if vert else im[20:225, 140:400]
prev = None; low = []; rows = []
for x in sorted(k for k in fs if round((k - a.t0) / a.step, 6) % 1 == 0):
    A = L(fs[x]); Bm = L(fs.get(round(x + .5, 2), fs[x]))
    mo = float(np.abs(A - Bm).mean()); ch = float(np.abs(A - prev).mean()) if prev is not None else 99; prev = A
    rows.append((x, mo, ch)); lo = mo < a.thr and ch < 3
    print(f'{x:8.1f} {int(x // 60)}:{int(x % 60):02d}  motion {mo:5.2f}  change {ch:5.2f}' + ('  LOW' if lo else ''))
    if lo: low.append(x)
runs = []; 
for x in low:
    if runs and x - runs[-1][1] <= a.step + .01: runs[-1][1] = x
    else: runs.append([x, x])
print('low-motion stretches:', ', '.join(f'{int(s // 60)}:{int(s % 60):02d}-{int((e + a.step) // 60)}:{int((e + a.step) % 60):02d}' for s, e in runs) or 'none')
