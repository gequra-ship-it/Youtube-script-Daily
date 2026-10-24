# -*- coding: utf-8 -*-
# Notebook frog (Miya's Note mascot) as an explainer inside the video (owner decision 2026-10-24, guideline 7-2 / 20-8).
# The frog hops in next to the thing it explains, points at it, talks (mouth follows the real word times) and blinks.
# markup()  -> SVG group string to put INTO a picture svg (ids fg<tag>_*), or into an overlay svg for chalkboard scenes
# js()      -> GSAP lines (absolute timeline seconds) for that frog
# Sidecar key in art3/<uid>.json: "frog": {"x": 220, "y": 1040, "s": 2.4, "flip": 1, "point": [tx, ty], "delay": 0.35}
#   x, y = feet position (picture coords), s = scale (82 units tall at s=1), flip = -1 mirrors it (arm then points left),
#   point = what the arm points at, delay = seconds after the unit starts. `"frog": true` = defaults.
#   2026-10-24 (miya feedback on the first shorts): the arm no longer waves or nods; it rests down and turns ONLY when the pointed object changes.
#   More keys: "points": [{"word": "Voyager", "to": [x, y]}, ...]  (arm retargets when that word is spoken; "point" = the first one),
#     "moods": [{"word": "...", "mood": "happy|surprised|curious|worried|proud|excited"}] (first entry without "word" = at the start),
#     "moves": [{"word": "...", "x": .., "y": .., "flip": 1|-1, "s": ..}] (the frog hops to a new place while explaining; s may change the size),
#     "outfit": ["helmet"] | ["goggles"] (bubble space helmet / diving mask + snorkel), "enter": "hop" (default, jumps up from below) | "pop" (appears in place,
#     use it when the frog sits on/in something so it does not rise through the picture), "stay": true (no exit fade-out needed, default).
#   The frog is part of the picture, so it can ride a spaceship, dive, stand next to an animal: just put x, y (feet) on that object and pick the size.
import math, re

INK = '#1d2b1c'; GREEN = '#6aa55a'


def defaults(vert=False):
    return dict(x=230, y=1400, s=3.2, flip=1, point=None, delay=0.35) if vert else dict(x=220, y=880, s=2.4, flip=1, point=None, delay=0.35)


def spec(sidecar, vert=False):
    f = (sidecar or {}).get('frog')
    if not f: return None
    d = defaults(vert)
    if isinstance(f, dict): d.update({k: v for k, v in f.items() if v is not None or k == 'point'})
    return d


def shoulder(d):
    """arm pivot in picture coordinates"""
    return d['x'] + d['flip'] * d['s'] * 32, d['y'] - d['s'] * 22


def outfit_markup(t, names):
    o = ''
    if 'goggles' in names:   # diving mask over the eyes + snorkel
        o += (f'<path d="M40 -66 q12 -12 8 -46" fill="none" stroke="#e0b84a" stroke-width="6"/><path d="M-34 -66 q-8 6 -4 14" fill="none" stroke-width="3"/>'
              f'<rect x="-27" y="-84" width="68" height="34" rx="14" fill="#9fd8ff" fill-opacity=".35" stroke-width="4.2"/><path d="M-27 -66 q-14 0 -16 8 M41 -66 q10 0 12 8" fill="none" stroke="#e0b84a" stroke-width="5"/>')
    if 'helmet' in names:    # bubble helmet like the thumbnails
        o += (f'<circle cx="6" cy="-58" r="46" fill="#cfe9ff" fill-opacity=".14" stroke="#e6f1fb" stroke-width="3.4"/><path d="M-26 -84 q10 -16 28 -20" fill="none" stroke="#fff" stroke-width="4" stroke-opacity=".7"/>'
              f'<ellipse cx="6" cy="-14" rx="42" ry="9" fill="#e6f1fb" fill-opacity=".55" stroke="#e6f1fb" stroke-width="3"/>')
    return o


