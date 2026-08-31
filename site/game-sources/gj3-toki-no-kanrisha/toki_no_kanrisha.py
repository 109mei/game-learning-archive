import pygame
import random
import time
import math
import os
import tkinter as tk
from tkinter import filedialog
from pathlib import Path
import glob
import traceback

# ============================================
# 基本設定 (Basic Settings)
# ============================================
WINDOW_WIDTH = 1920
WINDOW_HEIGHT = 1080
FPS = 60
GAME_TITLE = "時の管理者"

# ============================================
# 色定義 (Color Definitions)
# ============================================
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GRAY = (128, 128, 128)
LIGHT_BLUE = (173, 216, 230)
PURPLE = (147, 112, 219)
ORANGE = (255, 165, 0)
DARK_GRAY = (50, 50, 50)

from pathlib import Path

# ============================================
# 実行ファイル（この .py）の場所を基準にした相対パス
# ============================================
BASE_DIR = Path(__file__).resolve().parent
ASSET_DIR = BASE_DIR / "asset"
IMG_DIR = ASSET_DIR / "画像"
SND_DIR = ASSET_DIR / "効果音・BGM"

# ============================================
# フォント（.py と同じフォルダの日本語フォントを使う）
# ============================================
JP_FONT_TTF = BASE_DIR / "NotoSansJP-Regular.ttf"
JP_FONT_OTF = BASE_DIR / "NotoSansJP-Regular.otf"
JP_FONT_PATH = JP_FONT_TTF if JP_FONT_TTF.exists() else JP_FONT_OTF

# ============================================
# 画像 / 音ファイルパス定義（配布可能な相対パス）
# ============================================
PLAYER_IMG_PATH = str(IMG_DIR / "130.png")
BOSS_IMG_PATH   = str(IMG_DIR / "80.png")
ITEM_IMG_PATH   = str(IMG_DIR / "82.png")

ENTER_SFX_PATH  = str(SND_DIR / "9.mp3")
BOSS_SFX_PATH   = str(SND_DIR / "1.mp3")

# BGMは「効果音・BGM」フォルダに入っている前提に統一します
BGM_PATH        = str(SND_DIR / "bgm_loop.ogg")   # もしファイル名が違うならここだけ修正


# ============================================
# ゲーム状態 (Game States)
# ============================================
TITLE_SCREEN = "TITLE_SCREEN"
COLLECT_PHASE = "COLLECT_PHASE"
BOSS_PHASE = "BOSS_PHASE"
GAME_CLEAR = "GAME_CLEAR"
GAME_OVER = "GAME_OVER"
GAME_CLEAR_ANIM = "GAME_CLEAR_ANIM"
SCORE_SCREEN = "SCORE_SCREEN"

# ============================================
# プレイヤー設定 (Player Settings)
# ============================================
PLAYER_SIZE = 64
PLAYER_SPEED = 6
JUMP_FORCE = -18
GRAVITY = 1.0
GROUND_Y = WINDOW_HEIGHT - 80

# ============================================
# 入力判定閾値 (Input Thresholds)
# ============================================
SHORT_PRESS_THRESHOLD = 0.15
LONG_PRESS_THRESHOLD = 0.5
DOUBLE_TAP_THRESHOLD = 0.3

# ============================================
# タイマー設定 (Timer Settings)
# ============================================
COLLECT_PHASE_TIME = 30

# ============================================
# 雷設定 (Lightning Settings)
# ============================================
LIGHTNING_INTERVAL = 5.0
LIGHTNING_CHARGE = 1.0
LIGHTNING_DURATION = 0.35

# 雷のバリエーション（色とダメージ倍率）
LIGHTNING_VARIANTS = [
    {"name": "弱", "color": LIGHT_BLUE, "factor": 1.0},
    {"name": "中", "color": YELLOW, "factor": 1.4},
    {"name": "強", "color": PURPLE, "factor": 1.8},
    {"name": "極", "color": ORANGE, "factor": 2.4},
]


class ImageLoader:
    """画像ファイルの読み込みとフォールバック管理（強化版）"""

    IMAGE_EXTS = [".png", ".jpg", ".jpeg", ".bmp", ".gif"]

    def __init__(self):
        self.images = {}
        self.use_fallback = {}
        self.paths = {}

    def _find_image_in_dir(self, dirpath):
        p = Path(dirpath)
        if not p.exists() or not p.is_dir():
            return None
        for ext in self.IMAGE_EXTS:
            for f in p.glob(f"*{ext}"):
                return str(f)
        files = list(p.iterdir())
        return str(files[0]) if files else None

    def _try_variants(self, raw_path):
        """パスの空白や同等のファイル名を緩和して探す"""
        path = os.path.normpath(raw_path.strip())
        p = Path(path)
        if p.exists():
            return str(p)

        if str(raw_path).endswith(os.sep) or (p.parent.exists() and p.name == ""):
            found = self._find_image_in_dir(str(p))
            if found:
                return found

        n = " ".join(raw_path.split())
        parent = p.parent if p.parent.exists() else Path(".")
        base = p.name
        base_no_space = base.replace(" ", "")
        for f in parent.iterdir() if parent.exists() else []:
            fname = f.name
            if fname.replace(" ", "") == base_no_space:
                return str(f)
        glob_try = glob.glob(raw_path + "*")
        for g in glob_try:
            if any(g.lower().endswith(ext) for ext in self.IMAGE_EXTS):
                return g
        return None

    def load_image(self, name, path, fallback_size=None):
        """画像を読み込み、失敗時はフォールバックフラグを設定"""
        self.paths[name] = path
        found = None
        try:
            if path:
                cand = self._try_variants(path)
                if cand:
                    found = cand
                else:
                    cand2 = self._find_image_in_dir(path)
                    if cand2:
                        found = cand2

            if found and Path(found).exists():
                img = pygame.image.load(str(found)).convert_alpha()
                if fallback_size:
                    img = pygame.transform.smoothscale(img, (fallback_size[0], fallback_size[1]))
                self.images[name] = img
                self.use_fallback[name] = False
                self.paths[name] = str(found)
                return
            raise FileNotFoundError(f"Image not found (after variants): {path}")
        except Exception as e:
            print(f"画像読み込み失敗 ({path}): {e} - 図形描画に切り替えます")
            self.images[name] = None
            self.use_fallback[name] = True

    def should_use_fallback(self, name):
        return self.use_fallback.get(name, True)

    def get_image(self, name):
        return self.images.get(name)


class MagicProjectile:
    """プレイヤーの魔法弾（単発、ボスに命中するとダメージ）"""

    def __init__(self, x, y, target_x, target_y, speed=9, damage=1, color=(100, 200, 255)):
        self.x = x
        self.y = y
        dx = target_x - x
        dy = target_y - y
        dist = max(math.hypot(dx, dy), 0.001)
        self.vx = dx / dist * speed
        self.vy = dy / dist * speed
        self.radius = 14
        self.active = True
        self.damage = damage
        self.color = color
        self.spawn_time = time.time()
        self.glow_radius = self.radius * 2
        self.rotation = random.uniform(0, math.pi * 2)

    def update(self):
        self.x += self.vx
        self.y += self.vy
        if self.x < -200 or self.x > WINDOW_WIDTH + 200 or self.y < -200 or self.y > WINDOW_HEIGHT + 200:
            self.active = False
        if time.time() - self.spawn_time > 6.0:
            self.active = False

    def draw(self, screen):
        glow_r = int(self.glow_radius)
        surf = pygame.Surface((glow_r * 2, glow_r * 2), pygame.SRCALPHA)
        for i in range(4, 0, -1):
            a = int(40 * (1.0 - i * 0.12))
            pygame.draw.circle(surf, (*self.color, a), (glow_r, glow_r), int(glow_r * (i / 4.0)))
        screen.blit(surf, (int(self.x - glow_r), int(self.y - glow_r)), special_flags=pygame.BLEND_ADD)

        for i in range(6):
            ang = self.rotation + i * (math.pi * 2 / 6)
            lx = int(self.x + math.cos(ang) * (self.radius + 8))
            ly = int(self.y + math.sin(ang) * (self.radius + 8))
            pygame.draw.line(screen, WHITE, (int(self.x), int(self.y)), (lx, ly), 2)

        for i in range(4):
            talpha = int(80 * (1.0 - i * 0.22))
            tx = int(self.x - self.vx * i * 0.6)
            ty = int(self.y - self.vy * i * 0.6)
            rr = max(2, int(self.radius * (1.0 - i * 0.18)))
            s = pygame.Surface((rr * 2, rr * 2), pygame.SRCALPHA)
            pygame.draw.circle(s, (*self.color, talpha), (rr, rr), rr)
            screen.blit(s, (tx - rr, ty - rr), special_flags=pygame.BLEND_PREMULTIPLIED)

        s = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(s, (*self.color, 255), (self.radius, self.radius), self.radius)
        pygame.draw.circle(s, WHITE, (self.radius, self.radius), self.radius, 2)
        screen.blit(s, (int(self.x - self.radius), int(self.y - self.radius)))

    def get_rect(self):
        return pygame.Rect(int(self.x - self.radius), int(self.y - self.radius), self.radius * 2, self.radius * 2)


