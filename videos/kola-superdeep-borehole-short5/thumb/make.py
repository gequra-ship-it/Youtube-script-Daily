# Shorts thumbnail A for kola-superdeep-borehole-short5 (style B, guideline 16-9). Run: python3 videos/kola-superdeep-borehole-short5/thumb/make.py
# Hook  12 KM / STRAIGHT DOWN  -- script S01 "a pitch-black vertical shaft dropping twelve thousand two hundred sixty-two meters straight down";
#        S05 "a twelve-kilometer wound in the planet".
# Scene: Arctic ghost town at night (aurora, concrete skeleton with rusted rebar); a lone rusted bolted cap on broken concrete in the snow
#        (S01 "A rusted metal disc barely wider than a dinner plate sits bolted to broken concrete"); below it a cut-away of the rock with a
#        beam of light running down the thin shaft into darkness. Hard-hat frog with a lantern in a rock pocket bottom-left.
import os, sys, math, random
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', 'kola-superdeep-borehole-short1', 'thumb'))
from kshort_common import *

r = random.Random(65)
G = 650          # surface (cut edge)
CX, CY = 540, 600
defs = FILTERS + vig(a=.8)
defs += lin('sky', [(0, '#030817'), (.6, '#0c2244'), (1, '#20406a')])
defs += lina('aur', [(0, '#5cf2b0', 0), (.5, '#5cf2b0', .6), (1, '#2fb6a0', 0)])
defs += halo('hal', CX, CY, 460, inner='#fff3c8', outer='#ffb36a')
defs += lin('snow', [(0, '#dfe8f6'), (1, '#8ea4c4')])
defs += lin('rock', [(0, '#3a3a50'), (.3, '#24243a'), (.7, '#121222'), (1, '#04040a')])
defs += lin('shaft', [(0, '#fffbe8'), (.25, '#ffe2a0'), (.7, '#ff9a4a'), (1, '#ff9a4a')])
defs += lina('beam', [(0, '#fff3c8', .55), (.6, '#ffcf8a', .18), (1, '#ffcf8a', 0)])
defs += lin('rust', [(0, '#d27a44'), (.5, '#8a3c22'), (1, '#4e2216')], x2=1, y2=0)
b = f'<rect width="{W}" height="{H}" fill="url(#sky)"/>'
b += stars(r, 120, 0, 480)
b += aurora(((-100, 60, .5), (260, 90, .65), (620, 70, .55)), y=70, h=300)
# ghost-town ruins on the horizon: concrete skeleton with rebar, broken derrick
b += f'<path d="M0 560 Q260 520 540 540 T1080 530 V620 H0z" fill="#26405f"/>'
b += f'<path d="M60 560 V390 H300 V560 M60 450 H300 M140 390 V560 M220 390 V560" fill="none" stroke="#15253c" stroke-width="16"/>'
b += f'<path d="M300 390 l20 -30 M260 390 l10 -40 M60 390 l-14 -36" stroke="#6a3a22" stroke-width="5"/>'
b += f'<path d="M820 560 l30 -230 l30 230 M830 490 h40 M838 420 h24 M830 490 l36 -60 M870 490 l-36 -60" fill="none" stroke="#15253c" stroke-width="7"/>'
b += f'<path d="M850 330 l40 30" stroke="#15253c" stroke-width="7"/>'
b += f'<ellipse cx="{CX}" cy="{CY}" rx="520" ry="420" fill="url(#hal)" opacity=".7"/>'
# ---- cut-away below the surface: dark rock layers getting blacker with depth ----
b += f'<rect y="{G}" width="{W}" height="{H - G}" fill="url(#rock)"/>'
y = G + 50
for k in range(9):
    pts = jag((-20, y), (1100, y + 10), 18, 10, 70 + k)
    b += f'<polyline points="{P(pts)}" fill="none" stroke="{mix(["#6a6a88", "#2a2a40"], k / 8)}" stroke-width="3" opacity="{.7 - k * .06:.2f}"/>'
    y += 70 + k * 14
b += crystals(r, 380, 0, G + 20, W, H, ['#8a8aa8', '#5a5a78', '#a07a6a'], 4, 12, .1, .35, skip=lambda x, y: abs(x - CX) < 40)
# the beam of light running down the shaft
b += f'<path d="M{CX - 60} {G} L{CX - 200} {H} L{CX + 200} {H} L{CX + 60} {G}z" fill="url(#beam)" filter="url(#b14)"/>'
b += f'<rect x="{CX - 40}" y="{G}" width="80" height="{H - G}" fill="#ffd27a" opacity=".3" filter="url(#b14)"/>'
b += f'<rect x="{CX - 15}" y="{G}" width="30" height="{H - G}" fill="#05050a"/>'
b += f'<rect x="{CX - 9}" y="{G + 4}" width="18" height="{H - G}" fill="url(#shaft)"/>'
b += f'<rect x="{CX - 3}" y="{G + 4}" width="6" height="{H - G}" fill="#ffffff" opacity=".8"/>'
defs += lina('fade', [(0, '#04040a', 0), (1, '#04040a', 1)])
b += f'<rect y="1560" width="{W}" height="{H - 1560}" fill="url(#fade)"/>'
# snow surface strip + the cut edge
b += f'<path d="M-20 {G - 60} Q260 {G - 80} 540 {G - 64} T1100 {G - 66} V{G + 6} H-20z" fill="url(#snow)"/>'
b += f'<path d="M-20 {G + 4} H1100" stroke="#ffffff" stroke-width="4" opacity=".8"/>'
# broken concrete slab under the cap + rebar
b += f'<path d="M260 {G - 12} L300 {G - 70} L780 {G - 80} L830 {G - 14} Z" fill="#7c8597" stroke="#2a3040" stroke-width="5"/>'
b += f'<path d="M300 {G - 70} L780 {G - 80}" stroke="#e8f0ff" stroke-width="10" opacity=".9"/>'
b += f'<path d="M420 {G - 74} l-20 30 l18 20 M690 {G - 78} l16 26 l-12 24" fill="none" stroke="#2a3040" stroke-width="4"/>'
for d in (f'M300 {G - 60} q-30 -50 0 -90 q20 -30 -10 -60', f'M800 {G - 40} q40 -40 20 -80'):
    b += f'<path d="{d}" fill="none" stroke="#2a1a14" stroke-width="10" stroke-linecap="round"/><path d="{d}" fill="none" stroke="#b5562a" stroke-width="5" stroke-linecap="round"/>'
