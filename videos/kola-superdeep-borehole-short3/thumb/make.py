# Shorts thumbnail A for kola-superdeep-borehole-short3 (style B, guideline 16-9). Run: python3 videos/kola-superdeep-borehole-short3/thumb/make.py
# Hook  NEARLY / 2 BILLION / YEARS  -- script S02 "These microscopic fossils had been entombed inside the Baltic Shield for nearly two billion years."
# Scene: a rock core seen end-on; its polished crystalline cut face has one big glowing plankton microfossil (radiolarian-like) in the middle
#        and two small ones (S01 "a microscope revealed the fossilized remains of ... single-celled marine plankton"). Lab-coat frog with
#        goggles bottom-left, a small microscope bottom-right on the bench.
import os, sys, math, random
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', 'kola-superdeep-borehole-short1', 'thumb'))
from kshort_common import *

r = random.Random(43)
CX, CY, R = 520, 520, 300
BX, BY = 650, 330       # back end of the core (behind the face)
defs = FILTERS + vig(a=.8)
defs += lin('bg', [(0, '#040a14'), (.5, '#0a1e2c'), (1, '#03070e')])
defs += halo('hal', CX, CY, 640, inner='#e8fff8', outer='#3fd8c0')
defs += lin('side', [(0, '#3a4254'), (.45, '#6a7386'), (1, '#262c38')], x2=1, y2=-.3)
defs += rad('face', CX - 80, CY - 90, 420, [(0, '#b9c2d0', 1), (.6, '#7a8496', 1), (1, '#4a5262', 1)])
defs += rad('fg', CX, CY, 170, [(0, '#e8fff8', .95), (.4, '#7ff5d8', .5), (1, '#7ff5d8', 0)])
defs += f'<clipPath id="fc"><ellipse cx="{CX}" cy="{CY}" rx="{R}" ry="{R - 12}"/></clipPath>'
b = f'<rect width="{W}" height="{H}" fill="url(#bg)"/>'
b += f'<ellipse cx="{CX}" cy="{CY}" rx="700" ry="700" fill="url(#hal)" opacity=".6"/>'
# light rays out of the core face
for a in range(0, 360, 24):
    t = math.radians(a + 7)
    b += f'<path d="M{CX} {CY} L{CX + 900 * math.cos(t - .05):.0f} {CY + 900 * math.sin(t - .05):.0f} L{CX + 900 * math.cos(t + .05):.0f} {CY + 900 * math.sin(t + .05):.0f}z" fill="#bffff0" opacity=".05"/>'
# core body (cylinder going back toward the upper right)
dx, dy = BX - CX, BY - CY; L = math.hypot(dx, dy); nx, ny = -dy / L, dx / L
b += f'<ellipse cx="{BX}" cy="{BY}" rx="{R}" ry="{R - 12}" fill="url(#side)" stroke="#0a0d14" stroke-width="7"/>'
quad = [(CX + nx * R, CY + ny * R), (BX + nx * R, BY + ny * R), (BX - nx * R, BY - ny * R), (CX - nx * R, CY - ny * R)]
b += f'<polygon points="{P(quad)}" fill="url(#side)"/>'
defs += f'<clipPath id="sc"><polygon points="{P(quad)}"/><ellipse cx="{BX}" cy="{BY}" rx="{R}" ry="{R - 12}"/></clipPath>'
b += '<g clip-path="url(#sc)">' + crystals(r, 260, CX - R, BY - R, BX + R, CY + R, ['#eef2f8', '#2a2e38', '#c9b29a', '#5a6272'], 5, 16, .25, .6) + '</g>'
b += f'<path d="M{quad[0][0]:.0f} {quad[0][1]:.0f} L{quad[1][0]:.0f} {quad[1][1]:.0f} M{quad[2][0]:.0f} {quad[2][1]:.0f} L{quad[3][0]:.0f} {quad[3][1]:.0f}" stroke="#0a0d14" stroke-width="7"/>'
for k in range(5):  # banding on the side
    t = (k + 1) / 6
    b += f'<path d="M{CX - nx * R * (1 - 2 * t) + 0:.0f} {CY - ny * R * (1 - 2 * t):.0f} l{dx:.0f} {dy:.0f}" stroke="{r.choice(["#c9d0dc", "#4a5262", "#9a8a80"])}" stroke-width="{r.uniform(4, 10):.0f}" opacity=".35"/>'
b += f'<path d="M{BX - 200} {BY - 210} Q{BX + 40} {BY - 300} {BX + 250} {BY - 150}" fill="none" stroke="#e8fff8" stroke-width="5" opacity=".5"/>'
b += f'<ellipse cx="{CX}" cy="{CY}" rx="{R + 30}" ry="{R + 18}" fill="#7ff5d8" opacity=".35" filter="url(#b14)"/>'
# polished cut face: crystal mosaic + metamorphic banding
b += f'<ellipse cx="{CX}" cy="{CY}" rx="{R}" ry="{R - 12}" fill="url(#face)" stroke="#0a0d14" stroke-width="8"/>'
face = f'<g clip-path="url(#fc)">'
for k in range(7):
    off = -R + (k + .5) * 2 * R / 7 + r.uniform(-20, 20)
    d = f'M{CX - R - 20} {CY + off:.0f} ' + ' '.join(f'Q {CX - R + (j + .5) * 110:.0f} {CY + off + r.uniform(-30, 30):.0f} {CX - R + (j + 1) * 110:.0f} {CY + off + r.uniform(-12, 12):.0f}' for j in range(6))
    face += f'<path d="{d}" fill="none" stroke="{r.choice(["#5a6272", "#dfe4ec", "#8a7a72", "#3a4252"])}" stroke-width="{r.uniform(8, 22):.0f}" opacity=".35"/>'
