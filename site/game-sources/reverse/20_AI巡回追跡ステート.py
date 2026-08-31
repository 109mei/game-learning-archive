# coding: utf-8
"""
20_fsm_patrol_chase.py

単純なAIステートマシンを使って、敵が巡回と追跡の2状態を切り替える例です。
敵は画面上部を左右に巡回し、プレイヤーが近づくと追跡モードに入りプレイヤーに向かって
移動します。一定距離離れると巡回モードに戻ります。
"""

import sys  # sysモジュールはプラットフォーム判定に使用します
import pygame  # Pygameライブラリを読み込みます
from pygame.locals import *  # キー定数やQUITイベントを直接参照できるようにします
import os  # 環境変数設定に使用します

# ---------- OS設定 ----------
# 各OSでのDPIスケーリングとウィンドウ配置を調整します
if sys.platform == "win32":  # Windows環境の場合
    import ctypes  # Windows API呼び出し用モジュール
    ctypes.windll.user32.SetProcessDPIAware()  # DPIスケーリングを無効にします
    os.environ['SDL_VIDEO_CENTERED'] = '1'  # ウィンドウを中央に配置します
else:  # Windows以外のOSの場合
    os.environ['SDL_VIDEO_CENTERED'] = '1'  # ウィンドウを中央に配置します

W, H = 1280, 720  # 画面の幅(W)と高さ(H)を指定します
FONT_PATH = "NotoSansJP-Regular.ttf"  # 日本語フォントファイルのパス
FONT_SIZE = 24  # フォントサイズを指定します

pygame.init()  # Pygameを初期化します
screen = pygame.display.set_mode((W, H))  # 指定サイズでウィンドウを作成します
pygame.display.set_caption("20 AIステート: 巡回と追跡")  # ウィンドウタイトルを設定します

try:  # 指定したフォントを読み込みます
    font = pygame.font.Font(FONT_PATH, FONT_SIZE)  # フォントオブジェクトを生成
except IOError:  # 読み込めない場合は
    font = pygame.font.SysFont(None, FONT_SIZE)  # デフォルトフォントを使用します

# ---------- プレイヤー設定 ----------
player_rect = pygame.Rect(W//2, H - 80, 50, 50)  # プレイヤーの矩形(x,y,width,height) 初期位置は中央下
player_speed = 6  # プレイヤーの移動速度(pixels/frame)

# ---------- 敵設定 ----------
enemy_rect = pygame.Rect(W//2, 100, 60, 60)  # 敵の矩形。初期位置は画面上部中央
enemy_state = 'patrol'  # 初期ステートは巡回モード
enemy_dir = 1  # 巡回方向(1:右, -1:左)
patrol_speed = 3  # 巡回速度
chase_speed = 5  # 追跡速度
patrol_bounds = (200, W - 200)  # 巡回範囲の左右端
detection_radius = 300  # プレイヤー検出半径

clock = pygame.time.Clock()  # FPS制御用のClockオブジェクト
running = True  # メインループ継続フラグ
while running:  # メインループ
    dt = clock.tick(60)  # 経過時間(ms)を取得し60FPSに制限
    for event in pygame.event.get():  # イベント処理
        if event.type == QUIT:  # ウィンドウクローズイベント
            running = False  # ループ終了

    # ---------- プレイヤー移動 ----------
    keys = pygame.key.get_pressed()  # キー状態を取得します
    if keys[K_LEFT] and player_rect.left > 0:  # 左キーが押され左端より内側なら
        player_rect.x -= player_speed  # 左へ移動
    if keys[K_RIGHT] and player_rect.right < W:  # 右キーが押され右端より内側なら
        player_rect.x += player_speed  # 右へ移動
    if keys[K_UP] and player_rect.top > 0:  # 上キーが押され上端より内側なら
        player_rect.y -= player_speed  # 上へ移動
    if keys[K_DOWN] and player_rect.bottom < H:  # 下キーが押され下端より内側なら
        player_rect.y += player_speed  # 下へ移動

    # ---------- 敵AIステート ----------
    # プレイヤーとの距離を計算します
    dx = player_rect.centerx - enemy_rect.centerx  # x方向の差
    dy = player_rect.centery - enemy_rect.centery  # y方向の差
    dist = (dx*dx + dy*dy) ** 0.5  # ピタゴラスの定理で距離を求めます
    if enemy_state == 'patrol':  # 巡回ステート
        # 追跡開始条件: プレイヤーが検出範囲内かチェック
        if dist < detection_radius:  # プレイヤーが検出範囲内なら
            enemy_state = 'chase'  # 追跡モードに切り替え
        else:  # 検出範囲外の場合
            # 巡回中は範囲内で左右に移動
            enemy_rect.x += patrol_speed * enemy_dir  # 敵を左右に移動
            # 範囲端に達したら方向を反転
            if enemy_rect.left <= patrol_bounds[0] or enemy_rect.right >= patrol_bounds[1]:  # 巡回範囲の端に達した場合
                enemy_dir *= -1  # 端で方向反転
    elif enemy_state == 'chase':  # 追跡ステート
        # 追跡中に離れ過ぎたら巡回に戻る
        if dist > detection_radius * 1.2:  # プレイヤーが離れ過ぎたら
            enemy_state = 'patrol'  # 巡回に戻る
        else:  # まだプレイヤーを追跡
            # プレイヤーに向かって移動
            if dist != 0:  # 0で割らないようチェック
                vx = dx / dist * chase_speed  # x方向単位ベクトルに速度を乗算
                vy = dy / dist * chase_speed  # y方向単位ベクトルに速度を乗算
                enemy_rect.x += int(vx)  # x座標を更新
                enemy_rect.y += int(vy)  # y座標を更新

    # ---------- 描画 ----------
    screen.fill((40, 40, 60))  # 背景を濃い色で塗りつぶします
    # プレイヤー描画
    pygame.draw.rect(screen, (80, 220, 80), player_rect)  # 緑色でプレイヤーを描きます
    # 敵描画: 状態に応じて色を変更します
    color = (220, 80, 80) if enemy_state == 'chase' else (200, 200, 80)  # 追跡中は赤、巡回中は黄色
    pygame.draw.rect(screen, color, enemy_rect)  # 敵を描きます
    # ステート表示文字列を生成して描画
    state_text = font.render(f"敵の状態: {enemy_state}", True, (255, 255, 255))  # 白色で描画
    screen.blit(state_text, (20, 20))  # 画面左上に表示
    # ガイド: 操作方法の表示
    guide = font.render("プレイヤーを↑↓→←移動して敵の追跡挙動を確認してください", True, (255, 255, 255))  # 操作方法のガイドテキストを生成
    screen.blit(guide, (20, 50))  # ガイドを表示
    pygame.display.flip()  # 表示を更新します

pygame.quit()  # Pygameを終了してリソースを解放します