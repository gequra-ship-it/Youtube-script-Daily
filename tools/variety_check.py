# usage: python3 tools/variety_check.py <slug> [<slug>..] [--report]
# 2026-10-31 (miya: "항상 비슷한 것만 나와", guideline 7-2 J / 4-9): the VARIETY GATE. Counts, per video, what the sidecars and pictures will put on screen:
#   frog acts / outfits / moods (videos/<slug>/art3/U*.json 'frog'), object motion kinds (group ids mv-<kind>-.. / mv-core-<kind>-.., background kinds not counted),
#   and the moving small props the contact gags need (drop / topple / rollby / bouncing / swing / rise / popin / drip / slam / hop / magnet / unroll / pendulum / toss / coast).
# Thresholds (long-form; shorts are judged on frog acts only): top frog act <= 40 % of frog units, distinct acts >= 8 when >= 20 frogs (>= 5 when >= 10), distinct outfits >= 4,
# distinct object kinds >= 8 (>= 4 when < 20 units), moving props >= units / 6. Exit 1 when a line fails (final_check runs it); --report only prints.
import sys, os, re, json, glob, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from paths import REPO
BG = {'glint', 'drift', 'scroll', 'fade', 'rack', 'blink', 'breathe', 'cells', 'twinkle', 'tint', 'frog', 'chain', 'joint', 'core', 'emph', 'fill', 'neon', 'sparkle', 'settle'}
PROPS = {'core-drop', 'topple', 'rollby', 'bouncing', 'swing', 'rise', 'popin', 'drip', 'slam', 'hop', 'magnet', 'unroll', 'pendulum', 'toss', 'coast', 'bob', 'nudge', 'hatch', 'lift', 'teeter', 'scatter', 'converge', 'zigzag'}   # 2026-11-05: + the 4-13 kinds
PULSE = {'heartbeat', 'swell', 'tremble', 'wobble', 'ping', 'squeeze', 'pop', 'stamp'}   # 2026-11-05 (miya): event centre motions — capped by corefix (15 %, min 3), never ridden by the frog
GID = re.compile(r'id="mv-([a-z]+)(?:-([a-z]+))?[^"]*"')

def stats(slug):
    units = 0; frogs = 0; A = collections.Counter(); O = collections.Counter(); M = collections.Counter(); K = collections.Counter(); props = 0; C = collections.Counter(); pulse_rides = []
    for svg in sorted(glob.glob(f'{REPO}/videos/{slug}/art3/U*.svg')):
        units += 1; txt = open(svg, encoding='utf-8').read(); kinds = set(); has_prop = False
        for a, b in GID.findall(txt):
            kd = 'core-' + (b or '') if a == 'core' else a
            if a in BG and a != 'core': continue
            if a == 'core' and b in ('drop',): has_prop = True
            if kd in PROPS: has_prop = True
            if a != 'core' or b == 'drop': kinds.add(kd)
            if a == 'core' and b: C[b] += 1
        for k in kinds: K[k] += 1
        props += has_prop
        fn = svg[:-4] + '.json'
        fr = json.load(open(fn)).get('frog') if os.path.exists(fn) else None
        if fr and not fr.get('hide'):
            frogs += 1; a = fr.get('act'); a = a.get('type') if isinstance(a, dict) else a
            if fr.get('ride') and re.match(r'mv-core-(' + '|'.join(PULSE) + r')\b', str(fr['ride'])): pulse_rides.append(os.path.basename(svg)[:-4])
            A[a or 'roam:' + (fr.get('roam') or {}).get('kind', '-')] += 1; O['+'.join(fr.get('outfit') or ['-'])] += 1; M[(fr.get('moods') or [{}])[0].get('mood', '-')] += 1
    return dict(units=units, frogs=frogs, acts=A, outfits=O, moods=M, kinds=K, props=props, cores=C, pulse_rides=pulse_rides)

def judge(slug, s):
    vert = 'short' in slug; L = []; ok = True
    def line(name, good, detail):
        nonlocal ok; ok &= good; L.append(f"  {'ok ' if good else 'LOW'} {name}: {detail}")
    f = s['frogs']
    if f:
        top = s['acts'].most_common(1)[0]
        line('top frog act', top[1] <= max(2, .4 * f), f"{top[0]} {top[1]}/{f}")
        need = 8 if f >= 20 else 5 if f >= 10 else 2
        line('distinct frog acts', len(s['acts']) >= need, f"{len(s['acts'])} (need {need})")
        line('distinct outfits', len(s['outfits']) >= (4 if f >= 10 else 2), f"{len(s['outfits'])}" + ('' if len(s['outfits']) >= 4 else ' (an all-underwater video: diver + sea-pack extras count)'))
        line('distinct first moods', len(s['moods']) >= (4 if f >= 10 else 2), f"{len(s['moods'])}")
    if not vert:
        u = s['units']; needk = 8 if u >= 20 else 4
        line('distinct object motion kinds', len(s['kinds']) >= needk, f"{len(s['kinds'])} (need {needk}): " + ' '.join(f'{k}:{c}' for k, c in s['kinds'].most_common(12)))
        warn = s['props'] < u / 6   # a WARNING, not a failure: old videos drew no props; new art must meet it (art_spec 12 quota), the main session reads this line before the render
        cap = max(3, int(.15 * u)); over = [(k, c) for k, c in s['cores'].items() if k in PULSE and c > cap]   # 2026-11-05 (miya: "두근거림이 너무 자주"): event centre motions by word / name only, each <= 15 %
        if s['cores']: line('centre motion share', not over, ' '.join(f'{k}:{c}' for k, c in s['cores'].most_common(10)) + (f'  (over {cap}: ' + ' '.join(f'{k}:{c}' for k, c in over) + ' -> run tools/corefix.py)' if over else ''))
        _ix = f'{REPO}/render/{slug}/index.html'   # 2026-11-05 (miya 4:03): fast throbbing (scaleY 1.14 every 0.5 s) must stay rare: <= 10 % of the units, never a whole stretch
        if os.path.exists(_ix):
            _t = open(_ix, encoding='utf-8').read(); _n = len(re.findall(r'scaleY:1\.14,scaleX:\.92', _t)); _cap = max(2, int(.10 * u))
            line('fast throb tweens', _n <= _cap, f'{_n} (cap {_cap}: only flame/spark names or a sentence word; an unknown mv- name now glows calmly)')
        line('frog rides a pulsing centre object', not s['pulse_rides'], 'none' if not s['pulse_rides'] else ' '.join(s['pulse_rides']) + ' (rerun frog_place.py: the frog must stand beside and respond, 7-2 L)')
        L.append(f"  {'WARN' if warn else 'ok '} units with a moving small prop: {s['props']}/{u} (want >= {u // 6}; contact gags need them, art_spec 12)")
    print(f"{slug}: {s['units']} units, {f} frogs" + ('' if ok else '  <- VARIETY LOW'))
    for l in L: print(l)
    if f: print('  acts: ' + ' '.join(f'{k}:{c}' for k, c in s['acts'].most_common(10)) + '\n  outfits: ' + ' '.join(f'{k}:{c}' for k, c in s['outfits'].most_common(8)))
    return ok

if __name__ == '__main__':
    rep = '--report' in sys.argv; slugs = [a for a in sys.argv[1:] if not a.startswith('--')] or [os.environ.get('SLUG', '')]
    bad = [s for s in slugs if not judge(s, stats(s))]
    if bad and not rep: print('VARIETY CHECK FAILED:', ' '.join(bad), '(more acts / outfits come from script words + concept pools; object kinds and moving props come from the pictures: art_spec 7B/12)'); sys.exit(1)
