# -*- coding: utf-8 -*-
# Synthesised sound effects (no external sources, no licence issues). Run: python3 sfx_lib.py OUTDIR
# v3 (2026-10-27): +61 kinds below (92 in all), chosen automatically by tools/sfx_pick.py.
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
def trim(x, keep=0.12):        # drop trailing silence left by _seq padding (keep 0.12 s)
    nz = np.flatnonzero(np.abs(x) > 1e-4); return x if not len(nz) else x[:min(len(x), nz[-1] + int(keep * SR))]
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
def warp():        # very short sharp air flick (no slow swell -> not wave-like)
    t = t_(0.28); return bp(noise(t), 1500, 7000) * np.minimum(t / .008, 1) * np.exp(-t * 16)
def glimmer():     # very quiet cluster of soft high grains (light twinkle, ambient)
    t = t_(1.0); out = np.zeros(len(t))
    for _ in range(9):
        st = int(rng.uniform(0, .8) * SR); k = int(rng.uniform(.006, .015) * SR)
        b = bp(rng.standard_normal(k) * np.exp(-np.arange(k) / (k / 3)), 5500, 12000); out[st:st + k] += b[:len(out) - st] * rng.uniform(.3, .8)
    return out
COSMIC = dict(sparkle=sparkle, bloom=bloom, starfall=starfall, pulse=pulse, warp=warp, glimmer=glimmer)   # riser/sweep removed 2026-10-12: slow noise swells sounded like waves

LIB = dict(swish=swish, hush=hush, tick=tick, crackle=crackle, bubble=bubble, wind=wind, bell=bell, click=click,
           creak=creak, drip=drip, thud=thud, chime=chime, rustle=rustle, pop=pop, pencil=pencil, page=page, cloth=cloth,
           woodblock=woodblock, sand=sand, rain=rain, splash=splash, step=step, breath=breath, stone=stone, flutter=flutter)
LIB.update(COSMIC)
# ---- v3 (2026-10-27, miya: "more sound effects, picked automatically from the script"): 60 more kinds. Same rules: filtered noise and
# short dull knocks only, no ringing pitch, high-passed 150 Hz, peak -24 dBFS. Picked by tools/sfx_pick.py (word rules + palette ambient). ----
def _knock(f0, dec, nz=(400, 1800), nzdec=45, d=0.3, mix=.7):
    t = t_(d); return lp(np.sin(2 * np.pi * f0 * t) * np.exp(-t * dec) + bp(noise(t), *nz) * np.exp(-t * nzdec) * mix, max(nz[1], 1600))
def _grains(d, n, lo, hi, kmin, kmax, decay=5, env=None):
    t = t_(d); out = np.zeros(len(t))
    for _ in range(n):
        st = int(rng.uniform(0, max(d - kmax, .01)) * SR); k = int(rng.uniform(kmin, kmax) * SR)
        out[st:st + k] += bp(rng.standard_normal(k) * np.exp(-np.arange(k) / (k / decay)), lo, hi)[:len(out) - st] * rng.uniform(.3, 1)
    return out if env is None else out * env(t)
def _seq(parts, gaps):          # place short sounds one after another (gaps in s)
    n = int((sum(gaps) + 1.2) * SR); out = np.zeros(n); p = 0
    for x, g in zip(parts, gaps):
        p += int(g * SR); e = min(len(x), n - p); out[p:p + e] += x[:e]
    return out
# nature
def waves():       # one slow wave roll (band noise, soft rise and fall, 2.8 s)
    t = t_(2.8); n = bp(noise(t), 250, 2600); return n * swell(t, 2.8) ** 1.4 * (0.7 + 0.3 * np.sin(2 * np.pi * 0.9 * t))
def shore():       # foam hissing back over sand after a wave
    t = t_(2.2); return bp(noise(t), 1500, 7000) * np.minimum(t / .3, 1) * np.exp(-t * 1.4) * (0.7 + 0.3 * np.abs(noise(t[::600]).repeat(600)[:len(t)]))
def stream():      # small brook: bubbly mid noise with trickle grains
    t = t_(2.4); return bp(noise(t), 500, 3500) * .35 * (0.7 + 0.3 * np.sin(2 * np.pi * 1.3 * t)) + _grains(2.4, 40, 1500, 5000, .01, .04)
