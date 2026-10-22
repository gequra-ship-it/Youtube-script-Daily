# Per-video settings (guideline 3-5, 12, 17, 20-2): chalkboards, metadata text, background mode and palette per art theme.
CHALK = {
 4: dict(title="A Long Reign", sub="Ammonoids, rough dates",
         rows=[("First ammonoids", "~400 Ma", "early Devonian Period", 'y', "four hundred million years ago"),
               ("Asteroid impact", "66 Ma", "end of the Cretaceous", 'c', "sixty-six million years ago"),
               ("Their reign", "300+ Ma", "more than 300 million years", 'y', "more than three hundred million years")],
         concl=("Over 300 million years of dominance", "dominance"),
         src="Source: ammonoid fossil record (commonly cited dates); Ma = million years ago"),
 13: dict(title="Where They Lived", sub="Typical depth ranges",
          rows=[("Many ammonites", "0-100 m", "sunlit upper ocean", 'y', "zero to one hundred meters"),
                ("Nautilus today", "200-700 m", "twilight reef slopes", 'c', "two hundred to seven hundred meters"),
                ("Light", "Bright vs. dim", "surface vs. twilight", 'y', "bright water")],
          concl=("Two very different worlds", "different"),
          src="Source: ammonite and nautilus ecology (approximate; ammonite depth varied by species)"),
 23: dict(title="Two Ways to Start Life", sub="Size at the beginning",
          rows=[("Ammonite hatchling", "~1 mm", "tiny, drifting", 'y', "one millimeter"),
                ("Nautilus egg", "~3 cm", "large, full of yolk", 'c', "three centimeters"),
                ("Nautilus hatching", "~1 year", "slow, cold development", 'y', "almost a year")],
          concl=("Quantity versus quality", "quality"),
          src="Source: ammonitella size from fossils; nautilus egg and hatching time from aquarium observations"),
 37: dict(title="The Survival Scorecard", sub="Three differences",
          rows=[("Metabolism", "High vs. low", "ammonite vs. nautilus", 'y', "low metabolism"),
                ("Food", "Plankton vs. scraps", "fragile vs. flexible", 'c', "plankton"),
                ("Young", "~1 mm vs. ~3 cm", "drifting vs. self-reliant", 'y', "three centimeters")],
          concl=("The nautilus was built for lean times", "lean times"),
          src="Source: comparisons from the evidence discussed in this video (several are inferences)"),
 47: dict(title="Protection Timeline", sub="Nautilus and CITES",
          rows=[("Countries vote", "2016", "CITES meeting", 'y', "2016"),
                ("Rule takes effect", "2017", "all nautiluses listed", 'c', "2017"),
                ("Listing", "Appendix II", "exports need permits", 'y', "Appendix II")],
          concl=("Trade is now regulated", "regulated"),
          src="Source: CITES listing of the family Nautilidae (agreed 2016, in force 2017)"),
}
WHOOSH = []
TITLE = "Why Did Ammonites Perish While the Nautilus Survived?"
DESC = ["Ammonites and the nautilus look like twins, yet only one of them survived the asteroid that ended the age of dinosaurs. What decided their fates?",
        "In this video, we compare where they lived, what they ate, how fast they burned energy, and how they raised their young, then follow the impact winter that collapsed the sunlit ocean, and finish with the threats the nautilus faces today."]
CHAPTERS = [(1, "Two Identical Shells"), (3, "The Evolutionary Paradox"), (5, "A Record of Resilience"), (6, "Beneath the Spiral Shell"), (7, "Hidden Architecture"),
            (11, "Kings of the Sunlit Waters"), (14, "Pushed Into the Deep"), (15, "What They Ate"), (18, "The Engine of Life"), (19, "The Secret of the Eggs"),
            (26, "The Cosmic Hammer Falls"), (27, "The Impact Winter"), (30, "Starvation in the Shallows"), (32, "The Sanctuary of the Abyss"),
            (37, "The Survival Scorecard"), (38, "The Irreversible Boundary"), (40, "The Rise of Soft-Bodied Cousins"), (43, "A New Threat"),
            (46, "A Race for Protection"), (48, "Lessons from a Survivor"), (53, "The Fragile Spiral of Life")]
SOURCES = ["Schulte et al. (2010). The Chicxulub asteroid impact and mass extinction at the Cretaceous-Paleogene boundary. Science",
           "Kruta et al. (2011). Role of ammonites in the Mesozoic marine food web revealed by jaw preservation. Science",
           "Honisch et al. (2012). The geological record of ocean acidification. Science",
           "CITES: listing of the family Nautilidae in Appendix II (agreed 2016, in force 2017)"]
HASHTAGS = "#MiyasLab #Ammonite #Nautilus #MassExtinction #Paleontology"
BG = dict(twins='night', asteroid='night', museum='paper', chalk_reign='paper', resilience='dusk', tree='paper', xray='paper', siphon='paper', suture='night',
          unknown='paper', sunlit='dusk', twilight='night', chalk1='paper', retreat='dusk', radula='paper', scavenger='night', jet='dusk', metabolism='dusk',
          eggs='paper', tinyeggs='dusk', plankton='dusk', nursery='night', chalk2='paper', year='night', ready='dusk', hammer='night', winter='night',
          bloomgone='dusk', acid='night', starve='dusk', severed='night', sanctuary='night', marinesnow='night', famine='night', yolk='dusk', hatch='paper',
          chalk3='paper', boundary='paper', indexfossil='paper', coleoid='dusk', narrow='dusk', survivor='night', threat='dusk', slowgrowth='paper',
          acidecho='night', cites='paper', chalk_cites='paper', lesson='dusk', underdog='night', holding='paper', timeline='paper', guardians='dusk',
          spiral='night', cta='dusk')
PAL_DEFAULT = 'ocean'
PAL = dict(twins='ocean', asteroid='space', museum='history', chalk_reign='history', resilience='storm', tree='lab', xray='lab', siphon='lab', suture='lab',
           unknown='history', chalk1='lab', retreat='ocean', radula='lab', metabolism='body', eggs='body', nursery='body', chalk2='body', hammer='storm',
           winter='storm', bloomgone='storm', acid='storm', yolk='body', chalk3='lab', boundary='history', indexfossil='history', threat='storm',
           slowgrowth='body', acidecho='lab', cites='lab', chalk_cites='lab', holding='history', timeline='history', cta='sunset')
HOOK = dict(until=300, maxu=5.5)   # guideline 20-2
