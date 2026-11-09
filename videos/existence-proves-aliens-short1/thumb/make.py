# Shorts thumbnails (style B, guideline 16-9 / 16-8, brief tools/briefs/thumb_art.md) for existence-proves-aliens-short1..5.
# VERTICAL 1080x1920: one glowing concrete hero in the top half, centred 2-4 word hook on a darkband (y 860-1240), frog in a bottom corner.
# Run: python3 videos/existence-proves-aliens-short1/thumb/make.py [1 2 3 4 5] -> videos/existence-proves-aliens-shortN/thumb/A.html
# 1 ZERO BECAME ONE    glowing cupped hand holding a scoop of wet sand with a tiny crab, spiral galaxy behind; beach frog with bucket (short1 S04 zero->one, S08 scoop of sand)
# 2 100,000 YEARS AGO  telescope view of glowing ice-age Earth: woolly mammoth, glaciers, aurora, early humans at a fire; alien astronomer + helmet frog (short2 S06-S07)
# 3 LIFE IN THE DARK   black-smoker vent under an icy-moon ceiling, glowing microbes + tube worms; diving frog with lamp (short3 S02-S04, S07)
# 4 FIRST TO ARRIVE?   cosmic clock just past twelve, the first star igniting at its centre; early-bird frog with party hat on a young rock (short4 S04, S08, S11; hedged "?")
# 5 MADE OF STARS      human bust made of supernova debris (Fe, Ca, C glowing inside), supernova bursting behind; frog looking at its sparkling hand (short5 S02-S06)
import os, sys, math, random, shutil, importlib.util
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
sys.path.insert(0, os.path.join(REPO, 'tools'))
_spec = importlib.util.spec_from_file_location('trilo_make', os.path.join(REPO, 'videos', 'trilobite-extinction', 'thumb', 'make.py'))
_m = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(_m)
frog, FILTERS, INK, GREEN = _m.frog, _m.FILTERS, _m.INK, _m.GREEN   # shared posable frog (eye white #f4f5ea; keep look small so the pupil stays inside)
from thumb_lib import vpage, vsvg, lin, rad, spark, fireflies, halo, darkband

W, H = 1080, 1920
SPACE_HELMET = ('<circle cx="6" cy="-58" r="47" fill="#cfefff" fill-opacity=".13" stroke="#e8f0f8" stroke-width="5"/>'
                '<path d="M-26 -86 q12 -18 32 -21" stroke="#fff" stroke-width="5" fill="none" opacity=".85"/><path d="M44 -44 q6 -10 6 -22" stroke="#fff" stroke-width="3" fill="none" opacity=".5"/>'
                '<ellipse cx="6" cy="-13" rx="42" ry="9" fill="#d8dee6" stroke-width="3.2"/>')


def poly(pts):
    return 'M' + ' L'.join(f'{x:.1f} {y:.1f}' for x, y in pts) + 'Z'


def vig(id='vig', a=.75):
    return rad(id, 540, 960, 1250, [(0, '#000', 0), (.5, '#000', 0), (1, '#000', a)])


def starfield(rnd, n, y0=0, y1=H, col='#e8f4ff'):
    return ''.join(f'<circle cx="{rnd.uniform(0, W):.0f}" cy="{rnd.uniform(y0, y1):.0f}" r="{rnd.choice([1.2, 1.8, 2.6])}" fill="{col}" opacity="{rnd.uniform(.2, .8):.2f}"/>' for _ in range(n))


def save(n, bg, d, b, lines, outline, top):
    out = os.path.join(REPO, 'videos', f'existence-proves-aliens-short{n}', 'thumb'); os.makedirs(out, exist_ok=True)
    for f in ('common.css', 'Fredoka-700.woff2'):
        shutil.copy(os.path.join(REPO, 'tools', 'assets', 'thumb_v', f), out)
    open(os.path.join(out, 'A.html'), 'w').write(vpage(bg, vsvg(d, b), lines, outline=outline, top=top))


def galaxy(rnd, cx, cy, R, rot=-22, squash=.42, cols=('#bff4ff', '#ffffff', '#ffc8f0', '#fff0b0')):
    """two-armed spiral galaxy of dots, tilted"""
    ca, sa = math.cos(math.radians(rot)), math.sin(math.radians(rot)); o = ''
    def P(x, y):
        y *= squash; return cx + x * ca - y * sa, cy + x * sa + y * ca
    for arm in (0, math.pi):
        for i in range(420):
            t = i / 420 * 3.4 * math.pi; r = R * (.08 + .92 * i / 420)
            a = t * .55 + arm + rnd.gauss(0, .12); rr = r + rnd.gauss(0, R * .05)
            x, y = P(rr * math.cos(a), rr * math.sin(a))
            o += f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{rnd.choice([1.4, 2, 2.8, 3.6])}" fill="{rnd.choice(cols)}" opacity="{rnd.uniform(.35, .95):.2f}"/>'
    return o


