# Shorts thumbnails (guideline 16-9, miya 2026-11-06, corrected same day): VERTICAL 1080x1920, text centred mid-frame,
# ONE per short -> videos/sharpest-blade-fastest-gun-shortN/thumb/A.html (+ tools/assets/thumb_v common.css/font).
# Reuses frog/glint/spark helpers from make.py (long form). Each = the single key scene of that short's script:
# 1 knife edge under the microscope = jagged mountains ("sharpness is an illusion", S02)
# 2 diamond knife ribbon on the water bath + a hair ("two thousand slices ... a single strand of hair", S06)
# 3 single-atom needle over a copper surface, frog nudging an atom (S01-S03)
# 4 paint fleck chipping a spacecraft window (S03)
# 5 LHC ring under the countryside, protons at 99.9999991% of light speed (S02, S05)
import os, sys, math, random, shutil, importlib.util
HERE = os.path.dirname(os.path.abspath(__file__))
TOOLS = os.path.join(HERE, '..', '..', '..', 'tools')
sys.path.insert(0, TOOLS)
from thumb_lib import vpage, vsvg, lin, rad, spark
spec = importlib.util.spec_from_file_location('lf', os.path.join(HERE, 'make.py')); lf = importlib.util.module_from_spec(spec); spec.loader.exec_module(lf)
frog, glint, SOFT, starfield = lf.frog, lf.glint, lf.SOFT, lf.starfield
Y = lambda w: f'<span class="g">{w}</span>'
W, H = 1080, 1920
CU = ('<radialGradient id="cuA" cx=".5" cy=".5" r=".55" fx=".35" fy=".3"><stop offset="0" stop-color="#ffe2b8"/>'
      '<stop offset=".45" stop-color="#e08a48"/><stop offset="1" stop-color="#6a2e10"/></radialGradient>')


def textshade(y0, y1, col='#000', op=.45):   # soft dark band behind the centred text
    return f'<rect x="-100" y="{y0}" width="1280" height="{y1 - y0}" fill="{col}" opacity="{op}" filter="url(#blur30)"/>'


