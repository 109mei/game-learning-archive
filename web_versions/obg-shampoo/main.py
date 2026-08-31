# --- Web版 (pygbag対応のための変換コピー / ゲーム内容は変更していません) ---
import asyncio
import sys
import pygame
import random
from pygame.locals import *
import os

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

#基本設定
W, H = 1920, 1080
font_path = "NotoSansJP-Regular.ttf"
FONT_SIZE = 32
STEM_LENGTH_FACTOR = 2.0
#ゲーム進行設定
# 問題数やボーナス条件などの定数
QUESTION_LIMIT = 15        # 全問数
BONUS_THRESHOLD = 10       # 正解数がこれ以上でボーナス
BONUS_TIME_SEC = 5         # ボーナスタイム秒数
BONUS_POINTS_PER_PRESS = 20  # ボーナスタイム中の1回あたりの加点

pygame.init()
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("shampoo!")
clock = pygame.time.Clock()

#フォント設定
def make_font(size):
    try:
        if font_path and os.path.isfile(font_path):
            return pygame.font.Font(font_path, size)
    except Exception:
        pass

    candidates = [
        "Meiryo",
        "Yu Gothic",
        "MS Gothic",
        "MS PGothic",
        "Noto Sans CJK JP",
        "TakaoPGothic",
        "TakaoGothic",
    ]
    for name in candidates:
        try:
            f = pygame.font.SysFont(name, size)
            if f:
                return f
        except Exception:
            continue

    return pygame.font.SysFont(None, size)

font = make_font(FONT_SIZE)
font_small = make_font(24)
font_large = make_font(48)

def scale_image_keep_aspect(image, max_w, max_h):
    try:
        w, h = image.get_size()
        if w == 0 or h == 0:
            return image
        ratio = min(max_w / w, max_h / h)
        new_w = max(1, int(w * ratio))
        new_h = max(1, int(h * ratio))
        try:
            return pygame.transform.smoothscale(image, (new_w, new_h))
        except Exception:
            return pygame.transform.scale(image, (new_w, new_h))
    except Exception:
        return image

#背景画像読み込み
try:
    BACKGROUND_PATH = "asset/images/background.png"
    if os.path.isfile(BACKGROUND_PATH):
        _bg = pygame.image.load(BACKGROUND_PATH).convert()
        BACKGROUND_IMAGE = pygame.transform.scale(_bg, (W, H))
    else:
        BACKGROUND_IMAGE = None
except Exception:
    BACKGROUND_IMAGE = None


#プッシュボタン画像読み込み
try:
    BUTTON_IMAGE = None
    BUTTON_PRESSED_IMAGE = None
    candidates = [
        ("asset/images/button.png", "asset/images/button_pressed.png"),
        ("asset/images/bottle.png", "asset/images/bottle_pressed.png"),
        ("asset/images/button_default.png", "asset/images/button_default_pressed.png"),
    ]
    for normal_path, pressed_path in candidates:
        if os.path.isfile(normal_path):
            try:
                BUTTON_IMAGE = pygame.image.load(normal_path).convert_alpha()
            except Exception:
                BUTTON_IMAGE = None
        if os.path.isfile(pressed_path):
            try:
                BUTTON_PRESSED_IMAGE = pygame.image.load(pressed_path).convert_alpha()
            except Exception:
                BUTTON_PRESSED_IMAGE = None
        if BUTTON_IMAGE is not None:
            break
except Exception:
    BUTTON_IMAGE = None
    BUTTON_PRESSED_IMAGE = None


