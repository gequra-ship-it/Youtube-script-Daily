# -*- coding: utf-8 -*-
# On-screen text over the pictures (guideline 3-6, user decision 2026-10-11: "pictures show only subtitles; add fitting text from the script").
# Text is NOT drawn inside the SVG (art stays text-free); it is an HTML layer the builder places over the picture, so spelling is exact.
#
# Sidecar key  "labels": [ ... ]  (0-3 entries per unit), three types:
#   {"type": "name", "text": "Anomalocaris", "x": 1320, "y": 300, "to": [1180, 470], "word": "Anomalocaris"}
#       name of a thing/animal/place/era that is visible in the picture. text must appear in the unit text (case-insensitive).
#       x,y = centre of the label; "to" (optional) = point on the subject, a thin pointer line + dot is drawn to it.
#   {"type": "num", "text": "539 MILLION YEARS AGO", "word": "539 million"}
#       number/date badge, fixed at the top-left of the screen (does not move with the camera). Every number in it must be
#       said in the unit text (digits, or simple number words like "twenty", "two and a half", "a hundred").
#   {"type": "say", "text": "Too dry!", "x": 700, "y": 260, "to": [820, 420]}
#       short speech bubble for an animal, a generic person or an object (never a real, named person). Max 4 words / 24
#       characters, no digits, no facts: a reaction or feeling that matches the narration ("Hmm?", "Not today!", "So hot...").
#       "to" = the speaker's mouth; the bubble tail points there.
#   "word" (optional, all types) = exact words from the unit text; the label pops in when they are spoken (else ~0.4 s after the cut).
import re, html

LIMITS = dict(name=28, num=26, say=24)
SMALL = {w: i for i, w in enumerate('zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen '
                                     'sixteen seventeen eighteen nineteen'.split())}
TENS = {w: 10 * (i + 2) for i, w in enumerate('twenty thirty forty fifty sixty seventy eighty ninety'.split())}


def _num(s):
    return s.replace(',', '').rstrip('.')


def spoken_numbers(text):
    """numbers said in the text, as digit strings (digits written out + simple number words)."""
    t = text.lower(); out = {_num(x) for x in re.findall(r'\d[\d,]*(?:\.\d+)?', t)}
    words = re.findall(r"[a-z]+", t.replace('-', ' '))
    for k, w in enumerate(words):
        v = SMALL.get(w, TENS.get(w))
        if w in ('hundred', 'thousand') and (k == 0 or words[k - 1] in ('a', 'one', 'several', 'few')):
            v = 100 if w == 'hundred' else 1000
        if v is None: continue
        if w in TENS and k + 1 < len(words) and words[k + 1] in SMALL and 0 < SMALL[words[k + 1]] < 10:
            out.add(str(v + SMALL[words[k + 1]]))
        if k + 2 < len(words) and words[k + 1] == 'point' and words[k + 2] in SMALL and SMALL[words[k + 2]] < 10:
            ds = ''; j = k + 2
            while j < len(words) and words[j] in SMALL and SMALL[words[j]] < 10:
                ds += str(SMALL[words[j]]); out.add(f'{v}.{ds}'); j += 1      # "one point six five" -> 1.6 and 1.65
        if k + 3 < len(words) and words[k + 1:k + 4] == ['and', 'a', 'half']:
            out.add(f'{v}.5')
        if k + 1 < len(words) and words[k + 1] == 'hundred' and v < 10: out.add(str(v * 100))
        out.add(str(v))
    # scale words: "eleven thousand" -> 11000, "two hundred thousand" -> 200000, "a million" / "one million" -> 1000000
    for k, w in enumerate(words):
        if w not in ('thousand', 'million'): continue
        mult = 1000 if w == 'thousand' else 1000000
        j = k - 1; base = None
        if j >= 0 and words[j] == 'hundred':
            h = SMALL.get(words[j - 1]) if j >= 1 else None
            base = (h or 1) * 100
        elif j >= 0:
            v = SMALL.get(words[j], TENS.get(words[j]))
            if v is not None and j >= 1 and words[j - 1] in TENS and words[j] in SMALL: v += TENS[words[j - 1]]
            if v is None and words[j] in ('a', 'one'): v = 1
            base = v
        if base is not None: out.add(str(base * mult))
    # "a hundred and seventy" / "two hundred and five" -> 170 / 205
    for k, w in enumerate(words):
        if w != 'hundred' or k + 2 >= len(words) or words[k + 1] != 'and': continue
        h = SMALL.get(words[k - 1]) if k >= 1 else None
        h = h if h else 1
        rest = TENS.get(words[k + 2], SMALL.get(words[k + 2]))
        if rest is None: continue
        if words[k + 2] in TENS and k + 3 < len(words) and words[k + 3] in SMALL and 0 < SMALL[words[k + 3]] < 10: rest += SMALL[words[k + 3]]
        out.add(str(h * 100 + rest))
    out |= {x + '000' for x in re.findall(r'(\d+)(?:,\d{3})?\s+thousand', t)}
    if re.search(r'\bhalf\b', t): out.add('0.5')
    return out


