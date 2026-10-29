# usage: python3 tools/joinpart.py <slug> <uid> <part_group_id> <mover_group_id>
# Moves a tail/leg/neck group INTO the moving body group (at its start, so it stays behind the body) when the body travels (mv-path/glide/swim/creep ...) but the part was drawn outside it
# (miya 2026-10-29: the body moved, the tail stayed behind). The part keeps its own pivot (picture coordinates: the build converts them), so nothing else changes.
import os, sys, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from paths import *
slug, uid, part, mover = sys.argv[1:5]; f = f'{vdir(slug)}/art3/{uid}.svg'; s = open(f).read()
def span(gid):
    m = re.search(r'<g id="%s"[^>]*>' % re.escape(gid), s)
    if not m: sys.exit('no group ' + gid)
    d = 1; j = m.end()
    for t in re.finditer(r'<g[\s>]|</g>', s[j:]):
        d += 1 if t.group(0).startswith('<g') else -1
        if d == 0: return m.start(), j + t.end(), m.end()
a, b, _ = span(part); txt = s[a:b]; s = s[:a] + s[b:]
c, d, ce = span(mover); s = s[:ce] + txt + s[ce:]; open(f, 'w').write(s); print(uid, part, 'moved into', mover)
