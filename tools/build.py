# -*- coding: utf-8 -*-
# Build the HyperFrames composition for "never-eat-human-meat".
# usage: python3 build.py [OUTDIR] ; env SEL="1,2,16" builds a partial test.
import os, re, sys, json, html, shutil, subprocess, math, random
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from paths import *
SCENES = load_scenes()
B = wdir() + '/build'
OUT = sys.argv[1] if len(sys.argv) > 1 else f'{REPO}/render/{SLUG}'
os.makedirs(OUT, exist_ok=True)
SEL = [int(x) for x in os.environ.get('SEL', '').split(',') if x] or list(range(1, len(SCENES) + 1))
LEAD, GAP, TAIL = 1.0, 0.8, 2.5
MOTES = 14
timing = json.load(open(B + '/timing_base.json'))
D = timing['D']


def run(*a):
    return subprocess.run(a, capture_output=True, text=True)


def dur(f):
    return float(run('ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', f).stdout)


# ---------- assets ----------
for name in ['gsap.min.js', 'Fredoka-700.woff2', 'PatrickHand-400.woff2', 'logo.png', 'grain.png', 'whoosh.wav']:
    shutil.copy(f'{ASSETS}/{name}', f'{OUT}/{name}')

# chalk sound (synthesized, no external source)
import numpy as np, wave
def make_chalk(path):
    sr = 48000; n = int(0.38 * sr); rng = np.random.default_rng(7)
    x = rng.standard_normal(n)
    # crude band-pass by differencing + smoothing
    x = np.diff(x, prepend=0)
    k = np.ones(3) / 3; x = np.convolve(x, k, 'same')
    t = np.arange(n) / sr
    env = np.minimum(t / 0.01, 1) * np.exp(-t * 9) * (0.6 + 0.4 * np.sin(2 * np.pi * 38 * t) ** 2)
    x = x * env; x = x / np.max(np.abs(x)) * 10 ** (-22 / 20)
    st = np.stack([x, x], 1)
    with wave.open(path, 'wb') as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(sr)
        w.writeframes((st * 32767).astype('<i2').tobytes())
make_chalk(f'{OUT}/chalk.wav')

# compress audio for the repo (AAC 192k); amb gets short fades so tiling has no clicks
for f in ('whoosh', 'chalk'):
    pass
run('ffmpeg', '-y', '-v', 'error', '-i', ASSETS + '/amb_src.m4a', '-af', 'afade=t=in:d=0.4,afade=t=out:st=59.6:d=0.4',
    '-c:a', 'aac', '-b:a', '192k', f'{OUT}/amb.m4a')

# ---------- timeline ----------
starts = {}; t = LEAD
for i in SEL:
    starts[i] = t; t += D[i - 1] + GAP
last = SEL[-1]
TOTAL = starts[last] + D[last - 1] + TAIL
TOTAL = round(TOTAL, 3)

# per-scene sentence boundaries and timing model
def sentences(text):
    return re.split(r'(?<=[.?!])\s+', text.strip())

def pauses(i):
    r = run('ffmpeg', '-nostats', '-i', f'{B}/s{i:02d}.wav', '-af', 'silencedetect=noise=-35dB:d=0.12', '-f', 'null', '-')
    s = [float(x) for x in re.findall(r'silence_start: ([\d.]+)', r.stderr)]
    e = [float(x) for x in re.findall(r'silence_end: ([\d.]+)', r.stderr)]
    d = D[i - 1]
    return [((a + b) / 2, b - a) for a, b in zip(s, e) if a > 0.2 and b < d - 0.2]

snap_report = {}
model = {}   # i -> dict(sents=[(text, a, b)], D)
for i in SEL:
    text = SCENES[i - 1][4]
    ss = sentences(text); d = D[i - 1]
    ch = [len(x) + 1 for x in ss]; tot = sum(ch)
    ps = pauses(i)
    prop = [0.0]; c = 0
    for x in ch[:-1]:
        c += x; prop.append(d * c / tot)
    prop.append(d)
    k = len(ss) - 1
    # take the k longest pauses; accept only if each lies within 1.2 s of the proportional estimate
    cand = sorted(sorted(ps, key=lambda p: -p[1])[:k]) if k > 0 else []
    ok = len(cand) == k and all(abs(cand[j][0] - prop[j + 1]) <= 1.2 for j in range(k)) and all(cand[j][0] < cand[j + 1][0] for j in range(k - 1))
    if ok:
        bounds = [0.0] + [p[0] for p in cand] + [d]; snap_report[i] = 'snap'
    else:
        bounds = prop; snap_report[i] = f'prop(pauses={len(ps)},sents={len(ss)})'
    model[i] = [(ss[k], bounds[k], bounds[k + 1]) for k in range(len(ss))]

