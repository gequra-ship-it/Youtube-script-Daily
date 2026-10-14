# Split one render folder into N time chunks for parallel rendering (render-chunked.yml, 2026-10-14).
# usage: python3 tools/chunk_prep.py <slug> <n> <i>   -> writes render/<slug>__c<i>/ (assets linked, index.html rewritten)
# Every composition here is seek-safe (all motion is a function of the GSAP timeline time), so chunk i simply plays the
# main timeline from T0 = i * frames_per_chunk / FPS. Audio is removed from the chunks and muxed once after the concat.
import os, re, sys, math, json, shutil

FPS = 30
slug, n, i = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
src = f'render/{slug}'; dst = f'render/{slug}__c{i}'
html = open(f'{src}/index.html', encoding='utf-8').read()
m = re.search(r'id="root"[^>]*data-duration="([\d.]+)"', html)
total = float(m.group(1))
F = round(total * FPS); f = math.ceil(F / n)
t0 = i * f / FPS; frames = max(0, min(f, F - i * f)); L = frames / FPS
if frames == 0: raise SystemExit(f'chunk {i} is empty')
os.makedirs(dst, exist_ok=True)
for name in os.listdir(src):
    if name in ('index.html', 'renders', 'deliver') or name.startswith('.') or name.endswith('.log'): continue
    p = f'{dst}/{name}'
    if not os.path.exists(p): os.symlink(os.path.abspath(f'{src}/{name}'), p)
html = re.sub(r'<audio\b[^>]*>\s*</audio>', '', html)
html = re.sub(r'(id="root"[^>]*data-duration=")[\d.]+(")', lambda q: q.group(1) + f'{L:.6f}' + q.group(2), html, count=1)
wrap = ('<script>(function(){var m=window.__timelines.main,T0=%r,L=%r;var o=gsap.timeline({paused:true});'
        'var d={t:function(v){if(v===undefined)return T0;m.seek(v,false);}};'
        'o.fromTo(d,{t:T0},{t:T0+L,duration:L,ease:"none",immediateRender:true},0);'
        'window.__timelines.main=o;o.seek(0);})();</script>') % (t0, L)
html = html.replace('</body>', wrap + '</body>', 1) if '</body>' in html else html + wrap
open(f'{dst}/index.html', 'w', encoding='utf-8').write(html)
json.dump(dict(slug=slug, n=n, i=i, t0=t0, frames=frames, total=total), open(f'{dst}/chunk.json', 'w'))
print(f'chunk {i}/{n}: t0={t0:.3f}s frames={frames} ({L:.3f}s) of {total}s')
