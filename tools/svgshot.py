# usage: python3 svgshot.py out_dir file1.svg [file2.svg ...]   -> out_dir/<name>.png (viewBox size; set SHOT_W/SHOT_H for vertical)
import sys, os, asyncio
from playwright.sync_api import sync_playwright
out = sys.argv[1]; os.makedirs(out, exist_ok=True)
W = int(os.environ.get('SHOT_W', 1920)); H = int(os.environ.get('SHOT_H', 1080))
with sync_playwright() as p:
    b = p.chromium.launch(executable_path='/opt/pw-browsers/chromium-1194/chrome-linux/chrome')
    pg = b.new_page(viewport={'width': W, 'height': H})
    for f in sys.argv[2:]:
        pg.goto('file://' + os.path.abspath(f)); pg.screenshot(path=f'{out}/{os.path.basename(f)[:-4]}.png')
    b.close()
