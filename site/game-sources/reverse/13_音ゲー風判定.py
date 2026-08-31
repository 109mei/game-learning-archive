# coding: utf-8
"""
13_rhythm_like.py

簡易的なリズムゲーム風デモです。画面上部からノート（小さな四角形）が降りてきて、
画面下部の判定ラインに重なるときにスペースキーを押すことでタイミング判定を行います。
判定結果は「良」「可」「不可」の3段階で表示されます。
"""

import sys  # sysモジュールはプラットフォーム判定に使用します
import pygame  # Pygameライブラリを読み込みます
from pygame.locals import *  # キー定数やQUITイベントを直接参照できるようにします
import os  # 環境変数設定に使用します
import random  # ノートの生成時にランダム性を追加するため

# OS設定
# 各プラットフォームでDPIスケール無効化やウィンドウ位置を調整します
if sys.platform == "win32":  # Windows環境の場合
    import ctypes  # Windows API呼び出し用
    ctypes.windll.user32.SetProcessDPIAware()  # DPIスケールを無効にします
    os.environ['SDL_VIDEO_CENTERED'] = '1'  # ウィンドウを中央に配置します
else:  # Windows以外の場合
    os.environ['SDL_VIDEO_CENTERED'] = '1'  # ウィンドウを中央に配置します

W, H = 1280, 720  # 画面の幅と高さ
FONT_PATH = "NotoSansJP-Regular.ttf"  # 日本語フォントのパス
FONT_SIZE = 28  # フォントサイズ

pygame.init()  # Pygameを初期化します
screen = pygame.display.set_mode((W, H))  # 指定サイズのウィンドウを生成します
pygame.display.set_caption("13 リズムゲーム風デモ")  # ウィンドウタイトルを設定します

try:  # フォント読み込みを試みます
    font = pygame.font.Font(FONT_PATH, FONT_SIZE)  # 指定フォントを読み込みます
except IOError:  # フォントが読み込めない場合
    font = pygame.font.SysFont(None, FONT_SIZE)  # フォントが見つからない場合はデフォルトフォントを使用します

# ノートを格納するリスト。各ノートは辞書で管理します
notes = []  # アクティブなノートのリスト
spawn_interval = 1500  # ノートを生成する間隔 (ms)
last_spawn = 0  # 最後にノートを生成した時刻 (ms)
judge_line_y = H - 150  # 判定ラインのY座標（画面下部から150px上）

# タイミング判定の閾値設定
perfect_window = 50  # 判定ラインとの誤差が50px以内なら「良」と判定します
ok_window = 100  # 判定ラインとの誤差が100px以内なら「可」と判定します
message = "スペースキーでリズムを刻んでください"  # 最初に表示されるメッセージ

clock = pygame.time.Clock()  # フレームレート制御用のClockオブジェクト
running = True  # メインループの継続フラグ
elapsed_time = 0  # 起動からの経過時間(ms)
while running:  # メインループ
    dt = clock.tick(60)  # このフレームの経過時間(ms)を取得し、60fpsに制御
    elapsed_time += dt  # 経過時間を加算
    for event in pygame.event.get():  # イベント処理
        if event.type == QUIT:  # 閉じるボタンが押された
            running = False  # ループを終了
        elif event.type == KEYDOWN and event.key == K_SPACE:  # スペースキーが押された
            result = None  # 判定結果を初期化
            for note in notes:  # すべてのノートを確認
                if not note['hit']:  # まだ判定されていないノートに対して
                    dist = abs(note['y'] - judge_line_y)  # ノートと判定ラインの距離を計算
                    if dist <= ok_window:  # 判定可能な範囲内か
                        note['hit'] = True  # このノートをヒット済みとする
                        if dist <= perfect_window:  # より近ければ「良」
                            result = "良"  # 判定結果「良」を設定
                        else:  # 少し離れていれば「可"
                            result = "可"  # 判定結果「可」を設定
                        break  # 1つのノートだけ判定するのでループを抜ける
            if result is None:  # ヒットしていない場合は不可
                result = "不可"  # 判定結果「不可」を設定
            message = result  # 表示するメッセージを更新

    # ノート生成: 一定時間ごとに新しいノートを追加
    if elapsed_time - last_spawn >= spawn_interval:  # 前回生成から規定時間経過
        notes.append({'x': W // 2, 'y': -20, 'speed': 300, 'hit': False})  # 初期位置と速度を持つノートを追加
        last_spawn = elapsed_time  # 最終生成時刻を更新

    # ノート更新
    for note in notes[:]:  # ノートのリストをコピーして走査
        note['y'] += note['speed'] * (dt / 1000)  # ノートを下方向に移動させる
        # 判定ラインを越えてもヒットしていない場合
        if note['y'] > judge_line_y + ok_window and not note['hit']:  # 判定ラインより十分下に到達し未ヒットの場合
            message = "不可"  # 表示メッセージを「不可」にする
            notes.remove(note)  # ノートをリストから削除
        elif note['y'] > H + 40:  # 画面外に出た場合
            if note in notes:  # 念のためノートがリストに存在するか確認
                notes.remove(note)  # ノートをリストから削除

    # 描画処理
    screen.fill((0, 0, 0))  # 画面全体を黒でクリア
    # 判定ラインの描画
    pygame.draw.line(screen, (200, 200, 200), (0, judge_line_y), (W, judge_line_y), 4)  # 判定ラインを太線で描画
    # ノートの描画
    for note in notes:  # 現在のノートを1つずつ描画
        pygame.draw.rect(screen, (255, 200, 50), pygame.Rect(note['x'] - 20, note['y'] - 20, 40, 40), border_radius=5)  # ノートを矩形で描画
    # メッセージの描画
    msg_surface = font.render(message, True, (255, 255, 255))  # メッセージテキストをレンダリング
    screen.blit(msg_surface, ((W - msg_surface.get_width()) // 2, judge_line_y + 20))  # 判定ラインの下に描画
    # ガイド文の表示
    guide = font.render("上から降ってくるノートが判定ラインに来たらSpaceキーを押してください", True, (200, 200, 200))  # 操作ガイドをレンダリング
    screen.blit(guide, (20, 20))  # ガイドを画面左上に表示
    pygame.display.flip()  # 画面を更新

# ループ終了後にPygameを終了します
pygame.quit()  # Pygameの終了処理