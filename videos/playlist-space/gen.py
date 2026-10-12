import random, math
random.seed(11)
def stars(n, col, y0=0, y1=1080, x0=0, x1=1920, rmax=2.6):
    return ''.join(f'<circle cx="{random.randint(x0,x1)}" cy="{random.randint(y0,y1)}" r="{random.choice([1,1.5,2,rmax]):.1f}" fill="{col}" opacity="{random.uniform(.3,.85):.2f}"/>' for _ in range(n))
def star4(x,y,s,col,op=1):
    return f'<path d="M{x} {y-s} Q{x+s*.15} {y-s*.15} {x+s} {y} Q{x+s*.15} {y+s*.15} {x} {y+s} Q{x-s*.15} {y+s*.15} {x-s} {y} Q{x-s*.15} {y-s*.15} {x} {y-s}Z" fill="{col}" opacity="{op}"/>'
def page(body, style, svg):
    return f'<!doctype html><html><head><meta charset="utf-8"><link rel="stylesheet" href="common.css"><style>{style}</style></head><body><div class="stage">{svg}{body}</div></body></html>'

# ---------- A: Bite-Sized Knowledge - Space (paper) ----------
cx, cy, R = 1000, 360, 232
crumbs=''
for i,(x,y,a,s) in enumerate([(1290,215,20,16),(1360,188,-15,11),(1330,300,30,15),(1395,268,10,10),(1300,395,-20,14),(1405,350,40,11),(1370,425,15,9)]):
    crumbs+=f'<path d="M{x} {y} l{s} {-s*.3} l{s*.2} {s*.8} l{-s*.9} {s*.2}Z" fill="{"#e0b44f" if i%2 else "#2a3a6c"}" transform="rotate({a} {x} {y})"/>'
    crumbs+=f'<path d="M{x-48} {y+14} q14 -8 28 -2" fill="none" stroke="#8d93a8" stroke-width="2.5" stroke-linecap="round" opacity=".7"/>'
