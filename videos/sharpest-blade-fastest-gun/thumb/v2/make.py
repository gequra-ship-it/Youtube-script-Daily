# Thumbnails A-C for sharpest-blade-fastest-gun (v2, owner 2026-11-02: all intuitive, question + lineup/contest). v1 (homages) kept in v1/.
# A = WHAT'S THE SHARPEST?: lineup kitchen knife / obsidian / diamond knife / single-atom needle (S01, S09-S10, S14-S15, S18-S19)
# B = WHAT'S THE FASTEST?: race rifle bullet / light-gas-gun slug / proton streak (S24, S27-S28, S33)
# C = SHARPEST? FASTEST?: blade ending in one atom vs projectile, big question mark (S18, S28, S42)
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


# =========================== A: WHAT'S THE SHARPEST? (lineup of edges) ===========================
def make_A():
    rnd = random.Random(41)
    d = SOFT
    d += lin('aBg', [(0, '#121a33'), (.6, '#0c1226'), (1, '#05070f')])
    body = '<rect width="1920" height="1080" fill="url(#aBg)"/>'
    body += starfield(rnd, 70, (900, 0, 1920, 700), corner, '#cfe0ff', .35)
    SH = 862   # shelf top
    xs = [640, 880, 1100, 1480]
    for i, x in enumerate(xs):   # one spotlight per contestant, brightest on the last
        body += spot(x, -20, 40, 150, SH, '#fff1c8' if i < 3 else '#ffe39a', .10 if i < 3 else .2)
        body += f'<ellipse cx="{x}" cy="{SH + 4}" rx="140" ry="20" fill="#fff1c8" opacity="{.12 if i < 3 else .25}" filter="url(#blur6)"/>'
    # shelf (dark wood with a brass lip), stops short of the bottom-right corner
    d += lin('shelf', [(0, '#5a3a22'), (1, '#24140a')])
    body += f'<polygon points="470,{SH} 1560,{SH} 1590,{SH + 40} 440,{SH + 40}" fill="#7a5232" stroke="#140a04" stroke-width="5"/>'
    body += f'<rect x="440" y="{SH + 40}" width="1150" height="46" fill="url(#shelf)" stroke="#140a04" stroke-width="5"/>'
    body += f'<path d="M470 {SH + 3} H1560" stroke="#F2D27A" stroke-width="3" opacity=".55"/>'
    body += f'<ellipse cx="1015" cy="{SH + 110}" rx="620" ry="26" fill="#000" opacity=".5" filter="url(#blur12)"/>'
    # stands
    def stand(x, w=110):
        return (f'<rect x="{x - w / 2}" y="{SH - 34}" width="{w}" height="38" rx="8" fill="#2c3246" stroke="#0a0d16" stroke-width="4"/>'
                f'<path d="M{x - w / 2 + 8} {SH - 28} H{x + w / 2 - 8}" stroke="#9aa6c0" stroke-width="3" opacity=".6"/>')
    # 1) kitchen knife, point up, edge on the right
    x = xs[0]
    d += lin('kSteel', [(0, '#7d889a'), (.45, '#d6dde8'), (.7, '#f4f7fb'), (1, '#9aa4b4')], x2=1, y2=0)
    body += stand(x, 130)
    body += f'<rect x="{x - 34}" y="{SH - 190}" width="68" height="160" rx="16" fill="#2b1a12" stroke="#0c0604" stroke-width="5"/>'
    body += ''.join(f'<circle cx="{x}" cy="{yy}" r="8" fill="#d8dee8" stroke="#0c0604" stroke-width="3"/>' for yy in (SH - 160, SH - 110, SH - 60))
    body += f'<rect x="{x - 42}" y="{SH - 214}" width="84" height="28" rx="6" fill="#9aa4b4" stroke="#0c0604" stroke-width="5"/>'
    blade = f'M{x - 38} {SH - 212} L{x - 38} {SH - 400} Q{x - 30} {SH - 480} {x + 4} {SH - 540} Q{x + 56} {SH - 440} {x + 52} {SH - 212} Z'
    body += f'<path d="{blade}" fill="url(#kSteel)" stroke="#0c0604" stroke-width="5"/>'
    body += f'<path d="M{x + 30} {SH - 220} Q{x + 34} {SH - 440} {x + 2} {SH - 530}" fill="none" stroke="#ffffff" stroke-width="3" opacity=".8"/>'
    body += f'<path d="M{x + 50} {SH - 214} Q{x + 54} {SH - 442} {x + 4} {SH - 538}" fill="none" stroke="#fff" stroke-width="5"/>'
    body += glint(x + 46, SH - 380, 22, '#ffffff', .8)
    # 2) obsidian flake (black volcanic glass, conchoidal ripples)
    x = xs[1]
    body += stand(x)
    d += lin('obs', [(0, '#3a3450'), (.5, '#120e1c'), (1, '#050308')], x2=1, y2=1)
    obs = f'M{x - 48} {SH - 34} L{x - 60} {SH - 220} Q{x - 40} {SH - 400} {x + 2} {SH - 520} Q{x + 40} {SH - 380} {x + 54} {SH - 200} L{x + 44} {SH - 34} Z'
    body += f'<path d="{obs}" fill="url(#obs)" stroke="#000" stroke-width="5"/>'
    for j in range(1, 6):
        yy = SH - 60 - j * 70
        body += f'<path d="M{x - 50 + j * 4} {yy + 30} Q{x} {yy - 14} {x + 48 - j * 5} {yy + 26}" fill="none" stroke="#8f7fd0" stroke-width="2.4" opacity=".45"/>'
    body += f'<path d="M{x - 36} {SH - 230} Q{x - 24} {SH - 380} {x} {SH - 500}" fill="none" stroke="#d9d0ff" stroke-width="5" opacity=".55"/>'
    body += f'<path d="M{x + 54} {SH - 200} Q{x + 40} {SH - 380} {x + 2} {SH - 520}" fill="none" stroke="#fff" stroke-width="3.5"/>'
    body += glint(x + 30, SH - 410, 20, '#e6deff', .85)
    # 3) diamond knife on its metal boat
    x = xs[2]
    d += lin('boat', [(0, '#b9c3d2'), (1, '#4a5466')])
    body += f'<path d="M{x - 80} {SH} L{x - 70} {SH - 150} L{x + 70} {SH - 150} L{x + 80} {SH} Z" fill="url(#boat)" stroke="#0a0d16" stroke-width="5"/>'
    body += f'<rect x="{x - 56}" y="{SH - 136}" width="112" height="40" rx="6" fill="#5ab4e0" opacity=".55" stroke="#0a0d16" stroke-width="3"/>'
    d += lin('dia', [(0, '#ffffff'), (.4, '#bfe8ff'), (1, '#4a8fc0')], x2=1, y2=1)
    body += f'<polygon points="{x - 50},{SH - 150} {x + 50},{SH - 150} {x + 6},{SH - 300} {x - 2},{SH - 300}" fill="url(#dia)" stroke="#0a2a40" stroke-width="4"/>'
    body += f'<path d="M{x - 30} {SH - 150} L{x} {SH - 296} L{x + 22} {SH - 150} M{x - 50} {SH - 190} H{x + 40}" stroke="#ffffff" stroke-width="2" opacity=".6" fill="none"/>'
    body += f'<path d="M{x - 2} {SH - 300} H{x + 6}" stroke="#fff" stroke-width="6"/>'
    body += glint(x + 2, SH - 300, 30, '#e6f7ff', .95)
    # 4) single-atom needle: thin, tiny tip, glowing
    x = xs[3]
    body += stand(x, 120)
    nd, nb, (ax, ay) = needle(x, SH - 34, SH - 440, 60, 'tung')
    d += nd; body += nb
    gd, gb = atom_glow(d, 'atomA', ax, ay, 15)
    d = gd; body += gb
    body += spark(ax + 70, ay - 70, 18, '#fff6d6') + spark(ax - 90, ay - 30, 12, '#bfe9ff', .8)
    # ---- frog behind the shelf, squinting through a big magnifier at the atom ----
    FX, FY, FS = 1300, SH - 2, 2.7
    lens_x, lens_y, lens_r = 1452, ay + 4, 74
    hx, hy = FX + 46 * FS, FY - 40 * FS
    body += f'<path d="M{hx:.0f} {hy:.0f} L{lens_x - lens_r * .6:.0f} {lens_y + lens_r * .8:.0f}" stroke="#140a04" stroke-width="20" stroke-linecap="round"/>'
    body += f'<path d="M{hx:.0f} {hy:.0f} L{lens_x - lens_r * .6:.0f} {lens_y + lens_r * .8:.0f}" stroke="#8a5a32" stroke-width="12" stroke-linecap="round"/>'
    squint = ('<path d="M-22 -70 q12 -6 24 0" fill="none" stroke-width="3"/>')
    body += frog(FX, FY, FS, look=(5, -5), mouth='o', front=squint,
                 armR='M38 -24 q10 -10 8 -16', armL='M-34 -22 q-16 4 -18 20', feet=((-22, 4, 0), (22, 4, 0)))
    body += f'<circle cx="{lens_x}" cy="{lens_y}" r="{lens_r}" fill="#cfefff" fill-opacity=".12" stroke="#F2D27A" stroke-width="12"/>'
    body += f'<circle cx="{lens_x}" cy="{lens_y}" r="{lens_r - 6}" fill="none" stroke="#5a3c10" stroke-width="3"/>'
    body += f'<path d="M{lens_x - 48} {lens_y - 22} q14 -30 46 -38" fill="none" stroke="#fff" stroke-width="7" stroke-linecap="round" opacity=".6"/>'
    lines = [("WHAT'S THE", 118, 'w'), ('SHARPEST?', 172, 'y')]
    return page('#0c1226', svg(d, body), lines, outline='#05070f', top=56)


