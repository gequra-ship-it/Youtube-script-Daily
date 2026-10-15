# Probe: camera position/forward per scene type and time (for the camera director's pivot distances). usage: python3 tools/camprobe.py <render dir>
import sys, os, json, asyncio
from playwright.async_api import async_playwright
JS = '''() => { const D = window.MIYA_DEBUG, out = []; const T = THREE; let LK = null; const lk0 = T.Object3D.prototype.lookAt; T.Object3D.prototype.lookAt = function(x, y, z) { LK = (x && x.isVector3) ? x.clone() : new T.Vector3(x, y, z); return lk0.call(this, x, y, z); };
  D.SHOTS.forEach((s, i) => { const o = D.shotObj(i); const rows = [];
    for (const f of [.02, .25, .5, .75, .98]) { const t = s.t0 + (s.t1 - s.t0) * f; o.draw(t, t - s.t0); o.camera.updateMatrixWorld(true);
      const p = o.camera.position, fw = new T.Vector3(0, 0, -1).applyQuaternion(o.camera.quaternion);
      const toO = p.clone().negate().normalize(); const dl = LK ? +p.distanceTo(LK).toFixed(2) : null; LK = null;
      rows.push({ f, pos: p.toArray().map(v => +v.toFixed(2)), fwd: fw.toArray().map(v => +v.toFixed(3)), dist0: +p.length().toFixed(2), dlook: dl, ang0: +(Math.acos(Math.min(1, Math.max(-1, fw.dot(toO)))) * 57.3).toFixed(1), fov: o.camera.fov }); }
    out.push({ i, type: s.type, t0: s.t0, t1: s.t1, rows }); });
  return out; }'''
async def run(rdir):
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path='/opt/pw-browsers/chromium', args=['--disable-gpu', '--no-sandbox'])
        pg = await b.new_page(viewport={'width': 1920, 'height': 1080}); errs = []
        pg.on('pageerror', lambda e: errs.append(str(e)))
        await pg.goto('file://' + os.path.abspath(rdir) + '/index.html'); await pg.wait_for_timeout(2500)
        r = await pg.evaluate(JS); await b.close(); return r, errs
if __name__ == '__main__':
    r, errs = asyncio.run(run(sys.argv[1]))
    for s in r:
        print(f"shot {s['i']:2d} {s['type']:12s} {s['t0']:7.1f}-{s['t1']:7.1f}")
        for w in s['rows']: print(f"     f={w['f']:.2f} pos={w['pos']} fwd={w['fwd']} |pos|={w['dist0']} angToOrigin={w['ang0']} dLook={w['dlook']} fov={w['fov']}")
    if errs: print('ERRORS', errs[:5])
