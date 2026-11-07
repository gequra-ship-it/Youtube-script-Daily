# STYLE B shorts thumbnails for deep-sea-giants (guideline 16-9 B, 2026-11-07): dark scene + ONE big glowing concrete subject + centred 2-line hook.
# Reuses helpers (frog, isopod, isopod_front, plate_eye, whale, crushed_sub, snail, hourglass...) from ./make.py (old style, kept).
# Hooks come from the short scripts: 1 "about forty centimeters long ... size of a house cat" / pillbug; 2 "a large dinner plate" (eye 27 cm);
# 3 "meals come months, or even years, apart"; 4 "crumple like an empty soda can ... without being crushed"; 5 giant isopods vs "deep-sea dwarfism ... abyssal snails".
#   python3 videos/deep-sea-giants-short1/thumb/make_b.py   -> videos/deep-sea-giants-short{1..5}/thumb/A.html
import os, sys, math, random, importlib.util
HERE = os.path.dirname(os.path.abspath(__file__))
VID = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(VID, '..', 'tools'))
_s = importlib.util.spec_from_file_location('dsg_old', os.path.join(HERE, 'make.py'))
M = importlib.util.module_from_spec(_s); _s.loader.exec_module(M)
from thumb_lib import vpage, vsvg, lin, rad, spark, fireflies, halo, darkband
frog, hand_at, snow, vbed, bubbles = M.frog, M.hand_at, M.snow, M.vbed, M.bubbles
VIGB = rad('vigb', 540, 960, 1250, [(0, '#000', 0), (.55, '#000', 0), (1, '#000', .7)])


def base(rnd, c0, c1, c2, hx, hy, hr, inner, outer, nflies=46, flycol='#bff8ff', floor=(1640, '#1c3a46', '#040c12', 'floorb')):
    d = M.FILTERS + VIGB + M.ISO_GRAD
    d += lin('wb', [(0, c0), (.5, c1), (1, c2)])
    d += halo('hb', hx, hy, hr, inner=inner, outer=outer)
    b = '<rect width="1080" height="1920" fill="url(#wb)"/>'
    b += f'<ellipse cx="{hx}" cy="{hy}" rx="{hr}" ry="{hr}" fill="url(#hb)"/>'
    b += snow(rnd, 120, 0, 1080, 0, 1700, .06, .3)
    sd, sb = vbed(*floor[:1], floor[1], floor[2], floor[3], rnd); d += sd; b += sb
    b += fireflies(nflies, 120, 1800, col=flycol, core='#ffffff', seed=rnd.randint(1, 99))
    return d, b


def finish(d, b, lines, top, bg, band=(860, 1250, .5)):
    b += darkband(*band)
    b += '<rect width="1080" height="1920" fill="url(#vigb)"/>'
    return vpage(bg, vsvg(d, b), lines, outline='#03101c', top=top)


def pillbug(x, y, s):
    o = f'<g transform="translate({x} {y}) scale({s})" stroke="#2c1a2c" stroke-width="4" stroke-linejoin="round">'
    o += '<path d="M-60 0 Q-60 -52 0 -56 Q60 -52 60 0 Z" fill="url(#isoG)"/>'
    for k in range(-2, 3):
        o += f'<path d="M{k * 20} -54 Q{k * 22} -26 {k * 24} 0" fill="none" stroke-width="3"/>'
    o += '<circle cx="-46" cy="-14" r="6" fill="#1e1c26" stroke="none"/><path d="M-58 -30 q-14 -14 -26 -10 M-58 -22 q-18 -4 -28 6" fill="none" stroke-width="3"/>'
    return o + '</g>'


def pot(x, y, s):
    o = f'<g transform="translate({x} {y}) scale({s})" stroke="#3a1608" stroke-width="5" stroke-linejoin="round">'
    o += '<path d="M-90 0 L-70 160 L70 160 L90 0Z" fill="#c8643a"/><rect x="-104" y="-26" width="208" height="38" rx="8" fill="#e07a48"/>'
    o += '<path d="M-84 -16 L84 -16" stroke="#ffc090" stroke-width="5" opacity=".7" fill="none"/>'
    return o + '</g>'


