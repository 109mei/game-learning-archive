# coding: utf-8
"""
24_smooth_follow.py

スムーズ追従の例です。円がマウスカーソルをなめらかに追いかけます。追従には線形補間（lerp）
を使用し、毎フレーム位置を少しずつ目標に近づけます。
"""

import sys  # sysモジュールはプラットフォーム判定に使用します
import pygame  # Pygameライブラリを読み込みます
from pygame.locals import *  # イベント定数を直接参照できるようにします
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
FONT_SIZE = 24  # フォントサイズを指定します

pygame.init()  # Pygameを初期化します
screen = pygame.display.set_mode((W, H))  # 指定サイズのウィンドウを作成します
pygame.display.set_caption("24 スムーズ追従")  # ウィンドウタイトルを設定します

try:  # 指定したフォントを読み込みます
    font = pygame.font.Font(FONT_PATH, FONT_SIZE)  # 日本語フォントオブジェクトを生成
except IOError:  # 読み込めない場合は
    font = pygame.font.SysFont(None, FONT_SIZE)  # デフォルトフォントを使用します

# 追従する円の初期位置
follower = [W/2, H/2]  # 円の現在位置(x,y)をリストで保持
radius = 30  # 円の半径
smooth_factor = 0.1  # 0<値<1: 小さいほどゆっくり追従する係数

clock = pygame.time.Clock()  # FPS制御用のClockオブジェクト
running = True  # メインループ継続フラグ
while running:  # メインループ開始
    clock.tick(60)  # 1秒間に60回までループを実行します
    for event in pygame.event.get():  # イベントキューからイベントを取得
        if event.type == QUIT:  # ウィンドウの×ボタンが押された場合
            running = False  # ループを終了します

    target = pygame.mouse.get_pos()  # 目標位置(マウス)を取得
    # 線形補間(lerp)計算: follower += (target - follower) * factor
    follower[0] += (target[0] - follower[0]) * smooth_factor  # x座標を少し目標に近づける
    follower[1] += (target[1] - follower[1]) * smooth_factor  # y座標を少し目標に近づける

    screen.fill((255, 255, 255))  # 画面を白色で塗りつぶします
    pygame.draw.circle(screen, (250, 120, 120), (int(follower[0]), int(follower[1])), radius)  # 円を描画
    # ガイドメッセージを描画
    guide1 = font.render("マウスカーソルに円がスムーズに追従します", True, (0, 0, 0))  # ガイドテキストを生成
    screen.blit(guide1, (20, 20))  # テキストを画面に描画
    pygame.display.flip()  # 画面を更新します

pygame.quit()  # Pygameを終了してリソースを解放します