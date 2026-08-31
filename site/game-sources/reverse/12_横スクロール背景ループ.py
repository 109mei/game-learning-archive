# coding: utf-8
"""
12_side_scroll.py

2D横スクロールの基礎を示す例です。背景を一定速度で左へ流し、
2枚の背景を交互に再配置することで無限にスクロールしているように見せます。
本例では単色の矩形を背景として使用しますが、画像に置き換えることも可能です。
"""

import sys  # sysモジュールはプラットフォーム判定に使用します
import pygame  # Pygameライブラリを読み込みます
from pygame.locals import *  # キーやQUIT定数を直接参照できるようにします
import os  # 環境変数設定に使用します

# OS設定
# 各プラットフォームでDPIスケール無効化やウィンドウ位置を調整します
if sys.platform == "win32":  # Windows環境の場合
    import ctypes  # Windows API呼び出し用
    ctypes.windll.user32.SetProcessDPIAware()  # DPIスケーリングを無効にします
    os.environ['SDL_VIDEO_CENTERED'] = '1'  # ウィンドウを中央に配置します
else:  # Windows以外の場合
    os.environ['SDL_VIDEO_CENTERED'] = '1'  # ウィンドウを中央に配置します

W, H = 1280, 720  # 画面の幅と高さ
FONT_PATH = "NotoSansJP-Regular.ttf"  # 日本語フォントのパス
FONT_SIZE = 28  # フォントサイズ

pygame.init()  # Pygameを初期化します
screen = pygame.display.set_mode((W, H))  # 指定サイズのウィンドウを作成します
pygame.display.set_caption("12 横スクロール")  # ウィンドウタイトルを設定します

try:  # フォント読み込みを試みます
    font = pygame.font.Font(FONT_PATH, FONT_SIZE)  # 指定フォントを読み込みます
except IOError:  # フォントが見つからない場合に実行されます
    font = pygame.font.SysFont(None, FONT_SIZE)  # フォントが見つからない場合はデフォルトフォントを使用します

# 背景サーフェスの作成（ここでは単色矩形）
bg1 = pygame.Surface((W, H))  # 背景1用のSurfaceを作成します
bg1.fill((100, 150, 250))  # 空の色を設定します
bg2 = pygame.Surface((W, H))  # 背景2用のSurfaceを作成します
bg2.fill((120, 160, 255))  # 2枚目の背景色を設定します

bg_x1 = 0  # 背景1のx位置
bg_x2 = W  # 背景2のx位置（右に配置）
scroll_speed = 5  # スクロール速度（ピクセル/フレーム）

clock = pygame.time.Clock()  # FPS制御用のClockオブジェクトを作成します
running = True  # メインループ継続フラグ
while running:  # メインループ開始
    clock.tick(60)  # 1秒間に60フレームに制限します
    for event in pygame.event.get():  # イベントキューからイベントを取得
        if event.type == QUIT:  # ウィンドウの×ボタンが押された場合
            running = False  # ループを終了します

    # 背景の移動
    bg_x1 -= scroll_speed  # 背景1を左へ移動
    bg_x2 -= scroll_speed  # 背景2を左へ移動
    # 背景が画面外に出たら右端に再配置
    if bg_x1 <= -W:  # 背景1が画面の左端を完全に通過した場合
        bg_x1 = bg_x2 + W  # 背景1を背景2の右側に再配置
    if bg_x2 <= -W:  # 背景2が画面の左端を完全に通過した場合
        bg_x2 = bg_x1 + W  # 背景2を背景1の右側に再配置

    # 描画順序：後ろにあるほど先に描画
    screen.blit(bg1, (bg_x1, 0))  # 背景1を描画
    screen.blit(bg2, (bg_x2, 0))  # 背景2を描画

    # ガイドテキスト
    txt = font.render("横スクロールの例 - 背景が連続して流れます", True, (0, 0, 0))  # 説明文を生成
    screen.blit(txt, (20, 20))  # テキストを画面左上に描画

    pygame.display.flip()  # 画面を更新して描画内容を表示します

# ループ終了後にPygameを終了します
pygame.quit()  # Pygameのリソースを解放して終了します