# -*- coding: utf-8 -*-
# Miya's Lab composition builder v3 (new look: one picture per meaning unit, focus camera, 5 transitions, synced SFX).
# usage: SLUG=x python3 build3.py [OUTDIR]
# env: PLAN=1   only write videos/<slug>/plan.json (unit split) and exit
#      SEL="1,2" build a partial test;  VERT=1  vertical 1080x1920 (Shorts, no logo)
#      FALLBACK=1  a unit without art3/<uid>.svg reuses the scene picture art/<id>.svg (tests only)
#      CINE=1      cine look (2026-10-14): no SVG art; only narration/captions/SFX/BGM -> render/<slug>/mix.m4a + build_data.json,
#                  then tools/build_cine.py writes the page from videos/<slug>/cine.json
import os, re, sys, json, html, shutil, subprocess, math, random
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from paths import *
import numpy as np
import palettes, labels_lib, caption_hl
SCENES = load_scenes()
CFG = load_config()
B = wdir() + '/build'
VERT = os.environ.get('VERT') == '1'
W, H = (1080, 1920) if VERT else (1920, 1080)
CX, CY = (540, 860) if VERT else (960, 500)          # centre object position (zoom-through / match pivot)
OUT = sys.argv[1] if len(sys.argv) > 1 else f'{REPO}/render/{SLUG}'
SEL = [int(x) for x in os.environ.get('SEL', '').split(',') if x] or list(range(1, len(SCENES) + 1))
LEAD, GAP, TAIL = (0.3, 0.5, 1.2) if VERT else (1.0, 0.8, 2.5)
MAXU = 6.2            # target max seconds per unit (narration part); +gap keeps every unit <= 7 s
# 2026-10-16 (learned in the cine experiment, guideline 20-2): the first minutes must change picture more often.
# config HOOK = dict(until=300, maxu=4.5): scenes that START before `until` seconds split at maxu instead of MAXU (more pictures).
# Shorts: HOOK = dict(until=999, maxu=4.8). Old videos without HOOK keep their unit split (plan.json / art3 stay valid).
HOOK = getattr(CFG, 'HOOK', None)
timing = json.load(open(B + '/timing_base.json')); D = timing['D']
BGMODE = getattr(CFG, 'BG', {})
ART3 = f'{vdir()}/art3'


def run(*a):
    return subprocess.run(a, capture_output=True, text=True)


def dur(f):
    return float(run('ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', f).stdout)


# ---------- scene start times ----------
starts = {}; t = LEAD
for i in SEL:
    starts[i] = t; t += D[i - 1] + GAP
TOTAL = round(starts[SEL[-1]] + D[SEL[-1] - 1] + TAIL, 3)
def MX(i):   # max narration seconds per unit for scene i (HOOK pacing)
    return HOOK['maxu'] if HOOK and starts.get(i, 1e9) < HOOK.get('until', 300) else MAXU


# ---------- sentence timing model (narration time of every character) ----------
def sentences(text):
    out = []
    for piece in re.split(r'(?<=[.?!])\s+', text.strip()):
        if out and (re.search(r'(?:^|\s)(?:[A-Z][a-z]*|[A-Z]\.)\s[A-Z]\.$', out[-1])
                    or (re.search(r'(?:^|\s)[A-Z]\.$', out[-1]) and re.match(r'[A-Z]\.(?:\s|$)', piece))):   # "C. M. Kosemen   # a middle initial ("George W. Bush", "H. W.") is not a sentence end; "vitamin A." is
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
for i in SEL:
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
    if tchar(i, c1) - tchar(i, c0) <= MX(i):
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
    # snap every atom start to the real first character (skip whitespace)
    atoms = [(a + (len(text[a:]) - len(text[a:].lstrip())), b) for a, b in atoms]
    us = []; cur = [atoms[0][0], atoms[0][1]]
    for (a, b) in atoms[1:]:
        if tchar(i, b) - tchar(i, cur[0]) <= MX(i):
            cur[1] = b
        else:
            us.append(tuple(cur)); cur = [a, b]
    us.append(tuple(cur))
    if len(us) > 1 and tchar(i, us[-1][1]) - tchar(i, us[-1][0]) < 2.0:
        # first try to move trailing atoms of the previous unit into the short last unit (keeps both <= MX(i))
        span = lambda a, b: tchar(i, b) - tchar(i, a)
        inner = [a for (a, b) in atoms if us[-2][0] < a < us[-2][1]]
        fixed = False
        for cut in reversed(inner):
            if span(cut, us[-1][1]) > MX(i): break
            if span(cut, us[-1][1]) >= 2.0 and span(us[-2][0], cut) >= 2.0:
                us = us[:-2] + [(us[-2][0], cut), (cut, us[-1][1])]; fixed = True; break
        if not fixed and span(us[-2][0], us[-1][1]) <= MX(i) + 0.8:
            us = us[:-2] + [(us[-2][0], us[-1][1])]
    # a very short unit (< 1.6 s of narration, e.g. "Start with the hunter.") is merged into its neighbour
    k = 0
    while len(us) > 1 and k < len(us):
        a, b = us[k]
        if tchar(i, b) - tchar(i, a) < 1.6:
            j = k + 1 if k + 1 < len(us) else k - 1
            lo, hi = min(us[k][0], us[j][0]), max(us[k][1], us[j][1])
            us = [u for m, u in enumerate(us) if m not in (k, j)]; us.insert(min(k, j), (lo, hi)); k = 0; continue
        k += 1
    return us


units = []; n = 0
for i in SEL:
    kind = SCENES[i - 1][2]; text = SCENES[i - 1][4]
    last_scene = (i == SEL[-1])
    s1_scene = TOTAL if last_scene else starts[SEL[SEL.index(i) + 1]]
    if kind == 'chalk':
        n += 1
        units.append(dict(n=n, uid=f'U{n:03d}', scene=i, kind='chalk', c0=0, c1=len(text), text=text, t0=0.0 if i == SEL[0] else starts[i], t1=s1_scene))
        continue
    us = units_of(i)
    for k, (a, b) in enumerate(us):
        n += 1
        t0 = (0.0 if i == SEL[0] else starts[i]) if k == 0 else starts[i] + tchar(i, a)
        t1 = s1_scene if k == len(us) - 1 else starts[i] + tchar(i, us[k + 1][0])
        units.append(dict(n=n, uid=f'U{n:03d}', scene=i, kind='ill', c0=a, c1=b, text=text[a:b].strip(), t0=t0, t1=t1))
# partial test (SEL without scene 1): numbering restarts at 1, so take each picture's uid from the full plan.json instead
_plan = f'{vdir()}/plan.json'
if os.environ.get('SEL') and os.environ.get('PLAN') != '1' and os.path.exists(_plan):
    _map = {(p['scene'], p['text']): p['uid'] for p in json.load(open(_plan))}
    for u in units:
        if u['kind'] == 'ill':
            u['uid'] = _map.get((u['scene'], u['text']), u['uid'])
for u in units:
    assert u['t1'] - u['t0'] > 1.5, ('unit too short', u)

