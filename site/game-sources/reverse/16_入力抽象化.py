# coding: utf-8
"""
16_input_abstraction.py

押下/離上/長押しを抽象化する簡易クラスの例です。InputKeyクラスは特定のキーの状態を管理し、
press(押した瞬間)、release(離した瞬間)、hold(長押し中)を取得できます。
Spaceキーを対象に動作を可視化します。
"""

import sys  # sysモジュールはプラットフォーム判定に使用します
import pygame  # ゲームライブラリPygameを読み込みます
from pygame.locals import *  # キー定数やQUITイベントを直接参照できるようにします
import os  # 環境変数設定に使用します

# OS設定
# WindowsではDPIスケール無効化とウィンドウ位置の調整を行います
if sys.platform == "win32":  # Windows環境の場合
    import ctypes  # Windows APIを呼び出すためのモジュール
    ctypes.windll.user32.SetProcessDPIAware()  # DPIスケーリングを無効にします
    os.environ['SDL_VIDEO_CENTERED'] = '1'  # ウィンドウを中央に配置します
else:  # Windows以外のOSの場合
    os.environ['SDL_VIDEO_CENTERED'] = '1'  # ウィンドウを中央に配置します

W, H = 1280, 720  # 画面の幅と高さを指定します
FONT_PATH = "NotoSansJP-Regular.ttf"  # 日本語フォントのパス
FONT_SIZE = 30  # フォントサイズを指定します

pygame.init()  # Pygameの各モジュールを初期化します
screen = pygame.display.set_mode((W, H))  # 指定サイズのウィンドウを作成します
pygame.display.set_caption("16 入力抽象化クラス")  # ウィンドウタイトルを設定します

try:  # フォント読み込みを試みます
    font = pygame.font.Font(FONT_PATH, FONT_SIZE)  # 指定フォントを読み込みます
except IOError:  # フォントが読み込めない場合に実行されます
    font = pygame.font.SysFont(None, FONT_SIZE)  # デフォルトフォントを使用します

# 押下/離上/長押しを追跡するための変数を準備します
# Spaceキーに限定した状態管理にするため、クラスは使用しません。
space_key_code = K_SPACE  # 監視するキーコード
space_long_threshold = 800  # 長押しと判定する閾値(ms)
space_is_down = False  # 現在キーが押されているかどうか
space_time_down = 0  # キーを押している時間の累計(ms)
space_press = False  # 今フレームで押した瞬間かどうか
space_release = False  # 今フレームで離した瞬間かどうか
space_hold = False  # 長押し状態かどうか

clock = pygame.time.Clock()  # FPS制御用のClockオブジェクトを作成します
running = True  # メインループ継続フラグ
while running:  # メインループ開始
    dt = clock.tick(60)  # 前フレームからの経過時間(ms)を取得し、60FPSに制限します
    for event in pygame.event.get():  # イベントキューからイベントを取得
        if event.type == QUIT:  # ウィンドウの×ボタンが押された場合
            running = False  # ループを終了します
    # 毎フレームの状態をリセット
    space_press = False  # 押した瞬間フラグをリセットします
    space_release = False  # 離した瞬間フラグをリセットします
    space_hold = False  # 長押しフラグをリセットします
    # キー状態取得
    keys = pygame.key.get_pressed()  # 押されているキーの状態リストを取得します
    if keys[space_key_code]:  # Spaceキーが押されている場合
        if not space_is_down:  # まだ押されていなかった場合
            space_press = True  # まだ押されていなければ押した瞬間を記録します
            space_time_down = 0  # 押している時間をリセットします
            space_is_down = True  # 押下状態を更新します
        else:  # 既に押されている場合
            # 押され続けている場合は時間を加算します
            space_time_down += dt  # 経過時間を加算します
            if space_time_down >= space_long_threshold:  # 閾値を超えたか判定します
                space_hold = True  # 長押しと判定します
    else:  # Spaceキーが押されていない場合
        # キーが離された場合
        if space_is_down:  # 直前まで押されていたかどうか
            space_release = True  # 離した瞬間を記録します
        space_is_down = False  # 押下状態を解除します
        space_time_down = 0  # 押していた時間をリセットします
    # 表示するメッセージを生成します
    if space_press:  # 押した瞬間フラグが立っている場合
        msg = "Press (押した瞬間)"  # 押した瞬間のメッセージ
    elif space_hold:  # 長押しフラグが立っている場合
        msg = "Hold (長押し中)"  # 長押し中のメッセージ
    elif space_release:  # 離した瞬間フラグが立っている場合
        msg = "Release (離した瞬間)"  # 離した瞬間のメッセージ
    else:  # それ以外の場合
        msg = "待機中"  # 何もしていないときのメッセージ
    # 描画
    screen.fill((250, 250, 250))  # 背景を白で塗りつぶします
    title = font.render("Spaceキーの状態を抽象化", True, (0, 0, 0))  # タイトルテキストを生成します
    screen.blit(title, (20, 20))  # タイトルを画面に描画します
    status = font.render(msg, True, (50, 50, 200))  # 状態メッセージを生成します
    screen.blit(status, (20, 80))  # 状態メッセージを描画します
    guide = font.render("Spaceキーを押してみてください", True, (0, 0, 0))  # ガイドテキストを生成します
    screen.blit(guide, (20, 130))  # ガイドテキストを描画します
    pygame.display.flip()  # 画面を更新して描画内容を表示します

pygame.quit()  # Pygameのリソースを解放して終了します