# Shorts thumbnail A for hawking-time-travel-party-short4 (style B, guideline 16-9). Run: python3 videos/hawking-time-travel-party-short4/thumb/make.py
# Hook  CLOCKS RUN / FASTER / UP HIGH  -- script S03 "Clocks run faster where gravity is weaker."; S04 "A clock at the top of a tall
#        mountain ticks slightly faster than one at sea level, because gravity is weaker higher up."
# Scene: moonlit snowy peak with a big glowing clock on its summit, speed arcs round it; a small space station crosses the sky with a
#        tiny astronaut (S05, gold visor, no face). At the foot, by the dark sea, a dimmer sea-level clock. Climber frog (beanie, rope,
#        pocket watch) bottom-left looks up.
import os, sys, math, random
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', 'hawking-time-travel-party-short1', 'thumb'))
from hshort_common import *

r = random.Random(44)
defs = FILTERS + vig(a=.8)
defs += lin('sky', [(0, '#030714'), (.45, '#0c1a3a'), (1, '#16305a')])
defs += halo('hal', 540, 420, 520, inner='#fff3a8', outer='#7fb8ff')
defs += lin('rock', [(0, '#3a4a6a'), (1, '#0c1222')], x2=1, y2=1)
defs += lin('rockD', [(0, '#1a2440'), (1, '#060a16')])
defs += lin('snow', [(0, '#ffffff'), (1, '#b8cce8')])
defs += lin('sea', [(0, '#1a3a5a'), (1, '#040a14')])
b = f'<rect width="{W}" height="{H}" fill="url(#sky)"/>'
b += stars(r, 240, 0, 1100, big=7)
b += '<circle cx="190" cy="250" r="54" fill="#f4f8ff" opacity=".95"/><circle cx="190" cy="250" r="110" fill="#cfe0ff" opacity=".25" filter="url(#b24)"/>'
b += '<circle cx="175" cy="238" r="10" fill="#d8e2f0"/><circle cx="205" cy="268" r="14" fill="#d8e2f0"/>'
# ---- space station + astronaut, top-right, on an orbit arc ----
b += '<path d="M560 230 Q820 120 1100 210" fill="none" stroke="#bfe0ff" stroke-width="3" stroke-dasharray="10 12" opacity=".6"/>'
ss = '<g transform="translate(860 196) rotate(-10)">'
for dx in (-96, 56):
    ss += f'<rect x="{dx}" y="-26" width="40" height="52" fill="#2a5aa8" stroke="#0a1430" stroke-width="3"/>'
    ss += ''.join(f'<path d="M{dx + k * 10} -26 v52" stroke="#7fb8ff" stroke-width="1.4"/>' for k in range(1, 4))
ss += '<rect x="-56" y="-4" width="112" height="8" fill="#c8d0dc" stroke="#0a1430" stroke-width="2.4"/>'
ss += '<rect x="-24" y="-14" width="48" height="28" rx="8" fill="#eef2f6" stroke="#0a1430" stroke-width="3"/><circle cx="0" cy="0" r="6" fill="#7fb8ff" stroke="#0a1430" stroke-width="2"/>'
ss += '</g>'
b += f'<ellipse cx="860" cy="196" rx="140" ry="60" fill="#bfe0ff" opacity=".18" filter="url(#b12)"/>' + ss
astro = ('<g transform="translate(960 290) rotate(18)">'
         '<path d="M-14 -4 q-2 26 4 34 h20 q6 -8 4 -34z" fill="#eef2f6" stroke="#0a1430" stroke-width="3"/>'
         '<path d="M-14 6 l-14 12 M14 6 l14 -10 M-6 30 l-4 14 M8 30 l4 14" stroke="#eef2f6" stroke-width="8" stroke-linecap="round"/>'
         '<path d="M-14 6 l-14 12 M14 6 l14 -10 M-6 30 l-4 14 M8 30 l4 14" stroke="#0a1430" stroke-width="2" stroke-linecap="round" opacity=".5"/>'
         '<circle cx="0" cy="-18" r="16" fill="#eef2f6" stroke="#0a1430" stroke-width="3"/>'
         '<path d="M-10 -22 q10 -8 20 0 v8 q-10 6 -20 0z" fill="#e2b34a" stroke="#0a1430" stroke-width="2"/>'
         '<path d="M-6 -20 q4 -3 8 -1" stroke="#fff6d6" stroke-width="2"/></g>')
