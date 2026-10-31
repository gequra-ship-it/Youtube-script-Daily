# concepts.py -- CONCEPT rules + THEME PACKS for variety (2026-10-31, miya: "우주 영상은 내용이 비슷해 늘 비슷한 것만 나와 … 개념 규칙·주제 팩·다양성 게이트, 우주뿐 아니라 전부").
#
# Why: the frog / object rules key on single WORDS (rocket, cold, black hole). Space scripts repeat the same dozen ideas with few of those words,
# so most units fell to the same defaults (helmet + wind/shiver + squint). This module adds a second layer that is still deterministic:
#   1. CONCEPTS   a sentence is classified into idea classes (scale, time span, expansion, light speed, gravity, cold/empty, observation, unknown,
#                 birth, death, journey, danger, discovery, counting, comparison, change, speed, slowness, hidden, giant/tiny, home/safe, sound/signal ...)
#   2. PACKS      a theme pack per domain (space, sea, history, bio, body, time, earth, tech, generic): acts, outfit accessories, props the picture
#                 agents should draw moving, object motions that fit, compositions to rotate.
#   3. Tally      every pool pick is the LEAST-USED entry so far in the video (ties -> unit index), so a 130-unit space video spreads over the pool
#                 instead of repeating the first match. Word rules (frog_place ACTS, contact / locomotion picks) still win: this layer fills the rest.
# Nothing random: same script + same pictures -> same choices. Docs: guideline 7-2 J (frog), 4-9 (objects), art_spec 7B/12.
import re

# ---------------------------------------------------------------- domains (theme packs)
DOMAIN_W = [
    ('space',   r'\b(space|stars?|galax\w*|cosmic|cosmos|universe|planets?|orbit\w*|moon|mars|jupiter|saturn|solar|nebula\w*|comets?|asteroids?|astronaut\w*|rocket\w*|probe|voyager|light.?years?|black holes?|supernova\w*|big bang|telescope\w*|gravity well|spacetime|dark (matter|energy))\b'),
    ('sea',     r'\b(ocean\w*|seas?\b|seafloor|underwater|div(e|ing|ers?)|whales?|reefs?|corals?|fish\w*|sharks?|squids?|octopus\w*|plankton|abyss\w*|submarine\w*|tides?|waves?|shipwreck\w*|sailors?|harbou?rs?)\b'),
    ('history', r'\b(empire\w*|kings?|queens?|pharaoh\w*|romans?|greeks?|medieval|knights?|castles?|war\b|wars\b|battle\w*|armies|army|soldiers?|centur(y|ies)|ancient|dynast\w*|revolution\w*|treaty|colon\w*|vikings?|samurai|pirates?|explorers?|expedition\w*|emperor\w*|republic|parliament|archive\w*|manuscript\w*|chronicle\w*|\b1[0-9]{3}s?\b)\b'),
    ('body',    r'\b(brain\w*|hearts?|blood\w*|bones?|muscles?|nerves?|lungs?|stomach\w*|skin|cells?|dna|genes?|virus\w*|bacteri\w*|infect\w*|diseases?|patients?|doctors?|hospital\w*|surger\w*|medicine|immune|hormon\w*|organs?|digest\w*|parasit\w*|symptom\w*)\b'),
    ('bio',     r'\b(animals?|species|evolution\w*|evolv\w*|insects?|frogs?|birds?|mammals?|reptiles?|dinosaurs?|fossils?|predators?|prey|hunt\w*|nests?|eggs?|larva\w*|tadpoles?|forests?|jungles?|ecosystem\w*|habitat\w*|biolog\w*|plants?|seeds?|roots?|pollinat\w*|microbes?|fung\w*)\b'),
    ('time',    r'\b(clocks?|seconds?|minutes?|hours?|calendar\w*|time zones?|relativity|time dilation|ag(e|ing|ed)|past|future|yesterday|tomorrow|deadline\w*|schedule\w*|hourglass\w*|pendulum\w*|sundial\w*|leap (year|second)|midnight|watch(es)?\b)\b'),
    ('earth',   r'\b(volcano\w*|earthquake\w*|mountain\w*|rivers?|glaciers?|deserts?|storms?|hurricane\w*|climate|weather|rain\w*|snow\w*|ice|lava|tecton\w*|canyon\w*|caves?|soil|continent\w*|atmosphere|ozone|wind\w*|clouds?)\b'),
    ('tech',    r'\b(computer\w*|machines?|engines?|robots?|algorithm\w*|internet|data|signals?|radio|satellite\w*|electric\w*|circuit\w*|code|software|factor(y|ies)|invent\w*|patent\w*|gears?|steam|batter(y|ies)|wires?|antenna\w*)\b'),
]
DOMAIN_W = [(d, re.compile(rx, re.I)) for d, rx in DOMAIN_W]
PAL_DOMAIN = {'space': 'space', 'deepfield': 'space', 'solar': 'space', 'cosmic': 'space', 'ocean': 'sea', 'ice': 'earth', 'desert': 'earth', 'forest': 'bio', 'lab': 'body', 'parchment': 'history', 'sepia': 'history'}
PIC_DOMAIN = {'space': 'space', 'water': 'sea', 'bone': 'bio', 'heart': 'body', 'clock': 'time', 'gear': 'tech', 'typing': 'tech', 'book': 'history', 'coin': 'history', 'forest': 'bio', 'insect': 'bio', 'bird': 'bio', 'fire': 'earth', 'ice': 'earth', 'cave': 'earth'}


def video_domain(texts, palnames=()):
    """the whole video's theme: the domain whose words occur in the most units (palette names break ties)"""
    sc = {}
    for t in texts:
        for d, rx in DOMAIN_W:
            if rx.search(t): sc[d] = sc.get(d, 0) + 1
    for p in palnames:
        if p in PAL_DOMAIN: sc[PAL_DOMAIN[p]] = sc.get(PAL_DOMAIN[p], 0) + .5
    return max(sc, key=lambda d: (sc[d], d)) if sc else 'generic'


