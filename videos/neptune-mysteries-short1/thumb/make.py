# Shorts thumbnail A for neptune-mysteries-short1 (guideline 16-9: vertical 1080x1920, centred text; brief tools/briefs/thumb_art.md).
# Run: python3 videos/neptune-mysteries-short1/thumb/make.py
# A  WHY SO / BLUE?   intuitive: Neptune (top) is a half-finished painting, its left side still bare canvas with pencil bands; text in the middle;
#                     the frog painter (beret, palette) stands on a paint can below, wet blue brush raised, pale milky Uranus behind for contrast
#                     (S10-S12, S17-S18: methane alone cannot explain the lapis blue; "not even Neptune's color is fully explained")
import os, sys, math, random
HERE = os.path.dirname(os.path.abspath(__file__))
LONG = os.path.join(HERE, '../../neptune-mysteries/thumb/make.py')   # shared helpers (frog, neptune, diamond, starfield) from the long-form thumbs
_src = open(LONG).read(); _g = {'__file__': LONG}; exec(_src[:_src.index('def thumb_A')], _g); globals().update({k: v for k, v in _g.items() if not k.startswith('__') and k != 'HERE'})
from thumb_lib import vpage, vsvg, blobs

BERET = ('<path d="M-30 -84 q2 -24 40 -26 q38 4 34 22 q-30 10 -74 4z" fill="#b5413f" stroke-width="3.2"/>'
         '<path d="M8 -110 q2 -10 8 -12" fill="none" stroke-width="4"/><path d="M-22 -92 q22 -14 56 -6" fill="none" stroke="#d9655f" stroke-width="3" opacity=".7"/>')
PALETTE = ('<g transform="translate(-74 -30) rotate(-14)"><path d="M-42 0 q-4 -30 34 -34 q46 -2 50 26 q2 20 -22 24 q-14 0 -12 10 q2 12 -18 10 q-34 -4 -32 -36z" fill="#d7b98a" stroke-width="3.4"/>'
           '<circle cx="-22" cy="-14" r="8" fill="#123a9e" stroke-width="2.2"/><circle cx="0" cy="-22" r="8" fill="#2f6fe0" stroke-width="2.2"/>'
           '<circle cx="22" cy="-16" r="8" fill="#9fe3ee" stroke-width="2.2"/><circle cx="-26" cy="10" r="7" fill="#f4f1e6" stroke-width="2.2"/></g>')


