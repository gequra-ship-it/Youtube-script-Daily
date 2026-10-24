# usage: python3 tools/frog_auto.py <slug>...   Fills the frog explainer keys (moods / outfit / one hop / safe y) of every frog unit sidecar from the unit's text.
# Existing x, y, s, flip, point stay the base; run once, then hand-tune. Rules: guideline 7-2.
import json, re, sys, glob, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SPACE = re.compile(r'\b(space|star|stars|galax\w*|cosmic|universe|horizon|probe|voyager|light|planet|orbit|dark|expan\w*)\b', re.I)
SEA = re.compile(r'\b(ocean|sea|underwater|dive|water)\b', re.I)
def mood_of(s):
    if s.rstrip().endswith('?'): return 'curious'
    if s.rstrip().endswith('!'): return 'excited'
    if re.search(r'\b(never|impossible|terrifying|trapped|lost|prison|dark|fade|alone|gone)\b', s, re.I): return 'worried'
    if re.search(r'\d|\b(billion|million|thousand|trillion|faster|fastest)\b', s, re.I): return 'surprised'
    if re.search(r'\b(but|however|yet|actually|here)\b', s, re.I): return 'curious'
    return 'happy'
for slug in sys.argv[1:]:
    plan = {u['uid']: u for u in json.load(open(f'{ROOT}/videos/{slug}/plan.json'))}
    vert = 'short' in slug
    for fn in sorted(glob.glob(f'{ROOT}/videos/{slug}/art3/U*.json')):
        d = json.load(open(fn)); f = d.get('frog')
        if not isinstance(f, dict): continue
        text = plan[os.path.basename(fn)[:-5]]['text']
        sents = [x for x in re.findall(r'[^.!?]+[.!?]?', text) if x.strip()]
        if vert: f['y'] = min(f.get('y', 1250), 1250)
        f.pop('moods', None); f.pop('moves', None); f.pop('outfit', None)
        moods = []; prev = None
        for i, s in enumerate(sents):
            m = mood_of(s)
            if m == prev and i: m = 'happy' if m != 'happy' else 'curious'
            w = ' '.join(re.sub(r"[^\w']", '', t) for t in s.split()[:2]).strip()
            moods.append({'mood': m} if i == 0 else {'word': w, 'mood': m}); prev = m
        f['moods'] = moods
        if SEA.search(text): f['outfit'] = ['goggles']
        elif SPACE.search(text): f['outfit'] = ['helmet']
        if len(sents) >= 2 and len(text.split()) >= 14:
            w = ' '.join(re.sub(r"[^\w']", '', t) for t in sents[1].split()[:2]).strip()
            W = 1080 if vert else 1920
            f['moves'] = [{'word': w, 'x': W - f['x'], 'y': f['y'], 'flip': -f.get('flip', 1), 's': round(f.get('s', 2.4) * .85, 2)}]
        d['frog'] = f
        json.dump(d, open(fn, 'w'), ensure_ascii=False, indent=1)
        print(slug, os.path.basename(fn), [m['mood'] for m in moods], f.get('outfit'), 'hop' if 'moves' in f else '')