def unit_domain(text, palname='', pic=None, video=None):
    """this unit's theme: its own words (2+ hits), else the picture's tags, else the palette, else the video's theme"""
    hits = {d: len(rx.findall(text)) for d, rx in DOMAIN_W}; best = max(hits, key=lambda d: (hits[d], d == video, d))
    if hits[best] >= 2: return best
    for tag, d in PIC_DOMAIN.items():
        if pic and tag in pic: return d
    if palname in PAL_DOMAIN: return PAL_DOMAIN[palname]
    if hits[best] >= 1: return best
    return video or 'generic'


# ---------------------------------------------------------------- concepts (idea classes), checked on the unit text in this order
CONCEPTS = [
    ('scale',       r'\b(times (bigger|larger|smaller|wider|heavier|the size)|the size of|as (big|large|small|wide|tall|heavy) as|compared to|in comparison|dwarf\w*|enormous|gigantic|colossal|immense|vast\w*|minuscule|microscopic|a (grain|speck|dot) of|scale\b|to scale|shrunk|shrink\w*|magnif\w*)\b'),
    ('timespan',    r'\b(\d[\d,.]*\s*(billion|million|thousand|hundred)?\s*(years?|centuries|millennia|decades|ages|eons|aeons)|billions? of years|millions? of years|ages ago|long ago|forever|eternity|since the (beginning|dawn)|generations?|lifetimes?|over time|the age of the universe)\b'),
    ('expansion',   r'\b(expand\w*|stretch\w*|inflat\w*|swell\w*|grow(s|ing)? (bigger|larger|wider|apart)|spread\w* (out|apart)|further apart|balloon\w*|widen\w*|dilat\w*)\b'),
    ('lightspeed',  r'\b(speed of light|light.?speed|light.?years?|photons?|the fastest|faster than|nothing (is|can be) faster|at light|beam of light|a ray of)\b'),
    ('gravity',     r'\b(gravit\w*|pull\w* (in|down|toward|together)|attract\w*|orbit\w*|fall\w* (in|into|toward)|weight\w*|heavy|heavier|mass(es)?\b|tidal|sink\w*|collaps\w*|crush\w*)\b'),
    ('cold_empty',  r'\b(cold|colder|coldest|freez\w*|frozen|empty|emptiness|void|vacuum|nothing(ness)?|silence|silent|lonely|alone|desolate|barren|dark(ness|er|est)?|pitch.?black|absolute zero)\b'),
    ('observe',     r'\b(observ\w*|telescop\w*|microscop\w*|look(ed|ing|s)? (at|up|closer|through)|watch\w*|measur\w*|detect\w*|record\w*|scan\w*|peer\w*|examin\w*|inspect\w*|notice\w*|spot(ted|s)?\b|zoom\w*|lens\w*|instrument\w*)\b'),
    ('unknown',     r'\b(nobody knows|no one knows|we don.?t know|unknown|myster\w*|puzzl\w*|riddle\w*|unsolved|unanswered|debat\w*|hypothes\w*|theor\w*|speculat\w*|perhaps|maybe|might be|could be|why\b|what if|question\w*)\b'),
    ('birth',       r'\b(born|birth\w*|hatch\w*|bloom\w*|sprout\w*|emerg\w*|begin\w*|began|beginning|start\w*|the first|dawn of|form(ed|s|ing)?\b|creat\w*|ignit\w*|awaken\w*|new(born)?\b)\b'),
    ('death',       r'\b(died?|dies|dying|death\w*|dead|extinct\w*|perish\w*|vanish\w*|disappear\w*|fade\w* (away|out)|the end\b|ends?\b|ending|last (breath|days?|moments?)|collapse\w*|burn\w* out|gone\b|lost forever|ruins?)\b'),
    ('journey',     r'\b(journey\w*|travel\w*|voyag\w*|trip\b|cross\w*|reach\w*|arriv\w*|set (off|out|sail)|depart\w*|miles|kilomet\w*|destination\w*|far away|distan\w*|route\w*|path\w*|wander\w*|migrat\w*|drift\w*)\b'),
    ('danger',      r'\b(danger\w*|deadly|lethal|threat\w*|risk\w*|warn\w*|attack\w*|kill\w*|destroy\w*|explo\w*|erupt\w*|crash\w*|collid\w*|poison\w*|venom\w*|trap\w*|hunt(ed|s|ing)?\b|prey|predator\w*|escape\w*|survive?\w*)\b'),
    ('discovery',   r'\b(discover\w*|found\b|finds?\b|finding|reveal\w*|uncover\w*|evidence|clue\w*|proof|proved?|breakthrough\w*|first time|turns? out|realiz\w*|realis\w*|figured out|secret\w*|surpris\w*|unexpected\w*)\b'),
    ('counting',    r'\b(\d{1,3}(,\d{3})+|\d+(\.\d+)?\s*(percent|%|degrees|tons?|kilograms?|kg|meters?|metres?|km|miles|times)|countless|hundreds|thousands|millions|billions|trillions|dozens?|a handful|how many|numbers?|count\w*|calculat\w*|estimat\w*|statistic\w*)\b'),
    ('change',      r'\b(chang\w*|transform\w*|turn(s|ed|ing)? into|becom\w*|became|evolv\w*|mutat\w*|shift\w*|convert\w*|adapt\w*|reshap\w*|rebuil\w*|melt\w*|cool(s|ed|ing)? down|heat\w* up|decay\w*|rust\w*|age(s|d)?\b)\b'),
    ('speed',       r'\b(fast(er|est)?|quick\w*|rapid\w*|rush\w*|racing|race\b|sprint\w*|instant\w*|in a flash|blink of an eye|sudden\w*|accelerat\w*|hurtl\w*|zoom\w*|whizz\w*|speed\w*)\b'),
    ('slowness',    r'\b(slow(ly|er|est)?|gradual\w*|patien\w*|crawl\w*|inch(es|ed|ing)? (forward|along|closer)|took (centuries|ages|years|decades)|wait(ed|ing|s)?\b|linger\w*|creep\w*|at a snail|bit by bit|little by little)\b'),
    ('hidden',      r'\b(hidden|hide\w*|hiding|invisible|unseen|beneath|underneath|buried|below the surface|behind|lurk\w*|conceal\w*|camouflag\w*|disguis\w*|in the shadows|under the)\b'),
    ('giant_tiny',  r'\b(giants?|giant\b|huge|massive|titanic|towering|tiny|little|small(er|est)?|miniature|dwarf\w*|mini\b|micro\w*|nano\w*|the largest|the biggest|the smallest)\b'),
    ('home_safe',   r'\b(home\w*|safe(ty|ly)?|shelter\w*|protect\w*|warm\w*|comfort\w*|cozy|rest\w*|peace\w*|calm\w*|quiet\w*|family|together|belong\w*|nest\w*|refuge)\b'),
    ('signal',      r'\b(signal\w*|messag\w*|radio|broadcast\w*|transmit\w*|receiv\w*|hear\w*|listen\w*|sound\w*|echo\w*|voice\w*|call(ed|s|ing)? out|communicat\w*|whisper\w*|noise\w*|ring\w*|ping\w*)\b'),
    ('heat',        r'\b(hot(ter|test)?|heat\w*|burn\w*|boil\w*|scorch\w*|blaz\w*|fire\w*|flame\w*|molten|lava|furnace|degrees|sun\w*|glow\w*|bright\w*)\b'),
    ('food',        r'\b(eat\w*|ate\b|food\w*|feed\w*|hungry|hunger|starv\w*|meal\w*|feast\w*|swallow\w*|digest\w*|chew\w*|bite\w*|taste\w*|cook\w*)\b'),
    ('build',       r'\b(build\w*|built|construct\w*|engineer\w*|design\w*|assembl\w*|invent\w*|machine\w*|tool\w*|hammer\w*|repair\w*|fix(ed|es|ing)?\b|craft\w*|forg\w*)\b'),
    ('celebrate',   r'\b(celebrat\w*|victor\w*|triumph\w*|succe\w*|won\b|win(s|ning)?\b|achiev\w*|record\b|champion\w*|hero\w*|cheer\w*|festival\w*|parade\w*|proud\w*)\b'),
]
CONCEPTS = [(c, re.compile(rx, re.I)) for c, rx in CONCEPTS]


