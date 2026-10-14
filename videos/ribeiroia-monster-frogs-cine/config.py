# Per-video settings: chalkboards, metadata text, background mode per art theme.
CHALK = {
 4: dict(title="The Ney Pond Numbers", sub="Deformed northern leopard frogs near Henderson, Minnesota",
         rows=[("August 18, 1995", "60%", "of 53 frogs deformed", 'y', "On August 18, 1995"),
               ("One week later", "76%", "of 137 frogs deformed", 'c', "A week later"),
               ("September 1996", "47%", "of 70 frogs deformed", 'c', "And in September 1996")],
         concl=("Not one unlucky frog, but a whole population", "47 percent of 70"),
         src="Source: MNopedia, Deformed Frogs in Le Sueur County, 1995"),
 24: dict(title="Measuring the Damage", sub="Malformed frogs compared with normal frogs",
          rows=[("Jump distance", "41% shorter", "than normal frogs", 'y', "jumped 41 percent"),
                ("Swimming speed", "37% slower", "than normal frogs", 'c', "swam 37 percent"),
                ("Crickets caught", "55% fewer", "than normal frogs", 'c', "caught 55 percent")],
          concl=("Every survival skill fell far behind", "On every test"),
          src="Source: Goodman & Johnson (2011), PLOS ONE"),
 33: dict(title="Feeding the Parasite", sub="36 outdoor ponds, some enriched with nutrients",
          rows=[("Total snail mass", "+50%", "nearly, in enriched ponds", 'y', "rose by nearly 50 percent"),
                ("Cercariae per infected snail", "About 2x", "in enriched ponds", 'c', "about twice as many"),
                ("Tadpole infection", "2 to 5x", "in enriched ponds", 'c', "two to five times")],
          concl=("Fertilizer fed the snails, and the snails fed the parasite", "more infection"),
          src="Source: Johnson et al. (2007), PNAS"),
}
WHOOSH = []
TITLE = "The Parasite That Gives Frogs Extra Legs"
DESC = ["In 1995, students in Minnesota found frogs with missing, twisted and extra legs. Pollution was the first suspect, but in California the trail led to a tiny flatworm called Ribeiroia ondatrae.",
        "In this video, we follow the parasite from ram's horn snails to tadpoles to herons, see how its cysts can split a growing limb, measure how much slower malformed frogs become, and learn how fertilizer runoff and pond biodiversity change the outbreak."]
CHAPTERS = [(1, "A Hidden Nightmare"), (2, "The Discovery of 1995"), (5, "A Statewide Alarm"), (7, "Rounding Up the Suspects"),
            (9, "A Student in California"), (11, "The Decisive Experiment"), (13, "Was Minnesota Solved?"), (14, "A Three-Host Journey"),
            (19, "Splitting the Blueprint"), (26, "Why Would a Parasite?"), (30, "An Old Parasite"), (32, "The Human Fingerprint"),
            (35, "Safety in Numbers"), (37, "Amphibians Under Pressure"), (38, "The Web of Connections")]
SOURCES = ["MNopedia (Minnesota Historical Society): Deformed Frogs in Le Sueur County, 1995",
           "Johnson et al. (1999), The effect of trematode infection on amphibian limb development and survivorship, Science",
           "Johnson et al. (2003), Conservation Biology (historical amphibian malformations)",
           "Johnson et al. (2007), Aquatic eutrophication promotes pathogenic infection in amphibians, PNAS",
           "Goodman & Johnson (2011), PLOS ONE (performance of malformed frogs)",
           "Szuroczki, Vesprini et al. (2012), Presence of Ribeiroia ondatrae in the developing anuran limb disrupts retinoic acid levels, Parasitology Research",
           "Johnson et al. (2013), Nature (biodiversity and amphibian disease)",
           "Wikipedia: Ribeiroia ondatrae; Ribeiroia"]
HASHTAGS = "#MiyasLab #Frogs #Parasites #Biology #Nature"
BG = dict(pond='dusk', students='paper', helgen='paper', alarm='night', skin='paper', suspects='night', sessions='paper',
          johnson='dusk', cysts='night', tanks='paper', journal='paper', mystery='night', cycle='paper', snail='night',
          cercariae='night', tadpole='dusk', invasion='night', beads='paper', chemistry='night', mirror='paper', missing='night',
          jump='dusk', adults='paper', question='night', heron='dusk', predation='paper', gut='night', history='paper',
          jette='dusk', runoff='paper', cascade='night', diversity='dusk', tanks2='paper', decline='night', web='paper',
          worm='night', ending='dusk')
# Palettes (guideline 3-5): ponds, frogs, snails -> forest; lab work -> lab; old records -> history
PAL_DEFAULT = 'forest'
PAL = dict(cysts='lab', tanks='lab', journal='lab', beads='lab', chemistry='lab', tanks2='lab', history='history')

# cine sample: no chalkboards
CHALK = {}
