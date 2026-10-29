# usage: python3 tools/frog_place.py <slug>...   Run after the pictures exist and plan.json has `frog_hint` units, before build3.py.
# Guideline 7-2 (2026-10-26 consolidated). The explainer frog that points is for the CHALKBOARD only. In picture units (plan.json frog_hint: true,
# or a sidecar that already has "frog") the frog is a companion that only appears with a reason (a situational act, moving with an object, an outfit
# or a speech bubble):
#   - strong situation (wind, pull, shiver...) on a moving object: perched on the object's end nearer the screen edge, feet on its drawn surface (perch)
#   - calm act on an object: standing beside it at its foot, facing it (beside); never on top of the middle of the focal object
#   - no object: roaming through the free part of the background, or a special act (slide, orbit, doodle, push, huts)
# Moods per sentence, outfit by words + palette, sound words from per-act pools (never the same twice in a row). Sidecars with "lock": true are kept.
# Writes the "frog" key of videos/<slug>/art3/<uid>.json (creates the sidecar when missing). Never touches the chalkboard frog.
import sys, os, glob, json, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from paths import *
from playwright.sync_api import sync_playwright
import facing
import math, frog_rig, motions   # 2026-10-29: contact / locomotion / costume acts (guideline 7-2 G)
OK = re.compile(r'^mv-(core-(swell|heartbeat|wobble|sway|glide|approach|drop|ping|tremble)|path|slide|swing)')
SPACE = re.compile(r'\b(space|star|stars|galax\w*|cosmic|universe|horizon|probe|voyager|light|planet|orbit|dark|expan\w*)\b', re.I)
SEA = re.compile(r'\b(ocean|oceans|sea|seas|seafloor|underwater|dive|diving|water|whales?|reef|coral|fish|vents?|abyss\w*|deep|depths?|plankton|marine)\b', re.I)
SEA_RIDE = re.compile(r'shark|whale|fish|dolphin|squid|octopus|jelly|turtle|seal\b|ray\b|eel\b|crab|lobster|plankton|krill|sub\b|submarine|submersible|rov\b|diver', re.I)   # riding one of these = the frog is in the water
WATER_G = re.compile(r'water|sea\b|ocean|wave|lake|river|pool|pond|aquarium|tank|current|abyss|seafloor', re.I)


SPACE_PAL = ('space', 'deepfield', 'solar', 'cosmic')
SPACE_RIDE = re.compile(r'rocket|probe|voyager|pioneer|satellite|lander|shuttle|capsule|spaceship|starship|comet|asteroid|meteor', re.I)
GROUND_G = re.compile(r'ground|floor|desk|table|room|street|city|village|hut|house|field|lab\b|dome|cabin|cockpit', re.I)


SPACE_G = re.compile(r'planet|moon|galaxy|comet|asteroid|probe|rocket|satellite|orbit|\bsun\b|earth|mars|jupiter|saturn|blackhole|hole', re.I)   # a nebula wash is a background, not evidence


BG_LAYER = re.compile(r'^mv-(drift|cells|glint|twinkle|scroll|fade|tint|rack)-|\bbg\b|background|backdrop|sky\b|haze|wash', re.I)   # background layers are not objects


def has_group(gs, rx, frac, W, H):
    """an OBJECT group (not a background layer) whose NAME matches rx and whose box covers at least frac of the frame (picture evidence, 2026-10-27)"""
    return any(rx.search(g[0]) and not BG_LAYER.search(g[0]) and g[3] * g[4] >= frac * W * H for g in gs.values())


def in_space(text, palname, gs, ride, W, H, bg='night'):
    """the frog is out in space (helmet): a ridden spacecraft / comet, or a space palette WITH either space words or a big drawn space object
    (planet, probe, sun…) — a starry background alone is not enough (clocks, scales and families are drawn on it too). Never on paper,
    never when a big ground / indoor group (room, desk, street, dome…) is drawn."""
    if ride and SPACE_RIDE.search(ride): return True
    if bg == 'paper' or has_group(gs, GROUND_G, .25, W, H): return False
    if palname not in SPACE_PAL: return bool(SPACE.search(text) and not GROUND.search(text) and has_group(gs, SPACE_G, .04, W, H))
    return bool((SPACE.search(text) and not GROUND.search(text)) or has_group(gs, SPACE_G, .06, W, H))


# picture-evidence outfits (miya 2026-10-27 "대본 규칙이랑 그림 규칙을 다른 것들에도 모두"): (outfit, group-name regex, min frame fraction | 'ride' | 'pal:<name>')
# in priority order. Physical states (PIC_PHYS) beat a word costume; the rest fill in only when the words gave nothing.
PIC_OUTFIT = [('scarf', re.compile(r'snow|\bice\b|iceberg|glacier|igloo|frost|blizzard|icicle|penguin|polar|tundra', re.I), .06),
              ('scarf', None, 'pal:ice'),
              ('umbrella', re.compile(r'\brain|storm|thundercloud|downpour|drizzle', re.I), .08),
              ('umbrella', None, 'pal:storm'),
              ('lifevest', re.compile(r'boat|raft|canoe|kayak|ship\b|deck|ferry|dinghy', re.I), 'ride'),
              ('lab', re.compile(r'microscope|beaker|flask|petri|pipette|test-?tube|centrifuge|labbench', re.I), .02),
              ('lab', None, 'pal:lab'),
              ('headlamp', re.compile(r'cave|mine\b|tunnel|shaft', re.I), .25),
              ('explorer', re.compile(r'jungle|desert|dune|tent|canyon|ruins|temple|pyramid|liana|vine', re.I), .2),
              ('nightcap', re.compile(r'\bbed\b|pillow|blanket|cradle|crib', re.I), .06),
              ('hardhat', re.compile(r'crane|excavator|scaffold|girder|bulldozer|construction|drill', re.I), .08),
              ('chef', re.compile(r'\bpot\b|\bpan\b|stove|kitchen|oven|cauldron|wok', re.I), .05),
              ('doctor', re.compile(r'hospital|stethoscope|syringe|ambulance|x-?ray|wardbed', re.I), .05),
              ('strawhat', re.compile(r'barn|tractor|wheat|haystack|scarecrow|farm|paddy', re.I), .15),
              ('sunglasses', re.compile(r'beach|palm|parasol', re.I), .2)]
PIC_PHYS = ('scarf', 'umbrella', 'lifevest')
HOLE_G = re.compile(r'hole|\bbh\b|singular|vortex|whirlpool|(?<!s)well\b', re.I)   # a drawn hole (not 'swell', not the horizon ring)
ICE_G = PIC_OUTFIT[0][1]; FIRE_G = re.compile(r'fire|flame|lava|magma|furnace|kiln|volcano|ember|blaze|\bsun\b', re.I)


def pic_outfit(gs, palname, ride, W, H, phys_only=False):
    for nm, rx, cond in PIC_OUTFIT:
        if phys_only and nm not in PIC_PHYS: continue
        if cond == 'ride':
            if ride and rx.search(ride): return nm
        elif isinstance(cond, str) and cond.startswith('pal:'):
            if palname == cond[4:]: return nm
        elif has_group(gs, rx, cond, W, H) and not (nm == 'scarf' and palname == 'ocean'): return nm
    return None


def underwater(text, palname, gs, ride, W, H):
    """'deep' / 'shallow' / None: is the frog in the water, judged from the PICTURE as well as the sentence (miya 2026-10-27: the frog rode a shark in the
    human video with no diving gear because the narration spoke of mercury). deep = diving suit + tank, shallow = mask + snorkel."""
    surf = re.search(r'surface|shallow|beach|shore|wave|boat|raft|deck', text, re.I)
    if ride and SEA_RIDE.search(ride): return 'shallow' if surf and not DEEP.search(text) else 'deep'
    if palname == 'ocean': return 'shallow' if surf and not DEEP.search(text) else 'deep'
    big = [g for g in gs.values() if WATER_G.search(g[0]) and g[3] * g[4] >= .25 * W * H]   # a drawn body of water covering a quarter of the frame
    if big or SEA.search(text): return 'deep' if DEEP.search(text) else 'shallow'
    return None


