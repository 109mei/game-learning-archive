import json
import math
import os
import sys
import pygame as pg

# ==================================================

pg.init()

WIDTH = 1280
HEIGHT = 720
FPS = 60
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Hill Rush")
clock = pg.time.Clock()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSET_DIR = os.path.join(BASE_DIR, "assets")
CHAR_DIR = os.path.join(ASSET_DIR, "characters")
AUDIO_DIR = os.path.join(ASSET_DIR, "audio")
LEVEL_DIR = os.path.join(ASSET_DIR, "levels")
ENEMY_DIR = os.path.join(ASSET_DIR, "enemies")
SAVE_PATH = os.path.join(BASE_DIR, "save_data.json")

# --------------------------------------------------
# COLORS / FONTS
# --------------------------------------------------
WHITE = (255, 255, 255)
BLACK = (28, 25, 23)
DARK = (55, 45, 38)
CREAM = (246, 232, 195)
GOLD = (245, 185, 34)
GREEN = (61, 168, 92)
GREEN_HOVER = (76, 192, 107)
BLUE = (64, 142, 201)
BLUE_HOVER = (79, 159, 220)
RED = (196, 74, 63)
RED_HOVER = (218, 92, 79)
PURPLE = (145, 101, 180)
PURPLE_HOVER = (166, 119, 202)
GRAY = (125, 119, 112)
PANEL = (250, 239, 210, 225)

font_small = pg.font.SysFont(None, 25)
font = pg.font.SysFont(None, 34)
font_medium = pg.font.SysFont(None, 46)
font_big = pg.font.SysFont(None, 72)
font_title = pg.font.SysFont(None, 84)

CHARACTERS = {
    "gamekid": {
        "name": "GAME KID",
        "cost": 0,
        "files": ["gamekid_1.png", "gamekid_2.png", "gamekid_3.png"],
    },
    "bunny": {
        "name": "PURPLE BUNNY",
        "cost": 1200,
        "files": ["bunny_1.png", "bunny_2.png", "bunny_3.png", "bunny_4.png"],
    },
    "rotor": {
        "name": "ROTOR BOT",
        "cost": 3500,
        "files": ["rotor_1.png", "rotor_2.png"],
    },
    "cone": {
        "name": "CONE BOT",
        "cost": 7000,
        "files": ["cone_1.png", "cone_2.png", "cone_3.png", "cone_4.png"],
    },
}

MUSIC_NAMES = ["ORIGINAL BG", "BACKGROUND 1", "BACKGROUND 2"]
MUSIC_FILES = ["5(1).mp3", "1.mp3", "2.mp3"]


LEVELS = {
    
    1: {
        "name": "GREEN HILLS",
        "difficulty": "MODERATE",
        "background": os.path.join(ASSET_DIR, "background.png"),
        "length": 5600.0,
        "start_speed": 160.0,
        "min_speed": 0.0,
        "max_speed": 345.0,
        "acceleration": 125.0,
        "deceleration": 370.0,
        "gravity": 920.0,
        "jump_power": 438.0,
        "jump_forward_min": 225.0,
        "booster_bonus": 72.0,
        "booster_target": 265.0,
        "enemy_types": ["puffer", "launcher", "winged"],
        "enemy_gap": 930,
        "road": (168, 103, 56),
        "edge": (55, 190, 95),
        "terrain": (48, 23, 10),
        "projectile_speed": 235.0,
    },
    2: {
        "name": "ORANGE WOODS",
        "difficulty": "MODERATE - HARD",
        "background": os.path.join(LEVEL_DIR, "level2_orange.png"),
        "length": 6500.0,
        "start_speed": 172.0,
        "min_speed": 0.0,
        "max_speed": 370.0,
        "acceleration": 133.0,
        "deceleration": 385.0,
        "gravity": 942.0,
        "jump_power": 445.0,
        "jump_forward_min": 238.0,
        "booster_bonus": 78.0,
        "booster_target": 288.0,
        "enemy_types": ["puffer", "launcher", "winged"],
        "enemy_gap": 850,
        "road": (180, 103, 60),
        "edge": (242, 133, 48),
        "terrain": (53, 27, 11),
        "projectile_speed": 265.0,
    },
    3: {
        "name": "DESERT DASH",
        "difficulty": "HARD",
        "background": os.path.join(LEVEL_DIR, "level3_desert.png"),
        "length": 7400.0,
        "start_speed": 184.0,
        "min_speed": 0.0,
        "max_speed": 400.0,
        "acceleration": 142.0,
        "deceleration": 405.0,
        "gravity": 965.0,
        "jump_power": 453.0,
        "jump_forward_min": 252.0,
        "booster_bonus": 84.0,
        "booster_target": 312.0,
        "enemy_types": ["puffer", "launcher", "winged"],
        "enemy_gap": 790,
        "road": (213, 168, 97),
        "edge": (246, 222, 169),
        "terrain": (42, 20, 8),
        "projectile_speed": 300.0,
    },
    4: {
        "name": "CASTLE RUSH",
        "difficulty": "HARDEST",
        "background": os.path.join(LEVEL_DIR, "level4_castle.png"),
        "length": 8600.0,
        "start_speed": 198.0,
        "min_speed": 0.0,
        "max_speed": 432.0,
        "acceleration": 152.0,
        "deceleration": 425.0,
        "gravity": 990.0,
        "jump_power": 465.0,
        "jump_forward_min": 270.0,
        "booster_bonus": 90.0,
        "booster_target": 338.0,
        "enemy_types": ["puffer", "launcher", "winged"],
        "enemy_gap": 735,
        "road": (109, 147, 171),
        "edge": (187, 228, 246),
        "terrain": (60, 31, 13),
        "projectile_speed": 335.0,
    },
}

TOTAL_LEVELS = 4
COIN_VALUE = 10
DOUBLE_TAP_MS = 300
BOOST_TIME = 1.25
PROJECTILE_WARNING_TIME = 0.48
PLAYER_HALF_HEIGHT = 38
PLAYER_RADIUS = 29

# --------------------------------------------------
# IMAGE HELPERS
# --------------------------------------------------
def load_scaled(path, size, alpha=True):
    image = pg.image.load(path)
    image = image.convert_alpha() if alpha else image.convert()
    return pg.transform.smoothscale(image, size)


