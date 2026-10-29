# axis_lib.py -- THE AXIS CATALOGUE (2026-10-29, miya: "축에 대한 것들을 자세하고 다양하게 미리 다 만들어 놓고 규칙화해서 에이전트들이 그저 가져다 쓰게").
#
# One table says, for every kind of thing a picture agent draws, WHERE its axis is, WHICH motion kinds fit it and WHAT goes in its group.
# The agent only names the group after the thing (`mv-<kind>-<thing>`, art_spec 7); the pivot is then computed from the drawing by this
# module (`resolve` / `apply`), checked by attachcheck.py ("catalogue" lines) and written by `tools/axisfix.py`. build3 applies it before every build.
# No model judgement, no hand-typed coordinates: the same drawing always gets the same axis.
#
# Pivot rules (how the point is computed from the shapes of the group, in picture coordinates):
#   base     foot of the thing: x-centre of the narrow shapes that touch the bottom of the group, y = that bottom  (trees, grass, signs, poles, people)
#   top      hanging point: x-centre of the narrow shapes that touch the top of the group, y = that top             (lanterns, bells, pendulums, ropes, bags)
#   contact  where the part touches its body: centroid of the part's outline points that lie on body / parent-link shapes (tails, legs, necks, wings, jaws, lids, tools in a hand)
#   round    centre of the round face: the largest circle/ellipse inside the group (wheel, gear, fan) or, for a hand/needle, the smallest round body shape under its root end
#   edge     the hoist edge of a flag / sail: midpoint of the group's side that touches the pole (or its left side when no pole is found)
#   center   centre of the group box (free-floating or balanced things: planets, boats, balloons, seesaw beams, bubbles)
#   none     this must not rotate at all (water, smoke, fire, light, ground): sway / joint / rotor on it is a mistake
#
# Kinds: `ok` = kinds that fit; anything in `bad` is reported (motions.core_sanitize / obj_sanitize already rewrite some of them at build time).
import re, sys

W0, H0 = 1920, 1080

