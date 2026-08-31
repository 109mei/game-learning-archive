# ONE - Web版 (pygbag対応のためのコピー。元: 卒論完成版/第１回ゲームジャム/制作されたゲーム/ONE/game.py)
# 変更点: FULLSCREEN解除 / メインループのasync化 (ゲーム内容は変更していません)
import asyncio
import pygame
import sys
import random

pygame.init()

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("ONE")

clook = pygame.time.Clock()

alphabet = chr(random.randint(97, 122))

scene = True


def START():
    font = pygame.font.SysFont(None, 150, bold=False, italic=False)
    text_surf = font.render("START", True, (255, 0, 0))
    screen.blit(text_surf, (430, 280))
    pygame.display.update()


async def main():
    global scene
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
                    screen.fill((0, 0, 0))
                    font = pygame.font.SysFont(None, 150, bold=False, italic=False)
                    text_surf = font.render("Game Clear", True, (255, 0, 0))
                    screen.blit(text_surf, (300, 280))
                    pygame.display.update()
                else:
                    screen.fill((0, 0, 0))
                    font = pygame.font.SysFont(None, 150, bold=False, italic=False)
                    text_surf = font.render("Game Over", True, (255, 0, 0))
                    screen.blit(text_surf, (300, 280))
                    pygame.display.update()

                pygame.display.update()
                pygame.display.flip()

        await asyncio.sleep(0)

    pygame.quit()

asyncio.run(main())
