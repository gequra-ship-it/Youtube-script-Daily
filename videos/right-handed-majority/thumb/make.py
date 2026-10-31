# Thumbnails A-C for right-handed-majority, round 2 (guideline 16-6 / 16-8, brief tools/briefs/thumb_art.md).
# Owner on round 1 (hands only): "only hands appear, so I can't tell intuitively what it means" -> every picture is a SCENE with
# whole characters and readable faces; hands are only small round props (art_spec 6A/6B, tools/body.py arms).
# A  ONLY 1 IN 10        intuitive: a classroom, nine kids write with the right hand, ONE kid writes with the left hand in a gold
#                        spotlight; chalkboard pie 90/10 (S03-S04 "nine out of ten", "roughly ten percent"). Frog = classmate staring.
# B  LEFTIES FIGHT BETTER?  homage: Kill Bill (House of Blue Leaves: one fighter in a yellow track suit against a crowd of masked
#                        fighters in black suits, glowing checkered floor); the lone fighter holds the sword in the LEFT hand, the
#                        nine masked fighters in the right (S42-S51 fighting hypothesis, southpaws overrepresented; hedged with "?").
#                        Frog = a small masked fighter in the crowd, sweating.
# C  RIGHT-HANDED SINCE THE STONE AGE  intuitive: firelit cave, a painter blows ochre over a hand pressed on the wall full of stencils,
#                        a child and an elder watch by the fire (S05-S07 cave stencils, "the right-hand habit ... is ancient").
#                        Frog in a fur pelt with a torch.
import os, sys, math, random
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', '..', 'tools'))
from thumb_lib import page, svg, lin, rad, spark
from hands import hand
from body import arm as body_arm, P, shoulders

INK = '#1d2b1c'; GREEN = '#6aa55a'; DARKG = '#4d8a4a'; BELLY = '#9cc98a'
BODY = 'M-34 0 q-6 -64 34 -70 q40 -2 42 62 q0 10 -6 12 q-36 6 -70 -4z'
FILTERS = '<clipPath id="fbody"><path d="%s"/></clipPath>' % BODY + ''.join(
    f'<filter id="b{n}" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="{n}"/></filter>' for n in (2, 4, 8, 16, 32, 60))
LINE = '#22160f'


def limb(d, w=7.5, wi=3.4, col=GREEN):
    return f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="{w}"/><path d="{d}" fill="none" stroke="{col}" stroke-width="{wi}"/>'


def end_of(d):
    n = [float(v) for v in d.replace('M', ' ').replace('q', ' ').split()]
    return n[0] + n[-2], n[1] + n[-1]


# ---------------- mascot frog (tools/assets/frog.svg body), posable; feet at y=0, ~100 units tall ----------------
def frog(x, y, s, flip=False, look=(0, 0), mouth='O', armL=None, armR=None, back='', mid='', top='', front='', shadow=True, hands=('', '')):
    sx = -s if flip else s
    g = [f'<g transform="translate({x} {y}) scale({sx} {s})" stroke="{INK}" stroke-linejoin="round" stroke-linecap="round">']
    if shadow:
        g.append('<ellipse cx="0" cy="6" rx="56" ry="9" fill="#000" opacity=".35" stroke="none"/>')
    g.append(back)
    for fx in (-22, 22):
        g.append(f'<ellipse cx="{fx}" cy="4" rx="16" ry="9" fill="{DARKG}" stroke-width="3.2"/>')
    g.append(f'<path d="{BODY}" fill="{GREEN}" stroke-width="4"/>')
    g.append(f'<ellipse cx="2" cy="-12" rx="22" ry="20" fill="{BELLY}" stroke="none" opacity=".7"/>')
    g.append('<path d="M-24 -50 q6 -14 18 -16" fill="none" stroke="#b6dea0" stroke-width="3" opacity=".8"/>')
    g.append(mid)
    lx, ly = look
    for ex in (-10, 22):
        g.append(f'<circle cx="{ex}" cy="-66" r="13.5" fill="#f4f5ea" stroke-width="3.2"/>')
        g.append(f'<circle cx="{ex + 1 + lx}" cy="{-66 + ly}" r="4.4" fill="{INK}" stroke="none"/>')
        g.append(f'<circle cx="{ex + 2.4 + lx}" cy="{-67.6 + ly}" r="1.5" fill="#fff" stroke="none"/>')
    g.append('<path d="M-22 -88 q12 -9 24 -1 M10 -89 q12 -8 24 1" fill="none" stroke-width="3.4"/>')
    if mouth == 'O':
        g.append('<ellipse cx="6" cy="-38" rx="10" ry="12" fill="#7a2f33" stroke-width="3"/><ellipse cx="6" cy="-31" rx="6" ry="4" fill="#e07b7b" stroke="none"/>')
    else:
        g.append('<ellipse cx="6" cy="-41" rx="6" ry="7.5" fill="#7a2f33" stroke-width="3"/>')
    g.append('<ellipse cx="-18" cy="-48" rx="5" ry="3" fill="#e98a8a" stroke="none" opacity=".55"/><ellipse cx="30" cy="-48" rx="5" ry="3" fill="#e98a8a" stroke="none" opacity=".55"/>')
    g.append(top)
    for k, a in enumerate((armL or 'M-34 -22 q-14 6 -16 22', armR or 'M38 -22 q14 6 16 22')):
        ex_, ey_ = end_of(a)
        g.append(hands[k].replace('BEFORE', '').replace('EX', f'{ex_:.1f}').replace('EY', f'{ey_:.1f}') if 'BEFORE' in hands[k] else '')
        g.append(limb(a))
        g.append(f'<circle cx="{ex_:.1f}" cy="{ey_:.1f}" r="5.6" fill="{GREEN}" stroke-width="3"/>')
        if hands[k] and 'BEFORE' not in hands[k]:
            g.append(hands[k].replace('EX', f'{ex_:.1f}').replace('EY', f'{ey_:.1f}'))
    g.append(front); g.append('</g>')
    return ''.join(g)


# ---------------- cute people (tools/body.py proportions, arms by body.arm, round hands) ----------------
def _v(a):
    a = math.radians(a); return math.sin(a), math.cos(a)


def ik(S, T, H, kind='cute', bend_dir=1):
    """upper / bend for body.arm so that the WRIST lands on T (2-link arm, elbow folds to bend_dir)"""
    p = P[kind]; Lu, Lf = p['upper'] * H, p['fore'] * H
    dx, dy = T[0] - S[0], T[1] - S[1]; d = max(abs(Lu - Lf) + 1, min(math.hypot(dx, dy), (Lu + Lf) * .995))
    base = math.degrees(math.atan2(dx, dy))
    al = math.degrees(math.acos(max(-1, min(1, (Lu * Lu + d * d - Lf * Lf) / (2 * Lu * d)))))
    ga = math.degrees(math.acos(max(-1, min(1, (Lu * Lu + Lf * Lf - d * d) / (2 * Lu * Lf)))))
    return base - bend_dir * al, 180 - ga


def limb_to(S, T, H, kind, bend_dir, name, sleeve, skin, sleeve_len='long'):
    up, bend = ik(S, T, H, kind, bend_dir)
    return body_arm(S[0], S[1], H, up, min(140, bend), bend_dir, name, sleeve=sleeve, skin=skin, line=LINE, kind=kind,
                    sleeve_len=sleeve_len, amp=(0, 0))