DEEP = re.compile(r'\b(deep|depths?|abyss\w*|dark|darkness|seafloor|sinks?|sinking|descen\w*|vents?|bones?|carcass|silt|thousands of meters)\b', re.I)
ACTS = [   # (act, regex on the unit text, first mood)  -- first match wins (miya 2026-10-25: expression + motion that fits the situation, not only examples)
    ('slide',  re.compile(r'\b(gravity|gravitational|spacetime|space-time|warp\w*|dents?|dented|curves?|curved|curving|funnel|bowl)\b', re.I), 'surprised'),   # (2026-10-26 review: 'sinks/deeper/heavier/slope' gave a dead whale a "Wheee!" slide; ocean videos never slide)   # gravity pit: the frog slides down into it (miya 2026-10-26)
    ('pull',   re.compile(r'\b(black holes?|event horizon|horizon|plunge\w*|spiral\w*|drag\w*|gravity trap|falls? in|pulled|inward|swallow\w*|devour\w*|doom\w*|well)\b', re.I), 'scared'),
    ('wind',   re.compile(r'\b(speed\w*|rac(e|es|ing)|fast\w*|rocket|shuttle|lifts?|orbit\w*|fl(y|ies|ying)|hurtl\w*|streak\w*|whirl\w*|zip\w*|climb\w*|lander|route|dock\w*|launch\w*|race|travel\w*)\b', re.I), 'squint'),
    ('waves',  re.compile(r'\b(waves?|tides?|tidal|ocean|sea|water|splash\w*|wading|knee-deep|shallow|brine)\b', re.I), 'surprised'),
    ('shiver', re.compile(r'\b(crush\w*|freezing|alone|lonely|isolation|cold|terrif\w*|deadly|horror|fear|haunting|exhaustion|grief|mourn\w*|tragic\w*|brutal\w*)\b', re.I), 'scared'),
    ('awe',    re.compile(r'\b(giants?|enormous|supermassive|vast|towering|huge|colossal|billions?|millions?|leviathan|monster|universe|galax\w*)\b', re.I), 'surprised'),
    ('sleepy', re.compile(r'\b(years|decades|waiting|slow\w*|frozen|amber|steady|steadily|patient\w*|ticking|ticks?|clocks?)\b', re.I), 'sleepy'),
    ('cheer',  re.compile(r'\b(solved|breakthrough|discover\w*|works?|yes|answer|possible|allows?|proved?|proof)\b', re.I), 'excited'),
]
GROUND = re.compile(r'\b(planet|moon|mars|surface|ground|land|desert|shore|beach|island|terrain|crater|road|path|walk\w*|run\w*|city|field|hill|mountain)\b', re.I)
def free_band(pg, W, H, vert, n):
    """vertical centre of the emptiest horizontal band of the picture (lowest edge density), outside the caption zone"""
    import io, numpy as np
    from PIL import Image
    pg.set_viewport_size({'width': W, 'height': H})
    im = np.asarray(Image.open(io.BytesIO(pg.screenshot())).convert('L').resize((W // 8, H // 8)), dtype=np.float32)
    gy, gx = np.gradient(im); e = np.hypot(gx, gy)
    lo, hi = (560, 1300) if vert else (340, 780); best = None   # (2026-10-26 review 2) feet no higher than this: head + bubble stayed inside the frame, logo and top edge free
    for yc in range(lo, hi + 1, 40):
        band = e[max(0, (yc - 80) // 8):(yc + 80) // 8, 10:-10].mean() + .002 * abs(yc - (lo + hi) / 2) * (n % 2)   # mild variety between units
        if best is None or band < best[0]: best = (band, yc)
    return best[1]
SAYS = {'orbit': 'Whoa-oa-oa...', 'dizzy': 'Wooo-ooo...', 'pull': 'AAAAAH!', 'wind': 'Whooosh!', 'waves': 'Whoa-oa!', 'shiver': 'Brrrr...', 'awe': 'Woooow!', 'sleepy': 'Zzz...', 'cheer': 'Yay!', 'slide': 'Wheee!', 'nod': 'Mm-hm!', 'tilt': 'Hmm?', 'look': 'Ooh!', 'sway': 'Hum hum...', 'breathe': 'Ahh...', 'float': 'Wheee!'}
POOL = {'pull': ['AAAAAH!', 'Nooo!', 'Heeelp!', 'Whoaaa!'], 'wind': ['Whooosh!', 'Zoooom!', 'Hold on!'], 'shiver': ['Brrrr...', 'Eek...', 'Gulp.'],
        'awe': ['Woooow!', 'So big!', 'Whoa...'], 'sleepy': ['Zzz...', 'Yawn...'], 'slide': ['Wheee!', 'Down I go!', 'Whoa-oa!'], 'orbit': ['Whoa-oa-oa...', 'Round and round...'],
        'dizzy': ['Wooo-ooo...', 'So dizzy...'], 'waves': ['Whoa-oa!', 'Splash!'], 'cheer': ['Yay!', 'Got it!'], 'nod': ['Mm-hm!', 'I see!', 'Right!'], 'tilt': ['Hmm?', 'Huh?', 'Really?'],
        'look': ['Ooh!', 'Oh!', "What's that?"], 'sway': ['Hum hum...', 'La la la...'], 'breathe': ['Ahh...', 'Phew...'], 'float': ['Wheee!', 'Floaty...'],
        'hide': ["Can't look!", 'Eeek!', 'Nope nope!'], 'peek': ['Peek-a-boo!', 'Psst...', 'Who, me?'], 'hang': ['Hold on!', 'Wheee!', "Don't let go!"], 'tap': ['Knock knock!', 'Hmm, hard.', 'Tap tap.'],
        'rest': ['Ahh...', 'Safe at last.', 'Home sweet home.'], 'scope': ['I see it!', 'There!', 'Ooh, far away.'], 'wave': ['Hi there!', 'Hello!', 'Over here!'], 'startle': ['Eek!', 'Whoa!', 'Yikes!'],
        'bounce': ['Boing boing.', 'Bumpy!', 'Wobbly...'], 'lean': ['Here we go!', 'Steady...', 'Off we go!'],
        'dance': ['La la la~', 'Boom-cha!', 'Doo-doo-doo~'], 'salute': ['Aye aye!', 'Yes, captain!', 'Ready!'], 'think': ['Hmm...', 'Let me think.', 'But why?'], 'facepalm': ['Oh no...', 'Oops.', 'Not again!'],
        'idea': ['Aha!', 'I know!', 'Eureka!'], 'dig': ['Dig dig dig.', 'Almost there!', 'Found something?'], 'read': ['Interesting...', 'Page 2...', 'Let me read.'], 'eat': ['Nom nom.', 'Munch munch.', 'Yum!'],
        'cry': ['Sniff...', 'So sad...', 'Boo-hoo...'], 'photo': ['Say cheese!', 'Click!', 'Perfect shot!'], 'sneeze': ['Achoo!', 'Ah... ah... choo!', 'Sniff.'], 'clap': ['Bravo!', 'Well done!', 'Hooray!'],
        'magnify': ['A clue!', 'Hmm, interesting.', 'Look closer...'], 'snooze': ['Zzz...', 'So slow...', 'Mmm... zzz.'],
        'stretch': ['Good morning!', 'Stretch~', 'New day!'], 'shrug': ['Who knows?', 'No idea.', 'Beats me.'], 'bow': ['Thank you!', 'Much respect.', 'Honored!'], 'nervous': ['Uh-oh...', 'Gulp.', 'Careful...'],
        'flex': ['So strong!', 'Hnnng!', 'Mighty!'], 'balance': ['Steady...', 'Whoa, careful!', 'Easy does it.'], 'listen': ['Shh... listen.', 'Did you hear that?', 'Hmm?'], 'search': ['Where is it?', 'Over there?', 'Hmm, nothing.'],
        'yawn': ['Yaaawn...', 'So tired...', 'Long day.'], 'write': ['Noted!', 'Let me write that.', 'Scribble scribble.'], 'wish': ['Please...', 'I hope so!', 'Fingers crossed!'], 'faint': ['Too much...', 'Whoa... *thud*', 'I need a minute.']}   # (2026-10-26 review: "AAAAAH!" 10x, "Wheee!" 12x in one video)
CONTEXT = [(re.compile(r'\b(clocks?|ticking|ticks?|seconds?|minutes?|hours?)\b', re.I), 'Tick tock...'), (re.compile(r'\b(scales?|balance|weigh\w*)\b', re.I), 'Which way?'),
           (re.compile(r'\b(maps?|charts?|graphs?|numbers?)\b', re.I), 'Let me see...'), (re.compile(r'\b(bones?|skeleton)\b', re.I), 'Bones!')]   # calm frogs: a word about what is on screen
LAST = {'word': None, 'k': {}}
def pick_word(nm, text):
    if nm in CALM:
        for rx, w in CONTEXT:
            if rx.search(text): LAST['word'] = w; return w   # the same context word again is fine (miya 2026-10-27)
    pool = POOL.get(nm)
    if not pool: return None
    k = LAST['k'].get(nm, 0); w = pool[k % len(pool)]            # per-act rotation: the act's pool advances every time that act is used
    LAST['k'][nm] = k + 1; LAST['word'] = w; return w
CALM = ('tilt', 'look', 'sway', 'nod', 'breathe', 'tap', 'rest', 'scope', 'wave', 'bounce', 'lean', 'dance', 'salute', 'think', 'facepalm', 'idea', 'dig', 'read', 'eat', 'cry', 'photo', 'sneeze', 'clap', 'magnify', 'snooze', 'stretch', 'shrug', 'bow', 'nervous', 'flex', 'balance', 'listen', 'search', 'yawn', 'write', 'wish', 'faint')   # calm acts always get a bubble (guideline 7-2 B-1)
# ---- round 3 (2026-10-26, guideline 7-2 D "relation acts"): the frog relates to a person / an object in the picture. Keyed on unit words + group ids only,
#      so a different model, script or picture set gives the same choice. Only applied when the act so far is weak (calm / none / float / sleepy / awe / waves / cheer).
HIDEW = re.compile(r'\b(terrif\w*|horror|horrif\w*|nightmare\w*|scream\w*|gruesome|monstrous|can.?t (look|watch)|too scary|dreadful|bloody|gore)\b', re.I)
PEEKW = re.compile(r'\b(invisible|hidden|hide\w*|hiding|secret\w*|myster\w*|unknown|unseen|lurk\w*|sneak\w*|spy\w*|behind|disguise\w*|camouflag\w*)\b', re.I)
HANGW = re.compile(r'\b(hang\w*|dangl\w*|suspend\w*|balloon|cling\w*|grip\w*|hold on|hanging|swing\w*|ledge|cliff|edge of)\b', re.I)
HANGG = re.compile(r'balloon|branch|rope|wire|cable|beam|bar\b|ring|hook|ledge|cliff|ceiling|arm\b|crane|bridge|tail|fin|antenna|pole', re.I)
TAPW = re.compile(r'\b(test\w*|check\w*|examin\w*|measur\w*|press\w*|knock\w*|pok\w*|inspect\w*|sampl\w*|touch\w*|tap\w*|analy\w*|experiment\w*|scan\w*)\b', re.I)
RESTW = re.compile(r'\b(rest\w*|relax\w*|calm\w*|peace\w*|quiet\w*|gentl\w*|finally|safe\w*|comfort\w*|home\b|settle\w*|shelter\w*|warm\w*|cozy|cosy)\b', re.I)
SCOPEW = re.compile(r'\b(observ\w*|telescope\w*|astronom\w*|look(ed|ing)? up|watch(ed|ing)? the sky|search\w*|scan\w*|spot\w*|sight\w*|gaze\w*|peer\w*|far away|distant)\b', re.I)
PERSON = re.compile(r'person|people|man\b|woman|men\b|women|kid|child|boy|girl|astronaut|scientist|researcher|doctor|officer|villager|figure|human|farmer|worker|crowd|caretaker|observer|diver\b|sailor|crew', re.I)
LABW = re.compile(r'\b(lab|laboratory|experiment\w*|scientist\w*|researcher\w*|microscope\w*|test tube|petri|sample\w*|chemist\w*|biolog\w*|physicist\w*|study|studies)\b', re.I)
EXPLW = re.compile(r'\b(expedition\w*|explor\w*|jungle|desert|island\w*|mountain\w*|trek\w*|safari|cave\w*|wilderness|highlands?|trail\w*|voyage\w*)\b', re.I)
SCARFW = re.compile(r'\b(freez\w*|frozen|ice|icy|snow\w*|cold|colder|winter|arctic|antarctic\w*|glacier\w*|frost\w*|chill\w*)\b', re.I)
NIGHTW = re.compile(r'\b(sleep\w*|asleep|dream\w*|bed\w*|nap|yawn\w*|midnight|bedtime|drows\w*|slumber\w*)\b', re.I)
LOVEW = re.compile(r'\b(beautiful|lovely|favou?rite|ador\w*|love\w*|wonderful|delicious|gorgeous|precious|cute|charming)\b', re.I)
SHOCKW = re.compile(r'\b(shock\w*|unbelievabl\w*|suddenly|boom|explod\w*|burst\w*|what\?|wait\b|gasp\w*|stunn\w*|astonish\w*|incredibl\w*)\b', re.I)
ANGRYW = re.compile(r'\b(war\b|wars\b|fight\w*|attack\w*|villain\w*|enem\w*|greed\w*|cruel\w*|unfair|cheat\w*|steal\w*|stolen|thie\w*|rob\w*|furious|rage)\b', re.I)
POPG = re.compile(r'mv-(core-(pop|ping|stamp|drop|flicker)|popin)', re.I)
PULSEG = re.compile(r'mv-(core-(heartbeat|swell|wobble)|liquid|bubble)', re.I)
TRAVELG = re.compile(r'mv-(core-(glide|approach)|path|slide)', re.I)
# ---- round 4 (2026-10-26, miya: more motions / costumes ready for any script). Acts by narration words; outfits by narration words. Guideline 7-2 D / E.
DANCEW = re.compile(r'\b(music\w*|song\w*|sing\w*|danc\w*|rhythm\w*|melod\w*|drum\w*|beat\b|concert|orchestra|tune\b|hum\w*)\b', re.I)
SALUTEW = re.compile(r'\b(mission\w*|captain\w*|commander\w*|army|soldier\w*|navy|crew\b|launch\w*|general\b|officer\w*|admiral|pilot\w*|command\b|order(s|ed)\b)\b', re.I)
THINKW = re.compile(r'\b(why\b|question\w*|wonder\w*|puzzl\w*|riddle\w*|paradox\w*|debate\w*|theor\w*|hypothes\w*|philosoph\w*|thought experiment|imagine|suppose)\b', re.I)
FACEW = re.compile(r'\b(mistake\w*|wrong\b|fail\w*|error\w*|oops|blunder\w*|forgot\w*|disaster\w*|embarrass\w*|miscalculat\w*|backfire\w*|flaw\w*)\b', re.I)
IDEAW = re.compile(r'\b(idea\w*|realiz\w*|realis\w*|eureka|figured out|insight\w*|invent\w*|solution\w*|clever|breakthrough\w*|aha\b|brilliant)\b', re.I)
DIGW = re.compile(r'\b(dig\w*|dug\b|fossil\w*|excavat\w*|archaeolog\w*|paleontolog\w*|buried|unearth\w*|tomb\w*|sediment\w*|layers? of rock|underground)\b', re.I)
READW = re.compile(r'\b(read\w*|books?|pages?|chapter\w*|librar\w*|diar\w*|letters?|manuscript\w*|documents?|written|writing\w*|journal\w*|scroll\w*|text\b|archive\w*)\b', re.I)
EATW = re.compile(r'\b(eat\w*|ate\b|food\w*|meal\w*|hungry|hunger|feast\w*|dinner|lunch|breakfast|tast\w*|delicious|calorie\w*|cook\w*|recipe\w*|chew\w*|swallow\w*|snack\w*|diet\w*)\b', re.I)
CRYW = re.compile(r'\b(died|die\b|dies\b|dying|death\w*|extinct\w*|gone forever|farewell|goodbye|mourn\w*|grie\w*|tragic\w*|funeral\w*|perish\w*|last of (its|their) kind|never (came|come) back)\b', re.I)
PHOTOW = re.compile(r'\b(photo\w*|camera\w*|pictures?|images?|snapshot\w*|footage|film\w*|portrait\w*|selfie\w*|photograph\w*)\b', re.I)
SNEEZEW = re.compile(r'\b(dust\w*|pollen|sneez\w*|allerg\w*|pepper|spores?|ash\b|ashes|smoke\w*|soot)\b', re.I)
CLAPW = re.compile(r'\b(applau\w*|congratulat\w*|bravo|success\w*|achiev\w*|triumph\w*|victor\w*|won\b|winner\w*|celebrat\w*|well done|record-breaking|prize\w*|award\w*|medal\w*)\b', re.I)
MAGW = re.compile(r'\b(clue\w*|evidence|investigat\w*|detective\w*|examin\w*|inspect\w*|microscop\w*|tiny|microscopic|trace\w*|fingerprint\w*|close(r|ly)? look|zoom in)\b', re.I)
SNOOZEW = re.compile(r'\b(boring|bored|wait(ed|ing)?|hours? pass\w*|slowly|centuries pass\w*|nothing happen\w*|idle|dull|yawn\w*)\b', re.I)
OUTFIT_WORDS = [('crown', r'\b(king\w*|queen\w*|royal\w*|empire\w*|emperor\w*|throne\w*|pharaoh\w*|monarch\w*|prince\w*|princess\w*|kingdom\w*|crown\w*)\b'),
                ('knight', r'\b(knight\w*|battle\w*|castle\w*|medieval|sword\w*|armou?r\w*|siege\w*|warrior\w*|war\b|wars\b)\b'),
                ('pirate', r'\b(pirate\w*|treasure\w*|sail\w*|ship\w*|voyage\w*|harbou?r\w*|galleon\w*|captain\w*)\b'),
                ('doctor', r'\b(doctor\w*|disease\w*|virus\w*|hospital\w*|medic\w*|infect\w*|plague\w*|sick\w*|surgeon\w*|patient\w*|epidemic\w*|pandemic\w*|vaccine\w*)\b'),
                ('chef', r'\b(cook\w*|recipe\w*|kitchen\w*|chef\w*|bak\w*|dish\w*|cuisine|ingredient\w*)\b'),
                ('hardhat', r'\b(build\w*|construct\w*|engineer\w*|bridge\w*|tower\w*|machine\w*|factor(y|ies)|crane\w*|dam\b|tunnel\w*|skyscraper\w*|concrete)\b'),
                ('headphones', r'\b(music\w*|sound\w*|song\w*|listen\w*|radio\w*|signal\w*|frequenc\w*|noise\w*|audio|echo\w*)\b'),
                ('gradcap', r'\b(school\w*|learn\w*|student\w*|teacher\w*|lesson\w*|exam\w*|universit\w*|graduat\w*|professor\w*|classroom\w*|homework)\b'),
                ('strawhat', r'\b(farm\w*|harvest\w*|wheat|crop\w*|field\w*|plant\w*|seed\w*|garden\w*|orchard\w*|cattle|cows?)\b'),
                ('umbrella', r'\b(rain\w*|storm\w*|downpour|monsoon|drizzl\w*|umbrella\w*|wet\b|flood\w*)\b'),
                ('sunglasses', r'\b(sun\b|sunny|sunlight|sunshine|beach\w*|desert\w*|heat\w*|hot\b|hotter|bright\w*|glare|summer|tropical)\b'),
                ('partyhat', r'\b(part(y|ies)|celebrat\w*|birthday\w*|festival\w*|anniversar\w*|holiday\w*|new year|confetti|parade\w*)\b'),
                ('wizard', r'\b(magic\w*|wizard\w*|myth\w*|legend\w*|spell\w*|witch\w*|fairy|dragon\w*|sorcer\w*|enchant\w*|alchem\w*)\b'),
                ('detective', r'\b(clue\w*|detective\w*|evidence|investigat\w*|mystery|mysteries|solve\w*|suspect\w*|case\b|sleuth\w*)\b')]
OUTFIT_WORDS += [('tophat', r'\b(gentlem[ae]n|victorian|19th century|magician\w*|formal|top hat|aristocra\w*)\b'),
                 ('beret', r'\b(art\b|arts\b|artist\w*|paint\w*|sculpt\w*|museum\w*|gallery|canvas|paris|french)\b'),
                 ('cowboy', r'\b(cowboy\w*|wild west|ranch\w*|rodeo|frontier\w*|texas|saloon|lasso\w*)\b'),
                 ('bandana', r'\b(rebel\w*|bandit\w*|outlaw\w*|mechanic\w*|workshop\w*|garage\w*|treasure hunt\w*)\b'),
                 ('flowercrown', r'\b(spring\w*|bloom\w*|blossom\w*|meadow\w*|flowers?|petal\w*|pollen)\b'),
                 ('alien', r'\b(alien\w*|extraterrestrial\w*|ufo\w*|martian\w*|life beyond|little green)\b'),
                 ('bunny', r'\b(rabbit\w*|bunny|bunnies|hare\b|hares\b|easter|hop(s|ped|ping)?\b)\b'),
                 ('santa', r'\b(christmas|santa|gift\w*|present(s|ed)?\b|december|reindeer|sleigh)\b'),
                 ('bowtie', r'\b(ceremon\w*|dinner part\w*|elegan\w*|fancy|gala|opera|tuxedo|banquet\w*|butler\w*)\b'),
                 ('cape', r'\b(hero\w*|superhero\w*|rescue\w*|sav(e|ed|ing) (the|a|his|her|their)|brave\w*|courage\w*|defend\w*)\b'),
                 ('backpack', r'\b(hik\w*|trek\w*|journey\w*|travel\w*|camp\w*|backpack\w*|trail\w*|wander\w*|pilgrim\w*)\b'),
                 ('lifevest', r'\b(lifeboat\w*|shipwreck\w*|overboard|drown\w*|rescue at sea|sink(s|ing)? ship|capsiz\w*|flood\w*|titanic)\b'),
                 ('raincoat', r'\b(wet\b|puddle\w*|slipper\w*|soak\w*|drench\w*|damp|mud\w*|swamp\w*)\b'),
                 ('beanie', r'\b(chill\w*|autumn|fall season|cozy|cosy|knit\w*|crisp air|frosty morning)\b'),
                 ('halo', r'\b(angel\w*|heaven\w*|saint\w*|holy|sacred|afterlife|blessed|divine|god\b|gods\b|goddess\w*)\b'),
                 ('ghost', r'\b(ghost\w*|haunt\w*|spirit\w*|spooky|halloween|phantom\w*|undead|zombie\w*)\b'),
                 ('viking', r'\b(viking\w*|norse|longship\w*|raid\w*|scandinavia\w*|valhalla)\b'),
                 ('roman', r'\b(rome|roman\w*|legion\w*|gladiator\w*|caesar|colosseum|centurion\w*)\b'),
                 ('samurai', r'\b(samurai|japan\w*|shogun\w*|katana|edo|ninja\w*)\b'),
                 ('headlamp', r'\b(mine\b|mines\b|miner\w*|cavern\w*|tunnel\w*|underground|pitch[- ]black|cave\w*)\b'),
                 ('firefighter', r'\b(firefight\w*|blaze\w*|hose\w*|wildfire\w*|put out the fire|fire brigade|fire truck)\b'),
                 ('police', r'\b(police|crime\w*|arrest\w*|jail\w*|prison\w*|guard\w*|patrol\w*|sheriff\w*|law enforcement)\b'),
                 ('aviator', r'\b(fly|flies|flying|flight\w*|pilot\w*|aviat\w*|airplane\w*|aircraft|wright brothers|cockpit)\b'),
                 ('monocle', r'\b(rich\w*|wealth\w*|aristocra\w*|lord\w*|banker\w*|fortune\w*|millionaire\w*|billionaire\w*|luxur\w*|tycoon\w*)\b'),
                 ('glasses', r'\b(expert\w*|professor\w*|research\w*|intellect\w*|genius\w*|scholar\w*|philosoph\w*|mathematic\w*|calculat\w*)\b'),
                 ('medal', r'\b(champion\w*|olympi\w*|gold medal\w*|world record\w*|winner\w*|first place|trophy|trophies)\b'),
                 ('laurel', r'\b(greece|greek\w*|ancient|athens|sparta\w*|poet\w*|olympus|plato|aristotle|socrates)\b'),
                 ('propcap', r'\b(toy\w*|play\w*|kid\w*|child\w*|playground\w*|cartoon\w*|games?\b|puppet\w*)\b'),
                 ('headband', r'\b(sport\w*|run(s|ner|ners|ning)?\b|race\w*|marathon\w*|exercis\w*|athlet\w*|training|gym|sprint\w*|jog\w*)\b'),
                 ('vr', r'\b(virtual|simulat\w*|digital|computer\w*|software|cyber\w*|\bai\b|robot\w*|algorithm\w*|internet|online|video game\w*)\b'),
                 ('tinfoil', r'\b(conspirac\w*|hoax\w*|skeptic\w*|sceptic\w*|paranoi\w*|rumou?r\w*|myth busted|fake)\b'),
                 ('bandage', r'\b(injur\w*|hurt\w*|wound\w*|accident\w*|broken (leg|arm|bone)|bruis\w*|pain\w*|scar\w*)\b'),
                 ('dino', r'\b(dinosaur\w*|jurassic|t\.? ?rex|prehistoric|cretaceous|triassic|velociraptor\w*)\b'),
                 ('shark', r'\b(shark\w*|predator\w*|jaws)\b'),
                 ('bee', r'\b(bees?\b|honey\w*|pollinat\w*|hive\w*|insect\w*|bugs?\b|wasp\w*|beetle\w*)\b'),
                 ('clown', r'\b(funny|jok\w*|comed\w*|laugh\w*|silly|prank\w*|circus\w*|hilarious|giggl\w*)\b'),
                 ('mustache', r'\b(mustache\w*|moustache\w*|old days|grandpa|grandfather\w*|elder\w*|19th|1800s|1900s|century ago)\b'),
                 ('earmuffs', r'\b(loud\w*|nois\w*|deafen\w*|roar\w*|thunder\w*|blast\w*|decibel\w*)\b'),
                 ('turtle', r'\b(turtle\w*|tortoise\w*|shell\w*|slow and steady|armou?r\w*)\b'),
                 ('wings', r'\b(wings?\b|fairy|fairies|butterfl\w*|angel\w*|flutter\w*|moth\w*)\b'),
                 ('crownleaf', r'\b(autumn leaves|harvest festival|thanksgiving|forest king|woodland\w*|druid\w*)\b')]
OUTFIT_WORDS = [(n, re.compile(rx, re.I)) for n, rx in OUTFIT_WORDS]
# round 4b acts by words (checked after the task acts, before 'wave'): (act, regex, mood)
ACT_WORDS2 = [('stretch', r'\b(morning\w*|wak(e|es|ing|ened)\b|woke|dawn\w*|sunrise|a new day|fresh start)\b'),
              ('shrug', r'\b(nobody knows|no one knows|uncertain\w*|unknown|not sure|who knows|we don.?t know|remains? a mystery|unclear|debated)\b'),
              ('bow', r'\b(thank\w*|respect\w*|hono\w*|greet\w*|welcome\w*|tribute\w*|salute\w*|curtain call|applaud\w*)\b'),
              ('nervous', r'\b(nervous\w*|anxious\w*|pressure|deadline\w*|danger\w*|risk\w*|tense|tension|stress\w*|worr\w*|hold your breath)\b'),
              ('flex', r'\b(strong\w*|strength|power\w*|muscle\w*|mighty|force\w*|lift\w*|heav(y|ier|iest)|robust|tough)\b'),
              ('balance', r'\b(balanc\w*|tightrope|careful\w*|on the edge|delicate|fragile|equilibrium|steady|stabl\w*)\b'),
              ('listen', r'\b(hear\w*|listen\w*|whisper\w*|signal\w*|echo\w*|sound\w*|voice\w*|noise\w*|radio)\b'),
              ('search', r'\b(lost\b|missing|search\w*|look(ed|ing)? for|where (is|are|did|was)|hunt(ed|ing)? for|seek\w*|scour\w*|track(ed|ing)? down)\b'),
              ('yawn', r'\b(tired|exhaust\w*|sleepless|all night|long night|weary|fatigue\w*|drows\w*)\b'),
              ('write', r'\b(wrote|writ(e|es|ing|ten)\b|not(e|es|ed|ing)\b|calculat\w*|equation\w*|formula\w*|record(ed|ing)?\b|list(ed|ing)?\b|journal\w*|diar\w*)\b'),
              ('wish', r'\b(hop(e|es|ed|ing)\b|wish\w*|pray\w*|dream\w*|long(ed|ing)? for|yearn\w*|please let|fingers crossed)\b'),
              ('faint', r'\b(faint\w*|collaps\w*|overwhelm\w*|pass(ed|es)? out|knock(ed)? out|too much|dizzy|exhausted|staggering|mind-?blowing|mind-?boggling)\b')]
ACT_WORDS2 = [(a, re.compile(rx, re.I)) for a, rx in ACT_WORDS2]
ACT_MOOD2 = {'stretch': 'sleepy', 'shrug': 'worried', 'bow': 'proud', 'nervous': 'worried', 'flex': 'proud', 'balance': 'squint', 'listen': 'curious', 'search': 'squint', 'yawn': 'sleepy', 'write': 'curious', 'wish': 'love', 'faint': 'dizzy'}
WEAK = ('float', 'sleepy', 'awe', 'waves', 'cheer', 'nod', None)
STRONG = ('pull', 'shiver', 'awe', 'wind', 'orbit', 'dizzy', 'slide', 'hide', 'peek', 'hang', 'startle')   # always get a sound word; the other acts every second unit (miya 2026-10-26: speech bubble with emotion / sound words)
def says_for(act, keep, text, cnt):
    nm = act.get('type') if isinstance(act, dict) else act
    rm = (keep.get('roam') or {}).get('kind')
    word = pick_word(nm, text) if nm in POOL else SAYS.get(nm)
    if rm == 'roll': word = 'Waaaah!'
    elif rm in ('swim', 'lie', 'tumble'): word = 'Blub blub!' if keep.get('outfit') in (['diver'], ['goggles']) else 'Wheee!'
    elif rm == 'run': word = 'Hop hop!'
    elif rm == 'moonhop': word = 'Boing!'
    elif rm == 'walk' and word is None: word = 'Hmm?' if keep['moods'][0]['mood'] == 'curious' else 'Tada!'
    if word is None: return []
    if nm not in STRONG and nm not in CALM and cnt % 2: return []   # a calm default frog always gets a bubble (miya 2026-10-26: no meaningless frogs sitting on objects)
    return [{'text': word, 'shout': word.endswith('!') and nm in STRONG}]
HEAT = re.compile(r'\b(heat\w*|hot|furnace|kiln|fire|flames?|burn\w*|boil\w*|scorch\w*|molten|lava|magma|sizzl\w*|celsius|oven|sun)\b', re.I)   # miya 2026-10-26: overheated = woozy swirl eyes
FORE = re.compile(r'\b(fore people|papua|highlands?|villag\w*|tribe|tribal|clan|huts?|funeral\w*|mourn\w*|indigenous)\b', re.I)   # people-of-the-place scenes: native outfit
BOOK = re.compile(r'book|notebook|page|paper|diary|desk|chart|board|card', re.I)
NOTE = re.compile(r'\b(notebook|book|pages?|writ\w*|wrote|draw\w*|sketch\w*|pencil|notes?|records?|report|paper|diary|study|studies|research\w*)\b', re.I)
PUSHG = re.compile(r'lens|magnif|cart|crate|box|rock|stone|boulder|sled|wheel|barrow|wagon|anvil|weight', re.I)   # a movable object the frog can heave (holds the handle of a lens)
VILL = re.compile(r'\b(villag\w*|huts?|houses?|homes?|funeral\w*|rituals?|feast\w*)\b', re.I)
SERIOUS_OUT = ('Yay!', 'Tada!', 'Wheee!', 'Hop hop!', 'Boing!', 'Got it!', 'Down I go!', 'La la la...', 'Floaty...', 'Bones!')
PLAT = re.compile(r'belt|treadmill|tread\b|slats|ground|ledge|platform|bridge|shelf|deck|road|planet|moon|surface|floor|stage|track', re.I)
ACTIVE = re.compile(r'\b(run\w*|walk\w*|jump\w*|hop\w*|step\w*|treadmill|pump\w*|race|racing|sprint\w*)\b', re.I)
VEH = re.compile(r'\b(rocket|spaceship|spacecraft|ship|probe|warp drive|shuttle|lander)\b', re.I)
ROLL = re.compile(r'\b(drag\w*|spiral\w*|tumbl\w*|roll\w*|carried|swept|backward|whirl\w*|swirl\w*|knock\w*)\b', re.I)
ORBIT = re.compile(r'\b(particles?|orbit\w*|circl\w*|revolv\w*|accretion|ring|rings|disk|laser|radio wave)\b', re.I)
HOLE = re.compile(r'hole|bh|singular|well|horizon', re.I)
JS = '''()=>{const o=[];for(const g of document.querySelectorAll('g[id^="mv-"]')){const b=g.getBBox();if(b.width<8)continue;o.push([g.id,b.x,b.y,b.width,b.height])}return o}'''
JSD = '''()=>{const o=[];for(const g of document.querySelectorAll('[id^="door"]')){const b=g.getBBox();if(b.width<4)continue;o.push([b.x+b.width/2,b.y+b.height])}o.sort((a,c)=>a[0]-c[0]);return o}'''
JST = '''()=>[...document.querySelectorAll('text')].map(t=>{const r=t.getBoundingClientRect();return [r.left,r.top,r.width,r.height]}).filter(r=>r[2]>4)'''
JSS = '''([id,x,y0,y1])=>{const g=document.getElementById(id),m=g&&g.getScreenCTM();if(!m)return null;for(let y=y0;y<=y1;y+=3){const p=new DOMPoint(x,y).matrixTransform(m);for(const e of document.elementsFromPoint(p.x,p.y)){if(e.closest&&e.closest('[id="'+id+'"]')&&e.tagName!=='g')return y}}return null}'''   # x, y in the group's own coordinates
def hits(box, tb):   # overlap area of a box (x0, y0, x1, y1) with the picture's text boxes
    return sum(max(0, min(box[2], a + c) - max(box[0], a)) * max(0, min(box[3], b + d) - max(box[1], b)) for a, b, c, d in tb)
MOVING = re.compile(r'^mv-(slide|path)')   # groups that travel during the unit: the frog is placed on / beside them relative to their START box, so keep it on the side toward the screen centre (the object ends near an edge)
def beside(g, W, H, vert, tb):
    """a calm frog (no strong situation) does not sit on top of the object: it stands beside it at its foot, facing it and looking at it (2026-10-26 review)"""
    _, x, y, w, h = g; s = round(.95 * (1.15 if vert else 1), 2); best = None
    order = (-1, 1) if (x + w / 2) < W / 2 else (1, -1)
    if MOVING.match(g[0]): order = order[::-1]
    for side in order:
        fx = x - 40 * s if side < 0 else x + w + 40 * s; fy = max(min(y + h, H - (500 if vert else 290)), 82 * s + 150)
        if not (.1 * W <= fx <= .9 * W): continue
        sc = hits((fx - 45 * s, fy - 100 * s, fx + 45 * s, fy), tb)
        if best is None or sc < best[0]: best = (sc, fx, fy, side)
    if best is None: return None
    return dict(x=round(best[1]), y=round(best[2]), s=s, flip=-best[3], bside=best[3], gaze=1)   # gaze: pupils toward the object it faces
def perch(pg, g, W, H, vert, tb, n):
    """(2026-10-26 review) where a riding frog sits: NOT on top of the middle of the object (it hid the focal point), but on the end of the object nearer
    the screen edge, feet on the drawn surface (scanned from the page), small; the other end when that one covers on-screen text"""
    _, x, y, w, h = g; s = round(min(1.25, max(.8, w / 230)) * (1.15 if vert else 1), 2)
    if w < 260 or h < 90: return beside(g, W, H, vert, tb)   # a small object (a star, a photon, a watch): on its end = on its middle, so stand beside it instead
    ends = [.2, .8] if (x + w / 2) < W / 2 else [.8, .2]
    if MOVING.match(g[0]): ends = ends[::-1]
    best = None
    for f in ends:
        fx = x + w * f; fy = pg.evaluate(JSS, [g[0], round(fx), round(max(0, y - 4)), round(y + h)])
        if fy is None or not (.12 * W <= fx <= .88 * W): continue
        if fx > .74 * W and (fy or 0) < (430 if not vert else 520): continue   # the channel logo sits top-right   # no drawn surface there, or too near the frame edge (the drift camera crops it)
        fy = fy + 4 * s
        fy = max(fy, 82 * s + 150); bub = 1 if fx < W / 2 else -1   # head + bubble inside the frame (top crop of the drift camera, logo)
        box = (fx - 45 * s, fy - 100 * s, fx + 45 * s, fy); bbox = (fx + (0 if bub > 0 else -200), fy - 100 * s - 90, fx + (200 if bub > 0 else 0), fy - 100 * s)
        sc = hits(box, tb) * 3 + hits(bbox, tb)
        if best is None or sc < best[0]: best = (sc, round(fx), round(fy), bub)
        if sc == 0: break
    if best is None: return None
    return dict(x=best[1], y=best[2], s=s, flip=1 if best[1] < W / 2 else -1, bside=best[3])
# ---- 2026-10-29 (miya: "the frog itself is too static; let it meet the objects: an apple drops on it and it keels over"): contact acts keyed on the
# motion name + size of a picture group, locomotion acts keyed on words (+ a group when they need one), costume acts keyed on the outfit. frog_rig.py
# has the motions; the times come from frog_rig.obj_span so the bubble and the impact agree. Guideline 7-2 G. ----
CATCHW = re.compile(r'\b(catch\w*|caught|grab\w*|hold(s|ing)? (it|on to)|sav(e|ed|ing)|rescu\w*|keep\w* (it|them) safe)\b', re.I)
CHASEW = re.compile(r'\b(chas\w*|follow\w*|after (it|them|him|her)|escap\w*|fle[ed]\w*|run(s|ning)? away|runaway|pursu\w*|hunt(s|ed|ing)?\b|catch up|got away|slipp\w* away)\b', re.I)
BLOWW = re.compile(r'\b(wind\w*|gust\w*|storm\w*|blast\w*|hurricane\w*|typhoon\w*|gale\w*|breez\w*|blow(s|n|ing)?\b|tornado\w*|blizzard\w*)\b', re.I)
TUGW = re.compile(r'\b(pull\w*|tug\w*|haul\w*|tow(ed|ing)?\b|anchor\w*|rope\w*|reel\w*|leash\w*|drag\w*|yank\w*)\b', re.I)
LIFTW = re.compile(r'\b(heav(y|ier|iest)|lift\w*|carr(y|ied|ying)|rais\w*|weight\w*|load\w*|hoist\w*|tons?\b|kilogram\w*|pounds)\b', re.I)
ROPEG = re.compile(r'rope|chain|cable|leash|tether|lasso|line\b|cord|string|vine|anchor', re.I)
LOWG = re.compile(r'rock|stone|pebble|root|log\b|stick|branch|wire|cable|crack|hole|puddle|bump|brick|shell|bone|skull|coin|book', re.I)
SWIMW = re.compile(r'\b(swim\w*|swam|swum|strokes?\b|paddl\w*|breaststroke|laps?\b|wad(e|ed|ing)|cross(ed|ing)? the (river|lake|channel|sea))\b', re.I)
CLIMBW = re.compile(r'\b(climb\w*|clamber\w*|scal(e|ed|ing) (the|a|up)|ascend\w*|up the (rope|pole|tree|ladder|cliff|wall|mast|tower)|summit\w*|mountaineer\w*)\b', re.I)
CLIMBG = re.compile(r'rope|pole|tree|trunk|ladder|cliff|wall|tower|mast|vine|column|pillar|post|stalk|beanstalk|chain|rock', re.I)
LEAPW = re.compile(r'\b(leap\w*|jump\w*|hop\w* (over|across)|bound(ed|ing)? (over|across)|vault\w*|across the (gap|river|stream|chasm|canyon|crack)|gap\b|chasm|ravine|canyon)\b', re.I)
DANGLEW = re.compile(r'\b(slip\w*|lost (his|her|their|its) grip|let go|dangl\w*|cling\w*|hold(s|ing)? on|hanging (by|on|from)|hung (by|on|from)|grip\w*)\b', re.I)
SKATEW = re.compile(r'\b(skat\w*|glid\w*|slid(e|es|ing) (on|across|over)|slippery|frozen (lake|pond|river|sea)|ice rink|on the ice|sled\w*|ski\w*)\b', re.I)
SOMERW = re.compile(r'\b(somersault\w*|back ?flip\w*|front ?flip\w*|acrobat\w*|cartwheel\w*|gymnast\w*|stunt\w*|show(s|ed|ing)? off|trick\w*|circus)\b', re.I)
SNEAKW = re.compile(r'\b(sneak\w*|tiptoe\w*|creep\w*|crept|quietly|silently|stealth\w*|spy\w*|spied|prowl\w*|in secret|unnoticed|undetected)\b', re.I)
CRAWLW = re.compile(r'\b(crawl\w*|tunnel\w*|burrow\w*|squeez\w* (through|under|into)|narrow (passage|gap|crack|tunnel)|on all fours|wriggl\w*|through the (pipe|vent|hole|gap))\b', re.I)
TIGHTW = re.compile(r'\b(tightrope|high ?wire|balanc\w* (on|along|across)|narrow (beam|ledge|bridge|plank)|careful steps|one wrong step|inch(ed|ing)? (along|across))\b', re.I)
TIGHTG = re.compile(r'rope|wire|beam|ledge|plank|bridge|line\b|rail|branch|cable', re.I)
CONTACT_SAYS = {'bonk': ['Bonk!', 'Ouch...'], 'squish': ['Oof!', 'Ow ow ow.'], 'dodge': ['Whoa!'], 'chase': ['Wait!'], 'splash': ['Splash!'], 'swingride': ['Wheee!'], 'bumped': ['Boing!'],
                'blown': ['Whoaaa!'], 'tug': ['Hnnng...', 'Oof!'], 'lift': ['Hnnng!'], 'catch': ['Got it!'], 'trip': ['Oof!'],
                'sidestep': ['Phew!'], 'flattened': ['Oof!', 'Ow ow ow.'], 'trampoline': ['Boing!'], 'knocked': ['Bonk!'], 'shockwave': ['Yikes!'], 'magnetized': ['Whoa-oa!'], 'hopalong': ['Hop hop!'],
                'dripped': ['Drip...'], 'rimride': [], 'launched': ['Whoa!'], 'unrolled': ['Whoa!'], 'balloonride': ['Up, up!'], 'sinkride': ['Help!']}
CONTACT_MOOD = {'bonk': 'curious', 'squish': 'happy', 'dodge': 'happy', 'chase': 'determined', 'splash': 'curious', 'swingride': 'excited', 'bumped': 'surprised', 'blown': 'squint', 'tug': 'determined', 'lift': 'determined', 'catch': 'determined', 'trip': 'happy',
                'sidestep': 'curious', 'flattened': 'curious', 'trampoline': 'excited', 'knocked': 'curious', 'shockwave': 'curious', 'magnetized': 'curious', 'hopalong': 'happy', 'dripped': 'curious',
                'rimride': 'excited', 'launched': 'curious', 'unrolled': 'curious', 'balloonride': 'excited', 'sinkride': 'worried'}
SIDESTEPW = re.compile(r'\b(avoid\w*|miss(ed|es)?\b|dodg\w*|escap\w*|narrow\w*|close call|just in time|in time|safe\w*|luck\w*|survived?)\b', re.I)   # 2026-10-29 b: the frog steps aside instead of taking the hit
BOUNCEW = re.compile(r'\b(bounc\w*|jump\w*|spring\w*|trampolin\w*|boing|hop\w*|leap\w*)\b', re.I)
HEAVYG = re.compile(r'anvil|boulder|rock|stone|crate|weight|piano|safe\b|block|meteor|meteorite|asteroid|barrel|box|chest|log\b|trunk', re.I)   # (whale/elephant/tree names never reach core-drop: motions.core_sanitize turns their drop into swell)
WHEELG = re.compile(r'wheel|gear|cog|fan\b|windmill|ferris|turntable|disc|disk|record|carousel|propeller|rotor|tire|tyre|roulette|millstone|waterwheel', re.I)


def gattrs(svgtxt, gid):
    m = re.search(rf'<g\b[^>]*\bid="{re.escape(gid)}"[^>]*>', svgtxt)
    return dict(re.findall(r'(data-[a-z]+)="([^"]*)"', m.group(0))) if m else {}


def gkind(gid, at):
    """motion kind of a picture group after the round-4 sanity (the same the build applies)"""
    if gid.startswith('mv-core-'): return 'core-' + motions.core_sanitize(gid[8:].split('-')[0], gid, keep=at.get('data-keep') == '1')
    if gid.count('-') >= 2 and gid.split('-')[1] in motions.OBJ_KINDS: return motions.obj_sanitize(gid.split('-')[1], gid, keep=at.get('data-keep') == '1')
    return ''


def set_act(keep, ty, says=None, mood=None, **kw):
    keep['act'] = dict(type=ty, **kw)
    words = says if says is not None else CONTACT_SAYS.get(ty) or ([frog_rig.OUTFIT_SAYS[ty]] if ty in frog_rig.OUTFIT_SAYS else [])
    keep['_says'] = [{'text': w, 'shout': w.endswith('!')} for w in words]
    keep['moods'][0] = {'mood': mood or CONTACT_MOOD.get(ty, frog_rig.COSTUME_ACTS.get(ty, {}).get('mood', 'happy'))}; keep.pop('roam', None); keep.pop('cling', None)


def contact_pick(keep, text, gs, svgtxt, palname, W, H, vert, tb):
    """a moving object the frog can meet: returns True and fills keep (kind / x / y / s / flip / act / _says). Deterministic: first rule that fits."""
    cap = H - (460 if vert else 290); s0 = round(.95 * (1.15 if vert else 1), 2); water = palname == 'ocean' or has_group(gs, WATER_G, .2, W, H)
    objs = []
    for g in gs.values():
        at = gattrs(svgtxt, g[0]); kd = gkind(g[0], at)
        if kd: objs.append((g, kd, at))
    objs.sort(key=lambda o: -o[0][3] * o[0][4])
    space = bool(SPACE.search(text)) or palname in SPACE_PAL   # nothing lands, rolls or topples in space: no ground gags there
    for g, kd, at in objs:
        gid, x, y, w, h = g; cx = x + w / 2; side = 1 if cx < W / 2 else -1   # side: +1 = the frog stands to the right of the object (nearer the centre)
        if gid == keep.get('ride') or SPACE_RIDE.search(gid) or VEH.search(gid): continue   # a vehicle the frog rides (or could ride) is better ridden than dodged (edge-of-universe U007: Voyager)
        if space and kd in ('core-drop', 'topple', 'rollby', 'slide', 'bouncing'): continue
        if kd == 'core-drop' and w <= 260 and h <= 220:
            if CATCHW.search(text) and y + h + 42 * s0 <= cap:
                keep.update(kind='bg', ride=None, behind=None, x=round(cx), y=round(y + h + 42 * s0), s=s0, flip=side, enter='cut', delay=.02); set_act(keep, 'catch', obj=gid); return True
            if water and .1 * W < cx + side * (w / 2 + 62 * s0) < .9 * W and y + h <= cap:
                keep.update(kind='bg', ride=None, behind=None, x=round(cx + side * (w / 2 + 62 * s0)), y=round(y + h), s=s0, flip=-side, enter='cut', delay=.02); set_act(keep, 'splash', obj=gid); return True
            if not SERIOUS and y + h + 80 * s0 <= cap:
                ty_ = 'sidestep' if SIDESTEPW.search(text) else 'bonk'
                keep.update(kind='bg', ride=None, behind=None, x=round(cx), y=round(y + h + 80 * s0), s=s0, flip=side, enter='cut', delay=.02); set_act(keep, ty_, obj=gid); return True
        elif kd == 'core-drop' and (w > 260 or h > 220) and w <= 700 and h <= 600 and not SERIOUS and HEAVYG.search(gid) and y + h + 80 * s0 <= cap:   # a big heavy thing: pancaked under it
            keep.update(kind='bg', ride=None, behind=gid, x=round(cx), y=round(y + h + 80 * s0), s=s0, flip=side, enter='cut', delay=.02); set_act(keep, 'flattened', obj=gid, out=round(w / 2 + 70 * s0)); return True
        elif kd == 'topple' and 120 <= h <= 600 and w <= 400 and not SERIOUS and float(at.get('data-deg', 72)) > 0:
            fx = x + w + h * .5
            if .08 * W < fx < .92 * W and y + h <= cap + 20:
                keep.update(kind='bg', ride=None, behind=gid, x=round(fx), y=round(min(y + h, cap)), s=s0, flip=-1, enter='cut', delay=.02); set_act(keep, 'squish', obj=gid); return True
        elif kd in ('rollby', 'slide') and y + h <= cap + 30 and h >= 40:
            a, b = frog_rig.travel(kd, at, (x, y, w, h))
            if abs(b - a) < 150: continue
            dirx = 1 if b > a else -1; lane = round(min(y + h, cap))
            if CHASEW.search(text) or h > 240:
                fx = a - dirx * (w / 2 + 60 * s0)
                if not (.06 * W < fx < .94 * W): continue
                dist = min(abs(b - a) * .8, (W * .94 - fx) if dirx > 0 else (fx - W * .06))
                keep.update(kind='bg', ride=None, behind=None, x=round(fx), y=lane, s=s0, flip=dirx, enter='cut', delay=.02); set_act(keep, 'chase', obj=gid, dist=round(dist)); return True
            if not SERIOUS:
                P = a + .62 * (b - a)
                if not (.1 * W < P < .9 * W): continue
                keep.update(kind='bg', ride=None, behind=None, x=round(P), y=lane, s=s0, flip=-dirx, enter='cut', delay=.02)
                set_act(keep, 'dodge', obj=gid, h=round(h), **{'pass': round(frog_rig.pass_time(kd, at, (x, y, w, h), P, 0) or 1.2, 3)}); return True
        elif kd in ('swing', 'pendulum') and h >= 80 and w <= W * .5:
            amp = float(at.get('data-amp', 28 if kd == 'swing' else 18)); px = cx; py = y
            kx = px - math.sin(math.radians(amp)) * h - 36 * s0; ky = py + math.cos(math.radians(amp)) * h + 60 * s0   # where the tip is at its first +amp extreme: SVG rotation is clockwise, so a point below the pivot swings to the LEFT (checked on the synthetic page 2026-10-29)
            if h >= 250 and not SERIOUS and not HANGW.search(text) and .1 * W < kx < .9 * W and 82 * s0 + 150 <= ky <= cap:
                keep.update(kind='bg', ride=None, behind=None, x=round(kx), y=round(ky), s=s0, flip=1, enter='cut', delay=.02); set_act(keep, 'knocked', obj=gid); return True
            if y + h + 56 * s0 + 60 <= cap:
                keep.update(kind='ride', ride=gid, behind=None, x=round(cx), y=round(y + h + 56 * s0), s=s0, flip=1 if cx < W / 2 else -1); set_act(keep, 'swingride', obj=gid); return True
        elif kd == 'bouncing' and w <= 400:
            if w >= 120 and (BOUNCEW.search(text) or float(at.get('data-h', 60)) >= 80) and y - 160 * s0 >= 82 * s0 + 150:   # big enough to ride: bounces on top of it
                keep.update(kind='ride', ride=gid, behind=None, x=round(x + w * (.2 if cx > W / 2 else .8)), y=round(y + 4), s=s0, flip=1 if cx < W / 2 else -1); set_act(keep, 'trampoline', obj=gid, serious=SERIOUS); return True
            pos = beside(g, W, H, vert, tb)
            if pos: keep.update(kind='bg', ride=None, behind=None, **pos); set_act(keep, 'bumped', obj=gid, serious=SERIOUS); return True
        elif kd in ('slam', 'squash') and w <= 500 and h <= 500:   # a thud beside it throws it up
            pos = beside(g, W, H, vert, tb)
            if pos: keep.update(kind='bg', ride=None, behind=None, enter='cut', delay=.02, **pos); set_act(keep, 'shockwave', obj=gid); return True
        elif kd == 'magnet' and w <= 400 and h <= 400 and abs(float(at.get('data-dx', -200))) >= 120 and y + h <= cap + 30:   # holds it and gets yanked along
            ddx = float(at.get('data-dx', -200)); sg = 1 if ddx > 0 else -1; fx = cx - sg * (w / 2 + 40 * s0)
            if .08 * W < fx < .92 * W and .06 * W < fx + ddx * .85 < .94 * W:
                keep.update(kind='bg', ride=None, behind=None, x=round(fx), y=round(min(y + h, cap)), s=s0, flip=sg, enter='cut', delay=.02); set_act(keep, 'magnetized', obj=gid); return True
        elif kd == 'hop' and w <= 260 and h <= 260:   # hops along with a hopping creature
            pos = beside(g, W, H, vert, tb)
            if pos: keep.update(kind='bg', ride=None, behind=None, **pos); set_act(keep, 'hopalong', obj=gid); return True
        elif kd == 'drip' and float(at.get('data-fall', 140)) >= 80 and w <= 300:   # stands under the drip
            fall = float(at.get('data-fall', 140)); fy = y + fall + 80 * s0
            if 82 * s0 + 150 <= fy <= cap and .1 * W < cx < .9 * W:
                keep.update(kind='bg', ride=None, behind=None, x=round(cx), y=round(fy), s=s0, flip=1 if cx < W / 2 else -1, enter='cut', delay=.02); set_act(keep, 'dripped', obj=gid, serious=SERIOUS); return True
        elif kd == 'spin' and 160 <= w <= 600 and WHEELG.search(gid) and not SERIOUS and y - 100 * s0 >= 82 * s0 + 150:   # clings to the rim and goes round
            keep.update(kind='bg', ride=None, behind=None, x=round(cx), y=round(y + 6), s=round(min(s0, w / 300), 2), flip=1 if cx < W / 2 else -1, enter='cut', delay=.02); set_act(keep, 'rimride', obj=gid, r=round(h / 2 - 6)); return True
        elif kd == 'popin' and w <= 320 and h <= 320 and y + h <= cap + 20 and y - 80 * s0 >= 82 * s0 + 150:   # stands where it pops in: lifted on top
            keep.update(kind='bg', ride=None, behind=None, x=round(cx), y=round(min(y + h, cap)), s=s0, flip=1 if cx < W / 2 else -1, enter='cut', delay=.02); set_act(keep, 'launched', obj=gid, h=round(h)); return True
        elif kd == 'unroll' and w >= 400 and h <= 200 and y + h <= cap + 30:   # on the lane of the unrolling carpet
            fr = .7 if x + w * .7 < .9 * W else .5
            keep.update(kind='bg', ride=None, behind=None, x=round(x + w * fr), y=round(min(y + h, cap)), s=s0, flip=1, enter='cut', delay=.02); set_act(keep, 'unrolled', obj=gid, frac=fr); return True
        elif kd == 'ascend' and w <= 320 and h <= 400 and y + h + 56 * s0 + 60 <= cap:   # hangs under the rising thing
            keep.update(kind='ride', ride=gid, behind=None, x=round(cx), y=round(y + h + 56 * s0), s=s0, flip=1 if cx < W / 2 else -1); set_act(keep, 'balloonride', obj=gid); return True
        elif kd == 'sink' and 120 <= w <= 500 and y - 100 * s0 >= 82 * s0 + 150:   # stands on the end of the sinking thing, waving
            keep.update(kind='ride', ride=gid, behind=None, x=round(x + w * (.2 if cx > W / 2 else .8)), y=round(y + 4), s=s0, flip=1 if cx < W / 2 else -1); set_act(keep, 'sinkride', obj=gid); return True
        elif kd == 'rise' and w <= 320 and h <= 300 and LIFTW.search(text):
            keep.update(kind='ride', ride=gid, behind=None, x=round(cx), y=round(y + h + 50 * s0), s=s0, flip=1 if cx < W / 2 else -1); set_act(keep, 'lift', obj=gid); return True
    if TUGW.search(text):
        rp = sorted([g for g in gs.values() if ROPEG.search(g[0]) and g[3] >= 150], key=lambda g: -g[3])
        if rp:
            pos = beside(rp[0], W, H, vert, tb)
            if pos: keep.update(kind='bg', ride=None, behind=None, **pos); set_act(keep, 'tug'); return True
    if BLOWW.search(text) and not keep.get('ride') and not SPACE.search(text):
        ctx = facing.context({'groups': []}, svgtxt, {})
        wind = ctx.get('wind', 1) or 1; fx = W * (.62 if wind > 0 else .38)   # pushed along the wind: start on the upwind side of the centre
        keep.update(kind='bg', ride=None, behind=None, x=round(fx), y=(H - 360) if vert else (H - 190), s=s0, flip=-wind); set_act(keep, 'blown'); return True
    return False


def loco_pick(keep, text, gs, palname, W, H, vert, n, pg):
    """locomotion acts by words (+ a group when they need one). Returns True when applied."""
    if keep.get('ride') or keep.get('cling'): return False
    cap = H - (460 if vert else 290); s0 = round((1.05 if vert else .8) * [1.0, .9, 1.1, .95][n % 4], 2); y0 = (H - 360) if vert else (H - 190)
    right = (n % 2 == 1); x0 = max(260, min(W - 260, 260 if right else W - 260)); fl = 1 if right else -1; dist = round(W * (.34 if vert else .3))
    water = palname == 'ocean' or has_group(gs, WATER_G, .2, W, H)
    def lane(ty, **kw):
        keep.update(kind='bg', ride=None, behind=None, x=x0, y=y0, s=s0, flip=fl); set_act(keep, ty, dist=dist, **kw)
    if SWIMW.search(text) and (water or SEA.search(text)):
        yb = free_band(pg, W, H, vert, n); keep.update(kind='bg', ride=None, behind=None, x=x0, y=yb, s=s0, flip=fl); set_act(keep, 'swimstroke', dist=dist)
        if keep.get('outfit') not in (['diver'], ['goggles']): keep['outfit'] = ['goggles']
        return True
    if CLIMBW.search(text):
        cg = sorted([g for g in gs.values() if CLIMBG.search(g[0]) and g[4] >= 200 and g[3] <= W * .5], key=lambda g: -g[4])
        if cg:
            _, gx, gy, gw, gh = cg[0]; side = 1 if gx + gw / 2 < W / 2 else -1; fx = gx + gw / 2 + side * (gw / 2 + 26 * s0); base = min(gy + gh, cap)
            if .06 * W < fx < .94 * W:
                keep.update(kind='bg', ride=None, behind=None, x=round(fx), y=round(base), s=s0, flip=-side); set_act(keep, 'climb', dist=round(min(gh * .7, base - 160))); return True
    if DANGLEW.search(text):
        hg = sorted([g for g in gs.values() if HANGG.search(g[0]) and g[3] >= 80 and g[2] + g[4] < cap - 160], key=lambda g: -g[3])
        if hg:
            _, hx, hy, hw, hh = hg[0]; fx = hx + hw * (.35 if hx + hw / 2 > W / 2 else .65); fy = hy + hh + 56 * s0
            keep.update(kind='ride' if OK.match(hg[0][0]) else 'bg', ride=hg[0][0] if OK.match(hg[0][0]) else None, behind=None, x=round(fx), y=round(fy), s=s0, flip=1 if fx < W / 2 else -1)
            set_act(keep, 'dangle', drop=round(max(60, min(cap - fy, 420)))); keep['_says'] = [{'text': 'Uh-oh...', 'shout': False}, {'text': 'Oof!', 'shout': True}]; return True
    if TIGHTW.search(text):
        tg = sorted([g for g in gs.values() if TIGHTG.search(g[0]) and g[3] >= 300 and g[4] <= 80], key=lambda g: -g[3])
        if tg:
            _, gx, gy, gw, gh = tg[0]; fl2 = 1 if gx + gw / 2 >= W / 2 else -1; fx = gx + gw * (.12 if fl2 > 0 else .88)
            keep.update(kind='bg', ride=None, behind=None, x=round(fx), y=round(gy + 4), s=s0, flip=fl2); set_act(keep, 'tightrope', dist=round(gw * .7)); return True
    if LEAPW.search(text) and not SPACE.search(text): lane('leap'); return True
    if SKATEW.search(text) and not water: lane('skate'); keep['outfit'] = keep.get('outfit') or ['scarf']; return True
    if SOMERW.search(text) and not SERIOUS: lane('somersault'); return True
    if SNEAKW.search(text): lane('tiptoe'); return True
    if CRAWLW.search(text): lane('crawl'); return True
    return False


def costume_pick(keep, text, gs, W, H, vert, n):
    """the outfit decides what the frog does when nothing else did (frog_rig.OUTFIT_ACT); travel acts need a lane (a roam, or a free bottom band)"""
    for o in keep.get('outfit') or []:
        ty = frog_rig.OUTFIT_ACT.get(o)
        if not ty: continue
        if ty not in frog_rig.MOVES:   # an existing act (scope / magnify / think / snooze / float / fly / look)
            if keep.get('ride') and ty in ('fly', 'float'): return False
            keep['act'] = ty; keep.pop('roam', None); return True
        if ty in frog_rig.TRAVEL_ACTS:
            if keep.get('ride') or keep.get('cling'): return False
            rm = keep.get('roam')
            if rm: set_act(keep, ty, dist=rm.get('dist', 300))
            else:
                s0 = round((1.05 if vert else .8), 2); right = (n % 2 == 1)
                keep.update(kind='bg', ride=None, behind=None, x=max(260, min(W - 260, 260 if right else W - 260)), y=(H - 360) if vert else (H - 190), s=s0, flip=1 if right else -1); set_act(keep, ty, dist=round(W * (.3 if vert else .22)))
            return True
        set_act(keep, ty); return True
    return False


# round 4c (2026-10-26, miya: more expressions, picked per script + picture): sentence words -> one of the 20 new faces, first match wins,
# checked BEFORE the old punctuation / number rules. Playful faces (laugh, grin, cheeky, mischief, smug, wink) are dropped on serious topics.
MOODW = [
    ('tearful', r'\b(goodbye|farewell|tears?|wept|weep\w*|cried|crying|grie\w*|heartbreak\w*|last breath)\b'),
    ('hurt', r'\b(pain\w*|hurt\w*|sting\w*|bit(e|es|ten)|wound\w*|ouch|ache\w*|bruis\w*|burned)\b'),
    ('queasy', r'\b(rot\w*|stench|stink\w*|slime|slimy|decay\w*|putrid|maggot\w*|vomit\w*|nause\w*|seasick)\b'),
    ('disgust', r'\b(gross|disgust\w*|foul|revolting|filth\w*|yuck|eww|sewage)\b'),
    ('chilly', r'\b(freez\w*|frozen|frost\w*|icy|ice-cold|chill\w*|subzero|blizzard\w*|shiver\w*)\b'),
    ('hot', r'\b(scorch\w*|sweltering|blazing|heatwave|boiling hot|furnace|molten|sunburn\w*|overheat\w*)\b'),
    ('awe', r'\b(vast|enormous|gigantic|immense|colossal|countless|unimaginabl\w*|towering|staggering|mind-boggling)\b'),
    ('starry', r'\b(treasure\w*|jewel\w*|gold|diamond\w*|magic\w*|dream come true|sparkl\w*|glitter\w*|dazzl\w*)\b'),
    ('laugh', r'\b(funny|hilarious|joke\w*|laugh\w*|giggl\w*|comical|ridiculous)\b'),
    ('grin', r'\b(delicious|yummy|tasty|feast\w*|victory|won\b|winner\w*|jackpot|success\w*)\b'),
    ('cheeky', r'\b(silly|playful|tease\w*|teasing|goof\w*|mischie\w*|naughty)\b'),
    ('mischief', r'\b(sneak\w*|prank\w*|trick\w*|scheme\w*|plot\w*|cunning|sly)\b'),
    ('smug', r'\b(of course|obviously|easy|easily|effortless\w*|genius|clever\w*|outsmart\w*)\b'),
    ('wink', r'\b(secret\w*|between us|hint|wink\w*|spoiler|little trick)\b'),
    ('pout', r'\b(unfair|refus\w*|denied|forbid\w*|not allowed|no way|banned|rejected)\b'),
    ('bored', r'\b(boring|bored|tedious|monoton\w*|waiting|waited|nothing happen\w*|for centuries|for ages|dull)\b'),
    ('confused', r'\b(confus\w*|puzzl\w*|strange\w*|odd|weird|baffl\w*|bewilder\w*|makes no sense|paradox\w*)\b'),
    ('suspicious', r'\b(suspect\w*|suspicious|lie\b|lies\b|lying|fake\w*|fraud\w*|hidden|conceal\w*|hoax\w*|too good to be true)\b'),
    ('determined', r'\b(mission\w*|must\b|never give up|persist\w*|struggl\w*|determin\w*|against all odds|fight on|push\w* on|endur\w*)\b'),
    ('blush', r'\b(shy|embarrass\w*|blush\w*|compliment\w*|praise\w*|flatter\w*|bashful|crush on)\b'),
]
MOODW = [(m, re.compile(r, re.I)) for m, r in MOODW]
PLAYFUL = ('laugh', 'grin', 'cheeky', 'mischief', 'smug', 'wink', 'blush', 'starry')
# picture -> face: the name of the group the frog rides / stands by, when the sentence gave only a default face
RIDE_MOOD = [('determined', r'rocket|ship|probe|voyager|plane|jet|sled|boat|raft|canoe|car\b|train'), ('awe', r'whale|giant|mountain|volcano|tower|dinosaur|mammoth|planet|galaxy|sun\b'),
             ('starry', r'treasure|gold|gem|coin|crystal|jewel|crown'), ('hot', r'fire|lava|flame|furnace|sun\b|star\b'), ('chilly', r'ice|snow|glacier|iceberg|frost'),
             ('queasy', r'skull|bone|carcass|rot|slime|garbage|trash')]
RIDE_MOOD = [(m, re.compile(r, re.I)) for m, r in RIDE_MOOD]
PAL_MOOD = {'ice': 'chilly', 'desert': 'hot'}   # palette default for a calm first face


def mood_of(s):
    for m, rx in MOODW:
        if rx.search(s) and not (SERIOUS and m in PLAYFUL): return m
    if s.rstrip().endswith('?'): return 'curious'
    if s.rstrip().endswith('!'): return 'excited'
    if re.search(r'\b(never|impossible|terrifying|trapped|lost|prison|dark|fade|alone|gone)\b', s, re.I): return 'worried'
    if re.search(r'\d|\b(billion|million|thousand|trillion|faster|fastest)\b', s, re.I): return 'surprised'
    if re.search(r'\b(but|however|yet|actually|here)\b', s, re.I): return 'curious'
    return 'happy'
n = 0; SERIOUS = False
with sync_playwright() as p:
    b = p.chromium.launch(executable_path=chrome(), args=['--no-sandbox']); pg = b.new_page()
    for slug in sys.argv[1:]:
        vert = 'short' in slug; W, H = (1080, 1920) if vert else (1920, 1080)
        try: SERIOUS = getattr(load_config(slug), 'FROG_TONE', '') == 'serious'   # config.py FROG_TONE = 'serious' for grim topics (disease, death, war): no cheering, no Yay/Tada (miya 2026-10-26)
        except Exception: SERIOUS = False
        plan = {u['uid']: u for u in json.load(open(f'{REPO}/videos/{slug}/plan.json'))}
        for uid, u in sorted(plan.items()):
            fn = f'{REPO}/videos/{slug}/art3/{uid}.json'; svg = fn[:-5] + '.svg'
            d = json.load(open(fn)) if os.path.exists(fn) else {}
            if u.get('kind') == 'chalk' or not os.path.exists(svg): continue
            if not (u.get('frog_hint') or d.get('frog') or ('mv-edge-horizon' in open(svg).read() and re.search(r'horizon', u['text'], re.I))): continue   # a drawn event-horizon ring always gets the frog circling it (miya 2026-10-26)
            if (d.get('frog') or {}).get('lock'): continue   # hand-made sidecar (miya 2026-10-26, e.g. the caged frog in edge-of-universe U010): never overwritten
            f = d.get('frog') if isinstance(d.get('frog'), dict) else {}
            text = u['text']; palname = (u.get('pal') or {}).get('palette', ''); sents = [x for x in re.findall(r'[^.!?]+[.!?]?', text) if x.strip()]
            moods = []; prev = None
            for i, s in enumerate(sents):
                m = mood_of(s)                                      # (2026-10-27) the same mood on two sentences stays (the situation continues)
                w = ' '.join(re.sub(r"[^\w']", '', t) for t in s.split()[:2]).strip()
                moods.append({'mood': m} if i == 0 else {'word': w, 'mood': m}); prev = m
            act = None; first = None; matched = False
            for nm, rx, md in ACTS:
                if nm == 'slide' and palname == 'ocean': continue
                if nm == 'slide' and re.search(r'black holes?|event horizon|horizon|plunge\w*|swallow\w*|devour\w*|spiral\w*|drag\w*|falls? in', text, re.I): continue   # those stay 'pull'
                if rx.search(text): act, first = nm, md; matched = True; break
            if act is None:   # no situation word: a calm, varied reaction picked from the first sentence's mood, never a hop on every object (miya 2026-10-26)
                m0 = moods[0]['mood']; cyc = ('sway', 'nod', 'look', 'tilt', 'breathe'); cnt_calm = globals().setdefault('cnt_calm', 0); globals()['cnt_calm'] = cnt_calm + 1
                act = {'curious': 'tilt', 'surprised': 'look', 'worried': 'sway'}.get(m0) or cyc[cnt_calm % len(cyc)]
                if SPACE.search(text) and cnt_calm % 3 == 0: act = 'float'
                first = None if act != 'float' else 'happy'
            elif act == 'cheer':   # a real cheer word: only every second one hops, the others nod
                cnt_ch = globals().setdefault('cnt_cheer', 0); globals()['cnt_cheer'] = cnt_ch + 1
                if cnt_ch % 2: act = 'nod'

            if first: moods[0] = {'mood': first}
            if len(moods) > 1 and moods[1]['mood'] == first: moods[1]['mood'] = 'curious'
            keep = {'moods': moods, 'act': act}
            if SEA.search(text) or palname == 'ocean': keep['outfit'] = ['diver'] if (DEEP.search(text) or palname == 'ocean' and not re.search(r'surface|shallow|beach|shore|wave', text, re.I)) else ['goggles']   # (2026-10-26 review: a space helmet in the whale video)   # diving suit + tank in deep/dark water, mask + snorkel near the surface (miya 2026-10-25)
            elif SPACE.search(text): keep['outfit'] = ['helmet']
            pg.set_content('<style>body{margin:0}svg{display:block;width:100vw;height:100vh}</style><body>' + open(svg).read() + '</body>')
            pg.set_viewport_size({'width': W, 'height': H}); gs = {g[0]: g for g in pg.evaluate(JS)}; tb = pg.evaluate(JST)
            pick = f.get('ride') if f.get('ride') in gs else None
            if ROLL.search(text) and not ACTIVE.search(text): pick = None   # dragged / swept / spiralling: the frog rolls along instead of riding (miya 2026-10-26)
            elif not pick:
                cand = [g for g in gs.values() if OK.match(g[0]) and 60 <= g[3] <= W * .8 and g[4] >= 40]
                cand.sort(key=lambda g: -g[3] * g[4]); pick = cand[0][0] if cand else None
            if VEH.search(text) and not ROLL.search(text):   # a vehicle in the text: the frog clings beside the fin of the centre object (miya 2026-10-26)
                core = [g for g in gs.values() if g[0].startswith('mv-core-') and OK.match(g[0])]
                if core: pick = core[0][0]; keep['cling'] = True
            slid = False
            PIT = re.compile(r'hole|bh|well|funnel|pit|grid|sheet|fabric|dent|bowl|warp|sun|star|planet|mass|earth', re.I)
            if act == 'slide' and not ROLL.search(text) and not any(PIT.search(g) for g in gs) and not re.search(r'spacetime|space-time|fabric|warp', text, re.I):
                act = None; keep['act'] = None   # (review 2) 'gravity' beside an apple tree and a clock: nothing to slide into -> treated like a unit without a situation word below
                m0 = moods[0]['mood']; act = {'curious': 'tilt', 'surprised': 'look', 'worried': 'sway'}.get(m0, 'nod'); keep['act'] = act; keep['moods'][0] = {'mood': m0}
            if act == 'slide' and not ROLL.search(text):   # slides from the rim of the picture's pit (the heavy centre object / hole) down to its bottom
                tgt = [g for g in gs.values() if g[0].startswith('mv-core-') or HOLE.search(g[0]) or PIT.search(g[0])]
                tgt.sort(key=lambda g: (0 if HOLE.search(g[0]) else 1, -g[3] * g[4])); tx, ty = (round(tgt[0][1] + tgt[0][3] / 2), round(tgt[0][2] + tgt[0][4] * .6)) if tgt else (W // 2, round(H * .62))
                side = 1 if n % 2 == 0 else -1; sx = max(150, min(W - 150, round(tx - side * W * (.3 if not vert else .35)))); sy = max(210, round(ty - H * (.2 if not vert else .1)))
                s0 = round(.9 if not vert else 1.15, 2); n += 1; slid = True
                keep.update(kind='bg', ride=None, x=sx, y=sy, s=s0, flip=1 if tx > sx else -1, act={'type': 'slide', 'to': [tx, ty]}); keep.pop('roam', None); keep.pop('cling', None)
                keep['moods'] = [{'mood': 'surprised'}] + ([{'word': moods[1].get('word', ''), 'mood': 'scared'}] if len(moods) > 1 and moods[1].get('word') else [])
                if SPACE.search(text): keep['outfit'] = ['helmet']
            if slid: pass
            elif pick:
                _, x, y, w, h = gs[pick]
                if HOLE.search(pick) and act not in ('orbit', 'pull') and not keep.get('cling'): act = 'pull'; keep['act'] = 'pull'; keep['moods'][0] = {'mood': 'scared'}   # (review 2) a frog standing on a black hole: pulled instead
                calm = (act in CALM or act in ('awe', 'sleepy', 'float', None)) and not keep.get('cling')
                pos = (beside(gs[pick], W, H, vert, tb) if calm and not MOVING.match(pick) else None) or perch(pg, gs[pick], W, H, vert, tb, n) or beside(gs[pick], W, H, vert, tb)
                if act == 'pull' and HOLE.search(pick) and not keep.get('cling'):   # the picked object IS the hole: the frog floats beside it and gets pulled in, it does not ride the hole
                    side = 1 if (x + w / 2) < W / 2 else -1; pos = dict(x=round(min(W * .9, max(W * .1, x + w / 2 + side * max(w * .75, W * .22)))), y=round(y + h * .55), s=.9, flip=-side); pick = None
                if pos is None: pos = dict(x=round(x + w / 2), y=round(max(y + 8, 122)), s=1.0, flip=1 if x + w / 2 < W / 2 else -1)
                if pick: keep.update(ride=pick, kind='ride', **pos)
                else: keep.update(ride=None, kind='bg', **pos)
                if keep.pop('cling', False): keep.update(x=round(x + w * .95), y=round(y + h - 12), s=round(min(1.2, max(.9, h / 200)), 2), flip=-1, act='wind')
            elif not (act in STRONG or ACTIVE.search(text) or ROLL.search(text)):   # (a background frog needs a strong situation: pulled / wind / shivering / awe / running / rolled; waves, sleepy, cheer alone are not enough)
                # meaning gate (miya 2026-10-26: "frogs that appear at the bottom for no reason"): a frog that rides nothing and has no situation to react to is left out
                if 'frog' in d: d.pop('frog'); json.dump(d, open(fn, 'w'), ensure_ascii=False, indent=1)
                print(slug, uid, 'skip (no situation)'); continue
            else:
                n += 1   # roaming (miya 2026-10-26: the frog stayed in one bottom spot): small, travelling through the free part of the background
                plat = [g for g in gs.values() if PLAT.search(g[0]) and g[3] >= 220 and g[4] <= H * .25 and g[2] > H * .25]
                plat.sort(key=lambda g: -g[3]); plat = plat[0] if plat else None
                on_plat = None
                if plat and ACTIVE.search(text): kind = 'moonhop' if (SPACE.search(text) or 'tread' in text.lower() or 'tread' in plat[0]) else 'run'; on_plat = plat   # situation: the frog does it ON the platform of the picture (treadmill belt, ground, bridge...)
                elif ROLL.search(text): kind = 'roll'   # dragged / swept / spiralling: it rolls along
                elif SEA.search(text) or (SPACE.search(text) and not GROUND.search(text)):   # diver / space-suit drifting: upright float, lying on its back, somersault (space only)
                    kind = ('swim', 'lie', 'tumble' if not SEA.search(text) else 'swim')[(n - 1) % 3]
                elif GROUND.search(text): kind = ('run', 'moonhop' if SPACE.search(text) else 'run')[(n - 1) % 2]
                else: kind = 'walk'
                sz = [1.0, .9, 1.1, .95][(n - 1) % 4]
                if kind in ('swim', 'lie', 'tumble'): y0 = free_band(pg, W, H, vert, n); s0 = (1.1 if vert else .85) * sz
                elif kind == 'roll': y0 = free_band(pg, W, H, vert, n); s0 = (1.1 if vert else .85) * sz
                else: y0 = (H - 360) if vert else (H - 190); s0 = (1.05 if vert else .8) * sz   # (2026-10-26 review 2) above the caption box, never over the subtitles
                if on_plat: y0 = round(on_plat[2] + 6)
                right = (n % 2 == 1); dist = round(W * ((.28 if vert else .24) if kind in ('swim', 'lie', 'tumble', 'roll') else (.5 if vert else .15)))
                x0 = (260 if right else W - 260); fl = 1 if right else -1
                if on_plat:   # stays on the platform, on the side away from the figure that runs on it
                    figs = [g for g in gs.values() if re.search(r'run|astro|breathe|legs|walker|person|man\b|woman|kid|child', g[0], re.I) and g[0] != on_plat[0]]
                    pcx = on_plat[1] + on_plat[3] / 2; fcx = (sum(g[1] + g[3] / 2 for g in figs) / len(figs)) if figs else pcx
                    right = fcx > pcx   # figure on the right -> frog starts on the left part and walks toward the facing side (right)
                    x0 = round(on_plat[1] + on_plat[3] * (.15 if right else .85)); fl = 1 if right else -1; dist = round(min(dist, on_plat[3] * .3))
                else: x0 = max(260, min(W - 260, x0))
                if act in ('pull', 'shiver', 'awe') and not on_plat: y0 = free_band(pg, W, H, vert, n)   # a strong reaction in the open picture, not down in the caption zone
                keep.update(x=x0, y=y0, s=round(s0, 2), flip=fl, kind='bg', roam=dict(kind=kind, dist=dist))
                if act in ('float', 'cheer') or kind in ('swim', 'lie', 'tumble', 'roll'): keep['act'] = None   # the roaming motion replaces the in-place bob/hops; a drifting swimmer gets no lean/wind lines (miya 2026-10-26)
            # ---- round 3 relation acts (2026-10-26, guideline 7-2 D): applied only on a weak act; each one keyed on words + group ids ----
            cur = keep.get('act'); weak = (cur in CALM or cur in WEAK) and not isinstance(cur, dict) and not slid and not keep.get('cling')
            dood = bool(NOTE.search(text) and any(BOOK.search(g[0]) and g[3] >= 200 for g in gs.values()))   # this picture will get the doodle act below (was an undefined name, found 2026-10-27 whole-repo check)
            SOFT = re.compile(r'glow|halo|ring|bg\b|background|sky|grid|star|nebula|circle|field|beam|light|aura|dust|particle|fog|mist|cloud|haze|wave|line|path|track|orbit|trail|edge|shadow|glint|lamp', re.I)
            big = sorted([g for g in gs.values() if 200 <= g[3] <= W * .6 and g[4] >= 120 and not PLAT.search(g[0]) and not SOFT.search(g[0])], key=lambda g: -g[3] * g[4])   # a solid object to hide behind (no glows / rings / backgrounds)
            rk = keep.get('ride') or ''
            if weak and HIDEW.search(text):
                keep['act'] = 'hide'; keep['moods'][0] = {'mood': 'scared'}
            elif weak and CRYW.search(text) and not keep.get('cling'):   # round 4: a death / extinction / goodbye -> cries beside or on the object
                keep['act'] = 'cry'; keep['moods'][0] = {'mood': 'sad'}
            elif weak and FACEW.search(text):
                keep['act'] = 'facepalm'; keep['moods'][0] = {'mood': 'worried'}
            elif weak and contact_pick(keep, text, gs, open(svg, encoding='utf-8').read(), palname, W, H, vert, tb): pass   # 2026-10-29: meets a moving object (apple on the head, toppling pole, rolling boulder ...)
            elif weak and loco_pick(keep, text, gs, palname, W, H, vert, n, pg): n += 1   # 2026-10-29: swims / climbs / leaps / dangles / skates / somersaults / sneaks / crawls / walks a line
            elif weak and IDEAW.search(text) and not SERIOUS:
                keep['act'] = 'idea'; keep['moods'][0] = {'mood': 'excited'}
            elif weak and PEEKW.search(text) and big:   # hidden behind the biggest object, peeking out on the side toward the screen centre
                _, bx, by, bw, bh = big[0]; side = 1 if bx + bw / 2 < W / 2 else -1; s0 = round(1.0 if not vert else 1.2, 2)
                px = bx + bw - 10 if side > 0 else bx + 10; py = max(min(by + bh, H - (460 if vert else 290)), 82 * s0 + 150)
                keep.update(kind='bg', ride=None, behind=big[0][0], x=round(px), y=round(py), s=s0, flip=side, act='peek', moods=[{'mood': 'curious'}], bside=side); keep.pop('roam', None)
            elif weak and HANGW.search(text) and any(HANGG.search(g) for g in gs):   # hangs under a branch / rope / beam / ring of the picture by both hands
                hg_ = sorted([g for g in gs.values() if HANGG.search(g[0]) and g[3] >= 80], key=lambda g: -g[3])[0]
                _, hx_, hy_, hw_, hh_ = hg_; s0 = round(.95 if not vert else 1.15, 2); fx_ = hx_ + hw_ * (.35 if hx_ + hw_ / 2 > W / 2 else .65)
                keep.update(kind='ride' if OK.match(hg_[0]) else 'bg', ride=hg_[0] if OK.match(hg_[0]) else None, x=round(fx_), y=round(hy_ + hh_ + 96 * s0), s=s0, flip=1 if fx_ < W / 2 else -1, act='hang', moods=[{'mood': 'excited'}]); keep.pop('roam', None)
            elif weak and TAPW.search(text) and keep.get('ride') and keep.get('kind') == 'ride':
                keep['act'] = 'tap'; keep['moods'][0] = {'mood': 'curious'}
            elif weak and RESTW.search(text) and keep.get('ride'):
                keep['act'] = 'rest'; keep['moods'][0] = {'mood': 'happy' if not NIGHTW.search(text) else 'sleepy'}
            elif weak and SCOPEW.search(text) and (SPACE.search(text) or palname in ('space', 'deepfield') or re.search(r'telescope|observ', text, re.I)):
                keep['act'] = 'scope'; keep['moods'][0] = {'mood': 'curious'}
            elif weak and DIGW.search(text) and not keep.get('ride'): keep['act'] = 'dig'; keep['moods'][0] = {'mood': 'curious'}            # round 4 task acts (words only)
            elif weak and MAGW.search(text): keep['act'] = 'magnify'; keep['moods'][0] = {'mood': 'curious'}
            elif weak and READW.search(text) and not dood: keep['act'] = 'read'; keep['moods'][0] = {'mood': 'curious'}
            elif weak and PHOTOW.search(text): keep['act'] = 'photo'; keep['moods'][0] = {'mood': 'happy'}
            elif weak and EATW.search(text) and not SERIOUS: keep['act'] = 'eat'; keep['moods'][0] = {'mood': 'happy'}
            elif weak and DANCEW.search(text) and not SERIOUS: keep['act'] = 'dance'; keep['moods'][0] = {'mood': 'excited'}
            elif weak and CLAPW.search(text) and not SERIOUS: keep['act'] = 'clap'; keep['moods'][0] = {'mood': 'proud'}
            elif weak and SALUTEW.search(text): keep['act'] = 'salute'; keep['moods'][0] = {'mood': 'proud'}
            elif weak and THINKW.search(text): keep['act'] = 'think'; keep['moods'][0] = {'mood': 'curious'}
            elif weak and SNEEZEW.search(text) and not SPACE.search(text): keep['act'] = 'sneeze'; keep['moods'][0] = {'mood': 'squint'}
            elif weak and SNOOZEW.search(text) and keep.get('ride'): keep['act'] = 'snooze'; keep['moods'][0] = {'mood': 'sleepy'}
            elif weak and any(rx_.search(text) for _a, rx_ in ACT_WORDS2):   # round 4b data-driven acts (first matching word rule)
                a2 = next(a_ for a_, rx_ in ACT_WORDS2 if rx_.search(text)); keep['act'] = a2; keep['moods'][0] = {'mood': ACT_MOOD2[a2]}
            elif weak and any(PERSON.search(g) for g in gs) and not keep.get('ride'):   # a person in the picture and nothing better to do: stands near them and waves
                pg2 = sorted([g for g in gs.values() if PERSON.search(g[0])], key=lambda g: -g[4])[0]; pos2 = beside(pg2, W, H, vert, tb)
                if pos2: keep.update(kind='bg', ride=None, act='wave', moods=[{'mood': 'happy'}], **pos2); keep.pop('roam', None)
            elif weak and rk and POPG.search(rk): keep['act'] = 'startle'
            elif weak and rk and PULSEG.search(rk) and cur in CALM: keep['act'] = 'bounce'
            elif weak and rk and TRAVELG.search(rk) and cur in CALM and n % 2 == 0: keep['act'] = 'lean'   # every other ride on a traveller leans back; the others keep their calm act (variety)
            # ---- picture-evidence acts (miya 2026-10-27: script rule + picture rule everywhere): what the picture shows when the words gave nothing ----
            elif weak and ((has_group(gs, ICE_G, .06, W, H) and palname != 'ocean') or palname == 'ice') and not SERIOUS: keep['act'] = 'shiver'; keep['moods'][0] = {'mood': 'chilly'}   # (marine 'snow' in the ocean is not ice)
            elif weak and has_group(gs, HOLE_G, .06, W, H) and not keep.get('ride') and not isinstance(keep.get('act'), dict):   # a drawn black hole / well: pulled toward it (miya 2026-10-26 black hole = pulled in)
                hg_ = sorted([g for g in gs.values() if HOLE_G.search(g[0])], key=lambda g: -g[3] * g[4])[0]
                keep['act'] = {'type': 'pull', 'to': [round(hg_[1] + hg_[3] / 2), round(hg_[2] + hg_[4] / 2)]}; keep['moods'][0] = {'mood': 'scared'}
            elif weak and has_group(gs, FIRE_G, .08, W, H) and not keep.get('ride'): keep['act'] = {'type': 'dizzy'}; keep['moods'][0] = {'mood': 'dizzy'}   # a big fire / sun: overheated (same as the HEAT words)
            elif weak and has_group(gs, WATER_G, .25, W, H) and not keep.get('ride') and cur in CALM: keep['act'] = 'waves'; keep['moods'][0] = {'mood': 'surprised'}
            elif weak and rk and (SPACE_RIDE.search(rk) or re.search(r'plane|jet|train|car\b|sled|bike|motor', rk, re.I)) and cur in CALM: keep['act'] = 'wind'; keep['moods'][0] = {'mood': 'squint'}
            if keep.get('act') in ('scope', 'hide', 'tap', 'rest', 'wave', 'peek', 'hang', 'cry', 'facepalm', 'idea', 'dig', 'magnify', 'read', 'photo', 'eat', 'dance', 'clap', 'salute', 'think', 'sneeze', 'snooze') or (isinstance(keep.get('act'), str) and keep.get('act') in ACT_MOOD2): keep.pop('roam', None)   # these are done in place, not while roaming
            # ---- 2026-10-29 (frog_rig): a run / walk over a low thing on its lane trips it; a roll becomes a log-roll; the costume decides a weak act ----
            rm_ = keep.get('roam') or {}; weak2 = (keep.get('act') in CALM or keep.get('act') in WEAK) and not isinstance(keep.get('act'), dict) and not slid
            if rm_.get('kind') in ('run', 'walk') and not SERIOUS and weak2:
                lx0, lx1 = sorted((keep['x'], keep['x'] + keep['flip'] * rm_.get('dist', 300)))
                low = [g for g in gs.values() if LOWG.search(g[0]) and g[4] <= 80 and 40 <= g[3] <= 260 and abs(g[2] + g[4] - keep['y']) <= 50 and lx0 + 60 < g[1] + g[3] / 2 < lx1 - 40]
                if low:
                    g_ = low[0]; fr = (abs(g_[1] + g_[3] / 2 - keep['x']) - 30 * keep['s']) / max(rm_.get('dist', 300), 1)
                    set_act(keep, 'trip', dist=rm_.get('dist', 300), frac=round(min(max(fr, .2), .8), 3))
            elif rm_.get('kind') == 'roll': set_act(keep, 'logroll', dist=rm_.get('dist', 300))
            elif weak2 and not keep.get('_says') and rm_.get('kind') not in ('swim', 'lie', 'tumble', 'moonhop'): costume_pick(keep, text, gs, W, H, vert, n)
            # outfits by scene words (not over diving gear / helmet / fore)
            if not keep.get('outfit'):
                if LABW.search(text): keep['outfit'] = ['lab']
                elif EXPLW.search(text) and not SEA.search(text): keep['outfit'] = ['explorer']
                elif SCARFW.search(text): keep['outfit'] = ['scarf']
                elif NIGHTW.search(text): keep['outfit'] = ['nightcap']
                else:   # round 4: 14 more costumes by narration words, first match in the list order (crown, knight, pirate, doctor, chef, hardhat, headphones, gradcap, strawhat, umbrella, sunglasses, partyhat, wizard, detective)
                    for nm_, rx_ in OUTFIT_WORDS:
                        if rx_.search(text) and not (nm_ == 'pirate' and SPACE.search(text)) and not (nm_ == 'sunglasses' and (SPACE.search(text) or SEA.search(text))): keep['outfit'] = [nm_]; break
            po_ = pic_outfit(gs, palname, keep.get('ride'), W, H, phys_only=bool(keep.get('outfit')))   # picture evidence: fills in when the words gave nothing; cold / rain / boat beat a word costume
            if po_ and (not keep.get('outfit') or (keep['outfit'][0] not in ('helmet', 'diver', 'goggles', 'fore', 'fore_steps', 'lab', 'explorer', 'scarf', 'nightcap', 'umbrella', 'lifevest'))): keep['outfit'] = [po_]
            # extra faces on the first sentence when no strong act fixed it
            if keep.get('act') not in STRONG and not isinstance(keep.get('act'), dict):
                if ANGRYW.search(text): keep['moods'][0] = {'mood': 'angry'}
                elif SHOCKW.search(text): keep['moods'][0] = {'mood': 'shock'}
                elif LOVEW.search(text) and not SERIOUS: keep['moods'][0] = {'mood': 'love'}
            # ---- miya 2026-10-26 situation acts: heat -> dizzy, notebook/page -> doodle, hut doors -> huts + outfit steps, movable object (lens/crate) -> push by its handle ----
            doors = pg.evaluate(JSD)
            if keep.get('act') not in ('pull',) and HEAT.search(text) and not ROLL.search(text):
                keep['act'] = {'type': 'dizzy'}; keep['moods'] = [{'mood': 'dizzy'}]; keep.pop('outfit', None) if keep.get('outfit') == ['diver'] else None
            bk = [g for g in gs.values() if BOOK.search(g[0]) and g[3] >= 200]
            if NOTE.search(text) and bk and keep.get('act') != 'dizzy' and not (isinstance(keep.get('act'), dict) and keep['act'].get('type') == 'pull'):
                bk.sort(key=lambda g: -g[3] * g[4]); _, bx, by, bw, bh = bk[0]
                keep.update(kind='bg', x=round(bx + bw * .86), y=round(by + bh - 24), s=round(1.4 if vert else 1.5, 2), flip=-1, act={'type': 'doodle', 'from': 0.9}, moods=[{'mood': 'curious'}]); keep.pop('ride', None); keep.pop('roam', None)
            pg_ = [g for g in gs.values() if keep.get('ride') == g[0] and PUSHG.search(g[0]) and re.match(r'mv-(path|slide|glide)', g[0])]
            if pg_:
                _, gx, gy, gw, gh = pg_[0]; s1 = round(min(1.4, max(1.0, gw / 190)), 2)
                import facing
                mt_ = re.search(rf'<g [^>]*\bid="{re.escape(pg_[0][0])}"[^>]*>', open(svg, encoding='utf-8').read()); tsg = facing.travel_sign(mt_.group(0)) if mt_ else 0
                if tsg > 0:   # travels right: the frog heaves from the LEFT (back) side, facing right (2026-10-27, miya: interactions must match the direction)
                    keep.update(x=round(gx - 56 * s1), y=round(gy + gh * .92 + 36 * s1), s=s1, flip=1, kind='ride', act={'type': 'push', 'from': 0.6}, moods=[{'mood': 'squint'}])
                else:
                    hx, hy = gx + gw * .9, gy + gh * .92   # the handle end of a lens-like object (lower right of its box); travel left or unknown: push from the right
                    keep.update(x=round(hx + 56 * s1), y=round(hy + 36 * s1), s=s1, flip=-1, kind='ride', act={'type': 'push', 'from': 0.6}, moods=[{'mood': 'squint'}])
            if len(doors) >= 2 and VILL.search(text) and not vert:
                ts = [0.6 + i * 1.9 for i in range(min(3, len(doors)))]
                keep.update(kind='bg', x=round(max(100, doors[0][0] - 190)), y=round(doors[0][1] + 20), s=1.25, flip=1, outfit=['fore_steps'], moods=[{'mood': 'curious'}, {'word': 'in', 'mood': 'excited'}], ride=None,
                            act={'type': 'huts', 'huts': [{'t': t_, 'x': round(d_[0]), 'y': round(d_[1] + 4), 'wear': w_, 'stay': 0.3} for t_, d_, w_ in zip(ts, doors, ('bottom', 'top', 'head'))]})
                keep.pop('ride', None); keep.pop('roam', None); keep['_huts'] = [(t_ + 1.35, w_) for t_, w_ in zip(ts, ('Woo-hoo!', 'Look at me!', 'Ta-da!'))]
            elif FORE.search(text) and not SEA.search(text) and not SPACE.search(text) and 'outfit' not in keep: keep['outfit'] = ['fore']
            eh = [g for g in gs.values() if re.match(r'mv-edge-horizon', g[0])]
            if eh and re.search(r'horizon', text, re.I) and not ROLL.search(text):   # the drawn event-horizon ring (an arc group): the frog runs round it like a particle on its line, woozy (miya 2026-10-26)
                _, hx, hy, hw, hh = eh[0]; r = hh / 2; hcx, hcy = hx + r, hy + r; s0 = round((.85 if not vert else 1.0), 2)
                keep.update(kind='bg', ride=None, x=round(hcx), y=round(hcy - r + 8), s=s0, flip=1 if hcx < W / 2 else -1, act={'type': 'orbit', 'c': [round(hcx), round(hcy)], 'rx': round(r), 'ry': round(r), 'th0': -90, 'depth': 0, 'per': 3.6, 'dir': facing.spin_dir(open(svg, encoding='utf-8').read(), eh[0][0])})
                keep.pop('roam', None); keep.pop('cling', None); keep['moods'] = [{'mood': 'dizzy'}]; keep['outfit'] = ['helmet'] if SPACE.search(text) else []
            hg0 = [g for g in gs.values() if HOLE.search(g[0])]
            if not hg0 and re.search(r'black holes?|horizon', text, re.I): hg0 = [g for g in gs.values() if g[0].startswith('mv-core-')]   # the hole is the centre object
            if not isinstance(keep.get('act'), dict) and ORBIT.search(text) and hg0 and not ROLL.search(text):   # a black hole ring / particles in the text: the frog circles the ring like a particle on its line, woozy (miya 2026-10-26)
                _, hx, hy, hw, hh = hg0[0]; hcx, hcy = hx + hw / 2, hy + hh / 2; rx = max(110, min(hw * .62, W * .3)); ry = rx * .3; th0 = -90 if not vert else -90
                s0 = round((.9 if vert else .75) * [1.0, .9, 1.1][n % 3], 2)
                keep.update(kind='bg', ride=None, x=round(hcx), y=round(hcy - ry), s=s0, flip=1 if hcx < W / 2 else -1, act={'type': 'orbit', 'c': [round(hcx), round(hcy)], 'rx': round(rx), 'ry': round(ry), 'th0': th0, 'dir': facing.spin_dir(open(svg, encoding='utf-8').read(), hg0[0][0])})
                keep.pop('roam', None); keep.pop('cling', None); keep['moods'] = [{'mood': 'dizzy'}]; keep['outfit'] = ['helmet'] if SPACE.search(text) else keep.get('outfit', [])
                n += 1
            if act == 'pull' and not isinstance(keep.get('act'), dict):   # the hole the frog is dragged toward: a picture group named like a hole/well, else the picture centre
                hg = [g for g in gs.values() if HOLE.search(g[0])]
                keep['act'] = {'type': 'pull', 'to': [round(hg[0][1] + hg[0][3] / 2), round(hg[0][2] + hg[0][4] / 2)] if hg else [W // 2, H // 2]}
                if hg and (keep.get('kind') == 'ride' or not keep.get('roam')): keep['act']['vanish'] = True   # riding a star into the hole: pulled in, shrinking, gone (miya 2026-10-26)
            cnt_say = globals().setdefault('cnt_say', 0); globals()['cnt_say'] = cnt_say + 1
            if keep.get('outfit') not in (['helmet'], ['diver'], ['goggles'], ['fore'], ['fore_steps']) and in_space(text, palname, gs, keep.get('ride'), W, H, u.get('bg', 'night')) and not underwater(text, palname, gs, keep.get('ride'), W, H): keep['outfit'] = ['helmet']   # space helmet by the picture too (miya 2026-10-27: script rule + picture rule together)
            uw = underwater(text, palname, gs, keep.get('ride'), W, H)   # diving gear by the picture, not only the words (miya 2026-10-27); worn instead of a word costume
            if uw and keep.get('outfit') not in (['diver'], ['goggles'], ['helmet']) and not (isinstance(keep.get('act'), dict) and keep['act'].get('type') == 'huts'): keep['outfit'] = ['diver'] if uw == 'deep' else ['goggles']
            if uw and (keep.get('roam') or {}).get('kind') in ('swim', 'lie') and n % 2 == 0 and keep.get('_says') is None: set_act(keep, 'swimstroke', dist=keep['roam'].get('dist', 300))   # every other drifting diver really swims (2026-10-29)
            keep['says'] = says_for(keep['act'], keep, text, cnt_say); keep['bside'] = keep.get('bside') or (1 if keep['x'] < W / 2 else -1)
            if keep.get('_says') is not None: keep['says'] = keep.pop('_says')   # contact / locomotion / costume acts bring their own sound words (timed by the act)
            if isinstance(keep['act'], dict) and keep['act'].get('type') == 'push': keep['says'] = [{'text': 'Heave-ho!', 't': 1.0, 'dur': 1.6, 'shout': True}]
            if keep.get('_huts'): keep['says'] = [{'text': w_, 't': round(t_, 2), 'dur': 1.0, 'shout': True} for t_, w_ in keep.pop('_huts')]
            # round 4c: picture / palette faces when the first sentence gave only a default face and no strong act fixed one
            if keep['moods'][0]['mood'] in ('happy', 'curious', 'surprised') and keep.get('act') not in STRONG and not isinstance(keep.get('act'), dict):
                rn = keep.get('ride') or ''; pm = None
                for m_, rx_ in RIDE_MOOD:
                    if rx_.search(rn): pm = m_; break
                pm = pm or PAL_MOOD.get(palname)
                if pm and not (SERIOUS and pm in PLAYFUL): keep['moods'][0] = {'mood': pm}
            if SERIOUS:   # grim topics (config FROG_TONE='serious'): curious / worried faces, no cheering or happy sound words
                for m_ in keep['moods']:
                    if m_['mood'] in ('excited', 'happy'): m_['mood'] = 'curious'
                    if m_['mood'] == 'sleepy' and not re.search(r'wait|incubation|years|decades', text, re.I): m_['mood'] = 'worried'
                if keep['act'] in ('cheer',) or (keep['act'] == 'sleepy' and not re.search(r'wait|incubation|years|decades', text, re.I)): keep['act'] = None
                keep['says'] = [x_ for x_ in keep['says'] if x_['text'] not in SERIOUS_OUT and not (x_['text'] == 'Zzz...' and keep['act'] != 'sleepy')]
                if (keep.get('roam') or {}).get('kind') in ('run', 'moonhop'): keep['roam']['kind'] = 'walk'
                if not keep['act'] and not keep['says'] and not keep.get('roam'):   # (2026-10-26 review) the serious filter left a frog with nothing to do: a quiet worried look instead
                    keep['act'] = 'look'; keep['says'] = [{'text': 'Hmm...', 'shout': False}]; keep['moods'][0] = {'mood': 'worried'}
            if keep.get('kind') == 'ride' and keep.get('ride'):   # (2026-10-27, miya: interactions must match) the rider faces the way the object travels
                import facing
                mt = re.search(rf'<g [^>]*\bid="{re.escape(keep["ride"])}"[^>]*>', open(svg, encoding='utf-8').read())
                ts = facing.travel_sign(mt.group(0)) if mt else 0
                if ts: keep['flip'] = ts
            d['frog'] = keep
            json.dump(d, open(fn, 'w'), ensure_ascii=False, indent=1)
            print(slug, uid, keep['kind'], pick, keep['x'], keep['y'], keep['s'])
        nf = sum(1 for uu in plan if os.path.exists(f'{REPO}/videos/{slug}/art3/{uu}.json') and isinstance(json.load(open(f'{REPO}/videos/{slug}/art3/{uu}.json')).get('frog'), dict))
        if nf < .3 * len(plan): print(f'WARNING {slug}: frog in {nf}/{len(plan)} units (<30 %); add frog_hint to units with a situation (guideline 7-2: about 35-50 %)')
    b.close()
