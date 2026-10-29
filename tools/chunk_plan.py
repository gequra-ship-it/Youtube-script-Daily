# -*- coding: utf-8 -*-
# Chunk count for the parallel render (render-chunked.yml) of an SVG page (2026-10-16, guideline 20-7).
# usage: python3 tools/chunk_plan.py render/<slug> [target_min]
# Measured: an SVG page renders in about 3.75-3.9x its length on the GitHub runner (guideline 15-5). Each chunk is one job (300 min limit);
# we aim for ~target_min (default 30) minutes of render per chunk, so a 27-min video gets ~4 chunks and finishes in about 40 min.
import sys, re, math
d = sys.argv[1]; tgt = float(sys.argv[2]) if len(sys.argv) > 2 else 30.0
html = open(d.rstrip('/') + '/index.html', encoding='utf-8').read()
dur = float(re.search(r'id="root"[^>]*data-duration="([\d.]+)"', html).group(1))
est = dur * 3.9 / 60
n = max(1, math.ceil(est / tgt))
print(f'{d}: {dur:.1f} s video -> about {est:.0f} min render in one job; suggested chunks: {n} (~{est / n:.0f} min each). '
      f'Put "<slug> {n}" in render/.chunked.')
# 2026-10-29 gate (miya): the main session must have run tools/final_check.py on THIS build; it writes render/<slug>/.checked with the sha1 of index.html
import hashlib, os
_ck = d.rstrip('/') + '/.checked'; _sha = hashlib.sha1(html.encode('utf-8')).hexdigest()
if not os.path.exists(_ck) or open(_ck).read().split()[:1] != [_sha]:
    print('WARNING: render/%s/index.html has NOT passed tools/final_check.py (missing or out of date .checked). Run `SLUG=%s python3 tools/final_check.py` and fix every problem BEFORE pushing the render.' % (os.path.basename(d.rstrip('/')), os.path.basename(d.rstrip('/'))))
    sys.exit(2)
print('final_check passed for this build (.checked matches).')
