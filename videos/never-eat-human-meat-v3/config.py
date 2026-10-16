# Per-video settings: chalkboards, whoosh scenes, and the text for the metadata file.
# CHALK[i]: scene number -> chalkboard content. rows = (label, value, info, colour y|c, key phrase in narration where the row pops in)
# concl = (conclusion text, key phrase in narration where it pops in)
CHALK = {
 16: dict(title="What a Human Body Holds", sub="Approximate calories in an adult man's body",
          rows=[("Whole adult man", "126,000", "calories in total", 'y', "The numbers are modest"),
                ("Muscle only", "32,000", "the part that works like meat", 'c', "Only about 32,000"),
                ("Heart", "650", "Brain and spinal cord: 2,700", 'c', "The heart gives")],
          concl=("Muscle is only about a quarter of the total", "and the brain and spinal cord"),
          src="Source: Cole (2017), Scientific Reports"),
 17: dict(title="A Bad Deal on Calories", sub="Approximate calories offered by each animal",
          rows=[("Deer muscle", "163,000", "five times human muscle (about 32,000)", 'y', "Compare that"),
                ("Woolly rhinoceros", "1.26 million", "calories offered", 'c', "A woolly rhinoceros offers"),
                ("Woolly mammoth", "3.6 million", "calories offered", 'c', "and a woolly mammoth")],
          concl=("A big animal beat a person as a meal", "For hunters"),
          src="Source: Cole (2017), Scientific Reports"),
}

WHOOSH = [1, 5, 8, 15, 22, 26]          # scene numbers that start with a whoosh (4-8 per video)
TITLE = "The Terrifying Science of Why You Must Never Eat Human Meat"
DESC = ["Why does nature punish cannibalism? Follow the kuru epidemic among the Fore people of Papua New Guinea and the misfolded proteins called prions that cause it.",
        "In this video, we look at how a funeral ritual spread a fatal brain disease, why prions survive cooking and fool the immune system, what the 1990s mad cow outbreak taught medicine, and what the calorie count says about eating people. We also look at the evidence that disgust may protect us."]
CHAPTERS = [(1, "The Ultimate Biological Taboo"), (2, "Mystery in the Highlands"), (5, "The Funeral Ritual"), (8, "Neither Virus nor Bacteria"),
            (11, "Why Cooking Does Not Help"), (14, "Echoes of Mad Cow Disease"), (15, "The Calorie Count"), (20, "The Species Barrier"),
            (23, "Traces in Our DNA"), (26, "The Final Verdict")]   # (scene number, English Title Case, <=5 words); first becomes 00:00
SOURCES = ["James Cole, University of Brighton, 2017 study on the calories in human bodies, Scientific Reports"]
HASHTAGS = "#MiyasLab #Prions #Kuru #Science #Biology"

# background mode per art theme (new look): paper / night / dusk
BG = dict(lab='paper', highlands='dusk', patient='paper', doctors='paper', funeral='night', hut='paper', brain='night', particle='night',
          fold='night', domino='paper', fire='night', immune='night', calendar='paper', cattle='dusk', archaeo='paper', hunters='dusk',
          pyramid='paper', lock='night', insula='night', groups='paper', dna='night', highlands2='dusk', hospital='paper', scale='paper',
          modern='dusk', night='night')
