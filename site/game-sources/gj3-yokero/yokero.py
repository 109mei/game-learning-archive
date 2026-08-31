594028317640159284710362945801763492057381# coding: utf-8
import sys
import numpy as np #行列等を使うためのモジュール
import time #数秒待つ等を使うためのモジュール
import random #ランダムを使うためのモジュール
import sys  # sysモジュールはOS判定やプラットフォーム情報を取得するために使用します
import pygame  # ゲームライブラリPygameを読み込みます
from pygame.locals import *  # Pygameの定数を直接参照できるようにします
import os  # osモジュールは環境変数の設定に利用します
#初期化
pygame.init()
pygame.mixer.init()

# ↓あると便利なもの これがないとパソコンの設定から拡大・縮小率を100%に手動でしなければならない
# OS判定と適切な設定を適用
if sys.platform == "win32":  # Windows
    import ctypes
    ctypes.windll.user32.SetProcessDPIAware()
    # DPIスケール無効
    os.environ['SDL_VIDEO_CENTERED'] = '1'

elif sys.platform == "darwin":  # macOS
    os.environ['SDL_VIDEO_WINDOW_POS'] = '100,100'
    os.environ['SDL_VIDEO_CENTERED'] = '1'

elif sys.platform.startswith("linux"):  # Linux
    os.environ['SDL_VIDEO_X11_NET_WM_BYPASS_COMPOSITOR'] = '0'
    os.environ['SDL_VIDEO_CENTERED'] = '1'

elif sys.platform.startswith("freebsd") or sys.platform.startswith("openbsd") or sys.platform.startswith("netbsd"):  # BSD系
    os.environ['SDL_VIDEO_CENTERED'] = '1'

elif sys.platform.startswith("sunos"):  # Solaris
    os.environ['SDL_VIDEO_CENTERED'] = '1'

elif sys.platform.startswith("haiku"):  # Haiku OS
    os.environ['SDL_VIDEO_WINDOW_POS'] = '50,50'

elif sys.platform.startswith("android"):  # Android
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    os.environ['SDL_VIDEODRIVER'] = 'android'  # Android専用設定

elif sys.platform.startswith("emscripten"):  # WebAssembly
    print("Emscripten (WebAssembly) 環境: 追加設定不要")

elif sys.platform.startswith("cygwin") or sys.platform.startswith("msys"):  # Cygwin / MSYS2
    os.environ['SDL_VIDEO_CENTERED'] = '1'

elif sys.platform.startswith("riscos"):  # RISC OS
    os.environ['SDL_VIDEO_CENTERED'] = '1'

elif sys.platform.startswith("aix"):  # IBM AIX
    os.environ['SDL_VIDEO_CENTERED'] = '1'

elif sys.platform.startswith("vwxorks"):  # VxWorks
    os.environ['SDL_VIDEO_CENTERED'] = '1'

elif sys.platform.startswith("os2"):  # OS/2
    os.environ['SDL_VIDEO_CENTERED'] = '1'

elif sys.platform.startswith("amiga"):  # AmigaOS / MorphOS
    os.environ['SDL_VIDEO_CENTERED'] = '1'

else:  # その他の未知のOS
    print(f"警告: このOS（{sys.platform}）は未検証です。動作しない可能性があります。")

FONT_PATH = "NotoSansJP-Regular.ttf"  # 日本語表示用フォントファイルのパス。存在しない場合は適宜置き換えてください。
FONT_SIZE = 28  # フォントサイズ,文字の大きさを指定します。
try:  # 指定したフォントファイルの読み込みを試みます
    font_default = pygame.font.Font(FONT_PATH, 28)  # 指定したフォントファイルとサイズでフォントオブジェクトを生成します。
    font_large=pygame.font.Font(FONT_PATH, 140)
except IOError:  # フォントファイルが読み込めない場合の例外処理
    # フォントが読み込めない場合はデフォルトフォントを使用します。
    font_default = pygame.font.SysFont(None, 28)  # システムデフォルトフォントを取得します
    font_large=pygame.font.Font(None, 280)
    print("警告: 指定したフォントが見つかりません。デフォルトフォントを使用します。")  # 標準出力に警告を表示します
#pygame.font.Font(FONT_PATH, FONT_SIZE)  # 指定したフォントファイルとサイズでフォントオブジェクトを生成します。

