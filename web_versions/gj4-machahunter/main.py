# --- Web版 (pygbag対応のための変換コピー / ゲーム内容は変更していません) ---
import asyncio
import random
import sys
import pygame as pg

pg.init()
try:
    pg.mixer.init()
except pg.error:
    pass

WIDTH, HEIGHT = 900, 600
FPS, GAME_LENGTH = 60, 60
WATER_TOP, WATER_BOTTOM = 250, 520
POINTS_PER_LEVEL = 20
HIGH_SCORE_FILE = "highscore.txt"

# HOOK SPEED SETTINGS -------------------------------------------------------
# Change these two values before starting the game to set its initial speed.
# The values are pixels per frame (the game runs at 60 FPS).
HOOK_SWING_SPEED = 8.0       # Left/right swing speed
HOOK_VERTICAL_SPEED = 8.0    # Downward and reeling speed

# In-game adjustment amount. [ and ] change swing speed; , and . change
# vertical speed while playing.
HOOK_SPEED_STEP = 1.0
MIN_HOOK_SPEED = 1.0

screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Fishing Game")
clock = pg.time.Clock()

BLACK, WHITE = (20, 20, 20), (255, 255, 255)
SKY, WATER = (120, 200, 255), (35, 120, 190)
RED, YELLOW, GREEN, BROWN, SKIN, GOLD = (
    220, 60, 60), (245, 205, 40), (50, 180, 80), (130, 80, 35), (255, 210, 170), (255, 215, 60)
font_sm, font_md, font_lg = pg.font.Font(
    None, 30), pg.font.Font(None, 40), pg.font.Font(None, 72)


def load_image(path, size=None):
    try:
        image = pg.image.load(path).convert_alpha()
        return pg.transform.scale(image, size) if size else image
    except (FileNotFoundError, pg.error):
        return None


def load_sound(path):
    try:
        return pg.mixer.Sound(path)
    except (FileNotFoundError, pg.error):
        return None


def start_music(path):
    try:
        pg.mixer.music.load(path)
        pg.mixer.music.play(-1)
    except (FileNotFoundError, pg.error):
        pass


def stop_music():
    if pg.mixer.get_init():
        pg.mixer.music.stop()


def load_high_score():
    try:
        with open(HIGH_SCORE_FILE, "r") as file:
            return max(0, int(file.read().strip()))
    except (FileNotFoundError, ValueError, OSError):
        return 0


def save_high_score(score):
    try:
        with open(HIGH_SCORE_FILE, "w") as file:
            file.write(str(score))
    except OSError:
        pass


IMG_BG = load_image("background.png", (WIDTH, HEIGHT))
IMG_BOAT = load_image("boat.png", (180, 75))
IMG_HOOK = load_image("hook.png", (36, 40))
FISH_IMAGES = {
    "Common": load_image("ONE.png", (65, 65)),
    "Rare": load_image("TWO.png", (65, 65)),
    "Legendary": load_image("THREE.png", (65, 65)),
    "Shark": load_image("FOUR.png", (95, 65)),
}
SFX_CATCH = load_sound("catch.wav")


def load_first_sound(*paths):
    """Use hook_drop.wav or hook_drop.mp3 when the player adds either file."""
    for path in paths:
        sound = load_sound(path)
        if sound:
            return sound
    return None


SFX_DROP = load_first_sound("hook_drop.wav", "hook_drop.ogg", "hook1.ogg")

# Change only the first text in each row to set the fixed in-game character name.
CHARACTERS = [
    ("ROBO", "person.png"),
    ("Angry Fisher", "chara2.png"),
    ("BUNNY GIRL", "chara3.png"),
]
BGMS = [
    ("Ocean Adventure", "game2.ogg"),
    ("Calm Water", "2.ogg"),
]
CHARACTER_IMAGES = [load_image(path, (70, 70)) for _, path in CHARACTERS]


