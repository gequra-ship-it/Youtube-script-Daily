# STYLE B shorts thumbnails for megalodon-extinction (guideline 16-9 B): dark scene + ONE big glowing concrete subject + centred hook.
# Uses the drawing kit videos/megalodon-extinction/thumb/mgkit.py (frog, shark, tooth, whale).  Run:
#   python3 videos/megalodon-extinction-short1/thumb/make.py   -> videos/megalodon-extinction-short{1..5}/thumb/A.html
# 1 AS LONG AS A BUS     short1: "Imagine a shark as long as a city bus" + "A single tooth could be about as long as an adult human hand".
# 2 DINNER SWAM AWAY     short2: whales pulled toward the polar seas; "watching your dinner swim beyond your reach".
# 3 SMALL BEATS BIG?     short3: smaller early great whites competing for the same prey (hedged: "overlap, not proof").
# 4 NO SAFE NURSERY      short4: shallow nursery bays drying up as sea levels fell; a pup left in a shrinking pool.
# 5 NO GIANT DOWN THERE  short5: the Mariana Trench myth; "Large whales and seals do not feed in those depths", only small specialised animals.
import os, sys, math, random, shutil
HERE = os.path.dirname(os.path.abspath(__file__))
VIDS = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(VIDS, 'megalodon-extinction', 'thumb'))
from mgkit import *
from thumb_lib import vpage, vsvg, lin, rad, spark, fireflies, halo, darkband

W, H = 1080, 1920
VIG = rad('vig', 540, 960, 1250, [(0, '#000', 0), (.55, '#000', 0), (1, '#000', .72)])


def finish(n, d, b, lines, bg, top=880, band=(850, 1250, .5)):
    b += f'<rect width="{W}" height="{H}" fill="url(#vig)"/>'
    b += darkband(*band)
    out = os.path.join(VIDS, f'megalodon-extinction-short{n}', 'thumb')
    os.makedirs(out, exist_ok=True)
    for f in ('common.css', 'Fredoka-700.woff2'):
        if not os.path.exists(os.path.join(out, f)):
            shutil.copy(os.path.join(VIDS, '..', 'tools', 'assets', 'thumb_v', f), out)
    open(os.path.join(out, 'A.html'), 'w').write(vpage(bg, vsvg(FILTERS + VIG + d, b), lines, outline='#04101a', top=top))


def bubbles(rnd, n, x0, x1, y0, y1, col='#eaffff'):
    return ''.join(f'<circle cx="{rnd.randint(x0, x1)}" cy="{rnd.randint(y0, y1)}" r="{rnd.choice([4, 6, 8])}" fill="none" stroke="{col}" stroke-width="2.4" opacity=".5"/>' for _ in range(n))


# ------------------------------------------------ 1: as long as a bus ------------------------------------------------
def bus(x0, y0, L, Hh):
    """glowing city bus, left end x0, roof y0, length L, height Hh"""
    o = f'<rect x="{x0 - 6}" y="{y0 - 6}" width="{L + 12}" height="{Hh + 12}" rx="34" fill="#ffd25a" opacity=".5" filter="url(#b24)"/>'
    o += f'<rect x="{x0}" y="{y0}" width="{L}" height="{Hh}" rx="30" fill="url(#busg)" stroke="#1a1206" stroke-width="6"/>'
    o += f'<rect x="{x0 + 10}" y="{y0 + Hh * .62:.0f}" width="{L - 20}" height="{Hh * .1:.0f}" fill="#d9572a" opacity=".9"/>'
    nw = 9; ww = (L - 150) / nw
    for k in range(nw):
        o += f'<rect x="{x0 + 30 + k * ww:.0f}" y="{y0 + 22}" width="{ww - 12:.0f}" height="{Hh * .38:.0f}" rx="8" fill="#bff6ff" stroke="#1a1206" stroke-width="4"/>'
        o += f'<path d="M{x0 + 36 + k * ww:.0f} {y0 + 30} l{ww * .3:.0f} 0" stroke="#fff" stroke-width="4" opacity=".8"/>'
    o += f'<rect x="{x0 + L - 108}" y="{y0 + 22}" width="86" height="{Hh * .7:.0f}" rx="8" fill="#9fe6f6" stroke="#1a1206" stroke-width="4"/>'
    o += f'<path d="M{x0 + L - 65} {y0 + 22} v{Hh * .7:.0f}" stroke="#1a1206" stroke-width="3"/>'
    o += f'<circle cx="{x0 + L - 14}" cy="{y0 + Hh - 30}" r="12" fill="#fff6c8" stroke="#1a1206" stroke-width="3"/>'
    for wx in (x0 + 140, x0 + L - 210):
        o += f'<circle cx="{wx}" cy="{y0 + Hh}" r="46" fill="#1a1a1e" stroke="#060606" stroke-width="5"/><circle cx="{wx}" cy="{y0 + Hh}" r="20" fill="#9aa2aa"/>'
    return o