def concepts_of(text):
    """idea classes of a unit text, ordered by where they first occur (the earliest idea leads)"""
    found = []
    for c, rx in CONCEPTS:
        m = rx.search(text)
        if m: found.append((m.start(), c))
    return [c for _, c in sorted(found)]


# ---------------------------------------------------------------- act pools: concept -> domain -> [(act, mood, say)]
# act names: frog_rig.COSTUME_ACTS / CONCEPT_ACTS (data-driven), frog.SIMPLE_ACTS, frog_place relation acts; '*' = any domain. say None = the act's own word (OUTFIT_SAYS / says_for).
CONCEPT_ACTS = {
 'scale':      {'*': [('measure', 'curious', 'This big!'), ('shrinkdown', 'surprised', 'Tiny me...'), ('growtall', 'proud', 'Huge!'), ('binocs', 'curious', None), ('peer', 'squint', 'Hmm...')],
                'space': [('measure', 'surprised', 'Thaaat big?'), ('shrinkdown', 'surprised', 'So small...'), ('countstars', 'curious', 'Wow...'), ('growtall', 'surprised', None)]},
 'timespan':   {'*': [('slowwalk', 'sleepy', 'Still going...'), ('yawn', 'sleepy', None), ('stretch', 'sleepy', None), ('countfingers', 'curious', 'One... two...'), ('oldman', 'sleepy', 'Ages...')],
                'time': [('oldman', 'sleepy', 'Tick... tock...'), ('countfingers', 'curious', None), ('slowwalk', 'sleepy', None)]},
 'expansion':  {'*': [('stretchwide', 'surprised', 'Whoa, wider!'), ('growtall', 'surprised', None), ('pushaway', 'determined', 'Further!')],
                'space': [('stretchwide', 'surprised', 'Everything stretches!'), ('pushaway', 'surprised', 'Drifting apart...'), ('zerogroll', 'dizzy', 'Whoa-oa...')]},
 'lightspeed': {'*': [('speedrun', 'determined', 'Zoooom!'), ('sunshade', 'squint', 'Bright!'), ('binocs', 'curious', None)],
                'space': [('speedrun', 'excited', 'Light speed!'), ('sunshade', 'squint', 'So bright!'), ('starcatch', 'happy', 'Gotcha!')]},
 'gravity':    {'*': [('leanback', 'squint', 'Heavy...'), ('pushaway', 'determined', 'Hnnng!'), ('balance', 'squint', None), ('magnetwalk', 'determined', 'Stuck!')],
                'space': [('magnetwalk', 'determined', 'Magnet boots!'), ('zerogroll', 'dizzy', 'Wheee...'), ('leanback', 'squint', 'Pulling...')]},
 'cold_empty': {'*': [('hug', 'chilly', 'Brrr...'), ('rubhands', 'chilly', None), ('listen', 'curious', 'So quiet...'), ('search', 'worried', 'Anyone?')],
                'space': [('hug', 'chilly', 'So cold...'), ('search', 'worried', 'Hello...?'), ('listen', 'curious', 'Nothing...'), ('zerogroll', 'sleepy', None)]},
 'observe':    {'*': [('binocs', 'curious', None), ('peer', 'squint', 'Let me see...'), ('magnify', 'curious', None), ('photo', 'happy', None), ('write', 'curious', None)],
                'space': [('scope', 'curious', None), ('binocs', 'curious', 'Ooh!'), ('countstars', 'curious', None), ('write', 'curious', None)],
                'body': [('magnify', 'curious', None), ('peer', 'squint', None), ('write', 'curious', None), ('listen', 'curious', 'Thump, thump.')]},
 'unknown':    {'*': [('shrug', 'worried', None), ('think', 'curious', None), ('chinrub', 'curious', 'Hmm...'), ('search', 'squint', None), ('pacing', 'curious', 'Why...?')]},
 'birth':      {'*': [('gasp', 'surprised', 'Oh!'), ('present', 'proud', 'Ta-da!'), ('cheer', 'excited', None), ('stretch', 'sleepy', None)],
                'space': [('gasp', 'surprised', 'A new star!'), ('starcatch', 'happy', None), ('present', 'proud', 'Ta-da!')],
                'bio': [('gasp', 'surprised', 'Hatching!'), ('peer', 'curious', None), ('present', 'proud', None)]},
 'death':      {'*': [('cry', 'sad', None), ('bow', 'sad', '...'), ('hug', 'sad', None), ('wish', 'sad', None)]},
 'journey':    {'*': [('hike', 'determined', None), ('binocs', 'curious', 'There!'), ('slowwalk', 'determined', 'Long way...'), ('pointfar', 'excited', 'That way!'), ('pacing', 'curious', None)],
                'space': [('jetpack', 'excited', 'Whoosh!'), ('pointfar', 'excited', 'To the stars!'), ('moonbounce', 'happy', 'Boing!'), ('pushoff', 'determined', 'Push off!')],
                'sea': [('swimstroke', 'happy', None), ('paddle', 'determined', None), ('binocs', 'curious', 'Land ho!')]},
 'danger':     {'*': [('nervous', 'worried', None), ('hide', 'scared', None), ('tiptoe', 'worried', None), ('gasp', 'scared', 'Eek!'), ('peek', 'scared', None)],
                'space': [('nervous', 'worried', None), ('duck', 'scared', 'Incoming!'), ('hide', 'scared', None), ('helmetwipe', 'worried', 'Phew...')]},
 'discovery':  {'*': [('idea', 'excited', None), ('gasp', 'surprised', 'Aha!'), ('present', 'proud', 'Look!'), ('magnify', 'curious', None), ('clap', 'proud', None)]},
 'counting':   {'*': [('countfingers', 'curious', 'One, two...'), ('write', 'curious', None), ('measure', 'curious', None), ('think', 'curious', None)],
                'space': [('countstars', 'curious', 'Countless...'), ('countfingers', 'curious', None), ('write', 'curious', None)]},
 'change':     {'*': [('spinaround', 'surprised', 'Whoa!'), ('shrinkdown', 'surprised', None), ('growtall', 'surprised', None), ('oldman', 'sleepy', None), ('gasp', 'surprised', None)]},
 'speed':      {'*': [('speedrun', 'determined', 'Zoom!'), ('jog', 'determined', None), ('leanback', 'squint', 'Whoa!'), ('spinaround', 'dizzy', None)],
                'space': [('jetpack', 'excited', 'Zoooom!'), ('speedrun', 'determined', None), ('pushoff', 'determined', None)]},
 'slowness':   {'*': [('slowwalk', 'sleepy', 'Sooo slow...'), ('yawn', 'sleepy', None), ('snooze', 'sleepy', None), ('pacing', 'curious', 'Still waiting...')]},
 'hidden':     {'*': [('peek', 'curious', None), ('search', 'squint', None), ('duck', 'curious', 'Shh...'), ('magnify', 'curious', None), ('tiptoe', 'curious', None)]},
 'giant_tiny': {'*': [('growtall', 'proud', 'Big!'), ('shrinkdown', 'surprised', 'Small!'), ('measure', 'curious', None), ('peer', 'squint', None)]},
 'home_safe':  {'*': [('hug', 'love', None), ('rest', 'happy', None), ('wave', 'happy', None), ('stretch', 'sleepy', None), ('snooze', 'sleepy', None)]},
 'signal':     {'*': [('listen', 'curious', None), ('cupshout', 'excited', 'Hellooo!'), ('wavebig', 'happy', 'Over here!'), ('startle', 'surprised', None)],
                'space': [('listen', 'curious', 'Beep... beep...'), ('cupshout', 'excited', 'Anyone out there?'), ('wavebig', 'happy', 'Hi, Earth!')]},
 'heat':       {'*': [('sunshade', 'squint', 'Hot!'), ('fan', 'hot', 'Phew...'), ('shrinkdown', 'squint', None)]},
 'food':       {'*': [('eat', 'happy', None), ('chomp', 'mischief', None), ('rubbelly', 'happy', 'Yum!'), ('sniff', 'love', None)]},
 'build':      {'*': [('hammer', 'determined', None), ('measure', 'curious', None), ('write', 'curious', None), ('present', 'proud', None), ('flex', 'proud', None)]},
 'celebrate':  {'*': [('clap', 'proud', None), ('victory', 'proud', None), ('dance', 'excited', None), ('tosscap', 'proud', None), ('wavebig', 'happy', 'Hooray!')]},
}
# 2026-10-31 (miya: "개념 규칙도 우주만이 아닌 전체 적용"): domain flavours for the other packs too; the '*' pool is the fallback everywhere
_MORE = {
 ('scale', 'sea'):       [('measure', 'surprised', 'Whale-sized!'), ('shrinkdown', 'surprised', 'Plankton me...'), ('swimstroke', 'curious', None), ('peer', 'squint', None)],
 ('scale', 'history'):   [('measure', 'curious', 'Pyramid-tall!'), ('growtall', 'proud', 'Colossal!'), ('binocs', 'curious', None), ('countfingers', 'curious', None)],
 ('scale', 'body'):      [('shrinkdown', 'surprised', 'Cell-sized!'), ('magnify', 'curious', None), ('measure', 'curious', 'This long?'), ('peer', 'squint', None)],
 ('scale', 'bio'):       [('shrinkdown', 'surprised', 'Bug-sized!'), ('growtall', 'proud', 'Dino big!'), ('magnify', 'curious', None), ('measure', 'curious', None)],
 ('scale', 'earth'):     [('measure', 'curious', 'Mountain-high!'), ('binocs', 'curious', None), ('hike', 'determined', None), ('growtall', 'proud', None)],
 ('scale', 'tech'):      [('measure', 'curious', 'Nano!'), ('shrinkdown', 'surprised', None), ('vrgrab', 'curious', None), ('magnify', 'curious', None)],
 ('timespan', 'history'): [('oldman', 'sleepy', 'Centuries...'), ('write', 'curious', None), ('slowwalk', 'sleepy', None), ('pray', 'curious', None)],
 ('timespan', 'bio'):    [('oldman', 'sleepy', 'Generations...'), ('sow', 'happy', None), ('countfingers', 'curious', None), ('yawn', 'sleepy', None)],
 ('timespan', 'earth'):  [('oldman', 'sleepy', 'Eons...'), ('dig2', 'curious', None), ('slowwalk', 'sleepy', None), ('stretch', 'sleepy', None)],
 ('expansion', 'bio'):   [('stretchwide', 'surprised', 'Spreading!'), ('sow', 'happy', None), ('growtall', 'surprised', None)],
 ('expansion', 'tech'):  [('stretchwide', 'surprised', 'Everywhere!'), ('vrgrab', 'curious', None), ('present', 'proud', None)],
 ('gravity', 'earth'):   [('leanback', 'squint', 'Heavy...'), ('stomp', 'determined', None), ('balance', 'squint', None), ('puddlejump', 'happy', None)],
 ('gravity', 'sea'):     [('paddle', 'determined', 'Sinking...'), ('leanback', 'squint', None), ('swimstroke', 'determined', None)],
 ('cold_empty', 'sea'):  [('hug', 'chilly', 'Cold down here...'), ('rubhands', 'chilly', None), ('listen', 'curious', 'So quiet...'), ('swimstroke', 'chilly', None)],
 ('cold_empty', 'earth'): [('hug', 'chilly', 'Brrr!'), ('rubhands', 'chilly', None), ('windbrella', 'squint', None), ('stomp', 'chilly', 'Cold feet!')],
 ('cold_empty', 'history'): [('hug', 'sad', 'All gone...'), ('search', 'worried', 'Anyone?'), ('listen', 'curious', None), ('pray', 'sad', None)],
 ('observe', 'sea'):     [('swimstroke', 'curious', None), ('peer', 'squint', 'Down there...'), ('photo', 'happy', None), ('binocs', 'curious', None)],
 ('observe', 'history'): [('magnify', 'curious', None), ('write', 'curious', 'Noted.'), ('peer', 'squint', None), ('photo', 'happy', None)],
 ('observe', 'bio'):     [('magnify', 'curious', 'Look closer!'), ('sniff', 'curious', None), ('peer', 'squint', None), ('photo', 'happy', None), ('write', 'curious', None)],
 ('observe', 'tech'):    [('vrgrab', 'curious', None), ('magnify', 'curious', None), ('write', 'curious', None), ('peer', 'squint', 'Hmm...')],
 ('observe', 'earth'):   [('binocs', 'curious', None), ('dig2', 'curious', None), ('photo', 'happy', None), ('measure', 'curious', None)],
 ('unknown', 'history'): [('chinrub', 'curious', 'Who knows...'), ('shrug', 'worried', None), ('search', 'squint', None), ('write', 'curious', '?')],
 ('unknown', 'sea'):     [('peer', 'squint', 'Too dark...'), ('shrug', 'worried', None), ('swimstroke', 'curious', None), ('chinrub', 'curious', None)],
 ('birth', 'body'):      [('gasp', 'surprised', 'Hello!'), ('hug', 'love', None), ('present', 'proud', None), ('stretch', 'sleepy', None)],
 ('birth', 'earth'):     [('gasp', 'surprised', 'A new land!'), ('sow', 'happy', None), ('present', 'proud', None)],
 ('death', 'bio'):       [('cry', 'sad', None), ('bow', 'sad', '...'), ('sniff', 'sad', None), ('wish', 'sad', None)],
 ('death', 'history'):   [('bow', 'sad', '...'), ('pray', 'sad', None), ('cry', 'sad', None), ('hug', 'sad', None)],
 ('death', 'sea'):       [('bow', 'sad', '...'), ('swimstroke', 'sad', None), ('wish', 'sad', None), ('hug', 'sad', None)],
 ('journey', 'history'): [('hike', 'determined', 'Onward!'), ('pointfar', 'excited', 'That way!'), ('slowwalk', 'determined', None), ('regal', 'proud', None)],
 ('journey', 'earth'):   [('hike', 'determined', None), ('climb', 'determined', 'Up we go!'), ('pointfar', 'excited', None), ('skate', 'happy', None)],
 ('journey', 'bio'):     [('hike', 'determined', None), ('flap', 'happy', 'Migrating!'), ('crawl', 'determined', None), ('pointfar', 'excited', None)],
 ('journey', 'body'):    [('swimstroke', 'determined', 'Through the vein!'), ('crawl', 'determined', None), ('pointfar', 'excited', None)],
 ('journey', 'tech'):    [('speedrun', 'determined', None), ('skate', 'happy', None), ('pointfar', 'excited', None), ('charge', 'determined', None)],
 ('danger', 'sea'):      [('hideshell', 'scared', None), ('paddle', 'scared', 'Shark?!'), ('nervous', 'worried', None), ('peek', 'scared', None)],
 ('danger', 'bio'):      [('hideshell', 'scared', None), ('tiptoe', 'worried', None), ('gasp', 'scared', 'Eek!'), ('duck', 'scared', None), ('coverears', 'scared', None)],
 ('danger', 'history'):  [('hide', 'scared', None), ('duck', 'scared', 'Take cover!'), ('halt', 'worried', None), ('nervous', 'worried', None)],
 ('danger', 'body'):     [('nervous', 'worried', None), ('coverears', 'scared', None), ('gasp', 'scared', 'Uh-oh!'), ('hide', 'scared', None)],
 ('danger', 'earth'):    [('duck', 'scared', 'Look out!'), ('hide', 'scared', None), ('windbrella', 'squint', None), ('nervous', 'worried', None)],
 ('danger', 'tech'):     [('halt', 'worried', 'Stop!'), ('duck', 'scared', None), ('coverears', 'scared', None), ('nervous', 'worried', None)],
 ('discovery', 'history'): [('gasp', 'surprised', 'Aha!'), ('dig2', 'excited', None), ('present', 'proud', 'Found it!'), ('magnify', 'curious', None)],
 ('discovery', 'bio'):   [('magnify', 'curious', None), ('gasp', 'surprised', 'A new one!'), ('present', 'proud', None), ('photo', 'happy', None)],
 ('discovery', 'sea'):   [('gasp', 'surprised', 'Down there!'), ('swimstroke', 'excited', None), ('present', 'proud', None), ('photo', 'happy', None)],
 ('discovery', 'tech'):  [('idea', 'excited', None), ('present', 'proud', 'It works!'), ('vrgrab', 'curious', None), ('clap', 'proud', None)],
 ('counting', 'history'): [('countfingers', 'curious', None), ('write', 'curious', 'Tally...'), ('measure', 'curious', None)],
 ('counting', 'bio'):    [('countfingers', 'curious', 'So many!'), ('magnify', 'curious', None), ('write', 'curious', None)],
 ('change', 'bio'):      [('spinaround', 'surprised', 'Whoa!'), ('growtall', 'surprised', 'Grew!'), ('shrinkdown', 'surprised', None), ('flap', 'happy', None)],
 ('change', 'history'):  [('oldman', 'sleepy', None), ('spinaround', 'surprised', None), ('regal', 'proud', 'New king!'), ('gasp', 'surprised', None)],
 ('change', 'earth'):    [('spinaround', 'surprised', None), ('dig2', 'curious', None), ('windbrella', 'squint', None), ('gasp', 'surprised', None)],
 ('speed', 'sea'):       [('swimstroke', 'determined', 'Zoom!'), ('paddle', 'determined', None), ('leanback', 'squint', None)],
 ('speed', 'bio'):       [('speedrun', 'determined', None), ('flap', 'excited', 'Whoosh!'), ('leap', 'excited', None), ('jog', 'determined', None)],
 ('speed', 'tech'):      [('charge', 'determined', None), ('speedrun', 'determined', 'Zoom!'), ('skate', 'happy', None), ('spinaround', 'dizzy', None)],
 ('slowness', 'bio'):    [('crawl', 'sleepy', 'Sooo slow...'), ('slowwalk', 'sleepy', None), ('yawn', 'sleepy', None)],
 ('slowness', 'sea'):    [('swimstroke', 'sleepy', None), ('slowwalk', 'sleepy', 'Drifting...'), ('snooze', 'sleepy', None)],
 ('hidden', 'sea'):      [('hideshell', 'curious', None), ('peek', 'curious', None), ('peer', 'squint', 'Down there...'), ('swimstroke', 'curious', None)],
 ('hidden', 'body'):     [('magnify', 'curious', None), ('peek', 'curious', None), ('peer', 'squint', 'Inside...'), ('search', 'squint', None)],
 ('hidden', 'history'):  [('dig2', 'curious', None), ('magnify', 'curious', None), ('peek', 'curious', None), ('search', 'squint', 'Where...?')],
 ('hidden', 'earth'):    [('dig2', 'curious', 'Buried!'), ('peek', 'curious', None), ('search', 'squint', None)],
 ('home_safe', 'bio'):   [('hug', 'love', None), ('rest', 'happy', None), ('sow', 'happy', None), ('snooze', 'sleepy', None)],
 ('home_safe', 'sea'):   [('hideshell', 'happy', 'Cozy!'), ('rest', 'happy', None), ('wave', 'happy', None)],
 ('signal', 'sea'):      [('listen', 'curious', 'Whale song!'), ('cupshout', 'excited', None), ('wavebig', 'happy', None)],
 ('signal', 'bio'):      [('listen', 'curious', None), ('cupshout', 'excited', 'Hellooo!'), ('flap', 'happy', None), ('sniff', 'curious', None)],
 ('signal', 'tech'):     [('listen', 'curious', 'Beep!'), ('cupshout', 'excited', None), ('vrgrab', 'curious', None), ('startle', 'surprised', None)],
 ('heat', 'earth'):      [('fan', 'hot', 'Phew...'), ('sunshade', 'squint', 'Hot!'), ('hose', 'determined', None), ('shrinkdown', 'squint', None)],
 ('heat', 'body'):       [('fan', 'hot', 'Fever...'), ('sunshade', 'squint', None), ('faint', 'dizzy', None)],
 ('food', 'sea'):        [('chomp', 'mischief', None), ('eat', 'happy', None), ('rubbelly', 'happy', 'Yum!'), ('sniff', 'love', None)],
 ('food', 'bio'):        [('eat', 'happy', None), ('sniff', 'love', None), ('chomp', 'mischief', 'Chomp!'), ('stir', 'happy', None)],
 ('food', 'history'):    [('eat', 'happy', None), ('stir', 'happy', None), ('rubbelly', 'happy', 'Feast!'), ('chomp', 'mischief', None)],
 ('build', 'history'):   [('hammer', 'determined', None), ('measure', 'curious', None), ('stomp', 'determined', None), ('present', 'proud', 'Done!')],
 ('build', 'tech'):      [('hammer', 'determined', None), ('vrgrab', 'curious', None), ('write', 'curious', None), ('present', 'proud', 'Done!')],
 ('build', 'bio'):       [('sow', 'happy', None), ('dig2', 'determined', None), ('hammer', 'determined', None), ('present', 'proud', None)],
 ('celebrate', 'history'): [('regal', 'proud', None), ('tosscap', 'proud', None), ('clap', 'proud', None), ('wavebig', 'happy', 'Hooray!')],
 ('celebrate', 'sea'):   [('puddlejump', 'happy', 'Splash!'), ('clap', 'proud', None), ('wavebig', 'happy', None), ('victory', 'proud', None)],
}
for (c, d), pool in _MORE.items(): CONCEPT_ACTS[c][d] = pool

