# Shorts thumbnails (guideline 16-9): one per short, 1920x1080. Reuses the drawing helpers of make.py (larva, frog, beetle, grass...).
# Run: python3 videos/frog-hunting-beetle/thumb/short_make.py   -> videos/frog-hunting-beetle-shortN/thumb/A.html (+ common.css, font)
import os, shutil
HERE = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(HERE, 'make.py')).read().split('for name, fn in')[0]
exec(compile(src, 'make.py', 'exec'), globals())
REPO = os.path.abspath(os.path.join(HERE, '../../..'))


def scene_bg(top, mid, bot, glow=None):
    D = FILTERS + LARVA_DEFS + lin('sk', [(0, top), (.55, mid), (1, bot)]) + lin('gr', [(0, '#1b2416'), (.4, '#10170d'), (1, '#050804')])
    b = '<rect width="1920" height="1080" fill="url(#sk)"/>'
    if glow:
        D += rad('gl', glow[0], glow[1], 700, [(0, '#fff3cf', .8), (.25, '#ffe2a0', .35), (1, mid, 0)])
        b += '<rect width="1920" height="1080" fill="url(#gl)"/>'
    for _ in range(90):
        b += grass(random.randint(-20, 1940), 900, random.randint(70, 260), random.randint(-40, 40), random.choice(['#06201d', '#082622', '#0a2c26']), w=random.randint(6, 12))
    b += '<path d="M0,900 C500,880 1100,910 1920,890 L1920,1080 L0,1080Z" fill="url(#gr)"/>'
    return D, b


def s1():   # short1: the dance lure
    random.seed(1); D, b = scene_bg('#03141a', '#0a2a2c', '#0f3a33', (1350, 420))
    b += '<ellipse cx="1330" cy="930" rx="300" ry="26" fill="#000" opacity=".55" filter="url(#b8)"/>'
    b += larva(((1700, 960), (1600, 800), (1380, 810), (1290, 730)), W=70, opn=.55, head_rot=-10, ants=((-60, 3.4, -70), (30, 3.4, 60)), legs='walk', vside=1, light=(-.6, -.8), rim='#fff1c4')
    for k, (cx, cy, r) in enumerate(((1170, 600, 110), (1250, 540, 150), (1400, 560, 150))):   # waving arcs around the antennae
        b += f'<path d="M{cx-r} {cy} Q{cx} {cy-r*0.9} {cx+r} {cy}" fill="none" stroke="#fff3c0" stroke-width="9" stroke-linecap="round" opacity="{.8-k*.2:.1f}" stroke-dasharray="26 22"/>'
    b += f'<ellipse cx="560" cy="990" rx="260" ry="26" fill="#000" opacity=".5" filter="url(#b8)"/>' + frog(560, 985, 4.2, mouth=None, look=(7, 3), arms=('M-34 -22 q-14 6 -16 22', 'M38 -22 q14 6 16 22'), rim='#fff3c0')
    b += spark(880, 560, 20) + spark(1000, 420, 14) + '<text x="760" y="640" font-family="Fredoka" font-weight="700" font-size="150" fill="#fff6d6" stroke="#1d2b1c" stroke-width="8" paint-order="stroke">?</text>'
    return page('#03141a', svg(D, b), [('A DANCE', 175, 'w'), ('TRAP', 270, 'y')], outline='#02100f')


def s2():   # short2: the strike misses
    random.seed(2); D, b = scene_bg('#10222c', '#1a3a3a', '#27483a', (1100, 380))
    D += lin('tg', [(0, '#ffb9c4'), (1, '#d8607a')])
    for k in range(7):
        b += f'<path d="M{700+k*40} {770-k*30} L{1250+k*30} {750-k*30}" stroke="#fff6d6" stroke-width="5" opacity=".35"/>'
    b += '<path d="M640 830 C900 790 1120 640 1560 560" fill="none" stroke="#7a2f33" stroke-width="62" stroke-linecap="round"/><path d="M640 830 C900 790 1120 640 1560 560" fill="none" stroke="url(#tg)" stroke-width="44" stroke-linecap="round"/><circle cx="1568" cy="556" r="46" fill="#d8607a" stroke="#7a2f33" stroke-width="9"/>'
    b += '<ellipse cx="480" cy="990" rx="270" ry="26" fill="#000" opacity=".5" filter="url(#b8)"/>' + frog(480, 985, 4.2, mouth='wide', look=(8, 0), arms=('M-34 -22 q-14 6 -16 22', 'M38 -22 q14 6 16 22'), rim='#fff3c0')
    b += larva(((1500, 960), (1420, 930), (1250, 960), (1190, 880)), W=64, opn=.15, head_rot=35, ants=((-70, 3.2, -50), (-20, 3.2, -30)), legs='walk', vside=-1, light=(.6, -1), rim='#fff6d6')
    b += spark(1300, 700, 18) + spark(1700, 640, 14)
    return page('#10222c', svg(D, b), [('DODGED!', 230, 'y')], outline='#06141a')


