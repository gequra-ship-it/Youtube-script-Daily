# -*- coding: utf-8 -*-
# Miya's Lab audio + timing builder (2026-10-14; the audio/timing half of the retired SVG builder build3.py).
# From videos/<slug>/script.py and the Kokoro clips (tools/tts.sh -> tools/audio_prep.py) it splits the narration into
# meaning units, times the captions, places the SFX cues and synthesises the music, then writes
#   videos/<slug>/plan.json                       (PLAN=1: the unit split only, then exit)
#   render/<slug>/mix.m4a                          narration + SFX + chalk + music, one pre-mixed file
#   <work>/build/build_data.json                   unit/caption/cue times for tools/build_cine.py (build_data_partial.json with SEL)
# usage: SLUG=x [PLAN=1] [SEL=1,2] [VERT=1] [NOBGM=1] [BGM_BELOW=13] python3 tools/build_audio.py [OUTDIR]
#        transitions (for their sounds) come from videos/<slug>/cine.json (CINE_JSON=<file> for a test layout)
import os, re, sys, json, subprocess, math, wave
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from paths import *
import numpy as np
SCENES = load_scenes()
CFG = load_config()
B = wdir() + '/build'
VERT = os.environ.get('VERT') == '1'
OUT = sys.argv[1] if len(sys.argv) > 1 else f'{REPO}/render/{SLUG}'
SEL = [int(x) for x in os.environ.get('SEL', '').split(',') if x] or list(range(1, len(SCENES) + 1))
LEAD, GAP, TAIL = (0.3, 0.3, 1.2) if VERT else (1.0, 0.4, 2.5)   # 2026-10-16: GAP 0.8->0.4 (shorts 0.5->0.3), pace
MAXU = 6.2            # max seconds of narration per unit
D = json.load(open(B + '/timing_base.json'))['D']
CHALK = getattr(CFG, 'CHALK', {})


def run(*a):
    return subprocess.run(a, capture_output=True, text=True)


def dur(f):
    return float(run('ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', f).stdout)


# ---------- scene start times ----------
starts = {}; t = LEAD
for i in SEL:
    starts[i] = t; t += D[i - 1] + GAP
TOTAL = round(starts[SEL[-1]] + D[SEL[-1] - 1] + TAIL, 3)


# ---------- sentence timing model (narration time of every character) ----------
def sentences(text):
    out = []
    for piece in re.split(r'(?<=[.?!])\s+', text.strip()):
        if out and (re.search(r'(?:^|\s)(?:[A-Z][a-z]*|[A-Z]\.)\s[A-Z]\.$', out[-1])
                    or (re.search(r'(?:^|\s)[A-Z]\.$', out[-1]) and re.match(r'[A-Z]\.(?:\s|$)', piece))):   # middle initials ("George W. Bush") are not sentence ends
            out[-1] += ' ' + piece
        else:
            out.append(piece)
    return out


def pauses(i):
    r = run('ffmpeg', '-nostats', '-i', f'{B}/s{i:02d}.wav', '-af', 'silencedetect=noise=-35dB:d=0.12', '-f', 'null', '-')
    s = [float(x) for x in re.findall(r'silence_start: ([\d.]+)', r.stderr)]
    e = [float(x) for x in re.findall(r'silence_end: ([\d.]+)', r.stderr)]
    d = D[i - 1]
    return [((a + b) / 2, b - a) for a, b in zip(s, e) if a > 0.2 and b < d - 0.2]


