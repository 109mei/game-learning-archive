# coding: utf-8
"""
03_image_place_and_move.py

画像を画面に配置し、右矢印キーを押すと画像が右に移動するサンプルです。
このファイルでは背景画像とプレイヤー画像を読み込み、それぞれを画面に描画します。
指定されたファイルパスは次の通りです:
  背景　../素材/オブジェクト・UI/11.png
  プレイヤー　../素材/オブジェクト・UI/132.png
必要に応じてファイルが存在しない場合は単色のサーフェスで代用します。
画面サイズは1280x720ピクセル固定で、日本語テキストにはNotoSansJPフォントを利用します。
"""

import sys  # sysモジュールを読み込む
import pygame  # Pygameライブラリを読み込む
from pygame.locals import *  # 各種定数を直接参照できるようにする
import os  # OS関連の操作のためのモジュール

# ---------- OSごとの表示設定 ----------
# Windows環境かどうかを判定し、適切な設定を行います
if sys.platform == "win32":  # Windowsの場合
    import ctypes  # ctypesをインポートしてDPI設定を変更する
    ctypes.windll.user32.SetProcessDPIAware()  # DPIスケーリングを無効化する
    os.environ['SDL_VIDEO_CENTERED'] = '1'  # ウィンドウを画面中央に配置する
elif sys.platform == "darwin":  # macOSの場合
    os.environ['SDL_VIDEO_WINDOW_POS'] = '100,100'  # ウィンドウの位置を指定する
    os.environ['SDL_VIDEO_CENTERED'] = '1'  # ウィンドウを中央に配置する
elif sys.platform.startswith("linux"):  # Linux環境の場合
    os.environ['SDL_VIDEO_X11_NET_WM_BYPASS_COMPOSITOR'] = '0'  # LinuxのX11での設定
    os.environ['SDL_VIDEO_CENTERED'] = '1'  # Linuxでウィンドウを中央に配置する
else:  # 上記に該当しないその他のOSの場合
    os.environ['SDL_VIDEO_CENTERED'] = '1'  # その他のOSでは中央配置のみ行います

# 画面サイズとフォント設定
W, H = 1280, 720  # ウィンドウの幅と高さを設定する
FONT_PATH = "NotoSansJP-Regular.ttf"  # 日本語フォントファイルのパス
FONT_SIZE = 24  # フォントサイズ
BG_PATH = "../素材/オブジェクト・UI/11.png"  # 背景画像ファイルのパス
PLAYER_PATH = "../素材/オブジェクト・UI/132.png"  # プレイヤー画像ファイルのパス

pygame.init()  # Pygame全体を初期化する
screen = pygame.display.set_mode((W, H))  # 指定サイズでウィンドウを生成する
pygame.display.set_caption("03 画像配置＆右移動")  # ウィンドウタイトルを設定する

# フォント読み込み
try:  # 指定したフォントファイルを読み込むことを試みます
    font = pygame.font.Font(FONT_PATH, FONT_SIZE)  # 指定したフォントを読み込む
except IOError:  # フォントが読み込めなかった場合
    font = pygame.font.SysFont(None, FONT_SIZE)  # デフォルトフォントを使用する
    print("警告: 指定フォントが見つからないのでデフォルトフォントを使用します。")  # 標準出力に警告を表示

# 背景画像の読み込み
try:  # 背景画像ファイルの読み込みを試みます
    bg_image = pygame.image.load(BG_PATH).convert()  # 背景画像を読み込む（アルファ不要）
except Exception as e:  # 読み込みエラーが発生した場合
    print(f"背景画像 '{BG_PATH}' を読み込めませんでした: {e}")  # エラーメッセージを表示
    bg_image = pygame.Surface((W, H))  # 代替のSurfaceを生成
    bg_image.fill((200, 200, 200))  # グレーで塗りつぶす
# プレイヤー画像の読み込み
try:  # プレイヤー画像ファイルの読み込みを試みます
    player_image = pygame.image.load(PLAYER_PATH).convert_alpha()  # プレイヤー画像を読み込みアルファチャネル付きSurfaceに変換
except Exception as e:  # 読み込みエラーが発生した場合
    print(f"プレイヤー画像 '{PLAYER_PATH}' を読み込めませんでした: {e}")  # エラーメッセージを表示
    player_image = pygame.Surface((200, 200), pygame.SRCALPHA)  # 代替のSurfaceを生成
    player_image.fill((200, 200, 0, 255))  # 黄色い四角形で塗りつぶす

# プレイヤー画像の初期位置を設定
img_x, img_y = 100, (H - player_image.get_height()) // 2  # y位置は垂直中央に配置する
speed = 5  # プレイヤー画像の右方向への移動速度

# メインループ開始
clock = pygame.time.Clock()  # フレームレート制御用のClockを生成
running = True  # ループ継続フラグをTrueにする
while running:  # ゲームループを継続します
    clock.tick(60)  # 1秒間に60回までループを実行する
    for event in pygame.event.get():  # イベントキューからイベントを取り出す
        if event.type == QUIT:  # 閉じるボタンが押された場合
            running = False  # ループを終了する

    # キー入力処理
    keys = pygame.key.get_pressed()  # 全てのキーの状態を取得する
    if keys[K_RIGHT]:  # 右矢印キーが押されているか判定する
        img_x += speed  # x座標を増加させ、プレイヤー画像を右に移動する

    # 背景の描画
    screen.blit(bg_image, (0, 0))  # 背景画像を画面左上に描画する

    # プレイヤー画像の描画
    screen.blit(player_image, (img_x, img_y))  # プレイヤー画像を現在の位置に描画する

    # 説明テキストのリストを作成する
    messages = [  # 画面下部に表示するガイドメッセージを格納するリストです
        "画面に画像を表示しています。",  # テキスト1: 現在画像を表示していることを説明
        "右矢印キーを押すと画像が右に移動します。",  # テキスト2: 操作方法を説明
        "背景とプレイヤーの画像は指定されたパスから読み込んでいます。"  # テキスト3: 画像の読み込みについて説明
    ]  # messagesリストの終わり
    # 各テキストを描画
    for i, msg in enumerate(messages):  # enumerateでインデックスと要素を取得
        text_surface = font.render(msg, True, (0, 0, 0))  # テキストをSurfaceに変換する
        screen.blit(text_surface, (30, H - 100 + i * 30))  # 画面下部に表示する

    pygame.display.flip()  # 画面を更新して描画内容を表示する

pygame.quit()  # Pygameのリソースを解放して終了する