MOODS = {   # brows (left d, right d, opacity), pupil offset (dx, dy, r), mouth path + fill, lid height (eyes squint)
    'happy':     dict(bl='M-24 -84 q12 -6 24 0', br='M10 -84 q12 -6 24 0', bo=0, pup=(0, 0, 5), sm='M-8 -44 q14 12 28 0', fill='none', lid=0),
    'surprised': dict(bl='M-24 -90 q12 -8 24 0', br='M10 -90 q12 -8 24 0', bo=1, pup=(0, 0, 3.4), sm='M0 -47 q6 -6 12 0 q2 11 -6 11 q-8 0 -6 -11z', fill='#7a2f2f', lid=0),
    'curious':   dict(bl='M-24 -82 q12 0 24 2', br='M10 -92 q12 -8 24 -2', bo=1, pup=(3, -4, 5), sm='M-8 -42 q14 7 28 -5', fill='none', lid=0),
    'worried':   dict(bl='M-24 -80 q12 -2 24 -8', br='M10 -88 q12 6 24 8', bo=1, pup=(0, 2, 5), sm='M-6 -38 q12 -9 24 0', fill='none', lid=0),
    'proud':     dict(bl='M-24 -84 q12 -6 24 0', br='M10 -84 q12 -6 24 0', bo=0, pup=(0, 1, 5), sm='M-10 -47 q16 20 32 0', fill='none', lid=9),
    'excited':   dict(bl='M-24 -90 q12 -8 24 0', br='M10 -90 q12 -8 24 0', bo=1, pup=(0, -1, 5.6), sm='M-10 -47 q16 24 32 0z', fill='#7a2f2f', lid=0),
}


def markup(tag, d):
    t = f'fg{tag}'
    x, y, s, fl = d['x'], d['y'], d['s'], d['flip']
    return (f'<g id="{t}" transform="translate({x:.1f} {y:.1f}) scale({fl * s:.3f} {s:.3f})" stroke="{INK}" stroke-linejoin="round" stroke-linecap="round">'
            f'<defs><clipPath id="{t}_cl"><circle cx="-10" cy="-66" r="13"/></clipPath><clipPath id="{t}_cr"><circle cx="22" cy="-66" r="13"/></clipPath></defs>'
            f'<ellipse cx="0" cy="8" rx="52" ry="8" fill="#000" opacity=".18" stroke="none"/>'
            f'<g id="{t}_in">'
            f'<ellipse cx="-22" cy="4" rx="16" ry="9" fill="#4d8a4a" stroke-width="3.2"/><ellipse cx="22" cy="4" rx="16" ry="9" fill="#4d8a4a" stroke-width="3.2"/>'
            f'<path d="M-34 0 q-6 -64 34 -70 q40 -2 42 62 q0 10 -6 12 q-36 6 -70 -4z" fill="{GREEN}" stroke-width="4"/>'
            f'<ellipse cx="2" cy="-12" rx="22" ry="20" fill="#9cc98a" stroke="none" opacity=".7"/>'
            f'<circle cx="-10" cy="-66" r="13" fill="#e3e5d6" stroke-width="3.2"/><circle id="{t}_pl" cx="-8" cy="-66" r="5" fill="{INK}" stroke="none"/>'
            f'<circle cx="22" cy="-66" r="13" fill="#e3e5d6" stroke-width="3.2"/><circle id="{t}_pr" cx="24" cy="-66" r="5" fill="{INK}" stroke="none"/>'
            f'<g clip-path="url(#{t}_cl)"><rect id="{t}_ll" x="-24" y="-80" width="28" height="0" fill="{GREEN}" stroke="none"/></g>'
            f'<g clip-path="url(#{t}_cr)"><rect id="{t}_lr" x="8" y="-80" width="28" height="0" fill="{GREEN}" stroke="none"/></g>'
            f'<circle cx="-10" cy="-66" r="13" fill="none" stroke-width="3.2"/><circle cx="22" cy="-66" r="13" fill="none" stroke-width="3.2"/>'
            f'<path id="{t}_al" d="M-20 -64 q10 7 20 0" fill="none" stroke-width="3" opacity="0"/><path id="{t}_ar" d="M12 -64 q10 7 20 0" fill="none" stroke-width="3" opacity="0"/>'
            f'<path id="{t}_bl" d="M-24 -84 q12 -6 24 0" fill="none" stroke-width="3.4" opacity="0"/><path id="{t}_br" d="M10 -84 q12 -6 24 0" fill="none" stroke-width="3.4" opacity="0"/>'
            f'<path id="{t}_sm" d="M-8 -44 q14 12 28 0" fill="none" stroke-width="3.4"/>'
            f'<ellipse id="{t}_mo" cx="6" cy="-44" rx="13" ry="0" fill="#7a2f2f" stroke-width="2.8"/>'
            f'<ellipse id="{t}_tg" cx="6" cy="-44" rx="8" ry="0" fill="#e8847a" stroke="none"/>'
            f'<path d="M-34 -22 q-14 6 -16 22" fill="none" stroke-width="7.5"/><path d="M-34 -22 q-14 6 -16 22" fill="none" stroke="{GREEN}" stroke-width="3.4"/>'
            f'{outfit_markup(t, d.get("outfit") or [])}'
            f'<g transform="translate(32 -22)"><g id="{t}_arm">'
            f'<path d="M0 0 L58 0" stroke-width="11"/><circle cx="60" cy="0" r="9" fill="{INK}" stroke="none"/>'
            f'<path d="M0 0 L58 0" stroke="{GREEN}" stroke-width="6"/><circle cx="60" cy="0" r="6" fill="{GREEN}" stroke="none"/>'
            f'</g></g></g></g>')


