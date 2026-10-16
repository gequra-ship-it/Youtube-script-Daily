# usage: python3 tools/labelshot.py <slug> <out_dir> U001 U002 ...   (no uids = all units)
# Preview of pictures WITH their on-screen text (sidecar "labels", guideline 3-6), all labels shown, plus a label check.
# Vertical slugs (-short1/-short2) are detected from the svg size.
import sys, os, json, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import labels_lib, palettes
from playwright.sync_api import sync_playwright
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
slug, out = sys.argv[1], sys.argv[2]; os.makedirs(out, exist_ok=True)
V = f'{REPO}/videos/{slug}'; plan = {p['uid']: p for p in json.load(open(f'{V}/plan.json'))}
uids = sys.argv[3:] or list(plan)
A = f'{REPO}/tools/assets'; bad = 0
with sync_playwright() as pw:
    b = pw.chromium.launch(executable_path='/opt/pw-browsers/chromium-1194/chrome-linux/chrome')
    for uid in uids:
        p = plan[uid]; svg = open(f'{V}/art3/{uid}.svg', encoding='utf-8').read()
        sc = json.load(open(f'{V}/art3/{uid}.json')) if os.path.exists(f'{V}/art3/{uid}.json') else {}
        vert = 'viewBox="0 0 1080 1920"' in svg; W, H = (1080, 1920) if vert else (1920, 1080)
        errs = labels_lib.check(sc, p['text'], W, H, vert)
        if errs: bad += 1; print(uid, 'PROBLEMS:', '; '.join(errs))
        inner, outer, _ = ('', '', []) if errs else labels_lib.html_for(0, sc, p['bg'], palettes.PALETTES[p.get('pal', {}).get('palette', palettes.DEFAULT)], W, H, vert)
        page = (f'<!doctype html><html><head><meta charset="utf-8"><style>@font-face{{font-family:Fredoka;src:url(file://{A}/Fredoka-700.woff2)}}'
                f'@font-face{{font-family:Patrick;src:url(file://{A}/PatrickHand-400.woff2)}}*{{margin:0;padding:0;box-sizing:border-box}}'
                f'body{{width:{W}px;height:{H}px;position:relative;overflow:hidden}}.w{{position:absolute;left:0;top:0;width:{W}px;height:{H}px}}'
                f'.w>svg{{position:absolute;left:0;top:0;width:{W}px;height:{H}px}}{labels_lib.CSS}.lab b,.badge,.labov g{{opacity:1!important}}'
                f'.cap{{position:absolute;left:0;width:{W}px;bottom:{360 if vert else 60}px;text-align:center}}.cap span{{font:700 58px/54px Fredoka;color:#fff;background:rgba(0,0,0,.62);border-radius:12px;padding:20px}}'
                f'</style></head><body><div class="w">{svg}{inner}</div>{outer}<div class="cap"><span>Caption sits here</span></div></body></html>')
        f = f'{out}/{uid}_lab.html'; open(f, 'w', encoding='utf-8').write(page)
        pg = b.new_page(viewport={'width': W, 'height': H}); pg.goto('file://' + os.path.abspath(f)); pg.wait_for_timeout(150)
        pg.screenshot(path=f'{out}/{uid}_lab.png'); pg.close()
    b.close()
print('checked', len(uids), 'units,', bad, 'with problems')