# ---- the rusted bolted cap ----
RX, RY, TH, cy = 210, 62, 26, CY - 40
b += f'<ellipse cx="{CX}" cy="{cy + TH + 8}" rx="{RX + 30}" ry="{RY + 12}" fill="#000" opacity=".35" filter="url(#b8)"/>'
b += f'<path d="M{CX - RX} {cy} v{TH} a{RX} {RY} 0 0 0 {2 * RX} 0 v{-TH}z" fill="#5a2a18" stroke="#1a0c08" stroke-width="5"/>'
b += f'<ellipse cx="{CX}" cy="{cy}" rx="{RX}" ry="{RY}" fill="url(#rust)" stroke="#1a0c08" stroke-width="5"/>'
b += f'<ellipse cx="{CX}" cy="{cy}" rx="{RX - 30}" ry="{RY - 9}" fill="none" stroke="#3a180e" stroke-width="4"/>'
b += f'<ellipse cx="{CX}" cy="{cy}" rx="{RX - 36}" ry="{RY - 12}" fill="none" stroke="#f0a070" stroke-width="2.5" opacity=".6" stroke-dasharray="8 6"/>'
for k in range(12):
    a = k * math.pi / 6
    bx, by = CX + (RX - 14) * math.cos(a), cy + (RY - 6) * math.sin(a)
    b += f'<ellipse cx="{bx:.1f}" cy="{by:.1f}" rx="10" ry="6.5" fill="#9a5a3a" stroke="#1a0c08" stroke-width="3"/><ellipse cx="{bx - 2:.1f}" cy="{by - 2:.1f}" rx="3.5" ry="2" fill="#ffd0a0"/>'
for k in range(7):
    x = CX - 150 + k * 50
    b += f'<path d="M{x} {cy + 10} q5 12 0 {20 + k % 3 * 8}" stroke="#3a180e" stroke-width="3.5" opacity=".6"/>'
b += f'<path d="M{CX - 150} {cy - 14} q60 -36 130 -32 q-12 22 -60 30 q-36 8 -70 2z" fill="#f3f8ff"/>'
b += f'<path d="M{CX - RX + 14} {cy - 18} a{RX} {RY} 0 0 1 {RX * 1.3:.0f} {-RY + 8}" fill="none" stroke="#ffe0b0" stroke-width="5" opacity=".9"/>'
b += sparkles([(CX - 260, CY - 150, 24), (CX + 270, CY - 120, 18), (CX + 40, CY - 210, 16), (CX - 120, 1500, 14), (CX + 150, 1650, 16)], '#fff6d6')
b += fireflies(42, 100, 1850, col='#ffe2a0', core='#fff8e0', seed=34)
b += darkband(860, 1240, .5)
# rock pocket bottom-left with the frog (hard hat, lantern)
PX, PY = 235, 1610
b += f'<path d="M{PX - 215} {PY + 150} Q{PX - 225} {PY - 180} {PX} {PY - 200} Q{PX + 225} {PY - 180} {PX + 215} {PY + 150}z" fill="#0a0a14" stroke="#ffcf8a" stroke-width="4" opacity=".95"/>'
b += f'<path d="M{PX - 215} {PY + 150} H{PX + 215}" stroke="#ffcf8a" stroke-width="5"/>'
b += f'<ellipse cx="{PX + 60}" cy="{PY + 40}" rx="200" ry="160" fill="#ffcf8a" opacity=".16" filter="url(#b24)"/>'
FX, FY, FS = PX - 10, PY + 146, 2.9
lantern = ('<g transform="translate(56 -36)"><path d="M-9 -4 Q0 -24 9 -4" fill="none" stroke-width="2.6"/>'
           '<rect x="-12" y="-4" width="24" height="6" rx="2" fill="#3a3f4c" stroke-width="2.4"/>'
           '<rect x="-10" y="2" width="20" height="26" rx="4" fill="#ffe9a8" stroke-width="2.6"/><circle cx="0" cy="15" r="6" fill="#fff8e0" stroke="none"/>'
           '<rect x="-12" y="28" width="24" height="6" rx="2" fill="#3a3f4c" stroke-width="2.4"/></g>')
b += f'<circle cx="{FX + 56 * FS}" cy="{FY - 21 * FS}" r="70" fill="#ffe9a8" opacity=".35" filter="url(#b14)"/>'
b += f'<ellipse cx="{FX}" cy="{FY + 4}" rx="100" ry="14" fill="#000" opacity=".4"/>'
b += frog(FX, FY, FS, look=(5, -6), mouth='O', mid=PARKA, top=hardhat(), sleeve='#d2452e',
          armR='M38 -22 q16 -4 18 -28', armL='M-34 -22 q-14 6 -16 22', front=lantern)
b += f'<rect width="{W}" height="{H}" fill="url(#vig)"/>'
write(HERE, '#030817', defs, b, [('12 KM', 230, 'y'), ('STRAIGHT DOWN', 124, 'w')], outline='#04101c', top=880)