def face(cx, cy, H, look=(0, 0), mouth='smile', brows='calm', side=0, blush=True, mask=None):
    """cy = head centre. side: 0 front, +1 profile to the right (eye & mouth shifted)"""
    s = H; g = ''
    exs = (-.19, .19) if side == 0 else (.12 + .14 * side, .34 * side) if side else ()
    ey = cy + .04 * s
    if mask:   # domino mask band
        g += (f'<path d="M{cx - .5 * s:.1f} {ey - .1 * s:.1f} Q{cx:.1f} {ey - .2 * s:.1f} {cx + .5 * s:.1f} {ey - .1 * s:.1f} '
              f'L{cx + .47 * s:.1f} {ey + .12 * s:.1f} Q{cx:.1f} {ey + .05 * s:.1f} {cx - .47 * s:.1f} {ey + .12 * s:.1f}Z" fill="{mask}" stroke="{LINE}" stroke-width="{s * .03:.1f}"/>')
    for ex in exs:
        x = cx + ex * s
        g += f'<ellipse cx="{x:.1f}" cy="{ey:.1f}" rx="{.105 * s:.1f}" ry="{.12 * s:.1f}" fill="#fbfaf2" stroke="{LINE}" stroke-width="{s * .025:.1f}"/>'
        px, py = x + look[0] * .045 * s, ey + look[1] * .05 * s
        g += f'<circle cx="{px:.1f}" cy="{py:.1f}" r="{.06 * s:.1f}" fill="#1a120c"/><circle cx="{px + .02 * s:.1f}" cy="{py - .025 * s:.1f}" r="{.02 * s:.1f}" fill="#fff"/>'
        bx, by = x, ey - .2 * s
        tilt = {'calm': 0, 'up': -.05, 'worried': .06, 'angry': -.06, 'proud': -.03}[brows]
        sgn = -1 if ex < 0 else 1
        if side: sgn = 1 if ex == exs[0] else -1
        g += (f'<path d="M{bx - .09 * s:.1f} {by + tilt * s * sgn:.1f} L{bx + .09 * s:.1f} {by - tilt * s * sgn:.1f}" stroke="{LINE}" '
              f'stroke-width="{s * .035:.1f}" stroke-linecap="round"/>')
    mx = cx + (.3 * side * s if side else 0); my = cy + .3 * s
    if mouth == 'smile':
        g += f'<path d="M{mx - .11 * s:.1f} {my - .02 * s:.1f} Q{mx:.1f} {my + .1 * s:.1f} {mx + .11 * s:.1f} {my - .02 * s:.1f}" fill="none" stroke="{LINE}" stroke-width="{s * .032:.1f}" stroke-linecap="round"/>'
    elif mouth == 'grin':
        g += (f'<path d="M{mx - .15 * s:.1f} {my - .04 * s:.1f} Q{mx:.1f} {my + .2 * s:.1f} {mx + .15 * s:.1f} {my - .04 * s:.1f}Z" fill="#8a2f2a" stroke="{LINE}" stroke-width="{s * .028:.1f}" stroke-linejoin="round"/>'
              f'<path d="M{mx - .12 * s:.1f} {my - .03 * s:.1f} L{mx + .12 * s:.1f} {my - .03 * s:.1f} L{mx + .1 * s:.1f} {my + .01 * s:.1f} L{mx - .1 * s:.1f} {my + .01 * s:.1f}Z" fill="#fff"/>')
    elif mouth == 'o':
        g += f'<ellipse cx="{mx:.1f}" cy="{my + .02 * s:.1f}" rx="{.07 * s:.1f}" ry="{.09 * s:.1f}" fill="#7a2a26" stroke="{LINE}" stroke-width="{s * .028:.1f}"/>'
    elif mouth == 'wobble':
        g += f'<path d="M{mx - .12 * s:.1f} {my + .02 * s:.1f} q{.04 * s:.1f} {-.05 * s:.1f} {.08 * s:.1f} 0 q{.04 * s:.1f} {.05 * s:.1f} {.08 * s:.1f} 0 q{.04 * s:.1f} {-.05 * s:.1f} {.08 * s:.1f} 0" fill="none" stroke="{LINE}" stroke-width="{s * .03:.1f}" stroke-linecap="round"/>'
    elif mouth == 'flat':
        g += f'<path d="M{mx - .07 * s:.1f} {my + .02 * s:.1f} L{mx + .07 * s:.1f} {my + .02 * s:.1f}" stroke="{LINE}" stroke-width="{s * .03:.1f}" stroke-linecap="round"/>'
    if blush and not mask:
        for ex in exs:
            g += f'<ellipse cx="{cx + ex * s * 1.2:.1f}" cy="{cy + .22 * s:.1f}" rx="{.08 * s:.1f}" ry="{.045 * s:.1f}" fill="#ef7f74" opacity=".45"/>'
    return g


def hair_shapes(cx, cy, H, style, col):
    """returns (behind, front) svg for the hair; cy = head centre"""
    r = .5 * H; w = .54 * H; k = f'fill="{col}" stroke="{LINE}" stroke-width="{H * .03:.1f}" stroke-linejoin="round"'
    back = front = ''
    if style in ('bob', 'pony', 'long'):
        L = {'bob': .45, 'pony': .1, 'long': 1.0}[style]
        back = f'<path d="M{cx - w * 1.08:.1f} {cy:.1f} Q{cx - w * 1.15:.1f} {cy - r * 1.25:.1f} {cx:.1f} {cy - r * 1.12:.1f} Q{cx + w * 1.15:.1f} {cy - r * 1.25:.1f} {cx + w * 1.08:.1f} {cy:.1f} L{cx + w * 1.05:.1f} {cy + r * L * 1.4:.1f} Q{cx:.1f} {cy + r * (L * 1.4 + .15):.1f} {cx - w * 1.05:.1f} {cy + r * L * 1.4:.1f}Z" {k}/>'
    if style == 'pony':
        back = f'<path d="M{cx + w * .7:.1f} {cy - r * .6:.1f} q{w * .9:.1f} {-r * .2:.1f} {w * .75:.1f} {r * 1.1:.1f} q{-w * .2:.1f} {r * .4:.1f} {-w * .5:.1f} {r * .3:.1f} q{w * .2:.1f} {-r * .6:.1f} {-w * .2:.1f} {-r * 1.0:.1f}Z" {k}/>' + back
    if style == 'buns':
        back = ''.join(f'<circle cx="{cx + sx * w * .85:.1f}" cy="{cy - r * .85:.1f}" r="{r * .38:.1f}" {k}/>' for sx in (-1, 1))
    # front cap with fringe (all styles)
    fr = {'short': .15, 'bob': .25, 'pony': .2, 'buns': .2, 'spiky': .12, 'long': .25, 'bald': -1}[style]
    if fr < 0:
        return back, ''
    front = (f'<path d="M{cx - w * 1.02:.1f} {cy + r * .1:.1f} Q{cx - w * 1.05:.1f} {cy - r * 1.18:.1f} {cx:.1f} {cy - r * 1.1:.1f} '
             f'Q{cx + w * 1.05:.1f} {cy - r * 1.18:.1f} {cx + w * 1.02:.1f} {cy + r * .1:.1f} '
             f'Q{cx + w * .9:.1f} {cy - r * fr * 2.2:.1f} {cx + w * .55:.1f} {cy - r * (.35 - fr):.1f} '
             f'Q{cx + w * .2:.1f} {cy - r * (.2 - fr):.1f} {cx - w * .05:.1f} {cy - r * (.42 - fr * .5):.1f} '
             f'Q{cx - w * .4:.1f} {cy - r * (.25 - fr):.1f} {cx - w * .8:.1f} {cy - r * (.15 - fr):.1f} Z" {k}/>')
    if style == 'spiky':
        front += ''.join(f'<path d="M{cx + dx * w:.1f} {cy - r * .9:.1f} l{-.16 * w:.1f} {-r * .5:.1f} l{.36 * w:.1f} {r * .35:.1f}Z" {k}/>' for dx in (-.6, -.15, .3, .7))
    front += f'<path d="M{cx - w * .5:.1f} {cy - r * .85:.1f} q{w * .3:.1f} {-r * .2:.1f} {w * .6:.1f} {-r * .1:.1f}" fill="none" stroke="#fff" stroke-width="{H * .03:.1f}" opacity=".35" stroke-linecap="round"/>'
    return back, front


