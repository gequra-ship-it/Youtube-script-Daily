# Frog-eye check (miya 2026-11-07, guideline 16-9): the black pupil must lie fully inside the white of the eye (small shorts screens
# show only the white otherwise). Parses thumb HTML written by the shared frog() (white r=13.5 circle + pupil circle right after it).
# usage: python3 tools/eyecheck.py file.html [...]   -> prints bad eyes, exit 1 if any
import re, sys, math
PAT = re.compile(r'<circle cx="([-\d.]+)" cy="([-\d.]+)" r="([\d.]+)" fill="#f4f5ea"[^>]*/>\s*<circle cx="([-\d.]+)" cy="([-\d.]+)" r="([\d.]+)"')
def check(path, margin=1.6 + .5):
    bad = []; n = 0
    for m in PAT.finditer(open(path, encoding='utf-8').read()):
        wx, wy, wr, px, py, pr = map(float, m.groups()); n += 1
        if math.hypot(px - wx, py - wy) + pr > wr - margin: bad.append((wx, wy, round(math.hypot(px - wx, py - wy) + pr, 1), wr))
    return n, bad
if __name__ == '__main__':
    rc = 0
    for p in sys.argv[1:]:
        n, bad = check(p)
        print(p, 'eyes', n, 'BAD' if bad else 'ok', bad if bad else '')
        rc |= bool(bad)
    sys.exit(rc)
