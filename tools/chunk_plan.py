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
