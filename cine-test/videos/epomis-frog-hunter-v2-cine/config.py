# Per-video settings: chalkboards, whoosh scenes, metadata text, background mode per art theme.
CHALK = {
 7: dict(title="The Closer, the Harder", sub="Lure movements of a larva as a young toad comes near",
         rows=[("Toad 15 cm away", "2.8", "lure movements per minute", 'y', "When the toad was fifteen"),
               ("Toad 1 cm away", "4.9", "lure movements per minute", 'c', "When the toad was one centimeter"),
               ("Empty cage", "About 1", "lure movement per minute", 'c', "With an empty cage")],
         concl=("The closer the predator, the harder the bait works", "The closer the predator came"),
         src="Source: Wizen and Gasith (2011), PLoS ONE"),
 18: dict(title="How the Face-Offs Ended", sub="Larvae against young frogs and toads in the lab",
          rows=[("Trials run", "382", "one larva against one amphibian", 'y', "The researchers ran"),
                ("Larva gulped, then spat out", "7", "times, out of 382", 'c', "Only seven times"),
                ("Toad swallowed a larva", "1", "spat it out after about two hours", 'c', "In one more case")],
          concl=("Almost every time, the amphibian lost", "Almost every time"),
          src="Source: Wizen and Gasith (2011), PLoS ONE"),
}
WHOOSH = []
TITLE = "How a Tiny Beetle Larva Turns Frogs Into Its Meal"
DESC = ["What happens when an insect refuses to be a frog's dinner? The larva of the Epomis ground beetle lures frogs and toads, dodges the tongue in almost every encounter, and feeds on the animal that came to eat it.",
        "In this video, we look at how frogs see their prey, the lure and the double-hooked jaws, the 382 lab trials from Israel, the adult beetle's night ambush, and the questions scientists still cannot answer. We also meet other small hunters that break the size rules."]
CHAPTERS = [(1, "The Universal Law of Nature"), (3, "Introducing Genus Epomis"), (4, "How a Frog Finds Food"), (6, "The Deadly Lure"),
            (9, "The Strike and the Dodge"), (12, "Feeding Like a Parasite"), (15, "Why Would a Beetle Do This"), (16, "The Study That Proved It"),
            (20, "The Adult Emerges"), (23, "The Night Ambush"), (26, "The Poison Problem"), (27, "Lures and Small Hunters"),
            (30, "The Flaw in the Reflex"), (31, "What We Still Do Not Know"), (33, "Dare to Look Closer")]
SOURCES = ["Gil Wizen and Avital Gasith (2011), PLoS ONE 6(9): e25161",
           "Gil Wizen and Avital Gasith (2011), ZooKeys 100: 181-191",
           "Lettvin, Maturana, McCulloch and Pitts (1959), What the Frog's Eye Tells the Frog's Brain",
           "Nyffeler, Maxwell and Remsen (2017), Bird predation by praying mantises, The Wilson Journal of Ornithology",
           "National Geographic, reports on Epomis beetles and on giant water bugs (2019 review by Shin-ya Ohba)",
           "Noel et al. (2017), frog tongue and saliva, Journal of the Royal Society Interface"]
HASHTAGS = "#MiyasLab #Epomis #Frogs #Beetles #Science"
BG = dict(pond='night', larva='paper', genus='paper', frogeye='night', worm='paper', lure='night', approach='night', strike='night',
          dodge='dusk', hooks='paper', feed='dusk', bones='paper', stages='dusk', evolve='dusk', lab='paper', labnote='paper', adult='dusk',
          diet='paper', shelter='night', ambush='night', bite='night', spine='paper', poison='dusk', tricksters='night',
          smallhunters='dusk', reflex='paper', map='paper', ending='night', experiment='paper', waterbug='dusk', question='paper')
# Palettes (guideline 3-5, redrawn 2026-10-10): ponds, leaf litter, frogs, beetles -> forest; lab study and toxin chemistry -> lab; deep-sea anglerfish comparison -> ocean
PAL_DEFAULT = 'forest'
PAL = dict(lab='lab', experiment='lab', labnote='lab', poison='lab', tricksters='ocean')

# cine sample: no chalkboards
CHALK = {}
