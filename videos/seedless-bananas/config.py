# Per-video settings (guideline 3-5, 12, 17, 20-2): chalkboards, metadata text, background mode and palette per art theme.
CHALK = {
 9: dict(title="Sets of Chromosomes", sub="Why the seeds fail",
         rows=[("Wild banana", "2 sets", "of chromosomes", 'y', "two sets"),
               ("Cavendish banana", "3 sets", "of chromosomes", 'c', "three sets"),
               ("Result", "Few seeds", "nearly sterile", 'y', "seeds fail")],
         concl=("An odd number cannot pair evenly", "odd number"),
         src="Source: banana genetics (ProMusa) · triploid cultivars"),
 27: dict(title="Banana Numbers", sub="One clone carries the trade",
          rows=[("Harvested each year", "100+ M tons", "all banana types", 'y', "one hundred million tons"),
                ("Cavendish in exports", "95-99%", "estimates vary", 'c', "ninety-five to ninety-nine percent"),
                ("New plant to fruit", "~1 year", "roughly", 'y', "roughly a year")],
          concl=("A lot to ride on one clone", "one clone"),
          src="Source: FAO banana statistics · trade estimates (vary by source)"),
 35: dict(title="Tiny Numbers", sub="Potassium-40 in a banana",
          rows=[("K-40 in potassium", "0.012%", "of natural potassium", 'y', "zero point zero one two percent"),
                ("One banana", "~0.1 µSv", "usual estimate", 'c', "zero point one microsieverts"),
                ("Body potassium", "Steady", "kept in balance", 'y', "steady")],
          concl=("Tiny dose, no build-up", "build up radiation"),
          src="Source: banana equivalent dose (informal estimate)"),
 44: dict(title="The Banana Journey", sub="From farm to shelf",
          rows=[("Harvest", "Green", "picked unripe", 'y', "picked green"),
                ("Shipping", "~13 °C", "chilled", 'c', "thirteen degrees Celsius"),
                ("Ripening room", "A few days", "ethylene + warmth", 'y', "a few days")],
          concl=("Timing turns green into yellow", "ripening room"),
          src="Source: banana industry ripening practice (typical values)"),
}
WHOOSH = []
TITLE = "The Secret Life of Bananas: How Do Seedless Bananas Even Exist?"
DESC = ["How can a fruit with no seeds spread across the whole world? Bananas are nearly sterile plants that people grow by cloning, and that one fact hides a surprising chain of stories: a famous banana that the world largely lost, a fungus that now threatens the one we eat, and a slightly radioactive snack.",
        "In this video, we follow the banana from its wild, seed-filled ancestors to triploid chromosomes, parthenocarpy, suckers and tissue culture, then uncover three secrets: Big Mike and Panama disease, the spread of TR4, and the science of potassium-40, plus berries, banana republics, ripening rooms, and the frozen gene bank in Belgium."]
CHAPTERS = [(1, "The Seedless Puzzle"), (5, "Wild Ancestors"), (7, "Three Sets of Chromosomes"), (12, "A Giant Herb"), (14, "Cloning by Hand"),
            (18, "Secret One: Big Mike"), (21, "Panama Disease"), (24, "The Cavendish Arrives"), (26, "Secret Two: TR4"),
            (31, "The Race for Resistance"), (33, "Secret Three: Radioactive"), (38, "Berries and Curves"), (41, "Banana Republics"),
            (42, "Ripening Science"), (50, "The Frozen Vault")]
SOURCES = ["ProMusa: Domestication of the banana (banana remains about 7,000 years old, Kuk Swamp, New Guinea)",
           "Chatsworth House: The Chatsworth banana (Cavendish banana, Mauritius, Joseph Paxton)",
           "Frontiers in Plant Science (2024): Fusarium Tropical Race 4 in Latin America and the Caribbean (Colombia 2019, Peru 2021, Venezuela 2023)",
           "QUT: QCAV-4 genetically modified Cavendish banana approval (2024)",
           "Alliance of Bioversity International and CIAT: International Musa Germplasm Transit Centre (Leuven)",
           "FAO: banana facts and figures"]
HASHTAGS = "#MiyasLab #Bananas #Botany #PanamaDisease #Biology"
BG = dict(counter='dusk', splitfruit='paper', plantation='dusk', three='night', jungle='dusk', wildbanana='paper', species='paper', triploid='night',
          chalk1='paper', parthenocarpy='dusk', farmers='dusk', pseudostem='paper', corm='night', suckers='paper', lab='night', clones='dusk',
          loop='paper', secret1='night', grosmichel='dusk', flavor='paper', fungus='night', diversity='paper', collapse='dusk', chatsworth='paper',
          compromise='dusk', secret2='night', chalk2='paper', tr4='night', spread='paper', colombia='dusk', crispr='night', varieties='paper',
          secret3='night', potassium='night', chalk3='paper', detectors='dusk', worry='paper', berry='paper', curve='dusk', bunch='paper',
          republic='dusk', ethylene='night', ship='dusk', chalk4='paper', ripening='paper', sugarspots='dusk', matooke='paper', sprayplane='dusk',
          summary='night', vault='night', hand='dusk', question='paper', cta='dusk')
# Palettes (guideline 3-5): plants and fruit -> forest; science/radiation/genetics -> lab; trade history -> history; fungus and disease -> storm; ripening and food -> body
PAL_DEFAULT = 'forest'
PAL = dict(triploid='lab', lab='lab', crispr='lab', secret3='lab', potassium='lab', detectors='lab', worry='lab', chalk3='lab', chalk1='lab',
           farmers='history', grosmichel='history', collapse='history', chatsworth='history', republic='history', compromise='history',
           fungus='storm', tr4='storm', spread='storm', colombia='storm', secret2='storm', diversity='storm',
           ethylene='body', ship='ocean', chalk4='body', ripening='body', sugarspots='body', matooke='desert', sprayplane='storm',
           vault='ice', cta='sunset', hand='sunset', question='sunset')

HOOK = dict(until=300, maxu=5.5)   # guideline 20-2
