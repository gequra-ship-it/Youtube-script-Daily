# Shorts thumbnails for short-faced-bear-short1..5 (guideline 16-9: one thumbnail A per short, no miya approval).
# Each videos/short-faced-bear-shortN/thumb/make.py calls build(N). Reuses the frog / fur helpers of the long-form
# videos/short-faced-bear/thumb/make.py (imported, not changed).
# 1 EYE / TO / EYE      script short1: "its head close to the level of a grown person's eyes" (shoulder ~1.5 m, may have).
#                        Face-off at sunset on the open plain: hiker and bear on all fours, eyes on one dashed line; frog between them.
# 2 RUNNING / BEAR?     script short2: "Why did people once call this giant the running bear?" -> long-distance walker.
#                        Bear walking calmly along a long paw-print trail, frog hiker on its back, the pale "sprinter" myth fading behind.
# 3 WHAT DID / IT EAT?  script short3: chemistry of collagen (nitrogen, carbon) to ask a fossil bear what it ate; meat signature vs
#                        varied diet debated. Fossil skull under a lab lamp, glowing sample vial, balance scale meat vs berries, frog in goggles.
# 4 SLOW / SQUEEZE      script short4: "No single blow ended this bear. It was a slow squeeze": steppe gave way to forests and wetlands.
#                        Bear on the last sunlit patch of grass while dark forest closes in from both sides, mammoth ghosts fading; frog in boots.
# 5 LIVING / COUSIN     script short5: spectacled bear, Tremarctos ornatus, only surviving short-faced bear, misty Andes forests, eats bromeliads.
#                        Spectacled bear on a mossy branch with a bromeliad; a giant ghost of Arctodus looms in the mist; frog in a knitted cap.
import os, sys, math, random, shutil, importlib.util
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
sys.path.insert(0, os.path.join(REPO, 'tools'))
from thumb_lib import page, svg, vpage, vsvg, lin, rad, spark
from figlib import person
_spec = importlib.util.spec_from_file_location('sfb_long_thumb', os.path.join(REPO, 'videos', 'short-faced-bear', 'thumb', 'make.py'))
LT = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(LT)
frog, furred, claws, tufts, snow_spruce = LT.frog, LT.furred, LT.claws, LT.tufts, LT.snow_spruce
FILTERS, BINK, INK, GREEN = LT.FILTERS, LT.BINK, LT.INK, LT.GREEN
LONG_THUMB = os.path.join(REPO, 'videos', 'short-faced-bear', 'thumb')


# ------------------------------------------------------------------ generic side-view bear (faces LEFT, ground y=0, shoulder ~500) ----
def leg_path(hx, hy, fx, fy, wt, wb, bend=0):
    dx, dy = fx - hx, fy - hy; L = math.hypot(dx, dy); nx, ny = -dy / L, dx / L
    mx, my = (hx + fx) / 2 + nx * bend, (hy + fy) / 2 + ny * bend
    a = (hx + nx * wt / 2, hy + ny * wt / 2); b = (fx + nx * wb / 2, fy + ny * wb / 2)
    c = (fx - nx * wb / 2, fy - ny * wb / 2); d = (hx - nx * wt / 2, hy - ny * wt / 2)
    m1 = (mx + nx * (wt + wb) / 3.4, my + ny * (wt + wb) / 3.4); m2 = (mx - nx * (wt + wb) / 3.4, my - ny * (wt + wb) / 3.4)
    return (f'M{a[0]:.0f} {a[1]:.0f} Q{m1[0]:.0f} {m1[1]:.0f} {b[0]:.0f} {b[1]:.0f} L{c[0]:.0f} {c[1]:.0f} '
            f'Q{m2[0]:.0f} {m2[1]:.0f} {d[0]:.0f} {d[1]:.0f} Z')


BODY = ('M-30 -380 C-8 -450 50 -495 115 -500 C210 -506 335 -472 450 -456 C545 -444 610 -400 612 -320 C614 -262 594 -232 562 -216 '
        'C480 -192 340 -196 240 -204 C160 -210 80 -226 30 -258 C-10 -284 -40 -330 -30 -380 Z')
HEAD = ('M70 -10 C76 -90 20 -132 -50 -134 C-110 -136 -150 -110 -170 -76 L-200 -60 C-222 -50 -226 -22 -212 -6 '
        'C-192 16 -146 30 -96 34 C-36 40 36 36 60 18 C72 6 72 0 70 -10 Z')
MUZ = 'M-168 -78 L-200 -60 C-222 -50 -226 -22 -212 -6 C-194 12 -164 22 -138 18 C-126 -6 -136 -48 -168 -78 Z'
PAL = dict(base='#4a2c18', dark='#24140b', light='#8a5634', rim='#ffd28a', fbase='#2e1c12', fdark='#140a06', flight='#5a3a24', muz='#b8875a')


def bear_side(uid, rnd, stride=0, neck=(-20, -395), head_rot=0, pal=None, light=(-.3, -1), eye='calm', mouth='closed',
              flat=None, fur=1.0, look=(0, 0), hump_glow=None):
    """returns (defs, svg) in local coords. flat=(fill, stroke, width) draws a plain silhouette (ghost) instead of fur."""
    p = dict(PAL); p.update(pal or {})
    D, O = '', ''
    s = stride
    legs_far = [((100, -330), (70 + s * .6, 0), 130, 70), ((500, -330), (520 - s * .6, 0), 190, 74)]
    legs_near = [((90, -330), (60 - s, 0), 140, 76), ((520, -330), (550 + s * .7, 0), 200, 80)]

    def part(k, d, bb, far=False, n=150, flow=92, rimw=16):
        nonlocal D, O
        if flat:
            O += f'<path d="{d}" fill="{flat[0]}" stroke="{flat[1]}" stroke-width="{flat[2]}" stroke-linejoin="round"/>'
            return
        if far:
            df, of = furred(uid + k, d, bb, p['fbase'], p['fdark'], p['flight'], p['rim'], light, rnd, n=int(n * fur), rimw=rimw, rimop=.6, flow=flow)
        else:
            df, of = furred(uid + k, d, bb, p['base'], p['dark'], p['light'], p['rim'], light, rnd, n=int(n * fur), rimw=rimw, flow=flow)
        D += df; O += of

    def paw(fx, far):
        nonlocal O
        col = p['fdark'] if far else p['dark']
        if flat:
            O += f'<ellipse cx="{fx - 18}" cy="-14" rx="52" ry="20" fill="{flat[0]}" stroke="{flat[1]}" stroke-width="{flat[2]}"/>'
            return
        O += f'<ellipse cx="{fx - 18}" cy="-14" rx="52" ry="20" fill="{col}" stroke="{BINK}" stroke-width="5"/>'
        O += claws([(fx - 64 + j * 13, -10, 66) for j in range(4)], s=.85)

    for i, (h, f, wt, wb) in enumerate(legs_far):
        part(f'lf{i}', leg_path(*h, *f, wt, wb, bend=-10 if i == 0 else 16), (min(h[0], f[0]) - 90, -340, max(h[0], f[0]) + 90, 4), far=True, n=110)
        paw(f[0], True)
    for i, (h, f, wt, wb) in enumerate(legs_near):
        part(f'ln{i}', leg_path(*h, *f, wt, wb, bend=-12 if i == 0 else 20), (min(h[0], f[0]) - 95, -345, max(h[0], f[0]) + 95, 4), n=150)
        paw(f[0], False)
    # body (over the leg tops, so legs grow out of it)
    if flat:
        O += f'<path d="{BODY}" fill="{flat[0]}" stroke="{flat[1]}" stroke-width="{flat[2]}"/>'
    else:
        if hump_glow:
            O += f'<path d="{BODY}" fill="none" stroke="{hump_glow}" stroke-width="30" opacity=".5" filter="url(#b12)"/>'
        df, of = furred(uid + 'b', BODY, (-40, -506, 614, -192), p['base'], p['dark'], p['light'], p['rim'], light, rnd, n=int(520 * fur), rimw=26, flow=98)
        D += df; O += of
        O += tufts([(60 + k * 24, -494 - math.sin(k / 7 * math.pi) * 8 + k, 0, -1) for k in range(8)], p['base'], rnd, w=3.5, L=(10, 18))
        O += '<path d="M40 -330 C70 -380 140 -390 170 -330 C180 -290 160 -240 140 -212" fill="none" stroke="#120804" stroke-width="5" opacity=".4"/>'
        O += '<path d="M600 -360 C560 -410 470 -410 450 -340 C440 -290 470 -240 500 -206" fill="none" stroke="#120804" stroke-width="5" opacity=".4"/>'
        O += tufts([(180 + k * 34, -202 + abs(k - 4) * 1.5, 0, 1) for k in range(9)], p['base'], rnd, w=3, L=(8, 16))
    # head
    hx, hy = neck
    O += f'<g transform="translate({hx} {hy}) rotate({head_rot})">'
    for ex, ey, r in ((22, -122, 27), (-28, -132, 21)):
        if flat:
            O += f'<circle cx="{ex}" cy="{ey}" r="{r}" fill="{flat[0]}" stroke="{flat[1]}" stroke-width="{flat[2]}"/>'
        else:
            O += f'<circle cx="{ex}" cy="{ey}" r="{r}" fill="{p["fbase"]}" stroke="{BINK}" stroke-width="5"/><circle cx="{ex}" cy="{ey + 3}" r="{r * .5:.0f}" fill="{p["fdark"]}" opacity=".7"/>'
            O += f'<path d="M{ex - r * .8:.0f} {ey - r * .5:.0f} A{r} {r} 0 0 1 {ex + r * .8:.0f} {ey - r * .5:.0f}" fill="none" stroke="{p["rim"]}" stroke-width="4" opacity=".8"/>'
    if flat:
        O += f'<path d="{HEAD}" fill="{flat[0]}" stroke="{flat[1]}" stroke-width="{flat[2]}"/>'
    else:
        df, of = furred(uid + 'h', HEAD, (-228, -138, 74, 40), p['base'], p['dark'], p['light'], p['rim'], light, rnd, n=int(190 * fur), rimw=20, flow=110)
        D += df
        O += of
        O += f'<path d="{MUZ}" fill="{p["muz"]}" opacity=".55"/>'
        O += '<path d="M-166 -74 C-140 -96 -110 -104 -80 -100" fill="none" stroke="#120804" stroke-width="4" opacity=".35"/>'
        O += tufts([(-120 + k * 30, 30 + (k % 2) * 4, 0, 1) for k in range(6)], p['base'], rnd, w=3, L=(8, 14))
        O += '<ellipse cx="-214" cy="-40" rx="17" ry="14" fill="#0a0503"/><ellipse cx="-219" cy="-46" rx="5" ry="3.5" fill="#fff4d8" opacity=".85"/>'
        if mouth == 'open':
            O += '<path d="M-206 -2 C-186 10 -156 16 -122 12 C-140 36 -176 44 -200 30 Z" fill="#5a1e20" stroke="#0a0503" stroke-width="4"/>'
            O += '<path d="M-192 4 L-186 22 L-180 6 Z M-146 12 L-140 30 L-134 12 Z" fill="#f4ecd8" stroke="#0a0503" stroke-width="2"/>'
        elif mouth == 'worried':
            O += '<path d="M-206 -2 Q-180 6 -160 2 Q-140 -2 -124 8" fill="none" stroke="#0a0503" stroke-width="4.5" stroke-linecap="round"/>'
        else:
            O += '<path d="M-206 -2 Q-170 14 -128 12" fill="none" stroke="#0a0503" stroke-width="4.5" stroke-linecap="round"/>'
        lx, ly = look
        if eye == 'wide':
            O += f'<circle cx="-104" cy="-82" r="24" fill="{p["rim"]}" opacity=".35" filter="url(#b6)"/>'
            O += '<ellipse cx="-104" cy="-82" rx="15" ry="13" fill="#f3e6c4" stroke="#0a0503" stroke-width="3.5"/>'
            O += f'<circle cx="{-108 + lx}" cy="{-82 + ly}" r="8" fill="#0a0503"/><circle cx="{-105 + lx}" cy="{-86 + ly}" r="3" fill="#fff"/>'
            O += '<path d="M-126 -104 L-84 -100" stroke="#0a0503" stroke-width="6" stroke-linecap="round"/>'
        elif eye == 'sad':
            O += f'<ellipse cx="-104" cy="-82" rx="11" ry="10" fill="#f3e6c4" stroke="#0a0503" stroke-width="3"/><circle cx="{-107 + lx}" cy="{-80 + ly}" r="6.5" fill="#0a0503"/><circle cx="{-105 + lx}" cy="{-83 + ly}" r="2.2" fill="#fff"/>'
            O += '<path d="M-124 -96 L-86 -108" stroke="#0a0503" stroke-width="6" stroke-linecap="round"/>'
        else:
            O += f'<ellipse cx="-104" cy="-82" rx="10" ry="9" fill="#0a0503"/><circle cx="{-101 + lx}" cy="{-85 + ly}" r="3" fill="#fff4d8"/>'
            O += '<path d="M-124 -100 L-86 -100" stroke="#0a0503" stroke-width="5" stroke-linecap="round"/>'
    O += '</g>'
    return D, O


