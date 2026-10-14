# Preview and cost check for cine pages (2026-10-14).
#   python3 tools/cineshot.py <render dir> <out dir> <t> [<t> ...]     screenshots at those times (+ seconds per frame, page errors)
#   python3 tools/cineshot.py <render dir> --estimate [samples]         times ~24 evenly spread frames and suggests the chunk count
# The render server has no GPU; measured 2026-10-14: it is about 2-3x slower per frame than this container (cubefield 6 s/frame
# there vs ~2.5 s here; dataglobe ~0.6 s vs ~0.8 s). The estimate uses 3x and keeps every chunk under ~150 minutes.
import sys, os, json, re, time, math, asyncio
from playwright.async_api import async_playwright

def chrome():
    for p in ('/opt/pw-browsers/chromium', None):
        if p is None or os.path.exists(p): return p

async def run(rdir, ts, outdir):
    html = open(f'{rdir}/index.html').read(); m = re.search(r'data-width="(\d+)" data-height="(\d+)"', html); W, H = int(m.group(1)), int(m.group(2))
    async with async_playwright() as p:
        kw = dict(args=['--disable-gpu', '--no-sandbox']); c = chrome()
        if c: kw['executable_path'] = c
        b = await p.chromium.launch(**kw); pg = await b.new_page(viewport={'width': W, 'height': H}); logs = []
        pg.on('console', lambda m: logs.append(f'{m.type}: {m.text}') if 'GL Driver' not in m.text and m.type in ('error', 'warning') else None)
        pg.on('pageerror', lambda e: logs.append(f'PAGE ERROR {e}'))
        await pg.goto('file://' + os.path.abspath(rdir) + '/index.html'); await pg.wait_for_timeout(2000)
        if not await pg.evaluate('!!window.MIYA_CINE_READY'): logs.append('PAGE ERROR cine runtime did not start')
        res = []
        for t in ts:
            s = time.time(); await pg.evaluate('t=>{window.__timelines.main.seek(t)}', t)
            if outdir: await pg.screenshot(path=f'{outdir}/f_{t:07.2f}.png')
            else: await pg.screenshot(type='jpeg', quality=50)
            res.append((t, time.time() - s))
        await b.close()
    return res, logs, html

if __name__ == '__main__':
    rdir = sys.argv[1]
    if len(sys.argv) > 2 and sys.argv[2] == '--estimate':
        n = int(sys.argv[3]) if len(sys.argv) > 3 else 24
        total = float(re.search(r'id="root"[^>]*data-duration="([\d.]+)"', open(f'{rdir}/index.html').read()).group(1))
        ts = [total * (k + .5) / n for k in range(n)]
        res, logs, _ = asyncio.run(run(rdir, ts, None))
        avg = sum(s for _, s in res[1:]) / max(1, len(res) - 1); ci = avg * 3 * total * 30   # 30 fps
        chunks = max(1, min(20, math.ceil(ci / (150 * 60))))
        for t, s in res: print(f'{t:8.2f}s  {s:5.2f} s/frame')
        print(f'average {avg:.2f} s/frame here -> about {ci / 60:.0f} min on the render server in total; suggested chunks: {chunks} (~{ci / 60 / chunks:.0f} min each)')
    else:
        out = sys.argv[2]; os.makedirs(out, exist_ok=True)
        res, logs, _ = asyncio.run(run(rdir, [float(x) for x in sys.argv[3:]], out))
        for t, s in res: print(f'{t:8.2f}s  {s:5.2f} s/frame  -> {out}/f_{t:07.2f}.png')
    if logs: print('PAGE MESSAGES:\n  ' + '\n  '.join(logs[:20]))
