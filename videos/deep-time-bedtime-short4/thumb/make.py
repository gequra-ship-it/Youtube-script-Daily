# Shorts thumbnail A for deep-time-bedtime-short4 (guideline 16-9, brief tools/briefs/thumb_art.md). Run: python3 videos/deep-time-bedtime-short4/thumb/make.py
# text   THIS COAL / WAS A / TREE
# picture intuitive: a lump of coal with a glowing bark/fern imprint; the ghost of a Carboniferous scale tree and a giant dragonfly rise from it; frog in a scarf.
# source short4: "the lump of coal burning in a winter furnace was once a living tree in a swamp like that"
# Drawing code: videos/deep-time-bedtime/thumb/shorts_kit.py (short4). No hands drawn (frog arms only).
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../deep-time-bedtime/thumb'))
import shorts_kit
shorts_kit.build(4, HERE)
print('ok')