# a unit without any concept: the domain's own filler pool (replaces the old tilt / look / sway / nod / breathe cycle), still least-used first
DOMAIN_FILLER = {
 'space':   [('zerogroll', 'happy', None), ('countstars', 'curious', None), ('helmetwipe', 'squint', None), ('moonbounce', 'happy', None), ('binocs', 'curious', None), ('starcatch', 'happy', None), ('magnetwalk', 'determined', None), ('look', 'curious', None)],
 'sea':     [('swimstroke', 'happy', None), ('bob', 'happy', None), ('binocs', 'curious', None), ('peer', 'curious', None), ('wavebig', 'happy', None), ('look', 'curious', None)],
 'history': [('read', 'curious', None), ('salute', 'proud', None), ('bow', 'proud', None), ('write', 'curious', None), ('pacing', 'curious', None), ('present', 'proud', None), ('tilt', 'curious', None)],
 'body':    [('listen', 'curious', None), ('magnify', 'curious', None), ('peer', 'squint', None), ('write', 'curious', None), ('rubbelly', 'happy', None), ('tilt', 'curious', None)],
 'bio':     [('peer', 'curious', None), ('magnify', 'curious', None), ('sniff', 'love', None), ('binocs', 'curious', None), ('photo', 'happy', None), ('tiptoe', 'curious', None), ('look', 'curious', None)],
 'time':    [('countfingers', 'curious', None), ('pacing', 'curious', None), ('yawn', 'sleepy', None), ('oldman', 'sleepy', None), ('listen', 'curious', None), ('tilt', 'curious', None)],
 'earth':   [('binocs', 'curious', None), ('hike', 'determined', None), ('sunshade', 'squint', None), ('peer', 'curious', None), ('balance', 'squint', None), ('look', 'curious', None)],
 'tech':    [('hammer', 'determined', None), ('write', 'curious', None), ('listen', 'curious', None), ('tap', 'curious', None), ('think', 'curious', None), ('present', 'proud', None)],
 'generic': [('tilt', 'curious', None), ('look', 'curious', None), ('think', 'curious', None), ('peer', 'curious', None), ('shrug', 'worried', None), ('wave', 'happy', None), ('nod', 'happy', None)],
}

