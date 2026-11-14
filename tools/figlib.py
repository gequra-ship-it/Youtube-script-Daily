# Channel-style PEOPLE and HANDS, pre-drawn (2026-11-05, miya: "agents draw people and hands badly; draw them in advance,
# one person + one hand first, then more after I confirm" -> confirmed round 7B: existing channel look, round palm, short
# chubby fingers, ONE thick outer outline and only thin lines between fingers, no joint lines, short straight thumb,
# thumb hidden on side fists / grips).
#
# Picture agents use these instead of drawing people or hands by hand (art_spec 6A/6B):
#
#   import sys; sys.path.insert(0, 'tools')          # run from the repo root
#   from figlib import person, hand, HAND_POSES, PERSON_POSES
#   svg += person(cx, base, H=70, pose='wave', skin=..., hair=..., shirt=..., pants=..., hair_style='long', face='smile', name='teacher')
#   svg += hand('point_up', x, y, size=36, side='R', rot=-20, skin=..., line=...)
#
# person: cx = body centre x, base = ground line y (sole of the shoes), H = head height px (figure = 5.5 H for 'cute' adults,
#         4.5 H for 'cute_child'). pose = one of PERSON_POSES (arms + hands + legs are set together, deterministic).
#         Each arm is a body.arm() link (mv-limb, animated gently by build3); hands are figlib hands.
# hand:   (x, y) = wrist, size = palm height px (a figure's hand is about 0.3 H), rot = finger direction in degrees
#         (0 = up, clockwise), side = which hand of the figure it is ('R' = the figure's right hand, which is on the VIEWER'S
#         LEFT when the figure faces us). The pose is drawn for its natural side and mirrored for the other one.
# Everything carries data-fig="person:<pose>" / data-fig="hand:<pose>" so tools/check/figcheck.py can see that people and hands
# came from here. Reference sheets: python3 tools/figlib.py <out_dir>  (people.svg/.png, hands.svg/.png).

import math, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import body

LINE = '#2e2218'
SKINS = {'light': '#f1c9a5', 'tan': '#d9a37a', 'olive': '#c9956a', 'brown': '#b97a55', 'dark': '#8a5a3a', 'deep': '#5c3a26'}
DEFAULT = dict(skin='#d9a37a', hair='#3a2a1e', shirt='#5f7a8a', pants='#2b2f3a', shoe='#1a1a1a')


def _darken(hexcol, f=.82):
    h = hexcol.lstrip('#'); r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
    return '#%02x%02x%02x' % (int(r * f), int(g * f), int(b * f))


