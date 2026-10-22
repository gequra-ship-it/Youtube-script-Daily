#!/usr/bin/env python3
"""title_lint.py - lint a title (and optional thumbnail text) against guideline 16-6 / 17-3.

    python3 tools/title_lint.py --title "..." [--thumb "..."]
    python3 tools/title_lint.py titles.txt [--thumb "..."]    # one title per line

Adapted from title.py in Jakeschincariol/youtube-agent-skill (MIT), with this channel's limits:
title <= 70 chars (mobile feed shows ~40), Title Case, no emoji, no all-caps words, no vague hype,
thumbnail 2-4 words and no word shared with the title. Advisory only; numbers must come from the script.
"""
import re, sys, os

MAX, MOBILE = 70, 40
VAGUE = {"amazing", "incredible", "insane", "crazy", "huge", "massive", "ultimate", "best", "powerful",
         "secret", "revolutionary", "mindblowing", "epic", "perfect", "everything"}
STOP = {"the", "a", "an", "of", "for", "to", "in", "on", "and", "or", "is", "are", "with", "your", "you",
        "my", "i", "this", "that", "it", "how", "what", "why", "at", "by", "as"}
SMALL = STOP | {"vs", "but", "from", "into", "not"}
EMOJI = re.compile("[\U0001F000-\U0001FAFF☀-➿]")

def words(t): return re.findall(r"[a-z0-9']+", t.lower())

def check(title, thumb=None):
    t, issues = title.strip(), []
    n = len(t)
    if n > MAX: issues.append(f"{n} chars (limit {MAX})")
    if EMOJI.search(t): issues.append("emoji")
    if re.search(r"[가-힣]", t): issues.append("Korean text (English only)")
    caps = [w for w in t.split() if len(w) > 1 and w.isupper() and not re.search(r"\d", w)]
    if caps: issues.append(f"all-caps: {', '.join(caps)}")
    low = [w for i, w in enumerate(t.split()) if w[:1].islower() and (i == 0 or w.lower() not in SMALL)]
    if low: issues.append(f"not Title Case: {', '.join(low)}")
    v = sorted({w for w in words(t) if w in VAGUE})
    if v: issues.append(f"vague hype: {', '.join(v)}")
    if not [w for w in words(t)[:3] if w not in STOP]: issues.append("first 3 words are filler")
    if thumb:
        shared = (set(words(t)) - STOP) & (set(words(thumb)) - STOP)
        if shared: issues.append(f"thumbnail repeats title: {', '.join(sorted(shared))}")
        k = len(words(thumb))
        if not 2 <= k <= 4: issues.append(f"thumbnail has {k} words (2-4)")
    return n, issues

def main():
    a = sys.argv[1:]
    thumb = a[a.index("--thumb") + 1] if "--thumb" in a else None
    if "--title" in a: titles = [a[a.index("--title") + 1]]
    elif a and os.path.exists(a[0]): titles = [l for l in open(a[0]).read().splitlines() if l.strip()]
    else: print(__doc__); sys.exit(1)
    for t in titles:
        n, issues = check(t, thumb)
        print(f'{"OK " if not issues else "FIX"} [{n}] {t}')
        if not re.search(r"\d", t): print("      (note) no number/year - add one only if the script has it")
        if n > MOBILE: print(f'      (note) mobile feed shows ~"{t[:MOBILE].rsplit(" ", 1)[0]}..."')
        for i in issues: print(f"      - {i}")

if __name__ == "__main__":
    main()
