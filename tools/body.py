# Human proportions and arms for picture agents (2026-10-17, user: "the elbows bend strangely and the arms are far too long,
# grotesque. Think of human proportions, and organise it so every future picture with people uses it").
# Use together with tools/hands.py (art_spec 6A/6B).
#
#   import sys; sys.path.insert(0, '/home/user/rp/tools'); from body import arm, P
#   svg += arm(sx, sy, H, upper=10, bend=20, name='lefty-l', side='L', view='palm', pose='open',
#              sleeve='#e2a33a', skin='#8a5a3a', line='#2a1c14', kind='adult', sleeve_len='long')
#
# H = the figure's HEAD HEIGHT in px (chin to top of head). Everything is measured in heads, like a figure-drawing course.
# (sx, sy) = the SHOULDER joint (inside the top corner of the torso, about 0.25 H below the shoulder line, NOT at the neck).
# upper = direction of the upper arm in degrees: 0 = hanging straight down, +90 = out to the viewer's right, -90 = to the
#         viewer's left, +/-180 = straight up. bend = elbow flexion 0..140 degrees (0 = straight arm). bend_dir = +1 or -1:
#         the side the forearm folds to (+1 = counter-clockwise on screen). The forearm can only FOLD (never bend backwards),
#         so choose bend_dir once per arm and keep bend >= 0.
# hand: side/view/pose as in tools/hands.py; hand_tilt bends the wrist (-25..25 degrees).
#
# The arm comes out as a 2-link limb ready for animation: <g class="mv mv-limb-<name>-1" data-pivot="shoulder"> upper arm
# <g class="mv mv-limb-<name>-2" data-pivot="elbow"> forearm + hand </g></g>. build3 moves mv-limb links gently and IN STEP
# (upper arm about 2.5 deg, forearm about 2 deg, 2.4 s), unlike creature chains (mv-chain) whose tips whip in a wave.

import math, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from hands import hand, _capsule

# Proportions in head heights (H). Adult ~7.5 heads tall, child (~6 years) ~5.5 heads, toddler ~4.5 heads.
P = {
    'adult':   dict(height=7.5, shoulder_w=2.0, upper=1.35, fore=1.10, palm=0.42, arm_w=0.38, wrist_w=0.23,
                    thigh=1.95, shin=1.85, foot=1.0, neck=0.35),
    'child':   dict(height=5.5, shoulder_w=1.6, upper=1.00, fore=0.85, palm=0.36, arm_w=0.34, wrist_w=0.21,
                    thigh=1.35, shin=1.25, foot=0.75, neck=0.2),
    'toddler': dict(height=4.5, shoulder_w=1.4, upper=0.80, fore=0.70, palm=0.32, arm_w=0.33, wrist_w=0.21,
                    thigh=1.0, shin=0.95, foot=0.6, neck=0.1),
}
# Checks every drawing of a standing person must pass (art_spec 6B):
#  - arm hanging straight: elbow at the waist, wrist at the crotch / top of the thigh, fingertips at mid-thigh. Never below the knee.
#  - upper arm (shoulder->elbow) is LONGER than the forearm (elbow->wrist); forearm + hand is about as long as the upper arm + 0.5 H.
#  - shoulders 2 H wide for adults; the shoulder joint sits inside the torso outline, not at the neck or outside the body.
#  - elbows only fold (0-140 deg), never bend backwards, never a kink with two elbows; the elbow is a smooth round joint.
#  - legs: hip joint at mid-height of the figure (adult 3.75 H from the top of the head); knee halfway between hip and ankle.


def _v(a_deg):   # direction vector, 0 = down, +90 = viewer's right
    a = math.radians(a_deg); return math.sin(a), math.cos(a)


def arm(sx, sy, H, upper=0, bend=15, bend_dir=1, name='arm', side='R', view='palm', pose='flat', hand_tilt=0,
        sleeve='#5f7a8a', skin='#d9a37a', line='#2a1c14', kind='adult', sleeve_len='long', lw=None, amp=None):
    p = P[kind]; bend = max(0.0, min(140.0, float(bend))); hand_tilt = max(-25, min(25, hand_tilt))
    Lu, Lf = p['upper'] * H, p['fore'] * H; w0, w1, w2 = p['arm_w'] * H, p['arm_w'] * 0.82 * H, p['wrist_w'] * H
    lw = lw if lw is not None else max(1.4, H * 0.045)
    ux, uy = _v(upper); ex, ey = sx + ux * Lu, sy + uy * Lu
    fa = upper + bend * (1 if bend_dir >= 0 else -1)
    fx, fy = _v(fa); wx, wy = ex + fx * Lf, ey + fy * Lf
    up_col = sleeve
    fore_col = sleeve if sleeve_len == 'long' else skin
    def seg(x0, y0, x1, y1, a, b, col):
        d = _capsule(x0, y0, x1, y1, a, b)
        return (f'<path d="{d}" fill="{line}" stroke="{line}" stroke-width="{2 * lw:.2f}" stroke-linejoin="round"/>',
                f'<path d="{d}" fill="{col}" stroke="none"/>')
    u_out, u_in = seg(sx, sy, ex, ey, w0, w1, up_col)
    f_out, f_in = seg(ex, ey, wx - fx * w2 * 0.3, wy - fy * w2 * 0.3, w1, w2, fore_col)
    if sleeve_len == 'short':   # sleeve covers the top 55 % of the upper arm, the rest is skin
        mx, my = sx + ux * Lu * 0.55, sy + uy * Lu * 0.55
        so, si = seg(sx, sy, mx, my, w0 * 1.08, w0 * 1.0, sleeve)
        u_in = f'<path d="{_capsule(sx, sy, ex, ey, w0, w1)}" fill="{skin}" stroke="none"/>' + so + si
    elbow = f'<circle cx="{ex:.1f}" cy="{ey:.1f}" r="{w1 / 2:.1f}" fill="{fore_col if sleeve_len == "long" else skin}" stroke="none"/>'
    cuff = ''
    if sleeve_len == 'long':    # a thin cuff line near the wrist
        cx, cy = wx - fx * w2 * 0.9, wy - fy * w2 * 0.9; nx, ny = -fy, fx
        cuff = (f'<path d="M{cx + nx * w2 * 0.55:.1f},{cy + ny * w2 * 0.55:.1f} L{cx - nx * w2 * 0.55:.1f},{cy - ny * w2 * 0.55:.1f}" '
                f'stroke="{line}" stroke-width="{lw * 0.8:.2f}" stroke-linecap="round" opacity=".55"/>')
    hnd = hand(wx, wy, 180 - fa + hand_tilt, p['palm'] * H, side, view, pose, skin=skin, line=line, lw=lw * 0.9)
    a1 = f' data-amp="{amp[0]}"' if amp else ''; a2 = f' data-amp="{amp[1]}"' if amp else ''
    return (f'<g class="mv mv-limb-{name}-1" data-pivot="{sx:.1f} {sy:.1f}"{a1}>{u_out}{u_in}'
            f'<g class="mv mv-limb-{name}-2" data-pivot="{ex:.1f} {ey:.1f}"{a2}>{f_out}{f_in}{elbow}{cuff}{hnd}</g></g>')


