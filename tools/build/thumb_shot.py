# shorts (slug ends -shortN): VERTICAL 1080x1920, only A.html (guideline 16-9, 2026-11-06)
# usage: SLUG=<slug> python3 tools/build/thumb_shot.py   -> render/<slug>/deliver/<slug>_thumbnail_A..F.png (A-C since 2026-10-16; D-F only if thumb/D.html.. exist)
import os as _o, sys as _s; _T = _o.path.dirname(_o.path.dirname(_o.path.abspath(__file__))); _s.path[:0] = [_T] + [_T + '/' + _d for _d in ('build', 'check', 'fix', 'preview', 'writing')]   # tools root (libraries) + sibling folders, 2026-11-14 layout
import os, sys, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from paths import *
from playwright.sync_api import sync_playwright
out = f'{REPO}/render/{SLUG}/deliver'; os.makedirs(out, exist_ok=True)
CHROME = chrome()
SHORT = bool(re.search(r'-short\d+$', SLUG)); W, H = (1080, 1920) if SHORT else (1920, 1080)
with sync_playwright() as p:
    b = p.chromium.launch(executable_path=CHROME)
    pg = b.new_page(viewport={'width': W, 'height': H}); errs = []
    pg.on('pageerror', lambda e: errs.append(str(e)))
    for n in [x for x in (['A'] if SHORT else ['A', 'B', 'C', 'D', 'E', 'F']) if os.path.exists(f'{vdir()}/thumb/{x}.html')]:
        pg.goto(f'file://{vdir()}/thumb/{n}.html'); pg.wait_for_timeout(500)
        ok = pg.evaluate("document.fonts.check('700 100px Fredoka')")
        f = f'{out}/{SLUG}_thumbnail_{n}.png'; pg.screenshot(path=f); assert not SHORT or os.path.getsize(f) < 2_000_000, 'over 2MB'
        import eyecheck; _n, _bad = eyecheck.check(f'{vdir()}/thumb/{n}.html'); print('EYES', 'BAD pupil outside eye white: ' + str(_bad) if _bad else f'ok ({_n})')
        print(n, 'font', ok, os.path.getsize(f), 'bytes')
    print('errors', errs); b.close()
