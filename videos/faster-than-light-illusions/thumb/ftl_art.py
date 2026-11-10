# Shared drawing helpers for the faster-than-light-illusions thumbnails (long A-C in this folder, shorts 1-5 in
# videos/faster-than-light-illusions-shortN/thumb). Reuses the posable mascot frog / moon / smooth() from the pluto thumbnails.
import os, sys, math, random, importlib.util
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, '../../..'))
sys.path.insert(0, os.path.join(REPO, 'tools'))
from thumb_lib import page, svg, vpage, vsvg, lin, rad, spark, halo, darkband, fireflies
from figlib import person, hand
_spec = importlib.util.spec_from_file_location('pluto_thumb', os.path.join(REPO, 'videos/pluto-not-a-planet/thumb/make.py'))
P = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(P)
smooth, moon, starfield, INK, GREEN = P.smooth, P.moon, P.starfield, P.INK, P.GREEN
FILTERS = P.FILTERS
BODY = 'M-34 0 q-6 -64 34 -70 q40 -2 42 62 q0 10 -6 12 q-36 6 -70 -4z'
FROG_DEFS = f'<clipPath id="frogbody"><path d="{BODY}"/></clipPath>'
LIM = 6.6   # pupil centre offset limit (eye white r13.5, pupil r4.4)


def frog(*a, **kw):
    lx, ly = kw.get('look', (0, 0)); dx, dy = 1 + lx, ly; m = math.hypot(dx, dy)
    if m > LIM: dx, dy = dx * LIM / m, dy * LIM / m
    kw['look'] = (dx - 1, dy)
    return P.frog(*a, **kw)


# ---------------- outfits (frog units: feet y=0, head top ~-72, brows -88) ----------------
def suit(col, stripe=None, y0=-28):
    """clothes over the lower body (clipped to the frog body)."""
    o = f'<g clip-path="url(#frogbody)"><rect x="-60" y="{y0}" width="130" height="50" fill="{col}" stroke="none"/>'
    if stripe:
        for k in range(6):
            o += f'<rect x="-60" y="{y0 + 5 + k * 9}" width="130" height="3.6" fill="{stripe}" stroke="none"/>'
    o += f'<path d="M-40 {y0} q44 10 90 0" fill="none" stroke="{INK}" stroke-width="3"/></g>'
    return o


NIGHTCAP = ('<path d="M-30 -84 q30 -14 66 -2 q-4 -30 -30 -40 q-30 -10 -46 4 q-6 10 4 38z" fill="#4a6fc0" stroke-width="3.2"/>'
            '<path d="M-22 -112 l6 6 M-6 -118 l4 7 M10 -116 l2 8" stroke="#dfe8ff" stroke-width="3"/>'
            '<path d="M-26 -116 q-26 4 -34 24" fill="none" stroke="#4a6fc0" stroke-width="13"/><path d="M-26 -116 q-26 4 -34 24" fill="none" stroke="' + INK + '" stroke-width="3" opacity="0"/>'
            '<circle cx="-62" cy="-90" r="9" fill="#f4f1e6" stroke-width="3"/>'
            '<path d="M-34 -86 q34 -14 72 -2 l1 8 q-38 -10 -74 2z" fill="#f4f1e6" stroke-width="3"/>')
HARDHAT = ('<path d="M-36 -86 q2 -36 40 -38 q38 2 42 38z" fill="#f2c230" stroke-width="3.4"/>'
           '<path d="M-46 -86 l100 0 q2 7 -4 9 l-92 0 q-6 -2 -4 -9z" fill="#e0ad1c" stroke-width="3.2"/>'
           '<path d="M4 -122 l0 34" stroke="#c99512" stroke-width="5"/><path d="M-22 -108 q8 -12 20 -14" fill="none" stroke="#fff6c8" stroke-width="3.5" opacity=".8"/>')
CHEFHAT = ('<path d="M-26 -84 l-4 -22 q-22 -6 -12 -26 q8 -14 24 -6 q6 -18 26 -14 q16 4 16 16 q20 -6 24 12 q2 16 -16 20 l-2 20z" fill="#fbfbf6" stroke-width="3.2"/>'
           '<path d="M-26 -84 q30 6 56 0 l0 -10 q-28 6 -56 0z" fill="#e8e6dc" stroke-width="3"/>')


def glow_line(x1, y1, x2, y2, col, w, gw=None, op=1, blur='b6'):
    gw = gw or w * 5
    return (f'<path d="M{x1:.1f} {y1:.1f} L{x2:.1f} {y2:.1f}" stroke="{col}" stroke-width="{gw}" stroke-linecap="round" opacity="{.45 * op:.2f}" filter="url(#{blur})"/>'
            f'<path d="M{x1:.1f} {y1:.1f} L{x2:.1f} {y2:.1f}" stroke="{col}" stroke-width="{w}" stroke-linecap="round" opacity="{op}"/>')


