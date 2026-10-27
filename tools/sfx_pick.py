# -*- coding: utf-8 -*-
# Automatic sound-effect cues (2026-10-27, miya: "make more sound effects and pick them automatically from the script and the picture situation").
# Deterministic, like the frog/object/fx rules (guideline 7-2 D-2): word regex over the unit text -> sound name, anchored to the matched word;
# otherwise a quiet palette ambient on every third unit. No model judgement, no randomness.
#   sfx_for(text, palname, k, dur, cosmic, prev, side) -> list of 0-1 cue dicts {name, word|at, vol, auto}
#     text    unit narration text (exact substring of the scene text; the matched word is used by build3 for the timing)
#     palname palette of the unit ('ocean', 'history', ...), k unit index, dur unit length (s), cosmic = cosmic style video
#     prev    names of the last cues (no same name twice in a row), side = the picture agent's sidecar `sfx` list (fallback, or forced with sfx_lock)
import re

# (regex, sound, vol). First match wins; order = priority (events before textures). Word boundaries, case-insensitive.
SFX_WORDS = [
    (r'\b(thunder|lightning|thunderstorm)\b', 'thunder', .55),
    (r'\b(earthquakes?|quakes?|crumbl\w*|caves? in|landslide|avalanche|rockslide|collapsed? (?:into|onto|under))\b', 'crumble', .6),
    (r'\b(explo\w+|blast\w*|erupt\w*|detonat\w*)\b', 'impact', .6),
    (r'\b(rockets?|launch\w*|thrust\w*|engines?|lift-?off|boosters?|jet)\b', 'thrust', .45),
    (r'\b(heart ?beats?|heart ?rate|pulse rate|hearts? (?:beat|pound|race)\w*|pounding|hearts?|cardiac)\b', 'heartbeat', .55),
    (r'\b(breath\w*|inhal\w+|exhal\w+|gasp\w*|sigh\w*|lungs?)\b', 'breath', .5),
    (r'\b(clocks?|ticking|minutes? pass\w*|hours? pass\w*|seconds? tick\w*|countdown|stopwatch)\b', 'clock', .5),
    (r'\b(gears?|cogs?|mechanism|clockwork|ratchet\w*|machines?)\b', 'gear', .45),
    (r'\b(typ(?:e|ed|ing)|keyboard|computers?|laptops?|data ?bases?|code|software|programs?)\b', 'typing', .45),
    (r'\b(typewriter|telegram|dispatch\w*|memos?)\b', 'typewriter', .45),
    (r'\b(radios?|broadcast\w*|transmission|transmitt\w*|static|signals? from)\b', 'radio', .45),
    (r'\b(cameras?|photograph\w*|snapshots?|pictures? (?:were|was) taken|filmed)\b', 'shutter', .5),
    (r'\b(switch\w*|button|turned? (?:it )?on|turned? (?:it )?off|lights? (?:go|went|came) (?:on|out))\b', 'switch', .5),
    (r'\b(coins?|gold|silver|money|wealth|treasure|paid|fortune|riches|taxes|tribute)\b', 'coins', .5),
    (r'\b(keys?|padlock|keychain)\b', 'keys', .5),
    (r'\b(lock(?:ed|s|ing)?|latch\w*|seal(?:ed|s|ing)?|bolt(?:ed|s)?|clamp\w*|snapp?ed shut)\b', 'click', .55),
    (r'\b(doors?|gates?|hatch(?:es)?|entrance|entered the|went inside|stepped in(?:to|side))\b', 'door', .5),
    (r'\b(knock\w*|tapp?(?:ed|ing)? on|hammer\w*|nail\w*)\b', 'knock', .5),
    (r'\b(stamp\w*|seal of|decree|signed|signature|official|approved|verdict|sentenced|court|judges?|trial)\b', 'gavel', .5),
    (r'\b(chains?|chained|cages?|caged|prison\w*|shackl\w*|anchors?)\b', 'chain', .45),
    (r'\b(arrows?|darts?|spears?|javelins?|shot past|whizz\w*|zipp?(?:ed|ing) past)\b', 'arrow', .5),
    (r'\b(horses?|cavalry|riders?|gallop\w*|hooves|stagecoach|carriage)\b', 'hooves', .5),
    (r'\b(soldiers?|armies|army|troops|march\w*|legions?|regiment|parade)\b', 'march', .45),
    (r'\b(walk\w*|footsteps|strode|strolled|wander\w*|hik\w+|trek\w*|pac(?:ed|ing))\b', 'steps', .45),
    (r'\b(snow\w*|blizzard|frozen ground|glaciers?)\b', 'snowstep', .45),
    (r'\b(ice|icy|iceberg|frost\w*|freez\w+|froze|thaw\w*)\b', 'icecrack', .45),
    (r'\b(shovel\w*|dig(?:s|ging|ged)?|dug|excavat\w*|buried|burial|unearth\w*|graves?|tombs?)\b', 'dig', .5),
    (r'\b(scroll\w*|parchment|manuscripts?|maps?|unroll\w*|treaty|charter)\b', 'scroll', .45),
    (r'\b(wrote|writing|written|letters?|diary|journals?|ink|quill|pen\b|notebook|scribbl\w*|recorded in)\b', 'quill', .45),
    (r'\b(pencil\w*|sketch\w*|draw(?:s|ing|n)?|drew|diagram\w*|chalk\w*)\b', 'pencil', .45),
    (r'\b(pages?|books?|textbooks?|libraries|library|archives?|volumes?|chapters?|documents?|papers?|records?)\b', 'page', .45),
    (r'\b(tore (?:up|the (?:page|paper|letter|map))|tear(?:s|ing)? (?:up|the (?:page|paper|letter|map))|ripp?(?:ed|ing) (?:up|the (?:page|paper|letter|map))|shredd?(?:ed|ing) (?:the )?(?:paper|documents?|letters?))\b', 'tear', .5),
    (r'\b(closed the book|slammed|shut the|closed it)\b', 'bookclose', .5),
    (r'\b(candle\w*|lantern\w*|torch(?:es)?|oil lamps?|flickering)\b', 'candle', .4),
    (r'\b(match(?:es)? (?:was )?struck|struck a match|lit (?:a|the) (?:fire|candle|lamp|torch)|ignit\w*|spark\w*)\b', 'match', .5),
    (r'\b(fires?|flames?|burn\w*|bonfire|campfire|hearth|embers?|blaze\w*|wildfire)\b', 'crackle', .5),
    (r'\b(ash(?:es)?|smok(?:e|ing|y)|soot|volcan\w*|lava|magma)\b', 'ash', .4),
    (r'\b(fry\w*|fried|sizzl\w*|cook\w*|kitchen|grill\w*|roast\w*|bak(?:ed|ing))\b', 'sizzle', .45),
    (r'\b(chopp?\w*|slic(?:e|ed|ing)|knife|knives|cut(?:s|ting)? (?:it|the|into)|butcher\w*|carv\w*)\b', 'chop', .5),
    (r'\b(pour\w*|wine|beer|tea|coffee|milk|glass of|cup of|drink\w*|drank)\b', 'pour', .45),
    (r'\b(bottle\w*|cork\w*|uncork\w*|champagne|flasks?)\b', 'cork', .5),
    (r'\b(boil\w*|bubbl\w*|simmer\w*|ferment\w*|cauldron|brew\w*)\b', 'bubble', .5),
    (r'\b(steam\w*|kettle|geysers?|hot springs?|vents?)\b', 'steam', .45),
    (r'\b(hiss\w*|snakes?|serpents?|cobra|viper|gas leak\w*|leak(?:ed|ing|s)?)\b', 'hiss', .45),
    (r'\b(crunch\w*|bit into|biting into|munch\w*|crisp\w*|crackers?|apples?|nuts?|toast)\b', 'crunch', .45),
    (r'\b(slosh\w*|sloshed|buckets? of water|barrels?|canteens?|waterskins?|jugs?)\b', 'slosh', .4),
    (r'\b(drops?|dripp?\w*|tears?|trickl\w*|leak\w*)\b', 'drip', .5),
    (r'\b(splash\w*|dive[ds]?|diving|plung\w*|jumped in|fell into the (?:water|sea|river)|spray\w*)\b', 'splash', .55),
    (r'\b(waves?|surf|tides?|sea|ocean\w*|shore\w*|coast\w*|beach\w*|swell\w*)\b', 'waves', .45),
    (r'\b(rivers?|streams?|brooks?|creeks?|flow(?:s|ing|ed)? (?:down|through)|rapids|waterfalls?|currents?)\b', 'stream', .4),
    (r'\b(rain\w*|drizzl\w*|downpour|monsoon|shower\w*)\b', 'rain', .5),
    (r'\b(storms?|gales?|hurricanes?|typhoons?|tornado\w*|cyclon\w*|howl\w*|gusts?)\b', 'gust', .5),
    (r'\b(winds?|windy|windswept|breez\w*|blew|blowing|draughts?|drafty)\b', 'wind', .45),
    (r'\b(leaves|leaf|forests?|trees?|woods|jungle|canopy|branch\w*|bush(?:es)?|undergrowth)\b', 'leaves', .4),
    (r'\b(crickets?|night fell|at night|midnight|nightfall|after dark|evening)\b', 'cricket', .35),
    (r'\b(summer|heat ?wave|cicadas?|scorching|sweltering)\b', 'cicada', .35),
    (r'\b(bees?|wasps?|flies|fly|mosquito\w*|insects?|buzz\w*|hornets?|beetles?|swarm\w*)\b', 'buzz', .45),
    (r'\b(birds?|wings?|feathers?|flapp?\w*|flutter\w*|butterfl\w*|moths?|bats?)\b', 'flutter', .45),
    (r'\b(eagles?|hawks?|vultures?|owls?|geese|swans?|cranes?|albatross|soar\w*|glid(?:e|ed|ing))\b', 'wingbeat', .45),
    (r'\b(gravel|pebbles?|rubble|scree|rocky path|boots? (?:on|crunch))\b', 'gravel', .45),
    (r'\b(dust\w*|sandstorm|powder\w*|chalk dust|crumbs?)\b', 'dust', .4),
    (r'\b(sand\w*|deserts?|dunes?|hourglass|grains? of)\b', 'sand', .45),
    (r'\b(stones?|rocks?|boulders?|pebble|cliffs?|granite|marble|bricks?|walls?)\b', 'stone', .5),
    (r'\b(scrap(?:e|ed|ing)|scratch\w*|drag(?:ged|ging)|grind\w*|ground (?:down|against)|rasp\w*)\b', 'scrape', .45),
    (r'\b(crack(?:s|ed|ing)?|snapp?(?:ed|ing)?|fractur\w*|split (?:open|apart|in two)|broke|break(?:s|ing)?|shatter\w*)\b', 'crack', .5),
    (r'\b(fingers? snap\w*|clicked (?:his|her|their) fingers|in an instant|instantly|suddenly|all at once|in a flash)\b', 'snap', .45),
    (r'\b(crash(?:ed|es|ing)?|collid\w*|collision\w*|slamm?(?:ed|ing)|struck|smash\w*|toppl\w*|tumbl\w*|touch(?:es|ed)? down|hit the (?:ground|floor|wall|water|surface)|landed (?:on|with))\b', 'impact', .5),
    (r'\b(heavy|weigh\w*|tons?|massive|enormous|set (?:it )?down|placed|put down|lay (?:it )?down|rest(?:ed|s)? on)\b', 'thud', .5),
    (r'\b(wooden|timber|planks?|huts?|cabins?|barns?|floorboards?|creak\w*|hinges?|rafters?|wagons?|carts?)\b', 'creak', .45),
    (r'\b(clothing|clothes|dress(?:es|ed)?|robes?|coats?|cloaks?|silk|wool|linen|uniforms?|sleeves?|blankets?|sails?|flags?|curtains?|garments?)\b', 'cloth', .45),
    (r'\b(pumps?|bellows|pump(?:ed|ing)|inflat\w*|balloon\w*|squeez\w*)\b', 'pump', .45),
    (r'\b(zipp?\w*|backpacks?|bags?|luggage|suitcases?|tents?)\b', 'zipper', .45),
    (r'\b(metal\w*|iron|steel|copper|bronze|tools?|hammers?|anvils?|wrench\w*|cutlery|spoons?|forks?|cups?|mugs?|pots?|pans?)\b', 'clink', .5),
    (r'\b(whoosh\w*|swoosh\w*|swept|sweep(?:s|ing)?|rush(?:ed|es|ing)?|hurtl\w*|zoom\w*|sped|speed\w*|racing|dash(?:ed|es|ing)?|flew (?:past|by|over))\b', 'whoosh', .5),
    (r'\b(appear(?:s|ed|ing)?|emerg(?:e|es|ed|ing)|pop(?:s|ped|ping)? (?:up|out|into)|showed up|reveal(?:s|ed|ing)?|turns? out|sprang|sprout\w*|bloom(?:s|ed|ing)?|hatch(?:es|ed|ing)?|burst(?:s|ing)?)\b', 'pop', .5),
    (r'\b(discover\w*|realiz\w*|realis\w*|idea|insight|eureka|breakthrough|finally understood|the answer|solution|secret|mystery)\b', 'hush', .55),
    (r'\b(quiet(?:ly|ness)?|silen(?:ce|t|tly)|hushed|whisper\w*|held (?:his|her|their|its) breath)\b', 'breath', .4),
    (r'\b(tap(?:s|ped|ping)?|knuckles?|rapp?(?:ed|ing)|drumm?(?:ed|ing)? (?:his|her|their) fingers|clicked)\b', 'woodblock', .5),
    (r'\b(alarms?|bells?|tolled|tolling|rang|ringing)\b', 'bell', .5),
    (r'\b(count(?:ed|s|ing)?|numbers?|percent\w*|measur\w*|calculat\w*|tally|statistics?|figures?|data)\b', 'tick', .5),
    (r'\b(bubbles? (?:rose|rising|float)|single bubble|air bubble|oxygen bubble)\b', 'bubbleup', .5),
]
# cosmic style videos never use the earthly textures (art_spec 11): swap them for the space family
COSMIC_SWAP = {'wind': 'glimmer', 'rain': 'sparkle', 'swish': 'warp', 'hush': 'bloom', 'breath': 'pulse', 'waves': 'glimmer', 'gust': 'warp',
               'leaves': 'glimmer', 'cricket': 'glimmer', 'cicada': 'sparkle', 'thunder': 'bloom', 'stream': 'glimmer', 'shore': 'sparkle',
               'crackle': 'sparkle', 'thrust': 'thrust', 'whoosh': 'warp', 'impact': 'pulse', 'crumble': 'starfall', 'snowstep': 'glimmer',
               'buzz': 'pulse', 'flutter': 'sparkle', 'wingbeat': 'glimmer', 'candle': 'glimmer', 'ash': 'sparkle', 'dust': 'sparkle',
               'sand': 'sparkle', 'static': 'static', 'radio': 'radio'}