model = {}; snap_report = {}
for i in SEL:   # sentence bounds snap to the real pauses when they line up with the character-count estimate, else proportional
    text = SCENES[i - 1][4]; ss = sentences(text); d = D[i - 1]
    ch = [len(x) + 1 for x in ss]; tot = sum(ch); prop = [0.0]; c = 0
    for x in ch[:-1]:
        c += x; prop.append(d * c / tot)
    prop.append(d); k = len(ss) - 1; ps = pauses(i)
    cand = sorted(sorted(ps, key=lambda p: -p[1])[:k]) if k > 0 else []
    ok = len(cand) == k and all(abs(cand[j][0] - prop[j + 1]) <= 1.2 for j in range(k)) and all(cand[j][0] < cand[j + 1][0] for j in range(k - 1))
    bounds = ([0.0] + [p[0] for p in cand] + [d]) if ok else prop
    snap_report[i] = 'snap' if ok else 'prop'
    model[i] = [(ss[k], bounds[k], bounds[k + 1]) for k in range(len(ss))]


def tchar(i, idx):
    """scene-relative narration time of character index idx"""
    text = SCENES[i - 1][4]; pos = 0
    for n, (s, a, b) in enumerate(model[i]):
        j = text.find(s, pos)
        if j <= idx < j + len(s) + 1 or n == len(model[i]) - 1:
            return a + (b - a) * min(max((idx - j) / max(len(s), 1), 0), 1)
        pos = j + len(s)
    return D[i - 1]


# ---------- unit split: sentence/clause atoms merged to <= MAXU seconds ----------
def split_atom(i, c0, c1):
    text = SCENES[i - 1][4]
    if tchar(i, c1) - tchar(i, c0) <= MAXU:
        return [(c0, c1)]
    seg = text[c0:c1]
    pts = [c0 + m.end() for m in re.finditer(r'[,;:](?=\s)|\s—\s', seg) if 0 < m.end() < len(seg) - 6]
    if not pts:
        pts = [c0 + m.end() for m in re.finditer(r'\s', seg) if 8 < m.end() < len(seg) - 8]
    half = (tchar(i, c0) + tchar(i, c1)) / 2
    p = min(pts, key=lambda q: abs(tchar(i, q) - half))
    return split_atom(i, c0, p) + split_atom(i, p, c1)


def units_of(i):
    text = SCENES[i - 1][4]; atoms = []; pos = 0
    for (s, a, b) in model[i]:
        j = text.find(s, pos); atoms += split_atom(i, j, j + len(s)); pos = j + len(s)
    atoms = [(a + (len(text[a:]) - len(text[a:].lstrip())), b) for a, b in atoms]   # start at the first real character
    us = []; cur = [atoms[0][0], atoms[0][1]]
    for (a, b) in atoms[1:]:
        if tchar(i, b) - tchar(i, cur[0]) <= MAXU:
            cur[1] = b
        else:
            us.append(tuple(cur)); cur = [a, b]
    us.append(tuple(cur))
    span = lambda a, b: tchar(i, b) - tchar(i, a)
    if len(us) > 1 and span(*us[-1]) < 2.0:   # a short last unit takes trailing atoms of the previous one, or merges with it
        inner = [a for (a, b) in atoms if us[-2][0] < a < us[-2][1]]; fixed = False
        for cut in reversed(inner):
            if span(cut, us[-1][1]) > MAXU: break
            if span(cut, us[-1][1]) >= 2.0 and span(us[-2][0], cut) >= 2.0:
                us = us[:-2] + [(us[-2][0], cut), (cut, us[-1][1])]; fixed = True; break
        if not fixed and span(us[-2][0], us[-1][1]) <= MAXU + 0.8:
            us = us[:-2] + [(us[-2][0], us[-1][1])]
    k = 0
    while len(us) > 1 and k < len(us):   # a unit under 1.6 s ("Start with the hunter.") merges into its neighbour
        a, b = us[k]
        if span(a, b) < 1.6:
            j = k + 1 if k + 1 < len(us) else k - 1
            lo, hi = min(us[k][0], us[j][0]), max(us[k][1], us[j][1])
            us = [u for m, u in enumerate(us) if m not in (k, j)]; us.insert(min(k, j), (lo, hi)); k = 0; continue
        k += 1
    return us