def shoulders(cx, top, H, kind='adult'):
    """shoulder joints for a figure facing the viewer: cx = body centre, top = top of the head. Returns (left_xy, right_xy)."""
    p = P[kind]; y = top + H + p['neck'] * H + 0.25 * H; hw = p['shoulder_w'] * H / 2 - p['arm_w'] * H * 0.45
    return (cx - hw, y), (cx + hw, y)


if __name__ == '__main__':   # test sheet: python3 tools/body.py out.svg  (adult 7.5 heads, child; arms down / raised / bent)
    out = []
    def guide(cx, top, H, kind):
        p = P[kind]; n = p['height']
        g = ''.join(f'<line x1="{cx - 150}" y1="{top + k * H:.0f}" x2="{cx + 150}" y2="{top + k * H:.0f}" stroke="#b9a98f" stroke-width="1"/>' for k in range(int(n) + 1))
        hip = top + n * H / 2
        body = (f'<ellipse cx="{cx}" cy="{top + H / 2}" rx="{H * 0.38:.0f}" ry="{H / 2:.0f}" fill="#d9a37a" stroke="#2a1c14" stroke-width="3"/>'
                f'<rect x="{cx - p["shoulder_w"] * H / 2:.0f}" y="{top + H + p["neck"] * H:.0f}" width="{p["shoulder_w"] * H:.0f}" height="{hip - top - H - p["neck"] * H:.0f}" rx="{H * 0.3:.0f}" fill="#5f7a8a" stroke="#2a1c14" stroke-width="3"/>'
                f'<rect x="{cx - H * 0.62:.0f}" y="{hip:.0f}" width="{H * 0.55:.0f}" height="{(p["thigh"] + p["shin"]) * H:.0f}" rx="{H * 0.2:.0f}" fill="#33333d" stroke="#2a1c14" stroke-width="3"/>'
                f'<rect x="{cx + H * 0.07:.0f}" y="{hip:.0f}" width="{H * 0.55:.0f}" height="{(p["thigh"] + p["shin"]) * H:.0f}" rx="{H * 0.2:.0f}" fill="#33333d" stroke="#2a1c14" stroke-width="3"/>')
        return g + body
    H = 64
    poses = [  # (viewer-left arm: upper, bend, dir, pose), (viewer-right arm: ...)
        ((-6, 8, 1, 'flat'), (6, 8, -1, 'flat')),          # standing, arms relaxed
        ((-150, 25, -1, 'wave'), (25, 80, 1, 'hold')),      # waving / holding something in front
        ((-30, 95, 1, 'hold'), (165, 12, 1, 'open')),       # hand at the chest / arm raised
    ]
    for i, (L, R) in enumerate(poses):
        cx, top = 250 + i * 420, 40
        (lx, ly), (rx, ry) = shoulders(cx, top, H)
        out.append(guide(cx, top, H, 'adult'))
        # figure facing the viewer: its RIGHT arm is on the viewer's LEFT
        out.append(arm(lx, ly, H, L[0], L[1], L[2], f'a{i}r', 'R', 'palm', L[3]))
        out.append(arm(rx, ry, H, R[0], R[1], R[2], f'a{i}l', 'L', 'palm', R[3]))
    cx, top, H = 1550, 200, 64
    (lx, ly), (rx, ry) = shoulders(cx, top, H, 'child')
    out.append(guide(cx, top, H, 'child'))
    out.append(arm(lx, ly, H, -6, 8, 1, 'c1r', 'R', 'palm', 'flat', kind='child', sleeve='#c0563f', sleeve_len='short'))
    out.append(arm(rx, ry, H, 160, 15, 1, 'c1l', 'L', 'palm', 'wave', kind='child', sleeve='#c0563f', sleeve_len='short'))
    svg = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1900 620" width="1900" height="620">'
           '<rect width="1900" height="620" fill="#efe6d6"/>' + ''.join(out) + '</svg>')
    open(sys.argv[1] if len(sys.argv) > 1 else 'body_test.svg', 'w').write(svg)
