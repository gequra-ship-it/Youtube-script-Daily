# Shorts thumbnails (guideline 16-9, miya 2026-11-06): ONE per short -> videos/sharpest-blade-fastest-gun-shortN/thumb/A.html
# Reuses frog/glint/spark helpers from make.py (long form). Each = the single key scene of that short's script:
# 1 knife edge under the microscope = jagged mountains ("sharpness is an illusion", S02)
# 2 diamond knife ribbon on the water bath + a hair ("two thousand slices ... a single strand of hair", S06)
# 3 single-atom needle over a copper surface, frog nudging an atom (S01-S03)
# 4 paint fleck chipping a spacecraft window (S03)
# 5 LHC ring under the countryside, protons at 99.9999991% of light speed (S02, S05)
import os, sys, math, random, shutil, importlib.util
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', '..', 'tools'))
from thumb_lib import page, svg, lin, rad, spark
spec = importlib.util.spec_from_file_location('lf', os.path.join(HERE, 'make.py')); lf = importlib.util.module_from_spec(spec); spec.loader.exec_module(lf)
frog, glint, SOFT, INK, corner, starfield, speed_lines = lf.frog, lf.glint, lf.SOFT, lf.INK, lf.corner, lf.starfield, lf.speed_lines
Y = lambda w: f'<span class="g">{w}</span>'