# ---------- transitions (no same type twice in a row; hard around chalk; match only inside a scene) ----------
TR_WORDS = [   # a word in the unit text picks a transition that shows the same idea (70 % of the time, if allowed here)
    ('push', r'\b(fall\w*|fell|drop\w*|sink\w*|sank|plung\w*|descend\w*|rising|climb\w*|ascend\w*)\b'),
    ('whip', r'\b(speed\w*|race\w*|racing|rush\w*|sudden\w*|instant\w*|flash\w*)\b'),
    ('tilt', r'(\bimagine\b|\bwhat if\b|\bsurpris\w*|\btwist\w*)'),
    ('eye',  r'\b(open\w*|wake|woke|awake\w*|realis\w*|realiz\w*|discover\w*|reveal\w*)\b'),
]
rng = random.Random(20261009)
last2 = []; TR_COUNT = {}
for k, u in enumerate(units):
    if k == 0:
        u['tr'] = 'hard'; continue
    p = units[k - 1]
    if u['kind'] == 'chalk' or p['kind'] == 'chalk':
        u['tr'] = 'hard'; last2 = []; continue
    # 12 types (7 added 2026-10-14, user decision; the mosaic 'dots' was tried and dropped the same day): not every cut grows out of the centre object any more
    pool = ['zoom', 'fade', 'slide', 'match', 'wash', 'wipe', 'iris', 'eye', 'push', 'whip', 'tilt']
    if u['scene'] != p['scene']:
        pool.remove('match'); pool += ['zoom', 'wash', 'blinds', 'blinds', 'eye']   # scene change: favour the big covering cuts
    pool = [x for x in pool if x not in last2[-1:]]
    if len(last2) >= 2:
        pool = [x for x in pool if x not in last2[-2:]] or pool
    # balance: a type already used a lot is picked less (so 13 types spread out); a matching word wins half the time
    # unless that type is already above its fair share
    fair = (sum(TR_COUNT.values()) + 1) / 11
    kw = [t for t, rx in TR_WORDS if t in pool and TR_COUNT.get(t, 0) <= fair * 1.3 and re.search(rx, u['text'], re.I)]
    if kw and rng.random() < .5: u['tr'] = kw[0]
    else: u['tr'] = rng.choices(pool, weights=[1 / (1 + TR_COUNT.get(x, 0)) ** 1.5 for x in pool])[0]
    last2.append(u['tr']); TR_COUNT[u['tr']] = TR_COUNT.get(u['tr'], 0) + 1
CINE = os.environ.get('CINE') == '1'
if CINE:   # transitions come from videos/<slug>/cine.json: a chapter's or shot's first unit carries its transition (for its sound)
    _cine = json.load(open(os.environ.get('CINE_JSON') or f'{vdir()}/cine.json'))
    _first = {}
    for _ch in _cine['chapters']:
        _shots = _ch.get('shots') or [dict(frm=_ch['from'], tr=_ch.get('tr', 'dip'))]
        for _k, _s in enumerate(_shots):
            _first[_s.get('frm', _s.get('from'))] = _s.get('tr', _ch.get('tr', 'dip')) if _k else _ch.get('tr', _s.get('tr', 'dip'))
    for _k, u in enumerate(units):
        u['tr'] = 'cut' if _k == 0 else ('dip' if u['kind'] == 'chalk' or (_k and units[_k - 1]['kind'] == 'chalk') else _first.get(u.get('uid'), 'none'))
    CINE_BEATS = _cine.get('beats', {})
TIN = {'hard': 0.0, 'zoom': 0.5, 'fade': 0.6, 'slide': 0.7, 'match': 0.9, 'wash': 0.0,
       'wipe': 0.8, 'iris': 0.9, 'eye': 0.8, 'blinds': 0.65, 'push': 0.7, 'whip': 0.45, 'tilt': 0.8}

# ---------- sidecars / art ----------
def side(u):
    if CINE: return CINE_BEATS.get(u['uid'], {})
    f = f'{ART3}/{u["uid"]}.json'
    return json.load(open(f)) if os.path.exists(f) else {}


def art_path(u):
    f = f'{ART3}/{u["uid"]}.svg'
    if os.path.exists(f): return f, False
    assert os.environ.get('FALLBACK') == '1', ('missing art', u['uid'])
    return f'{vdir()}/art/{SCENES[u["scene"] - 1][3]}.svg', True


if os.environ.get('PLAN') == '1':
    if not getattr(CFG, 'PAL_DEFAULT', None): print('WARNING: config.py has no PAL_DEFAULT -> legacy purple/peach palette. Choose palettes from tools/palettes.py for this topic.')
    plan = []
    for k, u in enumerate(units):
        if u['kind'] == 'chalk': continue
        sc = SCENES[u['scene'] - 1]
        plan.append(dict(uid=u['uid'], scene=u['scene'], title=sc[1], art_theme=sc[3], bg=BGMODE.get(sc[3], 'paper'), pal=palettes.describe(palettes.for_theme(CFG, sc[3])), text=u['text'],
                         dur=round(u['t1'] - u['t0'], 2), transition_in=u['tr'], prev=units[k - 1]['text'] if k and units[k - 1]['scene'] == u['scene'] else '',
                         nxt=units[k + 1]['text'] if k + 1 < len(units) and units[k + 1]['scene'] == u['scene'] else ''))
    os.makedirs(vdir(), exist_ok=True)
    json.dump(plan, open(f'{vdir()}/plan.json', 'w'), ensure_ascii=False, indent=1)
    d = [p['dur'] for p in plan]
    print('units', len(plan), 'avg', round(sum(d) / len(d), 2), 'max', max(d), 'min', min(d), 'total', TOTAL)
    sys.exit(0)

os.makedirs(OUT, exist_ok=True)
for name in ['gsap.min.js', 'Fredoka-700.woff2', 'PatrickHand-400.woff2', 'logo.png', 'grain.png']:
    shutil.copy(f'{ASSETS}/{name}', f'{OUT}/{name}')
import sfx_lib
sfx_lib.make_all(OUT)
sfx_lib.make_chalk(f'{OUT}/chalk.wav') if hasattr(sfx_lib, 'make_chalk') else None

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


# ---------- SVG inlining ----------
def load_svg(n, path):
    s = open(path, encoding='utf-8').read()
    s = re.sub(r'<\?xml[^>]*\?>', '', s).strip()
    pre = f'u{n}_'
    ids = set(re.findall(r'\bid="([^"]+)"', s))
    def mv(m):
        tag = m.group(0); name = re.search(r'\bid="(mv-[^"]+)"', tag).group(1)
        tag = re.sub(r'\s*\bid="mv-[^"]+"', '', tag)
        if re.search(r'\bclass="', tag):
            tag = re.sub(r'\bclass="([^"]*)"', lambda mm: f'class="{mm.group(1)} mv {name}"', tag, 1)
        else:
            tag = tag[:-1].rstrip('/') + f' class="mv {name}"' + ('/>' if tag.endswith('/>') else '>')
        return tag
    s = re.sub(r'<[a-zA-Z][^>]*\bid="mv-[^"]+"[^>]*>', mv, s)
    ids = {x for x in ids if not x.startswith('mv-')}
    for x in ids:
        s = s.replace(f'id="{x}"', f'id="{pre}{x}"').replace(f'url(#{x})', f'url(#{pre}{x})').replace(f'href="#{x}"', f'href="#{pre}{x}"')
    s = re.sub(rf'\swidth="{W}"\s+height="{H}"', '', s, count=1)
    return s


# ---------- chalkboard (unchanged from v2) ----------
CHALK = CFG.CHALK
ROW_Y = [294, 459, 630]


def chalk_html(i):
    c = CHALK[i]; out = [f'<div class="chalk" id="k{i}">']
    out.append(f'<div class="ct">{html.escape(c["title"])}</div><div class="cs">{html.escape(c["sub"])}</div>')
    out.append(f'<div class="csrc">{html.escape(c["src"])}</div><div class="csig">Talking in class:<br>Miya</div>')
    for r, (lab, val, info, col, key) in enumerate(c['rows']):
        out.append(f'<div class="ph" id="k{i}ph{r}" style="top:{ROW_Y[r]}px"></div>')
        out.append(f'<div class="row {col}" id="k{i}r{r}" style="top:{ROW_Y[r]}px"><span class="l">{html.escape(lab)}</span>'
                   f'<span class="v">{html.escape(val)}</span><span class="n">{html.escape(info)}</span></div>')
    out.append(f'<div class="cc" id="k{i}cc">{html.escape(c["concl"][0])}</div>')
    out.append('<div class="chalks"><i style="background:#f4f1e8"></i><i style="background:#efca69"></i><i style="background:#e5826b"></i><i style="background:#9fd0e6"></i></div>')
    out.append('<div class="erasers"><b></b><b></b></div></div>')
    return '\n'.join(out)