def inject(svg_text, mk, ride=None):
    """ride = id of a picture group (a spaceship, probe, boat ...): the frog goes INSIDE that group, so it moves, turns and swings with it"""
    if ride:
        m = re.search(r'<g\b[^>]*(?:\bid="%s"|\bclass="[^"]*\b%s\b[^"]*")[^>]*>' % (re.escape(ride), re.escape(ride)), svg_text)
        if m:
            depth = 1; pos = m.end()
            for t in re.finditer(r'<g[\s>]|</g>', svg_text[m.end():]):
                depth += 1 if t.group(0).startswith('<g') else -1
                if depth == 0:
                    pos = m.end() + t.start(); break
            else: pos = None
            if pos is not None: return svg_text[:pos] + mk + svg_text[pos:]
    i = svg_text.rfind('</svg>')
    return svg_text[:i] + mk + svg_text[i:] if i >= 0 else svg_text + mk


TRACK_FN = ('window.__fgAim=window.__fgAim||function(t,id){var a=document.getElementById(t+"_arm"),o=document.querySelector(id);if(!a||!o)return null;'
            'var m=a.parentNode.getScreenCTM();if(!m)return null;var r=o.getBoundingClientRect();'
            'var v=new DOMPoint(r.left+r.width/2,r.top+r.height/2).matrixTransform(m.inverse());return Math.atan2(v.y,v.x)*180/Math.PI;};')


def _norm(w):
    return re.sub(r"[^a-z0-9']", '', w.lower())


def find_word(phrase, wt, a0, t1):
    """time (s) when `phrase` (words) is spoken: wt = [(text, start, end)] of the unit; None when not found"""
    ws = [_norm(x) for x in str(phrase).split() if _norm(x)]
    if not ws: return None
    toks = [_norm(x[0]) for x in wt]
    for k in range(len(toks) - len(ws) + 1):
        if toks[k:k + len(ws)] == ws: return min(max(wt[k][1], a0), t1 - .2)
    return None


def angle_to(d, target, st=None):
    """local rotation (deg) of the arm so that it points at target (picture coords). st = current placement after hops:
    dict(ox=x origin in picture coords of the (flipped) frog space, y=feet y, sx=signed horizontal scale, s=vertical scale)"""
    st = st or dict(ox=d['x'], y=d['y'], sx=d['flip'] * d['s'], s=d['s'])
    u = (target[0] - st['ox']) / st['sx']; v = (target[1] - st['y']) / st['s']
    return math.degrees(math.atan2(v + 22, u - 32))


REST = 75   # arm hangs down along the body (deg, local); it only moves when the pointed object changes


