# usage: python3 tools/frog_place.py <slug>...   Run after the pictures exist and plan.json has `frog_hint` units, before build3.py.
# Rules (guideline 7-2, miya 2026-10-25): the explainer frog that stands beside a picture and points is for the CHALKBOARD only.
# In picture units (plan.json frog_hint: true, or any sidecar that already has "frog") the frog is a cute companion:
#   - it sits ON a moving object (a group `mv-core-(swell|heartbeat|wobble|sway|glide|approach|drop|ping|tremble)`, `mv-path`, `mv-slide`, `mv-swing`),
#     drawn INSIDE that group so it moves/turns with it (frog.py "ride"); or, with no fitting object,
#   - it sits small in a bottom corner of the background (corners alternate). No arm, no pointing.
# Moods follow the sentences of the unit text, a helmet goes on in space scenes, goggles in water scenes. Re-running keeps `ride` of an existing sidecar.
# Writes the "frog" key of videos/<slug>/art3/<uid>.json (creates the sidecar when missing). Never touches the chalkboard frog.
import sys, os, glob, json, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from paths import *
from playwright.sync_api import sync_playwright
OK = re.compile(r'^mv-(core-(swell|heartbeat|wobble|sway|glide|approach|drop|ping|tremble)|path|slide|swing)')
SPACE = re.compile(r'\b(space|star|stars|galax\w*|cosmic|universe|horizon|probe|voyager|light|planet|orbit|dark|expan\w*)\b', re.I)
SEA = re.compile(r'\b(ocean|sea|underwater|dive|water)\b', re.I)
JS = '''()=>{const o=[];for(const g of document.querySelectorAll('g[id^="mv-"]')){const b=g.getBBox();if(b.width<8)continue;o.push([g.id,b.x,b.y,b.width,b.height])}return o}'''
def mood_of(s):
    if s.rstrip().endswith('?'): return 'curious'
    if s.rstrip().endswith('!'): return 'excited'
    if re.search(r'\b(never|impossible|terrifying|trapped|lost|prison|dark|fade|alone|gone)\b', s, re.I): return 'worried'
    if re.search(r'\d|\b(billion|million|thousand|trillion|faster|fastest)\b', s, re.I): return 'surprised'
    if re.search(r'\b(but|however|yet|actually|here)\b', s, re.I): return 'curious'
    return 'happy'
n = 0
with sync_playwright() as p:
    b = p.chromium.launch(executable_path=chrome(), args=['--no-sandbox']); pg = b.new_page()
    for slug in sys.argv[1:]:
        vert = 'short' in slug; W, H = (1080, 1920) if vert else (1920, 1080)
        plan = {u['uid']: u for u in json.load(open(f'{REPO}/videos/{slug}/plan.json'))}
        for uid, u in sorted(plan.items()):
            fn = f'{REPO}/videos/{slug}/art3/{uid}.json'; svg = fn[:-5] + '.svg'
            d = json.load(open(fn)) if os.path.exists(fn) else {}
            if not (u.get('frog_hint') or d.get('frog')) or u.get('kind') == 'chalk' or not os.path.exists(svg): continue
            f = d.get('frog') if isinstance(d.get('frog'), dict) else {}
            text = u['text']; sents = [x for x in re.findall(r'[^.!?]+[.!?]?', text) if x.strip()]
            moods = []; prev = None
            for i, s in enumerate(sents):
                m = mood_of(s)
                if m == prev and i: m = 'happy' if m != 'happy' else 'curious'
                w = ' '.join(re.sub(r"[^\w']", '', t) for t in s.split()[:2]).strip()
                moods.append({'mood': m} if i == 0 else {'word': w, 'mood': m}); prev = m
            keep = {'moods': moods}
            if SEA.search(text): keep['outfit'] = ['goggles']
            elif SPACE.search(text): keep['outfit'] = ['helmet']
            pg.set_content('<body style="margin:0">' + open(svg).read() + '</body>')
            gs = {g[0]: g for g in pg.evaluate(JS)}
            pick = f.get('ride') if f.get('ride') in gs else None
            if not pick:
                cand = [g for g in gs.values() if OK.match(g[0]) and 60 <= g[3] <= W * .8 and g[4] >= 40]
                cand.sort(key=lambda g: -g[3] * g[4]); pick = cand[0][0] if cand else None
            if pick:
                _, x, y, w, h = gs[pick]; s = round(min(1.5, max(.9, w / 170)), 2); cx = x + w / 2
                keep.update(ride=pick, x=round(cx), y=round(y + 8 * s), s=s, flip=1 if cx < W / 2 else -1, kind='ride')
            else:
                n += 1; left = n % 2 == 1
                keep.update(x=150 if left else W - 150, y=(H - 150) if vert else (H - 40), s=1.7 if vert else 1.35, flip=1 if left else -1, kind='bg')
            d['frog'] = keep
            json.dump(d, open(fn, 'w'), ensure_ascii=False, indent=1)
            print(slug, uid, keep['kind'], pick, keep['x'], keep['y'], keep['s'])
    b.close()
