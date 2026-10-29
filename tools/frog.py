# -*- coding: utf-8 -*-
# Notebook frog (Miya's Note mascot) inside the video (owner decisions 2026-10-24 / 2026-10-25, guideline 7-2).
# Two roles:
#   CHALKBOARD scenes: the explainer. It stands bottom-left, talks (mouth follows the real word times), blinks and points at the row being
#     spoken (js(..., targets=...)); the arm turns only when the pointed row changes.
#   PICTURE scenes (plan.json frog_hint units): NO explainer standing beside the picture. A companion: it rides a moving object (drawn INSIDE
#     that picture group via inject(..., ride=id), so it moves and turns with it) or roams / acts in the background; the arm is
#     hidden unless the sidecar has points. tools/frog_place.py writes these sidecars (guideline 7-2).
# markup()  -> SVG group string to put INTO a picture svg (ids fg<tag>_*), or into an overlay svg for chalkboard scenes
# js()      -> GSAP lines (absolute timeline seconds) for that frog
# Sidecar key in art3/<uid>.json: "frog": {"x": 220, "y": 1040, "s": 2.4, "flip": 1, "delay": 0.35, ...}
#   x, y = feet position (picture coords; for "ride" the coordinates of the group before it moves), s = scale (82 units tall at s=1),
#   flip = -1 mirrors it, delay = seconds after the unit starts. `"frog": true` = defaults.
#   "ride": "<id of a picture group>"  the frog is injected into that group. Only use groups whose motion does not flip/fade/clip
#     (core swell|heartbeat|wobble|sway|glide|approach|drop|ping|tremble, path, slide, swing). Never flip, flicker, reveal, fade, fill, grow, edge.
#   "moods": [{"word": "...", "mood": "happy|surprised|curious|worried|proud|excited"}] (first entry without "word" = at the start),
#   "outfit": one of helmet goggles diver fore lab explorer scarf nightcap crown wizard pirate chef hardhat headphones knight doctor gradcap strawhat umbrella sunglasses partyhat detective (round 4) — ["helmet"] | ["goggles"] | ["diver"] (bubble space helmet / diving mask + snorkel / full diving suit with tank: use it in deep-water scenes),
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
    if 'fore' in names or 'fore_steps' in names:   # (miya 2026-10-26) Fore highlands outfit, simple and respectful, three parts so a scene can add them one by one (fore_steps: all hidden, act 'huts' shows them)
        op = ' opacity="0"' if 'fore_steps' in names else ''
        o += (f'<g id="{t}_ob"{op}><path d="M-36 -22 q36 14 74 0 l-3 4 q-34 12 -68 0z" fill="#7a5a30" stroke-width="3"/>'
              + ''.join(f'<path d="M{-33 + k * 7.6:.1f} -14 q-1 14 {-1 + (k % 3)} 18" fill="none" stroke="{["#5f8a3c", "#8a6a3c", "#6f9a44"][k % 3]}" stroke-width="5"/>' for k in range(9))
              + '</g>'
              f'<g id="{t}_ot"{op}><path d="M-30 -56 q28 22 60 44" fill="none" stroke="#b5442a" stroke-width="4"/>'
              '<path d="M-44 -22 q-4 -16 12 -20 q16 4 14 20 q-12 12 -26 0z" fill="#d9703a" stroke-width="3"/>'
              '<path d="M-42 -30 h22 M-41 -24 h22 M-34 -40 v22 M-27 -40 v24" fill="none" stroke="#7a2f20" stroke-width="1.6"/></g>'
              f'<g id="{t}_oh"{op}><path d="M-26 -86 q32 -16 64 0" fill="none" stroke="#b5442a" stroke-width="5"/>'
              '<ellipse cx="-2" cy="-100" rx="5" ry="15" transform="rotate(-18 -2 -100)" fill="#e8b838" stroke-width="2.6"/>'
              '<ellipse cx="10" cy="-104" rx="5" ry="16" fill="#c2452d" stroke-width="2.6"/>'
              '<ellipse cx="22" cy="-100" rx="5" ry="15" transform="rotate(18 22 -100)" fill="#2f8f5a" stroke-width="2.6"/></g>')
    if 'lab' in names:       # (round 3) white lab coat with a pocket and safety goggles on the forehead: laboratory / experiment scenes
        o += ('<path d="M-36 -18 q-2 -26 10 -34 l26 -2 l26 2 q12 8 10 34 q-36 8 -72 0z" fill="#f4f4f0" stroke-width="3.4"/><path d="M0 -52 v34" fill="none" stroke="#b9bcc4" stroke-width="2.2"/>'
              '<rect x="10" y="-36" width="14" height="10" rx="2" fill="none" stroke="#b9bcc4" stroke-width="2"/><path d="M-26 -84 q32 -14 64 0" fill="none" stroke="#5a6b8a" stroke-width="4"/>'
              '<rect x="-24" y="-96" width="22" height="12" rx="5" fill="#9fd8ff" fill-opacity=".5" stroke-width="3"/><rect x="14" y="-96" width="22" height="12" rx="5" fill="#9fd8ff" fill-opacity=".5" stroke-width="3"/>')
    if 'explorer' in names:  # (round 3) wide-brim explorer hat: expedition / jungle / desert / cave scenes
        o += ('<path d="M-44 -82 q50 -10 100 0 q-6 8 -50 8 q-44 0 -50 -8z" fill="#c9a060" stroke-width="3.2"/><path d="M-26 -84 q0 -26 32 -26 q32 0 32 26z" fill="#c9a060" stroke-width="3.2"/><path d="M-24 -90 h60" fill="none" stroke="#6b4a2a" stroke-width="5"/>')
    if 'scarf' in names:     # (round 3) red knitted scarf: cold / ice / freezing scenes
        o += ('<path d="M-30 -40 q36 14 70 0 q2 8 -2 10 q-34 10 -66 0 q-4 -4 -2 -10z" fill="#d9534f" stroke-width="3.2"/><path d="M26 -34 q10 14 4 34 q-8 2 -10 -2 q4 -16 -2 -28z" fill="#d9534f" stroke-width="3"/><path d="M-26 -36 h62 M-24 -31 h58" fill="none" stroke="#a83a36" stroke-width="1.6"/>')
    if 'nightcap' in names:  # (round 3) striped nightcap with a pompom: sleep / dream / night scenes
        o += ('<path d="M-26 -84 q10 -34 50 -26 q14 20 26 44 q-50 -10 -100 0 q6 -12 24 -18z" fill="#7a9ad9" stroke-width="3.2"/><path d="M-14 -96 q30 -8 44 12 M-6 -104 q26 -4 40 14" fill="none" stroke="#e8edf8" stroke-width="3"/><circle cx="52" cy="-62" r="8" fill="#e8edf8" stroke-width="2.6"/>')
    # ---- round 4 (2026-10-26, miya: more costumes ready for any script) — each sits on the head (top ≈ y -90, centre x 6) or on the body; one per unit ----
    if 'crown' in names:     # gold crown: kings / queens / empires / pharaohs
        o += '<path d="M-24 -86 l0 -26 l14 12 l16 -22 l16 22 l14 -12 l0 26z" fill="#f2c94c" stroke-width="3.2"/><circle cx="6" cy="-122" r="4" fill="#e8605a" stroke-width="2"/><circle cx="-10" cy="-104" r="3" fill="#5fa8e8" stroke-width="1.8"/><circle cx="22" cy="-104" r="3" fill="#5fa8e8" stroke-width="1.8"/>'
    if 'wizard' in names:    # tall pointed hat with a star: magic / myths / legends
        o += '<path d="M-40 -84 q46 -10 92 0 q-6 8 -46 8 q-40 0 -46 -8z" fill="#5b4a9a" stroke-width="3.2"/><path d="M-22 -86 q14 -40 34 -74 q10 36 24 74z" fill="#5b4a9a" stroke-width="3.2"/><path d="M4 -118 l3 7 l7 1 l-5 5 l1 7 l-6 -4 l-6 4 l1 -7 l-5 -5 l7 -1z" fill="#f2c94c" stroke="none"/>'
    if 'pirate' in names:    # tricorn hat + eye patch: pirates / treasure / sailing
        o += '<path d="M-44 -86 q50 -28 100 0 q-10 -4 -50 -4 q-40 0 -50 4z" fill="#1f2430" stroke-width="3.2"/><path d="M-26 -88 q10 -22 32 -22 q22 0 32 22z" fill="#1f2430" stroke-width="3.2"/><path d="M-2 -100 q8 -6 16 0 M2 -96 l4 -4 l4 4" fill="none" stroke="#fff" stroke-width="2.4"/><path d="M-30 -74 q28 -14 64 -4" fill="none" stroke-width="3"/><circle cx="22" cy="-66" r="13" fill="#1f2430" stroke-width="3.2"/>'
    if 'chef' in names:      # white toque: cooking / recipes / food
        o += '<path d="M-26 -84 q-14 -40 22 -36 q6 -14 24 -10 q20 -8 24 12 q24 -8 12 34z" fill="#f7f7f2" stroke-width="3.2"/><rect x="-26" y="-90" width="76" height="10" rx="4" fill="#f7f7f2" stroke-width="3"/>'
    if 'hardhat' in names:   # yellow hard hat: building / engineering / machines
        o += '<path d="M-28 -86 q0 -30 34 -30 q34 0 34 30z" fill="#f2c94c" stroke-width="3.2"/><rect x="-40" y="-90" width="92" height="9" rx="4" fill="#f2c94c" stroke-width="3"/><path d="M0 -112 h12" stroke="#c99a1a" stroke-width="3"/>'
    if 'headphones' in names:   # headphones: music / sound / signals
        o += '<path d="M-26 -74 q-2 -40 32 -42 q34 2 32 42" fill="none" stroke="#2b2f3a" stroke-width="6"/><rect x="-36" y="-80" width="14" height="24" rx="6" fill="#e8605a" stroke="#2b2f3a" stroke-width="3"/><rect x="34" y="-80" width="14" height="24" rx="6" fill="#e8605a" stroke="#2b2f3a" stroke-width="3"/>'
    if 'knight' in names:    # knight helmet with a plume: battles / castles / medieval
        o += '<path d="M-28 -84 q0 -34 34 -34 q34 0 34 34z" fill="#9aa3ad" stroke-width="3.2"/><path d="M-26 -84 h64 l-4 16 q-28 6 -56 0z" fill="#9aa3ad" stroke-width="3"/><path d="M-18 -78 h48" stroke="#2b2f3a" stroke-width="2.4"/><path d="M6 -118 q-22 -18 -36 -4 q14 -2 20 8" fill="#e8605a" stroke-width="2.6"/>'
    if 'doctor' in names:    # white coat + head mirror + stethoscope: medicine / disease / hospitals
        o += ('<path d="M-36 -18 q-2 -26 10 -34 l26 -2 l26 2 q12 8 10 34 q-36 8 -72 0z" fill="#f4f4f0" stroke-width="3.4"/><path d="M-6 -52 q-12 14 -6 30 q12 10 24 0 q6 -16 -6 -30" fill="none" stroke="#2b2f3a" stroke-width="3"/><circle cx="18" cy="-18" r="6" fill="#9aa3ad" stroke-width="2.4"/>'
              '<path d="M-26 -86 q32 -12 64 0" fill="none" stroke="#6a7a9a" stroke-width="4"/><circle cx="6" cy="-98" r="9" fill="#e8f3ff" stroke-width="2.6"/><circle cx="6" cy="-98" r="4" fill="#6a7a9a" stroke="none"/>')
    if 'gradcap' in names:   # mortarboard with a tassel: school / learning / exams
        o += '<path d="M-30 -84 q36 -8 72 0 q-6 8 -36 8 q-30 0 -36 -8z" fill="#2b2f3a" stroke-width="3"/><path d="M-50 -96 l56 -16 l56 16 l-56 14z" fill="#2b2f3a" stroke-width="3.2"/><path d="M50 -94 v22" stroke="#f2c94c" stroke-width="3"/><circle cx="50" cy="-70" r="4" fill="#f2c94c" stroke="none"/>'
    if 'strawhat' in names:  # straw hat with a ribbon: farms / harvests / summer fields
        o += '<path d="M-54 -84 q60 -14 120 0 q-8 10 -60 10 q-52 0 -60 -10z" fill="#e8c97a" stroke-width="3.2"/><path d="M-26 -86 q4 -26 32 -26 q28 0 32 26z" fill="#e8c97a" stroke-width="3.2"/><path d="M-24 -92 h60" stroke="#c2452d" stroke-width="5"/>'
    if 'umbrella' in names:  # small umbrella held over the head in the left hand: rain / storms
        o += f'<g id="{t}_um"><path d="M-38 -22 l-10 -96" stroke-width="4"/><path d="M-110 -112 q62 -44 124 0 q-15 -8 -31 0 q-15 -8 -31 0 q-15 -8 -31 0 q-15 -8 -31 0z" fill="#e8605a" stroke-width="3.2"/></g>'
    if 'sunglasses' in names:   # dark shades: sun / heat / beaches / cool moments
        o += '<path d="M-30 -70 h70" stroke-width="3"/><rect x="-26" y="-78" width="30" height="20" rx="8" fill="#1f2430" stroke-width="3"/><rect x="8" y="-78" width="30" height="20" rx="8" fill="#1f2430" stroke-width="3"/><path d="M-20 -74 h10 M14 -74 h10" stroke="#fff" stroke-width="2" opacity=".6"/>'
    if 'partyhat' in names:  # striped cone hat with a pompom: parties / celebrations / anniversaries
        o += '<path d="M-14 -86 l20 -56 l20 56z" fill="#5fa8e8" stroke-width="3.2"/><path d="M-6 -108 h24 M-10 -96 h32" stroke="#f2c94c" stroke-width="4"/><circle cx="6" cy="-144" r="6" fill="#e8605a" stroke-width="2.4"/>'
    if 'detective' in names:   # deerstalker cap (the magnifier is the "magnify" act): clues / investigations / evidence
        o += '<path d="M-44 -86 q50 -8 100 0 q-6 6 -50 6 q-44 0 -50 -6z" fill="#a67c52" stroke-width="3"/><path d="M-26 -86 q4 -28 32 -28 q28 0 32 28z" fill="#a67c52" stroke-width="3.2"/><path d="M-16 -92 l12 -14 l12 14 M10 -92 l12 -14 l12 14" fill="none" stroke="#6b4a2a" stroke-width="2"/>'
    for nm_ in names:        # round 4b (2026-10-26, miya: 50 costumes): the data-driven ones
        if nm_ in OUTFITS2: o += OUTFITS2[nm_].replace('{t}', t)
    if 'helmet' in names:    # bubble helmet like the thumbnails
        o += (f'<circle cx="6" cy="-58" r="46" fill="#cfe9ff" fill-opacity=".14" stroke="#e6f1fb" stroke-width="3.4"/><path d="M-26 -84 q10 -16 28 -20" fill="none" stroke="#fff" stroke-width="4" stroke-opacity=".7"/>'
              f'<ellipse cx="6" cy="-14" rx="42" ry="9" fill="#e6f1fb" fill-opacity=".55" stroke="#e6f1fb" stroke-width="3"/>')
    return o


