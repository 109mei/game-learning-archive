#!/usr/bin/env python3
"""fix_paths.py <main_py> : replace backslashes with slashes inside quoted asset path strings"""
import re, sys, subprocess
p = sys.argv[1]
s = open(p, encoding='utf-8').read()
def fix(m):
    q, body = m.group(1), m.group(2)
    return q + body.replace('\\', '/') + q
s2 = re.sub(r'(["\'])([^"\'\n]*\\[^"\'\n]*\.(?:png|jpg|jpeg|gif|bmp|ogg|wav|mp3|ttf|otf|json|txt))\1', fix, s, flags=re.I)
if s2 != s:
    open(p, 'w', encoding='utf-8').write(s2)
    print('fixed backslash paths:', p)
else:
    print('no backslash paths:', p)
