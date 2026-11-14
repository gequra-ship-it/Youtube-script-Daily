# usage: python3 tools/fix/corefix.py <slug>... [--report]
# 2026-11-05 (miya: "빠르게 두근거리는 모션이 너무 자주 나오고 개구리가 붙어서 같이 두근거린다"). The pulse family of centre motions (mv-core-heartbeat / swell /
# tremble / ping / wobble / squeeze / pop / stamp / drop) is an EVENT: it stays only when the unit's sentence or the object's name says so (motions.CORE_WORDS /
# CORE_NAMES) and while it is under 15 % of the video's units; otherwise the group id is rewritten to the least-used calm kind (glide / sway / approach / orbit,
# flicker for lights) — the same deterministic choice for every model and every run (motions.core_fit, unit order). A heartbeat whose sentence says pound / panic /
# racing gets data-strong="1" (the hard beat); every other heartbeat is the calm 1.6 s beat. data-keep="1" groups are never changed. Idempotent.
# build3 and frog_place run it first; --report only prints. Guideline 4-1 (2026-11-05), 7-2 L.
import os as _o, sys as _s; _T = _o.path.dirname(_o.path.dirname(_o.path.abspath(__file__))); _s.path[:0] = [_T] + [_T + '/' + _d for _d in ('build', 'check', 'fix', 'preview', 'writing')]   # tools root (libraries) + sibling folders, 2026-11-14 layout
import os, re, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from paths import REPO
import motions
GID = re.compile(r'(<g\b[^>]*\bid=")mv-core-([a-z]+)(-[A-Za-z0-9-]*)?("[^>]*>)')


def fix(slug, report=False):
    pj = f'{REPO}/videos/{slug}/plan.json'
    if not os.path.exists(pj): return 0, 0
    plan = json.load(open(pj)); units = [u for u in plan if u.get('kind') != 'chalk']; tally = {}; changed = 0; strong = 0
    for u in units:
        fn = f'{REPO}/videos/{slug}/art3/{u["uid"]}.svg'
        if not os.path.exists(fn): continue
        txt = open(fn, encoding='utf-8').read(); out = txt; seen = {}
        for m in GID.finditer(txt):
            head, ct, name, tail = m.group(1), m.group(2), m.group(3) or '', m.group(4); gid = f'mv-core-{ct}{name}'
            if gid in seen: continue   # several groups with one id: the first decides for all (same kind)
            keep = 'data-keep="1"' in m.group(0)
            ct2, why = motions.core_fit(ct, gid, u['text'], tally, keep=keep, nunits=len(units)); seen[gid] = ct2
            whole = m.group(0); new = whole
            if ct2 != ct:
                new = head + f'mv-core-{ct2}{name}' + tail; changed += 1
                print(f'{slug} {u["uid"]} {gid} -> mv-core-{ct2}{name} ({why})')
            if ct2 == 'heartbeat' and 'data-strong' not in new and motions.HEART_STRONG.search(u['text']):
                new = new[:-1] + ' data-strong="1">'; strong += 1
            if new != whole: out = out.replace(whole, new)
        if out != txt:
            out = out.replace(f'class="mv mv-core-', 'class="mv mv-core-')   # (ids become classes at build time; nothing else to touch)
            if not report: open(fn, 'w', encoding='utf-8').write(out)
    return changed, strong


if __name__ == '__main__':
    rep = '--report' in sys.argv; tot = 0
    for s in [a for a in sys.argv[1:] if not a.startswith('--')]:
        c, st = fix(s, rep); tot += c
        print(f'corefix: {s}: {c} centre motions {"would be " if rep else ""}changed, {st} strong heartbeats')
    print('corefix:', tot, 'changed' + (' (report only)' if rep else ''))
