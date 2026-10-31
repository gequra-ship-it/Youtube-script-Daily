# usage: SLUG=<slug> [MIYA_WORK=...] python3 tools/final_check.py        (needs a finished build: render/<slug>/index.html)
# THE MAIN SESSION'S FINAL GATE before any render push (miya 2026-10-29: "마지막에 메인이 다시 한번 확인"). Agents check their own pictures (attachcheck / motionaudit), but the main
# session re-runs everything on the BUILT page and only then lets the render go:
#   1. attachcheck   every picture: hinges on the body, rotors on their centre, gears mesh, tails travel with the body, standing things have their foot as pivot, labels follow
#   2. pivotlive     the real page: every data-pivot group really turns about its pivot (a part that leaves its body is carried > 10 px at its pivot)
#   2b. originlive   groups without data-pivot (spin/turn/roll/wobble) really turn about their own centre
#   3. stuck pages   no moment of the timeline shows more than 3 pictures at once (a picture left on top)
#   4. coverage      every unit has its picture, no fallback art
#   5. variety       tools/variety_check.py: top frog act <= 40 %, >= 8 acts, >= 4 outfits, >= 8 object kinds; moving-prop quota printed as WARN (2026-10-31)
# Exit 0 + writes render/<slug>/.checked (sha1 of index.html) only when everything is clean. tools/chunk_plan.py refuses to print the render spec without a matching .checked.
# Then LOOK: `python3 tools/motionaudit.py <dir> <uid...>` on the units the owner listed or that the checks flagged before (strips with red pivot dots).
import os, sys, subprocess, hashlib, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from paths import *
T = os.path.dirname(os.path.abspath(__file__)); env = dict(os.environ, SLUG=SLUG)
bad = 0
def run(name, cmd):
    global bad
    r = subprocess.run(cmd, capture_output=True, text=True, env=env); out = (r.stdout + r.stderr).strip().splitlines()
    print(f'--- {name}: {"OK" if r.returncode == 0 else "PROBLEMS"}')
    for l in out[-40:] if r.returncode else out[-2:]: print('   ', l[:300])
    if r.returncode: bad += 1
run('attachcheck', [sys.executable, f'{T}/attachcheck.py', SLUG])
run('pivotlive', [sys.executable, f'{T}/pivotlive.py'])
run('originlive', [sys.executable, f'{T}/originlive.py'])   # 2026-10-29: groups without data-pivot turn about their own centre (short3 black hole)
run('variety', [sys.executable, f'{T}/variety_check.py', SLUG])   # 2026-10-31: the variety gate (frog acts / outfits / object kinds; moving-prop quota is a WARN line) — read its lines even when OK
bd = json.load(open(f'{wdir()}/build/build_data.json')); n = len(bd['cuts'])
miss = [c['id'] for c in bd['cuts'] if c.get('kind') != 'chalk' and not os.path.exists(f'{vdir(SLUG)}/art3/{c["id"]}.svg')]
print(f'--- coverage: {"OK" if not miss else "MISSING " + str(miss)} ({n} units)'); bad += bool(miss)
html = open(f'{REPO}/render/{SLUG}/index.html', encoding='utf-8').read()
import re as _re   # 2026-10-30: CustomWiggle type "random" froze the Actions capture near the end of its tween (miya: video stops, audio goes on); tremble uses miyaJit now. Never ship it again.
_rw = _re.findall(r'ease:"wiggle\(|CustomWiggle\.create|wiggle\(\{[^)]*random', html)   # any string wiggle ease froze the capture too (2nd cause)
if _rw: print(f'--- frozen-capture guard: {len(_rw)} CustomWiggle/string wiggle ease(s) on the page (use miyaW / miyaJit)'); bad += 1
if bad: print(f'FINAL CHECK FAILED ({bad} part(s)): fix, rebuild, run again. No .checked written.'); sys.exit(1)
open(f'{REPO}/render/{SLUG}/.checked', 'w').write(hashlib.sha1(html.encode('utf-8')).hexdigest() + '\n'); print('FINAL CHECK PASSED: .checked written for this build.')