# ============ 1: kitchen knife + magnifier showing a jagged mountain range ============
def make_1():
    rnd = random.Random(11); d = SOFT
    d += lin('bg1', [(0, '#2a2236'), (.6, '#141020'), (1, '#07060c')])
    d += rad('lamp1', 1500, 120, 900, [(0, '#ffe7b8', .35), (.5, '#ffb76a', .08), (1, '#ffb76a', 0)])
    b = '<rect width="1920" height="1080" fill="url(#bg1)"/><rect width="1920" height="1080" fill="url(#lamp1)"/>'
    # counter top
    d += lin('ctr', [(0, '#4a3826'), (1, '#1a120a')])
    b += '<polygon points="0,840 1920,800 1920,1080 0,1080" fill="url(#ctr)"/><path d="M0 840 L1920 800" stroke="#c99a5a" stroke-width="4" opacity=".6"/>'
    # knife, edge on top, tip right; lies on the counter
    d += lin('k1', [(0, '#f4f7fb'), (.25, '#d0d8e4'), (.7, '#8d98aa'), (1, '#5a6476')])
    b += '<ellipse cx="760" cy="860" rx="720" ry="26" fill="#000" opacity=".45" filter="url(#blur12)"/>'
    b += '<rect x="40" y="752" width="380" height="96" rx="40" fill="#2b1a12" stroke="#0c0604" stroke-width="6"/>'
    b += ''.join(f'<circle cx="{x}" cy="800" r="12" fill="#d8dee8" stroke="#0c0604" stroke-width="3"/>' for x in (130, 230, 330))
    b += '<path d="M90 768 H380" stroke="#6a4430" stroke-width="5" opacity=".7"/>'
    b += '<rect x="410" y="730" width="44" height="130" rx="10" fill="#aab4c4" stroke="#0c0604" stroke-width="6"/>'
    blade = 'M454 846 L1300 846 Q1420 840 1500 800 Q1240 680 900 652 Q640 640 454 650 Z'
    b += f'<path d="{blade}" fill="url(#k1)" stroke="#0c0604" stroke-width="6"/>'
    b += '<path d="M470 662 Q660 652 900 664 Q1230 690 1488 798" fill="none" stroke="#ffffff" stroke-width="5"/>'
    b += '<path d="M470 690 Q800 690 1100 720" fill="none" stroke="#ffffff" stroke-width="3" opacity=".45"/>'
    b += glint(1180, 700, 30, '#ffffff', .95) + glint(700, 654, 18, '#fff6e0', .7)
    # magnifier: lens centred above the edge, handle to the top right
    cx, cy, r = 1230, 410, 300
    tx, ty = 1050, 676   # spot on the edge being viewed
    b += f'<path d="M{cx - r * .55:.0f} {cy + r * .83:.0f} L{tx - 30} {ty - 6} M{cx + r * .55:.0f} {cy + r * .83:.0f} L{tx + 30} {ty - 6}" stroke="#bfe9ff" stroke-width="4" stroke-dasharray="14 10" opacity=".7"/>'
    b += f'<circle cx="{tx}" cy="{ty}" r="34" fill="none" stroke="#bfe9ff" stroke-width="5" opacity=".9"/>'
    b += f'<path d="M{cx + r * .7:.0f} {cy - r * .7:.0f} L{cx + r * 1.32:.0f} {cy - r * 1.32:.0f}" stroke="#0c0604" stroke-width="64" stroke-linecap="round"/>'
    b += f'<path d="M{cx + r * .72:.0f} {cy - r * .72:.0f} L{cx + r * 1.3:.0f} {cy - r * 1.3:.0f}" stroke="#7a2e1e" stroke-width="50" stroke-linecap="round"/>'
    b += f'<path d="M{cx + r * .76:.0f} {cy - r * .82:.0f} L{cx + r * 1.26:.0f} {cy - r * 1.36:.0f}" stroke="#c0604a" stroke-width="10" stroke-linecap="round"/>'
    d += f'<clipPath id="lens"><circle cx="{cx}" cy="{cy}" r="{r}"/></clipPath>'
    d += lin('sem', [(0, '#0a1420'), (1, '#1a2c3a')])
    d += lin('mtn', [(0, '#e8f2f8'), (.35, '#9fb4c4'), (1, '#2c3c4a')])
    L = f'<rect x="{cx - r}" y="{cy - r}" width="{2 * r}" height="{2 * r}" fill="url(#sem)"/>'
    # back ridge + front jagged ridge (the edge), electron-microscope grey-blue
    def ridge(base, amp, n, seed):
        rr = random.Random(seed); pts = [(cx - r - 20, base + 200)]; x = cx - r - 20
        while x < cx + r + 40:
            pts.append((x, base - rr.uniform(.3, 1) * amp)); x += rr.uniform(26, 70)
            pts.append((x, base + rr.uniform(-.1, .35) * amp)); x += rr.uniform(16, 50)
        pts.append((cx + r + 40, base + 200))
        return ' '.join(f'{p[0]:.0f},{p[1]:.0f}' for p in pts), pts
    p2, _ = ridge(cy + 30, 120, 0, 3)
    L += f'<polygon points="{p2}" fill="#3e5262" opacity=".8"/>'
    p1, pts = ridge(cy + 150, 230, 0, 7)
    L += f'<polygon points="{p1}" fill="url(#mtn)" stroke="#0a141c" stroke-width="4"/>'
    for (x0, y0), (x1, y1) in zip(pts[1:-2:2], pts[2:-1:2]):   # lit faces
        L += f'<path d="M{x0:.0f} {y0:.0f} L{x1:.0f} {y1:.0f}" stroke="#ffffff" stroke-width="3" opacity=".7"/>'
    L += ''.join(f'<path d="M{cx - r + k * 46} {cy + 160 + (k % 3) * 18} l60 -8" stroke="#0a141c" stroke-width="2" opacity=".35"/>' for k in range(12))
    # frog climbing the tallest peak, climber helmet
    peak = min(pts[3:-3], key=lambda p: p[1] if abs(p[0] - cx - 40) < 160 else 9e9)
    helm = ('<path d="M-26 -78 q30 -34 62 0 z" fill="#e2412c" stroke-width="3"/><rect x="-28" y="-80" width="66" height="7" rx="3" fill="#b8301e" stroke-width="2.5"/>'
            '<circle cx="5" cy="-92" r="5" fill="#fff6d6" stroke-width="2"/>')
    L += frog(peak[0], peak[1] + 6, 2.2, look=(-4, 5), mouth='o', helmet=helm,
              armL='M-34 -22 q-24 -16 -22 -46', armR='M38 -22 q18 4 22 26', feet=((-22, 4, -14), (22, 4, 14)))
    b += f'<circle cx="{cx}" cy="{cy}" r="{r + 30}" fill="#bfe9ff" opacity=".15" filter="url(#blur30)"/>'
    b += f'<g clip-path="url(#lens)">{L}<ellipse cx="{cx - 90}" cy="{cy - 150}" rx="150" ry="60" transform="rotate(-30 {cx - 90} {cy - 150})" fill="#fff" opacity=".18"/></g>'
    b += f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="#0c0604" stroke-width="40"/><circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="#c7ced8" stroke-width="26"/>'
    b += f'<circle cx="{cx}" cy="{cy}" r="{r - 6}" fill="none" stroke="#ffffff" stroke-width="4" opacity=".7"/>'
    b += spark(cx - 200, cy - 210, 26) + spark(1560, 180, 18, '#fff6d6', .8) + spark(860, 560, 14, '#fff6d6', .7)
    return page('#141020', svg(d, b), [('SHARPNESS', 150, 'w'), ('IS AN', 104, 'w'), (Y('ILLUSION'), 160, 'w')], outline='#07060c', top=36)


