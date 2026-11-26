# Shorts thumbnail A for hawking-time-travel-party-short3 (style B, guideline 16-9). Run: python3 videos/hawking-time-travel-party-short3/thumb/make.py
# Hook  WHO BUILT THE / MACHINE?  -- script S01 "You travel back in time and stop your grandparents from meeting. Now, who built the machine?"
# Scene: a brass time machine (seat, big clock-wheel, levers) inside a glowing loop arrow that bites its own tail; its right half is
#        dissolving into light pixels (S03 "The story cancels itself"; S05 "the future can erase its own past"). Below, a framed old
#        photo of two frog grandparents fades the same way. Goggles frog bottom-left. No people drawn.
import os, sys, math, random
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', 'hawking-time-travel-party-short1', 'thumb'))
from hshort_common import *

r = random.Random(33)
CX, CY = 540, 500
defs = FILTERS + vig(a=.8)
defs += lin('sky', [(0, '#03060f'), (.5, '#0a1430'), (1, '#03050c')])
defs += halo('hal', CX, CY, 620, inner='#fff3c8', outer='#4fd2ff')
defs += lin('brass', [(0, '#7a4a12'), (.35, '#f6d27a'), (.6, '#c9952e'), (1, '#5a3408')], x2=1, y2=0)
defs += rad('wheel', 560, 450, 220, [(0, '#fff6d6', 1), (.5, '#f2d27a', .95), (.85, '#c9952e', .95), (1, '#7a4a12', 1)])
defs += lin('velvet', [(0, '#c0392b'), (1, '#5a1414')])
defs += lin('fade', [(0, '#fff'), (.5, '#fff'), (.82, '#000'), (1, '#000')], x2=1, y2=0)
defs += lin('fade2', [(0, '#fff'), (.45, '#fff'), (.9, '#000'), (1, '#000')], x2=1, y2=0)
defs += f'<mask id="m1" maskUnits="userSpaceOnUse" x="0" y="0" width="{W}" height="{H}"><rect x="200" y="0" width="700" height="{H}" fill="url(#fade)"/></mask>'
b = f'<rect width="{W}" height="{H}" fill="url(#sky)"/>'
b += stars(r, 220, 0, H, big=6)
b += f'<ellipse cx="{CX}" cy="{CY}" rx="680" ry="660" fill="url(#hal)" opacity=".6"/>'
# ---- the time loop: a glowing arrow that bites its own tail ----
LX, LY = 420, 320
d = f'M{CX + LX * math.cos(math.radians(-70)):.0f} {CY + LY * math.sin(math.radians(-70)):.0f} A{LX} {LY} 0 1 1 {CX + LX * math.cos(math.radians(-100)):.0f} {CY + LY * math.sin(math.radians(-100)):.0f}'
b += f'<path d="{d}" fill="none" stroke="#4fd2ff" stroke-width="70" opacity=".25" filter="url(#b14)"/>'
b += f'<path d="{d}" fill="none" stroke="#bff4ff" stroke-width="26" stroke-linecap="round"/>'
b += f'<path d="{d}" fill="none" stroke="#ffffff" stroke-width="8" stroke-linecap="round"/>'
hx_, hy_ = CX + LX * math.cos(math.radians(-100)), CY + LY * math.sin(math.radians(-100))
b += f'<path transform="translate({hx_:.0f} {hy_:.0f})" d="M-6 -40 L56 0 L-6 40z" fill="#ffffff" stroke="#4fd2ff" stroke-width="6" stroke-linejoin="round"/>'
for k in range(10):   # ticks along the loop like a clock rim
    a = math.radians(k * 36 + 18)
    x, y = CX + LX * math.cos(a), CY + LY * math.sin(a)
    b += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="7" fill="#1a3a5a" stroke="#fff" stroke-width="3"/>'
# ---- the time machine (masked: right side dissolves) ----
m = ''
m += f'<ellipse cx="{CX}" cy="760" rx="300" ry="30" fill="#000" opacity=".5" filter="url(#b12)"/>'
# big clock wheel behind the seat
WX, WY, WR = 590, 450, 200
m += f'<circle cx="{WX}" cy="{WY}" r="{WR + 26}" fill="#f2d27a" opacity=".45" filter="url(#b24)"/>'
m += f'<circle cx="{WX}" cy="{WY}" r="{WR}" fill="url(#wheel)" stroke="#2a1606" stroke-width="7"/>'
m += f'<circle cx="{WX}" cy="{WY}" r="{WR - 24}" fill="none" stroke="#7a4a12" stroke-width="4"/>'
for k in range(12):
    a = math.radians(k * 30)
    m += f'<line x1="{WX + (WR - 24) * math.sin(a):.0f}" y1="{WY - (WR - 24) * math.cos(a):.0f}" x2="{WX + 40 * math.sin(a):.0f}" y2="{WY - 40 * math.cos(a):.0f}" stroke="#7a4a12" stroke-width="7"/>'
    m += f'<circle cx="{WX + (WR - 12) * math.sin(a):.0f}" cy="{WY - (WR - 12) * math.cos(a):.0f}" r="6" fill="#2a1606"/>'
