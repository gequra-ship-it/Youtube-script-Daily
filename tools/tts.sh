#!/bin/bash
# usage: SLUG=<slug> MIYA_WORK=<dir> HYPERFRAMES_PYTHON=<venv python with kokoro-onnx, soundfile> tools/tts.sh
# Makes one wav per scene (tts/p01.wav ...) from videos/$SLUG/script.py with Kokoro (voice af_heart).
set -e
HERE="$(cd "$(dirname "$0")/.." && pwd)"; W="${MIYA_WORK:-/tmp/miya-work}/$SLUG/tts"; mkdir -p "$W"
python3 - "$HERE" "$W" <<'PY'
import sys, shutil
sys.path.insert(0, f'{sys.argv[1]}/tools'); from tts_text import years; from paths import load_scenes
for i, s in enumerate(load_scenes(), 1):
    open(f'{sys.argv[2]}/p{i:02d}.txt', 'w').write(years(s[4]))
    if s[0] == 'OUTRO': shutil.copy(f'{sys.argv[1]}/tools/assets/outro.wav', f'{sys.argv[2]}/p{i:02d}.wav')   # the outro narration is one fixed file (2026-10-24)
PY
cd "$W"
for f in p*.txt; do n=${f%.txt}; [ -s $n.wav ] && continue; npx --yes hyperframes@0.8.141 tts "$f" -v af_heart -o $n.wav >/dev/null 2>&1 || echo "FAIL $n"; done
ls p*.wav | wc -l
