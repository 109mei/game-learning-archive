# --- Web版 (pygbag対応のための変換コピー / ゲーム内容は変更していません) ---
import asyncio
#Download link: https://github.com/coderboe/FlyMan.git
#@auther Lu Taw & Min Thant Htin & Thae Htet Htet Khaing

# Import pygame library for game functions
import pygame
# Import random for pipe height randomness
import random
# Import sys for system exit
import sys
# Import os for file and path operations
import os
# Initialize all imported pygame modules
pygame.init()

# Set the width of the game window
WIDTH = 400
# Set the height of the game window
HEIGHT = 600
# Create the game window with specified width and height
screen = pygame.display.set_mode((WIDTH, HEIGHT))
# Set the window title to "Fly Man One Button"
pygame.display.set_caption("Fly Man One Button")
# Create a clock object to control the frame rate (FPS)
clock = pygame.time.Clock()
# Define the folder where game assets are stored
ASSETS = "assets"

# Load the man image from assets folder
MAN_IMG = pygame.image.load(os.path.join(ASSETS, "flyMan_fly.png"))

# Scale the man image to 40 pixels wide and 30 pixels tall
MAN_IMG = pygame.transform.scale(MAN_IMG, (40, 30))

# Load the sound effect for man flap
flap_sound = pygame.mixer.Sound(os.path.join(ASSETS, "flap.ogg"))

# Load the sound effect for scoring
score_sound = pygame.mixer.Sound(os.path.join(ASSETS, "score.ogg"))

# Load the sound effect for hitting an obstacle
hit_sound = pygame.mixer.Sound(os.path.join(ASSETS, "hit.ogg"))

# Set gravity acceleration for man falling
gravity = 0.5

# Set the flap power (negative velocity) for man to move upwards
flap_power = -10

# Set the initial gap between top and bottom pipes
initial_pipe_gap = 180

# Set minimum allowed pipe gap to increase difficulty
min_pipe_gap = 100

# Set the initial speed at which pipes move leftwards
initial_pipe_speed = 3

# Set the maximum speed pipes can reach as difficulty increases
max_pipe_speed = 8

# Initialize current pipe gap to starting gap value
pipe_gap = initial_pipe_gap

# Initialize current pipe speed to starting speed value
pipe_speed = initial_pipe_speed

# Set the width of each pipe rectangle
pipe_width = 70

# Set how many frames between spawning new pipes
pipe_spawn_delay = 150

# Set the fixed horizontal position of the man
man_x = 50

# Set the starting vertical position of the man (center of screen)
man_y = HEIGHT // 2

# Initialize man's vertical velocity to zero
man_velocity = 0

# Create an empty list to store pipes currently on screen
pipes = []

# Initialize player score to zero
score = 0

# Initialize high score to zero
high_score = 0

# If a highscore file exists, read and load the high score from it
if os.path.exists("highscore.txt"):
    with open("highscore.txt", "r") as f:
        high_score = int(f.read())

# Create the main font for displaying score and text
font = pygame.font.SysFont(None, 40)

# Create a smaller font for buttons and info text
small_font = pygame.font.SysFont(None, 28)

# Define a Button class to create interactive buttons easily
class Button:
    # Initialize with rectangle, text, font, and colors
    def __init__(self, rect, text, font, bg_color=(100, 100, 100), fg_color=(255, 255, 255)):
        self.rect = pygame.Rect(rect)       # Rectangle for button area
        self.text = text                    # Text label of the button
        self.font = font                    # Font object to render text
        self.bg_color = bg_color            # Background color
        self.fg_color = fg_color            # Text color
        self.hovered = False                # Is mouse hovering?

    # Draw the button on given surface
    def draw(self, surf):
        # Change color when hovered
        color = (150, 150, 150) if self.hovered else self.bg_color
        pygame.draw.rect(surf, color, self.rect)   # Draw button rectangle
        txt_surf = self.font.render(self.text, True, self.fg_color)  # Render text surface
        txt_rect = txt_surf.get_rect(center=self.rect.center)       # Center text
        surf.blit(txt_surf, txt_rect)                                # Draw text on button

    # Update hovered status based on mouse position
    def check_hover(self, mouse_pos):
        self.hovered = self.rect.collidepoint(mouse_pos)

    # Check if button was clicked in an event
    def is_clicked(self, event):
        # Return True only if mouse clicked and hovering over button
        return event.type == pygame.MOUSEBUTTONDOWN and self.hovered and event.button == 1

