# -*- coding: utf-8 -*-
# Open-source effect libraries wired into the build (miya 2026-10-29, guideline 4-6): GSAP 3.15 plugins (all free since 3.13),
# anime.js 4 (springs + grid stagger, driven from the GSAP timeline so every frame stays seekable), lucide pictograms (2,193 ISC icons,
# svgo-minified into tools/assets/lucide.json) and an optional svgo pass over the art (tools/svg_opt.py).
# Everything here is chosen by code rules (script words > picture evidence > unit number), never by a model at build time.
import json, os, re
from collections import Counter
LOG = Counter()   # what the library rules chose in this build (printed by build3)

ASSETS = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets')
PLUGINS = ['DrawSVGPlugin', 'MorphSVGPlugin', 'MotionPathPlugin', 'SplitText', 'ScrambleTextPlugin', 'Physics2DPlugin', 'PhysicsPropsPlugin',
           'InertiaPlugin', 'CustomEase', 'CustomWiggle', 'CustomBounce', 'EasePack', 'Flip', 'TextPlugin']
# EasePack registers SlowMo / RoughEase / ExpoScaleEase under the names "slow(...)", "rough(...)", "expoScale(...)"
COPY = ['gsap.min.js', 'anime.min.js'] + [f'gsap/{p}.min.js' for p in PLUGINS]


def script_tags():
    return '<script src="gsap.min.js"></script>' + ''.join(f'<script src="gsap/{p}.min.js"></script>' for p in PLUGINS) + '<script src="anime.min.js"></script>'


# registered once at the top of the timeline script: plugins + the named eases every rule below refers to
REGISTER_JS = (
    'gsap.registerPlugin(' + ','.join(PLUGINS) + ');'
    'CustomWiggle.create("miyaWig",{wiggles:8,type:"easeOut"});'          # a hit that calms down (shake / tremble / rattle)
    'CustomWiggle.create("miyaWigU",{wiggles:10,type:"uniform"});'        # steady shiver (cold, fear)
    'CustomWiggle.create("miyaWigA",{wiggles:5,type:"anticipate"});'      # winds up then lets go (a stamp, a slam)
    'CustomWiggle.create("miyaWigR",{wiggles:12,type:"random"});'         # nervous jitter (earthquake, engine)
    'CustomBounce.create("miyaBnc",{strength:.6,squash:3});'              # real bounce + "miyaBnc-squash" for scaleX/scaleY
    'CustomBounce.create("miyaBncS",{strength:.4,squash:2});'             # softer landing
)