# ---- round 4b (2026-10-26, miya: 50 costumes ready for any script). Head top ≈ y -90, head centre x 6, body y -60..0, hands at (±50, 0). ----
OUTFITS2 = {
 'tophat': '<rect x="-30" y="-88" width="72" height="8" rx="3" fill="#1f2430" stroke-width="3"/><rect x="-18" y="-134" width="48" height="48" rx="4" fill="#1f2430" stroke-width="3"/><rect x="-18" y="-100" width="48" height="8" fill="#c2452d" stroke="none"/>',
 'beret': '<path d="M-34 -84 q-6 -28 40 -32 q42 0 36 30 q-36 -10 -76 2z" fill="#c2452d" stroke-width="3.2"/><path d="M2 -116 v-8" stroke-width="3"/>',
 'cowboy': '<path d="M-56 -84 q10 -16 24 -10 q38 -6 76 0 q14 -6 24 10 q-20 10 -62 8 q-42 2 -62 -8z" fill="#a67c52" stroke-width="3.2"/><path d="M-22 -88 q6 -30 28 -30 q22 0 28 30z" fill="#a67c52" stroke-width="3.2"/><path d="M-20 -92 h52" stroke="#6b4a2a" stroke-width="4"/>',
 'bandana': '<path d="M-30 -84 q36 -14 72 0 l-4 10 q-32 -8 -64 0z" fill="#c2452d" stroke-width="3"/><path d="M40 -80 l20 10 l-6 8 l-14 -10" fill="#c2452d" stroke-width="2.6"/><path d="M-20 -82 h8 M0 -84 h8 M20 -82 h8" stroke="#fff" stroke-width="2" opacity=".7"/>',
 'flowercrown': '<path d="M-30 -86 q36 -10 72 0" fill="none" stroke="#5f8a3c" stroke-width="5"/>' + ''.join(f'<circle cx="{-24 + k * 16}" cy="{-92 - (k % 2) * 4}" r="6" fill="{["#e8605a", "#f2c94c", "#5fa8e8", "#e88ac4"][k % 4]}" stroke-width="2"/><circle cx="{-24 + k * 16}" cy="{-92 - (k % 2) * 4}" r="2" fill="#fff" stroke="none"/>' for k in range(5)),
 'alien': '<path d="M-12 -88 q-10 -26 -20 -40 M24 -88 q10 -26 20 -40" fill="none" stroke-width="4"/><circle cx="-32" cy="-130" r="7" fill="#7be07b" stroke-width="2.6"/><circle cx="44" cy="-130" r="7" fill="#7be07b" stroke-width="2.6"/>',
 'bunny': '<path d="M-20 -86 q-12 -50 4 -70 q14 20 8 70z" fill="#f4f4f0" stroke-width="3"/><path d="M-12 -92 q-6 -34 2 -50 q6 16 4 50z" fill="#f4b6c2" stroke="none"/><path d="M20 -86 q-4 -50 12 -70 q14 20 2 70z" fill="#f4f4f0" stroke-width="3"/><path d="M26 -92 q0 -34 8 -50 q6 16 -2 50z" fill="#f4b6c2" stroke="none"/>',
 'santa': '<path d="M-28 -84 q10 -40 54 -30 q18 18 30 40 q-50 -8 -100 0 q4 -8 16 -10z" fill="#d9302c" stroke-width="3.2"/><rect x="-32" y="-92" width="80" height="12" rx="6" fill="#fff" stroke-width="2.8"/><circle cx="58" cy="-72" r="9" fill="#fff" stroke-width="2.6"/>',
 'bowtie': '<path d="M-8 -30 l-16 -8 v16z M20 -30 l16 -8 v16z" fill="#c2452d" stroke-width="2.6"/><circle cx="6" cy="-30" r="4" fill="#c2452d" stroke-width="2"/>',
 'cape': '<path d="M-36 -34 q-24 30 -26 46 q36 -2 36 -2 l-4 -40z M48 -34 q24 30 26 46 q-36 -2 -36 -2 l4 -40z" fill="#c2452d" stroke-width="3"/><path d="M-30 -36 q36 10 72 0" fill="none" stroke="#f2c94c" stroke-width="4"/>',
 'backpack': '<rect x="-58" y="-56" width="22" height="40" rx="8" fill="#5fa8e8" stroke-width="3"/><rect x="-54" y="-50" width="14" height="12" rx="3" fill="#2f6f9a" stroke-width="2"/><path d="M-36 -50 q14 -4 20 -2 M-36 -26 q14 -4 20 -2" fill="none" stroke="#2f6f9a" stroke-width="3"/>',
 'lifevest': '<path d="M-32 -46 q0 -8 10 -10 l10 -2 v40 l-16 2 q-6 -2 -6 -10z M44 -46 q0 -8 -10 -10 l-10 -2 v40 l16 2 q6 -2 6 -10z" fill="#ff8c42" stroke-width="3"/><path d="M-26 -36 h18 M20 -36 h18" stroke="#fff" stroke-width="3"/>',
 'raincoat': '<path d="M-28 -84 q10 -22 34 -22 q24 0 34 22 l6 10 q-40 -6 -80 0z" fill="#f2c94c" stroke-width="3.2"/><path d="M-34 -18 q-1 -22 6 -28 q36 8 72 0 q6 8 4 30 q-40 6 -82 -2z" fill="#f2c94c" stroke-width="3.4"/><path d="M6 -46 v30" stroke="#c99a1a" stroke-width="2.2"/>',
 'beanie': '<path d="M-28 -84 q4 -36 34 -36 q30 0 34 36z" fill="#5fa8e8" stroke-width="3.2"/><rect x="-30" y="-90" width="76" height="12" rx="4" fill="#2f6f9a" stroke-width="2.8"/><circle cx="6" cy="-122" r="7" fill="#f4f4f0" stroke-width="2.6"/>',
 'halo': '<ellipse cx="6" cy="-120" rx="30" ry="8" fill="none" stroke="#f2c94c" stroke-width="5"/>',
 'ghost': '<path d="M-44 -96 q0 -46 50 -46 q50 0 50 46 v70 q-10 -8 -20 0 q-10 8 -20 0 q-10 8 -20 0 q-10 8 -20 0 q-10 8 -20 0z" fill="#f4f4f0" fill-opacity=".92" stroke-width="3.2"/><circle cx="-8" cy="-72" r="6" fill="#1d2b1c" stroke="none"/><circle cx="22" cy="-72" r="6" fill="#1d2b1c" stroke="none"/><ellipse cx="7" cy="-50" rx="6" ry="9" fill="#1d2b1c" stroke="none"/>',
 'viking': '<path d="M-28 -84 q0 -32 34 -32 q34 0 34 32z" fill="#9aa3ad" stroke-width="3.2"/><rect x="-30" y="-90" width="76" height="9" rx="3" fill="#6b4a2a" stroke-width="2.6"/><path d="M-26 -94 q-24 -10 -22 -40 q14 14 26 24z M38 -94 q24 -10 22 -40 q-14 14 -26 24z" fill="#f4e6c8" stroke-width="3"/>',
 'roman': '<path d="M-28 -84 q0 -32 34 -32 q34 0 34 32z" fill="#f2c94c" stroke-width="3.2"/><path d="M-26 -84 h64 l-4 10 h-56z" fill="#f2c94c" stroke-width="2.8"/><path d="M-20 -112 q26 -30 52 0 l-6 6 q-20 -22 -40 0z" fill="#c2452d" stroke-width="2.8"/>',
 'samurai': '<path d="M-30 -84 q4 -30 36 -30 q32 0 36 30z" fill="#2b2f3a" stroke-width="3.2"/><path d="M-36 -82 h84 l-8 14 h-68z" fill="#2b2f3a" stroke-width="2.8"/><path d="M6 -114 l-20 -22 M6 -114 l20 -22 M-8 -114 h28" fill="none" stroke="#f2c94c" stroke-width="4"/>',
 'headlamp': '<path d="M-28 -84 q0 -30 34 -30 q34 0 34 30z" fill="#f2c94c" stroke-width="3.2"/><rect x="-30" y="-90" width="76" height="9" rx="3" fill="#2b2f3a" stroke-width="2.6"/><circle cx="6" cy="-100" r="9" fill="#fff8c4" stroke-width="2.6"/><path d="M14 -104 l40 -14 M14 -96 l44 4 M12 -100 l44 -5" stroke="#fff8c4" stroke-width="3" opacity=".6"/>',
 'firefighter': '<path d="M-30 -84 q0 -32 36 -32 q36 0 36 32z" fill="#d9302c" stroke-width="3.2"/><path d="M-44 -84 q50 -8 100 0 q-6 8 -50 8 q-44 0 -50 -8z" fill="#d9302c" stroke-width="3"/><rect x="-6" y="-106" width="24" height="14" rx="3" fill="#f2c94c" stroke-width="2.4"/>',
 'police': '<path d="M-26 -86 q0 -24 32 -24 q32 0 32 24z" fill="#2b3a6b" stroke-width="3.2"/><rect x="-30" y="-90" width="72" height="9" rx="3" fill="#1f2430" stroke-width="2.6"/><path d="M-30 -82 q36 4 72 0 l2 8 q-38 4 -76 0z" fill="#1f2430" stroke-width="2.4"/><circle cx="6" cy="-100" r="6" fill="#f2c94c" stroke-width="2"/>',
 'aviator': '<path d="M-28 -84 q0 -30 34 -30 q34 0 34 30z" fill="#6b4a2a" stroke-width="3.2"/><path d="M-28 -84 q-6 10 -2 20 M40 -84 q6 10 2 20" fill="none" stroke="#6b4a2a" stroke-width="7"/><rect x="-28" y="-98" width="30" height="16" rx="7" fill="#9fd8ff" fill-opacity=".6" stroke-width="3"/><rect x="10" y="-98" width="30" height="16" rx="7" fill="#9fd8ff" fill-opacity=".6" stroke-width="3"/>',
 'monocle': '<circle cx="22" cy="-66" r="17" fill="#9fd8ff" fill-opacity=".3" stroke="#f2c94c" stroke-width="4"/><path d="M36 -54 q10 20 4 40" fill="none" stroke="#f2c94c" stroke-width="2.4"/>',
 'glasses': '<rect x="-27" y="-78" width="32" height="24" rx="8" fill="#9fd8ff" fill-opacity=".25" stroke-width="3.2"/><rect x="7" y="-78" width="32" height="24" rx="8" fill="#9fd8ff" fill-opacity=".25" stroke-width="3.2"/><path d="M5 -68 h2 M-27 -70 q-8 2 -10 6 M39 -70 q8 2 10 6" stroke-width="3"/>',
 'medal': '<path d="M-10 -56 l12 26 l14 -26" fill="none" stroke="#c2452d" stroke-width="5"/><circle cx="3" cy="-24" r="11" fill="#f2c94c" stroke-width="3"/><path d="M3 -30 l2 5 l5 0 l-4 3 l2 5 l-5 -3 l-5 3 l2 -5 l-4 -3 l5 0z" fill="#c99a1a" stroke="none"/>',
 'laurel': '<path d="M-30 -84 q36 -10 72 0" fill="none" stroke="#5f8a3c" stroke-width="4"/>' + ''.join(f'<ellipse cx="{-26 + k * 10}" cy="{-92 - abs(k - 3) * -1.5}" rx="4" ry="8" transform="rotate({-50 + k * 16} {-26 + k * 10} {-92})" fill="#6f9a44" stroke-width="1.6"/>' for k in range(8)),
 'propcap': '<path d="M-28 -84 q0 -30 34 -30 q34 0 34 30z" fill="#5fa8e8" stroke-width="3.2"/><path d="M-10 -84 q16 -30 16 -30 q0 0 16 30" fill="#e8605a" stroke="none"/><path d="M6 -114 v-10" stroke-width="3"/><g id="{t}_pp"><path d="M-18 -126 h48" stroke="#f2c94c" stroke-width="5"/></g>',
 'headband': '<path d="M-30 -84 q36 -10 72 0 l0 10 q-36 -8 -72 0z" fill="#c2452d" stroke-width="3"/><path d="M-20 -80 h52" stroke="#fff" stroke-width="2.4"/>',
 'vr': '<rect x="-34" y="-84" width="80" height="34" rx="10" fill="#2b2f3a" stroke-width="3.2"/><rect x="-26" y="-78" width="64" height="20" rx="6" fill="#5fa8e8" fill-opacity=".8" stroke="none"/><path d="M-34 -70 q-8 0 -8 8 M46 -70 q8 0 8 8" fill="none" stroke-width="4"/>',
 'tinfoil': '<path d="M-26 -86 l10 -30 l12 12 l10 -36 l10 36 l12 -12 l10 30z" fill="#c9ced6" stroke-width="3"/>',
 'bandage': '<path d="M-30 -74 q36 -10 72 0 l0 12 q-36 -8 -72 0z" fill="#f4f4f0" stroke-width="2.8"/><path d="M-22 -70 l8 6 M-6 -72 l8 6 M12 -72 l8 6 M30 -70 l6 4" stroke="#c9ced6" stroke-width="2"/>',
 'dino': '<path d="M-34 -86 q-2 -40 40 -40 q42 0 40 40 q-40 -10 -80 0z" fill="#5f8a3c" stroke-width="3.2"/><path d="M-22 -100 l8 -16 l8 16 M-4 -108 l10 -18 l10 18 M18 -102 l8 -14 l8 14" fill="#f2c94c" stroke-width="2.4"/><path d="M-32 -88 l6 10 l6 -10 M34 -88 l6 10 l6 -10" fill="#fff" stroke-width="2.2"/>',
 'shark': '<path d="M-30 -86 q36 -8 72 0 l-6 8 q-30 -6 -60 0z" fill="#6a7a9a" stroke-width="3"/><path d="M-6 -90 q10 -50 36 -40 q-10 20 -8 40z" fill="#6a7a9a" stroke-width="3.2"/>',
 'bee': '<path d="M-8 -88 q-10 -20 -18 -28 M20 -88 q10 -20 18 -28" fill="none" stroke-width="3.6"/><circle cx="-26" cy="-118" r="6" fill="#1f2430" stroke="none"/><circle cx="38" cy="-118" r="6" fill="#1f2430" stroke="none"/><path d="M-32 -44 h74 M-33 -30 h76" stroke="#1f2430" stroke-width="7" opacity=".8"/><path d="M-32 -44 h74 M-33 -30 h76" stroke="#f2c94c" stroke-width="3"/>',
 'clown': '<circle cx="6" cy="-52" r="10" fill="#e8605a" stroke-width="3"/><path d="M-34 -84 q-20 -4 -22 10 q14 12 26 0z M46 -84 q20 -4 22 10 q-14 12 -26 0z" fill="#ff8c42" stroke-width="2.6"/>',
 'mustache': '<path d="M6 -48 q-8 -10 -18 -6 q-8 4 -10 10 q12 2 28 -4 q16 6 28 4 q-2 -6 -10 -10 q-10 -4 -18 6z" fill="#1d2b1c" stroke="none"/>',
 'earmuffs': '<path d="M-26 -74 q-2 -36 32 -38 q34 2 32 38" fill="none" stroke="#c2452d" stroke-width="5"/><circle cx="-30" cy="-66" r="12" fill="#e8605a" stroke-width="3"/><circle cx="42" cy="-66" r="12" fill="#e8605a" stroke-width="3"/>',
 'turtle': '<path d="M-68 -52 q4 -30 34 -26 q12 10 6 44 q-26 6 -38 -4 q-6 -6 -2 -14z" fill="#5f8a3c" stroke-width="3.2"/><path d="M-62 -42 h22 M-60 -32 h22 M-52 -58 v34" fill="none" stroke="#3f6a2c" stroke-width="2.4"/><path d="M-36 -46 q10 -2 10 6 M-36 -26 q10 -2 10 6" fill="none" stroke="#3f6a2c" stroke-width="3"/>',
 'wings': '<path d="M-38 -44 q-50 -30 -60 -4 q22 2 30 14 q-26 4 -30 20 q30 -4 46 -6 q-16 6 -18 18 q26 -6 36 -18z" fill="#fff" fill-opacity=".9" stroke-width="2.8"/><path d="M50 -44 q50 -30 60 -4 q-22 2 -30 14 q26 4 30 20 q-30 -4 -46 -6 q16 6 18 18 q-26 -6 -36 -18z" fill="#fff" fill-opacity=".9" stroke-width="2.8"/>',
 'crownleaf': '<path d="M-30 -86 q36 -12 72 0" fill="none" stroke="#a67c52" stroke-width="4"/>' + ''.join(f'<path d="M{-22 + k * 12} -90 q4 -14 8 -2 q-4 6 -8 2z" fill="#c2452d" stroke-width="1.6"/>' for k in range(5)),
}


