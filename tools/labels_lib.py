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
        if k + 3 < len(words) and words[k + 1:k + 4] == ['and', 'a', 'half']:
            out.add(f'{v}.5')
        if k + 1 < len(words) and words[k + 1] == 'hundred' and v < 10: out.add(str(v * 100))
        out.add(str(v))
    if re.search(r'\bhalf\b', t): out.add('0.5')
    return out


def check(sc, text, W, H, vert):
    """problems (list of str) for the labels of one unit; text = the unit's narration text."""
    errs = []; labs = sc.get('labels') or []
    if not isinstance(labs, list): return ['labels must be a list']
    if len(labs) > 3: errs.append('more than 3 labels')
    kinds = [l.get('type') for l in labs]
    if kinds.count('num') > 1: errs.append('more than one num badge')
    if kinds.count('say') > 1: errs.append('more than one speech bubble')
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
            outer.append(f'<div class="badge {cls}" id="{lid}" style="{pos};--ink:{ink};--acc:{acc}">{tx}</div>')
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
        inner.append(f'<div class="lab {ty} {cls}" id="{lid}" style="left:{x:.0f}px;top:{y:.0f}px;--ink:{ink}"><span><b id="{lid}s">{tx}</b></span></div>')
        items.append((ty, lid, f'{lid}g' if g else None, l))
    if ov: inner.insert(0, f'<svg class="labov" width="{W}" height="{H}" viewBox="0 0 {W} {H}">{"".join(ov)}</svg>')
    return ''.join(inner), ''.join(outer), items
