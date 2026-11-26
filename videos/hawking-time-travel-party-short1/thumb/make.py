# Shorts thumbnail A for hawking-time-travel-party-short1 (style B, guideline 16-9). Run: python3 videos/hawking-time-travel-party-short1/thumb/make.py
# Hook  NOBODY / CAME  -- script S01 "Champagne on ice, balloons on the ceiling, and a banner ... Nobody came, and that was the point."
# Scene (front view, unlike long B's corridor): a tall doorway glowing with a starry time tunnel stands open at the back of a dark
#        party room (S04 "set a machine to the right place and moment, and walk through the door"); bunting, balloons on the ceiling;
#        in front an empty round table with champagne on ice and untouched glasses. Waiter frog (bow tie, towel) waits bottom-left.
import os, sys, math, random
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from hshort_common import *

r = random.Random(11)
defs = FILTERS + vig(a=.8)
defs += lin('wall', [(0, '#0a0618'), (.6, '#1c0f33'), (1, '#120a24')])
defs += lin('floor', [(0, '#2a1840'), (1, '#07040e')])
defs += halo('hal', 540, 520, 600, inner='#f4fbff', outer='#8a7cff')
defs += rad('tun', 540, 470, 260, [(0, '#ffffff', 1), (.18, '#d8f0ff', .95), (.5, '#5a6cff', .9), (1, '#160a40', 1)])
defs += lin('wood', [(0, '#5a3418'), (.5, '#8a5428'), (1, '#4a2810')], x2=1, y2=0)
defs += lin('cloth', [(0, '#f4f0ff'), (1, '#9a90c0')])
defs += lin('bucket', [(0, '#7a7f8c'), (.35, '#eef2f6'), (.6, '#b8bec8'), (1, '#5a5f6c')], x2=1, y2=0)
defs += lin('bottle', [(0, '#0a2a18'), (.4, '#2f7a4a'), (1, '#0a2414')], x2=1, y2=0)
defs += lina('ray', [(0, '#e8f0ff', .35), (1, '#e8f0ff', 0)])
b = f'<rect width="{W}" height="{H}" fill="url(#wall)"/>'
# wall panels
for x in (60, 820):
    b += f'<rect x="{x}" y="300" width="200" height="460" rx="8" fill="none" stroke="#2c1a48" stroke-width="6"/>'
b += f'<ellipse cx="540" cy="520" rx="640" ry="600" fill="url(#hal)" opacity=".75"/>'
# floor
b += f'<path d="M0 820 H1080 V1920 H0z" fill="url(#floor)"/>'
for k in range(1, 9):
    y = 820 + k * k * 14
    b += f'<path d="M0 {y} H1080" stroke="#3a2456" stroke-width="2" opacity=".5"/>'
for k in range(-8, 9):
    b += f'<path d="M{540 + k * 40} 820 L{540 + k * 260} 1920" stroke="#3a2456" stroke-width="2" opacity=".45"/>'
# light spilling from the door onto the floor
b += f'<path d="M370 820 L700 820 L1000 1920 L60 1920z" fill="url(#ray)"/>'
b += f'<ellipse cx="540" cy="880" rx="260" ry="40" fill="#cfe0ff" opacity=".5" filter="url(#b24)"/>'
# ---- the glowing doorway ----
DX0, DX1, DY0, DY1 = 370, 710, 250, 820
arch = f'M{DX0} {DY1} V{DY0 + 170} A170 170 0 0 1 {DX1} {DY0 + 170} V{DY1}z'
b += f'<path d="M{DX0 - 46} {DY1} V{DY0 + 170} A216 216 0 0 1 {DX1 + 46} {DY0 + 170} V{DY1}z" fill="url(#wood)" stroke="#1a0c04" stroke-width="6"/>'
b += f'<path d="M{DX0 - 30} {DY1} V{DY0 + 170} A200 200 0 0 1 {DX1 + 30} {DY0 + 170} V{DY1}" fill="none" stroke="#e2b34a" stroke-width="5"/>'
b += f'<path d="{arch}" fill="url(#tun)" stroke="#1a0c04" stroke-width="6"/>'
defs += f'<clipPath id="door"><path d="{arch}"/></clipPath>'
g = '<g clip-path="url(#door)">'
for k in range(14):   # spiral tunnel rings
    rr = 18 + k * k * 2.2
    g += f'<ellipse cx="540" cy="{470 + k * 6}" rx="{rr * 1.0:.0f}" ry="{rr * 1.25:.0f}" fill="none" stroke="#ffffff" stroke-width="{1.5 + k * .3:.1f}" opacity="{.75 - k * .045:.2f}"/>'