# ---------- html ----------
WASHC = {'paper': '#ece4d1', 'night': '#14122b', 'dusk': '#5a4562'}      # old default; the palette of each scene overrides it (tools/palettes.py)
def washc(u):
    th = SCENES[u['scene'] - 1][3]; w = palettes.PALETTES[palettes.for_theme(CFG, th)]['wash']
    return dict(zip(('paper', 'night', 'dusk'), w))
import colorsys
def _hex(c): c = c.lstrip('#'); return [int(c[i:i + 2], 16) / 255 for i in (0, 2, 4)]
def scene_tones(u, n):
    """n muted tones of ONE colour family from the scene's own palette (user decision 2026-10-14: blinds must not
    bring in contrasting colours). Base = the scene background colour for its mode; partner = the palette accent closest in hue;
    tones step between them, then saturation is cut by a third."""
    th = SCENES[u['scene'] - 1][3]; P = palettes.PALETTES[palettes.for_theme(CFG, th)]; bg = BGMODE.get(th, 'paper')
    base = {'night': P['night'][1], 'dusk': P['dusk'][1], 'paper': P['paper'][0]}.get(bg, P['paper'][0])
    hb = colorsys.rgb_to_hls(*_hex(base))[0]
    acc = min(P['accents'], key=lambda c: min(abs(colorsys.rgb_to_hls(*_hex(c))[0] - hb), 1 - abs(colorsys.rgb_to_hls(*_hex(c))[0] - hb)))
    a, b = _hex(base), _hex(acc); out = []
    lo, hi = (.15, .5) if bg != 'paper' else (.12, .38)
    for i in range(n):
        t = lo + (hi - lo) * i / max(n - 1, 1)
        r, g, bl = [a[j] + (b[j] - a[j]) * t for j in range(3)]
        H_, L_, S_ = colorsys.rgb_to_hls(r, g, bl); r, g, bl = colorsys.hls_to_rgb(H_, L_, S_ * .66)
        out.append('#%02x%02x%02x' % tuple(int(round(v * 255)) for v in (r, g, bl)))
    return out
h = ['<!doctype html><html lang="en"><head><meta charset="UTF-8">', f'<meta name="viewport" content="width={W}, height={H}">']
h.append('<script src="gsap.min.js"></script><style>')
capcss = (".cap{position:absolute;left:0;width:%dpx;bottom:%dpx;display:flex;justify-content:center;opacity:0;z-index:1002}"
          ".cap span{font-family:Fredoka,sans-serif;font-weight:700;font-size:%dpx;line-height:%dpx;color:#fff;background:rgba(0,0,0,.62);border-radius:12px;padding:20px;%s}"
          % ((W, 360, 60, 68, 'white-space:normal;max-width:900px;text-align:center') if VERT else (W, 60, 58, 54, 'white-space:nowrap'))
          + caption_hl.CSS)
h.append('''@font-face{font-family:Fredoka;src:url(Fredoka-700.woff2) format("woff2");font-weight:700}
@font-face{font-family:Patrick;src:url(PatrickHand-400.woff2) format("woff2");font-weight:400}
*{margin:0;padding:0;box-sizing:border-box}html,body{width:%dpx;height:%dpx;overflow:hidden;background:#000}
#root{position:relative;width:%dpx;height:%dpx;overflow:hidden}
.t{position:absolute;left:0;top:0;width:%dpx;height:%dpx;display:none;overflow:hidden}
.w{position:absolute;left:0;top:0;width:%dpx;height:%dpx}
.w svg{position:absolute;left:0;top:0;width:%dpx;height:%dpx}
#wash{position:absolute;left:0;top:0;width:%dpx;height:%dpx;opacity:0;z-index:1000;pointer-events:none}
#tredge{position:absolute;left:0;top:0;width:%dpx;height:%dpx;z-index:999;pointer-events:none;display:none}
.trb{position:absolute;top:0;height:%dpx;z-index:999;transform:scaleY(0);transform-origin:top;pointer-events:none}
.trs{position:absolute;left:0;height:6px;border-radius:3px;background:#fff;z-index:999;opacity:0;pointer-events:none}
''' % ((W, H) * 7 + (H,)))
h.append(capcss); h.append(labels_lib.CSS)
h.append('''#logo{position:absolute;left:1799px;top:40px;width:81px;height:81px;z-index:1003}
#grain{position:absolute;left:0;top:0;width:@Wpx;height:@Hpx;z-index:1001;opacity:.35;pointer-events:none;object-fit:cover}
.chalk{position:absolute;left:0;top:0;width:1920px;height:1080px;display:none;background:
 radial-gradient(ellipse at 22% 30%,rgba(255,255,255,.05),transparent 45%),radial-gradient(ellipse at 70% 65%,rgba(255,255,255,.045),transparent 50%),
 radial-gradient(ellipse at 45% 90%,rgba(255,255,255,.04),transparent 40%),#2D4F40}
.chalk:after{content:"";position:absolute;left:0;bottom:0;width:1920px;height:28px;background:#9E7246}
.ct{position:absolute;left:135px;top:70px;font:700 66px/80px Fredoka,sans-serif;color:#fff}
.cs{position:absolute;left:137px;top:152px;font:400 28px/34px Patrick,sans-serif;color:#d9dccf}
.csrc{position:absolute;left:135px;top:858px;font:400 24px/30px Patrick,sans-serif;color:#9fb0a5}
.csig{position:absolute;left:1500px;top:836px;width:300px;font:400 24px/30px Patrick,sans-serif;color:#9fb0a5;text-align:right}
.ph{position:absolute;left:234px;width:1452px;height:140px;border:2px dashed rgba(255,255,255,.22);border-radius:6px}
.row{position:absolute;left:234px;width:1452px;height:140px;background:#364236;border:3px solid;border-radius:6px;opacity:0;display:flex;align-items:center}
.row.y{border-color:#EFCA69}.row.c{border-color:#E5826B}
.row .l{width:430px;padding-left:36px;font:400 30px/34px Patrick,sans-serif;color:#d9dccf}
.row .v{width:560px;text-align:center;font:700 78px/90px Fredoka,sans-serif}
.row.y .v{color:#EFCA69}.row.c .v{color:#E5826B}
.row .n{width:462px;padding-right:30px;text-align:right;font:400 26px/32px Patrick,sans-serif;color:#d9dccf}
.cc{position:absolute;left:0;width:1920px;top:790px;text-align:center;font:700 38px/46px Fredoka,sans-serif;color:#fff;opacity:0}
.chalks{position:absolute;left:70px;top:1032px;display:flex;gap:18px}.chalks i{display:block;width:56px;height:14px;border-radius:5px}
.erasers{position:absolute;left:1722px;top:1022px;display:flex;gap:14px}.erasers b{display:block;width:70px;height:26px;border-radius:4px;background:#5b4a38;border-bottom:8px solid #c9b79a}
'''.replace('@W', str(W)).replace('@H', str(H)))
h.append('.spd{position:absolute;left:0;top:0;width:%dpx;height:%dpx;pointer-events:none;overflow:hidden;opacity:0}.spd i{position:absolute;left:0;top:0;width:0;height:0}.spd b{position:absolute;left:0;top:-2px;width:210px;height:4px;border-radius:2px;background:linear-gradient(90deg,rgba(255,255,255,0),rgba(255,255,255,.85));transform-origin:0 50%%;opacity:0}' % (W, H))
h.append('</style></head><body>')
h.append(f'<div id="root" data-composition-id="main" data-start="0" data-duration="{TOTAL}" data-width="{W}" data-height="{H}">')
# speed streaks (2026-10-16, learned in the cine experiment; guideline 20-3). Cosmic videos get them on speed words; any video can force
# them with sidecar "speed": true (or turn them off with false).
SPEED_RE = re.compile(r"\b(speed\w*|fast\w*|accelerat\w*|racing|races?|rush\w*|launch\w*|rocket\w*|warp\w*|hurtl\w*|flying|flee\w*|fled|reced\w*|expand\w*|explod\w*|burst\w*|blast\w*|stream\w*|zoom\w*)\b", re.I)
NSPD = 30
def is_speed(u, sc0):
    if 'speed' in sc0: return bool(sc0['speed'])
    return getattr(CFG, 'STYLE', 'default') == 'cosmic' and bool(SPEED_RE.search(u['text']))
