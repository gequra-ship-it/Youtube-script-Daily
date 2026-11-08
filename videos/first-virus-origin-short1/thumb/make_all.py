# Shorts thumbnails (style B, guideline 16-9) for first-virus-origin-short1..5. VERTICAL 1080x1920, glow hero top half, hook centred y 860-1240, frog bottom corner.
# Run: python3 videos/first-virus-origin-short1/thumb/make_all.py [1 2 3 4 5] -> videos/first-virus-origin-shortN/thumb/A.html
# 1 ALIVE OR NOT?      virus capsid half dead stone / half awake cyan glow, cell with a lock below; frog doctor with stethoscope (short1: inert particle vs takeover)
# 2 OLDER THAN CELLS?  glowing RNA strand gathering a protein coat in a boiling early sea under volcanoes; frog in diving helmet (short2: hypothesis, hedged by "?")
# 3 A VIRUS THIS BIG?  light-microscope field: Mimivirus + Pandoravirus beside a smaller bacterium; frog in goggles at the microscope (short3)
# 4 YOUR DNA 8% VIRUS  magenta DNA helix with a gold viral stretch stitched in by a retrovirus; frog museum guard lighting an exhibit jar (short4)
# 5 VIRUSES FEED THE SEA  phages bursting a marine bacterium, gold carbon/nitrogen/phosphorus spill, plankton below; snorkel frog (short5)
import os, sys, math, random, shutil
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
sys.path.insert(0, os.path.join(REPO, 'tools'))
sys.path.insert(0, os.path.join(REPO, 'videos', 'trilobite-extinction', 'thumb'))
from make import frog, FILTERS, INK, GREEN   # shared posable frog (eye white #f4f5ea, pupil kept inside)
from thumb_lib import vpage, vsvg, lin, rad, spark, fireflies, halo, darkband

W, H = 1080, 1920


def hexrgb(c):
    c = c.lstrip('#'); return [int(c[i:i + 2], 16) for i in (0, 2, 4)]


def mix(a, b, t):
    A, B = hexrgb(a), hexrgb(b); t = max(0, min(1, t))
    return '#' + ''.join(f'{round(x + (y - x) * t):02x}' for x, y in zip(A, B))


def poly(pts):
    return 'M' + ' L'.join(f'{x:.1f} {y:.1f}' for x, y in pts) + 'Z'


def vig(id='vig', a=.75):
    return rad(id, 540, 960, 1250, [(0, '#000', 0), (.5, '#000', 0), (1, '#000', a)])


def icosa(cx, cy, r, light, dark, line, lw=5, op=1, rot=0, edge=None):
    """icosahedral capsid seen down a 3-fold axis: hexagon rim, inner triangle, 10 shaded facets (light from upper left)"""
    Hx = lambda a: (cx + r * math.cos(math.radians(a + rot)), cy + r * math.sin(math.radians(a + rot)))
    T = [(cx + r * .5 * math.cos(math.radians(-90 + 120 * k + rot)), cy + r * .5 * math.sin(math.radians(-90 + 120 * k + rot))) for k in range(3)]
    faces = [T[:]]
    for k in range(3):
        a = -90 + 120 * k
        faces += [[T[k], Hx(a - 60), Hx(a)], [T[k], Hx(a), Hx(a + 60)], [T[k], T[(k + 1) % 3], Hx(a + 60)]]
    o = ''
    for f in faces:
        mx = sum(p[0] for p in f) / 3 - cx; my = sum(p[1] for p in f) / 3 - cy
        t = .62 - (mx * -.6 + my * -.8) / r * .9
        o += f'<path d="{poly(f)}" fill="{mix(light, dark, t)}" fill-opacity="{op}" stroke="{line}" stroke-width="{lw}" stroke-linejoin="round"/>'
    if edge:
        o += f'<path d="{poly([Hx(-90 + 60 * k) for k in range(6)])}" fill="none" stroke="{edge}" stroke-width="{lw * 1.4}" stroke-linejoin="round"/>'
    return o


def hexverts(cx, cy, r, rot=0):
    return [(cx + r * math.cos(math.radians(-90 + 60 * k + rot)), cy + r * math.sin(math.radians(-90 + 60 * k + rot))) for k in range(6)]


def bubbles(rnd, n, x0, x1, y0, y1, col='#dff6ff', op=.55):
    return ''.join(f'<circle cx="{rnd.uniform(x0, x1):.0f}" cy="{rnd.uniform(y0, y1):.0f}" r="{rnd.choice([4, 6, 9, 12])}" fill="none" stroke="{col}" stroke-width="2.4" opacity="{op}"/>' for _ in range(n))


def save(n, bg, d, b, lines, outline, top):
    out = os.path.join(REPO, 'videos', f'first-virus-origin-short{n}', 'thumb'); os.makedirs(out, exist_ok=True)
    for f in ('common.css', 'Fredoka-700.woff2'):
        shutil.copy(os.path.join(REPO, 'tools', 'assets', 'thumb_v', f), out)
    open(os.path.join(out, 'A.html'), 'w').write(vpage(bg, vsvg(d, b), lines, outline=outline, top=top))


