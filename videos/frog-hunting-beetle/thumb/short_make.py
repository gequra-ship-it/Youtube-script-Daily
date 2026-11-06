# Shorts thumbnails (guideline 16-9, 2026-11-06 vertical 1080x1920, centred text). Reuses the drawing helpers of make.py (larva, frog, beetle, grass...).
# Run: python3 videos/frog-hunting-beetle/thumb/short_make.py   -> videos/frog-hunting-beetle-shortN/thumb/A.html (+ common.css, font)
import os, shutil
HERE = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(HERE, 'make.py')).read().split('for name, fn in')[0]
exec(compile(src, 'make.py', 'exec'), globals())
from thumb_lib import vpage, vsvg
REPO = os.path.abspath(os.path.join(HERE, '../../..'))


def scene_bg(top, mid, bot, glow=None):
    D = FILTERS + LARVA_DEFS + lin('sk', [(0, top), (.55, mid), (1, bot)]) + lin('gr', [(0, '#1b2416'), (.4, '#10170d'), (1, '#050804')])
    b = '<rect width="1080" height="1920" fill="url(#sk)"/>'
    if glow:
        D += rad('gl', glow[0], glow[1], 800, [(0, '#fff3cf', .8), (.25, '#ffe2a0', .35), (1, mid, 0)])
        b += '<rect width="1080" height="1920" fill="url(#gl)"/>'
    for _ in range(70):
        b += grass(random.randint(-20, 1100), 1700, random.randint(90, 330), random.randint(-40, 40), random.choice(['#06201d', '#082622', '#0a2c26']), w=random.randint(6, 12))
    b += '<path d="M0,1700 C300,1680 700,1710 1080,1690 L1080,1920 L0,1920Z" fill="url(#gr)"/>'
    return D, b


ARMS = ('M-34 -22 q-14 6 -16 22', 'M38 -22 q14 6 16 22')


def s1():
    random.seed(1); D, b = scene_bg('#03141a', '#0a2a2c', '#0f3a33', (540, 380))
    b += larva(((930, 640), (800, 520), (560, 560), (430, 440)), W=62, opn=.55, head_rot=-10, ants=((-60, 3.4, -70), (30, 3.4, 60)), legs='walk', vside=1, light=(-.6, -.8), rim='#fff1c4')
    for k, (cx, cy, r) in enumerate(((330, 330, 90), (400, 270, 130), (510, 300, 130))):
        b += f'<path d="M{cx-r} {cy} Q{cx} {cy-r*0.9} {cx+r} {cy}" fill="none" stroke="#fff3c0" stroke-width="8" stroke-linecap="round" opacity="{.8-k*.2:.1f}" stroke-dasharray="24 20"/>'
    b += '<ellipse cx="540" cy="1790" rx="300" ry="26" fill="#000" opacity=".5" filter="url(#b8)"/>' + frog(540, 1780, 5.2, mouth=None, look=(5, -7), arms=ARMS, rim='#fff3c0')
    b += spark(250, 900, 18) + spark(880, 1300, 14) + '<text x="700" y="1400" font-family="Fredoka" font-weight="700" font-size="150" fill="#fff6d6" stroke="#1d2b1c" stroke-width="8" paint-order="stroke">?</text>'
    return vpage('#03141a', vsvg(D, b), [('A DANCE', 190, 'w'), ('TRAP', 290, 'y')], outline='#02100f', top=790)


def s2():
    random.seed(2); D, b = scene_bg('#10222c', '#1a3a3a', '#27483a', (540, 360))
    D += lin('tg', [(0, '#ffb9c4'), (1, '#d8607a')])
    b += '<path d="M548 1400 C560 1100 700 800 760 480" fill="none" stroke="#7a2f33" stroke-width="58" stroke-linecap="round"/><path d="M548 1400 C560 1100 700 800 760 480" fill="none" stroke="url(#tg)" stroke-width="40" stroke-linecap="round"/><circle cx="762" cy="470" r="44" fill="#d8607a" stroke="#7a2f33" stroke-width="9"/>'
    for k in range(6):
        b += f'<path d="M{880+k*30} {1180-k*70} L{890+k*30} {700-k*70}" stroke="#fff6d6" stroke-width="5" opacity=".3"/>'
    b += '<ellipse cx="540" cy="1790" rx="300" ry="26" fill="#000" opacity=".5" filter="url(#b8)"/>' + frog(540, 1780, 5.6, mouth='wide', look=(0, -8), arms=ARMS, rim='#fff3c0')
    b += larva(((120, 560), (200, 640), (380, 560), (440, 420)), W=54, opn=.15, head_rot=-35, ants=((-70, 3.2, -50), (-20, 3.2, -30)), legs='walk', vside=1, light=(.6, -1), rim='#fff6d6')
    b += spark(300, 300, 18) + spark(900, 340, 14)
    return vpage('#10222c', vsvg(D, b), [('DODGED!', 200, 'y')], outline='#06141a', top=830)


