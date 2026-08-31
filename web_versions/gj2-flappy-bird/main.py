# --- Web版 (pygbag対応のための変換コピー / ゲーム内容は変更していません) ---
import asyncio
import pygame
import random

# ======================= CẤU HÌNH GAME ===========================
pygame.init()

WIDTH, HEIGHT = 400, 600
FPS = 65
GRAVITY = 0.25
FLAP_STRENGTH = -7
PIPE_SPEED = 3
PIPE_GAP = 150
PIPE_WIDTH = 50
BIRD_SIZE = 35

# Màu sắc
SKY_BLUE = (135, 206, 235)
PIPE_GREEN = (0, 168, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Màn hình
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")
clock = pygame.time.Clock()

# ===================== TẢI HÌNH ẢNH =============================
bird_img = pygame.image.load("image/chim1.png").convert_alpha()
bird_img = pygame.transform.scale(bird_img, (BIRD_SIZE, BIRD_SIZE))

background_img = pygame.image.load("image/nen.png").convert()
background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))

# ====================== ÂM THANH ================================
pygame.mixer.music.load("sound/FrenchPop_01.ogg")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)

point_sound = pygame.mixer.Sound("sound/決定3.ogg")
hit_sound = pygame.mixer.Sound("sound/ツッコミ打撃2.ogg")
fall_sound = pygame.mixer.Sound("sound/ゲームオーバー.ogg")
start_sound1 = pygame.mixer.Sound("sound/笛ピッピー2.ogg")
start_sound_2 = pygame.mixer.Sound("sound/はじまるよ.ogg")
click_sound = pygame.mixer.Sound("sound/振り回す1.ogg")

# ===================== LỚP BIRD ================================
class Bird:
    def __init__(self):
        self.x = 100
        self.y = HEIGHT // 2
        self.velocity = 0

    def flap(self):
        self.velocity = FLAP_STRENGTH

    def update(self):
        self.velocity += GRAVITY
        self.y += self.velocity

    def draw(self):
        screen.blit(bird_img, (self.x, self.y))

# ===================== LỚP PIPE ================================
class Pipe:
    def __init__(self):
        self.x = WIDTH
        self.height = random.randint(150, 400)

    def update(self):
        self.x -= PIPE_SPEED

    def draw(self):
        pygame.draw.rect(screen, PIPE_GREEN, (self.x, 0, PIPE_WIDTH, self.height))
        pygame.draw.rect(screen, PIPE_GREEN, (self.x, self.height + PIPE_GAP, PIPE_WIDTH, HEIGHT))
        pygame.draw.rect(screen, BLACK, (self.x, 0, PIPE_WIDTH, self.height), 2)
        pygame.draw.rect(screen, BLACK, (self.x, self.height + PIPE_GAP, PIPE_WIDTH, HEIGHT), 2)

    def collide(self, bird):
        bird_rect = pygame.Rect(bird.x, bird.y, BIRD_SIZE, BIRD_SIZE)
        top_pipe = pygame.Rect(self.x, 0, PIPE_WIDTH, self.height)
        bottom_pipe = pygame.Rect(self.x, self.height + PIPE_GAP, PIPE_WIDTH, HEIGHT)
        return bird_rect.colliderect(top_pipe) or bird_rect.colliderect(bottom_pipe)

# ===================== HÀM KHỞI TẠO GAME ========================
def setup():
    global bird, pipes, score, game_over, game_started
    bird = Bird()
    pipes = [Pipe()]
    score = 0
    game_over = False
    game_started = False
    start_sound1.play()
    start_sound_2.play()

# ===================== HÀM MAIN ================================
async def main():
    global bird, pipes, score, game_over, game_started 
    setup()
    font = pygame.font.SysFont(None, 36)
    font_hint = pygame.font.SysFont(None, 30)

    running = True
    while running:
        screen.blit(background_img, (0, 0))

        # ==== Xử lý sự kiện ====
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not game_over:
                    if not game_started:
                        game_started = True
                    bird.flap()
                    click_sound.play()
                if event.key == pygame.K_r and game_over:
                    setup()

            if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                if not game_started:
                    game_started = True
                bird.flap()
                click_sound.play()

        # ==== Cập nhật trạng thái nếu chưa thua ====
        if not game_over and game_started:
            bird.update()

            for pipe in pipes[:]:
                pipe.update()
                if pipe.x + PIPE_WIDTH < 0:
                    pipes.remove(pipe)
                    score += 1
                    point_sound.play()

            if pipes[-1].x < WIDTH - 200:
                pipes.append(Pipe())

            for pipe in pipes:
                if pipe.collide(bird):
                    hit_sound.play()
                    fall_sound.play()
                    game_over = True
                    break

            if bird.y < 0 or bird.y + BIRD_SIZE > HEIGHT:
                game_over = True

        # ==== Vẽ các đối tượng ====
        for pipe in pipes:
            pipe.draw()
        bird.draw()

        # ==== Hiển thị điểm số ====
        score_text = font.render(str(score), True, WHITE, BLACK)
        screen.blit(score_text, (WIDTH // 2, 50))

        # ==== Thông báo Game Over ====
        if game_over:
            game_over_text = font.render("Game Over! Press R to Restart", True, WHITE, BLACK)
            screen.blit(game_over_text, (WIDTH // 2 - 150, HEIGHT // 2))

        # ==== Hướng dẫn bắt đầu ====
        if not game_started and not game_over:
            hint_text = font_hint.render("Press SPACE or click to start", True, WHITE, BLACK)
            screen.blit(hint_text, (WIDTH // 2 - 130, HEIGHT // 2 - 50))

        pygame.display.flip()
        clock.tick(FPS)
        await asyncio.sleep(0)

    pygame.quit()

# ===================== CHẠY GAME ================================
if __name__ == "__main__":
    asyncio.run(main())