# ================= 1: ALIVE OR NOT? =================
def make_1():
    rnd = random.Random(11)
    CX, CY, R = 540, 470, 270
    d = FILTERS + rad('bg1', 540, 560, 1500, [(0, '#0f3a4a', 1), (.4, '#071a26', 1), (1, '#020609', 1)]) + vig()
    d += halo('h1', CX + 60, CY, 600, inner='#e8ffff', outer='#3fd8ff')
    d += f'<clipPath id="lhalf"><path d="M0 0 L{CX - 10} 0 L{CX + 30} {CY - 150} L{CX - 25} {CY - 40} L{CX + 20} {CY + 70} L{CX - 30} {CY + 180} L{CX} {H} L0 {H}Z"/></clipPath>'
    d += ('<filter id="grain" x="0" y="0" width="100%" height="100%"><feTurbulence type="fractalNoise" baseFrequency="1.1" numOctaves="2" seed="3"/>'
          '<feColorMatrix type="matrix" values="0 0 0 0 .1  0 0 0 0 .1  0 0 0 0 .1  0 0 0 .7 -.2"/><feComposite in2="SourceGraphic" operator="in"/></filter>')
    d += lin('cell1', [(0, '#e070a0'), (.4, '#8a2a5a'), (1, '#2a0a1e')])
    b = f'<rect width="{W}" height="{H}" fill="url(#bg1)"/>'
    b += ''.join(f'<circle cx="{rnd.uniform(0, W):.0f}" cy="{rnd.uniform(0, H):.0f}" r="{rnd.choice([1.2, 1.8, 2.6])}" fill="#cff6ff" opacity="{rnd.uniform(.15, .6):.2f}"/>' for _ in range(110))
    b += f'<ellipse cx="{CX + 60}" cy="{CY}" rx="620" ry="560" fill="url(#h1)"/>'
    b += f'<ellipse cx="{CX + 150}" cy="{CY}" rx="300" ry="360" fill="#5fe8ff" opacity=".55" filter="url(#b50)"/>'
    # spikes (fibres with knobs) at the 6 rim vertices + 6 edge midpoints
    V = hexverts(CX, CY, R)
    tips = []
    for k in range(6):
        a = math.radians(-90 + 60 * k); tips.append((V[k], a, 78))
        m = ((V[k][0] + V[(k + 1) % 6][0]) / 2, (V[k][1] + V[(k + 1) % 6][1]) / 2); tips.append((m, a + math.radians(30), 52))
    for (x, y), a, L in tips:
        ex, ey = x + L * math.cos(a), y + L * math.sin(a)
        alive = x > CX
        col = '#bffcff' if alive else '#7a8088'
        b += f'<path d="M{x:.0f} {y:.0f} L{ex:.0f} {ey:.0f}" stroke="#04121a" stroke-width="15" stroke-linecap="round"/><path d="M{x:.0f} {y:.0f} L{ex:.0f} {ey:.0f}" stroke="{col}" stroke-width="7" stroke-linecap="round"/>'
        if alive: b += f'<circle cx="{ex:.0f}" cy="{ey:.0f}" r="26" fill="#7ff0ff" opacity=".5" filter="url(#b12)"/>'
        b += f'<circle cx="{ex:.0f}" cy="{ey:.0f}" r="15" fill="{col}" stroke="#04121a" stroke-width="5"/>'
    # genome coil inside (seen through the glowing half)
    pts = []
    for i in range(240):
        t = i / 239 * 7 * math.pi; rr = 40 + 150 * i / 239
        pts.append((CX + rr * math.cos(t) * 1.0, CY + rr * math.sin(t) * .9))
    coil = 'M' + ' L'.join(f'{x:.1f} {y:.1f}' for x, y in pts)
    b += f'<path d="{poly(V)}" fill="#0a4a60"/><circle cx="{CX + 90}" cy="{CY}" r="190" fill="#bff8ff" opacity=".55" filter="url(#b50)"/>'
    b += f'<path d="{coil}" fill="none" stroke="#fff3a8" stroke-width="22" opacity=".45" filter="url(#b6)"/><path d="{coil}" fill="none" stroke="#fffbe0" stroke-width="7"/>'
    # awake half: translucent cyan facets
    b += icosa(CX, CY, R, '#efffff', '#2aa8d0', '#dfffff', lw=5, op=.32)
    # dead half: opaque grey stone facets + grain, clipped to the left of a jagged crack
    b += '<g clip-path="url(#lhalf)">' + icosa(CX, CY, R, '#b4b8bc', '#3a3e44', '#1a1c20', lw=6)
    b += f'<path d="{poly(V)}" fill="#fff" filter="url(#grain)" opacity=".9"/>'
    for _ in range(14):
        x, y = rnd.uniform(CX - R + 40, CX - 30), rnd.uniform(CY - 180, CY + 180)
        b += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{rnd.uniform(3, 8):.0f}" fill="#2a2c30" opacity=".6"/>'
    b += '</g>'
    crack = f'M{CX - 10} {CY - R + 2} L{CX + 30} {CY - 150} L{CX - 25} {CY - 40} L{CX + 20} {CY + 70} L{CX - 30} {CY + 180} L{CX} {CY + R - 4}'
    b += f'<path d="{crack}" fill="none" stroke="#9ff6ff" stroke-width="26" opacity=".6" filter="url(#b12)"/><path d="{crack}" fill="none" stroke="#f4ffff" stroke-width="6" stroke-linejoin="round"/>'
    b += f'<path d="{poly(V)}" fill="none" stroke="#04121a" stroke-width="10" stroke-linejoin="round"/>'
    b += f'<path d="M{V[0][0]:.0f} {V[0][1]:.0f} L{V[1][0]:.0f} {V[1][1]:.0f} L{V[2][0]:.0f} {V[2][1]:.0f}" fill="none" stroke="#f4ffff" stroke-width="5" opacity=".9"/>'
    for sx, sy, ss in ((CX + 360, CY - 210, 26), (CX + 330, CY + 210, 20), (CX - 380, CY - 260, 14), (CX + 160, CY - 330, 18), (CX + 420, CY + 20, 16)):
        b += spark(sx, sy, ss, col='#f0ffff')
    b += fireflies(45, 160, 1820, col='#9ff0ff', core='#efffff', seed=12)
    b += darkband(860, 1240, .5)
    # host cell below the text: membrane with a glowing lock (receptor)
    b += '<circle cx="900" cy="1960" r="560" fill="#ff7ab0" opacity=".25" filter="url(#b50)"/>'
    b += '<circle cx="900" cy="1960" r="520" fill="url(#cell1)" stroke="#1a0612" stroke-width="10"/>'
    b += '<circle cx="900" cy="1960" r="496" fill="none" stroke="#ffb8d4" stroke-width="5" opacity=".6"/>'
    for j in range(46):
        a = math.radians(180 + j * 4)
        b += f'<circle cx="{900 + 508 * math.cos(a):.0f}" cy="{1960 + 508 * math.sin(a):.0f}" r="5" fill="#ffd0e2" opacity=".55"/>'
    for x, y, r in ((760, 1720, 60), (1000, 1660, 44), (880, 1820, 36)):
        b += f'<ellipse cx="{x}" cy="{y}" rx="{r}" ry="{r * .6:.0f}" fill="#5a1036" stroke="#ff9cc4" stroke-width="3" opacity=".8"/>'
    LX, LY = 720, 1500
    b += f'<circle cx="{LX}" cy="{LY}" r="70" fill="#fff3a8" opacity=".45" filter="url(#b24)"/>'
    b += (f'<g transform="translate({LX} {LY}) rotate(-24)"><rect x="-34" y="-30" width="68" height="60" rx="14" fill="#ffd66a" stroke="#2a1606" stroke-width="5"/>'
          '<path d="M-20 -30 L-20 -52 A20 20 0 0 1 20 -52 L20 -30" fill="none" stroke="#2a1606" stroke-width="14"/><path d="M-20 -30 L-20 -52 A20 20 0 0 1 20 -52 L20 -30" fill="none" stroke="#e8e2c8" stroke-width="7"/>'
          '<circle cx="0" cy="-4" r="8" fill="#2a1606"/><path d="M-4 0 L-6 16 L6 16 L4 0Z" fill="#2a1606"/></g>')
    # frog doctor: head mirror + stethoscope held up toward the virus
    head = ('<path d="M-30 -80 q36 -18 70 0" fill="none" stroke-width="7"/><path d="M-30 -80 q36 -18 70 0" fill="none" stroke="#e8e8f0" stroke-width="3.4"/>'
            '<circle cx="6" cy="-98" r="12" fill="#d8e4ec" stroke-width="3.2"/><circle cx="6" cy="-98" r="6" fill="#f8ffff" stroke="none"/>')
    mid = ('<path d="M-30 -30 q4 22 26 26 q22 -2 34 -26" fill="none" stroke-width="6.5"/><path d="M-30 -30 q4 22 26 26 q22 -2 34 -26" fill="none" stroke="#5a6aa8" stroke-width="3"/>'
           '<path d="M30 -30 q30 0 34 -38" fill="none" stroke-width="6.5"/><path d="M30 -30 q30 0 34 -38" fill="none" stroke="#5a6aa8" stroke-width="3"/>')
    front = '<circle cx="66" cy="-74" r="9" fill="#d8dce4" stroke-width="3"/><circle cx="63" cy="-77" r="3" fill="#fff" stroke="none"/>'
    b += '<ellipse cx="260" cy="1600" rx="230" ry="200" fill="#9ff0ff" opacity=".14" filter="url(#b24)"/>'
    b += frog(250, 1740, 3.3, look=(3, -5), mouth='O', shadow=True, mid=head + mid, front=front, armR='M38 -22 q22 -6 28 -42', armL='M-34 -22 q-14 6 -16 22')
    b += f'<rect width="{W}" height="{H}" fill="url(#vig)"/>'
    save(1, '#020609', d, b, [('ALIVE', 230, 'y'), ('OR NOT?', 168, 'w')], '#020a10', 868)


