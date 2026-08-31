# --- Web版 (pygbag対応のための変換コピー / ゲーム内容は変更していません) ---
import asyncio
import pygame
import sys

import pygame.display

pygame.init()


#Screen set up
WIDTH, HEIGHT = 640, 480
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("ONE BUTTON")

#LOAD IMAGES
menu_bg=pygame.image.load("image/bg1.png").convert()
menu_bg=pygame.transform.scale(menu_bg,(WIDTH,HEIGHT))

game_bg=pygame.image.load("image/bg.png").convert()
game_bg=pygame.transform.scale(game_bg,(WIDTH,HEIGHT))

ground_img=pygame.image.load("image/gg.png").convert_alpha()
ground_height= ground_img.get_height()

player_img=pygame.image.load("image/mchr2.png").convert_alpha()
player_img=pygame.transform.scale(player_img, (80, 80))
player=player_img.get_rect()
player.x=100
player.y=HEIGHT-ground_height-player.height

obstacle_img=pygame.image.load("image/ene1.png").convert_alpha()
obstacle_img=pygame.transform.scale(obstacle_img,(40,40))
obstacle=obstacle_img.get_rect()
obstacle.x=WIDTH
obstacle.y=HEIGHT-ground_height-obstacle.height

sound_on_img=pygame.transform.scale(pygame.image.load("image/so.png").convert_alpha(), (30, 30))
sound_off_img = pygame.transform.scale(pygame.image.load("image/sof.png").convert_alpha(), (30, 30))
sound_button_rect = sound_on_img.get_rect(topleft=(10, HEIGHT - 40))
sound_on = True 

#load sound
jump_sound = pygame.mixer.Sound("sound/jump.ogg")
go_sound = pygame.mixer.Sound("sound/go.ogg")

#game object
player_height = 80
obstacle_height = 50

player = pygame.Rect(100, HEIGHT - ground_height - player_height, 80, player_height)
obstacle = pygame.Rect(WIDTH, HEIGHT - ground_height - obstacle_height, 40, obstacle_height)
gravity = 1
obstacle_speed = 5

# === Score system ===
score_font = pygame.font.SysFont(None, 36)
high_score = 0

# Clock 
clock = pygame.time.Clock()

# Toggle Sound 
def toggle_sound():
    global sound_on
    sound_on = not sound_on
    if not sound_on:
        pygame.mixer.pause()
    else:
        pygame.mixer.unpause()

