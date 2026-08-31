# coding: utf-8
import os
import sys
import pygame
from pygame.locals import *
import time #数秒待つ等を使うためのモジュール
import random

pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init() #各種pygameモジュールの初期化


def resource_path(*parts):
    if hasattr(sys, "_MEIPASS"):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, *parts)


def load_image(filename):
    return pygame.image.load(resource_path("images", filename))


class SilentSound:
    def play(self, *args, **kwargs):
        return None


def load_sound(filename):
    if not pygame.mixer.get_init():
        return SilentSound()
    try:
        return pygame.mixer.Sound(resource_path("sounds", filename))
    except pygame.error:
        return SilentSound()

#ディスプレイ設定
clock=pygame.time.Clock()
scr_w,scr_h=1920,1080
width, height = scr_w, scr_h
display_flags = FULLSCREEN | getattr(pygame, "SCALED", 0)
try:
    screen=pygame.display.set_mode((scr_w,scr_h),display_flags)
except pygame.error:
    screen=pygame.display.set_mode((scr_w,scr_h),FULLSCREEN)
pygame.display.set_caption("パキチョコ")
background_color=(255,255,255)
screen.fill(background_color)

#画像読み込み
image_choko=load_image("choko.png") #指定の画像を読み込み
image_choko1=load_image("choko2.png")
image_choko2=load_image("choko3.png")
image_choko3=load_image("choko4.png").convert_alpha()
bouru_migi1_img=load_image("migibourusyou.png")
bouru_migi2_img=load_image("migibourutyuu.PNG")
bouru_migi3_img=load_image("migibourudai.PNG")
bouru_hidari1_img=load_image("hidaribourusyou.PNG")
bouru_hidari2_img=load_image("hidaribourutyuu.PNG")
bouru_hidari3_img=load_image("hidaribourudai.PNG")
win_img=load_image("WIN.png")
lose_img=load_image("LOSE.png")
suuji0_img=load_image("suuji0.png")
suuji1_img=load_image("suuji1.png")
suuji2_img=load_image("suuji2.png")
suuji3_img=load_image("suuji3.png")
suuji4_img=load_image("suuji4.png")
suuji5_img=load_image("suuji5.png")
suuji6_img=load_image("suuji6.png")
suuji7_img=load_image("suuji7.png")
suuji8_img=load_image("suuji8.png")
suuji9_img=load_image("suuji9.png")
purasu_img=load_image("purasu.png")
mainasu_img=load_image("mainasu.png")
asobikata_img=load_image("Asobikata_sousa.png")
asobikata_img1=load_image("Asobikata_ru-ru.png")
asobikata_img2=load_image("Asobikata_tyoko.png")
asobikata_img3=load_image("Asobikata_syouri.png")
image_kasoru=load_image("kasoru.png")
image_drow=load_image("DRAW.png")
# 透過度の初期値
alpha = 128
image_haikei=load_image("haikei.jpeg")
image_haikei1=load_image("haikei2.png")
image_haikei2=load_image("haikei3.jpg")
cell_width = width // 12 # セルの幅（元の幅の1/12）
cell_height = height // 8 # セルの高さ（元の高さの1/8）
image_choko = pygame.transform.scale(image_choko, (cell_width, cell_height)) # 画像のサイズをセルに合わせて調整
image_choko1 = pygame.transform.scale(image_choko1, (cell_width, cell_height)) # 画像のサイズをセルに合わせて調整
image_choko2 = pygame.transform.scale(image_choko2, (cell_width, cell_height)) # 画像のサイズをセルに合わせて調整
image_choko3 = pygame.transform.scale(image_choko3, (cell_width, cell_height)) # 画像のサイズをセルに合わせて調整
image_haikei = pygame.transform.scale(image_haikei, (width, height))
rect_bg = image_haikei.get_rect()
image_haikei1 = pygame.transform.scale(image_haikei1, (width, height))
rect_bg1 = image_haikei1.get_rect()
image_haikei2 = pygame.transform.scale(image_haikei2, (width, height))
rect_bg2 = image_haikei2.get_rect()


#サウンド読み込み
choko1_sound=load_sound("choko1.wav")
choko2_sound=load_sound("choko2.wav")
choko3_sound=load_sound("choko3.wav")
choko4_sound=load_sound("choko4.wav")
choko5_sound=load_sound("choko5.wav")
choko6_sound=load_sound("choko6.wav")
choko7_sound=load_sound("choko7.wav")
choko8_sound=load_sound("choko8.wav")
choko9_sound=load_sound("choko9.wav")
choko10_sound=load_sound("choko10.wav")
choko11_sound=load_sound("choko11.wav")
choko12_sound=load_sound("choko12.wav")
choko13_sound=load_sound("choko13.wav")
choko14_sound=load_sound("choko14.wav")
choko15_sound=load_sound("choko15.wav")
choko16_sound=load_sound("choko16.wav")
choko17_sound=load_sound("choko17.wav")
choko18_sound=load_sound("choko18.wav")
choko19_sound=load_sound("choko19.wav")
choko20_sound=load_sound("choko20.wav")
choko21_sound=load_sound("choko21.wav")
randomsound=1

#ボタン設定
butann_sita_img=load_image("yajirusi_sita.png").convert_alpha()
butann_migi_img=load_image("yajirusi_migi.png").convert_alpha()
butann_title_img1=load_image("start.png").convert_alpha()
butann_title_img2=load_image("goki.png").convert_alpha()
butann_title_img3=load_image("easy.png").convert_alpha()
butann_title_img4=load_image("hard.png").convert_alpha()
butann_title_img5=load_image("Retry.png").convert_alpha()
butann_title_img6=load_image("Title.png").convert_alpha()
butann_asobikata_batu_img=load_image("Batu_butann.png")
butann_asobikata_hidari_img=load_image("hidari_butann.png")
butann_asobikata_migi_img=load_image("migi_butann.png")


butann_title_img1 = pygame.transform.scale(butann_title_img1, (360, 120))
butann_title_img2 = pygame.transform.scale(butann_title_img2, (360, 120))
butann_title_img3 = pygame.transform.scale(butann_title_img3, (500, 200))
butann_title_img4 = pygame.transform.scale(butann_title_img4, (500, 200))
butann_title_img5 = pygame.transform.scale(butann_title_img5, (500, 200))
butann_title_img6 = pygame.transform.scale(butann_title_img6, (500, 200))

enemy_img=load_image("Enemy.png").convert_alpha()
turn_img=load_image("Turn.png").convert_alpha()
you_img=load_image("You.png").convert_alpha()
enemy_img = pygame.transform.scale(enemy_img, (360, 170))
turn_img = pygame.transform.scale(turn_img, (360, 170))
you_img = pygame.transform.scale(you_img, (360, 170))
#ボタンクラス
class Button():
    def __init__(self,x,y,image,scale,tateyoko):
        width=image.get_width()
        height=image.get_height()
        self.image=pygame.transform.scale(image,(int(width*scale),int(height*scale)))
        self.image =image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)
        pos = pygame.mouse.get_pos() #マウスの位置を取得
        kakutei=0
        if self.rect.collidepoint(pos): #マウスがボタンに重なっているか取得
            self.image=pygame.transform.scale(image,(int(width*1.3),int(height*1.3)))


            if tateyoko==0:
                self.rect.topleft = (x-20,y-10)
                
  
            if tateyoko==1:
                self.rect.topleft = (x-10,y-20)
                

        else:
            kakutei=0
            self.image=pygame.transform.scale(image,(int(width*1),int(height*1)))
     
        self.clicked = False

    def draw(self,image,scale):
        if scene == 1:
            width=image.get_width()
            height=image.get_height()
            action = False
            pos = pygame.mouse.get_pos() #マウスの位置を取得
            if self.rect.collidepoint(pos): #マウスがボタンに重なっているか取得
                
                if pygame.mouse.get_pressed()[0] == 1 and self.clicked ==False:
                    self.clicked = True
                    action = True

        
            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False
        
            screen.blit(self.image,(self.rect.x,self.rect.y))

            return action
    def yosoku(self):
        pos = pygame.mouse.get_pos() #マウスの位置を取得
        kakutei=0
        if self.rect.collidepoint(pos): #マウスがボタンに重なっているか取得
            kakutei=1
        
        return kakutei

class titleButton():
    def __init__(self,x,y,image,scale):
        width=image.get_width()
        height=image.get_height()
        
        self.image =image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)
        pos = pygame.mouse.get_pos() #マウスの位置を取得
        if self.rect.collidepoint(pos): #マウスがボタンに重なっているか取得
            self.image=pygame.transform.scale(image,(float(width*1.1),float(height*1.1)))
            self.rect.topleft = (x-20,y-10)
            if butann_asobikata_migi:
                self.rect.topleft = (x,y-10)
            if butann_asobikata_batu:
                self.rect.topleft = (x-4,y-4)
        else:
            self.image=pygame.transform.scale(image,(float(width*scale),float(height*scale)))
        self.clicked = False
    def titledraw(self,image):
    
        width=image.get_width()
        height=image.get_height()
        action = False
        pos = pygame.mouse.get_pos() #マウスの位置を取得
        if self.rect.collidepoint(pos): #マウスがボタンに重なっているか取得
            
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked ==False:
                self.clicked = True
                action = True
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        screen.blit(self.image,(self.rect.x,self.rect.y))

        return action


def random_sound(a):
    b=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21]
    b.remove(a)
    c=random.choice(b)
    if c==1:
        d=choko1_sound
    elif c==2:
        d=choko2_sound
    elif c==3:
        d=choko3_sound
    elif c==4:
        d=choko4_sound
    elif c==5:
        d=choko5_sound
    elif c==6:
        d=choko6_sound
    elif c==7:
        d=choko7_sound
    elif c==8:
        d=choko8_sound
    elif c==9:
        d=choko9_sound
    elif c==10:
        d=choko10_sound
    elif c==11:
        d=choko11_sound
    elif c==12:
        d=choko12_sound
    elif c==13:
        d=choko13_sound
    elif c==14:
        d=choko14_sound
    elif c==15:
        d=choko15_sound
    elif c==16:
        d=choko16_sound
    elif c==17:
        d=choko17_sound
    elif c==18:
        d=choko18_sound
    elif c==19:
        d=choko19_sound
    elif c==20:
        d=choko20_sound
    else:
        d=choko21_sound

    return c,d






#ボタンを自動的に消す関数
def search_Button():
    a = 0
    b = 0
    c = 0
    d = 0
    e = 0
    f = 0
    g = 0
    for i in range(2):
        migi1_sakujo = 0
        migi2_sakujo = 0
        for j in range(6):
            migi1_sakujo+=choko[i][j]
            migi2_sakujo+=choko[i+1][j]
        if migi1_sakujo == 0:
            a = 1
        if migi2_sakujo == 0:
            b = 1
    for i in range(2):
        sita1_sakujo = 0
        sita2_sakujo = 0
        sita3_sakujo = 0
        sita4_sakujo = 0
        sita5_sakujo = 0
        for j in range(3):
            sita1_sakujo+=choko[j][i]
            sita2_sakujo+=choko[j][i+1]
            sita3_sakujo+=choko[j][i+2]
            sita4_sakujo+=choko[j][i+3]
            sita5_sakujo+=choko[j][i+4]
        if sita1_sakujo == 0:
            c = 1
        if sita2_sakujo == 0:
            d = 1
        if sita3_sakujo == 0:
            e = 1
        if sita4_sakujo == 0:
            f = 1
        if sita5_sakujo == 0:
            g = 1
    
    return (a,b,c,d,e,f,g)

#ボタン表示関数
def draw_Button():
    butann_migi1_sakujo,butann_migi2_sakujo,butann_sita1_sakujo,butann_sita2_sakujo,butann_sita3_sakujo,butann_sita4_sakujo,butann_sita5_sakujo = search_Button()
    a = 0
    b = 0
    c = 0
    d = 0
    e = 0
    f = 0
    g = 0

    if butann_migi1_sakujo == 0 and playr == 0:
        butann_migi1.draw(butann_migi_img,1)
    if butann_migi1_sakujo == 1:
        a=1

    if butann_migi2_sakujo == 0 and playr == 0:
        butann_migi2.draw(butann_migi_img,1)
    if butann_migi2_sakujo == 1:
        b=1

    if butann_sita1_sakujo == 0 and playr == 0:
        butann_sita1.draw(butann_sita_img,1)
    if butann_sita1_sakujo == 1:
        c=1

    if butann_sita2_sakujo == 0 and playr == 0:
        butann_sita2.draw(butann_sita_img,1)
    if butann_sita2_sakujo == 1:
        d=1

    if butann_sita3_sakujo == 0 and playr == 0:
        if senkou==1:
            butann_sita3.draw(butann_sita_img,1)
    if butann_sita3_sakujo == 1:
        e=1

    if butann_sita4_sakujo == 0 and playr == 0:
        butann_sita4.draw(butann_sita_img,1)
    if butann_sita4_sakujo == 1:
        f=1
    
    if butann_sita5_sakujo == 0 and playr == 0:
        butann_sita5.draw(butann_sita_img,1)
    if butann_sita5_sakujo == 1:
        g=1

    return (a,b,c,d,e,f,g)

