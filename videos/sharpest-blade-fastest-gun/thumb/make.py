# Thumbnails A-C for sharpest-blade-fastest-gun (v3, owner 2026-11-02: one split-screen concept, sharp half vs fast half, three layouts). v1/ = homages, v2/ = question lineups.
# Sharp half: kitchen knife / obsidian / diamond knife / single-atom needle (S01, S09-S10, S14-S15, S18-S19)
# Fast half: rifle bullet / light-gas-gun slug / proton streak (S24, S27-S28, S33). Text SHARPEST? FASTEST? (title)
# A = vertical seam, B = diagonal slash seam, C = steel-blue top / hot-orange bottom with a big question mark
import os, sys, math, random
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', '..', 'tools'))
from thumb_lib import page, svg, lin, rad, spark

INK = '#1d2b1c'; GREEN = '#6aa55a'; DARKG = '#4d8a4a'; BELLY = '#9cc98a'
SOFT = ('<filter id="soft" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="3"/></filter>'
        '<filter id="blur6" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="6"/></filter>'
        '<filter id="blur12" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="12"/></filter>'
        '<filter id="blur30" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="30"/></filter>')


def corner(x, y):   # bottom-right stays empty (duration badge)
    return x > 1540 and y > 820


def starfield(rnd, n, box, skip=None, col='#eef4ff', omax=.7):
    x0, y0, x1, y1 = box; out = ''
    for _ in range(n):
        x, y = rnd.randint(x0, x1), rnd.randint(y0, y1)
        if skip and skip(x, y): continue
        out += f'<circle cx="{x}" cy="{y}" r="{rnd.choice([1, 1.4, 1.9, 2.6])}" fill="{col}" opacity="{.12 + omax * rnd.random():.2f}"/>'
    return out


def rot(px, py, a, s=1.0):   # rotate a frog-local point by a degrees (SVG clockwise), scale s
    t = math.radians(a)
    return (px * s * math.cos(t) - py * s * math.sin(t), px * s * math.sin(t) + py * s * math.cos(t))


# ---------- mascot frog (tools/assets/frog.svg), posable ----------
def arm(d):
    return (f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="7.5"/>'
            f'<path d="{d}" fill="none" stroke="{GREEN}" stroke-width="3.4"/>')


def frog(x, y, s, flip=False, look=(0, 0), mouth='o', armL=None, armR=None, feet=None, rot_=0,
         back='', front='', helmet=None, nofeet=False):
    sx = -s if flip else s
    g = [f'<g transform="translate({x} {y}) rotate({rot_}) scale({sx} {s})" stroke="{INK}" stroke-linejoin="round" stroke-linecap="round">', back]
    if not nofeet:
        fl, fr = feet or ((-22, 4, 0), (22, 4, 0))
        for fx, fy, fa in (fl, fr):
            g.append(f'<ellipse cx="{fx}" cy="{fy}" rx="16" ry="9" transform="rotate({fa} {fx} {fy})" fill="{DARKG}" stroke-width="3.2"/>')
    g.append(f'<path d="M-34 0 q-6 -64 34 -70 q40 -2 42 62 q0 10 -6 12 q-36 6 -70 -4z" fill="{GREEN}" stroke-width="4"/>')
    g.append(f'<ellipse cx="2" cy="-12" rx="22" ry="20" fill="{BELLY}" stroke="none" opacity=".7"/>')
    g.append(f'<path d="M-24 -50 q6 -14 18 -16" fill="none" stroke="#a9d692" stroke-width="3" opacity=".8"/>')
    lx, ly = look
    for ex in (-10, 22):
        g.append(f'<circle cx="{ex}" cy="-66" r="13" fill="#f4f5ea" stroke-width="3.2"/>')
        g.append(f'<circle cx="{ex + 2 + lx}" cy="{-66 + ly}" r="5.4" fill="{INK}" stroke="none"/>')
        g.append(f'<circle cx="{ex + 3.6 + lx}" cy="{-68 + ly}" r="1.7" fill="#fff" stroke="none"/>')
    if mouth == 'o':
        g.append('<ellipse cx="6" cy="-42" rx="5.5" ry="6.5" fill="#3a1d1d" stroke-width="2.6"/>')
    else:
        g.append('<path d="M-8 -44 q14 12 28 0" fill="none" stroke-width="3.4"/>')
    g.append('<ellipse cx="-16" cy="-50" rx="5" ry="3" fill="#e88f86" stroke="none" opacity=".55"/><ellipse cx="28" cy="-50" rx="5" ry="3" fill="#e88f86" stroke="none" opacity=".55"/>')
    g.append(front)
    aL = armL or 'M-34 -22 q-14 6 -16 22'
    aR = armR or 'M38 -22 q14 6 16 22'
    g.append(arm(aL)); g.append(arm(aR))
    for a in (aL, aR):
        nums = [float(v) for v in a.replace('M', ' ').replace('q', ' ').split()]
        g.append(f'<circle cx="{nums[0] + nums[-2]}" cy="{nums[1] + nums[-1]}" r="4.2" fill="{GREEN}" stroke="{INK}" stroke-width="2.4"/>')
    if helmet: g.append(helmet)
    g.append('</g>')
    return ''.join(g)