def thunder():     # distant thunder: a soft crack then a rolling tail (all above 150 Hz, no rumble)
    t = t_(2.6); crack = bp(noise(t), 300, 2500) * np.minimum(t / .02, 1) * np.exp(-t * 6)
    roll = bp(noise(t), 160, 700) * np.clip(t / .4, 0, 1) * np.exp(-t * 1.3) * (0.6 + 0.4 * np.abs(np.sin(2 * np.pi * 2.3 * t)))
    return crack + roll * .8
def leaves():      # leaves stirring in a breeze
    t = t_(2.0); return bp(noise(t), 1200, 6500) * (0.4 + 0.6 * np.abs(np.sin(2 * np.pi * rng.uniform(1.5, 2.5) * t)) ** 1.5) * swell(t, 2.0) ** .6
def cricket():     # night crickets: fast high chirps in groups (noise, not a tone)
    t = t_(2.2); car = bp(noise(t), 3800, 6500); g = (np.sin(2 * np.pi * 28 * t) > .3).astype(float) * (np.sin(2 * np.pi * 1.6 * t) > -.2)
    return car * g * .8 * swell(t, 2.2) ** .5
def cicada():      # summer cicada: rattling high noise with a slow rise and fall
    t = t_(2.4); car = bp(noise(t), 3000, 7500); g = 0.5 + 0.5 * np.sign(np.sin(2 * np.pi * 95 * t)); return car * g * swell(t, 2.4) ** .8
def buzz():        # insect passing by: rough mid buzz (amplitude-modulated noise, not a sawtooth)
    t = t_(1.4); car = bp(noise(t), 180, 900); g = 0.55 + 0.45 * np.sign(np.sin(2 * np.pi * 160 * t)); return car * g * swell(t, 1.4) ** 1.2
def snowstep():    # footsteps on snow: crunchy grains, two steps
    a = _grains(.35, 25, 1500, 7000, .003, .01, env=lambda t: np.exp(-t * 9)); return _seq([a, a * .8], [0.0, .45])
def icecrack():    # ice cracking: sharp snap then tiny ticks
    t = t_(1.0); x = bp(noise(t), 1200, 7000) * np.minimum(t / .003, 1) * np.exp(-t * 40)
    return x + _grains(1.0, 12, 2000, 8000, .002, .006, env=lambda t: np.exp(-t * 2.5)) * .5
def gust():        # a gust of wind passing (faster than wind)
    t = t_(1.6); return bp(noise(t), 300, 2200) * swell(t, 1.6) ** 2 * (0.8 + 0.2 * np.sin(2 * np.pi * 3 * t))
def whoosh():      # fast whoosh (flame, cape, something large passing)
    t = t_(0.7); return bp(noise(t), 400, 4500) * swell(t, 0.7) ** 3
def crumble():     # earth or stone crumbling, grains falling
    t = t_(1.6); return _grains(1.6, 70, 600, 4000, .005, .03, env=lambda t: swell(t, 1.6) ** .5) + bp(noise(t), 200, 1200) * np.exp(-t * 2.5) * .4
def gravel():      # footsteps on gravel, two steps
    a = _grains(.3, 30, 800, 5000, .003, .012, env=lambda t: np.exp(-t * 12)); return _seq([a, a * .85], [0.0, .5])
def dig():         # shovel into soil: scrape then a soft soil thud
    t = t_(0.9); sc = bp(noise(t), 1000, 5000) * np.minimum(t / .02, 1) * np.exp(-t * 9); th = lp(bp(noise(t), 200, 900), 900) * np.clip((t - .25) / .01, 0, 1) * np.exp(-(t - .25) * 25)
    return sc * .6 + th
def dust():        # a puff of dust settling (softer, airier than sand)
    t = t_(1.3); return bp(noise(t), 1500, 7000) * np.minimum(t / .05, 1) * np.exp(-t * 2.4) * .8
def ash():         # ash and embers drifting: very sparse faint crackles
    return _grains(2.2, 10, 1500, 5000, .004, .02, decay=4, env=lambda t: swell(t, 2.2) ** .5) * .7
def candle():      # candle flame flicker: soft airy wobble with a few tiny crackles
    t = t_(1.8); return bp(noise(t), 800, 3500) * .35 * (0.6 + 0.4 * np.abs(np.sin(2 * np.pi * 6.5 * t))) * swell(t, 1.8) ** .6 + _grains(1.8, 6, 2000, 6000, .003, .008) * .5
