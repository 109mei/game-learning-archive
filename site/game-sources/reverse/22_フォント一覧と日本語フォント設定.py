# coding: utf-8
"""
22_fonts_listing.py

日本語フォントの設定と利用可能なフォント名の一覧を表示する例です。FONT_PATH に指定した
NotoSansJP を使用して日本語テキストを描画し、pygame.font.get_fonts() により利用可能な
フォント名のリストを一部表示します。
"""

import sys  # sysモジュールはプラットフォーム判定に使用します
import pygame  # Pygameライブラリを読み込みます
from pygame.locals import *  # QUITイベントなどの定数を直接参照できるようにします
import os  # 環境変数の設定に使用します

# ---------- OS設定 ----------
# 各OSでのDPIスケーリングとウィンドウ配置を調整します
if sys.platform == "win32":  # Windows環境の場合
    import ctypes  # Windows API呼び出し用モジュール
    ctypes.windll.user32.SetProcessDPIAware()  # DPIスケーリングを無効にします
    os.environ['SDL_VIDEO_CENTERED'] = '1'  # ウィンドウを中央に配置します
else:  # Windows以外のOSの場合
    os.environ['SDL_VIDEO_CENTERED'] = '1'  # ウィンドウを中央に配置します

W, H = 1280, 720  # 画面の幅(W)と高さ(H)を指定します
FONT_PATH = "NotoSansJP-Regular.ttf"  # 使用する日本語フォントファイルのパス
FONT_SIZE = 32  # フォントサイズを指定します

pygame.init()  # Pygameを初期化します
screen = pygame.display.set_mode((W, H))  # 指定サイズのウィンドウを作成します
pygame.display.set_caption("22 日本語フォント設定＆フォント一覧")  # ウィンドウタイトルを設定します

# 日本語フォント読み込み
try:  # 指定したフォントを読み込みます
    jp_font = pygame.font.Font(FONT_PATH, FONT_SIZE)  # 日本語フォントオブジェクトを生成
except IOError:  # 読み込めない場合は
    jp_font = pygame.font.SysFont(None, FONT_SIZE)  # デフォルトフォントを使用します
    print("指定した日本語フォントが見つかりません。デフォルトフォントを使用します。")  # 警告を表示

# 利用可能なフォント名の取得
fonts = pygame.font.get_fonts()  # 利用可能なフォント名のリスト（小文字）
fonts_sorted = sorted(set(fonts))  # 重複を除去し、アルファベット順にソート

clock = pygame.time.Clock()  # FPS制御用のClockオブジェクト
running = True  # メインループ継続フラグ
while running:  # メインループ
    clock.tick(60)  # 1秒間に60回までループを実行します
    for event in pygame.event.get():  # イベントキューからイベントを取得
        if event.type == QUIT:  # ウィンドウの×ボタンが押された場合
            running = False  # ループを終了します

    screen.fill((240, 240, 240))  # 背景を明るいグレーで塗りつぶします
    # 日本語テキスト表示
    jp_text = jp_font.render("これは日本語フォントのテストです", True, (50, 50, 50))  # テスト用の日本語文字列を描画
    screen.blit(jp_text, (20, 20))  # 画面に描画します
    # フォント名の表示
    header = jp_font.render("利用可能なフォント名の一部:", True, (0, 0, 0))  # 見出しを生成
    screen.blit(header, (20, 80))  # 見出しを描画
    # 最初の10件を表示
    for i, fname in enumerate(fonts_sorted[:10]):  # 最初の10件を列挙
        name_surface = jp_font.render(fname, True, (30, 30, 30))  # フォント名を描画するSurfaceを作成
        screen.blit(name_surface, (40, 120 + i * 30))  # 一覧として縦に並べて表示
    pygame.display.flip()  # 画面を更新します

pygame.quit()  # Pygameを終了してリソースを解放します