def check(sc, text, W, H, vert):
    """problems (list of str) for the labels of one unit; text = the unit's narration text."""
    errs = []; labs = sc.get('labels') or []
    if not isinstance(labs, list): return ['labels must be a list']
    if len(labs) > 3: errs.append('more than 3 labels')
    kinds = [l.get('type') for l in labs]
    if kinds.count('num') > 1: errs.append('more than one num badge')
    if kinds.count('say') > 2: errs.append('more than two speech bubbles')   # 2026-10-22: up to two (two things talking)
    lo = text.lower()
    x0, x1, y0, y1 = (100, 940, 300, 1400) if vert else (120, 1800, 80, 860)
    for l in labs:
        ty = l.get('type'); tx = str(l.get('text', '')).strip()
        if ty not in LIMITS: errs.append(f'unknown type {ty!r}'); continue
        if not tx: errs.append(f'{ty}: empty text'); continue
        if len(tx) > LIMITS[ty]: errs.append(f'{ty}: "{tx}" longer than {LIMITS[ty]} characters')
        if re.search(r'[가-힣]', tx): errs.append(f'{ty}: Korean letters in "{tx}"')
        if l.get('word') and l['word'] not in text: errs.append(f'{ty}: word "{l["word"]}" not in unit text')
        if ty == 'name' and tx.lower().rstrip('s') not in lo: errs.append(f'name: "{tx}" is not in the unit text')
        if ty == 'num':
            said = spoken_numbers(text)
            for n in re.findall(r'\d[\d,]*(?:\.\d+)?', tx):
                if _num(n) not in said: errs.append(f'num: {n} in "{tx}" is not said in the unit text (said: {sorted(said)})')
            if not re.search(r'\d', tx) and not any(w in lo for w in tx.lower().split()): errs.append(f'num: "{tx}" has no number')
        if ty == 'say':
            if len(tx.split()) > 4: errs.append(f'say: "{tx}" has more than 4 words')
            if re.search(r'\d', tx): errs.append(f'say: digits in "{tx}"')
        if ty in ('name', 'say'):
            try:
                x, y = float(l['x']), float(l['y'])
                if not (x0 <= x <= x1 and y0 <= y <= y1): errs.append(f'{ty}: x,y ({x:.0f},{y:.0f}) outside the safe area x {x0}-{x1}, y {y0}-{y1}')
                if not vert and x > 1660 and y < 190: errs.append(f'{ty}: overlaps the logo corner')
                f = sc.get('focus')
                if f:   # where the label ends up after the focus camera zoom (same maths as build3)
                    fx, fy, s = float(f[0]), float(f[1]), float(f[2])
                    cxm = min(max(fx, W / 2 / s), W - W / 2 / s); cym = min(max(fy, H / 2 / s), H - H / 2 / s)
                    sx, sy = W / 2 + (x - cxm) * s, H / 2 + (y - cym) * s
                    if not (x0 <= sx <= x1 and y0 <= sy <= y1):
                        errs.append(f'{ty}: after the focus zoom the label lands at ({sx:.0f},{sy:.0f}), outside the safe area; move it closer to the focus point')
                if 'to' in l and l['to'] is not None: float(l['to'][0]); float(l['to'][1])
            except (KeyError, TypeError, ValueError, IndexError):
                errs.append(f'{ty}: needs numeric x, y (and "to": [x, y] if given)')
    return errs


