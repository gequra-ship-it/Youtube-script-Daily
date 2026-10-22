# Shared hand drawing for picture agents (2026-10-17, user: "the thumbs bend at grotesque angles and are far too long").
# Agents must draw every visible hand with this module instead of free-hand paths.
#
#   import sys; sys.path.insert(0, 'tools')  # run from the repo root; from hands import hand
#   svg += hand(x, y, angle=0, size=120, side='L', view='palm', pose='open', skin='#c98f63', line='#2b1d14')
#
# (x, y)  = centre of the WRIST (where the forearm ends), in picture coordinates.
# angle   = direction the fingers point, degrees clockwise from straight up (0 = up, 90 = right, 180 = down).
# size    = palm length in px (wrist to the knuckles). Whole hand with fingers is about 1.95 x size tall.
# side    = 'L' or 'R' (whose hand it is). view = 'palm' (palm toward the viewer) or 'back'.
#           Thumb position follows anatomy: right palm / left back -> thumb on the viewer's right (fingers up);
#           left palm / right back -> thumb on the viewer's left.
# pose    = 'open' (fingers slightly spread), 'flat' (fingers together, pressed on a wall), 'point' (index finger out),
#           'fist', 'wave' (open, a little more spread), 'hold' (fingers wrapped round a horizontal handle at the palm top).
# Proportions (palm length = 1): middle finger 0.94, index 0.84, ring 0.87, little 0.68; the thumb starts on the side of
# the palm low down (0.30 above the wrist), leans out 22-40 degrees and is only 0.58 long: its tip ends level with
# the index knuckle, never above the middle of the index finger, and it is never hooked or bent backwards.
# Outline: drawn as one silhouette (thick dark under-stroke, fill on top), so no seams between fingers and palm.
import math


def _rot(px, py, a):
    c, s = math.cos(a), math.sin(a)
    return px * c - py * s, px * s + py * c


def _capsule(x0, y0, x1, y1, w0, w1):
    """tapered capsule from (x0,y0) (width w0) to (x1,y1) (width w1) as a path in local units"""
    dx, dy = x1 - x0, y1 - y0; L = math.hypot(dx, dy) or 1e-6; nx, ny = -dy / L, dx / L
    a = (x0 + nx * w0 / 2, y0 + ny * w0 / 2); b = (x1 + nx * w1 / 2, y1 + ny * w1 / 2)
    c = (x1 - nx * w1 / 2, y1 - ny * w1 / 2); d = (x0 - nx * w0 / 2, y0 - ny * w0 / 2)
    return ('M{:.4f},{:.4f} L{:.4f},{:.4f} A{:.4f},{:.4f} 0 0 0 {:.4f},{:.4f} L{:.4f},{:.4f} A{:.4f},{:.4f} 0 0 0 {:.4f},{:.4f} Z'
            .format(*a, *b, w1 / 2, w1 / 2, *c, *d, w0 / 2, w0 / 2, *a))


def _finger(bx, by, length, width, ang_deg, curl=0.0):
    """finger from base (bx,by) pointing up rotated by ang (deg, + = toward +x); curl 0..1 folds it down over the palm"""
    a = math.radians(ang_deg)
    if curl <= 0:
        tx, ty = bx + math.sin(a) * length, by - math.cos(a) * length
        return [_capsule(bx, by, tx, ty, width, width * 0.86)]
    # curled: a short knuckle stub pointing up then folding forward (drawn as a rounded block over the palm top)
    k = length * 0.42
    return [_capsule(bx, by + 0.02, bx + math.sin(a) * k, by - math.cos(a) * k, width * 1.02, width * 0.98)]


