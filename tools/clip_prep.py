# usage: python3 tools/clip_prep.py <slug> <t0> <len>   -> render/<slug>__clip/ (same trick as chunk_prep.py, any time range; for short sample clips)
# then: cd render/<slug>__clip && npx --yes hyperframes@0.8.141 render ; mux the audio part with ffmpeg -ss <t0> -t <len> from render/<slug>/<audio src>.
import os, re, sys, json
slug, t0, L = sys.argv[1], float(sys.argv[2]), float(sys.argv[3])
src = f'render/{slug}'; dst = f'render/{slug}__clip'
html = open(f'{src}/index.html', encoding='utf-8').read()
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
json.dump(dict(slug=slug, t0=t0, len=L), open(f'{dst}/chunk.json', 'w'))
print('clip', t0, L)