CSS = '''.lab{position:absolute;width:0;height:0;z-index:5}
.lab>span{position:absolute;left:-500px;top:-60px;width:1000px;height:120px;display:flex;align-items:center;justify-content:center}
.lab b{display:block;white-space:nowrap;opacity:0;font-weight:inherit}
.lab.name b{font:700 34px/40px Fredoka,sans-serif;padding:8px 18px;border-radius:999px}
.lab.say b{font:400 42px/46px Patrick,sans-serif;padding:12px 24px;border-radius:26px;background:#fffdf7;color:#1f1d1a;border:3px solid #1f1d1a}
.lab.paper.name b{background:rgba(255,251,242,.94);color:var(--ink);border:2px solid var(--ink)}
.lab.dark.name b{background:rgba(8,10,18,.70);color:#fff;border:2px solid rgba(255,255,255,.45)}
.badge{position:absolute;opacity:0;z-index:6;font:700 44px/52px Fredoka,sans-serif;letter-spacing:1px;padding:10px 26px 10px 22px;border-radius:12px;white-space:nowrap}
.badge.paper{background:rgba(255,251,242,.95);color:var(--ink);border-left:12px solid var(--acc)}
.badge.dark{background:rgba(8,10,18,.72);color:#fff;border-left:12px solid var(--acc)}
.labov{position:absolute;left:0;top:0;pointer-events:none;z-index:4}
.labov g{opacity:0}
.lab b i{display:inline-block;font-style:normal;white-space:pre}
.lab.name b{background-repeat:no-repeat;background-size:0% 100%}
.lab.name.hl b{background-image:linear-gradient(#ffe66d,#ffe66d)}
.lab.dark.name.hl b{background-image:linear-gradient(rgba(255,230,109,.55),rgba(255,230,109,.55))}
.lab b u{position:absolute;left:14px;right:14px;bottom:4px;height:3px;background:currentColor;transform:scaleX(0);transform-origin:0 50%}
.badge{transform-origin:0% 50%}
'''