# ---------------------------------------------------------------- hands (round 7B) ------------------------------------------
PALM_FRONT = 'M-16 -2 C-19 -10 -18 -22 -14 -28 C-6 -33 8 -33 15 -27 C18 -20 18 -10 15 -2 C9 4 -10 4 -16 -2 Z'
PALM_SIDE = 'M-12 -2 C-14 -10 -13 -24 -9 -30 C-4 -34 6 -34 9 -30 C11 -22 11 -10 9 -2 C6 3 -8 3 -12 -2 Z'
_KNUCKLES = [([(5, -31 + k * 8), (13, -30 + k * 8), (12, -25 + k * 8)], 8.5) for k in range(4)]
# coordinates: wrist at (0, 0), up = -y, palm about 30 tall, fingers 20-26 long, finger width 8-10 (units; size=30 -> 1 unit = 1 px).
# 'under' parts are drawn before the palm skin (finger bases blend into the palm), 'over' parts after it (a thumb lying across the palm).
HAND_POSES = {
    'open':       dict(under=[([(-11, -26), (-14, -48)], 9.5), ([(-3, -28), (-3, -54)], 9.5), ([(5, -27), (7, -49)], 9), ([(13, -22), (17, -40)], 8), ([(-14, -18), (-23, -29.5)], 9)],
                       palm=PALM_FRONT, over=[], lines='M-8 -16 Q0 -20 8 -16', natural='R', desc='open palm toward the viewer (stop, hello, showing)'),
    'fist':       dict(under=[([(-12, -26), (-12, -36)], 10), ([(-3, -28), (-3, -39)], 10), ([(6, -27), (6, -37)], 9.5), ([(14, -22), (14, -31)], 8.5)],
                       palm=PALM_FRONT, over=[([(-15, -16), (2, -20)], 9)], lines='M-8 -27 q3 -3 6 0 M1 -29 q3 -3 6 0 M9 -26 q3 -3 5 0', natural='R', desc='fist, knuckles toward the viewer'),
    'point_up':   dict(under=[([(-11, -26), (-13, -56)], 9.5), ([(-2, -28), (-2, -38)], 9.5), ([(6, -27), (6, -36)], 9), ([(13, -22), (13, -30)], 8)],
                       palm=PALM_FRONT, over=[([(-15, -16), (-1, -25.5)], 9)], lines='M0 -31 q3 -3 6 0 M8 -29 q3 -3 5 0', natural='R', desc='index finger up (idea, one, attention)'),
    'peace':      dict(under=[([(-10, -26), (-20, -52)], 9.5), ([(-2, -28), (2, -55)], 9.5), ([(7, -27), (7, -36)], 9), ([(14, -22), (14, -30)], 8)],
                       palm=PALM_FRONT, over=[([(-15, -16), (1, -24)], 9)], lines='M9 -31 q3 -3 5 0', natural='R', desc='two fingers (V, two, peace)'),
    'point_side': dict(under=[([(-2, -26), (28, -30)], 9.5)], palm='M-14 -2 C-16 -10 -15 -22 -11 -28 C-4 -33 6 -33 10 -27 C12 -20 12 -10 10 -2 C5 4 -9 4 -14 -2 Z',
                       over=[([(2, -20), (12, -19), (10, -11)], 8.5), ([(2, -12), (10, -11), (8, -5)], 8), ([(-8, -26), (0, -40)], 8.5)], lines='', natural='L', base=90, desc='index finger pointing sideways (away from the body)'),
    'side_up':    dict(under=[([(9, -24), (11, -46)], 8.5), ([(4, -27), (5, -52)], 9), ([(-2, -28), (-3, -54)], 9.5), ([(-8, -26), (-11, -50)], 9.5), ([(-10, -16), (-19, -28)], 9)],
                       palm='M-13 -2 C-15 -10 -14 -22 -11 -28 C-5 -33 6 -33 11 -27 C14 -20 14 -10 11 -2 C6 4 -8 4 -13 -2 Z',
                       over=[], lines='M-5 -14 Q1 -18 7 -14', natural='R', desc='raised palm, fingers together (wave, stop, oath)'),
    'hang':       dict(under=[([(11, 27), (12, 42), (7, 48)], 8), ([(4, 30), (5, 48), (-1, 55)], 9), ([(-4, 30), (-5, 50), (-12, 57)], 9.5), ([(-12, 30), (-14, 46), (-20, 52)], 9.5), ([(-13, 14), (-20, 31)], 9)],
                       palm='M-15 4 C-18 10 -18 24 -14 30 C-6 34 8 34 15 30 C18 24 18 10 15 4 C9 -2 -10 -2 -15 4 Z',
                       over=[], lines='M-8 12 q4 -3 8 0 M2 13 q4 -3 8 0', natural='L', down=True, desc='relaxed hanging hand (wrist at the top, fingers curl down)'),
    'cup':        dict(under=[([(15, -2), (30, -3), (38, -12)], 8), ([(16, -7), (33, -9), (42, -20)], 9), ([(16, -12), (34, -15), (44, -26)], 9.5), ([(16, -17), (32, -21), (40, -31)], 9.5), ([(-6, -18), (10, -27)], 9)],
                       palm='M-20 -6 C-22 -14 -14 -20 -2 -20 C10 -20 16 -16 18 -8 C19 0 14 4 4 4 C-6 4 -16 2 -20 -6 Z',
                       over=[], lines='M-8 -8 Q0 -4 8 -8', natural='L', desc='cupped palm up (offering, holding water, receiving)'),
    'claw':       dict(under=[([(-12, -26), (-18, -40), (-12, -50)], 9.5), ([(-3, -28), (-6, -44), (2, -54)], 9.5), ([(6, -27), (6, -42), (12, -50)], 9), ([(13, -22), (15, -34), (20, -40)], 8), ([(-14, -16), (-25, -26)], 9)],
                       palm=PALM_FRONT, over=[], lines='M-8 -26 q4 -3 8 0 M2 -27 q4 -3 8 0', natural='L', desc='grabbing from above (back of the hand, fingers curl in)'),
    'reach':      dict(under=[([(-6, -28), (-10, -50)], 9.5), ([(2, -30), (8, -54)], 9.5), ([(9, -26), (20, -46)], 9), ([(14, -20), (26, -34)], 8), ([(-14, -14), (-29, -19)], 9)],
                       palm='M-16 -2 C-18 -12 -14 -24 -8 -30 C0 -34 10 -32 16 -24 C19 -16 17 -8 14 -2 C8 4 -10 4 -16 -2 Z',
                       over=[], lines='M-8 -20 q4 -3 8 0 M2 -22 q4 -3 8 0', natural='L', desc='reaching, fingers spread (back of the hand)'),
    'fist_side':  dict(under=list(_KNUCKLES), palm=PALM_SIDE, over=[], lines='', natural='L', desc='fist from the side (knuckles outward, thumb hidden behind)'),
    'hold':       dict(under=list(_KNUCKLES), palm=PALM_SIDE, over=[], lines='', natural='L', desc='gripping a handle / stick (draw the object yourself: through the fist, behind the hand)'),
}
HAND_ALIASES = {'flat': 'open', 'wave': 'side_up', 'point': 'point_up', 'grip': 'hold', 'relaxed': 'hang', 'grab': 'claw'}


