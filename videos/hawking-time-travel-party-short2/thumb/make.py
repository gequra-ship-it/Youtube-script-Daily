# Shorts thumbnail A for hawking-time-travel-party-short2 (style B, guideline 16-9). Run: python3 videos/hawking-time-travel-party-short2/thumb/make.py
# Hook  SPACETIME / FEEDBACK?  (question: the script hedges it) -- S06 "spacetime could suffer a similar feedback near the edge of a
#        time machine"; S09 "This is a conjecture, not a proof."
# Scene (head-on, unlike long C's side-view funnel): the glowing mouth of a wormhole seen straight on, a loop of light racing round
#        and round its throat (S04 "go around again, and again"), the rim cracking and flying apart (S07 "torn apart before any traveler
#        could step inside"). Below: a microphone too close to a loudspeaker, screech waves between them (S05); a frog in a flight
#        suit covers its ears bottom-left.
import os, sys, math, random
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', 'hawking-time-travel-party-short1', 'thumb'))
from hshort_common import *

r = random.Random(22)
CX, CY = 540, 500
defs = FILTERS + vig(a=.8)
defs += lin('sky', [(0, '#05030f'), (.5, '#120626'), (1, '#05030c')])
defs += halo('hal', CX, CY, 620, inner='#ffffff', outer='#ff5ab4')
defs += rad('core', CX, CY, 300, [(0, '#ffffff', 1), (.12, '#fff2d0', 1), (.35, '#ff8ad0', .9), (.7, '#5a2aa8', .85), (1, '#12062a', 1)])
defs += lin('spk', [(0, '#2a2a3a'), (.5, '#3c3c50'), (1, '#16161f')], x2=1, y2=0)
defs += lin('mic', [(0, '#6a707c'), (.4, '#e8ecf2'), (1, '#5a606c')], x2=1, y2=0)
b = f'<rect width="{W}" height="{H}" fill="url(#sky)"/>'
b += stars(r, 260, 0, H, big=8)
b += f'<ellipse cx="{CX}" cy="{CY}" rx="700" ry="680" fill="url(#hal)" opacity=".7"/>'
# ---- wormhole mouth: rings receding into the throat ----
RX, RY = 330, 300
b += f'<ellipse cx="{CX}" cy="{CY}" rx="{RX}" ry="{RY}" fill="url(#core)"/>'
for k in range(16):
    t = k / 15; f = (1 - t) ** 1.8
    rx, ry = 20 + (RX - 20) * f, 18 + (RY - 18) * f
    col = mix(['#ffe8a8', '#ff8ad0', '#9a7cff'], t)
    b += f'<ellipse cx="{CX + 30 * t:.0f}" cy="{CY - 16 * t:.0f}" rx="{rx:.0f}" ry="{ry:.0f}" fill="none" stroke="{col}" stroke-width="{1.2 + 3 * f:.1f}" opacity="{.35 + .5 * f:.2f}"/>'
for k in range(24):   # grid spokes into the throat
    a = math.radians(k * 15)
    b += f'<path d="M{CX + RX * math.cos(a):.0f} {CY + RY * math.sin(a):.0f} L{CX + 30 + 20 * math.cos(a):.0f} {CY - 16 + 18 * math.sin(a):.0f}" stroke="#ffc8ec" stroke-width="1.6" opacity=".35"/>'
b += f'<circle cx="{CX + 30}" cy="{CY - 16}" r="70" fill="#fff" opacity=".9" filter="url(#b24)"/>'
# ---- loop of energy racing round the throat (again and again) ----
for k, (rx, ry, w, op) in enumerate(((250, 226, 14, .95), (190, 172, 10, .8), (130, 118, 7, .7))):
    rot = k * 50
    d = f'M{CX + rx} {CY} A{rx} {ry} 0 1 1 {CX + rx * math.cos(math.radians(-30)):.0f} {CY + ry * math.sin(math.radians(-30)):.0f}'
    g = f'<g transform="rotate({rot} {CX} {CY})">'
    g += f'<path d="{d}" fill="none" stroke="#ffd27a" stroke-width="{w * 3}" opacity=".35" filter="url(#b8)"/>'
    g += f'<path d="{d}" fill="none" stroke="#fff4c8" stroke-width="{w}" stroke-linecap="round" opacity="{op}"/>'
    ex, ey = CX + rx * math.cos(math.radians(-30)), CY + ry * math.sin(math.radians(-30))
    g += f'<path transform="translate({ex:.0f} {ey:.0f}) rotate(60)" d="M{-w * 2.2:.0f} {w * 1.2:.0f} L{w * 2.2:.0f} 0 L{-w * 2.2:.0f} {-w * 1.2:.0f}z" fill="#fff4c8"/>'
    b += g + '</g>'
