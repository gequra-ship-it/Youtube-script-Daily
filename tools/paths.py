# Shared paths and scene loader for the Miya's Note pipeline.
import os, importlib.util
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS = REPO + '/tools/assets'
SLUG = os.environ.get('SLUG', '')
WORK = os.environ.get('MIYA_WORK', '/tmp/miya-work')


def vdir(slug=None):
    s = slug or SLUG; d = f'{REPO}/videos/{s}'
    if not os.path.isdir(d) and os.path.isdir(f'{REPO}/cine-test/videos/{s}'):   # 3D (cine) test videos live in cine-test/ (2026-10-16)
        d = f'{REPO}/cine-test/videos/{s}'
    return d


def wdir(slug=None):
    p = f'{WORK}/{slug or SLUG}'; os.makedirs(p, exist_ok=True); return p


def load_scenes(slug=None):
    spec = importlib.util.spec_from_file_location('script', vdir(slug) + '/script.py')
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    sc = list(m.SCENES)
    if has_outro(slug): sc.append(OUTRO_SCENE)
    return sc


# 2026-10-24 (owner): every long form ends with the same outro (fixed narration tools/assets/outro.wav + fixed picture tools/assets/outro.svg).
# Added to the scene list here, so tts/audio_prep/align/build3/gen_text all see it. Shorts never get it; config.py `OUTRO = False` opts out (old rebuilds).
OUTRO_TEXT = "Thanks for watching! Subscribing and liking really help me make these videos. See you in the next one."
OUTRO_SCENE = ('OUTRO', 'Outro', 'ill', 'outro', OUTRO_TEXT)


def has_outro(slug=None):
    import re
    s = slug or SLUG
    if os.environ.get('VERT') == '1' or re.search(r'-short\d+$', s): return False
    try: return getattr(load_config(s), 'OUTRO', True)
    except Exception: return True


def load_config(slug=None):
    spec = importlib.util.spec_from_file_location('config', vdir(slug) + '/config.py')
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    return m


def chrome():
    """Chromium for playwright: $HYPERFRAMES_BROWSER_PATH / $PW_CHROME / $CHROME, else the newest /opt/pw-browsers/chromium-*/ (the version number changes between
    machines: 1194 on the old one, 1243 now), else None = playwright's own default."""
    import glob
    for e in ('HYPERFRAMES_BROWSER_PATH', 'PW_CHROME', 'CHROME'):
        if os.environ.get(e): return os.environ[e]
    c = sorted(glob.glob('/opt/pw-browsers/chromium-*/chrome-linux*/chrome'))
    return c[-1] if c else None