def person(cx, top, H, kind='cute', skin='#e8b48c', hair=('short', '#3a2416'), shirt='#4a6fa5', pants='#2c3550', shoes='#1d1d24',
           look=(0, 0), mouth='smile', brows='calm', arms=(), props_back='', props_front='', legs=True, mask=None, deco='',
           rim=None, side=0, collar=None, tie=None, stripe=None, sleeve_len='long', stance=0):
    """front-facing cute figure; arms = list of (shoulder 'L'|'R' (viewer side), target wrist (x, y), bend_dir).
    Returns svg. top = top of the head (hair adds ~0.1H)."""
    p = P[kind]; out = []
    hy = top + .5 * H
    torso_top = top + H + p['neck'] * H; hip = top + p['height'] * H / 2
    sw = p['shoulder_w'] * H
    (lx, ly), (rx, ry) = shoulders(cx, top, H, kind)
    if side:
        lx, rx = cx - .18 * H, cx + .18 * H; sw *= .78
    hb, hf = hair_shapes(cx, hy, H, hair[0], hair[1])
    out.append(props_back)
    out.append(hb)
    if legs:
        lw = .44 * H; leg = (p['thigh'] + p['shin']) * H
        for k, sx in enumerate((-1, 1)):
            x = cx + sx * (.25 * H + stance * H * .25)
            y1 = hip + leg
            out.append(f'<path d="M{cx + sx * .05 * H:.1f} {hip - .2 * H:.1f} L{cx + sx * (.05 * H + lw):.1f} {hip - .2 * H:.1f} L{x + sx * lw * .5:.1f} {y1:.1f} L{x - sx * lw * .5:.1f} {y1:.1f}Z" fill="{pants}" stroke="{LINE}" stroke-width="{H * .035:.1f}" stroke-linejoin="round"/>')
            if stripe:
                out.append(f'<path d="M{cx + sx * (.05 * H + lw * .92):.1f} {hip - .1 * H:.1f} L{x + sx * lw * .42:.1f} {y1:.1f}" stroke="{stripe}" stroke-width="{H * .07:.1f}"/>')
            out.append(f'<ellipse cx="{x + sx * .12 * H:.1f}" cy="{y1 + .08 * H:.1f}" rx="{.36 * H:.1f}" ry="{.15 * H:.1f}" fill="{shoes}" stroke="{LINE}" stroke-width="{H * .035:.1f}"/>')
    # torso
    wt = sw * .5; wb = sw * .44
    tb = hip + (.05 * H if legs else .6 * H)
    out.append(f'<path d="M{cx - wt:.1f} {torso_top + .3 * H:.1f} Q{cx - wt:.1f} {torso_top:.1f} {cx - wt + .3 * H:.1f} {torso_top:.1f} L{cx + wt - .3 * H:.1f} {torso_top:.1f} '
               f'Q{cx + wt:.1f} {torso_top:.1f} {cx + wt:.1f} {torso_top + .3 * H:.1f} L{cx + wb:.1f} {tb:.1f} L{cx - wb:.1f} {tb:.1f}Z" fill="{shirt}" stroke="{LINE}" stroke-width="{H * .035:.1f}" stroke-linejoin="round"/>')
    if stripe:
        for sx in (-1, 1):
            out.append(f'<path d="M{cx + sx * (wt - .08 * H):.1f} {torso_top + .15 * H:.1f} L{cx + sx * (wb - .06 * H):.1f} {tb:.1f}" stroke="{stripe}" stroke-width="{H * .07:.1f}"/>')
    if collar:
        out.append(f'<path d="M{cx - .3 * H:.1f} {torso_top - .02 * H:.1f} L{cx:.1f} {torso_top + .38 * H:.1f} L{cx + .3 * H:.1f} {torso_top - .02 * H:.1f}Z" fill="{collar}" stroke="{LINE}" stroke-width="{H * .03:.1f}" stroke-linejoin="round"/>')
    if tie:
        out.append(f'<path d="M{cx - .06 * H:.1f} {torso_top + .05 * H:.1f} L{cx + .06 * H:.1f} {torso_top + .05 * H:.1f} L{cx + .09 * H:.1f} {torso_top + .75 * H:.1f} L{cx:.1f} {torso_top + .88 * H:.1f} L{cx - .09 * H:.1f} {torso_top + .75 * H:.1f}Z" fill="{tie}" stroke="{LINE}" stroke-width="{H * .025:.1f}"/>')
    out.append(deco)
    # neck + head
    out.append(f'<rect x="{cx - .13 * H:.1f}" y="{top + H * .85:.1f}" width="{.26 * H:.1f}" height="{H * .35:.1f}" fill="{skin}" stroke="{LINE}" stroke-width="{H * .03:.1f}"/>')
    out.append(f'<ellipse cx="{cx:.1f}" cy="{hy:.1f}" rx="{.54 * H:.1f}" ry="{.5 * H:.1f}" fill="{skin}" stroke="{LINE}" stroke-width="{H * .035:.1f}"/>')
    for sx in (-1, 1):
        out.append(f'<ellipse cx="{cx + sx * .54 * H:.1f}" cy="{hy + .06 * H:.1f}" rx="{.08 * H:.1f}" ry="{.11 * H:.1f}" fill="{skin}" stroke="{LINE}" stroke-width="{H * .03:.1f}"/>')
    if rim:   # coloured rim light on one side of the head
        out.append(f'<path d="M{cx + rim[0] * .5 * H:.1f} {hy - .38 * H:.1f} Q{cx + rim[0] * .62 * H:.1f} {hy:.1f} {cx + rim[0] * .45 * H:.1f} {hy + .36 * H:.1f}" fill="none" stroke="{rim[1]}" stroke-width="{H * .06:.1f}" stroke-linecap="round" opacity=".8"/>')
    out.append(face(cx, hy, H, look, mouth, brows, side, mask=mask))
    out.append(hf)
    for k, (sh, T, bd) in enumerate(arms):
        S = (lx, ly) if sh == 'L' else (rx, ry)
        out.append(limb_to(S, T, H, kind, bd, f'p{int(cx)}{k}', shirt, skin, sleeve_len))
    out.append(props_front)
    return ''.join(out)


def sweat(x, y, s):
    return f'<path d="M{x} {y} q{-s * .5:.1f} {s * .8:.1f} 0 {s:.1f} q{s * .5:.1f} {-s * .2:.1f} 0 {-s:.1f}Z" fill="#bfe6ff" stroke="{LINE}" stroke-width="{s * .12:.1f}"/>'


def qmark(x, y, s, col='#fff', rot=0):
    """drawn question mark (a symbol, not text)"""
    return (f'<g transform="translate({x} {y}) rotate({rot}) scale({s / 100:.3f})"><path d="M-22 -30 Q-22 -60 4 -60 Q30 -60 30 -36 Q30 -18 10 -8 Q2 -3 2 12" fill="none" stroke="{LINE}" stroke-width="30" stroke-linecap="round"/>'
            f'<path d="M-22 -30 Q-22 -60 4 -60 Q30 -60 30 -36 Q30 -18 10 -8 Q2 -3 2 12" fill="none" stroke="{col}" stroke-width="15" stroke-linecap="round"/>'
            f'<circle cx="2" cy="36" r="13" fill="{col}" stroke="{LINE}" stroke-width="7"/></g>')


def bang(x, y, s, col='#F2D27A', rot=0):
    return (f'<g transform="translate({x} {y}) rotate({rot}) scale({s / 100:.3f})"><path d="M-12 -60 L12 -60 L6 14 L-6 14Z" fill="{col}" stroke="{LINE}" stroke-width="7" stroke-linejoin="round"/>'
            f'<circle cx="0" cy="38" r="12" fill="{col}" stroke="{LINE}" stroke-width="7"/></g>')


# =========================== A: classroom, ONE kid writes with the left hand ===========================
def pencil(x0, y0, ang, L, w):
    """pencil from its TIP (x0,y0) going in direction ang (deg, 0 = up, clockwise)"""
    return (f'<g transform="translate({x0} {y0}) rotate({ang})">'
            f'<path d="M0 0 L{-w / 2:.1f} {-w * 1.6:.1f} L{w / 2:.1f} {-w * 1.6:.1f}Z" fill="#f0d0a0" stroke="{LINE}" stroke-width="{w * .18:.1f}" stroke-linejoin="round"/>'
            f'<path d="M0 0 L{-w * .18:.1f} {-w * .55:.1f} L{w * .18:.1f} {-w * .55:.1f}Z" fill="#333"/>'
            f'<rect x="{-w / 2:.1f}" y="{-L:.1f}" width="{w:.1f}" height="{L - w * 1.6:.1f}" fill="#f6c534" stroke="{LINE}" stroke-width="{w * .18:.1f}"/>'
            f'<rect x="{-w / 2 + w * .32:.1f}" y="{-L:.1f}" width="{w * .2:.1f}" height="{L - w * 1.6:.1f}" fill="#fff3b0" opacity=".7"/>'
            f'<rect x="{-w / 2:.1f}" y="{-L - w * .5:.1f}" width="{w:.1f}" height="{w * .55:.1f}" fill="#c9c9c9" stroke="{LINE}" stroke-width="{w * .15:.1f}"/>'
            f'<rect x="{-w / 2:.1f}" y="{-L - w * 1.1:.1f}" width="{w:.1f}" height="{w * .65:.1f}" rx="{w * .3:.1f}" fill="#f08a9a" stroke="{LINE}" stroke-width="{w * .15:.1f}"/></g>')


