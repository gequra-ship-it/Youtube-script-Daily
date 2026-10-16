# Re-use existing pictures after a unit re-split (pacing change, HOOK/SLOW change, 2026-10-16).
# usage: SLUG=<slug> python3 tools/remap_art.py <old_plan.json> [<new_plan.json>]
#   old plan = plan.json saved BEFORE the re-split (its uids match the current art3 files)
#   new plan = plan.json written by `PLAN=1 python3 tools/build3.py` after the config change (default: videos/<slug>/plan.json)
# Each new unit takes the picture of the old unit it overlaps most (same scene, by narration characters).
# Sidecar: copied from that old unit; number badges and sound cues of the other overlapped old units are carried over
# when their word is still in the new unit's text (name labels / bubbles stay with their own picture only);
# focus_word / sfx words that are no longer in the text are dropped. Old art is kept in $MIYA_WORK/<slug>/art3_prev/ for undo.
import json, os, shutil, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from paths import *

old = json.load(open(sys.argv[1]))
new = json.load(open(sys.argv[2] if len(sys.argv) > 2 else f'{vdir()}/plan.json'))
A = f'{vdir()}/art3'; P = f'{wdir()}/art3_prev'


def ranges(plan):
    """uid -> (scene, c0, c1) by finding each unit's text in order inside its scene's concatenated text"""
    out = {}; pos = {}
    full = {}
    for u in plan:
        full.setdefault(u['scene'], []).append(u['text'])
    for u in plan:
        sc = u['scene']; t = ' '.join(full[sc]); p = pos.get(sc, 0)
        j = t.find(u['text'], p); j = p if j < 0 else j
        out[u['uid']] = (sc, j, j + len(u['text'])); pos[sc] = j + len(u['text'])
    return out


def norm(plan):   # character offsets over whitespace-normalised scene text so old and new splits line up
    return ranges([dict(u, text=' '.join(u['text'].split())) for u in plan])


ro, rn = norm(old), norm(new)
if os.path.exists(P): shutil.rmtree(P)
shutil.copytree(A, P)
for f in os.listdir(A):
    if f.endswith('.svg') or f.endswith('.json'): os.remove(f'{A}/{f}')
report = []
for u in new:
    sc, a, b = rn[u['uid']]
    ov = sorted(((min(b, c1) - max(a, c0), uid) for uid, (s2, c0, c1) in ro.items() if s2 == sc and min(b, c1) > max(a, c0)), reverse=True)
    if not ov or not os.path.exists(f'{P}/{ov[0][1]}.svg'):
        report.append(f'{u["uid"]}: NO ART'); continue
    base = ov[0][1]; text = u['text']
    shutil.copy(f'{P}/{base}.svg', f'{A}/{u["uid"]}.svg')
    sd = json.load(open(f'{P}/{base}.json')) if os.path.exists(f'{P}/{base}.json') else {}
    if sd.get('focus_word') and sd['focus_word'] not in text:
        sd.pop('focus_word')
    sd['sfx'] = [e for e in sd.get('sfx', []) if not e.get('word') or e['word'] in text]
    labs = [l for l in sd.get('labels', []) if (l.get('word') or str(l.get('text', ''))) in text]
    for _, uid in ov[1:]:
        if not os.path.exists(f'{P}/{uid}.json'): continue
        o = json.load(open(f'{P}/{uid}.json'))
        for l in o.get('labels', []):
            if l['type'] == 'num' and (l.get('word') or str(l['text'])) in text and len(labs) < 3 and not any(x['type'] == 'num' for x in labs):
                labs.append(l)
        for e in o.get('sfx', []):
            if e.get('word') and e['word'] in text and not any(x.get('word') == e['word'] for x in sd['sfx']):
                sd['sfx'].append(e)
    if labs: sd['labels'] = labs
    else: sd.pop('labels', None)
    if not sd['sfx']: sd.pop('sfx')
    json.dump(sd, open(f'{A}/{u["uid"]}.json', 'w'), ensure_ascii=False, indent=1)
    report.append(f'{u["uid"]} <- {base}' + (f' (+{len(ov) - 1} merged)' if len(ov) > 1 else ''))
print('\n'.join(report)); print(f'{len(new)} units (was {len(old)}); previous art kept in {P}')
