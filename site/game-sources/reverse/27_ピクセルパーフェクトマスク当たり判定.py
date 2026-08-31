# coding: utf-8
"""
27_mask_pixel_perfect.py

マスクを使用したピクセルパーフェクトな当たり判定の例です。不規則な形状を持つ2つの画像
（ここでは円形）同士の衝突判定を、マスクを用いて正確に行います。矢印キーで青い画像を
移動させ、赤い画像に接触すると"衝突!"と表示します。
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

W, H = 1280, 720  # 画面の幅(W)と高さ(H)を指定します
FONT_PATH = "NotoSansJP-Regular.ttf"  # 使用する日本語フォントファイルのパス
FONT_SIZE = 28  # フォントサイズを指定します

pygame.init()  # Pygameを初期化します
screen = pygame.display.set_mode((W, H))  # 指定サイズのウィンドウを作成します
pygame.display.set_caption("27 マスクによるピクセル当たり判定")  # ウィンドウタイトルを設定します

try:  # 指定したフォントを読み込みます
    font = pygame.font.Font(FONT_PATH, FONT_SIZE)  # 日本語フォントオブジェクトを生成
except IOError:  # 読み込めない場合は
    font = pygame.font.SysFont(None, FONT_SIZE)  # デフォルトフォントを使用します

# ---------- 不規則形状のSurface作成: 円を直接描画します ----------
red_radius = 80  # 赤い円の半径
blue_radius = 60  # 青い円の半径
red_surf = pygame.Surface((red_radius*2, red_radius*2), pygame.SRCALPHA)  # 赤い円を描画するためのサーフェス
blue_surf = pygame.Surface((blue_radius*2, blue_radius*2), pygame.SRCALPHA)  # 青い円を描画するためのサーフェス
pygame.draw.circle(red_surf, (255, 100, 100), (red_radius, red_radius), red_radius)  # 赤い円をサーフェスに描画
pygame.draw.circle(blue_surf, (100, 100, 255), (blue_radius, blue_radius), blue_radius)  # 青い円をサーフェスに描画

# マスク作成: サーフェスから不透明ピクセルのマスクを生成します
red_mask = pygame.mask.from_surface(red_surf)  # 赤い円のマスク
blue_mask = pygame.mask.from_surface(blue_surf)  # 青い円のマスク

red_pos = [500, 300]  # 赤い円の描画位置(x,y)
blue_pos = [200, 200]  # 青い円の描画位置(x,y)
speed = 6  # 青い円の移動速度(pixels/frame)
message = ""  # 衝突メッセージ文字列

clock = pygame.time.Clock()  # FPS制御用のClockオブジェクト
running = True  # メインループ継続フラグ
while running:  # メインループ
    clock.tick(60)  # 1秒間に60回までループを実行します
    for event in pygame.event.get():  # イベントキューからイベントを取得
        if event.type == QUIT:  # ウィンドウの×ボタンが押された場合
            running = False  # ループを終了します

    # ---------- 移動 ----------
    keys = pygame.key.get_pressed()  # 押されているキーの状態を取得
    if keys[K_LEFT]:  # 左矢印キーが押されている場合
        blue_pos[0] -= speed  # 左へ移動
    if keys[K_RIGHT]:  # 右矢印キーが押されている場合
        blue_pos[0] += speed  # 右へ移動
    if keys[K_UP]:  # 上矢印キーが押されている場合
        blue_pos[1] -= speed  # 上へ移動
    if keys[K_DOWN]:  # 下矢印キーが押されている場合
        blue_pos[1] += speed  # 下へ移動

    # ---------- マスク同士の衝突判定 ----------
    # offset = 相手画像との相対位置
    offset = (int(red_pos[0] - blue_pos[0]), int(red_pos[1] - blue_pos[1]))  # マスク計算用のオフセット
    if blue_mask.overlap(red_mask, offset):  # マスクが重なっているか判定
        message = "衝突!"  # 衝突した場合のメッセージ
    else:  # 衝突していない場合
        message = ""  # 衝突していない場合は空文字列

    # ---------- 描画 ----------
    screen.fill((240, 240, 240))  # 背景を淡いグレーで塗りつぶします
    # サーフェス描画
    screen.blit(red_surf, red_pos)  # 赤い円サーフェスを描画
    screen.blit(blue_surf, blue_pos)  # 青い円サーフェスを描画
    # 枠線の描画
    pygame.draw.rect(screen, (0,0,0), (*red_pos, red_surf.get_width(), red_surf.get_height()), 1)  # 赤い円の枠線
    pygame.draw.rect(screen, (0,0,0), (*blue_pos, blue_surf.get_width(), blue_surf.get_height()), 1)  # 青い円の枠線
    # メッセージの描画
    if message:  # messageが空でない場合
        txt = font.render(message, True, (200, 0, 0))  # メッセージテキストを生成
        screen.blit(txt, (20, 20))  # 画面に表示
    guide = font.render("矢印キーで青い円を動かし赤い円に近づけてください", True, (0,0,0))  # ガイドテキスト
    screen.blit(guide, (20, H - 40))  # ガイドを画面下部に表示
    pygame.display.flip()  # 表示を更新します

pygame.quit()  # Pygameを終了してリソースを解放します