svgA=f'''<svg class="art" viewBox="0 0 1920 1080" xmlns="http://www.w3.org/2000/svg"><defs>
<radialGradient id="bg" cx=".45" cy=".4" r=".8"><stop offset="0" stop-color="#eef0dc"/><stop offset="1" stop-color="#d9dcc4"/></radialGradient>
<radialGradient id="pl" cx=".38" cy=".3" r=".85"><stop offset="0" stop-color="#4a5f9e"/><stop offset=".55" stop-color="#2b3c75"/><stop offset="1" stop-color="#1a2552"/></radialGradient>
<radialGradient id="glow" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#fff6c8" stop-opacity=".75"/><stop offset="1" stop-color="#fff6c8" stop-opacity="0"/></radialGradient>
<radialGradient id="sh" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#5b6a5a" stop-opacity=".35"/><stop offset="1" stop-color="#5b6a5a" stop-opacity="0"/></radialGradient>
<mask id="bite"><rect width="1920" height="1080" fill="#fff"/><circle cx="1128" cy="232" r="78" fill="#000"/><circle cx="1190" cy="318" r="66" fill="#000"/><circle cx="1196" cy="392" r="48" fill="#000"/></mask>
<clipPath id="disc"><circle cx="{cx}" cy="{cy}" r="{R-14}"/></clipPath></defs>
<rect width="1920" height="1080" fill="url(#bg)"/>
<circle cx="{cx}" cy="{cy}" r="420" fill="url(#glow)"/>
<ellipse cx="1000" cy="628" rx="260" ry="26" fill="url(#sh)"/>
<g mask="url(#bite)">
<circle cx="{cx}" cy="{cy}" r="{R}" fill="url(#pl)" stroke="#141c40" stroke-width="5"/>
<circle cx="{cx}" cy="{cy}" r="{R-24}" fill="none" stroke="#c9d3f0" stroke-width="2.5" stroke-dasharray="3 11" stroke-linecap="round" opacity=".55"/>
<g clip-path="url(#disc)">
<path d="M770 470 C880 420 1020 430 1230 500 L1230 620 L770 620Z" fill="#3a4f8f" opacity=".7"/>
<ellipse cx="900" cy="500" rx="58" ry="20" fill="#1c2656" opacity=".7" stroke="#8fa0d8" stroke-width="2.5"/>
<ellipse cx="1090" cy="520" rx="40" ry="14" fill="#1c2656" opacity=".7" stroke="#8fa0d8" stroke-width="2.5"/>
<!-- crescent moon -->
<path d="M960 190 a40 40 0 1 0 38 56 a32 32 0 1 1 -38 -56Z" fill="#f2d27a" stroke="#c99a3a" stroke-width="3"/>
<!-- comet -->
<path d="M850 290 L965 262" stroke="#f2d27a" stroke-width="4" stroke-linecap="round" opacity=".5"/><path d="M880 302 L985 280" stroke="#f2d27a" stroke-width="3" stroke-linecap="round" opacity=".4"/>
<circle cx="840" cy="294" r="13" fill="#fff3c4" stroke="#e0b44f" stroke-width="3"/>
<!-- rocket -->
<g transform="translate(1040 330) rotate(20)"><path d="M0 -52 C22 -30 22 10 14 34 L-14 34 C-22 10 -22 -30 0 -52Z" fill="#f4f1e6" stroke="#141c40" stroke-width="3.5"/><circle cx="0" cy="-12" r="9" fill="#7fc7e0" stroke="#141c40" stroke-width="3"/><path d="M-14 14 L-30 40 L-14 32Z M14 14 L30 40 L14 32Z" fill="#b8453c" stroke="#141c40" stroke-width="3"/><path d="M-8 36 Q0 66 8 36Z" fill="#f2a34a"/></g>
<!-- tiny frog astronaut -->
<g transform="translate(985 470)"><ellipse cx="0" cy="26" rx="46" ry="12" fill="#1c2656" opacity=".6"/><path d="M-30 20 C-30 -14 30 -14 30 20Z" fill="#6aa84f" stroke="#26451f" stroke-width="3"/><circle cx="-12" cy="-8" r="9" fill="#fff" stroke="#26451f" stroke-width="3"/><circle cx="-12" cy="-8" r="3.5" fill="#1a1a1a"/><path d="M-2 8 q12 8 24 0" fill="none" stroke="#26451f" stroke-width="3" stroke-linecap="round"/><circle cx="0" cy="4" r="42" fill="#bfe9f0" opacity=".25" stroke="#e8f6fa" stroke-width="3.5"/><path d="M-26 -20 q8 -12 22 -14" fill="none" stroke="#fff" stroke-width="3" stroke-linecap="round" opacity=".8"/></g>
{star4(1180,478,16,"#f2d27a")}{star4(850,420,11,"#f2d27a",.9)}{star4(1000,420,9,"#f2d27a",.8)}
</g></g>
{crumbs}
{star4(1560,140,18,"#c99a3a",.7)}{star4(640,170,14,"#c99a3a",.6)}{star4(1650,560,12,"#c99a3a",.5)}
</svg>'''
styleA='body{background:#dfe2cb}.t{font-family:Fredoka;font-weight:700;position:absolute;line-height:1;white-space:nowrap}#l1{left:80px;top:665px;font-size:150px;color:#b8453c;letter-spacing:2px}#l2{left:80px;top:805px;font-size:150px;color:#1a2330;letter-spacing:2px}#l3{left:90px;top:975px;font-size:46px;color:#4a6b4a}'
bodyA='<div class="t" id="l1">BITE-SIZED</div><div class="t" id="l2">KNOWLEDGE</div><div class="t" id="l3">Miya\'s Lab · one fact, about a minute</div>'
open('A.html','w').write(page(bodyA,styleA,svgA))