# Function to draw vertical gradient background from sky blue to white
def draw_gradient_background():
    top_color = (135, 206, 250)      # Top color: sky blue
    bottom_color = (255, 255, 255)   # Bottom color: white
    # Draw line for each y position with interpolated color
    for y in range(HEIGHT):
        ratio = y / HEIGHT
        r = int(top_color[0] * (1 - ratio) + bottom_color[0] * ratio)
        g = int(top_color[1] * (1 - ratio) + bottom_color[1] * ratio)
        b = int(top_color[2] * (1 - ratio) + bottom_color[2] * ratio)
        pygame.draw.line(screen, (r, g, b), (0, y), (WIDTH, y))

# Function to draw the man sprite at vertical position y
def draw_man(y):
    screen.blit(MAN_IMG, (man_x, int(y)))

# Function to create a new pipe pair with random top pipe height
def create_pipe():
    top_height = random.randint(50, HEIGHT - pipe_gap - 100)   # Random top pipe height
    bottom_y = top_height + pipe_gap                            # Bottom pipe starts after gap
    pipes.append({'x': WIDTH, 'top': top_height, 'bottom': bottom_y})  # Append pipe dict

# Function to move pipes left and check scoring
def move_pipes():
    global score
    for pipe in pipes:
        pipe['x'] -= pipe_speed           # Move pipe left by pipe_speed
        # Check if man just passed pipe (score point)
        if pipe['x'] + pipe_width == man_x:
            score += 1                    # Increment score
            score_sound.play()            # Play scoring sound
            update_difficulty()           # Increase game difficulty
    # Remove pipe if it moves off screen left
    if pipes and pipes[0]['x'] < -pipe_width:
        pipes.pop(0)

# Function to draw all pipes on screen
def draw_pipes():
    for pipe in pipes:
        # Draw top pipe rectangle
        pygame.draw.rect(screen, (0, 255, 0), (pipe['x'], 0, pipe_width, pipe['top']))
        # Draw bottom pipe rectangle
        pygame.draw.rect(screen, (0, 255, 0), (pipe['x'], pipe['bottom'], pipe_width, HEIGHT))

# Function to check collision with pipes or boundaries
def check_collision(y):
    if y <= 0 or y + 30 >= HEIGHT:       # If man hits top or bottom screen
        return True
    for pipe in pipes:
        # Check if man horizontally overlaps pipe
        if man_x + 40 > pipe['x'] and man_x < pipe['x'] + pipe_width:
            # Check vertical collision with pipes
            if y < pipe['top'] or y + 30 > pipe['bottom']:
                return True
    return False

# Function to display current score and high score
def show_text():
    score_text = font.render(f"Score: {score}", True, (0, 0, 0))
    high_text = font.render(f"High Score: {high_score}", True, (0, 0, 0))
    screen.blit(score_text, (10, 10))
    screen.blit(high_text, (10, 50))

# Reset the game state variables for restarting
def reset_game():
    global man_y, man_velocity, pipes, score, pipe_speed, pipe_gap
    man_y = HEIGHT // 2            # Reset man vertical position
    man_velocity = 0               # Reset man velocity
    pipes = []                     # Clear all pipes
    score = 0                      # Reset score
    pipe_speed = initial_pipe_speed # Reset pipe speed
    pipe_gap = initial_pipe_gap     # Reset pipe gap

