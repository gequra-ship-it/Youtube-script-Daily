# -*- coding: utf-8 -*-
# Notebook frog (Miya's Note mascot) as an explainer inside the video (owner decision 2026-10-24, guideline 7-2 / 20-8).
# The frog hops in next to the thing it explains, points at it, talks (mouth follows the real word times) and blinks.
# markup()  -> SVG group string to put INTO a picture svg (ids fg<tag>_*), or into an overlay svg for chalkboard scenes
# js()      -> GSAP lines (absolute timeline seconds) for that frog
# Sidecar key in art3/<uid>.json: "frog": {"x": 220, "y": 1040, "s": 2.4, "flip": 1, "point": [tx, ty], "delay": 0.35}
#   x, y = feet position (picture coords), s = scale (82 units tall at s=1), flip = -1 mirrors it (arm then points left),
#   point = what the arm points at (omit: arm raised, waving), delay = seconds after the unit starts. `"frog": true` = defaults.
import math, re

INK = '#1d2b1c'; GREEN = '#6aa55a'


def defaults(vert=False):
    return dict(x=210, y=1400, s=2.4, flip=1, point=None, delay=0.35) if vert else dict(x=220, y=880, s=2.4, flip=1, point=None, delay=0.35)


def spec(sidecar, vert=False):
    f = (sidecar or {}).get('frog')
    if not f: return None
    d = defaults(vert)
    if isinstance(f, dict): d.update({k: v for k, v in f.items() if v is not None or k == 'point'})
    return d


def shoulder(d):
    """arm pivot in picture coordinates"""
    return d['x'] + d['flip'] * d['s'] * 32, d['y'] - d['s'] * 22


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
            f'<circle cx="-10" cy="-66" r="13" fill="#e3e5d6" stroke-width="3.2"/><circle cx="-8" cy="-66" r="5" fill="{INK}" stroke="none"/>'
            f'<circle cx="22" cy="-66" r="13" fill="#e3e5d6" stroke-width="3.2"/><circle cx="24" cy="-66" r="5" fill="{INK}" stroke="none"/>'
            f'<g clip-path="url(#{t}_cl)"><rect id="{t}_ll" x="-24" y="-80" width="28" height="0" fill="{GREEN}" stroke="none"/></g>'
            f'<g clip-path="url(#{t}_cr)"><rect id="{t}_lr" x="8" y="-80" width="28" height="0" fill="{GREEN}" stroke="none"/></g>'
            f'<circle cx="-10" cy="-66" r="13" fill="none" stroke-width="3.2"/><circle cx="22" cy="-66" r="13" fill="none" stroke-width="3.2"/>'
            f'<path id="{t}_al" d="M-20 -64 q10 7 20 0" fill="none" stroke-width="3" opacity="0"/><path id="{t}_ar" d="M12 -64 q10 7 20 0" fill="none" stroke-width="3" opacity="0"/>'
            f'<path d="M-8 -44 q14 12 28 0" fill="none" stroke-width="3.4"/>'
            f'<ellipse id="{t}_mo" cx="6" cy="-39" rx="8" ry="0" fill="#7a2f2f" stroke-width="2.6"/>'
            f'<path d="M-34 -22 q-14 6 -16 22" fill="none" stroke-width="7.5"/><path d="M-34 -22 q-14 6 -16 22" fill="none" stroke="{GREEN}" stroke-width="3.4"/>'
            f'<g transform="translate(32 -22)"><g id="{t}_arm">'
            f'<path d="M0 0 L58 0" stroke-width="11"/><circle cx="60" cy="0" r="9" fill="{INK}" stroke="none"/>'
            f'<path d="M0 0 L58 0" stroke="{GREEN}" stroke-width="6"/><circle cx="60" cy="0" r="6" fill="{GREEN}" stroke="none"/>'
            f'</g></g></g></g>')


def inject(svg_text, mk):
    i = svg_text.rfind('</svg>')
    return svg_text[:i] + mk + svg_text[i:] if i >= 0 else svg_text + mk


