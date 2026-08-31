# --- Web版 (pygbag対応のための変換コピー / ゲーム内容は変更していません) ---
import asyncio
import pygame as pg
import sys
import random


# ==================================================
# 初期設定
# ==================================================

pg.init()
pg.mixer.init()


# ==================================================
# 画面設定
# ==================================================

WIDTH = 800
HEIGHT = 600

screen = pg.display.set_mode((WIDTH, HEIGHT))

pg.display.set_caption("BULLET BUNNY")

clock = pg.time.Clock()


# ==================================================
# フォント
# ==================================================

font = pg.font.Font(None, 80)
small_font = pg.font.Font(None, 40)


# ==================================================
# BGM
# ==================================================

pg.mixer.music.load("2.ogg")
pg.mixer.music.set_volume(0.4)
pg.mixer.music.play(-1)


# ==================================================
# 発射音
# ==================================================

shot_sound = pg.mixer.Sound("1.ogg")


# ==================================================
# 背景画像
# ==================================================

background_img = pg.image.load(
    "7.png"
).convert()

background_img = pg.transform.scale(
    background_img,
    (WIDTH, HEIGHT)
)


# ==================================================
# START画像
# ==================================================

goImage = pg.image.load(
    "175.png"
).convert_alpha()

goImage = pg.transform.scale(
    goImage,
    (180, 100)
)


# ==================================================
# GAME OVER画像
# ==================================================

gameoverImage = pg.image.load(
    "174.png"
).convert_alpha()

gameoverImage = pg.transform.scale(
    gameoverImage,
    (180, 100)
)


# ==================================================
# プレイヤー設定
# ==================================================

player_x = 150
player_y = 300

player_size = 60


player_img = pg.image.load(
    "26.png"
).convert_alpha()

player_img = pg.transform.scale(
    player_img,
    (player_size, player_size)
)


# ==================================================
# プレイヤー移動速度
# ==================================================

up_speed = 5
down_speed = 4


# ==================================================
# プレイヤーの弾
# ==================================================

player_bullets = []

bullet_width = 20
bullet_height = 10

bullet_speed = 10


# ==================================================
# 連射設定
# ==================================================

normal_shot_interval = 500

fast_shot_interval = 250

player_shot_interval = normal_shot_interval

player_last_shot = 0

power_up = False


# ==================================================
# アイテム設定
# ==================================================

items = []

item_size = 30
item_speed = 3


# ==================================================
# 壁設定
# ==================================================

wall_x = WIDTH

wall_width = 80

wall_speed = 5

gap = 180

top_wall_height = random.randint(
    100,
    300
)

bottom_wall_y = (
    top_wall_height + gap
)

bottom_wall_height = (
    HEIGHT - bottom_wall_y
)


# ==================================================
# 敵設定
# ==================================================

enemy_size = 70


enemy_img = pg.image.load(
    "215.png"
).convert_alpha()

enemy_img = pg.transform.scale(
    enemy_img,
    (enemy_size, enemy_size)
)


# ==================================================
# 敵1
# ==================================================

enemy1_x = 680
enemy1_y = 120

enemy1_speed = 3
enemy1_direction = 1

enemy1_hp = 5

enemy1_alive = True

enemy1_last_shot = 0


# ==================================================
# 敵2
# ==================================================

enemy2_x = 680
enemy2_y = 400

enemy2_speed = 3
enemy2_direction = -1

enemy2_hp = 5

enemy2_alive = True

enemy2_last_shot = 0


# ==================================================
# 敵2の初弾
# ==================================================

enemy2_first_shot = True

enemy2_start_time = 0


# ==================================================
# 敵の弾
# ==================================================

enemy_bullets = []

enemy_bullet_width = 20
enemy_bullet_height = 10

enemy_bullet_speed = 7

enemy_shot_interval = 750


# ==================================================
# ゲーム状態
# ==================================================

# タイトル画面
home = True

# ゲーム開始待ち
game_start = False

# ゲームオーバー
game_over = False

# ゲームクリア
game_clear = False
game_end_time = 0

