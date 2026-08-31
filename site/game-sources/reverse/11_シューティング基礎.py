# coding: utf-8
"""
11_shooting_demo.py

シューティングゲームの基礎を示す例です。プレイヤーは画面下部の長方形で、左右矢印キーで移動し、
スペースキーを押すと弾を発射します。弾が敵（上部の赤い長方形）に当たると敵は位置をランダムに
変え、弾は消滅します。
"""

import sys  # sysモジュールはプラットフォーム判定に使用します
import pygame  # Pygameライブラリを読み込みます
from pygame.locals import *  # キーやQUIT定数を直接参照できるようにします
import os  # 環境変数設定に使用します
import random  # 敵の再配置にランダム値を使用するため

# OS設定
# 各プラットフォームでDPIスケール無効化やウィンドウ位置を調整します
if sys.platform == "win32":  # Windows環境の場合
    import ctypes  # WindowsのAPI呼び出しに使用します
    ctypes.windll.user32.SetProcessDPIAware()  # DPIスケールを無効にします
    os.environ['SDL_VIDEO_CENTERED'] = '1'  # ウィンドウを中央に配置します
else:  # Windows以外の場合
    os.environ['SDL_VIDEO_CENTERED'] = '1'  # ウィンドウを中央に配置します

W, H = 1280, 720  # 画面の幅と高さを指定します
FONT_PATH = "NotoSansJP-Regular.ttf"  # 日本語フォントファイルのパス
FONT_SIZE = 28  # フォントサイズ

# 画像ファイルのパスを定義します。存在しない場合は代替サーフェスを作成します。
BG_PATH = "../素材/オブジェクト・UI/11.png"  # 背景画像のパス
PLAYER_PATH = "../素材/オブジェクト・UI/132.png"  # プレイヤー画像のパス
ENEMY_PATH = "../素材/オブジェクト・UI/160.png"  # 敵画像のパス

pygame.init()  # Pygameを初期化します
screen = pygame.display.set_mode((W, H))  # 指定サイズのウィンドウを作成します
pygame.display.set_caption("11 シューティング基礎")  # ウィンドウタイトルを設定します

try:  # フォント読み込みを試みます
    font = pygame.font.Font(FONT_PATH, FONT_SIZE)  # 指定フォントを読み込みます
except IOError:  # フォントが見つからない場合に実行されます
    font = pygame.font.SysFont(None, FONT_SIZE)  # フォントが見つからない場合はデフォルトフォントを使用します


# 背景画像の読み込み
try:  # 背景画像を読み込む処理を試行します
    bg_image = pygame.image.load(BG_PATH).convert()  # 背景画像を読み込みます（アルファ不要）
except Exception as e:  # 読み込みに失敗した場合に実行されます
    print(f"背景画像を読み込めませんでした: {e}")  # 読み込みに失敗した場合に警告を表示
    bg_image = pygame.Surface((W, H))  # 読み込めない場合は単色のSurfaceを作成します
    bg_image.fill((20, 20, 40))  # 暗い青色で塗りつぶします


# プレイヤー画像の読み込み
try:  # プレイヤー画像を読み込む処理を試行します
    player_image = pygame.image.load(PLAYER_PATH).convert_alpha()  # プレイヤー画像を読み込みます
except Exception as e:  # 読み込みに失敗した場合に実行されます
    print(f"プレイヤー画像を読み込めませんでした: {e}")  # 読み込みエラーを表示
    # 読み込めない場合は指定サイズのSurfaceを作成し色を塗る
    player_image = pygame.Surface((100, 40), pygame.SRCALPHA)  # 幅100高さ40の透明なSurfaceを作成します
    player_image.fill((80, 200, 250, 255))  # 水色で塗りつぶします


