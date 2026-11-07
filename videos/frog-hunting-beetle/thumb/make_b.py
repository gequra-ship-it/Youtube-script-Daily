# STYLE B shorts thumbnails for frog-hunting-beetle (guideline 16-9 B, miya 2026-11-07): dark scene, ONE big glowing concrete subject in the top half
# (y 180-840), centred 2-line hook on a dark band (y 860-1240), frog + foreground in the bottom third. Hooks only from the short scripts, no invented numbers.
#   python3 videos/frog-hunting-beetle/thumb/make_b.py -> videos/frog-hunting-beetle-short{1..5}/thumb/A.html
# short1 THE TRAP / IS A DANCE   glowing larva waving antennae + jaws (S1: "the trap is a dance")
# short2 IT DODGED / THE TONGUE  pink tongue hits empty ground, larva leaps aside (S2: "almost always dodges the strike")
# short3 CAN'T / SHAKE IT        glowing larva jaws clamped on, big open curved jaws (S3: "curved jaws hold firm")
# short4 BITES FROM / BEHIND     glowing adult beetle (S4: "attack from behind", adult hunts amphibians)
# short5 420 / LARVAE            glowing dish of larvae (S5: "420 larvae", 382 encounters)
import os, shutil, math, random
HERE = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(HERE, 'make.py')).read().split('for name, fn in')[0]
exec(compile(src, 'make.py', 'exec'), globals())
from thumb_lib import vpage, vsvg, halo, fireflies, darkband
REPO = os.path.abspath(os.path.join(HERE, '../../..'))
_frog = frog
HZ = 860


def frog(x, y, s, look=(0, 0), **kw):   # clamp pupil offset so pupils stay fully inside the eye white (eyecheck)
    dx, dy = look; m = math.hypot(dx, dy)
    if m > 5.4: dx, dy = dx * 5.4 / m, dy * 5.4 / m
    return _frog(x, y, s, look=(dx, dy), **kw)


ARMS = ('M-34 -22 q-14 6 -16 22', 'M38 -22 q14 6 16 22')


def base(top, mid, bot, hx, hy, seed, ffcol='#fff3a8', hin='#fff3cf', hout='#7ff5d8', band=.5, gnd='#050804'):
    random.seed(seed)
    D = FILTERS + LARVA_DEFS + lin('sk', [(0, top), (.55, mid), (1, bot)]) + lin('gr', [(0, '#1b2416'), (.4, '#10170d'), (1, gnd)])
    D += halo('hh', hx, hy, 560, inner=hin, outer=hout)
    D += rad('vig', 540, 960, 1250, [(0, '#000', 0), (.55, '#000', 0), (1, '#000', .7)])
    b = '<rect width="1080" height="1920" fill="url(#sk)"/>' + f'<ellipse cx="{hx}" cy="{hy}" rx="560" ry="560" fill="url(#hh)"/>'
    return D, b


def foreground(b):
    for _ in range(60):
        b += grass(random.randint(-20, 1100), 1720, random.randint(90, 280), random.randint(-40, 40), random.choice(['#06201d', '#082622', '#0a2c26']), w=random.randint(6, 12))
    return b + '<path d="M0,1720 C300,1700 700,1730 1080,1710 L1080,1920 L0,1920Z" fill="url(#gr)"/>'


def finish(D, b, lines, bg, outline, top=880, ff=('#fff3a8', '#fffbd0'), seed=7):
    b += darkband(HZ, 1250, .5) + fireflies(40, 120, 1800, col=ff[0], core=ff[1], seed=seed)
    b += '<rect width="1080" height="1920" fill="url(#vig)"/>'
    return vpage(bg, vsvg(D, b), lines, outline=outline, top=top)