#Show Menu 
async def show_menu():
    title_font = pygame.font.SysFont(None, 250)
    menu_font = pygame.font.SysFont(None, 36)
    menu_font1 = pygame.font.SysFont(None, 25)
    name_font = pygame.font.SysFont(None, 22)
    jp_font1 = pygame.font.Font("jpfont/static/NotoSansJP-Regular.ttf", 35)
    jp_font = pygame.font.Font("jpfont/static/NotoSansJP-Regular.ttf", 22)

    title_text = jp_font1.render("ジャンプゲーム", True, (0, 0, 0))
    prompt_text1 = menu_font1.render("Help", True, (255, 0, 0))
    prompt_text = menu_font.render("Press Enter to Start", True, (255, 0, 0))
    name_text1 = name_font.render("Created by MKZ", True, (0, 0, 0))
    name_text2 = jp_font.render("九州情報大学", True, (0, 0, 0))

    icon_img = pygame.image.load("image/mchr2.png").convert_alpha()
    icon_img = pygame.transform.scale(icon_img, (40, 40))

    while True:
        await asyncio.sleep(0)
        screen.blit(menu_bg, (0, 0))
        screen.blit(icon_img, ((WIDTH - icon_img.get_width()) // 2, 135))
        screen.blit(title_text, ((WIDTH - title_text.get_width()) // 2, 180))
        screen.blit(prompt_text, ((WIDTH - prompt_text.get_width()) // 2, 250))
        screen.blit(prompt_text1, ((WIDTH - prompt_text1.get_width()) // 2, 280))
        screen.blit(name_text1, (WIDTH - name_text1.get_width() - 10, HEIGHT - 40))
        screen.blit(name_text2, (WIDTH - name_text2.get_width() - 10, HEIGHT - 30))
        screen.blit(sound_on_img if sound_on else sound_off_img, sound_button_rect.topleft)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return
                if event.key == pygame.K_h:
                    await show_help()
                if event.key == pygame.K_s:
                    toggle_sound()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if sound_button_rect.collidepoint(event.pos):
                    toggle_sound()

# Help screen 
async def show_help():
    help_font = pygame.font.SysFont(None, 28)
    lines = [
        "[SPACE] - Jump",
        "[ENTER] - Start Game",
        "[R] - Restart Game",
        "[ESC] - Return to Menu",
        "[S] - Toggle Sound"
    ]
    while True:
        await asyncio.sleep(0)
        screen.blit(menu_bg, (0, 0))
        for i, line in enumerate(lines):
            text = help_font.render(line, True, (0, 0, 0))
            screen.blit(text, ((WIDTH - text.get_width()) // 2, 150 + i * 40))
        screen.blit(sound_on_img if sound_on else sound_off_img, sound_button_rect.topleft)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
                if event.key == pygame.K_s:
                    toggle_sound()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if sound_button_rect.collidepoint(event.pos):
                    toggle_sound()

#Main Game Loop 
async def run_game():
    global high_score, obstacle_speed
    score = 0
    jumping = False
    velocity = 0

    player.y = HEIGHT - ground_height - player.height
    obstacle.x = WIDTH
    obstacle_speed = 5

    running = True
    while running:
        await asyncio.sleep(0)
        screen.blit(game_bg, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
                if event.key == pygame.K_s:
                    toggle_sound()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if sound_button_rect.collidepoint(event.pos):
                    toggle_sound()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and not jumping:
            velocity = -20
            jumping = True
            if sound_on:
                jump_sound.play()

        # Apply gravity
        velocity += gravity
        player.y += velocity
        if player.y >= HEIGHT - ground_height - player.height:
            player.y = HEIGHT - ground_height - player.height
            jumping = False
    
        # Move obstacle
        obstacle.x -= obstacle_speed
        if obstacle.x < -30:
            obstacle.x = WIDTH
            score += 1
            obstacle_speed = min(5 + score * 0.1, 15)

        # Convert speed to level (1–5)
        level = min(1 + int(score // 5), 5)

        # Check collision
        if player.colliderect(obstacle):
            if score > high_score:
                high_score = score
            if sound_on:
                go_sound.play()
            message_font = pygame.font.SysFont(None, 36)
            message = message_font.render("Game Over! Press R to Restart", True, (255, 0, 0))
            high_score_text = score_font.render(f"High Score: {high_score}", True, (255, 255, 0))

            while True:
                await asyncio.sleep(0)
                screen.blit(game_bg, (0, 0))
                for x in range(0, WIDTH, ground_img.get_width()):
                    screen.blit(ground_img, (x, HEIGHT - ground_height))
                screen.blit(message, ((WIDTH - message.get_width()) // 2, HEIGHT // 2 - 20))
                screen.blit(high_score_text, ((WIDTH - high_score_text.get_width()) // 2, HEIGHT // 2 + 20))
                pygame.display.flip()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_r:
                            return
                        if event.key == pygame.K_ESCAPE:
                            return

        #Draw all
        screen.blit(player_img, (player.x, player.y))
        screen.blit(obstacle_img, (obstacle.x, obstacle.y))
        for x in range(0, WIDTH, ground_img.get_width()):
            screen.blit(ground_img, (x, HEIGHT - ground_height))

        score_text = score_font.render(f"Score: {score}", True, (255, 255, 255))
        high_score_display = score_font.render(f"High Score: {high_score}", True, (255, 255, 0))
        level_text = score_font.render(f"Level: {level}", True, (0, 255, 255))

        screen.blit(score_text, (10, 10))
        screen.blit(high_score_display, (10, 40))
        screen.blit(level_text, (10, 70))
        screen.blit(sound_on_img if sound_on else sound_off_img, sound_button_rect.topleft)

        pygame.display.flip()
        clock.tick(60)
        await asyncio.sleep(0)

# === Start the Game ===

async def _web_main():
    await show_menu()
    while True:
        await asyncio.sleep(0)
        await run_game()
        await show_menu()

asyncio.run(_web_main())