# coding: utf-8
"""
04_scene_switch.py

メニュー画面とゲーム画面を切り替えるシーン遷移の例です。
メニュー画面では「Enterキーでゲーム開始」と表示し、ゲーム画面では
「Escキーでメニューに戻る」と表示します。
ゲーム画面では簡単なアニメーションとして四角形が左右に移動します。
"""

import sys  # sysモジュールはプラットフォーム判定に利用します
import pygame  # Pygameライブラリを読み込みます
from pygame.locals import *  # QUITやキー定数を直接参照できるようにします
import os  # 環境変数の操作に利用します

# OS別設定（詳細は01のスクリプト参照）
# 各OSでDPIスケールやウィンドウ配置を調整します
if sys.platform == "win32":  # Windowsの場合
    import ctypes  # WindowsのDPI設定変更に使用します
    ctypes.windll.user32.SetProcessDPIAware()  # DPIスケール無効化
    os.environ['SDL_VIDEO_CENTERED'] = '1'  # ウィンドウを中央に配置
elif sys.platform == "darwin":  # macOSの場合
    os.environ['SDL_VIDEO_WINDOW_POS'] = '100,100'  # ウィンドウの左上座標を設定
    os.environ['SDL_VIDEO_CENTERED'] = '1'  # ウィンドウを中央に配置
elif sys.platform.startswith("linux"):  # Linuxの場合
    os.environ['SDL_VIDEO_CENTERED'] = '1'  # Linuxでは中央配置のみ設定
else:  # 上記に該当しないその他のOSの場合
    os.environ['SDL_VIDEO_CENTERED'] = '1'  # その他のOSでも中央配置を設定

# 画面サイズ・フォント設定
W, H = 1280, 720  # 画面の横幅と縦幅を指定します
FONT_PATH = "NotoSansJP-Regular.ttf"  # 日本語フォントファイルのパス
FONT_SIZE = 32  # フォントサイズ（ポイント単位）

pygame.init()  # Pygame全体を初期化します
screen = pygame.display.set_mode((W, H))  # 指定したサイズのウィンドウを生成します
pygame.display.set_caption("04 シーン遷移の例")  # ウィンドウタイトルを設定します

# フォント読み込み
try:  # 指定したフォントファイルを読み込みます
    font = pygame.font.Font(FONT_PATH, FONT_SIZE)  # 指定した日本語フォントを読み込みます
except IOError:  # フォントが見つからない場合の処理
    font = pygame.font.SysFont(None, FONT_SIZE)  # フォントが見つからない場合はデフォルトフォントを使用します

# ゲーム状態の変数
scene = 'menu'  # 現在のシーンを表します（'menu' または 'game'）
rect_x = 100  # ゲーム画面で動く四角形のx座標の初期値
rect_speed = 4  # 四角形が1フレームで移動する速度（ピクセル）


clock = pygame.time.Clock()  # FPS制御のためのClockオブジェクトを生成
running = True  # メインループ継続フラグ
while running:  # メインループ開始
    clock.tick(60)  # ループを秒間60回に制限します
    for event in pygame.event.get():  # イベントキューからイベントを取得
        if event.type == QUIT:  # ウィンドウの閉じるボタンが押された場合
            running = False  # ループを終了させます
        elif event.type == KEYDOWN:  # キーボードが押された場合
            if scene == 'menu' and event.key == K_RETURN:  # メニューシーンでEnterが押された場合
                scene = 'game'  # Enterキーでゲーム画面に切り替えます
            elif scene == 'game' and event.key == K_ESCAPE:  # ゲームシーンでEscが押された場合
                scene = 'menu'  # Escキーでメニュー画面に戻ります

    # シーンによって処理を分岐
    if scene == 'menu':  # メニュー画面の場合
        # メニュー画面の描画
        screen.fill((240, 240, 240))  # 明るい背景色で塗りつぶします
        title = font.render("メニュー画面", True, (0, 0, 0))  # タイトル文字列をレンダリングします（色は黒）
        prompt = font.render("Enterキーでゲーム開始", True, (50, 50, 50))  # ガイド文字列をレンダリングします（色はグレー）
        # テキストを画面中央付近に描画
        screen.blit(title, ((W - title.get_width()) // 2, H // 3))  # タイトル文字を中央寄せで描画
        screen.blit(prompt, ((W - prompt.get_width()) // 2, H // 2))  # プロンプト文字を中央寄せで描画
    elif scene == 'game':  # ゲーム画面の場合
        # ゲーム画面の更新処理
        screen.fill((220, 230, 255))  # 淡い青色で背景を塗りつぶします
        # 四角形を左右に移動します
        rect_x += rect_speed  # x座標に速度を加算して移動させます
        # 画面端に到達したら移動方向を反転します
        if rect_x <= 0 or rect_x + 100 >= W:  # 左端または右端に当たったかを判定します
            rect_speed = -rect_speed  # 移動方向を逆にします
        # 四角形の描画: Rect(left, top, width, height)を指定し角丸を設定
        pygame.draw.rect(screen, (100, 180, 250), pygame.Rect(rect_x, H//2 - 50, 100, 100), border_radius=10)  # 四角形を描画します
        # ガイドテキストの生成
        guide = font.render("Escキーでメニューに戻る", True, (0, 0, 0))  # Escキーでメニューに戻る案内を描画用Surfaceに変換
        # 画面左上にガイドを描画
        screen.blit(guide, (20, 20))  # ガイドテキストをウィンドウ左上に描画

    pygame.display.flip()  # 画面全体を更新して描画内容を表示します

pygame.quit()  # Pygameのリソースを解放して終了します