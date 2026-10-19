# Per-video settings (cosmic mode, guideline 3-7): chalkboard, metadata text, background mode and palette per art theme.
STYLE = 'cosmic'
CHALK = {
 3: dict(title="The Kardashev Scale", sub="Three tiers of cosmic power (popular version)",
         rows=[("Type One", "A planet", "its home planet's energy", 'y', "Type One"),
               ("Type Two", "A star", "its parent star's power", 'c', "Type Two"),
               ("Type Three", "A galaxy", "an entire galaxy's energy", 'y', "Type Three")],
         concl=("Each step is a huge jump in power", "staggering energy"),
         src="Source: Kardashev (1964) · Sagan (1973)"),
}
WHOOSH = []
TITLE = "How Powerful Is Humanity in the Cosmos? The Kardashev Scale Explained"
DESC = ["How powerful is humanity when measured against the cosmos? In the 1960s, Soviet astrophysicist Nikolai Kardashev proposed ranking civilizations by the energy they can command, and Carl Sagan's estimate puts humanity at roughly Type zero point seven.",
        "In this video, we walk the Kardashev ladder from a Type One planet to a Type Two star and a Type Three galaxy, look at Freeman Dyson's solar-collector swarm, and ask whether the silence of the cosmos could point to a Great Filter that civilizations must survive."]
CHAPTERS = [(1, "Where Electricity Comes From"), (2, "A Simple Measuring Stick"), (3, "Three Cosmic Tiers"), (5, "Life at Type One"), (6, "Where Humanity Stands"),
            (7, "Swallowing a Star"), (8, "A Galactic Civilization"), (9, "The Great Silence"), (10, "Looking Up")]
SOURCES = ["Kardashev (1964), Transmission of Information by Extraterrestrial Civilizations, Soviet Astronomy 8, 217",
           "Dyson (1960), Search for Artificial Stellar Sources of Infrared Radiation, Science 131, 1667",
           "Sagan (1973), estimate of humanity at about Type 0.7",
           "Hydro-Québec, March 1989 geomagnetic storm and the Quebec blackout"]
HASHTAGS = "#MiyasLab #Kardashev #Space #DysonSphere #GreatFilter"
BG = dict(switch='night', kardashev='night', currency='night', chalkboard='paper', typeone='dusk', sagan='night', dyson='night', galaxy='night', silence='night', ending='dusk')
# Palettes (3-5, 3-7): star/galaxy scale -> deepfield; Dyson swarm and star light -> solar; Earth-scale life, weather, endings -> space
PAL_DEFAULT = 'deepfield'
PAL = dict(dyson='solar', typeone='aurora', sagan='space', ending='space')