# (regex on the group's name tail, pivot rule, kinds that fit, kinds that do not, what belongs in the group / note)
CATALOGUE = [
    # ---- standing things: axis = the foot ----
    (r'tree|trunk|oak|pine|palm|birch|willow|sapling|bush|shrub|hedge', 'base', 'sway tilt core-sway topple', 'spin wobble roll orbit tremble', 'trunk + crown only; no ground, shadow, water or other trees (one group per tree)'),
    (r'grass|reed|cattail|stalk|stem|wheat|rice|bamboo|fern|weed|kelp|seaweed|coral|sprout|seedling|flower|tulip|sunflower|plant|cactus|mushroom', 'base', 'sway tilt core-sway grow', 'spin wobble roll orbit', 'one clump per group (splitclumps.py); no pond / soil / shadow inside'),
    (r'sign|signpost|post|pole|mast|flagpole|lamppost|streetlight|lamp-post|tower|lighthouse|chimney|column|pillar|totem|obelisk|monument|statue|scarecrow|antenna|fence|tombstone|gravestone|cross|stake|pile|stack', 'base', 'sway tilt topple core-sway shake', 'spin wobble roll orbit', 'the whole upright thing (a sign = post + every board); it stands ON the ground, the ground stays outside'),
    (r'candle|torch|bottle|vase|jar|bowl|glass|cup|mug|flask|beaker|test-tube|bucket-standing|urn|pot-standing', 'base', 'sway tilt topple core-sway shake wobble core-wobble', 'spin orbit', 'a standing container tips from its foot (wobble is fine: a jar rocking)'),
    (r'person|people|man|woman|kid|child|boy|girl|figure|scientist|researcher|farmer|villager|astronaut|runner|walker|hiker|teacher|student|soldier|king|queen|worker|crowd|frog|toad|bear|deer|cow|horse|dog|cat|wolf|fox|rabbit|hare|mouse|rat|elephant|lion|tiger|monkey|ape|penguin|owl|bird|duck|heron|egret|crow|eagle|chicken|dinosaur|dino|lizard|snail|turtle|tortoise|crab|insect|ant|bee|beetle|spider|butterfly|moth', 'base', 'sway nod breathe hop creep path swim float bob tilt', 'spin roll flip orbit rotor', 'a creature sways from its FEET; its tail / legs / neck / wings are their own joint or chain groups INSIDE this one'),
    # ---- hanging things: axis = the hook ----
    (r'lantern|puppet|marionette|hanging-lamp|chandelier|bell|pendulum|bob|plumb|rope|cord|string|thread|chain|vine|liana|icicle|stalactite|hook|banner|curtain|drape|tag|label-tag|cocoon|chrysalis|hammock|noose|ornament|bauble|medal|necklace|pendant|locket|pocket-watch|cradle|basket-hanging|bag|sack|net-bag|pouch|punching-bag|windchime|wind-chime|mobile|key-ring|keys|hanging', 'top', 'swing pendulum sway', 'spin roll topple', 'the hanging thing + its cord; the pivot is where the cord meets the ceiling / branch / hand / pole'),
    (r'spider|bat', 'top', 'swing pendulum float', 'spin roll', 'hangs from its thread / the ceiling'),
    # ---- turning things: axis = the hub ----
    (r'wheel|gear|cog|sprocket|fan|propeller|prop|rotor|turbine|blades|windmill-blades|pinwheel|impeller|reel|spool|pulley|steering|knob|valve|dial|ferris|carousel|roulette|millstone|waterwheel|grindstone|turntable|record|vinyl|disc|disk|coin|token|medallion|saw-blade|sawblade|tire|tyre|hub|cap-spinning', 'round', 'rotor spin core-spin turn', 'sway topple wobble', 'the round part only (a windmill: blades = rotor, tower = a separate standing group); gears mesh (gearmesh.py)'),
    (r'hand|needle|pointer|arrow-hand|minute|hour|second|compass-needle|indicator|gauge-needle', 'round', 'rotor joint', 'sway spin', 'a clock / gauge hand turns about the CENTRE of its dial, not about its own middle'),
    # ---- parts of a body: axis = where the part meets the body ----
    (r'tail|tailfin|fin|flipper|fluke|tentacle|arm|forearm|leg|foreleg|hindleg|thigh|shin|foot|feet|paw|hoof|claw|pincer|wing|ear|neck|head|jaw|mouth|beak|bill|snout|trunk-elephant|tongue|whisker|feeler|antennae|horn|antler|mane|hair|ponytail|braid|finger|thumb|crest|feather|plume|tentacles|proboscis|stinger|eyestalk|extra-leg|extraleg', 'contact', 'joint chain flap wiggle', 'sway spin rotor topple', 'the part only, drawn so it OVERLAPS the body by a few px; chains nest (-1 holds -2); the whole creature\'s travel group holds the parts'),
    (r'door|lid|hatch|gate|drawbridge|visor|cover|book-cover|page|shutter|window|trapdoor|ramp|flap-door|mailbox-flag|screen|laptop|toilet-seat|piano-lid|cap-hinged|lever-arm|crane-arm|boom|jib|catapult|trebuchet|drawer', 'contact', 'joint swing', 'spin rotor sway', 'hinged along the edge that touches the frame / body: draw the hinge side overlapping the frame'),
    (r'hammer|axe|pickaxe|sword|dagger|knife|bat|club|racket|wand|baton|cane|stick|staff|spear|oar|paddle|rod|fishing-rod|brush|pen|pencil|chalk|spoon|ladle|fork|torch-held|flashlight|net|butterfly-net|sickle|scythe|shovel|spade|hoe|broom|mop|umbrella-held|flag-held', 'contact', 'joint swing', 'spin rotor sway', 'a hand-held tool pivots where the HAND holds it (net: pole end + bag in one group, or the bag swings from the rim)'),
    # ---- flags: axis = the hoist edge ----
    (r'flag|pennant|windsock|sail|streamer|bunting', 'edge', 'flagwave swing sway', 'spin rotor topple', 'the cloth only; the pole is a standing group of its own (or inside, in which case the pivot is the pole foot)'),
    # ---- balanced / free things: axis = the centre ----
    (r'seesaw|see-saw|teeter|lever|balance|scale|scales|beam|plank|raft-balance', 'center', 'tilt swing pendulum', 'spin roll topple', 'the beam pivots on its fulcrum (its centre, or data-pivot on the pin if drawn off-centre)'),
    (r'boat|ship|raft|canoe|kayak|ferry|yacht|submarine|sub|barge|buoy|lifeboat|dinghy', 'center', 'bob tilt path glide float', 'spin roll rotor sway', 'the hull + everything on it bobs together (sails may be their own flag groups)'),
    (r'balloon|airship|blimp|zeppelin|kite|parachute|cloud-ride|ufo|saucer|drone|helicopter|plane|airplane|jet|rocket|probe|satellite|capsule|shuttle|lander|voyager', 'center', 'float hover path glide ascend sink bob tilt', 'sway topple rotor', 'moves as one piece; propellers / rotors are separate round groups inside'),
    (r'planet|moon|sun|earth|mars|jupiter|saturn|venus|mercury|world|globe|asteroid|comet|meteor|star|galaxy|nebula|orb|sphere|bubble|ball|marble|pearl|egg|atom|nucleus|electron|molecule|cell|virus|bacterium|spore|seed|nut|bead|droplet-free|hourglass|clock|watch|dial-face|compass', 'center', 'spin wobble breathe swell heartbeat float orbit core-spin core-wobble', 'sway topple', 'round thing: turns / breathes about its own centre; the hands of a clock are separate round groups'),
    (r'box|crate|chest|barrel|drum|can|bucket|basket|cart|wagon|barrow|sled|sledge|trolley|car|truck|bus|train|tractor|tank|bike|bicycle|scooter|skateboard|wheelbarrow|anvil|rock|boulder|stone|brick|block|book|notebook|phone|tablet|radio|tv|television|monitor|camera|suitcase|bag-ground|backpack|package|parcel|gift|cake|pie|bread|pot|pan|kettle|bottle-lying', 'center', 'drop bouncing rollby slide skid toss magnet shake squash popin rise topple', 'rotor pendulum', 'a solid object; topple / tilt pivot at the bottom corner is set by the build'),
    (r'swarm|flock|school|shoal|herd|cloud-of|cluster|colony|tadpole|larva|larvae|cercaria|cercariae|worm|parasite|microbe|germ|amoeba|plankton|sperm|jellyfish|blob|dot|dots', 'center', 'wiggle swim float path drift orbit breathe heartbeat swell spin rotor turn', 'sway topple joint', 'a free swimmer / a crowd of small things moves as one about its own centre; no axis to attach'),
    (r'tile|card|panel|plate|slab|domino|brick-tile|block-tile|sheet|poster|photo|picture|frame|sticker|note|paper|letter|envelope|newspaper|map|scroll-flat', 'center', 'topple drop bouncing slide skid toss popin rise fade flip shake', 'rotor pendulum', 'a flat tile / card: topples from its bottom corner (set by the build), otherwise moves as one piece'),
    # ---- things that never rotate ----
    (r'water|sea|ocean|lake|pond|river|stream|waves|surf|puddle|rain|snow|smoke|steam|mist|fog|haze|cloud|fire|flame|blaze|ember|spark|light|ray|beam-light|glow|halo|shadow|ground|floor|soil|sand|road|path-ground|sky|horizon|sunlight|lightning|aurora|nebula-bg|grid|dust', 'none', 'ripple flicker drift fade breathe swell glint dash scroll liquid fill bubble', 'joint rotor sway swing pendulum spin topple tilt wobble', 'liquids, gases, light and ground have no axis: use ripple / flicker / drift / fade, never a rotation'),
]
CATALOGUE = [(re.compile(rx, re.I), rule, ok.split(), bad.split(), note) for rx, rule, ok, bad, note in CATALOGUE]
HAND_RE = re.compile(r'hand|needle|pointer|arrow-hand|minute|hour|second|compass-needle|indicator|gauge-needle', re.I)   # the only round things whose axis lies OUTSIDE the group (on the dial)
RULE_KO = {'base': '발(밑동)', 'top': '매단 점', 'contact': '몸에 닿는 점', 'round': '둥근 면 중심', 'edge': '깃대 쪽 가장자리', 'center': '중심', 'none': '축 없음(회전 금지)'}