def _seg(pts, w, o, line, skin):
    d = 'M' + ' L'.join(f'{x} {y}' for x, y in pts)
    return (f'<path d="{d}" fill="none" stroke="{line}" stroke-width="{w + 2 * o:.2f}" stroke-linecap="round" stroke-linejoin="round"/>',
            f'<path d="{d}" fill="none" stroke="{line}" stroke-width="{w + .9 * o:.2f}" stroke-linecap="round" stroke-linejoin="round" opacity=".85"/>',
            f'<path d="{d}" fill="none" stroke="{skin}" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round"/>')


def hand(pose, x, y, size=30, side='R', rot=0, skin=DEFAULT['skin'], line=LINE, crease=None, gid=None, lw=2.5):
    """One channel-style hand. Layers: palm outline (thick) -> each finger: thick ink, thin ink, skin (near finger over the far one)
    -> palm skin without stroke (finger bases blend into the palm, no joint line) -> parts lying across the palm -> crease lines.
    size = palm height px; rot = finger direction (0 up, clockwise); side = figure's hand ('R' = viewer's left when facing us)."""
    pose = HAND_ALIASES.get(pose, pose)
    if pose not in HAND_POSES:
        raise ValueError(f'figlib.hand: unknown pose {pose!r}; use one of {sorted(HAND_POSES)}')
    P = HAND_POSES[pose]; s = size / 30.0; o = lw / s; crease = crease or _darken(skin)
    mirror = side.upper()[0] != P['natural']
    g = [f'<path d="{P["palm"]}" fill="{skin}" stroke="{line}" stroke-width="{2 * o:.2f}" stroke-linejoin="round"/>']
    for pts, w in P['under'] + P['over']:
        g.append(_seg(pts, w, o, line, skin)[0])
    for pts, w in P['under']:
        a, b, c = _seg(pts, w, o, line, skin); g += [b, c]
    g.append(f'<path d="{P["palm"]}" fill="{skin}" stroke="none"/>')
    for pts, w in P['over']:
        a, b, c = _seg(pts, w, o, line, skin); g += [b, c]
    if P.get('lines'):
        g.append(f'<path d="{P["lines"]}" fill="none" stroke="{crease}" stroke-width="{.65 * o:.2f}" stroke-linecap="round" opacity=".8"/>')
    m = ' scale(-1 1)' if mirror else ''
    idt = f' id="{gid}"' if gid else ''
    return (f'<g{idt} data-fig="hand:{pose}" transform="translate({x:.1f} {y:.1f}) rotate({rot:.1f}) scale({s:.3f}){m}">'
            + ''.join(g) + '</g>')