def hiss():        # steady hiss (snake, gas, air leak)
    t = t_(1.1); return bp(noise(t), 2500, 9000) * swell(t, 1.1) ** .8
def steam():       # steam burst: strong hiss with quick attack
    t = t_(1.3); return bp(noise(t), 1800, 8000) * np.minimum(t / .04, 1) * np.exp(-t * 2.2)
def slosh():       # liquid sloshing in a container
    t = t_(1.0); return bp(noise(t), 300, 2000) * (0.5 + 0.5 * np.abs(np.sin(2 * np.pi * 2.2 * t))) ** 2 * swell(t, 1.0) ** .7
# objects, hands, rooms
def knock():       # two knocks on wood
    a = _knock(240, 30, (300, 1500), 50, .25); return _seq([a, a * .9], [0.0, .32])
def door():        # door: short creak then a latch
    t = t_(0.9); f = 180 + 60 * np.sin(2 * np.pi * 4 * t); ph = 2 * np.pi * np.cumsum(f) / SR
    cr = (np.sign(np.sin(ph)) * .4 + np.sin(ph)) * bp(noise(t), 300, 1800) * 2.5 * swell(t, .55) ** .8 * (t < .55)
    la = lp(bp(noise(t), 800, 4000), 4000) * np.clip((t - .6) / .003, 0, 1) * np.exp(-(t - .6) * 90)
    return lp(cr, 2500) * .6 + la
def coins():       # a few coins dropping on a table (dull metal clinks)
    parts = [_knock(rng.uniform(1900, 2600), 60, (2500, 6000), 70, .15, .4) for _ in range(5)]; return _seq(parts, [0.0, .09, .14, .07, .2])
def clink():       # one dull metal clink (cup, tool, ring)
    return _knock(2200, 55, (2000, 6500), 60, .2, .5)
def keys():        # keys jingling
    return _grains(.9, 24, 2500, 8000, .004, .015, decay=4, env=lambda t: swell(t, .9) ** .6)
def zipper():      # zipper: fast ratchet of tiny clicks
    t = t_(0.5); g = (np.sin(2 * np.pi * 110 * (1 + 1.2 * t) * t) > .6).astype(float); return bp(noise(t), 1500, 6000) * g * swell(t, .5) ** .5
def typing():      # typing on a keyboard: 8 soft key clicks
    parts = [_knock(rng.uniform(600, 900), 80, (1500, 6000), 110, .08, .9) for _ in range(8)]; return _seq(parts, [0.0] + list(rng.uniform(.07, .16, 7)))
def typewriter():  # typewriter: harder clicks with a small ring-free thock
    parts = [_knock(rng.uniform(400, 600), 60, (1200, 5500), 80, .1, 1.0) for _ in range(6)]; return _seq(parts, [0.0] + list(rng.uniform(.12, .22, 5)))
def heartbeat():   # two soft heart thumps (above 150 Hz, rounded)
    a = lp(np.sin(2 * np.pi * 175 * t_(.25)) * np.exp(-t_(.25) * 26) + bp(noise(t_(.25)), 160, 500) * np.exp(-t_(.25) * 30) * .4, 500)
    return _seq([a, a * .75], [0.0, .28])
def crunch():      # a bite / crunch (apple, leaf, bone-free)
    t = t_(0.35); return _grains(.35, 25, 800, 6000, .003, .012, env=lambda t: np.exp(-t * 10)) + bp(noise(t), 400, 2500) * np.minimum(t / .005, 1) * np.exp(-t * 30) * .6
def sizzle():      # frying / sizzling
    t = t_(2.0); return bp(noise(t), 2000, 9000) * .3 * (0.7 + 0.3 * np.abs(noise(t[::300]).repeat(300)[:len(t)])) * swell(t, 2.0) ** .4 + _grains(2.0, 50, 2500, 8000, .002, .006) * .4
def chop():        # knife on a board: three chops
    a = _knock(300, 50, (500, 3500), 70, .14, 1.0); return _seq([a, a, a], [0.0, .3, .3])
def pour():        # liquid pouring into a glass
    t = t_(1.6); return bp(noise(t), 500, 4000) * swell(t, 1.6) ** .7 * (0.75 + 0.25 * np.sin(2 * np.pi * 9 * t)) + _grains(1.6, 24, 1200, 4500, .008, .03) * .4