DRIFT = getattr(CFG, 'DRIFT', True)   # slow continuous camera move on every picture without a focus target (guideline 20-1)
fallback_used = []; label_errors = []; label_items = {}
for u in units:
    nn = u['n']
    if CINE: continue
    if u['kind'] == 'chalk':
        h.append(f'<div class="t" id="t{nn}" style="z-index:{nn}"><div class="w" id="w{nn}">{chalk_html(u["scene"])}</div></div>')
    else:
        p, fb = art_path(u)
        if fb: fallback_used.append(u['uid'])
        sc0 = side(u); th = SCENES[u['scene'] - 1][3]
        lerr = labels_lib.check(sc0, u['text'], W, H, VERT)
        if lerr: label_errors.append(f'{u["uid"]}: ' + '; '.join(lerr))
        lin, lout, litems = ('', '', []) if lerr else labels_lib.html_for(nn, sc0, BGMODE.get(th, 'paper'), palettes.PALETTES[palettes.for_theme(CFG, th)], W, H, VERT)
        label_items[nn] = litems
        spot = ''
        fz = sc0.get('focus')
        if fz and sc0.get('spot', True):   # focus spotlight: the rest of the picture dims while the camera pushes in (guideline 4-1)
            fx, fy, fs = float(fz[0]), float(fz[1]), max(float(fz[2]), 1.0)
            spot = (f'<div class="spot" id="sp{nn}" style="position:absolute;left:0;top:0;width:{W}px;height:{H}px;pointer-events:none;opacity:0;'
                    f'background:radial-gradient(circle at {fx:.0f}px {fy:.0f}px,rgba(0,0,0,0) {.30 * W / fs:.0f}px,rgba(0,0,0,.5) {.62 * W / fs:.0f}px)"></div>')
        spd = ''
        if is_speed(u, sc0):   # speed streaks (guideline 20-3): radial lines that accelerate out of frame and keep respawning
            ox, oy = (float(fz[0]), float(fz[1])) if fz else (CX, CY)
            spd = (f'<div class="spd" id="spd{nn}"><div style="position:absolute;left:{ox:.0f}px;top:{oy:.0f}px">'
                   + ''.join(f'<i style="transform:rotate({(k * 137.508) % 360:.1f}deg)"><b></b></i>' for k in range(NSPD)) + '</div></div>')
        h.append(f'<div class="t" id="t{nn}" style="z-index:{nn}"><div class="w" id="w{nn}">{load_svg(nn, p)}{spot}{lin}</div>{spd}{lout}</div>')
if label_errors: raise SystemExit('on-screen text (labels) problems, fix the sidecars:\n  ' + '\n  '.join(label_errors))
h.append('<div id="wash"></div><img id="grain" src="grain.png">' + ('' if VERT else '<img id="logo" src="logo.png">'))
# shared overlays for the 2026-10-14 transitions (cuts never overlap: units are at least 1.5 s apart)
h.append(f'<svg id="tredge" viewBox="0 0 {W} {H}"><line id="treline" x1="0" y1="0" x2="0" y2="0" stroke="#ffd54a" stroke-width="10" stroke-linecap="round"/></svg>')
NB = 6; h.append(''.join(f'<div class="trb" id="trb{i}" style="left:{i * W // NB}px;width:{W // NB + 2}px"></div>' for i in range(NB)))
h.append(''.join(f'<div class="trs" id="trs{i}" style="top:{int(H * (.1 + .09 * i))}px;width:{int(W * (.26 + ((i * 37) % 36) / 100))}px"></div>' for i in range(9)))
for k, c in enumerate(caps):
    h.append(f'<div class="cap" id="c{k}"><span>{caption_hl.words_html(k, c["text"])}</span></div>')   # one <i> per word for the highlight

# ---------- sound cues ----------
cues = []   # dict(name, t, vol, pri)
TRSND = {'zoom': ('swish', -0.85, 0.9), 'slide': ('swish', -0.6, 0.6), 'match': ('hush', -0.7, 0.8), 'wash': ('rustle', -0.5, 0.7),
         'wipe': ('swish', -0.7, 0.6), 'iris': ('hush', -0.9, 0.7), 'eye': ('hush', -0.7, 0.6), 'blinds': ('rustle', -0.6, 0.6),
         'push': ('swish', -0.6, 0.6), 'whip': ('swish', -0.4, 0.8), 'tilt': ('pop', -0.7, 0.6),
         'dip': ('hush', -0.5, 0.55), 'flash': ('hush', -0.4, 0.7), 'zoom': ('swish', -0.85, 0.9)}
if getattr(CFG, 'STYLE', 'default') == 'cosmic':   # cosmic videos: no swish/hush (guideline 3-7)
    TRSND = {'zoom': ('warp', -0.45, 0.8), 'slide': ('warp', -0.35, 0.5), 'match': ('glimmer', -0.5, 0.7), 'wash': ('sparkle', -0.4, 0.6),
             'wipe': ('warp', -0.6, 0.5), 'iris': ('glimmer', -0.8, 0.6), 'eye': ('glimmer', -0.6, 0.6), 'blinds': ('sparkle', -0.5, 0.5),
             'push': ('warp', -0.5, 0.5), 'whip': ('warp', -0.35, 0.7), 'tilt': ('pop', -0.7, 0.5),
             'dip': ('glimmer', -0.45, 0.55), 'flash': ('bloom', -0.35, 0.7), 'zoom': ('warp', -0.45, 0.8)}
focus_cam = {}; label_t = []
for u in units:
    nn = u['n']
    if u['kind'] == 'chalk': continue
    sc = side(u) if os.path.exists(f'{ART3}/{u["uid"]}.json') else {}
    text = SCENES[u['scene'] - 1][4]; base = starts[u['scene']]
    def tword(word):
        if not word: return None
        j = text.find(word, u['c0'])
        if j < 0 or j >= u['c1']: return None
        return base + tchar(u['scene'], j)
    if u['tr'] in TRSND:
        nm, off, vol = TRSND[u['tr']]
        cues.append(dict(name=nm, t=max(u['t0'] + off, 0.05), vol=vol, pri=2, unit=u['uid']))
    f = sc.get('focus')
    if f:
        tf = tword(sc.get('focus_word')) or (u['t0'] + 1.5)
        a = max(u['t0'] + 0.9, tf - 0.5); a = min(a, u['t1'] - 0.3 - 1.4)
        if a > u['t0'] + 0.5:
            focus_cam[nn] = (a, f)
            if sc.get('focus_tick', True): cues.append(dict(name='tick', t=a + 0.35, vol=0.6, pri=1, unit=u['uid']))
    for k2, (ty, lid, gid, l) in enumerate(label_items.get(nn, [])):
        tl_ = tword(l.get('word')) or (u['t0'] + 0.4 + 0.5 * k2)
        label_t.append((nn, ty, lid, gid, min(max(tl_ - 0.1, u['t0'] + 0.15), u['t1'] - 1.0)))
    for e in sc.get('sfx', []):
        te = tword(e.get('word'))
        if te is None: te = u['t0'] + 1.0
        cues.append(dict(name=e['name'], t=te + e.get('offset', 0.0), vol=e.get('vol', 0.8), pri=3, unit=u['uid']))
cues.sort(key=lambda c: c['t'])
kept = []
for c in sorted(cues, key=lambda c: -c['pri']):
    if all(abs(c['t'] - k['t']) >= 0.9 for k in kept): kept.append(c)