def place(o, x, y, s, flip=False, extra=''):
    return f'<g transform="translate({x} {y}) scale({-s if flip else s} {s})"{extra}>{o}</g>'


# ------------------------------------------------------------------ frog outfits (frog local units) ----
GOGGLES = ('<path d="M-30 -66 L-34 -64 M38 -66 L42 -64" stroke-width="5"/>'
           '<path d="M-28 -66 L40 -66" stroke="#3a4a5a" stroke-width="6"/>'
           '<rect x="-27" y="-82" width="34" height="32" rx="12" fill="#bfe8ff" fill-opacity=".38" stroke-width="3.6"/>'
           '<rect x="5" y="-82" width="34" height="32" rx="12" fill="#bfe8ff" fill-opacity=".38" stroke-width="3.6"/>'
           '<path d="M-20 -76 l8 -2 M12 -76 l8 -2" stroke="#fff" stroke-width="3" opacity=".9"/>')
COAT = ('<path d="M-35 -26 Q4 -14 41 -26 L43 -4 Q42 8 4 8 Q-34 8 -36 -4 Z" fill="#f4f6f8" stroke-width="3.4"/>'
        '<path d="M-6 -18 L4 -2 L14 -18" fill="none" stroke-width="2.6"/><path d="M4 -2 L4 8" stroke-width="2.4"/>'
        '<rect x="18" y="-12" width="14" height="12" rx="2" fill="#e2e6ea" stroke-width="2.2"/>'
        '<path d="M22 -12 l0 -8 M27 -12 l0 -6" stroke="#3f6fb0" stroke-width="3"/>')
BANDANA = ('<path d="M-34 -26 q38 12 76 -2 l-2 10 q-16 4 -26 20 l-8 4 l-8 -6 q-10 -16 -32 -18z" fill="#e0902e" stroke-width="3"/>'
           '<circle cx="-12" cy="-18" r="2" fill="#fff3d0" stroke="none"/><circle cx="16" cy="-16" r="2" fill="#fff3d0" stroke="none"/>'
           '<circle cx="2" cy="-8" r="2" fill="#fff3d0" stroke="none"/>')
PACK = ('<rect x="-56" y="-66" width="40" height="58" rx="10" fill="#8a5a34" stroke-width="3.4"/>'
        '<rect x="-60" y="-40" width="16" height="22" rx="5" fill="#6a4428" stroke-width="3"/>'
        '<path d="M-52 -66 q16 -16 34 -4" fill="none" stroke-width="3"/>'
        '<rect x="-62" y="-80" width="44" height="16" rx="8" fill="#3f6fb0" stroke-width="3"/>')
SAFARI = ('<path d="M-44 -82 Q6 -100 56 -82 Q6 -74 -44 -82 Z" fill="#d8c08a" stroke-width="3.2"/>'
          '<path d="M-24 -86 q2 -34 30 -36 q30 2 32 36 z" fill="#e6d29c" stroke-width="3.4"/>'
          '<path d="M-24 -90 q30 6 62 0" fill="none" stroke="#8a5a34" stroke-width="6"/>')
BOOTS = ('<path d="M-42 -16 L-8 -16 L-6 6 Q-6 12 -14 12 L-46 12 Q-54 12 -52 4 Z" fill="#f2c230" stroke-width="3.4"/>'
         '<path d="M6 -16 L40 -16 L44 4 Q46 12 38 12 L4 12 Q-2 12 -2 6 Z" fill="#f2c230" stroke-width="3.4"/>'
         '<path d="M-40 -10 L-10 -10 M8 -10 L38 -10" stroke="#fff4b8" stroke-width="3" opacity=".9"/>'
         '<path d="M-50 10 L-8 10 M0 10 L42 10" stroke="#8a6a10" stroke-width="3"/>')
CHULLO = ('<path d="M-30 -80 Q-34 -134 8 -136 Q50 -134 46 -80 Z" fill="#c8483a" stroke-width="3.4"/>'
          '<path d="M-31 -92 Q8 -102 46 -92 L46 -84 Q8 -94 -31 -84 Z" fill="#f2c230" stroke="none"/>'
          '<path d="M-30 -110 Q8 -120 44 -110 L42 -102 Q8 -112 -30 -102 Z" fill="#2f8f8a" stroke="none"/>'
          '<path d="M-22 -100 l6 -6 l6 6 l6 -6 l6 6 l6 -6 l6 6 l6 -6 l6 6 l6 -6 l6 6" fill="none" stroke="#fff3d0" stroke-width="2.4"/>'
          '<path d="M-30 -80 Q-34 -134 8 -136 Q50 -134 46 -80" fill="none" stroke-width="3.4"/>'
          '<path d="M-30 -82 L-40 -48 L-20 -60 Z" fill="#c8483a" stroke-width="3"/><path d="M46 -82 L56 -48 L36 -60 Z" fill="#c8483a" stroke-width="3"/>'
          '<path d="M-40 -48 L-42 -30 M56 -48 L58 -30" stroke-width="2.4"/>'
          '<circle cx="-42" cy="-28" r="5" fill="#f2c230" stroke-width="2.4"/><circle cx="58" cy="-28" r="5" fill="#f2c230" stroke-width="2.4"/>'
          '<circle cx="8" cy="-140" r="10" fill="#2f8f8a" stroke-width="3"/>')
SWEAT = '<path d="M50 -84 q6 10 0 16 q-6 -6 0 -16z" fill="#bfe8ff" stroke-width="2.2"/><path d="M-34 -92 q5 8 0 13 q-5 -5 0 -13z" fill="#bfe8ff" stroke-width="2"/>'