# ---- JS helpers appended to motions.MOTION_JS ----
LIB_JS = r"""
// anime.js timelines are never played: a GSAP proxy tween seeks them (modifiers run on tl.seek(t,false)), so chunked / seeked renders stay exact
function miyaAnime(tl,a,t0,L){var p={v:0};tl.fromTo(p,{v:0},{v:L,duration:L,ease:'none',immediateRender:false,modifiers:{v:function(x){a.seek(x*1000,true);return x;}}},t0);}
// anime spring as a GSAP ease: returns {ease, dur} (seconds) for the given stiffness / damping
function miyaSpring(k,d){var s=anime.spring({mass:1,stiffness:k,damping:d});return {ease:s.ease,dur:Math.max(.35,Math.min(2.4,s.duration/1000))};}
function miyaSpringTo(tl,el,from,to,k,d,at){var s=miyaSpring(k,d);to.duration=s.dur;to.ease=s.ease;to.immediateRender=false;tl.fromTo(el,from,to,at);}
// morph: the group's first path becomes the d of its last path (drawn by the artist with opacity 0), optionally back again
function miyaMorph(tl,g,st,du,back){var ps=g.querySelectorAll('path');if(ps.length<2)return;var a=ps[0],b=ps[ps.length-1];b.style.display='none';var d0=a.getAttribute('d');
 tl.to(a,{morphSVG:{shape:b,shapeIndex:'auto'},duration:du,ease:'power2.inOut'},st);if(back)tl.to(a,{morphSVG:{shape:d0,shapeIndex:'auto'},duration:du,ease:'power2.inOut'},st+du+.6);}
// regroup (Flip): the group's direct children move from where they were drawn into a ring / line / grid around the group's centre
function miyaRegroup(tl,g,shape,st,du,stag){var t=g.closest('.t'),pd=t?t.style.display:'',pv=t?t.style.visibility:'';if(t){t.style.display='block';t.style.visibility='hidden';}
 var kids=Array.prototype.filter.call(g.children,function(e){return e.tagName!=='defs';}),n=kids.length;if(n<2){if(t){t.style.display=pd;t.style.visibility=pv;}return;}
 var bb=g.getBBox(),cx=bb.x+bb.width/2,cy=bb.y+bb.height/2,R=Math.max(bb.width,bb.height)/2,tg=[];
 kids.forEach(function(e,i){var b=e.getBBox(),ex=b.x+b.width/2,ey=b.y+b.height/2,x,y;
  if(shape==='line'){x=bb.x+bb.width*(i+.5)/n;y=cy;}else if(shape==='grid'){var c=Math.ceil(Math.sqrt(n)),r=Math.ceil(n/c);x=bb.x+bb.width*((i%c)+.5)/c;y=bb.y+bb.height*(Math.floor(i/c)+.5)/r;}
  else{var a=-Math.PI/2+i/n*Math.PI*2;x=cx+Math.cos(a)*R;y=cy+Math.sin(a)*R*.8;}tg.push([x-ex,y-ey]);});
 var state=Flip.getState(kids);kids.forEach(function(e,i){gsap.set(e,{x:tg[i][0],y:tg[i][1]});});
 var f=Flip.from(state,{duration:du,ease:'power2.inOut',stagger:stag,simple:true});if(t){t.style.display=pd;t.style.visibility=pv;}tl.add(f,st);}
// pictogram strokes draw in (lucide icon beside a label / badge)
function miyaIconDraw(tl,sel,at){var ps=gsap.utils.toArray(sel+' path,'+sel+' circle,'+sel+' line,'+sel+' polyline,'+sel+' rect,'+sel+' ellipse');if(!ps.length)return;
 tl.fromTo(ps,{drawSVG:'0%'},{drawSVG:'100%',duration:.55,ease:'power1.inOut',stagger:.06,immediateRender:false},at);}
"""

# ---- word rules (unit text) ----
_c = lambda p: re.compile(p, re.I)
SCRAMBLE_W = _c(r'\b(secret\w*|code[sd]?|decod\w*|cipher\w*|encrypt\w*|decrypt\w*|myster\w*|unknown|riddle\w*|puzzl\w*|random\w*|signal\w*|hidden|classified|scrambl\w*|glitch\w*|static)\b')
TYPE_W = _c(r'\b(typ(e|ed|ing)|typewriter|letter\w*|telegra\w*|telegraph\w*|wrote|writ(e|es|ing|ten)|diary|diaries|journal\w*|manuscript\w*|memo\w*|note(s|book)?|report(s|ed)?|transcript\w*|printed|press release)\b')
SPEED_W = _c(r'\b(rush\w*|dash\w*|sprint\w*|rac(e|es|ed|ing)|speed\w*|fast(er|est)?|quick\w*|zoom\w*|hurtl\w*|accelerat\w*|rapid\w*|swift\w*|velocity|supersonic|hypersonic|light ?speed)\b')
ROUGH_W = _c(r'\b(earthquake\w*|tremor\w*|turbulen\w*|bump\w*|rough|chaotic|chaos|shak(e|es|ing|y)|rattl\w*|jolt\w*|rumbl\w*|quak\w*|vibrat\w*|engine\w*|storm\w*)\b')
PLAYFUL_W = _c(r'\b(bounc\w*|spring\w*|hop(s|ped|ping)?|jump\w*|boing|playful\w*|excit\w*|cheer\w*|jolly|giggl\w*|wobbl\w*|plop\w*|land(s|ed|ing)?)\b')
SERIOUS_W = _c(r'\b(death\w*|died|dying|dead|kill\w*|murder\w*|grave\w*|funeral\w*|mourn\w*|extinct\w*|tragic\w*|tragedy|starv\w*|famine|genocide|massacre|war\b|wars\b|victim\w*|cannibal\w*)\b')
WIGGLE_W = _c(r'\b(shak(e|es|ing|en)|trembl\w*|shiver\w*|quiver\w*|rattl\w*|wobbl\w*|jitter\w*|vibrat\w*|nervous\w*|buzz\w*|jiggl\w*|flutter\w*)\b')
BOUNCE_W = _c(r'\b(drop\w*|fall(s|ing)?|fell|land(s|ed|ing)?|bounc\w*|plummet\w*|tumbl\w*|crash\w* down|hit the (ground|floor)|thud\w*|plop\w*)\b')
ZOOM_W = _c(r'\b(zoom\w*|closer|close-?up|magnif\w*|microscop\w*|telescop\w*|look (inside|closer)|tiny|minuscule|microscopic|vast|enormous|gigantic|immense)\b')


