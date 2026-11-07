import os, sys, random, shutil
REPO=os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.insert(0, REPO+'/tools')
HERE=REPO+'/videos/parasite-monster-frogs/thumb'
OUT=os.path.join(os.path.dirname(os.path.abspath(__file__)),'glow_sample'); os.makedirs(OUT,exist_ok=True)  # writes A.html here; copy to videos/<slug>-shortN/thumb/ for a real short
src=open(HERE+'/make.py').read(); src=src[:src.index("for n, fn in (('A', thumb_A)")]
NS={'__file__':HERE+'/make.py'}; exec(compile(src,'make.py','exec'),NS)
globals().update({k:v for k,v in NS.items() if not k.startswith('__')})
from thumb_lib import vpage, vsvg, spark
W,H=1080,1920
random.seed(7)

def reeds(n,x0,x1,ybase,hmin,hmax,col,w=4,op=1):
    out=''
    for _ in range(n):
        x=random.randint(x0,x1); h=random.randint(hmin,hmax); bend=random.randint(-30,30)
        out+=f'<path d="M{x} {ybase} q{bend/3:.0f} {-h/2:.0f} {bend} {-h}" stroke="{col}" stroke-width="{w}" fill="none" opacity="{op}" stroke-linecap="round"/>'
        if random.random()<.25: out+=f'<ellipse cx="{x+bend}" cy="{ybase-h+18}" rx="7" ry="22" fill="#1a2a1a" opacity="{op}"/>'
    return out
def lily(lx,ly,lr,col='#4f8a3e'):
    return f'<path d="M{lx} {ly} m{lr} 0 a{lr} {lr*.38:.0f} 0 1 1 -8 -10 l-{lr-8} 10z" fill="{col}" stroke="#0e2a1c" stroke-width="3"/>'
defs=FILTERS+lin('sky',[(0,'#070d24'),(.45,'#143a4a'),(1,'#2c7a78')])
defs+=lin('wat',[(0,'#1d6a66'),(.25,'#0e3a40'),(1,'#050f16')])
defs+=rad('moon',540,360,520,[(0,'#e8fff4',.95),(.25,'#9ff0e0',.45),(1,'#9ff0e0',0)])
defs+=rad('halo',540,640,520,[(0,'#fff3a8',.95),(.35,'#7ff5d8',.45),(1,'#7ff5d8',0)])
defs+=rad('vig',540,960,1250,[(0,'#000',0),(.55,'#000',0),(1,'#000',.7)])
defs+=lin('pole',[(0,'#8a5a2e'),(.5,'#d9a066'),(1,'#6a3e1c')],x2=1,y2=0)
HZ=720
b=f'<rect width="{W}" height="{HZ+10}" fill="url(#sky)"/>'
for _ in range(90):
    b+=f'<circle cx="{random.randint(0,W)}" cy="{random.randint(0,HZ-60)}" r="{random.choice([1.2,1.8,2.4])}" fill="#eaffff" opacity="{random.uniform(.3,.9):.2f}"/>'
b+=f'<rect width="{W}" height="{H}" fill="url(#moon)"/>'
b+='<circle cx="540" cy="360" r="120" fill="#f4fffa" opacity=".9"/><circle cx="505" cy="335" r="22" fill="#cfe9e2" opacity=".6"/><circle cx="580" cy="395" r="30" fill="#cfe9e2" opacity=".5"/>'
# god rays
for x0,x1 in ((120,330),(330,420),(700,760),(820,990)):
    b+=f'<path d="M540 360 L{x0} {H} L{x1} {H}Z" fill="#bffff0" opacity=".05"/>'
b+=f'<path d="M0 {HZ-70} q200 -70 380 -24 q240 -66 420 -10 q160 -34 280 0 L{W} {HZ} L0 {HZ}z" fill="#0f3a3a"/>'
b+=f'<path d="M0 {HZ-20} q300 -34 560 -6 q300 -22 520 4 L{W} {HZ} L0 {HZ}z" fill="#07262a"/>'
b+=reeds(70,0,W,HZ+4,40,120,'#041a1c',4)
b+=f'<rect y="{HZ}" width="{W}" height="{H-HZ}" fill="url(#wat)"/>'
b+=f'<path d="M0 {HZ} L{W} {HZ}" stroke="#bffff0" stroke-width="4" opacity=".7"/>'
b+=f'<rect x="440" y="{HZ}" width="200" height="1100" fill="#bffff0" opacity=".12" filter="url(#b24)"/>'
for _ in range(45):
    y=random.randint(HZ+10,1880); b+=f'<path d="M{random.randint(-40,1080)} {y} l{random.randint(30,50+(y-HZ)//8)} 0" stroke="#9ff0e0" stroke-width="{2+(y-HZ)/600:.1f}" opacity=".22"/>'
b+='<ellipse cx="540" cy="1330" rx="330" ry="90" fill="#fff3a8" opacity=".28" filter="url(#b50)"/>'
for r in (50,95,150,210):
    b+=f'<ellipse cx="540" cy="1300" rx="{r*1.4:.0f}" ry="{r*.26:.0f}" fill="none" stroke="#e6fff4" stroke-width="3" opacity="{.75-r/300:.2f}"/>'
