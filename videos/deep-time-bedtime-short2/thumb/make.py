# Shorts thumbnail A for deep-time-bedtime-short2 (guideline 16-9, VERTICAL 1080x1920, text centred; brief tools/briefs/thumb_art.md). Run: python3 videos/deep-time-bedtime-short2/thumb/make.py
# text   SNOWBALL / EARTH?
# picture intuitive/iconic object: the frozen Earth inside a snow globe, a small glowing volcanic hot spot; shivering frog in earmuffs + scarf.
# source short2: "Scientists call this possibility Snowball Earth ... pockets of liquid water and around volcanic hot spots" (possibility -> question mark)
# Drawing code: videos/deep-time-bedtime/thumb/shorts_kit.py (short2). No hands drawn (frog arms only).
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../deep-time-bedtime/thumb'))
import shorts_kit
shorts_kit.build(2, HERE)
print('ok')