#寄せる計算関数
def margin():

    margin_height_1=0
    margin_height_2=0
    margin_height_3=0
    a=0
    b=0
    c=0
    d=0
    e=0
    f=0
    g=0
    h=0
    i=0
    j=0
    for x in range(6):
        margin_height_1+=choko[0][x]
        margin_height_3+=choko[1][x]
        margin_height_2+=choko[2][x]
    if margin_height_1==0:
        a =-70

    
    if margin_height_2==0:
        b =+70
        if margin_height_3==0:
            b =+140
    c=a+b
    
    for z in range(3):
        d+=choko[z][0]
        e+=choko[z][1]
        f+=choko[z][2]
        g+=choko[z][3]
        h+=choko[z][4]
        i+=choko[z][5]
    if d == 0:
        j+=-80
    if e == 0:
        if(g+h+i) == 0:
            j+=80
        else:
            j+=-80
    if f == 0:
        if(g+h+i) == 0:
            j+=80
        elif(i+h)==0:
            j+=80
        else:
            j+=-80
    if g == 0:
        if(d+e+f) == 0:
            j+=-80
        elif(d+e)==0:
            j+=-80
        
        else:
            j+=80
    if h == 0:
        if(d+e+f) == 0:
            j+=-80
        else:
            j+=80
    if i == 0:
        j+=80

    return(c,j)

def yoseru_sita1():
    a=0
    for i in range(3):
        a+=choko[i][1]
    if a==0:
        return (-60,100)
    else :
        return (100,-60)
def yoseru_sita2():
    a=0
    for i in range(3):
        a+=choko[i][2]
    if a==0:
        return (-30,50)
    else :
        return (50,-30)
def yoseru_sita3():
    a=0
    for i in range(3):
        a+=choko[i][3]
    if a==0:
        return (0,0)
    else :
        return (0,0)
def yoseru_sita4():
    a=0
    for i in range(3):
        a+=choko[i][4]
    if a==0:
        return (30,-50)
    else :
        return (-50,30)
def yoseru_sita5():
    a=0
    for i in range(3):
        a+=choko[i][5]
    if a==0:
        return (60,-100)
    else:
        return (-100,60)





def tumeru_Button():#左と上のゼロによってボタンをさらに寄せる
    
    a=0
    b=0
    c=0
    d=0
    e=0
    f=0
    g=0
    h=0
    j=0
    for i in range(6):
        a+=choko[0][i]
        b+=choko[1][i]
    if a == 0:
        c+=132
        if b == 0:
            c += 134
    
    for x in range(3):
        d+=choko[x][0]
        e+=choko[x][1]
        f+=choko[x][2]
        g+=choko[x][3]
        h+=choko[x][4]
    if d == 0:
        j+=158
        if e == 0:
            j+=160
            if f == 0:
                j+=161
                if g == 0:
                    j+=160
                    if h == 0:
                        j+=160

    return (j,c)

        

def tumeru_Tate():
    d=0
    e=0
    f=0
    g=0
    h=0
    j=0
    k=0
    i=0

    
    for x in range(3):
        d+=choko[x][0]
        e+=choko[x][1]
        f+=choko[x][2]
        g+=choko[x][3]
        h+=choko[x][4]
        i+=choko[x][5]
    if d == 0:
        j+=5
        k-=5
        if e == 0:
            j+=5
            k-=5
            if f == 0:
                j+=5
                k-=5
                if g == 0:
                    j+=5
                    k-=5
                    if h == 0:
                        j+=5
                        k-=5
                        if i == 0:
                            j+=5
                            k-=5
    

    return (k,j)

def AIsentakukeisan1():
    choko_kara=[
    [1,1,1,1,1,1],
    [1,1,1,1,1,1],
    [1,1,1,1,1,1]
    ]
    for i in range(3):
        for z in range(6):
            if choko[i][z]==0:
                choko_kara[i][z]=0
            if choko[i][z]==2:
                choko_kara[i][z]=2
            if choko[i][z]==3:
                choko_kara[i][z]=3
    
    a=0
    b=0
    c=0
    d=0
 
    for i in range(6):
        a+=choko_kara[0][i]
        if choko[0][i]==2:
            a-=1
        if choko[0][i]==3:
            a-=2
        b+=choko_kara[1][i]
        if choko[1][i]==2:
            b-=1
        if choko[1][i]==3:
            b-=2
        c+=choko_kara[2][i]
        if choko[2][i]==2:
            c-=1
        if choko[2][i]==2:
            c-=2
    if a<(b+c):
        for z in range(6):
            if choko[0][z]==0:
                d+=0
            if choko[0][z]==1:
                d+=1
            if choko[0][z]==2:
                d+=2
            if choko[0][z]==3:
                d-=2
    else:
        for i in range(2):
            for z in range(6):
                if choko[i+1][z]==0:
                    d+=0
                if choko[i+1][z]==1:
                    d+=1
                if choko[i+1][z]==2:
                    d+=2
                if choko[i+1][z]==3:
                    d-=2

    return d

def AIsentakukeisan2():
    choko_kara=[
    [1,1,1,1,1,1],
    [1,1,1,1,1,1],
    [1,1,1,1,1,1]
    ]
    for i in range(3):
        for z in range(6):
            if choko[i][z]==0:
                choko_kara[i][z]=0
            if choko[i][z]==2:
                choko_kara[i][z]=2
            if choko[i][z]==3:
                choko_kara[i][z]=3

    d=0
    for z in range(6):
        if choko[2][z]==0:
            d+=0
        if choko[2][z]==1:
            d+=1
        if choko[2][z]==2:
            d+=2
        if choko[2][z]==3:
            d-=2

    return d


def AIsentakukeisan3():
    choko_kara=[
    [1,1,1,1,1,1],
    [1,1,1,1,1,1],
    [1,1,1,1,1,1]
    ]
    for i in range(3):
        for z in range(6):
            if choko[i][z]==0:
                choko_kara[i][z]=0
            if choko[i][z]==2:
                choko_kara[i][z]=2
            if choko[i][z]==3:
                choko_kara[i][z]=3

    a=0
    b=0
    d=0
    for i in range(3):
        a+=choko[i][0]
        if choko[i][0]==2:
            a-=1
        if choko[i][0]==3:
            a-=2

    for j in range(5):
        for x in range(3):
            b+=choko[x][j+1]
            if choko[x][j+1]==2:
                b-=1
            if choko[x][j+1]==3:
                b-=2

    if a < b:
        for i in range(3):
            if choko[i][0]==0:
                d+=0
            if choko[i][0]==1:
                d+=1
            if choko[i][0]==2:
                d+=2
            if choko[i][0]==3:
                d-=2
    else:
        for j in range(5):
            for i in range(3):
                if choko[i][j+1]==0:
                    d+=0
                if choko[i][j+1]==1:
                    d+=1
                if choko[i][j+1]==2:
                    d+=2
                if choko[i][j+1]==3:
                    d-=2

    return d



def AIsentakukeisan4():
    choko_kara=[
    [1,1,1,1,1,1],
    [1,1,1,1,1,1],
    [1,1,1,1,1,1]
    ]
    for i in range(3):
        for z in range(6):
            if choko[i][z]==0:
                choko_kara[i][z]=0
            if choko[i][z]==2:
                choko_kara[i][z]=2
            if choko[i][z]==3:
                choko_kara[i][z]=3

    a=0
    b=0
    d=0
    for z in range(3):
        for i in range(2):
            a+=choko[z][i]
            if choko[z][i]==2:
                a-=1
            if choko[z][i]==3:
                a-=2
    for j in range(3):
        for x in range(4):
            b+=choko[j][x+2]
            if choko[j][x+2]==2:
                b-=1
            if choko[j][x+2]==3:
                b-=2

    if a < b:
        for i in range(3):
            for j in range(2):
                if choko[i][j]==0:
                    d+=0
                if choko[i][j]==1:
                    d+=1
                if choko[i][j]==2:
                    d+=2
                if choko[i][j]==3:
                    d-=2
    else:
        for i in range(3):
            for j in range(4):
                if choko[i][j+2]==0:
                    d+=0
                if choko[i][j+2]==1:
                    d+=1
                if choko[i][j+2]==2:
                    d+=2
                if choko[i][j+2]==3:
                    d-=2
    
    return d


def AIsentakukeisan5():
    choko_kara=[
    [1,1,1,1,1,1],
    [1,1,1,1,1,1],
    [1,1,1,1,1,1]
    ]
    for i in range(3):
        for z in range(6):
            if choko[i][z]==0:
                choko_kara[i][z]=0
            if choko[i][z]==2:
                choko_kara[i][z]=2
            if choko[i][z]==3:
                choko_kara[i][z]=3

    a=0
    b=0
    d=0
    for z in range(3):
        for i in range(3):
            a+=choko[z][i]
            if choko[z][i]==2:
                a-=1
            if choko[z][i]==3:
                a-=2
    for j in range(3):
        for x in range(3):
            b+=choko[j][x+3]
            if choko[j][x+3]==2:
                b-=1
            if choko[j][x+3]==3:
                b-=2

    if a < b:
        for i in range(3):
            for j in range(3):
                if choko[i][j]==0:
                    d+=0
                if choko[i][j]==1:
                    d+=1
                if choko[i][j]==2:
                    d+=2
                if choko[i][j]==3:
                    d-=2
    else:
        for i in range(3):
            for j in range(3):
                if choko[i][j+3]==0:
                    d+=0
                if choko[i][j+3]==1:
                    d+=1
                if choko[i][j+3]==2:
                    d+=2
                if choko[i][j+3]==3:
                    d-=2
    
    return d


def AIsentakukeisan6():
    choko_kara=[
    [1,1,1,1,1,1],
    [1,1,1,1,1,1],
    [1,1,1,1,1,1]
    ]
    for i in range(3):
        for z in range(6):
            if choko[i][z]==0:
                choko_kara[i][z]=0
            if choko[i][z]==2:
                choko_kara[i][z]=2
            if choko[i][z]==3:
                choko_kara[i][z]=3

    a=0
    b=0
    d=0
    for z in range(3):
        for i in range(4):
            a+=choko[z][i]
            if choko[z][i]==2:
                a-=1
            if choko[z][i]==3:
                a-=2
    for j in range(3):
        for x in range(2):
            b+=choko[j][x+4]
            if choko[j][x+4]==2:
                b-=1
            if choko[j][x+4]==3:
                b-=2

    if a < b:
        for i in range(3):
            for j in range(4):
                if choko[i][j]==0:
                    d+=0
                if choko[i][j]==1:
                    d+=1
                if choko[i][j]==2:
                    d+=2
                if choko[i][j]==3:
                    d-=2
    else:
        for i in range(3):
            for j in range(2):
                if choko[i][j+4]==0:
                    d+=0
                if choko[i][j+4]==1:
                    d+=1
                if choko[i][j+4]==2:
                    d+=2
                if choko[i][j+4]==3:
                    d-=2
    
    return d


def AIsentakukeisan7():
    choko_kara=[
    [1,1,1,1,1,1],
    [1,1,1,1,1,1],
    [1,1,1,1,1,1]
    ]
    for i in range(3):
        for z in range(6):
            if choko[i][z]==0:
                choko_kara[i][z]=0
            if choko[i][z]==2:
                choko_kara[i][z]=2
            if choko[i][z]==3:
                choko_kara[i][z]=3

    d=0
    for i in range(3):
        if choko[i][5]==0:
            d+=0
        if choko[i][5]==1:
            d+=1
        if choko[i][5]==2:
            d+=2
        if choko[i][5]==3:
            d-=2

    return d



def choko_yosoku_migi1():
    choko_kara=[
    [1,1,1,1,1,1],
    [1,1,1,1,1,1],
    [1,1,1,1,1,1]
    ]
    for i in range(3):
        for z in range(6):
            if choko[i][z]==0:
                choko_kara[i][z]=0
            if choko[i][z]==2:
                choko_kara[i][z]=2
            if choko[i][z]==3:
                choko_kara[i][z]=3

    a=0
    b=0
    c=0
 
    for i in range(6):
        a+=choko_kara[0][i]
        if choko[0][i]==2:
            a-=1
        if choko[0][i]==3:
            a-=2
        b+=choko_kara[1][i]
        if choko[1][i]==2:
            b-=1
        if choko[1][i]==3:
            b-=2
        c+=choko_kara[2][i]
        if choko[2][i]==2:
            c-=1
        if choko[2][i]==2:
            c-=2
    if a<(b+c):
        for z in range(6):
            if choko[0][z]==0:
                choko_kara[0][z]=0
            if choko[0][z]==1:
                choko_kara[0][z]=4
            if choko[0][z]==2:
                choko_kara[0][z]=5
            if choko[0][z]==3:
                choko_kara[0][z]=6
    else:
        for i in range(2):
            for z in range(6):
                if choko[i+1][z]==0:
                    choko_kara[i+1][z]=0
                if choko[i+1][z]==1:
                    choko_kara[i+1][z]=4
                if choko[i+1][z]==2:
                    choko_kara[i+1][z]=5
                if choko[i+1][z]==3:
                    choko_kara[i+1][z]=6

    return choko_kara