#ここから↑は基本何も変更する必要がない

#ウィンドウ作成
W, H = 1920, 1080# 画面の横幅と縦幅を指定します
screen = pygame.display.set_mode((W, H))# 指定したサイズのウィンドウを生成します
screen.fill((240, 240, 240))


# 使いたい変数や画像などをここで定義
shougaibutu_img = pygame.image.load("asset/画像/24.png").convert_alpha() #透明化処理されている画像の部分が透明化になる
shougaibutu_img=pygame.transform.scale(shougaibutu_img, (40, 160))
coin_img=pygame.image.load("asset/画像/82.png").convert_alpha()
coin_img=pygame.transform.scale(coin_img, (40, 40))
character_fall_img=pygame.transform.scale(pygame.image.load("asset/画像/80.png"), (50, 50))
character_rise_img=pygame.transform.scale(pygame.image.load("asset/画像/81.png"), (50, 50))
scenery_img_1=pygame.image.load("asset/画像/12.png").convert_alpha()
scenery_img_2=pygame.image.load("asset/画像/13.png").convert_alpha()
scenery_img_3=pygame.image.load("asset/画像/14.png").convert_alpha()
heart_img=pygame.image.load("asset/画像/136.png").convert_alpha()
resistance_character_fall_img=pygame.transform.scale(pygame.image.load("asset/画像/80_white.png"), (50, 50))
resistance_character_rise_img=pygame.transform.scale(pygame.image.load("asset/画像/81_white.png"), (50, 50))




BGM_menu="asset/効果音・BGM/menu.mp3"
BGM_rule="asset/効果音・BGM/rule.mp3"
BGM_game="asset/効果音・BGM/game.mp3"
choose_sound=pygame.mixer.Sound("asset/効果音・BGM/14.mp3")
choose_sound.set_volume(0.3)
decision_sound=pygame.mixer.Sound("asset/効果音・BGM/6.mp3")
decision_sound.set_volume(0.3)
start_sound=pygame.mixer.Sound("asset/効果音・BGM/13.mp3")
start_sound.set_volume(0.3)
accel_sound=pygame.mixer.Sound("asset/効果音・BGM/10.mp3")
accel_sound.set_volume(0.3)
damage_sound=pygame.mixer.Sound("asset/効果音・BGM/1.mp3")
damage_sound.set_volume(0.3)
get_coin_sound=pygame.mixer.Sound("asset/効果音・BGM/7.mp3")
get_coin_sound.set_volume(0.3)
get_heart_sound=pygame.mixer.Sound("asset/効果音・BGM/5.mp3")
get_heart_sound.set_volume(0.3)

clock = pygame.time.Clock() #フレームレート取得
 
#pygame.display.set_caption("04 シーン遷移の例")  # ウィンドウタイトルを設定します

# フォント読み込み



# ---------- 色の定義 ----------
# 色はRGB(A)の4要素またはRGBの3要素のタプルで指定します【792189879171763†L71-L79】。
# 赤、緑、青は0〜255の整数値で指定し、アルファ値は255で不透明を意味します【276529072627999†L90-L95】。
WHITE = (255, 255, 255)  
RED = (250, 140, 80) 
BLUE = (80, 170, 250)  
GREEN = (80, 250, 140)  



#表示する画面を設定する変数
point=0
high_score=0
scine="menu"
choice=0      #choiceはmenuでの次の操作を決定するための変数、スペースで決定で、０の時はゲームスタート、１の時はルール説明、２でゲームの終了
last_scine="phantom"

def change_music(music):
    try:  # BGMファイルの読み込みを試みます
        pygame.mixer.music.load(music) # BGMファイルを読み込みます
        pygame.mixer.music.set_volume(0.1)
        pygame.mixer.music.play(-1)  # -1を指定するとBGMをループ再生します
        bgm_loaded = True  # 読み込みが成功したのでフラグを更新します
    except Exception as e:  # 読み込みに失敗した場合に実行されます
        print(f"BGMを読み込めませんでした: {e}")  # エラーメッセージを表示します
    #   パスを真似して間違わないようにしよう
    

