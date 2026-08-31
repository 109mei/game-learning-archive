# --- Web版 (pygbag対応のための変換コピー / ゲーム内容は変更していません) ---
import asyncio
#使用モジュール
import pygame
import os
import sys
import time
import random
from pathlib import Path


# OS判定と適切な設定適用
if sys.platform == "win32": # Windows 
    pass  # web: ctypes無効化 | import ctypes
    pass  # web: ctypes無効化 | ctypes.windll.user32.SetProcessDPIAware()
    #DPIスケール無効化 
    os.environ['SDL_VIDEO_CENTERED'] = '1'
elif sys.platform == "darwin": # macOS
    os.environ['SDL_VIDEO_WINDOW_POS'] = '100,100'
    os.environ['SDL_VIDEO_CENTERED'] = '1'
elif sys.platform.startswith("linux"): # Linux 
    os.environ[ 
 'SDL_VIDEO_X11_NET_WM_BYPASS_COMPOSITOR'] = '0' 
    os.environ['SDL_VIDEO_CENTERED'] = '1'

elif sys.platform.startswith("freebsd") or sys.platform.startswith("openbsd") or sys.platform.startswith("netbsd"): # BSD系
    os.environ['SDL_VIDEO_CENTERED'] = '1'
 
elif sys.platform.startswith("sunos"): # Solaris 
   os.environ['SDL_VIDEO_CENTERED'] = '1'
elif sys.platform.startswith("haiku"): # Haiku OS 
   os.environ['SDL_VIDEO_WINDOW_POS'] = '50,50'
elif sys.platform.startswith("android"): # Android 
    os.environ['SDL_VIDEO_CENTERED'] = '1' 
    os.environ['SDL_VIDEODRIVER'] = 'android' # Android専用設定
elif sys.platform.startswith("emscripten"): #WebAssembly 
   print("Emscripten (WebAssembly) 環境:追加設定不要")
elif sys.platform.startswith("cygwin") or sys.platform.startswith("msys"): # Cygwin / MSYS2 
    os.environ['SDL_VIDEO_CENTERED'] = '1'
elif sys.platform.startswith("riscos"): # RISC OS 
    os.environ['SDL_VIDEO_CENTERED'] = '1'
elif sys.platform.startswith("aix"): # IBM AIX 
    os.environ['SDL_VIDEO_CENTERED'] = '1'
elif sys.platform.startswith("vxworks"):
    # VxWorks
    os.environ['SDL_VIDEO_CENTERED'] = '1'
elif sys.platform.startswith("os2"): # 05/2 os.environ ['SDL_VIDEO_CENTERED'] = '1'
    pass
elif sys.platform.startswith("amiga"):
    os.environ['SDL_VIDEO_CENTERED'] = '1'

# AmigaOS / Morphos
else: # その他の未知のos
    print(f"警告: このOS ({sys.platform})は未検証です。動作しない可能性があります。")

# 画面サイズ
WIDTH , HEIGHT = 1920 , 1080

#初期化
pygame.init()
pygame.mixer.init()

pygame.mixer.music.load("asset/sounds/bgm.ogg")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)


#ウィンドウ作成

win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Quick Draw")
clock = pygame.time.Clock()
result_time = 0



#日本語フォントの設定
font_path = "NotoSansJP-Regular.ttf"
font_size = 50
try:
    font = pygame.font.Font(font_path, font_size)
except Exception:
    font = pygame.font.SysFont(None, font_size)
line_spacing = 20

# フォントキャッシュ
font_cache = {font_size: font}

#音
fire_se = pygame.mixer.Sound("asset/sounds/fire.ogg")
shot_se = pygame.mixer.Sound("asset/sounds/shot.ogg")
win_se  = pygame.mixer.Sound("asset/sounds/seikou.ogg")
lose_se = pygame.mixer.Sound("asset/sounds/sippai.ogg")

start_sound_played = False
start_se = pygame.mixer.Sound("asset/sounds/start.ogg")

#スタートボタンの設定
try:
    start_btn_img = pygame.image.load("asset/image/start_btn.png").convert_alpha()
    start_btn_img = pygame.transform.scale(start_btn_img, (600, 300))
except Exception:
    start_btn_img = pygame.Surface((600, 300))
    start_btn_img.fill((80, 80, 80))