def choko_yosoku_migi2():
    choko_kara=[
    [1,1,1,1,1,1],
    [1,1,1,1,1,1],
    [1,1,1,1,1,1]
    ]
    for i in range(3):
        for z in range(6):
            if choko[i][z]==0:
                choko_kara[i][z]=0
            if choko[i][z]==2:
                choko_kara[i][z]=2
            if choko[i][z]==3:
                choko_kara[i][z]=3

    for z in range(6):
        if choko[2][z]==0:
            choko_kara[2][z]=0
        if choko[2][z]==1:
            choko_kara[2][z]=4
        if choko[2][z]==2:
            choko_kara[2][z]=5
        if choko[2][z]==3:
            choko_kara[2][z]=6

    return choko_kara

def choko_yosoku_sita1():
    choko_kara=[
    [1,1,1,1,1,1],
    [1,1,1,1,1,1],
    [1,1,1,1,1,1]
    ]
    for i in range(3):
        for z in range(6):
            if choko[i][z]==0:
                choko_kara[i][z]=0
            if choko[i][z]==2:
                choko_kara[i][z]=2
            if choko[i][z]==3:
                choko_kara[i][z]=3

    a=0
    b=0
    for i in range(3):
        a+=choko[i][0]
        if choko[i][0]==2:
            a-=1
        if choko[i][0]==3:
            a-=2

    for j in range(5):
        for x in range(3):
            b+=choko[x][j+1]
            if choko[x][j+1]==2:
                b-=1
            if choko[x][j+1]==3:
                b-=2

    if a < b:
        for i in range(3):
            if choko[i][0]==0:
                choko_kara[i][0]=0
            if choko[i][0]==1:
                choko_kara[i][0]=4
            if choko[i][0]==2:
                choko_kara[i][0]=5
            if choko[i][0]==3:
                choko_kara[i][0]=6
    else:
        for j in range(5):
            for i in range(3):
                if choko[i][j+1]==0:
                    choko_kara[i][j+1]=0
                if choko[i][j+1]==1:
                    choko_kara[i][j+1]=4
                if choko[i][j+1]==2:
                    choko_kara[i][j+1]=5
                if choko[i][j+1]==3:
                    choko_kara[i][j+1]=6

    return choko_kara

def choko_yosoku_sita2():
    choko_kara=[
    [1,1,1,1,1,1],
    [1,1,1,1,1,1],
    [1,1,1,1,1,1]
    ]
    for i in range(3):
        for z in range(6):
            if choko[i][z]==0:
                choko_kara[i][z]=0
            if choko[i][z]==2:
                choko_kara[i][z]=2
            if choko[i][z]==3:
                choko_kara[i][z]=3

    a=0
    b=0
    for z in range(3):
        for i in range(2):
            a+=choko[z][i]
            if choko[z][i]==2:
                a-=1
            if choko[z][i]==3:
                a-=2
    for j in range(3):
        for x in range(4):
            b+=choko[j][x+2]
            if choko[j][x+2]==2:
                b-=1
            if choko[j][x+2]==3:
                b-=2

    if a < b:
        for i in range(3):
            for j in range(2):
                if choko[i][j]==0:
                    choko_kara[i][j]=0
                if choko[i][j]==1:
                    choko_kara[i][j]=4
                if choko[i][j]==2:
                    choko_kara[i][j]=5
                if choko[i][j]==3:
                    choko_kara[i][j]=6
    else:
        for i in range(3):
            for j in range(4):
                if choko[i][j+2]==0:
                    choko_kara[i][j+2]=0
                if choko[i][j+2]==1:
                    choko_kara[i][j+2]=4
                if choko[i][j+2]==2:
                    choko_kara[i][j+2]=5
                if choko[i][j+2]==3:
                    choko_kara[i][j+2]=6
    
    return choko_kara

def choko_yosoku_sita3():
    choko_kara=[
    [1,1,1,1,1,1],
    [1,1,1,1,1,1],
    [1,1,1,1,1,1]
    ]
    for i in range(3):
        for z in range(6):
            if choko[i][z]==0:
                choko_kara[i][z]=0
            if choko[i][z]==2:
                choko_kara[i][z]=2
            if choko[i][z]==3:
                choko_kara[i][z]=3

    a=0
    b=0
    for z in range(3):
        for i in range(3):
            a+=choko[z][i]
            if choko[z][i]==2:
                a-=1
            if choko[z][i]==3:
                a-=2
    for j in range(3):
        for x in range(3):
            b+=choko[j][x+3]
            if choko[j][x+3]==2:
                b-=1
            if choko[j][x+3]==3:
                b-=2

    if a < b:
        for i in range(3):
            for j in range(3):
                if choko[i][j]==0:
                    choko_kara[i][j]=0
                if choko[i][j]==1:
                    choko_kara[i][j]=4
                if choko[i][j]==2:
                    choko_kara[i][j]=5
                if choko[i][j]==3:
                    choko_kara[i][j]=6
    else:
        for i in range(3):
            for j in range(3):
                if choko[i][j+3]==0:
                    choko_kara[i][j+3]=0
                if choko[i][j+3]==1:
                    choko_kara[i][j+3]=4
                if choko[i][j+3]==2:
                    choko_kara[i][j+3]=5
                if choko[i][j+3]==3:
                    choko_kara[i][j+3]=6
    
    return choko_kara

def choko_yosoku_sita4():
    choko_kara=[
    [1,1,1,1,1,1],
    [1,1,1,1,1,1],
    [1,1,1,1,1,1]
    ]
    for i in range(3):
        for z in range(6):
            if choko[i][z]==0:
                choko_kara[i][z]=0
            if choko[i][z]==2:
                choko_kara[i][z]=2
            if choko[i][z]==3:
                choko_kara[i][z]=3

    a=0
    b=0
    for z in range(3):
        for i in range(4):
            a+=choko[z][i]
            if choko[z][i]==2:
                a-=1
            if choko[z][i]==3:
                a-=2
    for j in range(3):
        for x in range(2):
            b+=choko[j][x+4]
            if choko[j][x+4]==2:
                b-=1
            if choko[j][x+4]==3:
                b-=2

    if a < b:
        for i in range(3):
            for j in range(4):
                if choko[i][j]==0:
                    choko_kara[i][j]=0
                if choko[i][j]==1:
                    choko_kara[i][j]=4
                if choko[i][j]==2:
                    choko_kara[i][j]=5
                if choko[i][j]==3:
                    choko_kara[i][j]=6
    else:
        for i in range(3):
            for j in range(2):
                if choko[i][j+4]==0:
                    choko_kara[i][j+4]=0
                if choko[i][j+4]==1:
                    choko_kara[i][j+4]=4
                if choko[i][j+4]==2:
                    choko_kara[i][j+4]=5
                if choko[i][j+4]==3:
                    choko_kara[i][j+4]=6
    
    return choko_kara

def choko_yosoku_sita5():
    choko_kara=[
    [1,1,1,1,1,1],
    [1,1,1,1,1,1],
    [1,1,1,1,1,1]
    ]
    for i in range(3):
        for z in range(6):
            if choko[i][z]==0:
                choko_kara[i][z]=0
            if choko[i][z]==2:
                choko_kara[i][z]=2
            if choko[i][z]==3:
                choko_kara[i][z]=3

    for i in range(3):
        if choko[i][5]==0:
            choko_kara[i][5]=0
        if choko[i][5]==1:
            choko_kara[i][5]=4
        if choko[i][5]==2:
            choko_kara[i][5]=5
        if choko[i][5]==3:
            choko_kara[i][5]=6

    return choko_kara

def aijuuhuku():
    a=0
    b=0
    c=0
    d=0
    e=0
    f=0
    g=0

    if atari_migi1 == 1:
        a=1

    if atari_migi2 == 1:
        b=1

    if atari_sita1 == 1:
        c=1

    if atari_sita2 == 1:
        d=1

    if atari_sita3 == 1:
        e=1

    if atari_sita4 == 1:
        f=1
    
    if atari_sita5 == 1:
        g=1

    return (a,b,c,d,e,f,g)


def syuuryouhantei():
    a=0
    z=0
    for i in range(6):
        for j in range(3):
            if choko[j][i]==1:
                a+=1
            elif choko[j][i]==2:
                a+=1
            elif choko[j][i]==3:
                a+=1
    if a == 1:
        z=1
    return z


def syourihantei():
    a=0
    if playrtokutensougou<aitokutensougou:
        a=2
    elif playrtokutensougou==aitokutensougou:
        a=1
    return a


def tumeru_Kaiten():
    a=0
    b=0
    c=0
    d=0
    e=0
    f=0
    g=0
    h=0
    j=0
    z=0
 
    for i in range(6):
        a+=choko_moto[0][i]
        b+=choko_moto[1][i]
        z+=choko_moto[2][i]
    if a == 0:
        c+=-70
        if b == 0:
            c += -70
    if z == 0:
        c+=70
        if b == 0:
            c += 70
    
    for x in range(3):
        d+=choko_moto[x][0]
        e+=choko_moto[x][1]
        f+=choko_moto[x][2]
        g+=choko_moto[x][3]
        h+=choko_moto[x][4]
        
    if d == 0:
        j+=-90
        if e == 0:
            j+=-90
            if f == 0:
                j+=-90
                if g == 0:
                    j+=-90
                    if h == 0:
                        j+=-90
                       
    

    if h == 0:
        j+=90
        if g == 0:
            j+=90
            if f == 0:
                j+=90
                if e == 0:
                    j+=90
                    if d == 0:
                        j+=90

    return (c,j)


#チョコ右１の計算
def chokokeisanmigi1_choko():
    f=0
    g=0
    choko_kara=[
    [1,1,1,1,1,1],
    [1,1,1,1,1,1],
    [1,1,1,1,1,1]
    ]
    for z in range(6):
        if choko_moto[0][z]==0:
            choko_kara[0][z]=0
        if choko_moto[0][z]==2:
            choko_kara[0][z]=2
        if choko_moto[0][z]==3:
            choko_kara[0][z]=3
        
        

    

    for x in range(2):
        for y in range(6):
            if choko_moto[x+1][y]==1:
                choko_kara[x+1][y]=0
                g+=1
            elif choko_moto[x+1][y]==2:
                choko_kara[x+1][y]=0
                g+=2
            elif choko_moto[x+1][y]==3:
                choko_kara[x+1][y]=0
                g-=2
            else:
                choko_kara[x+1][y]=0
    f=choko_kara

    return (f,g)

#aki右１の計算
def chokokeisanmigi1_aki():
    aki_kara=[
    [1,1,1,1,1,1],
    [1,1,1,1,1,1],
    [1,1,1,1,1,1]
    ]
    y=0
    g=0
    h=0
    for i in range(2):
        for f in range(6):
            if choko_moto[i+1][f]==0:
                aki_kara[i+1][f]=0
            if choko_moto[i+1][f]==2:
                aki_kara[i+1][f]=2
            if choko_moto[i+1][f]==3:
                aki_kara[i+1][f]=3

    
    for y in range(6):
        if choko_moto[0][y]==1:
            aki_kara[0][y]=0
            h+=1
        elif choko_moto[0][y]==2:
            aki_kara[0][y]=0
            h+=2
        elif choko_moto[0][y]==3:
            aki_kara[0][y]=0
            h-=2    
        else :
            aki_kara[0][y]=0
    g=aki_kara

    return (g,h)

#右１の比較
def chokokeisanmigi1_gyaku():
    a=0
    b=0
    c=0
    d=0
 
    for i in range(6):
        a+=choko_moto[0][i]
        if choko_moto[0][i]==2:
            a-=1
        if choko_moto[0][i]==3:
            a-=2
        b+=choko_moto[1][i]
        if choko_moto[1][i]==2:
            b-=1
        if choko_moto[1][i]==3:
            b-=2
        c+=choko_moto[2][i]
        if choko_moto[2][i]==2:
            c-=1
        if choko_moto[2][i]==2:
            c-=2
    if a<(b+c):
        d=1
    return (d)



