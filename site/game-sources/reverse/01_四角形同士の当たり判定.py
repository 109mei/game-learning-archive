# coding: utf-8
"""
01_collision_rect_rect.py

このスクリプトでは、Pygame を使って四角形同士の当たり判定（コリジョン）を示します。
画面には２つの矩形が表示され、１つは矢印キーで操作でき、もう１つは固定されています。
矩形が重なった場合には画面上に「衝突しています」というテキストを表示し、
矩形の枠（境界ボックス）を可視化して当たり判定の理解を助けます。

各行には詳しいコメントを付け、初心者の方でも何をしているのか理解できるようにしました。
画面サイズは幅1280ピクセル、高さ720ピクセルに固定しています。
"""
# coding: utf-8
import sys
import numpy as np #行列等を使うためのモジュール
import time #数秒待つ等を使うためのモジュール
import random #ランダムを使うためのモジュール
import sys  # sysモジュールはOS判定やプラットフォーム情報を取得するために使用します
import pygame  # ゲームライブラリPygameを読み込みます
from pygame.locals import *  # Pygameの定数を直接参照できるようにします
import os  # osモジュールは環境変数の設定に利用します

# ---------- OSごとの表示設定 ----------
# いくつかのOSではDPIスケーリングやウィンドウの配置が異なるため、適切に設定します。
# DPIスケール無効化やウィンドウ位置センタリングなどを行います。
if sys.platform == "win32":  # Windows環境の場合の設定を行います
    import ctypes  # WindowsでのDPI設定変更に使用
    ctypes.windll.user32.SetProcessDPIAware()  # DPIスケールを無効にすることで拡大・縮小を避ける
    os.environ['SDL_VIDEO_CENTERED'] = '1'  # ウィンドウを画面中央に表示
elif sys.platform == "darwin":  # macOS環境の場合
    os.environ['SDL_VIDEO_WINDOW_POS'] = '100,100'  # macOSでウィンドウの左上座標を指定します
    os.environ['SDL_VIDEO_CENTERED'] = '1'  # macOSでウィンドウを中央に配置します
elif sys.platform.startswith("linux"):  # Linux環境の場合
    os.environ['SDL_VIDEO_X11_NET_WM_BYPASS_COMPOSITOR'] = '0'  # X11の合成オーバーレイを無効にします
    os.environ['SDL_VIDEO_CENTERED'] = '1'  # Linuxでウィンドウを中央に配置します
elif sys.platform.startswith("freebsd") or sys.platform.startswith("openbsd") or sys.platform.startswith("netbsd"):  # BSD系OSの場合
    os.environ['SDL_VIDEO_CENTERED'] = '1'  # BSD系でもウィンドウを中央に配置します
elif sys.platform.startswith("sunos"):  # Solaris系の場合
    os.environ['SDL_VIDEO_CENTERED'] = '1'  # Solarisでウィンドウを中央に配置します
elif sys.platform.startswith("haiku"):  # Haiku OSの場合
    os.environ['SDL_VIDEO_WINDOW_POS'] = '50,50'  # Haiku OSでウィンドウの左上位置を指定します
elif sys.platform.startswith("android"):  # Androidの場合
    os.environ['SDL_VIDEO_CENTERED'] = '1'  # Androidでウィンドウを中央に配置します
    os.environ['SDL_VIDEODRIVER'] = 'android'  # Android専用のビデオドライバーを指定します
elif sys.platform.startswith("emscripten"):  # WebAssembly環境の場合
    print("Emscripten (WebAssembly) 環境: 追加設定不要")  # Emscriptenでは特別な設定は不要です
elif sys.platform.startswith("cygwin") or sys.platform.startswith("msys"):  # CygwinやMSYS2環境の場合
    os.environ['SDL_VIDEO_CENTERED'] = '1'  # Cygwin/MSYS2でも中央に配置します