def html_for(n, sc, bgmode, pal, W, H, vert):
    """(inside_camera_html, outside_camera_html, items) for unit n. items: list of (kind, element ids, label dict)."""
    labs = sc.get('labels') or []
    if not labs: return '', '', []
    dark = bgmode != 'paper'; cls = 'dark' if dark else 'paper'
    ink = pal['paper'][1]; acc = pal['accents'][0]
    line = 'rgba(255,255,255,.85)' if dark else ink
    inner, outer, ov, items = [], [], [], []
    for k, l in enumerate(labs):
        ty = l['type']; tx = html.escape(str(l['text']).strip(), quote=False); lid = f'L{n}_{k}'
        if ty == 'num':
            pos = 'left:100px;top:330px' if vert else 'left:80px;top:64px'
            outer.append(f'<div class="badge {cls}" id="{lid}" style="{pos};--ink:{ink};--acc:{acc}">{count_span(tx)}</div>')
            items.append(('num', lid, None, l)); continue
        x, y = float(l['x']), float(l['y']); to = l.get('to')
        g = ''
        if to is not None:
            tx2, ty2 = float(to[0]), float(to[1])
            if ty == 'name':
                g = (f'<g id="{lid}g"><line x1="{x:.0f}" y1="{y:.0f}" x2="{tx2:.0f}" y2="{ty2:.0f}" stroke="{line}" stroke-width="3" stroke-linecap="round"/>'
                     f'<circle cx="{tx2:.0f}" cy="{ty2:.0f}" r="7" fill="{line}"/></g>')
            else:   # speech-bubble tail: a narrow triangle from the bubble centre towards the mouth
                dx, dy = tx2 - x, ty2 - y; L = max((dx * dx + dy * dy) ** .5, 1); px, py = -dy / L * 22, dx / L * 22
                ex, ey = tx2 - dx / L * 10, ty2 - dy / L * 10
                g = (f'<g id="{lid}g"><path d="M{x + px:.0f},{y + py:.0f} L{ex:.0f},{ey:.0f} L{x - px:.0f},{y - py:.0f} Z" fill="#fffdf7" stroke="#1f1d1a" stroke-width="3" stroke-linejoin="round"/></g>')
        if g: ov.append(g)
        body = letters(tx) + '<u></u>' if ty == 'name' else tx   # round 4: one <i> per letter so letter effects can address them
        inner.append(f'<div class="lab {ty} {cls}{" hl" if ty == "name" else ""}" id="{lid}" style="left:{x:.0f}px;top:{y:.0f}px;--ink:{ink}"><span><b id="{lid}s" style="position:relative">{body}</b></span></div>')
        items.append((ty, lid, f'{lid}g' if g else None, l))
    if ov: inner.insert(0, f'<svg class="labov" width="{W}" height="{H}" viewBox="0 0 {W} {H}">{"".join(ov)}</svg>')
    return ''.join(inner), ''.join(outer), items


# Count-up for number badges (guideline 3-6, 2026-10-13): the first number in the badge counts up from 0.
# Years (four digits 1000-2100 without a comma) do not count, "0 to 1859" would read oddly.
def count_span(tx):
    m = re.search(r'\d[\d,]*(?:\.\d+)?', tx)
    if not m: return tx
    raw = m.group(0); v = float(raw.replace(',', ''))
    if re.fullmatch(r'\d{4}', raw) and 1000 <= v <= 2100: return tx
    dec = len(raw.split('.')[1]) if '.' in raw else 0
    return (tx[:m.start()] + f'<span class="cnt" data-v="{v}" data-dec="{dec}" data-grp="{1 if "," in raw else 0}">{raw}</span>' + tx[m.end():])


def count_js(lid, tt):
    """Seek-safe count-up: tweens the span's innerText, formatted by a modifier (no callbacks)."""
    return (f'(function(){{var c=document.querySelector("#{lid} .cnt");if(!c)return;var v=+c.dataset.v,d=+c.dataset.dec,gp=c.dataset.grp==="1";'
            f'tl.fromTo(c,{{innerText:0}},{{innerText:v,duration:.9,ease:"power2.out",immediateRender:false,'
            f'modifiers:{{innerText:function(x){{return (+x).toLocaleString("en-US",{{minimumFractionDigits:d,maximumFractionDigits:d,useGrouping:gp}});}}}}}},{tt:.3f});}})();')


# ---- text effects (round 4, 2026-10-26, miya: "텍스트 효과도", on-screen text only, never subtitles). Deterministic: the style of a
# name label is picked from NAME_FX by (unit number * 7 + label index), a speech bubble by its punctuation, a number badge by its order,
# and a few words of the unit text add a reaction (shake on danger words, highlight on key words). No randomness, no model choice.
import re as _re
NAME_FX = ['pop', 'typewriter', 'slideleft', 'rise', 'flip', 'zoom', 'stamp', 'wobble', 'blur', 'wave', 'drop', 'scatter', 'spin', 'swing', 'elastic',
           'sink', 'slideright', 'bounceletters', 'zoomletters', 'flipletters', 'glow', 'underline', 'highlight', 'squeeze', 'fan']