def _shapes(pose, ts):
    """local shapes (hand pointing up, wrist centre at 0,0, palm length 1). ts = +1 thumb on +x side, -1 on -x side."""
    S = []
    # palm: rounded trapezoid, wrist 0.74 wide, knuckles 0.96 wide; the thumb side bulges (thenar pad)
    wr, kn, top = 0.37, 0.48, -1.0
    t = ts
    palm = ('M{:.3f},0 C{:.3f},0.04 {:.3f},0.04 {:.3f},0 '
            'C{:.3f},-0.25 {:.3f},-0.62 {:.3f},{:.3f} '
            'C{:.3f},{:.3f} {:.3f},{:.3f} {:.3f},{:.3f} '
            'C{:.3f},-0.62 {:.3f},-0.22 {:.3f},0 Z').format(
        -wr * t, -wr * 0.3 * t, wr * 0.3 * t, wr * t,
        (wr + 0.13) * t, (kn + 0.03) * t, kn * t, top + 0.04,
        kn * 0.6 * t, top - 0.05, -kn * 0.6 * t, top - 0.05, -kn * t, top + 0.08,
        -(kn + 0.01) * t, -(wr + 0.02) * t, -wr * t)
    S.append(palm)
    O = []   # overlays: drawn after the silhouette, each with its own outline (folded thumb, curled fingers)
    # fingers: index next to the thumb, little finger on the far side (middle finger about as long as the palm)
    xs = [0.355, 0.12, -0.12, -0.35]             # index, middle, ring, little (times ts)
    bys = [-0.97, -1.0, -0.98, -0.90]
    lens = [0.84, 0.94, 0.87, 0.68]
    wids = [0.215, 0.225, 0.215, 0.185]
    spread = {'open': [7, 2, -3, -9], 'wave': [11, 3, -5, -14], 'flat': [1.5, 0.5, -0.5, -1.5],
              'point': [2, 0, 0, 0], 'fist': [0, 0, 0, 0], 'hold': [0, 0, 0, 0]}[pose]
    for i in range(4):
        curled = pose in ('fist', 'hold') or (pose == 'point' and i > 0)
        if not curled:
            S += _finger(xs[i] * t, bys[i], lens[i], wids[i], spread[i] * t)
        else:   # curled finger seen from the front: a rounded roll lying over the top of the palm
            O.append(_capsule(xs[i] * t, bys[i] + 0.03, xs[i] * t, bys[i] + 0.40, wids[i] * 1.1, wids[i] * 1.1))
    # thumb: base low on the thumb side of the palm, leaning out, short, tip at about the index knuckle height
    if pose in ('fist', 'hold', 'point'):
        # thumb folded across the front of the curled fingers (short, ends at the middle finger)
        O.append(_capsule(0.47 * t, -0.40, 0.02 * t, -0.55, 0.27, 0.23))
    else:
        lean = {'open': 34, 'wave': 40, 'flat': 22}[pose]
        a = math.radians(lean)
        bx, by = 0.34 * t, -0.30
        mx, my = bx + math.sin(a) * 0.32 * t, by - math.cos(a) * 0.32
        a2 = math.radians(lean - 12)            # tip segment turns slightly TOWARD the fingers (never outward)
        tx, ty = mx + math.sin(a2) * 0.26 * t, my - math.cos(a2) * 0.26
        S.append(_capsule(bx, by, mx, my, 0.27, 0.235))
        S.append(_capsule(mx, my, tx, ty, 0.235, 0.205))
    return S, O


def hand(x, y, angle=0, size=120, side='R', view='palm', pose='open', skin='#d9a37a', line='#2a1c14', lw=None,
         creases=True, gid=None):
    side = side.upper()[0]; view = view.lower()
    ts = 1 if (side == 'R') == (view == 'palm') else -1
    k = size; lw = lw if lw is not None else max(1.6, size * 0.028)
    shapes, over = _shapes(pose, ts)
    tr = f'translate({x:.1f} {y:.1f}) rotate({angle:.2f}) scale({k:.3f})'
    w = lw / k
    g = [f'<g{f" id={chr(34)}{gid}{chr(34)}" if gid else ""} transform="{tr}">']
    g.append(f'<g fill="{line}" stroke="{line}" stroke-width="{2 * w:.4f}" stroke-linejoin="round">' + ''.join(f'<path d="{d}"/>' for d in shapes) + '</g>')
    g.append(f'<g fill="{skin}" stroke="none">' + ''.join(f'<path d="{d}"/>' for d in shapes) + '</g>')
    for d in over:   # curled fingers / folded thumb: outlined so they read in front of the palm
        g.append(f'<path d="{d}" fill="{skin}" stroke="{line}" stroke-width="{w:.4f}" stroke-linejoin="round"/>')
    if creases and pose not in ('fist', 'hold', 'point'):
        cw = w * 0.7
        if view == 'palm':   # two soft palm lines
            g.append(f'<g fill="none" stroke="{line}" stroke-width="{cw:.4f}" stroke-linecap="round" opacity=".45">'
                     f'<path d="M{-0.30 * ts:.3f},-0.70 Q{0.0:.3f},-0.62 {0.22 * ts:.3f},-0.74"/>'
                     f'<path d="M{0.22 * ts:.3f},-0.52 Q{0.05 * ts:.3f},-0.36 {0.10 * ts:.3f},-0.12"/></g>')
        else:                # knuckle hints on the back of the hand
            g.append(f'<g fill="none" stroke="{line}" stroke-width="{cw:.4f}" stroke-linecap="round" opacity=".35">'
                     + ''.join(f'<path d="M{(xx - 0.05) * ts:.3f},-0.93 q{0.05 * ts:.3f},-0.03 {0.10 * ts:.3f},0"/>' for xx in (0.355, 0.12, -0.12, -0.35)) + '</g>')
    g.append('</g>')
    return ''.join(g)


if __name__ == '__main__':   # test sheet: python3 tools/hands.py out.svg
    import sys
    cells = []
    poses = ['open', 'flat', 'wave', 'point', 'fist', 'hold']
    for r, (side, view) in enumerate([('R', 'palm'), ('L', 'palm'), ('R', 'back'), ('L', 'back')]):
        for c, pose in enumerate(poses):
            cx, cy = 140 + c * 290, 260 + r * 260
            cells.append(hand(cx, cy, 0, 110, side, view, pose))
    cells.append(hand(1900, 600, 90, 110, 'L', 'palm', 'open')); cells.append(hand(1850, 900, -35, 90, 'R', 'back', 'point'))
    svg = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 2000 1100" width="2000" height="1100">'
           '<rect width="2000" height="1100" fill="#efe6d6"/>' + ''.join(cells) + '</svg>')
    open(sys.argv[1] if len(sys.argv) > 1 else 'hands_test.svg', 'w').write(svg)
