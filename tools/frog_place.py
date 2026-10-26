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
    ('pull',   re.compile(r'\b(black holes?|event horizon|horizon|plunge\w*|spiral\w*|drag\w*|gravity trap|falls? in|pulled|inward|swallow\w*|devour\w*|doom\w*|well)\b', re.I), 'scared'),
    ('wind',   re.compile(r'\b(speed\w*|rac(e|es|ing)|fast\w*|rocket|shuttle|lifts?|orbit\w*|fl(y|ies|ying)|hurtl\w*|streak\w*|whirl\w*|zip\w*|climb\w*|lander|route|dock\w*|launch\w*|race|travel\w*)\b', re.I), 'squint'),
    ('waves',  re.compile(r'\b(waves?|tides?|tidal|ocean|sea|water|splash\w*|wading|knee-deep|shallow|brine)\b', re.I), 'surprised'),
    ('shiver', re.compile(r'\b(crush\w*|freezing|alone|lonely|isolation|cold|terrif\w*|deadly|horror|fear|haunting|exhaustion|grief|mourn\w*|tragic\w*|brutal\w*)\b', re.I), 'scared'),
    ('awe',    re.compile(r'\b(giants?|enormous|supermassive|vast|towering|huge|colossal|billions?|millions?|leviathan|monster|universe|galax\w*)\b', re.I), 'surprised'),
    ('sleepy', re.compile(r'\b(years|decades|waiting|slow\w*|frozen|amber|steady|steadily|patient\w*|ticking|ticks?|clocks?)\b', re.I), 'sleepy'),
    ('cheer',  re.compile(r'\b(solved|breakthrough|discover\w*|works?|yes|answer|possible|allows?|proved?|proof)\b', re.I), 'excited'),
]
GROUND = re.compile(r'\b(planet|moon|mars|surface|ground|land|desert|shore|beach|island|terrain|crater|road|path|walk\w*|run\w*|city|field|hill|mountain)\b', re.I)
def free_band(pg, W, H, vert, n):
    """vertical centre of the emptiest horizontal band of the picture (lowest edge density), outside the caption zone"""
    import io, numpy as np
    from PIL import Image
    pg.set_viewport_size({'width': W, 'height': H})
    im = np.asarray(Image.open(io.BytesIO(pg.screenshot())).convert('L').resize((W // 8, H // 8)), dtype=np.float32)
    gy, gx = np.gradient(im); e = np.hypot(gx, gy)
    lo, hi = (420, 1380) if vert else (170, 800); best = None
    for yc in range(lo, hi + 1, 40):
        band = e[max(0, (yc - 80) // 8):(yc + 80) // 8, 10:-10].mean() + .002 * abs(yc - (lo + hi) / 2) * (n % 2)   # mild variety between units
        if best is None or band < best[0]: best = (band, yc)
    return best[1]
SAYS = {'pull': 'AAAAAH!', 'wind': 'Whooosh!', 'waves': 'Whoa-oa!', 'shiver': 'Brrrr...', 'awe': 'Woooow!', 'sleepy': 'Zzz...', 'cheer': 'Yay!', 'float': 'Wheee!'}
STRONG = ('pull', 'shiver', 'awe', 'wind')   # always get a sound word; the other acts every second unit (miya 2026-10-26: speech bubble with emotion / sound words)
def says_for(act, keep, text, cnt):
    nm = act.get('type') if isinstance(act, dict) else act
    rm = (keep.get('roam') or {}).get('kind')
    word = SAYS.get(nm)
    if rm == 'roll': word = 'Waaaah!'
    elif rm in ('swim', 'lie', 'tumble'): word = 'Blub blub!' if keep.get('outfit') in (['diver'], ['goggles']) else 'Wheee!'
    elif rm == 'run': word = 'Hop hop!'
    elif rm == 'moonhop': word = 'Boing!'
    elif rm == 'walk' and word is None: word = 'Hmm?' if keep['moods'][0]['mood'] == 'curious' else 'Tada!'
    if word is None: return []
    if nm not in STRONG and cnt % 2: return []
    return [{'text': word, 'shout': word.endswith('!') and nm in STRONG}]
PLAT = re.compile(r'belt|treadmill|tread\b|slats|ground|ledge|platform|bridge|shelf|deck|road|planet|moon|surface|floor|stage|track', re.I)
ACTIVE = re.compile(r'\b(run\w*|walk\w*|jump\w*|hop\w*|step\w*|treadmill|pump\w*|race|racing|sprint\w*)\b', re.I)
VEH = re.compile(r'\b(rocket|spaceship|spacecraft|ship|probe|warp drive|shuttle|lander)\b', re.I)
ROLL = re.compile(r'\b(drag\w*|spiral\w*|tumbl\w*|roll\w*|carried|swept|backward|whirl\w*|swirl\w*|knock\w*)\b', re.I)
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
            if (d.get('frog') or {}).get('lock'): continue   # hand-made sidecar (miya 2026-10-26, e.g. the caged frog in edge-of-universe U010): never overwritten
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
            pg.set_content('<style>body{margin:0}svg{display:block;width:100vw;height:100vh}</style><body>' + open(svg).read() + '</body>')
            gs = {g[0]: g for g in pg.evaluate(JS)}
            pick = f.get('ride') if f.get('ride') in gs else None
            if ROLL.search(text) and not ACTIVE.search(text): pick = None   # dragged / swept / spiralling: the frog rolls along instead of riding (miya 2026-10-26)
            elif not pick:
                cand = [g for g in gs.values() if OK.match(g[0]) and 60 <= g[3] <= W * .8 and g[4] >= 40]
                cand.sort(key=lambda g: -g[3] * g[4]); pick = cand[0][0] if cand else None
            if VEH.search(text) and not ROLL.search(text):   # a vehicle in the text: the frog clings beside the fin of the centre object (miya 2026-10-26)
                core = [g for g in gs.values() if g[0].startswith('mv-core-') and OK.match(g[0])]
                if core: pick = core[0][0]; keep['cling'] = True
            if pick:
                _, x, y, w, h = gs[pick]; s = round(min(1.5, max(.9, w / 170)), 2); cx = x + w / 2
                keep.update(ride=pick, x=round(cx), y=round(max(y + 8 * s, 82 * s + 40)), s=s, flip=1 if cx < W / 2 else -1, kind='ride')
                if keep.pop('cling', False): keep.update(x=round(x + w * .95), y=round(y + h - 12), s=round(min(1.2, max(.9, h / 200)), 2), flip=-1, act='wind')
            else:
                n += 1   # roaming (miya 2026-10-26: the frog stayed in one bottom spot): small, travelling through the free part of the background
                plat = [g for g in gs.values() if PLAT.search(g[0]) and g[3] >= 220 and g[4] <= H * .25 and g[2] > H * .25]
                plat.sort(key=lambda g: -g[3]); plat = plat[0] if plat else None
                on_plat = None
                if plat and ACTIVE.search(text): kind = 'moonhop' if (SPACE.search(text) or 'tread' in text.lower() or 'tread' in plat[0]) else 'run'; on_plat = plat   # situation: the frog does it ON the platform of the picture (treadmill belt, ground, bridge...)
                elif ROLL.search(text): kind = 'roll'   # dragged / swept / spiralling: it rolls along
                elif SEA.search(text) or (SPACE.search(text) and not GROUND.search(text)):   # diver / space-suit drifting: upright float, lying on its back, somersault (space only)
                    kind = ('swim', 'lie', 'tumble' if not SEA.search(text) else 'swim')[(n - 1) % 3]
                elif GROUND.search(text): kind = ('run', 'moonhop' if SPACE.search(text) else 'run')[(n - 1) % 2]
                else: kind = 'walk'
                sz = [1.0, .9, 1.1, .95][(n - 1) % 4]
                if kind in ('swim', 'lie', 'tumble'): y0 = free_band(pg, W, H, vert, n); s0 = (1.1 if vert else .85) * sz
                elif kind == 'roll': y0 = free_band(pg, W, H, vert, n); s0 = (1.1 if vert else .85) * sz
                else: y0 = (H - 110) if vert else (H - 50); s0 = (1.05 if vert else .8) * sz
                if on_plat: y0 = round(on_plat[2] + 6)
                right = (n % 2 == 1); dist = round(W * ((.28 if vert else .24) if kind in ('swim', 'lie', 'tumble', 'roll') else (.5 if vert else .15)))
                x0 = (130 if right else W - 130); fl = 1 if right else -1
                if on_plat:   # stays on the platform, on the side away from the figure that runs on it
                    figs = [g for g in gs.values() if re.search(r'run|astro|breathe|legs|walker|person|man\b|woman|kid|child', g[0], re.I) and g[0] != on_plat[0]]
                    pcx = on_plat[1] + on_plat[3] / 2; fcx = (sum(g[1] + g[3] / 2 for g in figs) / len(figs)) if figs else pcx
                    right = fcx > pcx   # figure on the right -> frog starts on the left part and walks toward the facing side (right)
                    x0 = round(on_plat[1] + on_plat[3] * (.15 if right else .85)); fl = 1 if right else -1; dist = round(min(dist, on_plat[3] * .3))
                else: x0 = max(170, min(W - 170, x0))
                keep.update(x=x0, y=y0, s=round(s0, 2), flip=fl, kind='bg', roam=dict(kind=kind, dist=dist))
                if act in ('float', 'cheer') or kind in ('swim', 'lie', 'tumble', 'roll'): keep['act'] = None   # the roaming motion replaces the in-place bob/hops; a drifting swimmer gets no lean/wind lines (miya 2026-10-26)
            if act == 'pull':   # the hole the frog is dragged toward: a picture group named like a hole/well, else the picture centre
                hg = [g for g in gs.values() if HOLE.search(g[0])]
                keep['act'] = {'type': 'pull', 'to': [round(hg[0][1] + hg[0][3] / 2), round(hg[0][2] + hg[0][4] / 2)] if hg else [W // 2, H // 2]}
                if hg and keep.get('kind') == 'ride': keep['act']['vanish'] = True   # riding a star into the hole: pulled in, shrinking, gone (miya 2026-10-26)
            cnt_say = globals().setdefault('cnt_say', 0); globals()['cnt_say'] = cnt_say + 1
            keep['says'] = says_for(keep['act'], keep, text, cnt_say); keep['bside'] = 1 if keep['x'] < W / 2 else -1
            d['frog'] = keep
            json.dump(d, open(fn, 'w'), ensure_ascii=False, indent=1)
            print(slug, uid, keep['kind'], pick, keep['x'], keep['y'], keep['s'])
    b.close()
