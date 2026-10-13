# Re-style the centre-object motion of an ALREADY BUILT render folder, without rebuilding (no TTS, no pictures needed).
# usage: python3 tools/restyle_motion.py render/<slug> [render/<slug2> ...]
# Rewrites render/<slug>/index.html in place:
#   * every `mv-glint-core` motion line -> one of the 13 centre motions (same rotation build3.py uses: motions.legacy_core_type)
#   * light groups (glint/lamp/lantern/beacon) that still squash vertically -> in-place glow pulse
#   * adds miyaWrapCores() so the motion moves the visible object, not just its glow (guideline 4-1)
# Audio (mix.m4a), pictures, subtitles, transitions and camera are not touched. Running it twice does nothing the second time.
import re, sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import motions

TIN = {'hard': 0.0, 'zoom': 0.5, 'fade': 0.6, 'slide': 0.7, 'match': 0.9, 'wash': 0.0}   # same table as build3.py


def entry_kind(block):
    if re.search(r'scale:2\.4,opacity:0', block): return 'zoom'
    if re.search(r'\{opacity:0\},\{opacity:1,duration:\.6', block): return 'fade'
    if re.search(r'\{x:\d+\},\{x:0,duration:\.7', block): return 'slide'
    if 'clipPath:"circle(120px' in block: return 'match'
    return 'wash'          # wash and hard cut both have t0 == v0


def restyle(path):
    s = open(path, encoding='utf-8').read()
    if 'miyaWrapCores' in s:
        print(path, ': already restyled, skipped'); return False
    i = s.rindex('const tl=gsap.timeline')
    head, js = s[:i], s[i:]
    cx, cy = (540, 860) if 'transformOrigin:"540px 860px"' in js else (960, 500)
    lines = js.split('\n')
    # unit windows: v0 from the "display:block" set, t1 from the "display:none" set
    win = {}
    for l in lines:
        m = re.match(r'tl\.set\("#t(\d+)",\{display:"block"\},([\d.]+)\);tl\.set\("#t\1",\{display:"none"\},([\d.]+)\);', l)
        if m: win[int(m.group(1))] = (float(m.group(2)), float(m.group(3)))
    out, ordinal, n_core, n_glow = [], 0, 0, 0
    cur = None
    block_of = {}
    for l in lines:                      # first pass: collect each unit's lines to find its entry transition
        m = re.match(r'tl\.set\("#t(\d+)",\{display:"block"\}', l)
        if m: cur = int(m.group(1))
        if cur is not None: block_of.setdefault(cur, []).append(l)
    for l in lines:
        m = re.match(r'tl\.fromTo\(gsap\.utils\.toArray\("#w(\d+) \.(mv-[A-Za-z0-9-]+)"\)\[(\d+)\],', l)
        if m and 'scaleY:1.14,scaleX:.92' in l:
            n, cls, kk = int(m.group(1)), m.group(2), int(m.group(3)); v0, t1 = win[n]; sp = t1 - v0 + 0.2
            g = f'gsap.utils.toArray("#w{n} .{cls}")[{kk}]'
            if cls == 'mv-glint-core':
                t0 = v0 + TIN[entry_kind('\n'.join(block_of[n]))]
                ct = motions.legacy_core_type(ordinal); ordinal += 1; n_core += 1
                out.extend(motions.core_js(ct, g, t0, v0, sp)); continue
            if re.match(r'mv-(glint|lamp|lantern|beacon)', cls):
                per = {'glint': 1.4, 'lamp': 1.2, 'lantern': 1.3, 'beacon': 1.5}[cls.split('-')[1]] * (1 + 0.13 * (kk % 3)); rep = int(math.ceil(sp / per)) - 1
                out.append(f'tl.fromTo({g},{{scale:1,opacity:.85,transformOrigin:"50% 50%"}},{{scale:1.06,opacity:1,duration:{per:.3f},ease:"sine.inOut",yoyo:true,repeat:{rep},immediateRender:false}},{v0:.3f});')
                n_glow += 1; continue
        out.append(l)
    new_js = '\n'.join(out).replace('const tl=gsap.timeline', motions.WRAP_JS + f'miyaWrapCores({cx},{cy});const tl=gsap.timeline', 1)
    open(path, 'w', encoding='utf-8').write(head + new_js)
    print(path, f': {n_core} centre motions, {n_glow} light groups changed, centre ({cx},{cy})')
    return True


if __name__ == '__main__':
    for d in sys.argv[1:]:
        restyle(d.rstrip('/') + '/index.html')