def glint(x, y, s, col='#ffffff', op=1.0, rays=True):   # flash glint on an edge
    out = f'<circle cx="{x}" cy="{y}" r="{s * 1.6:.0f}" fill="{col}" opacity="{.35 * op:.2f}" filter="url(#blur12)"/>'
    if rays:
        out += f'<path d="M{x - s * 4.5:.0f} {y} H{x + s * 4.5:.0f} M{x} {y - s * 3:.0f} V{y + s * 3:.0f}" stroke="{col}" stroke-width="{max(1.5, s * .06):.1f}" opacity="{.7 * op:.2f}"/>'
    out += spark(x, y, s, col, op)
    out += f'<circle cx="{x}" cy="{y}" r="{s * .18:.1f}" fill="#fff"/>'
    return out


def spot(x, top, w0, w1, bottom, col, op):   # theatre spotlight beam
    return (f'<polygon points="{x - w0},{top} {x + w0},{top} {x + w1},{bottom} {x - w1},{bottom}" fill="{col}" opacity="{op}" filter="url(#blur12)"/>')


def speed_lines(rnd, n, x0, x1, y0, y1, col, wmax=5, omax=.6):
    out = ''
    for _ in range(n):
        y = rnd.uniform(y0, y1); L = rnd.uniform(80, 420); x = rnd.uniform(x0, x1 - L)
        out += f'<path d="M{x:.0f} {y:.0f} h{L:.0f}" stroke="{col}" stroke-width="{rnd.uniform(1.5, wmax):.1f}" stroke-linecap="round" opacity="{rnd.uniform(.15, omax):.2f}"/>'
    return out


def atom_glow(d, gid, x, y, r):
    d += rad(gid, x, y, r * 9, [(0, '#ffffff', 1), (.1, '#fff1c4', .95), (.25, '#F2D27A', .55), (.55, '#62c9ff', .18), (1, '#62c9ff', 0)])
    b = f'<circle cx="{x}" cy="{y}" r="{r * 9}" fill="url(#{gid})"/>'
    for a in (0, 60, 120):
        b += f'<ellipse cx="{x}" cy="{y}" rx="{r * 3.4:.0f}" ry="{r * 1.05:.0f}" transform="rotate({a} {x} {y})" fill="none" stroke="#bfe9ff" stroke-width="{max(1.5, r * .16):.1f}" opacity=".8"/>'
    b += f'<circle cx="{x}" cy="{y}" r="{r}" fill="#fffaf0" stroke="#F2D27A" stroke-width="{max(1.5, r * .18):.1f}"/>'
    return d, b