SAY_FX = {'!': 'slam', '?': 'tilt', '...': 'slowfade', '~': 'jiggle'}   # else 'pop'; every bubble then floats (bob) while it stays
NUM_FX = ['slide', 'drop', 'flip', 'zoom', 'stamp', 'flashbg']
DANGERW = _re.compile(r'\b(danger\w*|deadly|lethal|kill\w*|attack\w*|poison\w*|terror\w*|panic\w*|crash\w*|explo\w*|collaps\w*)\b', _re.I)
KEYW = _re.compile(r'\b(the (key|secret|answer|reason)|most important|in fact|actually|turns out|the truth)\b', _re.I)
TEXT_FX_KINDS = NAME_FX + list(SAY_FX.values()) + ['pop', 'bob', 'shake'] + NUM_FX


def letters(tx):
    """escaped text as one <i> per character (spaces kept inside their own <i> so widths stay)"""
    return ''.join(f'<i>{c}</i>' for c in _re.findall(r'&[a-z]+;|.', tx))


def name_fx(nn, k):
    return NAME_FX[(nn * 7 + k) % len(NAME_FX)]


def say_fx(tx):
    t = tx.strip()
    if t.endswith('...') or t.endswith('\u2026'): return 'slowfade'
    for p, f in SAY_FX.items():
        if p in t: return f
    return 'pop'


