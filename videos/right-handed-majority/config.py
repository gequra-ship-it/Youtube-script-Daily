# Per-video settings.
CHALK = {20: {'concl': ('Same DNA, different hands', 'discordant'),
      'rows': [('Identical twin pairs', '1 in 5', 'have different hands', 'y', 'one in five'),
               ('Shared DNA', 'identical', 'so DNA is not the whole story', 'c', 'identical handedness'),
               ('Simple gene rule', 'would give 0', 'pairs with different hands', 'y', 'dominant and recessive')],
      'src': 'Source: twin studies (summary)',
      'sub': 'Twins and handedness',
      'title': 'Identical Twins'},
 26: {'concl': ('Handedness starts early', 'overwhelming'),
      'rows': [('Week 10', 'one arm', 'moves more often', 'y', 'tenth week'),
               ('Week 15', '90%', 'suck the right thumb', 'y', 'ninety percent'),
               ('Unborn babies', 'already', 'show a hand preference', 'c', 'sucking')],
      'src': 'Source: fetal ultrasound studies (summary)',
      'sub': 'Before birth',
      'title': 'The Womb'},
 49: {'concl': ('A pattern, not proof', 'homicide rates'),
      'rows': [('Peaceful societies', '~3%', 'left-handed', 'y', 'three percent'),
               ('Warlike societies', '~27%', 'left-handed men', 'c', 'twenty-seven percent'),
               ('Link', 'violence', 'goes with more lefties', 'y', 'proportion')],
      'src': 'Source: Faurie & Raymond (2005)',
      'sub': 'Left-handers across societies',
      'title': 'Handedness and Violence'}}
WHOOSH = []
TITLE = "Why Most of Us Use the Right Hand"
DESC = ["About nine in ten people use the right hand, and left-handedness never disappeared. Caves, genes, the womb, the brain and an old fighting hypothesis help explain why."]
CHAPTERS = [(1, 'Nine Out of Ten'), (5, 'Handprints in Caves'), (8, 'Half a Million Years'), (11, 'The Sinister Hand'), (14, 'Forced to Switch'), (16, 'Is There a Gene?'), (25, 'Decided in the Womb'), (28, 'Brain and Language'), (34, 'What About Chimps?'), (37, 'The Power of Cooperation'), (42, 'The Fighting Hypothesis'), (51, 'Fists and Foils'), (56, 'A Spectrum'), (59, 'Why Not Fifty-Fifty?'), (63, 'The Living Legacy')]
SOURCES = ["Faurie & Raymond (2004), Handedness frequency over more than ten thousand years, Proceedings of the Royal Society B",
 "Lozano et al. (2009), Right handedness of Homo heidelbergensis from Sima de los Huesos (Atapuerca, Spain) 500,000 years ago, Evolution and Human Behavior",
 "Wiberg et al. (2019), Handedness, language areas and neuropsychiatric diseases: insights from brain imaging and genetics, Brain (UK Biobank)",
 "Hepper et al. (2005), Handedness in the human fetus, Neuropsychologia",
 "Ocklenburg et al. (2017), Epigenetic regulation of lateralized fetal spinal gene expression underlies hemispheric asymmetries, eLife",
 "Lonsdorf & Hopkins (2005), Wild chimpanzees show population-level handedness for tool use, PNAS; Sanz, Morgan & Hopkins (2016), American Journal of Primatology",
 "Abrams & Panaggio (2012), A model balancing cooperation and competition can explain our right-handed world and the dominance of left-handed athletes, Journal of the Royal Society Interface",
 "Faurie & Raymond (2005), Handedness, homicide and negative frequency-dependent selection, Proceedings of the Royal Society B"]
HASHTAGS = "#MiyasNote #Handedness #LeftHanded #Evolution #Brain"
PAL_DEFAULT = 'history'
PAL = dict()
HOOK = dict(until=300, maxu=4.5)
