# --- Web版 (pygbag対応のための変換コピー / ゲーム内容は変更していません) ---
import asyncio
# coding: utf-8
import sys
import random
import time
import pygame
import os
from pygame.locals import *

# ==============================
# 初期化
# ==============================
pygame.init()

# 画面設定
info = pygame.display.Info()
W, H = info.current_w, info.current_h
screen = pygame.display.set_mode((W, H), 0)
pygame.display.set_caption("チンチロバトル")
clock = pygame.time.Clock()

# ==============================
# フォント
# ==============================
try:
    font = pygame.font.Font("NotoSansJP-Regular.ttf", 48)
    desc_font = pygame.font.Font("NotoSansJP-Regular.ttf", 32)
    dice_font = pygame.font.Font("NotoSansJP-Regular.ttf", 72)
except:
    font = pygame.font.SysFont(None, 48)
    desc_font = pygame.font.SysFont(None, 32)
    dice_font = pygame.font.SysFont(None, 72)

# ==============================
# パス
# ==============================
ASSET_DIR = os.path.join(os.path.dirname(__file__), "asset")
IMG_DIR = os.path.join(ASSET_DIR, "画像")
SOUND_DIR = os.path.join(ASSET_DIR, "効果音・BGM")

# ==============================
# 画像読み込み
# ==============================
DICE_SCALE = 6
dice_imgs_raw = [
    pygame.image.load(os.path.join(IMG_DIR, f"dice{i}.png")).convert_alpha()
    for i in range(1, 7)
]
dice_imgs = [
    pygame.transform.scale(img, (img.get_width() * DICE_SCALE, img.get_height() * DICE_SCALE))
    for img in dice_imgs_raw
]

bg_img = pygame.image.load(os.path.join(IMG_DIR, "BG.png")).convert()
bg_img = pygame.transform.scale(bg_img, (W, H))

img_27 = pygame.image.load(os.path.join(IMG_DIR, "27.png")).convert_alpha()
img_59 = pygame.image.load(os.path.join(IMG_DIR, "59.png")).convert_alpha()

PLAYER_X, PLAYER_Y = 890, 875
ENEMY_X, ENEMY_Y = 890, 100

# ==============================
# サウンド
# ==============================
pygame.mixer.init()
pygame.mixer.music.load(os.path.join(SOUND_DIR, "5.ogg"))
pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.play(-1)

roll_sound = pygame.mixer.Sound(os.path.join(SOUND_DIR, "8.ogg"))

# ==============================
# ステージ設定
# ==============================
STAGES = [
    {"name": "ステージ1", "tries": 5, "ok": lambda r: sum(r) >= 10,
     "rule": "5回以内に、サイコロの合計が10以上を出せ"},
    {"name": "ステージ2", "tries": 5, "ok": lambda r: sum(r) >= 11,
     "rule": "5回以内に、サイコロの合計が11以上を出せ"},
    {"name": "ステージ3", "tries": 6, "ok": lambda r: sum(r) >= 12,
     "rule": "6回以内に、サイコロの合計が12以上を出せ"},
    {"name": "ステージ4", "tries": 7, "ok": lambda r: sum(r) >= 13,
     "rule": "7回以内に、サイコロの合計が13以上を出せ"},
    {"name": "ステージ5", "tries": 7, "ok": lambda r: sum(r) >= 14,
     "rule": "7回以内に、サイコロの合計が14以上を出せ"},
]

TIME_LIMIT = 20

# ==============================
# 状態管理
# ==============================
MODE_TITLE = 0
MODE_RULE = 1
MODE_GAME = 2
MODE_CLEAR = 3
MODE_OVER = 4

game_mode = MODE_TITLE
stage_num = 0
tries_left = STAGES[0]["tries"]
current_dice = [1, 1, 1]

start_time = 0
game_clear = False
game_over = False

# キャラ演出
px_off = py_off = 0
ex_off = ey_off = 0

anim_mode = "none"
anim_timer = 0

# サイコロアニメ
dice_roll_anim = False
dice_roll_timer = 0
dice_roll_max = 60

# 連打防止
dice_roll_time_limit = 2
last_roll_time = 0

# ステージクリア演出
stage_clear_effect = False
stage_clear_timer = 0
stage_clear_duration = 30

# ==============================
# 関数
# ==============================
def reset_offsets():
    global px_off, py_off, ex_off, ey_off
    px_off = py_off = 0
    ex_off = ey_off = 0

def start_anim(mode):
    global anim_mode, anim_timer
    anim_mode = mode
    anim_timer = 19

