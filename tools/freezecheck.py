# usage: python3 tools/freezecheck.py <video.mp4> [min_freeze_seconds=5]      exit 1 when the picture is frozen
# Found 2026-10-29 (miya, shorts3): the Actions capture can stall on a heavy frame and then every later frame is the same picture (video frozen, audio goes on) although the
# workflow reports success (frame count and length are right). This samples the video at 2 fps and reports every stretch of >= min seconds with at most 2 distinct frames.
# Run it on the chunk artifact right after a render:  gh run download <run> -R <repo> -n chunk-<slug>-0 ; python3 tools/freezecheck.py chunk.mp4
import sys, subprocess, hashlib, tempfile, os, glob
mp4 = sys.argv[1]; mn = float(sys.argv[2]) if len(sys.argv) > 2 else 5.0
with tempfile.TemporaryDirectory() as d:
    subprocess.run(['ffmpeg', '-nostdin', '-v', 'error', '-i', mp4, '-vf', 'fps=2,scale=108:-2', f'{d}/%05d.png'], check=True)
    fr = sorted(glob.glob(d + '/*.png')); h = [hashlib.md5(open(f, 'rb').read()).hexdigest() for f in fr]
bad = []; i = 0; w = int(mn * 2)
while i < len(h):
    j = i
    while j + 1 < len(h) and len(set(h[i:j + 2])) <= 2: j += 1
    if j - i + 1 >= w: bad.append((i / 2, (j + 1) / 2)); i = j + 1
    else: i += 1
for a, b in bad: print(f'FROZEN picture from {a:.1f}s to {b:.1f}s ({b - a:.1f}s with at most 2 distinct frames)')
print(os.path.basename(mp4), 'freezecheck:', 'FROZEN' if bad else 'ok', f'({len(h)/2:.0f}s sampled)'); sys.exit(1 if bad else 0)