units = []; n = 0
for i in SEL:
    kind = SCENES[i - 1][2]; text = SCENES[i - 1][4]
    s1_scene = TOTAL if i == SEL[-1] else starts[SEL[SEL.index(i) + 1]]
    if kind == 'chalk' or i in CHALK:   # a data-card scene is one unit
        n += 1
        units.append(dict(n=n, uid=f'U{n:03d}', scene=i, kind='chalk', c0=0, c1=len(text), text=text, t0=0.0 if i == SEL[0] else starts[i], t1=s1_scene))
        continue
    us = units_of(i)
    for k, (a, b) in enumerate(us):
        n += 1
        t0 = (0.0 if i == SEL[0] else starts[i]) if k == 0 else starts[i] + tchar(i, a)
        t1 = s1_scene if k == len(us) - 1 else starts[i] + tchar(i, us[k + 1][0])
        units.append(dict(n=n, uid=f'U{n:03d}', scene=i, kind='ill', c0=a, c1=b, text=text[a:b].strip(), t0=t0, t1=t1))
_plan = f'{vdir()}/plan.json'
if os.environ.get('SEL') and os.environ.get('PLAN') != '1' and os.path.exists(_plan):   # partial build: keep the full plan's unit ids
    _map = {(p['scene'], p['text']): p['uid'] for p in json.load(open(_plan))}
    for u in units:
        if u['kind'] == 'ill':
            u['uid'] = _map.get((u['scene'], u['text']), u['uid'])
for u in units:
    assert u['t1'] - u['t0'] > 1.5, ('unit too short', u)

if os.environ.get('PLAN') == '1':
    if not getattr(CFG, 'PAL_DEFAULT', None): print('WARNING: config.py has no PAL_DEFAULT (choose one from tools/palettes.py for this topic)')
    plan = []
    for k, u in enumerate(units):
        if u['kind'] == 'chalk': continue
        sc = SCENES[u['scene'] - 1]
        plan.append(dict(uid=u['uid'], scene=u['scene'], title=sc[1], text=u['text'], dur=round(u['t1'] - u['t0'], 2),
                         prev=units[k - 1]['text'] if k and units[k - 1]['scene'] == u['scene'] else '',
                         nxt=units[k + 1]['text'] if k + 1 < len(units) and units[k + 1]['scene'] == u['scene'] else ''))
    os.makedirs(vdir(), exist_ok=True)
    json.dump(plan, open(_plan, 'w'), ensure_ascii=False, indent=1)
    d = [p['dur'] for p in plan]
    print('units', len(plan), 'avg', round(sum(d) / len(d), 2), 'max', max(d), 'min', min(d), 'total', TOTAL)
    sys.exit(0)

# ---------- transitions from cine.json: a chapter's or shot's first unit carries its transition (for its sound) ----------
CJ = json.load(open(os.environ.get('CINE_JSON') or f'{vdir()}/cine.json'))
first = {}
for ch in CJ['chapters']:
    shots = ch.get('shots') or [dict(frm=ch['from'], tr=ch.get('tr', 'dip'))]
    for k, s in enumerate(shots):
        first[s.get('frm', s.get('from'))] = s.get('tr', ch.get('tr', 'dip')) if k else ch.get('tr', s.get('tr', 'dip'))
for k, u in enumerate(units):
    u['tr'] = 'cut' if k == 0 else ('dip' if u['kind'] == 'chalk' or units[k - 1]['kind'] == 'chalk' else first.get(u['uid'], 'none'))

# ---------- caption lines ----------
LMAX, WMAX, CHARMAX = (22, 4, 30) if VERT else (30, 7, 46)


def split_lines(sent):
    words = sent.split(); lines = []; cur = []
    def clen(ws): return len(' '.join(ws))
    for w in words:
        if cur and clen(cur + [w]) > LMAX + 6:   # a long word would overflow the line: break before it
            lines.append(cur); cur = []
        cur.append(w)
        if clen(cur) >= LMAX or len(cur) >= WMAX:
            lines.append(cur); cur = []
        elif len(cur) >= (3 if VERT else 4) and re.search(r'[,;:]$', w):
            lines.append(cur); cur = []
    if cur:
        if lines and (len(cur) < 3 or clen(cur) < 12) and clen(lines[-1]) + 1 + clen(cur) <= CHARMAX and len(lines[-1]) + len(cur) <= WMAX + 2:
            lines[-1] += cur
        else:
            lines.append(cur)
    return [' '.join(l) for l in lines]


