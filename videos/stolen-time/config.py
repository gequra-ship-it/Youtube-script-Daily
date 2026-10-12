# Per-video settings (cosmic mode, guideline 3-7): chalkboards, metadata text, background mode and palette per art theme.
STYLE = 'cosmic'
CHALK = {
 9: dict(title="From Microseconds to Decades", sub="How much slower would time have to run?",
         rows=[("GPS satellites", "45 microseconds", "per day, from gravity alone", 'y', "On Earth"),
               ("The ocean world", "3 hours", "on the surface", 'y', "three hours"),
               ("Meanwhile on Earth", "23 years", "about 1 hour : 67,000 hours", 'c', "astronomical value")],
         concl=("Same physics, a trillion times stronger", "sixty-seven thousand"),
         src="Source: Ashby (2003), Living Reviews in Relativity · Thorne (2014), The Science of Interstellar"),
 16: dict(title="Spinning at the Brink", sub="What the black hole must be",
          rows=[("Mass", "100 million Suns", "so tides stay gentle", 'y', "Kip Thorne"),
                ("Spin", "99.999999999999%", "of the maximum", 'c', "99.999999999999"),
                ("Planet's orbit", "at the ISCO", "right against the horizon", 'y', "innermost stable")],
          concl=("Allowed by physics, almost never found", "technically intact"),
          src="Source: Thorne (2014), The Science of Interstellar · Kerr (1963)"),
 36: dict(title="Real Giants", sub="Supermassive black holes we have measured",
          rows=[("Sagittarius A*", "4 million Suns", "center of the Milky Way", 'y', "Sagittarius A-star"),
                ("M87*", "6.5 billion Suns", "first black hole ever imaged", 'y', "galaxy M87"),
                ("TON 618", "tens of billions", "one of the largest known", 'c', "TON 618")],
          concl=("Giants like this are everywhere", "may drift"),
          src="Source: EHT Collaboration (2019, 2022) · Wikipedia, TON 618"),
}
WHOOSH = []
TITLE = "The Physics of Stolen Time: How 3 Hours Can Equal 23 Years"
DESC = ["Could three hours on an ocean world really equal twenty-three years on Earth? Yes, if the planet orbits a supermassive black hole of 100 million Suns spinning at almost its maximum rate, right at the innermost stable orbit.",
        "In this video, we follow the physics from Newton's absolute time and Einstein's relativity to GPS clocks, Schwarzschild and Kerr black holes, frame-dragging, Kip Thorne's calculation, the giant tidal waves, gravitational redshift, the one-way ticket to the future, and the real supermassive black holes we have found."]
CHAPTERS = [(1, "Time Is Not What You Think"), (2, "Three Hours, Twenty-Three Years"), (4, "Newton's Absolute Time"), (5, "Einstein's Revolution"),
            (7, "Gravitational Time Dilation"), (8, "Proof From GPS"), (10, "Supermassive Black Holes"), (12, "Why a Static Hole Fails"),
            (13, "The Spinning Kerr Black Hole"), (16, "Kip Thorne's Numbers"), (18, "The Colossal Waves"), (22, "Stretched Messages"),
            (26, "What You Would Feel"), (27, "Surviving the Inferno"), (31, "The Human Cost"), (33, "Escape and Reunion"),
            (36, "Real Giants"), (38, "What Is Time?"), (43, "The Triumph of Reason")]
SOURCES = ["Thorne (2014), The Science of Interstellar, W. W. Norton",
           "Kerr (1963), Gravitational field of a spinning mass as an example of algebraically special metrics, Physical Review Letters",
           "Ashby (2003), Relativity in the Global Positioning System, Living Reviews in Relativity",
           "Event Horizon Telescope Collaboration (2019, 2022), First M87 and Sagittarius A* event horizon scale images, ApJL",
           "Wada, Tsukamoto & Kokubo (2019), Planet formation around supermassive black holes in the active galactic nuclei, ApJ (blanets)",
           "Penrose & Floyd (1971), Extraction of rotational energy from a black hole, Nature Physical Science",
           "Bardeen, Press & Teukolsky (1972), Rotating black holes: locally nonrotating frames, energy extraction, and scalar synchrotron radiation, ApJ (ISCO of Kerr holes)"]
HASHTAGS = "#MiyasLab #Space #BlackHole #Relativity #Physics"
BG = dict(wristwatch='paper', oceanworld='night', question='night', newton='paper', einstein='paper', fabric='night', twoclocks='night',
          gps='night', leviathan='night', horizon='night', schwarzschild='night', kerr='night', framedrag='night',
          sizematters='night', orbitspeed='night', wavewall='dusk', bulge='night', walking='dusk', isco='night',
          signal='night', redshift='night', firehose='night', skywhirl='night', heartbeat='night', accretion='night', magnetosphere='night',
          lensing='night', thorne='paper', heartbreak='night', oneway='night', escape='night', airlock='night', caretaker='night',
          blanet='night', river='night', equations='night', outcasts='night', ringcity='night', tworealities='dusk',
          chalkboard='paper', verdict='night', ending='dusk')
# Palettes (3-5, 3-7): black hole / horizons / cosmic scale -> deepfield; the ocean world and its tides -> aurora; accretion disk, radiation, energy -> solar
PAL_DEFAULT = 'deepfield'
PAL = dict(oceanworld='aurora', wavewall='aurora', bulge='aurora', walking='aurora', heartbeat='aurora', tworealities='aurora', blanet='aurora',
           accretion='solar', magnetosphere='solar', lensing='solar', redshift='solar', firehose='solar', escape='solar', ringcity='solar')
