# Per-video settings (cosmic mode, guideline 3-7): chalkboards, metadata text, background mode and palette per art theme.
STYLE = 'cosmic'
CHALK = {
 8: dict(title="Orbit Speeds", sub="In a solar system, farther out means slower",
         rows=[("Sun around the Milky Way", "200+ km/s", "one lap takes 200+ million years", 'y', "Sun"),
               ("Mercury", "47 km/s", "innermost planet", 'y', "Mercury moves"),
               ("Neptune", "5 km/s", "outermost planet", 'c', "Neptune crawls")],
         concl=("Farther out, slower: the rule galaxies broke", "the farther out"),
         src="Source: NASA Planetary Fact Sheet · Milky Way rotation (Bland-Hawthorn & Gerhard 2016)"),
 15: dict(title="Three Clues", sub="Different evidence, different decades, one message",
          rows=[("1933", "Coma Cluster", "galaxies moving too fast", 'y', "1933"),
                ("Around 1970", "Spiral galaxies", "outer stars spin too fast", 'y', "Around 1970"),
                ("2006", "Bullet Cluster", "mass sits apart from the gas", 'c', "2006")],
          concl=("Three clues, one missing ingredient", "one missing ingredient"),
          src="Source: Zwicky (1933) · Rubin & Ford (1970) · Clowe et al. (2006)"),
 33: dict(title="The Cosmic Budget", sub="What the universe is made of",
          rows=[("Ordinary matter", "~5%", "stars, planets, gas", 'y', "five percent"),
                ("Dark matter", "~27%", "invisible mass", 'y', "twenty-seven"),
                ("Dark energy", "~68%", "pushing space apart", 'c', "sixty-eight")],
          concl=("The dark parts add up to roughly 95%", "roughly ninety-five"),
          src="Source: Planck Collaboration (2014), A&A 571, A16"),
}
WHOOSH = []
TITLE = "Why 96 Percent of the Universe Is Completely Invisible"
DESC = ["Everything we have ever seen, from atoms to galaxies, makes up only about five percent of the cosmos. The other ninety-five percent is dark matter and dark energy, and no one has yet seen what either one really is.",
        "In this video, we follow the clues that revealed the hidden universe: galaxies that spin too fast, light bent by invisible mass, the Bullet Cluster, and exploding stars that showed the expansion of space is speeding up. We look at what scientists suspect dark matter and dark energy might be, how they are hunting for them, and what it means that most of reality is still unread."]
CHAPTERS = [(1, 'The Five Percent'), (4, 'Reading the Invisible'), (6, 'How Galaxies Should Spin'), (9, "Vera Rubin's Curves"), (12, 'Why Call It Dark?'), (14, 'The Bullet Cluster'), (18, 'Through Your Living Room'), (21, 'The Underground Hunt'), (24, 'The Baby Picture'), (25, 'A Bigger Surprise'), (29, 'Dark Energy'), (33, 'The Cosmic Budget'), (36, 'Not the First Time'), (39, 'Three Possible Endings'), (41, 'Look Up Tonight')]
SOURCES = ["Zwicky (1933), Die Rotverschiebung von extragalaktischen Nebeln, Helvetica Physica Acta 6, 110",
           "Rubin and Ford (1970), Rotation of the Andromeda Nebula from a Spectroscopic Survey of Emission Regions, The Astrophysical Journal 159, 379",
           "Clowe et al. (2006), A Direct Empirical Proof of the Existence of Dark Matter, The Astrophysical Journal 648, L109",
           "Riess et al. (1998), Observational Evidence from Supernovae for an Accelerating Universe, The Astronomical Journal 116, 1009",
           "Perlmutter et al. (1999), Measurements of Omega and Lambda from 42 High-Redshift Supernovae, The Astrophysical Journal 517, 565",
           "Planck Collaboration (2014), Planck 2013 results. XVI. Cosmological parameters, Astronomy and Astrophysics 571, A16",
           "NASA, Planetary Fact Sheet"]
HASHTAGS = "#MiyasLab #DarkMatter #DarkEnergy #Cosmology #Universe"
BG = {'room': 'dusk', 'atoms': 'night', 'starsfew': 'night', 'detective': 'paper', 'coma': 'night', 'solarsys': 'night', 'swing': 'paper', 'chalk': 'paper', 'rubin': 'night', 'radio': 'night', 'flung': 'night', 'darkword': 'night', 'lensing': 'night', 'bullet': 'night', 'chalk2': 'paper', 'whatisit': 'night', 'weighing': 'night', 'livingroom': 'dusk', 'suspects': 'night', 'knowns': 'night', 'underground': 'night', 'web': 'night', 'headstart': 'night', 'cmb': 'night', 'expansion': 'night', 'supernova': 'night', 'whitedwarf': 'night', 'accelerate': 'night', 'darkenergy': 'night', 'dilute': 'night', 'einstein': 'paper', 'desi': 'night', 'chalk3': 'paper', 'pie': 'night', 'library': 'dusk', 'century': 'night', 'euclid': 'night', 'horizon': 'night', 'fates': 'night', 'stardust': 'dusk', 'outside': 'dusk', 'outro': 'night'}
# Palettes (3-5, 3-7): the dark universe -> deepfield (navy + gold) as the base; the cosmic web and halos -> nebula; supernovae -> solar; atmosphere of explanation scenes -> lab; Earth-side scenes -> space; far future -> deepfield
PAL_DEFAULT = 'deepfield'
PAL = {'room': 'space', 'atoms': 'space', 'starsfew': 'deepfield', 'detective': 'lab', 'coma': 'nebula', 'solarsys': 'space', 'swing': 'lab', 'chalk': 'lab', 'rubin': 'space', 'radio': 'lab', 'flung': 'nebula', 'darkword': 'deepfield', 'lensing': 'deepfield', 'bullet': 'solar', 'chalk2': 'lab', 'whatisit': 'nebula', 'weighing': 'nebula', 'livingroom': 'space', 'suspects': 'lab', 'knowns': 'deepfield', 'underground': 'storm', 'web': 'nebula', 'headstart': 'nebula', 'cmb': 'solar', 'expansion': 'deepfield', 'supernova': 'solar', 'whitedwarf': 'solar', 'accelerate': 'nebula', 'darkenergy': 'deepfield', 'dilute': 'lab', 'einstein': 'history', 'desi': 'lab', 'chalk3': 'lab', 'pie': 'deepfield', 'library': 'history', 'century': 'history', 'euclid': 'deepfield', 'horizon': 'deepfield', 'fates': 'nebula', 'stardust': 'aurora', 'outside': 'space', 'outro': 'nebula'}
