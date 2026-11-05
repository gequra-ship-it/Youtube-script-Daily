# usage: python3 tools/figcheck.py <slug> [uid..] [--strict]
# 2026-11-05 (miya: "agents draw hands badly -> pre-drawn library"; people stay as they are): every hand with fingers must come from
# tools/figlib.py hand() (stamps data-fig="hand:<pose>"), see art_spec 6A. This lists groups whose NAME says hand/fist/finger...
# but that contain no data-fig element, i.e. drawn free-hand (round body.arm hands have no such name and are fine).
# Exit 0 always (final_check prints the lines as WARN: old videos were drawn before the library); --strict exits 1 when any.
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from paths import vdir

PEOPLE = re.compile(r'(?<![a-z])(hand|hands|fist|fists|palm|palms|finger|fingers|thumb|knuckles?)(?![a-z])', re.I)   # hands only (miya 2026-11-05: people stay as they are)
SKIP = re.compile(r'(frog|robot|statue|skeleton|shadow|silhouette|stencil|print|icon|chart|label|text|bubble|band|clock|glove|mitten|'
                  r'arm(ou|o)r|armchair|armada|handle|handrail|hand-?writing|second-?hand|manuscript|mantle|mane|humanity-?label|'
                  r'squid|octopus|starfish|crab|beetle|insect|spider|monkey|ape|bear|tree|branch|lever|crane|anemone|coral|galaxy|spiral)', re.I)


def check(slug, uids=None):
    d = f'{vdir(slug)}/art3'; out = []
    if not os.path.isdir(d):
        return out
    for f in sorted(os.listdir(d)):
        if not f.endswith('.svg') or (uids and f[:-4] not in uids):
            continue
        s = open(f'{d}/{f}', encoding='utf-8').read(); seen_to = -1
        for m in re.finditer(r'<g\b[^>]*\b(?:id|class)="([^"]*)"[^>]*>', s):
            name = m.group(1)
            if m.start() < seen_to or not PEOPLE.search(name) or SKIP.search(name):   # one report per outermost people group
                continue
            # the group's own extent: up to its closing tag (depth count)
            i = m.end(); depth = 1
            for t in re.finditer(r'<g\b|</g>', s[i:]):
                depth += 1 if t.group() == '<g' else -1
                if depth == 0:
                    j = i + t.start(); break
            else:
                j = len(s)
            body = s[m.start():j]
            if 'data-fig=' in body:
                seen_to = j; continue
            seen_to = j; out.append((f[:-4], name))
    return out


if __name__ == '__main__':
    args = [a for a in sys.argv[1:] if not a.startswith('--')]; strict = '--strict' in sys.argv
    slug = args[0] if args else os.environ.get('SLUG')
    bad = check(slug, set(args[1:]) or None)
    for uid, name in bad:
        print(f'WARN {uid}: group "{name}" looks like a hand but was not drawn with tools/figlib.py (no data-fig inside)')
    print(f'figcheck: {len(bad)} free-hand hand group(s)' + (' — redraw with figlib.hand()' if bad else ' (OK)'))
    sys.exit(1 if (bad and strict) else 0)