def snail_big(x, y):
    o = f'<g transform="translate({x} {y})" stroke="#2a1a10" stroke-width="7" stroke-linejoin="round" stroke-linecap="round">'
    o += '<path d="M-150 0 Q-160 -30 -120 -34 L90 -34 Q120 -40 130 -80 Q132 -120 118 -134 Q104 -110 100 -70 L96 -50 L170 0 Z" fill="#e8d0b0" transform="translate(0 0)"/>'
    o += '<path d="M112 -118 l16 -60 M126 -108 l54 -40" fill="none" stroke-width="6"/><circle cx="128" cy="-182" r="9" fill="#2a1a10" stroke="none"/><circle cx="182" cy="-150" r="9" fill="#2a1a10" stroke="none"/>'
    o += '<circle cx="-10" cy="-110" r="98" fill="url(#shellG)"/>'
    o += '<path d="M-10 -110 m-8 0 a12 12 0 1 1 24 0 a30 30 0 1 1 -50 6 a52 52 0 1 1 86 8 a76 76 0 0 1 -60 66" fill="none" stroke-width="6"/>'
    o += '<path d="M-72 -170 Q-30 -204 22 -196" fill="none" stroke="#fff" stroke-width="10" opacity=".8"/>'
    return o + '</g>'


# ---- 1: giant isopod side view, huge, glowing; tiny pillbug on a flowerpot below ----
def b1():
    rnd = random.Random(11)
    d, b = base(rnd, '#06101e', '#040a16', '#02060c', 540, 480, 640, '#ffe6f0', '#7ff5d8')
    b += '<ellipse cx="540" cy="760" rx="520" ry="60" fill="#000" opacity=".5" filter="url(#b24)"/>'
    b += M.isopod(590, 640, 450, 320, rnd, legs_near=True, shadow=False,
                  ants=(('M95 650 C20 560 -20 520 -40 470', 13), ('M100 670 C40 690 20 730 30 780', 11)))
    b += '<g transform="translate(0 0)"></g>'
    # bottom: frog (diving helmet) amazed + flowerpot with a tiny pillbug
    b += '<ellipse cx="560" cy="1640" rx="520" ry="200" fill="#7ff5d8" opacity=".09" filter="url(#b50)"/>'
    b += pot(800, 1590, 1.5) + pillbug(800, 1580, 1.1)
    b += spark(800, 1470, 16, '#ffe8b0')
    b += frog(300, 1790, 3.4, look=(12, -8), mouth='O', helmet=True, shadow=True, armL='M-34 -22 q-18 4 -24 22', armR='M38 -22 q18 -14 22 -40')
    b += bubbles(340, 1420)
    b += spark(120, 220, 20, '#fff6d6') + spark(980, 300, 18, '#e8fbff') + spark(900, 820, 14)
    return finish(d, b, [('40 CM', 240, 'y'), ('PILLBUG', 168, 'w')], 880, '#02060c')


