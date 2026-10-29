# axisfix.py -- write / check the catalogue axis of every mv- group (2026-10-29, miya: axes broke when another model drew; agents now just name the thing and run this).
# usage: python3 tools/axisfix.py <slug> [uid..] [--force] [--report] [--svg file..]
#   default   writes a missing data-pivot on every group whose name is in tools/axis_lib.py (the axis is computed from the drawing, not typed by the agent)
#   --force   also rewrites a data-pivot that is more than 12 px from the catalogue axis
#   --report  writes nothing, prints what it would write and every problem
#   --svg     check these files instead of videos/<slug>/art3/U*.svg
# Prints one line per written pivot and per problem (wrong kind for the thing, rotation on a thing without an axis, pivot off the catalogue axis, part touching no body).
# Exit 1 when there are problems. build3 runs the default mode before every build; attachcheck.py prints the same problems; final_check.py refuses the render while any remain.
import os, sys, glob
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from paths import *
import axis_lib
from playwright.sync_api import sync_playwright


def main():
    a = sys.argv[1:]; force = '--force' in a; report = '--report' in a
    svgs = []
    if '--svg' in a: i = a.index('--svg'); svgs = [x for x in a[i + 1:] if not x.startswith('--')]; a = a[:i]
    a = [x for x in a if not x.startswith('--')]
    slug = a[0] if a else os.environ.get('SLUG', ''); uids = a[1:]
    vert = slug.endswith(tuple(f'short{i}' for i in range(1, 10))) or os.environ.get('VERT') == '1'
    W, H = (1080, 1920) if vert else (1920, 1080)
    files = svgs or sorted(glob.glob(f'{vdir(slug)}/art3/U*.svg'))
    if uids: files = [f for f in files if os.path.basename(f)[:-4] in uids]
    nw = nb = 0
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path=chrome(), args=['--no-sandbox']); pg = b.new_page(viewport={'width': W, 'height': H})
        for f in files:
            uid = os.path.basename(f)[:-4]
            if report:
                res = axis_lib.resolve(pg, open(f, encoding='utf-8').read(), W, H); problems = axis_lib.problems_of(res)
                written = [f"{r['id']}: would write data-pivot {r['local']} ({axis_lib.RULE_KO[r['rule']]} of a {r['word']})" for r in res if r['current'] is None and r['pivot'] and axis_lib.needs_pivot(r['kind']) and not r['err'] and not r['kind_bad'] and r['rule'] != 'none']
                problems = [x for x in problems if ': no data-pivot' not in x]
            else: written, problems = axis_lib.apply(pg, f, W, H, force=force)
            for l in written: print(slug, uid, l); nw += 1
            for l in problems: print(slug, uid, 'PROBLEM', l); nb += 1
        b.close()
    print(slug, 'axisfix:', len(files), 'units,', nw, 'pivots written' if not report else 'pivots to write,', nb, 'problems')
    sys.exit(1 if nb else 0)


if __name__ == '__main__': main()