# extra event rules for cosmic videos (checked first there)
COSMIC_WORDS = [
    (r'\b(stars? (?:born|forms?|formed|ignit\w*)|supernova\w*|flare\w*|flash\w*|burst\w*|explo\w+|big bang)\b', 'bloom', .6),
    (r'\b(meteors?|shooting stars?|comets?|asteroids?|falls? (?:toward|into)|fell (?:toward|into)|plung\w*|sink\w*|descend\w*)\b', 'starfall', .55),
    (r'\b(signals?|messages?|pings?|transmission|beacons?|detect\w*|antenna\w*|telescopes? (?:picked|caught)|listen\w*)\b', 'pulse', .5),
    (r'\b(jump\w*|teleport\w*|warp\w*|instantly|in an instant|suddenly|all at once|in a flash|blink of)\b', 'warp', .55),
    (r'\b(galax\w+|stars?|starlight|constellation\w*|twinkl\w*|glitter\w*|sparkl\w*|shimmer\w*|dust|nebula\w*)\b', 'sparkle', .45),
    (r'\b(glow\w*|faint\w*|dim\w*|distant|far away|horizon|light-?years?)\b', 'glimmer', .4),
]
# quiet ambient per palette: the units with no event get one of these on every third unit (k % 3 == 1), short and low
AMBIENT = {
    'ocean': ['waves', 'shore', 'bubble', 'stream'], 'forest': ['leaves', 'cricket', 'flutter', 'stream'], 'desert': ['wind', 'dust', 'gust', 'sand'],
    'ice': ['gust', 'snowstep', 'icecrack', 'wind'], 'storm': ['rain', 'thunder', 'gust', 'wind'], 'history': ['candle', 'scroll', 'steps', 'quill'],
    'lab': ['bubble', 'typing', 'switch', 'static'], 'body': ['heartbeat', 'breath', 'pulse', 'heartbeat'], 'sunset': ['leaves', 'wind', 'cricket', 'cicada'],
    'space': ['glimmer', 'sparkle', 'pulse', 'static'], 'deepfield': ['glimmer', 'sparkle', 'pulse', 'glimmer'], 'nebula': ['glimmer', 'sparkle', 'bloom', 'glimmer'],
    'aurora': ['glimmer', 'sparkle', 'glimmer', 'pulse'], 'solar': ['sparkle', 'bloom', 'glimmer', 'static'],
}
AMBIENT_VOL = .32
DENSITY = .45          # at most ~45 % of the units get a cue (guideline 9-3: 35-45 %); the first STRONG_N word rules (real events) may exceed it
STRONG_N = 24
LONG = {'waves', 'shore', 'stream', 'thunder', 'leaves', 'cricket', 'cicada', 'rain', 'wind', 'crackle', 'bubble', 'sizzle', 'candle', 'ash', 'thrust', 'radio', 'steps', 'hooves', 'march', 'typing', 'typewriter', 'gear', 'clock'}   # >= 1.5 s textures: not in units shorter than 4 s


