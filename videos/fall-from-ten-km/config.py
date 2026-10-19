# Per-video settings (guideline 3-5, 12, 17, 20-2): chalkboards, metadata text, background mode and palette per art theme.
CHALK = {
 4: dict(title="Ten Kilometers Up", sub="Conditions at cruising altitude",
         rows=[("Air pressure", "~1/4", "of sea level", 'y', "one quarter"),
               ("Useful consciousness", "~30 s", "at 10,000 m", 'c', "thirty seconds"),
               ("Air temperature", "-50 °C", "around", 'y', "minus fifty")],
         concl=("Thin, cold air is the first threat", "Celsius"),
         src="Source: Standard Atmosphere · FAA altitude physiology"),
 9: dict(title="How Fast Do You Fall?", sub="Belly-down, no parachute",
         rows=[("High, thin air", "300+ km/h", "can briefly top", 'c', "top three hundred"),
               ("Near the ground", "~200 km/h", "terminal velocity", 'y', "about two hundred"),
               ("Every second", "~55 m", "at 200 km/h", 'y', "fifty-five meters")],
         concl=("Thicker air slows the fall", "every second"),
         src="Source: skydiving physics · drag-model estimate"),
 21: dict(title="Time and Force", sub="The same stop, spread over more time",
          rows=[("Impact lasts 0.01 s", "10x force", "average", 'c', "one hundredth"),
                ("Impact lasts 0.1 s", "1x force", "average", 'y', "one tenth"),
                ("Ten times longer", "1/10", "of the force", 'y', "cuts the average force")],
          concl=("A longer stop means less force", "to one tenth"),
          src="Source: impulse-momentum theorem (F = change in momentum / time)"),
}
WHOOSH = []
TITLE = "Falling from Ten Kilometers: The Extreme Science of Survival"
DESC = ["What would happen if you fell from ten kilometers up with no parachute? Thin air, freezing cold, and a fall of roughly two hundred kilometers per hour would all be against you, yet a handful of people have survived falls from airliner heights.",
        "In this video, we follow the fall second by second: the time of useful consciousness, drag and terminal velocity, the spread-eagle position, why stopping distance decides everything, and what the cases of Vesna Vulovic and Juliane Koepcke suggest about trees, snow, and wreckage."]
CHAPTERS = [(1, "Seatbelt at Ten Kilometers"), (3, "No Air to Breathe"), (6, "The Biting Cold"), (7, "Gravity and Drag"),
            (11, "Waking Up Mid-Fall"), (14, "Stopping Distance"), (15, "Why Water Is Hard"), (16, "Trees and Snow"),
            (18, "Wreckage and Survivors"), (21, "Time and Force"), (23, "Muscles and Landing"), (27, "Two and a Half Minutes"),
            (31, "Rules of the Universe"), (36, "Looking Up")]
SOURCES = ["Guinness World Records: Highest fall survived without parachute (Vesna Vulovic, 26 January 1972, 10,160 m)",
           "FAA Advisory Circular 61-107B: time of useful consciousness",
           "Wikipedia: LANSA Flight 508 (Juliane Koepcke, 24 December 1971)",
           "International Standard Atmosphere"]
HASHTAGS = "#MiyasLab #Physics #FreeFall #TerminalVelocity #Survival"
BG = dict(seatbelt='dusk', shell='night', thinair='night', chalk1='paper', blackout='night', cold='night', drag='paper', terminal='night',
          chalk2='paper', skydiver='dusk', waking='night', spread='dusk', stability='paper', stopdist='paper', water='dusk', trees='paper',
          snow='night', wreckage='dusk', vulovic='paper', koepcke='dusk', chalk3='paper', milli='night', muscles='paper', flexible='dusk',
          feetfirst='paper', roll='dusk', clock='night', fragile='dusk', machine='paper', luck='night', rules='night', after='dusk',
          airline='dusk', demo='paper', thinline='night', outside='dusk', mercy='night', ending='dusk')
# Palettes (guideline 3-5): high air and cosmos-like height -> space; cold and snow -> ice; trees -> forest; water -> ocean; body and muscles -> body; wreckage and disaster -> storm
PAL_DEFAULT = 'space'
PAL = dict(cold='ice', snow='ice', trees='forest', water='ocean', after='forest', muscles='body', flexible='body', feetfirst='body',
           roll='body', wreckage='storm', vulovic='storm', koepcke='forest', seatbelt='history', outside='sunset')

HOOK = dict(until=300, maxu=5.5)   # guideline 20-2