def s1():
    D, b = base('#03141a', '#0a2a2c', '#0f3a33', 540, 520, 1, hout='#6af0c8')
    b = foreground(b)
    b += larva(((930, 700), (800, 560), (560, 620), (420, 480)), W=74, opn=.6, head_rot=-10, ants=((-60, 3.4, -70), (30, 3.4, 60)), legs='walk', vside=1, light=(-.6, -.8), rim='#fff1c4')
    for k, (cx, cy, r) in enumerate(((300, 340, 90), (380, 270, 140), (500, 290, 140))):
        b += f'<path d="M{cx-r} {cy} Q{cx} {cy-r*0.9} {cx+r} {cy}" fill="none" stroke="#fff3c0" stroke-width="8" stroke-linecap="round" opacity="{.85-k*.2:.2f}" stroke-dasharray="24 20"/>'
    b += spark(180, 600, 20) + spark(930, 330, 16)
    b += '<ellipse cx="540" cy="1810" rx="300" ry="26" fill="#000" opacity=".5" filter="url(#b8)"/>' + frog(540, 1800, 4.0, mouth='o', look=(4, -5), arms=ARMS, rim='#fff3c0')
    return finish(D, b, [('THE TRAP', 190, 'w'), ('IS A DANCE', 160, 'y')], '#03141a', '#02100f')


def s2():
    D, b = base('#10222c', '#1a3a3a', '#27483a', 540, 520, 2, hout='#ffb9c4')
    D += lin('tg', [(0, '#ffb9c4'), (1, '#e0607a')])
    b = foreground(b)
    tp = 'M1120 700 C980 760 860 620 700 520'
    b += f'<path d="{tp}" fill="none" stroke="#fff0c8" stroke-width="110" stroke-linecap="round" opacity=".18" filter="url(#b26)"/>'
    b += f'<path d="{tp}" fill="none" stroke="#7a2f33" stroke-width="66" stroke-linecap="round"/><path d="{tp}" fill="none" stroke="url(#tg)" stroke-width="46" stroke-linecap="round"/>'
    b += '<circle cx="696" cy="520" r="52" fill="#e0607a" stroke="#7a2f33" stroke-width="9"/><circle cx="680" cy="504" r="14" fill="#fff" opacity=".5"/>'
    b += '<path d="M640 600 q-30 20 -60 4 M660 640 q-30 14 -54 -6" fill="none" stroke="#fff6d6" stroke-width="6" stroke-linecap="round" opacity=".7"/>'
    b += larva(((120, 700), (200, 780), (380, 700), (450, 560)), W=64, opn=.3, head_rot=-35, ants=((-70, 3.2, -50), (-20, 3.2, -30)), legs='walk', vside=1, light=(.6, -1), rim='#fff6d6')
    b += spark(260, 300, 20) + spark(920, 340, 16)
    b += '<ellipse cx="540" cy="1810" rx="300" ry="26" fill="#000" opacity=".5" filter="url(#b8)"/>' + frog(540, 1800, 4.2, mouth='wide', look=(0, -6), arms=ARMS, rim='#fff3c0')
    return finish(D, b, [('IT DODGED', 180, 'w'), ('THE TONGUE', 170, 'y')], '#10222c', '#06141a', ff=('#ffd0d8', '#fff6f0'))


def s3():
    D, b = base('#1a1430', '#2c2147', '#3b2a55', 540, 520, 3, hout='#c8a0ff')
    b = foreground(b)
    b += larva(((900, 760), (800, 560), (680, 640), (560, 460)), W=96, opn=.0, head_rot=0, ants=((-40, 3.2, -40), (40, 3.2, 40)), legs='flail', vside=1, light=(-.6, -.8), rim='#fff1c4')
    b += shake(130, 460, 1.3, flip=True) + shake(960, 420, 1.4) + spark(200, 700, 18) + spark(900, 260, 16)
    b += '<ellipse cx="540" cy="1810" rx="420" ry="30" fill="#000" opacity=".5" filter="url(#b14)"/>'
    b += '<g transform="rotate(-6 540 1760)">' + frog(540, 1800, 4.4, mouth='o', look=(4, -4), arms=ARMS) + '</g>'
    b += sweat(250, 1500, 1.5, -30) + sweat(830, 1480, 1.4, 30)
    return finish(D, b, [("CAN'T", 190, 'w'), ('SHAKE IT', 200, 'y')], '#1a1430', '#0c0818', ff=('#e0c8ff', '#ffffff'))


