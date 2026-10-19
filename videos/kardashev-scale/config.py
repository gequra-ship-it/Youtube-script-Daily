# Per-video settings (cosmic mode, guideline 3-7): chalkboard, metadata text, background mode and palette per art theme.
STYLE = 'cosmic'
CHALK = {
 5: dict(title="The Kardashev Scale", sub="Three tiers of cosmic power (popular version)",
         rows=[("Type One", "A planet", "its home planet's energy", 'y', "Type One"),
               ("Type Two", "A star", "its parent star's power", 'c', "Type Two"),
               ("Type Three", "A galaxy", "an entire galaxy's energy", 'y', "Type Three")],
         concl=("Each step is a huge jump in power", "staggering energy"),
         src="Source: Kardashev (1964) · Sagan (1973)"),
}
WHOOSH = []
TITLE = "How Powerful Is Humanity in the Cosmos? The Kardashev Scale Explained"
DESC = ["How powerful is humanity when measured against the cosmos? In the 1960s, Soviet astrophysicist Nikolai Kardashev proposed ranking civilizations by the energy they can command, and Carl Sagan's estimate puts humanity at roughly Type zero point seven.",
        "In this video, we walk the Kardashev ladder, check the numbers behind it,  from a Type One planet to a Type Two star and a Type Three galaxy, look at Freeman Dyson's solar-collector swarm, and ask whether the silence of the cosmos could point to a Great Filter that civilizations must survive."]
CHAPTERS = [(1, "Where Electricity Comes From"), (2, "How Much Power We Use"), (3, "A Simple Measuring Stick"), (4, "A Radio Astronomer's Question"), (5, "Three Cosmic Tiers"),
            (7, "The Arithmetic of Growth"), (8, "Life at Type One"), (10, "Where More Power Could Come From"), (11, "Where Humanity Stands"), (12, "Nature Still Wins"),
            (13, "Swallowing a Star"), (16, "Dyson's One-Page Idea"), (17, "Hunting for Leaked Heat"), (18, "A Galactic Civilization"), (20, "Power From a Black Hole"),
            (21, "Is Energy the Right Ruler?"), (22, "Where Is Everybody?"), (23, "The Great Silence"), (24, "Time Enough"), (25, "Our Own Test"), (26, "Looking Up")]
SOURCES = ["Kardashev (1964), Transmission of Information by Extraterrestrial Civilizations, Soviet Astronomy 8, 217",
           "Dyson (1960), Search for Artificial Stellar Sources of Infrared Radiation, Science 131, 1667",
           "Sagan (1973), estimate of humanity at about Type 0.7",
           "Hydro-Québec, March 1989 geomagnetic storm and the Quebec blackout",
           "NASA, DART mission (2022), first test of asteroid deflection",
           "Boyajian et al. (2018), The First Post-Kepler Brightness Dips of KIC 8462852, ApJ Letters 853, L8",
           "Penrose (1969), Gravitational collapse: the role of general relativity, Rivista del Nuovo Cimento 1",
           "Hart (1975), An explanation for the absence of extraterrestrials on Earth, Quarterly Journal of the Royal Astronomical Society 16, 128",
           "Hanson (1996), The Great Filter - Are We Almost Past It?",
           "Lawrence Livermore National Laboratory, National Ignition Facility fusion ignition (December 2022)"]
HASHTAGS = "#MiyasLab #Kardashev #Space #DysonSphere #GreatFilter"
BG = dict(power='night', paper1964='paper', growth='night', planetpower='dusk', fusion='night', naturewins='dusk', starwaste='night', sunfusion='night', dysonidea='paper', irsearch='night', galaxyscale='night', blackhole='night', criticism='paper', fermi='night', hart='night', ourtest='dusk', switch='night', kardashev='night', currency='night', chalkboard='paper', typeone='dusk', sagan='night', dyson='night', galaxy='night', silence='night', ending='dusk')
# Palettes (3-5, 3-7): star/galaxy scale -> deepfield; Dyson swarm and star light -> solar; Earth-scale life, weather, endings -> space
PAL_DEFAULT = 'deepfield'
PAL = dict(starwaste='solar', sunfusion='solar', dysonidea='solar', irsearch='solar', blackhole='solar', planetpower='aurora', naturewins='storm', ourtest='space', dyson='solar', typeone='aurora', sagan='space', ending='space')