# Increase difficulty based on score
def update_difficulty():
    global pipe_speed, pipe_gap
    # Increase speed but cap at max_pipe_speed
    pipe_speed = min(initial_pipe_speed + score // 5, max_pipe_speed)
    # Decrease gap but no smaller than min_pipe_gap
    pipe_gap = max(initial_pipe_gap - score * 5, min_pipe_gap)

# Draw Exit button during gameplay
def draw_in_game_exit_button():
    exit_rect = pygame.Rect(WIDTH - 80, 10, 70, 35)               # Rectangle area for Exit button
    pygame.draw.rect(screen, (200, 0, 0), exit_rect)              # Draw red button rectangle
    txt = small_font.render("Exit", True, (255, 255, 255))       # Render Exit text
    txt_rect = txt.get_rect(center=exit_rect.center)              # Center text inside button
    screen.blit(txt, txt_rect)                                    # Draw text on button
    return exit_rect                                              # Return rect for click detection

# Prepare menu buttons on right side with text labels
menu_buttons = []
button_width = 120
button_height = 40
button_x = WIDTH - button_width - 10
button_spacing = 10
menu_texts = ["Start", "Help", "About", "Exit"]

# Create Button objects for each menu item
for i, text in enumerate(menu_texts):
    rect = (button_x, 50 + i*(button_height + button_spacing), button_width, button_height)
    menu_buttons.append(Button(rect, text, font))

# Define game states for controlling flow
IN_MENU = 0
IN_GAME = 1
IN_HELP = 2
IN_ABOUT = 3

# Start with the menu shown
state = IN_MENU

running = True                  # Main loop control variable
frame_count = 0                # Frame counter for pipe spawning
game_over = False              # Game over flag

# Main game loop

async def main():
    global about_lines, button, event, exit_button_rect, f, frame_count, game_over, game_over_text, help_lines, high_score, i, line, man_velocity, man_y, mouse_pos, state, title_rect, title_surf, txt
    while running:

        # Cap frame rate at 60 FPS
        clock.tick(60)
        await asyncio.sleep(0)

        # Get current mouse position for hover effects
        mouse_pos = pygame.mouse.get_pos()

        # Event handling loop
        for event in pygame.event.get():

            # Handle window close button
            if event.type == pygame.QUIT:
                with open("highscore.txt", "w") as f:
                    f.write(str(max(score, high_score)))   # Save high score
                pygame.quit()
                return

            # Event handling based on current state
            if state == IN_MENU:
                # Check all menu buttons for clicks
                for button in menu_buttons:
                    if button.is_clicked(event):
                        if button.text == "Start":
                            reset_game()
                            state = IN_GAME
                            game_over = False
                        elif button.text == "Help":
                            state = IN_HELP
                        elif button.text == "About":
                            state = IN_ABOUT
                        elif button.text == "Exit":
                            pygame.quit()
                            return

            elif state == IN_GAME:
                # Keyboard events during gameplay
                if event.type == pygame.KEYDOWN:
                    if not game_over and event.key == pygame.K_SPACE:
                        man_velocity = flap_power
                        flap_sound.play()
                    if game_over and event.key == pygame.K_r:
                        reset_game()
                        game_over = False

                # Mouse click for in-game exit button
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    exit_button_rect = pygame.Rect(WIDTH - 80, 10, 70, 35)
                    if exit_button_rect.collidepoint(event.pos):
                        state = IN_MENU

            else:
                # IN_HELP or IN_ABOUT: ESC returns to menu
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    state = IN_MENU

        # Clear screen each frame
        screen.fill((255, 255, 255))

        # Draw according to current state
        if state == IN_MENU:
            draw_gradient_background()  # Draw background gradient

            # Update hover states and draw buttons
            for button in menu_buttons:
                button.check_hover(mouse_pos)
                button.draw(screen)

            # Draw title centered on left side
            title_surf = font.render("Fly Man", True, (0, 0, 0))
            title_rect = title_surf.get_rect(center=(WIDTH//2 - 50, 30))
            screen.blit(title_surf, title_rect)

        elif state == IN_HELP:
            # Fill background for help screen
            screen.fill((230, 230, 250))

            # Lines of help text
            help_lines = [
                "Help:",
                "- Press SPACEBAR to flap",
                "- Avoid pipes",
                "- Press R to restart on game over",
                "- Click Exit to return to menu",
                "- ESC to go back to menu"
            ]

            # Render and display each line of help text
            for i, line in enumerate(help_lines):
                txt = small_font.render(line, True, (0, 0, 0))
                screen.blit(txt, (20, 40 + i*30))

        elif state == IN_ABOUT:
            # Fill background for about screen
            screen.fill((245, 245, 220))

            # Lines of about text
            about_lines = [
                "About:",
                "Fly Man is a simple game created",
                "by Lu Taw ,Min Thant Htin & Thae",
                "HtetHtet Khaing. OneButton Game",
                "created with Python & Pygame.",
                "Enjoy the game!",
                "ESC to return to menu"
            ]

            # Render and display each line of about text
            for i, line in enumerate(about_lines):
                txt = small_font.render(line, True, (0, 0, 0))
                screen.blit(txt, (20, 40 + i*30))

        elif state == IN_GAME:
            draw_gradient_background()  # Draw game background

            if not game_over:
                man_velocity += gravity  # Apply gravity to man
                man_y += man_velocity   # Update man position

                # Spawn new pipes every pipe_spawn_delay frames
                if frame_count % pipe_spawn_delay == 0:
                    create_pipe()

                move_pipes()              # Move pipes left and update score
                draw_pipes()              # Draw pipes
                draw_man(man_y)         # Draw man
                show_text()               # Show current score and high score

                # Check collisions
                if check_collision(man_y):
                    game_over = True
                    hit_sound.play()
                    if score > high_score:
                        high_score = score

                frame_count += 1
            else:
                # Display Game Over text with restart instructions
                game_over_text = font.render("Game Over! R to Restart", True, (255, 0, 0))
                screen.blit(game_over_text, (WIDTH // 2 - 130, HEIGHT // 2))

            # Draw Exit button on top right during game
            exit_button_rect = draw_in_game_exit_button()

        # Update the full display surface to the screen
        pygame.display.update()


asyncio.run(main())