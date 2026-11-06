# Shorts thumbnail A for deep-time-bedtime-short1 (guideline 16-9, brief tools/briefs/thumb_art.md). Run: python3 videos/deep-time-bedtime-short1/thumb/make.py
# text   BORN FROM / A CRASH?
# picture intuitive: a Mars-sized body slams into the molten young Earth, debris gathers into the Moon; frog astronaut on a drifting rock.
# source short1: "a wandering celestial body roughly the size of Mars collided with our proto-Earth ... coalesced into our Moon" (hedged -> question mark)
# Drawing code: videos/deep-time-bedtime/thumb/shorts_kit.py (short1). No hands drawn (frog arms only).
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../deep-time-bedtime/thumb'))
import shorts_kit
shorts_kit.build(1, HERE)
print('ok')
