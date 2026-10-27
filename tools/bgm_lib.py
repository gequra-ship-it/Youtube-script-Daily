# -*- coding: utf-8 -*-
# Background music synthesiser for Miya's Note (own composition, no samples, no vocals -> no copyright issue).
# Soft pad + sparse soft plucks, slow chord changes, all content above ~200 Hz (no low drone), high-passed at 250 Hz.
# Ducked under the narration with an envelope computed from the actual narration files.
# 2026-10-27 (miya: "more background music, chosen automatically from the script"): 9 STYLES (one timbre/tempo per video, picked by
# style_for() from the palette + the whole script, config STYLE overrides) x 4 MOODS (calm/bright/dark/tense progression pools, picked per
# scene by scene_moods() from the narration words; the pool and the pluck density change at the next chord boundary). 72 progressions.
# All deterministic (seed + word counts), guideline 9-4.
import sys, subprocess, wave, re
import numpy as np
from scipy.signal import butter, sosfilt
SR = 48000
PC = {'C': 0, 'D': 2, 'E': 4, 'F': 5, 'G': 7, 'A': 9, 'B': 11}
Q = {'': [0, 4, 7, 12], 'm': [0, 3, 7, 12], 'maj7': [0, 4, 7, 11], 'm7': [0, 3, 7, 10], '7': [0, 4, 7, 10], 'sus2': [0, 2, 7, 12], 'sus4': [0, 5, 7, 12],
     'add9': [0, 4, 7, 14], 'madd9': [0, 3, 7, 14], 'dim': [0, 3, 6, 12], 'm9': [0, 3, 10, 14], '69': [0, 4, 9, 14], 'mb6': [0, 3, 7, 8], 'maj9': [0, 4, 11, 14],
     'm6': [0, 3, 7, 9], 'aug': [0, 4, 8, 12], 'sus2b': [0, 2, 7, 10], 'm7b5': [0, 3, 6, 10], 'mmaj7': [0, 3, 7, 11]}
def hz(m): return 440.0 * 2 ** ((m - 69) / 12)
def chord(sym):
    """'Am' 'Fmaj7' 'Bbadd9' 'Dsus2' -> MIDI notes, root in A3..G#4 (same register as the 2026-10-10 voicings)"""
    m = re.match(r'([A-G])([#b]?)(.*)', sym); pc = PC[m.group(1)] + (1 if m.group(2) == '#' else -1 if m.group(2) == 'b' else 0)
    r = 48 + pc % 12
    if r < 53: r += 12
    return [r + i for i in Q[m.group(3)]]