for i in range(140):
    a = i * .55; rr = 6 + i * 2.1
    x, y = 540 + rr * math.cos(a), 470 + rr * 1.25 * math.sin(a)
    g += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{1 + i / 60:.1f}" fill="#fff" opacity=".85"/>'
g += '</g>'
b += g
b += f'<circle cx="540" cy="470" r="60" fill="#fff" opacity=".9" filter="url(#b24)"/>'
# open door leaf swung toward the viewer on the right
b += f'<path d="M{DX1} {DY0 + 120} L{DX1 + 120} {DY0 + 60} L{DX1 + 120} {DY1 + 40} L{DX1} {DY1}z" fill="#3a2010" stroke="#1a0c04" stroke-width="6"/>'
b += f'<path d="M{DX1 + 20} {DY0 + 150} L{DX1 + 100} {DY0 + 110} L{DX1 + 100} {DY0 + 380} L{DX1 + 20} {DY0 + 400}z M{DX1 + 20} {DY0 + 450} L{DX1 + 100} {DY0 + 440} L{DX1 + 100} {DY1 + 10} L{DX1 + 20} {DY1 - 10}z" fill="none" stroke="#6a4020" stroke-width="5"/>'
b += f'<circle cx="{DX1 + 96}" cy="{DY0 + 420}" r="9" fill="#e2b34a" stroke="#1a0c04" stroke-width="3"/>'
b += f'<path d="M{DX1} {DY0 + 120} L{DX1 + 120} {DY0 + 60}" stroke="#cfe0ff" stroke-width="4" opacity=".7"/>'
b += f'<path d="M{DX0 - 46} {DY1} H{DX1 + 120}" stroke="#0a0408" stroke-width="10"/>'
# ---- bunting garlands (banner) ----
cols = ['#e0566a', '#f2d27a', '#5ab4e0', '#7ad08a', '#c08aff']
def garland(x0, y0, x1, y1, sag, n):
    o = f'<path d="M{x0} {y0} Q{(x0 + x1) / 2} {max(y0, y1) + sag} {x1} {y1}" fill="none" stroke="#e8dcc0" stroke-width="3"/>'
    for i in range(n):
        t = (i + .5) / n; x = (1 - t) ** 2 * x0 + 2 * t * (1 - t) * (x0 + x1) / 2 + t * t * x1
        y = (1 - t) ** 2 * y0 + 2 * t * (1 - t) * (max(y0, y1) + sag) + t * t * y1
        o += f'<path d="M{x - 20:.0f} {y:.0f} L{x + 20:.0f} {y:.0f} L{x:.0f} {y + 46:.0f}z" fill="{cols[i % 5]}" stroke="#1a0c24" stroke-width="3"/>'
        o += f'<path d="M{x - 12:.0f} {y + 4:.0f} L{x - 2:.0f} {y + 30:.0f}" stroke="#fff" stroke-width="3" opacity=".45"/>'
    return o
b += garland(-10, 170, 330, 300, 80, 7) + garland(750, 300, 1090, 170, 80, 7)
# ---- balloons on the ceiling ----
def balloon(x, y, rr, col, hi, tail=280, sway=20):
    o = f'<path d="M{x} {y + rr * 1.15:.0f} q{sway} {tail * .4:.0f} {-sway * .4:.0f} {tail * .7:.0f} t{sway * .5:.0f} {tail * .3:.0f}" fill="none" stroke="#e8dcc0" stroke-width="2.4" opacity=".8"/>'
    o += f'<ellipse cx="{x}" cy="{y}" rx="{rr}" ry="{rr * 1.15:.0f}" fill="{col}" stroke="#1a0c24" stroke-width="4"/>'
    o += f'<path d="M{x - 9} {y + rr * 1.15 + 12:.0f} L{x} {y + rr * 1.15 - 2:.0f} L{x + 9} {y + rr * 1.15 + 12:.0f}z" fill="{col}" stroke="#1a0c24" stroke-width="3"/>'
    o += f'<ellipse cx="{x - rr * .35:.0f}" cy="{y - rr * .45:.0f}" rx="{rr * .2:.0f}" ry="{rr * .32:.0f}" fill="{hi}" opacity=".75" transform="rotate(-25 {x - rr * .35:.0f} {y - rr * .45:.0f})"/>'
    o += f'<path d="M{x + rr * .75:.0f} {y - rr * .2:.0f} a{rr} {rr * 1.15:.0f} 0 0 1 {-rr * .5:.0f} {rr * .95:.0f}" fill="none" stroke="#cfe0ff" stroke-width="5" opacity=".55"/>'
    return o
