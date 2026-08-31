#!/usr/bin/env python3
"""webify.py <orig_main_py> <dest_dir> [--noto] [--keep-mp3] [--drop-import=name ...]
Full web conversion for pygame games with nested loops:
- mp3->ogg refs, backslash paths, ctypes guard, FULLSCREEN removal
- asyncifies functions containing loops/tick/delay and their callers (call graph)
- awaits calls to asyncified functions; converts delay/wait/sleep to asyncio.sleep
- wraps top-level game flow into async main() with global declarations
Writes <dest_dir>/main.py. Original file is never modified."""
import ast, re, sys, os, shutil, subprocess

ORIG, DST = sys.argv[1], sys.argv[2]
NOTO = '--noto' in sys.argv
KEEPMP3 = '--keep-mp3' in sys.argv
DROPS = [a.split('=',1)[1] for a in sys.argv if a.startswith('--drop-import=')]
NOTO_TTF = "/home/claude/sources/卒論完成版/第4回ゲームジャム/これまで制作された作品/2Dgameジャンムー/jpfont/static/NotoSansJP-Regular.ttf"

src = open(ORIG, encoding='utf-8', errors='replace').read()
warn = []

# --- textual pre-transforms ---
if not KEEPMP3:
    src = re.sub(r'\.mp3(["\'])', r'.ogg\1', src, flags=re.I)
def _fixslash(m):
    q, body = m.group(1), m.group(2)
    return q + body.replace('\\', '/') + q
src = re.sub(r'(["\'])([^"\'\n]*\\[^"\'\n]*\.(?:png|jpg|jpeg|gif|bmp|ogg|wav|mp3|ttf|otf|json|txt))\1', _fixslash, src, flags=re.I)
src = re.sub(r'pygame\.FULLSCREEN', '0', src)
for d in DROPS:
    src = re.sub(rf'^(\s*)import {re.escape(d)}\s*$', rf'\1pass  # web: import {d} 無効化', src, flags=re.M)
    src = re.sub(rf'^(\s*)import {re.escape(d)} as (\w+)\s*$', rf'\1pass  # web: import {d} 無効化', src, flags=re.M)
lines = src.split('\n')
for i, ln in enumerate(lines):
    if re.match(r'\s*import ctypes', ln) or 'windll' in ln or 'SetProcessDpiAware' in ln or 'SetProcessDPIAware' in ln:
        indent = re.match(r'(\s*)', ln).group(1)
        lines[i] = indent + 'pass  # web: ctypes無効化 | ' + ln.strip()
src = '\n'.join(lines)

tree = ast.parse(src)

# --- find functions needing async ---
MARKERS = re.compile(r'\.tick\(|pygame\.time\.delay\(|pygame\.time\.wait\(|time\.sleep\(|pygame\.display\.flip\(|pygame\.display\.update\(')
funcs = {}
calls = {}
class FInfo(ast.NodeVisitor):
    def __init__(self): self.stack=[]
    def visit_FunctionDef(self, n):
        seg = ast.get_source_segment(src, n) or ''
        has_loop = any(isinstance(x, (ast.While, ast.For)) for x in ast.walk(n))
        needs = bool(MARKERS.search(seg)) and has_loop or bool(re.search(r'pygame\.time\.delay\(|pygame\.time\.wait\(|time\.sleep\(', seg))
        funcs[n.name] = needs
        cs = set()
        for x in ast.walk(n):
            if isinstance(x, ast.Call) and isinstance(x.func, ast.Name):
                cs.add(x.func.id)
        calls[n.name] = cs
        for b in n.body: self.visit(b)
FInfo().visit(tree)

async_set = {n for n, v in funcs.items() if v}
changed = True
while changed:
    changed = False
    for n, cs in calls.items():
        if n not in async_set and cs & async_set:
            async_set.add(n); changed = True

# --- rewrite defs and calls (text level) ---
for name in async_set:
    src = re.sub(rf'^(\s*)def {re.escape(name)}\(', rf'\1async def {name}(', src, flags=re.M)
    src = re.sub(rf'(?<!def )(?<!await )(?<!\.)\b{re.escape(name)}\(', f'await {name}(', src)
    src = re.sub(rf'async def await {re.escape(name)}\(', f'async def {name}(', src)  # repair def lines

# delay/wait/sleep -> await asyncio.sleep  (assume they sit in async context now)
src = re.sub(r'pygame\.time\.delay\(([^)]+)\)', r'await asyncio.sleep((\1)/1000)', src)
src = re.sub(r'pygame\.time\.wait\(([^)]+)\)', r'await asyncio.sleep((\1)/1000)', src)
src = re.sub(r'(?<!await asyncio\.)time\.sleep\(([^)]+)\)', r'await asyncio.sleep(\1)', src)

# insert await sleep(0) after tick lines
out_lines = []
for ln in src.split('\n'):
    out_lines.append(ln)
    if re.search(r'\.tick\(', ln) and 'await asyncio.sleep' not in ln:
        out_lines.append(re.match(r'(\s*)', ln).group(1) + 'await asyncio.sleep(0)')