def tail_of(gid):
    """the thing's name: 'mv-swing-net-bag' -> 'net-bag', 'mv-core-sway-tree' -> 'tree', 'mv-chain-tail-2' -> 'tail'"""
    t = re.sub(r'^mv-(core-)?[a-z]+-', '', gid); t = re.sub(r'-\d+$', '', t); t = re.sub(r'^u\d+', '', t)
    return t


def kind_of(gid):
    m = re.match(r'^mv-(core-[a-z]+|[a-z]+)', gid); return m.group(1) if m else ''


def _match(w):
    for rx, rule, ok, bad, note in CATALOGUE:
        m = rx.fullmatch(w) or rx.search(w)
        if m and (m.group(0) == w or len(w) > 14): return dict(rule=rule, ok=ok, bad=bad, note=note, word=w)
    return None


def entry_for(gid):
    """the catalogue row for a group name. Words of the name tail are tried from the LAST (the head noun: 'net-bag' = bag, 'bird-neck' = neck, 'windmill-blades' = blades);
    a row whose kinds fit the group's own kind wins over an earlier word ('wheel-cart' + rotor = wheel), else the first row found; then a substring fallback ('reedclump')."""
    t = tail_of(gid); kind = kind_of(gid); ks = kind.replace('core-', '')
    cands = [e for e in (_match(re.sub(r'\d+$', '', w)) for w in reversed(re.split(r'[-_ ]+', t)) if re.sub(r'\d+$', '', w)) if e]
    e = None
    for c in cands:
        if kind in c['ok'] or ks in c['ok']: e = c; break
    if e is None and cands: e = cands[0]
    if e is None:
        for rx, rule, ok, bad, note in CATALOGUE:   # substring at the END of a short prefix only: 'hptail' -> tail, not 'overhead' -> head
            m = rx.search(t)
            if m and len(m.group(0)) >= 4 and m.end() == len(t) and m.start() <= 2: e = dict(rule=rule, ok=ok, bad=bad, note=note, word=m.group(0)); break
    if e and ks in ('joint', 'chain') and (e['rule'] in ('base', 'center') or (e['rule'] == 'round' and not HAND_RE.fullmatch(e['word']))):
        # a joint / chain named after the creature or the machine ('mv-chain-ant-1', 'mv-joint-valve' = its lever) is a PART of it: it hinges where it touches the rest; soft = the drawing decides, no gap error
        e = dict(e, rule='contact', ok=sorted(set(e['ok']) | {'joint', 'chain'}), bad=[b for b in e['bad'] if b not in ('joint', 'chain')], soft=True)
    return e


