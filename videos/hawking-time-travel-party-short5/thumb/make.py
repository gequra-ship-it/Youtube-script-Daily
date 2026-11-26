# Shorts thumbnail A for hawking-time-travel-party-short5 (style B, guideline 16-9). Run: python3 videos/hawking-time-travel-party-short5/thumb/make.py
# Hook  YOU CANNOT / GO BACK  -- script S01 "A cracked egg on your kitchen floor will never put itself back together. ... it is the real
#        reason you cannot go back."; S05 "That steady rise of entropy gives the universe an arrow of time."
# Scene: on a dark kitchen counter a whole egg glows gold (past, left); a huge glowing arrow of time arcs over to the right, where the
#        same egg lies cracked, yolk and shell spread out (S03 "yolk and shell spread out in a mess"). Below the text, a tiled kitchen
#        floor with scattered shell bits fading into the dark. Chef frog bottom-right looks back at the broken egg. No people drawn.
import os, sys, math, random
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', 'hawking-time-travel-party-short1', 'thumb'))
from hshort_common import *

r = random.Random(55)
defs = FILTERS + vig(a=.82)
defs += lin('sky', [(0, '#06040c'), (.5, '#140c22'), (1, '#05040a')])
defs += halo('hal', 300, 600, 460, inner='#fff1b0', outer='#ff9a3c')
defs += halo('hal2', 790, 660, 380, inner='#ffd27a', outer='#b04a9a')
defs += rad('shell', 280, 520, 230, [(0, '#ffffff', 1), (.55, '#fbf0dc', 1), (1, '#d9c09a', 1)])
defs += rad('yolk', 770, 690, 90, [(0, '#fff2a0', 1), (.45, '#ffc02a', 1), (1, '#e08a0a', 1)])
defs += lin('counter', [(0, '#3a2a48'), (1, '#120a1c')])
defs += lin('arrow', [(0, '#fff6c8'), (.5, '#ffd25a'), (1, '#ff8a3c')], x2=1, y2=0)
b = f'<rect width="{W}" height="{H}" fill="url(#sky)"/>'
b += stars(r, 150, 0, 820, col='#f0e6ff', big=5)
b += f'<ellipse cx="300" cy="600" rx="520" ry="520" fill="url(#hal)" opacity=".6"/>'
b += f'<ellipse cx="790" cy="660" rx="420" ry="400" fill="url(#hal2)" opacity=".4"/>'
# ---- counter top ----
b += '<path d="M0 760 L1080 760 L1080 860 L0 860z" fill="url(#counter)"/><path d="M0 760 H1080" stroke="#b89ad0" stroke-width="4" opacity=".6"/>'
# ---- arrow of time: big glowing arc from the whole egg to the broken one ----
d = 'M200 330 Q540 60 900 380'
b += f'<path d="{d}" fill="none" stroke="#ffb03c" stroke-width="80" opacity=".28" filter="url(#b24)"/>'
b += f'<path d="{d}" fill="none" stroke="url(#arrow)" stroke-width="34" stroke-linecap="round"/>'
b += f'<path d="{d}" fill="none" stroke="#fffbe8" stroke-width="9" stroke-linecap="round" opacity=".9"/>'
ang = math.degrees(math.atan2(380 - 220, 900 - 720))
b += f'<path transform="translate(900 380) rotate({ang:.0f})" d="M-10 -52 L70 0 L-10 52z" fill="#ff9a3c" stroke="#fff3c4" stroke-width="7" stroke-linejoin="round"/>'
for t in (.18, .36, .54, .72):   # clock ticks riding the arrow
    x = (1 - t) ** 2 * 200 + 2 * (1 - t) * t * 540 + t * t * 900
    y = (1 - t) ** 2 * 330 + 2 * (1 - t) * t * 60 + t * t * 380
    b += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="9" fill="#5a2a0a" stroke="#fff6d6" stroke-width="3.5"/>'
b += clockface(540, 236, 52, 2, 10, face='#fffbea', rim='#e2b34a', glow='#fff3a8')
# ---- the whole egg (left), glowing ----
EX, EY = 290, 560
b += f'<ellipse cx="{EX}" cy="{EY + 196}" rx="150" ry="22" fill="#000" opacity=".5" filter="url(#b12)"/>'
b += f'<ellipse cx="{EX}" cy="{EY}" rx="220" ry="260" fill="#fff1b0" opacity=".35" filter="url(#b24)"/>'
egg = f'M{EX} {EY - 200} C{EX + 120} {EY - 200} {EX + 155} {EY + 40} {EX + 150} {EY + 90} C{EX + 140} {EY + 200} {EX - 140} {EY + 200} {EX - 150} {EY + 90} C{EX - 155} {EY + 40} {EX - 120} {EY - 200} {EX} {EY - 200}z'
b += f'<path d="{egg}" fill="url(#shell)" stroke="#2a1606" stroke-width="7"/>'
b += f'<path d="M{EX - 90} {EY - 70} Q{EX - 70} {EY - 160} {EX - 10} {EY - 178}" fill="none" stroke="#fff" stroke-width="16" stroke-linecap="round" opacity=".85"/>'
b += f'<path d="M{EX + 110} {EY + 70} Q{EX + 90} {EY + 150} {EX + 20} {EY + 170}" fill="none" stroke="#c9a878" stroke-width="10" stroke-linecap="round" opacity=".6"/>'
b += sparkles([(EX - 190, EY - 150, 26), (EX + 175, EY - 120, 20), (EX - 200, EY + 120, 16), (EX + 40, EY - 260, 14)], '#fffbe0')
# ---- the broken egg (right): yolk puddle, white spill, jagged shell halves ----
BX, BY = 790, 700
b += f'<path d="M{BX - 230} {BY + 20} q30 -60 120 -50 q60 -40 140 -10 q90 -20 120 40 q40 30 -10 60 q-80 30 -180 20 q-120 20 -190 -60z" fill="#fbf4e6" stroke="#2a1606" stroke-width="5" opacity=".95"/>'
b += f'<ellipse cx="{BX - 20}" cy="{BY - 10}" rx="86" ry="54" fill="url(#yolk)" stroke="#7a3a04" stroke-width="5"/>'
b += f'<ellipse cx="{BX - 44}" cy="{BY - 30}" rx="26" ry="12" fill="#fff" opacity=".8"/>'
def half(x, y, rot, flipy=False):
    p = ('M-70 0 C-70 -70 -30 -110 0 -110 C30 -110 70 -70 70 0 L50 -14 L34 6 L16 -18 L0 4 L-18 -16 L-34 6 L-52 -12z')
    return f'<g transform="translate({x} {y}) rotate({rot})"><path d="{p}" fill="url(#shell)" stroke="#2a1606" stroke-width="5" stroke-linejoin="round"/><path d="M-40 -50 q8 -34 36 -44" fill="none" stroke="#fff" stroke-width="7" opacity=".8" stroke-linecap="round"/></g>'