class Orb:
    """Tama wo Tobasu の小弾（複数）"""

    def __init__(self, x, y, target_x, target_y, speed=7, damage=1, color=(200, 160, 255)):
        self.x = x
        self.y = y
        dx = target_x - x + random.uniform(-80, 80)
        dy = target_y - y + random.uniform(-40, 40)
        dist = max(math.hypot(dx, dy), 0.001)
        self.vx = dx / dist * speed
        self.vy = dy / dist * speed
        self.radius = 10
        self.active = True
        self.damage = damage
        self.color = color
        self.spawn_time = time.time()
        self.rotation = random.uniform(0, math.pi * 2)

    def update(self):
        self.x += self.vx
        self.y += self.vy
        if self.x < -200 or self.x > WINDOW_WIDTH + 200 or self.y < -200 or self.y > WINDOW_HEIGHT + 200:
            self.active = False
        if time.time() - self.spawn_time > 6.0:
            self.active = False

    def draw(self, screen):
        for i in range(3):
            rr = int(self.radius * (1.0 + i * 0.18))
            a = int(60 * (1.0 - i * 0.3))
            surf = pygame.Surface((rr * 2, rr * 2), pygame.SRCALPHA)
            pygame.draw.circle(surf, (*self.color, a), (rr, rr), rr)
            screen.blit(surf, (int(self.x - rr), int(self.y - rr)), special_flags=pygame.BLEND_PREMULTIPLIED)
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)
        pygame.draw.circle(screen, WHITE, (int(self.x), int(self.y)), self.radius, 2)

    def get_rect(self):
        return pygame.Rect(int(self.x - self.radius), int(self.y - self.radius), self.radius * 2, self.radius * 2)


