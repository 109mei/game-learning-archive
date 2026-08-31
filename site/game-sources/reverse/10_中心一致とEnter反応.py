# coding: utf-8
"""
10_center_match_enter.py

二つの円の中心がほぼ一致しているときに Enter キーを押すと特別な反応を示す例です。
青い円は矢印キーで移動でき、赤い円は固定されています。中心の距離が一定以下の場合に
Enterキーを押すと「ほぼ一致しました！」と表示されます。
"""

import sys  # sysモジュールはプラットフォーム判定に使用します
import pygame  # Pygameライブラリを読み込みます
from pygame.locals import *  # キー定数やQUITを直接参照できるようにします
import os  # 環境変数設定に使用します

# OS設定
# 各プラットフォームでDPIスケール無効化やウィンドウ位置を調整します
if sys.platform == "win32":  # Windows環境の場合
    import ctypes  # WindowsのAPI呼び出し用
    ctypes.windll.user32.SetProcessDPIAware()  # DPIスケールを無効にします
    os.environ['SDL_VIDEO_CENTERED'] = '1'  # ウィンドウを中央に配置します
else:  # Windows以外の場合
    os.environ['SDL_VIDEO_CENTERED'] = '1'  # ウィンドウを中央に配置します

W, H = 1280, 720  # 画面の幅と高さ
FONT_PATH = "NotoSansJP-Regular.ttf"  # 日本語フォントのパス
FONT_SIZE = 28  # フォントサイズ

pygame.init()  # Pygameを初期化します
screen = pygame.display.set_mode((W, H))  # 指定サイズでウィンドウを生成します
pygame.display.set_caption("10 中心一致＋Enter反応")  # ウィンドウタイトルを設定します

try:  # フォント読み込みを試みます
    font = pygame.font.Font(FONT_PATH, FONT_SIZE)  # 指定フォントを読み込みます
except IOError:  # フォントが見つからない場合に実行されます
    font = pygame.font.SysFont(None, FONT_SIZE)  # フォントが見つからない場合はデフォルトフォントを使用します

# 円の設定
fixed_pos = (W // 2, H // 2)  # 固定円の中心座標
fixed_radius = 50  # 固定円の半径
move_pos = [200, 200]  # 操作する移動円の中心座標
move_radius = 40  # 移動円の半径
speed = 5  # 矢印キーによる移動速度

message = ""  # 表示メッセージ用の文字列を初期化
clock = pygame.time.Clock()  # FPS制御用のClockオブジェクト
running = True  # メインループ継続フラグ
while running:  # メインループ開始
    clock.tick(60)  # 1秒間に60フレームに制限します
    for event in pygame.event.get():  # イベントキューからイベントを取得
        if event.type == QUIT:  # ウィンドウの×ボタンが押された場合
            running = False  # ループを終了します
        elif event.type == KEYDOWN and event.key == K_RETURN:  # Enterキーが押された場合
            # 中心が近ければEnterキーでメッセージを表示します
            # 二つの中心間の距離を計算します
            dx = move_pos[0] - fixed_pos[0]  # x座標の差を計算します
            dy = move_pos[1] - fixed_pos[1]  # y座標の差を計算します
            distance = (dx**2 + dy**2) ** 0.5  # ピタゴラスの定理で距離を算出
            if distance <= 30:  # 30ピクセル以内を「ほぼ一致」とみなします
                message = "ほぼ一致しました！"  # 一致した場合のメッセージ
            else:  # 距離が閾値より大きい場合はこちら
                message = "中心が一致していません"  # 一致していない場合のメッセージ

    # キー入力で移動
    keys = pygame.key.get_pressed()  # 押されているキーの状態を取得します
    if keys[K_LEFT]:  # 左矢印キーが押されている場合
        move_pos[0] -= speed  # x座標を減少させます（左へ移動）
    if keys[K_RIGHT]:  # 右矢印キーが押されている場合
        move_pos[0] += speed  # x座標を増加させます（右へ移動）
    if keys[K_UP]:  # 上矢印キーが押されている場合
        move_pos[1] -= speed  # y座標を減少させます（上へ移動）
    if keys[K_DOWN]:  # 下矢印キーが押されている場合
        move_pos[1] += speed  # y座標を増加させます（下へ移動）

    screen.fill((255, 255, 255))  # 背景を白で塗りつぶします
    # 円の描画
    pygame.draw.circle(screen, (250, 100, 100), fixed_pos, fixed_radius)  # 固定円を赤色で描画
    pygame.draw.circle(screen, (100, 150, 250), move_pos, move_radius)  # 移動円を青色で描画
    # ガイドテキストを生成
    guide1 = font.render("青い円を矢印キーで移動して赤い円の中心に重ねてください", True, (0,0,0))  # 操作説明文
    guide2 = font.render("中心がほぼ一致した状態でEnterキーを押すと反応します", True, (0,0,0))  # 判定説明文
    screen.blit(guide1, (20, H - 80))  # ガイド1を画面下部に表示
    screen.blit(guide2, (20, H - 50))  # ガイド2をその下に表示
    # メッセージの描画
    if message:  # メッセージが空でない場合に描画します
        msg_surf = font.render(message, True, (0, 100, 0))  # メッセージを緑色で描画
        screen.blit(msg_surf, (20, 20))  # メッセージを画面左上に表示

    pygame.display.flip()  # 画面を更新して描画内容を表示します

# ループ終了後にPygameを終了します
pygame.quit()  # Pygameのリソースを解放して終了します