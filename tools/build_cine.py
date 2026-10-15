# Miya's Lab cine page builder (2026-10-14). Writes render/<slug>/index.html for the cine look from
#   videos/<slug>/cine.json            chapters (stage / cuts), shots (scene type + params), beats per unit (tools/cine_spec.md)
#   <work>/build/build_data.json       unit and caption times, chalk pop times (from: SLUG=x python3 tools/build_audio.py)
#   render/<slug>/mix.m4a              the mixed narration + music + SFX (same command)
# usage: SLUG=x [VERT=1] [SEL=1,2] [CINE_JSON=f] python3 tools/build_cine.py [out dir]   (SEL = the same selection as the CINE build)
# Chalkboard scenes become data cards over a slow star field. Shorts: VERT=1 (1080x1920).
import os, re, sys, json, glob, shutil, colorsys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from paths import *
import caption_hl, palettes

CFG = load_config(); SCENES = load_scenes()
VERT = os.environ.get('VERT') == '1'; W, H = (1080, 1920) if VERT else (1920, 1080)
SEL = [int(x) for x in os.environ.get('SEL', '').split(',') if x]
B = wdir() + '/build'; OUT = sys.argv[1] if len(sys.argv) > 1 else f'{REPO}/render/{SLUG}'
D = json.load(open(B + ('/build_data_partial.json' if SEL else '/build_data.json')))
CJ = json.load(open(os.environ.get('CINE_JSON') or vdir() + '/cine.json'))   # CINE_JSON=<file>: a test layout
CINE_DIR = REPO + '/tools/cine'
errors, warns = [], []

cuts = D['cuts']; byid = {c['id']: c for c in cuts}; order = [c['id'] for c in cuts]
TOTAL = D['total']

# ---------- captions with word times ----------
def norm(w): return re.sub(r"[^a-z0-9']", '', w.lower())
caps = []
for c in D['caps']:
    ws = c['text'].split(); wt = caption_hl.word_times(c['text'], c['t0'], c['sp1'])
    caps.append(dict(t0=round(c['t0'], 3), t1=round(c['t1'], 3), words=ws, wt=[round(x, 3) for x in wt]))
WORDS = [(norm(w), t) for c in caps for w, t in zip(c['words'], c['wt'])]

# ---------- cues: "U007" = unit start, "U009:standstill" (or a phrase) = when that word is spoken in that unit ----------
CUE_RX = re.compile(r'^U\d{3}(:.+)?$')
def cue_time(s):
    uid, _, word = s.partition(':')
    if uid not in byid: return None
    u = byid[uid]
    if not word: return round(u['t0'], 3)
    toks = [norm(x) for x in word.split() if norm(x)]
    for k in range(len(WORDS)):
        t = WORDS[k][1]
        if t < u['t0'] - .3 or t > u['t1'] + .3: continue
        if [w for w, _ in WORDS[k:k + len(toks)]] == toks: return t
    return None
cues = {}
def scan(o):
    if isinstance(o, dict): [scan(v) for v in o.values()]
    elif isinstance(o, list): [scan(v) for v in o]
    elif isinstance(o, str) and CUE_RX.match(o):
        t = cue_time(o)
        if t is None: (warns if SEL else errors).append(f'cue "{o}" not found (unit missing or word not spoken in that unit)')
        else: cues[o] = t
scan(CJ.get('chapters', []))

# ---------- chapters and shots ----------
def t_of(uid, end=False):
    c = byid.get(uid); return None if c is None else (c['t1'] if end else c['t0'])