# ---- round 4b (2026-10-26): 12 data-driven acts. body = (from, to, period) tween on #<t>_ac (yoyo); ra / la = arm angles (deg); prop = part id to show; mood; pup = pupil cy;
# mouth = open-mouth ry; mirror = flip rotation/x with the facing side; sweat / spiral = extra loops. Words that choose them: tools/frog_place.py ACT_WORDS2. ----
SIMPLE_ACTS = {
 'stretch':  dict(body=({'scaleY': 1.0, 'y': 0}, {'scaleY': 1.07, 'y': -4}, 1.6), ra=-165, la=165, mood='sleepy', mouth=9),          # morning / waking / a new day: arms up, long stretch
 'shrug':    dict(body=({'rotation': -3, 'y': 0}, {'rotation': 3, 'y': -3}, 1.4), ra=-70, la=70, mood='worried', mirror=True),            # nobody knows / uncertain: palms up, shoulders lift
 'bow':      dict(body=({'rotation': 0}, {'rotation': 22}, 2.2), ra=-30, la=30, mood='proud', mirror=True),                              # thanks / respect / honour: bends forward and back
 'nervous':  dict(body=({'x': -2}, {'x': 2}, .12), ra=-162, mood='worried', sweat=True),                                                 # pressure / danger ahead / deadline: wipes the brow, sweat drops
 'flex':     dict(body=({'scaleX': 1.0, 'y': 0}, {'scaleX': 1.05, 'y': -3}, .8), ra=-130, la=130, mood='proud'),                         # strength / power / muscle: both arms bent up
 'balance':  dict(body=({'rotation': -9}, {'rotation': 9}, 1.8), ra=-90, la=90, mood='squint'),                                          # tightrope / careful / on the edge: arms out, slow tilt
 'listen':   dict(body=({'rotation': 0}, {'rotation': 7}, 2.0), ra=-136, mood='curious', pup=-64, mirror=True),                          # hear / whisper / signal: hand cupped at the ear, leans toward it
 'search':   dict(body=({'rotation': -6, 'x': -4}, {'rotation': 6, 'x': 4}, 1.6), ra=-166, mood='squint', pup=-70),                      # lost / missing / where: hand shading the eyes, turns left and right
 'yawn':     dict(body=({'scaleY': 1.0}, {'scaleY': 1.04}, 2.4), ra=160, mood='sleepy', mouth=11, pup=-64),                             # tired / long night: big open mouth, hand toward it
 'write':    dict(body=({'rotation': 2, 'y': 0}, {'rotation': 4, 'y': 1}, .5), ra=-40, prop='pc', mood='curious', pup=-62, mirror=True),  # notes / calculations / writing: pencil scribbles
 'wish':     dict(body=({'rotation': -2}, {'rotation': 2}, 2.6), ra=142, la=-137, mood='love', pup=-70, mirror=True),                      # hope / wish / dream: hands together, eyes up
 'faint':    dict(body=({'rotation': 0, 'y': 0}, {'rotation': -70, 'y': 6}, 3.0), ra=-20, la=20, mood='dizzy', spiral=True, mirror=True),  # shock / overwhelmed / exhausted: keels over slowly, swirl eyes
}