# ================= 2: OLDER THAN CELLS? =================
def make_2():
    rnd = random.Random(22)
    HZ = 400; CX, CY, R = 540, 610, 190
    d = FILTERS + lin('sky2', [(0, '#1a0420'), (.5, '#5a0e2a'), (.85, '#c8401e'), (1, '#ff8a2a')])
    d += lin('sea2', [(0, '#7a2a2a'), (.12, '#3a0e22'), (.5, '#1a0616'), (1, '#07020a')]) + vig()
    d += halo('h2', CX, CY, 520, inner='#fff0d0', outer='#ff4fa0')
    d += rad('lava2', 300, HZ, 300, [(0, '#ffb04a', .9), (1, '#ff4a1a', 0)])
    d += lin('rock2', [(0, '#3a1a1e'), (1, '#120608')])
    b = f'<rect width="{W}" height="{HZ}" fill="url(#sky2)"/>'
    b += ''.join(f'<circle cx="{rnd.uniform(0, W):.0f}" cy="{rnd.uniform(0, HZ - 150):.0f}" r="{rnd.choice([1.2, 1.8])}" fill="#ffd8e8" opacity="{rnd.uniform(.2, .6):.2f}"/>' for _ in range(40))
    # volcanoes with lava glow + ash plumes + lightning
    b += f'<ellipse cx="300" cy="{HZ}" rx="320" ry="160" fill="url(#lava2)"/>'
    for px, ph, pw, col in ((300, 190, 260, '#2a0a12'), (820, 120, 220, '#3a1018'), (60, 90, 160, '#3a1018')):
        b += f'<path d="M{px - pw} {HZ} L{px - 34} {HZ - ph} L{px + 34} {HZ - ph} L{px + pw} {HZ}Z" fill="{col}"/>'
    b += f'<path d="M282 {HZ - 190} q-10 60 -40 110 q20 -10 30 -50 q10 50 0 140" fill="none" stroke="#ff8a2a" stroke-width="7" opacity=".9"/>'
    b += f'<ellipse cx="300" cy="{HZ - 190}" rx="40" ry="14" fill="#ffd27a" opacity=".9" filter="url(#b6)"/>'
    for j in range(7):
        b += f'<circle cx="{300 + j * 26 + rnd.uniform(-10, 10):.0f}" cy="{HZ - 230 - j * 26:.0f}" r="{40 + j * 9}" fill="#2a0e16" opacity=".75"/>'
    bolt = 'M860 140 L820 230 L852 236 L800 330 L880 210 L846 204 L880 140'
    b += f'<path d="{bolt}" fill="#ffe8ff" opacity=".7" filter="url(#b12)"/><path d="{bolt}" fill="#fff8ff"/>'
    # sea
    b += f'<rect y="{HZ}" width="{W}" height="{H - HZ}" fill="url(#sea2)"/>'
    b += f'<path d="M0 {HZ} L{W} {HZ}" stroke="#ffb07a" stroke-width="5" opacity=".8"/>'
    for j in range(6):
        b += f'<path d="M{80 + j * 180} {HZ} L{20 + j * 190} 1150 L{120 + j * 190} 1150Z" fill="#ff9a6a" opacity=".05"/>'
    b += bubbles(rnd, 40, 0, W, HZ + 20, 860, '#ffd0c0', .35)
    # organic soup: small ring molecules drifting
    for _ in range(26):
        x, y, s = rnd.uniform(30, 1050), rnd.uniform(HZ + 40, 850), rnd.uniform(10, 18)
        if math.hypot(x - CX, y - CY) < R + 60: continue
        b += f'<path d="{poly(hexverts(x, y, s, rnd.uniform(0, 60)))}" fill="none" stroke="#ffb0c8" stroke-width="3" opacity=".45"/>'
    b += f'<ellipse cx="{CX}" cy="{CY}" rx="560" ry="470" fill="url(#h2)"/>'
    # RNA strand: backbone + bases, coiling in through the gap of a half-built protein coat
    pts = []
    for i in range(300):
        u = i / 299
        if u < .35:   # comes in from the upper right
            t = u / .35; x = 1000 - (1000 - CX - 120) * t; y = HZ + 80 + (CY - 120 - HZ - 80) * t + 40 * math.sin(t * 9)
        else:
            t = (u - .35) / .65; a = -0.6 + t * 4.4 * math.pi; rr = 140 - 100 * t
            x = CX + rr * math.cos(a); y = CY + rr * math.sin(a) * .85
        pts.append((x, y))
    bb = 'M' + ' L'.join(f'{x:.1f} {y:.1f}' for x, y in pts)
    cols = ['#ffd84a', '#5ae0ff', '#ff6a8a', '#9aff7a']
    bases = ''
    for i in range(4, 296, 7):
        (x0, y0), (x1, y1) = pts[i - 1], pts[i + 1]
        nx, ny = -(y1 - y0), x1 - x0; L = math.hypot(nx, ny) or 1
        bases += f'<path d="M{x0:.0f} {y0:.0f} l{nx / L * 22:.1f} {ny / L * 22:.1f}" stroke="{cols[i % 4]}" stroke-width="7" stroke-linecap="round"/>'
    # back half of the coat
    caps = []
    for k in range(26):
        a = math.radians(70 + k * 10.4)
        caps.append((CX + R * math.cos(a), CY + R * math.sin(a), a))
    b += f'<circle cx="{CX}" cy="{CY}" r="{R + 6}" fill="#ff5fa8" opacity=".18"/>'
    b += f'<path d="{bb}" fill="none" stroke="#ff9ad0" stroke-width="30" opacity=".5" filter="url(#b12)"/>' + bases
    b += f'<path d="{bb}" fill="none" stroke="#2a0614" stroke-width="13" stroke-linecap="round"/><path d="{bb}" fill="none" stroke="#fff0f6" stroke-width="7" stroke-linecap="round"/>'
    for x, y, a in caps:
        b += (f'<g transform="translate({x:.0f} {y:.0f}) rotate({math.degrees(a):.0f})"><path d="{poly(hexverts(0, 0, 30, 30))}" fill="#ffb26a" stroke="#3a0a14" stroke-width="5"/>'
              f'<path d="{poly(hexverts(0, 0, 15, 30))}" fill="#ffe0a8" stroke="none"/><path d="M-14 -22 L12 -22" stroke="#fff6e0" stroke-width="4" opacity=".8"/></g>')
    # free coat pieces drifting toward the gap
    for x, y, rt in ((CX + 150, CY - 250, 10), (CX + 260, CY - 170, 40), (CX + 290, CY - 40, 20), (CX + 40, CY - 300, 50)):
        b += f'<circle cx="{x}" cy="{y}" r="44" fill="#ffb26a" opacity=".35" filter="url(#b12)"/>'
        b += f'<g transform="translate({x} {y}) rotate({rt})"><path d="{poly(hexverts(0, 0, 30, 30))}" fill="#ffb26a" stroke="#3a0a14" stroke-width="5"/><path d="{poly(hexverts(0, 0, 15, 30))}" fill="#ffe0a8"/></g>'
    for sx, sy, ss in ((CX - 300, CY - 160, 22), (CX + 330, CY + 150, 18), (CX - 240, CY + 220, 16), (CX + 210, CY - 330, 14)):
        b += spark(sx, sy, ss, col='#fff0f8')
    b += fireflies(40, HZ + 30, 1820, col='#ff9ad0', core='#fff0f6', seed=23)
    b += darkband(860, 1240, .5)
    # sea floor + rocks, rising bubbles; frog in a diving helmet
    b += f'<path d="M0 1610 Q300 1560 560 1600 T1080 1590 L1080 {H} L0 {H}Z" fill="url(#rock2)"/>'
    b += '<path d="M0 1610 Q300 1560 560 1600 T1080 1590" fill="none" stroke="#ff7a5a" stroke-width="4" opacity=".4"/>'
    for x, y, rx, ry in ((760, 1640, 120, 60), (930, 1610, 90, 70), (640, 1690, 60, 30)):
        b += f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{ry}" fill="#2a0e12" stroke="#0a0204" stroke-width="5"/><path d="M{x - rx * .7:.0f} {y - ry * .5:.0f} q{rx * .5:.0f} {-ry * .5:.0f} {rx:.0f} {-ry * .3:.0f}" fill="none" stroke="#ff8a5a" stroke-width="4" opacity=".5"/>'
    for x in (780, 920):
        for j in range(6):
            b += f'<circle cx="{x + 10 * math.sin(j * 1.7):.0f}" cy="{1560 - j * 52}" r="{5 + j * 1.6:.0f}" fill="none" stroke="#ffd8c8" stroke-width="2.5" opacity="{.7 - j * .08:.2f}"/>'
    b += '<ellipse cx="270" cy="1570" rx="230" ry="200" fill="#ff7ab0" opacity=".16" filter="url(#b24)"/>'
    b += frog(270, 1720, 3.3, look=(3, -5), mouth='O', shadow=True, helmet=True, armR='M38 -22 q22 -6 26 -40', armL='M-34 -22 q-16 4 -18 24')
    b += bubbles(rnd, 6, 330, 420, 1300, 1420, '#ffe8f0', .7)
    b += f'<rect width="{W}" height="{H}" fill="url(#vig)"/>'
    save(2, '#07020a', d, b, [('OLDER', 232, 'y'), ('THAN CELLS?', 132, 'w')], '#10020a', 875)


