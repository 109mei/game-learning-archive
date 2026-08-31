# --- Web版 (pygbag対応のための変換コピー / ゲーム内容は変更していません) ---
import asyncio

# coding: utf-8

import random #ランダムを使うためのモジュール
import sys  # sysモジュールはOS判定やプラットフォーム情報を取得するために使用します
import pygame  # ゲームライブラリPygameを読み込みます
from pygame.locals import *  # Pygameの定数を直接参照できるようにします
import os  # osモジュールは環境変数の設定に利用します
import math
#初期化
pygame.init()

# ↓あると便利なもの これがないとパソコンの設定から拡大・縮小率を100%に手動でしなければならない
# OS判定と適切な設定を適用
if sys.platform == "win32":  # Windows
    pass  # web: ctypes無効化 | import ctypes
    pass  # web: ctypes無効化 | ctypes.windll.user32.SetProcessDPIAware()
    # DPIスケール無効
    os.environ['SDL_VIDEO_CENTERED'] = '1'

elif sys.platform == "darwin":  # macOS
    os.environ['SDL_VIDEO_WINDOW_POS'] = '100,100'
    os.environ['SDL_VIDEO_CENTERED'] = '1'

elif sys.platform.startswith("linux"):  # Linux
    os.environ['SDL_VIDEO_X11_NET_WM_BYPASS_COMPOSITOR'] = '0'
    os.environ['SDL_VIDEO_CENTERED'] = '1'

elif sys.platform.startswith("freebsd") or sys.platform.startswith("openbsd") or sys.platform.startswith("netbsd"):  # BSD系
    os.environ['SDL_VIDEO_CENTERED'] = '1'

elif sys.platform.startswith("sunos"):  # Solaris
    os.environ['SDL_VIDEO_CENTERED'] = '1'

elif sys.platform.startswith("haiku"):  # Haiku OS
    os.environ['SDL_VIDEO_WINDOW_POS'] = '50,50'

elif sys.platform.startswith("android"):  # Android
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    os.environ['SDL_VIDEODRIVER'] = 'android'  # Android専用設定

elif sys.platform.startswith("emscripten"):  # WebAssembly
    print("Emscripten (WebAssembly) 環境: 追加設定不要")

elif sys.platform.startswith("cygwin") or sys.platform.startswith("msys"):  # Cygwin / MSYS2
    os.environ['SDL_VIDEO_CENTERED'] = '1'

elif sys.platform.startswith("riscos"):  # RISC OS
    os.environ['SDL_VIDEO_CENTERED'] = '1'

elif sys.platform.startswith("aix"):  # IBM AIX
    os.environ['SDL_VIDEO_CENTERED'] = '1'

elif sys.platform.startswith("vwxorks"):  # VxWorks
    os.environ['SDL_VIDEO_CENTERED'] = '1'

elif sys.platform.startswith("os2"):  # OS/2
    os.environ['SDL_VIDEO_CENTERED'] = '1'

elif sys.platform.startswith("amiga"):  # AmigaOS / MorphOS
    os.environ['SDL_VIDEO_CENTERED'] = '1'

else:  # その他の未知のOS
    print(f"警告: このOS（{sys.platform}）は未検証です。動作しない可能性があります。")

FONT_PATH = "NotoSansJP-Regular.ttf"  # 日本語表示用フォントファイルのパス。
FONT_SIZE = 28  # フォントサイズ,文字の大きさを指定します。
font = pygame.font.Font(FONT_PATH, FONT_SIZE)  # 指定したフォントファイルとサイズでフォントオブジェクトを生成します。
titlefont = pygame.font.Font(FONT_PATH, 50)



#ウィンドウ作成
# ===============================
# 画面設定
# ===============================
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("pygame")

WIDTH, HEIGHT = SCREEN_WIDTH, SCREEN_HEIGHT
clock = pygame.time.Clock()

# ===============================
# 画像読み込み
# ===============================
enemy_img = pygame.image.load("素材/57.png").convert_alpha()
enemy_img = pygame.transform.scale(enemy_img, (80, 80))

bg_img = pygame.image.load("素材/14.png").convert()
bg_img = pygame.transform.scale(bg_img, (WIDTH, HEIGHT))

crosshair_img = pygame.image.load("素材/50.png").convert_alpha()
crosshair_img = pygame.transform.scale(crosshair_img, (40, 40))

# ===============================
# BGM設定
# ===============================
pygame.mixer.music.load("素材/8.ogg")
pygame.mixer.music.set_volume(0.4)
bgm_playing = False

# ===============================
# ゲーム変数
# ===============================
cross_x = WIDTH // 2
cross_y = HEIGHT // 2
cross_speed = 3.5

score = 0
hp = 100
game_result = None

