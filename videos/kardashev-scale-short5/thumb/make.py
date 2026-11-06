# Shorts thumbnail A for kardashev-scale-short5 (guideline 16-9: VERTICAL 1080x1920, text centred). Run: python3 make.py
# Layout: the Milky Way rises diagonally through the tall sky, text centred, rooftop + frog + telescope fill the bottom.
# AN OPEN / FRONTIER   intuitive: lights off, the Milky Way blazing over the rooftops; the frog in pyjamas and a nightcap sits on
#                      the roof ridge next to a small telescope, looking up; the attic window behind it is dark (light turned off).
#                      (script: "Tonight, when you turn off the light and look up at the night sky ... the quiet darkness is not
#                       empty space. It is an open frontier.")
import os, sys, math, random
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
sys.path.insert(0, os.path.join(REPO, 'tools'))
LONG = os.path.join(REPO, 'videos', 'kardashev-scale', 'thumb', 'make.py')
G = {'__file__': LONG}; exec(open(LONG).read().split('\nfor n, fn in')[0], G)
frog, starfield, FILTERS, P, INK = G['frog'], G['starfield'], G['FILTERS'], G['P'], G['INK']
from thumb_lib import vpage, vsvg, lin, rad, spark


def nightcap():
    return ('<g transform="translate(0 -12)"><path d="M-36 -84 q4 -40 44 -42 q34 0 44 28 q20 -4 34 20 q-20 -16 -36 -4 q6 12 4 22z" fill="#4a6ad0" stroke-width="4"/>'
            '<path d="M-20 -104 q14 -16 32 -16" fill="none" stroke="#a8c0ff" stroke-width="3.5" opacity=".8"/>'
            '<circle cx="-12" cy="-110" r="3" fill="#f2d27a" stroke="none"/><circle cx="20" cy="-114" r="3" fill="#f2d27a" stroke="none"/><circle cx="40" cy="-96" r="3" fill="#f2d27a" stroke="none"/>'
            '<path d="M-40 -84 q48 -12 96 2 q2 10 -4 12 q-44 -12 -90 0 q-6 -4 -2 -14z" fill="#f4f0e4" stroke-width="3.4"/>'
            '</g>')


def pyjama():
    return ('<path d="M-33 -30 q36 12 72 -2 l3 26 q0 10 -6 12 q-36 6 -70 -4 q-2 -16 1 -32z" fill="#4a6ad0" stroke-width="3.6"/>'
            '<path d="M-24 -22 V2 M-4 -18 V6 M16 -18 V6 M34 -24 V0" stroke="#a8c0ff" stroke-width="3" fill="none"/>'
            '<circle cx="4" cy="-16" r="2.6" fill="#f4f0e4" stroke="none"/><circle cx="4" cy="-6" r="2.6" fill="#f4f0e4" stroke="none"/>')


