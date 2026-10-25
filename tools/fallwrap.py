# usage: python3 tools/fallwrap.py <art.svg> <first-needle> <last-needle> '<path d>' [dur] [delay] [name]
# Wraps the whole object (from the element containing <first-needle> to the end of the sibling element that contains <last-needle>, tail/joint groups included)
# in <g id="mv-path-<name>" data-path=... data-rot="0"> so a falling/sinking object really moves across the frame (path coordinates = picture coordinates, start = object's place).
import sys, re
f, a, b, d = sys.argv[1:5]; dur = sys.argv[5] if len(sys.argv) > 5 else '6.5'; dl = sys.argv[6] if len(sys.argv) > 6 else '.4'; nm = sys.argv[7] if len(sys.argv) > 7 else 'sink'
s = open(f, encoding='utf-8').read()
i = s.index(a); i = s.rfind('<', 0, i + 1) if s[i] != '<' else i
j = s.index(b, i)
# end of the element containing b: balance <g>..</g> if it opens a group, else the self-closed/closed tag
k = s.rfind('<', 0, j + 1); depth = 0; pos = k
m = re.compile(r'<(/?)(g)\b[^>]*?(/?)>|<(/?)(path|circle|ellipse|rect|polygon|line)\b[^>]*?(/?)>')
if re.match(r'<g\b', s[k:]):
    for mm in m.finditer(s, k):
        if mm.group(2) == 'g':
            depth += -1 if mm.group(1) else 1
            if depth == 0: pos = mm.end(); break
else:
    pos = s.index('>', k) + 1
out = s[:i] + f'<g id="mv-path-{nm}" data-path="{d}" data-rot="0" data-delay="{dl}" data-dur="{dur}">' + s[i:pos] + '</g>' + s[pos:]
open(f, 'w', encoding='utf-8').write(out); print('wrapped', len(s[i:pos]), 'chars')
