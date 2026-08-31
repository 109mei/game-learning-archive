# --- Web版 (pygbag対応のための変換コピー / ゲーム内容は変更していません) ---
import asyncio
#使用モジュール
import pygame
import sys
# import numpy  # web: 未使用のため無効化
import time
import random

#初期化
pygame.init()

#ウィンドウ作成
SCREEN_WIDTH = 512 
SCREEN_HEIGHT = 480 
screen=pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pygame.display.set_caption("jamgeme")

#主人公
player_img=pygame.image.load("selected_images/player_07.png").convert_alpha()
player_img=pygame.transform.scale(player_img,(32,32))
px,py=256,400


#敵
enemy_img=pygame.image.load("selected_images/platformPack_tile044.png").convert_alpha()
enemy_img=pygame.transform.scale(enemy_img,(64,64))
enemyX=random.randint(0,448)
enemyY=random.randint(50,150)
enemyX_change,enemyY_change=4,40

#ボタン画像読み込み、座標、サイズ、色
btn_img=pygame.image.load("selected_images/lile_0578.png")
btn_img=pygame.transform.scale(btn_img,(64,64))
button_x = 300 #座標
button_y = 200 #座標
button_w = 16 #サイズ
button_h = 16 #サイズ
button_color = (255,255,255)       #ボタンの色（グレー）
button_color_hover = (255,255,255) #マウスが乗った時の色

#状態を表す定数
STATE_TITLE=0
STATE_MAIN=1
STATE_RESULT=2
game_state=STATE_TITLE

#フォント
font=pygame.font.Font(None,55)

#画像を描画
def player(x,y):
    screen.blit(player_img,(x,y))
def enemy(x,y):
    screen.blit(enemy_img,(x,y))

#タイトル画面
def draw_title_screen():
    global game_state
    screen.fill((0,0,100))
    font=pygame.font.SysFont(None,60)
    text_surf=font.render("TITLE:Press ENTER", True,(233, 218, 240))
    screen.blit(text_surf,(50,250))

#メインゲーム画面
def draw_main_game():
    global game_state
    screen.fill((181, 129, 204))
    font=pygame.font.SysFont(None,40)

#リザルト画面
def draw_result_screen():
    global game_state
    if game_clear:
        screen.fill((54, 112, 207)) #クリア時の背景色
    else:
        screen.fill((148, 37, 70)) #ゲームオーバー時の背景色
    
    font=pygame.font.SysFont(None,40)

def handle_result_button():
    global game_state
    game_state=STATE_TITLE

#メインループ
clock=pygame.time.Clock()
running = True
pressed_keys=pygame.key.get_pressed()
start_time=None #ゲーム開始時間
game_clear=False


async def main():
    global btn, color, current_time, enemyX, enemyX_change, enemyY, enemyY_change, enemy_rect, event, game_clear, game_state, keys, msg, msg2, mx, my, player_rect, pressed_keys, px, py, running, start_time
    while running: 
        clock.tick(60) #フレームレート（FPS）を60に制限
        await asyncio.sleep(0)
        keys=pygame.key.get_pressed()
        pressed_keys=keys

        #イベント処理
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT: #もしウィンドウの✕ボタンが押されたら
                running = False #変数runningにFslseを代入
            elif event.type == pygame.KEYDOWN: #もし何かキーが押されたら
                if event.key ==pygame.K_ESCAPE:
                    running = False
                elif event.key==pygame.K_RETURN and game_state==STATE_RESULT:
                    if game_clear:
                        handle_result_button()
                        game_state=STATE_TITLE


            #ボタン
            elif event.type==pygame.MOUSEBUTTONDOWN:
                if event.button==1: #左クリック
                    mx,my=pygame.mouse.get_pos()
                    if game_state==STATE_RESULT:
                        if (button_x <=mx <=button_x+button_w)and(button_y <= my <= button_y +button_h):
                            handle_result_button()
                            game_state=STATE_TITLE
            elif event.type==pygame.KEYDOWN:
                if event.key==pygame.K_ESCAPE:
                    running=False

        #タイトル画面（エンターキーでメイン画面へ）
        if game_state == STATE_TITLE:
            draw_title_screen()
            if keys[pygame.K_RETURN]:
                game_state=STATE_MAIN
                start_time=pygame.time.get_ticks()
                game_clear=False

                #主人公、敵の位置リセット
                px,py=256,400
                enemyX=random.randint(0,448)
                enemyY=random.randint(50,150)
                enemyX_change=4
                enemyY_change=40

        #メイン画面
        elif game_state==STATE_MAIN:
            draw_main_game()

            #主人公移動
            if pressed_keys[pygame.K_LEFT]:
                px -=5
            elif pressed_keys[pygame.K_RIGHT]:
                px +=5
            elif pressed_keys[pygame.K_UP]:
                py -=5
            elif pressed_keys[pygame.K_DOWN]:
                py +=5

            #敵移動
            enemyX +=enemyX_change
            if enemyX <= 0:
                enemyX_change = 16
                enemyY += enemyY_change
            elif enemyX >=448:
                enemyX_change = -16
                enemyY += enemyY_change

            #当たり判定
            player_rect=pygame.Rect(px,py,32,32)
            enemy_rect=pygame.Rect(enemyX,enemyY,64,64)

            if player_rect.colliderect(enemy_rect):
                game_clear=False
                game_state=STATE_RESULT #敵に当たったらゲームオーバーでリザルト画面へ

            #一定時間経過でクリア
            current_time=pygame.time.get_ticks()
            if current_time - start_time >= 5000:
                game_clear=True
                game_state=STATE_RESULT

            #主人公、敵の描画
            player(px,py)
            enemy(enemyX,enemyY)

        #リザルト画面
        elif game_state==STATE_RESULT:
            draw_result_screen()

            #ゲームオーバー、クリアの表示
            if game_clear:
                msg=font.render("CLEAR!!", True,(0,255,0))
                screen.blit(msg,(130,210))
                msg2=font.render("press the button!", True,(0,255,0))
                screen.blit(msg2,(110,280))

                #ボタンを描画
                mx,my=pygame.mouse.get_pos()
                if (button_x <=mx <=button_x+button_w)and(button_y <= my <= button_y +button_h):
                    color=button_color_hover
                else:
                    color=button_color
                pygame.draw.rect(screen,color,(button_x,button_y,button_w,button_h))
                btn=screen.blit(btn_img,(275,175))

            else:
                msg=font.render("GAME OVER!", True,(255,0,0))
                screen.blit(msg,(130,235))

        #画面の更新
        pygame.display.flip()

    #メインループ終了後実行
    pygame.quit() #ウィンドウを閉じる
    sys.exit() #プログラムを終了する

asyncio.run(main())