# rules whose computed point is exact enough to REPORT a written data-pivot that disagrees (foot, hook, hub, hoist edge). 'contact' (limbs, tails, necks) is only computed to
# fill a MISSING pivot: where a limb drawn over the belly really hinges is for attachcheck (pivot on the part AND on the body) and the eye (motionaudit); 'center' may sit on a fulcrum pin;
# a clock / gauge HAND is also fill-only (the hub vs a tick dot vs a glow behind the dial cannot be told apart reliably; attachcheck's rotor-on-round-face rule covers it).
DIST_RULES = ('base', 'top', 'round', 'edge')
TOL = {'top': 32}   # px: a hanging point (strings / a crossbar) is softer than a foot or a hub (12)
HINGE_KINDS = ('joint', 'chain', 'swing', 'rotor', 'pendulum', 'shackle', 'flap', 'wiggle', 'sway', 'tilt', 'core-sway', 'core-tilt', 'spin', 'core-spin', 'turn', 'core-turn', 'flagwave', 'topple')

# Browser side: computes the catalogue pivot of one group from its shapes (same hit-testing as attachcheck.py).
JS = r'''
([W, H, specs]) => {
 const svg = document.querySelector('svg'); const SH = 'path,circle,ellipse,rect,polygon,polyline,line';
 const all = [...svg.querySelectorAll(SH)].filter(e => !e.closest('defs,clipPath,mask,pattern,marker,symbol'));
 const rootCTM = svg.getScreenCTM(); const inv = rootCTM.inverse();
 const bbs = new Map(); const bb = e => { if (!bbs.has(e)) { try { bbs.set(e, e.getBBox()); } catch (x) { bbs.set(e, {x:0,y:0,width:0,height:0}); } } return bbs.get(e); };
 const scrs = new Map(); const scr = e => { if (scrs.has(e)) return scrs.get(e); const r = scr0(e); scrs.set(e, r); return r; };
 const scr0 = e => { const b = bb(e), M = inv.multiply(e.getScreenCTM()); const P = [[b.x,b.y],[b.x+b.width,b.y],[b.x,b.y+b.height],[b.x+b.width,b.y+b.height]].map(([x,y]) => new DOMPoint(x,y).matrixTransform(M));
   const xs = P.map(p=>p.x), ys = P.map(p=>p.y); return {x:Math.min(...xs), y:Math.min(...ys), w:Math.max(...xs)-Math.min(...xs), h:Math.max(...ys)-Math.min(...ys)}; };
 const BGRE = /(^|[-_ ])(bg|backdrop|sky|haze|mist|fog|vignette|background|ground|floor|water|sea|pond|lake)([-_ ]|$)/i;
 const isBig = e => { const s = scr(e); return s.w * s.h > 0.25 * W * H; };
 const ids = e => { const o = []; let n = e; while (n && n !== svg) { if (n.id) o.push(n.id); n = n.parentNode; } return o; };
 const isBg = e => isBig(e) || ids(e).some(i => BGRE.test(i));
 const hit = (e, x, y) => { const m = e.getScreenCTM(); if (!m) return false; const q = new DOMPoint(x, y).matrixTransform(rootCTM).matrixTransform(m.inverse()); const cs = getComputedStyle(e);
   try { if (cs.fill !== 'none' && e.tagName !== 'line' && e.tagName !== 'polyline' && e.isPointInFill(q)) return true; } catch (z) {}
   try { if (cs.stroke !== 'none' && e.isPointInStroke(q)) return true; } catch (z) {}
   return false; };
 const R = [0, 3, 6, 9, 12, 18, 26, 40], DIR = 12;
 const dist = (set, x, y, maxr) => { for (const r of R) { if (r > maxr) break; const n = r === 0 ? 1 : DIR; for (let k = 0; k < n; k++) { const a = 2 * Math.PI * k / DIR, px = x + r * Math.cos(a), py = y + r * Math.sin(a);
     for (const e of set) if (hit(e, px, py)) return r; } } return 999; };
 const shapesIn = g => [...g.querySelectorAll(SH)].filter(e => !e.closest('defs,clipPath,mask,pattern,marker,symbol'));
 const box = part => { let x0 = 1e9, y0 = 1e9, x1 = -1e9, y1 = -1e9; for (const e of part) { const t = scr(e); if (t.w + t.h === 0) continue; x0 = Math.min(x0, t.x); y0 = Math.min(y0, t.y); x1 = Math.max(x1, t.x + t.w); y1 = Math.max(y1, t.y + t.h); } return {x: x0, y: y0, w: x1 - x0, h: y1 - y0}; };
 // outline sample points of a part: perimeter of each shape's box + the box edges, kept only where the part really is (hit test)
 const outline = part => { const pts = []; for (const e of part) { const s = scr(e); const n = Math.max(6, Math.round((s.w + s.h) / 12));
     for (let i = 0; i <= n; i++) { const f = i / n; for (const [x, y] of [[s.x + f * s.w, s.y], [s.x + f * s.w, s.y + s.h], [s.x, s.y + f * s.h], [s.x + s.w, s.y + f * s.h]]) if (hit(e, x, y) || dist([e], x, y, 3) < 999) pts.push([x, y]); } }
   return pts; };
 const out = [];
 for (const sp of specs) {
   const g = document.getElementById(sp.id); if (!g) { out.push({id: sp.id, err: 'no group'}); continue; }
   const part = shapesIn(g); if (!part.length) { out.push({id: sp.id, err: 'empty'}); continue; }
   const gb = box(part); const res = {id: sp.id, box: [Math.round(gb.x), Math.round(gb.y), Math.round(gb.w), Math.round(gb.h)]};
   const near = e => { const s = scr(e); return s.x < gb.x + gb.w + 50 && s.x + s.w > gb.x - 50 && s.y < gb.y + gb.h + 50 && s.y + s.h > gb.y - 50; };
   const contains = e => { const s = scr(e); return s.x <= gb.x + 2 && s.y <= gb.y + 2 && s.x + s.w >= gb.x + gb.w - 2 && s.y + s.h >= gb.y + gb.h - 2; };   // a panel / tank / card behind the part is not its body
   const body = all.filter(e => !g.contains(e) && near(e) && !isBg(e) && !contains(e));
   // parent link for chains / nested joints
   let parentG = null; for (let a = g.parentNode; a && a !== svg; a = a.parentNode) if (a.id && /^mv-(chain|joint)/.test(a.id)) { parentG = a; break; }
   const parentShapes = parentG ? shapesIn(parentG).filter(e => !g.contains(e) && near(e)) : null;
   const narrow = part.map(e => ({e, s: scr(e)})).filter(o => o.s.w < Math.max(60, 0.5 * gb.w) || o.s.h > 0.4 * gb.h);
   const pool = narrow.length ? narrow : part.map(e => ({e, s: scr(e)}));
   if (sp.rule === 'base') { const yb = Math.max(...pool.map(o => o.s.y + o.s.h)); const foot = pool.filter(o => o.s.y + o.s.h > yb - Math.max(8, 0.04 * gb.h));
     res.pivot = [foot.reduce((s, o) => s + o.s.x + o.s.w / 2, 0) / foot.length, yb]; }
   else if (sp.rule === 'top') { const yt = Math.min(...pool.map(o => o.s.y)); const head = pool.filter(o => o.s.y < yt + Math.max(8, 0.04 * gb.h));
     res.pivot = [head.reduce((s, o) => s + o.s.x + o.s.w / 2, 0) / head.length, yt]; }
   else if (sp.rule === 'center') res.pivot = [gb.x + gb.w / 2, gb.y + gb.h / 2];
   else if (sp.rule === 'round') {
     // 1 a circle / ellipse of the group's own near its box centre (hub); 2 a roughly square group (toothed gear path) = box centre; 3 an elongated hand / needle: the dial = round shape near one of its ends
     const cx0 = gb.x + gb.w / 2, cy0 = gb.y + gb.h / 2, sz = Math.max(gb.w, gb.h); let best = null, bd = 1e9;
     for (const e of part) { if (!(e.tagName === 'circle' || e.tagName === 'ellipse')) continue; const s = scr(e); const d = Math.hypot(s.x + s.w / 2 - cx0, s.y + s.h / 2 - cy0); if (d < bd) { bd = d; best = {cx: s.x + s.w / 2, cy: s.y + s.h / 2}; } }
     const aspect = gb.w / Math.max(1, gb.h);
     if (best && bd < 0.2 * sz) { res.pivot = [best.cx, best.cy]; res.round = 'own'; }
     else if (!sp.hand) { res.pivot = [cx0, cy0]; res.round = 'box'; }   // a propeller / blade pair / fan without a hub circle turns about its box centre; only a hand / needle looks for its dial
     else { // a hand / needle: the dial or hub = a round shape (not of the group, >= 10 px, no star dots) whose centre sits at one END of the hand; the smallest one within 20 px (the hub) wins, else the nearest
       let b2 = null; const ends = [[gb.x, gb.y], [gb.x + gb.w, gb.y], [gb.x, gb.y + gb.h], [gb.x + gb.w, gb.y + gb.h], [gb.x + gb.w / 2, gb.y], [gb.x + gb.w / 2, gb.y + gb.h], [gb.x, gb.y + gb.h / 2], [gb.x + gb.w, gb.y + gb.h / 2]];
       const cand = [];
       for (const e of all) { if (g.contains(e) || !(e.tagName === 'circle' || e.tagName === 'ellipse')) continue; const s = scr(e); if (s.w > 0.6 * W || s.w < 10) continue; const cx = s.x + s.w / 2, cy = s.y + s.h / 2;
         const d = Math.min(...ends.map(([x, y]) => Math.hypot(x - cx, y - cy))); if (d <= 0.5 * Math.max(s.w, s.h) + 30) cand.push({d, a: s.w * s.h, cx, cy}); }
       const close = cand.filter(c => c.d <= 20); if (close.length) b2 = close.reduce((m, c) => c.a < m.a ? c : m);   // the hub, not a glow / dial behind it (concentric anyway) else if (cand.length) b2 = cand.reduce((m, c) => c.d < m.d ? c : m);
       if (b2) { res.pivot = [b2.cx, b2.cy]; res.round = 'face'; } else { res.pivot = [cx0, cy0]; res.round = 'box'; } } }
   else if (sp.rule === 'edge') {
     // the pole: a tall thin body shape touching the group's left or right side
     let side = null, bestD = 1e9; for (const e of body) { const s = scr(e); if (!(s.h > 2.5 * s.w && s.h > 0.6 * gb.h)) continue;
       const dl = Math.abs(s.x + s.w / 2 - gb.x), dr = Math.abs(s.x + s.w / 2 - (gb.x + gb.w)); if (dl < 30 && dl < bestD) { bestD = dl; side = 'L'; } if (dr < 30 && dr < bestD) { bestD = dr; side = 'R'; } }
     if (!side) { let t = null; for (const e of part) { const s = scr(e); if (s.h > 2.5 * s.w && s.h > 0.6 * gb.h) t = s; } if (t) { res.pivot = [t.x + t.w / 2, t.y + t.h]; res.edge = 'pole-inside'; } else { res.pivot = [gb.x, gb.y + gb.h / 2]; res.edge = 'left?'; } }
     else { res.pivot = [side === 'L' ? gb.x : gb.x + gb.w, gb.y + gb.h / 2]; res.edge = side; } }
   else if (sp.rule === 'contact') {
     // overlap region of the part and its body (grid sample of points inside both); the body = the biggest shape it overlaps (a sibling leg is smaller than the belly);
     // the pivot = centroid of the deepest quarter of that overlap, measured from the part's free end (tip of a tail / toe / head end of a neck), so a limb drawn far over the belly still hinges at its root
     const ref = parentShapes && parentShapes.length ? parentShapes : body; const step = Math.max(3, Math.min(gb.w, gb.h) / 25);
     const inPart = (x, y) => part.some(e => hit(e, x, y)); const grid = [];
     for (let x = gb.x; x <= gb.x + gb.w; x += step) for (let y = gb.y; y <= gb.y + gb.h; y += step) if (inPart(x, y)) grid.push([x, y]);
     const byRef = new Map(); for (const p of grid) for (const e of ref) if (hit(e, p[0], p[1])) { if (!byRef.has(e)) byRef.set(e, []); byRef.get(e).push(p); }
     // the host: a big shape the part overlaps a LITTLE (the belly at a leg's root), not a pad / floor the whole limb lies on (overlap > 60 % of the part) and not a thin sibling limb
     let host = null; for (const [e, ps] of byRef) { if (ps.length < 3 || ps.length > 0.6 * grid.length) continue; const s = scr(e); const sc = s.w * s.h / ps.length; if (!host || sc > host.sc) host = {e, sc, ps}; }
     if (host) {
       const c = host.ps.reduce((o, p) => [o[0] + p[0] / host.ps.length, o[1] + p[1] / host.ps.length], [0, 0]);
       let tip = null, td = -1; for (const p of grid) { const d = Math.hypot(p[0] - c[0], p[1] - c[1]); if (d > td) { td = d; tip = p; } }
       const ds = host.ps.map(p => Math.hypot(p[0] - tip[0], p[1] - tip[1])); const dmax = Math.max(...ds), dmin = Math.min(...ds); const cut = dmax - 0.25 * (dmax - dmin);
       const deep = host.ps.filter((p, i) => ds[i] >= cut); res.pivot = [deep.reduce((s, p) => s + p[0], 0) / deep.length, deep.reduce((s, p) => s + p[1], 0) / deep.length]; res.contact = deep.length; }
     else { // no overlap: nearest outline point to the body (gap)
       const pts = outline(part); let bp = null, bd = 1e9; for (const p of pts) { for (const r of [3, 6, 9, 12, 18, 26, 40]) { if (dist(ref, p[0], p[1], r) < 999) { if (r < bd) { bd = r; bp = p; } break; } } }
       if (bp) { res.pivot = bp; res.contact = 0; res.gap = bd; } else { res.err = 'part touches no body shape (gap > 40 px)'; } }
     // hinge pin drawn inside the group wins
     for (const e of part) { if (e.tagName === 'circle') { const s = scr(e); if (s.w < 40 && res.pivot && Math.hypot(s.x + s.w / 2 - res.pivot[0], s.y + s.h / 2 - res.pivot[1]) < 60) { res.pivot = [s.x + s.w / 2, s.y + s.h / 2]; res.pin = true; } } } }
   else if (sp.rule === 'none') { res.pivot = null; }
   if (res.pivot) { res.pivot = res.pivot.map(v => Math.round(v * 10) / 10);
     // the same point in the group's own (parent) coordinates: shorts wrap a landscape drawing in a scaled group, and data-pivot is written in the drawing's coordinates (build3 miyaPv accepts either frame)
     try { const q = new DOMPoint(res.pivot[0], res.pivot[1]).matrixTransform(rootCTM).matrixTransform(g.parentNode.getScreenCTM().inverse()); res.local = [Math.round(q.x * 10) / 10, Math.round(q.y * 10) / 10]; } catch (z) { res.local = res.pivot; } }
   out.push(res);
 }
 return out;
}
'''


