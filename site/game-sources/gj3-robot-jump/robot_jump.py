# coding: utf-8
import sys
import pygame
from pygame.locals import *
import os
import random

# --- OS別設定 ---
if sys.platform == "win32":
    import ctypes
    ctypes.windll.user32.SetProcessDPIAware()
    os.environ['SDL_VIDEO_CENTERED'] = '1'
elif sys.platform == "darwin":
    os.environ['SDL_VIDEO_WINDOW_POS'] = '100,100'
    os.environ['SDL_VIDEO_CENTERED'] = '1'
elif sys.platform.startswith("linux"):
    os.environ['SDL_VIDEO_CENTERED'] = '1'
else:
    os.environ['SDL_VIDEO_CENTERED'] = '1'

# --- 基本設定 ---
W, H = 1920, 1080  # フルHD
FONT_PATH = "NotoSansJP-Regular.ttf"
FONT_SIZE = 48

pygame.init()
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("横スクロールジャンプゲーム")
clock = pygame.time.Clock()

# --- フォント設定 ---
try:
    font = pygame.font.Font(FONT_PATH, FONT_SIZE)
except IOError:
    font = pygame.font.SysFont(None, FONT_SIZE)

# =========================================================
# メニュー画面
# =========================================================
def show_menu():
    screen.fill((230, 240, 250))

    title_font = pygame.font.Font(FONT_PATH, 96)
    title = title_font.render("横スクロールジャンプゲーム", True, (10, 10, 40))
    screen.blit(title, ((W - title.get_width()) // 2, H // 4))

    guide_font = pygame.font.Font(FONT_PATH, 40)
    guide_lines = [
        "Enterキーでゲーム開始",
        "ESCキーで終了",
        "Spaceキー：ジャンプ（長押しでホバー）／左右キー：移動"
    ]
    for i, line in enumerate(guide_lines):
        guide_text = guide_font.render(line, True, (40, 40, 40))
        screen.blit(guide_text, ((W - guide_text.get_width()) // 2,
                                 H // 2 + i * 50))

    pygame.display.flip()

# =========================================================
# ゲームオーバー画面（白背景）
# =========================================================
def show_game_over(final_score):
    screen.fill((255, 255, 255))

    over_font = pygame.font.Font(FONT_PATH, 120)
    over_text = over_font.render("GAME OVER", True, (220, 50, 50))
    screen.blit(over_text, ((W - over_text.get_width()) // 2, H // 4))

    score_font = pygame.font.Font(FONT_PATH, 80)
    stext = score_font.render(f"Score: {final_score}", True, (40, 40, 40))
    screen.blit(stext, ((W - stext.get_width()) // 2, H // 2))

    menu_font = pygame.font.Font(FONT_PATH, 48)
    guide = menu_font.render("Rキー：リトライ ／ ESCキー：ゲーム一覧に戻る", True, (60, 60, 60))
    screen.blit(guide, ((W - guide.get_width()) // 2, H // 2 + 120))

    pygame.display.flip()

# =========================================================
# ゲーム本体
# =========================================================
def run_game():

    # ---------- 音 ----------
    jump_sound = None
    try:
        if not pygame.mixer.music.get_busy():
            pygame.mixer.music.load("asset/効果音・BGM/5.mp3")
            pygame.mixer.music.play(-1)
            pygame.mixer.music.set_volume(0.5)
        jump_sound = pygame.mixer.Sound("asset/効果音・BGM/10.mp3")
    except:
        pass

    # ---------- 画像 ----------
    try:
        bg1 = pygame.image.load("asset/画像/background.png").convert()
        bg2 = pygame.image.load("asset/画像/background.png").convert()
        bg1 = pygame.transform.scale(bg1, (W, H))
        bg2 = pygame.transform.scale(bg2, (W, H))

        walk_images = [
            pygame.image.load("asset/画像/walk1.png").convert_alpha(),
            pygame.image.load("asset/画像/walk2.png").convert_alpha()
        ]
        walk_images = [pygame.transform.scale(img, (140, 140)) for img in walk_images]

        jump_image = pygame.image.load("asset/画像/jump.png").convert_alpha()
        jump_image = pygame.transform.scale(jump_image, (140, 140))

        # enemy1（歩く・赤い敵）
        enemy_raw = [
            pygame.image.load("asset/画像/enemy1_walk1.png").convert_alpha(),
            pygame.image.load("asset/画像/enemy1_walk2.png").convert_alpha()
        ]
        scale_factor = 0.9
        enemy_imgs = [
            pygame.transform.rotozoom(pygame.transform.flip(img, True, False), 0, scale_factor)
            for img in enemy_raw
        ]

        # enemy2（ジャンプして飛ぶ・羽ばたく敵）
        enemy2_raw = [
            pygame.image.load("asset/画像/enemy2_up.png").convert_alpha(),
            pygame.image.load("asset/画像/enemy2_down.png").convert_alpha()
        ]
        enemy2_imgs = [
            pygame.transform.rotozoom(pygame.transform.flip(img, True, False), 0, 1.0)
            for img in enemy2_raw
        ]
    except pygame.error as e:
        print("画像ロードエラー:", e)
        return 0

    # ---------- 初期化 ----------
    bg_x1 = 0
    bg_x2 = W
    scroll_speed = 7.0
    enemy_speed = 8.0

    enemy_frame = 0
    enemy_frame_timer = 0.0

    # プレイヤー
    player_rect = walk_images[0].get_rect()
    player_rect.midbottom = (W // 3, H - 50)

    vel_y = 0.0
    gravity = 1200.0          # ★ 重力
    jump_velocity = -650.0
    coyote_time = 0.20
    coyote_timer = 0.0
    on_ground = False

    # プレイヤーアニメ
    current_frame = 0
    player_anim_timer = 0.0
    player_anim_speed = 0.18

    # ホバー（浮遊）
    is_gliding = False
    GLIDE_GRAVITY = 20.0 
    GLIDE_TIME = 1.5 
    glide_timer = GLIDE_TIME
    can_air_action = False

    # 敵生成
    spacing = 900             # ★ 敵の間隔を広げる
    enemies = []
    for i in range(5):
        etype = random.choice(["walk", "fly"])
        imgs = enemy_imgs if etype == "walk" else enemy2_imgs
        r = imgs[0].get_rect()
        r.midbottom = (W + i * spacing, H - 50)
        enemies.append({
            "type": etype,
            "imgs": imgs,
            "rect": r,
            "vy": 0.0,
            "state": "run",
            "cleared": False  # スコア加算済みか
        })

    cleared_score = 0
    ground_rect = pygame.Rect(0, H - 50, W, 50)

    last_space = False

    # ============================================================
    # メインループ
    # ============================================================
    running = True
    while running:
        dt = clock.tick(60) / 1000.0
        keys = pygame.key.get_pressed()
        space_down = keys[K_SPACE]

        # ---- イベント処理 ----
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit(); sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False  # ゲームを抜けてゲームオーバー画面へ

        # ---- スピード上昇（強め）----
        scroll_speed += 0.08 * dt
        enemy_speed += 0.10 * dt

        # ---- プレイヤー移動 ----
        move_speed = 300
        if keys[K_LEFT]:
            player_rect.x -= move_speed * dt
        if keys[K_RIGHT]:
            player_rect.x += move_speed * dt

        # ---- 背景 ----
        bg_x1 -= scroll_speed
        bg_x2 -= scroll_speed
        if bg_x1 <= -W:
            bg_x1 = bg_x2 + W
        if bg_x2 <= -W:
            bg_x2 = bg_x1 + W

        # ---- 地面接地 ----
        on_ground = player_rect.bottom >= ground_rect.top and vel_y >= 0
        if on_ground:
            coyote_timer = coyote_time
            player_rect.bottom = ground_rect.top
            vel_y = 0
            is_gliding = False
            can_air_action = True
            glide_timer = GLIDE_TIME
        else:
            coyote_timer = max(coyote_timer - dt, 0)

        # ---- ジャンプ ----
        if space_down and not last_space:
            if on_ground or coyote_timer > 0:
                vel_y = jump_velocity
                if jump_sound:
                    jump_sound.play()
                can_air_action = True

        # ---- ホバー ----
        if (not on_ground) and space_down and can_air_action and glide_timer > 0:
            is_gliding = True
            glide_timer -= dt
        else:
            is_gliding = False
            if glide_timer <= 0:
                can_air_action = False

        # ---- 重力 ----
        g = GLIDE_GRAVITY if is_gliding else gravity
        vel_y += g * dt
        player_rect.y += vel_y * dt

        if player_rect.bottom > ground_rect.top:
            player_rect.bottom = ground_rect.top
            vel_y = 0

        # ---- プレイヤーアニメ ----
        player_anim_timer += dt
        if player_anim_timer >= player_anim_speed:
            player_anim_timer = 0
            current_frame = (current_frame + 1) % len(walk_images)

        # ---- 敵処理 ----
        for e in enemies:
            e["rect"].x -= enemy_speed

            # ★ 飛び越え検知
            overlap_x = (e["rect"].left <= player_rect.centerx <= e["rect"].right)
            if overlap_x and (player_rect.bottom < e["rect"].top) and (not e["cleared"]):
                cleared_score += 300 if e["type"] == "fly" else 100
                e["cleared"] = True

            # enemy2 の大ジャンプ
            if e["type"] == "fly":
                trigger_x = player_rect.centerx + 300
                if e["state"] == "run" and e["rect"].left < trigger_x:
                    e["vy"] = -900
                    e["state"] = "jump"

                if e["state"] == "jump":
                    e["rect"].y += e["vy"] * dt
                    e["vy"] += gravity * dt
                    if e["rect"].bottom > ground_rect.top:
                        e["rect"].bottom = ground_rect.top
                        e["state"] = "run"

            # 画面外 → 再出現
            if e["rect"].right < 0:
                e["type"] = random.choice(["walk", "fly"])
                e["imgs"] = enemy_imgs if e["type"] == "walk" else enemy2_imgs

                rightmost = max(ee["rect"].right for ee in enemies)
                spawn_x = max(W + 150, rightmost + spacing)

                e["rect"] = e["imgs"][0].get_rect()
                e["rect"].midbottom = (spawn_x, H - 50)
                e["vy"] = 0.0
                e["state"] = "run"
                e["cleared"] = False

        # ---- 敵アニメ ----
        enemy_frame_timer += dt
        if enemy_frame_timer >= 0.18:
            enemy_frame_timer = 0
            enemy_frame = (enemy_frame + 1) % 2
            for e in enemies:
                keep = e["rect"].midbottom
                e["rect"] = e["imgs"][enemy_frame].get_rect()
                e["rect"].midbottom = keep

        # ---- 当たり判定 ----
        player_box = player_rect.inflate(-20, -20)
        for e in enemies:
            enemy_box = e["rect"].inflate(-20, -20)
            if player_box.colliderect(enemy_box):
                if pygame.mixer.get_init():
                    pygame.mixer.music.stop()
                return cleared_score  # スコアを返してゲーム終了

        # ---- 描画 ----
        screen.blit(bg1, (bg_x1, 0))
        screen.blit(bg2, (bg_x2, 0))

        for e in enemies:
            screen.blit(e["imgs"][enemy_frame], e["rect"])

        pygame.draw.rect(screen, (100, 60, 60), ground_rect)

        if not on_ground:
            screen.blit(jump_image, player_rect)
        else:
            screen.blit(walk_images[current_frame], player_rect)

        # スコア表示
        score_text = font.render(f"Score: {cleared_score}", True, (20, 20, 20))
        screen.blit(score_text, (20, 20))

        pygame.display.flip()
        last_space = space_down

    if pygame.mixer.get_init():
        pygame.mixer.music.stop()
    return cleared_score

# =========================================================
# メインループ（シーン管理）
# =========================================================
scene = "menu"
running = True
final_score = 0

while running:
    if scene == "menu":
        show_menu()
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == KEYDOWN:
                if event.key in (K_RETURN, K_KP_ENTER):
                    scene = "game"
                elif event.key == K_ESCAPE:
                    running = False

    elif scene == "game":
        final_score = run_game()
        scene = "game_over"

    elif scene == "game_over":
        show_game_over(final_score)
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == KEYDOWN:
                if event.key == K_r:
                    scene = "game"      # タイトルを挟まず即リトライ
                elif event.key == K_ESCAPE:
                    running = False

pygame.quit()