# ===============================
# 敵生成
# ===============================
def create_enemies(n):
    enemies = []
    for _ in range(n):
        x = random.randint(100, WIDTH - 50)
        y = random.randint(100, HEIGHT - 50)
        enemies.append([x, y])
    return enemies

enemies = create_enemies(20)
killed_order = []

# ===============================
# リセット処理
# ===============================
def reset_game():
    global enemies, killed_order, score, hp
    global cross_x, cross_y, game_result, bgm_playing

    enemies = create_enemies(20)
    killed_order = []
    score = 0
    hp = 100

    cross_x = WIDTH // 2
    cross_y = HEIGHT // 2

    game_result = None
    bgm_playing = False

# ===============================
# スタート画面
# ===============================
async def show_start_screen():
    while True:
        await asyncio.sleep(0)
        screen.fill((80, 208, 255))

        title = titlefont.render("シューティングゲーム", True, (255, 255, 255))
        screen.blit(title, (120, 150))

        text = font.render("スペースを押してゲーム開始！　的を撃ちぬけ！", True, (255, 255, 255))
        screen.blit(text, (110, 350))

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and event.key == K_SPACE:
                return

        pygame.display.update()
        clock.tick(60)
        await asyncio.sleep(0)

# ===============================
# クリア画面
# ===============================
async def show_clear_screen():
    while True:
        await asyncio.sleep(0)
        screen.fill((80, 208, 255))

        cleartext = font.render("おめでとう！ゲームクリア！", True, (255, 255, 255))
        screen.blit(cleartext, (200, 200))

        info = font.render("スペースキーで終了", True, (255, 255, 255))
        screen.blit(info, (250, 300))

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and event.key == K_SPACE:
                return

        pygame.display.update()
        clock.tick(60)
        await asyncio.sleep(0)

# ===============================
# ゲームオーバー画面
# ===============================
async def show_gameover_screen():
    while True:
        await asyncio.sleep(0)
        screen.fill((0, 0, 0))

        over_text = titlefont.render("ゲームオーバー", True, (255, 0, 0))
        screen.blit(over_text, (250, 200))

        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(score_text, (300, 280))

        info = font.render("スペースキーでリスタートできます", True, (255, 255, 255))
        screen.blit(info, (260, 350))

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and event.key == K_SPACE:
                return True

        pygame.display.update()
        clock.tick(60)
        await asyncio.sleep(0)

# ===============================
# メインループ
# ===============================

async def _web_main():
    global bgm_playing, cross_x, cross_y, dist, dx, dy, event, ex, ey, game_result, hp, i, running, score, target
    while True:
        await asyncio.sleep(0)
        await show_start_screen()
        reset_game()

        running = True

        while running:
            await asyncio.sleep(0)
            if not bgm_playing:
                pygame.mixer.music.play(-1)
                bgm_playing = True

            clock.tick(60)
            await asyncio.sleep(0)

            # -------- イベント --------
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    return

                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False

                    if event.key == K_SPACE:
                        for i, (ex, ey) in enumerate(enemies):
                            if crosshair_img.get_rect(center=(cross_x, cross_y)).colliderect(
                                    enemy_img.get_rect(center=(ex, ey))):
                                score += 10
                                killed_order.append([ex, ey])
                                del enemies[i]
                                break

            # -------- クロスヘア移動 --------
            if enemies:
                target = min(enemies, key=lambda e: math.hypot(e[0]-cross_x, e[1]-cross_y))
                dx, dy = target[0]-cross_x, target[1]-cross_y
                dist = math.hypot(dx, dy)

                if dist != 0:
                    cross_x += dx / dist * cross_speed
                    cross_y += dy / dist * cross_speed

                if dist < 5:
                    hp -= 10
                    killed_order.append(target)
                    enemies.remove(target)

            if len(killed_order) >= 10:
                enemies.append(killed_order.pop(0))

            # -------- 判定 --------
            if score >= 150:
                pygame.mixer.music.stop()
                game_result = "クリア"
                running = False

            if hp <= 0:
                pygame.mixer.music.stop()
                game_result = "ゲームオーバー"
                running = False

            # -------- 描画 --------
            screen.blit(bg_img, (0, 0))
            for ex, ey in enemies:
                screen.blit(enemy_img, enemy_img.get_rect(center=(ex, ey)))

            screen.blit(crosshair_img, crosshair_img.get_rect(center=(cross_x, cross_y)))
            screen.blit(font.render(f"HP: {hp}", True, (200, 0, 0)), (500, 20))
            screen.blit(font.render(f"Score: {score}", True, (0, 0, 0)), (300, 20))
            screen.blit(font.render("シューティングゲーム", True, (0, 0, 0)), (10, 20))

            pygame.display.update()

        # ===== 結果画面 =====
        if game_result == "クリア":
            await show_clear_screen()
            break

        elif game_result == "ゲームオーバー":
            if await show_gameover_screen():
                continue

    pygame.quit()
    return





asyncio.run(_web_main())