# ---------------------------------------------------------------- outfit packs: base (worn when the domain's physics asks) + accessories rotated on top
PACK_OUTFITS = {
 'space':   dict(base='helmet', extra=['jetpack', 'moonboots', 'goldvisor', 'antenna', 'patch', 'backpack', None]),
 'sea':     dict(base=None, extra=['flippers', 'sailorhat', 'lifering', 'captainhat', 'shellhat', None]),
 'history': dict(base=None, extra=['toga', 'shield', 'turban', 'feathercap', 'crown', 'knight', 'laurel', 'tophat', 'monocle', None]),
 'body':    dict(base=None, extra=['doctor', 'lab', 'facemask', 'glasses', 'headlamp', None]),
 'bio':     dict(base=None, extra=['leafhat', 'explorer', 'bee', 'flowercrown', 'backpack', 'strawhat', None]),
 'time':    dict(base=None, extra=['clockhat', 'pocketwatch', 'nightcap', 'glasses', 'tophat', None]),
 'earth':   dict(base=None, extra=['explorer', 'raincoat', 'scarf', 'sunglasses', 'hardhat', 'headlamp', None]),
 'tech':    dict(base=None, extra=['hardhat', 'goggles', 'vr', 'headphones', 'tinfoil', 'glasses', None]),
 'generic': dict(base=None, extra=['cap', 'bowler', 'bowtie', 'beanie', 'glasses', 'headband', None]),
}