def groups_in(svg):
    """[(id, kind, data-pivot or None)] for every mv- group (static regex, document order)"""
    out = []
    for m in re.finditer(r'<g\b([^>]*)\bid="(mv-[A-Za-z0-9_-]+)"([^>]*)>', svg):
        attrs = m.group(1) + m.group(3); gid = m.group(2)
        pv = re.search(r'data-pivot="\s*(-?[\d.]+)[ ,]+(-?[\d.]+)\s*"', attrs)
        out.append((gid, kind_of(gid), (float(pv.group(1)), float(pv.group(2))) if pv else None))
    return out


def resolve(page, svg, W, H):
    """[{id, kind, rule, word, pivot, current, dist, kind_bad, note, ...}] for every mv- group whose name is in the catalogue"""
    page.set_content(f'<body style="margin:0">{svg}</body>')
    specs = []; meta = {}
    for gid, kind, cur in groups_in(svg):
        e = entry_for(gid)
        if not e: continue
        meta[gid] = dict(dict(soft=False), kind=kind, cur=cur, **e); specs.append(dict(id=gid, rule=e['rule'], hand=bool(HAND_RE.fullmatch(e['word']))))
    res = page.evaluate(JS, [W, H, specs]) if specs else []
    out = []
    for r in res:
        m = meta[r['id']]; kind = m['kind']; kshort = kind.replace('core-', '')
        d = None; loc = r.get('local') or r.get('pivot')
        if r.get('pivot') and m['cur']: d = min(((pt[0] - m['cur'][0]) ** 2 + (pt[1] - m['cur'][1]) ** 2) ** .5 for pt in (r['pivot'], loc))
        kind_bad = (kind in m['bad'] or kshort in m['bad']) and not (kind in m['ok'] or kshort in m['ok'])
        err = r.get('err')
        if err and (m['soft'] or not needs_pivot(kind)): err = None   # an empty / detached group only matters when its kind rotates about a pivot; a whole creature named as a joint is the drawing's business
        out.append(dict(id=r['id'], kind=kind, rule=m['rule'], word=m['word'], note=m['note'], ok=m['ok'], pivot=r.get('pivot'), local=loc, current=m['cur'], dist=d, kind_bad=kind_bad, err=err, extra={k: v for k, v in r.items() if k not in ('id', 'pivot', 'box', 'err')}))
    return out


