# Thumbnails A-C for hollow-skyscraper (Burj Khalifa, 828 m, mostly air). Opus thumb agent 2026-11-03, set 2 (all INTUITIVE, owner:
# "make intuitive ones, emphasise the intuitive type, 3 again"). Set 1 (homages) is kept in v1/.
# A = cut-away tower: inside is mostly air + glowing concrete spine (S01, S18), beside a rolled paper tube carrying a stack of books (S03, S51).
#     Text MOSTLY AIR / BUT STRONG (S01 "most of it is air"; S25 "does not need to be solid to be strong").
# B = the tower stands on a giant pair of snowshoes on soft sand, a high heel sinks next to it (S12-S13 raft = "architectural snowshoe").
#     Text THE SECRET: / SNOWSHOES.
# C = a swirling wind monster blasts the tower; the stepped spiral taper breaks the blast into small soft eddies (S30-S39).
#     Text CONFUSE / THE WIND (S38, museum exhibit's three words).
import os, sys, math, random
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', '..', 'tools'))
from thumb_lib import svg, lin, rad, spark

INK = '#1d2b1c'; GREEN = '#6aa55a'; DARKG = '#4d8a4a'; BELLY = '#9cc98a'
FILTERS = ''.join(f'<filter id="blur{s}" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="{s}"/></filter>'
                  for s in (2, 4, 8, 14, 30, 60))
HEAD = '<!doctype html><html><head><meta charset="utf-8"><link rel="stylesheet" href="common.css"><style>%s</style></head><body><div class="stage">'


def page(bg, art, lines, outline='#0b0f24', left=84, top=40):
    """lines: [(size, [(text, 'w'|'y'), ...]), ...] - one yellow word allowed."""
    css = f'body{{background:{bg}}}.o{{-webkit-text-stroke:16px {outline};paint-order:stroke fill}}.g{{color:#F2D27A}}'
    html = ''; y = top
    for k, (sz, segs) in enumerate(lines):
        css += f'#t{k}{{left:{left}px;top:{y}px;font-size:{sz}px;letter-spacing:3px;line-height:1;filter:drop-shadow(0 8px 10px rgba(0,0,0,.45))}}'
        inner = ''.join(f'<span class="g">{t}</span>' if c == 'y' else t for t, c in segs)
        html += f'<div class="txt o" id="t{k}">{inner}</div>'
        y += int(sz * 0.98)
    return HEAD % css + art + html + '</div></body></html>'


# ---------- mascot frog (tools/assets/frog.svg), posable ----------
def arm(d):
    return (f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="7.5"/>'
            f'<path d="{d}" fill="none" stroke="{GREEN}" stroke-width="3.4"/>')


def frog(x, y, s, flip=False, look=(0, 0), mouth='o', armL=None, armR=None, feet=None, rot_=0, back='', front='', top=''):
    sx = -s if flip else s
    g = [f'<g transform="translate({x} {y}) rotate({rot_}) scale({sx} {s})" stroke="{INK}" stroke-linejoin="round" stroke-linecap="round">', back]
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
    for a in (aL, aR):
        g.append(arm(a))
        nums = [float(v) for v in a.replace('M', ' ').replace('q', ' ').split()]
        g.append(f'<circle cx="{nums[0] + nums[-2]}" cy="{nums[1] + nums[-1]}" r="4.4" fill="{GREEN}" stroke="{INK}" stroke-width="2.4"/>')
    g.append(top)
    g.append('</g>')
    return ''.join(g)


HARDHAT = ('<path d="M-24 -78 q30 -36 62 0 z" fill="#f2b632" stroke-width="3"/><path d="M6 -96 v16" stroke="#c98a12" stroke-width="3"/>'
           '<rect x="-31" y="-81" width="76" height="9" rx="4" fill="#e09a1c" stroke-width="2.6"/>'
           '<path d="M-14 -84 q10 -18 24 -20" fill="none" stroke="#ffe7a0" stroke-width="3" opacity=".9"/>')


# ---------- Burj Khalifa, front elevation (Y plan seen from one wing tip) ----------
# outer half-widths of the left and right wings (units of the base width W), stepping back in a spiral, h in units of H (tip = 1)
# concave taper like the real tower: big setbacks low down, a long slim needle above
LST = [(0, .50), (.07, .42), (.14, .35), (.21, .29), (.28, .24), (.35, .20), (.42, .165), (.49, .135), (.56, .11), (.63, .09), (.70, .072), (.76, .058)]
RST = [(0, .50), (.105, .40), (.175, .33), (.245, .27), (.315, .22), (.385, .18), (.455, .15), (.525, .12), (.595, .10), (.665, .08), (.735, .064), (.775, .056)]
NTOP = .80   # top of the needle, spire above


def stepv(st, h):
    v = st[0][1]
    for b, w in st:
        if h >= b: v = w
    return v


def BPS():
    return sorted(set(b for b, _ in LST[1:]) | set(b for b, _ in RST[1:]))


def cfun(h):
    return min(.16, .52 * min(stepv(LST, h), stepv(RST, h)))


def strip_path(fa, fb, cx, base, W, H, ra=False, rb=False, top=NTOP, inset=0):
    X = lambda u: cx + u * W; Y = lambda h: base - h * H
    bps = [b for b in BPS() if b < top]
    a0 = fa(0) + inset
    d = f'M{X(a0):.1f} {Y(0) + 1:.1f}'
    cur = a0
    for b in bps:
        new = fa(b + 1e-6) + inset
        if abs(new - cur) > 1e-9:
            if ra:
                r = min(abs(new - cur) * W * 1.3, 40)
                d += f' L{X(cur):.1f} {Y(b) + r:.1f} Q{X(cur):.1f} {Y(b):.1f} {X(new):.1f} {Y(b):.1f}'
            else:
                d += f' L{X(cur):.1f} {Y(b):.1f} L{X(new):.1f} {Y(b):.1f}'
            cur = new
    d += f' L{X(cur):.1f} {Y(top):.1f}'
    bt = fb(top - 1e-6) - inset
    d += f' L{X(bt):.1f} {Y(top):.1f}'
    cur = bt
    for b in reversed(bps):
        new = fb(b - 1e-6) - inset
        if abs(new - cur) > 1e-9:
            if rb:
                r = min(abs(new - cur) * W * 1.3, 40)
                d += f' L{X(cur):.1f} {Y(b):.1f} Q{X(new):.1f} {Y(b):.1f} {X(new):.1f} {Y(b) + r:.1f}'
            else:
                d += f' L{X(cur):.1f} {Y(b):.1f} L{X(new):.1f} {Y(b):.1f}'
            cur = new
    d += f' L{X(cur):.1f} {Y(0) + 1:.1f} Z'
    return d


