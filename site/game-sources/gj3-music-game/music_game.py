# coding: utf-8
"""
_rhythm_like.py

簡易的なリズムゲーム風デモです。
"""
import sys
import pygame
from pygame.locals import *
import os
import random

# OS設定
if sys.platform == "win32":
    import ctypes
    ctypes.windll.user32.SetProcessDPIAware()
    os.environ['SDL_VIDEO_CENTERED'] = '1'
else:
    os.environ['SDL_VIDEO_CENTERED'] = '1'

W, H = 1920, 1080
FONT_PATH = "NotoSansJP-Regular.ttf"
FONT_SIZE = 30

pygame.init()
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("音楽ゲーム")

try:
    font = pygame.font.Font(FONT_PATH, FONT_SIZE)
except IOError:
    font = pygame.font.SysFont(None, FONT_SIZE)

# 画像読み込み（ファイルパスは環境に合わせて）
arrow_center = pygame.image.load("asset/画像/3.png")
arrow_left   = pygame.image.load("asset/画像/4.png")
arrow_right  = pygame.image.load("asset/画像/5.png")
arrow_imgs = [arrow_center, arrow_left, arrow_right]

# 効果音・BGM
test_se5 = pygame.mixer.Sound("asset/効果音/5.mp3")
test_se6 = pygame.mixer.Sound("asset/効果音/6.mp3")
test_se10 = pygame.mixer.Sound("asset/効果音/10.mp3")
test_se5.set_volume(0.8)
test_se10.set_volume(0.6)

test_se4 = pygame.mixer.Sound("asset/効果音/4.mp3")
test_se4.set_volume(1.0)

# ゲーム状態
notes = []
decor_notes = []
spawn_interval = 1500
last_spawn = 0
judge_line_y = H - 150

CENTER_X = W // 2
LEFT_X = W // 2 - 200
RIGHT_X = W // 2 + 200

perfect_window = 30
ok_window = 50
message = "中央列の矢印が判定ラインに来たらエンタキー"

HP = 300
point = 0
スコア = point
スコア = max(0, スコア + point)

scene = "menu"

clock = pygame.time.Clock()
running = True
elapsed_time = 0
game_limit_ms = 60_000
hyouzi_time = "0 秒"

# ゲーム状態初期化
def reset_game():
    global notes, decor_notes, elapsed_time, last_spawn, HP, point, message, hyouzi_time
    notes.clear()
    decor_notes.clear()
    elapsed_time = 0
    last_spawn = 0
    HP = 300
    point = 0
    message = "中央列の矢印が判定ラインに来たらエンターキー"
    hyouzi_time = "0 秒"