def s1():
    rnd = random.Random(1)
    d = lin('bg1', [(0, '#041628'), (.5, '#06223a'), (1, '#020a14')])
    d += halo('h1', 540, 480, 620, inner='#d8fbff', outer='#3ab8e8')
    d += halo('h1b', 300, 1560, 360, inner='#fff3a8', outer='#ffb84a')
    d += lin('busg', [(0, '#ffe07a'), (.6, '#f2b83a'), (1, '#c98a1a')])
    b = f'<rect width="{W}" height="{H}" fill="url(#bg1)"/>'
    for x0, w in ((200, 120), (480, 160), (760, 110)):
        b += f'<path d="M{x0} 0 L{x0 + w} 0 L{x0 + w - 200} {H} L{x0 - 300} {H}Z" fill="#bff4ff" opacity=".05"/>'
    b += f'<ellipse cx="540" cy="480" rx="700" ry="560" fill="url(#h1)"/>'
    s = .9; L = 1082 * s; xl = (W - L) / 2
    cx = xl + (82 + 500) * s
    sd, sg = shark(cx, 380, s, mouth='closed', idp='s1', top='#2c4a5c', mid='#6a8c9c', rim='#e0fbff', glow='#a8f2ff', glow_op=.55)
    d += sd; b += sg
    b += bus(xl, 640, L, 150)
    # measuring guides: both ends line up
    for gx in (xl, xl + L):
        b += f'<path d="M{gx:.0f} 160 V830" stroke="#fff3a8" stroke-width="4" stroke-dasharray="14 12" opacity=".8"/>'
    b += f'<path d="M{xl + 20:.0f} 600 H{xl + L - 20:.0f}" stroke="#fff3a8" stroke-width="5" opacity=".9"/>'
    b += f'<path d="M{xl + 40:.0f} 586 L{xl + 14:.0f} 600 L{xl + 40:.0f} 614 M{xl + L - 40:.0f} 586 L{xl + L - 14:.0f} 600 L{xl + L - 40:.0f} 614" fill="none" stroke="#fff3a8" stroke-width="5"/>'
    b += fireflies(50, 120, 1850, col='#bff8ff', core='#ffffff', seed=11)
    # bottom: frog in a diving helmet hugging one fossil tooth
    b += f'<path d="M0 1760 Q300 1700 560 1730 Q820 1760 1080 1720 V1920 H0Z" fill="#0a2230"/>'
    b += f'<ellipse cx="420" cy="1560" rx="360" ry="300" fill="url(#h1b)"/>'
    td, tg = tooth(700, 1600, 1.0, rot=14, idp='t1'); d += td
    b += '<ellipse cx="700" cy="1745" rx="120" ry="18" fill="#000" opacity=".4"/>' + tg
    b += frog(300, 1760, 3.3, look=(4, -2), helmet=True, armR='M38 -24 q24 -10 36 -26', armL='M-34 -24 q-18 4 -20 22')
    for sx_, sy_, ss in ((160, 280, 22), (930, 250, 20), (700, 1440, 18), (900, 1600, 16), (120, 800, 16)):
        b += spark(sx_, sy_, ss, col='#fffbe0')
    finish(1, d, b, [('AS LONG AS A', 124, 'w'), ('BUS', 250, 'y')], '#041628')


