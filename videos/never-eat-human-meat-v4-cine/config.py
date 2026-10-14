# Per-video settings: chalkboards, metadata text, background mode per art theme.
CHALK = {
 4: dict(title="Kuru by the Numbers", sub="The epidemic among the Fore of Papua New Guinea",
         rows=[("Deaths per year at the peak", "About 200", "around 1957", 'y', "about 200 people died"),
               ("Total deaths", "About 2,700", "over the decades", 'c', "In total"),
               ("Women and children vs. men", "8 to 9 times", "more common at the peak", 'c', "And at the height")],
         concl=("A disease that chose its victims", "than among men"),
         src="Source: Wikipedia, Kuru (disease)"),
 18: dict(title="The Mad Cow Toll", sub="Bovine spongiform encephalopathy in the United Kingdom",
          rows=[("Cattle diagnosed, 1986 to 2015", "184,000+", "in the United Kingdom", 'y', "more than 184,000"),
                ("Cows killed", "About 4 million", "to stop the outbreak", 'c', "About four million"),
                ("Human deaths by 2014", "177", "variant Creutzfeldt-Jakob disease", 'c', "And by 2014")],
          concl=("Feeding cattle to cattle came at a huge cost", "177 people had died"),
          src="Source: Wikipedia, Bovine spongiform encephalopathy"),
 22: dict(title="What a Human Body Holds", sub="Approximate calories in an adult man's body",
          rows=[("Whole adult man", "126,000", "calories in total", 'y', "The numbers are modest"),
                ("Muscle only", "32,000", "the part that works like meat", 'c', "Only about 32,000"),
                ("Heart", "650", "Brain and spinal cord: 2,700", 'c', "The heart gives")],
          concl=("Muscle is only about a quarter of the total", "and the brain and spinal cord"),
          src="Source: Cole (2017), Scientific Reports"),
 23: dict(title="A Bad Deal on Calories", sub="Approximate calories offered by each animal",
          rows=[("Deer muscle", "163,000", "five times human muscle (about 32,000)", 'y', "Compare that"),
                ("Woolly rhinoceros", "1.26 million", "calories offered", 'c', "A woolly rhinoceros offers"),
                ("Woolly mammoth", "3.6 million", "calories offered", 'c', "and a woolly mammoth")],
          concl=("A big animal beat a person as a meal", "For hunters"),
          src="Source: Cole (2017), Scientific Reports"),
}
WHOOSH = []
TITLE = "The Terrifying Science of Why You Must Never Eat Human Meat"
DESC = ["Why does nature punish cannibalism? Follow the kuru epidemic among the Fore people of Papua New Guinea, the misfolded proteins called prions, and a protective gene that appeared in the survivors.",
        "In this video, we look at how a funeral ritual spread a fatal brain disease, why prions survive cooking and fool the immune system, what mad cow disease and chronic wasting disease reveal, what 800,000-year-old cut marks and a calorie count say about eating people, and why disgust may protect us."]
CHAPTERS = [(1, "The Ultimate Biological Taboo"), (2, "Mystery in the Highlands"), (6, "The Funeral Ritual"), (9, "Proof in the Laboratory"),
            (10, "Neither Virus nor Bacteria"), (14, "Why Cooking Does Not Help"), (17, "Echoes of Mad Cow Disease"), (20, "Ancient Cut Marks"),
            (21, "The Calorie Count"), (25, "Pollutants and Germs"), (28, "The Chemistry of Disgust"), (31, "Traces in Our DNA"),
            (33, "The End of an Epidemic"), (35, "The Final Verdict")]
SOURCES = ["James Cole (2017), Assessing the calorific significance of episodes of human cannibalism in the Palaeolithic, Scientific Reports",
           "Mead et al. (2003), Balancing selection at the prion protein gene consistent with prehistoric kuru-like epidemics, Science",
           "Mead et al. (2009), A novel protective prion protein variant that colocalizes with kuru exposure, New England Journal of Medicine",
           "Wikipedia: Kuru (disease); Bovine spongiform encephalopathy; Creutzfeldt-Jakob disease; Scrapie; Chronic wasting disease",
           "National Geographic (2010), Gran Dolina cannibalism; Live Science (2011), Gough's Cave skull cups"]
HASHTAGS = "#MiyasLab #Prions #Kuru #Science #Biology"
BG = dict(lab='night', highlands='dusk', patient='paper', doctors='paper', funeral='night', hut='dusk', brain='night', chimp='paper',
          particle='night', fold='night', domino='paper', family='paper', fire='night', immune='night', calendar='paper', cattle='dusk',
          animals='dusk', archaeo='paper', scale='paper', hunters='dusk', pyramid='paper', lock='night', key='night', insula='night',
          groups='paper', fire2='dusk', dna='night', shield='dusk', highlands2='dusk', hospital='paper', verdict='paper', modern='night')

# cine sample: no chalkboards
CHALK = {}
