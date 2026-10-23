# Centre-object motions (guideline 4-1). The picture's round centre object lives in a group
# `mv-core-<type>`; each type below moves it differently, so the object is not always the same
# up-and-down squash. Every tween is finite (repeat count, never -1) so the timeline stays seekable,
# and nothing uses an SVG filter.
import math

# 19 types (13 + 6 taken from a motion-graphics reference on 2026-10-13: pop, ping, stamp, flip, draw, drop).
# Order matters: build3 walks it with a step that never repeats a type in consecutive pictures.
CORE_TYPES = ['spin', 'pop', 'sway', 'orbit', 'ping', 'glide', 'heartbeat', 'draw', 'flicker', 'swell',
              'stamp', 'tremble', 'approach', 'flip', 'reveal', 'squeeze', 'drop', 'wobble', 'roll']

CORE_STEP = 7   # coprime with 19: visits all 19 types before repeating, neighbours always differ


def legacy_core_type(ordinal):
    """Type for a picture whose centre group is still the old `mv-glint-core` (no explicit type)."""
    return CORE_TYPES[(ordinal * CORE_STEP + 3) % len(CORE_TYPES)]


def core_js(ctype, g, t0, v0, sp, ring=None):
    """GSAP lines for one centre object.
    g: JS expression for the element, t0: picture start (s), v0: transition-in start (s),
    sp: seconds the picture stays on screen (plus margin), ring: JS expression for the ring that
    miyaWrapCores() draws around the object (needed by ping and stamp). Returns a list of JS statements."""
    C = 'transformOrigin:"50% 50%"'
    yo = lambda per: f'ease:"sine.inOut",yoyo:true,repeat:{max(int(math.ceil(sp / per)) - 1, 0)},immediateRender:false'
    if ctype == 'spin':        # slow one-way turn (lens, clock, planet, gear)
        return [f'tl.fromTo({g},{{rotation:0,{C}}},{{rotation:{36 * sp:.1f},duration:{sp:.3f},ease:"none",immediateRender:false}},{v0:.3f});']
    if ctype == 'turn':        # (2026-10-19) turns ONLY this group (wind-turbine rotor, fan, propeller); neighbours are not wrapped in, so the tower/body stays still
        return [f'tl.fromTo({g},{{rotation:0,{C}}},{{rotation:{90 * sp:.1f},duration:{sp:.3f},ease:"none",immediateRender:false}},{v0:.3f});']
    if ctype == 'sway':        # pendulum around the top (lamp, bell, key, hanging things)
        return [f'tl.fromTo({g},{{rotation:-14,transformOrigin:"50% 0%"}},{{rotation:14,duration:1.4,{yo(1.4)}}},{v0:.3f});']
    if ctype == 'orbit':       # drifts along a loop: x and y use different periods, so it never just bobs up and down
        return [f'tl.fromTo({g},{{x:-34,y:0}},{{x:34,duration:2.4,{yo(2.4)}}},{v0:.3f});',
                f'tl.fromTo({g},{{y:-26}},{{y:26,duration:3.1,{yo(3.1)}}},{v0:.3f});']
    if ctype == 'glide':       # sideways only
        return [f'tl.fromTo({g},{{x:-60}},{{x:60,duration:2.6,{yo(2.6)}}},{v0:.3f});']
    if ctype == 'heartbeat':   # lub-dub, then rest
        rep = max(int(math.ceil(sp / 0.9)) - 1, 0)
        return [f'tl.set({g},{{scale:1,{C}}},{v0:.3f});',
                f'tl.to({g},{{keyframes:[{{scale:1.14,duration:.12}},{{scale:1,duration:.18}},{{scale:1.09,duration:.12}},{{scale:1,duration:.48}}],repeat:{rep},immediateRender:false}},{v0:.3f});']
    if ctype == 'flicker':     # candle-like uneven light, no movement
        rep = max(int(math.ceil(sp / 1.0)) - 1, 0)
        return [f'tl.set({g},{{opacity:1}},{v0:.3f});',
                f'tl.to({g},{{keyframes:[{{opacity:.45,duration:.12}},{{opacity:1,duration:.18}},{{opacity:.62,duration:.14}},{{opacity:.95,duration:.2}},{{opacity:.35,duration:.1}},{{opacity:1,duration:.26}}],repeat:{rep},immediateRender:false}},{v0:.3f});']
    if ctype == 'swell':       # even growth in all directions
        return [f'tl.fromTo({g},{{scale:1,{C}}},{{scale:1.2,duration:2.2,{yo(2.2)}}},{v0:.3f});']
    if ctype == 'tremble':     # tension: tiny fast shake
        per = 0.07; rep = min(int(math.ceil(sp / per)) - 1, 400)
        return [f'tl.fromTo({g},{{x:-5,rotation:-1.5,{C}}},{{x:5,rotation:1.5,duration:{per},ease:"none",yoyo:true,repeat:{rep},immediateRender:false}},{v0:.3f});']
    if ctype == 'approach':    # slow push toward the viewer, one way
        return [f'tl.fromTo({g},{{scale:1,{C}}},{{scale:1.3,duration:{sp:.3f},ease:"power1.out",immediateRender:false}},{v0:.3f});']
    if ctype == 'reveal':      # appears: fades up and grows into place when the picture starts
        return [f'tl.set({g},{{opacity:.15,scale:.6,{C}}},{v0:.3f});',      # already small/faint while the picture transitions in
                f'tl.to({g},{{opacity:1,scale:1,duration:.7,ease:"power2.out",immediateRender:false}},{t0:.3f});']
    if ctype == 'squeeze':     # horizontal squeeze (a cell, a drop, a bellows)
        return [f'tl.fromTo({g},{{scaleX:1,scaleY:1,{C}}},{{scaleX:.55,scaleY:1.2,duration:1.1,{yo(1.1)}}},{v0:.3f});']
    if ctype == 'wobble':      # springy settle after a hit, then still
        return [f'tl.set({g},{{rotation:30,scale:1.3,{C}}},{v0:.3f});',
                f'tl.to({g},{{rotation:0,scale:1,duration:2.2,ease:"elastic.out(1,.25)",immediateRender:false}},{t0 + .2:.3f});']
    if ctype == 'roll':        # rolls sideways while turning
        return [f'tl.fromTo({g},{{x:-110,rotation:-180,{C}}},{{x:110,rotation:180,duration:{sp:.3f},ease:"power1.inOut",immediateRender:false}},{v0:.3f});']
    if ctype == 'pop':         # pops into place with an overshoot, then still (chips/cards popping in)
        return [f'tl.set({g},{{scale:.2,opacity:0,{C}}},{v0:.3f});',
                f'tl.to({g},{{scale:1,opacity:1,duration:.6,ease:"back.out(2.4)",immediateRender:false}},{t0 + .15:.3f});']
    if ctype == 'ping':        # rings keep spreading out from the object, the object itself stays put
        rep = max(int(math.ceil(sp / 1.3)) - 1, 0)
        return [f'tl.fromTo({ring},{{scale:.85,opacity:.95,{C}}},{{scale:1.8,opacity:0,duration:1.3,ease:"power2.out",repeat:{rep},immediateRender:false}},{v0:.3f});']
    if ctype == 'stamp':       # slams down from big and see-through, a ring bursts out at the hit
        return [f'tl.set({g},{{scale:1.8,opacity:0,{C}}},{v0:.3f});',
                f'tl.to({g},{{scale:1,opacity:1,duration:.28,ease:"power4.in",immediateRender:false}},{t0 + .2:.3f});',
                f'tl.fromTo({ring},{{scale:.9,opacity:1,{C}}},{{scale:1.9,opacity:0,duration:.7,ease:"power2.out",immediateRender:false}},{t0 + .48:.3f});']
    if ctype == 'flip':        # turns over like a card, twice while the picture is on
        rep = max(int(sp // 2.4) - 1, 0)
        return [f'tl.set({g},{{scaleX:1,{C}}},{v0:.3f});',
                f'tl.to({g},{{keyframes:[{{scaleX:0,duration:.2,ease:"power2.in"}},{{scaleX:1,duration:.26,ease:"power2.out"}}],repeat:{rep},repeatDelay:1.94,immediateRender:false}},{t0 + .3:.3f});']
    if ctype == 'draw':        # the outline draws itself, then the colour fills in (sketch -> colour, guideline 4-3)
        return [f'tl.set(miyaStroked({g}),{{strokeDasharray:(i,e)=>e.__len,strokeDashoffset:(i,e)=>e.__len}},{v0:.3f});',
                f'tl.set(miyaFilled({g}),{{opacity:0}},{v0:.3f});',
                f'tl.to(miyaStroked({g}),{{strokeDashoffset:0,duration:1.3,ease:"power1.inOut",stagger:.05,immediateRender:false}},{t0 + .1:.3f});',
                f'tl.to(miyaFilled({g}),{{opacity:(i,e)=>e.__op,duration:.6,ease:"power1.out",stagger:.03,immediateRender:false}},{t0 + .9:.3f});']
    if ctype == 'drop':        # falls in tilted and bounces to rest (tokens dropping into place)
        return [f'tl.set({g},{{y:-160,rotation:-18,opacity:0,{C}}},{v0:.3f});',
                f'tl.to({g},{{y:0,rotation:0,opacity:1,duration:.9,ease:"bounce.out",immediateRender:false}},{t0 + .15:.3f});']
    raise ValueError(ctype)


# The centre group in the pictures only wraps the soft glow; the visible object is drawn right after it as separate
# top-level shapes. Moving/rotating the glow alone is almost invisible, so at page load we wrap the glow together with
# the neighbouring shapes that sit on the centre disc (contiguous in drawing order, so stacking stays the same) and
# move that wrapper instead. cx, cy = centre point of the picture (960,500 landscape; 540,860 vertical).
WRAP_JS = """
function miyaWrapCores(cx,cy){
 document.querySelectorAll('.t').forEach(function(t){
  var cores=t.querySelectorAll('.mv-glint-core,[class*="mv-core-"]'); if(!cores.length) return;
  var pd=t.style.display, pv=t.style.visibility; t.style.display='block'; t.style.visibility='hidden';
  cores.forEach(function(core){
   var svg=core.ownerSVGElement; if(!svg||core.parentNode!==svg) return;
   var kids=Array.prototype.slice.call(svg.children).filter(function(e){return e.tagName!=='defs';});
   var sr=svg.getBoundingClientRect(), k=svg.viewBox.baseVal.width/sr.width;
   function ok(e){var r=e.getBoundingClientRect(),w=r.width*k,h=r.height*k,x=(r.left-sr.left)*k+w/2,y=(r.top-sr.top)*k+h/2;
    return w>0&&w<=460&&h<=460&&Math.hypot(x-cx,y-cy)<=170;}
   var i=kids.indexOf(core),a=i,b=i, solo=/mv-core-turn/.test(core.getAttribute('class')||'');   // 'turn' = only the moving part itself, no neighbours (2026-10-19)
   while(!solo&&a>0&&ok(kids[a-1]))a--;
   while(!solo&&b<kids.length-1&&ok(kids[b+1]))b++;
   var g=document.createElementNS('http://www.w3.org/2000/svg','g');
   g.setAttribute('class',core.getAttribute('class')); core.setAttribute('class','');
   svg.insertBefore(g,kids[a]); for(var j=a;j<=b;j++)g.appendChild(kids[j]);
   // ring for ping/stamp: drawn on top of the object, hidden until a motion shows it (dark rim + warm line, visible on paper and night)
   var bb=g.getBBox(), r=Math.min(Math.max(bb.width,bb.height)/2,200)+12, NS='http://www.w3.org/2000/svg';
   var rg=document.createElementNS(NS,'g'); rg.setAttribute('class','mv-ring'); rg.setAttribute('opacity','0');
   [['rgba(0,0,0,.28)',12],['#ffcf5a',6]].forEach(function(c){var ci=document.createElementNS(NS,'circle');
    ci.setAttribute('cx',bb.x+bb.width/2);ci.setAttribute('cy',bb.y+bb.height/2);ci.setAttribute('r',r);
    ci.setAttribute('fill','none');ci.setAttribute('stroke',c[0]);ci.setAttribute('stroke-width',c[1]);rg.appendChild(ci);});
   svg.insertBefore(rg,g.nextSibling);
   // stroke lengths and opacities for 'draw' (measured now, while the picture is laid out)
   g.querySelectorAll('path,line,polyline,polygon,circle,ellipse,rect').forEach(function(e){var cs=getComputedStyle(e);
    e.__op=+cs.opacity; if(cs.stroke!=='none'&&parseFloat(cs.strokeWidth)>0&&e.getTotalLength){try{e.__len=e.getTotalLength();}catch(x){}}});
  });
  t.style.display=pd; t.style.visibility=pv;
 });
}
function miyaStroked(g){return Array.prototype.filter.call(g.querySelectorAll('*'),function(e){return e.__len>0;});}
function miyaFilled(g){return Array.prototype.filter.call(g.querySelectorAll('path,line,polyline,polygon,circle,ellipse,rect'),function(e){return !(e.__len>0);});}
"""

# Chalkboard fit (guideline 7, 2026-10-13): long card values such as "sail-backed giant" wrapped to two lines and spilled
# out of the 140 px card. At page load every value is kept on one line and shrunk until it fits its 560 px column, the
# small left/right notes shrink until they fit the card height, and the title stays clear of the logo. Runs again when
# the fonts have loaded (the first pass may measure with the fallback font).
CHALK_FIT_JS = """
function miyaFitChalk(){
 document.querySelectorAll('.chalk').forEach(function(c){
  var t=c.closest('.t'),pt=t?t.style.display:'',pv=t?t.style.visibility:'',pc=c.style.display;
  if(t){t.style.display='block';t.style.visibility='hidden';} c.style.display='block';
  c.querySelectorAll('.row .v').forEach(function(v){v.style.fontSize='';v.style.whiteSpace='nowrap';
   var fs=parseFloat(getComputedStyle(v).fontSize);while(v.scrollWidth>v.clientWidth+1&&fs>28){fs-=2;v.style.fontSize=fs+'px';}});
  c.querySelectorAll('.row .l,.row .n').forEach(function(e){e.style.fontSize='';e.style.lineHeight='';
   var fs=parseFloat(getComputedStyle(e).fontSize);while(e.scrollHeight>118&&fs>14){fs-=1;e.style.fontSize=fs+'px';e.style.lineHeight='1.12';}});
  var ct=c.querySelector('.ct');if(ct){ct.style.fontSize='';ct.style.whiteSpace='nowrap';
   var fs=parseFloat(getComputedStyle(ct).fontSize);while(ct.getBoundingClientRect().right>1640&&fs>36){fs-=2;ct.style.fontSize=fs+'px';}}
  var cc=c.querySelector('.cc');if(cc){cc.style.fontSize='';cc.style.whiteSpace='nowrap';
   var rg=document.createRange();rg.selectNodeContents(cc);   // the box is 1920 px wide, so measure the text itself
   var fs=parseFloat(getComputedStyle(cc).fontSize);while(rg.getBoundingClientRect().width>1700&&fs>22){fs-=2;cc.style.fontSize=fs+'px';}}
  c.style.display=pc; if(t){t.style.display=pt;t.style.visibility=pv;}
 });
}
miyaFitChalk(); if(document.fonts&&document.fonts.ready)document.fonts.ready.then(miyaFitChalk);
"""


# ---------------------------------------------------------------------------------------------------------------
# 2026-10-22 (user decision, from the 20 s motion test): the round centre object is no longer required, and the
# pictures may use object motions anywhere on the canvas plus five more transitions. See guideline 3-2, 4-1, 4-3.
# ---------------------------------------------------------------------------------------------------------------

# New transitions (build3 pool). Each one is driven by a seekable proxy tween: miyaTr() recomputes the clip-path from k (0..1).
#   seam    a yellow line draws from the bottom left to the top right, then the seam opens into a widening diagonal band
#   diamond a diamond opens from an off-centre point (it ends fully covering every corner, so nothing pops at the end)
#   page    the old picture folds away to the left like a page, the new one is revealed behind it
#   zigzag  a torn zigzag edge sweeps left to right
#   wave    a wavy yellow edge rises from the bottom
NEW_TR = ['seam', 'diamond', 'page', 'zigzag', 'wave']
TR_DUR = {'seam': 1.0, 'diamond': 0.9, 'page': 0.8, 'zigzag': 0.9, 'wave': 1.0}


def tr_js(tr, T, v0, W, H):
    """JS statements that bring picture `T` (css selector) in with one of NEW_TR, starting at v0."""
    d = TR_DUR[tr]
    if tr == 'page':   # the old picture's exit (scaleX -> 0 about its left edge, same ease) is added by build3
        return [f'tl.fromTo("{T}",{{clipPath:"inset(0px 0px 0px 100%)"}},{{clipPath:"inset(0px 0px 0px 0%)",duration:{d},ease:"power2.inOut",immediateRender:false}},{v0:.3f});',
                f'tl.set("{T}",{{clipPath:"none"}},{v0 + d + .01:.3f});',
                f'tl.set("#tredge",{{display:"block"}},{v0:.3f});tl.set("#tredge",{{display:"none"}},{v0 + d:.3f});',
                f'tl.fromTo("#treline",{{attr:{{x1:{W},y1:0,x2:{W},y2:{H}}}}},{{attr:{{x1:0,y1:0,x2:0,y2:{H}}},duration:{d},ease:"power2.inOut",immediateRender:false}},{v0:.3f});']
    return [f'miyaTrAnim(tl,"{T}","{tr}",{v0:.3f},{d},{W},{H});']


# Object motions anywhere in a picture (art groups `id="mv-<kind>-<name>"` with data-* attributes, see art_spec.md 7):
#   path     data-path="M.. C.."  follows the path (paper plane, rocket), turning with it unless data-rot="0"; data-dur, data-delay
#   flip     turns data-deg (180) about data-pivot (hourglass), data-delay, data-dur
#   fill     scales from data-from (0) to data-to (1) along data-axis (y) about data-pivot (sand, bars, gauges); data-delay, data-dur
#   grow     = fill, from 0
#   swing    damped pendulum about data-pivot, data-amp degrees, data-per seconds
#   topple   falls data-deg (72) about data-pivot (domino), data-delay, data-dur
#   liquid   rises data-rise px and scrolls data-scroll px sideways (a wide wavy-topped shape clipped by the vessel)
#   bubble   rises data-rise px while fading, repeats every data-per seconds
#   edge     the group's strokes draw themselves on (network lines), data-delay, data-dur
#   keyturn  a side-view key bow turning about its shaft: scaleY 1 -> data-to (.32) about data-pivot
#   shackle  lifts data-lift px and swings data-deg about data-pivot (padlock opening)
#   popin    pops in with an overshoot about its own centre (network nodes)
#   shake    quick left-right shake, data-amp px (3), data-dur s (.25): a lock clicking, an impact
#   dash     the dashes of a dashed line march along it (a travelled route), data-speed px/s (40)
#   scroll   drifts sideways data-dist px (160) over the whole picture (parallax stars, clouds)
#   slam     slams in from 2.4x size with a slight turn (a stamp or title)
#   rise     slides up data-from px (60) while fading in (a tag, a label)
OBJ_KINDS = ['path', 'flip', 'fill', 'grow', 'swing', 'topple', 'liquid', 'bubble', 'edge', 'keyturn', 'shackle', 'popin',
             'shake', 'dash', 'scroll', 'slam', 'rise']


def path_timing(at, t0, sp):
    """Start and duration of a path motion (shared by the object and the tracking camera)."""
    st = t0 + float(at.get('data-delay', 0.3))
    du = float(at['data-dur']) if 'data-dur' in at else min(sp - .6, 3.4)
    return st, du


def track_spec(raw, sidecar):
    """Camera tracking for a picture with a long travelling motion (2026-10-22): returns (d, delay, dur or None, scale) or None.
    Sources: a `mv-path-*` object (the camera follows it), an empty group `mv-track-*` with data-path (a route only the camera follows),
    or three or more `mv-topple-*` dominoes (the camera pans along their pivots). Sidecar `"track": false` turns it off, `{"scale": 1.4}` sets the zoom."""
    import re
    tk = sidecar.get('track') if sidecar else None
    if tk is False: return None
    sc = float(tk.get('scale', 1.3)) if isinstance(tk, dict) else 1.3
    tags = [dict(re.findall(r'(data-[a-z]+)="([^"]*)"', m.group(0)), _id=m.group(1))
            for m in re.finditer(r'<g\b[^>]*\bid="(mv-(?:path|track|topple)-[^"]*)"[^>]*>', raw)]
    for a in tags:
        if a['_id'].startswith(('mv-path-', 'mv-track-')) and a.get('data-track') != '0' and a.get('data-path'):
            return a['data-path'].replace('"', ''), float(a.get('data-delay', 0.3)), (float(a['data-dur']) if 'data-dur' in a else None), float(a.get('data-scale', sc)), 'power2.inOut'
    tp = [a for a in tags if a['_id'].startswith('mv-topple-') and len(a.get('data-pivot', '').replace(',', ' ').split()) == 2]
    if len(tp) >= 3:
        tp.sort(key=lambda a: float(a.get('data-delay', 0.3)))
        pts = [a['data-pivot'].replace(',', ' ').split() for a in tp]
        d = 'M' + ' L'.join(f'{x} {y}' for x, y in pts)
        d0 = float(tp[0].get('data-delay', 0.3)); d1 = float(tp[-1].get('data-delay', 0.3)) + float(tp[-1].get('data-dur', .55))
        return d, d0, d1 - d0, sc, 'sine.inOut'
    return None


def track_js(spec, wsel, t0, sp, W, H):
    d, delay, dur, scale, ease = spec
    st = t0 + delay; du = dur if dur is not None else min(sp - .6, 3.4)
    return f'miyaTrack(tl,"{wsel}","{d}",{st:.3f},{du:.3f},{scale},{W},{H},"{ease}");'


def obj_js(kind, g, at, t0, v0, sp):
    """GSAP lines for one object motion. at: the group's data-* attributes, g: JS expression for the element,
    t0: picture start, v0: transition-in start, sp: seconds the picture stays (plus margin)."""
    f = lambda k, d: float(at.get('data-' + k, d))
    pv = at.get('data-pivot', '').replace(',', ' ').split()
    org = (lambda dflt: f'svgOrigin:"{pv[0]} {pv[1]}"') if len(pv) == 2 else (lambda dflt: f'transformOrigin:"{dflt}"')
    st = t0 + f('delay', 0.3); du = f('dur', 1.0)
    if kind == 'path':
        d = at.get('data-path', '').replace('"', '')
        pst, pdu = path_timing(at, t0, sp)
        return [f'miyaPath(tl,{g},"{d}",{pst:.3f},{pdu:.3f},{0 if at.get("data-rot") == "0" else 1},{f("rot0", 0)});']
    if kind == 'flip':
        return [f'tl.set({g},{{rotation:0,{org("50% 50%")}}},{v0:.3f});',
                f'tl.to({g},{{rotation:{f("deg", 180)},duration:{du},ease:"power2.inOut",immediateRender:false}},{st:.3f});']
    if kind in ('fill', 'grow'):
        pr = 'scaleX' if at.get('data-axis') == 'x' else 'scaleY'
        a, b = f('from', 0), f('to', 1)
        return [f'tl.set({g},{{{pr}:{a},{org("50% 100%" if pr == "scaleY" else "0% 50%")}}},{v0:.3f});',
                f'tl.to({g},{{{pr}:{b},duration:{du},ease:"power1.inOut",immediateRender:false}},{st:.3f});']
    if kind == 'swing':
        amp, per = f('amp', 28), f('per', 2.4)
        n = max(int(math.ceil(sp / (per / 2))), 2)
        kf = ','.join(f'{{rotation:{amp * (-1) ** i * .78 ** i:.2f},duration:{per / 2:.3f},ease:"sine.inOut"}}' for i in range(n))
        return [f'tl.set({g},{{rotation:0,{org("50% 0%")}}},{v0:.3f});',
                f'tl.to({g},{{keyframes:[{kf}],immediateRender:false}},{v0:.3f});']
    if kind == 'topple':
        return [f'tl.set({g},{{rotation:0,{org("100% 100%")}}},{v0:.3f});',
                f'tl.to({g},{{rotation:{f("deg", 72)},duration:{f("dur", .55)},ease:"power2.inOut",immediateRender:false}},{st:.3f});']
    if kind == 'liquid':
        out = [f'tl.fromTo({g},{{y:0}},{{y:{-f("rise", 300):.0f},duration:{du if "data-dur" in at else 2.4},ease:"power1.inOut",immediateRender:false}},{st:.3f});']
        if f('scroll', 0):
            out.append(f'tl.fromTo({g},{{x:0}},{{x:{-f("scroll", 0):.0f},duration:1.6,ease:"none",repeat:{max(int(math.ceil(sp / 1.6)) - 1, 0)},immediateRender:false}},{v0:.3f});')
        return out
    if kind == 'bubble':
        per = f('per', 1.6); rise = f('rise', 200)
        return [f'tl.set({g},{{opacity:0}},{v0:.3f});',
                f'tl.fromTo({g},{{y:0,opacity:.8}},{{y:{-rise:.0f},opacity:0,duration:{per},ease:"none",repeat:{max(int(math.ceil(sp / per)) - 1, 0)},immediateRender:false}},{st:.3f});']
    if kind == 'edge':
        return [f'miyaDraw(tl,{g},{v0:.3f},{st:.3f},{du});']
    if kind == 'keyturn':
        return [f'tl.set({g},{{scaleY:1,{org("50% 50%")}}},{v0:.3f});',
                f'tl.to({g},{{scaleY:{f("to", .32)},duration:{f("dur", .8)},ease:"power2.inOut",immediateRender:false}},{st:.3f});']
    if kind == 'shackle':
        return [f'tl.set({g},{{y:0,rotation:0,{org("50% 100%")}}},{v0:.3f});',
                f'tl.to({g},{{y:{-f("lift", 46):.0f},rotation:{f("deg", -16)},duration:{f("dur", .6)},ease:"power2.inOut",immediateRender:false}},{st:.3f});']
    if kind == 'popin':
        return [f'tl.set({g},{{scale:0,opacity:0,{org("50% 50%")}}},{v0:.3f});',
                f'tl.to({g},{{scale:1,opacity:1,duration:.45,ease:"back.out(2)",immediateRender:false}},{st:.3f});']
    if kind == 'shake':
        amp = f('amp', 3); dd = f('dur', .25); per = .03
        return [f'tl.fromTo({g},{{x:{-amp}}},{{x:{amp},duration:{per},ease:"none",yoyo:true,repeat:{max(int(dd / per) - 1, 1)},immediateRender:false}},{st:.3f});',
                f'tl.set({g},{{x:0}},{st + dd + per:.3f});']
    if kind == 'dash':
        sel = f'Array.prototype.slice.call({g}.querySelectorAll("path,line,polyline,polygon,circle,ellipse,rect"))'
        return [f'tl.fromTo({sel},{{strokeDashoffset:0}},{{strokeDashoffset:{-f("speed", 40) * sp:.0f},duration:{sp:.3f},ease:"none",immediateRender:false}},{v0:.3f});']
    if kind == 'scroll':
        return [f'tl.fromTo({g},{{x:0}},{{x:{-f("dist", 160):.0f},duration:{sp:.3f},ease:"none",immediateRender:false}},{v0:.3f});']
    if kind == 'slam':
        return [f'tl.set({g},{{scale:2.4,opacity:0,rotation:{f("rot", -4)},{org("50% 50%")}}},{v0:.3f});',
                f'tl.to({g},{{scale:1,opacity:1,rotation:0,duration:.28,ease:"power4.in",immediateRender:false}},{st:.3f});']
    if kind == 'rise':
        return [f'tl.set({g},{{y:{f("from", 60):.0f},opacity:0}},{v0:.3f});',
                f'tl.to({g},{{y:0,opacity:1,duration:{f("dur", .5)},ease:"power2.out",immediateRender:false}},{st:.3f});']
    raise ValueError(kind)


MOTION_JS = """
function miyaEase(x){return x<.5?4*x*x*x:1-Math.pow(-2*x+2,3)/2;}
// travelling motion (path object, tracking camera): constant speed with short 15 % soft start/stop (no mid-way speed-up, owner 2026-10-22)
function miyaCruise(x){var r=.15,v=1/(1-r);return x<r?v*x*x/(2*r):x>1-r?1-v*(1-x)*(1-x)/(2*r):v*(r/2+x-r);}
function miyaClamp(x){return Math.min(1,Math.max(0,x));}
// new transitions: clip-path of picture `el` from k (0..1); the overlay #trfx carries the light edges
function miyaTr(el,tr,k,W,H){
 var e=miyaEase(k),c='none',l1=document.getElementById('trl1'),l2=document.getElementById('trl2'),pz=document.getElementById('trpz'),pd=document.getElementById('trpd');
 [l1,l2,pz,pd].forEach(function(n){n.setAttribute('opacity',0);});
 function line(n,x1,y1,x2,y2){n.setAttribute('x1',x1);n.setAttribute('y1',y1);n.setAttribute('x2',x2);n.setAttribute('y2',y2);n.setAttribute('opacity',1);}
 if(k>=1){el.style.clipPath='none';return;}
 if(tr==='seam'){
  var len=Math.hypot(W,H),ux=W/len,uy=-H/len,nx=-uy,ny=ux,cx=W/2,cy=H/2,L=len*1.5,wmax=W*H/len+40;
  var dr=miyaClamp(k/.35),op=miyaEase(miyaClamp((k-.35)/.65)),w=op*wmax;
  function P(s,o){return (cx+ux*s+nx*o).toFixed(1)+'px '+(cy+uy*s+ny*o).toFixed(1)+'px';}
  if(op===0){c='polygon(0px 0px,0px 0px,0px 0px,0px 0px)';var q=1-Math.pow(1-dr,3);line(l1,0,H,W*q,H-H*q);}
  else{c='polygon('+[P(-L,-w),P(L,-w),P(L,w),P(-L,w)].join(',')+')';
   [[l1,-w],[l2,w]].forEach(function(a){line(a[0],cx-ux*L+nx*a[1],cy-uy*L+ny*a[1],cx+ux*L+nx*a[1],cy+uy*L+ny*a[1]);});}
 }else if(tr==='diamond'){
  var px=W*.73,py=H*.28,rmax=Math.max(px,W-px)+Math.max(py,H-py)+30,r=e*rmax;
  c='polygon('+[px+'px '+(py-r)+'px',(px+r)+'px '+py+'px',px+'px '+(py+r)+'px',(px-r)+'px '+py+'px'].join(',')+')';
  pd.setAttribute('points',[px+','+(py-r),(px+r)+','+py,px+','+(py+r),(px-r)+','+py].join(' '));pd.setAttribute('opacity',1-miyaEase(miyaClamp((k-.6)/.4)));
 }else if(tr==='zigzag'){
  var a=90*W/1920,xe=-a-30+e*(W+a+60),n=12,pts=['0px 0px',xe+'px 0px'],dd='M'+xe+' 0';
  for(var i=1;i<=n;i++){var x=xe+(i%2?-a:0),y=i*H/n;pts.push(x+'px '+y+'px');dd+='L'+x+' '+y;}
  pts.push('0px '+H+'px');c='polygon('+pts.join(',')+')';pz.setAttribute('d',dd);pz.setAttribute('stroke','#fff');pz.setAttribute('opacity',1-miyaClamp((k-.85)/.15));
 }else if(tr==='wave'){
  var ye=(H+170)+e*(-H-340),ph=k*9,s=W/48,pts2=['0px '+H+'px'],dd2='';
  for(var x2=0;x2<=W+1;x2+=s){var y2=ye+Math.sin(x2*.012+ph)*45;pts2.push(x2.toFixed(0)+'px '+y2.toFixed(1)+'px');dd2+=(dd2?'L':'M')+x2.toFixed(0)+' '+y2.toFixed(1);}
  pts2.push(W+'px '+H+'px');c='polygon('+pts2.join(',')+')';pz.setAttribute('d',dd2);pz.setAttribute('stroke','#ffd54a');pz.setAttribute('opacity',1-miyaClamp((k-.85)/.15));
 }
 el.style.clipPath=c;
}
function miyaTrAnim(tl,sel,tr,t0,dur,W,H){
 var el=document.querySelector(sel),o={k:0};
 tl.set('#trfx',{display:'block'},t0);
 tl.to(o,{k:1,duration:dur,ease:'none',immediateRender:false,modifiers:{k:function(v){miyaTr(el,tr,v,W,H);return v;}}},t0);   // modifiers, not onUpdate: seeking suppresses callbacks
 tl.set('#trfx',{display:'none'},t0+dur+.01); tl.set(sel,{clipPath:'none'},t0+dur+.01);
}
// object follows an SVG path, turning with it (paper plane, rocket)
function miyaPath(tl,g,d,t0,dur,rot,rot0){
 var t=g.closest('.t'),pd=t.style.display,pv=t.style.visibility;t.style.display='block';t.style.visibility='hidden';
 var NS='http://www.w3.org/2000/svg',svg=g.ownerSVGElement,p=document.createElementNS(NS,'path');p.setAttribute('d',d);p.setAttribute('visibility','hidden');svg.appendChild(p);
 var L=p.getTotalLength(),P0=p.getPointAtLength(0),o={k:0};
 function ang(k){var s0=Math.max(0,Math.min(L-2,L*k)),a=p.getPointAtLength(s0),b=p.getPointAtLength(Math.min(L,s0+2));return Math.atan2(b.y-a.y,b.x-a.x)*180/Math.PI;}
 var a0=ang(0);t.style.display=pd;t.style.visibility=pv;
 function ap(k){var q=p.getPointAtLength(L*k);gsap.set(g,{x:q.x-P0.x,y:q.y-P0.y,rotation:rot?ang(k)-a0+(rot0||0):0,svgOrigin:P0.x+' '+P0.y});}
 tl.to(o,{k:1,duration:dur,ease:miyaCruise,immediateRender:false,modifiers:{k:function(v){ap(v);return v;}}},t0);
}
// camera tracking: the camera centre follows an SVG path (same window and ease as the object), zooming in at the start and out at the end
function miyaTrack(tl,wsel,d,t0,dur,sc,W,H,ease){
 var w=document.querySelector(wsel),t=w.closest('.t'),pd=t.style.display,pv=t.style.visibility;t.style.display='block';t.style.visibility='hidden';
 var NS='http://www.w3.org/2000/svg',svg=w.querySelector('svg'),p=document.createElementNS(NS,'path');p.setAttribute('d',d);p.setAttribute('visibility','hidden');svg.appendChild(p);
 var L=p.getTotalLength(),o={k:0};t.style.display=pd;t.style.visibility=pv;
 function ap(k){var q=p.getPointAtLength(L*k),r=Math.min(1,k/.12,(1-k)/.12),s=1+(sc-1)*r*r*(3-2*r);
  var cx=Math.min(Math.max(q.x,W/2/s),W-W/2/s),cy=Math.min(Math.max(q.y,H/2/s),H-H/2/s);
  gsap.set(w,{scale:s,x:W/2-cx*s,y:H/2-cy*s,transformOrigin:'0px 0px'});}
 tl.to(o,{k:1,duration:dur,ease:ease==='power2.inOut'?miyaCruise:ease,immediateRender:false,modifiers:{k:function(v){ap(v);return v;}}},t0);
}
// strokes draw themselves on (network edges)
function miyaDraw(tl,g,v0,st,dur){
 var t=g.closest('.t'),pd=t.style.display,pv=t.style.visibility;t.style.display='block';t.style.visibility='hidden';
 var els=Array.prototype.filter.call(g.querySelectorAll('path,line,polyline,polygon,circle,ellipse,rect'),function(e){try{e.__len=e.getTotalLength();return e.__len>0;}catch(x){return false;}});
 t.style.display=pd;t.style.visibility=pv;
 tl.set(els,{strokeDasharray:function(i,e){return e.__len;},strokeDashoffset:function(i,e){return e.__len;}},v0);
 tl.to(els,{strokeDashoffset:0,duration:dur,ease:'power1.inOut',stagger:.05,immediateRender:false},st);
}
"""
