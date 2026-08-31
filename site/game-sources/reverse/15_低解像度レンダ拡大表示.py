# coding: utf-8
"""
15_resolution_scaling.py

低解像度のレンダリング結果を拡大して表示する例です。320x180ピクセルのサーフェスに描画し、
それを4倍に拡大して1280x720ピクセルのウィンドウに表示します。ピクセルアートのような
ブロック感のある表現が必要な場合に役立ちます。
"""

import sys  # OSプラットフォーム判定に使用するモジュール
import pygame  # Pygameライブラリ本体をインポート
from pygame.locals import *  # Pygameの定数を直接参照できるようにインポート
import os  # 環境変数設定などOS関連の機能を利用するためのモジュール

# OS設定: Windowsかそれ以外かでDPIの扱いを変える
if sys.platform == "win32":  # Windowsの場合
    import ctypes  # Windows APIを呼び出すためのモジュール
    ctypes.windll.user32.SetProcessDPIAware()  # DPIスケーリングを無効にしてUIがぼやけないようにする
    os.environ['SDL_VIDEO_CENTERED'] = '1'  # ウィンドウを画面中央に表示するための環境変数
else:  # Windows以外のOSの場合
    os.environ['SDL_VIDEO_CENTERED'] = '1'  # その他のOSでもウィンドウを中央に配置

W, H = 1280, 720  # 画面の幅と高さ (ピクセル)
LOW_W, LOW_H = 320, 180  # 低解像度レンダリングの幅と高さ
SCALE = W // LOW_W  # 拡大倍率 (W/LOW_W=4)
FONT_PATH = "NotoSansJP-Regular.ttf"  # 日本語フォントのパス
FONT_SIZE = 24  # フォントサイズ

pygame.init()  # Pygameの各モジュールを初期化
screen = pygame.display.set_mode((W, H))  # 指定サイズのウィンドウを作成
pygame.display.set_caption("15 低解像度レンダ→拡大表示")  # ウィンドウタイトルを設定

try:  # フォント読み込みを試みます
    font = pygame.font.Font(FONT_PATH, FONT_SIZE)  # 指定した日本語フォントを読み込みます
except IOError:  # フォントが見つからない場合に実行されます
    font = pygame.font.SysFont(None, FONT_SIZE)  # フォントが見つからない場合はデフォルトフォントを使用します

# 低解像度用Surfaceを作成: ここに描画して後で拡大
low_surface = pygame.Surface((LOW_W, LOW_H))  # 低解像度描画用のSurfaceを作成します

clock = pygame.time.Clock()  # FPS制御用のClockオブジェクト
running = True  # メインループ継続フラグ
angle = 0  # 回転角度の初期値
while running:  # メインループ開始
    dt = clock.tick(60) / 1000  # 前フレームからの経過秒数を取得し、FPSを60に保つ
    for event in pygame.event.get():  # イベントを処理
        if event.type == QUIT:  # ウィンドウの×ボタンが押されたとき
            running = False  # ループを終了

    angle += 90 * dt  # 1秒間で90度回転するように角度を増やす

    # 低解像度サーフェスに描画: まず背景を塗りつぶす
    low_surface.fill((30, 30, 60))  # 背景色で塗りつぶし
    # 回転する矩形を用意
    rect_size = 40  # 矩形のサイズ
    rect_center = (LOW_W // 2, LOW_H // 2)  # 矩形の回転中心
    # 回転用サーフェスを作成。SRCALPHA を指定してアルファチャンネルを有効にする
    box = pygame.Surface((rect_size, rect_size), pygame.SRCALPHA)  # 回転用の矩形サーフェスを作成します
    box.fill((200, 200, 50))  # 矩形を黄色で塗りつぶす
    rotated = pygame.transform.rotate(box, angle)  # 矩形をangle度回転させる
    rot_rect = rotated.get_rect(center=rect_center)  # 回転後のサーフェスの位置を計算
    low_surface.blit(rotated, rot_rect)  # 低解像度サーフェスに回転した矩形を描画
    # テキスト(低解像度)を描画
    txt = font.render("低解像度で描画中", True, (255, 255, 255))  # テキストをレンダリング
    txt_scaled = pygame.transform.scale(txt, (txt.get_width(), txt.get_height()))  # 同じサイズでダミー拡大
    low_surface.blit(txt_scaled, (10, 10))  # サーフェスにテキストを描画

    # 低解像度のサーフェスをウィンドウサイズに拡大する
    scaled_surface = pygame.transform.scale(low_surface, (W, H))  # 低解像度のサーフェスをウィンドウサイズに拡大

    # 拡大されたサーフェスを大きな画面に描画
    screen.blit(scaled_surface, (0, 0))  # 拡大したサーフェスを画面全体に描画
    # ガイドテキストを描画
    guide = font.render("320x180で描画 → 1280x720に拡大", True, (255, 255, 255))  # ガイドテキストを生成
    screen.blit(guide, (20, H - 40))  # ガイドテキストを画面下部に描画
    pygame.display.flip()  # 表示を更新

pygame.quit()  # Pygameを終了してリソースを解放