# coding: utf-8
"""
21_variables_basics.py

Pythonの基本的な変数の使い方と種類を紹介するサンプルです。整数、浮動小数点、文字列、
リストなど複数の型の変数を宣言し、画面に表示します。コメントで各変数の意味を説明します。
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
FONT_SIZE = 28  # フォントサイズを指定します

pygame.init()  # Pygameを初期化します
screen = pygame.display.set_mode((W, H))  # 指定サイズのウィンドウを作成します
pygame.display.set_caption("21 変数の基本")  # ウィンドウタイトルを設定します

try:  # 指定したフォントを読み込みます
    font = pygame.font.Font(FONT_PATH, FONT_SIZE)  # フォントオブジェクトを生成
except IOError:  # 読み込めない場合
    font = pygame.font.SysFont(None, FONT_SIZE)  # デフォルトフォントを使用します

# 変数の宣言
integer_var = 42  # 整数型の変数
float_var = 3.14  # 浮動小数点数型の変数
string_var = "こんにちは"  # 文字列型の変数
list_var = [1, 2, 3]  # リスト型の変数
dict_var = {"鍵": "値", "数字": 123}  # 辞書型の変数

clock = pygame.time.Clock()  # FPS制御用のClockオブジェクト
running = True  # メインループ継続フラグ
while running:  # メインループ
    clock.tick(60)  # 1秒間に60回までループを実行します
    for event in pygame.event.get():  # イベントキューからイベントを取得
        if event.type == QUIT:  # ウィンドウの×ボタンが押された場合
            running = False  # ループを終了します

    screen.fill((255, 255, 245))  # 背景をオフホワイトで塗りつぶします
    # 各変数を文字列に変換して表示するためのリストを作成
    lines = [  # 変数値を組み込んだ文字列のリスト
        f"整数(integer_var): {integer_var}",  # 整数の値を表示
        f"浮動小数点(float_var): {float_var}",  # 浮動小数点数の値を表示
        f"文字列(string_var): {string_var}",  # 文字列の内容を表示
        f"リスト(list_var): {list_var}",  # リストの内容を表示
        f"辞書(dict_var): {dict_var}"  # 辞書の内容を表示
    ]  # リスト定義終了
    for i, text in enumerate(lines):  # リストの各行を描画します
        surf = font.render(text, True, (0, 0, 0))  # 黒色テキストSurfaceを生成
        screen.blit(surf, (50, 100 + i * 40))  # 縦に並べて描画
    title = font.render("Pythonの変数の例", True, (0, 50, 100))  # タイトル文字列を描画
    screen.blit(title, (50, 40))  # タイトルを画面上部に表示
    pygame.display.flip()  # 描画内容を画面に反映します

pygame.quit()  # Pygameを終了してリソースを解放します