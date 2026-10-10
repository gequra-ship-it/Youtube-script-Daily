# Per-video settings: chalkboards, metadata text, background mode per art theme.
CHALK = {
 15: dict(title="The Four Stages", sub="How long each stage of a whale fall can last",
          rows=[("Stage 1: mobile scavengers", "Up to 1.5 years", "from a few months", 'y', "The mobile scavenger stage lasts"),
                ("Stage 2: enrichment opportunists", "Up to 4.5 years", "from a few months", 'c', "The enrichment opportunist stage lasts"),
                ("Stage 3: sulfur lovers", "50 to 100 years", "possibly the longest", 'c', "And the sulfophilic stage")],
          concl=("Then come the bare bones: the reef stage", "50 to possibly 100 years"),
          src="Source: Wikipedia, Whale fall"),
 25: dict(title="The Tiny Males", sub="Inside the tube of a female Osedax",
          rows=[("Dwarf males per female", "50 to 100", "living in her tube", 'y', "Between 50 and 100"),
                ("Male growth", "Larval size", "never grow up", 'c', "They never grow"),
                ("Female vs. male", "20,000x larger", "or more", 'c', "more than 20,000 times")],
          concl=("One of the biggest size gaps in the animal world", "the females are more than"),
          src="Source: Wikipedia, Osedax"),
 30: dict(title="How Many Whale Falls?", sub="Large whale carcasses decaying at any one time",
          rows=[("Carcasses in decay", "About 690,000", "nine largest whale species", 'y', "around 690,000"),
                ("Average spacing", "About 12 km", "across the oceans", 'c', "about 12 kilometers"),
                ("Along migration routes", "About 5 km", "or even closer", 'c', "as little as 5 kilometers")],
          concl=("Close enough for larvae to hop between them", "along whale migration routes"),
          src="Source: Wikipedia, Whale fall"),
 35: dict(title="Whales and Carbon", sub="What one carcass carries to the deep",
          rows=[("Typical carcass", "40 tonnes", "of whale", 'y', "40 tonnes"),
                ("Carbon inside", "About 2 tonnes", "locked in the body", 'c', "about two tonnes"),
                ("Normal delivery to 1 hectare", "100-200 years", "of abyssal seafloor", 'c', "100 to 200 years")],
          concl=("Centuries of carbon, delivered in one day", "in about 100 to 200 years"),
          src="Source: Wikipedia, Whale fall"),
}
WHOOSH = []
TITLE = "What Happens When a Whale Dies in the Deep Sea"
DESC = ["When a whale dies and sinks, its body can feed life in the dark deep sea for decades. Follow a whale fall from the surface to the abyss and through every stage of an ecosystem built on one carcass.",
        "In this video, we meet sleeper sharks, hagfish and giant isopods, the bone-eating Osedax worms with no mouth and no gut, bacteria that turn bone fat into chemical energy, fossil traces 30 to 100 million years old, and what whaling took from the deep ocean."]
CHAPTERS = [(1, "The Gentle Giants"), (3, "To Float or to Sink"), (5, "The Descent"), (9, "The Accidental Discovery"),
            (10, "The Scavengers Arrive"), (15, "The Four Stages"), (16, "The Opportunists"), (19, "The Sulfur Lovers"),
            (22, "The Bone-Eating Worm"), (27, "Older Than Whales"), (29, "Stepping Stones"), (31, "The Reef Stage"),
            (34, "The Carbon Sink"), (36, "The Cost of Whaling"), (38, "The Cycle Reborn")]
SOURCES = ["Wikipedia: Whale fall; Osedax; Bathynomus giganteus; Exploding whale",
           "Smith et al. (2014), Seven-year enrichment: macrofaunal succession in deep-sea sediments around a 30 tonne whale fall in the Northeast Pacific",
           "Baco & Smith (2003), High species richness in deep-sea chemoautotrophic whale skeleton communities, Marine Ecology Progress Series",
           "Kiel et al. (2010), Fossil traces of the bone-eating worm Osedax in early Oligocene whale bones",
           "Danise & Higgs (2015), Bone-eating Osedax worms lived on Mesozoic marine reptile deadfalls, Biology Letters",
           "Rocha, Clapham & Ivashchenko (2014), Emptying the Oceans, Marine Fisheries Review",
           "Max Planck Institute for Marine Microbiology: Symbioses in wood-boring bivalves"]
HASHTAGS = "#MiyasLab #WhaleFall #DeepSea #Ocean #MarineBiology"
BG = dict(bluewhale='dusk', lastbreath='dusk', float='paper', explode='paper', descent='night', layers='paper', snow='night',
          touchdown='night', discovery='paper', scent='night', sharks='night', hagfish='night', isopods='paper', strip='night',
          opportunist='paper', sevenyear='paper', bones='night', sulfophilic='night', chemo='night', crowded='paper',
          osedax='night', plumes='paper', roots='night', otherbones='paper', fossilbone='paper', plesiosaur='dusk',
          stepping='dusk', reef='night', woodfall='dusk', survey='paper', carbon='night', whaling='dusk', rov='night',
          cycle='dusk', ending='dusk')
# Palettes (guideline 3-5): deep sea -> ocean; whaling/fossils -> history; research vessels and surveys -> lab
PAL_DEFAULT = 'ocean'
PAL = dict(whaling='history', fossilbone='history', plesiosaur='history', discovery='lab', survey='lab', rov='lab')