# ================= 3: A VIRUS THIS BIG? =================
def make_3():
    rnd = random.Random(33)
    FX, FY, R = 540, 470, 360
    d = FILTERS + rad('bg3', 540, 500, 1400, [(0, '#16301a', 1), (.45, '#08140a', 1), (1, '#010402', 1)]) + vig()
    d += rad('field3', FX - 60, FY - 80, R * 1.2, [(0, '#f8ffd8', 1), (.45, '#c8f07a', 1), (.85, '#6ab83a', 1), (1, '#2a6a1a', 1)])
    d += lin('ring3', [(0, '#e8eef0'), (.35, '#8a969c'), (.6, '#2a3236'), (1, '#6a7478')], x2=1, y2=1)
    d += lin('scope3', [(0, '#e4e8ea'), (.5, '#9aa4a8'), (1, '#4a5458')], x2=1, y2=0)
    d += f'<clipPath id="fc3"><circle cx="{FX}" cy="{FY}" r="{R}"/></clipPath>'
    b = f'<rect width="{W}" height="{H}" fill="url(#bg3)"/>'
    b += ''.join(f'<circle cx="{rnd.uniform(0, W):.0f}" cy="{rnd.uniform(0, H):.0f}" r="{rnd.choice([1.2, 1.8, 2.4])}" fill="#e8ffc8" opacity="{rnd.uniform(.1, .45):.2f}"/>' for _ in range(80))
    b += f'<circle cx="{FX}" cy="{FY}" r="{R + 190}" fill="#b8ff5a" opacity=".3" filter="url(#b50)"/>'
    b += f'<circle cx="{FX}" cy="{FY}" r="{R + 70}" fill="#e8ff9a" opacity=".25" filter="url(#b24)"/>'
    f = f'<g clip-path="url(#fc3)"><rect x="{FX - R}" y="{FY - R}" width="{2 * R}" height="{2 * R}" fill="url(#field3)"/>'
    for _ in range(18):
        f += f'<ellipse cx="{rnd.uniform(FX - R, FX + R):.0f}" cy="{rnd.uniform(FY - R, FY + R):.0f}" rx="{rnd.uniform(20, 70):.0f}" ry="{rnd.uniform(10, 30):.0f}" fill="#4a8a2a" opacity=".12" filter="url(#b6)"/>'
    # tiny ordinary viruses (dots) for contrast
    for _ in range(16):
        x, y = rnd.uniform(FX - 300, FX + 300), rnd.uniform(FY - 300, FY + 300)
        if math.hypot(x - 430, y - 500) < 230 or math.hypot(x - 760, y - 330) < 150: continue
        f += f'<path d="{poly(hexverts(x, y, 6))}" fill="#3a5a1a" stroke="#1a2a0a" stroke-width="1.5"/>'
    # small bacterium (rod) lower right
    BX, BY = 760, 680
    f += f'<g transform="translate({BX} {BY}) rotate(-20)"><rect x="-80" y="-34" width="160" height="68" rx="34" fill="#8ab84a" stroke="#1e3a10" stroke-width="5"/>'
    f += '<rect x="-64" y="-20" width="128" height="40" rx="20" fill="#b8e07a" opacity=".7"/><path d="M-60 -22 L40 -22" stroke="#f4ffd8" stroke-width="5" opacity=".7"/>'
    f += '<path d="M80 0 q30 -10 50 10 q20 20 46 6" fill="none" stroke="#1e3a10" stroke-width="4"/></g>'
    # Pandoravirus: amphora-shaped with an apical pore
    PX, PY = 790, 320
    f += (f'<g transform="translate({PX} {PY}) rotate(28)"><path d="M0 -120 C70 -120 80 -40 76 20 C70 90 40 120 0 120 C-40 120 -70 90 -76 20 C-80 -40 -70 -120 0 -120Z" '
          'fill="#c8a03a" stroke="#3a2a08" stroke-width="7"/><path d="M0 -104 C56 -104 64 -40 60 20 C56 80 30 104 0 104 C-30 104 -56 80 -60 20 C-64 -40 -56 -104 0 -104Z" fill="#e8c86a" opacity=".7"/>'
          '<ellipse cx="0" cy="-116" rx="20" ry="8" fill="#3a2a08"/><path d="M-40 -70 q-10 50 0 120" fill="none" stroke="#fff6c8" stroke-width="6" opacity=".7"/></g>')
    # Mimivirus: icosahedral capsid in a thick halo of fibres + a star-shaped portal
    MX, MY, MR = 430, 500, 150
    for k in range(260):
        a = rnd.uniform(0, 2 * math.pi); r0 = MR * .86; r1 = MR + rnd.uniform(36, 62)
        f += f'<path d="M{MX + r0 * math.cos(a):.1f} {MY + r0 * math.sin(a):.1f} L{MX + r1 * math.cos(a + rnd.uniform(-.05, .05)):.1f} {MY + r1 * math.sin(a):.1f}" stroke="{rnd.choice(["#5a7a1a", "#7a9a2a", "#3a5a12"])}" stroke-width="3" opacity=".8"/>'
    f += f'<circle cx="{MX}" cy="{MY}" r="{MR + 50}" fill="none" stroke="#2a4a0a" stroke-width="3" opacity=".4"/>'
    f += icosa(MX, MY, MR, '#fff2b0', '#8a6a1a', '#3a2a08', lw=5, edge='#2a1e06')
    star = ' '.join(f'{MX + (44 if j % 2 == 0 else 14) * math.cos(math.radians(-90 + j * 36)):.1f},{MY - 20 + (44 if j % 2 == 0 else 14) * math.sin(math.radians(-90 + j * 36)):.1f}' for j in range(10))
    f += f'<polygon points="{star}" fill="#fffbe0" stroke="#5a3a08" stroke-width="3" opacity=".85"/>'
    f += f'<circle cx="{FX}" cy="{FY}" r="{R}" fill="none" stroke="#000" stroke-width="80" opacity=".45" filter="url(#b24)"/></g>'
    b += f
    b += f'<circle cx="{FX}" cy="{FY}" r="{R + 22}" fill="none" stroke="#020402" stroke-width="40"/><circle cx="{FX}" cy="{FY}" r="{R + 14}" fill="none" stroke="url(#ring3)" stroke-width="18"/>'
    b += f'<path d="M{FX - R * .72:.0f} {FY - R * .72:.0f} A{R + 14} {R + 14} 0 0 1 {FX + R * .2:.0f} {FY - R - 12:.0f}" fill="none" stroke="#fff" stroke-width="5" opacity=".7"/>'
    for sx, sy, ss in ((FX - 400, FY - 260, 22), (FX + 400, FY + 220, 20), (FX + 380, FY - 330, 16), (FX - 420, FY + 300, 14)):
        b += spark(sx, sy, ss, col='#f4ffd8')
    b += fireflies(36, 160, 1820, col='#d8ff7a', core='#f8ffe0', seed=34)
    b += darkband(860, 1240, .5)
    # lab bench + microscope (right) and frog in goggles + lab coat (left)
    b += f'<path d="M0 1640 Q540 1610 1080 1640 L1080 {H} L0 {H}Z" fill="#1a2a1a"/><path d="M0 1640 Q540 1610 1080 1640" fill="none" stroke="#b8ff7a" stroke-width="4" opacity=".4"/>'
    b += '<ellipse cx="800" cy="1660" rx="190" ry="26" fill="#000" opacity=".5" filter="url(#b12)"/>'
    m = '<g transform="translate(800 1650)" stroke="#0a0e0c" stroke-width="7" stroke-linejoin="round">'
    m += '<rect x="-130" y="-40" width="260" height="40" rx="12" fill="url(#scope3)"/>'
    m += '<path d="M40 -40 L40 -170 Q40 -250 -30 -290 L-10 -320 Q80 -270 80 -170 L80 -40Z" fill="url(#scope3)"/>'
    m += '<rect x="-110" y="-150" width="170" height="24" rx="6" fill="#6a7478"/>'
    m += '<path d="M-60 -330 L-10 -230 L-40 -215 L-90 -315Z" fill="#cfd6da"/><rect x="-108" y="-372" width="60" height="56" rx="10" transform="rotate(-27 -78 -344)" fill="#9aa4a8"/>'
    m += '<rect x="-36" y="-226" width="34" height="70" rx="8" fill="#9aa4a8"/><circle cx="62" cy="-110" r="26" fill="#cfd6da"/>'
    m += '</g><ellipse cx="780" cy="1508" rx="44" ry="14" fill="#f4ffb0" opacity=".8" filter="url(#b6)"/>'
    b += m
    goggles = ('<path d="M-30 -66 L-40 -64 M42 -66 L52 -64" stroke-width="5"/><path d="M-30 -66 L-40 -64 M42 -66 L52 -64" stroke="#e8a83a" stroke-width="2.4"/>'
               '<circle cx="-10" cy="-66" r="18" fill="#cfffff" fill-opacity=".22" stroke-width="5"/><circle cx="22" cy="-66" r="18" fill="#cfffff" fill-opacity=".22" stroke-width="5"/>'
               '<path d="M8 -70 L4 -70" stroke-width="5"/><path d="M-20 -78 q6 -6 14 -6 M12 -78 q6 -6 14 -6" stroke="#fff" stroke-width="2.6" fill="none" opacity=".9"/>')
    coat = ('<path d="M-36 4 q-6 -40 6 -58 q8 24 20 40 l2 20z" fill="#f4f6f0" stroke-width="3.4"/><path d="M44 4 q6 -40 -6 -58 q-8 24 -20 40 l-2 20z" fill="#f4f6f0" stroke-width="3.4"/>'
            '<rect x="30" y="-24" width="9" height="14" rx="2" fill="#5a8ad0" stroke-width="2"/>')
    b += '<ellipse cx="300" cy="1580" rx="240" ry="200" fill="#d8ff7a" opacity=".14" filter="url(#b24)"/>'
    b += frog(300, 1740, 3.3, look=(3, -5), mouth='O', shadow=True, mid=coat + goggles, armR='M38 -22 q24 -4 34 -36', armL='M-34 -22 q-16 6 -18 24')
    b += f'<rect width="{W}" height="{H}" fill="url(#vig)"/>'
    save(3, '#010402', d, b, [('A VIRUS THIS', 118, 'w'), ('BIG?', 250, 'y')], '#020a04', 880)