# ==================================================
# レベル選択
# ==================================================

# 1 = LEVEL 1
# 2 = LEVEL 2

selected_level = 1


# ==================================================
# 色
# ==================================================

wall_color = (
    200,
    100,
    100
)

player_bullet_color = (
    255,
    210,
    0
)

enemy_bullet_color = (
    255,
    100,
    40
)

item_color = (
    50,
    220,
    100
)

text_color = (
    60,
    30,
    70
)


# ==================================================
# 敵1を倒す処理
# ==================================================

def defeat_enemy1():

    global enemy1_hp
    global enemy1_alive
    global enemy2_hp

    # 敵1を撃破
    enemy1_hp = 0
    enemy1_alive = False

    # 敵2が生きていればHPを全回復
    if enemy2_alive:

        enemy2_hp = 5


# ==================================================
# 敵2を倒す処理
# ==================================================

def defeat_enemy2():

    global enemy2_hp
    global enemy2_alive
    global enemy1_hp

    # 敵2を撃破
    enemy2_hp = 0
    enemy2_alive = False

    # 敵1が生きていればHPを全回復
    if enemy1_alive:

        enemy1_hp = 5


# ==================================================
# ゲームを開始する関数
# ==================================================

def start_level(level):

    global player_y

    global wall_x
    global top_wall_height
    global bottom_wall_y
    global bottom_wall_height

    global enemy1_y
    global enemy1_direction
    global enemy1_hp
    global enemy1_alive
    global enemy1_last_shot

    global enemy2_y
    global enemy2_direction
    global enemy2_hp
    global enemy2_alive
    global enemy2_last_shot

    global enemy2_first_shot
    global enemy2_start_time

    global player_shot_interval
    global power_up
    global player_last_shot

    global game_start
    global game_over
    global game_clear

    # ==================================================
    # プレイヤー
    # ==================================================

    player_y = 300


    # ==================================================
    # 壁
    # ==================================================

    wall_x = WIDTH

    top_wall_height = random.randint(
        100,
        300
    )

    bottom_wall_y = (
        top_wall_height + gap
    )

    bottom_wall_height = (
        HEIGHT - bottom_wall_y
    )


    # ==================================================
    # 敵1
    # ==================================================

    enemy1_y = 120

    enemy1_direction = 1

    enemy1_hp = 5

    enemy1_alive = True

    enemy1_last_shot = 0


    # ==================================================
    # 敵2
    # ==================================================

    enemy2_y = 400

    enemy2_direction = -1

    enemy2_hp = 5

    enemy2_alive = True

    enemy2_last_shot = 0


    # ==================================================
    # 敵2初弾
    # ==================================================

    enemy2_first_shot = True

    enemy2_start_time = 0


    # ==================================================
    # 弾を削除
    # ==================================================

    player_bullets.clear()

    enemy_bullets.clear()


    # ==================================================
    # アイテムを削除
    # ==================================================

    items.clear()


    # ==================================================
    # パワーアップをリセット
    # ==================================================

    power_up = False

    player_shot_interval = (
        normal_shot_interval
    )

    player_last_shot = 0


    # ==================================================
    # ゲーム状態
    # ==================================================

    game_over = False

    game_clear = False

    game_start = True


# ==================================================
# タイトル画面に戻る関数
# ==================================================

def return_to_title():

    global home
    global game_start
    global game_over
    global game_clear

    home = True

    game_start = False

    game_over = False

    game_clear = False


# ==================================================
# メインループ
# ==================================================


