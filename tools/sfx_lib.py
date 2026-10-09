# -*- coding: utf-8 -*-
# Synthesised sound effects (no external sources, no licence issues). Run: python3 sfx_lib.py OUTDIR
# All sounds: stereo 48 kHz, high-passed at 140 Hz (no low rumble), peak about -18 dBFS, short fades.
import sys, wave
import numpy as np
SR = 48000
rng = np.random.default_rng(11)

def hp(x, fc=140.0):          # one-pole high-pass, applied twice
    a = np.exp(-2 * np.pi * fc / SR)
    for _ in range(2):
        y = np.zeros_like(x); px = 0.0; py = 0.0
        for n in range(len(x)):
            py = a * (py + x[n] - px); px = x[n]; y[n] = py
        x = y
    return x

def lp(x, fc):
    a = np.exp(-2 * np.pi * fc / SR); y = np.zeros_like(x); py = 0.0
    for n in range(len(x)):
        py = (1 - a) * x[n] + a * py; y[n] = py
    return y

def bp(x, lo, hi): return lp(hp(x, lo), hi)
def t_(d): return np.arange(int(d * SR)) / SR
def env_ad(t, a, d): return np.minimum(t / a, 1) * np.exp(-t / d)
def fade(x, a=0.01, b=0.04):
    n = len(x); fi = int(a * SR); fo = int(b * SR)
    x[:fi] *= np.linspace(0, 1, fi); x[-fo:] *= np.linspace(1, 0, fo); return x
def norm(x, db=-18): return x / (np.max(np.abs(x)) + 1e-9) * 10 ** (db / 20)

def swish():       # short air sweep
    t = t_(0.55); n = bp(rng.standard_normal(len(t)), 600, 5000)
    e = np.sin(np.pi * np.clip(t / 0.55, 0, 1)) ** 2
    return n * e
def shimmer():     # soft sparkle
    t = t_(1.3); x = np.zeros_like(t)
    for f, d0 in [(1568, 0), (2093, .08), (2637, .16), (3136, .26), (3951, .36)]:
        tt = np.clip(t - d0, 0, None); x += np.sin(2 * np.pi * f * tt) * env_ad(tt, .005, .18) * (t >= d0)
    return x
def tick():        # small wooden tick
    t = t_(0.18); return np.sin(2 * np.pi * 900 * t) * np.exp(-t * 60) + bp(rng.standard_normal(len(t)), 1500, 4000) * np.exp(-t * 90) * .5
def crackle():     # fire crackle (random clicks over soft hiss)
    t = t_(2.4); x = bp(rng.standard_normal(len(t)), 800, 3000) * .08
    for _ in range(38):
        p = int(rng.uniform(0, len(t) - 800)); k = rng.integers(60, 400)
        x[p:p + k] += rng.standard_normal(k) * np.exp(-np.arange(k) / (k / 5)) * rng.uniform(.3, 1)
    return x
def bubble():      # boiling water
    t = t_(2.4); x = bp(rng.standard_normal(len(t)), 300, 1800) * .06
    for _ in range(22):
        p = int(rng.uniform(0, len(t) - 6000)); f0 = rng.uniform(350, 900); tt = np.arange(6000) / SR
        x[p:p + 6000] += np.sin(2 * np.pi * (f0 + 900 * tt) * tt) * np.exp(-tt * 45) * rng.uniform(.3, 1)
    return x
def wind():        # gentle wind
    t = t_(2.5); n = bp(rng.standard_normal(len(t)), 200, 1400)
    e = 0.6 + 0.4 * np.sin(2 * np.pi * 0.7 * t + 1) ; return n * e
def bell():        # small bell
    t = t_(2.2); x = sum(np.sin(2 * np.pi * f * t) * np.exp(-t * d) * a for f, d, a in [(880, 2.2, 1), (1320, 3.2, .5), (2210, 4.5, .35), (2960, 6, .2)])
    return x
def click():       # latch / lock click
    t = t_(0.25); return (np.sin(2 * np.pi * 1400 * t) * np.exp(-t * 90) + np.sin(2 * np.pi * 620 * t) * np.exp(-t * 55) * .6 + bp(rng.standard_normal(len(t)), 2000, 6000) * np.exp(-t * 120) * .4)
def creak():       # wood creak
    t = t_(1.0); f = 220 + 90 * np.sin(2 * np.pi * 3.5 * t) + 60 * t
    ph = 2 * np.pi * np.cumsum(f) / SR; x = (np.sign(np.sin(ph)) * .5 + np.sin(ph)) * bp(rng.standard_normal(len(t)), 300, 2500) * 3
    return x * np.sin(np.pi * np.clip(t, 0, 1)) ** 1.5
def drip():        # single water drop
    t = t_(0.5); return np.sin(2 * np.pi * (1100 + 1800 * np.exp(-t * 30)) * t) * np.exp(-t * 22)
def thud():        # soft object set down (kept above 140 Hz)
    t = t_(0.4); return np.sin(2 * np.pi * 190 * t) * np.exp(-t * 28) + bp(rng.standard_normal(len(t)), 300, 1500) * np.exp(-t * 40) * .6
def chime():       # gentle two-note chime
    t = t_(1.6); x = np.zeros_like(t)
    for f, d0 in [(1175, 0), (1568, .22)]:
        tt = np.clip(t - d0, 0, None); x += np.sin(2 * np.pi * f * tt) * np.exp(-tt * 3.2) * (t >= d0)
    return x
def rustle():      # paper / cloth rustle
    t = t_(0.9); n = bp(rng.standard_normal(len(t)), 2000, 7000)
    return n * (np.abs(np.sin(2 * np.pi * 9 * t)) * np.sin(np.pi * np.clip(t / 0.9, 0, 1)))
def pop():         # soft pop
    t = t_(0.2); return np.sin(2 * np.pi * (500 + 700 * np.exp(-t * 40)) * t) * np.exp(-t * 35)

LIB = dict(swish=swish, shimmer=shimmer, tick=tick, crackle=crackle, bubble=bubble, wind=wind, bell=bell, click=click,
           creak=creak, drip=drip, thud=thud, chime=chime, rustle=rustle, pop=pop)

def write(path, x):
    st = np.stack([x, x], 1)
    with wave.open(path, 'wb') as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((st * 32767).astype('<i2').tobytes())

def make_all(out):
    import os; os.makedirs(out, exist_ok=True)
    for name, fn in LIB.items():
        x = fn().astype(np.float64); x = hp(x); x = fade(x); x = norm(x, -18); write(f'{out}/sfx_{name}.wav', x)
    return list(LIB)

if __name__ == '__main__':
    print(make_all(sys.argv[1]))


def make_chalk(path):    # chalk tap for the chalkboard scenes (noise burst, peak -22 dBFS)
    n = int(0.38 * SR); rng = np.random.default_rng(7)
    x = np.diff(rng.standard_normal(n), prepend=0); x = np.convolve(x, np.ones(3) / 3, 'same')
    t = np.arange(n) / SR
    env = np.minimum(t / 0.01, 1) * np.exp(-t * 9) * (0.6 + 0.4 * np.sin(2 * np.pi * 38 * t) ** 2)
    write(path, norm(x * env, -22))