elif sys.platform.startswith("riscos"):  # RISC OS環境の場合
    os.environ['SDL_VIDEO_CENTERED'] = '1'  # RISC OSでも中央に配置します
elif sys.platform.startswith("aix"):  # IBM AIX環境の場合
    os.environ['SDL_VIDEO_CENTERED'] = '1'  # AIXでも中央に配置します
elif sys.platform.startswith("vwxorks"):  # VxWorks環境の場合
    os.environ['SDL_VIDEO_CENTERED'] = '1'  # VxWorksでも中央に配置します
elif sys.platform.startswith("os2"):  # OS/2環境の場合
    os.environ['SDL_VIDEO_CENTERED'] = '1'  # OS/2でも中央に配置します
elif sys.platform.startswith("amiga"):  # AmigaOSまたはMorphOSの場合
    os.environ['SDL_VIDEO_CENTERED'] = '1'  # Amiga系でも中央に配置します
else:  # 上記のいずれにも該当しない未知のOSの場合
    # 未知のOSの場合は警告を表示しますが、処理は継続します。
    print(f"警告: このOS（{sys.platform}）は未検証です。動作しない可能性があります。")  # 警告メッセージを標準出力に表示します

# ---------- 画面サイズとフォント設定 ----------
W, H = 1280, 720  # 画面の幅(W)と高さ(H)を指定します。タプル(1280, 720)が set_mode の引数になります。
FONT_PATH = "NotoSansJP-Regular.ttf"  # 日本語表示用フォントファイルのパス。存在しない場合は適宜置き換えてください。
FONT_SIZE = 28  # フォントサイズを指定します。

# ---------- Pygameの初期化 ----------
pygame.init()  # Pygame全体を初期化します。必須です。
screen = pygame.display.set_mode((W, H))  # 画面を作成します。引数は(幅, 高さ)のタプルです【848242811292111†L244-L254】。
pygame.display.set_caption("01 矩形同士の当たり判定")  # ウィンドウのタイトルバーに表示される文字列を設定します。

# ---------- フォントのロード ----------
try:  # 指定したフォントファイルの読み込みを試みます
    font = pygame.font.Font(FONT_PATH, FONT_SIZE)  # 指定したフォントファイルとサイズでフォントオブジェクトを生成します。
except IOError:  # フォントファイルが読み込めない場合の例外処理
    # フォントが読み込めない場合はデフォルトフォントを使用します。
    font = pygame.font.SysFont(None, FONT_SIZE)  # システムデフォルトフォントを取得します
    print("警告: 指定したフォントが見つかりません。デフォルトフォントを使用します。")  # 標準出力に警告を表示します

# ---------- 色の定義 ----------
# 色はRGB(A)の4要素またはRGBの3要素のタプルで指定します【792189879171763†L71-L79】。
# 赤、緑、青は0〜255の整数値で指定し、アルファ値は255で不透明を意味します【276529072627999†L90-L95】。
WHITE = (255, 255, 255)  # 背景用の白色
RED = (250, 140, 80)  # 固定四角形用の色 (R=250, G=140, B=80)
BLUE = (80, 170, 250)  # 操作可能な四角形用の色
GREEN = (80, 250, 140)  # 衝突時に変更する色

# ---------- 矩形データの初期化 ----------
rect_static = pygame.Rect(500, 300, 200, 150)  # 固定四角形：左上位置(x=500,y=300) 幅200 高さ150のRectを作成
rect_movable = pygame.Rect(100, 100, 150, 100)  # 移動可能な四角形：初期位置(x=100,y=100) 幅150 高さ100
speed = 5  # 移動速度。矢印キーを押したときに四角形が移動するピクセル数

# ---------- メインループ ----------
running = True  # ループ継続フラグ（Trueの間ゲームループを継続します）
clock = pygame.time.Clock()  # FPS制御用のClockオブジェクトを作成