chapters = []
for ch in CJ['chapters']:
    a = t_of(ch['from'])
    if a is None: (warns if SEL else errors).append(f'chapter {ch.get("id")}: unit {ch["from"]} not in this build'); continue
    i_from = order.index(ch['from'])
    to = ch.get('to'); b = t_of(to, True) if to else None
    if b is None:   # until the unit before the next chapter / chalk
        j = i_from
        while j + 1 < len(order) and cuts[j + 1]['kind'] != 'chalk' and not any(c2['from'] == order[j + 1] for c2 in CJ['chapters']): j += 1
        b = cuts[j]['t1']
    out = dict(id=ch.get('id'), label=ch.get('label', ''), title=ch.get('title', CFG.TITLE), mode=ch.get('mode', 'stage'), t0=round(a, 3), t1=round(b, 3), shots=[])
    if ch.get('plot'): out['plot'] = ch['plot']
    if ch.get('badge_label'): out['badge_label'] = ch['badge_label']
    if out['mode'] == 'stage':
        sc = ch['scene']; out['shots'].append(dict(t0=out['t0'], t1=out['t1'], type=sc['type'], params=sc.get('params', {}), tr=ch.get('tr', 'dip'), trd=ch.get('trd'), tro=ch.get('tro')))
    else:
        shots = ch['shots']
        for k, s in enumerate(shots):
            s0 = t_of(s['from'])
            if s0 is None: warns.append(f'shot from {s["from"]} not in this build'); continue
            s1 = t_of(shots[k + 1]['from']) if k + 1 < len(shots) and t_of(shots[k + 1]['from']) is not None else out['t1']
            out['shots'].append(dict(t0=round(s0, 3), t1=round(s1, 3), type=s['type'], params=s.get('params', {}), tr=s.get('tr', 'dip' if k == 0 else 'xfade') if k else ch.get('tr', s.get('tr', 'dip')), trd=s.get('trd'), tro=s.get('tro')))
    chapters.append(out)
# chalkboard units -> data card chapters (slow star field behind)
datacards = []
for c in cuts:
    if c['kind'] != 'chalk': continue
    ck = CFG.CHALK.get(c['scene']) if hasattr(CFG, 'CHALK') else None
    if not ck: errors.append(f'chalk scene {c["scene"]} has no CHALK entry'); continue
    pop = (D.get('chalk_pop') or {}).get(str(c['scene'])) or []
    datacards.append(dict(t0=round(c['t0'], 3), t1=round(c['t1'], 3), title=ck['title'], sub=ck.get('sub', ''), rows=[[r[0], r[1], r[2], r[3] if len(r) > 3 else ''] for r in ck['rows']],
                          concl=ck['concl'][0] if isinstance(ck.get('concl'), (list, tuple)) else ck.get('concl', ''), source=ck.get('src', ''), pop=pop))
    chapters.append(dict(id=f'card{c["scene"]}', label='', title=ck['title'], mode='card', t0=round(c['t0'], 3), t1=round(c['t1'], 3),
                         shots=[dict(t0=round(c['t0'], 3), t1=round(c['t1'], 3), type='void', params={}, tr='dip')]))
chapters.sort(key=lambda c: c['t0'])
if chapters: chapters[0]['shots'][0]['tr'] = 'cut'
# coverage check
t = 0.0
for ch in chapters:
    if ch['t0'] > t + 1.2: errors.append(f'gap with no chapter from {t:.2f} to {ch["t0"]:.2f} s')
    t = max(t, ch['t1'])
if TOTAL - t > 3.5: errors.append(f'no chapter after {t:.2f} s (video ends {TOTAL:.2f})')
if chapters: chapters[-1]['t1'] = round(TOTAL, 3); chapters[-1]['shots'][-1]['t1'] = round(TOTAL, 3)

# ---------- beats ----------
beats = CJ.get('beats', {}); units = []
for c in cuts:
    if c['kind'] == 'chalk': continue
    b = beats.get(c['id'], {}); u = dict(uid=c['id'], t0=round(c['t0'], 3), t1=round(c['t1'], 3))
    for k in ('kw', 'sub', 'log', 'badge', 'plot', 'card', 'acc'):
        if k in b: u[k] = b[k]
    if b.get('kw') and len(b['kw']) > 16: warns.append(f'{c["id"]}: keyword "{b["kw"]}" is long (>16 chars)')
    if b.get('card') and (c['t1'] - c['t0']) < 2.5: warns.append(f'{c["id"]}: text card on a unit shorter than 2.5 s')
    units.append(u)
for k in beats:
    if k not in byid and not SEL: warns.append(f'beat for unknown unit {k}')

# ---------- scene types available ----------
lib = {}
for f in sorted(glob.glob(CINE_DIR + '/scenes/*.js')) + sorted(glob.glob(vdir() + '/scenes/*.js')):
    for m in re.finditer(r'scenes\.([A-Za-z_][\w]*)\s*=', open(f).read()): lib[m.group(1)] = f
for ch in chapters:
    for s in ch['shots']:
        if s['type'] not in lib: errors.append(f'scene type "{s["type"]}" not found (tools/cine/scenes or videos/{SLUG}/scenes)')