while running:
    dt = clock.tick(60)
    elapsed_time += dt
    remain_ms = max(0, game_limit_ms - elapsed_time)
    hyouzi_time = f"残り {remain_ms // 1000:02d} 秒"

    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

        # キー押下イベント
        if event.type == KEYDOWN:

            # Eキーで強制終了 
            if event.key == K_e:
                try:
                    test_se4.stop()
                except:
                    pass
                pygame.quit()
                sys.exit()

            # スペース：メニューからプレイ開始、またはクリア/オーバーから再挑戦
            if event.key == K_SPACE:
                if scene == "menu":
                    scene = "play"
                    test_se4.stop()
                    test_se4.play(-1)
                elif scene == "clear":
                    reset_game()
                    scene = "play"
                    test_se4.stop()
                    test_se4.play(-1)
                elif scene == "over":
                    reset_game()
                    scene = "play"
                    test_se4.stop()
                    test_se4.play(-1)

            # バックスペース：どのシーンからでもタイトルへ
            elif event.key == K_BACKSPACE:
                reset_game()
                scene = "menu"
                test_se4.stop()

            # Enter：プレイ中の判定
            elif event.key == K_RETURN and scene == "play":
                result = None
                for note in notes:
                    if not note.get('hit', False):
                        dist = abs(note['y'] - judge_line_y)
                        if dist <= ok_window:
                            note['hit'] = True
                            if dist <= perfect_window:
                                result = "良"
                                point = max(0, point + 10)
                                test_se6.play()
                            else:
                                result = "可"
                                point = max(0, point + 5)
                                HP = max(0, HP - 50)
                                test_se5.play()
                            break
                if result is None:
                    result = "不可"
                    HP = max(0, HP - 100)
                message = result

    # シーンごとの処理
    if scene == "play":
        if remain_ms == 0:
            scene = "clear"
            message = "CLEAR!"

        if random.random() < 0.02:
            notes.append({'x': CENTER_X, 'y': -20, 'speed': 300, 'hit': False, 'img': arrow_center})
            last_spawn = elapsed_time
        if random.random() < 0.02:
            decor_notes.append({'x': LEFT_X, 'y': -20, 'speed': 300, 'img': arrow_left})
        if random.random() < 0.02:
            decor_notes.append({'x': RIGHT_X, 'y': -20, 'speed': 300, 'img': arrow_right})

        for note in notes[:]:
            note['y'] += note['speed'] * (dt / 1000.0)
            if note['y'] > judge_line_y + ok_window and not note.get('hit', False):
                message = "不可"
                HP = max(0, HP - 50)
                try:
                    notes.remove(note)
                except ValueError:
                    pass
            elif note['y'] > H + 40:
                if note in notes:
                    notes.remove(note)

        for dnote in decor_notes[:]:
            dnote['y'] += dnote['speed'] * (dt / 1000.0)
            if dnote['y'] > H + 40:
                try:
                    decor_notes.remove(dnote)
                except ValueError:
                    pass

        for dnote in decor_notes:
            dist = abs(dnote['y'] - judge_line_y)
            if dist <= 20:
                test_se10.play()

        if HP <= 0:
            scene = "over"
            message = "GAME OVER"

        screen.fill((255, 255, 255))
        pygame.draw.line(screen, (200, 200, 200), (0, judge_line_y), (W, judge_line_y), 4)

        for note in notes:
            img = note['img']
            rect = img.get_rect(center=(note['x'], note['y']))
            screen.blit(img, rect.topleft)

        for dnote in decor_notes:
            img = dnote['img']
            rect = img.get_rect(center=(dnote['x'], dnote['y']))
            screen.blit(img, rect.topleft)

        msg_surface1 = font.render(str(message), True, (0, 0, 0))
        msg_surface2 = font.render(str(hyouzi_time), True, (0, 0, 0))
        msg_surface3 = font.render(str(point), True, (0, 0, 0))
        msg_surface_hp = font.render(f"HP: {HP}", True, (0, 0, 0))

        screen.blit(msg_surface1, ((W - msg_surface1.get_width()) // 2, judge_line_y + 20))
        screen.blit(msg_surface2, (20, H - 80))
        screen.blit(msg_surface_hp, (20, H - 40))
        screen.blit(msg_surface3, (1000, 50))

        guide = font.render("中央列の矢印が判定ラインに来たらエンターキーを押してください", True, (0, 0, 0))
        screen.blit(guide, (20, 20))
        guide2 = font.render("Eキーでゲームを終了する", True, (0, 0, 0))
        screen.blit(guide2, (20, 70))
        pygame.display.flip()
        continue

    if scene == "menu":
        screen.fill((255, 255, 255))
        title  = font.render("GAME START!", True, (0, 0, 0))
        guide2 = font.render("スペースキーでスタート", True, (0, 0, 0))
        guide3 = font.render("中央列の矢印が判定ラインに来たらエンターキーを押してください", True, (0, 0, 0))
        guide4 = font.render("バックスペースキーでタイトルに戻る", True, (0, 0, 0))
        guide5 = font.render("Eキーでゲームを終了する", True, (0, 0, 0))
        screen.blit(title, ((W - title.get_width()) // 2, H // 2 - 40))
        screen.blit(title, ((W - title.get_width()) // 2, H // 2 - 40))
        screen.blit(guide2, ((W - guide2.get_width()) // 2, H // 2 + 10))
        screen.blit(guide3, (500, H // 2 + 60))
        screen.blit(guide4, (700, H // 2 + 100))
        screen.blit(guide5, (750, H // 2 + 130))
        pygame.display.flip()
        continue

    if scene == "over":
        test_se4.stop()
        screen.fill((255, 255, 255))
        title = font.render("GAME OVER", True, (0, 0, 0))
        guide2 = font.render("スペースキーで再チャレンジ", True, (0, 0, 0))
        guide5 = font.render("Eキーでゲームを終了する", True, (0, 0, 0))
        screen.blit(title, ((W - title.get_width()) // 2, H // 2 - 40))
        screen.blit(guide2, ((W - guide2.get_width()) // 2, H // 2 + 10))
        screen.blit(guide5, ((W - guide2.get_width()) // 2, H // 2 + 50))
        pygame.display.flip()
        continue

    if scene == "clear":
        test_se4.stop()
        screen.fill((255, 255, 255))
        title = font.render("GAME CLEAR!", True, (0, 0, 0))
        guide2 = font.render("スペースキーでタイトルへ", True, (0, 0, 0))
        guide5 = font.render("Eキーでゲームを終了する", True, (0, 0, 0))
        screen.blit(title, ((W - title.get_width()) // 2, H // 2 - 40))
        screen.blit(guide2, ((W - guide2.get_width()) // 2, H // 2 + 10))
        screen.blit(guide5, ((W - guide2.get_width()) // 2, H // 2 + 50))
        pygame.display.flip()
        continue

    pygame.display.flip()

pygame.quit()