def P(*progs): return [[chord(c) for c in p.split()] for p in progs]
# -- progression pools: each style has calm / bright / dark / tense, two progressions each, 4 chords each (own writing) --
POOLS = {
 'warm': dict(calm=P('Am F C G', 'Cmaj7 Am7 F G'), bright=P('C G Am F', 'F C G Am'), dark=P('Dm Bb C Am', 'Am Em F Dm'), tense=P('Am9 Fmaj7 Cmaj7 G', 'Dm Bbmaj7 Gm Am')),
 'cosmic': dict(calm=P('Am9 Fmaj7 G69 Em9', 'Dsus2 Csus2 Am9 Bm7'), bright=P('Cmaj9 Amadd9 F69 G69', 'Gsus2 Dsus2 Em9 Csus2'), dark=P('Am9 Fmaj7 Dm9 Em9', 'Em9 Cmaj9 Am9 Bsus2b'), tense=P('Am9 Bbmaj7 Am9 Gm9', 'Dm9 Ebmaj7 Dm9 Csus2')),
 'ancient': dict(calm=P('Dm Dm7 C Dm', 'Am G Am Em'), bright=P('D Dsus4 D G', 'C Dm C F'), dark=P('Dm Gm Dm Am', 'Em Am Em Bm'), tense=P('Dm Ebmaj7 Dm Am', 'Am Bb Am Gm')),
 'ocean': dict(calm=P('Cadd9 Gsus4 Amadd9 Fadd9', 'Fmaj7 Cmaj7 Gsus2 Amadd9'), bright=P('Gadd9 Dsus2 Em9 Cadd9', 'Cmaj9 Fmaj9 Gsus4 Cadd9'), dark=P('Amadd9 Fmaj7 Dm9 Em7', 'Dm9 Bbmaj7 Fmaj7 Am7'), tense=P('Am9 Fmaj7 Dm9 E7', 'Dm9 Bbmaj7 Gm9 A7')),
 'mystery': dict(calm=P('Am Fmaj7 Am Em9', 'Em Cmaj7 Em Bm7'), bright=P('Cmaj7 Ebmaj7 Cmaj7 Fmaj7', 'Fmaj7 Abmaj7 Fmaj7 G69'), dark=P('Am Abaug Am Dm9', 'Em Ebaug Em Am9'), tense=P('Am Bbmaj7 Am Bdim', 'Dm Ebmaj7 Dm Edim')),
 'tense': dict(calm=P('Am Am Fmaj7 Am', 'Dm Dm Bbmaj7 Dm'), bright=P('Am C G Am', 'Dm F C Dm'), dark=P('Am Fm Am Em', 'Dm Bbm Dm Am'), tense=P('Am Bb Am Bdim', 'Am Bbm7b5 Am Gm')),
 'bright': dict(calm=P('C G Am F', 'G D Em C'), bright=P('C D F C', 'F G C Am'), dark=P('Am F Dm Am', 'Em C Am Em'), tense=P('C Fm C G', 'F Bbm F C')),
 'gentle': dict(calm=P('Cmaj7 Fmaj7 Am7 Gsus4', 'Fmaj7 Em7 Dm7 Cmaj7'), bright=P('Cmaj7 Dm7 Em7 Fmaj7', 'Gmaj7 Cmaj7 Am7 Dsus4'), dark=P('Am7 Dm7 Fmaj7 Em7', 'Dm7 Gm7 Bbmaj7 Am7'), tense=P('Am7 Fmaj7 Dm7 E7', 'Em7 Cmaj7 Am7 B7')),
 'solemn': dict(calm=P('Am Em F Em', 'Dm Am Bb Am'), bright=P('F C Dm Am', 'C G Am Em'), dark=P('Am Dm Am Em', 'Dm Gm Dm Am'), tense=P('Am Fm Am Em', 'Dm Bbm Dm Am')),
}
# timbre / tempo per style (never changes inside one video, guideline 9-4)
STYLES = {
 'warm':    dict(chord_s=8.0, voices=((0.0, .35), (0.0035, -.35)), h2=.25, h3=0.0, env=(2.2, 3.0), pad=.06, pluck=.42, pdec=2.2, pamp=.045, poct=(0, 12, 12), arp=0, echo=0, lp=4500),
 'cosmic':  dict(chord_s=12.0, voices=((-0.004, .6), (0.0, 0.0), (0.004, -.6)), h2=.35, h3=.12, env=(4.0, 5.0), pad=.045, pluck=0.0, pdec=1.1, pamp=.03, poct=(12,), arp=1.5, echo=1, lp=6500),
 'ancient': dict(chord_s=8.0, voices=((0.0, .3), (0.003, -.3)), h2=.45, h3=.18, env=(1.6, 2.4), pad=.05, pluck=.5, pdec=3.4, pamp=.05, poct=(0, 0, 12), arp=0, echo=0, lp=5000),
 'ocean':   dict(chord_s=10.0, voices=((-0.003, .5), (0.0, 0.0), (0.003, -.5)), h2=.3, h3=.05, env=(3.5, 4.5), pad=.055, pluck=.3, pdec=1.4, pamp=.04, poct=(0, 12), arp=0, echo=1, lp=5000),
 'mystery': dict(chord_s=9.0, voices=((-0.005, .4), (0.005, -.4)), h2=.2, h3=.1, env=(3.0, 3.5), pad=.05, pluck=.3, pdec=1.8, pamp=.04, poct=(12, 12, 24), arp=0, echo=1, lp=5500),
 'tense':   dict(chord_s=7.0, voices=((-0.004, .3), (0.004, -.3)), h2=.3, h3=.15, env=(1.2, 2.0), pad=.055, pluck=.3, pdec=4.0, pamp=.045, poct=(0, 0, 12), arp=0, echo=0, lp=4000, trem=.5),
 'bright':  dict(chord_s=6.0, voices=((0.0, .35), (0.003, -.35)), h2=.3, h3=.08, env=(1.5, 2.0), pad=.055, pluck=.55, pdec=2.6, pamp=.05, poct=(0, 12, 12, 24), arp=0, echo=0, lp=5000),
 'gentle':  dict(chord_s=8.0, voices=((0.0, .3), (0.0025, -.3)), h2=.2, h3=0.0, env=(2.6, 3.4), pad=.06, pluck=.35, pdec=2.0, pamp=.04, poct=(0, 12), arp=0, echo=0, lp=4200),
 'solemn':  dict(chord_s=10.0, voices=((0.0, .3), (0.003, -.3)), h2=.15, h3=0.0, env=(3.2, 4.0), pad=.06, pluck=.22, pdec=1.6, pamp=.04, poct=(0, 0, 12), arp=0, echo=0, lp=3800),
}
STYLES['default'] = STYLES['warm']; POOLS['default'] = POOLS['warm']
MOOD_PLUCK = {'calm': 1.0, 'bright': 1.3, 'dark': .7, 'tense': .6}
MOOD_PAD = {'calm': 1.0, 'bright': 1.0, 'dark': .9, 'tense': .95}
CHORD_S = 8.0; CHORD_S_COSMIC = 12.0           # kept for older imports
PROGS = POOLS['warm']['calm'] + POOLS['warm']['tense']; PROGS_COSMIC = POOLS['cosmic']['calm'] + POOLS['cosmic']['bright'][:1]

