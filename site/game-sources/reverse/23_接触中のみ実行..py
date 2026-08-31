# coding: utf-8
"""
23_action_only_when_colliding.py

2つの矩形が接触しているときのみキー操作が有効になる例です。青い矩形を矢印キーで移動し、
赤い矩形と重なっている間に A キーを押すとメッセージが表示されます。重なっていない場合は
何も起こりません。
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
pygame.display.set_caption("23 接触中のみキーで実行")  # ウィンドウタイトルを設定します

try:  # 指定したフォントを読み込みます
    font = pygame.font.Font(FONT_PATH, FONT_SIZE)  # 日本語フォントオブジェクトを生成
except IOError:  # 読み込めない場合は
    font = pygame.font.SysFont(None, FONT_SIZE)  # デフォルトフォントを使用します

# 矩形設定
static_rect = pygame.Rect(600, 300, 200, 150)  # 固定矩形: 赤い矩形の位置とサイズ
movable_rect = pygame.Rect(200, 200, 150, 100)  # 移動可能な青い矩形の位置とサイズ
speed = 6  # 移動速度(pixels/frame)
message = ""  # 画面に表示するメッセージ文字列

clock = pygame.time.Clock()  # FPS制御用のClockオブジェクト
running = True  # メインループ継続フラグ
while running:  # メインループ開始
    clock.tick(60)  # 1秒間に60回までループを実行します
    for event in pygame.event.get():  # イベントキューからイベントを取得
        if event.type == QUIT:  # ウィンドウの×ボタンが押された場合
            running = False  # ループを終了します
        elif event.type == KEYDOWN and event.key == K_a:  # Aキーが押された場合
            # 衝突中のみメッセージを表示
            if movable_rect.colliderect(static_rect):  # 青い矩形と赤い矩形が重なっているか判定
                message = "Aキーで実行しました！"  # 衝突中にAキーを押したときのメッセージ
            else:  # 重なっていない場合
                message = "衝突していません"  # 衝突していない場合のメッセージ

    # キー状態を取得して矩形を移動します
    keys = pygame.key.get_pressed()  # 押されているキーの状態を取得
    if keys[K_LEFT]:  # 左矢印キーが押されている場合
        movable_rect.x -= speed  # 左へ移動
    if keys[K_RIGHT]:  # 右矢印キーが押されている場合
        movable_rect.x += speed  # 右へ移動
    if keys[K_UP]:  # 上矢印キーが押されている場合
        movable_rect.y -= speed  # 上へ移動
    if keys[K_DOWN]:  # 下矢印キーが押されている場合
        movable_rect.y += speed  # 下へ移動

    # ---------- 描画 ----------
    screen.fill((240, 240, 240))  # 背景を淡いグレーで塗りつぶします
    # 固定の赤い矩形を描画
    pygame.draw.rect(screen, (255, 150, 150), static_rect)  # 赤い固定矩形を描画
    # 操作可能な青い矩形を描画
    pygame.draw.rect(screen, (150, 150, 255), movable_rect)  # 青い操作矩形を描画
    # ガイドのテキストを生成して描画
    guide1 = font.render("矢印キーで青い矩形を移動", True, (0, 0, 0))  # ガイド1
    guide2 = font.render("赤い矩形と重なっている間に A キーを押すと実行", True, (0, 0, 0))  # ガイド2
    screen.blit(guide1, (20, H - 80))  # ガイド1を画面下部に表示
    screen.blit(guide2, (20, H - 50))  # ガイド2を画面下部に表示
    # メッセージの表示
    if message:  # messageが空でない場合
        msg_surf = font.render(message, True, (200, 50, 50))  # メッセージ用Surfaceを生成
        screen.blit(msg_surf, (20, 20))  # 画面左上に表示
    pygame.display.flip()  # 画面を更新します

pygame.quit()  # Pygameを終了してリソースを解放します