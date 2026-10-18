# usage: SLUG=<slug> python3 tools/thumb_shot.py   -> render/<slug>/deliver/<slug>_thumbnail_A..F.png (A-C since 2026-10-16; D-F only if thumb/D.html.. exist)
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from paths import *
from playwright.sync_api import sync_playwright
out = f'{REPO}/render/{SLUG}/deliver'; os.makedirs(out, exist_ok=True)
CHROME = os.environ.get('HYPERFRAMES_BROWSER_PATH', '/opt/pw-browsers/chromium-1194/chrome-linux/chrome')
with sync_playwright() as p:
    b = p.chromium.launch(executable_path=CHROME)
    pg = b.new_page(viewport={'width': 1920, 'height': 1080}); errs = []
    pg.on('pageerror', lambda e: errs.append(str(e)))
    for n in [x for x in ['A', 'B', 'C', 'D', 'E', 'F'] if os.path.exists(f'{vdir()}/thumb/{x}.html')]:
        pg.goto(f'file://{vdir()}/thumb/{n}.html'); pg.wait_for_timeout(500)
        ok = pg.evaluate("document.fonts.check('700 100px Fredoka')")
        f = f'{out}/{SLUG}_thumbnail_{n}.png'; pg.screenshot(path=f)
        print(n, 'font', ok, os.path.getsize(f), 'bytes')
    print('errors', errs); b.close()