def kid_writing(cx, top, H, desk_y, lefty, skin, hair, shirt, look, mouth, brows, rim=None):
    """seated kid behind a desk; writes with the right hand (viewer-left) or, if lefty, with the left hand (viewer-right)"""
    kind = 'cute_child'
    (lx, ly), (rx, ry) = shoulders(cx, top, H, kind)
    paper_x = cx + (.25 * H if lefty else -.25 * H)
    wx = cx + (.55 * H if lefty else -.55 * H); wy = desk_y - .05 * H   # writing hand
    ox = cx + (-.45 * H if lefty else .45 * H); oy = desk_y + .02 * H    # resting hand
    pen = pencil(wx + (-.3 * H if lefty else .3 * H), desk_y + .04 * H, 30 if lefty else -30, H * 1.35, H * .17)
    if lefty:
        arms_ = [('R', (wx, wy), -1), ('L', (ox, oy), 1)]
    else:
        arms_ = [('L', (wx, wy), 1), ('R', (ox, oy), -1)]
    paper = (f'<path d="M{paper_x - .7 * H:.1f} {desk_y + .02 * H:.1f} L{paper_x + .7 * H:.1f} {desk_y + .02 * H:.1f} L{paper_x + .62 * H:.1f} {desk_y - .16 * H:.1f} L{paper_x - .62 * H:.1f} {desk_y - .16 * H:.1f}Z" fill="#f7f3e6" stroke="{LINE}" stroke-width="{H * .025:.1f}"/>')
    body = person(cx, top, H, kind, skin, hair, shirt, look=look, mouth=mouth, brows=brows, legs=False, collar='#f4f1e8', rim=rim)
    armsvg = ''.join(limb_to((lx, ly) if sh == 'L' else (rx, ry), T, H, kind, bd, f'k{int(cx)}{sh}', shirt, skin) for sh, T, bd in arms_)
    return body, paper, pen + armsvg


def desk(x0, x1, y, depth, H, col='#b07a48', top='#d39a5e'):
    return (f'<path d="M{x0 - 10} {y - depth} L{x1 + 10} {y - depth} L{x1 + 30} {y + 10} L{x0 - 30} {y + 10}Z" fill="{top}" stroke="{LINE}" stroke-width="{H * .04:.1f}" stroke-linejoin="round"/>'
            f'<rect x="{x0 - 30}" y="{y + 10}" width="{x1 - x0 + 60}" height="{H * .9:.1f}" fill="{col}" stroke="{LINE}" stroke-width="{H * .04:.1f}"/>'
            f'<rect x="{x0 - 30}" y="{y + 10}" width="{x1 - x0 + 60}" height="{H * .12:.1f}" fill="#fff" opacity=".18"/>')


def make_A():
    rnd = random.Random(11)
    d = FILTERS
    d += lin('wallA', [(0, '#1f3550'), (.6, '#243c58'), (1, '#152536')])
    d += '<linearGradient id="coneA" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff0b8" stop-opacity=".85"/><stop offset="1" stop-color="#ffd36a" stop-opacity=".12"/></linearGradient>'
    d += rad('haloA', 870, 640, 420, [(0, '#ffe39a', .75), (.4, '#f2b54a', .32), (1, '#000', 0)])
    d += rad('vigA', 960, 540, 1150, [(0, '#000', 0), (.6, '#000', 0), (1, '#000', .6)])
    d += lin('floorA', [(0, '#2a2030'), (1, '#120c16')])
    b = '<rect width="1920" height="1080" fill="url(#wallA)"/>'
    # window light panes on the wall (soft) and a chalkboard with a 90/10 pie
    for x in (40, 330):
        b += f'<rect x="{x}" y="520" width="240" height="150" rx="10" fill="#5c87b8" opacity=".18"/>'
    b += '<rect x="1130" y="40" width="760" height="300" rx="14" fill="#5a3a22" stroke="#120c08" stroke-width="8"/>'
    b += '<rect x="1150" y="58" width="720" height="264" rx="8" fill="#1f3a2c"/>'
    b += '<rect x="1150" y="58" width="720" height="264" rx="8" fill="#fff" opacity=".04"/>'
    pcx, pcy, pr = 1720, 190, 105
    a10 = math.radians(36)
    b += f'<circle cx="{pcx}" cy="{pcy}" r="{pr}" fill="#e8efe6" opacity=".22" stroke="#e8efe6" stroke-width="6" stroke-opacity=".7"/>'
    b += (f'<path d="M{pcx} {pcy} L{pcx} {pcy - pr} A{pr} {pr} 0 0 1 {pcx + pr * math.sin(a10):.1f} {pcy - pr * math.cos(a10):.1f}Z" '
          f'fill="#F2D27A" opacity=".9" stroke="#fff3c0" stroke-width="5" transform="translate(14 -14)"/>')
    for k in range(5):   # chalk scribble lines (not letters)
        y = 100 + k * 44; x = 1200 + rnd.randint(0, 20)
        b += f'<path d="M{x} {y} q30 -14 60 0 t60 0 t60 0 t60 0" fill="none" stroke="#e8efe6" stroke-width="5" opacity="{.25 + rnd.random() * .2:.2f}"/>'
    b += '<path d="M1190 290 q120 -40 240 -6" stroke="#e8efe6" stroke-width="5" fill="none" opacity=".3"/>'
    # floor
    b += '<rect y="880" width="1920" height="200" fill="url(#floorA)"/>'
    # ---------- back row (smaller), all right-handed ----------
    skins = ['#f3c9a2', '#d9a37a', '#a8714a', '#7a4d30', '#f5d6b8', '#c88c62', '#e2b08a', '#8f5c3a', '#f0c19a', '#b98059']
    hairs = [('bob', '#2b1d14'), ('short', '#6b3e1e'), ('buns', '#1a1a1a'), ('spiky', '#c98c3a'), ('pony', '#3a2416'), ('short', '#111'),
             ('bob', '#8a4a20'), ('spiky', '#2b1d14'), ('pony', '#c98c3a'), ('short', '#3a2416')]
    BH = 64; btop = 360; bdesk = btop + 2.05 * BH
    back = []; papers = []; fronts = []
    for i, x in enumerate((1110, 1260, 1410, 1560, 1710, 1860)):
        lk = (-1, 1) if i in (0, 1) else (0, 1)
        bo, pa, fr = kid_writing(x, btop, BH, bdesk, False, skins[i], hairs[i], '#39507c', lk, 'flat' if i % 2 else 'smile', 'calm')
        back.append(bo); papers.append(pa); fronts.append(fr)
    b += '<g opacity=".92">' + ''.join(back) + desk(1050, 1900, bdesk, 18, BH, '#7a5434', '#a8784a') + ''.join(papers) + ''.join(fronts) + '</g>'
    b += '<rect x="1000" y="300" width="920" height="320" fill="#0e1a30" opacity=".28"/>'   # back row in shade
    # ---------- spotlight cone onto the lefty ----------
    LX = 820
    b += f'<path d="M{LX - 70} -20 L{LX + 70} -20 L{LX + 330} 900 L{LX - 330} 900 Z" fill="url(#coneA)" filter="url(#b16)" opacity=".85"/>'
    b += '<rect width="1920" height="1080" fill="url(#haloA)"/>'
    for _ in range(45):
        y = rnd.uniform(380, 860); w = 70 + 260 * y / 900
        b += f'<circle cx="{LX + rnd.uniform(-w, w):.0f}" cy="{y:.0f}" r="{rnd.uniform(1.4, 3.4):.1f}" fill="#fff4d0" opacity="{rnd.uniform(.3, .9):.2f}"/>'
    # ---------- front row ----------
    FH = 128; ftop = 560; fdesk = ftop + 2.05 * FH
    xs = [190, 500, LX, 1140]
    looks = [(1.2, .2), (1.4, 0), (0, -.1), (-1.4, 0)]
    mouths = ['o', 'o', 'grin', 'o']
    brows = ['up', 'up', 'proud', 'up']
    bodies = []; papers = []; fronts = []
    for i, x in enumerate(xs):
        lefty = x == LX
        bo, pa, fr = kid_writing(x, ftop, FH, fdesk, lefty, skins[6 + i] if not lefty else '#e8b28a', hairs[6 + i] if not lefty else ('spiky', '#5a2e14'),
                                 '#c0563f' if lefty else '#3d5a8c', looks[i], mouths[i], brows[i], rim=None)
        bodies.append(bo); papers.append(pa); fronts.append(fr)
    # lefty glow behind him
    b += f'<ellipse cx="{LX}" cy="{ftop + 150}" rx="230" ry="260" fill="#ffd27a" opacity=".55" filter="url(#b32)"/>'
    b += ''.join(bodies)
    # frog classmate at the end of the row, staring at the lefty
    b += frog(1420, fdesk + 30, 2.6, look=(-6, 1), mouth='O', armL='M-34 -26 q-20 -8 -30 -30', armR='M38 -22 q14 -2 24 -6',
              shadow=False,
              mid=f'<g clip-path="url(#fbody)"><rect x="-50" y="-40" width="110" height="60" fill="#3d5a8c" stroke-width="3"/><path d="M-6 -40 L6 -24 L18 -40" fill="#f4f1e8" stroke-width="2.6"/></g><path d="{BODY}" fill="none" stroke-width="4"/>')
    b += desk(40, 1510, fdesk, 26, FH)
    b += ''.join(papers) + ''.join(fronts)
    # gold rim + sparkles on the lefty, '!' above
    b += f'<path d="M{LX + 300} {ftop - 60} q60 -50 30 -110" fill="none" stroke="#F2D27A" stroke-width="10" stroke-linecap="round" opacity="0"/>'
    b += spark(LX + 150, ftop - 10, 26) + spark(LX - 170, ftop + 60, 16) + spark(LX + 210, ftop + 170, 13) + spark(LX - 40, ftop - 70, 18)
    b += bang(LX + 120, ftop - 70, 95, rot=12)
    b += '<rect width="1920" height="1080" fill="url(#vigA)"/>'
    lines = [('ONLY', 150, 'w'), ('1 IN 10', 240, 'y')]
    return page('#1f3550', svg(d, b), lines, outline='#0b1422', top=50)