# ---------------------------------------------------------------- picture-side packs (for art_spec / briefs and variety_check): props to draw MOVING (named), object motions that fit, compositions
PACK_PICTURE = {
 'space':   dict(props='floating wrench (mv-coast), tumbling meteorite (mv-rollby or mv-core-drop), small satellite (mv-rotor dish + mv-path), comet (mv-path + tail), light beam (mv-dash), planted flag (mv-flagwave), lander leg (mv-joint), tether rope (mv-swing), ring of asteroids (mv-orbit), floating snack (mv-coast), helmet / tool drifting by (mv-coast)',
                motions='orbit spin core-spin swell heartbeat path coast rollby core-drop dash flagwave rotor swing magnet rise sink popin',
                compositions='wide field with a small subject; close-up inside a helmet / cockpit; split frame (then vs now); object seen from above; a ruler or a stack of familiar things for scale; diagram on a dark board'),
 'sea':     dict(props='rising bubbles (mv-bubble), crab (mv-creep), jellyfish (mv-wiggle), dropped anchor (mv-core-drop), buoy (mv-bob), seaweed (mv-sway), fish (mv-swim), ship wheel (mv-rotor), swinging lantern (mv-pendulum), falling marine snow (code), rolling barrel (mv-rollby)',
                motions='swim bob bubble sway ripple wiggle creep path rotor pendulum core-drop rollby rise sink',
                compositions='surface split (above / below water); silhouette against light from above; close-up of a creature; wide seafloor; inside a submarine window; cross-section depth chart'),
 'history': dict(props='catapult arm (mv-joint), banner (mv-flagwave), tossed coin (mv-toss), unrolling scroll (mv-unroll), cart wheel (mv-rotor), tolling bell (mv-pendulum), candle (mv-flame), hourglass (mv-flip), swinging gate (mv-swing), toppling column (mv-topple), rolling barrel (mv-rollby)',
                motions='flagwave joint toss unroll rotor pendulum flame flip swing topple rollby path march',
                compositions='map with a moving marker; portrait frame; battlefield wide shot; inside a hall; scroll / parchment inset; timeline strip'),
 'body':    dict(props='pulsing cell (mv-breathe), heart (mv-core-heartbeat), microscope knob (mv-rotor), petri dish (mv-popin), DNA strand (mv-spin), bouncing blood drop (mv-bouncing), pill (mv-rollby), syringe (mv-slide), swinging stethoscope (mv-pendulum)',
                motions='breathe heartbeat rotor popin spin bouncing rollby slide pendulum liquid fill',
                compositions='zoom from body to organ to cell; x-ray silhouette; split healthy / sick; lab bench close-up; chart with a moving needle'),
 'bio':     dict(props='falling leaf (mv-core-drop), hopping frog (mv-hop), hovering insect (mv-hover), wobbling egg (mv-wobble then mv-popin hatch), swaying reed (mv-sway), creeping snail (mv-creep), flapping bird (mv-flap), swinging vine (mv-swing), rolling nut (mv-rollby), tadpole (mv-wiggle)',
                motions='hop hover wobble popin sway creep flap swing rollby wiggle swim path core-drop',
                compositions='life-cycle ring; predator / prey split; close-up of eyes; wide habitat; underground cross-section; size ladder'),
 'time':    dict(props='clock hand (mv-rotor on the dial), pendulum (mv-pendulum), hourglass (mv-flip), calendar page (mv-flip / mv-unroll), sundial shadow (mv-rotor), metronome (mv-pendulum), falling sand (code), gears (mv-rotor pair), rolling marble on a track (mv-rollby)',
                motions='rotor pendulum flip unroll ticks rollby scroll fade',
                compositions='clock face full frame; two clocks side by side; a day as a strip; the same place in two eras; a racing track for time'),
 'earth':   dict(props='rolling boulder (mv-rollby), erupting rock (mv-toss), falling snow (code), swaying tree (mv-sway), cracking ice (mv-popin), spinning weather vane (mv-rotor), blowing flag (mv-flagwave), rising smoke (code), drifting raft (mv-bob), tumbling tumbleweed (mv-rollby)',
                motions='rollby toss sway popin rotor flagwave bob path topple rise sink ripple',
                compositions='cross-section of the ground; horizon wide shot; before / after; close-up of a crack; map with arrows'),
 'tech':    dict(props='turning gears (mv-rotor pair, meshing), piston (mv-slide), blinking light (mv-flicker), conveyor box (mv-slide), robot arm (mv-joint), spinning dish (mv-rotor), bouncing ball bearing (mv-bouncing), switch lever (mv-joint), ticker tape (mv-unroll)',
                motions='rotor slide flicker joint bouncing unroll dash scroll popin',
                compositions='exploded diagram; inside the machine; control panel close-up; assembly line wide; circuit as a map'),
 'generic': dict(props='a small thing falling from above (mv-core-drop), a toppling post (mv-topple), a rolling ball (mv-rollby), a bouncing ball (mv-bouncing), a swinging sign (mv-swing), a rising balloon (mv-rise), a tossed coin (mv-toss)',
                motions='core-drop topple rollby bouncing swing rise toss popin path',
                compositions='close-up; wide; split; from above; inset diagram'),
}