# ------------------------------------------------ 2: dinner swam away (to the cold polar sea) ------------------------------------------------
def s2():
    rnd = random.Random(2)
    d = lin('bg2', [(0, '#0a3a5a'), (.4, '#06243a'), (.55, '#1a0c08'), (1, '#3a1406')])
    d += halo('h2', 540, 360, 640, inner='#e8ffff', outer='#5ad8ff')
    d += halo('h2b', 640, 1560, 520, inner='#ffcf7a', outer='#ff7a2a')
    b = f'<rect width="{W}" height="{H}" fill="url(#bg2)"/>'
    # polar surface: ice floes + aurora at the very top
    b += '<path d="M-20 120 C200 40 420 160 640 80 C820 20 980 110 1100 60" fill="none" stroke="#7affc8" stroke-width="60" opacity=".18" filter="url(#b24)"/>'
    b += f'<ellipse cx="540" cy="360" rx="720" ry="520" fill="url(#h2)"/>'
    b += '<rect x="0" y="196" width="1080" height="6" fill="#e8ffff" opacity=".7"/>'
    for x0, w, dd, hh in ((-30, 330, 110, 60), (360, 170, 50, 22), (590, 300, 130, 80), (950, 180, 70, 30)):
        b += f'<path d="M{x0} 200 L{x0 + 30} {200 - hh * .6:.0f} L{x0 + w * .4:.0f} {200 - hh} L{x0 + w * .7:.0f} {200 - hh * .8:.0f} L{x0 + w} 200 L{x0 + w * .8:.0f} {200 + dd * .7:.0f} L{x0 + w * .5:.0f} {200 + dd} L{x0 + w * .15:.0f} {200 + dd * .6:.0f}Z" fill="#9fd8ee" stroke="#0a3048" stroke-width="4" opacity=".95"/>'
        b += f'<path d="M{x0} 200 L{x0 + 30} {200 - hh * .6:.0f} L{x0 + w * .4:.0f} {200 - hh} L{x0 + w * .7:.0f} {200 - hh * .8:.0f} L{x0 + w} 200Z" fill="#f4feff" stroke="#0a3048" stroke-width="4"/>'
    # krill / plankton bloom near the poles
    b += fireflies(70, 210, 620, col='#9ff6ff', core='#ffffff', seed=21)
    # whales swimming up and away toward the ice
    for wx, wy, ws, wr in ((600, 470, .62, -22), (260, 640, .42, -26), (880, 690, .36, -18)):
        b += whale(wx, wy, ws, rot=wr, col='#3a5a70', belly='#cfe2ea', rim='#e0fdff', glow='#9ff0ff')
    b += bubbles(rnd, 16, 100, 1000, 300, 820)
    # warm, empty water below: the megalodon looking up, hungry
    b += f'<ellipse cx="640" cy="1560" rx="620" ry="460" fill="url(#h2b)"/>'
    sd, sg = shark(700, 1500, .62, rot=-24, mouth='closed', idp='s2', top='#3a3a44', mid='#7a7a80', belly='#e8e0d8', rim='#ffd9a0', glow='#ffb04a', glow_op=.5)
    d += sd; b += sg
    b += fireflies(26, 1300, 1850, col='#ffcf7a', core='#fff6d8', seed=22)
    # frog with a napkin and a fork, bottom-left
    nap = '<path d="M-20 -32 L32 -32 L24 2 L6 14 L-12 2Z" fill="#fff" stroke-width="3"/><path d="M-6 -20 L16 -20 M-2 -10 L12 -10" stroke="#d84a3a" stroke-width="3"/>'
    fork = '<path d="M54 -6 L66 -64" stroke-width="5"/><path d="M54 -6 L66 -64" stroke="#d8dde4" stroke-width="2.5"/><path d="M60 -66 L58 -86 M66 -66 L66 -88 M72 -64 L74 -86" stroke-width="3.5"/>'
    b += frog(210, 1800, 3.3, look=(3, -5), armR='M38 -22 q16 0 18 -14', mid=nap, front=fork)
    for sx_, sy_, ss in ((150, 300, 20), (960, 330, 22), (900, 1700, 16), (420, 1380, 14)):
        b += spark(sx_, sy_, ss, col='#fffbe0')
    finish(2, d, b, [('DINNER', 230, 'y'), ('SWAM AWAY', 140, 'w')], '#06243a')