def tchar(i, idx):
    """time (scene-relative) of character index idx in narration, proportional within its sentence"""
    text = SCENES[i - 1][4]; pos = 0
    for (s, a, b) in model[i]:
        j = text.find(s, pos)
        if j <= idx < j + len(s) + 1 or s is model[i][-1][0]:
            return a + (b - a) * min(max((idx - j) / max(len(s), 1), 0), 1)
        pos = j + len(s)
    return D[i - 1]

# ---------- caption lines ----------
def split_lines(sent):
    words = sent.split(); lines = []; cur = []
    def clen(ws): return len(' '.join(ws))
    for w in words:
        cur.append(w)
        if clen(cur) >= 30 or len(cur) >= 7:
            lines.append(cur); cur = []
        elif len(cur) >= 4 and re.search(r'[,;:]$', w):
            lines.append(cur); cur = []
    if cur:
        if lines and (len(cur) < 3 or clen(cur) < 12) and clen(lines[-1]) + 1 + clen(cur) <= 46 and len(lines[-1]) + len(cur) <= 9:
            lines[-1] += cur
        else:
            lines.append(cur)
    return [' '.join(l) for l in lines]

caps = []   # dict(text, t0, t1) absolute
for i in SEL:
    s0 = starts[i]; scene_caps = []
    for (s, a, b) in model[i]:
        ls = split_lines(s); ch = [len(x) + 1 for x in ls]; tot = sum(ch); c = 0
        for k, ltxt in enumerate(ls):
            scene_caps.append([ltxt, s0 + a + (b - a) * c / tot])
            c += ch[k]
    for k, cp in enumerate(scene_caps):
        end = scene_caps[k + 1][1] if k + 1 < len(scene_caps) else s0 + D[i - 1] + 0.25
        caps.append({'text': cp[0], 't0': cp[1], 't1': end, 'scene': i})
# validation
prev = -1
for c in caps:
    assert c['t0'] < c['t1'] - 0.3, ('short/reversed caption', c)
    assert c['t0'] >= prev, ('non-monotonic', c)
    prev = c['t0']
assert max(len(c['text']) for c in caps) <= 46, max(caps, key=lambda c: len(c['text']))

# ---------- SVG inlining ----------
def load_svg(i, art):
    s = open(f'{vdir()}/art/{art}.svg', encoding='utf-8').read()
    s = re.sub(r'<\?xml[^>]*\?>', '', s).strip()
    pre = f'p{i}_'
    ids = set(re.findall(r'\bid="([^"]+)"', s))
    def mv(m):
        tag = m.group(0)
        name = re.search(r'\bid="(mv-[^"]+)"', tag).group(1)
        tag = re.sub(r'\s*\bid="mv-[^"]+"', '', tag)
        if re.search(r'\bclass="', tag):
            tag = re.sub(r'\bclass="([^"]*)"', lambda mm: f'class="{mm.group(1)} mv {name}"', tag, 1)
        else:
            tag = tag[:-1].rstrip('/') + f' class="mv {name}"' + ('/>' if tag.endswith('/>') else '>')
        return tag
    s = re.sub(r'<[a-zA-Z][^>]*\bid="mv-[^"]+"[^>]*>', mv, s)
    ids = {x for x in ids if not x.startswith('mv-')}
    for x in ids:
        s = s.replace(f'id="{x}"', f'id="{pre}{x}"').replace(f'url(#{x})', f'url(#{pre}{x})')
        s = s.replace(f'href="#{x}"', f'href="#{pre}{x}"')
    s = re.sub(r'\swidth="1920"\s+height="1080"', '', s, count=1)
    return s

# ---------- chalkboard ----------
CHALK = load_config().CHALK
ROW_Y = [294, 459, 630]
chalk_events = {}   # i -> list of abs times of chalk sounds

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

