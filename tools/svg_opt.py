# -*- coding: utf-8 -*-
# Optional svgo pass over the art before the build (miya 2026-10-29, guideline 4-6 / 15장). Keeps everything the rules read:
# ids (cleanupIds off: `mv-*` group names are the picture evidence), data-* attributes, group structure (collapseGroups off), hidden
# elements (removeHiddenElems off: opacity-0 morph targets, invisible parts motions reveal), basic shapes (convertShapeToPath off: facing.py
# finds eyes as circles), empty groups (mv-track routes), transforms as written. What it does: drops editor junk / comments / metadata,
# rounds numbers to 2 decimals, shortens path data and colours. Needs node + npx (svgo is fetched once per machine); when npx is missing
# or fails the original file is used and the build log says `svgo: skipped`. Never changes the originals: optimized copies go to <work>/art_opt/.
import hashlib, json, os, shutil, subprocess

CONFIG = {"multipass": False, "js2svg": {"indent": 0, "pretty": False},
          "plugins": [{"name": "preset-default", "params": {"overrides": {
              "cleanupIds": False, "collapseGroups": False, "removeHiddenElems": False, "convertShapeToPath": False, "mergePaths": False,
              "removeUnknownsAndDefaults": {"keepDataAttrs": True, "keepRoleAttr": True}, "removeUselessStrokeAndFill": False,
              "removeEmptyContainers": False, "convertTransform": False, "moveElemsAttrsToGroup": False, "moveGroupAttrsToElems": False,
              "removeViewBox": False, "cleanupNumericValues": {"floatPrecision": 2}, "convertPathData": {"floatPrecision": 2},
              "inlineStyles": False, "minifyStyles": False}}}]}
SVGO = ['npx', '--yes', 'svgo@4']


def available(timeout=90):
    """True when `npx svgo` can run here (node + network or a cached package)."""
    if os.environ.get('SVGO', '1') == '0' or not shutil.which('npx'): return False
    try:
        r = subprocess.run(SVGO + ['--version'], capture_output=True, text=True, timeout=timeout)
        return r.returncode == 0
    except Exception:
        return False


def optimize_dir(src_dir, work, names=None, timeout=240):
    """Optimize every *.svg of src_dir (or `names`) into <work>/art_opt/. Returns (mapping original->optimized path, stats dict).
    Files whose content hash is unchanged since the last run are reused (hash file next to the copy)."""
    out = f'{work}/art_opt'; os.makedirs(out, exist_ok=True); mp = {}; stats = dict(files=0, before=0, after=0, skipped=0, reason='')
    files = sorted(n for n in (names or os.listdir(src_dir)) if n.endswith('.svg'))
    if not files: return mp, stats
    todo = []
    for n in files:
        src = f'{src_dir}/{n}'; dst = f'{out}/{n}'; h = hashlib.sha1(open(src, 'rb').read()).hexdigest()
        hf = dst + '.sha1'
        if os.path.exists(dst) and os.path.exists(hf) and open(hf).read().strip() == h: mp[src] = dst; continue
        todo.append((src, dst, h))
    if todo:
        if not available(): stats['skipped'] = len(todo); stats['reason'] = 'npx svgo not available'; return {k: v for k, v in mp.items()}, stats
        tmp = f'{out}/_in'; shutil.rmtree(tmp, ignore_errors=True); os.makedirs(tmp)
        for src, dst, h in todo: shutil.copy(src, f'{tmp}/{os.path.basename(src)}')
        cfg = f'{out}/svgo.config.mjs'; open(cfg, 'w').write('export default ' + json.dumps(CONFIG) + ';\n')
        try:
            r = subprocess.run(SVGO + ['-q', '--config', cfg, '-f', tmp, '-o', out], capture_output=True, text=True, timeout=timeout)
        except Exception as e:
            stats['skipped'] = len(todo); stats['reason'] = f'svgo failed: {e}'; return mp, stats
        if r.returncode != 0:
            stats['skipped'] = len(todo); stats['reason'] = 'svgo exit ' + str(r.returncode) + ' ' + (r.stderr or '')[:120]; return mp, stats
        for src, dst, h in todo:
            if os.path.exists(dst) and os.path.getsize(dst) > 0 and '<svg' in open(dst, encoding='utf-8').read(400):
                open(dst + '.sha1', 'w').write(h); mp[src] = dst
            else: stats['skipped'] += 1
        shutil.rmtree(tmp, ignore_errors=True)
    for src, dst in mp.items():
        stats['files'] += 1; stats['before'] += os.path.getsize(src); stats['after'] += os.path.getsize(dst)
    return mp, stats


if __name__ == '__main__':
    import sys, tempfile
    d = sys.argv[1]; w = tempfile.mkdtemp()
    m, st = optimize_dir(d, w)
    print(json.dumps(st), 'saved', f'{(1 - st["after"] / st["before"]) * 100:.1f}%' if st['before'] else '-', 'at', w + '/art_opt')