# ============ 2: diamond knife, ribbon of slices on the water bath, a giant hair ============
def make_2():
    rnd = random.Random(22); d = SOFT
    d += lin('bg2', [(0, '#0e2a33'), (.55, '#08161d'), (1, '#03080b')])
    b = '<rect width="1920" height="1080" fill="url(#bg2)"/>'
    d += rad('l2', 1180, 560, 760, [(0, '#bff6ff', .35), (.4, '#5ad2e8', .1), (1, '#5ad2e8', 0)])
    b += '<rect width="1920" height="1080" fill="url(#l2)"/>'
    # giant hair strand behind, diagonal (scale)
    d += lin('hair', [(0, '#7a4a26'), (.35, '#c08048'), (.55, '#e0a56a'), (.8, '#6a3a1a'), (1, '#3a1e0c')], x2=0, y2=1)
    b += '<g transform="rotate(-14 1200 330)"><rect x="560" y="210" width="1500" height="200" rx="0" fill="url(#hair)" stroke="#1e0e04" stroke-width="6"/>'
    for k in range(14):
        x = 600 + k * 105
        b += f'<path d="M{x} 212 q30 90 0 196" fill="none" stroke="#2e1606" stroke-width="4" opacity=".55"/><path d="M{x + 8} 230 q22 70 0 150" fill="none" stroke="#ffd7a0" stroke-width="2.5" opacity=".45"/>'
    b += '<ellipse cx="560" cy="310" rx="40" ry="100" fill="#d8935a" stroke="#1e0e04" stroke-width="6"/><ellipse cx="560" cy="310" rx="20" ry="56" fill="#8a5028" opacity=".8"/></g>'
    # water bath (trough) behind the knife edge
    d += lin('wat', [(0, '#7fe6f2'), (.5, '#2a9ab0'), (1, '#0c4a5a')])
    b += '<path d="M180 690 L1480 640 L1520 760 L120 860 Z" fill="url(#wat)" stroke="#06232b" stroke-width="5" opacity=".95"/>'
    b += ''.join(f'<path d="M{200 + k * 120} {800 - k * 8} q40 -10 80 0" fill="none" stroke="#e6fbff" stroke-width="2.5" opacity=".45"/>' for k in range(10))
    # metal boat
    d += lin('bt2', [(0, '#c9d2de'), (1, '#4a5466')])
    b += '<path d="M100 860 L1530 760 L1560 860 L90 980 Z" fill="url(#bt2)" stroke="#0a0d16" stroke-width="6"/>'
    b += '<path d="M110 872 L1530 772" stroke="#ffffff" stroke-width="4" opacity=".6"/>'
    # ribbon of slices floating from the edge (right) to the left
    for k in range(13):
        t = k / 12; x = 1300 - t * 1080; y = 680 + t * 70 + math.sin(t * 7) * 10
        w, h = 74, 44
        b += (f'<g transform="translate({x:.0f} {y:.0f}) skewX(-20)"><rect x="{-w / 2}" y="{-h / 2}" width="{w}" height="{h}" rx="4" fill="#ffd98a" fill-opacity="{.85 - t * .3:.2f}" stroke="#a8641a" stroke-width="2.5"/>'
              f'<ellipse cx="-6" cy="0" rx="16" ry="10" fill="#e88a5a" opacity=".6"/><circle cx="12" cy="-8" r="4" fill="#c05a3a" opacity=".6"/></g>')
    # frog riding a slice like a raft (diving goggles)
    gog = ('<path d="M-26 -66 h62" stroke="#1e1e1e" stroke-width="4"/><rect x="-24" y="-76" width="26" height="22" rx="9" fill="#9fe8ff" fill-opacity=".45" stroke-width="3"/>'
           '<rect x="9" y="-76" width="26" height="22" rx="9" fill="#9fe8ff" fill-opacity=".45" stroke-width="3"/>')
    b += '<g transform="translate(560 730) skewX(-20)"><rect x="-90" y="-30" width="180" height="60" rx="6" fill="#ffd98a" stroke="#a8641a" stroke-width="3"/></g>'
    b += frog(560, 742, 2.3, look=(6, -4), mouth='o', helmet=gog, armL='M-34 -22 q-24 -14 -26 -42', armR='M38 -22 q24 -14 26 -42')
    # diamond knife edge, glowing, at the right end of the water
    d += lin('dia2', [(0, '#ffffff'), (.35, '#c6f3ff'), (.7, '#58b8e0'), (1, '#1e5a80')], x2=1, y2=1)
    b += '<polygon points="1340,660 1500,620 1560,780 1380,800" fill="url(#dia2)" stroke="#06283c" stroke-width="5"/>'
    b += '<path d="M1340 660 L1500 620" stroke="#ffffff" stroke-width="7"/><path d="M1360 700 L1520 670 M1380 740 L1540 720" stroke="#ffffff" stroke-width="2.5" opacity=".6"/>'
    b += '<circle cx="1420" cy="640" r="90" fill="#bff6ff" opacity=".35" filter="url(#blur30)"/>' + glint(1420, 640, 46, '#ffffff', 1)
    # specimen arm coming down from the top onto the edge, resin block
    b += '<rect x="1430" y="-20" width="70" height="440" fill="#5a6476" stroke="#0a0d16" stroke-width="5"/><path d="M1444 0 V410" stroke="#c9d2de" stroke-width="5" opacity=".7"/>'
    b += '<polygon points="1400,420 1530,420 1500,560 1430,560" fill="#e8a83a" fill-opacity=".9" stroke="#5a3608" stroke-width="5"/><path d="M1415 432 L1440 550" stroke="#fff3c8" stroke-width="4" opacity=".7"/>'
    b += '<path d="M1360 520 l-40 -14 M1360 560 l-50 0 M1360 600 l-40 14" stroke="#fff" stroke-width="5" stroke-linecap="round" opacity=".8"/>'
    b += starfield(rnd, 40, (900, 20, 1900, 600), None, '#bff6ff', .4) + spark(1650, 520, 22) + spark(1100, 600, 16, '#e6fbff', .8)
    return page('#08161d', svg(d, b), [(Y('2,000') + ' SLICES', 150, 'w'), ('= ONE HAIR', 132, 'w')], outline='#03080b', top=40)