# ============ 1: knife (top) + big magnifier with a jagged mountain range (bottom) ============
def make_1():
    d = SOFT + lin('bg1', [(0, '#2a2236'), (.5, '#141020'), (1, '#07060c')])
    d += rad('lamp1', 860, 160, 900, [(0, '#ffe7b8', .35), (.5, '#ffb76a', .08), (1, '#ffb76a', 0)])
    b = f'<rect width="{W}" height="{H}" fill="url(#bg1)"/><rect width="{W}" height="{H}" fill="url(#lamp1)"/>'
    # knife, diagonal across the top, edge up, tip to the upper right
    d += lin('k1', [(0, '#f4f7fb'), (.25, '#d0d8e4'), (.7, '#8d98aa'), (1, '#5a6476')])
    k = '<g transform="translate(-50 460) scale(.66) rotate(-24)">'
    k += '<ellipse cx="760" cy="400" rx="720" ry="26" fill="#000" opacity=".35" filter="url(#blur12)"/>'
    k += '<rect x="40" y="292" width="380" height="96" rx="40" fill="#2b1a12" stroke="#0c0604" stroke-width="6"/>'
    k += ''.join(f'<circle cx="{x}" cy="340" r="12" fill="#d8dee8" stroke="#0c0604" stroke-width="3"/>' for x in (130, 230, 330))
    k += '<rect x="410" y="270" width="44" height="130" rx="10" fill="#aab4c4" stroke="#0c0604" stroke-width="6"/>'
    k += '<path d="M454 386 L1300 386 Q1420 380 1500 340 Q1240 220 900 192 Q640 180 454 190 Z" fill="url(#k1)" stroke="#0c0604" stroke-width="6"/>'
    k += '<path d="M470 202 Q660 192 900 204 Q1230 230 1488 338" fill="none" stroke="#ffffff" stroke-width="5"/>'
    k += '<path d="M470 230 Q800 230 1100 260" fill="none" stroke="#ffffff" stroke-width="3" opacity=".45"/>'
    k += glint(1100, 230, 34, '#ffffff', 1) + '<circle cx="900" cy="196" r="34" fill="none" stroke="#bfe9ff" stroke-width="5"/>'
    k += '</g>'
    b += k
    # magnifier lens (hero), handle down-left
    cx, cy, r = 560, 1420, 330
    b += f'<path d="M{cx - r * .7:.0f} {cy + r * .7:.0f} L{cx - r * 1.15:.0f} {cy + r * 1.15:.0f}" stroke="#0c0604" stroke-width="70" stroke-linecap="round"/>'
    b += f'<path d="M{cx - r * .72:.0f} {cy + r * .72:.0f} L{cx - r * 1.13:.0f} {cy + r * 1.13:.0f}" stroke="#7a2e1e" stroke-width="54" stroke-linecap="round"/>'
    d += f'<clipPath id="lens"><circle cx="{cx}" cy="{cy}" r="{r}"/></clipPath>'
    d += lin('sem', [(0, '#0a1420'), (1, '#1a2c3a')]) + lin('mtn', [(0, '#e8f2f8'), (.35, '#9fb4c4'), (1, '#2c3c4a')])
    L = f'<rect x="{cx - r}" y="{cy - r}" width="{2 * r}" height="{2 * r}" fill="url(#sem)"/>'

    def ridge(base, amp, seed):
        rr = random.Random(seed); pts = [(cx - r - 20, base + 300)]; x = cx - r - 20
        while x < cx + r + 40:
            pts.append((x, base - rr.uniform(.3, 1) * amp)); x += rr.uniform(30, 76)
            pts.append((x, base + rr.uniform(-.1, .35) * amp)); x += rr.uniform(18, 54)
        pts.append((cx + r + 40, base + 300))
        return ' '.join(f'{p[0]:.0f},{p[1]:.0f}' for p in pts), pts
    p2, _ = ridge(cy + 40, 130, 3)
    L += f'<polygon points="{p2}" fill="#3e5262" opacity=".8"/>'
    p1, pts = ridge(cy + 170, 250, 7)
    L += f'<polygon points="{p1}" fill="url(#mtn)" stroke="#0a141c" stroke-width="4"/>'
    for (x0, y0), (x1, y1) in zip(pts[1:-2:2], pts[2:-1:2]):
        L += f'<path d="M{x0:.0f} {y0:.0f} L{x1:.0f} {y1:.0f}" stroke="#ffffff" stroke-width="3" opacity=".7"/>'
    peak = min(pts[3:-3], key=lambda p: p[1] if abs(p[0] - cx - 60) < 170 else 9e9)
    helm = ('<path d="M-26 -78 q30 -34 62 0 z" fill="#e2412c" stroke-width="3"/><rect x="-28" y="-80" width="66" height="7" rx="3" fill="#b8301e" stroke-width="2.5"/>'
            '<circle cx="5" cy="-92" r="5" fill="#fff6d6" stroke-width="2"/>')
    L += frog(peak[0], peak[1] + 6, 2.3, look=(-4, 5), mouth='o', helmet=helm,
              armL='M-34 -22 q-24 -16 -22 -46', armR='M38 -22 q18 4 22 26', feet=((-22, 4, -14), (22, 4, 14)))
    b += f'<circle cx="{cx}" cy="{cy}" r="{r + 40}" fill="#bfe9ff" opacity=".15" filter="url(#blur30)"/>'
    b += f'<g clip-path="url(#lens)">{L}<ellipse cx="{cx - 110}" cy="{cy - 170}" rx="160" ry="60" transform="rotate(-30 {cx - 110} {cy - 170})" fill="#fff" opacity=".18"/></g>'
    b += f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="#0c0604" stroke-width="44"/><circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="#c7ced8" stroke-width="28"/>'
    b += f'<circle cx="{cx}" cy="{cy}" r="{r - 6}" fill="none" stroke="#ffffff" stroke-width="4" opacity=".7"/>'
    b += spark(cx + 280, cy - 300, 26) + spark(180, 240, 18, '#fff6d6', .8) + spark(950, 620, 16, '#fff6d6', .7)
    b += textshade(700, 1080, '#07060c', .55)
    return vpage('#141020', vsvg(d, b), [('SHARPNESS', 150, 'w'), ('IS AN', 104, 'w'), (Y('ILLUSION'), 166, 'w')], outline='#07060c', top=700)