# ------------------------------------------------ 3: small beats big? ------------------------------------------------
def s3():
    rnd = random.Random(3)
    d = lin('bg3', [(0, '#03101e'), (.5, '#061a2c'), (1, '#02070e')])
    d += halo('h3', 640, 700, 380, inner='#fff3a8', outer='#ffbf4a')
    d += halo('h3b', 500, 380, 640, inner='#4a7a9a', outer='#1a3a5a')
    b = f'<rect width="{W}" height="{H}" fill="url(#bg3)"/>'
    b += f'<ellipse cx="500" cy="380" rx="700" ry="520" fill="url(#h3b)"/>'
    # the giant: huge, dim, facing right, mouth closed
    sd, sg = shark(470, 380, .98, mouth='closed', idp='s3a', top='#22343f', mid='#4a6270', belly='#9aa8ae', rim='#8ab8d0', glow='#4a8ab0', glow_op=.35)
    d += sd; b += sg
    # the small great white: bright, fast, catching the fish first
    b += f'<ellipse cx="640" cy="700" rx="520" ry="300" fill="url(#h3)"/>'
    for k in range(5):
        b += f'<path d="M{170 - k * 20} {660 + k * 22} l{-150 + k * 10} 0" stroke="#fff3c8" stroke-width="5" opacity="{.7 - k * .1:.2f}" stroke-linecap="round"/>'
    sd, sg = shark(520, 690, .36, rot=-6, mouth='open', idp='s3b', top='#55636e', mid='#9aa6ae', belly='#f4f2ea', rim='#fff3c8', glow='#ffd86a', glow_op=.7)
    d += sd; b += sg
    # fish in front of it
    b += ('<g transform="translate(830 640) rotate(-8)"><ellipse cx="0" cy="0" rx="56" ry="24" fill="#c9d6de" stroke="#0b161d" stroke-width="4"/>'
          '<path d="M48 0 L84 -22 L80 22Z" fill="#9fb0bc" stroke="#0b161d" stroke-width="4"/><circle cx="-34" cy="-5" r="5" fill="#0b161d"/>'
          '<path d="M-10 -22 q20 -14 40 0" fill="#9fb0bc" stroke="#0b161d" stroke-width="3"/></g>')
    b += fireflies(46, 120, 1850, col='#bff8ff', core='#ffffff', seed=31)
    b += bubbles(rnd, 12, 600, 1000, 560, 800)
    # sea floor + referee frog
    b += '<path d="M0 1740 Q260 1690 540 1720 Q820 1750 1080 1700 V1920 H0Z" fill="#0c2230"/>'
    b += '<ellipse cx="300" cy="1600" rx="300" ry="220" fill="#fff3a8" opacity=".12" filter="url(#b24)"/>'
    shirt = ('<g clip-path="url(#fb3)"><rect x="-50" y="-34" width="110" height="40" fill="#f4f4f0" stroke="none"/>'
             + ''.join(f'<rect x="{-46 + k * 16}" y="-34" width="8" height="40" fill="#1a1a1a" stroke="none"/>' for k in range(7)) + '</g>')
    whistle = '<path d="M-6 -46 Q6 -20 20 -40" fill="none" stroke="#d84a3a" stroke-width="2.5"/><rect x="14" y="-34" width="22" height="12" rx="5" fill="#ffd25a" stroke-width="3"/>'
    d += '<clipPath id="fb3"><path d="M-34 0 q-6 -64 34 -70 q40 -2 42 62 q0 10 -6 12 q-36 6 -70 -4z"/></clipPath>'
    b += frog(260, 1760, 3.3, look=(4, -4), armR='M38 -24 q28 -14 30 -46', mid=shirt + whistle)
    for sx_, sy_, ss in ((950, 520, 22), (380, 820, 16), (130, 180, 18), (960, 1500, 16)):
        b += spark(sx_, sy_, ss, col='#fffbe0')
    finish(3, d, b, [('SMALL', 250, 'y'), ('BEATS BIG?', 140, 'w')], '#03101e')


