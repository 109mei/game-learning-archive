# coding: utf-8
"""
30_fps_state_overlay.py

FPSとプレイヤーの座標や状態をオーバーレイ表示する例です。画面右上に現在のFPS値を表示し、
画面左上にはプレイヤーの座標と速度を表示します。矢印キーでプレイヤーを移動すると数値が更新
される様子が分かります。
"""

import sys  # sysモジュールはプラットフォーム判定に使用します
import pygame  # ゲームライブラリPygameを読み込みます
from pygame.locals import *  # キー定数やQUITイベントを直接参照できるようにします
import os  # 環境変数の設定に利用します

# ---------- OS設定 ----------
# 各OSでのDPIスケール設定とウィンドウの中央配置を行います
if sys.platform == "win32":  # Windows環境の場合
    import ctypes  # Windows API呼び出し用モジュールを読み込み
    ctypes.windll.user32.SetProcessDPIAware()  # DPIスケーリングを無効にして拡大縮小を防止します
    os.environ['SDL_VIDEO_CENTERED'] = '1'  # ウィンドウを中央に配置するよう環境変数を設定します
else:  # Windows以外のOSの場合
    os.environ['SDL_VIDEO_CENTERED'] = '1'  # Windows以外のOSでもウィンドウを中央に配置します

# ---------- 画面サイズとフォント設定 ----------
W, H = 1280, 720  # 画面の幅(W)と高さ(H)を指定します
FONT_PATH = "NotoSansJP-Regular.ttf"  # 使用する日本語フォントファイルのパス
FONT_SIZE = 24  # フォントサイズを指定します

# ---------- Pygameの初期化 ----------
pygame.init()  # Pygame全体を初期化します
screen = pygame.display.set_mode((W, H))  # 指定サイズのウィンドウを作成します
pygame.display.set_caption("30 FPS表示＆座標/状態オーバーレイ")  # ウィンドウタイトルを設定します

# ---------- フォントのロード ----------
try:  # フォント読み込みを試みます
    # 指定したフォントファイルを読み込み、フォントオブジェクトを作成
    font = pygame.font.Font(FONT_PATH, FONT_SIZE)  # フォントファイルを読み込んでフォントオブジェクトを生成
except IOError:  # フォントが読み込めない場合
    # フォント読み込みに失敗した場合、デフォルトフォントを使用します
    font = pygame.font.SysFont(None, FONT_SIZE)  # システムデフォルトのフォントを使用

# ---------- プレイヤーの設定 ----------
player_rect = pygame.Rect(W // 2, H // 2, 60, 60)  # プレイヤー矩形の初期位置とサイズ
player_speed = 7  # プレイヤーの移動速度(pixels/frame)
velocity = [0, 0]  # 各フレームで計算する速度ベクトル [x方向速度, y方向速度]

# ---------- 時計とループ制御 ----------
clock = pygame.time.Clock()  # FPS制御用のClockオブジェクト
running = True  # メインループ継続フラグ
while running:  # メインループを開始します
    dt_ms = clock.tick(60)  # 1秒間に60回までループを実行し、経過時間(ms)を取得
    fps = clock.get_fps()  # 現在のFPS値を取得します
    for event in pygame.event.get():  # イベントキューからイベントを取得します
        if event.type == QUIT:  # ウィンドウの×ボタンが押された場合
            running = False  # ループを終了させます

    # ---------- キー入力による速度更新 ----------
    keys = pygame.key.get_pressed()  # 押されているキーの状態を取得します
    velocity = [0, 0]  # 各フレームで速度をリセットします
    if keys[K_LEFT]:  # 左矢印キーが押されている場合
        velocity[0] = -player_speed  # x方向速度を負値に設定します（左移動）
    if keys[K_RIGHT]:  # 右矢印キーが押されている場合
        velocity[0] = player_speed  # x方向速度を正値に設定します（右移動）
    if keys[K_UP]:  # 上矢印キーが押されている場合
        velocity[1] = -player_speed  # y方向速度を負値に設定します（上移動）
    if keys[K_DOWN]:  # 下矢印キーが押されている場合
        velocity[1] = player_speed  # y方向速度を正値に設定します（下移動）

    # ---------- 位置更新と画面端制限 ----------
    player_rect.x += velocity[0]  # x座標を更新します
    player_rect.y += velocity[1]  # y座標を更新します
    # 画面の端に出ないように範囲内に制限します
    player_rect.x = max(0, min(W - player_rect.w, player_rect.x))  # x座標を0から画面幅-プレイヤー幅の範囲に制限
    player_rect.y = max(0, min(H - player_rect.h, player_rect.y))  # y座標を0から画面高さ-プレイヤー高さの範囲に制限

    # ---------- 描画処理 ----------
    screen.fill((220, 230, 240))  # 背景を淡い色で塗りつぶします
    pygame.draw.rect(screen, (100, 150, 250), player_rect, border_radius=8)  # プレイヤー矩形を描画します
    # FPSのオーバーレイ表示
    fps_text = font.render(f"FPS: {fps:.2f}", True, (0, 0, 0))  # FPS値を文字列にして描画サーフェスを生成
    screen.blit(fps_text, (W - fps_text.get_width() - 20, 20))  # 右上にFPS表示を描画します
    # プレイヤー座標と速度のオーバーレイ表示
    pos_text = font.render(f"位置: ({player_rect.x}, {player_rect.y})", True, (0, 0, 0))  # 位置情報を描画サーフェスに
    vel_text = font.render(f"速度: ({velocity[0]}, {velocity[1]})", True, (0, 0, 0))  # 速度情報を描画サーフェスに
    screen.blit(pos_text, (20, 20))  # 画面左上に位置情報を表示
    screen.blit(vel_text, (20, 50))  # 位置の下に速度情報を表示
    # 操作ガイドの表示
    guide = font.render("矢印キーでプレイヤーを移動", True, (0, 0, 0))  # ガイドテキストを描画サーフェスに
    screen.blit(guide, (20, H - 40))  # 画面下部にガイドを表示
    pygame.display.flip()  # 描画内容を画面に反映させます

# ---------- 終了処理 ----------
pygame.quit()  # Pygameを終了し、リソースを解放します