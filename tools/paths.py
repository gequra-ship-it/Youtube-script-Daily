# Shared paths and scene loader for the Miya's Lab pipeline.
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
    return m.SCENES


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