# =========================== B: WHAT'S THE FASTEST? (race of projectiles) ===========================
def make_B():
    rnd = random.Random(53)
    d = SOFT
    d += lin('bBg', [(0, '#0c1024'), (.6, '#130c2a'), (1, '#05040c')])
    body = '<rect width="1920" height="1080" fill="url(#bBg)"/>'
    body += starfield(rnd, 90, (0, 0, 1920, 1080), corner, '#d8e2ff', .3)
    lanes = [470, 630, 780]
    # race lanes (glowing track lines) and a chequered finish line
    for y in lanes:
        for yy in ((y - 80, y + 80) if y < 700 else (y - 80,)):
            body += f'<path d="M0 {yy} H1920" stroke="#3a3f7a" stroke-width="3" opacity=".55"/>'
    FL = 1620
    for k in range(int((800 - (lanes[0] - 80)) / 26)):
        y = lanes[0] - 80 + k * 26
        if y + 26 > 820 and False: break
        for c in range(2):
            col = '#f4f4f4' if (k + c) % 2 == 0 else '#15151f'
            body += f'<rect x="{FL + c * 26}" y="{y}" width="26" height="26" fill="{col}" opacity=".85"/>'
    body += f'<rect x="{FL}" y="{lanes[0] - 80}" width="52" height="{int((800 - (lanes[0] - 80)) / 26) * 26}" fill="none" stroke="#000" stroke-width="3"/>'
    # ---- lane 3: rifle bullet (slow, left, few streaks) ----
    y = lanes[2]; bx = 640
    d += lin('cu', [(0, '#ffd2a0'), (.35, '#d98a4a'), (.75, '#8a4a1e'), (1, '#4a240c')])
    body += speed_lines(rnd, 10, 120, bx - 120, y - 30, y + 30, '#ffcf9a', 4, .4)
    body += (f'<path d="M{bx - 170} {y - 34} L{bx - 10} {y - 34} Q{bx + 70} {y - 30} {bx + 110} {y} Q{bx + 70} {y + 30} {bx - 10} {y + 34} L{bx - 170} {y + 34} Q{bx - 182} {y} {bx - 170} {y - 34} Z" '
             f'fill="url(#cu)" stroke="#1c0c04" stroke-width="5"/>')
    body += f'<path d="M{bx - 160} {y - 20} L{bx} {y - 22} Q{bx + 56} {y - 20} {bx + 92} {y - 6}" fill="none" stroke="#fff3e0" stroke-width="4" opacity=".7"/>'
    body += f'<path d="M{bx - 120} {y - 34} V{y + 34} M{bx - 100} {y - 34} V{y + 34}" stroke="#5a2e10" stroke-width="3" opacity=".7"/>'
    # ---- lane 2: light-gas-gun slug (fast: shock cone, many streaks, hot trail) ----
    y = lanes[1]; sx = 1250; R = 52
    d += ('<linearGradient id="trail2" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#5ac8ff" stop-opacity="0"/>'
          '<stop offset=".7" stop-color="#ffb35a" stop-opacity=".55"/><stop offset="1" stop-color="#fff2c8" stop-opacity=".95"/></linearGradient>')
    body += f'<polygon points="{sx - 900},{y} {sx - 150},{y - R * .8:.0f} {sx - 150},{y + R * .8:.0f}" fill="url(#trail2)"/>'
    body += speed_lines(rnd, 34, 60, sx - 120, y - 70, y + 70, '#cfe4ff', 5, .7)
    # shock cone from the nose, opening backward
    nx = sx + 120
    d += ('<linearGradient id="cone" x1="1" y1="0" x2="0" y2="0"><stop offset="0" stop-color="#ffffff" stop-opacity=".55"/>'
          '<stop offset="1" stop-color="#9fd8ff" stop-opacity="0"/></linearGradient>')
    for k, (ang, L) in enumerate(((24, 520), (30, 430), (36, 340))):
        t = math.radians(ang)
        body += (f'<path d="M{nx - L * math.cos(t):.0f} {y - L * math.sin(t):.0f} L{nx + 6} {y} L{nx - L * math.cos(t):.0f} {y + L * math.sin(t):.0f}" '
                 f'fill="none" stroke="url(#cone)" stroke-width="{7 - k * 2}" stroke-linecap="round"/>')
    body += f'<path d="M{nx - 470:.0f} {y - 210:.0f} L{nx + 6} {y} L{nx - 470:.0f} {y + 210:.0f} Z" fill="url(#cone)" opacity=".18"/>'
    d += lin('slug', [(0, '#f4f7fb'), (.3, '#b9c3d2'), (.75, '#5b6680'), (1, '#262c3c')])
    body += f'<rect x="{sx - 150}" y="{y - R}" width="240" height="{2 * R}" rx="14" fill="url(#slug)" stroke="#0a0f1e" stroke-width="5"/>'
    body += f'<path d="M{sx + 88} {y - R} Q{sx + 124} {y - R + 4} {nx} {y} Q{sx + 124} {y + R - 4} {sx + 88} {y + R} Z" fill="url(#slug)" stroke="#0a0f1e" stroke-width="5"/>'
    body += f'<path d="M{sx - 136} {y - R + 14} H{sx + 96}" stroke="#fff" stroke-width="5" opacity=".7"/>'
    body += f'<path d="M{nx - 14} {y - 30} Q{nx + 10} {y} {nx - 14} {y + 30}" fill="none" stroke="#ffd59a" stroke-width="6" opacity=".9"/>'
    body += glint(sx - 20, y - R + 10, 18, '#ffffff', .8, rays=False)
    # ---- lane 1: the proton, a near-invisible streak of light already past the finish ----
    y = lanes[0]; px = 1840
    d += ('<linearGradient id="pStreak" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#9fe8ff" stop-opacity="0"/>'
          '<stop offset=".75" stop-color="#bff0ff" stop-opacity=".7"/><stop offset="1" stop-color="#ffffff" stop-opacity="1"/></linearGradient>')
    body += f'<path d="M80 {y} L{px} {y}" stroke="#5ac8ff" stroke-width="26" opacity=".18" filter="url(#blur6)"/>'
    body += f'<path d="M80 {y} L{px} {y}" stroke="url(#pStreak)" stroke-width="5" stroke-linecap="round"/>'
    gd, gb = atom_glow(d, 'pG', px, y, 9)
    d = gd; body += gb
    body += f'<circle cx="{px}" cy="{y}" r="160" fill="#bff0ff" opacity=".12" filter="url(#blur30)"/>'
    body += glint(px, y, 46, '#ffffff', 1)
    # ---- frog at the trackside, startled, arms flung up ----
    sweat = ''.join(f'<path d="M{xx} {yy} q-5 9 0 13 q5 -4 0 -13z" fill="#bfe6ff" stroke="{INK}" stroke-width="1.8"/>' for xx, yy in ((-52, -84), (62, -90)))
    body += '<ellipse cx="1150" cy="1018" rx="120" ry="14" fill="#000" opacity=".5"/>'
    body += frog(1150, 1010, 2.6, look=(6, -6), mouth='o', front=sweat, rot_=-6,
                 armL='M-34 -24 q-22 -14 -26 -40', armR='M38 -24 q22 -14 26 -40', feet=((-26, 4, -10), (26, 4, 10)))
    for k in range(3):   # startle lines
        a = math.radians(-120 + k * 30)
        body += f'<path d="M{1160 + 175 * math.cos(a):.0f} {870 + 175 * math.sin(a):.0f} l{30 * math.cos(a):.0f} {30 * math.sin(a):.0f}" stroke="#fff" stroke-width="6" stroke-linecap="round"/>'
    lines = [("WHAT'S THE", 118, 'w'), ('FASTEST?', 182, 'y')]
    return page('#0c1024', svg(d, body), lines, outline='#05040c', top=40)


