# usage: python3 tools/splitclumps.py <slug> <uid> <group_id> [gap=300]
# A sway group that holds SEVERAL clumps far apart (reeds left + right) turns about one base for all of them. Splits its (flat) children by x into one group per clump
# (<id>, <id>-2, ...), removes the old data-pivot; then run `python3 tools/setbase.py <slug> <uid>` to write the foot of each clump.
import os, sys, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from paths import *
slug, uid, gid = sys.argv[1:4]; gap = float(sys.argv[4]) if len(sys.argv) > 4 else 300
f = f'{vdir(slug)}/art3/{uid}.svg'; s = open(f).read()
m = re.search(r'<g id="%s"[^>]*>' % re.escape(gid), s); i = m.end(); j = s.find('</g>', i); inner = s[i:j]
els = re.findall(r'<(?:path|ellipse|circle|line|rect|polygon)[^>]*?/>', inner)
if ''.join(els) != inner: sys.exit(f'{gid}: not a flat group, split it by hand')
def x(e):
    mm = re.search(r' d="M\s*(-?[\d.]+)', e) or re.search(r'c?x="(-?[\d.]+)"', e) or re.search(r'x1="(-?[\d.]+)"', e) or re.search(r'points="(-?[\d.]+)', e); return float(mm.group(1)) if mm else 0
order = sorted(els, key=x); cl = []
for e in order:
    if cl and x(e) - x(cl[-1][-1]) < gap: cl[-1].append(e)
    else: cl.append([e])
if len(cl) < 2: sys.exit('one clump only')
new = ''.join(f'<g id="{gid}{"" if k == 0 else "-%d" % (k + 1)}">{"".join(c)}</g>' for k, c in enumerate(cl))
s = s[:m.start()] + new + s[j + 4:]; open(f, 'w').write(s); print(uid, gid, '->', len(cl), 'groups')