def s4():
    D, b = base('#060a1e', '#101d3a', '#17304a', 540, 520, 4, hout='#8ac8ff')
    b = foreground(b)
    b += '<circle cx="540" cy="330" r="150" fill="#fff6dc" opacity=".35" filter="url(#b50)"/>'
    b += beetle(540, 480, 170, 2.0)
    b += '<path d="M180 640 q-30 -26 -60 0 M200 580 q-24 -22 -50 0" fill="none" stroke="#fff3d0" stroke-width="7" stroke-linecap="round" opacity=".8"/>' + spark(160, 340, 20) + spark(940, 300, 16)
    b += '<ellipse cx="540" cy="1810" rx="300" ry="26" fill="#000" opacity=".55" filter="url(#b14)"/>' + frog(540, 1800, 4.2, mouth='o', look=(-4, -4), arms=ARMS, flip=True, rim='#cfe7ff')
    b += sweat(300, 1480, 1.4, -30)
    return finish(D, b, [('BITES FROM', 170, 'w'), ('BEHIND', 240, 'y')], '#060a1e', '#070818', ff=('#cfe7ff', '#ffffff'))


def s5():
    D, b = base('#16202a', '#223442', '#2d4654', 540, 520, 5, hout='#9ad8e8')
    b = foreground(b)
    b += '<ellipse cx="540" cy="520" rx="440" ry="360" fill="#cfe9ef" opacity=".3" stroke="#e9fbff" stroke-width="12"/><ellipse cx="540" cy="520" rx="390" ry="315" fill="#b4d8de" opacity=".25"/>'
    for _ in range(110):
        x = 540 + random.uniform(-350, 350); y = 520 + random.uniform(-280, 280)
        if ((x - 540) / 360) ** 2 + ((y - 520) / 290) ** 2 > 1: continue
        a = random.uniform(0, 180)
        b += f'<g transform="translate({x:.0f} {y:.0f}) rotate({a:.0f})"><ellipse cx="0" cy="0" rx="26" ry="9" fill="#e2ad5f" stroke="#5a3a12" stroke-width="2.5"/><circle cx="23" cy="0" r="8" fill="#d39a35" stroke="#5a3a12" stroke-width="2.5"/></g>'
    b += '<path d="M240 330 Q330 250 470 240" fill="none" stroke="#fff" stroke-width="12" stroke-linecap="round" opacity=".5"/>'
    b += spark(120, 300, 20) + spark(980, 250, 16) + spark(960, 860, 14)
    b += '<ellipse cx="540" cy="1810" rx="300" ry="24" fill="#000" opacity=".5" filter="url(#b8)"/>' + frog(540, 1800, 4.0, mouth=None, look=(5, -4), arms=('M-34 -22 q-14 6 -16 22', 'M38 -22 q10 -8 4 -22'), rim='#fff3c0')
    return finish(D, b, [('420', 300, 'y'), ('LARVAE', 215, 'w')], '#16202a', '#07101a', ff=('#e0f4f8', '#ffffff'))


for n, fn in enumerate((s1, s2, s3, s4, s5), 1):
    d = os.path.join(REPO, 'videos', f'frog-hunting-beetle-short{n}', 'thumb'); os.makedirs(d, exist_ok=True)
    for f in ('common.css', 'Fredoka-700.woff2'):
        shutil.copy(os.path.join(REPO, 'tools/assets/thumb_v', f), d)
    open(os.path.join(d, 'A.html'), 'w').write(fn())
print('ok')