# ================= 4: YOUR DNA 8% VIRUS =================
def make_4():
    rnd = random.Random(44)
    CX, CY = 540, 490
    d = FILTERS + rad('bg4', 540, 520, 1500, [(0, '#3a0a3a', 1), (.4, '#1a0420', 1), (1, '#05010a', 1)]) + vig()
    d += halo('h4', CX, CY, 600, inner='#ffe8f8', outer='#ff4fd8')
    d += lin('ped4', [(0, '#e8d8c8'), (.5, '#a89078'), (1, '#4a3a2a')], x2=1, y2=0)
    b = f'<rect width="{W}" height="{H}" fill="url(#bg4)"/>'
    b += ''.join(f'<circle cx="{rnd.uniform(0, W):.0f}" cy="{rnd.uniform(0, H):.0f}" r="{rnd.choice([1.2, 1.8, 2.4])}" fill="#ffd8f8" opacity="{rnd.uniform(.12, .5):.2f}"/>' for _ in range(90))
    b += f'<ellipse cx="{CX}" cy="{CY}" rx="640" ry="480" fill="url(#h4)" opacity=".9"/>'
    # double helix (tilted), back strand / rungs / front strand; a gold viral stretch in the middle
    A, ROT, N = 150, -22, 400
    x0, x1 = -600, 600; g0, g1 = -150, 150
    def P(x, ph):
        y = A * math.sin(x / 105 + ph); z = math.cos(x / 105 + ph)
        c, s = math.cos(math.radians(ROT)), math.sin(math.radians(ROT))
        return CX + x * c - y * s, CY + x * s + y * c, z
    seg = lambda ph, lo, hi: [P(x0 + (x1 - x0) * i / N, ph) for i in range(N + 1) if lo <= x0 + (x1 - x0) * i / N <= hi]
    def strand(ph, front, col, glow, lo, hi):
        o = ''; pts = seg(ph, lo, hi); run = []
        for p in pts + [(0, 0, -9 if front else 9)]:
            if (p[2] >= 0) == front and p[2] != (-9 if front else 9): run.append(p)
            else:
                if len(run) > 1:
                    dd = 'M' + ' L'.join(f'{x:.1f} {y:.1f}' for x, y, _ in run)
                    if glow: o += f'<path d="{dd}" fill="none" stroke="{glow}" stroke-width="44" opacity=".55" filter="url(#b12)" stroke-linecap="round"/>'
                    o += f'<path d="{dd}" fill="none" stroke="#14020e" stroke-width="{30 if front else 24}" stroke-linecap="round"/><path d="{dd}" fill="none" stroke="{col}" stroke-width="{18 if front else 13}" stroke-linecap="round"/>'
                    if front: o += f'<path d="{dd}" fill="none" stroke="#fff" stroke-width="4" opacity=".55" transform="translate(-3 -5)" stroke-linecap="round"/>'
                run = []
        return o
    for front in (False, True):
        for ph in (0, math.pi):
            if not front:
                b += strand(ph, False, '#8a2a7a', None, x0, x1)
        if not front:
            for i in range(0, 46):
                x = x0 + 24 + i * 25.6
                (ax, ay, _), (bx, by, _) = P(x, 0), P(x, math.pi)
                vir = g0 <= x <= g1
                cols = ('#ffd84a', '#ffb02a') if vir else (('#5ae0ff', '#ff6aa8') if i % 2 else ('#9aff7a', '#ffd0f0'))
                mx, my = (ax + bx) / 2, (ay + by) / 2
                if vir: b += f'<path d="M{ax:.0f} {ay:.0f} L{bx:.0f} {by:.0f}" stroke="#ffe27a" stroke-width="22" opacity=".5" filter="url(#b6)"/>'
                b += f'<path d="M{ax:.0f} {ay:.0f} L{bx:.0f} {by:.0f}" stroke="#14020e" stroke-width="13"/>'
                b += f'<path d="M{ax:.0f} {ay:.0f} L{mx:.0f} {my:.0f}" stroke="{cols[0]}" stroke-width="7"/><path d="M{mx:.0f} {my:.0f} L{bx:.0f} {by:.0f}" stroke="{cols[1]}" stroke-width="7"/>'
        else:
            for ph in (0, math.pi):
                b += strand(ph, True, '#ff9ae0', None, x0, g0) + strand(ph, True, '#ffe27a', '#ffd84a', g0, g1) + strand(ph, True, '#ff9ae0', None, g1, x1)
    # retrovirus up right, stitching its thread into the gold stretch
    VX, VY, VR = 850, 230, 70
    gx, gy, _ = P(90, 0)
    th = f'M{VX - 40} {VY + 50} C{VX - 80} {VY + 140} {gx + 120} {gy - 80} {gx:.0f} {gy:.0f}'
    b += f'<path d="{th}" fill="none" stroke="#ffe27a" stroke-width="16" opacity=".5" filter="url(#b6)"/><path d="{th}" fill="none" stroke="#fff3b0" stroke-width="5" stroke-dasharray="14 9"/>'
    b += f'<circle cx="{VX}" cy="{VY}" r="{VR + 60}" fill="#ffd84a" opacity=".3" filter="url(#b24)"/>'
    for k in range(14):
        a = math.radians(k * 360 / 14)
        ex, ey = VX + (VR + 30) * math.cos(a), VY + (VR + 30) * math.sin(a)
        b += f'<path d="M{VX + VR * math.cos(a):.0f} {VY + VR * math.sin(a):.0f} L{ex:.0f} {ey:.0f}" stroke="#2a1606" stroke-width="10"/><circle cx="{ex:.0f}" cy="{ey:.0f}" r="10" fill="#ffd84a" stroke="#2a1606" stroke-width="4"/>'
    b += f'<circle cx="{VX}" cy="{VY}" r="{VR}" fill="#e8a83a" stroke="#2a1606" stroke-width="7"/><circle cx="{VX}" cy="{VY}" r="{VR * .55:.0f}" fill="#ffe8a0" opacity=".8"/>'
    b += f'<path d="M{VX - 40} {VY - 30} q20 -26 50 -26" fill="none" stroke="#fff8e0" stroke-width="6" opacity=".9"/>'
    for sx, sy, ss in ((180, 220, 22), (960, 640, 18), (300, 760, 16), (620, 180, 14), (gx + 40, gy - 60, 20)):
        b += spark(sx, sy, ss, col='#fff0fa')
    b += fireflies(42, 160, 1820, col='#ff9ae0', core='#fff0fa', seed=45)
    b += darkband(860, 1240, .5)
    # museum below: pedestal with a glass bell jar (a strand of DNA inside), frog guard with a torch
    b += f'<path d="M0 1660 L1080 1660 L1080 {H} L0 {H}Z" fill="#160616"/><path d="M0 1660 L1080 1660" stroke="#ff9ae0" stroke-width="4" opacity=".35"/>'
    for j in range(5):
        b += f'<path d="M{j * 260 - 40} {H} L{j * 260 + 60} 1660" stroke="#3a1236" stroke-width="3"/>'
    b += '<ellipse cx="800" cy="1676" rx="170" ry="22" fill="#000" opacity=".5" filter="url(#b12)"/>'
    b += '<path d="M680 1670 L700 1520 L900 1520 L920 1670Z" fill="url(#ped4)" stroke="#1a0a06" stroke-width="6"/><rect x="670" y="1500" width="260" height="30" rx="6" fill="#e8d8c8" stroke="#1a0a06" stroke-width="6"/>'
    b += '<rect x="752" y="1580" width="96" height="44" rx="4" fill="#c8a03a" stroke="#3a2a08" stroke-width="3"/><path d="M766 1594 h68 M766 1608 h50" stroke="#3a2a08" stroke-width="4"/>'
    b += '<circle cx="800" cy="1420" r="110" fill="#ffd84a" opacity=".35" filter="url(#b24)"/>'
    for k in range(8):
        y = 1340 + k * 18
        b += f'<path d="M{770 + 22 * math.sin(k * .9):.0f} {y} L{830 - 22 * math.sin(k * .9):.0f} {y}" stroke="#ffd84a" stroke-width="6"/>'
    b += '<path d="M770 1340 ' + ' '.join(f'L{770 + 22 * math.sin(k * .9) * 0 + 30 - 30 * math.cos(k * .9):.0f} {1340 + k * 18}' for k in range(8)) + '" fill="none" stroke="#ff9ae0" stroke-width="5"/>'
    b += '<path d="M720 1500 L720 1360 A80 80 0 0 1 880 1360 L880 1500Z" fill="#dff4ff" fill-opacity=".14" stroke="#e8f6ff" stroke-width="5"/>'
    b += '<path d="M740 1370 q4 -50 40 -64" fill="none" stroke="#fff" stroke-width="7" opacity=".7"/><circle cx="800" cy="1272" r="12" fill="#e8f6ff" stroke="#1a0a06" stroke-width="4"/>'
    cap = ('<g transform="translate(0 -14)"><path d="M-24 -80 q30 -26 64 -2 l0 6 q-34 -6 -64 2z" fill="#2a3a7a" stroke-width="3.4"/><path d="M-30 -76 q36 -10 76 2 q4 6 -4 8 q-36 -10 -70 -2z" fill="#1a2450" stroke-width="3"/>'
           '<circle cx="8" cy="-90" r="6" fill="#f2d27a" stroke-width="2"/></g>')
    torch = ('<g transform="translate(70 -64) rotate(-48)"><path d="M0 -10 L120 -60 L120 60 L0 10Z" fill="#fff6c0" opacity=".35" stroke="none"/>'
             '<rect x="-30" y="-8" width="34" height="16" rx="3" fill="#3a3a44" stroke-width="2.6"/><rect x="2" y="-11" width="10" height="22" rx="2" fill="#c8c8d0" stroke-width="2.6"/></g>')
    b += '<ellipse cx="270" cy="1580" rx="230" ry="200" fill="#ff9ae0" opacity=".14" filter="url(#b24)"/>'
    b += frog(270, 1740, 3.3, look=(3, -4), mouth='O', shadow=True, mid=cap, front=torch, armR='M38 -22 q22 -6 30 -38', armL='M-34 -22 q-16 6 -18 24')
    b += f'<rect width="{W}" height="{H}" fill="url(#vig)"/>'
    save(4, '#05010a', d, b, [('YOUR DNA', 150, 'w'), ('<span class="g">8%</span> VIRUS', 196, 'w')], '#12020e', 885)


