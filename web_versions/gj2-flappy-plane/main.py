# --- Web版 (pygbag対応のための変換コピー / ゲーム内容は変更していません) ---
import asyncio
import pygame
import sys
import os
import random

pygame.init()
pygame.mixer.init()

# 画面サイズとタイトル
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("flappy_plane")
clock = pygame.time.Clock()

ASSETS = "assets"

# 音楽ロード
try:
    pygame.mixer.music.load(os.path.join(ASSETS, "RPG_Battle_03.ogg"))
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)
except pygame.error:
    print("音楽ファイルの読み込み失敗")

# 画像ロード
player_img = pygame.image.load(os.path.join(ASSETS, "plane_blue.png")).convert_alpha()
enemy_imgs = [
    pygame.image.load(os.path.join(ASSETS, "plane_gray1.png")).convert_alpha(),
    pygame.image.load(os.path.join(ASSETS, "plane_gray2.png")).convert_alpha(),
    pygame.image.load(os.path.join(ASSETS, "plane_orange.png")).convert_alpha()
]

# テキスト描画関数
def draw_text(text, size, x, y, color=(255, 255, 255)):
    font = pygame.font.SysFont(None, size)
    surf = font.render(text, True, color)
    screen.blit(surf, (x, y))

# シーンの状態を定義
STATE_TITLE = 0
STATE_PLAYING = 1
STATE_GAMEOVER = 2

game_state = STATE_TITLE
paused = False
score = 0  # スコア初期化

# プレイヤー設定
player_rect = player_img.get_rect()
player_rect.centerx = 200
player_rect.bottom = SCREEN_HEIGHT - 50
player_y_vel = 0
gravity = 0.6
jump_power = -10

# 敵設定
enemy_rects = []
enemy_speed = 5
for i in range(3):
    rect = enemy_imgs[i].get_rect()
    rect.y = 150 + i * 120
    rect.x = random.randint(850, 1500)
    enemy_rects.append(rect)

# プレイヤー初期化関数
def reset_player():
    global player_y_vel
    player_rect.centerx = 200
    player_rect.bottom = SCREEN_HEIGHT - 50
    player_y_vel = 0

# 敵初期化関数
def reset_enemies():
    for rect in enemy_rects:
        rect.x = random.randint(850, 1500)
        rect.y = random.randint(50, SCREEN_HEIGHT - 100)

# --- メインゲームループ ---
running = True

async def main():
    global dt, event, game_state, i, keys, paused, player_y_vel, rect, running, score
    while running:
        dt = clock.tick(FPS)
        await asyncio.sleep(0)
        screen.fill((30, 30, 60))

        # --- イベント処理 ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_p and game_state == STATE_PLAYING:
                    paused = not paused

        keys = pygame.key.get_pressed()

        # --- タイトル画面 ---
        if game_state == STATE_TITLE:
            draw_text("flappy_plane", 64, 200, 180)
            draw_text("Press SPACE to Start", 32, 250, 300)

            if keys[pygame.K_SPACE]:
                game_state = STATE_PLAYING
                reset_player()
                reset_enemies()
                score = 0  # スコアリセット

        # --- プレイ中画面 ---
        elif game_state == STATE_PLAYING:
            if not paused:
                score += 1  # スコア加算（毎フレーム）

                # ジャンプ処理
                if keys[pygame.K_SPACE]:
                    player_y_vel = jump_power

                # 重力処理
                player_y_vel += gravity
                player_rect.y += player_y_vel

                # 画面内に収める
                if player_rect.bottom > SCREEN_HEIGHT:
                    player_rect.bottom = SCREEN_HEIGHT
                    player_y_vel = 0
                if player_rect.top < 0:
                    player_rect.top = 0

                # プレイヤー描画
                screen.blit(player_img, player_rect)
                draw_text(f"Score: {score}", 30, 10, 10)  # スコア表示

                # 敵の移動と描画
                for i, rect in enumerate(enemy_rects):
                    rect.x -= enemy_speed
                    if rect.right < 0:
                        rect.x = random.randint(850, 1200)
                        rect.y = random.randint(50, SCREEN_HEIGHT - 100)
                    screen.blit(enemy_imgs[i], rect)

                    # 衝突判定
                    if player_rect.colliderect(rect):
                        game_state = STATE_GAMEOVER

            else:
                draw_text("PAUSED", 60, SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 30, (255, 255, 0))

        # --- ゲームオーバー画面 ---
        elif game_state == STATE_GAMEOVER:
            draw_text("Game Over", 64, 270, 250)
            draw_text(f"Final Score: {score}", 32, 270, 290)  # 最終スコア表示
            draw_text("Press R to Retry", 32, 270, 320)
            draw_text("Press ESC to Exit", 28, 270, 360)

            if keys[pygame.K_r]:
                game_state = STATE_TITLE
            elif keys[pygame.K_ESCAPE]:
                running = False

        pygame.display.update()

    # 終了処理
    pygame.quit()
    return


asyncio.run(main())