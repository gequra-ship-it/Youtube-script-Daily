# usage: python3 tools/frog_place.py <slug>...   Run after the pictures exist and plan.json has `frog_hint` units, before build3.py.
# Rules (guideline 7-2, miya 2026-10-25): the explainer frog that stands beside a picture and points is for the CHALKBOARD only.
# In picture units (plan.json frog_hint: true, or any sidecar that already has "frog") the frog is a cute companion:
#   - it sits ON a moving object (a group `mv-core-(swell|heartbeat|wobble|sway|glide|approach|drop|ping|tremble)`, `mv-path`, `mv-slide`, `mv-swing`),
#     drawn INSIDE that group so it moves/turns with it (frog.py "ride"); or, with no fitting object,
#   - it sits small in a bottom corner of the background (corners alternate). No arm, no pointing.
# Moods follow the sentences of the unit text, a helmet goes on in space scenes, a diving suit with tank in deep/dark water scenes, goggles near the surface. The mouth does NOT follow the words in picture scenes (only the explainer on the chalkboard talks); a surprised/excited mood opens it. Re-running keeps `ride` of an existing sidecar.
# Writes the "frog" key of videos/<slug>/art3/<uid>.json (creates the sidecar when missing). Never touches the chalkboard frog.
import sys, os, glob, json, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from paths import *
from playwright.sync_api import sync_playwright
OK = re.compile(r'^mv-(core-(swell|heartbeat|wobble|sway|glide|approach|drop|ping|tremble)|path|slide|swing)')
SPACE = re.compile(r'\b(space|star|stars|galax\w*|cosmic|universe|horizon|probe|voyager|light|planet|orbit|dark|expan\w*)\b', re.I)
SEA = re.compile(r'\b(ocean|oceans|sea|seas|seafloor|underwater|dive|diving|water|whales?|reef|coral|fish|vents?|abyss\w*|deep|depths?|plankton|marine)\b', re.I)
DEEP = re.compile(r'\b(deep|depths?|abyss\w*|dark|darkness|seafloor|sinks?|sinking|descen\w*|vents?|bones?|carcass|silt|thousands of meters)\b', re.I)
ACTS = [   # (act, regex on the unit text, first mood)  -- first match wins (miya 2026-10-25: expression + motion that fits the situation, not only examples)
    ('pull',   re.compile(r'\b(black holes?|event horizon|horizon|plunge\w*|spiral\w*|sink\w*|drag\w*|abyss|gravity trap|falls? in|pulled|inward|swallow\w*|devour\w*|doom\w*|crush\w*|well)\b', re.I), 'scared'),
    ('wind',   re.compile(r'\b(speed\w*|rac(e|es|ing)|fast\w*|rocket|shuttle|lifts?|orbit\w*|fl(y|ies|ying)|hurtl\w*|streak\w*|whirl\w*|zip\w*|climb\w*|lander|route|dock\w*|launch\w*|race|travel\w*)\b', re.I), 'squint'),
    ('waves',  re.compile(r'\b(waves?|tides?|tidal|ocean|sea|water|splash\w*|wading|knee-deep|shallow|brine)\b', re.I), 'surprised'),
    ('shiver', re.compile(r'\b(alone|lonely|isolation|cold|terrif\w*|deadly|horror|fear|haunting|exhaustion|grief|mourn\w*|tragic\w*|brutal\w*)\b', re.I), 'scared'),
    ('awe',    re.compile(r'\b(giants?|enormous|supermassive|vast|towering|huge|colossal|billions?|millions?|leviathan|monster|universe|galax\w*)\b', re.I), 'surprised'),
    ('sleepy', re.compile(r'\b(years|decades|waiting|slow\w*|frozen|amber|steady|steadily|patient\w*|ticking|ticks?|clocks?)\b', re.I), 'sleepy'),
    ('cheer',  re.compile(r'\b(solved|breakthrough|discover\w*|works?|yes|answer|possible|allows?|proved?|proof)\b', re.I), 'excited'),
]
HOLE = re.compile(r'hole|bh|singular|well|horizon', re.I)
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
            act = None; first = None
            for nm, rx, md in ACTS:
                if rx.search(text): act, first = nm, md; break
            if act is None: act, first = ('float' if SPACE.search(text) else 'cheer'), ('happy' if SPACE.search(text) else 'excited')
            if first: moods[0] = {'mood': first}
            if len(moods) > 1 and moods[1]['mood'] == first: moods[1]['mood'] = 'curious'
            keep = {'moods': moods, 'act': act}
            if SEA.search(text): keep['outfit'] = ['diver'] if DEEP.search(text) else ['goggles']   # diving suit + tank in deep/dark water, mask + snorkel near the surface (miya 2026-10-25)
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
                n += 1   # corners vary (miya 2026-10-25): far left, far right, left-third, right-third, each with its own size
                xs = [150, W - 150, round(W * .3), round(W * .72)]; x0 = xs[(n - 1) % 4]; sz = [1.0, 1.15, .9, 1.05][(n - 1) % 4]
                keep.update(x=x0, y=(H - 150) if vert else (H - 40), s=round((1.7 if vert else 1.35) * sz, 2), flip=1 if x0 < W / 2 else -1, kind='bg')
            if act == 'pull':   # the hole the frog is dragged toward: a picture group named like a hole/well, else the picture centre
                hg = [g for g in gs.values() if HOLE.search(g[0])]
                keep['act'] = {'type': 'pull', 'to': [round(hg[0][1] + hg[0][3] / 2), round(hg[0][2] + hg[0][4] / 2)] if hg else [W // 2, H // 2]}
            d['frog'] = keep
            json.dump(d, open(fn, 'w'), ensure_ascii=False, indent=1)
            print(slug, uid, keep['kind'], pick, keep['x'], keep['y'], keep['s'])
    b.close()