def angle_to(d, target):
    """local rotation (deg) of the arm so that it points at target (picture coords)"""
    sx, sy = shoulder(d)
    lx = (target[0] - sx) / (d['flip'] * d['s']); ly = (target[1] - sy) / d['s']
    return math.degrees(math.atan2(ly, lx))


def js(tag, d, t0, t1, words, targets=None):
    """GSAP lines. words = [(start, end)] absolute seconds of the unit's words (mouth), targets = [(time, (x, y))] arm pointing
    (default: one target = d['point'] at t0+delay; none = arm raised and waving)"""
    t = f'fg{tag}'; out = []; a0 = t0 + d['delay']; sx, sy = shoulder(d)
    org = 'svgOrigin:"0 0"'   # the arm's own coordinate space starts at the shoulder (parent group translate(32 -22))
    out.append(f'tl.set("#{t}_in",{{opacity:0,y:300}},0);tl.set("#{t}",{{opacity:0}},0);tl.set("#{t}",{{opacity:1}},{a0 - .01:.3f});tl.set("#{t}",{{opacity:0}},{t1:.3f});')
    out.append(f'tl.fromTo("#{t}_in",{{y:300,opacity:0}},{{y:0,opacity:1,duration:.45,ease:"back.out(1.6)",immediateRender:false}},{a0:.3f});')
    # arm
    tg = targets if targets is not None else ([(a0 + .5, d['point'])] if d.get('point') else [])
    if tg:
        ang = angle_to(d, tg[0][1])
        out.append(f'tl.set("#{t}_arm",{{rotation:{ang + 55:.1f},{org}}},0);')
        for k, (tt, p) in enumerate(tg):
            a = angle_to(d, p)
            out.append(f'tl.to("#{t}_arm",{{rotation:{a:.1f},duration:.3,ease:"power2.out"}},{tt:.3f});')
        if len(tg) == 1:   # gentle nodding of the pointing arm
            n = max(1, int((t1 - tg[0][0]) / .5)); a = angle_to(d, tg[0][1])
            out.append(f'tl.fromTo("#{t}_arm",{{rotation:{a - 4:.1f}}},{{rotation:{a + 4:.1f},duration:.5,ease:"sine.inOut",repeat:{n},yoyo:true,immediateRender:false}},{tg[0][0] + .3:.3f});')
    else:   # raised, waving
        up = -75 if d['flip'] == 1 else -75
        out.append(f'tl.set("#{t}_arm",{{rotation:{up},{org}}},0);')
        n = max(1, int((t1 - a0 - .5) / .35))
        out.append(f'tl.fromTo("#{t}_arm",{{rotation:{up - 14}}},{{rotation:{up + 14},duration:.35,ease:"sine.inOut",repeat:{n},yoyo:true,immediateRender:false}},{a0 + .45:.3f});')
    # mouth follows the spoken words
    for k, (ws, we) in enumerate(words):
        if ws < a0 or ws > t1: continue
        r = (5.5, 7.0, 4.5)[k % 3]
        out.append(f'tl.set("#{t}_mo",{{attr:{{ry:{r}}}}},{ws:.3f});tl.set("#{t}_mo",{{attr:{{ry:0}}}},{max(ws + .06, we - .03):.3f});')
    # blink every ~2.7 s
    tb = a0 + 1.1
    while tb < t1 - .2:
        out.append(f'tl.to("#{t}_ll,#{t}_lr",{{attr:{{height:27}},duration:.06,ease:"none"}},{tb:.3f});tl.set("#{t}_al,#{t}_ar",{{opacity:1}},{tb + .06:.3f});'
                   f'tl.set("#{t}_al,#{t}_ar",{{opacity:0}},{tb + .1:.3f});tl.to("#{t}_ll,#{t}_lr",{{attr:{{height:0}},duration:.08,ease:"none"}},{tb + .1:.3f});')
        tb += 2.7
    return out