while running:  # メインループ本体：runningがTrueの間繰り返します
    clock.tick(60)  # 1秒間に最大60回の処理になるように待機します（FPS制御）

    # イベント処理: キー入力やウィンドウを閉じる操作を処理します
    for event in pygame.event.get():  # イベントキューから順にイベントを取得して処理します
        if event.type == QUIT:  # ウィンドウの×ボタンなどでQUITイベントが発生した場合
            running = False  # ループを終了させます

    # キー状態の取得：押されているキーに応じて矩形を移動させます
    keys = pygame.key.get_pressed()  # 押されているキーの状態を辞書形式で取得
    if keys[K_LEFT]:  # 左矢印キーが押されているか
        rect_movable.x -= speed  # x座標を減少させる（左に移動）
    if keys[K_RIGHT]:  # 右矢印キーが押されているか
        rect_movable.x += speed  # x座標を増加させる（右に移動）
    if keys[K_UP]:  # 上矢印キーが押されているか
        rect_movable.y -= speed  # y座標を減少させる（上に移動）
    if keys[K_DOWN]:  # 下矢印キーが押されているか
        rect_movable.y += speed  # y座標を増加させる（下に移動）

    # 画面のクリア：毎フレーム背景色で塗りつぶして描画内容をリセットします
    screen.fill(WHITE)  # Surface.fill()は指定した色で画面全体を塗りつぶします

    # 衝突判定：2つのRectが重なっているか判定します【880888389410395†L137-L146】。
    collided = rect_movable.colliderect(rect_static)  # colliderect()は重なっていればTrueを返します【880888389410395†L137-L146】

    # 矩形の描画：draw.rect関数で矩形を描画します【792189879171763†L115-L124】。
    # border_radius引数に値を指定すると角丸の矩形を描画できます【792189879171763†L140-L149】。
    pygame.draw.rect(screen, RED if not collided else GREEN, rect_static, border_radius=8)  # 固定矩形を描画
    pygame.draw.rect(screen, BLUE if not collided else GREEN, rect_movable, border_radius=8)  # 移動矩形を描画

    # 枠線の描画：内側が空の矩形枠を描画するには width 引数に1以上の値を渡します【792189879171763†L123-L130】。
    pygame.draw.rect(screen, (0, 0, 0), rect_static, width=2, border_radius=8)  # 黒色の枠線を描画
    pygame.draw.rect(screen, (0, 0, 0), rect_movable, width=2, border_radius=8)  # 移動矩形の枠線を描画します

    # 衝突している場合はテキストを描画
    if collided:  # 当たり判定結果が真の場合
        text_surface = font.render("衝突しています!", True, (200, 0, 0))  # 第2引数のTrueはアンチエイリアス有効【792189879171763†L115-L124】
        # (True)を(False)にするとアンチエイリアスが無効になり、文字がギザギザになります。
        # 第3引数は文字色のRGBタプルです。
        screen.blit(text_surface, (50, 50))  # blit()でテキストサーフェスを描画します

    # 説明テキストの描画
    info_lines = [  # 説明文を格納するリストを定義します
        "←↑→↓キーで青い矩形を移動",  # 操作方法を説明するテキスト
        "四角形が重なると色が緑になり、'衝突しています!'と表示"  # 衝突時の挙動を説明するテキスト
    ]  # 説明用のテキストを格納するリストを定義します
    # 複数行のテキストを1行ずつ描画します
    for i, line in enumerate(info_lines):  # 各テキストとそのインデックスを取得します
        surface = font.render(line, True, (0, 0, 0))  # テキストをSurfaceに変換します
        screen.blit(surface, (50, H - 80 + i * 30))  # 下部にテキストを描画します

    # 画面を更新：draw後にflip()を呼ぶことで表示が更新されます【848242811292111†L332-L339】。
    pygame.display.flip()  # フロントバッファとバックバッファを入れ替えて画面を更新します

# メインループを抜けたらPygameを終了します
pygame.quit()  # Pygameの各モジュールをクリーンアップして終了します