# coding: utf-8
"""
31_loop_basics.py

このスクリプトでは、Python の for ループと while ループの基礎を紹介します。for ループを
使って複数の円を生成・描画し、矢印キーでそれらすべてを同時に動かします。また、メイン
ループ自体が while ループであることを示し、ゲーム処理が毎フレーム繰り返し実行される
様子を学習できます。各行にコメントを付けているので、初心者の方でも繰り返し処理の考え
方を理解しやすくなっています。
"""

import sys  # sysモジュールはプラットフォーム判定に使用します
import pygame  # ゲームライブラリ Pygame を読み込みます
from pygame.locals import *  # キー定数やQUITイベントを直接参照できるようにします
import os  # 環境変数の設定に利用します

# ---------- OS設定 ----------
# 各OSでのDPIスケール設定とウィンドウの中央配置を行います
if sys.platform == "win32":  # Windows環境の場合
    import ctypes  # Windows API呼び出し用モジュールを読み込み
    ctypes.windll.user32.SetProcessDPIAware()  # DPIスケーリングを無効にして拡大縮小を防止します
    os.environ['SDL_VIDEO_CENTERED'] = '1'  # ウィンドウを中央に配置するよう環境変数を設定します
else:  # Windows以外のOSの場合
    os.environ['SDL_VIDEO_CENTERED'] = '1'  # 他のOSでもウィンドウを中央に配置します

# ---------- 画面サイズとフォント設定 ----------
W, H = 1280, 720  # 画面の幅(W)と高さ(H)を指定します
FONT_PATH = "NotoSansJP-Regular.ttf"  # 使用する日本語フォントファイルのパス
FONT_SIZE = 24  # フォントサイズを指定します

# ---------- Pygameの初期化 ----------
pygame.init()  # Pygame全体を初期化します
screen = pygame.display.set_mode((W, H))  # 指定サイズのウィンドウを作成します
pygame.display.set_caption("31 繰り返しの基礎")  # ウィンドウタイトルを設定します

# ---------- フォントのロード ----------
try:  # フォント読み込みを試みます
    font = pygame.font.Font(FONT_PATH, FONT_SIZE)  # 指定したフォントファイルを読み込みます
except IOError:  # フォントが読み込めない場合
    font = pygame.font.SysFont(None, FONT_SIZE)  # デフォルトフォントを使用します

# ---------- 円の初期位置を生成 ----------
circle_positions = []  # 円の位置を保持するリストを初期化します
for i in range(10):  # 0から9までの10個に対して繰り返します
    x = 100 + i * 100  # 各円のx座標を計算します (100px間隔)
    y = H // 2  # 円のy座標は画面中央に固定します
    circle_positions.append([x, y])  # 計算した座標をリストに追加します

speed = 5  # 円の移動速度(pixels/frame)

# ---------- 時計とループ制御 ----------
clock = pygame.time.Clock()  # FPS制御用のClockオブジェクトを生成します
running = True  # メインループの継続フラグを設定します
while running:  # whileループでメインループを開始します
    clock.tick(60)  # 1秒間に60回までループを実行します
    for event in pygame.event.get():  # イベントキューからイベントを取り出します
        if event.type == QUIT:  # ウィンドウの×ボタンが押された場合
            running = False  # ループを終了します

    # ---------- キー入力処理 ----------
    keys = pygame.key.get_pressed()  # 押されているキーの状態を取得します
    if keys[K_LEFT]:  # 左矢印キーが押されている場合
        for pos in circle_positions:  # 各円の座標をforループで更新します
            pos[0] -= speed  # x座標を減少させて左に移動します
    if keys[K_RIGHT]:  # 右矢印キーが押されている場合
        for pos in circle_positions:  # 各円の座標を更新します
            pos[0] += speed  # x座標を増加させて右に移動します

    # ---------- 画面描画 ----------
    screen.fill((240, 240, 240))  # 背景を明るいグレーで塗りつぶします
    # 円を描画します。forループでリスト内のすべての円を描きます
    for pos in circle_positions:  # 各円の座標を反復します
        pygame.draw.circle(screen, (100, 150, 240), pos, 30)  # 指定した色と半径で円を描きます

    # テキストを表示します。forループとwhileループについての説明文をリストにまとめます
    lines = [
        "forループ: range(10)を使って10個の円を生成・描画",  # forループの説明
        "矢印キーで全ての円を左右に移動 (forループでリストの要素を更新)",  # 移動処理の説明
        "メインループはwhile running: で繰り返し実行しています"  # whileループの説明
    ]
    for i, line in enumerate(lines):  # 行番号と内容でforループ
        txt = font.render(line, True, (0, 0, 0))  # テキストを描画サーフェスに変換します
        screen.blit(txt, (20, 20 + i * 30))  # テキストを順に表示します

    pygame.display.flip()  # 描画内容を画面に反映させます

# ---------- 終了処理 ----------
pygame.quit()  # Pygameを終了し、リソースを解放します