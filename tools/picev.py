"""Picture evidence (miya 2026-10-27 "대본 규칙이랑 그림 규칙을 다른 것들에도 모두"): what a picture SHOWS, read from the names and sizes of its
object groups (facing.compute boxes: {group id: [x0, x1, y0, y1]} in picture pixels), so background effects, sound effects and text effects can be
chosen from the picture as well as from the narration words. Background layers (star haze, particle rows, sky washes) are not evidence.
evidence(boxes, W, H) -> {tag: biggest frame fraction} for every tag whose regex matches an object group at least `min` of the frame."""
import re

BG_LAYER = re.compile(r'^mv-(drift|cells|glint|twinkle|scroll|fade|tint|rack)-|\bbg\b|background|backdrop|sky\b|haze|wash|grid\b', re.I)
TAGS = [   # (tag, group-name regex, min frame fraction)
    ('fire',    re.compile(r'fire|flame|lava|magma|furnace|kiln|volcano|ember|blaze|campfire|torch|bonfire', re.I), .03),
    ('candle',  re.compile(r'candle', re.I), .01),
    ('smoke',   re.compile(r'chimney|smoke|smokestack|factory|exhaust', re.I), .03),
    ('steam',   re.compile(r'kettle|geyser|steam|boiler|hotspring|teapot', re.I), .02),
    ('water',   re.compile(r'water|sea\b|ocean|wave|lake|river|pool|pond|aquarium|current|abyss|seafloor|reef', re.I), .25),
    ('rain',    re.compile(r'\brain|storm|thundercloud|downpour|drizzle|raincloud', re.I), .06),
    ('cloud',   re.compile(r'cloud', re.I), .08),
    ('ice',     re.compile(r'snow|\bice\b|iceberg|glacier|igloo|frost|blizzard|icicle|tundra|polar', re.I), .06),
    ('forest',  re.compile(r'forest|tree|jungle|canopy|woods|pine|oak|palm', re.I), .25),
    ('flower',  re.compile(r'flower|blossom|petal|meadow|garden', re.I), .08),
    ('desert',  re.compile(r'desert|dune|sand\b|canyon', re.I), .25),
    ('sun',     re.compile(r'\bsun\b|sun$|sunburst|solar', re.I), .04),
    ('space',   re.compile(r'planet|moon|galaxy|comet|asteroid|probe|rocket|satellite|orbit|earth|mars|jupiter|saturn|blackhole|hole', re.I), .06),
    ('clock',   re.compile(r'clock|watch|hourglass|timer|metronome|pendulum', re.I), .04),
    ('bell',    re.compile(r'bell\b', re.I), .02),
    ('gear',    re.compile(r'gear|cog|sprocket|machine|engine|piston', re.I), .04),
    ('book',    re.compile(r'book|scroll|page|letter|document|parchment|manuscript|newspaper', re.I), .06),
    ('typing',  re.compile(r'typewriter|keyboard|laptop|computer|terminal', re.I), .06),
    ('coin',    re.compile(r'coin|gold|treasure|money|purse', re.I), .03),
    ('chain',   re.compile(r'chain|shackle|anchor', re.I), .04),
    ('heart',   re.compile(r'heart\b|cardiac', re.I), .04),
    ('bird',    re.compile(r'bird|crow\b|eagle|gull|\bowl\b|sparrow|\bwings?\b|feather', re.I), .02),
    ('insect',  re.compile(r'\bbees?\b|mosquito|\bfl(y|ies)\b|butterfly|wasp|beetle|cricket|cicada|firefly', re.I), .01),
    ('crowd',   re.compile(r'crowd|people|audience|army|march', re.I), .1),
    ('door',    re.compile(r'door|gate|hatch', re.I), .04),
    ('wind',    re.compile(r'windmill|turbine|windsock|flag|banner|kite|sail', re.I), .03),
    ('bubble',  re.compile(r'bubble|beaker|flask|boil|cauldron|potion', re.I), .02),
    ('bone',    re.compile(r'bone|skull|skeleton|fossil|carcass', re.I), .06),
    ('cave',    re.compile(r'cave|mine\b|tunnel|shaft|crypt|tomb', re.I), .25),
]


def evidence(boxes, W=1920, H=1080):
    out = {}
    A = float(W * H) or 1.0
    for gid, b in (boxes or {}).items():
        if BG_LAYER.search(gid): continue
        try: fr = max(0.0, (b[1] - b[0]) * (b[3] - b[2])) / A
        except Exception: continue
        nm = re.sub(r'^mv-[a-z]+-', '', gid)
        for tag, rx, mn in TAGS:
            if fr >= mn and rx.search(nm) and fr > out.get(tag, 0): out[tag] = round(fr, 3)
    return out


def has(pic, *tags):
    return bool(pic) and any(t in pic for t in tags)
