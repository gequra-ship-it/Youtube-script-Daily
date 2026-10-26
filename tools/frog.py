# -*- coding: utf-8 -*-
# Notebook frog (Miya's Note mascot) inside the video (owner decisions 2026-10-24 / 2026-10-25, guideline 7-2).
# Two roles:
#   CHALKBOARD scenes: the explainer. It stands bottom-left, talks (mouth follows the real word times), blinks and points at the row being
#     spoken (js(..., targets=...)); the arm turns only when the pointed row changes.
#   PICTURE scenes (plan.json frog_hint units): NO explainer standing beside the picture. A companion: it rides a moving object (drawn INSIDE
#     that picture group via inject(..., ride=id), so it moves and turns with it) or sits small in a bottom corner of the background; the arm is
#     hidden unless the sidecar has points. tools/frog_place.py writes these sidecars (moods per sentence, helmet / goggles, ride or corner).
# markup()  -> SVG group string to put INTO a picture svg (ids fg<tag>_*), or into an overlay svg for chalkboard scenes
# js()      -> GSAP lines (absolute timeline seconds) for that frog
# Sidecar key in art3/<uid>.json: "frog": {"x": 220, "y": 1040, "s": 2.4, "flip": 1, "delay": 0.35, ...}
#   x, y = feet position (picture coords; for "ride" the coordinates of the group before it moves), s = scale (82 units tall at s=1),
#   flip = -1 mirrors it, delay = seconds after the unit starts. `"frog": true` = defaults.
#   "ride": "<id of a picture group>"  the frog is injected into that group. Only use groups whose motion does not flip/fade/clip
#     (core swell|heartbeat|wobble|sway|glide|approach|drop|ping|tremble, path, slide, swing). Never flip, flicker, reveal, fade, fill, grow, edge.
#   "moods": [{"word": "...", "mood": "happy|surprised|curious|worried|proud|excited"}] (first entry without "word" = at the start),
#   "outfit": ["helmet"] | ["goggles"] | ["diver"] (bubble space helmet / diving mask + snorkel / full diving suit with tank: use it in deep-water scenes),
#   "talk": true|false  mouth follows the spoken words. Default: chalkboard explainer yes, picture companion (ride / bg) NO (miya 2026-10-25: no lip-sync needed; the mouth opens only when the scene calls for it, e.g. a surprised / excited mood),
#   "enter": "hop" (default, jumps up from below) | "pop" (appears in place),
#   optional pointing (chalkboard, or a deliberate exception): "point": [tx, ty] or "points": [{"word": "Voyager", "to": [x, y], "obj": "<group class>"}];
#     with "obj" (or "point_obj") the arm FOLLOWS that moving object (its position is read from the page every frame, modifiers keep it seekable).
#     The arm turns ONLY when the pointed object changes; no waving or nodding. A unit without points hides the arm.
#   "moves": [{"word": "...", "x": .., "y": .., "flip": 1|-1, "s": ..}]  the frog hops to a new place (not used with "ride").
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
    if 'diver' in names:     # diving suit (miya 2026-10-25): navy wetsuit with a yellow stripe, air tank + hose on the back, mask on the eyes
        o += ('<rect x="-54" y="-60" width="17" height="42" rx="7" fill="#d9a630" stroke-width="3"/><rect x="-50" y="-66" width="9" height="8" rx="2" fill="#8a8f96" stroke-width="2.4"/><path d="M-45 -66 q-6 -20 18 -22" fill="none" stroke="#8a8f96" stroke-width="3.4"/>'
              '<path d="M-35 -16 q-1 -20 6 -26 q36 8 72 0 q4 8 4 28 q0 10 -6 12 q-36 6 -70 -4z" fill="#24465e" stroke-width="3.6"/><path d="M-33 -22 q35 7 72 0" fill="none" stroke="#e8b838" stroke-width="3.2"/>'
              '<path d="M40 -66 q12 -12 8 -46" fill="none" stroke="#e0b84a" stroke-width="6"/>'
              '<rect x="-27" y="-84" width="68" height="34" rx="14" fill="#9fd8ff" fill-opacity=".35" stroke-width="4.2"/><path d="M-27 -66 q-14 0 -16 8 M41 -66 q10 0 12 8" fill="none" stroke="#e0b84a" stroke-width="5"/>')
    if 'fore' in names:      # (miya 2026-10-26) Fore highlands outfit, simple and respectful: woven leaf waist-wrap, red-and-orange string bag (bilum) on a shoulder strap, feather headband
        o += ('<path d="M-36 -22 q36 14 74 0 l-3 4 q-34 12 -68 0z" fill="#7a5a30" stroke-width="3"/>'
              + ''.join(f'<path d="M{-33 + k * 7.6:.1f} -14 q-1 14 {-1 + (k % 3)} 18" fill="none" stroke="{["#5f8a3c", "#8a6a3c", "#6f9a44"][k % 3]}" stroke-width="5"/>' for k in range(9))
              + '<path d="M-30 -56 q28 22 60 44" fill="none" stroke="#b5442a" stroke-width="4"/>'
              '<path d="M-44 -22 q-4 -16 12 -20 q16 4 14 20 q-12 12 -26 0z" fill="#d9703a" stroke-width="3"/>'
              '<path d="M-42 -30 h22 M-41 -24 h22 M-34 -40 v22 M-27 -40 v24" fill="none" stroke="#7a2f20" stroke-width="1.6"/>'
              '<path d="M-26 -86 q32 -16 64 0" fill="none" stroke="#b5442a" stroke-width="5"/>'
              '<ellipse cx="-2" cy="-100" rx="5" ry="15" transform="rotate(-18 -2 -100)" fill="#e8b838" stroke-width="2.6"/>'
              '<ellipse cx="10" cy="-104" rx="5" ry="16" fill="#c2452d" stroke-width="2.6"/>'
              '<ellipse cx="22" cy="-100" rx="5" ry="15" transform="rotate(18 22 -100)" fill="#2f8f5a" stroke-width="2.6"/>')
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
    'sad':       dict(bl='M-24 -76 q12 -4 24 -12', br='M10 -88 q12 8 24 12', bo=1, pup=(0, 3, 6), sm='M-8 -36 q14 -10 28 0', fill='none', lid=0),   # miya 2026-10-26: sad / pleading face (caged, lonely): brows slanting up in the middle, mouth turned down, pupils looking down
    'scared':    dict(bl='M-24 -80 q12 -2 24 -9', br='M10 -89 q12 7 24 9', bo=1, pup=(0, 1, 3), sm='M-9 -39 q4.5 -7 9 0 q4.5 7 9 0 q4.5 -7 9 0', fill='none', lid=0),
    'dizzy':     dict(bl='M-24 -80 q12 -2 24 -8', br='M10 -88 q12 6 24 8', bo=1, pup=(0, 0, 2.2), sm='M-9 -40 q4.5 -6 9 0 q4.5 6 9 0 q4.5 -6 9 0', fill='none', lid=5),   # miya 2026-10-26: woozy face while circling a black hole ring: tiny pupils, wavy mouth, half lids
    'squint':    dict(bl='M-24 -78 q12 -6 24 -2', br='M10 -80 q12 4 24 8', bo=1, pup=(0, 0, 4), sm='M-10 -47 q16 24 32 0z', fill='#7a2f2f', lid=11),
    'sleepy':    dict(bl='M-24 -80 q12 2 24 -2', br='M10 -82 q12 -2 24 2', bo=1, pup=(0, 3, 4.5), sm='M-6 -42 q8 3 16 0', fill='none', lid=14),
    'dizzy':     dict(bl='M-24 -78 q12 4 24 -4', br='M10 -80 q12 -4 24 4', bo=1, pup=(0, 0, 0.1), sm='M-10 -44 q4 -7 8 0 q4 7 8 0 q4 -7 8 0 q4 7 8 0', fill='none', lid=0),   # swirl eyes (the _sp spirals cover the pupils), wobbly mouth (2026-10-26 miya: overheated frog)
    'excited':   dict(bl='M-24 -90 q12 -8 24 0', br='M10 -90 q12 -8 24 0', bo=1, pup=(0, -1, 5.6), sm='M-10 -47 q16 24 32 0z', fill='#7a2f2f', lid=0),
}