def s3():
    random.seed(3); D, b = scene_bg('#1a1430', '#2c2147', '#3b2a55', (540, 800))
    b += '<ellipse cx="540" cy="1800" rx="420" ry="30" fill="#000" opacity=".5" filter="url(#b14)"/>'
    b += '<g transform="rotate(-8 540 1700)">' + frog(540, 1790, 6.6, mouth='o', look=(5, -5), arms=ARMS) + '</g>'
    b += larva(((760, 1500), (730, 1420), (820, 1330), (730, 1280)), W=34, opn=.0, head_rot=0, ants=((-40, 3.2, -40), (40, 3.2, 40)), legs='flail', vside=1, light=(-.6, -.8), rim='#fff1c4')
    b += shake(130, 1250, 1.3, flip=True) + shake(950, 1220, 1.4) + sweat(200, 1050, 1.5, -30) + sweat(860, 1020, 1.4, 30)
    b += spark(130, 1500, 16) + spark(960, 1550, 14)
    return vpage('#1a1430', vsvg(D, b), [("CAN'T", 200, 'w'), ('SHAKE IT', 215, 'y')], outline='#0c0818', top=560)


def s4():
    random.seed(4); D, b = scene_bg('#060a1e', '#101d3a', '#17304a', (540, 300))
    b += '<circle cx="540" cy="330" r="150" fill="#fff6dc" opacity=".95" filter="url(#b4)"/>'
    b += '<ellipse cx="400" cy="1790" rx="300" ry="26" fill="#000" opacity=".55" filter="url(#b14)"/>' + frog(380, 1780, 5.4, mouth='o', look=(-6, 0), arms=ARMS, flip=True, rim='#cfe7ff')
    b += '<ellipse cx="800" cy="1780" rx="210" ry="22" fill="#000" opacity=".55" filter="url(#b8)"/>' + beetle(790, 1700, 180, 1.3)
    b += '<path d="M620 1520 q-30 -26 -60 0 M630 1460 q-24 -22 -50 0" fill="none" stroke="#fff3d0" stroke-width="7" stroke-linecap="round" opacity=".8"/>'
    b += sweat(230, 1300, 1.3, -30) + spark(900, 1400, 16) + spark(150, 800, 14)
    return vpage('#060a1e', vsvg(D, b), [('FROM', 210, 'w'), ('BEHIND', 260, 'y')], outline='#070818', top=700)


def s5():
    random.seed(5); D, b = scene_bg('#16202a', '#223442', '#2d4654', (540, 500))
    b += '<ellipse cx="540" cy="430" rx="420" ry="340" fill="#cfe9ef" opacity=".28" stroke="#e9fbff" stroke-width="12"/><ellipse cx="540" cy="430" rx="370" ry="295" fill="#b4d8de" opacity=".25"/>'
    for _ in range(90):
        x = 540 + random.uniform(-330, 330); y = 430 + random.uniform(-260, 260)
        if ((x - 540) / 340) ** 2 + ((y - 430) / 270) ** 2 > 1: continue
        a = random.uniform(0, 180)
        b += f'<g transform="translate({x:.0f} {y:.0f}) rotate({a:.0f})"><ellipse rx="24" ry="8" fill="#e2ad5f" stroke="#5a3a12" stroke-width="2.5"/><circle cx="21" cy="0" r="7" fill="#d39a35" stroke="#5a3a12" stroke-width="2.5"/></g>'
    b += '<ellipse cx="480" cy="1790" rx="280" ry="24" fill="#000" opacity=".5" filter="url(#b8)"/>' + frog(480, 1780, 5.2, mouth=None, look=(6, -6), arms=('M-34 -22 q-14 6 -16 22', 'M38 -22 q10 -8 4 -22'), rim='#fff3c0')
    b += '<g transform="translate(660 1470) rotate(-30)"><circle r="50" fill="#bfe8ee" opacity=".5" stroke="#f2d27a" stroke-width="13"/><rect x="44" y="-10" width="96" height="20" rx="9" fill="#f2d27a" stroke="#1d2b1c" stroke-width="4"/></g>'
    b += spark(120, 300, 18) + spark(980, 250, 14)
    return vpage('#16202a', vsvg(D, b), [('420', 300, 'y'), ('LARVAE', 215, 'w')], outline='#07101a', top=860)


for n, fn in enumerate((s1, s2, s3, s4, s5), 1):
    d = os.path.join(REPO, 'videos', f'frog-hunting-beetle-short{n}', 'thumb'); os.makedirs(d, exist_ok=True)
    for f in ('common.css', 'Fredoka-700.woff2'):
        shutil.copy(os.path.join(REPO, 'tools/assets/thumb_v', f), d)
    open(os.path.join(d, 'A.html'), 'w').write(fn())
