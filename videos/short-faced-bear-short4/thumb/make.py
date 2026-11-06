# Shorts thumbnail A for short-faced-bear-short4 (guideline 16-9). Drawing code: videos/short-faced-bear-short1/thumb/sfb_shorts.py
# Run: python3 videos/short-faced-bear-short4/thumb/make.py  then  SLUG=short-faced-bear-short4 python3 tools/thumb_shot.py
import os, importlib.util
p = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'short-faced-bear-short1', 'thumb', 'sfb_shorts.py')
s = importlib.util.spec_from_file_location('sfb_shorts', p); m = importlib.util.module_from_spec(s); s.loader.exec_module(m)
m.build(4)