def make():
    rnd = random.Random(61)
    mwx, mwy, mwa = 780, 200, -62          # Milky Way band centre and angle
    d = FILTERS
    d += lin('sky', [(0, '#050720'), (.6, '#120c38'), (.85, '#3a1a4a'), (1, '#6a2a4a')], 0, 1)
    d += rad('vig', 540, 960, 1150, [(0, '#000', 0), (.7, '#000', 0), (1, '#000', .6)])
    d += lin('roof', [(0, '#3a1e22'), (1, '#1a0c10')], 0, 1)
    d += rad('hor', 640, 1660, 900, [(0, '#ff9a5a', .55), (.35, '#c0406a', .25), (1, '#3a1a4a', 0)])
    d += rad('scope', 780, 640, 120, [(0, '#bfe6ff', .6), (1, '#bfe6ff', 0)])
    d += rad('txtBg', 540, 950, 560, [(0, '#04051a', .5), (.6, '#04051a', .25), (1, '#04051a', 0)])
    b = '<rect width="1080" height="1920" fill="url(#sky)"/>'
    b += '<rect width="1080" height="1920" fill="url(#hor)"/>'
    b += starfield(rnd, 620, (0, 0, 1080, 1700))
    # ---- Milky Way ----
    ca, sa = math.cos(math.radians(mwa)), math.sin(math.radians(mwa))
    def mp(u, v):
        return mwx + u * ca - v * sa, mwy + u * sa + v * ca
    g = f'<g transform="translate({mwx} {mwy}) rotate({mwa})">'
    g += '<ellipse cx="0" cy="0" rx="1250" ry="250" fill="#4a3a9a" opacity=".45" filter="url(#b50)"/>'
    g += '<ellipse cx="-80" cy="0" rx="1000" ry="150" fill="#9a7ae0" opacity=".5" filter="url(#b50)"/>'
    g += '<ellipse cx="-260" cy="10" rx="420" ry="140" fill="#ffc890" opacity=".5" filter="url(#b50)"/>'
    g += '<ellipse cx="-300" cy="10" rx="220" ry="85" fill="#fff0d0" opacity=".65" filter="url(#b24)"/>'
    g += '<ellipse cx="-300" cy="8" rx="110" ry="40" fill="#ffffff" opacity=".7" filter="url(#b12)"/>'
    for _ in range(18):   # pink / blue nebula knots
        g += f'<ellipse cx="{rnd.uniform(-900, 900):.0f}" cy="{rnd.gauss(0, 60):.0f}" rx="{rnd.uniform(40, 110):.0f}" ry="{rnd.uniform(20, 50):.0f}" fill="{rnd.choice(["#ff6aa8", "#ff8a7a", "#6ab0ff", "#c08aff"])}" opacity="{rnd.uniform(.18, .35):.2f}" filter="url(#b12)"/>'
    # dark dust lanes
    for k, (off, w, op) in enumerate(((-6, 18, .4), (22, 10, .3), (-34, 8, .25))):
        pts = [(u, off + 22 * math.sin(u / 140 + k) + rnd.uniform(-6, 6)) for u in range(-1100, 1101, 50)]
        g += f'<polyline points="{P(pts)}" fill="none" stroke="#0a0618" stroke-width="{w}" opacity="{op}" filter="url(#b6)" stroke-linecap="round"/>'
    for _ in range(1500):   # dense star field along the band
        u = rnd.uniform(-1150, 1150); v = rnd.gauss(0, 85 if abs(u + 300) > 300 else 110)
        g += f'<circle cx="{u:.0f}" cy="{v:.0f}" r="{rnd.choice([.9, 1.2, 1.6, 2.1])}" fill="{rnd.choice(["#ffffff", "#ffe8d0", "#d8e4ff"])}" opacity="{rnd.uniform(.35, .95):.2f}"/>'
    g += '</g>'
    b += g
    for k in range(9):   # bright stars with glints
        x, y = rnd.uniform(60, 1020), rnd.uniform(60, 1500)
        b += spark(int(x), int(y), rnd.choice([10, 13, 16]), op=.9)
    b += '<path d="M980 150 L800 290" stroke="#fff" stroke-width="4" opacity=".85" stroke-linecap="round"/><path d="M980 150 L740 340" stroke="#fff" stroke-width="12" opacity=".2" filter="url(#b3)" stroke-linecap="round"/>'   # shooting star
    b += '<rect width="1080" height="1920" fill="url(#txtBg)"/>'
    # ---- distant hills and a sleeping town (lights off) ----
    b += '<path d="M0 1700 Q300 1650 620 1680 T1080 1670 V1920 H0z" fill="#140c22"/>'
    for k in range(30):
        x = -10 + k * 37 + rnd.uniform(-8, 8); h = rnd.uniform(30, 90); w = rnd.uniform(26, 40)
        b += f'<rect x="{x:.0f}" y="{1700 - h:.0f}" width="{w:.0f}" height="{h + 40:.0f}" fill="#0c0718"/>'
        if rnd.random() < .18:
            b += f'<rect x="{x + 8:.0f}" y="{1700 - h + 12:.0f}" width="7" height="9" fill="#ffd27a" opacity=".8"/>'
    b += '<path d="M0 1740 Q500 1715 1080 1735 V1920 H0z" fill="#0a0612"/>'
    SKY = b; b = ''
    # ---- the roof in the foreground ----
    roof = 'M-20 1100 L-20 840 L760 735 L1180 1100z'
    b += f'<path d="{roof}" fill="url(#roof)" stroke="#0a0408" stroke-width="6"/>'
    for k in range(1, 9):   # tile rows, lit by the sky on their upper edges
        y0 = 840 + k * 34; x1 = 760 + (1180 - 760) * (k * 34 + 735 - 735) / 365
        b += f'<path d="M-20 {y0 + k * 1:.0f} L{760 + k * 47:.0f} {735 + k * 40:.0f}" stroke="#6a3a4a" stroke-width="3" opacity=".55"/>'
    b += '<path d="M-20 840 L760 735 L1180 1100" fill="none" stroke="#c08aa0" stroke-width="5" opacity=".55"/>'
    # chimney
    b += '<path d="M150 820 L150 660 L250 660 L250 806z" fill="#4a2228" stroke="#0a0408" stroke-width="6"/><rect x="138" y="640" width="124" height="26" fill="#5a2a30" stroke="#0a0408" stroke-width="6"/>'
    b += '<path d="M156 668 H244" stroke="#c08aa0" stroke-width="3" opacity=".5"/>'
    # dormer with a dark window (light switched off)
    b += '<path d="M330 800 L330 700 L410 640 L490 700 L490 780z" fill="#3a1c22" stroke="#0a0408" stroke-width="6"/>'
    b += '<rect x="360" y="705" width="100" height="72" rx="6" fill="#0a0a1a" stroke="#0a0408" stroke-width="5"/><path d="M410 705 V777 M360 741 H460" stroke="#3a2a3a" stroke-width="5"/>'
    b += '<path d="M368 712 L392 712 L372 736z" fill="#8a9ad0" opacity=".35"/>'
    # telescope on a little tripod, pointing up at the band
    tx, ty = 870, 770
    b += f'<circle cx="{tx - 70}" cy="{ty - 150}" r="110" fill="url(#scope)"/>'
    b += f'<path d="M{tx} {ty - 50} L{tx - 40} {ty + 40} M{tx} {ty - 50} L{tx + 40} {ty + 46} M{tx} {ty - 50} L{tx + 4} {ty + 48}" stroke="{INK}" stroke-width="7"/>'
    b += f'<g transform="translate({tx} {ty - 60}) rotate(-50)"><rect x="-40" y="-17" width="170" height="34" rx="8" fill="#e8e4f0" stroke="{INK}" stroke-width="5"/>'
    b += f'<rect x="120" y="-22" width="28" height="44" rx="6" fill="#4a6ad0" stroke="{INK}" stroke-width="5"/><path d="M-30 -9 H110" stroke="#fff" stroke-width="4" opacity=".8"/></g>'
    # frog in pyjamas + nightcap sitting on the ridge, looking up
    b += frog(640, 748, 2.4, rot=-6, look=(6, -8), mouth='O', armL='M-34 -22 q-26 -4 -36 -32', armR='M38 -22 q34 -8 50 -30',
              legs=((-20, -6, -30, 6, -14), (20, -6, 30, 8, 14)), brows=False, back='', front=pyjama() + nightcap())
    b = SKY + f'<g transform="translate(-212 758) scale(1.2)">{b}</g>'
    b += '<rect width="1080" height="1920" fill="url(#vig)"/>'
    lines = [('AN OPEN', 150, 'w'), ('<span class="g">FRONTIER</span>', 180, 'w')]
    return vpage('#050720', vsvg(d, b), lines, outline='#04051a', top=800)


open(os.path.join(HERE, 'A.html'), 'w').write(make())
print('ok')
