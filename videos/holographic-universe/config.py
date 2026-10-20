# Per-video settings (cosmic mode, guideline 3-7): chalkboards, metadata text, background mode and palette per art theme.
STYLE = 'cosmic'
CHALK = {
 11: dict(title="Counting Information", sub="What limits how much a thing can hold?",
          rows=[("Hard drive", "Grows with volume", "twice the space, twice the data", 'y', "drive"),
                ("Black hole", "Grows with area", "twice the area, twice the entropy", 'c', "area"),
                ("One patch", "Planck length", "far smaller than a proton", 'y', "Planck")],
          concl=("The surface counts, not the volume", "proton"),
          src="Source: Bekenstein (1973) · Hawking (1975)"),
 21: dict(title="The Road to Holography", sub="Three steps from a puzzle to a new idea",
          rows=[("1973", "Bekenstein", "entropy tracks horizon area", 'y', "Bekenstein"),
                ("1993", "'t Hooft", "gravity described on a boundary", 'y', "Hooft"),
                ("1997", "Maldacena", "a precise example", 'c', "Maldacena")],
          concl=("From a cup of tea to a new view of space", "tea"),
          src="Source: Bekenstein (1973) · 't Hooft (1993) · Maldacena (1997)"),
}
WHOOSH = []
TITLE = "Is Our Entire Universe Just a Hologram?"
DESC = ["Could our three-dimensional world be described by information on a distant two-dimensional surface? This is the holographic principle, an idea born from black holes. No one has proven that our universe works this way, and this video separates what is established from what is still a hypothesis.",
        "In this video, we follow the story from the hologram on a credit card to black hole entropy, Hawking radiation, the information paradox, 't Hooft and Susskind, Maldacena's holographic duality, entanglement and space, the Page curve, and the experiments that tried to test it."]
CHAPTERS = [(1, "Look at Your Hands"), (3, "The Card in Your Wallet"), (6, "The Point of No Return"), (8, "The Cup of Tea Problem"), (10, "Black Holes Are Not Black"),
            (13, "The Information Paradox"), (15, "The Holographic Principle"), (17, "Maldacena's Duality"), (19, "Not Proven for Our Universe"),
            (22, "A Tool That Works"), (23, "Entanglement and Space"), (26, "Solving the Paradox"), (27, "Can We Test It?"),
            (31, "What We Know"), (33, "The Quiet Space Around You")]
SOURCES = ["Gabor (1948), A new microscopic principle, Nature 161, 777; The Nobel Prize in Physics 1971",
           "Bekenstein (1973), Black Holes and Entropy, Physical Review D 7, 2333",
           "Hawking (1974), Black hole explosions?, Nature 248, 30; Hawking (1975), Particle creation by black holes, Communications in Mathematical Physics 43, 199",
           "Hawking (1976), Breakdown of predictability in gravitational collapse, Physical Review D 14, 2460",
           "Preskill (2004), On Hawking's Concession (Caltech)",
           "'t Hooft (1993), Dimensional Reduction in Quantum Gravity, arXiv:gr-qc/9310026",
           "Susskind (1995), The World as a Hologram, Journal of Mathematical Physics 36, 6377",
           "Bousso (1999), A covariant entropy conjecture, Journal of High Energy Physics 07, 004",
           "Maldacena (1998), The Large N Limit of Superconformal Field Theories and Supergravity, Advances in Theoretical and Mathematical Physics 2, 231",
           "Gibbons and Hawking (1977), Cosmological event horizons, thermodynamics, and particle creation, Physical Review D 15, 2738",
           "Ryu and Takayanagi (2006), Holographic Derivation of Entanglement Entropy from AdS/CFT, Physical Review Letters 96, 181602",
           "Van Raamsdonk (2010), Building up spacetime with quantum entanglement, General Relativity and Gravitation 42, 2323",
           "Page (1993), Information in black hole radiation, Physical Review Letters 71, 3743; Penington (2019), arXiv:1905.08255; Almheiri, Engelhardt, Marolf and Maxfield (2019), Journal of High Energy Physics 12, 063",
           "Isi, Farr, Giesler, Scheel and Teukolsky (2021), Testing the Black-Hole Area Law with GW150914, Physical Review Letters 127, 011103",
           "Fermilab (2015), Holometer rules out first theory of space-time correlations"]
HASHTAGS = "#MiyasLab #HolographicPrinciple #BlackHoles #Physics #Universe"
BG = dict(hands='paper', welcome='night', card='paper', recording='night', boldclaim='night', horizon='night', shadow='night', tea='dusk', merge='night',
          glow='night', chalk='paper', skin='night', paradox='night', bet='dusk', twominds='dusk', collapse='night', maldacena='night', dictionary='night',
          conjecture='night', cosmichorizon='night', plasma='night', entangle='night', emerge='night', temperature='paper', pagecurve='night', holometer='night',
          quantumlab='night', notsim='night', itfrombit='night', tally='night', open='night', room='dusk', outro='dusk')
# Palettes (3-5, 3-7): black holes, horizons, cosmic scale -> deepfield; entanglement, emergence -> nebula; hot plasma -> solar; lab and hologram scenes -> lab; history scenes -> history
PAL_DEFAULT = 'deepfield'
PAL = dict(hands='lab', card='lab', recording='lab', tea='lab', temperature='lab', holometer='lab', quantumlab='lab',
           bet='history', twominds='history', entangle='nebula', emerge='nebula', itfrombit='nebula', plasma='solar', glow='solar',
           welcome='lab', room='aurora', outro='aurora')
