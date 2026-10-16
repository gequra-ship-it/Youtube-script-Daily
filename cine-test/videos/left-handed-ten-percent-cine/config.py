# Per-video settings: chalkboards, metadata text, background mode per art theme.
CHALK = {
 9: dict(title="The Lefties Come Back", sub="Self-reported left-handers by birth cohort, United States",
         rows=[("Born ~1900", "~3%", "said left-handed", 'y', "born around 1900"),
               ("Born after ~1950", "~11-12%", "said left-handed", 'c', "second half of the century"),
               ("The biology", "unchanged", "the pressure lifted", 'y', "The biology")],
         concl=("Hidden, not new", "forced to hide"),
         src="Source: Gilbert & Wysocki (1992) · LiveScience (2007)"),
 12: dict(title="Genes, but Not a Switch", sub="How strongly handedness is inherited",
          rows=[("Two left-handed parents", "~26%", "left-handed child", 'y', "two left-handed parents"),
                ("Identical twins", "1 in 5", "pairs disagree", 'c', "identical twins"),
                ("Genes explain", "~25%", "of the variation", 'y', "genes account")],
          concl=("It runs in families, without a simple rule", "runs in families"),
          src="Source: Wikipedia, Handedness · twin studies"),
 26: dict(title="Violence and the Left Hand", sub="Traditional societies compared",
          rows=[("Dioula, Burkina Faso", "3.4%", "left-handed", 'y', "Among the Dioula"),
                ("Eipo, New Guinea", "27%", "left-handed", 'c', "Among the Eipo"),
                ("The pattern", "more violence", "more left-handers", 'y', "higher homicide rates")],
          concl=("A correlation, not proof", "It's a correlation"),
          src="Source: Faurie & Raymond (2005), Proc. R. Soc. B"),
}
WHOOSH = []
TITLE = "Why Are Only 10% of People Left-Handed?"
DESC = ["About one person in ten is left-handed, and the ratio is far older than our species: Ice Age hand stencils and 400,000-year-old teeth show the same right-handed majority. So why didn't evolution settle at fifty-fifty, or wipe left-handers out?",
        "In this video, we follow the evidence from cave walls and fossil teeth to forced hand-switching in schools, twin studies and the Oxford UK Biobank genome study, fetal thumb-sucking and the spinal cord, the lopsided brain, and the fighting hypothesis that may keep left-handers at about ten percent. We also check a few popular myths along the way."]
CHAPTERS = [(1, "Nine Out of Ten"), (3, "Ancient Hands"), (6, "The Sinister Side"), (8, "Forced to Switch"), (10, "Is It Genetic?"),
            (15, "Decided in the Womb"), (17, "The Lopsided Brain"), (20, "Other Animals"), (22, "Cooperation"),
            (24, "The Fighting Hypothesis"), (27, "Southpaws in Sport"), (29, "Myths and Claims"), (34, "Presidents and Gestures"),
            (39, "A Spectrum"), (41, "Why Ten Percent")]
SOURCES = ["Faurie & Raymond (2005), Handedness, homicide and negative frequency-dependent selection, Proc. R. Soc. B",
           "Abrams & Panaggio (2012), A model balancing cooperation and competition can explain our right-handed world, J. R. Soc. Interface",
           "Wiberg et al. (2019), Handedness, language areas and neuropsychiatric diseases, Brain",
           "Ocklenburg et al. (2017), Epigenetic regulation of lateralized fetal spinal gene expression underlies hemispheric asymmetries, eLife",
           "Hepper et al. (1990, 1998, 2005), fetal arm movement and thumb-sucking studies",
           "Casasanto & Jasmin (2010), Good and bad in the hands of politicians, PLoS ONE",
           "Papadatou-Pastou et al. (2020), Human handedness: a meta-analysis, Psychological Bulletin",
           "Wikipedia: Handedness"]
HASHTAGS = "#MiyasLab #LeftHanded #Evolution #Neuroscience #Science"
BG = dict(crowd='dusk', tools='paper', stencil='night', teeth='paper', neanderthal='dusk', latin='paper', medieval='night',
          classroom='paper', dna='night', twins='paper', biobank='night', microtubule='dusk', womb='night', spine='paper',
          brain='night', gesture='dusk', lefthbrain='paper', chimp='dusk', animals='paper', campfire='night', model='paper',
          duel='dusk', frequency='paper', boxing='night', tennis='dusk', davinci='paper', creative='dusk', headline='paper',
          workshop='night', neuro='paper', presidents='dusk', debate='night', hormone='paper', birth='dusk', map='night',
          spectrum='paper', symmetry='night', fiftyfifty='dusk', lefttools='paper', ending='dusk')
# Palettes (guideline 3-5): science of brain/genes -> lab; prehistory, language, religion, schools -> history; womb, birth, body -> body
PAL_DEFAULT = 'lab'
PAL = dict(stencil='history', teeth='history', neanderthal='history', latin='history', medieval='history', classroom='history',
           campfire='history', duel='history', davinci='history', twins='body', womb='body', spine='body', hormone='body', birth='body')

# cine sample: no chalkboards
CHALK = {}