# =========================== C: SHARPEST? FASTEST? (blade vs gun, big question mark) ===========================
def make_C():
    rnd = random.Random(67)
    d = SOFT
    d += ('<linearGradient id="cBg" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#0f2430"/><stop offset=".5" stop-color="#181434"/>'
          '<stop offset="1" stop-color="#2a0e22"/></linearGradient>')
    body = '<rect width="1920" height="1080" fill="url(#cBg)"/>'
    body += starfield(rnd, 90, (0, 0, 1920, 1080), corner, '#e6eeff', .3)
    # ---- left: huge blade coming in from the left, razor edge, ending in one atom ----
    d += lin('cSteel', [(0, '#f4f7fb'), (.3, '#c3ccda'), (.7, '#6d7890'), (1, '#2e3548')])
    tipx, tipy = 840, 640
    blade = f'M-40 520 L520 520 Q700 540 {tipx} {tipy} Q640 720 380 800 L-40 830 Z'
    body += f'<path d="{blade}" fill="#000" opacity=".4" transform="translate(10 26)" filter="url(#blur12)"/>'
    body += f'<path d="{blade}" fill="url(#cSteel)" stroke="#05070c" stroke-width="6"/>'
    body += f'<path d="M-40 760 Q300 760 380 744 Q620 690 {tipx - 10} {tipy + 2}" fill="none" stroke="#e8eef8" stroke-width="22" opacity=".25"/>'
    body += f'<path d="M-40 826 L380 798 Q640 718 {tipx} {tipy}" fill="none" stroke="#ffffff" stroke-width="6"/>'
    body += f'<path d="M-40 540 L500 540" stroke="#fff" stroke-width="4" opacity=".6"/>'
    body += glint(470, 780, 34, '#ffffff', 1)
    for k in range(3):   # the edge narrows to atoms
        body += f'<circle cx="{tipx + 4 + k * 0}" cy="{tipy - 12 + k * 12}" r="7" fill="#9aa6bc" stroke="#05070c" stroke-width="2"/>'
    body += f'<circle cx="{tipx + 18}" cy="{tipy - 6}" r="7" fill="#9aa6bc" stroke="#05070c" stroke-width="2"/><circle cx="{tipx + 18}" cy="{tipy + 6}" r="7" fill="#9aa6bc" stroke="#05070c" stroke-width="2"/>'
    gd, gb = atom_glow(d, 'cA', tipx + 36, tipy, 15)
    d = gd; body += gb
    # ---- right: a glowing projectile flying in from the right with streaks and a shock cone ----
    py, px, R = 600, 1380, 48
    d += ('<linearGradient id="cTrail" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#fff2c8" stop-opacity=".95"/>'
          '<stop offset=".3" stop-color="#ff8a5a" stop-opacity=".55"/><stop offset="1" stop-color="#b04aff" stop-opacity="0"/></linearGradient>')
    body += f'<polygon points="{px + 40},{py - R * .8:.0f} 1960,{py - 10} 1960,{py + 10} {px + 40},{py + R * .8:.0f}" fill="url(#cTrail)"/>'
    body += speed_lines(rnd, 40, px + 60, 1920, py - 110, py + 110, '#ffd9f0', 5, .7)
    nx = px - 120
    d += ('<linearGradient id="cCone" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#ffffff" stop-opacity=".6"/>'
          '<stop offset="1" stop-color="#ff9ad0" stop-opacity="0"/></linearGradient>')
    for k, (ang, L) in enumerate(((22, 520), (28, 420), (34, 320))):
        t = math.radians(ang)
        body += (f'<path d="M{nx + L * math.cos(t):.0f} {py - L * math.sin(t):.0f} L{nx - 6} {py} L{nx + L * math.cos(t):.0f} {py + L * math.sin(t):.0f}" '
                 f'fill="none" stroke="url(#cCone)" stroke-width="{7 - k * 2}" stroke-linecap="round"/>')
    d += lin('cSlug', [(0, '#fff3e0'), (.3, '#e0a36a'), (.75, '#8a4a1e'), (1, '#3a1a08')])
    body += (f'<path d="M{px + 140} {py - R} L{px - 40} {py - R} Q{px - 100} {py - R + 6} {nx} {py} Q{px - 100} {py + R - 6} {px - 40} {py + R} L{px + 140} {py + R} Z" '
             f'fill="url(#cSlug)" stroke="#1c0c04" stroke-width="5"/>')
    body += f'<path d="M{px + 130} {py - R + 14} L{px - 40} {py - R + 14} Q{px - 84} {py - R + 18} {nx + 14} {py - 8}" fill="none" stroke="#fff" stroke-width="5" opacity=".7"/>'
    body += f'<circle cx="{nx}" cy="{py}" r="70" fill="#fff1c4" opacity=".35" filter="url(#blur12)"/>'
    body += f'<path d="M{nx + 16} {py - 34} Q{nx - 10} {py} {nx + 16} {py + 34}" fill="none" stroke="#fff2c8" stroke-width="7"/>'
    body += glint(px + 40, py - R + 8, 20, '#ffffff', .85, rays=False)
    # ---- big glowing question mark between them ----
    qx, qy = 1050, 600
    body += f'<text x="{qx}" y="{qy + 150}" text-anchor="middle" font-family="Fredoka" font-weight="700" font-size="460" fill="#F2D27A" opacity=".35" filter="url(#blur30)">?</text>'
    body += (f'<text x="{qx}" y="{qy + 150}" text-anchor="middle" font-family="Fredoka" font-weight="700" font-size="430" fill="#F2D27A" '
             f'stroke="#2a1404" stroke-width="16" paint-order="stroke fill">?</text>')
    body += spark(qx + 120, qy - 160, 26) + spark(qx - 140, qy + 40, 16, '#fff6d6', .8) + spark(1700, 300, 18, '#ffd9f0', .7)
    # ---- frog below, between blade and bullet, looking up at both, surprised ----
    body += '<ellipse cx="1060" cy="1022" rx="110" ry="14" fill="#000" opacity=".5"/>'
    body += frog(1060, 1014, 2.5, look=(0, -6), mouth='o',
                 armL='M-34 -22 q-14 -10 -6 -30', armR='M38 -22 q14 -10 6 -30')
    lines = [('SHARPEST?', 150, 'w'), ('FASTEST?', 172, 'y')]
    return page('#181434', svg(d, body), lines, outline='#05070c', top=44)


if __name__ == '__main__':
    for n, f in (('A', make_A), ('B', make_B), ('C', make_C)):
        open(os.path.join(HERE, f'{n}.html'), 'w').write(f())
        print('wrote', n)
