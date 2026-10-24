#!/bin/bash
# usage: SLUG=<slug> MIYA_WORK=<dir> HYPERFRAMES_PYTHON=<venv python with kokoro-onnx, soundfile> tools/tts.sh
# Makes one wav per scene (tts/p01.wav ...) from videos/$SLUG/script.py with Kokoro (voice af_heart).
set -e
HERE="$(cd "$(dirname "$0")/.." && pwd)"; W="${MIYA_WORK:-/tmp/miya-work}/$SLUG/tts"; mkdir -p "$W"
python3 - "$HERE" "$W" <<'PY'
import sys, importlib.util
sys.path.insert(0, f'{sys.argv[1]}/tools'); from tts_text import years
spec = importlib.util.spec_from_file_location('s', f'{sys.argv[1]}/videos/{__import__("os").environ["SLUG"]}/script.py'); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
for i, s in enumerate(m.SCENES, 1): open(f'{sys.argv[2]}/p{i:02d}.txt', 'w').write(years(s[4]))
PY
cd "$W"
for f in p*.txt; do n=${f%.txt}; [ -s $n.wav ] && continue; npx --yes hyperframes@0.8.141 tts "$f" -v af_heart -o $n.wav >/dev/null 2>&1 || echo "FAIL $n"; done
ls p*.wav | wc -l
