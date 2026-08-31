# --- Web版 (pygbag対応のための自動変換コピー) ---
# 元ファイル: game.py / ゲーム内容は変更していません
import asyncio

async def main():
    import pygame
    import random
    import time
    import os

    # Initialize Pygame
    pygame.init()
    pygame.mixer.init()

    # Screen setup
    WIDTH, HEIGHT = 400, 600
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("fly high")
    clock = pygame.time.Clock()

    # Colors
    WHITE = (255, 255, 255)
    GRAY = (30, 30, 30)
    BLUE = (0, 100, 255)

    # Base path for resources
    base_path = os.path.dirname(__file__)
    image_path = os.path.join(base_path, "asset", "image")
    sound_path = os.path.join(base_path, "asset", "sound")

    # Load images
    try:
        car_img = pygame.image.load(os.path.join(image_path, "c.png"))
        bike_img = pygame.image.load(os.path.join(image_path, "rcar.png"))
        car_img = pygame.transform.scale(car_img, (40, 60))
        bike_img = pygame.transform.scale(bike_img, (30, 50))
    except Exception as e:
        print(f"Error loading images: {e}")
        pygame.quit()
        exit()

    # Load background music
    try:
        pygame.mixer.music.load(os.path.join(sound_path, "m.ogg"))
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)  # Loop music
    except Exception as e:
        print(f"Error loading sound: {e}")

    # Fonts
    font = pygame.font.SysFont(None, 36)

    # Game variables
    lanes = [80, 160, 240]
    lane_index = 1
    player = pygame.Rect(lanes[lane_index], HEIGHT - 80, car_img.get_width(), car_img.get_height())
    score = 0
    obstacles = []
    scroll_speed = 5
    last_obstacle_time = 0
    click_times = []
    game_over = False

    # Create obstacle
    def create_obstacle():
        lane = random.choice(lanes)
        obstacles.append({
            "rect": pygame.Rect(lane, -60, bike_img.get_width(), bike_img.get_height()),
            "x": lane
        })

    # Main loop
    running = True
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if game_over:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    # Restart game
                    lane_index = 1
                    player.x = lanes[lane_index]
                    player.y = HEIGHT - 80
                    score = 0
                    obstacles = []
                    game_over = False
                    pygame.mixer.music.play(-1)
            else:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    now = time.time()
                    click_times = [t for t in click_times if now - t < 0.2]
                    click_times.append(now)

                    if len(click_times) >= 2:
                        # Double press = move right
                        if lane_index < 2:
                            lane_index += 1
                        player.x = lanes[lane_index]
                        click_times = []
                    else:
                        pygame.time.set_timer(pygame.USEREVENT, 200)

                elif event.type == pygame.USEREVENT:
                    if len(click_times) == 1:
                        # Single press = move left
                        if lane_index > 0:
                            lane_index -= 1
                        player.x = lanes[lane_index]
                    click_times = []
                    pygame.time.set_timer(pygame.USEREVENT, 0)

        # Game logic
        if not game_over:
            current_time = pygame.time.get_ticks()
            if current_time - last_obstacle_time > 800:
                create_obstacle()
                last_obstacle_time = current_time

            for obstacle in obstacles[:]:
                obstacle["rect"].y += scroll_speed

                # Collision detection
                if obstacle["rect"].colliderect(player):
                    game_over = True
                    pygame.mixer.music.stop()

                if obstacle["rect"].y > HEIGHT:
                    obstacles.remove(obstacle)
                    score += 1

        # Drawing
        screen.fill(GRAY)

        if game_over:
            text = font.render(f"Game Over! Score: {score}", True, WHITE)
            restart = font.render("Press SPACE to restart", True, BLUE)
            screen.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2 - 30))
            screen.blit(restart, (WIDTH//2 - restart.get_width()//2, HEIGHT//2 + 30))
        else:
            for obstacle in obstacles:
                screen.blit(bike_img, (obstacle["x"], obstacle["rect"].y))
            screen.blit(car_img, (player.x, player.y))
            score_display = font.render(f"Score: {score}", True, WHITE)
            screen.blit(score_display, (10, 10))

        pygame.display.flip()
        clock.tick(60)
        await asyncio.sleep(0)

    pygame.quit()


asyncio.run(main())