def needle(x, base, tip, w, gid):   # tungsten needle, base width w, apex in rows of atoms ending in one
    d = lin(gid, [(0, '#2c3344'), (.35, '#8f9bb2'), (.55, '#e2e8f3'), (.8, '#56617a'), (1, '#20263a')], x2=1, y2=0)
    a = 9   # atom radius
    top = tip + a * 6
    b = f'<polygon points="{x - w / 2},{base} {x + w / 2},{base} {x + a * 2.2},{top} {x - a * 2.2},{top}" fill="url(#{gid})" stroke="#0a0f1e" stroke-width="4"/>'
    b += f'<path d="M{x - w * .12:.0f} {base - 10} L{x - 3} {top + 6}" stroke="#fff" stroke-width="3" opacity=".6"/>'
    for n, y in ((3, top - a * .4), (2, top - a * 2.2)):
        for k in range(n):
            cx = x + (k - (n - 1) / 2) * a * 2
            b += f'<circle cx="{cx:.0f}" cy="{y:.0f}" r="{a}" fill="#8f9bb4" stroke="#0a0f1e" stroke-width="2.4"/><circle cx="{cx - 3:.0f}" cy="{y - 3:.0f}" r="3" fill="#eef3fb" opacity=".8"/>'
    return d, b, (x, top - a * 4.2)


# =========================== shared halves (v3: one split-screen concept, three layouts) ===========================
def sharp_scene(d, light='#fff1c8'):
    """Lineup of edges on a shelf, local box 0..900 x 0..600 (shelf top y=560): kitchen knife, obsidian, diamond knife, one-atom needle."""
    SH = 560; xs = [110, 330, 545, 775]; b = ''
    for i, x in enumerate(xs):
        b += spot(x, -40, 30, 120, SH, light if i < 3 else '#ffe39a', .10 if i < 3 else .22)
        b += f'<ellipse cx="{x}" cy="{SH + 4}" rx="120" ry="18" fill="{light}" opacity="{.12 if i < 3 else .28}" filter="url(#blur6)"/>'
    d += lin('shelf', [(0, '#5a3a22'), (1, '#24140a')])
    b += f'<polygon points="-10,{SH} 900,{SH} 925,{SH + 34} -35,{SH + 34}" fill="#7a5232" stroke="#140a04" stroke-width="5"/>'
    b += f'<rect x="-35" y="{SH + 34}" width="960" height="40" fill="url(#shelf)" stroke="#140a04" stroke-width="5"/>'
    b += f'<path d="M-10 {SH + 3} H900" stroke="#F2D27A" stroke-width="3" opacity=".55"/>'

    def stand(x, w=110):
        return (f'<rect x="{x - w / 2}" y="{SH - 34}" width="{w}" height="38" rx="8" fill="#2c3246" stroke="#0a0d16" stroke-width="4"/>'
                f'<path d="M{x - w / 2 + 8} {SH - 28} H{x + w / 2 - 8}" stroke="#9aa6c0" stroke-width="3" opacity=".6"/>')
    # 1) kitchen knife
    x = xs[0]
    d += lin('kSteel', [(0, '#7d889a'), (.45, '#d6dde8'), (.7, '#f4f7fb'), (1, '#9aa4b4')], x2=1, y2=0)
    b += stand(x, 130)
    b += f'<rect x="{x - 34}" y="{SH - 190}" width="68" height="160" rx="16" fill="#2b1a12" stroke="#0c0604" stroke-width="5"/>'
    b += ''.join(f'<circle cx="{x}" cy="{yy}" r="8" fill="#d8dee8" stroke="#0c0604" stroke-width="3"/>' for yy in (SH - 160, SH - 110, SH - 60))
    b += f'<rect x="{x - 42}" y="{SH - 214}" width="84" height="28" rx="6" fill="#9aa4b4" stroke="#0c0604" stroke-width="5"/>'
    blade = f'M{x - 38} {SH - 212} L{x - 38} {SH - 400} Q{x - 30} {SH - 480} {x + 4} {SH - 540} Q{x + 56} {SH - 440} {x + 52} {SH - 212} Z'
    b += f'<path d="{blade}" fill="url(#kSteel)" stroke="#0c0604" stroke-width="5"/>'
    b += f'<path d="M{x + 30} {SH - 220} Q{x + 34} {SH - 440} {x + 2} {SH - 530}" fill="none" stroke="#ffffff" stroke-width="3" opacity=".8"/>'
    b += f'<path d="M{x + 50} {SH - 214} Q{x + 54} {SH - 442} {x + 4} {SH - 538}" fill="none" stroke="#fff" stroke-width="5"/>'
    b += glint(x + 46, SH - 380, 22, '#ffffff', .8)
    # 2) obsidian flake
    x = xs[1]
    b += stand(x)
    d += lin('obs', [(0, '#3a3450'), (.5, '#120e1c'), (1, '#050308')], x2=1, y2=1)
    obs = f'M{x - 48} {SH - 34} L{x - 60} {SH - 220} Q{x - 40} {SH - 400} {x + 2} {SH - 500} Q{x + 40} {SH - 380} {x + 54} {SH - 200} L{x + 44} {SH - 34} Z'
    b += f'<path d="{obs}" fill="url(#obs)" stroke="#000" stroke-width="5"/>'
    for j in range(1, 6):
        yy = SH - 60 - j * 68
        b += f'<path d="M{x - 50 + j * 4} {yy + 30} Q{x} {yy - 14} {x + 48 - j * 5} {yy + 26}" fill="none" stroke="#8f7fd0" stroke-width="2.4" opacity=".45"/>'
    b += f'<path d="M{x - 36} {SH - 230} Q{x - 24} {SH - 370} {x} {SH - 480}" fill="none" stroke="#d9d0ff" stroke-width="5" opacity=".55"/>'
    b += f'<path d="M{x + 54} {SH - 200} Q{x + 40} {SH - 380} {x + 2} {SH - 500}" fill="none" stroke="#fff" stroke-width="3.5"/>'
    b += glint(x + 30, SH - 400, 20, '#e6deff', .85)
    # 3) diamond knife on its metal boat
    x = xs[2]
    d += lin('boat', [(0, '#b9c3d2'), (1, '#4a5466')])
    b += f'<path d="M{x - 80} {SH} L{x - 70} {SH - 150} L{x + 70} {SH - 150} L{x + 80} {SH} Z" fill="url(#boat)" stroke="#0a0d16" stroke-width="5"/>'
    b += f'<rect x="{x - 56}" y="{SH - 136}" width="112" height="40" rx="6" fill="#5ab4e0" opacity=".55" stroke="#0a0d16" stroke-width="3"/>'
    d += lin('dia', [(0, '#ffffff'), (.4, '#bfe8ff'), (1, '#4a8fc0')], x2=1, y2=1)
    b += f'<polygon points="{x - 50},{SH - 150} {x + 50},{SH - 150} {x + 6},{SH - 310} {x - 2},{SH - 310}" fill="url(#dia)" stroke="#0a2a40" stroke-width="4"/>'
    b += f'<path d="M{x - 30} {SH - 150} L{x} {SH - 306} L{x + 22} {SH - 150} M{x - 50} {SH - 190} H{x + 40}" stroke="#ffffff" stroke-width="2" opacity=".6" fill="none"/>'
    b += glint(x + 2, SH - 310, 30, '#e6f7ff', .95)
    # 4) single-atom needle
    x = xs[3]
    b += stand(x, 120)
    nd, nb, (ax, ay) = needle(x, SH - 34, SH - 470, 60, 'tung')
    d += nd; b += nb
    d, gb = atom_glow(d, 'atomS', ax, ay, 15)
    b += gb + spark(ax + 70, ay - 60, 18, '#fff6d6') + spark(ax - 80, ay - 20, 12, '#bfe9ff', .8)
    return d, b, (ax, ay)