def make_vector_button_surface(w, h, pressed=False, stem_length_factor=1.0):
    surf = pygame.Surface((w, h), pygame.SRCALPHA)

    # カラー設定
    bottle_color = (180, 220, 250)
    cap_color = (160, 200, 240)
    pump_color = (200, 230, 255)
    stem_color = (255, 255, 255)
    border_color = (100, 100, 100)

    # ボトル本体
    bottle_w = int(w * 0.4)
    bottle_h = int(h * 0.6)
    bottle_x = (w - bottle_w) // 2
    bottle_y = int(h * 0.35)
    br = int(min(w, h) * 0.2)
    pygame.draw.rect(surf, bottle_color, (bottle_x, bottle_y, bottle_w, bottle_h), border_radius=br)
    pygame.draw.rect(surf, border_color, (bottle_x, bottle_y, bottle_w, bottle_h), 2, border_radius=br)

    # キャップ
    cap_w = int(bottle_w * 0.5)
    cap_h = int(h * 0.05)
    cap_x = (w - cap_w) // 2
    cap_y = bottle_y - cap_h + 4
    pygame.draw.rect(surf, cap_color, (cap_x, cap_y, cap_w, cap_h), border_radius=cap_h // 2)
    pygame.draw.rect(surf, border_color, (cap_x, cap_y, cap_w, cap_h), 2, border_radius=cap_h // 2)

    # ポンプヘッド
    head_w = int(w * 0.15)
    head_h = int(h * 0.06)
    head_x = (w - head_w) // 2
    head_y = cap_y - head_h - 2
    if pressed:
        head_y += 4
    pygame.draw.rect(surf, pump_color, (head_x, head_y, head_w, head_h), border_radius=head_h // 2)
    pygame.draw.rect(surf, border_color, (head_x, head_y, head_w, head_h), 2, border_radius=head_h // 2)

    # ステム
    stem_w = max(2, int(w * 0.02))
    stem_h = max(2, int((cap_y - (head_y + head_h)) * stem_length_factor))
    stem_x = head_x + (head_w - stem_w) // 2
    stem_y = head_y + head_h
    pygame.draw.rect(surf, stem_color, (stem_x, stem_y, stem_w, stem_h))
    pygame.draw.rect(surf, border_color, (stem_x, stem_y, stem_w, stem_h), 1)

    # ノズル
    nozzle_w = int(head_w * 0.4)
    nozzle_h = int(h * 0.03)
    nozzle_x = head_x - nozzle_w + 4
    nozzle_y = head_y + head_h // 2 - nozzle_h // 2
    pygame.draw.rect(surf, pump_color, (nozzle_x, nozzle_y, nozzle_w, nozzle_h), border_radius=nozzle_h // 2)
    pygame.draw.rect(surf, border_color, (nozzle_x, nozzle_y, nozzle_w, nozzle_h), 2, border_radius=nozzle_h // 2)

    # 押下時
    if pressed:
        overlay = pygame.Surface((w, h), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 30))
        surf.blit(overlay, (0, int(h * 0.02)))

    return surf


#髪の画像ファイル（同じ画像を大きさを変えて使い分ける）
HAIR_IMAGE_FILES = [
    "asset/images/ahiru.png",
    "asset/images/hane.png",
    "asset/images/pikopiko.png",
    "asset/images/toge.png",
    "asset/images/girl.png",
]

#表示倍率
HAIR_IMAGE_MULTIPLIERS = [1.0, 2.0, 2.25, 1.25, 1.5]

#髪のパターンデータ
# (髪の長さスコア, サイズ, 推奨シャンプータイプレベル, image_index_in_IMAGE_PATHS, (min_presses, max_presses))
HAIR_LENGTHS = [
    (5,  "1.0倍",  0, 2, (0, 1)),  #ほとんど不要
    (30, "1.5倍",  1, 1, (3, 5)),  #中くらい
    (35, "2.0倍",  1, 4, (2, 4)),  #中程度
    (40, "2.5倍",  2, 3, (4, 6)),  #やや多め
    (45, "3.0倍",  2, 0, (6, 8)),  #多め
]

# メニュー画面
async def show_menu():
    if BACKGROUND_IMAGE:
        screen.blit(BACKGROUND_IMAGE, (0, 0))
    else:
        screen.fill((230, 240, 250))

    try:
        title_font = pygame.font.Font(font_path, 72)
    except Exception:
        title_font = pygame.font.SysFont(None, 72)
    title = title_font.render("shampoo!", True, (10, 10, 40))
    screen.blit(title, ((W - title.get_width()) // 2, H // 4))

    try:
        guide_font = pygame.font.Font(font_path, 28)
    except Exception:
        guide_font = pygame.font.SysFont(None, 28)
    guide_lines = [
        "Enterキーでゲーム開始",
        "ESCキーで終了します",
        "スペースで連打してシャンプーの量を調整！",
        "制限時間内に適切な回数を押して正解を目指そう！",
        "何度もプレイして適切なシャンプーの量を覚えよう！",
        f"全{QUESTION_LIMIT}問中{BONUS_THRESHOLD}問以上正解でボーナスタイム突入！",
        f"ボーナスタイム中は連打で{BONUS_POINTS_PER_PRESS}点ずつ加点！",
        "ハイスコアを目指して頑張ろう！",

    ]
    for i, line in enumerate(guide_lines):
        guide_text = guide_font.render(line, True, (40, 40, 40))
        screen.blit(guide_text, ((W - guide_text.get_width()) // 2, H // 2 + i * 40))

    pygame.display.flip()


async def show_countdown(seconds=3):
    for sec in range(seconds, 0, -1):
        start = pygame.time.get_ticks()
        screen.fill((20, 20, 40))
        try:
            title_font = pygame.font.Font(font_path, 72)
        except Exception:
            title_font = pygame.font.SysFont(None, 72)
        title = title_font.render("shampoo!", True, (255, 255, 255))
        screen.blit(title, ((W - title.get_width()) // 2, H // 4))

        num_text = font_large.render(str(sec), True, (255, 200, 50))
        screen.blit(num_text, ((W - num_text.get_width()) // 2, (H - num_text.get_height()) // 2))

        pygame.display.flip()

        # 1秒間イベント処理・待機
        while pygame.time.get_ticks() - start < 1000:
            await asyncio.sleep(0)
            for ev in pygame.event.get():
                if ev.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif ev.type == KEYDOWN:
                    if ev.key == K_ESCAPE:
                        pygame.quit()
                        sys.exit()


# 本編
async def run_game():
    # スコア管理
    score = 0
    combo = 0
    max_combo = 0
    question_count = 0
    correct_count = 0
    game_running = True
    current_customer = None
    result_message = ""
    result_time = 0

    # 最終画面
    final_pending = False
    final_saved = False
    
    # ボタン押下管理
    button_press_count = 0  # 現在のボタン押下数
    button_press_feedback_time = 0 
    # ボーナスモード管理
    bonus_mode = False
    bonus_frames_remaining = 0
    bonus_press_count = 0
    bonus_score = 0
    # 次のあひるを保留
    next_customer_pending = False
    
    # あひるを生成
    def get_new_customer():
        # pick a pattern that now includes press range and image index
        hair_length, hair_name, required_shampoo, image_index, press_range = random.choice(HAIR_LENGTHS)
        customer_image = None
        image_path = None
        display_w = 200
        display_h = 300
        try:
            # image_index は HAIR_LENGTHS の4番目の要素として定義
            hair_image_index = image_index
            # 優先: 画像ごとの固定倍率があれば使用（indexに対応）
            try:
                if 0 <= hair_image_index < len(HAIR_IMAGE_MULTIPLIERS):
                    multiplier = float(HAIR_IMAGE_MULTIPLIERS[hair_image_index])
            except Exception:
                multiplier = None

            if 0 <= hair_image_index < len(HAIR_IMAGE_FILES):
                candidate = HAIR_IMAGE_FILES[hair_image_index]
                if candidate and os.path.isfile(candidate):
                    image_path = candidate
                    # 候補ファイルから倍率を決定できる場合は使う
                    if multiplier is None and candidate in HAIR_IMAGE_FILES:
                        try:
                            idx = HAIR_IMAGE_FILES.index(candidate)
                            if 0 <= idx < len(HAIR_IMAGE_MULTIPLIERS):
                                multiplier = float(HAIR_IMAGE_MULTIPLIERS[idx])
                        except Exception:
                            pass
                    # 
                    if multiplier is None:
                        try:
                            if isinstance(hair_name, str) and hair_name.endswith("倍"):
                                multiplier = float(hair_name.replace("倍", "").strip())
                            else:
                                multiplier = max(0.1, float(hair_length) / 40.0)
                        except Exception:
                            multiplier = 1.0
                    display_w = max(1, int(200 * multiplier))
                    display_h = max(1, int(300 * multiplier))
                    customer_image = pygame.image.load(image_path).convert_alpha()
                    customer_image = scale_image_keep_aspect(customer_image, display_w, display_h)
            # fallback: pick any available HAIR_IMAGE_FILES image
            if customer_image is None:
                fallback_path = None
                if 0 <= image_index < len(HAIR_IMAGE_FILES) and os.path.isfile(HAIR_IMAGE_FILES[image_index]):
                    fallback_path = HAIR_IMAGE_FILES[image_index]
                else:
                    for p in HAIR_IMAGE_FILES:
                        if p and os.path.isfile(p):
                            fallback_path = p
                            break
                if fallback_path:
                    image_path = fallback_path
                    # fallback のファイルに対応する固定倍率を使えるなら使う
                    try:
                        idx = HAIR_IMAGE_FILES.index(fallback_path)
                        if 0 <= idx < len(HAIR_IMAGE_MULTIPLIERS):
                            multiplier = float(HAIR_IMAGE_MULTIPLIERS[idx])
                    except Exception:
                        pass
                    # まだ未決定なら HAIR_LENGTHS の名前や長さから推測
                    if multiplier is None:
                        try:
                            if isinstance(hair_name, str) and hair_name.endswith("倍"):
                                multiplier = float(hair_name.replace("倍", "").strip())
                            else:
                                multiplier = max(0.1, float(hair_length) / 40.0)
                        except Exception:
                            multiplier = 1.0
                    display_w = max(1, int(200 * multiplier))
                    display_h = max(1, int(300 * multiplier))
                    customer_image = pygame.image.load(image_path).convert_alpha()
                    customer_image = scale_image_keep_aspect(customer_image, display_w, display_h)
        except Exception:
            customer_image = None

            customer_image = None

        return {
            "hair_length": hair_length,
            "hair_name": hair_name,
            "required_shampoo": required_shampoo,
            "image_index": image_index,
            "image_path": image_path,
            "image": customer_image,
            "press_range": press_range,
            "display_size": (display_w, display_h),
            "display_multiplier": multiplier,
            "display_time": 0,
            # 制限時間: 5秒 -> 300フレーム
            "time_limit_frames": 300
        }
    
    current_customer = get_new_customer()

    # BGM と効果音の読み込み（存在するファイルを優先して使用）
    duck_sound = None
    correct_sound = None
    bonus_start_sound = None
    game_end_sound = None
    incorrect_sound = None

    try:
        bg_path = "asset/sounds/backmusic.ogg"
        if not os.path.isfile(bg_path):
            bg_path = "asset/sounds/5.ogg"
        if os.path.isfile(bg_path):
            if not pygame.mixer.music.get_busy():
                pygame.mixer.music.load(bg_path)
                pygame.mixer.music.play(-1)
                pygame.mixer.music.set_volume(0.5)
    except Exception:
        pass

    # 効果音
    try:
        p = "asset/sounds/6.ogg"  # 正解時
        if os.path.isfile(p):
            correct_sound = pygame.mixer.Sound(p)
    except Exception:
        correct_sound = None

    try:
        p = "asset/sounds/7.ogg"  # ボーナスタイム開始時
        if os.path.isfile(p):
            bonus_start_sound = pygame.mixer.Sound(p)
    except Exception:
        bonus_start_sound = None

    try:
        p = "asset/sounds/9.ogg"  # ボーナスタイム中の連打
        if os.path.isfile(p):
            bonus_press_sound = pygame.mixer.Sound(p)
    except Exception:
        bonus_press_sound = None

    try:
        p = "asset/sounds/13.ogg"  # ゲーム終了時
        if os.path.isfile(p):
            game_end_sound = pygame.mixer.Sound(p)
    except Exception:
        game_end_sound = None

    try:
        p = "asset/sounds/5.ogg"  # あひる表示時
        if os.path.isfile(p):
            duck_sound = pygame.mixer.Sound(p)
    except Exception:
        duck_sound = None
    # あひる出現時の効果音を再生
    try:
        if current_customer and duck_sound:
            duck_sound.play()
    except Exception:
        pass

    # ゲームループ
    while game_running:
        await asyncio.sleep(0)
        clock.tick(60)
        await asyncio.sleep(0)
        if current_customer:
            current_customer["display_time"] += 1
        
        if button_press_feedback_time > 0:
            button_press_feedback_time -= 1

        #制限時間で判定（5秒=300フレーム想定）
        if current_customer and current_customer.get("display_time", 0) >= current_customer.get("time_limit_frames", 300):
            question_count += 1
            min_presses, max_presses = current_customer.get("press_range", (0, 0))

            if min_presses <= button_press_count <= max_presses:
                result_message = f"正解！{button_press_count}回"
                correct_count += 1
                combo += 1
                max_combo = max(max_combo, combo)
                score += 100 + (combo * 10)
                if correct_sound:
                    correct_sound.play()
            else:
                result_message = f"不正解 必要:{min_presses}-{max_presses}回 選択:{button_press_count}回"
                combo = 0
                if incorrect_sound:
                    incorrect_sound.play()

            #後処理（正解/不正解に関わらず）
            result_time = 90
            button_press_count = 0

            #次のあひる保留
            next_customer_pending = True

            #問題数が上限に達したらボーナス判定または終了処理
            if question_count >= QUESTION_LIMIT:
                if correct_count >= BONUS_THRESHOLD:
                    bonus_mode = True
                    bonus_frames_remaining = BONUS_TIME_SEC * 60
                    bonus_press_count = 0
                    bonus_score = 0
                    result_message = "ボーナスタイム！連打でボーナスを稼ごう！"
                    result_time = 90
                    # 次のあひるは表示しない
                    current_customer = None
                    try:
                        if bonus_start_sound:
                            bonus_start_sound.play()
                    except Exception:
                        pass
                else:
                    # ボーナスに届かない場合はゲーム終了
                    result_message = f"終了: {correct_count}/{QUESTION_LIMIT} 正解"
                    result_time = 180
                    current_customer = None
                    final_pending = True
                    try:
                        if game_end_sound:
                            game_end_sound.play()
                    except Exception:
                        pass
            else:
                current_customer = None
        
        #最終画面用のリトライボタン
        retry_rect = pygame.Rect((W - 300) // 2, H // 2 + 40, 300, 80)

        #イベント処理
        for event in pygame.event.get():
            if event.type == QUIT:
                return False
            elif event.type == KEYDOWN:

                if final_pending and result_time <= 0:
                    if event.key == K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                    if event.key == K_r:
                        score = 0
                        combo = 0
                        max_combo = 0
                        question_count = 0
                        correct_count = 0
                        result_message = ""
                        result_time = 0
                        button_press_count = 0
                        button_press_feedback_time = 0
                        bonus_mode = False
                        bonus_frames_remaining = 0
                        bonus_press_count = 0
                        bonus_score = 0
                        current_customer = get_new_customer()
                        try:
                            if duck_sound:
                                duck_sound.play()
                        except Exception:
                            pass
                        final_pending = False
                        final_saved = False

                        await show_countdown(3)
                    continue

                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                #スペースキーでの処理
                elif event.key == K_SPACE:
                    #判定結果表示中はボタンを無効化
                    if result_time > 0:
                        continue
                    #ボーナスモード中はボーナス用のカウント
                    if bonus_mode:
                        bonus_press_count += 1
                        button_press_feedback_time = 10
                        try:
                            if bonus_press_sound:
                                bonus_press_sound.play()
                        except Exception:
                            pass
                    else:

                        button_press_count += 1
                        button_press_feedback_time = 10

            elif event.type == MOUSEBUTTONDOWN:

                if final_pending and result_time <= 0:
                    if event.button == 1:
                        if retry_rect.collidepoint(event.pos):
                            score = 0
                            combo = 0
                            max_combo = 0
                            question_count = 0
                            correct_count = 0
                            result_message = ""
                            result_time = 0
                            button_press_count = 0
                            button_press_feedback_time = 0
                            bonus_mode = False
                            bonus_frames_remaining = 0
                            bonus_press_count = 0
                            bonus_score = 0
                            current_customer = get_new_customer()
                            try:
                                if duck_sound:
                                    duck_sound.play()
                            except Exception:
                                pass
                            final_pending = False
                            final_saved = False
                            await show_countdown(3)
                            continue
        
        # 画面描画
        if BACKGROUND_IMAGE:
            screen.blit(BACKGROUND_IMAGE, (0, 0))
        else:
            screen.fill((240, 250, 255))
        
        #スコア表示
        score_text = font.render(f"スコア: {score}", True, (0, 0, 0))
        screen.blit(score_text, (20, 20))
        
        combo_text = font_small.render(f"コンボ: {combo}", True, (0, 100, 200))
        screen.blit(combo_text, (20, 70))
        
        count_text = font_small.render(f"問題: {question_count} 正解: {correct_count}", True, (0, 0, 0))
        screen.blit(count_text, (20, 110))

        question_text = font_small.render(f"残りの問題数: {15-question_count}", True, (0, 0, 0))
        screen.blit(question_text, (20, 150))
        
        # あひるを表示
        if current_customer and current_customer.get("image"):
            ds = current_customer.get("display_size", (300, 450))
            ahiru_img = scale_image_keep_aspect(current_customer["image"], ds[0], ds[1])
            screen.blit(ahiru_img, ((W - ahiru_img.get_width()) // 2, 100))

        #ボーナスモード画面描画
        if bonus_mode:
            #ボーナスタイムの残り時間と現在の連打数を表示
            remain_sec = bonus_frames_remaining // 60
            remain_text = font_large.render(f"BONUS TIME: {remain_sec}s", True, (255, 200, 50))
            screen.blit(remain_text, ((W - remain_text.get_width()) // 2, 80))

            bonus_count_text = font_large.render(str(bonus_press_count), True, (255, 50, 50))
            screen.blit(bonus_count_text, ((W - bonus_count_text.get_width()) // 2, 180))
        
        # プッシュボタンを表示
        button_x = W // 2 - 260
        button_y = H // 2 + 40
        button_width = 260*2
        button_height = 180*2

        feedback_offset = 0
        if button_press_feedback_time > 0:
            feedback_offset = int(10 * (1 - button_press_feedback_time / 10))

        # ベクター描画を使う（いつも使いたい場合は True にする）
        USE_VECTOR_BUTTON = True
        if globals().get("BUTTON_IMAGE") and not USE_VECTOR_BUTTON:
            img_to_use = globals().get("BUTTON_IMAGE")
            if button_press_feedback_time > 0 and globals().get("BUTTON_PRESSED_IMAGE"):
                img_to_use = globals().get("BUTTON_PRESSED_IMAGE")
            img_draw = scale_image_keep_aspect(img_to_use, button_width, button_height)
            img_x = button_x + (button_width - img_draw.get_width()) // 2
            img_y = button_y + feedback_offset
            screen.blit(img_draw, (img_x, img_y))
            #ボタンテキスト（画像に無い場合にのみ描画）
            button_text = font_large.render("PUSH", True, (255, 255, 255))
            screen.blit(button_text, (button_x + button_width // 2 - button_text.get_width() // 2, img_y + (button_height - button_text.get_height()) // 2))
        else:
            # ベクターで生成したボタン画像を使う（キャッシュして毎フレーム再生成を避ける）
            try:
                if "_vector_button_cache" not in locals():
                    _vector_button_cache = {}
            except Exception:
                _vector_button_cache = {}

            key = (button_width, button_height, STEM_LENGTH_FACTOR)
            if key not in _vector_button_cache:
                _vector_button_cache[key] = (
                    make_vector_button_surface(button_width, button_height, pressed=False, stem_length_factor=STEM_LENGTH_FACTOR),
                    make_vector_button_surface(button_width, button_height, pressed=True, stem_length_factor=STEM_LENGTH_FACTOR)
                )
            vec_normal, vec_pressed = _vector_button_cache[key]
            img_draw = vec_pressed if button_press_feedback_time > 0 else vec_normal
            img_x = button_x + (button_width - img_draw.get_width()) // 2
            img_y = button_y + feedback_offset + (4 if button_press_feedback_time > 0 else 0)
            screen.blit(img_draw, (img_x, img_y))

        
        # 現在の押回数を表示
        display_press_count = bonus_press_count if bonus_mode else button_press_count
        press_count_text = font_large.render(str(display_press_count), True, (255, 0, 0))
        screen.blit(press_count_text, (button_x + button_width // 2 - press_count_text.get_width() // 2, button_y + 270))
        
        #結果メッセージ
        if result_time > 0:
            if "正解" in result_message:
                result_color = (0, 200, 0)
            else:
                result_color = (200, 0, 0)
            
            result_text = font.render(result_message, True, result_color)
            screen.blit(result_text, ((W - result_text.get_width()) // 2, H // 2 - 100))
            
            result_time -= 1

        if result_time <= 0 and next_customer_pending and (not final_pending) and (not bonus_mode):
            current_customer = get_new_customer()
            try:
                if duck_sound:
                    duck_sound.play()
            except Exception:
                pass
            next_customer_pending = False

        #最終画面表示判定
        if final_pending and result_time <= 0:
            #最終画面描画
            if BACKGROUND_IMAGE:
                screen.blit(BACKGROUND_IMAGE, (0, 0))
            else:
                screen.fill((230, 230, 240))
            final_title = font_large.render("ゲーム終了", True, (10, 10, 40))
            screen.blit(final_title, ((W - final_title.get_width()) // 2, 120))

            final_score_text = font.render(f"最終スコア: {score}", True, (0, 0, 0))
            screen.blit(final_score_text, ((W - final_score_text.get_width()) // 2, 220))

            #リトライボタン
            retry_rect = pygame.Rect((W - 300) // 2, H // 2 + 40, 300, 80)
            pygame.draw.rect(screen, (100, 200, 100), retry_rect)
            pygame.draw.rect(screen, (0, 120, 0), retry_rect, 4)
            retry_text = font_large.render("リトライ", True, (255, 255, 255))
            screen.blit(retry_text, (retry_rect.x + (retry_rect.width - retry_text.get_width()) // 2,
                                     retry_rect.y + (retry_rect.height - retry_text.get_height()) // 2))

            hint_text = font_small.render("Rキーでもリトライ | ESCでメニューへ", True, (80, 80, 80))
            screen.blit(hint_text, ((W - hint_text.get_width()) // 2, retry_rect.y + retry_rect.height + 20))

            pygame.display.flip()
            continue

        # ボーナスモードの更新
        if bonus_mode:
            if bonus_frames_remaining > 0:
                bonus_frames_remaining -= 1
            else:
                # ボーナスタイム終了→スコア加算して終了
                bonus_score = bonus_press_count * BONUS_POINTS_PER_PRESS
                score += bonus_score
                result_message = f"ボーナス +{bonus_score}点！"
                result_time = 180
                bonus_mode = False
                final_pending = True
                try:
                    if game_end_sound:
                        game_end_sound.play()
                except Exception:
                    pass
        
        # 操作説明
        if bonus_mode:
            help_line = "ボーナス中：スペースで連打してボーナスを稼ごう！ | ESCで終了"
        else:
            help_line = "スペースで連打 → (自動で5秒後に判定) | ESCで終了"
        help_text = font_small.render(help_line, True, (100, 100, 100))
        screen.blit(help_text, ((W - help_text.get_width()) // 2, H - 80))
        
        pygame.display.flip()

# メイン処理
async def main():
    running = True
    while running:
        await asyncio.sleep(0)
        await show_menu()
        
        # メニュー画面でのキー入力待機
        waiting_for_input = True
        while waiting_for_input:
            await asyncio.sleep(0)
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                    waiting_for_input = False
                if event.type == KEYDOWN:
                    if event.key == K_RETURN:  # Enter
                        waiting_for_input = False
                    elif event.key == K_ESCAPE:  # ESC
                        pygame.quit()
                        sys.exit()
            
            clock.tick(60)
            await asyncio.sleep(0)
        
        if running:
            await show_countdown(3)
            running = await run_game()


async def _web_main():
    if __name__ == "__main__":
        await main()
        pygame.quit()
        return

asyncio.run(_web_main())