def markup(tag, d):
    t = f'fg{tag}'
    x, y, s, fl = d['x'], d['y'], d['s'], d['flip']
    return (f'<g id="{t}" transform="translate({x:.1f} {y:.1f}) scale({fl * s:.3f} {s:.3f})" stroke="{INK}" stroke-linejoin="round" stroke-linecap="round">'
            f'<defs><clipPath id="{t}_cl"><circle cx="-10" cy="-66" r="13"/></clipPath><clipPath id="{t}_cr"><circle cx="22" cy="-66" r="13"/></clipPath></defs>'
            f'<ellipse cx="0" cy="8" rx="52" ry="8" fill="#000" opacity=".18" stroke="none"/>'
            f'<g id="{t}_wd" opacity="0" fill="none" stroke="#e8f3ff" stroke-width="3.4" stroke-linecap="round"><path d="M70 -70 h46"/><path d="M82 -44 h56"/><path d="M70 -18 h40"/><path d="M96 -88 h34"/></g>'
            f'<g id="{t}_in"><g id="{t}_tr"><g id="{t}_rm"><g id="{t}_ac">'
            f'<ellipse cx="-22" cy="4" rx="16" ry="9" fill="#4d8a4a" stroke-width="3.2"/><ellipse cx="22" cy="4" rx="16" ry="9" fill="#4d8a4a" stroke-width="3.2"/>'
            f'<path d="M-34 0 q-6 -64 34 -70 q40 -2 42 62 q0 10 -6 12 q-36 6 -70 -4z" fill="{GREEN}" stroke-width="4"/>'
            f'<ellipse cx="2" cy="-12" rx="22" ry="20" fill="#9cc98a" stroke="none" opacity=".7"/>'
            f'<circle cx="-10" cy="-66" r="13" fill="#e3e5d6" stroke-width="3.2"/><circle id="{t}_pl" cx="-8" cy="-66" r="5" fill="{INK}" stroke="none"/>'
            f'<circle cx="22" cy="-66" r="13" fill="#e3e5d6" stroke-width="3.2"/><circle id="{t}_pr" cx="24" cy="-66" r="5" fill="{INK}" stroke="none"/>'
            f'<g clip-path="url(#{t}_cl)"><rect id="{t}_ll" x="-24" y="-80" width="28" height="0" fill="{GREEN}" stroke="none"/></g>'
            f'<g clip-path="url(#{t}_cr)"><rect id="{t}_lr" x="8" y="-80" width="28" height="0" fill="{GREEN}" stroke="none"/></g>'
            f'<circle cx="-10" cy="-66" r="13" fill="none" stroke-width="3.2"/><circle cx="22" cy="-66" r="13" fill="none" stroke-width="3.2"/>'
            f'<g id="{t}_spl" opacity="0"><circle cx="-10" cy="-66" r="12" fill="#e3e5d6" stroke="none"/><path d="M-10.0 -66.0 L-9.8 -65.9 L-9.6 -65.7 L-9.6 -65.4 L-9.8 -65.0 L-10.2 -64.8 L-10.7 -64.7 L-11.3 -64.8 L-11.9 -65.3 L-12.2 -65.9 L-12.4 -66.8 L-12.2 -67.7 L-11.6 -68.5 L-10.7 -69.2 L-9.6 -69.5 L-8.3 -69.3 L-7.1 -68.7 L-6.1 -67.7 L-5.5 -66.3 L-5.4 -64.7 L-6.0 -63.1 L-7.0 -61.7 L-8.6 -60.7 L-10.5 -60.3 L-12.6 -60.6 L-14.4 -61.6 L-15.9 -63.2 L-16.7 -65.4 L-16.8 -67.7 L-16.0 -70.1 L-14.4 -72.1 L-12.2 -73.4 L-9.5 -74.0 L-6.7 -73.6 L-4.2 -72.2 L-2.2 -70.0 L-1.1 -67.1 L-1.0 -64.0 L-2.0 -60.9 L-4.0 -58.3 L-6.9 -56.5" fill="none" stroke-width="2.4"/></g>'
            f'<g id="{t}_spr" opacity="0"><circle cx="22" cy="-66" r="12" fill="#e3e5d6" stroke="none"/><path d="M22.0 -66.0 L22.2 -65.9 L22.4 -65.7 L22.4 -65.4 L22.2 -65.0 L21.8 -64.8 L21.3 -64.7 L20.7 -64.8 L20.1 -65.3 L19.8 -65.9 L19.6 -66.8 L19.8 -67.7 L20.4 -68.5 L21.3 -69.2 L22.4 -69.5 L23.7 -69.3 L24.9 -68.7 L25.9 -67.7 L26.5 -66.3 L26.6 -64.7 L26.0 -63.1 L25.0 -61.7 L23.4 -60.7 L21.5 -60.3 L19.4 -60.6 L17.6 -61.6 L16.1 -63.2 L15.3 -65.4 L15.2 -67.7 L16.0 -70.1 L17.6 -72.1 L19.8 -73.4 L22.5 -74.0 L25.3 -73.6 L27.8 -72.2 L29.8 -70.0 L30.9 -67.1 L31.0 -64.0 L30.0 -60.9 L28.0 -58.3 L25.1 -56.5" fill="none" stroke-width="2.4"/></g>'
            f'<ellipse id="{t}_fl1" cx="-20" cy="-48" rx="9" ry="5.5" fill="#e8605a" stroke="none" opacity="0"/><ellipse id="{t}_fl2" cx="34" cy="-48" rx="9" ry="5.5" fill="#e8605a" stroke="none" opacity="0"/>'
            f'<path id="{t}_al" d="M-20 -64 q10 7 20 0" fill="none" stroke-width="3" opacity="0"/><path id="{t}_ar" d="M12 -64 q10 7 20 0" fill="none" stroke-width="3" opacity="0"/>'
            f'<path id="{t}_bl" d="M-24 -84 q12 -6 24 0" fill="none" stroke-width="3.4" opacity="0"/><path id="{t}_br" d="M10 -84 q12 -6 24 0" fill="none" stroke-width="3.4" opacity="0"/>'
            f'<path id="{t}_sm" d="M-8 -44 q14 12 28 0" fill="none" stroke-width="3.4"/>'
            f'<ellipse id="{t}_mo" cx="6" cy="-44" rx="13" ry="0" fill="#7a2f2f" stroke-width="2.8"/>'
            f'<ellipse id="{t}_tg" cx="6" cy="-44" rx="8" ry="0" fill="#e8847a" stroke="none"/>'
            f'<path d="M-34 -22 q-14 6 -16 22" fill="none" stroke-width="7.5"/><path d="M-34 -22 q-14 6 -16 22" fill="none" stroke="{GREEN}" stroke-width="3.4"/>'
            f'<g id="{t}_ra"><path d="M34 -22 q14 6 16 22" fill="none" stroke-width="7.5"/><path d="M34 -22 q14 6 16 22" fill="none" stroke="{GREEN}" stroke-width="3.4"/>'
            f'<g id="{t}_pc" opacity="0" transform="translate(50 0) rotate(-35)"><rect x="-3.4" y="-40" width="6.8" height="36" rx="1.4" fill="#f2c94c" stroke-width="2.4"/><rect x="-3.4" y="-45" width="6.8" height="6" rx="2" fill="#e8847a" stroke-width="2.2"/><path d="M-3.4 -4 L0 6 L3.4 -4z" fill="#e8c9a0" stroke-width="2"/><path d="M-1.2 2 L0 6 L1.2 2z" fill="#3a3a3a" stroke="none"/></g></g>'
            f'<g id="{t}_dd" opacity="0" fill="none" stroke="#4a4a52" stroke-width="3" stroke-linecap="round"><path id="{t}_dd1" pathLength="1" d="M58 0 q8 -16 16 0 t16 0 t16 0 t16 0 q10 -14 -2 -16 q-12 0 -6 14"/><path id="{t}_dd2" pathLength="1" d="M60 -26 l4 12 l-12 -8 l16 0 l-12 8z"/><path id="{t}_dd3" pathLength="1" d="M118 -34 q8 -12 16 0 q6 12 -16 24 q-22 -12 -16 -24 q8 -12 16 0"/></g>'
            f'<g id="{t}_sw" opacity="0" fill="#7fc4f0" stroke="#2f6f9a" stroke-width="2"><path id="{t}_sw0" d="M-34 -98 q-6 12 0 14 q6 -2 0 -14z"/><path id="{t}_sw1" d="M44 -96 q-6 12 0 14 q6 -2 0 -14z"/><path id="{t}_sw2" d="M6 -112 q-6 12 0 14 q6 -2 0 -14z"/></g>'
            f'{outfit_markup(t, d.get("outfit") or [])}'
            f'<g transform="translate(32 -22)"><g id="{t}_arm">'
            f'<path d="M0 0 L58 0" stroke-width="11"/><circle cx="60" cy="0" r="9" fill="{INK}" stroke="none"/>'
            f'<path d="M0 0 L58 0" stroke="{GREEN}" stroke-width="6"/><circle cx="60" cy="0" r="6" fill="{GREEN}" stroke="none"/>'
            f'</g></g></g></g>{bubble_markup(t, d)}</g></g></g>')

