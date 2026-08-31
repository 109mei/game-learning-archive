# coding: utf-8
"""
06_image_button.py

画像を使ったボタンの例です。マウスカーソルがボタン上に乗ると枠線の色が変わり、
クリックするとメッセージが表示されます。IMAGE_PATH にボタン画像のパスを設定してください。
"""

import sys  # sysモジュールはプラットフォーム判定に利用します
import pygame  # Pygameライブラリを読み込みます
from pygame.locals import *  # QUITやマウスイベント定数を直接参照できるようにします
import os  # 環境変数設定に使用します

# OS設定 (詳細は01参照)
# 各OSでDPIスケールやウィンドウ位置を適切に設定します
if sys.platform == "win32":  # Windowsの場合
    import ctypes  # Windows APIを呼び出すためのctypes
    ctypes.windll.user32.SetProcessDPIAware()  # 高DPI環境でのスケーリングを無効にします
    os.environ['SDL_VIDEO_CENTERED'] = '1'  # ウィンドウを中央に配置します
else:  # Windows以外の場合
    # Windows以外の場合はウィンドウを中央に配置するだけです
    os.environ['SDL_VIDEO_CENTERED'] = '1'  # ウィンドウを中央に配置します

W, H = 1280, 720  # 画面サイズの幅と高さ
FONT_PATH = "NotoSansJP-Regular.ttf"  # 日本語フォントのパス
FONT_SIZE = 28  # フォントサイズ
# ボタン用画像ファイルのパス。後で変更する場合はこの変数を修正してください
IMAGE_PATH = "../素材/オブジェクト・UI/101.png"  # ボタン画像ファイルのパスを指定します

pygame.init()  # Pygameを初期化します
screen = pygame.display.set_mode((W, H))  # ウィンドウを作成します
pygame.display.set_caption("06 画像ボタン")  # ウィンドウタイトルを設定します

try:  # 指定されたフォントファイルの読み込みを試みます
    font = pygame.font.Font(FONT_PATH, FONT_SIZE)  # 指定されたフォントを読み込みます
except IOError:  # フォントファイルが読み込めなかった場合
    font = pygame.font.SysFont(None, FONT_SIZE)  # フォントが読み込めない場合はデフォルトフォントを使用します

# 画像読み込み
try:  # ボタン画像の読み込みを試みます
    button_img = pygame.image.load(IMAGE_PATH).convert_alpha()  # ボタン画像を読み込みアルファ付きSurfaceに変換します
except Exception as e:  # 画像が読み込めない場合の例外処理
    print(f"ボタン画像を読み込めません: {e}")  # 読み込みに失敗した場合のエラーメッセージ
    button_img = pygame.Surface((200, 80), pygame.SRCALPHA)  # 代用Surfaceを作成します
    button_img.fill((180, 180, 250, 255))  # 紫色で塗りつぶします


# ボタン位置と矩形
btn_rect = button_img.get_rect()  # ボタン画像の矩形領域を取得します
btn_rect.center = (W // 2, H // 2)  # 矩形の中心を画面中央に設定します

clicked = False  # ボタンがクリックされたかどうかを示すフラグ
clock = pygame.time.Clock()  # フレームレート制御用のClockオブジェクト
running = True  # メインループ継続フラグ
while running:  # メインループを開始します
    clock.tick(60)  # 1秒間に60回までループを実行します
    for event in pygame.event.get():  # イベントキューからイベントを取得します
        if event.type == QUIT:  # ウィンドウの閉じるボタンが押された場合
            running = False  # ループを終了します
        elif event.type == MOUSEBUTTONDOWN and event.button == 1:  # 左クリックが押された場合
            if btn_rect.collidepoint(event.pos):  # マウスクリック位置がボタン上か判定します
                clicked = True  # ボタンがクリックされたと記録します

    # マウスカーソル位置を取得
    mouse_pos = pygame.mouse.get_pos()  # 現在のマウス座標を取得します
    hovering = btn_rect.collidepoint(mouse_pos)  # カーソルがボタン上にあるかどうか

    screen.fill((255, 255, 255))  # 背景を白で塗りつぶします
    # ボタン描画
    screen.blit(button_img, btn_rect.topleft)  # ボタン画像を矩形の位置に描画します
    # ホバー時の枠を描画
    border_color = (50, 150, 250) if hovering else (150, 150, 150)  # ホバー時は青色、通常時はグレー
    pygame.draw.rect(screen, border_color, btn_rect, 3, border_radius=10)  # ボタンの周囲に枠線を描画します

    # メッセージ表示
    if clicked:  # クリックされた場合
        msg = font.render("ボタンがクリックされました！", True, (200, 50, 50))  # メッセージを生成します
        screen.blit(msg, ((W - msg.get_width()) // 2, btn_rect.bottom + 20))  # ボタンの下にメッセージを描画します

    # 説明テキスト
    info = font.render("画像ボタンにカーソルを合わせクリックしてみてください", True, (0, 0, 0))  # ガイドテキストを生成します
    screen.blit(info, (30, H - 50))  # 画面下部にガイドテキストを描画します

    pygame.display.flip()  # 画面を更新して描画内容を表示します

# ループ終了後にPygameを終了します
pygame.quit()  # Pygameのリソースを解放して終了します