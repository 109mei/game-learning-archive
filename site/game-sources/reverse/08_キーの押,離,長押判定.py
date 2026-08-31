# coding: utf-8
"""
08_key_press_release_long.py

キー押下/離上/長押しの検出例です。Spaceキーを対象に、
押した瞬間、離した瞬間、一定時間以上押し続けた場合の３種類のイベントを検出します。
"""

import sys  # sysモジュールはプラットフォーム判定に使用します
import pygame  # Pygameライブラリを読み込みます
from pygame.locals import *  # キー定数やQUITイベントを直接参照できるようにします
import os  # 環境変数設定に使用します

# OS設定
# 各プラットフォームでDPIスケールやウィンドウ配置を調整します
if sys.platform == "win32":  # Windowsの場合
    import ctypes  # WindowsのAPI呼び出し用
    ctypes.windll.user32.SetProcessDPIAware()  # DPIスケールを無効にします
    os.environ['SDL_VIDEO_CENTERED'] = '1'  # ウィンドウを中央に配置します
else:  # Windows以外の場合
    os.environ['SDL_VIDEO_CENTERED'] = '1'  # ウィンドウを中央に配置します

W, H = 1280, 720  # 画面の幅と高さ
FONT_PATH = "NotoSansJP-Regular.ttf"  # 日本語フォントのパス
FONT_SIZE = 36  # フォントサイズ

pygame.init()  # Pygameを初期化します
screen = pygame.display.set_mode((W, H))  # 指定サイズの画面を生成します
pygame.display.set_caption("08 キー押下/離上/長押し")  # ウィンドウタイトルを設定します

try:  # フォント読み込みを試みます
    font = pygame.font.Font(FONT_PATH, FONT_SIZE)  # 指定フォントを読み込みます
except IOError:  # フォントが読み込めない場合に実行されます
    font = pygame.font.SysFont(None, FONT_SIZE)  # フォントが読み込めない場合はデフォルトフォントを使用します

# 状態管理
is_pressed = False  # スペースキーが押されているかどうか
press_time = 0  # キーを押している時間をミリ秒単位で保持します
LONG_PRESS_THRESHOLD = 1000  # 長押しと判定する閾値 (ミリ秒)

clock = pygame.time.Clock()  # FPS制御用のClockオブジェクトを作成
running = True  # メインループ継続フラグ
message = "Spaceキーを押してください"  # 初期メッセージ
while running:  # メインループ開始
    dt = clock.tick(60)  # 前フレームからの経過時間(ミリ秒)を取得し、60FPSに制限
    for event in pygame.event.get():  # イベントキューからイベントを取得
        if event.type == QUIT:  # ウィンドウの×ボタンが押された場合
            running = False  # ループを終了します
        elif event.type == KEYDOWN and event.key == K_SPACE:  # スペースキーが押された瞬間
            # キーを押した瞬間の処理
            is_pressed = True  # 押下状態にする
            press_time = 0  # 押し時間をリセット
            message = "押しました!"  # 押した瞬間のメッセージを設定
        elif event.type == KEYUP and event.key == K_SPACE:  # スペースキーが離された瞬間
            # キーを離した瞬間の処理
            is_pressed = False  # 押下状態を解除
            message = "離しました!"  # 離した瞬間のメッセージを設定

    # 長押し判定
    if is_pressed:  # キーが押されている場合
        press_time += dt  # 経過時間を加算
        if press_time >= LONG_PRESS_THRESHOLD:  # 閾値を超えたら長押しと判定
            message = "長押し中..."  # 長押し中のメッセージを設定

    # 描画処理
    screen.fill((255, 255, 255))  # 画面を白で塗りつぶします
    text_surface = font.render(message, True, (0, 0, 0))  # 状態メッセージをレンダリングします
    screen.blit(text_surface, ((W - text_surface.get_width()) // 2, H // 2))  # メッセージを画面中央に描画します
    guide = font.render("Spaceキーの押下/離上/長押しを試してみてください", True, (50, 50, 50))  # ガイドメッセージをレンダリングします
    screen.blit(guide, ((W - guide.get_width()) // 2, H // 2 + 60))  # ガイドをその下に描画します
    pygame.display.flip()  # 画面を更新して描画内容を表示します

# ループ終了後にPygameを終了します
pygame.quit()  # Pygameのリソースを解放して終了します