# ================= 1: ZERO BECAME ONE =================
def make_1():
    rnd = random.Random(101)
    d = FILTERS + rad('bg1', 540, 420, 1500, [(0, '#16305a', 1), (.35, '#0a1430', 1), (1, '#02040c', 1)]) + vig()
    d += halo('h1', 560, 560, 560, inner='#fff3c0', outer='#5fd8ff')
    d += lin('skin1', [(0, '#ffd9b8'), (.5, '#e9a57c'), (1, '#9a5a3e')])
    d += lin('sand1', [(0, '#f6d48a'), (.5, '#c99a52'), (1, '#7a5a2e')])
    d += lin('beach1', [(0, '#3a3a5a'), (.3, '#2a2840'), (1, '#0c0a14')])
    d += lin('sea1', [(0, '#123a5a'), (1, '#06182a')])
    b = f'<rect width="{W}" height="{H}" fill="url(#bg1)"/>' + starfield(rnd, 140, 0, 1300)
    # galaxy behind the hand
    b += '<ellipse cx="540" cy="330" rx="470" ry="210" transform="rotate(-22 540 330)" fill="#7fdcff" opacity=".22" filter="url(#b50)"/>'
    b += galaxy(rnd, 540, 330, 430)
    b += '<ellipse cx="540" cy="330" rx="110" ry="54" transform="rotate(-22 540 330)" fill="#fff3c0" opacity=".9" filter="url(#b24)"/><ellipse cx="540" cy="330" rx="46" ry="24" transform="rotate(-22 540 330)" fill="#fffbe8"/>'
    b += f'<ellipse cx="560" cy="600" rx="560" ry="420" fill="url(#h1)"/>'
    # cupped right hand, palm up, wrist off the right edge
    under = 'M1120 690 C1000 690 900 700 830 712 L330 742 C280 746 250 770 262 800 C280 832 360 842 470 842 C640 842 820 838 1120 836Z'
    b += f'<path d="{under}" fill="#ffd27a" opacity=".55" filter="url(#b24)"/>'
    b += f'<path d="{under}" fill="url(#skin1)" stroke="#2a1408" stroke-width="7"/>'
    b += '<path d="M300 828 C420 846 700 842 1100 834" stroke="#7a3a24" stroke-width="5" fill="none" opacity=".5"/>'
    # sand scoop (wet: dark patches + shine)
    mound = 'M330 742 C340 640 420 560 540 548 C660 540 760 600 820 712Z'
    b += f'<path d="{mound}" fill="url(#sand1)" stroke="#3a2610" stroke-width="6"/>'
    for _ in range(70):
        x, y = rnd.uniform(380, 790), rnd.uniform(590, 735)
        b += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{rnd.choice([2, 3, 4])}" fill="{rnd.choice(["#7a5a2e", "#fff0c0", "#a07a40"])}" opacity=".7"/>'
    for x, y, rx in ((450, 690, 60), (690, 680, 54), (580, 720, 70)):
        b += f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="16" fill="#6a4a22" opacity=".45"/><path d="M{x - rx * .6:.0f} {y - 6} q{rx * .6:.0f} -10 {rx * 1.1:.0f} 0" stroke="#fff6dc" stroke-width="3" fill="none" opacity=".8"/>'
    # tiny crab on top of the sand
    CX, CY = 556, 552
    cr = f'<g transform="translate({CX} {CY})" stroke="#3a0a06" stroke-width="5" stroke-linecap="round" stroke-linejoin="round">'
    cr += '<ellipse cx="0" cy="-20" rx="110" ry="70" fill="#ffb070" opacity=".5" stroke="none" filter="url(#b24)"/>'
    for s in (-1, 1):
        for k in range(3):
            cr += f'<path d="M{s * 40} {-10 + k * 8} q{s * 34} {-6 + k * 6} {s * 50} {18 + k * 6}" fill="none" stroke-width="9"/><path d="M{s * 40} {-10 + k * 8} q{s * 34} {-6 + k * 6} {s * 50} {18 + k * 6}" fill="none" stroke="#f0703a" stroke-width="4"/>'
        cr += f'<path d="M{s * 38} -30 q{s * 26} -26 {s * 40} -58" fill="none" stroke-width="11"/><path d="M{s * 38} -30 q{s * 26} -26 {s * 40} -58" fill="none" stroke="#f0703a" stroke-width="5"/>'
        cr += f'<path d="M{s * 78} -88 q{s * 30} -6 {s * 22} 22 q{s * -10} 4 {s * -16} -4 q{s * 6} -4 {s * 4} -10 q{s * -8} 2 {s * -10} -8z" fill="#ff7a3e"/>'
        cr += f'<path d="M{s * 12} -40 L{s * 18} -66" stroke-width="5"/><circle cx="{s * 18}" cy="-72" r="9" fill="#fff"/><circle cx="{s * 19}" cy="-72" r="4.5" fill="#1a0604" stroke="none"/>'
    cr += '<ellipse cx="0" cy="-18" rx="46" ry="30" fill="#ff7a3e"/><path d="M-30 -30 q30 -16 60 0" stroke="#ffd0a8" stroke-width="4" fill="none"/><path d="M-10 -6 q10 6 20 0" stroke-width="3.5" fill="none"/>'
    b += cr + '</g>'
    # curled fingers (left) and thumb (front), drawn over the sand
    for k, (bx, tx, ty) in enumerate(((300, 300, 610), (316, 336, 600), (330, 372, 606), (346, 404, 624))):
        fp = f'M{bx} 812 C{bx - 50} 760 {tx - 40} {ty + 30} {tx} {ty}'
        b += f'<path d="{fp}" stroke="#2a1408" stroke-width="54" fill="none" stroke-linecap="round"/><path d="{fp}" stroke="url(#skin1)" stroke-width="42" fill="none" stroke-linecap="round"/>'
        b += f'<path d="M{tx - 10} {ty - 6} q12 -6 18 6" stroke="#ffe8d4" stroke-width="5" fill="none" opacity=".8"/>'
    thumb = 'M900 760 C820 720 700 700 610 694 C580 692 570 720 600 730 C690 744 790 770 880 806Z'
    b += f'<path d="{thumb}" fill="url(#skin1)" stroke="#2a1408" stroke-width="7"/><path d="M612 700 q-14 10 -6 22" stroke="#ffe8d4" stroke-width="5" fill="none"/>'
    b += '<path d="M640 702 C720 708 800 726 880 760" stroke="#ffe8d4" stroke-width="4" fill="none" opacity=".7"/>'
    # rim light on the hand
    b += '<path d="M262 800 C280 832 360 842 470 842 C640 842 820 838 1080 836" stroke="#9ff0ff" stroke-width="5" fill="none" opacity=".8"/>'
    for sx, sy, ss in ((300, 470, 24), (820, 520, 30), (720, 420, 16), (420, 500, 18), (900, 640, 20), (200, 650, 14)):
        b += spark(sx, sy, ss, col='#fffbe0')
    b += fireflies(40, 140, 840, col='#9ff0ff', core='#efffff', seed=13)
    b += darkband(860, 1240, .5)
    # night beach below: glowing surf + footprints
    b += f'<rect y="1290" width="{W}" height="200" fill="url(#sea1)"/>'
    for k, y in enumerate((1330, 1380, 1430, 1470)):
        wv = f'M-20 {y} ' + ' '.join(f'q60 {-14 - k * 2} 120 0' for _ in range(10))
        b += f'<path d="{wv}" stroke="#7ff5ff" stroke-width="{3 + k}" fill="none" opacity="{.35 + k * .12:.2f}"/>'
    b += f'<path d="M-20 1490 q300 -30 560 -6 q300 22 560 -10 L{W} {H} L0 {H}Z" fill="url(#beach1)"/>'
    b += '<path d="M-20 1490 q300 -30 560 -6 q300 22 560 -10" stroke="#bffcff" stroke-width="6" fill="none" opacity=".7" filter="url(#b3)"/>'
    for k in range(7):
        x, y = 980 - k * 70, 1840 - k * 46
        b += f'<ellipse cx="{x + (14 if k % 2 else -14)}" cy="{y}" rx="16" ry="26" transform="rotate(-50 {x} {y})" fill="#0a0812" opacity=".7"/>'
    for x, y in ((760, 1560), (880, 1640), (640, 1700)):
        b += f'<circle cx="{x}" cy="{y}" r="5" fill="#fff6d0" opacity=".8"/>'
    # beach frog with a bucket of sand, looking up at the scoop
    pail = ('<path d="M44 -40 L48 -6 L80 -6 L84 -40Z" fill="#e85a4a" stroke-width="3.4"/><ellipse cx="64" cy="-40" rx="20" ry="6" fill="#f6d48a" stroke-width="3"/>'
            '<path d="M46 -38 q18 -30 36 0" fill="none" stroke-width="3"/>')
    b += '<ellipse cx="260" cy="1640" rx="230" ry="190" fill="#9ff0ff" opacity=".13" filter="url(#b24)"/>'
    b += frog(250, 1770, 3.3, look=(3, -4), mouth='O', shadow=True, front=pail, armR='M38 -22 q14 -2 22 -20', armL='M-34 -22 q-20 -14 -24 -44')
    b += f'<rect width="{W}" height="{H}" fill="url(#vig)"/>'
    save(1, '#02040c', d, b, [('ZERO BECAME', 122, 'w'), ('ONE', 236, 'y')], '#02060f', 866)


