# _cdn — pygbag ランタイムの同梱コピー

遊べる23作品はすべて pygbag でビルドされており、以前は実行環境を
`https://pygame-web.github.io/cdn/0.9.4/` から読み込んでいた。
そのCDNが止まる・バージョンが消えると**全作品が一斉に遊べなくなる**ため、
アーカイブとして残すことを優先して、ここに一式を複製している。

## 取得元と内容（2026-09-04 時点）

`https://pygame-web.github.io/cdn/` から以下をそのまま複製した。

| ファイル | サイズ | 役割 |
|---|---|---|
| `0.9.4/pythons.js` | 69 KB | ランタイムの入口。ゲームの index.html はこれを読む |
| `0.9.4/cpython313/main.js` | 854 KB | CPython 3.13 の WASM ローダー |
| `0.9.4/cpython313/main.wasm` | 12.2 MB | CPython 3.13 本体 |
| `0.9.4/cpython313/main.data` | 6.8 MB | 標準ライブラリ・同梱パッケージ |
| `0.9.4/cpythonrc.py` | 50 KB | 起動時に実行される初期化スクリプト |
| `index-0.9.3-cp313.json` / `index-0.9.4-cp313.json` | 各 1.3 KB | パッケージの索引 |
| `vt.js` / `vtx.js` | 24 KB | 端末表示（`data-os="vtx,..."` が使う） |
| `vt/xterm.js` ほか3点 | 343 KB | 上記が読み込む xterm.js 一式（css・本体・画像アドオン） |
| `0.9.4/empty.html` | 0.1 KB | 本家では404だったため、404を出さないよう空ファイルを置いた |

## 注意

- **ディレクトリ構成を変えないこと。** `pythons.js` は自分のURLから
  基準パスを組み立て、`cpython313/…` や `../index-*.json` を相対で読む。
- ゲーム側の参照は `../_cdn/0.9.4/pythons.js`（相対）。
  公開先が `/game-learning-archive/` 配下でも、そのまま解決される。
- 差し替えたのは各ゲームの `index.html` の script の src だけで、
  **ゲームの中身（コード・素材・挙動）は変更していない。**
- pygbag のライセンスは配布元（pygame-web/pygbag）に従う。