def bubble_geom(sy, d):
    tx = sy['text'][:24]; wd = 26 * len(tx) * .5 + 44; hh = 34
    side = d.get('bside', 1)   # +1: the bubble body leans to the right of the frog (screen), -1: to the left
    bx = side * max(0, wd / 2 - 30); x1 = bx - wd / 2; x2 = bx + wd / 2; r = 14; top = -(hh * 2 + 8); bot = -14
    path = (f'M{x1 + r:.0f} {top} H{x2 - r:.0f} a{r} {r} 0 0 1 {r} {r} V{bot - r} a{r} {r} 0 0 1 -{r} {r} H12 L0 0 L-12 {bot} H{x1 + r:.0f} '
            f'a{r} {r} 0 0 1 -{r} -{r} V{top + r} a{r} {r} 0 0 1 {r} -{r}z')
    return tx, path, bx, (top + bot) / 2 + 15


def bubble_markup(t, d):
    """speech bubbles with a sound word / short reaction (miya 2026-10-26); drawn at screen size above the head, they follow the frog (rides, roams).
    Each bubble group is counter-scaled so the text is never mirrored or shrunk by the frog's flip/scale."""
    out = ''
    s, fl = d['s'], d['flip']
    for k, sy in enumerate(d.get('says') or []):
        tx, path, bx, ty = bubble_geom(sy, d)
        out += (f'<g id="{t}_bub{k}" opacity="0" transform="translate(0 -96) scale({fl / s:.4f} {1 / s:.4f})">'
                f'<g id="{t}_bx{k}"><path d="{path}" fill="#fff" stroke="#14122b" stroke-width="3.2" stroke-linejoin="round"/>'
                f'<text x="{bx:.0f}" y="{ty:.0f}" text-anchor="middle" font-family="Patrick,sans-serif" font-size="44" fill="#14122b" stroke="none">{tx}</text></g></g>')
    return out


