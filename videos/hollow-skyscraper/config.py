# hollow-skyscraper (Miya's Note)
WHOOSH = []
TITLE = 'Why the Hollow Burj Khalifa Never Collapses'
DESC = ['How can a tower that is mostly air stand 828 meters tall? Burj Khalifa rests on piles and a thick raft, with a concrete spine, three buttressing wings and a shape built to confuse the wind.']
HASHTAGS = '#MiyasNote #BurjKhalifa #Engineering #Skyscraper'
SOURCES = ['Skyscraper Museum, Burj Khalifa exhibit (buttressed core, wind tunnel, concrete to level 156, steel spire)', 'Khaleej Times interview with Bill Baker, SOM chief structural engineer (core, buttresses, wind, 50 mm settlement)', 'McCormick School of Engineering, Northwestern University, on Bill Baker (first design failed wind tests, 828 m)', 'Burj Khalifa fact sheet and Wikipedia (828 m, foundation volume and weight, piles, 606 m concrete pumping record)', 'CPP Wind Engineering, full-scale monitoring of Burj Khalifa; Abdelrazaq, SMAR 2011 (sensors, settlement and strain monitoring)']
CHAPTERS = [(1, 'The Needle of Dubai'), (3, 'Paper, Bones and Bamboo'), (5, 'Two Enemies'), (8, 'Rock Beneath the Sand'), (12, 'A Snowshoe of Concrete'), (17, 'The Spine'), (22, 'Three Wings'), (26, 'Ski Poles'), (30, 'The Wind Monster'), (35, 'Confusing the Wind'), (42, 'The Tower Sways'), (45, 'Glass and Sensors'), (47, 'Emptiness as Strength')]
PAL_DEFAULT = 'desert'
PAL = dict()
HOOK = dict(until=300, maxu=4.8)
CHALK = {14: {'concl': ('A giant snowshoe', 'spread out the load'),
      'rows': [('Raft thickness', '3.7 m', 'about 12 feet', 'y', 'thick'),
               ('Concrete', '45,000+ m³', 'foundation', 'y', 'cubic meters'),
               ('Weight', '110,000+ tonnes', 'of that concrete', 'c', 'tonnes')],
      'src': 'Source: Burj Khalifa fact sheet; geotechnical summaries',
      'sub': 'What lies under the tower',
      'title': 'The Foundation'},
 40: {'concl': ('Tuned in a tunnel', 'against the wind'),
      'rows': [('First design', 'about 518 m', 'reported', 'y', 'original'),
               ('Final height', '828 m', 'Burj Khalifa', 'y', 'Refining'),
               ('Gained', 'about 310 m', 'taller', 'c', 'taller')],
      'src': 'Source: Khaleej Times; Northwestern University (reported)',
      'sub': 'Reshaping against the wind',
      'title': 'Wind Made It Taller'}}
