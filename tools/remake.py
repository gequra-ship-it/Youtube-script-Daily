# Remake an existing video with the current rules while reusing its pictures (guideline 21, 2026-10-17).
# usage: SLUG=<slug> python3 tools/remake.py          (narration audio must exist: tools/tts.sh + tools/audio_prep.py first)
# 1. keeps the current plan.json as $MIYA_WORK/<slug>/plan_prev.json
# 2. re-splits units with the current pacing (build3 HOOK default unless config.py sets HOOK) -> plan.json
# 3. tools/remap_art.py gives every new unit the old picture it overlaps most; prints NO ART / NEEDS VARIANT units (the only drawing left)
# 4. checks render/<slug>/.dest (old/... = archive folder) and removes .skip_deliver so metadata/script/thumbnails upload again
import os, shutil, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from paths import *
slug = os.environ['SLUG']; env = dict(os.environ)
os.makedirs(wdir(), exist_ok=True)
prev = f'{wdir()}/plan_prev.json'
shutil.copy(f'{vdir()}/plan.json', prev)
subprocess.run([sys.executable, f'{REPO}/tools/build3.py'], env=dict(env, PLAN='1'), check=True)
subprocess.run([sys.executable, f'{REPO}/tools/remap_art.py', prev], env=env, check=True)
r = f'{REPO}/render/{slug}'
dest = open(f'{r}/.dest').read().strip() if os.path.exists(f'{r}/.dest') else '(none: default folder)'
print('Drive .dest:', dest, '  <- old/... is the archive; set "<Category>/NN_<slug>" for a new upload' if dest.startswith('old/') else '')
if os.path.exists(f'{r}/.skip_deliver'):
    os.remove(f'{r}/.skip_deliver'); print('removed .skip_deliver (deliver/ uploads again)')