def object_stick(img,x,start_y,goal_y,width_x,width_y):#ｙ座標のスタートとゴールを指定してその範囲を任意の画像で敷き詰めたリストを出力する関数
    imgs_list=[]
    last_y=start_y
    if goal_y<start_y:
        
        while goal_y<last_y:
            last_y=last_y-width_y
            imgs_list.append({"img":img,"x":x,"y":last_y})
            
    else:
        while goal_y>last_y:
            
            imgs_list.append({"img":img,"x":x,"y":last_y})
            last_y=last_y+width_y

    return imgs_list

def object(img,x,y,width,height):
    list={"judgment":pygame.Rect(x,y,width,height),"img":[{"img":img,"x":x,"y":y}]}
    
    return list

def scroll_object(list,velocity):#image_stickで作成したリストをx座標について指定した速度で移動させる関数
    for all in list:
        all["judgment"].x+=velocity
        coordinate=all["judgment"].x
        for all in all["img"]:
            all["x"]=coordinate
    
    return 

def draw(list):#image_stickで作成したリストの画像を描く関数、出力はリストになっている
    bilts=[]
    if list==[]:
        pass
    else:
        for all in list:
            all=all["img"]
            for all in all:
                img=all["img"]
                x=all["x"]
                y=all["y"]
                bilts.append(screen.blit(img,(x,y)))

    return bilts

def ad_massage(masage,x,y):
    bilts=[]
    
    for all in masage:
        title = font_default.render(all, True, (0, 0, 0))
        bilts.append(screen.blit(title, (x, y)))
        x+=title.get_width()
    
    return bilts

