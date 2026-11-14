#!/usr/bin/env python3
"""2026-11-05 (miya): entrance motions must not show the finished arrangement before they start.
A tl.fromTo(X,{hidden start},{...immediateRender:false},t) leaves X drawn until t. It needs a tl.set(X,{same hidden property},..) earlier.
Usage: entrycheck.py <slug>   (reads render/<slug>/index.html; exit 1 on findings)"""
import os as _o, sys as _s; _T = _o.path.dirname(_o.path.dirname(_o.path.abspath(__file__))); _s.path[:0] = [_T] + [_T + '/' + _d for _d in ('build', 'check', 'fix', 'preview', 'writing')]   # tools root (libraries) + sibling folders, 2026-11-14 layout
import re, sys, os
slug = sys.argv[1]
root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
html = open(f'{root}/render/{slug}/index.html', encoding='utf-8').read()
HID = re.compile(r'(opacity:0(?![.\d])|scale:0(?![.\d])|scaleX:0(?![.\d])|scaleY:0(?![.\d])|scale:\.[0-4]\d*|drawSVG:"0%")')
sets = re.findall(r'tl\.set\((.+?),\{([^}]*)\}', html)
bad = []
for m in re.finditer(r'tl\.fromTo\((.+?),\{([^{}]*)\},\{[^\n]*?immediateRender:false', html):
    tgt, frm = m.group(1), m.group(2)
    props = {p.split(':')[0] for p in HID.findall(frm) if False} or {re.split(r'[:\d.]', h)[0] for h in HID.findall(frm)}
    if not HID.search(frm) or '.mv-' not in tgt or re.search(r'mv-(glint|drift|cells|rip|ring)', tgt): continue   # picture groups only; ambient layers and helper fx are always visible
    key = re.findall(r'(opacity|scaleX|scaleY|scale|drawSVG)\s*:', frm)
    ok = any(t == tgt and any(k in body for k in key) for t, body in sets)
    if not ok and 'miyaPath' not in tgt: bad.append(tgt[:60])
print(f'entrycheck: {"OK" if not bad else str(len(bad)) + " entrance(s) show the finished state first: " + ", ".join(sorted(set(bad))[:6])}')
sys.exit(1 if bad else 0)
