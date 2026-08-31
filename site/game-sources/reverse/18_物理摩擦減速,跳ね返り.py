# coding: utf-8
"""
18_physics_friction.py

加速と摩擦による減速を示す例です。矢印キーを押して加速し、キーを離すと摩擦によって
物体(ボール)が徐々に止まります。速度や位置の計算を通じて基本的な物理シミュレーションを
体験できます。
"""

import sys  # sysモジュールはプラットフォーム判定に使用します
import pygame  # Pygameライブラリを読み込みます
from pygame.locals import *  # キー定数やQUITイベントを直接参照できるようにします
import os  # 環境変数設定に使用します

# OS設定
if sys.platform == "win32":  # Windows環境の場合
    import ctypes  # Windows API呼び出し用モジュール
    ctypes.windll.user32.SetProcessDPIAware()  # DPIスケーリングを無効にします
    os.environ['SDL_VIDEO_CENTERED'] = '1'  # ウィンドウを中央に配置します
else:  # Windows以外のOSの場合
    os.environ['SDL_VIDEO_CENTERED'] = '1'  # ウィンドウを中央に配置します

W, H = 1280, 720  # 画面の幅と高さを指定します
FONT_PATH = "NotoSansJP-Regular.ttf"  # 日本語フォントのパス
FONT_SIZE = 28  # フォントサイズを指定します

pygame.init()  # Pygameを初期化します
screen = pygame.display.set_mode((W, H))  # 指定サイズのウィンドウを作成します
pygame.display.set_caption("18 物理加速＋摩擦")  # ウィンドウタイトルを設定します

try:  # フォント読み込みを試みます
    font = pygame.font.Font(FONT_PATH, FONT_SIZE)  # 指定フォントを読み込みます
except IOError:  # フォントが見つからない場合
    font = pygame.font.SysFont(None, FONT_SIZE)  # デフォルトフォントを使用します

# ボール状態
pos = [W/2, H/2]  # ボールの初期位置を画面中央に設定します
vel = [0.0, 0.0]  # ボールの初期速度(x, y)
acc = 300.0  # 加速度 (ピクセル/秒^2)
friction = 0.9  # 摩擦係数: 速度を毎フレームこの係数で乗算します
radius = 30  # ボールの半径(ピクセル)

clock = pygame.time.Clock()  # FPS制御用のClockオブジェクトを作成します
running = True  # メインループ継続フラグ
while running:  # メインループ開始
    dt = clock.tick(60) / 1000.0  # 前フレームからの経過時間(秒)を取得し、60FPSに制限
    for event in pygame.event.get():  # イベントキューからイベントを取得
        if event.type == QUIT:  # ウィンドウの×ボタンが押された場合
            running = False  # ループを終了します

    # 入力による加速度
    keys = pygame.key.get_pressed()  # 押されているキーの状態を取得します
    if keys[K_LEFT]:  # 左矢印キーが押されている場合
        vel[0] -= acc * dt  # x方向に負の加速度を加えます
    if keys[K_RIGHT]:  # 右矢印キーが押されている場合
        vel[0] += acc * dt  # x方向に正の加速度を加えます
    if keys[K_UP]:  # 上矢印キーが押されている場合
        vel[1] -= acc * dt  # y方向に負の加速度を加えます
    if keys[K_DOWN]:  # 下矢印キーが押されている場合
        vel[1] += acc * dt  # y方向に正の加速度を加えます

    # 摩擦による減速: 速度に係数をかけます
    vel[0] *= friction  # x速度に摩擦を適用します
    vel[1] *= friction  # y速度に摩擦を適用します

    # 位置の更新
    pos[0] += vel[0] * dt * 60  # dt*60で1秒当たりの速度に近似して位置を更新します
    pos[1] += vel[1] * dt * 60  # y座標も同様に更新します
    # 画面端で跳ね返り
    if pos[0] - radius < 0 or pos[0] + radius > W:  # 左右の壁に衝突したか確認します
        vel[0] *= -1  # 左右の壁に当たった場合はx速度の符号を反転させます
    if pos[1] - radius < 0 or pos[1] + radius > H:  # 上下の壁に衝突したか確認します
        vel[1] *= -1  # 上下の壁に当たった場合はy速度の符号を反転させます

    # 描画
    screen.fill((10, 20, 30))  # 背景を暗い色で塗りつぶします
    pygame.draw.circle(screen, (150, 220, 150), (int(pos[0]), int(pos[1])), radius)  # ボールを描画します
    # 速度表示
    speed_text = font.render(f"速度: ({vel[0]:.2f}, {vel[1]:.2f})", True, (230, 230, 230))  # 速度テキストを生成
    screen.blit(speed_text, (20, 20))  # 速度テキストを画面に表示します
    guide = font.render("矢印キーで加速、離すと摩擦で減速します", True, (200, 200, 200))  # ガイドテキストを生成します
    screen.blit(guide, (20, 60))  # ガイドテキストを画面に表示します
    pygame.display.flip()  # 画面を更新して描画内容を表示します

pygame.quit()  # Pygameのリソースを解放して終了します