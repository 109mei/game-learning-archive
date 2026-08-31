# coding: utf-8
"""
14_fixed_timestep.py

固定時間ステップ更新と可変フレームレート描画の例です。物理計算を一定のΔtで行うことで、
フレームレートの変動に関係なく一貫した動きを実現します。このデモではボールが一定速度で
画面を移動し、端で跳ね返ります。
"""

import sys  # sysモジュールはプラットフォーム判定に使用します
import pygame  # Pygameライブラリを読み込みます
from pygame.locals import *  # QUITなどの定数を直接参照できるようにします
import os  # 環境変数設定に使用します

# OS設定
# 各プラットフォームでDPIスケール無効化やウィンドウ位置を調整します
if sys.platform == "win32":  # Windows環境の場合
    import ctypes  # Windows API呼び出し用
    ctypes.windll.user32.SetProcessDPIAware()  # DPIスケールを無効にします
    os.environ['SDL_VIDEO_CENTERED'] = '1'  # ウィンドウを中央に配置します
else:  # Windows以外の場合
    os.environ['SDL_VIDEO_CENTERED'] = '1'  # ウィンドウを中央に配置します

W, H = 1280, 720  # 画面の幅と高さ
FONT_PATH = "NotoSansJP-Regular.ttf"  # 日本語フォントのパス
FONT_SIZE = 24  # フォントサイズ

pygame.init()  # Pygameを初期化します
screen = pygame.display.set_mode((W, H))  # 指定サイズのウィンドウを作成します
pygame.display.set_caption("14 固定Δt更新＋可変描画")  # ウィンドウタイトルを設定します

try:  # フォント読み込みを試みます
    font = pygame.font.Font(FONT_PATH, FONT_SIZE)  # 指定フォントを読み込みます
except IOError:  # フォントが見つからない場合に実行されます
    font = pygame.font.SysFont(None, FONT_SIZE)  # フォントが見つからない場合はデフォルトフォントを使用します

# ボールの状態
ball_pos = [W/2, H/2]  # ボールの位置(x, y)を浮動小数点で保持
ball_vel = [150, 90]  # ボールの速度(ピクセル/秒)をxとyで指定
ball_radius = 30  # ボールの半径(ピクセル)

fixed_dt = 1/60  # 更新ステップ(秒)。物理計算をこの間隔で更新します
accumulator = 0.0  # フレーム間の残り時間を蓄積するための変数

clock = pygame.time.Clock()  # FPS制御用のClockオブジェクト
running = True  # メインループ継続フラグ
while running:  # メインループ開始
    dt_ms = clock.tick(60)  # 1フレームの実時間(ms)を取得し60FPSに制御します
    dt = dt_ms / 1000.0  # フレーム時間を秒に変換
    for event in pygame.event.get():  # イベントキューからイベントを取得
        if event.type == QUIT:  # ウィンドウの×ボタンが押された場合
            running = False  # ループを終了します

    accumulator += dt  # 経過した時間をaccumulatorに加算
    # 固定ステップで物理更新
    while accumulator >= fixed_dt:  # 残り時間が1ステップ分以上ある場合、物理更新を繰り返します
        # 位置更新: v * dt
        ball_pos[0] += ball_vel[0] * fixed_dt  # x座標の更新
        ball_pos[1] += ball_vel[1] * fixed_dt  # y座標の更新
        # 壁で跳ね返り
        if ball_pos[0] - ball_radius <= 0 or ball_pos[0] + ball_radius >= W:  # 左右の壁に当たったか確認します
            ball_vel[0] *= -1  # 左右の端に当たった場合はx速度の符号を反転させる
        if ball_pos[1] - ball_radius <= 0 or ball_pos[1] + ball_radius >= H:  # 上下の壁に当たったか確認します
            ball_vel[1] *= -1  # 上下の端に当たった場合はy速度の符号を反転させる
        accumulator -= fixed_dt  # 処理済みの時間をaccumulatorから引いてループ条件を更新

    # 描画
    screen.fill((20, 20, 20))  # 背景を暗い色で塗りつぶします
    # ボールの描画
    pygame.draw.circle(screen, (200, 200, 100), (int(ball_pos[0]), int(ball_pos[1])), ball_radius)  # ボールを描画します
    # 説明テキスト
    info = font.render("固定Δt更新により一定速度で移動 (ボールが滑らかに見えます)", True, (230, 230, 230))  # 説明テキストを生成します
    screen.blit(info, (20, 20))  # 説明テキストを左上に描画します
    pygame.display.flip()  # 画面を更新して描画内容を表示します

# ループ終了後にPygameを終了します
pygame.quit()  # Pygameのリソースを解放して終了します