cues = sorted(kept, key=lambda c: c['t'])
SFXLEN = {}
vcount = {}
for c in cues:      # alias old names, cycle the 3 recorded variants of each sound
    nm = sfx_lib.ALIAS.get(c['name'], c['name'])
    if nm not in sfx_lib.LIB: raise SystemExit(f'unknown sfx name {nm} in {c["unit"]}')
    k = vcount.get(nm, 0); vcount[nm] = k + 1; v = k % sfx_lib.VARIANTS + 1
    c['file'] = f'sfx_{nm}{"" if v == 1 else "_" + str(v)}.wav'
    if c['file'] not in SFXLEN: SFXLEN[c['file']] = dur(f'{OUT}/{c["file"]}')

audio = []
for i in SEL:
    run('ffmpeg', '-y', '-v', 'error', '-i', f'{B}/n{i:02d}.wav', '-c:a', 'aac', '-b:a', '192k', f'{OUT}/n{i:02d}.m4a')
    audio.append((f'n{i:02d}.m4a', starts[i], dur(f'{OUT}/n{i:02d}.m4a'), 0, 1))
chalk_t = []
for i in SEL:
    if i in CHALK:
        s0 = starts[i]; c = CHALK[i]; ts = [s0 + 0.05]; text = SCENES[i - 1][4]
        for r in (1, 2):
            idx = text.find(c['rows'][r][4]); assert idx >= 0
            ts.append(s0 + tchar(i, idx))
        idx = text.find(c['concl'][1]); assert idx >= 0
        ts.append(s0 + tchar(i, idx)); CHALK[i]['pop'] = ts
        for tt in ts: chalk_t.append(tt); audio.append(('chalk.wav', tt, 0.38, 1, 1))
tracks_end = {}
for c in cues:
    d = SFXLEN[c['file']]; tr = 2
    while tracks_end.get(tr, -1) > c['t'] + 1e-6: tr += 1
    tracks_end[tr] = c['t'] + d
    audio.append((c['file'], c['t'], d, tr, c['vol']))
# ---------- background music (synthesised, ducked under the narration; SFX bgm off with NOBGM=1) ----------
BGM_REPORT = None
if os.environ.get('NOBGM') != '1':
    import bgm_lib
    BGM_REPORT = bgm_lib.make_bgm(f'{B}/bgm.wav', TOTAL, [(f'{B}/n{i:02d}.wav', starts[i]) for i in SEL], below_db=float(os.environ.get('BGM_BELOW', '13')), style=getattr(CFG, 'STYLE', 'default'))
    run('ffmpeg', '-y', '-v', 'error', '-i', f'{B}/bgm.wav', '-c:a', 'aac', '-b:a', '96k', f'{OUT}/bgm.m4a')
    audio.append(('bgm.m4a', 0.0, TOTAL, 20, 1))
    print('bgm', {k: round(v, 1) for k, v in BGM_REPORT.items()})
# ---------- one pre-mixed audio file (2026-10-11): the renderer's own mix of ~400 <audio> tracks hit its 300 s ffmpeg timeout
# on the server ("audio_processing_failed: ffmpeg_timeout", paleozoic-chronicles run #21/#22). The same sum (start, length, volume)
# is now done here with numpy and the page carries a single track. SEPARATE_AUDIO=1 keeps the old per-track layout.
if os.environ.get('SEPARATE_AUDIO') == '1':
    for (src, st, dd, tr, vol) in audio:
        h.append(f'<audio src="{src}" data-start="{st:.3f}" data-duration="{dd:.3f}" data-track-index="{tr}" data-volume="{vol}"></audio>')
else:
    SR = 48000; mixbuf = np.zeros((int(TOTAL * SR) + SR, 2), dtype=np.float32); cache = {}
    for (src, st, dd, tr, vol) in audio:
        if src not in cache:
            raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', f'{OUT}/{src}', '-f', 'f32le', '-ac', '2', '-ar', str(SR), '-'], capture_output=True).stdout
            cache[src] = np.frombuffer(raw, dtype=np.float32).reshape(-1, 2)
        a = cache[src][:int(dd * SR)]; i0 = int(round(st * SR)); a = a[:max(0, len(mixbuf) - i0)]
        mixbuf[i0:i0 + len(a)] += a * float(vol)
    mixbuf = mixbuf[:int(TOTAL * SR)]
    peak = float(np.abs(mixbuf).max()) if len(mixbuf) else 0.0
    if peak > 0.98: mixbuf *= 0.98 / peak
    import wave
    wf = wave.open(f'{B}/mix.wav', 'wb'); wf.setnchannels(2); wf.setsampwidth(2); wf.setframerate(SR)
    wf.writeframes((np.clip(mixbuf, -1, 1) * 32767).astype('<i2').tobytes()); wf.close()
    run('ffmpeg', '-y', '-v', 'error', '-i', f'{B}/mix.wav', '-c:a', 'aac', '-b:a', '192k', f'{OUT}/mix.m4a')
    used = {x[0] for x in audio}
    for f in used:                          # the separate pieces are no longer needed in the render folder
        if f != 'mix.m4a' and os.path.exists(f'{OUT}/{f}'): os.remove(f'{OUT}/{f}')
    h.append(f'<audio src="mix.m4a" data-start="0" data-duration="{TOTAL:.3f}" data-track-index="0" data-volume="1"></audio>')
    print('audio premix', len(audio), 'pieces -> mix.m4a, peak', round(20 * math.log10(max(peak, 1e-9)), 1), 'dBFS')
if CINE:   # cine look: the page is written by tools/build_cine.py
    for f in os.listdir(OUT):
        if f.startswith('sfx_') or f in ('Fredoka-700.woff2', 'PatrickHand-400.woff2', 'grain.png', 'chalk.wav', 'index.html'): os.remove(f'{OUT}/{f}')
    data = dict(slug=SLUG, total=TOTAL, lead=LEAD, gap=GAP, tail=TAIL, starts={str(k): v for k, v in starts.items()}, D={str(i): D[i - 1] for i in SEL},
                cuts=[dict(id=u['uid'], scene=u['scene'], kind=u['kind'], t0=u['t0'], t1=u['t1'], tr=u['tr'], text=u['text']) for u in units],
                caps=caps, sfx=cues, chalk=chalk_t, snap=snap_report, chalk_pop={str(k): v.get('pop') for k, v in CHALK.items() if 'pop' in v}, sel=SEL)
    json.dump(data, open(B + ('/build_data.json' if len(SEL) == len(SCENES) else '/build_data_partial.json'), 'w'), ensure_ascii=False, indent=1)
    print('CINE audio/timing done:', TOTAL, 's,', len(units), 'units,', len(caps), 'caps,', len(cues), 'sfx cues')
    sys.exit(0)

# ---------- timeline ----------
import motions  # centre-object motions (guideline 4-1)
js = ['<script>' + motions.WRAP_JS + motions.CHALK_FIT_JS + f'miyaWrapCores({CX},{CY});const tl=gsap.timeline({{paused:true}});']
ORG = f'{CX}px {CY}px'
MV = {'flame': ('pulse', .30), 'lamp': ('glow', 1.2), 'lantern': ('glow', 1.3), 'beacon': ('glow', 1.5), 'glint': ('glow', 1.4),
      'spark': ('pulse', .25), 'smoke': ('drift', 1.6), 'steam': ('drift', 1.3), 'stink': ('drift', 1.1), 'cells': ('drift', 1.8),
      'antenna': ('sway', .35), 'breathe': ('breathe', 2.2), 'nod': ('nod', 1.8), 'lean': ('lean', 3.0), 'arm': ('arm', 1.4),
      'walk': ('walk', 3.5), 'hand': ('hand', 1.0), 'rain': ('drift', .9), 'bell': ('swing', .8), 'knot': ('swing', 1.2), 'key': ('drift', .8),
      # cosmic mode (guideline 3-7)
      'drift-nebula': ('nebula', 10.0), 'orbit': ('orbit', 24.0), 'pulse': ('glow', 1.6)}
