# Per-video settings (cosmic mode, guideline 3-7): chalkboards, metadata text, background mode and palette per art theme.
STYLE = 'cosmic'
CHALK = {
 21: dict(title="TRAPPIST-1 at a Glance", sub="A tiny star with a crowded family",
          rows=[("Distance", "40 light-years", "toward Aquarius", 'y', "forty"),
                ("Planets", "7 Earth-sized", "rocky worlds", 'c', "seven"),
                ("Habitable zone", "3 worlds", "TRAPPIST-1e, f and g", 'y', "three")],
          concl=("Seven worlds, three in the sweet spot", "squarely"),
          src="Source: Gillon et al. (2017), Nature 542, 456"),
 27: dict(title="The Webb Telescope", sub="A golden eye in deep infrared",
          rows=[("Launched", "Dec 25, 2021", "Christmas Day", 'y', "Christmas"),
                ("Distance", "~1 million miles", "from Earth", 'c', "million"),
                ("Orbit", "L2", "the second Lagrange point", 'y', "Lagrange")],
          concl=("Starlight becomes a chemical inventory", "inventory"),
          src="Source: NASA James Webb Space Telescope mission"),
}
WHOOSH = []
TITLE = "The Search for Earth Two and the Secret of Alien Life"
DESC = ["Is there another Earth out there, and could it hold life? Astronomers have found thousands of planets, a few of them in the habitable zone of their stars, and the James Webb Space Telescope is now reading starlight that has passed through their atmospheres.",
        "In this video, we follow the hunt from the first planet around a Sun-like star to Kepler-186f, Kepler-452b, Proxima Centauri b and the seven worlds of TRAPPIST-1, see how oxygen and methane could act as signs of life, and ask what the Fermi Paradox and the Great Filter might mean for us."]
CHAPTERS = [(1, 'A Cup of Coffee'), (2, 'Hostile Neighbors'), (3, 'The First Wobble'), (5, 'The Goldilocks Zone'), (6, 'Why Liquid Water'), (8, 'Hunting by Wobble'), (9, 'Hunting by Shadow'), (10, 'The Kepler Telescope'), (11, 'Kepler-186f'), (13, 'Kepler-452b'), (15, 'Too Far to Visit'), (16, 'Our Nearest Neighbor'), (18, 'Tidal Locking'), (19, 'The Twilight Strip'), (21, 'Seven Worlds, One Star'), (23, 'The Best Candidate'), (24, "Earth's Hidden Engine"), (26, 'Reading Atmospheres'), (27, 'The Webb Telescope'), (29, 'Signs of Life'), (31, 'False Alarms'), (32, 'Where Is Everybody?'), (34, 'The Great Filter'), (36, 'A Filter Ahead'), (38, 'Cosmic Humility'), (40, 'No Planet B'), (41, 'Your Blue Oasis')]
SOURCES = ["Mayor and Queloz (1995), A Jupiter-mass companion to a solar-type star, Nature 378, 355",
           "Borucki et al. (2010), Kepler Planet-Detection Mission: Introduction and First Results, Science 327, 977",
           "Quintana et al. (2014), An Earth-sized planet in the habitable zone of a cool star, Science 344, 277",
           "Jenkins et al. (2015), Discovery and Validation of Kepler-452b, The Astronomical Journal 150, 56",
           "Anglada-Escude et al. (2016), A terrestrial planet candidate in a temperate orbit around Proxima Centauri, Nature 536, 437",
           "Gillon et al. (2017), Seven temperate terrestrial planets around the nearby ultracool dwarf star TRAPPIST-1, Nature 542, 456",
           "Lovelock (1965), A physical basis for life detection experiments, Nature 207, 568",
           "Hanson (1996), The Great Filter - Are We Almost Past It?",
           "NASA, James Webb Space Telescope mission overview"]
HASHTAGS = "#MiyasLab #Exoplanets #AlienLife #FermiParadox #JamesWebb"
BG = {'coffee': 'dusk', 'neighbors': 'night', 'pegasus': 'night', 'wilderness': 'night', 'goldilocks': 'dusk', 'water': 'paper', 'firefly': 'night', 'radialvel': 'night', 'transit': 'paper', 'kepler': 'night', 'k186': 'night', 'amber': 'dusk', 'k452': 'night', 'heavy': 'night', 'toofar': 'night', 'proxima': 'night', 'flares': 'night', 'locking': 'night', 'terminator': 'dusk', 'circulation': 'night', 'chalk': 'paper', 'trappistsky': 'night', 'trappiste': 'night', 'dynamo': 'night', 'tectonics': 'dusk', 'atmos': 'night', 'spectrum': 'paper', 'biosig': 'dusk', 'beacon': 'night', 'falsealarm': 'night', 'fermi': 'night', 'silence': 'night', 'filter': 'night', 'eukaryote': 'night', 'filterahead': 'night', 'mirror': 'night', 'humility': 'dusk', 'precious': 'dusk', 'planetb': 'night', 'oasis': 'dusk', 'outro': 'night'}
# Palettes (3-5, 3-7): red dwarfs and flares -> solar; atmospheres and Earth -> aurora; deep time and the Fermi silence -> deepfield; methods and spectra -> lab
PAL_DEFAULT = 'space'
PAL = {'coffee': 'space', 'neighbors': 'desert', 'pegasus': 'solar', 'wilderness': 'nebula', 'goldilocks': 'solar', 'water': 'ocean', 'firefly': 'space', 'radialvel': 'lab', 'transit': 'lab', 'kepler': 'deepfield', 'k186': 'solar', 'amber': 'solar', 'k452': 'space', 'heavy': 'space', 'toofar': 'deepfield', 'proxima': 'solar', 'flares': 'solar', 'locking': 'solar', 'terminator': 'solar', 'circulation': 'aurora', 'chalk': 'lab', 'trappistsky': 'nebula', 'trappiste': 'solar', 'dynamo': 'aurora', 'tectonics': 'storm', 'atmos': 'aurora', 'spectrum': 'lab', 'biosig': 'aurora', 'beacon': 'aurora', 'falsealarm': 'lab', 'fermi': 'deepfield', 'silence': 'deepfield', 'filter': 'nebula', 'eukaryote': 'ocean', 'filterahead': 'storm', 'mirror': 'nebula', 'humility': 'space', 'precious': 'aurora', 'planetb': 'space', 'oasis': 'aurora', 'outro': 'nebula'}