def tower(cx, base, H, W, p, tag, extra_inside=''):
    """p: faces=[(bottom,top) x4 left->right], edge, rim, rimside 'L'|'R', band, line, glow, glowop.
    Returns (defs, body). extra_inside is drawn clipped to the silhouette on top of the facade (cut-away)."""
    L = lambda h: -stepv(LST, h); R = lambda h: stepv(RST, h)
    C = lambda h: -cfun(h); Cp = cfun; Z = lambda h: 0
    X = lambda u: cx + u * W; Y = lambda h: base - h * H
    d = ''
    for i, (c0, c1) in enumerate(p['faces']):
        d += f'<linearGradient id="{tag}f{i}" x1="0" y1="{Y(0)}" x2="0" y2="{Y(NTOP)}" gradientUnits="userSpaceOnUse"><stop offset="0" stop-color="{c0}"/><stop offset="1" stop-color="{c1}"/></linearGradient>'
    fs = max(4.0, H / 165)
    d += (f'<pattern id="{tag}fl" width="40" height="{fs:.2f}" patternUnits="userSpaceOnUse">'
          f'<rect width="40" height="{max(1.1, fs * .28):.2f}" fill="{p["line"]}" opacity=".38"/></pattern>')
    sil = strip_path(L, R, cx, base, W, H, True, True)
    d += f'<clipPath id="{tag}clip"><path d="{sil}"/></clipPath>'
    d += lin(f'{tag}sh', [(0, '#ffffff'), (1, '#ffffff')], x2=1, y2=0)
    b = ''
    # halo
    b += f'<ellipse cx="{cx}" cy="{base - H * .42}" rx="{W * 1.25}" ry="{H * .58}" fill="{p["glow"]}" opacity="{p.get("glowop", .4)}" filter="url(#blur60)"/>'
    b += f'<ellipse cx="{cx}" cy="{base - H * .35}" rx="{W * .7}" ry="{H * .4}" fill="{p["glow"]}" opacity="{p.get("glowop", .4) * .6}" filter="url(#blur30)"/>'
    strips = [(L, C, True, False), (C, Z, False, False), (Z, Cp, False, False), (Cp, R, False, True)]
    for i, (fa, fb, ra, rb) in enumerate(strips):
        b += f'<path d="{strip_path(fa, fb, cx, base, W, H, ra, rb)}" fill="url(#{tag}f{i})"/>'
    g = f'<g clip-path="url(#{tag}clip)">'
    g += f'<rect x="{X(-.6):.0f}" y="{Y(NTOP):.0f}" width="{W * 1.2:.0f}" height="{H * NTOP + 2:.0f}" fill="url(#{tag}fl)"/>'
    # vertical mullions
    for u in (-.42, -.34, -.26, -.2, -.1, -.05, .05, .1, .2, .26, .34, .42):
        b2 = 'M{0:.1f} {1:.1f} V{2:.1f}'.format(X(u), Y(0), Y(NTOP))
        g += f'<path d="{b2}" stroke="{p["line"]}" stroke-width="{max(1.2, W / 260):.1f}" opacity=".35"/>'
    # mechanical floors (darker bands)
    for fy in (.075, .16, .245, .33, .415, .5, .585, .67, .745):
        g += f'<rect x="{X(-.6):.0f}" y="{Y(fy):.1f}" width="{W * 1.2:.0f}" height="{max(4, H / 120):.1f}" fill="{p["band"]}" opacity=".5"/>'
    # wing seams (sharp edges of the Y)
    for u in (0,):
        g += f'<path d="M{X(u):.1f} {Y(0)} V{Y(NTOP)}" stroke="{p["rim"]}" stroke-width="{max(2, W / 110):.1f}" opacity=".55"/>'
    # sky reflection sheen
    g += f'<path d="M{X(-.6):.0f} {Y(.12):.0f} L{X(.6):.0f} {Y(.42):.0f} L{X(.6):.0f} {Y(.52):.0f} L{X(-.6):.0f} {Y(.22):.0f}Z" fill="#ffffff" opacity=".10" filter="url(#blur8)"/>'
    g += f'<path d="M{X(-.6):.0f} {Y(.44):.0f} L{X(.6):.0f} {Y(.66):.0f} L{X(.6):.0f} {Y(.69):.0f} L{X(-.6):.0f} {Y(.47):.0f}Z" fill="#ffffff" opacity=".12" filter="url(#blur4)"/>'
    g += extra_inside
    g += '</g>'
    b += g
    # crisp outline + rim light on the lit edge
    b += f'<path d="{sil}" fill="none" stroke="{p["edge"]}" stroke-width="{max(2, W / 120):.1f}"/>'
    rim = strip_path(L, R, cx, base, W, H, True, True)
    side = p.get('rimside', 'L')
    b += (f'<clipPath id="{tag}rc"><rect x="{X(-.7) if side == "L" else cx:.0f}" y="0" width="{W * .7:.0f}" height="{base + 5}"/></clipPath>'
          f'<path d="{rim}" fill="none" stroke="{p["rim"]}" stroke-width="{max(3, W / 70):.1f}" clip-path="url(#{tag}rc)" opacity=".9"/>')
    # needle cap and spire
    t0 = Y(NTOP); tip = Y(1)
    hw = .05 * W
    b += f'<polygon points="{cx - hw:.1f},{t0 + 2} {cx + hw:.1f},{t0 + 2} {cx + 2:.1f},{tip + H * .03:.1f} {cx:.1f},{tip} {cx - 2:.1f},{tip + H * .03:.1f}" fill="{p["faces"][3][1]}" stroke="{p["edge"]}" stroke-width="2"/>'
    b += f'<polygon points="{cx - hw:.1f},{t0 + 2} {cx:.1f},{t0 + 2} {cx:.1f},{tip} {cx - 2:.1f},{tip + H * .03:.1f}" fill="{p["faces"][1][1]}"/>'
    for k in range(1, 8):
        y = t0 - (t0 - tip) * k / 8.5; w = hw * (1 - k / 8.5) + 1
        b += f'<path d="M{cx - w:.1f} {y:.1f} H{cx + w:.1f}" stroke="{p["edge"]}" stroke-width="1.8" opacity=".55"/>'
    b += f'<path d="M{cx - (hw if side == "L" else -hw) * .9:.1f} {t0} L{cx:.1f} {tip}" stroke="{p["rim"]}" stroke-width="3" opacity=".9"/>'
    b += f'<circle cx="{cx}" cy="{tip + 4}" r="18" fill="{p["rim"]}" opacity=".6" filter="url(#blur8)"/>' + spark(cx, tip + 4, 30, '#fffbe8', .95)
    return d, b