MOODS = {   # brows (left d, right d, opacity), pupil offset (dx, dy, r), mouth path + fill, lid height (eyes squint)
    'happy':     dict(bl='M-24 -84 q12 -6 24 0', br='M10 -84 q12 -6 24 0', bo=0, pup=(0, 0, 5), sm='M-8 -44 q14 12 28 0', fill='none', lid=0),
    'surprised': dict(bl='M-24 -90 q12 -8 24 0', br='M10 -90 q12 -8 24 0', bo=1, pup=(0, 0, 3.4), sm='M0 -47 q6 -6 12 0 q2 11 -6 11 q-8 0 -6 -11z', fill='#7a2f2f', lid=0),
    'curious':   dict(bl='M-24 -82 q12 0 24 2', br='M10 -92 q12 -8 24 -2', bo=1, pup=(3, -4, 5), sm='M-8 -42 q14 7 28 -5', fill='none', lid=0),
    'worried':   dict(bl='M-24 -80 q12 -2 24 -8', br='M10 -88 q12 6 24 8', bo=1, pup=(0, 2, 5), sm='M-6 -38 q12 -9 24 0', fill='none', lid=0),
    'proud':     dict(bl='M-24 -84 q12 -6 24 0', br='M10 -84 q12 -6 24 0', bo=0, pup=(0, 1, 5), sm='M-10 -47 q16 20 32 0', fill='none', lid=9),
    'sad':       dict(bl='M-24 -76 q12 -4 24 -12', br='M10 -88 q12 8 24 12', bo=1, pup=(0, 3, 6), sm='M-8 -36 q14 -10 28 0', fill='none', lid=0),   # miya 2026-10-26: sad / pleading face (caged, lonely): brows slanting up in the middle, mouth turned down, pupils looking down
    'scared':    dict(bl='M-24 -80 q12 -2 24 -9', br='M10 -89 q12 7 24 9', bo=1, pup=(0, 1, 3), sm='M-9 -39 q4.5 -7 9 0 q4.5 7 9 0 q4.5 -7 9 0', fill='none', lid=0),
    'dizzy_old': dict(bl='M-24 -80 q12 -2 24 -8', br='M10 -88 q12 6 24 8', bo=1, pup=(0, 0, 2.2), sm='M-9 -40 q4.5 -6 9 0 q4.5 6 9 0 q4.5 -6 9 0', fill='none', lid=5),   # miya 2026-10-26: woozy face while circling a black hole ring: tiny pupils, wavy mouth, half lids
    'squint':    dict(bl='M-24 -78 q12 -6 24 -2', br='M10 -80 q12 4 24 8', bo=1, pup=(0, 0, 4), sm='M-10 -47 q16 24 32 0z', fill='#7a2f2f', lid=11),
    'sleepy':    dict(bl='M-24 -80 q12 2 24 -2', br='M10 -82 q12 -2 24 2', bo=1, pup=(0, 3, 4.5), sm='M-6 -42 q8 3 16 0', fill='none', lid=14),
    'dizzy':     dict(bl='M-24 -78 q12 4 24 -4', br='M10 -80 q12 -4 24 4', bo=1, pup=(0, 0, 0.1), sm='M-10 -44 q4 -7 8 0 q4 7 8 0 q4 -7 8 0 q4 7 8 0', fill='none', lid=0),   # swirl eyes (the _sp spirals cover the pupils), wobbly mouth (2026-10-26 miya: overheated frog)
    'excited':   dict(bl='M-24 -90 q12 -8 24 0', br='M10 -90 q12 -8 24 0', bo=1, pup=(0, -1, 5.6), sm='M-10 -47 q16 24 32 0z', fill='#7a2f2f', lid=0),
    # 2026-10-26 round 3 (guideline 7-2 F): love = soft brows, big pupils, wide smile (beautiful / favourite); shock = brows high, tiny pupils, round open mouth (suddenly / unbelievable); angry = brows down toward the middle, flat mouth (war / cruel / unfair)
    'love':      dict(bl='M-24 -86 q12 -8 24 -2', br='M10 -88 q12 -6 24 2', bo=1, pup=(0, 0, 6.2), sm='M-10 -46 q16 18 32 0', fill='none', lid=4),
    'shock':     dict(bl='M-24 -94 q12 -8 24 0', br='M10 -94 q12 -8 24 0', bo=1, pup=(0, 0, 2.6), sm='M-2 -48 q8 -8 16 0 q4 14 -8 14 q-12 0 -8 -14z', fill='#7a2f2f', lid=0),
    'angry':     dict(bl='M-24 -90 q12 4 24 10', br='M10 -80 q12 -6 24 -10', bo=1, pup=(0, 0, 4.4), sm='M-8 -42 h28', fill='none', lid=6),
    # 2026-10-26 round 4c (miya: more expressions, picked per script + picture, guideline 7-2 F). Optional keys: lidl / lidr = per-eye lid height
    # (a wink / a wince), ex = extra parts shown with the face ('fl' blush, 'tg' tongue, 'st' star eyes, 'th' teeth, 'te' tears, 'sw' sweat, 'sp' swirls),
    # mouth = open-mouth height (the round mouth replaces the smile line).
    'wink':      dict(bl='M-24 -84 q12 -6 24 0', br='M10 -88 q12 -8 24 -2', bo=1, pup=(2, 0, 5), sm='M-8 -44 q14 12 28 -4', fill='none', lid=0, lidl=27),          # a secret / a trick / between us
    'laugh':     dict(bl='M-24 -88 q12 -8 24 0', br='M10 -88 q12 -8 24 0', bo=1, pup=(0, 0, 5), sm='M-10 -47 q16 24 32 0z', fill='#7a2f2f', lid=27, ex=('fl',)),  # funny / joke / hilarious: eyes shut, big open mouth, blush
    'grin':      dict(bl='M-24 -86 q12 -6 24 0', br='M10 -86 q12 -6 24 0', bo=1, pup=(0, 0, 5), sm='M-12 -46 q18 22 36 0z', fill='#7a2f2f', lid=2, ex=('th',)),     # delicious / won / success: wide grin with teeth
    'pout':      dict(bl='M-24 -82 q12 2 24 4', br='M10 -78 q12 -4 24 -4', bo=1, pup=(0, 1, 5), sm='M0 -42 q6 -5 12 0 q-6 5 -12 0z', fill='#7a2f2f', lid=4, ex=('fl',)),  # unfair / refused / no way: small puckered mouth, puffed cheeks
    'bored':     dict(bl='M-24 -82 q12 0 24 0', br='M10 -82 q12 0 24 0', bo=1, pup=(4, 1, 4.6), sm='M-6 -42 h24', fill='none', lid=13),                              # waiting / nothing happens / centuries: half lids, flat mouth, eyes aside
    'confused':  dict(bl='M-24 -80 q12 4 24 2', br='M10 -94 q12 -8 24 0', bo=1, pup=(-3, -1, 5), sm='M-10 -42 q5 -6 10 0 q5 6 10 0 q5 -6 10 0', fill='none', lid=0),  # strange / odd / puzzle: one brow up, wavy mouth
    'determined': dict(bl='M-24 -92 q12 6 24 8', br='M10 -84 q12 -6 24 -8', bo=1, pup=(0, -1, 5), sm='M-8 -44 q14 8 28 0', fill='none', lid=5),                    # mission / must / struggle on: brows down, tight smile
    'smug':      dict(bl='M-24 -84 q12 -4 24 0', br='M10 -90 q12 -8 24 -2', bo=1, pup=(3, 0, 4.8), sm='M-6 -44 q12 6 24 -6', fill='none', lid=10),                   # of course / obviously / easy: half lids, lopsided smile
    'chilly':    dict(bl='M-24 -86 q12 -6 24 -2', br='M10 -88 q12 -6 24 2', bo=1, pup=(0, 1, 5), sm='M-10 -42 q3.5 -5 7 0 q3.5 5 7 0 q3.5 -5 7 0 q3.5 5 7 0', fill='none', lid=0, ex=('fl',)),  # cold / frost / ice: chattering wavy mouth, red cheeks
    'hot':       dict(bl='M-24 -82 q12 -2 24 -6', br='M10 -88 q12 6 24 6', bo=1, pup=(0, 2, 4.6), sm='M-8 -44 q14 10 28 0', fill='none', lid=8, ex=('fl', 'sw'), tongue=6),  # heat / scorching / sun: tongue out, sweat, flushed
    'tearful':   dict(bl='M-24 -76 q12 -4 24 -12', br='M10 -88 q12 8 24 12', bo=1, pup=(0, 3, 6), sm='M-8 -36 q14 -10 28 0', fill='none', lid=0, ex=('te',)),         # goodbye / farewell / lost: sad face with tears
    'queasy':    dict(bl='M-24 -80 q12 -2 24 -8', br='M10 -88 q12 6 24 8', bo=1, pup=(0, 2, 4.4), sm='M-10 -42 q5 6 10 0 q5 -6 10 0 q5 6 10 0', fill='none', lid=9, ex=('fl',)),  # rot / stench / slime: green-ish wobble (blush part recoloured by 'sick')
    'suspicious': dict(bl='M-24 -84 q12 -2 24 2', br='M10 -82 q12 0 24 -2', bo=1, pup=(5, 0, 4.4), sm='M-6 -42 h22', fill='none', lid=7, lidr=12),                   # lie / fake / hidden / trust: narrowed uneven eyes, eyes to the side
    'awe':       dict(bl='M-24 -92 q12 -8 24 -2', br='M10 -94 q12 -8 24 2', bo=1, pup=(0, -4, 6.4), sm='M1 -46 q5 -5 10 0 q2 8 -5 8 q-7 0 -5 -8z', fill='#7a2f2f', lid=0),   # vast / enormous / countless: huge pupils looking up, small open mouth
    'mischief':  dict(bl='M-24 -90 q12 4 24 8', br='M10 -82 q12 -6 24 -8', bo=1, pup=(2, 1, 4.6), sm='M-12 -46 q18 20 36 -2', fill='none', lid=9),                   # sneak / prank / trick: V brows, sly wide smile
    'hurt':      dict(bl='M-24 -80 q12 -2 24 -8', br='M10 -88 q12 6 24 8', bo=1, pup=(0, 1, 4.4), sm='M-10 -42 l5 -5 l5 5 l5 -5 l5 5 l5 -5', fill='none', lid=0, lidr=27, ex=('sw',)),  # pain / sting / bite: one eye winced shut, zigzag mouth
    'starry':    dict(bl='M-24 -88 q12 -8 24 0', br='M10 -88 q12 -8 24 0', bo=1, pup=(0, 0, 0.1), sm='M-10 -47 q16 20 32 0', fill='none', lid=0, ex=('st',)),           # treasure / magic / dream come true: star eyes
    'blush':     dict(bl='M-24 -84 q12 -6 24 0', br='M10 -84 q12 -6 24 0', bo=0, pup=(0, 1, 5), sm='M-6 -44 q12 8 24 0', fill='none', lid=6, ex=('fl',)),             # shy / praised / embarrassed: small smile, pink cheeks, lowered lids
    'cheeky':    dict(bl='M-24 -86 q12 -6 24 0', br='M10 -90 q12 -8 24 -2', bo=1, pup=(2, 0, 5), sm='M-8 -44 q14 10 28 0', fill='none', lid=0, lidl=27, tongue=7),     # playful / tease / silly: tongue out, one eye shut
    'disgust':   dict(bl='M-24 -86 q12 0 24 4', br='M10 -82 q12 -4 24 -4', bo=1, pup=(0, 1, 4.4), sm='M-8 -40 q14 -10 28 -2', fill='none', lid=8),                    # gross / foul / revolting: raised lip, narrowed eyes
}


