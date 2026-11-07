# STYLE B (guideline 16-9 B, 2026-11-07): dark scene + glowing level golden scale (nine vs one) + one-line hook.
# Shorts thumbnail (VERTICAL 1080x1920, text centred) for right-handed-majority-short5 (guideline 16-9, brief tools/briefs/thumb_art.md 'Shorts thumbnails').
# WHY 90 : 10?   intuitive: a big golden balance scale held LEVEL: nine right-handed toolmakers crowd one pan, ONE
#                left-hander with a glowing hand axe stands alone on the other pan; the frog sits on top of the pivot like a
#                judge. Script: "Why did humans settle on a 90-to-10 split instead of a coin flip?", the ratio as a stable
#                equilibrium of cooperation and competition, "a balanced evolutionary treaty" (Abrams & Panaggio model).
import os, sys, math, random, importlib.util
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', '..', 'tools'))
_s = importlib.util.spec_from_file_location('rhm_thumb', os.path.join(HERE, '..', '..', 'right-handed-majority', 'thumb', 'make.py'))
L = importlib.util.module_from_spec(_s); _s.loader.exec_module(L)
from thumb_lib import vpage, vsvg, lin, rad, spark, fireflies, halo, darkband
from body import shoulders
LINE, BODY = L.LINE, L.BODY
GOLD = '#e8b84a'; GOLDL = '#ffe39a'; GOLDD = '#a8762a'


def axe(gx, gy, ang, s, glow=False):
    g = f'<g transform="translate({gx:.0f} {gy:.0f}) rotate({ang}) scale({s:.2f})">'
    if glow:
        g += '<ellipse cx="0" cy="-40" rx="60" ry="70" fill="#ffe08a" opacity=".8" filter="url(#b8)"/>'
    g += (f'<path d="M0 10 Q-26 -20 -22 -56 Q-12 -90 0 -96 Q12 -90 22 -56 Q26 -20 0 10Z" fill="#9aa0aa" stroke="{LINE}" stroke-width="6" stroke-linejoin="round"/>'
          f'<path d="M-8 -20 L4 -40 L-6 -60 M8 -16 L-2 -34" stroke="#6a707a" stroke-width="4" fill="none"/>'
          f'<path d="M-10 -70 Q-4 -86 4 -88" stroke="#e8eef6" stroke-width="5" fill="none" stroke-linecap="round"/></g>')
    return g


def worker(cx, top, H, skin, hair, shirt, look, mouth, lefty=False, glow=False):
    kind = 'cute'
    (lx, ly), (rx, ry) = shoulders(cx, top, H, kind)
    if not lefty:   # tool in the RIGHT hand (viewer left), raised a little
        tool = axe(lx - .55 * H, ly - .1 * H, -25, H / 90)
        arms = L.limb_to((lx, ly), (lx - .5 * H, ly + .25 * H), H, kind, 1, f'w{int(cx)}{top}a', shirt, skin, 'short') + \
            L.limb_to((rx, ry), (rx + .15 * H, ry + 1.4 * H), H, kind, -1, f'w{int(cx)}{top}b', shirt, skin, 'short')
    else:           # tool in the LEFT hand (viewer right), raised high
        tool = axe(rx - .37 * H, ry - 1.55 * H, 18, H / 62, glow)
        arms = L.limb_to((rx, ry), (rx + .55 * H, ry - .95 * H), H, kind, -1, f'w{int(cx)}{top}a', shirt, skin, 'short') + \
            L.limb_to((lx, ly), (lx - .15 * H, ly + 1.4 * H), H, kind, 1, f'w{int(cx)}{top}b', shirt, skin, 'short')
    return L.person(cx, top, H, kind, skin, hair, shirt, '#4a3020', '#2a1a10', look=look, mouth=mouth, brows='up',
                    props_front=tool + arms, sleeve_len='short')