#チョコ右２の計算
def chokokeisanmigi2_choko():
    f=0
    g=0
    choko_kara=[
    [1,1,1,1,1,1],
    [1,1,1,1,1,1],
    [1,1,1,1,1,1]
    ]
    for x in range(2):
        for y in range(6):
            if choko_moto[x][y]==0:
                choko_kara[x][y]=0
            if choko_moto[x][y]==2:
                choko_kara[x][y]=2
            if choko_moto[x][y]==3:
                choko_kara[x][y]=3
                
    for z in range(6):
        if choko_moto[2][z]==1:
            choko_kara[2][z]=0
            g+=1
        elif choko_moto[2][z]==2:
            choko_kara[2][z]=0
            g+=2
        elif choko_moto[2][z]==3:
            choko_kara[2][z]=0
            g-=2
        else:
            choko_kara[2][z]=0
            
    f=choko_kara

    return (f,g)

#aki右2の計算
def chokokeisanmigi2_aki():
    aki_kara=[
    [1,1,1,1,1,1],
    [1,1,1,1,1,1],
    [1,1,1,1,1,1]
    ]
    y=0
    g=0
    
    
    for y in range(6):
        if choko_moto[2][y]==0:
            aki_kara[2][y]=0
        if choko_moto[2][y]==2:
            aki_kara[2][y]=2
        if choko_moto[2][y]==3:
            aki_kara[2][y]=3

    for i in range(2):
        for f in range(6):
            if choko_moto[i][f]==1:
                aki_kara[i][f]=0
            elif choko_moto[i][f]==2:
                aki_kara[i][f]=0
            elif choko_moto[i][f]==3:
                aki_kara[i][f]=0
            else:
                aki_kara[i][f]=0
    g=aki_kara
    return g

#チョコ下１の計算
def chokokeisansita1_choko():
    a=0
    b=0

    choko_kara=[
    [1,1,1,1,1,1],
    [1,1,1,1,1,1],
    [1,1,1,1,1,1]
    ]
    for i in range(3):
        if choko_moto[i][0]==0:
            choko_kara[i][0]=0
        if choko_moto[i][0]==2:
            choko_kara[i][0]=2
        if choko_moto[i][0]==3:
            choko_kara[i][0]=3
    
    for j in range(5):
        for x in range(3):
            if choko_moto[x][j+1]==1:
                choko_kara[x][j+1]=0
                b+=1
            elif choko_moto[x][j+1]==2:
                choko_kara[x][j+1]=0
                b+=2
            elif choko_moto[x][j+1]==3:
                choko_kara[x][j+1]=0
                b-=2
            else:
                choko_kara[x][j+1]=0
    a=choko_kara

    return (a,b)

#aki下１の計算
def chokokeisansita1_aki():
    a=0
    b=0
    aki_kara=[
    [1,1,1,1,1,1],
    [1,1,1,1,1,1],
    [1,1,1,1,1,1]
    ]
    for i in range(5):
        for j in range(3):
            if choko_moto[j][i+1]==0:
                aki_kara[j][i+1]=0
            if choko_moto[j][i+1]==2:
                aki_kara[j][i+1]=2
            if choko_moto[j][i+1]==3:
                aki_kara[j][i+1]=3
    
    for x in range(3):
        if choko_moto[x][0]==1:
            aki_kara[x][0]=0
            b+=1
        if choko_moto[x][0]==2:
            aki_kara[x][0]=0
            b+=2
        if choko_moto[x][0]==3:
            aki_kara[x][0]=0
            b-=2
        else:
            aki_kara[x][0]=0
    a=aki_kara

    return (a,b)

#下１の比較
def chokokeisansita1_gyaku():
    a=0
    b=0
    c=0
    for i in range(3):
        a+=choko_moto[i][0]
        if choko_moto[i][0]==2:
            a-=1
        if choko_moto[i][0]==3:
            a-=2

    for j in range(5):
        for x in range(3):
            b+=choko_moto[x][j+1]
            if choko_moto[x][j+1]==2:
                b-=1
            if choko_moto[x][j+1]==3:
                b-=2

    if a < b:
        c=1
    return c

#チョコ下2の計算
def chokokeisansita2_choko():
    a=0
    b=0
    choko_kara=[
    [1,1,1,1,1,1],
    [1,1,1,1,1,1],
    [1,1,1,1,1,1]
    ]
    for h in range(2):
        for i in range(3):
            if choko_moto[i][h]==0:
                choko_kara[i][h]=0
            if choko_moto[i][h]==2:
                choko_kara[i][h]=2
            if choko_moto[i][h]==3:
                choko_kara[i][h]=3
    
    for j in range(4):
        for x in range(3):
            if choko_moto[x][j+2]==1:
                choko_kara[x][j+2]=0
                b+=1
            elif choko_moto[x][j+2]==2:
                choko_kara[x][j+2]=0
                b+=2
            elif choko_moto[x][j+2]==3:
                choko_kara[x][j+2]=0
                b-=2
            else:
                choko_kara[x][j+2]=0

    a=choko_kara

    return (a,b)

#aki下2の計算
def chokokeisansita2_aki():
    a=0
    b=0
    aki_kara=[
    [1,1,1,1,1,1],
    [1,1,1,1,1,1],
    [1,1,1,1,1,1]
    ]
    for i in range(4):
        for j in range(3):
            if choko_moto[j][i+2]==0:
                aki_kara[j][i+2]=0
            if choko_moto[j][i+2]==2:
                aki_kara[j][i+2]=2
            if choko_moto[j][i+2]==3:
                aki_kara[j][i+2]=3



    for x in range(2):
        for z in range(3):
            if choko_moto[z][x]==1:
                aki_kara[z][x]=0
                b+=1
            if choko_moto[z][x]==2:
                aki_kara[z][x]=0
                b+=2
            if choko_moto[z][x]==3:
                aki_kara[z][x]=0
                b-=2
            else:
                aki_kara[z][x]=0
    a=aki_kara

    return (a,b)

#下2の比較
def chokokeisansita2_gyaku():
    a=0
    b=0
    c=0
    for z in range(3):
        for i in range(2):
            a+=choko_moto[z][i]
            if choko_moto[z][i]==2:
                a-=1
            if choko_moto[z][i]==3:
                a-=2

    for j in range(3):
        for x in range(4):
            b+=choko_moto[j][x+2]
            if choko_moto[j][x+2]==2:
                b-=1
            if choko_moto[j][x+2]==3:
                b-=2
    if a < b:
        c=1
    return c

#チョコ下3の計算
def chokokeisansita3_choko():
    a=0
    b=0
    choko_kara=[
    [1,1,1,1,1,1],
    [1,1,1,1,1,1],
    [1,1,1,1,1,1]
    ]
    for h in range(3):
        for i in range(3):
            if choko_moto[i][h]==0:
                choko_kara[i][h]=0
            if choko_moto[i][h]==2:
                choko_kara[i][h]=2
            if choko_moto[i][h]==3:
                choko_kara[i][h]=3
    
    for j in range(3):
        for x in range(3):
            if choko_moto[x][j+3]==1:
                choko_kara[x][j+3]=0
                b+=1
            elif choko_moto[x][j+3]==2:
                choko_kara[x][j+3]=0
                b+=2
            elif choko_moto[x][j+3]==3:
                choko_kara[x][j+3]=0
                b-=2
            else:
                choko_kara[x][j+3]=0

    a=choko_kara

    return (a,b)

#aki下3の計算
def chokokeisansita3_aki():
    a=0
    b=0
    aki_kara=[
    [1,1,1,1,1,1],
    [1,1,1,1,1,1],
    [1,1,1,1,1,1]
    ]
    for i in range(3):
        for j in range(3):
            if choko_moto[j][i+3]==0:
                aki_kara[j][i+3]=0
            if choko_moto[j][i+3]==2:
                aki_kara[j][i+3]=2
            if choko_moto[j][i+3]==3:
                aki_kara[j][i+3]=3

    for x in range(3):
        for z in range(3):
            if choko_moto[z][x]==1:
                aki_kara[z][x]=0
                b+=1
            if choko_moto[z][x]==2:
                aki_kara[z][x]=0
                b+=2
            if choko_moto[z][x]==3:
                aki_kara[z][x]=0
                b-=2
            else:
                aki_kara[z][x]=0
    a=aki_kara

    return (a,b)

#下3の比較
def chokokeisansita3_gyaku():
    a=0
    b=0
    c=0
    for z in range(3):
        for i in range(3):
            a+=choko_moto[z][i]
            if choko_moto[z][i]==2:
                a-=1
            if choko_moto[z][i]==3:
                a-=2


    for j in range(3):
        for x in range(3):
            b+=choko_moto[j][x+3]
            if choko_moto[j][x+3]==2:
                b-=1
            if choko_moto[j][x+3]==3:
                b-=2
    if a < b:
        c=1
    return c

#チョコ下4の計算
def chokokeisansita4_choko():
    a=0
    b=0
    
    choko_kara=[
    [1,1,1,1,1,1],
    [1,1,1,1,1,1],
    [1,1,1,1,1,1]
    ]
    for h in range(4):
        for i in range(3):
            if choko_moto[i][h]==0:
                choko_kara[i][h]=0
            if choko_moto[i][h]==2:
                choko_kara[i][h]=2
            if choko_moto[i][h]==3:
                choko_kara[i][h]=3
    
    for j in range(2):
        for x in range(3):
            if choko_moto[x][j+4]==1:
                choko_kara[x][j+4]=0
                b+=1
            elif choko_moto[x][j+4]==2:
                choko_kara[x][j+4]=0
                b+=2
            elif choko_moto[x][j+4]==3:
                choko_kara[x][j+4]=0
                b-=2
            else:
                choko_kara[x][j+4]=0

    a=choko_kara

    return (a,b)

#aki下4の計算
def chokokeisansita4_aki():
    a=0
    b=0

    aki_kara=[
    [1,1,1,1,1,1],
    [1,1,1,1,1,1],
    [1,1,1,1,1,1]
    ]
    for i in range(2):
        for j in range(3):
            if choko_moto[j][i+4]==0:
                aki_kara[j][i+4]=0
            if choko_moto[j][i+4]==2:
                aki_kara[j][i+4]=2
            if choko_moto[j][i+4]==3:
                aki_kara[j][i+4]=3

    for x in range(4):
        for z in range(3):
            if choko_moto[z][x]==1:
                aki_kara[z][x]=0
                b+=1
            if choko_moto[z][x]==2:
                aki_kara[z][x]=0
                b+=2
            if choko_moto[z][x]==3:
                aki_kara[z][x]=0
                b-=2
            else:
                aki_kara[z][x]=0
    a=aki_kara

    return (a,b)

#下4の比較
def chokokeisansita4_gyaku():
    a=0
    b=0
    c=0
    for z in range(3):
        for i in range(4):
            a+=choko_moto[z][i]
            if choko_moto[z][i]==2:
                a-=1
            if choko_moto[z][i]==3:
                a-=2

    for j in range(3):
        for x in range(2):
            b+=choko_moto[j][x+4]
            if choko_moto[j][x+4]==2:
                b-=1
            if choko_moto[j][x+4]==3:
                b-=2
    if a < b:
        c=1
    return c


#チョコ下5の計算
def chokokeisansita5_choko():
    a=0
    b=0
    choko_kara=[
    [1,1,1,1,1,1],
    [1,1,1,1,1,1],
    [1,1,1,1,1,1]
    ]
    for j in range(5):
        for x in range(3):
            if choko_moto[x][j]==0:
                choko_kara[x][j]=0
            if choko_moto[x][j]==2:
                choko_kara[x][j]=2
            if choko_moto[x][j]==3:
                choko_kara[x][j]=3

    for i in range(3):
        if choko_moto[i][5]==1:
            choko_kara[i][5]=0
            b+=1
        if choko_moto[i][5]==2:
            choko_kara[i][5]=0
            b+=2
        if choko_moto[i][5]==3:
            choko_kara[i][5]=0
            b-=2
        else:
            choko_kara[i][5]=0
    a=choko_kara

    return (a,b)

#aki下5の計算
def chokokeisansita5_aki():
    a=0
    aki_kara=[
    [1,1,1,1,1,1],
    [1,1,1,1,1,1],
    [1,1,1,1,1,1]
    ]
    for i in range(3):
        if choko_moto[i][5]==0:
            aki_kara[i][5]=0
        if choko_moto[i][5]==2:
            aki_kara[i][5]=2
        if choko_moto[i][5]==3:
            aki_kara[i][5]=3

    
    for j in range(3):
        for x in range(5):
            if choko_moto[j][x]==1:
                aki_kara[j][x]=0
            if choko_moto[j][x]==2:
                aki_kara[j][x]=0
            if choko_moto[j][x]==3:
                aki_kara[j][x]=0
            else:
                aki_kara[j][x]=0
    a=aki_kara
    return (a)

  
nannido=0



scene = 0 #シーンの初期値
roundsuu=0
playrtokutensougou=0
aitokutensougou=0
tennsuukioku=0
tennsuukioku1=0
game=True
kasorux=1920/2
kasoruy=1080/2
pygame.mouse.set_visible(False)
pygame.mouse.set_pos((kasorux,kasoruy))