# ---------------------------------------------------------------- people ---------------------------------------------------
# arms: (upper, bend, bend_dir, hand pose) for the figure's RIGHT arm (viewer's left) and LEFT arm (viewer's right); body.arm angles.
_HANG_R, _HANG_L = (-10, 10, 1, 'hang'), (10, 10, -1, 'hang')
PERSON_POSES = {
    'stand':      dict(R=_HANG_R, L=_HANG_L, desc='standing, arms hanging'),
    'walk':       dict(R=(-25, 15, 1, 'hang'), L=(20, 20, -1, 'hang'), legs='walk', desc='walking (legs apart, arms swing)'),
    'wave':       dict(R=(-125, 55, 1, 'side_up'), L=_HANG_L, desc='waving / greeting with the raised right hand'),
    'point_side': dict(R=_HANG_R, L=(95, 10, -1, 'point_side'), desc='pointing sideways (to the viewer\'s right) with the left arm'),
    'point_up':   dict(R=_HANG_R, L=(150, 30, -1, 'point_up'), desc='index finger raised (idea, attention)'),
    'cheer':      dict(R=(-150, 25, 1, 'open'), L=(150, 25, -1, 'open'), desc='both arms up, open palms (joy, victory)'),
    'think':      dict(R=_HANG_R, L=(25, 120, -1, 'fist'), desc='hand at the chin (thinking)'),
    'offer':      dict(R=(-35, 95, 1, 'cup'), L=(35, 95, -1, 'cup'), desc='both hands cupped forward (offering, holding, receiving)'),
    'reach':      dict(R=_HANG_R, L=(110, 15, -1, 'reach'), desc='reaching out sideways, fingers spread'),
    'peace':      dict(R=_HANG_R, L=(140, 50, -1, 'peace'), desc='V sign raised'),
    'hips':       dict(R=(-45, 110, 1, 'fist'), L=(45, 110, -1, 'fist'), desc='hands on the hips'),
    'grab':       dict(R=_HANG_R, L=(100, 35, -1, 'claw'), desc='grabbing something from above with the left hand'),
    'hold':       dict(R=_HANG_R, L=(60, 75, -1, 'hold'), desc='holding a stick / handle in the left fist (draw the object through the fist)'),
    'shrug':      dict(R=(-60, 110, 1, 'open'), L=(60, 110, -1, 'open'), desc='shrug, palms up and out'),
}
HAIR_STYLES = ('cap', 'long', 'bun', 'curly', 'bald', 'ponytail')
FACES = ('smile', 'calm', 'surprise', 'sad', 'laugh')