# ---- 2: the squid eye as a glowing dinner plate ----
def b2():
    rnd = random.Random(7)
    d, b = base(rnd, '#050a14', '#030812', '#01040a', 540, 470, 700, '#ffe2a0', '#ff8a4a', flycol='#6ff6ff')
    d += rad('china', 1200, 600, 300, [(0, '#ffffff', 1), (.8, '#e8f0f8', 1), (1, '#a8b8c8', 1)])
    d += rad('iris2', 1200, 610, 205, [(0, '#3a1e06', 1), (.7, '#8a5418', 1), (.88, '#f0b850', 1), (1, '#6a3e10', 1)])
    d += rad('pup2', 1180, 600, 150, [(0, '#0e2440', 1), (.75, '#030810', 1), (1, '#000', 1)])
    d += lin('steel', [(0, '#f4f7fb'), (.5, '#b8c2d0'), (1, '#6c7888')], 1, 0)
    d += '<clipPath id="pupC"><circle cx="1185" cy="612" r="146"/></clipPath>'
    s = 1.02
    b += f'<g transform="translate({540 - 1200 * s:.1f} {470 - 610 * s:.1f}) scale({s})">{M.plate_eye(rnd)}</g>'
    # hunter shadow below + frog with bib and fork
    b += '<ellipse cx="640" cy="1480" rx="330" ry="90" fill="#1a4870" opacity=".4" filter="url(#b50)"/>'
    b += f'<g transform="translate(1290 0) scale(-1 1)">{M.sperm_whale(650, 1480, 1.3, "#0a1c2e", "#5fc8ee")}</g>'
    bib = '<path d="M-22 -24 L30 -24 L20 4 L4 14 L-12 4 Z" fill="#ffffff" stroke-width="3"/><path d="M-22 -24 L30 -24" stroke="#c8423a" stroke-width="4"/>'
    arm = 'M38 -22 q18 -12 24 -40'
    fx, fy, fs = 300, 1790, 3.2
    b += '<circle cx="300" cy="1640" r="200" fill="#6ff6ff" opacity=".1" filter="url(#b50)"/>'
    b += frog(fx, fy, fs, look=(11, -6), mouth='O', helmet=True, shadow=True, mid=bib, armL='M-34 -22 q-18 4 -24 22', armR=arm)
    hx, hy = hand_at(fx, fy, fs, arm)
    b += f'<g transform="translate({hx:.0f} {hy:.0f}) rotate(16)">{M.fork(0, -150, 0, .4)}</g>'
    b += bubbles(340, 1450) + spark(900, 1300, 16) + spark(120, 1260, 14, '#e8fbff')
    return finish(d, b, [('EYES LIKE', 150, 'w'), ('PLATES', 230, 'y')], 910, '#01040a', band=(880, 1280, .5))


# ---- 3: the whale fall glowing as it sinks; months of waiting below ----
def b3():
    rnd = random.Random(41)
    d, b = base(rnd, '#06161f', '#040e18', '#02070c', 520, 440, 640, '#e8fbff', '#6fc8ee', flycol='#f8fffb')
    d += lin('whaleG', [(0, '#c8dcea'), (.35, '#7896ae'), (1, '#28405a')])
    b += '<path d="M250 -20 L880 -20 L820 1560 L300 1560 Z" fill="#e8fbff" opacity=".1" filter="url(#b24)"/>'
    b += M.whale(130, 640, .98, -26)
    b += snow(rnd, 90, 100, 1000, 120, 760, .5, .95, '#f8fffb')
    for ax, ay, r in ((140, 740, 20), (230, 800, 40), (90, 640, 10), (330, 730, 60)):
        b += M.amphipod(ax, ay, 1.5, r)
    b += '<ellipse cx="700" cy="1650" rx="340" ry="44" fill="#bfe8ff" opacity=".12" filter="url(#b24)"/>'
    b += M.isopod(740, 1590, 250, 170, rnd, ants=(('M475 1592 C440 1520 460 1450 520 1390', 11), ('M480 1608 C440 1590 420 1570 400 1550', 9)))
    b += M.hourglass(360, 1745, 1.0)
    b += frog(160, 1790, 3.0, look=(10, -9), mouth='O', helmet=True, shadow=True, armL='M-34 -22 q-20 -4 -26 -30', armR='M38 -22 q18 0 24 18')
    b += bubbles(190, 1470) + spark(720, 150, 20, '#ffffff') + spark(960, 520, 16)
    return finish(d, b, [('MEALS', 150, 'w'), ('MONTHS', 220, 'y'), ('APART', 150, 'w')], 840, '#02070c', band=(850, 1290, .45))