def grass(rnd, n, x0, x1, y0, y1, col, h=(14, 34), op=(.35, .8), w=2.6):
    o = ''
    for _ in range(n):
        x = rnd.uniform(x0, x1); y = rnd.uniform(y0, y1); hh = rnd.uniform(*h) * (1 + (y - y0) / 400)
        o += (f'<path d="M{x:.0f} {y:.0f} q{rnd.uniform(-6, 6):.0f} {-hh * .6:.0f} {rnd.uniform(-10, 10):.0f} {-hh:.0f} M{x + 4:.0f} {y:.0f} q{rnd.uniform(0, 8):.0f} {-hh * .5:.0f} {rnd.uniform(4, 16):.0f} {-hh * .8:.0f}" '
              f'fill="none" stroke="{col}" stroke-width="{w}" opacity="{rnd.uniform(*op):.2f}"/>')
    return o


def mist(rnd, n, x0, x1, y0, y1, col, rx=(160, 360), ry=(30, 70), op=(.25, .5), blur=24):
    return ''.join(f'<ellipse cx="{rnd.uniform(x0, x1):.0f}" cy="{rnd.uniform(y0, y1):.0f}" rx="{rnd.uniform(*rx):.0f}" ry="{rnd.uniform(*ry):.0f}" '
                   f'fill="{col}" opacity="{rnd.uniform(*op):.2f}" filter="url(#b{blur})"/>' for _ in range(n))


def mammoth(x, y, s, col, op):
    return (f'<g transform="translate({x} {y}) scale({s})" fill="{col}" opacity="{op}"><path d="M-40 0 L-40 -40 C-40 -70 -10 -80 20 -76 C40 -74 52 -60 54 -40 C60 -30 62 -10 56 10 L50 10 C50 -10 46 -24 42 -30 L40 0 L28 0 L28 -20 L-24 -20 L-26 0 Z"/>'
            f'<path d="M50 -30 Q70 -20 64 -4" fill="none" stroke="{col}" stroke-width="5"/></g>')


# ================================================================== 1: EYE TO EYE =========================================
def make_1():
    rnd = random.Random(101); d = FILTERS; G = 935
    d += lin('sky1', [(0, '#231a3a'), (.35, '#5a3a5e'), (.62, '#c8705a'), (.8, '#f4b070'), (1, '#ffd89a')])
    d += rad('sun1', 860, 690, 820, [(0, '#fff6d8', 1), (.08, '#ffe2a0', .9), (.25, '#f8a868', .45), (.6, '#d0705a', .12), (1, '#d0705a', 0)])
    d += lin('gnd1', [(0, '#5a3a30'), (.3, '#3a2426'), (1, '#140c12')])
    d += rad('vig1', 960, 540, 1150, [(0, '#000', 0), (.7, '#000', 0), (1, '#0a0610', .6)])
    b = '<rect width="1920" height="1080" fill="url(#sky1)"/><rect width="1920" height="1080" fill="url(#sun1)"/>'
    for y, x0, x1, op in ((170, 980, 1900, .22), (260, 1200, 1920, .25), (360, 900, 1600, .2), (120, 500, 1200, .15)):
        b += f'<path d="M{x0} {y} Q{(x0 + x1) / 2} {y - 16} {x1} {y} Q{(x0 + x1) / 2} {y + 10} {x0} {y}Z" fill="#ffc890" opacity="{op}"/>'
    for k in range(16):
        a = math.radians(180 + k * 12)
        b += (f'<path d="M860 690 L{860 + math.cos(a - .025) * 1300:.0f} {690 + math.sin(a - .025) * 1300:.0f} L{860 + math.cos(a + .025) * 1300:.0f} {690 + math.sin(a + .025) * 1300:.0f}Z" fill="#ffe6b8" opacity=".07"/>')
    b += '<circle cx="860" cy="690" r="90" fill="#fff8e4"/><circle cx="860" cy="690" r="180" fill="#ffe0a0" opacity=".5" filter="url(#b24)"/>'
    # far hills + distant herd
    b += '<path d="M-20 720 Q300 650 640 690 Q900 715 1200 680 Q1550 640 1940 690 L1940 760 L-20 760Z" fill="#6a4048" opacity=".85"/>'
    for mx, ms in ((330, .7), (430, .55), (1500, .65), (1600, .5)):
        b += mammoth(mx, 690, ms, '#4a2a38', .7)
    b += f'<path d="M-20 750 Q500 720 960 745 Q1400 765 1940 735 L1940 1080 L-20 1080Z" fill="url(#gnd1)"/>'
    b += '<path d="M-20 750 Q500 720 960 745 Q1400 765 1940 735" fill="none" stroke="#ffcf8a" stroke-width="4" opacity=".5"/>'
    b += grass(rnd, 160, 0, 1920, 760, 1080, '#7a5048', op=(.3, .7))
    # ---- bear on all fours, head at the hiker's eye level ----
    bs = .83; bx = 1215
    bd, bo = bear_side('b1', rnd, stride=26, neck=(-20, -432), head_rot=-6, light=(-.9, -.5), eye='wide', mouth='closed',
                       pal=dict(rim='#ffd9a0'), hump_glow='#ffd8a0')
    d += bd
    b += f'<ellipse cx="{bx + 260 * bs:.0f}" cy="{G + 4}" rx="330" ry="22" fill="#000" opacity=".45"/>'
    b += place(bo, bx, G, bs)
    # ---- hiker ----
    H = 470 / 5.5; pcx = 650
    b += f'<ellipse cx="{pcx}" cy="{G + 4}" rx="100" ry="14" fill="#000" opacity=".4"/>'
    b += person(pcx, G, H=H, pose='stand', skin='#e6b48c', hair='#3a2a1e', shirt='#2f6f8f', pants='#2b3446', hair_style='cap', face='surprise', name='hiker')
    b += f'<path d="M{pcx - H * .7:.0f} {G - 5.5 * H + H * 1.2:.0f} Q{pcx - H * .8:.0f} {G - 5.5 * H + 2 * H:.0f} {pcx - H * .68:.0f} {G - 5.5 * H + 2.8 * H:.0f}" fill="none" stroke="#ffd8a0" stroke-width="5" opacity=".7"/>'
    # eye line: hiker eye -> bear eye
    pey = G - 5.5 * H + H * .5 + H * .04
    # bear eye in page coords: neck(-20,-432) rotated head point (-104,-82)
    a = math.radians(-6); ex = -20 + (-104 * math.cos(a) - -82 * math.sin(a)); ey = -432 + (-104 * math.sin(a) + -82 * math.cos(a))
    bex, bey = bx + ex * bs, G + ey * bs
    x0 = pcx + H * .3; x1 = bex - 22
    b += f'<path d="M{x0:.0f} {pey:.0f} L{x1:.0f} {bey:.0f}" stroke="#fff6d8" stroke-width="9" stroke-dasharray="22 16" stroke-linecap="round" opacity=".95"/>'
    b += f'<path d="M{x0:.0f} {pey:.0f} L{x1:.0f} {bey:.0f}" stroke="#2a1420" stroke-width="2.5" stroke-dasharray="22 16" opacity=".4"/>'
    b += spark(x0 + 4, pey, 16, '#fff6d8') + spark(x1, bey, 16, '#fff6d8')
    # frog between them, looking up at the bear, sweating
    b += frog(845, G + 2, 2.15, flip=False, look=(6, -7), mouth='O', shadow=True, head=SAFARI, brows=False, front=SWEAT,
              armL='M-34 -22 q-16 -8 -18 -30', armR='M38 -22 q16 -8 18 -30')
    for _ in range(40):
        b += f'<circle cx="{rnd.uniform(900, 1900):.0f}" cy="{rnd.uniform(60, 700):.0f}" r="{rnd.choice([1.4, 2, 2.6])}" fill="#fff0d0" opacity="{rnd.uniform(.25, .7):.2f}"/>'
    b += spark(1500, 200, 20, '#fff2d0') + spark(1700, 420, 14, '#fff2d0') + spark(1080, 300, 16, '#fff2d0')
    b += '<rect width="1920" height="1080" fill="url(#vig1)"/>'
    return d, b, [('EYE', 200, 'w'), ('TO', 110, 'w'), ('EYE', 236, 'y')], '#160c18'


