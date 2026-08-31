# coding: utf-8
"""
07_rect_button.py

矩形ボタンの例です。ボタンはホバーすると色が変わり、クリックすると反応を表示します。
画像ではなく単純な矩形でボタンを構成し、色やクリック判定の基本を学びます。
"""

import sys  # sysモジュールはプラットフォーム判定に使用します
import pygame  # Pygameライブラリを読み込みます
from pygame.locals import *  # マウスやキーボードの定数を直接参照できるようにします
import os  # 環境変数設定に使用します

# OS設定
# 各OSで適切にDPIスケール無効化やウィンドウ配置を行います
if sys.platform == "win32":  # Windowsの場合
    import ctypes  # Windows API呼び出し用
    ctypes.windll.user32.SetProcessDPIAware()  # DPIスケールを無効にします
    os.environ['SDL_VIDEO_CENTERED'] = '1'  # ウィンドウを中央に配置します
else:  # Windows以外の場合
    os.environ['SDL_VIDEO_CENTERED'] = '1'  # ウィンドウを中央に配置します

W, H = 1280, 720  # 画面の幅と高さを指定します
FONT_PATH = "NotoSansJP-Regular.ttf"  # 日本語フォントのパス
FONT_SIZE = 32  # フォントサイズを指定します

pygame.init()  # Pygameを初期化します
screen = pygame.display.set_mode((W, H))  # 指定サイズのウィンドウを作成します
pygame.display.set_caption("07 矩形ボタン")  # ウィンドウタイトルを設定します

# フォント読み込み
try:  # フォント読み込みを試みます
    font = pygame.font.Font(FONT_PATH, FONT_SIZE)  # 指定フォントを読み込みます
except IOError:  # フォントが見つからない場合に実行されます
    font = pygame.font.SysFont(None, FONT_SIZE)  # フォントが見つからない場合はデフォルトフォントを使用します

# ボタン定義
button_rect = pygame.Rect(0, 0, 250, 100)  # ボタン用の矩形を作成します(左上x, 左上y, 幅, 高さ)
button_rect.center = (W // 2, H // 2)  # ボタンを画面中央に配置します
color_normal = (180, 220, 180)  # 通常状態のボタン色
color_hover = (140, 200, 140)  # ホバー時に使用するボタン色
color_click = (100, 180, 100)  # クリック時に使用するボタン色

clicked = False  # ボタンがクリックされたかどうかのフラグ
clock = pygame.time.Clock()  # FPS制御用のClockオブジェクトを作成
running = True  # メインループ継続フラグ
while running:  # メインループを開始します
    clock.tick(60)  # 1秒間に60回までループを実行します
    for event in pygame.event.get():  # イベントキューからイベントを取得
        if event.type == QUIT:  # ウィンドウの×ボタンが押された場合
            running = False  # ループを終了します
        elif event.type == MOUSEBUTTONDOWN and event.button == 1:  # 左マウスボタンが押された場合
            if button_rect.collidepoint(event.pos):  # クリック位置がボタン内か判定します
                clicked = True  # ボタンがクリックされたことを記録します

    # マウスの状態
    mouse_pos = pygame.mouse.get_pos()  # マウスカーソルの現在位置を取得します
    hovering = button_rect.collidepoint(mouse_pos)  # カーソルがボタンの上に乗っているか判定します

    # 色の選択
    if clicked:  # ボタンがクリック状態の場合
        current_color = color_click  # クリック時の色を選びます
    elif hovering:  # ボタンにホバーしている場合
        current_color = color_hover  # ホバー時の色を選びます
    else:  # それ以外の場合
        current_color = color_normal  # 通常時の色を選びます

    screen.fill((245, 245, 245))  # 背景を薄いグレーで塗りつぶします
    # ボタンを描画
    pygame.draw.rect(screen, current_color, button_rect, border_radius=10)  # 塗りつぶした矩形を描画します
    # ボタンの枠線
    pygame.draw.rect(screen, (100, 100, 100), button_rect, 2, border_radius=10)  # ボタンの外枠を描画します
    # ボタンラベル
    label = font.render("クリック", True, (0, 0, 0))  # ラベルテキストを生成します
    screen.blit(label, ((button_rect.centerx - label.get_width() // 2), (button_rect.centery - label.get_height() // 2)))  # ラベルをボタンの中央に描画します

    # クリック後のメッセージ
    if clicked:  # ボタンがクリックされている場合
        msg = font.render("ボタンが押されました！", True, (200, 60, 60))  # メッセージを生成します
        screen.blit(msg, (W//2 - msg.get_width()//2, button_rect.bottom + 20))  # ボタンの下にメッセージを表示します

    # ガイドテキスト
    guide = font.render("矩形ボタンをクリックしてみてください。", True, (0, 0, 0))  # ガイドテキストを生成します
    screen.blit(guide, (30, H - 50))  # 画面下部にガイドテキストを描画します

    pygame.display.flip()  # 画面を更新して描画内容を表示します

# ループ終了後にPygameを終了します
pygame.quit()  # Pygameのリソースを解放して終了します