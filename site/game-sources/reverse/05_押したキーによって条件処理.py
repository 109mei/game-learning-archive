# coding: utf-8
"""
05_conditional_logic.py

条件分岐(if/else)による処理切り替えの例です。
左矢印キーを押すと背景がピンクになり「左が押されました」と表示、
右矢印キーを押すと背景がライトグリーンになり「右が押されました」と表示します。
どちらも押されていない場合はデフォルトの背景色とテキストを表示します。
"""

import sys  # sysモジュールはプラットフォーム情報取得に使用します
import pygame  # Pygameライブラリを読み込みます
from pygame.locals import *  # QUITやキー定数を直接参照できるようにします
import os  # 環境変数設定に使用します

# OS設定
# 各プラットフォームでDPIスケールやウィンドウ位置を調整します
if sys.platform == "win32":  # Windowsの場合
    import ctypes  # Windows API 呼び出し用
    ctypes.windll.user32.SetProcessDPIAware()  # DPIスケールを無効化します
    os.environ['SDL_VIDEO_CENTERED'] = '1'  # ウィンドウを中央に配置します
elif sys.platform == "darwin":  # macOSの場合
    os.environ['SDL_VIDEO_CENTERED'] = '1'  # ウィンドウを中央に配置します
elif sys.platform.startswith("linux"):  # Linuxの場合
    os.environ['SDL_VIDEO_CENTERED'] = '1'  # ウィンドウを中央に配置します
else:  # 上記に該当しないその他のOSの場合
    os.environ['SDL_VIDEO_CENTERED'] = '1'  # その他のOSでも中央配置します

# 画面とフォント設定
W, H = 1280, 720  # 画面の横幅と縦幅を指定します
FONT_PATH = "NotoSansJP-Regular.ttf"  # 日本語フォントのパス
FONT_SIZE = 36  # フォントサイズ

pygame.init()  # Pygameを初期化します
screen = pygame.display.set_mode((W, H))  # 指定したサイズのウィンドウを生成します
pygame.display.set_caption("05 条件分岐の例")  # ウィンドウタイトルを設定します

# フォント
try:  # 指定したフォントファイルを読み込みます
    font = pygame.font.Font(FONT_PATH, FONT_SIZE)  # 指定したフォントを読み込みます
except IOError:  # フォントが見つからない場合の処理
    font = pygame.font.SysFont(None, FONT_SIZE)  # フォントが見つからない場合はデフォルトフォントを使用します

# 色定義
DEFAULT_BG = (240, 240, 240)  # デフォルト背景色（グレー）
LEFT_BG = (255, 200, 220)  # 左キーを押したときの背景色（ピンク）
RIGHT_BG = (200, 255, 210)  # 右キーを押したときの背景色（ライトグリーン）

clock = pygame.time.Clock()  # FPS制御用のClockオブジェクトを生成します
running = True  # メインループ継続フラグ
while running:  # ゲームループを開始します
    clock.tick(60)  # 1秒間に60フレームに制限します
    for event in pygame.event.get():  # イベントキューからイベントを処理します
        if event.type == QUIT:  # ウィンドウの×ボタンが押された場合
            running = False  # ループを終了させます

    keys = pygame.key.get_pressed()  # 押されているキーの状態を取得します
    # 条件分岐: 左右キーの状態を判定
    if keys[K_LEFT]:  # 左キーが押されている場合
        bg_color = LEFT_BG  # 背景をピンク色に変更
        message = "左が押されました"  # 表示するメッセージ
    elif keys[K_RIGHT]:  # 右キーが押されている場合
        bg_color = RIGHT_BG  # 背景をライトグリーンに変更
        message = "右が押されました"  # 表示するメッセージ
    else:  # どちらのキーも押されていない場合
        bg_color = DEFAULT_BG  # デフォルトの背景色に戻す
        message = "左右の矢印キーを押してください"  # 操作を促すメッセージ

    # 背景塗りつぶし
    screen.fill(bg_color)  # 背景色で画面を塗りつぶします
    # テキスト描画
    text_surface = font.render(message, True, (0, 0, 0))  # メッセージをSurfaceに描画します
    screen.blit(text_surface, ((W - text_surface.get_width()) // 2, H // 2))  # 画面中央にテキストを表示

    pygame.display.flip()  # 画面を更新して描画内容を表示します

# メインループを終了したらPygameを終了します
pygame.quit()  # 初期化したPygameのリソースを解放して終了します