for lx,ly,lr in ((860,1380,78),(960,1520,60),(120,1300,54),(720,1740,96)):
    b+=lily(lx,ly,lr,'#2f6a3a')
HX,HY,HRX,HRY=540,300,350,108
b+=f'<path d="M{HX+HRX-24} {HY-14} L1180 -60" stroke="#0a0604" stroke-width="44" stroke-linecap="round"/><path d="M{HX+HRX-24} {HY-14} L1180 -60" stroke="url(#pole)" stroke-width="32" stroke-linecap="round"/>'
bag=f'M{HX-HRX} {HY} C{HX-HRX+10} {HY+290} {HX-150} {HY+450} {HX} {HY+450} C{HX+160} {HY+450} {HX+HRX-10} {HY+290} {HX+HRX} {HY} Z'
defs+=f'<clipPath id="bag1"><path d="{bag}"/></clipPath>'
b+=f'<ellipse cx="{HX}" cy="{HY+240}" rx="520" ry="440" fill="url(#halo)"/>'
b+=f'<path d="{bag}" fill="#0b2a2a" opacity=".45"/>'
mesh=lambda off,col,op:(f'<g clip-path="url(#bag1)" stroke="{col}" stroke-width="2.6" opacity="{op}">'+''.join(f'<path d="M{HX-560+off+k*36} {HY-40} l460 580 M{HX+560-off-k*36} {HY-40} l-460 580"/>' for k in range(-20,34))+'</g>')
b+=mesh(0,'#d8fff0',.4)
b+=f'<path d="M{HX-HRX} {HY} A{HRX} {HRY} 0 0 1 {HX+HRX} {HY}" stroke="#0a1014" stroke-width="22" fill="none"/><path d="M{HX-HRX} {HY} A{HRX} {HRY} 0 0 1 {HX+HRX} {HY}" stroke="#9fb0b8" stroke-width="13" fill="none"/>'
b+=monster(HX,HY+360,3.3,extra=4,mouth='smile',look=(-2,2),glow='#fff3a8')
b+=mesh(20,'#f4fffa',.3)
b+=f'<path d="{bag}" fill="none" stroke="#e8fff4" stroke-width="4" opacity=".8"/>'
b+=f'<path d="M{HX-HRX} {HY} A{HRX} {HRY} 0 0 0 {HX+HRX} {HY}" stroke="#0a1014" stroke-width="26" fill="none"/><path d="M{HX-HRX} {HY} A{HRX} {HRY} 0 0 0 {HX+HRX} {HY}" stroke="#c0ccd2" stroke-width="16" fill="none"/>'
for dx,dy in ((HX-40,HY+480),(HX+30,HY+520),(HX-10,HY+590),(HX+70,HY+470)):
    b+=f'<path d="M{dx} {dy-14} q9 14 0 21 q-9 -7 0 -21z" fill="#dff6ff" stroke="#2c5a6a" stroke-width="2.6"/>'
for sx,sy,ss in ((HX-400,HY+40,26),(HX+420,HY+230,22),(HX-380,HY+380,18),(HX+150,HY-110,18),(HX+300,HY+420,20)):
    b+=spark(sx,sy,ss,col='#fffbe0')
# fireflies
for _ in range(60):
    x,y=random.randint(0,W),random.randint(260,1850); r=random.choice([3,4,6])
    b+=f'<circle cx="{x}" cy="{y}" r="{r*3}" fill="#fff3a8" opacity=".18" filter="url(#b6)"/><circle cx="{x}" cy="{y}" r="{r}" fill="#fffbd0" opacity=".9"/>'
b+='<rect x="-50" y="860" width="1180" height="380" fill="#000" opacity=".4" filter="url(#b50)"/>'
b+='<path d="M40 1720 q14 -130 230 -140 q230 -6 260 140z" fill="#2a3a38" stroke="#0e1a18" stroke-width="5"/><ellipse cx="290" cy="1724" rx="300" ry="26" fill="#000" opacity=".3" filter="url(#b12)"/>'
back='<rect x="-52" y="-58" width="34" height="52" rx="10" fill="#d9733a" stroke-width="3.2"/>'
torso='<path d="M-26 -40 q4 22 -2 40 M34 -40 q-4 22 2 40" stroke="#b5562a" stroke-width="6" fill="none"/>'
hat='<path d="M-30 -84 q34 -48 70 0z" fill="#f2c94c" stroke-width="3.4"/><path d="M-44 -82 q50 -14 98 0 q-50 10 -98 0z" fill="#e8b93a" stroke-width="3.4"/>'
b+=f'<ellipse cx="290" cy="1560" rx="230" ry="200" fill="#fff3a8" opacity=".18" filter="url(#b24)"/>'
b+=frog(290,1600,3.3,mouth='o',arms=('q-18 -6 -22 -30','q18 -6 22 -30'),look=(5,-6),back=back,torso=torso,head=hat,sweat=True)
b+=f'<rect width="{W}" height="{H}" fill="url(#vig)"/>'
lines=[('TOO MANY',160,'w'),('LEGS',260,'y')]
shutil.copy(REPO+'/tools/assets/thumb_v/common.css',OUT); shutil.copy(REPO+'/tools/assets/thumb_v/Fredoka-700.woff2',OUT)
open(OUT+'/A.html','w').write(vpage('#070d24',vsvg(defs,b),lines,outline='#04101a',top=860))