def face_js(t, M, tm, gz=0, swirl=False):
    """one tl.set block that puts a MOODS face on frog t at time tm (brows, pupils, mouth, lids per eye, extras); seek-safe"""
    ll = M.get('lidl', M['lid']); lr = M.get('lidr', M['lid']); ex = set(M.get('ex', ())); tg = M.get('tongue', 0)
    o = (f'tl.set("#{t}_bl",{{attr:{{d:"{M["bl"]}"}},opacity:{M["bo"]}}},{tm:.3f});tl.set("#{t}_br",{{attr:{{d:"{M["br"]}"}},opacity:{M["bo"]}}},{tm:.3f});'
         f'tl.set("#{t}_pl",{{attr:{{cx:{-8 + M["pup"][0] + gz:.1f},cy:{-66 + M["pup"][1]},r:{M["pup"][2]}}}}},{tm:.3f});tl.set("#{t}_pr",{{attr:{{cx:{24 + M["pup"][0] + gz:.1f},cy:{-66 + M["pup"][1]},r:{M["pup"][2]}}}}},{tm:.3f});'
         f'tl.set("#{t}_sm",{{attr:{{d:"{M["sm"]}",fill:"{M["fill"]}"}}}},{tm:.3f});tl.set("#{t}_ll",{{attr:{{height:{ll}}}}},{tm:.3f});tl.set("#{t}_lr",{{attr:{{height:{lr}}}}},{tm:.3f});'
         f'tl.set("#{t}_spl,#{t}_spr",{{opacity:{1 if (swirl or "sp" in ex) else 0}}},{tm:.3f});'
         f'tl.set("#{t}_fl1,#{t}_fl2",{{opacity:{.75 if "fl" in ex else 0}}},{tm:.3f});tl.set("#{t}_st",{{opacity:{1 if "st" in ex else 0}}},{tm:.3f});tl.set("#{t}_th",{{opacity:{1 if "th" in ex else 0}}},{tm:.3f});'
         f'tl.set("#{t}_te",{{opacity:{1 if "te" in ex else 0}}},{tm:.3f});tl.set("#{t}_sw",{{opacity:{1 if "sw" in ex else 0}}},{tm:.3f});'
         f'tl.set("#{t}_tg",{{attr:{{ry:{tg * 1.3:.1f},cy:{-44 + tg * 1.4:.1f}}}}},{tm:.3f});'
         f'tl.set("#{t}_al",{{opacity:{1 if ll >= 27 else 0}}},{tm:.3f});tl.set("#{t}_ar",{{opacity:{1 if lr >= 27 else 0}}},{tm:.3f});')   # shut eyes get the happy arc
    return o


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
            f'<g id="{t}_st" opacity="0" fill="#f2c94c" stroke="#b8860b" stroke-width="1.6"><path d="M-10 -74 l2.4 5.6 6 .6 -4.6 4 1.4 6 -5.2 -3.2 -5.2 3.2 1.4 -6 -4.6 -4 6 -.6z"/><path d="M22 -74 l2.4 5.6 6 .6 -4.6 4 1.4 6 -5.2 -3.2 -5.2 3.2 1.4 -6 -4.6 -4 6 -.6z"/></g>'
            f'<path id="{t}_al" d="M-20 -64 q10 7 20 0" fill="none" stroke-width="3" opacity="0"/><path id="{t}_ar" d="M12 -64 q10 7 20 0" fill="none" stroke-width="3" opacity="0"/>'
            f'<path id="{t}_bl" d="M-24 -84 q12 -6 24 0" fill="none" stroke-width="3.4" opacity="0"/><path id="{t}_br" d="M10 -84 q12 -6 24 0" fill="none" stroke-width="3.4" opacity="0"/>'
            f'<path id="{t}_sm" d="M-8 -44 q14 12 28 0" fill="none" stroke-width="3.4"/>'
            f'<path id="{t}_th" d="M-9 -45 h30 v5 q-15 3 -30 0z" fill="#fff" stroke="none" opacity="0"/>'
            f'<ellipse id="{t}_mo" cx="6" cy="-44" rx="13" ry="0" fill="#7a2f2f" stroke-width="2.8"/>'
            f'<ellipse id="{t}_tg" cx="6" cy="-44" rx="8" ry="0" fill="#e8847a" stroke="none"/>'
            f'<g id="{t}_la"><path d="M-34 -22 q-14 6 -16 22" fill="none" stroke-width="7.5"/><path d="M-34 -22 q-14 6 -16 22" fill="none" stroke="{GREEN}" stroke-width="3.4"/></g>'
            f'<g id="{t}_ra"><path d="M34 -22 q14 6 16 22" fill="none" stroke-width="7.5"/><path d="M34 -22 q14 6 16 22" fill="none" stroke="{GREEN}" stroke-width="3.4"/>'
            f'<g id="{t}_sc" opacity="0" transform="translate(50 0) rotate(-55)"><rect x="-5" y="-54" width="10" height="40" rx="3" fill="#3b4a6b" stroke-width="2.4"/><rect x="-7" y="-62" width="14" height="10" rx="3" fill="#8a9bbf" stroke-width="2.4"/><rect x="-4" y="-14" width="8" height="12" rx="2" fill="#8a9bbf" stroke-width="2.2"/></g>'
            f'<g id="{t}_sv" opacity="0" transform="translate(50 0) rotate(28)"><rect x="-3" y="-70" width="6" height="64" rx="2" fill="#a67c52" stroke-width="2.4"/><path d="M-12 -6 h24 l-4 22 q-8 6 -16 0z" fill="#9aa3ad" stroke-width="2.6"/><rect x="-8" y="-78" width="16" height="9" rx="3" fill="#a67c52" stroke-width="2.4"/></g>'
            f'<g id="{t}_bk" opacity="0" transform="translate(46 -8) rotate(-12)"><path d="M-30 -24 q30 -8 60 0 v30 q-30 -8 -60 0z" fill="#f4e6c8" stroke-width="2.8"/><path d="M0 -28 v32" stroke-width="2.4"/><path d="M-22 -16 h16 M-22 -8 h16 M6 -16 h16 M6 -8 h16" stroke="#8a8f96" stroke-width="1.8"/></g>'
            f'<g id="{t}_cm" opacity="0" transform="translate(50 -6)"><rect x="-22" y="-16" width="44" height="30" rx="5" fill="#2b2f3a" stroke-width="2.6"/><circle cx="0" cy="-1" r="9" fill="#6a7a9a" stroke-width="2.4"/><circle cx="0" cy="-1" r="4" fill="#9fd8ff" stroke="none"/><rect x="-16" y="-22" width="12" height="7" rx="2" fill="#2b2f3a" stroke-width="2"/><circle id="{t}_fs" cx="14" cy="-22" r="6" fill="#fff8c4" stroke="none" opacity="0"/></g>'
            f'<g id="{t}_mg" opacity="0" transform="translate(50 -4) rotate(-40)"><rect x="-3.5" y="0" width="7" height="34" rx="2" fill="#a67c52" stroke-width="2.4"/><circle cx="0" cy="-16" r="17" fill="#9fd8ff" fill-opacity=".35" stroke-width="3.2"/><path d="M-8 -24 q6 -6 12 -2" fill="none" stroke="#fff" stroke-width="2.4" opacity=".7"/></g>'
            f'<g id="{t}_pc" opacity="0" transform="translate(50 0) rotate(-35)"><rect x="-3.4" y="-40" width="6.8" height="36" rx="1.4" fill="#f2c94c" stroke-width="2.4"/><rect x="-3.4" y="-45" width="6.8" height="6" rx="2" fill="#e8847a" stroke-width="2.2"/><path d="M-3.4 -4 L0 6 L3.4 -4z" fill="#e8c9a0" stroke-width="2"/><path d="M-1.2 2 L0 6 L1.2 2z" fill="#3a3a3a" stroke="none"/></g></g>'
            f'<g id="{t}_dd" opacity="0" fill="none" stroke="#4a4a52" stroke-width="3" stroke-linecap="round"><path id="{t}_dd1" pathLength="1" d="M58 0 q8 -16 16 0 t16 0 t16 0 t16 0 q10 -14 -2 -16 q-12 0 -6 14"/><path id="{t}_dd2" pathLength="1" d="M60 -26 l4 12 l-12 -8 l16 0 l-12 8z"/><path id="{t}_dd3" pathLength="1" d="M118 -34 q8 -12 16 0 q6 12 -16 24 q-22 -12 -16 -24 q8 -12 16 0"/></g>'
            f'<circle id="{t}_tp" cx="58" cy="-4" r="10" fill="none" stroke="#fff" stroke-width="3" opacity="0"/>'
            f'<g id="{t}_lb" opacity="0" transform="translate(6 -128)"><path d="M-14 -6 q0 -22 14 -22 q14 0 14 22 q0 10 -7 16 h-14 q-7 -6 -7 -16z" fill="#fff3a8" stroke-width="2.8"/><rect x="-7" y="10" width="14" height="8" rx="2" fill="#9aa3ad" stroke-width="2.4"/><path d="M-26 -22 l-8 -6 M26 -22 l8 -6 M0 -36 v-10 M-20 -2 h-10 M20 -2 h10" stroke="#f2c94c" stroke-width="3"/></g>'
            f'<g id="{t}_te" opacity="0"><path id="{t}_te1" d="M-14 -52 q-4 8 0 12 q4 -4 0 -12z" fill="#7fc4f0" stroke="#2f6f9a" stroke-width="1.8"/><path id="{t}_te2" d="M26 -52 q-4 8 0 12 q4 -4 0 -12z" fill="#7fc4f0" stroke="#2f6f9a" stroke-width="1.8"/></g>'
            f'<g id="{t}_zz" opacity="0" fill="none" stroke="#e8f3ff" stroke-width="3" stroke-linecap="round"><path d="M44 -100 h12 l-12 12 h12"/><path d="M62 -124 h9 l-9 9 h9"/></g>'
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
    elif not d.get('roam') and not d.get('act') and not d.get('says') and not d.get('behind'): w.append('a background frog with no act, no bubble and no roam (guideline 7-2 B-1: only a meaningful frog): python3 tools/frog_place.py <slug>')
    return w



def inject(svg_text, mk, ride=None, behind=None):
    """ride = id of a picture group (a spaceship, probe, boat ...): the frog goes INSIDE that group, so it moves, turns and swings with it.
    behind = id of a group: the frog goes right BEFORE that group (the object covers it: peeking out from behind, round 3)"""
    if behind:
        m = re.search(r'<g\b[^>]*(?:\bid="%s"|\bclass="[^"]*\b%s\b[^"]*")[^>]*>' % (re.escape(behind), re.escape(behind)), svg_text)
        if m: return svg_text[:m.start()] + mk + svg_text[m.start():]
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


# ARM AXES (2026-10-26 axis check): #_ra turns about the right shoulder (34,-22), #_la about the left shoulder (-34,-22); the resting arm points down-outward,
# so NEGATIVE rotation lifts the right arm outward/up (wave, salute, hide ~ -118..-165) and POSITIVE turns it across the body (eat/yawn +160, clap +100..124, wish +142);
# mirrored signs for the left arm. The body (#_ac) turns about the feet (svgOrigin 0 0).
REST = 75   # arm hangs down along the body (deg, local); it only moves when the pointed object changes