caps = []
for i in SEL:
    s0 = starts[i]; sc = []
    for (s, a, b) in model[i]:
        ls = split_lines(s); ch = [len(x) + 1 for x in ls]; tot = sum(ch); c = 0
        for k, ltxt in enumerate(ls):
            sc.append([ltxt, s0 + a + (b - a) * c / tot, s0 + a + (b - a) * (c + ch[k]) / tot]); c += ch[k]
    for k, cp in enumerate(sc):
        end = sc[k + 1][1] if k + 1 < len(sc) else s0 + D[i - 1] + 0.25
        caps.append({'text': cp[0], 't0': cp[1], 't1': end, 'sp1': min(cp[2], end), 'scene': i})
prev = -1
for c in caps:
    assert c['t0'] < c['t1'] - 0.3, ('short/reversed caption', c)
    assert c['t0'] >= prev, ('non-monotonic', c); prev = c['t0']
assert max(len(c['text']) for c in caps) <= CHARMAX, max(caps, key=lambda c: len(c['text']))

# ---------- sound cues: one per transition (cosmic videos use the cosmic set, guideline 3-7) ----------
import sfx_lib
SFX = B + '/sfx'; os.makedirs(SFX, exist_ok=True)
sfx_lib.make_all(SFX); sfx_lib.make_chalk(f'{SFX}/chalk.wav')
TRSND = {'zoom': ('swish', -0.85, 0.9), 'wipe': ('swish', -0.7, 0.6), 'iris': ('hush', -0.9, 0.7), 'eye': ('hush', -0.7, 0.6),
         'blinds': ('rustle', -0.6, 0.6), 'push': ('swish', -0.6, 0.6), 'whip': ('swish', -0.4, 0.8), 'dip': ('hush', -0.5, 0.55),
         'flash': ('hush', -0.4, 0.7)}
if getattr(CFG, 'STYLE', 'default') == 'cosmic':
    TRSND = {'zoom': ('warp', -0.45, 0.8), 'wipe': ('warp', -0.6, 0.5), 'iris': ('glimmer', -0.8, 0.6), 'eye': ('glimmer', -0.6, 0.6),
             'blinds': ('sparkle', -0.5, 0.5), 'push': ('warp', -0.5, 0.5), 'whip': ('warp', -0.35, 0.7), 'dip': ('glimmer', -0.45, 0.55),
             'flash': ('bloom', -0.35, 0.7)}
cues = [dict(name=TRSND[u['tr']][0], t=max(u['t0'] + TRSND[u['tr']][1], 0.05), vol=TRSND[u['tr']][2], unit=u['uid']) for u in units if u['tr'] in TRSND]
kept = []
for c in cues:   # cues closer than 0.9 s: keep the first
    if all(abs(c['t'] - k['t']) >= 0.9 for k in kept): kept.append(c)
cues = kept; vcount = {}
for c in cues:   # cycle the 3 variants of each sound
    nm = sfx_lib.ALIAS.get(c['name'], c['name']); k = vcount.get(nm, 0); vcount[nm] = k + 1; v = k % sfx_lib.VARIANTS + 1
    c['file'] = f'sfx_{nm}{"" if v == 1 else "_" + str(v)}.wav'