# ------------------------------------------------ 4: no safe nursery ------------------------------------------------
def s4():
    rnd = random.Random(4)
    d = lin('sky4', [(0, '#0a0a26'), (.5, '#3a1a4a'), (1, '#c8603a')])
    d += lin('mud4', [(0, '#6a4a32'), (.5, '#3a2618'), (1, '#120a06')])
    d += halo('h4', 470, 620, 420, inner='#fff3c8', outer='#5ae8e0')
    d += lin('pool4', [(0, '#7af0e8'), (1, '#1a7a8a')])
    b = f'<rect width="{W}" height="520" fill="url(#sky4)"/>'
    b += ''.join(f'<circle cx="{rnd.randint(0, W)}" cy="{rnd.randint(10, 300)}" r="{rnd.choice([1.4, 2, 2.6])}" fill="#fff" opacity="{rnd.uniform(.3, .9):.2f}"/>' for _ in range(70))
    b += '<circle cx="860" cy="470" r="70" fill="#ffb060" opacity=".9"/><circle cx="860" cy="470" r="160" fill="#ff9050" opacity=".25" filter="url(#b24)"/>'
    # the open sea pulled far back to the horizon (right), the bay floor exposed
    b += '<path d="M600 520 L1080 500 L1080 560 Q900 540 600 520Z" fill="#2a6a8a"/>'
    b += f'<path d="M0 500 Q300 520 600 520 Q900 540 1080 560 V{H} H0Z" fill="url(#mud4)"/>'
    # old waterline marks on the mud (where the bay used to be)
    for k, y in enumerate((620, 700, 790)):
        b += f'<path d="M0 {y} Q300 {y - 30} 600 {y - 10} Q850 {y + 10} 1080 {y - 20}" fill="none" stroke="#c9a06a" stroke-width="4" opacity="{.45 - k * .1:.2f}" stroke-dasharray="20 14"/>'
    # cracks
    for _ in range(40):
        x, y = rnd.randint(0, W), rnd.randint(560, 1880)
        if 820 < y < 1280: continue
        pts = [(x, y)]
        for k in range(4):
            x += rnd.randint(-60, 60); y += rnd.randint(-20, 40); pts.append((x, y))
        b += f'<polyline points="{P(pts)}" fill="none" stroke="#0e0804" stroke-width="{rnd.choice([3, 4, 5])}" opacity=".8"/>'
    # the last shrinking pool with the pup
    b += f'<ellipse cx="470" cy="640" rx="560" ry="300" fill="url(#h4)"/>'
    b += '<ellipse cx="470" cy="660" rx="400" ry="120" fill="#0a2a30" stroke="#2a1a0e" stroke-width="6"/>'
    b += '<ellipse cx="470" cy="652" rx="380" ry="108" fill="url(#pool4)" opacity=".85"/>'
    b += '<ellipse cx="470" cy="652" rx="380" ry="108" fill="none" stroke="#e8fffc" stroke-width="4" opacity=".7"/>'
    for r in (120, 200, 280):
        b += f'<ellipse cx="470" cy="660" rx="{r}" ry="{r * .26:.0f}" fill="none" stroke="#e8fffc" stroke-width="3" opacity="{.6 - r / 600:.2f}"/>'
    sd, sg = shark(470, 640, .5, rot=-3, mouth='closed', idp='s4', top='#3a5a6a', mid='#7a9aa8', belly='#f4f8f8', rim='#eafffc', glow='#9ff8ee', glow_op=.6)
    d += sd
    d += '<clipPath id="poolc4"><rect x="0" y="560" width="1080" height="400"/></clipPath>'
    b += sg
    b += '<path d="M120 646 Q470 680 820 646 Q470 700 120 646Z" fill="#7af0e8" opacity=".35"/>'
    b += fireflies(40, 120, 1850, col='#bff8f0', core='#ffffff', seed=41)
    # frog with a bucket of water, bottom
    bucket = ('<path d="M44 -36 Q66 -70 88 -36" fill="none" stroke-width="3.5"/>'
              '<path d="M40 -36 L92 -36 L86 4 L46 4Z" fill="#8aa0b4" stroke-width="3.5"/><ellipse cx="66" cy="-36" rx="26" ry="6" fill="#5ad8e8" stroke-width="3"/>'
              '<path d="M90 -32 q10 10 4 24" fill="none" stroke="#7af0e8" stroke-width="3"/>')
    b += frog(330, 1760, 3.3, look=(3, -5), armR='M38 -22 q20 -16 28 -30', back=bucket)
    for sx_, sy_, ss in ((150, 200, 20), (980, 250, 18), (880, 760, 16), (120, 740, 14)):
        b += spark(sx_, sy_, ss, col='#fffbe0')
    finish(4, d, b, [('NO SAFE', 150, 'w'), ('NURSERY', 220, 'y')], '#0a0a26')