def js(tag, d, t0, t1, words, targets=None, wt=None):
    """GSAP lines. words = [(start, end)] absolute seconds of the unit's words (mouth), targets = [(time, (x, y))] arm pointing
    (default: sidecar "points"/"point"; none = arm rests), wt = [(text, start, end)] to resolve the "word" keys of points/moods/moves."""
    t = f'fg{tag}'; out = []; a0 = t0 + d['delay']; wt = wt or []
    org = 'svgOrigin:"0 0"'   # the arm's own coordinate space starts at the shoulder (parent group translate(32 -22))
    # entrance / exit by kind (2026-10-26 frog review): only the chalkboard explainer hops up from below; a picture frog fades in where it is
    # (rides: peeks up from its object, roams: drifts in) and fades out shortly before the cut instead of vanishing in one frame
    enter = d.get('enter') or ('hop' if not (d.get('ride') or d.get('kind') in ('ride', 'bg')) else ('peek' if d.get('ride') else 'fade'))
    oy = {'hop': 300, 'peek': 26, 'fade': 0}.get(enter, 40)
    out.append(f'tl.set("#{t}_in",{{opacity:0,y:{oy}}},0);tl.set("#{t}",{{opacity:0}},0);tl.set("#{t}",{{opacity:1}},{a0 - .01:.3f});tl.set("#{t}",{{opacity:0}},{t1:.3f});')
    if enter == 'hop': out.append(f'tl.fromTo("#{t}_in",{{y:300,opacity:0}},{{y:0,opacity:1,duration:.45,ease:"back.out(1.6)",immediateRender:false}},{a0:.3f});')
    else:
        out.append(f'tl.fromTo("#{t}_in",{{y:{oy},opacity:0,scale:.85,svgOrigin:"0 0"}},{{y:0,opacity:1,scale:1,duration:.5,ease:"power2.out",immediateRender:false}},{a0:.3f});')
        if t1 - a0 > 1.4: out.append(f'tl.to("#{t}_in",{{opacity:0,duration:.3,ease:"power1.in"}},{t1 - .32:.3f});')
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
    out.append(f'tl.set("#{t}_arm",{{rotation:{REST},{org}}},0);tl.set("#{t}_spl,#{t}_spr,#{t}_fl1,#{t}_fl2,#{t}_sw,#{t}_dd,#{t}_pc,#{t}_sc,#{t}_sv,#{t}_bk,#{t}_cm,#{t}_mg,#{t}_lb,#{t}_te,#{t}_zz,#{t}_st,#{t}_th",{{opacity:0}},0);')
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
            gz = 3 * float(d.get('gaze') or 0)   # round 3: a frog standing beside / looking at an object keeps its pupils toward it (its facing side = local +x)
            out.append(face_js(t, M, tm, gz=gz, swirl=(pl == 'dizzy')))
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
            c = act.get('c', [d['x'], d['y']]); rx = float(act.get('rx', 160)); ry = float(act.get('ry', 50)); th0 = math.radians(float(act.get('th0', 90))); per = float(act.get('per', 3.4)); sd = -1 if str(act.get('dir', 1)).startswith('-') else 1   # same way as the whirl / ring spins (facing.spin_dir, 4-4 B)
            x0_ = rx * math.cos(th0); y0_ = ry * math.sin(th0); stp = .12; tt = a1
            while tt < T - .02:
                th = th0 + sd * 2 * math.pi * (tt + stp - a1) / per
                gx = d['flip'] * (rx * math.cos(th) - x0_) / d['s']; gy = (ry * math.sin(th) - y0_) / d['s']; sc = 1 + float(act.get('depth', .14)) * math.sin(th)   # nearer (front of the ring) = a little bigger
                out.append(f'tl.to("#{t}_tr",{{x:{gx:.1f},y:{gy:.1f},scaleX:{sc:.3f},scaleY:{sc:.3f},duration:{stp},ease:"none",svgOrigin:"0 0"}},{tt:.3f});'); tt += stp
            out.append(f'tl.to({ac},{{rotation:9,duration:.45,yoyo:true,repeat:{max(int((T - a1) / .45), 1)},ease:"sine.inOut",{org2}}},{a1:.3f});')   # head-rolling wobble
        elif at == 'dizzy' and not isinstance(act, dict):   # (string act) riding something that goes round and round (a particle on its line): head-rolling wobble, woozy face (miya 2026-10-26)
            out.append(f'tl.to({ac},{{rotation:10,y:-3,duration:.5,yoyo:true,repeat:{max(int((T - a1) / .5), 1)},ease:"sine.inOut",{org2}}},{a1:.3f});')
        elif at == 'fly':     # Superman pose (miya 2026-10-26): body turned prone toward its facing side, one arm stretched ahead, gentle bob; for a frog that carries / pulls something through the picture (the footboard under a flying figure)
            out.append(f'tl.to({ac},{{rotation:90,duration:.5,ease:"power2.out",svgOrigin:"0 -40"}},{a1:.3f});tl.to("#{t}_ra",{{rotation:-165,duration:.4,ease:"power2.out",svgOrigin:"34 -22"}},{a1:.3f});')
            out.append(f'tl.to({ac},{{y:-7,duration:1.1,yoyo:true,repeat:{max(int((T - a1) / 1.1), 1)},ease:"sine.inOut"}},{a1 + .5:.3f});')
        elif at == 'tilt':    # curious head tilt, held, then back (miya 2026-10-26: not hopping on every object)
            while tm < T - .3:
                sg = 1 if k % 2 == 0 else -1
                out.append(f'tl.to({ac},{{rotation:{9 * sg},x:{2 * sg},duration:.9,ease:"sine.inOut",{org2}}},{tm:.3f});tl.to({ac},{{rotation:{9 * sg},duration:1.2}},{tm + .9:.3f});tl.to({ac},{{rotation:0,x:0,duration:.9,ease:"sine.inOut",{org2}}},{tm + 2.1:.3f});'); tm += 3.4; k += 1
        elif at == 'sway':    # calm side-to-side lean, like listening to a tune
            while tm < T - .2:
                out.append(f'tl.to({ac},{{rotation:{3 if k % 2 == 0 else -3},x:{3 if k % 2 == 0 else -3},duration:1.5,ease:"sine.inOut",{org2}}},{tm:.3f});'); tm += 1.5; k += 1
        elif at == 'look':    # glances around: pupils slide left and right, head turns a little
            while tm < T - .3:
                for dx, rot, dt in ((-4, -4, 0), (4, 4, 1.1), (0, 0, 2.2)):
                    out.append(f'tl.to("#{t}_pl",{{attr:{{cx:{-8 + dx}}},duration:.25}},{tm + dt:.3f});tl.to("#{t}_pr",{{attr:{{cx:{24 + dx}}},duration:.25}},{tm + dt:.3f});tl.to({ac},{{rotation:{rot},duration:.5,ease:"sine.inOut",{org2}}},{tm + dt:.3f});')
                tm += 3.0
        elif at == 'nod':     # agreeing / explaining: two soft nods, then rest
            while tm < T - .3:
                out.append(f'tl.to({ac},{{y:4,rotation:2,duration:.35,yoyo:true,repeat:3,ease:"sine.inOut",{org2}}},{tm:.3f});'); tm += 3.2
        elif at == 'breathe': # calm, slow breathing, no travel
            out.append(f'tl.to({ac},{{scaleY:1.035,duration:1.8,yoyo:true,repeat:{max(int((T - a1) / 1.8), 1)},ease:"sine.inOut",svgOrigin:"0 0"}},{a1:.3f});')
        elif at == 'slide':   # gravity pit (miya 2026-10-26): slides down the slope of a warped sheet / well to the bottom, leaning into it, then settles with a small dizzy wobble
            gx = d['flip'] * (tg[0] - d['x']) / d['s']; gy = (tg[1] - d['y']) / d['s']; D = max(min(T - a1 - .8, 3.4), .8)
            out.append(f'tl.to("#{t}_tr",{{x:{gx:.1f},duration:{D:.2f},ease:"power1.in"}},{a1:.3f});tl.to("#{t}_tr",{{y:{gy:.1f},duration:{D:.2f},ease:"sine.inOut"}},{a1:.3f});')
            out.append(f'tl.to({ac},{{rotation:{-dirn * 14},duration:{D:.2f},ease:"power1.in",{org2}}},{a1:.3f});tl.to({ac},{{rotation:0,duration:.5,ease:"back.out(2)",{org2}}},{a1 + D:.3f});')
            out.append(f'tl.to({ac},{{rotation:5,duration:.45,yoyo:true,repeat:{max(int((T - a1 - D) / .45), 1)},ease:"sine.inOut",{org2}}},{a1 + D + .5:.3f});')
        elif at == 'float':   # weightless drift
            while tm < T - .2:
                out.append(f'tl.to({ac},{{y:-5,rotation:{2 if k % 2 == 0 else -2},duration:2.0,ease:"sine.inOut",{org2}}},{tm:.3f});tl.to({ac},{{y:2,rotation:{-2 if k % 2 == 0 else 2},duration:2.0,ease:"sine.inOut",{org2}}},{tm + 2.0:.3f});'); tm += 4.0; k += 1   # slow soft drift (miya 2026-10-26: the 1.4 s bobbing looked like meaningless jumping)
        elif at == 'waves':   # riding / bracing against the swell
            while tm < T - .2:
                out.append(f'tl.to({ac},{{y:-14,rotation:{dirn * 7},duration:1.0,ease:"sine.inOut",{org2}}},{tm:.3f});tl.to({ac},{{y:4,rotation:{-dirn * 6},duration:1.0,ease:"sine.inOut",{org2}}},{tm + 1.0:.3f});'); tm += 2.0
        elif at == 'shiver':  # shaking with fear / cold / loneliness: one CustomWiggle tween (uniform) over the whole stay (2026-10-29, was a 0.05 s yoyo loop)
            if T - tm > .3:
                out.append(f'tl.fromTo({ac},{{x:0}},{{x:2.4,duration:{T - .1 - tm:.3f},ease:"wiggle({{wiggles:{max(int((T - tm) / .1), 4)},type:{chr(39)}uniform{chr(39)}}})",immediateRender:false}},{tm:.3f});'); tm = T
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
        elif at == 'push':    # heaving a heavy thing (miya 2026-10-26): leans into it, strains, small forward shoves, sweat drops fall; the frog stands beside the object (use "ride" so it travels with it)
            out.append(f'tl.set("#{t}_sw",{{opacity:1}},{a1:.3f});tl.to("#{t}_ra",{{rotation:-80,duration:.3,svgOrigin:"34 -22"}},{a1:.3f});tl.to({ac},{{rotation:16,x:6,duration:.5,ease:"power2.out",{org2}}},{a1:.3f});')
            n2 = 0
            while tm < T - .3:
                out.append(f'tl.to({ac},{{x:{12 if n2 % 2 == 0 else 5},rotation:{18 if n2 % 2 == 0 else 14},duration:.55,ease:"sine.inOut",{org2}}},{tm + .5:.3f});'); tm += .55; n2 += 1
            for i2 in range(3):
                tw = a1 + .2 + i2 * .45
                while tw < T - .4:
                    out.append(f'tl.fromTo("#{t}_sw{i2}",{{y:0,opacity:1}},{{y:46,opacity:0,duration:.9,ease:"power1.in",immediateRender:false}},{tw:.3f});'); tw += 1.3
        elif at == 'huts':    # runs to each hut, goes in, comes out wearing one more piece of the outfit (bottom, top, headband) and shouts a happy sound word
            hs = (act.get('huts') if isinstance(act, dict) else None) or []
            wear = {'bottom': '_ob', 'top': '_ot', 'head': '_oh'}
            R = f'"#{t}_tr"'; RM = f'"#{t}_rm"'
            cx, cy = d['x'], d['y']
            for h in hs:
                ti = t0 + float(h['t']); lx = (h['x'] - d['x']) / (d['flip'] * d['s']); ly = (h['y'] - d['y']) / d['s']
                hd = .7
                out.append(f'tl.to({R},{{x:{lx:.1f},y:{ly:.1f},duration:{hd},ease:"power1.inOut"}},{ti:.3f});')
                out.append(f'tl.to({R},{{y:{ly - 40:.1f},duration:{hd / 2},ease:"power2.out",overwrite:false}},{ti:.3f});tl.to({R},{{y:{ly:.1f},duration:{hd / 2},ease:"power2.in",overwrite:false}},{ti + hd / 2:.3f});')
                out.append(f'tl.to({RM},{{scaleX:.12,scaleY:.12,opacity:0,duration:.25,ease:"power2.in",svgOrigin:"0 0"}},{ti + hd + .05:.3f});')
                te = ti + hd + .05 + .25 + float(h.get('stay', .5))
                out.append(f'tl.to("#{t}{wear[h["wear"]]}",{{opacity:1,duration:.01}},{te:.3f});tl.to({RM},{{scaleX:1,scaleY:1,opacity:1,duration:.3,ease:"back.out(2)",svgOrigin:"0 0"}},{te:.3f});')
                out.append(f'tl.to({ac},{{y:-22,duration:.18,ease:"power2.out"}},{te + .3:.3f});tl.to({ac},{{y:0,duration:.3,ease:"bounce.out"}},{te + .48:.3f});')
        # ---- round 3 (2026-10-26, guideline 7-2 D): acts that relate the frog to a person / an object in the picture ----
        elif at == 'wave':    # waves at a person in the picture: right arm up, three quick waves, down; again after a pause; small happy lean toward them
            while tm < T - 1.6:
                out.append(f'tl.to("#{t}_ra",{{rotation:-150,duration:.35,ease:"power2.out",svgOrigin:"34 -22"}},{tm:.3f});')
                for j in range(4): out.append(f'tl.to("#{t}_ra",{{rotation:{-150 + (18 if j % 2 == 0 else -18)},duration:.18,ease:"sine.inOut",svgOrigin:"34 -22"}},{tm + .35 + j * .18:.3f});')
                out.append(f'tl.to("#{t}_ra",{{rotation:0,duration:.4,ease:"power2.inOut",svgOrigin:"34 -22"}},{tm + 1.15:.3f});tl.to({ac},{{rotation:4,duration:.5,yoyo:true,repeat:1,ease:"sine.inOut",{org2}}},{tm:.3f});'); tm += 4.2
        elif at == 'peek':    # hidden behind an object (sidecar behind=<group>): slides out sideways to peek, looks around, slides back; the pupils follow
            dx = 34 * (1 if dirn >= 0 else -1)
            while tm < T - 2.2:
                out.append(f'tl.to({ac},{{x:{-dx},duration:.6,ease:"power2.out",{org2}}},{tm:.3f});tl.to("#{t}_pl,#{t}_pr",{{attr:{{cx:"-=5"}},duration:.3}},{tm + .6:.3f});'
                           f'tl.to("#{t}_pl,#{t}_pr",{{attr:{{cx:"+=10"}},duration:.4}},{tm + 1.2:.3f});tl.to("#{t}_pl,#{t}_pr",{{attr:{{cx:"-=5"}},duration:.3}},{tm + 1.8:.3f});tl.to({ac},{{x:0,duration:.5,ease:"power2.in",{org2}}},{tm + 2.3:.3f});'); tm += 4.6
        elif at == 'hang':    # hangs under an object by both hands (feet dangling): arms straight up, slow pendulum sway, little leg kicks
            out.append(f'tl.to("#{t}_ra",{{rotation:-170,duration:.3,svgOrigin:"34 -22"}},{a1 - .3:.3f});tl.to("#{t}_la",{{rotation:170,duration:.3,svgOrigin:"-34 -22"}},{a1 - .3:.3f});')
            out.append(f'tl.to({ac},{{rotation:7,duration:1.3,yoyo:true,repeat:{max(int((T - a1) / 1.3), 1)},ease:"sine.inOut",svgOrigin:"0 -34"}},{a1:.3f});')
            while tm < T - .6:
                out.append(f'tl.to({ac},{{y:4,duration:.25,yoyo:true,repeat:3,ease:"sine.inOut"}},{tm + 1.0:.3f});'); tm += 3.9
        elif at == 'tap':     # taps / knocks on the object beside it: leans in, right arm pokes forward three times, leans back and looks (curious)
            while tm < T - 1.4:
                out.append(f'tl.to({ac},{{rotation:{dirn * 8},x:{dirn * 6},duration:.4,ease:"power2.out",{org2}}},{tm:.3f});')
                for j in range(3):
                    out.append(f'tl.to("#{t}_ra",{{rotation:-60,duration:.14,yoyo:true,repeat:1,ease:"power2.in",svgOrigin:"34 -22"}},{tm + .4 + j * .36:.3f});')
                    out.append(f'tl.fromTo("#{t}_tp",{{scale:.3,opacity:.9,svgOrigin:"58 -4"}},{{scale:1.6,opacity:0,duration:.35,ease:"power2.out",immediateRender:false}},{tm + .54 + j * .36:.3f});')   # little impact ring where the hand knocks
                out.append(f'tl.to({ac},{{rotation:0,x:0,duration:.5,ease:"power2.inOut",{org2}}},{tm + 1.6:.3f});'); tm += 4.0
        elif at == 'hide':    # covers its eyes with both hands (too scary to watch), peeks between the fingers now and then
            out.append(f'tl.to("#{t}_ra",{{rotation:-118,duration:.3,ease:"power2.out",svgOrigin:"34 -22"}},{a1:.3f});tl.to("#{t}_la",{{rotation:118,duration:.3,ease:"power2.out",svgOrigin:"-34 -22"}},{a1:.3f});')
            out.append(f'tl.to({ac},{{x:1.6,duration:.07,yoyo:true,repeat:{int(max(T - a1, .5) / .07)},ease:"none"}},{a1:.3f});')
            tm = a1 + 2.0
            while tm < T - 1.0:
                out.append(f'tl.to("#{t}_ra",{{rotation:-95,duration:.3,svgOrigin:"34 -22"}},{tm:.3f});tl.to("#{t}_ra",{{rotation:-118,duration:.3,svgOrigin:"34 -22"}},{tm + .8:.3f});'); tm += 3.6
        elif at == 'rest':    # leans back against the object (safe / calm / finally), arms down, slow breathing, now and then a contented head tilt
            out.append(f'tl.to({ac},{{rotation:{-dirn * 10},x:{dirn * 5},duration:.7,ease:"power2.out",{org2}}},{a1:.3f});')
            out.append(f'tl.to({ac},{{scaleY:1.03,duration:1.9,yoyo:true,repeat:{max(int((T - a1) / 1.9), 1)},ease:"sine.inOut",svgOrigin:"0 0"}},{a1 + .7:.3f});')
        elif at == 'scope':   # looks through a small telescope held in the right hand: arm up, head tilted back, slow pan; the pupils drift upward
            out.append(f'tl.set("#{t}_sc",{{opacity:1}},{a1 - .2:.3f});tl.to("#{t}_ra",{{rotation:-128,duration:.4,ease:"power2.out",svgOrigin:"34 -22"}},{a1 - .2:.3f});')
            out.append(f'tl.to({ac},{{rotation:{-dirn * 9},duration:.5,ease:"power2.out",{org2}}},{a1:.3f});tl.to("#{t}_pl,#{t}_pr",{{attr:{{cy:-70}},duration:.3}},{a1:.3f});')
            out.append(f'tl.to({ac},{{rotation:{-dirn * 14},duration:2.6,yoyo:true,repeat:{max(int((T - a1) / 2.6), 1)},ease:"sine.inOut",{org2}}},{a1 + .5:.3f});')
        elif at == 'startle': # the object it rides pops / pings / stamps at the start: the frog jolts up with both arms thrown up, round mouth, then settles
            out.append(f'tl.to({ac},{{y:-22,duration:.16,ease:"power3.out"}},{a1:.3f});tl.to({ac},{{y:0,duration:.5,ease:"bounce.out"}},{a1 + .16:.3f});')
            out.append(f'tl.to("#{t}_ra",{{rotation:-150,duration:.15,svgOrigin:"34 -22"}},{a1:.3f});tl.to("#{t}_la",{{rotation:150,duration:.15,svgOrigin:"-34 -22"}},{a1:.3f});')
            out.append(f'tl.to("#{t}_ra",{{rotation:0,duration:.6,ease:"power2.inOut",svgOrigin:"34 -22"}},{a1 + 1.2:.3f});tl.to("#{t}_la",{{rotation:0,duration:.6,ease:"power2.inOut",svgOrigin:"-34 -22"}},{a1 + 1.2:.3f});')
            M = MOODS['shock']
            out.append(f'tl.set("#{t}_sm",{{attr:{{d:"{M["sm"]}",fill:"{M["fill"]}"}}}},{a1:.3f});tl.set("#{t}_pl,#{t}_pr",{{attr:{{r:{M["pup"][2]}}}}},{a1:.3f});')
            M2 = MOODS.get((d.get('moods') or [{}])[0].get('mood', 'happy'), MOODS['happy'])
            out.append(f'tl.set("#{t}_sm",{{attr:{{d:"{M2["sm"]}",fill:"{M2["fill"]}"}}}},{a1 + 1.4:.3f});tl.set("#{t}_pl,#{t}_pr",{{attr:{{r:{M2["pup"][2]}}}}},{a1 + 1.4:.3f});')
        elif at == 'bounce':  # riding something that pulses / swells / wobbles: the frog bobs with it (knees soft), a little late like a passenger
            out.append(f'tl.to({ac},{{y:-6,scaleY:.97,duration:.5,yoyo:true,repeat:{max(int((T - a1) / .5), 1)},ease:"sine.inOut",svgOrigin:"0 0"}},{a1 + .15:.3f});')
        elif at == 'lean':    # riding something that glides / approaches / travels along a path: leans back a little against the motion, hands down, hair-in-the-wind feel without streaks
            out.append(f'tl.to({ac},{{rotation:{-dirn * 7},x:{-dirn * 3},duration:.6,ease:"power2.out",{org2}}},{a1:.3f});')
            out.append(f'tl.to({ac},{{rotation:{-dirn * 10},y:-2,duration:1.1,yoyo:true,repeat:{max(int((T - a1 - .6) / 1.1), 1)},ease:"sine.inOut",{org2}}},{a1 + .6:.3f});')
        # ---- round 4 (2026-10-26, miya: more frog motions for any script); chosen by frog_place.py regexes, guideline 7-2 D ----
        elif at == 'dance':   # sways to a beat, arms alternate up and down (music / song / celebration)
            nb = max(int((T - a1) / .45), 2)
            out.append(f'tl.fromTo({ac},{{rotation:-7,x:-3}},{{rotation:7,x:3,duration:.45,yoyo:true,repeat:{nb},ease:"sine.inOut",{org2}}},{a1:.3f});')
            out.append(f'tl.fromTo("#{t}_ra",{{rotation:-20,svgOrigin:"34 -22"}},{{rotation:-140,duration:.9,yoyo:true,repeat:{max(nb // 2, 1)},ease:"sine.inOut",svgOrigin:"34 -22"}},{a1:.3f});')
            out.append(f'tl.fromTo("#{t}_la",{{rotation:140,svgOrigin:"-34 -22"}},{{rotation:20,duration:.9,yoyo:true,repeat:{max(nb // 2, 1)},ease:"sine.inOut",svgOrigin:"-34 -22"}},{a1:.3f});')
        elif at == 'salute':  # straightens up and salutes with the right hand (missions / captains / crews)
            out.append(f'tl.to({ac},{{scaleY:1.04,duration:.3,ease:"power2.out",svgOrigin:"0 0"}},{a1:.3f});tl.to("#{t}_ra",{{rotation:-160,duration:.35,ease:"back.out(1.6)",svgOrigin:"34 -22"}},{a1:.3f});')
            out.append(f'tl.to("#{t}_ra",{{rotation:0,duration:.5,ease:"power2.inOut",svgOrigin:"34 -22"}},{min(a1 + 3.2, T - .3):.3f});tl.to({ac},{{scaleY:1,duration:.4,svgOrigin:"0 0"}},{min(a1 + 3.2, T - .3):.3f});')
        elif at == 'think':   # hand on the chin, head tilted, eyes up (questions / puzzles / theories)
            out.append(f'tl.to("#{t}_la",{{rotation:-152,duration:.4,ease:"power2.out",svgOrigin:"-34 -22"}},{a1:.3f});tl.to({ac},{{rotation:{dirn * 6},duration:.5,ease:"power2.out",{org2}}},{a1:.3f});')
            out.append(f'tl.to("#{t}_pl,#{t}_pr",{{attr:{{cy:-70}},duration:.3}},{a1:.3f});')
            out.append(f'tl.to({ac},{{rotation:{-dirn * 4},duration:2.4,yoyo:true,repeat:{max(int((T - a1 - .5) / 2.4), 1)},ease:"sine.inOut",{org2}}},{a1 + .5:.3f});')
        elif at == 'facepalm':   # right hand over the face, head down, slow shake (mistakes / failures / oops)
            out.append(f'tl.to("#{t}_ra",{{rotation:-160,duration:.3,ease:"power2.in",svgOrigin:"34 -22"}},{a1:.3f});tl.to({ac},{{rotation:{dirn * 8},y:4,duration:.35,ease:"power2.out",{org2}}},{a1:.3f});')
            out.append(f'tl.to({ac},{{x:-3,duration:.6,yoyo:true,repeat:{max(int((T - a1 - .4) / .6), 1)},ease:"sine.inOut",{org2}}},{a1 + .4:.3f});')
        elif at == 'idea':    # a light bulb pops above the head, both arms up for a moment (ideas / realisations / inventions)
            out.append(f'tl.to({ac},{{y:-6,duration:.2,ease:"power2.out"}},{a1:.3f});tl.to({ac},{{y:0,duration:.4,ease:"bounce.out"}},{a1 + .2:.3f});')
            out.append(f'tl.fromTo("#{t}_lb",{{opacity:0,scale:.3,svgOrigin:"6 -128"}},{{opacity:1,scale:1,duration:.35,ease:"back.out(2.4)",immediateRender:false}},{a1 + .1:.3f});tl.to("#{t}_lb",{{opacity:0,duration:.3}},{min(a1 + 2.8, T - .2):.3f});')
            out.append(f'tl.to("#{t}_ra",{{rotation:-150,duration:.25,svgOrigin:"34 -22"}},{a1:.3f});tl.to("#{t}_la",{{rotation:150,duration:.25,svgOrigin:"-34 -22"}},{a1:.3f});')
            out.append(f'tl.to("#{t}_ra",{{rotation:0,duration:.5,svgOrigin:"34 -22"}},{min(a1 + 2.6, T - .3):.3f});tl.to("#{t}_la",{{rotation:0,duration:.5,svgOrigin:"-34 -22"}},{min(a1 + 2.6, T - .3):.3f});')
        elif at == 'dig':     # digs with a small shovel: bends, pushes down, lifts, again (fossils / excavations / buried things)
            out.append(f'tl.set("#{t}_sv",{{opacity:1}},{a1 - .1:.3f});tl.to("#{t}_ra",{{rotation:-40,duration:.3,svgOrigin:"34 -22"}},{a1 - .1:.3f});')
            while tm < T - 1.3:
                out.append(f'tl.to({ac},{{rotation:{dirn * 9},y:4,duration:.4,ease:"power2.in",{org2}}},{tm:.3f});tl.to("#{t}_ra",{{rotation:-10,duration:.4,ease:"power2.in",svgOrigin:"34 -22"}},{tm:.3f});')
                out.append(f'tl.to({ac},{{rotation:{-dirn * 4},y:-2,duration:.5,ease:"power2.out",{org2}}},{tm + .45:.3f});tl.to("#{t}_ra",{{rotation:-70,duration:.5,ease:"power2.out",svgOrigin:"34 -22"}},{tm + .45:.3f});'); tm += 1.3
        elif at == 'read':    # holds a book in front, head nods along the lines, turns a page now and then (books / records / letters)
            out.append(f'tl.set("#{t}_bk",{{opacity:1}},{a1 - .1:.3f});tl.to("#{t}_ra",{{rotation:-60,duration:.35,svgOrigin:"34 -22"}},{a1 - .1:.3f});tl.to("#{t}_pl,#{t}_pr",{{attr:{{cy:-62}},duration:.3}},{a1:.3f});')
            out.append(f'tl.fromTo({ac},{{rotation:{dirn * 2}}},{{rotation:{dirn * 5},duration:1.6,yoyo:true,repeat:{max(int((T - a1) / 1.6), 1)},ease:"sine.inOut",{org2}}},{a1:.3f});')
            tm = a1 + 2.6
            while tm < T - 1:
                out.append(f'tl.to("#{t}_bk",{{scaleX:.2,duration:.14,yoyo:true,repeat:1,svgOrigin:"46 -8"}},{tm:.3f});'); tm += 3.1
        elif at == 'eat':     # munches: hand to the mouth, cheeks blush, little chews (food / meals / hunger)
            out.append(f'tl.to("#{t}_ra",{{rotation:160,duration:.35,ease:"power2.out",svgOrigin:"34 -22"}},{a1:.3f});')
            nb = max(int((T - a1 - .4) / .32), 2)
            out.append(f'tl.fromTo({ac},{{scaleY:1}},{{scaleY:.97,duration:.16,yoyo:true,repeat:{nb},ease:"sine.inOut",svgOrigin:"0 0"}},{a1 + .4:.3f});')
            out.append(f'tl.fromTo("#{t}_fl1,#{t}_fl2",{{opacity:0}},{{opacity:.7,duration:.3,immediateRender:false}},{a1 + .4:.3f});')
        elif at == 'cry':     # sad face, tears drop again and again, shoulders tremble (deaths / extinctions / goodbyes)
            M = MOODS['sad']
            out.append(face_js(t, M, a1))
            out.append(f'tl.set("#{t}_te",{{opacity:1}},{a1 + .2:.3f});tl.to({ac},{{x:1.4,duration:.09,yoyo:true,repeat:{int(max(T - a1, .5) / .09)},ease:"none"}},{a1:.3f});')
            for j, te in enumerate(('te1', 'te2')):
                out.append(f'tl.fromTo("#{t}_{te}",{{y:0,opacity:1}},{{y:46,opacity:0,duration:1.1,ease:"power1.in",repeat:{max(int((T - a1 - .2) / 1.1) - 1, 0)},immediateRender:false}},{a1 + .2 + j * .5:.3f});')
        elif at == 'photo':   # lifts a camera, the flash pops, smiles (photographs / images / footage)
            out.append(f'tl.set("#{t}_cm",{{opacity:1}},{a1 - .1:.3f});tl.to("#{t}_ra",{{rotation:-95,duration:.4,ease:"power2.out",svgOrigin:"34 -22"}},{a1 - .1:.3f});')
            tm = a1 + .8
            while tm < T - .8:
                out.append(f'tl.fromTo("#{t}_fs",{{opacity:1,scale:.4,svgOrigin:"14 -22"}},{{opacity:0,scale:4,duration:.3,ease:"power2.out",immediateRender:false}},{tm:.3f});tl.to({ac},{{y:-3,duration:.08,yoyo:true,repeat:1}},{tm:.3f});'); tm += 3.4
        elif at == 'sneeze':  # leans back slowly, then a quick forward sneeze (dust / pollen / spores)
            while tm < T - 1.6:
                out.append(f'tl.to({ac},{{rotation:{-dirn * 12},y:-3,duration:1.1,ease:"power1.in",{org2}}},{tm:.3f});tl.to("#{t}_pl,#{t}_pr",{{attr:{{cy:-70}},duration:.6}},{tm:.3f});')
                out.append(f'tl.to({ac},{{rotation:{dirn * 14},y:4,duration:.12,ease:"power3.in",{org2}}},{tm + 1.1:.3f});tl.to({ac},{{rotation:0,y:0,duration:.5,ease:"power2.out",{org2}}},{tm + 1.25:.3f});tl.to("#{t}_pl,#{t}_pr",{{attr:{{cy:-66}},duration:.2}},{tm + 1.1:.3f});'); tm += 4.2
        elif at == 'clap':    # claps with both hands in front (applause / success / congratulations)
            nb = max(int((T - a1) / .3), 2)
            out.append(f'tl.fromTo("#{t}_ra",{{rotation:100,svgOrigin:"34 -22"}},{{rotation:124,duration:.15,yoyo:true,repeat:{nb},ease:"power1.inOut",svgOrigin:"34 -22"}},{a1:.3f});')   # hands meet in front of the chest (axis check 2026-10-26: + turns the right arm toward the body)
            out.append(f'tl.fromTo("#{t}_la",{{rotation:-100,svgOrigin:"-34 -22"}},{{rotation:-124,duration:.15,yoyo:true,repeat:{nb},ease:"power1.inOut",svgOrigin:"-34 -22"}},{a1:.3f});')
            out.append(f'tl.fromTo({ac},{{y:0}},{{y:-3,duration:.3,yoyo:true,repeat:{nb // 2},ease:"sine.inOut"}},{a1:.3f});')
        elif at == 'magnify': # inspects with a magnifying glass, leaning in and out (clues / evidence / tiny things)
            out.append(f'tl.set("#{t}_mg",{{opacity:1}},{a1 - .1:.3f});tl.to("#{t}_ra",{{rotation:-80,duration:.4,ease:"power2.out",svgOrigin:"34 -22"}},{a1 - .1:.3f});')
            out.append(f'tl.to({ac},{{rotation:{dirn * 8},x:{dirn * 6},duration:1.4,yoyo:true,repeat:{max(int((T - a1) / 1.4), 1)},ease:"sine.inOut",{org2}}},{a1:.3f});')
        elif at == 'snooze':  # dozes off: eyes shut, slow nod, Zz floating up (slow / waiting stretches)
            out.append(f'tl.to("#{t}_ll,#{t}_lr",{{attr:{{height:22}},duration:.6}},{a1:.3f});tl.to({ac},{{rotation:{dirn * 10},duration:.9,ease:"power2.out",{org2}}},{a1:.3f});')
            out.append(f'tl.to({ac},{{rotation:{dirn * 14},y:2,duration:2.6,yoyo:true,repeat:{max(int((T - a1 - .9) / 2.6), 1)},ease:"sine.inOut",{org2}}},{a1 + .9:.3f});')
            out.append(f'tl.fromTo("#{t}_zz",{{opacity:0,y:0}},{{opacity:1,y:-18,duration:1.6,ease:"power1.out",repeat:{max(int((T - a1 - 1) / 1.9) - 1, 0)},repeatDelay:.3,immediateRender:false}},{a1 + 1:.3f});')
        elif at in SIMPLE_ACTS:   # round 4b data-driven acts (12): a held pose + one looping body motion, optional prop / mood
            A = SIMPLE_ACTS[at]
            if A.get('ra') is not None: out.append(f'tl.to("#{t}_ra",{{rotation:{A["ra"]},duration:.35,ease:"power2.out",svgOrigin:"34 -22"}},{a1:.3f});')
            if A.get('la') is not None: out.append(f'tl.to("#{t}_la",{{rotation:{A["la"]},duration:.35,ease:"power2.out",svgOrigin:"-34 -22"}},{a1:.3f});')
            if A.get('prop'): out.append(f'tl.set("#{t}_{A["prop"]}",{{opacity:1}},{a1 - .05:.3f});')
            if A.get('pup') is not None: out.append(f'tl.to("#{t}_pl,#{t}_pr",{{attr:{{cy:{A["pup"]}}},duration:.3}},{a1:.3f});')
            if A.get('mood'):
                M = MOODS[A['mood']]
                out.append(face_js(t, M, a1))
            if A.get('mouth'): out.append(f'tl.set("#{t}_sm",{{opacity:0}},{a1:.3f});tl.set("#{t}_mo",{{attr:{{ry:{A["mouth"]},cy:{-44 + A["mouth"]}}}}},{a1:.3f});')
            fr, to, per = A['body']; fr = {k: (v * dirn if k in ('rotation', 'x') and A.get('mirror') else v) for k, v in fr.items()}; to = {k: (v * dirn if k in ('rotation', 'x') and A.get('mirror') else v) for k, v in to.items()}
            jsd = lambda d_: ','.join(f'{k}:{v}' for k, v in d_.items())
            out.append(f'tl.fromTo({ac},{{{jsd(fr)},{org2}}},{{{jsd(to)},duration:{per},yoyo:true,repeat:{max(int((T - a1 - .3) / per), 1)},ease:"sine.inOut",{org2}}},{a1 + .3:.3f});')
            if A.get('sweat'): out.append(f'tl.set("#{t}_sw",{{opacity:1}},{a1 + .4:.3f});tl.fromTo("#{t}_sw0,#{t}_sw1,#{t}_sw2",{{y:0,opacity:1}},{{y:26,opacity:0,duration:1.1,stagger:.35,repeat:{max(int((T - a1) / 1.6), 1)},ease:"power1.in",immediateRender:false}},{a1 + .4:.3f});')
            if A.get('spiral'): out.append(f'tl.set("#{t}_spl,#{t}_spr",{{opacity:1}},{a1 + .4:.3f});tl.to("#{t}_spl,#{t}_spr",{{rotation:360,duration:1.6,repeat:{max(int((T - a1) / 1.6), 1)},ease:"none",svgOrigin:"-10 -66"}},{a1 + .4:.3f});')
        elif at == 'cheer':   # happy hops with both arms up
            out.append(f'tl.to("#{t}_ra",{{rotation:-150,duration:.3,svgOrigin:"34 -22"}},{a1:.3f});tl.to("#{t}_la",{{rotation:150,duration:.3,svgOrigin:"-34 -22"}},{a1:.3f});')
            while tm < T - .2:
                out.append(f'tl.to({ac},{{y:-16,rotation:{5 if k % 2 == 0 else -5},duration:.3,ease:"power2.out",{org2}}},{tm:.3f});tl.to({ac},{{y:0,rotation:0,duration:.35,ease:"bounce.out",{org2}}},{tm + .3:.3f});'); tm += 2.4; k += 1   # fewer, lower hops: only for a real cheer
        elif at == 'sleepy':  # slow time: heavy slow sway, drooping
            while tm < T - .2:
                out.append(f'tl.to({ac},{{rotation:5,y:3,duration:2.2,ease:"sine.inOut",{org2}}},{tm:.3f});tl.to({ac},{{rotation:-4,y:0,duration:2.2,ease:"sine.inOut",{org2}}},{tm + 2.2:.3f});'); tm += 4.4
    # ---- speech bubble / sound word (2026-10-26): says = [{text, word?, dur?, shout?}]; pops in at the word, shakes when shouted, fades after dur ----
    for k, sy in enumerate(d.get('says') or []):
        tm = find_word(sy.get('word'), wt, a0, t1) if sy.get('word') else None
        if tm is None and sy.get('t') is not None: tm = t0 + float(sy['t'])   # seconds into the unit
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
    # blinks at irregular intervals (back to the mood's eye height afterwards)
    M0 = MOODS.get((d.get('moods') or [{}])[0].get('mood', 'happy'), MOODS['happy']); lid = M0['lid']; lidl, lidr = M0.get('lidl', lid), M0.get('lidr', lid)
    tb = a0 + 1.1; kb = 0
    while tb < t1 - .2:
        out.append(f'tl.to("#{t}_ll,#{t}_lr",{{attr:{{height:27}},duration:.06,ease:"none"}},{tb:.3f});tl.set("#{t}_al,#{t}_ar",{{opacity:1}},{tb + .06:.3f});'
                   f'tl.set("#{t}_al,#{t}_ar",{{opacity:0}},{tb + .1:.3f});tl.to("#{t}_ll",{{attr:{{height:{lidl}}},duration:.08,ease:"none"}},{tb + .1:.3f});tl.to("#{t}_lr",{{attr:{{height:{lidr}}},duration:.08,ease:"none"}},{tb + .1:.3f});')
        tb += (2.3, 3.6, .32, 2.9, 4.1)[kb % 5]; kb += 1   # irregular blinks with an occasional double blink (a fixed 2.7 s looked mechanical)
    return out
