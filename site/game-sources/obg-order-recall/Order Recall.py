# -*- coding: utf-8 -*-
import pygame
import random
import math
import os
import sys

# --- ADD THIS: The name of your Japanese font file ---
# Make sure this file is in the same folder as your script!
JAPANESE_FONT = "NotoSansJP-Regular.ttf" # Or "NotoSansJP-Regular.ttf"

def get_resource_path(filename):
    if hasattr(sys, "_MEIPASS"):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, filename)

pygame.init()

# Screen settings
WIDTH = 1600
HEIGHT = 900
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (100, 150, 255)

# Game states
STATE_MAIN_MENU = "menu"
STATE_MEMORIZE = "memorize"
STATE_FLIP_BACK = "flip_back"
STATE_SHUFFLE = "shuffle"
STATE_FLIP_FRONT = "flip_front"
STATE_GUESS = "guess"
STATE_RESULT = "result"
STATE_COMPLETE = "complete"

class Card:
    def __init__(self, x, y, image_name, card_id):
        self.x = x
        self.y = y
        self.target_x = x
        self.target_y = y
        self.card_id = card_id
        self.face_up = True
        self.selected = False
        
        scale_factor = min(WIDTH / 1920, HEIGHT / 1080)
        self.width = int(160 * scale_factor)
        self.height = int(160 * scale_factor)

        try:
            self.image = pygame.image.load(get_resource_path(image_name))
            self.image = pygame.transform.scale(self.image, (self.width, self.height))
        except Exception as e:
            print(f"Warning: Could not load {image_name}: {e}")
            self.image = pygame.Surface((self.width, self.height))
            self.image.fill((200, 200, 200))
            # Use the global font path here too for safety
            try:
                font = pygame.font.Font(get_resource_path(JAPANESE_FONT), 36)
            except:
                font = pygame.font.Font(None, 36)
            text = font.render(str(card_id + 1), True, BLACK)
            text_rect = text.get_rect(center=(self.width // 2, self.height // 2))
            self.image.blit(text, text_rect)

    def draw(self, screen):
        if self.face_up:
            screen.blit(self.image, (int(self.x), int(self.y)))
            if self.selected:
                pygame.draw.circle(screen, GREEN, 
                                 (int(self.x + self.width - 20), int(self.y + 20)), 15)
                pygame.draw.circle(screen, WHITE, 
                                 (int(self.x + self.width - 20), int(self.y + 20)), 15, 3)
        else:
            pygame.draw.rect(screen, (50, 50, 150),
                           (int(self.x), int(self.y), self.width, self.height))
            pygame.draw.rect(screen, WHITE,
                           (int(self.x), int(self.y), self.width, self.height), 4)
    
    def move_towards_target(self, speed=8):
        dx = self.target_x - self.x
        dy = self.target_y - self.y
        dist = math.sqrt(dx**2 + dy**2)
        if dist > speed:
            self.x += (dx / dist) * speed
            self.y += (dy / dist) * speed
            return False
        else:
            self.x = self.target_x
            self.y = self.target_y
            return True

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("オーダー・リコール (Order Recall)")
        self.clock = pygame.time.Clock()
        self.running = True

        try:
            self.background = pygame.image.load(get_resource_path("background.png"))
            self.background = pygame.transform.scale(self.background, (WIDTH, HEIGHT))
        except:
            self.background = pygame.Surface((WIDTH, HEIGHT))
            self.background.fill((30, 30, 60))

        # --- UPDATED: Load Japanese Font Files ---
        font_path = get_resource_path(JAPANESE_FONT)
        scale_factor = HEIGHT / 1080
        try:
            self.font_large = pygame.font.Font(font_path, int(96 * scale_factor))
            self.font_medium = pygame.font.Font(font_path, int(64 * scale_factor))
            self.font_small = pygame.font.Font(font_path, int(42 * scale_factor))
        except:
            print(f"ERROR: Could not find font file {JAPANESE_FONT}!")
            pygame.quit()
            sys.exit()

        self.level = 1
        self.state = STATE_MAIN_MENU
        self.cards = []
        self.correct_order = []
        self.player_guesses = []
        self.cursor_index = 0
        self.cursor_speed = 2.0
        self.cursor_timer = 0
        self.cursor_order = []
        self.cursor_position = 0
        self.memorize_timer = 0
        self.memorize_duration = 6000  # Changed to 6 seconds
        self.flip_timer = 0
        self.flip_duration = 1000
        self.result_timer = 0
        self.result_duration = 2000  # Duration to show result before auto-continue
        self.shuffle_count = 0
        self.max_shuffles = 3
        self.complete_timer = 0
        self.complete_duration = 3000  # Duration to show completion before returning to menu

        self.level_images = {
            1: ["1a.png", "1b.png", "1c.png", "1d.png"],
            2: ["2a.png", "2b.png", "2c.png", "2d.png", "2e.png"],
            3: ["3a.png", "3b.png", "3c.png", "3d.png", "3e.png", "3f.png"]
        }
        
        # Level-specific memorization text - UPDATED with "left to right"
        self.level_text = {
            1: "ドアの順番を左から右に覚えてください！",
            2: "車の順番を左から右に覚えてください！",
            3: "アヒルの順番を左から右に覚えてください！"
        }

    def setup_level(self):
        self.cards = []
        self.correct_order = []
        self.player_guesses = []
        self.cursor_index = 0
        self.cursor_timer = 0
        self.memorize_timer = 0
        self.shuffle_count = 0
        self.flip_timer = 0
        self.cursor_order = []
        self.cursor_position = 0
        images = self.level_images[self.level]
        if self.level == 1: self.cursor_speed = 2.0
        elif self.level == 2: self.cursor_speed = 1.8
        else: self.cursor_speed = 1.5
        scale_factor = min(WIDTH / 1920, HEIGHT / 1080)
        spacing = int(200 * scale_factor)
        total_width = len(images) * spacing - int(40 * scale_factor)
        start_x = (WIDTH - total_width) // 2
        y = HEIGHT // 2 - int(80 * scale_factor) + int(50 * scale_factor)
        
        # RANDOMIZE: Shuffle the images list to randomize initial placement
        randomized_images = images.copy()
        random.shuffle(randomized_images)
        
        for i, img in enumerate(randomized_images):
            card = Card(start_x + i * spacing, y, img, i)
            self.cards.append(card)
            self.correct_order.append(i)
        self.state = STATE_MEMORIZE

    def shuffle_cards(self):
        positions = [(card.x, card.y) for card in self.cards]
        random.shuffle(positions)
        for i, card in enumerate(self.cards):
            card.target_x, card.target_y = positions[i]

    def get_current_card_order(self):
        sorted_cards = sorted(enumerate(self.cards), key=lambda x: x[1].x)
        return [self.correct_order.index(card_id) + 1 for card_id, card in sorted_cards]

    def draw_cursor(self):
        if self.state == STATE_GUESS and len(self.player_guesses) < len(self.cards):
            card = self.cards[self.cursor_index]
            cursor_y = card.y - 50
            cursor_x = card.x + card.width // 2
            offset = math.sin(pygame.time.get_ticks() / 200) * 15
            pygame.draw.polygon(self.screen, YELLOW, [
                (cursor_x, cursor_y + offset),
                (cursor_x - 25, cursor_y - 30 + offset),
                (cursor_x + 25, cursor_y - 30 + offset)
            ])
            progress = (self.cursor_timer % (self.cursor_speed * 1000)) / (self.cursor_speed * 1000)
            bar_width = card.width
            bar_height = 12
            bar_x = card.x
            bar_y = card.y + card.height + 15
            pygame.draw.rect(self.screen, WHITE, (bar_x, bar_y, bar_width, bar_height), 3)
            pygame.draw.rect(self.screen, GREEN, (bar_x, bar_y, bar_width * progress, bar_height))

    def draw_ui(self):
        if self.state != STATE_MAIN_MENU:
            # Translated: Level
            level_text = self.font_medium.render(f"レベル: {self.level}/3", True, WHITE)
            self.screen.blit(level_text, (30, 30))
        
        if self.state == STATE_MEMORIZE:
            remaining = int((self.memorize_duration - self.memorize_timer) / 1000) + 1
            # Use level-specific text
            text = self.font_small.render(f"{self.level_text[self.level]} 残り {remaining} 秒", True, WHITE)
            self.screen.blit(text, (WIDTH // 2 - text.get_width() // 2, 200))
            
        elif self.state == STATE_GUESS:
            text = self.font_small.render(
                f"タイミングよくスペースキーを押して選択！ ({len(self.player_guesses)}/{len(self.cards)})", 
                True, WHITE)
            self.screen.blit(text, (WIDTH // 2 - text.get_width() // 2, 200))
            
            if len(self.player_guesses) > 0:
                guess_text = "選択した順: "
                for guess in self.player_guesses:
                    guess_text += f"{guess + 1} "
                text = self.font_small.render(guess_text, True, YELLOW)
                self.screen.blit(text, (30, HEIGHT - 70))

    def check_result(self):
        return self.player_guesses == self.correct_order

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                # Q key to quit game from anywhere
                if event.key == pygame.K_q:
                    self.running = False
                elif self.state == STATE_MAIN_MENU:
                    if event.key == pygame.K_SPACE:
                        self.setup_level()
                elif event.key == pygame.K_ESCAPE:
                    self.level = 1
                    self.state = STATE_MAIN_MENU
                elif event.key == pygame.K_SPACE:
                    if self.state == STATE_GUESS and len(self.player_guesses) < len(self.cards):
                        self.cards[self.cursor_index].selected = True
                        self.player_guesses.append(self.cursor_index)
                        if len(self.player_guesses) == len(self.cards):
                            self.state = STATE_RESULT
                            self.result_timer = pygame.time.get_ticks()
                    elif self.state == STATE_RESULT:
                        if self.check_result():
                            # Success - auto continue
                            if self.level < 3:
                                self.level += 1
                                self.setup_level()
                            else:
                                self.state = STATE_COMPLETE
                                self.complete_timer = pygame.time.get_ticks()
                        else:
                            # Failure - retry same level
                            self.setup_level()

    def update(self):
        dt = self.clock.get_time()
        if self.state == STATE_MEMORIZE:
            self.memorize_timer += dt
            if self.memorize_timer >= self.memorize_duration:
                self.state = STATE_FLIP_BACK
                self.flip_timer = 0
                
        elif self.state == STATE_FLIP_BACK:
            self.flip_timer += dt
            if self.flip_timer >= self.flip_duration:
                for card in self.cards: card.face_up = False
                self.state = STATE_SHUFFLE
                self.shuffle_cards()
                
        elif self.state == STATE_SHUFFLE:
            all_reached = True
            for card in self.cards:
                if not card.move_towards_target(8): all_reached = False
            if all_reached:
                self.shuffle_count += 1
                if self.shuffle_count < self.max_shuffles: 
                    self.shuffle_cards()
                else:
                    self.state = STATE_FLIP_FRONT
                    self.flip_timer = 0
                    
        elif self.state == STATE_FLIP_FRONT:
            self.flip_timer += dt
            if self.flip_timer >= self.flip_duration:
                for card in self.cards: card.face_up = True
                self.state = STATE_GUESS
                self.cursor_order = list(range(len(self.cards)))
                random.shuffle(self.cursor_order)
                self.cursor_index = self.cursor_order[0]
                self.cursor_position = 0
                
        elif self.state == STATE_GUESS:
            self.cursor_timer += dt
            if self.cursor_timer >= self.cursor_speed * 1000:
                self.cursor_timer = 0
                attempts = 0
                while attempts < len(self.cards):
                    self.cursor_position = (self.cursor_position + 1) % len(self.cards)
                    self.cursor_index = self.cursor_order[self.cursor_position]
                    if self.cursor_index not in self.player_guesses: break
                    attempts += 1
                    
        elif self.state == STATE_RESULT:
            # Only auto-continue on success
            if self.check_result():
                if pygame.time.get_ticks() - self.result_timer >= self.result_duration:
                    if self.level < 3:
                        self.level += 1
                        self.setup_level()
                    else:
                        self.state = STATE_COMPLETE
                        self.complete_timer = pygame.time.get_ticks()
                    
        elif self.state == STATE_COMPLETE:
            # Don't auto-return to menu - let player decide
            pass

    def draw(self):
        self.screen.blit(self.background, (0, 0))
        if self.state == STATE_MAIN_MENU:
            overlay = pygame.Surface((WIDTH, HEIGHT))
            overlay.set_alpha(180)
            overlay.fill(BLACK)
            self.screen.blit(overlay, (0, 0))
            
            title = self.font_large.render("オーダー・リコール", True, YELLOW)
            self.screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 2 - 250))
            
            pulse = abs(math.sin(pygame.time.get_ticks() / 400))
            alpha = int(155 + pulse * 100)
            play_text = self.font_medium.render("スペースキーで開始", True, GREEN)
            play_surface = pygame.Surface((play_text.get_width(), play_text.get_height()), pygame.SRCALPHA)
            play_surface.blit(play_text, (0, 0))
            play_surface.set_alpha(alpha)
            self.screen.blit(play_surface, (WIDTH // 2 - play_text.get_width() // 2, HEIGHT // 2 - 100))
            
            restart_text = self.font_small.render("ESCキーでメニューに戻る (ゲーム中)", True, WHITE)
            self.screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 - 20))
            
            quit_text = self.font_small.render("Qキーでゲーム終了", True, WHITE)
            self.screen.blit(quit_text, (WIDTH // 2 - quit_text.get_width() // 2, HEIGHT // 2 + 20))
            
            # UPDATED instructions with "left to right"
            instructions = [
                "遊び方:",
                "1. 絵の順番を左から右に覚える",
                "2. シャッフルされるのを見る",
                "3. カーソルが合った時に元の順番で選択する",
                "4. 全3レベルをクリアして勝利！"
            ]
            y_offset = HEIGHT // 2 + 60
            for instruction in instructions:
                text = self.font_small.render(instruction, True, WHITE)
                self.screen.blit(text, (WIDTH // 2 - text.get_width() // 2, y_offset))
                y_offset += 50
        else:
            for card in self.cards: card.draw(self.screen)
            self.draw_cursor()
            self.draw_ui()
            
            if self.state == STATE_RESULT:
                overlay = pygame.Surface((WIDTH, HEIGHT))
                overlay.set_alpha(200)
                overlay.fill(BLACK)
                self.screen.blit(overlay, (0, 0))
                if self.check_result():
                    text = self.font_large.render("正解！", True, GREEN)
                    self.screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - 80))
                else:
                    text = self.font_large.render("残念！", True, RED)
                    self.screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - 120))
                    # Show retry options for failure
                    retry_text = self.font_medium.render("スペースキーでリトライ", True, YELLOW)
                    menu_text = self.font_small.render("ESCキーでメニューに戻る", True, WHITE)
                    self.screen.blit(retry_text, (WIDTH // 2 - retry_text.get_width() // 2, HEIGHT // 2 + 20))
                    self.screen.blit(menu_text, (WIDTH // 2 - menu_text.get_width() // 2, HEIGHT // 2 + 90))
                    
                correct_text = "正解の順番: " + " ".join(map(str, self.get_current_card_order()))
                order_text = self.font_small.render(correct_text, True, YELLOW)
                self.screen.blit(order_text, (WIDTH // 2 - order_text.get_width() // 2, HEIGHT // 2 + 160))
            
            elif self.state == STATE_COMPLETE:
                overlay = pygame.Surface((WIDTH, HEIGHT))
                overlay.set_alpha(220)
                overlay.fill(BLACK)
                self.screen.blit(overlay, (0, 0))
                congrats = self.font_large.render("おめでとうございます！", True, GREEN)
                msg1 = self.font_medium.render("全レベルをクリアしました！", True, YELLOW)
                msg2 = self.font_medium.render("あなたは記憶力マスターです！", True, YELLOW)
                menu_text = self.font_small.render("ESCキーでメニューに戻る", True, WHITE)
                quit_text = self.font_small.render("Qキーでゲーム終了", True, WHITE)
                self.screen.blit(congrats, (WIDTH // 2 - congrats.get_width() // 2, HEIGHT // 2 - 150))
                self.screen.blit(msg1, (WIDTH // 2 - msg1.get_width() // 2, HEIGHT // 2 - 60))
                self.screen.blit(msg2, (WIDTH // 2 - msg2.get_width() // 2, HEIGHT // 2))
                self.screen.blit(menu_text, (WIDTH // 2 - menu_text.get_width() // 2, HEIGHT // 2 + 80))
                self.screen.blit(quit_text, (WIDTH // 2 - quit_text.get_width() // 2, HEIGHT // 2 + 130))

        pygame.display.flip()

    def run(self):
        while self.running:
            self.handle_input()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        pygame.quit()

if __name__ == "__main__":
    try:
        Game().run()
    except Exception as e:
        print(f"ERROR: {e}")
        input("\nPress Enter to exit...")
        sys.exit(1)