def burst(x, y, s, rnd, col='#fff2c8', shard='#cfefff', n=14, spread=70):   # flash + shards flying forward (to +x)
    b = f'<circle cx="{x}" cy="{y}" r="{s * 1.6:.0f}" fill="{col}" opacity=".45" filter="url(#blur12)"/>'
    b += ''.join(f'<path d="M{x} {y} L{x + s * 2.2 * math.cos(math.radians(a)):.0f} {y + s * 2.2 * math.sin(math.radians(a)):.0f}" stroke="{col}" stroke-width="{s * .07:.1f}" stroke-linecap="round" opacity=".85"/>'
                 for a in range(-spread, spread + 1, max(8, spread // 5)))
    for _ in range(n):
        a = math.radians(rnd.uniform(-spread, spread)); r_ = rnd.uniform(s * .6, s * 2.4); px, py = x + r_ * math.cos(a), y + r_ * math.sin(a); k = rnd.uniform(s * .1, s * .26)
        b += (f'<polygon points="{px:.0f},{py - k:.0f} {px + k * 1.3:.0f},{py + k * .2:.0f} {px - k * .4:.0f},{py + k:.0f}" transform="rotate({rnd.randint(0, 360)} {px:.0f} {py:.0f})" '
              f'fill="{shard}" fill-opacity=".75" stroke="#ffffff" stroke-width="1.6"/>')
    b += spark(x, y, s * .7, '#ffffff', 1)
    return b


def fast_scene(d, rnd, lane='#3a3f7a'):
    """Race of three projectiles, local box 0..960 x 0..500, moving right; tails extend left of 0 (clip outside)."""
    lanes = [90, 250, 410]; b = ''
    for y in lanes:
        for yy in (y - 70, y + 70):
            b += f'<path d="M-500 {yy} H960" stroke="{lane}" stroke-width="3" opacity=".6"/>'
    FL = 790
    for k in range(18):
        for c in range(2):
            col = '#f4f4f4' if (k + c) % 2 == 0 else '#15151f'
            b += f'<rect x="{FL + c * 24}" y="{20 + k * 24}" width="24" height="24" fill="{col}" opacity=".85"/>'
    b += f'<rect x="{FL}" y="20" width="48" height="432" fill="none" stroke="#000" stroke-width="3"/>'
    # rifle bullet (slowest): copper, short streaks, small air puff in front
    y = lanes[2]; bx = 250
    d += lin('cu', [(0, '#ffd2a0'), (.35, '#d98a4a'), (.75, '#8a4a1e'), (1, '#4a240c')])
    b += speed_lines(rnd, 12, -300, bx - 120, y - 28, y + 28, '#ffcf9a', 4, .45)
    b += (f'<path d="M{bx - 160} {y - 32} L{bx - 10} {y - 32} Q{bx + 66} {y - 28} {bx + 104} {y} Q{bx + 66} {y + 28} {bx - 10} {y + 32} L{bx - 160} {y + 32} Q{bx - 172} {y} {bx - 160} {y - 32} Z" '
          f'fill="url(#cu)" stroke="#1c0c04" stroke-width="5"/>')
    b += f'<path d="M{bx - 150} {y - 19} L{bx} {y - 21} Q{bx + 52} {y - 19} {bx + 86} {y - 6}" fill="none" stroke="#fff3e0" stroke-width="4" opacity=".7"/>'
    b += f'<path d="M{bx - 112} {y - 32} V{y + 32} M{bx - 94} {y - 32} V{y + 32}" stroke="#5a2e10" stroke-width="3" opacity=".7"/>'
    b += burst(bx + 124, y, 26, rnd, '#ffe2b8', '#ffd2a0', n=6, spread=50)
    # light-gas-gun slug: pointed steel projectile, hot glowing nose, shock cone, punching through a glass pane
    y = lanes[1]; sx = 470; R = 44; nx = sx + 190
    d += ('<linearGradient id="trail2" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#5ac8ff" stop-opacity="0"/>'
          '<stop offset=".7" stop-color="#ffb35a" stop-opacity=".55"/><stop offset="1" stop-color="#fff2c8" stop-opacity=".95"/></linearGradient>')
    b += f'<polygon points="{sx - 900},{y} {sx - 120},{y - R * .8:.0f} {sx - 120},{y + R * .8:.0f}" fill="url(#trail2)"/>'
    b += speed_lines(rnd, 30, -400, sx - 100, y - 62, y + 62, '#cfe4ff', 5, .7)
    d += ('<linearGradient id="cone" x1="1" y1="0" x2="0" y2="0"><stop offset="0" stop-color="#ffffff" stop-opacity=".6"/>'
          '<stop offset="1" stop-color="#9fd8ff" stop-opacity="0"/></linearGradient>')
    for k, (ang, L) in enumerate(((22, 440), (28, 360), (34, 290))):
        t = math.radians(ang)
        b += (f'<path d="M{nx - L * math.cos(t):.0f} {y - L * math.sin(t):.0f} L{nx + 4} {y} L{nx - L * math.cos(t):.0f} {y + L * math.sin(t):.0f}" '
              f'fill="none" stroke="url(#cone)" stroke-width="{6 - k * 1.6:.1f}" stroke-linecap="round"/>')
    d += lin('slug', [(0, '#f4f7fb'), (.3, '#b9c3d2'), (.75, '#5b6680'), (1, '#262c3c')])
    b += f'<path d="M{sx - 120} {y - R} L{sx + 60} {y - R} Q{sx + 150} {y - R + 6} {nx} {y} Q{sx + 150} {y + R - 6} {sx + 60} {y + R} L{sx - 120} {y + R} Q{sx - 130} {y} {sx - 120} {y - R} Z" fill="url(#slug)" stroke="#0a0f1e" stroke-width="5"/>'
    b += f'<path d="M{sx - 110} {y - R + 12} L{sx + 60} {y - R + 12} Q{sx + 130} {y - R + 18} {nx - 20} {y - 6}" fill="none" stroke="#fff" stroke-width="4" opacity=".7"/>'
    b += f'<path d="M{sx - 60} {y - R} V{y + R} M{sx - 40} {y - R} V{y + R}" stroke="#2a3040" stroke-width="4" opacity=".6"/>'
    d += rad('hotnose', nx - 20, y, 70, [(0, '#fff6d6', 1), (.3, '#ffb35a', .8), (1, '#ff5a2a', 0)])
    b += f'<path d="M{sx + 100} {y - R + 14} Q{sx + 150} {y - R + 16} {nx} {y} Q{sx + 150} {y + R - 16} {sx + 100} {y + R - 14} Z" fill="url(#hotnose)" opacity=".9"/>'
    px_ = nx + 22   # glass pane being shattered
    b += f'<path d="M{px_} {y - 120} L{px_ + 10} {y - 40} M{px_} {y + 120} L{px_ + 10} {y + 40}" stroke="#bfe9ff" stroke-width="10" opacity=".55"/>'
    b += burst(px_ + 4, y, 56, rnd, '#fff2c8', '#cfefff', n=18, spread=70)
    # proton: a near-invisible streak of light, already past the finish line
    y = lanes[0]; ph = 915
    d += ('<linearGradient id="pStreak" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#9fe8ff" stop-opacity="0"/>'
          '<stop offset=".8" stop-color="#bff0ff" stop-opacity=".75"/><stop offset="1" stop-color="#ffffff" stop-opacity="1"/></linearGradient>')
    b += f'<path d="M-500 {y} L{ph} {y}" stroke="#5ac8ff" stroke-width="34" opacity=".35" filter="url(#blur6)"/>'
    b += f'<path d="M-500 {y} L{ph} {y}" stroke="url(#pStreak)" stroke-width="10" stroke-linecap="round"/>'
    b += f'<path d="M200 {y} L{ph} {y}" stroke="#ffffff" stroke-width="3" stroke-linecap="round" opacity=".9"/>'
    d, gb = atom_glow(d, 'pG', ph, y, 8)
    b += gb + f'<circle cx="{ph}" cy="{y}" r="130" fill="#bff0ff" opacity=".12" filter="url(#blur30)"/>' + glint(ph, y, 40, '#ffffff', 1)
    return d, b


def seam_glow(path, col='#fff1c4', w=6):
    return (f'<path d="{path}" fill="none" stroke="{col}" stroke-width="{w * 7}" opacity=".18" filter="url(#blur12)"/>'
            f'<path d="{path}" fill="none" stroke="{col}" stroke-width="{w * 2.4}" opacity=".45" filter="url(#blur6)"/>'
            f'<path d="{path}" fill="none" stroke="#ffffff" stroke-width="{w}"/>')


TEXT = [('SHARPEST?', 136, 'w'), ('FASTEST?', 158, 'y')]


# =========================== A: clean vertical split, frog peeking over the seam ===========================
def make_A():
    rnd = random.Random(71)
    d = SOFT
    d += lin('aL', [(0, '#16233d'), (1, '#070b16')]) + lin('aR', [(0, '#1a0f33'), (1, '#07040f')])
    d += '<clipPath id="cL"><rect x="0" y="0" width="960" height="1080"/></clipPath><clipPath id="cR"><rect x="960" y="0" width="960" height="1080"/></clipPath>'
    body = '<rect width="960" height="1080" fill="url(#aL)"/><rect x="960" width="960" height="1080" fill="url(#aR)"/>'
    body += starfield(rnd, 60, (0, 0, 960, 1080), None, '#cfe0ff', .3) + starfield(rnd, 70, (960, 0, 1920, 1080), corner, '#e6dcff', .3)
    d, sb, _ = sharp_scene(d)
    body += f'<g clip-path="url(#cL)"><g transform="translate(20 400) scale(.9)">{sb}</g></g>'
    d, fb = fast_scene(d, rnd)
    body += f'<g clip-path="url(#cR)"><g transform="translate(975 290) scale(1.0)">{fb}</g></g>'
    body += seam_glow('M960 0 V1080')
    # frog peeking over / straddling the seam at the bottom
    body += '<ellipse cx="960" cy="1040" rx="130" ry="16" fill="#000" opacity=".5"/>'
    body += frog(960, 1034, 3.0, look=(6, -5), mouth='o',
                 armL='M-34 -22 q-24 -18 -22 -44', armR='M38 -24 q26 -10 34 -34', feet=((-26, 4, -10), (26, 4, 10)))
    for k in range(3):
        a = math.radians(-125 + k * 28)
        body += f'<path d="M{970 + 190 * math.cos(a):.0f} {860 + 190 * math.sin(a):.0f} l{32 * math.cos(a):.0f} {32 * math.sin(a):.0f}" stroke="#fff" stroke-width="6" stroke-linecap="round"/>'
    return page('#0b0f1e', svg(d, body), TEXT, outline='#05070f', top=40)


# =========================== B: diagonal slash split, frog in goggles and lab coat ===========================
def make_B():
    rnd = random.Random(83)
    d = SOFT
    X0, X1 = 1300, 640   # seam: (X0,0) -> (X1,1080)
    d += lin('bL', [(0, '#10283a'), (1, '#050c14')]) + lin('bR', [(0, '#2a0f2e'), (1, '#0a0412')])
    d += f'<clipPath id="cL"><polygon points="0,0 {X0},0 {X1},1080 0,1080"/></clipPath><clipPath id="cR"><polygon points="{X0},0 1920,0 1920,1080 {X1},1080"/></clipPath>'
    body = f'<polygon points="0,0 {X0},0 {X1},1080 0,1080" fill="url(#bL)"/><polygon points="{X0},0 1920,0 1920,1080 {X1},1080" fill="url(#bR)"/>'
    body += starfield(rnd, 140, (0, 0, 1920, 1080), corner, '#e6eeff', .3)
    d, sb, _ = sharp_scene(d)
    body += f'<g clip-path="url(#cL)"><g transform="translate(30 520) scale(.74)">{sb}</g></g>'
    d, fb = fast_scene(d, rnd, lane='#5a2f6a')
    body += f'<g clip-path="url(#cR)"><g transform="translate(1010 130) scale(.9)">{fb}</g></g>'
    seam = f'M{X0} 0 L{X1} 1080'
    body += seam_glow(seam, '#9fe8ff', 7)
    # sparks flying off the slash
    for _ in range(26):
        t = rnd.uniform(.05, .95); x, y = X0 + (X1 - X0) * t, 1080 * t
        a = math.radians(rnd.uniform(-60, 60) + (180 if rnd.random() < .5 else 0)); L = rnd.uniform(14, 46)
        if corner(x, y): continue
        body += f'<path d="M{x:.0f} {y:.0f} l{L * math.cos(a):.0f} {L * math.sin(a):.0f}" stroke="#fff2c8" stroke-width="3" stroke-linecap="round" opacity=".85"/>'
    body += spark(X0 + (X1 - X0) * .45, 1080 * .45, 30, '#ffffff') + spark(X0 + (X1 - X0) * .2, 1080 * .2, 20, '#e6f7ff', .9)
    # frog on the fast side by the seam: safety goggles pushed up, lab coat, ducking with hands on cheeks
    coat = ('<path d="M-36 -2 q-6 -30 0 -44 l12 2 q6 22 8 42 z M42 0 q6 -30 0 -44 l-12 2 q-6 22 -8 42 z" fill="#f4f6fa" stroke-width="3"/>'
            '<path d="M-36 -2 q-4 10 4 14 l12 -4 z M42 0 q4 10 -4 14 l-12 -4 z" fill="#f4f6fa" stroke-width="3"/>')
    goggles = ('<path d="M-24 -84 h56" stroke="#2a2a2a" stroke-width="4"/><rect x="-24" y="-92" width="22" height="14" rx="6" fill="#9fe8ff" fill-opacity=".7" stroke-width="3"/>'
               '<rect x="10" y="-92" width="22" height="14" rx="6" fill="#9fe8ff" fill-opacity=".7" stroke-width="3"/>')
    body += '<ellipse cx="930" cy="1040" rx="120" ry="14" fill="#000" opacity=".5"/>'
    body += frog(930, 1032, 2.8, look=(6, -6), mouth='o', front=coat, helmet=goggles, rot_=4,
                 armL='M-34 -22 q-14 -10 -6 -30', armR='M38 -22 q14 -10 6 -30')
    return page('#0b0f1e', svg(d, body), TEXT, outline='#05070f', top=40)


# =========================== C: top/bottom colour split, big question mark at the seam ===========================
def make_C():
    rnd = random.Random(97)
    d = SOFT
    SY = 548
    d += lin('cT', [(0, '#24456a'), (1, '#0f2238')]) + lin('cB', [(0, '#8a3410'), (.5, '#5a1e08'), (1, '#2a0c04')])
    d += f'<clipPath id="cTop"><rect width="1920" height="{SY}"/></clipPath><clipPath id="cBot"><rect y="{SY}" width="1920" height="{1080 - SY}"/></clipPath>'
    body = f'<rect width="1920" height="{SY}" fill="url(#cT)"/><rect y="{SY}" width="1920" height="{1080 - SY}" fill="url(#cB)"/>'
    body += starfield(rnd, 60, (0, 0, 1920, SY), None, '#dff0ff', .3)
    d += rad('heat', 900, 820, 700, [(0, '#ffb35a', .35), (1, '#ff5a2a', 0)])
    body += f'<rect y="{SY}" width="1920" height="{1080 - SY}" fill="url(#heat)"/>'
    d, sb, _ = sharp_scene(d, light='#dff0ff')
    body += f'<g clip-path="url(#cTop)"><g transform="translate(1130 70) scale(.78)">{sb}</g></g>'
    d, fb = fast_scene(d, rnd, lane='#c8642a')
    body += f'<g clip-path="url(#cBot)"><g transform="translate(40 590) scale(.92)">{fb}</g></g>'
    body += seam_glow(f'M0 {SY} H1920', '#fff1c4', 6)
    # big question mark sitting on the seam
    qx, qy = 1010, SY + 150
    body += f'<text x="{qx}" y="{qy}" text-anchor="middle" font-family="Fredoka" font-weight="700" font-size="430" fill="#F2D27A" opacity=".4" filter="url(#blur30)">?</text>'
    body += (f'<text x="{qx}" y="{qy}" text-anchor="middle" font-family="Fredoka" font-weight="700" font-size="400" fill="#F2D27A" '
             f'stroke="#2a1404" stroke-width="16" paint-order="stroke fill">?</text>')
    body += spark(qx + 130, qy - 300, 22) + spark(qx - 150, qy - 120, 16, '#fff6d6', .8)
    # frog beside the question mark, hard hat, startled, hands up
    hat = ('<path d="M-22 -80 q26 -26 54 0 z" fill="#f2b632" stroke-width="3"/><rect x="-26" y="-82" width="62" height="7" rx="3" fill="#e09a1c" stroke-width="2.5"/>')
    body += '<ellipse cx="1400" cy="1040" rx="110" ry="14" fill="#000" opacity=".5"/>'
    body += frog(1400, 1032, 2.7, flip=True, look=(4, -6), mouth='o', helmet=hat,
                 armL='M-34 -22 q-22 -14 -26 -40', armR='M38 -24 q22 -14 26 -40')
    return page('#0f2238', svg(d, body), TEXT, outline='#05070f', top=40)


if __name__ == '__main__':
    for n, f in (('A', make_A), ('B', make_B), ('C', make_C)):
        open(os.path.join(HERE, f'{n}.html'), 'w').write(f())
        print('wrote', n)
