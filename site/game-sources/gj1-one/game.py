import pygame
import sys
import random

pygame.init()

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT),pygame.FULLSCREEN)
pygame.display.set_caption("pygame 基礎")


#clear_img = pygame.image.load("images\good.png").convert_alpha()
#over_img = pygame.image.load("images\end.png").convert_alpha()



clook = pygame.time.Clock()

alphabet = chr(random.randint(97, 123))

scene = True



def START():
    font = pygame.font.SysFont(None, 200, bold=False, italic=False)
    text_surf = font.render("START", True, (255,0,0))
    screen.blit(text_surf, (550,350))
    pygame.display.update()




running = True
while running:

    clook.tick(60)

    if scene:
        START()
    

    for event in pygame.event.get():
      scene = False
      if event.type == pygame.KEYDOWN:
            push_key = pygame.key.name(event.key)

            
            
            if event.key == pygame.K_ESCAPE:
                running = False

            


            if alphabet == push_key:
                screen.fill((0,0,0))
                font = pygame.font.SysFont(None, 200, bold=False, italic=False)
                text_surf = font.render("Game Clear", True, (255,0,0))
                screen.blit(text_surf, (375,350))
                #screen.blit(clear_img, (100, 100))
                pygame.display.update()

            else:
                screen.fill((0,0,0))
                font = pygame.font.SysFont(None, 200, bold=False, italic=False)
                text_surf = font.render("Game Over", True, (255,0,0))
                screen.blit(text_surf, (375,350))
                #screen.blit(over_img, (100, 100))
                pygame.display.update()



            pygame.display.update()
            pygame.display.flip()

pygame.quit()
sys.exit()