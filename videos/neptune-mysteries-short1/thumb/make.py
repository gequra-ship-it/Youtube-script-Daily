# Shorts thumbnail A for neptune-mysteries-short1 (guideline 16-9; brief tools/briefs/thumb_art.md). Run: python3 videos/neptune-mysteries-short1/thumb/make.py
# A  WHY SO / BLUE?   intuitive: Neptune is a half-finished painting; frog painter (beret, palette) is still brushing on the deep blue,
#                     pale milky Uranus behind for contrast (S10-S12, S17-S18: methane alone cannot explain the lapis blue; "not even Neptune's color is fully explained")
import os, math, random
HERE = os.path.dirname(os.path.abspath(__file__))
LONG = os.path.join(HERE, '../../neptune-mysteries/thumb/make.py')   # shared helpers (frog, neptune, diamond) from the long-form thumbs
_src = open(LONG).read(); _g = {'__file__': LONG}; exec(_src[:_src.index('def thumb_A')], _g); globals().update({k: v for k, v in _g.items() if not k.startswith('__') and k != 'HERE'})

BERET = ('<path d="M-30 -84 q2 -24 40 -26 q38 4 34 22 q-30 10 -74 4z" fill="#b5413f" stroke-width="3.2"/>'
         '<path d="M8 -110 q2 -10 8 -12" fill="none" stroke-width="4"/><path d="M-22 -92 q22 -14 56 -6" fill="none" stroke="#d9655f" stroke-width="3" opacity=".7"/>')
PALETTE = ('<g transform="translate(-92 -38) rotate(-14)"><path d="M-42 0 q-4 -30 34 -34 q46 -2 50 26 q2 20 -22 24 q-14 0 -12 10 q2 12 -18 10 q-34 -4 -32 -36z" fill="#d7b98a" stroke-width="3.4"/>'
           '<circle cx="-22" cy="-14" r="8" fill="#123a9e" stroke-width="2.2"/><circle cx="0" cy="-22" r="8" fill="#2f6fe0" stroke-width="2.2"/>'
           '<circle cx="22" cy="-16" r="8" fill="#9fe3ee" stroke-width="2.2"/><circle cx="-26" cy="10" r="7" fill="#f4f1e6" stroke-width="2.2"/>'
           '<circle cx="2" cy="16" r="5" fill="#ffffff" stroke="none" opacity=".0"/></g>')