def label_js(ty, lid, tt, nn, k, text, utext, te=None):
    """entrance (+ reaction) tweens for one name / say label at absolute time tt (seek-safe, finite). te = leave time for bubbles (bob until then)."""
    S = f'"#{lid}s"'; L = f'"#{lid}s i"'; js = []; A = f'{tt:.3f}'
    if ty == 'say':
        f = say_fx(text)
        if f == 'slam': js.append(f'tl.fromTo({S},{{opacity:0,scale:1.8}},{{opacity:1,scale:1,duration:.22,ease:"power3.in",immediateRender:false}},{A});tl.fromTo({S},{{x:0}},{{x:5,duration:.04,yoyo:true,repeat:5,immediateRender:false}},{tt + .22:.3f});')
        elif f == 'tilt': js.append(f'tl.fromTo({S},{{opacity:0,scale:.6,rotation:-12,transformOrigin:"50% 100%"}},{{opacity:1,scale:1,rotation:0,duration:.4,ease:"back.out(2.5)",immediateRender:false}},{A});tl.fromTo({S},{{rotation:0}},{{rotation:5,duration:.5,yoyo:true,repeat:3,ease:"sine.inOut",immediateRender:false}},{tt + .45:.3f});')
        elif f == 'slowfade': js.append(f'tl.fromTo({S},{{opacity:0,y:10}},{{opacity:1,y:0,duration:1.1,ease:"sine.out",immediateRender:false}},{A});')
        elif f == 'jiggle': js.append(f'tl.fromTo({S},{{opacity:0,scale:.6}},{{opacity:1,scale:1,duration:.25,ease:"back.out(2)",immediateRender:false}},{A});tl.fromTo({S},{{skewX:-6}},{{skewX:6,duration:.18,yoyo:true,repeat:5,ease:"sine.inOut",immediateRender:false}},{tt + .25:.3f});')
        else: js.append(f'tl.fromTo({S},{{opacity:0,scale:.6}},{{opacity:1,scale:1,duration:.25,ease:"back.out(2)",immediateRender:false}},{A});')
        if te and te - tt > 2.2:   # the bubble floats gently while it stays (never jumps)
            js.append(f'tl.fromTo({S},{{y:0}},{{y:-6,duration:1.4,yoyo:true,repeat:{max(int((te - tt - 1) / 1.4), 1)},ease:"sine.inOut",immediateRender:false}},{tt + 1:.3f});')
        if DANGERW.search(utext): js.append(f'tl.fromTo({S},{{x:0}},{{x:-4,duration:.05,yoyo:true,repeat:7,immediateRender:false}},{tt + 1.6:.3f});')
        return js
    f = name_fx(nn, k); n = len(_re.findall(r'&[a-z]+;|.', text)); st = max(.02, min(.07, .5 / max(n, 1)))
    V = lambda a, b, d, e='power2.out': f'tl.fromTo({S},{{{a}}},{{{b},duration:{d},ease:"{e}",immediateRender:false}},{A});'
    LV = lambda a, b, d, e='power2.out', s=st: f'tl.set({S},{{opacity:1}},{A});tl.fromTo({L},{{{a}}},{{{b},duration:{d},stagger:{s},ease:"{e}",immediateRender:false}},{A});'
    if f == 'pop': js.append(V('opacity:0,scale:.6', 'opacity:1,scale:1', .25, 'back.out(2)'))
    elif f == 'typewriter': js.append(LV('opacity:0', 'opacity:1', .02, 'none'))
    elif f == 'slideleft': js.append(V('opacity:0,x:-40', 'opacity:1,x:0', .35))
    elif f == 'slideright': js.append(V('opacity:0,x:40', 'opacity:1,x:0', .35))
    elif f == 'rise': js.append(V('opacity:0,y:30', 'opacity:1,y:0', .4))
    elif f == 'sink': js.append(V('opacity:0,y:-30', 'opacity:1,y:0', .4, 'bounce.out'))
    elif f == 'flip': js.append(V('opacity:0,rotationX:-90,transformPerspective:500,transformOrigin:"50% 50%"', 'opacity:1,rotationX:0', .45))
    elif f == 'zoom': js.append(V('opacity:0,scale:2.2', 'opacity:1,scale:1', .35, 'power3.out'))
    elif f == 'stamp': js.append(V('opacity:0,scale:1.6,rotation:-6,transformOrigin:"50% 50%"', 'opacity:1,scale:1,rotation:-2', .2, 'power3.in'))
    elif f == 'wobble': js.append(V('opacity:0,rotation:-10,scale:.8,transformOrigin:"50% 100%"', 'opacity:1,rotation:0,scale:1', .55, 'elastic.out(1,.4)'))
    elif f == 'blur': js.append(V('opacity:0,filter:"blur(12px)"', 'opacity:1,filter:"blur(0px)"', .5))
    elif f == 'wave': js.append(V('opacity:0', 'opacity:1', .2, 'none') + f'tl.fromTo({L},{{y:0}},{{y:-8,duration:.22,yoyo:true,repeat:1,stagger:{st},ease:"sine.inOut",immediateRender:false}},{tt + .15:.3f});')
    elif f == 'drop': js.append(LV('opacity:0,y:-28', 'opacity:1,y:0', .3, 'bounce.out'))
    elif f == 'scatter': js.append(f'tl.set({S},{{opacity:1}},{A});' + ''.join(f'tl.fromTo("#{lid}s i:nth-child({i + 1})",{{opacity:0,x:{((i * 37) % 41) - 20},y:{((i * 53) % 31) - 15},rotation:{((i * 29) % 40) - 20}}},{{opacity:1,x:0,y:0,rotation:0,duration:.4,ease:"power2.out",immediateRender:false}},{tt + i * st:.3f});' for i in range(n)))
    elif f == 'spin': js.append(LV('opacity:0,rotation:90,transformOrigin:"50% 50%"', 'opacity:1,rotation:0', .3, 'back.out(1.5)'))
    elif f == 'swing': js.append(V('opacity:0,rotation:-25,transformOrigin:"0% 0%"', 'opacity:1,rotation:0', .6, 'elastic.out(1,.5)'))
    elif f == 'elastic': js.append(V('opacity:0,scaleX:.3,transformOrigin:"0% 50%"', 'opacity:1,scaleX:1', .7, 'elastic.out(1,.45)'))
    elif f == 'bounceletters': js.append(LV('opacity:0,scale:0,transformOrigin:"50% 100%"', 'opacity:1,scale:1', .35, 'back.out(3)'))
    elif f == 'zoomletters': js.append(LV('opacity:0,scale:2.5,transformOrigin:"50% 50%"', 'opacity:1,scale:1', .25))
    elif f == 'flipletters': js.append(LV('opacity:0,rotationY:90,transformPerspective:400,transformOrigin:"50% 50%"', 'opacity:1,rotationY:0', .3))
    elif f == 'glow': js.append(V('opacity:0,scale:.9', 'opacity:1,scale:1', .3) + f'tl.fromTo({S},{{textShadow:"0 0 0px rgba(255,230,109,0)"}},{{textShadow:"0 0 18px rgba(255,230,109,.9)",duration:.6,yoyo:true,repeat:3,ease:"sine.inOut",immediateRender:false}},{tt + .3:.3f});')
    elif f == 'underline': js.append(V('opacity:0,y:12', 'opacity:1,y:0', .3) + f'tl.fromTo("#{lid}s u",{{scaleX:0}},{{scaleX:1,duration:.4,ease:"power2.out",immediateRender:false}},{tt + .3:.3f});')
    elif f == 'highlight': js.append(V('opacity:0', 'opacity:1', .25, 'none') + f'tl.fromTo({S},{{backgroundSize:"0% 100%"}},{{backgroundSize:"100% 100%",duration:.5,ease:"power2.inOut",immediateRender:false}},{tt + .2:.3f});')
    elif f == 'squeeze': js.append(V('opacity:0,scaleY:.2,scaleX:1.4,transformOrigin:"50% 50%"', 'opacity:1,scaleY:1,scaleX:1', .4, 'back.out(1.7)'))
    elif f == 'fan': js.append(LV('opacity:0,rotation:-40,y:10,transformOrigin:"0% 100%"', 'opacity:1,rotation:0,y:0', .3, 'back.out(1.5)'))
    if KEYW.search(utext) and f not in ('highlight', 'glow'):   # key sentence: the name gets a quick emphasis pulse 1 s after it lands
        js.append(f'tl.fromTo({S},{{scale:1}},{{scale:1.1,duration:.16,yoyo:true,repeat:1,ease:"power2.out",immediateRender:false}},{tt + 1.1:.3f});')
    return js


