# -*- coding: utf-8 -*-
# Synthesised sound effects (no external sources, no licence issues). Run: python3 sfx_lib.py OUTDIR
# v2 (2026-10-10): quieter (peak -24 dBFS), no ringing/pitched sounds (bell, chime, shimmer are now soft noise or
# dull wooden sounds), more kinds, 3 variants per sound (sfx_<name>.wav, sfx_<name>_2.wav, sfx_<name>_3.wav).
# All sounds: stereo 48 kHz, high-passed at 150 Hz (no low rumble), short fades.
import sys, wave
import numpy as np
from scipy.signal import butter, sosfilt
SR = 48000
rng = np.random.default_rng(11)
PEAK_DB = -24

def hp(x, fc=150.0): return sosfilt(butter(2, fc, 'hp', fs=SR, output='sos'), x)
def lp(x, fc): return sosfilt(butter(2, fc, 'lp', fs=SR, output='sos'), x)
def bp(x, lo, hi): return lp(hp(x, lo), hi)
def t_(d): return np.arange(int(d * SR)) / SR
def noise(t): return rng.standard_normal(len(t))
def fade(x, a=0.01, b=0.05):
    fi = int(a * SR); fo = int(b * SR)
    x[:fi] *= np.linspace(0, 1, fi); x[-fo:] *= np.linspace(1, 0, fo); return x
def norm(x, db=PEAK_DB): return x / (np.max(np.abs(x)) + 1e-9) * 10 ** (db / 20)
def swell(t, d): return np.sin(np.pi * np.clip(t / d, 0, 1)) ** 2
def burst(n, k, decay):      # decaying noise burst of k samples placed in a buffer of n
    b = np.zeros(n); b[:k] = rng.standard_normal(k) * np.exp(-np.arange(k) / (k / decay)); return b

def swish():       # soft air sweep, band-limited
    t = t_(0.6); return bp(noise(t), 500, 3200) * swell(t, 0.6)
def hush():        # airy swell for shape-matching transitions (was 'shimmer'; no pitch)
    t = t_(1.0); n = bp(noise(t), 2500, 7000); return n * swell(t, 1.0) ** 1.5 * 0.7
def tick():        # small dull wooden tick
    t = t_(0.14); return lp(bp(noise(t), 500, 2500) * np.exp(-t * 80) + np.sin(2 * np.pi * 700 * t) * np.exp(-t * 90) * .5, 2600)
def crackle():     # soft fire crackle
    t = t_(2.4); x = bp(noise(t), 800, 2800) * .06
    for _ in range(30):
        p = int(rng.uniform(0, len(t) - 800)); k = int(rng.integers(60, 360))
        x[p:p + k] += rng.standard_normal(k) * np.exp(-np.arange(k) / (k / 5)) * rng.uniform(.2, .9)
    return lp(x, 4000)
def bubble():      # simmering water, soft
    t = t_(2.4); x = bp(noise(t), 300, 1500) * .05
    for _ in range(16):
        p = int(rng.uniform(0, len(t) - 4000)); f0 = rng.uniform(300, 600); tt = np.arange(3000) / SR
        x[p:p + 3000] += np.sin(2 * np.pi * (f0 + 500 * tt) * tt) * np.exp(-tt * 70) * rng.uniform(.2, .6)
    return lp(x, 2200)
def wind():        # gentle wind
    t = t_(2.6); n = bp(noise(t), 200, 1200); return n * (0.6 + 0.4 * np.sin(2 * np.pi * 0.55 * t + rng.uniform(0, 6)))
def bell():        # (old name) dull wooden knock instead of a ringing bell
    t = t_(0.5); return lp(np.sin(2 * np.pi * 330 * t) * np.exp(-t * 22) + bp(noise(t), 400, 1800) * np.exp(-t * 45) * .7, 1800)
def click():       # latch / lock click
    t = t_(0.2); return lp(bp(noise(t), 1000, 5000) * np.exp(-t * 110) + bp(noise(t), 400, 1200) * np.exp(-t * 60) * .6, 5000)
def creak():       # wood creak
    t = t_(1.0); f = 220 + 90 * np.sin(2 * np.pi * 3.5 * t) + 60 * t
    ph = 2 * np.pi * np.cumsum(f) / SR; x = (np.sign(np.sin(ph)) * .5 + np.sin(ph)) * bp(noise(t), 300, 2000) * 3
    return lp(x * swell(t, 1.0) ** .75, 2500)
def drip():        # single water drop, muted
    t = t_(0.35); return lp(np.sin(2 * np.pi * (900 + 1200 * np.exp(-t * 35)) * t) * np.exp(-t * 28), 2000)