# -- word rules (per scene) --
MOODW = {
 'tense':  r'\b(danger\w*|deadly|lethal|poison\w*|attack\w*|war|wars|battle\w*|enem(?:y|ies)|trapp?ed|panic\w*|terrif\w*|threat\w*|crisis|collaps\w*|chas(?:e|ed|ing)|flee\w*|fled|escap\w*|alarm\w*|desperate\w*|fatal\w*|kill\w*|murder\w*|hunt(?:ed|ing)?|predator\w*|crushing|explo\w+|outbreak|infect\w*|epidemic|plague|starv\w*|drown\w*|suffocat\w*)\b',
 'dark':   r'\b(died?|death|dead|dying|grave\w*|tomb\w*|lost|alone|lonel\w*|dark\w*|cold|silen\w*|extinct\w*|grief|mourn\w*|sorrow|decay\w*|rot\w*|sink\w*|sank|vanish\w*|forgotten|ruins?|empty|void|never (?:came|returned|seen)|last (?:breath|time|days?)|fade\w*|bur(?:ied|ial)|corpse\w*|bones?|skeleton\w*|abandon\w*)\b',
 'bright': r'\b(discover\w*|wonder\w*|beautiful\w*|amazing|astonish\w*|finally|success\w*|hope\w*|celebrat\w*|joy\w*|laugh\w*|incredibl\w*|remarkabl\w*|brilliant|triumph\w*|thriv\w*|flourish\w*|bloom\w*|born|birth|new life|alive|sunrise|dawn|smil\w*|delight\w*|marvel\w*|breakthrough|solved|cheer\w*|surviv\w*|rescu\w*)\b',
}
PAL_STYLE = {'ocean': 'ocean', 'forest': 'gentle', 'desert': 'ancient', 'ice': 'solemn', 'lab': 'mystery', 'history': 'ancient', 'space': 'cosmic', 'deepfield': 'cosmic',
             'nebula': 'cosmic', 'aurora': 'cosmic', 'solar': 'cosmic', 'storm': 'tense', 'body': 'gentle', 'sunset': 'warm'}
MOOD_STYLE = {'tense': 'tense', 'dark': 'solemn', 'bright': 'bright'}


def mood_counts(text):
    return {m: len(re.findall(rx, text, re.I)) for m, rx in MOODW.items()}