# プレイヤーの位置情報。Rectを使って当たり判定を行います
player_rect = player_image.get_rect()  # プレイヤー画像のサイズからRectを生成します
player_rect.midbottom = (W // 2, H - 30)  # 画面下部中央にプレイヤーを配置します
player_speed = 8  # プレイヤーの左右移動速度（ピクセル/フレーム）


# 敵画像の読み込み
try:  # 敵画像を読み込む処理を試行します
    enemy_image = pygame.image.load(ENEMY_PATH).convert_alpha()  # 敵画像を読み込みます
except Exception as e:  # 読み込みに失敗した場合に実行されます
    print(f"敵画像を読み込めませんでした: {e}")  # 読み込みエラーを表示
    enemy_image = pygame.Surface((80, 30), pygame.SRCALPHA)  # 読み込めない場合は矩形で代用します
    enemy_image.fill((250, 80, 80, 255))  # 赤色で塗りつぶします


# 敵の位置情報
enemy_rect = enemy_image.get_rect()  # 敵画像のサイズからRectを生成します
enemy_rect.x = random.randint(0, W - enemy_rect.width)  # X座標をランダムに配置します
enemy_rect.y = 50  # Y座標は画面上部に固定します


# 弾のリストと速度設定。弾は小さな矩形で表現し、画像は使用しません
bullets = []  # 発射された弾を保持するためのリスト
bullet_speed = 10  # 弾の移動速度（ピクセル/フレーム）

clock = pygame.time.Clock()  # FPS制御用のClockオブジェクト
running = True  # メインループ継続フラグ
while running:  # メインループ開始
    clock.tick(60)  # 1秒間に60フレームに制限します
    for event in pygame.event.get():  # イベントキューからイベントを取得
        if event.type == QUIT:  # ウィンドウの×ボタンが押された場合
            running = False  # ループを終了します
        elif event.type == KEYDOWN:  # キーが押されたとき
            if event.key == K_SPACE:  # スペースキーが押された場合
                # プレイヤー中央から弾を発射
                bullet_rect = pygame.Rect(player_rect.centerx - 5, player_rect.top - 10, 10, 20)  # 弾のRectを作成
                bullets.append(bullet_rect)  # 弾リストに追加します

    # キー入力でプレイヤー移動
    keys = pygame.key.get_pressed()  # 押されているキーの状態を取得します
    if keys[K_LEFT] and player_rect.left > 0:  # 左キーが押され、画面左端に達していない場合
        player_rect.x -= player_speed  # プレイヤーを左に移動します
    if keys[K_RIGHT] and player_rect.right < W:  # 右キーが押され、画面右端に達していない場合
        player_rect.x += player_speed  # プレイヤーを右に移動します

    # 弾の移動と当たり判定
    for bullet in bullets[:]:  # 弾リストのコピーでループします
        bullet.y -= bullet_speed  # 弾を上方向に移動させます
        if bullet.bottom < 0:  # 画面外に出た弾はリストから削除します
            bullets.remove(bullet)  # 画面外に出た弾を削除します
        elif bullet.colliderect(enemy_rect):  # 弾が敵に当たった場合
            bullets.remove(bullet)  # 弾を削除します
            # 敵を再配置
            enemy_rect.x = random.randint(0, W - enemy_rect.width)  # 新しいX位置をランダムに設定します

    # 画面描画
    screen.blit(bg_image, (0, 0))  # 背景を描画します
    # プレイヤーの描画
    screen.blit(player_image, player_rect.topleft)  # プレイヤー画像を描画します
    # 敵の描画
    screen.blit(enemy_image, enemy_rect.topleft)  # 敵画像を描画します
    # 弾の描画
    for bullet in bullets:  # 各弾を1つずつ取り出します
        pygame.draw.rect(screen, (255, 255, 100), bullet)  # 弾は黄色い矩形で描画します

    # ガイドテキストの描画
    txt1 = font.render("←→キーで移動、Spaceキーで弾を発射", True, (200, 200, 200))  # 操作説明文1
    screen.blit(txt1, (20, H - 80))  # 説明文を画面下部に表示します
    txt2 = font.render("敵に弾が当たると再配置されます", True, (200, 200, 200))  # 操作説明文2
    screen.blit(txt2, (20, H - 50))  # 説明文をその下に表示します

    pygame.display.flip()  # 画面を更新して描画内容を表示します

# ループ終了後にPygameを終了します
pygame.quit()  # Pygameのリソースを解放して終了します