# ================= 2: 100,000 YEARS AGO =================
def mammoth(x, y, s):
    g = f'<g transform="translate({x} {y}) scale({s})" stroke="#1a0c06" stroke-width="5" stroke-linejoin="round" stroke-linecap="round">'
    for lx, sh in ((-40, '#4a2a16'), (95, '#4a2a16')):
        g += f'<path d="M{lx} -10 L{lx - 4} 78 L{lx + 34} 78 L{lx + 36} -10Z" fill="{sh}"/>'
    g += '<path d="M-140 -60 C-172 -150 -120 -218 -60 -206 C0 -200 90 -172 126 -112 C150 -72 146 -22 132 10 L-104 12 C-132 -6 -140 -30 -140 -60Z" fill="#8a5432"/>'
    for lx in (-100, 50):
        g += f'<path d="M{lx} -10 L{lx - 4} 82 L{lx + 38} 82 L{lx + 40} -10Z" fill="#7a4628"/><path d="M{lx - 6} 80 l8 -12 l8 12 l8 -12 l8 12 l8 -12" stroke="#2a160a" fill="none" stroke-width="3"/>'
    for k in range(30):   # shaggy fringe
        fx = -120 + k * 8.5
        g += f'<path d="M{fx} 4 q-3 22 3 {34 + (k % 3) * 8}" stroke="#5a3018" stroke-width="5" fill="none"/>'
    for k in range(10):
        g += f'<path d="M{-80 + k * 18} -150 q8 20 0 40" stroke="#b07a4a" stroke-width="3" fill="none" opacity=".8"/>'
    g += '<path d="M-130 -150 C-110 -200 -40 -214 30 -194 C80 -180 118 -140 128 -110" stroke="#c8fff0" stroke-width="5" fill="none" opacity=".75"/>'
    g += '<path d="M-148 -96 C-186 -60 -182 0 -172 48 C-166 76 -144 80 -140 62" fill="none" stroke-width="40"/><path d="M-148 -96 C-186 -60 -182 0 -172 48 C-166 76 -144 80 -140 62" fill="none" stroke="#7a4628" stroke-width="30"/>'
    g += '<path d="M-150 -62 C-210 -30 -226 30 -180 62" fill="none" stroke-width="20"/><path d="M-150 -62 C-210 -30 -226 30 -180 62" fill="none" stroke="#f4ecd4" stroke-width="12"/>'
    g += '<ellipse cx="-104" cy="-118" rx="22" ry="30" fill="#6a3a20"/><circle cx="-128" cy="-132" r="6" fill="#140804" stroke="none"/><circle cx="-126" cy="-134" r="2" fill="#fff" stroke="none"/>'
    return g + '</g>'