# ================= 5: VIRUSES FEED THE SEA =================
def make_5():
    rnd = random.Random(55)
    CX, CY = 520, 500
    d = FILTERS + lin('sea5', [(0, '#0a3a6a'), (.35, '#062448'), (.7, '#031428'), (1, '#01060e')]) + vig()
    d += halo('h5', CX + 140, CY - 60, 520, inner='#fff6c8', outer='#ffb02a')
    d += lin('cell5', [(0, '#7ad8c8'), (.5, '#2a8a8a'), (1, '#0a3a44')], x2=0, y2=1)
    b = f'<rect width="{W}" height="{H}" fill="url(#sea5)"/>'
    for x0, x1 in ((80, 260), (380, 470), (640, 820), (900, 1000)):
        b += f'<path d="M{x0} 0 L{x0 - 160} 1500 L{x1 - 60} 1500 L{x1} 0Z" fill="#8ad8ff" opacity=".05"/>'
    # countless tiny virus particles everywhere
    for _ in range(420):
        x, y = rnd.uniform(0, W), rnd.uniform(100, 1880)
        b += f'<path d="{poly(hexverts(x, y, rnd.choice([3, 4, 5])))}" fill="#a8d8ff" opacity="{rnd.uniform(.15, .5):.2f}"/>'
    b += f'<ellipse cx="{CX + 140}" cy="{CY - 60}" rx="600" ry="520" fill="url(#h5)"/>'
    # the marine bacterium: a capsule, ripped open at its upper-right end
    ROT = -24; L, RR = 260, 120
    c, s = math.cos(math.radians(ROT)), math.sin(math.radians(ROT))
    T = lambda x, y: (CX + x * c - y * s, CY + x * s + y * c)
    body = (f'<g transform="translate({CX} {CY}) rotate({ROT})">'
            f'<path d="M{L - 40} {-RR + 6} L{-L + RR} {-RR} A{RR} {RR} 0 0 0 {-L + RR} {RR} L{L - 50} {RR - 4} L{L - 20} {RR - 40} L{L - 60} 40 L{L - 10} 10 L{L - 50} -30 L{L - 10} -60Z" '
            'fill="url(#cell5)" stroke="#021418" stroke-width="9" stroke-linejoin="round"/>'
            f'<path d="M{-L + RR} {-RR + 26} L{L - 60} {-RR + 30}" stroke="#d8fff4" stroke-width="7" opacity=".6" stroke-linecap="round"/>'
            f'<path d="M{-L + 60} 0 q60 -40 120 0 t120 0 t100 -10" fill="none" stroke="#0a4a50" stroke-width="10" opacity=".7"/>'
            f'<path d="M{L - 40} {-RR + 6} L{L - 10} -60 L{L - 50} -30 L{L - 10} 10 L{L - 60} 40 L{L - 20} {RR - 40} L{L - 50} {RR - 4}" fill="none" stroke="#fff3b0" stroke-width="10" opacity=".9"/></g>')
    b += f'<ellipse cx="{CX}" cy="{CY}" rx="{L + 40}" ry="{RR + 50}" transform="rotate({ROT} {CX} {CY})" fill="#5ae0d0" opacity=".25" filter="url(#b24)"/>'
    b += body
    # phages docked on the cell, pointing in
    def phage(x, y, ang, sz=1.0, op=1):
        g = f'<g transform="translate({x:.0f} {y:.0f}) rotate({ang:.0f}) scale({sz})" stroke="#0a1a2a" stroke-width="3.6" stroke-linejoin="round" opacity="{op}">'
        g += '<path d="M-10 6 L-22 26 M10 6 L22 26 M-4 6 L-8 28 M4 6 L8 28" fill="none" stroke-width="3"/>'
        g += '<rect x="-4" y="-26" width="8" height="32" fill="#c8e0f0"/><rect x="-10" y="2" width="20" height="6" rx="2" fill="#8ab0d0"/>'
        g += f'<path d="{poly(hexverts(0, -42, 18, 30))}" fill="#e8f4ff"/><path d="M-8 -50 L4 -54" stroke="#fff" stroke-width="3"/></g>'
        return g
    for k in range(12):
        t = -L + 70 + k * 36
        for side in (-1, 1):
            if k % 2 == (side > 0): continue
            x, y = T(t, side * (RR + 26))
            b += phage(x, y, ROT + (0 if side > 0 else 180), 1.0)
    for x, y, a in ((CX - 330, CY - 210, 140), (CX - 380, CY + 150, 60), (CX + 40, CY + 300, 10), (CX - 120, CY - 290, 200)):
        b += phage(x, y, a, .9, .85)
    # the spill: carbon / nitrogen / phosphorus out of the torn end
    ox, oy = T(L, 0)
    for _ in range(70):
        a = math.radians(ROT + rnd.uniform(-70, 70)); r = rnd.uniform(30, 360)
        x, y = ox + r * math.cos(a), oy + r * math.sin(a)
        if y > 820 or y < 140 or x > 1060: continue
        rr = rnd.choice([5, 7, 9, 12])
        b += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{rr * 3}" fill="#ffc84a" opacity=".3" filter="url(#b6)"/><circle cx="{x:.0f}" cy="{y:.0f}" r="{rr}" fill="#fff0a8"/>'
    for (x, y, t) in ((ox + 150, oy - 150, 'C'), (ox + 250, oy - 30, 'N'), (ox + 120, oy + 110, 'P')):
        b += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="60" fill="#ffb02a" opacity=".45" filter="url(#b12)"/><circle cx="{x:.0f}" cy="{y:.0f}" r="36" fill="#ffd84a" stroke="#3a2006" stroke-width="5"/>'
        b += f'<text x="{x:.0f}" y="{y + 15:.0f}" text-anchor="middle" font-family="Fredoka" font-weight="700" font-size="44" fill="#3a2006">{t}</text>'
    for sx, sy, ss in ((ox + 60, oy - 260, 24), (ox - 120, oy - 200, 16), (CX - 400, CY - 40, 16), (ox + 300, oy + 160, 18)):
        b += spark(sx, sy, ss, col='#fffbe0')
    b += fireflies(30, 160, 1820, col='#ffd84a', core='#fff8d8', seed=56)
    b += darkband(860, 1240, .5)
    # below: plankton gathering on the spilled food (diatoms + a copepod), snorkel frog
    for x, y, r in ((640, 1430, 46), (840, 1360, 34), (960, 1560, 54), (720, 1640, 30)):
        b += f'<circle cx="{x}" cy="{y}" r="{r + 26}" fill="#7affc8" opacity=".25" filter="url(#b12)"/><circle cx="{x}" cy="{y}" r="{r}" fill="#2a8a6a" stroke="#04241a" stroke-width="5"/>'
        b += ''.join(f'<path d="M{x} {y} L{x + r * .8 * math.cos(math.radians(j * 30)):.0f} {y + r * .8 * math.sin(math.radians(j * 30)):.0f}" stroke="#9affd8" stroke-width="2.5" opacity=".8"/>' for j in range(12))
        b += f'<circle cx="{x}" cy="{y}" r="{r * .25:.0f}" fill="#d8ffe8"/>'
    for _ in range(18):
        x, y = rnd.uniform(560, 1040), rnd.uniform(1320, 1700)
        b += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="5" fill="#fff0a8" opacity=".85"/>'
    b += '<ellipse cx="270" cy="1580" rx="240" ry="200" fill="#ffd84a" opacity=".12" filter="url(#b24)"/>'
    mask = ('<rect x="-28" y="-84" width="68" height="36" rx="16" fill="#bff0ff" fill-opacity=".25" stroke-width="5"/><path d="M-28 -66 L-38 -64 M40 -66 L50 -64" stroke-width="5"/>'
            '<path d="M-20 -78 q8 -4 16 -2" stroke="#fff" stroke-width="3" fill="none"/>'
            '<path d="M50 -60 L56 -130 q2 -8 10 -6" fill="none" stroke-width="10"/><path d="M50 -60 L56 -130 q2 -8 10 -6" fill="none" stroke="#ffb02a" stroke-width="5"/>')
    b += frog(270, 1740, 3.3, rot=-8, look=(3, -5), mouth='O', shadow=False, mid=mask, armR='M38 -22 q24 -10 34 -40', armL='M-34 -22 q-24 -4 -34 -30')
    b += bubbles(rnd, 7, 440, 520, 1280, 1400, '#e8f8ff', .7)
    b += f'<rect width="{W}" height="{H}" fill="url(#vig)"/>'
    save(5, '#01060e', d, b, [('VIRUSES', 124, 'w'), ('FEED', 176, 'y'), ('THE SEA', 116, 'w')], '#020a14', 862)


if __name__ == '__main__':
    which = sys.argv[1:] or ['1', '2', '3', '4', '5']
    for n in which:
        fn = globals().get(f'make_{n}')
        if fn: fn(); print('made', n)