def cork():        # cork pop (softer and rounder than pop)
    t = t_(0.25); return lp(np.sin(2 * np.pi * (260 + 300 * np.exp(-t * 40)) * t) * np.exp(-t * 30) + bp(noise(t), 600, 3000) * np.exp(-t * 60) * .5, 2200)
def tear():        # paper tearing
    t = t_(0.7); return bp(noise(t), 1500, 7500) * np.minimum(t / .03, 1) * (0.6 + 0.4 * np.abs(np.sin(2 * np.pi * 40 * t))) * np.exp(-t * 2.5)
def stamp():       # rubber stamp / seal pressed down: thud + tap
    t = t_(0.4); return _knock(190, 30, (300, 1500), 40, .4) + lp(bp(noise(t), 1500, 5000), 5000) * np.clip((t - .08) / .003, 0, 1) * np.exp(-(t - .08) * 100) * .5
def gavel():       # gavel / mallet: one firm wooden knock
    return _knock(360, 36, (500, 2800), 60, .35, .8)
def switch():      # light switch / button
    t = t_(0.15); return lp(bp(noise(t), 1500, 6000) * np.exp(-t * 150) + bp(noise(t), 500, 1500) * np.clip((t - .03) / .002, 0, 1) * np.exp(-(t - .03) * 120) * .8, 6000)
def shutter():     # camera shutter: two very short clicks
    a = lp(bp(noise(t_(.06)), 1500, 7000) * np.exp(-t_(.06) * 160), 7000); return _seq([a, a * .8], [0.0, .07])
def static():      # radio static burst
    t = t_(0.9); return bp(noise(t), 1000, 7000) * (0.5 + 0.5 * np.abs(noise(t[::200]).repeat(200)[:len(t)])) * swell(t, .9) ** .5
def radio():       # old radio: static with a few soft pulses (unpitched)
    t = t_(1.6); st = bp(noise(t), 800, 5000) * .35 * swell(t, 1.6) ** .4
    return st + _grains(1.6, 6, 400, 1500, .03, .08, decay=3) * .9
def steps():       # four walking footsteps
    a = step(); return _seq([a, a * .9, a * .95, a * .85], [0.0, .5, .5, .5])
def hooves():      # horse hooves: gallop groups of dull knocks
    a = _knock(230, 40, (300, 1500), 60, .14, .6); return _seq([a, a * .8, a * .9, a * .7, a, a * .8, a * .9, a * .7], [0.0, .13, .13, .3, .13, .13, .3, .13])
def march():       # marching: heavy even steps
    a = lp(bp(noise(t_(.3)), 200, 900) * np.exp(-t_(.3) * 22), 900) + _knock(180, 25, (250, 900), 40, .3, .3) * .5; return _seq([a, a, a, a], [0.0, .55, .55, .55])
def scrape():      # stone or metal scraping
    t = t_(0.9); return bp(noise(t), 700, 4500) * swell(t, .9) ** .8 * (0.7 + 0.3 * np.abs(np.sin(2 * np.pi * 30 * t)))
def chain():       # chain links moving
    return _grains(1.0, 18, 1800, 6500, .005, .02, decay=4, env=lambda t: swell(t, 1.0) ** .5) + np.pad(_knock(900, 40, (1500, 5000), 60, .3, .7), (0, SR - int(.3 * SR))) * .3
def arrow():       # fast short whizz (arrow, dart, something flying past)
    t = t_(0.35); return bp(noise(t), 1200, 7000) * swell(t, .35) ** 3
def scroll():      # a scroll or map unrolling: long paper slide
    t = t_(1.3); return bp(noise(t), 1000, 5000) * swell(t, 1.3) ** .5 * (0.8 + 0.2 * np.sin(2 * np.pi * 7 * t))
def quill():       # quill / pen writing: lighter scratches than pencil, with pauses
    t = t_(1.2); g = (np.sin(2 * np.pi * 2.2 * t) > -.3).astype(float); return bp(noise(t), 3000, 9000) * (np.abs(np.sin(2 * np.pi * 9 * t)) ** 1.5) * g * swell(t, 1.2) ** .5
def match():       # striking a match: scrape then a soft flare of air
    t = t_(1.0); sc = bp(noise(t), 1500, 7000) * np.minimum(t / .01, 1) * np.exp(-t * 18); fl = bp(noise(t), 500, 3000) * np.clip((t - .12) / .05, 0, 1) * np.exp(-(t - .12) * 4)
    return sc + fl * .7