def make_2():
    rnd = random.Random(202)
    CX, CY, R = 540, 480, 330
    d = FILTERS + lin('bg2', [(0, '#0c0420'), (.5, '#1c0a3a'), (1, '#05020e')]) + vig()
    d += halo('h2', CX, CY, 560, inner='#e8fff8', outer='#5ff0d8')
    d += lin('icesky2', [(0, '#02122a'), (.55, '#0a3a5a'), (1, '#4a8aa8')])
    d += lin('snow2', [(0, '#eaf8ff'), (1, '#8ab4cc')])
    d += lin('ground2', [(0, '#3a1a4a'), (1, '#0c0614')])
    d += lin('tube2', [(0, '#d8dce8'), (.5, '#6a7088'), (1, '#2a2e40')], x2=1, y2=0)
    d += lin('beam2', [(0, '#9ff0ff', ), (1, '#9ff0ff')])
    d += f'<clipPath id="view2"><circle cx="{CX}" cy="{CY}" r="{R}"/></clipPath>'
    b = f'<rect width="{W}" height="{H}" fill="url(#bg2)"/>' + starfield(rnd, 160, 0, H, '#f0e8ff')
    b += '<path d="M-100 300 L1180 1100 L1180 1300 L-100 520Z" fill="#c8a8ff" opacity=".08" filter="url(#b50)"/>'
    # light beam from the alien telescope up to the view
    b += f'<path d="M700 1330 L790 1320 L{CX + 240} {CY + 160} L{CX - 120} {CY + 260}Z" fill="#9ff0ff" opacity=".12" filter="url(#b12)"/>'
    b += f'<ellipse cx="{CX}" cy="{CY}" rx="600" ry="560" fill="url(#h2)"/>'
    # the telescope view: ice-age Earth
    v = f'<rect x="{CX - R}" y="{CY - R}" width="{2 * R}" height="{2 * R}" fill="url(#icesky2)"/>'
    v += ''.join(f'<circle cx="{rnd.uniform(CX - R, CX + R):.0f}" cy="{rnd.uniform(CY - R, CY):.0f}" r="{rnd.choice([1.4, 2])}" fill="#fff" opacity=".7"/>' for _ in range(40))
    for k, (y0, col) in enumerate(((CY - 260, '#7affc0'), (CY - 210, '#5ff0ff'), (CY - 170, '#b08aff'))):
        au = f'M{CX - R} {y0 + 40} C{CX - 150} {y0 - 40} {CX + 60} {y0 + 70} {CX + R} {y0 - 10}'
        v += f'<path d="{au}" stroke="{col}" stroke-width="{46 - k * 10}" fill="none" opacity=".45" filter="url(#b12)"/><path d="{au}" stroke="#eafff4" stroke-width="3" fill="none" opacity=".6"/>'
    v += f'<path d="M{CX - R} {CY + 40} L{CX - 260} {CY - 70} L{CX - 190} {CY - 10} L{CX - 120} {CY - 110} L{CX - 30} {CY + 10} L{CX + 70} {CY - 90} L{CX + 170} {CY - 20} L{CX + 250} {CY - 130} L{CX + R} {CY + 20} L{CX + R} {CY + 120} L{CX - R} {CY + 120}Z" fill="#cfe8f6" stroke="#5a8aa8" stroke-width="4"/>'
    for px, py in ((CX - 120, CY - 110), (CX + 70, CY - 90), (CX + 250, CY - 130), (CX - 260, CY - 70)):
        v += f'<path d="M{px} {py} l-22 46 l14 -6 l8 18 l12 -20 l16 8z" fill="#ffffff"/>'
    v += f'<path d="M{CX - R} {CY + 70} Q{CX} {CY + 30} {CX + R} {CY + 80} L{CX + R} {CY + R} L{CX - R} {CY + R}Z" fill="url(#snow2)"/>'
    v += mammoth(CX + 60, CY + 120, .95)
    # campfire + two early humans with spears (left)
    fx, fy = CX - 210, CY + 190
    v += f'<circle cx="{fx}" cy="{fy - 16}" r="70" fill="#ffb040" opacity=".55" filter="url(#b12)"/>'
    v += f'<path d="M{fx - 18} {fy} q-4 -30 10 -50 q4 20 14 10 q4 22 -6 40z" fill="#ffd060" stroke="#7a2a06" stroke-width="3"/>'
    for hx, sp in ((fx - 60, -1), (fx + 52, 1)):
        v += (f'<g transform="translate({hx} {fy})" stroke="#140a06" stroke-linecap="round"><path d="M0 0 L0 -40" stroke-width="12"/><circle cx="0" cy="-50" r="9" fill="#3a2010" stroke-width="3"/>'
              f'<path d="M-6 0 l-6 20 M6 0 l6 20" stroke-width="7"/><path d="M{sp * 8} -34 L{sp * 22} -76" stroke-width="4"/><path d="M{sp * 22} -76 l{sp * 4} -10" stroke="#e8e8f0" stroke-width="5"/></g>')
    b += f'<g clip-path="url(#view2)">{v}</g>'
    # eyepiece rim with crosshair ticks
    b += f'<circle cx="{CX}" cy="{CY}" r="{R + 10}" fill="none" stroke="#04020a" stroke-width="30"/><circle cx="{CX}" cy="{CY}" r="{R + 10}" fill="none" stroke="#bfe8f0" stroke-width="8"/>'
    b += f'<circle cx="{CX}" cy="{CY}" r="{R + 26}" fill="none" stroke="#7ff5d8" stroke-width="4" opacity=".7"/>'
    for a in range(0, 360, 30):
        ca, sa = math.cos(math.radians(a)), math.sin(math.radians(a)); L = 26 if a % 90 == 0 else 14
        b += f'<path d="M{CX + (R - 4) * ca:.0f} {CY + (R - 4) * sa:.0f} L{CX + (R - 4 - L) * ca:.0f} {CY + (R - 4 - L) * sa:.0f}" stroke="#e8fff8" stroke-width="5" opacity=".85"/>'
    for sx, sy, ss in ((CX + 330, CY - 260, 26), (CX - 350, CY - 220, 18), (CX + 380, CY + 160, 16), (CX - 320, CY + 260, 20)):
        b += spark(sx, sy, ss, col='#effffa')
    b += fireflies(30, 140, 840, col='#9ff0ff', core='#efffff', seed=21)
    b += darkband(860, 1240, .5)
    # alien planet + telescope + alien astronomer below
    b += '<circle cx="160" cy="1380" r="60" fill="#ffb0d8" opacity=".9"/><circle cx="160" cy="1380" r="100" fill="#ff8ac8" opacity=".25" filter="url(#b24)"/><path d="M90 1380 q70 -30 140 0" stroke="#ffe0f0" stroke-width="6" fill="none" opacity=".7"/>'
    b += f'<path d="M-20 1600 q200 -60 420 -20 q240 40 420 -30 q160 -40 280 0 L{W} {H} L0 {H}Z" fill="url(#ground2)"/>'
    b += '<path d="M-20 1600 q200 -60 420 -20 q240 40 420 -30 q160 -40 280 0" stroke="#c8a8ff" stroke-width="4" fill="none" opacity=".6"/>'
    for x, y, r in ((520, 1700, 40), (680, 1820, 60), (980, 1760, 30)):
        b += f'<ellipse cx="{x}" cy="{y}" rx="{r}" ry="{r * .5:.0f}" fill="#24102e" stroke="#4a2a5a" stroke-width="3"/>'
    TX, TY = 830, 1630   # tripod head; tube points up-left at the view
    b += f'<path d="M{TX} {TY} L{TX - 90} 1820 M{TX} {TY} L{TX + 90} 1820 M{TX} {TY} L{TX + 10} 1840" stroke="#0a0614" stroke-width="16"/><path d="M{TX} {TY} L{TX - 90} 1820 M{TX} {TY} L{TX + 90} 1820 M{TX} {TY} L{TX + 10} 1840" stroke="#8a90a8" stroke-width="7"/>'
    b += (f'<g transform="translate({TX} {TY}) rotate(-106)"><rect x="-90" y="-36" width="420" height="72" rx="16" fill="url(#tube2)" stroke="#0a0614" stroke-width="7"/>'
          '<rect x="300" y="-46" width="50" height="92" rx="12" fill="#3a4058" stroke="#0a0614" stroke-width="7"/><ellipse cx="350" cy="0" rx="10" ry="40" fill="#9ff0ff" opacity=".9"/>'
          '<rect x="-130" y="-14" width="46" height="28" rx="6" fill="#3a4058" stroke="#0a0614" stroke-width="6"/><rect x="40" y="-38" width="20" height="76" fill="#c8a8ff" opacity=".7"/></g>')
    # alien astronomer at the eyepiece (eyepiece is at about TX+24, TY+120)
    AX, AY = 900, 1790
    b += (f'<g transform="translate({AX} {AY})" stroke="#0a1a14" stroke-width="5" stroke-linejoin="round" stroke-linecap="round">'
          '<path d="M-44 0 q-6 -90 44 -96 q50 6 44 96z" fill="#7ad8a8"/>'
          '<ellipse cx="-14" cy="-150" rx="58" ry="66" fill="#8ae8b8"/><path d="M-40 -206 q-20 -40 -40 -48 M10 -212 q14 -40 34 -44" fill="none"/><circle cx="-80" cy="-254" r="9" fill="#ffd0f0"/><circle cx="44" cy="-256" r="9" fill="#ffd0f0"/>'
          '<ellipse cx="-44" cy="-160" rx="20" ry="26" fill="#0a1a14" transform="rotate(20 -44 -160)"/><circle cx="-50" cy="-170" r="6" fill="#fff" stroke="none"/>'
          '<ellipse cx="8" cy="-164" rx="14" ry="20" fill="#0a1a14" transform="rotate(-10 8 -164)"/><circle cx="4" cy="-172" r="4" fill="#fff" stroke="none"/>'
          '<path d="M-36 -40 q-20 -60 -40 -86" fill="none" stroke-width="16"/><path d="M-36 -40 q-20 -60 -40 -86" fill="none" stroke="#7ad8a8" stroke-width="8"/></g>')
    b += '<ellipse cx="250" cy="1640" rx="230" ry="190" fill="#9ff0ff" opacity=".12" filter="url(#b24)"/>'
    b += frog(240, 1790, 3.2, look=(3, -4), mouth='O', shadow=True, mid=SPACE_HELMET, armR='M38 -22 q24 -10 30 -44', armL='M-34 -22 q-14 6 -16 22')
    b += f'<rect width="{W}" height="{H}" fill="url(#vig)"/>'
    save(2, '#05020e', d, b, [('100,000', 210, 'y'), ('YEARS AGO', 146, 'w')], '#05020e', 868)


