# Shorts thumbnail A for deep-time-bedtime-short3 (guideline 16-9, brief tools/briefs/thumb_art.md). Run: python3 videos/deep-time-bedtime-short3/thumb/make.py
# text   LEAVING / THE WATER
# picture intuitive: Tiktaalik props itself on wrist-like fins and lifts its head out of a Devonian shallow; frog waves from the mud bank.
# source short3: "creatures like Tiktaalik evolved sturdy fins with wrist-like bones ... lift their heads out of the water" / "Life was about to leave the water."
# Drawing code: videos/deep-time-bedtime/thumb/shorts_kit.py (short3). No hands drawn (frog arms only).
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../deep-time-bedtime/thumb'))
import shorts_kit
shorts_kit.build(3, HERE)
print('ok')