def person(cx, base, H=70, pose='stand', kind='cute', skin=DEFAULT['skin'], hair=DEFAULT['hair'], shirt=DEFAULT['shirt'],
           pants=DEFAULT['pants'], shoe=DEFAULT['shoe'], hair_style='cap', face='smile', name='person', line=LINE, flip=False):
    """A whole standing figure in the channel style (round head, oval eyes with a highlight, straight brows, cheeks, flat hair cap,
    rounded shirt, straight trousers); arms from body.arm (one mv-limb link each) with figlib hands. flip=True mirrors the whole
    figure (then its left arm is on the viewer's left)."""
    if pose not in PERSON_POSES:
        raise ValueError(f'figlib.person: unknown pose {pose!r}; use one of {sorted(PERSON_POSES)}')
    PP = PERSON_POSES[pose]; n = body.P[kind]['height']
    top = base - n * H; hy = top + H * .5                      # head centre
    sw = 1.4 * H; ty = top + H * 1.15; tb = base - (n / 2) * H  # torso top / bottom (hip at mid-height)
    lw = max(1.6, H * .036)
    g = [f'<g id="{name}" data-fig="person:{pose}" stroke="{line}" stroke-width="{lw:.2f}" stroke-linejoin="round"'
         + (f' transform="translate({2 * cx:.1f} 0) scale(-1 1)"' if flip else '') + '>']
    g.append(f'<ellipse cx="{cx}" cy="{base + 2}" rx="{sw * .9:.0f}" ry="6" fill="{line}" opacity=".12" stroke="none"/>')
    # legs + shoes
    for sgn in (-1, 1):
        lx = cx + sgn * H * .3; dx = sgn * H * .12 if PP.get('legs') == 'walk' else 0
        g.append(f'<path d="M{lx - H * .22:.0f} {tb:.0f} L{lx + H * .22:.0f} {tb:.0f} L{lx + dx + H * .2:.0f} {base - 8:.0f} L{lx + dx - H * .2:.0f} {base - 8:.0f} Z" fill="{pants}"/>')
        g.append(f'<path d="M{lx + dx - H * .24:.0f} {base - 9:.0f} L{lx + dx + H * .26:.0f} {base - 9:.0f} Q{lx + dx + H * .34:.0f} {base - 4:.0f} {lx + dx + H * .26:.0f} {base:.0f} L{lx + dx - H * .24:.0f} {base:.0f} Z" fill="{shoe}"/>')
    # torso
    g.append(f'<path d="M{cx - sw / 2:.0f} {ty + H * .3:.0f} Q{cx - sw / 2:.0f} {ty:.0f} {cx - sw / 2 + H * .3:.0f} {ty:.0f} L{cx + sw / 2 - H * .3:.0f} {ty:.0f} Q{cx + sw / 2:.0f} {ty:.0f} {cx + sw / 2:.0f} {ty + H * .3:.0f} L{cx + sw / 2 - H * .08:.0f} {tb:.0f} L{cx - sw / 2 + H * .08:.0f} {tb:.0f} Z" fill="{shirt}"/>')
    # neck + head
    g.append(f'<rect x="{cx - H * .13:.0f}" y="{hy + H * .35:.0f}" width="{H * .26:.0f}" height="{H * .35:.0f}" fill="{skin}" stroke-width="{lw * .85:.2f}"/>')
    if hair_style in ('long',):   # hair behind the head
        g.append(f'<path d="M{cx - H * .58:.0f} {hy - H * .1:.0f} L{cx - H * .62:.0f} {hy + H * .75:.0f} Q{cx} {hy + H * .9:.0f} {cx + H * .62:.0f} {hy + H * .75:.0f} L{cx + H * .58:.0f} {hy - H * .1:.0f} Z" fill="{hair}" stroke-width="{lw * .85:.2f}"/>')
    if hair_style == 'ponytail':
        g.append(f'<path d="M{cx + H * .4:.0f} {hy - H * .2:.0f} Q{cx + H * .95:.0f} {hy - H * .1:.0f} {cx + H * .7:.0f} {hy + H * .55:.0f} Q{cx + H * .55:.0f} {hy + H * .2:.0f} {cx + H * .4:.0f} {hy - H * .2:.0f} Z" fill="{hair}" stroke-width="{lw * .85:.2f}"/>')
    g.append(f'<ellipse cx="{cx}" cy="{hy:.0f}" rx="{H * .54:.0f}" ry="{H * .5:.0f}" fill="{skin}"/>')
    g.append(f'<ellipse cx="{cx - H * .54:.0f}" cy="{hy + H * .06:.0f}" rx="{H * .08:.0f}" ry="{H * .11:.0f}" fill="{skin}" stroke-width="{lw * .85:.2f}"/>'
             f'<ellipse cx="{cx + H * .54:.0f}" cy="{hy + H * .06:.0f}" rx="{H * .08:.0f}" ry="{H * .11:.0f}" fill="{skin}" stroke-width="{lw * .85:.2f}"/>')
    browy = -.16 if face != 'surprise' else -.21
    for sgn in (-1, 1):
        ex = cx + sgn * H * .19; ey = hy + H * .04
        g.append(f'<ellipse cx="{ex:.0f}" cy="{ey:.0f}" rx="{H * .105:.1f}" ry="{H * .12:.1f}" fill="#fbfaf2" stroke-width="{lw * .72:.2f}"/>'
                 f'<circle cx="{ex - H * .045:.1f}" cy="{ey + H * .03:.1f}" r="{H * .06:.1f}" fill="#1a120c" stroke="none"/>'
                 f'<circle cx="{ex - H * .025:.1f}" cy="{ey + H * .005:.1f}" r="{H * .02:.1f}" fill="#fff" stroke="none"/>')
        if face == 'sad':
            g.append(f'<path d="M{ex - sgn * H * .09:.0f} {ey + H * (browy + .04):.0f} L{ex + sgn * H * .09:.0f} {ey + H * browy:.0f}" stroke-linecap="round"/>')
        else:
            g.append(f'<path d="M{ex - H * .09:.0f} {ey + H * browy:.0f} L{ex + H * .09:.0f} {ey + H * browy:.0f}" stroke-linecap="round"/>')
        g.append(f'<ellipse cx="{cx + sgn * H * .23:.0f}" cy="{hy + H * .22:.0f}" rx="{H * .08:.0f}" ry="{H * .045:.0f}" fill="#ef7f74" opacity=".45" stroke="none"/>')
    my = hy + H * .28
    if face == 'smile':
        g.append(f'<path d="M{cx - H * .11:.0f} {my:.0f} Q{cx} {hy + H * .4:.0f} {cx + H * .11:.0f} {my:.0f}" fill="none" stroke-width="{lw * .9:.2f}" stroke-linecap="round"/>')
    elif face == 'calm':
        g.append(f'<path d="M{cx - H * .09:.0f} {my + H * .04:.0f} L{cx + H * .09:.0f} {my + H * .04:.0f}" fill="none" stroke-width="{lw * .9:.2f}" stroke-linecap="round"/>')
    elif face == 'surprise':
        g.append(f'<ellipse cx="{cx}" cy="{my + H * .06:.0f}" rx="{H * .06:.0f}" ry="{H * .08:.0f}" fill="#7a3b3b" stroke-width="{lw * .9:.2f}"/>')
    elif face == 'sad':
        g.append(f'<path d="M{cx - H * .1:.0f} {my + H * .08:.0f} Q{cx} {my - H * .02:.0f} {cx + H * .1:.0f} {my + H * .08:.0f}" fill="none" stroke-width="{lw * .9:.2f}" stroke-linecap="round"/>')
    elif face == 'laugh':
        g.append(f'<path d="M{cx - H * .12:.0f} {my:.0f} Q{cx} {my + H * .22:.0f} {cx + H * .12:.0f} {my:.0f} Z" fill="#7a3b3b" stroke-width="{lw * .9:.2f}" stroke-linejoin="round"/>')
    # hair
    cap = (f'M{cx - H * .55:.0f} {hy + H * .05:.0f} Q{cx - H * .57:.0f} {hy - H * .6:.0f} {cx} {hy - H * .55:.0f} Q{cx + H * .57:.0f} {hy - H * .6:.0f} {cx + H * .55:.0f} {hy + H * .05:.0f} '
           f'Q{cx + H * .48:.0f} {hy - H * .22:.0f} {cx + H * .3:.0f} {hy - H * .08:.0f} Q{cx + H * .1:.0f} {hy:.0f} {cx - H * .03:.0f} {hy - H * .16:.0f} Q{cx - H * .22:.0f} {hy - H * .03:.0f} {cx - H * .43:.0f} {hy + H * .02:.0f} Z')
    if hair_style == 'bald':
        g.append(f'<path d="M{cx - H * .5:.0f} {hy - H * .15:.0f} Q{cx - H * .45:.0f} {hy - H * .4:.0f} {cx - H * .25:.0f} {hy - H * .42:.0f}" fill="none" stroke="{hair}" stroke-width="{lw * 1.6:.2f}" stroke-linecap="round"/>')
    elif hair_style == 'curly':
        g.append(f'<path d="{cap}" fill="{hair}" stroke-width="{lw * .85:.2f}"/>')
        for k in range(5):
            a = -150 + k * 30; rx = cx + math.cos(math.radians(a)) * H * .5; ry = hy - H * .02 + math.sin(math.radians(a)) * H * .5
            g.append(f'<circle cx="{rx:.0f}" cy="{ry:.0f}" r="{H * .12:.0f}" fill="{hair}" stroke-width="{lw * .85:.2f}"/>')
    else:
        g.append(f'<path d="{cap}" fill="{hair}" stroke-width="{lw * .85:.2f}"/>')
        if hair_style == 'bun':
            g.append(f'<circle cx="{cx + H * .12:.0f}" cy="{hy - H * .6:.0f}" r="{H * .16:.0f}" fill="{hair}" stroke-width="{lw * .85:.2f}"/>')
    g.append(f'<path d="M{cx - H * .27:.0f} {hy - H * .38:.0f} q{H * .16:.0f} -{H * .1:.0f} {H * .32:.0f} -{H * .05:.0f}" fill="none" stroke="#fff" stroke-width="{lw * .85:.2f}" opacity=".35" stroke-linecap="round"/>')
    # arms (body.arm links) with figlib hands; the figure's right arm is on the viewer's left
    sh = ty + H * .25; hs = body.P[kind]['palm'] * H * 1.05
    def mk(side):
        upper, bend, bdir, hp = PP[side]
        def fn(x, y, ang):
            HP = HAND_POSES[hp]; base = HP.get('base', 0) * (1 if side == HP['natural'] else -1)   # finger direction of the drawn pose
            rot = ang - 180 if HP.get('down') else ang - base
            return hand(hp, x, y, hs, side=side, rot=rot, skin=skin, line=line, lw=lw)
        sx = cx - sw / 2 + H * .12 if side == 'R' else cx + sw / 2 - H * .12
        a = body.arm(sx, sh, H, upper=upper, bend=bend, bend_dir=bdir, name=f'{name}-arm-{side.lower()}', side=side,
                     sleeve=shirt, skin=skin, line=line, kind=kind, lw=lw, hand_fn=fn)
        if bend >= 60:   # a deliberate fold (hand at the chin, on the hip, cupped forward): tools/fix/armfix.py leaves marked arms alone
            a = a.replace('<g class="mv mv-limb-', '<g data-armfixed="1" class="mv mv-limb-', 1)
        return a
    g.append(mk('R')); g.append(mk('L'))
    g.append('</g>')
    return ''.join(g)