# ============ 3: one-atom needle over a copper surface ============
def make_3():
    rnd = random.Random(33); d = SOFT
    d += lin('bg3', [(0, '#160f2e'), (.6, '#0a0718'), (1, '#04030a')])
    b = '<rect width="1920" height="1080" fill="url(#bg3)"/>' + starfield(rnd, 70, (0, 0, 1920, 700), corner, '#d8ccff', .35)
    # copper atom surface in perspective (rows)
    d += ('<radialGradient id="cuA" cx=".5" cy=".5" r=".55" fx=".35" fy=".3"><stop offset="0" stop-color="#ffe2b8"/>'
          '<stop offset=".45" stop-color="#e08a48"/><stop offset="1" stop-color="#6a2e10"/></radialGradient>')
    rows = []
    for j in range(9):
        y = 700 + j * (24 + j * 7); rr = 16 + j * 6; step = rr * 2.05
        off = (j % 2) * rr
        x = -60 + off
        while x < 1980:
            dk = max(0, (x - 1250) / 400) * max(0, (y - 740) / 160)   # fade into the bottom-right corner
            rows.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{rr}" fill="url(#cuA)" stroke="#2a1004" stroke-width="{1.5 + j * .3:.1f}" opacity="{max(.18, 1 - dk * 1.6):.2f}"/>')
            x += step
    b += ''.join(rows)
    b += '<rect x="1500" y="800" width="420" height="280" fill="#04030a" opacity=".55" filter="url(#blur30)"/>'
    # tunnelling glow under the tip
    tx, ty = 1180, 600
    b += f'<ellipse cx="{tx}" cy="736" rx="170" ry="34" fill="#9fe8ff" opacity=".45" filter="url(#blur12)"/>'
    for k in range(5):
        x0 = tx - 40 + k * 20
        b += f'<path d="M{x0} {ty + 24} l{(k - 2) * 6} 24 l{-(k - 2) * 4 + 8} 22 l{(k - 2) * 5 - 6} 26 l2 20" fill="none" stroke="#bff6ff" stroke-width="3" opacity=".85"/>'
    # needle from top right
    d += lin('nd3', [(0, '#202638'), (.3, '#7d89a2'), (.5, '#e8eef7'), (.75, '#55607a'), (1, '#1a1f30')], x2=1, y2=0)
    b += f'<polygon points="1010,-20 1350,-20 {tx + 26},{ty - 40} {tx - 26},{ty - 40}" fill="url(#nd3)" stroke="#06080f" stroke-width="6"/>'
    b += f'<path d="M1120 0 L{tx - 8} {ty - 50}" stroke="#fff" stroke-width="5" opacity=".6"/>'
    for n, y in ((3, ty - 42), (2, ty - 20)):
        for k in range(n):
            cx_ = tx + (k - (n - 1) / 2) * 22
            b += f'<circle cx="{cx_:.0f}" cy="{y:.0f}" r="11" fill="#9aa6be" stroke="#06080f" stroke-width="3"/><circle cx="{cx_ - 3:.0f}" cy="{y - 4:.0f}" r="3.5" fill="#fff" opacity=".8"/>'
    d, ab = lf.atom_glow(d, 'tip3', tx, ty + 6, 16)
    b += ab + spark(tx + 90, ty - 40, 22) + spark(tx - 110, ty + 10, 14, '#bfe9ff', .9)
    b += glint(1150, 200, 24, '#ffffff', .8)
    # frog on the surface pushing one copper atom like a boulder (miner hat with lamp)
    ax, ay, ar = 660, 820, 54
    b += f'<ellipse cx="{ax + 60}" cy="{ay + 58}" rx="170" ry="18" fill="#000" opacity=".5"/>'
    b += f'<circle cx="{ax}" cy="{ay}" r="{ar}" fill="url(#cuA)" stroke="#2a1004" stroke-width="5"/><circle cx="{ax - 16}" cy="{ay - 18}" r="12" fill="#fff6e0" opacity=".8"/>'
    b += f'<path d="M{ax - 120} {ay + 20} h-60 M{ax - 120} {ay - 6} h-90 M{ax - 120} {ay + 44} h-40" stroke="#ffd2a0" stroke-width="5" stroke-linecap="round" opacity=".6"/>'
    hat = ('<path d="M-24 -80 q28 -30 58 0 z" fill="#f2b632" stroke-width="3"/><rect x="-28" y="-82" width="66" height="7" rx="3" fill="#e09a1c" stroke-width="2.5"/>'
           '<circle cx="-22" cy="-88" r="7" fill="#fff6d6" stroke-width="2.5"/>')
    b += frog(ax + 150, ay + 52, 2.5, flip=True, look=(-6, -2), mouth='o', helmet=hat, rot_=-8,
              armL='M-34 -24 q-6 -22 6 -40', armR='M38 -24 q-8 -14 -40 -12', feet=((-24, 4, -20), (24, 4, 10)))
    return page('#0a0718', svg(d, b), [('IT ENDS IN', 112, 'w'), (Y('ONE ATOM'), 168, 'w')], outline='#04030a', top=48)


# ============ 4: paint fleck chipping a spacecraft window ============
def make_4():
    rnd = random.Random(44); d = SOFT
    b = '<rect width="1920" height="1080" fill="#03050c"/>' + starfield(rnd, 160, (0, 0, 1920, 1080), corner, '#eef4ff', .6)
    # Earth limb bottom-left
    d += rad('earth', 380, 1700, 1100, [(0, '#3a8ad8', 1), (.85, '#1a4a8a', 1), (.97, '#6ad2ff', 1), (1, '#6ad2ff', 0)])
    b += '<circle cx="380" cy="1700" r="1100" fill="url(#earth)"/>'
    b += '<circle cx="380" cy="1700" r="1112" fill="none" stroke="#9fe8ff" stroke-width="22" opacity=".35" filter="url(#blur12)"/>'
    b += ''.join(f'<ellipse cx="{rnd.randint(-100, 1100)}" cy="{rnd.randint(700, 1080)}" rx="{rnd.randint(60, 180)}" ry="{rnd.randint(14, 30)}" fill="#ffffff" opacity=".22"/>' for _ in range(10))
    # hull panel (right)
    d += lin('hull', [(0, '#e8ecf2'), (.6, '#a8b2c0'), (1, '#4a5466')], x2=1, y2=1)
    hull = 'M820 -20 Q760 540 900 1100 L1920 1100 L1920 -20 Z'
    b += f'<path d="{hull}" fill="url(#hull)" stroke="#0a0d16" stroke-width="6"/>'
    b += '<path d="M830 -20 Q770 540 910 1100" fill="none" stroke="#ffffff" stroke-width="5" opacity=".6"/>'
    for y in (140, 960):
        b += f'<path d="M{850 if y < 500 else 880} {y} H1920" stroke="#6a7486" stroke-width="3" opacity=".6"/>'
    b += ''.join(f'<circle cx="{x}" cy="{y}" r="5" fill="#6a7486"/>' for x in range(920, 1520, 60) for y in (120, 160))
    # porthole
    cx, cy, r = 1260, 540, 300
    b += f'<circle cx="{cx + 10}" cy="{cy + 14}" r="{r + 58}" fill="#000" opacity=".35" filter="url(#blur12)"/>'
    d += lin('ring4', [(0, '#f4f6fa'), (.5, '#8a94a6'), (1, '#3a4252')], x2=1, y2=1)
    b += f'<circle cx="{cx}" cy="{cy}" r="{r + 56}" fill="url(#ring4)" stroke="#0a0d16" stroke-width="6"/>'
    b += ''.join(f'<circle cx="{cx + (r + 30) * math.cos(math.radians(a)):.0f}" cy="{cy + (r + 30) * math.sin(math.radians(a)):.0f}" r="9" fill="#5a6476" stroke="#0a0d16" stroke-width="3"/>' for a in range(0, 360, 30))
    d += f'<clipPath id="win"><circle cx="{cx}" cy="{cy}" r="{r}"/></clipPath>'
    d += lin('cab', [(0, '#1c2a40'), (1, '#0a101c')])
    W = f'<rect x="{cx - r}" y="{cy - r}" width="{2 * r}" height="{2 * r}" fill="url(#cab)"/>'
    W += f'<circle cx="{cx}" cy="{cy - 140}" r="200" fill="#ffd98a" opacity=".18" filter="url(#blur30)"/>'
    # frog inside in a space helmet, hands on the glass
    bub = ('<circle cx="6" cy="-46" r="60" fill="#bfe9ff" fill-opacity=".18" stroke="#e6f7ff" stroke-width="4"/>'
           '<path d="M-30 -78 q14 -18 34 -22" fill="none" stroke="#ffffff" stroke-width="5" opacity=".8"/>')
    suit = '<path d="M-40 4 q-4 -30 6 -40 h70 q12 10 6 40 z" fill="#f4f6fa" stroke-width="3.5"/><rect x="-8" y="-22" width="26" height="16" rx="4" fill="#e2412c" stroke-width="2.5"/>'
    W += frog(cx + 20, cy + 250, 3.0, look=(-6, -8), mouth='o', back=suit, helmet=bub,
              armL='M-34 -22 q-30 -16 -34 -60', armR='M38 -22 q30 -16 34 -60', nofeet=True)
    b += f'<g clip-path="url(#win)">{W}</g>'
    b += f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="#9fd8ff" opacity=".08"/>'
    b += f'<path d="M{cx - 200} {cy - 120} Q{cx - 120} {cy - 240} {cx + 20} {cy - 270}" fill="none" stroke="#ffffff" stroke-width="14" opacity=".35"/>'
    b += f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="#0a0d16" stroke-width="8"/>'
    # impact chip with star cracks (upper right of the glass)
    ix, iy = cx + 120, cy - 170
    for k in range(9):
        a = math.radians(k * 40 + rnd.uniform(-12, 12)); L = rnd.uniform(70, 150)
        mx, my = ix + L * .5 * math.cos(a) + rnd.uniform(-10, 10), iy + L * .5 * math.sin(a) + rnd.uniform(-10, 10)
        b += f'<path d="M{ix} {iy} L{mx:.0f} {my:.0f} L{ix + L * math.cos(a):.0f} {iy + L * math.sin(a):.0f}" fill="none" stroke="#ffffff" stroke-width="3" opacity=".9"/>'
    for rr in (40, 80):
        b += f'<circle cx="{ix}" cy="{iy}" r="{rr}" fill="none" stroke="#ffffff" stroke-width="2" stroke-dasharray="18 14" opacity=".6"/>'
    b += f'<circle cx="{ix}" cy="{iy}" r="18" fill="#ffffff" opacity=".9"/><circle cx="{ix}" cy="{iy}" r="70" fill="#fff2c8" opacity=".5" filter="url(#blur12)"/>'
    # the paint fleck streaking in from the top right, glowing hot
    d += ('<linearGradient id="trl4" x1="1" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ff8a3a" stop-opacity="0"/>'
          '<stop offset=".8" stop-color="#ffb35a" stop-opacity=".8"/><stop offset="1" stop-color="#fff6d6" stop-opacity="1"/></linearGradient>')
    fx, fy = ix + 50, iy - 44
    b += f'<polygon points="1930,-60 {fx + 6},{fy - 12} {fx - 6},{fy + 12} 1910,-20" fill="url(#trl4)"/>'
    b += f'<path d="M1900 -40 L{fx} {fy}" stroke="#fff2c8" stroke-width="3" opacity=".8"/>'
    b += f'<g transform="translate({fx} {fy}) rotate(-38)"><rect x="-16" y="-9" width="32" height="18" rx="3" fill="#ffffff" stroke="#e2412c" stroke-width="4"/></g>'
    b += glint(ix, iy, 44, '#ffffff', 1) + spark(1700, 90, 18, '#fff6d6', .8)
    return page('#03050c', svg(d, b), [('A FLECK OF', 120, 'w'), (Y('PAINT'), 190, 'w'), ('VS. A WINDOW', 104, 'w')], outline='#02030a', top=36)


# ============ 5: LHC ring under the countryside, protons on the ring ============
def make_5():
    rnd = random.Random(55); d = SOFT
    d += lin('sky5', [(0, '#120c2a'), (.7, '#3a2456'), (1, '#c8644a')])
    d += lin('rock', [(0, '#3a2a1e'), (.3, '#1e1610'), (1, '#07050a')])
    b = '<rect width="1920" height="230" fill="url(#sky5)"/>' + starfield(rnd, 50, (900, 10, 1900, 140), None, '#fff', .5)
    b += '<path d="M0 200 Q300 150 600 190 T1200 180 T1920 170 V260 H0 Z" fill="#2e4a26"/><path d="M0 230 Q500 200 1000 226 T1920 210 V280 H0Z" fill="#243e1e"/>'
    b += ''.join(f'<g transform="translate({x} {y})"><rect x="-4" y="-6" width="8" height="18" fill="#3a2614"/><circle cx="0" cy="-16" r="16" fill="#3e6e2a"/></g>' for x, y in ((1120, 180), (1180, 186), (1560, 170), (1610, 176), (1850, 168)))
    b += '<g transform="translate(1380 180)"><rect x="-26" y="-20" width="52" height="30" fill="#f2e6cc" stroke="#3a2614" stroke-width="3"/><path d="M-32 -18 L0 -42 L32 -18 Z" fill="#b8301e" stroke="#3a2614" stroke-width="3"/></g>'
    b += '<rect y="262" width="1920" height="820" fill="url(#rock)"/><path d="M0 262 H1920" stroke="#1a120a" stroke-width="6"/>'
    b += ''.join(f'<path d="M0 {y} Q480 {y - 14} 960 {y} T1920 {y}" fill="none" stroke="#5a4232" stroke-width="3" opacity=".35"/>' for y in (330, 410, 500))
    # ring (perspective ellipse)
    cx, cy, rx, ry = 1150, 700, 640, 230
    b += f'<ellipse cx="{cx}" cy="{cy}" rx="{rx + 40}" ry="{ry + 40}" fill="#3a8aff" opacity=".18" filter="url(#blur30)"/>'
    b += f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="none" stroke="#06101e" stroke-width="70"/>'
    b += f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="none" stroke="#1e5ab8" stroke-width="58"/>'
    b += f'<ellipse cx="{cx}" cy="{cy - 14}" rx="{rx}" ry="{ry}" fill="none" stroke="#6ab4ff" stroke-width="12" opacity=".8"/>'
    b += ''.join(f'<path d="M{cx + (rx) * math.cos(math.radians(a)):.0f} {cy + ry * math.sin(math.radians(a)) - 28:.0f} v56" stroke="#06101e" stroke-width="4" opacity=".7"/>' for a in range(0, 360, 15))
    # beam glow along the ring
    b += f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="none" stroke="#bff6ff" stroke-width="6" opacity=".9"/>'
    # proton comets running round opposite ways, meeting at the front-centre in a burst
    def comet(a0, a1, col):
        out = ''
        n = 18
        for k in range(n):
            a = math.radians(a0 + (a1 - a0) * k / (n - 1))
            out += f'<circle cx="{cx + rx * math.cos(a):.0f}" cy="{cy + ry * math.sin(a):.0f}" r="{4 + 14 * k / n:.1f}" fill="{col}" opacity="{.08 + .7 * k / n:.2f}"/>'
        return out
    b += comet(160, 105, '#ff6a5a') + comet(20, 75, '#6ad2ff')
    bx, by = cx - 20, cy + ry
    b += f'<circle cx="{bx}" cy="{by}" r="190" fill="#fff2c8" opacity=".35" filter="url(#blur30)"/>'
    for k in range(10):   # curly particle tracks
        a = math.radians(-160 + k * 36 + rnd.uniform(-8, 8)); L = rnd.uniform(110, 200); s = rnd.choice([-1, 1])
        ex, ey = bx + L * math.cos(a), by + L * math.sin(a) * .8
        b += f'<path d="M{bx} {by} Q{bx + L * .6 * math.cos(a + s * .6):.0f} {by + L * .6 * math.sin(a + s * .6) * .8:.0f} {ex:.0f} {ey:.0f}" fill="none" stroke="{rnd.choice(["#F2D27A", "#9fe8ff", "#ff9a8a", "#ffffff"])}" stroke-width="4" opacity=".9"/>'
    b += glint(bx, by, 60, '#ffffff', 1)
    # frog riding the ring at the left, hard hat + goggles, holding on
    hat = ('<path d="M-24 -80 q28 -30 58 0 z" fill="#f2b632" stroke-width="3"/><rect x="-28" y="-82" width="66" height="7" rx="3" fill="#e09a1c" stroke-width="2.5"/>')
    vest = '<path d="M-30 -4 q-2 -24 8 -34 l10 30 z M40 -4 q2 -24 -8 -34 l-10 30 z" fill="#ff7a1a" stroke-width="3"/>'
    fa = math.radians(150); fx, fy = cx + rx * math.cos(fa), cy + ry * math.sin(fa) - 30
    b += frog(fx, fy, 2.4, look=(6, 2), mouth='o', helmet=hat, front=vest, rot_=-6,
              armL='M-34 -22 q-10 14 -4 30', armR='M38 -22 q24 -16 30 -46')
    b += spark(1720, 420, 20, '#bff6ff') + spark(760, 520, 14, '#fff6d6', .8)
    return page('#07050a', svg(d, b), [(Y('99.9999991%'), 132, 'w'), ('OF LIGHT', 120, 'w'), ('SPEED', 120, 'w')], outline='#07050a', top=34)


if __name__ == '__main__':
    V = os.path.dirname(HERE)
    for n, f in enumerate((make_1, make_2, make_3, make_4, make_5), 1):
        out = os.path.join(V + f'-short{n}', 'thumb'); os.makedirs(out, exist_ok=True)
        for c in ('common.css', 'Fredoka-700.woff2'): shutil.copy(os.path.join(HERE, c), out)
        open(os.path.join(out, 'A.html'), 'w').write(f())
        print('wrote short', n)