class Fish:
    TYPES = {
        "Common": (1, (2, 3), (65, 65), YELLOW),
        "Rare": (3, (3, 5), (65, 65), (80, 160, 240)),
        "Legendary": (10, (4, 6), (65, 65), GOLD),
        "Shark": (0, (3, 6), (95, 65), RED),
    }
    WEIGHTS = {"Common": 60, "Rare": 30, "Legendary": 10}

    def __init__(self, fish_type=None, speed_multiplier=1.0):
        self.type = fish_type or random.choices(
            list(self.WEIGHTS), weights=list(self.WEIGHTS.values()))[0]
        points, speeds, size, self.color = self.TYPES[self.type]
        self.points, self.w, self.h = points, *size
        self.speed = random.uniform(*speeds) * speed_multiplier
        self.x = random.randint(20, WIDTH - self.w - 20)
        self.y = random.randint(WATER_TOP, WATER_BOTTOM)
        self.direction = random.choice((-1, 1))
        self.image = FISH_IMAGES[self.type]
        self.hooked = False

    def rect(self):
        return pg.Rect(int(self.x), int(self.y), self.w, self.h)

    def update(self):
        if self.hooked:
            return
        self.x += self.speed * self.direction
        if self.x <= 10 or self.x + self.w >= WIDTH - 10:
            self.direction *= -1
            self.x = max(10, min(self.x, WIDTH - self.w - 10))

    def draw(self, surface):
        if self.image:
            image = pg.transform.flip(
                self.image, True, False) if self.direction < 0 else self.image
            surface.blit(image, (int(self.x), int(self.y)))
        else:
            pg.draw.ellipse(surface, self.color, self.rect())
            eye_x = self.x + self.w * (0.8 if self.direction > 0 else 0.2)
            pg.draw.circle(surface, BLACK, (int(eye_x),
                           int(self.y + self.h * .35)), 4)


class Hook:
    WIDTH, HEIGHT = 36, 40

    def __init__(self, anchor_x, rest_y, swing_speed, vertical_speed):
        self.anchor_x, self.rest_y = anchor_x, rest_y
        # These are instance values, so changes affect the current hook.
        self.swing_speed = float(swing_speed)
        self.vertical_speed = float(vertical_speed)
        self.reset()

    def reset(self):
        self.x, self.y, self.direction = self.anchor_x, self.rest_y, 1
        self.state, self.catch = "swinging", None

    def drop(self):
        if self.state == "swinging":
            self.state = "dropping"

    def rect(self):
        return pg.Rect(int(self.x - self.WIDTH / 2), int(self.y), self.WIDTH, self.HEIGHT)

    def update(self, fish, sharks):
        if self.state == "swinging":
            self.x += self.swing_speed * self.direction
            if self.x <= 25 or self.x >= WIDTH - 25:
                self.x = max(25, min(self.x, WIDTH - 25))
                self.direction *= -1
        elif self.state == "dropping":
            self.y += self.vertical_speed
            hook = self.rect()
            if any(hook.colliderect(shark.rect()) for shark in sharks):
                return "shark_hit"
            for item in fish:
                if hook.colliderect(item.rect()):
                    self.catch, item.hooked, self.state = item, True, "reeling"
                    return "caught"
            if self.y >= HEIGHT - self.HEIGHT - 10:
                self.y, self.state = HEIGHT - self.HEIGHT - 10, "reeling"
        else:
            self.y -= self.vertical_speed
            if self.catch:
                self.catch.x, self.catch.y = self.x - self.catch.w / 2, self.y + self.HEIGHT
            if self.y <= self.rest_y:
                self.y, self.state = self.rest_y, "swinging"
                caught, self.catch = self.catch, None
                if caught:
                    return "landed", caught

    def draw(self, surface, anchor):
        pg.draw.line(surface, BLACK, anchor, (int(self.x), int(self.y)), 2)
        if IMG_HOOK:
            surface.blit(IMG_HOOK, (int(self.x - self.WIDTH / 2), int(self.y)))
        else:
            pg.draw.line(surface, (60, 60, 60), (int(self.x), int(
                self.y)), (int(self.x), int(self.y + 22)), 3)
            pg.draw.arc(surface, (60, 60, 60), (int(self.x - 9),
                        int(self.y + 14), 18, 18), 0, 3.14, 3)


