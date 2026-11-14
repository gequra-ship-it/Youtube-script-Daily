# usage: python3 tools/check/used_check.py <slug> [pasted.txt]      one video
#        python3 tools/check/used_check.py --all                    every videos/<slug> (on main: every slug that has a used file)
# 2026-11-11 (miya): the used/ copy must be the ORIGINAL script miya pasted, unchanged. Prints WARN lines, always exit 0 (never blocks a render).
#   - MISSING : no scripts/<daily|owl|igwahyung>/used/<slug>__*.txt on main
#   - EXTRA   : more than one file for the slug (a revised copy next to the original)
#   - DIFFERS : with a pasted.txt (the chat message body saved to a file) the used file is not identical (whitespace-insensitive)
# Looks at the working tree when scripts/*/used exists, otherwise at origin/main (render-pipeline has no scripts/). 2026-11-14: folders renamed from scripts, scripts_owl, scripts_igwahyung.
import os as _o, sys as _s; _T = _o.path.dirname(_o.path.dirname(_o.path.abspath(__file__))); _s.path[:0] = [_T] + [_T + '/' + _d for _d in ('build', 'check', 'fix', 'preview', 'writing')]   # tools root (libraries) + sibling folders, 2026-11-14 layout
import os, re, sys, subprocess, unicodedata
R = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
def norm(t):
    t = unicodedata.normalize('NFKC', t).replace('’', "'").replace('‘', "'").replace('“', '"').replace('”', '"')
    return re.sub(r'\s+', ' ', t).strip().lower()
def git(*a): return subprocess.run(['git', '-C', R, *a], capture_output=True, text=True)
DIRS = ('scripts/daily', 'scripts/owl', 'scripts/igwahyung')
def used_files():
    out = {}
    if any(os.path.isdir(f'{R}/{d}/used') for d in DIRS):
        for d in DIRS:
            p = f'{R}/{d}/used'
            for f in (os.listdir(p) if os.path.isdir(p) else []):
                if '__' in f: out.setdefault(f.split('__')[0], []).append(('fs', f'{p}/{f}'))
    else:
        r = git('ls-tree', '-r', '--name-only', 'origin/main')
        if r.returncode:
            print('WARN used_check: cannot read origin/main (git fetch origin main)'); return out
        for l in r.stdout.splitlines():
            l = l.strip('"')
            m = re.match(r'(scripts/(?:daily|owl|igwahyung))/used/([^/]+)__', l)
            if m: out.setdefault(m.group(2), []).append(('git', l))
    return out
def read(src):
    k, p = src
    return open(p, encoding='utf-8').read() if k == 'fs' else git('show', f'origin/main:{p}').stdout
def check(slug, used, paste=None):
    fl = used.get(slug, [])
    if not fl: print(f'WARN used_check {slug}: MISSING scripts/<daily|owl|igwahyung>/used/{slug}__*.txt (move the original pasted script, unchanged)'); return 1
    bad = 0
    if len(fl) > 1: print(f'WARN used_check {slug}: EXTRA {len(fl)} files {[os.path.basename(p) for _, p in fl]} (keep only the original)'); bad = 1
    if paste is not None:
        if not any(norm(read(s)) == norm(paste) for s in fl): print(f'WARN used_check {slug}: DIFFERS from the pasted text (used/ must be the unchanged original)'); bad = 1
    if not bad: print(f'used_check {slug}: OK ({os.path.basename(fl[0][1])})')
    return bad
if __name__ == '__main__':
    a = sys.argv[1:]; used = used_files()
    if a and a[0] == '--all':
        vd = f'{R}/videos'
        slugs = sorted(d for d in os.listdir(vd) if os.path.isdir(f'{vd}/{d}') and not re.search(r'-short\d$', d)) if os.path.isdir(vd) else sorted(used)
        n = sum(check(s, used) for s in slugs); print(f'used_check: {n} problem(s) in {len(slugs)} videos')
    elif a:
        slug = a[0]; paste = open(a[1], encoding='utf-8').read() if len(a) > 1 else None; check(slug, used, paste)
    else: print(__doc__)
