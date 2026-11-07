# STYLE B (guideline 16-9 B, 2026-11-07): dark scene + glowing womb bubble + one-line hook.
# Shorts thumbnail (VERTICAL 1080x1920, text centred) for right-handed-majority-short3 (guideline 16-9, brief tools/briefs/thumb_art.md 'Shorts thumbnails').
# CHOSEN BEFORE BIRTH?   intuitive: a glowing womb bubble; inside, a curled cute fetus sucks its RIGHT thumb (gold glow on that
#                        hand); the frog doctor (head mirror) listens with a stethoscope on the bubble. Script: by the 15th week
#                        about 90% of fetuses suck the right thumb; "handedness may already be decided" (hedged -> '?').
import os, sys, math, random, importlib.util
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', '..', 'tools'))
_s = importlib.util.spec_from_file_location('rhm_thumb', os.path.join(HERE, '..', '..', 'right-handed-majority', 'thumb', 'make.py'))
L = importlib.util.module_from_spec(_s); _s.loader.exec_module(L)
from thumb_lib import vpage, vsvg, lin, rad, spark, fireflies, halo, darkband
LINE, BODY = L.LINE, L.BODY
SK = '#f6bfa6'; SKD = '#e59a84'


def make():
    rnd = random.Random(4)
    WX, WY, WR = 1330, 560, 420
    d = L.FILTERS
    d += lin('bg3', [(0, '#0e0310'), (.6, '#240a1e'), (1, '#0e0310')])
    d += rad('womb3', WX - 80, WY - 120, WR * 1.15, [(0, '#ffd2b8', 1), (.45, '#f58a7a', 1), (.85, '#b8324a', 1), (1, '#7a1a34', 1)])
    d += halo('halo3', 540, 470, 640, inner='#ffd0c0', outer='#ff5a7a')
    d += '<filter id="b6" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="6"/></filter><filter id="b50" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="50"/></filter>'
    d += rad('vig3', 540, 960, 1250, [(0, '#000', 0), (.6, '#000', 0), (1, '#000', .62)])
    d += f'<clipPath id="wclip"><circle cx="{WX}" cy="{WY}" r="{WR}"/></clipPath>'
    b = '<rect width="1080" height="1920" fill="url(#bg3)"/>'
    for _ in range(40):   # soft bokeh
        b += f'<circle cx="{rnd.randint(0, 1080)}" cy="{rnd.randint(0, 1920)}" r="{rnd.randint(10, 46)}" fill="#ff9aa8" opacity="{rnd.uniform(.05, .18):.2f}" filter="url(#b4)"/>'
    b += '<rect width="1080" height="1920" fill="url(#halo3)"/>'
    pulse = 'M40 1480 L330 1480 L370 1430 L410 1530 L450 1370 L500 1580 L540 1480 L700 1480'   # heartbeat trace (ultrasound room)
    b += f'<g transform="translate(320 0)"><path d="{pulse}" stroke="#ff7a9a" stroke-width="16" fill="none" opacity=".35" filter="url(#b8)"/><path d="{pulse}" stroke="#ffb0c4" stroke-width="6" fill="none" opacity=".7" stroke-linejoin="round"/></g>'
    b += fireflies(50, 100, 1850, col='#ff9ab0', core='#ffe0e8', seed=5) + '<g transform="translate(-457 50) scale(.75)">'
    # womb bubble
    b += f'<circle cx="{WX}" cy="{WY}" r="{WR + 30}" fill="#ff8a8a" opacity=".45" filter="url(#b32)"/>'
    b += f'<circle cx="{WX}" cy="{WY}" r="{WR}" fill="url(#womb3)"/>'
    inner = ''
    for k in range(7):   # veins
        a = rnd.uniform(0, 2 * math.pi); x0 = WX + WR * math.cos(a); y0 = WY + WR * math.sin(a)
        x1 = WX + (WR - 120) * math.cos(a + .3); y1 = WY + (WR - 120) * math.sin(a + .3)
        inner += f'<path d="M{x0:.0f} {y0:.0f} Q{(x0 + x1) / 2 + 30:.0f} {(y0 + y1) / 2 - 20:.0f} {x1:.0f} {y1:.0f} l30 -25 M{(x0 + x1) / 2:.0f} {(y0 + y1) / 2:.0f} l-34 -10" stroke="#9a2440" stroke-width="7" fill="none" opacity=".35" stroke-linecap="round"/>'
    for _ in range(30):
        inner += f'<circle cx="{rnd.randint(WX - WR, WX + WR)}" cy="{rnd.randint(WY - WR, WY + WR)}" r="{rnd.choice([3, 4, 6])}" fill="#fff4e8" opacity="{rnd.uniform(.2, .6):.2f}"/>'
    # umbilical cord (curly) from the belly to the wall
    cord = f'<path d="M{WX + 70} 720 C{WX + 200} 760 {WX + 160} 860 {WX + 260} 880 S{WX + 330} 820 {WX + 360} 760" stroke="{LINE}" stroke-width="40" fill="none" stroke-linecap="round"/>'
    cord += f'<path d="M{WX + 70} 720 C{WX + 200} 760 {WX + 160} 860 {WX + 260} 880 S{WX + 330} 820 {WX + 360} 760" stroke="#e88aa0" stroke-width="28" fill="none" stroke-linecap="round"/>'
    cord += f'<path d="M{WX + 70} 720 C{WX + 200} 760 {WX + 160} 860 {WX + 260} 880 S{WX + 330} 820 {WX + 360} 760" stroke="#b85a78" stroke-width="5" stroke-dasharray="14 18" fill="none"/>'
    inner += cord
    # ---- curled fetus ----
    FX, FY = WX - 30, WY - 60     # head centre
    HR = 150
    f = ''
    # back + bottom
    f += f'<ellipse cx="{FX + 80}" cy="{FY + 230}" rx="170" ry="150" fill="{SK}" stroke="{LINE}" stroke-width="9"/>'
    f += f'<path d="M{FX + 200} {FY + 150} Q{FX + 250} {FY + 240} {FX + 200} {FY + 330}" stroke="#fff" stroke-width="14" fill="none" opacity=".35" stroke-linecap="round"/>'
    # folded legs (knees up in front)
    f += f'<ellipse cx="{FX + 150}" cy="{FY + 300}" rx="110" ry="70" transform="rotate(-25 {FX + 150} {FY + 300})" fill="{SK}" stroke="{LINE}" stroke-width="9"/>'
    f += f'<ellipse cx="{FX + 40}" cy="{FY + 345}" rx="70" ry="38" fill="{SK}" stroke="{LINE}" stroke-width="9"/>'
    for t in range(4):
        f += f'<circle cx="{FX - 18 + t * 13}" cy="{FY + 330 + abs(t - 1.5) * 4:.0f}" r="9" fill="{SK}" stroke="{LINE}" stroke-width="5"/>'
    # left arm (viewer right) resting on the knee
    f += f'<path d="M{FX + 130} {FY + 170} Q{FX + 190} {FY + 230} {FX + 120} {FY + 270}" stroke="{LINE}" stroke-width="56" fill="none" stroke-linecap="round"/>'
    f += f'<path d="M{FX + 130} {FY + 170} Q{FX + 190} {FY + 230} {FX + 120} {FY + 270}" stroke="{SK}" stroke-width="40" fill="none" stroke-linecap="round"/>'
    # head
    f += f'<circle cx="{FX}" cy="{FY}" r="{HR}" fill="{SK}" stroke="{LINE}" stroke-width="10"/>'
    f += f'<path d="M{FX - 100} {FY - 90} Q{FX - 40} {FY - 140} {FX + 40} {FY - 130}" stroke="#fff" stroke-width="16" fill="none" opacity=".45" stroke-linecap="round"/>'
    f += f'<ellipse cx="{FX + HR - 8}" cy="{FY + 10}" rx="22" ry="30" fill="{SK}" stroke="{LINE}" stroke-width="7"/>'
    # closed eyes, cheeks
    for ex in (-58, 42):
        f += f'<path d="M{FX + ex - 26} {FY + 2} Q{FX + ex} {FY + 24} {FX + ex + 26} {FY + 2}" stroke="{LINE}" stroke-width="8" fill="none" stroke-linecap="round"/>'
        f += f'<ellipse cx="{FX + ex * 1.25}" cy="{FY + 42}" rx="26" ry="15" fill="#ef7f74" opacity=".5"/>'
    # right arm (viewer left): from the shoulder up to the mouth, thumb in the mouth (gold glow)
    mx, my = FX - 6, FY + 62
    f += f'<circle cx="{mx - 10}" cy="{my + 20}" r="90" fill="#ffe08a" opacity=".55" filter="url(#b16)"/>'
    f += f'<path d="M{FX - 40} {FY + 200} Q{FX - 120} {FY + 170} {mx - 50} {my + 40}" stroke="{LINE}" stroke-width="58" fill="none" stroke-linecap="round"/>'
    f += f'<path d="M{FX - 40} {FY + 200} Q{FX - 120} {FY + 170} {mx - 50} {my + 40}" stroke="{SK}" stroke-width="42" fill="none" stroke-linecap="round"/>'
    f += f'<ellipse cx="{mx - 40}" cy="{my + 36}" rx="40" ry="34" fill="{SK}" stroke="{LINE}" stroke-width="8"/>'
    f += f'<path d="M{mx - 52} {my + 22} q14 -8 30 0 M{mx - 56} {my + 40} q16 -6 32 2" stroke="{SKD}" stroke-width="5" fill="none" stroke-linecap="round"/>'
    f += f'<ellipse cx="{mx + 6}" cy="{my}" rx="20" ry="17" fill="#8a2f3a" stroke="{LINE}" stroke-width="6"/>'
    f += f'<path d="M{mx - 22} {my + 22} L{mx + 4} {my - 2}" stroke="{LINE}" stroke-width="30" stroke-linecap="round"/><path d="M{mx - 22} {my + 22} L{mx + 4} {my - 2}" stroke="{SK}" stroke-width="17" stroke-linecap="round"/>'
    f += f'<path d="M{mx - 12} {my - 8} Q{mx + 6} {my - 30} {mx + 26} {my - 4} Q{mx + 8} {my - 14} {mx - 12} {my - 8}Z" fill="{SK}" stroke="{LINE}" stroke-width="6" stroke-linejoin="round"/>'
    f += f'<path d="M{mx + 22} {my + 6} Q{mx + 18} {my + 20} {mx + 4} {my + 18}" stroke="{LINE}" stroke-width="6" fill="none" stroke-linecap="round"/>'
    inner += f
    b += f'<g clip-path="url(#wclip)">{inner}</g>'
    # membrane shine
    b += f'<circle cx="{WX}" cy="{WY}" r="{WR}" fill="none" stroke="#ffd2c8" stroke-width="14" opacity=".7"/>'
    b += f'<circle cx="{WX}" cy="{WY}" r="{WR}" fill="none" stroke="{LINE}" stroke-width="7" opacity=".7"/>'
    b += f'<path d="M{WX - 330} {WY - 170} A{WR - 40} {WR - 40} 0 0 1 {WX - 120} {WY - 360}" stroke="#fff" stroke-width="22" fill="none" opacity=".55" stroke-linecap="round"/>'
    b += f'<path d="M{WX + 300} {WY + 230} A{WR - 40} {WR - 40} 0 0 1 {WX + 180} {WY + 320}" stroke="#fff" stroke-width="12" fill="none" opacity=".35" stroke-linecap="round"/>'
    b += spark(mx - 110, my - 60, 26) + spark(mx - 160, my + 100, 16) + spark(1760, 220, 18, '#ffd8e0') + spark(980, 160, 14, '#ffd8e0')
    b += '</g>'
    # frog doctor with a head mirror and stethoscope on the bubble
    FRX, FRY, FS = 230, 1700, 2.6
    mirror = ('<path d="M-30 -86 Q8 -104 46 -86" fill="none" stroke="#e8e8f0" stroke-width="8"/>'
              '<circle cx="6" cy="-104" r="17" fill="#dfe8f2" stroke-width="4"/><circle cx="6" cy="-104" r="7" fill="#fff" stroke="none"/>')
    coat = f'<g clip-path="url(#fbody)"><rect x="-50" y="-44" width="110" height="70" fill="#f4f6fb" stroke-width="3"/><path d="M-2 -44 L8 -10 L18 -44" fill="#7ac0b8" stroke-width="2.6"/></g><path d="{BODY}" fill="none" stroke-width="4"/>'
    steth = '<path d="M-20 -50 Q-10 -20 6 -18 Q22 -20 32 -50" fill="none" stroke="#3a3a4a" stroke-width="5"/>'
    b += L.frog(FRX, FRY, FS, look=(6, -4), mouth='O', armL='M-34 -24 q-14 -14 -20 -34', armR='M38 -22 q14 -14 20 -34', top=mirror, mid=coat + steth, shadow=False)
    b += darkband(860, 1240, .45)
    b += '<rect width="1080" height="1920" fill="url(#vig3)"/>'
    lines = [('CHOSEN BEFORE', 125, 'w'), ('BIRTH?', 250, 'y')]
    return vpage('#0e0310', vsvg(d, b), lines, outline='#14040e', top=900)


if __name__ == '__main__':
    open(os.path.join(HERE, 'A.html'), 'w').write(make()); print('ok')