# ---------- cuts ----------
# Several cuts per illustrated scene (same SVG, different framing); transitions only between illustrated scenes.
TARGET_CUT, MIN_CUT = 6.5, 3.2
WH = load_config().WHOOSH
scene_caps = {}
for cp in caps: scene_caps.setdefault(cp['scene'], []).append(cp['t0'])
cuts = []
for idx, i in enumerate(SEL):
    kind = SCENES[i - 1][2]
    s0 = 0.0 if i == SEL[0] else starts[i]
    s1 = starts[SEL[idx + 1]] if idx + 1 < len(SEL) else TOTAL
    if kind == 'chalk':
        cuts.append(dict(scene=i, kind='chalk', part=0, first=True, t0=s0, t1=s1)); continue
    L = s1 - s0; n = max(1, round(L / TARGET_CUT))
    cand = [t for t in scene_caps[i][1:] if s0 + MIN_CUT <= t <= s1 - MIN_CUT]
    bounds = []
    for k in range(1, n):
        ideal = s0 + L * k / n
        opts = [t for t in cand if not bounds or t >= bounds[-1] + MIN_CUT]
        if not opts: break
        bounds.append(min(opts, key=lambda t: abs(t - ideal)))
    pts = [s0] + bounds + [s1]
    for j in range(len(pts) - 1):
        cuts.append(dict(scene=i, kind='ill', part=j, first=(j == 0), t0=pts[j], t1=pts[j + 1]))
for n, c in enumerate(cuts, 1):
    c['id'] = f'C{n:03d}'
# transitions into each illustrated scene (chalk boards and the first scene stay hard cuts, as before)
TR = {}; kind_of = {i: SCENES[i - 1][2] for i in SEL}; mix = ['fade', 'hard', 'wipel', 'fade', 'wipeu', 'hard']; mk = int(os.environ.get('MIX0', '0'))
for idx, i in enumerate(SEL):
    if idx == 0 or kind_of[i] == 'chalk' or kind_of[SEL[idx - 1]] == 'chalk':
        TR[i] = ('hard', 0.0); continue
    if i in WH:
        TR[i] = ('iris', 0.6)
    else:
        ty = mix[mk % len(mix)]; mk += 1
        TR[i] = (ty, 0.0 if ty == 'hard' else 0.45)
for c in cuts:
    c['vis0'] = c['t0'] - (TR[c['scene']][1] if c['first'] else 0.0)
    c['tr'] = TR[c['scene']][0] if c['first'] else 'cut'

# ---------- html ----------
h = []
h.append('<!doctype html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=1920, height=1080">')
h.append('<script src="gsap.min.js"></script><style>')
h.append('''@font-face{font-family:Fredoka;src:url(Fredoka-700.woff2) format("woff2");font-weight:700}
@font-face{font-family:Patrick;src:url(PatrickHand-400.woff2) format("woff2");font-weight:400}
*{margin:0;padding:0;box-sizing:border-box}html,body{width:1920px;height:1080px;overflow:hidden;background:#000}
#root{position:relative;width:1920px;height:1080px;overflow:hidden}
.w{position:absolute;left:0;top:0;width:1920px;height:1080px;display:none;will-change:transform}
.w svg{position:absolute;left:0;top:0;width:1920px;height:1080px}
.motes{position:absolute;left:0;top:0;width:1920px;height:1080px;pointer-events:none}.motes i{position:absolute;display:block;border-radius:50%;background:#fff6dc}
.cap{position:absolute;left:0;width:1920px;bottom:60px;display:flex;justify-content:center;opacity:0;z-index:1002}
.cap span{font-family:Fredoka,sans-serif;font-weight:700;font-size:58px;line-height:54px;color:#fff;background:rgba(0,0,0,.62);border-radius:12px;padding:20px;white-space:nowrap}
#logo{position:absolute;left:1799px;top:40px;width:81px;height:81px;z-index:1003}
#grain{position:absolute;left:0;top:0;width:1920px;height:1080px;z-index:1001;opacity:.35;pointer-events:none}
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
''')
h.append('</style></head><body>')
h.append(f'<div id="root" data-composition-id="main" data-start="0" data-duration="{TOTAL}" data-width="1920" data-height="1080">')
for i in SEL:
    kind = SCENES[i - 1][2]
    if kind == 'chalk':
        h.append(f'<div class="w" id="w{i}" style="display:none;z-index:{i}">{chalk_html(i)}</div>')
    else:
        rr = random.Random(i * 7919); mo = []
        for m in range(MOTES):
            mo.append(f'<i style="left:{rr.randint(40, 1880)}px;top:{rr.randint(160, 1000)}px;width:{(sz := rr.randint(5, 10))}px;height:{sz}px;opacity:{rr.choice([.28, .36, .44, .5])}"></i>')
        h.append(f'<div class="w" id="w{i}" style="z-index:{i}">{load_svg(i, SCENES[i - 1][3])}<div class="motes">{"".join(mo)}</div></div>')
