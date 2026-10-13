# Centre-object motions (guideline 4-1). The picture's round centre object lives in a group
# `mv-core-<type>`; each type below moves it differently, so the object is not always the same
# up-and-down squash. Every tween is finite (repeat count, never -1) so the timeline stays seekable,
# and nothing uses an SVG filter.
import math

# 13 types. Order matters: build3 walks it with a step that never repeats a type in consecutive pictures.
CORE_TYPES = ['spin', 'sway', 'orbit', 'glide', 'heartbeat', 'flicker', 'swell',
              'tremble', 'approach', 'reveal', 'squeeze', 'wobble', 'roll']

CORE_STEP = 5   # coprime with 13: visits all 13 types before repeating, neighbours always differ


def legacy_core_type(ordinal):
    """Type for a picture whose centre group is still the old `mv-glint-core` (no explicit type)."""
    return CORE_TYPES[(ordinal * CORE_STEP + 3) % len(CORE_TYPES)]


def core_js(ctype, g, t0, v0, sp):
    """GSAP lines for one centre object.
    g: JS expression for the element, t0: picture start (s), v0: transition-in start (s),
    sp: seconds the picture stays on screen (plus margin). Returns a list of JS statements."""
    C = 'transformOrigin:"50% 50%"'
    yo = lambda per: f'ease:"sine.inOut",yoyo:true,repeat:{max(int(math.ceil(sp / per)) - 1, 0)},immediateRender:false'
    if ctype == 'spin':        # slow one-way turn (lens, clock, planet, gear)
        return [f'tl.fromTo({g},{{rotation:0,{C}}},{{rotation:{36 * sp:.1f},duration:{sp:.3f},ease:"none",immediateRender:false}},{v0:.3f});']
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
   var i=kids.indexOf(core),a=i,b=i;
   while(a>0&&ok(kids[a-1]))a--;
   while(b<kids.length-1&&ok(kids[b+1]))b++;
   var g=document.createElementNS('http://www.w3.org/2000/svg','g');
   g.setAttribute('class',core.getAttribute('class')); core.setAttribute('class','');
   svg.insertBefore(g,kids[a]); for(var j=a;j<=b;j++)g.appendChild(kids[j]);
  });
  t.style.display=pd; t.style.visibility=pv;
 });
}
"""
