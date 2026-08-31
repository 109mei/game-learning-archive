# coding: utf-8
"""
02_shapes_move.py

丸（円）、四角（矩形）、三角（多角形）を画面上に表示し、矢印キーでそれぞれの位置を移動させるサンプルです。
Pygame の基本的な図形描画関数を用います。
初心者が理解しやすいように、各行に詳しいコメントを付けています。

画面サイズは1280x720ピクセルです。
"""

import sys  # sysモジュールはOS判定などに使用します
import pygame  # Pygameライブラリを読み込みます
from pygame.locals import *  # Pygameの定数を直接参照できるようにします
import os  # 環境変数の設定やOS固有の処理に使用します

# ---------- OSごとの表示設定 ----------
# 各OSでウィンドウサイズやDPIスケールが異なるため、
# 適切にDPI無効化やウィンドウの中央配置設定を行います。
if sys.platform == "win32":  # Windows環境の場合
    import ctypes  # ctypesでWindowsのシステムAPIを呼び出します
    ctypes.windll.user32.SetProcessDPIAware()  # DPIスケールを無効化して拡大縮小を防ぎます
    os.environ['SDL_VIDEO_CENTERED'] = '1'  # ウィンドウを中央に配置します
elif sys.platform == "darwin":  # macOS環境の場合
    os.environ['SDL_VIDEO_WINDOW_POS'] = '100,100'  # ウィンドウの表示位置を指定します
    os.environ['SDL_VIDEO_CENTERED'] = '1'  # ウィンドウを中央に配置します
elif sys.platform.startswith("linux"):  # Linux環境の場合
    os.environ['SDL_VIDEO_X11_NET_WM_BYPASS_COMPOSITOR'] = '0'  # Compositorのバイパス設定
    os.environ['SDL_VIDEO_CENTERED'] = '1'  # ウィンドウを中央に配置します
else:  # 上記のいずれのOSにも該当しない場合
    # その他のOSでは中央配置のみ行います
    os.environ['SDL_VIDEO_CENTERED'] = '1'  # ウィンドウを中央に配置します

# ---------- 画面サイズとフォント ----------
W, H = 1280, 720  # ゲームウィンドウの幅と高さを指定します
FONT_PATH = "NotoSansJP-Regular.ttf"  # 日本語フォントのパスを指定します
FONT_SIZE = 24  # 文字の大きさを指定します

# ---------- Pygame初期化 ----------
pygame.init()  # Pygameのすべてのモジュールを初期化します
screen = pygame.display.set_mode((W, H))  # 指定した幅と高さで画面を生成します
pygame.display.set_caption("02 図形の表示と移動")  # ウィンドウタイトルを設定します

# ---------- フォント読み込み ----------
try:  # 指定したフォントファイルからフォントを読み込む処理です
    font = pygame.font.Font(FONT_PATH, FONT_SIZE)  # 指定されたフォントファイルとサイズでフォントを生成します
except IOError:  # フォントが存在しない場合は例外が発生します
    # フォントが見つからない場合はシステムのデフォルトフォントを使用します
    font = pygame.font.SysFont(None, FONT_SIZE)  # デフォルトフォントを取得します
    print("警告: フォントが見つからないためデフォルトフォントを使用します。")  # 警告を表示します

# ---------- 色定義 ----------
WHITE = (255, 255, 255)  # 背景などに使う白
RED = (255, 100, 100)  # 円の色
GREEN = (100, 255, 100)  # 矩形の色
BLUE = (100, 100, 255)  # 三角形の色
BLACK = (0, 0, 0)  # テキスト表示に使う黒

# ---------- 図形の初期位置とサイズ ----------
circle_pos = [200, 200]  # 円の中心位置を(x, y)で指定します
circle_radius = 50  # 円の半径を指定します
rect_pos = [500, 200]  # 矩形の左上の座標を指定します
rect_size = [120, 80]  # 矩形の幅と高さを指定します
triangle_pos = [800, 200]  # 三角形の基準位置を指定します
triangle_points = [  # 三角形を構成する3頂点のリストを定義します
    [triangle_pos[0], triangle_pos[1]],  # 三角形の1つ目の頂点
    [triangle_pos[0] + 60, triangle_pos[1] + 100],  # 三角形の2つ目の頂点
    [triangle_pos[0] - 60, triangle_pos[1] + 100]  # 三角形の3つ目の頂点
]  # ここまでで三角形の頂点をまとめています
speed = 5  # 矢印キーを押した際の移動速度（ピクセル数）