RIDEABLE = re.compile(r'^mv-(core-(swell|heartbeat|wobble|sway|glide|approach|drop|ping|tremble)|path|slide|swing)')


def lint(d, vert=False):
    """warnings for a PICTURE-scene frog sidecar (guideline 7-2, 2026-10-25): it must ride a moving object , sit in a bottom corner or roam through the background (sidecar roam), never stand mid-picture or point"""
    w = []
    if d.get('point') or d.get('points'): w.append('points in a picture scene (the explainer is chalkboard only)')
    if d.get('ride'):
        if not RIDEABLE.match(d['ride']): w.append(f'rides {d["ride"]}, a motion that flips/fades/fills/clips (pick a core swell|heartbeat|wobble|sway|glide|approach|drop|ping|tremble, path, slide or swing group)')
    elif not d.get('roam') and not (isinstance(d.get('act'), dict) and d['act'].get('type') == 'orbit') and d['y'] < (1920 - 200 if vert else 1080 - 100): w.append('stands mid-picture (use "ride" or a bottom corner: python3 tools/frog_place.py <slug>)')
    return w



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
    out.append(f'tl.set("#{t}_arm",{{rotation:{REST},{org}}},0);tl.set("#{t}_spl,#{t}_spr,#{t}_fl1,#{t}_fl2,#{t}_sw,#{t}_dd,#{t}_pc",{{opacity:0}},0);')
    if not pts: out.append(f'tl.set("#{t}_arm",{{opacity:0}},0);')   # no pointing in this unit (rides / sits in the background): the long arm stick is hidden and a short resting right arm shows instead
    else: out.append(f'tl.set("#{t}_ra",{{opacity:0}},0);')   # pointing frog (chalkboard): the long pointing arm is the right arm
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
                       f'tl.set("#{t}_sm",{{attr:{{d:"{M["sm"]}",fill:"{M["fill"]}"}}}},{tm:.3f});tl.set("#{t}_ll,#{t}_lr",{{attr:{{height:{M["lid"]}}}}},{tm:.3f});'
                       f'tl.set("#{t}_spl,#{t}_spr",{{opacity:{1 if pl == "dizzy" else 0}}},{tm:.3f});')
    # ---- body act (2026-10-25, miya: expression + motion that fits the situation); all tweens on #<t>_ac, absolute times so seeking works ----
    act = d.get('act'); at = (act.get('type') if isinstance(act, dict) else act) or None
    if at:
        ac = f'"#{t}_ac"'; a1 = a0 + .5; T = t1 - .05; org2 = 'svgOrigin:"0 0"'
        if isinstance(act, dict) and act.get('from') is not None: a1 = t0 + float(act['from'])   # start the act this many seconds into the unit
        tg = (act.get('to') if isinstance(act, dict) else None) or [d['x'] + 300 * d['flip'], d['y']]
        dirn = 1 if (tg[0] - d['x']) * d['flip'] >= 0 else -1   # +1 = the hole/thing lies in front of the frog (its facing side), -1 = behind
        k = 0; tm = a1
        if at == 'wind':      # leaning back into the wind, bracing, squinting; air streaks fly past
            out.append(f'tl.to({ac},{{rotation:-10,x:-4,duration:.4,ease:"power2.out",{org2}}},{a1:.3f});')
            nn = max(int((T - a1 - .4) / .8), 1)   # smooth lean sway (miya 2026-10-26: the old 0.09 s jitter looked unnatural); one yoyo tween, seek-safe
            out.append(f'tl.to({ac},{{rotation:-13,y:-3,x:-5,duration:.8,yoyo:true,repeat:{nn},ease:"sine.inOut",{org2}}},{a1 + .4:.3f});')
        elif at == 'pull':    # dragged toward the hole: slides and leans, digs in, gets dragged again (never quite escapes)
            vz = isinstance(act, dict) and act.get('vanish')   # miya 2026-10-26: sucked in like the star: spirals toward the hole, shrinks and disappears
            if vz:
                vd = float(vz) if not isinstance(vz, bool) else 2.2; tv = max(T - vd, a1 + .5)
                gx = d['flip'] * (tg[0] - d['x']) / d['s']; gy = (tg[1] - d['y']) / d['s']   # local x is mirrored by the frog's flip
                out.append(f'tl.to("#{t}_tr",{{x:{gx:.1f},y:{gy:.1f},duration:{T - tv:.3f},ease:"power2.in"}},{tv:.3f});')
                out.append(f'tl.to("#{t}_rm",{{rotation:{dirn * 360},scaleX:.04,scaleY:.04,duration:{T - tv:.3f},ease:"power2.in",svgOrigin:"0 -30"}},{tv:.3f});')
                out.append(f'tl.to("#{t}_in",{{opacity:0,duration:.35,ease:"none"}},{T - .35:.3f});')
            te = (tv if vz else T) - .1
            if te > a1 + .4:   # soft lean in and out (no snapping) with a continuous fine tremble (miya 2026-10-26: trembling good, the stutter not)
                out.append(f'tl.to({ac},{{y:-2.2,duration:.1,yoyo:true,repeat:{int((te - a1) / .1)},ease:"sine.inOut"}},{a1:.3f});')
                while tm < te - .3:
                    dd = min(1.0, (te - tm) / 2)
                    out.append(f'tl.to({ac},{{x:{dirn * 14},rotation:{dirn * 2},duration:{dd:.2f},ease:"sine.inOut",{org2}}},{tm:.3f});')   # no head-tilt (miya 2026-10-26): stays upright, only slides and trembles
                    out.append(f'tl.to({ac},{{x:{-dirn * 3},rotation:0,duration:{dd:.2f},ease:"sine.inOut",{org2}}},{tm + dd:.3f});')
                    tm += 2 * dd
        elif at == 'orbit':   # circles a black hole ring like a particle on its line, woozy (miya 2026-10-26): ellipse about act.c with radii act.rx/ry, frog start = its angle act.th0
            import math
            c = act.get('c', [d['x'], d['y']]); rx = float(act.get('rx', 160)); ry = float(act.get('ry', 50)); th0 = math.radians(float(act.get('th0', 90))); per = float(act.get('per', 3.4)); sd = 1
            x0_ = rx * math.cos(th0); y0_ = ry * math.sin(th0); stp = .12; tt = a1
            while tt < T - .02:
                th = th0 + sd * 2 * math.pi * (tt + stp - a1) / per
                gx = d['flip'] * (rx * math.cos(th) - x0_) / d['s']; gy = (ry * math.sin(th) - y0_) / d['s']; sc = 1 + .14 * math.sin(th)   # nearer (front of the ring) = a little bigger
                out.append(f'tl.to("#{t}_tr",{{x:{gx:.1f},y:{gy:.1f},scaleX:{sc:.3f},scaleY:{sc:.3f},duration:{stp},ease:"none",svgOrigin:"0 0"}},{tt:.3f});'); tt += stp
            out.append(f'tl.to({ac},{{rotation:9,duration:.45,yoyo:true,repeat:{max(int((T - a1) / .45), 1)},ease:"sine.inOut",{org2}}},{a1:.3f});')   # head-rolling wobble
        elif at == 'dizzy':   # riding something that goes round and round (a particle on its line): head-rolling wobble, woozy face (miya 2026-10-26)
            out.append(f'tl.to({ac},{{rotation:10,y:-3,duration:.5,yoyo:true,repeat:{max(int((T - a1) / .5), 1)},ease:"sine.inOut",{org2}}},{a1:.3f});')
        elif at == 'float':   # weightless drift
            while tm < T - .2:
                out.append(f'tl.to({ac},{{y:-9,rotation:{3 if k % 2 == 0 else -3},duration:1.4,ease:"sine.inOut",{org2}}},{tm:.3f});tl.to({ac},{{y:3,rotation:{-3 if k % 2 == 0 else 3},duration:1.4,ease:"sine.inOut",{org2}}},{tm + 1.4:.3f});'); tm += 2.8; k += 1
        elif at == 'waves':   # riding / bracing against the swell
            while tm < T - .2:
                out.append(f'tl.to({ac},{{y:-14,rotation:{dirn * 7},duration:1.0,ease:"sine.inOut",{org2}}},{tm:.3f});tl.to({ac},{{y:4,rotation:{-dirn * 6},duration:1.0,ease:"sine.inOut",{org2}}},{tm + 1.0:.3f});'); tm += 2.0
        elif at == 'shiver':  # shaking with fear / cold / loneliness
            while tm < T - .1:
                out.append(f'tl.to({ac},{{x:{2.4 if k % 2 == 0 else -2.4},duration:.05,ease:"none"}},{tm:.3f});'); tm += .05; k += 1
        elif at == 'awe':     # looks up at something huge, slowly leans back, little step back
            out.append(f'tl.to({ac},{{rotation:-7,y:-3,duration:1.2,ease:"power1.out",{org2}}},{a1:.3f});tl.to("#{t}_pl,#{t}_pr",{{attr:{{cy:-71}},duration:.3}},{a1:.3f});')
            while tm < T - .2:
                out.append(f'tl.to({ac},{{y:-8,duration:1.1,ease:"sine.inOut"}},{tm + 1.2:.3f});tl.to({ac},{{y:-2,duration:1.1,ease:"sine.inOut"}},{tm + 2.3:.3f});'); tm += 2.2
        elif at == 'dizzy':   # overheated (miya 2026-10-26): swirl eyes, flushed cheeks, wobbly sway, sweat drops fall, sticks the tongue out of its wobbly mouth
            out.append(f'tl.to("#{t}_fl1,#{t}_fl2",{{opacity:.75,duration:.6}},{a1:.3f});tl.set("#{t}_sw",{{opacity:1}},{a1:.3f});')
            out.append(f'tl.fromTo("#{t}_spl",{{rotation:0}},{{rotation:1440,duration:{max(T - a1, .5):.3f},ease:"none",svgOrigin:"-10 -66",immediateRender:false}},{a1:.3f});tl.fromTo("#{t}_spr",{{rotation:0}},{{rotation:-1440,duration:{max(T - a1, .5):.3f},ease:"none",svgOrigin:"22 -66",immediateRender:false}},{a1:.3f});')
            n2 = 0
            while tm < T - .3:
                sgn = 1 if n2 % 2 == 0 else -1
                out.append(f'tl.to({ac},{{rotation:{sgn * 13},x:{sgn * 7},y:{-3 if n2 % 2 else 0},duration:.8,ease:"sine.inOut",{org2}}},{tm:.3f});'); tm += .8; n2 += 1
            for i2 in range(3):
                tw = a1 + .2 + i2 * .5
                while tw < T - .4:
                    out.append(f'tl.fromTo("#{t}_sw{i2}",{{y:0,opacity:1}},{{y:46,opacity:0,duration:1.0,ease:"power1.in",immediateRender:false}},{tw:.3f});'); tw += 1.5
        elif at == 'doodle':  # scribbles on the page with a pencil in its right hand: arm raised forward, quick small strokes, the doodle draws itself in front
            out.append(f'tl.set("#{t}_pc",{{opacity:1}},{a1 - .3:.3f});tl.to("#{t}_ra",{{rotation:-62,duration:.4,ease:"power2.out",svgOrigin:"34 -22"}},{a1 - .3:.3f});')
            span = max(T - a1, 1.0)
            out.append(f'tl.set("#{t}_dd",{{opacity:1}},{a1:.3f});')
            for i2, (dd0, dd1) in enumerate(((0, .45), (.45, .72), (.72, 1.0))):
                out.append(f'tl.fromTo("#{t}_dd{i2 + 1}",{{attr:{{"stroke-dasharray":1,"stroke-dashoffset":1}}}},{{attr:{{"stroke-dashoffset":0}},duration:{span * (dd1 - dd0):.3f},ease:"none",immediateRender:false}},{a1 + span * dd0:.3f});')
            n2 = 0; tw = a1
            while tw < T - .1:   # pencil hand scribbles (small seek-safe back-and-forth)
                out.append(f'tl.to("#{t}_ra",{{rotation:{-62 + (7 if n2 % 2 == 0 else -7)},duration:.11,ease:"none",svgOrigin:"34 -22"}},{tw:.3f});'); tw += .11; n2 += 1
            out.append(f'tl.to({ac},{{rotation:-4,duration:.5,ease:"sine.inOut",{org2}}},{a1:.3f});')
        elif at == 'cheer':   # happy hops with a little arm-free wiggle
            while tm < T - .2:
                out.append(f'tl.to({ac},{{y:-26,rotation:{6 if k % 2 == 0 else -6},duration:.28,ease:"power2.out",{org2}}},{tm:.3f});tl.to({ac},{{y:0,rotation:0,duration:.3,ease:"bounce.out",{org2}}},{tm + .28:.3f});'); tm += 1.1; k += 1
        elif at == 'sleepy':  # slow time: heavy slow sway, drooping
            while tm < T - .2:
                out.append(f'tl.to({ac},{{rotation:5,y:3,duration:2.2,ease:"sine.inOut",{org2}}},{tm:.3f});tl.to({ac},{{rotation:-4,y:0,duration:2.2,ease:"sine.inOut",{org2}}},{tm + 2.2:.3f});'); tm += 4.4
    # ---- speech bubble / sound word (2026-10-26): says = [{text, word?, dur?, shout?}]; pops in at the word, shakes when shouted, fades after dur ----
    for k, sy in enumerate(d.get('says') or []):
        tm = find_word(sy.get('word'), wt, a0, t1) if sy.get('word') else None
        if tm is None: tm = a0 + .7 + k * 2.4
        dur = min(sy.get('dur', 2.0), max(t1 - tm - .05, .6)); B = f'"#{t}_bub{k}"'; X = f'"#{t}_bx{k}"'
        out.append(f'tl.fromTo({B},{{opacity:0}},{{opacity:1,duration:.1,immediateRender:false}},{tm:.3f});')
        out.append(f'tl.fromTo({X},{{scale:.3,svgOrigin:"0 0"}},{{scale:1,duration:.28,ease:"back.out(2.4)",immediateRender:false}},{tm:.3f});')
        if sy.get('shout', True):
            n2 = 0; tt = tm + .3
            while tt < tm + dur - .1:
                out.append(f'tl.to({X},{{x:{2.5 if n2 % 2 == 0 else -2.5},rotation:{2 if n2 % 2 == 0 else -2},duration:.05,ease:"none",svgOrigin:"0 0"}},{tt:.3f});'); tt += .05; n2 += 1
            out.append(f'tl.to({X},{{x:0,rotation:0,duration:.05}},{tt:.3f});')
        out.append(f'tl.to({B},{{opacity:0,duration:.18}},{tm + dur:.3f});')
    # ---- roaming (2026-10-26, miya: the frog stayed in place at the bottom; let it move through the background): travels along its facing side on #<t>_rm ----
    rm = d.get('roam')
    if rm and not d.get('ride'):
        R = f'"#{t}_tr"'; RR = f'"#{t}_rm"'; kind = rm.get('kind', 'swim'); L = rm.get('dist', 500) / d['s']; ta = a0 + .45; T2 = t1 - .05; dur = max(T2 - ta, 1.0)
        out.append(f'tl.fromTo({R},{{x:0}},{{x:{L:.1f},duration:{dur:.3f},ease:"none",immediateRender:false}},{ta:.3f});')
        tm = ta; k = 0
        if kind == 'swim':    # weightless drift (miya 2026-10-26: floating, not paddling): slow eased travel, a long lazy up-down curve and a slow tumble
            out[-1] = out[-1].replace('ease:"none"', 'ease:"sine.inOut"')
            ys = (-18, 12, -10, 16, -14, 8); rs = (9, -11, 7, -9, 10, -6); k = 0; tm = ta; ty = 0
            while tm < T2 - .1:
                dd = 1.7 + (k % 3) * .5
                out.append(f'tl.to({R},{{y:{ys[k % 6]},duration:{dd:.2f},ease:"sine.inOut"}},{tm:.3f});'); tm += dd; k += 1
            tm = ta + .3; k = 0
            while tm < T2 - .1:
                dd = 2.3 + (k % 2) * .6
                out.append(f'tl.to({RR},{{rotation:{rs[k % 6]},duration:{dd:.2f},ease:"sine.inOut",svgOrigin:"0 -30"}},{tm:.3f});'); tm += dd; k += 1
        elif kind == 'lie':   # floating on its back: lies flat (head toward the drift), slowly bobbing and rocking
            out.append(f'tl.to({RR},{{rotation:78,duration:.9,ease:"sine.inOut",svgOrigin:"0 -30"}},{ta:.3f});')
            ys = (-16, 10, -12, 14, -9, 11); rs = (72, 84, 70, 86, 74, 82); tm = ta + .9; k = 0
            while tm < T2 - .1:
                dd = 2.0 + (k % 2) * .6
                out.append(f'tl.to({R},{{y:{ys[k % 6]},duration:{dd:.2f},ease:"sine.inOut"}},{tm:.3f});tl.to({RR},{{rotation:{rs[k % 6]},duration:{dd:.2f},ease:"sine.inOut",svgOrigin:"0 -30"}},{tm:.3f});'); tm += dd; k += 1
        elif kind == 'tumble':   # slow weightless somersault while drifting
            out.append(f'tl.fromTo({RR},{{rotation:0}},{{rotation:{360 * rm.get("turns", 1)},duration:{dur:.3f},ease:"none",svgOrigin:"0 -30",immediateRender:false}},{ta:.3f});')
            ys = (-14, 10, -10, 12); tm = ta; k = 0
            while tm < T2 - .1:
                dd = 2.0
                out.append(f'tl.to({R},{{y:{ys[k % 4]},duration:{dd:.2f},ease:"sine.inOut"}},{tm:.3f});'); tm += dd; k += 1
        elif kind == 'moonhop':   # low gravity: slow, very high hops, turning a little in the air
            per = 1.5; k = 0; tm = ta
            while tm < T2 - .2:
                out.append(f'tl.to({R},{{y:-70,duration:{per / 2:.2f},ease:"power1.out"}},{tm:.3f});tl.to({R},{{y:0,duration:{per / 2:.2f},ease:"power1.in"}},{tm + per / 2:.3f});tl.to({RR},{{rotation:{10 if k % 2 == 0 else -10},duration:{per / 2:.2f},ease:"power1.out",svgOrigin:"0 -30"}},{tm:.3f});tl.to({RR},{{rotation:0,duration:{per / 2:.2f},ease:"power1.in",svgOrigin:"0 -30"}},{tm + per / 2:.3f});'); tm += per; k += 1
        elif kind == 'roll':   # tumbling / rolling along (dragged, swept away): accelerates, the body turns exactly with the distance travelled
            deg = 360 * L / 283.0
            out[-1] = out[-1].replace('ease:"none"', 'ease:"power1.in"')
            out.append(f'tl.fromTo({RR},{{rotation:0}},{{rotation:{deg:.0f},duration:{dur:.3f},ease:"power1.in",svgOrigin:"0 -34",immediateRender:false}},{ta:.3f});')
        elif kind in ('run', 'walk'):   # hops along the ground: run = big quick hops leaning forward, walk = small steps
            hh, per = (24, .46) if kind == 'run' else (9, .62)
            out.append(f'tl.to({RR},{{rotation:{6 if kind == "run" else 0},duration:.3,svgOrigin:"0 0"}},{ta:.3f});')
            while tm < T2 - .1:
                out.append(f'tl.to({R},{{y:{-hh},duration:{per / 2:.2f},ease:"power2.out"}},{tm:.3f});tl.to({R},{{y:0,duration:{per / 2:.2f},ease:"power2.in"}},{tm + per / 2:.3f});'); tm += per
    # mouth follows the spoken words: closed = the mood's mouth; open = a big round "ahh" of the same width that hangs from the smile line, with a tongue
    talk = d.get('talk', not (d.get('ride') or d.get('kind') in ('ride', 'bg')))
    for k, (ws, we) in enumerate(words if talk else []):
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
