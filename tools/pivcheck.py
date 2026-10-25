# usage: python3 tools/pivcheck.py <slug>   (after build3) lists every chain/joint/rotor/grow/flip pivot that lands >40 px from its part (tails that would turn away from the body)
import re,sys,os,json
sys.path.insert(0,__import__('os').path.dirname(__import__('os').path.abspath(__file__)))
from paths import chrome
from playwright.sync_api import sync_playwright
slug=sys.argv[1]; vert=slug.endswith(tuple(f'short{i}' for i in range(1,10)))
W,H=(1080,1920) if vert else (1920,1080)
p=os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),'render',slug,'index.html')
html=open(p).read()
items=re.findall(r'gsap\.utils\.toArray\("([^"]+)"\)\[0\][^;]*?',html)
pv=re.findall(r'miyaPv\(gsap\.utils\.toArray\("([^"]+)"\)\[0\],(-?[\d.]+),(-?[\d.]+)\)',html)
pv=sorted(set(pv))
JS='''([sel,x,y])=>{const g=document.querySelector(sel);if(!g)return null;const t=g.closest('.t');const pd=t?t.style.display:'',pvv=t?t.style.visibility:'';
const o=miyaPv(g,x,y).split(' ').map(Number);if(t){t.style.display='block';t.style.visibility='hidden';}
let r;try{const b=g.getBBox();const dx=Math.max(b.x-o[0],0,o[0]-b.x-b.width),dy=Math.max(b.y-o[1],0,o[1]-b.y-b.height);r=[Math.hypot(dx,dy),Math.round(b.width),Math.round(b.height)];}catch(e){r=['err'+e]}
if(t){t.style.display=pd;t.style.visibility=pvv;}return r;}'''
with sync_playwright() as pw:
    b=pw.chromium.launch(executable_path=chrome(),args=['--no-sandbox']);pg=b.new_page(viewport={'width':W,'height':H})
    pg.goto('file://'+p);pg.wait_for_timeout(1500)
    bad=0
    for s,x,y in pv:
        r=pg.evaluate(JS,[s,float(x),float(y)])
        if r is None or isinstance(r[0],str) or r[0]>40:
            bad+=1;print(slug,s,x,y,r)
    print(slug,'pivots',len(pv),'bad',bad)
    b.close()