# ================= 3: LIFE IN THE DARK =================
def worm(x, y, h, lean, s=1.0):
    top = (x + lean, y - h)
    p = f'M{x} {y} Q{x + lean * .2:.0f} {y - h * .6:.0f} {top[0]:.0f} {top[1]:.0f}'
    g = f'<path d="{p}" stroke="#2a1a14" stroke-width="{20 * s:.0f}" fill="none" stroke-linecap="round"/><path d="{p}" stroke="#ece4d0" stroke-width="{13 * s:.0f}" fill="none" stroke-linecap="round"/>'
    g += f'<circle cx="{top[0]:.0f}" cy="{top[1] - 10 * s:.0f}" r="{30 * s:.0f}" fill="#ff4a4a" opacity=".45" filter="url(#b6)"/>'
    for k in range(7):
        a = math.radians(-160 + k * 23)
        g += f'<path d="M{top[0]:.0f} {top[1]:.0f} q{10 * s * math.cos(a):.0f} {14 * s * math.sin(a) - 8 * s:.0f} {24 * s * math.cos(a):.0f} {22 * s * math.sin(a):.0f}" stroke="#e8203a" stroke-width="{8 * s:.0f}" fill="none" stroke-linecap="round"/>'
    g += f'<ellipse cx="{top[0]:.0f}" cy="{top[1] - 6 * s:.0f}" rx="{16 * s:.0f}" ry="{12 * s:.0f}" fill="#ff5a5a" stroke="#5a0a10" stroke-width="3"/>'
    return g


