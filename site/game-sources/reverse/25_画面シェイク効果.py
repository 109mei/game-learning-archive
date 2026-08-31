# coding: utf-8
"""
25_screen_shake.py

画面シェイク効果を示す例です。Spaceキーを押すと一定時間ランダムに画面が揺れます。
シェイク中は描画内容がオフセットされることで揺れているように見えます。
"""

import sys  # sysモジュールはプラットフォーム判定に使用します
import pygame  # Pygameライブラリを読み込みます
from pygame.locals import *  # キー定数やQUITイベントを直接参照できるようにします
import os  # 環境変数の設定に使用します
import random  # 乱数生成に使用します

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
FONT_SIZE = 28  # フォントサイズを指定します

pygame.init()  # Pygameを初期化します
screen = pygame.display.set_mode((W, H))  # 指定サイズのウィンドウを作成します
pygame.display.set_caption("25 画面シェイク")  # ウィンドウタイトルを設定します

try:  # 指定したフォントを読み込みます
    font = pygame.font.Font(FONT_PATH, FONT_SIZE)  # 日本語フォントオブジェクトを生成
except IOError:  # 読み込めない場合は
    font = pygame.font.SysFont(None, FONT_SIZE)  # デフォルトフォントを使用します

shake_time = 0  # シェイク残り時間(秒)
shake_intensity = 0  # シェイクの強さ（初期値は0）

clock = pygame.time.Clock()  # FPS制御用のClockオブジェクト
running = True  # メインループ継続フラグ
while running:  # メインループ開始
    dt = clock.tick(60) / 1000.0  # 前回のフレームからの経過時間(秒)を取得し60FPSに制限
    for event in pygame.event.get():  # イベントキューからイベントを取得
        if event.type == QUIT:  # ウィンドウの×ボタンが押された場合
            running = False  # ループを終了します
        elif event.type == KEYDOWN and event.key == K_SPACE:  # スペースキーが押された場合
            # Spaceでシェイク開始
            shake_time = 0.5  # シェイク時間を0.5秒に設定
            shake_intensity = 10  # 最大オフセットを設定

    # ---------- シェイク処理 ----------
    offset_x, offset_y = 0, 0  # 初期オフセットをゼロにリセット
    if shake_time > 0:  # シェイク時間が残っている場合
        shake_time -= dt  # 経過時間分だけ残りシェイク時間を減らす
        # 時間の経過に伴い強度を減衰させる
        current_intensity = shake_intensity * (shake_time / 0.5)  # 残り時間に応じて強度を計算
        # ランダムなオフセットを生成して画面を揺らす
        offset_x = random.uniform(-current_intensity, current_intensity)  # x方向にランダムなオフセットを設定
        offset_y = random.uniform(-current_intensity, current_intensity)  # y方向にランダムなオフセットを設定

    # ---------- 描画処理 ----------
    # ベース背景を描画 (スクリーンより大きなサーフェスに描画し、オフセットさせる)
    base_surface = pygame.Surface((W, H))  # オフスクリーンサーフェスを作成
    base_surface.fill((50, 70, 100))  # ベース背景色で塗りつぶす
    # 中央に長方形を描画
    pygame.draw.rect(base_surface, (200, 200, 250), pygame.Rect(W//2 - 100, H//2 - 50, 200, 100), border_radius=10)  # 中央の長方形
    # ガイドテキスト
    guide = font.render("Spaceキーで画面シェイクを発生させます", True, (255, 255, 255))  # ガイド文字列を生成
    base_surface.blit(guide, (20, 20))  # ガイドをサーフェスに描画
    # シェイクした位置に描画
    screen.fill((0, 0, 0))  # 画面を黒でクリア
    screen.blit(base_surface, (int(offset_x), int(offset_y)))  # オフセットを適用して描画
    pygame.display.flip()  # 画面を更新します

pygame.quit()  # Pygameを終了してリソースを解放します