def scene_mood(text):
    """mood of one scene's narration: the strongest word group with >= 2 hits (ties: tense > dark > bright), else calm"""
    c = mood_counts(text); best = max(('tense', 'dark', 'bright'), key=lambda m: (c[m], -['tense', 'dark', 'bright'].index(m)))
    return best if c[best] >= 2 and c[best] >= 1.5 * max(v for m, v in c.items() if m != best) else 'calm'


def scene_moods(texts, starts):
    """[(start_s, mood)] per scene, in time order; the first scene is never 'tense' (the hook should open calm/bright)"""
    out = []
    for i, (t, st) in enumerate(zip(texts, starts)):
        m = scene_mood(t)
        if i == 0 and m == 'tense': m = 'dark'
        out.append((st, m))
    return out


def style_for(cfg, texts, pal_default):
    """config STYLE wins; else palette -> style, overridden by a strong whole-script mood (>= 6 hits per 1000 words and 1.5x the others)"""
    st = getattr(cfg, 'STYLE', None)
    if st: return st if st in STYLES else 'warm'
    base = PAL_STYLE.get(pal_default, 'warm')
    if base == 'cosmic': return base
    text = ' '.join(texts); words = max(len(text.split()), 1); c = mood_counts(text)
    best = max(c, key=c.get); per = c[best] * 1000 / words
    if per >= 6 and c[best] >= 1.5 * max(v for m, v in c.items() if m != best): return MOOD_STYLE[best]
    return base


