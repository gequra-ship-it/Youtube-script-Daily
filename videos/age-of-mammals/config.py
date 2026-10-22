# Per-video settings: chalkboards, metadata text, background mode per art theme.
CHALK = {
 10: dict(title="The Impact in Numbers", sub="The asteroid that ended the Cretaceous",
          rows=[("Asteroid impact", "66 million", "years ago", 'y', "The asteroid struck"),
                ("Impact site", "Mexico", "a shallow sea", 'c', "It hit the shallow sea"),
                ("Species lost", "About 75%", "three out of four", 'c', "And about three-quarters")],
          concl=("Three out of every four species, gone", "In a single stroke"),
          src="Source: Wikipedia, Cretaceous-Paleogene extinction event"),
 16: dict(title="A Map of Time", sub="The first three epochs of the Cenozoic",
          rows=[("Paleocene", "66 to 56 million", "years ago", 'y', "The Paleocene began"),
                ("Eocene", "56 to 34 million", "years ago", 'c', "The Eocene followed"),
                ("Oligocene", "34 to 23 million", "years ago", 'c', "Then came the Oligocene")],
          concl=("43 million years in only three epochs", "That is forty-three"),
          src="Source: Wikipedia, Geologic time scale"),
 25: dict(title="The Next Three Epochs", sub="From the grasslands to the ice sheets",
          rows=[("Miocene", "23 to 5.3 million", "years ago", 'y', "The Miocene began"),
                ("Pliocene", "5.3 to 2.6 million", "years ago", 'c', "The Pliocene came next"),
                ("Pleistocene", "2.6 million to 11,700", "years ago", 'c', "And the Pleistocene")],
          concl=("The long road from here to us", "That is the long road"),
          src="Source: Wikipedia, Geologic time scale"),
 39: dict(title="The Cost of a Big Brain", sub="What the human brain takes from the body",
          rows=[("Share of body weight", "About 2%", "the brain", 'y', "about two percent"),
                ("Share of resting energy", "About 20%", "burned by the brain", 'c', "twenty percent"),
                ("Nerve cells", "About 86 billion", "in a human brain", 'c', "eighty-six billion")],
          concl=("A small organ with a large appetite", "A small organ"),
          src="Source: Wikipedia, Human brain"),
}
WHOOSH = []
TITLE = "The Age of Mammals: From the Fall of Dinosaurs to Modern Humans"
DESC = ["After an asteroid ended the age of dinosaurs about 66 million years ago, small, furry survivors inherited the Earth. Follow the mammals through the whole Cenozoic era, from the first shrew-like survivors to the people reading this now.",
        "In this video, we watch an asteroid change the world, see mammals diversify into whales, bats and primates, follow cooling climates and spreading grasslands that reshaped teeth, hooves and hunters, and trace how walking upright, stone tools, a hungry brain, fire, farming and writing led to us."]
CHAPTERS = [(1, "The Warmth in Your Hand"), (3, "The Cretaceous Forest"), (7, "The Asteroid Strikes"), (11, "Survivors in the Ash"),
            (13, "Mammals Take Over"), (17, "The Greenhouse World"), (20, "From Land to Sea"), (22, "The World Cools Down"),
            (26, "The Rise of Grass"), (31, "Continents Collide"), (33, "The Rift Valley"), (36, "First Steps Upright"),
            (40, "The Great Ice Age"), (46, "Farms and Cities"), (49, "The Cenozoic Story")]
SOURCES = []
HASHTAGS = "#MiyasLab #Cenozoic #MammalEvolution #Paleontology #DeepTime"
BG = dict(palm='paper', newlife='dusk', cretforest='dusk', oldmammals='paper', shrews='night', warmblood='night', asteroid='night',
          crater='paper', darkness='night', ash='dusk', birds='dusk', emptystage='paper', branchout='paper', milk='night',
          greenhouse='dusk', primates='paper', bats='night', wading='dusk', walkwhale='night', antarctica='night', drying='paper',
          giant='dusk', grass='paper', silica='night', teeth='paper', hooves='dusk', predators='night', collide='paper',
          panama='dusk', rift='dusk', upright='paper', freehands='night', hominins='dusk', lucy='paper', marrow='night',
          icesheet='night', megafauna='paper', fire='night', hearth='night', sapiens='dusk', cavepaint='night', iceretreat='dusk',
          villages='paper', tablets='paper', stepout='dusk', fivefingers='paper', legacy='night', campfire='night')
# Palettes (guideline 3-5): living things and forests -> forest; impact/dark -> storm; ice ages -> ice; savanna and early humans -> desert;
# fossils/dates/writing/villages -> history; mammal biology -> body; lab-like facts -> lab
PAL_DEFAULT = 'forest'
PAL = dict(asteroid='storm', crater='storm', darkness='storm', ash='storm', palm='body', warmblood='body', milk='body', shrews='body',
           antarctica='ice', icesheet='ice', megafauna='ice', iceretreat='ice',
           grass='desert', hooves='desert', predators='desert', rift='desert', upright='desert', freehands='desert', hominins='desert',
           lucy='desert', marrow='desert', fire='desert', hearth='desert', collide='history', panama='history', cavepaint='history',
           villages='history', tablets='history', oldmammals='history', teeth='lab', silica='lab', sapiens='history')
