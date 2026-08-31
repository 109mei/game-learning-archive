# coding: utf-8
"""
26_zoom_in_out.py

ズームイン・アウトの例です。矢印キーでカメラを移動し、zキーでズームイン、xキーで
ズームアウトできます。ワールドは画面より大きなサーフェスに描かれ、zoom_factorに応じて
縮尺を変えて表示します。
"""

import sys  # sysモジュールはプラットフォーム判定に使用します
import pygame  # Pygameライブラリを読み込みます
from pygame.locals import *  # キー定数やQUITイベントを直接参照できるようにします
import os  # 環境変数の設定に使用します

# ---------- OS設定 ----------
# 各OSでのDPIスケーリングとウィンドウ配置を調整します
if sys.platform == "win32":  # Windows環境の場合
    import ctypes  # Windows API呼び出し用モジュール
    ctypes.windll.user32.SetProcessDPIAware()  # DPIスケーリングを無効にします
    os.environ['SDL_VIDEO_CENTERED'] = '1'  # ウィンドウを中央に配置します
else:  # Windows以外のOSの場合
    os.environ['SDL_VIDEO_CENTERED'] = '1'  # ウィンドウを中央に配置します

W, H = 1280, 720  # 表示画面の幅と高さ
WORLD_W, WORLD_H = 2000, 2000  # ワールド全体のサイズ

# 最小ズーム倍率を計算します。画面よりもワールドが小さい場合に拡大しすぎて範囲外を参照しないようにします。
min_zoom_factor = max(W / WORLD_W, H / WORLD_H)  # W/WORLD_WやH/WORLD_Hのうち大きい方を下限とします
FONT_PATH = "NotoSansJP-Regular.ttf"  # 使用する日本語フォントファイルのパス
FONT_SIZE = 24  # フォントサイズを指定します

pygame.init()  # Pygameを初期化します
screen = pygame.display.set_mode((W, H))  # 指定サイズのウィンドウを作成します
pygame.display.set_caption("26 ズームイン/アウト")  # ウィンドウタイトルを設定します

try:  # 指定したフォントを読み込みます
    font = pygame.font.Font(FONT_PATH, FONT_SIZE)  # 日本語フォントオブジェクトを生成
except IOError:  # 読み込めない場合は
    font = pygame.font.SysFont(None, FONT_SIZE)  # デフォルトフォントを使用します

# ---------- ワールドサーフェス作成 ----------
world = pygame.Surface((WORLD_W, WORLD_H))  # ワールド全体を描画するためのオフスクリーンサーフェス
world.fill((60, 100, 60))  # ワールドの背景色で塗りつぶします
# グリッドを描く
grid_color = (90, 130, 90)  # グリッド線の色
for x in range(0, WORLD_W, 100):  # 100ピクセル毎に縦線を描画
    pygame.draw.line(world, grid_color, (x, 0), (x, WORLD_H))  # 縦線を描く
for y in range(0, WORLD_H, 100):  # 100ピクセル毎に横線を描画
    pygame.draw.line(world, grid_color, (0, y), (WORLD_W, y))  # 横線を描く
# 目印として赤い四角を描画
pygame.draw.rect(world, (200, 50, 50), pygame.Rect(900, 900, 200, 200))  # 中央付近に赤い目印

camera_x, camera_y = 0, 0  # カメラの位置を表す座標
zoom_factor = 1.0  # ズーム倍率(1.0が等倍)

clock = pygame.time.Clock()  # FPS制御用のClockオブジェクト
running = True  # メインループ継続フラグ
while running:  # メインループ
    dt = clock.tick(60)  # 経過時間(ms)を取得し60FPSに制限
    for event in pygame.event.get():  # イベントキューからイベントを取得
        if event.type == QUIT:  # ウィンドウの×ボタンが押された場合
            running = False  # ループを終了します
        elif event.type == KEYDOWN:  # キーが押された場合
            if event.key == K_EQUALS or event.key == K_z:  # =キーまたはzキー
                zoom_factor = min(zoom_factor * 1.1, 4.0)  # ズームイン: 最大4倍に制限
            elif event.key == K_x:  # xキー
                # ズームアウト: 最小ズーム倍率(min_zoom_factor)まで縮小できます
                zoom_factor = max(zoom_factor / 1.1, min_zoom_factor)  # これ以上小さくするとワールド外を参照するため

    # ---------- カメラ移動 ----------
    keys = pygame.key.get_pressed()  # 押されているキーの状態を取得
    move_speed = int(8 / zoom_factor)  # ズームイン時は移動速度を遅くする
    if keys[K_LEFT]:  # 左矢印キーが押されている場合
        camera_x -= move_speed  # カメラを左へ移動
    if keys[K_RIGHT]:  # 右矢印キーが押されている場合
        camera_x += move_speed  # カメラを右へ移動
    if keys[K_UP]:  # 上矢印キーが押されている場合
        camera_y -= move_speed  # カメラを上へ移動
    if keys[K_DOWN]:  # 下矢印キーが押されている場合
        camera_y += move_speed  # カメラを下へ移動
    # カメラ位置の制限: ワールドの境界内に制限
    max_x = WORLD_W - W / zoom_factor  # カメラが移動できる最大x座標
    max_y = WORLD_H - H / zoom_factor  # カメラが移動できる最大y座標
    camera_x = max(0, min(camera_x, max_x))  # x座標を0からmax_xの範囲に制限
    camera_y = max(0, min(camera_y, max_y))  # y座標を0からmax_yの範囲に制限

    # ---------- ズーム表示 ----------
    # カメラの視野矩形をワールドから切り出す
    view_rect = pygame.Rect(int(camera_x), int(camera_y), int(W / zoom_factor), int(H / zoom_factor))  # 表示範囲
    sub = world.subsurface(view_rect)  # 視野範囲のサーフェスを取得
    # サブサーフェスを画面サイズに拡大
    scaled = pygame.transform.scale(sub, (W, H))  # ズームファクターに応じて拡大
    screen.blit(scaled, (0, 0))  # 拡大したサーフェスを画面に描画

    # ズーム率表示とガイド表示
    zoom_text = font.render(f"ズーム率: {zoom_factor:.2f}x", True, (255, 255, 255))  # ズーム率テキストを生成
    screen.blit(zoom_text, (20, 20))  # ズーム率を表示
    guide1 = font.render("zキーでズームイン、xキーでズームアウト", True, (255, 255, 255))  # ガイド1
    screen.blit(guide1, (20, 50))  # ガイド1を表示
    guide2 = font.render("矢印キーで移動", True, (255, 255, 255))  # ガイド2
    screen.blit(guide2, (20, 80))  # ガイド2を表示

    pygame.display.flip()  # 画面を更新します

pygame.quit()  # Pygameを終了してリソースを解放します