def thud():        # soft object set down (above 150 Hz)
    t = t_(0.35); return lp(np.sin(2 * np.pi * 200 * t) * np.exp(-t * 32) + bp(noise(t), 300, 1200) * np.exp(-t * 45) * .6, 1500)
def chime():       # (old name) two soft paper flicks instead of a chime
    t = t_(0.7); x = np.zeros(len(t))
    for d0 in (0.0, 0.2):
        k = int(0.12 * SR); p = int(d0 * SR); x[p:p + k] += bp(rng.standard_normal(k), 1800, 6000) * np.exp(-np.arange(k) / (k / 5))
    return x
def rustle():      # paper / cloth rustle
    t = t_(0.9); n = bp(noise(t), 1800, 6500)
    return n * (np.abs(np.sin(2 * np.pi * rng.uniform(7, 11) * t)) * swell(t, 0.9))
def pop():         # soft pop
    t = t_(0.14); return lp(np.sin(2 * np.pi * (420 + 500 * np.exp(-t * 50)) * t) * np.exp(-t * 45), 1800)
# --- new in v2 ---
def pencil():      # pencil scratch on paper
    t = t_(0.9); x = bp(noise(t), 2500, 7500)
    return x * (np.abs(np.sin(2 * np.pi * rng.uniform(5, 8) * t)) ** 2) * swell(t, 0.9) ** .7
def page():        # page turn
    t = t_(0.8); return bp(noise(t), 1200, 5500) * np.minimum(t / 0.05, 1) * np.exp(-t * 4) * (0.7 + 0.3 * np.sin(2 * np.pi * 14 * t))
def cloth():       # cloth movement
    t = t_(0.9); return bp(noise(t), 300, 2200) * swell(t, 0.9) * (0.6 + 0.4 * np.sin(2 * np.pi * 5 * t + 1))
def woodblock():   # soft wood tap
    t = t_(0.25); return lp(np.sin(2 * np.pi * 480 * t) * np.exp(-t * 40) + bp(noise(t), 600, 2500) * np.exp(-t * 80) * .5, 2400)
def sand():        # grains pouring
    t = t_(1.6); x = bp(noise(t), 2000, 8000) * .5
    return x * (0.6 + 0.4 * np.abs(noise(t[::480]).repeat(480)[:len(t)])) * swell(t, 1.6) ** .6
def rain():        # light rain on a surface
    t = t_(2.4); x = bp(noise(t), 1500, 9000) * .25
    for _ in range(60):
        p = int(rng.uniform(0, len(t) - 500)); k = int(rng.integers(80, 400))
        x[p:p + k] += bp(rng.standard_normal(k), 1500, 6000) * np.exp(-np.arange(k) / (k / 6)) * rng.uniform(.3, 1)
    return x * (0.5 + 0.5 * swell(t, 2.4) ** .5)
def splash():      # small water splash
    t = t_(0.6); return bp(noise(t), 700, 4500) * np.minimum(t / 0.01, 1) * np.exp(-t * 9) * (0.6 + 0.4 * np.abs(np.sin(2 * np.pi * 20 * t)))
def step():        # soft footstep
    t = t_(0.3); return lp(bp(noise(t), 200, 900) * np.exp(-t * 28), 1000) + lp(noise(t) * np.exp(-t * 90), 3000) * .3
def breath():      # quiet breath-like air
    t = t_(1.4); return bp(noise(t), 600, 3500) * swell(t, 1.4) ** 1.3
def stone():       # dull stone knock
    t = t_(0.3); return lp(bp(noise(t), 500, 2200) * np.exp(-t * 60) + np.sin(2 * np.pi * 260 * t) * np.exp(-t * 50) * .5, 2200)
def flutter():     # wings / cloth flutter
    t = t_(0.8); return bp(noise(t), 500, 3000) * (np.abs(np.sin(2 * np.pi * 11 * t)) ** 1.5) * swell(t, 0.8)


# ---- cosmic family (space videos): filtered noise only, no pitch. Still high-passed at 150 Hz and peak -24 dBFS. ----
def riser():       # slow rising air swell (band moves up) -- builds towards a reveal
    t = t_(2.2); n = noise(t); k = 3; out = np.zeros(len(t)); edges = np.geomspace(500, 7500, k + 1)
    for i in range(k):
        seg = bp(n, edges[i], edges[i + 1]) * np.clip((t - i * .55) / .9, 0, 1) * (1 - 0.0 * i)
        out += seg
    return out * (t / t[-1]) ** 2.2 * np.minimum((t[-1] - t) / .12, 1)