import pivots   # shoulder/wrist pivots for arm and hand groups (arms used to swing off the body)
PIV = pivots.compute(sorted({art_path(u)[0] for u in units if u['kind'] != 'chalk'}), W, H, cache=f'{B}/pivots.json')
CORE_USED = []   # centre-motion type per picture, in order (checked after the loop)
for k, u in enumerate(units):
    nn = u['n']; t0, t1 = u['t0'], u['t1']; tr = u['tr']; T = f'#t{nn}'; Wq = f'#w{nn}'
    v0 = t0 - TIN[tr]
    nxt = units[k + 1] if k + 1 < len(units) else None
    js.append(f'tl.set("{T}",{{display:"block"}},{v0:.3f});tl.set("{T}",{{display:"none"}},{t1:.3f});')
    if u['kind'] == 'chalk':
        i = u['scene']; ts = CHALK[i]['pop']
        js.append(f'tl.set("#k{i}",{{display:"block"}},{t0:.3f});tl.set("#k{i}",{{display:"none"}},{t1:.3f});')
        js.append(f'tl.set("#k{i}r0",{{opacity:1}},{t0:.3f});tl.set("#k{i}ph0",{{opacity:0}},{t0:.3f});')
        for r, tt in ((1, ts[1]), (2, ts[2])):
            js.append(f'tl.set("#k{i}ph{r}",{{opacity:0}},{tt:.3f});tl.fromTo("#k{i}r{r}",{{opacity:1,scale:.96}},{{scale:1.02,duration:.05,ease:"power1.out",immediateRender:false}},{tt:.3f});tl.to("#k{i}r{r}",{{scale:1,duration:.05,ease:"power1.in"}},{tt + .05:.3f});')
        js.append(f'tl.fromTo("#k{i}cc",{{opacity:1,scale:.96}},{{scale:1.02,duration:.05,immediateRender:false}},{ts[3]:.3f});tl.to("#k{i}cc",{{scale:1,duration:.05}},{ts[3] + .05:.3f});')
        js.append(f'tl.set("#k{i}r1",{{opacity:0}},{t0:.3f});tl.set("#k{i}r2",{{opacity:0}},{t0:.3f});tl.set("#k{i}cc",{{opacity:0}},{t0:.3f});tl.set("#k{i}ph1",{{opacity:1}},{t0:.3f});tl.set("#k{i}ph2",{{opacity:1}},{t0:.3f});')
        continue
    # resting state of wrapper + camera
    js.append(f'tl.set("{T}",{{scale:1,x:0,y:0,opacity:1,clipPath:"none",transformOrigin:"{ORG}"}},{v0:.3f});')
    js.append(f'tl.set("{Wq}",{{scale:1,x:0,y:0,transformOrigin:"0px 0px"}},{v0:.3f});')
    # --- entry transition ---
    if tr == 'zoom':
        js.append(f'tl.fromTo("{T}",{{scale:2.4,opacity:0}},{{scale:1,duration:1.7,ease:"power3.out",immediateRender:false}},{v0:.3f});')
        js.append(f'tl.to("{T}",{{opacity:1,duration:.5,ease:"none"}},{v0:.3f});')
    elif tr == 'fade':
        js.append(f'tl.fromTo("{T}",{{opacity:0}},{{opacity:1,duration:.6,ease:"power1.inOut",immediateRender:false}},{v0:.3f});')
    elif tr == 'slide':
        js.append(f'tl.fromTo("{T}",{{x:{W}}},{{x:0,duration:.7,ease:"power2.out",immediateRender:false}},{v0:.3f});')
    elif tr == 'match':
        js.append(f'tl.fromTo("{T}",{{clipPath:"circle(120px at {CX}px {CY}px)"}},{{clipPath:"circle({int(max(W, H) * .95)}px at {CX}px {CY}px)",duration:.9,ease:"power2.inOut",immediateRender:false}},{v0:.3f});')
        js.append(f'tl.set("{T}",{{clipPath:"none"}},{t0 + .002:.3f});')
    elif tr == 'wash':
        bg = BGMODE.get(SCENES[u['scene'] - 1][3], 'paper')
        js.append(f'tl.set("#wash",{{background:"{washc(u).get(bg, washc(u)["paper"])}"}},{t0 - .5:.3f});')
        js.append(f'tl.fromTo("#wash",{{opacity:0}},{{opacity:1,duration:.45,ease:"power1.in",immediateRender:false}},{t0 - .45:.3f});')
        js.append(f'tl.to("#wash",{{opacity:0,duration:.45,ease:"power1.out"}},{t0:.3f});')
    elif tr == 'wipe':   # diagonal wipe led by a thin light edge; direction alternates
        m = nn % 2
        a0, a1 = ('polygon(0px 0px,0px 0px,0px 0px)', f'polygon(0px 0px,{W * 2.6:.0f}px 0px,0px {W * 2.6:.0f}px)') if not m else \
                 (f'polygon({W}px 0px,{W}px 0px,{W}px 0px)', f'polygon({W}px 0px,{W - W * 2.6:.0f}px 0px,{W}px {W * 2.6:.0f}px)')
        e0 = (0, 0, 0, 0) if not m else (W, 0, W, 0); e1 = (W * 2.6, 0, 0, W * 2.6) if not m else (W - W * 2.6, 0, W, W * 2.6)
        js.append(f'tl.fromTo("{T}",{{clipPath:"{a0}"}},{{clipPath:"{a1}",duration:.8,ease:"power2.inOut",immediateRender:false}},{v0:.3f});')
        js.append(f'tl.set("{T}",{{clipPath:"none"}},{v0 + .81:.3f});')
        js.append(f'tl.set("#tredge",{{display:"block"}},{v0:.3f});tl.set("#tredge",{{display:"none"}},{v0 + .8:.3f});')
        js.append(f'tl.fromTo("#treline",{{attr:{{x1:{e0[0]},y1:{e0[1]},x2:{e0[2]},y2:{e0[3]}}}}},{{attr:{{x1:{e1[0]:.0f},y1:{e1[1]},x2:{e1[2]},y2:{e1[3]:.0f}}},duration:.8,ease:"power2.inOut",immediateRender:false}},{v0:.3f});')
    elif tr == 'iris':   # circle opens from a subject at the side (sidecar "iris" [x,y], else an off-centre focus, else left/right)
        sc_ = side(u); ip = sc_.get('iris') or (sc_['focus'][:2] if sc_.get('focus') and abs(sc_['focus'][0] - CX) > W * .13 else None) \
              or ((W * .22, H * .52) if nn % 2 else (W * .78, H * .52))
        ix, iy = float(ip[0]), float(ip[1]); R = int(((max(ix, W - ix)) ** 2 + (max(iy, H - iy)) ** 2) ** .5) + 20
        js.append(f'tl.fromTo("{T}",{{clipPath:"circle(0px at {ix:.0f}px {iy:.0f}px)"}},{{clipPath:"circle({R}px at {ix:.0f}px {iy:.0f}px)",duration:.9,ease:"power2.in",immediateRender:false}},{v0:.3f});')
        js.append(f'tl.set("{T}",{{clipPath:"none"}},{v0 + .91:.3f});')
    elif tr == 'eye':    # opens from a horizontal line like an eye
        js.append(f'tl.fromTo("{T}",{{clipPath:"inset(50% 0% 50% 0%)"}},{{clipPath:"inset(0% 0% 0% 0%)",duration:.8,ease:"power3.inOut",immediateRender:false}},{v0:.3f});')
        js.append(f'tl.set("{T}",{{clipPath:"none"}},{v0 + .81:.3f});')
    elif tr == 'blinds': # bars in muted tones of the scene's own colour family drop over the old picture, then lift off the new one
        acc = scene_tones(u, NB)
        js.append(f'tl.set("{T}",{{opacity:0}},{v0:.3f});tl.set("{T}",{{opacity:1}},{v0 + .62:.3f});')
        for i in range(NB):
            js.append(f'tl.set("#trb{i}",{{background:"{acc[i]}",transformOrigin:"50% 0%"}},{v0:.3f});')
            js.append(f'tl.fromTo("#trb{i}",{{scaleY:0}},{{scaleY:1,duration:.34,ease:"power2.in",immediateRender:false}},{v0 + i * .05:.3f});')
            js.append(f'tl.set("#trb{i}",{{transformOrigin:"50% 100%"}},{v0 + .64:.3f});')
            js.append(f'tl.to("#trb{i}",{{scaleY:0,duration:.34,ease:"power2.out"}},{v0 + .65 + i * .05:.3f});')
    elif tr == 'push':   # vertical push: the old picture leaves upwards (see exit), the new one comes up from below
        js.append(f'tl.fromTo("{T}",{{y:{H}}},{{y:0,duration:.7,ease:"power3.inOut",immediateRender:false}},{v0:.3f});')
    elif tr == 'whip':   # very fast sideways pass with speed streaks
        js.append(f'tl.fromTo("{T}",{{x:{W}}},{{x:0,duration:.45,ease:"expo.out",immediateRender:false}},{v0:.3f});')
        for i in range(9):
            js.append(f'tl.fromTo("#trs{i}",{{x:{W + 80},opacity:.85}},{{x:{-int(W * .75)},opacity:0,duration:.45,ease:"power1.out",immediateRender:false}},{v0 + i * .015:.3f});')
    elif tr == 'tilt':   # the new picture tips in like a card
        js.append(f'tl.fromTo("{T}",{{rotation:-8,scale:1.25,opacity:0,transformOrigin:"50% 120%"}},{{rotation:0,scale:1,opacity:1,duration:.8,ease:"back.out(1.4)",immediateRender:false}},{v0:.3f});')
        js.append(f'tl.set("{T}",{{transformOrigin:"{ORG}"}},{v0 + .81:.3f});')
    # --- exit (depends on how the NEXT unit comes in) ---
    if nxt and nxt['kind'] != 'chalk':
        if nxt['tr'] == 'zoom':
            st = max(t1 - 1.1, t0 + 1.4); js.append(f'tl.to("{T}",{{scale:2.6,duration:{t1 - st:.3f},ease:"power2.in"}},{st:.3f});')
        elif nxt['tr'] == 'slide':
            st = max(t1 - .7, t0 + .8); js.append(f'tl.to("{T}",{{x:{-int(W * .18)},duration:{t1 - st:.3f},ease:"power2.in"}},{st:.3f});')
        elif nxt['tr'] == 'push':
            st = t1 - .7; js.append(f'tl.to("{T}",{{y:{-H},duration:.7,ease:"power3.inOut"}},{st:.3f});')
        elif nxt['tr'] == 'whip':
            st = t1 - .45; js.append(f'tl.to("{T}",{{x:{-W},duration:.45,ease:"expo.out"}},{st:.3f});')
    # --- focus camera (only when the picture has a focus target) ---
    if nn in focus_cam:
        a, (fx, fy, s) = focus_cam[nn]
        cxm = min(max(fx, W / 2 / s), W - W / 2 / s); cym = min(max(fy, H / 2 / s), H - H / 2 / s)
        js.append(f'tl.to("{Wq}",{{scale:{s},x:{W / 2 - cxm * s:.1f},y:{H / 2 - cym * s:.1f},duration:1.4,ease:"power2.inOut"}},{a:.3f});')
        js.append(f'if(document.getElementById("sp{nn}"))tl.fromTo("#sp{nn}",{{opacity:0}},{{opacity:1,duration:1.4,ease:"power2.inOut",immediateRender:false}},{a:.3f});')
    elif DRIFT and u['kind'] != 'chalk':   # --- drift camera: one smooth eased move per picture (push / pan / pull), never a jump ---
        mv = k % 4; d = t1 - v0; s0, s1 = (1.0, 1.06) if mv != 3 else (1.06, 1.0)
        dx = {0: 0, 1: -W * .025, 2: W * .025, 3: 0}[mv]
        js.append(f'tl.fromTo("{Wq}",{{scale:{s0},x:0,y:0,transformOrigin:"{ORG}"}},{{scale:{s1},x:{dx:.1f},y:0,duration:{d:.3f},ease:"sine.inOut",immediateRender:false}},{v0:.3f});')
    if u['kind'] != 'chalk' and is_speed(u, side(u)):   # --- speed streaks: each line accelerates outward (power3.in) and respawns ---
        R = (W * W + H * H) ** .5; d = t1 - v0
        js.append(f'tl.fromTo("#spd{nn}",{{opacity:0}},{{opacity:1,duration:.5,immediateRender:false}},{v0:.3f});')
        for q in range(NSPD):
            per = 0.9 + 0.5 * ((q * 7) % 5) / 4; off = (q * 0.61803) % 1 * per
            rep = max(0, int(math.ceil((d - off) / per)) - 1)
            js.append(f'tl.fromTo("#spd{nn} i:nth-child({q + 1}) b",{{x:{R * .04:.0f},scaleX:.15,opacity:0}},{{x:{R * .62:.0f},scaleX:1.6,opacity:.9,duration:{per:.2f},ease:"power3.in",repeat:{rep},immediateRender:false}},{v0 + off:.3f});')
    # --- motion groups (finite, seek-safe) ---
    p, fb = art_path(u); svg = load_svg(nn, p); cnt = {}
    sp = t1 - v0 + 0.2
    JT = {}; JDEP = {}   # joint / chain groups in document order (outer first): their data-pivot / data-amp / data-per / data-phase
    for mt in re.finditer(r'<g\b[^>]*>', svg):
        cm = re.search(r'class="[^"]*\bmv (mv-(?:chain|joint)-[A-Za-z0-9-]+)', mt.group(0))
        if cm:
            at = dict(re.findall(r'(data-[a-z]+)="([^"]*)"', mt.group(0)))
            base = re.sub(r'-\d+$', '', cm.group(1)); at['_dep'] = JDEP.get(base, 0); JDEP[base] = at['_dep'] + 1   # depth = order of the link in its chain (outer first)
            JT.setdefault(cm.group(1), []).append(at)
    for nm in re.findall(r'class="[^"]*\bmv (mv-[A-Za-z0-9-]+)', svg):
        kind, per = MV.get(nm[3:], MV.get(nm[3:].split('-')[0], ('pulse', .5))); kk = cnt.get(nm, 0); cnt[nm] = kk + 1
        if re.match(r'mv-glint-s\d', nm): kind, per = 'twinkle', {'1': 1.6, '2': 2.1, '3': 2.7}.get(nm[10:11], 2.0)   # cosmic star tiers (3-7)
        g = f'gsap.utils.toArray("#w{nn} .{nm}")[{kk}]'
        if nm == 'mv-glint-core' or nm.startswith('mv-core-'):    # the round centre object: one of 13 motions, never the same twice in a row
            ct = nm[8:].split('-')[0] if nm.startswith('mv-core-') else motions.legacy_core_type(len(CORE_USED))
            js.extend(motions.core_js(ct, g, t0, v0, sp, ring=f'gsap.utils.toArray("#w{nn} .mv-ring")[{kk}]')); CORE_USED.append(ct)
            continue
        if nm.startswith('mv-chain-') or nm.startswith('mv-joint-'):   # creature joints (guideline 20-6): hinge rotation about data-pivot
            at = (JT.get(nm) or [{}])[min(kk, len(JT.get(nm) or [{}]) - 1)]; chain = nm.startswith('mv-chain-')
            pv = at.get('data-pivot', '').replace(',', ' ').split()
            org = f'svgOrigin:"{pv[0]} {pv[1]}"' if len(pv) == 2 else 'transformOrigin:"0% 50%"'
            dep = at.get('_dep', kk) if chain else 0
            amp = float(at.get('data-amp', 7 if chain else 12)) * (1 + 0.35 * dep)   # the tip of a chain bends more
            pj = float(at.get('data-per', 1.5 if chain else 1.1))
            lag = float(at.get('data-phase', 0.55 * dep)) * pj / math.pi             # each link lags its parent -> travelling wave
            st = max(0.0, v0 - lag); rj = int(math.ceil((t1 + 0.2 - st) / pj)) - 1
            js.append(f'tl.fromTo({g},{{rotation:{-amp:.2f},{org}}},{{rotation:{amp:.2f},duration:{pj:.3f},ease:"sine.inOut",yoyo:true,repeat:{rj},immediateRender:false}},{st:.3f});')
            continue
        per = per * (1 + 0.13 * (kk % 3)); rep = int(math.ceil(sp / per)) - 1
        ease = f'ease:"sine.inOut",yoyo:true,repeat:{rep},immediateRender:false'
        if kind == 'pulse': js.append(f'tl.fromTo({g},{{scaleY:1,scaleX:1,transformOrigin:"50% 100%"}},{{scaleY:1.14,scaleX:.92,duration:{per:.3f},{ease}}},{v0:.3f});')
        elif kind == 'drift': js.append(f'tl.fromTo({g},{{y:0,x:0}},{{y:-14,x:6,duration:{per:.3f},{ease}}},{v0:.3f});')
        elif kind == 'breathe': js.append(f'tl.fromTo({g},{{scaleY:1,transformOrigin:"50% 100%"}},{{scaleY:1.03,duration:{per:.3f},{ease}}},{v0:.3f});')
        elif kind == 'nod': js.append(f'tl.fromTo({g},{{rotation:-3,transformOrigin:"50% 100%"}},{{rotation:3,duration:{per:.3f},{ease}}},{v0:.3f});')
        elif kind == 'lean': js.append(f'tl.fromTo({g},{{rotation:-2,transformOrigin:"50% 100%"}},{{rotation:2,duration:{per:.3f},{ease}}},{v0:.3f});')
        elif kind == 'arm':     # gentle swing around the shoulder (pivot from pivots.py, in SVG units)
            pv = PIV.get(p, {}).get(nm)
            org = f'transformOrigin:"{pv[0]:.1f}px {pv[1]:.1f}px"' if pv else 'transformOrigin:"50% 0%"'
            js.append(f'tl.fromTo({g},{{rotation:-7,{org}}},{{rotation:7,duration:{per:.3f},{ease}}},{v0:.3f});')
        elif kind == 'hand':    # small turn around the hand's own centre, no lift, so it stays on the wrist
            js.append(f'tl.fromTo({g},{{rotation:-5,transformOrigin:"50% 50%"}},{{rotation:5,duration:{per:.3f},{ease}}},{v0:.3f});')
        elif kind == 'walk':
            pb = 0.5; rb = int(math.ceil(sp / pb)) - 1
            js.append(f'tl.fromTo({g},{{x:-60}},{{x:60,duration:{per:.3f},{ease}}},{v0:.3f});')
            js.append(f'tl.fromTo({g},{{y:0}},{{y:-9,duration:{pb},ease:"sine.inOut",yoyo:true,repeat:{rb},immediateRender:false}},{v0:.3f});')
        elif kind == 'twinkle': js.append(f'tl.fromTo({g},{{opacity:1}},{{opacity:.35,duration:{per:.3f},{ease}}},{v0:.3f});')
        elif kind == 'nebula': js.append(f'tl.fromTo({g},{{x:-25}},{{x:25,duration:{per:.3f},{ease}}},{v0:.3f});')
        elif kind == 'glow': js.append(f'tl.fromTo({g},{{scale:1,opacity:.85,transformOrigin:"50% 50%"}},{{scale:1.06,opacity:1,duration:{per:.3f},{ease}}},{v0:.3f});')
        elif kind == 'orbit':   # one-way turn around the group's centre (the group holds an invisible full orbit circle so its centre is the orbit centre)
            js.append(f'tl.fromTo({g},{{rotation:0,transformOrigin:"50% 50%"}},{{rotation:{360 * sp / per:.1f},duration:{sp:.3f},ease:"none",immediateRender:false}},{v0:.3f});')
        elif kind == 'sway': js.append(f'tl.fromTo({g},{{rotation:-7,transformOrigin:"50% 100%"}},{{rotation:7,duration:{per:.3f},{ease}}},{v0:.3f});')
        else: js.append(f'tl.fromTo({g},{{rotation:-5,transformOrigin:"50% 0%"}},{{rotation:5,duration:{per:.3f},{ease}}},{v0:.3f});')