def path_ease(text):
    """ease for a travelling object (mv-path): a speed word -> SlowMo ramp (slow in, linear rush, slow out), else the usual cruise"""
    return 'slow(0.35,0.75,false)' if SPEED_W.search(text) else None


def cam_ease(text):
    """drift / focus camera ease: an earthquake / rough word -> RoughEase jitter on top of the move; a zoom word -> ExpoScaleEase"""
    if ROUGH_W.search(text): return 'rough({strength:1,points:24,template:"sine.inOut",taper:"both",randomize:true,clamp:true})'
    return None


def spring_params(text, k):
    """springy entrances (anime.spring) only when the sentence is playful and not grim; the unit number picks soft / medium / stiff"""
    if SERIOUS_W.search(text) or not PLAYFUL_W.search(text): return None
    return [(70, 8), (140, 11), (260, 15)][k % 3]


def wiggle_ease(text):
    if re.search(r'\b(cold|freez\w*|shiver\w*|fear\w*|afraid|terrif\w*|scared)\b', text, re.I): return 'miyaWigU'
    if ROUGH_W.search(text): return 'miyaWigR'
    return 'miyaWig'


# ---- lucide pictograms ----
_ICONS = None; _TAGS = None
# only picture-like icons: a single word name (no -off / -check / -cog variants) that is not a UI word, plus a few two-word ones
UI_BLOCK = _c(r'^(text|type|list|menu|code|link|grid|layout|panel|table|rows|columns|box|boxes|square|circle|triangle|hexagon|octagon|pentagon|diamond|'
              r'component|container|frame|group|ungroup|tag|tags|hash|percent|plus|minus|equal|divide|asterisk|slash|check|ban|info|option|command|'
              r'variable|function|binary|braces|brackets|parentheses|regex|terminal|cpu|server|database|cookie|bug|dot|ellipsis|more|move|maximize|'
              r'minimize|expand|shrink|fullscreen|focus|scan|crop|pointer|cursor|mouse|touchpad|keyboard|monitor|laptop|tablet|smartphone|phone|'
              r'watch|wifi|bluetooth|usb|cast|airplay|signal|rss|share|forward|reply|undo|redo|repeat|shuffle|play|pause|square|rewind|skip|volume|'
              r'mic|video|image|images|file|files|folder|folders|archive|inbox|mail|send|bookmark|pin|pen|pencil|eraser|highlighter|brush|palette|'
              r'pipette|ruler|spline|vector|pentool|type|heading|bold|italic|underline|strikethrough|subscript|superscript|quote|indent|outdent|'
              r'wrap|unlink|anchor|at|sign|badge|award|star|shield|lock|unlock|key|eye|bell|user|users|contact|settings|sliders|toggle|filter|'
              r'funnel|search|zoom|download|upload|import|export|save|trash|delete|copy|clipboard|paste|scissors|printer|qr|barcode|calendar|'
              r'clock|timer|hourglass|alarm|history|activity|gauge|chart|trending|kanban|workflow|route|map|navigation|compass|locate|'
              r'home|house|building|store|shop|cart|basket|receipt|wallet|credit|banknote|coins|bitcoin|euro|dollar|pound|yen|gem|crown|'
              r'languages|globe|earth|flag|milestone|goal|target|crosshair|radar|radio|podcast|music|disc|cassette|film|clapperboard|tv|'
              r'projector|camera|aperture|webcam|lamp|lightbulb|flashlight|candle|plug|power|battery|zap|bolt|fuel|car|bus|truck|train|'
              r'tram|plane|rocket|ship|sailboat|bike|footprints|accessibility|baby|dog|cat|bird|fish|rabbit|rat|turtle|snail|squirrel|panda|'
              r'bone|skull|ghost|heart|brain|ear|hand|eye|dna|atom|flask|microscope|telescope|magnet|pill|syringe|stethoscope|thermometer|'
              r'bandage|ambulance|hospital|cross|church|landmark|castle|tent|mountain|trees|tree|leaf|flower|sprout|wheat|apple|banana|'
              r'cherry|grape|citrus|carrot|egg|milk|coffee|wine|beer|pizza|cake|candy|cookie|croissant|donut|hamburger|sandwich|soup|salad|'
              r'utensils|cloud|cloudy|sun|moon|sunrise|sunset|rainbow|snowflake|wind|waves|droplet|droplets|flame|tornado|haze|umbrella|'
              r'thermometer|anvil|hammer|wrench|pickaxe|axe|shovel|drill|saw|cog|gear|bolt|nut|chain|rope|feather|origami|puzzle|dice|'
              r'gamepad|joystick|trophy|medal|swords|sword|bomb|crosshair|drum|guitar|piano|book|library|newspaper|scroll|notebook|graduation|'
              r'school|backpack|briefcase|luggage|shirt|glasses|watch|gift|party|balloon|cigarette|tooth|biohazard|radiation|recycle|'
              r'infinity|omega|sigma|pi|percent|binary|bath|bed|sofa|armchair|lamp|door|fence|warehouse|factory|tractor|caravan|'
              r'lighthouse|ferris|roller|tent|campfire|sailboat|anchor|shell|fishing|bug|worm|spider|snail|butterfly)$')