# ================================================================== 2: RUNNING BEAR? ======================================
def make_2():
    rnd = random.Random(202); d = FILTERS; G = 905
    d += lin('sky2', [(0, '#3d78b8'), (.45, '#8ab8dc'), (.75, '#e6dcb8'), (1, '#f6e2a8')])
    d += rad('sun2', 1700, 180, 900, [(0, '#fffbe6', 1), (.12, '#fff0b8', .7), (.4, '#ffe2a0', .25), (1, '#ffe2a0', 0)])
    d += lin('hill2a', [(0, '#a8b878'), (1, '#7a8c58')]); d += lin('hill2b', [(0, '#c8b06a'), (1, '#8a7a44')])
    d += lin('gnd2', [(0, '#c8a860'), (.4, '#9a8448'), (1, '#4a3e24')])
    d += rad('vig2', 960, 540, 1150, [(0, '#000', 0), (.72, '#000', 0), (1, '#1a1408', .5)])
    b = '<rect width="1920" height="1080" fill="url(#sky2)"/><rect width="1920" height="1080" fill="url(#sun2)"/>'
    b += '<circle cx="1700" cy="180" r="70" fill="#fffbea"/>'
    for cx_, cy_, s_ in ((1180, 120, .9), (1450, 330, .7)):
        b += f'<g transform="translate({cx_} {cy_}) scale({s_})" fill="#fffaf0" opacity=".85"><ellipse cx="0" cy="0" rx="160" ry="40"/><ellipse cx="-60" cy="-26" rx="80" ry="48"/><ellipse cx="50" cy="-34" rx="90" ry="56"/></g>'
    # far mountains / hills
    b += '<path d="M-20 640 L160 520 L300 580 L460 470 L640 560 L800 500 L980 590 L1180 480 L1380 580 L1560 500 L1760 570 L1940 520 L1940 700 L-20 700Z" fill="#9aaac4" opacity=".8"/>'
    b += '<path d="M-20 680 Q300 600 700 650 Q1100 700 1500 620 Q1750 590 1940 640 L1940 760 L-20 760Z" fill="url(#hill2a)"/>'
    b += '<path d="M-20 740 Q400 690 900 720 Q1400 750 1940 700 L1940 820 L-20 820Z" fill="url(#hill2b)"/>'
    b += f'<path d="M-20 800 Q600 770 1100 790 Q1500 800 1940 780 L1940 1080 L-20 1080Z" fill="url(#gnd2)"/>'
    # winding trail of paw prints from the far hills to the bear
    trail = []
    for k in range(26):
        t = k / 25
        x = 330 + 520 * t + math.sin(t * 5.2) * 110 * (1 - t)
        y = 700 + (G - 700) * t ** 1.6
        sc = .18 + .9 * t ** 1.5
        trail.append((x, y, sc))
    b += '<path d="M' + ' L'.join(f'{x:.0f} {y + 6:.0f}' for x, y, _ in trail) + '" fill="none" stroke="#e8d49a" stroke-width="26" stroke-linecap="round" opacity=".45" filter="url(#b6)"/>'
    for k, (x, y, sc) in enumerate(trail[:-3]):
        off = (14 if k % 2 else -14) * sc
        b += (f'<g transform="translate({x:.0f} {y + off:.0f}) scale({sc * 1.1:.2f} {sc * .55:.2f})" fill="#5a4626" opacity=".7">'
              f'<ellipse cx="0" cy="0" rx="26" ry="18"/>' + ''.join(f'<ellipse cx="{-22 + j * 11}" cy="-22" rx="5" ry="6"/>' for j in range(5)) + '</g>')
    b += grass(rnd, 120, 0, 1920, 810, 1080, '#6a5a30', h=(14, 30), op=(.3, .7))
    for _ in range(26):   # little flowers
        x = rnd.uniform(0, 1920); y = rnd.uniform(830, 1060)
        b += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{rnd.uniform(3, 6):.1f}" fill="{rnd.choice(["#fff3c0", "#f2d27a", "#e8a0b0"])}" opacity=".85"/>'
    # ---- the myth: a pale sprinting bear dissolving behind ----
    gd, go = bear_side('g2', rnd, stride=170, neck=(-30, -410), head_rot=-6, flat=('#eef6ff', '#7aa8d8', 7), eye='calm')
    b += '<ellipse cx="900" cy="560" rx="330" ry="170" fill="#ffffff" opacity=".25" filter="url(#b50)"/>'
    b += place(go, 900, 720, .6, flip=True, extra=' opacity=".6"')
    for k in range(7):
        y = 470 + k * 30; x0 = 300 + (k % 3) * 40
        b += f'<path d="M{x0} {y} L{x0 + 240 - (k % 2) * 60} {y}" stroke="#ffffff" stroke-width="{8 - k % 3 * 2}" stroke-linecap="round" opacity=".45"/>'
    for _ in range(18):
        x = rnd.uniform(880, 1060); y = rnd.uniform(460, 720)
        b += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{rnd.uniform(3, 8):.1f}" fill="#ffffff" opacity="{rnd.uniform(.2, .5):.2f}"/>'
    # ---- the real bear, walking calmly to the right ----
    bs = 1.0; bx = 1620
    bd, bo = bear_side('b2', rnd, stride=105, neck=(-20, -388), head_rot=10, light=(.55, -1), eye='calm', mouth='closed',
                       pal=dict(rim='#fff0c0', base='#5a3620', light='#a06a3e'), hump_glow='#fff2c8')
    d += bd
    b += f'<ellipse cx="{bx - 280:.0f}" cy="{G + 6}" rx="380" ry="22" fill="#2a2010" opacity=".4"/>'
    # frog hiker riding on the hump (drawn in page coords after the bear)
    b += place(bo, bx, G, bs, flip=True)
    b += frog(1500, G - 488, 1.95, flip=True, look=(-8, -3), mouth='O', back=PACK, mid=BANDANA, shadow=False,
              legs=((-20, -6, -40, 6, -20), (20, -6, 40, 6, 20)),
              armL='M-34 -22 q-18 4 -22 18', armR='M38 -22 q18 -14 26 -36')
    b += spark(1230, 420, 18, '#fffbe6') + spark(1820, 520, 16, '#fffbe6') + spark(860, 620, 14, '#fffbe6')
    b += '<rect width="1920" height="1080" fill="url(#vig2)"/>'
    return d, b, [('RUNNING', 176, 'y'), ('BEAR?', 236, 'w')], '#1a1206'


# ================================================================== 3: WHAT DID IT EAT? ===================================
def skull(rnd):
    """Arctodus skull, side view facing LEFT, tooth line y=0, about x -410..390 / y -270..110."""
    o = ''
    cran = ('M-400 -40 C-412 -100 -392 -150 -342 -172 C-300 -192 -250 -206 -200 -226 C-120 -256 0 -272 120 -264 '
            'C240 -256 330 -232 380 -172 C402 -140 396 -100 370 -80 C330 -60 282 -62 250 -42 L150 -16 L-60 -8 L-300 -8 C-360 -8 -394 -18 -400 -40 Z')
    mand = ('M-392 42 C-396 22 -380 12 -360 12 L140 12 C196 12 222 -36 236 -96 L270 -108 C282 -70 270 -30 300 0 '
            'C322 30 302 62 262 72 C120 102 -100 112 -300 102 C-362 98 -392 82 -392 42 Z')
    o += f'<path d="{mand}" fill="url(#bone3d)" stroke="#2a1608" stroke-width="7" stroke-linejoin="round"/>'
    o += '<path d="M-360 70 C-200 90 0 92 220 60" fill="none" stroke="#6a4420" stroke-width="5" opacity=".5"/>'
    o += '<circle cx="-250" cy="60" r="9" fill="#3a2210"/><circle cx="-200" cy="64" r="7" fill="#3a2210"/>'
    # lower teeth
    o += '<path d="M-352 16 C-356 -20 -346 -50 -330 -66 C-326 -40 -326 -10 -322 14 Z" fill="#f4ead2" stroke="#2a1608" stroke-width="4"/>'
    o += f'<path d="{cran}" fill="url(#bone3)" stroke="#2a1608" stroke-width="7" stroke-linejoin="round"/>'
    # temporal fossa (dark hollow behind the eye) + zygomatic arch
    o += '<path d="M-110 -150 C-50 -206 110 -214 214 -160 C232 -126 210 -96 176 -96 C80 -98 -40 -88 -112 -106 Z" fill="#3a2010" opacity=".9"/>'
    o += '<path d="M-130 -150 C-60 -196 90 -206 190 -170" fill="none" stroke="#1e1006" stroke-width="10" opacity=".5"/>'
    o += '<path d="M-150 -78 C-80 -50 40 -46 110 -66 C150 -78 180 -98 200 -112" fill="none" stroke="#2a1608" stroke-width="46" stroke-linecap="round"/>'
    o += '<path d="M-150 -78 C-80 -50 40 -46 110 -66 C150 -78 180 -98 200 -112" fill="none" stroke="url(#bone3)" stroke-width="34" stroke-linecap="round"/>'
    o += '<path d="M-140 -90 C-80 -66 30 -62 100 -80" fill="none" stroke="#fff4d6" stroke-width="7" opacity=".7" stroke-linecap="round"/>'
    # orbit
    o += '<ellipse cx="-176" cy="-138" rx="54" ry="48" fill="#1e0e06" stroke="#2a1608" stroke-width="6"/>'
    o += '<path d="M-224 -150 C-214 -182 -170 -194 -136 -176" fill="none" stroke="#fff4d6" stroke-width="7" opacity=".8" stroke-linecap="round"/>'
    # nasal opening
    o += '<path d="M-398 -60 C-408 -100 -396 -140 -370 -148 C-360 -120 -364 -80 -378 -50 Z" fill="#1e0e06" stroke="#2a1608" stroke-width="4"/>'
    # sagittal crest highlight + cracks + patina
    o += '<path d="M-180 -232 C-100 -258 20 -270 130 -262 C230 -254 310 -236 360 -196" fill="none" stroke="#fff6dc" stroke-width="9" opacity=".75" stroke-linecap="round"/>'
    for c in ('M40 -250 l-14 30 l10 18 l-12 26', 'M260 -230 l16 26 l-8 20', 'M-260 -190 l20 24 l-6 22', 'M300 -120 l-30 10 l-10 24'):
        o += f'<path d="{c}" fill="none" stroke="#4a2a12" stroke-width="3.5" opacity=".7"/>'
    for _ in range(46):
        x = rnd.uniform(-360, 360); y = rnd.uniform(-240, 80)
        o += f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{rnd.uniform(6, 22):.0f}" ry="{rnd.uniform(3, 9):.0f}" fill="#8a5a2a" opacity="{rnd.uniform(.12, .3):.2f}"/>'
    # upper teeth: incisors, big canine, cheek teeth
    for x in (-396, -384):
        o += f'<path d="M{x} -10 L{x - 4} 14 Q{x + 4} 20 {x + 10} 12 L{x + 10} -10 Z" fill="#f4ead2" stroke="#2a1608" stroke-width="3"/>'
    o += '<path d="M-346 -12 C-344 30 -330 66 -306 92 C-306 56 -302 20 -296 -12 Z" fill="#fbf2dc" stroke="#2a1608" stroke-width="5"/>'
    o += '<path d="M-336 0 C-332 30 -322 56 -310 72" fill="none" stroke="#fff" stroke-width="4" opacity=".8"/>'
    for k, x in enumerate((-240, -180, -110, -30, 60)):
        w = 48 if k > 2 else 38
        o += f'<path d="M{x} -10 L{x} 10 Q{x + w / 2} 26 {x + w} 10 L{x + w} -10 Z" fill="#eadcbc" stroke="#2a1608" stroke-width="4"/>'
    return o