if CORE_USED:
    from collections import Counter
    cc = Counter(CORE_USED); rep_pairs = sum(1 for a, b in zip(CORE_USED, CORE_USED[1:]) if a == b)
    print('centre motions:', dict(cc), '| distinct', len(cc), '| same type twice in a row:', rep_pairs)
    if len(cc) < min(10, len(CORE_USED)): print('WARNING: fewer than 10 centre-motion types used (guideline 4-1)')
    if rep_pairs: print('WARNING: the same centre motion appears in consecutive pictures')
    if max(cc.values()) > .2 * len(CORE_USED) + 1: print('WARNING: one centre motion is over 20% of the pictures')
for (nn, ty, lid, gid, tt) in label_t:          # on-screen text pops in when its words are spoken (guideline 3-6)
    if ty == 'num':
        js.append(f'tl.fromTo("#{lid}",{{opacity:0,x:-30}},{{opacity:1,x:0,duration:.3,ease:"power2.out",immediateRender:false}},{tt:.3f});')
        js.append(labels_lib.count_js(lid, tt))      # the number counts up from 0 as the badge comes in (guideline 3-6)
        continue
    js.append(f'tl.fromTo("#{lid}s",{{opacity:0,scale:.6}},{{opacity:1,scale:1,duration:.25,ease:"back.out(2)",immediateRender:false}},{tt:.3f});')
    if gid: js.append(f'tl.set("#{gid}",{{opacity:1}},{tt:.3f});')
    if nn in focus_cam:       # keep the text the same size while the camera zooms in (it still follows its subject)
        a, (fx, fy, s) = focus_cam[nn]
        js.append(f'tl.fromTo("#{lid}",{{scale:1,transformOrigin:"0px 0px"}},{{scale:{1 / s:.4f},duration:1.4,ease:"power2.inOut",immediateRender:false}},{a:.3f});')