def _env(n, a, r):
    e = np.ones(n); na = int(a * SR); nr = int(r * SR)
    na = min(na, n // 2); nr = min(nr, n // 2)
    e[:na] = np.linspace(0, 1, na) ** 2; e[n - nr:] = np.linspace(1, 0, nr) ** 2
    return e


def _order(rng, pools, moods, nchord, cs):
    """progression per chord slot: pool by the mood active at the slot start (a mood must hold >= 2 slots). The progression changes with the
    situation: a new one when the mood changes, otherwise the same one for two cycles and then the pool's next (miya 2026-10-27: repetition
    follows the script, no blanket ban); returns [(mood, prog, k)]"""
    out = []; prog = None; k = 4; cur = 'calm'; held = 0; cyc = 0; base = int(rng.integers(8))
    for ci in range(nchord):
        t = ci * cs; m = 'calm'
        for st, mm in moods:
            if st <= t + 1e-6: m = mm
        if m != cur and held >= 2: cur = m; held = 0; k = 4; cyc = 0; base += 1   # mood change -> new progression from the new pool at this slot
        held += 1
        if k >= 4:
            pool = pools.get(cur) or pools['calm']; pi = (base + cyc // 2) % len(pool)
            prog = pool[pi]; k = 0; cyc += 1
        out.append((cur, prog, k)); k += 1
    return out


def synth(total, seed=5, style='default', accents=(), moods=()):
    """accents: times (s) of big picture changes -> two soft chord tones of the chord playing then (guideline 9-5).
    moods: [(start_s, 'calm'|'bright'|'dark'|'tense')] per scene (scene_moods); empty = calm throughout."""
    S = STYLES.get(style, STYLES['warm']); pools = POOLS.get(style, POOLS['warm']); cs = S['chord_s']
    rng = np.random.default_rng(seed)
    nchord = int(total / cs) + 2
    n = int((nchord * cs + 20) * SR); L = np.zeros(n); R = np.zeros(n)
    order = _order(rng, pools, moods, nchord, cs)
    atk, rel = S['env']; tail = rel + 1.0
    for ci, (mood, prog, k) in enumerate(order):
        ch = prog[k]; t0 = int(ci * cs * SR); dl = int((cs + tail) * SR)
        tt = np.arange(dl) / SR; env = _env(dl, atk, rel) * MOOD_PAD[mood]
        if S.get('trem'): env = env * (1 - .12 * (1 - np.cos(2 * np.pi * S['trem'] * tt)) / 2)
        for mi, m in enumerate(ch):
            for det, pan in S['voices']:
                f = hz(m) * (1 + det + rng.uniform(-.0008, .0008))
                sw = 1 + .3 * np.sin(2 * np.pi * (.1 + .02 * mi) * tt + mi * 1.7)
                x = (np.sin(2 * np.pi * f * tt) + S['h2'] * np.sin(2 * np.pi * 2 * f * tt) * sw + S['h3'] * np.sin(2 * np.pi * 3 * f * tt)) * env * S['pad'] * (2 / len(S['voices']))
                L[t0:t0 + dl] += x * (1 - pan); R[t0:t0 + dl] += x * (1 + pan)
        pp = S['pluck'] * MOOD_PLUCK[mood]
        if pp > 0:                                        # soft plucks on the beat grid (60 bpm), probability per beat
            for b in range(int(cs)):
                if rng.random() < pp:
                    m = int(rng.choice(ch)) + int(rng.choice(S['poct']))
                    st = max(0, t0 + int((b + rng.uniform(-.02, .05)) * SR)); dd = int(2.4 * SR); t2 = np.arange(dd) / SR
                    f = hz(m); x = (np.sin(2 * np.pi * f * t2) + .3 * np.sin(2 * np.pi * 2 * f * t2) * np.exp(-t2 * 5)) * np.exp(-t2 * S['pdec']) * np.minimum(t2 / .012, 1) * S['pamp']
                    pan = rng.uniform(-.5, .5); e = min(dd, n - st); L[st:st + e] += x[:e] * (1 - pan); R[st:st + e] += x[:e] * (1 + pan)
        if S['arp']:                                      # slow high arpeggio (cosmic): one note every arp s, octave above
            for b_ in range(int(cs / S['arp'])):
                if rng.random() < .7 * MOOD_PLUCK[mood]:
                    m = int(ch[b_ % len(ch)]) + 12
                    st = max(0, t0 + int((b_ * S['arp'] + rng.uniform(-.05, .1)) * SR)); dd = int(4.0 * SR); t2 = np.arange(dd) / SR
                    f = hz(m); x = (np.sin(2 * np.pi * f * t2) + .2 * np.sin(2 * np.pi * 2 * f * t2) * np.exp(-t2 * 4)) * np.exp(-t2 * S['pdec']) * np.minimum(t2 / .02, 1) * S['pamp']
                    pan = rng.uniform(-.7, .7); e = min(dd, n - st); L[st:st + e] += x[:e] * (1 - pan); R[st:st + e] += x[:e] * (1 + pan)
    for ta in accents:                                     # accent plucks on the big transitions (2026-10-24)
        ci = int(ta / cs)
        if ci >= len(order) or ta < 0: continue
        _, prog, k = order[ci]; ch = prog[k]; st = int(ta * SR); dd = int(2.4 * SR); t2 = np.arange(dd) / SR
        for m in (ch[1], ch[2] - 12 if ch[2] > 66 else ch[2]):
            f = hz(m); x = (np.sin(2 * np.pi * f * t2) + .3 * np.sin(2 * np.pi * 2 * f * t2) * np.exp(-t2 * 5)) * np.exp(-t2 * 2.2) * np.minimum(t2 / .012, 1) * .06
            e = min(dd, n - st)
            if e > 0: L[st:st + e] += x[:e]; R[st:st + e] += x[:e]
    if S['echo']:
        for chn in (L, R):
            d1 = int(.43 * SR); d2 = int(.81 * SR)
            chn[d1:] += chn[:-d1] * .32; chn[d2:] += chn[:-d2] * .2
    out = []
    for chn in (L, R):
        chn = sosfilt(butter(2, 250, 'hp', fs=SR, output='sos'), chn)
        chn = sosfilt(butter(2, S['lp'], 'lp', fs=SR, output='sos'), chn)
        out.append(chn[:int(total * SR)])
    return np.stack(out, 1)


def synth_cosmic(total, seed=5): return synth(total, seed, 'cosmic')


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

def make_bgm(path_wav, total, files_starts, below_db=13.0, seed=5, style='default', accents=(), moods=()):
    x = synth(total, seed, style, accents, moods)
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