def _valid(name):
    import sfx_lib
    return sfx_lib.ALIAS.get(name, name) in sfx_lib.LIB


def sfx_for(text, palname, k, dur, cosmic=False, prev=(), side=None, lock=False, count=None):
    """returns [] or [cue]; cue = {name, word, vol, auto: 'word'|'ambient'|'agent'} (word None + 'at' seconds for ambients).
    count = cues placed so far (default len(prev)): once the density cap is reached only strong events and ambients on the 3rd units pass."""
    if count is None: count = len(prev)
    full = count >= DENSITY * (k + 1) + 1
    side = [e for e in (side or []) if isinstance(e, dict) and e.get('name') and _valid(e['name'])]
    if lock and side: return [dict(side[0], auto='agent')]
    last = prev[-1] if prev else None
    rules = (COSMIC_WORDS + SFX_WORDS) if cosmic else SFX_WORDS
    for ri, (rx, name, vol) in enumerate(rules):
        if full and ri >= STRONG_N + (len(COSMIC_WORDS) if cosmic else 0): break
        m = re.search(rx, text, re.I)
        if not m: continue
        if cosmic: name = COSMIC_SWAP.get(name, name)
        if name == last: continue                                   # same sound twice in a row: skip this rule, try the next
        if name in LONG and dur < 4: continue
        return [dict(name=name, word=m.group(0), vol=vol, auto='word')]
    if side and side[0]['name'] != last and not full:                           # the picture agent saw something in the picture the words do not say
        return [dict(side[0], auto='agent')]
    if k % 3 == 1 and dur >= 6 and not full:
        pool = AMBIENT.get(palname) or []
        if cosmic: pool = [COSMIC_SWAP.get(n, n) for n in pool]
        for j in range(len(pool)):
            name = pool[(k // 3 + j) % len(pool)]
            if name != last: return [dict(name=name, word=None, at=1.2, vol=AMBIENT_VOL, auto='ambient')]
    return []


if __name__ == '__main__':      # quick self-check: every rule's sound exists
    import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    bad = [n for _, n, _ in SFX_WORDS + COSMIC_WORDS if not _valid(n)] + [n for n in set(COSMIC_SWAP.values()) if not _valid(n)] + [n for v in AMBIENT.values() for n in v if not _valid(n)]
    print('rules', len(SFX_WORDS), 'cosmic', len(COSMIC_WORDS), 'ambient palettes', len(AMBIENT), 'bad names', bad)