def sheets(out_dir):
    """reference sheets: people.svg (14 poses x adult/child, hair styles, faces, skins) and hands.svg (12 poses, right + left)."""
    os.makedirs(out_dir, exist_ok=True)
    BG = '#efe6d6'
    # hands
    W, H_ = 1500, 700; cells = []
    for i, k in enumerate(HAND_POSES):
        cx = (i % 6) * 250 + 125
        for r, side in enumerate(('R', 'L')):
            cy = (i // 6) * 350 + 230 + r * 0  # both hands in one cell, side by side
            cells.append(hand(k, cx - 50 + r * 100, cy if not HAND_POSES[k].get('down') else cy - 110, 48, side=side))
        cells.append(f'<text x="{cx}" y="{(i // 6) * 350 + 300}" font-family="sans-serif" font-size="15" fill="#555" text-anchor="middle">{k}  (R / L)</text>')
    hands_svg = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H_}" width="{W}" height="{H_}"><rect width="{W}" height="{H_}" fill="{BG}"/>' + ''.join(cells) + '</svg>'
    open(os.path.join(out_dir, 'hands.svg'), 'w').write(hands_svg)
    # people
    W, H_ = 2000, 1500; cells = []; H = 56
    poses = list(PERSON_POSES)
    for i, k in enumerate(poses):
        cx = (i % 7) * 285 + 142; base = (i // 7) * 480 + 420
        cells.append(person(cx, base, H, pose=k, name=f'p{i}'))
        cells.append(f'<text x="{cx}" y="{base + 30}" font-family="sans-serif" font-size="16" fill="#555" text-anchor="middle">{k}</text>')
    variants = [dict(kind='cute_child', hair_style='curly', face='laugh', skin=SKINS['brown'], shirt='#c86b4a'),
                dict(hair_style='long', face='calm', skin=SKINS['light'], shirt='#7a5aa8', hair='#8a4a2a'),
                dict(hair_style='bun', face='surprise', skin=SKINS['olive'], shirt='#3f8a6a'),
                dict(hair_style='bald', face='sad', skin=SKINS['dark'], shirt='#8a6a3f'),
                dict(hair_style='ponytail', face='smile', skin=SKINS['deep'], shirt='#b84a6a', hair='#1a1210'),
                dict(hair_style='cap', face='calm', skin=SKINS['tan'], shirt='#4a6ab8', flip=True, pose='point_side'),
                dict(kind='cute_child', hair_style='ponytail', face='smile', skin=SKINS['light'], shirt='#d8a63a', pose='cheer')]
    for i, v in enumerate(variants):
        cx = i * 285 + 142; base = 2 * 480 + 420
        cells.append(person(cx, base, H, pose=v.pop('pose', 'stand'), name=f'v{i}', **v))
        cells.append(f'<text x="{cx}" y="{base + 30}" font-family="sans-serif" font-size="16" fill="#555" text-anchor="middle">{v.get("kind", "cute")} / {v["hair_style"]} / {v["face"]}</text>')
    people_svg = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H_}" width="{W}" height="{H_}"><rect width="{W}" height="{H_}" fill="{BG}"/>' + ''.join(cells) + '</svg>'
    open(os.path.join(out_dir, 'people.svg'), 'w').write(people_svg)
    try:
        from paths import chrome
        from playwright.sync_api import sync_playwright
        with sync_playwright() as p:
            b = p.chromium.launch(executable_path=chrome(), args=['--no-sandbox'])
            for nm, svg, (w, h) in (('hands', hands_svg, (1500, 700)), ('people', people_svg, (2000, 1500))):
                pg = b.new_page(viewport={'width': w, 'height': h}, device_scale_factor=1)
                pg.set_content('<body style="margin:0">' + svg + '</body>'); pg.screenshot(path=os.path.join(out_dir, nm + '.png')); pg.close()
            b.close()
    except Exception as e:   # png is optional (needs playwright + chrome)
        print('png skipped:', e)
    return out_dir


if __name__ == '__main__':
    print(sheets(sys.argv[1] if len(sys.argv) > 1 else '/tmp/figlib_sheets'))
