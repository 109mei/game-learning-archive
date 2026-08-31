# WEB_COMPATIBILITY.md — pygame系ゲームのブラウザ対応状況

方式: pygame-ce → **pygbag**（WebAssembly）→ `site/public/play-files/<id>/` に配置し、プレイページ(iframe)から起動。
原則: **元ゲームは一切変更しない**。Web対応の修正は `web_versions/<id>/` のコピーに対して行う。

## 共通の変換ポイント（今回の全作品で確認された事項）

| 事項 | 対応 |
|---|---|
| メインループが同期処理 | `async def main()` 化し、フレーム毎に `await asyncio.sleep(0)` を挿入（pygbag必須要件） |
| `ctypes`（Windows DPI設定等） | Webでは動かないため `sys.platform == "emscripten"` 判定で無効化 |
| mp3音源 | pygbag環境で不安定なため web版では **ogg に変換**して差し替え |
| 日本語フォント（`SysFont` / `Font(None)`） | WASM側にOSフォントが無いため、日本語を描画する作品は **NotoSansJP-Regular.ttf を同梱**して差し替え |
| ハイスコア等のファイル書き込み | ブラウザ内の仮想FSに書かれる（タブを閉じると消える）。注記を表示 |
| メインファイル名 | pygbag要件により `main.py` にリネーム（web版コピーのみ） |
| ファイル名の氏名・文字化け | web版コピーでリネーム（PRIVACY_CHECK.md参照） |

## 作品別の調査結果と状況

状態: ✅=Web版ビルド済み / 🔧=対応可能（未変換） / ⚠=要修正あり / ❌=現状不可

| 作品 | 規模 | 主な論点 | 状態 |
|---|---|---|---|
| ONE（第1回） | 78行・素材なし | 単純ループのみ | 🔧（変換対象） |
| Quick Draw（第1回） | 223行 | ctypes・mp3 | 🔧（OneButtonGames収録版を使用） |
| runaway!（第1回） | 204行 | numpy・Font(None) | 🔧（numpyはpygbag対応可否を実機確認） |
| dodge the bullet（第1回/予備 要確認） | 108行 | 単純 | 🔧 |
| Flappy Bird（第2回） | 176行 | mp3 | 🔧 |
| flappy plane（第2回） | 165行 | mp3 | 🔧 |
| FlyMan（第2回） | 393行 | wav・スコア書込 | 🔧 |
| hurdle（第2回） | 146行 | mp3 | 🔧 |
| indian poker（第2回） | 325行 | ctypes・画像62枚 | 🔧 |
| one_touch_jump_game（第2回） | 106行 | 単純 | 🔧 |
| 2Dgameジャンムー | 245行 | NotoSansJP同梱済・mp3 | 🔧 |
| ELECTRO BEAT（第3回） | - | ソース未ステージ（次回対応） | 🔧（要ソース確認） |
| SwitchQuiz（第3回改良版） | 605行 | ctypes・numpy・mp3 | 🔧 |
| チンチロバトル（第3回改良版） | 404行 | Noto同梱済・mp3 | 🔧 |
| ロボットジャンプ（第3回改良版） | 386行 | ctypes・mp3 | 🔧 |
| 音楽ゲーム（第3回改良版） | 274行 | ctypes・mp3 | 🔧 |
| 時の管理者（純真・追加） | 1866行 | **tkinterのファイルダイアログ使用 → Web不可**。tkinter除去の改修をすればWeb化可能 | ❌（初期版では見送り） |
| 避けろ！（純真・追加） | 861行 | ctypes・numpy・mp3 10本 | 🔧 |
| ORDER_RECALL（九情大） | 441行 | Font(None)・日本語有無要確認 | 🔧 |
| shampoo（九情大） | 830行 | ctypes・mp3 | 🔧 |
| シューティングゲーム（九情大） | 308行 | ctypes・mp3 | 🔧 |
| HILL_RUSH（第4回） | 2087行 | jsonセーブ・mp3・大規模 | 🔧 |
| machahunter（第4回） | 616行 | Font(None)・mp3/wav | 🔧 |
| バレットバニー（第4回） | 2160行 | zip内ファイル名がShift-JIS文字化け → web版で正規化 | 🔧 |
| geem（第4回・ダックハント修正後） | 328行 | 拡張子が `.ph`（.py誤記と推定・要確認）・ogg/wav/mp3混在 | ⚠ 🔧 |
| ダックハント（第4回・修正前） | 204行・素材なし | geemとの対応関係要確認。代表版はgeem側 | 保留 |
| OneButtonGames ランチャー | 6668行 | 収録ゲーム呼び出し型・numpy・大規模。ランチャーのWeb化は工数大 | ❌（初期版では見送り。収録ゲームを個別にWeb化） |
| チョコパキ!（IDERIA） | 3538行 | SysFont("HG創英角ゴシックUB")→Noto差し替え・wav 37本 | 🔧 |
| しまっぴー先生の覚えてクイズ | TyranoScript | pygbag対象外。TyranoScriptのブラウザ書き出しで対応可能（別方式・要確認） | 保留 |
| Scratch 3作品（コンテスト） | Scratch | pygbag対象外。TurboWarp埋め込み等で対応可能（sb3の公開可否要確認） | 保留 |
| Einar build（Unity/UE4） | exe | WebGLビルドはプロジェクトファイルが無いため不可（exeのみ） | ❌ |