def galaxy(cx, cy, r, rot, col='#cfe0ff', core='#fff4d8', uid='g', tilt=.45, rnd=None):
    """small spiral galaxy: glowing core + two arms of dots, squashed by tilt."""
    rnd = rnd or random.Random(uid)
    o = f'<g transform="translate({cx:.1f} {cy:.1f}) rotate({rot}) scale(1 {tilt})">'
    o += f'<circle r="{r * 1.25:.1f}" fill="{col}" opacity=".22" filter="url(#b12)"/>'
    for arm in (0, math.pi):
        pts = [(math.cos(arm + t * 2.6) * r * t, math.sin(arm + t * 2.6) * r * t) for t in [i / 14 for i in range(1, 15)]]
        o += f'<path d="{smooth(pts)}" fill="none" stroke="{col}" stroke-width="{r * .22:.1f}" opacity=".55" filter="url(#b3)"/>'
        for x, y in pts[2:]:
            o += f'<circle cx="{x + rnd.uniform(-2, 2):.1f}" cy="{y + rnd.uniform(-2, 2):.1f}" r="{rnd.uniform(.8, 2.2) * r / 40:.1f}" fill="#fff" opacity=".8"/>'
    o += f'<circle r="{r * .38:.1f}" fill="{core}" opacity=".7" filter="url(#b6)"/><circle r="{r * .16:.1f}" fill="#fff"/></g>'
    return o


def scissors(x, y, L, ang, gap, uid='sc', col='#cdd6e6'):
    """giant open scissors: pivot near handles at (x,y), blades length L along direction ang (deg), opening gap (deg).
    Returns (svg, intersection point)."""
    a = math.radians(ang); h1 = math.radians(ang + gap / 2); h2 = math.radians(ang - gap / 2)
    o = ''
    for k, hh in enumerate((h1, h2)):
        tx, ty = x + math.cos(hh) * L, y + math.sin(hh) * L
        nx, ny = -math.sin(hh), math.cos(hh); sgn = 1 if k == 0 else -1
        w = 34
        bl = [(x - math.cos(hh) * 40 + nx * w * sgn * .4, y - math.sin(hh) * 40 + ny * w * sgn * .4),
              (x + math.cos(hh) * L * .5 + nx * w * sgn, y + math.sin(hh) * L * .5 + ny * w * sgn), (tx, ty),
              (x + math.cos(hh) * L * .5 - nx * 6 * sgn, y + math.sin(hh) * L * .5 - ny * 6 * sgn), (x - math.cos(hh) * 40, y - math.sin(hh) * 40)]
        d = 'M' + ' L'.join(f'{px:.1f},{py:.1f}' for px, py in bl) + 'Z'
        o += f'<path d="{d}" fill="url(#blade{uid})" stroke="#1a2236" stroke-width="5" stroke-linejoin="round"/>'
        o += f'<path d="M{bl[4][0]:.1f} {bl[4][1]:.1f} L{tx:.1f} {ty:.1f}" stroke="#ffffff" stroke-width="4" opacity=".9"/>'
        # handle ring behind the pivot
        hx, hy = x - math.cos(hh) * 150, y - math.sin(hh) * 150
        hx += -math.sin(hh) * 50 * -sgn; hy += math.cos(hh) * 50 * -sgn
        o = (f'<ellipse cx="{hx:.1f}" cy="{hy:.1f}" rx="70" ry="48" transform="rotate({math.degrees(hh):.1f} {hx:.1f} {hy:.1f})" fill="none" stroke="#1a2236" stroke-width="40"/>'
             f'<ellipse cx="{hx:.1f}" cy="{hy:.1f}" rx="70" ry="48" transform="rotate({math.degrees(hh):.1f} {hx:.1f} {hy:.1f})" fill="none" stroke="#d6453d" stroke-width="30"/>'
             f'<path d="M{x:.1f} {y:.1f} L{hx:.1f} {hy:.1f}" stroke="#1a2236" stroke-width="40" stroke-linecap="round"/><path d="M{x:.1f} {y:.1f} L{hx:.1f} {hy:.1f}" stroke="#d6453d" stroke-width="30" stroke-linecap="round"/>') + o
    o += f'<circle cx="{x}" cy="{y}" r="22" fill="#e9eef7" stroke="#1a2236" stroke-width="5"/><circle cx="{x}" cy="{y}" r="7" fill="#1a2236"/>'
    defs = lin(f'blade{uid}', [(0, '#f6f9ff'), (.5, col), (1, '#6b7894')], 1, 1)
    return defs, o
