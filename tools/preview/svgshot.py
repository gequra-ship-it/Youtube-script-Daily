# usage: python3 svgshot.py out_dir file1.svg [file2.svg ...]   -> out_dir/<name>.png (viewBox size; set SHOT_W/SHOT_H for vertical)
import os as _o, sys as _s; _T = _o.path.dirname(_o.path.dirname(_o.path.abspath(__file__))); _s.path[:0] = [_T] + [_T + '/' + _d for _d in ('build', 'check', 'fix', 'preview', 'writing')]   # tools root (libraries) + sibling folders, 2026-11-14 layout
import sys, os, asyncio
import sys; sys.path.insert(0, __import__('os').path.dirname(__import__('os').path.abspath(__file__))); from paths import chrome
from playwright.sync_api import sync_playwright
out = sys.argv[1]; os.makedirs(out, exist_ok=True)
W = int(os.environ.get('SHOT_W', 1920)); H = int(os.environ.get('SHOT_H', 1080))
with sync_playwright() as p:
    b = p.chromium.launch(executable_path=chrome())
    pg = b.new_page(viewport={'width': W, 'height': H})
    for f in sys.argv[2:]:
        pg.goto('file://' + os.path.abspath(f)); pg.screenshot(path=f'{out}/{os.path.basename(f)[:-4]}.png')
    b.close()
