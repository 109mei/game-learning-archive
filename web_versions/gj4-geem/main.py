# --- Web版 (pygbag対応のための変換コピー / ゲーム内容は変更していません) ---
import asyncio
import pygame
import sys
import os
import random

# Pygameと音声機能(Mixer)の初期化（音の遅延防止・再生の安定化）
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()
pygame.mixer.init()

WIDTH, HEIGHT = 1280, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Duck Target Shooter")
clock = pygame.time.Clock()

# マウスカーソルを非表示
pygame.mouse.set_visible(False)

# 実行スクリプトのディレクトリパスを取得
BASE_DIR = os.path.dirname(os.path.abspath(__file__)) if '__file__' in globals() else os.getcwd()

# 色の定義
BLACK = (15, 15, 20)
WHITE = (255, 255, 255)
RED = (255, 60, 60)
CYAN = (0, 255, 255)
YELLOW = (255, 215, 0)
BROWN = (180, 100, 40)

# 音源ロードヘルパー関数 (1.mp3 を最優先で読み込み)
def load_game_sound():
    candidates = ["1.ogg", "1.wav", "shot.ogg", "shot.wav", "shot.ogg"]
    for filename in candidates:
        filepath = os.path.join(BASE_DIR, filename)
        target = filepath if os.path.exists(filepath) else (filename if os.path.exists(filename) else None)
        if target:
            try:
                sound = pygame.mixer.Sound(target)
                sound.set_volume(0.8)
                print(f"[SUCCESS] 音源ファイルを読み込みました: {target}")
                return sound
            except Exception as e:
                print(f"[ERROR] 音源の読み込みに失敗しました ({target}): {e}")
    print("[WARNING] 音源ファイル (1.mp3) が見つかりません。")
    return None

# 効果音ロード
shot_sound = load_game_sound()