def needs_pivot(kind):
    """kinds whose rotation uses data-pivot when present (the build falls back to a box corner / centre otherwise)"""
    return kind in HINGE_KINDS or kind.replace('core-', '') in HINGE_KINDS


def problems_of(res, tol=12):
    """problem strings for resolve() results (shared by attachcheck.py, axisfix.py --report and apply)"""
    out = []
    for r in res:
        gid = r['id']
        if r['err']: out.append(f"{gid}: {r['err']} (rule {r['rule']})"); continue
        if r['kind_bad']: out.append(f"{gid}: kind '{r['kind']}' does not fit a {r['word']} (axis {RULE_KO[r['rule']]}; use {', '.join(r['ok'][:4])})"); continue
        if r['rule'] == 'none':
            if needs_pivot(r['kind']): out.append(f"{gid}: a {r['word']} has no axis; '{r['kind']}' rotates it (use ripple / flicker / drift / fade)")
            continue
        if not needs_pivot(r['kind']) or not r['pivot']: continue
        if r['current'] is None: out.append(f"{gid}: no data-pivot ({RULE_KO[r['rule']]} of a {r['word']} = {[round(v) for v in r['pivot']]}); run axisfix.py")
        elif r['rule'] in DIST_RULES and not HAND_RE.fullmatch(r['word']) and r['dist'] > TOL.get(r['rule'], tol):
            out.append(f"{gid}: data-pivot {[round(v) for v in r['current']]} is {r['dist']:.0f} px from the catalogue axis {[round(v) for v in r['pivot']]} ({RULE_KO[r['rule']]} of a {r['word']}); axisfix.py --force writes it")
    return out


