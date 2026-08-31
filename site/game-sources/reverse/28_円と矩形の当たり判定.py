# coding: utf-8
"""
28_circle_collisions.py

円同士および円と矩形の当たり判定を示す例です。円と円の衝突は中心間距離と半径の和で判定し、
円と矩形の衝突は矩形の最も近い点と円の中心の距離で判定します。矢印キーで青い円を動かし、
赤い円または緑の矩形に衝突させてみてください。
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
pygame.display.set_caption("28 円×円／円×矩形の当たり判定")  # ウィンドウタイトルを設定します

try:  # 指定したフォントを読み込みます
    font = pygame.font.Font(FONT_PATH, FONT_SIZE)  # 日本語フォントオブジェクトを生成
except IOError:  # 読み込めない場合は
    font = pygame.font.SysFont(None, FONT_SIZE)  # デフォルトフォントを使用します

# ---------- オブジェクト設定 ----------
circle1_pos = [300, 300]  # 静的な赤い円の中心位置
circle1_radius = 60  # 静的な赤い円の半径
circle2_pos = [800, 300]  # 静的な紫の円の中心位置
circle2_radius = 80  # 静的な紫の円の半径
rect = pygame.Rect(600, 500, 200, 100)  # 緑色の矩形オブジェクトを作成
player_circle_pos = [100, 100]  # プレイヤーが操作する青い円の中心位置
player_radius = 40  # プレイヤー円の半径
speed = 6  # プレイヤーの移動速度(pixels/frame)
collision_msg = ""  # 衝突メッセージ用の文字列を初期化

clock = pygame.time.Clock()  # FPS制御用のClockオブジェクト
running = True  # メインループ継続フラグ
while running:  # メインループ
    clock.tick(60)  # 1秒間に60回までループを実行します
    for event in pygame.event.get():  # イベントキューからイベントを取得
        if event.type == QUIT:  # ウィンドウの×ボタンが押された場合
            running = False  # ループを終了します

    # ---------- プレイヤー移動 ----------
    keys = pygame.key.get_pressed()  # 押されているキーの状態を取得
    if keys[K_LEFT]:  # 左矢印キーが押されている場合
        player_circle_pos[0] -= speed  # 左へ移動
    if keys[K_RIGHT]:  # 右矢印キーが押されている場合
        player_circle_pos[0] += speed  # 右へ移動
    if keys[K_UP]:  # 上矢印キーが押されている場合
        player_circle_pos[1] -= speed  # 上へ移動
    if keys[K_DOWN]:  # 下矢印キーが押されている場合
        player_circle_pos[1] += speed  # 下へ移動

    # ---------- 衝突判定処理 ----------
    collision_msg = ""  # 毎フレームメッセージをリセット
    # 円×円の当たり判定: 中心間距離の二乗が半径の和の二乗以下か判定
    dx1 = player_circle_pos[0] - circle1_pos[0]  # 赤い円とのx方向差
    dy1 = player_circle_pos[1] - circle1_pos[1]  # 赤い円とのy方向差
    if dx1*dx1 + dy1*dy1 <= (player_radius + circle1_radius) ** 2:  # 赤い円との衝突判定
        collision_msg = "赤い円と衝突!"  # 衝突メッセージを設定
    else:  # 赤い円と衝突していない場合
        dx2 = player_circle_pos[0] - circle2_pos[0]  # 紫の円とのx方向差
        dy2 = player_circle_pos[1] - circle2_pos[1]  # 紫の円とのy方向差
        if dx2*dx2 + dy2*dy2 <= (player_radius + circle2_radius) ** 2:  # 紫の円との衝突判定
            collision_msg = "紫の円と衝突!"  # 衝突メッセージを設定
        else:  # どちらの円とも衝突していない場合
            # 円×矩形の当たり判定: 矩形の内側で円の中心に最も近い点を計算
            closest_x = max(rect.left, min(player_circle_pos[0], rect.right))  # x方向の最も近い点
            closest_y = max(rect.top,  min(player_circle_pos[1], rect.bottom))  # y方向の最も近い点
            dxr = player_circle_pos[0] - closest_x  # 矩形の最近点とプレイヤー円中心のx差
            dyr = player_circle_pos[1] - closest_y  # 矩形の最近点とプレイヤー円中心のy差
            if dxr*dxr + dyr*dyr <= player_radius * player_radius:  # 距離の二乗で衝突判定
                collision_msg = "緑の矩形と衝突!"  # 衝突メッセージを設定

    # ---------- 描画 ----------
    screen.fill((245, 245, 245))  # 背景を薄いグレーで塗りつぶします
    # 静的オブジェクトを描画
    pygame.draw.circle(screen, (250, 100, 100), circle1_pos, circle1_radius)  # 赤い円
    pygame.draw.circle(screen, (200, 100, 250), circle2_pos, circle2_radius)  # 紫の円
    pygame.draw.rect(screen, (100, 250, 100), rect)  # 緑の矩形
    # プレイヤー円
    pygame.draw.circle(screen, (100, 150, 250), player_circle_pos, player_radius)  # 青い円
    # ガイドメッセージを描画
    guide1 = font.render("青い円を矢印キーで動かして他のオブジェクトに近づけてください", True, (0,0,0))  # ガイドテキスト
    screen.blit(guide1, (20, 20))  # ガイドテキストを描画
    if collision_msg:  # 衝突メッセージがある場合
        msg = font.render(collision_msg, True, (200,0,0))  # メッセージを生成
        screen.blit(msg, (20, 60))  # メッセージを表示
    pygame.display.flip()  # 画面を更新します

pygame.quit()  # Pygameを終了してリソースを解放します