def thrust():      # engine / rocket thrust: rough broadband roar with a fast attack (above 150 Hz, no slow wave-like swell)
    t = t_(2.0); car = bp(noise(t), 160, 4000); g = 0.7 + 0.3 * np.abs(noise(t[::96]).repeat(96)[:len(t)]); return car * g * np.minimum(t / .15, 1) * np.exp(-t * 1.1)
def impact():      # soft impact / collision (harder than thud, no pitch)
    t = t_(0.4); return bp(noise(t), 200, 1800) * np.minimum(t / .004, 1) * np.exp(-t * 22) + bp(noise(t), 1500, 6000) * np.exp(-t * 60) * .5
def crack():       # a branch or shell cracking
    t = t_(0.3); return bp(noise(t), 800, 6000) * np.minimum(t / .002, 1) * np.exp(-t * 45) + _grains(.3, 5, 2000, 7000, .002, .005) * .5
def snap():        # finger snap / small snap
    t = t_(0.12); return lp(bp(noise(t), 1800, 7000) * np.exp(-t * 120) + bp(noise(t), 600, 2000) * np.exp(-t * 80) * .5, 7000)
def wingbeat():    # large slow wing beats (3), softer and slower than flutter
    t = t_(0.5); a = bp(noise(t), 300, 2000) * swell(t, .5) ** 2; return _seq([a, a * .9, a * .8], [0.0, .55, .55])
def clock():       # clock tick-tock (two dull ticks, 1 s apart) -- time passing
    a = _knock(1100, 90, (1500, 5000), 120, .08, .8); b = _knock(850, 90, (1200, 4500), 120, .08, .8); return _seq([a, b, a], [0.0, .5, .5])
def gear():        # gears / ratchet turning: regular small clicks slowing down
    parts = [_knock(rng.uniform(1200, 1800), 90, (1800, 6000), 120, .06, .9) for _ in range(9)]; return _seq(parts, [0.0] + [.07 + .015 * i for i in range(8)])
def pump():        # bellows / pump: two airy pushes
    t = t_(0.6); a = bp(noise(t), 400, 2500) * swell(t, .6) ** 1.5; return _seq([a, a * .9], [0.0, .7])
def bookclose():   # a book closing: page rustle then a soft thump
    t = t_(0.6); ru = bp(noise(t), 1500, 6000) * swell(t, .3) ** .8 * (t < .3); th = _knock(170, 28, (250, 1200), 40, .6, .5)[:len(t)] * np.clip((t - .28) / .005, 0, 1)
    return ru * .6 + th
def bubbleup():    # one bubble rising (single soft blip, falling-free)
    t = t_(0.3); return lp(np.sin(2 * np.pi * (380 + 420 * t) * t) * np.exp(-t * 18), 1800) * np.minimum(t / .01, 1)

LIB.update(dict(waves=waves, shore=shore, stream=stream, thunder=thunder, leaves=leaves, cricket=cricket, cicada=cicada, buzz=buzz, snowstep=snowstep,
                icecrack=icecrack, gust=gust, whoosh=whoosh, crumble=crumble, gravel=gravel, dig=dig, dust=dust, ash=ash, candle=candle, hiss=hiss,
                steam=steam, slosh=slosh, knock=knock, door=door, coins=coins, clink=clink, keys=keys, zipper=zipper, typing=typing, typewriter=typewriter,
                heartbeat=heartbeat, crunch=crunch, sizzle=sizzle, chop=chop, pour=pour, cork=cork, tear=tear, stamp=stamp, gavel=gavel, switch=switch,
                shutter=shutter, static=static, radio=radio, steps=steps, hooves=hooves, march=march, scrape=scrape, chain=chain, arrow=arrow, scroll=scroll,
                quill=quill, match=match, thrust=thrust, impact=impact, crack=crack, snap=snap, wingbeat=wingbeat, clock=clock, gear=gear, pump=pump,
                bookclose=bookclose, bubbleup=bubbleup))
V3 = set(LIB) - set('swish hush tick crackle bubble wind bell click creak drip thud chime rustle pop pencil page cloth woodblock sand rain splash step breath stone flutter'.split()) - set(COSMIC)

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
            x = fn().astype(np.float64); x = hp(x); x = trim(x); x = fade(x); x = norm(x)
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