# =========================== A: hollow but strong ===========================
def make_A():
    rnd = random.Random(3); d = FILTERS; HZ = 830
    d += lin('aSky', [(0, '#0e1240'), (.45, '#2b2f78'), (.75, '#7b4a92'), (.93, '#e0857a'), (1, '#ffc58a')])
    d += lin('aGnd', [(0, '#5a3a5a'), (.3, '#3a2546'), (1, '#170f24')])
    body = f'<rect width="1920" height="{HZ}" fill="url(#aSky)"/>'
    body += f'<ellipse cx="1300" cy="{HZ}" rx="900" ry="220" fill="#ffb27a" opacity=".35" filter="url(#blur60)"/>'
    for _ in range(140):
        body += f'<circle cx="{rnd.randint(20, 1900)}" cy="{rnd.randint(10, 560)}" r="{rnd.choice([1.2, 1.7, 2.4])}" fill="#eef0ff" opacity="{rnd.uniform(.2, .8):.2f}"/>'
    # distant Dubai skyline with lit windows
    sky = ''
    for x0, x1 in ((0, 760), (1560, 1920)):
        x = x0
        while x < x1:
            w = rnd.randint(18, 46); h = rnd.randint(20, 120) if rnd.random() < .8 else rnd.randint(120, 210)
            sky += f'<rect x="{x}" y="{HZ - h}" width="{w}" height="{h + 4}" fill="#2a1d44"/>'
            for _ in range(h // 14):
                if rnd.random() < .55:
                    sky += f'<rect x="{x + rnd.randint(3, w - 6)}" y="{HZ - h + rnd.randint(4, h - 6)}" width="3" height="3" fill="#ffd38a" opacity="{rnd.uniform(.4, .95):.2f}"/>'
            x += w + rnd.randint(2, 14)
    body += sky
    body += f'<rect y="{HZ}" width="1920" height="{1080 - HZ}" fill="url(#aGnd)"/>'
    body += f'<path d="M0 {HZ + 40} Q400 {HZ + 5} 900 {HZ + 50} T1920 {HZ + 30} V1080 H0Z" fill="#2c1c3a"/>'
    body += f'<path d="M0 {HZ + 40} Q400 {HZ + 5} 900 {HZ + 50} T1920 {HZ + 30}" fill="none" stroke="#e7a07e" stroke-width="3" opacity=".55"/>'
    body += '<path d="M0 960 Q500 900 1100 975 T1920 960 V1080 H0Z" fill="#1d1229"/>'
    body += '<path d="M0 960 Q500 900 1100 975 T1920 960" fill="none" stroke="#c98a7a" stroke-width="3" opacity=".45"/>'

    # ---- the cut-away tower ----
    cx, base, H, W = 1330, 985, 960, 420
    X = lambda u: cx + u * W; Y = lambda h: base - h * H
    # interior: airy sky inside, a few thin floor slabs, the glowing hexagonal concrete core
    din = lin('aIn', [(0, '#fff6dc'), (.5, '#d9ecff'), (1, '#a9c9f2')])
    din += lin('aCore', [(0, '#a8742a'), (.25, '#f6d488'), (.5, '#fff1c2'), (.75, '#e7b562'), (1, '#8a5b22')], x2=1, y2=0)
    din += rad('aCoreG', cx, Y(.35), 420, [(0, '#ffe2a0', .9), (.4, '#ffd27a', .35), (1, '#ffd27a', 0)])
    hcut0, hcut1 = .04, .58
    inner = strip_path(lambda h: -stepv(LST, h), lambda h: stepv(RST, h), cx, base, W, H, True, True, inset=.04)
    jag = ' '.join(f'L{X(.34 - .2 * t + (.03 if k % 2 else -.02)):.0f} {Y(hcut0 + (hcut1 - hcut0) * t):.0f}' for k, t in enumerate([i / 9 for i in range(10)]))
    cutpath = f'M{X(-.7)} {Y(hcut0)} {jag} L{X(-.7)} {Y(hcut1 + .03)}Z'
    din += f'<clipPath id="aCut"><path d="{cutpath}"/></clipPath>'
    din += f'<clipPath id="aInner"><path d="{inner}"/></clipPath>'
    cut = f'<g clip-path="url(#aCut)"><g clip-path="url(#aInner)">'
    cut += f'<rect x="{X(-.6)}" y="{Y(hcut1 + .05)}" width="{W * 1.2}" height="{H * .7}" fill="url(#aIn)"/>'
    cut += f'<rect x="{X(-.6)}" y="{Y(hcut1 + .05)}" width="{W * 1.2}" height="{H * .7}" fill="url(#aCoreG)"/>'
    # soft clouds of air drifting inside
    for (u, h, s) in ((-.28, .13, 1.25), (.24, .2, 1.1), (-.19, .3, .95), (.15, .4, .7), (-.1, .48, .6), (.27, .07, .9)):
        x, y = X(u), Y(h)
        cut += (f'<g fill="none" stroke="#8fa8d8" stroke-width="7" opacity=".8"><ellipse cx="{x}" cy="{y}" rx="{46 * s}" ry="{18 * s}"/><ellipse cx="{x - 18 * s}" cy="{y - 10 * s}" rx="{24 * s}" ry="{16 * s}"/><ellipse cx="{x + 16 * s}" cy="{y - 13 * s}" rx="{20 * s}" ry="{15 * s}"/></g>'
                f'<g opacity=".95"><ellipse cx="{x}" cy="{y}" rx="{46 * s}" ry="{18 * s}" fill="#ffffff"/>'
                f'<ellipse cx="{x - 18 * s}" cy="{y - 10 * s}" rx="{24 * s}" ry="{16 * s}" fill="#ffffff"/>'
                f'<ellipse cx="{x + 16 * s}" cy="{y - 13 * s}" rx="{20 * s}" ry="{15 * s}" fill="#ffffff"/>'
                f'<ellipse cx="{x}" cy="{y + 8 * s}" rx="{44 * s}" ry="{8 * s}" fill="#c9dcf5" opacity=".7"/></g>')
    # thin floor slabs (only a few: it is mostly air), in perspective
    for k, h in enumerate((.085, .17, .255, .34, .425)):
        y = Y(h)
        cut += f'<path d="M{X(-.6)} {y} H{X(.6)}" stroke="#6b7fa8" stroke-width="7" opacity=".9"/>'
        cut += f'<path d="M{X(-.6)} {y - 3} H{X(.6)}" stroke="#eef4ff" stroke-width="2.5" opacity=".9"/>'
        cut += f'<path d="M{X(-.6)} {y + 4} L{X(.6)} {y + 4} L{X(.6)} {y + 26} L{X(-.6)} {y + 26}Z" fill="#7f95c4" opacity=".16"/>'
        for u in (-.3, -.19, .19, .3):   # slim columns
            cut += f'<rect x="{X(u) - 3}" y="{y + 4}" width="6" height="{H * .085 - 6}" fill="#8aa0cc" opacity=".55"/>'
    # tiny people for scale on two floors
    for u, h in ((-.26, .17), (.2, .34), (-.3, .085)):
        x, y = X(u), Y(h) - 4
        cut += f'<g fill="#2b2f5e"><circle cx="{x}" cy="{y - 15}" r="3.6"/><rect x="{x - 3}" y="{y - 11}" width="6" height="11" rx="2"/></g>'
    # the core: glowing concrete spine
    cw = .085
    cut += f'<rect x="{X(-cw) - 30}" y="{Y(.9)}" width="{2 * cw * W + 60}" height="{H}" fill="#ffd27a" opacity=".55" filter="url(#blur14)"/>'
    cut += f'<rect x="{X(-cw)}" y="{Y(.9)}" width="{2 * cw * W}" height="{H}" fill="url(#aCore)" stroke="#6a4416" stroke-width="3"/>'
    for k in range(18):
        y = Y(.045 + k * .033)
        cut += f'<path d="M{X(-cw)} {y} H{X(cw)}" stroke="#8a5b22" stroke-width="1.6" opacity=".45"/>'
    cut += f'<path d="M{X(-cw * .35)} {Y(.9)} V{base}" stroke="#fff7d8" stroke-width="5" opacity=".85"/>'
    cut += f'<path d="M{X(cw * .45)} {Y(.9)} V{base}" stroke="#a8742a" stroke-width="3" opacity=".6"/>'
    cut += '</g></g>'
    # cut edge: facade thickness + slab ends along the slanted section line
    edge = f'<g clip-path="url(#aInner)"><path d="{cutpath}" fill="none" stroke="#2a2050" stroke-width="16" opacity=".5"/><path d="{cutpath}" fill="none" stroke="#f3e6ff" stroke-width="6"/></g>'
    d2, b2 = tower(cx, base, H, W, dict(
        faces=[('#5a6fb0', '#a6b6ea'), ('#7489c8', '#c7d2f6'), ('#3c4a86', '#7f8fcc'), ('#2b3570', '#5f6db0')],
        edge='#141a40', rim='#ffd6b0', rimside='L', band='#1b2252', line='#16204e', glow='#ffcf9a', glowop=.55), 'aT', cut + edge)
    d += din + d2
    body += b2
    # cut frame outline around the open section (thick concrete edge)
    body += (f'<g clip-path="url(#aTclip)"><path d="{inner}" fill="none" stroke="#e9dcff" stroke-width="7" clip-path="url(#aCut)" opacity=".85"/></g>')
    # sparkles of air around the open part
    for (x, y, s) in ((X(-.62), Y(.3), 22), (X(.6), Y(.22), 18), (X(.55), Y(.5), 26), (X(-.5), Y(.55), 16), (1640, 330, 22), (1020, 250, 16)):
        body += spark(x, y, s, '#fff4d6', .9)

    # ---- rolled paper tube carrying a stack of books ----
    tx, tb, tr, th = 560, 990, 108, 400       # centre x, bottom y, radius, height
    d += lin('aPap', [(0, '#b9a990'), (.18, '#f3ead8'), (.42, '#fffdf5'), (.75, '#e3d6bd'), (1, '#9c8a70')], x2=1, y2=0)
    d += rad('aTubeG', tx, tb - th * .6, 380, [(0, '#ffe7b8', .7), (.5, '#ffcf8a', .25), (1, '#ffcf8a', 0)])
    body += f'<ellipse cx="{tx}" cy="{tb - th * .55}" rx="360" ry="380" fill="url(#aTubeG)"/>'
    body += f'<ellipse cx="{tx + 40}" cy="{tb + 6}" rx="{tr + 90}" ry="22" fill="#0b0614" opacity=".55" filter="url(#blur8)"/>'
    top = tb - th; ry = 26
    body += f'<path d="M{tx - tr} {top} V{tb} A{tr} {ry} 0 0 0 {tx + tr} {tb} V{top}Z" fill="url(#aPap)" stroke="#4b3c2c" stroke-width="4"/>'
    # spiral seam of the rolled sheet + loose outer edge
    for k in range(4):
        y0 = top + 60 + k * 95
        body += f'<path d="M{tx - tr} {y0} Q{tx} {y0 + ry * 1.9} {tx + tr} {y0 + 40}" fill="none" stroke="#a8977a" stroke-width="3" opacity=".7"/>'
    body += f'<path d="M{tx - tr + 26} {top + 30} V{tb - 20}" stroke="#ffffff" stroke-width="12" opacity=".7" stroke-linecap="round"/>'
    # stack of heavy books on top
    books = [('#c0443e', '#8e2b28', 300, 62, -2), ('#2f6fa8', '#1e4b75', 280, 56, 3), ('#e0a531', '#a8761b', 290, 60, -1.5), ('#4d8a4a', '#2f5e2d', 262, 54, 2)]
    y = top - 6
    for col, dark, w, h, ang in books:
        y -= h
        bx = tx - w / 2 + (ang * 3)
        body += (f'<g transform="rotate({ang} {tx} {y + h / 2})">'
                 f'<rect x="{bx}" y="{y}" width="{w}" height="{h}" rx="7" fill="{col}" stroke="#2a1a14" stroke-width="4"/>'
                 f'<rect x="{bx + 14}" y="{y + 8}" width="{w - 22}" height="{h - 16}" rx="3" fill="#f7efdc"/>'
                 f'<path d="M{bx + 16} {y + 16} H{bx + w - 10} M{bx + 16} {y + 26} H{bx + w - 10} M{bx + 16} {y + 36} H{bx + w - 10}" stroke="#d4c6a6" stroke-width="2"/>'
                 f'<rect x="{bx}" y="{y}" width="20" height="{h}" rx="7" fill="{dark}" stroke="#2a1a14" stroke-width="4"/>'
                 f'<path d="M{bx + 4} {y + 10} H{bx + 16} M{bx + 4} {y + h - 10} H{bx + 16}" stroke="#F2D27A" stroke-width="3"/></g>')
    body += f'<path d="M{tx - 150} {y - 30} q-20 -14 -6 -30 M{tx + 150} {y - 30} q20 -14 6 -30" fill="none" stroke="#ffe7b8" stroke-width="5" opacity=".0"/>'
    # hollow top of the tube peeking (dark inner ring) under the books
    body += f'<ellipse cx="{tx}" cy="{top}" rx="{tr}" ry="{ry}" fill="none" stroke="#4b3c2c" stroke-width="4" opacity=".0"/>'
    # ---- frog in a hard hat, both arms up in amazement ----
    body += frog(860, 1000, 3.0, look=(-3, -4), mouth='o',
                 armL='M-34 -24 q-22 -10 -26 -40', armR='M38 -24 q22 -10 24 -40', top=HARDHAT)
    for (x, y) in ((760, 690), (950, 650)):
        body += spark(x, y, 16, '#fff4d6', .9)
    return page('#0e1240', svg(d, body), [(170, [('MOSTLY ', 'w'), ('AIR', 'y')]), (124, [('BUT STRONG', 'w')])], outline='#0b0a26')


# =========================== B: snowshoes ===========================
def snowshoe(cx, cy, L, Wd, ang, tag):
    """a classic wooden snowshoe lying flat, seen in perspective (squashed vertically)."""
    o = f'<g transform="translate({cx} {cy}) scale(1 .5) rotate({ang})">'
    frame = (f'M0 {-L / 2} C{Wd * .66} {-L / 2} {Wd * .62} {L * .05} {Wd * .2} {L * .3} L{Wd * .04} {L / 2} L{-Wd * .04} {L / 2} '
             f'L{-Wd * .2} {L * .3} C{-Wd * .62} {L * .05} {-Wd * .66} {-L / 2} 0 {-L / 2}Z')
    o += f'<path d="{frame}" transform="translate(10 26)" fill="#5a3410" opacity=".35"/>'
    o += f'<clipPath id="{tag}c"><path d="{frame}"/></clipPath>'
    o += f'<path d="{frame}" fill="#7a4a1c" opacity=".55"/>'
    # rawhide lattice webbing
    web = ''
    for k in range(-14, 15):
        web += f'<path d="M{k * Wd * .085 - L} {-L} L{k * Wd * .085 + L} {L}" stroke="#f4e2b8" stroke-width="8"/>'
        web += f'<path d="M{k * Wd * .085 + L} {-L} L{k * Wd * .085 - L} {L}" stroke="#b98a4a" stroke-width="8"/>'
    o += f'<g clip-path="url(#{tag}c)">{web}</g>'
    # cross bars
    for yy in (-L * .12, L * .16):
        o += f'<path d="M{-Wd * .48} {yy} H{Wd * .48}" stroke="#7a4a1c" stroke-width="16" clip-path="url(#{tag}c)"/>'
    o += f'<path d="{frame}" fill="none" stroke="#2e1806" stroke-width="{Wd * .17:.0f}"/>'
    o += f'<path d="{frame}" fill="none" stroke="#9a5a22" stroke-width="{Wd * .12:.0f}"/>'
    o += f'<path d="{frame}" fill="none" stroke="#f0b26a" stroke-width="{Wd * .03:.0f}" transform="translate(-3 -5)"/>'
    o += '</g>'
    return o


def make_B():
    rnd = random.Random(7); d = FILTERS; HZ = 740
    d += lin('bSky', [(0, '#1f7fc4'), (.5, '#5fbde6'), (.85, '#bfe6f0'), (1, '#ffe6b0')])
    d += lin('bSand', [(0, '#f6c27a'), (.4, '#eaa75a'), (1, '#c7793a')])
    d += rad('bSun', 1720, 150, 380, [(0, '#fffbe6', 1), (.12, '#fff1b8', .9), (.35, '#ffe08a', .35), (1, '#ffe08a', 0)])
    body = f'<rect width="1920" height="{HZ}" fill="url(#bSky)"/><rect width="1920" height="{HZ}" fill="url(#bSun)"/>'
    body += '<circle cx="1720" cy="150" r="62" fill="#fffbe8"/>'
    for (x, y, s) in ((420, 520, 1.4), (1530, 470, 1.1), (780, 600, .8)):
        body += (f'<g opacity=".85" fill="#ffffff"><ellipse cx="{x}" cy="{y}" rx="{90 * s}" ry="{20 * s}"/><ellipse cx="{x - 30 * s}" cy="{y - 14 * s}" rx="{44 * s}" ry="{22 * s}"/>'
                 f'<ellipse cx="{x + 30 * s}" cy="{y - 18 * s}" rx="{40 * s}" ry="{24 * s}"/></g>')
    # far city on the horizon
    for x0, x1 in ((40, 760), (1560, 1900)):
        x = x0
        while x < x1:
            w = rnd.randint(14, 36); h = rnd.randint(14, 70)
            body += f'<rect x="{x}" y="{HZ - h}" width="{w}" height="{h + 4}" fill="#8fb0c4" opacity=".75"/>'
            x += w + rnd.randint(3, 16)
    body += f'<rect y="{HZ}" width="1920" height="{1080 - HZ}" fill="url(#bSand)"/>'
    body += f'<path d="M0 {HZ + 10} Q300 {HZ - 30} 700 {HZ + 20} T1400 {HZ} T1920 {HZ + 10} V1080 H0Z" fill="#f2b468"/>'
    body += f'<path d="M0 {HZ + 10} Q300 {HZ - 30} 700 {HZ + 20} T1400 {HZ} T1920 {HZ + 10}" fill="none" stroke="#fff0c8" stroke-width="4" opacity=".7"/>'
    # wind ripples in the sand
    for k in range(26):
        y = HZ + 50 + k * 13 + rnd.randint(-4, 4); x = rnd.randint(-100, 1700); w = rnd.randint(160, 420)
        body += f'<path d="M{x} {y} q{w / 2} -10 {w} 0" fill="none" stroke="#c97c3c" stroke-width="3" opacity=".35"/>'
        body += f'<path d="M{x} {y - 4} q{w / 2} -10 {w} 0" fill="none" stroke="#ffe0a8" stroke-width="2" opacity=".45"/>'

    # ---- tower on a pair of snowshoes ----
    cx, base, H, W = 1210, 870, 830, 360
    shoes = ''
    shoes += f'<ellipse cx="{cx}" cy="{base + 16}" rx="430" ry="70" fill="#9a5a26" opacity=".35" filter="url(#blur14)"/>'
    shoes += snowshoe(cx - 225, base + 50, 480, 300, 180 + 24, 'bs1')
    shoes += snowshoe(cx + 225, base + 50, 480, 300, 180 - 24, 'bs2')
    body += shoes
    d2, b2 = tower(cx, base, H, W, dict(
        faces=[('#6d8eb3', '#bfe0f5'), ('#86a8cc', '#dff1fb'), ('#9ec0de', '#f0fbff'), ('#b8d6ec', '#ffffff')],
        edge='#22344e', rim='#ffffff', rimside='R', band='#3d5a7c', line='#2c4766', glow='#fff3c4', glowop=.55), 'bT')
    d += d2; body += b2
    # binding straps over the tower base (it "wears" the snowshoes)
    for sx in (-1, 1):
        x = cx + sx * 110
        body += f'<path d="M{x - 80} {base + 6} q80 -40 160 0" fill="none" stroke="#3a210a" stroke-width="26" stroke-linecap="round"/>'
        body += f'<path d="M{x - 80} {base + 6} q80 -40 160 0" fill="none" stroke="#b3462e" stroke-width="16" stroke-linecap="round"/>'
        body += f'<rect x="{x - 14}" y="{base - 26}" width="28" height="20" rx="3" fill="#e0c060" stroke="#3a210a" stroke-width="3"/>'
    # barely a dent: light sand puffs around the shoes, no sinking
    for (x, y) in ((cx - 440, base + 60), (cx + 450, base + 56), (cx, base + 150)):
        body += f'<ellipse cx="{x}" cy="{y}" rx="38" ry="10" fill="#fff0c8" opacity=".6" filter="url(#blur4)"/>'

    # ---- a high heel sinking deep into the sand ----
    hx, hy = 630, 905
    d += lin('bLip', [(0, '#efad62'), (.55, '#e09a52'), (1, '#d38a46')])
    d += lin('bHeel', [(0, '#ff7a7a'), (.45, '#e0303e'), (1, '#8e1b25')])
    body += f'<ellipse cx="{hx}" cy="{hy + 6}" rx="210" ry="40" fill="#8a4a1c"/>'
    body += f'<ellipse cx="{hx}" cy="{hy + 2}" rx="180" ry="28" fill="#5e2f10"/>'
    heel = f'<g transform="translate({hx - 10} {hy + 10}) rotate(14) scale(1.5)">'
    heel += ('<path d="M-150 -4 Q-160 -40 -110 -44 L-50 -44 Q30 -60 70 -150 Q86 -184 104 -168 L108 -150 L98 30 L84 30 L80 -110 '
             'Q20 -100 -40 -6 L-140 8 Q-160 8 -150 -4Z" fill="url(#bHeel)" stroke="#3b0c12" stroke-width="5" stroke-linejoin="round"/>')
    heel += '<path d="M-50 -44 Q30 -60 70 -150 Q86 -184 104 -168 Q60 -120 -50 -44Z" fill="#5a0f18" stroke="#3b0c12" stroke-width="3"/>'
    heel += '<path d="M-130 -26 Q-110 -40 -60 -40" fill="none" stroke="#ffd6d6" stroke-width="7" stroke-linecap="round" opacity=".85"/>'
    heel += '<path d="M-20 -30 Q20 -50 50 -100" fill="none" stroke="#ff9a9a" stroke-width="5" stroke-linecap="round" opacity=".7"/>'
    heel += '</g>'
    body += heel
    # front lip of sand swallowing the heel and the toe
    lip = (f'M{hx - 280} {hy + 64} Q{hx - 230} {hy - 6} {hx - 150} {hy + 12} Q{hx - 60} {hy + 36} {hx + 40} {hy + 22} Q{hx + 140} {hy + 4} {hx + 200} {hy + 14} '
           f'Q{hx + 260} {hy + 24} {hx + 290} {hy + 64}')
    body += f'<path d="{lip} Q{hx} {hy + 150} {hx - 280} {hy + 64}Z" fill="url(#bLip)"/>'
    body += f'<path d="{lip}" fill="none" stroke="#ffe0a8" stroke-width="5" stroke-linecap="round"/>'
    for k in range(11):   # sand spray
        a = math.radians(195 + k * 15); r = rnd.randint(170, 240)
        body += f'<circle cx="{hx + math.cos(a) * r:.0f}" cy="{hy - 10 + math.sin(a) * r * .5:.0f}" r="{rnd.randint(5, 10)}" fill="#f6c27a" stroke="#b56d2e" stroke-width="2"/>'
    # little "sinking" motion marks
    for k in (-1, 1):
        body += f'<path d="M{hx + k * 230} {hy - 120} q{-k * 10} 40 0 70" fill="none" stroke="#ffffff" stroke-width="7" stroke-linecap="round" opacity=".85"/>'
    # ---- frog on its own little snowshoes, looking at the sinking heel ----
    fx, fy, fs = 215, 1000, 2.9
    cap = ('<path d="M-26 -76 q32 -30 62 0 z" fill="#2f6fa8" stroke-width="3"/><path d="M30 -78 q24 -2 34 6 q-16 6 -36 2z" fill="#2f6fa8" stroke-width="3"/>'
           '<circle cx="5" cy="-92" r="4" fill="#F2D27A" stroke-width="2"/>')
    body += frog(fx, fy, fs, look=(4, 2), mouth='o', armL='M-34 -24 q-20 -4 -26 -26', armR='M38 -22 q24 -8 30 -30', top=cap)
    for (x, y, s) in ((cx - 300, 380, 22), (cx + 330, 300, 26), (cx + 290, 620, 18), (760, 640, 16)):
        body += spark(x, y, s, '#ffffff', .95)
    return page('#1f7fc4', svg(d, body), [(116, [('THE SECRET:', 'w')]), (176, [('SNOWSHOES', 'y')])], outline='#10203a')


# =========================== C: the wind monster ===========================
def make_C():
    rnd = random.Random(5); d = FILTERS; HZ = 850
    d += lin('cSky', [(0, '#0c2230'), (.4, '#1d4b5a'), (.75, '#4f7f78'), (1, '#e0a65c')])
    d += lin('cGnd', [(0, '#b07a3c'), (.3, '#7a4f28'), (1, '#2e1d10')])
    body = f'<rect width="1920" height="{HZ}" fill="url(#cSky)"/>'
    body += f'<ellipse cx="1400" cy="520" rx="520" ry="520" fill="#ffd38a" opacity=".35" filter="url(#blur60)"/>'
    # storm cloud bank and dust haze
    for k in range(16):
        x = rnd.randint(-100, 2000); y = rnd.randint(-40, 160)
        body += f'<ellipse cx="{x}" cy="{y}" rx="{rnd.randint(160, 320)}" ry="{rnd.randint(50, 90)}" fill="#0a1a24" opacity=".55" filter="url(#blur14)"/>'
    body += f'<rect y="{HZ - 120}" width="1920" height="140" fill="#e0a65c" opacity=".35" filter="url(#blur30)"/>'
    for x0, x1 in ((900, 1180), (1640, 1900)):
        x = x0
        while x < x1:
            w = rnd.randint(14, 34); h = rnd.randint(16, 80)
            body += f'<rect x="{x}" y="{HZ - h}" width="{w}" height="{h + 4}" fill="#5e6a62" opacity=".7"/>'
            x += w + rnd.randint(3, 14)
    body += f'<rect y="{HZ}" width="1920" height="{1080 - HZ}" fill="url(#cGnd)"/>'
    body += f'<path d="M0 {HZ + 30} Q500 {HZ - 10} 1000 {HZ + 40} T1920 {HZ + 20} V1080 H0Z" fill="#6a4423"/>'
    body += f'<path d="M0 {HZ + 30} Q500 {HZ - 10} 1000 {HZ + 40} T1920 {HZ + 20}" fill="none" stroke="#f0b870" stroke-width="3" opacity=".6"/>'

    # ---- tower ----
    cx, base, H, W = 1440, 990, 950, 380
    d2, b2 = tower(cx, base, H, W, dict(
        faces=[('#3f6070', '#9fc2c8'), ('#557a86', '#cfe6e2'), ('#2f4b5a', '#7fa3aa'), ('#223a48', '#5f8590')],
        edge='#0c1a22', rim='#ffd890', rimside='L', band='#132a36', line='#122833', glow='#ffd38a', glowop=.5), 'cT')
    d += d2

    # ---- wind streams from the monster's mouth to the tower ----
    mx, my = 540, 690          # monster centre
    streams = ''
    d += lin('cStr', [(0, '#ffffff'), (.7, '#dff3f5'), (1, '#dff3f5')], x2=1, y2=0)
    for k, (y0, y1, w, op) in enumerate(((690, 300, 60, .55), (715, 450, 80, .6), (740, 600, 90, .7), (765, 750, 76, .6), (790, 880, 56, .5))):
        x0 = mx + 210
        pth = f'M{x0} {y0} C{x0 + 240} {y0 - 10} {cx - 420} {y1} {cx - W * .2} {y1}'
        streams += f'<path d="{pth}" fill="none" stroke="#e8f7f8" stroke-width="{w}" stroke-linecap="round" opacity="{op * .45}" filter="url(#blur14)"/>'
        streams += f'<path d="{pth}" fill="none" stroke="#f4fcfc" stroke-width="{w * .3:.0f}" stroke-linecap="round" opacity="{op * .9}" filter="url(#blur2)" stroke-dasharray="{rnd.randint(140, 220)} {rnd.randint(30, 50)}"/>'
        streams += f'<path d="{pth}" fill="none" stroke="#ffffff" stroke-width="5" stroke-linecap="round" opacity=".9" stroke-dasharray="{rnd.randint(60, 120)} {rnd.randint(60, 120)}" stroke-dashoffset="{rnd.randint(0, 80)}"/>'
    # blast cone from the mouth
    streams += f'<path d="M{mx + 200} {my + 70} L{mx + 520} {my - 40} L{mx + 540} {my + 200}Z" fill="#ffffff" opacity=".35" filter="url(#blur14)"/>'
    body += streams
    body += b2
    # ---- broken into small soft eddies all around the tower (at different heights, different directions) ----
    ed = ''
    def wisp(x, y, s, a, op=.85, col='#fff3d6'):
        # an open, tapering curl with a tail (not a closed ring)
        return (f'<g transform="translate({x:.0f} {y:.0f}) rotate({a}) scale({s})" opacity="{op}">'
                f'<path d="M-110 8 C-70 10 -30 6 0 -10 C16 -20 14 -38 -2 -36" fill="none" stroke="{col}" stroke-width="20" stroke-linecap="round" opacity=".28" filter="url(#blur4)"/>'
                f'<path d="M-110 8 C-70 10 -30 6 0 -10 C16 -20 14 -38 -2 -36" fill="none" stroke="{col}" stroke-width="6" stroke-linecap="round"/>'
                f'<path d="M-150 22 C-130 22 -120 20 -100 18" fill="none" stroke="{col}" stroke-width="3" stroke-linecap="round" opacity=".5"/></g>')
    spots = []
    for h in [i / 15 for i in range(1, 13)]:
        y = base - h * H * .8
        hwR = stepv(RST, h * .8) * W; hwL = stepv(LST, h * .8) * W
        spots.append((cx + hwR + rnd.randint(30, 120), y + rnd.randint(-20, 20), rnd.uniform(.6, 1.0), rnd.choice([-25, 0, 15, -50, 30, 200])))
        if rnd.random() < .7:
            spots.append((cx + hwR + rnd.randint(150, 290), y + rnd.randint(-30, 30), rnd.uniform(.45, .75), rnd.choice([-40, 10, 25, 190])))
        if h < .85 and rnd.random() < .55:
            spots.append((cx - hwL - rnd.randint(10, 60), y - rnd.randint(30, 60), rnd.uniform(.4, .6), rnd.choice([-70, -110, 250])))
    for (x, y, s, a) in spots:
        if x > 1780 and y > 860: continue
        ed += wisp(x, y, s * 1.15, a, .9, '#ffffff')
        ed += f'<circle cx="{x}" cy="{y}" r="{26 * s}" fill="#ffe3a8" opacity=".25" filter="url(#blur8)"/>'
    body += ed

    # ---- the wind monster: a round swirling cloud with a face, puffing ----
    mon = ''
    d += rad('cMon', mx - 40, my - 60, 300, [(0, '#ffffff', 1), (.55, '#dfeef3', 1), (.85, '#a9c3d4', 1), (1, '#7f97b8', 1)])
    mon += f'<ellipse cx="{mx}" cy="{my}" rx="300" ry="280" fill="#bfe6ff" opacity=".35" filter="url(#blur30)"/>'
    # tornado tail down to the ground
    mon += f'<path d="M{mx - 170} {my + 200} C{mx - 150} {my + 320} {mx - 40} {my + 300} {mx - 30} {1050} L{mx + 20} {1050} C{mx + 40} {my + 300} {mx + 110} {my + 300} {mx + 120} {my + 210}Z" fill="#c9dbe6" stroke="#2a3a55" stroke-width="6"/>'
    # vortex arms spinning round the body
    for k, (r, a0, w) in enumerate(((330, 200, 26), (300, 20, 20), (360, 120, 14))):
        a1 = math.radians(a0); a2 = math.radians(a0 + 110)
        p0 = (mx + r * math.cos(a1), my + r * .9 * math.sin(a1)); p1 = (mx + (r - 60) * math.cos(a2), my + (r - 60) * .9 * math.sin(a2))
        arc = f'M{p0[0]:.0f} {p0[1]:.0f} A{r} {r * .9} 0 0 1 {p1[0]:.0f} {p1[1]:.0f}'
        mon += f'<path d="{arc}" fill="none" stroke="#e8f7ff" stroke-width="{w * 2}" stroke-linecap="round" opacity=".35" filter="url(#blur8)"/>'
        mon += f'<path d="{arc}" fill="none" stroke="#ffffff" stroke-width="{w * .55:.0f}" stroke-linecap="round" opacity="1"/>'
    for k in range(10):   # sand grains and a leaf caught in the swirl
        a = math.radians(rnd.randint(0, 360)); r = rnd.randint(280, 360)
        mon += f'<circle cx="{mx + r * math.cos(a):.0f}" cy="{my + r * .85 * math.sin(a):.0f}" r="{rnd.randint(4, 8)}" fill="#e0b070" stroke="#6a4423" stroke-width="2"/>'
    for k in range(4):
        y = my + 230 + k * 40
        mon += f'<path d="M{mx - 120 + k * 18} {y} q60 18 {150 - k * 30} -6" fill="none" stroke="#7f97b8" stroke-width="5" opacity=".7"/>'
    mon += f'<ellipse cx="{mx - 70}" cy="{HZ + 120}" rx="120" ry="26" fill="#d9a560" opacity=".8" filter="url(#blur4)"/>'
    # puffy body (overlapping cloud lobes)
    lobes = [(-190, 30, 120), (-120, -150, 120), (40, -180, 112), (190, -80, 120), (160, 110, 115), (-30, 170, 120), (-200, 150, 95), (0, 0, 220)]
    for (ox, oy, r) in lobes:
        mon += f'<circle cx="{mx + ox}" cy="{my + oy}" r="{r}" fill="url(#cMon)" stroke="#2a3a55" stroke-width="7"/>'
    for (ox, oy, r) in lobes:
        mon += f'<circle cx="{mx + ox}" cy="{my + oy}" r="{r - 3}" fill="url(#cMon)"/>'
    # spiral swirl lines on the body
    sp = ''
    for k in range(3):
        r0 = 70 + k * 60
        sp += f'<path d="M{mx - r0} {my + 20} A{r0} {r0 * .9} 0 1 1 {mx + r0 * .7} {my + r0 * .7}" fill="none" stroke="#7f97c4" stroke-width="{12 - k * 3}" opacity=".75" stroke-linecap="round"/>'
    mon += sp
    # face: angry-funny brows, big eyes looking at the tower, puffed cheeks, pursed blowing mouth on the right
    ex, ey = mx + 10, my - 60
    for dx in (-70, 50):
        mon += f'<ellipse cx="{ex + dx}" cy="{ey}" rx="44" ry="52" fill="#ffffff" stroke="#1b2540" stroke-width="7"/>'
        mon += f'<circle cx="{ex + dx + 18}" cy="{ey + 8}" r="22" fill="#1b2540"/><circle cx="{ex + dx + 26}" cy="{ey}" r="7" fill="#ffffff"/>'
    mon += f'<path d="M{ex - 125} {ey - 80} Q{ex - 70} {ey - 110} {ex - 20} {ey - 62}" fill="none" stroke="#1b2540" stroke-width="16" stroke-linecap="round"/>'
    mon += f'<path d="M{ex + 10} {ey - 62} Q{ex + 60} {ey - 112} {ex + 110} {ey - 84}" fill="none" stroke="#1b2540" stroke-width="16" stroke-linecap="round"/>'
    mon += f'<ellipse cx="{ex + 150}" cy="{ey + 110}" rx="70" ry="58" fill="#ffd6e0" opacity=".85"/>'
    mon += f'<ellipse cx="{ex - 110}" cy="{ey + 100}" rx="58" ry="44" fill="#ffd6e0" opacity=".6"/>'
    mon += f'<ellipse cx="{mx + 190}" cy="{my + 70}" rx="34" ry="40" fill="#3b1b2e" stroke="#1b2540" stroke-width="7"/>'
    mon += f'<ellipse cx="{mx + 196}" cy="{my + 68}" rx="18" ry="24" fill="#7a3550"/>'
    mon += f'<path d="M{mx + 168} {my + 30} q22 -10 40 4" fill="none" stroke="#1b2540" stroke-width="6" stroke-linecap="round"/>'
    # highlight
    mon += f'<path d="M{mx - 240} {my - 60} q30 -110 140 -140" fill="none" stroke="#ffffff" stroke-width="14" stroke-linecap="round" opacity=".9"/>'
    body += mon
    # ---- frog with goggles, hugging a palm tree, scarf blowing toward the tower ----
    px, pyb = 960, 1015
    palm = f'<path d="M{px} {pyb} C{px + 10} {pyb - 120} {px + 40} {pyb - 220} {px + 90} {pyb - 300}" fill="none" stroke="#3a2412" stroke-width="38" stroke-linecap="round"/>'
    palm += f'<path d="M{px} {pyb} C{px + 10} {pyb - 120} {px + 40} {pyb - 220} {px + 90} {pyb - 300}" fill="none" stroke="#8a5a2b" stroke-width="26" stroke-linecap="round"/>'
    for k in range(8):
        t = k / 8; y = pyb - 20 - t * 260; x = px + 4 + t * t * 80
        palm += f'<path d="M{x - 10} {y} q12 -8 22 0" fill="none" stroke="#5a3818" stroke-width="4"/>'
    tx, ty = px + 90, pyb - 300
    for (dx, dy) in ((210, 40), (230, -20), (180, 100), (150, -80), (110, 140), (60, -110)):   # fronds all blown toward the tower
        palm += f'<path d="M{tx} {ty} q{dx * .5} {dy * .5 - 50} {dx} {dy}" fill="none" stroke="#1e3b1a" stroke-width="22" stroke-linecap="round"/>'
        palm += f'<path d="M{tx} {ty} q{dx * .5} {dy * .5 - 50} {dx} {dy}" fill="none" stroke="#4f8a3c" stroke-width="13" stroke-linecap="round"/>'
    body += palm
    scarf = ('<path d="M-30 -30 q36 12 70 -2" fill="none" stroke="#1d2b1c" stroke-width="15" stroke-linecap="round"/>'
             '<path d="M-30 -30 q36 12 70 -2" fill="none" stroke="#c0443e" stroke-width="10" stroke-linecap="round"/>'
             '<path d="M34 -30 q20 -12 38 -2 q14 -12 30 -4 q-14 14 -32 10 q-16 8 -36 -4z" fill="#c0443e" stroke-width="3"/>'
             '<path d="M48 -26 l5 -5 M64 -24 l5 -5 M84 -22 l5 -5" stroke="#F2D27A" stroke-width="3"/>')
    gog = ('<path d="M-26 -84 q32 -14 62 0" fill="none" stroke="#5a3a1a" stroke-width="7"/>'
           '<circle cx="-8" cy="-86" r="10" fill="#7fd6e6" stroke-width="3.5"/><circle cx="22" cy="-86" r="10" fill="#7fd6e6" stroke-width="3.5"/>'
           '<path d="M-12 -90 l6 -2 M18 -90 l6 -2" stroke="#ffffff" stroke-width="2.5"/>')
    body += frog(px - 135, pyb, 2.9, look=(-4, -2), mouth='o', rot_=4, armL='M-34 -24 q-22 -10 -24 -40', armR='M40 -30 q14 -6 12 -26',
                 feet=((-24, 4, -10), (24, 2, 10)), front=scarf, top=gog)
    for (x, y, s) in ((cx - 260, 230, 22), (cx + 300, 160, 18), (860, 420, 18)):
        body += spark(x, y, s, '#fff4d6', .9)
    return page('#0c2230', svg(d, body), [(176, [('CONFUSE', 'w')]), (176, [('THE ', 'w'), ('WIND', 'y')])], outline='#06121a')


if __name__ == '__main__':
    for n, f in (('A', make_A), ('B', make_B), ('C', make_C)):
        open(os.path.join(HERE, f'{n}.html'), 'w').write(f())
    print('ok')
