# STYLE B (guideline 16-9 B, 2026-11-07): dark scene + glowing sunset duel + one-line hook.
# Shorts thumbnail (VERTICAL 1080x1920, text centred) for right-handed-majority-short4 (guideline 16-9, brief tools/briefs/thumb_art.md 'Shorts thumbnails').
# SURPRISE FROM THE LEFT   intuitive: prehistoric one-on-one duel on a rock ledge in front of a huge setting sun; the
#                          right-hander guards with his spear on his right side and sweats, the rare left-hander swings his
#                          club with the LEFT hand (gold arc). Frog in a fur headband peeks from behind a rock.
#                          Script: surprise and unfamiliar angles, "the left-hander held the lethal advantage of novelty"
#                          (fighting hypothesis). Differs from long B (Kill Bill crowd) by composition, place and palette.
import os, sys, math, random, importlib.util
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', '..', 'tools'))
_s = importlib.util.spec_from_file_location('rhm_thumb', os.path.join(HERE, '..', '..', 'right-handed-majority', 'thumb', 'make.py'))
L = importlib.util.module_from_spec(_s); _s.loader.exec_module(L)
from thumb_lib import vpage, vsvg, lin, rad, spark, fireflies, halo, darkband
from body import shoulders
LINE, BODY = L.LINE, L.BODY


def club(gx, gy, ang, Ln, w):
    """grip at (gx, gy), club head in direction ang (0 = up, clockwise)"""
    return (f'<g transform="translate({gx:.0f} {gy:.0f}) rotate({ang})">'
            f'<path d="M{-w * .35:.0f} {w * .8:.0f} L{-w * .55:.0f} {-Ln * .55:.0f} Q{-w * 1.1:.0f} {-Ln * .95:.0f} {-w * .2:.0f} {-Ln:.0f} Q{w * 1.2:.0f} {-Ln * 1.02:.0f} {w * .95:.0f} {-Ln * .7:.0f} L{w * .35:.0f} {w * .8:.0f}Z" fill="#8a5a2e" stroke="{LINE}" stroke-width="{w * .22:.0f}" stroke-linejoin="round"/>'
            f'<path d="M{-w * .1:.0f} {-Ln * .2:.0f} L{-w * .2:.0f} {-Ln * .85:.0f}" stroke="#c48a50" stroke-width="{w * .2:.0f}" stroke-linecap="round"/>'
            f'<circle cx="{w * .3:.0f}" cy="{-Ln * .8:.0f}" r="{w * .16:.0f}" fill="#5a3418"/><circle cx="{-w * .4:.0f}" cy="{-Ln * .66:.0f}" r="{w * .12:.0f}" fill="#5a3418"/>'
            f'<path d="M{-w * .45:.0f} 0 l{w * .9:.0f} {-w * .3:.0f} M{-w * .45:.0f} {w * .35:.0f} l{w * .9:.0f} {-w * .3:.0f}" stroke="#d8c8a0" stroke-width="{w * .12:.0f}"/></g>')


def spear(gx, gy, ang, Ln, w):
    return (f'<g transform="translate({gx:.0f} {gy:.0f}) rotate({ang})">'
            f'<rect x="{-w / 2:.0f}" y="{-Ln * .7:.0f}" width="{w:.0f}" height="{Ln:.0f}" rx="{w / 2:.0f}" fill="#9a6a3a" stroke="{LINE}" stroke-width="{w * .35:.0f}"/>'
            f'<path d="M0 {-Ln * .7 - w * 4.5:.0f} L{w * 1.5:.0f} {-Ln * .7 + w * .5:.0f} L{-w * 1.5:.0f} {-Ln * .7 + w * .5:.0f}Z" fill="#7a8088" stroke="{LINE}" stroke-width="{w * .35:.0f}" stroke-linejoin="round"/>'
            f'<path d="M{-w * .7:.0f} {-Ln * .7 + w * .6:.0f} l{w * 1.4:.0f} {w * .8:.0f}" stroke="#c8a060" stroke-width="{w * .4:.0f}"/></g>')