# ---------------------------------------------------------------- deterministic least-used picking
class Tally:
    """counts per family ('act', 'outfit', ...) across one video; pick() returns the least-used entry of a pool, ties broken by the unit index"""
    def __init__(self): self.c = {}

    def pick(self, family, pool, k, key=lambda e: e[0] if isinstance(e, (tuple, list)) else e):
        if not pool: return None
        cnt = self.c.setdefault(family, {})
        lo = min(cnt.get(key(e), 0) for e in pool); cands = [e for e in pool if cnt.get(key(e), 0) == lo]
        e = cands[k % len(cands)]; cnt[key(e)] = cnt.get(key(e), 0) + 1
        return e

    def note(self, family, name): c = self.c.setdefault(family, {}); c[name] = c.get(name, 0) + 1


def act_pool(text, domain):
    """the act pool for a unit: the leading concept's domain pool (or '*'), else the domain filler. Returns (concept, pool)."""
    for c in concepts_of(text):
        pools = CONCEPT_ACTS.get(c) or {}
        pool = pools.get(domain) or pools.get('*')
        if pool: return c, pool
    return None, DOMAIN_FILLER.get(domain) or DOMAIN_FILLER['generic']


def doc():
    L = ['# Concept rules and theme packs (generated from tools/concepts.py: `python3 tools/concepts.py --doc`)', '',
         '## Concepts (idea classes read from the unit text, first occurrence leads)', '', '| concept | words (sample) | acts (any domain) | space pool |', '|---|---|---|---|']
    for c, rx in CONCEPTS:
        words = rx.pattern.strip('\\b()').split('|')[:6]
        p = CONCEPT_ACTS.get(c, {}); L.append(f"| {c} | {', '.join(w.replace(chr(92), '') for w in words)} … | {' '.join(a for a, _, _ in p.get('*', []))} | {' '.join(a for a, _, _ in p.get('space', [])) or '(= any)'} |")
    L += ['', '## Theme packs', '', '| domain | filler acts | outfit base + accessories | props to draw moving | object motions | compositions |', '|---|---|---|---|---|---|']
    for d in PACK_PICTURE:
        o = PACK_OUTFITS[d]; L.append(f"| {d} | {' '.join(a for a, _, _ in DOMAIN_FILLER[d])} | {o['base'] or '-'} + {' '.join(x or '(none)' for x in o['extra'])} | {PACK_PICTURE[d]['props']} | {PACK_PICTURE[d]['motions']} | {PACK_PICTURE[d]['compositions']} |")
    L += ['', 'Picking: the least-used entry of the pool so far in the video; ties -> unit index. Word rules (frog_place ACTS, contact / locomotion picks) run first; this layer fills every unit they left on a default.']
    return '\n'.join(L) + '\n'


if __name__ == '__main__':
    import sys
    if '--doc' in sys.argv: print(doc())
    else:   # a slug: the video's theme pack and every unit's domain / idea class; any other text: its domain and classes
        import os, json
        for a in sys.argv[1:]:
            pj = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'videos', a, 'plan.json')
            if os.path.exists(pj):
                plan = json.load(open(pj)); vd = video_domain([u['text'] for u in plan], [(u.get('pal') or {}).get('palette', '') for u in plan])
                print(a, 'theme pack:', vd, '| props:', PACK_PICTURE[vd]['props'], '| compositions:', PACK_PICTURE[vd]['compositions'])
                for u in plan: print(' ', u['uid'], unit_domain(u['text'], (u.get('pal') or {}).get('palette', ''), video=vd), ','.join(concepts_of(u['text'])) or '-')
            else: print(a, '->', unit_domain(a), concepts_of(a))
