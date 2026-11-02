# sharpest-blade-fastest-gun
STYLE = 'mystery'
WHOOSH = []
TITLE = "Science's Sharpest Blade and Fastest Gun"
DESC = ['The sharpest blade ends in a single atom, and the fastest gun fires protons at nearly the speed of light. A tour of obsidian, diamond knives, light-gas guns and the Large Hadron Collider.']
HASHTAGS = '#MiyasNote #Science #Physics #LHC'
SOURCES = ['CERN, The Large Hadron Collider (home.cern)', 'NASA Orbital Debris Program Office (orbitaldebris.jsc.nasa.gov)', 'NASA Ames Vertical Gun Range and two-stage light-gas gun facilities (nasa.gov)', 'IBM Research, scanning tunneling microscope and single-atom manipulation (1980s-1990)', 'Obsidian blades in surgery, medical literature (reported edge thickness; hedged in the video)']
CHAPTERS = [(1, 'The Kitchen Knife'), (5, 'What Cutting Really Is'), (7, 'The Steel Limit'), (9, "Nature's Glass"), (12, 'Slicing a Cell'), (18, 'One Atom Tip'), (21, 'A Blade of Energy'), (23, 'The Fastest Gun'), (26, 'The Light-Gas Gun'), (30, 'The Large Hadron Collider'), (37, 'Two Sides of a Coin'), (39, 'From War to Wonder')]
PAL_DEFAULT = 'lab'
PAL = dict()
HOOK = dict(until=999, maxu=4.8)
CHALK = {24: {'concl': ('Too slow for orbit', 'sluggish crawl'),
      'rows': [('Rifle bullet', '800-1,000 m/s', 'typical muzzle speed', 'y', 'eight hundred'),
               ('Feels like', 'blazing fast', 'to our human senses', 'y', 'blazing fast'),
               ('Orbital speed', 'far faster', 'spacecraft debris moves much faster', 'c', 'orbital mechanics')],
      'src': 'Source: ballistics textbooks (typical rifle values)',
      'sub': 'How fast a gunpowder gun can shoot',
      'title': 'The Rifle Bullet'},
 28: {'concl': ('Manhattan in seconds', 'about three seconds'),
      'rows': [('Muzzle speed', '7-8 km/s', 'light-gas gun', 'y', 'seven to eight kilometers per second'),
               ('Per hour', '25,000+ km/h', 'more than', 'y', 'twenty-five thousand kilometers per hour'),
               ('Across Manhattan', 'about 3 s', 'at sea level, in a line', 'c', 'Manhattan')],
      'src': 'Source: NASA Ames hypervelocity impact facilities',
      'sub': 'A projectile at hypervelocity',
      'title': 'The Light-Gas Gun'},
 33: {'concl': ('Nearly light speed', 'in a single second'),
      'rows': [('Speed', '99.9999991% of c', 'speed of light', 'y', 'ninety-nine point nine'),
               ('Ring', '27 km', 'around the tunnel', 'y', 'twenty-seven-kilometer ring'),
               ('Laps', '11,000+ per second', 'one proton', 'c', 'eleven thousand times')],
      'src': 'Source: CERN',
      'sub': 'Almost the speed of light',
      'title': 'Protons at the LHC'}}