PICT_ALLOW = _c(r'^(anchor|apple|atom|axe|baby|banana|bell|bike|biohazard|bird|bomb|bone|book|brain|bug|cake|calendar|camera|candy|car|carrot|castle|cat|'
                r'cherry|church|citrus|clock|cloud|coffee|cog|coins|compass|crown|dna|dog|donut|drum|droplet|droplets|ear|earth|egg|eye|factory|feather|'
                r'film|fish|flag|flame|flask-conical|flower|footprints|gem|ghost|globe|grape|guitar|hammer|hand|heart|hospital|hourglass|house|'
                r'key|landmark|leaf|lightbulb|lighthouse|lock|magnet|map|medal|microscope|milk|moon|mountain|origami|panda|pickaxe|piano|pill|'
                r'pizza|plane|rabbit|radiation|rainbow|rat|rocket|sailboat|scissors|scroll|shell|ship|shield|skull|snail|snowflake|squirrel|star|'
                r'stethoscope|sun|sunrise|sunset|sword|swords|syringe|telescope|tent|thermometer|tornado|tractor|train|tree-pine|tree-palm|trees|'
                r'trophy|turtle|umbrella|utensils|waves|wheat|wind|worm|wrench|cloud-rain|cloud-snow|cloud-lightning|cloud-fog|cooking-pot|'
                r'egg-fried|fish-symbol|hand-fist|heart-pulse|map-pin|bird|bus|truck|wine|beer|dice-5|puzzle|gamepad-2|infinity|crosshair|'
                r'candle|anvil|shovel|drill|saw|tooth|glasses|shirt|gift|bath|bed|sofa|door-open|fence|warehouse|campfire|spider|butterfly|'
                r'satellite|satellite-dish|radar|radio|binoculars|orbit|planet|volcano|dinosaur|footprints|cctv|alarm-clock|calendar-days|'
                r'thermometer-sun|thermometer-snowflake|snowflake|sun-snow|cloud-sun|moon-star|sparkles|zap|flame-kindling|droplet|waves-ladder|'
                r'fish-off|siren|ambulance|school|graduation-cap|backpack|briefcase|luggage|newspaper|library|notebook|pen-tool|paintbrush|palette|'
                r'ruler|scale|balance|gavel|handshake|hand-coins|banknote|wallet|credit-card|bitcoin|receipt|shopping-cart|store|package|'
                r'box|container|cylinder|test-tube|test-tubes|beaker|dna-off|microchip|cpu|battery|plug|lamp|lamp-desk|flashlight|'
                r'projector|tv|monitor|smartphone|phone|printer|keyboard|mouse|headphones|speaker|mic|music|disc|cassette-tape|clapperboard|'
                r'ticket|popcorn|ice-cream-cone|lollipop|cookie|sandwich|hamburger|soup|salad|utensils-crossed|chef-hat|cup-soda|bottle-wine|'
                r'martini|grape|nut|leafy-green|sprout|clover|cactus|palmtree|shrub|flower-2|trees|tree-deciduous|bird|egg|feather|shell|'
                r'squirrel|turtle|snail|rabbit|rat|cat|dog|panda|bug|worm|paw-print|bone|skull|ghost|baby|person-standing|accessibility|'
                r'footprints|hand|hand-metal|thumbs-up|thumbs-down|eye|ear|brain|heart|lungs|stethoscope|syringe|pill|bandage|hospital|'
                r'ambulance|biohazard|radiation|skull|shield|sword|swords|bomb|target|crosshair|flag|medal|trophy|crown|gem|ring|'
                r'key|lock|unlock|door-closed|door-open|house|home|building|building-2|castle|church|landmark|tent|warehouse|factory|'
                r'lighthouse|ferris-wheel|roller-coaster|tractor|car|bus|train-front|plane|rocket|ship|sailboat|anchor|bike|'
                r'fuel|wrench|hammer|pickaxe|axe|shovel|drill|saw|cog|magnet|scale-3d|ruler|pencil|pen|eraser|scissors|'
                r'book|book-open|scroll|scroll-text|newspaper|library|notebook|graduation-cap|school|backpack|'
                r'sun|moon|star|sparkles|cloud|cloud-rain|cloud-snow|cloud-lightning|cloud-fog|tornado|wind|waves|droplet|droplets|snowflake|'
                r'flame|mountain|mountain-snow|volcano|earth|globe|orbit|satellite|telescope|microscope|atom|dna|flask-conical|test-tube|'
                r'hourglass|clock|calendar|timer|alarm-clock|history|infinity|coins|banknote|wallet|gem|'
                r'music|guitar|piano|drum|film|camera|tv|radio|lightbulb|lamp|candle|flashlight|zap|battery|plug|'
                r'utensils|pizza|cake|candy|apple|banana|cherry|citrus|carrot|wheat|egg|milk|coffee|wine|beer)$')