# =========================== B: Kill Bill homage, one LEFT-handed fighter vs nine right-handed ===========================
def katana(gx, gy, ang, L, w, blade='#e6eef8', glow=None):
    """grip centre (gx,gy); blade goes in direction ang (0 = up, clockwise)"""
    g = f'<g transform="translate({gx:.1f} {gy:.1f}) rotate({ang})">'
    if glow:
        g += f'<path d="M{-w * .7:.1f} {-w * 1.2:.1f} L{-w * .7:.1f} {-L:.1f} Q0 {-L - w * 2:.1f} {w * .7:.1f} {-L:.1f} L{w * .7:.1f} {-w * 1.2:.1f}Z" fill="{glow}" opacity=".7" filter="url(#b8)"/>'
    g += (f'<path d="M{-w / 2:.1f} {-w * 1.2:.1f} L{-w / 2:.1f} {-L * .92:.1f} Q{-w * .4:.1f} {-L:.1f} {w / 2:.1f} {-L - w:.1f} L{w / 2:.1f} {-w * 1.2:.1f}Z" fill="{blade}" stroke="{LINE}" stroke-width="{w * .25:.1f}" stroke-linejoin="round"/>'
          f'<path d="M{w * .1:.1f} {-w * 1.4:.1f} L{w * .1:.1f} {-L * .9:.1f}" stroke="#fff" stroke-width="{w * .2:.1f}" opacity=".8"/>'
          f'<ellipse cx="0" cy="{-w * 1.15:.1f}" rx="{w * 1.3:.1f}" ry="{w * .35:.1f}" fill="#c9a24a" stroke="{LINE}" stroke-width="{w * .2:.1f}"/>'
          f'<rect x="{-w * .55:.1f}" y="{-w * 1.0:.1f}" width="{w * 1.1:.1f}" height="{w * 3.2:.1f}" rx="{w * .3:.1f}" fill="#1a1414" stroke="{LINE}" stroke-width="{w * .2:.1f}"/>'
          f'<path d="M{-w * .5:.1f} {-w * .4:.1f} l{w:.1f} {w * .6:.1f} M{-w * .5:.1f} {w * .6:.1f} l{w:.1f} {w * .6:.1f}" stroke="#d8c8a0" stroke-width="{w * .15:.1f}" opacity=".7"/></g>')
    return g


def fighter(cx, top, H, sword_side, blade_ang, grip, look, mouth, brows, skin, extra=''):
    """masked fighter in a black suit; sword hand = viewer side 'L' (= the figure's RIGHT hand)"""
    kind = 'cute'
    (lx, ly), (rx, ry) = shoulders(cx, top, H, kind)
    S = (lx, ly) if sword_side == 'L' else (rx, ry)
    gx, gy = grip
    sw = katana(gx, gy, blade_ang, H * 2.3, H * .13)
    bd = 1 if sword_side == 'L' else -1
    if gx > S[0] if sword_side == 'L' else gx < S[0]:
        bd = -bd
    swordarm = limb_to(S, (gx, gy + .12 * H), H, kind, bd, f'f{int(cx)}', '#16161c', skin)
    other = (rx, ry) if sword_side == 'L' else (lx, ly)
    oT = (other[0] + (.55 if sword_side == 'L' else -.55) * H, other[1] + 1.2 * H)
    offarm = limb_to(other, oT, H, kind, -1 if sword_side == 'L' else 1, f'o{int(cx)}', '#16161c', skin)
    return person(cx, top, H, kind, skin, ('short', '#141010'), '#16161c', '#16161c', '#0b0b0e', look=look, mouth=mouth, brows=brows,
                  mask='#0b0b0e', collar='#f2f2f2', tie='#0b0b0e', props_front=offarm + sw + swordarm + extra, stance=.4)


