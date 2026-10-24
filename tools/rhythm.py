# -*- coding: utf-8 -*-
# Rhythm helpers for build3.py (2026-10-24, guideline 9-5): near-silences and accent times.
#   silence_windows(...)  -> [(a, b)] seconds where the background music and the sound effects are muted (narration stays)
#   accent_times(units, TIN) -> times of the big picture changes (scene changes with a real transition); bgm_lib adds chord-tone accents there
#   gain_mask(n, sr, windows) -> numpy gain curve (1 outside, 0 inside, 0.15 s soft edges)
import numpy as np


def silence_windows(cfg, sel, starts, D, gap, total, tail):
    """Two near-silences per video (DIRECTOR.md 6: at least two): (1) before one scene change, from 1.2 s before the narrator stops to 0.4 s
    before the next scene starts, so the first sound after it (the transition swish) lands as an event; (2) the end: from 0.3 s after the last
    word to the end. config.py `SILENCE = [scene numbers]` picks the scenes to be preceded by a silence (`[]` = only the end); without it one
    is chosen at about 60 % of the video."""
    wins = []
    pick = getattr(cfg, 'SILENCE', None)
    if pick is None and len(sel) >= 4: pick = [sel[int(len(sel) * .6)]]
    for i in (pick or []):
        if i not in starts or i == sel[0]: continue
        k = sel.index(i); prev = sel[k - 1]
        a = starts[prev] + D[prev - 1] - 1.2; b = starts[i] - 0.4
        if b - a > .5: wins.append((a, b))
    last = sel[-1]; a = starts[last] + D[last - 1] + 0.3
    if total - a > .6: wins.append((a, total))
    return wins


def accent_times(units, TIN):
    """picture changes that deserve a musical accent: the first unit of each new scene (not hard cuts, not chalkboards); the accent sits in the middle of the transition"""
    out = []; prev = None
    for u in units:
        if prev is not None and u['kind'] != 'chalk' and prev['kind'] != 'chalk' and u['scene'] != prev['scene'] and TIN.get(u['tr'], 0) > 0:
            out.append(round(u['t0'] - TIN[u['tr']] / 2, 3))
        prev = u
    return out


def gain_mask(n, sr, windows, edge=.15):
    m = np.ones(n, dtype=np.float32); e = max(int(edge * sr), 1)
    for a, b in windows:
        i0, i1 = max(int(a * sr), 0), min(int(b * sr), n)
        if i1 <= i0: continue
        m[i0:i1] = 0
        j0 = max(i0 - e, 0); m[j0:i0] = np.minimum(m[j0:i0], np.linspace(1, 0, i0 - j0, dtype=np.float32))
        j1 = min(i1 + e, n); m[i1:j1] = np.minimum(m[i1:j1], np.linspace(0, 1, j1 - i1, dtype=np.float32))
    return m