def js(tag, d, t0, t1, words, targets=None, wt=None):
    """GSAP lines. words = [(start, end)] absolute seconds of the unit's words (mouth), targets = [(time, (x, y))] arm pointing
    (default: sidecar "points"/"point"; none = arm rests), wt = [(text, start, end)] to resolve the "word" keys of points/moods/moves."""
    t = f'fg{tag}'; out = []; a0 = t0 + d['delay']; wt = wt or []
    org = 'svgOrigin:"0 0"'   # the arm's own coordinate space starts at the shoulder (parent group translate(32 -22))
    enter = d.get('enter', 'hop')
    out.append(f'tl.set("#{t}_in",{{opacity:0,y:{300 if enter == "hop" else 40}}},0);tl.set("#{t}",{{opacity:0}},0);tl.set("#{t}",{{opacity:1}},{a0 - .01:.3f});tl.set("#{t}",{{opacity:0}},{t1:.3f});')
    out.append(f'tl.fromTo("#{t}_in",{{y:{300 if enter == "hop" else 40},opacity:0}},{{y:0,opacity:1,duration:{.45 if enter == "hop" else .3},ease:"back.out(1.6)",immediateRender:false}},{a0:.3f});')
    # ---- moves (hops to a new place while explaining) ----
    st = dict(ox=d['x'], y=d['y'], sx=d['flip'] * d['s'], s=d['s']); base = dict(st); timeline = []   # (time, kind, payload)
    for m in d.get('moves') or []:
        tm = find_word(m.get('word'), wt, a0 + .4, t1) if m.get('word') else None
        if tm is None: tm = a0 + .8
        timeline.append((tm, 'move', m))
    # ---- points: arm retargets only when the pointed object changes ----
    pts = list(d.get('points') or [])
    if not pts and targets is None and d.get('point'): pts = [dict(to=d['point'], obj=d.get('point_obj'))]
    if targets is not None: pts = [dict(to=p, _tm=tt) for tt, p in targets]
    for k, p in enumerate(pts):
        tm = p.get('_tm')
        if tm is None: tm = find_word(p.get('word'), wt, a0 + .3, t1) if p.get('word') else None
        if tm is None: tm = a0 + .5 if k == 0 else a0 + .5 + k * 1.5
        timeline.append((tm, 'point', dict(to=p['to'], obj=p.get('obj')) if p.get('obj') else p['to']))
    for mo in d.get('moods') or []:
        tm = find_word(mo.get('word'), wt, a0, t1) if mo.get('word') else None
        timeline.append((a0 if tm is None else tm, 'mood', mo.get('mood', 'happy')))
    timeline.sort(key=lambda x: (x[0], {'move': 0, 'mood': 1, 'point': 2}[x[1]]))
    out.append(f'tl.set("#{t}_arm",{{rotation:{REST},{org}}},0);')
    cur_tgt = None; tracked = False; last_ang = REST
    for tm, kind, pl in timeline:
        if kind == 'move':
            nx = pl.get('x', st['ox']); ny = pl.get('y', d['y']); nfl = pl.get('flip', d['flip']); ns = pl.get('s', d['s'])
            # frog space = (base group transform) -> _in; hop in _in local units: x offset, y arc, scale change relative to the base
            r = ns / base['s']; rel_flip = (nfl * ns) / (base['sx'] * r) if base['sx'] else 1
            dx = (nx - base['ox']) / base['sx']; dy = (ny - base['y']) / base['s']
            dur = .55
            out.append(f'tl.to("#{t}_in",{{x:{dx:.1f},y:{dy:.1f},scaleX:{rel_flip * r:.3f},scaleY:{r:.3f},svgOrigin:"0 0",duration:{dur},ease:"power1.inOut"}},{tm:.3f});')
            out.append(f'tl.to("#{t}_in",{{y:{dy - 34 * ns / base["s"]:.1f},duration:{dur / 2},ease:"power2.out",overwrite:false}},{tm:.3f});tl.to("#{t}_in",{{y:{dy:.1f},duration:{dur / 2},ease:"power2.in",overwrite:false}},{tm + dur / 2:.3f});')
            st = dict(ox=base['ox'] + base['sx'] * dx, y=base['y'] + base['s'] * dy, sx=base['sx'] * r * rel_flip, s=ns)
            if cur_tgt is not None:   # keep pointing at the same object from the new place
                out.append(f'tl.to("#{t}_arm",{{rotation:{angle_to(d, cur_tgt, st):.1f},duration:{dur},ease:"power1.inOut"}},{tm:.3f});')
        elif kind == 'point':
            obj = pl.get('obj') if isinstance(pl, dict) else None
            pl = pl['to'] if isinstance(pl, dict) else pl
            cur_tgt = pl; a1 = angle_to(d, pl, st)
            if obj:   # the arm follows the pointed object while it moves (its position is read from the page on every frame; eased in over .4 s)
                nxt = [x[0] for x in timeline if x[1] == 'point' and x[0] > tm]; te = min(nxt + [t1]) - .05
                if not tracked: out.append(TRACK_FN); tracked = True
                out.append(f'tl.fromTo("#{t}_arm",{{rotation:{last_ang:.1f}}},{{rotation:{last_ang:.1f},duration:{max(te - tm, .1):.3f},ease:"none",immediateRender:false,'
                           f'modifiers:{{rotation:function(v){{var g=window.__fgAim("{t}","#w{t[3:]} .{obj}");if(g===null)return v;var w=Math.min(1,Math.max(0,(tl.time()-{tm:.3f})/.4));'
                           f'w=w*w*(3-2*w);var dd=((g-{last_ang:.1f}+540)%360)-180;return {last_ang:.1f}+dd*w;}}}}}},{tm:.3f});')
                last_ang = a1
            else:
                out.append(f'tl.to("#{t}_arm",{{rotation:{a1:.1f},duration:.35,ease:"power2.out"}},{tm:.3f});'); last_ang = a1
        else:
            M = MOODS.get(pl, MOODS['happy'])
            out.append(f'tl.set("#{t}_bl",{{attr:{{d:"{M["bl"]}"}},opacity:{M["bo"]}}},{tm:.3f});tl.set("#{t}_br",{{attr:{{d:"{M["br"]}"}},opacity:{M["bo"]}}},{tm:.3f});'
                       f'tl.set("#{t}_pl",{{attr:{{cx:{-8 + M["pup"][0]},cy:{-66 + M["pup"][1]},r:{M["pup"][2]}}}}},{tm:.3f});tl.set("#{t}_pr",{{attr:{{cx:{24 + M["pup"][0]},cy:{-66 + M["pup"][1]},r:{M["pup"][2]}}}}},{tm:.3f});'
                       f'tl.set("#{t}_sm",{{attr:{{d:"{M["sm"]}",fill:"{M["fill"]}"}}}},{tm:.3f});tl.set("#{t}_ll,#{t}_lr",{{attr:{{height:{M["lid"]}}}}},{tm:.3f});')
    # mouth follows the spoken words: closed = the mood's mouth; open = a big round "ahh" of the same width that hangs from the smile line, with a tongue
    for k, (ws, we) in enumerate(words):
        if ws < a0 or ws > t1: continue
        r = (10, 7, 12, 8)[k % 4]; e = max(ws + .08, we - .03)
        out.append(f'tl.set("#{t}_sm",{{opacity:0}},{ws:.3f});tl.set("#{t}_mo",{{attr:{{ry:{r},cy:{-44 + r}}}}},{ws:.3f});tl.set("#{t}_tg",{{attr:{{ry:{r * .42:.1f},cy:{-44 + r * 1.58:.1f}}}}},{ws:.3f});'
                   f'tl.set("#{t}_mo",{{attr:{{ry:0,cy:-44}}}},{e:.3f});tl.set("#{t}_tg",{{attr:{{ry:0,cy:-44}}}},{e:.3f});tl.set("#{t}_sm",{{opacity:1}},{e:.3f});')
    # blink every ~2.7 s (back to the mood's eye height afterwards)
    lid = MOODS.get((d.get('moods') or [{}])[0].get('mood', 'happy'), MOODS['happy'])['lid']
    tb = a0 + 1.1
    while tb < t1 - .2:
        out.append(f'tl.to("#{t}_ll,#{t}_lr",{{attr:{{height:27}},duration:.06,ease:"none"}},{tb:.3f});tl.set("#{t}_al,#{t}_ar",{{opacity:1}},{tb + .06:.3f});'
                   f'tl.set("#{t}_al,#{t}_ar",{{opacity:0}},{tb + .1:.3f});tl.to("#{t}_ll,#{t}_lr",{{attr:{{height:{lid}}},duration:.08,ease:"none"}},{tb + .1:.3f});')
        tb += 2.7
    return out