def make_B():
    rnd = random.Random(3)
    d = FILTERS
    d += lin('skyB', [(0, '#06112a'), (.55, '#0c2350'), (1, '#071230')])
    d += rad('hotB', 1110, 560, 520, [(0, '#fff1b0', .85), (.35, '#f2c24a', .35), (1, '#000', 0)])
    d += rad('vigB', 960, 540, 1150, [(0, '#000', 0), (.6, '#000', 0), (1, '#000', .65)])
    d += '<linearGradient id="coneB" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff4c0" stop-opacity=".8"/><stop offset="1" stop-color="#ffd36a" stop-opacity=".1"/></linearGradient>'
    b = '<rect width="1920" height="1080" fill="url(#skyB)"/>'
    # shoji paper screens glowing warm-blue, upper balcony rail, paper lanterns
    for i in range(12):
        x = 40 + i * 160
        b += f'<rect x="{x}" y="120" width="150" height="430" fill="#2a63b8" opacity=".55"/>'
        for gx in range(1, 3):
            b += f'<line x1="{x + gx * 50}" y1="120" x2="{x + gx * 50}" y2="550" stroke="#06112a" stroke-width="6"/>'
        for gy in range(1, 6):
            b += f'<line x1="{x}" y1="{120 + gy * 72}" x2="{x + 150}" y2="{120 + gy * 72}" stroke="#06112a" stroke-width="6"/>'
        b += f'<rect x="{x}" y="120" width="150" height="430" fill="none" stroke="#040a18" stroke-width="12"/>'
    b += '<rect x="0" y="80" width="1920" height="44" fill="#140d0a"/><rect x="0" y="540" width="1920" height="40" fill="#140d0a"/>'
    b += '<rect x="0" y="0" width="1920" height="80" fill="#04060e"/>'
    for x in (300, 700, 1500, 1820):
        b += f'<line x1="{x}" y1="80" x2="{x}" y2="150" stroke="#000" stroke-width="3"/><ellipse cx="{x}" cy="190" rx="34" ry="44" fill="#d8402a" opacity=".9"/><ellipse cx="{x}" cy="190" rx="70" ry="80" fill="#ff6a3a" opacity=".35" filter="url(#b16)"/>'
        b += f'<path d="M{x - 30} 175 q30 -8 60 0 M{x - 32} 200 q32 8 64 0" stroke="#7a1a10" stroke-width="3" fill="none"/>'
    # glowing checker floor in perspective (vanishing point 1100, 380)
    VX, VY = 1100, 380; y0 = 580
    b += '<rect y="580" width="1920" height="500" fill="#05081a"/>'
    rows = [580, 610, 650, 705, 780, 880, 1010, 1180]
    cols = list(range(-16, 17))
    for r in range(len(rows) - 1):
        for c in range(len(cols) - 1):
            if (r + c) % 2: continue
            def X(col, y): return VX + (col * 150) * (y - VY) / (1080 - VY)
            ya, yb = rows[r], rows[r + 1]
            pts = f'{X(cols[c], ya):.0f},{ya} {X(cols[c + 1], ya):.0f},{ya} {X(cols[c + 1], yb):.0f},{yb} {X(cols[c], yb):.0f},{yb}'
            b += f'<polygon points="{pts}" fill="#2f7cff" opacity="{.18 + .25 * r / 7:.2f}"/>'
    b += '<rect y="575" width="1920" height="30" fill="#5aa0ff" opacity=".25" filter="url(#b8)"/>'
    # spotlight on the hero
    HX = 1110
    b += f'<path d="M{HX - 60} -20 L{HX + 60} -20 L{HX + 360} 960 L{HX - 360} 960 Z" fill="url(#coneB)" filter="url(#b16)" opacity=".75"/>'
    b += f'<ellipse cx="{HX}" cy="965" rx="330" ry="55" fill="#ffe9a0" opacity=".5" filter="url(#b8)"/>'
    b += '<rect width="1920" height="1080" fill="url(#hotB)"/>'
    skins = ['#e2b08a', '#c88c62', '#f3c9a2', '#a8714a', '#d9a37a', '#8f5c3a', '#f0c19a', '#b98059', '#e8b48c']
    # back row (small), facing the hero; sword in their RIGHT hand (viewer-left)
    out = []
    BH = 58; btop = 330
    for i, x in enumerate((960, 1300, 1560, 1790)):
        right_of_hero = x > HX
        look = (-1.3, .2) if right_of_hero else (1.3, .2)
        S = shoulders(x, btop, BH)[0]
        if right_of_hero:
            grip = (S[0] + .5 * BH, S[1] + .35 * BH); ang = -40
        else:
            grip = (S[0] - .45 * BH, S[1] - .3 * BH); ang = 35
        out.append(fighter(x, btop, BH, 'L', ang, grip, look, ['o', 'wobble'][i % 2], 'worried', skins[i]))
    b += '<g opacity=".9">' + ''.join(out) + '</g>'
    b += '<rect x="900" y="300" width="1020" height="380" fill="#081634" opacity=".25"/>'
    # mid row right
    out = []
    MH = 74
    for i, (x, t) in enumerate(((1470, 430), (1740, 410))):
        S = shoulders(x, t, MH)[0]
        grip = (S[0] + .5 * MH, S[1] + .3 * MH)
        out.append(fighter(x, t, MH, 'L', -38, grip, (-1.4, .3), ['wobble', 'o'][i], 'worried', skins[4 + i],
                           extra=sweat(x + .62 * MH, t + .15 * MH, MH * .28) + (qmark(x + .1 * MH, t - .45 * MH, MH * .9, rot=10) if i == 0 else '')))
    b += ''.join(out)
    # ---------- the hero: yellow suit, katana in the LEFT hand (viewer-right) ----------
    H = 108; top = 330
    (lx, ly), (rx, ry) = shoulders(HX, top, H)
    grip = (rx + .9 * H, ry + .55 * H)
    sw = katana(grip[0], grip[1], 48, H * 2.6, H * .14, '#fffbe8', glow='#fff2a0')
    hero_arm = limb_to((rx, ry), (grip[0] - .05 * H, grip[1] + .12 * H), H, 'cute', 1, 'hero-l', '#f2c418', '#e8b48c')
    off_arm = limb_to((lx, ly), (HX - .25 * H, ly + .5 * H), H, 'cute', 1, 'hero-r', '#f2c418', '#e8b48c')
    b += f'<ellipse cx="{HX}" cy="{top + 260}" rx="260" ry="330" fill="#ffd56a" opacity=".45" filter="url(#b32)"/>'
    b += person(HX, top, H, 'cute', '#e8b48c', ('pony', '#2a1a10'), '#f2c418', '#f2c418', '#f2c418', look=(1.3, 0), mouth='grin', brows='angry',
                stripe='#151515', props_front=off_arm + sw + hero_arm, stance=.9)
    b += spark(grip[0] + 230, grip[1] - 250, 30) + spark(grip[0] + 120, grip[1] - 120, 16) + spark(HX - 160, top + 40, 14)
    # front-left row (bigger, in shade), facing right toward the hero
    out = []
    FH = 88
    for i, (x, t) in enumerate(((250, 600), (560, 560))):
        S = shoulders(x, t, FH)[0]
        grip = (S[0] - .4 * FH, S[1] - .35 * FH)
        out.append(fighter(x, t, FH, 'L', 38, grip, (1.4, .2), ['o', 'wobble'][i], 'worried', skins[6 + i],
                           extra=sweat(x - .65 * FH, t + .2 * FH, FH * .25)))
    b += ''.join(out)
    # frog: tiny masked fighter in a black suit, holding a toothpick sword in its right hand
    b += frog(800, 1000, 2.5, look=(5, -2), mouth='O', armL='M-34 -24 q-14 -10 -18 -30', armR='M38 -22 q16 4 18 22',
              mid=f'<g clip-path="url(#fbody)"><rect x="-50" y="-44" width="110" height="64" fill="#16161c" stroke-width="3"/><path d="M-8 -44 L6 -18 L20 -44Z" fill="#f2f2f2" stroke-width="2.4"/><path d="M4 -40 L8 -40 L10 -14 L6 -10 L2 -14Z" fill="#0b0b0e" stroke-width="1.6"/></g><path d="{BODY}" fill="none" stroke-width="4"/>',
              top='<path d="M-30 -74 Q6 -84 40 -74 L38 -58 Q6 -64 -28 -58Z" fill="#0b0b0e" stroke-width="3" opacity=".9"/>'
                  + '<circle cx="-10" cy="-66" r="9" fill="#f4f5ea" stroke="none"/><circle cx="22" cy="-66" r="9" fill="#f4f5ea" stroke="none"/><circle cx="-5" cy="-67" r="4.4" fill="#1d2b1c" stroke="none"/><circle cx="27" cy="-67" r="4.4" fill="#1d2b1c" stroke="none"/>',
              hands=(f'<g transform="translate(EX EY) rotate(25)"><rect x="-2.5" y="-62" width="5" height="54" fill="#e6eef8" stroke-width="1.6"/><rect x="-7" y="-10" width="14" height="4" fill="#c9a24a" stroke-width="1.4"/><rect x="-3" y="-6" width="6" height="14" fill="#1a1414" stroke-width="1.4"/></g>BEFORE', ''),
              front=sweat(-44, -82, 16), shadow=True)
    b += '<rect width="1920" height="1080" fill="url(#vigB)"/>'
    lines = [('LEFTIES', 150, 'w'), ('FIGHT', 150, 'w'), ('BETTER?', 175, 'y')]
    return page('#06112a', svg(d, b), lines, outline='#030714', top=36)


# =========================== C: cave painter, Stone Age ===========================
def stencil(x, y, ang, sz, side, rnd, col='#c4482c', wall='#8a5a3c', fresh=False, op=.8):
    g = f'<g opacity="{op}">'
    g += f'<ellipse cx="{x + math.sin(math.radians(ang)) * sz * .9:.0f}" cy="{y - math.cos(math.radians(ang)) * sz * .9:.0f}" rx="{sz * 1.25:.0f}" ry="{sz * 1.35:.0f}" fill="{col}" opacity="{.95 if fresh else .7}" filter="url(#b16)"/>'
    for _ in range(14 if fresh else 6):
        a = rnd.uniform(0, 6.28); r = rnd.uniform(sz * .9, sz * 1.6)
        g += f'<circle cx="{x + math.cos(a) * r:.0f}" cy="{y - sz * .9 + math.sin(a) * r:.0f}" r="{rnd.uniform(1.5, 4):.1f}" fill="{col}" opacity=".7"/>'
    g += hand(x, y, ang, sz, side, 'back', 'open', skin=wall, line=wall, creases=False)
    return g + '</g>'