def make_3():
    rnd = random.Random(303)
    d = FILTERS + lin('bg3', [(0, '#0a2a44'), (.18, '#04142a'), (.6, '#020a16'), (1, '#01040a')]) + vig(a=.8)
    d += halo('h3', 540, 640, 520, inner='#ffe0a0', outer='#3fe8d8')
    d += lin('ice3', [(0, '#f4fdff'), (.6, '#9fd8ec'), (1, '#4a9abc')])
    d += lin('chim3', [(0, '#3a3a40'), (.5, '#1a1a20'), (1, '#0a0a0e')], x2=1, y2=0)
    d += lin('plume3', [(0, '#1a1c24', ), (1, '#ff8a3a')])
    b = f'<rect width="{W}" height="{H}" fill="url(#bg3)"/>'
    # icy-moon crust overhead
    crust = 'M-20 -10 L1100 -10 L1100 150 ' + ' '.join(f'L{1100 - k * 60} {150 + (25 if k % 2 else -5) + rnd.randint(-12, 12)}' for k in range(20)) + ' L-20 160Z'
    b += f'<path d="{crust}" fill="url(#ice3)" stroke="#dffaff" stroke-width="4"/>'
    for k in range(9):
        x = rnd.uniform(40, 1040); b += f'<path d="M{x:.0f} -10 l{rnd.uniform(-30, 30):.0f} 60 l{rnd.uniform(-30, 30):.0f} 50" stroke="#4a8ab0" stroke-width="3" fill="none" opacity=".7"/>'
    for x0 in (200, 560, 880):
        b += f'<path d="M{x0 - 40} 150 L{x0 + 40} 150 L{x0 + 160} 900 L{x0 - 160} 900Z" fill="#9fe8ff" opacity=".05"/>'
    b += f'<ellipse cx="540" cy="640" rx="560" ry="460" fill="url(#h3)"/>'
    # plume of mineral smoke rising from the chimney mouth
    for k in range(8):
        py = 330 - k * 24; px = 540 + 26 * math.sin(k * .9); r = 34 + k * 10
        b += f'<circle cx="{px:.0f}" cy="{py}" r="{r}" fill="{['#8a5a40', '#6a5058', '#5a5060', '#4a4a5a'][min(k // 2, 3)]}" opacity="{.75 - k * .06:.2f}" filter="url(#b6)"/>'
        b += f'<circle cx="{px - r * .3:.0f}" cy="{py - r * .3:.0f}" r="{r * .45:.0f}" fill="#c89a80" opacity="{.4 - k * .04:.2f}" filter="url(#b6)"/>'
    b += '<ellipse cx="540" cy="340" rx="60" ry="40" fill="#ffb050" opacity=".9" filter="url(#b12)"/><ellipse cx="540" cy="350" rx="34" ry="18" fill="#fff0b0"/>'
    # ridge + chimney
    b += '<path d="M-20 860 Q160 760 330 790 Q440 740 540 760 Q660 740 760 790 Q920 760 1100 850 L1100 900 L-20 900Z" fill="#0c1218" stroke="#3fe8d8" stroke-width="4" stroke-opacity=".4"/>'
    chim = 'M430 790 C440 700 470 640 480 560 C484 500 470 460 490 400 L500 350 L580 350 L590 410 C610 470 600 520 610 580 C620 660 650 720 660 790Z'
    b += f'<path d="{chim}" fill="url(#chim3)" stroke="#05060a" stroke-width="8"/>'
    for crk in ('M512 420 l14 30 l-10 26 l18 34', 'M570 470 l-12 36 l16 30 l-8 40', 'M488 600 l20 40 l-6 34 l22 44', 'M600 640 l-16 50 l14 40', 'M540 520 l6 30 l-10 24'):
        b += f'<path d="{crk}" stroke="#ffb050" stroke-width="16" fill="none" opacity=".35" filter="url(#b6)"/><path d="{crk}" stroke="#ff9a40" stroke-width="5" fill="none" stroke-linejoin="round"/>'
    for x, y, r in ((470, 700, 26), (620, 560, 20), (500, 480, 18), (640, 740, 24)):
        b += f'<ellipse cx="{x}" cy="{y}" rx="{r}" ry="{r * .6:.0f}" fill="#2a2a32" stroke="#05060a" stroke-width="4"/>'
    b += '<path d="M500 352 L580 352" stroke="#ffd080" stroke-width="10"/><path d="M576 380 C596 470 600 560 640 700" stroke="#ffd8a0" stroke-width="4" fill="none" opacity=".5"/>'
    # microbial mats + tube worm clusters at the base
    for x, y, rx in ((330, 800, 120), (760, 800, 130), (540, 790, 90)):
        b += f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="28" fill="#5ff8e0" opacity=".55" filter="url(#b12)"/><ellipse cx="{x}" cy="{y}" rx="{rx * .7:.0f}" ry="12" fill="#b8fff0" opacity=".7"/>'
    for x, h, lean in ((300, 140, -30), (330, 200, -10), (360, 170, 6), (390, 120, 20), (270, 100, -40), (420, 90, 26)):
        b += worm(x, 810, h, lean)
    for x, h, lean in ((690, 110, -24), (720, 180, -6), (750, 210, 10), (785, 150, 26), (815, 100, 40), (660, 80, -30)):
        b += worm(x, 810, h, lean)
    for sx, sy, ss in ((250, 520, 22), (840, 470, 26), (720, 300, 14), (360, 330, 16), (940, 680, 18)):
        b += spark(sx, sy, ss, col='#e0fffa')
    b += fireflies(60, 180, 840, col='#5ff8e0', core='#dffff8', seed=31)
    b += darkband(860, 1240, .5)
    # foreground seafloor below: rocks with glowing microbes, worms lit by the frog's lamp
    b += f'<path d="M-20 1700 Q200 1620 420 1660 Q640 1600 840 1640 Q980 1610 1100 1650 L1100 {H} L-20 {H}Z" fill="#0a1016" stroke="#3fe8d8" stroke-width="3" stroke-opacity=".35"/>'
    b += '<path d="M330 1580 L1100 1380 L1100 1800 L380 1640Z" fill="#fff6c8" opacity=".09" filter="url(#b12)"/>'
    for x, y, rx in ((820, 1650, 120), (560, 1680, 80), (980, 1640, 70)):
        b += f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="24" fill="#5ff8e0" opacity=".5" filter="url(#b12)"/>'
    for x, h, lean in ((780, 120, -14), (810, 170, 0), (845, 140, 16), (875, 90, 30), (940, 110, 10)):
        b += worm(x, 1660, h, lean, .9)
    b += fireflies(25, 1280, 1840, col='#5ff8e0', core='#dffff8', seed=32)
    for k in range(8):
        b += f'<circle cx="{180 + k * 6 + rnd.uniform(-8, 8):.0f}" cy="{1400 - k * 40}" r="{rnd.choice([5, 7, 9])}" fill="none" stroke="#dff6ff" stroke-width="2.4" opacity=".6"/>'
    lamp = ('<path d="M56 -40 L74 -40 L78 -18 L52 -18Z" fill="#c9a24e" stroke-width="3"/><circle cx="66" cy="-46" r="9" fill="#fff6c8" stroke-width="3"/>'
            '<circle cx="66" cy="-46" r="20" fill="#fff6c8" opacity=".5" stroke="none"/>')
    b += '<ellipse cx="260" cy="1640" rx="230" ry="190" fill="#5ff8e0" opacity=".12" filter="url(#b24)"/>'
    b += frog(250, 1770, 3.3, look=(3, -3), mouth='O', shadow=True, helmet=True, front=lamp, armR='M38 -22 q16 -4 24 -20', armL='M-34 -22 q-14 6 -16 22')
    b += f'<rect width="{W}" height="{H}" fill="url(#vig)"/>'
    save(3, '#01040a', d, b, [('LIFE IN', 170, 'w'), ('THE DARK', 170, 'y')], '#01060c', 872)