for k, c in enumerate(caps):
    js.append(f'tl.set("#c{k}",{{opacity:1}},{c["t0"]:.3f});tl.set("#c{k}",{{opacity:0}},{c["t1"]:.3f});')
    js.append(caption_hl.highlight_js(k, c['text'], c['t0'], c['sp1']))   # spoken word turns yellow (guideline 5)
js.append('window.__timelines=window.__timelines||{};window.__timelines["main"]=tl;</script>')
h.append('\n'.join(js)); h.append('</div></body></html>')
open(f'{OUT}/index.html', 'w', encoding='utf-8').write('\n'.join(h))

for f in os.listdir(OUT):          # drop sfx files that no cue uses (keep the repo small)
    if f.startswith('sfx_') and f not in SFXLEN and os.path.exists(f'{OUT}/{f}'): os.remove(f'{OUT}/{f}')
data = dict(slug=SLUG, total=TOTAL, lead=LEAD, gap=GAP, tail=TAIL, starts={str(k): v for k, v in starts.items()}, D={str(i): D[i - 1] for i in SEL},
            cuts=[dict(id=u['uid'], scene=u['scene'], kind=u['kind'], t0=u['t0'], t1=u['t1'], tr=u['tr'], text=u['text']) for u in units],
            caps=caps, sfx=cues, chalk=chalk_t, snap=snap_report, chalk_pop={str(k): v.get('pop') for k, v in CHALK.items() if 'pop' in v})
json.dump(data, open(B + ('/build_data.json' if len(SEL) == len(SCENES) else '/build_data_partial.json'), 'w'), ensure_ascii=False, indent=1)
dd = [u['t1'] - u['t0'] for u in units]
from collections import Counter
print('labels', len(label_t), 'total', TOTAL, 'units', len(units), 'avg', round(sum(dd) / len(dd), 2), 'max', round(max(dd), 2), 'caps', len(caps), 'sfx cues', len(cues), 'fallback art', len(fallback_used))
print('transitions', dict(Counter(u['tr'] for u in units)), 'focus cams', len(focus_cam))