h.append('<img id="grain" src="grain.png"><img id="logo" src="logo.png">')
for n, c in enumerate(caps):
    h.append(f'<div class="cap" id="c{n}"><span>{html.escape(c["text"], quote=False)}</span></div>')

# audio
audio = []   # (src, start, dur, track, vol)
for i in SEL:
    run('ffmpeg', '-y', '-v', 'error', '-i', f'{B}/n{i:02d}.wav', '-c:a', 'aac', '-b:a', '192k', f'{OUT}/n{i:02d}.m4a')
    audio.append((f'n{i:02d}.m4a', starts[i], dur(f'{OUT}/n{i:02d}.m4a'), 0, 1))
whoosh_t = []
for i in WH:
    if i in starts:
        wt = starts[i] - (TR[i][1] if TR[i][0] == 'iris' else 0.0)
        wt = max(wt, 0.0)
        whoosh_t.append(wt); audio.append(('whoosh.wav', wt, 1.2, 2, 1))
# ambient everywhere except chalk scenes
amb_ranges = []; cur = 0.0
for c in cuts:
    if c['kind'] == 'chalk':
        if c['t0'] > cur: amb_ranges.append((cur, c['t0']))
        cur = c['t1']
if TOTAL > cur: amb_ranges.append((cur, TOTAL))
for (a, b) in amb_ranges:
    t0 = a
    while t0 < b - 0.05:
        dd = min(60.0, b - t0); audio.append(('amb.m4a', t0, round(dd, 3), 1, 1)); t0 += dd
# chalk sounds
chalk_t = []
for i in SEL:
    if i in CHALK:
        s0 = starts[i]; c = CHALK[i]
        ts = [s0 + 0.05]
        text = SCENES[i - 1][4]
        for r in (1, 2):
            key = c['rows'][r][4]; idx = text.find(key); assert idx >= 0, key
            ts.append(s0 + tchar(i, idx))
        key = c['concl'][1]; idx = text.find(key); assert idx >= 0, key
        ts.append(s0 + tchar(i, idx))
        CHALK[i]['pop'] = ts
        for tt in ts:
            chalk_t.append(tt); audio.append(('chalk.wav', tt, 0.38, 3, 1))
for (src, st, dd, tr, vol) in audio:
    h.append(f'<audio src="{src}" data-start="{st:.3f}" data-duration="{dd:.3f}" data-track-index="{tr}" data-volume="{vol}"></audio>')

# timeline script
js = ['<script>const tl=gsap.timeline({paused:true});']
FOC = ['32% 62%', '68% 56%', '50% 44%', '62% 70%', '38% 46%', '72% 40%']
# framings for the 2nd, 3rd... cut of a scene: (scale from, scale to, origin, x from, x to, y from, y to)
def view(i, j):
    if j == 0:
        d = -20 if i % 2 == 0 else 20
        return (1.06, 1.12, '50% 50%', -d, d, 0, 0)
    f = lambda k: FOC[(i * 2 + j + k) % len(FOC)]
    sg = 1 if (i + j) % 2 == 0 else -1
    cyc = [(1.30, 1.40, f(0), 0, 0, 0, 0), (1.20, 1.20, '50% 50%', 60 * sg, -60 * sg, 0, 0),
           (1.50, 1.38, f(2), 0, 0, 0, 0), (1.14, 1.26, f(4), 0, 0, 0, 0),
           (1.22, 1.22, '50% 50%', 0, 0, -40 * sg, 40 * sg)]
    return cyc[(i + j) % len(cyc)]