# ---- rim cracking apart: dark rim with jagged gaps + shards flying out ----
b += f'<ellipse cx="{CX}" cy="{CY}" rx="{RX + 14}" ry="{RY + 14}" fill="none" stroke="#1a0a2a" stroke-width="30"/>'
b += f'<ellipse cx="{CX}" cy="{CY}" rx="{RX + 14}" ry="{RY + 14}" fill="none" stroke="#ff9ad8" stroke-width="6" opacity=".9"/>'
for k in range(9):
    a0 = math.radians(k * 40 + 12)
    x0, y0 = CX + (RX + 14) * math.cos(a0), CY + (RY + 14) * math.sin(a0)
    # bright gap in the rim
    b += f'<path d="M{x0:.0f} {y0:.0f} l{14 * math.cos(a0 + 1.2):.0f} {14 * math.sin(a0 + 1.2):.0f}" stroke="#fff" stroke-width="40" opacity=".0"/>'
    pts = [(x0 - 28 * math.cos(a0), y0 - 28 * math.sin(a0))]
    for j in range(1, 4):
        rr = j * 26; jit = (-1) ** j * 10
        pts.append((x0 + rr * math.cos(a0) + jit * math.sin(a0), y0 + rr * math.sin(a0) - jit * math.cos(a0)))
    b += f'<polyline points="{P(pts)}" fill="none" stroke="#ffd27a" stroke-width="14" opacity=".5" filter="url(#b6)"/>'
    b += f'<polyline points="{P(pts)}" fill="none" stroke="#fff" stroke-width="4"/>'
    for j in range(3):   # shards
        rr = 60 + j * 46 + r.uniform(0, 30); aa = a0 + r.uniform(-.18, .18)
        sx, sy = CX + (RX + rr) * math.cos(aa), CY + (RY + rr * .9) * math.sin(aa)
        if not (90 < sy < 840): continue
        s = r.uniform(16, 34)
        b += f'<path transform="translate({sx:.0f} {sy:.0f}) rotate({r.uniform(0, 360):.0f})" d="M0 {-s:.0f} L{s * .8:.0f} {s * .3:.0f} L{-s * .4:.0f} {s * .7:.0f}z" fill="#2a1240" stroke="#ff9ad8" stroke-width="3"/>'
        b += f'<path d="M{sx:.0f} {sy:.0f} l{-28 * math.cos(aa):.0f} {-28 * math.sin(aa):.0f}" stroke="#ffc8ec" stroke-width="3" opacity=".6"/>'
b += sparkles([(CX - 300, CY - 280, 24), (CX + 330, CY - 250, 20), (CX + 380, CY + 260, 18), (CX - 380, CY + 230, 18), (CX + 40, CY - 330, 16)], '#fff1f8')
b += fireflies(46, 140, 1850, col='#ff9ad8', core='#fff0f8', seed=8)
# ---- floor of the lower half: dark stage ----
b += f'<path d="M0 1500 Q540 1440 1080 1500 V1920 H0z" fill="#0c0618"/>'
b += f'<path d="M0 1500 Q540 1440 1080 1500" fill="none" stroke="#ff9ad8" stroke-width="3" opacity=".4"/>'
# ---- loudspeaker (right) ----
SX, SY = 880, 1560
b += f'<ellipse cx="{SX}" cy="{SY + 190}" rx="150" ry="20" fill="#000" opacity=".5" filter="url(#b12)"/>'
b += f'<rect x="{SX - 120}" y="{SY - 240}" width="240" height="430" rx="16" fill="url(#spk)" stroke="#05050a" stroke-width="6"/>'
b += f'<rect x="{SX - 120}" y="{SY - 240}" width="240" height="430" rx="16" fill="none" stroke="#ff9ad8" stroke-width="3" opacity=".5"/>'
b += f'<circle cx="{SX}" cy="{SY - 150}" r="46" fill="#14141c" stroke="#05050a" stroke-width="4"/><circle cx="{SX}" cy="{SY - 150}" r="18" fill="#4a4a60"/>'
b += f'<circle cx="{SX}" cy="{SY + 50}" r="98" fill="#14141c" stroke="#05050a" stroke-width="5"/><circle cx="{SX}" cy="{SY + 50}" r="70" fill="#22222e" stroke="#3a3a4e" stroke-width="4"/><circle cx="{SX}" cy="{SY + 50}" r="28" fill="#4a4a60" stroke="#05050a" stroke-width="3"/>'
b += f'<path d="M{SX - 70} {SY - 10} a98 98 0 0 0 -16 120" fill="none" stroke="#ffd27a" stroke-width="5" opacity=".8"/>'
# screech waves from the speaker toward the mic
for k in range(4):
    rr = 70 + k * 46
    b += f'<path d="M{SX - 110 - k * 30} {SY + 50 - rr} Q{SX - 170 - k * 50} {SY + 50} {SX - 110 - k * 30} {SY + 50 + rr}" fill="none" stroke="#ffd27a" stroke-width="{7 - k}" opacity="{.9 - k * .16:.2f}" stroke-linecap="round"/>'
