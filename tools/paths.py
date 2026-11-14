# Shared paths and scene loader for the Miya's Note pipeline.
import os, importlib.util
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS = REPO + '/tools/assets'
TOOLS = REPO + '/tools'
TOOL_DIRS = ('build', 'check', 'fix', 'preview', 'writing')   # 2026-11-14: command-line tools live in these folders, importable libraries stay in tools/
SHARED = ['Fredoka-700.woff2', 'PatrickHand-400.woff2', 'logo.png', 'grain.png', 'gsap.min.js', 'anime.min.js', 'gsap']   # same for every video: not committed under render/<slug>/ since 2026-11-14


def tool(name):
    """absolute path of a tool script wherever it lives under tools/ (tool('armfix.py') -> .../tools/fix/armfix.py)"""
    for d in ('',) + TOOL_DIRS:
        p = os.path.join(TOOLS, d, name)
        if os.path.exists(p): return p
    raise FileNotFoundError(name)


def ensure_assets(render_dir):
    """link the shared page assets (fonts, logo, grain, gsap, anime) from tools/assets into a render folder that lacks them (fresh clone, chunk folder)"""
    for n in SHARED:
        p = os.path.join(render_dir, n)
        if not os.path.lexists(p) and os.path.exists(f'{ASSETS}/{n}'): os.symlink(os.path.abspath(f'{ASSETS}/{n}'), p)
SLUG = os.environ.get('SLUG', '')
WORK = os.environ.get('MIYA_WORK', '/tmp/miya-work')


def vdir(slug=None):
    s = slug or SLUG; d = f'{REPO}/videos/{s}'
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
