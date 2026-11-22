"""Check the YouTube metadata of a video before it is uploaded (guideline 22-3). Report only.
Usage: python3 tools/check/title_unique.py <long slug> [<long slug> ...]
For each slug and its -short1..5 it checks render/<slug>/deliver/*_metadata.txt:
  - the title is not the title of ANY OTHER render/*/deliver metadata (a duplicate would be skipped as "already on the channel")
  - title <= 100 characters, not empty
  - description <= 4900 bytes (the uploader cuts longer ones) and without < > (the uploader removes them: WARN)
Exit 1 when an ERROR is found, so the youtube-upload workflow stops before uploading."""
import re, sys, glob, pathlib

def read(p):
    t = pathlib.Path(p).read_text(encoding="utf-8")
    m = re.search(r"=== TITLE ===\s*(.+?)\s*=== DESCRIPTION ===\s*(.*)", t, re.S)
    return (m.group(1).strip(), m.group(2).strip()) if m else (None, None)

bases = sys.argv[1:]
mine = {}
for b in bases:
    for s in [b] + [f"{b}-short{i}" for i in range(1, 6)] + [f"{b}-short"]:
        for f in glob.glob(f"render/{s}/deliver/*_metadata.txt"): mine[s] = f
allt = {}
for f in glob.glob("render/*/deliver/*_metadata.txt"):
    slug = f.split("/")[1]
    t, _ = read(f)
    if t: allt.setdefault(t.lower(), []).append(slug)
err = warn = 0
for s, f in sorted(mine.items()):
    t, d = read(f)
    if not t: print(f"ERROR {s}: no '=== TITLE ===' / '=== DESCRIPTION ===' in {f}"); err += 1; continue
    others = [x for x in allt.get(t.lower(), []) if x != s]
    if others: print(f"ERROR {s}: title '{t}' is also the title of {', '.join(others)}"); err += 1
    if len(t) > 100: print(f"ERROR {s}: title is {len(t)} characters (max 100)"); err += 1
    if "<" in t or ">" in t: print(f"ERROR {s}: title contains < or >"); err += 1
    if len(d.encode("utf-8")) > 4900: print(f"WARN {s}: description {len(d.encode('utf-8'))} bytes, the uploader will cut it"); warn += 1
    if "<" in d or ">" in d: print(f"WARN {s}: description has < or >, the uploader removes them"); warn += 1
print(f"checked {len(mine)} metadata files: {err} error(s), {warn} warning(s)")
sys.exit(1 if err else 0)