start_btn_rect = start_btn_img.get_rect(center=(WIDTH//2, HEIGHT//2 +100))
# 画像サイズ取得
width, height = start_btn_img.get_size()
# スタートボタンテキスト表示
start_text = font.render("START", True, (255, 255, 255), None)
start_text_rect = start_text.get_rect(center=(WIDTH//2, HEIGHT//2 + 100))
win.blit(start_text, start_text_rect)

# リスタートボタンテキスト表示
restart_text = font.render("RESTART", True, (255, 255, 255), None)
restart_text_rect = restart_text.get_rect(center=(WIDTH//2, HEIGHT//2 + 100))

#打撃ボタンの設定
dageki_btn_img = None
try:
    dageki_btn_img = pygame.image.load("asset/image/dageki_btn.png").convert_alpha()
    dageki_btn_img = pygame.transform.scale(dageki_btn_img, (500, 500))
except Exception:
    dageki_btn_img = pygame.Surface((500, 500))
    dageki_btn_img.fill((120, 120, 120))
dageki_btn_rect = dageki_btn_img.get_rect(center=(WIDTH//2, HEIGHT//2 +100))

def load_background():
    background_filename = "cackgrond.png"
    background_path = "asset/image/" + background_filename
    if os.path.exists(background_path):
        try:
            img = pygame.image.load(background_path)
            img = img.convert()
            print(f"背景画像: {background_filename} を使用します。")
            return pygame.transform.scale(img, (WIDTH, HEIGHT))
        except Exception as e:
            print(f"警告: 背景画像の読み込みに失敗しました: {background_path} -> {e}")
    s = pygame.Surface((WIDTH, HEIGHT))
    s.fill((30, 30, 30))
    return s

bg_img = load_background()


# 色
WHITE = (255, 255, 255) 
RED = (255, 100, 100)
GREEN = (100, 255, 100)
BLACK = (0, 0, 0)

# 状態
state = "start"
rounds = 0
player_wins = 0
enemy_wins = 0

#タイミング設定
fire_time = 0
reaction_time = 0
player_shot = False
fire_sound_played = False

def draw_text(text, color, y_offset=0, size=None):
    global font, font_path, font_size, font_cache
    if size is not None:
        temp_font = font_cache.get(size)
        if temp_font is None:
            try:
                temp_font = pygame.font.Font(font_path, size)
            except Exception:
                temp_font = pygame.font.SysFont(None, size)
            font_cache[size] = temp_font
    else:
        temp_font = font
    text_surface = temp_font.render(text, True, color)
    rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 + y_offset))
    win.blit(text_surface, rect)

def draw_rule():
    rule = [
        "<ルール説明>", 
        "startボタンでゲーム開始！",
        "「Fire！」が表示されたら打撃ボタンを押そう！",
        "フライングは負けになるよ！",
        "5本勝負！先に3勝した方が勝ち！",
        "Escキーでゲーム終了",
    ]
    for i , line in enumerate(rule):
        text_surface = font.render(line, True, BLACK)
        rect = text_surface.get_rect(center=(WIDTH//2, 50 + i * 50))
        win.blit(text_surface, rect)

def reset_round():
    global state, fire_time, player_shot, fire_sound_played
    state = "wait"
    fire_time = time.perf_counter() + random.randint(2 , 5)
    player_shot = False
    fire_sound_played = False

#メイン部分
running = True

async def _web_main():
    global enemy_wins, event, fire_sound_played, now, overlay, player_shot, player_wins, reaction_time, result_color, result_message, result_time, running, start_sound_played, state
    while running:
        await asyncio.sleep(0)
        if 'bg_img' in globals() and bg_img is not None:
            win.blit(bg_img, (0, 0))
        else:
            win.fill(BLACK)
        now = time.perf_counter()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            #ESCキーでゲーム終了
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            #判定
            if event.type == pygame.MOUSEBUTTONDOWN:
                if state == "start" and start_btn_rect.collidepoint(event.pos):
                    player_wins = 0
                    enemy_wins = 0
                    if not start_sound_played:
                        start_se.play()
                        start_sound_played = True
                    start_sound_played = False
                    reset_round()
                elif state == "end" and start_btn_rect.collidepoint(event.pos):
                    state = "start"
                    if not start_sound_played:
                        start_se.play()
                        start_sound_played = True
                    start_sound_played = False
                elif state == "wait" and dageki_btn_rect.collidepoint(event.pos):
                    # フライング負け
                    player_shot = True
                    enemy_wins += 1
                    result_message = "Too Early!"
                    result_color = RED
                    result_time = time.perf_counter()
                    state = "result"
                    try:
                        lose_se.play()
                    except Exception:
                        pass
                elif state == "fire" and dageki_btn_rect.collidepoint(event.pos) and not player_shot:
                    # 正常の射撃判定
                    reaction_time = (time.perf_counter() - fire_time) * 1000
                    player_shot = True
                    try:
                        shot_se.play()
                    except Exception:
                        pass
                    if reaction_time < 450:
                        player_wins += 1
                        result_message = "You Win! %.2fms" % (reaction_time)
                        result_color = GREEN
                        try:
                            win_se.play()
                        except Exception:
                            pass
                    else:
                        enemy_wins += 1
                        result_message = "You Lose!"
                        result_color = RED
                        try:
                            lose_se.play()
                        except Exception:
                            pass
                    state = "result"
                    result_time = time.perf_counter()


        #画面出力
        if state == "start":
            draw_rule()
            win.blit(start_btn_img, start_btn_rect)


            win.blit(start_text, start_text_rect)
        elif state == "wait":
            draw_text("Ready...", BLACK , -220 , size=100)
            if now >= fire_time:
                state = "fire"
            win.blit(dageki_btn_img, dageki_btn_rect)
        elif state == "fire":
            draw_text("FIRE!", RED , -220 , size=100)
            if not fire_sound_played:
                try:
                    fire_se.play()
                except Exception:
                    pass
                fire_sound_played = True
            win.blit(dageki_btn_img, dageki_btn_rect)
        elif state == "result":
            if 'bg_img' in globals() and bg_img is not None:
                win.blit(bg_img, (0, 0))
            else:
                win.fill(BLACK)
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 160))
            win.blit(overlay, (0, 0))
            draw_text(result_message, result_color, y_offset=0, size=100)
            if time.perf_counter() - result_time > 2:
                if player_wins == 3:
                    state = "end"
                elif enemy_wins == 3:
                    state = "end"
                else:
                    reset_round()
        elif state == "end":

            draw_text("ゲーム終了", BLACK, y_offset=-290, size=100)
            if player_wins == 3:
                draw_text(f"君の勝ち! {player_wins} - {enemy_wins}", (0, 255, 150), y_offset=-200, size=100)
            else:
                draw_text(f"君の負け... {player_wins} - {enemy_wins}", (255, 0, 0), y_offset=-200, size=100)
            draw_text("リスタートボタンを押してください", BLACK, y_offset=-110, size=100)
            win.blit(start_btn_img, start_btn_rect)
            win.blit(restart_text, restart_text_rect)

        pygame.display.update()
        clock.tick(60)
        await asyncio.sleep(0)
    pygame.quit()

asyncio.run(_web_main())