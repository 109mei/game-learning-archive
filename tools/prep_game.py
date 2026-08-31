#!/usr/bin/env python3
"""prep_game.py <src_dir> <id> <mainfile_rel> [--noto] [--keep-mp3]
Copies a pygame game to web_versions/<id>/, converts mp3->ogg, applies
web transforms to the main file (async wrap, ctypes guard, sys.exit->return),
and reports risky patterns. Original files are never modified."""
import os, re, shutil, subprocess, sys

SRC, GID, MAIN = sys.argv[1], sys.argv[2], sys.argv[3]
NOTO = '--noto' in sys.argv
KEEPMP3 = '--keep-mp3' in sys.argv
DST = f"/home/claude/game-learning-archive/web_versions/{GID}"
NOTO_TTF = "/home/claude/sources/卒論完成版/第4回ゲームジャム/これまで制作された作品/2Dgameジャンムー/jpfont/static/NotoSansJP-Regular.ttf"

EXCLUDE = {'__MACOSX', '.DS_Store', 'Thumbs.db', 'build', 'dist', '__pycache__'}

def ignore(d, names):
    return [n for n in names if n in EXCLUDE or n.endswith(('.exe', '.spec', '.blend', '.mp4', '.pptx', '.docx', '.xlsx'))]

if os.path.exists(DST):
    shutil.rmtree(DST)
shutil.copytree(SRC, DST, ignore=ignore)

warnings = []

# 1) mp3 -> ogg
if not KEEPMP3:
    for dp, dn, fn in os.walk(DST):
        for f in fn:
            if f.lower().endswith('.mp3'):
                src = os.path.join(dp, f)
                dst = src[:-4] + '.ogg'
                r = subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', src, '-c:a', 'libvorbis', '-qscale:a', '4', dst])
                if r.returncode == 0:
                    os.remove(src)
                else:
                    warnings.append(f'ffmpeg failed: {f}')

# 2) patch .py files: .mp3 -> .ogg references
for dp, dn, fn in os.walk(DST):
    for f in fn:
        if f.endswith('.py'):
            p = os.path.join(dp, f)
            s = open(p, encoding='utf-8', errors='replace').read()
            if not KEEPMP3:
                s2 = re.sub(r'\.mp3(["\'])', r'.ogg\1', s, flags=re.I)
            else:
                s2 = s
            if s2 != s:
                open(p, 'w', encoding='utf-8').write(s2)

mainp = os.path.join(DST, MAIN)
src = open(mainp, encoding='utf-8', errors='replace').read()
lines = src.split('\n')

# report risky patterns
if re.search(r'^\s*global\s', src, re.M):
    warnings.append('USES global STATEMENTS -> check scoping manually')
if 'tkinter' in src:
    warnings.append('USES tkinter -> not web compatible')
if re.search(r'while\s', src) is None:
    warnings.append('no while loop found?')
jp = re.findall(r'render\(\s*[fu]?["\'][^"\']*[ぁ-んァ-ヶ一-龠][^"\']*["\']', src)
if jp:
    warnings.append(f'JAPANESE text rendered ({len(jp)} calls) -> needs bundled font (--noto)')

out = []
out.append('# --- Web版 (pygbag対応のための自動変換コピー) ---')
out.append(f'# 元ファイル: {MAIN} / ゲーム内容は変更していません')
out.append('import asyncio')
out.append('')
out.append('async def main():')

body = []
for ln in lines:
    # ctypes guard
    if re.match(r'\s*import ctypes', ln) or 'ctypes.' in ln or 'windll' in ln or 'SetProcessDpiAware' in ln:
        body.append('    ' + re.match(r'(\s*)', ln).group(1) + 'pass  # web: ctypes無効化 | ' + ln.strip())
        continue
    # sys.exit -> return (top-level scope only, crude: indent <= 8)
    m = re.match(r'(\s*)sys\.exit\(\)', ln)
    if m:
        body.append('    ' + m.group(1) + 'return')
        continue
    body.append('    ' + ln if ln.strip() else '')

# insert await after clock.tick(...) lines and after top-level flip when no tick
ticked = False
res = []
for ln in body:
    res.append(ln)
    if re.search(r'\.tick\(', ln):
        indent = re.match(r'(\s*)', ln).group(1)
        res.append(indent + 'await asyncio.sleep(0)')
        ticked = True
if not ticked:
    res2 = []
    for ln in res:
        res2.append(ln)
        if re.search(r'pygame\.display\.(flip|update)\(', ln):
            indent = re.match(r'(\s*)', ln).group(1)
            res2.append(indent + 'await asyncio.sleep(0)')
    res = res2
    warnings.append('no clock.tick found; await inserted after flip/update (CHECK nested functions!)')

out += res
out.append('')
out.append('asyncio.run(main())')

# NOTO font replacement
final = '\n'.join(out)
if NOTO:
    shutil.copy(NOTO_TTF, os.path.join(DST, '_webfont.ttf'))
    final = re.sub(r'pygame\.font\.SysFont\(\s*(?:None|["\'][^"\']*["\'])\s*,\s*(\w+)([^)]*)\)',
                   r'pygame.font.Font("_webfont.ttf", \1)', final)
    final = re.sub(r'pygame\.font\.Font\(\s*None\s*,\s*(\w+)\s*\)',
                   r'pygame.font.Font("_webfont.ttf", \1)', final)

if MAIN != 'main.py':
    os.remove(mainp)
open(os.path.join(DST, 'main.py'), 'w', encoding='utf-8').write(final)

# syntax check
r = subprocess.run(['python3', '-m', 'py_compile', os.path.join(DST, 'main.py')], capture_output=True, text=True)
if r.returncode != 0:
    warnings.append('SYNTAX ERROR:\n' + r.stderr[-600:])

print(f'[{GID}] prepared at {DST}')
for w in warnings:
    print('  WARN:', w)