m += f'<circle cx="{WX}" cy="{WY}" r="40" fill="#c9952e" stroke="#2a1606" stroke-width="5"/><circle cx="{WX}" cy="{WY}" r="14" fill="#2a1606"/>'
m += f'<path d="M{WX - 130} {WY - 110} A170 170 0 0 1 {WX + 40} {WY - 168}" fill="none" stroke="#fff" stroke-width="10" opacity=".5" stroke-linecap="round"/>'
# rails / sled base
m += f'<path d="M290 720 Q300 690 340 690 H760 Q800 690 810 720 Z" fill="url(#brass)" stroke="#2a1606" stroke-width="6"/>'
m += f'<rect x="280" y="718" width="540" height="22" rx="10" fill="#5a3408" stroke="#2a1606" stroke-width="5"/>'
for x in (360, 480, 620, 740):
    m += f'<path d="M{x} 690 V560" stroke="#2a1606" stroke-width="16"/><path d="M{x} 690 V560" stroke="url(#brass)" stroke-width="9"/>'
# seat
m += f'<path d="M440 640 L430 420 Q500 380 580 420 L570 640z" fill="url(#velvet)" stroke="#2a0606" stroke-width="6"/>'
m += f'<path d="M455 620 L448 436 Q505 408 562 436 L555 620" fill="none" stroke="#e05a4a" stroke-width="4" opacity=".7"/>'
for bx, by in ((480, 470), (530, 470), (480, 540), (530, 540)):
    m += f'<circle cx="{bx}" cy="{by}" r="5" fill="#f2d27a" stroke="#2a0606" stroke-width="2"/>'
m += f'<path d="M410 640 Q500 610 600 640 L610 690 H400z" fill="#8a1e1e" stroke="#2a0606" stroke-width="6"/>'
m += f'<path d="M405 600 h-40 v90 M605 600 h40 v90" fill="none" stroke="#2a1606" stroke-width="12"/><path d="M405 600 h-40 v90 M605 600 h40 v90" fill="none" stroke="url(#brass)" stroke-width="6"/>'
# control panel with dials and a lever (left)
m += f'<path d="M270 690 L300 560 H380 L400 690z" fill="#3a2410" stroke="#140a04" stroke-width="6"/>'
for dx, dy, rr in ((322, 600, 18), (360, 630, 14), (330, 652, 12)):
    m += clockface(dx, dy, rr, 10, 10 + dx % 40)
m += f'<path d="M305 560 L250 470" stroke="#140a04" stroke-width="14" stroke-linecap="round"/><path d="M305 560 L250 470" stroke="#c9d0dc" stroke-width="7" stroke-linecap="round"/>'
m += f'<circle cx="248" cy="466" r="17" fill="#e0566a" stroke="#140a04" stroke-width="5"/><circle cx="243" cy="460" r="5" fill="#fff" opacity=".7"/>'
# glowing crystal rods on the right
for x, h in ((700, 150), (740, 110), (680, 90)):
    m += f'<path d="M{x - 12} 690 V{690 - h} L{x} {670 - h} L{x + 12} {690 - h} V690z" fill="#bff4ff" stroke="#0c3a52" stroke-width="4"/>'
    m += f'<rect x="{x - 26}" y="{640 - h}" width="52" height="{h + 30}" fill="#4fd2ff" opacity=".25" filter="url(#b8)"/>'
b += f'<g mask="url(#m1)">{m}</g>'
# dissolving pixels drifting off to the right along the loop
for _ in range(170):
    x = r.uniform(640, 1000); y = r.uniform(300, 760)
    t = (x - 640) / 360
    if r.random() < t * .5: continue
    y -= t * 120
    s = r.uniform(5, 15) * (1 - .5 * t)
    col = r.choice(['#f6d27a', '#c9952e', '#fff6d6', '#bff4ff', '#e05a4a'])
    b += f'<rect x="{x:.0f}" y="{y:.0f}" width="{s:.0f}" height="{s:.0f}" fill="{col}" opacity="{.95 - .6 * t:.2f}"/>'
