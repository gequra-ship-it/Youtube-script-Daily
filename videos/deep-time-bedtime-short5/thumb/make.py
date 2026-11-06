# Shorts thumbnail A for deep-time-bedtime-short5 (guideline 16-9, VERTICAL 1080x1920, text centred; brief tools/briefs/thumb_art.md). Run: python3 videos/deep-time-bedtime-short5/thumb/make.py
# text   THE SMALL / SURVIVED
# picture intuitive cut-away: ash sky, burnt stumps and a big three-toed footprint above; below, a warm burrow with a small furry mammal and the frog.
# source short5: "Scientists think small mammals endured by sheltering in burrows ... the mammals crawled out into a wide, empty kingdom"
# Drawing code: videos/deep-time-bedtime/thumb/shorts_kit.py (short5). No hands drawn (frog arms only).
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../deep-time-bedtime/thumb'))
import shorts_kit
shorts_kit.build(5, HERE)
print('ok')
