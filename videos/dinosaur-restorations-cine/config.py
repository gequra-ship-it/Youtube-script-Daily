# Per-video settings: chalkboards, metadata text, background mode per art theme.
CHALK = {
 8: dict(title="Three Iguanodons", sub="How one dinosaur was redrawn",
         rows=[("1825", "giant iguana", "Mantell, from teeth", 'y', "In 1825"),
               ("1854", "horn on the nose", "Crystal Palace", 'y', "In 1854"),
               ("1878 on", "thumb spike", "Bernissart skeletons", 'c', "after the Bernissart")],
         concl=("Same animal, three pictures", "the horn moved"),
         src="Source: Wikipedia, Iguanodon · Crystal Palace Dinosaurs"),
 32: dict(title="Four Versions of Spinosaurus", sub="A century of redrawing",
          rows=[("1915", "sail-backed giant", "Stromer", 'y', "In 1915"),
                ("1944", "fossils destroyed", "Munich bombing", 'c', "In 1944"),
                ("2014-2020", "short legs, paddle tail", "Ibrahim et al.", 'y', "In 2014")],
          concl=("Still being argued about", "still arguing"),
          src="Source: Ibrahim et al. (2014, 2020) · Wikipedia, Spinosaurus"),
 41: dict(title="Colors From Fossils", sub="Pigment structures read from fossil feathers",
          rows=[("Sinosauropteryx", "striped tail", "2010", 'y', "In 2010"),
                ("Anchiornis", "red crest", "2010", 'y', "The same year"),
                ("Microraptor", "glossy black", "2012", 'c', "In 2012")],
          concl=("Colors backed by evidence", "backed by evidence"),
          src="Source: Zhang et al. (2010) · Li et al. (2010, 2012)"),
}
WHOOSH = []
TITLE = "How Our Pictures of Dinosaurs Kept Getting It Wrong"
DESC = ["Iguanodon once had a horn on its nose, Elasmosaurus had its head on its tail, and Hallucigenia was drawn upside down and backwards. For 170 years, scientists and artists have kept redrawing extinct animals as new fossils turned up.",
        "In this video, we follow paleoart from the Crystal Palace sculptures and the Bone Wars to swamp-bound sauropods, tail-dragging T. rex, the Dinosaur Renaissance, the many lives of Spinosaurus, shrink-wrapping, lips, feathers and the first real dinosaur colors."]
CHAPTERS = [(1, "A Beast in the Park"), (3, "The Iguana Tooth"), (6, "Crystal Palace"), (9, "The Bone Wars"), (12, "The Roof Lizard"),
            (14, "Charles R. Knight"), (15, "Giants in the Swamp"), (17, "The Tail-Dragging Tyrant"), (19, "Cambrian Puzzles"),
            (24, "The Dinosaur Renaissance"), (27, "Spinosaurus"), (33, "Shrink-Wrapped"), (36, "Feathers"), (38, "Real Colors"),
            (42, "Scales, Air and Growth"), (47, "What Will They Think of Us?")]
SOURCES = ["Zhang et al. (2010), Fossilized melanosomes and the colour of Cretaceous dinosaurs and birds, Nature",
           "Li et al. (2010), Plumage color patterns of an extinct dinosaur, Science; Li et al. (2012), Reconstruction of Microraptor and the evolution of iridescent plumage, Science",
           "Turner et al. (2007), Feather quill knobs in the dinosaur Velociraptor, Science",
           "Bell et al. (2017), Tyrannosauroid integument reveals conflicting patterns of gigantism and feather evolution, Biology Letters",
           "Cullen et al. (2023), Theropod dinosaur facial reconstruction and the importance of soft tissues in paleobiology, Science",
           "Ibrahim et al. (2014), Science; Ibrahim et al. (2020), Nature (Spinosaurus)",
           "Tschopp et al. (2015), A specimen-level phylogenetic analysis and taxonomic revision of Diplodocidae, PeerJ",
           "Smith & Caron (2015), Hallucigenia's head and the pharyngeal armature of early ecdysozoans, Nature",
           "Wikipedia: Iguanodon; Crystal Palace Dinosaurs; Elasmosaurus; Stegosaurus; Anomalocaris; Spinosaurus; All Yesterdays"]
HASHTAGS = "#MiyasLab #Dinosaurs #Paleontology #Paleoart #Science"
BG = dict(park='dusk', dragons='night', teeth='paper', nosehorn='paper', bernissart='night', crystalpalace='dusk', dinner='night',
          bonewars='dusk', elasmosaurus='paper', brontosaurus='night', stegosaurus='paper', secondbrain='night',
          knight='paper', swamp='dusk', pressure='paper', tailtrex='night', trackways='dusk', burgess='paper', anomalocaris='night',
          reunion='paper', hallucigenia='dusk', flipped='paper', deinonychus='dusk', bakker='paper', jurassic='night',
          spinosaurus='dusk', bombing='night', jp3='night', shortlegs='paper', paddletail='dusk', shrinkwrap='paper',
          allyesterdays='night', lips='dusk', sinosauropteryx='paper', velociraptor='dusk', melanosomes='night', ginger='paper',
          anchiornis='dusk', scalytrex='paper', airsacs='night', growth='paper', triceratops='dusk', timeline='paper',
          future='night', ending='dusk')
# Palettes (guideline 3-5): history of science, museums, artists -> history; living dinosaurs in their world -> forest; Cambrian seas -> ocean
PAL_DEFAULT = 'history'
PAL = dict(swamp='forest', trackways='forest', deinonychus='forest', jurassic='forest', shortlegs='forest', paddletail='forest',
           lips='forest', sinosauropteryx='forest', velociraptor='forest', ginger='forest', anchiornis='forest', scalytrex='forest',
           airsacs='forest', triceratops='forest', burgess='ocean', anomalocaris='ocean', reunion='ocean', hallucigenia='ocean',
           flipped='ocean', elasmosaurus='ocean')

# cine sample: no chalkboards
CHALK = {}