# ---------- B: Deep Dives - Space (night) ----------
random.seed(5)
# accretion disc / black hole
bh=(1230,980)
svgB=f'''<svg class="art" viewBox="0 0 1920 1080" xmlns="http://www.w3.org/2000/svg"><defs>
<linearGradient id="bg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#0b1a3c"/><stop offset=".6" stop-color="#070f2b"/><stop offset="1" stop-color="#050a1d"/></linearGradient>
<radialGradient id="n1" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#2e86a8" stop-opacity=".4"/><stop offset="1" stop-color="#2e86a8" stop-opacity="0"/></radialGradient>
<radialGradient id="n2" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#5b4fb8" stop-opacity=".38"/><stop offset="1" stop-color="#5b4fb8" stop-opacity="0"/></radialGradient>
<radialGradient id="lamp" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#8fe8dc" stop-opacity=".5"/><stop offset="1" stop-color="#8fe8dc" stop-opacity="0"/></radialGradient>
<linearGradient id="beam" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#bff5ea" stop-opacity=".42"/><stop offset="1" stop-color="#bff5ea" stop-opacity="0"/></linearGradient>
<radialGradient id="disk" cx=".5" cy=".5" r=".5"><stop offset=".55" stop-color="#ffe9a8" stop-opacity="0"/><stop offset=".72" stop-color="#f2b84a" stop-opacity=".9"/><stop offset=".86" stop-color="#d9693a" stop-opacity=".55"/><stop offset="1" stop-color="#d9693a" stop-opacity="0"/></radialGradient>
<radialGradient id="cap" cx=".4" cy=".35" r=".8"><stop offset="0" stop-color="#2f4f7a"/><stop offset="1" stop-color="#13243f"/></radialGradient>
<radialGradient id="port" cx=".4" cy=".35" r=".7"><stop offset="0" stop-color="#f3fff5"/><stop offset=".5" stop-color="#a8f0dc"/><stop offset="1" stop-color="#2aa38f"/></radialGradient>
</defs>
<rect width="1920" height="1080" fill="url(#bg)"/>
<circle cx="1450" cy="300" r="620" fill="url(#n2)"/><circle cx="600" cy="880" r="520" fill="url(#n1)"/><circle cx="1750" cy="760" r="380" fill="url(#n1)"/>
{stars(150,"#cfe3ff",0,1080,0,1920)}
{star4(1380,170,20,"#fff4c8",.9)}{star4(1700,420,14,"#fff4c8",.7)}{star4(1120,330,11,"#bfe9f0",.7)}{star4(300,820,13,"#bfe9f0",.6)}
<!-- distant spiral galaxy -->
<g transform="translate(1560 270) rotate(-24)"><ellipse rx="150" ry="52" fill="url(#n2)"/><ellipse rx="120" ry="38" fill="none" stroke="#b9a8ff" stroke-width="2.5" opacity=".5"/><path d="M-110 6 C-60 -34 40 -34 110 -4" fill="none" stroke="#cfc4ff" stroke-width="3" opacity=".55" stroke-linecap="round"/><path d="M110 -6 C60 34 -40 34 -110 4" fill="none" stroke="#cfc4ff" stroke-width="3" opacity=".55" stroke-linecap="round"/><ellipse rx="26" ry="14" fill="#fff0c0" opacity=".85"/></g>
<!-- black hole -->
<ellipse cx="{bh[0]}" cy="{bh[1]}" rx="620" ry="130" fill="url(#disk)" transform="rotate(-6 {bh[0]} {bh[1]})"/>
<ellipse cx="{bh[0]}" cy="{bh[1]}" rx="440" ry="80" fill="none" stroke="#ffd98a" stroke-width="3" opacity=".7" transform="rotate(-6 {bh[0]} {bh[1]})"/>
<circle cx="{bh[0]}" cy="{bh[1]}" r="150" fill="#02040c" stroke="#ffe3a0" stroke-width="4" opacity=".98"/>
<path d="M{bh[0]-190} {bh[1]+10} a190 190 0 0 1 380 0" fill="none" stroke="#ffd98a" stroke-width="3" opacity=".45"/>
<!-- probe line from frog's asteroid -->
<path d="M1105 150 C1060 260 940 330 930 425" fill="none" stroke="#8fe8dc" stroke-width="2.5" opacity=".7"/>
{''.join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="#bff5ea" opacity="{o}"/>' for x,y,r,o in [(1075,205,5,.8),(1020,262,4,.7),(978,318,3.5,.6),(950,372,3,.5)])}
<!-- frog on small asteroid -->
<path d="M1000 74 C1030 40 1110 38 1170 62 C1195 74 1200 100 1175 112 C1130 132 1040 128 1005 108 C990 98 990 84 1000 74Z" fill="#3b4c6e" stroke="#9fd0e8" stroke-width="3" opacity=".95"/>
<ellipse cx="1060" cy="64" rx="18" ry="7" fill="#27375a" stroke="#9fd0e8" stroke-width="2" opacity=".8"/>
<g transform="translate(1100 46)"><path d="M-34 24 C-34 -18 34 -18 34 24Z" fill="#6aa84f" stroke="#cfeeb0" stroke-width="3"/><circle cx="-12" cy="-8" r="10" fill="#fff" stroke="#26451f" stroke-width="3"/><circle cx="-12" cy="-8" r="4" fill="#1a1a1a"/><path d="M0 10 q12 8 24 0" fill="none" stroke="#26451f" stroke-width="3" stroke-linecap="round"/><circle cx="0" cy="4" r="46" fill="#bfe9f0" opacity=".18" stroke="#e8f6fa" stroke-width="3.5"/></g>
<!-- capsule -->
<circle cx="930" cy="510" r="190" fill="url(#lamp)"/>
<path d="M880 590 L780 930 L1080 930 L980 590Z" fill="url(#beam)"/>
<path d="M870 600 l-34 34 M990 600 l34 34 M836 634 h56 M1024 634 h-56" fill="none" stroke="#8fe8dc" stroke-width="3.5" stroke-linecap="round" opacity=".85"/>
<rect x="915" y="418" width="30" height="16" rx="4" fill="#13243f" stroke="#8fe8dc" stroke-width="3"/>
<circle cx="930" cy="510" r="84" fill="url(#cap)" stroke="#8fe8dc" stroke-width="4"/>
<circle cx="930" cy="510" r="46" fill="url(#port)" stroke="#f1e2a8" stroke-width="5"/>
<circle cx="916" cy="494" r="9" fill="#fff" opacity=".9"/>
{''.join(f'<circle cx="{930+68*math.cos(a):.0f}" cy="{510+68*math.sin(a):.0f}" r="4.5" fill="#bff5ea" opacity=".9"/>' for a in [i*math.pi/4 for i in range(8)] )}
<!-- small drifting rocks and a comet -->
<path d="M1260 560 L1330 540" stroke="#cfe3ff" stroke-width="3" stroke-linecap="round" opacity=".35"/><circle cx="1350" cy="535" r="9" fill="#fff3c4" opacity=".9"/>
<path d="M1100 700 c8 -10 26 -10 30 2 c4 12 -8 20 -22 18 c-12 -2 -16 -10 -8 -20Z" fill="#33466c" stroke="#9fd0e8" stroke-width="2.5" opacity=".7"/>
<path d="M1500 650 c8 -9 22 -9 26 2 c3 10 -7 17 -19 15 c-10 -2 -14 -9 -7 -17Z" fill="#33466c" stroke="#9fd0e8" stroke-width="2.5" opacity=".6"/>
</svg>'''
styleB='body{background:#070f2b}.t{font-family:Fredoka;font-weight:700;position:absolute;line-height:1;white-space:nowrap;-webkit-text-stroke:10px #040a1e;paint-order:stroke fill}#l1{left:84px;top:118px;font-size:225px;color:#F2D27A;letter-spacing:6px}#l2{left:80px;top:338px;font-size:225px;color:#fff;letter-spacing:10px}#l3{left:92px;top:582px;font-size:48px;color:#c8f0f4;line-height:1.25;-webkit-text-stroke:7px #040a1e;white-space:normal;width:760px}'
bodyB='<div class="t" id="l1">DEEP</div><div class="t" id="l2">D<span style="margin-right:4px">I</span>VES</div><div class="t" id="l3">Miya\'s Lab · one big question, explored in depth</div>'
open('B.html','w').write(page(bodyB,styleB,svgB))