def make_3(v=False):
    rnd = random.Random(303); d = FILTERS
    d += lin('wall3', [(0, '#0e1e2a'), (.6, '#16303c'), (1, '#1e3a44')])
    d += rad('lamp3', 1240, 520, 820, [(0, '#ffe6b0', .75), (.25, '#f6c27a', .4), (.6, '#c08a50', .1), (1, '#c08a50', 0)])
    d += lin('bench3', [(0, '#8a5a34'), (.15, '#6a4226'), (1, '#2a180c')])
    d += lin('bone3', [(0, '#f6e2b4'), (.5, '#d8b07a'), (1, '#9a6a3a')])
    d += lin('bone3d', [(0, '#d8b07a'), (1, '#7a4e26')])
    d += rad('vial3', 1640, 640, 160, [(0, '#c8ffe8', 1), (.4, '#5ae0b0', .6), (1, '#5ae0b0', 0)])
    d += lin('meat3', [(0, '#e88a72'), (1, '#9a3a34')])
    d += rad('vig3', 960, 540, 1150, [(0, '#000', 0), (.66, '#000', 0), (1, '#04080c', .7)])
    b = '<rect width="1920" height="1080" fill="url(#wall3)"/>'
    # shelves with jars and bones in the dark
    for sy in (230, 470):
        b += f'<rect x="980" y="{sy}" width="960" height="16" fill="#0a161e"/><rect x="980" y="{sy}" width="960" height="4" fill="#3a5a64" opacity=".6"/>'
        for k in range(9):
            x = 1000 + k * 104 + rnd.uniform(-10, 10); h = rnd.uniform(60, 120); w = rnd.uniform(40, 70)
            col = rnd.choice(['#1c3a44', '#22424a', '#183038'])
            b += f'<rect x="{x:.0f}" y="{sy - h:.0f}" width="{w:.0f}" height="{h:.0f}" rx="8" fill="{col}" stroke="#08121a" stroke-width="3"/>'
            b += f'<rect x="{x + 6:.0f}" y="{sy - h + 8:.0f}" width="6" height="{h - 20:.0f}" rx="3" fill="#5a8a94" opacity=".35"/>'
    b += '<rect width="1920" height="1080" fill="url(#lamp3)"/>'
    # lamp: arm from top right and shade
    b += '<path d="M1960 40 L1620 110 L1430 150" fill="none" stroke="#0a1218" stroke-width="20" stroke-linecap="round"/>'
    b += '<path d="M1960 40 L1620 110 L1430 150" fill="none" stroke="#3a4e58" stroke-width="8" stroke-linecap="round"/>'
    b += '<path d="M1360 120 L1500 120 L1560 230 L1300 230 Z" fill="#2f6f70" stroke="#0a1218" stroke-width="7" stroke-linejoin="round"/>'
    b += '<path d="M1380 130 L1430 130 L1410 220 L1330 220 Z" fill="#6ab0ac" opacity=".5"/>'
    b += '<ellipse cx="1430" cy="232" rx="128" ry="16" fill="#fff8e0"/>'
    b += '<path d="M1302 232 L1558 232 L1840 820 L860 820 Z" fill="#fff0c8" opacity=".14"/>'
    b += '<path d="M1302 232 L1558 232 L1700 820 L1000 820 Z" fill="#fff4d8" opacity=".1"/>'
    # bench
    b += '<path d="M-20 800 L1940 800 L1940 1080 L-20 1080 Z" fill="url(#bench3)"/>'
    b += '<path d="M-20 800 L1940 800" stroke="#e8b880" stroke-width="5" opacity=".7"/>'
    b += '<ellipse cx="1240" cy="806" rx="520" ry="34" fill="#ffd89a" opacity=".22" filter="url(#b12)"/>'
    for k in range(6):
        y = 840 + k * 40
        b += f'<path d="M-20 {y} Q960 {y + 10} 1940 {y - 6}" stroke="#2a180c" stroke-width="3" opacity=".5" fill="none"/>'
    # ---- balance scale: meat (heavier, lower) vs berries (landscape only; no room in the portrait crop) ----
    sx, sy = 470, 580
    b0 = b
    b += f'<ellipse cx="{sx}" cy="806" rx="110" ry="12" fill="#000" opacity=".4"/>'
    b += f'<path d="M{sx - 70} 800 L{sx + 70} 800 L{sx + 50} 776 L{sx - 50} 776 Z" fill="#b8892e" stroke="#1a1006" stroke-width="5"/>'
    b += f'<rect x="{sx - 9}" y="{sy}" width="18" height="{776 - sy}" fill="#d8aa44" stroke="#1a1006" stroke-width="5"/>'
    tilt = 9; L_ = 175
    ax0 = sx - L_ * math.cos(math.radians(tilt)); ay0 = sy + L_ * math.sin(math.radians(tilt))
    ax1 = sx + L_ * math.cos(math.radians(tilt)); ay1 = sy - L_ * math.sin(math.radians(tilt))
    b += f'<path d="M{ax0:.0f} {ay0:.0f} L{ax1:.0f} {ay1:.0f}" stroke="#1a1006" stroke-width="16" stroke-linecap="round"/><path d="M{ax0:.0f} {ay0:.0f} L{ax1:.0f} {ay1:.0f}" stroke="#e8c060" stroke-width="8" stroke-linecap="round"/>'
    b += f'<circle cx="{sx}" cy="{sy}" r="16" fill="#f2d27a" stroke="#1a1006" stroke-width="5"/>'
    for px_, py_, kind in ((ax0, ay0, 'meat'), (ax1, ay1, 'berry')):
        pb = py_ + 130
        b += f'<path d="M{px_:.0f} {py_:.0f} L{px_ - 70:.0f} {pb:.0f} M{px_:.0f} {py_:.0f} L{px_ + 70:.0f} {pb:.0f}" stroke="#d8aa44" stroke-width="4"/>'
        if kind == 'meat':
            b += f'<g transform="translate({px_:.0f} {pb - 34:.0f}) rotate(-12)"><circle cx="58" cy="-6" r="13" fill="#f4ecd8" stroke="{BINK}" stroke-width="4"/><circle cx="58" cy="14" r="13" fill="#f4ecd8" stroke="{BINK}" stroke-width="4"/>'
            b += f'<path d="M0 0 L60 4" stroke="{BINK}" stroke-width="18" stroke-linecap="round"/><path d="M0 0 L60 4" stroke="#f4ecd8" stroke-width="10" stroke-linecap="round"/>'
            b += f'<ellipse cx="-14" cy="0" rx="58" ry="40" fill="url(#meat3)" stroke="{BINK}" stroke-width="5"/><path d="M-50 -14 Q-20 -36 20 -26" fill="none" stroke="#fff" stroke-width="6" opacity=".55" stroke-linecap="round"/></g>'
        else:
            for j, (bx_, by_) in enumerate(((-30, -16), (0, -18), (30, -16), (-15, -40), (15, -40), (0, -62))):
                b += f'<circle cx="{px_ + bx_:.0f}" cy="{pb + by_:.0f}" r="15" fill="{"#5a3a9a" if j % 2 else "#c83a5a"}" stroke="{BINK}" stroke-width="4"/><circle cx="{px_ + bx_ - 5:.0f}" cy="{pb + by_ - 5:.0f}" r="4" fill="#fff" opacity=".7"/>'
            b += f'<path d="M{px_:.0f} {pb - 76:.0f} q10 -18 26 -14 q-10 14 -26 14" fill="#5aa04a" stroke="{BINK}" stroke-width="3"/>'
        b += f'<path d="M{px_ - 78:.0f} {pb:.0f} Q{px_:.0f} {pb + 40:.0f} {px_ + 78:.0f} {pb:.0f} Z" fill="#d8aa44" stroke="#1a1006" stroke-width="5"/>'
    if v:
        b = b0
    # ---- the fossil skull on a wooden block ----
    b += '<ellipse cx="1240" cy="808" rx="400" ry="22" fill="#000" opacity=".5"/>'
    b += '<path d="M1010 800 L1470 800 L1450 742 L1030 742 Z" fill="#6a4226" stroke="#1a1006" stroke-width="6"/><path d="M1030 746 L1450 746" stroke="#c8925e" stroke-width="4" opacity=".7"/>'
    b += '<circle cx="1240" cy="520" r="380" fill="#ffd89a" opacity=".22" filter="url(#b50)"/>'
    b += f'<g transform="translate(1240 630) scale(1.02) rotate(-4)">{skull(rnd)}</g>'
    # glowing sample: small drilled hole on the skull + vial
    b += '<circle cx="1420" cy="470" r="9" fill="#1e0e06"/><circle cx="1420" cy="470" r="16" fill="#7affd0" opacity=".35" filter="url(#b6)"/>'
    for k in range(7):
        b += f'<circle cx="{1430 + k * 30 + rnd.uniform(-6, 6):.0f}" cy="{460 + k * 22 + rnd.uniform(-6, 6):.0f}" r="{rnd.uniform(3, 6):.1f}" fill="#bfffe6" opacity="{.8 - k * .08:.2f}"/>'
    # ---- frog scientist in goggles holding up the glowing vial ----
    b += '<circle cx="1640" cy="640" r="150" fill="url(#vial3)"/>'
    b += frog(1700, 800, 2.45, flip=True, look=(-7, -6), mouth='O', shadow=True, head=GOGGLES, mid=COAT, brows=False,
              armL='M-34 -22 q-10 -10 -4 -34', armR='M38 -22 q14 6 16 22')
    # vial in the frog's raised hand (hand at local (-38,-56) -> page)
    vx, vy = 1700 + 38 * 2.45, 800 - 56 * 2.45
    b += f'<g transform="translate({vx:.0f} {vy - 70:.0f}) rotate(10)"><rect x="-17" y="-70" width="34" height="130" rx="17" fill="#e8fff6" fill-opacity=".35" stroke="#0a1a14" stroke-width="5"/>'
    b += '<path d="M-14 0 L14 0 L14 44 Q14 58 0 58 Q-14 58 -14 44 Z" fill="#5ae0b0"/><rect x="-21" y="-80" width="42" height="18" rx="5" fill="#c8483a" stroke="#0a1a14" stroke-width="4"/>'
    b += '<path d="M-8 -50 L-8 30" stroke="#fff" stroke-width="5" opacity=".7" stroke-linecap="round"/></g>'
    b += spark(vx - 40, vy - 190, 20, '#d8fff0') + spark(vx + 40, vy - 120, 13, '#d8fff0')
    b += spark(1180, 330, 18, '#fff6d6') + spark(900, 680, 14, '#fff6d6')
    for _ in range(40):
        b += f'<circle cx="{rnd.uniform(1050, 1800):.0f}" cy="{rnd.uniform(240, 800):.0f}" r="{rnd.choice([1.4, 2, 2.6])}" fill="#fff4d8" opacity="{rnd.uniform(.15, .5):.2f}"/>'
    b += '<rect width="1920" height="1080" fill="url(#vig3)"/>'
    return d, b, [('WHAT DID', 150, 'w'), ('IT EAT?', 232, 'y')], '#06121a'


