#!/usr/bin/env python3
"""wrap_toploop.py <orig_main_py> <dest_dir> [--noto] [--keep-mp3]
For games with module-level functions (using `global`) plus a top-level while loop.
Wraps only the top-level while loop (and everything after it) into async main(),
declaring `global` for names assigned inside the loop. Writes <dest_dir>/main.py.
Assumes prep of assets (mp3->ogg etc.) already done by prep_game.py (which may
have produced a broken main.py to be overwritten by this)."""
import ast, re, sys, os, subprocess, shutil

ORIG, DST = sys.argv[1], sys.argv[2]
NOTO = '--noto' in sys.argv
KEEPMP3 = '--keep-mp3' in sys.argv
NOTO_TTF = "/home/claude/sources/卒論完成版/第4回ゲームジャム/これまで制作された作品/2Dgameジャンムー/jpfont/static/NotoSansJP-Regular.ttf"

src = open(ORIG, encoding='utf-8', errors='replace').read()
if not KEEPMP3:
    src = re.sub(r'\.mp3(["\'])', r'.ogg\1', src, flags=re.I)
# ctypes guard (line-based)
lines = src.split('\n')
for i, ln in enumerate(lines):
    if re.match(r'\s*import ctypes', ln) or 'windll' in ln or 'SetProcessDpiAware' in ln or ('ctypes.' in ln and 'import' not in ln):
        indent = re.match(r'(\s*)', ln).group(1)
        lines[i] = indent + 'pass  # web: ctypes無効化 | ' + ln.strip()
src = '\n'.join(lines)

tree = ast.parse(src)
whiles = [n for n in tree.body if isinstance(n, ast.While)]
if not whiles:
    print('NO top-level while found'); sys.exit(1)
w = whiles[-1]
start = w.lineno - 1          # 0-based
lines = src.split('\n')

# collect names assigned inside the loop (excluding nested funcs)
assigned = set()
class V(ast.NodeVisitor):
    def visit_FunctionDef(self, n): pass
    def visit_AsyncFunctionDef(self, n): pass
    def collect_target(self, t):
        if isinstance(t, ast.Name): assigned.add(t.id)
        elif isinstance(t, (ast.Tuple, ast.List)):
            for e in t.elts: self.collect_target(e)
    def visit_Assign(self, n):
        for t in n.targets: self.collect_target(t)
        self.generic_visit(n)
    def visit_AugAssign(self, n):
        self.collect_target(n.target); self.generic_visit(n)
    def visit_For(self, n):
        self.collect_target(n.target); self.generic_visit(n)
    def visit_withitem(self, n):
        if n.optional_vars: self.collect_target(n.optional_vars)
V().visit(w)
assigned = sorted(a for a in assigned if not a.startswith('__'))

head = lines[:start]
tail = lines[start:]
out = []
out.append('# --- Web版 (pygbag対応のための変換コピー / ゲーム内容は変更していません) ---')
out.append('import asyncio')
out += head
out.append('')
out.append('async def main():')
if assigned:
    out.append('    global ' + ', '.join(assigned))
for ln in tail:
    m = re.match(r'(\s*)sys\.exit\(\)\s*$', ln)
    if m:
        out.append('    ' + m.group(1) + 'return')
        continue
    out.append('    ' + ln if ln.strip() else '')
    if re.search(r'\.tick\(', ln):
        out.append('    ' + re.match(r'(\s*)', ln).group(1) + 'await asyncio.sleep(0)')
out.append('')
out.append('asyncio.run(main())')
final = '\n'.join(out)
if NOTO:
    shutil.copy(NOTO_TTF, os.path.join(DST, '_webfont.ttf'))
    final = re.sub(r'pygame\.font\.SysFont\(\s*(?:None|["\'][^"\']*["\'])\s*,\s*(\w+)([^)]*)\)',
                   r'pygame.font.Font("_webfont.ttf", \1)', final)
    final = re.sub(r'pygame\.font\.Font\(\s*None\s*,\s*(\w+)\s*\)',
                   r'pygame.font.Font("_webfont.ttf", \1)', final)
open(os.path.join(DST, 'main.py'), 'w', encoding='utf-8').write(final)
r = subprocess.run(['python3', '-m', 'py_compile', os.path.join(DST, 'main.py')], capture_output=True, text=True)
print('globals:', ', '.join(assigned) if assigned else '(none)')
print(r.stderr[-500:] if r.returncode else 'syntax OK')