def make_C():
    rnd = random.Random(21)
    d = FILTERS
    d += lin('caveC', [(0, '#1a0d08'), (.5, '#2a160c'), (1, '#120805')])
    d += rad('fireC', 640, 900, 900, [(0, '#ffb85a', .75), (.3, '#e0662a', .35), (.7, '#5a1e0a', .1), (1, '#000', 0)])
    d += rad('wallC', 1450, 380, 620, [(0, '#b8805a', 1), (.55, '#7a4a30', 1), (1, '#2a160c', 0)])
    d += rad('sprayC', 1600, 330, 140, [(0, '#e0502e', .9), (.6, '#c03a20', .4), (1, '#c03a20', 0)])
    d += rad('vigC', 960, 540, 1150, [(0, '#000', 0), (.6, '#000', 0), (1, '#000', .7)])
    b = '<rect width="1920" height="1080" fill="url(#caveC)"/>'
    # lit rock wall (upper right) with texture
    b += '<path d="M880 0 L1920 0 L1920 860 Q1700 820 1500 840 Q1200 760 1010 600 Q900 420 930 200Z" fill="url(#wallC)"/>'
    for _ in range(60):
        x = rnd.randint(950, 1900); y = rnd.randint(20, 780)
        b += f'<ellipse cx="{x}" cy="{y}" rx="{rnd.randint(20, 90)}" ry="{rnd.randint(8, 30)}" fill="{rnd.choice(["#5a321e", "#c8916a", "#3a2014"])}" opacity="{rnd.uniform(.08, .25):.2f}" transform="rotate({rnd.randint(-20, 20)} {x} {y})"/>'
    for k in range(7):   # cracks
        x = rnd.randint(1000, 1880); y = rnd.randint(40, 700)
        b += f'<path d="M{x} {y} l{rnd.randint(-30, 30)} {rnd.randint(30, 60)} l{rnd.randint(-30, 30)} {rnd.randint(30, 60)}" stroke="#2a160c" stroke-width="4" fill="none" opacity=".4"/>'
    # stencils: mostly LEFT hands (S06), a few right
    W = '#e2b48a'
    sts = [(1180, 300, -20, 44, 'L'), (1300, 170, -8, 40, 'L'), (1440, 120, 10, 42, 'R'), (1760, 160, 14, 46, 'L'), (1850, 360, 22, 40, 'L'),
           (1130, 520, -25, 38, 'L'), (1790, 560, 10, 42, 'L'), (1610, 90, -6, 36, 'L'), (1290, 420, -14, 34, 'L')]
    for x, y, a, s, side in sts:
        b += stencil(x, y, a, s * 1.2, side, rnd, '#c8402a', W, op=.9)
    b += '<g opacity=".35">' + ''.join(f'<path d="M{x} {y} q30 -30 70 -10 q20 20 60 0 l10 20 q-60 30 -130 10Z" fill="#2a120a"/>' for x, y in ((1480, 640), (1050, 160))) + '</g>'
    # stalactites / cave mouth framing (top)
    for x in range(0, 1920, 70):
        h = rnd.randint(30, 140) if x < 900 else rnd.randint(10, 60)
        b += f'<path d="M{x - 40} -5 L{x + 40} -5 L{x + rnd.randint(-8, 8)} {h}Z" fill="#0e0604"/>'
    # floor
    b += '<path d="M0 820 Q500 780 1000 820 Q1500 860 1920 830 L1920 1080 L0 1080Z" fill="#1c0e07"/>'
    b += '<rect width="1920" height="1080" fill="url(#fireC)"/>'
    # ---------- painter (front view, head turned to the wall on the right) ----------
    PX, PT, PH = 1380, 300, 112
    (lx, ly), (rx, ry) = shoulders(PX, PT, PH)
    target = (rx + 1.05 * PH, ry - .85 * PH)          # wrist of the hand pressed on the wall
    b += f'<circle cx="{target[0] + 25:.0f}" cy="{target[1] - 45:.0f}" r="190" fill="url(#sprayC)"/>'
    b += f'<circle cx="{target[0] + 25:.0f}" cy="{target[1] - 45:.0f}" r="120" fill="#ff7a4a" opacity=".35" filter="url(#b32)"/>'
    wall_arm = limb_to((rx, ry), target, PH, 'cute', 1, 'painter-left', '#8a5a2a', '#c88c62', 'short')
    wall_hand = hand(target[0], target[1], 28, PH * .4, 'L', 'back', 'flat', skin='#d49a6c', line=LINE)
    mouth = (PX + .06 * PH, PT + .82 * PH); pend = (target[0] - .25 * PH, target[1] - .2 * PH)
    pipe = (f'<path d="M{mouth[0]:.0f} {mouth[1]:.0f} L{pend[0]:.0f} {pend[1]:.0f}" stroke="{LINE}" stroke-width="16" stroke-linecap="round"/>'
            f'<path d="M{mouth[0]:.0f} {mouth[1]:.0f} L{pend[0]:.0f} {pend[1]:.0f}" stroke="#ece0c4" stroke-width="9" stroke-linecap="round"/>')
    mist = ''
    for _ in range(70):
        t = rnd.random() ** .7; r = 6 + 70 * t
        x = pend[0] + (target[0] + 20 - pend[0]) * t + rnd.uniform(-r, r) * .6; y = pend[1] + (target[1] - 60 - pend[1]) * t + rnd.uniform(-r, r) * .6
        mist += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{rnd.uniform(2, 5.5):.1f}" fill="{rnd.choice(["#e0502e", "#ff7a4a", "#c03a20"])}" opacity="{rnd.uniform(.5, .95):.2f}"/>'
    gx = mouth[0] + (pend[0] - mouth[0]) * .45; gy = mouth[1] + (pend[1] - mouth[1]) * .45
    pipe_arm = limb_to((lx, ly), (gx, gy + .12 * PH), PH, 'cute', 1, 'painter-right', '#8a5a2a', '#c88c62', 'short')
    pelt = (f'<path d="M{PX - .78 * PH:.0f} {PT + 1.3 * PH:.0f} L{PX + .78 * PH:.0f} {PT + 1.22 * PH:.0f} L{PX + .7 * PH:.0f} {PT + 2.95 * PH:.0f} L{PX + .35 * PH:.0f} {PT + 2.8 * PH:.0f} L{PX:.0f} {PT + 3.0 * PH:.0f} L{PX - .35 * PH:.0f} {PT + 2.8 * PH:.0f} L{PX - .72 * PH:.0f} {PT + 2.95 * PH:.0f}Z" fill="#9a6a34" stroke="{LINE}" stroke-width="4" stroke-linejoin="round"/>'
            + ''.join(f'<ellipse cx="{PX + dx * PH:.0f}" cy="{PT + dy * PH:.0f}" rx="{.09 * PH:.0f}" ry="{.06 * PH:.0f}" fill="#5a3a1a" opacity=".7"/>' for dx, dy in ((-.3, 1.7), (.2, 2.0), (-.1, 2.5), (.4, 1.6), (-.45, 2.3), (.45, 2.5)))
            + f'<path d="M{PX - .78 * PH:.0f} {PT + 1.3 * PH:.0f} L{PX + .78 * PH:.0f} {PT + 1.22 * PH:.0f}" stroke="#d8b080" stroke-width="5" opacity=".6"/>')
    band = f'<path d="M{PX - .55 * PH:.0f} {PT + .22 * PH:.0f} Q{PX:.0f} {PT + .1 * PH:.0f} {PX + .55 * PH:.0f} {PT + .22 * PH:.0f}" stroke="#c0402a" stroke-width="{.09 * PH:.0f}" fill="none"/>'
    b += person(PX, PT, PH, 'cute', '#c88c62', ('pony', '#3a1e0e'), '#9a6a34', '#6a4422', '#3a2412', look=(1.6, -1.0), mouth='o', brows='calm',
                deco=pelt, props_front=band + wall_arm + wall_hand + pipe + pipe_arm + mist, rim=(1, '#ffc090'), sleeve_len='short', stance=.3)
    # ---------- watchers by the fire ----------
    # fire
    FX, FY = 640, 930
    b += f'<ellipse cx="{FX}" cy="{FY - 60}" rx="260" ry="200" fill="#ff8a2a" opacity=".45" filter="url(#b32)"/>'
    for k, (dx, a) in enumerate(((-50, -20), (40, 18), (0, 0))):
        b += f'<path d="M{FX + dx - 40} {FY + 20} L{FX + dx + 40} {FY - 10}" stroke="#3a2010" stroke-width="22" stroke-linecap="round" transform="rotate({a} {FX} {FY})"/>'
    b += f'<path d="M{FX - 80} {FY} Q{FX - 90} {FY - 110} {FX - 20} {FY - 200} Q{FX - 20} {FY - 120} {FX + 10} {FY - 100} Q{FX + 30} {FY - 190} {FX + 70} {FY - 230} Q{FX + 110} {FY - 100} {FX + 80} {FY}Z" fill="#ff7a1a" stroke="#c03a10" stroke-width="5"/>'
    b += f'<path d="M{FX - 45} {FY} Q{FX - 50} {FY - 70} {FX} {FY - 130} Q{FX + 20} {FY - 80} {FX + 40} {FY - 140} Q{FX + 70} {FY - 60} {FX + 45} {FY}Z" fill="#ffd25a"/>'
    b += f'<ellipse cx="{FX + 5}" cy="{FY - 30}" rx="35" ry="45" fill="#fff6c0"/>'
    for _ in range(25):
        b += f'<circle cx="{FX + rnd.uniform(-120, 160):.0f}" cy="{FY - rnd.uniform(160, 520):.0f}" r="{rnd.uniform(2, 5):.1f}" fill="#ffc060" opacity="{rnd.uniform(.4, 1):.2f}"/>'
    # child sitting on a rock, looking up at the wall in awe (pointing)
    CX, CT, CH = 960, 545, 84
    rock = f'<path d="M{CX - 110} 940 Q{CX - 120} 870 {CX - 40} 860 Q{CX + 70} 850 {CX + 110} 900 Q{CX + 120} 935 {CX + 100} 945Z" fill="#3a2214" stroke="{LINE}" stroke-width="4"/>'
    b += rock
    kid_pelt = f'<path d="M{CX - 55} {CT + 112} L{CX + 55} {CT + 108} L{CX + 50} {CT + 220} L{CX - 50} {CT + 222}Z" fill="#b07a3a" stroke="{LINE}" stroke-width="3" stroke-linejoin="round"/>'
    kshr = shoulders(CX, CT, CH, 'cute_child')
    point = limb_to(kshr[1], (kshr[1][0] + 70, kshr[1][1] - 60), CH, 'cute_child', -1, 'kid-point', '#b07a3a', '#a8714a', 'short')
    point += hand(kshr[1][0] + 70, kshr[1][1] - 60, 40, CH * .27, 'L', 'back', 'point', skin='#a8714a', line=LINE)
    rest = limb_to(kshr[0], (CX - 30, CT + 2.2 * CH), CH, 'cute_child', -1, 'kid-rest', '#b07a3a', '#a8714a', 'short')
    b += person(CX, CT, CH, 'cute_child', '#a8714a', ('spiky', '#24140a'), '#b07a3a', '#a8714a', '#4a2a14', look=(1.4, -1.2), mouth='o', brows='up',
                deco=kid_pelt, props_front=rest + point, rim=(1, '#ffb070'), sleeve_len='short')
    # elder at the left of the fire, knapping a stone tool with the RIGHT hand
    EX, ET, EH = 330, 620, 80
    eshr = shoulders(EX, ET, EH, 'cute')
    stone = f'<path d="M{EX + 30} {ET + 2.05 * EH} l40 -14 l26 18 l-30 22 l-38 -6Z" fill="#8a8a92" stroke="{LINE}" stroke-width="3"/>'
    hammer_arm = limb_to(eshr[0], (EX - 10, ET + 1.75 * EH), EH, 'cute', 1, 'elder-r', '#7a5a34', '#8f5c3a', 'short')
    hold_arm = limb_to(eshr[1], (EX + 60, ET + 2.15 * EH), EH, 'cute', -1, 'elder-l', '#7a5a34', '#8f5c3a', 'short')
    hammer = f'<ellipse cx="{EX + 10}" cy="{ET + 1.62 * EH}" rx="20" ry="15" fill="#6a6a72" stroke="{LINE}" stroke-width="3"/>'
    beard = f'<path d="M{EX - 30} {ET + 72} Q{EX} {ET + 150} {EX + 30} {ET + 72} Q{EX} {ET + 92} {EX - 30} {ET + 72}Z" fill="#d8d0c0" stroke="{LINE}" stroke-width="3"/>'
    b += person(EX, ET, EH, 'cute', '#8f5c3a', ('bald', '#ccc'), '#7a5a34', '#8f5c3a', '#4a2a14', look=(1.6, -1.2), mouth='o', brows='up', legs=False,
                props_front=beard + stone + hold_arm + hammer + hammer_arm + f'<path d="M{EX + 40} {ET + 1.6 * EH} l20 -12 M{EX + 46} {ET + 1.75 * EH} l24 -4" stroke="#fff6c0" stroke-width="4" stroke-linecap="round"/>', rim=(1, '#ffb070'))
    b += (f'<ellipse cx="{EX - 45}" cy="{ET + 2.75 * EH:.0f}" rx="62" ry="34" fill="#6a4a2a" stroke="{LINE}" stroke-width="4"/><ellipse cx="{EX + 45}" cy="{ET + 2.75 * EH:.0f}" rx="62" ry="34" fill="#6a4a2a" stroke="{LINE}" stroke-width="4"/>'
          f'<rect x="{EX - 190}" y="{ET + 2.95 * EH:.0f}" width="380" height="90" rx="40" fill="#4a2c16" stroke="{LINE}" stroke-width="5"/>'
          f'<ellipse cx="{EX + 190}" cy="{ET + 2.95 * EH + 45:.0f}" rx="26" ry="45" fill="#8a5a30" stroke="{LINE}" stroke-width="4"/><ellipse cx="{EX + 190}" cy="{ET + 2.95 * EH + 45:.0f}" rx="12" ry="22" fill="none" stroke="#5a3a1a" stroke-width="3"/>')
    # frog with a torch and a fur pelt, standing on a rock between the fire and the wall, gazing up at the hands
    torch = ('<g transform="translate(EX EY) rotate(20)"><rect x="-4" y="-70" width="8" height="78" fill="#6a4020" stroke-width="2.4"/>'
             '<ellipse cx="0" cy="-90" rx="28" ry="36" fill="#ff9a2a" opacity=".5" filter="url(#b8)" stroke="none"/>'
             '<path d="M-12 -70 Q-14 -96 0 -112 Q4 -94 10 -100 Q16 -84 12 -70Z" fill="#ffb23a" stroke="#c03a10" stroke-width="2.4"/><path d="M-5 -72 Q-4 -88 2 -96 Q6 -84 6 -72Z" fill="#fff0a0" stroke="none"/></g>BEFORE')
    b += f'<path d="M1100 1000 Q1110 930 1190 920 Q1290 915 1310 990 L1305 1010 L1100 1015Z" fill="#2a160c" stroke="{LINE}" stroke-width="4"/>'
    b += frog(1205, 935, 2.4, look=(4, -5), mouth='O', armL='M-34 -24 q-14 -10 -16 -34', armR='M38 -22 q14 6 16 22',
              mid='<g clip-path="url(#fbody)"><path d="M-50 -30 L60 -44 L60 20 L-50 20Z" fill="#b07a3a" stroke-width="3"/><ellipse cx="-14" cy="-6" rx="7" ry="5" fill="#5a3a1a" stroke="none"/><ellipse cx="24" cy="-20" rx="6" ry="4" fill="#5a3a1a" stroke="none"/><ellipse cx="14" cy="6" rx="7" ry="5" fill="#5a3a1a" stroke="none"/></g>' + f'<path d="{BODY}" fill="none" stroke-width="4"/>',
              hands=(torch, ''), shadow=False)
    b += '<rect width="1920" height="1080" fill="url(#vigC)"/>'
    b += spark(1640, 240, 20, '#ffd8a0') + spark(1250, 120, 14, '#ffd8a0') + spark(1840, 470, 12, '#ffd8a0')
    lines = [('RIGHT-HANDED', 112, 'w'), ('SINCE THE', 112, 'w'), ('STONE AGE', 170, 'y')]
    return page('#1a0d08', svg(d, b), lines, outline='#0e0603', top=44)


if __name__ == '__main__':
    for n, f in (('A', make_A), ('B', make_B), ('C', make_C)):
        open(os.path.join(HERE, f'{n}.html'), 'w').write(f())
    print('ok')
