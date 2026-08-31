# coding: utf-8
"""
09_mouse_follow.py

マウスの座標に追従する円の例です。マウスを動かすと円がその位置に表示されます。
追加でマウス座標を画面に表示して位置が確認できるようにしています。
"""

import sys  # sysモジュールはプラットフォーム判定に使用します
import pygame  # Pygameライブラリを読み込みます
from pygame.locals import *  # キーやQUIT定数を直接参照できるようにします
import os  # 環境変数設定に使用します

# OS設定
# 各プラットフォームでDPIスケールやウィンドウ配置を調整します
if sys.platform == "win32":  # Windowsの場合
    import ctypes  # Windows API呼び出し用
    ctypes.windll.user32.SetProcessDPIAware()  # DPIスケーリングを無効にします
    os.environ['SDL_VIDEO_CENTERED'] = '1'  # ウィンドウを中央に配置します
else:  # Windows以外の場合
    os.environ['SDL_VIDEO_CENTERED'] = '1'  # ウィンドウを中央に配置します

W, H = 1280, 720  # 画面の幅と高さ
FONT_PATH = "NotoSansJP-Regular.ttf"  # 日本語フォントのパス
FONT_SIZE = 24  # フォントサイズ

pygame.init()  # Pygameを初期化します
screen = pygame.display.set_mode((W, H))  # 指定サイズで画面を生成します
pygame.display.set_caption("09 マウス追従")  # ウィンドウタイトルを設定します

try:  # フォント読み込みを試みます
    font = pygame.font.Font(FONT_PATH, FONT_SIZE)  # 指定フォントを読み込みます
except IOError:  # フォントが見つからない場合に実行されます
    font = pygame.font.SysFont(None, FONT_SIZE)  # フォントが見つからない場合はデフォルトフォントを使用します

clock = pygame.time.Clock()  # FPS制御用のClockオブジェクトを作成
running = True  # メインループ継続フラグ
while running:  # メインループ開始
    clock.tick(60)  # 1秒間に60フレームまで処理します
    for event in pygame.event.get():  # イベントキューからイベントを取得します
        if event.type == QUIT:  # ウィンドウの閉じるボタンが押された場合
            running = False  # ループを終了します

    # マウスの現在位置を取得
    mx, my = pygame.mouse.get_pos()  # マウスカーソルの座標を取得します

    screen.fill((255, 255, 255))  # 背景を白色で塗りつぶします
    # マウス位置に円を描画
    pygame.draw.circle(screen, (200, 100, 100), (mx, my), 30)  # 指定位置に赤色の円を描画します
    # 座標表示
    coord_text = font.render(f"座標: ({mx}, {my})", True, (0, 0, 0))  # 現在の座標を文字列にして描画用Surfaceに変換
    screen.blit(coord_text, (10, 10))  # 座標テキストを左上に表示
    guide = font.render("マウスを動かすと円が追従します", True, (0, 0, 0))  # ガイドテキストを生成します
    screen.blit(guide, (10, 40))  # ガイドテキストをその下に表示
    pygame.display.flip()  # 画面を更新して描画内容を表示します

# ループ終了後にPygameを終了します
pygame.quit()  # Pygameのリソースを解放して終了します