for x, y, rr, c, hi, t, s in ((90, 230, 62, '#e0566a', '#ffc0c8', 360, 18), (210, 210, 58, '#f2d27a', '#fff6d0', 420, -16), (150, 330, 52, '#5ab4e0', '#d0f0ff', 300, 12),
                              (990, 230, 62, '#c08aff', '#ecd8ff', 360, -18), (870, 205, 56, '#7ad08a', '#dcffe0', 430, 16), (940, 335, 50, '#e0566a', '#ffc0c8', 290, -12)):
    b += balloon(x, y, rr, c, hi, t, s)
b += sparkles([(540, 200, 26), (300, 470, 18), (790, 500, 20), (250, 640, 14), (840, 700, 16), (460, 760, 12)], '#f4f8ff')
b += fireflies(40, 160, 1850, col='#c8b8ff', core='#f4f0ff', seed=3)
# confetti on the floor
for _ in range(90):
    x, y = r.uniform(20, 1060), r.uniform(1260, 1880)
    b += f'<rect x="{x:.0f}" y="{y:.0f}" width="12" height="6" rx="2" fill="{r.choice(cols)}" opacity=".8" transform="rotate({r.uniform(0, 180):.0f} {x:.0f} {y:.0f})"/>'
# ---- empty chairs behind the table ----
def chair(x, y, s=1):
    return (f'<g transform="translate({x} {y}) scale({s})"><path d="M-60 0 L-66 -240 Q0 -270 66 -240 L60 0z" fill="#6a1e2a" stroke="#1a060a" stroke-width="5"/>'
            f'<path d="M-44 -30 L-48 -220 Q0 -240 48 -220 L44 -30z" fill="#8a2a38" stroke="#1a060a" stroke-width="3"/>'
            f'<path d="M-40 -210 Q0 -228 40 -210" stroke="#e2b34a" stroke-width="4" fill="none"/></g>')
b += chair(330, 1500, .85) + chair(750, 1500, .85)
# ---- round table with champagne on ice ----
TX, TY = 540, 1460
b += f'<ellipse cx="{TX}" cy="1790" rx="360" ry="40" fill="#000" opacity=".5" filter="url(#b12)"/>'
b += f'<path d="M{TX - 330} {TY} Q{TX - 350} 1640 {TX - 310} 1780 Q{TX} 1820 {TX + 310} 1780 Q{TX + 350} 1640 {TX + 330} {TY}z" fill="url(#cloth)" stroke="#2a1a40" stroke-width="5"/>'
for dx in (-220, -110, 0, 110, 220):
    b += f'<path d="M{TX + dx} {TY + 40} Q{TX + dx * 1.08:.0f} 1650 {TX + dx * 1.04:.0f} 1790" fill="none" stroke="#8a80b0" stroke-width="3" opacity=".6"/>'
b += f'<ellipse cx="{TX}" cy="{TY}" rx="330" ry="66" fill="#fbf8ff" stroke="#2a1a40" stroke-width="5"/>'
b += f'<ellipse cx="{TX}" cy="{TY - 10}" rx="290" ry="44" fill="#dcd4ff" opacity=".35"/>'
b += f'<ellipse cx="{TX}" cy="{TY}" rx="200" ry="40" fill="#cfe0ff" opacity=".35" filter="url(#b12)"/>'
# plates
for px in (TX - 210, TX + 210):
    b += f'<ellipse cx="{px}" cy="{TY + 18}" rx="56" ry="13" fill="#fff" stroke="#6a6090" stroke-width="3"/><ellipse cx="{px}" cy="{TY + 18}" rx="36" ry="8" fill="none" stroke="#c8c0e8" stroke-width="2"/>'
# glasses (flutes, empty)
def flute(x, y, s=1, fill=0):
    o = f'<g transform="translate({x} {y}) scale({s})"><ellipse cx="0" cy="0" rx="18" ry="5" fill="#cfe0ff" opacity=".6" stroke="#5a6080" stroke-width="2"/>'
    o += '<path d="M0 0 v-40" stroke="#dfe8ff" stroke-width="4"/>'
    o += '<path d="M-13 -40 q-4 -46 2 -86 h22 q6 40 2 86 q-13 8 -26 0z" fill="#e8f2ff" fill-opacity=".35" stroke="#dfe8ff" stroke-width="3"/>'
    o += '<path d="M-6 -50 q-3 -30 0 -66" stroke="#fff" stroke-width="3" opacity=".9"/></g>'
    return o
for x, y in ((TX - 130, TY + 6), (TX - 90, TY + 26), (TX + 100, TY + 26), (TX + 140, TY + 4)):
    b += flute(x, y, 1.05)