# ================================================================== 4: SLOW SQUEEZE =======================================
def tree_wall(rnd, x0, x1, base, hmin, hmax, col, trunk, n, lean=0, op=1.0):
    o = f'<g opacity="{op}">'
    for _ in range(n):
        x = rnd.uniform(x0, x1); h = rnd.uniform(hmin, hmax); bb = base + rnd.uniform(-20, 30)
        lx = lean * h
        o += f'<path d="M{x - 10:.0f} {bb:.0f} L{x + lx * .7 - 6:.0f} {bb - h * .7:.0f} L{x + lx * .7 + 6:.0f} {bb - h * .7:.0f} L{x + 10:.0f} {bb:.0f} Z" fill="{trunk}"/>'
        w = h * .3
        for k in range(5):
            t = k / 5; yy = bb - h * .15 - t * h * .82; ww = w * (1 - t * .75); xx = x + lx * (yy - bb) / -h
            o += f'<path d="M{xx - ww:.0f} {yy:.0f} L{xx + lx * .2:.0f} {yy - h * .3:.0f} L{xx + ww:.0f} {yy:.0f} Q{xx:.0f} {yy - h * .06:.0f} {xx - ww:.0f} {yy:.0f} Z" fill="{col}"/>'
    return o + '</g>'


def make_4():
    rnd = random.Random(404); d = FILTERS; G = 860
    d += lin('sky4', [(0, '#1a2a2c'), (.4, '#3a5050'), (.75, '#c8a870'), (1, '#f0d290')])
    d += rad('gap4', 1210, 620, 640, [(0, '#fff2c8', .95), (.25, '#f6d590', .55), (.6, '#c8a060', .15), (1, '#c8a060', 0)])
    d += rad('patch4', 1210, 880, 520, [(0, '#e8c46a', 1), (.5, '#b89a48', .85), (1, '#3a3a20', 0)])
    d += lin('mud4', [(0, '#2a2418'), (1, '#0e0c08')])
    d += rad('vig4', 960, 540, 1150, [(0, '#000', 0), (.6, '#000', 0), (1, '#050806', .75)])
    b = '<rect width="1920" height="1080" fill="url(#sky4)"/><rect width="1920" height="1080" fill="url(#gap4)"/>'
    # distant open steppe in the gap, mammoth ghosts walking away
    b += '<path d="M700 690 Q1000 650 1300 670 Q1550 690 1720 660 L1720 760 L700 760Z" fill="#b8a070" opacity=".85"/>'
    for mx, ms, op in ((1000, .9, .45), (1110, .7, .35), (1380, .8, .3), (1480, .6, .22)):
        b += mammoth(mx, 678, ms, '#6a5a44', op)
    b += mist(rnd, 14, 700, 1700, 640, 760, '#fff0c8', op=(.2, .45), blur=24)
    # back tree rows (lighter), then the closing walls
    b += tree_wall(rnd, -40, 760, 760, 260, 420, '#2c4438', '#1c2a22', 24, lean=.05, op=.85)
    b += tree_wall(rnd, 1660, 1960, 760, 260, 420, '#2c4438', '#1c2a22', 12, lean=-.05, op=.85)
    b += mist(rnd, 10, 0, 1920, 700, 820, '#c8d0b0', op=(.15, .3))
    # sunlit grass patch (the last open steppe) + mud around it
    b += '<rect x="-20" y="760" width="1960" height="340" fill="url(#mud4)"/>'
    b += '<ellipse cx="1210" cy="880" rx="560" ry="120" fill="url(#patch4)"/>'
    b += grass(rnd, 140, 760, 1660, 800, 960, '#f2d27a', h=(16, 34), op=(.4, .85))
    # puddles (wetland) reflecting the light
    for px_, py_, rx_, ry_ in ((560, 980, 220, 34), (1480, 1010, 160, 24), (300, 900, 160, 22)):
        b += f'<ellipse cx="{px_}" cy="{py_}" rx="{rx_}" ry="{ry_}" fill="#7a8a80" opacity=".5"/><path d="M{px_ - rx_ * .6:.0f} {py_ - 4} L{px_ + rx_ * .3:.0f} {py_ - 6}" stroke="#e8e0c0" stroke-width="4" opacity=".6"/>'
    # ---- the bear on the patch ----
    bs = .86; bx = 1080
    bd, bo = bear_side('b4', rnd, stride=10, neck=(-14, -372), head_rot=14, light=(.2, -1), eye='sad', mouth='worried',
                       pal=dict(rim='#ffe2a0'), hump_glow='#ffe6b0', look=(4, 2))
    d += bd
    b += f'<ellipse cx="{bx + 260 * bs:.0f}" cy="{G + 6}" rx="320" ry="20" fill="#2a2010" opacity=".5"/>'
    b += place(bo, bx, G, bs)
    # front forest walls: big dark trunks + spruces leaning in, branches reaching toward the bear
    b += tree_wall(rnd, -60, 560, 1000, 520, 820, '#122018', '#0c140e', 16, lean=.12)
    b += tree_wall(rnd, 1760, 2000, 1000, 520, 820, '#122018', '#0c140e', 7, lean=-.12)
    for x, w in ((420, 70), (600, 54), (1800, 80)):
        b += f'<path d="M{x - w / 2} 1080 C{x - w / 2 + 10} 700 {x - w / 2 + 30} 300 {x - w / 2 + 50 if x < 960 else x - w / 2 - 50} -20 L{x + w / 2 + (50 if x < 960 else -50)} -20 C{x + w / 2 + 20} 300 {x + w / 2} 700 {x + w / 2} 1080 Z" fill="#0e1810" stroke="#050a06" stroke-width="5"/>'
    # branches reaching in
    for (x0, y0, x1, y1) in ((620, 380, 870, 470), (640, 560, 830, 620), (1780, 300, 1560, 420), (1790, 520, 1620, 590)):
        b += f'<path d="M{x0} {y0} Q{(x0 + x1) / 2} {min(y0, y1) - 40} {x1} {y1}" fill="none" stroke="#0e1810" stroke-width="16" stroke-linecap="round"/>'
        for k in range(5):
            t = (k + 1) / 6; xx = x0 + (x1 - x0) * t; yy = y0 + (y1 - y0) * t - 30 * math.sin(t * math.pi)
            b += f'<ellipse cx="{xx:.0f}" cy="{yy + 14:.0f}" rx="{46 - k * 5}" ry="{22 - k * 2}" fill="#1a3020" stroke="#050a06" stroke-width="3"/>'
    # foreground ferns creeping in
    for (x, y, s, f) in ((80, 1080, 1.4, 1), (300, 1090, 1.1, 1), (1840, 1080, 1.2, -1)):
        b += f'<g transform="translate({x} {y}) scale({s * f} {s})">'
        for k in range(7):
            a = -150 + k * 20
            ex_ = math.cos(math.radians(a)) * 220; ey_ = math.sin(math.radians(a)) * 220
            b += f'<path d="M0 0 Q{ex_ * .5:.0f} {ey_ * .7:.0f} {ex_:.0f} {ey_:.0f}" fill="none" stroke="#0a140c" stroke-width="14" stroke-linecap="round"/>'
            for j in range(1, 9):
                t = j / 9; px_ = ex_ * t; py_ = ey_ * t + ey_ * .3 * t * (1 - t); ln = 46 * (1 - t * .7)
                for sg in (-1, 1):
                    b += f'<path d="M{px_:.0f} {py_:.0f} q{-ey_ / 220 * ln * sg * .6:.0f} {ex_ / 220 * ln * sg * .6:.0f} {-ey_ / 220 * ln * sg + ex_ / 220 * 10:.0f} {ex_ / 220 * ln * sg + ey_ / 220 * 10:.0f}" fill="none" stroke="#14281a" stroke-width="9" stroke-linecap="round"/>'
        b += '</g>'
    # frog in rain boots standing in the mud puddle, worried
    b += frog(720, 958, 2.25, flip=False, look=(8, -4), mouth='o', shadow=True, front=BOOTS + SWEAT,
              armL='M-34 -22 q-14 -2 -18 -24', armR='M38 -22 q14 -2 18 -24')
    b += '<ellipse cx="720" cy="966" rx="120" ry="12" fill="#9aa898" opacity=".35"/>'
    b += spark(1210, 560, 20, '#fff6d6') + spark(1400, 640, 14, '#fff6d6')
    for _ in range(30):
        b += f'<circle cx="{rnd.uniform(800, 1620):.0f}" cy="{rnd.uniform(400, 760):.0f}" r="{rnd.choice([1.4, 2, 2.6])}" fill="#fff4d0" opacity="{rnd.uniform(.25, .6):.2f}"/>'
    b += '<rect width="1920" height="1080" fill="url(#vig4)"/>'
    return d, b, [('SLOW', 176, 'w'), ('SQUEEZE', 206, 'y')], '#08100a'