def apply(page, path, W, H, force=False, tol=12):
    """write catalogue pivots into the SVG: missing ones always; wrong ones (> tol px, exact rules only) only with force. Returns (written, problems) lists of strings."""
    svg = open(path, encoding='utf-8').read(); written = []
    res = resolve(page, svg, W, H)
    for r in res:
        gid = r['id']
        if r['err'] or r['kind_bad'] or r['rule'] == 'none' or not needs_pivot(r['kind']) or not r['pivot']: continue
        px, py = r['local'] or r['pivot']   # written in the drawing's own coordinates
        if r['current'] is None or (force and r['rule'] in DIST_RULES and not HAND_RE.fullmatch(r['word']) and r['dist'] > TOL.get(r['rule'], tol)):
            m = re.search(r'<g\b[^>]*\bid="%s"[^>]*>' % re.escape(gid), svg)
            if not m: continue
            tag = m.group(0); new = re.sub(r'\s*data-pivot="[^"]*"', '', tag); new = new[:-1] + f' data-pivot="{px:.0f} {py:.0f}">'
            svg = svg[:m.start()] + new + svg[m.end():]
            written.append(f"{gid}: data-pivot {px:.0f},{py:.0f} ({RULE_KO[r['rule']]} of a {r['word']}{', was ' + str([round(v) for v in r['current']]) if r['current'] else ''})")
            r['current'] = (px, py); r['dist'] = 0.0
    if written: open(path, 'w', encoding='utf-8').write(svg)
    return written, problems_of(res, tol)


