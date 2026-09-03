#!/usr/bin/env python3
"""site/dist のリンク切れチェック（依存パッケージなし）

使い方:
    node site/build.mjs && python3 tools/linkcheck.py
    BASE_URL=/game-learning-archive node site/build.mjs && python3 tools/linkcheck.py --base /game-learning-archive

チェック内容:
  * href / src の内部リンクが dist 内の実ファイル（/foo/ → foo/index.html）に解決できるか
  * 同一ページ内のアンカー（#id）の指す id が存在するか
  * 外部リンク（http/https）は数だけ数えて通信は行わない
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit

ATTR_RE = re.compile(r'(?:href|src)\s*=\s*"([^"]*)"', re.I)
ID_RE = re.compile(r'\sid\s*=\s*"([^"]+)"', re.I)
SKIP_PREFIX = ("mailto:", "tel:", "javascript:", "data:")


def collect_ids(html: str) -> set[str]:
    return set(ID_RE.findall(html))


def resolve(dist: Path, page: Path, url: str, base: str) -> Path | None:
    """リンク先のファイルパスを返す。判定不能なら None。"""
    path = urlsplit(url).path
    if not path:
        return None
    if path.startswith("/"):
        if base and path.startswith(base + "/"):
            path = path[len(base):]
        elif base and path == base:
            path = "/"
        target = dist / unquote(path.lstrip("/"))
    else:
        target = (page.parent / unquote(path)).resolve()
    if target.is_dir():
        target = target / "index.html"
    elif path.endswith("/"):
        target = target / "index.html"
    return target


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dist", default="site/dist", help="ビルド出力ディレクトリ")
    ap.add_argument("--base", default="", help='BASE_URL 付きビルドの場合に指定（例: /game-learning-archive）')
    args = ap.parse_args()

    dist = Path(args.dist).resolve()
    base = args.base.rstrip("/")
    if not dist.is_dir():
        print(f"NG: {dist} がありません。先に `node site/build.mjs` を実行してください。")
        return 2

    pages = sorted(dist.rglob("*.html"))
    # play-files（pygbagビルド成果物）は生成物なので対象外
    pages = [p for p in pages if "play-files" not in p.relative_to(dist).parts]

    broken: list[str] = []
    checked = external = anchors = 0

    for page in pages:
        html = page.read_text(encoding="utf-8", errors="replace")
        ids = collect_ids(html)
        rel = page.relative_to(dist)
        for raw in ATTR_RE.findall(html):
            url = raw.strip()
            if not url or url.startswith(SKIP_PREFIX):
                continue
            if url.startswith(("http://", "https://", "//")):
                external += 1
                continue
            if url.startswith("#"):
                anchors += 1
                if url[1:] and url[1:] not in ids:
                    broken.append(f"{rel}: アンカー {url} が見つかりません")
                continue
            target = resolve(dist, page, url, base)
            if target is None:
                continue
            checked += 1
            if not target.exists():
                broken.append(f"{rel}: {url} → {target.relative_to(dist) if dist in target.parents else target} がありません")

    print(f"pages: {len(pages)} / 内部リンク: {checked} / アンカー: {anchors} / 外部リンク: {external}（未検証）")
    if broken:
        print(f"\nNG: リンク切れ {len(broken)} 件")
        for b in broken:
            print("  -", b)
        return 1
    print("OK: リンク切れはありません")
    return 0


if __name__ == "__main__":
    sys.exit(main())