def update_anim():
    global anim_mode, anim_timer
    global px_off, py_off, ex_off, ey_off

    if anim_mode == "none":
        return

    if anim_timer <= 0:
        anim_mode = "none"
        reset_offsets()
        return

    if anim_mode == "attack":
        py_off = -12 if anim_timer > 9 else -6
        ey_off = 4 if anim_timer > 9 else 2
        ex_off = -2 if anim_timer % 2 == 0 else 2

    elif anim_mode == "miss":
        py_off = 6 if anim_timer > 6 else 2
        ex_off = ey_off = 0

    anim_timer -= 1

def reset_all():
    global stage_num, tries_left, current_dice
    global game_clear, game_over
    global game_mode, start_time

    stage_num = 0
    tries_left = STAGES[0]["tries"]
    current_dice = [1, 1, 1]
    game_clear = False
    game_over = False
    reset_offsets()
    start_time = time.time()
    game_mode = MODE_GAME

def start_stage_clear_effect():
    global stage_clear_effect, stage_clear_timer
    stage_clear_effect = True
    stage_clear_timer = stage_clear_duration

def update_stage_clear_effect():
    global stage_clear_effect, stage_clear_timer
    if stage_clear_effect:
        if stage_clear_timer > 0:
            stage_clear_timer -= 1
        else:
            stage_clear_effect = False

def roll():
    global dice_roll_anim, dice_roll_timer, last_roll_time
    if dice_roll_anim:
        return

    current_time = time.time()
    if current_time - last_roll_time < dice_roll_time_limit:
        return

    dice_roll_anim = True
    dice_roll_timer = dice_roll_max
    roll_sound.play()
    last_roll_time = current_time

def update_dice_animation():
    global dice_roll_anim, dice_roll_timer
    global current_dice, tries_left, stage_num
    global game_over, game_clear, game_mode, start_time

    if not dice_roll_anim:
        return

    if dice_roll_timer > 0:
        current_dice = [random.randint(1, 6) for _ in range(3)]
        dice_roll_timer -= 1
        return

    dice_roll_anim = False
    current_dice = [random.randint(1, 6) for _ in range(3)]
    tries_left -= 1

    ok = STAGES[stage_num]["ok"](current_dice)

    if ok:
        start_anim("attack")
        start_stage_clear_effect()
    else:
        start_anim("miss")

    if ok:
        stage_num += 1
        if stage_num >= len(STAGES):
            game_clear = True
            game_mode = MODE_CLEAR
        else:
            tries_left = STAGES[stage_num]["tries"]
            start_time = time.time()
    else:
        if tries_left <= 0:
            game_over = True
            game_mode = MODE_OVER

def draw_dice_total():
    total = sum(current_dice)

    label_text = dice_font.render("出目の合計：", True, (255, 255, 255))
    shadow_label_text = dice_font.render("出目の合計：", True, (0, 0, 0))
    screen.blit(shadow_label_text, (W - shadow_label_text.get_width() - 100, 25))
    screen.blit(label_text, (W - label_text.get_width() - 95, 20))

    shadow_text = dice_font.render(str(total), True, (0, 0, 0))
    screen.blit(shadow_text, (W - shadow_text.get_width() - 25, 25))

    total_text = dice_font.render(str(total), True, (255, 255, 255))
    screen.blit(total_text, (W - total_text.get_width() - 20, 20))

