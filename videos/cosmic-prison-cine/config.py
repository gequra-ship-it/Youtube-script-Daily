# Per-video settings (cosmic mode, guideline 3-7): chalkboards, metadata text, background mode and palette per art theme.
STYLE = 'cosmic'
CHALK = {
 7: dict(title="How Big Is Our Neighborhood?", sub="Three steps out from home",
         rows=[("Milky Way", "100 billion+ stars", "our home galaxy", 'y', "Our home galaxy"),
               ("Local Group", "10 million ly", "across", 'y', "Local Group"),
               ("Laniakea", "520 million ly", "~100,000 galaxies", 'c', "Laniakea")],
         concl=("And this is still a tiny corner", "stretched across"),
         src="Source: Tully et al. (2014), Nature · Wikipedia, Local Group"),
 13: dict(title="Hubble's Law in Numbers", sub="Recession speed grows with distance",
          rows=[("1 megaparsec", "+70 km/s", "3.26 million light-years", 'y', "For every megaparsec"),
                ("2 megaparsecs", "140 km/s", "twice as far", 'y', "two megaparsecs"),
                ("10 megaparsecs", "700 km/s", "ten times as far", 'c', "ten megaparsecs")],
          concl=("Farther away, faster away", "700 kilometers"),
          src="Source: Hubble (1929) · Planck Collaboration (2018)"),
 22: dict(title="The Observable Universe", sub="What light has had time to show us",
          rows=[("Observable universe", "93 billion ly", "across, centered on us", 'y', "The observable universe is a sphere"),
                ("Since the Big Bang", "13.8 billion yrs", "time for light to travel", 'y', "13.8 billion"),
                ("Beyond the bubble", "unknown size", "may be infinite", 'c', "unobservable universe")],
          concl=("We only see a bubble", "may even be infinite"),
          src="Source: Planck Collaboration (2018) · Davis & Lineweaver (2004)"),
}
WHOOSH = []
TITLE = "The Cosmic Prison: Why We Can Never Reach the Edge of the Universe"
DESC = ["Why can't we ever reach the edge of the universe? Space itself is expanding, and beyond about 16 billion light-years lies the cosmic event horizon. By one estimate, about 94 percent of the galaxies in the observable universe are already out of reach.",
        "In this video, we go from Voyager 1 and the speed of light to Hubble's discovery, Hubble's law, the cosmic event horizon, dark energy, the observable universe, the Local Group and Andromeda, wormholes and warp drives, the shape of space, the Boötes Void, and the far future of the cosmos."]
CHAPTERS = [(1, "The Endless Frontier"), (2, "Voyager 1"), (4, "The Speed Limit"), (6, "The Scale of the Cosmos"), (9, "Hubble's Discovery"),
            (12, "Hubble's Law"), (15, "Faster Than Light"), (18, "The Cosmic Event Horizon"), (19, "Dark Energy"), (22, "The Observable Universe"),
            (25, "Our Local Group"), (28, "The Long Freeze"), (30, "Wormholes and Warp Drives"), (35, "Where Is the Edge?"), (39, "The Boötes Void"),
            (41, "Entropy and the Far Future"), (45, "The Golden Window"), (51, "The Cosmos Within")]
SOURCES = ["Hubble (1929), A relation between distance and radial velocity among extra-galactic nebulae, PNAS",
           "Riess et al. (1998), Astronomical Journal; Perlmutter et al. (1999), Astrophysical Journal (accelerating expansion)",
           "Planck Collaboration (2018), Planck 2018 results VI. Cosmological parameters",
           "Davis & Lineweaver (2004), Expanding confusion: common misconceptions of cosmological horizons, PASA",
           "Tully et al. (2014), The Laniakea supercluster of galaxies, Nature",
           "Sawala et al. (2025), No certainty of a Milky Way-Andromeda collision, Nature Astronomy",
           "Krauss & Scherrer (2007), The return of a static universe and the end of cosmology",
           "Alcubierre (1994), The warp drive: hyper-fast travel within general relativity; McMonigal, Lewis & O'Byrne (2012), Physical Review D",
           "Hawking (1992), Chronology protection conjecture, Physical Review D",
           "Adams & Laughlin (1997), A dying universe, Reviews of Modern Physics",
           "Ethan Siegel, Big Think: how much of the universe is reachable"]
HASHTAGS = "#MiyasLab #Space #Cosmology #Astronomy #DarkEnergy"
BG = dict(nightsky='dusk', voyager='night', proxima='night', lightspeed='night', energy='night', cosmicweb='night', speck='night',
          hubble='night', redshift='night', fabric='night', hubblelaw='night', abyss='night', threshold='night', loophole='night',
          treadmill='paper', eventhorizon='night', supernova='night', darkenergy='night', vanishing='night', seenotvisit='night',
          lost='night', localgroup='night', andromeda='night', trueedge='night', freeze='night', erasure='night', wormhole='night',
          quantum='night', warp='night', snowplow='night', trapped='night', teleport='night', ant='paper', flat='night',
          phantom='night', bootes='night', shoreline='night', entropy='night', dimstars='night', blackholes='night',
          heatdeath='night', awakening='night', window='night', privilege='night', guardians='paper', boundary='night',
          home='night', mystery='night', within='night', clearnight='dusk', ending='night')
# Palettes (3-5, 3-7): cosmic scale / horizons -> deepfield; galaxies, nebulae, dark energy -> nebula; stars, supernovae, energy, blasts -> solar
PAL_DEFAULT = 'deepfield'
PAL = dict(cosmicweb='nebula', speck='nebula', darkenergy='nebula', vanishing='nebula', localgroup='nebula', andromeda='nebula',
           window='nebula', privilege='nebula', mystery='nebula', home='nebula',
           voyager='solar', energy='solar', supernova='solar', snowplow='solar', entropy='solar', dimstars='solar', within='solar')

# cine sample: no chalkboards
CHALK = {}