b += astro + '<path d="M928 270 Q900 240 890 214" fill="none" stroke="#eef2f6" stroke-width="2" opacity=".7"/>'
# ---- mountains ----
b += f'<ellipse cx="540" cy="460" rx="620" ry="560" fill="url(#hal)" opacity=".6"/>'
b += '<path d="M-60 1240 L200 760 L330 900 L420 820 L560 1240z" fill="#14203a"/><path d="M500 1240 L760 820 L860 920 L980 760 L1140 1240z" fill="#14203a"/>'
b += '<path d="M200 760 L240 830 L215 820 L195 850 L170 815z" fill="#cfdcf0" opacity=".7"/><path d="M980 760 L1020 830 L995 820 L975 845 L945 812z" fill="#cfdcf0" opacity=".7"/>'
PK = (540, 640)
main = f'M-120 1560 L{PK[0] - 90} {PK[1] + 70} L{PK[0]} {PK[1]} L{PK[0] + 100} {PK[1] + 80} L1200 1560z'
b += f'<path d="{main}" fill="url(#rock)" stroke="#05080f" stroke-width="5"/>'
b += f'<path d="M{PK[0]} {PK[1]} L{PK[0] + 100} {PK[1] + 80} L1200 1560 L640 1560 L600 1100 L560 900z" fill="url(#rockD)" opacity=".8"/>'
snow = f'M{PK[0] - 90} {PK[1] + 70} L{PK[0]} {PK[1]} L{PK[0] + 100} {PK[1] + 80} L{PK[0] + 160} {PK[1] + 160} L{PK[0] + 110} {PK[1] + 140} L{PK[0] + 80} {PK[1] + 200} L{PK[0] + 40} {PK[1] + 150} L{PK[0]} {PK[1] + 220} L{PK[0] - 50} {PK[1] + 150} L{PK[0] - 90} {PK[1] + 190} L{PK[0] - 120} {PK[1] + 130} L{PK[0] - 170} {PK[1] + 160}z'
b += f'<path d="{snow}" fill="url(#snow)" stroke="#05080f" stroke-width="4" stroke-linejoin="round"/>'
b += f'<path d="M{PK[0] - 80} {PK[1] + 76} L{PK[0]} {PK[1] + 6}" stroke="#fff" stroke-width="6" opacity=".8"/>'
for _ in range(30):   # rock ridges
    x = r.uniform(80, 1000); y = r.uniform(900, 1520)
    b += f'<path d="M{x:.0f} {y:.0f} l{r.uniform(-60, 60):.0f} {r.uniform(30, 90):.0f}" stroke="#5a6a8a" stroke-width="3" opacity=".35"/>'
# ---- the glowing summit clock ----
CX, CY, CR = 540, 430, 150
b += f'<rect x="{CX - 40}" y="{CY + CR}" width="80" height="{PK[1] - CY - CR + 20}" fill="#3a2a1a" stroke="#120a04" stroke-width="5"/>'
b += f'<circle cx="{CX}" cy="{CY}" r="{CR * 1.7:.0f}" fill="#fff3a8" opacity=".35" filter="url(#b26)"/>'
for k in range(3):   # speed arcs: it runs fast
    rr = CR + 46 + k * 30
    b += f'<path d="M{CX + rr * math.cos(math.radians(-150)):.0f} {CY + rr * math.sin(math.radians(-150)):.0f} A{rr} {rr} 0 0 1 {CX + rr * math.cos(math.radians(-40)):.0f} {CY + rr * math.sin(math.radians(-40)):.0f}" fill="none" stroke="#fff3a8" stroke-width="{9 - k * 2}" opacity="{.9 - k * .25:.2f}" stroke-linecap="round"/>'
    ex, ey = CX + rr * math.cos(math.radians(-40)), CY + rr * math.sin(math.radians(-40))
    b += f'<path transform="translate({ex:.0f} {ey:.0f}) rotate(50)" d="M-12 -10 L14 0 L-12 10z" fill="#fff3a8" opacity="{.9 - k * .25:.2f}"/>'