# ================= 4: FIRST TO ARRIVE? =================
def make_4():
    rnd = random.Random(404)
    CX, CY, R = 540, 480, 320
    d = FILTERS + rad('bg4', 540, 480, 1400, [(0, '#2a1450', 1), (.35, '#120828', 1), (1, '#030108', 1)]) + vig()
    d += halo('h4', CX, CY, 560, inner='#ffffff', outer='#8a7aff')
    d += rad('face4', CX, CY, R, [(0, '#fff8e0', .95), (.15, '#ffb0e0', .7), (.5, '#5a3aa8', .55), (.85, '#1e2a6a', .5), (1, '#0a0a2a', .4)])
    d += lin('rim4', [(0, '#fff3c0'), (.5, '#e0a040'), (1, '#8a5a1a')])
    b = f'<rect width="{W}" height="{H}" fill="url(#bg4)"/>' + starfield(rnd, 60, 0, H, '#d8d0ff')
    b += f'<ellipse cx="{CX}" cy="{CY}" rx="620" ry="580" fill="url(#h4)"/>'
    # clock face: swirling young gas
    b += f'<circle cx="{CX}" cy="{CY}" r="{R}" fill="url(#face4)"/>'
    for arm in range(3):
        pts = []
        for i in range(120):
            t = i / 119; a = arm * 2.09 + t * 4.2; r = 40 + t * (R - 60)
            pts.append((CX + r * math.cos(a), CY + r * math.sin(a)))
        sw = 'M' + ' L'.join(f'{x:.1f} {y:.1f}' for x, y in pts)
        b += f'<path d="{sw}" stroke="#d8b0ff" stroke-width="34" fill="none" opacity=".25" filter="url(#b12)"/><path d="{sw}" stroke="#ffe0f8" stroke-width="4" fill="none" opacity=".5"/>'
    for _ in range(90):
        a, r = rnd.uniform(0, 6.28), R * math.sqrt(rnd.random()) * .95
        b += f'<circle cx="{CX + r * math.cos(a):.0f}" cy="{CY + r * math.sin(a):.0f}" r="{rnd.choice([1.4, 2, 3])}" fill="#fff" opacity="{rnd.uniform(.3, .9):.2f}"/>'
    # rim + hour marks (stars)
    b += f'<circle cx="{CX}" cy="{CY}" r="{R + 12}" fill="none" stroke="#120626" stroke-width="34"/><circle cx="{CX}" cy="{CY}" r="{R + 12}" fill="none" stroke="url(#rim4)" stroke-width="20"/>'
    b += f'<circle cx="{CX}" cy="{CY}" r="{R + 34}" fill="none" stroke="#ffd27a" stroke-width="4" opacity=".6"/>'
    for k in range(12):
        a = math.radians(-90 + k * 30); x, y = CX + (R - 34) * math.cos(a), CY + (R - 34) * math.sin(a)
        b += spark(x, y, 26 if k == 0 else 15, col='#fff8d8' if k == 0 else '#e8e0ff')
    # hands: just past twelve
    for ang, L, w in ((-84, R * .55, 22), (-60, R * .82, 14)):
        a = math.radians(ang); ex, ey = CX + L * math.cos(a), CY + L * math.sin(a)
        b += f'<path d="M{CX} {CY} L{ex:.0f} {ey:.0f}" stroke="#2a1006" stroke-width="{w + 10}" stroke-linecap="round"/><path d="M{CX} {CY} L{ex:.0f} {ey:.0f}" stroke="#ffd27a" stroke-width="{w}" stroke-linecap="round"/>'
        b += f'<path d="M{CX} {CY} L{ex:.0f} {ey:.0f}" stroke="#fff6d8" stroke-width="{w * .3:.0f}" stroke-linecap="round" opacity=".8"/>'
    # the first star igniting at the centre
    b += f'<circle cx="{CX}" cy="{CY}" r="120" fill="#bfe0ff" opacity=".7" filter="url(#b24)"/><circle cx="{CX}" cy="{CY}" r="54" fill="#ffffff" opacity=".95" filter="url(#b6)"/>'
    b += f'<path d="M{CX - 260} {CY} L{CX + 260} {CY} M{CX} {CY - 220} L{CX} {CY + 220}" stroke="#eaf4ff" stroke-width="6" opacity=".8" filter="url(#b2)"/>'
    b += spark(CX, CY, 90, col='#ffffff', op=1) + f'<circle cx="{CX}" cy="{CY}" r="26" fill="#fff"/>'
    for sx, sy, ss in ((CX + 380, CY - 270, 24), (CX - 400, CY - 200, 18), (CX + 400, CY + 230, 16), (CX - 380, CY + 280, 20)):
        b += spark(sx, sy, ss, col='#fff6e0')
    b += fireflies(30, 140, 840, col='#d8b0ff', core='#fff8ff', seed=41)
    b += darkband(860, 1240, .5)
    # below: the still-empty party: small newborn galaxies + a young ringed planet; frog on a young rock
    for x, y, r, rot in ((820, 1400, 70, -20), (960, 1600, 44, 30), (640, 1500, 36, 10)):
        b += f'<ellipse cx="{x}" cy="{y}" rx="{r}" ry="{r * .35:.0f}" transform="rotate({rot} {x} {y})" fill="#b8a0ff" opacity=".35" filter="url(#b6)"/><ellipse cx="{x}" cy="{y}" rx="{r * .3:.0f}" ry="{r * .14:.0f}" transform="rotate({rot} {x} {y})" fill="#fff4d8"/>'
    b += '<circle cx="840" cy="1740" r="80" fill="#4a6ad8" stroke="#0a0a2a" stroke-width="6"/><path d="M780 1720 q60 -20 120 0" stroke="#9ab8ff" stroke-width="10" fill="none" opacity=".6"/>'
    b += '<ellipse cx="840" cy="1740" rx="150" ry="28" fill="none" stroke="#0a0a2a" stroke-width="14" transform="rotate(-14 840 1740)"/><ellipse cx="840" cy="1740" rx="150" ry="28" fill="none" stroke="#f2d27a" stroke-width="7" transform="rotate(-14 840 1740)"/>'
    b += '<path d="M60 1800 Q80 1700 200 1690 Q330 1680 420 1720 Q480 1770 450 1830 Q300 1880 120 1860 Q60 1850 60 1800Z" fill="#5a4a6a" stroke="#120a1a" stroke-width="7"/>'
    b += '<path d="M120 1720 Q240 1700 380 1716" stroke="#c8b8e8" stroke-width="5" fill="none" opacity=".7"/><ellipse cx="300" cy="1790" rx="30" ry="12" fill="#2a1e36"/><ellipse cx="160" cy="1810" rx="20" ry="8" fill="#2a1e36"/>'
    party = ('<path d="M-6 -104 L12 -150 L28 -102Z" fill="#ff6ab0" stroke-width="3.4"/><path d="M0 -118 L22 -114 M5 -132 L18 -130" stroke="#ffe06a" stroke-width="4"/>'
             '<circle cx="12" cy="-152" r="7" fill="#ffe06a" stroke-width="3"/>')
    b += '<ellipse cx="260" cy="1600" rx="230" ry="190" fill="#d8b0ff" opacity=".13" filter="url(#b24)"/>'
    b += frog(260, 1730, 3.2, look=(3, -4), mouth='O', shadow=True, mid=SPACE_HELMET + party, armR='M38 -22 q22 -12 26 -46', armL='M-34 -22 q-14 6 -16 22')
    b += f'<rect width="{W}" height="{H}" fill="url(#vig)"/>'
    save(4, '#030108', d, b, [('FIRST', 236, 'y'), ('TO ARRIVE?', 128, 'w')], '#04020a', 864)