class Fireball:
    """ボスの炎攻撃（ファイアボール）"""

    def __init__(self, x, y, target_x, target_y, speed=6):
        self.x = x
        self.y = y
        dx = target_x - x
        dy = target_y - y
        dist = max(math.hypot(dx, dy), 0.01)
        self.vx = dx / dist * speed
        self.vy = dy / dist * speed
        self.radius = 10
        self.active = True
        self.spawn_time = time.time()

    def update(self):
        self.x += self.vx
        self.y += self.vy
        if self.x < -50 or self.x > WINDOW_WIDTH + 50 or self.y < -50 or self.y > WINDOW_HEIGHT + 50:
            self.active = False
        if time.time() - self.spawn_time > 6.0:
            self.active = False

    def draw(self, screen):
        g = pygame.Surface((self.radius * 6, self.radius * 6), pygame.SRCALPHA)
        gg = int(self.radius * 2.5)
        pygame.draw.circle(g, (255, 140, 20, 140), (g.get_width() // 2, g.get_height() // 2), gg)
        screen.blit(g, (int(self.x - g.get_width() // 2), int(self.y - g.get_height() // 2)), special_flags=pygame.BLEND_ADD)
        pygame.draw.circle(screen, ORANGE, (int(self.x), int(self.y)), self.radius)
        pygame.draw.circle(screen, (255, 120, 0), (int(self.x), int(self.y)), self.radius, 2)
        for i in range(3):
            tx = int(self.x - self.vx * (i + 1) * 0.4)
            ty = int(self.y - self.vy * (i + 1) * 0.4)
            ta = int(90 * (1.0 - i * 0.33))
            rr = max(2, int(self.radius * (0.8 - i * 0.2)))
            surf = pygame.Surface((rr * 2, rr * 2), pygame.SRCALPHA)
            pygame.draw.circle(surf, (255, 150, 40, ta), (rr, rr), rr)
            screen.blit(surf, (tx - rr, ty - rr), special_flags=pygame.BLEND_PREMULTIPLIED)

    def get_rect(self):
        return pygame.Rect(int(self.x) - self.radius, int(self.y) - self.radius, self.radius * 2, self.radius * 2)


class Particle:
    """単純な粒子（アイテム取得や被弾エフェクト用）"""

    def __init__(self, x, y, color, life=0.6):
        self.x = x
        self.y = y
        self.vx = random.uniform(-2.5, 2.5)
        self.vy = random.uniform(-3.5, -0.5)
        self.color = color
        self.life = life
        self.created = time.time()
        self.size = random.randint(2, 5)

    def update(self):
        self.vy += 0.12
        self.x += self.vx
        self.y += self.vy

    def draw(self, screen):
        age = time.time() - self.created
        alpha = max(0, 255 - int((age / self.life) * 255))
        surf = pygame.Surface((self.size * 2, self.size * 2), pygame.SRCALPHA)
        pygame.draw.circle(surf, (*self.color[:3], alpha), (self.size, self.size), self.size)
        screen.blit(surf, (int(self.x - self.size), int(self.y - self.size)))

    def is_dead(self):
        return (time.time() - self.created) > self.life


class Player:
    """プレイヤークラス"""

    def __init__(self, image_loader):
        self.x = 100
        self.y = GROUND_Y - PLAYER_SIZE
        self.vel_x = 0
        self.vel_y = 0
        self.is_grounded = True
        self.image_loader = image_loader
        self.collected_items = 0
        self.facing_right = True
        self.max_hp = 5
        self.hp = self.max_hp
        self.dead = False
        self.collapse_start = None
        self.attack_power = 1
        self.recalc_stats()

    def move_right(self):
        self.vel_x = PLAYER_SPEED
        self.facing_right = True

    def move_left(self):
        self.vel_x = -int(PLAYER_SPEED * 1.6)
        self.facing_right = False

    def stop(self):
        self.vel_x *= 0.6
        if abs(self.vel_x) < 0.3:
            self.vel_x = 0

    def jump(self):
        if self.is_grounded and not self.dead:
            self.vel_y = JUMP_FORCE
            self.is_grounded = False

    def update(self):
        if self.dead:
            self.vel_y += GRAVITY
            self.x += self.vel_x * 0.3
            self.y += self.vel_y
            if self.collapse_start and time.time() - self.collapse_start > 2.5:
                self.vel_x = 0
            return

        self.vel_y += GRAVITY
        self.x += self.vel_x
        self.y += self.vel_y

        self.vel_x *= 0.95

        if self.x < 0:
            self.x = 0
            self.vel_x = 0
        if self.x > WINDOW_WIDTH - PLAYER_SIZE:
            self.x = WINDOW_WIDTH - PLAYER_SIZE
            self.vel_x = 0

        if self.y >= GROUND_Y - PLAYER_SIZE:
            self.y = GROUND_Y - PLAYER_SIZE
            self.vel_y = 0
            self.is_grounded = True

    def take_damage(self, amount):
        if self.dead:
            return
        self.hp = max(0, self.hp - amount)
        if self.hp <= 0:
            self.dead = True
            self.collapse_start = time.time()

    def draw(self, screen):
        if self.image_loader.should_use_fallback("player"):
            color = DARK_GRAY if self.dead else GREEN
            pygame.draw.rect(screen, color, (int(self.x), int(self.y), PLAYER_SIZE, PLAYER_SIZE), border_radius=6)
        else:
            img = self.image_loader.get_image("player")
            if img:
                img_to_draw = img
                if self.dead:
                    img_to_draw = img.copy()
                    arr = pygame.Surface(img_to_draw.get_size(), pygame.SRCALPHA)
                    arr.fill((0, 0, 0, 120))
                    img_to_draw.blit(arr, (0, 0), special_flags=pygame.BLEND_RGBA_SUB)
                screen.blit(img_to_draw, (int(self.x), int(self.y)))

    def recalc_stats(self):
        """Collect に応じて最大HPと攻撃力を再計算する"""
        prev_max = getattr(self, "max_hp", 5)
        self.max_hp = 5 + (self.collected_items // 5)
        self.attack_power = 1 + (self.collected_items // 3)
        if self.max_hp > prev_max:
            self.hp = min(self.max_hp, self.hp + (self.max_hp - prev_max))

    def get_rect(self):
        return pygame.Rect(int(self.x), int(self.y), PLAYER_SIZE, PLAYER_SIZE)


class Item:
    """アイテム（記憶の断片）クラス - 空から降るように初期化可能"""

    def __init__(self, x, y, image_loader):
        self.x = x
        self.y = y
        self.radius = 7
        self.image_loader = image_loader
        self.collected = False
        self.vy = 0.0
        self.dropped = True if y >= GROUND_Y - 40 else False

    def update(self):
        if self.collected:
            return
        if not self.dropped:
            self.vy += 0.25
            self.y += self.vy
            if self.y >= GROUND_Y - 16:
                self.y = GROUND_Y - 16
                self.vy = 0.0
                self.dropped = True

    def draw(self, screen):
        if not self.collected:
            if self.image_loader.should_use_fallback("item"):
                pygame.draw.circle(screen, YELLOW, (int(self.x), int(self.y)), self.radius)
                pygame.draw.circle(screen, ORANGE, (int(self.x), int(self.y)), self.radius, 2)
            else:
                img = self.image_loader.get_image("item")
                if img:
                    w, h = img.get_size()
                    screen.blit(img, (int(self.x - w / 2), int(self.y - h / 2)))

    def get_rect(self):
        return pygame.Rect(int(self.x) - self.radius, int(self.y) - self.radius, self.radius * 2, self.radius * 2)


class Boss:
    """Boss (Administrator) class"""

    def __init__(self, image_loader):
        self.x = WINDOW_WIDTH // 2
        self.y = WINDOW_HEIGHT // 2 - 50
        self.radius = 54
        self.hp = 30
        self.max_hp = 30
        self.image_loader = image_loader
        self.vel_x = random.choice([-2, 2])
        self.vel_y = random.choice([-1, 1])
        self.move_timer = time.time()
        self.direction_change_interval = random.uniform(1.0, 3.0)
        self.last_fire_time = time.time()
        self.fire_interval = random.uniform(2.0, 4.0)

    def update(self):
        current_time = time.time()
        if current_time - self.move_timer > self.direction_change_interval:
            self.vel_x = random.uniform(-3, 3)
            self.vel_y = random.uniform(-2, 2)
            self.direction_change_interval = random.uniform(1.0, 3.0)
            self.move_timer = current_time

        self.x += self.vel_x
        self.y += self.vel_y

        if self.x < self.radius + 100:
            self.x = self.radius + 100
            self.vel_x = abs(self.vel_x)
        if self.x > WINDOW_WIDTH - self.radius:
            self.x = WINDOW_WIDTH - self.radius
            self.vel_x = -abs(self.vel_x)
        if self.y < self.radius + 50:
            self.y = self.radius + 50
            self.vel_y = abs(self.vel_y)
        if self.y > GROUND_Y - self.radius - 50:
            self.y = GROUND_Y - self.radius - 50
            self.vel_y = -abs(self.vel_y)

    def draw(self, screen):
        if self.image_loader.should_use_fallback("boss"):
            pygame.draw.circle(screen, RED, (int(self.x), int(self.y)), self.radius)
            pygame.draw.circle(screen, (200, 0, 0), (int(self.x), int(self.y)), self.radius, 4)
        else:
            img = self.image_loader.get_image("boss")
            if img:
                w, h = img.get_size()
                screen.blit(img, (int(self.x - w // 2), int(self.y - h // 2)))


class Lightning:
    """雷エフェクトクラス"""

    def __init__(self, x):
        self.x = x
        self.variant = random.choice(LIGHTNING_VARIANTS)
        self.color = self.variant["color"]
        self.damage_factor = self.variant["factor"]
        self.name = self.variant["name"]
        self.active = True
        self.start_time = time.time()
        self.charge_duration = random.uniform(0.6, 1.4)
        self.phase = "charge"
        self.points = self._generate_zigzag()
        self.strike_point = self.points[-1] if self.points else (self.x, WINDOW_HEIGHT)
        self.intensity = random.uniform(1.0, 2.2)
        self.bolt_start = None

    def _generate_zigzag(self):
        points = [(self.x, 0)]
        y = 0
        while y < WINDOW_HEIGHT:
            y += random.randint(30, 120)
            x_offset = random.randint(-120, 120)
            points.append((self.x + x_offset, min(y, WINDOW_HEIGHT)))
        return points

    def update(self):
        now = time.time()
        if self.phase == "charge":
            if now - self.start_time > self.charge_duration:
                self.phase = "bolt"
                self.bolt_start = now
        elif self.phase == "bolt":
            if now - (self.bolt_start or now) > LIGHTNING_DURATION:
                self.strike_point = self.points[-1] if self.points else (self.x, WINDOW_HEIGHT)
                self.active = False
                self.intensity = min(3.0, self.intensity * 1.2)

    def draw(self, screen):
        if self.phase == "charge":
            charge_t = (time.time() - self.start_time) / max(0.001, self.charge_duration)
            orb_y = max(60, int(min(WINDOW_HEIGHT * 0.4, 60 + charge_t * 220)))
            orb_radius = int(12 + charge_t * 28 * self.intensity)
            surf = pygame.Surface((orb_radius * 2, orb_radius * 2), pygame.SRCALPHA)
            pygame.draw.circle(surf, (*self.color, int(40 + 200 * charge_t)), (orb_radius, orb_radius), orb_radius)
            screen.blit(surf, (int(self.x - orb_radius), int(orb_y - orb_radius)))
            for _ in range(6):
                if random.random() < charge_t:
                    sx = int(self.x + random.randint(-40, 40))
                    sy = int(orb_y + random.randint(-20, 20))
                    pygame.draw.circle(screen, WHITE, (sx, sy), 2)
        elif self.phase == "bolt" and len(self.points) > 1:
            for i in range(len(self.points) - 1):
                p1 = self.points[i]
                p2 = self.points[i + 1]
                thickness = random.choice([5, 6, 8])
                pygame.draw.line(screen, self.color, p1, p2, thickness)
                if random.random() < 0.5:
                    sx = (p1[0] + p2[0]) // 2 + random.randint(-20, 20)
                    sy = (p1[1] + p2[1]) // 2 + random.randint(-20, 20)
                    pygame.draw.circle(screen, WHITE, (sx, sy), 4)
                if random.random() < 0.35:
                    bx = (p1[0] + p2[0]) // 2 + random.randint(-50, 50)
                    by = (p1[1] + p2[1]) // 2 + random.randint(-50, 50)
                    pygame.draw.line(screen, self.color, (bx, by), (bx + random.randint(-30, 30), by + random.randint(10, 90)), 2)
            strike_x = int(self.points[-1][0]) if self.points else int(self.x)
            prog = min(1.0, max(0.0, (time.time() - (self.bolt_start or time.time())) / max(0.001, LIGHTNING_DURATION)))
            glow_alpha = int(180 * (1.0 - prog))
            glow_r = int(120 * (0.8 + self.intensity * 0.2))
            glow = pygame.Surface((glow_r * 2, 80), pygame.SRCALPHA)
            gc = tuple(min(255, int(self.color[i] * 0.6 + 200 * 0.4)) for i in range(3))
            pygame.draw.ellipse(glow, (*gc, glow_alpha), (0, 0, glow_r * 2, 80))
            screen.blit(glow, (strike_x - glow_r, GROUND_Y - 40), special_flags=pygame.BLEND_ADD)


class BurningZone:
    """燃えるゾーン（雷が落ちた後、またはボスの破壊で発生）"""

    def __init__(self, x, y, width=160, duration=8.0):
        self.x = max(0, min(WINDOW_WIDTH - width, int(x - width // 2)))
        self.y = y
        self.width = width
        self.duration = duration
        self.start = time.time()
        self.active = True

    def update(self):
        if time.time() - self.start > self.duration:
            self.active = False

    def draw(self, surface):
        age = (time.time() - self.start) / self.duration
        alpha = int(max(0, 180 * (1.0 - age)))
        surf = pygame.Surface((self.width, WINDOW_HEIGHT - self.y), pygame.SRCALPHA)
        color = (255, 100, 20, alpha)
        surf.fill(color)
        surface.blit(surf, (self.x, self.y))


class Bomb:
    """落下する爆弾。着地で爆発し燃焼ゾーンを作る"""

    def __init__(self, x):
        self.x = x
        self.y = -40
        self.vy = random.uniform(8.0, 14.0)
        self.active = True
        self.exploded = False
        self.spawn = time.time()
        self.intensity = random.uniform(0.9, 1.8)

    def update(self):
        if not self.active:
            return
        self.y += self.vy
        self.vy += 0.6
        if self.y >= GROUND_Y - 10:
            self.explode()

    def explode(self):
        if self.exploded:
            return
        self.exploded = True
        self.active = False

    def draw(self, screen):
        if self.active:
            pygame.draw.circle(screen, (80, 80, 80), (int(self.x), int(self.y)), 12)
            pygame.draw.circle(screen, (180, 60, 60), (int(self.x), int(self.y)), 6)


class Firework:
    """花火: 打ち上げてから炸裂する簡易花火エフェクト"""

    def __init__(self, x, base_y):
        self.x = x
        self.y = base_y
        self.vy = random.uniform(-12.0, -8.0)
        self.active = True
        self.phase = "ascend"
        self.particles = []
        self.created = time.time()

    def update(self):
        if self.phase == "ascend":
            self.y += self.vy
            self.vy += 0.5
            if self.vy > -2.5:
                self.phase = "burst"
                count = random.randint(20, 40)
                for _ in range(count):
                    angle = random.uniform(0, math.pi * 2)
                    speed = random.uniform(2.5, 7.0)
                    pv = {
                        "x": self.x,
                        "y": self.y,
                        "vx": math.cos(angle) * speed,
                        "vy": math.sin(angle) * speed,
                        "life": random.uniform(0.9, 1.8),
                        "created": time.time(),
                        "color": (random.randint(200, 255), random.randint(100, 255), random.randint(50, 255))
                    }
                    self.particles.append(pv)
        elif self.phase == "burst":
            alive = []
            for p in self.particles:
                age = time.time() - p["created"]
                if age < p["life"]:
                    p["vx"] *= 0.995
                    p["vy"] += 0.12
                    p["x"] += p["vx"]
                    p["y"] += p["vy"]
                    alive.append(p)
            self.particles = alive
            if not self.particles:
                self.active = False

    def draw(self, surface):
        if self.phase == "ascend":
            pygame.draw.circle(surface, WHITE, (int(self.x), int(self.y)), 3)
        else:
            for p in self.particles:
                age = time.time() - p["created"]
                alpha = max(0, 255 - int((age / p["life"]) * 255))
                surf = pygame.Surface((6, 6), pygame.SRCALPHA)
                surf.fill((*p["color"], alpha))
                surface.blit(surf, (int(p["x"]), int(p["y"])))


class MagicCircle:
    """簡易的な魔法陣エフェクト（回転するリング）"""

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = 48
        self.angle = 0.0
        self.created = time.time()

    def update(self):
        self.angle += 0.08

    def draw(self, surface):
        r = int(self.radius + math.sin(time.time() - self.created) * 6)
        for i in range(4):
            a = self.angle + i * math.pi / 2
            ox = int(math.cos(a) * r)
            oy = int(math.sin(a) * r)
            pygame.draw.circle(surface, PURPLE, (int(self.x + ox), int(self.y + oy)), 6, 2)
        for i in range(6):
            a = self.angle + i * (math.pi * 2 / 6)
            sx = int(self.x + math.cos(a) * (r - 12))
            sy = int(self.y + math.sin(a) * (r - 12))
            ex = int(self.x + math.cos(a + 0.3) * (r - 4))
            ey = int(self.y + math.sin(a + 0.3) * (r - 4))
            pygame.draw.line(surface, WHITE, (sx, sy), (ex, ey), 2)


class InputHandler:
    """Enterキーの入力判定ロジック（短押し/長押し/ダブルタップ）"""

    def __init__(self):
        self.key_down_time = 0
        self.key_up_time = 0
        self.is_pressing = False
        self.press_duration = 0
        self.last_tap_time = 0
        self.short_press_detected = False
        self.long_press_detected = False
        self.double_tap_detected = False
        self.is_holding = False

    def on_key_down(self):
        current_time = time.time()
        if not self.is_pressing:
            time_since_last_tap = current_time - self.key_up_time
            if time_since_last_tap < DOUBLE_TAP_THRESHOLD and self.key_up_time > 0:
                self.double_tap_detected = True
            self.key_down_time = current_time
            self.is_pressing = True
            self.is_holding = False

    def on_key_up(self):
        current_time = time.time()
        if self.is_pressing:
            self.press_duration = current_time - self.key_down_time
            self.key_up_time = current_time
            self.is_pressing = False
            self.is_holding = False
            if self.press_duration < SHORT_PRESS_THRESHOLD:
                self.short_press_detected = True
            elif self.press_duration > LONG_PRESS_THRESHOLD:
                self.long_press_detected = True

    def update(self):
        if self.is_pressing:
            current_time = time.time()
            self.press_duration = current_time - self.key_down_time
            if self.press_duration > LONG_PRESS_THRESHOLD:
                self.is_holding = True

    def consume_short_press(self):
        if self.short_press_detected:
            self.short_press_detected = False
            return True
        return False

    def consume_long_press(self):
        if self.long_press_detected:
            self.long_press_detected = False
            return True
        return False

    def consume_double_tap(self):
        if self.double_tap_detected:
            self.double_tap_detected = False
            return True
        return False

    def reset(self):
        self.short_press_detected = False
        self.long_press_detected = False
        self.double_tap_detected = False


class Game:
    """メインゲームクラス"""

    def __init__(self):
        pygame.init()
        try:
            pygame.mixer.init()
            pygame.mixer.set_num_channels(32)
        except Exception:
            pass
 
        pygame.display.set_caption(GAME_TITLE)
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True

# 英字用（保険）
        self.font_large = pygame.font.Font(None, 72)
        self.font_medium = pygame.font.Font(None, 40)
        self.font_small = pygame.font.Font(None, 28)

# 日本語用（配布先でも確実に動く：同梱フォントを直接読む）
        if JP_FONT_PATH and JP_FONT_PATH.exists():
           self.font_jp = pygame.font.Font(str(JP_FONT_PATH), 28)
           self.font_jp_large = pygame.font.Font(str(JP_FONT_PATH), 44)
           self.font_title = pygame.font.Font(str(JP_FONT_PATH), 72)   # タイトル用（必要ならサイズ調整）
        else:
    # フォントが見つからない場合のフォールバック（この場合は豆腐になる可能性あり）
           self.font_jp = self.font_small
           self.font_jp_large = self.font_medium
           self.font_title = self.font_large


        self.image_loader = ImageLoader()
        self.image_loader.load_image("player", PLAYER_IMG_PATH, (PLAYER_SIZE, PLAYER_SIZE))
        self.image_loader.load_image("boss", BOSS_IMG_PATH, (140, 140))
        self.image_loader.load_image("item", ITEM_IMG_PATH, (60, 60))

        self.input_handler = InputHandler()

        self.state = TITLE_SCREEN
        self.timer = COLLECT_PHASE_TIME
        self.timer_start = 0

        self.player = None
        self.boss = None
        self.items = []
        self.lightnings = []
        self.last_lightning_time = 0

        self.skill_options = ["MAGIMAGICA", "ONE ON ONE", "GUN"]
        self.skill_highlight_index = 0
        self.skill_highlight_timer = 0
        self.selected_skill = None
        self.magic_circle = None
        self.countdown_value = None
        self.countdown_start = 0

        self.fireballs = []
        self.player_projectiles = []
        self.particles = []

        self.burning_zones = []
        self.fireworks = []
        self.recent_strikes = []

        self.screen_shake_timer = 0
        self.screen_shake_magnitude = 0

        self.skill_armed = False
        self.skill_arm_time = 0.0

        self.clear_start = 0
        self.clear_brightness = 0.0
        self.score = 0
        self.last_score = 0
        self.bombs = []
        self.last_bomb_time = 0
        self.abyss_start = None

        self.enter_sound = None
        self.enter_channel = None
        self.boss_sfx = None
        self.boss_channel = None
        
        try:
            if pygame.mixer.get_init() is None:
                try:
                    pygame.mixer.init()
                except Exception:
                    pass
            if os.path.exists(BGM_PATH):
                try:
                    pygame.mixer.music.load(BGM_PATH)
                    pygame.mixer.music.set_volume(0.6)
                    pygame.mixer.music.play(-1)
                except Exception:
                    pass
            if os.path.exists(ENTER_SFX_PATH):
                try:
                    self.enter_sound = pygame.mixer.Sound(ENTER_SFX_PATH)
                    try:
                        self.enter_channel = pygame.mixer.Channel(6)
                    except Exception:
                        self.enter_channel = None
                except Exception:
                    self.enter_sound = None
                    self.enter_channel = None
            if os.path.exists(BOSS_SFX_PATH):
                try:
                    self.boss_sfx = pygame.mixer.Sound(BOSS_SFX_PATH)
                    try:
                        self.boss_channel = pygame.mixer.Channel(7)
                    except Exception:
                        self.boss_channel = None
                except Exception:
                    self.boss_sfx = None
                    self.boss_channel = None
        except Exception:
            self.enter_sound = None
            self.enter_channel = None
            self.boss_sfx = None
            self.boss_channel = None

    def _play_boss_attack_sfx(self):
        if not self.boss_sfx:
            return
        try:
            if self.boss_channel:
                if self.boss_channel.get_busy():
                    self.boss_channel.stop()
                self.boss_channel.play(self.boss_sfx)
            else:
                self.boss_sfx.play()
        except Exception:
            pass

    def reset_game(self):
        self.player = Player(self.image_loader)
        self.boss = Boss(self.image_loader)
        self.items = []
        self.lightnings = []
        self.timer = COLLECT_PHASE_TIME
        self.timer_start = time.time()
        self.last_lightning_time = time.time()
        self.selected_skill = None
        self.magic_circle = None
        self.countdown_value = None
        self.fireballs = []
        self.player_projectiles = []
        self.particles = []

        self.burning_zones = []
        self.fireworks = []
        self.score = 0
        self.bombs = []
        self.last_bomb_time = time.time()
        self.abyss_start = None

        self.skill_armed = False
        self.skill_arm_time = 0.0

        self.screen_shake_timer = 0
        self.screen_shake_magnitude = 0

        attempts = 0
        placed = 0
        target_count = 18
        min_sep = 48
        xs = []
        while placed < target_count and attempts < 2000:
            attempts += 1
            x = random.randint(120, WINDOW_WIDTH - 120)
            ok = True
            for ox in xs:
                if abs(ox - x) < min_sep:
                    ok = False
                    break
            if not ok:
                continue
            y = random.randint(-600, -80)
            self.items.append(Item(x, y, self.image_loader))
            xs.append(x)
            placed += 1
    
    def go_to_title(self):
        # 入力の残りを完全に無効化
        self.input_handler.reset()
        self.input_handler.is_pressing = False

        # 演出・残留物を全消し
        self.screen_shake_timer = 0
        self.screen_shake_magnitude = 0
        self.clear_brightness = 0.0
        self.clear_start = 0

        self.fireworks = []
        self.particles = []
        self.burning_zones = []
        self.lightnings = []
        self.bombs = []
        self.fireballs = []
        self.player_projectiles = []
        self.recent_strikes = []

        # 状態関連の残りを消す
        for attr in ("clear_to_score_time", "over_to_score_time", "clear_anim_start", "clear_wait_start"):
            if hasattr(self, attr):
                delattr(self, attr)

        self.abyss_start = None
        self.magic_circle = None
        self.selected_skill = None
        self.skill_armed = False

        # タイトルではゲームオブジェクトを持たない（残骸による誤判定防止）
        self.player = None
        self.boss = None
        self.items = []


        # タイトルへ
        self.state = TITLE_SCREEN


    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.input_handler.on_key_down()

                    # Enter効果音（必要なら）
                    if self.enter_sound:
                        try:
                            if self.enter_channel:
                                if self.enter_channel.get_busy():
                                    self.enter_channel.stop()
                                self.enter_channel.play(self.enter_sound)
                            else:
                                self.enter_sound.play()
                        except Exception:
                            pass

                elif event.key == pygame.K_r:
                    if self.state == GAME_CLEAR:
                        self.go_to_title()
                    elif self.state in (GAME_OVER, SCORE_SCREEN):
                        # リトライ：即ゲームを作り直して回収パートへ
                        self.input_handler.reset()
                        self.input_handler.is_pressing = False
                        self.reset_game()
                        self.state = COLLECT_PHASE

                elif event.key == pygame.K_ESCAPE:
                    self.running = False

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_RETURN:
                    self.input_handler.on_key_up()





#    def open_image_picker(self):
        """タイトル画面での長押しにより画像選択ダイアログを開く"""
#        changed = False
#        changed |= self.image_loader.set_image_from_dialog("player", (PLAYER_SIZE, PLAYER_SIZE))
#        changed |= self.image_loader.set_image_from_dialog("boss", (140, 140))
#        changed |= self.image_loader.set_image_from_dialog("item", (20, 20))
#        if changed:
#            print("選択した画像を読み込みました。")

    def spawn_basic_shot(self):
        """素早い通常射（弱めの弾）を生成"""
        if not self.player or not self.boss:
            return
        mp = MagicProjectile(
            self.player.x + PLAYER_SIZE / 2,
            self.player.y + PLAYER_SIZE / 2,
            self.boss.x + random.uniform(-10, 10),
            self.boss.y + random.uniform(-10, 10),
            speed=11,
            damage=getattr(self.player, "attack_power", 1),
            color=(160, 220, 255)
        )
        for _ in range(6):
            self.particles.append(Particle(mp.x + random.uniform(-6, 6), mp.y + random.uniform(-6, 6), (200, 230, 255), life=0.4))
        self.player_projectiles.append(mp)

    def process_lightnings(self):
        """Update all lightnings, create burning zones and strike effects on completion."""
        if not self.lightnings:
            return
        new_lightnings = []
        now = time.time()
        for lightning in self.lightnings:
            lightning.update()
            if not lightning.active:
                strike_x, strike_y = lightning.strike_point
                dur = max(6.0, 8.0 * lightning.intensity)
                self.burning_zones.append(BurningZone(strike_x, strike_y, width=int(220 * lightning.intensity), duration=dur))
                if self.player and not self.player.dead:
                    player_rect = self.player.get_rect()
                    zone_rect = pygame.Rect(strike_x - int(120 * lightning.intensity), strike_y - int(120 * lightning.intensity), int(240 * lightning.intensity), int(240 * lightning.intensity))
                    if player_rect.colliderect(zone_rect):
                        base = 1
                        dmg = max(1, int(round(base * lightning.damage_factor * (0.8 + lightning.intensity * 0.4))))
                        self.player.take_damage(dmg)
                for _ in range(30 + int(30 * lightning.intensity)):
                    self.particles.append(Particle(strike_x + random.uniform(-80, 80), strike_y + random.uniform(-40, 40), ORANGE, life=random.uniform(0.8, 1.8)))
                self.recent_strikes.append((now, lightning.intensity, strike_x, strike_y))
            else:
                new_lightnings.append(lightning)
        self.lightnings = new_lightnings

    def process_bombs(self):
        now = time.time()
        if now - self.last_bomb_time > 8.0 + random.random() * 12.0:
            bx = random.randint(60, WINDOW_WIDTH - 60)
            self.bombs.append(Bomb(bx))
            self.last_bomb_time = now

        new_bombs = []
        for b in self.bombs:
            b.update()
            if b.exploded:
                sx = int(b.x)
                sy = GROUND_Y
                dur = 5.0 * b.intensity
                self.burning_zones.append(BurningZone(sx, sy, width=int(180 * b.intensity), duration=dur))
                if self.player and not self.player.dead:
                    pr = self.player.get_rect()
                    zone_rect = pygame.Rect(sx - int(100 * b.intensity), sy - int(100 * b.intensity), int(200 * b.intensity), int(200 * b.intensity))
                    if pr.colliderect(zone_rect):
                        self.player.take_damage(int(1 + 3 * b.intensity))
                for _ in range(20 + int(20 * b.intensity)):
                    self.particles.append(Particle(sx + random.uniform(-80, 80), sy + random.uniform(-20, 20), ORANGE, life=random.uniform(0.8, 1.6)))
            else:
                new_bombs.append(b)
        self.bombs = new_bombs

    def update(self):
        self.input_handler.update()
        self.process_lightnings()
        self.process_bombs()

        if self.player and self.player.hp <= 0 and self.state in (COLLECT_PHASE, BOSS_PHASE):
            self.last_score = self.score
            self.state = SCORE_SCREEN
            return

        if self.state == GAME_CLEAR_ANIM:
            try:
                if hasattr(self, 'boss') and self.boss:
                    self.boss.y += self.boss_fall_vy
                    self.boss_fall_vy += 0.9
                    if random.random() < 0.25:
                        self.particles.append(Particle(self.boss.x + random.uniform(-30, 30), self.boss.y + random.uniform(-20, 20), (200, 160, 40), life=0.9))
                    if self.boss.y >= GROUND_Y - self.boss.radius:
                        if not getattr(self, 'clear_exploded', False):
                            sx = int(self.boss.x)
                            sy = int(GROUND_Y)
                            for _ in range(180):
                                self.particles.append(Particle(sx + random.uniform(-180, 180), sy + random.uniform(-80, 80), random.choice([YELLOW, RED, ORANGE]), life=random.uniform(0.8, 2.0)))
                            for _ in range(12):
                                fx = random.randint(200, WINDOW_WIDTH - 200)
                                self.fireworks.append(Firework(fx, WINDOW_HEIGHT // 2))
                            self.clear_brightness = 1.0
                            self.clear_start = time.time()
                            self.screen_shake_timer = time.time()
                            self.screen_shake_magnitude = 36
                            self.clear_exploded = True
                            self.clear_to_score_time = time.time() + 2.0
                else:
                    self.state = GAME_CLEAR
            except Exception:
                traceback.print_exc()
                self.state = GAME_CLEAR

        if self.state == GAME_CLEAR_ANIM and hasattr(self, 'clear_to_score_time') and time.time() > getattr(self, 'clear_to_score_time', 0):
            self.state = GAME_CLEAR
            self.clear_start = time.time()
            self.clear_brightness = 1.0

        if self.state == GAME_OVER and hasattr(self, 'over_to_score_time') and time.time() > getattr(self, 'over_to_score_time', 0):
            self.last_score = self.score
            self.state = SCORE_SCREEN

        #if self.state == SCORE_SCREEN:
            #if self.input_handler.consume_short_press():
            #    self.state = TITLE_SCREEN
            #    try:
            #        self.reset_game()
            #    except Exception:
            #        traceback.print_exc()
            # return

        if self.state == TITLE_SCREEN:
            self.update_title_screen()
        elif self.state == COLLECT_PHASE:
            self.update_collect_phase()
        elif self.state == BOSS_PHASE:
            self.update_boss_phase()
        elif self.state == GAME_CLEAR or self.state == GAME_OVER:
            self.update_end_state()

    def update_title_screen(self):
    # 長押しでの画像選択は一旦無効化
    # if self.input_handler.consume_long_press():
    #     self.open_image_picker()

        if self.input_handler.consume_short_press():
           self.reset_game()
           self.state = COLLECT_PHASE


    def update_collect_phase(self):
        elapsed = time.time() - self.timer_start
        self.timer = max(0, COLLECT_PHASE_TIME - int(elapsed))

        if self.timer <= 0:
            self.state = BOSS_PHASE
            self.skill_highlight_timer = time.time()
            return

        if self.input_handler.consume_double_tap():
            self.player.move_left()
        if self.input_handler.consume_short_press():
            self.player.move_right()
        if self.input_handler.consume_long_press() or self.input_handler.is_holding:
            self.player.jump()

        for item in self.items:
            item.update()

        self.player.update()
        if self.player.hp <= 0:
            self.last_score = self.score
            self.state = SCORE_SCREEN
            return

        player_rect = self.player.get_rect()
        for item in self.items:
            if not item.collected and player_rect.colliderect(item.get_rect()):
                item.collected = True
                self.player.collected_items += 1
                if self.player:
                    self.player.recalc_stats()
                self.score += 100
                for _ in range(12):
                    self.particles.append(Particle(item.x, item.y, YELLOW, life=0.7))

        current_time = time.time()
        if current_time - self.last_lightning_time > LIGHTNING_INTERVAL:
            x = random.randint(50, WINDOW_WIDTH - 50)
            self.lightnings.append(Lightning(x))
            self.last_lightning_time = current_time

        for proj in self.player_projectiles:
            proj.update()
        self.player_projectiles = [p for p in self.player_projectiles if p.active]

        if self.input_handler.consume_double_tap():
            self.spawn_basic_shot()

        for p in self.particles:
            p.update()
        self.particles = [p for p in self.particles if not p.is_dead()]

        for zone in self.burning_zones:
            zone.update()
            if zone.active and self.player and not self.player.dead:
                player_rect = self.player.get_rect()
                zone_rect = pygame.Rect(zone.x, zone.y, zone.width, WINDOW_HEIGHT - zone.y)
                if player_rect.colliderect(zone_rect):
                    self.player.take_damage(1 if random.random() < 0.02 else 0)
                    if self.player.hp <= 0:
                        self.trigger_game_over()
        self.burning_zones = [z for z in self.burning_zones if z.active]

    def update_boss_phase(self):
        current_time = time.time()

        if self.player and self.player.dead:
            pass

        self.boss.update()

        if current_time - self.boss.last_fire_time > self.boss.fire_interval:
            self.boss.last_fire_time = current_time
            self.boss.fire_interval = random.uniform(1.2, 3.0)
            self._play_boss_attack_sfx()
            choice = random.random()
            if choice < 0.5:
                if self.player:
                    fb = Fireball(self.boss.x, self.boss.y, self.player.x + PLAYER_SIZE / 2, self.player.y + PLAYER_SIZE / 2, speed=random.uniform(4.5, 7.0))
                    self.fireballs.append(fb)
            elif choice < 0.85:
                if self.player:
                    for i in range(5):
                        offset_x = (i - 2) * 40
                        tx = self.player.x + PLAYER_SIZE / 2 + offset_x + random.uniform(-20, 20)
                        ty = self.player.y + PLAYER_SIZE / 2 + random.uniform(-20, 20)
                        fb = Fireball(self.boss.x, self.boss.y, tx, ty, speed=random.uniform(5.0, 7.5))
                        self.fireballs.append(fb)
            else:
                if self.player:
                    sx = int(self.player.x + PLAYER_SIZE / 2)
                    sy = GROUND_Y - random.randint(20, 60)
                    dur = random.uniform(4.0, 9.0)
                    self.burning_zones.append(BurningZone(sx, sy, width=random.randint(120, 260), duration=dur))
                    for _ in range(16):
                        self.particles.append(Particle(sx + random.uniform(-40, 40), sy + random.uniform(-20, 20), ORANGE, life=0.9))

        if self.selected_skill is None:
            if current_time - self.skill_highlight_timer > 0.5:
                self.skill_highlight_index = (self.skill_highlight_index + 1) % len(self.skill_options)
                self.skill_highlight_timer = current_time

            if self.input_handler.consume_short_press():
                self.selected_skill = self.skill_options[self.skill_highlight_index]
                self.skill_armed = True
                self.skill_arm_time = current_time
                if self.selected_skill == "Tama wo Tobasu":
                    self.countdown_value = 3
                    self.countdown_start = current_time
        else:
            if self.input_handler.consume_double_tap():
                self.spawn_basic_shot()

            if self.skill_armed and self.input_handler.consume_short_press():
                self.on_skill_selected()
                self.skill_armed = False
                self.selected_skill = None

            if self.selected_skill == "Mahou Kougeki" and self.magic_circle:
                self.magic_circle.update()
            elif self.selected_skill == "Tama wo Tobasu" and self.countdown_value is not None:
                elapsed = current_time - self.countdown_start
                if elapsed < 1:
                    self.countdown_value = 3
                elif elapsed < 2:
                    self.countdown_value = 2
                elif elapsed < 3:
                    self.countdown_value = 1
                elif elapsed < 4:
                    self.countdown_value = "GO!"
                else:
                    if self.countdown_value is not None:
                        self.spawn_tama_orbs()
                    self.countdown_value = None
                    self.selected_skill = None
                    self.skill_armed = False

        for fb in self.fireballs:
            fb.update()
            if fb.active and self.player and fb.get_rect().colliderect(self.player.get_rect()):
                fb.active = False
                self.player.x = max(0, self.player.x - 120)
                self.player.vel_x = -6
                self.player.take_damage(1)
                if self.player.hp <= 0:
                    self.trigger_game_over()
                if self.player.collected_items > 0:
                    self.player.collected_items = max(0, self.player.collected_items - 1)
                for _ in range(22):
                    self.particles.append(Particle(self.player.x + PLAYER_SIZE / 2, self.player.y + PLAYER_SIZE / 2, ORANGE, life=0.9))
                self.screen_shake_timer = time.time()
                self.screen_shake_magnitude = 10

        self.fireballs = [f for f in self.fireballs if f.active]

        for proj in self.player_projectiles:
            proj.update()
            if proj.active:
                boss_rect = pygame.Rect(int(self.boss.x - self.boss.radius), int(self.boss.y - self.boss.radius), self.boss.radius * 2, self.boss.radius * 2)
                if proj.get_rect().colliderect(boss_rect):
                    proj.active = False
                    damage = getattr(proj, "damage", 1)
                    self.boss.hp = max(0, self.boss.hp - damage)
                    self.score += 50 * int(damage)
                    for _ in range(18 + int(damage * 6)):
                        col = random.choice([YELLOW, ORANGE, RED])
                        self.particles.append(Particle(self.boss.x + random.uniform(-40, 40), self.boss.y + random.uniform(-40, 40), col, life=random.uniform(0.8, 1.6)))
                    ring = pygame.Surface((300, 300), pygame.SRCALPHA)
                    pygame.draw.circle(ring, (255, 200, 120, 40), (150, 150), 120)
                    self.screen.blit(ring, (int(self.boss.x - 150), int(self.boss.y - 150)), special_flags=pygame.BLEND_ADD)
                    self.screen_shake_timer = time.time()
                    self.screen_shake_magnitude = min(40, self.screen_shake_magnitude + 6)

        self.player_projectiles = [p for p in self.player_projectiles if p.active]

        for p in self.particles:
            p.update()
        self.particles = [p for p in self.particles if not p.is_dead()]

        for zone in self.burning_zones:
            zone.update()
            if zone.active and self.player and not self.player.dead:
                player_rect = self.player.get_rect()
                zone_rect = pygame.Rect(zone.x, zone.y, zone.width, WINDOW_HEIGHT - zone.y)
                if player_rect.colliderect(zone_rect):
                    if random.random() < 0.04:
                        self.player.take_damage(1)
                    if self.player.hp <= 0:
                        self.trigger_game_over()
        self.burning_zones = [z for z in self.burning_zones if z.active]

        if time.time() - self.screen_shake_timer > 0.5:
            self.screen_shake_magnitude = max(0, self.screen_shake_magnitude - 0.5)

        if self.boss.hp <= 0:
            self.trigger_game_clear()

    def trigger_game_clear(self):
        if not hasattr(self, 'boss') or not self.boss:
            self.state = GAME_CLEAR_ANIM
            self.input_handler.reset()    # 追加：連打の残りを消す
            self.clear_brightness = 1.0
            self.clear_start = time.time()
            self.clear_wait_start = time.time()
            return
        self.clear_anim_start = time.time()
        self.clear_exploded = False
        self.boss_fall_vy = 2.0
        self.state = GAME_CLEAR_ANIM
        for _ in range(24):
            self.particles.append(Particle(self.boss.x + random.uniform(-40, 40), self.boss.y + random.uniform(-40, 40), YELLOW, life=random.uniform(0.6, 1.2)))

    def trigger_game_over(self):
        self.last_score = self.score
        self.abyss_start = time.time()
        for _ in range(8):
            x = random.randint(100, WINDOW_WIDTH - 200)
            y = GROUND_Y - random.randint(40, 10)
            dur = random.uniform(6.0, 12.0)
            self.burning_zones.append(BurningZone(x, y, width=random.randint(120, 320), duration=dur))
        for _ in range(80):
            self.particles.append(Particle(random.randint(50, WINDOW_WIDTH - 50), random.randint(50, GROUND_Y - 20), ORANGE, life=random.uniform(0.8, 1.8)))
        self.state = GAME_OVER
        self.over_to_score_time = time.time() + 3.5
        self.screen_shake_timer = time.time()
        self.screen_shake_magnitude = 22

    def on_skill_selected(self):
        if self.selected_skill == "Mahou Kougeki":
            self.magic_circle = MagicCircle(self.player.x + PLAYER_SIZE // 2, self.player.y + PLAYER_SIZE)
            mp = MagicProjectile(self.player.x + PLAYER_SIZE / 2, self.player.y + PLAYER_SIZE / 2, self.boss.x, self.boss.y, speed=10, damage=getattr(self.player, "attack_power", 1) + 1, color=(255, 220, 140))
            for _ in range(24):
                self.particles.append(Particle(mp.x + random.uniform(-12, 12), mp.y + random.uniform(-12, 12), (255, 200, 120), life=0.9))
            self.player_projectiles.append(mp)
        elif self.selected_skill == "Tama wo Tobasu":
            pass
        elif self.selected_skill == "Ikkiuchi":
            self.boss.hp = max(0, self.boss.hp - 2)
            for _ in range(30):
                self.particles.append(Particle(self.boss.x, self.boss.y, RED, life=1.0))
            self.screen_shake_timer = time.time()
            self.screen_shake_magnitude = 12

    def spawn_tama_orbs(self):
        """Tama wo Tobasu の発射処理（カウント終了後に複数弾をボスへ）"""
        for _ in range(8):
            orb = Orb(self.player.x + PLAYER_SIZE / 2, self.player.y + PLAYER_SIZE / 2, self.boss.x + random.uniform(-20, 20), self.boss.y + random.uniform(-20, 20), speed=random.uniform(5.5, 8.0), damage=getattr(self.player, "attack_power", 1))
            for _ in range(4):
                self.particles.append(Particle(orb.x + random.uniform(-6, 6), orb.y + random.uniform(-6, 6), (220, 180, 255), life=0.5))
            self.player_projectiles.append(orb)

    def update_end_state(self):
        for fw in self.fireworks:
            fw.update()
        self.fireworks = [f for f in self.fireworks if f.active]

        for p in self.particles:
            p.update()
        self.particles = [p for p in self.particles if not p.is_dead()]

        for zone in self.burning_zones:
            zone.update()
        self.burning_zones = [z for z in self.burning_zones if z.active]

        if self.state == GAME_CLEAR:
            t = time.time() - self.clear_start
            self.clear_brightness = max(0.0, 1.0 - (t / 4.0))
            if random.random() < 0.02:
                fx = random.randint(200, WINDOW_WIDTH - 200)
                self.fireworks.append(Firework(fx, WINDOW_HEIGHT // 2))

    def draw(self):
        shake_x = shake_y = 0
        if self.screen_shake_magnitude > 0:
            shake_x = random.randint(-int(self.screen_shake_magnitude), int(self.screen_shake_magnitude))
            shake_y = random.randint(-int(self.screen_shake_magnitude), int(self.screen_shake_magnitude))

        self.screen.fill(DARK_GRAY)
        temp = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        temp.fill(DARK_GRAY)

        if self.state == TITLE_SCREEN:
            self.draw_title_screen(temp)
        elif self.state == COLLECT_PHASE:
            self.draw_collect_phase(temp)
        elif self.state == BOSS_PHASE or self.state == GAME_CLEAR_ANIM:
            if self.boss:
                self.draw_boss_phase(temp)
            else:
                self.draw_collect_phase(temp)
        elif self.state == GAME_CLEAR:
            if self.boss:
                self.draw_boss_phase(temp)
            else:
                self.draw_collect_phase(temp)
        elif self.state == GAME_OVER:
            if self.boss:
                self.draw_boss_phase(temp)
            else:
                self.draw_collect_phase(temp)

        for zone in self.burning_zones:
            zone.draw(temp)

        for proj in self.player_projectiles:
            proj.draw(temp)
        for b in self.bombs:
            b.draw(temp)
        for p in self.particles:
            p.draw(temp)
        for fb in self.fireballs:
            fb.draw(temp)
        for lightning in self.lightnings:
            lightning.draw(temp)

        for fw in self.fireworks:
            fw.draw(temp)

        if self.state == GAME_CLEAR and self.clear_brightness > 0:
            overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
            alpha = int(180 * self.clear_brightness)
            overlay.fill((255, 255, 220, alpha))
            temp.blit(overlay, (0, 0))

        now = time.time()
        new_recent = []
        for (tstr, intensity, sx, sy) in getattr(self, 'recent_strikes', []):
            age = now - tstr
            if age < 0.45:
                fade = 1.0 - (age / 0.45)
                alpha = int(min(220, 220 * intensity * fade))
                flash = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
                flash.fill((255, 255, 240, alpha))
                temp.blit(flash, (0, 0))
                rr = int(120 * intensity * (0.8 + 0.4 * fade))
                glow = pygame.Surface((rr * 2, rr * 2), pygame.SRCALPHA)
                pygame.draw.circle(glow, (255, 220, 140, int(alpha * 0.8)), (rr, rr), rr)
                temp.blit(glow, (int(sx - rr), int(sy - rr)), special_flags=pygame.BLEND_ADD)
                new_recent.append((tstr, intensity, sx, sy))
        self.recent_strikes = new_recent

        if self.state == GAME_OVER and self.abyss_start:
            t = now - self.abyss_start
            prog = min(1.0, t / 6.0)
            alpha = int(180 * prog)
            abyss = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
            abyss.fill((8, 4, 20, alpha))
            rr = int(300 + prog * 800)
            glow = pygame.Surface((rr * 2, rr * 2), pygame.SRCALPHA)
            gcol = int(120 * (1.0 - prog))
            pygame.draw.circle(glow, (0, 0, 0, int(200 * prog)), (rr, rr), rr)
            abyss.blit(glow, (WINDOW_WIDTH // 2 - rr, WINDOW_HEIGHT // 2 - rr), special_flags=pygame.BLEND_RGBA_SUB)
            temp.blit(abyss, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
            if random.random() < 0.08 + prog * 0.12:
                px = random.randint(0, WINDOW_WIDTH)
                py = random.randint(0, WINDOW_HEIGHT)
                self.particles.append(Particle(px, py, (30, 0, 60), life=2.0))

        self.screen.blit(temp, (shake_x, shake_y))

        self.draw_overlay(self.screen)

        pygame.display.flip()

    def draw_overlay(self, surface):
        if self.state == COLLECT_PHASE:
            timer_text = self.font_large.render(f"Time: {self.timer}", True, WHITE)
            surface.blit(timer_text, (WINDOW_WIDTH // 2 - 140, 30))

        items_text = self.font_small.render(f"Items: {self.player.collected_items if self.player else 0}", True, WHITE)
        surface.blit(items_text, (30, 30))

        if self.player:
            bar_x = 30
            bar_y = 70
            bar_w = 260
            bar_h = 24
            pygame.draw.rect(surface, DARK_GRAY, (bar_x, bar_y, bar_w, bar_h))
            if self.player.max_hp > 0:
                fill_w = int(bar_w * (self.player.hp / float(self.player.max_hp)))
            else:
                fill_w = 0
            pygame.draw.rect(surface, GREEN, (bar_x, bar_y, fill_w, bar_h))
            pygame.draw.rect(surface, WHITE, (bar_x, bar_y, bar_w, bar_h), 2)
            hp_text = self.font_small.render(f"HP: {self.player.hp}/{self.player.max_hp}", True, WHITE)
            surface.blit(hp_text, (bar_x + 6, bar_y - 2))

        if self.state == COLLECT_PHASE:
            help_lines = [
                "Enter 短押し: 前進",
                "Enter 長押し: ジャンプ",
                "Enter ダブルタップ: 左へ / 発射"
            ]
        elif self.state == BOSS_PHASE:
            if self.selected_skill is None:
                help_lines = ["Enter 短押し: ワザを装填"]
            else:
                help_lines = ["装填済み: Enter 短押しで発動"]
        elif self.state == TITLE_SCREEN:
            help_lines = ["[短押し Enter で開始]"]
        elif self.state == GAME_CLEAR:
            help_lines = ["GAME CLEAR!  R: タイトルへ / Esc: 終了"]
        elif self.state == GAME_OVER:
            help_lines = ["GAME OVER... R:リトライ / Esc:終了"]
        elif self.state == SCORE_SCREEN:
            help_lines = [f"Score: {getattr(self, 'last_score', self.score)}", "R:リトライ / Esc:終了"]
        else:
            help_lines = []

        x_right = WINDOW_WIDTH - 30
        y_top = 50
        for line in help_lines:
            text = self.font_jp.render(line, True, WHITE)
            surface.blit(text, (x_right - text.get_width(), y_top))
            y_top += 34

        if self.state == COLLECT_PHASE:
            legend_w = 520
            legend_h = 48
            lx = WINDOW_WIDTH // 2 - legend_w // 2
            ly = 110
            pygame.draw.rect(surface, (20, 20, 30), (lx - 8, ly - 8, legend_w + 16, legend_h + 16), border_radius=8)
            gap = legend_w // len(LIGHTNING_VARIANTS)
            for i, v in enumerate(LIGHTNING_VARIANTS):
                cx = lx + i * gap + gap // 2
                box_rect = pygame.Rect(cx - 28, ly, 56, 36)
                pygame.draw.rect(surface, v["color"], box_rect, border_radius=6)
                pygame.draw.rect(surface, WHITE, box_rect, 2, border_radius=6)
                lab = f"x{v['factor']:.1f}"
                t = self.font_small.render(lab, True, WHITE)
                surface.blit(t, (cx - t.get_width() // 2, ly + 40 - 10))
                tn = self.font_jp.render(v["name"], True, WHITE)
                surface.blit(tn, (cx - tn.get_width() // 2, ly - 18))

        if self.state == GAME_CLEAR:
            text = self.font_large.render("GAME CLEAR", True, (255, 240, 200))
            text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 140))
            surface.blit(text, text_rect)

            sub = self.font_jp_large.render("世界はエンターキーの呪いから解放された", True, WHITE)
            sub_rect = sub.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 80))
            surface.blit(sub, sub_rect)

            score_t = self.font_medium.render(f"Score: {self.score}", True, YELLOW)
            st_rect = score_t.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 20))
            surface.blit(score_t, st_rect)

            hint1 = self.font_jp.render("R でタイトルに戻る", True, WHITE)
            hint2 = self.font_jp.render("Esc でゲーム一覧に戻る", True, WHITE)

            y = WINDOW_HEIGHT // 2 + 25
            surface.blit(hint1, (WINDOW_WIDTH // 2 - hint1.get_width() // 2, y))
            surface.blit(hint2, (WINDOW_WIDTH // 2 - hint2.get_width() // 2, y + 34))  
        
        elif self.state == GAME_OVER:
            text = self.font_large.render("世界は魔王に支配された...", True, (180, 30, 30))
            text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 120))
            surface.blit(text, text_rect)
            sub = self.font_jp_large.render("世界は消滅の淵にある", True, WHITE)
            sub_rect = sub.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 60))
            surface.blit(sub, sub_rect)
            score_t = self.font_medium.render(f"Final Score: {self.score}", True, YELLOW)
            st_rect = score_t.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 10))
            surface.blit(score_t, st_rect)
            hint = self.font_jp.render("R:リトライ / Esc:終了", True, WHITE)
            surface.blit(hint, (WINDOW_WIDTH // 2 - hint.get_width() // 2, WINDOW_HEIGHT // 2 + 30))
        elif self.state == SCORE_SCREEN:
            title = self.font_large.render("SCORE", True, YELLOW)
            title_rect = title.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 120))
            surface.blit(title, title_rect)
            sc = getattr(self, 'last_score', self.score)
            score_t = self.font_jp_large.render(f"Final Score: {sc}", True, WHITE)
            st_rect = score_t.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 40))
            surface.blit(score_t, st_rect)
            hint = self.font_jp.render("R:リトライ / Esc:終了", True, WHITE)
            surface.blit(hint, (WINDOW_WIDTH // 2 - hint.get_width() // 2, WINDOW_HEIGHT // 2 + 40))

    def draw_title_screen(self, surface):
        title_text = self.font_title.render(GAME_TITLE, True, WHITE)
        title_rect = title_text.get_rect(center=(WINDOW_WIDTH // 2, 140))
        surface.blit(title_text, title_rect)

        scenario_lines = [
            "So... you have awakened, Recorder.",
            "You were chosen to become the Administrator of the Eternal 30 Seconds.",
            "Now, fulfill your role and step forward.",
            "",
            "[Enter で開始]"
        ]

        y_offset = WINDOW_HEIGHT // 2 - 100
        for line in scenario_lines:
            text = self.font_jp.render(line, True, WHITE)
            text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, y_offset))
            surface.blit(text, text_rect)
            y_offset += 48

    def draw_collect_phase(self, surface):
        pygame.draw.rect(surface, GRAY, (0, GROUND_Y, WINDOW_WIDTH, WINDOW_HEIGHT - GROUND_Y))

        for item in self.items:
            item.draw(surface)

        for lightning in self.lightnings:
            lightning.draw(surface)

        self.player.draw(surface)

    def draw_boss_phase(self, surface):
        pygame.draw.rect(surface, GRAY, (0, GROUND_Y, WINDOW_WIDTH, WINDOW_HEIGHT - GROUND_Y))

        self.boss.draw(surface)
        self.player.draw(surface)

        if self.magic_circle:
            self.magic_circle.draw(surface)

        self.draw_boss_hp(surface)

        if self.selected_skill is None:
            self.draw_skill_menu(surface)
        else:
            self.draw_skill_effect(surface)

    def draw_boss_hp(self, surface):
        bar_w = 420
        bar_h = 28
        bar_x = WINDOW_WIDTH - 40 - bar_w
        bar_y = 30
        pygame.draw.rect(surface, DARK_GRAY, (bar_x, bar_y, bar_w, bar_h))
        if self.boss.max_hp > 0:
            fill_w = int(bar_w * (self.boss.hp / float(self.boss.max_hp)))
        else:
            fill_w = 0
        pygame.draw.rect(surface, RED, (bar_x, bar_y, fill_w, bar_h))
        pygame.draw.rect(surface, WHITE, (bar_x, bar_y, bar_w, bar_h), 3)
        t = self.font_small.render(f"BOSS: {self.boss.hp}/{self.boss.max_hp}", True, WHITE)
        surface.blit(t, (bar_x + 8, bar_y + (bar_h - t.get_height()) // 2))

    def draw_skill_menu(self, surface):
        menu_y = WINDOW_HEIGHT - 280

        for i, skill in enumerate(self.skill_options):
            if i == self.skill_highlight_index:
                color = YELLOW
                prefix = "> "
            else:
                color = WHITE
                prefix = "  "

            text = self.font_jp_large.render(f"{prefix}[ {skill} ]", True, color)
            text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, menu_y + i * 72))
            surface.blit(text, text_rect)

    def draw_skill_effect(self, surface):
        if self.selected_skill == "Mahou Kougeki":
            text = self.font_jp_large.render("CHARGE chuu...", True, PURPLE)
            text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT - 240))
            surface.blit(text, text_rect)

            gauge_width = 320
            gauge_height = 28
            gauge_x = WINDOW_WIDTH // 2 - gauge_width // 2
            gauge_y = WINDOW_HEIGHT - 200
            pygame.draw.rect(surface, GRAY, (gauge_x, gauge_y, gauge_width, gauge_height))
            fill_width = int(gauge_width * 0.6)
            pygame.draw.rect(surface, PURPLE, (gauge_x, gauge_y, fill_width, gauge_height))
            pygame.draw.rect(surface, WHITE, (gauge_x, gauge_y, gauge_width, gauge_height), 3)

        elif self.selected_skill == "Tama wo Tobasu" and self.countdown_value is not None:
            text = self.font_large.render(str(self.countdown_value), True, ORANGE)
            text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
            surface.blit(text, text_rect)

        elif self.selected_skill == "Ikkiuchi":
            text = self.font_jp_large.render("Ikkiuchi kaishi!", True, RED)
            text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT - 240))
            surface.blit(text, text_rect)

    def run(self):
        while self.running:
            try:
                self.handle_events()
                self.update()
                self.draw()
                self.clock.tick(FPS)
            except Exception:
                traceback.print_exc()
                self.last_score = self.score
                self.state = TITLE_SCREEN
                try:
                    self.reset_game()
                except Exception:
                    traceback.print_exc()

        try:
            pygame.mixer.music.fadeout(300)
        except Exception:
            pass
        pygame.quit()


if __name__ == "__main__":
    game = Game()
    game.run()