# ---------- メインループ ----------
clock = pygame.time.Clock()  # FPS制御用のClockオブジェクトを作成します
running = True  # ゲームループ継続フラグ
while running:  # メインループがTrueの間繰り返します
    clock.tick(60)  # 1秒あたり最大60フレームに制限します
    for event in pygame.event.get():  # キューに入っているイベントを処理します
        if event.type == QUIT:  # ウィンドウの×ボタンが押された場合
            running = False  # ループを終了します

    # キーの取得: 現在押されているキーの状態を辞書形式で取得します
    keys = pygame.key.get_pressed()  # 現在押されているすべてのキーの状態を取得します
    # 左右移動処理
    if keys[K_LEFT]:  # 左矢印キーが押されている場合
        circle_pos[0] -= speed  # 円のx座標を左へ移動します
        rect_pos[0] -= speed  # 矩形も左へ移動します
        for pt in triangle_points:  # 三角形の各頂点も左へ移動します
            pt[0] -= speed  # 各頂点のx座標を左に移動します
    if keys[K_RIGHT]:  # 右矢印キーが押されている場合
        circle_pos[0] += speed  # 円のx座標を右へ移動します
        rect_pos[0] += speed  # 矩形も右へ移動します
        for pt in triangle_points:  # 三角形の各頂点も右へ移動します
            pt[0] += speed  # 各頂点のx座標を右に移動します
    # 上下移動処理
    if keys[K_UP]:  # 上矢印キーが押されている場合
        circle_pos[1] -= speed  # 円のy座標を上へ移動します
        rect_pos[1] -= speed  # 矩形も上へ移動します
        for pt in triangle_points:  # 三角形の各頂点も上へ移動します
            pt[1] -= speed  # 各頂点のy座標を上に移動します
    if keys[K_DOWN]:  # 下矢印キーが押されている場合
        circle_pos[1] += speed  # 円のy座標を下へ移動します
        rect_pos[1] += speed  # 矩形も下へ移動します
        for pt in triangle_points:  # 三角形の各頂点も下へ移動します
            pt[1] += speed  # 各頂点のy座標を下に移動します

    # 背景の塗りつぶし: 毎フレーム最初に画面を白色で塗りつぶします
    screen.fill(WHITE)  # 背景を白色で塗りつぶして前フレームの描画を消去します

    # 円の描画: Surface, 色, 中心座標, 半径を指定します
    pygame.draw.circle(screen, RED, circle_pos, circle_radius)  # 赤色の円を描画します
    # 矩形の描画: Surface, 色, Rectオブジェクト(左上座標とサイズ)を指定します
    pygame.draw.rect(screen, GREEN, pygame.Rect(rect_pos, rect_size), border_radius=8)  # 緑色の矩形を角丸で描画します
    # 三角形の描画: polygon関数に頂点リストを渡します
    pygame.draw.polygon(screen, BLUE, triangle_points)  # 青色の三角形を描画します

    # 説明文の表示: 操作方法などのガイドを画面下部に描画します
    info_lines = [  # 画面下部に表示するガイドテキストのリスト
        "←→↑↓キーで全ての図形を移動できます。",  # 操作方法を説明するテキスト
        "赤: 円, 緑: 矩形, 青: 三角形"  # 各色の図形が何を表すかを説明するテキスト
    ]  # info_linesリストの終わり
    for i, line in enumerate(info_lines):  # 各行テキストを描画します
        txt = font.render(line, True, BLACK)  # テキストをレンダリングします
        screen.blit(txt, (30, H - 60 + i * 30))  # 描画位置を指定して表示します

    pygame.display.flip()  # 画面全体を更新して描画内容を反映します

# ループ終了後はPygameを終了します
pygame.quit()  # 初期化したPygameのリソースを解放して終了します