# script nouns that have no icon of the same name
OVERRIDE = {
    'whale': 'fish', 'whales': 'fish', 'shark': 'fish', 'sharks': 'fish', 'tuna': 'fish', 'salmon': 'fish', 'sardine': 'fish', 'dolphin': 'fish',
    'squid': 'fish-symbol', 'octopus': 'fish-symbol', 'crab': 'shell', 'clam': 'shell', 'mussel': 'shell', 'snail': 'snail', 'worm': 'worm', 'worms': 'worm',
    'dinosaur': 'bone', 'dinosaurs': 'bone', 'fossil': 'bone', 'fossils': 'bone', 'skeleton': 'bone', 'bones': 'bone', 'skull': 'skull', 'death': 'skull',
    'ocean': 'waves', 'sea': 'waves', 'seas': 'waves', 'tide': 'waves', 'tsunami': 'waves', 'river': 'waves', 'lake': 'waves', 'water': 'droplet', 'rain': 'cloud-rain',
    'snow': 'snowflake', 'ice': 'snowflake', 'glacier': 'mountain-snow', 'winter': 'snowflake', 'storm': 'cloud-lightning', 'thunder': 'cloud-lightning',
    'lightning': 'zap', 'fog': 'cloud-fog', 'mist': 'cloud-fog', 'hurricane': 'tornado', 'typhoon': 'tornado', 'volcano': 'volcano', 'lava': 'flame',
    'fire': 'flame', 'flames': 'flame', 'heat': 'thermometer-sun', 'temperature': 'thermometer', 'cold': 'thermometer-snowflake', 
    'forest': 'trees', 'jungle': 'trees', 'tree': 'tree-pine', 'trees': 'trees', 'plant': 'sprout', 'plants': 'sprout', 'seed': 'sprout', 'seeds': 'sprout',
    'grain': 'wheat', 'rice': 'wheat', 'bread': 'croissant', 'food': 'utensils', 'meal': 'utensils', 'meat': 'beef', 'hunger': 'utensils', 'famine': 'wheat',
    'planet': 'orbit', 'planets': 'orbit', 'earth': 'earth', 'world': 'globe', 'universe': 'orbit', 'galaxy': 'orbit', 'galaxies': 'orbit', 
    'astronaut': 'rocket', 'spacecraft': 'rocket', 'probe': 'satellite', 'voyager': 'satellite', 'telescope': 'telescope', 'comet': 'sparkles', 'meteor': 'sparkles',
    'idea': 'lightbulb', 'electricity': 'zap', 'energy': 'zap', 'power': 'zap', 'time': 'clock', 'hour': 'clock', 'hours': 'clock',
    'minute': 'timer', 'minutes': 'timer', 'second': 'timer', 'seconds': 'timer', 'year': 'calendar', 'years': 'calendar', 'century': 'calendar', 'day': 'sun', 'night': 'moon',
    'money': 'banknote', 'gold': 'coins', 'treasure': 'gem', 'wealth': 'coins', 'price': 'banknote', 'cost': 'banknote', 'trade': 'handshake', 'deal': 'handshake',
    'king': 'crown', 'queen': 'crown', 'emperor': 'crown', 'empire': 'crown', 'war': 'swords', 'battle': 'swords', 'army': 'shield', 'soldier': 'shield',
    'weapon': 'sword', 'bomb': 'bomb', 'explosion': 'bomb', 'disease': 'biohazard', 'virus': 'biohazard', 'bacteria': 'microscope', 'germ': 'microscope',
    'medicine': 'pill', 'doctor': 'stethoscope', 'hospital': 'hospital', 'blood': 'droplet', 'heart': 'heart', 'brain': 'brain', 'mind': 'brain', 'memory': 'brain',
    'eye': 'eye', 'eyes': 'eye', 'ear': 'ear', 'hand': 'hand', 'hands': 'hand', 'body': 'person-standing', 'human': 'person-standing', 'humans': 'person-standing',
    'people': 'users', 'person': 'user', 'child': 'baby', 'children': 'baby', 'baby': 'baby', 'family': 'users', 'tribe': 'users', 'village': 'houses', 'city': 'building-2',
    'house': 'house', 'home': 'house', 'temple': 'landmark', 'church': 'church', 'castle': 'castle', 'tower': 'building',  'pyramid': 'triangle',
    'ship': 'ship', 'boat': 'sailboat', 'sail': 'sailboat', 'submarine': 'ship', 'train': 'train-front', 'car': 'car', 'plane': 'plane', 'aircraft': 'plane', 'rocket': 'rocket',
    'book': 'book', 'books': 'book', 'letter': 'mail', 'map': 'map', 'compass': 'compass', 'key': 'key', 'lock': 'lock', 'clock': 'clock', 'bell': 'bell',
    'music': 'music', 'song': 'music', 'camera': 'camera', 'photo': 'camera', 'film': 'film', 'movie': 'film', 'radio': 'radio', 'signal': 'radio', 'satellite': 'satellite',
    'atom': 'atom', 'molecule': 'atom', 'dna': 'dna', 'gene': 'dna', 'genes': 'dna', 'cell': 'microscope', 'cells': 'microscope', 'experiment': 'flask-conical', 'chemistry': 'flask-conical',
    'science': 'atom', 'scientist': 'microscope', 'laboratory': 'flask-conical', 'lab': 'flask-conical', 'math': 'sigma', 'puzzle': 'puzzle', 'mystery': 'search',
    'gear': 'cog', 'machine': 'cog', 'engine': 'cog', 'factory': 'factory', 'tool': 'wrench', 'tools': 'wrench', 'hammer': 'hammer', 'anvil': 'anvil', 'magnet': 'magnet',
    'bird': 'bird', 'birds': 'bird', 'egg': 'egg', 'eggs': 'egg', 'feather': 'feather', 'wing': 'feather', 'insect': 'bug', 'insects': 'bug', 'beetle': 'bug', 'ant': 'bug', 'bee': 'bug',
    'butterfly': 'bug', 'spider': 'bug', 'frog': 'bug', 'mouse': 'rat', 'rat': 'rat', 'rats': 'rat', 'rabbit': 'rabbit', 'cat': 'cat', 'dog': 'dog', 'wolf': 'dog',
    'bear': 'paw-print', 'lion': 'paw-print', 'tiger': 'paw-print', 'elephant': 'paw-print', 'mammoth': 'paw-print', 'horse': 'paw-print', 'cow': 'beef', 'pig': 'ham',
    'turtle': 'turtle', 'snake': 'worm', 'lizard': 'worm', 'footprint': 'footprints', 'footprints': 'footprints', 'track': 'footprints', 'tracks': 'footprints',
    'mountain': 'mountain', 'mountains': 'mountain', 'cave': 'mountain', 'island': 'tree-palm', 'beach': 'tree-palm', 'sun': 'sun', 'moon': 'moon', 'star': 'star', 'stars': 'star',
    'cloud': 'cloud', 'clouds': 'cloud', 'wind': 'wind', 'air': 'wind', 'oxygen': 'wind', 'breath': 'wind', 'rainbow': 'rainbow', 'drop': 'droplet', 'flood': 'waves',
    'trophy': 'trophy', 'medal': 'medal', 'prize': 'trophy', 'winner': 'trophy', 'flag': 'flag', 'target': 'target', 'goal': 'target', 'gift': 'gift', 'party': 'party-popper',
    'diamond': 'gem', 'gem': 'gem', 'jewel': 'gem', 'coin': 'coins', 'coins': 'coins', 'bank': 'landmark', 'market': 'store', 'shop': 'store',
    'scale': 'scale', 'balance': 'scale', 'law': 'scale', 'court': 'gavel', 'judge': 'gavel', 'rule': 'ruler', 'ruler': 'ruler', 'measure': 'ruler', 'thermometer': 'thermometer',
    'pen': 'pen', 'pencil': 'pencil', 'paper': 'file-text', 'page': 'file-text', 'document': 'file-text', 'scroll': 'scroll', 'newspaper': 'newspaper', 'library': 'library',
    'school': 'school', 'student': 'graduation-cap', 'teacher': 'graduation-cap', 'graduate': 'graduation-cap', 'lesson': 'book-open', 'question': 'circle-help', 'answer': 'circle-check',
    'danger': 'triangle-alert', 'warning': 'triangle-alert', 'alarm': 'siren', 'siren': 'siren', 'poison': 'skull', 'toxic': 'biohazard', 'radiation': 'radiation',
    'tooth': 'tooth', 'teeth': 'tooth', 'bite': 'tooth', 'jaw': 'tooth', 'glasses': 'glasses', 'shirt': 'shirt', 'cloth': 'shirt', 'clothes': 'shirt', 'bag': 'briefcase',
    'bed': 'bed', 'sleep': 'bed', 'dream': 'moon-star', 'bath': 'bath', 'door': 'door-open', 'fence': 'fence', 'wall': 'brick-wall', 'road': 'route',
    'path': 'route', 'journey': 'route', 'trip': 'route', 'travel': 'plane', 'distance': 'ruler', 'depth': 'anchor', 'deep': 'anchor', 'ladder': 'ladder',
    'candle': 'candle', 'lamp': 'lamp', 'lantern': 'lamp', 'torch': 'flashlight', 'battery': 'battery', 'plug': 'plug', 'wire': 'cable', 'chain': 'link', 'rope': 'link',
    'tent': 'tent', 'camp': 'tent', 'campfire': 'flame-kindling', 'smoke': 'cloud-fog', 'steam': 'cloud-fog', 'dust': 'cloud-fog', 'sand': 'hourglass', 'hourglass': 'hourglass',
    'calendar': 'calendar', 'date': 'calendar', 'history': 'history', 'past': 'history', 'future': 'telescope', 'infinity': 'infinity', 'forever': 'infinity', 'cycle': 'refresh-cw',
    'wheel': 'circle-dot',   'cube': 'box', 'box': 'box', 'package': 'package', 'crate': 'package',
    'glass': 'wine', 'bottle': 'bottle-wine', 'cup': 'coffee', 'coffee': 'coffee', 'tea': 'coffee', 'wine': 'wine', 'beer': 'beer', 'milk': 'milk', 'honey': 'droplet', 'sugar': 'candy',
    'salt': 'droplets', 'pizza': 'pizza', 'cake': 'cake', 'cookie': 'cookie', 'apple': 'apple', 'fruit': 'apple', 'banana': 'banana', 'cherry': 'cherry', 'grape': 'grape',
    'grapes': 'grape', 'carrot': 'carrot', 'vegetable': 'carrot', 'nut': 'nut', 'nuts': 'nut', 'egg': 'egg', 'soup': 'soup', 'knife': 'utensils', 'fork': 'utensils', 'spoon': 'utensils',
    'guitar': 'guitar', 'piano': 'piano', 'drum': 'drum', 'drums': 'drum', 'trumpet': 'music', 'violin': 'music', 'dance': 'music', 'theater': 'drama', 'theatre': 'drama', 'mask': 'drama',
    'game': 'gamepad-2', 'dice': 'dice-5', 'chess': 'crown', 'ticket': 'ticket', 'phone': 'phone', 'computer': 'laptop',
    'screen': 'monitor', 'television': 'tv', 'tv': 'tv', 'internet': 'globe', 'network': 'network', 'robot': 'bot', 'chip': 'cpu', 
}
WORD = re.compile(r"[a-z][a-z'-]*")