while game:
    randomchoko_y = random.randint(0,2)
    randomchoko_x = random.randint(0,5)
    choko1randomchoko_y = 0
    choko1randomchoko_x = 0
    randomchoko_y1 = 0
    randomchoko_x1 = 0
    choko1randomchoko_y1 = 0
    choko1randomchoko_x1 = 0
    
    # チョコ表示リストと空白表示リスト
    choko=[
        [1,1,1,1,1,1],
        [1,1,1,1,1,1],
        [1,1,1,1,1,1]
    ]
    choko[randomchoko_y][randomchoko_x] = 2
    while True:
        choko1randomchoko_y=random.randint(0,2)
        choko1randomchoko_x=random.randint(0,5)
        if randomchoko_x==0 or randomchoko_x==1 or randomchoko_x==2:
            if choko1randomchoko_x==3 or choko1randomchoko_x==4 or choko1randomchoko_x==5:
                if choko1randomchoko_y!=randomchoko_y:
                    choko[choko1randomchoko_y][choko1randomchoko_x]=2
                    break
        if randomchoko_x==3 or randomchoko_x==4 or randomchoko_x==5:
            if choko1randomchoko_x==0 or choko1randomchoko_x==1 or choko1randomchoko_x==2:
                if choko1randomchoko_y!=randomchoko_y:
                    choko[choko1randomchoko_y][choko1randomchoko_x]=2
                    break
    while True:
        randomchoko_y1=random.randint(0,2)
        randomchoko_x1=random.randint(0,5)
        if randomchoko_y1 != randomchoko_y and randomchoko_x1 != randomchoko_x:
            if randomchoko_y1 != choko1randomchoko_y and randomchoko_x1 != choko1randomchoko_x:
                choko[randomchoko_y1][randomchoko_x1]=3
                break
    while True:
        choko1randomchoko_y1=random.randint(0,2)
        choko1randomchoko_x1=random.randint(0,5)
        if randomchoko_x1==0 or randomchoko_x1==1 or randomchoko_x1==2:
            if choko1randomchoko_x1==3 or choko1randomchoko_x1==4 or choko1randomchoko_x1==5:
                if choko1randomchoko_y1!=randomchoko_y1:
                    if choko1randomchoko_y1!=randomchoko_y and choko1randomchoko_x1!=randomchoko_x:
                        if choko1randomchoko_x1!=choko1randomchoko_x:      
                            choko[choko1randomchoko_y1][choko1randomchoko_x1]=3
                            break
        if randomchoko_x1==3 or randomchoko_x1==4 or randomchoko_x1==5:
            if choko1randomchoko_x1==0 or choko1randomchoko_x1==1 or choko1randomchoko_x1==2:
                if choko1randomchoko_y1!=randomchoko_y1:
                    if choko1randomchoko_y1!=randomchoko_y and choko1randomchoko_x1!=randomchoko_x:
                        if choko1randomchoko_x1!=choko1randomchoko_x:
                            choko[choko1randomchoko_y1][choko1randomchoko_x1]=3
                            break
    choko_yosoku=choko
    


    aki=[
        [0,0,0,0,0,0],
        [0,0,0,0,0,0],
        [0,0,0,0,0,0]
    ]
    aki1=[
        [0,0,0,0,0,0],
        [0,0,0,0,0,0],
        [0,0,0,0,0,0]
    ]
    choko_moto=[
        [0,0,0,0,0,0],
        [0,0,0,0,0,0],
        [0,0,0,0,0,0]
    ]
    if roundsuu==0:
        playrtokutensougou=0
        aitokutensougou=0


    

    # セルの余白の設定
    top_margin = 300 # 上部の余白
    total_cell_width = len(choko[0]) * cell_width
    total_cell_width1 = len(aki[0]) * cell_width
    left_margin = (width - total_cell_width) // 2 # 画面中央に配置
    left_margin1 = (width - total_cell_width1) // 2 # 画面中央に配置

    #初期値設定
    rotation_angle = 0 # 回転角度の初期値
    angle = 0 #角度を通常に戻す変数
    tumeru = 0 #横幅の余白の初期値　
    
    hantei=0
    syouri=0
    senkou=0
    ataru_x=0
    ataru_y=0
    sentaku=[0,0,0,0,0,0,0]

    kaiten_width = 0 #回転の位置
    kaiten_width1 = 0
    kaiten_height = 0 #回転の位置
    kaiten_height1 = 0
    margin_width = 0 #横に詰める量
    margin_height = 0 #縦に詰める量
    yoserumigi = 0
    yoserusita = 0 
    
    playrtokuten=0
    playrtokuten1=0
    aitokuten=0
    aitokuten1=0
    hyouji=0

    font = pygame.font.SysFont("hg創英角ｺﾞｼｯｸub",100)
    


    gyaku=0
    gyaku_hantei=0

    butann_sita1_sakujo = 0 #ボタンを消すための変数
    butann_sita2_sakujo = 0
    butann_sita3_sakujo = 0
    butann_sita4_sakujo = 0
    butann_sita5_sakujo = 0
    butann_migi1_sakujo = 0
    butann_migi2_sakujo = 0

    atari_sita1 = 0 #ボタンの当たり判定削除のための変数
    atari_sita2 = 0
    atari_sita3 = 0
    atari_sita4 = 0
    atari_sita5 = 0
    atari_migi1 = 0
    atari_migi2 = 0

    migisita=0 #右ボタンが押されたか下ボタンが押されたか
    q=0
    z=0

    tumeru_kaiten = 0
    tumeru_kaiten1 = 0
    tumeru_tate = 0
    tumeru_tate1 = 0
    tumeru_tate2 = 0
    #ボタンインスタンス
    butann_migi1 = Button(409+margin_width,436+margin_height,butann_migi_img,1,0)
    butann_migi2 = Button(409+margin_width,573+margin_height,butann_migi_img,1,0)
    butann_sita1 = Button(604+margin_width,268+margin_height,butann_sita_img,1,1)
    butann_sita2 = Button(764+margin_width,268+margin_height,butann_sita_img,1,1)
    butann_sita3 = Button(924+margin_width,268+margin_height,butann_sita_img,1,1)
    butann_sita4 = Button(1084+margin_width,268+margin_height,butann_sita_img,1,1)
    butann_sita5 = Button(1244+margin_width,268+margin_height,butann_sita_img,1,1)
    butann_title_hajime = titleButton(1000,268,butann_title_img1,1)
    butann_title_asobi = titleButton(124,268,butann_title_img2,1)
    butann_title_easy = titleButton(1000,268,butann_title_img3,1)
    butann_title_hard = titleButton(124,268,butann_title_img4,1)
    butann_asobikata_batu= titleButton(124,268,butann_asobikata_batu_img,1)
    butann_asobikata_hidari = titleButton(124,268,butann_asobikata_hidari_img,1)
    butann_asobikata_migi = titleButton(124,268,butann_asobikata_migi_img,1)
    butann_Retry = titleButton(1000,268,butann_title_img5,1)
    butann_Title = titleButton(124,268,butann_title_img6,1)
    AIplay=0
    AIplaylist=[1,2,3,4,5,6,7]
    AIturn=True
    playr = 0 #プレイヤーのターンを示す初期値
    if roundsuu==1:
        playr = 1
    AIsentaku1=0
    AIsentaku2=0
    AIsentaku3=0
    AIsentaku4=0
    AIsentaku5=0
    AIsentaku6=0
    AIsentaku7=0
    AIsentakukaisuu1=0
    AIsentakukaisuu2=0
    AIsentakukaisuu3=0
    AIsentakukaisuu4=0
    AIsentakukaisuu5=0
    AIsentakukaisuu6=0
    AIsentakukaisuu7=0
    ataru_a=0
    yosoku=0
    kakutei=[0,0,0,0,0,0,0]
    yosoku_hituyou=0
    choko_yosoku_toki=0
    tomeru=0
    tomeru1=0
    tomeru2=0
    suuji=0
    suuji1=0
    suuji2=0
    suuji3=0
    #ゲームプレイのループ
    running=True
    while running:
        
        

        
        
        #タイトル画面
        if scene == 0:
            
            screen.blit(image_haikei,rect_bg)
            
            for event in pygame .event.get():
                if event.type==MOUSEMOTION:
                    kasorux,kasoruy = event.pos
                if event.type == pygame.QUIT: #ウィンドウの×ボタンが押された時ゲーム終了
                    running = False
                    game = False
                    
                if event.type == pygame.KEYDOWN: #もし何かキーが押された時実行
                    if event.key == pygame.K_ESCAPE: #もし押されたキーがESCキーならゲームを終了
                        running = False
                        game = False
            if butann_title_hajime.titledraw(butann_title_img1):
                randomsound,choko_sound=random_sound(randomsound)
                choko_sound.play(0)
                time.sleep(1.2)
                scene=3 #対戦画面に移行
            if butann_title_asobi.titledraw(butann_title_img2):
                randomsound,choko_sound=random_sound(randomsound)
                choko_sound.play(0)
                time.sleep(1.2)
                scene=4
            butann_title_hajime = titleButton(900,920,butann_title_img1,1)
            butann_title_asobi = titleButton(1300,920,butann_title_img2,1)


        if scene == 3:
            screen.blit(image_haikei2,rect_bg2)
            butann_title_easy = titleButton(680,330,butann_title_img3,1)
            butann_title_hard = titleButton(680,630,butann_title_img4,1)
            for event in pygame .event.get():
                if event.type==MOUSEMOTION:
                    kasorux,kasoruy = event.pos
                if event.type == pygame.QUIT: #ウィンドウの×ボタンが押された時ゲーム終了
                    running = False
                    game = False
                    
                if event.type == pygame.KEYDOWN: #もし何かキーが押された時実行
                    if event.key == pygame.K_ESCAPE: #もし押されたキーがESCキーならゲームを終了
                        running = False
                        game = False
            if butann_title_easy.titledraw(butann_title_img3):
                nannido = 0
                randomsound,choko_sound=random_sound(randomsound)
                choko_sound.play(0)
                time.sleep(0.8)
                scene=1 #対戦画面に移行
            if butann_title_hard.titledraw(butann_title_img4):
                nannido = 1
                randomsound,choko_sound=random_sound(randomsound)
                choko_sound.play(0)
                time.sleep(0.8)
                scene=1 #対戦画面に移行
            text7=font.render("難易度",True,(0,0,0))
            screen.blit(text7,[775,190])
            

        
        if scene == 4:
            screen.blit(asobikata_img,rect_bg)
            for event in pygame .event.get():
                if event.type == pygame.QUIT: #ウィンドウの×ボタンが押された時ゲーム終了
                    running = False
                    game = False
                if event.type==MOUSEMOTION:
                    kasorux,kasoruy = event.pos
                    
                if event.type == pygame.KEYDOWN: #もし何かキーが押された時実行
                    if event.key == pygame.K_ESCAPE: #もし押されたキーがESCキーならゲームを終了
                        running = False
                        game = False

            butann_asobikata_batu= titleButton(1780,30,butann_asobikata_batu_img,1)
            butann_asobikata_migi = titleButton(1780,490,butann_asobikata_migi_img,1)
            if butann_asobikata_migi.titledraw(butann_asobikata_migi_img):
                randomsound,choko_sound=random_sound(randomsound)
                choko_sound.play(0)
                time.sleep(0.3)
                scene=5
            
            if butann_asobikata_batu.titledraw(butann_asobikata_batu_img):
                randomsound,choko_sound=random_sound(randomsound)
                choko_sound.play(0)
                time.sleep(0.3)
                scene=0
        
        if scene == 5:
            screen.blit(asobikata_img1,rect_bg)
            for event in pygame .event.get():
                if event.type == pygame.QUIT: #ウィンドウの×ボタンが押された時ゲーム終了
                    running = False
                    game = False
                if event.type==MOUSEMOTION:
                    kasorux,kasoruy = event.pos
                    
                if event.type == pygame.KEYDOWN: #もし何かキーが押された時実行
                    if event.key == pygame.K_ESCAPE: #もし押されたキーがESCキーならゲームを終了
                        running = False
                        game = False

            butann_asobikata_batu= titleButton(1780,30,butann_asobikata_batu_img,1)
            butann_asobikata_migi = titleButton(1780,490,butann_asobikata_migi_img,1)
            butann_asobikata_hidari = titleButton(45,490,butann_asobikata_hidari_img,1)
            
            if butann_asobikata_migi.titledraw(butann_asobikata_migi_img):
                randomsound,choko_sound=random_sound(randomsound)
                choko_sound.play(0)
                time.sleep(0.3)
                scene=6
            if butann_asobikata_hidari.titledraw(butann_asobikata_hidari_img):
                randomsound,choko_sound=random_sound(randomsound)
                choko_sound.play(0)
                time.sleep(0.3)
                scene=4
            if butann_asobikata_batu.titledraw(butann_asobikata_batu_img):
                randomsound,choko_sound=random_sound(randomsound)
                choko_sound.play(0)
                time.sleep(0.3)
                scene=0
        
        if scene == 6:
            screen.blit(asobikata_img2,rect_bg)
            for event in pygame .event.get():
                if event.type == pygame.QUIT: #ウィンドウの×ボタンが押された時ゲーム終了
                    running = False
                    game = False
                if event.type==MOUSEMOTION:
                    kasorux,kasoruy = event.pos
                if event.type == pygame.KEYDOWN: #もし何かキーが押された時実行
                    if event.key == pygame.K_ESCAPE: #もし押されたキーがESCキーならゲームを終了
                        running = False
                        game = False

            butann_asobikata_batu= titleButton(1780,30,butann_asobikata_batu_img,1)
            butann_asobikata_migi = titleButton(1780,490,butann_asobikata_migi_img,1)
            butann_asobikata_hidari = titleButton(45,490,butann_asobikata_hidari_img,1)
            if butann_asobikata_migi.titledraw(butann_asobikata_migi_img):
                randomsound,choko_sound=random_sound(randomsound)
                choko_sound.play(0)
                time.sleep(0.3)
                scene=7
            if butann_asobikata_hidari.titledraw(butann_asobikata_hidari_img):
                randomsound,choko_sound=random_sound(randomsound)
                choko_sound.play(0)
                time.sleep(0.3)
                scene=5
            if butann_asobikata_batu.titledraw(butann_asobikata_batu_img):
                randomsound,choko_sound=random_sound(randomsound)
                choko_sound.play(0)
                time.sleep(0.3)
                scene=0
        
        if scene == 7:
            screen.blit(asobikata_img3,rect_bg)
            for event in pygame .event.get():
                if event.type == pygame.QUIT: #ウィンドウの×ボタンが押された時ゲーム終了
                    running = False
                    game = False
                if event.type==MOUSEMOTION:
                    kasorux,kasoruy = event.pos
                if event.type == pygame.KEYDOWN: #もし何かキーが押された時実行
                    if event.key == pygame.K_ESCAPE: #もし押されたキーがESCキーならゲームを終了
                        running = False
                        game = False

            butann_asobikata_batu= titleButton(1780,30,butann_asobikata_batu_img,1)
            butann_asobikata_hidari = titleButton(45,490,butann_asobikata_hidari_img,1)
            
            if butann_asobikata_hidari.titledraw(butann_asobikata_hidari_img):
                randomsound,choko_sound=random_sound(randomsound)
                choko_sound.play(0)
                time.sleep(0.3)
                scene=6
            if butann_asobikata_batu.titledraw(butann_asobikata_batu_img):
                randomsound,choko_sound=random_sound(randomsound)
                choko_sound.play(0)
                time.sleep(0.3)
                scene=0


        if angle == 1:
            suuji=0
            randomsound,choko_sound=random_sound(randomsound)
            choko_sound.play(0)
            if playr == 1:
                if playrtokuten>=0:
                    text10=purasu_img
                    suuji=playrtokuten
                else :
                    text10=mainasu_img
                    suuji=(playrtokuten*-1)
            if playr == 3:
                if aitokuten>=0:
                    text11=purasu_img
                    suuji=aitokuten
                else :
                    text11=mainasu_img
                    suuji=(aitokuten*-1)


            if suuji==0:
                suuji=suuji0_img
            elif suuji==1:
                suuji=suuji1_img
            elif suuji==2:
                suuji=suuji2_img
            elif suuji==3:
                suuji=suuji3_img
            elif suuji==4:
                suuji=suuji4_img
            elif suuji==5:
                suuji=suuji5_img
            elif suuji==6:
                suuji=suuji6_img
            elif suuji==7:
                suuji=suuji7_img
            elif suuji==8:
                suuji=suuji8_img
            elif suuji==9:
                suuji=suuji9_img

            for i in range(1):
                c=0
                for d in range(7):
                    if playr == 1:
                        if playrtokuten>=0:
                            screen.blit(text10,[355,218-c])
                        else:
                            screen.blit(text10,[355,239-c])
                        screen.blit(suuji,[420,200-c])
                    if playr == 3:
                        if aitokuten>=0:
                            screen.blit(text11,[1335,218-c])
                        else:
                            screen.blit(text11,[1335,239-c])
                        screen.blit(suuji,[1400,200-c])
                    c+=7
                    screen.blit(rotated_image, rotated_rect.topleft)
                    screen.blit(rotated_image1, rotated_rect1.topleft)
                
                    pygame.display.update()
                    time.sleep(0.01)
                    screen.blit(image_haikei1,rect_bg1)

            time.sleep(0.9)
            rotation_angle =15
            rotation_angle -= 15 # 15度右に回転
            aki= [
                [0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0]
                ]
            aki1=[
                [0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0]
                ]
            angle=0
            yosoku_hituyou=0
            hantei=syuuryouhantei()
            

        
        

                    
                    

        

        #対戦シーン
        if scene == 1:
            if playr==0:
                if yosoku_hituyou==0:
                    choko_yosoku=choko
                    choko_yosoku_toki=0
                    choko_yosoku_1=choko_yosoku_migi1()
                    choko_yosoku_2=choko_yosoku_migi2()
                    choko_yosoku_3=choko_yosoku_sita1()
                    choko_yosoku_4=choko_yosoku_sita2()
                    choko_yosoku_5=choko_yosoku_sita3()
                    choko_yosoku_6=choko_yosoku_sita4()
                    choko_yosoku_7=choko_yosoku_sita5()

                    yosoku_hituyou=1


            kakutei[0]=butann_migi1.yosoku()
            kakutei[1]=butann_migi2.yosoku()
            kakutei[2]=butann_sita1.yosoku()
            kakutei[3]=butann_sita2.yosoku()
            kakutei[4]=butann_sita3.yosoku()
            kakutei[5]=butann_sita4.yosoku()
            kakutei[6]=butann_sita5.yosoku()
            if (kakutei[0]+kakutei[1]+kakutei[2]+kakutei[3]+kakutei[4]+kakutei[5]+kakutei[6])==0:
                alpha=0
                yosoku=0
                image_choko3.set_alpha(alpha)  # 透過度の設定
                
            if kakutei[0]==1:
                choko_yosoku=choko_yosoku_1
                if yosoku==0:
                    alpha+=1
                    if alpha==90:
                        yosoku=1
                if yosoku==1:
                    alpha-=1
                    if alpha==0:
                        yosoku=0
                
                image_choko3.set_alpha(alpha)  # 透過度の設定
                pygame.display.update()

            if kakutei[1]==1:
                choko_yosoku=choko_yosoku_2
                if yosoku==0:
                    alpha+=1
                    if alpha==90:
                        yosoku=1
                if yosoku==1:
                    alpha-=1
                    if alpha==0:
                        yosoku=0
                
                image_choko3.set_alpha(alpha)  # 透過度の設定
                pygame.display.update()

            if kakutei[2]==1:
                choko_yosoku=choko_yosoku_3
                if yosoku==0:
                    alpha+=1
                    if alpha==90:
                        yosoku=1
                if yosoku==1:
                    alpha-=1
                    if alpha==0:
                        yosoku=0
                
                image_choko3.set_alpha(alpha)  # 透過度の設定
                pygame.display.update()

            if kakutei[3]==1:
                choko_yosoku=choko_yosoku_4
                if yosoku==0:
                    alpha+=1
                    if alpha==90:
                        yosoku=1
                if yosoku==1:
                    alpha-=1
                    if alpha==0:
                        yosoku=0
                
                image_choko3.set_alpha(alpha)  # 透過度の設定
                pygame.display.update()

            if kakutei[4]==1:
                choko_yosoku=choko_yosoku_5
                if yosoku==0:
                    alpha+=1
                    if alpha==90:
                        yosoku=1
                if yosoku==1:
                    alpha-=1
                    if alpha==0:
                        yosoku=0
                
                image_choko3.set_alpha(alpha)  # 透過度の設定
                pygame.display.update()
            
            if kakutei[5]==1:
                choko_yosoku=choko_yosoku_6
                if yosoku==0:
                    alpha+=1
                    if alpha==90:
                        yosoku=1
                if yosoku==1:
                    alpha-=1
                    if alpha==0:
                        yosoku=0
                
                image_choko3.set_alpha(alpha)  # 透過度の設定
                pygame.display.update()
            
            if kakutei[6]==1:
                choko_yosoku=choko_yosoku_7
                if yosoku==0:
                    alpha+=1
                    if alpha==90:
                        yosoku=1
                if yosoku==1:
                    alpha-=1
                    if alpha==0:
                        yosoku=0
                
                image_choko3.set_alpha(alpha)  # 透過度の設定
                pygame.display.update()

            for event in pygame .event.get():
                if event.type==MOUSEMOTION:
                    kasorux,kasoruy = event.pos
                if event.type == pygame.QUIT: #ウィンドウの×ボタンが押された時ゲーム終了
                    running = False
                    game = False
                if event.type == pygame.KEYDOWN: #もし何かキーが押された時実行
                    if event.key == pygame.K_ESCAPE: #もし押されたキーがESCキーならゲームを終了
                        running = False
                        game = False
                    
                        
                        
                    



                if scene == 1:
                    if angle==0:
                        
                        if hantei == 0 : 
                            if playr == 0:
                                


                                if atari_migi1 == 0:
                                    if butann_migi1.draw(butann_migi_img,2) :
                                        rotation_angle -= 4 # 15度左に回転
                                        choko_moto=choko
                                        #チョコを割る計算
                                        choko,playrtokuten=chokokeisanmigi1_choko()
                                        aki,playrtokuten1=chokokeisanmigi1_aki()            
                                        gyaku_hantei = chokokeisanmigi1_gyaku()
                                        if gyaku_hantei == 1:
                                            aki1=choko
                                            playrtokuten=playrtokuten1
                                            gyaku=1
                                        playrtokutensougou+=playrtokuten
                                        tumeru_tate2=1
                                        angle=1
                                        migisita=1
                                        playr=1
                                        senkou=1
                                        choko_yosoku_toki=1
                                        
                                if atari_migi2 == 0:
                                    if butann_migi2.draw(butann_migi_img,2) :
                                        rotation_angle -= 4 # 15度左に回転
                                        choko_moto=choko
                                        #チョコを割る計算
                                        choko,playrtokuten=chokokeisanmigi2_choko()
                                        aki=chokokeisanmigi2_aki()
                                        playrtokutensougou+=playrtokuten

                                        angle=1
                                        migisita=1
                                        playr=1
                                        senkou=1
                                        choko_yosoku_toki=1
                                        

                                if atari_sita1 == 0:
                                    
                                    if butann_sita1.draw(butann_sita_img,2) :
                                        rotation_angle += 15 # 15度左に回転
                                        choko_moto=choko
                                        choko,playrtokuten=chokokeisansita1_choko()
                                        aki,playrtokuten1=chokokeisansita1_aki()
                                        gyaku_hantei = chokokeisansita1_gyaku()
                                        if gyaku_hantei == 1:
                                            aki1=choko
                                            gyaku=1
                                            playrtokuten=playrtokuten1

                                        playrtokutensougou+=playrtokuten
                                        kaiten_height,kaiten_height1=yoseru_sita1()
                                        angle=1
                                        migisita=2
                                        playr=1
                                        senkou=1
                                        choko_yosoku_toki=1
                                    
                                        
                                        
                                if atari_sita2 == 0:
                                    if butann_sita2.draw(butann_sita_img,2) :
                                        rotation_angle += 15 # 15度左に回転
                                        choko_moto=choko
                                        choko,playrtokuten=chokokeisansita2_choko()
                                        aki,playrtokuten1 = chokokeisansita2_aki()
                                        gyaku_hantei = chokokeisansita2_gyaku()
                                        if gyaku_hantei == 1:
                                            aki1=choko
                                            gyaku=1
                                            playrtokuten=playrtokuten1

                                        playrtokutensougou+=playrtokuten
                                        kaiten_height,kaiten_height1=yoseru_sita2()
                                        angle=1
                                        migisita=2
                                        playr=1
                                        senkou=1
                                        choko_yosoku_toki=1
                                        

                                if atari_sita3 == 0:
                                    if senkou == 1:
                                        if butann_sita3.draw(butann_sita_img,2) :
                                            rotation_angle += 15 # 15度左に回転
                                            choko_moto=choko
                                            choko,playrtokuten=chokokeisansita3_choko()
                                            aki,playrtokuten1 = chokokeisansita3_aki()
                                            gyaku_hantei = chokokeisansita3_gyaku()
                                            if gyaku_hantei == 1:
                                                aki1=choko
                                                gyaku=1
                                                playrtokuten=playrtokuten1

                                            playrtokutensougou+=playrtokuten
                                            kaiten_height,kaiten_height1=yoseru_sita3()
                                            angle=1
                                            migisita=2
                                            playr=1
                                            senkou=1
                                            choko_yosoku_toki=1
                                        

                                if atari_sita4 == 0:
                                    if butann_sita4.draw(butann_sita_img,2) :
                                        rotation_angle += 15 # 15度左に回転
                                        choko_moto=choko
                                        choko,playrtokuten=chokokeisansita4_choko()
                                        aki,playrtokuten1 = chokokeisansita4_aki()
                                        gyaku_hantei = chokokeisansita4_gyaku()
                                        if gyaku_hantei == 1:
                                            aki1=choko
                                            gyaku=1
                                            playrtokuten=playrtokuten1
                                    
                                        playrtokutensougou+=playrtokuten
                                        kaiten_height,kaiten_height1=yoseru_sita4()
                                        angle=1
                                        migisita=2
                                        playr=1
                                        senkou=1
                                        choko_yosoku_toki=1

                                if atari_sita5 == 0:
                                    if butann_sita5.draw(butann_sita_img,2) :
                                        rotation_angle += 15 # 15度左に回転
                                        choko_moto=choko
                                        choko,playrtokuten=chokokeisansita5_choko()
                                        aki = chokokeisansita5_aki()

                                        playrtokutensougou+=playrtokuten
                                        kaiten_height,kaiten_height1=yoseru_sita5()
                                        angle=1
                                        migisita=2
                                        playr=1
                                        senkou=1
                                        choko_yosoku_toki=1
                            
                                

                                        
                                                
                    
                            

        if hantei == 0:
            if playr == 2 :
                time.sleep(random.uniform(0.8,1.6))
                choko_yosoku_toki=1
                AIsentaku1,AIsentaku2,AIsentaku3,AIsentaku4,AIsentaku5,AIsentaku6,AIsentaku7=aijuuhuku()
                if nannido==0:
                    if len(AIplaylist)==1:
                        AIplay=AIplaylist[0]
                    else:
                    
                    
                        if AIsentaku1==1:
                            if AIsentakukaisuu1==0:
                                AIplaylist.remove(1)
                                AIsentakukaisuu1=1
            
                        if AIsentaku2==1:
                            if AIsentakukaisuu2==0:
                                AIplaylist.remove(2)
                                AIsentakukaisuu2=1
                        
                        if AIsentaku3==1:
                            if AIsentakukaisuu3==0:
                                AIplaylist.remove(3)
                                AIsentakukaisuu3=1

                        if AIsentaku4==1:
                            if AIsentakukaisuu4==0:
                                AIplaylist.remove(4)
                                AIsentakukaisuu4=1
                    
                        if AIsentaku5==1:
                            if AIsentakukaisuu5==0:
                                AIplaylist.remove(5)
                                AIsentakukaisuu5=1
                        
                        if AIsentaku6==1:
                            if AIsentakukaisuu6==0:
                                AIplaylist.remove(6)
                                AIsentakukaisuu6=1
                        
                        if AIsentaku7==1:
                            if AIsentakukaisuu7==0:
                                AIplaylist.remove(7)
                                AIsentakukaisuu7=1
                        while True:
                            AIplay=random.choice(AIplaylist)
                            if senkou==0:
                                if AIplay==1 or AIplay==2 or AIplay==3 or AIplay==4 or AIplay==6 or AIplay==7:
                                    break
                            else:
                                break
                if nannido==1:
                    if AIsentaku1==1:
                        if AIsentakukaisuu1==0:
                            AIplaylist.remove(1)
                            AIsentakukaisuu1=1
        
                    if AIsentaku2==1:
                        if AIsentakukaisuu2==0:
                            AIplaylist.remove(2)
                            AIsentakukaisuu2=1
                    
                    if AIsentaku3==1:
                        if AIsentakukaisuu3==0:
                            AIplaylist.remove(3)
                            AIsentakukaisuu3=1

                    if AIsentaku4==1:
                        if AIsentakukaisuu4==0:
                            AIplaylist.remove(4)
                            AIsentakukaisuu4=1
                
                    if AIsentaku5==1:
                        if AIsentakukaisuu5==0:
                            AIplaylist.remove(5)
                            AIsentakukaisuu5=1
                    
                    if AIsentaku6==1:
                        if AIsentakukaisuu6==0:
                            AIplaylist.remove(6)
                            AIsentakukaisuu6=1
                    
                    if AIsentaku7==1:
                        if AIsentakukaisuu7==0:
                            AIplaylist.remove(7)
                            AIsentakukaisuu7=1
                    sentaku=[0,0,0,0,0,0,0]
                    if AIsentaku1==0:
                        sentaku[0]=AIsentakukeisan1()
                    else:
                        sentaku[0]=-99
                    if AIsentaku2==0:
                        sentaku[1]=AIsentakukeisan2()
                    else:
                        sentaku[1]=-99
                    if AIsentaku3==0:
                        sentaku[2]=AIsentakukeisan3()
                    else:
                        sentaku[2]=-99
                    if AIsentaku4==0:
                        sentaku[3]=AIsentakukeisan4()
                    else:
                        sentaku[3]=-99
                    if senkou==1:
                        if AIsentaku5==0:
                            sentaku[4]=AIsentakukeisan5()
                        else:
                            sentaku[4]=-99
                    else:
                        sentaku[4]=-99
                    if AIsentaku6==0:
                        sentaku[5]=AIsentakukeisan6()
                    else:
                        sentaku[5]=-99
                    if AIsentaku7==0:
                        sentaku[6]=AIsentakukeisan7()
                    else:
                        sentaku[6]=-99

                    sentakusuu=0
                    saikousentaku=sentaku[0]
                    for i in range(7):
                        if saikousentaku<sentaku[i]:
                            sentakusuu=i
                            saikousentaku=sentaku[i]
                    sentakusuu+=1
                    if sentakusuu==1:
                        AIplay=1
                    if sentakusuu==2:
                        AIplay=2
                    if sentakusuu==3:
                        AIplay=3
                    if sentakusuu==4:
                        AIplay=4
                    if sentakusuu==5:
                        AIplay=5
                    if sentakusuu==6:
                        AIplay=6
                    if sentakusuu==7:
                        AIplay=7


                            


                if AIplay==1 :
                    rotation_angle -= 4 # 15度左に回転
                    choko_moto=choko
                    #チョコを割る計算
                    choko,aitokuten=chokokeisanmigi1_choko()
                    aki,aitokuten1=chokokeisanmigi1_aki()            
                    gyaku_hantei = chokokeisanmigi1_gyaku()
                    if gyaku_hantei == 1:
                        aki1=choko
                        aitokuten=aitokuten1
                        gyaku=1
                    aitokutensougou+=aitokuten
                    tumeru_tate2=1
                    angle=1
                    migisita=1
                    senkou=1
                
                        

                if AIplay==2 :
                    rotation_angle -= 4 # 15度左に回転
                    choko_moto=choko
                    #チョコを割る計算
                    choko,aitokuten=chokokeisanmigi2_choko()
                    aki=chokokeisanmigi2_aki()
                    aitokutensougou+=aitokuten

                    angle=1
                    migisita=1
                    senkou=1
                    
                        
                    
                if AIplay==3 :
                    rotation_angle += 15 # 15度左に回転
                    choko_moto=choko
                    choko,aitokuten=chokokeisansita1_choko()
                    aki,aitokuten1=chokokeisansita1_aki()
                    gyaku_hantei = chokokeisansita1_gyaku()
                    if gyaku_hantei == 1:
                        aki1=choko
                        gyaku=1
                        aitokuten=aitokuten1

                    aitokutensougou+=aitokuten
                    kaiten_height,kaiten_height1=yoseru_sita1()
                    angle=1
                    migisita=2
                    senkou=1
                
                    
                if AIplay==4 :
                    rotation_angle += 15 # 15度左に回転
                    choko_moto=choko
                    choko,aitokuten=chokokeisansita2_choko()
                    aki,aitokuten1 = chokokeisansita2_aki()
                    gyaku_hantei = chokokeisansita2_gyaku()
                    if gyaku_hantei == 1:
                        aki1=choko
                        gyaku=1
                        aitokuten=aitokuten1

                    aitokutensougou+=aitokuten
                    kaiten_height,kaiten_height1=yoseru_sita2()
                    angle=1
                    migisita=2
                    senkou=1
                    
                        

                if AIplay==5 :
                    rotation_angle += 15 # 15度左に回転
                    choko_moto=choko
                    choko,aitokuten=chokokeisansita3_choko()
                    aki,aitokuten1 = chokokeisansita3_aki()
                    gyaku_hantei = chokokeisansita3_gyaku()
                    if gyaku_hantei == 1:
                        aki1=choko
                        gyaku=1
                        aitokuten=aitokuten1

                    aitokutensougou+=aitokuten
                    kaiten_height,kaiten_height1=yoseru_sita3()
                    angle=1
                    migisita=2
                    senkou=1
                    
                    
                if AIplay==6 :
                    rotation_angle += 15 # 15度左に回転
                    choko_moto=choko
                    choko,aitokuten=chokokeisansita4_choko()
                    aki,aitokuten1 = chokokeisansita4_aki()
                    gyaku_hantei = chokokeisansita4_gyaku()
                    if gyaku_hantei == 1:
                        aki1=choko
                        gyaku=1
                        aitokuten=aitokuten1
                    
                    aitokutensougou+=aitokuten
                    kaiten_height,kaiten_height1=yoseru_sita4()
                    angle=1
                    migisita=2
                    senkou=1
                    
                        
                    
                if AIplay==7 :
                    rotation_angle += 15 # 15度左に回転
                    choko_moto=choko
                    choko,aitokuten=chokokeisansita5_choko()
                    aki = chokokeisansita5_aki()

                    aitokutensougou+=aitokuten
                    kaiten_height,kaiten_height1=yoseru_sita5()
                    angle=1
                    migisita=2
                    senkou=1
                    
                playr = 3
        
        if hantei == 1:
            if q==0:
                if playr == 0 or playr==2: 
                    if angle == 0:
                        if playr==0:
                            playrtokuten=5
                            playrtokutensougou+=5
                            text10=purasu_img
                            suuji=playrtokuten
                        if playr==2:
                            aitokuten=5
                            aitokutensougou+=5
                            text11=purasu_img
                            suuji=aitokuten
                       
                        if suuji==0:
                            suuji=suuji0_img
                        elif suuji==1:
                            suuji=suuji1_img
                        elif suuji==2:
                            suuji=suuji2_img
                        elif suuji==3:
                            suuji=suuji3_img
                        elif suuji==4:
                            suuji=suuji4_img
                        elif suuji==5:
                            suuji=suuji5_img
                        elif suuji==6:
                            suuji=suuji6_img
                        elif suuji==7:
                            suuji=suuji7_img
                        elif suuji==8:
                            suuji=suuji8_img
                        elif suuji==9:
                            suuji=suuji9_img

                        for i in range(1):
                            c=0
                            time.sleep(0.4)
                            for d in range(8):
                                if playr == 0:
                                    screen.blit(text10,[355,218-c])
                                    screen.blit(suuji,[420,200-c])
                                if playr == 2:
                                    screen.blit(text11,[1335,218-c])
                                    screen.blit(suuji,[1400,200-c])
                                c+=7
                                screen.blit(rotated_image, rotated_rect.topleft)
                                screen.blit(rotated_image1, rotated_rect1.topleft)
                            
                                pygame.display.update()
                                time.sleep(0.01)
                                screen.blit(image_haikei1,rect_bg1)                       
                        time.sleep(0.8)
                        screen.fill(background_color)
                        if roundsuu==0:
                            roundsuu+=1
                            running = False
                            tennsuukioku=0
                            tennsuukioku1=0
                        else:
                            scene=2
                            

                    q=1
            
                        

                        
        


        # すべてのセルを一つの画像に合成
        combined_image = pygame.Surface((cell_width * 6, cell_height * 3), pygame.SRCALPHA)
        combined_image1 = pygame.Surface((cell_width * 6, cell_height * 3), pygame.SRCALPHA)

        if choko_yosoku_toki==0:
            y = 0
            for row in choko_yosoku:
                x = 0
                for cell in row:
                    if cell == 1:
                        combined_image.blit(image_choko, (x, y))
                    if cell == 2:
                        combined_image.blit(image_choko1, (x, y))
                    if cell == 3:
                        combined_image.blit(image_choko2, (x, y))
                    if cell == 4:
                        combined_image.blit(image_choko, (x, y))
                        combined_image.blit(image_choko3, (x, y))
                    if cell == 5:
                        combined_image.blit(image_choko1, (x, y))
                        combined_image.blit(image_choko3, (x, y))
                    if cell == 6:
                        combined_image.blit(image_choko2, (x, y))
                        combined_image.blit(image_choko3, (x, y))
                    x += cell_width
                y += cell_height
        if choko_yosoku_toki==1:
            y = 0
            for row in choko:
                x = 0
                for cell in row:
                    if cell == 1:
                        combined_image.blit(image_choko, (x, y))
                    if cell == 2:
                        combined_image.blit(image_choko1, (x, y))
                    if cell == 3:
                        combined_image.blit(image_choko2, (x, y))
                    x += cell_width
                y += cell_height
            y=0
            for row in aki:
                x = 0
                for cell in row:
                    if cell == 1:
                        combined_image1.blit(image_choko, (x, y))
                    if cell == 2:
                        combined_image1.blit(image_choko1, (x, y))
                    if cell == 3:
                        combined_image1.blit(image_choko2, (x, y))
                    x += cell_width
                y += cell_height

        margin_height,margin_width=margin()

        if angle == 0:
            # 画像を描写

            rotated_image = pygame.transform.rotate(combined_image, rotation_angle)
            rotated_image1 = pygame.transform.rotate(combined_image1, -rotation_angle)
            rotated_rect = rotated_image.get_rect(center=((width // 2)+margin_width, (height // 2)+margin_height))
            rotated_rect1 = rotated_image1.get_rect(center=((width // 2)+margin_width, (height // 2)+margin_height))
            
        if angle == 1:
            # 画像を回転
            tumeru_kaiten,tumeru_kaiten1 = tumeru_Kaiten()
            if migisita == 1:
                tumeru_tate,tumeru_tate1=tumeru_Tate()
                if tumeru_tate2 == 0:
                    
                    rotated_image = pygame.transform.rotate(combined_image, rotation_angle)
                    rotated_image1 = pygame.transform.rotate(combined_image1, -rotation_angle)
                    rotated_rect = rotated_image.get_rect(center=((width // 2)+tumeru_kaiten1, (height // 2)-35+tumeru_tate+tumeru_kaiten))
                    rotated_rect1 = rotated_image1.get_rect(center=((width // 2)+tumeru_kaiten1, (height // 2)+35+tumeru_tate1+tumeru_kaiten))
                else :
                    tumeru_tate2 = 0
                    rotated_image = pygame.transform.rotate(combined_image, rotation_angle)
                    rotated_image1 = pygame.transform.rotate(combined_image1, -rotation_angle)
                    rotated_rect = rotated_image.get_rect(center=((width // 2)+45+tumeru_kaiten1, (height // 2)-35+tumeru_tate+tumeru_kaiten))
                    rotated_rect1 = rotated_image1.get_rect(center=((width // 2)+45+tumeru_kaiten1, (height // 2)+35+tumeru_tate1+tumeru_kaiten))    
            if migisita == 2:
                rotated_image = pygame.transform.rotate(combined_image, rotation_angle)
                rotated_image1 = pygame.transform.rotate(combined_image1, -rotation_angle)
                rotated_rect = rotated_image.get_rect(center=((width // 2)-50+tumeru_kaiten1, (height // 2)+kaiten_height+tumeru_kaiten))
                rotated_rect1 = rotated_image1.get_rect(center=((width // 2)+60+tumeru_kaiten1, (height // 2)+kaiten_height1+tumeru_kaiten))
            if gyaku == 1 :
                choko = aki
                aki = aki1
                gyaku = 0
        if scene == 1:
            # 画面をクリア
            screen.blit(image_haikei1,rect_bg1)
        
        
            
        
        if scene == 1:
            # 画像、ボタンを描画
            
            if angle == 0:
                if playr == 0 or playr ==1:
                    
                
                    yoserumigi,yoserusita=tumeru_Button()#ボタンの描写位置を計算
                    if atari_migi1 == 0:
                        butann_migi1 = Button(409+margin_width+yoserumigi,436+margin_height,butann_migi_img,1,0)
                    if atari_migi2 == 0:
                        butann_migi2 = Button(409+margin_width+yoserumigi,573+margin_height,butann_migi_img,1,0)
                    if atari_sita1 == 0:
                        butann_sita1 = Button(604+margin_width,268+margin_height+yoserusita,butann_sita_img,1,1)
                    if atari_sita2 == 0:
                        butann_sita2 = Button(764+margin_width,268+margin_height+yoserusita,butann_sita_img,1,1)
                    if atari_sita3 == 0:
                        if senkou == 1:
                            butann_sita3 = Button(924+margin_width,268+margin_height+yoserusita,butann_sita_img,1,1)
                    if atari_sita4 == 0:
                        butann_sita4 = Button(1084+margin_width,268+margin_height+yoserusita,butann_sita_img,1,1)
                    if atari_sita5 == 0:
                        butann_sita5 = Button(1244+margin_width,268+margin_height+yoserusita,butann_sita_img,1,1)

                    atari_migi1,atari_migi2,atari_sita1,atari_sita2,atari_sita3,atari_sita4,atari_sita5=draw_Button() #ボタン描写                                       
                    if playr==1:
                        playr=2
                if playr==3:
                    playr=0                
            if playr == 0:
                screen.blit(you_img,[570,65])
                screen.blit(turn_img,[930,65])
            if playr == 2:
                screen.blit(enemy_img,[570,65])
                screen.blit(turn_img,[930,65])
            
            

            screen.blit(rotated_image, rotated_rect.topleft)
            screen.blit(rotated_image1, rotated_rect1.topleft)
        
            
            #結果画面
        if scene == 2:
            for event in pygame .event.get():
                if event.type == pygame.QUIT: #ウィンドウの×ボタンが押された時ゲーム終了
                    running = False
                    game = False
                if event.type==MOUSEMOTION:
                    kasorux,kasoruy = event.pos
                if event.type == pygame.KEYDOWN: #もし何かキーが押された時実行
                    if event.key == pygame.K_ESCAPE: #もし押されたキーがESCキーならゲームを終了
                        running = False
                        game = False
                    
                        
            screen.blit(image_haikei2,rect_bg2)
            screen.blit(enemy_img,[1350,150])
            screen.blit(you_img,[220,120])
            if tomeru==0:
                pygame.display.update()
                randomsound,choko_sound=random_sound(randomsound)
                choko_sound.play(0)
                time.sleep(1.3)
                if len(str(playrtokutensougou))==2:
                    suuji=(int(str(playrtokutensougou)[-1]))
                    suuji1=(int(str(playrtokutensougou)[-2]))
                    if suuji==0:
                        suuji=suuji0_img
                    elif suuji==1:
                        suuji=suuji1_img
                    elif suuji==2:
                        suuji=suuji2_img
                    elif suuji==3:
                        suuji=suuji3_img
                    elif suuji==4:
                        suuji=suuji4_img
                    elif suuji==5:
                        suuji=suuji5_img
                    elif suuji==6:
                        suuji=suuji6_img
                    elif suuji==7:
                        suuji=suuji7_img
                    elif suuji==8:
                        suuji=suuji8_img
                    elif suuji==9:
                        suuji=suuji9_img

                    if suuji1==0:
                        suuji1=suuji0_img
                    elif suuji1==1:
                        suuji1=suuji1_img
                    elif suuji1==2:
                        suuji1=suuji2_img
                    elif suuji1==3:
                        suuji1=suuji3_img
                    elif suuji1==4:
                        suuji1=suuji4_img
                    elif suuji1==5:
                        suuji1=suuji5_img
                    elif suuji1==6:
                        suuji1=suuji6_img
                    elif suuji1==7:
                        suuji1=suuji7_img
                    elif suuji1==8:
                        suuji1=suuji8_img
                    elif suuji1==9:
                        suuji1=suuji9_img
                    

                else:
                    suuji=(int(str(playrtokutensougou)[-1]))
                    if suuji==0:
                        suuji=suuji0_img
                    elif suuji==1:
                        suuji=suuji1_img
                    elif suuji==2:
                        suuji=suuji2_img
                    elif suuji==3:
                        suuji=suuji3_img
                    elif suuji==4:
                        suuji=suuji4_img
                    elif suuji==5:
                        suuji=suuji5_img
                    elif suuji==6:
                        suuji=suuji6_img
                    elif suuji==7:
                        suuji=suuji7_img
                    elif suuji==8:
                        suuji=suuji8_img
                    elif suuji==9:
                        suuji=suuji9_img

                if len(str(aitokutensougou))==2:
                    suuji2=(int(str(aitokutensougou)[-1]))
                    suuji3=(int(str(aitokutensougou)[-2]))
                    if suuji2==0:
                        suuji2=suuji0_img
                    elif suuji2==1:
                        suuji2=suuji1_img
                    elif suuji2==2:
                        suuji2=suuji2_img
                    elif suuji2==3:
                        suuji2=suuji3_img
                    elif suuji2==4:
                        suuji2=suuji4_img
                    elif suuji2==5:
                        suuji2=suuji5_img
                    elif suuji2==6:
                        suuji2=suuji6_img
                    elif suuji2==7:
                        suuji2=suuji7_img
                    elif suuji2==8:
                        suuji2=suuji8_img
                    elif suuji2==9:
                        suuji2=suuji9_img
                    
                    if suuji3==0:
                        suuji3=suuji0_img
                    elif suuji3==1:
                        suuji3=suuji1_img
                    elif suuji3==2:
                        suuji3=suuji2_img
                    elif suuji3==3:
                        suuji3=suuji3_img
                    elif suuji3==4:
                        suuji3=suuji4_img
                    elif suuji3==5:
                        suuji3=suuji5_img
                    elif suuji3==6:
                        suuji3=suuji6_img
                    elif suuji3==7:
                        suuji3=suuji7_img
                    elif suuji3==8:
                        suuji3=suuji8_img
                    elif suuji3==9:
                        suuji3=suuji9_img
                else:
                    suuji2=(int(str(aitokutensougou)[-1]))
                    if suuji2==0:
                        suuji2=suuji0_img
                    elif suuji2==1:
                        suuji2=suuji1_img
                    elif suuji2==2:
                        suuji2=suuji2_img
                    elif suuji2==3:
                        suuji2=suuji3_img
                    elif suuji2==4:
                        suuji2=suuji4_img
                    elif suuji2==5:
                        suuji2=suuji5_img
                    elif suuji2==6:
                        suuji2=suuji6_img
                    elif suuji2==7:
                        suuji2=suuji7_img
                    elif suuji2==8:
                        suuji2=suuji8_img
                    elif suuji2==9:
                        suuji2=suuji9_img

                tomeru=1
            
            if (playrtokutensougou>=20):
                screen.blit(bouru_hidari3_img,rect_bg2)
            elif (playrtokutensougou>=10):
                screen.blit(bouru_hidari2_img,rect_bg2)
            else:
                screen.blit(bouru_hidari1_img,rect_bg2)
            if (aitokutensougou>=20):
                screen.blit(bouru_migi3_img,rect_bg2)
            elif(aitokutensougou>=10):
                screen.blit(bouru_migi2_img,rect_bg2)
            else:
                screen.blit(bouru_migi1_img,rect_bg2)

            if len(str(playrtokutensougou))==2:
                screen.blit(suuji,[760,350])
                screen.blit(suuji1,[680,350])
            else:
                screen.blit(suuji,[680,350])

            if len(str(aitokutensougou))==2:
                screen.blit(suuji2,[1160,350])
                screen.blit(suuji3,[1080,350])
            else:
                screen.blit(suuji2,[1080,350])
            
            

            
            

            if tomeru1==0:
                pygame.display.update()
                randomsound,choko_sound=random_sound(randomsound)
                choko_sound.play(0)
                time.sleep(1.3)
                tomeru1=1

            
            if tomeru2==0:
                syouri=syourihantei()
            if syouri==0:
                screen.blit(win_img,[630,770])
            elif syouri==1:
                screen.blit(image_drow,[630,770])
            else:
                screen.blit(lose_img,[620,770])
            if tomeru2==0:
                pygame.display.update()
                randomsound,choko_sound=random_sound(randomsound)
                choko_sound.play(0)
                time.sleep(1.3)
                tomeru2=1


            
            
            
            butann_Retry = titleButton(1420,890,butann_title_img5,1)
            butann_Title = titleButton(0,890,butann_title_img6,1)

            if butann_Retry.titledraw(butann_title_img5):
                randomsound,choko_sound=random_sound(randomsound)
                choko_sound.play(0)
                time.sleep(0.8)
                scene=1
                roundsuu=0
                playrtokutensougou=0
                aitokutensougou=0
                tennsuukioku=0
                tennsuukioku1=0
                running=False
                
            if butann_Title.titledraw(butann_title_img6):
                randomsound,choko_sound=random_sound(randomsound)
                choko_sound.play(0)
                time.sleep(0.8)
                roundsuu=0
                playrtokutensougou=0
                aitokutensougou=0
                tennsuukioku=0
                tennsuukioku1=0
                scene=0
                running=False
        
       
        screen.blit(image_kasoru,((kasorux-2),(kasoruy-27)))
        #画面を更新
        pygame.display.update()
        #画面のフレームレートを制御
        clock.tick(60)  # フレームレートを1秒間に60フレームに設定



pygame.quit()
sys.exit()
