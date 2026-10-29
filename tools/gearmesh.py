# usage: python3 tools/gearmesh.py <svg> <gearA_id> <gearB_id> <angle_deg_A_to_B> [gapfrac]
# Rebuilds two gear groups (mv-rotor-gear-*) so that they MESH (miya 2026-10-29): gear A stays where it is (its data-pivot is its centre, tooth count and
# radii are read from its path), gear B is moved along the line of centres to distance = pitch radius A + pitch radius B, both get a clean tooth profile with the
# phase that interlocks (a tooth of A points at a gap of B), the pivots are the gear centres, and B's period = A's period * teethB / teethA (opposite direction).
# Radii of B are taken from its own tooth count so that the tooth size matches A's tooth size.
import re, sys, math
svg, ga, gb, ang = sys.argv[1], sys.argv[2], sys.argv[3], math.radians(float(sys.argv[4]))
s = open(svg).read()
def grp(gid):
    m = re.search(r'<g id="%s"([^>]*)>' % gid, s); i = m.start(); d = 1; j = m.end()
    for t in re.finditer(r'<g[ >]|</g>', s[j:]):
        d += 1 if t.group(0).startswith('<g') else -1
        if d == 0: return i, j + t.end(), m.group(1)
def info(gid):
    i, j, attrs = grp(gid); seg = s[i:j]; pv = list(map(float, re.search(r'data-pivot="([^"]+)"', attrs).group(1).split()))
    path = re.search(r'<path d="([^"]+)"([^>]*)/>', seg); pts = [(float(a), float(b)) for a, b in re.findall(r'(-?[\d.]+)[ ,](-?[\d.]+)', path.group(1))]
    xs = [p[0] for p in pts]; ys = [p[1] for p in pts]; cx, cy = (min(xs) + max(xs)) / 2, (min(ys) + max(ys)) / 2
    rs = [math.hypot(x - cx, y - cy) for x, y in pts]; tip, root = max(rs), min(rs)
    hub = re.search(r'<circle[^>]*/>', seg); return dict(i=i, j=j, attrs=attrs, pv=pv, n=len(pts) // 2 if False else None, cx=cx, cy=cy, tip=tip, root=root, pts=pts, path_attrs=path.group(2), hub=hub.group(0) if hub else None, seg=seg)
A, B = info(ga), info(gb)
nA = round(len(A['pts']) / 4); nB = round(len(B['pts']) / 4)   # 4 points per tooth in the generator below; old paths: 2 per flank pair -> count teeth by radius peaks
def teeth(pts, cx, cy, tip, root):
    mid = (tip + root) / 2; up = [math.hypot(x - cx, y - cy) > mid for x, y in pts]; return sum(1 for k in range(len(pts)) if up[k] and not up[k - 1])
nA, nB = teeth(A['pts'], A['cx'], A['cy'], A['tip'], A['root']), teeth(B['pts'], B['cx'], B['cy'], B['tip'], B['root'])
pitchA = (A['tip'] + A['root']) / 2; half = (A['tip'] - A['root']) / 2; pitchB = pitchA * nB / nA; D = pitchA + pitchB
cxA, cyA = A['cx'], A['cy']; cxB, cyB = cxA + D * math.cos(ang), cyA + D * math.sin(ang)
def gear(cx, cy, n, pitch, phase):
    tip, root = pitch + half, pitch - half; p = 2 * math.pi / n; pts = []
    for k in range(n):
        c = phase + k * p
        for f, r in ((-0.26, root), (-0.14, tip), (0.14, tip), (0.26, root)): pts.append((cx + r * math.cos(c + f * p), cy + r * math.sin(c + f * p)))
    return 'M' + ' L'.join(f'{x:.1f},{y:.1f}' for x, y in pts) + 'Z'
phA = ang; phB = ang + math.pi + math.pi / nB   # tooth of A on the line of centres <-> gap of B
def rebuild(g, cx, cy, n, pitch, ph, per, direc):
    seg = g['seg']; hubr = re.search(r'r="([\d.]+)"', g['hub']).group(1) if g['hub'] else '14'; hubattrs = re.sub(r'\s(cx|cy)="[^"]*"', '', g['hub'] or '<circle r="14" fill="#e3d4a8" stroke="#1d2b1c" stroke-width="2.5"/>')
    hub = hubattrs.replace('<circle', f'<circle cx="{cx:.1f}" cy="{cy:.1f}"', 1)
    attrs = re.sub(r'data-pivot="[^"]*"', f'data-pivot="{cx:.0f} {cy:.0f}"', g['attrs']); attrs = re.sub(r'data-per="[^"]*"', f'data-per="{per:g}"', attrs)
    return f'<g id="{ga if g is A else gb}"{attrs}><path d="{gear(cx, cy, n, pitch, ph)}"{g["path_attrs"]}/>{hub}</g>'
perA = float(re.search(r'data-per="([^"]+)"', A['attrs']).group(1)); perB = perA * nB / nA
newA = rebuild(A, cxA, cyA, nA, pitchA, phA, perA, 1); newB = rebuild(B, cxB, cyB, nB, pitchB, phB, perB, -1)
for g, new in sorted(((A, newA), (B, newB)), key=lambda t: -t[0]['i']): s = s[:g['i']] + new + s[g['j']:]
open(svg, 'w').write(s); print(f'teeth {nA}/{nB}  A=({cxA:.0f},{cyA:.0f}) B=({cxB:.0f},{cyB:.0f}) dist {D:.0f} periods {perA:g}/{perB:g}')