TRSET = {'fade': ('{opacity:0}', '{opacity:1}'),
         'wipel': ('{clipPath:"inset(0% 0% 0% 100%)"}', '{clipPath:"inset(0% 0% 0% 0%)"}'),
         'wipeu': ('{clipPath:"inset(100% 0% 0% 0%)"}', '{clipPath:"inset(0% 0% 0% 0%)"}'),
         'iris': ('{clipPath:"circle(0% at 50% 50%)"}', '{clipPath:"circle(75% at 50% 50%)"}')}
for n, c in enumerate(cuts):
    i = c['scene']; w = f'#w{i}'; t0 = c['t0']; t1 = c['t1']; v0 = c['vis0']
    js.append(f'tl.set("{w}",{{display:"block"}},{v0:.3f});tl.set("{w}",{{display:"none"}},{t1:.3f});')
    if c['kind'] == 'ill':
        s_a, s_b, org, xa, xb, ya, yb = view(i, c['part'])
        js.append(f'tl.fromTo("{w}",{{scale:{s_a},x:{xa},y:{ya},transformOrigin:"{org}"}},{{scale:{s_b},x:{xb},y:{yb},duration:{t1 - v0:.3f},ease:"none",immediateRender:false}},{v0:.3f});')
        if c['tr'] in TRSET:
            a0, a1 = TRSET[c['tr']]; T = t0 - v0
            js.append(f'tl.fromTo("{w}",{a0},Object.assign({a1},{{duration:{T:.3f},ease:"power1.inOut",immediateRender:false}}),{v0:.3f});')
            js.append(f'tl.set("{w}",{{clipPath:"none",opacity:1}},{t0 + .001:.3f});')
    else:
        js.append(f'tl.set("#k{i}",{{display:"block"}},{t0:.3f});tl.set("#k{i}",{{display:"none"}},{t1:.3f});')
        ts = CHALK[i]['pop']
        js.append(f'tl.set("#k{i}r0",{{opacity:1}},{t0:.3f});tl.set("#k{i}ph0",{{opacity:0}},{t0:.3f});')
        for r, tt in ((1, ts[1]), (2, ts[2])):
            js.append(f'tl.set("#k{i}ph{r}",{{opacity:0}},{tt:.3f});tl.fromTo("#k{i}r{r}",{{opacity:1,scale:.96}},{{scale:1.02,duration:.05,ease:"power1.out",immediateRender:false}},{tt:.3f});tl.to("#k{i}r{r}",{{scale:1,duration:.05,ease:"power1.in"}},{tt + .05:.3f});')
        js.append(f'tl.fromTo("#k{i}cc",{{opacity:1,scale:.96}},{{scale:1.02,duration:.05,immediateRender:false}},{ts[3]:.3f});tl.to("#k{i}cc",{{scale:1,duration:.05}},{ts[3] + .05:.3f});')
        # rows 1,2 hidden before their pop: set opacity 0 at cut start (reset when seeking back)
        js.append(f'tl.set("#k{i}r1",{{opacity:0}},{t0:.3f});tl.set("#k{i}r2",{{opacity:0}},{t0:.3f});tl.set("#k{i}cc",{{opacity:0}},{t0:.3f});tl.set("#k{i}ph1",{{opacity:1}},{t0:.3f});tl.set("#k{i}ph2",{{opacity:1}},{t0:.3f});')
# mv animations (once per scene, for the whole scene span)
MV = {'flame': ('pulse', .30), 'lamp': ('pulse', .5), 'lantern': ('pulse', .55), 'beacon': ('pulse', .7), 'glint': ('pulse', .6),
      'spark': ('pulse', .25), 'smoke': ('drift', 1.6), 'steam': ('drift', 1.3), 'stink': ('drift', 1.1), 'cells': ('drift', 1.8),
      'antenna': ('sway', .35), 'rain': ('drift', .9), 'bell': ('swing', .8), 'knot': ('swing', 1.2), 'key': ('drift', .8)}
