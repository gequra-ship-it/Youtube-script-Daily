# Miya's Lab HDRI prep (2026-10-15): a Radiance .hdr environment (e.g. CC0 from polyhaven.com/hdris, 1k is enough for lighting)
# -> a page-ready file that scenes use synchronously with MIYA.kit.hdri(name, renderer): image-based light and reflections from a
# real photographed sky (night pond, forest, desert...). Pixels stay RGBE (4 bytes, base64); kit.js decodes them to floats.
#   python3 tools/hdri_prep.py <file.hdr> <name> --credit "..." [--width 1024] [--out tools/cine/models]
# A scene lists it like a model: "// models: pond_bridge_night" (build_cine copies <name>.js from the same folders).
import os, sys, re, json, base64, argparse
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from paths import REPO

ap = argparse.ArgumentParser()
ap.add_argument('src'); ap.add_argument('name'); ap.add_argument('--credit', required=True)
ap.add_argument('--width', type=int, default=1024); ap.add_argument('--out', default=f'{REPO}/tools/cine/models')
a = ap.parse_args()

def read_hdr(path):
    b = open(path, 'rb').read(); i = 0
    while True:   # header lines until an empty line, then the resolution line
        j = b.index(b'\n', i); line = b[i:j]; i = j + 1
        if line == b'': break
        if line.startswith(b'FORMAT') and b'32-bit_rle_rgbe' not in line: raise SystemExit('only RGBE .hdr is supported')
    j = b.index(b'\n', i); m = re.match(rb'-Y (\d+) \+X (\d+)', b[i:j]); i = j + 1
    if not m: raise SystemExit('unsupported orientation ' + b[i:j].decode())
    h, w = int(m.group(1)), int(m.group(2)); out = np.zeros((h, w, 4), np.uint8); d = np.frombuffer(b, np.uint8)
    for y in range(h):
        if d[i] == 2 and d[i + 1] == 2 and (int(d[i + 2]) << 8 | int(d[i + 3])) == w:   # new-style RLE scanline, one channel at a time
            i += 4
            for c in range(4):
                x = 0
                while x < w:
                    n = int(d[i]); i += 1
                    if n > 128: n -= 128; out[y, x:x + n, c] = d[i]; i += 1
                    else: out[y, x:x + n, c] = d[i:i + n]; i += n
                    x += n
        else: out[y] = d[i:i + w * 4].reshape(w, 4); i += w * 4
    return out

px = read_hdr(a.src)
if px.shape[1] > a.width:   # box-downscale in float, then back to RGBE
    f = px[..., :3].astype(np.float32) * np.ldexp(1.0, px[..., 3:4].astype(np.int32) - 136)
    k = px.shape[1] // a.width; f = f[:f.shape[0] // k * k, :f.shape[1] // k * k].reshape(f.shape[0] // k, k, f.shape[1] // k, k, 3).mean((1, 3))
    mx = f.max(-1); e = np.where(mx > 1e-32, np.floor(np.log2(np.maximum(mx, 1e-32))) + 1, -128)
    sc = np.where(mx > 1e-32, 256.0 / np.ldexp(1.0, e.astype(np.int32)), 0)
    px = np.concatenate([np.clip(f * sc[..., None], 0, 255).astype(np.uint8), np.clip(e + 128, 0, 255).astype(np.uint8)[..., None]], -1)
h, w = px.shape[:2]
data = {'w': w, 'h': h, 'rgbe': base64.b64encode(np.ascontiguousarray(px).tobytes()).decode()}
os.makedirs(a.out, exist_ok=True)
open(f'{a.out}/{a.name}.js', 'w').write(f'(window.MIYA = window.MIYA || {{}}).hdris = window.MIYA.hdris || {{}};\nwindow.MIYA.hdris[{json.dumps(a.name)}] = {json.dumps(data)};\n')
open(f'{a.out}/{a.name}.txt', 'w').write(a.credit.strip() + '\n')
print(f'{a.out}/{a.name}.js  {w}x{h}  {os.path.getsize(f"{a.out}/{a.name}.js") / 1e6:.1f} MB')
