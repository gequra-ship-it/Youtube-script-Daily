# Per-video settings (guideline 3-5, 12, 17, 20-2): chalkboards, metadata text, background mode and palette per art theme.
CHALK = {
 9: dict(title="Sacabambaspis by the Numbers", sub="Estimates from the fossils",
         rows=[("Length", "~35 cm", "counting the thin tail", 'y', "thirty-five centimeters"),
               ("Mouth plates", "~60 rows", "tiny bony plates", 'c', "nearly sixty rows"),
               ("Age", "~460 million yrs", "Ordovician Period", 'y', "four hundred and sixty million years")],
         concl=("A small fish with a funny face", "funny face"),
         src="Source: Sacabambaspis descriptions (Gagnier, Blieck & Rodrigo 1986; later studies)"),
 15: dict(title="What It Went Without", sub="Sacabambaspis, the jawless armored fish",
          rows=[("Jaws", "None", "a jawless fish", 'c', "no jaws"),
                ("Paired fins", "None", "no side fins", 'c', "no paired fins"),
                ("Fins in total", "Tail only", "one small tail fin", 'y', "tail fin")],
          concl=("Nothing to steer or hover with", "hover"),
          src="Source: Sacabambaspis anatomy (Gagnier 1989; Pradel et al. 2006)"),
 22: dict(title="A Timeline of Early Fish", sub="Approximate ages",
          rows=[("Haikouichthys", "518 million", "soft body, no armor", 'y', "five hundred and eighteen million years ago"),
                ("Sacabambaspis", "460 million", "armored, no jaw", 'y', "four hundred and sixty million years ago"),
                ("Mass extinction", "444 million", "~85% of marine species lost", 'c', "four hundred and forty-four million years ago")],
          concl=("Armor first, jaws later", "no jaw"),
          src="Source: Chengjiang and Ordovician fossil records (approximate dates)"),
}
WHOOSH = []
TITLE = "The Bizarre Biology of Sacabambaspis, the Meme Fish"
DESC = ["Why does a 460-million-year-old fish look so surprised? Sacabambaspis was a small armored fish with no jaws, no side fins, and eyes at the very front of its head, and a hand-made museum model turned it into an internet star.",
        "In this video, we separate the meme from the fossils: where the fish lived, how its armor and mouth worked, what a mass-death site in Bolivia tells us, how jaws later changed the sea, and why this cousin of ours still matters."]
CHAPTERS = [(1, "The Derpiest Face"), (3, "The Woman Who Made the Face"), (4, "The Ordovician World"), (6, "The Find in the Andes"),
            (8, "A Shell-Skinned Fish"), (11, "Eyes at the Very Front"), (13, "Life Without a Jaw"), (16, "Wriggling Like a Tadpole"),
            (19, "Armor Made of Bone"), (21, "Before the Armor"), (24, "Armored Cousins"), (26, "A Crowd Frozen in Stone"),
            (28, "How Good Is the Model?"), (31, "The Invention of Jaws"), (34, "Ice Over Gondwana"), (36, "A Cousin, Not an Ancestor"),
            (40, "A Meme That Teaches")]
SOURCES = ["Gagnier, Blieck & Rodrigo (1986): original description of Sacabambaspis (Bolivia); anatomy summary in the Wikipedia article Sacabambaspis (consulted 2026-10-22)",
           "Ritchie & Gilbert-Tomlinson (1977): naming of the Arandaspida; summary in the Wikipedia article Arandaspida (consulted 2026-10-22)",
           "Pilcher, H. BBC Science Focus: article on Sacabambaspis and the Helsinki museum model (2026)",
           "Finnish Museum of Natural History, Helsinki: fossil fish exhibit (1995)"]
HASHTAGS = "#MiyasLab #Sacabambaspis #Paleontology #Evolution #AncientLife"
BG = dict(face='night', meme='paper', sculptor='dusk', ordovician='night', invert='dusk', andes='paper', shore='dusk', shellskin='paper',
          chalk1='paper', tank='night', eyes='dusk', eyesoft='paper', nojaw='night', plates='paper', chalk2='paper', tadpole='night',
          heavy='dusk', lateral='night', armor='paper', whyarmor='dusk', cambrian='night', chalk3='paper', outside='dusk', australia='paper',
          cousins='dusk', crowd='night', storm='dusk', crushed='paper', verdict='dusk', golden='night', jaws='paper', placoderm='night',
          coexist='dusk', ice='night', lamprey='dusk', cousin='paper', scan='night', brain='dusk', unknown='paper', whyface='night',
          teach='dusk', bush='paper', gaze='night', more='dusk', cta='paper')
PAL_DEFAULT = 'ocean'
PAL = dict(face='body', meme='lab', sculptor='history', andes='desert', shore='desert', shellskin='history', chalk1='lab', chalk2='lab', chalk3='lab',
           cambrian='forest', storm='storm', crushed='history', verdict='lab', ice='ice', scan='lab', brain='lab', unknown='history',
           teach='sunset', bush='forest', gaze='space', more='sunset', cta='sunset')
HOOK = dict(until=300, maxu=5.5)   # guideline 20-2