# ================= 5: MADE OF STARS =================
def make_5():
    rnd = random.Random(505)
    SX, SY = 860, 230
    d = FILTERS + rad('bg5', 600, 400, 1500, [(0, '#2a0a3a', 1), (.4, '#10041e', 1), (1, '#020106', 1)]) + vig()
    d += rad('sn5', SX, SY, 520, [(0, '#ffffff', 1), (.12, '#fff0b0', .9), (.35, '#ff6ab0', .45), (.7, '#6a3aff', .15), (1, '#6a3aff', 0)])
    d += rad('body5', 560, 520, 520, [(0, '#fff3c0', 1), (.3, '#ff8ad0', .9), (.65, '#7a4aff', .85), (1, '#1a2a8a', .9)])
    bust = ('M520 220 C440 220 390 290 392 370 C394 440 420 500 460 532 L466 590 C420 620 300 630 220 680 C170 712 150 780 146 850 L894 850 '
            'C890 780 870 712 820 680 C740 630 620 620 574 590 L580 532 C620 500 646 440 648 370 C650 290 600 220 520 220Z')
    d += f'<clipPath id="bust5"><path d="{bust}"/></clipPath>'
    b = f'<rect width="{W}" height="{H}" fill="url(#bg5)"/>' + starfield(rnd, 150, 0, H, '#f0e0ff')
    # supernova behind, top right
    b += f'<circle cx="{SX}" cy="{SY}" r="520" fill="url(#sn5)"/>'
    for k in range(16):
        a = math.radians(k * 22.5 + 8); L = 260 + (k % 3) * 70
        b += f'<path d="M{SX} {SY} L{SX + L * math.cos(a):.0f} {SY + L * math.sin(a):.0f}" stroke="#fff4e0" stroke-width="{6 - k % 3 * 1.5}" opacity=".55" filter="url(#b2)"/>'
    for r, col in ((180, '#ffd27a'), (260, '#ff6ab0')):
        b += f'<circle cx="{SX}" cy="{SY}" r="{r}" fill="none" stroke="{col}" stroke-width="10" opacity=".45" filter="url(#b6)" stroke-dasharray="40 26"/>'
    b += spark(SX, SY, 80, col='#ffffff', op=1) + f'<circle cx="{SX}" cy="{SY}" r="30" fill="#fff"/>'
    # debris streaming from the supernova into the silhouette
    for k in range(9):
        y_end = 360 + k * 50
        p = f'M{SX} {SY} Q{SX - 120} {SY + 40 + k * 30} {560 + rnd.randint(-80, 80)} {y_end}'
        b += f'<path d="{p}" stroke="#ffb0e0" stroke-width="3" fill="none" opacity=".35" stroke-dasharray="2 14" stroke-linecap="round"/>'
    for _ in range(70):
        t = rnd.random(); x = SX + (420 - SX) * t + rnd.gauss(0, 50); y = SY + (560 - SY) * t + rnd.gauss(0, 60)
        b += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{rnd.choice([2, 3, 4])}" fill="{rnd.choice(["#fff3c0", "#ffb0e0", "#bfe8ff"])}" opacity=".85"/>'
    # the human bust, filled with nebula + star debris
    b += f'<path d="{bust}" fill="#ff8ad0" opacity=".55" filter="url(#b24)"/>'
    inner = f'<rect x="100" y="200" width="850" height="660" fill="url(#body5)"/>'
    for k in range(5):
        p = f'M{150 + k * 40} {860 - k * 30} C{300 + k * 30} {600 - k * 40} {600 - k * 20} {700 - k * 60} {700 + k * 20} {300 + k * 40}'
        inner += f'<path d="{p}" stroke="#ffe8ff" stroke-width="{30 - k * 4}" fill="none" opacity=".18" filter="url(#b6)"/>'
    inner += ''.join(f'<circle cx="{rnd.uniform(140, 900):.0f}" cy="{rnd.uniform(210, 850):.0f}" r="{rnd.choice([1.6, 2.4, 3.4, 4.4])}" fill="{rnd.choice(["#fff", "#fff3c0", "#bfe8ff", "#ffd0f0"])}" opacity="{rnd.uniform(.5, 1):.2f}"/>' for _ in range(260))
    for x, y, s in ((470, 330, 14), (600, 720, 18), (330, 760, 12), (760, 760, 12), (540, 450, 10)):
        inner += spark(x, y, s, col='#ffffff')
    b += f'<g clip-path="url(#bust5)">{inner}</g>'
    b += f'<path d="{bust}" fill="none" stroke="#fff4e0" stroke-width="6" opacity=".9"/><path d="{bust}" fill="none" stroke="#ffd27a" stroke-width="18" opacity=".35" filter="url(#b6)"/>'
    # element chips inside: iron (blood), calcium (bones), carbon (cells)
    for x, y, t, col in ((604, 742, 'Fe', '#ff6a6a'), (360, 720, 'Ca', '#f4f0e0'), (520, 380, 'C', '#ffd27a')):
        b += f'<circle cx="{x}" cy="{y}" r="58" fill="{col}" opacity=".45" filter="url(#b12)"/><circle cx="{x}" cy="{y}" r="40" fill="#1a0a2a" stroke="{col}" stroke-width="6"/>'
        b += f'<text x="{x}" y="{y + 15}" text-anchor="middle" font-family="Fredoka" font-weight="700" font-size="42" fill="{col}">{t}</text>'
    b += fireflies(35, 140, 840, col='#ffb0e0', core='#fff4fa', seed=51)
    b += darkband(860, 1240, .5)
    # below: drifting star dust + a meteorite; frog looking at its own sparkling hand
    b += fireflies(30, 1280, 1850, col='#ffd27a', core='#fff8e0', seed=52)
    b += '<path d="M700 1620 Q760 1540 860 1560 Q960 1570 980 1650 Q990 1730 900 1760 Q780 1780 720 1720 Q680 1680 700 1620Z" fill="#4a3a4a" stroke="#120a14" stroke-width="7"/>'
    for x, y, r in ((780, 1620, 16), (900, 1680, 22), (820, 1720, 12)):
        b += f'<circle cx="{x}" cy="{y}" r="{r}" fill="#2a1e2a"/>'
    for x, y in ((760, 1680), (860, 1610), (930, 1730), (840, 1660)):
        b += f'<circle cx="{x}" cy="{y}" r="12" fill="#ffd27a" opacity=".6" filter="url(#b3)"/><circle cx="{x}" cy="{y}" r="4" fill="#fff8e0"/>'
    b += '<path d="M690 1620 L560 1540 M700 1660 L590 1610" stroke="#ffd27a" stroke-width="4" opacity=".4" stroke-linecap="round"/>'
    sparkle = ''.join(spark(x, y, s, col='#fff3c0') for x, y, s in ((72, -86, 9), (60, -106, 6), (90, -100, 5)))
    b += '<ellipse cx="260" cy="1620" rx="230" ry="190" fill="#ffb0e0" opacity=".13" filter="url(#b24)"/>'
    b += '<circle cx="320" cy="1500" r="40" fill="#fff3c0" opacity=".35" filter="url(#b12)"/>'
    b += frog(250, 1770, 3.3, look=(4, -4), mouth='O', shadow=True, mid=SPACE_HELMET, front=sparkle, armR='M38 -22 q26 -16 30 -66', armL='M-34 -22 q-14 6 -16 22')
    b += f'<rect width="{W}" height="{H}" fill="url(#vig)"/>'
    save(5, '#020106', d, b, [('MADE OF', 150, 'w'), ('STARS', 224, 'y')], '#030108', 864)


if __name__ == '__main__':
    which = sys.argv[1:] or ['1', '2', '3', '4', '5']
    for n in which:
        globals()[f'make_{n}'](); print('made', n)
