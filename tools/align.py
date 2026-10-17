# Word-level timing of every narration clip (2026-10-17): the real speech, not a character-count estimate.
# usage: SLUG=<slug> python3 tools/align.py [scene numbers...]      (or: python3 tools/align.py <slug> [<slug> ...])
# Reads  <work>/<slug>/build/s<NN>.wav  and the scene text from videos/<slug>/script.py,
# writes <work>/<slug>/build/words.json = {"model":..., "scenes": {"<NN>": {"cov": 0..1, "words": [[t0, t1], ...]}}}
# with one [t0, t1] (seconds from the clip start) for EVERY whitespace-separated token of the scene text.
# Method: faster-whisper transcribes with word timestamps (the script is given as initial prompt, so numbers and names
# come out as written), the recognised words are matched to the script words (difflib); script words with no match
# (digits spoken as words, symbols) take the time span of the unmatched recognised words, or are spread by length
# between their matched neighbours. build3.py refuses to build when a scene matches < 90 % of its words.
import os, re, sys, json, difflib, hashlib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

MODEL = os.environ.get('ALIGN_MODEL', 'small.en')


def load_audio(path):
    import subprocess, numpy as np
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', path, '-f', 'f32le', '-ac', '1', '-ar', '16000', '-'], capture_output=True).stdout
    return np.frombuffer(raw, dtype=np.float32)


def norm(w):
    return re.sub(r'[^a-z0-9]', '', w.lower())


def spread(items, t0, t1):
    """items: list of token strings; give each a slice of [t0, t1] proportional to its length"""
    t1 = max(t1, t0 + 0.04 * len(items))
    ln = [max(len(x), 1) for x in items]; tot = sum(ln); out = []; c = 0
    for l in ln:
        out.append([t0 + (t1 - t0) * c / tot, t0 + (t1 - t0) * (c + l) / tot]); c += l
    return out


def match(tokens, rec):
    """tokens: script tokens; rec: [(word, t0, t1)] recognised. -> (times per token, coverage)"""
    a = [norm(t) for t in tokens]; b = [norm(r[0]) for r in rec]
    sm = difflib.SequenceMatcher(None, a, b, autojunk=False)
    times = [None] * len(tokens); eq = 0
    ops = sm.get_opcodes()
    for tag, i1, i2, j1, j2 in ops:
        if tag == 'equal':
            for k in range(i2 - i1):
                times[i1 + k] = [rec[j1 + k][1], rec[j1 + k][2]]
            eq += i2 - i1
    for n, (tag, i1, i2, j1, j2) in enumerate(ops):
        if tag == 'equal' or i1 == i2:
            continue
        prev_end = rec[j1 - 1][2] if j1 > 0 else 0.0
        next_start = rec[j2][1] if j2 < len(rec) else (rec[-1][2] if rec else prev_end + 0.3 * (i2 - i1))
        if j2 > j1:                       # recognised words that did not match (spoken digits, name spellings ...)
            t0, t1 = rec[j1][1], rec[j2 - 1][2]
            eq += min(i2 - i1, 2 * (j2 - j1))   # heard something there: counts as covered, a skipped passage does not
        else:
            t0, t1 = prev_end, next_start
        for k, t in enumerate(spread(tokens[i1:i2], t0, t1)):
            times[i1 + k] = t
    for k in range(len(times)):           # monotonic, non-negative
        lo = times[k - 1][1] if k else 0.0
        times[k][0] = max(times[k][0], lo if k else 0.0); times[k][1] = max(times[k][1], times[k][0])
    return times, (eq / len(tokens) if tokens else 1.0)


def align_slug(slug, only=None):
    from faster_whisper import WhisperModel
    import paths
    paths.SLUG = slug; os.environ['SLUG'] = slug
    from paths import load_scenes, wdir
    scenes = load_scenes(slug); B = wdir(slug) + '/build'; out_f = f'{B}/words.json'
    data = json.load(open(out_f)) if os.path.exists(out_f) else {'model': MODEL, 'scenes': {}}
    if data.get('model') != MODEL:
        data = {'model': MODEL, 'scenes': {}}
    model = None
    for i in range(1, len(scenes) + 1):
        if only and i not in only:
            continue
        text = scenes[i - 1][4]; wav = f'{B}/s{i:02d}.wav'
        key = hashlib.md5((text + str(os.path.getsize(wav))).encode()).hexdigest()
        old = data['scenes'].get(f'{i:02d}', {})
        if old.get('key') == key and old.get('cov', 0) >= 0.9:
            continue
        if model is None:
            model = WhisperModel(MODEL, device='cpu', compute_type='int8', cpu_threads=os.cpu_count() or 4)
        audio = load_audio(wav); tokens = text.split(); best = None
        for prompt in (text[:800], None):   # the prompt keeps numbers/names as written, but can make the model skip text: then retry without it
            segs, _ = model.transcribe(audio, language='en', word_timestamps=True, initial_prompt=prompt,
                                       condition_on_previous_text=False, beam_size=5, vad_filter=False)
            rec = [(w.word.strip(), w.start, w.end) for s in segs for w in (s.words or []) if norm(w.word)]
            times, cov = match(tokens, rec)
            if best is None or cov > best[1]:
                best = (times, cov)
            if cov >= 0.9:
                break
        times, cov = best
        data['scenes'][f'{i:02d}'] = {'key': key, 'cov': round(cov, 3), 'words': [[round(a, 3), round(b, 3)] for a, b in times]}
        print(f'{slug} scene {i:02d}: {len(tokens)} words, matched {cov:.0%}', flush=True)
        json.dump(data, open(out_f, 'w'))
    json.dump(data, open(out_f, 'w'))
    low = [k for k, v in data['scenes'].items() if v['cov'] < 0.9]
    print(f'{slug}: {len(data["scenes"])} scenes, low coverage: {low or "none"}', flush=True)


if __name__ == '__main__':
    args = sys.argv[1:]
    if args and not args[0].isdigit():
        for s in args:
            align_slug(s)
    else:
        align_slug(os.environ['SLUG'], {int(x) for x in args})
