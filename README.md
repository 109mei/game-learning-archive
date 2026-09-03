# ゲーム制作・プログラミング学習アーカイブ

「**ゲームを遊んで、コードを見て、ゲーム制作を学ぶ**」ためのアーカイブサイトです。
ゲームジャム・ゲームコンテスト・ゲームプログラミング授業・高大連携・IDERIAの制作活動で生まれたゲームを、ブラウザで遊べる形（pygame-ce → pygbag → WebAssembly）で記録・公開します。

※ このサイトは **IDERIA公式ホームページではありません**。IDERIA公式サイト（`ideriaOfficialUrl`）とポートフォリオ（`portfolioUrl`）のURLは `site/src/data/site.json` で設定し、フッター上の「関連サイト」セクションとフッターの両方に自動でリンクが出ます（**空欄のあいだは表示されません**）。

## フォルダ構成

```
game-learning-archive/
├── README.md            ← このファイル
├── docs/                ← 監査記録・設計書・要確認リスト（TODO.md を必ず確認）
├── web_versions/        ← pygame作品のWeb対応版（元ゲームは一切変更していません）
│   └── <作品id>/main.py + 素材 + build/web/（pygbagビルド結果）
└── site/                ← Webサイト本体
    ├── build.mjs        ← 静的サイトジェネレーター（依存パッケージなし・Node 18+）
    ├── src/data/        ← ★サイトの全データ（ここを編集するだけでページが増える）
    │   ├── site.json / categories.json / organizations.json / tech.json
    │   ├── games/<作品id>.json       ← 1作品=1ファイル
    │   └── activities/<活動id>.json  ← 1活動=1ファイル
    ├── src/styles.css / src/site.js  ← デザイン・クライアントJS
    ├── game-sources/<作品id>/        ← コード閲覧ページに表示するソース（公開確認済みのみ）
    │   └── reverse/                  ← 逆引きコード35本（学習ページの元データ）
    ├── public/
    │   ├── play-files/<作品id>/      ← pygbagビルド（ブラウザで遊ぶ実体）
    │   └── images/games/             ← サムネイル・スクリーンショット
    └── dist/                         ← ビルド出力（このフォルダを公開する）
```

## サイトの起動方法

Node.js 18以上があれば **npm install 不要** で動きます。

```bash
cd site
node build.mjs                 # dist/ に全ページを生成
cd dist
python -m http.server 8080     # または npx serve など
# → http://localhost:8080 を開く
```

ビルド後は、リンク切れがないかを確認できます（Python標準ライブラリのみ）。

```bash
node site/build.mjs && python3 tools/linkcheck.py
# サブパス公開の確認は: BASE_URL=/game-learning-archive node site/build.mjs && python3 tools/linkcheck.py --base /game-learning-archive
```

公開するときは `dist/` をそのまま GitHub Pages / Netlify / Cloudflare Pages にアップロードします（無料枠で運用可能）。GitHub Actions を使う場合は「node site/build.mjs → site/dist を公開」の2ステップだけです。

## 作品の追加方法（データを足すだけ）

1. `site/src/data/games/` に新しいJSONを1つ作る（既存ファイルをコピーして書き換えるのが簡単です）。
   - `id` はファイル名と同じ英小文字+ハイフン。`activities` に関連する活動idを配列で入れると、活動ページにも自動で表示されます（多対多）。
   - 不明な項目は `null` のままにすると **サイト上では自動的に非表示** になります。推測で埋めないでください。
2. 画像: プレイ画面を `site/public/images/games/<id>.png`（640×400目安）に置くとサムネイルに自動採用。無ければ「画像準備中」プレースホルダーが表示されます。
3. ブラウザ対応させる場合（pygame-ce作品）:
   - `web_versions/<id>/` にゲームのコピーを作り `main.py` にリネーム、メインループを `async` 化（`docs/WEB_COMPATIBILITY.md` の共通変換ポイント参照）。
   - `pip install pygbag` して `pygbag --build web_versions/<id>/main.py`
   - できた `build/web/` を `site/public/play-files/<id>/` にコピーし、gameのJSONで `play.playable: true, play.url: "/play-files/<id>/index.html"` にする。
4. ソード公開する場合: `site/game-sources/<id>/` に **公開確認済みの** ソースを置き、JSONの `source` を設定（ファイル名・コード内に個人名が無いか必ず確認）。
5. `node build.mjs` を実行して確認 → コミット。

活動・カテゴリ・年度も同様に、`activities/` へのJSON追加・`categories.json` への1行追加だけで一覧・詳細・年度ページへ自動反映されます（第5回・第6回ゲームジャム等はJSONを1つ足すだけ）。

## GitHubでの管理・公開

このフォルダはそのままGitリポジトリになっています（`.gitignore` 設定済み。`site/dist/` とpygbagの中間ビルドはコミット対象外で、`node site/build.mjs` でいつでも再生成できます）。

**GitHubへ最初にpushする手順**（GitHubで空のリポジトリ `game-learning-archive` を作成してから）:

```bash
git remote add origin https://github.com/<ユーザー名>/game-learning-archive.git
git push -u origin main
```