# ---- microphone on a stand, pointed at the speaker ----
MX, MY = 490, 1500
b += f'<ellipse cx="{MX - 20}" cy="1800" rx="90" ry="14" fill="#000" opacity=".5"/>'
b += f'<path d="M{MX - 70} 1800 L{MX - 20} 1780 L{MX + 30} 1800" fill="none" stroke="#1a1a24" stroke-width="12" stroke-linecap="round"/>'
b += f'<path d="M{MX - 20} 1782 V{MY + 40}" stroke="#1a1a24" stroke-width="12"/><path d="M{MX - 22} 1780 V{MY + 40}" stroke="#5a5f6c" stroke-width="4"/>'
b += f'<g transform="translate({MX - 20} {MY + 40}) rotate(66) scale(.85)">'
b += '<rect x="-10" y="-150" width="20" height="150" rx="6" fill="#1a1a24" stroke="#05050a" stroke-width="3"/>'
b += '<path d="M-20 -150 h40 l-4 -16 h-32z" fill="#8a8f9c" stroke="#05050a" stroke-width="3"/>'
b += '<ellipse cx="0" cy="-206" rx="38" ry="46" fill="url(#mic)" stroke="#05050a" stroke-width="4"/>'
b += ''.join(f'<path d="M-34 {-206 + dy} h68" stroke="#4a505c" stroke-width="2.4"/>' for dy in (-24, -12, 0, 12, 24))
b += '<path d="M-12 -238 v64 M12 -238 v64" stroke="#4a505c" stroke-width="2.4"/>'
b += '<path d="M-20 -230 q-8 20 0 44" fill="none" stroke="#fff" stroke-width="5" opacity=".8"/></g>'
# feedback squiggle between mic head and speaker
mhx, mhy = MX - 20 + 175 * math.sin(math.radians(66)), MY + 40 - 175 * math.cos(math.radians(66))
pts = []
for i in range(50):
    t = i / 49; x = mhx + 40 + (SX - 130 - mhx - 40) * t; y = mhy + (SY - 40 - mhy) * t
    a = 18 * math.sin(t * 30) * (.4 + t)
    pts.append((x, y + a))
b += f'<polyline points="{P(pts)}" fill="none" stroke="#ff5ab4" stroke-width="16" opacity=".35" filter="url(#b6)"/>'
b += f'<polyline points="{P(pts)}" fill="none" stroke="#ffc8ec" stroke-width="5" stroke-linecap="round"/>'
b += sparkles([(mhx + 20, mhy - 60, 18), (SX - 150, SY - 200, 16)], '#fff1f8')
b += darkband(860, 1240, .5)
# ---- frog in a flight suit, hands over its ears (the screech), bottom-left ----
FX, FY, FS = 200, 1800, 2.9
b += f'<ellipse cx="{FX}" cy="{FY + 8}" rx="100" ry="15" fill="#000" opacity=".45"/>'
b += f'<ellipse cx="{FX}" cy="{FY - 130}" rx="190" ry="190" fill="#ff9ad8" opacity=".14" filter="url(#b24)"/>'
suit = ('<path d="M-36 2 q-8 -36 2 -46 q38 -12 76 0 q10 14 2 46 q-40 10 -80 0z" fill="#eef2f6" stroke-width="3.6"/>'
        '<rect x="-10" y="-28" width="30" height="18" rx="4" fill="#cfd8e2" stroke-width="2.4"/>'
        '<circle cx="-1" cy="-19" r="3.2" fill="#e0566a" stroke="none"/><circle cx="11" cy="-19" r="3.2" fill="#5ab4e0" stroke="none"/>')
lines_ = '<path d="M-58 -78 l-12 -6 M-60 -62 l-14 0 M66 -78 l12 -6 M68 -62 l14 0" stroke="#ffd27a" stroke-width="3.4"/>'
b += frog(FX, FY, FS, look=(-2, 1), mouth='O', mid=suit, top=lines_, sleeve='#eef2f6',
          armL='M-34 -26 q-16 -14 -10 -36', armR='M38 -26 q16 -14 10 -36')
b += f'<rect width="{W}" height="{H}" fill="url(#vig)"/>'
write(HERE, '#05030f', defs, b, [('SPACETIME', 150, 'w'), ('FEEDBACK?', 170, 'y')], outline='#0a0418', top=900)
