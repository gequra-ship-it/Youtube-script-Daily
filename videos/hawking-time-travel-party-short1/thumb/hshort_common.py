# Shared helpers for the hawking-time-travel-party-short1..5 Shorts thumbnails (style B, guideline 16-9, brief tools/briefs/thumb_art.md).
# Reuses frog / limb / mix / lina from the long-form thumbnails (videos/hawking-time-travel-party/thumb/make.py) without running
# that file's A-C writer. Each videos/hawking-time-travel-party-shortN/thumb/make.py imports this and writes A.html.
import os, sys, math, random, shutil
_HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(_HERE, '..', '..', '..'))
sys.path.insert(0, os.path.join(REPO, 'tools'))
_LF = os.path.join(REPO, 'videos', 'hawking-time-travel-party', 'thumb', 'make.py')
_src = open(_LF).read(); _src = _src[:_src.index("for n, fn in (('A', thumb_A)")]
_NS = {'__file__': _LF}; exec(compile(_src, _LF, 'exec'), _NS)
frog, limb, P, mix, lina = _NS['frog'], _NS['limb'], _NS['P'], _NS['mix'], _NS['lina']
INK, GREEN, DARKG = _NS['INK'], _NS['GREEN'], _NS['DARKG']
FILTERS = _NS['FILTERS'] + ''.join(f'<filter id="b{n}" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="{n}"/></filter>' for n in (6, 12, 24))
from thumb_lib import vpage, vsvg, lin, rad, spark, fireflies, halo, darkband

W, H = 1080, 1920


def vig(id='vig', a=.75):
    return rad(id, 540, 900, 1250, [(0, '#000', 0), (.52, '#000', 0), (1, '#000', a)])


def stars(rnd, n, y0=0, y1=H, col='#e8f0ff', big=6, x0=0, x1=W):
    o = ''.join(f'<circle cx="{rnd.uniform(x0, x1):.0f}" cy="{rnd.uniform(y0, y1):.0f}" r="{rnd.choice([1.1, 1.6, 2.2])}" fill="{col}" opacity="{rnd.uniform(.25, .9):.2f}"/>' for _ in range(n))
    for _ in range(big):
        x, y = rnd.uniform(x0 + 30, x1 - 30), rnd.uniform(y0 + 20, y1 - 20)
        o += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="9" fill="{col}" opacity=".25" filter="url(#b6)"/>' + spark(x, y, rnd.choice([10, 14, 18]), col='#f4f8ff', op=.8)
    return o


def sparkles(lst, col='#fff6d6'):
    return ''.join(f'<circle cx="{x}" cy="{y}" r="{s * .7:.0f}" fill="{col}" opacity=".25" filter="url(#b6)"/>' + spark(x, y, s, col) for x, y, s in lst)


def clockface(cx, cy, R, hh, mm, face='#fbf3dc', rim='#c9952e', ink='#2a1a08', roman=False, glow=None):
    """round clock: rim, ticks, hands at hh:mm (no numerals text)."""
    o = ''
    if glow:
        o += f'<circle cx="{cx}" cy="{cy}" r="{R * 1.25:.0f}" fill="{glow}" opacity=".45" filter="url(#b24)"/>'
    o += f'<circle cx="{cx}" cy="{cy}" r="{R + R * .14:.0f}" fill="{rim}" stroke="{ink}" stroke-width="{max(4, R * .04):.0f}"/>'
    o += f'<circle cx="{cx}" cy="{cy}" r="{R + R * .05:.0f}" fill="none" stroke="#fff3c4" stroke-width="{R * .02 + 1:.1f}" opacity=".7"/>'
    o += f'<circle cx="{cx}" cy="{cy}" r="{R}" fill="{face}" stroke="{ink}" stroke-width="{max(3, R * .03):.0f}"/>'
    for k in range(60):
        a = math.radians(k * 6); big = k % 5 == 0
        r0 = R * (.80 if big else .88); r1 = R * .94
        o += f'<line x1="{cx + r0 * math.sin(a):.1f}" y1="{cy - r0 * math.cos(a):.1f}" x2="{cx + r1 * math.sin(a):.1f}" y2="{cy - r1 * math.cos(a):.1f}" stroke="{ink}" stroke-width="{R * (.035 if big else .012):.1f}" stroke-linecap="round"/>'
    for ang, L, wd in ((hh % 12 * 30 + mm * .5, .52, .06), (mm * 6, .78, .035)):
        a = math.radians(ang)
        o += f'<line x1="{cx - R * .1 * math.sin(a):.1f}" y1="{cy + R * .1 * math.cos(a):.1f}" x2="{cx + R * L * math.sin(a):.1f}" y2="{cy - R * L * math.cos(a):.1f}" stroke="{ink}" stroke-width="{R * wd:.1f}" stroke-linecap="round"/>'
    o += f'<circle cx="{cx}" cy="{cy}" r="{R * .06:.1f}" fill="{rim}" stroke="{ink}" stroke-width="{R * .02 + 1:.1f}"/>'
    o += f'<path d="M{cx - R * .62:.0f} {cy - R * .5:.0f} A{R * .8:.0f} {R * .8:.0f} 0 0 1 {cx + R * .2:.0f} {cy - R * .78:.0f}" fill="none" stroke="#fff" stroke-width="{R * .05:.1f}" opacity=".55" stroke-linecap="round"/>'
    return o


def write(here, bg, defs, body, lines, outline='#050b18', top=880):
    for f in ('common.css', 'Fredoka-700.woff2'):
        shutil.copy(os.path.join(REPO, 'tools', 'assets', 'thumb_v', f), here)
    open(os.path.join(here, 'A.html'), 'w').write(vpage(bg, vsvg(defs, body), lines, outline=outline, top=top))
    print('wrote', os.path.join(here, 'A.html'))