def badge_js(lid, tt, idx):
    """entrance for the number badge: style by its order among all badges (NUM_FX rotation)"""
    f = NUM_FX[idx % len(NUM_FX)]; Q = f'"#{lid}"'; A = f'{tt:.3f}'
    if f == 'slide': return [f'tl.fromTo({Q},{{opacity:0,x:-30}},{{opacity:1,x:0,duration:.3,ease:"power2.out",immediateRender:false}},{A});']
    if f == 'drop': return [f'tl.fromTo({Q},{{opacity:0,y:-60}},{{opacity:1,y:0,duration:.5,ease:"bounce.out",immediateRender:false}},{A});']
    if f == 'flip': return [f'tl.fromTo({Q},{{opacity:0,rotationX:90,transformPerspective:600,transformOrigin:"50% 0%"}},{{opacity:1,rotationX:0,duration:.45,ease:"power2.out",immediateRender:false}},{A});']
    if f == 'zoom': return [f'tl.fromTo({Q},{{opacity:0,scale:1.8}},{{opacity:1,scale:1,duration:.3,ease:"power3.out",immediateRender:false}},{A});']
    if f == 'stamp': return [f'tl.fromTo({Q},{{opacity:0,scale:1.5,rotation:-4}},{{opacity:1,scale:1,rotation:0,duration:.2,ease:"power3.in",immediateRender:false}},{A});']
    return [f'tl.fromTo({Q},{{opacity:0,x:-30}},{{opacity:1,x:0,duration:.3,ease:"power2.out",immediateRender:false}},{A});',
            f'tl.fromTo({Q},{{filter:"brightness(1)"}},{{filter:"brightness(1.6)",duration:.12,yoyo:true,repeat:1,immediateRender:false}},{tt + .9:.3f});']   # flashbg: a bright blink when the count lands