# ==============================
# 描画
# ==============================
def draw_title():
    screen.blit(bg_img, (0, 0))
    t1 = font.render("チンチロバトル", True, (0, 0, 0))
    t2 = desc_font.render("Enter：ゲーム開始", True, (0, 0, 0))
    t3 = desc_font.render("R：ルール説明", True, (0, 0, 0))
    t4 = desc_font.render("Esc：終了", True, (0, 0, 0))

    screen.blit(t1, (W // 2 - t1.get_width() // 2, 150))
    screen.blit(t2, (W // 2 - t2.get_width() // 2, 350))
    screen.blit(t3, (W // 2 - t3.get_width() // 2, 420))
    screen.blit(t4, (W // 2 - t4.get_width() // 2, 490))

def draw_rule():
    screen.blit(bg_img, (0, 0))
    y = 150
    for st in STAGES:
        txt = desc_font.render(f"{st['name']}：{st['rule']}", True, (0, 0, 0))
        screen.blit(txt, (80, y))
        y += 70

    t1 = desc_font.render("Enter：ゲーム開始", True, (0, 0, 0))
    t2 = desc_font.render("B：タイトルに戻る", True, (0, 0, 0))
    screen.blit(t1, (80, H - 200))
    screen.blit(t2, (80, H - 130))

def draw_game():
    screen.blit(bg_img, (0, 0))

    screen.blit(img_27, (PLAYER_X + px_off, PLAYER_Y + py_off))
    screen.blit(img_59, (ENEMY_X + ex_off, ENEMY_Y + ey_off))

    if anim_mode == "attack" and anim_timer > 0:
        screen.blit(font.render("!", True, (0, 0, 0)), (ENEMY_X + 120, ENEMY_Y - 20))
    if anim_mode == "miss" and anim_timer > 0:
        screen.blit(font.render("...", True, (0, 0, 0)), (PLAYER_X + 120, PLAYER_Y - 40))

    base_x = W // 2 - 350
    y = 600
    for i, v in enumerate(current_dice):
        screen.blit(dice_imgs[v - 1], (base_x + i * 250, y))

    name = STAGES[stage_num]["name"]
    rule = STAGES[stage_num]["rule"]
    screen.blit(font.render(name, True, (0, 0, 0)), (60, 40))
    screen.blit(desc_font.render(rule, True, (0, 0, 0)), (60, 110))

    screen.blit(font.render(f"残り回数: {tries_left}", True, (0, 0, 0)), (60, H - 200))

    remain = TIME_LIMIT - int(time.time() - start_time)
    screen.blit(font.render(f"残り時間: {remain} 秒", True, (0, 0, 0)), (60, H - 130))

    if stage_clear_effect:
        text = font.render("ステージクリア！", True, (255, 255, 255))
        shadow_text = font.render("ステージクリア！", True, (0, 0, 0))
        screen.blit(shadow_text, (W // 2 - shadow_text.get_width() // 2 + 2, H // 2 - 40 + 2))
        screen.blit(text, (W // 2 - text.get_width() // 2, H // 2 - 40))

    draw_dice_total()

    # ＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝
    # ★ 追加：Spaceキー案内
    # ＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝
    guide = desc_font.render("Spaceキーでサイコロを振る", True, (0, 0, 0))
    screen.blit(guide, (W // 2 - guide.get_width() // 2, H - 80))

def draw_clear():
    screen.blit(bg_img, (0, 0))
    t1 = font.render("ゲームクリア！", True, (0, 0, 0))
    t2 = desc_font.render("Enter：タイトルへ", True, (0, 0, 0))
    t3 = desc_font.render("Esc：終了", True, (0, 0, 0))

    screen.blit(t1, (W // 2 - t1.get_width() // 2, 250))
    screen.blit(t2, (W // 2 - t2.get_width() // 2, 360))
    screen.blit(t3, (W // 2 - t3.get_width() // 2, 430))

def draw_over():
    screen.blit(bg_img, (0, 0))
    t1 = font.render("ゲームオーバー", True, (0, 0, 0))
    t2 = desc_font.render("Enter：タイトルへ", True, (0, 0, 0))
    t3 = desc_font.render("Esc：終了", True, (0, 0, 0))

    screen.blit(t1, (W // 2 - t1.get_width() // 2, 250))
    screen.blit(t2, (W // 2 - t2.get_width() // 2, 360))
    screen.blit(t3, (W // 2 - t3.get_width() // 2, 430))

# ==============================
# メインループ
# ==============================

async def _web_main():
    global event, game_mode
    while True:
        await asyncio.sleep(0)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                return

            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    return

                if game_mode == MODE_TITLE:
                    if event.key == K_RETURN:
                        reset_all()
                    elif event.key == K_r:
                        game_mode = MODE_RULE

                elif game_mode == MODE_RULE:
                    if event.key == K_RETURN:
                        reset_all()
                    elif event.key == K_b:
                        game_mode = MODE_TITLE

                elif game_mode == MODE_GAME:
                    if event.key == K_SPACE:
                        roll()

                elif game_mode == MODE_CLEAR:
                    if event.key == K_RETURN:
                        game_mode = MODE_TITLE

                elif game_mode == MODE_OVER:
                    if event.key == K_RETURN:
                        game_mode = MODE_TITLE

        if game_mode == MODE_GAME:
            if TIME_LIMIT - (time.time() - start_time) <= 0:
                game_mode = MODE_OVER

        update_dice_animation()
        update_anim()
        update_stage_clear_effect()

        if game_mode == MODE_TITLE:
            draw_title()
        elif game_mode == MODE_RULE:
            draw_rule()
        elif game_mode == MODE_GAME:
            draw_game()
        elif game_mode == MODE_CLEAR:
            draw_clear()
        elif game_mode == MODE_OVER:
            draw_over()

        pygame.display.update()
        clock.tick(60)
        await asyncio.sleep(0)


asyncio.run(_web_main())