for i in SEL:
    if SCENES[i - 1][2] == 'chalk': continue
    s0 = starts[i]; s1 = starts[SEL[SEL.index(i) + 1]] if SEL.index(i) + 1 < len(SEL) else TOTAL
    # gentle float of the whole drawing + drifting dust motes (finite repeats, seek-safe)
    sp = s1 - s0 + 0.8; per = 7.0; rep = int(math.ceil(sp / per)) - 1
    js.append(f'tl.fromTo("#w{i} > svg",{{x:-12,y:-7}},{{x:12,y:7,duration:{per},ease:"sine.inOut",yoyo:true,repeat:{rep},immediateRender:false}},{max(s0 - 0.8, 0):.3f});')
    rr = random.Random(i * 31 + 5)
    for m in range(MOTES):
        pm = rr.uniform(4, 8); rm = int(math.ceil(sp / pm)) - 1; dy = -rr.randint(70, 170); dx = rr.randint(-30, 30)
        js.append(f'tl.fromTo(gsap.utils.toArray("#w{i} .motes i")[{m}],{{x:0,y:0}},{{x:{dx},y:{dy},duration:{pm:.2f},ease:"sine.inOut",yoyo:true,repeat:{rm},immediateRender:false}},{max(s0 - 0.8, 0):.3f});')
    svg = load_svg(i, SCENES[i - 1][3])
    names = re.findall(r'class="[^"]*\bmv (mv-[a-z]+)', svg)
    cnt = {}
    for nm in names:
        kind, per = MV.get(nm[3:], ('pulse', .5)); k = cnt.get(nm, 0); cnt[nm] = k + 1
        sel = f'#w{i} .{nm}'
        # one tween per matched element index
        per = per * (1 + 0.13 * (k % 3)); rep = int(math.ceil((s1 - s0) / per)) - 1
        if kind == 'pulse':
            js.append(f'tl.fromTo(gsap.utils.toArray("{sel}")[{k}],{{scaleY:1,scaleX:1,transformOrigin:"50% 100%"}},{{scaleY:1.14,scaleX:.92,duration:{per:.3f},ease:"sine.inOut",yoyo:true,repeat:{rep},immediateRender:false}},{s0:.3f});')
        elif kind == 'drift':
            js.append(f'tl.fromTo(gsap.utils.toArray("{sel}")[{k}],{{y:0,x:0}},{{y:-14,x:6,duration:{per:.3f},ease:"sine.inOut",yoyo:true,repeat:{rep},immediateRender:false}},{s0:.3f});')
        elif kind == 'sway':
            js.append(f'tl.fromTo(gsap.utils.toArray("{sel}")[{k}],{{rotation:-7,transformOrigin:"50% 100%"}},{{rotation:7,duration:{per:.3f},ease:"sine.inOut",yoyo:true,repeat:{rep},immediateRender:false}},{s0:.3f});')
        else:
            js.append(f'tl.fromTo(gsap.utils.toArray("{sel}")[{k}],{{rotation:-5,transformOrigin:"50% 0%"}},{{rotation:5,duration:{per:.3f},ease:"sine.inOut",yoyo:true,repeat:{rep},immediateRender:false}},{s0:.3f});')
for n, c in enumerate(caps):
    js.append(f'tl.set("#c{n}",{{opacity:1}},{c["t0"]:.3f});tl.set("#c{n}",{{opacity:0}},{c["t1"]:.3f});')
js.append('window.__timelines=window.__timelines||{};window.__timelines["main"]=tl;</script>')
h.append('\n'.join(js)); h.append('</div></body></html>')
open(f'{OUT}/index.html', 'w', encoding='utf-8').write('\n'.join(h))

# data for the deliverable text files
data = dict(slug=SLUG, total=TOTAL, lead=LEAD, gap=GAP, starts={str(k): v for k, v in starts.items()},
            D={str(i): D[i - 1] for i in SEL}, cuts=cuts, caps=caps, whoosh=whoosh_t, chalk=chalk_t,
            amb=amb_ranges, snap=snap_report, chalk_pop={str(k): v.get('pop') for k, v in CHALK.items() if 'pop' in v})
json.dump(data, open(B + ('/build_data.json' if len(SEL) == len(SCENES) else '/build_data_partial.json'), 'w'), ensure_ascii=False, indent=1)
print('total', TOTAL, 'cuts', len(cuts), 'caps', len(caps), 'mv', 'snap', sum(1 for v in snap_report.values() if v == 'snap'), '/', len(snap_report))
print('avg cut', round(sum(c['t1'] - c['t0'] for c in cuts) / len(cuts), 1), 'max line', max(len(c['text']) for c in caps))