# ice bucket with the champagne bottle
BX, BY = TX, TY + 10
b += f'<ellipse cx="{BX}" cy="{BY - 150}" rx="140" ry="120" fill="#f2d27a" opacity=".3" filter="url(#b24)"/>'
b += f'<g transform="rotate(14 {BX} {BY - 60})"><path d="M{BX - 22} {BY - 60} V{BY - 150} q0 -26 12 -36 V{BY - 200} h20 V{BY - 186} q12 10 12 36 V{BY - 60}z" fill="url(#bottle)" stroke="#04140a" stroke-width="4"/>'
b += f'<rect x="{BX - 12}" y="{BY - 214}" width="24" height="30" rx="4" fill="#e2b34a" stroke="#3a2406" stroke-width="3"/>'
b += f'<rect x="{BX - 20}" y="{BY - 140}" width="40" height="40" rx="4" fill="#f4ecd0" stroke="#3a2406" stroke-width="3"/><path d="M{BX - 12} {BY - 124} h24 M{BX - 12} {BY - 114} h18" stroke="#c9952e" stroke-width="3"/>'
b += f'<path d="M{BX - 14} {BY - 180} v100" stroke="#8fd0a8" stroke-width="4" opacity=".7"/></g>'
b += f'<path d="M{BX - 72} {BY - 92} L{BX - 58} {BY} H{BX + 58} L{BX + 72} {BY - 92}z" fill="url(#bucket)" stroke="#2a2e38" stroke-width="5"/>'
b += f'<ellipse cx="{BX}" cy="{BY - 92}" rx="74" ry="16" fill="#cfe8f4" stroke="#2a2e38" stroke-width="4"/>'
for ix, iy in ((-46, -98), (-20, -104), (26, -100), (50, -96), (6, -94)):
    b += f'<path d="M{BX + ix} {BY + iy} l14 -8 l12 6 l-4 14 l-16 2z" fill="#eaf8ff" stroke="#7ab0c8" stroke-width="2"/>'
b += f'<path d="M{BX - 76} {BY - 70} h-12 v26 h12 M{BX + 76} {BY - 70} h12 v26 h-12" fill="none" stroke="#2a2e38" stroke-width="5"/>'
b += f'<path d="M{BX - 48} {BY - 80} L{BX - 40} {BY - 10}" stroke="#fff" stroke-width="6" opacity=".7"/>'
b += sparkles([(BX + 90, BY - 210, 18), (BX - 120, BY - 150, 14), (BX + 200, BY - 70, 12)], '#fff6d6')
b += darkband(860, 1240, .5)
# ---- waiter frog, bottom-left: bow tie, white towel over the arm, looking at the door ----
FX, FY, FS = 196, 1790, 2.9
b += f'<ellipse cx="{FX}" cy="{FY + 8}" rx="100" ry="15" fill="#000" opacity=".45"/>'
b += f'<ellipse cx="{FX}" cy="{FY - 120}" rx="190" ry="190" fill="#c8b8ff" opacity=".14" filter="url(#b24)"/>'
vest = ('<path d="M-34 0 q-4 -24 2 -34 q36 -8 72 0 q8 12 2 34 q-38 8 -76 0z" fill="#1e1e2c" stroke-width="3.4"/>'
        '<path d="M-8 -34 L4 -6 L16 -34" fill="#f4f4f8" stroke-width="2.6"/>'
        '<circle cx="4" cy="-4" r="2.4" fill="#e2b34a" stroke="none"/><circle cx="4" cy="4" r="2.4" fill="#e2b34a" stroke="none"/>')
bowtie = '<path d="M3 -28 l-15 -8 v16z M7 -28 l15 -8 v16z" fill="#c0392b" stroke-width="2.6"/><circle cx="5" cy="-28" r="4" fill="#8a1e1e" stroke-width="2"/>'
towel = '<path d="M-52 -14 q-6 14 -4 34 h14 q-2 -18 4 -32z" fill="#ffffff" stroke-width="2.6"/><path d="M-50 4 h10" stroke="#c8c8d8" stroke-width="2"/>'
b += frog(FX, FY, FS, look=(4, -5), mouth='O', mid=vest + bowtie, front=towel, sleeve='#1e1e2c',
          armL='M-34 -22 q-18 4 -18 10', armR='M38 -24 q14 -4 20 -24')
b += f'<rect width="{W}" height="{H}" fill="url(#vig)"/>'
write(HERE, '#0a0618', defs, b, [('NOBODY', 230, 'y'), ('CAME', 230, 'w')], outline='#0a0418', top=880)