# ---- 4: the crushed submarine glowing; calm fish below ----
def b4():
    rnd = random.Random(57)
    d, b = base(rnd, '#06141e', '#030a12', '#01050a', 540, 520, 660, '#ffe8a0', '#ffb060', flycol='#e8fbff')
    d += lin('subG', [(0, '#ffd85a'), (.5, '#f2b632'), (1, '#9a6a12')])
    d += lin('fishG', [(0, '#fbe4ec'), (.55, '#e0a8bc'), (1, '#8a5068')])
    s = 1.0
    b += f'<g transform="translate({540 - 1270 * s:.1f} {540 - 600 * s:.1f}) scale({s})">{M.crushed_sub(rnd)}</g>'
    b += '<rect width="1080" height="1920" fill="url(#hb)" opacity=".0"/>'
    b += '<ellipse cx="560" cy="1470" rx="400" ry="150" fill="#ffd6e4" opacity=".14" filter="url(#b50)"/>'
    b += M.calm_fish(580, 1470, 1.3, rnd)
    b += frog(170, 1790, 3.0, look=(12, -8), mouth='O', helmet=True, shadow=True, armL='M-34 -22 q-20 -6 -26 -32', armR='M38 -22 q22 -6 28 -38')
    b += bubbles(200, 1470) + spark(900, 300, 18) + spark(880, 1320, 14, '#e8fbff')
    return finish(d, b, [('WHY NOT', 170, 'w'), ('CRUSHED?', 176, 'y')], 880, '#01050a')


# ---- 5: tiny snail under the glowing magnifier vs a towering isopod ----
def b5():
    rnd = random.Random(73)
    d, b = base(rnd, '#05141c', '#030a12', '#01050a', 540, 470, 660, '#fff1c0', '#ffb040', flycol='#fff3a8')
    d += rad('shellG', -6, -38, 30, [(0, '#fff4dc', 1), (.6, '#f0a868', 1), (1, '#a85a2a', 1)])
    d += rad('glassb', 540, 470, 250, [(0, '#fff6d8', 1), (.7, '#f4dcae', 1), (1, '#d9b47a', 1)])
    d += '<clipPath id="lensb"><circle cx="540" cy="470" r="215"/></clipPath>'
    b += '<circle cx="540" cy="470" r="262" fill="#ffe7a8" opacity=".5" filter="url(#b24)"/>'
    b += '<circle cx="540" cy="470" r="215" fill="url(#glassb)"/>'
    b += f'<g clip-path="url(#lensb)"><ellipse cx="540" cy="580" rx="230" ry="30" fill="#c9a266" opacity=".6"/>{snail_big(540, 600)}</g>'
    b += '<circle cx="540" cy="470" r="215" fill="none" stroke="#c99a3a" stroke-width="28"/><circle cx="540" cy="470" r="215" fill="none" stroke="#2a1c06" stroke-width="6"/><circle cx="540" cy="470" r="229" fill="none" stroke="#2a1c06" stroke-width="6"/>'
    b += '<path d="M400 340 A170 170 0 0 1 500 280" stroke="#fff" stroke-width="12" fill="none" opacity=".8" stroke-linecap="round"/>'
    b += '<path d="M690 626 L800 740" stroke="#2a1c06" stroke-width="48" stroke-linecap="round"/><path d="M690 626 L800 740" stroke="#a8743a" stroke-width="32" stroke-linecap="round"/>'
    # towering isopod below the text
    b += M.isopod_front(560, 1560, 700, 400, rnd)
    b += frog(200, 1800, 2.8, look=(10, -8), mouth='O', helmet=True, shadow=True, armL='M-34 -22 q-20 -4 -26 -30', armR='M38 -22 q18 -14 22 -40')
    b += bubbles(190, 1500) + spark(900, 260, 20, '#fff6d6') + spark(150, 300, 16, '#fff6d6')
    d += lin('isoF', [(0, '#fbeef0'), (.35, '#e2c3cc'), (.75, '#a87f95'), (1, '#4e3049')])
    return finish(d, b, [('TINY', 190, 'w'), ('OR', 100, 'w'), ('GIANT?', 220, 'y')], 840, '#01050a', band=(850, 1230, .45))


if __name__ == '__main__':
    for n, fn in enumerate((b1, b2, b3, b4, b5), 1):
        out = os.path.join(VID, f'deep-sea-giants-short{n}', 'thumb')
        os.makedirs(out, exist_ok=True)
        open(os.path.join(out, 'A.html'), 'w').write(fn())
    print('ok')
