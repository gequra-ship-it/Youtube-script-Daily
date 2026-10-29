# Centre-object motions (guideline 4-1). The picture's round centre object lives in a group
# `mv-core-<type>`; each type below moves it differently, so the object is not always the same
# up-and-down squash. Every tween is finite (repeat count, never -1) so the timeline stays seekable,
# and nothing uses an SVG filter.
import fxlib   # open-source library glue (2026-10-29)
import math, json

# 19 types (13 + 6 taken from a motion-graphics reference on 2026-10-13: pop, ping, stamp, flip, draw, drop).
# Order matters: build3 walks it with a step that never repeats a type in consecutive pictures.
CORE_TYPES = ['spin', 'pop', 'sway', 'orbit', 'ping', 'glide', 'heartbeat', 'draw', 'flicker', 'swell',
              'stamp', 'tremble', 'approach', 'flip', 'reveal', 'squeeze', 'drop', 'wobble', 'roll']

CORE_STEP = 7   # coprime with 19: visits all 19 types before repeating, neighbours always differ


def legacy_core_type(ordinal):
    """Type for a picture whose centre group is still the old `mv-glint-core` (no explicit type)."""
    return CORE_TYPES[(ordinal * CORE_STEP + 3) % len(CORE_TYPES)]


# ---- pivot / kind sanity by object name (round 4, 2026-10-26; miya: a tree swayed from its top, the trunk waving instead of the crown) ----
# Deterministic: only the group's name decides. An agent can keep an unusual choice on purpose with data-keep="1" on the group.
import re as _re
BOTTOM_NAMES = _re.compile(r'tree|trunk|palm|plant|flower|grass|reed|kelp|seaweed|weed|pole|post|mast|tower|candle|torch|cactus|mushroom|stalk|stem|column|pillar|statue|totem|hut|house|island|person|\bman\b|woman|figure|astro|runner|walker|kid|child|sign(?!al)|flag|lamppost|chimney|building|mountain|hill|bush|shrub|tent|tomb|grave|scarecrow|ladder|fence', _re.I)
HANG_NAMES = _re.compile(r'lantern|bell|pendul|chandelier|rope|chain|vine|icicle|hook|banner|curtain|tag\b|cocoon|spider|\bbat\b|watch|cradle|medal|necklace|hanging|ornament|drip|droplet|bulb|noose|hammock', _re.I)
CENTER_NAMES = _re.compile(r'scale|balance|beam|seesaw|see-saw|lever|needle|compass|planet|ship|boat|raft|canoe|probe|voyager|plane|rocket|wheel|ball|coin|disc|disk|gear|cog|globe|earth|world|moon|sun|galaxy|star|orb|bubble|sphere|clock|dial|satellite|ufo|drone|balloon', _re.I)
ROUND_NAMES = _re.compile(r'hole|vortex|whirlpool|swirl|wheel|ball|coin|disc|disk|gear|cog|globe|earth|world|planet|moon|galaxy|orb|sphere|stone|rock(?!et)|hourglass|needle|card|page|medal|lens|record|weave|spiral|ring|tire|tyre|\bw\b|\bmw\b|prion|helix|dna|vinyl|token|chip|seal|plate|atom|molecule|cell|nucleus', _re.I)
HEAVY_NAMES = _re.compile(r'whale|fish|shark|animal|carcass|body|ship|mountain|building|tree|house|person|elephant|dinosaur|mammoth|bear|skeleton|bone', _re.I)


def _tail(name):
    """the descriptive part of a group name: mv-core-<type>-<tail> / mv-<kind>-<tail>, without a trailing unit suffix (-u072 / -U072 / -2)"""
    parts = name.split('-'); tail = '-'.join(parts[3:] if len(parts) > 2 and parts[1] == 'core' else parts[2:])
    return _re.sub(r'-?(?:[uU]\d{3,}|\d+)$', '', tail)


def pivot_of(name):
    """'bottom' for things that stand on the ground, 'top' for things that hang, 'center' for free / round / balanced things, None = no opinion."""
    tail = _tail(name)
    if HANG_NAMES.search(tail): return 'top'
    if BOTTOM_NAMES.search(tail): return 'bottom'
    if CENTER_NAMES.search(tail): return 'center'
    return None


def core_sanitize(ctype, name, keep=False):
    """Replace a centre motion that cannot fit the named object: spin/roll/flip only for round or card-like things, drop not for heavy bodies or creatures,
    wobble/tremble/orbit not for things standing on the ground (they sway from the base instead)."""
    if keep: return ctype
    tail = _tail(name)
    if not tail or _re.fullmatch(r'[a-z]?\d*|[uU]\d+', tail): return ctype   # no descriptive name -> trust the agent
    pv = pivot_of(name)
    if ctype in ('spin', 'roll', 'flip', 'turn') and not ROUND_NAMES.search(tail): ctype = {'spin': 'wobble', 'roll': 'glide', 'flip': 'wobble', 'turn': 'wobble'}[ctype]
    if ctype == 'drop' and HEAVY_NAMES.search(tail): ctype = 'swell'
    if pv == 'bottom' and ctype in ('wobble', 'tremble', 'orbit', 'roll', 'spin', 'flip', 'glide'): ctype = 'sway'
    return ctype


OBJ_TURNING = ('spin', 'rollby', 'flip', 'circle', 'coast')


def obj_sanitize(kind, name, keep=False):
    """axis sanity for object motions (round 4, miya: '오브젝트 모션 추가할 때 축 점검'): a thing that stands on the ground (tree, person, tower)
    or a heavy body (whale, ship) never spins, rolls, flips or orbits -> it sways from its base; a hanging thing (lantern, bell) that was asked
    to spin/flip swings as a pendulum instead. data-keep="1" keeps the author's choice. Non-descriptive names are left alone."""
    if keep: return kind
    t = _tail(name)
    if not t or kind not in OBJ_TURNING: return kind
    if HANG_NAMES.search(t) and kind in ('spin', 'flip'): return 'pendulum'
    if BOTTOM_NAMES.search(t) and not ROUND_NAMES.search(t): return 'sway'
    if HEAVY_NAMES.search(t) and not ROUND_NAMES.search(t): return 'sway'
    return kind


def core_js(ctype, g, t0, v0, sp, ring=None, pivot=None, pv=None):
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
    if ctype == 'sway':        # pendulum around the top (lamp, bell, key, hanging things); round 4: things that stand on the ground sway from the base (pivot='bottom': tree, pole, sign post, figure)
        if pv and len(pv) == 2:   # 2026-10-29: an explicit data-pivot (tools/setbase.py writes the foot of the stem/trunk/post) beats the bbox percent, which sat beside a leaning trunk or inside a wide group
            return [f'tl.fromTo({g},{{rotation:-5,svgOrigin:miyaPv({g},{pv[0]},{pv[1]}),smoothOrigin:false}},{{rotation:5,duration:2.2,{yo(2.2)}}},{v0:.3f});']
        if pivot == 'bottom': return [f'tl.fromTo({g},{{rotation:-5,transformOrigin:"50% 100%"}},{{rotation:5,duration:2.2,{yo(2.2)}}},{v0:.3f});']
        if pivot == 'center': return [f'tl.fromTo({g},{{rotation:-6,{C}}},{{rotation:6,duration:2.0,{yo(2.0)}}},{v0:.3f});']
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
        return [f'tl.fromTo({g},{{x:0,rotation:0,{C}}},{{x:5,rotation:1.5,duration:{sp:.3f},ease:"wiggle({{wiggles:{max(int(sp / .14), 4)},type:{chr(39)}random{chr(39)}}})",immediateRender:false}},{v0:.3f});']   # 2026-10-29: CustomWiggle random (nervous jitter)
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
                f'tl.to({g},{{y:0,rotation:0,opacity:1,duration:.9,ease:"miyaBnc",immediateRender:false}},{t0 + .15:.3f});',   # 2026-10-29: CustomBounce + squash
                f'tl.fromTo({g},{{scaleX:1,scaleY:1,transformOrigin:"50% 100%"}},{{scaleX:1.2,scaleY:.8,duration:.9,ease:"miyaBnc-squash",immediateRender:false}},{t0 + .15:.3f});']
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
# Added 2026-10-24 (composition blocks from the lemo-opuscar study, test film motion-demo/bears-60s-v2, guideline 4-1B):
#   slide    moves data-dx/data-dy px (default -960/0) from there to its place (a half-screen panel, a layer, a tab); data-dir="out" moves it
#            from its place to the offset instead (eraser leaving, page off); data-dur .7, data-delay
#   fade     opacity data-from (0) -> data-to (1) over data-dur (.4) at data-delay: a ghost lighting up (.1 -> .6), an eraser pass (from 1 to 0, dur .12)
#   ticks    the group's children appear one by one, data-step s apart (.1), from data-delay; data-fill="#hex" recolours them instead of
#            showing them (a row of squares filling: 1 square = 1 unit), data-n limits how many
#   rack     rack focus: the group is soft (data-r px, 14) and sharpens to 0 (data-dir="in", default), or the reverse ("out"); data-delay, data-dur (1.2).
#            Made from 6 offset ghost copies, no SVG filter. Put the near object in one rack group and the far one in another with the opposite dir.
# `popin` takes data-axis="y" or "x": it grows along that axis only (a pull-tab slat flipping up).
# 2026-10-29 library kinds (miya: wire the open-source plugins in, guideline 4-6):
#   draw     the group's strokes draw themselves on with DrawSVGPlugin (stagger .08), fills fade in after; data-delay, data-dur (1.4). Like a pen sketching the object.
#   morph    the group's FIRST path turns into the d of its LAST path (draw that target with opacity="0"); MorphSVGPlugin, shapeIndex auto; data-back="1" morphs back; data-delay, data-dur (1.0)
#   toss     thrown: Physics2DPlugin arc with data-v px/s (520), data-angle degrees (-60 = up-right, -120 = up-left), data-g (1400), data-friction (.02), turning data-deg (240); data-delay, data-dur (1.6)
#   skid     slides and stops: InertiaPlugin, data-v px/s (900) sideways, snaps to data-dist px (420), data-res resistance (800); data-delay
#   coast    a wheel / top / coin that spins down: PhysicsPropsPlugin rotation velocity data-v deg/s (720), data-friction (.12), about the CENTRE or data-pivot; data-delay, data-dur (3)
#   regroup  the group's direct children re-arrange from where they were drawn into data-shape ring | line | grid (Flip plugin, stagger .05); data-delay, data-dur (1.2)
OBJ_KINDS = ['path', 'flip', 'fill', 'grow', 'swing', 'topple', 'liquid', 'bubble', 'edge', 'keyturn', 'shackle', 'popin',
             'shake', 'dash', 'scroll', 'slam', 'rise', 'slide', 'fade', 'ticks', 'rack',
             'bob', 'hover', 'pendulum', 'wiggle', 'tilt', 'crumble', 'emph',   # round 4 (2026-10-26): 7 more, guideline 4-1
             'spin', 'rollby', 'float', 'flap', 'swim', 'hop', 'drip', 'unfold', 'unroll', 'flagwave', 'ripple', 'sparkle', 'circle', 'squash',
             'neon', 'shiver', 'beat', 'settle', 'magnet', 'bouncing', 'creep', 'sink', 'ascend', 'tick', 'flicker', 'breathe', 'nodding', 'sway',   # round 4b: 28 more (axis noted per kind)
             'draw', 'morph', 'toss', 'skid', 'coast', 'regroup']   # 2026-10-29 library kinds (guideline 4-6): DrawSVG, MorphSVG, Physics2D, Inertia, PhysicsProps, Flip


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
        # a falling/sinking object must visibly move across the frame: the camera does not follow it (a followed fall looks frozen)
        if a['_id'].startswith('mv-path-') and re.search(r'sink|fall|drop|plunge|descen|carcass', a['_id']): continue
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


def track_js(spec, wsel, t0, sp, W, H, WW=None, WH=None):
    d, delay, dur, scale, ease = spec
    st = t0 + delay; du = dur if dur is not None else min(sp - .6, 3.4)
    return f'miyaTrack(tl,"{wsel}","{d}",{st:.3f},{du:.3f},{scale},{W},{H},"{ease}",{WW or W},{WH or H});'


