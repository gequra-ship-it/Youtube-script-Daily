# Per-video settings: chalkboards, metadata text, background mode per art theme.
CHALK = {
 21: dict(title="Giants, Measured Again", sub="Old sizes versus newer estimates",
          rows=[("Anomalocaris", "< 40 cm", "once said 1 m", 'y', "Anomalocaris was once"),
                ("Cameroceras", "~2 m", "once said 9 m", 'y', "Cameroceras was said"),
                ("Dunkleosteus", "~3.5 m", "once said 9 m", 'c', "And Dunkleosteus")],
          concl=("Bigger stories travel faster than measurements", "Bigger stories"),
          src="Source: Engelman (2023), Diversity · Wikipedia, Anomalocaris · Cameroceras"),
 30: dict(title="Thick Air, Big Bodies", sub="Oxygen in the Carboniferous air",
          rows=[("Air today", "21%", "oxygen", 'y', "Today, oxygen"),
                ("Carboniferous", "up to ~35%", "some models", 'c', "In the Carboniferous"),
                ("Meganeura", "~70 cm", "wingspan", 'c', "griffinfly Meganeura")],
          concl=("More oxygen, bigger bodies? Still debated", "still debate"),
          src="Source: Wikipedia, Carboniferous · Meganeura"),
 39: dict(title="Three Great Losses", sub="Paleozoic mass extinctions compared",
          rows=[("End-Ordovician", "~85%", "marine species", 'y', "end of the Ordovician"),
                ("Late Devonian", "~70%", "of species", 'y', "In the Late Devonian"),
                ("End-Permian", "~81%+", "marine species", 'c', "end of the Permian")],
          concl=("Life came close to the edge, more than once", "came close"),
          src="Source: Stanley (2016), PNAS · Wikipedia, extinction events"),
}
WHOOSH = []
TITLE = "The Paleozoic: 290 Million Years That Built Your Body"
DESC = ["Long before the dinosaurs, the Paleozoic Era gave life its shells, eyes, jaws, bones, forests, limbs and eggs for dry land, and then ended in the Great Dying, the worst mass extinction in the history of animal life.",
        "In this video, we travel from the Cambrian Explosion and the Burgess Shale to armored fish, the first walking fish, giant insects of the coal forests, the synapsids of Pangaea and the eruptions of the Siberian Traps, and we look at which famous sizes have been revised by newer studies."]
CHAPTERS = [(1, "Your Body Is a Museum"), (3, "The Cambrian Explosion"), (8, "A Very Strange Animal"), (10, "The Seas Fill Up"),
            (12, "Plants Leave the Water"), (14, "The First Great Extinction"), (17, "The Invention of Jaws"), (19, "The Age of Fishes"),
            (23, "Walking Fish"), (27, "Coal Forests"), (31, "An Egg for Dry Land"), (32, "One Giant Continent"),
            (36, "Fire Beneath Siberia"), (40, "The Unlikely Survivor"), (41, "What We Inherited")]
SOURCES = ["Engelman (2023), Size and body shape of Dunkleosteus terrelli, Diversity",
           "Stanley (2016), Estimates of the magnitudes of major marine mass extinctions in earth history, PNAS",
           "Sun et al. (2012), Lethally hot temperatures during the Early Triassic greenhouse, Science",
           "Botha (2020), The paleobiology and paleoecology of South African Lystrosaurus, PeerJ",
           "Natural History Museum, London (2021), Arthropleura news release",
           "Wikipedia: Opabinia; Anomalocaris; Cameroceras; Pterygotus; Permian-Triassic extinction event"]
HASHTAGS = "#MiyasLab #Paleozoic #Paleontology #Evolution #Fossils"
BG = dict(heartbeat='night', periods='paper', explosion='dusk', burgess='paper', anomalocaris='night', oralcone='paper',
          trilobite='dusk', opabinia='night', pikaia='paper', gobe='dusk', nautiloid='night',
          firstplants='dusk', icesheet='night', ordoextinct='paper', cooksonia='dusk', millipede='paper', jaws='night',
          pterygotus='dusk', dunkleosteus='night', dunksize='paper', lobefin='dusk', tiktaalik='paper', acanthostega='night',
          archaeopteris='dusk', deadzone='night', coalforest='paper', meganeura='night', arthropleura='paper',
          egg='dusk', pangaea='paper', dimetrodon='dusk', gorgonopsian='paper',
          cynodont='night', siberia='dusk', hotocean='paper', greatdying='night', lystrosaurus='dusk', toolkit='paper',
          ending='night')
# Palettes (guideline 3-5): Paleozoic seas -> ocean; land plants, coal forests, giant arthropods -> forest; Permian Pangaea and the Great Dying -> desert
PAL_DEFAULT = 'ocean'
PAL = dict(firstplants='forest', cooksonia='forest', millipede='forest', tiktaalik='forest', acanthostega='forest',
           archaeopteris='forest', coalforest='forest', meganeura='forest', arthropleura='forest', egg='forest', pangaea='desert', dimetrodon='desert', gorgonopsian='desert', cynodont='desert',
           siberia='desert', greatdying='desert', lystrosaurus='desert', ending='desert', heartbeat='desert')