# ============ 2: giant hair (top), text, diamond knife + slice ribbon on the water (bottom) ============
def make_2():
    rnd = random.Random(22); d = SOFT
    d += lin('bg2', [(0, '#0e2a33'), (.55, '#08161d'), (1, '#03080b')])
    d += rad('l2', 760, 1400, 760, [(0, '#bff6ff', .35), (.4, '#5ad2e8', .1), (1, '#5ad2e8', 0)])
    b = f'<rect width="{W}" height="{H}" fill="url(#bg2)"/><rect width="{W}" height="{H}" fill="url(#l2)"/>'
    b += starfield(rnd, 50, (20, 140, 1060, 1800), None, '#bff6ff', .4)
    # giant hair strand, diagonal across the top
    d += lin('hair', [(0, '#7a4a26'), (.35, '#c08048'), (.55, '#e0a56a'), (.8, '#6a3a1a'), (1, '#3a1e0c')])
    b += '<g transform="rotate(-18 540 420)"><rect x="160" y="300" width="1300" height="230" fill="url(#hair)" stroke="#1e0e04" stroke-width="6"/>'
    for kk in range(12):
        x = 200 + kk * 105
        b += f'<path d="M{x} 302 q34 104 0 226" fill="none" stroke="#2e1606" stroke-width="4" opacity=".55"/><path d="M{x + 8} 322 q24 80 0 172" fill="none" stroke="#ffd7a0" stroke-width="2.5" opacity=".45"/>'
    b += '<ellipse cx="160" cy="415" rx="46" ry="115" fill="#d8935a" stroke="#1e0e04" stroke-width="6"/><ellipse cx="160" cy="415" rx="22" ry="64" fill="#8a5028" opacity=".8"/></g>'
    b += spark(900, 220, 24) + spark(120, 640, 16, '#fff6d6', .8)
    # bottom: water bath + boat
    d += lin('wat', [(0, '#7fe6f2'), (.5, '#2a9ab0'), (1, '#0c4a5a')]) + lin('bt2', [(0, '#c9d2de'), (1, '#4a5466')])
    b += '<path d="M40 1420 L1040 1360 L1060 1500 L20 1600 Z" fill="url(#wat)" stroke="#06232b" stroke-width="5"/>'
    b += ''.join(f'<path d="M{60 + kk * 110} {1540 - kk * 10} q40 -10 80 0" fill="none" stroke="#e6fbff" stroke-width="2.5" opacity=".45"/>' for kk in range(9))
    b += '<path d="M10 1600 L1060 1500 L1070 1620 L0 1730 Z" fill="url(#bt2)" stroke="#0a0d16" stroke-width="6"/><path d="M14 1612 L1060 1512" stroke="#fff" stroke-width="4" opacity=".6"/>'
    # specimen arm + resin block, just above the knife (right)
    b += '<rect x="852" y="1150" width="64" height="150" fill="#5a6476" stroke="#0a0d16" stroke-width="5"/><path d="M866 1155 V1295" stroke="#c9d2de" stroke-width="5" opacity=".7"/>'
    b += '<polygon points="820,1296 948,1296 920,1400 846,1400" fill="#e8a83a" fill-opacity=".9" stroke="#5a3608" stroke-width="5"/><path d="M836 1308 L860 1392" stroke="#fff3c8" stroke-width="4" opacity=".7"/>'
    # slices ribbon from the edge to the left
    for kk in range(10):
        t = kk / 9; x = 780 - t * 700; y = 1430 + t * 60 + math.sin(t * 6) * 8
        b += (f'<g transform="translate({x:.0f} {y:.0f}) skewX(-20)"><rect x="-34" y="-20" width="68" height="40" rx="4" fill="#ffd98a" fill-opacity="{.88 - t * .3:.2f}" stroke="#a8641a" stroke-width="2.5"/>'
              f'<ellipse cx="-6" cy="0" rx="14" ry="9" fill="#e88a5a" opacity=".6"/><circle cx="11" cy="-7" r="4" fill="#c05a3a" opacity=".6"/></g>')
    # frog on a slice raft
    gog = ('<path d="M-26 -66 h62" stroke="#1e1e1e" stroke-width="4"/><rect x="-24" y="-76" width="26" height="22" rx="9" fill="#9fe8ff" fill-opacity=".45" stroke-width="3"/>'
           '<rect x="9" y="-76" width="26" height="22" rx="9" fill="#9fe8ff" fill-opacity=".45" stroke-width="3"/>')
    b += '<g transform="translate(300 1480) skewX(-20)"><rect x="-90" y="-28" width="180" height="56" rx="6" fill="#ffd98a" stroke="#a8641a" stroke-width="3"/></g>'
    b += frog(300, 1490, 2.4, look=(8, -4), mouth='o', helmet=gog, armL='M-34 -22 q-24 -14 -26 -42', armR='M38 -22 q24 -14 26 -42')
    # diamond knife (hero glow)
    d += lin('dia2', [(0, '#ffffff'), (.35, '#c6f3ff'), (.7, '#58b8e0'), (1, '#1e5a80')], x2=1, y2=1)
    b += '<polygon points="790,1420 960,1380 1010,1540 830,1560" fill="url(#dia2)" stroke="#06283c" stroke-width="5"/>'
    b += '<path d="M790 1420 L960 1380" stroke="#ffffff" stroke-width="7"/><path d="M810 1460 L975 1430 M830 1500 L990 1475" stroke="#fff" stroke-width="2.5" opacity=".6"/>'
    b += '<circle cx="870" cy="1400" r="110" fill="#bff6ff" opacity=".35" filter="url(#blur30)"/>' + glint(870, 1400, 50, '#ffffff', 1)
    b += textshade(700, 1020, '#03080b', .5)
    return vpage('#08161d', vsvg(d, b), [(Y('2,000'), 190, 'w'), ('SLICES', 150, 'w'), ('= ONE HAIR', 120, 'w')], outline='#03080b', top=660)