**GitHub Pagesで公開する手順**:

1. リポジトリの Settings → Pages → 「Build and deployment」の Source を **GitHub Actions** にする
2. mainにpushすると `.github/workflows/deploy.yml` が自動でビルド・公開（`https://<ユーザー名>.github.io/game-learning-archive/` で公開されます）

サブパス公開のためのURL調整は自動です（ワークフローが `BASE_URL` を設定してビルドします）。手元で同じ状態を確認したいときは `BASE_URL=/game-learning-archive node site/build.mjs`。

注意: 学生作品などの権利関係が未確認のため、**公開リポジトリにする前に `docs/TODO.md` の公開可否チェックを済ませ、それまでは Private リポジトリにしておくことを推奨**します。オープンソースライセンスは付与していません（作品の著作権は各制作者にあります）。

## デザイン（テーマ「コードの深海に潜る」）

見た目と遊び要素の仕様は **`docs/DESIGN_SPEC_V2.md` が「正」** です。デザインを変えたいときは、まず仕様書を書きかえてから実装します。

- トップページは「潜行ルート」の層構造（海面 → あそぶ → よむ → しくみをしる → つくる → きろく）。画面端の**深度メーター**と**層ジャンプ**で行き来できます。深度の数値は演出で、実データではありません。
- **ダークトーン基調**（深海）。ヘッダーの ◐ ボタンでライト（浅瀬）に切りかえられ、選択は localStorage に保存されます。
- 遊び要素（**図鑑スタンプ・実績バッジ**）の記録は **localStorage のみ**。サーバーへは一切送信せず、保存が使えないブラウザではスタンプ表示を省くだけで他の機能は通常どおり動きます。
- 泡や光の演出は自作のCSSアニメーションで、`prefers-reduced-motion` が有効な環境では停止します。
- フッターの上に「**関連サイト**」（ポートフォリオ・IDERIA公式サイト）のカードを全ページ共通で表示します。URLは `site.json` 由来で、空欄のカードは表示されません。

## 技術選定の理由

要件（GitHub管理・ゲーム追加が簡単・静的公開・pygbag埋め込み・将来のDB移行・複雑にしない・無料公開）に対して React / Next.js / Astro / 自作ジェネレーターを比較しました。

| 候補 | 評価 |
|---|---|
| Next.js (React) | SPA/SSR向き。静的アーカイブには過剰で、依存パッケージの更新・破壊的変更への追従コストが長期運用の負担になる |
| Astro | データ駆動の静的生成に好適。ただし依存が大きく、数年スパンではメジャーアップデート対応が必要 |
| 素のHTML手書き | 作品が増えるたびに全ページ手編集になるため不採用（要件違反） |
| **自作静的ジェネレーター（採用）** | **Node標準機能のみ・依存ゼロ**。`node build.mjs` だけで動き、npm install も lockfile も不要なので**何年後でも同じように動く**。データ(JSON)→全ページ自動生成という構造はAstroと同じで、将来Astro等へ移行する場合もデータをそのまま使える |

データはすべてJSON（= そのままDBのレコード構造）なので、将来データベースやCMSへ移行する際は games / activities / categories / organizations の4テーブル＋関連テーブルにインポートするだけです。

## ブラウザプレイの仕組み

pygame-ce 製ゲーム → **pygbag** で WebAssembly 化 → `public/play-files/<id>/` に配置 → プレイページ(`/play/<id>/`)から **iframe** で分離表示。
実行ランタイム（pythons.js 等）は pygame-web の公式CDNから読み込むため、プレイにはインターネット接続が必要です。各作品のWeb対応状況・変換内容は `docs/WEB_COMPATIBILITY.md` を参照してください。**元のゲームファイルは一切変更していません**（Web対応はすべて `web_versions/` のコピーに対して実施）。

## 公開前に必ず確認すること

`docs/TODO.md`（人間の確認が必要な項目）と `docs/PRIVACY_CHECK.md`（非公開にすべき資料）を必ず確認してください。特に:

- 学生作品の公開許可（ソースコード含む）
- 写真の公開可否（現状、人物が写っている可能性のある写真は掲載していません）
- 「要確認」となっている日付・人数・作品名

## 管理ドキュメント

| ファイル | 内容 |
|---|---|
| docs/SITE_PLAN.md | サイト情報設計 |
| docs/SPECIFICATION.md | 機能仕様 |
| docs/DESIGN_SPEC_V2.md | デザイン・遊び要素の仕様（見た目の「正」） |
| docs/DATA_MODEL.md | データ構造の説明 |
| docs/CONTENT_AUDIT.md | 元資料の監査記録 |
| docs/GAME_INVENTORY.md | 見つかったゲーム一覧 |
| docs/ACTIVITY_INVENTORY.md | 見つかった活動一覧 |
| docs/WEB_COMPATIBILITY.md | 各pygame作品のWeb対応状況 |
| docs/PRIVACY_CHECK.md | 公開時に注意が必要な資料 |
| docs/TODO.md | 人間による確認が必要な項目 |