# ================================================================== 5: LIVING COUSIN ======================================
def spectacled(rnd, d_acc):
    """spectacled bear sitting, front view, centre x=0, seat y=0 (about 330 wide, 420 tall)."""
    o = ''; D = ''
    pal = ('#2a2220', '#100c0a', '#4e4440', '#cfe8d8')
    legs = 'M-150 -10 C-170 -60 -130 -110 -70 -100 C-30 -90 -20 -40 -40 0 C-70 16 -130 16 -150 -10 Z'
    legs2 = 'M150 -10 C170 -60 130 -110 70 -100 C30 -90 20 -40 40 0 C70 16 130 16 150 -10 Z'
    torso = 'M-120 -40 C-150 -140 -130 -250 -60 -290 C-20 -306 20 -306 60 -290 C130 -250 150 -140 120 -40 C80 0 -80 0 -120 -40 Z'
    for k, p in (('t', torso), ('l1', legs), ('l2', legs2)):
        df, of = furred('sp' + k, p, (-170, -310, 170, 20), *pal, (.5, -1), rnd, n=260 if k == 't' else 80, rimw=18, flow=95)
        D += df; o += of
    for fx in (-100, 100):   # foot pads facing us
        o += f'<ellipse cx="{fx}" cy="-30" rx="30" ry="24" fill="#3a302c" stroke="{BINK}" stroke-width="4"/>'
        o += ''.join(f'<ellipse cx="{fx - 20 + j * 13}" cy="-58" rx="6" ry="7" fill="#3a302c" stroke="{BINK}" stroke-width="3"/>' for j in range(4))
    # cream chest bib
    o += '<path d="M-60 -250 C-40 -220 -20 -200 0 -160 C20 -200 40 -220 60 -250 C40 -230 20 -226 0 -236 C-20 -226 -40 -230 -60 -250 Z" fill="#e8dcb4" opacity=".9"/>'
    # head
    hd = 'M-96 -360 C-100 -430 -50 -470 0 -470 C50 -470 100 -430 96 -360 C94 -310 50 -282 0 -282 C-50 -282 -94 -310 -96 -360 Z'
    for ex in (-72, 72):
        o += f'<circle cx="{ex}" cy="-448" r="26" fill="{pal[0]}" stroke="{BINK}" stroke-width="5"/><circle cx="{ex}" cy="-446" r="12" fill="{pal[1]}"/>'
    df, of = furred('sph', hd, (-100, -474, 100, -280), *pal, (.5, -1), rnd, n=150, rimw=16, flow=100)
    D += df; o += of
    # spectacle markings (pale rings around the eyes) + pale muzzle
    o += '<path d="M-74 -398 C-80 -430 -50 -446 -26 -430 C-14 -420 -20 -392 -30 -372 C-36 -356 -46 -330 -40 -312 C-60 -330 -70 -360 -74 -398 Z" fill="#e8dcb4"/>'
    o += '<path d="M74 -398 C80 -430 50 -446 26 -430 C14 -420 20 -392 30 -372 C36 -356 46 -330 40 -312 C60 -330 70 -360 74 -398 Z" fill="#e8dcb4"/>'
    o += '<ellipse cx="0" cy="-330" rx="48" ry="38" fill="#e2d2a8" stroke="#3a2a20" stroke-width="3"/>'
    o += '<ellipse cx="0" cy="-348" rx="20" ry="14" fill="#100c0a"/><ellipse cx="-6" cy="-353" rx="6" ry="3.5" fill="#fff" opacity=".8"/>'
    o += '<path d="M0 -334 L0 -318 M-16 -312 Q0 -302 16 -312" fill="none" stroke="#100c0a" stroke-width="4" stroke-linecap="round"/>'
    for ex in (-46, 46):
        o += f'<ellipse cx="{ex}" cy="-404" rx="13" ry="14" fill="#100c0a"/><circle cx="{ex + 4}" cy="-409" r="4.5" fill="#fff"/>'
    # arms holding the bromeliad
    for sgn in (-1, 1):
        a = f'M{sgn * 90} -230 C{sgn * 130} -190 {sgn * 110} -130 {sgn * 46} -136 C{sgn * 30} -150 {sgn * 40} -180 {sgn * 60} -200 Z'
        df, of = furred(f'spa{sgn + 1}', a, (-140, -240, 140, -120), *pal, (.5, -1), rnd, n=50, rimw=12, flow=60 if sgn < 0 else 120)
        D += df; o += of
    # bromeliad: red bract star with green leaves
    br = '<g transform="translate(0 -176) scale(1.25)">'
    for k in range(9):
        a = -170 + k * 20
        br += f'<path d="M0 0 Q{math.cos(math.radians(a)) * 50:.0f} {math.sin(math.radians(a)) * 50 - 10:.0f} {math.cos(math.radians(a)) * 96:.0f} {math.sin(math.radians(a)) * 96:.0f} Q{math.cos(math.radians(a + 8)) * 40:.0f} {math.sin(math.radians(a + 8)) * 40:.0f} 0 0 Z" fill="#7ac860" stroke="{BINK}" stroke-width="3"/>'
    for k in range(7):
        a = -150 + k * 20
        br += f'<path d="M0 -6 Q{math.cos(math.radians(a)) * 30:.0f} {math.sin(math.radians(a)) * 30 - 10:.0f} {math.cos(math.radians(a)) * 70:.0f} {math.sin(math.radians(a)) * 70 - 8:.0f} Q{math.cos(math.radians(a + 10)) * 26:.0f} {math.sin(math.radians(a + 10)) * 26:.0f} 0 -6 Z" fill="#ff5a44" stroke="{BINK}" stroke-width="3"/>'
    br += '<circle cx="0" cy="-14" r="12" fill="#f2d27a" stroke="#1d2b1c" stroke-width="3"/></g>'
    o += br
    for sgn in (-1, 1):   # paws in front of the plant
        o += f'<ellipse cx="{sgn * 46}" cy="-140" rx="26" ry="22" fill="#2a2220" stroke="{BINK}" stroke-width="4"/>'
        o += claws([(sgn * 46 + j * 10 - 15, -128, 0) for j in range(4)], s=.5)
    return D, o