# ============ 3: one-atom needle from the top down to a copper surface ============
def make_3():
    rnd = random.Random(33); d = SOFT + CU
    d += lin('bg3', [(0, '#160f2e'), (.6, '#0a0718'), (1, '#04030a')])
    b = f'<rect width="{W}" height="{H}" fill="url(#bg3)"/>' + starfield(rnd, 90, (0, 0, 1080, 1300), None, '#d8ccff', .35)
    tx, ty = 700, 1280
    # copper surface rows (bottom)
    for j in range(8):
        y = 1400 + j * (26 + j * 7); rr = 18 + j * 6; step = rr * 2.05; x = -60 + (j % 2) * rr
        while x < 1140:
            b += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{rr}" fill="url(#cuA)" stroke="#2a1004" stroke-width="{1.5 + j * .3:.1f}"/>'
            x += step
    b += f'<rect y="1800" width="{W}" height="200" fill="#04030a" opacity=".7" filter="url(#blur30)"/>'
    b += f'<ellipse cx="{tx}" cy="1408" rx="170" ry="34" fill="#9fe8ff" opacity=".5" filter="url(#blur12)"/>'
    for kk in range(5):
        x0 = tx - 40 + kk * 20
        b += f'<path d="M{x0} {ty + 26} l{(kk - 2) * 6} 24 l{-(kk - 2) * 4 + 8} 22 l{(kk - 2) * 5 - 6} 26 l2 20" fill="none" stroke="#bff6ff" stroke-width="3" opacity=".85"/>'
    # needle: wide at the top, tapering to one atom
    d += lin('nd3', [(0, '#202638'), (.3, '#7d89a2'), (.5, '#e8eef7'), (.75, '#55607a'), (1, '#1a1f30')], x2=1, y2=0)
    b += f'<polygon points="430,120 1010,120 {tx + 26},{ty - 40} {tx - 26},{ty - 40}" fill="url(#nd3)" stroke="#06080f" stroke-width="6"/>'
    b += f'<rect x="400" y="40" width="640" height="90" rx="14" fill="#3a4252" stroke="#06080f" stroke-width="6"/><path d="M420 64 H1020" stroke="#9aa6be" stroke-width="5" opacity=".6"/>'
    b += f'<path d="M600 140 L{tx - 8} {ty - 50}" stroke="#fff" stroke-width="5" opacity=".6"/>'
    for n, y in ((3, ty - 42), (2, ty - 20)):
        for kk in range(n):
            c = tx + (kk - (n - 1) / 2) * 22
            b += f'<circle cx="{c:.0f}" cy="{y:.0f}" r="11" fill="#9aa6be" stroke="#06080f" stroke-width="3"/><circle cx="{c - 3:.0f}" cy="{y - 4:.0f}" r="3.5" fill="#fff" opacity=".8"/>'
    d, ab = lf.atom_glow(d, 'tip3', tx, ty + 6, 18)
    b += ab + spark(tx + 110, ty - 50, 24) + spark(tx - 120, ty + 10, 16, '#bfe9ff', .9) + glint(780, 360, 26, '#fff', .8)
    # frog pushing one copper atom (left)
    ax, ay, ar = 250, 1500, 58
    b += f'<ellipse cx="{ax + 60}" cy="{ay + 62}" rx="170" ry="18" fill="#000" opacity=".5"/>'
    b += f'<circle cx="{ax}" cy="{ay}" r="{ar}" fill="url(#cuA)" stroke="#2a1004" stroke-width="5"/><circle cx="{ax - 16}" cy="{ay - 18}" r="12" fill="#fff6e0" opacity=".8"/>'
    hat = ('<path d="M-24 -80 q28 -30 58 0 z" fill="#f2b632" stroke-width="3"/><rect x="-28" y="-82" width="66" height="7" rx="3" fill="#e09a1c" stroke-width="2.5"/>'
           '<circle cx="-22" cy="-88" r="7" fill="#fff6d6" stroke-width="2.5"/>')
    b += frog(ax + 150, ay + 56, 2.5, flip=True, look=(-6, -2), mouth='o', helmet=hat, rot_=-8,
              armL='M-34 -24 q-6 -22 6 -40', armR='M38 -24 q-8 -14 -40 -12', feet=((-24, 4, -20), (24, 4, 10)))
    b += textshade(700, 1010, '#04030a', .6)
    return vpage('#0a0718', vsvg(d, b), [('IT ENDS IN', 116, 'w'), (Y('ONE'), 170, 'w'), (Y('ATOM'), 170, 'w')], outline='#04030a', top=690)


# ============ 4: Earth (top), text, porthole with the paint-fleck chip (bottom) ============
def make_4():
    rnd = random.Random(44); d = SOFT
    b = f'<rect width="{W}" height="{H}" fill="#03050c"/>' + starfield(rnd, 160, (0, 0, 1080, 1100), None, '#eef4ff', .6)
    d += rad('earth', 540, -760, 1240, [(0, '#3a8ad8', 1), (.85, '#1a4a8a', 1), (.97, '#6ad2ff', 1), (1, '#6ad2ff', 0)])
    b += '<circle cx="540" cy="-760" r="1240" fill="url(#earth)"/><circle cx="540" cy="-760" r="1252" fill="none" stroke="#9fe8ff" stroke-width="22" opacity=".35" filter="url(#blur12)"/>'
    b += ''.join(f'<ellipse cx="{rnd.randint(0, 1080)}" cy="{rnd.randint(120, 400)}" rx="{rnd.randint(60, 180)}" ry="{rnd.randint(14, 30)}" fill="#fff" opacity=".22"/>' for _ in range(10))
    # hull panel (bottom part)
    d += lin('hull', [(0, '#e8ecf2'), (.6, '#a8b2c0'), (1, '#4a5466')], x2=1, y2=1)
    b += '<path d="M-20 1120 Q540 1040 1100 1120 L1100 1940 L-20 1940 Z" fill="url(#hull)" stroke="#0a0d16" stroke-width="6"/>'
    b += '<path d="M-20 1130 Q540 1050 1100 1130" fill="none" stroke="#fff" stroke-width="5" opacity=".6"/>'
    b += ''.join(f'<circle cx="{x}" cy="{1150 - 60 * math.sin(math.pi * x / 1080):.0f}" r="5" fill="#6a7486"/>' for x in range(40, 1080, 60))
    cx, cy, r = 540, 1460, 290
    b += f'<circle cx="{cx + 10}" cy="{cy + 14}" r="{r + 58}" fill="#000" opacity=".35" filter="url(#blur12)"/>'
    d += lin('ring4', [(0, '#f4f6fa'), (.5, '#8a94a6'), (1, '#3a4252')], x2=1, y2=1)
    b += f'<circle cx="{cx}" cy="{cy}" r="{r + 54}" fill="url(#ring4)" stroke="#0a0d16" stroke-width="6"/>'
    b += ''.join(f'<circle cx="{cx + (r + 28) * math.cos(math.radians(a)):.0f}" cy="{cy + (r + 28) * math.sin(math.radians(a)):.0f}" r="9" fill="#5a6476" stroke="#0a0d16" stroke-width="3"/>' for a in range(0, 360, 30))
    d += f'<clipPath id="win"><circle cx="{cx}" cy="{cy}" r="{r}"/></clipPath>' + lin('cab', [(0, '#1c2a40'), (1, '#0a101c')])
    Wn = f'<rect x="{cx - r}" y="{cy - r}" width="{2 * r}" height="{2 * r}" fill="url(#cab)"/><circle cx="{cx}" cy="{cy - 140}" r="200" fill="#ffd98a" opacity=".18" filter="url(#blur30)"/>'
    bub = ('<circle cx="6" cy="-46" r="60" fill="#bfe9ff" fill-opacity=".18" stroke="#e6f7ff" stroke-width="4"/>'
           '<path d="M-30 -78 q14 -18 34 -22" fill="none" stroke="#fff" stroke-width="5" opacity=".8"/>')
    suit = '<path d="M-40 4 q-4 -30 6 -40 h70 q12 10 6 40 z" fill="#f4f6fa" stroke-width="3.5"/><rect x="-8" y="-22" width="26" height="16" rx="4" fill="#e2412c" stroke-width="2.5"/>'
    Wn += frog(cx - 30, cy + 250, 2.9, look=(6, -8), mouth='o', back=suit, helmet=bub, armL='M-34 -22 q-30 -16 -34 -60', armR='M38 -22 q30 -16 34 -60', nofeet=True)
    b += f'<g clip-path="url(#win)">{Wn}</g><circle cx="{cx}" cy="{cy}" r="{r}" fill="#9fd8ff" opacity=".08"/>'
    b += f'<path d="M{cx - 200} {cy - 110} Q{cx - 120} {cy - 230} {cx + 20} {cy - 260}" fill="none" stroke="#fff" stroke-width="14" opacity=".35"/>'
    b += f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="#0a0d16" stroke-width="8"/>'
    ix, iy = cx + 120, cy - 150
    for kk in range(9):
        a = math.radians(kk * 40 + rnd.uniform(-12, 12)); L = rnd.uniform(70, 150)
        mx, my = ix + L * .5 * math.cos(a) + rnd.uniform(-10, 10), iy + L * .5 * math.sin(a) + rnd.uniform(-10, 10)
        b += f'<path d="M{ix} {iy} L{mx:.0f} {my:.0f} L{ix + L * math.cos(a):.0f} {iy + L * math.sin(a):.0f}" fill="none" stroke="#fff" stroke-width="3" opacity=".9"/>'
    for rr in (40, 80):
        b += f'<circle cx="{ix}" cy="{iy}" r="{rr}" fill="none" stroke="#fff" stroke-width="2" stroke-dasharray="18 14" opacity=".6"/>'
    b += f'<circle cx="{ix}" cy="{iy}" r="18" fill="#fff" opacity=".9"/><circle cx="{ix}" cy="{iy}" r="70" fill="#fff2c8" opacity=".5" filter="url(#blur12)"/>'
    d += ('<linearGradient id="trl4" x1="1" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ff8a3a" stop-opacity="0"/>'
          '<stop offset=".8" stop-color="#ffb35a" stop-opacity=".85"/><stop offset="1" stop-color="#fff6d6" stop-opacity="1"/></linearGradient>')
    fx, fy = ix + 50, iy - 40
    b += f'<polygon points="1100,1080 {fx + 8},{fy - 12} {fx - 6},{fy + 12} 1100,1130" fill="url(#trl4)"/><path d="M1100 1100 L{fx} {fy}" stroke="#fff2c8" stroke-width="3" opacity=".8"/>'
    b += f'<g transform="translate({fx} {fy}) rotate(-40)"><rect x="-18" y="-10" width="36" height="20" rx="3" fill="#fff" stroke="#e2412c" stroke-width="4"/></g>'
    b += glint(ix, iy, 46, '#fff', 1) + spark(940, 560, 18, '#fff6d6', .8) + spark(120, 1000, 14, '#fff6d6', .7)
    b += textshade(560, 1000, '#02030a', .55)
    return vpage('#03050c', vsvg(d, b), [('A FLECK OF', 120, 'w'), (Y('PAINT'), 200, 'w'), ('VS. A WINDOW', 104, 'w')], outline='#02030a', top=600)


# ============ 5: countryside (top), text, collider ring with the collision burst (bottom) ============
def make_5():
    rnd = random.Random(55); d = SOFT
    d += lin('sky5', [(0, '#120c2a'), (.7, '#3a2456'), (1, '#c8644a')]) + lin('rock', [(0, '#3a2a1e'), (.3, '#1e1610'), (1, '#07050a')])
    b = '<rect width="1080" height="480" fill="url(#sky5)"/>' + starfield(rnd, 60, (0, 30, 1080, 330), None, '#fff', .5)
    b += '<path d="M0 430 Q270 380 540 420 T1080 400 V500 H0 Z" fill="#2e4a26"/><path d="M0 460 Q300 430 600 456 T1080 440 V520 H0Z" fill="#243e1e"/>'
    b += ''.join(f'<g transform="translate({x} {y})"><rect x="-4" y="-6" width="8" height="18" fill="#3a2614"/><circle cx="0" cy="-16" r="16" fill="#3e6e2a"/></g>' for x, y in ((140, 412), (190, 410), (820, 404), (870, 408)))
    b += '<g transform="translate(560 410)"><rect x="-26" y="-20" width="52" height="30" fill="#f2e6cc" stroke="#3a2614" stroke-width="3"/><path d="M-32 -18 L0 -42 L32 -18 Z" fill="#b8301e" stroke="#3a2614" stroke-width="3"/></g>'
    b += '<rect y="490" width="1080" height="1430" fill="url(#rock)"/><path d="M0 490 H1080" stroke="#1a120a" stroke-width="6"/>'
    b += ''.join(f'<path d="M0 {y} Q270 {y - 14} 540 {y} T1080 {y}" fill="none" stroke="#5a4232" stroke-width="3" opacity=".35"/>' for y in (560, 640, 1180, 1760))
    cx, cy, rx, ry = 540, 1440, 450, 190
    b += f'<ellipse cx="{cx}" cy="{cy}" rx="{rx + 40}" ry="{ry + 40}" fill="#3a8aff" opacity=".22" filter="url(#blur30)"/>'
    b += f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="none" stroke="#06101e" stroke-width="72"/>'
    b += f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="none" stroke="#1e5ab8" stroke-width="60"/>'
    b += f'<ellipse cx="{cx}" cy="{cy - 14}" rx="{rx}" ry="{ry}" fill="none" stroke="#6ab4ff" stroke-width="12" opacity=".8"/>'
    b += ''.join(f'<path d="M{cx + rx * math.cos(math.radians(a)):.0f} {cy + ry * math.sin(math.radians(a)) - 28:.0f} v56" stroke="#06101e" stroke-width="4" opacity=".7"/>' for a in range(0, 360, 15))
    b += f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="none" stroke="#bff6ff" stroke-width="6" opacity=".9"/>'

    def comet(a0, a1, col):
        out = ''
        for kk in range(18):
            a = math.radians(a0 + (a1 - a0) * kk / 17)
            out += f'<circle cx="{cx + rx * math.cos(a):.0f}" cy="{cy + ry * math.sin(a):.0f}" r="{4 + 15 * kk / 18:.1f}" fill="{col}" opacity="{.08 + .7 * kk / 18:.2f}"/>'
        return out
    b += comet(170, 102, '#ff6a5a') + comet(10, 78, '#6ad2ff')
    bx, by = cx, cy + ry
    b += f'<circle cx="{bx}" cy="{by}" r="200" fill="#fff2c8" opacity=".35" filter="url(#blur30)"/>'
    for kk in range(12):
        a = math.radians(-170 + kk * 30 + rnd.uniform(-8, 8)); L = rnd.uniform(110, 200); s = rnd.choice([-1, 1])
        ex, ey = bx + L * math.cos(a), by + L * math.sin(a) * .8
        b += f'<path d="M{bx} {by} Q{bx + L * .6 * math.cos(a + s * .6):.0f} {by + L * .6 * math.sin(a + s * .6) * .8:.0f} {ex:.0f} {ey:.0f}" fill="none" stroke="{rnd.choice(["#F2D27A", "#9fe8ff", "#ff9a8a", "#ffffff"])}" stroke-width="4" opacity=".9"/>'
    b += glint(bx, by, 64, '#fff', 1)
    hat = '<path d="M-24 -80 q28 -30 58 0 z" fill="#f2b632" stroke-width="3"/><rect x="-28" y="-82" width="66" height="7" rx="3" fill="#e09a1c" stroke-width="2.5"/>'
    vest = '<path d="M-30 -4 q-2 -24 8 -34 l10 30 z M40 -4 q2 -24 -8 -34 l-10 30 z" fill="#ff7a1a" stroke-width="3"/>'
    fa = math.radians(215); fx, fy = cx + rx * math.cos(fa), cy + ry * math.sin(fa) - 26
    b += frog(fx, fy, 2.5, look=(6, 2), mouth='o', helmet=hat, front=vest, rot_=-6, armL='M-34 -22 q-10 14 -4 30', armR='M38 -22 q24 -16 30 -46')
    b += spark(900, 1220, 20, '#bff6ff') + spark(150, 1180, 14, '#fff6d6', .8)
    b += textshade(700, 1080, '#07050a', .5)
    return vpage('#07050a', vsvg(d, b), [(Y('99.9999991%'), 128, 'w'), ('OF LIGHT', 130, 'w'), ('SPEED', 130, 'w')], outline='#07050a', top=720)


if __name__ == '__main__':
    V = os.path.dirname(HERE)
    for n, f in enumerate((make_1, make_2, make_3, make_4, make_5), 1):
        out = os.path.join(V + f'-short{n}', 'thumb'); os.makedirs(out, exist_ok=True)
        for c in ('common.css', 'Fredoka-700.woff2'): shutil.copy(os.path.join(TOOLS, 'assets', 'thumb_v', c), out)
        open(os.path.join(out, 'A.html'), 'w').write(f())
        print('wrote short', n)
