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
    # DEFAULT (user decision 2026-10-17: "the earlier pictures were cleaner and the body proportions cuter"): cute style
    'cute':       dict(height=5.5, shoulder_w=1.5, upper=0.85, fore=0.72, palm=0.30, arm_w=0.30, wrist_w=0.20,
                       thigh=1.20, shin=1.15, foot=0.6, neck=0.15),
    'cute_child': dict(height=4.5, shoulder_w=1.3, upper=0.68, fore=0.58, palm=0.27, arm_w=0.28, wrist_w=0.19,
                       thigh=0.90, shin=0.85, foot=0.5, neck=0.1),
    # realistic proportions (only when a scene really needs a realistic figure)
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


def _bez(p0, c, p2, t):
    return ((1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * c[0] + t * t * p2[0], (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * c[1] + t * t * p2[1])


def arm(sx, sy, H, upper=0, bend=15, bend_dir=1, name='arm', side='R', view='palm', pose='flat', hand_tilt=0,
        sleeve='#5f7a8a', skin='#d9a37a', line='#2a1c14', kind='cute', sleeve_len='long', lw=None, amp=None,
        elbow_moves=False, fingers=False):
    """One clean arm (user 2026-10-17: "the detailed elbow joints look strange; use the elbow joint only when the elbow
    moves, the earlier pictures were cleaner"). By default the arm is ONE smooth tapered shape following a gentle curve
    through the elbow (no visible joint, no seam) and moves as ONE mv-limb link from the shoulder. elbow_moves=True splits
    it into upper arm + forearm links (only for a scene where the forearm really swings: waving, hammering, writing).
    fingers=False (default, user 2026-10-17: "use a hand with fingers only where the scene needs fingers, otherwise just round"):
    the hand is a simple round shape like the original pictures. fingers=True draws a hands.py hand (pointing, gripping a visible
    object, a waving close-up, a hand that is the subject of the sentence)."""
    p = P[kind]; bend = max(0.0, min(140.0, float(bend))); hand_tilt = max(-25, min(25, hand_tilt))
    Lu, Lf = p['upper'] * H, p['fore'] * H; w0, w1, w2 = p['arm_w'] * H, p['arm_w'] * 0.85 * H, p['wrist_w'] * H
    def mkhand(x, y, ang):
        if fingers:
            return hand(x, y, ang, p['palm'] * H, side, view, pose, skin=skin, line=line, lw=lw * 0.9)
        r = w2 * 0.78; a = math.radians(ang); cx, cy = x + math.sin(a) * r * 0.55, y - math.cos(a) * r * 0.55
        return f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r:.1f}" fill="{skin}" stroke="{line}" stroke-width="{lw:.2f}"/>'
    lw = lw if lw is not None else max(1.4, H * 0.045)
    ux, uy = _v(upper); E = (sx + ux * Lu, sy + uy * Lu)
    fa = upper + bend * (1 if bend_dir >= 0 else -1)
    fx, fy = _v(fa); W = (E[0] + fx * Lf, E[1] + fy * Lf); S = (sx, sy)
    fore_col = sleeve if sleeve_len == 'long' else skin
    a1 = f' data-amp="{amp[0]}"' if amp else ''; a2 = f' data-amp="{amp[1]}"' if amp else ''
    def outline(pts, widths):
        # one closed path: left side forward, round cap at the end, right side back, round cap at the start
        L, R = [], []
        for k, (x, y) in enumerate(pts):
            a = pts[min(k + 1, len(pts) - 1)]; b = pts[max(k - 1, 0)]
            dx, dy = a[0] - b[0], a[1] - b[1]; m = math.hypot(dx, dy) or 1; nx, ny = -dy / m, dx / m; h = widths[k] / 2
            L.append((x + nx * h, y + ny * h)); R.append((x - nx * h, y - ny * h))
        e, b0 = widths[-1] / 2, widths[0] / 2
        d = f'M{L[0][0]:.1f},{L[0][1]:.1f} ' + ' '.join(f'L{x:.1f},{y:.1f}' for x, y in L[1:])
        d += f' A{e:.1f},{e:.1f} 0 0 0 {R[-1][0]:.1f},{R[-1][1]:.1f} ' + ' '.join(f'L{x:.1f},{y:.1f}' for x, y in reversed(R[:-1]))
        d += f' A{b0:.1f},{b0:.1f} 0 0 0 {L[0][0]:.1f},{L[0][1]:.1f}Z'
        return d
    def silhouette(pts, widths, cols):
        d = outline(pts, widths)
        out = f'<path d="{d}" fill="{cols[0]}" stroke="{line}" stroke-width="{lw:.2f}" stroke-linejoin="round"/>'
        k = next((i for i, c in enumerate(cols) if c != cols[0]), None)   # short sleeve: skin part drawn over the end
        if k is not None:
            out += f'<path d="{outline(pts[k:], widths[k:])}" fill="{cols[k]}" stroke="{line}" stroke-width="{lw:.2f}" stroke-linejoin="round"/>'
        return out
    def cuff(x, y, dx, dy, w):
        L = math.hypot(dx, dy) or 1; dx, dy = dx / L, dy / L; nx, ny = -dy, dx; cx, cy = x - dx * w * 0.9, y - dy * w * 0.9
        return (f'<path d="M{cx + nx * w * 0.55:.1f},{cy + ny * w * 0.55:.1f} L{cx - nx * w * 0.55:.1f},{cy - ny * w * 0.55:.1f}" '
                f'stroke="{line}" stroke-width="{lw * 0.8:.2f}" stroke-linecap="round" opacity=".5"/>') if sleeve_len == 'long' else ''
    if not elbow_moves:
        C = (2 * E[0] - (S[0] + W[0]) / 2, 2 * E[1] - (S[1] + W[1]) / 2)    # the curve passes through the elbow point
        n = 12; pts = [_bez(S, C, W, k / n) for k in range(n + 1)]
        wid = [w0 + (w2 - w0) * (k / n) ** 1.2 for k in range(n + 1)]
        cols = [(sleeve if (sleeve_len == 'long' or k / n < 0.3) else skin) for k in range(n)]
        tx, ty = W[0] - C[0], W[1] - C[1]; ang = math.degrees(math.atan2(tx, ty))
        hnd = mkhand(W[0], W[1], 180 - ang + hand_tilt)
        return (f'<g class="mv mv-limb-{name}-1" data-pivot="{sx:.1f} {sy:.1f}"{a1}>{silhouette(pts, wid, cols)}'
                f'{cuff(W[0], W[1], tx, ty, w2)}{hnd}</g>')
    # elbow really moves: two links, each a clean silhouette; the elbow is a round end hidden under the forearm
    up = silhouette([S, E], [w0, w1], [sleeve if sleeve_len == 'long' else sleeve])
    fo = silhouette([E, W], [w1, w2], [fore_col])
    hnd = mkhand(W[0], W[1], 180 - fa + hand_tilt)
    return (f'<g class="mv mv-limb-{name}-1" data-pivot="{sx:.1f} {sy:.1f}"{a1}>{up}'
            f'<g class="mv mv-limb-{name}-2" data-pivot="{E[0]:.1f} {E[1]:.1f}"{a2}>{fo}{cuff(W[0], W[1], fx, fy, w2)}{hnd}</g></g>')


def shoulders(cx, top, H, kind='cute'):
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
    H = 80
    poses = [  # (viewer-left arm: upper, bend, dir, pose), (viewer-right arm: ...)
        ((-6, 8, 1, 'flat'), (6, 8, -1, 'flat')),          # standing, arms relaxed
        ((-150, 25, -1, 'wave'), (25, 80, 1, 'hold')),      # waving / holding something in front
        ((-30, 95, 1, 'hold'), (165, 12, 1, 'open')),       # hand at the chest / arm raised
    ]
    for i, (L, R) in enumerate(poses):
        cx, top = 250 + i * 420, 40
        (lx, ly), (rx, ry) = shoulders(cx, top, H, 'cute')
        out.append(guide(cx, top, H, 'cute'))
        # figure facing the viewer: its RIGHT arm is on the viewer's LEFT
        out.append(arm(lx, ly, H, L[0], L[1], L[2], f'a{i}r', 'R', 'palm', L[3], kind='cute'))
        out.append(arm(rx, ry, H, R[0], R[1], R[2], f'a{i}l', 'L', 'palm', R[3], kind='cute', elbow_moves=(i == 1)))
    cx, top, H = 1550, 200, 64
    (lx, ly), (rx, ry) = shoulders(cx, top, H, 'cute_child')
    out.append(guide(cx, top, H, 'cute_child'))
    out.append(arm(lx, ly, H, -6, 8, 1, 'c1r', 'R', 'palm', 'flat', kind='cute_child', sleeve='#c0563f', sleeve_len='short'))
    out.append(arm(rx, ry, H, 160, 15, 1, 'c1l', 'L', 'palm', 'wave', kind='cute_child', sleeve='#c0563f', sleeve_len='short'))
    svg = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1900 620" width="1900" height="620">'
           '<rect width="1900" height="620" fill="#efe6d6"/>' + ''.join(out) + '</svg>')
    open(sys.argv[1] if len(sys.argv) > 1 else 'body_test.svg', 'w').write(svg)