# 画像ロードヘルパー関数
def load_game_image(filename, target_size):
    filepath = os.path.join(BASE_DIR, filename)
    if os.path.exists(filepath):
        raw = pygame.image.load(filepath).convert_alpha()
        return pygame.transform.scale(raw, target_size)
    elif os.path.exists(filename):
        raw = pygame.image.load(filename).convert_alpha()
        return pygame.transform.scale(raw, target_size)
    else:
        surf = pygame.Surface(target_size, pygame.SRCALPHA)
        pygame.draw.circle(surf, YELLOW, (target_size[0]//2, target_size[1]//2), target_size[0]//2)
        return surf

# SCOREロゴ画像読み込み/生成
def get_score_logo_image(target_size=(220, 65)):
    filepath = os.path.join(BASE_DIR, "score_logo.png")
    if os.path.exists(filepath):
        raw = pygame.image.load(filepath).convert_alpha()
        return pygame.transform.scale(raw, target_size)
    elif os.path.exists("score_logo.png"):
        raw = pygame.image.load("score_logo.png").convert_alpha()
        return pygame.transform.scale(raw, target_size)

    surf = pygame.Surface(target_size, pygame.SRCALPHA)
    font_logo = pygame.font.SysFont(["arial", "impact"], 48, bold=True)
    for dx, dy in [(-3,0), (3,0), (0,-3), (0,3), (-2,-2), (2,2), (-2,2), (2,-2)]:
        txt_bg = font_logo.render("SCORE", True, BROWN)
        surf.blit(txt_bg, (target_size[0]//2 - txt_bg.get_width()//2 + dx, target_size[1]//2 - txt_bg.get_height()//2 + dy))
    txt_fg = font_logo.render("SCORE", True, WHITE)
    surf.blit(txt_fg, (target_size[0]//2 - txt_fg.get_width()//2, target_size[1]//2 - txt_fg.get_height()//2))
    return surf

# 画像セットアップ
IMG_SIZE = (60, 60)
yellow_duck_img = load_game_image("58.png", IMG_SIZE)
green_duck_img = load_game_image("57.png", IMG_SIZE)
bonus_img = load_game_image("215.png", IMG_SIZE)
score_logo_image = get_score_logo_image((220, 65))

enemy_width, enemy_height = IMG_SIZE
enemy_step_down = 45

# 通常敵の生成処理
def create_enemy(duck_type="yellow"):
    x = 0
    y = random.randint(50, HEIGHT - enemy_height - 60)
    speed = random.uniform(2.5, 4.5)
    
    if duck_type == "green":
        img = green_duck_img
        score_val = -100
    else:
        img = yellow_duck_img
        score_val = 100

    rect = pygame.Rect(x, y, enemy_width, enemy_height)
    return {
        'x': float(x),
        'y': float(y),
        'speed': speed,
        'rect': rect,
        'image': img,
        'score_val': score_val,
        'type': duck_type
    }

# ボーナスキャラの生成処理
def create_bonus_enemy():
    speed = random.uniform(2.5, 4.5) * 2.2
    
    edge = random.randint(0, 3)
    if edge == 0:
        start_x = random.randint(0, WIDTH - enemy_width)
        start_y = -enemy_height
        target_x = random.randint(0, WIDTH - enemy_width)
        target_y = HEIGHT + enemy_height
    elif edge == 1:
        start_x = random.randint(0, WIDTH - enemy_width)
        start_y = HEIGHT + enemy_height
        target_x = random.randint(0, WIDTH - enemy_width)
        target_y = -enemy_height
    elif edge == 2:
        start_x = -enemy_width
        start_y = random.randint(0, HEIGHT - enemy_height)
        target_x = WIDTH + enemy_width
        target_y = random.randint(0, HEIGHT - enemy_height)
    else:
        start_x = WIDTH + enemy_width
        start_y = random.randint(0, HEIGHT - enemy_height)
        target_x = -enemy_width
        target_y = random.randint(0, HEIGHT - enemy_height)

    dx = target_x - start_x
    dy = target_y - start_y
    dist = (dx**2 + dy**2) ** 0.5
    vx = (dx / dist) * speed
    vy = (dy / dist) * speed

    rect = pygame.Rect(start_x, start_y, enemy_width, enemy_height)
    return {
        'x': float(start_x),
        'y': float(start_y),
        'vx': vx,
        'vy': vy,
        'rect': rect,
        'image': bonus_img,
        'score_val': 1000,
        'type': 'bonus'
    }

# 制限時間（30秒）
GAME_TIME = 30

# ゲーム状態のリセット関数
def reset_game(start_in_title=False):
    enemies = []
    for _ in range(8):
        enemies.append(create_enemy("yellow"))
        enemies.append(create_enemy("green"))
    random.shuffle(enemies)
    
    bonus_spawn_times = [
        random.uniform(4.0, 12.0),
        random.uniform(16.0, 24.0)
    ]
    
    return {
        'enemies': enemies,
        'score': 0,
        'start_ticks': pygame.time.get_ticks(),
        'state': 'TITLE' if start_in_title else 'PLAYING',
        'bonus_spawn_times': bonus_spawn_times
    }

game_state = reset_game(start_in_title=True)

# UI用フォント
font = pygame.font.Font("_webfont.ttf", 42); font.set_bold(True)
title_font = pygame.font.Font("_webfont.ttf", 48); title_font.set_bold(True)
score_num_font = pygame.font.SysFont(["arial", "impact"], 80, bold=True)

# メインループ
running = True

async def _web_main():
    global dx, dy, elapsed_seconds, enemy, enemy_type, event, final_score_text, game_state, is_locked, line1, line2, logo_rect, mouse_pos, retry_rect, retry_text, running, score_rect, score_str, score_text, shadow_rect, shadow_score, shadow_timer, sight_color, start_msg, time_left, timer_color, timer_rect, timer_str, timer_text
    while running:
        await asyncio.sleep(0)
        mouse_pos = pygame.mouse.get_pos()

        # 進行状態の処理
        if game_state['state'] == 'PLAYING':
            elapsed_seconds = (pygame.time.get_ticks() - game_state['start_ticks']) / 1000.0
            time_left = max(0, int(GAME_TIME - elapsed_seconds))

            if game_state['bonus_spawn_times'] and elapsed_seconds >= game_state['bonus_spawn_times'][0]:
                game_state['bonus_spawn_times'].pop(0)
                game_state['enemies'].append(create_bonus_enemy())

            if time_left == 0:
                game_state['state'] = 'GAME_OVER'
        else:
            time_left = GAME_TIME if game_state['state'] == 'TITLE' else 0

        # イベント処理
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # マウスクリック処理（すべて左クリック: button == 1）
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    # 左クリック時に効果音を再生
                    if shot_sound:
                        shot_sound.play()

                    # タイトル画面：左クリックでスタート
                    if game_state['state'] == 'TITLE':
                        game_state['state'] = 'PLAYING'
                        game_state['start_ticks'] = pygame.time.get_ticks()

                    # プレイ画面：左クリックで敵をショット
                    elif game_state['state'] == 'PLAYING':
                        for enemy in game_state['enemies'][:]:
                            if enemy['rect'].collidepoint(mouse_pos):
                                enemy_type = enemy['type']
                                game_state['enemies'].remove(enemy)
                                game_state['score'] += enemy['score_val']

                                if enemy_type != 'bonus':
                                    game_state['enemies'].append(create_enemy(enemy_type))
                                break

                    # リザルト画面：左クリックでリトライ
                    elif game_state['state'] == 'GAME_OVER':
                        game_state = reset_game(start_in_title=False)

        # 移動処理（プレイ中のみ）
        if game_state['state'] == 'PLAYING':
            for enemy in game_state['enemies'][:]:
                if enemy['type'] == 'bonus':
                    enemy['x'] += enemy['vx']
                    enemy['y'] += enemy['vy']
                    enemy['rect'].x = int(enemy['x'])
                    enemy['rect'].y = int(enemy['y'])

                    if (enemy['x'] < -enemy_width * 2 or enemy['x'] > WIDTH + enemy_width * 2 or
                        enemy['y'] < -enemy_height * 2 or enemy['y'] > HEIGHT + enemy_height * 2):
                        game_state['enemies'].remove(enemy)
                else:
                    enemy['x'] += enemy['speed']
                    if enemy['x'] > WIDTH - enemy_width:
                        enemy['x'] = 0
                        enemy['y'] += enemy_step_down
                        if enemy['y'] > HEIGHT - enemy_height - 40:
                            enemy_type = enemy['type']
                            game_state['enemies'].remove(enemy)
                            game_state['enemies'].append(create_enemy(enemy_type))
                            continue

                    enemy['rect'].x = int(enemy['x'])
                    enemy['rect'].y = int(enemy['y'])

        # 描画処理
        screen.fill(BLACK)

        if game_state['state'] in ('PLAYING', 'GAME_OVER'):
            for enemy in game_state['enemies']:
                screen.blit(enemy['image'], (enemy['rect'].x, enemy['rect'].y))

        # 照準マーク描画
        is_locked = any(e['rect'].collidepoint(mouse_pos) for e in game_state['enemies']) if game_state['state'] == 'PLAYING' else False
        sight_color = RED if is_locked else CYAN
        pygame.draw.circle(screen, sight_color, mouse_pos, 16, 2)
        pygame.draw.circle(screen, sight_color, mouse_pos, 3)

        # スタート画面
        if game_state['state'] == 'TITLE':
            line1 = title_font.render("カーソルを合わせて", True, WHITE)
            line2 = title_font.render("左クリックで打ち抜け！", True, YELLOW)
            start_msg = font.render("左クリックでスタート", True, CYAN)

            screen.blit(line1, line1.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 100)))
            screen.blit(line2, line2.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 20)))
            screen.blit(start_msg, start_msg.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 100)))

        # プレイ中のUI表示
        if game_state['state'] == 'PLAYING':
            score_str = f"スコア: {game_state['score']}"
            for dx, dy in [(-2,0), (2,0), (0,-2), (0,2)]:
                shadow_score = font.render(score_str, True, BLACK)
                screen.blit(shadow_score, (30 + dx, 25 + dy))
            score_text = font.render(score_str, True, WHITE)
            screen.blit(score_text, (30, 25))

            timer_str = f"残り時間: {time_left}秒"
            timer_color = RED if time_left <= 10 else WHITE
            for dx, dy in [(-2,0), (2,0), (0,-2), (0,2)]:
                shadow_timer = font.render(timer_str, True, BLACK)
                shadow_rect = shadow_timer.get_rect(topright=(WIDTH - 30 + dx, 25 + dy))
                screen.blit(shadow_timer, shadow_rect)
            timer_text = font.render(timer_str, True, timer_color)
            timer_rect = timer_text.get_rect(topright=(WIDTH - 30, 25))
            screen.blit(timer_text, timer_rect)

        # リザルト画面
        if game_state['state'] == 'GAME_OVER':
            logo_rect = score_logo_image.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 90))
            screen.blit(score_logo_image, logo_rect)

            final_score_text = score_num_font.render(f"{game_state['score']}", True, YELLOW)
            score_rect = final_score_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 5))
            screen.blit(final_score_text, score_rect)

            retry_text = font.render("左クリックでリトライ", True, WHITE)
            retry_rect = retry_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 100))
            screen.blit(retry_text, retry_rect)

        pygame.display.flip()
        clock.tick(60)
        await asyncio.sleep(0)

    pygame.quit()
    return

asyncio.run(_web_main())