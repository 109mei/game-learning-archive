# --- Web版 (pygbag対応のための自動変換コピー) ---
# 元ファイル: one_touch_game.py / ゲーム内容は変更していません
import asyncio

async def main():
    import pygame
    import sys
    import random

    # Init
    pygame.init()
    pygame.mixer.init()

    # Constants
    WIDTH, HEIGHT = 800, 600
    FPS = 60
    GRAVITY = 0.5
    JUMP_STRENGTH = -10
    OBSTACLE_WIDTH = 50
    OBSTACLE_GAP = 200
    OBSTACLE_SPEED = 5

    # Setup display
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("One Touch Jump Game")
    clock = pygame.time.Clock()

    # Load assets
    bg = pygame.image.load("assets/bg.png").convert()
    player_img = pygame.image.load("assets/player.png").convert_alpha()
    jump_sound = pygame.mixer.Sound("assets/jump.wav")

    # Player
    player = pygame.Rect(100, HEIGHT // 2, 50, 50)
    vel_y = 0
    score = 0
    game_active = False

    # Font
    font = pygame.font.SysFont(None, 48)

    # Obstacles
    def create_obstacle():
        gap_y = random.randint(150, HEIGHT - 150)
        top_rect = pygame.Rect(WIDTH, 0, OBSTACLE_WIDTH, gap_y - OBSTACLE_GAP // 2)
        bottom_rect = pygame.Rect(WIDTH, gap_y + OBSTACLE_GAP // 2, OBSTACLE_WIDTH, HEIGHT)
        return [top_rect, bottom_rect]

    obstacles = []

    # Draw text
    def draw_text(text, size, color, x, y):
        font = pygame.font.SysFont(None, size)
        surface = font.render(text, True, color)
        rect = surface.get_rect(center=(x, y))
        screen.blit(surface, rect)

    # Game loop
    spawn_timer = 0
    while True:
        screen.blit(bg, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.MOUSEBUTTONDOWN or (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE):
                if not game_active:
                    game_active = True
                    player.y = HEIGHT // 2
                    vel_y = 0
                    score = 0
                    obstacles.clear()
                else:
                    vel_y = JUMP_STRENGTH
                    jump_sound.play()

        if game_active:
            # Gravity
            vel_y += GRAVITY
            player.y += vel_y

            # Add new obstacles
            spawn_timer += 1
            if spawn_timer > 90:
                obstacles.extend(create_obstacle())
                spawn_timer = 0

            # Move obstacles and detect collisions
            for obs in obstacles:
                obs.x -= OBSTACLE_SPEED
                pygame.draw.rect(screen, (255, 0, 0), obs)
                if player.colliderect(obs):
                    game_active = False  # Game over

            # Remove off-screen obstacles
            obstacles = [obs for obs in obstacles if obs.right > 0]

            # Ground check
            if player.bottom > HEIGHT or player.top < 0:
                game_active = False

            screen.blit(player_img, player)
            score += 1 / FPS
            draw_text(f"Score: {int(score)}", 36, (255, 255, 255), WIDTH // 2, 50)

        else:
            draw_text("One Touch Jump Game", 64, (255, 255, 255), WIDTH // 2, HEIGHT // 3)
            draw_text("Click or Press Space to Start", 36, (200, 200, 200), WIDTH // 2, HEIGHT // 2)

        pygame.display.flip()
        clock.tick(FPS)
        await asyncio.sleep(0)


asyncio.run(main())