def make_5():
    rnd = random.Random(505); d = FILTERS
    d += lin('sky5', [(0, '#1e3a3a'), (.45, '#4a7a6a'), (.8, '#a8c8a0'), (1, '#d8e8c0')])
    d += rad('sun5', 1620, 120, 1000, [(0, '#fff8d8', 1), (.15, '#f8f0c0', .6), (.5, '#c8e0b0', .2), (1, '#c8e0b0', 0)])
    d += lin('branch5', [(0, '#6a4a30'), (1, '#2a1a10')])
    d += rad('ghost5', 1360, 420, 700, [(0, '#f4fff8', .55), (.6, '#d8f0e8', .2), (1, '#d8f0e8', 0)])
    d += rad('vig5', 960, 540, 1150, [(0, '#000', 0), (.7, '#000', 0), (1, '#06100c', .6)])
    b = '<rect width="1920" height="1080" fill="url(#sky5)"/><rect width="1920" height="1080" fill="url(#sun5)"/>'
    # Andes peaks above the cloud forest
    b += '<path d="M-20 560 L200 330 L320 420 L520 220 L700 400 L860 300 L1040 460 L1240 260 L1420 420 L1600 200 L1780 380 L1940 300 L1940 640 L-20 640Z" fill="#7a9a94" opacity=".7"/>'
    b += '<path d="M520 220 L570 280 L600 270 M1240 260 L1290 320 L1320 310 M1600 200 L1650 260 L1690 250" fill="none" stroke="#f4fbff" stroke-width="10" stroke-linejoin="round" opacity=".8"/>'
    b += mist(rnd, 20, -100, 2000, 440, 620, '#f0f8f0', op=(.35, .7), blur=24)
    # sun rays through the mist
    for k in range(9):
        x0 = 1250 + k * 90
        b += f'<path d="M{x0} -20 L{x0 + 70} -20 L{x0 - 380} 1100 L{x0 - 470} 1100 Z" fill="#fffbe0" opacity=".06"/>'
    # mid forest silhouettes with moss
    for k in range(18):
        x = rnd.uniform(-40, 1960); w = rnd.uniform(30, 60)
        b += f'<path d="M{x:.0f} 1080 L{x + 6:.0f} 520 L{x + w:.0f} 520 L{x + w + 6:.0f} 1080 Z" fill="#3a5a4a" opacity=".55"/>'
        b += f'<ellipse cx="{x + w / 2:.0f}" cy="{rnd.uniform(500, 560):.0f}" rx="{rnd.uniform(90, 160):.0f}" ry="{rnd.uniform(50, 80):.0f}" fill="#4a7058" opacity=".55"/>'
    b += mist(rnd, 16, -100, 2000, 600, 900, '#e8f4ec', op=(.25, .5), blur=24)
    # ---- the ghost of Arctodus, huge, looming in the mist behind ----
    b += '<ellipse cx="1360" cy="420" rx="620" ry="420" fill="url(#ghost5)"/>'
    gd, go = bear_side('g5', rnd, stride=20, neck=(-20, -420), head_rot=22, flat=('#dff4f0', '#8ac0b8', 6))
    b += f'<g opacity=".42" filter="url(#b2)">{place(go, 1290, 960, 1.42)}</g>'
    # ghost face details (eye + nose) so it reads as a bear looking down
    a = math.radians(22); s_ = 1.42
    def gp(px, py):
        return 1290 + s_ * (-20 + px * math.cos(a) - py * math.sin(a)), 960 + s_ * (-420 + px * math.sin(a) + py * math.cos(a))
    gx, gy = gp(-104, -82); nx_, ny_ = gp(-214, -40)
    b += f'<ellipse cx="{gx:.0f}" cy="{gy:.0f}" rx="16" ry="14" fill="#2a4a44" opacity=".7"/><ellipse cx="{nx_:.0f}" cy="{ny_:.0f}" rx="26" ry="20" fill="#2a4a44" opacity=".6"/>'
    b += mist(rnd, 6, 900, 1900, 820, 960, '#f4fbf6', op=(.25, .5), blur=24)
    # ---- mossy branch across the frame ----
    br = 'M620 770 C900 740 1200 760 1500 735 C1700 720 1850 700 1960 690 L1960 790 C1850 800 1700 820 1500 832 C1200 850 900 836 640 840 C600 830 596 790 620 770 Z'
    b += f'<path d="{br}" fill="url(#branch5)" stroke="#140c06" stroke-width="7"/>'
    b += '<path d="M650 774 C900 746 1200 766 1500 741 C1700 726 1850 706 1960 696" fill="none" stroke="#c8a070" stroke-width="5" opacity=".5"/>'
    for _ in range(46):   # moss cushions on top
        x = rnd.uniform(640, 1940); t = (x - 620) / 1340; y = 770 - 70 * t + rnd.uniform(-6, 8)
        b += f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{rnd.uniform(24, 50):.0f}" ry="{rnd.uniform(10, 18):.0f}" fill="{rnd.choice(["#6aa04a", "#8ab85a", "#4e8a42"])}" stroke="#1a3010" stroke-width="2.5"/>'
    for _ in range(14):   # hanging moss strands
        x = rnd.uniform(680, 1900); t = (x - 620) / 1340; y = 836 - 40 * t
        L = rnd.uniform(40, 140)
        b += f'<path d="M{x:.0f} {y:.0f} q{rnd.uniform(-10, 10):.0f} {L * .5:.0f} {rnd.uniform(-6, 6):.0f} {L:.0f}" fill="none" stroke="#6a9a5a" stroke-width="6" stroke-linecap="round" opacity=".85"/>'
    # ---- the spectacled bear sitting on the branch ----
    sd, so = spectacled(rnd, d)
    d += sd
    b += f'<g transform="translate(1290 762) scale(1.08)">{so}</g>'
    # frog in a knitted cap on the branch, looking up at the bear
    b += frog(965, 760, 2.25, flip=False, look=(7, -6), mouth='O', shadow=False, head=CHULLO, brows=False,
              armL='M-34 -22 q-14 -2 -18 -24', armR='M38 -22 q16 -6 22 -26')
    b += spark(1290, 300, 20, '#fffbe6') + spark(1560, 520, 14, '#fffbe6') + spark(1050, 560, 14, '#fffbe6')
    for _ in range(40):
        b += f'<circle cx="{rnd.uniform(900, 1900):.0f}" cy="{rnd.uniform(60, 720):.0f}" r="{rnd.choice([1.4, 2, 2.6])}" fill="#fffff0" opacity="{rnd.uniform(.2, .6):.2f}"/>'
    b += '<rect width="1920" height="1080" fill="url(#vig5)"/>'
    return d, b, [('LIVING', 170, 'w'), ('COUSIN', 214, 'y')], '#0a1a14'


# portrait recomposition (guideline 16-9, 2026-11-06: shorts thumbnails are 1080x1920, text centred near mid-screen):
# the landscape scene is scaled (s), centred on the subject (cx) and moved down (ty); above/below it the sky/ground colour continues.
V = {1: dict(s=.92, cx=1150, ty=664, top='#231a3a', bot='#140c12', ttop=460, lines=[('EYE', 176, 'w'), ('TO', 100, 'w'), ('EYE', 210, 'y')]),
     2: dict(s=.95, cx=1380, ty=775, top='#3d78b8', bot='#4a3e24', ttop=520, lines=[('RUNNING', 176, 'y'), ('BEAR?', 210, 'w')]),
     3: dict(s=1.05, cx=1320, ty=780, top='#0e1e2a', bot='#2a180c', ttop=500, lines=[('WHAT DID', 150, 'w'), ('IT EAT?', 220, 'y')]),
     4: dict(s=1.05, cx=1110, ty=640, top='#1a2a2c', bot='#0e0c08', ttop=470, lines=[('SLOW', 170, 'w'), ('SQUEEZE', 186, 'y')]),
     5: dict(s=1.1, cx=1220, ty=785, top='#1e3a3a', bot='#b8d0b4', ttop=500, lines=[('LIVING', 170, 'w'), ('COUSIN', 200, 'y')])}


def vertical(n):
    c = V[n]; fn = globals()[f'make_{n}']
    dd, bb, _, outline = fn(v=True) if n == 3 else fn()
    bb = bb.replace(f'<rect width="1920" height="1080" fill="url(#vig{n})"/>', '')
    s_, ty = c['s'], c['ty']; tx = 540 - c['cx'] * s_; bot_y = ty + 1080 * s_
    dd += lin('vext', [(0, c['top'], ), (1, c['top'])]).replace('stop-color="' + c['top'] + '"/></linearGradient>', 'stop-color="' + c['top'] + '" stop-opacity="0"/></linearGradient>')
    dd += rad('vvig', 540, 960, 1250, [(0, '#000', 0), (.62, '#000', 0), (1, '#05060a', .65)])
    rnd = random.Random(900 + n)
    o = f'<rect width="1080" height="1920" fill="{c["top"]}"/>'
    o += f'<g transform="translate({tx:.1f} {ty}) scale({s_})">{bb}</g>'
    o += f'<rect x="0" y="{ty - 2}" width="1080" height="{160}" fill="url(#vext)"/>'
    o += f'<rect x="0" y="{bot_y - 1:.0f}" width="1080" height="{1922 - bot_y:.0f}" fill="{c["bot"]}"/>'
    for _ in range(36):   # sparkles / dust in the extended sky
        o += f'<circle cx="{rnd.uniform(20, 1060):.0f}" cy="{rnd.uniform(80, ty + 60):.0f}" r="{rnd.choice([1.6, 2.2, 3])}" fill="#fff6dc" opacity="{rnd.uniform(.2, .6):.2f}"/>'
    o += spark(170, 300, 18, '#fff6d6') + spark(900, 420, 22, '#fff6d6') + spark(820, 180, 12, '#fff6d6')
    o += '<rect width="1080" height="1920" fill="url(#vvig)"/>'
    return dd, o, c['lines'], outline, c['ttop']


def build(n):
    out = os.path.join(REPO, 'videos', f'short-faced-bear-short{n}', 'thumb'); os.makedirs(out, exist_ok=True)
    for f in ('common.css', 'Fredoka-700.woff2'):   # portrait page css (tools/assets/thumb_v)
        shutil.copy(os.path.join(REPO, 'tools', 'assets', 'thumb_v', f), out)
    dd, bb, lines, outline, ttop = vertical(n)
    open(os.path.join(out, 'A.html'), 'w').write(vpage('#101010', vsvg(dd, bb), lines, outline=outline, top=ttop))
    print('short', n, 'ok')


if __name__ == '__main__':
    for n in (sys.argv[1:] or ['1', '2', '3', '4', '5']):
        build(int(n))