def s3():   # short3: locked on, cannot shake it
    random.seed(3); D, b = scene_bg('#1a1430', '#2c2147', '#3b2a55', (1300, 420))
    b += '<ellipse cx="1000" cy="1000" rx="400" ry="30" fill="#000" opacity=".5" filter="url(#b14)"/>'
    b += '<g transform="rotate(-9 1000 880)">' + frog(1000, 985, 6.4, mouth='o', look=(6, -4), arms=('M-34 -22 q-14 6 -16 22', 'M38 -22 q10 -8 4 -22')) + '</g>'
    b += larva(((1210, 870), (1180, 800), (1270, 700), (1180, 650)), W=40, opn=.0, head_rot=0, ants=((-40, 3.2, -40), (40, 3.2, 40)), legs='flail', vside=1, light=(-.6, -.8), rim='#fff1c4')
    b += shake(560, 560, 1.3, flip=True) + shake(1500, 520, 1.5) + sweat(760, 380, 1.5, -30) + sweat(1330, 340, 1.4, 30) + sweat(600, 700, 1.1, -45)
    b += spark(1430, 760, 18) + spark(500, 800, 14)
    return page('#1a1430', svg(D, b), [("CAN'T", 175, 'w'), ('SHAKE IT', 220, 'y')], outline='#0c0818')


def s4():   # short4: adult beetle from behind
    random.seed(4); D, b = scene_bg('#060a1e', '#101d3a', '#17304a', (1500, 300))
    b += '<circle cx="1500" cy="300" r="130" fill="#fff6dc" opacity=".95" filter="url(#b4)"/>'
    b += '<ellipse cx="760" cy="1000" rx="360" ry="30" fill="#000" opacity=".55" filter="url(#b14)"/>' + frog(760, 995, 5.6, mouth='o', look=(-8, 0), arms=('M-34 -22 q-14 6 -16 22', 'M38 -22 q14 6 16 22'), flip=True, rim='#cfe7ff')
    b += '<ellipse cx="1180" cy="985" rx="220" ry="22" fill="#000" opacity=".55" filter="url(#b8)"/>' + beetle(1190, 905, 180, 1.5)
    b += f'<path d="M1010 760 q-30 -26 -60 0 M1020 700 q-24 -22 -50 0" fill="none" stroke="#fff3d0" stroke-width="7" stroke-linecap="round" opacity=".8"/>'
    b += sweat(560, 520, 1.3, -30) + spark(1380, 700, 16) + spark(1000, 360, 14)
    return page('#060a1e', svg(D, b), [('FROM', 200, 'w'), ('BEHIND', 250, 'y')], outline='#070818')


def s5():   # short5: the lab study, 420 larvae
    random.seed(5); D, b = scene_bg('#16202a', '#223442', '#2d4654', (1300, 400))
    b += '<ellipse cx="1260" cy="470" rx="400" ry="330" fill="#cfe9ef" opacity=".28" stroke="#e9fbff" stroke-width="12"/><ellipse cx="1260" cy="470" rx="350" ry="285" fill="#b4d8de" opacity=".25"/>'
    for _ in range(70):
        x = 1260 + random.uniform(-290, 290); y = 470 + random.uniform(-230, 230)
        if ((x - 1260) / 300) ** 2 + ((y - 470) / 240) ** 2 > 1: continue
        a = random.uniform(0, 180)
        b += f'<g transform="translate({x:.0f} {y:.0f}) rotate({a:.0f})"><ellipse rx="22" ry="7" fill="#e2ad5f" stroke="#5a3a12" stroke-width="2.5"/><circle cx="19" cy="0" r="6" fill="#d39a35" stroke="#5a3a12" stroke-width="2.5"/></g>'
    b += '<ellipse cx="420" cy="1000" rx="250" ry="24" fill="#000" opacity=".5" filter="url(#b8)"/>' + frog(420, 995, 4.2, mouth=None, look=(8, -4), arms=('M-34 -22 q-14 6 -16 22', 'M38 -22 q10 -8 4 -22'), rim='#fff3c0')
    b += '<g transform="translate(560 700) rotate(-30)"><circle r="46" fill="#bfe8ee" opacity=".5" stroke="#f2d27a" stroke-width="12"/><rect x="40" y="-9" width="86" height="18" rx="8" fill="#f2d27a" stroke="#1d2b1c" stroke-width="4"/></g>'
    b += spark(900, 300, 18) + spark(1700, 250, 14)
    return page('#16202a', svg(D, b), [('420', 260, 'y'), ('LARVAE', 175, 'w')], outline='#07101a')


for n, fn in enumerate((s1, s2, s3, s4, s5), 1):
    d = os.path.join(REPO, 'videos', f'frog-hunting-beetle-short{n}', 'thumb'); os.makedirs(d, exist_ok=True)
    for f in ('common.css', 'Fredoka-700.woff2'):
        shutil.copy(os.path.join(HERE, f), d)
    open(os.path.join(d, 'A.html'), 'w').write(fn())
