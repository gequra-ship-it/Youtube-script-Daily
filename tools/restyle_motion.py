# Re-style an ALREADY BUILT render folder to the current motion rules, without rebuilding (no TTS, no pictures needed).
# usage: python3 tools/restyle_motion.py render/<slug> [render/<slug2> ...]
# Rewrites render/<slug>/index.html in place:
#   * every `mv-glint-core` motion line -> one of the 19 centre motions (same rotation build3.py uses: motions.legacy_core_type)
#   * light groups (glint/lamp/lantern/beacon) that still squash vertically -> in-place glow pulse
#   * adds miyaWrapCores() so the motion moves the visible object, not just its glow (guideline 4-1)
#   * chalkboard text is shrunk to fit its card (motions.CHALK_FIT_JS, guideline 7)
#   * number badges count up (labels_lib.count_span/count_js, guideline 3-6)
#   * focus spotlight dims the picture while the camera pushes in (guideline 4-1)
#   * the spoken subtitle word turns yellow (caption_hl, guideline 5)
# Audio (mix.m4a), pictures, transitions and camera moves are not touched. Run it on the ORIGINAL build3 output:
# a file that already has miyaWrapCores is skipped.
import re, sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import motions, labels_lib, caption_hl

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
    vert = 'transformOrigin:"540px 860px"' in js
    cx, cy = (540, 860) if vert else (960, 500)
    W, H = (1080, 1920) if vert else (1920, 1080)
    lines = js.split('\n')
    # unit windows: v0 from the "display:block" set, t1 from the "display:none" set
    win = {}
    for l in lines:
        m = re.match(r'tl\.set\("#t(\d+)",\{display:"block"\},([\d.]+)\);tl\.set\("#t\1",\{display:"none"\},([\d.]+)\);', l)
        if m: win[int(m.group(1))] = (float(m.group(2)), float(m.group(3)))
    cur = None; block_of = {}
    for l in lines:                      # first pass: collect each unit's lines to find its entry transition
        m = re.match(r'tl\.set\("#t(\d+)",\{display:"block"\}', l)
        if m: cur = int(m.group(1))
        if cur is not None: block_of.setdefault(cur, []).append(l)
    caps = {}                            # caption k -> its text, for the word highlight
    for m in re.finditer(r'<div class="cap" id="c(\d+)"><span>(.*?)</span></div>', head):
        caps[int(m.group(1))] = m.group(2)
    out, ordinal = [], 0; n = dict(core=0, glow=0, count=0, spot=0, cap=0); spots = {}
    for l in lines:
        m = re.match(r'tl\.fromTo\(gsap\.utils\.toArray\("#w(\d+) \.(mv-[A-Za-z0-9-]+)"\)\[(\d+)\],', l)
        if m and 'scaleY:1.14,scaleX:.92' in l:
            u, cls, kk = int(m.group(1)), m.group(2), int(m.group(3)); v0, t1 = win[u]; sp = t1 - v0 + 0.2
            g = f'gsap.utils.toArray("#w{u} .{cls}")[{kk}]'
            if cls == 'mv-glint-core':
                t0 = v0 + TIN[entry_kind('\n'.join(block_of[u]))]
                ct = motions.legacy_core_type(ordinal); ordinal += 1; n['core'] += 1
                out.extend(motions.core_js(ct, g, t0, v0, sp, ring=f'gsap.utils.toArray("#w{u} .mv-ring")[{kk}]')); continue
            if re.match(r'mv-(glint|lamp|lantern|beacon)', cls):
                per = {'glint': 1.4, 'lamp': 1.2, 'lantern': 1.3, 'beacon': 1.5}[cls.split('-')[1]] * (1 + 0.13 * (kk % 3)); rep = int(math.ceil(sp / per)) - 1
                out.append(f'tl.fromTo({g},{{scale:1,opacity:.85,transformOrigin:"50% 50%"}},{{scale:1.06,opacity:1,duration:{per:.3f},ease:"sine.inOut",yoyo:true,repeat:{rep},immediateRender:false}},{v0:.3f});')
                n['glow'] += 1; continue
        out.append(l)
        m = re.match(r'tl\.fromTo\("#(L\d+_\d+)",\{opacity:0,x:-30\}.*,([\d.]+)\);$', l)
        if m:                            # number badge -> count up
            out.append(labels_lib.count_js(m.group(1), float(m.group(2)))); n['count'] += 1
        m = re.match(r'tl\.to\("#w(\d+)",\{scale:([\d.]+),x:(-?[\d.]+),y:(-?[\d.]+),duration:1\.4,ease:"power2\.inOut"\},([\d.]+)\);$', l)
        if m:                            # focus camera -> spotlight on the same point
            u, S, X, Y, A = int(m.group(1)), float(m.group(2)), float(m.group(3)), float(m.group(4)), float(m.group(5))
            spots[u] = ((W / 2 - X) / S, (H / 2 - Y) / S, S)
            out.append(f'tl.fromTo("#sp{u}",{{opacity:0}},{{opacity:1,duration:1.4,ease:"power2.inOut",immediateRender:false}},{A:.3f});'); n['spot'] += 1
        for m in re.finditer(r'tl\.set\("#c(\d+)",\{opacity:1\},([\d.]+)\);tl\.set\("#c\1",\{opacity:0\},([\d.]+)\);', l):
            k, a, b = int(m.group(1)), float(m.group(2)), float(m.group(3))
            if k in caps:                # subtitle -> spoken word highlight (speaking window ends a moment before the line goes)
                out.append(caption_hl.highlight_js(k, caps[k], a, max(a + 0.3, b - 0.2))); n['cap'] += 1
    # html side: caption words, badge count span, spotlight layers, CSS
    head = re.sub(r'<div class="cap" id="c(\d+)"><span>(.*?)</span></div>',
                  lambda m: f'<div class="cap" id="c{m.group(1)}"><span>{caption_hl.words_html(int(m.group(1)), m.group(2))}</span></div>', head)
    head = re.sub(r'(<div class="badge [^"]*" id="L\d+_\d+" style="[^"]*">)(.*?)(</div>)', lambda m: m.group(1) + labels_lib.count_span(m.group(2)) + m.group(3), head)
    for u, (fx, fy, S) in spots.items():
        k = head.find(f'<div class="w" id="w{u}">'); e = head.find('</svg>', k) + len('</svg>')
        spot = (f'<div class="spot" id="sp{u}" style="position:absolute;left:0;top:0;width:{W}px;height:{H}px;pointer-events:none;opacity:0;'
                f'background:radial-gradient(circle at {fx:.0f}px {fy:.0f}px,rgba(0,0,0,0) {.30 * W / S:.0f}px,rgba(0,0,0,.5) {.62 * W / S:.0f}px)"></div>')
        head = head[:e] + spot + head[e:]
    head = head.replace('</style>', caption_hl.CSS + '</style>', 1)
    new_js = '\n'.join(out).replace('const tl=gsap.timeline', motions.WRAP_JS + motions.CHALK_FIT_JS + f'miyaWrapCores({cx},{cy});const tl=gsap.timeline', 1)
    open(path, 'w', encoding='utf-8').write(head + new_js)
    print(path, f": {n['core']} centre motions, {n['glow']} light groups, {n['count']} counting badges, {n['spot']} spotlights, {n['cap']} highlighted captions")
    return True


if __name__ == '__main__':
    for d in sys.argv[1:]:
        restyle(d.rstrip('/') + '/index.html')
