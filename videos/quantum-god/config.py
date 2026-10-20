# Per-video settings: chalkboards, metadata text, background mode and palette per art theme.
CHALK = {
 13: dict(title="Half-Lives of Decay", sub="Time for half of the atoms to decay",
          rows=[("Radon-222", "3.8 days", "a radioactive gas", 'y', "radon"),
                ("Carbon-14", "5,730 years", "used to date old bones", 'y', "carbon"),
                ("Uranium-238", "4.47 billion years", "about the age of the Earth", 'c', "uranium")],
          concl=("The group is regular, the single atom is not", "individual"),
          src="Source: standard nuclear data tables (rounded)"),
 18: dict(title="Testing Bell's Limit", sub="Each test found the limit broken",
          rows=[("1964", "John Bell", "proposes the test", 'y', "Bell"),
                ("1982", "Alain Aspect", "closes more gaps", 'y', "Aspect"),
                ("2015", "Three groups", "loophole-free tests", 'c', "fifteen")],
          concl=("Nobel Prize in Physics, 2022", "Nobel"),
          src="Source: Bell (1964) · Aspect (1982) · Nobel Prize in Physics 2022"),
}
WHOOSH = []
TITLE = "Does God Exist? The Terrifying Truth of Quantum Mechanics"
DESC = ["Does quantum mechanics say anything about God? We follow the experiments, from the double slit to Bell's test, and ask which old arguments about cause, design, and knowledge they challenge, and which they leave untouched.",
        "In this video, we walk through Laplace's predictable clockwork, Planck's quanta, the Solvay debate, the double-slit experiment, the uncertainty principle, radioactive decay, entanglement and Bell's inequality, decoherence, and the competing interpretations, and we separate what is measured from what is only argued."]
CHAPTERS = [(1, "The Clockwork Universe"), (3, "Three Old Arguments"), (5, "The Battle in Brussels"), (6, "Two Slits"), (8, "Watching Changes the Result"),
            (10, "The Uncertainty Principle"), (12, "A Decay With No Reason"), (14, "Not the Only Reading"), (15, "The Busy Vacuum"), (17, "Spooky Action"),
            (18, "Bell Settles the Debate"), (20, "Decoherence"), (22, "Schrodinger's Cat"), (23, "Many Worlds"), (26, "Seeds of the Galaxies"),
            (28, "Randomness Is Not Freedom"), (30, "Black Holes Evaporate"), (32, "What Physics Cannot Say"), (33, "The Cosmos Looking Back")]
SOURCES = ["Laplace (1814), A Philosophical Essay on Probabilities",
           "Aquinas, Summa Theologica (the Five Ways)",
           "Einstein, Podolsky, Rosen (1935), Can Quantum-Mechanical Description of Physical Reality Be Considered Complete?, Physical Review 47, 777",
           "Bell (1964), On the Einstein Podolsky Rosen Paradox, Physics 1, 195",
           "Schrodinger (1935), Die gegenwaertige Situation in der Quantenmechanik",
           "Everett (1957), Relative State Formulation of Quantum Mechanics, Reviews of Modern Physics 29, 454",
           "Wigner (1961), Remarks on the Mind-Body Question",
           "Tonomura et al. (1989), Demonstration of single-electron buildup of an interference pattern, American Journal of Physics 57, 117",
           "The Nobel Prize in Physics 2022 (Aspect, Clauser, Zeilinger); The Nobel Prize in Physics 2006 (Mather, Smoot)",
           "Hawking (1974), Black hole explosions?, Nature 248, 30"]
HASHTAGS = "#MiyasLab #QuantumMechanics #Physics #DoubleSlit #BellsInequality"
BG = dict(clockwork='night', laplace='paper', arguments='paper', planck='paper', solvay='paper', doubleslit='night', singleelectron='night', detector='night', instrument='paper',
          heisenberg='paper', fog='night', decay='night', interpretations='paper', vacuum='night', bigbang='night', entangled='night', localreal='night', decoherence='night',
          berkeley='paper', cat='dusk', branches='night', wigner='paper', casino='dusk', cmb='night', dna='paper', freewill='dusk', mysticism='dusk', hawking='night',
          heatdeath='night', limits='paper', ending='dusk', chalk='paper')
# Palettes (3-5): physics lab and experiments -> lab; history scenes -> history; cosmic scale -> space; living/body -> body
PAL_DEFAULT = 'lab'
PAL = dict(laplace='history', arguments='history', solvay='history', berkeley='history', limits='history', planck='history', clockwork='space', bigbang='space', cmb='space',
           hawking='space', heatdeath='space', vacuum='space', ending='space', dna='body', freewill='body', casino='storm')
