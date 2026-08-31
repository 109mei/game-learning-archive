# coding: utf-8
"""
29_collision_debug_draw.py

当たり判定の可視化（デバッグ描画）の例です。2つの矩形同士の衝突判定を行い、矩形の枠線を
赤や青で描いて状態を分かりやすく表示します。矢印キーで青い矩形を移動させ、衝突時は枠線を
赤に変えます。また、矩形の座標やサイズをテキストとして表示します。
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

W, H = 1280, 720  # 画面の幅と高さ
FONT_PATH = "NotoSansJP-Regular.ttf"  # 使用する日本語フォントファイルのパス
FONT_SIZE = 24  # フォントサイズ

pygame.init()  # Pygameを初期化します
screen = pygame.display.set_mode((W, H))  # 指定サイズのウィンドウを作成します
pygame.display.set_caption("29 当たり判定のデバッグ描画")  # ウィンドウタイトルを設定します

try:  # 指定したフォントを読み込みます
    font = pygame.font.Font(FONT_PATH, FONT_SIZE)  # 日本語フォントオブジェクトを生成
except IOError:  # 読み込めない場合は
    font = pygame.font.SysFont(None, FONT_SIZE)  # デフォルトフォントを使用します

# ---------- 矩形設定 ----------
rect1 = pygame.Rect(400, 300, 250, 150)  # 赤い矩形の位置とサイズ
rect2 = pygame.Rect(150, 150, 200, 120)  # 青い矩形の位置とサイズ
speed = 5  # 移動速度(pixels/frame)

clock = pygame.time.Clock()  # FPS制御用のClockオブジェクト
running = True  # メインループ継続フラグ
while running:  # メインループ
    clock.tick(60)  # 1秒間に60回までループを実行します
    for event in pygame.event.get():  # イベントキューからイベントを取得
        if event.type == QUIT:  # ウィンドウの×ボタンが押された場合
            running = False  # ループを終了します

    # ---------- キー入力でrect2を移動 ----------
    keys = pygame.key.get_pressed()  # キー状態を取得
    if keys[K_LEFT]:  # 左矢印キーが押されている場合
        rect2.x -= speed  # 左へ移動
    if keys[K_RIGHT]:  # 右矢印キーが押されている場合
        rect2.x += speed  # 右へ移動
    if keys[K_UP]:  # 上矢印キーが押されている場合
        rect2.y -= speed  # 上へ移動
    if keys[K_DOWN]:  # 下矢印キーが押されている場合
        rect2.y += speed  # 下へ移動

    # ---------- 衝突判定 ----------
    colliding = rect1.colliderect(rect2)  # 矩形同士が衝突しているか判定
    # ---------- 描画 ----------
    screen.fill((255,255,255))  # 背景を白で塗りつぶします
    # 矩形塗りつぶし
    pygame.draw.rect(screen, (200, 200, 250), rect1)  # 赤い矩形の塗りつぶし
    pygame.draw.rect(screen, (250, 200, 200), rect2)  # 青い矩形の塗りつぶし
    # 枠線: 衝突していれば赤、していなければ黒
    color1 = (255,0,0) if colliding else (0,0,0)  # rect1の枠線色を決定
    color2 = (255,0,0) if colliding else (0,0,0)  # rect2の枠線色を決定
    pygame.draw.rect(screen, color1, rect1, 3)  # rect1の枠線を描画
    pygame.draw.rect(screen, color2, rect2, 3)  # rect2の枠線を描画
    # 情報表示
    info1 = font.render(f"Rect1: x={rect1.x}, y={rect1.y}, w={rect1.w}, h={rect1.h}", True, (0,0,0))  # rect1の情報
    info2 = font.render(f"Rect2: x={rect2.x}, y={rect2.y}, w={rect2.w}, h={rect2.h}", True, (0,0,0))  # rect2の情報
    collide_text = font.render("衝突中" if colliding else "未衝突", True, (255,0,0) if colliding else (0,0,0))  # 衝突状況テキスト
    screen.blit(info1, (20, 20))  # rect1情報を表示
    screen.blit(info2, (20, 50))  # rect2情報を表示
    screen.blit(collide_text, (20, 80))  # 衝突状況を表示
    guide = font.render("矢印キーで青い矩形を動かし赤い矩形と衝突させてください", True, (0,0,0))  # 操作ガイド
    screen.blit(guide, (20, H - 40))  # ガイドを画面下部に表示
    pygame.display.flip()  # 画面を更新します

pygame.quit()  # Pygameを終了してリソースを解放します