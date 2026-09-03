# DATA_MODEL.md — データ構造設計

原則: **作品(Games)と活動(Activities)は別データ・多対多**。データファイルを追加するだけで一覧・詳細・年度・カテゴリページに自動反映される。不明値は `null` または `"要確認"` で保持し、サイト側は非表示にする。

## ディレクトリ

```
site/src/data/
├── site.json            # サイト全体設定（IDERIA公式URL等）
├── categories.json      # 活動カテゴリ（追加可能）
├── organizations.json   # 団体・制作元
├── games/               # 1作品=1ファイル
│   └── <game-id>.json
└── activities/          # 1活動=1ファイル
    └── <activity-id>.json
site/src/content/learn/  # 学習コンテンツ（Markdown, 追加可能）
    └── <slug>.md
```

## Game（games/*.json）

```jsonc
{
  "id": "gj1-one",                  // ファイル名と一致。英数小文字とハイフン
  "title": "ONE",
  "summary": "1ボタンで遊ぶ…",      // カード用の短い説明（null可）
  "description": "…",               // 詳細ページ用（null可）
  "controls": "スペースキーでジャンプ", // 操作方法（null可）
  "genre": "アクション",             // null か "要確認" なら非表示
  "players": "1人",                 // null可
  "year": 2025,                     // 年度（西暦の年度=4月始まり）
  "createdDate": "2025-05-22",      // null可
  "organizations": ["kiis"],        // organizations.json の id 配列
  "creatorDisplay": "九州情報大学の学生チーム（3名）", // 表示用のみ。個人名は本人作品のみ
  "activities": ["game-jam-1"],     // 多対多: 活動idの配列
  "tech": ["python", "pygame"],     // 使用技術タグ
  "thumbnail": null,                // /images/games/… へのパス。null=「画像準備中」
  "screenshots": [],
  "background": null,               // 制作背景（null可）
  "highlights": null,               // 工夫した点（null可）
  "play": {                         // ブラウザプレイ
    "playable": true,
    "url": "/play-files/gj1-one/index.html", // pygbagビルドの場所
    "note": null                    // 「音が出ない場合は…」等
  },
  "source": {                       // ソースコード閲覧
    "available": true,
    "dir": "gj1-one",               // site/game-sources/<dir>/ を読み込む
    "entry": "game.py"
  },
  "learnTopics": ["collision", "game-loop"], // 学習ページのslug（「このゲームで使われている技術」）
  "webVersionNote": null,           // Web版で変更した点
  "verification": "要確認: …"       // 監査メモ（サイト非表示）
}
```

## Activity（activities/*.json）

```jsonc
{
  "id": "game-jam-1",
  "title": "第1回ゲームジャム",
  "category": "game-jam",           // categories.json の id
  "series": { "name": "ゲームジャム", "number": 1 }, // 一覧の「年度→開催回」表示に使用。null可
  "year": 2025,                     // 年度
  "dates": ["2025-05-15", "2025-05-22"], // 不明なら []
  "dateNote": null,                 // 「推定」等の注記
  "place": "九州情報大学",
  "target": "大学生",
  "participants": 9,                // null=非表示
  "teams": 4,
  "theme": null,
  "format": "2回の活動に分割・チーム制作",
  "tech": ["python", "pygame"],
  "organizations": ["kiis", "ideria"],
  "summary": "…",
  "description": "…",
  "photos": [],                     // 公開許可確認済みのみ追加
  "relatedDocs": [],                // {title, url} 配列（配布資料など）
  "researchNote": "研究上は旧第1回（新第1回の内訳A）", // サイト非表示のメモ
  "verification": null
}
```

作品→活動は `game.activities`、活動→作品はビルド時に全gamesを走査して逆引き（活動ページに自動で作品一覧が出る）。

## categories.json（追加自由）

```jsonc
[
  { "id": "game-jam",  "name": "ゲームジャム",           "slug": "game-jams" },
  { "id": "contest",   "name": "ゲームコンテスト",       "slug": "contests" },
  { "id": "class",     "name": "ゲームプログラミング授業", "slug": "classes" },
  { "id": "collab",    "name": "高大連携",               "slug": "collabs" },
  { "id": "ideria",    "name": "IDERIA制作",             "slug": "ideria" },
  { "id": "personal",  "name": "自主制作",               "slug": "personal" },
  { "id": "exhibit",   "name": "展示",                   "slug": "exhibits" },
  { "id": "workshop",  "name": "ワークショップ",          "slug": "workshops" },
  { "id": "other",     "name": "その他",                 "slug": "others" }
]
```

活動は `category`（主分類）のほか `subCategories`（任意配列）で複数分類に対応（例: 第3回ジャム = game-jam ＋ collab）。

## organizations.json

```jsonc
[
  { "id": "ideria", "name": "IDERIA", "url": null },   // 公式サイトURLは決まったら記入
  { "id": "kiis",   "name": "九州情報大学", "url": null },
  { "id": "junshin","name": "純真高等学校", "url": null },
  { "id": "kaho",   "name": "福岡県立嘉穂総合高等学校", "url": null }
]
```

## site.json

```jsonc
{
  "title": "PLAYCE",
  "subtitle": "ゲーム制作・プログラミング学習アーカイブ",
  "tagline": "ゲームを遊んで、コードを見て、ゲーム制作を学ぶ",
  "ideriaOfficialUrl": "",   // ★将来IDERIA公式サイトができたらURLを入れる（空なら非表示）
  "baseUrl": ""
}
```

## Learn（src/content/learn/*.md）

```md
---
title: "当たり判定"
slug: "collision"
order: 5
level: "初級"
summary: "四角形同士がぶつかったかを調べる"
sampleSource: "reverse/01_四角形同士の当たり判定.py"  # 逆引きコードを表示
---
本文（Markdown）
```

## 年度・技術タグ

- 年度ページ・フィルタは games/activities の `year` から**自動集計**（年度マスタ不要）。
- 技術タグ表示名は `site/src/data/tech.json`（id→表示名。未定義idはそのまま表示）。

## 将来のDB移行

全データがJSON（=そのままレコード）。games/activities/categories/organizations の4テーブル＋中間テーブル(game_activities)に1対1で対応する構造のため、将来のDB移行時はJSONをインポートするだけでよい。