def obj_js(kind, g, at, t0, v0, sp, name='', spring=None):
    """GSAP lines for one object motion. at: the group's data-* attributes, g: JS expression for the element,
    t0: picture start, v0: transition-in start, sp: seconds the picture stays (plus margin)."""
    f = lambda k, d: float(at.get('data-' + k, d))
    pv = at.get('data-pivot', '').replace(',', ' ').split()
    org = (lambda dflt: f'svgOrigin:miyaPv({g},{pv[0]},{pv[1]}),smoothOrigin:false') if len(pv) == 2 else (lambda dflt: f'transformOrigin:"{dflt}"')
    st = t0 + f('delay', 0.3); du = f('dur', 1.0)
    if kind == 'path':
        d = at.get('data-path', '').replace('"', '')
        pst, pdu = path_timing(at, t0, sp)
        ez = at.get('data-ease', '')   # 2026-10-29: build3 puts a SlowMo ramp here when the sentence says fast / rush / race (fxlib.path_ease)
        return [f'miyaPath(tl,{g},"{d}",{pst:.3f},{pdu:.3f},{0 if at.get("data-rot") == "0" else 1},{f("rot0", 0)}{"," + chr(34) + ez + chr(34) if ez else ""});']
    if kind == 'draw':      # DrawSVGPlugin
        du = f('dur', 1.4)
        SH = f'{g}.querySelectorAll("path,line,polyline,polygon,circle,ellipse,rect")'   # fills hide (fill-opacity, strokes stay) while DrawSVG draws the outlines, then come back
        return [f'tl.set({SH},{{fillOpacity:0}},{v0:.3f});',
                f'tl.fromTo({SH},{{drawSVG:"0%"}},{{drawSVG:"100%",duration:{du},ease:"power1.inOut",stagger:.08,immediateRender:false}},{st:.3f});',
                f'tl.to({SH},{{fillOpacity:(i,e)=>parseFloat(e.getAttribute("fill-opacity")||1),duration:.6,ease:"power1.out",stagger:.03,immediateRender:false}},{st + du * .6:.3f});']
    if kind == 'morph':     # MorphSVGPlugin
        return [f'miyaMorph(tl,{g},{st:.3f},{f("dur", 1.0)},{1 if at.get("data-back") == "1" else 0});']
    if kind == 'toss':      # Physics2DPlugin
        return [f'tl.fromTo({g},{{x:0,y:0,rotation:0,{org("50% 50%")}}},{{duration:{f("dur", 1.6)},physics2D:{{velocity:{f("v", 520)},angle:{f("angle", -60)},gravity:{f("g", 1400)},friction:{f("friction", .02)}}},rotation:{f("deg", 240)},ease:"none",immediateRender:false}},{st:.3f});']
    if kind == 'skid':      # InertiaPlugin (duration comes from velocity + resistance)
        return [f'tl.fromTo({g},{{x:0}},{{inertia:{{x:{{velocity:{f("v", 900)},end:[{f("dist", 420)}]}},resistance:{f("res", 800)}}},immediateRender:false}},{st:.3f});']
    if kind == 'coast':     # PhysicsPropsPlugin
        return [f'tl.fromTo({g},{{rotation:0,{org("50% 50%")}}},{{duration:{f("dur", 3)},physicsProps:{{rotation:{{velocity:{f("v", 720)},friction:{f("friction", .12)}}}}},immediateRender:false}},{st:.3f});']
    if kind == 'regroup':   # Flip
        return [f'miyaRegroup(tl,{g},"{at.get("data-shape", "ring")}",{st:.3f},{f("dur", 1.2)},.05);']
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
        sw_org = {'bottom': '50% 100%', 'center': '50% 50%'}.get(pivot_of(name) if name else None, '50% 0%')   # round 4: a pole swings from its foot, a balance beam about its middle, hanging things from the top
        return [f'tl.set({g},{{rotation:0,{org(sw_org)}}},{v0:.3f});',
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
        ax = at.get('data-axis')
        pr = {'y': 'scaleY', 'x': 'scaleX'}.get(ax, 'scale')
        if spring: fxlib.LOG['spring'] += 1; return [f'tl.set({g},{{{pr}:0,opacity:0,{org("50% 50%")}}},{v0:.3f});', f'miyaSpringTo(tl,{g},{{{pr}:0,opacity:0}},{{{pr}:1,opacity:1}},{spring[0]},{spring[1]},{st:.3f});']
        return [f'tl.set({g},{{{pr}:0,opacity:0,{org("50% 50%")}}},{v0:.3f});',
                f'tl.to({g},{{{pr}:1,opacity:1,duration:.45,ease:"back.out(2)",immediateRender:false}},{st:.3f});']
    if kind == 'slide':
        dx, dy = f('dx', -960), f('dy', 0); d = f('dur', .7)
        a, b = ({'x': 0, 'y': 0}, {'x': dx, 'y': dy}) if at.get('data-dir') == 'out' else ({'x': dx, 'y': dy}, {'x': 0, 'y': 0})
        return [f'tl.set({g},{{x:{a["x"]:.0f},y:{a["y"]:.0f}}},{v0:.3f});',
                f'tl.to({g},{{x:{b["x"]:.0f},y:{b["y"]:.0f},duration:{d},ease:"power3.{"in" if at.get("data-dir") == "out" else "out"}",immediateRender:false}},{st:.3f});']
    if kind == 'fade':
        a, b = f('from', 0), f('to', 1)
        return [f'tl.set({g},{{opacity:{a}}},{v0:.3f});',
                f'tl.to({g},{{opacity:{b},duration:{f("dur", .4)},ease:"power1.inOut",immediateRender:false}},{st:.3f});']
    if kind == 'ticks':
        return [f'miyaTicks(tl,{g},{v0:.3f},{st:.3f},{f("step", .1)},{json.dumps(at.get("data-fill", ""))},{int(f("n", 9999))});']
    if kind == 'rack':
        return [f'miyaRack(tl,{g},{v0:.3f},{st:.3f},{f("dur", 1.2)},{f("r", 14)},{1 if at.get("data-dir", "in") == "in" else 0});']
    if kind == 'shake':
        amp = f('amp', 3); dd = f('dur', .25)   # 2026-10-29: CustomWiggle (a hit that calms down) instead of a flat yoyo
        return [f'tl.fromTo({g},{{x:0}},{{x:{amp},duration:{max(dd, .2):.2f},ease:"wiggle({{wiggles:{max(int(dd / .04), 4)},type:{chr(39)}easeOut{chr(39)}}})",immediateRender:false}},{st:.3f});']
    if kind == 'dash':
        sel = f'Array.prototype.slice.call({g}.querySelectorAll("path,line,polyline,polygon,circle,ellipse,rect"))'
        return [f'tl.fromTo({sel},{{strokeDashoffset:0}},{{strokeDashoffset:{-f("speed", 40) * sp:.0f},duration:{sp:.3f},ease:"none",immediateRender:false}},{v0:.3f});']
    if kind == 'scroll':
        return [f'tl.fromTo({g},{{x:0}},{{x:{-f("dist", 160):.0f},duration:{sp:.3f},ease:"none",immediateRender:false}},{v0:.3f});']
    if kind == 'slam':
        return [f'tl.set({g},{{scale:2.4,opacity:0,rotation:{f("rot", -4)},{org("50% 50%")}}},{v0:.3f});',
                f'tl.to({g},{{scale:1,opacity:1,rotation:0,duration:.28,ease:"power4.in",immediateRender:false}},{st:.3f});']
    if kind == 'rise':
        if spring: fxlib.LOG['spring'] += 1; return [f'tl.set({g},{{y:{f("from", 60):.0f},opacity:0}},{v0:.3f});', f'miyaSpringTo(tl,{g},{{y:{f("from", 60):.0f},opacity:0}},{{y:0,opacity:1}},{spring[0]},{spring[1]},{st:.3f});']
        return [f'tl.set({g},{{y:{f("from", 60):.0f},opacity:0}},{v0:.3f});',
                f'tl.to({g},{{y:0,opacity:1,duration:{f("dur", .5)},ease:"power2.out",immediateRender:false}},{st:.3f});']
    # ---- round 4 (2026-10-26, miya: richer object motion). All continuous ones are finite yoyo tweens from v0 (seek-safe). ----
    yo = lambda per: f'ease:"sine.inOut",yoyo:true,repeat:{max(int(math.ceil(sp / per)) - 1, 0)},immediateRender:false'
    if kind == 'bob':      # floats on water: up-down data-amp (8 px) with a small roll data-deg (3) around the centre (boats, buoys, floating things)
        amp, deg, per = f('amp', 8), f('deg', 3), f('per', 2.4)
        return [f'tl.fromTo({g},{{y:{-amp:.0f},rotation:{-deg:.1f},{org("50% 50%")}}},{{y:{amp:.0f},rotation:{deg:.1f},duration:{per:.3f},{yo(per)}}},{v0:.3f});']
    if kind == 'hover':    # hangs in the air with a slow up-down (data-amp 10) and a slower sideways drift (data-dx 14): drones, UFOs, bees, helicopters, spirits
        amp, dx, per = f('amp', 10), f('dx', 14), f('per', 1.6)
        return [f'tl.fromTo({g},{{y:{-amp:.0f}}},{{y:{amp:.0f},duration:{per:.3f},{yo(per)}}},{v0:.3f});',
                f'tl.fromTo({g},{{x:{-dx:.0f}}},{{x:{dx:.0f},duration:{per * 2.3:.3f},{yo(per * 2.3)}}},{v0:.3f});']
    if kind == 'pendulum': # steady swing about data-pivot (default top centre), never dies out: clock pendulums, hanging lamps that keep swinging, a swing
        amp, per = f('amp', 18), f('per', 1.2)
        return [f'tl.fromTo({g},{{rotation:{-amp:.1f},{org("50% 0%")}}},{{rotation:{amp:.1f},duration:{per:.3f},{yo(per)}}},{v0:.3f});']
    if kind == 'wiggle':   # quick jelly-like squash and stretch (data-amp .06, data-per .35): jellyfish bells, blobs, puddings, soft creatures
        amp, per = f('amp', .06), f('per', .35)
        return [f'tl.fromTo({g},{{scaleX:{1 + amp:.3f},scaleY:{1 - amp:.3f},{org("50% 100%")}}},{{scaleX:{1 - amp:.3f},scaleY:{1 + amp:.3f},duration:{per:.3f},{yo(per)}}},{v0:.3f});']
    if kind == 'tilt':     # see-saw: slow rock by data-deg (6) about data-pivot (default centre): balance scales, rafts, teeter boards, a tipping stone
        deg, per = f('deg', 6), f('per', 2.8)
        return [f'tl.fromTo({g},{{rotation:{-deg:.1f},{org("50% 50%")}}},{{rotation:{deg:.1f},duration:{per:.3f},{yo(per)}}},{v0:.3f});']
    if kind == 'crumble':  # falls apart: each child drops (data-fall 120 px), turns a little and fades, one after another (collapse, erosion, extinction, a wall coming down)
        fall, step = f('fall', 120), f('step', .08)
        ch = f'Array.prototype.slice.call({g}.children)'
        return [f'tl.fromTo({ch},{{y:0,rotation:0,opacity:1}},{{y:{fall:.0f},rotation:(i)=>(i%2?1:-1)*(8+i*3),opacity:0,duration:{f("dur", .9)},ease:"power2.in",stagger:{step:.2f},immediateRender:false}},{st:.3f});']
    if kind == 'emph':     # attention once: grows to data-to (1.15) and back with a soft overshoot at data-delay (the thing the narration points at)
        return [f'tl.fromTo({g},{{scale:1,{org("50% 50%")}}},{{scale:{f("to", 1.15):.2f},duration:.22,ease:"power2.out",yoyo:true,repeat:1,repeatDelay:.1,immediateRender:false}},{st:.3f});']
    # ---- round 4b (2026-10-26): 28 more object motions. AXIS of each is written in its comment; data-pivot (picture coords) overrides it. ----
    pv_by_name = pivot_of(name) if name else None
    if kind == 'spin':     # continuous turn about the CENTRE (wheels, gears, fans, coins seen flat, whirlpools); data-per s per turn (6), data-dir 1/-1
        per = max(f('per', 6), .4); dr = -1 if at.get('data-dir', '1').startswith('-') else 1
        return [f'tl.fromTo({g},{{rotation:0,{org("50% 50%")}}},{{rotation:{dr * 360 * sp / per:.1f},duration:{sp:.3f},ease:"none",immediateRender:false}},{v0:.3f});']
    if kind == 'rollby':   # rolls across by data-dist px (600) turning as it goes, about the CENTRE (balls, barrels, tumbleweed, boulders); data-dur (3)
        dist, d_ = f('dist', 600), f('dur', 3)
        return [f'tl.fromTo({g},{{x:0,rotation:0,{org("50% 50%")}}},{{x:{dist:.0f},rotation:{dist / 1.2:.0f},duration:{d_},ease:"power1.inOut",immediateRender:false}},{st:.3f});']
    if kind == 'float':    # slow up-down only, no tilt (balloons, lanterns in air, jellyfish bodies, moons); data-amp 12, data-per 3
        amp, per = f('amp', 12), f('per', 3)
        return [f'tl.fromTo({g},{{y:{-amp:.0f}}},{{y:{amp:.0f},duration:{per:.3f},{yo(per)}}},{v0:.3f});']
    if kind == 'flap':     # wing beat: scaleX squeezes toward the wing ROOT (data-pivot = where the wing meets the body; default the group's inner edge), data-per .35
        per = f('per', .35)
        return [f'tl.fromTo({g},{{scaleX:1,{org("0% 50%")}}},{{scaleX:{f("to", .25):.2f},duration:{per:.3f},{yo(per)}}},{v0:.3f});']
    if kind == 'swim':     # fish: travels data-dist (400) over the picture while the body wags about its CENTRE (±data-deg 6) at data-per .5
        dist, deg, per = f('dist', 400), f('deg', 6), f('per', .5)
        return [f'tl.fromTo({g},{{x:0}},{{x:{dist:.0f},duration:{sp:.3f},ease:"sine.inOut",immediateRender:false}},{v0:.3f});',
                f'tl.fromTo({g},{{rotation:{-deg:.1f},{org("50% 50%")}}},{{rotation:{deg:.1f},duration:{per:.3f},{yo(per)}}},{v0:.3f});']
    if kind == 'hop':      # little hops about the FEET (bottom centre): squash, jump data-h (40), land; every data-per 1.4 s (small creatures, rabbits, grasshoppers)
        hgt, per = f('h', 40), f('per', 1.4); outl = []; tt = st
        while tt < v0 + sp - .9:
            outl.append(f'tl.to({g},{{scaleY:.9,scaleX:1.06,duration:.12,{org("50% 100%")}}},{tt:.3f});tl.to({g},{{scaleY:1,scaleX:1,y:{-hgt:.0f},duration:.26,ease:"power2.out",{org("50% 100%")}}},{tt + .12:.3f});tl.to({g},{{y:0,duration:.26,ease:"power2.in"}},{tt + .38:.3f});tl.to({g},{{scaleY:.94,duration:.08,yoyo:true,repeat:1,{org("50% 100%")}}},{tt + .64:.3f});'); tt += per
        return outl
    if kind == 'drip':     # a drop forms at the TOP of the group and falls data-fall px (140), fading; repeats every data-per 1.8 s (taps, stalactites, melting ice)
        fall, per = f('fall', 140), f('per', 1.8); rep = max(int(math.ceil(sp / per)) - 1, 0)
        return [f'tl.fromTo({g},{{y:0,opacity:0,scale:.3,{org("50% 0%")}}},{{keyframes:[{{opacity:1,scale:1,duration:.3}},{{y:{fall:.0f},duration:{per * .5:.2f},ease:"power2.in"}},{{opacity:0,duration:.1}}],repeat:{rep},immediateRender:false}},{v0 + .2:.3f});']
    if kind == 'unfold':   # unrolls DOWN from its top edge (maps, scrolls, banners dropping open): scaleY 0 -> 1 about the TOP, data-dur .8
        return [f'tl.set({g},{{scaleY:0,{org("50% 0%")}}},{v0:.3f});', f'tl.to({g},{{scaleY:1,duration:{f("dur", .8)},ease:"power2.out",immediateRender:false}},{st:.3f});']
    if kind == 'unroll':   # unrolls SIDEWAYS from its left edge (timelines, red carpets, tape measures): scaleX 0 -> 1 about the LEFT, data-dur .8
        return [f'tl.set({g},{{scaleX:0,{org("0% 50%")}}},{v0:.3f});', f'tl.to({g},{{scaleX:1,duration:{f("dur", .8)},ease:"power2.out",immediateRender:false}},{st:.3f});']
    if kind == 'flagwave': # cloth ripple: skewY about the LEFT edge (the pole side), ±data-deg 4, data-per .7 (flags, banners, sails, laundry)
        deg, per = f('deg', 4), f('per', .7)
        return [f'tl.fromTo({g},{{skewY:{-deg:.1f},{org("0% 50%")}}},{{skewY:{deg:.1f},duration:{per:.3f},{yo(per)}}},{v0:.3f});']
    if kind == 'ripple':   # rings spread from the group's CENTRE: the group holds 1-3 circles; each scales .3 -> 2.2 and fades, data-per 1.6 (raindrops, sonar, a stone in water)
        per = f('per', 1.6); rep = max(int((sp - per * .7) / per) - 1, 0)
        return [f'tl.fromTo(Array.prototype.slice.call({g}.children),{{scale:.3,opacity:.9,{org("50% 50%")}}},{{scale:2.2,opacity:0,duration:{per:.2f},ease:"power1.out",stagger:{{each:{per / 3:.2f},repeat:{rep}}},immediateRender:false}},{v0:.3f});']
    if kind == 'sparkle':  # the group's children twinkle one after another about their own centres (gems, stars on a map, dew): scale 1 -> 1.5 + opacity, staggered by index
        ch = f'Array.prototype.slice.call({g}.children)'; per = f('per', 1.2); rep = max(int((sp - per) / (per / 2)) - 1, 1)
        return [f'tl.fromTo({ch},{{scale:1,opacity:.6,{org("50% 50%")}}},{{scale:1.5,opacity:1,duration:{per / 2:.2f},ease:"sine.inOut",stagger:{{each:{per / 4:.2f},repeat:{rep},yoyo:true}},immediateRender:false}},{v0:.3f});']
    if kind == 'circle' and len(pv) != 2: kind = 'float'   # no orbit centre given: an orbit about its own centre would tear the object apart, so it floats instead
    if kind == 'circle':   # goes round a point: data-pivot = the ORBIT CENTRE (picture coords, REQUIRED), data-per s per lap (8), data-dir; the object keeps upright (moons, satellites, bees round a flower)
        per = max(f('per', 8), .5); dr = -1 if at.get('data-dir', '1').startswith('-') else 1; cnt = f'Array.prototype.slice.call({g}.children)'
        return [f'tl.fromTo({g},{{rotation:0,{org("50% 50%")}}},{{rotation:{dr * 360 * sp / per:.1f},duration:{sp:.3f},ease:"none",immediateRender:false}},{v0:.3f});',
                f'tl.fromTo({cnt},{{rotation:0,transformOrigin:"50% 50%"}},{{rotation:{-dr * 360 * sp / per:.1f},duration:{sp:.3f},ease:"none",immediateRender:false}},{v0:.3f});']
    if kind == 'squash':   # one impact squash-and-stretch about the FEET at data-delay (landing, a hit, a stamp on the ground), data-amp .25
        a = f('amp', .25)
        return [f'tl.fromTo({g},{{scaleY:1,scaleX:1,{org("50% 100%")}}},{{keyframes:[{{scaleY:{1 - a:.2f},scaleX:{1 + a * .7:.2f},duration:.1,ease:"power2.in"}},{{scaleY:{1 + a * .5:.2f},scaleX:{1 - a * .3:.2f},duration:.14}},{{scaleY:1,scaleX:1,duration:.3,ease:"elastic.out(1,.4)"}}],immediateRender:false}},{st:.3f});']
    if kind == 'neon':     # switches on with a flicker (neon signs, old lamps, screens): opacity 0, 1, .2, 1, .4, 1 over .9 s at data-delay
        return [f'tl.set({g},{{opacity:0}},{v0:.3f});', f'tl.to({g},{{keyframes:[{{opacity:1,duration:.08}},{{opacity:.2,duration:.1}},{{opacity:1,duration:.08}},{{opacity:.4,duration:.14}},{{opacity:1,duration:.1}}],ease:"none",immediateRender:false}},{st:.3f});']
    if kind == 'shiver':   # fine continuous tremble about the CENTRE, ±data-amp 1.5 px at .06 s (cold, fear, strain, an engine idling)
        amp = f('amp', 1.5)   # 2026-10-29: one CustomWiggle tween (uniform) over the whole stay instead of hundreds of yoyo repeats
        return [f'tl.fromTo({g},{{x:0}},{{x:{amp},duration:{sp:.3f},ease:"wiggle({{wiggles:{max(int(sp / .12), 4)},type:{chr(39)}uniform{chr(39)}}})",immediateRender:false}},{v0:.3f});']
    if kind == 'beat':     # heart beat for any object about its CENTRE: 1 -> 1.12 -> 1 -> 1.06 -> 1 then rest, every data-per 1.0 s
        per = f('per', 1.0); rep = max(int(math.ceil(sp / per)) - 1, 0)
        return [f'tl.fromTo({g},{{scale:1,{org("50% 50%")}}},{{keyframes:[{{scale:1.12,duration:.12}},{{scale:1,duration:.14}},{{scale:1.06,duration:.1}},{{scale:1,duration:.14}},{{scale:1,duration:{max(per - .5, .1):.2f}}}],ease:"power1.out",repeat:{rep},immediateRender:false}},{v0:.3f});']
    if kind == 'settle':   # wobbles to rest after a hit, about the FEET (bottom centre) unless data-pivot: rotation ±data-deg 10 decaying over data-dur 1.6, at data-delay
        deg, d_ = f('deg', 10), f('dur', 1.6); n = 6
        kf = ','.join(f'{{rotation:{deg * (-1) ** i * .6 ** i:.2f},duration:{d_ / n:.3f},ease:"sine.inOut"}}' for i in range(n)) + f',{{rotation:0,duration:{d_ / n:.3f}}}'
        return [f'tl.set({g},{{rotation:0,{org("50% 100%")}}},{v0:.3f});', f'tl.to({g},{{keyframes:[{kf}],immediateRender:false}},{st:.3f});']
    if kind == 'magnet':   # pulled to a point once with an elastic snap: data-dx / data-dy px, data-dur .9 (magnets, gravity capture, a key to a lock)
        return [f'tl.fromTo({g},{{x:0,y:0}},{{x:{f("dx", -200):.0f},y:{f("dy", 0):.0f},duration:{f("dur", .9)},ease:"elastic.out(1,.6)",immediateRender:false}},{st:.3f});']
    if kind == 'bouncing': # keeps bouncing on the spot about the FEET: drops data-h 60 px with a real bounce (CustomBounce, 2026-10-29) and a squash on each landing, every data-per .9 (balls, springs, excited things)
        hgt, per = f('h', 60), f('per', .9); rep = max(int(math.ceil(sp / per)) - 1, 0)
        return [f'tl.fromTo({g},{{y:{-hgt:.0f},{org("50% 100%")}}},{{y:0,duration:{per:.3f},ease:"miyaBnc",repeat:{rep},immediateRender:false}},{v0:.3f});',
                f'tl.fromTo({g},{{scaleX:1,scaleY:1,{org("50% 100%")}}},{{scaleX:1.25,scaleY:.75,duration:{per:.3f},ease:"miyaBnc-squash",repeat:{rep},immediateRender:false}},{v0:.3f});']
    if kind == 'creep':    # very slow sideways travel over the whole picture, data-dist 60 px (glaciers, continents, shadows, the hour hand of time)
        return [f'tl.fromTo({g},{{x:0}},{{x:{f("dist", 60):.0f},duration:{sp:.3f},ease:"none",immediateRender:false}},{v0:.3f});']
    if kind == 'sink':     # slow descent data-dist (160) with a gentle sway about the CENTRE and a fade to data-to (.35): sinking, settling dust, a sunset
        dist = f('dist', 160)
        return [f'tl.fromTo({g},{{y:0,opacity:1}},{{y:{dist:.0f},opacity:{f("to", .35)},duration:{sp:.3f},ease:"sine.in",immediateRender:false}},{v0:.3f});',
                f'tl.fromTo({g},{{rotation:-3,{org("50% 50%")}}},{{rotation:3,duration:1.8,{yo(1.8)}}},{v0:.3f});']
    if kind == 'ascend':   # slow rise data-dist (160) with a sway (balloons, lanterns, smoke rings, souls); opposite of sink
        dist = f('dist', 160)
        return [f'tl.fromTo({g},{{y:0}},{{y:{-dist:.0f},duration:{sp:.3f},ease:"sine.out",immediateRender:false}},{v0:.3f});',
                f'tl.fromTo({g},{{rotation:-3,{org("50% 50%")}}},{{rotation:3,duration:2.2,{yo(2.2)}}},{v0:.3f});']
    if kind == 'tick':     # steps round about data-pivot (default CENTRE) by data-deg 6 every data-step 1 s (second hands, ratchets, counters)
        deg, step = f('deg', 6), f('step', 1.0); outl = [f'tl.set({g},{{rotation:0,{org("50% 50%")}}},{v0:.3f});']; tt = v0 + step; k = 1
        while tt < v0 + sp:
            outl.append(f'tl.to({g},{{rotation:{deg * k:.1f},duration:.12,ease:"back.out(3)"}},{tt:.3f});'); tt += step; k += 1
        return outl
    if kind == 'flicker':  # uneven opacity flicker .55-1 (candles, torches, faulty lights, screens); period .13 s with a 3-step irregular pattern
        rep = max(int(sp / .39) - 1, 0)
        return [f'tl.fromTo({g},{{opacity:1}},{{keyframes:[{{opacity:.6,duration:.13}},{{opacity:1,duration:.1}},{{opacity:.8,duration:.16}}],ease:"none",repeat:{rep},immediateRender:false}},{v0:.3f});']
    if kind == 'breathe':  # body breathes: scaleY 1 -> 1 + data-amp .03 about the FEET (any creature or person drawn as one group), data-per 2.2
        amp, per = f('amp', .03), f('per', 2.2)
        return [f'tl.fromTo({g},{{scaleY:1,{org("50% 100%")}}},{{scaleY:{1 + amp:.3f},duration:{per:.3f},{yo(per)}}},{v0:.3f});']
    if kind == 'nodding':  # head nods about the NECK (bottom centre of the head group): ±data-deg 3, data-per 1.8
        deg, per = f('deg', 3), f('per', 1.8)
        return [f'tl.fromTo({g},{{rotation:{-deg:.1f},{org("50% 100%")}}},{{rotation:{deg:.1f},duration:{per:.3f},{yo(per)}}},{v0:.3f});']
    if kind == 'sway':     # sways about the BASE for standing things (trees, grass, poles, people), about the TOP for hanging ones (by name or data-pivot): ±data-deg 5, data-per 2.2
        deg, per = f('deg', 5), f('per', 2.2); o_ = '50% 0%' if pv_by_name == 'top' or at.get('data-hang') == '1' else '50% 100%'
        return [f'tl.fromTo({g},{{rotation:{-deg:.1f},{org(o_)}}},{{rotation:{deg:.1f},duration:{per:.3f},{yo(per)}}},{v0:.3f});']
    raise ValueError(kind)


SETTLE_KINDS = ('path', 'slide', 'slam', 'popin', 'rise', 'topple', 'flip', 'rollby', 'unfold', 'unroll', 'magnet', 'draw', 'morph', 'toss', 'skid', 'coast', 'regroup')


def settle_js(kind, g, at, t0, v0, sp):
    """(round 3, 2026-10-26) After a one-shot motion ends, the object must not freeze: when more than 2.5 s of the picture remain,
    it breathes (scale 1 -> 1.03, 2.6 s, sine) from the moment it comes to rest until the cut. Deterministic: only the group's data-* and timing matter."""
    if kind not in SETTLE_KINDS or (at.get('data-dir') == 'out'): return []
    f = lambda k, d: float(at.get('data-' + k, d))
    if kind == 'path': st, du = path_timing(at, t0, sp)
    elif kind == 'slam': st, du = t0 + f('delay', 0.3), .28
    elif kind == 'popin': st, du = t0 + f('delay', 0.3), .45
    elif kind == 'slide': st, du = t0 + f('delay', 0.3), f('dur', .7)
    elif kind == 'rise': st, du = t0 + f('delay', 0.3), f('dur', .5)
    elif kind == 'topple': st, du = t0 + f('delay', 0.3), f('dur', .55)
    elif kind == 'rollby': st, du = t0 + f('delay', 0.3), f('dur', 3)
    elif kind in ('unfold', 'unroll'): st, du = t0 + f('delay', 0.3), f('dur', .8)
    elif kind == 'magnet': st, du = t0 + f('delay', 0.3), f('dur', .9) + .6
    elif kind == 'draw': st, du = t0 + f('delay', 0.3), f('dur', 1.4) + .6
    elif kind == 'morph': st, du = t0 + f('delay', 0.3), f('dur', 1.0) * (2 if at.get('data-back') == '1' else 1) + (.6 if at.get('data-back') == '1' else 0)
    elif kind == 'toss': st, du = t0 + f('delay', 0.3), f('dur', 1.6)
    elif kind == 'skid': st, du = t0 + f('delay', 0.3), 1.6
    elif kind == 'coast': st, du = t0 + f('delay', 0.3), f('dur', 3)
    elif kind == 'regroup': st, du = t0 + f('delay', 0.3), f('dur', 1.2) + .4
    else: st, du = t0 + f('delay', 0.3), f('dur', 1.0)
    end = st + du + .15; left = (v0 + sp - .2) - end
    if left < 2.5: return []
    per = 2.6; rep = max(int(math.ceil(left / per)) - 1, 0)
    pv = at.get('data-pivot', '').replace(',', ' ').split()
    org = f'svgOrigin:miyaPv({g},{pv[0]},{pv[1]}),smoothOrigin:false' if len(pv) == 2 and kind in ('topple', 'flip') else 'transformOrigin:"50% 60%"'
    return [f'tl.fromTo({g},{{scale:1,{org}}},{{scale:1.03,duration:{per},ease:"sine.inOut",yoyo:true,repeat:{rep},immediateRender:false}},{end:.3f});']


def chalk_life_js(i, t0, t1, ts, frog_on=True):
    """(round 3, 2026-10-26) Chalkboard life. The motion check of all 4 videos found every low-motion stretch inside a chalkboard gap between row pops.
    C1 the empty dashed slots breathe (opacity .5-1, 1.1 s) until their row pops. C2 in a gap longer than 7 s, every 5 s the last filled row's value
    (or the conclusion) pulses once (scale 1.08) and the frog's pointing arm taps it (y -7). Keyed on the pop times ts only -> same result for any script."""
    js = []
    for r in (1, 2):
        nrep = int((ts[r] - t0 - .1) / 1.1) - 1
        if nrep >= 1: js.append(f'tl.fromTo("#k{i}ph{r}",{{opacity:.5}},{{opacity:1,duration:1.1,ease:"sine.inOut",yoyo:true,repeat:{nrep},immediateRender:false}},{t0 + .05:.3f});')
    for r, (ta, tb) in enumerate(zip(ts, ts[1:] + [t1])):
        if tb - ta <= 7: continue
        tp = ta + 5.0
        while tp < tb - 2:
            sel = f'#k{i}cc' if r == 3 else f'#k{i}r{r} .v'
            js.append(f'tl.fromTo("{sel}",{{scale:1,transformOrigin:"50% 50%"}},{{scale:1.08,duration:.16,ease:"power2.out",yoyo:true,repeat:1,immediateRender:false}},{tp:.3f});')
            if frog_on: js.append(f'tl.fromTo("#fgk{i}_arm",{{y:0}},{{y:-7,duration:.14,ease:"power2.out",yoyo:true,repeat:1,immediateRender:false}},{tp - .08:.3f});')
            tp += 5.0
    return js


# ---- background effects (round 4, 2026-10-26): deterministic overlays keyed on the unit's words / palette / bg mode / unit index.
# Markup goes in the unit's <div class="t"> (one <svg class="ss" id="fx{nn}"> per picture), JS on the main timeline (finite, absolute, seek-safe).
# fx_for(text, palname, bgmode, k, dur, cosmic) -> [(kind, {})] with at most ONE kind per picture; fx_markup / fx_js render it.
# Two families: PARTICLES (a table: n pieces of one shape that travel across the frame and repeat) and OVERLAYS (one-off or ambient full-frame
# effects such as flash, fog, rays, vignette). Every kind is listed in FX_KINDS. Generic "dust motes" are banned (guideline 4-1), so none here.
import math as _m

# particle table. Each row: shape, colour (paper bg, night bg), size (min, span), travel dy / dx as fractions of H / W (+ = down / right),
# period (base, span) s, sway px (x yoyo), start y fraction, fade (1 = fades out along the way), spin (deg over one travel), blink (opacity pulse s)
_P = lambda **kw: dict(dict(n=14, shape='dot', col=('#9fb6c9', '#ffffff'), size=(3, 4), dy=1.0, dx=0, per=(5, 3), sway=14, y0=-.2, fade=0, spin=0, blink=0, op=.8), **kw)
PARTICLES = {
    'snow':      _P(n=22, col=('#a9c6dc', '#ffffff'), size=(3, 5), dy=1.05, per=(5, 3.5), sway=16, y0=-.25),
    'hail':      _P(n=18, col=('#8fb0c9', '#eef6ff'), size=(2, 3), dy=1.2, dx=-.05, per=(.9, .4), sway=0, y0=-.2),
    'bubbles':   _P(n=9, shape='ring', col=('#7fb5d6', '#dff3ff'), size=(5, 9), dy=-.62, per=(3.2, 2.1), sway=10, y0=.78, fade=1, op=.55),
    'embers':    _P(n=14, col=('#ff8c2e', '#ffb347'), size=(2.5, 4), dy=-.5, per=(2.2, 1.6), sway=40, y0=.86, fade=1, op=.9),
    'sparks':    _P(n=16, shape='streak', col=('#ff9a3c', '#ffd27a'), size=(8, 10), dy=-.45, dx=.08, per=(.9, .6), sway=0, y0=.7, fade=1),
    'ash':       _P(n=16, col=('#6a6a6a', '#b9b9b9'), size=(2.5, 3), dy=.7, dx=.04, per=(7, 3), sway=22, y0=-.2, op=.6),
    'pollen':    _P(n=14, col=('#d4a820', '#fff0a0'), size=(2.5, 3), dy=-.18, dx=.12, per=(7, 3), sway=18, y0=.6, op=.7),
    'fireflies': _P(n=12, col=('#b7d94a', '#e4ff7a'), size=(3, 2), dy=-.08, dx=.06, per=(6, 3), sway=30, y0=.55, blink=1.4, op=.9),
    'leaves':    _P(n=10, shape='leaf', col=('#b8742a', '#d9924a'), size=(9, 6), dy=1.0, dx=.12, per=(6, 3), sway=40, y0=-.2, spin=200, op=.85),
    'petals':    _P(n=14, shape='petal', col=('#f2a6c0', '#ffc2d6'), size=(6, 4), dy=1.0, dx=.15, per=(6, 3), sway=36, y0=-.2, spin=160, op=.85),
    'confetti':  _P(n=24, shape='flake', col=('#ff5c7a', '#ffd166'), size=(5, 4), dy=1.0, dx=.05, per=(3.5, 2), sway=30, y0=-.2, spin=540, op=.9),
    'feathers':  _P(n=7, shape='feather', col=('#9fb0c3', '#f4f7fb'), size=(14, 8), dy=1.0, dx=.1, per=(8, 3), sway=70, y0=-.2, spin=60, op=.85),
    'sand':      _P(n=26, col=('#a8824a', '#e6cb8a'), size=(2, 2), dy=-.03, dx=1.1, per=(1.4, 1), sway=0, y0=.55, op=.6),
    'meteors':   _P(n=6, shape='streak', col=('#ffffff', '#ffffff'), size=(40, 40), dy=.5, dx=.6, per=(1.2, .8), sway=0, y0=-.1, fade=1, op=.9),
    'twinkle':   _P(n=18, shape='star', col=('#d9e6f2', '#ffffff'), size=(2, 2.5), dy=0, dx=0, per=(9, 1), sway=0, y0=.05, blink=2.2, op=.9),
    'coins':     _P(n=10, shape='coin', col=('#d4a017', '#ffd34a'), size=(7, 4), dy=1.0, dx=.03, per=(3.5, 2), sway=10, y0=-.2, spin=0, op=.95),
    'notes':     _P(n=10, shape='text:♪', col=('#4a5a7a', '#ffffff'), size=(18, 10), dy=-.45, dx=.05, per=(5, 2.5), sway=20, y0=.75, fade=1, spin=20, op=.9),
    'hearts':    _P(n=10, shape='heart', col=('#ff6b8a', '#ff8fa8'), size=(6, 5), dy=-.5, dx=.04, per=(5, 2.5), sway=20, y0=.8, fade=1, op=.9),
    'questions': _P(n=8, shape='text:?', col=('#5a6a8a', '#ffffff'), size=(20, 12), dy=-.4, dx=.06, per=(5.5, 2.5), sway=22, y0=.75, fade=1, spin=25, op=.85),
    'plankton':  _P(n=20, col=('#4f92a8', '#bfeeff'), size=(2, 2), dy=-.1, dx=.08, per=(8, 3), sway=12, y0=.5, blink=3, op=.7),
    'seeds':     _P(n=9, shape='seed', col=('#8a949c', '#f0f4f7'), size=(8, 4), dy=-.25, dx=.35, per=(7, 3), sway=24, y0=.5, spin=40, op=.85),
    'spores':    _P(n=16, col=('#6a9a4a', '#c6f09a'), size=(2.5, 2), dy=-.3, dx=.03, per=(7, 3), sway=14, y0=.7, fade=1, op=.75),
    'bats':      _P(n=5, shape='bat', col=('#2a2a3a', '#101018'), size=(12, 6), dy=-.08, dx=1.3, per=(2.6, 1.4), sway=28, y0=.25, op=.9),
    'birds':     _P(n=6, shape='bird', col=('#44505f', '#e8eef5'), size=(10, 6), dy=-.05, dx=1.3, per=(6, 3), sway=20, y0=.18, op=.8),
    'fish':      _P(n=5, shape='fish', col=('#5f88a8', '#8fc3e8'), size=(16, 10), dy=.02, dx=1.3, per=(7, 4), sway=12, y0=.45, op=.75),
    'jellies':   _P(n=5, shape='jelly', col=('#b9a0d8', '#e0c8ff'), size=(10, 6), dy=-.3, dx=.05, per=(9, 3), sway=20, y0=.75, blink=2.6, op=.7),
    'germs':     _P(n=10, shape='germ', col=('#7fb86a', '#b6f09a'), size=(6, 4), dy=-.12, dx=.1, per=(8, 3), sway=26, y0=.55, spin=90, op=.8),
    'lanterns':  _P(n=6, shape='lantern', col=('#ffb24a', '#ffcf7a'), size=(10, 5), dy=-.6, dx=.06, per=(10, 3), sway=18, y0=.9, blink=2.4, op=.95),
    'balloons':  _P(n=7, shape='balloon', col=('#ff6b6b', '#ff8c8c'), size=(10, 5), dy=-.8, dx=.08, per=(9, 3), sway=22, y0=.95, op=.9),
    'droplets':  _P(n=14, shape='drop', col=('#5f95b6', '#cfe9ff'), size=(4, 3), dy=1.1, dx=0, per=(1.6, .8), sway=0, y0=-.2, op=.7),
    'bones':     _P(n=0),   # placeholder so the name is reserved; never drawn (grim topics get 'vignette' instead)
}
PARTICLES.pop('bones')
# overlay kinds: one-off or ambient full-frame effects (no particles)
OVERLAYS = ['burst',   # 2026-10-29: Physics2D burst (guideline 4-6)
            'rain', 'flash', 'bolt', 'fog', 'heat', 'rays', 'searchlight', 'vignette', 'tint', 'clouds', 'windlines', 'smoke', 'steam',
            'shockwave', 'letterbox', 'scanlines', 'glitch', 'lightleak', 'flare', 'aurora', 'ripples', 'waves', 'rainbow', 'spotlight', 'frost', 'starburst']
FX_KINDS = list(PARTICLES) + OVERLAYS

# word rules in priority order (first match wins). A rule may be limited to a bg mode ('night'/'paper') or min duration.
FX_WORDS = [
    ('burst', r'\b(confetti|fireworks?|shatter\w*|scatter\w*|splash\w*|spray\w*|debris|shrapnel|erupt\w*|burst\w*|explo(d|s)\w*|detonat\w*|sneez\w*|spew\w*|eject\w*|pop(s|ped|ping)? (open|out)|blow\w* (up|apart))\b', None),
    ('flash', r'\b(lightning|explo(d|s)\w*|flash\w*|boom|blast\w*|burst\w*|supernova\w*|big bang|detonat\w*|erupt\w*)\b', None),
    ('bolt', r'\b(thunder\w*|lightning)\b', None),
    ('shockwave', r'\b(earthquake\w*|impact\w*|shock\s?wave\w*|collid\w*|collision\w*|crash\w*|slam\w*|tremor\w*)\b', None),
    ('rain', r'\b(rain\w*|downpour|monsoon|drizzl\w*|thunderstorm\w*)\b', None),
    ('hail', r'\b(hail\w*|sleet)\b', None),
    ('snow', r'\b(snow\w*|blizzard\w*|snowfall|flakes?|ice age|frozen (world|land|planet)|winter)\b', None),
    ('frost', r'\b(frost\w*|freez\w*|frozen|icy|subzero|permafrost)\b', None),
    ('embers', r'\b(fire\w*|flames?|burn\w*|campfire|bonfire|lava|volcano\w*|embers?|wildfire\w*)\b', None),
    ('sparks', r'\b(sparks?|forge\w*|weld\w*|anvil|blacksmith\w*|grind\w*)\b', None),
    ('smoke', r'\b(smoke\w*|smog|soot|chimney\w*|factory|factories|industrial)\b', None),
    ('steam', r'\b(steam\w*|boil\w*|geyser\w*|hot spring\w*|kettle)\b', None),
    ('ash', r'\b(ash\w*|ruins?|rubble|aftermath|wasteland|cinders?)\b', None),
    ('fog', r'\b(fog\w*|mists?|misty|haze|hazy|murky|gloom\w*)\b', None),
    ('windlines', r'\b(wind\w*|gale\w*|gust\w*|breez\w*|hurricane\w*|typhoon\w*|tornado\w*)\b', None),
    ('sand', r'\b(sand\w*|dune\w*|desert\w*|sahara|dust storm\w*)\b', None),
    ('heat', r'\b(heat\w*|scorch\w*|blazing|sweltering|hottest)\b', None),
    ('waves', r'\b(waves?|tsunami\w*|tide\w*|surf\w*|swell\w*)\b', None),
    ('ripples', r'\b(rippl\w*|ponds?|puddle\w*|droplet\w*|splash\w*)\b', None),
    ('droplets', r'\b(drip\w*|leak\w*|dripping|trickl\w*)\b', None),
    ('bubbles', r'\b(bubbl\w*|breath\w* out|exhal\w*|fizz\w*|carbonat\w*)\b', None),
    ('plankton', r'\b(plankton|krill|microb\w*|algae|bloom\w*)\b', None),
    ('fish', r'\b(fish\w*|shoal\w*|school of|sardine\w*|tuna|salmon|shark\w*)\b', None),
    ('jellies', r'\b(jellyfish|jellies|medusa\w*)\b', None),
    ('aurora', r'\b(aurora\w*|northern lights|southern lights)\b', None),
    ('meteors', r'\b(meteor\w*|asteroid\w*|comet\w*|shooting stars?)\b', None),
    ('rays', r'\b(dawn|sunrise|sunlight|sunbeam\w*|daybreak|morning sun|hope\w*|holy|sacred|revelation)\b', None),
    ('flare', r'\b(glare|blinding|dazzl\w*|solar flare\w*|brightest|glint\w*)\b', None),
    ('rainbow', r'\b(rainbow\w*|prism\w*|spectrum)\b', None),
    ('searchlight', r'\b(searchlight\w*|spotlight\w*|radar|lighthouse\w*|patrol\w*)\b', None),
    ('hearts', r'\b(love\w*|romance|romantic|kiss\w*|beloved|sweetheart\w*|affection\w*)\b', None),
    ('notes', r'\b(music\w*|song\w*|sing(s|ing|ers?)?|melod\w*|orchestra\w*|concert\w*|rhythm\w*|humming)\b', None),
    ('questions', r'\b(mystery|mysterious|puzzl\w*|riddle\w*|nobody knows|no one knows|unsolved|unknown)\b', None),
    ('confetti', r'\b(celebrat\w*|party|parties|victory|victories|champion\w*|festival\w*|parade\w*|triumph\w*)\b', None),
    ('lanterns', r'\b(lantern\w*|temple\w*|shrine\w*|ceremony|ceremonies|ritual\w*)\b', None),
    ('balloons', r'\b(balloon\w*|birthday\w*|carnival\w*)\b', None),
    ('coins', r'\b(coins?|money|gold|treasure\w*|wealth\w*|riches|fortune\w*|jackpot\w*)\b', None),
    ('bats', r'\b(bats?|cave\w*|vampire\w*|cavern\w*)\b', 'night'),
    ('birds', r'\b(birds?|flocks?|migrat\w*|geese|swallows|seagull\w*|gulls?)\b', None),
    ('feathers', r'\b(feather\w*|plumage|wings?|pillow\w*)\b', None),
    ('leaves', r'\b(autumn|fall(ing)? leaves|leaves|leaf|foliage|deciduous)\b', None),
    ('petals', r'\b(petal\w*|blossom\w*|cherry|sakura|spring\w*|bloom\w*)\b', None),
    ('pollen', r'\b(pollen|bees?|honey\w*|meadow\w*|wildflower\w*|flowers?)\b', None),
    ('seeds', r'\b(seeds?|dandelion\w*|disperse\w*)\b', None),
    ('spores', r'\b(spores?|fung\w*|mushroom\w*|mold|mould|mycel\w*)\b', None),
    ('germs', r'\b(germs?|bacteri\w*|virus\w*|infect\w*|pathogen\w*|microbe\w*)\b', None),
    ('fireflies', r'\b(firefl\w*|glow\w*|twilight|dusk|evening)\b', 'night'),
    ('twinkle', r'\b(stars?|starry|constellation\w*|night sky|galax\w*)\b', 'night'),
    ('glitch', r'\b(glitch\w*|corrupt\w*|malfunction\w*|static|signal\w* (lost|broke)|errors?)\b', None),
    ('scanlines', r'\b(television|\btv\b|broadcast\w*|footage|camera\w*|recording\w*|screen\w*|monitor\w*)\b', None),
    ('letterbox', r'\b(cinema\w*|movie\w*|film\w*|hollywood|director\w*)\b', None),
    ('lightleak', r'\b(dream\w*|memor\w*|nostalg\w*|childhood|remember\w*|long ago)\b', None),
    ('vignette', r'\b(death\w*|died|dying|dead|grave\w*|funeral\w*|mourn\w*|extinct\w*|doom\w*|tragic\w*|tragedy)\b', None),
    ('starburst', r'\b(discover\w*|eureka|breakthrough\w*|invent\w*|genius|brilliant)\b', None),
    ('spotlight', r'\b(famous|celebrity|on stage|theat(re|er)|performance\w*|audience\w*|spotlight\w*)\b', None),
    ('clouds', r'\b(clouds?|cloudy|overcast|sky|skies)\b', None),
    ('tint', r'\b(blood\w*|wound\w*|poison\w*|toxic\w*|radiat\w*)\b', None),
]
FX_WORDS = [(k, _re.compile(p, _re.I), bg) for k, p, bg in FX_WORDS]
# ambient rotation per palette when no word applies: every second picture (k % 2 == 0) gets the next kind of its palette's list (by k // 2)
FX_AMBIENT = {
    'ocean': ['bubbles', 'plankton', 'fish', 'ripples'], 'forest': ['pollen', 'leaves', 'seeds', 'spores'], 'desert': ['sand', 'heat', 'rays'],
    'ice': ['snow', 'frost', 'fog'], 'storm': ['windlines', 'fog', 'rain', 'ash'], 'history': ['fog', 'rays', 'lightleak'], 'sunset': ['lightleak', 'petals', 'rays'],
    'lab': ['scanlines', 'germs'], 'body': [], 'space': ['twinkle', 'meteors'], 'deepfield': ['twinkle', 'meteors'], 'nebula': ['twinkle', 'aurora'],
    'aurora': ['aurora', 'twinkle'], 'solar': ['flare', 'sparks'],
}
NIGHT_ONLY = {'twinkle', 'fireflies', 'bats', 'meteors', 'aurora', 'lanterns', 'searchlight', 'spotlight'}
# legacy names kept for build3 (flash word timing)
FLASHW = FX_WORDS[0][1]


HEAVY_FX = {'burst', 'vignette', 'tint', 'spotlight', 'letterbox', 'scanlines', 'flash', 'glitch', 'shockwave', 'bolt', 'starburst', 'frost'}


FX_PIC = [   # picture evidence (tools/picev.py tags) -> background effect, in priority order; used when no word rule matched (miya 2026-10-27)
    ('fire', 'embers'), ('smoke', 'smoke'), ('steam', 'steam'), ('rain', 'rain'), ('ice', 'frost'), ('candle', 'lightleak'), ('bubble', 'bubbles'),
    ('water', 'bubbles'), ('flower', 'petals'), ('forest', 'pollen'), ('desert', 'heat'), ('sun', 'rays'), ('insect', 'fireflies'), ('bird', 'feathers'),
    ('wind', 'windlines'), ('cloud', 'clouds'), ('space', 'twinkle'), ('cave', 'fog'), ('bone', 'plankton')]
FX_PIC_DAY = {'bubbles': 'ripples', 'fireflies': 'pollen', 'twinkle': 'rays', 'embers': 'sparks'}   # paper-background stand-ins for night-only kinds


def fx_for(text, palname, bgmode, k, dur, cosmic=False, prev=(), pic=None):
    """Which background effect a picture gets (at most ONE), deterministic: word rules in FX_WORDS order, else the palette's ambient
    rotation on every second picture. Cosmic pictures keep the shooting star on k % 3 == 1 and get an ambient kind only on k % 3 == 0.
    Pictures under 3 s get none. Night-only kinds never land on a paper background. prev = the kinds of the previous pictures (in order):
    a word-matched kind may repeat on the next picture when the words repeat (miya 2026-10-27: no blanket 'never twice in a row'; the situation
    decides), the ambient filler rotates away from the last kind, and a heavy full-frame kind (vignette, flash, letterbox ...) needs two pictures
    without any heavy kind before it (eye comfort, not a repeat ban)."""
    if dur < 3: return []
    prev = [x for x in prev]; last = prev[-1] if prev else None; heavy_recent = any(x in HEAVY_FX for x in prev[-2:])
    kind = None
    for kd, rx, bg in FX_WORDS:
        if bg and bgmode != bg: continue
        if rx.search(text): kind = kd; break
    if kind is None and pic:   # the picture shows it (chimney -> smoke, drawn fire -> embers, a lake -> ripples): situational like a word rule, may repeat
        for tag, kd in FX_PIC:
            if tag in pic:
                kind = kd
                if kind in NIGHT_ONLY and bgmode != 'night': kind = FX_PIC_DAY.get(kind)
                if kind: break
    if kind is None:
        amb = FX_AMBIENT.get(palname, [])
        if amb and dur > 5 and ((cosmic and k % 3 == 0) or (not cosmic and k % 2 == 0)):
            kind = amb[(k // 2) % len(amb)]
            if kind == last and len(amb) > 1: kind = amb[(k // 2 + 1) % len(amb)]   # filler only: a different ambient than the last picture
    if kind is None: return []
    if kind in HEAVY_FX and heavy_recent: return []
    if kind in NIGHT_ONLY and bgmode != 'night': return []
    if cosmic and kind in ('flash',) and k % 3 == 1: return []   # never flash and shooting star on the same cosmic picture
    return [(kind, {})]


def _shape(sh, x, y, r, col, op, pid, flipx=1):
    """one particle element of size r, placed by an outer <g translate> that is never tweened (GSAP x/y replace, not add, a transform
    attribute, so the position must live on a parent); the inner element carries the id that JS addresses"""
    return f'<g transform="translate({x:.0f} {y:.0f}){" scale(-1 1)" if flipx < 0 else ""}">{_shape0(sh, r, col, op, pid)}</g>'


def _shape0(sh, r, col, op, pid):
    x = y = 0
    a = f'id="{pid}" fill="{col}" opacity="{op}"'
    if sh == 'dot': return f'<circle {a} cx="{x:.0f}" cy="{y:.0f}" r="{r:.1f}"/>'
    if sh == 'ring': return f'<circle {a} cx="{x:.0f}" cy="{y:.0f}" r="{r:.1f}" fill="none" stroke="{col}" stroke-width="2"/>'
    if sh == 'streak' or sh.startswith('streak:'):   # tail trails BEHIND the travel: 'streak:dx:dy' (fractions, + = right/down) sets the direction; plain = tail up-left
        tx, ty = (-.55, 1.0)
        if ':' in sh:
            ddx, ddy = float(sh.split(':')[1]), float(sh.split(':')[2]); L = (ddx * ddx + ddy * ddy) ** .5 or 1; tx, ty = -ddx / L * 1.1, -ddy / L * 1.1
        return f'<line {a} x1="{x:.0f}" y1="{y:.0f}" x2="{x + r * tx:.0f}" y2="{y + r * ty:.0f}" stroke="{col}" stroke-width="2.4" stroke-linecap="round"/>'
    if sh == 'star': return f'<circle {a} cx="{x:.0f}" cy="{y:.0f}" r="{r:.1f}"/>'
    if sh == 'leaf': return f'<path {a} d="M0 {-r:.0f} C{r * .9:.0f} {-r * .4:.0f} {r * .9:.0f} {r * .5:.0f} 0 {r:.0f} C{-r * .9:.0f} {r * .5:.0f} {-r * .9:.0f} {-r * .4:.0f} 0 {-r:.0f}Z"/>'
    if sh == 'petal': return f'<ellipse {a} cx="0" cy="0" rx="{r * .55:.1f}" ry="{r:.1f}"/>'
    if sh == 'flake': return f'<rect {a} x="{-r * .5:.1f}" y="{-r * .3:.1f}" width="{r:.1f}" height="{r * .6:.1f}"/>'
    if sh == 'feather': return f'<path {a} d="M0 {-r:.0f} Q{r * .6:.0f} 0 0 {r:.0f} Q{-r * .25:.0f} 0 0 {-r:.0f}Z M0 {-r * .8:.0f} L0 {r * 1.2:.0f}" stroke="{col}" stroke-width="1.2"/>'
    if sh == 'coin': return f'<g {a}><circle r="{r:.1f}" fill="{col}"/><circle r="{r * .6:.1f}" fill="none" stroke="#7a5a10" stroke-width="1.4" opacity=".7"/></g>'
    if sh.startswith('text:'): return f'<text {a} font-size="{r:.0f}" font-family="Georgia,serif" text-anchor="middle" font-weight="700">{sh[5:]}</text>'
    if sh == 'heart': return f'<path {a} transform="scale({r / 6:.2f})" d="M0 5 C-7 -1 -6 -8 -1 -7 C0 -7 0 -6 0 -5 C0 -6 0 -7 1 -7 C6 -8 7 -1 0 5Z"/>'
    if sh == 'seed': return f'<g {a} stroke="{col}" stroke-width="1"><circle cy="{r:.0f}" r="1.6" fill="{col}"/><line x1="0" y1="{r:.0f}" x2="0" y2="{-r * .3:.0f}"/><line x1="0" y1="{-r * .3:.0f}" x2="{-r * .7:.0f}" y2="{-r:.0f}"/><line x1="0" y1="{-r * .3:.0f}" x2="{r * .7:.0f}" y2="{-r:.0f}"/><line x1="0" y1="{-r * .3:.0f}" x2="0" y2="{-r * 1.1:.0f}"/></g>'
    if sh == 'bat': return f'<path {a} d="M{-r:.0f} 0 Q{-r * .5:.0f} {-r * .7:.0f} 0 0 Q{r * .5:.0f} {-r * .7:.0f} {r:.0f} 0 Q{r * .5:.0f} {r * .25:.0f} 0 {r * .15:.0f} Q{-r * .5:.0f} {r * .25:.0f} {-r:.0f} 0Z"/>'
    if sh == 'bird': return f'<path {a} d="M{-r:.0f} 0 Q{-r * .5:.0f} {-r * .6:.0f} 0 0 Q{r * .5:.0f} {-r * .6:.0f} {r:.0f} 0" fill="none" stroke="{col}" stroke-width="2" stroke-linecap="round"/>'
    if sh == 'fish': return f'<path {a} d="M{r:.0f} 0 Q{r * .4:.0f} {-r * .5:.0f} {-r * .4:.0f} 0 Q{r * .4:.0f} {r * .5:.0f} {r:.0f} 0Z M{-r * .4:.0f} 0 L{-r:.0f} {-r * .35:.0f} L{-r:.0f} {r * .35:.0f}Z"/>'   # head at +x: the fish row travels right (2026-10-27, miya: fish swam backwards)
    if sh == 'jelly': return f'<g {a} stroke="{col}" stroke-width="1.2"><path d="M{-r:.0f} 0 A{r:.0f} {r:.0f} 0 0 1 {r:.0f} 0Z"/><line x1="{-r * .5:.0f}" y1="0" x2="{-r * .6:.0f}" y2="{r * 1.3:.0f}"/><line x1="0" y1="0" x2="{r * .1:.0f}" y2="{r * 1.5:.0f}"/><line x1="{r * .5:.0f}" y1="0" x2="{r * .6:.0f}" y2="{r * 1.3:.0f}"/></g>'
    if sh == 'germ': return f'<g {a} stroke="{col}" stroke-width="1.4"><ellipse rx="{r:.0f}" ry="{r * .65:.0f}"/>' + ''.join(f'<line x1="{r * _m.cos(t) * .9:.0f}" y1="{r * _m.sin(t) * .6:.0f}" x2="{r * _m.cos(t) * 1.5:.0f}" y2="{r * _m.sin(t) * 1.1:.0f}"/>' for t in (0, 1, 2, 3, 4, 5)) + '</g>'
    if sh == 'lantern': return f'<g {a}><rect x="{-r * .5:.0f}" y="{-r:.0f}" width="{r:.0f}" height="{r * 1.6:.0f}" rx="{r * .3:.0f}"/><rect x="{-r * .2:.0f}" y="{-r * 1.25:.0f}" width="{r * .4:.0f}" height="{r * .3:.0f}" fill="#7a4a10"/></g>'
    if sh == 'balloon': return f'<g {a}><ellipse rx="{r * .7:.0f}" ry="{r:.0f}"/><line x1="0" y1="{r:.0f}" x2="{r * .15:.0f}" y2="{r * 2.2:.0f}" stroke="{col}" stroke-width="1"/></g>'
    if sh == 'drop': return f'<path {a} d="M0 {-r * 1.4:.0f} Q{r:.0f} {r * .2:.0f} 0 {r:.0f} Q{-r:.0f} {r * .2:.0f} 0 {-r * 1.4:.0f}Z"/>'
    return f'<circle {a} cx="{x:.0f}" cy="{y:.0f}" r="{r:.1f}"/>'


CREATURE_ROWS = ('fish', 'birds', 'bats')   # go with the picture's travel (schooling); other drifting rows go with the wind


def dir_sign(kind, wind=1, travel=0):
    """horizontal sign for a particle row / overlay in this picture (2026-10-27, miya: wind and pull are directions too)"""
    if kind in CREATURE_ROWS: return travel or 1
    if kind in ('pollen', 'spores', 'plankton', 'fireflies', 'germs'): return 1   # these alternate per piece anyway
    return wind or 1


def fx_markup(nn, kind, W, H, bgmode='night', wind=1, travel=0):
    """one <svg class="ss" id="fx{nn}"> overlay (same class as the shooting star: full frame, pointer-events none, opacity 0 until its tween)"""
    g = []; ci = 1 if bgmode == 'night' else 0; I = f'fx{nn}'; ds = dir_sign(kind, wind, travel)
    if kind in PARTICLES:
        P = PARTICLES[kind]; col = P['col'][ci]
        for i in range(P['n']):   # positions by golden-ratio sequences: spread, never random, same every build
            x = W * (.04 + ((i * .618 + nn * .13) % 1) * .92); y = H * (P['y0'] + ((i * .382) % 1) * (.3 if P['dy'] else .6))
            r = (P['size'][0] + (i * 7 % 10) / 10 * P['size'][1]) * 2.2   # sizes are for a 1920 x 1080 frame
            shp = f"streak:{P['dx'] * ds * 1920:.0f}:{P['dy'] * 1080:.0f}" if P['shape'] == 'streak' else P['shape']   # streak tails trail behind the travel (2026-10-27)
            g.append(_shape(shp, x, y, r, col, P['op'], f'{I}p{i}', flipx=ds if kind in CREATURE_ROWS else 1))
    elif kind == 'burst':   # 2026-10-29: 72 pieces at the frame centre, thrown by Physics2DPlugin at the word (velocity / angle / gravity by golden-ratio sequences, never random)
        cols = ['#ff5c7a', '#ffd166', '#5fbfa0', '#6f8fe8', '#b58fe0'] if bgmode != 'night' else ['#ffd166', '#ffffff', '#8fc3e8', '#ff9a8c', '#c9b3ff']
        for i in range(72):
            r = 5 + (i * 7 % 9); sh = f'<circle id="{I}p{i}" r="{r * .5:.1f}" fill="{cols[i % 5]}"/>' if i % 3 else f'<rect id="{I}p{i}" x="{-r:.0f}" y="{-r * .35:.0f}" width="{r * 2:.0f}" height="{r * .7:.0f}" rx="2" fill="{cols[i % 5]}"/>'
            g.append(f'<g transform="translate({W / 2:.0f} {H * .5:.0f})">{sh}</g>')
        g.append(f'<circle id="{I}a" cx="{W / 2:.0f}" cy="{H * .5:.0f}" r="30" fill="none" stroke="#fff" stroke-width="8" opacity="0"/>')
    elif kind == 'rain':
        for i in range(26):
            x = W * (((i * .618) % 1)); y = H * (((i * .382) % 1)); L = 26 + (i * 5) % 18
            g.append(f'<line id="{I}p{i}" x1="{x:.0f}" y1="{y:.0f}" x2="{x + ds * L * .35:.0f}" y2="{y + L:.0f}" stroke="{"#cfe6ff" if ci else "#7fa6c9"}" stroke-width="2.2" stroke-linecap="round" opacity=".55"/>')   # slants with the wind
    elif kind in ('flash', 'tint', 'vignette', 'frost'):
        if kind == 'flash': g.append(f'<rect id="{I}a" x="0" y="0" width="{W}" height="{H}" fill="#fff" opacity="0"/>')
        elif kind == 'tint': g.append(f'<rect id="{I}a" x="0" y="0" width="{W}" height="{H}" fill="#b0102a" opacity="0"/>')
        else:
            cc = '#0b0f1a' if kind != 'frost' else '#dff3ff'
            g.append(f'<defs><radialGradient id="{I}g" cx="50%" cy="50%" r="70%"><stop offset="55%" stop-color="{cc}" stop-opacity="0"/><stop offset="100%" stop-color="{cc}" stop-opacity="{.85 if kind != "frost" else .8}"/></radialGradient></defs><rect id="{I}a" x="0" y="0" width="{W}" height="{H}" fill="url(#{I}g)" opacity="0"/>')
    elif kind == 'bolt':
        pts = ' '.join(f'{W * (.62 + (j % 2) * .04 - j * .012):.0f},{H * (j / 7):.0f}' for j in range(8))
        g.append(f'<polyline id="{I}a" points="{pts}" fill="none" stroke="{"#fff" if ci else "#3a4a7a"}" stroke-width="{4 if ci else 6}" stroke-linejoin="round" opacity="0"/><rect id="{I}b" x="0" y="0" width="{W}" height="{H}" fill="#dde8ff" opacity="0"/>')
    elif kind in ('fog', 'clouds', 'smoke', 'steam'):
        n = 7 if kind in ('fog', 'clouds') else 9; col = {'fog': '#dfe6ee', 'clouds': '#ffffff' if ci else '#f4f6f8', 'smoke': '#6b6b70', 'steam': '#ffffff'}[kind]
        for i in range(n):
            if kind in ('fog', 'clouds'):
                y = H * ((.12 if kind == 'clouds' else .55) + ((i * .382) % 1) * .35); rx = W * (.18 + (i * 3 % 5) * .03); ry = H * (.05 + (i % 3) * .015)
                g.append(f'<ellipse id="{I}p{i}" cx="{W * ((i * .618) % 1):.0f}" cy="{y:.0f}" rx="{rx:.0f}" ry="{ry:.0f}" fill="{col}" opacity="{.16 if kind == "fog" else .5}"/>')
            else:
                x = W * (.3 + ((i * .618) % 1) * .4); r = 14 + (i * 3 % 5) * 5
                g.append(f'<circle id="{I}p{i}" cx="{x:.0f}" cy="{H * .9:.0f}" r="{r}" fill="{col}" opacity=".35"/>')
    elif kind == 'heat':
        for i in range(8):
            y = H * (.35 + i * .07); d = ' '.join(f'{"M" if j == 0 else "L"}{W * j / 16:.0f} {y + (6 if j % 2 else -6):.0f}' for j in range(17))
            g.append(f'<path id="{I}p{i}" d="{d}" fill="none" stroke="{"#fff" if ci else "#5a4a30"}" stroke-width="1.6" opacity="{.18 if ci else .12}"/>')
    elif kind in ('rays', 'searchlight', 'spotlight', 'starburst'):
        cx, cy = (W * .5, H * .5) if kind == 'starburst' else (W * .85, -H * .1) if kind == 'rays' else (W * .5, H * 1.15) if kind == 'searchlight' else (W * .5, -H * .2)
        if kind == 'spotlight':
            g.append(f'<defs><radialGradient id="{I}g" cx="50%" cy="20%" r="60%"><stop offset="0%" stop-color="#fff" stop-opacity=".0"/><stop offset="45%" stop-color="#000" stop-opacity=".0"/><stop offset="100%" stop-color="#000" stop-opacity=".75"/></radialGradient></defs><rect id="{I}a" x="0" y="0" width="{W}" height="{H}" fill="url(#{I}g)" opacity="0"/><polygon id="{I}b" points="{cx - 40:.0f},{cy:.0f} {cx + 40:.0f},{cy:.0f} {cx + W * .22:.0f},{H * .95:.0f} {cx - W * .22:.0f},{H * .95:.0f}" fill="{"#fff" if ci else "#f6c948"}" opacity="{.12 if ci else .2}"/>')
        else:
            n = 12 if kind != 'searchlight' else 1; col = ('#ffe9a8' if ci else '#f2b84a') if kind == 'rays' else ('#fff' if ci else '#f6c948')
            g.append(f'<g id="{I}r">')
            for i in range(n):   # rays: a fan from the top-right corner towards the bottom-left (SVG rotation is clockwise, so 6..72 deg swings a downward ray to the left)
                g.append(f'<polygon id="{I}p{i}" points="{cx:.0f},{cy:.0f} {cx + W * .05:.0f},{cy + H * 2.2:.0f} {cx - W * .05:.0f},{cy + H * 2.2:.0f}" fill="{col}" opacity="{(.08 if ci else .14) if kind != "searchlight" else (.16 if ci else .28)}" transform="rotate({i * (360 / n) if kind == "starburst" else 6 + i * 6 if kind == "rays" else 0:.1f} {cx:.0f} {cy:.0f})"/>')
            g.append('</g>')
    elif kind == 'windlines':
        if ds < 0: g.append(f'<g transform="translate({W} 0) scale(-1 1)">')   # wind blowing left: the whole overlay mirrored (the tween still adds +x)
        for i in range(12):
            y = H * (((i * .382) % 1)); L = W * (.12 + (i % 4) * .05)
            g.append(f'<line id="{I}p{i}" x1="{-L:.0f}" y1="{y:.0f}" x2="0" y2="{y:.0f}" stroke="{"#fff" if ci else "#7a8a9a"}" stroke-width="2.5" stroke-linecap="round" opacity=".4"/>')
        if ds < 0: g.append('</g>')
    elif kind == 'shockwave':
        g.append(f'<circle id="{I}a" cx="{W / 2:.0f}" cy="{H / 2:.0f}" r="40" fill="none" stroke="#fff" stroke-width="10" opacity="0"/>')
    elif kind == 'letterbox':
        g.append(f'<rect id="{I}a" x="0" y="{-H * .11:.0f}" width="{W}" height="{H * .11:.0f}" fill="#000"/><rect id="{I}b" x="0" y="{H:.0f}" width="{W}" height="{H * .11:.0f}" fill="#000"/>')
    elif kind == 'scanlines':
        g.append(f'<defs><pattern id="{I}g" width="4" height="4" patternUnits="userSpaceOnUse"><rect width="4" height="2" fill="#000" opacity=".1"/></pattern></defs><rect id="{I}a" x="0" y="0" width="{W}" height="{H}" fill="url(#{I}g)"/>')
    elif kind == 'glitch':
        for i in range(5):
            g.append(f'<rect id="{I}p{i}" x="0" y="{H * (.12 + i * .17):.0f}" width="{W}" height="{8 + i * 3}" fill="{"#49f0ff" if i % 2 else "#ff4d9a"}" opacity="0"/>')
    elif kind in ('lightleak', 'flare'):
        col = '#ffb070' if kind == 'lightleak' else '#fff'
        g.append(f'<defs><radialGradient id="{I}g"><stop offset="0%" stop-color="{col}" stop-opacity=".55"/><stop offset="100%" stop-color="{col}" stop-opacity="0"/></radialGradient></defs>')
        if kind == 'lightleak': g.append(f'<ellipse id="{I}a" cx="{W * .9:.0f}" cy="{H * .2:.0f}" rx="{W * .45:.0f}" ry="{H * .6:.0f}" fill="url(#{I}g)"/>')
        else:
            g.append(f'<circle id="{I}a" cx="{W * .78:.0f}" cy="{H * .22:.0f}" r="{H * .22:.0f}" fill="url(#{I}g)"/>')
            for i, (f, r) in enumerate(((.35, 18), (.55, 10), (.72, 26), (.9, 8))):
                g.append(f'<circle id="{I}p{i}" cx="{W * .78 - (W * .78 - W * .2) * f:.0f}" cy="{H * .22 + (H * .8 - H * .22) * f:.0f}" r="{r}" fill="{col}" opacity=".18"/>')
    elif kind == 'aurora':
        for i in range(3):
            y = H * (.12 + i * .08); d = f'M0 {y:.0f} ' + ' '.join(f'Q{W * (j + .5) / 4:.0f} {y + (-40 if j % 2 else 40):.0f} {W * (j + 1) / 4:.0f} {y:.0f}' for j in range(4))
            g.append(f'<path id="{I}p{i}" d="{d}" fill="none" stroke="{"#7cf7b0" if i != 1 else "#8fb8ff"}" stroke-width="{34 - i * 6}" stroke-linecap="round" opacity=".22"/>')
    elif kind == 'ripples':
        for i in range(4):
            g.append(f'<ellipse id="{I}p{i}" cx="{W * (.3 + i * .14):.0f}" cy="{H * (.72 + (i % 2) * .1):.0f}" rx="18" ry="6" fill="none" stroke="{"#dff3ff" if ci else "#5f88a8"}" stroke-width="2.5" opacity="0"/>')
    elif kind == 'waves':
        for i in range(3):
            y = H * (.78 + i * .07); d = f'M{-W:.0f} {y:.0f} ' + ' '.join(f'Q{-W + W * (j + .5) / 4:.0f} {y - 18:.0f} {-W + W * (j + 1) / 4:.0f} {y:.0f}' for j in range(8))
            g.append(f'<path id="{I}p{i}" d="{d}" fill="none" stroke="{"#dff3ff" if ci else "#5f88a8"}" stroke-width="{3.5 - i * .6:.1f}" opacity="{.5 - i * .12:.2f}"/>')
    elif kind == 'rainbow':
        cols = ['#ff5a5a', '#ffb347', '#ffe94a', '#6fd36f', '#5aa9ff', '#9b6bff']
        for i, c in enumerate(cols):
            r = H * .62 - i * 9
            g.append(f'<path id="{I}p{i}" d="M{W / 2 - r:.0f} {H * .95:.0f} A{r:.0f} {r:.0f} 0 0 1 {W / 2 + r:.0f} {H * .95:.0f}" fill="none" stroke="{c}" stroke-width="9" opacity=".45"/>')
    return f'<svg class="ss" id="{I}" viewBox="0 0 {W} {H}">{"".join(g)}</svg>'


def fx_js(nn, kind, v0, t1, H, flash_t=None, W=1920, wind=1, travel=0):
    """tweens for one overlay; all finite, absolute times, seek-safe. One-shot kinds (flash, bolt, shockwave, glitch, starburst, letterbox)
    land at flash_t (the trigger word) or 1 s in; ambient kinds run from the cut to the end."""
    sp = t1 - v0; I = f'fx{nn}'; Q = f'"#{I}"'; one = kind in ('flash', 'bolt', 'shockwave', 'glitch', 'starburst', 'letterbox', 'burst'); ds = dir_sign(kind, wind, travel)
    js = [] if one else [f'tl.fromTo({Q},{{opacity:0}},{{opacity:1,duration:.6,immediateRender:false}},{v0 + .2:.3f});tl.to({Q},{{opacity:0,duration:.4}},{t1 - .45:.3f});']
    if one: js.append(f'tl.set({Q},{{opacity:1}},{v0:.3f});')
    ft = max(flash_t if flash_t is not None else v0 + 1.0, v0 + .4)
    R = lambda d, off=0: max(int((sp - off) / d) - 1, 0)   # repeats so the tween ends by t1 (never past the cut, never negative)
    if kind in PARTICLES:
        P = PARTICLES[kind]
        for i in range(P['n']):
            per = P['per'][0] + (i * .7) % P['per'][1]; fr = (i * .618) % 1; S = f'"#{I}p{i}"'
            dy = P['dy'] * H; dx = P['dx'] * W * ((-1) ** i if kind in ('pollen', 'spores', 'plankton', 'fireflies', 'germs') else ds)
            x0 = -W * .5 * ds if abs(P['dx']) >= 1 else 0   # cross-frame travellers start half a frame behind
            if P['dy'] or P['dx']:   # each piece is already fr of the way along at the cut (no empty sky), then repeats full passes until the cut ends
                op1 = f',opacity:{P["op"] * (1 - fr):.2f}' if P['fade'] else ''; opE = ',opacity:0' if P['fade'] else ''
                rot1 = f',rotation:{P["spin"] * (-1 if i % 2 else 1) * fr:.0f}' if P['spin'] else ''; rotE = f',rotation:{P["spin"] * (-1 if i % 2 else 1)}' if P['spin'] else ''
                ez = "sine.in" if kind == 'bubbles' else "none"; d1 = per * (1 - fr); q = min(1, sp / d1); d1 = d1 * q   # first pass never runs past the cut
                fE = fr + (1 - fr) * q; op1 = op1 if q == 1 else f',opacity:{P["op"] * (1 - fr):.2f}'; opE = opE if q == 1 else f',opacity:{P["op"] * (1 - fE):.2f}'
                rotE = rotE if q == 1 else (f',rotation:{P["spin"] * (-1 if i % 2 else 1) * fE:.0f}' if P['spin'] else '')
                js.append(f'tl.fromTo({S},{{y:{dy * fr:.0f},x:{x0 + dx * fr:.0f}{op1}{rot1},transformOrigin:"50% 50%"}},{{y:{dy * fE:.0f},x:{x0 + dx * fE:.0f}{opE}{rotE},duration:{d1:.2f},ease:"{ez}",immediateRender:false}},{v0:.3f});')
                rem = sp - d1; full = int(rem / per); tail = rem - full * per; opF = ',opacity:0' if P['fade'] else ''; rotF = f',rotation:{P["spin"] * (-1 if i % 2 else 1)}' if P['spin'] else ''
                if full >= 1:   # full passes
                    js.append(f'tl.fromTo({S},{{y:0,x:{x0:.0f},opacity:{P["op"]},rotation:0}},{{y:{dy:.0f},x:{x0 + dx:.0f}{opF}{rotF},duration:{per:.2f},ease:"{ez}",repeat:{full - 1},immediateRender:false}},{v0 + d1:.3f});')
                if tail > per * .25:   # a last partial pass that stops exactly at the cut
                    qt = tail / per; opT = f',opacity:{P["op"] * (1 - qt):.2f}' if P['fade'] else ''; rotT = f',rotation:{P["spin"] * (-1 if i % 2 else 1) * qt:.0f}' if P['spin'] else ''
                    js.append(f'tl.fromTo({S},{{y:0,x:{x0:.0f},opacity:{P["op"]},rotation:0}},{{y:{dy * qt:.0f},x:{x0 + dx * qt:.0f}{opT}{rotT},duration:{tail:.2f},ease:"{ez}",immediateRender:false}},{v0 + d1 + full * per:.3f});')
            if P['sway']:
                sd = 1.2 + (i % 4) * .4
                js.append(f'tl.fromTo({S},{{x:"-={P["sway"]}"}},{{x:"+={P["sway"] * 2}",duration:{sd:.2f},ease:"sine.inOut",yoyo:true,repeat:{R(sd)},immediateRender:false}},{v0:.3f});')
            if P['blink']:
                bd = P['blink'] * (.5 + (i % 3) * .25); bo = (i * .37) % 1.5
                js.append(f'tl.fromTo({S},{{opacity:{P["op"] * .15:.2f}}},{{opacity:{P["op"]},duration:{bd:.2f},ease:"sine.inOut",yoyo:true,repeat:{R(bd, bo)},immediateRender:false}},{v0 + bo:.3f});')
            if kind == 'coins':   # coins flip about their vertical axis (scaleX yoyo), never roll (no rotation)
                co = (i * .13) % .7
                js.append(f'tl.fromTo({S},{{scaleX:1}},{{scaleX:.15,duration:.35,ease:"sine.inOut",yoyo:true,repeat:{R(.35, co)},immediateRender:false}},{v0 + co:.3f});')
    elif kind == 'rain':
        per = .55
        js.append(f'tl.fromTo("#{I} line",{{y:{-H * .25:.0f},x:{-ds * H * .09:.0f}}},{{y:{H * .25:.0f},x:{ds * H * .09:.0f},duration:{per},ease:"none",stagger:{{each:.021,repeat:{R(per, .6)}}},immediateRender:false}},{v0:.3f});')   # drifts with the wind
    elif kind == 'flash':   # one white flash at the word (or 1 s in): fast up, soft down; never over the first 0.4 s
        js.append(f'tl.fromTo("#{I}a",{{opacity:0}},{{opacity:.75,duration:.08,ease:"power1.in",immediateRender:false}},{ft:.3f});tl.to("#{I}a",{{opacity:0,duration:.6,ease:"power2.out"}},{ft + .08:.3f});')
    elif kind == 'bolt':    # the bolt shows twice (0.12 s, gap 0.1 s) with a pale sky flash
        for d in (0, .22):
            js.append(f'tl.fromTo("#{I}a",{{opacity:0}},{{opacity:1,duration:.04,immediateRender:false}},{ft + d:.3f});tl.to("#{I}a",{{opacity:0,duration:.12}},{ft + d + .08:.3f});')
        js.append(f'tl.fromTo("#{I}b",{{opacity:0}},{{opacity:.45,duration:.05,immediateRender:false}},{ft:.3f});tl.to("#{I}b",{{opacity:0,duration:.5}},{ft + .1:.3f});')
    elif kind in ('tint', 'vignette', 'frost'):
        top = {'tint': .22, 'vignette': .7, 'frost': .8}[kind]
        js.append(f'tl.fromTo("#{I}a",{{opacity:0}},{{opacity:{top},duration:1.2,ease:"sine.out",immediateRender:false}},{v0 + .3:.3f});')
    elif kind in ('fog', 'clouds'):   # drift sideways slowly (fog also breathes)
        for i in range(7):
            js.append(f'tl.fromTo("#{I}p{i}",{{x:{-ds * W * .2:.0f}}},{{x:{ds * W * .2:.0f},duration:{sp + .5:.2f},ease:"none",immediateRender:false}},{v0:.3f});')   # fog and clouds drift with the wind
            if kind == 'fog': js.append(f'tl.fromTo("#{I}p{i}",{{opacity:.1}},{{opacity:.22,duration:{2.4 + i * .3:.2f},yoyo:true,repeat:{R(2.8)},ease:"sine.inOut",immediateRender:false}},{v0:.3f});')
    elif kind in ('smoke', 'steam'):  # puffs rise, grow and thin out (AXIS: y up, scale about own centre)
        for i in range(9):
            per = 3 + (i * .5) % 2; off = (i * .618) % 1 * per
            js.append(f'tl.fromTo("#{I}p{i}",{{y:0,scale:.6,opacity:.35,transformOrigin:"50% 50%"}},{{y:{-H * .7:.0f},scale:2.2,opacity:0,duration:{per:.2f},ease:"sine.out",repeat:{R(per, off)},immediateRender:false}},{v0 + off:.3f});')
    elif kind == 'heat':   # shimmer lines wobble sideways and drift up
        for i in range(8):
            js.append(f'tl.fromTo("#{I}p{i}",{{x:-8}},{{x:8,duration:{.5 + (i % 3) * .15:.2f},yoyo:true,repeat:{R(.5 + (i % 3) * .15)},ease:"sine.inOut",immediateRender:false}},{v0:.3f});')
            js.append(f'tl.fromTo("#{I}p{i}",{{y:0}},{{y:{-H * .12:.0f},duration:{3 + (i % 4) * .5:.2f},repeat:{R(3 + (i % 4) * .5)},ease:"none",immediateRender:false}},{v0:.3f});')
    elif kind == 'rays':   # the fan of rays rotates slowly about its apex (AXIS: the sun corner) and breathes
        js.append(f'tl.fromTo("#{I}r",{{rotation:-3,svgOrigin:"{W * .85:.0f} {-H * .1:.0f}"}},{{rotation:3,duration:{max(sp, 4):.2f},ease:"sine.inOut",immediateRender:false}},{v0:.3f});')
        js.append(f'tl.fromTo("#{I} polygon",{{opacity:.05}},{{opacity:.12,duration:1.6,yoyo:true,stagger:{{each:.12,repeat:{R(1.6, 1.5)},yoyo:true}},ease:"sine.inOut",immediateRender:false}},{v0:.3f});')
    elif kind == 'searchlight':   # one beam sweeps left-right about its base at the bottom (AXIS: bottom centre)
        js.append(f'tl.fromTo("#{I}p0",{{rotation:-35,svgOrigin:"{W * .5:.0f} {H * 1.15:.0f}"}},{{rotation:35,duration:3.2,yoyo:true,repeat:{R(3.2)},ease:"sine.inOut",immediateRender:false}},{v0:.3f});')
    elif kind == 'spotlight':
        js.append(f'tl.fromTo("#{I}a",{{opacity:0}},{{opacity:1,duration:1,immediateRender:false}},{v0 + .3:.3f});tl.fromTo("#{I}b",{{rotation:-6,svgOrigin:"{W * .5:.0f} {-H * .2:.0f}"}},{{rotation:6,duration:2.6,yoyo:true,repeat:{R(2.6)},ease:"sine.inOut",immediateRender:false}},{v0:.3f});')
    elif kind == 'starburst':  # rays burst out from the centre once at the word, spin a little, and fade
        js.append(f'tl.fromTo("#{I}r",{{scale:0,opacity:1,svgOrigin:"{W * .5:.0f} {H * .5:.0f}"}},{{scale:1,opacity:0,rotation:25,duration:1.1,ease:"power2.out",immediateRender:false}},{ft:.3f});')
    elif kind == 'windlines':   # streaks fly left-to-right, staggered (AXIS: horizontal)
        per = 1.1
        js.append(f'tl.fromTo("#{I} line",{{x:0}},{{x:{W * 1.4:.0f},duration:{per},ease:"power1.in",stagger:{{each:.09,repeat:{R(per, 1.1)}}},immediateRender:false}},{v0:.3f});')
    elif kind == 'shockwave':   # one ring expands from the centre at the word (AXIS: frame centre)
        js.append(f'tl.fromTo("#{I}a",{{scale:.2,opacity:.8,svgOrigin:"{W * .5:.0f} {H * .5:.0f}"}},{{scale:{W / 60:.1f},opacity:0,duration:.9,ease:"power2.out",immediateRender:false}},{ft:.3f});')
        js.append(f'tl.fromTo("#t{nn}",{{x:0}},{{x:8,duration:.05,yoyo:true,repeat:7,immediateRender:false}},{ft:.3f});')
    elif kind == 'burst':   # pieces fly out with gravity (Physics2DPlugin) at the word; a quick ring marks the moment
        js.append(f'tl.fromTo("#{I}a",{{scale:.3,opacity:.9,svgOrigin:"{W * .5:.0f} {H * .5:.0f}"}},{{scale:9,opacity:0,duration:.7,ease:"power2.out",immediateRender:false}},{ft:.3f});')
        for i in range(72):
            v = 380 + ((i * .618) % 1) * 820; ang = -150 + ((i * .382) % 1) * 120; rot = ((i * 137) % 720) - 360
            dl = ((i * .236) % 1) * .28   # staggered launch: a cloud, not one ring
            js.append(f'tl.set("#{I}p{i}",{{opacity:0}},{v0:.3f});tl.fromTo("#{I}p{i}",{{x:0,y:0,rotation:0,opacity:1}},{{duration:2.6,physics2D:{{velocity:{v:.0f},angle:{ang:.0f},gravity:1500,friction:.03}},rotation:{rot},ease:"none",immediateRender:false}},{ft + dl:.3f});'
                      f'tl.to("#{I}p{i}",{{opacity:0,duration:.9,ease:"power1.in",immediateRender:false}},{ft + dl + 1.7:.3f});')   # pieces stay bright while they fly, fade as they fall out
    elif kind == 'letterbox':   # black bars slide in from top and bottom over 0.6 s and stay
        js.append(f'tl.fromTo("#{I}a",{{y:0}},{{y:{H * .11:.0f},duration:.6,ease:"power2.out",immediateRender:false}},{v0 + .2:.3f});tl.fromTo("#{I}b",{{y:0}},{{y:{-H * .11:.0f},duration:.6,ease:"power2.out",immediateRender:false}},{v0 + .2:.3f});')
    elif kind == 'scanlines':   # a faint line pattern that rolls down slowly
        js.append(f'tl.fromTo("#{I}a",{{y:-4}},{{y:0,duration:.4,ease:"none",repeat:{R(.4)},immediateRender:false}},{v0:.3f});')
    elif kind == 'glitch':   # coloured bars jump in for 0.4 s at the word (two bursts)
        for d in (0, .9):
            for i in range(5):
                js.append(f'tl.fromTo("#{I}p{i}",{{opacity:0,x:{(-1) ** i * 30}}},{{opacity:.55,x:{(-1) ** (i + 1) * 30},duration:.07,yoyo:true,repeat:3,immediateRender:false}},{ft + d + i * .03:.3f});')
            js.append(f'tl.fromTo("#t{nn}",{{x:0}},{{x:-10,duration:.06,yoyo:true,repeat:5,immediateRender:false}},{ft + d:.3f});')
    elif kind == 'lightleak':   # the warm blob drifts slowly and breathes
        js.append(f'tl.fromTo("#{I}a",{{x:0,opacity:.6}},{{x:{-W * .15:.0f},opacity:1,duration:{max(sp, 4):.2f},ease:"sine.inOut",immediateRender:false}},{v0:.3f});')
    elif kind == 'flare':   # the flare pulses; its ghost circles slide along the diagonal
        js.append(f'tl.fromTo("#{I}a",{{opacity:.7,scale:.95,transformOrigin:"50% 50%"}},{{opacity:1,scale:1.05,duration:1.4,yoyo:true,repeat:{R(1.4)},ease:"sine.inOut",immediateRender:false}},{v0:.3f});')
        for i in range(4): js.append(f'tl.fromTo("#{I}p{i}",{{x:-14,y:14}},{{x:14,y:-14,duration:{max(sp, 4):.2f},ease:"sine.inOut",immediateRender:false}},{v0:.3f});')
    elif kind == 'aurora':   # bands wave sideways and shimmer
        for i in range(3):
            js.append(f'tl.fromTo("#{I}p{i}",{{x:{-30 - i * 10}}},{{x:{30 + i * 10},duration:{4 + i:.2f},yoyo:true,repeat:{R(4 + i)},ease:"sine.inOut",immediateRender:false}},{v0:.3f});')
            js.append(f'tl.fromTo("#{I}p{i}",{{opacity:.12}},{{opacity:.3,duration:{2.2 + i * .4:.2f},yoyo:true,repeat:{R(2.2 + i * .4, i * .5)},ease:"sine.inOut",immediateRender:false}},{v0 + i * .5:.3f});')
    elif kind == 'ripples':   # rings expand from their own centre and fade, one after another (AXIS: each ring's centre)
        for i in range(4):
            per = 2.4; off = i * .6
            js.append(f'tl.fromTo("#{I}p{i}",{{scale:.2,opacity:.7,transformOrigin:"50% 50%"}},{{scale:4,opacity:0,duration:{per},ease:"power1.out",repeat:{R(per, off)},immediateRender:false}},{v0 + off:.3f});')
    elif kind == 'waves':   # wave lines scroll right (seamless: path is two frame-widths long)
        for i in range(3):
            per = 4 + i * 1.2
            js.append(f'tl.fromTo("#{I}p{i}",{{x:0}},{{x:{W * .5:.0f},duration:{per:.2f},ease:"none",repeat:{R(per)},immediateRender:false}},{v0:.3f});')
    elif kind == 'rainbow':   # the arc draws in from the left (scaleX about the left foot) then holds
        js.append(f'tl.fromTo("#{I} path",{{scaleX:0,svgOrigin:"{W * .5 - H * .62:.0f} {H * .95:.0f}"}},{{scaleX:1,duration:1.4,stagger:.08,ease:"power2.out",immediateRender:false}},{v0 + .4:.3f});')
    return js


# ---- text effects (round 4, 2026-10-26): on-screen text only, never the subtitles (guideline 5) ----
def chalk_title_html(title):
    """the chalk title as one <i> per character so it can be written on (spaces kept)"""
    import html as _h
    return ''.join(f'<i>{_h.escape(c)}</i>' if c != ' ' else ' ' for c in title)


def chalk_title_js(i, t0):
    """letters appear one by one like chalk writing (0.035 s each, from t0 + 0.1), the subtitle fades in after"""
    return [f'tl.fromTo("#k{i} .ct i",{{opacity:0,y:4}},{{opacity:1,y:0,duration:.08,stagger:.035,ease:"power1.out",immediateRender:false}},{t0 + .1:.3f});',
            f'tl.fromTo("#k{i} .cs",{{opacity:0}},{{opacity:1,duration:.4,immediateRender:false}},{t0 + .9:.3f});']


def chalk_concl_js(i, tc):
    """a chalk underline draws under the conclusion 0.3 s after it pops (scaleX 0 -> 1 from the left)"""
    return [f'tl.fromTo("#k{i}ul",{{scaleX:0,opacity:1,transformOrigin:"0% 50%"}},{{scaleX:1,duration:.45,ease:"power2.out",immediateRender:false}},{tc + .3:.3f});']


def badge_bounce_js(lid, tt):
    """number badge: a small bounce when the count-up lands (0.9 s after it comes in)"""
    return [f'tl.fromTo("#{lid}",{{scale:1,transformOrigin:"0% 50%"}},{{scale:1.08,duration:.14,ease:"power2.out",yoyo:true,repeat:1,immediateRender:false}},{tt + .9:.3f});']


MOTION_JS = """
function miyaEase(x){return x<.5?4*x*x*x:1-Math.pow(-2*x+2,3)/2;}
// travelling motion (path object, tracking camera): constant speed with short 15 % soft start/stop (no mid-way speed-up, owner 2026-10-22)
function miyaCruise(x){var r=.15,v=1/(1-r);return x<r?v*x*x/(2*r):x>1-r?1-v*(1-x)*(1-x)/(2*r):v*(r/2+x-r);}
function miyaClamp(x){return Math.min(1,Math.max(0,x));}
// children of group `g` appear one by one (or are recoloured to `fill`), `step` s apart, from time `st`; `n` limits how many
function miyaTicks(tl,g,v0,st,step,fill,n){
 var kids=Array.prototype.slice.call(g.children).slice(0,n);
 kids.forEach(function(c,i){
  if(fill){tl.set(c,{fill:fill},st+i*step);}else{tl.set(c,{opacity:0},v0);tl.set(c,{opacity:1},st+i*step);}
 });
}
// rack focus without an SVG filter: six ghost copies on a circle of radius r*(1-k) around the group; k 0..1 is the sharpness
// (dir 1: soft -> sharp, dir 0: sharp -> soft). The original gets less opaque while soft. Seek-safe: a modifier writes the state.
function miyaRack(tl,g,v0,st,du,r,dir){
 var N=6,ghosts=[],o={k:0};
 for(var i=0;i<N;i++){var c=g.cloneNode(true);c.setAttribute('class','mvc');c.removeAttribute('id');Array.prototype.forEach.call(c.querySelectorAll('[class*=mv]'),function(n){n.setAttribute('class','mvc');});g.parentNode.insertBefore(c,g);ghosts.push(c);}
 function ap(k){var s=dir?k:1-k,rr=r*(1-s);
  ghosts.forEach(function(c,i){var a=i/N*Math.PI*2;c.setAttribute('transform','translate('+(Math.cos(a)*rr).toFixed(2)+' '+(Math.sin(a)*rr).toFixed(2)+')');c.setAttribute('opacity',rr>.4?.17:0);});
  g.style.opacity=rr>.4?(.55+.45*s):1;}
 ap(0);
 tl.to(o,{k:1,duration:du,ease:'power2.inOut',immediateRender:false,modifiers:{k:function(v){ap(v);return v;}}},st);
}
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
// (2026-10-25) GSAP svgOrigin and x/y live in the PARENT group's coordinate space, not in the picture's. data-pivot / path coordinates are picture (root svg) coordinates,
// so a link inside a translated/scaled wrapper rotated about a point far from its joint (whale tails and fins came off the body). miyaM = picture -> parent-local matrix.
// a name label / speech bubble whose target point sits on a MOVING group follows that group (miya 2026-10-27: labels stayed at the pre-motion spot).
// Seek-safe: a modifier tween reads the group's current matrix on every render (callbacks are skipped by seek, modifiers are not); the reference
// matrix is read once at page init, before any motion is applied (units are hidden then, so the unit is shown invisibly for the read).
function miyaFollow(tl,gsel,els,px,py,t0,t1,tm){var g=document.querySelector(gsel);if(!g||!g.ownerSVGElement)return;var svg=g.ownerSVGElement,p=svg.createSVGPoint();p.x=px;p.y=py;
 var tg=els.map(function(s){return document.querySelector(s);}).filter(Boolean);if(!tg.length)return;
 var rec={g:g,p:p,q0:null,t:t0,tm:(tm==null?t0:tm),last:[0,0],tg:tg};/* tm = when the object still stands where it was DRAWN (picture start): the label's pointer was authored against that spot, so the offset is measured from there */window.MIYA_FOLLOW=window.MIYA_FOLLOW||[];window.MIYA_FOLLOW.push(rec);
 function d(){if(!rec.q0)return[0,0];var m=miyaCtm(g);if(!m)return rec.last;var q=p.matrixTransform(m);rec.last=[q.x-rec.q0.x,q.y-rec.q0.y];return rec.last;}
 tl.fromTo(tg,{x:0.001,y:0.001},{x:0,y:0,duration:Math.max(t1-t0,.1),ease:'none',immediateRender:false,modifiers:{x:function(){return d()[0]+'px';},y:function(){return d()[1]+'px';}}},t0);}
function miyaCtm(g){var t=g.closest('.t'),m=null;if(t&&t.style.display==='none'){var pd=t.style.display,pv=t.style.visibility;t.style.display='block';t.style.visibility='hidden';try{m=g.getCTM();}catch(e){}t.style.display=pd;t.style.visibility=pv;}else{try{m=g.getCTM();}catch(e){}}return m;}
// after the whole timeline exists: the tracked point (the group's centre) and its position are read AT THE LABEL'S START TIME (GSAP replaces a group's own transform
// attribute, so the matrix at page init is not the one the label was placed against); then the timeline goes back to 0
function miyaFollowInit(tl){var L=window.MIYA_FOLLOW||[];if(!L.length)return;L.slice().sort(function(a,b){return a.tm-b.tm;}).forEach(function(r){void tl.seek(r.tm+0.05,false);try{var bb=r.g.getBBox();if(bb&&bb.width){r.p.x=bb.x+bb.width/2;r.p.y=bb.y+bb.height/2;}}catch(e){}var m=miyaCtm(r.g);if(m)r.q0=r.p.matrixTransform(m);});void tl.seek(0,false);   // 2026-10-29: the measuring seeks must go FORWARD in time only. A seek backwards renders the children in reverse order, so a picture's `display:none` (its end) was applied before its tweens had initialised: GSAP then read the empty bbox of the hidden picture and froze the wrong svgOrigin (bbox corner) of every hinge/rotor that had not been initialised yet (windmill, gears, frog legs, tails, neck, clock hand). tools/pivotlive.py checks it
 // render order inside one seek can leave the follower one step behind its object: after every seek (the renderer steps frame by frame with seek) the followers are set again from the objects' final matrices
 function fix(){L.forEach(function(r){if(!r.q0||!r.tg)return;var m=miyaCtm(r.g);if(!m)return;var q=r.p.matrixTransform(m);gsap.set(r.tg,{x:q.x-r.q0.x,y:q.y-r.q0.y});});}
 var seek0=tl.seek;tl.seek=function(a,b){var out=seek0.call(tl,a,b);fix();return out;};var time0=tl.time;tl.time=function(a,b){var out=time0.call(tl,a,b);if(arguments.length)fix();return out;};gsap.ticker.add(function(){if(tl.isActive())fix();});}   // the tracked point = the group's own centre (local bbox), so a turning object does not swing the label about a far pivot
function miyaM(g){var pa=g.parentNode,t=g.closest('.t'),pd=t?t.style.display:'',pv=t?t.style.visibility:'',m=null;if(t){t.style.display='block';t.style.visibility='hidden';}
 try{m=pa.getCTM();}catch(e){}if(t){t.style.display=pd;t.style.visibility=pv;}return m?m.inverse():null;}
// data-pivot is meant in picture coordinates, but agents often wrote it in the coordinates the part was drawn in (inside a translated/scaled wrapper): use whichever reading lands nearer the part itself
function miyaPv(g,x,y){var m=miyaM(g);if(!m)return x+' '+y;var cx=m.a*x+m.c*y+m.e,cy=m.b*x+m.d*y+m.f,b=null,t=g.closest('.t'),pd=t?t.style.display:'',pv=t?t.style.visibility:'';
 if(t){t.style.display='block';t.style.visibility='hidden';}try{b=g.getBBox();}catch(e){}if(t){t.style.display=pd;t.style.visibility=pv;}
 if(b&&b.width+b.height>0){function dd(u,v){return Math.hypot(Math.max(b.x-u,0,u-b.x-b.width),Math.max(b.y-v,0,v-b.y-b.height));}if(dd(x,y)+4<dd(cx,cy))return x+' '+y;}
 return cx+' '+cy;}
// object follows an SVG path, turning with it (paper plane, rocket)
function miyaPath(tl,g,d,t0,dur,rot,rot0,ez){
 var t=g.closest('.t'),pd=t.style.display,pv=t.style.visibility;t.style.display='block';t.style.visibility='hidden';
 var NS='http://www.w3.org/2000/svg',svg=g.ownerSVGElement,p=document.createElementNS(NS,'path');p.setAttribute('d',d);p.setAttribute('visibility','hidden');svg.appendChild(p);
 var L=p.getTotalLength(),P0=p.getPointAtLength(0),o={k:0};
 function ang(k){var s0=Math.max(0,Math.min(L-2,L*k)),a=p.getPointAtLength(s0),b=p.getPointAtLength(Math.min(L,s0+2));return Math.atan2(b.y-a.y,b.x-a.x)*180/Math.PI;}
 var a0=ang(0);t.style.display=pd;t.style.visibility=pv;
 var M=miyaM(g),O=miyaPv(g,P0.x,P0.y);if(O==P0.x+' '+P0.y)M=null;gsap.set(g,{svgOrigin:O});   // origin set once: re-setting it every frame made turning objects drift
 function ap(k){var q=p.getPointAtLength(L*k),dx=q.x-P0.x,dy=q.y-P0.y;if(M){var ex=M.a*dx+M.c*dy,ey=M.b*dx+M.d*dy;dx=ex;dy=ey;}gsap.set(g,{x:dx,y:dy,rotation:rot?ang(k)-a0+(rot0||0):0});}
 tl.to(o,{k:1,duration:dur,ease:ez||miyaCruise,immediateRender:false,modifiers:{k:function(v){ap(v);return v;}}},t0);
}
// camera tracking: the camera centre follows an SVG path (same window and ease as the object), zooming in at the start and out at the end
function miyaTrack(tl,wsel,d,t0,dur,sc,W,H,ease,WW,WH){
 WW=WW||W;WH=WH||H;   // W,H = the screen, WW,WH = the picture (a `world` picture is bigger than the screen)
 var w=document.querySelector(wsel),t=w.closest('.t'),pd=t.style.display,pv=t.style.visibility;t.style.display='block';t.style.visibility='hidden';
 var NS='http://www.w3.org/2000/svg',svg=w.querySelector('svg'),p=document.createElementNS(NS,'path');p.setAttribute('d',d);p.setAttribute('visibility','hidden');svg.appendChild(p);
 var L=p.getTotalLength(),o={k:0};t.style.display=pd;t.style.visibility=pv;
 function ap(k){var q=p.getPointAtLength(L*k),r=Math.min(1,k/.12,(1-k)/.12),s=1+(sc-1)*r*r*(3-2*r);
  var cx=Math.min(Math.max(q.x,W/2/s),WW-W/2/s),cy=Math.min(Math.max(q.y,H/2/s),WH-H/2/s);
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
""" + fxlib.LIB_JS
