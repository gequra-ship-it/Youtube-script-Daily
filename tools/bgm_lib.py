# -*- coding: utf-8 -*-
# Background music synthesiser for Miya's Lab (own composition, no samples, no vocals -> no copyright issue).
# Soft pad + sparse soft plucks, slow chord changes, all content above ~200 Hz (no low drone), high-passed at 250 Hz.
# Ducked under the narration with an envelope computed from the actual narration files.
import sys, subprocess, wave
import numpy as np
from scipy.signal import butter, sosfilt
SR = 48000
NOTE = {'C': 0, 'D': 2, 'E': 4, 'F': 5, 'G': 7, 'A': 9, 'B': 11}
def hz(m): return 440.0 * 2 ** ((m - 69) / 12)
# progressions as MIDI chords (all notes >= A3 = 57)
PROGS = [
    [[57, 64, 69, 72], [53, 60, 65, 69], [60, 64, 67, 72], [55, 62, 67, 71]],      # Am F C G
    [[60, 64, 67, 71], [57, 64, 67, 72], [53, 60, 65, 69], [55, 62, 67, 71]],      # Cmaj7 Am7 F G
    [[62, 65, 69, 72], [58, 62, 65, 69], [60, 64, 67, 72], [57, 64, 69, 72]],      # Dm Bb C Am
    [[57, 60, 64, 71], [65, 69, 72, 76], [60, 64, 67, 71], [55, 62, 67, 71]],      # Am9 Fmaj7 Cmaj7 G
]
CHORD_S = 8.0

def _env(n, a, r):
    e = np.ones(n); na = int(a * SR); nr = int(r * SR)
    na = min(na, n // 2); nr = min(nr, n // 2)
    e[:na] = np.linspace(0, 1, na) ** 2; e[n - nr:] = np.linspace(1, 0, nr) ** 2
    return e

def synth(total, seed=5):
    rng = np.random.default_rng(seed)
    nchord = int(total / CHORD_S) + 2
    n = int((nchord * CHORD_S + 14) * SR)
    L = np.zeros(n); R = np.zeros(n)
    order = []
    while len(order) < nchord:                       # section order: shuffled progressions, never the same twice in a row
        p = int(rng.integers(len(PROGS)))
        if order and p == order[-1][0]: continue
        for k in range(4): order.append((p, k))
    order = order[:nchord]
    for ci, (pi, k) in enumerate(order):
        chord = PROGS[pi][k]; t0 = int(ci * CHORD_S * SR); dl = int((CHORD_S + 3.0) * SR)
        tt = np.arange(dl) / SR; env = _env(dl, 2.2, 3.0)
        for mi, m in enumerate(chord):
            for det, pan in ((0.0, 0.35), (0.0035, -0.35)):
                f = hz(m) * (1 + det + rng.uniform(-.0008, .0008))
                x = (np.sin(2 * np.pi * f * tt) + .25 * np.sin(2 * np.pi * 2 * f * tt) * (1 + .3 * np.sin(2 * np.pi * .1 * tt + mi))) * env * .06
                L[t0:t0 + dl] += x * (1 - pan) * .5 * 2; R[t0:t0 + dl] += x * (1 + pan) * .5 * 2
        # sparse soft plucks: pentatonic-ish chord tones, 1 per beat at 60 bpm with ~40 % probability
        nb = int(CHORD_S)
        for b in range(nb):
            if rng.random() < .42:
                m = int(rng.choice(chord)) + int(rng.choice([0, 12, 12]))
                st = max(0, t0 + int((b + rng.uniform(-.02, .05)) * SR)); dd = int(2.4 * SR); t2 = np.arange(dd) / SR
                f = hz(m); x = (np.sin(2 * np.pi * f * t2) + .3 * np.sin(2 * np.pi * 2 * f * t2) * np.exp(-t2 * 5)) * np.exp(-t2 * 2.2) * np.minimum(t2 / .012, 1) * .045
                pan = rng.uniform(-.5, .5); L[st:st + dd] += x * (1 - pan); R[st:st + dd] += x * (1 + pan)
    out = []
    for ch in (L, R):
        ch = sosfilt(butter(2, 250, 'hp', fs=SR, output='sos'), ch)
        ch = sosfilt(butter(2, 4500, 'lp', fs=SR, output='sos'), ch)
        out.append(ch[:int(total * SR)])
    return np.stack(out, 1)

def narration_envelope(files_starts, total, hop=0.05):
    """returns (rms per hop frame (linear), mask of speech) from narration files placed at start times"""
    nf = int(total / hop) + 2; rms = np.zeros(nf)
    for f, st in files_starts:
        raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', f, '-ac', '1', '-ar', '8000', '-f', 'f32le', '-'], capture_output=True).stdout
        x = np.frombuffer(raw, '<f4'); h = int(8000 * hop); m = len(x) // h
        r = np.sqrt((x[:m * h].reshape(m, h) ** 2).mean(1)); i0 = int(round(st / hop))
        rms[i0:i0 + m] = np.maximum(rms[i0:i0 + m], r[:max(0, min(m, nf - i0))] if i0 + m <= nf else r[:nf - i0])
    return rms

def duck_gain(rms, hop=0.05, close_s=0.6, up_db=4.0, atk=0.25, rel=1.2):
    sp = rms > 10 ** (-48 / 20)
    k = int(close_s / hop); sp2 = sp.copy()
    idx = np.flatnonzero(sp)
    for a, b in zip(idx[:-1], idx[1:]):              # close gaps shorter than close_s
        if 1 < b - a <= k: sp2[a:b] = True
    tgt = np.where(sp2, 0.0, up_db)                  # dB relative to ducked level
    g = np.zeros(len(tgt)); cur = 0.0
    for i, v in enumerate(tgt):
        c = hop / (atk if v < cur else rel); cur += (v - cur) * min(c, 1.0); g[i] = cur
    return g, sp2

def make_bgm(path_wav, total, files_starts, below_db=13.0, seed=5):
    x = synth(total, seed)
    rms = narration_envelope(files_starts, total)
    g, sp = duck_gain(rms)
    hop = 0.05; tt = np.arange(len(x)) / SR
    gi = np.interp(tt, np.arange(len(g)) * hop, g)
    x = x * (10 ** (gi / 20))[:, None]
    # calibrate: BGM rms over speech frames = narration rms over speech frames - below_db
    spi = np.interp(tt, np.arange(len(sp)) * hop, sp.astype(float)) > .5
    nr = np.sqrt((rms[sp] ** 2).mean()) if sp.any() else 0.1
    br = np.sqrt((x[spi] ** 2).mean()) if spi.any() else np.sqrt((x ** 2).mean())
    x = x * (nr * 10 ** (-below_db / 20) / br)
    fi = int(3 * SR); fo = int(5 * SR)
    x[:fi] *= np.linspace(0, 1, fi)[:, None] ** 2; x[-fo:] *= np.linspace(1, 0, fo)[:, None] ** 2
    with wave.open(path_wav, 'wb') as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((np.clip(x, -1, 1) * 32767).astype('<i2').tobytes())
    return dict(narr_speech_rms_db=20 * np.log10(nr + 1e-9), bgm_speech_rms_db=20 * np.log10(np.sqrt((x[spi] ** 2).mean()) + 1e-9), peak_db=20 * np.log10(np.abs(x).max()))
