# 変換ツール（参考）

pygame-ce作品をWeb対応（pygbag用）に変換する際に使ったスクリプトです。
新しい作品を変換するときの参考にしてください（パスは環境にあわせて書き換えてください）。

- `prep_game.py` … ゲームフォルダのコピー・mp3→ogg変換・main.py生成（単純な1ループ構成向け）
- `wrap_toploop.py` … トップレベルにwhileループがある作品のasync化
- `webify.py` … ネストしたループ・画面遷移関数がある作品の本格変換（ctypes無効化・await挿入など）
- `fix_paths.py` … 素材パスの `\` → `/` 修正

変換の考え方・作品ごとの結果は `../docs/WEB_COMPATIBILITY.md` を参照。
