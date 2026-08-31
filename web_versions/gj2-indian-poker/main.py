# --- Web版 (pygbag対応のための自動変換コピー) ---
# 元ファイル: indian poker.py / ゲーム内容は変更していません
import asyncio

async def main():
    import pygame
    import sys
    import time
    import random
    import os


    if sys.platform == "win32":
        pass  # web: ctypes無効化 | import ctypes
        pass  # web: ctypes無効化 | ctypes.windll.user32.SetProcessDPIAware()

        os.environ['SDL_VIDEO_CENTERED'] = '1'
    elif sys.platform == "darwin":
        os.environ['SDL_VIDEO_WINDOW_POS'] = '100,100'
        os.environ['SDL_VIDEO_CENTERED'] = '1'
    elif sys.platform.startswith("linux"): 
        os.environ[ 
     'SDL_VIDEO_X11_NET_WM_BYPASS_COMPOSITOR'] = '0' 
        os.environ['SDL_VIDEO_CENTERED'] = '1'

    elif sys.platform.startswith("freebsd") or sys.platform.startswith("openbsd") or sys.platform.startswith("netbsd"):
        os.environ['SDL_VIDEO_CENTERED'] = '1'

    elif sys.platform.startswith("sunos"): 
       os.environ['SDL_VIDEO_CENTERED'] = '1'
    elif sys.platform.startswith("haiku"): 
       os.environ['SDL_VIDEO_WINDOW_POS'] = '50,50'
    elif sys.platform.startswith("android"): 
        os.environ['SDL_VIDEO_CENTERED'] = '1' 
        os.environ['SDL_VIDEODRIVER'] = 'android'
    elif sys.platform.startswith("emscripten"):
       print("Emscripten (WebAssembly) 環境:追加設定不要")
    elif sys.platform.startswith("cygwin") or sys.platform.startswith("msys"):
        os.environ['SDL_VIDEO_CENTERED'] = '1'
    elif sys.platform.startswith("riscos"):
        os.environ['SDL_VIDEO_CENTERED'] = '1'
    elif sys.platform.startswith("aix"):
        os.environ['SDL_VIDEO_CENTERED'] = '1'
    elif sys.platform.startswith("vxworks"):

        os.environ['SDL_VIDEO_CENTERED'] = '1'
    elif sys.platform.startswith("os2"):
        pass
    elif sys.platform.startswith("amiga"):
        os.environ['SDL_VIDEO_CENTERED'] = '1'


    else:
        print(f"警告: このOS ({sys.platform})は未検証です。動作しない可能性があります。")


    pygame.init()

    SCREEN_WIDTH = 1920
    SCREEN_HEIGHT = 1080
    screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT),pygame.FULLSCREEN)
    pygame.display.set_caption("pygame 基礎")

    #使いたい変数や画像
    blue2 = pygame.image.load("image/blue2.png")
    blue2 = pygame.transform.scale(blue2,(100,100))
    blue2 = pygame.transform.flip(blue2,True,False)
    blue2_rect = pygame.rect.Rect(500,0,100,100)

    red2 = pygame.image.load("image/red2.png")
    red2 = pygame.transform.scale(red2,(100,100))
    red2 = pygame.transform.flip(red2,True,False)
    red2_rect = pygame.rect.Rect(200,0,400,400)

    s1 = pygame.image.load("image/s1.png")
    s1 = pygame.transform.scale(s1,(100,100))
    s1 = pygame.transform.flip(s1,True,False)
    s1_rect = pygame.rect.Rect(500,0,100,100)

    s2 = pygame.image.load("image/s2.png")
    s2 = pygame.transform.scale(s2,(100,100))
    s2 = pygame.transform.flip(s2,True,False)
    s2_rect = pygame.rect.Rect(500,0,100,100)

    s3 = pygame.image.load("image/s3.png")
    s3 = pygame.transform.scale(s3,(100,100))
    s3 = pygame.transform.flip(s3,True,False)
    s3_rect = pygame.rect.Rect(500,0,100,100)

    s4 = pygame.image.load("image/s4.png")
    s4 = pygame.transform.scale(s4,(100,100))
    s4 = pygame.transform.flip(s4,True,False)
    s4_rect = pygame.rect.Rect(500,0,100,100)

    s5 = pygame.image.load("image/s5.png")
    s5 = pygame.transform.scale(s5,(100,100))
    s5 = pygame.transform.flip(s5,True,False)
    s5_rect = pygame.rect.Rect(500,0,100,100)

    s6 = pygame.image.load("image/s6.png")
    s6 = pygame.transform.scale(s6,(100,100))
    s6 = pygame.transform.flip(s6,True,False)
    s6_rect = pygame.rect.Rect(500,0,100,100)

    s7 = pygame.image.load("image/s7.png")
    s7 = pygame.transform.scale(s7,(100,100))
    s7 = pygame.transform.flip(s7,True,False)
    s7_rect = pygame.rect.Rect(500,0,100,100)

    s8 = pygame.image.load("image/s8.png")
    s8 = pygame.transform.scale(s8,(100,100))
    s8 = pygame.transform.flip(s8,True,False)
    s8_rect = pygame.rect.Rect(500,0,100,100)

    s9 = pygame.image.load("image/s9.png")
    s9 = pygame.transform.scale(s9,(100,100))
    s9 = pygame.transform.flip(s9,True,False)
    s9_rect = pygame.rect.Rect(500,0,100,100)

    s10 = pygame.image.load("image/s10.png")
    s10 = pygame.transform.scale(s10,(100,100))
    s10 = pygame.transform.flip(s10,True,False)
    s10_rect = pygame.rect.Rect(500,0,100,100)

    s11 = pygame.image.load("image/s11.png")
    s11 = pygame.transform.scale(s11,(100,100))
    s11 = pygame.transform.flip(s11,True,False)
    s11_rect = pygame.rect.Rect(500,0,100,100)

    s12 = pygame.image.load("image/s12.png")
    s12 = pygame.transform.scale(s12,(100,100))
    s12 = pygame.transform.flip(s12,True,False)
    s12_rect = pygame.rect.Rect(500,0,100,100)

    s13 = pygame.image.load("image/s13.png")
    s13 = pygame.transform.scale(s13,(100,100))
    s13 = pygame.transform.flip(s13,True,False)
    s13_rect = pygame.rect.Rect(500,0,100,100)

    h1 = pygame.image.load("image/h1.png")
    h1 = pygame.transform.scale(h1,(100,100))
    h1 = pygame.transform.flip(h1,True,False)
    h1_rect = pygame.rect.Rect(200,0,400,400)

    h2 = pygame.image.load("image/h2.png")
    h2 = pygame.transform.scale(h2,(100,100))
    h2 = pygame.transform.flip(h2,True,False)
    h2_rect = pygame.rect.Rect(200,0,400,400)

    h3 = pygame.image.load("image/h3.png")
    h3 = pygame.transform.scale(h3,(100,100))
    h3 = pygame.transform.flip(h3,True,False)
    h3_rect = pygame.rect.Rect(200,0,400,400)

    h4 = pygame.image.load("image/h4.png")
    h4 = pygame.transform.scale(h4,(100,100))
    h4 = pygame.transform.flip(h4,True,False)
    h4_rect = pygame.rect.Rect(200,0,400,400)

    h5 = pygame.image.load("image/h5.png")
    h5 = pygame.transform.scale(h5,(100,100))
    h5 = pygame.transform.flip(h5,True,False)
    h5_rect = pygame.rect.Rect(200,0,400,400)

    h6 = pygame.image.load("image/h6.png")
    h6 = pygame.transform.scale(h6,(100,100))
    h6 = pygame.transform.flip(h6,True,False)
    h6_rect = pygame.rect.Rect(200,0,400,400)

    h7 = pygame.image.load("image/h7.png")
    h7 = pygame.transform.scale(h7,(100,100))
    h7 = pygame.transform.flip(h7,True,False)
    h7_rect = pygame.rect.Rect(200,0,400,400)

    h8 = pygame.image.load("image/h8.png")
    h8 = pygame.transform.scale(h8,(100,100))
    h8 = pygame.transform.flip(h8,True,False)
    h8_rect = pygame.rect.Rect(200,0,400,400)

    h9 = pygame.image.load("image/h9.png")
    h9 = pygame.transform.scale(h9,(100,100))
    h9 = pygame.transform.flip(h9,True,False)
    h9_rect = pygame.rect.Rect(200,0,400,400)

    h10 = pygame.image.load("image/h10.png")
    h10 = pygame.transform.scale(h10,(100,100))
    h10 = pygame.transform.flip(h10,True,False)
    h10_rect = pygame.rect.Rect(200,0,400,400)

    h11 = pygame.image.load("image/h11.png")
    h11 = pygame.transform.scale(h11,(100,100))
    h11 = pygame.transform.flip(h11,True,False)
    h11_rect = pygame.rect.Rect(200,0,400,400)

    h12 = pygame.image.load("image/h12.png")
    h12 = pygame.transform.scale(h12,(100,100))
    h12 = pygame.transform.flip(h12,True,False)
    h12_rect = pygame.rect.Rect(200,0,400,400)

    h13 = pygame.image.load("image/h13.png")
    h13 = pygame.transform.scale(h13,(100,100))
    h13 = pygame.transform.flip(h13,True,False)
    h13_rect = pygame.rect.Rect(200,0,400,400)



    clock = pygame.time.Clock()




    runnning = True
    while runnning:

        clock.tick(60)
        await asyncio.sleep(0)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                runnning = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    runnning = False


        screen.fill((255,255,255))


    #追加機能や画像表示、音楽再生など

    import random
    my_card = random.randint(1,13)
    if my_card == 1:
        print(s1)

    elif my_card == 2:
        print(s2)

    elif my_card == 3:
        print(s3)

    elif my_card == 4:
        print(s4)

    elif my_card == 5:
        print(s5)

    elif my_card == 6:
        print(s6)

    elif my_card == 7:
        print(s7)

    elif my_card == 8:
        print(s8)

    elif my_card == 9:
        print(s9)

    elif my_card == 10:
        print(s10)

    elif my_card == 11:
        print(s11)

    elif my_card == 12:
        print(s12)

    else:
        print(s13)



    enemy_card = random.randint(1,13)
    if enemy_card == 1:
        print(h1)

    elif enemy_card == 2:
        print(h2)

    elif enemy_card == 3:
        print(h3)

    elif enemy_card == 4:
        print(h4)

    elif enemy_card == 5:
        print(h5)

    elif enemy_card == 6:
        print(h6)

    elif enemy_card == 7:
        print(h7)

    elif enemy_card == 8:
        print(h8)

    elif enemy_card == 9:
        print(h9)

    elif enemy_card == 10:
        print(h10)

    elif enemy_card == 11:
        print(h11)

    elif enemy_card == 12:
        print(h12)

    else:
        print(h13)


    if my_card > enemy_card:
        print("You win!!")

    elif my_card == enemy_card:
        print("Draw")

    else:
        print("You Lose…")




    #メインループ終了後
    pygame.quit()  
    return




asyncio.run(main())