b += clockface(CX, CY, CR, 12, 0, face='#fffbea', rim='#e2b34a', glow='#fff3a8')
b += sparkles([(CX - 230, CY - 150, 24), (CX + 250, CY + 40, 20), (CX - 260, CY + 120, 16), (CX + 40, CY - 240, 18)], '#fffbe0')
b += fireflies(36, 140, 1850, col='#cfe6ff', core='#f4faff', seed=4)   # falling snow glints
# ---- sea level: dark sea, shore, a dimmer clock ----
b += f'<rect y="1560" width="{W}" height="360" fill="url(#sea)"/>'
b += '<path d="M0 1560 H1080" stroke="#7fb8ff" stroke-width="3" opacity=".5"/>'
for _ in range(30):
    y = r.uniform(1580, 1880); x = r.uniform(-20, 1060)
    b += f'<path d="M{x:.0f} {y:.0f} h{r.uniform(30, 80):.0f}" stroke="#7fb8ff" stroke-width="2.4" opacity=".3"/>'
b += '<path d="M0 1700 Q200 1650 420 1690 Q520 1710 560 1920 H0z" fill="#1a1a24" stroke="#05050a" stroke-width="4"/>'
b += '<path d="M640 1920 Q700 1690 860 1670 Q980 1660 1080 1690 V1920z" fill="#1a1a24" stroke="#05050a" stroke-width="4"/>'
SX, SY, SR = 860, 1500, 92
b += f'<rect x="{SX - 12}" y="{SY + SR}" width="24" height="{1680 - SY - SR}" fill="#3a3f4c" stroke="#0a0a10" stroke-width="4"/>'
b += clockface(SX, SY, SR, 11, 58, face='#c8d4e4', rim='#7a8494', ink='#1a2030')
b += f'<circle cx="{SX}" cy="{SY}" r="{SR * 1.15:.0f}" fill="#04080f" opacity=".25"/>'
b += darkband(850, 1270, .5)
# ---- climber frog bottom-left: beanie, coiled rope, pocket watch, looking up at the summit ----
FX, FY, FS = 220, 1790, 2.9
b += f'<ellipse cx="{FX}" cy="{FY + 8}" rx="100" ry="15" fill="#000" opacity=".45"/>'
b += f'<ellipse cx="{FX}" cy="{FY - 130}" rx="190" ry="190" fill="#cfe6ff" opacity=".12" filter="url(#b24)"/>'
beanie = ('<path d="M-30 -90 q4 -38 36 -40 q34 2 38 40z" fill="#e0566a" stroke-width="3.4"/>'
          '<rect x="-36" y="-96" width="86" height="16" rx="8" fill="#f2d27a" stroke-width="3"/><circle cx="8" cy="-134" r="9" fill="#fff" stroke-width="2.6"/>')
rope = ('<ellipse cx="-4" cy="-18" rx="34" ry="14" fill="none" stroke="#c9952e" stroke-width="6"/>'
        '<ellipse cx="-4" cy="-18" rx="26" ry="9" fill="none" stroke="#e2b34a" stroke-width="4"/><path d="M-36 -26 L34 -6" stroke="#8a5a2e" stroke-width="5"/>')
watch = ('<g transform="translate(66 -60)"><path d="M-8 18 q-6 14 -16 18" fill="none" stroke="#e2b34a" stroke-width="2.4"/>'
         '<circle cx="0" cy="0" r="15" fill="#fffbea" stroke-width="3"/><rect x="-3" y="-21" width="6" height="6" fill="#e2b34a" stroke-width="2"/>'
         '<path d="M0 0 v-9 M0 0 l6 3" stroke-width="2.2"/></g>')
b += f'<circle cx="{FX + 66 * FS}" cy="{FY - 60 * FS}" r="60" fill="#fff3a8" opacity=".25" filter="url(#b12)"/>'
b += frog(FX, FY, FS, look=(4, -5), mouth='O', mid=rope, top=beanie, front=watch,
          armL='M-34 -22 q-14 6 -16 22', armR='M38 -24 q18 -10 22 -26')
b += f'<rect width="{W}" height="{H}" fill="url(#vig)"/>'
write(HERE, '#030714', defs, b, [('CLOCKS RUN', 112, 'w'), ('FASTER', 190, 'y'), ('UP HIGH', 112, 'w')], outline='#04101a', top=862)