b += half(BX - 170, BY - 20, -58) + half(BX + 140, BY + 4, 64)
for _ in range(16):   # shell bits spread out
    x = r.uniform(BX - 260, BX + 260); y = r.uniform(BY + 20, BY + 70); s = r.uniform(8, 20)
    b += f'<path transform="translate({x:.0f} {y:.0f}) rotate({r.uniform(0, 360):.0f})" d="M0 {-s:.0f} L{s * .9:.0f} {s * .4:.0f} L{-s * .7:.0f} {s * .6:.0f}z" fill="#f6ead2" stroke="#2a1606" stroke-width="2.4"/>'
b += sparkles([(BX + 210, BY - 150, 18), (BX - 80, BY - 170, 14)], '#ffe6a8')
b += fireflies(40, 120, 1850, col='#ffd9a0', core='#fff6e0', seed=5)
# ---- kitchen floor (below the text) ----
b += '<path d="M0 1300 H1080 V1920 H0z" fill="#1a1222"/>'
for k in range(9):
    y = 1300 + (k ** 1.6) * 22
    b += f'<path d="M0 {y:.0f} H1080" stroke="#3a2a4a" stroke-width="{2 + k * .5:.1f}"/>'
for k in range(-6, 17):
    x0 = 540 + (k - 5) * 70; x1 = 540 + (k - 5) * 240
    b += f'<path d="M{x0} 1300 L{x1} 1920" stroke="#3a2a4a" stroke-width="3"/>'
b += '<ellipse cx="540" cy="1300" rx="700" ry="60" fill="#ffb03c" opacity=".12" filter="url(#b24)"/>'
for _ in range(26):   # shell crumbs scattered across the floor
    x = r.uniform(80, 760); y = r.uniform(1340, 1860); s = r.uniform(8, 18) * (1 + (y - 1300) / 900)
    b += f'<path transform="translate({x:.0f} {y:.0f}) rotate({r.uniform(0, 360):.0f})" d="M0 {-s:.0f} L{s * .9:.0f} {s * .4:.0f} L{-s * .7:.0f} {s * .6:.0f}z" fill="#e8dcc4" stroke="#1a0e06" stroke-width="2.4" opacity="{r.uniform(.5, .9):.2f}"/>'
b += '<path d="M260 1520 q60 -30 150 -10 q80 -20 120 30 q-10 40 -120 40 q-120 10 -150 -60z" fill="#f2ead8" opacity=".55"/>'
b += '<ellipse cx="400" cy="1530" rx="44" ry="26" fill="url(#yolk)" opacity=".8"/>'
b += darkband(860, 1250, .5)
# ---- chef frog bottom-right, looking back up at the broken egg ----
FX, FY, FS = 840, 1790, 2.9
b += f'<ellipse cx="{FX}" cy="{FY + 8}" rx="100" ry="15" fill="#000" opacity=".45"/>'
b += f'<ellipse cx="{FX}" cy="{FY - 130}" rx="190" ry="190" fill="#ffd9a0" opacity=".12" filter="url(#b24)"/>'
hat = ('<path d="M-26 -88 v-18 q-20 -4 -16 -24 q4 -18 22 -14 q6 -18 26 -16 q20 2 22 20 q18 -4 22 14 q2 18 -18 22 v16z" fill="#fff" stroke-width="3.4"/>'
       '<path d="M-26 -92 h56" stroke-width="3"/>')
apron = ('<path d="M-22 4 q-4 -20 -2 -30 h48 q2 10 -2 30z" fill="#f4f0e8" stroke-width="3.2"/>'
         '<path d="M-24 -26 q24 -10 48 0" fill="none" stroke-width="2.6"/>')
spoon = ('<g transform="translate(-60 -44) rotate(-30)"><path d="M0 0 v-46" stroke="#8a5a2e" stroke-width="6"/>'
         '<ellipse cx="0" cy="-56" rx="11" ry="15" fill="#c9d0dc" stroke-width="3"/></g>')
b += frog(FX, FY, FS, look=(-5, -5), mouth='O', mid=apron, top=hat, front=spoon,
          armL='M-34 -22 q-18 -6 -24 -22', armR='M38 -24 q14 6 16 22')
b += f'<rect width="{W}" height="{H}" fill="url(#vig)"/>'
write(HERE, '#06040c', defs, b, [('YOU CANNOT', 120, 'w'), ('GO BACK', 196, 'y')], outline='#0a0414', top=905)
