# coding: utf-8
"""
17_audio_channels.py

BGMと効果音(SE)の再生を示す例です。BGM_FILEとSE_FILEに音源ファイルのパスを指定し、
起動時にBGMを再生します。Spaceキーで効果音を鳴らし、MキーでBGMの再生/停止を切り替えます。
"""

import sys  # sysモジュールはプラットフォーム判定に使用します
import pygame  # Pygameライブラリを読み込みます
from pygame.locals import *  # キー定数やQUITイベントを直接参照できるようにします
import os  # 環境変数設定に使用します

# OS設定
# WindowsではDPIスケール無効化とウィンドウ位置の調整を行います
if sys.platform == "win32":  # Windows環境の場合
    import ctypes  # Windows API呼び出し用モジュール
    ctypes.windll.user32.SetProcessDPIAware()  # DPIスケーリングを無効にします
    os.environ['SDL_VIDEO_CENTERED'] = '1'  # ウィンドウを画面中央に配置します
else:  # Windows以外のOSの場合
    os.environ['SDL_VIDEO_CENTERED'] = '1'  # ウィンドウを中央に配置します

W, H = 1280, 720  # 画面の幅と高さを指定します
FONT_PATH = "NotoSansJP-Regular.ttf"  # 日本語フォントのパス
FONT_SIZE = 28  # フォントサイズを指定します
BGM_FILE = "../素材/BGM/1.mp3"  # BGMファイルのパスを指定します
SE_FILE = "../素材/効果音/1.mp3"   # 効果音ファイルのパスを指定します

pygame.init()  # Pygameを初期化します
pygame.mixer.init()  # サウンド再生の初期化を行います
screen = pygame.display.set_mode((W, H))  # 指定サイズのウィンドウを作成します
pygame.display.set_caption("17 BGMとSEの再生")  # ウィンドウタイトルを設定します

try:  # フォント読み込みを試みます
    font = pygame.font.Font(FONT_PATH, FONT_SIZE)  # 指定したフォントを読み込みます
except IOError:  # フォントが読み込めない場合
    font = pygame.font.SysFont(None, FONT_SIZE)  # デフォルトフォントを使用します

# BGM読み込みと再生
bgm_loaded = False  # BGMが正常に読み込めたかどうかを示すフラグ
try:  # BGMファイルの読み込みを試みます
    pygame.mixer.music.load(BGM_FILE)  # BGMファイルを読み込みます
    pygame.mixer.music.play(-1)  # -1を指定するとBGMをループ再生します
    bgm_loaded = True  # 読み込みが成功したのでフラグを更新します
except Exception as e:  # 読み込みに失敗した場合に実行されます
    print(f"BGMを読み込めませんでした: {e}")  # エラーメッセージを表示します

# SE読み込み
se_sound = None  # 効果音オブジェクトを初期化
try:  # 効果音ファイルの読み込みを試みます
    se_sound = pygame.mixer.Sound(SE_FILE)  # 効果音ファイルを読み込みます
except Exception as e:  # 読み込みに失敗した場合に実行されます
    print(f"効果音を読み込めませんでした: {e}")  # エラーメッセージを表示します

bgm_playing = True  # BGMの再生状態を示すフラグ

clock = pygame.time.Clock()  # FPS制御用のClockオブジェクトを作成します
running = True  # メインループ継続フラグ
while running:  # メインループ開始
    clock.tick(60)  # 1秒間に60フレームまで処理します
    for event in pygame.event.get():  # イベントキューからイベントを取得します
        if event.type == QUIT:  # ウィンドウの×ボタンが押された場合
            running = False  # ループを終了します
        elif event.type == KEYDOWN:  # キーが押されたとき
            if event.key == K_SPACE and se_sound:  # Spaceキーが押され効果音が読み込めている場合
                se_sound.play()  # 効果音を再生します
            elif event.key == K_m and bgm_loaded:  # Mキーが押されBGMが読み込めている場合
                # MキーでBGMの再生/停止を切り替えます
                if bgm_playing:  # 現在BGMが再生中の場合
                    pygame.mixer.music.pause()  # BGMを一時停止します
                    bgm_playing = False  # 状態を更新します
                else:  # BGMが停止中の場合
                    pygame.mixer.music.unpause()  # BGMの再生を再開します
                    bgm_playing = True  # 状態を更新します

    # 描画
    screen.fill((30, 30, 30))  # 背景を暗いグレーで塗りつぶします
    lines = [  # 画面に表示する複数行の文字列をリストで定義します
        "Spaceキーで効果音を再生します。",  # 操作説明1
        "MキーでBGMの再生/一時停止を切り替えます。",  # 操作説明2
        "BGM_FILE と SE_FILE を適切なパスに設定してください。"  # ファイル設定の案内
    ]  # リスト定義の終了
    for i, line in enumerate(lines):  # 説明文を順番に描画します
        txt = font.render(line, True, (230, 230, 230))  # テキストSurfaceを生成
        screen.blit(txt, (20, 50 + i*40))  # 位置をずらしながら描画
    pygame.display.flip()  # 画面を更新して描画内容を表示します

pygame.quit()  # Pygameのリソースを解放して終了します