#メインループ
running = True    #変数をrunningにTrueを代入
while running:    #変数runningがTrueである間繰り返す（他の変数名、Trueだけでも可）

    clock.tick(60)  #フレームレート（fps）を60に制限
    #screen.fill((128,0,0)) #背景色(RGB)を描画　これを一番下に持っていき実行すると画面が全部白くなるので注意、背景は最初に持ってこよう
    keys = pygame.key.get_pressed()  # 押されているキーの状態を辞書形式で取得

    #イベント取得
    for event in pygame.event.get(): #もし何か（キーが押された、マウスが動いた、クリックされた等）が起きた場合を検知
        if event.type == pygame.QUIT: #もしウィンドウの×ボタンが押されたなら（フルスクリーンでは表示不可）
            running = False #変数runningにFalseを代入（runningがTrueではないためメインループが終了する）
        if event.type == pygame.KEYDOWN: #もし何かキーが押されたなら
            if event.key == pygame.K_ESCAPE: #押されたキーがもしエスケープキーなら
                running = False  #変数runningにFalseを代入（runningがTrueではないためメインループが終了する）
            elif scine=="menu":#menuの画面でのボタンを押したとき一時的な動き
                
                if event.key== pygame.K_DOWN:
                    if choice!=2:
                        choice+=1
                        choose_sound.play()
                elif event.key==pygame.K_UP:
                    if choice!=0:
                        choice-=1
                        choose_sound.play()
                elif event.key == pygame.K_RETURN:
                    decision_sound.play()
                    if choice==0:
                        scine="shougaibutu_game"
                    elif choice==1:
                        keep_point=point
                        point=0
                        last_point=0
                        speed=0
                        last_speed=0
                        shougaibutu=[]
                        coin=[]
                        hearts=[]
                        character=[{"judgment":pygame.Rect(50, 50, 50, 50),"img":[{"img":character_fall_img,"x":50,"y":50}]}]
                        Fall_judgment = pygame.Rect(0, H, W, 1)
                        ceiling=pygame.Rect(0 , 0 , H , 1)

                        scine="tutorial"
                        tutorial_page=0
                    elif choice==2:
                        running=False
            elif scine=="tutorial":
                if tutorial_page==2:
                    if event.key==pygame.K_UP:
                        level+=1
                    elif event.key==pygame.K_DOWN:
                        level+=-1
                if event.key== pygame.K_RETURN:
                    point=0
                    last_point=0
                    speed=0
                    last_speed=0
                    level=0
                    HP=1
                    shougaibutu=[]
                    coin=[]
                    hearts=[]
                    character=[{"judgment":pygame.Rect(50, 50, 50, 50),"img":[{"img":character_fall_img,"x":50,"y":50}]}]
                    shougaibutu_previous_time=time.time()-3
                    resistance=0
                    

                    if tutorial_page==2:
                        point=keep_point
                        scine="menu"
                        
                    else:
                        tutorial_page+=1

            
    

                    
    #上のボタンが押された時の一時的な処理の欄は必要なかった可能性が高い
    #どうせエンターしか使わないのにほかのキーを押したときの処理を作ったのは意味がないね



    #シーンによって画面を分岐
    if scine == "menu":#menuで表示する画面
        if last_scine!=scine:
            change_music(BGM_menu)
        last_scine=scine

        if high_score<point:
            high_score=point


        screen.fill((240, 240, 240))

        message="避けろ！"
        text_surface = font_large.render(message, True, (0, 0, 0))  # テキストをSurfaceに変換する
        screen.blit(text_surface, (720, H -  980))
        if choice==0:
            message="スタート"
            text_surface = font_default.render(message, True, (255, 99, 71))  # テキストをSurfaceに変換する
            screen.blit(text_surface, (870, H -  560))
            message="チュートリアル"
            text_surface = font_default.render(message, True, (0, 0, 0))  # テキストをSurfaceに変換する
            screen.blit(text_surface, (870, H -  530))
            message="終了"
            text_surface = font_default.render(message, True, (0, 0, 0))  # テキストをSurfaceに変換する
            screen.blit(text_surface, (870, H -  500))
        elif choice==1:
            message="スタート"
            text_surface = font_default.render(message, True, (0, 0, 0))  # テキストをSurfaceに変換する
            screen.blit(text_surface, (870, H -  560))
            message="チュートリアル"
            text_surface = font_default.render(message, True, (255, 99, 71))  # テキストをSurfaceに変換する
            screen.blit(text_surface, (870, H -  530))
            message="終了"
            text_surface = font_default.render(message, True, (0, 0, 0))  # テキストをSurfaceに変換する
            screen.blit(text_surface, (870, H -  500))
        elif choice==2:
            message="スタート"
            text_surface = font_default.render(message, True, (0, 0, 0))  # テキストをSurfaceに変換する
            screen.blit(text_surface, (870, H -  560))
            message="チュートリアル"
            text_surface = font_default.render(message, True, (0, 0, 0))  # テキストをSurfaceに変換する
            screen.blit(text_surface, (870, H -  530))
            message="終了"
            text_surface = font_default.render(message, True, (255, 99, 71))  # テキストをSurfaceに変換する
            screen.blit(text_surface, (870, H -  500))
        message="ハイスコア"
        text_surface = font_default.render(message, True, (0, 0, 0))  # テキストをSurfaceに変換する
        screen.blit(text_surface, (750, H -  680))
        message=str(high_score)
        text_surface = font_default.render(message, True, (0, 0, 0))  # テキストをSurfaceに変換する
        screen.blit(text_surface, (960, H -  680))

        message="前回のスコア"
        text_surface = font_default.render(message, True, (0, 0, 0))  # テキストをSurfaceに変換する
        screen.blit(text_surface, (750, H -  650))
        message=str(point)
        text_surface = font_default.render(message, True, (0, 0, 0))  # テキストをSurfaceに変換する
        screen.blit(text_surface, (960, H -  650))
    elif scine=="tutorial" :
        if last_scine!=scine:
            change_music(BGM_rule)
        last_scine=scine
        screen.fill((240, 240, 240))
        if tutorial_page==0:

            if last_speed*speed<0:

                if speed>0:
                    character[0]["img"][0]["img"]=character_fall_img
                else:
                   character[0]["img"][0]["img"]=character_rise_img
            
            if keys[K_SPACE]:#エンターが押されたときに上に加速するやつ
                speed+=-0.6
            else:
                if speed>0: 
                    speed+=0.2
                else:
                    speed+=0.4
        
            
            if character[0]["judgment"].y>H:#落下したことの判定
                character[0]["judgment"].y=50
                speed=0
            
            if character[0]["judgment"].colliderect(ceiling):#天井にあたった時に起こることと、キャラクターの移動
                speed=0
                character[0]["judgment"].y=1
            else:
                character[0]["judgment"].y+=speed
            character[0]["img"][0]["y"]=character[0]["judgment"].y

            if last_speed*speed<0:

                if speed>0:
                    character[0]["img"][0]["img"]=character_fall_img
                else:
                    character[0]["img"][0]["img"]=character_rise_img
                if keys[K_r] or character[0]["judgment"].y>H:
                    character[0]["judgment"].y=50
                    speed=0
            last_speed=speed

            for all in draw(character):
                all




            messages = [  # 画面下部に表示するガイドメッセージを格納するリストです
            "あなたの操作するプロペラの着いたキャラクターはどんどん落下していきます",  
            "スペースを押すと上に加速するので、いい感じにスペースを押して落下しないようにしましょう" ,
            "本番では落下すると最初からになります"
            ]  # messagesリストの終わり
                # 各テキストを描画
            for i, msg in enumerate(messages):  # enumerateでインデックスと要素を取得
                text_surface = font_default.render(msg, True, (0, 0, 0))  # テキストをSurfaceに変換する
                screen.blit(text_surface, (30, H - 100 + i * 30))  # 画面下部に表示する



            
        elif tutorial_page==1:
            if (time.time()-shougaibutu_previous_time)//3==1 :#一定時間ごとにリストに追加
            
                gap=random.randint(300,H)
                interval=(random.randint(-25,25))/100
                shougaibutu_previous_time=time.time()+interval
                
                

                #障害物の上のほうの判定と画像を追加する
                shougaibutu.append({"judgment":pygame.Rect(W,0,20,H-gap),"img":object_stick(shougaibutu_img,W,H-gap,0,40,160)})
                #障害物の下のほうの衝突判定と画像を追加する
                shougaibutu.append({"judgment":pygame.Rect(W,H-gap+300,20,H),"img":object_stick(shougaibutu_img,W,H-gap+300,H,40,160)})
                #コインの判定と画像を追加する
                coin.append(object(coin_img,W,H-gap+140,40,40))
            scroll_object (shougaibutu,-5)
            scroll_object (coin, -5)

            for all in coin:#coinをゲットした判定
                if all["judgment"].x<-100:
                    coin.remove(all)
                elif character[0]["judgment"].colliderect(all["judgment"]):
                    get_coin_sound.play()
                    point+=20
                    coin.remove(all)
            if last_speed*speed<0:

                if speed>0:
                    character[0]["img"][0]["img"]=character_fall_img
                else:
                    character[0]["img"][0]["img"]=character_rise_img

            for all in shougaibutu :#ここですべて移動物に対して衝突判定を作る予定
            
                if all["judgment"].x<0:
                    shougaibutu.remove(all)
                if time.time()-1<resistance:
                    if speed>0:
                        character[0]["img"][0]["img"]=resistance_character_fall_img
                    else:
                        character[0]["img"][0]["img"]=resistance_character_rise_img
                elif character[0]["judgment"].colliderect(all["judgment"]):
                    damage_sound.play()
                    HP-=1
                    resistance=time.time()
                    if speed>0:
                        character[0]["img"][0]["img"]=resistance_character_fall_img
                    else:
                        character[0]["img"][0]["img"]=resistance_character_rise_img
                
            last_speed=speed
            
            if keys[K_SPACE]:#エンターが押されたときに上に加速するやつ
                speed+=-0.6
            else:
                if speed>0: 
                    speed+=0.2
                else:
                    speed+=0.4
            
            
            if character[0]["judgment"].y>H+20:#落下したことの判定
                character[0]["judgment"].y=50
                speed=0    
            
            if character[0]["judgment"].colliderect(ceiling):#天井にあたった時に起こることと、キャラクターの移動
                speed=0
                character[0]["judgment"].y=1
            else:
                character[0]["judgment"].y+=speed
            character[0]["img"][0]["y"]=character[0]["judgment"].y

            
            
                
            for all in draw(character):
                all
            for all in draw(shougaibutu):
                all
            for all in draw(coin):
                all
            
            for all in ad_massage([str(point),"ポイント"],112*W//128,8*H//128):
                all
            for all in ad_massage(["残機：",str(HP-1)],12*W//128,8*H//128):
                all
            messages = [  # 画面下部に表示するガイドメッセージを格納するリストです
            "前から障害物が流れてくるのでそれをよけ続けましょう",  
            "障害物の間にあるコインを取ることでポイントを手に入れることができます",
            "本番では障害物に当たると残機が一つ減り、0で障害物に当たると最初からになります"
            ]  # messagesリストの終わり
                # 各テキストを描画
            for i, msg in enumerate(messages):  # enumerateでインデックスと要素を取得
                text_surface = font_default.render(msg, True, (0, 0, 0))  # テキストをSurfaceに変換する
                screen.blit(text_surface, (30, H - 100 + i * 30))  # 画面下部に表示する
        elif tutorial_page==2:
            if ((time.time()-shougaibutu_previous_time)*(1.1)**level)//3==1 :#一定時間ごとにリストに追加
            
                gap=random.randint(300,H)
                interval=(random.randint(-25,25))/100
                shougaibutu_previous_time=time.time()+interval
                

                #障害物の上のほうの判定と画像を追加する
                shougaibutu.append({"judgment":pygame.Rect(W,0,20,H-gap),"img":object_stick(shougaibutu_img,W,H-gap,0,40,160)})
                #障害物の下のほうの衝突判定と画像を追加する
                shougaibutu.append({"judgment":pygame.Rect(W,H-gap+300,20,H),"img":object_stick(shougaibutu_img,W,H-gap+300,H,40,160)})
                #コインの判定と画像を追加する
                coin.append(object(coin_img,W,H-gap+140,40,40))

            scroll_object (shougaibutu,-5*(1.1)**level)
            scroll_object (coin, -5*(1.1)**level)
            scroll_object (hearts,-5*(1.1)**level)

            for all in coin:#coinをゲットした判定
                if all["judgment"].x<-100:
                    coin.remove(all)
                elif character[0]["judgment"].colliderect(all["judgment"]):
                    get_coin_sound.play()
                    point+=20
                    coin.remove(all)
            
            if point//100!=last_point//100:#レベルが増える判定
                level+=1
                if hearts==[]:
                    random_x=random.randint(0,W)#レベルが上がるごとにランダムな場所にハートを出現させる
                    random_y=random.randint(0,H)
                    heart=object(heart_img,random_x+W,random_y,32,32)
                else:

                    while  shougaibutu[0]["judgment"].colliderect(hearts[0]["judgment"]):
                        random_x=random.randint(0,W)#レベルが上がるごとにランダムな場所にハートを出現させる
                        random_y=random.randint(0,H)
                        heart=object(heart_img,random_x+W,random_y,32,32)
                        
                hearts.append(heart)
            last_point=point

            if last_speed*speed<0:

                            if speed>0:
                                character[0]["img"][0]["img"]=character_fall_img
                            else:
                                character[0]["img"][0]["img"]=character_rise_img

            for all in shougaibutu :#ここですべて移動物に対して衝突判定を作る予定
            
                if all["judgment"].x<0:
                    shougaibutu.remove(all)
                if time.time()-1<resistance:
                    if speed>0:
                        character[0]["img"][0]["img"]=resistance_character_fall_img
                    else:
                        character[0]["img"][0]["img"]=resistance_character_rise_img
                elif character[0]["judgment"].colliderect(all["judgment"]):
                    damage_sound.play()
                    HP-=1
                    resistance=time.time()
                    if speed>0:
                        character[0]["img"][0]["img"]=resistance_character_fall_img
                    else:
                        character[0]["img"][0]["img"]=resistance_character_rise_img
            last_speed=speed    
                
            if keys[K_SPACE]:#エンターが押されたときに上に加速するやつ
                speed+=-0.6*1.1**level
            else:
                if speed>0: 
                    speed+=0.2*1.1**level
                else:
                    speed+=0.4
            

            if hearts==[]:
                pass
            elif character[0]["judgment"].colliderect(hearts[0]["judgment"]):
                get_heart_sound.play()
                HP+=1
                hearts.remove(hearts[0])
            elif hearts[0]["judgment"].x<=-100:
                hearts.remove(hearts[0])


            if character[0]["judgment"].y>H+20:#落下したことの判定
                character[0]["judgment"].y=50
                speed=0    
            
            if character[0]["judgment"].colliderect(ceiling):#天井にあたった時に起こることと、キャラクターの移動
                speed=0
                character[0]["judgment"].y=1
            else:
                character[0]["judgment"].y+=speed
            character[0]["img"][0]["y"]=character[0]["judgment"].y
            point
            
            
            
                

            for all in draw(character):
                all
            for all in draw(shougaibutu):
                all
            for all in draw(coin):
                all
            for all in draw(hearts):
                all

            for all in ad_massage([str(point),"ポイント"],112*W//128,8*H//128):
                all
            for all in ad_massage(["残機：",str(HP-1)],12*W//128,8*H//128):
                all
            for all in ad_massage(["現在のレベル：",str(level)],105*W//128,H-190):
                all
            messages = [  # 画面下部に表示するガイドメッセージを格納するリストです
            "100ポイントごとにレベルが上がりゲームの処理が少し速くなります",
            "そしてレベルが上がるとハートが出現し手に入れると残機が一つ増えます"  
            "この画面では右下にレベルが表示され、上下の矢印キーで変更できます"
            ]  # messagesリストの終わり
                # 各テキストを描画
            for i, msg in enumerate(messages):  # enumerateでインデックスと要素を取得
                text_surface = font_default.render(msg, True, (0, 0, 0))  # テキストをSurfaceに変換する
                screen.blit(text_surface, (30, H - 130 + i * 30))  # 画面下部に表示する
        message="エンターキーを押して次のページへ"
        text_surface = font_default.render(message, True, (255, 99, 71))  # テキストをSurfaceに変換する
        screen.blit(text_surface, (48*W//128,8*H//128))

    elif scine =="shougaibutu_game":#shougaibutu_gameの内容
        #------------------------------shougaibutu_gameの内部処理---------------------

        
        
        if last_scine!=scine:#scineが切り替わった時に起こること
            change_music(BGM_game)
            point=0
            last_point=0
            speed=0
            last_speed=0
            level=0
            HP=1
            resistance=0
            shougaibutu_previous_time=time.time()
            interval=(random.randint(-25,25))/100
            Fall_judgment = pygame.Rect(0, H, W, 1)
            ceiling=pygame.Rect(0 , 0 , H , 1)
            character=[{"judgment":pygame.Rect(50, 50, 50, 50),"img":[{"img":character_fall_img,"x":50,"y":50}]}]
            scenery_img_1=pygame.transform.scale(scenery_img_1, (W, H))
            scenery_img_2=pygame.transform.scale(scenery_img_2, (W, H))
            scenery_img_3=pygame.transform.scale(scenery_img_3, (W, H))
            character_fall_img=pygame.transform.scale(pygame.image.load("asset/画像/80.png"), (50, 50))
            scenerys=[{"img":[{"img":scenery_img_1,"x":0,"y":0}]},{"img":[{"img":scenery_img_1,"x":W,"y":0}]}]
            #ゲーム起動時に何もないリストに変換
            shougaibutu=[]
            coin=[]
            hearts=[]
            
        

        if ((time.time()-shougaibutu_previous_time)*(1.1)**level)//3==1 or last_scine!=scine:#一定時間ごとにリストに追加
            
            gap=random.randint(300,H)
            interval=(random.randint(-25,25))/100
            shougaibutu_previous_time=time.time()+interval

            #障害物の上のほうの判定と画像を追加する
            shougaibutu.append({"judgment":pygame.Rect(W,0,20,H-gap),"img":object_stick(shougaibutu_img,W,H-gap,0,40,160)})
            #障害物の下のほうの衝突判定と画像を追加する
            shougaibutu.append({"judgment":pygame.Rect(W,H-gap+300,20,H),"img":object_stick(shougaibutu_img,W,H-gap+300,H,40,160)})
            #コインの判定と画像を追加する
            coin.append(object(coin_img,W,H-gap+140,40,40))
        last_scine=scine    
        
        
        #リストで管理されているものを移動
        scroll_object (shougaibutu,-5*(1.1)**level)
        scroll_object (coin, -5*(1.1)**level)
        scroll_object (hearts,-5*(1.1)**level)

        for all in scenerys:
            for all in all["img"]:
                if all["x"]<-W:
                    all["x"]+=2*W
                all["x"]+=-1
                






        if keys[K_SPACE]:#エンターが押されたときに上に加速するやつ
            speed=speed-0.6*(1.1)**level
        else:
            if speed>0: 
                speed=speed+0.2*(1.1)**level
            else:
                speed=speed+0.4*(1.1)**level


        #character=[{"judgment":rect_movable,"img":[{"img":character_fall_img,"x":W,"y":H-gap+80}]}]


        if last_speed*speed<0:

            if speed>0:
                character[0]["img"][0]["img"]=character_fall_img
            else:
                character[0]["img"][0]["img"]=character_rise_img

        level
        # 衝突判定：2つのRectが重なっているか判定します【880888389410395†L137-L146】。
        collide=False


        
        for all in shougaibutu :#ここですべて移動物に対して衝突判定を作る予定
            
            if all["judgment"].x<0:
                shougaibutu.remove(all)
            
            if character[0]["judgment"].colliderect(all["judgment"]):
                collide=True
        for all in coin:#coinをゲットした判定
            if all["judgment"].x<-100:
                coin.remove(all)
            elif character[0]["judgment"].colliderect(all["judgment"]):
                get_coin_sound.play()
                point+=20
                coin.remove(all)
        
        if point//100!=last_point//100:#レベルが増える判定
            level+=1
            if hearts==[]:
                random_x=random.randint(0,W)#レベルが上がるごとにランダムな場所にハートを出現させる
                random_y=random.randint(0,H)
                heart=object(heart_img,random_x+W,random_y,32,32)
            else:

                while  shougaibutu[0]["judgment"].colliderect(hearts[0]["judgment"]):
                    random_x=random.randint(0,W)#レベルが上がるごとにランダムな場所にハートを出現させる
                    random_y=random.randint(0,H)
                    heart=object(heart_img,random_x+W,random_y,32,32)
            hearts.append(heart)

        

        if character[0]["judgment"].y>H+20:
            damage_sound.play()
            HP=0
        elif time.time()-3<resistance:
            if last_speed*speed<0:

                if speed>0:
                    character[0]["img"][0]["img"]=resistance_character_fall_img
                else:
                   character[0]["img"][0]["img"]=resistance_character_rise_img
        elif  collide ==True :#落下、もしくはぶつかった時に起こること
            damage_sound.play()
            HP=HP-1
            resistance=time.time()
            if speed>0:
                character[0]["img"][0]["img"]=resistance_character_fall_img
            else:
               character[0]["img"][0]["img"]=resistance_character_rise_img

        
        if character[0]["judgment"].colliderect(ceiling):#天井にあたった時に起こることと、キャラクターの移動
            speed=0
            character[0]["judgment"].y=1
        else:
            character[0]["judgment"].y+=speed
        character[0]["img"][0]["y"]=character[0]["judgment"].y

        if hearts==[]:
            pass
        elif character[0]["judgment"].colliderect(hearts[0]["judgment"]):
            get_heart_sound.play()
            HP+=1
            hearts.remove(hearts[0])
        elif hearts[0]["judgment"].x<=-100:
            hearts.remove(hearts[0])


        if HP <=0:
            scine="menu"

        
        #------------------------shougaibutu_gameで表示する内容-----------------------------------
        screen.fill((255,255,255))
        

            # 矩形の描画：draw.rect関数で矩形を描画します【792189879171763†L115-L124】。
        # border_radius引数に値を指定すると角丸の矩形を描画できます【792189879171763†L140-L149】。

        for all in draw(scenerys):
            all

        for all in draw(shougaibutu):
            all
        for all in draw(coin):
            all

        for all in draw(character):
            all
        for all in draw(hearts):
            all
        #pygame.draw.rect(screen, BLUE if not falling else GREEN, rect_movable, border_radius=8)  # 移動矩形を描画

        # 枠線の描画：内側が空の矩形枠を描画するには width 引数に1以上の値を渡します【792189879171763†L123-L130】。

        for all in ad_massage([str(point),"ポイント"],112*W//128,8*H//128):
            all
        for all in ad_massage(["残機：",str(HP-1)],12*W//128,8*H//128):
            all
        last_speed=speed
        last_point=point

        
    
    
 







    

    #----追加機能を実装、音楽再生等を追加する部分----

    pygame.display.update() #画面更新


#メインループ終了後
pygame.quit() #ウィンドウを閉じる
sys.exit()    #プログラムを終了する

#次来た時にやること
#回転する障害物をさっさと実装する
#チュートリアルの時のポイントがメニューのポイント欄に表示させるバグが発生しています、要改善
#上ができれば完成、BGMのほうから対応しな
#タイトルや操作説明の所をさっさと作る