# ---------- palette tones for the tone-bar transition ----------
pal = palettes.PALETTES[palettes.for_theme(CFG, SCENES[0][3])]
def hx(c): c = c.lstrip('#'); return [int(c[i:i + 2], 16) / 255 for i in (0, 2, 4)]
base = hx(pal['night'][1]); hb = colorsys.rgb_to_hls(*base)[0]
acc = min(pal['accents'], key=lambda c: min(abs(colorsys.rgb_to_hls(*hx(c))[0] - hb), 1 - abs(colorsys.rgb_to_hls(*hx(c))[0] - hb)))
tones = []
for i in range(6):
    tt = .15 + .35 * i / 5; r, g, b2 = [base[j] + (hx(acc)[j] - base[j]) * tt for j in range(3)]
    hh, ll, ss = colorsys.rgb_to_hls(r, g, b2); r, g, b2 = colorsys.hls_to_rgb(hh, ll, ss * .66); tones.append('#%02x%02x%02x' % tuple(int(v * 255) for v in (r, g, b2)))

if warns: print('WARN\n  ' + '\n  '.join(warns))
if errors: raise SystemExit('cine.json problems:\n  ' + '\n  '.join(errors))

# ---------- write the page ----------
os.makedirs(OUT, exist_ok=True)
for f in glob.glob(CINE_DIR + '/assets/*'): shutil.copy(f, OUT)
for f in ('cine.js', 'cine.css'): shutil.copy(f'{CINE_DIR}/{f}', OUT)
shutil.copy(f'{ASSETS}/logo.png', OUT)
shutil.copy(f'{CINE_DIR}/kit.js', OUT)
os.makedirs(f'{OUT}/scenes', exist_ok=True)
used = {lib[s['type']] for ch in chapters for s in ch['shots']}
for f in list(used):   # a scene file can build on other scene types: a line "// requires: pond, void" pulls their files in first
    for m in re.findall(r'^//\s*requires:\s*(.+)$', open(f).read(), re.M):
        for ty in [x.strip() for x in m.split(',') if x.strip()]:
            if ty not in lib: raise SystemExit(f'{os.path.basename(f)} requires unknown scene type {ty}')
            else: used.add(lib[ty])
used = sorted(used)
scene_tags = []
for f in used:
    name = ('v_' if f.startswith(vdir()) else '') + os.path.basename(f); shutil.copy(f, f'{OUT}/scenes/{name}'); scene_tags.append(f'<script src="scenes/{name}"></script>')
cfg = dict(w=W, h=H, total=round(TOTAL, 3), lead=D.get('lead', 0), title=CJ.get('title', CFG.TITLE), accent=CJ.get('accent', pal['accents'][0] if pal['accents'][0].lower() != '#6b4bd6' else '#ffc65a'),
           exposure=CJ.get('exposure', 1.0), tones=tones, chapters=chapters, units=units, caps=caps, cues=cues, datacards=datacards)
assert os.path.exists(f'{OUT}/mix.m4a'), 'render/<slug>/mix.m4a missing: run SLUG=x python3 tools/build_audio.py first'
html = f'''<!doctype html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width={W}, height={H}">
<link rel="stylesheet" href="cine.css"><script src="gsap.min.js"></script><script src="three.js"></script><script src="room-env.js"></script><script src="kit.js"></script>
{''.join(scene_tags)}
</head><body>
<div id="root" data-composition-id="main" data-start="0" data-duration="{TOTAL:.3f}" data-width="{W}" data-height="{H}">
<canvas id="gl" width="{W}" height="{H}"></canvas><div id="vig"></div><div id="dim"></div>
<div class="hud" id="hudL"></div><div class="hud" id="hudR">Your clock<b id="clk">00:00:00.000</b></div>
<div id="bar"><s id="prog"></s><div id="dot"></div></div>
<img id="logo" src="logo.png"><div id="err">WEBGL UNAVAILABLE</div><div id="fade"></div>
<audio src="mix.m4a" data-start="0" data-duration="{TOTAL:.3f}" data-track-index="0" data-volume="1"></audio>
</div>
<script>window.CINE={json.dumps(cfg, ensure_ascii=False)};</script>
<script src="cine.js"></script>
</body></html>'''
open(f'{OUT}/index.html', 'w', encoding='utf-8').write(html)
n_sh = sum(len(c['shots']) for c in chapters)
print(f'cine page: {OUT}/index.html  {TOTAL:.1f}s  chapters {len(chapters)}  shots {n_sh}  units {len(units)}  caps {len(caps)}  cues {len(cues)}  data cards {len(datacards)}')
print('scenes:', ', '.join(sorted({s["type"] for c in chapters for s in c["shots"]})))