# ---------- audio pieces: narration, chalk at each data-card row, SFX, music ----------
audio = [(f'{B}/n{i:02d}.wav', starts[i], D[i - 1] + GAP, 1) for i in SEL]
chalk_t = []
for i in SEL:
    if i in CHALK:   # first row at the scene start, rows 2-3 and the conclusion when their words are spoken
        s0 = starts[i]; c = CHALK[i]; ts = [s0 + 0.05]; text = SCENES[i - 1][4]
        for r in (1, 2):
            idx = text.find(c['rows'][r][4]); assert idx >= 0, ('data card row words not in the narration', i, c['rows'][r][4])
            ts.append(s0 + tchar(i, idx))
        idx = text.find(c['concl'][1]); assert idx >= 0, ('data card conclusion words not in the narration', i, c['concl'][1])
        ts.append(s0 + tchar(i, idx)); CHALK[i]['pop'] = ts
        for tt in ts: chalk_t.append(tt); audio.append((f'{SFX}/chalk.wav', tt, 0.38, 1))
for c in cues:
    audio.append((f'{SFX}/{c["file"]}', c['t'], dur(f'{SFX}/{c["file"]}'), c['vol']))
if os.environ.get('NOBGM') != '1':   # synthesised, ducked under the narration (guideline 7-3)
    import bgm_lib
    rep = bgm_lib.make_bgm(f'{B}/bgm.wav', TOTAL, [(f'{B}/n{i:02d}.wav', starts[i]) for i in SEL], below_db=float(os.environ.get('BGM_BELOW', '13')), style=getattr(CFG, 'STYLE', 'default'))
    audio.append((f'{B}/bgm.wav', 0.0, TOTAL, 1))
    print('bgm', {k: round(v, 1) for k, v in rep.items()})

# ---------- one pre-mixed file (the renderer's own mix of hundreds of <audio> tracks hit its 300 s ffmpeg timeout, 2026-10-11) ----------
SR = 48000; mix = np.zeros((int(TOTAL * SR) + SR, 2), dtype=np.float32); cache = {}
for (src, st, dd, vol) in audio:
    if src not in cache:
        raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', src, '-f', 'f32le', '-ac', '2', '-ar', str(SR), '-'], capture_output=True).stdout
        cache[src] = np.frombuffer(raw, dtype=np.float32).reshape(-1, 2)
    a = cache[src][:int(dd * SR)]; i0 = int(round(st * SR)); a = a[:max(0, len(mix) - i0)]
    mix[i0:i0 + len(a)] += a * float(vol)
mix = mix[:int(TOTAL * SR)]
peak = float(np.abs(mix).max()) if len(mix) else 0.0
if peak > 0.98: mix *= 0.98 / peak
wf = wave.open(f'{B}/mix.wav', 'wb'); wf.setnchannels(2); wf.setsampwidth(2); wf.setframerate(SR)
wf.writeframes((np.clip(mix, -1, 1) * 32767).astype('<i2').tobytes()); wf.close()
os.makedirs(OUT, exist_ok=True)
run('ffmpeg', '-y', '-v', 'error', '-i', f'{B}/mix.wav', '-c:a', 'aac', '-b:a', '192k', f'{OUT}/mix.m4a')
print('audio premix', len(audio), 'pieces -> mix.m4a, peak', round(20 * math.log10(max(peak, 1e-9)), 1), 'dBFS')

data = dict(slug=SLUG, total=TOTAL, lead=LEAD, gap=GAP, tail=TAIL, starts={str(k): v for k, v in starts.items()}, D={str(i): D[i - 1] for i in SEL},
            cuts=[dict(id=u['uid'], scene=u['scene'], kind=u['kind'], t0=u['t0'], t1=u['t1'], tr=u['tr'], text=u['text']) for u in units],
            caps=caps, sfx=cues, chalk=chalk_t, snap=snap_report, chalk_pop={str(k): v.get('pop') for k, v in CHALK.items() if 'pop' in v}, sel=SEL)
json.dump(data, open(B + ('/build_data.json' if len(SEL) == len(SCENES) else '/build_data_partial.json'), 'w'), ensure_ascii=False, indent=1)
print('audio/timing done:', TOTAL, 's,', len(units), 'units,', len(caps), 'caps,', len(cues), 'sfx cues')