def make():
    rnd = random.Random(9)
    d = L.FILTERS
    d += lin('bg5', [(0, '#030c10'), (.6, '#08202a'), (1, '#030c10')])
    d += halo("spot5", 540, 460, 680, inner='#ffe6a0', outer='#e8a84a')
    d += '<filter id="b6" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="6"/></filter><filter id="b50" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="50"/></filter>'
    d += rad('vig5', 540, 960, 1250, [(0, '#000', 0), (.6, '#000', 0), (1, '#000', .6)])
    d += lin('gold5', [(0, GOLDL), (.5, GOLD), (1, GOLDD)])
    d += lin('floor5', [(0, '#16323a'), (1, '#081418')])
    b = '<rect width="1080" height="1920" fill="url(#bg5)"/>'
    b += '<path d="M0 1440 Q300 1380 640 1420 T1080 1400 L1080 1920 L0 1920Z" fill="#0e2a30"/>'
    b += '<rect width="1080" height="1920" fill="url(#spot5)"/>'
    b += '<path d="M0 1610 Q500 1580 1080 1600 L1080 1920 L0 1920Z" fill="url(#floor5)"/>'
    for _ in range(60):
        b += f'<circle cx="{rnd.randint(20, 1060)}" cy="{rnd.randint(60, 1700)}" r="{rnd.choice([2, 3, 4])}" fill="#ffe8b0" opacity="{rnd.uniform(.2, .7):.2f}"/>'
    b += spark(160, 260, 22, '#ffe8b0') + spark(900, 380, 18, '#ffe8b0') + spark(820, 170, 14, '#ffe8b0')
    b += '<g transform="translate(-548 25) scale(.86)">'
    # ---------- balance scale ----------
    PX, BY = 1300, 330
    b += f'<ellipse cx="{PX}" cy="{BY + 20}" rx="520" ry="160" fill="#ffd27a" opacity=".25" filter="url(#b32)"/>'
    # post + base
    b += f'<path d="M{PX - 26} {BY} L{PX + 26} {BY} L{PX + 34} 900 L{PX - 34} 900Z" fill="url(#gold5)" stroke="{LINE}" stroke-width="8"/>'
    b += f'<path d="M{PX - 170} 960 Q{PX - 160} 890 {PX} 885 Q{PX + 160} 890 {PX + 170} 960Z" fill="url(#gold5)" stroke="{LINE}" stroke-width="8"/>'
    b += f'<path d="M{PX - 12} {BY + 20} L{PX - 12} 880" stroke="#fff6d0" stroke-width="8" opacity=".6"/>'
    LX, RX, PY = 900, 1630, 700
    # chains (behind people)
    def chains(cx):
        return ''.join(f'<path d="M{cx} {BY + 6} L{cx + dx} {PY - 10}" stroke="{LINE}" stroke-width="9"/><path d="M{cx} {BY + 6} L{cx + dx} {PY - 10}" stroke="{GOLD}" stroke-width="4" stroke-dasharray="10 6"/>' for dx in (-190, 190))
    b += chains(LX) + chains(RX)
    # beam (level)
    b += f'<rect x="{LX - 30}" y="{BY - 18}" width="{RX - LX + 60}" height="36" rx="18" fill="url(#gold5)" stroke="{LINE}" stroke-width="8"/>'
    b += f'<path d="M{LX} {BY - 6} L{RX} {BY - 6}" stroke="#fff6d0" stroke-width="7" opacity=".7" stroke-linecap="round"/>'
    for cx in (LX, RX):
        b += f'<circle cx="{cx}" cy="{BY}" r="22" fill="{GOLDL}" stroke="{LINE}" stroke-width="7"/>'
    b += f'<circle cx="{PX}" cy="{BY}" r="40" fill="{GOLDL}" stroke="{LINE}" stroke-width="8"/><circle cx="{PX}" cy="{BY}" r="14" fill="{GOLDD}"/>'
    # ---------- pans: nine right-handers | one left-hander ----------
    skins = ['#f3c9a2', '#d9a37a', '#a8714a', '#7a4d30', '#f5d6b8', '#c88c62', '#e2b08a', '#8f5c3a', '#f0c19a']
    hairs = [('bob', '#2b1d14'), ('short', '#6b3e1e'), ('buns', '#1a1a1a'), ('spiky', '#c98c3a'), ('pony', '#3a2416'), ('short', '#111'),
             ('long', '#8a4a20'), ('spiky', '#2b1d14'), ('short', '#3a2416')]
    shirts = ['#7a5a34', '#8a6a3a', '#6a4a2a', '#9a6a3a', '#7a5030', '#8a5a2e', '#6a5030', '#9a7040', '#7a6038']
    H = 44
    crowd = ''
    k = 0
    for row, (top, xs) in enumerate(((PY - 5.1 * H - 34, (780, 860, 940, 1020)), (PY - 5.1 * H - 8, (740, 820, 900, 980, 1060)))):
        for x in xs:
            crowd += worker(x, top, H, skins[k], hairs[k], shirts[k], (1.5, 0) if x > 860 else (1.2, .2), 'o' if k % 3 == 0 else 'smile')
            k += 1
    b += crowd
    lefty_glow = f'<ellipse cx="{RX}" cy="{PY - 160}" rx="170" ry="220" fill="#ffd06a" opacity=".55" filter="url(#b32)"/>'
    b += lefty_glow
    b += worker(RX, PY - 5.1 * 64 - 8, 64, '#c88c62', ('spiky', '#5a2e14'), '#c0563f', (-1.2, 0), 'grin', lefty=True, glow=True)
    def pan(cx):
        return (f'<path d="M{cx - 220} {PY - 14} Q{cx} {PY + 120} {cx + 220} {PY - 14}Z" fill="url(#gold5)" stroke="{LINE}" stroke-width="8" stroke-linejoin="round"/>'
                f'<ellipse cx="{cx}" cy="{PY - 14}" rx="220" ry="16" fill="{GOLDL}" stroke="{LINE}" stroke-width="7"/>'
                f'<path d="M{cx - 160} {PY + 20} Q{cx - 60} {PY + 70} {cx + 40} {PY + 60}" stroke="#fff6d0" stroke-width="8" fill="none" opacity=".6" stroke-linecap="round"/>')
    b += pan(LX) + pan(RX)
    b += spark(RX + 130, PY - 420, 26) + spark(RX - 120, PY - 330, 16) + spark(LX - 260, PY - 120, 14, '#ffe8b0') + spark(PX + 90, BY - 210, 18)
    # frog judge on top of the pivot
    wig = ('<path d="M-38 -70 Q-44 -110 8 -112 Q58 -110 52 -70" fill="#f4f1e8" stroke-width="3.6"/>'
           '<circle cx="-36" cy="-66" r="10" fill="#f4f1e8" stroke-width="3"/><circle cx="50" cy="-66" r="10" fill="#f4f1e8" stroke-width="3"/>'
           '<circle cx="-38" cy="-48" r="9" fill="#f4f1e8" stroke-width="3"/><circle cx="52" cy="-48" r="9" fill="#f4f1e8" stroke-width="3"/>')
    robe = f'<g clip-path="url(#fbody)"><rect x="-50" y="-40" width="110" height="64" fill="#2a2a3a" stroke-width="3"/><path d="M-4 -40 L8 -20 L20 -40" fill="#f4f1e8" stroke-width="2.6"/></g><path d="{BODY}" fill="none" stroke-width="4"/>'
    b += L.frog(PX - 4, BY - 36, 2.05, look=(6, -2), mouth='O', armL='M-34 -24 q-18 -2 -26 -26', armR='M38 -22 q14 6 16 22', back=wig, mid=robe, shadow=False)
    b += '</g>'
    b += fireflies(60, 80, 1850, col='#ffd27a', core='#fff3c0', seed=6)
    b += darkband(860, 1240, .45)
    b += '<rect width="1080" height="1920" fill="url(#vig5)"/>'
    lines = [('WHY', 190, 'w'), ('90 : 10?', 260, 'y')]
    return vpage('#030c10', vsvg(d, b), lines, outline='#041216', top=890)


if __name__ == '__main__':
    open(os.path.join(HERE, 'A.html'), 'w').write(make()); print('ok')