def _load():
    global _ICONS, _TAGS
    if _ICONS is None:
        _ICONS = json.load(open(os.path.join(ASSETS, 'lucide.json'), encoding='utf-8'))
        _TAGS = {}   # lucide tags are not shipped (too loose, see icon_for)
    return _ICONS


def _sing(w):
    if w.endswith('ies') and len(w) > 4: return w[:-3] + 'y'
    if w.endswith('es') and len(w) > 4 and w[-3] in 'sxz': return w[:-2]
    if w.endswith('s') and not w.endswith('ss') and len(w) > 3: return w[:-1]
    return w


def icon_for(text):
    """lucide icon name for a name label / number badge text, or None. Priority: OVERRIDE (script nouns) > an icon named exactly like a word.
    Only picture-like icons (PICT_ALLOW); UI glyphs never. Deterministic: first word that matches wins."""
    icons = _load(); words = WORD.findall(text.lower())
    for w in words:
        for cand in (w, _sing(w)):
            if cand in OVERRIDE and OVERRIDE[cand] in icons: return OVERRIDE[cand]
    for w in words:
        for cand in (w, _sing(w)):
            if cand in icons and PICT_ALLOW.match(cand): return cand
    return None   # lucide tags are NOT used: they matched too loosely (hole -> drill, horizon -> calendar) in the 2026-10-29 dry run



def icon_svg(name, size=40, color='currentColor', sw=2, cls='pict', idp=''):
    """inline lucide icon (24-unit viewBox) as an <svg> string; strokes only (fill none), so DrawSVG can draw it in"""
    body = _load().get(name)
    if not body: return ''
    return (f'<svg class="{cls}" {f"id={chr(34)}{idp}{chr(34)} " if idp else ""}viewBox="0 0 24 24" width="{size}" height="{size}" fill="none" stroke="{color}" '
            f'stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round">{body}</svg>')


def icon_count():
    return len(_load())


if __name__ == '__main__':
    import sys
    for t in sys.argv[1:] or ['Marine snow', 'Whale fall', '3,800 m deep', 'Stolen time', 'Voyager 1', 'The Fore people', 'Kuru', 'Big Bang', 'Black hole']:
        print(f'{t!r:28} -> {icon_for(t)}')
    print('icons', icon_count())
