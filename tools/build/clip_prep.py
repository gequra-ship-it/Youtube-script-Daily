# usage: python3 tools/build/clip_prep.py <slug> <t0> <len>   -> render/<slug>__clip/ (same trick as chunk_prep.py, any time range; for short sample clips)
# then: cd render/<slug>__clip && npx --yes hyperframes@0.8.141 render ; mux the audio part with ffmpeg -ss <t0> -t <len> from render/<slug>/<audio src>.
import os as _o, sys as _s; _T = _o.path.dirname(_o.path.dirname(_o.path.abspath(__file__))); _s.path[:0] = [_T] + [_T + '/' + _d for _d in ('build', 'check', 'fix', 'preview', 'writing')]   # tools root (libraries) + sibling folders, 2026-11-14 layout
import os, re, sys, json
slug, t0, L = sys.argv[1], float(sys.argv[2]), float(sys.argv[3])
src = f'render/{slug}'; dst = f'render/{slug}__clip'
html = open(f'{src}/index.html', encoding='utf-8').read()
os.makedirs(dst, exist_ok=True)
for name in os.listdir(src):
    if name in ('index.html', 'renders', 'deliver') or name.startswith('.') or name.endswith('.log'): continue
    p = f'{dst}/{name}'
    if not os.path.exists(p): os.symlink(os.path.abspath(f'{src}/{name}'), p)
# 2026-11-14: the assets every video shares (fonts, logo, grain, gsap, anime) are no longer committed under render/<slug>/; link them from tools/assets
_A = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'assets')
for name in ('Fredoka-700.woff2', 'PatrickHand-400.woff2', 'logo.png', 'grain.png', 'gsap.min.js', 'anime.min.js', 'gsap'):
    p = f'{dst}/{name}'
    if not os.path.lexists(p) and os.path.exists(f'{_A}/{name}'): os.symlink(os.path.abspath(f'{_A}/{name}'), p)
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
