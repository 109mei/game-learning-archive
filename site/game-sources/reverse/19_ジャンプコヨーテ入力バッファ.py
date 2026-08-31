# coding: utf-8
"""
19_jump_coyote_buffer.py

ジャンプにコヨーテタイムと入力バッファを導入した例です。キャラクターは地面に接している際に
スペースキーでジャンプしますが、地面から離れて少しの間(コヨーテタイム)はジャンプが許可され、
着地直前にジャンプキーを押してもバッファ時間内であればジャンプが実行されます。
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
FONT_SIZE = 24  # フォントサイズを指定します

pygame.init()  # Pygameを初期化します
screen = pygame.display.set_mode((W, H))  # 指定サイズのウィンドウを作成します
pygame.display.set_caption("19 ジャンプ: コヨーテタイム＋入力バッファ")  # ウィンドウタイトルを設定します

try:  # フォント読み込みを試みます
    font = pygame.font.Font(FONT_PATH, FONT_SIZE)  # 指定フォントを読み込みます
except IOError:  # フォントが読み込めない場合
    font = pygame.font.SysFont(None, FONT_SIZE)  # デフォルトフォントを使用します

# キャラクター設定
player_rect = pygame.Rect(200, H - 100, 50, 50)  # プレイヤーの矩形(x,y,width,height)
vel_y = 0.0  # 垂直方向の速度
gravity = 900.0  # 重力加速度(px/s^2)
jump_velocity = -400.0  # ジャンプ初速度(負値は上方向)
coyote_time = 0.15  # コヨーテタイム(秒): 地面から離れてもジャンプできる猶予
jump_buffer = 0.15  # ジャンプ入力バッファ(秒): 着地前の入力猶予
coyote_timer = 0.0  # 現在のコヨーテタイマー
buffer_timer = 0.0  # 現在のバッファタイマー
on_ground = False  # 接地しているかどうかのフラグ

# 地面
ground_rect = pygame.Rect(0, H - 50, W, 50)  # 画面下部に地面の矩形を作成

clock = pygame.time.Clock()  # FPS制御用のClockオブジェクト
running = True  # メインループ継続フラグ
while running:  # メインループ開始
    dt = clock.tick(60) / 1000.0  # フレーム経過時間(秒)を取得し60FPSに制限
    for event in pygame.event.get():  # イベントキューからイベントを取得
        if event.type == QUIT:  # ウィンドウの×ボタンが押された場合
            running = False  # ループを終了します
        elif event.type == KEYDOWN and event.key == K_SPACE:  # Spaceキーが押された場合
            # ジャンプキーを押したらバッファタイマーをセット
            buffer_timer = jump_buffer  # バッファタイマーにジャンプ猶予を設定

    # 接地判定: プレイヤーの底が地面と接触しているかを判定
    on_ground = player_rect.bottom >= ground_rect.top and vel_y >= 0  # 接地判定: 下端が地面に接触し速度が上向きでない
    if on_ground:  # 接地している場合
        coyote_timer = coyote_time  # 接地中にコヨーテタイマーをリセット
        player_rect.bottom = ground_rect.top  # プレイヤーを地面の上に揃える
        vel_y = 0  # 垂直速度をリセット
    else:  # 接地していない場合
        coyote_timer = max(coyote_timer - dt, 0)  # 空中ではタイマーを減少

    # ジャンプ実行判定
    if buffer_timer > 0:  # ジャンプ入力がバッファに残っているか
        if on_ground or coyote_timer > 0:  # 地面にいるか、コヨーテタイム内ならジャンプを許可
            vel_y = jump_velocity  # ジャンプ初速度を設定
            buffer_timer = 0  # バッファを消費
        else:  # ジャンプできないときはバッファを減らす
            buffer_timer -= dt  # まだジャンプできない場合はバッファ時間を減少

    # 重力による速度更新と位置更新
    vel_y += gravity * dt  # 重力を速度に加算
    player_rect.y += vel_y * dt  # 速度に基づいて位置を更新

    # 画面外に出ないように: 地面を突き抜けないよう調整
    if player_rect.bottom > ground_rect.top:  # プレイヤーが地面を突き抜けたか判定
        player_rect.bottom = ground_rect.top  # 地面の上に戻す
        vel_y = 0  # 落下速度をリセット

    # 描画処理
    screen.fill((30, 30, 30))  # 背景を暗い色で塗りつぶします
    # 地面
    pygame.draw.rect(screen, (100, 60, 60), ground_rect)  # 地面を描画します
    # プレイヤー
    pygame.draw.rect(screen, (100, 200, 100), player_rect)  # プレイヤーを描画します
    # テキスト
    lines = [  # 説明文のリストを定義します
        "Spaceキーでジャンプ",  # 説明1: ジャンプ操作方法
        "コヨーテタイム: 地面から離れても少しの間ジャンプ可能",  # 説明2: コヨーテタイムの内容
        "ジャンプバッファ: 着地直前にキーを押してもジャンプ実行"  # 説明3: ジャンプバッファの説明
    ]  # リスト定義終了
    for i, l in enumerate(lines):  # 各行を描画
        txt = font.render(l, True, (230, 230, 230))  # テキストSurfaceを生成
        screen.blit(txt, (20, 20 + i*30))  # 画面に描画
    pygame.display.flip()  # 画面を更新して描画内容を表示します

pygame.quit()  # Pygameのリソースを解放して終了します