def sparkle():     # sparse bright grains (high noise ticks), like starlight
    t = t_(1.3); out = np.zeros(len(t))
    for _ in range(22):
        st = int(rng.uniform(0, .95) * SR); k = int(rng.uniform(.004, .012) * SR)
        b = bp(rng.standard_normal(k) * np.exp(-np.arange(k) / (k / 4)), 4500, 11000)
        out[st:st + k] += b[:len(out) - st] * rng.uniform(.3, 1)
    return out * np.exp(-t * 1.6)
def sweep():       # long airy pass-by (bandpass slides down)
    t = t_(2.0); n = noise(t); a = bp(n, 1800, 6500) * swell(t, 2.0); b = bp(n, 600, 2200) * np.clip(t / 2.0, 0, 1) ** .5 * swell(t, 2.0)
    return a * np.exp(-t * .3) * .8 + b * .4
def bloom():       # soft expanding burst, e.g. a flare or a star appearing (noise swell, quick attack, long tail)
    t = t_(1.5); return bp(noise(t), 300, 5000) * np.minimum(t / .06, 1) * np.exp(-t * 3.2)
def starfall():    # descending shimmer of noise (falling meteor trail)
    t = t_(1.2); n = noise(t); hi = bp(n, 3500, 9000) * np.exp(-t * 2.2); lo = bp(n, 800, 2600) * np.clip(t / .5, 0, 1) * np.exp(-t * 3)
    return (hi * np.clip(1 - t / 1.2, 0, 1) + lo * .6) * np.minimum(t / .02, 1)
def pulse():       # one soft rounded air pulse (distant signal), above 150 Hz
    t = t_(0.5); return lp(bp(noise(t), 320, 1800), 1800) * np.minimum(t / .03, 1) * np.exp(-t * 9)
def warp():        # fast rise then soft release (travelling between places)
    t = t_(1.0); n = noise(t); up = bp(n, 700, 6000) * np.clip(t / .55, 0, 1) ** 2 * (t < .55)
    dn = bp(n, 400, 3000) * np.exp(-(t - .55) * 7) * (t >= .55); return up + dn * .7
def glimmer():     # very quiet cluster of soft high grains (light twinkle, ambient)
    t = t_(1.0); out = np.zeros(len(t))
    for _ in range(9):
        st = int(rng.uniform(0, .8) * SR); k = int(rng.uniform(.006, .015) * SR)
        b = bp(rng.standard_normal(k) * np.exp(-np.arange(k) / (k / 3)), 5500, 12000); out[st:st + k] += b[:len(out) - st] * rng.uniform(.3, .8)
    return out
COSMIC = dict(riser=riser, sparkle=sparkle, sweep=sweep, bloom=bloom, starfall=starfall, pulse=pulse, warp=warp, glimmer=glimmer)

LIB = dict(swish=swish, hush=hush, tick=tick, crackle=crackle, bubble=bubble, wind=wind, bell=bell, click=click,
           creak=creak, drip=drip, thud=thud, chime=chime, rustle=rustle, pop=pop, pencil=pencil, page=page, cloth=cloth,
           woodblock=woodblock, sand=sand, rain=rain, splash=splash, step=step, breath=breath, stone=stone, flutter=flutter)
LIB.update(COSMIC)
ALIAS = {'shimmer': 'hush'}          # old name used by existing sidecars/plans
VARIANTS = 3

def write(path, x):
    st = np.stack([x, x], 1)
    with wave.open(path, 'wb') as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((np.clip(st, -1, 1) * 32767).astype('<i2').tobytes())

def make_all(out):
    global rng
    import os; os.makedirs(out, exist_ok=True)
    for name, fn in LIB.items():
        for v in range(1, VARIANTS + 1):
            rng = np.random.default_rng(1000 * v + sum(map(ord, name)))
            x = fn().astype(np.float64); x = hp(x); x = fade(x); x = norm(x)
            write(f'{out}/sfx_{name}{"" if v == 1 else "_" + str(v)}.wav', x)
    return list(LIB)

def make_chalk(path):    # chalk tap for the chalkboard scenes (noise burst, peak -26 dBFS)
    global rng
    rng = np.random.default_rng(7); n = int(0.38 * SR)
    x = np.diff(rng.standard_normal(n), prepend=0); x = np.convolve(x, np.ones(3) / 3, 'same')
    t = np.arange(n) / SR
    env = np.minimum(t / 0.01, 1) * np.exp(-t * 9) * (0.6 + 0.4 * np.sin(2 * np.pi * 38 * t) ** 2)
    write(path, norm(x * env, -26))

if __name__ == '__main__':
    print(make_all(sys.argv[1]))