b += sparkles([(CX - 330, CY - 260, 24), (CX + 360, CY - 230, 18), (CX - 420, CY + 160, 16), (CX + 430, CY + 240, 18), (CX + 60, CY - 340, 14)], '#f0fcff')
b += fireflies(44, 140, 1850, col='#9fe8ff', core='#e8fbff', seed=6)
# ---- table top in the lower half with the fading family photo ----
b += f'<path d="M0 1560 Q540 1520 1080 1560 V1920 H0z" fill="#1a1008"/><path d="M0 1560 Q540 1520 1080 1560" fill="none" stroke="#6a4020" stroke-width="5"/>'
PX, PY, PW, PH = 770, 1530, 300, 360
defs += f'<mask id="m2" maskUnits="userSpaceOnUse" x="0" y="0" width="{W}" height="{H}"><rect x="{PX - PW / 2 - 20:.0f}" y="0" width="{PW + 40}" height="{H}" fill="url(#fade2)"/></mask>'
ph = f'<g transform="rotate(-6 {PX} {PY})">'
ph += f'<ellipse cx="{PX}" cy="{PY + PH / 2 + 10:.0f}" rx="{PW * .6:.0f}" ry="20" fill="#000" opacity=".5" filter="url(#b12)"/>'
ph += f'<rect x="{PX - PW / 2:.0f}" y="{PY - PH / 2:.0f}" width="{PW}" height="{PH}" rx="10" fill="url(#brass)" stroke="#2a1606" stroke-width="6"/>'
ph += f'<rect x="{PX - PW / 2 + 26:.0f}" y="{PY - PH / 2 + 26:.0f}" width="{PW - 52}" height="{PH - 52}" fill="#e8d4a8" stroke="#5a3408" stroke-width="4"/>'
ph += f'<rect x="{PX - PW / 2 + 26:.0f}" y="{PY - PH / 2 + 26:.0f}" width="{PW - 52}" height="{PH - 52}" fill="#f2d27a" opacity=".25"/>'
# two grandparent frog silhouettes (sepia, no eye whites) + a heart
def gfrog(x, y, s, hat=''):
    return (f'<g transform="translate({x} {y}) scale({s})" fill="#7a5a34" stroke="#3a2410" stroke-width="3">'
            '<path d="M-34 0 q-6 -64 34 -70 q40 -2 42 62 q0 10 -6 12 q-36 6 -70 -4z"/>'
            '<circle cx="-10" cy="-66" r="13"/><circle cx="22" cy="-66" r="13"/>'
            '<circle cx="-9" cy="-66" r="4" fill="#3a2410" stroke="none"/><circle cx="23" cy="-66" r="4" fill="#3a2410" stroke="none"/>'
            '<path d="M-6 -40 q12 8 24 0" fill="none"/>' + hat + '</g>')
ph += gfrog(PX - 60, PY + 120, 1.25, '<path d="M-24 -84 h56 v-26 h-56z M-34 -84 h76" fill="#4a3018"/>')
ph += gfrog(PX + 62, PY + 120, 1.15, '<path d="M-26 -82 q30 -30 60 0z" fill="#b07a4a"/><circle cx="20" cy="-96" r="6" fill="#e0566a"/>')
ph += f'<path transform="translate({PX} {PY - 80})" d="M0 14 C-30 -6 -18 -30 0 -16 C18 -30 30 -6 0 14z" fill="#e0566a" stroke="#5a1414" stroke-width="3"/>'
ph += '</g>'
b += f'<g mask="url(#m2)">{ph}</g>'
for _ in range(70):
    x = r.uniform(PX + 20, PX + 260); y = r.uniform(PY - 200, PY + 170); t = (x - PX - 20) / 240
    if r.random() < t * .6: continue
    s = r.uniform(4, 12) * (1 - .5 * t)
    b += f'<rect x="{x:.0f}" y="{y - t * 80:.0f}" width="{s:.0f}" height="{s:.0f}" fill="{r.choice(["#e8d4a8", "#f6d27a", "#7a5a34", "#e0566a"])}" opacity="{.9 - .6 * t:.2f}"/>'
b += darkband(870, 1250, .5)
# ---- goggles frog bottom-left, staring at the fading photo ----
FX, FY, FS = 230, 1790, 2.9
b += f'<ellipse cx="{FX}" cy="{FY + 8}" rx="100" ry="15" fill="#000" opacity=".45"/>'
b += f'<ellipse cx="{FX}" cy="{FY - 130}" rx="190" ry="190" fill="#9fe8ff" opacity=".12" filter="url(#b24)"/>'
goggles = ('<path d="M-36 -84 q40 -16 82 0" fill="none" stroke="#3a3f4c" stroke-width="6"/>'
           '<circle cx="-8" cy="-91" r="9.5" fill="#bff4ff" stroke-width="3.2"/><circle cx="20" cy="-92" r="9.5" fill="#bff4ff" stroke-width="3.2"/>'
           '<circle cx="-11" cy="-94" r="2.6" fill="#fff" stroke="none"/><circle cx="17" cy="-95" r="2.6" fill="#fff" stroke="none"/>')
coat = ('<path d="M-38 2 q-6 -22 2 -30 q12 -4 30 -4 l8 18 l8 -18 q18 0 32 4 q10 10 2 30 q-42 10 -82 0z" fill="#8a5a2e" stroke-width="3.6"/>'
        '<path d="M2 -16 v16" stroke-width="2.4"/><circle cx="-14" cy="-10" r="2.6" fill="#f2d27a" stroke="none"/><circle cx="-14" cy="-2" r="2.6" fill="#f2d27a" stroke="none"/>')
b += frog(FX, FY, FS, look=(5, -2), mouth='O', mid=coat, top=goggles, sleeve='#8a5a2e',
          armL='M-34 -22 q-14 6 -16 22', armR='M38 -24 q12 -10 8 -30')
b += f'<rect width="{W}" height="{H}" fill="url(#vig)"/>'
write(HERE, '#03060f', defs, b, [('WHO BUILT THE', 116, 'w'), ('MACHINE?', 180, 'y')], outline='#04101a', top=905)
