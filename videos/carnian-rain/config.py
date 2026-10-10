# Per-video settings: chalkboards, metadata text, background mode per art theme.
CHALK = {
 13: dict(title="The Planet Warms", sub="The Carnian Pluvial Episode by the numbers",
          rows=[("Start", "~234.5 Ma", "million years ago", 'y', "The episode began around"),
                ("Ocean warming", "3 to 4 °C+", "from conodont teeth", 'c', "warming of at least"),
                ("Marine species lost", "About 1/3", "of all species", 'c', "around one third")],
          concl=("A wet age lasting roughly 1 to 2 million years", "were lost"),
          src="Source: Wikipedia, Carnian pluvial event · Dal Corso et al. (2020)"),
 29: dict(title="The Dinosaur Timeline", sub="Rare for millions of years, then everywhere",
          rows=[("Dinosaurs appear", "~20 Myr earlier", "but stay rare", 'y', "Dinosaurs appeared"),
                ("Wet episode begins", "~234.5 Ma", "Carnian Pluvial Episode", 'c', "The wet episode began"),
                ("Ischigualasto layers", "~231 Ma", "earliest dinosaur-bearing", 'c', "Ischigualasto Formation")],
          concl=("The rain came first, then the dinosaurs", "date to around"),
          src="Source: Univ. of Bristol (2020) · Wikipedia, Carnian pluvial event"),
}
WHOOSH = []
TITLE = "The Rain That Lasted a Million Years and Made the Dinosaurs"
DESC = ["Around 234 million years ago, volcanic eruptions warmed the planet and the supercontinent Pangaea entered a long wet age called the Carnian Pluvial Episode. When it ended, dinosaurs were on the rise.",
        "In this video, we read the clues in red rocks, river sands and the oldest amber with trapped arthropods, follow the losses in the oceans and the birth of modern coral reefs, and look at why dinosaurs went from rare to everywhere, and why scientists still debate it."]
CHAPTERS = [(1, "What If It Never Stopped?"), (2, "A Clue in Red Rocks"), (5, "One Giant Continent"), (8, "Fire in the Ocean"),
            (10, "A Carbon Shock"), (14, "An Engine of Rain"), (16, "Not One Endless Storm"), (19, "Treasure in Tree Resin"),
            (21, "Trouble in the Sea"), (25, "Forests Change"), (27, "Hard Times for Old Plant-Eaters"), (28, "Dinosaurs Step Forward"),
            (33, "Why Dinosaurs?"), (39, "Another Great Extinction"), (41, "A Warning From Deep Time")]
SOURCES = ["Dal Corso et al. (2020), Extinction and dawn of the modern world in the Carnian (Late Triassic), Science Advances",
           "Bernardi et al. (2018), Dinosaur diversification linked with the Carnian Pluvial Episode, Nature Communications",
           "Simms & Ruffell (1989), Synchroneity of climatic change and extinctions in the Late Triassic, Geology",
           "Schmidt et al. (2012), Arthropods in amber from the Triassic Period, PNAS",
           "Norell et al. (2020), The first dinosaur egg was soft, Nature",
           "Wikipedia: Carnian pluvial event; University of Bristol news (2020); Eos (2020)"]
HASHTAGS = "#MiyasLab #Dinosaurs #Triassic #Paleontology #Climate"
BG = dict(window='night', redrock='paper', geologists='paper', doubt='dusk', pangaea='night', recovery='paper', before='dusk',
          volcano='night', basalt='paper', carbon='paper', conodont='night', onset='dusk', evaporation='dusk', monsoon='night',
          pulses='paper', rivers='dusk', clay='paper', amber='night', amber2='paper', sea='night', blackshale='night',
          coral='dusk', plankton='night', conifers='dusk', pollen='paper', rhynchosaur='dusk', footprints='paper',
          ischigualasto='dusk', eoraptor='paper', herrera='night', why='paper', posture='dusk', eggs='paper', debate='night',
          modern='dusk', mammals='night', extinction='paper', burial='dusk', warning='night', water='dusk', museum='paper',
          ending='night')
# Palettes (guideline 3-5): ancient dry lands, volcanoes and dinosaurs -> desert; rain, rivers, forests -> forest; oceans -> ocean
PAL_DEFAULT = 'desert'
PAL = dict(window='forest', evaporation='forest', monsoon='forest', pulses='forest', rivers='forest', clay='forest', amber='forest',
           amber2='forest', conifers='forest', pollen='forest', water='forest', ending='forest', burial='forest', mammals='forest',
           sea='ocean', blackshale='ocean', coral='ocean', plankton='ocean', conodont='ocean')