def doc():
    """the catalogue as a Markdown table (tools/axis_catalog.md is generated from this: python3 tools/axis_lib.py --doc)"""
    L = ['# Axis catalogue (generated from tools/axis_lib.py, do not edit by hand)', '',
         'Name the group after the thing (`mv-<kind>-<thing>`); the axis is computed from the drawing by the rule in column 2 (`tools/axisfix.py`, automatic in build3). '
         'Column 3 = motion kinds that fit, column 4 = kinds that are reported as wrong.', '',
         '| thing (name words) | axis rule | kinds that fit | kinds that do not | group holds / note |', '|---|---|---|---|---|']
    for rx, rule, ok, bad, note in CATALOGUE:
        words = rx.pattern.replace('\\b', '').replace('(?!et)', '').split('|')
        L.append(f"| {', '.join(words[:12])}{' …' if len(words) > 12 else ''} | **{rule}** ({RULE_KO[rule]}) | {' '.join(ok)} | {' '.join(bad)} | {note} |")
    L += ['', 'Rules: base = foot (x-centre of the narrow shapes touching the bottom, y = bottom) · top = hanging point (same at the top) · contact = centroid of the part outline points that lie on the body / parent link (a hinge-pin circle inside the group wins) · '
          'round = centre of the biggest circle/ellipse in the group, else of the smallest round body shape under the part · edge = midpoint of the side that touches a pole · center = box centre · none = must not rotate.',
          '', 'Tolerance: a written `data-pivot` farther than 12 px from the catalogue point is reported by attachcheck.py (`axisfix.py --force` rewrites it).']
    return '\n'.join(L) + '\n'


if __name__ == '__main__':
    if '--doc' in sys.argv: print(doc())
    else:
        for a in sys.argv[1:]: print(a, '->', entry_for(a))