async def _web_main():
    global bottom_wall, bottom_wall_height, bottom_wall_y, bullet, bullet_x, bullet_y, clear_rect, clear_text, control_rect, control_text, current_time, enemy1_direction, enemy1_hp, enemy1_last_shot, enemy1_rect, enemy1_y, enemy2_direction, enemy2_first_shot, enemy2_hp, enemy2_last_shot, enemy2_rect, enemy2_start_time, enemy2_y, enemy_bullet, enemy_bullets, event, game_clear, game_end_time, game_over, game_start, gameover_rect, go_rect, home, hp_text1, hp_text2, item, item_text, item_text_rect, items, keys, level1_color, level1_rect, level1_text, level2_color, level2_rect, level2_text, level_text, player_bullets, player_last_shot, player_rect, player_shot_interval, player_y, power_text, power_up, restart_rect, restart_text, select_rect, select_text, selected_level, start_rect, start_text, title_rect, title_text, top_wall, top_wall_height, wall_x
    while True:
        await asyncio.sleep(0)
        current_time = pg.time.get_ticks()

        # ==================================================
        # イベント処理
        # ==================================================

        for event in pg.event.get():


            # ==================================================
            # ゲーム終了
            # ==================================================

            if event.type == pg.QUIT:

                pg.quit()

                return


            # ==================================================
            # キー入力
            # ==================================================

            if event.type == pg.KEYDOWN:


                # ==================================================
                # タイトル画面
                # ==================================================

                if home:


                    # ------------------------------------------
                    # 上キー
                    # ------------------------------------------

                    if event.key == pg.K_UP:

                        selected_level -= 1

                        if selected_level < 1:

                            selected_level = 2


                    # ------------------------------------------
                    # 下キー
                    # ------------------------------------------

                    elif event.key == pg.K_DOWN:

                        selected_level += 1

                        if selected_level > 2:

                            selected_level = 1


                    # ------------------------------------------
                    # SPACEでレベル決定
                    # ------------------------------------------

                    elif event.key == pg.K_SPACE:

                        home = False

                        start_level(
                            selected_level
                        )


                # ==================================================
                # ゲームオーバー・ゲームクリア
                # ==================================================

                elif game_over or game_clear:


                    # SPACEでタイトル画面へ戻る

                    if event.key == pg.K_SPACE:
                        if current_time - game_end_time >= 1000:
                            return_to_title()


                # ==================================================
                # ゲーム開始画面
                # ==================================================

                elif game_start:


                    if event.key == pg.K_SPACE:


                        game_start = False

                        current_time = (
                            pg.time.get_ticks()
                        )


                        # プレイヤー発射開始

                        player_last_shot = (
                            current_time
                        )


                        # 敵1発射開始

                        enemy1_last_shot = (
                            current_time
                        )


                        # 敵2初弾タイマー開始

                        enemy2_start_time = (
                            current_time
                        )

                        enemy2_first_shot = True


        # ==================================================
        # ゲーム中
        # ==================================================

        if (
            not home
            and not game_start
            and not game_over
            and not game_clear
        ):


            # ==================================================
            # プレイヤー移動
            # ==================================================

            keys = pg.key.get_pressed()


            if keys[pg.K_SPACE]:

                player_y -= up_speed

            else:

                player_y += down_speed


            # ==================================================
            # 画面外防止
            # ==================================================

            if player_y < 0:

                player_y = 0


            if player_y > HEIGHT - player_size:

                player_y = (
                    HEIGHT - player_size
                )


            # ==================================================
            # 壁を移動
            # ==================================================

            wall_x -= wall_speed


            if wall_x < -wall_width:


                wall_x = WIDTH


                top_wall_height = random.randint(
                    100,
                    300
                )


                bottom_wall_y = (
                    top_wall_height + gap
                )


                bottom_wall_height = (
                    HEIGHT - bottom_wall_y
                )


            # ==================================================
            # 敵1を移動
            # ==================================================

            if enemy1_alive:


                enemy1_y += (
                    enemy1_speed
                    * enemy1_direction
                )


                if enemy1_y <= 0:

                    enemy1_y = 0

                    enemy1_direction = 1


                if enemy1_y >= HEIGHT - enemy_size:

                    enemy1_y = (
                        HEIGHT - enemy_size
                    )

                    enemy1_direction = -1


            # ==================================================
            # 敵2を移動
            # ==================================================

            # LEVEL 2のみ敵2を動かす

            if selected_level == 2:

                if enemy2_alive:


                    enemy2_y += (
                        enemy2_speed
                        * enemy2_direction
                    )


                    if enemy2_y <= 0:

                        enemy2_y = 0

                        enemy2_direction = 1


                    if enemy2_y >= HEIGHT - enemy_size:

                        enemy2_y = (
                            HEIGHT - enemy_size
                        )

                        enemy2_direction = -1


            # ==================================================
            # 現在時間
            # ==================================================

            current_time = pg.time.get_ticks()


            # ==================================================
            # プレイヤー自動発射
            # ==================================================

            if (
                current_time
                - player_last_shot
                >= player_shot_interval
            ):


                bullet_x = (
                    player_x
                    + player_size
                )


                bullet_y = (
                    player_y
                    + player_size // 2
                    - bullet_height // 2
                )


                player_bullets.append(

                    pg.Rect(

                        bullet_x,
                        bullet_y,

                        bullet_width,
                        bullet_height

                    )

                )


                shot_sound.play()


                player_last_shot = (
                    current_time
                )


            # ==================================================
            # プレイヤー弾移動
            # ==================================================

            for bullet in player_bullets:

                bullet.x += bullet_speed


            player_bullets = [

                bullet

                for bullet in player_bullets

                if bullet.left < WIDTH

            ]


            # ==================================================
            # 敵1の発射
            # ==================================================

            if enemy1_alive:


                if (
                    current_time
                    - enemy1_last_shot
                    >= enemy_shot_interval
                ):


                    enemy_bullet = pg.Rect(

                        enemy1_x,

                        enemy1_y
                        + enemy_size // 2
                        - enemy_bullet_height // 2,

                        enemy_bullet_width,
                        enemy_bullet_height

                    )


                    enemy_bullets.append(
                        enemy_bullet
                    )


                    enemy1_last_shot = (
                        current_time
                    )


            # ==================================================
            # 敵2の発射
            # ==================================================

            if (
                selected_level == 2
                and enemy2_alive
            ):


                # ==================================================
                # 敵2の初弾
                # ==================================================

                if enemy2_first_shot:


                    if (
                        current_time
                        - enemy2_start_time
                        >= 1750
                    ):


                        enemy_bullet = pg.Rect(

                            enemy2_x,

                            enemy2_y
                            + enemy_size // 2
                            - enemy_bullet_height // 2,

                            enemy_bullet_width,
                            enemy_bullet_height

                        )


                        enemy_bullets.append(
                            enemy_bullet
                        )


                        enemy2_last_shot = (
                            current_time
                        )

                        enemy2_first_shot = False


                # ==================================================
                # 2発目以降
                # ==================================================

                else:


                    if (
                        current_time
                        - enemy2_last_shot
                        >= enemy_shot_interval
                    ):


                        enemy_bullet = pg.Rect(

                            enemy2_x,

                            enemy2_y
                            + enemy_size // 2
                            - enemy_bullet_height // 2,

                            enemy_bullet_width,
                            enemy_bullet_height

                        )


                        enemy_bullets.append(
                            enemy_bullet
                        )


                        enemy2_last_shot = (
                            current_time
                        )


            # ==================================================
            # 敵の弾を移動
            # ==================================================

            for bullet in enemy_bullets:

                bullet.x -= enemy_bullet_speed


            enemy_bullets = [

                bullet

                for bullet in enemy_bullets

                if bullet.right > 0

            ]


            # ==================================================
            # アイテムを移動
            # ==================================================

            for item in items:

                item.x -= item_speed


            items = [

                item

                for item in items

                if item.right > 0

            ]


            # ==================================================
            # Rect
            # ==================================================

            player_rect = pg.Rect(

                player_x,
                player_y,

                player_size,
                player_size

            )


            top_wall = pg.Rect(

                wall_x,
                0,

                wall_width,
                top_wall_height

            )


            bottom_wall = pg.Rect(

                wall_x,
                bottom_wall_y,

                wall_width,
                bottom_wall_height

            )


            enemy1_rect = pg.Rect(

                enemy1_x,
                enemy1_y,

                enemy_size,
                enemy_size

            )


            enemy2_rect = pg.Rect(

                enemy2_x,
                enemy2_y,

                enemy_size,
                enemy_size

            )


            # ==================================================
            # 壁との当たり判定
            # ==================================================

            if player_rect.colliderect(
                top_wall
            ):

                game_over = True
                game_end_time = current_time

            if player_rect.colliderect(
                bottom_wall
            ):

                game_over = True
                game_end_time = current_time

            # ==================================================
            # 敵との当たり判定
            # ==================================================

            if enemy1_alive:

                if player_rect.colliderect(
                    enemy1_rect
                ):

                    game_over = True
                    game_end_time = current_time

            if (
                selected_level == 2
                and enemy2_alive
            ):

                if player_rect.colliderect(
                    enemy2_rect
                ):

                    game_over = True
                    game_end_time = current_time

            # ==================================================
            # 敵弾との当たり判定
            # ==================================================

            for bullet in enemy_bullets:

                if player_rect.colliderect(
                    bullet
                ):

                    game_over = True
                    game_end_time = current_time

            # ==================================================
            # プレイヤー弾と敵
            # ==================================================

            for bullet in player_bullets[:]:


                # ==================================================
                # 敵1
                # ==================================================

                if (
                    enemy1_alive
                    and enemy1_rect.colliderect(
                        bullet
                    )
                ):


                    player_bullets.remove(
                        bullet
                    )


                    enemy1_hp -= 1


                    # ------------------------------------------
                    # 敵1撃破
                    # ------------------------------------------

                    if enemy1_hp <= 0:


                        defeat_enemy1()


                        # アイテムドロップ

                        items.append(

                            pg.Rect(

                                enemy1_x,
                                enemy1_y,

                                item_size,
                                item_size

                            )

                        )


                    # ------------------------------------------
                    # 敵1がまだ生存
                    # ------------------------------------------

                    else:


                        enemy1_y = random.randint(

                            0,
                            HEIGHT - enemy_size

                        )


                # ==================================================
                # 敵2
                # ==================================================

                elif (
                    selected_level == 2
                    and enemy2_alive
                    and enemy2_rect.colliderect(
                        bullet
                    )
                ):


                    player_bullets.remove(
                        bullet
                    )


                    enemy2_hp -= 1


                    # ------------------------------------------
                    # 敵2撃破
                    # ------------------------------------------

                    if enemy2_hp <= 0:


                        defeat_enemy2()


                        # アイテムドロップ

                        items.append(

                            pg.Rect(

                                enemy2_x,
                                enemy2_y,

                                item_size,
                                item_size

                            )

                        )


                    # ------------------------------------------
                    # 敵2がまだ生存
                    # ------------------------------------------

                    else:


                        enemy2_y = random.randint(

                            0,
                            HEIGHT - enemy_size

                        )


            # ==================================================
            # アイテム取得
            # ==================================================

            for item in items[:]:


                if player_rect.colliderect(
                    item
                ):


                    items.remove(item)


                    power_up = True

                    player_shot_interval = (
                        fast_shot_interval
                    )


            # ==================================================
            # ゲームクリア判定
            # ==================================================

            if selected_level == 1:


                # LEVEL 1は敵1を倒せばクリア

                if not enemy1_alive:

                    game_clear = True
                    game_end_time = current_time
                    enemy_bullets.clear()


            else:


                # LEVEL 2は敵1と敵2を両方倒せばクリア

                if (
                    not enemy1_alive
                    and not enemy2_alive
                ):

                    game_clear = True
                    game_end_time = current_time
                    enemy_bullets.clear()


        # ==================================================
        # 描画用Rect
        # ==================================================

        player_rect = pg.Rect(

            player_x,
            player_y,

            player_size,
            player_size

        )


        top_wall = pg.Rect(

            wall_x,
            0,

            wall_width,
            top_wall_height

        )


        bottom_wall = pg.Rect(

            wall_x,
            bottom_wall_y,

            wall_width,
            bottom_wall_height

        )


        enemy1_rect = pg.Rect(

            enemy1_x,
            enemy1_y,

            enemy_size,
            enemy_size

        )


        enemy2_rect = pg.Rect(

            enemy2_x,
            enemy2_y,

            enemy_size,
            enemy_size

        )


        # ==================================================
        # 背景
        # ==================================================

        screen.blit(

            background_img,

            (0, 0)

        )


        # ==================================================
        # タイトル画面
        # ==================================================

        if home:


            # ==================================================
            # タイトル
            # ==================================================

            title_text = font.render(

                "BULLET BUNNY",

                True,

                text_color

            )


            title_rect = title_text.get_rect(

                center=(

                    WIDTH // 2,

                    100

                )

            )


            screen.blit(

                title_text,

                title_rect

            )


            # ==================================================
            # LEVEL 1
            # ==================================================

            level1_color = text_color

            if selected_level == 1:

                level1_color = (
                    255,
                    80,
                    80
                )


            level1_text = small_font.render(

                "LEVEL 1",

                True,

                level1_color

            )


            level1_rect = level1_text.get_rect(

                center=(

                    WIDTH // 2,

                    250

                )

            )


            screen.blit(

                level1_text,

                level1_rect

            )


            # ==================================================
            # LEVEL 2
            # ==================================================

            level2_color = text_color

            if selected_level == 2:

                level2_color = (
                    255,
                    80,
                    80
                )


            level2_text = small_font.render(

                "LEVEL 2",

                True,

                level2_color

            )


            level2_rect = level2_text.get_rect(

                center=(

                    WIDTH // 2,

                    330

                )

            )


            screen.blit(

                level2_text,

                level2_rect

            )


            # ==================================================
            # 選択マーク
            # ==================================================

            if selected_level == 1:

                select_text = small_font.render(

                    "▶",

                    True,

                    (255, 80, 80)

                )

                select_rect = select_text.get_rect(

                    center=(

                        WIDTH // 2 - 100,

                        250

                    )

                )

                screen.blit(

                    select_text,

                    select_rect

                )


            else:

                select_text = small_font.render(

                    "▶",

                    True,

                    (255, 80, 80)

                )

                select_rect = select_text.get_rect(

                    center=(

                        WIDTH // 2 - 100,

                        330

                    )

                )

                screen.blit(

                    select_text,

                    select_rect

                )


            # ==================================================
            # 操作説明
            # ==================================================

            control_text = small_font.render(

                "UP / DOWN : Select",

                True,

                text_color

            )


            control_rect = control_text.get_rect(

                center=(

                    WIDTH // 2,

                    430

                )

            )


            screen.blit(

                control_text,

                control_rect

            )


            start_text = small_font.render(

                "SPACE : Start",

                True,

                text_color

            )


            start_rect = start_text.get_rect(

                center=(

                    WIDTH // 2,

                    480

                )

            )


            screen.blit(

                start_text,

                start_rect

            )


        # ==================================================
        # ゲーム画面
        # ==================================================

        else:


            # ==================================================
            # 壁
            # ==================================================

            pg.draw.rect(

                screen,
                wall_color,
                top_wall

            )


            pg.draw.rect(

                screen,
                wall_color,
                bottom_wall

            )


            # ==================================================
            # プレイヤー
            # ==================================================

            screen.blit(

                player_img,
                player_rect

            )


            # ==================================================
            # 敵1
            # ==================================================

            if enemy1_alive:

                screen.blit(

                    enemy_img,
                    enemy1_rect

                )


            # ==================================================
            # 敵2
            # ==================================================

            if (
                selected_level == 2
                and enemy2_alive
            ):

                screen.blit(

                    enemy_img,
                    enemy2_rect

                )


            # ==================================================
            # プレイヤー弾
            # ==================================================

            for bullet in player_bullets:

                pg.draw.rect(

                    screen,

                    player_bullet_color,

                    bullet

                )


            # ==================================================
            # 敵弾
            # ==================================================

            for bullet in enemy_bullets:

                pg.draw.rect(

                    screen,

                    enemy_bullet_color,

                    bullet

                )


            # ==================================================
            # アイテム
            # ==================================================

            for item in items:


                pg.draw.rect(

                    screen,

                    item_color,

                    item

                )


                item_text = small_font.render(

                    "P",

                    True,

                    (255, 255, 255)

                )


                item_text_rect = (
                    item_text.get_rect(
                        center=item.center
                    )
                )


                screen.blit(

                    item_text,

                    item_text_rect

                )


            # ==================================================
            # レベル表示
            # ==================================================

            level_text = small_font.render(

                f"LEVEL {selected_level}",

                True,

                text_color

            )


            screen.blit(

                level_text,

                (20, 20)

            )


            # ==================================================
            # 敵1 HP
            # ==================================================

            if enemy1_alive:


                hp_text1 = small_font.render(

                    f"ENEMY 1 HP: {enemy1_hp}",

                    True,

                    text_color

                )


                screen.blit(

                    hp_text1,

                    (500, 20)

                )


            # ==================================================
            # 敵2 HP
            # ==================================================

            if (
                selected_level == 2
                and enemy2_alive
            ):


                hp_text2 = small_font.render(

                    f"ENEMY 2 HP: {enemy2_hp}",

                    True,

                    text_color

                )


                screen.blit(

                    hp_text2,

                    (500, 60)

                )


            # ==================================================
            # パワーアップ
            # ==================================================

            if power_up:


                power_text = small_font.render(

                    "POWER UP! x2",

                    True,

                    (0, 200, 0)

                )


                screen.blit(

                    power_text,

                    (20, 60)

                )


            # ==================================================
            # ゲーム開始
            # ==================================================

            if game_start:


                go_rect = goImage.get_rect(

                    center=(

                        WIDTH // 2,

                        HEIGHT // 2

                    )

                )


                screen.blit(

                    goImage,

                    go_rect

                )


                start_text = small_font.render(

                    "Press SPACE to Start",

                    True,

                    text_color

                )


                start_rect = start_text.get_rect(

                    center=(

                        WIDTH // 2,

                        HEIGHT // 2 + 80

                    )

                )


                screen.blit(

                    start_text,

                    start_rect

                )


            # ==================================================
            # GAME OVER
            # ==================================================

            if game_over:


                gameover_rect = (
                    gameoverImage.get_rect(

                        center=(

                            WIDTH // 2,
                            HEIGHT // 2

                        )

                    )
                )


                screen.blit(

                    gameoverImage,

                    gameover_rect

                )
                if current_time - game_end_time >= 1000:

                    restart_text = small_font.render(
                        "Press SPACE for MENU",
                        True,
                        text_color
                    )

                else:

                    restart_text = small_font.render(
                        "Wait...",
                        True,
                        text_color
                    )


                restart_rect = restart_text.get_rect(

                    center=(

                        WIDTH // 2,

                        HEIGHT // 2 + 80

                    )

                )


                screen.blit(

                    restart_text,

                    restart_rect

                )


            # ==================================================
            # GAME CLEAR
            # ==================================================

            if game_clear:


                clear_text = font.render(

                    "GAME CLEAR!",

                    True,

                    (50, 220, 120)

                )


                clear_rect = clear_text.get_rect(

                    center=(

                        WIDTH // 2,

                        HEIGHT // 2

                    )

                )


                screen.blit(

                    clear_text,

                    clear_rect

                )


                if current_time - game_end_time >= 1000:

                    restart_text = small_font.render(
                        "Press SPACE for MENU",
                        True,
                        text_color
                    )

                else:

                    restart_text = small_font.render(
                        "Wait...",
                        True,
                        text_color
                    )


                restart_rect = restart_text.get_rect(

                    center=(

                        WIDTH // 2,

                        HEIGHT // 2 + 70

                    )

                )


                screen.blit(

                    restart_text,

                    restart_rect

                )


        # ==================================================
        # 画面更新
        # ==================================================

        pg.display.update()


        # ==================================================
        # FPS
        # ==================================================

        clock.tick(60)
        await asyncio.sleep(0)


asyncio.run(_web_main())