def make():
    random.seed(11)
    CX, CY, R = 560, 520, 335
    d = FILTERS
    nd, nb = neptune(CX, CY, R, 'np', spot=True, light=(-.2, -.5))
    d += nd
    d += lin('bg', [(0, '#0b0a26'), (.5, '#141a4a'), (1, '#0a0c22')])
    d += rad('lamp', CX, CY, 760, [(0, '#3a5cff', .32), (1, '#3a5cff', 0)])
    d += rad('ur', 860, 1440, 130, [(0, '#e6fbfb', 1), (.5, '#a9e4ea', 1), (1, '#5e9fa8', 1)])
    d += rad('floor', 540, 1800, 620, [(0, '#2a4fd0', .35), (1, '#2a4fd0', 0)])
    d += f'<clipPath id="pc"><circle cx="{CX}" cy="{CY}" r="{R}"/></clipPath>'
    b = '<rect width="1080" height="1920" fill="url(#bg)"/>' + starfield(230, x1=1080, y1=1920, seed=3, op=.6)
    b += '<rect width="1080" height="1920" fill="url(#lamp)"/><rect width="1080" height="1920" fill="url(#floor)"/>'
    # pale, milky Uranus lower right (contrast: "pale cyan hue of its twin")
    UX, UY, UR = 860, 1440, 120
    b += f'<circle cx="{UX}" cy="{UY}" r="{UR + 14}" fill="#dff6f4" opacity=".25" filter="url(#b24)"/>'
    b += f'<circle cx="{UX}" cy="{UY}" r="{UR}" fill="url(#ur)"/><circle cx="{UX}" cy="{UY}" r="{UR}" fill="#ffffff" opacity=".28"/>'
    b += f'<ellipse cx="{UX}" cy="{UY}" rx="{UR * 1.5:.0f}" ry="{UR * .22:.0f}" fill="none" stroke="#dff6f4" stroke-width="3" opacity=".35" transform="rotate(-70 {UX} {UY})"/>'
    # Neptune (painted part)
    b += nb
    b += f'<circle cx="{CX}" cy="{CY}" r="{R}" fill="#2f7bff" opacity=".22" style="mix-blend-mode:screen"/>'
    # unpainted canvas on the left side with a brushy edge
    def xb(y):
        return 470 + 26 * math.sin(y / 37.0) + 14 * math.sin(y / 13.0)
    pts = [(150, 120)] + [(xb(y), y) for y in range(160, 880, 12)] + [(150, 900)]
    pl = 'M' + ' L'.join(f'{x:.0f} {y:.0f}' for x, y in pts) + 'Z'
    b += f'<g clip-path="url(#pc)"><path d="{pl}" fill="#ece5d2"/>'
    for k in range(17):  # canvas weave
        y = 200 + k * 40
        b += f'<path d="M220 {y} L520 {y + 8}" stroke="#cfc6ad" stroke-width="2" opacity=".55"/>'
    for y, w in ((330, 5), (450, 4), (590, 5), (720, 4)):  # pencil sketch of the bands
        b += f'<path d="M250 {y} q100 -14 200 -10" fill="none" stroke="#8d8672" stroke-width="{w}" stroke-dasharray="14 9" opacity=".7"/>'
    for y in range(190, 870, 22):  # wet brush strokes reaching into the canvas
        x0 = xb(y); L = random.uniform(30, 90)
        col = random.choice(['#1f4bc2', '#2b5fd8', '#173a9e', '#3f78ea'])
        b += f'<path d="M{x0 + 30:.0f} {y} L{x0 - L:.0f} {y + random.uniform(-6, 6):.0f}" stroke="{col}" stroke-width="{random.uniform(26, 40):.0f}" stroke-linecap="round"/>'
        b += f'<path d="M{x0 + 20:.0f} {y - 7} L{x0 - L + 14:.0f} {y - 6:.0f}" stroke="#9cc4ff" stroke-width="4" stroke-linecap="round" opacity=".55"/>'
    b += '</g>'
    b += f'<circle cx="{CX}" cy="{CY}" r="{R}" fill="none" stroke="#0b0a26" stroke-width="3" opacity=".6"/>'
    # short paint drips off the bottom of the painted part
    for x, L in ((760, 46), (820, 60), (870, 34)):
        yb = CY + math.sqrt(max(0, R * R - (x - CX) ** 2)) - 6
        b += f'<path d="M{x - 12} {yb:.0f} L{x - 10} {yb + L:.0f} q10 16 20 0 L{x + 12} {yb:.0f}Z" fill="#1f4bc2" stroke="#0b1d6a" stroke-width="3"/>'
        b += f'<path d="M{x - 4} {yb + 8:.0f} L{x - 4} {yb + L - 6:.0f}" stroke="#8fb6ff" stroke-width="4" stroke-linecap="round" opacity=".7"/>'
    for x, y, s in ((470, 240, 18), (880, 300, 20), (950, 760, 14), (140, 820, 14)):
        b += spark(x, y, s)
    # paint can + blue splats on the floor
    FX, FY, S = 400, 1660, 2.5
    for x, y, rx in ((300, 1736, 70), (640, 1750, 46), (520, 1770, 30)):
        b += f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{rx * .28:.0f}" fill="#1f4bc2" stroke="#0b1d6a" stroke-width="3"/>'
    b += f'<ellipse cx="{FX + 10}" cy="{FY + 150}" rx="190" ry="22" fill="#000" opacity=".4" filter="url(#b6)"/>'
    b += f'<path d="M{FX - 110} {FY + 6} L{FX - 96} {FY + 146} q106 22 212 0 L{FX + 130} {FY + 6}Z" fill="#c9ccd6" stroke="{INK}" stroke-width="6"/>'
    b += f'<ellipse cx="{FX + 10}" cy="{FY + 6}" rx="120" ry="22" fill="#1f4bc2" stroke="{INK}" stroke-width="6"/>'
    b += f'<path d="M{FX - 70} {FY + 10} q40 8 70 -2" fill="none" stroke="#8fb6ff" stroke-width="6" stroke-linecap="round" opacity=".7"/>'
    b += f'<path d="M{FX + 80} {FY + 14} L{FX + 82} {FY + 70} q10 14 18 0 L{FX + 104} {FY + 10}Z" fill="#1f4bc2" stroke="#0b1d6a" stroke-width="3"/>'
    b += f'<path d="M{FX - 84} {FY + 70} L{FX + 104} {FY + 70}" stroke="#9aa0b0" stroke-width="5"/>'
    # frog painter: palette in left hand, brush raised in right hand toward Neptune
    hx, hy = FX + (38 + 36) * S, FY - (22 + 50) * S
    b += frog(FX, FY, S, la='q-26 -4 -40 -12', ra='q24 -26 36 -50', mouth='o', look=(4, -6), hat=BERET, front=PALETTE)
    ang = -34
    L = 200
    c, s_ = math.cos(math.radians(ang)), math.sin(math.radians(ang))
    br = f'<g transform="translate({hx - 40 * c:.0f} {hy - 40 * s_:.0f}) rotate({ang})">'
    br += f'<rect x="0" y="-9" width="{L - 40}" height="18" rx="9" fill="#a8683a" stroke="{INK}" stroke-width="4"/>'
    br += f'<rect x="{L - 48}" y="-12" width="32" height="24" rx="3" fill="#c9ccd6" stroke="{INK}" stroke-width="4"/>'
    br += f'<path d="M{L - 18} -13 q34 2 50 13 q-16 11 -50 13z" fill="#1f4bc2" stroke="{INK}" stroke-width="4" stroke-linejoin="round"/></g>'
    b += br
    tipx, tipy = hx - 40 * c + (L + 30) * c, hy - 40 * s_ + (L + 30) * s_
    for k in range(3):  # drops flicking off the brush
        b += f'<ellipse cx="{tipx + 20 + k * 18:.0f}" cy="{tipy + 26 + k * 30:.0f}" rx="7" ry="9" fill="#2b5fd8" stroke="#0b1d6a" stroke-width="2.5"/>'
    b += f'<circle cx="{hx:.0f}" cy="{hy:.0f}" r="{5.5 * S:.0f}" fill="{GREEN}" stroke="{INK}" stroke-width="{3 * S:.1f}"/>'
    return vpage('#0b0a26', vsvg(d, b), [('WHY SO', 190, 'w'), ('BLUE?', 290, 'y')], outline='#070620', top=810)


open(os.path.join(HERE, 'A.html'), 'w').write(make())
print('wrote A')
