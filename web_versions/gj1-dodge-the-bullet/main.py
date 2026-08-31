# --- Web版 (pygbag対応のための自動変換コピー) ---
# 元ファイル: dodge the bullet.py / ゲーム内容は変更していません
import asyncio

async def main():
    import pygame
    import os

    pygame.init()  # Starts Pygame. Always needed at the beginning before you use Pygame features.

    # Screen settings
    WIDTH, HEIGHT = 800, 400
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Dodge the Bullets")

    # Path settings for images (relative path)
    BASE_DIR = os.path.dirname(__file__)
    ASSET_DIR = os.path.join(BASE_DIR, "assets")

    # Load images using relative paths
    player_img = pygame.image.load(os.path.join(ASSET_DIR, "player.png"))
    enemy_img = pygame.image.load(os.path.join(ASSET_DIR, "enemy.png"))
    bullet_img = pygame.image.load(os.path.join(ASSET_DIR, "bullet.png"))

    # Resize images
    player_img = pygame.transform.scale(player_img, (50, 50))
    enemy_img = pygame.transform.scale(enemy_img, (50, 100))
    bullet_img = pygame.transform.scale(bullet_img, (20, 20))

    # Player settings
    player_x = 20
    player_y = HEIGHT - 50
    player_y_vel = 0
    on_ground = True
    gravity = 1
    jump_power = -20

    # Enemy settings
    enemy_x = WIDTH - 70
    enemy_y = HEIGHT - 100

    # Bullets
    bullets = []
    bullet_speed = 10

    # Game state
    running = True
    game_over = False
    frame_count = 0

    clock = pygame.time.Clock()

    while running:
        screen.fill((255, 255, 255))  # White background

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Input handling (jump)
        keys = pygame.key.get_pressed()
        if not game_over and keys[pygame.K_SPACE] and on_ground:
            player_y_vel = jump_power
            on_ground = False

        # Player movement
        player_y += player_y_vel
        if not on_ground:
            player_y_vel += gravity
        if player_y >= HEIGHT - 50:
            player_y = HEIGHT - 50
            player_y_vel = 0
            on_ground = True

        # Enemy shoots bullet every 60 frames (~1 second)
        frame_count += 1
        if not game_over and frame_count % 60 == 0:
            bullet_y = enemy_y + 40
            bullets.append([enemy_x, bullet_y])

        # Move bullets
        for bullet in bullets:
            bullet[0] -= bullet_speed

        # Collision check
        player_rect = pygame.Rect(player_x, player_y, 50, 50)
        for b in bullets:
            bullet_rect = pygame.Rect(b[0], b[1], 20, 20)
            if player_rect.colliderect(bullet_rect):
                game_over = True

        # Drawing
        screen.blit(player_img, (player_x, player_y))
        screen.blit(enemy_img, (enemy_x, enemy_y))
        for b in bullets:
            screen.blit(bullet_img, (b[0], b[1]))

        # Show game over text
        if game_over:
            font = pygame.font.SysFont(None, 60)
            text = font.render("Game Over! Press ESC to exit", True, (255, 0, 0))
            screen.blit(text, (150, 150))

        pygame.display.update()
        clock.tick(60)
        await asyncio.sleep(0)

        # Exit if ESC is pressed during game over
        if game_over:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_ESCAPE]:
                running = False

    pygame.quit()


asyncio.run(main())