## ビルド結果（2026-08-31 実施済み）

**24作品をpygbagでビルドし、ヘッドレスブラウザで起動・スクリーンショットにより動作確認済み。うち23作品をサイトで公開**（dodge the bulletはビルド成功だが写真素材の問題で公開保留）。

| 作品 | 結果 | 実施した変換 |
|---|---|---|
| ONE | ✅公開・動作確認済 | FULLSCREEN解除・async化 |
| Quick Draw | ✅ | mp3→ogg・async化 |
| runaway! | ✅ | 画像パスの `\` → `/`・未使用numpy無効化・async化 |
| dodge the bullet | ⛔ビルド成功・公開保留 | 実在人物の写真素材のため（TODO参照） |
| Flappy Bird | ✅ | mp3→ogg・main関数async化 |
| flappy plane / FlyMan / hurdle / one_touch_jump_game | ✅ | mp3→ogg・async化 |
| indian poker | ⛔ソースのみ公開 | 原作に描画処理が未実装（画面が更新されない） |
| 2Dgameジャンムー | ✅ | mp3→ogg・async化（Notoフォント同梱済みの作品） |
| ELECTRO BEAT | ✅ | SysFont(meiryo)→NotoSansJP同梱・async化 |
| SwitchQuiz / チンチロバトル / ロボットジャンプ / 音楽ゲーム / 避けろ！ | ✅ | ctypes無効化・mp3→ogg・FULLSCREEN解除・ネストしたループのasync化 |
| 時の管理者 | ❌未対応 | tkinter使用（改修すれば対応可能） |
| シューティングゲーム / shampoo | ✅ | ctypes無効化・mp3→ogg・画面遷移関数のasync化 |
| ORDER_RECALL | ✅ | クラスのrun()メソッドをasync化 |
| HILL RUSH | ✅ | async化。セーブ(save_data.json)はブラウザ内のみ・初期化済み |
| machha hunter | ✅ | **pygame.time.set_timer がWASM未対応** → メインループでの手動タイマーに置換 |
| バレットバニー | ✅ | zip内Shift-JISファイル名の正規化・async化 |
| geem | ✅ | 拡張子 .ph → .py・SysFont(リスト指定)→NotoSansJP同梱 |
| チョコパキ! | ✅ | bare FULLSCREEN解除・**大文字拡張子(.PNG)の小文字コピー追加**（WASMのFSは大文字小文字を区別）・SysFont(HG創英角)→Noto・time.sleep→asyncio.sleep |
| OneButtonGamesランチャー | ❌初期版では見送り | 6,668行・収録ゲーム呼び出し型のため（ソースは公開） |

### 今回わかった追加の変換ポイント（今後の作品にも適用）

1. `pygame.time.set_timer` はWASM未対応 → get_ticks による手動タイマーへ置換
2. WindowsのファイルシステムとちがいWASMは**大文字小文字を区別**（.PNG と .png）
3. `from pygame.locals import *` の bare `FULLSCREEN` も解除が必要
4. zipがShift-JISファイル名の場合は展開時に文字コード指定
5. メニュー画面など**tickの無いループにも**毎フレーム `await asyncio.sleep(0)` が必要（無いとブラウザがフリーズ）
6. 未使用でも `import numpy` があると起動しないことがある → 未使用なら無効化

変換は `tools/`（作業時の変換スクリプト）と同等の手作業でも可能。各Web版の冒頭コメントに変更点を記載している。