def load_cover(path, size):
    """Scale without stretching, then crop to fill the screen."""
    image = pg.image.load(path).convert()
    iw, ih = image.get_size()
    tw, th = size
    scale = max(tw / iw, th / ih)
    nw = max(1, int(iw * scale))
    nh = max(1, int(ih * scale))
    image = pg.transform.smoothscale(image, (nw, nh))
    x = max(0, (nw - tw) // 2)
    y = max(0, (nh - th) // 2)
    return image.subsurface(pg.Rect(x, y, tw, th)).copy()


menu_background = load_cover(os.path.join(ASSET_DIR, "menu_background.jpg"), (WIDTH, HEIGHT))
coin_img = load_scaled(os.path.join(ASSET_DIR, "coin.png"), (42, 42), alpha=True)
coin_small = pg.transform.smoothscale(coin_img, (30, 30))
finish_house = load_scaled(os.path.join(ASSET_DIR, "finish_house.png"), (170, 153), alpha=True)

level_backgrounds = {
    level: load_cover(info["background"], (WIDTH, HEIGHT))
    for level, info in LEVELS.items()
}

character_frames = {}
for key, info in CHARACTERS.items():
    frames = []
    for filename in info["files"]:
        img = pg.image.load(os.path.join(CHAR_DIR, filename)).convert_alpha()
        frames.append(pg.transform.smoothscale(img, (88, 88)))
    character_frames[key] = frames

enemy_images = {
    "puffer": load_scaled(os.path.join(ENEMY_DIR, "puffer.png"), (72, 72), alpha=True),
    "launcher": load_scaled(os.path.join(ENEMY_DIR, "launcher.png"), (58, 61), alpha=True),
    "winged": load_scaled(os.path.join(ENEMY_DIR, "winged.png"), (92, 48), alpha=True),
    "projectile": load_scaled(os.path.join(ENEMY_DIR, "projectile.png"), (25, 25), alpha=True),
}

# --------------------------------------------------
# SAVE DATA
# --------------------------------------------------
def default_profile():
    return {
        "points": 0,
        "best_time": 0.0,
        "selected_character": "gamekid",
        "unlocked": ["gamekid"],
        "music_enabled": True,
        "music_track": 0,
        "levels_cleared": 0,
    }


def load_profile():
    data = default_profile()
    try:
        with open(SAVE_PATH, "r", encoding="utf-8") as file:
            loaded = json.load(file)
        data.update(loaded)
    except (OSError, json.JSONDecodeError):
        pass

    if data.get("selected_character") not in CHARACTERS:
        data["selected_character"] = "gamekid"

    unlocked = [key for key in data.get("unlocked", []) if key in CHARACTERS]
    if "gamekid" not in unlocked:
        unlocked.insert(0, "gamekid")
    data["unlocked"] = unlocked

    data["points"] = max(0, int(data.get("points", 0)))
    data["best_time"] = max(0.0, float(data.get("best_time", 0.0)))
    data["music_enabled"] = bool(data.get("music_enabled", True))
    data["music_track"] = int(data.get("music_track", 0)) % len(MUSIC_FILES)
    data["levels_cleared"] = max(0, min(TOTAL_LEVELS, int(data.get("levels_cleared", 0))))
    data.pop("tutorial_seen", None)
    return data


def save_profile():
    try:
        with open(SAVE_PATH, "w", encoding="utf-8") as file:
            json.dump(profile, file, indent=2)
    except OSError:
        pass


profile = load_profile()

# --------------------------------------------------
# AUDIO
# --------------------------------------------------
class AudioManager:
    def __init__(self):
        self.available = False
        self.sfx = {}
        try:
            if not pg.mixer.get_init():
                pg.mixer.init(frequency=22050, size=-16, channels=1, buffer=512)
            self.sfx = {
                "start": pg.mixer.Sound(os.path.join(AUDIO_DIR, "13.mp3")),
                "game_over": pg.mixer.Sound(os.path.join(AUDIO_DIR, "4.mp3")),
                "booster": pg.mixer.Sound(os.path.join(AUDIO_DIR, "5.mp3")),
                "coin": pg.mixer.Sound(os.path.join(AUDIO_DIR, "6.mp3")),
            }
            for sound in self.sfx.values():
                sound.set_volume(0.38)
            self.available = True
        except pg.error:
            self.available = False

    def play_sfx(self, name):
        if self.available and name in self.sfx:
            self.sfx[name].play()

    def apply_music(self):
        if not self.available:
            return
        if not profile["music_enabled"]:
            pg.mixer.music.stop()
            return
        try:
            track = os.path.join(AUDIO_DIR, MUSIC_FILES[profile["music_track"]])
            pg.mixer.music.load(track)
            pg.mixer.music.set_volume(0.18)
            pg.mixer.music.play(-1)
        except pg.error:
            pass


audio = AudioManager()
audio.apply_music()

# --------------------------------------------------
# UI HELPERS
# --------------------------------------------------
def draw_text(text, font_obj, color, x, y, center=False):
    surf = font_obj.render(text, True, color)
    rect = surf.get_rect()
    if center:
        rect.center = (x, y)
    else:
        rect.topleft = (x, y)
    screen.blit(surf, rect)
    return rect


def draw_panel(rect, color=PANEL, radius=18, border=(105, 79, 55)):
    panel = pg.Surface((rect.width, rect.height), pg.SRCALPHA)
    pg.draw.rect(panel, color, panel.get_rect(), border_radius=radius)
    screen.blit(panel, rect.topleft)
    pg.draw.rect(screen, border, rect, 2, border_radius=radius)


class Button:
    def __init__(self, rect, text, color=GREEN, hover=GREEN_HOVER, font_obj=font_medium):
        self.rect = pg.Rect(rect)
        self.text = text
        self.color = color
        self.hover = hover
        self.font = font_obj

    def draw(self):
        mouse = pg.mouse.get_pos()
        color = self.hover if self.rect.collidepoint(mouse) else self.color
        pg.draw.rect(screen, color, self.rect, border_radius=12)
        pg.draw.rect(screen, DARK, self.rect, 3, border_radius=12)
        draw_text(self.text, self.font, WHITE, self.rect.centerx, self.rect.centery + 1, center=True)

    def clicked(self, pos):
        return self.rect.collidepoint(pos)


# --------------------------------------------------
# TERRAIN
# --------------------------------------------------
def ground_y(x, level=None):
    if level is None:
        level = game["level"] if game else 1
    a, b, c = LEVELS[level]["terrain"]
    # Different frequencies make the route rough without becoming random.
    return 535 + a * math.sin(x / 195) + b * math.sin(x / 86) + c * math.sin(x / 39)


def road_slope(x, level=None):
    d = 3
    return (ground_y(x + d, level) - ground_y(x - d, level)) / (2 * d)


def road_angle(x, level=None):
    return math.degrees(math.atan(road_slope(x, level)))


# --------------------------------------------------
# LEVEL OBJECTS
# --------------------------------------------------
def terrain_curvature(x, level):
    d = 10
    return ground_y(x + d, level) - 2 * ground_y(x, level) + ground_y(x - d, level)


def terrain_fairness_score(x, level, prefer_low=False):
    """Lower score = easier to read and safer to place an object here."""
    slope = abs(road_slope(x, level))
    curve = abs(terrain_curvature(x, level))
    ground = ground_y(x, level)
    high_crest = max(0.0, 520 - ground)
    score = slope * 190 + curve * 10
    if prefer_low:
        score += high_crest * 1.6
    return score


def find_fair_obstacle_x(target_x, level, used_positions, kind):
    """Shift an authored enemy target slightly so it never sits on a bad crest."""
    best_x = float(target_x)
    best_score = 10**9
    for offset in range(-180, 181, 10):
        x = float(target_x + offset)
        if x < 1050 or x > LEVELS[level]["length"] - 650:
            continue
        if any(abs(x - old) < 650 for old in used_positions):
            continue

        score = terrain_fairness_score(x, level, prefer_low=(kind == "puffer"))
        # Ground enemies should be especially readable and close to flat.
        if kind in ("puffer", "launcher"):
            score += abs(road_slope(x, level)) * 90
        score += abs(offset) * 0.04

        if score < best_score:
            best_score = score
            best_x = x
    return best_x


def find_booster_before(enemy_x, level):
    """Find gentle ground 360-470 px before an assisted enemy."""
    best_x = enemy_x - 420
    best_score = 10**9
    for distance in range(360, 471, 10):
        x = enemy_x - distance
        if x < 650:
            continue
        score = terrain_fairness_score(x, level, prefer_low=False)
        score += abs(distance - 415) * 0.02
        if score < best_score:
            best_score = score
            best_x = x
    return float(best_x)


# The route is authored as encounters rather than scattering objects independently.
# "boost": True means the encounter always receives a usable booster before it.
LEVEL_ENCOUNTER_PLAN = {
    # Fixed layouts: different per level, identical after restart so they are learnable.
    # Level 1 is moderate and already contains all three enemy types.
    1: [
        {"kind": "puffer", "x": 1320, "boost": True},
        {"kind": "winged", "x": 2460, "boost": False, "wing_base": 116, "wing_amp": 58, "wing_freq": 4.2},
        {"kind": "launcher", "x": 3600, "boost": False},
        {"kind": "puffer", "x": 4740, "boost": True},
    ],
    2: [
        {"kind": "launcher", "x": 1180, "boost": False},
        {"kind": "puffer", "x": 2160, "boost": True},
        {"kind": "winged", "x": 3160, "boost": False, "wing_base": 118, "wing_amp": 68, "wing_freq": 4.9},
        {"kind": "puffer", "x": 4160, "boost": True},
        {"kind": "launcher", "x": 5100, "boost": False},
        {"kind": "winged", "x": 5780, "boost": False, "wing_base": 122, "wing_amp": 70, "wing_freq": 5.2},
    ],
    3: [
        {"kind": "winged", "x": 1180, "boost": False, "wing_base": 120, "wing_amp": 76, "wing_freq": 5.4},
        {"kind": "puffer", "x": 2080, "boost": True},
        {"kind": "launcher", "x": 3000, "boost": False},
        {"kind": "winged", "x": 3940, "boost": False, "wing_base": 124, "wing_amp": 80, "wing_freq": 5.8},
        {"kind": "puffer", "x": 4880, "boost": True},
        {"kind": "launcher", "x": 5800, "boost": False},
        {"kind": "winged", "x": 6680, "boost": False, "wing_base": 126, "wing_amp": 82, "wing_freq": 6.0},
    ],
    4: [
        {"kind": "launcher", "x": 1120, "boost": False},
        {"kind": "winged", "x": 1960, "boost": False, "wing_base": 124, "wing_amp": 84, "wing_freq": 6.1},
        {"kind": "puffer", "x": 2820, "boost": True},
        {"kind": "launcher", "x": 3680, "boost": False},
        {"kind": "winged", "x": 4540, "boost": False, "wing_base": 128, "wing_amp": 90, "wing_freq": 6.6},
        {"kind": "puffer", "x": 5400, "boost": True},
        {"kind": "winged", "x": 6260, "boost": False, "wing_base": 126, "wing_amp": 88, "wing_freq": 7.0},
        {"kind": "launcher", "x": 7120, "boost": False},
        {"kind": "puffer", "x": 7900, "boost": True},
    ],
}


def create_enemies(level):
    # The authored positions above are already selected on fair terrain.
    # Do not shift or randomize them: every level has one learnable layout.
    enemies = []
    for index, item in enumerate(LEVEL_ENCOUNTER_PLAN[level]):
        enemies.append({
            "kind": item["kind"],
            "x": float(item["x"]),
            "needs_boost": item["boost"],
            "phase": index * 0.91,
            "wing_base": item.get("wing_base", 116),
            "wing_amp": item.get("wing_amp", 70),
            "wing_freq": item.get("wing_freq", 5.0),
            "last_shot": -999.0,
            "warn_until": 0.0,
        })
    return enemies


def create_boosters(level, enemies=None):
    """One intentional booster before each difficult encounter; no random extras."""
    if enemies is None:
        enemies = create_enemies(level)

    boosters = []
    for enemy in enemies:
        if not enemy.get("needs_boost"):
            continue
        bx = find_booster_before(enemy["x"], level)
        boosters.append({
            "x": bx,
            "used": False,
            "for_enemy": enemy["x"],
        })

    # De-duplicate only genuine accidental overlaps, keeping the encounter booster.
    boosters.sort(key=lambda b: b["x"])
    cleaned = []
    for booster in boosters:
        if cleaned and booster["x"] - cleaned[-1]["x"] < 300:
            # Keep the later booster because it belongs to the nearer danger.
            cleaned[-1] = booster
        else:
            cleaned.append(booster)
    return cleaned


def add_coin(coins, x, y, kind="normal"):
    """Add one coin unless another coin is already almost on top of it."""
    if any((x - c["x"]) ** 2 + (y - c["y"]) ** 2 < 55 ** 2 for c in coins):
        return
    coins.append({"x": float(x), "y": float(y), "taken": False, "kind": kind})


def add_ground_coin_line(coins, start, end, level, spacing=175):
    x = float(start)
    while x <= end:
        add_coin(coins, x, ground_y(x, level) - 73, "ground")
        x += spacing


def add_jump_arc(coins, enemy, level):
    """Coins visually teach the safe jump path over each obstacle."""
    ex = enemy["x"]
    kind = enemy["kind"]

    # Launchers are narrower; puffers/winged enemies get a slightly higher arc.
    if kind == "launcher":
        offsets = [-205, -140, -75, 0, 75, 140, 205]
        heights = [88, 122, 155, 180, 155, 122, 88]
    else:
        offsets = [-220, -150, -80, 0, 80, 150, 220]
        heights = [92, 135, 178, 210, 178, 135, 92]

    for dx, height in zip(offsets, heights):
        cx = ex + dx
        add_coin(coins, cx, ground_y(cx, level) - height, "jump")


def create_coins(level, enemies=None, boosters=None):
    """Build an even reward rhythm: approach -> booster -> jump arc -> recovery."""
    finish_x = LEVELS[level]["length"]
    if enemies is None:
        enemies = create_enemies(level)
    if boosters is None:
        boosters = create_boosters(level, enemies)

    coins = []

    # Start with an easy coin trail so every level begins readable rather than empty.
    add_ground_coin_line(coins, 480, 920, level, 145)

    # Ground coins are distributed throughout safe spaces only.
    # Around every enemy we reserve a large clear zone and replace it with a jump arc.
    safe_x = 1050.0
    while safe_x < finish_x - 360:
        near_enemy = any(abs(safe_x - e["x"]) < 310 for e in enemies)
        near_booster = any(abs(safe_x - b["x"]) < 105 for b in boosters)
        if not near_enemy and not near_booster:
            add_coin(coins, safe_x, ground_y(safe_x, level) - 73, "ground")
        safe_x += max(185, 220 - level * 8)

    # Each booster has two lead-in coins, but never a coin directly on the pad.
    for booster in boosters:
        bx = booster["x"]
        for dx in (-150, -75):
            cx = bx + dx
            if cx > 420:
                add_coin(coins, cx, ground_y(cx, level) - 73, "boost_lead")

    # Every enemy gets exactly one readable reward arc.
    for enemy in enemies:
        add_jump_arc(coins, enemy, level)

        # Two recovery coins after the landing zone. This makes the rhythm obvious.
        for dx in (310, 470):
            cx = enemy["x"] + dx
            if cx < finish_x - 330 and all(abs(cx - other["x"]) > 260 for other in enemies if other is not enemy):
                add_coin(coins, cx, ground_y(cx, level) - 73, "recovery")

    # A short final trail leads visibly toward the house, with no enemy in the way.
    final_start = max(700, finish_x - 560)
    add_ground_coin_line(coins, final_start, finish_x - 220, level, 115)

    coins.sort(key=lambda c: c["x"])
    return coins


def validate_level_layout(level, enemies, boosters, coins):
    """Sanity checks that stop impossible layouts from creeping back in."""
    finish_x = LEVELS[level]["length"]

    # Enemies need clear reaction/landing space.
    enemy_x = sorted(e["x"] for e in enemies)
    for a, b in zip(enemy_x, enemy_x[1:]):
        if b - a < 650:
            raise ValueError(f"Level {level}: enemies too close at {a:.0f}/{b:.0f}")

    for enemy in enemies:
        if enemy.get("needs_boost"):
            candidates = [b for b in boosters if 330 <= enemy["x"] - b["x"] <= 500]
            if not candidates:
                raise ValueError(f"Level {level}: missing usable booster before {enemy['kind']} at {enemy['x']:.0f}")

    for booster in boosters:
        if abs(road_slope(booster["x"], level)) > 0.55:
            raise ValueError(f"Level {level}: booster on terrain that is too steep")

    if any(e["x"] > finish_x - 600 for e in enemies):
        raise ValueError(f"Level {level}: enemy too close to finish")

def new_level_state(level, run_time=0.0, run_points=0, run_coins=0):
    config = LEVELS[level]
    enemies = create_enemies(level)
    boosters = create_boosters(level, enemies)
    coins = create_coins(level, enemies, boosters)
    validate_level_layout(level, enemies, boosters, coins)
    return {
        "level": level,
        "x": 250.0,
        "y": ground_y(250, level) - PLAYER_HALF_HEIGHT,
        "speed": 0.0,
        "vy": 0.0,
        "angle": road_angle(250, level) * 0.24,
        "airborne": False,
        "coins": coins,
        "boosters": boosters,
        "enemies": enemies,
        "projectiles": [],
        "level_points": 0,
        "level_coins": 0,
        "run_points": run_points,
        "run_coins": run_coins,
        "level_time": 0.0,
        "run_time": run_time,
        "anim_time": 0.0,
        "last_tap_ms": -9999,
        "boost_timer": 0.0,
        "jump_flash": 0.0,
        "banked": False,
        "death_reason": "",
        "banner_time": 1.7,
        "started": False,
    }


game = new_level_state(1)

# --------------------------------------------------
# SCREEN STATE / BUTTONS
# --------------------------------------------------
state = "menu"  # menu / characters / music / tutorial / game / gameover / levelcomplete / victory

tutorial_step = 0
tutorial_time = 0.0
TUTORIAL_LAST_STEP = 4
TUTORIAL_FLOOR_Y = 500
TUTORIAL_SUCCESS_DELAY = 1.25
tutorial_demo = {}

menu_start = Button((125, 220, 290, 58), "START", GREEN, GREEN_HOVER)
menu_char = Button((125, 300, 290, 58), "SELECT CHARACTER", BLUE, BLUE_HOVER, font)
menu_music = Button((125, 380, 290, 58), "MUSIC", PURPLE, PURPLE_HOVER)
menu_quit = Button((125, 590, 290, 58), "QUIT", RED, RED_HOVER)
menu_bg_buttons = [
    Button((125, 500, 88, 44), "BG 1", BLUE, BLUE_HOVER, font_small),
    Button((226, 500, 88, 44), "BG 2", BLUE, BLUE_HOVER, font_small),
    Button((327, 500, 88, 44), "BG 3", BLUE, BLUE_HOVER, font_small),
]
back_button = Button((55, 625, 190, 55), "BACK", RED, RED_HOVER, font)
music_toggle = Button((420, 205, 440, 62), "", GREEN, GREEN_HOVER, font)
music_track_buttons = [
    Button((365, 340, 550, 55), "", BLUE, BLUE_HOVER, font),
    Button((365, 410, 550, 55), "", BLUE, BLUE_HOVER, font),
    Button((365, 480, 550, 55), "", BLUE, BLUE_HOVER, font),
]

character_keys = list(CHARACTERS.keys())
character_cards = {}
card_w, card_h = 255, 360
start_x = 65
gap = 40
for i, key in enumerate(character_keys):
    character_cards[key] = pg.Rect(start_x + i * (card_w + gap), 190, card_w, card_h)


# --------------------------------------------------
# MENU
# --------------------------------------------------
def selected_preview(size=150):
    key = profile["selected_character"]
    return pg.transform.smoothscale(character_frames[key][0], (size, size))


def draw_main_menu():
    screen.blit(menu_background, (0, 0))

    draw_text("HILL RUSH", font_title, DARK, WIDTH // 2, 86, center=True)
    draw_text("ONE BUTTON GAME", font_small, DARK, WIDTH // 2, 138, center=True)

    left_panel = pg.Rect(95, 185, 355, 475)
    draw_panel(left_panel, color=(249, 241, 220, 228), border=(110, 84, 58))

    menu_start.draw()
    menu_char.draw()
    menu_music.draw()

    draw_text("MUSIC TRACK", font_small, DARK, 270, 470, center=True)
    for i, button in enumerate(menu_bg_buttons):
        selected = i == profile["music_track"]
        button.color = GREEN if selected else BLUE
        button.hover = GREEN_HOVER if selected else BLUE_HOVER
        button.draw()

    menu_quit.draw()

    char_panel = pg.Rect(495, 220, 330, 320)
    draw_panel(char_panel, color=(248, 242, 228, 235), border=(110, 84, 58))
    draw_text("SELECTED CHARACTER", font_small, DARK, char_panel.centerx, 258, center=True)
    preview = selected_preview(175)
    screen.blit(preview, preview.get_rect(center=(char_panel.centerx, 372)))
    draw_text(CHARACTERS[profile["selected_character"]]["name"], font, DARK, char_panel.centerx, 500, center=True)

    controls_panel = pg.Rect(495, 560, 330, 98)
    draw_panel(controls_panel, color=(246, 244, 236, 228), border=(110, 84, 58))
    draw_text("SPACE: START / HOLD: RUN", font_small, DARK, controls_panel.centerx, 592, center=True)
    draw_text("DOUBLE TAP: JUMP / RELEASE: STOP", font_small, DARK, controls_panel.centerx, 624, center=True)

    board = pg.Rect(870, 220, 330, 395)
    draw_panel(board, color=(248, 224, 153, 235), border=(120, 87, 42))
    draw_text("SCOREBOARD", font_medium, DARK, board.centerx, 265, center=True)
    pg.draw.line(screen, DARK, (910, 300), (1160, 300), 2)

    screen.blit(coin_small, (920, 328))
    draw_text("TOTAL POINTS", font_small, DARK, 964, 329)
    draw_text(str(profile["points"]), font_medium, DARK, board.centerx, 385, center=True)

    draw_text("BEST SURVIVAL TIME", font_small, DARK, board.centerx, 445, center=True)
    draw_text(f"{profile['best_time']:.1f} sec", font, DARK, board.centerx, 482, center=True)

    draw_text("LEVELS CLEARED", font_small, DARK, board.centerx, 530, center=True)
    draw_text(f"{profile['levels_cleared']} / {TOTAL_LEVELS}", font, DARK, board.centerx, 563, center=True)

    music_status = "ON" if profile["music_enabled"] else "OFF"
    selected_music = MUSIC_NAMES[profile["music_track"]]
    draw_text(f"MUSIC: {music_status} - {selected_music}", font_small, GRAY, board.centerx, 597, center=True)


# --------------------------------------------------
# CHARACTER SHOP
# --------------------------------------------------
def draw_character_select():
    screen.blit(menu_background, (0, 0))
    draw_text("SELECT CHARACTER", font_big, DARK, WIDTH // 2, 82, center=True)
    draw_text(f"Your points: {profile['points']}", font, DARK, WIDTH // 2, 135, center=True)

    mouse = pg.mouse.get_pos()
    for key in character_keys:
        info = CHARACTERS[key]
        rect = character_cards[key]
        unlocked = key in profile["unlocked"]
        selected = key == profile["selected_character"]
        hover = rect.collidepoint(mouse)

        fill = (255, 245, 218, 235) if not hover else (255, 250, 230, 245)
        if selected:
            fill = (222, 247, 220, 240)
        draw_panel(rect, fill, radius=18, border=GREEN if selected else (105, 79, 55))

        draw_text(info["name"], font, DARK, rect.centerx, rect.top + 38, center=True)
        icon = pg.transform.smoothscale(character_frames[key][0], (150, 150))
        screen.blit(icon, icon.get_rect(center=(rect.centerx, rect.top + 145)))

        if selected:
            label, color = "SELECTED", GREEN
        elif unlocked:
            label, color = "SELECT", BLUE
        else:
            label, color = f"BUY {info['cost']} PTS", GOLD

        button_rect = pg.Rect(rect.left + 24, rect.bottom - 76, rect.width - 48, 48)
        pg.draw.rect(screen, color, button_rect, border_radius=10)
        pg.draw.rect(screen, DARK, button_rect, 2, border_radius=10)
        draw_text(label, font_small, DARK if color == GOLD else WHITE, button_rect.centerx, button_rect.centery, center=True)

        if not unlocked and profile["points"] < info["cost"]:
            draw_text("LOCKED", font_small, RED, rect.centerx, rect.bottom - 102, center=True)
        elif unlocked and not selected:
            draw_text("UNLOCKED", font_small, GREEN, rect.centerx, rect.bottom - 102, center=True)

    back_button.draw()
    draw_text("Coins are worth 10 points. Rare characters require many successful runs.", font_small, DARK, WIDTH // 2, 665, center=True)


def handle_character_click(pos):
    for key, rect in character_cards.items():
        if not rect.collidepoint(pos):
            continue

        if key in profile["unlocked"]:
            profile["selected_character"] = key
            save_profile()
        else:
            cost = CHARACTERS[key]["cost"]
            if profile["points"] >= cost:
                profile["points"] -= cost
                profile["unlocked"].append(key)
                profile["selected_character"] = key
                save_profile()
                # No separate purchase sound in the current audio set.
        return


# --------------------------------------------------
# MUSIC MENU
# --------------------------------------------------
def draw_music_menu():
    screen.blit(menu_background, (0, 0))
    draw_text("MUSIC", font_title, DARK, WIDTH // 2, 80, center=True)

    panel = pg.Rect(300, 145, 680, 455)
    draw_panel(panel)

    enabled = profile["music_enabled"]
    music_toggle.text = "MUSIC: ON" if enabled else "MUSIC: OFF"
    music_toggle.color = GREEN if enabled else RED
    music_toggle.hover = GREEN_HOVER if enabled else RED_HOVER
    music_toggle.draw()

    draw_text("SELECT BACKGROUND MUSIC", font, DARK, WIDTH // 2, 305, center=True)

    for i, button in enumerate(music_track_buttons):
        selected = i == profile["music_track"]
        button.text = f"{i + 1}. {MUSIC_NAMES[i]}"
        button.color = GREEN if selected else BLUE
        button.hover = GREEN_HOVER if selected else BLUE_HOVER
        button.draw()
        if selected:
            draw_text("SELECTED", font_small, GREEN, button.rect.right + 72, button.rect.centery, center=True)

    draw_text("Choose 1 of 3 background tracks. Sound effects stay active.", font_small, GRAY, WIDTH // 2, 565, center=True)
    back_button.draw()


# --------------------------------------------------
# GAME DRAWING
# --------------------------------------------------
def draw_road(camera_x):
    level = game["level"]
    config = LEVELS[level]
    points = []
    for sx in range(-20, WIDTH + 40, 8):
        wx = camera_x + sx
        points.append((sx, int(ground_y(wx, level))))

    polygon = points + [(WIDTH + 40, HEIGHT), (-20, HEIGHT)]
    pg.draw.polygon(screen, config["road"], polygon)

    edge_bottom = [(sx, y + 15) for sx, y in reversed(points)]
    pg.draw.polygon(screen, config["edge"], points + edge_bottom)


def recommended_jump_speed(enemy):
    config = LEVELS[game["level"]]
    if enemy.get("needs_boost"):
        return config["booster_target"]
    return max(config["jump_forward_min"], config["start_speed"] + 85.0)


def jump_hint_x(enemy):
    """Fixed take-off marker tuned to put the obstacle near jump apex.

    The marker is where the player's SECOND SPACE tap should happen.  A wide
    assisted zone around it makes a correctly timed double-tap reliable.
    """
    config = LEVELS[game["level"]]
    expected_speed = recommended_jump_speed(enemy)
    apex_time = config["jump_power"] / config["gravity"]
    lead = expected_speed * apex_time
    # Give larger enemies a little more approach room.
    if enemy["kind"] == "winged":
        lead += 22.0
    elif enemy["kind"] == "puffer":
        lead += 14.0
    else:
        lead += 8.0
    return enemy["x"] - lead


def guided_enemy_for_jump():
    """Return the obstacle whose take-off marker the player is currently using."""
    best = None
    best_distance = 10**9
    for enemy in game["enemies"]:
        if enemy["x"] <= game["x"]:
            continue
        marker = jump_hint_x(enemy)
        distance = abs(game["x"] - marker)
        # The second tap may happen slightly after the visible stripe.
        if distance <= 85 and distance < best_distance:
            if enemy["kind"] == "winged" and winged_route_choice(enemy) != "over":
                continue
            best = enemy
            best_distance = distance
    return best


def guided_safe_height(enemy):
    """Safe player-centre Y at the obstacle for a guided jump."""
    ground = ground_y(enemy["x"], game["level"])
    if enemy["kind"] == "winged":
        return ground - 165
    if enemy["kind"] == "puffer":
        return ground - 150
    return ground - 125


def draw_jump_trajectory(enemy, camera_x, marker_x):
    """Draw a simple dotted guide showing the intended jump path."""
    start_x = marker_x
    end_x = enemy["x"] + (205 if enemy["kind"] != "launcher" else 175)
    start_y = ground_y(start_x, game["level"]) - PLAYER_HALF_HEIGHT
    end_y = ground_y(end_x, game["level"]) - PLAYER_HALF_HEIGHT

    # The guide is deliberately a little higher than the obstacle so the
    # player reads it as a safe route, not as an exact physics prediction.
    extra_height = 205 if enemy["kind"] in ("puffer", "winged") else 175
    control_x = (start_x + end_x) * 0.5
    control_y = min(start_y, end_y, ground_y(enemy["x"], game["level"]) - 95) - extra_height

    for i in range(1, 15):
        t = i / 15.0
        u = 1.0 - t
        wx = u * u * start_x + 2 * u * t * control_x + t * t * end_x
        wy = u * u * start_y + 2 * u * t * control_y + t * t * end_y
        sx = int(wx - camera_x)
        if -20 <= sx <= WIDTH + 20:
            radius = 5 if i % 2 else 4
            pg.draw.circle(screen, (255, 235, 85), (sx, int(wy)), radius)
            pg.draw.circle(screen, (120, 85, 20), (sx, int(wy)), radius, 1)


def winged_route_choice(enemy):
    """Predict whether the bird will be high or low when the player reaches it."""
    distance = max(1.0, enemy["x"] - game["x"])
    approach_speed = max(game["speed"], recommended_jump_speed(enemy), 205.0)
    travel_time = distance / approach_speed
    future_y = winged_y(enemy, travel_time)
    ground = ground_y(enemy["x"], game["level"])
    clearance = ground - future_y

    # High bird: safe gap beneath it. Low bird: jump above it. Middle band is
    # deliberately dangerous, so the player should stop and wait.
    if clearance >= 150:
        return "under"
    if clearance <= 92:
        return "over"
    return "wait"


def draw_under_path(enemy, camera_x):
    """Draw a short cyan path under a high bird."""
    start_x = enemy["x"] - 230
    end_x = enemy["x"] + 170
    for i in range(10):
        wx = start_x + (end_x - start_x) * i / 9
        wy = ground_y(wx, game["level"]) - PLAYER_HALF_HEIGHT - 5
        sx = int(wx - camera_x)
        if -20 <= sx <= WIDTH + 20:
            pg.draw.circle(screen, (80, 225, 245), (sx, int(wy)), 5)
            pg.draw.circle(screen, (28, 104, 130), (sx, int(wy)), 5, 1)


def draw_jump_hints(camera_x):
    """Hints remain useful, but later flying enemies require timing choices."""
    upcoming = [e for e in game["enemies"] if -40 < e["x"] - game["x"] < 820]
    if not upcoming:
        return

    enemy = min(upcoming, key=lambda e: e["x"])
    marker_x = jump_hint_x(enemy)
    marker_distance = marker_x - game["x"]
    if marker_distance < -80:
        return

    route = "over"
    if enemy["kind"] == "winged":
        route = winged_route_choice(enemy)

    ex, ey = enemy_position(enemy)
    obstacle_sx = int(ex - camera_x)
    image = enemy_draw_image(enemy)
    obstacle_top = int(ey - image.get_height() * 0.55)

    # Flying gates have three states: run under, jump over, or wait.
    if enemy["kind"] == "winged" and route == "under":
        draw_under_path(enemy, camera_x)
        label = "BIRD HIGH - RUN UNDER"
        label_color = (196, 248, 255)
        border = (28, 104, 130)
        if 50 < enemy["x"] - game["x"] < 430:
            draw_text("KEEP RUNNING - DO NOT JUMP", font_small, DARK, WIDTH // 2, 112, center=True)
    elif enemy["kind"] == "winged" and route == "wait":
        label = "WAIT - WATCH THE BIRD"
        label_color = (255, 229, 170)
        border = (175, 95, 25)
        if 20 < enemy["x"] - game["x"] < 480:
            draw_text("RELEASE SPACE - WAIT FOR HIGH OR LOW", font_small, RED, WIDTH // 2, 112, center=True)
    else:
        draw_jump_trajectory(enemy, camera_x, marker_x)
        sx = int(marker_x - camera_x)
        gy = int(ground_y(marker_x, game["level"]))
        if -80 < sx < WIDTH + 80:
            active = abs(marker_distance) <= 50
            marker_color = (92, 235, 112) if active else (73, 205, 95)
            dark_marker = (30, 105, 45)
            pg.draw.line(screen, dark_marker, (sx - 38, gy - 2), (sx + 38, gy - 2), 10)
            pg.draw.line(screen, marker_color, (sx - 34, gy - 4), (sx + 34, gy - 4), 6)
            pg.draw.line(screen, dark_marker, (sx, gy - 62), (sx, gy - 18), 5)
            pg.draw.polygon(screen, marker_color, [(sx, gy - 8), (sx - 11, gy - 24), (sx + 11, gy - 24)])

        label = "BIRD LOW - JUMP OVER" if enemy["kind"] == "winged" else "JUMP AT GREEN LINE"
        label_color = (255, 247, 181)
        border = (30, 105, 45)
        if 90 < marker_distance < 430:
            draw_text("GET READY - HOLD SPACE", font_small, DARK, WIDTH // 2, 112, center=True)
        elif -20 <= marker_distance <= 90:
            draw_text("DOUBLE TAP SPACE NOW!", font, RED, WIDTH // 2, 112, center=True)

    # Label above the obstacle, never behind the coin path.
    label_surf = font_small.render(label, True, DARK)
    pad = pg.Rect(0, 0, label_surf.get_width() + 20, 34)
    pad.center = (obstacle_sx, max(68, obstacle_top - 46))
    pg.draw.rect(screen, label_color, pad, border_radius=8)
    pg.draw.rect(screen, border, pad, 2, border_radius=8)
    screen.blit(label_surf, label_surf.get_rect(center=pad.center))


def draw_boosters(camera_x):
    for booster in game["boosters"]:
        if booster["used"]:
            continue
        sx = booster["x"] - camera_x
        if -100 < sx < WIDTH + 100:
            gy = ground_y(booster["x"], game["level"])
            rect = pg.Rect(int(sx - 44), int(gy - 13), 88, 13)
            pg.draw.rect(screen, (255, 139, 35), rect, border_radius=5)
            for offset in (-17, 11):
                pg.draw.polygon(
                    screen,
                    (255, 245, 90),
                    [
                        (int(sx + offset - 10), int(gy - 11)),
                        (int(sx + offset + 12), int(gy - 6)),
                        (int(sx + offset - 10), int(gy - 1)),
                    ],
                )
            if 0 < sx < WIDTH:
                draw_text("BOOST", font_small, (205, 93, 21), int(sx), int(gy - 38), center=True)


def draw_coins(camera_x):
    for coin in game["coins"]:
        if coin["taken"]:
            continue
        sx = coin["x"] - camera_x
        if -60 < sx < WIDTH + 60:
            screen.blit(coin_img, coin_img.get_rect(center=(int(sx), int(coin["y"]))))


def puffer_pulse(enemy):
    """Puffers become more aggressive in later levels."""
    level = game["level"]
    scale_amp = {1: 0.26, 2: 0.30, 3: 0.35, 4: 0.40}[level]
    bob_amp = {1: 12, 2: 15, 3: 18, 4: 22}[level]
    pulse_speed = {1: 4.5, 2: 4.9, 3: 5.4, 4: 5.9}[level]
    bob_speed = {1: 2.8, 2: 3.2, 3: 3.6, 4: 4.0}[level]
    pulse = 1.0 + scale_amp * math.sin(game["level_time"] * pulse_speed + enemy["phase"])
    bob = math.sin(game["level_time"] * bob_speed + enemy["phase"] * 1.35) * bob_amp
    return pulse, bob


def winged_y(enemy, future_time=0.0):
    """Winged enemies sweep from near-road height to high overhead.

    This creates two valid choices: wait for a high pass and run underneath,
    or catch a low pass and jump over it.
    """
    level = game["level"]
    t = game["level_time"] + future_time
    offset = enemy.get("wing_base", 116)
    amp = enemy.get("wing_amp", 70)
    freq = enemy.get("wing_freq", 5.0)
    bob = math.sin(t * freq + enemy["phase"] * 1.15) * amp
    return ground_y(enemy["x"], level) - offset + bob


def enemy_position(enemy):
    level = game["level"]
    x = enemy["x"]
    if enemy["kind"] == "puffer":
        _, bob = puffer_pulse(enemy)
        return x, ground_y(x, level) - 42 + bob
    if enemy["kind"] == "launcher":
        return x, ground_y(x, level) - 31
    return x, winged_y(enemy)


def enemy_draw_image(enemy):
    image = enemy_images[enemy["kind"]]
    if enemy["kind"] != "puffer":
        return image

    pulse, _ = puffer_pulse(enemy)
    width = max(44, int(image.get_width() * pulse))
    height = max(44, int(image.get_height() * pulse))
    return pg.transform.smoothscale(image, (width, height))


def enemy_collision_radius(enemy):
    if enemy["kind"] == "winged":
        return {1: 29, 2: 30, 3: 32, 4: 34}[game["level"]]
    if enemy["kind"] == "puffer":
        pulse, _ = puffer_pulse(enemy)
        return int(30 * pulse)
    return 27


def draw_enemies(camera_x):
    for enemy in game["enemies"]:
        ex, ey = enemy_position(enemy)
        sx = ex - camera_x
        if -120 < sx < WIDTH + 160:
            image = enemy_draw_image(enemy)
            rect = image.get_rect(center=(int(sx), int(ey)))
            screen.blit(image, rect)
            distance = enemy["x"] - game["x"]
            if 180 < distance < 620:
                draw_text("!", font_medium, RED, int(sx), int(ey - image.get_height() // 2 - 25), center=True)

    for projectile in game["projectiles"]:
        sx = projectile["x"] - camera_x
        if -60 < sx < WIDTH + 60:
            if projectile.get("warning", 0.0) > 0:
                pulse = 9 + int(4 * abs(math.sin(game["level_time"] * 12)))
                pg.draw.circle(screen, (235, 72, 55), (int(sx), int(projectile["y"])), pulse, 3)
                draw_text("!", font_small, RED, int(sx), int(projectile["y"] - 28), center=True)
            else:
                rotated = pg.transform.rotate(enemy_images["projectile"], projectile["spin"])
                rect = rotated.get_rect(center=(int(sx), int(projectile["y"])))
                screen.blit(rotated, rect)


def draw_finish_house(camera_x):
    finish_x = LEVELS[game["level"]]["length"]
    sx = finish_x - camera_x
    if -220 < sx < WIDTH + 260:
        gy = ground_y(finish_x, game["level"])
        rect = finish_house.get_rect(midbottom=(int(sx), int(gy + 3)))
        screen.blit(finish_house, rect)
        label_y = max(55, rect.top - 35)
        draw_text("FINISH", font_medium, RED, int(sx), label_y, center=True)


def current_character_frame():
    frames = character_frames[profile["selected_character"]]
    if game["airborne"]:
        return frames[min(1, len(frames) - 1)]
    if (not game["started"]) or game["speed"] < 12:
        return frames[0]
    animation_speed = 5 + game["speed"] / 85
    index = int(game["anim_time"] * animation_speed) % len(frames)
    return frames[index]


def draw_character(camera_x):
    sx = game["x"] - camera_x
    sprite = current_character_frame()
    rotated = pg.transform.rotozoom(sprite, -game["angle"], 1.0)
    rect = rotated.get_rect(center=(int(sx), int(game["y"])))
    screen.blit(rotated, rect)


def draw_hud():
    hud = pg.Surface((445, 155), pg.SRCALPHA)
    hud.fill((255, 255, 255, 185))
    screen.blit(hud, (15, 15))

    screen.blit(coin_small, (29, 29))
    draw_text(f"{game['run_coins']} COINS", font, BLACK, 68, 27)
    draw_text(f"RUN POINTS  {game['run_points']}", font_small, BLACK, 29, 68)
    draw_text(f"TIME  {game['run_time']:.1f}s", font_small, BLACK, 29, 98)
    draw_text(f"SPEED  {int(game['speed'])}", font_small, BLACK, 29, 127)

    level_box = pg.Surface((265, 96), pg.SRCALPHA)
    level_box.fill((255, 255, 255, 185))
    screen.blit(level_box, (WIDTH - 285, 15))
    draw_text(f"LEVEL {game['level']} / {TOTAL_LEVELS}", font, BLACK, WIDTH - 152, 34, center=True)
    draw_text(LEVELS[game["level"]]["name"], font_small, BLACK, WIDTH - 152, 64, center=True)
    draw_text(LEVELS[game["level"]]["difficulty"], font_small, RED, WIDTH - 152, 88, center=True)

    # Progress toward the house / finish line.
    bar = pg.Rect(WIDTH // 2 - 150, 30, 300, 14)
    pg.draw.rect(screen, (255, 255, 255), bar, border_radius=7)
    progress = max(0.0, min(1.0, game["x"] / LEVELS[game["level"]]["length"]))
    fill = pg.Rect(bar.x, bar.y, int(bar.width * progress), bar.height)
    pg.draw.rect(screen, GREEN, fill, border_radius=7)
    pg.draw.rect(screen, DARK, bar, 2, border_radius=7)
    draw_text("HOUSE", font_small, DARK, bar.right + 38, bar.centery + 1, center=True)

    if game["boost_timer"] > 0:
        draw_text("BOOST!", font_medium, (245, 117, 24), WIDTH // 2, 72, center=True)
    if game["jump_flash"] > 0:
        draw_text("JUMP!", font, BLUE, WIDTH // 2, 116, center=True)

    if game["banner_time"] > 0:
        banner = pg.Surface((540, 122), pg.SRCALPHA)
        banner.fill((20, 20, 20, 150))
        rect = banner.get_rect(center=(WIDTH // 2, 210))
        screen.blit(banner, rect)
        draw_text(f"LEVEL {game['level']}", font_medium, WHITE, WIDTH // 2, 177, center=True)
        draw_text(LEVELS[game["level"]]["name"], font, WHITE, WIDTH // 2, 214, center=True)
        draw_text(LEVELS[game["level"]]["difficulty"], font_small, GOLD, WIDTH // 2, 246, center=True)



# --------------------------------------------------
# INTERACTIVE HOW-TO-PLAY TRAINING
# --------------------------------------------------
# This is deliberately interactive instead of an automatic "video".  The
# player must perform the same actions used in the real level before moving on.

def tutorial_selected_frame(moving=False):
    frames = character_frames[profile["selected_character"]]
    if not moving:
        return frames[0]
    return frames[int(tutorial_time * 8) % len(frames)]


def tutorial_reset_demo(message=""):
    global tutorial_demo
    tutorial_demo = {
        "x": 220.0,
        "y": TUTORIAL_FLOOR_Y - PLAYER_HALF_HEIGHT,
        "speed": 0.0,
        "vy": 0.0,
        "airborne": False,
        "last_tap_ms": -9999,
        "success": False,
        "success_time": 0.0,
        "message": message,
        "message_time": 1.7 if message else 0.0,
        "projectile_x": None,
        "projectile_warning": 0.0,
        "projectile_fired": False,
        "projectile_dodged": False,
    }


def tutorial_advance_after_success(dt):
    global tutorial_step, tutorial_time
    if not tutorial_demo.get("success"):
        return
    tutorial_demo["success_time"] += dt
    if tutorial_demo["success_time"] >= TUTORIAL_SUCCESS_DELAY:
        tutorial_step += 1
        tutorial_time = 0.0
        tutorial_reset_demo()


def tutorial_fail(message):
    tutorial_reset_demo(message)


def tutorial_success(message="GOOD!"):
    if not tutorial_demo.get("success"):
        tutorial_demo["success"] = True
        tutorial_demo["success_time"] = 0.0
        tutorial_demo["message"] = message
        tutorial_demo["message_time"] = 99.0


def tutorial_jump():
    config = LEVELS[1]
    if tutorial_demo["airborne"]:
        return
    tutorial_demo["airborne"] = True
    tutorial_demo["speed"] = max(tutorial_demo["speed"], config["jump_forward_min"])
    tutorial_demo["vy"] = -config["jump_power"]


def tutorial_handle_space_keydown():
    """Use the same double-tap timing as the real game."""
    global state, game
    if tutorial_step == TUTORIAL_LAST_STEP:
        start_new_run()
        return

    # Movement practice does not use jumping.
    if tutorial_step == 0:
        return

    now = pg.time.get_ticks()
    if now - tutorial_demo.get("last_tap_ms", -9999) <= DOUBLE_TAP_MS:
        if not tutorial_demo["airborne"]:
            # Give useful timing feedback in the puffer lesson.
            if tutorial_step == 1:
                marker_x = 690
                if tutorial_demo["x"] < marker_x - 55:
                    tutorial_demo["message"] = "TOO EARLY - WAIT FOR THE GREEN LINE"
                    tutorial_demo["message_time"] = 1.2
                elif tutorial_demo["x"] > marker_x + 55:
                    tutorial_demo["message"] = "TOO LATE - JUMP AT THE GREEN LINE"
                    tutorial_demo["message_time"] = 1.2
                else:
                    tutorial_demo["message"] = "GOOD TIMING!"
                    tutorial_demo["message_time"] = 1.0
            tutorial_jump()
        tutorial_demo["last_tap_ms"] = -9999
    else:
        tutorial_demo["last_tap_ms"] = now


def draw_tutorial_base(title, instruction):
    screen.blit(level_backgrounds[1], (0, 0))
    veil = pg.Surface((WIDTH, HEIGHT), pg.SRCALPHA)
    veil.fill((245, 238, 215, 135))
    screen.blit(veil, (0, 0))

    outer = pg.Rect(55, 35, 1170, 650)
    draw_panel(outer, color=(251, 244, 222, 244), border=(92, 68, 48))
    draw_text("LEVEL 1 - HOW TO PLAY", font_small, PURPLE, WIDTH // 2, 65, center=True)
    draw_text(title, font_medium, DARK, WIDTH // 2, 105, center=True)

    info = pg.Rect(155, 135, 970, 64)
    pg.draw.rect(screen, (255, 250, 224), info, border_radius=10)
    pg.draw.rect(screen, (132, 102, 66), info, 2, border_radius=10)
    draw_text(instruction, font, DARK, WIDTH // 2, 167, center=True)

    # Flat practice road so the controls are easy to understand before hills.
    pg.draw.rect(screen, (170, 107, 59), (130, TUTORIAL_FLOOR_Y, 1020, 100))
    pg.draw.line(screen, (62, 180, 92), (130, TUTORIAL_FLOOR_Y), (1150, TUTORIAL_FLOOR_Y), 14)

    for i in range(TUTORIAL_LAST_STEP + 1):
        color = GREEN if i == tutorial_step else (185, 170, 145)
        pg.draw.circle(screen, color, (550 + i * 45, 650), 8)

    draw_text("S = SKIP INTRO", font_small, BLUE, 205, 650, center=True)
    draw_text("ESC = HOME", font_small, GRAY, 1080, 650, center=True)

    if tutorial_demo.get("message") and tutorial_demo.get("message_time", 0) > 0:
        color = GREEN if tutorial_demo.get("success") or "GOOD" in tutorial_demo["message"] else RED
        msg = tutorial_demo["message"]
        surf = font.render(msg, True, color)
        box = surf.get_rect(center=(WIDTH // 2, 225)).inflate(28, 16)
        pg.draw.rect(screen, (255, 252, 230), box, border_radius=9)
        pg.draw.rect(screen, color, box, 2, border_radius=9)
        screen.blit(surf, surf.get_rect(center=box.center))


def draw_tutorial_player():
    moving = tutorial_demo["airborne"] or tutorial_demo["speed"] > 12
    sprite = tutorial_selected_frame(moving)
    rect = sprite.get_rect(center=(int(tutorial_demo["x"]), int(tutorial_demo["y"])))
    screen.blit(sprite, rect)


def draw_tutorial_jump_arc(start_x, obstacle_x):
    """Show the safe shape of the jump without hiding the obstacle."""
    for i in range(13):
        t = i / 12.0
        x = start_x + (obstacle_x + 145 - start_x) * t
        y = (TUTORIAL_FLOOR_Y - PLAYER_HALF_HEIGHT) - math.sin(t * math.pi) * 170
        pg.draw.circle(screen, (255, 222, 65), (int(x), int(y)), 5)


def draw_tutorial():
    t = tutorial_time

    if tutorial_step == 0:
        draw_tutorial_base(
            "1. RUN AND STOP",
            "HOLD SPACE to run. RELEASE SPACE and stop inside the green box.",
        )
        stop_zone = pg.Rect(735, TUTORIAL_FLOOR_Y - 18, 150, 25)
        pg.draw.rect(screen, (79, 205, 105), stop_zone, border_radius=8)
        pg.draw.rect(screen, (35, 113, 55), stop_zone, 3, border_radius=8)
        draw_text("STOP HERE", font_small, GREEN, stop_zone.centerx, 445, center=True)
        draw_text("HOLD SPACE", font_small, BLUE, 330, 390, center=True)
        draw_text("RELEASE BEFORE THE BOX", font_small, RED, 650, 390, center=True)
        draw_tutorial_player()

    elif tutorial_step == 1:
        draw_tutorial_base(
            "2. PUFFER - JUMP TIMING",
            "HOLD SPACE to approach. DOUBLE TAP exactly at the green line.",
        )
        marker_x = 690
        puffer_x = 850
        # Real enemy motion: size and height change while you approach.
        scale = 1.0 + 0.28 * math.sin(t * 4.6)
        bob = math.sin(t * 3.0) * 14
        puffer = pg.transform.smoothscale(enemy_images["puffer"], (int(82 * scale), int(82 * scale)))
        puffer_y = TUTORIAL_FLOOR_Y - 39 + bob
        screen.blit(puffer, puffer.get_rect(center=(puffer_x, int(puffer_y))))

        pg.draw.line(screen, (35, 113, 55), (marker_x, TUTORIAL_FLOOR_Y - 55), (marker_x, TUTORIAL_FLOOR_Y + 5), 12)
        pg.draw.line(screen, (72, 225, 104), (marker_x, TUTORIAL_FLOOR_Y - 55), (marker_x, TUTORIAL_FLOOR_Y + 5), 7)
        draw_text("DOUBLE TAP HERE", font_small, GREEN, marker_x, 405, center=True)
        draw_tutorial_jump_arc(marker_x, puffer_x)
        draw_text("PUFFER", font_small, RED, puffer_x, 365, center=True)
        draw_tutorial_player()

    elif tutorial_step == 2:
        draw_tutorial_base(
            "3. BIRD - CHOOSE YOUR ROUTE",
            "Watch the bird first. HIGH = run under. LOW = jump over. MIDDLE = stop and wait.",
        )
        bird_x = 850
        bird_y = 345 + math.sin(t * 5.3) * 105
        bird = pg.transform.smoothscale(enemy_images["winged"], (150, 78))
        screen.blit(bird, bird.get_rect(center=(bird_x, int(bird_y))))

        decision = pg.Rect(540, TUTORIAL_FLOOR_Y - 15, 120, 20)
        pg.draw.rect(screen, (89, 194, 224), decision, border_radius=6)
        draw_text("WATCH HERE", font_small, BLUE, decision.centerx, 445, center=True)

        if bird_y < 315:
            draw_text("BIRD HIGH -> HOLD SPACE, RUN UNDER", font, GREEN, WIDTH // 2, 265, center=True)
            for x in range(680, 1010, 45):
                pg.draw.circle(screen, (80, 225, 245), (x, TUTORIAL_FLOOR_Y - PLAYER_HALF_HEIGHT), 5)
        elif bird_y > 395:
            draw_text("BIRD LOW -> DOUBLE TAP AT GREEN LINE", font, PURPLE, WIDTH // 2, 265, center=True)
            marker_x = 690
            pg.draw.line(screen, (35, 113, 55), (marker_x, TUTORIAL_FLOOR_Y - 55), (marker_x, TUTORIAL_FLOOR_Y + 5), 12)
            pg.draw.line(screen, (72, 225, 104), (marker_x, TUTORIAL_FLOOR_Y - 55), (marker_x, TUTORIAL_FLOOR_Y + 5), 7)
            draw_tutorial_jump_arc(marker_x, bird_x)
        else:
            draw_text("BIRD IN THE MIDDLE -> RELEASE SPACE AND WAIT", font, RED, WIDTH // 2, 265, center=True)

        draw_tutorial_player()

    elif tutorial_step == 3:
        draw_tutorial_base(
            "4. LAUNCHER - READ THE WARNING",
            "When you see !, release if needed to control timing, then DOUBLE TAP to jump the shot.",
        )
        launcher_x = 980
        launcher = pg.transform.smoothscale(enemy_images["launcher"], (78, 82))
        screen.blit(launcher, launcher.get_rect(center=(launcher_x, TUTORIAL_FLOOR_Y - 40)))
        draw_text("LAUNCHER", font_small, RED, launcher_x, 385, center=True)

        if tutorial_demo["projectile_warning"] > 0:
            pulse = 20 + int(4 * abs(math.sin(t * 12)))
            pg.draw.circle(screen, RED, (930, 435), pulse, 3)
            draw_text("!", font_medium, RED, 930, 435, center=True)
            draw_text("WARNING -> GET READY", font, RED, WIDTH // 2, 275, center=True)
        elif tutorial_demo["projectile_x"] is not None:
            projectile = pg.transform.rotate(enemy_images["projectile"], t * 300)
            py = TUTORIAL_FLOOR_Y - 58
            screen.blit(projectile, projectile.get_rect(center=(int(tutorial_demo["projectile_x"]), py)))
            draw_text("PROJECTILE -> DOUBLE TAP TO JUMP IT", font, PURPLE, WIDTH // 2, 275, center=True)
        else:
            draw_text("HOLD SPACE TO APPROACH THE LAUNCHER", font, BLUE, WIDTH // 2, 275, center=True)

        finish = pg.Rect(790, TUTORIAL_FLOOR_Y - 12, 85, 17)
        pg.draw.rect(screen, GREEN, finish, border_radius=5)
        draw_text("SAFE", font_small, GREEN, finish.centerx, 455, center=True)
        draw_tutorial_player()

    else:
        draw_tutorial_base(
            "YOU ARE READY",
            "You completed the controls and every enemy practice. Level 1 starts at moderate difficulty.",
        )
        draw_text("REMEMBER", font_medium, DARK, WIDTH // 2, 280, center=True)
        draw_text("HOLD = RUN     RELEASE = STOP     DOUBLE TAP = JUMP", font, BLUE, WIDTH // 2, 335, center=True)
        draw_text("PUFFER: jump at the green line", font, DARK, WIDTH // 2, 390, center=True)
        draw_text("BIRD: high -> under   |   low -> over   |   middle -> wait", font, DARK, WIDTH // 2, 430, center=True)
        draw_text("LAUNCHER: watch the ! warning and dodge the shot", font, DARK, WIDTH // 2, 470, center=True)
        draw_text("PRESS SPACE TO START LEVEL 1", font_medium, GREEN, WIDTH // 2, 555, center=True)


def tutorial_update_motion(dt, allow_jump=True):
    config = LEVELS[1]
    keys = pg.key.get_pressed()
    space = keys[pg.K_SPACE]

    if tutorial_demo["airborne"]:
        # Keep horizontal momentum in the air, exactly like the real game.
        tutorial_demo["speed"] = max(tutorial_demo["speed"], config["jump_forward_min"])
        tutorial_demo["vy"] += config["gravity"] * dt
        tutorial_demo["y"] += tutorial_demo["vy"] * dt
        if tutorial_demo["y"] + PLAYER_RADIUS >= TUTORIAL_FLOOR_Y and tutorial_demo["vy"] > 0:
            tutorial_demo["airborne"] = False
            tutorial_demo["y"] = TUTORIAL_FLOOR_Y - PLAYER_HALF_HEIGHT
            tutorial_demo["vy"] = 0.0
    else:
        if space:
            tutorial_demo["speed"] += 165.0 * dt
        else:
            tutorial_demo["speed"] -= 420.0 * dt
            if tutorial_demo["speed"] < 15:
                tutorial_demo["speed"] = 0.0
        tutorial_demo["speed"] = max(0.0, min(275.0, tutorial_demo["speed"]))

    tutorial_demo["x"] += tutorial_demo["speed"] * dt


def update_tutorial(dt):
    global tutorial_time
    if state != "tutorial":
        return

    tutorial_time += dt
    tutorial_demo["message_time"] = max(0.0, tutorial_demo.get("message_time", 0.0) - dt)

    if tutorial_step == TUTORIAL_LAST_STEP:
        return

    if tutorial_demo.get("success"):
        tutorial_demo["speed"] = 0.0
        tutorial_advance_after_success(dt)
        return

    tutorial_update_motion(dt)

    if tutorial_step == 0:
        # The task is complete only when the player actually comes to rest.
        if 735 <= tutorial_demo["x"] <= 885 and tutorial_demo["speed"] == 0:
            tutorial_success("PERFECT - YOU CAN CONTROL YOUR SPEED")
        elif tutorial_demo["x"] > 930:
            tutorial_fail("TOO FAR - RELEASE SPACE EARLIER")

    elif tutorial_step == 1:
        puffer_x = 850
        scale = 1.0 + 0.28 * math.sin(tutorial_time * 4.6)
        bob = math.sin(tutorial_time * 3.0) * 14
        puffer_y = TUTORIAL_FLOOR_Y - 39 + bob
        radius = 31 * scale
        dx = tutorial_demo["x"] - puffer_x
        dy = tutorial_demo["y"] - puffer_y
        if dx * dx + dy * dy < (PLAYER_RADIUS + radius) ** 2:
            tutorial_fail("HIT! DOUBLE TAP AT THE GREEN LINE")
            return
        if tutorial_demo["x"] > puffer_x + 145 and not tutorial_demo["airborne"]:
            tutorial_success("CLEAR! THAT IS THE JUMP TIMING USED IN THE GAME")
        elif tutorial_demo["x"] > 1090:
            tutorial_fail("TRY AGAIN - USE THE GREEN LINE")

    elif tutorial_step == 2:
        bird_x = 850
        bird_y = 345 + math.sin(tutorial_time * 5.3) * 105
        dx = tutorial_demo["x"] - bird_x
        dy = tutorial_demo["y"] - bird_y
        if dx * dx + dy * dy < (PLAYER_RADIUS + 38) ** 2:
            tutorial_fail("HIT! WATCH THE BIRD HEIGHT BEFORE MOVING")
            return
        if tutorial_demo["x"] > bird_x + 145:
            tutorial_success("CLEAR! HIGH = UNDER, LOW = OVER")
        elif tutorial_demo["x"] > 1100:
            tutorial_fail("TRY AGAIN - WAIT FOR A SAFE BIRD POSITION")

    elif tutorial_step == 3:
        # Fire once the player is close enough to clearly see the warning.
        if not tutorial_demo["projectile_fired"] and tutorial_demo["x"] > 430:
            tutorial_demo["projectile_fired"] = True
            tutorial_demo["projectile_warning"] = 0.85
            tutorial_demo["projectile_x"] = 930.0

        if tutorial_demo["projectile_warning"] > 0:
            tutorial_demo["projectile_warning"] = max(0.0, tutorial_demo["projectile_warning"] - dt)
        elif tutorial_demo["projectile_x"] is not None and not tutorial_demo["projectile_dodged"]:
            tutorial_demo["projectile_x"] -= 265.0 * dt
            py = TUTORIAL_FLOOR_Y - 58
            dx = tutorial_demo["x"] - tutorial_demo["projectile_x"]
            dy = tutorial_demo["y"] - py
            if dx * dx + dy * dy < (PLAYER_RADIUS + 14) ** 2:
                tutorial_fail("HIT! USE THE ! WARNING TO PREPARE")
                return
            if tutorial_demo["projectile_x"] < tutorial_demo["x"] - 80:
                tutorial_demo["projectile_dodged"] = True
                tutorial_demo["message"] = "SHOT DODGED - NOW REACH THE GREEN SAFE ZONE"
                tutorial_demo["message_time"] = 2.0

        if tutorial_demo["projectile_dodged"] and 790 <= tutorial_demo["x"] <= 900:
            tutorial_success("CLEAR! YOU READ THE WARNING AND DODGED")
        elif tutorial_demo["x"] > 925:
            tutorial_fail("DON'T RUN INTO THE LAUNCHER - DODGE, THEN STOP IN SAFE")

    tutorial_advance_after_success(dt)


def start_tutorial():
    global tutorial_step, tutorial_time, state, game
    game = new_level_state(1)
    tutorial_step = 0
    tutorial_time = 0.0
    tutorial_reset_demo()
    state = "tutorial"


def draw_game():
    camera_x = game["x"] - 280
    screen.blit(level_backgrounds[game["level"]], (0, 0))
    draw_road(camera_x)
    draw_boosters(camera_x)
    draw_finish_house(camera_x)
    draw_coins(camera_x)
    draw_enemies(camera_x)
    draw_jump_hints(camera_x)
    draw_character(camera_x)
    draw_hud()

    if not game["started"] and state == "game":
        box = pg.Surface((560, 120), pg.SRCALPHA)
        box.fill((20, 20, 20, 175))
        rect = box.get_rect(center=(WIDTH // 2, 315))
        screen.blit(box, rect)
        draw_text("PRESS SPACE TO START", font_medium, WHITE, WIDTH // 2, 292, center=True)
        draw_text("Hold SPACE to run  |  Follow JUMP HERE markers", font_small, WHITE, WIDTH // 2, 336, center=True)


def draw_game_over():
    draw_game()
    overlay = pg.Surface((WIDTH, HEIGHT), pg.SRCALPHA)
    overlay.fill((0, 0, 0, 150))
    screen.blit(overlay, (0, 0))

    box = pg.Rect(355, 145, 570, 450)
    draw_panel(box, color=(250, 239, 210, 248), border=(90, 63, 43))
    draw_text("GAME OVER", font_big, RED, WIDTH // 2, 205, center=True)
    draw_text(game["death_reason"], font, DARK, WIDTH // 2, 278, center=True)
    draw_text(f"Level reached: {game['level']}", font, DARK, WIDTH // 2, 330, center=True)
    draw_text(f"Run points: {game['run_points']}", font, DARK, WIDTH // 2, 375, center=True)
    draw_text(f"Survival time: {game['run_time']:.1f} sec", font, DARK, WIDTH // 2, 420, center=True)
    draw_text(f"Saved total points: {profile['points']}", font, DARK, WIDTH // 2, 470, center=True)
    draw_text("R = restart this level", font, BLUE, WIDTH // 2, 535, center=True)
    draw_text("ESC = home", font_small, GRAY, WIDTH // 2, 570, center=True)


def draw_level_complete():
    draw_game()
    overlay = pg.Surface((WIDTH, HEIGHT), pg.SRCALPHA)
    overlay.fill((0, 0, 0, 125))
    screen.blit(overlay, (0, 0))

    box = pg.Rect(365, 165, 550, 390)
    draw_panel(box, color=(242, 249, 222, 248), border=(72, 135, 67))
    draw_text("LEVEL COMPLETE!", font_big, GREEN, WIDTH // 2, 225, center=True)
    draw_text(f"Level {game['level']} cleared", font, DARK, WIDTH // 2, 305, center=True)
    draw_text(f"Run points: {game['run_points']}", font, DARK, WIDTH // 2, 355, center=True)
    draw_text(f"Run time: {game['run_time']:.1f} sec", font, DARK, WIDTH // 2, 400, center=True)
    draw_text(f"NEXT: LEVEL {game['level'] + 1}", font_medium, BLUE, WIDTH // 2, 470, center=True)
    draw_text("Press SPACE to continue", font, DARK, WIDTH // 2, 520, center=True)


def draw_victory():
    draw_game()
    overlay = pg.Surface((WIDTH, HEIGHT), pg.SRCALPHA)
    overlay.fill((0, 0, 0, 135))
    screen.blit(overlay, (0, 0))

    box = pg.Rect(330, 135, 620, 485)
    draw_panel(box, color=(255, 241, 184, 250), border=(160, 115, 37))
    draw_text("HILL RUSH COMPLETE!", font_big, GOLD, WIDTH // 2, 205, center=True)
    draw_text("YOU CLEARED ALL 4 LEVELS", font, DARK, WIDTH // 2, 285, center=True)
    draw_text(f"Coins collected: {game['run_coins']}", font, DARK, WIDTH // 2, 350, center=True)
    draw_text(f"Points earned: {game['run_points']}", font, DARK, WIDTH // 2, 395, center=True)
    draw_text(f"Total time: {game['run_time']:.1f} sec", font, DARK, WIDTH // 2, 440, center=True)
    draw_text(f"Saved points: {profile['points']}", font, DARK, WIDTH // 2, 485, center=True)
    draw_text("R = PLAY AGAIN", font, BLUE, WIDTH // 2, 548, center=True)
    draw_text("ESC = HOME", font_small, GRAY, WIDTH // 2, 582, center=True)


# --------------------------------------------------
# GAME LOGIC
# --------------------------------------------------
def bank_current_level_points():
    if game["banked"]:
        return
    profile["points"] += game["level_points"]
    game["banked"] = True
    save_profile()


def update_best_time():
    if game["run_time"] > profile["best_time"]:
        profile["best_time"] = round(game["run_time"], 2)
        save_profile()


def start_new_run():
    global game, state
    game = new_level_state(1)
    state = "game"


def retry_current_level():
    global game, state
    # Points from the failed attempt were already banked. Retry starts the
    # same level but keeps the run's previous completed-level total/time.
    carried_points = game["run_points"] - game["level_points"]
    carried_coins = game["run_coins"] - game["level_coins"]
    carried_time = max(0.0, game["run_time"] - game["level_time"])
    game = new_level_state(game["level"], carried_time, carried_points, carried_coins)
    state = "game"


def trigger_game_over(reason):
    global state
    game["death_reason"] = reason
    bank_current_level_points()
    update_best_time()
    audio.play_sfx("game_over")
    state = "gameover"


def complete_level():
    global state
    bank_current_level_points()
    profile["levels_cleared"] = max(profile["levels_cleared"], game["level"])
    update_best_time()
    save_profile()

    if game["level"] >= TOTAL_LEVELS:
        state = "victory"
    else:
        state = "levelcomplete"


def advance_level():
    global game, state
    next_level = game["level"] + 1
    game = new_level_state(
        next_level,
        run_time=game["run_time"],
        run_points=game["run_points"],
        run_coins=game["run_coins"],
    )
    state = "game"


def handle_game_space_keydown():
    now = pg.time.get_ticks()

    # A level begins completely stopped. The first SPACE press starts the run.
    if not game["started"]:
        game["started"] = True
        game["last_tap_ms"] = now
        audio.play_sfx("start")
        return

    if not game["airborne"] and now - game["last_tap_ms"] <= DOUBLE_TAP_MS:
        config = LEVELS[game["level"]]
        game["airborne"] = True

        # Normal jump keeps momentum.  If the player double-taps inside the
        # visible take-off zone, apply a small physics correction so the hint
        # is genuinely trustworthy rather than decorative.
        guided_enemy = guided_enemy_for_jump()
        if guided_enemy is not None:
            game["speed"] = max(game["speed"], recommended_jump_speed(guided_enemy))
        else:
            game["speed"] = max(game["speed"], config["jump_forward_min"])

        slope_bonus = max(0.0, -road_slope(game["x"], game["level"])) * 55
        speed_bonus = max(0.0, game["speed"] - config["start_speed"]) * 0.18
        base_vy = -(config["jump_power"] + min(80, slope_bonus + speed_bonus))

        if guided_enemy is not None:
            distance_x = max(35.0, guided_enemy["x"] - game["x"])
            time_to_enemy = distance_x / max(1.0, game["speed"])
            safe_y = guided_safe_height(guided_enemy)
            required_vy = (safe_y - game["y"] - 0.5 * config["gravity"] * time_to_enemy ** 2) / time_to_enemy
            # The hint helps, but does not auto-win the jump. Give only a
            # small correction so timing and approach speed still matter.
            desired_vy = required_vy - 14.0
            game["vy"] = min(base_vy, max(desired_vy, base_vy - 42.0))
        else:
            game["vy"] = base_vy

        game["jump_flash"] = 0.25
        game["last_tap_ms"] = -9999
    else:
        game["last_tap_ms"] = now


def spawn_projectiles():
    level = game["level"]

    for enemy in game["enemies"]:
        if enemy["kind"] != "launcher":
            continue

        distance = enemy["x"] - game["x"]
        # Launchers only fire once the player can clearly see them.
        cooldown = {1: 2.00, 2: 1.78, 3: 1.58, 4: 1.42}[level]
        if 240 < distance < 590 and game["level_time"] - enemy["last_shot"] >= cooldown:
            _, ey = enemy_position(enemy)
            game["projectiles"].append({
                "x": enemy["x"] - 18,
                "y": ey - 4,
                "vx": -LEVELS[level]["projectile_speed"],
                "spin": 0.0,
                "warning": max(0.32, PROJECTILE_WARNING_TIME - (level - 1) * 0.04),
            })
            enemy["last_shot"] = game["level_time"]


def update_projectiles(dt):
    for projectile in game["projectiles"]:
        if projectile.get("warning", 0.0) > 0:
            projectile["warning"] = max(0.0, projectile["warning"] - dt)
        else:
            projectile["x"] += projectile["vx"] * dt
            projectile["spin"] = (projectile["spin"] + 420 * dt) % 360

    game["projectiles"] = [p for p in game["projectiles"] if p["x"] > game["x"] - 500]


def check_enemy_collisions():
    px, py = game["x"], game["y"]

    for enemy in game["enemies"]:
        ex, ey = enemy_position(enemy)
        dx = px - ex
        dy = py - ey
        radius = enemy_collision_radius(enemy)

        if dx * dx + dy * dy < (PLAYER_RADIUS + radius) ** 2:
            if enemy["kind"] == "puffer":
                trigger_game_over("You hit the puffer enemy!")
            elif enemy["kind"] == "launcher":
                trigger_game_over("You crashed into the launcher!")
            else:
                trigger_game_over("You hit the flying enemy!")
            return True

    for projectile in game["projectiles"]:
        if projectile.get("warning", 0.0) > 0:
            continue
        dx = px - projectile["x"]
        dy = py - projectile["y"]
        if dx * dx + dy * dy < (PLAYER_RADIUS + 12) ** 2:
            trigger_game_over("You were hit by a projectile!")
            return True

    return False


def update_game(dt):
    if state != "game":
        return

    config = LEVELS[game["level"]]
    keys = pg.key.get_pressed()
    space = keys[pg.K_SPACE]

    # The timer and movement begin only after the player presses SPACE.
    if game["started"]:
        game["level_time"] += dt
        game["run_time"] += dt
        if game["airborne"] or game["speed"] > 15:
            game["anim_time"] += dt * (0.65 + game["speed"] / 180.0)

    game["banner_time"] = max(0.0, game["banner_time"] - dt)
    game["jump_flash"] = max(0.0, game["jump_flash"] - dt)
    game["boost_timer"] = max(0.0, game["boost_timer"] - dt)

    effective_max = config["max_speed"] + (config["booster_bonus"] if game["boost_timer"] > 0 else 0)

    if not game["started"]:
        game["speed"] = 0.0
    elif game["airborne"]:
        # Do not remove horizontal momentum during the release needed for a
        # double-tap jump. This is what makes obstacles clearable with one key.
        game["speed"] = min(game["speed"], effective_max)
    else:
        # On the ground SPACE is the throttle. Releasing it now brings the
        # character all the way to a stop instead of forcing an automatic run.
        if space:
            accel = config["acceleration"] * (1.28 if game["speed"] < 80 else 1.0)
            game["speed"] += accel * dt
        else:
            game["speed"] -= config["deceleration"] * dt
            if game["speed"] < 18:
                game["speed"] = 0.0
        game["speed"] = max(0.0, min(game["speed"], effective_max))

    game["x"] += game["speed"] * dt

    if not game["airborne"]:
        game["y"] = ground_y(game["x"], game["level"]) - PLAYER_HALF_HEIGHT
        target_angle = road_angle(game["x"], game["level"]) * 0.24
        game["angle"] += (target_angle - game["angle"]) * min(1.0, dt * 10.0)
    else:
        game["vy"] += config["gravity"] * dt
        game["y"] += game["vy"] * dt

        target_angle = max(-9, min(9, road_angle(game["x"], game["level"]) * 0.10))
        game["angle"] += (target_angle - game["angle"]) * min(1.0, dt * 5.5)

        gy = ground_y(game["x"], game["level"])
        if game["y"] + PLAYER_RADIUS >= gy and game["vy"] > 0:
            # Very hard landings still kill the player, but normal jumps are forgiving.
            if game["vy"] > 825 + game["level"] * 25:
                trigger_game_over("Hard landing!")
                return
            game["airborne"] = False
            game["y"] = gy - PLAYER_HALF_HEIGHT
            game["vy"] = 0.0
            game["angle"] = road_angle(game["x"], game["level"]) * 0.24
            game["speed"] *= 0.985

    # Coins: each coin adds 10 spendable points.
    for coin in game["coins"]:
        if coin["taken"]:
            continue
        dx = game["x"] - coin["x"]
        dy = game["y"] - coin["y"]
        if dx * dx + dy * dy < 47 * 47:
            coin["taken"] = True
            game["level_coins"] += 1
            game["run_coins"] += 1
            game["level_points"] += COIN_VALUE
            game["run_points"] += COIN_VALUE
            audio.play_sfx("coin")

    # Boosters.
    if not game["airborne"]:
        for booster in game["boosters"]:
            if booster["used"]:
                continue
            if abs(game["x"] - booster["x"]) < 44:
                booster["used"] = True
                game["boost_timer"] = BOOST_TIME
                boosted_max = config["max_speed"] + config["booster_bonus"]
                # Bring a slow player up to a designed useful speed; do not punish an
                # already-fast player with an uncontrollable speed spike.
                game["speed"] = min(boosted_max, max(game["speed"], config["booster_target"]))
                audio.play_sfx("booster")

    spawn_projectiles()
    update_projectiles(dt)

    if check_enemy_collisions():
        return

    # House is the finish line.
    if game["x"] >= config["length"] - 35:
        complete_level()
        return

    if game["y"] > HEIGHT + 120:
        trigger_game_over("You fell off the road!")


# --------------------------------------------------
# INPUT / MAIN LOOP
# --------------------------------------------------
running = True
while running:
    dt = clock.tick(FPS) / 1000.0

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                if state in ("characters", "music", "tutorial"):
                    state = "menu"
                elif state == "game":
                    # Keep collected points before leaving the level.
                    bank_current_level_points()
                    update_best_time()
                    state = "menu"
                elif state in ("gameover", "levelcomplete", "victory"):
                    state = "menu"
                else:
                    running = False

            if event.key == pg.K_SPACE:
                if state == "tutorial":
                    tutorial_handle_space_keydown()
                elif state == "game":
                    handle_game_space_keydown()
                elif state == "levelcomplete":
                    advance_level()

            if event.key == pg.K_r:
                if state == "gameover":
                    retry_current_level()
                elif state == "victory":
                    start_new_run()

            if event.key == pg.K_s and state == "tutorial":
                start_new_run()

        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            pos = event.pos

            if state == "menu":
                if menu_start.clicked(pos):
                    start_tutorial()
                elif menu_char.clicked(pos):
                    state = "characters"
                elif menu_music.clicked(pos):
                    state = "music"
                elif menu_quit.clicked(pos):
                    running = False
                else:
                    for i, button in enumerate(menu_bg_buttons):
                        if button.clicked(pos):
                            profile["music_track"] = i
                            save_profile()
                            audio.apply_music()
                            break

            elif state == "characters":
                if back_button.clicked(pos):
                    state = "menu"
                else:
                    handle_character_click(pos)

            elif state == "music":
                if back_button.clicked(pos):
                    state = "menu"
                elif music_toggle.clicked(pos):
                    profile["music_enabled"] = not profile["music_enabled"]
                    save_profile()
                    audio.apply_music()
                else:
                    for i, button in enumerate(music_track_buttons):
                        if button.clicked(pos):
                            profile["music_track"] = i
                            save_profile()
                            audio.apply_music()
                            break

    update_tutorial(dt)
    update_game(dt)

    if state == "menu":
        draw_main_menu()
    elif state == "characters":
        draw_character_select()
    elif state == "music":
        draw_music_menu()
    elif state == "tutorial":
        draw_tutorial()
    elif state == "game":
        draw_game()
    elif state == "gameover":
        draw_game_over()
    elif state == "levelcomplete":
        draw_level_complete()
    elif state == "victory":
        draw_victory()

    pg.display.flip()

save_profile()
pg.quit()
sys.exit()