# ------------------------------------------------ 5: no giant down there ------------------------------------------------
def s5():
    rnd = random.Random(5)
    d = lin('bg5', [(0, '#061a2c'), (.35, '#030c18'), (1, '#000204')])
    d += halo('h5', 540, 470, 540, inner='#9ff0ff', outer='#2a6aa8')
    b = f'<rect width="{W}" height="{H}" fill="url(#bg5)"/>'
    # trench walls narrowing into the dark
    b += '<path d="M0 0 L250 0 Q300 400 380 820 Q420 1300 470 1920 L0 1920Z" fill="#0a1622"/><path d="M1080 0 L830 0 Q780 400 700 820 Q660 1300 610 1920 L1080 1920Z" fill="#0a1622"/>'
    b += '<path d="M250 0 Q300 400 380 820 Q420 1300 470 1920" fill="none" stroke="#3a6a8a" stroke-width="5" opacity=".6"/><path d="M830 0 Q780 400 700 820 Q660 1300 610 1920" fill="none" stroke="#3a6a8a" stroke-width="5" opacity=".6"/>'
    for _ in range(26):
        y = rnd.randint(40, 1880); sd_ = rnd.choice([-1, 1])
        x = (250 + (y / 1920) * 220) if sd_ < 0 else (830 - (y / 1920) * 220)
        b += f'<path d="M{x:.0f} {y} l{-sd_ * rnd.randint(-60, -10)} {rnd.randint(10, 40)}" stroke="#1e3a50" stroke-width="5" opacity=".7"/>'
    b += f'<ellipse cx="540" cy="470" rx="620" ry="460" fill="url(#h5)"/>'
    # the empty outline where people imagine the giant: glowing dashed silhouette, nothing inside
    s = .78; cx = 540
    sil = ''.join(f'<path d="{p}"/>' for p in silhouette_d())
    b += f'<g transform="translate({cx} 470) rotate(-6) scale({s}) translate(-500 0)" fill="#000" opacity=".55">{sil}</g>'
    b += f'<g transform="translate({cx} 470) rotate(-6) scale({s}) translate(-500 0)" fill="none" stroke="#bff8ff" stroke-width="16" opacity=".55" filter="url(#b6)" stroke-linejoin="round">{sil}</g>'
    b += f'<g transform="translate({cx} 470) rotate(-6) scale({s}) translate(-500 0)" fill="none" stroke="#f2feff" stroke-width="6" stroke-dasharray="26 18" stroke-linejoin="round">{sil}</g>'
    # big question-free emptiness: drifting marine snow, small specialised animals
    b += fireflies(60, 80, 1850, col='#9ff0ff', core='#ffffff', seed=51)
    for ax, ay, ar in ((200, 760, 12), (880, 300, -20), (840, 760, 8)):
        b += (f'<g transform="translate({ax} {ay}) rotate({ar})" stroke="#0b161d" stroke-width="3"><path d="M-30 0 q30 -26 60 0 q-30 22 -60 0z" fill="#e8b0c8"/>'
              f'<path d="M30 0 l16 -12 l-2 24z" fill="#e8b0c8"/><circle cx="-16" cy="-3" r="3" fill="#0b161d" stroke="none"/></g>')
    # bathyscaphe with the frog at the bottom, lamp shining up
    b += '<path d="M330 1640 L130 960 L330 960Z" fill="#fff8d8" opacity=".05"/>'
    sub = ('<g transform="translate(300 1700)" stroke="#05080a" stroke-width="6">'
           '<rect x="-60" y="-300" width="120" height="70" rx="14" fill="#d8a23a"/>'
           '<circle cx="0" cy="-120" r="190" fill="#e8b84a"/><path d="M-150 -220 Q-60 -300 80 -290" fill="none" stroke="#fff3c8" stroke-width="10" opacity=".7"/>'
           '<circle cx="0" cy="-120" r="128" fill="#0a2a3a"/>'
           '<rect x="170" y="-160" width="70" height="56" rx="10" fill="#c9cfd8"/><circle cx="240" cy="-132" r="24" fill="#fff8d0"/>'
           '<path d="M-150 30 L-190 90 M150 30 L190 90" fill="none"/><rect x="-220" y="80" width="440" height="22" rx="10" fill="#8a929a"/></g>')
    b += '<circle cx="540" cy="1568" r="60" fill="#fff8d0" opacity=".35" filter="url(#b24)"/>'
    b += sub
    b += '<defs><clipPath id="port5"><circle cx="300" cy="1580" r="124"/></clipPath></defs>'
    b += '<g clip-path="url(#port5)">' + frog(300, 1690, 2.5, look=(3, -5), armL='M-34 -24 q-14 -10 -16 -34', armR='M38 -24 q14 -10 16 -34') + '</g>'
    b += '<circle cx="300" cy="1580" r="128" fill="#bfefff" opacity=".12" stroke="#05080a" stroke-width="8"/><path d="M215 1510 Q250 1470 300 1462" fill="none" stroke="#fff" stroke-width="8" opacity=".6"/>'
    for sx_, sy_, ss in ((540, 200, 22), (900, 620, 18), (180, 420, 16), (700, 1500, 14)):
        b += spark(sx_, sy_, ss, col='#effdff')
    finish(5, d, b, [('NO GIANT', 210, 'y'), ('DOWN THERE', 140, 'w')], '#030c18')


if __name__ == '__main__':
    for f in (s1, s2, s3, s4, s5):
        f()
    print('ok')
