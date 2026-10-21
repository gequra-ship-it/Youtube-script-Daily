# Per-video settings (guideline 3-5, 12, 17, 20-2): chalkboards, metadata text, background mode and palette per art theme.
CHALK = {
 9: dict(title="Where the Neurons Are", sub="Common octopus, rough estimates",
         rows=[("Neurons in total", "~500 million", "common octopus", 'y', "five hundred million"),
               ("Central brain", "~1/3", "around the esophagus", 'c', "one third"),
               ("Eight arms", "~2/3", "local nerve cords", 'y', "two thirds")],
         concl=("The arms do a lot of their own thinking", "own thinking"),
         src="Source: octopus neuroanatomy (commonly cited estimates; the exact split varies)"),
 15: dict(title="Three Layers of Skin", sub="A living display screen",
          rows=[("Upper layer", "Chromatophores", "pigment sacs", 'y', "Chromatophores"),
                ("Middle layer", "Iridophores", "living mirrors", 'c', "Iridophores"),
                ("Deep layer", "Leucophores", "white scatter", 'y', "leucophores")],
          concl=("Together, a living screen", "living screen"),
          src="Source: cephalopod skin biology (general description)"),
 29: dict(title="Editing the Message", sub="RNA recoding in nerve cells",
          rows=[("Squid brain messages", "60%+", "recoded by editing", 'c', "sixty percent"),
                ("Human messages", "<1%", "recoded", 'y', "one percent"),
                ("Role of editing", "Major tool", "for cephalopod nerves", 'y', "major tool")],
          concl=("Cephalopods edit far more than we do", "major tool"),
          src="Source: Liscovitch-Brauer et al., Cell (2017) and its press summary"),
 34: dict(title="Count the Hearts", sub="Blue blood, three pumps",
          rows=[("Gill hearts", "2", "one beside each gill", 'y', "Two gill hearts"),
                ("Systemic heart", "1", "serves the body", 'c', "One systemic heart"),
                ("Total", "3 hearts", "per octopus", 'y', "three hearts")],
          concl=("Three hearts in total", "in total"),
          src="Source: cephalopod circulatory system (general description)"),
 40: dict(title="Lifespans Compared", sub="Short lives, long learning gap",
          rows=[("Small species", "~6 months", "some species", 'y', "six months"),
                ("Giant Pacific", "3-5 years", "usual lifespan", 'c', "three to five years"),
                ("Humans", "Decades", "long childhoods", 'y', "decades")],
          concl=("Very little time to learn", "very little time"),
          src="Source: typical lifespans from cephalopod biology references"),
}
WHOOSH = []
TITLE = "The Alien on Earth: The Bizarre Evolution and Genius of the Octopus"
DESC = ["Could the closest thing to an alien mind be living in our own oceans? The octopus has blue blood, three hearts, and most of its neurons spread through eight arms, and it edits the RNA messages of its own nerve cells.",
        "In this video, we follow the octopus from a worm-like ancestor about six hundred million years ago to its shell-less, flexible body, then look at camouflage, tool use, the Inky escape, RNA editing, mimicry, and the short life that may explain why octopuses never built a culture."]
CHAPTERS = [(1, "An Alien Among Us"), (3, "The Ancient Fork"), (5, "Trading Armor for Freedom"), (7, "A Radical Architecture"), (10, "Eight Thinking Limbs"),
            (13, "Masters of Camouflage"), (18, "The Colorblind Paradox"), (21, "Tools and Planning"), (24, "Great Escapes"), (26, "Faces and Play"),
            (28, "Editing the Message"), (32, "Blue Blood, Three Hearts"), (36, "The Mimic Octopus"), (38, "The Short-Life Question"),
            (44, "No Culture to Share"), (46, "Intelligence Evolved Twice")]
SOURCES = ["Godfrey-Smith, P. (2016). Other Minds: The Octopus, the Sea, and the Deep Origins of Consciousness",
           "Finn, Tregenza & Norman (2009). Defensive tool use in a coconut-carrying octopus. Current Biology",
           "Norman, Finn & Tregenza (2001). Dynamic mimicry in an Indo-Malayan octopus. Proc. R. Soc. B",
           "Liscovitch-Brauer et al. (2017). Trade-off between transcriptome plasticity and genome evolution in cephalopods. Cell",
           "Garrett & Rosenthal (2012). RNA editing underlies temperature adaptation in K+ channels from polar octopuses. Science",
           "Stubbs & Stubbs (2016). Spectral discrimination in color blind animals via chromatic aberration and pupil shape. PNAS (hypothesis)",
           "Ramirez & Oakley (2015). Eye-independent, light-activated chromatophore expansion in Octopus bimaculoides. J. Exp. Biol.",
           "Anderson et al. (2010). Octopuses (Enteroctopus dofleini) recognize individual humans. J. Appl. Anim. Welf. Sci.",
           "Wodinsky (1977). Hormonal inhibition of feeding and death in octopus: control by optic gland secretion. Science",
           "National Aquarium of New Zealand: Inky's escape (2016)"]
HASHTAGS = "#MiyasLab #Octopus #MarineBiology #Evolution #Intelligence"
BG = dict(alien='night', gaze='night', fork='paper', shells='paper', armor='dusk', squeeze='night', neurons='night', arms='dusk', chalk1='paper',
          severed='night', suckers='paper', manager='dusk', camo='night', skinlayers='paper', chalk2='paper', pixels='night', papillae='dusk',
          eye='paper', pupil='night', skinlight='dusk', coconut='dusk', plan='paper', jar='paper', escape='night', lamp='dusk', faces='paper',
          play='dusk', rna='night', chalk3='paper', cold='night', genome='night', blood='dusk', hearts='night', chalk4='paper', swim='night',
          mimic='dusk', seasnake='night', question1='paper', sand='dusk', chalk5='paper', mother='night', hatch='dusk', gland='night',
          orphan='paper', whatif='dusk', tree='paper', gaze2='night', stars='night', reef='dusk', montage='night', cta='dusk')
PAL_DEFAULT = 'ocean'
PAL = dict(neurons='lab', arms='lab', chalk1='lab', severed='lab', manager='lab', skinlayers='body', chalk2='body', pixels='lab', pupil='lab', eye='lab',
           skinlight='lab', rna='lab', chalk3='lab', cold='ice', genome='lab', blood='body', hearts='body', chalk4='body', swim='body',
           coconut='desert', plan='desert', jar='lab', faces='body', play='body', lamp='lab', escape='storm', question1='history', sand='history',
           chalk5='history', mother='body', hatch='body', gland='lab', orphan='ocean', whatif='sunset', tree='forest', stars='space', cta='sunset',
           gaze2='space', montage='deepfield')
HOOK = dict(until=300, maxu=5.5)   # guideline 20-2