face += crystals(r, 520, CX - R, CY - R, CX + R, CY + R, ['#eef2f8', '#2a2e38', '#c9b29a', '#9aa2b4', '#5a6272'], 6, 22, .35, .8)
face += f'<ellipse cx="{CX}" cy="{CY}" rx="170" ry="165" fill="#06121c" opacity=".6" filter="url(#b26)"/>'
face += f'<circle cx="{CX}" cy="{CY}" r="170" fill="url(#fg)"/>'
# the hero fossil + two small ones, glowing
hero = radiolarian(CX, CY, 2.7, '#9ffff0')
face += f'<g filter="url(#b8)" opacity=".9">{hero}</g>' + hero
face += radiolarian(CX, CY, 2.7, '#ffffff').replace('stroke-width="2.6"', 'stroke-width="1"').replace('fill-opacity=".18"', 'fill-opacity="0"')
for f in (foram(CX + 170, CY + 140, 1.3, '#f2d27a', 30), diatom(CX - 170, CY + 150, 1.3, '#f2d27a', -25), foram(CX - 160, CY - 150, .9, '#7ff5d8', 120)):
    face += f'<g filter="url(#b4)" opacity=".85">{f}</g>' + f
face += f'<ellipse cx="{CX - 110}" cy="{CY - 140}" rx="150" ry="60" transform="rotate(-25 {CX - 110} {CY - 140})" fill="#ffffff" opacity=".12"/>'
face += '</g>'
b += face
b += f'<path d="M{CX - R + 30} {CY - 90} A{R} {R - 12} 0 0 1 {CX + 60} {CY - R + 16}" fill="none" stroke="#f0fffa" stroke-width="7" opacity=".8" stroke-linecap="round"/>'
b += sparkles([(CX + 250, CY - 290, 26), (CX - 300, CY - 240, 18), (CX + 330, CY + 200, 20), (CX - 340, CY + 250, 16), (CX + 40, CY - 330, 14)], '#eafff8')
b += fireflies(56, 60, 1850, col='#7ff5d8', core='#e8fff8', seed=13)
b += darkband(860, 1240, .5)
# lab bench at the bottom
b += f'<path d="M0 1700 L1080 1680 V1920 H0z" fill="#1c140e"/><path d="M0 1700 L1080 1680" stroke="#8a6040" stroke-width="5" opacity=".8"/>'
# microscope (bottom-right) with a glowing slide
MX, MY = 860, 1690
scope = (f'<g transform="translate({MX} {MY})" stroke="#0a0d14" stroke-width="5" stroke-linejoin="round">'
         '<rect x="-80" y="-30" width="160" height="30" rx="8" fill="#e8ecf2"/>'
         '<path d="M40 -30 q30 -120 -20 -230 l-30 14 q40 100 10 216z" fill="#e8ecf2"/>'
         '<rect x="-70" y="-120" width="110" height="16" rx="4" fill="#3a4252"/>'
         '<rect x="-46" y="-126" width="60" height="6" fill="#7ff5d8" stroke-width="2"/>'
         '<g transform="rotate(-28 -10 -240)"><rect x="-34" y="-300" width="44" height="130" rx="8" fill="#3a4252"/><rect x="-26" y="-330" width="28" height="36" rx="6" fill="#5a6272"/>'
         '<rect x="-24" y="-172" width="24" height="30" fill="#8a93a6"/></g>'
         '<circle cx="34" cy="-160" r="16" fill="#8a93a6"/></g>')
b += f'<ellipse cx="{MX - 20}" cy="{MY - 120}" rx="90" ry="40" fill="#7ff5d8" opacity=".35" filter="url(#b12)"/>' + scope
# frog in a lab coat and goggles (bottom-left), looking up at the core
FX, FY, FS = 290, 1700, 3.2
b += f'<ellipse cx="{FX}" cy="{FY - 200}" rx="230" ry="220" fill="#7ff5d8" opacity=".1" filter="url(#b24)"/>'
b += f'<ellipse cx="{FX}" cy="{FY + 8}" rx="110" ry="14" fill="#000" opacity=".4"/>'
b += frog(FX, FY, FS, look=(4, -6), mouth='O', mid=LABCOAT, top=GOGGLES, sleeve='#f2f4f6',
          armL='M-34 -22 q-14 6 -16 22', armR='M38 -24 q18 -10 22 -34')
b += f'<rect width="{W}" height="{H}" fill="url(#vig)"/>'
write(HERE, '#040a14', defs, b, [('NEARLY', 110, 'w'), ('2 BILLION', 180, 'y'), ('YEARS', 110, 'w')], outline='#04101c', top=875)