src = '\n'.join(out_lines)

# --- wrap top-level tail into async main() ---
tree2 = ast.parse(re.sub(r'\bawait ', '', src))  # parse a sync-ish shadow just for line numbers of top-level stmts
top = tree2.body
start_line = None
for n in top:
    seg_has_async_call = False
    if not isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef, ast.Import, ast.ImportFrom)):
        seg = ast.get_source_segment(re.sub(r'\bawait ', '', src), n) or ''
        if isinstance(n, ast.While) or any(re.search(rf'\b{re.escape(a)}\(', seg) for a in async_set) or 'await asyncio.sleep' in seg:
            seg_has_async_call = True
    if seg_has_async_call:
        start_line = n.lineno
        break
if start_line is None:
    warn.append('NO top-level wrap point found (no while / async calls at top level)')
    final = 'import asyncio\n' + src
else:
    slines = src.split('\n')
    head, tail = slines[:start_line-1], slines[start_line-1:]
    # collect names assigned in tail at top level
    assigned = set()
    tail_src = '\n'.join(tail)
    ttree = ast.parse(re.sub(r'\bawait ', '', tail_src))
    class TV(ast.NodeVisitor):
        def visit_FunctionDef(self, n): pass
        def visit_AsyncFunctionDef(self, n): pass
        def visit_ClassDef(self, n): pass
        def coll(self, t):
            if isinstance(t, ast.Name): assigned.add(t.id)
            elif isinstance(t, (ast.Tuple, ast.List)):
                for e in t.elts: self.coll(e)
        def visit_Assign(self, n):
            for t in n.targets: self.coll(t)
            self.generic_visit(n)
        def visit_AugAssign(self, n): self.coll(n.target); self.generic_visit(n)
        def visit_For(self, n): self.coll(n.target); self.generic_visit(n)
    TV().visit(ttree)
    assigned = sorted(a for a in assigned if not a.startswith('__'))
    out = ['# --- Web版 (pygbag対応のための変換コピー / ゲーム内容は変更していません) ---', 'import asyncio']
    out += head
    out.append('')
    out.append('async def _web_main():')
    if assigned:
        out.append('    global ' + ', '.join(assigned))
    for ln in tail:
        m = re.match(r'(\s*)sys\.exit\(\)\s*(#.*)?$', ln)
        if m:
            out.append('    ' + m.group(1) + 'return')
            continue
        out.append('    ' + ln if ln.strip() else '')
    out.append('')
    out.append('asyncio.run(_web_main())')
    final = '\n'.join(out)


# --- ensure every while loop inside async defs yields ---
def _inject_loop_awaits(text):
    lines = text.split('\n')
    out = []
    scopes = []  # (indent, is_async)
    warns = []
    for idx, ln in enumerate(lines):
        stripped = ln.strip()
        ind = len(ln) - len(ln.lstrip()) if stripped else None
        if stripped and scopes:
            while scopes and ind is not None and ind <= scopes[-1][0]:
                scopes.pop()
        m = re.match(r'^(\s*)(async\s+)?def\s', ln)
        if m:
            scopes.append((len(m.group(1)), bool(m.group(2))))
            out.append(ln)
            continue
        out.append(ln)
        mw = re.match(r'^(\s*)while\b.*:\s*(#.*)?$', ln)
        if mw:
            in_async = scopes[-1][1] if scopes else False
            if in_async:
                nxt = None
                for j in range(idx+1, len(lines)):
                    if lines[j].strip(): nxt = lines[j]; break
                if nxt is None or 'await asyncio.sleep' not in nxt:
                    out.append(mw.group(1) + '    ' + 'await asyncio.sleep(0)')
            else:
                warns.append('sync while at line %d not yielded' % (idx+1))
    return '\n'.join(out), warns

final, _loopwarns = _inject_loop_awaits(final)
for w in _loopwarns: warn.append(w)

if NOTO:
    shutil.copy(NOTO_TTF, os.path.join(DST, '_webfont.ttf'))
    final = re.sub(r'pygame\.font\.SysFont\(\s*(?:None|["\'][^"\']*["\'])\s*,\s*(\w+)([^)]*)\)',
                   r'pygame.font.Font("_webfont.ttf", \1)', final)
    final = re.sub(r'pygame\.font\.Font\(\s*None\s*,\s*(\w+)\s*\)',
                   r'pygame.font.Font("_webfont.ttf", \1)', final)

os.makedirs(DST, exist_ok=True)
open(os.path.join(DST, 'main.py'), 'w', encoding='utf-8').write(final)
r = subprocess.run(['python3', '-m', 'py_compile', os.path.join(DST, 'main.py')], capture_output=True, text=True)
print('async funcs:', ', '.join(sorted(async_set)) or '(none)')
for w in warn: print('WARN:', w)
print(r.stderr[-800:] if r.returncode else 'syntax OK')