def make():
    rnd = random.Random(21)
    d = L.FILTERS
    d += lin('sky4', [(0, '#0a0414'), (.35, '#2a0f30'), (.6, '#5a1a34'), (1, '#1a0a1a')])
    d += halo('sun4', 540, 470, 700, inner='#fff0b0', outer='#ff8a2a')
    d += '<filter id="b6" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="6"/></filter><filter id="b50" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="50"/></filter>'
    d += rad('vig4', 540, 960, 1250, [(0, '#000', 0), (.6, '#000', 0), (1, '#000', .62)])
    b = '<rect width="1080" height="1920" fill="url(#sky4)"/>'
    b += '<rect width="1080" height="1920" fill="url(#sun4)"/>'
    b += '<circle cx="540" cy="470" r="330" fill="#ffe7a0"/><circle cx="540" cy="470" r="330" fill="#fff6d0" opacity=".5" filter="url(#b16)"/>'
    for y, o in ((400, .22), (480, .18), (560, .14)):   # sun bands
        b += f'<rect x="200" y="{y}" width="680" height="10" fill="#e2662e" opacity="{o}"/>'
    for x, y, s_ in ((820, 300, 1), (900, 350, .7), (180, 260, .8)):
        b += f'<path d="M{x} {y} q{14 * s_:.0f} {-12 * s_:.0f} {28 * s_:.0f} 0 q{14 * s_:.0f} {-12 * s_:.0f} {28 * s_:.0f} 0" stroke="#3a1426" stroke-width="5" fill="none" stroke-linecap="round"/>'
    b += fireflies(50, 100, 1850, col='#ffb060', core='#fff0c0', seed=4)
    b += '<g transform="translate(-308 30) scale(.64)">'
    # rock ledge they fight on
    H = 160; kind = 'cute'; TOP = 330
    # ---------- the right-hander (left of frame): spear in his RIGHT hand (viewer left), braced the wrong way ----------
    DX = 1090; SKD = '#c48a5e'; FURD = '#7a5030'
    (lx, ly), (rx, ry) = shoulders(DX, TOP, H, kind)
    sp = spear(lx - 30, ly + 238, -14, 560, 20)
    a1 = L.limb_to((lx, ly), (lx - 30, ly + 228), H, kind, 1, 'dR', FURD, SKD, 'short')
    a2 = L.limb_to((rx, ry), (rx + 30, ry + 228), H, kind, -1, 'dL', FURD, SKD, 'short')
    sweat = L.sweat(DX + 100, TOP + 20, 40) + L.sweat(DX + 120, TOP + 90, 28)
    tunic = f'<path d="M{DX - .7 * H} {TOP + 1.3 * H} L{DX + .7 * H} {TOP + 1.3 * H} L{DX + .78 * H} {TOP + 3.0 * H} L{DX + .3 * H} {TOP + 2.8 * H} L{DX} {TOP + 3.05 * H} L{DX - .35 * H} {TOP + 2.8 * H} L{DX - .78 * H} {TOP + 3.0 * H}Z" fill="{FURD}" stroke="{LINE}" stroke-width="6" stroke-linejoin="round"/>'
    b += f'<ellipse cx="{DX}" cy="{TOP + 1.8 * H}" rx="200" ry="320" fill="#ffe0a0" opacity=".3" filter="url(#b32)"/>'
    b += L.person(DX, TOP, H, kind, SKD, ('spiky', '#2a1a10'), FURD, SKD, '#3a2416', look=(-1, 0), mouth='wobble', brows='worried', side=-1,
                  deco=tunic, props_back=sp, props_front=a1 + a2 + sweat, rim=(1, '#ffe08a'), sleeve_len='short', stance=.3)
    # ---------- the rare left-hander (right of frame): club raised in his LEFT hand (viewer right) ----------
    AX = 1560; SKA = '#a8714a'; FURA = '#5a3a24'
    (lx, ly), (rx, ry) = shoulders(AX, TOP, H, kind)
    swing = (f'<path d="M{rx + 150} {ry + 40} Q{rx + 120} {TOP - 260} {DX + 130} {TOP - 120}" stroke="#F2D27A" stroke-width="40" fill="none" stroke-linecap="round" opacity=".55" filter="url(#b8)"/>'
             f'<path d="M{rx + 150} {ry + 40} Q{rx + 120} {TOP - 260} {DX + 130} {TOP - 120}" stroke="#fff6c8" stroke-width="12" fill="none" stroke-linecap="round" stroke-dasharray="70 30"/>')
    cl = club(rx + 70, ry - 120, -38, 300, 60)
    up = L.limb_to((rx, ry), (rx + 70, ry - 110), H, kind, -1, 'aL', FURA, SKA, 'short')
    down = L.limb_to((lx, ly), (lx - 30, ly + 228), H, kind, 1, 'aR', FURA, SKA, 'short')
    tunic = f'<path d="M{AX - .7 * H} {TOP + 1.3 * H} L{AX + .7 * H} {TOP + 1.3 * H} L{AX + .78 * H} {TOP + 3.0 * H} L{AX + .3 * H} {TOP + 2.8 * H} L{AX} {TOP + 3.05 * H} L{AX - .35 * H} {TOP + 2.8 * H} L{AX - .78 * H} {TOP + 3.0 * H}Z" fill="{FURA}" stroke="{LINE}" stroke-width="6" stroke-linejoin="round"/>'
    paint = f'<path d="M{AX - .4 * H} {TOP + .52 * H} l{.18 * H} 0 M{AX + .22 * H} {TOP + .52 * H} l{.18 * H} 0" stroke="#e8e0d0" stroke-width="7" stroke-linecap="round"/>'
    b += f'<ellipse cx="{rx + 80}" cy="{ry - 160}" rx="170" ry="190" fill="#ffd06a" opacity=".55" filter="url(#b32)"/>'
    b += swing
    b += f'<g transform="rotate(-9 {AX} 1000)">' + L.person(AX, TOP, H, kind, SKA, ('long', '#1a120c'), FURA, SKA, '#2a1a10', look=(-1, 0), mouth='grin', brows='angry', side=-1,
                  deco=tunic, props_front=down + cl + up, rim=(-1, '#ffe08a'), sleeve_len='short', stance=.5) + '</g>'
    for k in range(4):   # speed lines behind the lunging left-hander
        b += f'<path d="M{AX + 150 + k * 22} {TOP + 260 + k * 70} l{120 - k * 15} {-10}" stroke="#fff3c0" stroke-width="10" stroke-linecap="round" opacity=".7"/>'
    b += spark(rx + 210, ry - 330, 26) + spark(DX + 240, TOP - 160, 18) + spark(rx - 40, ry - 300, 14)
    b += L.bang(DX + 150, TOP - 20, 100, rot=14)
    b += '</g>'
    b += '<path d="M0 775 Q300 760 540 772 T1080 766 L1080 840 L0 840Z" fill="#1a0a1a" stroke="#ff9a5a" stroke-width="4" opacity=".9"/>'
    b += f'<path d="M-20 1920 L-10 1700 Q60 1660 300 1670 Q560 1640 820 1660 Q1000 1670 1100 1720 L1100 1920Z" fill="#2a0e1a" stroke="{LINE}" stroke-width="8"/>'
    b += '<path d="M60 1685 Q560 1650 1000 1685" stroke="#ff9a5a" stroke-width="8" fill="none" opacity=".6" stroke-linecap="round"/>'
    # frog peeking from behind a rock, fur headband with a feather
    band = ('<path d="M-30 -60 Q8 -72 44 -62" fill="none" stroke="#9a6a3a" stroke-width="10"/>'
            '<path d="M40 -64 Q70 -100 62 -126 Q44 -100 40 -64Z" fill="#e2563a" stroke-width="3"/>')
    b += L.frog(490, 1800, 1.9, look=(6, -4), mouth='O', armL='M-34 -24 q-10 10 -4 30', armR='M38 -24 q20 -2 34 -18', mid=band, shadow=False)
    b += darkband(860, 1240, .45)
    b += '<rect width="1080" height="1920" fill="url(#vig4)"/>'
    lines = [('SURPRISE FROM', 118, 'w'), ('THE LEFT', 200, 'y')]
    return vpage('#0a0414', vsvg(d, b), lines, outline='#14061a', top=905)


if __name__ == '__main__':
    open(os.path.join(HERE, 'A.html'), 'w').write(make()); print('ok')
