# Helpers for thumbnail pages (guideline 16-6): big stacked text top-left + one metaphor picture (SVG), 1920x1080.
# usage in videos/<slug>/thumb/make.py:  from thumb_lib import *;  open('A.html','w').write(page(bg, svg, [(text, size, 'w'|'y'), ...]))
import random, math
HEAD = '<!doctype html><html><head><meta charset="utf-8"><link rel="stylesheet" href="common.css"><style>%s</style></head><body><div class="stage">'


def page(bg, svg, lines, outline='#050b18', left=84, top=40):
    css = f'body{{background:{bg}}}.o{{-webkit-text-stroke:15px {outline};paint-order:stroke fill}}.g{{color:#F2D27A}}'
    html = ''; y = top
    for k, (t, sz, c) in enumerate(lines):
        css += f'#t{k}{{left:{left}px;top:{y}px;font-size:{sz}px;letter-spacing:3px;line-height:1}}'
        html += f'<div class="txt o{" g" if c == "y" else ""}" id="t{k}">{t}</div>'
        y += int(sz * 0.97)
    return HEAD % css + svg + html + '</div></body></html>'


def svg(defs, body):
    return f'<svg class="art" viewBox="0 0 1920 1080" xmlns="http://www.w3.org/2000/svg"><defs>{defs}</defs>{body}</svg>'


def lin(id, stops, x2=0, y2=1):
    return f'<linearGradient id="{id}" x1="0" y1="0" x2="{x2}" y2="{y2}">' + ''.join(f'<stop offset="{o}" stop-color="{c}"/>' for o, c in stops) + '</linearGradient>'


def rad(id, cx, cy, r, stops):
    return f'<radialGradient id="{id}" cx="{cx}" cy="{cy}" r="{r}" gradientUnits="userSpaceOnUse">' + ''.join(f'<stop offset="{o}" stop-color="{c}" stop-opacity="{a}"/>' for o, c, a in stops) + '</radialGradient>'


def stars(n, ymax, xmin=0, col='#e8f4ff', op=.5, sparks=4):
    out = ''
    for _ in range(n):
        out += f'<circle cx="{random.randint(xmin + 20, 1900)}" cy="{random.randint(10, ymax)}" r="{random.choice([1.3, 1.9, 2.6])}" fill="{col}" opacity="{op * random.random() + .15:.2f}"/>'
    for _ in range(sparks):
        out += spark(random.randint(max(xmin, 900), 1880), random.randint(40, max(60, ymax - 40)), random.choice([14, 18, 22]))
    return out


def spark(x, y, s, col='#fff6d6', op=.85):
    return (f'<path transform="translate({x} {y})" d="M0 {-s} L{s * .2:.1f} {-s * .2:.1f} L{s} 0 L{s * .2:.1f} {s * .2:.1f} L0 {s} '
            f'L{-s * .2:.1f} {s * .2:.1f} L{-s} 0 L{-s * .2:.1f} {-s * .2:.1f}Z" fill="{col}" opacity="{op}"/>')


def blobs(n, x0, y0, x1, y1, col, o0, o1, rmin, rmax):
    return ''.join(f'<ellipse cx="{random.randint(x0, x1)}" cy="{random.randint(y0, y1)}" rx="{random.randint(rmin, rmax)}" ry="{random.randint(rmin // 2, rmax // 2)}" '
                   f'fill="{col}" opacity="{random.uniform(o0, o1):.2f}"/>' for _ in range(n))


# --- Shorts thumbnails (miya 2026-11-06, guideline 16-9): VERTICAL 1080x1920, text CENTRED, no empty corner needed ---
# usage in videos/<slug>-shortN/thumb/make.py: open('A.html','w').write(vpage(bg, vsvg(defs, body), [(text, size, 'w'|'y'), ...]))  (copy tools/assets/thumb_v/common.css next to it)
def vpage(bg, svg, lines, outline='#050b18', top=700):
    css = f'body{{background:{bg}}}.o{{-webkit-text-stroke:15px {outline};paint-order:stroke fill}}.g{{color:#F2D27A}}'
    html = ''; y = top
    for k, (t, sz, c) in enumerate(lines):
        css += f'#t{k}{{left:0;width:1080px;text-align:center;top:{y}px;font-size:{sz}px;letter-spacing:3px;line-height:1}}'
        html += f'<div class="txt o{" g" if c == "y" else ""}" id="t{k}">{t}</div>'
        y += int(sz * 0.97)
    return HEAD % css + svg + html + '</div></body></html>'


def vsvg(defs, body):
    return f'<svg class="art" viewBox="0 0 1080 1920" xmlns="http://www.w3.org/2000/svg"><defs>{defs}</defs>{body}</svg>'


# --- Shorts "glow" helpers (miya 2026-11-07, guideline 16-9 B): dark scene + glowing focal object + light particles ---
# defs needs a blur filter id "b6" and "b50" (FILTERS in videos/*/thumb/make.py) for fireflies() and darkband().
def fireflies(n, y0=260, y1=1850, w=1080, col='#fff3a8', core='#fffbd0', seed=None):
    """n glowing light dots (fireflies / plankton / dust). Call random.seed() first for a repeatable layout."""
    if seed is not None: random.seed(seed)
    out = ''
    for _ in range(n):
        x, y, r = random.randint(0, w), random.randint(y0, y1), random.choice([3, 4, 6])
        out += (f'<circle cx="{x}" cy="{y}" r="{r * 3}" fill="{col}" opacity=".18" filter="url(#b6)"/>'
                f'<circle cx="{x}" cy="{y}" r="{r}" fill="{core}" opacity=".9"/>')
    return out


def halo(id, cx, cy, r, inner='#fff3a8', outer='#7ff5d8'):
    """radial glow gradient def (use with <ellipse fill="url(#id)">) behind the focal object"""
    return rad(id, cx, cy, r, [(0, inner, .95), (.35, outer, .45), (1, outer, 0)])


def darkband(y0, y1, a=.4):
    """soft dark band behind the centred text so it stays readable on a bright/glowing scene"""
    return f'<rect x="-50" y="{y0}" width="1180" height="{y1 - y0}" fill="#000" opacity="{a}" filter="url(#b50)"/>'