class Game:
    NUM_FISH, STARTING_SHARKS = 8, 3

    def __init__(self):
        self.boat_x, self.boat_y = WIDTH // 2, 95
        self.hook = Hook(
            self.boat_x, self.boat_y + 85,
            HOOK_SWING_SPEED, HOOK_VERTICAL_SPEED
        )
        self.timer_event = pg.USEREVENT + 1
        # web: set_timerはWASM未対応のためメインループで代替
        self._web_last_timer = pg.time.get_ticks()
        self.high_score, self.level, self.state = load_high_score(), 1, "start"
        self.menu_index = 0
        self.character_index = 0
        self.bgm_index = 0
        self.exit_button = pg.Rect(WIDTH - 155, 65, 135, 35)
        self.reset_round()

    @property
    def target_score(self):
        return POINTS_PER_LEVEL * self.level

    @property
    def speed_multiplier(self):
        return 1 + (self.level - 1) * .18

    def reset_round(self):
        self.score, self.time_left, self.end_reason = 0, GAME_LENGTH, ""
        self.fish = [Fish(speed_multiplier=self.speed_multiplier)
                     for _ in range(self.NUM_FISH)]
        self.sharks = [Fish("Shark", self.speed_multiplier)
                       for _ in range(self.STARTING_SHARKS + self.level - 1)]
        self.hook.reset()

    def start_new_game(self):
        self.level = 1
        self.reset_round()
        self.state = "playing"
        start_music(BGMS[self.bgm_index][1])

    def start_next_level(self):
        self.level += 1
        self.reset_round()
        self.state = "playing"
        start_music(BGMS[self.bgm_index][1])

    def preview_selected_bgm(self):
        """Immediately play the music currently highlighted in the BGM menu."""
        stop_music()
        start_music(BGMS[self.bgm_index][1])

    def return_to_start(self):
        stop_music()
        self.level = 1
        self.reset_round()
        self.state = "start"

    def menu_items(self):
        return [
            "Start Game",
            "How to Play",
            f"Choose Character: {CHARACTERS[self.character_index][0]}",
            f"Choose BGM: {BGMS[self.bgm_index][0]}",
        ]

    def activate_menu_item(self):
        if self.menu_index == 0:
            self.start_new_game()
        elif self.menu_index == 1:
            self.state = "how_to_play"
        elif self.menu_index == 2:
            self.state = "choose_character"
        else:
            self.state = "choose_bgm"
            self.preview_selected_bgm()

    def end_game(self, reason):
        self.state, self.end_reason = "game_over", reason
        stop_music()
        if self.score > self.high_score:
            self.high_score = self.score
            save_high_score(self.high_score)

    def complete_level(self):
        self.state = "level_complete"
        stop_music()
        if self.score > self.high_score:
            self.high_score = self.score
            save_high_score(self.high_score)

    def handle_event(self, event):
        if event.type == self.timer_event and self.state == "playing":
            self.time_left -= 1
            if self.time_left <= 0:
                self.time_left = 0
                self.end_game("TIME'S UP!")
        elif event.type == pg.KEYDOWN:
            if self.state == "start":
                if event.key == pg.K_UP:
                    self.menu_index = (self.menu_index -
                                       1) % len(self.menu_items())
                elif event.key == pg.K_DOWN:
                    self.menu_index = (self.menu_index +
                                       1) % len(self.menu_items())
                elif event.key in (pg.K_SPACE, pg.K_RETURN):
                    self.activate_menu_item()
                return
            if self.state in ("how_to_play", "choose_character", "choose_bgm"):
                if event.key == pg.K_ESCAPE:
                    if self.state == "choose_bgm":
                        stop_music()
                    self.state = "start"
                elif self.state == "choose_character" and event.key in (pg.K_UP, pg.K_LEFT):
                    self.character_index = (
                        self.character_index - 1) % len(CHARACTERS)
                elif self.state == "choose_character" and event.key in (pg.K_DOWN, pg.K_RIGHT):
                    self.character_index = (
                        self.character_index + 1) % len(CHARACTERS)
                elif self.state == "choose_bgm" and event.key in (pg.K_UP, pg.K_LEFT):
                    self.bgm_index = (self.bgm_index - 1) % len(BGMS)
                    self.preview_selected_bgm()
                elif self.state == "choose_bgm" and event.key in (pg.K_DOWN, pg.K_RIGHT):
                    self.bgm_index = (self.bgm_index + 1) % len(BGMS)
                    self.preview_selected_bgm()
                elif event.key in (pg.K_SPACE, pg.K_RETURN):
                    if self.state == "choose_bgm":
                        stop_music()
                    self.state = "start"
                return
            if event.key == pg.K_ESCAPE and self.state == "playing":
                self.return_to_start()
            elif event.key == pg.K_LEFTBRACKET and self.state == "playing":
                self.hook.swing_speed = max(
                    MIN_HOOK_SPEED, self.hook.swing_speed - HOOK_SPEED_STEP)
            elif event.key == pg.K_RIGHTBRACKET and self.state == "playing":
                self.hook.swing_speed += HOOK_SPEED_STEP
            elif event.key == pg.K_COMMA and self.state == "playing":
                self.hook.vertical_speed = max(
                    MIN_HOOK_SPEED, self.hook.vertical_speed - HOOK_SPEED_STEP)
            elif event.key == pg.K_PERIOD and self.state == "playing":
                self.hook.vertical_speed += HOOK_SPEED_STEP
            elif event.key == pg.K_SPACE:
                if self.state in ("start", "game_over"):
                    self.start_new_game()
                elif self.state == "level_complete":
                    self.start_next_level()
                elif self.state == "playing":
                    if SFX_DROP:
                        SFX_DROP.play()
                    self.hook.drop()
        elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1 and self.state == "playing":
            if self.exit_button.collidepoint(event.pos):
                self.return_to_start()

    def update(self):
        if self.state != "playing":
            return
        for item in self.fish + self.sharks:
            item.update()
        result = self.hook.update(self.fish, self.sharks)
        if result == "shark_hit":
            self.end_game("EATEN BY A SHARK!")
        elif isinstance(result, tuple) and result[0] == "landed":
            caught = result[1]
            self.score += caught.points
            if SFX_CATCH:
                SFX_CATCH.play()
            if caught in self.fish:
                self.fish.remove(caught)
                self.fish.append(Fish(speed_multiplier=self.speed_multiplier))
            if self.score >= self.target_score:
                self.complete_level()

    def background(self):
        if IMG_BG:
            screen.blit(IMG_BG, (0, 0))
        else:
            screen.fill(SKY)
            pg.draw.rect(screen, WATER, (0, WATER_TOP - 20,
                         WIDTH, HEIGHT - WATER_TOP + 20))
        if IMG_BOAT:
            screen.blit(IMG_BOAT, (self.boat_x - 90, self.boat_y))
        else:
            pg.draw.polygon(screen, BROWN, [(self.boat_x - 90, self.boat_y), (self.boat_x + 90, self.boat_y),
                            (self.boat_x + 55, self.boat_y + 45), (self.boat_x - 55, self.boat_y + 45)])
        character_image = CHARACTER_IMAGES[self.character_index]
        if character_image:
            screen.blit(character_image, (self.boat_x - 35, self.boat_y - 55))
        else:
            pg.draw.circle(screen, SKIN, (self.boat_x, self.boat_y - 42), 16)
            pg.draw.rect(screen, GREEN, (self.boat_x -
                         15, self.boat_y - 28, 30, 28))
        name = font_sm.render(CHARACTERS[self.character_index][0], True, WHITE)
        name_box = name.get_rect(center=(self.boat_x, self.boat_y - 72))
        pg.draw.rect(screen, (5, 35, 65), name_box.inflate(14, 8), border_radius=8)
        screen.blit(name, name_box)

    def overlay(self, title, rows, title_color=WHITE):
        layer = pg.Surface((WIDTH, HEIGHT), pg.SRCALPHA)
        layer.fill((0, 0, 0, 175))
        screen.blit(layer, (0, 0))
        heading = font_lg.render(title, True, title_color)
        screen.blit(heading, heading.get_rect(center=(WIDTH // 2, 155)))
        for index, (text, color, font) in enumerate(rows):
            line = font.render(text, True, color)
            screen.blit(line, line.get_rect(
                center=(WIDTH // 2, 250 + index * 47)))

    def draw_hud(self):
        labels = [(f"Score: {self.score}/{self.target_score}", 20), (f"Level: {self.level}",
                                                                     55), (f"High Score: {self.high_score}", 90)]
        for text, y in labels:
            screen.blit(font_sm.render(
                text, True, GOLD if "High" in text else BLACK), (20, y))
        timer = font_md.render(
            f"Time: {self.time_left}", True, RED if self.time_left <= 10 else BLACK)
        screen.blit(timer, (WIDTH - timer.get_width() - 20, 15))
        pg.draw.rect(screen, RED, self.exit_button, border_radius=7)
        label = font_sm.render("Exit (Esc)", True, WHITE)
        screen.blit(label, label.get_rect(center=self.exit_button.center))

    def draw_start_menu(self):
        banner = pg.Rect(115, 45, WIDTH - 230, 115)
        pg.draw.rect(screen, (5, 39, 76), banner, border_radius=24)
        pg.draw.rect(screen, (80, 208, 242), banner, 3, border_radius=24)
        shadow = font_lg.render("MACHHA HUNTER", True, (0, 18, 37))
        title = font_lg.render("MACHHA HUNTER", True, GOLD)
        screen.blit(shadow, shadow.get_rect(center=(WIDTH // 2 + 3, 90)))
        screen.blit(title, title.get_rect(center=(WIDTH // 2, 87)))
        subtitle = font_sm.render("CAST  •  CATCH  •  CONQUER THE OCEAN", True, WHITE)
        screen.blit(subtitle, subtitle.get_rect(center=(WIDTH // 2, 128)))

        menu_panel = pg.Rect(160, 185, 580, 275)
        pg.draw.rect(screen, (5, 33, 69), menu_panel, border_radius=20)
        pg.draw.rect(screen, (58, 165, 210), menu_panel, 3, border_radius=20)
        for index, item in enumerate(self.menu_items()):
            button = pg.Rect(menu_panel.x + 34, menu_panel.y + 24 + index * 58, menu_panel.width - 68, 46)
            selected = index == self.menu_index
            pg.draw.rect(screen, (35, 134, 178) if selected else (12, 65, 108), button, border_radius=12)
            pg.draw.rect(screen, GOLD if selected else (69, 157, 196), button, 2, border_radius=12)
            prefix = "▶  " if selected else "    "
            label = font_md.render(prefix + item, True, WHITE)
            screen.blit(label, label.get_rect(center=button.center))

        tips = pg.Rect(195, 485, 510, 70)
        pg.draw.rect(screen, (4, 29, 57), tips, border_radius=15)
        pg.draw.rect(screen, (53, 132, 171), tips, 2, border_radius=15)
        controls = font_sm.render("↑ ↓  Select     SPACE / ENTER  Confirm", True, WHITE)
        selected = font_sm.render(f"Ready: {CHARACTERS[self.character_index][0]}  |  {BGMS[self.bgm_index][0]}", True, GOLD)
        screen.blit(controls, controls.get_rect(center=(WIDTH // 2, 507)))
        screen.blit(selected, selected.get_rect(center=(WIDTH // 2, 535)))

    def draw_menu_background(self):
        """Standalone ocean UI background; it never shows gameplay artwork."""
        for y in range(0, HEIGHT, 20):
            depth = y / HEIGHT
            color = (5 + int(8 * depth), 39 + int(55 * depth), 78 + int(75 * depth))
            pg.draw.rect(screen, color, (0, y, WIDTH, 20))
        ticks = pg.time.get_ticks() // 24
        for index in range(18):
            x = (40 + index * 53) % WIDTH
            y = HEIGHT - ((ticks + index * 61) % 500) - 25
            pg.draw.circle(screen, (145, 222, 245), (x, y), 2 + index % 4, 1)
        for index in range(4):
            x = 90 + index * 245
            y = 500 + (index % 2) * 35
            pg.draw.ellipse(screen, (8, 69, 116), (x, y, 82, 28))
            pg.draw.polygon(screen, (8, 69, 116), [(x + 70, y + 14), (x + 95, y), (x + 95, y + 28)])
        for y in (25, 32):
            pg.draw.line(screen, (62, 175, 213), (0, y), (WIDTH, y), 1)

    def draw_menu_page(self, title, rows, footer):
        header = font_lg.render(title, True, GOLD)
        screen.blit(header, header.get_rect(center=(WIDTH // 2, 100)))
        card = pg.Rect(135, 165, WIDTH - 270, 310)
        pg.draw.rect(screen, (5, 31, 65), card, border_radius=24)
        pg.draw.rect(screen, (82, 201, 237), card, 3, border_radius=24)
        for index, (text, color, font) in enumerate(rows):
            line = font.render(text, True, color)
            screen.blit(line, line.get_rect(center=(WIDTH // 2, 225 + index * 48)))
        footer_label = font_sm.render(footer, True, WHITE)
        screen.blit(footer_label, footer_label.get_rect(center=(WIDTH // 2, 515)))

    def draw_character_picker(self):
        image = CHARACTER_IMAGES[self.character_index]
        self.draw_menu_page("CHOOSE CHARACTER", [(f"<  {CHARACTERS[self.character_index][0]}  >", GOLD, font_md), ("Use LEFT / RIGHT or UP / DOWN", WHITE, font_sm), ("Character names are set in the CHARACTERS list in the code.", (185, 230, 245), font_sm)], "SPACE / ENTER  Save       ESC  Back")
        preview = pg.Rect(WIDTH // 2 - 75, 330, 150, 105)
        pg.draw.rect(screen, (13, 81, 125), preview, border_radius=18)
        pg.draw.rect(screen, GOLD, preview, 2, border_radius=18)
        if image:
            enlarged = pg.transform.smoothscale(image, (92, 92))
            screen.blit(enlarged, enlarged.get_rect(center=preview.center))

    def draw_bgm_picker(self):
        self.draw_menu_page("CHOOSE BGM", [(f"<  {BGMS[self.bgm_index][0]}  >", GOLD, font_md), ("Use LEFT / RIGHT or UP / DOWN", WHITE, font_sm), ("Your selected song plays when the game begins.", (185, 230, 245), font_sm)], "SPACE / ENTER  Save       ESC  Back")
        center = (WIDTH // 2, 385)
        pg.draw.circle(screen, (30, 140, 183), center, 45)
        pg.draw.circle(screen, GOLD, center, 45, 3)
        pg.draw.circle(screen, (5, 31, 65), center, 14)
        pg.draw.circle(screen, WHITE, center, 5)

    def draw_how_to_play(self):
        """Visual scoring and controls guide, inspired by the supplied reference."""
        title = font_lg.render("MACHHA HUNTER", True, GOLD)
        screen.blit(title, title.get_rect(center=(WIDTH // 2, 52)))

        cards = [
            ("Common", "1 POINT", GOLD),
            ("Rare", "3 POINTS", GOLD),
            ("Legendary", "10 POINTS", GOLD),
            ("Shark", "GAME OVER", RED),
        ]
        for index, (fish_type, label, color) in enumerate(cards):
            card = pg.Rect(48 + index * 204, 88, 192, 124)
            pg.draw.rect(screen, (7, 42, 79), card, border_radius=16)
            pg.draw.rect(screen, color if fish_type == "Shark" else (74, 177, 215), card, 2, border_radius=16)
            image = FISH_IMAGES[fish_type]
            if image:
                size = (72, 72) if fish_type != "Shark" else (92, 64)
                sprite = pg.transform.smoothscale(image, size)
                screen.blit(sprite, sprite.get_rect(center=(card.centerx, 132)))
            else:
                pg.draw.ellipse(screen, color, (card.centerx - 30, 108, 60, 38))
            label_surface = font_sm.render(label, True, color)
            screen.blit(label_surface, label_surface.get_rect(center=(card.centerx, 188)))

        timer = font_md.render("60 seconds — catch as many fish as you can!", True, WHITE)
        screen.blit(timer, timer.get_rect(center=(WIDTH // 2, 242)))
        levels = font_sm.render("LEVEL 1: 20 points  →  every new level is faster and has more sharks", True, GOLD)
        screen.blit(levels, levels.get_rect(center=(WIDTH // 2, 275)))
        pg.draw.line(screen, (76, 179, 215), (110, 300), (WIDTH - 110, 300), 2)

        heading = font_md.render("HOW TO PLAY", True, GOLD)
        screen.blit(heading, heading.get_rect(center=(WIDTH // 2, 330)))
        instructions = [
            "The hook moves left and right automatically.",
            "Press SPACE to lower the hook and catch fish.",
            "Bring the fish back to the boat to score points.",
        ]
        for index, text in enumerate(instructions):
            item = font_sm.render(text, True, WHITE)
            screen.blit(item, item.get_rect(center=(WIDTH // 2, 370 + index * 35)))
        warning = font_sm.render("Touching a shark = GAME OVER!", True, RED)
        screen.blit(warning, warning.get_rect(center=(WIDTH // 2, 482)))
        footer = font_sm.render("SPACE / ENTER / ESC  Back", True, WHITE)
        screen.blit(footer, footer.get_rect(center=(WIDTH // 2, 550)))

    def draw(self):
        if self.state in ("start", "how_to_play", "choose_character", "choose_bgm"):
            self.draw_menu_background()
            if self.state == "start":
                self.draw_start_menu()
            elif self.state == "how_to_play":
                self.draw_how_to_play()
            elif self.state == "choose_character":
                self.draw_character_picker()
            else:
                self.draw_bgm_picker()
            return

        self.background()
        for item in self.fish + self.sharks:
            item.draw(screen)
        self.hook.draw(screen, (self.boat_x, self.boat_y))
        if self.state == "playing":
            self.draw_hud()
        elif self.state == "level_complete":
            self.overlay(f"LEVEL {self.level} COMPLETE!", [(f"You reached {self.score} points.", GOLD, font_md), (
                f"Level {self.level + 1} target: {POINTS_PER_LEVEL * (self.level + 1)} points", WHITE, font_md), ("Press SPACE for the next level", GREEN, font_md)])
        else:
            self.overlay("GAME OVER", [(self.end_reason, RED, font_md), (
                f"Score: {self.score}/{self.target_score}", WHITE, font_md), ("Press SPACE to start a new game", GREEN, font_md)], RED)


async def main():
    game, running = Game(), True
    while running:
        await asyncio.sleep(0)
        clock.tick(FPS)
        await asyncio.sleep(0)
        _now = pg.time.get_ticks()
        if _now - game._web_last_timer >= 1000:
            game._web_last_timer = _now
            pg.event.post(pg.event.Event(game.timer_event))
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            else:
                game.handle_event(event)
        game.update()
        game.draw()
        pg.display.flip()
    stop_music()
    save_high_score(game.high_score)
    pg.quit()
    return



async def _web_main():
    if __name__ == "__main__":
        await main()



async def _web_boot():
    try:
        await _web_main()
    except Exception:
        import traceback
        tb = traceback.format_exc()
        try:
            import platform as _pf
            _pf.window.console.log("PYERROR:\n" + tb)
        except Exception:
            print(tb)

asyncio.run(_web_boot())