def make():
    random.seed(11)
    CX, CY, R = 1250, 540, 360
    d = FILTERS
    nd, nb = neptune(CX, CY, R, 'np', spot=True, light=(-.2, -.5))
    d += nd
    d += lin('bg', [(0, '#0b0a26'), (.6, '#141a4a'), (1, '#0a0c22')])
    d += rad('lamp', 1250, 520, 700, [(0, '#3a5cff', .28), (1, '#3a5cff', 0)])
    d += rad('ur', 1690, 150, 110, [(0, '#e6fbfb', 1), (.5, '#a9e4ea', 1), (1, '#5e9fa8', 1)])
    d += f'<clipPath id="pc"><circle cx="{CX}" cy="{CY}" r="{R}"/></clipPath>'
    b = '<rect width="1920" height="1080" fill="url(#bg)"/>' + starfield(170, seed=3, op=.6)
    b += '<rect width="1920" height="1080" fill="url(#lamp)"/>'
    # pale, milky Uranus far behind (contrast: "pale cyan hue of its twin")
    b += '<circle cx="1690" cy="150" r="70" fill="#dff6f4" opacity=".25" filter="url(#b24)"/>'
    b += '<circle cx="1690" cy="150" r="64" fill="url(#ur)"/><circle cx="1690" cy="150" r="64" fill="#ffffff" opacity=".28"/>'
    # Neptune (painted part)
    b += nb
    b += f'<circle cx="{CX}" cy="{CY}" r="{R}" fill="#2f7bff" opacity=".22" style="mix-blend-mode:screen"/>'
    # unpainted canvas on the left side with a brushy edge
    def xb(y):
        return 1015 + 26 * math.sin(y / 37.0) + 14 * math.sin(y / 13.0)
    pts = [(700, 120)] + [(xb(y), y) for y in range(140, 960, 12)] + [(700, 960)]
    poly = 'M' + ' L'.join(f'{x:.0f} {y:.0f}' for x, y in pts) + 'Z'
    b += f'<g clip-path="url(#pc)"><path d="{poly}" fill="#ece5d2"/>'
    for k in range(18):  # canvas weave
        y = 190 + k * 42
        b += f'<path d="M820 {y} L1060 {y + 8}" stroke="#cfc6ad" stroke-width="2" opacity=".55"/>'
    # pencil sketch of the bands on the canvas
    for y, w in ((330, 5), (470, 4), (620, 5), (760, 4)):
        b += f'<path d="M880 {y} q90 -14 160 -10" fill="none" stroke="#8d8672" stroke-width="{w}" stroke-dasharray="14 9" opacity=".7"/>'
    b += f'<ellipse cx="{CX - R * .18:.0f}" cy="{CY + R * .32:.0f}" rx="{R * .2:.0f}" ry="{R * .1:.0f}" fill="none" stroke="#8d8672" stroke-width="4" stroke-dasharray="12 8" opacity=".6" transform="rotate(-8 {CX} {CY})"/>'
    # wet brush strokes reaching into the canvas
    for y in range(160, 950, 22):
        x0 = xb(y); L = random.uniform(30, 90)
        col = random.choice(['#1f4bc2', '#2b5fd8', '#173a9e', '#3f78ea'])
        b += f'<path d="M{x0 + 30:.0f} {y} L{x0 - L:.0f} {y + random.uniform(-6, 6):.0f}" stroke="{col}" stroke-width="{random.uniform(26, 40):.0f}" stroke-linecap="round"/>'
        b += f'<path d="M{x0 + 20:.0f} {y - 7} L{x0 - L + 14:.0f} {y - 6:.0f}" stroke="#9cc4ff" stroke-width="4" stroke-linecap="round" opacity=".55"/>'
    b += '</g>'
    b += f'<circle cx="{CX}" cy="{CY}" r="{R}" fill="none" stroke="#0b0a26" stroke-width="3" opacity=".6"/>'
    # paint drips running off the bottom of the planet
    for x, L in ((1110, 70), (1180, 130), (1265, 95), (1340, 150), (1410, 60)):
        yb = CY + math.sqrt(max(0, R * R - (x - CX) ** 2)) - 6
        b += f'<path d="M{x - 13} {yb:.0f} L{x - 11} {yb + L:.0f} q11 18 22 0 L{x + 13} {yb:.0f}Z" fill="#1f4bc2" stroke="#0b1d6a" stroke-width="3"/>'
        b += f'<path d="M{x - 5} {yb + 8:.0f} L{x - 5} {yb + L - 6:.0f}" stroke="#8fb6ff" stroke-width="4" stroke-linecap="round" opacity=".7"/>'
        b += f'<ellipse cx="{x}" cy="{yb + L + 40:.0f}" rx="9" ry="12" fill="#2b5fd8" stroke="#0b1d6a" stroke-width="3"/>'
    # frog painter: beret, palette in left hand, big brush in right hand touching the wet edge
    FX, FY, S = 720, 985, 2.35
    hx, hy = FX + 88 * S, FY - 72 * S
    tx, ty = xb(560) + 8, 560
    ang = math.degrees(math.atan2(ty - hy, tx - hx))
    b += f'<ellipse cx="{FX + 10}" cy="{FY + 8}" rx="120" ry="16" fill="#000" opacity=".35" filter="url(#b6)"/>'
    b += frog(FX, FY, S, la='q-26 -4 -40 -22', ra='q30 -16 50 -50', mouth='o', look=(5, -4), hat=BERET, front=PALETTE)
    L = math.hypot(tx - hx, ty - hy)
    brush = f'<g transform="translate({hx - 30 * math.cos(math.radians(ang)):.0f} {hy - 30 * math.sin(math.radians(ang)):.0f}) rotate({ang:.1f})">'
    brush += f'<rect x="0" y="-8" width="{L - 40:.0f}" height="16" rx="8" fill="#a8683a" stroke="{INK}" stroke-width="4"/>'
    brush += f'<rect x="{L - 48:.0f}" y="-11" width="30" height="22" rx="3" fill="#c9ccd6" stroke="{INK}" stroke-width="4"/>'
    brush += f'<path d="M{L - 18:.0f} -12 q30 2 44 12 q-14 10 -44 12z" fill="#1f4bc2" stroke="{INK}" stroke-width="4" stroke-linejoin="round"/></g>'
    b += brush
    # redraw the right hand over the brush handle
    b += f'<circle cx="{hx:.0f}" cy="{hy:.0f}" r="{5.5 * S:.0f}" fill="{GREEN}" stroke="{INK}" stroke-width="{3 * S:.1f}"/>'
    # sparkles of fresh paint
    for x, y, s in ((1060, 520, 20), (1500, 300, 16), (1560, 760, 14), (1120, 250, 12)):
        b += spark(x, y, s)
    return page('#0b0a26', svg(d, b), [('WHY SO', 176, 'w'), ('BLUE?', 250, 'y')], outline='#070620')


open(os.path.join(HERE, 'A.html'), 'w').write(make())
print('wrote A')
